# Provisional strategy candidates — not yet validated

These are pre-registered candidate rules derived from the research evidence. They are hypotheses, not recommendations or validated strategies.

## Common state variables

For each decision timestamp t, the common engine produces:
- forecast median return m;
- lower/upper forecast q10 and q90;
- forecast uncertainty u = q90 - q10, calibrated on prior walk-forward data;
- forecast volatility sigma_f;
- expected net move hurdle c = fees + spread + slippage + impact;
- regime state R;
- liquidity state L.

A trade is prohibited when PIT checks, liquidity, broker rules or the license gate fail.

## S1 — Scalping: cost-dominant range gate

Instrument universe: only highly liquid index/futures or the most liquid cash instruments supported by validated intraday data.

Signal:
- form TimesFM 3.0 short-horizon forecast distribution in research mode;
- estimate conservative movement as max(|q10|, |q90|) after calibration;
- trade only when conservative movement is greater than a pre-registered multiple of round-trip execution cost;
- direction can use an independent market-structure setup; TimesFM is the confirmation/range filter.

Sizing:
position size inversely proportional to forecast uncertainty, capped by participation and daily risk.

Stop/exit:
time stop, structure invalidation and hard loss cap; no averaging down.

Why this is being tested:
Scalping is likely to be dominated by spread, latency and adverse selection. A model that cannot forecast enough movement to clear costs should not be converted into trades.

## S2 — Intraday: setup plus forecast/range confirmation

Candidate setups:
- opening-range breakout;
- VWAP continuation/reversion;
- volatility expansion after compression.

Entry requirements:
1. setup signal passes;
2. TimesFM forecast sign/range is directionally consistent with the setup in research mode;
3. expected movement exceeds conservative cost hurdle;
4. India VIX/regime gate is compatible.

Sizing:
volatility-targeted, uncertainty-adjusted.

Primary comparison:
setup alone vs setup + TimesFM.

## S3 — BTST: overnight distribution gate

Decision at the final allowed pre-close timestamp.

Inputs:
- TimesFM next-open and next-close distribution;
- GIFT NIFTY / global market state available before decision;
- India VIX;
- USDINR;
- event/corporate-action filter.

Trade concept:
TimesFM first controls whether overnight exposure is justified by forecasted range relative to gap risk and cost. Directional selection is secondary and must beat the base-rate/persistence gate.

Comparison:
BTST rule without TimesFM vs BTST + TimesFM.

## S4 — Swing: volatility-targeted portfolio

Universe:
liquid NIFTY 50 names or a point-in-time index universe.

Core rule:
- rank or select using a separate permitted signal layer;
- use TimesFM forecast uncertainty/volatility to scale total equity exposure;
- reduce exposure when forecast volatility is high, increase toward target when forecast volatility is low;
- never exceed 100% gross exposure in the base case.

This is the strongest candidate suggested by the external evidence because a TimesFM Alpha Gate study found direction failing while forecast bands were usable for risk sizing, although a plain EWMA volatility meter was nearly as informative in that study. citeturn259680search0

Required test:
TimesFM uncertainty meter vs EWMA/VIX-only sizing, not TimesFM alone.

## S5 — Options: forecast range minus implied move

Universe:
NIFTY/BANKNIFTY options with validated historical quote/volume/OI data and executable spreads.

Signal:
forecast realized movement from TimesFM distribution minus market-implied movement from option prices.

Trade only when:
- forecast-vs-implied residual exceeds a calibrated threshold;
- the forecast edge survives market-implied baseline comparison;
- IV/skew/term structure is consistent with the structure;
- maximum loss is defined;
- spread and liquidity pass;
- total expected costs are below the residual edge.

Preferred structures:
- defined-risk debit spread;
- defined-risk long-vol spread;
- selected calendar/term-structure spread.

Do not promote naked short-vol structures from this rule.

## Cross-strategy consistency

All five candidates use the same:
- point-in-time data contract;
- TimesFM forecast cache;
- calibration method;
- economic edge calculation;
- cost model;
- portfolio risk limits;
- monitoring framework.

Only the strategy adapter changes.

## Promotion gate

No candidate becomes a validated strategy until it has:
- untouched walk-forward evidence;
- positive net expectancy under realistic costs;
- cost/slippage stress survival;
- multiple-regime stability;
- multiple-testing control;
- operational feasibility;
- a model/license path suitable for the intended trading use.
