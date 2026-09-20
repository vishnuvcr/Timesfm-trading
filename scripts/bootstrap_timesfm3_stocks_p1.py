from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter
from src.stats.forecast_metrics import mae, rmse, spearman_rank_ic

CONTEXT = 128  # stock bootstrap execution marker v1
HORIZON = 5
ORIGINS = 40
DEFAULT_SYMBOLS = [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","SBIN","ITC","BHARTIARTL","LT",
    "AXISBANK","KOTAKBANK","HINDUNILVR","MARUTI","SUNPHARMA","BAJFINANCE","ASIANPAINT",
    "TITAN","HCLTECH","WIPRO","ULTRACEMCO","NESTLEIND","M&M","NTPC","ONGC","POWERGRID",
    "TATAMOTORS","TATASTEEL","ADANIENT","CIPLA","DRREDDY",
]


def load_adjusted(path: Path) -> tuple[list[str], np.ndarray]:
    dates = []
    values = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"date", "adj_close"}
        if not required.issubset(reader.fieldnames or []):
            raise RuntimeError(f"{path}: missing {required - set(reader.fieldnames or [])}")
        for row in reader:
            try:
                dates.append(row["date"][:10])
                v = float(row["adj_close"])
            except (TypeError, ValueError) as exc:
                raise RuntimeError(f"{path}: bad adjusted row {row}") from exc
            if v <= 0:
                raise RuntimeError(f"{path}: non-positive adjusted close")
            values.append(v)
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: dates not sorted/unique")
    return dates, np.log(np.asarray(values, dtype=np.float32))


def evaluate_stock(model: TimesFM3Adapter, symbol: str, path: Path) -> dict:
    dates, values = load_adjusted(path)
    if len(values) < CONTEXT + HORIZON + ORIGINS:
        raise RuntimeError(f"{symbol}: insufficient rows {len(values)}")

    start = len(values) - ORIGINS - HORIZON
    origin_idx = np.linspace(start, len(values) - HORIZON - 1, ORIGINS, dtype=int)
    contexts = [values[i - CONTEXT:i].copy() for i in origin_idx]
    outputs = model.predict_batch(
        contexts,
        horizon=HORIZON,
        return_quantiles=True,
        univariate=True,
    )

    actuals, forecasts, persistence = [], [], []
    forecast_returns, actual_returns, persistence_returns = [], [], []
    interval_widths, abs_moves = [], []

    for idx, out in zip(origin_idx, outputs):
        pred = np.asarray(out.forecast).reshape(-1)
        if pred.size != HORIZON:
            raise RuntimeError(f"{symbol}: unexpected forecast shape {out.forecast.shape}")
        actual = values[idx:idx + HORIZON]
        last = values[idx - 1]

        actuals.extend(actual.tolist())
        forecasts.extend(pred.tolist())
        persistence.extend([last] * HORIZON)
        forecast_returns.append(float(pred[-1] - last))
        actual_returns.append(float(actual[-1] - last))
        persistence_returns.append(0.0)

        if out.quantiles is not None:
            q = np.asarray(out.quantiles)
            if q.ndim == 2 and q.shape == (HORIZON, 9):
                interval_widths.append(float(q[-1, -1] - q[-1, 0]))
            elif q.ndim == 3 and q.shape[-2:] == (HORIZON, 9):
                interval_widths.append(float(q[0, -1, -1] - q[0, -1, 0]))
            else:
                raise RuntimeError(f"{symbol}: unexpected quantile shape {out.quantiles.shape}")
            abs_moves.append(abs(float(actual[-1] - last)))

    if not interval_widths:
        interval_rho = float("nan")
    else:
        interval_rho = spearman_rank_ic(np.asarray(abs_moves), np.asarray(interval_widths))

    return {
        "symbol": symbol,
        "rows": int(len(values)),
        "date_start": dates[0],
        "date_end": dates[-1],
        "origins": int(len(origin_idx)),
        "context": CONTEXT,
        "horizon": HORIZON,
        "log_mae_timesfm": mae(actuals, forecasts),
        "log_mae_persistence": mae(actuals, persistence),
        "log_rmse_timesfm": rmse(actuals, forecasts),
        "log_rmse_persistence": rmse(actuals, persistence),
        "five_day_return_mae_timesfm": mae(actual_returns, forecast_returns),
        "five_day_return_mae_persistence": mae(actual_returns, persistence_returns),
        "directional_accuracy_timesfm": float(np.mean((np.asarray(actual_returns) > 0) == (np.asarray(forecast_returns) > 0))),
        "directional_base_rate": float(np.mean(np.asarray(actual_returns) > 0)),
        "q10_q90_width_h5_spearman_vs_abs_move": float(interval_rho),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    ap.add_argument("--output", default="p3_stock_results")
    args = ap.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    data_dir = Path(args.data_dir)
    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    rows = []
    for symbol in symbols:
        rows.append(evaluate_stock(model, symbol, data_dir / f"{symbol}.csv"))

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "per_stock.json").write_text(json.dumps(rows, indent=2) + "\\n", encoding="utf-8")

    summary = {
        "lane": "P1_exploratory_individual_stock_bootstrap",
        "model": "timesfm-3.0-pytorch",
        "universe": "30-name bootstrap from Phase 2 TejHQ adjusted-price cache",
        "stocks": len(rows),
        "horizon": HORIZON,
        "context": CONTEXT,
        "origins_per_stock": ORIGINS,
        "aggregate_mean_log_mae_timesfm": float(np.mean([r["log_mae_timesfm"] for r in rows])),
        "aggregate_mean_log_mae_persistence": float(np.mean([r["log_mae_persistence"] for r in rows])),
        "aggregate_mean_log_rmse_timesfm": float(np.mean([r["log_rmse_timesfm"] for r in rows])),
        "aggregate_mean_log_rmse_persistence": float(np.mean([r["log_rmse_persistence"] for r in rows])),
        "stocks_better_mae_than_persistence": int(sum(r["log_mae_timesfm"] < r["log_mae_persistence"] for r in rows)),
        "stocks_better_rmse_than_persistence": int(sum(r["log_rmse_timesfm"] < r["log_rmse_persistence"] for r in rows)),
        "aggregate_mean_directional_accuracy": float(np.mean([r["directional_accuracy_timesfm"] for r in rows])),
        "aggregate_mean_directional_base_rate": float(np.mean([r["directional_base_rate"] for r in rows])),
        "aggregate_mean_interval_return_abs_move_spearman": float(np.nanmean([r["q10_q90_width_h5_spearman_vs_abs_move"] for r in rows])),
        "note": "Exploratory stock-level forecast gate only. Bootstrap fixed universe; no strategy promotion, economic claim or final PIT inference.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
