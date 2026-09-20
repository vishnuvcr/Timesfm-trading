# Chat / decision log\n
## 2026-09-20 — user scope confirmation

**User decision:** Keep TimesFM 3.0 as the primary model because the project is research to derive a trading strategy, not to actually trade.

**Repository consequence:** The entire program remains 3.0-first for forecasting, strategy-hypothesis generation, cost/slippage/tax-aware simulated backtesting and research conclusions. The project explicitly excludes real order placement, broker execution, production deployment and revenue-generating/commercial decision-making. TimesFM 2.5 is benchmark/ablation only.
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


## 2026-09-20 — license boundary correction

A direct read of the official TimesFM 3.0 Non-Commercial License shows a stricter boundary than earlier project notes: Non-Commercial Purpose excludes commercial gain, revenue generation and commercial decision-making, and the restrictions extend to model Outputs. The research plan is corrected so 3.0 remains the primary scientific/evaluation lane, while 3.0-derived trading decisions remain blocked until commercial rights are obtained. TimesFM 2.5 remains the current trading/production research lane.


## 2026-09-20 — implementation progress after scope confirmation

**Observable outcomes**
- Phase 3 unit/statistics CI became green after correcting MAE/RMSE fixtures; no real forecast result exists yet.
- Phase 2 CI became green after fixing an unterminated string literal in the manifest validator; the remaining gate is acquisition of the first frozen P0 datasets.
- Phase 4 added non-executing research primitives for cost hurdles, uncertainty-adjusted sizing, volatility-targeted exposure and a simulation-aware model/license gate; CI passed.
- Phase 5 added implied-movement benchmarking, residual-vs-cost gating and defined-risk debit-spread accounting. The first CI run found a floating-point fixture assertion; it was changed to approximate comparison and the corrected CI run is being verified.
- Draft PR #5 was opened for the Phase 5 engineering bootstrap.


## 2026-09-20 — official P0 acquisition blocker

**Observable outcome:** Four GitHub Actions attempts to retrieve the official NIFTY 50 historical endpoint all received the NIFTY Indices HTML application page with HTTP 200 rather than the expected JSON response. Cloudflare/browser-profiled session warm-up did not resolve it. The retry loop was closed and issue #6 opened. A fixed secondary Google Finance-derived NIFTY 50 snapshot is being used only for P1 TimesFM 3.0 pipeline validation; it is not primary evidence and is not redistributed because the upstream repo has no explicit license file.


## 2026-09-20 — first TimesFM 3.0 P1 forecast result

**Observable outcome:** Corrected Phase 3 P1 workflow run 56 completed successfully on the fixed secondary NIFTY 50 snapshot. At 80 origins / 5-session horizon, TimesFM 3.0 reduced log-level MAE by 13.63% and RMSE by 15.66% versus persistence; five-day return MAE improved by 13.18%. Directional accuracy was 70.0% versus a 75.0% positive-return base rate, and q10-q90 coverage was 78.75%. The result is recorded as C-grade exploratory evidence only and cannot promote a trading strategy or substitute for primary NSE P0 data.
