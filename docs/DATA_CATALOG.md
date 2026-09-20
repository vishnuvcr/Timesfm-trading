# Indian market data catalog — Phase 2

Updated: 2026-09-20 IST

## P0 primary domains

The target data lake remains:
- NSE security-wise cash-equity EOD;
- NSE historical indices and India VIX;
- NSE F&O/UDiFF EOD;
- option chain/history with executable bid/ask, OI, volume, IV and expiry/strike mapping;
- corporate actions and corporate filings;
- historical trade/order data for genuine scalping/execution research where licensed.

## Alternate individual-stock EOD lane

### TejHQ / Indian Markets
Repository role: **P0-alternate bootstrap / candidate primary EOD stock input**.

Published coverage includes NSE/BSE equities, raw prices, corporate actions, back-adjusted prices, symbol history, derived metrics and a point-in-time liquidity universe. The public Hugging Face dataset is MIT-licensed and the API exposes keyless per-symbol raw EOD access; adjusted-price and universe surfaces may have separate access requirements.

Repository cache:
- 30-stock NSE bootstrap universe;
- raw EOD OHLCV/turnover;
- separate corporate-action files;
- SHA-256 manifest;
- retrieval timestamp and request URL.

The cached fixed-name panel is not final PIT evidence. Final stock studies must use point-in-time eligibility/liquidity rules and reconcile security identifiers across renames, mergers and delistings.

### Independent Yahoo/yfinance dataset
Hugging Face `vishnun0027/indian-market-historical-ohlcv` is retained as an independent cross-check. It reports thousands of Indian stocks with raw OHLCV plus `adj_close`, dividends and stock splits, sourced from Yahoo Finance via yfinance and MIT licensed.

Role: adjustment/corporate-action cross-check, missing-data diagnostic and source-divergence audit. It is not treated as exchange-primary evidence.

### Other alternate/secondary sources
- GitHub NSE-OHLCV repositories with daily/hourly stock panels: exploratory cross-check only; provenance and licensing must be frozen before use.
- Kaggle Indian stock panels: exploratory cross-check only; provenance, adjustment and license vary by dataset.
- BSE data: separate official cross-exchange source; do not silently merge BSE and NSE observations without identifier/exchange mapping.

## P1/P2 context

- FII/FPI and DII flows with publication vintages;
- GIFT NIFTY / NSE IX;
- BSE cross-exchange data;
- USDINR, rates, crude, gold, Asian/US indices;
- breadth and sector variables;
- timestamped corporate announcements/news;
- point-in-time fundamentals and filings.

## Point-in-time policy

For every feature:
- observation timestamp;
- publication/availability timestamp;
- effective timestamp when distinct;
- revision/vintage;
- source identifier;
- license/storage class.

No feature enters a decision timestamp when its information became available later. Missingness is explicit. No forward-fill across market closures or contract lifecycle boundaries without a documented rule.

## Storage policy

Public repository:
schemas, source registry, manifests, checksums, validation code, permitted bootstrap datasets and derived aggregates.

Private/licensed tier:
restricted exchange raw data, paid historical trade/order data and other vendor-controlled material.

Important raw data is cached once where redistribution terms allow it; workflows reuse the cache instead of downloading the same immutable files on every model run.

## Known hard blocker

The hosted GitHub Actions runner has tested three distinct official NSE historical routes without receiving usable data. That access-layer problem is recorded in issue #6. It does not justify treating alternate datasets as official-primary by assertion; evidence hierarchy and cross-checks remain mandatory.


## 2026-09-20 stock bootstrap result

The alternate lane now contains three linked layers for the 30-name bootstrap:

1. raw EOD OHLCV/turnover;
2. separate corporate actions;
3. back-adjusted prices with cumulative adjustment factors.

It also contains a filtered point-in-time liquid-universe table with monthly rebalance dates, validity intervals, rank and trailing 63-day turnover. This is the data structure intended for stock-level selection without survivorship-biased current-name filtering.

An independent Yahoo/yfinance-derived source was tested on five names. Raw price levels sometimes differed materially, consistent with distinct corporate-action adjustment conventions, while daily return paths were extremely close in the bootstrap sample. The cross-check summary is stored at `data/derived/stock_source_crosscheck.json`.
