# Phase 5 options protocol — TimesFM 3.0

## Core question

Does TimesFM 3.0 add information about future underlying return/range or implied-volatility dynamics beyond what NSE option prices already imply, and can that residual survive realistic option execution costs?

## Core benchmark rule

Do not infer option profitability from underlying forecast accuracy. Every options experiment must compare against both naive/statistical models and the option market's own implied forecast, including forward-variance information where constructible.

Recent TimesFM-3 research on the SPY implied-volatility surface found that the market's forward-variance-implied forecast beat TimesFM at ATM nodes even where TimesFM was competitive in raw forecast-loss comparisons. That study stopped before a full fill/P&L test.

## Strategy families

### A. Defined-risk directional
- long call/put;
- debit call/put spread;
- delta-targeted vertical spread.

Entry requires an underlying forecast edge, uncertainty gate, liquidity gate, IV/skew check, maximum premium-at-risk and explicit DTE/expiry rule.

### B. Forecast-range versus implied-move
Compare TimesFM q10/q90 or forecast realized volatility with the option market's implied movement. Trade only when the residual exceeds calibration error and the full cost hurdle.

### C. Volatility strategies
Use defined-risk long-vol or bounded short-vol structures and selected calendar/term-structure spreads. Unbounded short straddles/strangles are not primary promotion candidates.

### D. Surface relative-value
Study 25-delta put, ATM and 25-delta call; front/back expiry; and delta-matched relationships. Model skew, vega, theta and execution explicitly.

## Contract selection

Filter by underlying, expiry, strike, DTE, delta, OI, volume, bid/ask width, quote freshness, moneyness, corporate-action state and contract lifecycle. Store the exact exchange contract identifier.

## Greeks

At minimum calculate delta, gamma, theta, vega, IV, realized volatility and TimesFM forecast volatility/range. Reports separate P&L attribution into delta, gamma, theta/carry, vega/IV change and execution/cost.

## Expiry and settlement

Use dated official NSE contract specifications. Never assume one expiry calendar across the entire historical sample.

## Current 2026 option cost rule

NSE's April 1, 2026 STT schedule applies 0.15% to sale of an option, based on premium, and 0.15% to an option that is exercised, based on intrinsic value. Other broker/exchange charges are applied through the dated fee manifest.

## Primary statistical tests

Forecast layer: pinball loss, weighted interval score, q10–q90 coverage, Diebold-Mariano against random walk/AR/market-implied forecasts, and model-confidence/recalibration tests when justified.

Trading layer: net P&L, P&L/risk, Sharpe/Sortino, maximum drawdown, tail loss/expected shortfall, turnover, total cost, break-even spread and break-even forecast error.

## Promotion gate

An options family advances only if the forecast component adds information beyond naive and market-implied baselines; option P&L stays positive after frozen costs; results survive spread/slippage stress and multiple expiry/regime folds; tail risk is bounded; and trades are executable under the broker's operational rules.

## Prohibited shortcut

Never convert a positive TimesFM underlying forecast directly into a naked option purchase without an explicit, tested mapping from forecast distribution to contract/structure.
