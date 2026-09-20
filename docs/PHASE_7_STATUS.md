# Phase 7 status

Updated: 2026-09-20 IST

## Status

**Cost-engineering bootstrap complete; empirical walk-forward waits for frozen P0 data and Phase 3 forecast gate.**

## Implemented

- Date-versioned fee manifest remains the source of rates.
- Execution-event model counts actual unique executed F&O orders rather than signals.
- Current 2026 STT rules are represented for cash delivery, cash intraday sales, futures sales and option sales.
- Paytm Money F&O brokerage and intraday square-off charges are represented.
- Spread and slippage are explicit cost components.
- Forced square-off is represented as an execution event.
- Option slippage is modeled at contract level rather than using underlying-equity slippage as a proxy.

## Walk-forward gate

Every promoted simulation must report gross and net P&L, brokerage, statutory charges, spread/slippage, turnover, cost per trade and break-even slippage. Stressed scenarios must include higher spread/impact and incomplete fills where data permit.

No strategy is promoted until the P0 data gate, Phase 3 forecast gate, realistic execution model and multiple-testing controls pass.


## Phase 7 frozen candidate — 2026-09-20

A single post-selection candidate is now registered for the final cost-aware holdout:

- TimesFM 3.0 cross-sectional stock ranking;
- 10-session horizon;
- top-six long-only;
- 20-session momentum control;
- 2023-01-01+ holdout;
- 10-session non-overlapping rebalances;
- PIT eligibility at each origin;
- position-drift-aware rebalancing;
- explicit final liquidation;
- dated cash-equity brokerage/statutory/DP model;
- one-way slippage/impact stresses from 0 to 0.50%;
- capacity, year/regime and block-aware inference diagnostics.

No tuning or alternative TimesFM variants are permitted in this holdout. The Phase 4B candidate remains research-only and non-executing.
