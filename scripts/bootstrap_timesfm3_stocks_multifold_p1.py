from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter
from src.stats.forecast_metrics import mae, rmse, spearman_rank_ic

CONTEXT = 128
HORIZON = 5
FOLDS = 4
ORIGINS_PER_FOLD = 40

DEFAULT_SYMBOLS = [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","SBIN","ITC","BHARTIARTL","LT",
    "AXISBANK","KOTAKBANK","HINDUNILVR","MARUTI","SUNPHARMA","BAJFINANCE","ASIANPAINT",
    "TITAN","HCLTECH","WIPRO","ULTRACEMCO","NESTLEIND","M&M","NTPC","ONGC","POWERGRID",
    "TATAMOTORS","TATASTEEL","ADANIENT","CIPLA","DRREDDY",
]


def load_adjusted(path: Path) -> tuple[list[str], np.ndarray]:
    dates: list[str] = []
    values: list[float] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"date", "adj_close"}
        if not required.issubset(reader.fieldnames or []):
            raise RuntimeError(f"{path}: missing {required - set(reader.fieldnames or [])}")
        for row in reader:
            try:
                dates.append(row["date"][:10])
                values.append(float(row["adj_close"]))
            except (TypeError, ValueError) as exc:
                raise RuntimeError(f"{path}: bad adjusted row {row}") from exc
            if values[-1] <= 0:
                raise RuntimeError(f"{path}: non-positive adjusted close")
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: dates not sorted/unique")
    return dates, np.log(np.asarray(values, dtype=np.float32))


def fold_origins(n: int) -> list[np.ndarray]:
    low = CONTEXT + HORIZON
    high = n - HORIZON - 1
    if high <= low:
        raise RuntimeError(f"insufficient history for fold construction: n={n}")
    edges = np.linspace(low, high + 1, FOLDS + 1, dtype=int)
    folds: list[np.ndarray] = []
    for k in range(FOLDS):
        a, b = int(edges[k]), int(edges[k + 1] - 1)
        if b < a or (b - a + 1) < ORIGINS_PER_FOLD:
            raise RuntimeError(f"fold {k+1} too short for {ORIGINS_PER_FOLD} origins: {a}:{b}")
        folds.append(np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int))
    return folds


def evaluate_fold(model: TimesFM3Adapter, values: np.ndarray, origins: np.ndarray) -> dict:
    contexts = [values[i - CONTEXT:i].copy() for i in origins]
    outputs = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=True, univariate=True)

    actuals: list[float] = []
    forecasts: list[float] = []
    persistence: list[float] = []
    actual_returns: list[float] = []
    forecast_returns: list[float] = []
    interval_widths: list[float] = []
    abs_moves: list[float] = []

    for idx, out in zip(origins, outputs):
        pred = np.asarray(out.forecast).reshape(-1)
        if pred.size != HORIZON:
            raise RuntimeError(f"unexpected forecast shape {out.forecast.shape}")
        actual = values[idx:idx + HORIZON]
        last = values[idx - 1]
        actuals.extend(actual.tolist())
        forecasts.extend(pred.tolist())
        persistence.extend([last] * HORIZON)
        actual_returns.append(float(actual[-1] - last))
        forecast_returns.append(float(pred[-1] - last))

        if out.quantiles is not None:
            q = np.asarray(out.quantiles)
            if q.ndim == 2 and q.shape == (HORIZON, 9):
                interval_widths.append(float(q[-1, -1] - q[-1, 0]))
            elif q.ndim == 3 and q.shape[-2:] == (HORIZON, 9):
                interval_widths.append(float(q[0, -1, -1] - q[0, -1, 0]))
            else:
                raise RuntimeError(f"unexpected quantile shape {out.quantiles.shape}")
            abs_moves.append(abs(float(actual[-1] - last)))

    return {
        "origins": int(len(origins)),
        "log_mae_timesfm": mae(actuals, forecasts),
        "log_mae_persistence": mae(actuals, persistence),
        "log_rmse_timesfm": rmse(actuals, forecasts),
        "log_rmse_persistence": rmse(actuals, persistence),
        "five_day_return_mae_timesfm": mae(actual_returns, forecast_returns),
        "five_day_return_mae_persistence": mae(actual_returns, [0.0] * len(actual_returns)),
        "directional_accuracy_timesfm": float(np.mean(
            (np.asarray(actual_returns) > 0) == (np.asarray(forecast_returns) > 0)
        )),
        "directional_base_rate": float(np.mean(np.asarray(actual_returns) > 0)),
        "q10_q90_width_h5_spearman_vs_abs_move": float(
            spearman_rank_ic(np.asarray(abs_moves), np.asarray(interval_widths))
        ) if interval_widths else float("nan"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    ap.add_argument("--output", default="p3_stock_multifold_results")
    args = ap.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    data_dir = Path(args.data_dir)
    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    fold_rows: list[dict] = []
    stock_rows: list[dict] = []

    for symbol in symbols:
        dates, values = load_adjusted(data_dir / f"{symbol}.csv")
        folds = fold_origins(len(values))
        all_results = []
        for fold_no, origins in enumerate(folds, start=1):
            result = evaluate_fold(model, values, origins)
            result.update({
                "symbol": symbol,
                "fold": fold_no,
                "date_first_origin": dates[int(origins[0])],
                "date_last_origin": dates[int(origins[-1])],
            })
            fold_rows.append(result)
            all_results.append(result)

        stock_rows.append({
            "symbol": symbol,
            "rows": int(len(values)),
            "date_start": dates[0],
            "date_end": dates[-1],
            "folds": FOLDS,
            "origins_per_fold": ORIGINS_PER_FOLD,
            "total_origins": FOLDS * ORIGINS_PER_FOLD,
            "mean_log_mae_diff_timesfm_minus_persistence": float(np.mean([
                r["log_mae_timesfm"] - r["log_mae_persistence"] for r in all_results
            ])),
            "mean_log_rmse_diff_timesfm_minus_persistence": float(np.mean([
                r["log_rmse_timesfm"] - r["log_rmse_persistence"] for r in all_results
            ])),
            "mean_five_day_return_mae_diff_timesfm_minus_persistence": float(np.mean([
                r["five_day_return_mae_timesfm"] - r["five_day_return_mae_persistence"] for r in all_results
            ])),
            "mean_directional_excess": float(np.mean([
                r["directional_accuracy_timesfm"] - r["directional_base_rate"] for r in all_results
            ])),
            "mean_interval_rho": float(np.nanmean([
                r["q10_q90_width_h5_spearman_vs_abs_move"] for r in all_results
            ])),
            "folds_with_mae_improvement": int(sum(
                r["log_mae_timesfm"] < r["log_mae_persistence"] for r in all_results
            )),
            "folds_with_rmse_improvement": int(sum(
                r["log_rmse_timesfm"] < r["log_rmse_persistence"] for r in all_results
            )),
        })

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "fold_results.json").write_text(json.dumps(fold_rows, indent=2) + "\\n", encoding="utf-8")
    (out / "per_stock_summary.json").write_text(json.dumps(stock_rows, indent=2) + "\\n", encoding="utf-8")

    summary = {
        "lane": "P1.1_exploratory_individual_stock_multifold",
        "model": "timesfm-3.0-pytorch",
        "stocks": len(stock_rows),
        "folds": FOLDS,
        "origins_per_fold": ORIGINS_PER_FOLD,
        "total_stock_origins": len(stock_rows) * FOLDS * ORIGINS_PER_FOLD,
        "mean_stock_log_mae_diff": float(np.mean([r["mean_log_mae_diff_timesfm_minus_persistence"] for r in stock_rows])),
        "mean_stock_log_rmse_diff": float(np.mean([r["mean_log_rmse_diff_timesfm_minus_persistence"] for r in stock_rows])),
        "mean_stock_return_mae_diff": float(np.mean([r["mean_five_day_return_mae_diff_timesfm_minus_persistence"] for r in stock_rows])),
        "mean_stock_directional_excess": float(np.mean([r["mean_directional_excess"] for r in stock_rows])),
        "mean_stock_interval_rho": float(np.nanmean([r["mean_interval_rho"] for r in stock_rows])),
        "stocks_with_nonnegative_mean_directional_excess": int(sum(r["mean_directional_excess"] >= 0 for r in stock_rows)),
        "stocks_with_mean_mae_improvement": int(sum(r["mean_log_mae_diff_timesfm_minus_persistence"] < 0 for r in stock_rows)),
        "note": "Exploratory chronological-fold robustness test. Not PIT-final evidence, not cost-aware strategy validation, and not a promotion gate.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
