# Chat / decision log

## 2026-09-20 — individual-stock scope expansion

**User instruction:** Trading strategy must include individual stocks, not only indices.

**Observable implementation**
- Added a 30-name NSE stock bootstrap universe.
- Added an alternate EOD acquisition lane using TejHQ.
- Added corporate-action caching and validation.
- Added individual-stock strategy design and first-class stock experiments.
- Added an independent Yahoo/yfinance-derived Hugging Face cross-check workflow.
- Kept the fixed 30-name list as bootstrap-only; final evidence requires point-in-time universe/liquidity selection and identifier continuity.

## 2026-09-20 — official NSE blocker response

Three distinct hosted-runner NSE routes remain blocked. The decision is to use independently reachable sources without relabeling them as official-primary.

## 2026-09-20 — alternate stock acquisition outcome

30 stock EOD series were cached and validated. Corporate-action histories are also cached. SHA-256 manifests record source URLs and file hashes. The lane is green for engineering/bootstrapping and not yet a final alpha/strategy dataset.
