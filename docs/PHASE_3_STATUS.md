# Phase 3 status

Updated: 2026-09-20 IST

## Scope confirmation
TimesFM 3.0 is the primary model for the full project. Phase 3 results are restricted to non-commercial research/evaluation and may feed simulated strategy research, but no broker execution or commercial decision-making is permitted.

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

## P1 exploratory bootstrap
An explicitly non-promotional P1 bootstrap lane has been added. It uses the public NIFTY 50 total-return series only to exercise the end-to-end TimesFM 3.0 forecasting, quantile and metric pipeline. It cannot promote a trading result because it is not the frozen primary price/OHLC P0 dataset.

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

No strategy is promoted from Phase 3 on raw forecast accuracy alone. P1 bootstrap output is retained as pipeline validation, not as a primary empirical finding.


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

Pull-request CI run 21 failed on an incorrect MAE fixture expectation; corrected to 0.5. Pull-request CI run 25 then exposed an incorrect RMSE fixture expectation; corrected to sqrt(1.25/3). CI verification is now green: pull-request run 29 (`35517423864`) completed successfully; the `unit-tests` job passed and the model-smoke job was skipped because it is manual-only. The two prior fixture failures were corrected and the statistical/adapter unit suite now passes.
