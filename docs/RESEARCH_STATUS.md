# Research status

Updated: 2026-09-20 IST

## Scope decision — 2026-09-20
**Confirmed:** TimesFM 3.0 stays the primary model for all phases because this project is research for deriving and testing a trading strategy, not actually trading.

The scope is explicitly **non-executing scientific research**:
- strategy hypotheses may be generated and falsified;
- full cost/slippage/tax-aware simulated backtests are allowed;
- no broker execution, production deployment, client-facing trading decision or revenue-generating use is part of the project;
- TimesFM 2.5 is a benchmark/ablation model only.

## Phase 0 — Governance
**Complete for bootstrap.**

## Phase 1 — Literature
**Complete / protocol frozen.**

Model decision:
- TimesFM 3.0 primary scientific/evaluation model throughout the research.
- TimesFM 2.5 benchmark/ablation only.
- Direct direction is one hypothesis; uncertainty, volatility, multivariate inputs and causal covariates are explicit research targets.
- The current 3.0 pretrained-weight license remains a hard governance gate for any commercial/production use.

## Phase 2 — Data
**Validation green. Official public NSE runner routes remain blocked; alternate individual-stock EOD lane is now green.**

Completed on `phase-2-data`:
- point-in-time data policy;
- official source registry;
- community/alternate source registry;
- dataset manifest schema;
- manifest validator;
- synthetic PIT leakage test;
- manual GitHub Actions validation workflow;
- official-source audit;
- alternate TejHQ individual-stock EOD acquisition workflow;
- 30-name bootstrap stock cache with SHA-256 manifest;
- separate corporate-action cache and validator;
- stock-specific source documentation.

### Phase 2 evidence state

**Primary official NSE route:** blocked from hosted Actions runner. This remains issue #6.

**Alternate stock route:** green. Workflow run 35521951823 successfully acquired and validated the cached stock panel and corporate-action files.

**Current cache:** 30 NSE individual-stock EOD series, broadly 2010-01-04 to 2026-09-18 subject to each symbol's own listing history. The files include OHLCV/turnover and separate corporate-action histories. The cache is usable for engineering and exploratory forecasting, but not yet final stock-level evidence.

**Remaining stock-data gate:** build/verify price adjustment and point-in-time security identity/universe logic, and cross-check selected names against an independent Yahoo/yfinance-based dataset before running the main holdout.

## Phase 3 — TimesFM 3.0
**Engineering/unit-test gate green; statistical forecast gate can now be extended to individual-stock bootstrap data, while official NIFTY P0 remains blocked.**

The 3.0 branch includes:
- pinned TimesFM 3.0.2;
- TimesFM3Evaluator adapter;
- multivariate targets;
- past-only covariates;
- nine quantiles;
- forecast provenance schema;
- manual model-smoke workflow.

The existing NIFTY P1 results remain exploratory C-grade evidence. The new stock cache opens an additional bootstrap lane, but it does not replace the requirement for PIT-clean primary/independent validation before final claims.

## Phase 4 — Strategy research
**Engineering bootstrap complete; individual-stock strategy lane explicitly added; empirical gate depends on stock-data quality + forecast/cost gates.**

Individual stocks are first-class instruments. Current strategy hypotheses include:
- single-stock forecast overlays;
- cross-sectional ranking;
- uncertainty-conditioned sizing;
- stock-vs-index residuals;
- corporate-event-aware stock research.

The common engine still requires PIT integrity, realistic costs/slippage, walk-forward stability and multiple-testing control.

## Phase 5 — Options
**Protocol/engineering bootstrap complete; empirical testing blocked by authorized historical option data.**

## Phases 6–9
**Engineering tracks exist and are being maintained; empirical promotion remains downstream of data/forecast/cost gates.**

No strategy has passed a final empirical promotion gate. No live/paper execution path has been enabled.

## Review checkpoints

- Phase 2 draft PR #1: data/PIT infrastructure.
- Phase 3 draft PR #2: TimesFM 3.0 forecast-gate infrastructure.
- Phase 4 draft PR #3: strategy infrastructure.
- Phase 5 draft PR #5: options infrastructure.
- Issue #6: official NSE hosted-runner P0 blocker.

## Current provisional conclusion

The current evidence still does **not** establish standalone directional TimesFM alpha. The most defensible research hypothesis remains to use forecast distribution/uncertainty as a conditioning variable around an independently specified stock-selection or market-structure signal, and test the combination against identical no-TimesFM controls.

The individual-stock lane is now operational at the EOD bootstrap level, so the next scientific step is to reconcile corporate actions/identifier history and run the same frozen forecast matrix across a PIT stock cross-section before any strategy promotion.
