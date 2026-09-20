# Provisional research conclusion

Updated: 2026-09-20 IST

## Current evidence

The first TimesFM 3.0 exploratory NIFTY 50 run on secondary data found lower five-session point forecast error than persistence:

- log MAE: 0.01310 versus 0.01517;
- log RMSE: 0.01649 versus 0.01955;
- five-session return MAE: 0.01849 versus 0.02129.

However, directional accuracy was 70.0% versus a 75.0% positive-return base rate. The evidence therefore does not support treating TimesFM 3.0's raw direction as the primary alpha signal.

Forecast uncertainty was more promising as a risk/magnitude variable. Five-session q10-q90 interval width had Spearman correlation approximately 0.350 with subsequent absolute five-session movement. The highest-width quartile had about 2.32 times the mean absolute movement of the lowest-width quartile in the secondary sample.

The multivariate ablation produced mixed evidence. Native five-series multivariate forecasting raised directional accuracy from 70.0% to 72.5% but increased MAE by about 0.51% and RMSE by about 4.21%. Four past-only stock covariates produced no recorded metric change versus univariate in that run.

## Provisional strategy hypothesis

The most defensible current research design is therefore an **uncertainty-conditioned exposure overlay**, not a standalone TimesFM directional strategy.

Conceptually:

1. Use TimesFM 3.0 median forecasts and an independent baseline signal for direction; do not assume TimesFM direction is alpha.
2. Convert the calibrated q10-q90 width into an uncertainty measure.
3. Reduce position size as forecast uncertainty rises and increase size only within a hard exposure cap when uncertainty is lower.
4. Require the external directional signal to exceed a conservative all-in round-trip cost hurdle before opening a simulated position.
5. Apply regime, liquidity, event and participation constraints from Phase 6.
6. Evaluate the overlay against the same directional baseline without TimesFM uncertainty.

This is the existing Phase 4 volatility-targeted/uncertainty-sizing hypothesis made concrete. It is not a validated trading strategy.

## Promotion conditions

The hypothesis can only be promoted after:

- authorized point-in-time NSE data are frozen and validated;
- the full TimesFM 3.0 horizon/target/input matrix is run;
- uncertainty calibration is checked out-of-sample;
- the overlay survives walk-forward validation;
- current brokerage, STT, exchange/SEBI charges, GST/stamp duty, spread/slippage and participation assumptions are applied;
- multiple-testing/FDR controls are passed;
- performance survives regime and stress-cost breakdowns.

## Present conclusion

The current research supports using TimesFM 3.0 primarily as a **forecast-distribution and risk-information model**, not as a proven directional alpha generator.

The project has reached the end of the planned engineering stack, but it should not claim a validated profitable NSE strategy until the P0 data gate is cleared and the remaining empirical phases are run.
