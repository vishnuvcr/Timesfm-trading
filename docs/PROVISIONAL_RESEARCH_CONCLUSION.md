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


## Multi-fold stock robustness update — 2026-09-20

The four-fold extension used 30 stocks × 4 chronological folds × 40 origins per fold (4,800 origins total), retaining the same TimesFM 3.0 configuration and persistence comparator.

The result is consistently unfavorable for point forecasting: every stock's four-fold mean MAE difference was positive (TimesFM worse than persistence), with mean MAE difference +0.001144 and mean RMSE difference +0.001470. Mean five-session return-MAE difference was +0.001885.

The recent-window directional result also failed the robustness test. Mean directional excess was -2.90 percentage points, with only 13/30 stocks non-negative across the four folds. Fold-level directional excess was negative in three of four folds.

The interval-width/absolute-movement relationship was mildly positive in the multi-fold sample (mean Spearman rho +0.091), but this is far smaller and qualitatively different from the earlier secondary NIFTY observation (~+0.350). It is not calibrated, not cost-tested, and not sufficient to support a stock-sizing strategy.

### Current inference

The evidence now supports a **negative result for standalone TimesFM 3.0 stock forecasting against persistence on this bootstrap**. The recent directional excess should be treated as a recency-window artifact until independently reproduced.

The remaining scientific opportunity is not to keep searching for a TimesFM-only direction rule. It is to test whether TimesFM adds incremental information to an independently specified stock-selection or market-structure signal after PIT universe construction, corporate-action reconciliation, multiple-testing correction and full economic costs.

No stock strategy is currently validated.


## Daily individual-stock strategy gate closure — 2026-09-20

The Phase 4 daily stock strategy lane is now closed after two sequential tests.

First, the simple stock-selection test compared 20-session cross-sectional momentum, TimesFM 5-session forecast ranking, a 50/50 hybrid and a momentum-gated TimesFM variant. TimesFM had lower mean rank IC than momentum and produced more negative net returns under the tested cost scenarios.

Second, a nested regime-conditioned residual test used only prior-fold information to define a low-breadth regime and compared the TimesFM-minus-momentum residual with the same momentum control. The residual lost to momentum at every one-way cost scenario from 0.125% to 0.50%.

The combined conclusion is now stronger than the earlier provisional hypothesis: **no tested daily individual-stock TimesFM mechanism has demonstrated incremental economic value over the declared stock-selection baseline on the current research panel.**

The repository therefore closes the current daily stock overlay gate rather than generating more thresholds or simple combinations. Future stock work requires a material protocol amendment, new authorized/PIT-clean data, or a genuinely different economic mechanism such as event-conditioned or stock-vs-sector residual forecasting.

See [Individual-stock TimesFM gate conclusion](INDIVIDUAL_STOCK_TIMESFM_GATE_CONCLUSION.md).
