# Phase 4B swing conclusion — 2026-09-20

## Research question

After the daily individual-stock TimesFM overlay lane failed, does TimesFM 3.0 add useful information at a different stock holding period when tested against an independent 20-session momentum control?

## Design

Thirty bootstrap NSE stocks were evaluated with a 128-session context, TimesFM 3.0 adjusted-log-price forecasts, 2/5/10/20-session horizons, four chronological folds, eight non-overlapping rebalances per fold/horizon, top-six long-only selection, and four one-way cost stresses: 0.125%, 0.25%, 0.375% and 0.50%.

The uncertainty-conditioned mechanism was frozen before observing the result: 20-session momentum multiplied by an inverse TimesFM q10-q90 forecast-width factor.

The run completed successfully as workflow 35525457869; the signal-level artifact is retained in GitHub Actions and the compact result summary is committed under results/.

## Data-source gate

The candidate 1-minute source passed a structural 200-row probe for 20MICRONS: the expected schema was present, duplicate timestamps were zero, invalid OHLC rows were zero, timestamps began at 09:15 IST, and 21 sampled rows had zero volume.

This is a source-integrity check only; the source is not being upgraded to exchange-primary or fill-accurate evidence. Hugging Face documents its Dataset Viewer rows and filter APIs for querying parquet datasets without downloading the full dataset.

## Forecast findings

| Horizon | TimesFM MAE | Persistence MAE | Directional excess | Rank IC |
|---|---:|---:|---:|---:|
| 2d | 0.020474 | 0.019254 | -2.40 pp | -0.0668 |
| 5d | 0.035607 | 0.033388 | -4.58 pp | -0.0392 |
| 10d | 0.046599 | 0.042405 | -5.00 pp | -0.0204 |
| 20d | 0.063672 | 0.058139 | -1.15 pp | +0.0235 |

TimesFM point-error MAE was worse than persistence at every horizon. The 10-session strategy result must therefore not be described as a general improvement in point forecasting.

## Strategy findings at 0.125% one-way cost

| Horizon | Momentum | TimesFM | Uncertainty-scaled momentum |
|---|---:|---:|---:|
| 2d | -10.42% | -15.58% | -11.62% |
| 5d | -18.34% | -29.98% | -12.03% |
| 10d | +9.58% | +19.87% | +0.29% |
| 20d | -17.55% | -18.07% | +7.80% |

At the 0.50% one-way stress: 2d momentum/TimesFM/scaled = -17.66%/-25.60%/-19.49%; 5d = -26.77%/-38.57%/-20.61%; 10d = -4.80%/+3.41%/-13.23%; 20d = -32.11%/-29.41%/-10.68%.

The 10-session TimesFM ranking is the only TimesFM cell that beats momentum at every tested cost level.

## Ten-session chronological folds at 0.125%

| Fold | Momentum | TimesFM |
|---|---:|---:|
| 1 | -8.58% | -12.98% |
| 2 | +0.28% | +2.41% |
| 3 | +1.20% | +11.90% |
| 4 | +18.11% | +20.21% |

TimesFM is ahead of momentum in three of four chronological folds, but not in fold 1.

## Statistical interpretation

The exact four-fold sign-flip p-value for 10-session TimesFM versus momentum is 0.3125 at each tested cost level. At the 0.125% reference, Benjamini-Hochberg adjustment across the eight predeclared horizon/mechanism cells gives The candidate is not statistically promoted; this final holdout gate is intentionally carried forward to Phase 7 rather than treating the sparse four-fold result as conclusive.

Therefore the result is not statistically promoted. It is a candidate research signal, not validated alpha.

## Concentration

For the 10-session TimesFM ranking, selection HHI was 0.0379; the top five names represented 25.5% of selections and 32.8% of absolute gross contribution; median selection frequency was 7 of 32 rebalances and maximum was 11.

## Decision

Advance only the 10-session TimesFM stock-ranking hypothesis to the next research gate. Do not promote the 2-session, 5-session or 20-session TimesFM ranking cells. Do not promote the uncertainty-scaled mechanism because its 20-session advantage does not survive the full cost stress range.

The 10-session cell remains exploratory because the point forecast was worse than persistence, the universe is a fixed 30-name engineering/bootstrap panel, the four-fold statistical evidence is weak, and final PIT identity/corporate-action reconciliation is incomplete.

## Next gate

The candidate now advances directly to the predefined Phase 7 post-selection holdout. The previously completed Phase 6 regime-residual track is not reopened; no additional TimesFM variants are being searched.

BTST, intraday and scalping remain separate lanes requiring deeper 1-minute validation and execution-quality checks. A daily close-to-close return will not be relabeled as BTST.

## Strengths and limitations

Strengths: frozen horizons, chronological folds, independent baseline, explicit cost stresses, and predeclared uncertainty mechanism.

Limitations: bootstrap stock universe, limited 1-minute source probe, low-power four-fold significance test, and a simplified cost/execution model pending Phase 7.

## Conclusion

Phase 4B has produced one scientifically useful candidate: a 10-session TimesFM 3.0 cross-sectional forecast ranking. It has not produced a validated trading strategy. The next step is conditional, point-in-time and cost-aware validation rather than arbitrary threshold tuning.