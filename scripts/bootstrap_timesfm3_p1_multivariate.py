from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter
from src.stats.forecast_metrics import (
    directional_accuracy,
    mae,
    rmse,
)


SOURCE_FILES = {
    "NIFTY50": "NIFTY_50(INDEX)from2000.csv",
    "RELIANCE": "NSE_RELIANCE_from2000.csv",
    "TCS": "NSE_TCS_from2000.csv",
    "HDFCBANK": "NSE_HDFCBANK_from2000.csv",
    "HINDUNILVR": "NSE_HINDUNILVR_from2000.csv",
}
SOURCE_COMMIT = "c73de0e6c9acca1330a19cd41ee3d7dbd5100260"
CONTEXT = 128
HORIZON = 5
ORIGINS = 80


def load(path: Path) -> dict[str, float]:
    out: dict[str, float] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            d = datetime.strptime(row["Date"], "%m/%d/%Y").date().isoformat()
            close = float(row["Close"])
            if close > 0:
                out[d] = close
    return out


def forecast_vector(out, horizon: int, target_index: int | None = None) -> np.ndarray:
    arr = np.asarray(out.forecast, dtype=float)
    if target_index is None:
        arr = arr.reshape(-1)
    else:
        if arr.ndim == 2:
            arr = arr[target_index]
        else:
            arr = arr.reshape(-1)
    if arr.size != horizon:
        raise RuntimeError(f"unexpected forecast shape {np.asarray(out.forecast).shape}")
    return arr


def evaluate(
    model: TimesFM3Adapter,
    name: str,
    contexts: list[np.ndarray],
    actuals: list[np.ndarray],
    horizon: int,
    *,
    past_only_covariates: list[np.ndarray] | None = None,
    target_index: int | None = None,
) -> dict:
    outputs = model.predict_batch(
        contexts,
        horizon=horizon,
        past_only_covariates=past_only_covariates,
        return_quantiles=False,
        univariate=(target_index is None and past_only_covariates is None),
    )
    preds = []
    ys = []
    for out, actual in zip(outputs, actuals):
        p = forecast_vector(out, horizon, target_index=target_index)
        preds.append(float(p[-1]))
        ys.append(float(actual[-1]))
    preds_arr = np.asarray(preds)
    ys_arr = np.asarray(ys)
    returns_pred = preds_arr - np.asarray([c[-1] for c in contexts])
    returns_actual = ys_arr - np.asarray([c[0] if target_index is not None else c[-1] for c in contexts])
    return {
        "model": name,
        "mae_log_level": mae(ys_arr, preds_arr),
        "rmse_log_level": rmse(ys_arr, preds_arr),
        "directional_accuracy": directional_accuracy(returns_actual, returns_pred),
        "n_origins": len(preds),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    series = {
        name: load(data_dir / filename)
        for name, filename in SOURCE_FILES.items()
    }
    dates = sorted(set.intersection(*(set(v) for v in series.values())))
    if len(dates) < CONTEXT + HORIZON + ORIGINS:
        raise RuntimeError(f"insufficient aligned dates: {len(dates)}")

    values = {
        name: np.log(np.asarray([series[name][d] for d in dates], dtype=np.float32))
        for name in series
    }
    origin_idx = np.linspace(
        len(dates) - ORIGINS - HORIZON,
        len(dates) - HORIZON - 1,
        ORIGINS,
        dtype=int,
    )

    uni_contexts = [values["NIFTY50"][i - CONTEXT:i] for i in origin_idx]
    uni_actuals = [values["NIFTY50"][i:i + HORIZON] for i in origin_idx]

    multi_contexts = [
        np.stack(
            [values[name][i - CONTEXT:i] for name in SOURCE_FILES],
            axis=0,
        )
        for i in origin_idx
    ]
    multi_actuals = [
        np.stack(
            [values[name][i:i + HORIZON] for name in SOURCE_FILES],
            axis=0,
        )
        for i in origin_idx
    ]

    covariate_contexts = [
        values["NIFTY50"][i - CONTEXT:i] for i in origin_idx
    ]
    covariates = [
        np.stack(
            [values[name][i - CONTEXT:i] for name in ("RELIANCE", "TCS", "HDFCBANK", "HINDUNILVR")],
            axis=0,
        )
        for i in origin_idx
    ]

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    results = []
    uni = evaluate(
        model,
        "univariate",
        uni_contexts,
        uni_actuals,
        HORIZON,
    )
    results.append(uni)

    multi_outputs = model.predict_batch(
        multi_contexts,
        horizon=HORIZON,
        return_quantiles=False,
        univariate=False,
    )
    multi_pred = np.asarray([forecast_vector(o, HORIZON, target_index=0)[-1] for o in multi_outputs])
    multi_actual = np.asarray([a[0, -1] for a in multi_actuals])
    multi_last = np.asarray([c[0, -1] for c in multi_contexts])
    results.append(
        {
            "model": "native_multivariate_5_series",
            "mae_log_level": mae(multi_actual, multi_pred),
            "rmse_log_level": rmse(multi_actual, multi_pred),
            "directional_accuracy": directional_accuracy(multi_actual - multi_last, multi_pred - multi_last),
            "n_origins": len(multi_pred),
        }
    )

    cov_outputs = model.predict_batch(
        covariate_contexts,
        horizon=HORIZON,
        past_only_covariates=covariates,
        return_quantiles=False,
        univariate=True,
    )
    cov_pred = np.asarray([forecast_vector(o, HORIZON)[-1] for o in cov_outputs])
    cov_actual = np.asarray([a[-1] for a in uni_actuals])
    cov_last = np.asarray([c[-1] for c in covariate_contexts])
    results.append(
        {
            "model": "univariate_plus_4_past_only_covariates",
            "mae_log_level": mae(cov_actual, cov_pred),
            "rmse_log_level": rmse(cov_actual, cov_pred),
            "directional_accuracy": directional_accuracy(cov_actual - cov_last, cov_pred - cov_last),
            "n_origins": len(cov_pred),
        }
    )

    summary = {
        "lane": "P1_exploratory_phase3_ablation",
        "source_repo": "Gajapathy-Selvaraj/Stock_Market_Datasets_NSE",
        "source_commit": SOURCE_COMMIT,
        "series": list(SOURCE_FILES),
        "rows_aligned": len(dates),
        "date_start": dates[0],
        "date_end": dates[-1],
        "origins": ORIGINS,
        "context": CONTEXT,
        "horizon": HORIZON,
        "results": results,
        "note": "Secondary-data ablation only; not primary NSE evidence and not eligible for strategy promotion.",
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
