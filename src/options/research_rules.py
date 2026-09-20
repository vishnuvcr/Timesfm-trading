from __future__ import annotations

from math import sqrt


TRADING_DAYS_PER_YEAR = 365.0


def implied_move_from_iv(iv: float, spot: float, dte_days: float) -> float:
    if iv <= 0 or spot <= 0 or dte_days <= 0:
        return 0.0
    return spot * iv * sqrt(dte_days / TRADING_DAYS_PER_YEAR)


def forecast_move_from_quantiles(q10: float, q90: float) -> float:
    return max(abs(q10), abs(q90))


def implied_residual(
    forecast_move: float,
    implied_move: float,
    calibration_error: float = 0.0,
) -> float:
    return abs(forecast_move - implied_move) - max(0.0, calibration_error)


def passes_option_edge_gate(
    residual: float,
    total_cost: float,
    safety_multiple: float = 1.5,
) -> bool:
    return residual > total_cost * safety_multiple


def debit_spread_max_loss(net_debit: float) -> float:
    return max(0.0, net_debit)


def debit_spread_max_profit(
    spread_width: float,
    net_debit: float,
) -> float:
    if spread_width <= 0:
        return 0.0
    return max(0.0, spread_width - max(0.0, net_debit))
