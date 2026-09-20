# Phase 3 status

Updated: 2026-09-20 IST

## Scope confirmation
TimesFM 3.0 is the primary model for the full project. Phase 3 results are restricted to non-commercial research/evaluation and may feed simulated strategy research, but no broker execution or commercial decision-making is permitted.

## Status
Engineering bootstrap plus exploratory stock forecast gate complete. The primary/PIT statistical gate remains blocked because the official hosted-runner NSE route is still unavailable and the 30-name panel is explicitly bootstrap-only.

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

## 2026-09-20 — individual-stock exploratory result
The repaired 30-stock TimesFM 3.0 bootstrap completed successfully in workflow run `35522976491`; artifact `10608372793` was uploaded and the per-stock results are stored in `results/p1_individual_stock_bootstrap.csv` and `results/p1_individual_stock_bootstrap_summary.json`.

Configuration: fixed 30-name bootstrap, adjusted close, context 128, 5-session horizon, 40 recent chronological origins per stock.

Observed aggregate results:
- mean log MAE: 0.018675 TimesFM vs 0.017629 persistence;
- mean log RMSE: 0.027242 vs 0.025726;
- only 3/30 stocks improved MAE and 3/30 improved RMSE;
- mean five-session directional accuracy 50.83% versus mean positive-return base rate 39.75%, with 25/30 stocks showing positive stock-level directional excess;
- only 5/30 improved five-session return MAE;
- mean q10–q90 interval-width Spearman correlation with subsequent absolute five-session movement was -0.121, with 9 positive and 21 negative stock-level correlations.

A descriptive cluster bootstrap over the 30 stock-level metrics gave 95% intervals showing positive TimesFM-minus-persistence error differences for MAE/RMSE/return-MAE and a negative interval-width/movement correlation. These resamples do not replace origin-level inference and do not establish a tradable edge.

Interpretation: the stock sample does not support TimesFM 3.0 as a better point-forecast model than persistence on average. The directional excess is an exploratory lead only; it has not been benchmarked against an independently specified stock-selection signal, multiple-testing corrected, walk-forward validated across historical folds, or cost-tested. The uncertainty/interval-width hypothesis from the earlier secondary NIFTY sample does not reproduce here and is therefore not promoted as a stock-sizing signal.

Known data-quality flag: `TATAMOTORS.csv` in the adjusted bootstrap ends on 2025-10-23 while most names extend to 2026-09-18. This is logged as a stock-source/identifier continuity issue to resolve before final PIT evidence.

No strategy is promoted from this exploratory run.


## 2026-09-20 — four-fold stock robustness extension

A separate exploratory track is now defined to run four chronological folds across each stock's available adjusted-price history, with 40 origins per fold (160 origins per stock where history permits). This is intentionally outside the frozen primary matrix and cannot promote a result by itself.

The track is triggered by a push marker `[stock-p1-multifold]`, uses the same TimesFM 3.0 checkpoint/context/horizon and the same persistence baseline, and stores fold-level and stock-level results as a workflow artifact. The purpose is to test whether the recent-40-origin stock result survives earlier market periods rather than becoming a recency artifact.



## 2026-09-20 — four-fold stock robustness result

The separate P1.1 multi-fold workflow completed successfully as run 35523375234; artifact 10608933929 was uploaded. Aggregate and per-stock summaries are stored in results/p1_individual_stock_multifold_summary.json and results/p1_individual_stock_multifold_per_stock.csv.

Design: 30 stocks × 4 chronological folds × 40 origins per fold = 4,800 stock-level forecast origins, using the same TimesFM 3.0 checkpoint, 128-session context, 5-session horizon and persistence baseline.

Aggregate result:
- mean stock log-MAE difference (TimesFM minus persistence): +0.001144;
- mean stock log-RMSE difference: +0.001470;
- mean five-session return-MAE difference: +0.001885;
- mean directional excess over each stock's fold-specific positive-return base rate: -2.90 percentage points;
- only 13/30 stocks had non-negative mean directional excess;
- no stock had a negative mean MAE difference across its four folds;
- mean interval-width/absolute-movement Spearman rho: +0.091.

Fold-level directional excess was negative in folds 1, 2 and 4 and only slightly positive in fold 3. Thus the +11.1 percentage-point directional excess seen in the recent-40-origin bootstrap does not persist across broader historical folds.

Interpretation: the chronological robustness test materially weakens the recent stock-direction finding. TimesFM 3.0 did not beat persistence on stock point-error metrics, and its directional excess became negative when history was broadened. The interval-width relationship is mildly positive in this multi-fold sample, but the effect is small and not yet calibrated or economically validated. No stock strategy is promoted.

