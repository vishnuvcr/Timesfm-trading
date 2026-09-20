# Phase 4B BTST / overnight strategy matrix

Updated: 2026-09-21 IST

## Research question

Does TimesFM 3.0 add incremental information for individual NSE stocks' next-session overnight return, from the Indian close to the next Indian open, beyond a simple historical overnight-return control and timestamp-safe global-market information?

## Target

For stock i on signal day t:
overnight_return(i,t+1) = log(Open(i,t+1) / Close(i,t)).

Execution proxy:
- entry = 15:29 IST regular-session close on day t;
- exit = 09:15 IST first-minute open on day t+1;
- no position overlap because each BTST position is closed at the next open before the next day's close entry.

This is a genuine BTST target. It is not a relabeled close-to-close return.

## Validated universe

Fixed ten-stock minute-source universe:
RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, SBIN, ITC, BHARTIARTL, LT, AXISBANK.

Source release:
- repository: voletiramu/nse-fno-1min-data;
- release: v1.0.0;
- SHA-256: 20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2;
- validated regular-session source window: 2024-04-01 to 2026-04-30.

BTST strategy sample is restricted to the common date window available after joining the fixed global-data source set, currently expected to end 2026-03-31.

Corporate-action control:
- exclude an overnight observation when either the signal date or next-session date has a recorded corporate-action event in the Phase 2 action cache;
- retain the exclusion count in the results artifact.

## Primary model cells

1. TimesFM 3.0 univariate overnight model.
2. TimesFM 3.0 with fixed past-only global/domestic covariates.

Target construction for TimesFM:
- build a daily pseudo-level as cumulative sum of observed overnight log returns;
- forecast the next pseudo-level with horizon 1;
- subtract the last observed pseudo-level to obtain the predicted next overnight return.

Context: 128 daily overnight observations.

No horizon search, context search, threshold search, stock-universe search or post-result feature selection is permitted.

## Independent control

20-session exponentially weighted mean overnight return, computed using observations available through the signal close.

Control rank is cross-sectional and is evaluated on the same fixed stock set, dates and execution convention as TimesFM.

## Timestamp-safe global/domestic covariates

These are deliberately conservative relative to the 15:30 IST information cutoff:
- same-day NIFTY 50 close-to-close return;
- same-day Nikkei 225 return, available before the Indian close;
- same-day Hang Seng return, available before the Indian close;
- previous-day S&P 500 return;
- previous-day DAX return;
- previous-day Brent return;
- previous-day Gold return;
- previous-day US Dollar Index return;
- same-day ten-stock breadth: fraction with positive close-to-close return;
- same-day 20-session cross-sectional realized-volatility state.

The European/U.S./commodity features are lagged one source day rather than using their later local closes, because their daily closing times are after the Indian 15:30 signal cutoff.

FII/FPI/DII:
- the repository will attempt a separate timestamp-safe historical extraction from the fixed upstream workbook source;
- FII/DII is a secondary sensitivity feature, not a separate promotion family in this first BTST gate;
- if the workbook cannot be parsed reproducibly, that failure is logged and the primary BTST gate remains frozen without silently imputing flows.

## Strategy layer

At each signal date, rank all eligible stocks by predicted next overnight return and go long the top three, equal-weighted.

No shorting, leverage, stops, profit targets or discretionary filters.

## Costs

Cash-delivery/BTST baseline uses the project's effective-date fee manifest:
- ₹20 brokerage per executed order reference;
- 0.10% STT on cash-delivery buy and sell;
- NSE exchange/IPFT and SEBI turnover charges;
- GST on brokerage/exchange/SEBI components;
- stamp duty on buy;
- ₹13.5 delivery-sale DP charge reference as a conservative baseline.

Additional one-way slippage stresses:
- 0.00%;
- 0.025%;
- 0.050%;
- 0.100%;
- 0.200%.

Slippage is applied to both entry and exit prices. Fixed order costs are calculated from actual notional trade events.

Because the minute source is OHLCV without bid/ask history, these are execution-stress simulations rather than exact historical fill reconstruction.

## Capacity

For every selected stock, compute the trade notional as a fraction of trailing 20-session median traded value.

Hard capacity exclusion: >1.0% of trailing 20-session median traded value.

Also report maximum and median participation for every strategy/cost cell.

## Chronological validation

Use four chronological folds over all eligible common sessions:
- folds 1-3: development;
- fold 4: untouched holdout.

Every eligible common session is an origin; there is no sparse rebalancing subsample.

Development rule for a TimesFM cell:
1. positive net compounded return on development folds at 0.05% additional one-way slippage;
2. ahead of the 20-session overnight control on each development fold at that same stress;
3. paired 5-session block sign-flip one-sided p < 0.10;
4. BH-FDR q < 0.10 across the two primary TimesFM cells;
5. maximum participation <=1.0%.

Only a cell satisfying all conditions may enter fold 4.

Holdout survival rule:
- positive net return at 0.10% additional one-way slippage;
- ahead of the independent control at 0.10%;
- reported paired block inference;
- no capacity violation;
- no additional parameter selection.

## Forecast diagnostics

Report per horizon/cell:
- MAE against realized overnight return;
- persistence MAE;
- directional excess over the contemporaneous positive-return base rate;
- cross-sectional rank IC;
- calibration/interval metrics if quantiles are requested.

## FDR and inference

Primary multiple-testing family = the two TimesFM cells.

Use 5-session moving blocks for paired sign-flip inference.

Report exact fold returns, p-values, BH q-values, confidence intervals where estimable, and full cost sensitivity.

## Stop rule

If neither TimesFM cell passes development, close the BTST TimesFM family and do not add more overnight technical variants.

If exactly one cell passes, only that cell proceeds to the untouched holdout.

If the holdout passes, the result remains a research finding requiring later independent-universe replication before manuscript promotion.

## License / execution boundary

TimesFM 3.0 remains research-only and non-executing under the project license gate. No real or paper broker execution is performed.