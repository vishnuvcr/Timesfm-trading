# Individual-stock TimesFM strategy gate conclusion

Updated: 2026-09-20 IST

## Research question

Does TimesFM 3.0 add economically useful incremental information to individual-NSE-stock selection after chronological robustness checks, an independent selection baseline, regime conditioning and explicit trading costs?

## Evidence completed

### Phase 3 stock forecast gate
30-stock bootstrap, 5-session horizon, context 128, 40 recent origins per stock:
- mean log MAE: 0.018675 vs persistence 0.017629;
- mean log RMSE: 0.027242 vs 0.025726;
- only 3/30 stocks improved MAE;
- only 3/30 improved RMSE.

Four-fold robustness extension:
- 30 stocks × 4 folds × 40 origins = 4,800 origins;
- mean MAE difference TimesFM-minus-persistence: +0.001144;
- mean RMSE difference: +0.001470;
- mean 5-session return-MAE difference: +0.001885;
- mean directional excess: -2.90 percentage points;
- 13/30 stocks had non-negative mean directional excess;
- no stock had a negative mean MAE difference across all four folds.

### Phase 4.1 stock selection
Compared:
- 20-session cross-sectional momentum;
- TimesFM 5-session forecast ranking;
- 50/50 standardized hybrid;
- momentum-gated TimesFM.

Across 30 stocks and 32 sparse five-session rebalances:
- momentum mean rank IC: +0.0138;
- TimesFM mean rank IC: -0.0237;
- hybrid mean rank IC: -0.0151.

At 0.125% one-way proportional cost:
- equal-weight universe: about -7.3% net total return;
- momentum: about -15.2%;
- TimesFM-only: about -26.6%;
- hybrid: about -21.8%.

These were exploratory stress-cost simulations, not final effective-date Phase 7 calculations.

### Phase 4.2 nested regime-conditioned incremental test
Predeclared rule:
- define market breadth as the fraction of stocks with positive 20-session return;
- estimate the low-breadth threshold from prior folds only;
- compute the rank residual z(TimesFM 5-session forecast) minus z(20-session momentum);
- select the top six stocks only in the low-breadth regime;
- test on folds 2–4 without parameter selection on test folds.

At 0.125% one-way:
- momentum control: -5.20%;
- TimesFM residual: -10.02%.

At 0.25%:
- momentum: -7.72%;
- residual: -12.22%.

At 0.375%:
- momentum: -10.16%;
- residual: -14.37%.

At 0.50%:
- momentum: -12.55%;
- residual: -16.48%.

The conditional TimesFM residual lost to the independent momentum control at every tested cost level.

## Inference

The evidence does not support a validated daily individual-stock TimesFM strategy on the current 30-name alternate-data research panel.

The recent directional excess seen in the first 40-origin bootstrap was not robust to chronological broadening. The simple TimesFM selector, hybrid selector and nested regime-conditioned residual all failed to add incremental value over the declared control.

This is a research conclusion, not a claim that individual-stock trading is impossible. The conclusion is specifically that the tested TimesFM mechanisms have not established incremental economic value under the current data, horizons, controls and cost assumptions.

## Strengths

- Individual stocks were treated as first-class instruments.
- Multiple chronological folds were used.
- The initial positive-looking directional result was subjected to a broader robustness test.
- Phase 4 used an independent stock-selection comparator.
- The apparent regime improvement was re-tested under nested walk-forward rules to remove hindsight.
- Costs were stressed rather than reported only gross.
- All failures and interpretation changes are logged in the repository.

## Limitations

- The current 30-name stock panel is an engineering/bootstrap universe, not final exchange-primary PIT evidence.
- TATAMOTORS has a shorter adjusted-price history than most names and requires identifier/source reconciliation.
- The official NSE hosted-runner P0 route remains blocked.
- The Phase 4.1 rebalance sample is sparse.
- The current cost scenarios are stress references rather than the final effective-date fee engine.
- Intraday/scalping execution quality has not been established from exchange-grade tick/quote data.
- The external Yahoo/yfinance cross-check covers only a small subset of names.
- The experiments do not yet use the full regime/external-information feature set (India VIX, FII/DII, global lead/lag, news, event timestamps).

## Decision

**Close the current daily individual-stock TimesFM overlay gate.**

Do not generate more TimesFM stock-ranking thresholds or simple combinations inside this protocol merely in search of a positive backtest.

A future stock strategy may reopen the gate only through a material protocol amendment backed by a new economic mechanism or a newly authorized/PIT-clean data layer. The amendment must be frozen before testing and must include the no-TimesFM control, realistic costs, walk-forward validation and multiple-testing correction.

## Future research

The most defensible future directions are:
- authorized point-in-time broader stock universe and identifier continuity;
- stock-vs-sector/market residual targets rather than raw returns;
- event-conditioned research using timestamped corporate/news availability;
- higher-quality intraday data for scalping/intraday questions;
- TimesFM comparison with local supervised models and TimesFM 2.5 on identical folds;
- options research only after authorized historical option-chain data are available.

These are future research directions, not implied strategy recommendations.
