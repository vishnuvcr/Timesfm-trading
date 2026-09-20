# Frozen experiment matrix — TimesFM 3.0 on NSE

## Primary research question

Does TimesFM 3.0 add statistically and economically useful information to an NSE trading pipeline after realistic execution costs?

## Aims

1. Quantify TimesFM 3.0 forecast skill by horizon and target.
2. Determine whether native multivariate inputs and causal covariates add incremental value.
3. Measure uncertainty calibration and volatility information.
4. Translate only surviving information into cash, BTST, swing and options strategies.
5. Establish a reproducible cost-aware promotion gate.

## Primary endpoints

### Forecast
- MAE
- RMSE
- pinball loss across q10–q90
- weighted interval score
- q10–q90 empirical coverage
- directional excess over contemporaneous base rate
- rank IC for cross-sectional forecasts
- Diebold-Mariano versus persistence

### Trading
- net expectancy per trade
- net Sharpe
- maximum drawdown
- turnover
- cost per traded rupee
- break-even slippage
- worst decile / tail loss
- fold-by-fold stability

## Fixed target families

1. log price
2. log return
3. realized range/volatility
4. option-implied volatility / skew targets where data permit

No additional target family is promoted into the primary matrix without a logged protocol amendment.

## Fixed input families

A. univariate target only  
B. native multivariate targets  
C. multivariate + past-only covariates  
D. multivariate + future-known/forecastable covariates

Future covariates are allowed only when their future values are genuinely known at decision time or are themselves separately forecast without leakage.

## Fixed horizon families

### Scalping
1, 3, 5, 10 bars using validated 1-minute/5-minute data.

### Intraday
15, 30, 60 minutes using session-relative horizons.

### BTST
next open, next close and two-session return.

### Swing
2, 5, 10 and 20 trading sessions.

### Options
1-day and 5-day underlying/IV horizons plus expiry-relative buckets.

## Primary instruments

Phase 3 starts with liquid index targets:
- NIFTY 50
- NIFTY Bank
- India VIX as a volatility covariate/target where appropriate

The equity cross-section expands only after the index-level gate and point-in-time membership dataset are validated.

## Baselines

Every primary cell includes:
- persistence / random walk
- drift
- simple moving-average or EMA baseline
- AR(1) where statistically appropriate
- one lightweight supervised baseline selected before looking at test results

## Walk-forward design

- training/calibration period strictly precedes validation;
- test origins are chronologically ordered;
- no parameter selection on final test windows;
- overlapping horizons use overlap-aware loss comparison;
- all experiments use the same frozen origin calendar within a comparison block.

## Multiple testing

Track every experiment configuration. Use Benjamini-Hochberg FDR for families of instrument-level tests. Use Deflated Sharpe or a comparable selection-bias correction when strategy search becomes broad.

## Primary promotion gate

A forecast component enters strategy research only when:
1. it improves a pre-declared primary forecast metric against persistence on untouched test data;
2. any directional advantage exceeds the contemporaneous base rate;
3. quantile calibration is acceptable and stable;
4. the result is not concentrated in one fold/regime without a documented mechanism.

A trading strategy enters paper research only when it:
1. is net positive under the frozen realistic cost model;
2. survives cost and slippage stress;
3. is robust across multiple walk-forward folds;
4. has no material look-ahead/survivorship error;
5. has operationally acceptable turnover, liquidity and drawdown.

## Search-space stop rule

The primary matrix is frozen. Exploratory variants may be run only in a separately labeled exploratory track and cannot be promoted without a new pre-registration/holdout.
