# TimesFM 3.0 for Indian-Equity Trading Research: A Point-in-Time, Cost-Aware Evaluation

**Research program:** TimesFM Trading — NSE Research Program  
**Research date:** 20 September 2026 (IST)  
**Primary scientific model:** TimesFM 3.0 — google/timesfm-3.0-pytorch  
**Market focus:** NSE individual cash equities, with index/market-state and broader Indian-market features as contextual inputs  
**Execution status:** Non-executing research only

---

## Abstract

This study evaluates whether Google TimesFM 3.0 can provide statistically and economically useful information for Indian-equity trading research. The project was designed as a gate-first, point-in-time, cost-aware program covering individual stocks, indices, intraday/swing horizons, options, market regimes, corporate actions, institutional flows and global cross-market information. A major practical constraint was the inability of the hosted GitHub Actions environment to retrieve several official NSE historical routes. Rather than repeatedly retrying the same endpoints, the data program established an alternate individual-stock end-of-day lane based on TejHQ Indian-market data, independently cross-checked against Yahoo/yfinance-derived data. The study explicitly distinguishes alternate datasets from exchange-primary truth.

The individual-stock TimesFM research progressed through three empirical gates. First, a 30-stock five-session forecast bootstrap used a 128-session context and 40 recent chronological origins per stock. TimesFM was worse than persistence on mean log MAE (0.018675 vs 0.017629) and RMSE (0.027242 vs 0.025726), although a recent-window directional excess appeared. Second, a four-fold chronological robustness test expanded the evaluation to 4,800 stock-level origins. TimesFM remained worse than persistence on point error and the mean directional excess became negative (-2.90 percentage points), eliminating the recent directional finding as a robust result. Third, an explicit stock-selection experiment compared a 20-session momentum control with TimesFM ranking and a 50/50 hybrid across 32 rebalances. TimesFM's mean rank IC was -0.0237 versus +0.0138 for momentum, and the TimesFM-only and hybrid portfolios were weaker under multiple cost stresses.

A final regime-conditioned test asked whether TimesFM provided incremental information after trend, breadth, volatility, liquidity and post-corporate-action conditioning. The TimesFM residual had no statistically supported unconditional or regime-specific rank information after rebalance-level permutation testing and Benjamini-Hochberg false-discovery-rate control. A risk-on overlay produced a small zero-cost improvement over momentum but underperformed once a 0.25% one-way cost stress was introduced. On the declared promotion gate, no individual-stock TimesFM strategy survived.

The study therefore reaches a negative but actionable scientific conclusion: **the tested TimesFM 3.0 stock strategies do not demonstrate robust, cost-surviving incremental alpha on the available bootstrap evidence.** The result does not show that TimesFM is incapable of helping Indian-market research. It shows that simple TimesFM direction, uncertainty sizing, raw ranking and basic regime-conditioned overlays are not sufficient.

---

## 1. Introduction

Time-series foundation models promise general-purpose forecasting across heterogeneous domains. TimesFM 3.0, released by Google Research in August 2026, adds native multivariate forecasting and both past-only and past-and-future covariate support. Google reports strong performance on general forecasting benchmarks, but those benchmarks do not establish trading profitability. 

Financial markets create a particularly difficult forecasting environment. Prices are noisy, non-stationary, highly competitive and affected by market structure, costs, corporate actions, scheduled events, institutional flows, global markets and execution frictions. A lower forecast error therefore need not produce a positive trading expectancy.

The study was designed around a central principle:

> Forecasting value must be demonstrated as incremental information after a realistic trading baseline and realistic costs, not merely as lower forecast error.

The primary unit of trading research was an individual NSE-listed stock. Indices were retained as market-state and benchmark variables rather than treated as the sole trading instruments.

TimesFM 3.0 was selected as the primary scientific model. Its current pretrained weights are distributed by Google under a non-commercial/non-production license, so this research remained explicitly non-executing and non-commercial.

---

## 2. Research Questions

### RQ1 — Forecast skill

Does TimesFM 3.0 improve point and distributional forecasts of individual NSE stocks relative to persistence on untouched chronological origins?

### RQ2 — Directional information

Does TimesFM 3.0 provide directional information beyond each stock's contemporaneous positive-return base rate and persistence benchmark?

### RQ3 — Forecast uncertainty

Does TimesFM 3.0 forecast-interval width contain useful information about subsequent movement magnitude that can be used for risk sizing?

### RQ4 — Incremental stock selection

Does TimesFM add information to an independently specified stock-selection control, rather than acting as the sole stock selector?

### RQ5 — Regime dependence

Is any TimesFM incremental information concentrated in predeclared market regimes such as risk-on, stress, high/low volatility, high/low breadth or trend states?

### RQ6 — Economic value

Do any surviving signals remain economically attractive after turnover, spread/slippage and broker/statutory cost stress?

### RQ7 — Options transferability

Can underlying TimesFM information transfer into options strategies after comparison with the market-implied forecast?

RQ7 was not empirically completed because authorized historical options data were not available.

---

## 3. Aims and Objectives

### Aim

Scientifically evaluate whether TimesFM 3.0 contributes useful, reproducible information to an Indian-equity trading research pipeline.

### Objectives

1. Establish a reproducible point-in-time data architecture.
2. Compare TimesFM 3.0 with naive/statistical baselines.
3. Evaluate individual-stock forecasts rather than index-only forecasts.
4. Test directional, uncertainty and cross-sectional hypotheses.
5. Test incremental information around a predeclared independent stock-selection signal.
6. Condition tests on market regime, breadth, volatility, liquidity and corporate-action state.
7. Apply multiple-testing controls.
8. Apply explicit trading-cost stress.
9. Stop unsupported strategy variants rather than recursively searching thresholds.
10. Produce a manuscript-grade reproducible research record.

---

## 4. Hypotheses

H1. TimesFM 3.0 improves stock forecast error versus persistence.

H2. TimesFM 3.0 provides directional information beyond contemporaneous base rates.

H3. TimesFM 3.0 forecast uncertainty predicts future movement magnitude.

H4. TimesFM 3.0 adds incremental information to a predeclared stock-selection baseline.

H5. Incremental TimesFM information varies systematically with market regimes.

H6. A surviving TimesFM component remains positive after realistic transaction costs and stress.

The empirical program rejected or failed to support H1-H6 on the available bootstrap evidence.

---

## 5. Literature and Evidence Context

TimesFM 3.0 is a general foundation model, not a stock-specific forecasting system. Google describes native multivariate targets, probabilistic forecasts and past/past-future covariates as core capabilities.

This study therefore did not assume that benchmark-leading general forecasting performance implies financial alpha. The protocol explicitly included persistence, simple technical/statistical controls, rank-based cross-sectional evaluation, walk-forward evaluation and cost gates.

The literature review emphasized several recurring financial-forecasting hazards:

- persistence/random-walk baselines can be difficult to beat;
- positive-return base rates can make raw directional accuracy misleading;
- overlapping forecast horizons induce dependence;
- survivorship and look-ahead errors can create spurious alpha;
- corporate-action adjustment conventions can change price-level comparisons;
- gross return is insufficient when turnover and market friction are material.

These considerations motivated the project architecture rather than a single model-comparison contest.

---

## 6. Data and Source Hierarchy

### 6.1 Primary reference sources

NSE and BSE official data remain the preferred exchange-primary inputs for final evidence. The hosted GitHub Actions environment could not reliably retrieve several NSE historical routes. Three official routes were tested repeatedly with unusable responses:

1. historical-index route returning HTML/HTTP 200 instead of the expected JSON;
2. historical-index API returning HTTP 403 during session warm-up;
3. static index archive timing out, including an HTTP/1.1 retry.

The project therefore stopped retrying the same access path.

### 6.2 Individual-stock alternate data

The executable bootstrap lane uses TejHQ's Indian Markets dataset. Its published documentation describes raw NSE/BSE prices, corporate actions, back-adjusted prices, symbol history and a point-in-time liquidity universe built from exchange bhavcopy data.

The fixed research panel contains 30 liquid large-cap NSE names. It is explicitly an engineering/bootstrap universe, not a final survivorship-safe research universe.

### 6.3 Independent daily cross-check

Yahoo/yfinance-derived Indian-market data were used on five names as an independent cross-check. Absolute adjusted price levels could differ under different corporate-action conventions, but overlapping daily raw-close return paths were extremely close in the five-name bootstrap.

### 6.4 Intraday source discovery

The source search also identified a public MIT-licensed Hugging Face dataset reporting roughly 720 million rows across 2,500+ NSE stocks and indices, with one-minute data for 2022-2026 and daily data back to 2000. It is catalogued as a candidate intraday/scalping cross-check, not exchange-primary truth.

A separate public NSE F&O one-minute stock dataset covers 214 F&O underlyings from April 2024 to April 2026, sourced from the Zerodha Kite API. It is classified as secondary research data pending provenance and execution-quality validation.

### 6.5 Institutional-flow and sentiment sources

The source review identified multiple public FII/DII data projects, including historical dashboards and APIs backed by NSE or related public feeds. These were not substituted for official participant reports because their provenance, revision behavior and publication timestamps require dedicated point-in-time validation.

### 6.6 Options

Public NSE options/intraday datasets exist on community repositories, but the protocol requires authorized historical options data with exact contract identifiers, quote freshness, OI, volume, IV and lifecycle metadata before empirical option P&L research is promoted.

---

## 7. Scientific Methodology

### 7.1 Forecast model

Primary model: TimesFM 3.0, checkpoint google/timesfm-3.0-pytorch.

Configuration used for the stock bootstrap:
- context: 128 trading sessions;
- horizon: 5 sessions;
- univariate stock target;
- native quantile output;
- CPU inference in GitHub Actions;
- research-only license guard.

### 7.2 Baselines

Primary forecast baseline:
- persistence / last observation carried forward.

Stock-selection baseline:
- 20-session cross-sectional momentum.

### 7.3 Forecast metrics

- MAE;
- RMSE;
- five-session return MAE;
- directional accuracy;
- directional excess against the stock's contemporaneous positive-return base rate;
- rank IC;
- interval-width versus future absolute movement;
- rebalance-level permutation testing.

### 7.4 Strategy metrics

- top-six cross-sectional return;
- excess versus equal-weight universe;
- excess versus momentum control;
- net total return under cost stress;
- turnover;
- regime/sub-period stability.

### 7.5 Multiple testing

Phase 6 used Benjamini-Hochberg false-discovery-rate adjustment across predeclared regime rank-IC tests. The permutation unit was the rebalance, not the individual stock observation.

### 7.6 Point-in-time controls

The experimental code uses only data available at the forecast origin for:
- momentum;
- liquidity;
- market-state regime;
- volatility regime;
- corporate-action cooldown.

Future corporate-action dates were not used as predictors.

### 7.7 Cost framework

The exploratory strategy runs applied one-way proportional cost stresses of 0.125%, 0.25% and 0.50% in Phase 4, and 0.25% and 0.50% in the Phase 6 regime test.

The project's full cost engine additionally requires dated brokerage, STT, GST, exchange charges, stamp duty, DP charges, spread, market impact, financing and settlement treatment.

For current 2026 context, NSE documents that cash-equity delivery STT remains 0.10% on both purchase and sale, while certain derivatives STT rates changed effective April 1, 2026.

Paytm Money states that its current brokerage calculator excludes platform, depository, auto-square-off and other fees, so a single displayed brokerage number is not the complete execution cost. Its published material also documents a ₹13.5 delivery-sale DP charge and historical ₹20-per-executed-order pricing for newer accounts, with older users on legacy schedules.

---

## 8. Results

### 8.1 Phase 3 — recent 30-stock bootstrap

Configuration:
- 30 stocks;
- 40 recent chronological origins per stock;
- 5-session forecast horizon;
- 128-session context.

| Metric | TimesFM 3.0 | Persistence |
|---|---:|---:|
| Mean log MAE | 0.018675 | 0.017629 |
| Mean log RMSE | 0.027242 | 0.025726 |
| Stocks improving MAE | 3/30 | — |
| Stocks improving RMSE | 3/30 | — |
| Mean directional accuracy | 50.83% | — |
| Mean positive-return base rate | 39.75% | — |

The recent-window directional excess was +11.1 percentage points, but it was not accepted as evidence of alpha.

### 8.2 Phase 3 — four-fold robustness extension

The robustness experiment used:

30 stocks × 4 chronological folds × 40 origins = 4,800 stock-level forecast origins.

| Metric | TimesFM − persistence |
|---|---:|
| Mean MAE difference | +0.001144 |
| Mean RMSE difference | +0.001470 |
| Mean 5-session return-MAE difference | +0.001885 |
| Mean directional excess | −2.90 pp |
| Stocks with non-negative mean directional excess | 13/30 |
| Stocks with negative mean MAE difference across all folds | 0/30 |
| Mean interval-width/absolute-move Spearman rho | +0.091 |

The recent +11.1 pp directional excess therefore did not survive chronological broadening.

### 8.3 Phase 4.1 — individual-stock selection

A predeclared 20-session momentum control was compared with:
- TimesFM five-session forecast rank;
- 50/50 standardized momentum + TimesFM;
- momentum gated by TimesFM direction.

| Signal | Mean rank IC |
|---|---:|
| 20-session momentum | +0.0138 |
| TimesFM 5-session forecast | −0.0237 |
| 50/50 hybrid | −0.0151 |

Across 32 non-overlapping rebalances, TimesFM did not add cross-sectional ranking value.

At the lowest Phase 4 proportional cost stress:

| Strategy | Net total return |
|---|---:|
| Equal-weight universe | −7.3% |
| Momentum | −15.2% |
| TimesFM-only | −26.6% |
| Hybrid | −21.8% |

Higher cost stress worsened all strategies.

### 8.4 Phase 6.1 — regime-conditioned incremental information

The final stock experiment residualized the TimesFM forecast against momentum before evaluation and applied predeclared market-state, liquidity and event-conditioning rules.

| Regime | Residual rank IC | p-value | FDR q |
|---|---:|---:|---:|
| All | −0.0030 | 0.935 | 0.935 |
| Risk-on | −0.0454 | 0.396 | 0.779 |
| Breadth-high | −0.0280 | 0.557 | 0.779 |
| Breadth-low | +0.0609 | 0.439 | 0.779 |
| Trend-up | −0.0379 | 0.456 | 0.779 |
| Trend-down | +0.0551 | 0.425 | 0.779 |
| Low-vol | −0.0030 | 0.934 | 0.935 |

High-volatility and stress cells were not populated by the sparse 32-rebalance design and are therefore labelled untested, not interpreted as zero effect.

### 8.5 Phase 6.1 cost stress

At zero proportional cost:

| Strategy | Net total return |
|---|---:|
| Momentum | +35.00% |
| Risk-on TimesFM residual overlay | +35.79% |
| Hybrid | +34.52% |

At 0.25% one-way cost:

| Strategy | Net total return |
|---|---:|
| Momentum | +22.25% |
| Risk-on TimesFM residual overlay | +20.93% |
| Hybrid | +20.99% |

At 0.50% one-way cost:

| Strategy | Net total return |
|---|---:|
| Momentum | +10.66% |
| Risk-on TimesFM residual overlay | +7.65% |
| Hybrid | +8.78% |

The small gross risk-on improvement therefore did not survive cost stress.

---

## 9. Visual Summary

### 9.1 Research pipeline

~~~mermaid
flowchart LR
A[Point-in-time data] --> B[TimesFM 3.0 forecast]
B --> C[Calibration / forecast gate]
C --> D[Independent stock signal]
D --> E[Incremental TimesFM residual]
E --> F[Regime + liquidity + event gates]
F --> G[Cost / slippage hurdle]
G --> H[Walk-forward promotion]
H --> I[Manuscript evidence]
~~~

### 9.2 Stock forecast robustness

~~~mermaid
xychart-beta
    title "TimesFM minus Persistence: Four-Fold Stock Forecast Error"
    x-axis ["MAE","RMSE","5d Return MAE"]
    y-axis "Difference" 0 --> 0.0025
    bar [0.001144,0.001470,0.001885]
~~~

Positive values mean TimesFM had higher error.

### 9.3 Cross-sectional ranking

~~~mermaid
xychart-beta
    title "Mean Rank IC: Individual-Stock Selection"
    x-axis ["Momentum","TimesFM","Hybrid"]
    y-axis "Rank IC" -0.03 --> 0.02
    bar [0.0138,-0.0237,-0.0151]
~~~

### 9.4 Cost stress

~~~mermaid
xychart-beta
    title "Phase 6 Risk-On Overlay vs Momentum"
    x-axis ["0%","0.25%","0.50%"]
    y-axis "Net total return" 0 --> 0.40
    line [0.3500,0.2225,0.1066]
    line [0.3579,0.2093,0.0765]
~~~

First line: momentum.  
Second line: risk-on TimesFM residual overlay.

---

## 10. Inference

### Inference 1 — No standalone stock forecast edge

TimesFM 3.0 did not beat persistence on mean point-error metrics in the stock bootstrap or the four-fold robustness evaluation.

### Inference 2 — Recent directional excess was not robust

A positive recent-window directional excess reversed under broader chronological validation. The result should therefore be treated as a recency-window artifact unless reproduced in an independent holdout.

### Inference 3 — Raw TimesFM ranking was not useful for stock selection

TimesFM rank IC was negative in the Phase 4.1 stock-selection test and lower than the momentum control.

### Inference 4 — Regime conditioning did not rescue the signal

The predeclared regime cells did not show statistically supported incremental TimesFM information after FDR correction.

### Inference 5 — Small gross improvements were not economically durable

The risk-on TimesFM residual overlay was slightly better than momentum before proportional costs but became worse once cost stress was introduced.

---

## 11. Discussion

### 11.1 What failed

The study rejected a sequence of increasingly sophisticated but still simple hypotheses:

1. direct TimesFM stock direction;
2. uncertainty-conditioned stock sizing;
3. TimesFM cross-sectional ranking;
4. momentum + TimesFM blending;
5. TimesFM directional gating;
6. regime-conditioned TimesFM residual selection.

The important scientific point is not that a particular threshold failed. The important point is that the information did not survive progressively stricter controls.

### 11.2 Why this does not invalidate TimesFM generally

TimesFM 3.0 was not designed specifically for NSE microstructure. Its general benchmark performance does not guarantee alpha in a competitive, cost-sensitive market. Google explicitly positions TimesFM-3 as a general zero-shot model with broad multivariate capabilities rather than a proprietary trading signal.

The negative findings therefore narrow the plausible research space rather than proving universal model failure.

### 11.3 The more defensible future hypothesis

The remaining scientifically interesting use is conditional information, not raw direction.

That means asking whether TimesFM contributes information that an independent signal cannot already recover, for example:
- residual return expectation;
- event-conditioned range;
- market-to-stock residual movement;
- forecast distribution mismatch versus implied movement;
- execution timing;
- volatility forecasting.

Such a study should be run on a larger, fully point-in-time universe with authorized exchange-grade data.

---

## 12. Strengths

1. Individual stocks were treated as first-class instruments.
2. A real hosted-runner data-access failure was not disguised by repeatedly retrying the same endpoint.
3. Multiple independent data sources were explicitly separated by evidence tier.
4. Corporate-action and adjustment issues were treated as first-order research problems.
5. Forecast results were subjected to chronological robustness testing.
6. Stock-selection testing used an independently specified control.
7. Regime tests were predeclared.
8. Multiple-testing correction used rebalance-level permutation tests and BH-FDR.
9. Cost stress was applied before strategy promotion.
10. Every research failure and correction was written to the repository.

---

## 13. Limitations

### Data limitations

The final evidence does not use a fully authorized exchange-primary historical NSE dataset because of the hosted-runner access blocker. The 30-stock panel remains a bootstrap universe and is not sufficient to establish survivorship-free population-level stock evidence.

TATAMOTORS also has a shorter cached adjusted history than most names, ending at 2025-10-23 in the bootstrap, which requires identifier/source reconciliation before final PIT use.

### Regime limitations

The Phase 6.1 design contained no stress/high-vol observations in the sparse 32-rebalance sample. Those regimes therefore remain untested rather than null.

### Statistical limitations

The stock strategy tests contain relatively few rebalances. Their purpose was to falsify weak hypotheses, not to provide definitive population estimates of a professional trading program's long-run Sharpe ratio.

### Execution limitations

Daily OHLC data cannot reproduce queue position, spread dynamics, latency, partial fills or impact for scalping. No high-frequency strategy is considered execution-validated.

### Options limitation

Authorized historical option quotes/trades and contract lifecycle data were unavailable, so the options phase did not receive an empirical P&L test.

### External-feature limitation

FII/FPI/DII, India VIX, global lead/lag, USDINR, crude, gold and timestamped news were fully specified in the protocol but not all were incorporated into a final empirical stock model because the project stopped after the stock promotion gate failed.

---

## 14. Reproducibility and Audit

Primary repository artifacts include:

- docs/RESEARCH_PLAN.md
- docs/RESEARCH_STATUS.md
- docs/DATA_CATALOG.md
- docs/ALTERNATE_DATA_SOURCES.md
- docs/ERROR_LOG.md
- docs/CHAT_LOG.md
- docs/INDIVIDUAL_STOCK_STRATEGY_DESIGN.md
- docs/PHASE_3_STATUS.md
- docs/PHASE_4_STATUS.md
- docs/PHASE_6_STATUS.md
- results/p1_individual_stock_bootstrap.csv
- results/p1_individual_stock_bootstrap_summary.json
- results/p1_individual_stock_multifold_summary.json
- results/p1_individual_stock_multifold_per_stock.csv
- results/p4_p41_stock_overlay_summary.json
- results/p4_p41_origin_diagnostics.csv
- results/p6_p61_summary.json
- results/p6_p61_regime_metrics.json
- results/p6_p61_strategy_cost_results.json

Each experimental branch retains its own workflow and run history.

---

## 15. Final Conclusion

**No validated TimesFM 3.0 individual-stock trading strategy was established by this research program.**

The evidence is consistent across progressively stricter tests:

- TimesFM did not beat persistence on stock point forecasting.
- Recent directional excess did not survive chronological robustness.
- TimesFM stock ranking had negative mean rank IC in the strategy test.
- Simple momentum + TimesFM blending did not improve stock selection.
- Regime-conditioned TimesFM residuals were not statistically supported after FDR correction.
- The small gross risk-on improvement disappeared after cost stress.
- Options could not be promoted because the required historical option dataset was unavailable.
- Intraday/scalping claims were not promoted because execution-quality validation remains incomplete.

The usable research conclusion is therefore a negative one:

> On the available 2026 bootstrap evidence, TimesFM 3.0 should not be treated as a standalone directional stock-selection engine for NSE equities, nor should its simple forecast or uncertainty outputs be promoted into a trading strategy.

This is a research conclusion, not a recommendation about actual trading.

---

## 16. Future Research Directions

### Priority A — PIT stock universe

Replace the fixed 30-name bootstrap with a fully point-in-time liquidity universe, continuous ISIN lineage, delisting history and corporate-action-vintage controls.

### Priority B — Incremental residual research

Use a predeclared stock-selection control based on momentum, value, volatility or sector-relative residuals, then ask whether TimesFM adds information after the control.

### Priority C — Global cross-market information

Add:
- GIFT NIFTY;
- US close-to-NSE-open spillover;
- USDINR;
- crude;
- gold;
- rates;
- Asian-session variables.

Test both close-to-open and session-overlap effects.

### Priority D — Institutional-flow conditioning

Use point-in-time FII/FPI/DII observations and test:
- flow surprise;
- flow trend;
- FII-vs-DII divergence;
- flow × TimesFM interactions.

### Priority E — Option-implied comparison

Use authorized historical option quotes to compare:
- TimesFM forecast range;
- realized range;
- implied move;
- IV surface;
- skew;
- term structure.

Only residual forecast information that beats the market-implied forecast should be considered for option structures.

### Priority F — Intraday execution

Validate the public 1-minute data source against an independently licensed execution-grade feed before using it for scalping claims.

### Priority G — Alternative models

Test TimesFM 2.5 as a benchmark/ablation and compare against simple statistical models plus at least one lightweight supervised baseline under identical frozen origins.

---

# Appendix A — Promotion Gate

A stock strategy can be promoted only if all conditions hold:

1. Point-in-time data clean.
2. Security identifiers reconciled.
3. Forecast improvement versus primary baseline.
4. Directional or rank advantage survives relevant base-rate controls.
5. Quantile calibration acceptable.
6. Incremental signal survives FDR/multiple-testing control.
7. Strategy is positive after full dated costs.
8. Results remain stable across chronological folds.
9. Regime stress does not collapse performance.
10. Liquidity and participation constraints remain plausible.
11. No material look-ahead or survivorship error.
12. A reproducible run manifest exists.

No tested stock strategy satisfied all conditions.

---

# Appendix B — Current Cost References

NSE's published 2026 STT schedule keeps delivery-equity purchase and sale STT at 0.10% and changes selected derivative rates effective April 1, 2026.

Paytm Money's published material documents delivery-sale DP charges of ₹13.5 and historical flat-order brokerage schedules that depend on account vintage; its current brokerage calculator explicitly states that platform and depository fees are not included in the calculator result.

The Phase 7 cost engine therefore remains date-versioned rather than hard-coding one price across the entire historical record.

---

# Appendix C — Source Hierarchy

P0: NSE/BSE official or authorized licensed data  
P0-alternate: TejHQ exchange-derived EOD stock lane  
P1: independent Yahoo/yfinance-derived data; validated public intraday datasets  
P2: GitHub/Kaggle/Hugging Face community datasets used for diagnostics or bootstrap only

No secondary source is silently promoted to exchange-primary status.

---

# Appendix D — Research Stop Rule

The project was designed not to search indefinitely.

The individual-stock EOD empirical search stopped after:
1. a recent-stock forecast bootstrap;
2. a chronological robustness extension;
3. a direct stock-selection experiment;
4. a regime-conditioned incremental experiment.

The final result was negative at each progressively stricter economic gate.

Future work therefore belongs to a new preregistered research branch, not additional unlogged threshold/search variants in the existing holdout.

---

# Supplementary Materials

Supplement S1: results/p1_individual_stock_bootstrap.csv  
Supplement S2: results/p1_individual_stock_multifold_per_stock.csv  
Supplement S3: results/p4_p41_origin_diagnostics.csv  
Supplement S4: results/p6_p61_regime_metrics.json  
Supplement S5: results/p6_p61_strategy_cost_results.json  
Supplement S6: docs/ERROR_LOG.md  
Supplement S7: docs/CHAT_LOG.md
