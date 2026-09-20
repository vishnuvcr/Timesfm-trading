# TimesFM for NSE Trading: Individual-Stock EOD/Multiday Research Manuscript

## Abstract

This manuscript reports the completed individual-stock EOD/multiday research lane evaluating TimesFM 3.0 for NSE stock trading. The protocol separates forecast quality from economic value, uses a fixed bootstrap universe, chronological evaluation, an independent 20-session momentum control, point-in-time eligibility, realistic cash-equity cost modeling and a post-selection holdout. A 10-session cross-sectional TimesFM ranking emerged as the only exploratory candidate from the predeclared swing matrix, but failed the untouched 2023+ holdout: +3.72% at zero added slippage versus +67.97% for the fixed momentum control, deteriorating to -35.72% versus -1.12% at 0.50% one-way extra slippage. The candidate was therefore rejected. The result is a negative finding for this individual-stock mechanism, not a universal impossibility theorem for TimesFM.

## 1. Introduction

Financial forecasting performance does not automatically translate into trading value because simple baselines, turnover, transaction costs, slippage, capacity and regime dependence can dominate small forecast improvements. The research therefore uses gate-based validation rather than equating predictive accuracy with profitability.

TimesFM 3.0 is the primary research model. The research remains non-executing and subject to the project's TimesFM 3.0 pretrained-weight licensing restrictions.

## 2. Research questions

1. Does TimesFM 3.0 improve individual-stock forecast quality relative to persistence?
2. Does TimesFM 3.0 provide cross-sectional ranking information beyond a simple 20-session momentum control?
3. Does forecast uncertainty add useful sizing information?
4. Does an exploratory TimesFM stock-selection mechanism survive point-in-time validation, realistic costs and an untouched chronological holdout?

## 3. Aims and objectives

### Aim

Determine whether TimesFM 3.0 provides reproducible economic value for NSE individual-stock EOD/multiday research.

### Objectives

- evaluate multiple holding horizons;
- compare with persistence and momentum;
- avoid look-ahead and holdout tuning;
- incorporate cash-equity trading costs;
- quantify drawdown, turnover and capacity;
- document negative results and stop rules.

## 4. Data and provenance

The executable EOD lane uses a cached alternate stock source with separate corporate-action and PIT metadata. Official NSE hosted-runner historical routes were repeatedly blocked, so the alternate data source is retained as a secondary research lane rather than mislabeled exchange-primary truth.

The bootstrap universe contains 30 fixed names. PIT eligibility is evaluated at each forecast origin.

The candidate intraday source is a Hugging Face 1-minute NSE dataset reporting 1-minute candles from 2022–2026, UTC timestamps, OHLCV/OI and MIT licensing. It has passed a structural probe but has not yet passed a full execution-quality gate.

## 5. Experimental design

The frozen Phase 4B matrix tested 2, 5, 10 and 20-session horizons with a 128-session context, four chronological folds, eight non-overlapping rebalances per fold/horizon, top-six long-only portfolios, a 20-session momentum control, and an explicitly predeclared uncertainty-scaled momentum mechanism.

Only the 10-session TimesFM ranking advanced to Phase 7.

The Phase 7 holdout was frozen before execution:
- 2023-01-02 through 2026-09-03;
- 91 ten-session rebalances;
- PIT eligibility at each origin;
- position drift between rebalances;
- explicit final liquidation;
- dated cash-equity charges;
- additional one-way slippage stresses from 0 to 0.50%.

## 6. Statistical analysis

Forecast metrics include MAE, directional excess and cross-sectional rank IC.

Strategy inference uses chronological fold differences and paired block-signflip tests. No test-period parameter search was allowed.

## 7. Cost model

The Phase 7 simulation included:
- brokerage reference cost;
- delivery-sale DP charge;
- cash-delivery STT;
- stamp duty;
- exchange/IPFT and SEBI turnover charges;
- GST on modeled service components;
- extra one-way slippage/impact stresses;
- explicit liquidation costs.

The model is a research reference cost model, not a contract-note reconstruction for every historical account configuration.

## 8. Results

### 8.1 Forecast gate

TimesFM point forecast MAE was worse than persistence across the tested 2/5/10/20-session horizons. At 10 sessions the return MAE was 0.04660 versus 0.04241 for persistence, directional excess was -5.00 percentage points, and mean cross-sectional rank IC was approximately +0.0048.

### 8.2 Exploratory Phase 4B candidate

The 10-session TimesFM ranking was the only horizon that exceeded the momentum control across all four Phase 4B proportional-cost stresses. Because the exploratory chronology was sparse, this was retained only as a frozen candidate.

### 8.3 Final Phase 7 holdout

| Extra one-way slippage | TimesFM net return | Momentum net return |
|---|---:|---:|
| 0.00% | +3.72% | +67.97% |
| 0.125% | -7.93% | +47.20% |
| 0.25% | -18.30% | +28.96% |
| 0.375% | -27.52% | +12.94% |
| 0.50% | -35.72% | -1.12% |

TimesFM underperformed momentum at every stress level.

At 0.50% extra slippage, TimesFM max drawdown was -41.46% and periodized Sharpe was -0.736. Maximum simulated participation was approximately 0.014% of trailing turnover.

Paired block-signflip p-values were 0.972–0.984 one-sided.

## 9. Inference

The exploratory 10-session advantage did not survive the post-selection chronological holdout. This closes the tested individual-stock EOD/multiday TimesFM mechanism under the present protocol.

## 10. Discussion

The central methodological lesson is the distinction between forecast behavior and economic value. The point forecast itself did not beat persistence, and the only promising cross-sectional selection result did not generalize to the untouched holdout.

The independent momentum control also serves as a useful scientific safeguard: a model should not be promoted simply because its own ranking has positive returns; it must provide incremental value against a plausible simple alternative under the same execution assumptions.

## 11. Strengths and limitations

### Strengths

- frozen experiment matrix;
- independent baseline;
- chronological validation;
- PIT eligibility;
- explicit cost/slippage stresses;
- capacity diagnostics;
- reproducible GitHub Actions;
- detailed error/decision logs;
- explicit stop rule.

### Limitations

- fixed 30-name bootstrap universe;
- official NSE hosted-runner access restrictions;
- research-reference fee model;
- limited block-test power;
- intraday and options lanes remain unresolved.

## 12. Conclusion

Under the tested protocol, TimesFM 3.0 did not produce a validated individual-stock EOD/multiday NSE trading strategy. The single 10-session candidate failed the untouched 2023+ holdout against fixed momentum at zero and all tested slippage levels.

The stock mechanism is closed. No additional TimesFM thresholds, horizons, hybrids or regime variants will be searched on this completed holdout.

## 13. Future research

The next lane is intraday/BTST/scalping research using genuinely validated minute data and execution assumptions. First validate session completeness, missing bars, duplicates, zero-volume behavior, OHLC consistency, daily aggregation and fill realism. Historical options research remains gated on authorized historical option-chain/IV/OI data.

## Appendix A — Reproducibility

Repository: TimesFM-trading

Key artifacts:
- docs/PHASE_4B_CONCLUSION.md
- docs/PHASE_7_TIMESFM10_HOLDOUT.md
- results/p7_timesfm10_holdout_summary.json
- scripts/phase7_timesfm10_holdout.py
- .github/workflows/phase-7-timesfm10-holdout.yml
