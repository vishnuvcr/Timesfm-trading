from __future__ import annotations

import math
import numpy as np


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def newey_west_long_run_variance(x: np.ndarray, max_lag: int) -> float:
    x = np.asarray(x, dtype=float).reshape(-1)
    x = x[np.isfinite(x)]
    if x.size < 2:
        raise ValueError("need at least two observations")
    centered = x - x.mean()
    gamma0 = float(np.mean(centered * centered))
    lr = gamma0
    for lag in range(1, min(max_lag, x.size - 1) + 1):
        weight = 1.0 - lag / (max_lag + 1.0)
        gamma = float(np.mean(centered[lag:] * centered[:-lag]))
        lr += 2.0 * weight * gamma
    return max(lr, 0.0)


def diebold_mariano(loss_a: np.ndarray, loss_b: np.ndarray, max_lag: int = 0) -> tuple[float, float]:
    a = np.asarray(loss_a, dtype=float).reshape(-1)
    b = np.asarray(loss_b, dtype=float).reshape(-1)
    if a.shape != b.shape:
        raise ValueError("loss arrays must have identical shape")
    mask = np.isfinite(a) & np.isfinite(b)
    d = (a - b)[mask]
    if d.size < 2:
        raise ValueError("need at least two paired loss observations")
    lrv = newey_west_long_run_variance(d, max_lag=max_lag)
    if lrv <= 0:
        return 0.0, 1.0
    stat = float(d.mean() / math.sqrt(lrv / d.size))
    p_one_sided = 1.0 - _normal_cdf(stat)
    return stat, p_one_sided


def block_bootstrap_mean_ci(values: np.ndarray, block_length: int, n_boot: int = 2000, seed: int = 7, alpha: float = 0.05) -> tuple[float, float, float]:
    x = np.asarray(values, dtype=float).reshape(-1)
    x = x[np.isfinite(x)]
    if x.size < 2:
        raise ValueError("need at least two observations")
    if block_length < 1:
        raise ValueError("block_length must be positive")
    rng = np.random.default_rng(seed)
    starts = np.arange(max(1, x.size - block_length + 1))
    n_blocks = int(math.ceil(x.size / block_length))
    boot = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        sample_parts = []
        for _ in range(n_blocks):
            start = int(rng.choice(starts))
            sample_parts.append(x[start:start + block_length])
        sample = np.concatenate(sample_parts)[:x.size]
        boot[i] = sample.mean()
    lo = float(np.quantile(boot, alpha / 2.0))
    hi = float(np.quantile(boot, 1.0 - alpha / 2.0))
    return float(x.mean()), lo, hi


def benjamini_hochberg(p_values: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(p_values, dtype=float).reshape(-1)
    if np.any((p < 0) | (p > 1) | ~np.isfinite(p)):
        raise ValueError("p_values must be finite and in [0, 1]")
    m = p.size
    order = np.argsort(p)
    ranked = p[order]
    thresholds = alpha * (np.arange(1, m + 1) / m)
    discoveries_sorted = ranked <= thresholds
    if np.any(discoveries_sorted):
        k = np.flatnonzero(discoveries_sorted)[-1]
        rejected_sorted = np.zeros(m, dtype=bool)
        rejected_sorted[: k + 1] = True
    else:
        rejected_sorted = np.zeros(m, dtype=bool)
    rejected = np.empty(m, dtype=bool)
    rejected[order] = rejected_sorted

    q_sorted = ranked * m / np.arange(1, m + 1)
    q_sorted = np.minimum.accumulate(q_sorted[::-1])[::-1]
    q_values = np.empty(m, dtype=float)
    q_values[order] = np.clip(q_sorted, 0.0, 1.0)
    return rejected, q_values
