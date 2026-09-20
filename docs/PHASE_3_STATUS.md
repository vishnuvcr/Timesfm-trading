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
An explicitly non-promotional P1 bootstrap lane has been added. Because the official NIFTY Indices application endpoint returns HTML to GitHub Actions runners, the bootstrap uses a fixed secondary Google Finance-derived NIFTY 50 snapshot identified by upstream commit/blob SHA. The input is cached in GitHub Actions but not redistributed into this repository because the upstream repository has no explicit license file. It exercises the end-to-end TimesFM 3.0 forecasting, quantile and metric pipeline. It cannot promote a trading result because it is not the frozen primary price/OHLC P0 dataset.

## P1 result — pipeline validation only
Recorded in [P1 bootstrap result](P1_BOOTSTRAP_RESULT.md) and `results/p1_bootstrap_timesfm3.json`.

Observed on the secondary snapshot: log-level MAE 0.01310 vs persistence 0.01517 (-13.63%), RMSE 0.01649 vs 0.01955 (-15.66%), five-day return MAE 0.01849 vs 0.02129 (-13.18%). Directional accuracy was 70.0% versus a 75.0% positive-return base rate, so directional excess was -5.0 percentage points. q10–q90 coverage was 78.75%. An exploratory lag-4 HAC paired-loss test gave t = -2.10, one-sided p ≈ 0.018; moving-block bootstrap (block 5) 95% CI [-0.00416, -0.00029]. These are secondary-data exploratory statistics, not the primary P0 gate.

## P1 multivariate/covariate ablation
A secondary-data ablation is now queued to compare univariate NIFTY 50, native five-series multivariate, and NIFTY 50 plus four past-only stock covariates on identical origins. This directly tests H2/H3 without weakening the P0 primary-data gate.

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
