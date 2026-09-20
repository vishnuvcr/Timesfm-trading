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
| 3 | TimesFM 3.0 baseline/gate by horizon | Planned |
| 4 | Strategy research: scalping/intraday/BTST/swing | Planned |
| 5 | Options research + IV/OI/Greeks | Planned |
| 6 | Cross-market/regime/news/corporate-action features | Planned |
| 7 | Cost/slippage/tax-aware walk-forward backtests | Planned |
| 8 | Paper-trading/live readiness + monitoring | Planned |
| 9 | Final manuscript + reproducible release | Planned |

All ten phase branches exist and have manual GitHub Actions entry points.

## Core model decision

**TimesFM 3.0 is the primary research model.** TimesFM 2.5 remains the benchmark/ablation/fallback model.

Google's current official documentation says TimesFM 3.0 adds native multivariate forecasting and flexible past-only and past-and-future covariate support. The source code in the main TimesFM repository is Apache-2.0, but the pretrained 3.0 weights are distributed under a separate TimesFM Non-Commercial License v1.0. That license permits qualifying testing, evaluation and research; commercial or production use of the pretrained weights requires separate permission/license from Google.

## Phase 1 result

The protocol is frozen around a gate-first sequence:

**3.0 forecast → calibration → multivariate/covariate conditioning → net economic edge → execution feasibility → risk/sizing → promotion**

Direct directional forecasting is not assumed to be the only useful output. Volatility, uncertainty, regime filters, execution timing and option-implied-versus-forecast range remain first-class hypotheses.

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

## Repository map

- [Research plan](docs/RESEARCH_PLAN.md)
- [Research status](docs/RESEARCH_STATUS.md)
- [Methodology](docs/METHODOLOGY.md)
- [Literature review](docs/LITERATURE_REVIEW.md)
- [Data catalog](docs/DATA_CATALOG.md)
- [Cost model](docs/COST_MODEL.md)
- [Strategy matrix](docs/STRATEGY_MATRIX.md)
- [Error log](docs/ERROR_LOG.md)
- [Chat/decision log](docs/CHAT_LOG.md)
- [Project instructions](PROJECT_INSTRUCTIONS.md)
- [Phase 2 status](https://github.com/vishnuvcr/Timesfm-trading/blob/phase-2-data/docs/PHASE_2_STATUS.md)
- [Phase 2 data policy](https://github.com/vishnuvcr/Timesfm-trading/blob/phase-2-data/docs/PHASE_2_DATA_POLICY.md)
- [Phase 2 source registry](https://github.com/vishnuvcr/Timesfm-trading/blob/phase-2-data/configs/source_registry.json)

## Market data scope

The data lake will cover NSE cash equity, NIFTY-family indices, futures/options, India VIX, FII/FPI and DII, option-chain/OI/IV/skew, corporate actions, global lead/lag variables, GIFT NIFTY, BSE cross-exchange data, USDINR, rates, crude, gold, breadth and timestamped events/news.

## Execution realism

Paytm Money is the primary broker cost reference for the project. Current official material is reconciled by effective date; backtests model brokerage, exchange/statutory charges, taxes, spread, slippage, impact, financing and instrument-specific settlement.

## Important limitation

No live trading claim is made. The repository currently contains a frozen research protocol and an active data-engineering framework, not a validated trading strategy.
