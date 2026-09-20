from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter
from src.stats.forecast_metrics import mae, rmse


P1_SOURCE_COMMIT = "c73de0e6c9acca1330a19cd41ee3d7dbd5100260"
P1_SOURCE_BLOB = "fc51a9331ee2b72c430724d5e0bdd0237f91103a"
P1_SOURCE_REPO = "Gajapathy-Selvaraj/Stock_Market_Datasets_NSE"
P1_SOURCE_FILE = "NIFTY_50(INDEX)from2000.csv"
CONTEXT = 128
HORIZON = 5
ORIGINS = 80


def load_p1_csv(path: Path) -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"Date", "Open", "High", "Low", "Close"}
        if not required.issubset(reader.fieldnames or []):
            raise RuntimeError(f"missing columns: {sorted(required)}")
        for row in reader:
            try:
                dt = datetime.strptime(row["Date"], "%m/%d/%Y").date().isoformat()
                close = float(row["Close"])
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError(f"invalid P1 row: {row}") from exc
            if close <= 0:
                raise RuntimeError(f"non-positive close: {row}")
            out.append((dt, close))
    out.sort()
    if len(out) < CONTEXT + HORIZON + ORIGINS:
        raise RuntimeError(f"insufficient P1 rows: {len(out)}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    args = ap.parse_args()
    rows = load_p1_csv(Path(args.input))
    if len(rows) < CONTEXT + HORIZON + ORIGINS:
        raise RuntimeError(f"insufficient TRI rows: {len(rows)}")

    dates = [d for d, _ in rows]
    values = np.log(np.asarray([v for _, v in rows], dtype=np.float32))

    origin_idx = np.linspace(
        len(values) - ORIGINS - HORIZON,
        len(values) - HORIZON - 1,
        ORIGINS,
        dtype=int,
    )
    contexts = [values[i - CONTEXT:i].copy() for i in origin_idx]

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )
    outputs = model.predict_batch(
        contexts,
        horizon=HORIZON,
        return_quantiles=True,
        univariate=True,
    )

    forecasts = []
    actuals = []
    persistence = []
    q10 = []
    q90 = []
    forecast_returns = []
    actual_returns = []
    persistence_returns = []

    for idx, out in zip(origin_idx, outputs):
        pred = np.asarray(out.forecast).reshape(-1)
        if pred.size != HORIZON:
            raise RuntimeError(f"unexpected forecast shape: {out.forecast.shape}")
        actual = values[idx:idx + HORIZON]
        last = values[idx - 1]
        forecasts.extend(pred.tolist())
        actuals.extend(actual.tolist())
        persistence.extend([last] * HORIZON)
        forecast_returns.append(float(pred[-1] - last))
        actual_returns.append(float(actual[-1] - last))
        persistence_returns.append(0.0)
        if out.quantiles is not None:
            q = np.asarray(out.quantiles)
            q = q.reshape(-1, HORIZON, 9) if q.ndim == 3 else q
            if q.ndim != 3:
                raise RuntimeError(f"unexpected quantile shape: {out.quantiles.shape}")
            q10.extend(q[0, :, 0].tolist())
            q90.extend(q[0, :, -1].tolist())

    summary = {
        "lane": "P1_exploratory_bootstrap",
        "primary_model": "timesfm-3.0-pytorch",
        "dataset": "NIFTY 50 daily OHLC secondary snapshot",
        "source_repo": P1_SOURCE_REPO,
        "source_file": P1_SOURCE_FILE,
        "source_commit": P1_SOURCE_COMMIT,
        "source_blob": P1_SOURCE_BLOB,
        "date_start": dates[0],
        "date_end": dates[-1],
        "origins": len(origin_idx),
        "context": CONTEXT,
        "horizon": HORIZON,
        "log_level_mae_timesfm": mae(actuals, forecasts),
        "log_level_rmse_timesfm": rmse(actuals, forecasts),
        "log_level_mae_persistence": mae(actuals, persistence),
        "log_level_rmse_persistence": rmse(actuals, persistence),
        "five_day_return_mae_timesfm": mae(actual_returns, forecast_returns),
        "five_day_return_mae_persistence": mae(actual_returns, persistence_returns),
        "directional_accuracy_timesfm": float(np.mean((np.asarray(actual_returns) > 0) == (np.asarray(forecast_returns) > 0))),
        "directional_base_rate": float(np.mean(np.asarray(actual_returns) > 0)),
        "note": "Pipeline-validation result only. Secondary Google Finance-derived snapshot; not P0 evidence and not eligible for strategy promotion.",
    }

    outdir = Path("p1_results")
    outdir.mkdir(exist_ok=True)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    with (outdir / "forecast_panel.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["origin_date", "horizon", "actual_log_tri", "forecast_log_tri", "persistence_log_tri", "q10", "q90"])
        k = 0
        for idx in origin_idx:
            for h in range(HORIZON):
                writer.writerow([
                    dates[idx + h],
                    h + 1,
                    f"{actuals[k]:.8f}",
                    f"{forecasts[k]:.8f}",
                    f"{persistence[k]:.8f}",
                    f"{q10[k]:.8f}" if q10 else "",
                    f"{q90[k]:.8f}" if q90 else "",
                ])
                k += 1

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
