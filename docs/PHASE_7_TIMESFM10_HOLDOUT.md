# Phase 7 — TimesFM 10-session post-selection holdout

Updated: 2026-09-20 IST

## Candidate being tested

This holdout evaluates **one frozen candidate only**:

- individual-stock TimesFM 3.0 cross-sectional ranking;
- 10-session forecast horizon;
- long-only top-six equal-weight portfolio;
- 20-session momentum is the no-TimesFM control;
- no threshold tuning, hybrid-weight tuning or alternative horizon search.

The candidate was selected before this holdout from the Phase 4B 2/5/10/20-session bootstrap and cached PIT check.

## Holdout design

- Start date: 2023-01-01.
- Rebalance step: every 10 trading sessions.
- Holding horizon: 10 trading sessions.
- Context: 128 sessions.
- PIT eligibility is evaluated at each origin date using the Phase 2 monthly PIT universe.
- Candidate and control use the same eligible stock set.
- Position values drift with realized returns between rebalances before target reweighting.
- Final liquidation costs are explicitly charged.

This is a post-selection holdout. No result from the 2023+ holdout may be used to tune the candidate.

## Cost model

The cash-delivery cost model includes:
- ₹20 broker-per-executed-order reference stress;
- ₹13.5 Paytm Money delivery-sale DP charge reference;
- NSE cash-market transaction/IPFT total of ₹307 per crore per side;
- SEBI turnover fee of ₹10 per crore;
- cash-delivery STT 0.10% on both buy and sell;
- delivery stamp duty 0.015% on the buyer;
- GST at 18% on brokerage/exchange/SEBI service components;
- additional one-way slippage/impact stresses of 0, 0.125%, 0.25%, 0.375% and 0.50%.

Brokerage/DP assumptions are reference stresses because Paytm Money pricing can vary by account vintage; the holdout is not described as a contract-note reconstruction.

## Economic outputs

The workflow records:
- gross and net return;
- annualized periodized Sharpe;
- maximum drawdown;
- turnover;
- detailed cost components;
- maximum simulated trade participation relative to trailing 63-session turnover;
- annual and regime diagnostics;
- paired block sign-flip inference against momentum.

## Promotion gate

The candidate can only be discussed as surviving Phase 7 if:
1. net total return remains positive across the full slippage stress range;
2. it remains ahead of the no-TimesFM momentum control at the maximum stress;
3. block-aware paired inference and confidence diagnostics are reported;
4. participation/capacity and drawdown are operationally interpretable;
5. no test-period tuning or additional multiple-testing search is introduced.

Failure of the gate closes the current individual-stock TimesFM research lane. Passing means only research validation, not live execution authorization.

## Source limitations

The underlying price/PIT evidence is still the repository's 30-name bootstrap panel. TATAMOTORS has a known source-continuity end-date issue in the adjusted cache and is allowed to disappear only where the required origin/future observation is unavailable; the workflow records eligible-stock counts rather than silently forward-filling it.

The research remains non-executing and research-only.


## Holdout result and gate decision

The frozen candidate failed the post-selection holdout.

| Extra one-way slippage | TimesFM net return | Momentum net return | TimesFM max DD | TimesFM Sharpe |
|---|---:|---:|---:|---:|
| 0.00% | +3.72% | +67.97% | -25.13% | 0.144 |
| 0.125% | -7.93% | +47.20% | -28.83% | -0.075 |
| 0.25% | -18.30% | +28.96% | -32.35% | -0.295 |
| 0.375% | -27.52% | +12.94% | -36.79% | -0.515 |
| 0.50% | -35.72% | -1.12% | -41.46% | -0.736 |

The TimesFM candidate was below the momentum control at all five stress levels, including the zero-extra-slippage scenario. The paired period difference was negative throughout; one-sided block-signflip p-values were 0.972–0.984.

Capacity was not the limiting factor: maximum simulated participation was about 0.014% of trailing turnover.

### Final Phase 7 decision

**FAIL.** The single preselected 10-session TimesFM individual-stock candidate is closed. No further specification search is allowed on this completed stock holdout.

The result does not prove that all possible TimesFM/market combinations fail. It establishes that this frozen individual-stock mechanism did not survive a post-selection 2023+ cost-aware holdout.
