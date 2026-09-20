# Phase 6.2 — 10-session TimesFM regime conditioning

## Research question

Does the Phase 4B 10-session TimesFM 3.0 stock-ranking candidate add incremental value only under specific observable market states?

## Predeclared conditioning

The experiment keeps the Phase 4B 10-session horizon and freezes five cells:
- unconditional TimesFM ranking;
- risk-on overlay;
- breadth-low overlay;
- trend-down overlay;
- high-volatility overlay.

Risk-on, breadth, trend and volatility are computed using only information available at the forecast origin. A top-20-of-30 trailing-turnover liquidity filter and five-session post-ex-date cooldown are applied before stock selection.

The independent control is the same 20-session momentum strategy on the same eligible names and rebalance dates.

## Promotion gate

A conditional cell must:
- exceed the matched momentum control after costs;
- remain directionally credible across chronological folds;
- survive four-fold sign-flip testing;
- survive BH correction across the five predeclared economic cells;
- remain eligible for Phase 7 cost/slippage/capacity validation.

No cell is promoted solely because it has a higher raw return.

## Data limitation

The current 30-name universe is still bootstrap evidence. Global cues, FII/FPI/DII, India VIX, options and timestamped news are not included here because the repository does not yet contain frozen point-in-time versions of those P0 feature series. They remain Phase 6 downstream requirements rather than being proxied with hindsight or current-value data.

## Status

Pending workflow execution.
