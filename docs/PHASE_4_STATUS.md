# Phase 4 status

Updated: 2026-09-20 IST\n\n## Scope expansion — individual stocks\n\nIndividual NSE-listed stocks are now explicit first-class research instruments. The index lane and stock lane will run in parallel once their respective data-quality gates are satisfied. A 30-name fixed panel is an engineering/bootstrap cache only; final evidence must use point-in-time liquidity/membership rules. See [INDIVIDUAL_STOCK_STRATEGY_DESIGN](INDIVIDUAL_STOCK_STRATEGY_DESIGN.md).

## Status

**Daily individual-stock TimesFM strategy gate closed.** Phase 4.1 and nested Phase 4.2 tests are complete; no tested daily TimesFM stock-selection mechanism survived the declared chronological, baseline and cost-aware gates. Intraday/scalping and event/market-state studies remain separate gates.

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


## 2026-09-20 — empirical Phase 4.1 stock overlay launched

Phase 3's broader stock test did not support standalone TimesFM direction against persistence. Phase 4 therefore switches to an incremental-information design: an independently specified 20-session cross-sectional momentum control, a TimesFM 5-session forecast rank, a 50/50 standardized hybrid, and a momentum-gated TimesFM variant.

The experiment uses the common history of the 30-name bootstrap, four chronological folds, eight non-overlapping rebalances per fold, top-six long-only selection, and four all-in one-way cost-stress scenarios. Cash equity is the trading instrument. Brokerage and delivery-sale DP references are included as explicit fixed-order costs, while proportional costs are stressed rather than treated as a historical-exact fee schedule.

This is a research-only, non-executing TimesFM 3.0 simulation. It cannot promote a live strategy.



## 2026-09-20 — Phase 4.1 result

Workflow 35523966952 completed successfully (artifact 10609283452). The test used the common history of 30 bootstrap stocks, four chronological folds, eight non-overlapping 5-session rebalances per fold (32 total), top-six long-only selection, and explicit brokerage/DP plus proportional cost stress.

Cross-sectional result:
- momentum 20-session mean rank IC: +0.0138;
- TimesFM 5-session forecast mean rank IC: -0.0237;
- 50/50 hybrid mean rank IC: -0.0151;
- TimesFM top-six excess return versus equal-weight universe: -0.00554 per 5-session period on average;
- hybrid top-six excess: -0.00359;
- TimesFM versus momentum top-six excess differential: -0.00416.

At the lowest proportional cost scenario tested (0.125% one-way), net total return over the sparse 32-rebalance test was -26.6% for TimesFM-only, -21.8% for the hybrid, and -15.2% for the momentum control. The equal-weight universe control was -7.3%. Results became more negative as costs were stressed to 0.50% one-way.

Interpretation: this is a negative Phase 4.1 result for standalone TimesFM stock selection and for the tested simple hybrid overlay. The test is sparse and uses stress-cost assumptions rather than the final effective-date fee engine, so it is not a final economic verdict. It is sufficient to reject promotion of these two simple stock overlays into the next strategy gate.

Next Phase 4 research question: test whether TimesFM can add **incremental conditional information** to a stronger, independently specified stock-selection signal only after regime/liquidity/event conditioning, rather than using the raw TimesFM forecast as the selector.


## 2026-09-20 — synchronized Phase 4.2 result

The nested regime-conditioned experiment (workflow 35524516653, artifact 10609740180) used prior-fold-only breadth thresholds and a TimesFM-minus-momentum residual. It was tested on folds 2–4 across 30 stocks and 24 rebalances.

At 0.125% one-way cost, momentum returned -5.20% and the residual -10.02%; at 0.25%, -7.72% versus -12.22%; at 0.375%, -10.16% versus -14.37%; at 0.50%, -12.55% versus -16.48%.

Decision: close the current daily stock TimesFM overlay gate. No daily individual-stock TimesFM strategy is validated.
