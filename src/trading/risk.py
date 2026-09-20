from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ExecutionMode = Literal["simulation", "paper", "live"]


@dataclass(frozen=True)
class RiskLimits:
    max_gross_exposure: float = 1.0
    max_single_trade_loss: float = 0.01
    max_participation: float = 0.10


def interval_uncertainty(lower_quantile: float, upper_quantile: float) -> float:
    """Return half-width of a forecast interval as a scalar uncertainty measure."""
    if not (upper_quantile >= lower_quantile):
        return 0.0
    return 0.5 * (upper_quantile - lower_quantile)


def uncertainty_adjusted_size(
    *,
    expected_edge: float,
    forecast_uncertainty: float,
    volatility: float,
    capital: float,
    risk_fraction: float = 0.01,
    limits: RiskLimits = RiskLimits(),
) -> float:
    if expected_edge <= 0 or forecast_uncertainty <= 0 or volatility <= 0:
        return 0.0
    confidence = min(1.0, expected_edge / forecast_uncertainty)
    risk_budget = capital * min(risk_fraction, limits.max_single_trade_loss)
    raw = risk_budget * confidence / volatility
    return max(0.0, min(raw, capital * limits.max_gross_exposure))


def passes_edge_gate(
    expected_move: float,
    cost_hurdle: float,
    safety_multiple: float = 1.0,
) -> bool:
    return expected_move > cost_hurdle * safety_multiple


def passes_license_gate(
    license_state: str,
    model_id: str,
    execution_mode: ExecutionMode = "simulation",
) -> bool:
    """Validate model use for the project's declared execution mode.

    TimesFM 3.0 research_only is valid for non-executing simulation only.
    Live/production modes require an explicitly licensed production model.
    """
    if execution_mode == "simulation":
        if model_id.startswith("timesfm-3.0"):
            return license_state == "research_only"
        return license_state in {"research_only", "licensed_production"}

    if model_id.startswith("timesfm-3.0"):
        return license_state == "licensed_production"

    return license_state == "licensed_production"
