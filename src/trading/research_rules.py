from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastEnvelope:
    mean: float
    q10: float
    q90: float
    uncertainty: float


@dataclass(frozen=True)
class CostProfile:
    round_trip_cost: float
    safety_multiple: float = 1.25


def net_edge(expected_move: float, costs: CostProfile) -> float:
    return expected_move - costs.round_trip_cost


def directional_gate(expected_move: float, costs: CostProfile) -> bool:
    return expected_move > costs.round_trip_cost * costs.safety_multiple


def envelope_move(envelope: ForecastEnvelope) -> float:
    return max(abs(envelope.q10), abs(envelope.q90), abs(envelope.mean))


def uncertainty_confidence(envelope: ForecastEnvelope) -> float:
    if envelope.uncertainty <= 0:
        return 0.0
    return max(0.0, min(1.0, abs(envelope.mean) / envelope.uncertainty))


def volatility_target_exposure(
    *,
    target_volatility: float,
    forecast_volatility: float,
    max_exposure: float = 1.0,
) -> float:
    if target_volatility <= 0 or forecast_volatility <= 0:
        return 0.0
    return max(
        0.0,
        min(max_exposure, target_volatility / forecast_volatility),
    )


def overnight_edge_gate(
    expected_gap: float,
    round_trip_cost: float,
    overnight_safety_multiple: float = 1.5,
) -> bool:
    return abs(expected_gap) > round_trip_cost * overnight_safety_multiple
