# Final research manuscript outline

## Title
TimesFM 3.0 for Point-in-Time NSE Forecasting and Cost-Aware Trading Strategy Research

## Abstract
- Background and motivation.
- Research questions.
- Data sources and point-in-time controls.
- TimesFM 3.0 configurations and baselines.
- Primary forecast results.
- Economic simulation results after costs.
- Principal limitations.
- Conclusion.

## 1. Introduction
- NSE market microstructure and forecasting problem.
- Why foundation time-series models need finance-specific validation.
- Directional base-rate trap.
- Importance of uncertainty, regime and execution costs.
- Study contribution.

## 2. Research Questions and Hypotheses
- H1 forecast information.
- H2 multivariate/covariate value.
- H3 uncertainty/volatility information.
- H4 robustness across regimes and costs.
- H5 2.5 versus 3.0.
- H6 simulated strategy inference without deployment claims.

## 3. Literature Review
- Foundation time-series models.
- Financial time-series forecasting.
- Random-walk and technical/statistical baselines.
- Forecast calibration and interval scoring.
- Regime dependence.
- Market microstructure and transaction-cost modeling.
- Option-implied versus statistical forecasts.
- Data leakage and point-in-time research.

## 4. Data and Provenance
- NSE cash/index/futures/options.
- India VIX.
- FII/FPI/DII.
- Global markets, GIFT NIFTY, USDINR, rates, crude and gold.
- Corporate actions.
- Timestamped news/events.
- Source hierarchy, licensing and revisions.
- PIT availability and vintage rules.

## 5. Methodology
- Forecast origins.
- Context/horizon matrix.
- Univariate, multivariate and causal covariates.
- Targets: price, return, range, volatility and option-implied movement.
- Baselines.
- Quantile calibration.
- Statistical tests: MAE/RMSE, rank IC, directional excess, pinball, coverage, DM, HAC and block bootstrap.
- Multiple-testing control.
- Walk-forward and nested tuning.
- Cost model and slippage scenarios.
- Simulation-only governance.

## 6. Results
### 6.1 Forecast performance
Tables for every target/horizon/model family.

### 6.2 Directional information
Base-rate-adjusted direction and rank IC.

### 6.3 Forecast uncertainty
Calibration, coverage and interval-width versus realized movement.

### 6.4 Multivariate and covariate ablations
Identical-origin comparisons.

### 6.5 Regime dependence
Trend/range, India VIX, stress, expiry and event conditions.

### 6.6 Strategy simulations
Scalping, intraday, BTST, swing and options, with gross/net performance.

### 6.7 Cost sensitivity
Brokerage, STT, exchange/SEBI charges, GST, stamp duty, spread, slippage, participation, financing and capacity.

## 7. Inference
- Confidence intervals.
- Statistical significance versus economic significance.
- FDR-adjusted claims.
- Stability across years and regimes.

## 8. Discussion
- What TimesFM 3.0 contributes.
- Where it does not add information.
- Uncertainty as risk input versus directional alpha.
- Market-implied information in options.
- Execution constraints.
- Comparison with literature.

## 9. Strengths
- PIT design.
- Reproducibility.
- Explicit costs.
- Multiple-testing discipline.
- Separate evidence grades.
- Non-executing governance.

## 10. Limitations
- Data licensing/access constraints.
- Secondary-data bootstrap limitations.
- Historical regime coverage.
- Model/version drift.
- Fill uncertainty.
- Capacity.
- Potential selection effects.

## 11. Conclusion
State only claims supported by the frozen P0 evidence and statistical gates.

## 12. Future Research
- Authorized current NSE data.
- Longer intraday histories.
- Cross-market causal covariates.
- Option surface residuals.
- Regime-specific recalibration.
- Model adaptation versus zero-shot.
- Capacity and impact modeling.

## Figures
1. Research pipeline.
2. Data provenance/PIT timeline.
3. Forecast error by horizon.
4. Directional excess by horizon.
5. Quantile coverage/calibration.
6. Interval width versus realized movement.
7. Regime performance.
8. Net P&L after costs.
9. Cost sensitivity.
10. Walk-forward equity/underwater curves.

## Tables
1. Dataset provenance.
2. Model/configuration matrix.
3. Forecast metrics.
4. Calibration metrics.
5. Statistical tests.
6. Regime breakdown.
7. Strategy specifications.
8. Gross versus net economics.
9. Cost sensitivity.
10. Ablation summary.

## Appendices
- Hyperparameters.
- Fee manifests.
- Data schemas.
- Full statistical output.
- FDR tables.
- Failure/error log.
- Model/license details.
- Reproduction commands.

## Supplements
- Frozen manifests.
- Forecast panels.
- Simulated execution ledgers.
- Source citations.
- Extended sensitivity analyses.
