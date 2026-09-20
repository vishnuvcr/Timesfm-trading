# Phase 2 — NSE data policy

## Purpose

Build a point-in-time data lake suitable for TimesFM 3.0 forecasting and cost-aware trading research.

## Non-negotiable rules

1. Raw source data is immutable after ingestion.
2. Every snapshot records source, URL/identifier, retrieval timestamp, effective date, coverage, schema version, checksum and licence/storage class.
3. Research features use only information available at the forecast timestamp.
4. Revisions are stored as new vintages; historical rows are never silently overwritten.
5. Corporate actions are event data, not merely price adjustments.
6. Futures/options contracts are identified by exchange contract identifiers, not reconstructed only from strike/expiry text.
7. Option-chain observations retain quote timestamp, bid/ask, OI, volume, IV and underlying reference.
8. Missingness is explicit; no forward fill is allowed across a market closure or contract lifecycle boundary without a documented rule.
9. Cached licensed data are stored only where redistribution rights permit. For restricted NSE/BSE data, the public repository stores manifests, schemas, derived research aggregates and reproducibility metadata; private/licensed storage is referenced by content hash.
10. Every dataset is tested for duplicates, timestamp ordering, timezone, schema drift, impossible prices, corporate-action discontinuities and future-information leakage.

## TimesFM 3.0 alignment

TimesFM 3.0 can consume multivariate series and past/future covariates. Phase 2 therefore stores a causal feature timeline rather than only a price table.

For every feature, the metadata records:
- observation time
- publication/availability time
- effective time, if different
- revision/vintage
- allowed forecast horizons
- source priority

A feature is eligible only when its availability timestamp is <= the strategy decision timestamp.

## Storage tiers

### Tier A — public repository
Schemas, source registry, manifests, checksums, tests, derived aggregates that contain no restricted raw market data.

### Tier B — repository release/artifact
Research outputs and small permitted samples used for tests.

### Tier C — private/licensed cache
Restricted NSE/BSE raw files, paid historical trade/order data and other vendor-controlled data.

The data loader must accept Tier C paths through environment variables and must never require downloading the same immutable file on every workflow run.

## Primary official source families

NSE historical reports and security-wise archives; NSE F&O UDiFF/bhavcopy reports; NSE option-chain interface; NSE India VIX; NSE FII/FPI and DII reports; NSE corporate filings/actions; NSE historical EOD/trade data products; NSE index data products; NSE IX/GIFT NIFTY; BSE EOD/historical products.

## Phase 2 gate

The phase passes only when:
- the source registry is complete for P0 datasets;
- every P0 dataset has a schema and PIT rule;
- a manifest can be validated without network access;
- a synthetic leakage test catches a deliberately future-dated feature;
- no restricted raw file is accidentally committed to the public repo.


## Derivatives format transition

The historical F&O ingestion layer must branch by trade date at the NSE UDiFF transition on 2024-07-08. Before that date, legacy F&O bhavcopy archives use the `foDDMMMYYYYbhav.csv.zip` convention; from 2024-07-08, UDiFF common bhavcopy files use the `BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip` convention. This parser transition is independently documented in the community F&O archive and should be cross-checked against NSE's own report metadata before production ingestion. 
