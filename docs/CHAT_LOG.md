# Chat / decision log

## 2026-09-20 — user scope confirmation

**User decision:** Keep TimesFM 3.0 as the primary model because the project is research to derive a trading strategy, not to actually trade.

**Repository consequence:** The entire program remains 3.0-first for forecasting, strategy-hypothesis generation, cost/slippage/tax-aware simulated backtesting and research conclusions. The project explicitly excludes real order placement, broker execution, production deployment and revenue-generating/commercial decision-making. TimesFM 2.5 is benchmark/ablation only.

## 2026-09-20 — individual-stock scope expansion

**User request:** Do not treat the trading strategy as index-only; individual stocks must be included.

**Observable repository changes**
- Added a first-class individual-stock research lane to Phase 4.
- Added a 30-name NSE bootstrap universe for engineering/data validation.
- Added stock strategy families: single-stock forecast overlay, cross-sectional ranking, uncertainty-conditioned sizing, stock-vs-index residuals and event-aware stock research.
- Required point-in-time liquidity/membership rules for final stock evidence; the fixed bootstrap universe is not allowed as final evidence.
- Added stock-specific controls for corporate actions, identifier continuity, liquidity, spread/slippage/impact, brokerage/statutory charges and participation caps.

## 2026-09-20 — official NSE acquisition blocker broadened

**Observable outcome:** Hosted GitHub Actions had tested three distinct official NSE routes: NSE Indices historical backend (HTTP 200 HTML instead of JSON), historical-index API (HTTP 403 at session warm-up), and static index archive (repeated timeout including HTTP/1.1 retry).

**Decision:** Do not keep retrying the same blocked public runner path. Add independently reachable alternate sources, preserve their provenance/licensing/PIT status, and use them as alternate P0/P1 research inputs rather than silently upgrading them to official primary status.

## 2026-09-20 — alternate individual-stock source search

**Sources evaluated:** TejHQ Indian Markets, Hugging Face `vishnun0027/indian-market-historical-ohlcv`, Kaggle stock panels, BSE/community historical tooling and existing GitHub NSE OHLCV archives.

**Decision:** TejHQ is the first executable alternate EOD stock lane because its published dataset explicitly covers NSE/BSE equities, corporate actions and a PIT liquidity universe, with keyless per-symbol EOD API access. The Hugging Face Yahoo/yfinance dataset is retained as an independent adjusted-price cross-check. BSE and other community sources remain cross-exchange/secondary validation lanes.

## 2026-09-20 — alternate stock cache result

**Observable result:** The Phase 2 alternate-stock GitHub Actions workflow successfully cached and validated 30 NSE stock EOD series covering approximately 2010-01-04 through 2026-09-18 where each symbol had that much history. A manifest records per-file row counts, source URL and SHA-256. Corporate-action files were subsequently added and validated separately.

**Examples:** RELIANCE, TCS and HDFCBANK each have 4,117 cached EOD rows; INFY has 3,744 beginning 2011-06-29; BAJFINANCE has 3,932 beginning 2010-09-29. RELIANCE action history includes dividends, bonus, rights and demerger events with ISIN/company metadata.

**Evidence classification:** engineering/bootstrap data only until identifier continuity, adjustment methodology and PIT universe eligibility are reconciled.

## 2026-09-20 — existing TimesFM 3.0 P1 evidence

A secondary-data NIFTY 50 bootstrap showed lower point forecast error than persistence but directional accuracy below the positive-return base rate. The multivariate ablation produced mixed results. These remain C-grade exploratory evidence only.

Private chain-of-thought is not copied here; this log records observable decisions, tool/data outcomes, errors and repository changes.


## 2026-09-20 — alternate-source stock validation result

**Observable outcome:** The independent Yahoo/yfinance-derived Hugging Face source was not used as a silent replacement for TejHQ. Instead, five-name cross-checks were run. Raw levels showed adjustment-method differences, but daily return paths were highly consistent; at least 99.7% of overlapping daily raw-close returns differed by no more than 0.10 percentage points for the tested names.

**Decision:** Stock research will validate return paths and corporate-action methodology separately from absolute price-level equality, and will use the TejHQ adjusted-price/PIT-universe trees for the main bootstrap.

## 2026-09-20 — adjusted stock/PIT data result

**Observable outcome:** The TejHQ adjusted-price and point-in-time universe workflow completed successfully. The repository now has adjusted individual-stock series and a monthly PIT liquidity universe for the 30-name bootstrap, in addition to raw prices and corporate actions.

**Next gate:** freeze final PIT universe rules and identifier continuity, then extend the TimesFM forecast matrix from indices to individual stocks before economic strategy promotion.


## 2026-09-20 — Phase 4.1 result synchronized to main

Phase 4.1 tested whether TimesFM adds value to individual-stock selection beyond a predeclared 20-session momentum control. Across 32 five-session rebalances, TimesFM mean rank IC was -0.0237 versus +0.0138 for momentum; the 50/50 hybrid was -0.0151. At the lowest cost stress, TimesFM-only net total return was -26.6%, hybrid -21.8%, momentum -15.2%, and equal-weight universe -7.3%. Higher cost stress worsened results.

Decision: reject the simple TimesFM-only and simple hybrid stock-selection hypotheses. The next empirical step is regime/liquidity/event-conditioned incremental-value testing.


## 2026-09-20 — Phase 4.2 nested regime-conditioned conclusion

The apparent improvement from a low-breadth TimesFM-minus-momentum residual was re-tested with strict nested walk-forward thresholds learned only from prior folds. The residual lost to momentum at every tested cost level from 0.125% to 0.50% one-way.

**Decision:** close the current daily individual-stock TimesFM overlay lane. No tested daily TimesFM stock-selection mechanism has demonstrated incremental value over the independent baseline.

The next work should not search arbitrary TimesFM thresholds for a positive result. Future reopening requires a material protocol amendment, new authorized/PIT-clean data or a genuinely different economic mechanism.


## 2026-09-20 — Phase 4B repository setup

**Observable outcome:** dedicated branch `phase-4b-stock-multifrequency` created from current main. The branch now contains the Phase 4B status/matrix, a 30-stock 2/5/10/20-session swing experiment, a candidate minute-source validation script, and a manual/push Actions workflow.

**Method gate:** BTST is not proxied by a daily close-to-close return. Next-session open/close data must be available and validated before genuine BTST claims are tested.

**Current external evidence:** the candidate minute dataset publishes UTC timestamped OHLCV/OI fields and reports 2022–2026 1-minute coverage; NSE documents regular equity trading 09:15–15:30. These support a validation plan, not yet a promotion to exchange-primary evidence. citeturn461402search0turn437184search0

## 2026-09-20 — Phase 4B CI correction

**Observed failure:** Phase 4B workflow run 35525131467 failed in `setup-python` because the source-validation job requested pip caching without a requirements file. The dependent swing job was skipped.

**Fix:** disabled pip caching for the source-only job; retained dependency caching in the TimesFM swing job. The failure is logged in `docs/ERROR_LOG.md`.

## 2026-09-20 — Phase 4B CI second correction

Run 35525174393 reached setup-python but failed because `cache: false` is not a supported value. The workflow was corrected by removing the cache parameter from the source-validation job entirely. The error is logged in `docs/ERROR_LOG.md`.

## 2026-09-20 — Phase 4B swing matrix result

Observable result: workflow 35525457869 completed the frozen 30-stock 2/5/10/20-session swing matrix, totaling 3,840 stock-level forecast origins.

Source result: the candidate 1-minute source passed a 200-row structural 20MICRONS probe with correct schema, zero duplicate timestamps and zero invalid OHLC rows.

Forecast result: TimesFM MAE was worse than persistence at all horizons; directional excess was negative at every horizon.

Strategy result: the 10-session TimesFM ranking beat the 20-session momentum control at every tested cost stress, including +19.87% versus +9.58% at 0.125% one-way and +3.41% versus -4.80% at 0.50%. It was ahead in three of four chronological folds at 0.125%, but exact sign-flip p=0.625 and BH q=0.833.

Decision: do not call this validated alpha. Retain the 10-session TimesFM ranking as a downstream exploratory candidate for regime/external-information and Phase 7 walk-forward validation; reject the other TimesFM horizon cells for promotion.

Artifacts: workflow 35525457869; swing artifact 10609348369; source-validation artifact 10610350345. Compact results and hashes are committed under results/.