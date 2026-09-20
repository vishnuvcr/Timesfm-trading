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


## 2026-09-20 — Phase 4.1 stock strategy result

The research was extended from forecast accuracy into an explicit individual-stock selection test. The control was 20-session cross-sectional momentum; TimesFM supplied a 5-session forecast rank; the hybrid was a 50/50 standardized combination; a momentum-gated TimesFM variant was also tested.

Across 32 non-overlapping rebalances, TimesFM mean rank IC was -0.0237 versus +0.0138 for momentum. The hybrid was -0.0151. TimesFM top-six excess versus the equal-weight universe averaged -0.00554 per five-session period; the hybrid averaged -0.00359.

At the lowest cost stress, TimesFM-only net total return was -26.6%, hybrid -21.8%, momentum control -15.2%, and equal-weight universe -7.3% over the sparse test. Higher cost stress worsened all strategies.

**Decision:** do not promote the standalone TimesFM or simple hybrid stock strategies. The next strategy experiment must test conditional/incremental information after stronger regime, liquidity and event controls.


## 2026-09-20 — Phase 4.2 nested regime result

The low-breadth TimesFM-minus-momentum residual showed an apparent improvement when the breadth threshold was viewed using the full sample. That was recognized as a potential selection/hindsight problem.

The rule was rewritten as a nested walk-forward: each test fold's breadth threshold uses only earlier folds. On the resulting folds 2–4, the residual strategy underperformed the momentum control at every tested cost level:
- 0.125% one-way: -10.02% residual vs -5.20% momentum;
- 0.25%: -12.22% vs -7.72%;
- 0.375%: -14.37% vs -10.16%;
- 0.50%: -16.48% vs -12.55%.

**Decision:** close the current daily individual-stock TimesFM overlay lane. Do not recycle the earlier full-sample conditional result as positive evidence.
