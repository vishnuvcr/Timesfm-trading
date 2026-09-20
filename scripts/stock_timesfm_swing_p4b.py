from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

CONTEXT = 128
LOOKBACK = 20
HORIZONS = (2, 5, 10, 20)
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

def zscore(x: np.ndarray) -> np.ndarray:
    s = float(np.std(x))
    return (x - float(np.mean(x))) / s if s > 1e-12 else np.zeros_like(x)

def top_k(scores: np.ndarray) -> np.ndarray:
    picks = np.argsort(scores)[::-1][: min(TOP_K, len(scores))]
    w = np.zeros(len(scores), dtype=float)
    if len(picks):
        w[picks] = 1.0 / len(picks)
    return w

def trade_cost(old_w: np.ndarray, new_w: np.ndarray, capital: float, rate: float) -> float:
    delta = np.abs(new_w - old_w)
    traded = float(delta.sum() * capital)
    sell = int(np.sum((old_w > 1e-12) & (new_w < 1e-12)))
    buy = int(np.sum((new_w > 1e-12) & (old_w < 1e-12)))
    resized = int(np.sum((delta > 1e-12) & (old_w > 1e-12) & (new_w > 1e-12)))
    return traded * rate + (sell + buy + 2 * resized) * BROKERAGE_PER_ORDER + sell * DP_SELL

def make_folds(dates: list[str], horizon: int) -> list[np.ndarray]:
    start = CONTEXT + LOOKBACK
    end = len(dates) - horizon - 1
    edges = np.linspace(start, end + 1, FOLDS + 1, dtype=int)
    folds = []
    for f in range(FOLDS):
        a, b = int(edges[f]), int(edges[f + 1] - 1)
        if b < a:
            raise RuntimeError("empty chronological fold")
        cand = np.arange(a, b + 1, horizon, dtype=int)
        if len(cand) < ORIGINS_PER_FOLD:
            cand = np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int)
        folds.append(np.unique(cand[:ORIGINS_PER_FOLD]))
    return folds

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--output", default="p4b_swing_results")
    args = ap.parse_args()

    series = {}
    for symbol in SYMBOLS:
        series[symbol] = load_series(Path(args.data_dir) / f"{symbol}.csv")
    common_dates = sorted(set.intersection(*(set(v[0]) for v in series.values())))
    index = {s: {d: i for i, d in enumerate(series[s][0])} for s in SYMBOLS}
    if len(common_dates) < CONTEXT + LOOKBACK + max(HORIZONS) + FOLDS * ORIGINS_PER_FOLD:
        raise RuntimeError("insufficient common history")

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    signal_rows, experiment_rows = [], []

    for horizon in HORIZONS:
        fold_rows = []
        for fold_no, origins in enumerate(make_folds(common_dates, horizon), start=1):
            for origin in origins:
                date = common_dates[int(origin)]
                contexts, momentum, future = [], [], []
                for symbol in SYMBOLS:
                    i = index[symbol][date]
                    contexts.append(series[symbol][1][i-CONTEXT:i])
                    momentum.append(float(series[symbol][1][i] - series[symbol][1][i-LOOKBACK]))
                    future.append(float(series[symbol][1][i+horizon] - series[symbol][1][i]))
                forecasts = model.predict_batch(contexts, horizon=horizon, return_quantiles=True, univariate=True)
                tfm = np.array([float(np.asarray(out.forecast).reshape(-1)[-1] - contexts[j][-1]) for j, out in enumerate(forecasts)])
                widths = []
                for out in forecasts:
                    if out.quantiles is None:
                        widths.append(np.nan)
                        continue
                    q = np.asarray(out.quantiles)
                    if q.ndim == 2 and q.shape == (horizon, 9):
                        widths.append(float(q[-1, -1] - q[-1, 0]))
                    elif q.ndim == 3 and q.shape[-2:] == (horizon, 9):
                        widths.append(float(q[0, -1, -1] - q[0, -1, 0]))
                    else:
                        raise RuntimeError(f"unexpected TimesFM quantile shape {q.shape}; expected ({horizon}, 9) or (N, {horizon}, 9)")
                widths = np.asarray(widths, dtype=float)
                mom = np.asarray(momentum, dtype=float)
                fut = np.asarray(future, dtype=float)
                width_filled = np.nan_to_num(widths, nan=float(np.nanmedian(widths)))
                width_z = zscore(width_filled)
                scale = 1.0 / np.clip(1.0 + width_z, 0.25, 2.5)
                scaled = zscore(mom) * scale
                fold_rows.append({
                    "fold": fold_no, "date": date, "future": fut,
                    "momentum": mom, "timesfm": tfm, "scaled": scaled, "width": widths,
                })
                for symbol, m, t, sm, w, fwd in zip(SYMBOLS, mom, tfm, scaled, widths, fut):
                    signal_rows.append({
                        "horizon": horizon, "fold": fold_no, "date": date, "symbol": symbol,
                        "momentum": float(m), "timesfm_forecast_return": float(t),
                        "uncertainty_scaled_momentum": float(sm),
                        "q10_q90_width": float(w), "future_log_return": float(fwd),
                    })

        for strategy_name in ("momentum", "timesfm", "scaled"):
            for rate in COSTS:
                capital = CAPITAL
                old = np.zeros(len(SYMBOLS))
                nets, gross, turns = [], [], []
                for row in fold_rows:
                    new = top_k(row[strategy_name])
                    g = float(np.dot(new, row["future"]))
                    fee = trade_cost(old, new, capital, rate)
                    n = (g * capital - fee) / capital
                    capital *= max(0.0, 1.0 + n)
                    nets.append(n)
                    gross.append(g)
                    turns.append(float(np.abs(new - old).sum()))
                    old = new
                arr = np.asarray(nets)
                experiment_rows.append({
                    "horizon": horizon,
                    "strategy": strategy_name,
                    "one_way_cost_rate": rate,
                    "net_total_return": float(capital / CAPITAL - 1.0),
                    "gross_mean_return": float(np.mean(gross)),
                    "net_mean_return": float(np.mean(arr)),
                    "hit_rate": float(np.mean(arr > 0)),
                    "mean_turnover_fraction": float(np.mean(turns)),
                    "rebalance_count": int(len(arr)),
                })

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if signal_rows:
        with (out / "signal_rows.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=signal_rows[0].keys())
            w.writeheader()
            w.writerows(signal_rows)
    (out / "results.json").write_text(json.dumps(experiment_rows, indent=2) + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({
        "lane": "phase_4b_swing_bootstrap",
        "model": "timesfm-3.0-pytorch",
        "context": CONTEXT,
        "horizons": HORIZONS,
        "folds": FOLDS,
        "origins_per_fold": ORIGINS_PER_FOLD,
        "costs": COSTS,
        "top_k": TOP_K,
        "bootstrap_only": True,
        "note": "Engineering/exploratory stock panel; not final PIT evidence and not Phase 7 economic validation."
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(experiment_rows, indent=2))

if __name__ == "__main__":
    main()
