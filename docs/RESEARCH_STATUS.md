# Research status

Updated: 2026-09-20 IST

## Scope decision — 2026-09-20
**Confirmed:** TimesFM 3.0 stays the primary model for all phases because this project is research for deriving and testing a trading strategy, not actually trading.

The scope is explicitly **non-executing scientific research**:
- strategy hypotheses may be generated and falsified;
- full cost/slippage/tax-aware simulated backtests are allowed;
- no broker execution, production deployment, client-facing trading decision or revenue-generating use is part of the project;
- TimesFM 2.5 is a benchmark/ablation model only.

## Phase 0 — Governance
**Complete for bootstrap.**

## Phase 1 — Literature
**Complete / protocol frozen.**

Model decision:
- TimesFM 3.0 primary scientific/evaluation model throughout the research.
- TimesFM 2.5 benchmark/ablation only.
- Direct direction is one hypothesis; uncertainty, volatility, multivariate inputs and causal covariates are explicit research targets.
- The current 3.0 pretrained-weight license remains a hard governance gate for any commercial/production use.

## Phase 2 — Data
**Validation green. Official public NSE runner routes remain blocked; alternate individual-stock EOD lane is now green.**

Completed on `phase-2-data`:
- point-in-time data policy;
- official source registry;
- community/alternate source registry;
- dataset manifest schema;
- manifest validator;
- synthetic PIT leakage test;
- manual GitHub Actions validation workflow;
- official-source audit;
- alternate TejHQ individual-stock EOD acquisition workflow;
- 30-name bootstrap stock cache with SHA-256 manifest;
- separate corporate-action cache and validator;
- stock-specific source documentation.

### Phase 2 evidence state

**Primary official NSE route:** blocked from hosted Actions runner. This remains issue #6.

**Alternate stock route:** green. Workflow run 35521951823 successfully acquired and validated the cached stock panel and corporate-action files.

**Current cache:** 30 NSE individual-stock EOD series, broadly 2010-01-04 to 2026-09-18 subject to each symbol's own listing history. The files include OHLCV/turnover and separate corporate-action histories. The cache is usable for engineering and exploratory forecasting, but not yet final stock-level evidence.

**Remaining stock-data gate:** build/verify price adjustment and point-in-time security identity/universe logic, and cross-check selected names against an independent Yahoo/yfinance-based dataset before running the main holdout.

## Phase 3 — TimesFM 3.0
**Engineering/unit-test gate green; individual-stock exploratory bootstrap completed; official NIFTY P0 remains blocked and the stock sample is not yet primary evidence.**

The 3.0 branch includes:
- pinned TimesFM 3.0.2;
- TimesFM3Evaluator adapter;
- multivariate targets;
- past-only covariates;
- nine quantiles;
- forecast provenance schema;
- manual model-smoke workflow.

The existing NIFTY P1 results remain exploratory C-grade evidence. The new stock cache opens an additional bootstrap lane, but it does not replace the requirement for PIT-clean primary/independent validation before final claims.

## Phase 4 — Strategy research
**Daily individual-stock TimesFM overlay gate closed after Phase 4.1 and nested Phase 4.2 tests. No tested daily TimesFM stock-selection mechanism survived chronological, baseline and cost-aware gates.**

Individual stocks are first-class instruments. Current strategy hypotheses include:
- single-stock forecast overlays;
- cross-sectional ranking;
- uncertainty-conditioned sizing;
- stock-vs-index residuals;
- corporate-event-aware stock research.

The common engine still requires PIT integrity, realistic costs/slippage, walk-forward stability and multiple-testing control.

## Phase 5 — Options
**Protocol/engineering bootstrap complete; empirical testing remains blocked by authorized historical option data.**

## Phase 6 — Regimes/external information
**Phase 6.1 stock regime-conditioning test completed; no incremental TimesFM stock information survived the statistical/economic gate.**

## Phase 7 — Cost/slippage/tax-aware walk-forward
**Cost-engineering track complete; no Phase 6 candidate advanced to a full promotion walk-forward.**

## Phase 8 — Simulation readiness/audit
**Non-executing engineering only; no paper/live execution path enabled.**

## Phase 9 — Final manuscript/release
**Complete. Final manuscript and conclusion committed; individual-stock empirical search stopped at the declared promotion gate.**

No strategy has passed a final empirical promotion gate. No live/paper execution path has been enabled.

## Review checkpoints

- Phase 2 draft PR #1: data/PIT infrastructure.
- Phase 3 draft PR #2: TimesFM 3.0 forecast-gate infrastructure.
- Phase 4 draft PR #3: strategy infrastructure.
- Phase 5 draft PR #5: options infrastructure.
- Issue #6: official NSE hosted-runner P0 blocker.

## Current provisional conclusion

The current evidence still does **not** establish standalone directional TimesFM alpha. The most defensible research hypothesis remains to use forecast distribution/uncertainty as a conditioning variable around an independently specified stock-selection or market-structure signal, and test the combination against identical no-TimesFM controls.

The individual-stock lane is now operational at the EOD bootstrap level, so the next scientific step is to reconcile corporate actions/identifier history and run the same frozen forecast matrix across a PIT stock cross-section before any strategy promotion.


## Phase 2 stock-lane checkpoint — 2026-09-20

The official NSE hosted-runner blocker remains unchanged for the primary index route, but the individual-stock research lane has advanced materially.

- 30-name raw EOD stock cache: green.
- Corporate-action cache: green.
- TejHQ back-adjusted stock cache: green.
- TejHQ point-in-time liquidity-universe cache: green.
- Independent Yahoo/yfinance cross-check on RELIANCE, TCS, HDFCBANK, INFY and SBIN: green.
- Cross-check overlap: approximately 3,738–4,110 trading dates per symbol.
- In that five-name bootstrap, at least 99.7% of overlapping daily raw-close returns differed by no more than 0.10 percentage points between the two sources.

This does not make the bootstrap a final unbiased universe. Final stock evidence still requires frozen PIT eligibility, identifier continuity and holdout separation.


## Phase 3 stock bootstrap checkpoint — 2026-09-20

Workflow 35522976491 completed the repaired 30-stock exploratory TimesFM 3.0 lane successfully.

Configuration:
- 30-name TejHQ adjusted-price bootstrap;
- context 128;
- horizon 5 sessions;
- 40 recent chronological origins per stock.

Observed:
- mean log MAE 0.018675 vs persistence 0.017629;
- mean log RMSE 0.027242 vs persistence 0.025726;
- 3/30 stocks better on MAE and 3/30 on RMSE;
- mean directional accuracy 50.83% vs mean positive-return base rate 39.75%;
- 25/30 stocks showed positive stock-level directional excess;
- only 5/30 improved five-session return MAE;
- mean q10–q90 width versus subsequent absolute movement Spearman rho -0.121, with 9 positive and 21 negative stock-level correlations.

Interpretation:
The bootstrap does not support a general TimesFM point-forecast advantage over persistence. The directional excess is an exploratory finding that still requires an independent stock-selection baseline, broader chronological folds, multiple-testing control and realistic cost/slippage simulation. The negative interval-width relationship means the uncertainty-sizing hypothesis seen in the earlier secondary NIFTY experiment does not transfer automatically to stocks.

A source-quality flag remains for TATAMOTORS, whose cached adjusted series ends 2025-10-23 while most names extend to 2026-09-18. Final PIT evidence must resolve identifier/source continuity before holdout promotion.

## Updated next gate

The next empirical stock step is a multi-fold stock forecast matrix on a frozen PIT universe, with explicit baseline selection and the existing economic-cost gate. High-frequency/scalping claims remain gated on the newly identified 1-minute source validation and execution-quality checks.


## Phase 3 P1.1 robustness checkpoint — 2026-09-20

The four-fold stock robustness extension completed successfully (workflow 35523375234; artifact 10608933929). It evaluated 30 stocks across four chronological folds with 40 origins per fold, for 4,800 stock-level forecast origins.

Aggregate:
- mean log-MAE difference (TimesFM minus persistence): +0.001144;
- mean log-RMSE difference: +0.001470;
- mean five-session return-MAE difference: +0.001885;
- mean directional excess: -2.90 percentage points;
- 13/30 stocks had non-negative mean directional excess;
- no stock had a negative mean MAE difference across all four folds;
- mean interval-width/absolute-movement Spearman rho: +0.091.

The initial recent-origin result (+11.1 percentage points directional excess) therefore does not survive chronological broadening. The current Phase 3 inference is that TimesFM 3.0 has not demonstrated incremental stock-level directional skill against the persistence benchmark, and the earlier uncertainty-sizing hypothesis remains unproven.



## Phase 4.1 synchronized result — 2026-09-20

The completed Phase 4.1 individual-stock experiment is now synchronized into main. It used a predeclared 20-session cross-sectional momentum control, TimesFM 5-session forecast ranking and a standardized 50/50 hybrid across 30 stocks and 32 non-overlapping five-session rebalances.

Cross-sectional diagnostics:
- momentum mean rank IC: +0.0138;
- TimesFM mean rank IC: -0.0237;
- hybrid mean rank IC: -0.0151.

At the lowest proportional cost stress, net total returns over the sparse test were approximately -15.2% momentum, -26.6% TimesFM-only, -21.8% hybrid and -7.3% equal-weight universe. These are exploratory results, not final Phase 7 evidence, but they are sufficient to reject the simple TimesFM stock-selection overlays for further promotion.

The next stock research experiment should therefore test incremental TimesFM information only after regime, liquidity, event and market-state conditioning, with the same no-TimesFM control.


## Phase 4.2 synchronized result — 2026-09-20

The nested regime-conditioned individual-stock experiment completed successfully (workflow 35524516653; artifact 10609740180).

Rule:
- 20-session stock breadth;
- low-breadth threshold learned only from prior folds;
- TimesFM 5-session forecast rank residualized against 20-session momentum;
- top six names traded only in the low-breadth regime;
- folds 2–4 used as the test sequence;
- no test-fold parameter selection.

Net total return:
- 0.125% one-way: momentum -5.20%, residual -10.02%;
- 0.25%: momentum -7.72%, residual -12.22%;
- 0.375%: momentum -10.16%, residual -14.37%;
- 0.50%: momentum -12.55%, residual -16.48%.

The incremental TimesFM residual lost to the independent momentum control at every cost level. The daily stock TimesFM overlay gate is therefore closed. No stock strategy is validated.

See [individual-stock TimesFM gate conclusion](docs/INDIVIDUAL_STOCK_TIMESFM_GATE_CONCLUSION.md).


## Final empirical conclusion — 2026-09-20

The individual-stock EOD empirical program has reached its stop rule.

Completed stock gates:
1. 30-stock TimesFM 3.0 forecast bootstrap;
2. four-fold robustness across 4,800 stock-level origins;
3. direct stock-selection comparison against 20-session momentum;
4. regime/liquidity/corporate-action-conditioned incremental-information test;
5. cost-stress rejection of the remaining gross candidate.

No tested TimesFM stock strategy passed all promotion conditions. The result is a negative research finding, not evidence that all future TimesFM/market combinations must fail.

The complete manuscript is at manuscript/TimesFM_NSE_Research_Manuscript.md and the final conclusion is at docs/FINAL_RESEARCH_CONCLUSION.md.


## Phase 4B continuation — 2026-09-20

The earlier Phase 9 stock stop was superseded by a predeclared multifrequency continuation. Phase 4B tested 2/5/10/20-session stock horizons using the existing 30-name bootstrap.

The 10-session raw TimesFM cross-sectional ranking was the only candidate that remained ahead of the 20-session momentum control across all four Phase 4B proportional-cost stresses. A PIT timestamp rerun left all 30 cached symbols eligible at the 32 tested dates, so the result did not change.

This is **candidate evidence only**. The exact four-fold sign-flip p-value is 0.3125 one-sided, and the bootstrap remains a 30-name panel rather than a final universe-scale PIT dataset. The candidate is frozen for a post-selection Phase 7 holdout; no additional TimesFM search is permitted before that result.


## Phase 7 resolution — 2026-09-20

The earlier Phase 4B 10-session candidate has now been resolved by the final post-selection holdout.

The 2023+ holdout used 91 ten-session rebalances with a mean of 29.76 PIT-eligible bootstrap names per origin, dated cash-equity statutory/broker/DP costs, position drift, final liquidation and five additional slippage stresses.

TimesFM net total return versus the 20-session momentum control:
- 0.00% extra slippage: +3.72% vs +67.97%;
- 0.125%: -7.93% vs +47.20%;
- 0.25%: -18.30% vs +28.96%;
- 0.375%: -27.52% vs +12.94%;
- 0.50%: -35.72% vs -1.12%.

The candidate was below momentum at every stress. One-sided block-signflip p-values ranged from 0.972 to 0.984. Maximum simulated participation was about 0.014% of trailing turnover.

**Final inference:** the Phase 4B candidate failed the Phase 7 promotion gate. The current individual-stock TimesFM EOD strategy search is closed. The project proceeds to final manuscript/release and preserves options/intraday work as separately data-gated future research.
