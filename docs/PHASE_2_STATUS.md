# Phase 2 status

Updated: 2026-09-20 IST

## Status
Validation green — source/schema architecture and CI validation complete; official public NIFTY P0 acquisition is currently blocked.

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
Local and GitHub Actions validation is now passing.

GitHub Actions run 30 validated the source registry, manifest validator and data-layer tests. The earlier run 19 failure was a syntax error in `src/data/validate_manifest.py`; it was fixed and the corrected run passed.

The same validator code was executed in a local offline harness:
- manifest validation: passed
- synthetic future-availability rejection test: passed
- pytest: 2 passed

A direct repository clone from the execution container was attempted for an end-to-end repository test, but the environment could not resolve github.com. This is logged as an environment/network limitation, not a code failure.

## Acquisition gate
A reproducible public-P0 acquisition workflow is now wired for the official NSE Indices NIFTY 50 historical OHLC endpoint. The workflow is triggered once by a `[acquire-p0]` commit marker, validates the resulting dataset, freezes its SHA-256 manifest, and commits the canonical cache to this branch. The cached data will then be reused rather than downloaded on every forecast run.

The remaining P0 data families—NIFTY Bank, India VIX, full cash/F&O history, corporate actions, participant flows and authorized intraday/options data—remain separate gates.

Official NIFTY 50 acquisition was attempted four times from GitHub Actions (runs 40, 43, 49 and 51). Each reached the NIFTY Indices application endpoint but received HTML with HTTP 200 instead of the expected JSON payload. Browser-profiled/cloudscraper session warm-up did not change this behavior. The retry loop is now stopped; see [issue #6](https://github.com/vishnuvcr/Timesfm-trading/issues/6).

Next gate:
Probe the distinct official NSE `/api/historicalOR/indicesHistory` route. If both historical and current windows succeed, promote it to the primary NIFTY 50 acquisition path and generate the frozen P0 manifest. The previously blocked NSE Indices backend remains disabled for acquisition.
1. schema conformance,
2. PIT leakage tests,
3. calendar/session tests,
4. corporate-action discontinuity tests,
5. derivative contract lifecycle tests,
6. option quote integrity tests.

Phase 3 engineering is already bootstrapped and its unit/statistics CI is green. The Phase 3 statistical forecast gate now waits only for the first frozen, point-in-time P0 dataset.


## Canonical schema layer added

Phase 2 now defines canonical schemas and invariant checks for equity bars, option quotes, derivative contracts and corporate actions. These checks explicitly reject impossible OHLC, negative volume/OI, crossed quotes, post-expiry quotes, invalid contract chronology and corporate-action dates that precede the announcement timestamp.


Final acquisition retry recorded after correcting the public-P0 acquisition job dependency step.
