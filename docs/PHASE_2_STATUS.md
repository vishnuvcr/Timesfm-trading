# Phase 2 status

Updated: 2026-09-20 IST

## Status
In progress — source and schema architecture complete; acquisition validation next.

## Completed
- Point-in-time data policy.
- Source registry with P0/P1 source families.
- Storage/licensing tiers.
- Dataset manifest schema.
- Manifest validator.
- Synthetic PIT test fixture.
- Manual Phase 2 GitHub Actions validation workflow.
- Official-source audit for NSE historical reports, UDiFF derivatives reports, India VIX, option chain, FII/FPI/DII, corporate actions, paid historical trade/order data, GIFT NIFTY and BSE historical products.

## Validation result
The same validator code was executed in a local offline harness:
- manifest validation: passed
- synthetic future-availability rejection test: passed
- pytest: 2 passed

A direct repository clone from the execution container was attempted for an end-to-end repository test, but the environment could not resolve github.com. This is logged as an environment/network limitation, not a code failure.

## Next gate
Acquire or connect the first licensed/permitted P0 datasets, generate real manifests, and run:
1. schema conformance,
2. PIT leakage tests,
3. calendar/session tests,
4. corporate-action discontinuity tests,
5. derivative contract lifecycle tests,
6. option quote integrity tests.

Only after these pass will Phase 3 begin.


## Canonical schema layer added

Phase 2 now defines canonical schemas and invariant checks for equity bars, option quotes, derivative contracts and corporate actions. These checks explicitly reject impossible OHLC, negative volume/OI, crossed quotes, post-expiry quotes, invalid contract chronology and corporate-action dates that precede the announcement timestamp.
