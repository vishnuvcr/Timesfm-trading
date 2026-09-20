# Final research conclusion

Updated: 2026-09-20 IST

## Executive conclusion

The completed individual-stock TimesFM 3.0 research program did **not** establish a validated trading strategy.

The strongest evidence is the post-selection Phase 7 holdout of the only Phase 4B candidate that survived the exploratory gates. The candidate was a 10-session TimesFM 3.0 cross-sectional ranking strategy using a long-only top-six portfolio and a 20-session momentum control.

On an untouched 2023+ holdout with 91 ten-session rebalances:

| Extra one-way slippage | TimesFM net return | Momentum net return |
|---|---:|---:|
| 0.00% | +3.72% | +67.97% |
| 0.125% | -7.93% | +47.20% |
| 0.25% | -18.30% | +28.96% |
| 0.375% | -27.52% | +12.94% |
| 0.50% | -35.72% | -1.12% |

The TimesFM candidate was below momentum at every stress level, including zero additional slippage. Its maximum drawdown reached -41.46% at the maximum stress, versus -23.80% for momentum. The paired period difference was negative throughout, with one-sided block-signflip p-values between 0.972 and 0.984. Maximum simulated participation was only about 0.014% of trailing turnover, so capacity was not the binding explanation.

## Evidence sequence

1. The 30-stock TimesFM 3.0 bootstrap was worse than persistence on stock point-error aggregates.
2. A recent positive directional finding did not survive four-fold chronological robustness across 4,800 origins.
3. Direct TimesFM stock ranking, hybrid selection and directional gating did not outperform the independent momentum baseline in the initial strategy tests.
4. Regime-conditioned TimesFM residuals did not show statistically supported incremental information after rebalance-level permutation tests and BH-FDR.
5. A predeclared 2/5/10/20-session swing matrix identified one exploratory 10-session TimesFM ranking candidate that exceeded momentum across Phase 4B proportional cost stresses.
6. The candidate passed the cached point-in-time eligibility check, but this check remained limited to the 30-name bootstrap panel.
7. The single candidate then failed the untouched 2023+ Phase 7 post-selection holdout.

## Scientific interpretation

The negative conclusion is narrower than “TimesFM cannot work in finance.” It means that, on the available Indian-equity bootstrap data and under the frozen strategy translation tested here, TimesFM 3.0 did not demonstrate robust incremental economic value after chronological robustness, an independent trading baseline, and a cost-aware post-selection holdout.

The failure of the candidate at zero extra slippage is especially informative: the main issue is not merely an aggressive slippage assumption. Additional slippage simply widens an already negative gap.

## Current stop rule

The current individual-stock EOD TimesFM search is closed. The completed holdout must not be mined for new thresholds, alternate horizon choices, hybrid weights, regime filters or other specification variants.

A future reopening requires a new preregistered branch and untouched holdout, and should use a materially different economic mechanism, a materially broader/cleaner point-in-time universe, or a different instrument/frequency.

## Remaining research scope

The negative stock result does not resolve:
- authorized broad-universe exchange data;
- historical options with bid/ask, OI, IV and Greeks;
- licensed execution-grade intraday data;
- global cross-market or institutional-flow conditioning on a fresh holdout;
- other model classes under identical frozen-origin benchmarks.

These are distinct future research tracks, not reasons to reopen the completed TimesFM10 stock holdout.

## Reproducibility

The final candidate holdout is reproducible from:
- `scripts/phase7_timesfm10_holdout.py`
- `.github/workflows/phase-7-timesfm10-holdout.yml`
- `configs/fee_manifest_2026-09-20.json`
- `results/p7_timesfm10_holdout_summary.json`
- `docs/PHASE_7_TIMESFM10_HOLDOUT.md`

The full manuscript is:
`manuscript/TimesFM_NSE_Research_Manuscript.md`

No live, paper, broker or production execution path is enabled.
