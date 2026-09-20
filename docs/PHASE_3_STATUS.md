# Phase 3 status

Updated: 2026-09-20 IST

## Status
Engineering bootstrap only. Statistical forecast gate has not started.

## Implemented
- official TimesFM 3.0 PyTorch checkpoint pinned in the research environment;
- thin adapter around Google's TimesFM3Evaluator;
- multivariate target support;
- past-only covariate path;
- nine quantile outputs;
- forecast-record schema with model/checkpoint/data-vintage provenance;
- manual GitHub Actions smoke-test workflow.

## Experimental gate remains blocked
The real forecast experiment cannot be declared valid until Phase 2 supplies a frozen, point-in-time P0 dataset and the Phase 2 leakage, calendar, contract and option-integrity tests pass.

## Planned forecast matrix

### Horizon families
- scalping: 1, 3, 5, 10 intraday bars
- intraday: 15, 30, 60 minutes / session-relative horizons
- BTST: next open, next close, two-session horizon
- swing: 2, 5, 10, 20 trading sessions
- options: underlying forecast horizon matched to contract DTE buckets

### Input families
A. univariate target only
B. multivariate targets
C. multivariate + past-only covariates
D. multivariate + causally available future covariates

The four input families will be evaluated on identical forecast origins and frozen data.

### Primary metrics
- MAE/RMSE vs persistence
- directional excess vs base rate
- rank IC
- quantile coverage and calibration
- Diebold-Mariano versus persistence
- economic value after the frozen cost model

No strategy is promoted from Phase 3 on raw forecast accuracy alone.


## Statistical infrastructure added

The phase now contains deterministic NumPy-only implementations for:
- MAE/RMSE;
- base-rate-honest directional excess accuracy;
- cross-sectional rank IC;
- pinball loss and interval coverage;
- Newey-West variance and one-sided Diebold-Mariano statistic;
- moving/block bootstrap confidence intervals;
- Benjamini-Hochberg FDR adjustment.

These are reusable research primitives, not results. The workflow runs their unit tests before the model smoke test.


## CI verification history

Pull-request CI run 21 failed on an incorrect MAE fixture expectation; corrected to 0.5. Pull-request CI run 25 then exposed an incorrect RMSE fixture expectation; corrected to sqrt(1.25/3). A third CI run is expected from the latest commit before this phase can be called green.
