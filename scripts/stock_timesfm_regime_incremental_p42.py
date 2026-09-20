from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

CONTEXT = 128
HORIZON = 5
LOOKBACK = 20
TOP_K = 6
FOLDS = (2, 3, 4)
ORIGINS_PER_FOLD = 8
CAPITAL = 1_000_000.0
BROKERAGE_PER_ORDER = 20.0
DP_SELL = 13.5
ONE_WAY_COST_SCENARIOS = (0.00125, 0.0025, 0.00375, 0.0050)

SYMBOLS = [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","SBIN","ITC","BHARTIARTL","LT",
    "AXISBANK","KOTAKBANK","HINDUNILVR","MARUTI","SUNPHARMA","BAJFINANCE","ASIANPAINT",
    "TITAN","HCLTECH","WIPRO","ULTRACEMCO","NESTLEIND","M&M","NTPC","ONGC","POWERGRID",
    "TATAMOTORS","TATASTEEL","ADANIENT","CIPLA","DRREDDY",
]


def load_series(path: Path) -> tuple[list[str], np.ndarray]:
    dates, values = [], []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            dates.append(row["date"][:10])
            values.append(float(row["adj_close"]))
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: unsorted/duplicate dates")
    return dates, np.log(np.asarray(values, dtype=np.float32))


def zscore(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    s = float(np.std(v))
    return (v - float(np.mean(v))) / s if s > 1e-12 else np.zeros_like(v)


def execute_period(old_w: np.ndarray, new_w: np.ndarray, future: np.ndarray, capital: float, rate: float) -> tuple[float, float, float]:
    gross = float(np.dot(new_w, future))
    delta = np.abs(new_w - old_w)
    traded = float(delta.sum() * capital)
    sell = int(((old_w > 1e-12) & (new_w < 1e-12)).sum())
    buy = int(((new_w > 1e-12) & (old_w < 1e-12)).sum())
    resize = int(((delta > 1e-12) & ~(((old_w > 1e-12) & (new_w < 1e-12)) | ((new_w > 1e-12) & (old_w < 1e-12)))).sum())
    fixed = (sell + buy + 2 * resize) * BROKERAGE_PER_ORDER + (sell + resize) * DP_SELL
    fee = traded * rate + fixed
    net = (gross * capital - fee) / capital
    return capital * (1.0 + net), gross, net


def select(score: np.ndarray, use: bool) -> np.ndarray:
    w = np.zeros(len(score), dtype=float)
    if use:
        idx = np.argsort(score)[-TOP_K:]
        w[idx] = 1.0 / TOP_K
    return w


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--output", default="p4_p42_nested_results")
    args = ap.parse_args()

    series = {s: load_series(Path(args.data_dir) / f"{s}.csv") for s in SYMBOLS}
    common = set(series[SYMBOLS[0]][0])
    for s in SYMBOLS[1:]:
        common &= set(series[s][0])
    dates = sorted(common)
    idx = {s: {d: i for i, d in enumerate(series[s][0])} for s in SYMBOLS}

    # Fixed chronological anchors: 32 total rebalances, 8 per fold, same dates as Phase 4.1.
    start = CONTEXT + LOOKBACK
    end = len(dates) - HORIZON - 1
    edges = np.linspace(start, end + 1, 5, dtype=int)
    fold_origins = {}
    for fold in (1, 2, 3, 4):
        a, b = int(edges[fold - 1]), int(edges[fold] - 1)
        fold_origins[fold] = np.unique(np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int))

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    origin_rows = []
    for fold in (1, 2, 3, 4):
        for origin in fold_origins[fold]:
            d = dates[int(origin)]
            contexts, momentum, future = [], [], []
            for s in SYMBOLS:
                i = idx[s][d]
                values = series[s][1]
                contexts.append(values[i - CONTEXT:i].copy())
                momentum.append(float(values[i] - values[i - LOOKBACK]))
                future.append(float(np.exp(values[i + HORIZON] - values[i]) - 1.0))
            out = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=False, univariate=True)
            tf = np.array([
                float(np.asarray(o.forecast).reshape(-1)[-1] - contexts[j][-1])
                for j, o in enumerate(out)
            ])
            mom = np.asarray(momentum)
            fut = np.asarray(future)
            origin_rows.append({
                "fold": fold,
                "date": d,
                "breadth": float(np.mean(mom > 0)),
                "momentum": zscore(mom),
                "timesfm": zscore(tf),
                "residual": zscore(tf) - zscore(mom),
                "future": fut,
            })

    outputs = []
    for rate in ONE_WAY_COST_SCENARIOS:
        for signal in ("momentum", "residual"):
            capital = CAPITAL
            old_w = np.zeros(len(SYMBOLS))
            period_rows = []
            for fold in FOLDS:
                prior = [r["breadth"] for r in origin_rows if r["fold"] < fold]
                threshold = float(np.median(prior))
                for r in [x for x in origin_rows if x["fold"] == fold]:
                    use = r["breadth"] < threshold
                    new_w = select(r[signal], use)
                    capital, gross, net = execute_period(old_w, new_w, r["future"], capital, rate)
                    period_rows.append({
                        "fold": fold,
                        "date": r["date"],
                        "signal": signal,
                        "one_way_cost_rate": rate,
                        "training_breadth_threshold": threshold,
                        "breadth": r["breadth"],
                        "used": use,
                        "gross_return": gross,
                        "net_return": net,
                    })
                    old_w = new_w
            used = [x for x in period_rows if x["used"]]
            outputs.append({
                "signal": signal,
                "one_way_cost_rate": rate,
                "test_rebalances": len(period_rows),
                "used_rebalances": len(used),
                "net_total_return": float(capital / CAPITAL - 1.0),
                "used_mean_net_return": float(np.mean([x["net_return"] for x in used])) if used else 0.0,
                "used_mean_gross_return": float(np.mean([x["gross_return"] for x in used])) if used else 0.0,
            })

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "strategy_results.json").write_text(json.dumps(outputs, indent=2) + "\n", encoding="utf-8")
    flat_rows = []
    for rate in ONE_WAY_COST_SCENARIOS:
        for signal in ("momentum", "residual"):
            capital = CAPITAL
            old_w = np.zeros(len(SYMBOLS))
            for fold in FOLDS:
                threshold = float(np.median([r["breadth"] for r in origin_rows if r["fold"] < fold]))
                for r in [x for x in origin_rows if x["fold"] == fold]:
                    use = r["breadth"] < threshold
                    new_w = select(r[signal], use)
                    capital, gross, net = execute_period(old_w, new_w, r["future"], capital, rate)
                    flat_rows.append({
                        "fold": fold, "date": r["date"], "signal": signal,
                        "one_way_cost_rate": rate, "threshold": threshold,
                        "breadth": r["breadth"], "used": use,
                        "gross_return": gross, "net_return": net,
                    })
                    old_w = new_w
    with (out / "period_results.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=flat_rows[0].keys())
        writer.writeheader()
        writer.writerows(flat_rows)

    meta = {
        "lane": "P4.2_nested_regime_conditioned_timesfm_incremental_test",
        "rule": "20-session breadth determines a low-breadth regime using only prior folds; rank residual = z(TimesFM 5-session forecast) - z(20-session momentum); select top six only in low-breadth regime",
        "test_folds": list(FOLDS),
        "rebalances_per_fold": ORIGINS_PER_FOLD,
        "stocks": len(SYMBOLS),
        "cost_scenarios": list(ONE_WAY_COST_SCENARIOS),
        "note": "No parameter selection on test folds. Research-only; not a promotion result.",
    }
    (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"metadata": meta, "results": outputs}, indent=2))


if __name__ == "__main__":
    main()
