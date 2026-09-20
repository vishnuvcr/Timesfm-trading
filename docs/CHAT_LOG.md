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


## 2026-09-20 — final empirical stop and manuscript release

The individual-stock empirical sequence is complete under the project's declared stop rule: forecast bootstrap → chronological robustness → stock-selection control → regime-conditioned incremental test → cost gate.

No TimesFM 3.0 stock strategy passed promotion. The final repository release therefore records a negative scientific conclusion rather than continuing specification search. Phase 9 manuscript and final-conclusion artifacts were validated by GitHub Actions and synchronized into main.

No live/paper execution is enabled.


## 2026-09-20 — Phase 4B superseded the earlier stock stop

The earlier daily-stock empirical stop was followed by the predeclared multifrequency continuation. The 10-session TimesFM cross-sectional ranking passed the cached PIT candidate gate and is now frozen for a Phase 7 post-selection holdout.

This is not an authorization to reopen arbitrary TimesFM variants. The single candidate is the only stock mechanism moving forward.


## 2026-09-20 — Phase 7 resolves the Phase 4B candidate

The single frozen 10-session TimesFM individual-stock ranking candidate was evaluated once on the untouched 2023+ holdout.

Results:
- 0.00% extra slippage: TimesFM +3.72% vs momentum +67.97%;
- 0.125%: -7.93% vs +47.20%;
- 0.25%: -18.30% vs +28.96%;
- 0.375%: -27.52% vs +12.94%;
- 0.50%: -35.72% vs -1.12%.

The candidate was below momentum at every stress level. One-sided block-signflip p-values were 0.972–0.984. Maximum participation was about 0.014% of trailing turnover.

**Decision:** close the current individual-stock TimesFM strategy search and proceed to final manuscript/release. No additional TimesFM thresholds, horizons, hybrids or regime variants are permitted on the completed holdout.

## 2026-09-20 — Phase 4 intraday gate started

The daily/multiday individual-stock TimesFM candidate was closed by Phase 7. A separate intraday/BTST/scalping data-integrity gate was started on branch `phase-4-intraday-gate`.

The gate is source-only: no TimesFM trading strategy is being tested yet. It checks minute-bar schema, UTC→IST session mapping, complete 09:15–15:29 sessions, duplicates/gaps, OHLC validity, zero-volume behavior and source consistency against the cached EOD lane.

The first execution failed on an unused NumPy import; it was removed and rerun. The current hosted run remains active.
