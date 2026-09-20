# Cost model — frozen design principles

## Purpose

No economic result is accepted unless gross and net performance are both reported and the net calculation is reproducible from an effective-date fee manifest.

## Current 2026 regulatory inputs

NSE's current STT schedule, effective April 1, 2026:
- sale of an option: 0.15% of option premium, seller;
- option exercised: 0.15% of intrinsic value, purchaser;
- sale of a futures contract: 0.05% of traded value, seller;
- cash-equity delivery purchase/sale: 0.10% each side under the current NSE table. citeturn571953search0turn571953search2

These replace older pre-April-2026 assumptions in any backtest that spans the rate change. The cost engine must support date-varying rates rather than applying a single lifetime constant.

## Paytm Money broker inputs

The current Paytm Money F&O FAQ states brokerage of ₹10 for each unique executed F&O order. Partial executions can create additional order-level brokerage/tax effects, so the simulator must model executions rather than simply counting strategy signals. citeturn571953search4turn571953search5

Paytm Money states that intraday F&O positions are auto-squared within the final 15 minutes of the normal session and that a 75% initial-margin loss threshold can trigger RMS square-off. Its RMS policy also notes that the eligible intraday scrip list can change with market conditions. citeturn571953search1turn571953search32

The Paytm Money overnight F&O FAQ states an intraday square-off charge of ₹50 + applicable taxes per order. ATS/options strategy-builder intraday positions have an earlier 3:10 pm auto-square-off timing. citeturn571953search3

These are execution constraints, not optional cost assumptions. The simulator must be able to reject trades that would violate broker operational rules.

## Cash equity

Model separately:
- brokerage;
- exchange/clearing charges;
- SEBI charges;
- STT;
- stamp duty;
- GST on applicable components;
- spread;
- slippage/market impact;
- DP/depository costs where applicable;
- financing/MTF if used.

## Futures

Model:
- brokerage;
- exchange/clearing charges;
- GST;
- current STT;
- spread and impact;
- funding/carry;
- roll cost;
- broker RMS/auto-square-off constraints.

## Options

Model at contract level:
- brokerage per actual execution;
- exchange/clearing charges;
- current STT regime;
- stamp duty;
- GST;
- bid/ask;
- execution slippage;
- volume/open-interest/liquidity filters;
- theta;
- vega;
- gamma;
- IV/skew/term-structure movement;
- expiry/settlement;
- physical-delivery consequences where relevant;
- margin and financing;
- broker-specific square-off/position rules.

Do not use underlying-equity slippage as an option fill proxy.

## Slippage scenarios

Every strategy is evaluated under at least:
1. half-spread proxy;
2. spread + volatility impact;
3. volume/participation impact;
4. 2× stressed spread/impact;
5. non-100% fill probability where data permit.

For scalping, the primary cost measure is round-trip execution friction as a fraction of forecasted expected movement.

## Economic outputs

Every run must report:
- gross P&L;
- net P&L;
- total costs;
- brokerage;
- statutory/exchange charges;
- spread/slippage;
- financing;
- cost/trade;
- turnover;
- average holding time;
- break-even slippage;
- break-even total cost.

## Effective-date principle

The final simulator reads an effective-date fee table rather than hard-coding current charges into strategy code. When tax/broker rules change, the historical simulation automatically applies the correct vintage.

## Research warning

A positive gross strategy is not an edge. A strategy can pass forecast tests and still fail after the current STT regime, broker fees, spread and realistic execution constraints.
