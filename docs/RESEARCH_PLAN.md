# Research plan

## Objective
Build and validate a consistent TimesFM-enabled NSE research/trading pipeline across scalping, intraday, BTST, swing and options strategies.

## Model policy
**TimesFM 3.0 is the primary research model for this project.** TimesFM 2.5 is retained as a benchmark, ablation and fallback engineering lane.

The project separates research/backtesting use of the 3.0 pretrained weights from production/live deployment. Under Google's current TimesFM Non-Commercial License v1.0, testing, evaluation and research are permitted when not tied to commercial gain, production deployment or revenue generation. Commercial or production use requires separate permission/license from Google.

This is a licensing constraint, not a technical objection to TimesFM 3.0.

### Hypotheses
- H1: TimesFM 3.0 forecasts add statistically and economically useful information after realistic costs.
- H2: Native multivariate and covariate support in 3.0 can improve conditional forecasting versus univariate input.
- H3: Even when directional skill is weak, 3.0 uncertainty/volatility can improve sizing, regime filters or execution timing.
- H4: Any deployable edge must survive point-in-time validation across regimes and cost assumptions.
- H5: 2.5 and 3.0 should be compared on identical frozen datasets, horizons and forecast origins.

## Phase 0 — governance and reproducibility
Create repo controls, plan, status model, logs, branch/workflow convention and citation ledger.

## Phase 1 — literature and evidence review
Determine what is known about TimesFM 3.0 in finance, multivariate/covariate forecasting, base-rate traps, leakage, adaptation, frequency/context constraints and realistic trading economics. Freeze the experimental protocol from evidence.

## Phase 2 — NSE data lake
Freeze cash OHLCV, corporate actions, index membership, futures, options chain/history, OI, IV/skew, India VIX, FII/FPI/DII, global benchmarks, rates/FX/commodities and timestamped news. Validate point-in-time integrity.

## Phase 3 — TimesFM 3.0 forecast gate
Run TimesFM 3.0 first and treat it as the primary model. Use identical-origin 2.5 runs as the benchmark.
Test:
- univariate vs native multivariate
- past-only vs past-and-future covariates where causally available
- multiple contexts and forecast horizons
- price, return, range and volatility targets
- quantile calibration

Baselines: persistence, drift, simple technical/statistical models and a lightweight supervised model.

Metrics: forecast error, excess direction, rank IC, quantile coverage, calibration, Diebold-Mariano comparisons and economic value after costs.

## Phase 4 — cash equity
### Scalping
Test only liquid instruments/time windows with credible intraday data and fill assumptions. Use 3.0 return/range/uncertainty as a feature/veto, with VWAP, spread proxy, realized vol and order-flow proxies.

### Intraday
Test trend, mean-reversion, breakout, volatility expansion, opening-range and VWAP timing.

### BTST
Model overnight gap and next-session return with global cues, India VIX and event filters. No next-morning information leakage.

### Swing
Test multi-day return/range and volatility; control sector/name concentration and events.

Only families surviving out-of-sample and cost sensitivity move to options.

## Phase 5 — options
Test delta-controlled directional structures, debit spreads, calendars/diagonals where data permit, volatility trades comparing forecast range with implied volatility, and defined-risk event structures.

Do not assume underlying forecast skill transfers to options P&L. Reprice historical contracts using IV/Greeks, OI, term structure, spreads, expiry/settlement and realistic fills. Evaluate theta, vega, gamma and gap risk.

## Phase 6 — regimes/external information
Condition tests on trend/range, India VIX, stress, expiry week, event days, FII/FPI/DII, global cues, USDINR, rates, crude, gold, breadth, corporate actions and timestamped news.

## Phase 7 — cost-aware walk-forward
Use rolling/expanding walk-forward, nested tuning, realistic and stressed costs, slippage sensitivity, turnover/participation caps, tax/financing treatment, bootstrap/paired tests, FDR, year/regime breakdowns and capacity stress.

## Phase 8 — paper/live readiness
Paper execution, audit trail, kill switches, model/data drift monitors, broker/API failure handling and reconciliation.

**3.0 deployment gate:** no live/production use of Google's pretrained 3.0 weights until the licensing position is explicitly resolved. The research may finish with a 3.0-based strategy candidate and then either obtain permission/license or port the demonstrated method to appropriately licensed weights for production.

## Phase 9 — manuscript/release
Complete manuscript with abstract, introduction, literature, questions, aims/objectives, scientific methodology, data, results, inference, discussion, strengths/limitations, conclusion, future research, figures, tables, appendices and supplements.

## Stop rule
The program ends after Phase 9. Within each phase, weak branches stop at their gate rather than creating endless variants.
