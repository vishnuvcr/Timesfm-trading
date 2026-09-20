from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

CONTEXT = 128
LOOKBACK = 20
HORIZON = 10
FOLDS = 4
ORIGINS_PER_FOLD = 8
TOP_K = 6
CAPITAL = 1_000_000.0
BROKERAGE_PER_ORDER = 20.0
DP_SELL = 13.5
COSTS = (0.00125, 0.0025, 0.00375, 0.0050)
SYMBOLS = (
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "SBIN", "ITC",
    "BHARTIARTL", "LT", "AXISBANK", "KOTAKBANK", "HINDUNILVR", "MARUTI",
    "SUNPHARMA", "BAJFINANCE", "ASIANPAINT", "TITAN", "HCLTECH", "WIPRO",
    "ULTRACEMCO", "NESTLEIND", "M&M", "NTPC", "ONGC", "POWERGRID",
    "TATAMOTORS", "TATASTEEL", "ADANIENT", "CIPLA", "DRREDDY",
)

def load_series(path: Path) -> tuple[list[str], np.ndarray]:
    dates, values = [], []
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            dates.append(row["date"][:10])
            values.append(float(row["adj_close"]))
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: dates are not sorted/unique")
    return dates, np.log(np.asarray(values, dtype=np.float32))

def load_pit(path: Path) -> dict[str, list[tuple[date, date]]]:
    spans: dict[str, list[tuple[date, date]]] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("exchange") != "NSE":
                continue
            symbol = row["symbol"].upper()
            if symbol not in SYMBOLS:
                continue
            a = date.fromisoformat(row["rebalance_date"][:10])
            b = date.fromisoformat(row["valid_to"][:10])
            spans.setdefault(symbol, []).append((a, b))
    for symbol in spans:
        spans[symbol].sort()
    if not spans:
        raise RuntimeError("PIT universe contains no matching bootstrap symbols")
    return spans

def eligible_symbols(spans: dict[str, list[tuple[date, date]]], day: str) -> list[str]:
    d = date.fromisoformat(day[:10])
    out = []
    for symbol in SYMBOLS:
        for a, b in spans.get(symbol, []):
            if a <= d <= b:
                out.append(symbol)
                break
    return out

def top_k(scores: np.ndarray, k: int = TOP_K) -> np.ndarray:
    if len(scores) == 0:
        return np.zeros(0, dtype=float)
    picks = np.argsort(scores)[::-1][: min(k, len(scores))]
    w = np.zeros(len(scores), dtype=float)
    if len(picks):
        w[picks] = 1.0 / len(picks)
    return w

def zscore(x: np.ndarray) -> np.ndarray:
    s = float(np.std(x))
    return (x - float(np.mean(x))) / s if s > 1e-12 else np.zeros_like(x)

def trade_cost(old_w: np.ndarray, new_w: np.ndarray, capital: float, rate: float) -> float:
    n = max(len(old_w), len(new_w))
    old = np.pad(old_w, (0, n-len(old_w)))
    new = np.pad(new_w, (0, n-len(new_w)))
    delta = np.abs(new - old)
    traded = float(delta.sum() * capital)
    sell = int(np.sum((old > 1e-12) & (new < 1e-12)))
    buy = int(np.sum((new > 1e-12) & (old < 1e-12)))
    resized = int(np.sum((delta > 1e-12) & (old > 1e-12) & (new > 1e-12)))
    return traded * rate + (sell + buy + 2 * resized) * BROKERAGE_PER_ORDER + sell * DP_SELL

def make_origins(common_dates: list[str]) -> list[np.ndarray]:
    start = CONTEXT + LOOKBACK
    end = len(common_dates) - HORIZON - 1
    edges = np.linspace(start, end + 1, FOLDS + 1, dtype=int)
    folds = []
    for f in range(FOLDS):
        a, b = int(edges[f]), int(edges[f + 1] - 1)
        cand = np.arange(a, b + 1, HORIZON, dtype=int)
        if len(cand) < ORIGINS_PER_FOLD:
            cand = np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int)
        folds.append(np.unique(cand[:ORIGINS_PER_FOLD]))
    return folds

def exact_signflip_pvalue(diffs: np.ndarray) -> float:
    diffs = np.asarray(diffs, dtype=float)
    if len(diffs) != FOLDS:
        return float("nan")
    obs = float(np.mean(diffs))
    values = []
    for mask in range(1 << FOLDS):
        signs = np.array([1.0 if (mask >> i) & 1 else -1.0 for i in range(FOLDS)])
        values.append(float(np.mean(diffs * signs)))
    return float(np.mean(np.asarray(values) >= obs - 1e-15))

def compound_fold_return(rows: list[dict], score_key: str, rate: float) -> float:
    capital = CAPITAL
    if not rows:
        return 0.0
    old = np.zeros(len(rows[0]["symbols"]))
    for row in rows:
        score = np.asarray(row[score_key], dtype=float)
        future = np.asarray(row["future"], dtype=float)
        new = top_k(score)
        gross = float(np.dot(new, future))
        fee = trade_cost(old, new, capital, rate)
        net = (gross * capital - fee) / capital
        capital *= max(0.0, 1.0 + net)
        old = new
    return float(capital / CAPITAL - 1.0)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--pit-universe", default="data/cache/equities/tejhq_nse_pit_universe.csv")
    ap.add_argument("--output", default="p4b_pit_10d_results")
    args = ap.parse_args()

    series = {s: load_series(Path(args.data_dir) / f"{s}.csv") for s in SYMBOLS}
    spans = load_pit(Path(args.pit_universe))
    common = sorted(set.intersection(*(set(v[0]) for v in series.values())))
    if len(common) < CONTEXT + LOOKBACK + HORIZON + FOLDS * ORIGINS_PER_FOLD:
        raise RuntimeError("insufficient common history")
    index = {s: {d: i for i, d in enumerate(series[s][0])} for s in SYMBOLS}

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    folds_rows: dict[int, list[dict]] = {f: [] for f in range(1, FOLDS + 1)}
    signal_rows = []
    eligible_counts = []

    for fold_no, origins in enumerate(make_origins(common), start=1):
        for origin in origins:
            day = common[int(origin)]
            elig = eligible_symbols(spans, day)
            if len(elig) < TOP_K:
                raise RuntimeError(f"{day}: only {len(elig)} PIT-eligible stocks; need at least {TOP_K}")
            contexts, momentum, future = [], [], []
            for symbol in elig:
                i = index[symbol][day]
                contexts.append(series[symbol][1][i-CONTEXT:i])
                momentum.append(float(series[symbol][1][i] - series[symbol][1][i-LOOKBACK]))
                future.append(float(series[symbol][1][i+HORIZON] - series[symbol][1][i]))
            forecasts = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=True, univariate=True)
            tfm = np.array([
                float(np.asarray(o.forecast).reshape(-1)[-1] - contexts[j][-1])
                for j, o in enumerate(forecasts)
            ])
            widths = []
            for o in forecasts:
                q = None if o.quantiles is None else np.asarray(o.quantiles)
                if q is None:
                    widths.append(np.nan)
                elif q.ndim == 2 and q.shape == (HORIZON, 9):
                    widths.append(float(q[-1, -1] - q[-1, 0]))
                elif q.ndim == 3 and q.shape[-2:] == (HORIZON, 9):
                    widths.append(float(q[0, -1, -1] - q[0, -1, 0]))
                else:
                    raise RuntimeError(f"unexpected quantile shape {q.shape}")
            widths = np.asarray(widths, dtype=float)
            mom = np.asarray(momentum, dtype=float)
            fut = np.asarray(future, dtype=float)
            width_filled = np.nan_to_num(widths, nan=float(np.nanmedian(widths)))
            scaled = zscore(mom) / np.clip(1.0 + zscore(width_filled), 0.25, 2.5)
            row = {
                "symbols": elig,
                "future": fut,
                "momentum": mom,
                "timesfm": tfm,
                "scaled": scaled,
            }
            folds_rows[fold_no].append(row)
            eligible_counts.append(len(elig))
            for symbol, m, t, sm, w, fwd in zip(elig, mom, tfm, scaled, widths, fut):
                signal_rows.append({
                    "fold": fold_no,
                    "date": day,
                    "symbol": symbol,
                    "momentum": float(m),
                    "timesfm_forecast_return": float(t),
                    "uncertainty_scaled_momentum": float(sm),
                    "q10_q90_width": float(w),
                    "future_log_return": float(fwd),
                })

    summary = []
    for rate in COSTS:
        fold_metrics = []
        for fold_no in range(1, FOLDS + 1):
            rows = folds_rows[fold_no]
            for strat in ("momentum", "timesfm", "scaled"):
                fold_metrics.append({
                    "fold": fold_no,
                    "strategy": strat,
                    "cost": rate,
                    "compound_return": compound_fold_return(rows, strat, rate),
                })
        for strat in ("momentum", "timesfm", "scaled"):
            vals = [r["compound_return"] for r in fold_metrics if r["strategy"] == strat]
            summary.append({
                "strategy": strat,
                "one_way_cost_rate": rate,
                "mean_fold_compound_return": float(np.mean(vals)),
                "compound_all_folds": float(np.prod(1 + np.asarray(vals)) - 1.0),
            })
        mom = np.array([r["compound_return"] for r in fold_metrics if r["strategy"] == "momentum"])
        tf = np.array([r["compound_return"] for r in fold_metrics if r["strategy"] == "timesfm"])
        sc = np.array([r["compound_return"] for r in fold_metrics if r["strategy"] == "scaled"])
        summary.append({
            "strategy": "timesfm_minus_momentum_block_test",
            "one_way_cost_rate": rate,
            "fold_differences": (tf - mom).tolist(),
            "mean_difference": float(np.mean(tf - mom)),
            "positive_folds": int(np.sum(tf > mom)),
            "exact_four_fold_signflip_p_one_sided": exact_signflip_pvalue(tf - mom),
        })
        summary.append({
            "strategy": "scaled_minus_momentum_block_test",
            "one_way_cost_rate": rate,
            "fold_differences": (sc - mom).tolist(),
            "mean_difference": float(np.mean(sc - mom)),
            "positive_folds": int(np.sum(sc > mom)),
            "exact_four_fold_signflip_p_one_sided": exact_signflip_pvalue(sc - mom),
        })

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "signal_rows.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=signal_rows[0].keys())
        writer.writeheader()
        writer.writerows(signal_rows)
    (out / "summary.json").write_text(json.dumps({
        "lane": "phase_4b_pit_10d_validation",
        "model": "timesfm-3.0-pytorch",
        "horizon": HORIZON,
        "context": CONTEXT,
        "folds": FOLDS,
        "origins_per_fold": ORIGINS_PER_FOLD,
        "rebalance_count": FOLDS * ORIGINS_PER_FOLD,
        "mean_pit_eligible_stocks": float(np.mean(eligible_counts)),
        "min_pit_eligible_stocks": int(np.min(eligible_counts)),
        "max_pit_eligible_stocks": int(np.max(eligible_counts)),
        "results": summary,
        "note": "Bootstrap PIT-universe validation. It removes current-name selection from the 30-stock panel but is not final universe-scale evidence.",
    }, indent=2) + "\n", encoding="utf-8")
    (out / "fold_results.json").write_text(json.dumps(fold_metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
