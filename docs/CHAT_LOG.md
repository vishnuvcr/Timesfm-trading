# Chat / decision log

## 2026-09-20

**User request:** Deep research on using TimesFM for NSE trading across scalping, intraday, BTST, swing and options, with a consistent trading pipeline; repository: `vishnuvcr/Timesfm-trading`.

**Recorded actions/outcomes**
- Inspected repository metadata: public repo, default branch `main`, initially empty.
- Created phased research plan and governance files.
- Started evidence review using Google Research/TimesFM, arXiv/Hugging Face research, NSE official materials and Paytm Money official materials.
- Identified license constraint: TimesFM 3.0 pretrained weights are currently non-commercial/non-production; TimesFM 2.5 remains the practical deployable research lane under Apache-2.0 weights.
- Identified evidence that raw directional accuracy can be misleading and that TSFM gains over naive financial baselines may be small; the project therefore uses a forecast gate and economic-value gate.
- No live strategy has been approved.

Private chain-of-thought is not copied here; this log records observable decisions and outcomes.


## 2026-09-20 — Phase 6.1 regime-conditioned stock result

The next planned experiment tested TimesFM only as an incremental residual around a 20-session momentum control, with predeclared market-state, liquidity and post-corporate-action conditioning. Rebalance-level permutation tests and Benjamini-Hochberg FDR were used.

No predeclared regime produced statistically supported residual rank information. The risk-on overlay was slightly better than momentum before costs but underperformed after 0.25% and 0.50% one-way stress.

**Decision:** stop adding stock strategy variants. The individual-stock EOD research lane has reached a negative promotion conclusion; move to final audit/manuscript and document data-gated future research rather than continue specification search.
