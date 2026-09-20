# TimesFM 3.0 for Indian-Equity Trading Research: A Point-in-Time, Cost-Aware Evaluation

**Research program:** TimesFM Trading — NSE Research Program  
**Research date:** 20 September 2026 (IST)  
**Primary scientific model:** TimesFM 3.0 — google/timesfm-3.0-pytorch  
**Market focus:** NSE individual cash equities, with index/market-state and broader Indian-market features as contextual inputs  
**Execution status:** Non-executing research only

---

## Abstract

This study evaluates whether Google TimesFM 3.0 can provide statistically and economically useful information for Indian-equity trading research. The project was designed as a gate-first, point-in-time, cost-aware program covering individual stocks, indices, swing/intraday horizons, options, market regimes, corporate actions, institutional flows and global cross-market information. Several official NSE historical routes were inaccessible from the hosted GitHub Actions environment, so the data program established an alternate individual-stock end-of-day lane based on TejHQ Indian-market data and independently cross-checked it against Yahoo/yfinance-derived data. Alternate sources were kept separate from exchange-primary evidence.

The individual-stock research progressed through a sequence of increasingly strict tests. A 30-stock five-session TimesFM 3.0 forecast bootstrap was worse than persistence on mean log MAE and RMSE. A four-fold chronological robustness test covering 4,800 stock-level origins reversed an apparent recent directional excess into a negative mean directional excess. Direct cross-sectional selection, hybrid and regime-conditioned residual tests also failed to demonstrate incremental value after baseline and cost controls.

A predeclared Phase 4B multifrequency extension then tested 2, 5, 10 and 20-session holding horizons. The 10-session TimesFM cross-sectional ranking was the only exploratory cell that exceeded the 20-session momentum control across the declared cost stresses on the bootstrap panel. It was therefore frozen, subjected to a point-in-time eligibility rerun, and advanced without further tuning to a post-selection 2023+ Phase 7 holdout. That holdout used 91 non-overlapping ten-session rebalances, the dated cash-equity statutory/broker/DP cost model, position drift, final liquidation, and five additional one-way slippage stresses. At zero extra slippage, the TimesFM candidate returned +3.72% versus +67.97% for momentum; at 0.125% extra slippage it became -7.93% versus +47.20%. At 0.50% extra slippage it was -35.72% versus -1.12%. Paired block sign-flip tests were adverse at every stress level, and maximum simulated participation was only about 0.014% of trailing turnover.

The final conclusion is therefore stronger than the earlier exploratory stop: **the single frozen 10-session individual-stock TimesFM mechanism failed its untouched post-selection holdout and no validated individual-stock TimesFM trading strategy was established.** The result does not prove that every TimesFM/market combination must fail; it establishes that the tested stock mechanisms did not survive chronological robustness and a realistic post-selection economic holdout on the available bootstrap evidence.
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

The robustness experiment used 30 stocks × 4 chronological folds × 40 origins = 4,800 stock-level forecast origins.

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

A predeclared 20-session momentum control was compared with TimesFM five-session forecast ranking and a 50/50 standardized hybrid.

| Signal | Mean rank IC |
|---|---:|
| 20-session momentum | +0.0138 |
| TimesFM 5-session forecast | −0.0237 |
| 50/50 hybrid | −0.0151 |

Across 32 non-overlapping rebalances, TimesFM did not add cross-sectional ranking value. At the lowest Phase 4 proportional cost stress, TimesFM-only net total return was about -26.6%, versus -15.2% for momentum and -21.8% for the hybrid.

### 8.4 Phase 6.1 — regime-conditioned incremental information

The predeclared regime-conditioned stock test residualized TimesFM against momentum and evaluated market state, breadth, volatility, liquidity and post-corporate-action conditions. No regime cell survived rebalance-level permutation testing and Benjamini-Hochberg FDR correction.

The risk-on overlay produced a small gross improvement over momentum before proportional costs but underperformed after 0.25% and 0.50% one-way cost stress.

### 8.5 Phase 4B — multifrequency swing matrix

A frozen 2/5/10/20-session swing matrix used 30 stocks, four chronological folds, eight non-overlapping rebalances per horizon and a top-six long-only portfolio.

Forecast-level metrics remained worse than persistence at all four horizons. The 10-session cell was the only exploratory mechanism that exceeded the 20-session momentum control under all four Phase 4B proportional cost stresses:

| Horizon | TimesFM net return at 0.125% | Momentum | TimesFM net return at 0.50% | Momentum |
|---|---:|---:|---:|---:|
| 2d | -15.58% | -10.42% | -25.60% | -17.66% |
| 5d | -29.98% | -18.34% | -38.57% | -26.77% |
| 10d | +19.87% | +9.58% | +3.41% | -4.80% |
| 20d | -18.07% | -17.55% | -29.41% | -32.11% |

The exact four-fold sign-flip p-value for the 10-session TimesFM-minus-momentum difference was 0.3125 one-sided. The 10-session candidate was therefore frozen for a downstream post-selection holdout rather than promoted.

### 8.6 Phase 4B — point-in-time candidate check

The frozen 10-session candidate was rerun against the Phase 2 point-in-time liquidity table. All 30 cached bootstrap names were eligible at all 32 tested rebalances. The PIT restriction therefore did not alter portfolio composition.

This validates timestamp eligibility inside the cached panel, but not broad-universe survivorship protection because the price cache remains a 30-name engineering/bootstrap panel.

### 8.7 Phase 7 — 2023+ post-selection holdout

The candidate was then evaluated once on an untouched 2023+ holdout. There were 91 non-overlapping ten-session rebalances from 2023-01-02 through 2026-09-03. Mean PIT-eligible names per origin were 29.76 (minimum 29, maximum 30). The candidate was fixed before this holdout; no parameters were tuned on holdout results.

The cost model included current cash-delivery STT, exchange/IPFT charges, SEBI turnover fees, delivery stamp duty, GST on applicable service components, a ₹20/order brokerage reference, ₹13.5 delivery-sale DP reference, explicit position drift and final liquidation. Additional one-way slippage/impact stresses were 0%, 0.125%, 0.25%, 0.375% and 0.50%.

| Extra one-way slippage | TimesFM net return | Momentum net return | TimesFM max DD | TimesFM Sharpe |
|---|---:|---:|---:|---:|
| 0.00% | +3.72% | +67.97% | -25.13% | 0.144 |
| 0.125% | -7.93% | +47.20% | -28.83% | -0.075 |
| 0.25% | -18.30% | +28.96% | -32.35% | -0.295 |
| 0.375% | -27.52% | +12.94% | -36.79% | -0.515 |
| 0.50% | -35.72% | -1.12% | -41.46% | -0.736 |

The TimesFM candidate was below the no-TimesFM momentum control at every stress level, including zero extra slippage.

The paired period difference was negative throughout. The one-sided block-signflip p-values were 0.984, 0.982, 0.979, 0.976 and 0.972 from the lowest to highest slippage stress. Maximum simulated participation was only about 0.014% of trailing turnover, so capacity was not the binding explanation.

At the maximum 0.50% stress, the TimesFM candidate compounded negatively in every calendar year of the holdout: approximately +1.0% in 2023, -12.0% in 2024, -11.7% in 2025 and -17.6% in 2026. The momentum control was approximately +2.6%, +5.7%, +1.4% and -9.6% respectively.

The candidate therefore failed the final economic promotion gate.
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

TimesFM 3.0 did not beat persistence on mean point-error metrics in the recent bootstrap or the four-fold stock robustness evaluation.

### Inference 2 — Recent directional excess was not robust

The positive recent-window directional finding reversed under broader chronological validation and is not accepted as evidence of a stable directional edge.

### Inference 3 — Direct stock ranking did not survive selection controls

TimesFM ranking was weaker than the independent 20-session momentum control in the first stock-selection experiment.

### Inference 4 — A different holding period produced an exploratory candidate, not a validated edge

The 10-session TimesFM ranking was the only Phase 4B cell that survived the exploratory cost screen, but its four-fold evidence was low-power and it remained a fixed 30-name bootstrap result.

### Inference 5 — The untouched post-selection holdout rejected the candidate

The 2023+ Phase 7 holdout produced lower net returns than momentum at every slippage stress, including zero extra slippage. This resolves the exploratory Phase 4B candidate against the final economic gate.

### Inference 6 — Capacity was not the limiting explanation

Maximum simulated participation was approximately 0.014% of trailing turnover. The candidate's failure therefore did not arise from an obviously binding participation constraint in this simulation.

### Inference 7 — Current individual-stock TimesFM search should stop

Under the declared stop rule, the completed stock holdout should not be mined for new thresholds, horizons, hybrid weights or regime filters. Any future reopening requires a materially different preregistered question, new authorized/PIT-clean data or a genuinely different instrument/economic mechanism.
## 11. Discussion

### 11.1 What failed

The study rejected a sequence of increasingly demanding stock-level hypotheses:

1. direct TimesFM stock direction;
2. uncertainty-conditioned stock sizing;
3. five-session and then multifrequency raw TimesFM ranking;
4. momentum + TimesFM blending;
5. TimesFM directional gating;
6. regime-conditioned TimesFM residual selection;
7. the one 10-session ranking candidate that survived exploratory cost screening.

The most important result is the post-selection holdout: the only candidate allowed to advance from Phase 4B under the preregistered protocol did not survive a 2023+ cost-aware test against the independent momentum control.

### 11.2 Why this does not invalidate TimesFM generally

TimesFM 3.0 is a general time-series foundation model, not a model trained specifically for NSE cross-sectional alpha. The negative result is conditional on the tested data source, universe, horizons, cost model and strategy translation. It does not establish that every market, target or TimesFM use case must fail.

The research does establish something narrower and useful: on this stock panel, simple forecast translation into a long-only selection strategy did not produce robust incremental economics after post-selection testing.

### 11.3 Why the exploratory Phase 4B result disappeared

The 10-session bootstrap result was supported by only four chronological blocks and was generated on a sparse 30-name panel. The stronger 2023+ holdout introduced 91 rebalances, current dated costs, position drift and final liquidation without allowing retuning. Its negative result therefore provides a materially stronger falsification test than the original Phase 4B candidate screen.

### 11.4 Remaining scientifically credible directions

Future research should shift the economic mechanism rather than search the same holdout for a better threshold. Plausible directions include:
- stock-vs-index residual forecasting;
- event-conditioned range/volatility forecasting;
- forecast versus option-implied movement;
- intraday execution timing with licensed execution-quality data;
- broader point-in-time universes with continuous security identity;
- other model classes used under the same frozen-origin benchmark.
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

The evidence now includes both exploratory and post-selection tests:

- TimesFM did not beat persistence on stock point forecasting.
- A recent directional excess did not survive four-fold chronological robustness.
- Initial direct stock-selection and hybrid overlays were weaker than the independent momentum control.
- Regime-conditioned TimesFM residuals were not statistically supported after rebalance-level permutation testing and FDR correction.
- A predeclared multifrequency extension found one exploratory 10-session candidate, but that candidate failed the untouched 2023+ Phase 7 holdout.
- The 10-session candidate was below momentum at every tested slippage stress, including zero extra slippage.
- The maximum simulated participation was only about 0.014% of trailing turnover, so capacity was not the binding explanation.

The strongest current scientific statement is therefore:

> On the available Indian-equity bootstrap evidence, the tested TimesFM 3.0 individual-stock mechanisms do not provide robust incremental trading value after chronological robustness, baseline comparison and post-selection cost-aware validation.

This is a research conclusion, not a recommendation about actual trading.

The conclusion remains limited by the alternate EOD data lane and the lack of fully authorized exchange-grade broad-universe data and historical option/intraday execution datasets. Future research can test different economic mechanisms, instruments or higher-quality data under new preregistered holdouts. The completed individual-stock holdout itself is closed to further specification search.
## 16. Future Research Directions

### Priority A — Authorized point-in-time stock universe

Replace the fixed 30-name bootstrap with a broad point-in-time liquidity universe with continuous ISIN lineage, delisting history and complete corporate-action vintage controls.

### Priority B — Different economic mechanisms

If the stock program is reopened, use a new preregistered hypothesis such as stock-vs-index residual returns, event-conditioned range/volatility forecasting, or cross-asset relative-value signals. Do not mine the completed TimesFM10 holdout for thresholds or weights.

### Priority C — Global cross-market information

Add GIFT NIFTY, US close-to-NSE-open spillovers, USDINR, crude, gold, rates and Asian-session variables with publication/availability timestamps.

### Priority D — Institutional-flow conditioning

Use point-in-time FII/FPI/DII data and test flow surprises, divergence and interactions only on a fresh holdout.

### Priority E — Option-implied comparison

With authorized historical bid/ask/OI/IV/Greeks, compare TimesFM forecast distributions with implied movement before considering any options structure.

### Priority F — Intraday execution

Validate the candidate public minute source against licensed execution-grade data, including session completeness, spread, zero-volume handling, corporate actions and fill-quality diagnostics, before any scalping or BTST economic claim.

### Priority G — Alternative models and benchmarks

Compare TimesFM 2.5, lightweight statistical models and supervised baselines on identical frozen origins. Any future positive result must satisfy the same cost-aware post-selection standard used here.
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
13. A post-selection holdout is completed without test-period tuning.

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
3. direct stock-selection and hybrid tests;
4. a regime-conditioned incremental experiment;
5. a frozen multifrequency swing candidate;
6. a point-in-time candidate check;
7. a 2023+ post-selection cost-aware holdout.

The final candidate failed the holdout at zero and all additional slippage stresses.

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
