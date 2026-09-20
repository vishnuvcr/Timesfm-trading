# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |


| 2026-09-20 | Phase 6.1 regime inference | Initial design risked pseudo-replication by pooling stock observations for significance testing. | Could have understated uncertainty because observations within a rebalance are cross-sectionally dependent. | Corrected to rebalance-level rank-IC permutation testing before empirical execution, then applied Benjamini-Hochberg FDR across predeclared regime cells. |
| 2026-09-20 | Phase 6.1 empirical result | No predeclared regime cell showed statistically supported incremental TimesFM information; risk-on overlay's small gross advantage disappeared under cost stress. | No strategy candidate survived the regime/cost gate. | Stop stock-strategy variant search and move to final audit/manuscript; untested stress/high-vol cells are explicitly labeled as data-sparse rather than null. |
