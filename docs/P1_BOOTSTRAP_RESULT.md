# Phase 3 P1 bootstrap result

## Result

TimesFM 3.0 completed an 80-origin, 5-day-horizon exploratory forecast run on a fixed secondary NIFTY 50 OHLC snapshot.

| Metric | TimesFM 3.0 | Persistence | P1 observation |
|---|---:|---:|---|
| Log-level MAE | 0.01310 | 0.01517 | 13.63% lower for 3.0 |
| Log-level RMSE | 0.01649 | 0.01955 | 15.66% lower for 3.0 |
| Five-day return MAE | 0.01849 | 0.02129 | 13.18% lower for 3.0 |
| Directional accuracy | 70.0% | Base rate 75.0% | -5.0 percentage points |
| q10–q90 coverage | 78.75% | nominal 80% | slightly under nominal |

An exploratory Newey-West-adjusted paired loss test on 80 origin-level five-day forecast blocks gave a mean loss difference of -0.00207, lag-4 HAC t = -2.10 and one-sided p ≈ 0.018. A moving-block bootstrap with block length 5 gave a 95% interval of approximately [-0.00416, -0.00029]. These inferential numbers are exploratory and were not part of the pre-registered primary P0 gate.

## Interpretation

The result supports a narrow research observation: in this secondary historical snapshot, TimesFM 3.0 produced lower point forecast error than persistence for the tested five-day horizon. It does not support a directional-alpha conclusion; the directional forecast was below the contemporaneous positive-return base rate.

## Evidence status

- Evidence grade: C / exploratory secondary-data result.
- Not primary NSE P0 evidence.
- Not a trading strategy result.
- Not used to promote a strategy.
- Not evidence of live/deployment suitability.

Primary Phase 3 remains blocked until authorized/official point-in-time NSE P0 data are available.