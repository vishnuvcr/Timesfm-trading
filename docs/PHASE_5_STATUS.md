# Phase 5 status

Updated: 2026-09-20 IST

## Status

**Protocol/engineering bootstrap in progress.** Empirical options research is blocked until authorized historical option data and a frozen Phase 3 forecast dataset are available.

## Implemented

- Frozen options research protocol.
- Explicit market-implied forecast benchmark requirement.
- Defined-risk strategy families.
- Research primitives for IV-implied movement, TimesFM forecast movement, residual-vs-implied edge, and debit-spread bounded-risk accounting.
- Unit tests for the options research primitives.
- Manual GitHub Actions workflow for protocol/unit validation.

## Research rule

TimesFM 3.0 is the primary scientific model. Option conclusions must compare against:
1. naive/statistical forecasts,
2. the option market's own implied movement/forward-variance information,
3. realistic option costs, spread and slippage.

No option family is promoted from underlying directional accuracy alone.

## Data gate

Required before empirical work:
- authorized historical option quotes/trades;
- exact contract identifiers and lifecycle;
- bid/ask, OI, volume and IV where available;
- PIT-safe corporate actions and expiry calendars;
- frozen TimesFM forecast origins.

No live or broker order execution is part of this phase.
