# Phase 7 status

Updated: 2026-09-20 IST

## Status

**Cost-engineering bootstrap complete; empirical walk-forward waits for frozen P0 data and Phase 3 forecast gate.**

## Implemented

- Date-versioned fee manifest remains the source of rates.
- Execution-event model counts actual unique executed F&O orders rather than signals.
- Current 2026 STT rules are represented for cash delivery, cash intraday sales, futures sales and option sales.
- Paytm Money F&O brokerage and intraday square-off charges are represented.
- Spread and slippage are explicit cost components.
- Forced square-off is represented as an execution event.
- Option slippage is modeled at contract level rather than using underlying-equity slippage as a proxy.

## Walk-forward gate

Every promoted simulation must report gross and net P&L, brokerage, statutory charges, spread/slippage, turnover, cost per trade and break-even slippage. Stressed scenarios must include higher spread/impact and incomplete fills where data permit.

No strategy is promoted until the P0 data gate, Phase 3 forecast gate, realistic execution model and multiple-testing controls pass.


## Phase 7 frozen candidate — 2026-09-20

A single post-selection candidate is now registered for the final cost-aware holdout:

- TimesFM 3.0 cross-sectional stock ranking;
- 10-session horizon;
- top-six long-only;
- 20-session momentum control;
- 2023-01-01+ holdout;
- 10-session non-overlapping rebalances;
- PIT eligibility at each origin;
- position-drift-aware rebalancing;
- explicit final liquidation;
- dated cash-equity brokerage/statutory/DP model;
- one-way slippage/impact stresses from 0 to 0.50%;
- capacity, year/regime and block-aware inference diagnostics.

No tuning or alternative TimesFM variants are permitted in this holdout. The Phase 4B candidate remains research-only and non-executing.


## Final Phase 7 holdout result — 2026-09-20

Workflow 35527715462 / artifact 10610571439 completed the frozen post-selection holdout.

Holdout:
- 91 non-overlapping 10-session rebalances from 2023-01-02 through 2026-09-03;
- mean PIT-eligible names 29.76, minimum 29, maximum 30;
- fixed TimesFM 3.0 10-session ranking, top six, no tuning;
- 20-session momentum control;
- dated cash-equity statutory/broker/DP model;
- one-way slippage/impact stress 0%, 0.125%, 0.25%, 0.375%, 0.50%;
- position drift and explicit final liquidation.

Net total return:
- 0% extra slippage: TimesFM +3.72% vs momentum +67.97%;
- 0.125%: TimesFM -7.93% vs momentum +47.20%;
- 0.25%: -18.30% vs +28.96%;
- 0.375%: -27.52% vs +12.94%;
- 0.50%: -35.72% vs -1.12%.

TimesFM was below momentum at every stress level. At the maximum stress, TimesFM maximum drawdown was -41.46% versus -23.80% for momentum; periodized Sharpe was -0.736 versus +0.059.

Paired block inference was negative for TimesFM at every cost level. The one-sided block-signflip p-values ranged from 0.972 to 0.984. Maximum simulated trade participation was only about 0.014% of trailing turnover, so capacity was not the binding explanation.

**Decision:** reject and close the single frozen Phase 4B stock candidate. No current individual-stock TimesFM strategy is validated. No additional TimesFM threshold, horizon, hybrid or regime search is permitted on the completed stock holdout.

