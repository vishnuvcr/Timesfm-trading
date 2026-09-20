from src.options.research_rules import (
    debit_spread_max_loss,
    debit_spread_max_profit,
    forecast_move_from_quantiles,
    implied_move_from_iv,
    implied_residual,
    passes_option_edge_gate,
)


def test_implied_move_uses_iv_and_dte() -> None:
    move = implied_move_from_iv(0.20, 100.0, 30.0)
    assert 5.7 < move < 5.8


def test_forecast_range_and_residual() -> None:
    assert forecast_move_from_quantiles(-0.03, 0.05) == 0.05
    assert implied_residual(0.05, 0.03, calibration_error=0.005) == 0.015


def test_option_edge_gate_includes_safety_multiple() -> None:
    assert passes_option_edge_gate(0.02, 0.01, safety_multiple=1.5)
    assert not passes_option_edge_gate(0.014, 0.01, safety_multiple=1.5)


def test_debit_spread_has_bounded_risk() -> None:
    assert debit_spread_max_loss(1.25) == 1.25
    assert debit_spread_max_profit(5.0, 1.25) == 3.75
