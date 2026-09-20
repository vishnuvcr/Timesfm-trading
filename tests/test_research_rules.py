from src.trading.research_rules import (
    CostProfile,
    ForecastEnvelope,
    directional_gate,
    envelope_move,
    net_edge,
    overnight_edge_gate,
    uncertainty_confidence,
    volatility_target_exposure,
)


def test_cost_adjusted_edge_and_direction_gate() -> None:
    costs = CostProfile(round_trip_cost=0.01, safety_multiple=1.25)
    assert net_edge(0.02, costs) == 0.01
    assert directional_gate(0.02, costs)
    assert not directional_gate(0.011, costs)


def test_uncertainty_confidence_is_bounded() -> None:
    env = ForecastEnvelope(mean=0.02, q10=-0.01, q90=0.05, uncertainty=0.04)
    assert uncertainty_confidence(env) == 0.5
    assert envelope_move(env) == 0.05


def test_volatility_target_exposure_is_capped() -> None:
    assert volatility_target_exposure(target_volatility=0.10, forecast_volatility=0.20) == 0.5
    assert volatility_target_exposure(target_volatility=0.20, forecast_volatility=0.10) == 1.0


def test_overnight_gate_requires_a_hurdle() -> None:
    assert overnight_edge_gate(0.03, 0.01, overnight_safety_multiple=2.0)
    assert not overnight_edge_gate(0.02, 0.01, overnight_safety_multiple=2.0)
