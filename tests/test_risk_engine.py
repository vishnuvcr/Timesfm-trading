import numpy as np

from src.trading.risk import passes_edge_gate, passes_license_gate, uncertainty_adjusted_size


def test_edge_gate_rejects_non_positive_net_edge() -> None:
    assert not passes_edge_gate(0.01, 0.01)
    assert passes_edge_gate(0.021, 0.01, safety_multiple=2.0)


def test_uncertainty_adjusted_size_drops_when_uncertainty_is_zero() -> None:
    assert uncertainty_adjusted_size(expected_edge=0.1, forecast_uncertainty=0.0, volatility=0.2, capital=100000.0) == 0.0


def test_timesfm3_license_gate() -> None:
    assert not passes_license_gate("research_only", "timesfm-3.0-pytorch")
    assert passes_license_gate("licensed_production", "timesfm-3.0-pytorch")
    assert passes_license_gate("research_only", "timesfm-2.5-pytorch")
