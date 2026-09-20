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
