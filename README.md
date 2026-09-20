# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible NSE trading pipeline covering scalping, intraday, BTST, swing and options strategies.

**Research start:** 2026-09-20 (IST)  
**Repository state at start:** empty repository; no prior code, datasets, workflows or research files were found.

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Complete** |
| 1 | Literature + evidence review | **Complete / protocol frozen** |
| 2 | NSE data lake and point-in-time controls | **Validation green; official public P0 acquisition blocked** |
| 3 | TimesFM 3.0 baseline/gate by horizon | **Engineering + unit-test gate green; real forecast blocked by P0 data acquisition** |
| 4 | Strategy research: scalping/intraday/BTST/swing | **Engineering bootstrap complete; empirical gate blocked by P0/Phase 3** |
| 5 | Options research + IV/OI/Greeks | **Protocol/engineering bootstrap complete; empirical gate blocked by authorized options data** |
| 6 | Cross-market/regime/news/corporate-action features | Planned |
| 7 | Cost/slippage/tax-aware walk-forward simulation | Planned |
| 8 | Simulation readiness + monitoring | Planned |
| 9 | Final manuscript + reproducible release | Planned |

All ten phase branches exist and have manual GitHub Actions entry points.

## Core model decision

**TimesFM 3.0 is the primary scientific/evaluation model for the entire project.** TimesFM 2.5 is retained only as a benchmark/ablation model.

Google's current official documentation says TimesFM 3.0 adds native multivariate forecasting and flexible past-only and past-and-future covariate support. The project is intentionally **research-only and non-executing**. We will derive and test strategy hypotheses, perform cost/slippage-aware simulations, and quantify uncertainty, but we will not place trades, connect a broker for execution, operate a production strategy, or use TimesFM 3.0 outputs for commercial decision-making within this project. citeturn670140view0 citeturn498629view0turn388765search3

## License gate

Commercial-license tracking issue: https://github.com/vishnuvcr/Timesfm-trading/issues/4

See [TimesFM 3.0 license gate](docs/LICENSE_GATE.md). Under the current scope, the issue is a future-scope tracker rather than a blocker for non-executing scientific research.

## Phase 1 result

The protocol is frozen around a gate-first sequence:

**3.0 forecast → calibration → multivariate/covariate conditioning → net simulated economic edge → execution simulation → risk/sizing → manuscript-level promotion**

Direct directional forecasting is not assumed to be the only useful output. Volatility, uncertainty, regime filters, execution timing and option-implied-versus-forecast range remain first-class hypotheses.

Recent finance-specific evidence reinforces that design. Financial TSFM benchmarks report small/sparse gains over random-walk baselines; a base-rate-honest TimesFM study shows raw directional accuracy can be misleading; and a September 2026 pre-registered TimesFM-3 study on the SPY implied-volatility surface found forecast-loss gains that narrowed after calibration, with the market's forward-variance forecast beating TimesFM at ATM nodes and no economic/fill test being run. citeturn130125academia13turn130125academia14turn290367search0

## Frozen experiment matrix

[Experiment matrix](docs/EXPERIMENT_MATRIX.md) fixes the primary target families, horizon families, input families, baselines, statistical metrics and promotion gates before strategy results are observed.

## Phase 2 result so far

The data architecture is now defined around:
- official NSE/BSE source registry;
- point-in-time metadata;
- immutable dataset manifests;
- licensing-aware public/private storage tiers;
- synthetic leakage tests;
- a manual GitHub Actions validation workflow.

The public repository will not redistribute restricted exchange raw data. Public files contain schemas, manifests, checksums, derived aggregates and permitted fixtures; licensed raw feeds are referenced by hash and stored privately.

NSE's official ecosystem provides security-wise archives, historical index/VIX data, F&O UDiFF/common bhavcopy reports, participant OI/volume, FII/FPI/DII reports, corporate actions, and licensed historical trade/order products. citeturn209752search0turn173596search2turn209752search3turn676787search6turn676787search0

The public option-chain interface exposes OI, change in OI, volume, IV, LTP and bid/ask, but its terms restrict copying/aggregation; the research therefore treats an authorized historical options dataset as mandatory for Phase 5. citeturn173596search1

Community GitHub/Kaggle/Hugging Face datasets are catalogued as secondary validation/bootstrapping sources, never as the primary exchange truth. citeturn325482search0turn325482search1turn325482search2turn325482search9

## Phase 3 engineering result

The 3.0 branch now contains:
- pinned TimesFM 3.0.2 research environment;
- a thin adapter around Google's TimesFM3Evaluator;
- multivariate targets;
- past-only covariates;
- nine native quantiles;
- a forecast-record provenance schema;
- a manual model-smoke workflow.

Phase 3 unit/statistics CI is green; the actual statistical forecast gate remains blocked until Phase 2 supplies a frozen P0 dataset.

## Repository map

- [Research plan](docs/RESEARCH_PLAN.md)
- [Research status](docs/RESEARCH_STATUS.md)
- [Experiment matrix](docs/EXPERIMENT_MATRIX.md)
- [Trading pipeline specification](docs/TRADING_PIPELINE_SPEC.md)
- [Methodology](docs/METHODOLOGY.md)
- [Literature review](docs/LITERATURE_REVIEW.md)
- [Data catalog](docs/DATA_CATALOG.md)
- [Cost model](docs/COST_MODEL.md)
- [Strategy matrix](docs/STRATEGY_MATRIX.md)
- [Error log](docs/ERROR_LOG.md)
- [Chat/decision log](docs/CHAT_LOG.md)
- [Project instructions](PROJECT_INSTRUCTIONS.md)
- [Phase 2 branch status](https://github.com/vishnuvcr/Timesfm-trading/blob/phase-2-data/docs/PHASE_2_STATUS.md)
- [Phase 2 source registry](https://github.com/vishnuvcr/Timesfm-trading/blob/phase-2-data/configs/source_registry.json)
- [Phase 3 branch status](https://github.com/vishnuvcr/Timesfm-trading/blob/phase-3-timesfm-gate/docs/PHASE_3_STATUS.md)
- [Draft PR #1 — Phase 2](https://github.com/vishnuvcr/Timesfm-trading/pull/1)
- [Draft PR #2 — Phase 3](https://github.com/vishnuvcr/Timesfm-trading/pull/2)
- [Draft PR #3 — Phase 4](https://github.com/vishnuvcr/Timesfm-trading/pull/3)
- [Draft PR #5 — Phase 5](https://github.com/vishnuvcr/Timesfm-trading/pull/5)
- [Issue #6 — Official NIFTY P0 acquisition blocker](https://github.com/vishnuvcr/Timesfm-trading/issues/6)

## Market data scope

The data lake will cover NSE cash equity, NIFTY-family indices, futures/options, India VIX, FII/FPI and DII, option-chain/OI/IV/skew, corporate actions, global lead/lag variables, GIFT NIFTY, BSE cross-exchange data, USDINR, rates, crude, gold, breadth and timestamped events/news.

## Execution realism

Paytm Money is the primary broker cost reference for the project. These costs are used only in **simulated execution and economic-value analysis**; there is no broker order routing in the project. Current official material is reconciled by effective date; simulations model brokerage, exchange/statutory charges, taxes, spread, slippage, impact, financing and instrument-specific settlement.

## Important limitation

No live trading claim is made. The repository contains a frozen research protocol, active data/model engineering, and a non-executing strategy research pipeline—not a validated trading strategy or a deployment system.


## Current research conclusion

- [Provisional research conclusion and strategy hypothesis](docs/PROVISIONAL_RESEARCH_CONCLUSION.md)
- [P1 TimesFM 3.0 forecast result](../phase-3-timesfm-gate/docs/P1_BOOTSTRAP_RESULT.md)
- [P1 multivariate/covariate ablation](../phase-3-timesfm-gate/docs/P1_MULTIVARIATE_ABLATION.md)
- [Official NSE data-access blocker — Issue #6](https://github.com/vishnuvcr/Timesfm-trading/issues/6)
