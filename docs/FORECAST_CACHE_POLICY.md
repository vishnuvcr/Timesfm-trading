# Forecast cache policy — TimesFM 3.0

## Rule

The TimesFM model is called once for each pre-registered forecast origin/configuration. The resulting forecasts are cached. Downstream scoring and backtests must never call the model again.

## Cache key

A cache key is the SHA-256 digest of the model id, exact checkpoint, package version, model configuration, weights hash when available, source commit, feature-manifest hash, data vintage, instrument set, target definition, context, horizon, covariate configuration, inference device and deterministic settings.

## Stored result

Each forecast record contains run id, origin timestamp, instrument id, model/checkpoint, horizon, context, target definition, p50, native quantiles, data-vintage hash and feature-manifest hash.

## Storage

Permitted caches may be stored as Parquet/NPZ according to source-data rights. Restricted exchange inputs must not be republished merely because a forecast was derived from them.

## Reproducibility

A scoring job receives only frozen actuals, the forecast cache and the experiment manifest. This prevents accidental model re-runs, configuration drift and silent data refreshes.

## Integrity

Forecast caches are content-hashed. Re-scoring never modifies the cache. A cache becomes immutable once its associated gate report is published.
