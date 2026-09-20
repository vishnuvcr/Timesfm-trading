from __future__ import annotations

from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class ForecastMetrics:
    mae: float
    rmse: float
    directional_accuracy: float
    base_rate_up: float
    excess_directional_accuracy: float
    rank_ic: float
    pinball_loss: float | None
    coverage_q10_q90: float | None

def _finite_pair(actual: np.ndarray, forecast: np.ndarray):
    y = np.asarray(actual, dtype=float).reshape(-1)
    p = np.asarray(forecast, dtype=float).reshape(-1)
    m = np.isfinite(y) & np.isfinite(p)
    if not np.any(m):
        raise ValueError("no finite forecast/actual pairs")
    return y[m], p[m]

def mae(actual, forecast):
    y, p = _finite_pair(actual, forecast)
    return float(np.mean(np.abs(y - p)))

def rmse(actual, forecast):
    y, p = _finite_pair(actual, forecast)
    return float(np.sqrt(np.mean((y - p) ** 2)))

def directional_accuracy(actual_returns, forecast_returns):
    y, p = _finite_pair(actual_returns, forecast_returns)
    return float(np.mean((y > 0) == (p > 0)))

def excess_directional_accuracy(actual_returns, forecast_returns):
    y, p = _finite_pair(actual_returns, forecast_returns)
    acc = directional_accuracy(y, p)
    base = float(np.mean(y > 0))
    return acc, base, acc - base

def spearman_rank_ic(actual, forecast):
    y, p = _finite_pair(actual, forecast)
    if y.size < 2:
        return float("nan")
    yr = np.argsort(np.argsort(y)).astype(float)
    pr = np.argsort(np.argsort(p)).astype(float)
    yr -= yr.mean(); pr -= pr.mean()
    denom = float(np.sqrt(np.dot(yr, yr) * np.dot(pr, pr)))
    return float(np.dot(yr, pr) / denom) if denom > 0 else float("nan")

def pinball_loss(actual, forecast, quantile):
    y, q = _finite_pair(actual, forecast)
    e = y - q
    return float(np.mean(np.maximum(quantile * e, (quantile - 1.0) * e)))

def interval_coverage(actual, lower, upper):
    y = np.asarray(actual, dtype=float).reshape(-1)
    lo = np.asarray(lower, dtype=float).reshape(-1)
    hi = np.asarray(upper, dtype=float).reshape(-1)
    m = np.isfinite(y) & np.isfinite(lo) & np.isfinite(hi)
    if not np.any(m):
        raise ValueError("no finite interval observations")
    return float(np.mean((y[m] >= lo[m]) & (y[m] <= hi[m])))
