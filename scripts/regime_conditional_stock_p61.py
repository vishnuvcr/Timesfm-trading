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
HORIZON = 5
TOP_K = 6
FOLDS = 4
ORIGINS_PER_FOLD = 8
ONE_WAY_COSTS = (0.0, 0.0025, 0.0050)


def zscore(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    sd = float(np.std(x))
    if sd <= 1e-12:
        return np.zeros_like(x)
    return (x - float(np.mean(x))) / sd


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    X = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return y - X @ beta


def load_prices(path: Path) -> tuple[list[str], np.ndarray, np.ndarray]:
    dates, adj, turnover = [], [], []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"date", "adj_close", "turnover"}
        if not required.issubset(reader.fieldnames or []):
            raise RuntimeError(f"{path}: missing {required - set(reader.fieldnames or [])}")
        for row in reader:
            dates.append(row["date"][:10])
            adj.append(float(row["adj_close"]))
            turnover.append(float(row["turnover"]))
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: unsorted/duplicate dates")
    return dates, np.log(np.asarray(adj, dtype=np.float32)), np.asarray(turnover, dtype=np.float64)


def load_action_dates(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if "ex_date" not in (reader.fieldnames or []):
            return set()
        return {row["ex_date"][:10] for row in reader if row.get("ex_date")}


def fold_origins(dates: list[str]) -> list[np.ndarray]:
    start = max(CONTEXT, LOOKBACK) + HORIZON + 5
    end = len(dates) - HORIZON - 1
    if end <= start:
        raise RuntimeError("insufficient history")
    edges = np.linspace(start, end + 1, FOLDS + 1, dtype=int)
    out = []
    for f in range(FOLDS):
        a, b = int(edges[f]), int(edges[f + 1] - 1)
        out.append(np.unique(np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int)))
    return out


def bh_adjust(pvals: list[float]) -> list[float]:
    n = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(n, dtype=float)
    running = 1.0
    for rank in range(n, 0, -1):
        i = int(order[rank - 1])
        running = min(running, pvals[i] * n / rank)
        adj[i] = min(1.0, running)
    return adj.tolist()


def permutation_pvalue(x: np.ndarray, y: np.ndarray, seed: int = 7, n_perm: int = 2000) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    observed = abs(float(spearman_rank_ic(x, y)))
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_perm):
        yp = rng.permutation(y)
        hits += abs(float(spearman_rank_ic(x, yp))) >= observed
    return (hits + 1.0) / (n_perm + 1.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--actions-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="p6_regime_incremental_results")
    ap.add_argument("--symbols", default="RELIANCE,TCS,HDFCBANK,INFY,ICICIBANK,SBIN,ITC,BHARTIARTL,LT,AXISBANK,KOTAKBANK,HINDUNILVR,MARUTI,SUNPHARMA,BAJFINANCE,ASIANPAINT,TITAN,HCLTECH,WIPRO,ULTRACEMCO,NESTLEIND,M&M,NTPC,ONGC,POWERGRID,TATAMOTORS,TATASTEEL,ADANIENT,CIPLA,DRREDDY")
    args = ap.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    data_dir = Path(args.data_dir)
    actions_dir = Path(args.actions_dir)

    raw = {}
    action_dates = {}
    for s in symbols:
        dates, logp, turnover = load_prices(data_dir / f"{s}.csv")
        raw[s] = {"dates": dates, "logp": logp, "turnover": turnover}
        action_dates[s] = load_action_dates(actions_dir / f"{s}_actions.csv")

    common_dates = sorted(set(raw[symbols[0]]["dates"]).intersection(*[set(raw[s]["dates"]) for s in symbols[1:]]))
    if len(common_dates) < 400:
        raise RuntimeError("common history too short")

    idx = {s: {d: i for i, d in enumerate(raw[s]["dates"])} for s in symbols}
    date_pos = {d: i for i, d in enumerate(common_dates)}
    folds = fold_origins(common_dates)

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    rows = []
    for fold_no, origins in enumerate(folds, start=1):
        for oi in origins:
            date = common_dates[int(oi)]
            contexts, mom, future, turns = [], [], [], []
            for s in symbols:
                j = idx[s][date]
                contexts.append(raw[s]["logp"][j - CONTEXT:j].copy())
                mom.append(float(raw[s]["logp"][j] - raw[s]["logp"][j - LOOKBACK]))
                future.append(float(np.exp(raw[s]["logp"][j + HORIZON] - raw[s]["logp"][j]) - 1.0))
                start = max(0, j - LOOKBACK + 1)
                turns.append(float(np.mean(raw[s]["turnover"][start:j + 1])))

            outputs = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=True, univariate=True)
            tfm = np.array([float(np.asarray(o.forecast).reshape(-1)[-1] - contexts[k][-1]) for k, o in enumerate(outputs)])
            mom = np.asarray(mom)
            future = np.asarray(future)
            turns = np.asarray(turns)

            residual = residualize(tfm, mom)
            hybrid = zscore(mom) + 0.5 * zscore(residual)

            # Market-state features use only information at/before origin.
            daily_1d = np.zeros((len(symbols), LOOKBACK))
            for k, s in enumerate(symbols):
                j = idx[s][date]
                lp = raw[s]["logp"]
                hist = lp[j - LOOKBACK + 1:j + 1]
                daily_1d[k, 1:] = np.diff(hist)
            market_daily = np.mean(daily_1d, axis=0)
            market_20d_return = float(np.sum(mom) / len(mom))
            market_vol = float(np.std(market_daily))
            breadth = float(np.mean(mom > 0))
            dispersion = float(np.std(daily_1d[:, -1]))

            # Past-only volatility benchmark for high/low-vol classification.
            past_vols = []
            for past_pos in range(max(LOOKBACK, int(oi) - 252), int(oi)):
                d = common_dates[past_pos]
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

            # Post-corporate-action cooldown: only past ex-dates, never future events.
            event_clean = np.ones(len(symbols), dtype=bool)
            for k, s in enumerate(symbols):
                j = idx[s][date]
                prior_dates = set(raw[s]["dates"][max(0, j - 5):j + 1])
                if action_dates[s].intersection(prior_dates):
                    event_clean[k] = False

            # Point-in-time liquidity: top 20 by trailing turnover.
            top_liq_idx = np.argsort(turns)[::-1][:20]
            eligible = np.zeros(len(symbols), dtype=bool)
            eligible[top_liq_idx] = True
            eligible &= event_clean

            risk_on = (market_20d_return >= 0.0) and (breadth >= 0.50) and (not high_vol)
            stress = (market_20d_return < 0.0) and (breadth < 0.50) and high_vol
            regime = "risk_on" if risk_on else "stress" if stress else "neutral"

            rows.append({
                "fold": fold_no,
                "date": date,
                "future_return": future,
                "momentum": mom,
                "timesfm": tfm,
                "residual": residual,
                "hybrid": hybrid,
                "eligible": eligible,
                "risk_on": risk_on,
                "stress": stress,
                "high_vol": high_vol,
                "breadth_high": breadth >= 0.50,
                "trend_up": market_20d_return >= 0,
                "market_20d_return": market_20d_return,
                "market_vol": market_vol,
                "breadth": breadth,
                "dispersion": dispersion,
                "regime": regime,
            })

    regime_names = ("all", "risk_on", "stress", "high_vol", "low_vol", "breadth_high", "breadth_low", "trend_up", "trend_down")
    metrics = []
    pvals = []

    for name in regime_names:
        subset = rows if name == "all" else [
            r for r in rows
            if (name == "risk_on" and r["risk_on"])
            or (name == "stress" and r["stress"])
            or (name == "high_vol" and r["high_vol"])
            or (name == "low_vol" and not r["high_vol"])
            or (name == "breadth_high" and r["breadth_high"])
            or (name == "breadth_low" and not r["breadth_high"])
            or (name == "trend_up" and r["trend_up"])
            or (name == "trend_down" and not r["trend_up"])
        ]
        x_resid, y = [], []
        momentum_excess, resid_excess = [], []
        for r in subset:
            eligible = r["eligible"]
            if int(np.sum(eligible)) < TOP_K:
                continue
            idxs = np.flatnonzero(eligible)
            rr = r["residual"][idxs]
            mm = r["momentum"][idxs]
            yy = r["future_return"][idxs]
            x_resid.extend(rr.tolist())
            y.extend(yy.tolist())

            top_m = idxs[np.argsort(mm)[-TOP_K:]]
            top_r = idxs[np.argsort(rr)[-TOP_K:]]
            momentum_excess.append(float(np.mean(r["future_return"][top_m]) - np.mean(r["future_return"][top_m * 0 + idxs])))
            resid_excess.append(float(np.mean(r["future_return"][top_r]) - np.mean(r["future_return"][top_m])))

        if len(x_resid) >= 20:
            rank_ic = float(spearman_rank_ic(np.asarray(x_resid), np.asarray(y)))
            p = permutation_pvalue(np.asarray(x_resid), np.asarray(y), seed=19 + len(metrics))
            pvals.append(p)
        else:
            rank_ic, p = float("nan"), float("nan")

        metrics.append({
            "regime": name,
            "rebalances": len(subset),
            "eligible_name_rebalances": len(momentum_excess),
            "residual_rank_ic": rank_ic,
            "residual_rank_ic_p": p,
            "mean_top6_residual_minus_momentum": float(np.mean(resid_excess)) if resid_excess else float("nan"),
        })

    valid_pvals = [p for p in pvals if np.isfinite(p)]
    adj = bh_adjust(valid_pvals)
    k = 0
    for m in metrics:
        if np.isfinite(m["residual_rank_ic_p"]):
            m["residual_rank_ic_fdr_q"] = adj[k]
            k += 1
        else:
            m["residual_rank_ic_fdr_q"] = float("nan")

    def top6_return(r: dict, score_key: str) -> float:
        eligible = r["eligible"]
        if int(np.sum(eligible)) < TOP_K:
            return float("nan")
        idxs = np.flatnonzero(eligible)
        score = np.asarray(r[score_key])[idxs]
        selected = idxs[np.argsort(score)[-TOP_K:]]
        return float(np.mean(r["future_return"][selected]))

    strategy_rows = []
    for cost in ONE_WAY_COSTS:
        equity = {k: 1_000_000.0 for k in ("momentum", "residual_overlay_risk_on", "residual_overlay_stress", "hybrid")}
        prev = {k: np.zeros(len(symbols)) for k in equity}
        for r in rows:
            if int(np.sum(r["eligible"])) < TOP_K:
                continue
            eligible = r["eligible"]
            idxs = np.flatnonzero(eligible)
            n = len(idxs)
            mom_score = np.asarray(r["momentum"])
            resid_score = np.asarray(r["residual"])
            hybrid_score = np.asarray(r["hybrid"])

            new = {}
            for key, score in [
                ("momentum", mom_score),
                ("hybrid", hybrid_score),
            ]:
                w = np.zeros(len(symbols))
                sel = idxs[np.argsort(score[idxs])[-TOP_K:]]
                w[sel] = 1.0 / TOP_K
                new[key] = w

            for key, condition in [
                ("residual_overlay_risk_on", bool(r["risk_on"])),
                ("residual_overlay_stress", bool(r["stress"])),
            ]:
                base = new["momentum"]
                if condition:
                    w = np.zeros(len(symbols))
                    sel = idxs[np.argsort(resid_score[idxs])[-TOP_K:]]
                    w[sel] = 1.0 / TOP_K
                    new[key] = w
                else:
                    new[key] = base.copy()

            for key, w in new.items():
                turnover = float(np.sum(np.abs(w - prev[key])))
                gross = float(np.dot(w, r["future_return"]))
                net = gross - turnover * cost
                equity[key] *= max(0.0, 1.0 + net)
                prev[key] = w

        for key, value in equity.items():
            strategy_rows.append({
                "strategy": key,
                "one_way_cost": cost,
                "net_total_return": value / 1_000_000.0 - 1.0,
            })

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    serial_rows = []
    for r in rows:
        serial_rows.append({
            "fold": r["fold"], "date": r["date"], "risk_on": r["risk_on"], "stress": r["stress"],
            "high_vol": r["high_vol"], "breadth_high": r["breadth_high"], "trend_up": r["trend_up"],
            "market_20d_return": r["market_20d_return"], "market_vol": r["market_vol"],
            "breadth": r["breadth"], "dispersion": r["dispersion"], "regime": r["regime"],
            "eligible_count": int(np.sum(r["eligible"])),
        })
    with (out / "origin_regimes.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=serial_rows[0].keys())
        w.writeheader(); w.writerows(serial_rows)

    (out / "regime_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (out / "strategy_cost_results.json").write_text(json.dumps(strategy_rows, indent=2) + "\n", encoding="utf-8")
    summary = {
        "lane": "P6.1_exploratory_regime_conditional_incremental_timesfm",
        "stocks": len(symbols),
        "folds": FOLDS,
        "rebalances": len(rows),
        "top_k": TOP_K,
        "event_rule": "exclude names with an ex-date in the preceding 5 trading sessions",
        "liquidity_rule": "top 20 of 30 by trailing 20-session turnover at origin",
        "regime_rules": {
            "risk_on": "market 20d return >= 0, breadth >= 50%, low-vol vs trailing past median",
            "stress": "market 20d return < 0, breadth < 50%, high-vol vs trailing past median",
            "trend": "sign of equal-weight 30-stock 20d return",
            "volatility": "equal-weight cross-sectional daily-return volatility vs past-only median",
        },
        "fdr": "Benjamini-Hochberg across predeclared regime rank-IC tests",
        "note": "Exploratory; stock bootstrap is not final PIT evidence and Phase 7 effective-date costs are still required for promotion.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "regime_metrics": metrics, "strategy_results": strategy_rows}, indent=2))


if __name__ == "__main__":
    main()
