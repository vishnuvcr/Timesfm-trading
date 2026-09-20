# Phase 7 status

Updated: 2026-09-20 IST

## Status

**Cost-engineering bootstrap complete; no individual-stock candidate advanced to the final promotion walk-forward.**

## Implemented

- Date-versioned fee manifest remains the source of rates.
- Execution-event model counts actual unique executed orders rather than signals.
- Current 2026 STT rules are represented for cash delivery, cash intraday sales, futures sales and option sales.
- Paytm Money brokerage and execution constraints are represented through dated research inputs.
- Spread and slippage are explicit cost components.
- Forced square-off is represented as an execution event.
- Option slippage is modeled at contract level rather than using underlying-equity slippage as a proxy.

## Research result

The Phase 4 and Phase 6 stock candidates failed before the final Phase 7 promotion gate: the simple TimesFM stock selectors and the regime-conditioned residual overlay did not remain superior to the independent momentum control under cost stress.

Accordingly, no full promoted-strategy walk-forward is claimed. The cost engine remains available for any future preregistered candidate.

## Promotion rule

Every promoted simulation must report gross and net P&L, brokerage, statutory charges, spread/slippage, turnover, cost per trade and break-even slippage. Stressed scenarios must include higher spread/impact and incomplete fills where data permit.

No strategy is promoted without P0 data integrity, forecast evidence, realistic execution modeling and multiple-testing controls.


## Final post-selection holdout — 2026-09-20

Workflow 35527715462 / artifact 10610571439 completed the frozen individual-stock TimesFM 10-session holdout.

The untouched 2023-01-02 to 2026-09-03 period contained 91 non-overlapping rebalances with 29–30 PIT-eligible names per origin. The candidate was fixed before the holdout: TimesFM 3.0 10-session cross-sectional rank, top six long-only, compared with the 20-session momentum control.

Net total return after the dated cash-equity cost model:
- 0.00% extra slippage: TimesFM +3.72% vs momentum +67.97%;
- 0.125%: -7.93% vs +47.20%;
- 0.25%: -18.30% vs +28.96%;
- 0.375%: -27.52% vs +12.94%;
- 0.50%: -35.72% vs -1.12%.

At 0.50% extra slippage, TimesFM max drawdown was -41.46% and periodized Sharpe -0.736 versus momentum -23.80% and +0.059. Capacity was not the limiting factor: maximum simulated participation was about 0.014% of trailing turnover.

Paired block-signflip p-values were 0.972–0.984 one-sided against an alternative of TimesFM outperforming momentum.

**Decision:** the single frozen Phase 4B stock candidate failed Phase 7 and is closed. No additional TimesFM threshold, horizon, hybrid, or regime search is permitted on this completed holdout.
