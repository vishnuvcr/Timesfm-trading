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


## 2026-09-20 — continued research after NSE hosted-runner blocker

**User direction:** Try other market-data sources and treat individual stocks as first-class trading instruments, not an index-only exercise.

**Observable research actions/outcomes**
- Inspected the repository plan/status/error logs before continuing.
- Retained official NSE/BSE feeds as Tier-P0 reference/authorized sources, but did not keep retrying the same blocked hosted-runner NSE endpoints.
- Expanded the source hierarchy to TejHQ Indian Markets, Yahoo/yfinance-derived Hugging Face data, a large 1-minute NSE stock dataset, an hourly NIFTY/BankNIFTY/IndiaVIX/futures dataset, GitHub NSE OHLCV archives and Kaggle panels, with provenance/licensing/PIT gates documented in `docs/ALTERNATE_DATA_SOURCES.md`.
- Confirmed the individual-stock Phase 2 cache and ran the repaired TimesFM 3.0 30-stock exploratory bootstrap: 5-session horizon, context 128, 40 chronological origins per stock.
- Workflow run 35522976491 completed successfully; artifact 10608372793 was uploaded.
- Mean point-error metrics were worse than persistence across the bootstrap, while mean directional accuracy exceeded the mean positive-return base rate. The interval-width/magnitude relationship was negative and did not reproduce the earlier secondary NIFTY result.
- Decision: do not promote either raw stock direction or TimesFM uncertainty sizing from this run. The next stock research gate must use broader chronological folds, PIT universe/identifier controls, an independent stock-selection baseline and the full cost/slippage model.
