# Alternate Indian equity data sources — Phase 2

Updated: 2026-09-20 IST

## Reason for the alternate lane

The hosted GitHub Actions runner has repeatedly failed to retrieve the official NSE NIFTY 50 history through three distinct public routes:

1. NSE Indices historical backend — HTTP 200 HTML instead of JSON.
2. NSE historical-index API — HTTP 403 during session warm-up.
3. NSE static index archive — repeated timeouts, including an HTTP/1.1 retry.

This is an access-path blocker, not evidence that exchange data do not exist. The research therefore adds independently reachable sources instead of repeatedly retrying the same blocked runner path.

## Source A — TejHQ / `tejhq/indian-markets`

TejHQ states that its Indian EOD dataset is built from official NSE and BSE bhavcopy/corporate-action feeds. It publishes raw EOD prices, corporate actions, back-adjusted prices, symbol history and a point-in-time liquidity universe. NSE coverage is stated as 2010-01-04 to present.

The keyless API exposes per-symbol EOD OHLCV and corporate-action data; adjusted-price and symbol-history API surfaces require a free key. The same data are published in parquet on Hugging Face.

**Research role:** alternate P0 candidate for individual-stock EOD bootstrap and cross-sectional research, with source lineage preserved.

**Current cache:** a fixed 30-name NSE stock panel is wired into the repository. This is explicitly a bootstrap/engineering dataset, not final PIT evidence.

## Source B — Hugging Face `vishnun0027/indian-market-historical-ohlcv`

The dataset reports thousands of Indian stocks plus indices/ETFs/commodities/FX and provides raw OHLCV, adjusted close, dividends and stock splits. It is listed with an MIT dataset license and states that its source is Yahoo Finance via `yfinance`.

**Research role:** independent adjusted-price cross-check and corporate-action/price-series divergence diagnostic. It is not treated as exchange-primary data.

## Source C — Kaggle stock panels

Kaggle hosts multiple historical NSE-stock datasets, including all-stock daily OHLCV snapshots and yfinance-derived Nifty-500 panels. These can be used as additional reproducibility checks, but each dataset's provenance, licensing and adjustment method must be frozen before use.

## Source D — BSE

BSE exposes official equity bhavcopy/history endpoints, and community implementations document the current UDiFF naming convention. BSE will be retained as a separate cross-exchange validation source rather than mixing BSE and NSE rows without a security/ISIN mapping.

## Stock-strategy implication

Individual stocks are now an explicit Phase 4 research object, not an index-only extension. The index becomes a market-state/baseline feature; stock-level hypotheses will be tested across:

- individual-stock returns/range/volatility;
- cross-sectional ranking and dispersion;
- stock-vs-index relative strength;
- sector/market regime conditioning;
- liquidity/turnover and participation constraints;
- corporate-action/event days;
- stock-specific costs and slippage.

The fixed bootstrap list is not a final universe. Final evidence must use point-in-time membership/liquidity rules and preserve name/ISIN history where available.

## Evidence hierarchy

For each alternate dataset, the repository records:

1. source URL and claimed upstream lineage;
2. retrieval timestamp and exact request;
3. SHA-256 checksum;
4. coverage and missingness;
5. adjustment/corporate-action methodology;
6. licensing/redistribution status;
7. PIT/survivorship-bias status;
8. role in the evidence hierarchy.

A reachable source is not automatically upgraded to official P0 merely because it is accessible.


## TejHQ adjusted prices and PIT liquidity universe

The alternate lane now uses more than raw EOD values. The public TejHQ dataset also exposes a `prices_adjusted/` tree with cumulative adjustment factors and adjusted close, plus `symbol_history/` and `universe/nse_liquid.parquet` for point-in-time liquidity membership. The Phase 2 workflow filters these structures to the bootstrap stock set and caches the resulting adjusted series and PIT membership table.

This is preferable to applying a simplistic split-only correction because dividends and other corporate actions can affect historical price continuity. The exact adjustment convention remains documented and must be frozen before final stock backtesting.

## Independent cross-check

The five-name Yahoo/yfinance-derived Hugging Face cross-check is executed by a separate manual/push workflow. It is a validation source, not the primary series. Absolute price-level differences can be material under different corporate-action conventions; the cross-check therefore reports both level divergence and daily return-path agreement. The first five-name run passed with >=99.7% of overlapping daily raw-close returns within 0.10 percentage points.


## Additional stock/intraday sources

### TickerTruth NSE security master
A CC-BY-4.0 reference dataset normalizes NSE equity symbols, ISINs, listing dates and active/delisted status. It states that its source is the NSE public equity master and is refreshed nightly.

**Role:** identifier continuity and survivorship/delisting cross-check. It is not used as the primary price series.

### Indian stock minute dataset
The MIT-licensed `xxparthparekhxx/indian-stock-market-minute-data` dataset contains roughly 713 million minute observations for more than 2,500 NSE stocks/indices over 2022–2026.

**Role:** P1 intraday/scalping exploratory lane. Because minute-bar provenance, corporate-action treatment, timestamp normalization and execution semantics differ from the EOD pipeline, it must pass a separate intraday data-quality gate before any cost-aware inference.

### NSE-OHLCV-Data
The `Dr-Kitz28/NSE-OHLCV-Data` GitHub repository provides daily and hourly stock OHLCV and states academic/research use.

**Role:** P2 hourly/daily cross-check only until license and provenance are frozen.
