# Scientific methodology

## Study design
Freeze dated datasets first. Generate forecasts using only information available by each forecast origin, then evaluate only against future observations.

## Primary unit
Forecast origin t × instrument/contract × horizon H.

## Targets
- log price
- simple/log return
- realized range or volatility
- option-implied quantities only when constructed causally

## Validation
Rolling or expanding walk-forward splits. Tuning data strictly precede test windows.

## Forecast tests
- MAE/RMSE vs persistence/drift
- directional accuracy vs contemporaneous base rate
- rank IC for cross-sectional ranking
- Diebold-Mariano forecast-loss comparison with overlap-aware handling
- quantile coverage/calibration
- block-bootstrap confidence intervals

## Trading tests
Signal timestamp → decision delay → order model → fill → costs → position → exit. No same-bar fills unless the trading rule genuinely permits them.

## Statistical controls
Predeclare primary metrics; track every tested configuration; use Benjamini-Hochberg FDR for multiplicity; use Deflated Sharpe and reality-check style robustness when the search space is broad.

## Regimes
At minimum: India VIX bands, trend/range, stress periods, expiry vs non-expiry, time of day, event vs non-event.

## Execution stress
Test wider spreads, higher volatility impact, lower fill probability, participation caps, missing bars, inference delays and broker/API failures.

## Promotion gate
Paper eligibility requires positive net results on untouched test windows, no material leakage, cost/slippage robustness, stable evidence across more than one period/regime, and pre-defined monitoring thresholds.
