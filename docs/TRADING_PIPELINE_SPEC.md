# Consistent NSE trading pipeline — TimesFM 3.0

## Design objective
Use one common decision engine across five holding styles. The strategy-specific component is the mapping from forecast/risk state to trade structure.

## Canonical flow
1. Data snapshot: point-in-time prices, market/derivative state, global inputs, events/news, corporate actions, broker/exchange rules.
2. Feature timeline: normalize timestamps to Asia/Kolkata, attach availability timestamps, reject future information, freeze the feature manifest.
3. TimesFM 3.0 forecast: univariate baseline, multivariate targets, causal past-only covariates, future-known covariates only when truly known, p10-p90 distribution.
4. Forecast calibration: point loss, quantile loss, interval coverage, calibration by regime/horizon, uncertainty score.
5. Economic edge: convert forecast to expected tradable movement, subtract execution hurdle and risk penalty, reject non-positive net edge.
6. Regime gate: trend/range, India VIX, liquidity, event proximity, expiry state, global risk state.
7. Strategy adapter: scalping, intraday, BTST, swing or options.
8. Position sizing: signal strength, forecast uncertainty, volatility, liquidity and portfolio exposure.
9. Execution simulator: timestamp, order type, delay, partial fills, spread, impact/slippage and broker rules.
10. Cost engine: dated fee manifest, exchange/statutory charges, brokerage, taxes, financing and settlement.
11. Position/P&L ledger: fills, margin, realized/unrealized P&L, option Greeks and cost attribution.
12. Monitoring: data freshness, forecast calibration, rolling skill, realized costs, turnover, drawdown and model checksum/version.

## Common decision object
A candidate trade records timestamp, instrument, side, strategy, forecast, uncertainty, regime, expected move, cost hurdle, edge, size, max loss and execution rule.

A decision is rejected when data freshness, point-in-time integrity, forecast gate, expected edge, liquidity, risk limits or broker constraints fail.

## Strategy adapters

### Scalping
Targets 1/3/5/10 intraday bars. The primary hurdle is round-trip spread/slippage and latency. TimesFM 3.0 is used for short-horizon range/volatility and confirmation rather than assumed raw direction.

### Intraday
Targets 15/30/60 minutes. Candidate setups are trend, reversion, breakout, ORB and VWAP timing. TimesFM provides conditioning and range/timing information.

### BTST
Targets next open, next close and two-session return. Key inputs include GIFT NIFTY, global close, USDINR, India VIX and events. TimesFM provides the overnight distribution.

### Swing
Targets 2/5/10/20 sessions. Candidate setups are ranking, sector rotation and volatility sizing. TimesFM provides multi-day expected return/range and uncertainty.

### Options
Targets underlying return/range plus IV/skew. Candidate structures are defined-risk directional spreads, forecast-range-versus-implied-move trades and selected term-structure/volatility spreads. TimesFM is treated as residual information after market-implied movement.

## Portfolio controls
- maximum single-name exposure;
- maximum sector exposure;
- maximum market beta;
- maximum overnight exposure;
- maximum option gamma/vega/theta;
- maximum daily loss;
- drawdown response;
- maximum turnover;
- maximum volume participation;
- minimum expected edge/cost ratio.

## Promotion ladder
Research → backtest → stress backtest → paper execution → monitored paper → licensed production candidate → staged live.

The TimesFM 3.0 pretrained-weight license gate sits between licensed production candidate and live production.

## Core philosophy
TimesFM is an information source, not the risk manager. The engine must remain safe if TimesFM is removed and must never bypass data, cost, liquidity or risk controls.