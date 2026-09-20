# Research plan

## Objective

Build and scientifically validate a consistent TimesFM 3.0-enabled NSE research pipeline for deriving and evaluating trading-strategy hypotheses across scalping, intraday, BTST, swing and options domains. The project is explicitly non-executing: it will not place trades or operate a revenue-generating strategy.

## Model policy

**TimesFM 3.0 is the primary research/evaluation model.** TimesFM 2.5 is retained as the benchmark and currently usable trading/production lane.

### Critical license gate

Google's current TimesFM 3.0 pretrained-weight license grants use only for Non-Commercial Purposes. The license defines that term to exclude commercial gain, production deployment, revenue generation and use of outputs in commercial decision-making; it also prohibits use of the model or its outputs for commercial or production purposes. Accordingly, the current project scope is deliberately constrained to:
- non-commercial scientific research and reproducible forecasting evaluation;
- strategy-hypothesis generation and falsification;
- simulated/cost-aware backtesting and statistical inference;
- manuscript, figures, tables and research artifacts.

The project will **not**:
- place real trades or connect a broker for execution;
- operate a production trading system;
- use 3.0 outputs for commercial decision-making, paid services, client deliverables or revenue generation;
- claim that a simulated strategy is deployable merely because it passes a research backtest.

This is a research-governance interpretation, not legal advice. The license must be reviewed again if the project's purpose or distribution changes.

### Hypotheses
- H1: TimesFM 3.0 forecasts add statistically useful information on NSE after rigorous PIT validation.
- H2: Native multivariate and covariate support in 3.0 can improve conditional forecasting versus univariate input.
- H3: Even when directional skill is weak, 3.0 uncertainty/volatility can improve scientific understanding of risk forecasting.
- H4: Any deployable trading edge must survive point-in-time validation, realistic costs and multiple market regimes.
- H5: 2.5 and 3.0 should be compared on identical frozen datasets, horizons and forecast origins.
- H6: A simulated 3.0-derived strategy result should be treated as a research finding, not a deployment recommendation.

## Phase 0 — governance and reproducibility

Create repo controls, plan, status model, logs, branch/workflow convention and citation ledger.

## Phase 1 — literature and evidence review

Determine what is known about TimesFM 3.0 in finance, multivariate/covariate forecasting, base-rate traps, leakage, adaptation, frequency/context constraints and realistic trading economics. Freeze the experimental protocol from evidence.

## Phase 2 — NSE data lake

Freeze cash OHLCV, corporate actions, index membership, futures, options chain/history, OI, IV/skew, India VIX, FII/FPI/DII, global benchmarks, rates/FX/commodities and timestamped news. Validate point-in-time integrity.

## Phase 3 — TimesFM 3.0 forecast gate

Run TimesFM 3.0 as the primary scientific benchmark. Use identical-origin 2.5 runs as the practical benchmark.

Test:
- univariate vs native multivariate;
- past-only vs causally available future covariates;
- multiple contexts and forecast horizons;
- price, return, range and volatility targets;
- quantile calibration.

Baselines: persistence, drift, simple technical/statistical models and a lightweight supervised model.

Metrics: forecast error, excess direction, rank IC, quantile coverage, calibration, Diebold-Mariano comparisons and block-bootstrap uncertainty.

**No 3.0 forecast output from this phase may be promoted into a revenue-generating trading decision until the license gate is cleared.**

## Phase 4 — cash equity and individual-stock strategy research

Use the common strategy engine to derive and falsify simulated strategy hypotheses across **individual NSE-listed stocks as first-class instruments**, with indices used as market-state/baseline variables rather than the sole trading universe.

The final stock study must use point-in-time eligibility/liquidity rules and retain name/ISIN history where available. The current fixed 30-name stock panel is only an engineering/bootstrap cache.

### Individual stocks

Test single-stock forecast overlays, cross-sectional ranking, uncertainty-conditioned sizing, stock-vs-index residual returns and event-aware stock setups. Compare every TimesFM condition with a non-TimesFM baseline.

### Scalping
Test only liquid instruments/time windows with credible intraday data and fill assumptions. 3.0 remains the primary research model.

### Intraday
Test trend, mean-reversion, breakout, volatility expansion, opening-range and VWAP timing.

### BTST
Model overnight gap and next-session return with global cues, India VIX and event filters.

### Swing
Test multi-day return/range and volatility, with sector/name constraints.

Only strategy families surviving the forecast and cost gates proceed.

## Phase 5 — options

Test delta-controlled directional structures, debit spreads, calendars/diagonals where data permit, volatility trades comparing forecast range with implied movement, and defined-risk event structures.

Benchmark against the option market's own implied forecast. Do not infer option profitability from underlying forecast accuracy.

3.0 remains the primary scientific model; outputs remain non-executing research artifacts.

## Phase 6 — regimes/external information

Condition tests on trend/range, India VIX, stress, expiry week, event days, FII/FPI/DII, global cues, USDINR, rates, crude, gold, breadth, corporate actions and timestamped news.

## Phase 7 — cost-aware walk-forward

Use rolling/expanding walk-forward, nested tuning, realistic and stressed costs, slippage sensitivity, turnover/participation caps, tax/financing treatment, bootstrap/paired tests, FDR, year/regime breakdowns and capacity stress.

## Phase 8 — simulation readiness and monitoring

Build a non-executing paper/simulation harness with audit trails, reproducibility checks, data/model drift monitors, kill-switch logic for simulations, and reconciliation of simulated fills.

No broker order placement or live execution is part of this phase under the current research scope.

## Phase 9 — manuscript/release

Complete manuscript with abstract, introduction, literature, questions, aims/objectives, scientific methodology, data, results, inference, discussion, strengths/limitations, conclusion, future research, figures, tables, appendices and supplements.

## Stop rule

The program ends after Phase 9. Within each phase, weak branches stop at their gate rather than creating endless variants.

## Scope-change trigger

A future decision to trade, deploy, sell, provide client-facing signals, connect a broker for execution, or otherwise use 3.0 outputs in commercial decision-making is a material scope change and requires a license review plus a fresh end-to-end validation plan.


## Protocol amendment — Phase 4B multifrequency stock continuation — 2026-09-20

After the daily individual-stock TimesFM overlay gate closed, the research scope was extended to the already-declared multifrequency stock families in the frozen experiment matrix rather than reopening arbitrary daily thresholds. Phase 4B predeclared 2/5/10/20-session swing targets and separate BTST/intraday/scalping data gates.

The 10-session cross-sectional TimesFM ranking survived the bootstrap and cached PIT gates as a single candidate. It is now frozen for a post-selection Phase 7 holdout with exact cash-equity statutory/broker costs and slippage stress.

This amendment supersedes the earlier Phase 9 final-stop wording. Phase 9 manuscript/release remains deferred until the frozen candidate is resolved by the downstream cost-aware gate.
