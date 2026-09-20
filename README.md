# TimesFM Trading — NSE Research Program

Research program to evaluate Google TimesFM for a reproducible Indian-market trading research pipeline covering **individual stocks, scalping, intraday, BTST, swing and options**.

**Research start:** 2026-09-20 (IST)

## Current status

| Phase | Scope | Status |
|---|---|---|
| 0 | Governance, reproducibility, repo bootstrap | **Complete** |
| 1 | Literature + evidence review | **Complete / protocol frozen** |
| 2 | NSE/BSE data lake + PIT controls | **Validation green; official NSE hosted-runner routes blocked; alternate individual-stock EOD lane green** |
| 3 | TimesFM 3.0 forecast gates | **Engineering green; NIFTY P0 blocked; 30-stock recent-window bootstrap and four-fold robustness extension complete; no stock alpha promoted** |
| 4 | Individual-stock + index strategy research | **Phase 4.1 stock overlay tested; simple TimesFM-only/hybrid selection rejected; conditional stock-signal research next** |
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

## Source expansion after the blocker

The alternate-source search has now been widened beyond daily EOD feeds. A published Hugging Face 1-minute NSE dataset reports roughly 715 million rows across 2,500+ stocks/indices for 2022–2026 and is marked MIT; this is being treated as a **candidate intraday/scalping cross-check**, not as exchange-primary truth. A separate CC-BY-4.0 Hugging Face hourly dataset covers NIFTY/Bank NIFTY/India VIX and futures for 2017–2021 and is being retained for historical intraday methodology cross-checks. Older Kaggle NSE panels and GitHub hourly/daily archives remain benchmark/diagnostic sources until provenance, licensing, PIT and adjustment rules are frozen.

See the [expanded alternate data-source policy](docs/ALTERNATE_DATA_SOURCES.md) for the source hierarchy and promotion rules.

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

The current stock-level gate is now incremental-information research: TimesFM must add value to an independently specified stock-selection signal after regime/liquidity/event conditioning. The standalone and simple hybrid stock overlays have failed the exploratory gate. High-frequency claims remain gated on intraday-source and execution-quality validation.


## Latest stock research result — 2026-09-20

The repaired 30-stock TimesFM 3.0 bootstrap completed successfully, followed by a four-fold chronological robustness extension covering 4,800 stock-level forecast origins. The recent-window bootstrap showed +11.1 percentage points mean directional excess, but the broader four-fold test reversed this to -2.9 percentage points. TimesFM was worse than persistence on point-error aggregates in both tests, and no stock had a negative mean MAE difference across all four folds.

This is now treated as a **negative result for standalone stock TimesFM forecasting against persistence on the bootstrap**. The next empirical question is incremental value around an independent stock-selection/market-structure signal, with PIT controls and full cost/slippage modeling.


## Phase 4.1 stock-selection checkpoint

The first explicit individual-stock strategy experiment is complete and synchronized into main. Across 30 bootstrap stocks and 32 non-overlapping five-session rebalances, the independent 20-session momentum control had mean rank IC +0.0138, TimesFM had -0.0237, and the 50/50 hybrid had -0.0151. Under the lowest tested proportional-cost stress, TimesFM-only net total return was about -26.6%, versus -15.2% for momentum and -21.8% for the hybrid.

This is an exploratory negative result, not the final Phase 7 walk-forward verdict. The research now tests only whether TimesFM contributes incremental conditional information after regime, liquidity, event and market-state controls.


## Individual-stock strategy conclusion — 2026-09-20

Three layers of stock evidence were completed:
- TimesFM-only stock ranking;
- TimesFM plus independent momentum controls;
- nested regime-conditioned TimesFM-minus-momentum residual.

The four-fold forecast robustness test covered 4,800 stock origins. The final nested strategy test used prior-fold-only regime thresholds and failed against the momentum control at every tested cost scenario. No daily individual-stock TimesFM strategy is validated.

See [Individual-stock TimesFM gate conclusion](docs/INDIVIDUAL_STOCK_TIMESFM_GATE_CONCLUSION.md).


## Phase 4B active — 2026-09-20

Phase 4B now has a frozen multifrequency stock matrix on the dedicated `phase-4b-stock-multifrequency` branch. The immediate swing lane tests 2, 5, 10 and 20 sessions with TimesFM 3.0 versus a 20-session momentum control and a predeclared uncertainty-scaled momentum mechanism. Genuine BTST/intraday/scalping remains gated on validation of the candidate 1-minute source.

See:
- `docs/PHASE_4B_STATUS.md`
- `docs/PHASE_4B_EXPERIMENT_MATRIX.md`
- `scripts/stock_timesfm_swing_p4b.py`
- `scripts/validate_intraday_source_p4b.py`
- `.github/workflows/phase-4b-stock-multifrequency.yml`
