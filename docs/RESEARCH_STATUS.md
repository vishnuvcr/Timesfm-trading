# Research status

Updated: 2026-09-20 IST

## Phase 0 — Governance
**Complete for bootstrap.**

## Phase 1 — Literature
**Complete / protocol frozen.**

Model decision:
- TimesFM 3.0 primary.
- TimesFM 2.5 benchmark/ablation/fallback.
- Direct direction is only one hypothesis; uncertainty, volatility, multivariate inputs and causal covariates are explicit research targets.
- Deployment licensing is a later gate, not a reason to exclude 3.0 from research.

New options evidence:
A September 2026 pre-registered SPY implied-volatility study found TimesFM-3 forecast-loss advantages that narrowed after recalibration; the market's own forward-variance forecast beat the model at ATM nodes, while a residual wing signal survived statistical controls. The study stopped before economic/fill testing. This strengthens the Phase 5 requirement to compare TimesFM against market-implied forecasts and execute a full option P&L backtest before any conclusion.

## Phase 2 — Data
**In progress.**

Completed on branch `phase-2-data`:
- point-in-time data policy;
- official source registry;
- community secondary-source registry;
- dataset manifest schema;
- manifest validator;
- synthetic future-information rejection test;
- manual GitHub Actions validation workflow;
- official-source audit for NSE historical reports, UDiFF, India VIX, FII/FPI/DII, corporate actions, paid historical trade/order data, GIFT NIFTY and BSE data.

Validation:
- local offline manifest validation: passed;
- PIT rejection test: passed;
- pytest: 2 passed;
- direct container clone could not run because github.com DNS was unavailable; logged as environment limitation.

Current Phase 2 gate:
Acquire/connect real P0 datasets and produce first real frozen manifests. Then run schema, PIT, calendar, corporate-action, derivatives lifecycle and option-quote integrity tests.

## Phase 3 — TimesFM 3.0
**Engineering bootstrap complete; statistical gate blocked by Phase 2.**

The phase-3 branch now includes:
- pinned TimesFM 3.0.2 research environment;
- native TimesFM3Evaluator adapter;
- multivariate targets;
- past-only covariates;
- nine quantile outputs;
- forecast provenance schema;
- manual model smoke workflow.

The official TimesFM README confirms the 3.0 evaluator supports univariate and multivariate forecasting, past-only and past-future covariates, and nine quantiles. citeturn498629view0

No real forecast result has been reported yet.

## Frozen experiment design

The primary experiment matrix is now frozen in [docs/EXPERIMENT_MATRIX.md](docs/EXPERIMENT_MATRIX.md), including targets, horizons, input families, baselines, primary metrics, multiple-testing controls and promotion gates.

## Phase 4 onward
**Planned.**

No live strategy has passed a research gate.
