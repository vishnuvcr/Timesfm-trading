from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter
from src.stats.forecast_metrics import mae, rmse


ENDPOINT = "https://www.niftyindices.com/Backpage.aspx/getTotalReturnIndexString"
INDEX_NAME = "NIFTY 50"
START_DATE = "01-Jan-2000"
END_DATE = "18-Sep-2026"
CONTEXT = 128
HORIZON = 5
ORIGINS = 80


def fetch_tri() -> list[tuple[str, float]]:
    cinfo = (
        f"{{'name':'{INDEX_NAME}','startDate':'{START_DATE}',"
        f"'endDate':'{END_DATE}','indexName':'{INDEX_NAME}'}}"
    )
    payload = json.dumps({"cinfo": cinfo}).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.niftyindices.com/reports/historical-data",
        "User-Agent": "Mozilla/5.0 (compatible; TimesFM-NSE-research/1.0)",
    }
    req = Request(ENDPOINT, data=payload, headers=headers, method="POST")
    with urlopen(req, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))
    rows = json.loads(body["d"])
    out = []
    for row in rows:
        d = datetime.strptime(row["Date"], "%d %b %Y").date().isoformat()
        out.append((d, float(row["TotalReturnsIndex"])))
    out.sort()
    return out


def main() -> None:
    rows = fetch_tri()
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
        "dataset": "NIFTY 50 Total Return Index",
        "source": ENDPOINT,
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
        "note": "Exploratory pipeline validation only; not a primary trading result and not a P0 promotion result.",
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
