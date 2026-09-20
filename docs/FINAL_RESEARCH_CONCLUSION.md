# Current research conclusion — 2026-09-20

## Individual-stock EOD/multiday lane

The current individual-stock EOD/multiday TimesFM research sequence is complete under the present protocol.

Completed gates:
1. 30-stock TimesFM 3.0 forecast bootstrap.
2. Four-fold chronological robustness over 4,800 stock-level origins.
3. Direct stock selection versus an independent 20-session momentum control.
4. Nested regime-conditioned incremental test.
5. Frozen Phase 4B 2/5/10/20-session swing matrix.
6. PIT eligibility rerun for the surviving 10-session candidate.
7. Frozen Phase 7 post-selection 2023+ holdout with dated cash-equity costs and slippage stress.

## Final holdout result

The only candidate advanced to Phase 7 was:
- TimesFM 3.0;
- 10-session cross-sectional ranking;
- top-six long-only portfolio;
- fixed 20-session momentum control;
- no holdout tuning.

Holdout: 91 non-overlapping ten-session rebalances from 2023-01-02 through 2026-09-03, with 29–30 PIT-eligible names per origin.

| Extra one-way slippage | TimesFM net return | Momentum net return |
|---|---:|---:|
| 0.00% | +3.72% | +67.97% |
| 0.125% | -7.93% | +47.20% |
| 0.25% | -18.30% | +28.96% |
| 0.375% | -27.52% | +12.94% |
| 0.50% | -35.72% | -1.12% |

TimesFM was behind momentum at every stress level, including zero added slippage.

At 0.50% extra slippage:
- TimesFM maximum drawdown: -41.46%;
- TimesFM periodized Sharpe: -0.736;
- momentum maximum drawdown: -23.80%;
- momentum periodized Sharpe: +0.059.

Paired block-signflip p-values were 0.972–0.984 one-sided. Maximum simulated TimesFM participation was about 0.014% of trailing turnover, so capacity was not the limiting explanation.

## Scientific inference

**No individual-stock EOD/multiday TimesFM 3.0 strategy has been validated by this research program.**

The earlier 10-session Phase 4B result was a real exploratory candidate, but it did not survive the untouched post-selection holdout. The correct inference is negative for this tested mechanism, not a universal claim that every possible TimesFM strategy must fail.

## Scope that remains open

The following are not being presented as validated:
- intraday;
- BTST;
- scalping;
- options;
- cross-market event-conditioned strategies.

The next permitted lane is a materially different intraday/BTST/scalping mechanism, beginning with minute-data integrity and execution-quality validation. Historical options remain gated on authorized historical option-chain/IV/OI data.

## Strengths

Frozen candidate selection; chronological evaluation; independent baseline; PIT eligibility; dated cost model; multiple slippage stresses; explicit liquidation; capacity diagnostics; block-aware inference; and an explicit no-further-search rule after holdout failure.

## Limitations

The stock evidence uses a 30-name bootstrap panel rather than a full survivorship-free universe. The minute-data source has passed only a structural probe so far. The fee model is a research reference model rather than a contract-note reconstruction for every historical account configuration. Statistical power for sparse chronological blocks is limited.

## Future direction

The next scientific question is whether TimesFM provides incremental information at shorter horizons when paired with execution-aware microstructure baselines. That lane must first pass session completeness, duplicate/gap, volume, OHLC, daily aggregation and fill-model validation before any P&L experiment is promoted.
