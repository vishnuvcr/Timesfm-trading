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
