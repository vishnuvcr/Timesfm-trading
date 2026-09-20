# Phase 4B BTST / overnight status

Updated: 2026-09-21 IST

## Status

BTST protocol frozen. Source and feature preparation is the current gate.

## Fixed stock universe
RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, SBIN, ITC, BHARTIARTL, LT, AXISBANK.

## Minute source
voletiramu/nse-fno-1min-data v1.0.0
SHA-256: 20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2

## External global source
Hareeshkesavan/Stock-Market-Dataset
upstream main commit frozen as aa60b746f089c3f54df6760bf021708c2d3ce1e8
Raw files are not copied into the repository because the upstream repository does not expose a machine-readable license file. The workflow uses a fixed commit plus GitHub Actions cache and records source hashes/metadata.

Primary global files:
- Nifty 50 Historical Data.csv
- Nikkei 225 Historical Data.csv
- Hang Seng Historical Data.csv
- S&P 500 Historical Data.csv
- DAX Historical Data.csv
- Brent Oil Futures Historical Data.csv
- Gold Futures Historical Data.csv
- US Dollar Index Historical Data.csv

Secondary institutional-flow file:
- FII and DII.xlsx

## Current gate
Validate date parsing, common-session alignment, timestamp-safe feature availability, corporate-action exclusion, next-open construction, capacity and cost calculations before TimesFM inference.

## Experiment state
No BTST strategy result exists yet. No holdout has been opened.