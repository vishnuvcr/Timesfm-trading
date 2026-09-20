# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible NSE trading pipeline covering scalping, intraday, BTST, swing and options strategies.

**Research start:** 2026-09-20 (IST)  
**Repository state at start:** empty repository; no prior code, datasets, workflows or research files were found.

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Complete** |
| 1 | Literature + evidence review | **Complete / protocol frozen** |
| 2 | NSE data lake and point-in-time controls | **In progress** |
| 3 | TimesFM 3.0 baseline/gate by horizon | **Engineering bootstrap complete; experiment blocked by Phase 2 gate** |
| 4 | Strategy research: scalping/intraday/BTST/swing | Planned |
| 5 | Options research + IV/OI/Greeks | Planned |
| 6 | Cross-market/regime/news/corporate-action features | Planned |
| 7 | Cost/slippage/tax-aware walk-forward backtests | Planned |
| 8 | Paper-trading/live readiness + monitoring | Planned |
| 9 | Final manuscript + reproducible release | Planned |

All ten phase branches exist and have manual GitHub Actions entry points.

## Core model decision

**TimesFM 3.0 is the primary scientific/evaluation model.** TimesFM 2.5 remains the benchmark and current trading/production research lane unless 3.0 commercial rights are obtained.

Google's current official documentation says TimesFM 3.0 adds native multivariate forecasting and flexible past-only and past-and-future covariate support. The source code in the main TimesFM repository is Apache-2.0, but the pretrained 3.0 weights are distributed under a separate TimesFM Non-Commercial License v1.0. That license permits only qualifying non-commercial/non-production use. It explicitly excludes revenue-generating activity and commercial decision-making and its restrictions extend to model outputs. Therefore this project blocks using pretrained 3.0 outputs to select, optimize or operate a profit-seeking trading strategy until appropriate commercial rights are obtained. citeturn670140view0 citeturn498629view0turn388765search3

## License gate

Commercial-license tracking issue: https://github.com/vishnuvcr/Timesfm-trading/issues/4

See [TimesFM 3.0 license gate](docs/LICENSE_GATE.md). The research lane and production/trading lane are now deliberately separated.

## Phase 1 result

The protocol is frozen around a gate-first sequence:

**3.0 forecast → calibration → multivariate/covariate conditioning → net economic edge → execution feasibility → risk/sizing → promotion**

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

The actual statistical gate is intentionally blocked until Phase 2 supplies a frozen P0 dataset.

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

## Market data scope

The data lake will cover NSE cash equity, NIFTY-family indices, futures/options, India VIX, FII/FPI and DII, option-chain/OI/IV/skew, corporate actions, global lead/lag variables, GIFT NIFTY, BSE cross-exchange data, USDINR, rates, crude, gold, breadth and timestamped events/news.

## Execution realism

Paytm Money is the primary broker cost reference for the project. Current official material is reconciled by effective date; backtests model brokerage, exchange/statutory charges, taxes, spread, slippage, impact, financing and instrument-specific settlement.

## Important limitation

No live trading claim is made. The repository currently contains a frozen research protocol and active data/model engineering, not a validated trading strategy.
