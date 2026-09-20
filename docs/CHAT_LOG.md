# Chat / decision log

## 2026-09-20

**User request:** Deep research on using TimesFM for NSE trading across scalping, intraday, BTST, swing and options, with a consistent trading pipeline; repository: `vishnuvcr/Timesfm-trading`.

**Recorded actions/outcomes**
- Inspected repository metadata: public repo, default branch `main`, initially empty.
- Created phased research plan and governance files.
- Started evidence review using Google Research/TimesFM, arXiv/Hugging Face research, NSE official materials and Paytm Money official materials.
- Identified license constraint: TimesFM 3.0 pretrained weights are currently non-commercial/non-production; TimesFM 2.5 remains the practical deployable research lane under Apache-2.0 weights.
- Identified evidence that raw directional accuracy can be misleading and that TSFM gains over naive financial baselines may be small; the project therefore uses a forecast gate and economic-value gate.
- No live strategy has been approved.

Private chain-of-thought is not copied here; this log records observable decisions and outcomes.


## 2026-09-20 — model selection update

The user explicitly selected TimesFM 3.0. The plan is changed to make 3.0 the primary research model and 2.5 the benchmark/ablation/fallback. Official sources confirm 3.0 supports native multivariate forecasting and flexible covariates. Its current pretrained-weight license permits qualifying research/evaluation but does not clear commercial or production use; live deployment therefore requires separate licensing/permission or an appropriately licensed production model.

## 2026-09-20 — Phase 7 holdout resolves Phase 4B

The single frozen 10-session TimesFM stock-ranking candidate failed the 2023+ post-selection holdout. Net return was +3.72% at zero extra slippage versus +67.97% momentum, and became negative at 0.125% extra slippage. At 0.50% extra slippage it was -35.72% versus -1.12% momentum. Capacity was not the bottleneck.

Decision: close the current individual-stock TimesFM strategy search. No further TimesFM thresholds/horizons/hybrids/regime variants are permitted on this completed holdout.
