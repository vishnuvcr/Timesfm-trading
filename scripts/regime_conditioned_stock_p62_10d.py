from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter
from src.stats.forecast_metrics import spearman_rank_ic

CONTEXT = 128
LOOKBACK = 20
HORIZON = 10
FOLDS = 4
ORIGINS_PER_FOLD = 8
TOP_K = 6
SYMBOLS = (
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "SBIN", "ITC",
    "BHARTIARTL", "LT", "AXISBANK", "KOTAKBANK", "HINDUNILVR", "MARUTI",
    "SUNPHARMA", "BAJFINANCE", "ASIANPAINT", "TITAN", "HCLTECH", "WIPRO",
    "ULTRACEMCO", "NESTLEIND", "M&M", "NTPC", "ONGC", "POWERGRID",
    "TATAMOTORS", "TATASTEEL", "ADANIENT", "CIPLA", "DRREDDY",
)
COSTS = (0.00125, 0.0025, 0.00375, 0.0050)
CAPITAL = 1_000_000.0
BROKERAGE_PER_ORDER = 20.0
DP_SELL = 13.5
REGIMES = ("all", "risk_on", "breadth_low", "trend_down", "high_vol")


def load_series(path: Path) -> tuple[list[str], np.ndarray, np.ndarray]:
    dates, prices, turnover = [], [], []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"date", "adj_close", "turnover"}
        if not required.issubset(reader.fieldnames or []):
            raise RuntimeError(f"{path}: missing {required - set(reader.fieldnames or [])}")
        for row in reader:
            dates.append(row["date"][:10])
            prices.append(float(row["adj_close"]))
            turnover.append(float(row["turnover"]))
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: unsorted/duplicate dates")
    return dates, np.log(np.asarray(prices, dtype=np.float32)), np.asarray(turnover, dtype=float)


def load_action_dates(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if "ex_date" not in (reader.fieldnames or []):
            return set()
        return {row["ex_date"][:10] for row in reader if row.get("ex_date")}


def fold_origins(n: int) -> list[np.ndarray]:
    start = CONTEXT + LOOKBACK + 5
    end = n - HORIZON - 1
    edges = np.linspace(start, end + 1, FOLDS + 1, dtype=int)
    out = []
    for f in range(FOLDS):
        a, b = int(edges[f]), int(edges[f + 1] - 1)
        if b < a or (b - a + 1) < ORIGINS_PER_FOLD:
            raise RuntimeError(f"fold {f+1} too short: {a}:{b}")
        out.append(np.unique(np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int)))
    return out


def exact_signflip_pvalue(fold_diffs: np.ndarray) -> float:
    fold_diffs = np.asarray(fold_diffs, dtype=float)
    observed = abs(float(np.mean(fold_diffs)))
    total = 0
    extreme = 0
    for mask in range(1 << len(fold_diffs)):
        signs = np.array([1.0 if ((mask >> i) & 1) else -1.0 for i in range(len(fold_diffs))])
        if abs(float(np.mean(fold_diffs * signs))) >= observed - 1e-15:
            extreme += 1
        total += 1
    return float(extreme / total)


def bh_adjust(pvals: list[float]) -> list[float]:
    m = len(pvals)
    order = np.argsort(pvals)
    out = np.ones(m, dtype=float)
    running = 1.0
    for rank in range(m, 0, -1):
        idx = int(order[rank - 1])
        running = min(running, float(pvals[idx]) * m / rank)
        out[idx] = min(1.0, running)
    return out.tolist()


def market_state(
    date_index: int,
    common_dates: list[str],
    raw: dict,
    idx: dict,
    symbols: list[str],
) -> dict:
    daily = []
    momentum = []
    turns = []
    for s in symbols:
        j = idx[s][common_dates[date_index]]
        lp = raw[s]["logp"]
        hist = lp[j - LOOKBACK + 1:j + 1]
        daily.append(np.diff(hist))
        momentum.append(float(lp[j] - lp[j - LOOKBACK]))
        start = max(0, j - LOOKBACK + 1)
        turns.append(float(np.mean(raw[s]["turnover"][start:j + 1])))
    daily = np.asarray(daily, dtype=float)
    momentum = np.asarray(momentum, dtype=float)
    market_20d = float(np.mean(momentum))
    market_vol = float(np.std(np.mean(daily, axis=0)))

    past_vols = []
    for p in range(max(LOOKBACK + 5, date_index - 252), date_index):
        d = common_dates[p]
        vals = []
        for s in symbols:
            j = idx[s][d]
            if j < LOOKBACK:
                continue
            lp = raw[s]["logp"][j - LOOKBACK + 1:j + 1]
            vals.append(float(np.std(np.diff(lp))))
        if vals:
            past_vols.append(float(np.mean(vals)))
    vol_threshold = float(np.median(past_vols)) if past_vols else market_vol
    high_vol = market_vol >= vol_threshold
    breadth = float(np.mean(momentum > 0))
    return {
        "market_20d_return": market_20d,
        "market_vol": market_vol,
        "breadth": breadth,
        "turnover": np.asarray(turns),
        "risk_on": (market_20d >= 0.0) and (breadth >= 0.50) and (not high_vol),
        "breadth_low": breadth < 0.50,
        "trend_down": market_20d < 0.0,
        "high_vol": high_vol,
    }


def select_weights(scores: np.ndarray, eligible: np.ndarray) -> np.ndarray:
    w = np.zeros(len(scores), dtype=float)
    idxs = np.flatnonzero(eligible)
    if len(idxs) < TOP_K:
        return w
    picks = idxs[np.argsort(scores[idxs])[-TOP_K:]]
    w[picks] = 1.0 / TOP_K
    return w


def trade_cost(old_w: np.ndarray, new_w: np.ndarray, capital: float, rate: float) -> float:
    delta = np.abs(new_w - old_w)
    traded = float(delta.sum() * capital)
    sells = int(np.sum((old_w > 1e-12) & (new_w < 1e-12)))
    buys = int(np.sum((new_w > 1e-12) & (old_w < 1e-12)))
    resizes = int(np.sum((delta > 1e-12) & (old_w > 1e-12) & (new_w > 1e-12)))
    return traded * rate + (sells + buys + 2 * resizes) * BROKERAGE_PER_ORDER + sells * DP_SELL


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--actions-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="p6_2_10d_results")
    args = ap.parse_args()

    symbols = list(SYMBOLS)
    raw, actions = {}, {}
    for s in symbols:
        dates, logp, turnover = load_series(Path(args.data_dir) / f"{s}.csv")
        raw[s] = {"dates": dates, "logp": logp, "turnover": turnover}
        actions[s] = load_action_dates(Path(args.actions_dir) / f"{s}_actions.csv")

    common_dates = sorted(set(raw[symbols[0]]["dates"]).intersection(*[set(raw[s]["dates"]) for s in symbols[1:]]))
    if len(common_dates) < 400:
        raise RuntimeError("common history too short")
    idx = {s: {d: i for i, d in enumerate(raw[s]["dates"])} for s in symbols}

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    rows = []
    for fold_no, origins in enumerate(fold_origins(len(common_dates)), start=1):
        for oi in origins:
            date = common_dates[int(oi)]
            contexts, future, momentum = [], [], []
            for s in symbols:
                j = idx[s][date]
                contexts.append(raw[s]["logp"][j - CONTEXT:j].copy())
                momentum.append(float(raw[s]["logp"][j] - raw[s]["logp"][j - LOOKBACK]))
                future.append(float(np.exp(raw[s]["logp"][j + HORIZON] - raw[s]["logp"][j]) - 1.0))

            outputs = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=True, univariate=True)
            tfm = np.asarray([
                float(np.asarray(o.forecast).reshape(-1)[-1] - contexts[k][-1])
                for k, o in enumerate(outputs)
            ])
            future = np.asarray(future, dtype=float)
            momentum = np.asarray(momentum, dtype=float)
            state = market_state(int(oi), common_dates, raw, idx, symbols)

            eligible = np.zeros(len(symbols), dtype=bool)
            top_liq = np.argsort(state["turnover"])[-20:]
            eligible[top_liq] = True
            for k, s in enumerate(symbols):
                j = idx[s][date]
                prior = set(raw[s]["dates"][max(0, j - 5):j + 1])
                if actions[s].intersection(prior):
                    eligible[k] = False

            rows.append({
                "fold": fold_no, "date": date, "future": future, "timesfm": tfm,
                "momentum": momentum, "eligible": eligible,
                **{k: v for k, v in state.items() if k != "turnover"},
            })

    regime_masks = {
        "all": lambda r: True,
        "risk_on": lambda r: bool(r["risk_on"]),
        "breadth_low": lambda r: bool(r["breadth_low"]),
        "trend_down": lambda r: bool(r["trend_down"]),
        "high_vol": lambda r: bool(r["high_vol"]),
    }

    metrics = []
    for name, fn in regime_masks.items():
        subset = [r for r in rows if fn(r)]
        ics, excess = [], []
        for r in subset:
            eligible = r["eligible"]
            if np.sum(eligible) < TOP_K:
                continue
            ix = np.flatnonzero(eligible)
            ics.append(float(spearman_rank_ic(r["timesfm"][ix], r["future"][ix])))
            msel = ix[np.argsort(r["momentum"][ix])[-TOP_K:]]
            tsel = ix[np.argsort(r["timesfm"][ix])[-TOP_K:]]
            excess.append(float(np.mean(r["future"][tsel]) - np.mean(r["future"][msel])))
        metrics.append({
            "regime": name,
            "rebalances": len(subset),
            "eligible_rebalances": len(ics),
            "rank_ic_mean": float(np.mean(ics)) if ics else float("nan"),
            "timesfm_minus_momentum_mean_top6_return": float(np.mean(excess)) if excess else float("nan"),
        })

    # Predeclared economic overlays: use TimesFM ranking only inside the regime, otherwise stay in momentum.
    strategy_defs = {
        "timesfm_all": lambda r: True,
        "timesfm_risk_on_overlay": lambda r: bool(r["risk_on"]),
        "timesfm_breadth_low_overlay": lambda r: bool(r["breadth_low"]),
        "timesfm_trend_down_overlay": lambda r: bool(r["trend_down"]),
        "timesfm_high_vol_overlay": lambda r: bool(r["high_vol"]),
    }

    fold_strategy_returns = []
    strategy_rows = []
    for cost in COSTS:
        for strategy, condition in strategy_defs.items():
            by_fold = []
            for fold_no in range(1, FOLDS + 1):
                cap = CAPITAL
                old_m = np.zeros(len(symbols))
                old_t = np.zeros(len(symbols))
                current_momentum = np.zeros(len(symbols))
                test_rows = [r for r in rows if r["fold"] == fold_no]
                for r in test_rows:
                    eligible = r["eligible"]
                    if np.sum(eligible) < TOP_K:
                        continue
                    m = select_weights(r["momentum"], eligible)
                    use_tfm = bool(condition(r))
                    t = select_weights(r["timesfm"], eligible)
                    new = t if use_tfm else m
                    gross = float(np.dot(new, r["future"]))
                    fee = trade_cost(old_t, new, cap, cost)
                    net = (gross * cap - fee) / cap
                    cap *= max(0.0, 1.0 + net)
                    old_t = new
                    current_momentum = m
                    # Independent momentum control on the same origins/costs.
                    gross_m = float(np.dot(m, r["future"]))
                    fee_m = trade_cost(old_m, m, CAPITAL if not by_fold else cap, cost)
                    # To keep the comparator economically consistent, maintain it in a separate accumulator below.
                # recompute separate control cleanly
                cap_m = CAPITAL
                old = np.zeros(len(symbols))
                for r in test_rows:
                    if np.sum(r["eligible"]) < TOP_K:
                        continue
                    m = select_weights(r["momentum"], r["eligible"])
                    g = float(np.dot(m, r["future"]))
                    fee = trade_cost(old, m, cap_m, cost)
                    n = (g * cap_m - fee) / cap_m
                    cap_m *= max(0.0, 1.0 + n)
                    old = m
                by_fold.append({
                    "fold": fold_no,
                    "strategy_net_return": cap / CAPITAL - 1.0,
                    "momentum_net_return": cap_m / CAPITAL - 1.0,
                    "excess": (cap / CAPITAL - 1.0) - (cap_m / CAPITAL - 1.0),
                })
            diffs = np.asarray([x["excess"] for x in by_fold], dtype=float)
            strategy_rows.append({
                "strategy": strategy,
                "one_way_cost": cost,
                "net_total_return": float(np.prod([1.0 + x["strategy_net_return"] for x in by_fold]) - 1.0),
                "momentum_control_net_total_return": float(np.prod([1.0 + x["momentum_net_return"] for x in by_fold]) - 1.0),
                "mean_fold_excess": float(np.mean(diffs)),
                "exact_four_fold_signflip_p": exact_signflip_pvalue(diffs),
            })
            fold_strategy_returns.append({"strategy": strategy, "cost": cost, "folds": by_fold})

    # BH per cost across the five predeclared economic strategies.
    for cost in COSTS:
        ix = [i for i, x in enumerate(strategy_rows) if x["one_way_cost"] == cost]
        q = bh_adjust([strategy_rows[i]["exact_four_fold_signflip_p"] for i in ix])
        for i, qv in zip(ix, q):
            strategy_rows[i]["bh_q"] = qv

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "origin_state.csv").open("w", encoding="utf-8", newline="") as fh:
        fields = ["fold","date","risk_on","breadth_low","trend_down","high_vol","market_20d_return","market_vol","breadth","eligible_count"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({**{k:r[k] for k in fields[:-1]}, "eligible_count": int(np.sum(r["eligible"]))})
    (out / "regime_metrics.json").write_text(json.dumps(metrics, indent=2) + "
", encoding="utf-8")
    (out / "strategy_results.json").write_text(json.dumps(strategy_rows, indent=2) + "
", encoding="utf-8")
    (out / "fold_strategy_returns.json").write_text(json.dumps(fold_strategy_returns, indent=2) + "
", encoding="utf-8")
    (out / "summary.json").write_text(json.dumps({
        "lane":"P6.2_10d_timesfm_regime_conditioning",
        "horizon":HORIZON,"stocks":len(symbols),"folds":FOLDS,"origins_per_fold":ORIGINS_PER_FOLD,
        "top_k":TOP_K,"costs":COSTS,"regime_cells":list(regime_masks),
        "event_rule":"exclude names with an ex-date in preceding 5 trading sessions",
        "liquidity_rule":"top 20 of 30 by trailing 20-session turnover at origin",
        "note":"Exploratory. Final promotion requires PIT universe reconciliation and Phase 7 effective-date cost/slippage/capacity validation.",
    }, indent=2) + "
", encoding="utf-8")
    print(json.dumps({"regime_metrics":metrics,"strategy_results":strategy_rows}, indent=2))


if __name__ == "__main__":
    main()
