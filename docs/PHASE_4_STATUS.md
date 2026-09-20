# Phase 4 status

Updated: 2026-09-20 IST\n\n## Scope expansion — individual stocks\n\nIndividual NSE-listed stocks are now explicit first-class research instruments. The index lane and stock lane will run in parallel once their respective data-quality gates are satisfied. A 30-name fixed panel is an engineering/bootstrap cache only; final evidence must use point-in-time liquidity/membership rules. See [INDIVIDUAL_STOCK_STRATEGY_DESIGN](INDIVIDUAL_STOCK_STRATEGY_DESIGN.md).

## Status

**Research-engineering bootstrap in progress.** Empirical strategy testing is blocked until Phase 2 produces a frozen P0 dataset and Phase 3 completes its real forecast gate.

## Scope

TimesFM 3.0 remains the primary model for strategy research. This branch builds non-executing simulation primitives only; it does not place orders or create a production execution path.

## Implemented

- Canonical trade-decision schema.
- Uncertainty-adjusted position sizing primitive.
- Quantile-interval-to-uncertainty adapter for simulation sizing, motivated by the Phase 3 P1 interval-width/movement result.
- Cost-hurdle gate.
- License gate distinguishing research-only simulation from live/production use.
- Shared forecast-envelope and cost-aware signal primitives for scalping, intraday, BTST and swing research.\n- Individual-stock strategy design covering single-name overlays, cross-sectional ranking, uncertainty-conditioned sizing, stock-vs-index residuals and event-aware testing.
- Unit tests for risk, license and research-rule invariants.
- Manual GitHub Actions workflow; latest phase-4 CI run 70 passed after the interval-uncertainty test was corrected to use tolerance-based floating-point comparison.

## Research hypotheses represented by the shared primitives

- Scalping/intraday: movement must exceed a conservative round-trip cost hurdle.
- BTST: expected overnight gap must exceed a higher safety multiple because overnight uncertainty and gap risk are larger.
- Swing: exposure can be scaled using forecast volatility relative to a declared target volatility, subject to a cap.
- All variants must retain uncertainty and liquidity constraints and must be compared with a no-TimesFM control.

These are protocol primitives, not empirical results.

## Gate

No strategy is promoted until real P0 data, Phase 3 forecast results, cost assumptions and walk-forward tests are available.
