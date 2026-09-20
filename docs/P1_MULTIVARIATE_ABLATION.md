# Phase 3 P1 multivariate/covariate ablation

## Design

The same TimesFM 3.0 model, 80 forecast origins, context 128 and five-session horizon were used across three input conditions:

1. NIFTY 50 univariate.
2. Native five-series multivariate: NIFTY 50, RELIANCE, TCS, HDFCBANK and HINDUNILVR.
3. NIFTY 50 with four past-only stock covariates.

The aligned secondary dataset contained 4,015 common trading dates from 2004-08-25 through 2021-01-25.

## Results

| Condition | Log MAE | Log RMSE | Directional accuracy |
|---|---:|---:|---:|
| Univariate | 0.018486 | 0.021659 | 70.0% |
| Native multivariate, 5 series | 0.018580 | 0.022571 | 72.5% |
| Past-only covariates | 0.018486 | 0.021659 | 70.0% |

Relative to univariate, the native multivariate condition had about 0.51% higher MAE and 4.21% higher RMSE in this exploratory sample, while directional accuracy was 2.5 percentage points higher. The past-only covariate condition produced no recorded metric change in this run.

## Interpretation

This result does not establish that multivariate TimesFM is inferior or superior in general. It is a single secondary-data ablation with 80 origins and one five-session horizon. It shows that adding cross-series information can alter the directional forecast without necessarily improving point forecast error.

The exact equality of the past-only-covariate metrics in this run should be treated as an empirical observation, not evidence that the covariates are ignored; a larger P0 experiment is required.

## Evidence status

- Grade: C, exploratory secondary-data result.
- Primary NSE P0 gate: not satisfied.
- Strategy promotion: not permitted.
- Commercial/deployment use: not permitted.

The full Phase 3 forecast gate remains blocked until authorized/official point-in-time NSE P0 data are available.
