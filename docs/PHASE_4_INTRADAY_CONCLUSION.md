# Phase 4 intraday strategy conclusion

Updated: 2026-09-20 IST

## Question

Does TimesFM 3.0 add cross-sectional information at 15/30/60-minute horizons beyond a past-only VWAP-deviation control on ten validated NSE F&O underlyings?

## Result

The frozen development gate rejected all three horizons.

Development block-signflip one-sided p-values at the 0.10% one-way slippage stress:
- 15 minutes: 0.4381
- 30 minutes: 0.3043
- 60 minutes: 0.6125

Benjamini-Hochberg q-values were 0.6125 for all three cells.

Therefore there was no development-qualified candidate and no holdout was opened.

## Forecast diagnostics

TimesFM point-error MAE was worse than the zero-return persistence benchmark at every horizon:
- 15m: 0.001586 vs 0.001444;
- 30m: 0.002461 vs 0.002047;
- 60m: 0.003968 vs 0.002981.

Directional excess was positive at 15m (+8.74 pp) and 30m (+4.35 pp), but cross-sectional rank IC was approximately zero/negative and the economic strategy gate did not survive.

## Strategy economics

At zero additional slippage:
- 15m TimesFM: -9.31%; VWAP: -10.09%;
- 30m TimesFM: -9.89%; VWAP: -11.46%;
- 60m TimesFM: -9.40%; VWAP: -9.79%.

At 0.10% extra one-way slippage:
- 15m: -34.33% TimesFM;
- 30m: -34.75%;
- 60m: -34.40%.

At 0.20% extra one-way slippage:
- 15m: -52.53%;
- 30m: -52.84%;
- 60m: -52.58%.

The VWAP control was also negative, so the experiment does not establish that the market was untradeable; it establishes that this TimesFM intraday mechanism did not meet the predeclared development criteria.

## Decision

Close the current 15/30/60-minute TimesFM-vs-VWAP intraday strategy family under the present protocol.

No additional intraday TimesFM indicators, thresholds, hybrids, horizons or stock-universe searches will be added based on this result.

The next permitted holding-period mechanism is BTST/overnight. That lane will use the validated minute source to construct next-session-open targets and will explicitly test overnight/global-market information availability before any economic strategy gate.

## Strengths and limitations

Strengths:
- ten-source-validated liquid F&O stocks;
- fixed source hash;
- fixed 15/30/60 horizons;
- no same-bar execution;
- broker auto-square-off avoided;
- dated cash-intraday costs;
- five slippage stresses;
- chronological development/holdout design;
- BH-FDR and block-aware inference.

Limitations:
- OHLCV source has no bid/ask history;
- execution friction is therefore a stress proxy;
- development sample is sparse relative to a dense intraday simulation;
- this gate tests only one technical control family (VWAP) and does not address overnight information.

## Conclusion

TimesFM 3.0 did not demonstrate incremental intraday stock-selection value under the frozen first intraday protocol. The lane is closed without holdout promotion.