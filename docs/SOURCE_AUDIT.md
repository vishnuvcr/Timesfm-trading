# Phase 2 source audit

## Primary sources

TimesFM 3.0:
- GitHub: https://github.com/google-research/timesfm
- PyTorch weights: https://huggingface.co/google/timesfm-3.0-pytorch
- Google Research release: https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/

NSE India:
- Historical reports: https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives
- Derivatives reports: https://www.nseindia.com/all-reports-derivatives
- Option chain: https://www.nseindia.com/option-chain
- India VIX: https://www.nseindia.com/static/products-services/indices-indiavix-index
- FII/FPI and DII: https://www.nseindia.com/reports/fii-dii/
- Corporate actions: https://www.nseindia.com/static/investor-relations/corporate-actions
- Historical trade/order data: https://www.nseindia.com/static/market-data/eod-historical-data-subscription
- Data policy: https://www.nseindia.com/static/market-data/nse-data-policy

NSE IX / GIFT NIFTY:
- https://www.nseix.com/markets/trading/tradinghours

BSE India:
- https://www.bseindia.com/

Paytm Money:
- https://www.paytmmoney.com/stocks/brokerage-calculator

## Secondary validation sources

- https://github.com/NikhilSuthar/indian-market-data
- https://github.com/SantoshSrinivas79/NSE-FNO-Data-bank
- https://github.com/gsidhu/nse-intraday-data
- https://huggingface.co/datasets/rissin/nse-options-intraday
- https://www.kaggle.com/datasets/nishanthsalian/indian-stock-index-eod-data1990-onwards

These community sources are useful for parser development, provenance checks and bootstrap tests, but official/licensed exchange data remain the source of record.

A YouTube search for directly relevant TimesFM 3.0 trading/finance/NSE material returned no useful results during the Phase 2 audit.

## Source hierarchy

1. official exchange/regulator/model source
2. licensed vendor
3. reproducible community implementation
4. community dataset
5. practitioner content


## 2026-09-20 — hosted-runner access test outcome

Official NSE access was tested through three independent routes from GitHub Actions: the NSE Indices historical backend, the NSE `historicalOR/indicesHistory` API, and the `nsearchives.nseindia.com` static index archive. The first returned HTML with HTTP 200, the second returned HTTP 403 during session warm-up, and the third timed out repeatedly. These are access-layer limitations of the hosted runner environment, not evidence that the data itself is unavailable. Primary research therefore requires an authorized/official data-delivery mechanism or licensed vendor feed.
