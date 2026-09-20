# Phase 4B frozen experiment matrix

## Research question
Does TimesFM 3.0 add useful information at different individual-stock holding periods after the previously tested daily ranking mechanism failed?

## Test cells

| Lane | Target | Horizon | Baseline | TimesFM signal | Extra mechanism |
|---|---|---:|---|---|---|
| Swing | adjusted log price / return | 2 sessions | 20d momentum | H-session forecast return | none |
| Swing | adjusted log price / return | 5 sessions | 20d momentum | H-session forecast return | none |
| Swing | adjusted log price / return | 10 sessions | 20d momentum | H-session forecast return | none |
| Swing | adjusted log price / return | 20 sessions | 20d momentum | H-session forecast return | none |
| Swing | adjusted log price / return | 2/5/10/20 | 20d momentum | — | TimesFM inverse-interval-width sizing |
| BTST | next-session open | 1 session | predeclared short-horizon baseline | open/gap target forecast | gated on intraday source |
| Intraday | 15/30/60 min | session-relative | persistence + VWAP/EMA baseline | TimesFM return/range | gated on minute data |
| Scalping | 1/3/5/10 min | session-relative | persistence/mean-reversion | TimesFM return/range | gated on execution data |

## Common settings
- 30-stock bootstrap panel for engineering only.
- context 128.
- chronological 4-fold split.
- 8 non-overlapping rebalances per fold and horizon.
- long-only top-6 stock portfolio for selection tests.
- all costs reported in gross and net form.
- one-way proportional stress: 0.125%, 0.25%, 0.375%, 0.50%.
- ₹20/order brokerage stress and ₹13.5 delivery-sale DP reference in the current cash-equity simulator; historical effective-date fee tables remain the Phase 7 requirement. Paytm Money publicly documents the ₹13.5 delivery-sale DP charge split in its October 2024 update. citeturn437184search3
- no shorting in the bootstrap strategy test.

## Primary comparisons
1. TimesFM forecast vs persistence on point/return error.
2. TimesFM selection vs 20d momentum.
3. uncertainty-scaled momentum vs unscaled momentum.
4. gross vs net economics under all cost scenarios.

## Statistical plan
- paired fold-level loss differences;
- paired permutation/sign-flip p-values for strategy return differences;
- Benjamini-Hochberg FDR across the predeclared swing strategy cells;
- fold/regime and stock concentration diagnostics;
- no selection on final test outcomes.

No result is promoted to final manuscript evidence until PIT and Phase 7 gates are complete.
