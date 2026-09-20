# Phase 4 intraday strategy matrix — frozen protocol

Updated: 2026-09-20 IST

## Research question

Does TimesFM 3.0 add incremental cross-sectional information for liquid NSE individual stocks at intraday horizons when compared with a simple, past-only VWAP-deviation control and realistic cash-equity trading costs?

## Source and universe

Use the hash-verified GitHub release:
- repository: voletiramu/nse-fno-1min-data
- release: v1.0.0
- asset SHA-256: 20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2
- release period: 2024-04-01 to 2026-04-30
- fixed validated universe: RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, SBIN, ITC, BHARTIARTL, LT, AXISBANK.

Only complete 09:15–15:29 sessions are used. The source gate showed zero duplicate timestamps, <=2 quarantined invalid-OHLC rows per symbol, negligible zero-volume fractions, and cross-source daily-return consistency within the frozen 25 bp median / 100 bp P95 bounds after recorded corporate-action dates were excluded.

## Frozen forecast matrix

Three horizon cells:
- 15 minutes
- 30 minutes
- 60 minutes

Common model:
- TimesFM 3.0 primary;
- univariate log-close context;
- context = 128 one-minute observations;
- one forecast path to 60 minutes; use the H-minute endpoint for each H;
- no covariates or model tuning in this first intraday matrix.

Forecast baseline:
- persistence/zero-return benchmark.

## Frozen strategy controls

### TimesFM
At each origin, rank the ten stocks by the H-minute TimesFM forecast return and go long the top three.

### VWAP control
At the same origin, rank stocks by price / session_VWAP - 1 and go long the top three.

The VWAP control is calculated only from data available through the origin close.

No shorting, leverage, threshold tuning, stop-loss tuning, or additional technical filters are included in this first matrix.

## Execution convention

Signal is generated at the origin minute close.

To prevent same-bar leakage:
- entry = next minute open;
- exit = close of the H-th minute after the origin.

Only origins whose exit is by 15:14 IST are eligible. This avoids the Paytm Money intraday auto-square-off window beginning in the final 15 minutes of the regular session. Paytm Money states that intraday positions are automatically squared off between 3:15 and 3:30 pm.

At each rebalance, all three prior positions are closed before the new three are opened. There are no overlapping holdings.

## Sampling / chronology

- four chronological folds over the validated common-session period;
- folds 1–3 = development;
- fold 4 = untouched holdout;
- 40 non-overlapping origins per fold/horizon;
- origins are spread deterministically across each fold;
- minimum origin minute = 09:45 IST;
- no origin is used if the required 128-minute context contains an invalid/quarantined bar for that stock.

The development-stage candidate rule is frozen before execution:
1. TimesFM must beat the VWAP control in compounded net return at 10 bps one-way extra slippage in each of the three development folds;
2. paired block-sign-flip one-sided p < 0.10 at the 10 bps development stress;
3. Benjamini-Hochberg q < 0.10 across the three TimesFM horizon cells.

All development-pass cells are then evaluated independently on fold 4. No holdout result is used to tune horizon or costs.

## Cost model

Current Paytm Money reference for stock intraday trading:
- ₹20 per executed order;
- brokerage was aligned to ₹20 across segments from 15 Jan 2025 for the applicable new-user schedule.

Research cash-intraday charges:
- NSE cash transaction + IPFT: ₹307/crore each side from 1 Mar 2026;
- SEBI turnover fee: ₹10/crore;
- STT: 0.025% on the intraday sale side;
- stamp duty: 0.003% on the buy side;
- GST: 18% on brokerage + exchange/SEBI charge components.

Additional one-way slippage/impact stresses:
- 0.00%
- 0.025%
- 0.050%
- 0.100%
- 0.200%

No DP charge, financing or MTF cost is included because all positions are intraday and fully squared the same session.

Because the minute source has OHLCV but no bid/ask quote history, slippage is a stress proxy rather than a claim of historical fill reconstruction.

## Statistical analysis

For each horizon:
- MAE/RMSE against zero-return persistence;
- directional excess over the positive-return base rate;
- cross-sectional rank IC;
- gross and net strategy return;
- fold-level paired differences versus VWAP;
- moving-block sign-flip inference using 5-rebalance blocks;
- BH-FDR across the three TimesFM horizon tests.

Economic outputs:
- cumulative net return;
- maximum drawdown;
- periodized Sharpe;
- turnover;
- average holding time;
- total brokerage/statutory/slippage cost.

## Promotion rule

A development cell can reach holdout only through the predeclared development rule. On the holdout, it is considered research-surviving only if:
- net return remains positive at 0.20% extra one-way slippage;
- it remains ahead of the VWAP control at 0.20%;
- its holdout paired block test is reported;
- no capacity/participation constraint is violated;
- no additional parameter search is introduced.

Passing this intraday matrix does not authorize live trading. A positive candidate would require a separate final holdout with quote/fill data before any final manuscript promotion.

## Stop rule

Do not add more TimesFM horizons, technical indicators, thresholds, hybrids or stocks based on observed outcomes. If all three horizon cells fail the development rule, close this intraday strategy family and move to the next predeclared lane.
