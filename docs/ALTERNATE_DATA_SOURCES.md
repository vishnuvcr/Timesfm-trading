# Alternate data-source policy and source expansion

Updated: 2026-09-20 IST

## Purpose

The official NSE hosted GitHub Actions access path is currently blocked for several historical-index routes. The research therefore uses a source hierarchy rather than treating any alternate feed as silently equivalent to an exchange-primary dataset.

## Source hierarchy

### Tier P0 — exchange-primary / authorized
**NSE official**
- Security-wise price/volume archives for equities.
- Historical indices and India VIX.
- F&O and other official historical reports.
- Securities master and corporate-action reports.
- Paid EOD/order/trade historical products where licensed.

NSE documents confirm that security-wise archives, historical indices/VIX, derivatives reports and corporate-action/security-master reports are part of the official data ecosystem.

**Current status:** official public routes tested by the hosted runner remain blocked or unusable for the required historical-index workflow. This is recorded in Issue #6. The existence of the official archives is not treated as evidence that the hosted runner can retrieve them.

**BSE official**
- BSE bhavcopy / EOD ecosystem and historical OHLC/data products are the cross-exchange reference.
- BSE documentation also exposes current/historical bhavcopy formats and pricing for licensed historical OHLC/EOD data.

**Current status:** candidate cross-check / authorized source; no BSE dataset is promoted to primary until identifier, adjustment, licensing and hosted-runner retrieval tests are completed.

## Tier P0-alternate — current executable stock lane

### TejHQ / Indian Markets
Hugging Face dataset: `tejhq/indian-markets`

Published dataset description states that it contains NSE/BSE listed equities from official exchange bhavcopy feeds, with raw prices, corporate actions, back-adjusted prices, symbol history, derived metrics and a survivorship-bias-free liquidity universe. The public dataset is MIT-licensed.

**Repository status:** green bootstrap lane.
- 30-name NSE raw EOD cache;
- corporate-action cache;
- adjusted-price cache;
- point-in-time liquidity metadata;
- SHA-256 manifests;
- GitHub Actions acquisition and validation.

**Scientific status:** usable for bootstrap/engineering and exploratory stock forecasting. Final evidence still requires identifier continuity, corporate-action reconciliation and frozen PIT universe rules.

## Tier P1 — independent cross-check sources

### Yahoo Finance / yfinance-derived Hugging Face dataset
Dataset: `vishnun0027/indian-market-historical-ohlcv`

Current dataset metadata reports 2,615 stock files plus indices/ETFs/commodities/FX, daily OHLCV with adjusted close, dividends and splits, and daily refreshes.

**Role:** independent return-path / corporate-action cross-check and missing-data diagnostic.

**Restriction:** not exchange-primary evidence. A source disagreement is investigated rather than resolved by assuming either provider is correct.

### Hugging Face 1-minute NSE stock dataset
Dataset: `xxparthparekhxx/indian-stock-market-minute-data` (also mirrored as `rahulkrraj/indian-stock-market-minute-data`)

Current dataset card reports roughly 715 million rows covering 2,500+ NSE stocks and indices, 1-minute candles for 2022–2026, and daily data back to 2000. The dataset is marked MIT and is suitable as a candidate source for intraday stock research.

**Role:** candidate intraday/scalping cross-check and TimesFM high-frequency bootstrap.

**Gate before empirical use:** validate symbol continuity, timestamp/session coverage, duplicate bars, missing bars, corporate-action treatment, source provenance and execution-price plausibility. The repository must not treat the dataset's coverage claims as equivalent to exchange-primary certification.

### Hugging Face hourly Indian-market dataset
Dataset: `calender/indian-stock-hourly-2017-2021`

The dataset is marked CC-BY-4.0 and contains approximately 40,445 hourly bars across NIFTY, Bank NIFTY, India VIX and two futures instruments from May 2017 to December 2021.

**Role:** historical intraday/index/futures methodology cross-check.

**Restriction:** it is not a full individual-stock minute history and therefore cannot by itself support stock scalping claims.

### GitHub NSE-OHLCV-Data
Repository: `Dr-Kitz28/NSE-OHLCV-Data`

The repository states that it provides daily and hourly OHLCV data for NSE stocks and is intended for academic/research use.

**Role:** secondary reproducibility/cross-check source.

**Restriction:** provenance, redistribution rights, adjustment methodology and exact update history must be frozen before repository caching or promotion into an empirical holdout.

## Tier P2 — older/public benchmark datasets

### Kaggle NSE stock datasets
Examples located during source review include:
- NSE India Stock Market Data (2015–2024);
- Historical Data of Stocks Listed on NSE;
- Indian Stock Market EOD Data (1990 onwards).

The reviewed datasets generally derive from yfinance, nsepy/nsetools or other public collection layers and have different licenses/coverage periods.

**Role:** benchmark/failure-diagnostic only. They are not used to establish exchange-primary truth.

## Selection rule

A source is promoted only after the following are separately checked:
1. provenance and license;
2. symbol/ISIN continuity;
3. corporate-action treatment;
4. trading-calendar and session integrity;
5. missing/duplicate bar rates;
6. PIT eligibility/universe construction;
7. cross-source return-path agreement;
8. execution-price plausibility for the intended frequency.

The main stock study currently remains anchored on the TejHQ adjusted/PIT bootstrap plus independent Yahoo/yfinance checks. The new 1-minute source is a candidate for Phase 4 intraday/scalping validation, not a shortcut around exchange-primary execution-quality requirements.

## Implication for the research plan

The NSE blocker no longer blocks individual-stock EOD research. It does, however, continue to block claims that require exchange-primary NIFTY/index history or exchange-grade intraday execution data. The Phase 4 empirical stock lane can therefore proceed on the daily bootstrap after the forecast/cost gates, while scalping claims remain gated on intraday data validation.
