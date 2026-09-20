# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible Indian-market trading research pipeline covering **individual stocks, scalping, intraday, BTST, swing and options**.

**Research start:** 2026-09-20 (IST)

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Complete** |
| 1 | Literature + evidence review | **Complete / protocol frozen** |
| 2 | NSE/BSE data lake + PIT controls | **Validation green; official NSE hosted-runner routes blocked; alternate individual-stock EOD lane green** |
| 3 | TimesFM 3.0 forecast gates | **Engineering green; NIFTY P0 blocked; stock bootstrap extension now available** |
| 4 | Individual-stock + index strategy research | **Engineering bootstrap complete; empirical gate open only after stock data-quality/forecast/cost gates** |
| 5 | Options + IV/OI/Greeks | **Protocol/engineering bootstrap complete; empirical gate blocked by authorized historical option data** |
| 6 | Regimes/cross-market/news/corporate actions | **Engineering track active; empirical promotion downstream of data gates** |
| 7 | Cost/slippage/tax-aware walk-forward | **Engineering track active** |
| 8 | Simulation readiness/audit | **Engineering track active; non-executing only** |
| 9 | Final manuscript/release | **Engineering track active** |

All ten phase branches exist and have manual GitHub Actions entry points.

## Core model decision

**TimesFM 3.0 is the primary scientific/evaluation model.** TimesFM 2.5 remains a benchmark/ablation model.

The project is **research-only and non-executing**. It derives and falsifies strategy hypotheses, runs cost/slippage-aware simulations and produces manuscript-grade evidence. It does not place broker orders, operate production execution, or use TimesFM 3.0 outputs for commercial decision-making under the current license boundary.

## What changed after the NSE blocker

We did not keep retrying the same three blocked hosted-runner NSE endpoints.

Instead, the data program now has an **alternate individual-stock lane** based on TejHQ's published Indian-market EOD data, plus an independent Yahoo/yfinance-derived Hugging Face dataset for cross-checking. TejHQ states that its dataset is built from official NSE/BSE bhavcopy feeds and includes corporate actions, back-adjusted prices, symbol history and a point-in-time liquidity universe; the current public dataset is MIT-licensed. citeturn498069search2turn498069search8

The repository now has:
- a 30-name NSE bootstrap stock universe;
- cached per-stock EOD OHLCV/turnover files;
- separate corporate-action histories;
- SHA-256 manifests;
- validation code;
- a manual/push GitHub Actions acquisition workflow;
- a documented independent cross-check source;
- back-adjusted stock prices and a filtered point-in-time liquidity-universe table;
- a return-path cross-check summary for five liquid names. 

The current cache is **bootstrap evidence**, not a final claim of PIT/survivorship-safe stock performance. Individual-stock empirical testing must still reconcile identifier history, corporate actions, point-in-time universe membership and execution costs.

## Individual stocks are first-class strategy instruments

The strategy research explicitly includes:
- single-stock forecast overlays;
- cross-sectional forecast/residual ranking;
- uncertainty-conditioned position sizing;
- stock-vs-index and stock-vs-sector residual models;
- event-aware stock research;
- swing/BTST/intraday variants where validated data support the frequency.

The fixed 30-name list is only a bootstrap cache. Final evidence will use a point-in-time liquidity/membership universe and retain delisted/name-change history where data permit.

See [Individual-stock strategy design](docs/INDIVIDUAL_STOCK_STRATEGY_DESIGN.md) and [alternate data-source policy](docs/ALTERNATE_DATA_SOURCES.md).

## Research gate

The main scientific sequence remains:

**forecast → calibration → baseline comparison → economic-cost hurdle → walk-forward simulation → risk/sizing → regime stress → multiple-testing correction → manuscript promotion**

No directional TimesFM alpha has yet been established. The current provisional architecture is an uncertainty-conditioned overlay around an independently specified directional/selection signal.

## Data scope

The research lake covers:
NSE/BSE cash equities; NIFTY-family indices; futures/options; India VIX; FII/FPI/DII; option-chain/OI/IV/skew; corporate actions; global lead/lag variables; GIFT NIFTY; USDINR; rates; crude; gold; breadth; sector/regime features; timestamped corporate/news events.

## Execution realism

Paytm Money remains the reference brokerage/RMS source for simulation. Models must include brokerage, statutory charges/taxes, spread, slippage, impact, financing/holding costs and instrument-specific settlement. Scalping/intraday claims require intraday execution-quality data; daily OHLC alone is not enough to claim fill realism.

## Current research conclusion

- [Provisional research conclusion and strategy hypothesis](docs/PROVISIONAL_RESEARCH_CONCLUSION.md)
- [Research plan](docs/RESEARCH_PLAN.md)
- [Experiment matrix](docs/EXPERIMENT_MATRIX.md)
- [Research status](docs/RESEARCH_STATUS.md)
- [Data catalog](docs/DATA_CATALOG.md)
- [Alternate data sources](docs/ALTERNATE_DATA_SOURCES.md)
- [Error log](docs/ERROR_LOG.md)
- [Chat/decision log](docs/CHAT_LOG.md)
- [Official NSE access blocker — Issue #6](https://github.com/vishnuvcr/Timesfm-trading/issues/6)


## Stock-data validation checkpoint

The alternate stock lane is now green through raw prices, corporate actions, adjusted prices and PIT liquidity metadata. The independent source check found large level differences in some names, but those differences were consistent with adjustment conventions; overlapping daily raw-close return paths were extremely close in the five-name bootstrap, with at least 99.7% of daily return differences within 0.10 percentage points.

The next stock-level research gate is therefore not "find a different data source"; it is to freeze the PIT universe/identifier rules, reconcile corporate actions, and run the same pre-declared TimesFM forecast matrix across the stock cross-section.

