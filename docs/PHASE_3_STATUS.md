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

Observed on the secondary snapshot: log-level MAE 0.01310 vs persistence 0.01517 (-13.63%), RMSE 0.01649 vs 0.01955 (-15.66%), five-day return MAE 0.01849 vs 0.02129 (-13.18%). Directional accuracy was 70.0% versus a 75.0% positive-return base rate, so directional excess was -5.0 percentage points. q10–q90 coverage was 78.75%. An exploratory lag-4 HAC paired-loss test gave t = -2.10, one-sided p ≈ 0.018; moving-block bootstrap (block 5) 95% CI [-0.00416, -0.00029]. The five-day q10–q90 width correlated with subsequent absolute movement at Spearman rho ≈ 0.350; the highest-width quartile had about 2.32× the mean absolute movement of the lowest-width quartile. These are secondary-data exploratory statistics, not the primary P0 gate.

## P1 multivariate/covariate ablation
A secondary-data ablation is now queued to compare univariate NIFTY 50, native five-series multivariate, and NIFTY 50 plus four past-only stock covariates on identical origins. This directly tests H2/H3 without weakening the P0 primary-data gate.

## P1 multivariate/covariate ablation result
Recorded in [P1 multivariate ablation](P1_MULTIVARIATE_ABLATION.md) and `results/p1_multivariate_ablation.json`.

On 4,015 aligned secondary rows (2004-08-25 to 2021-01-25), 80 identical origins, context 128 and 5-session horizon: univariate log-level MAE/RMSE were 0.01849/0.02166 with 70.0% directional accuracy; native five-series multivariate was 0.01858/0.02257 with 72.5% directional accuracy; NIFTY 50 plus four past-only covariates was identical to the univariate metrics in this run. Thus multivariate conditioning changed the directional figure in this exploratory sample but slightly worsened point-error metrics; past-only covariates produced no recorded change. These are secondary-data observations only and not strategy-promotion evidence.

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


## Individual-stock bootstrap engineering
A 30-stock exploratory TimesFM 3.0 lane is now wired to consume the Phase 2 TejHQ adjusted-price cache directly from the `phase-2-data` branch. It uses adjusted close, a 128-session context, a five-session horizon and 40 chronological origins per stock. The lane reports per-stock MAE/RMSE versus persistence, five-session return MAE, base-rate-honest direction and interval-width/risk correlation.

The first execution attempt failed before forecasting because of a Python string-literal syntax error in the new stock script. The error was corrected and a syntax-check step was added before the model run. The rerun is the active exploratory gate. No strategy promotion is attached to this job.
