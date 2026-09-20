# Research status

Updated: 2026-09-20 IST

## Phase 0 — Governance
**Complete for bootstrap.**

## Phase 1 — Literature
**In progress — model choice updated.**

### Current model decision
**TimesFM 3.0 is now the primary model for research.** TimesFM 2.5 is the benchmark/ablation model.

Reason:
- 3.0 adds native multivariate forecasting.
- 3.0 supports past-only and past-and-future covariates.
- 3.0 is the model selected for this research.
- Controlled research/backtesting is compatible with its current non-commercial/non-production license when it remains genuinely research/evaluation use.

Restriction:
The current pretrained 3.0 weights are not licensed for commercial or production use. Therefore the final live-deployment phase must either obtain a separate commercial license/permission from Google or use separately licensed weights for production. This does not prevent a 3.0 research/backtest program.

## Phase 2 — Data
**Planned.**

First data gate:
point-in-time integrity, timestamp normalization, corporate-action handling, contract lifecycle/roll handling, option liquidity filters, and immutable manifests.

## Phase 3 onward
**Planned.**

No live strategy has passed a research gate.
