# Individual-stock strategy research design

## Scope correction

Individual NSE-listed stocks are first-class research instruments. Indices are not a gate that must be completed before stocks can be studied; the index and stock lanes run in parallel once their data-quality gates are satisfied.

The goal is to determine whether TimesFM adds useful information at the **stock level** after point-in-time controls, liquidity constraints and realistic trading costs.

## Research universe

### Bootstrap universe
A fixed 30-name liquid-stock panel is used only for engineering and pipeline validation. It is explicitly not final evidence because a fixed current list creates survivorship and membership bias.

### Final empirical universe
The final stock study uses a point-in-time universe built from historical liquidity/membership information. At each rebalance date, only information available by that date may determine eligibility. Securities that later delist, merge or change names are retained for the periods in which they were eligible.

Primary filters:
- minimum trailing trading history;
- minimum trailing turnover;
- no unresolved corporate-action discontinuity;
- exchange/series eligibility;
- maximum participation fraction for simulated orders.

The universe is frozen before the main holdout is evaluated.

## Individual-stock strategy families

### A. Single-stock forecast overlay
Baseline signal from a predeclared technical/statistical model; TimesFM contributes forecast median, range and uncertainty. Compare baseline versus baseline + TimesFM.

### B. Cross-sectional ranking
Rank eligible stocks by a forecast-derived quantity such as next-period return or forecast-minus-baseline residual. Evaluate rank IC first, then simulate a capped long-only portfolio. Any short leg must use a legally supported instrument and be modeled separately.

### C. Volatility-conditioned sizing
Use forecast uncertainty/volatility to scale an independent stock-selection signal. This is the main current hypothesis because preliminary evidence showed useful relationship between TimesFM interval width and future movement without evidence of standalone directional alpha.

### D. Stock-vs-index residual
Forecast the stock's residual return relative to a market/sector benchmark. Test whether TimesFM adds information beyond the index or sector baseline.

### E. Event-aware stock trading
Condition around corporate announcements, earnings, dividends/splits and other timestamped events only when the event was publicly available before the decision time. Event days must be isolated from ordinary sessions.

## Required stock-level controls

Every experiment records:
- stock symbol plus ISIN when available;
- trading session and forecast timestamp;
- point-in-time universe eligibility;
- raw execution price and analysis price separately;
- corporate-action state;
- trailing turnover/liquidity;
- expected spread/slippage/impact;
- brokerage/statutory charges;
- participation and position caps;
- sector and market regime.

## Statistical analysis

For stock-level forecast evaluation:
- per-stock MAE/RMSE and quantile losses;
- excess directional accuracy versus each stock's own contemporaneous base rate;
- cross-sectional rank IC;
- Diebold-Mariano or block-bootstrap paired losses where appropriate;
- cross-sectional clustered uncertainty when aggregating many stocks.

For strategy evaluation:
- net expectancy, Sharpe, drawdown and turnover;
- fold-by-fold and regime-by-regime results;
- FDR across stocks and strategy cells;
- Deflated Sharpe or comparable selection correction if search is broad;
- capacity/participation stress.

## Cost realism

EOD stock research cannot claim actual fill quality from OHLC alone. Where executable intraday quote data are unavailable, simulations use conservative slippage/impact stress bands and do not label the result execution-validated. High-frequency stock strategies require separate intraday/tick data.

## Stop rule

A stock-level candidate is promoted only if the same frozen gate used for index strategies is satisfied: PIT-clean data, forecast improvement, net-positive simulated economics after costs, stress survival, multi-fold/multi-regime stability and multiple-testing control.
