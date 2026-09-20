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
