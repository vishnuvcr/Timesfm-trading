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

## Frozen BTST execution marker — 2026-09-21

Running the predeclared close-to-next-open BTST matrix on the validated ten-stock universe with timestamp-safe global features, corporate-action exclusions, delivery/STT/DP costs, and fixed four-fold development/holdout rules.


## Rerun marker after implementation fix — 2026-09-21

The first execution failed only in the global-covariate breadth lookup. The research protocol, data source, dates, costs and promotion rules remain unchanged; rerunning the same frozen matrix after correcting the stock-level breadth reference.


## Corrected execution marker — 2026-09-21

Run the same frozen BTST matrix after the breadth-index implementation fix.


## Covariate-contract correction marker — 2026-09-21

Before rerun, the global covariate builder was corrected to emit TimesFM 3.0's documented (covariates, context) orientation. The experiment matrix, dates, costs, universe and promotion rules remain unchanged.


## Final corrected BTST execution marker — 2026-09-21

Running the same frozen BTST matrix after fixing per-symbol covariate access and enforcing the documented TimesFM 3.0 covariate shape contract.


## Corrected global-only execution marker — 2026-09-21

The previous canonical run's univariate cell is retained as valid. The global-covariate cell is being rerun separately with TimesFM 3.0 covariates enabled through the documented non-univariate path.
