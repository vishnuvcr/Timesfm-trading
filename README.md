# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible NSE trading pipeline covering scalping, intraday, BTST, swing and options strategies.

**Research start:** 2026-09-20 (IST)  
**Repository state at start:** empty repository; no prior code, datasets, workflows or research files were found.

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Complete** |
| 1 | Literature + evidence review | **In progress — 3.0 selected** |
| 2 | NSE data lake and point-in-time controls | Planned |
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

Google's current official documentation says TimesFM 3.0 adds native multivariate forecasting and flexible past-only and past-and-future covariate support. The source code in the main TimesFM repository is Apache-2.0, but the pretrained 3.0 weights are distributed under a separate TimesFM Non-Commercial License v1.0. That license permits testing, evaluation and research that is not tied to commercial gain, production deployment or revenue generation; commercial or production use requires separate permission/license from Google.

Therefore:
- **3.0 research/backtesting: YES — primary lane.**
- **3.0 paper trading/simulation for research: YES, provided it remains within the license.**
- **3.0 live/production trading: NOT yet cleared by the current pretrained-weight license; licensing must be resolved first.**
- **2.5:** retained as a comparison model and possible production fallback if necessary.

The licensing issue is a deployment constraint, not a reason to exclude 3.0 from this research program.

## Research controls

Every strategy must pass:

1. Point-in-time data and no look-ahead.
2. Walk-forward validation with untouched test windows.
3. Explicit baselines (persistence, market/sector benchmark, simple technical/statistical baselines).
4. Transaction costs, brokerage, exchange charges, statutory taxes and realistic slippage.
5. Turnover/liquidity constraints and order-fill assumptions.
6. Multiple-testing controls where many variants are searched.
7. Regime and sub-period reporting.
8. Reproducible cached inputs, model/version hashes and run manifests.
9. A pre-registered promotion gate before any paper/live step.
10. A complete error log and experiment log.

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

## Phase 1 preliminary conclusion

The literature does not justify assuming that any TimesFM version is automatically an NSE alpha engine. Recent financial TSFM work finds model rankings that can look strong while gains over random-walk baselines remain small and sparse. A 2026 base-rate-honest TimesFM study shows that raw directional accuracy can be dominated by the market up-rate. An independent 2026 NSE-inclusive TimesFM benchmark reports a negative directional gate for zero-shot TimesFM 2.5 on Indian equities and explores uncertainty-driven volatility sizing.

For this project, 3.0 will be tested more broadly rather than assuming it fixes those problems.

The experimental sequence is:

**3.0 forecast → calibration → multivariate/covariate conditioning → net economic edge → execution feasibility → risk/sizing → promotion**

A failure of direct directional skill does not automatically terminate the research. Fallback branches test volatility/risk sizing, regime filtering, execution timing, and forecast-range versus option-implied-move comparisons.

## Market data scope

The data lake will prioritize NSE primary sources for cash and derivatives history, option chain/OI, corporate actions, market timing and participant/FII/FPI/DII reports. It will also include India VIX, global benchmark/lead-lag variables, USDINR, rates, crude, gold, market breadth and timestamped events/news where a point-in-time historical source is available.

## Execution realism

Paytm Money is the primary broker cost reference for the project. Current official material must be treated as the source of record for account-specific brokerage and current statutory/exchange charges. Options are modeled at contract level, including spread, slippage, Greeks, expiry/settlement and applicable tax/charge mechanics.

## Important limitation

No live trading claim is made. The repo currently contains **research plans and early evidence synthesis**, not a validated trading strategy.
