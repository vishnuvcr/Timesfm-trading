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
