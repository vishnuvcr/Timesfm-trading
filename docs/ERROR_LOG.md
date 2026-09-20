# Error log

This branch inherits the project error history and adds Phase 2-specific corrections. See main `docs/ERROR_LOG.md` for the complete cross-phase record.

## 2026-09-20 — alternate stock acquisition workflow
- The first TejHQ workflow design used a job-level marker condition that produced non-executable/no-job attempts. It was replaced with a path-filtered push trigger plus an unconditional job and manual inputs.
- A cache-commit attempt failed after successful acquisition/validation because branch state had advanced during overlapping workflow runs. Subsequent controlled runs completed the cache commit.

## 2026-09-20 — corporate-action validation
- Adding `*_actions.csv` files caused the price validator to interpret them as OHLCV files. Run 35521851050 failed at validation.
- The validator was split into price-file and action-file validation. Run 35521951823 then passed acquisition and validation.

## 2026-09-20 — cached-price/action interaction
- The acquisition script initially skipped the rest of the symbol loop when a cached price file existed, which also skipped newly requested corporate actions.
- The script was refactored so cached prices are reused while actions are independently fetched/cached when `--actions` is enabled.

## 2026-09-20 — stock-data identity caveat
- Raw cached TejHQ price rows have blank `series`/`isin` fields for some historical rows, while the separate action files contain ISIN/company metadata.
- Final PIT stock evidence therefore requires an identifier/history reconciliation step rather than assuming the raw price CSV alone is sufficient.
