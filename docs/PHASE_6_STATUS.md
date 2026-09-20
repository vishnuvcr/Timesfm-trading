# Phase 6 status

Updated: 2026-09-20 IST

## Status

Research-engineering bootstrap complete; empirical testing waits for the frozen P0 dataset.

## Feature families

- Regime: trend/range state, realized volatility, volatility-of-volatility, breadth.
- India-specific: India VIX, FII/FPI/DII flows and participant positioning with point-in-time availability.
- Global cross-market: major US equity lead markets, GIFT NIFTY, USDINR, rates, crude and gold; close-to-open and session-overlap lead/lag features.
- Options: IV, skew, term structure, OI/volume and implied-versus-realized movement.
- Corporate actions: announcement time, ex-date, split/bonus/dividend metadata and adjustment vintage.
- News/sentiment: publication time, event time and availability time kept separate.
- Macro: release timestamp, observation period, revision/vintage identifiers and surprise measures.

## Point-in-time contract

Every observation carries event time, availability time, source id and vintage id. A forecast may consume a feature only when availability_time is no later than the forecast origin, unless it is explicitly classified as future-known.

Revisions are represented explicitly rather than overwriting history. No generic forward-fill is permitted across market closures or contract lifecycle boundaries.

## Cross-market tests

The empirical matrix will include lead/lag regressions, rank IC, close-to-open spillover, session-overlap effects, regime conditioning, FII/DII surprise interactions, event-day comparisons and global-to-NSE overnight spillovers.

No economic conclusion is promoted until PIT validation, multiple-testing correction and Phase 7 cost-aware walk-forward testing pass.

## Gate

Phase 6 cannot promote a signal until P0 datasets, PIT controls and the frozen cost model are available.


## 2026-09-20 — Phase 6.1 empirical stock conditioning

A separate exploratory track now tests whether TimesFM adds incremental information to an independent 20-session momentum signal after observable market-state conditioning.

Predeclared regimes:
- risk-on: equal-weight 30-stock 20-session return >= 0, breadth >= 50%, and low volatility versus a past-only rolling median;
- stress: 20-session return < 0, breadth < 50%, and high volatility;
- trend-up/down and high/low volatility;
- top-20-of-30 liquidity filter using trailing turnover;
- five-trading-session post-corporate-action cooldown, using only ex-dates already observed by the decision timestamp.

The TimesFM component is residualized cross-sectionally against momentum before rank testing. Significance uses rebalance-level permutation testing and Benjamini-Hochberg FDR across the predeclared regime cells. This avoids treating stock observations within the same rebalance as independent evidence.

The experiment remains exploratory because the 30-name universe is not final PIT evidence and Phase 7's dated full cost engine is not yet applied.


## 2026-09-20 — Phase 6.1 result

Workflow 35524645761 completed successfully and uploaded artifact 10609451021.

Across 30 stocks and 32 common rebalances:
- unconditional TimesFM residual rank IC: -0.0030, permutation p=0.935, FDR q=0.935;
- risk-on residual rank IC: -0.0454, p=0.396, FDR q=0.779;
- breadth-low residual rank IC: +0.0609, p=0.439, FDR q=0.779;
- trend-down residual rank IC: +0.0551, p=0.425, FDR q=0.779;
- no predeclared cell achieved statistical support after rebalance-level permutation testing and FDR.

The risk-on residual overlay produced a slightly higher zero-cost total return than momentum (35.79% vs 35.00%), but this advantage reversed after a 0.25% one-way proportional cost stress (20.93% vs 22.25%) and widened at 0.50% stress (7.65% vs 10.66%).

The stress/high-vol cells were under-populated in this sparse 32-rebalance design, so they are reported as untested rather than interpreted as null evidence.

**Decision:** no Phase 6 regime-conditioned TimesFM strategy is promoted. The research stop rule is now reached for the individual-stock EOD strategy lane: all tested standalone, hybrid and regime-conditioned TimesFM stock hypotheses failed a statistical/economic promotion gate.
