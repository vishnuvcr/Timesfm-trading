# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible NSE trading pipeline covering scalping, intraday, BTST, swing and options strategies.

**Research start:** 2026-09-20 (IST)  
**Repository state at start:** empty repository; no prior code, datasets, workflows or research files were found.

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Complete** |
| 1 | Literature + evidence review | **In progress — protocol being frozen** |
| 2 | NSE data lake and point-in-time controls | Planned |
| 3 | TimesFM baseline/gate by horizon | Planned |
| 4 | Strategy research: scalping/intraday/BTST/swing | Planned |
| 5 | Options research + IV/OI/Greeks | Planned |
| 6 | Cross-market/regime/news/corporate-action features | Planned |
| 7 | Cost/slippage/tax-aware walk-forward backtests | Planned |
| 8 | Paper-trading/live readiness + monitoring | Planned |
| 9 | Final manuscript + reproducible release | Planned |

All ten phase branches exist and have manual GitHub Actions entry points. The phase workflows are intentionally small at bootstrap; strategy/data jobs will be added only after the protocol is frozen.

## Core research question

Can TimesFM 2.5, used as a forecast and uncertainty engine rather than as a stand-alone buy/sell oracle, improve **net-of-cost, out-of-sample** trading performance on NSE across multiple holding horizons and market regimes?

TimesFM 3.0 is an evaluation-only benchmark while Google's current pretrained-weight terms restrict commercial/production use; TimesFM 2.5 is the practical deployable open-weight lane.

## Phase 1 preliminary conclusion

The literature does **not** justify assuming that zero-shot TimesFM is an NSE alpha engine. Recent financial TSFM work finds strong model rankings in some return-forecast tasks but small and sparse improvements over random-walk baselines. A 2026 base-rate-honest TimesFM study shows that raw directional accuracy can be dominated by the market up-rate. An independent 2026 NSE-inclusive TimesFM benchmark reports a negative directional gate for its Indian-equity zero-shot test and explores uncertainty-driven volatility sizing.

Therefore the experiment is explicitly **gate-first**:
forecast skill -> calibrated uncertainty -> net economic edge -> execution feasibility -> promotion.

A failure of direct directional skill does not automatically terminate the research. The fallback branches test volatility/risk sizing, regime filtering, execution timing, and forecast-range versus option-implied-move comparisons.

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

## Market data scope

The data lake will prioritize NSE primary sources for cash and derivatives history, option chain/OI, corporate actions, market timing and participant/FII/FPI/DII reports. It will also include India VIX, global benchmark/lead-lag variables, USDINR, rates, crude, gold, market breadth and timestamped events/news where a point-in-time historical source is available.

GIFT NIFTY is a planned cross-market feature because NSE IX documents long trading hours spanning the Indian pre-open/overnight period. BSE/NSE cross-exchange effects will be tested only where timestamped data are sufficiently granular.

## Execution realism

Paytm Money is the primary broker cost reference for the project. Current official material must be treated as the source of record for account-specific brokerage and current statutory/exchange charges; historical broker pages are retained only to explain legacy fee cohorts. Options are modeled at contract level, including spread, slippage, Greeks, expiry/settlement and applicable tax/charge mechanics.

## Decision principle

The project will not assume that a forecast implies a trade. A forecast must create economically useful information after costs, or it will be repurposed toward volatility/risk sizing, execution timing, or regime detection.

## Important limitation

No live trading claim is made at initialization. The repo currently contains **research plans and early evidence synthesis**, not a validated trading strategy.
