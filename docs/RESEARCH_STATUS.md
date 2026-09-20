# Research status

Updated: 2026-09-20 IST

## Scope decision — 2026-09-20
**Confirmed:** TimesFM 3.0 stays the primary model for all phases because this project is research for deriving and testing a trading strategy, not actually trading.

The scope is now explicitly **non-executing scientific research**:
- strategy hypotheses may be generated and falsified;
- full cost/slippage/tax-aware simulated backtests are allowed;
- no broker execution, production deployment, client-facing trading decision or revenue-generating use is part of the project;
- TimesFM 2.5 is a benchmark/ablation model only.

The current official 3.0 license permits qualifying non-commercial research/evaluation but excludes commercial/production use and commercial decision-making, so the repository treats this boundary as a hard governance control. citeturn341680search0

## Phase 0 — Governance
**Complete for bootstrap.**

## Phase 1 — Literature
**Complete / protocol frozen.**

Model decision:
- TimesFM 3.0 primary scientific/evaluation model throughout the research.
- TimesFM 2.5 benchmark/ablation only.
- Direct direction is only one hypothesis; uncertainty, volatility, multivariate inputs and causal covariates are explicit research targets.
- The current 3.0 pretrained-weight license is a hard gate: 3.0 outputs cannot be used to select/optimize/operate a revenue-generating trading strategy without commercial permission. See [LICENSE_GATE](LICENSE_GATE.md).

New options evidence:
A September 2026 pre-registered SPY implied-volatility study found TimesFM-3 forecast-loss advantages that narrowed after recalibration; the market's own forward-variance forecast beat the model at ATM nodes, while a residual wing signal survived statistical controls. The study stopped before economic/fill testing. This strengthens the Phase 5 requirement to compare TimesFM against market-implied forecasts and execute a full option P&L backtest before any conclusion.

## Phase 2 — Data
**Validation green; official public P0 acquisition blocked; authorized/alternate official delivery required.**

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
- GitHub Actions validation run 30: source registry, manifest validation and data-layer tests passed;
- direct container clone could not run because github.com DNS was unavailable; logged as environment limitation.

Current Phase 2 gate:
The public NIFTY Indices route has been attempted four times from GitHub Actions and consistently returns the NIFTY Indices HTML page with HTTP 200 rather than JSON. The retry loop is closed and tracked in [issue #6](https://github.com/vishnuvcr/Timesfm-trading/issues/6). An authorized/alternate official data-delivery route is now required for the primary P0 dataset.

## Phase 3 — TimesFM 3.0
**Engineering/unit-test gate green; statistical forecast gate blocked by real P0 acquisition.**

The phase-3 branch now includes:
- pinned TimesFM 3.0.2 research environment;
- native TimesFM3Evaluator adapter;
- multivariate targets;
- past-only covariates;
- nine quantile outputs;
- forecast provenance schema;
- manual model smoke workflow.

The official TimesFM README confirms the 3.0 evaluator supports univariate and multivariate forecasting, past-only and past-future covariates, and nine quantiles. citeturn341680search8turn341680search1

CI verification is green: the statistics/adapter unit suite passes. The P1 TimesFM 3.0 bootstrap completed successfully on secondary data and showed lower point forecast error than persistence but directional accuracy below the positive-return base rate. A second P1 ablation compared univariate, native multivariate and past-only covariate inputs: multivariate slightly worsened point error while raising direction to 72.5%, and the past-only covariate condition matched univariate metrics in that run. These are exploratory C-grade observations only; the primary forecast gate still requires P0 data.

## Frozen experiment design

The primary experiment matrix is now frozen in [docs/EXPERIMENT_MATRIX.md](docs/EXPERIMENT_MATRIX.md), including targets, horizons, input families, baselines, primary metrics, multiple-testing controls and promotion gates.

## Cross-phase architecture
**Specified.**

The common trading engine is documented in [docs/TRADING_PIPELINE_SPEC.md](docs/TRADING_PIPELINE_SPEC.md). All five strategy families use the same forecast, calibration, economic-edge, risk, execution and monitoring gates.

The dated 2026 cost model is frozen in [docs/COST_MODEL.md](docs/COST_MODEL.md); current NSE STT and Paytm Money F&O/RMS assumptions are versioned by effective date.

## Phase 4 — Strategy research
**Engineering bootstrap complete; empirical testing blocked by frozen P0 data and Phase 3 forecast gate.**

Phase 4 now includes non-executing shared research rules for cost hurdles, uncertainty-adjusted sizing and volatility-targeted exposure. Phase 4 CI run 35 passed.

## Phase 5 — Options
**Protocol/engineering bootstrap complete; empirical testing blocked by authorized historical option data.**

Phase 5 now includes a formal implied-move benchmark, residual-vs-cost gate and defined-risk spread accounting. Corrected options CI run 38 passed.

No live or paper order execution is planned. No strategy has passed an empirical research gate.


## Review checkpoints

Draft PR #1 contains Phase 2 data-lake/PIT infrastructure; draft PR #2 contains Phase 3 TimesFM 3.0 forecast-gate infrastructure. Neither is merged because their empirical phase gates are not yet complete.


## License interpretation correction

The official 3.0 license is more restrictive than the earlier project notes implied: Non-Commercial Purpose explicitly excludes revenue-generating activity and commercial decision-making, and restrictions extend to outputs. This is now treated as a hard governance gate, not a deployment-afterthought. citeturn670140view0


## License checkpoint

Open issue #4 remains the future commercial-permission tracker. It is not a blocker for the current non-executing research scope, but becomes a hard blocker if project scope ever changes to commercial/production use.
