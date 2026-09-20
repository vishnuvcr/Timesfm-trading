# Research plan

## Objective

Build and validate a consistent TimesFM-enabled NSE trading pipeline across scalping, intraday, BTST, swing and options strategies.

## Model policy

**TimesFM 3.0 is the primary research/evaluation model.** TimesFM 2.5 is retained as the benchmark and currently usable trading/production lane.

### Critical license gate

Google's current TimesFM 3.0 pretrained-weight license grants use only for Non-Commercial Purposes. The license defines that term to exclude commercial gain, production deployment, revenue generation and use of outputs in commercial decision-making; it also prohibits use of the model or its outputs for commercial or production purposes. Therefore:

- TimesFM 3.0 can be used for qualifying academic/non-commercial evaluation and reproducible forecasting research.
- TimesFM 3.0 must **not** be used to select, optimize, or operate a revenue-generating trading strategy under the current pretrained-weight license.
- Before 3.0 outputs are used in a production or profit-seeking trading decision, obtain an appropriate commercial license from Google or use weights/model components with suitable commercial rights.
- The research repository keeps the 3.0 lane because it is scientifically valuable, but the promotion gate explicitly blocks 3.0-derived trading decisions until the license gate is cleared.

This is a licensing constraint, not a technical objection to TimesFM 3.0.

### Hypotheses
- H1: TimesFM 3.0 forecasts add statistically useful information on NSE after rigorous PIT validation.
- H2: Native multivariate and covariate support in 3.0 can improve conditional forecasting versus univariate input.
- H3: Even when directional skill is weak, 3.0 uncertainty/volatility can improve scientific understanding of risk forecasting.
- H4: Any deployable trading edge must survive point-in-time validation, realistic costs and multiple market regimes.
- H5: 2.5 and 3.0 should be compared on identical frozen datasets, horizons and forecast origins.
- H6: A 3.0 research result should be transferable to a separately licensed production model only if the transfer itself is scientifically demonstrated.

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

## Phase 4 — cash equity

Use the common strategy engine. For trading decisions, use a commercially permitted model lane.

### Scalping
Test only liquid instruments/time windows with credible intraday data and fill assumptions. Candidate 3.0 results remain scientific/evaluation only unless licensed.

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

3.0 may be used for non-commercial scientific evaluation; trading promotion requires a licensed production model.

## Phase 6 — regimes/external information

Condition tests on trend/range, India VIX, stress, expiry week, event days, FII/FPI/DII, global cues, USDINR, rates, crude, gold, breadth, corporate actions and timestamped news.

## Phase 7 — cost-aware walk-forward

Use rolling/expanding walk-forward, nested tuning, realistic and stressed costs, slippage sensitivity, turnover/participation caps, tax/financing treatment, bootstrap/paired tests, FDR, year/regime breakdowns and capacity stress.

## Phase 8 — paper/live readiness

Paper execution, audit trail, kill switches, model/data drift monitors, broker/API failure handling and reconciliation.

**3.0 deployment gate:** production/live trading using Google's pretrained 3.0 weights is blocked until explicit commercial permission/license is obtained. Otherwise, transfer the validated signal design to a commercially permitted model and revalidate end-to-end.

## Phase 9 — manuscript/release

Complete manuscript with abstract, introduction, literature, questions, aims/objectives, scientific methodology, data, results, inference, discussion, strengths/limitations, conclusion, future research, figures, tables, appendices and supplements.

## Stop rule

The program ends after Phase 9. Within each phase, weak branches stop at their gate rather than creating endless variants.
