# Phase 4 intraday/BTST/scalping data gate

Updated: 2026-09-20 IST

## Status

**Data-integrity validation active. No intraday/BTST/scalping strategy is being tested until the minute source passes this gate.**

## Source

Candidate source: `xxparthparekhxx/indian-stock-market-minute-data`.

Published metadata reports:
- 1-minute intraday candles from 2022–2026;
- 2,500+ NSE stocks/indices;
- UTC timestamps;
- OHLCV + OI fields;
- MIT license;
- symbol/timestamp ordering within shards.

NSE documents the regular equity session as 09:15–15:30, with pre-open separately defined. citeturn752108search0turn752108search1

## Deep validation matrix

The gate tests:
1. schema/type consistency;
2. UTC→IST conversion;
3. regular-session membership;
4. expected 375 one-minute bars for a complete 09:15–15:29 session;
5. duplicate timestamps;
6. missing minute gaps;
7. invalid OHLC relations;
8. zero-volume prevalence;
9. non-positive prices;
10. chronological monotonicity;
11. daily OHLC aggregation;
12. close-to-close return agreement with the Phase 2 raw EOD cache;
13. timestamp coverage across early/mid/recent sample regions;
14. reproducible API query metadata.

Symbols are restricted to a fixed diagnostic set (RELIANCE, TCS, HDFCBANK, INFY, SBIN) for the gate. This is a source-integrity test, not a strategy universe selection.

## Promotion rule

The source is eligible for intraday strategy experiments only if:
- sampled complete sessions show no unexplained missing-minute/gap pattern;
- invalid OHLC is zero;
- duplicate timestamps are zero;
- zero-volume behavior is quantified and operationally handled;
- session mapping is correct;
- aggregated daily return paths are consistent with the independent EOD source within a predeclared tolerance;
- query failures and partial-result behavior are fully logged.

Passing this gate does not establish fill accuracy. Execution-quality validation remains a separate step requiring spread/impact assumptions and, where possible, trade/quote data.

## Next strategy step

After the data gate, the first intraday mechanism will be a frozen 15/30/60-minute TimesFM target matrix with VWAP/persistence controls. BTST will require a separately validated next-session open path. Scalping will require a still stricter execution gate.


## Execution marker — 2026-09-20

The deep minute-source gate is now being executed on the five fixed diagnostic symbols. No strategy computation is attached to this workflow.


## Independent release gate — started 2026-09-20

The Hugging Face-filter path is no longer the automatic source gate because its query service returned repeated 422/500/timeouts on the 10.5 GB dataset. The independent GitHub release `voletiramu/nse-fno-1min-data` is now the primary candidate for this frequency gate.

Release v1.0.0:
- 214 NSE F&O underlying stocks;
- 1-minute OHLCV;
- 2024-04-01 to 2026-04-30;
- compressed release asset SHA-256: `20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2`;
- stated source: Zerodha Kite API.

The gate will selectively extract five fixed liquid symbols and compare full-session minute bars with the cached EOD series before any strategy work.


## Reconciliation rerun — 2026-09-20

The first verified-release run proved the release artifact and produced 512 complete sessions for each of the tested symbols, but the raw daily-close comparison was contaminated by corporate-action/adjustment differences and the validator treated 15:30 endpoint rows as out-of-session.

The rerun now:
- excludes daily return pairs adjacent to recorded NSE corporate-action dates;
- accepts 15:30 as an endpoint row without treating it as an anomaly;
- counts all other out-of-session rows;
- records concrete invalid-OHLC examples;
- retains the release SHA-256 gate.
