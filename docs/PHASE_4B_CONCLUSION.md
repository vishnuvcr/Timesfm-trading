# Phase 4B conclusion — individual-stock multifrequency TimesFM research

Updated: 2026-09-20 IST

## Research question

Does a materially different individual-stock holding period reveal useful TimesFM 3.0 cross-sectional information after the daily stock-selection gate failed?

## Frozen tests

The phase tested 2, 5, 10 and 20-session horizons on the fixed 30-stock bootstrap with four chronological folds and eight non-overlapping rebalances per fold. The candidate signal was the raw TimesFM H-session forecast return. The predeclared control was 20-session momentum. A separate uncertainty-scaled momentum mechanism was also tested.

## Main result

The **10-session TimesFM cross-sectional ranking** was the only horizon that produced a positive economic result across all four tested one-way proportional cost stresses.

At 0.125%, 0.25%, 0.375% and 0.50% one-way cost, the bootstrap net total return was approximately +19.87%, +14.12%, +8.64% and +3.41% for TimesFM, versus +9.58%, +4.57%, -0.22% and -4.80% for the momentum control.

The 10-session TimesFM strategy was ahead of momentum in three of four chronological folds. However, the exact four-fold sign-flip test gives a one-sided p-value of 0.3125. With only four chronological blocks, this is not statistically conclusive.

## Forecast-versus-strategy distinction

The TimesFM point forecast itself was not superior to persistence at 10 sessions:
- return MAE: 0.04660 versus 0.04241 for persistence;
- directional excess versus the contemporaneous positive-return base rate: -5.00 percentage points;
- mean cross-sectional rank IC: +0.0048.

Therefore the observed economic result cannot be described as a general point-forecast accuracy advantage. It is a cross-sectional portfolio-ranking result that requires further validation.

## PIT check

The candidate was rerun using the Phase 2 point-in-time liquidity-universe table. All 30 cached bootstrap names were PIT-eligible at all 32 rebalance dates, so the PIT restriction did not change the candidate portfolio.

This is useful evidence that the decision timestamps were aligned to the cached PIT intervals, but it does **not** establish final universe-scale survivorship protection because the price cache itself still contains only the 30-name bootstrap panel.

## Minute-data finding

The candidate 1-minute source passed a corrected structural probe for schema, timestamps and OHLC consistency. The probe also contained zero-volume rows, so the source is not being treated as execution/fill validated. Genuine BTST/intraday/scalping work remains a separate gate.

## Decision

The 10-session TimesFM ranking is retained as a **single frozen candidate** for the predefined Phase 7 cost-aware holdout. No new TimesFM thresholds, horizons, hybrid weights or regime variants are being searched.

Phase 6.1's previously completed stock regime-residual experiment did not provide statistical/economic support for that different mechanism, so it is not being reopened.

The candidate is not a validated or production strategy. The next gate is a post-selection, 2023+ holdout with the date-versioned cash-equity fee model, explicit brokerage/statutory charges, spread/slippage stress, turnover, capacity, drawdown, year/regime breakdown and multiple-testing-aware inference.


## Superseded by Phase 7 — 2026-09-20

The 10-session TimesFM ranking identified here as an exploratory candidate was subsequently tested once, without retuning, on the predefined 2023+ Phase 7 post-selection holdout.

It failed against the 20-session momentum control at zero and all additional slippage stresses. Therefore this Phase 4B document should be read as the exploratory candidate-stage conclusion only; the current final decision is recorded in `docs/FINAL_RESEARCH_CONCLUSION.md`.
