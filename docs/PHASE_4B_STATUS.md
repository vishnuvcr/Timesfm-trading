# Phase 4B status — individual-stock multifrequency research

Updated: 2026-09-20 IST

## Scope
Phase 4B follows closure of the daily individual-stock TimesFM overlay lane. It tests materially different holding-period/target mechanisms rather than reopening arbitrary daily TimesFM ranking thresholds.

Primary lanes:
- Swing: 2, 5, 10 and 20-session targets using the adjusted daily stock cache.
- BTST: next-session open/overnight targets, only after intraday/open data pass the source-quality gate.
- Intraday: 15, 30 and 60-minute targets using validated 1-minute data.
- Scalping: 1, 3, 5 and 10-minute targets only after execution-quality validation.

## Governance
TimesFM 3.0 remains the primary scientific model. All work is research-only and non-executing.

The fixed 30-stock cache is an engineering/bootstrap panel, not final survivorship-safe evidence. Any positive finding here is exploratory until replicated on the point-in-time universe.

## Frozen swing experiment
For each horizon H in {2,5,10,20} sessions:
- context = 128 sessions;
- target = adjusted log price;
- TimesFM forecast return = predicted log price at H minus origin log price;
- independent baseline = 20-session cross-sectional momentum;
- TimesFM ranking = raw H-session forecast return;
- uncertainty mechanism = momentum signal scaled within each stock by inverse TimesFM q10-q90 forecast width;
- long-only top-6 portfolio;
- chronological 4-fold evaluation;
- 8 non-overlapping rebalances per fold/horizon;
- no test-fold threshold tuning;
- cost stress = 0.125%, 0.25%, 0.375% and 0.50% one-way proportional friction plus broker/order-level costs.

The uncertainty mechanism is an explicit hypothesis test, not a post-result optimization.

## Forecast gate
For each horizon:
- MAE and RMSE versus persistence;
- target-horizon return MAE;
- directional excess versus contemporaneous positive-return base rate;
- rank IC;
- q10-q90 coverage;
- forecast-width/realized-movement association.

## Strategy gate
A swing cell is not promoted merely because it beats another tested cell. It must:
1. beat the independent momentum control after costs;
2. remain stable across chronological folds;
3. survive the stressed cost range;
4. avoid single-stock or single-fold concentration;
5. remain eligible for multiple-testing correction.

Phase 7 remains the final cost-aware walk-forward gate.

## BTST/intraday data gate
The candidate HF source xxparthparekhxx/indian-stock-market-minute-data reports 1-minute NSE data from 2022–2026, roughly 713–715 million rows, UTC timestamps, OHLCV and OI, and an MIT license in its published metadata. This is a candidate source, not exchange-primary evidence. citeturn461402search0turn461402search4

Before using it for BTST/intraday:
- validate schema and symbol continuity;
- validate UTC-to-IST session mapping;
- verify 09:15–15:30 regular-session coverage;
- quantify missing/duplicate bars;
- test OHLC consistency;
- test zero/abnormal volume rates;
- compare daily close/open aggregation against the EOD stock cache;
- check corporate-action discontinuities;
- preserve source/version/hash metadata.

NSE documents normal equity trading as 09:15–15:30, with a separate pre-open session. citeturn437184search0turn437184search1

A close-to-close daily return is not labeled BTST. Genuine BTST requires a next-session open/close execution path.

## Stop rule
Do not expand the swing search beyond the predeclared horizon/mechanism matrix unless a protocol amendment is recorded. Weak cells stop at the phase gate.
