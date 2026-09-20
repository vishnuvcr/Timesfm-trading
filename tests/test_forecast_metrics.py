import numpy as np

from src.stats.forecast_metrics import (
    excess_directional_accuracy,
    interval_coverage,
    mae,
    rmse,
    spearman_rank_ic,
)


def test_basic_forecast_metrics() -> None:
    actual = np.array([1.0, 2.0, 3.0])
    forecast = np.array([1.0, 2.5, 2.0])
    assert np.isclose(mae(actual, forecast), 0.5)
    assert np.isclose(rmse(actual, forecast), np.sqrt(1.25 / 3))


def test_directional_excess_uses_base_rate() -> None:
    actual = np.array([0.01, -0.01, 0.02, 0.03])
    forecast = np.array([0.01, 0.01, 0.01, 0.01])
    acc, base, excess = excess_directional_accuracy(actual, forecast)
    assert acc == 0.75
    assert base == 0.75
    assert excess == 0.0


def test_rank_ic_and_coverage() -> None:
    x = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.isclose(spearman_rank_ic(x, x), 1.0)
    assert interval_coverage(x, x - 0.5, x + 0.5) == 1.0
