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

## Phase 2 — Data
**In progress.**

Completed on branch `phase-2-data`:
- point-in-time data policy;
- official source registry;
- dataset manifest schema;
- manifest validator;
- synthetic future-information rejection test;
- manual GitHub Actions validation workflow;
- official source audit for NSE historical reports, UDiFF, India VIX, FII/FPI/DII, corporate actions, paid historical trade/order data, GIFT NIFTY and BSE data.

Validation:
- local offline manifest validation: passed;
- PIT rejection test: passed;
- pytest: 2 passed;
- direct container clone could not run because github.com DNS was unavailable; logged as environment limitation.

Current Phase 2 gate:
Acquire/connect real P0 datasets and produce first real frozen manifests. Then run schema, PIT, calendar, corporate-action, derivatives lifecycle and option-quote integrity tests.

## Phase 3 onward
**Planned.**

No live strategy has passed a research gate.
