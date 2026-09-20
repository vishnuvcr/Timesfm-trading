# Dataset manifests

This directory stores metadata about frozen datasets, not restricted raw market data.

Each manifest records:
- source and URL
- retrieval and effective dates
- content hash
- row count where known
- schema version
- storage/licence tier
- point-in-time validation status
- revision/vintage

Restricted NSE/BSE raw data should remain in approved private/licensed storage. The manifest makes the exact input reproducible without redistributing the raw feed publicly.
