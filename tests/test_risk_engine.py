from src.trading.risk import (
    interval_uncertainty,
    passes_edge_gate,
    passes_license_gate,
    uncertainty_adjusted_size,
)


def test_edge_gate_rejects_non_positive_net_edge() -> None:
    assert not passes_edge_gate(0.01, 0.01)
    assert passes_edge_gate(0.021, 0.01, safety_multiple=2.0)


def test_uncertainty_adjusted_size_drops_when_uncertainty_is_zero() -> None:
    assert uncertainty_adjusted_size(
        expected_edge=0.1,
        forecast_uncertainty=0.0,
        volatility=0.2,
        capital=100000.0,
    ) == 0.0


def test_timesfm3_is_allowed_for_non_executing_simulation() -> None:
    assert passes_license_gate("research_only", "timesfm-3.0-pytorch", "simulation")
    assert not passes_license_gate("research_only", "timesfm-3.0-pytorch", "live")
    assert passes_license_gate("licensed_production", "timesfm-3.0-pytorch", "live")


def test_timesfm25_can_be_used_as_research_benchmark() -> None:
    assert passes_license_gate("research_only", "timesfm-2.5-pytorch", "simulation")
    assert not passes_license_gate("research_only", "timesfm-2.5-pytorch", "live")


def test_interval_uncertainty_is_half_width_and_rejects_crossed_bounds() -> None:
    assert interval_uncertainty(0.90, 1.10) == 0.10
    assert interval_uncertainty(1.10, 0.90) == 0.0
