# Provisional research conclusion

Updated: 2026-09-20 IST

## Current evidence

The first TimesFM 3.0 exploratory NIFTY 50 run on secondary data found lower five-session point forecast error than persistence:

- log MAE: 0.01310 versus 0.01517;
- log RMSE: 0.01649 versus 0.01955;
- five-session return MAE: 0.01849 versus 0.02129.

However, directional accuracy was 70.0% versus a 75.0% positive-return base rate. The evidence therefore does not support treating TimesFM 3.0's raw direction as the primary alpha signal.

Forecast uncertainty was more promising as a risk/magnitude variable in the earlier secondary NIFTY sample, but that relationship did not reproduce in the 30-stock bootstrap. Five-session q10-q90 interval width had Spearman correlation approximately 0.350 with subsequent absolute five-session movement. The highest-width quartile had about 2.32 times the mean absolute movement of the lowest-width quartile in the secondary sample.

The multivariate ablation produced mixed evidence. Native five-series multivariate forecasting raised directional accuracy from 70.0% to 72.5% but increased MAE by about 0.51% and RMSE by about 4.21%. Four past-only stock covariates produced no recorded metric change versus univariate in that run.

## Provisional strategy hypothesis

The most defensible current research position is now more cautious: **do not promote a TimesFM-only directional or uncertainty-sizing stock strategy yet**. The stock bootstrap must first establish whether any incremental information survives broader chronological folds and an independent stock-selection baseline.

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


## Individual-stock bootstrap update — 2026-09-20

The repaired 30-stock exploratory TimesFM 3.0 run used adjusted close, context 128, horizon 5 and 40 recent chronological origins per stock. Mean log MAE was 0.018675 versus 0.017629 for persistence; mean log RMSE was 0.027242 versus 0.025726. Only 3/30 stocks improved MAE and 3/30 improved RMSE.

Directional accuracy was 50.83% against a 39.75% mean positive-return base rate, and 25/30 stocks had positive stock-level directional excess. This is potentially interesting, but it is not evidence of a tradable edge: the stock baseline is persistence rather than an independently frozen selection signal, the sample uses only recent origins, the universe is a fixed bootstrap panel, multiple testing is not yet corrected at the strategy level, and no execution-cost hurdle has been applied.

The q10–q90 interval-width/absolute-movement relationship averaged Spearman rho -0.121 across stocks, versus approximately +0.350 in the earlier secondary NIFTY sample. The sign reversal means the current evidence does not support promoting uncertainty width as a portable stock-sizing signal.

## Revised research hypothesis

The stock pathway should now test whether TimesFM provides **incremental conditional information** to an independently specified cross-sectional or technical signal, rather than assuming that TimesFM itself supplies the direction.

The next validation should:
1. freeze a PIT universe with identifier/corporate-action continuity;
2. run multiple chronological stock folds rather than only the most recent 40 origins;
3. compare against a predeclared stock-selection baseline;
4. test cross-sectional rank IC and residual information;
5. apply FDR/selection-bias controls;
6. pass the existing brokerage, statutory-charge, spread/slippage/impact and participation-cost model before strategy promotion.

No stock strategy is validated by the present bootstrap.
