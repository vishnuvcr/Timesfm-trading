# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible NSE trading pipeline covering scalping, intraday, BTST, swing and options strategies.

**Research start:** 2026-09-20 (IST)  
**Repository state at start:** empty repository; no prior code, datasets, workflows or research files were found.

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Initialized** |
| 1 | Literature + evidence review | **In progress** |
| 2 | NSE data lake and point-in-time controls | Planned |
| 3 | TimesFM baseline/gate by horizon | Planned |
| 4 | Strategy research: scalping/intraday/BTST/swing | Planned |
| 5 | Options research + IV/OI/Greeks | Planned |
| 6 | Cross-market/regime/news/corporate-action features | Planned |
| 7 | Cost/slippage/tax-aware walk-forward backtests | Planned |
| 8 | Paper-trading/live readiness + monitoring | Planned |
| 9 | Final manuscript + reproducible release | Planned |

## Core research question

Can TimesFM 2.5, used as a forecast and uncertainty engine rather than as a stand-alone buy/sell oracle, improve **net-of-cost, out-of-sample** trading performance on NSE across multiple holding horizons and market regimes?

TimesFM 3.0 will be treated as an evaluation-only benchmark because Google currently distributes the 3.0 pretrained weights under a non-commercial/non-production license; TimesFM 2.5 weights remain Apache-2.0. See [research plan](docs/RESEARCH_PLAN.md).

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

## Key evidence already found

Google describes TimesFM as a general time-series foundation model, not a stock-specific trading model. TimesFM 3.0 adds native multivariate and covariate support, but its pretrained weights are currently non-commercial/non-production. Independent 2026 research on financial returns reports that TimesFM-family models can rank well against other forecasting models while producing only sparse/small improvements over random-walk baselines; a separate base-rate-honest TimesFM study reports no directional skill over naive baselines in broad US and Indian equity tests. These results are evidence for a rigorous **gate-first** design, not proof that NSE intraday or options use cases cannot work.

Official NSE sources will be preferred for market mechanics, derivatives contracts, option-chain and FII/FPI/DII data. Paytm Money's current pricing page states statutory/exchange charges are levied at actuals and its published historical/current materials must be reconciled before the final cost model is frozen.

## Decision principle

The project will not assume that a forecast implies a trade. A forecast must create economically useful information after costs, or it will be repurposed toward volatility/risk sizing, execution timing, or regime detection.

## Important limitation

No live trading claim is made at initialization. The repo currently contains **research plans and evidence**, not a validated trading strategy.
