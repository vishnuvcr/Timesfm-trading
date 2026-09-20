# Research plan

## Objective
Build and validate a consistent TimesFM-enabled NSE research/trading pipeline across scalping, intraday, BTST, swing and options strategies.

### Hypotheses
- H1: TimesFM forecasts add statistically and economically useful information after realistic costs.
- H2: Even when directional skill is weak, TimesFM uncertainty/volatility can improve sizing, regime filters or execution timing.
- H3: Any deployable edge must survive point-in-time validation across regimes and cost assumptions.

## Phase 0 — governance and reproducibility
Create repo controls, plan, status model, logs, branch/workflow convention and citation ledger.

## Phase 1 — literature and evidence review
Determine what is known about TimesFM in finance, base-rate traps, leakage, fine-tuning, frequency/context/covariates and realistic trading economics. Freeze the experimental protocol from evidence.

## Phase 2 — NSE data lake
Freeze cash OHLCV, corporate actions, index membership, futures, options chain/history, OI, IV/skew, India VIX, FII/FPI/DII, global benchmarks, rates/FX/commodities and timestamped news. Validate point-in-time integrity.

## Phase 3 — TimesFM forecast gate
Run TimesFM 2.5 first. Use TimesFM 3.0 only as an evaluation comparator while its current weight-license terms apply. Test multiple horizons and targets against persistence, drift and simple statistical/ML baselines. Measure forecast error, excess direction, rank IC, quantile coverage and economic value.

## Phase 4 — cash equity
### Scalping
Test only liquid instruments/time windows with credible intraday data and fill assumptions. Use TimesFM return/range/uncertainty as a feature/veto, with VWAP, spread proxy, realized vol and order-flow proxies.

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

## Phase 9 — manuscript/release
Complete manuscript with abstract, introduction, literature, questions, aims/objectives, scientific methodology, data, results, inference, discussion, strengths/limitations, conclusion, future research, figures, tables, appendices and supplements.

## Stop rule
The program ends after Phase 9. Within each phase, weak branches stop at their gate rather than creating endless variants.
