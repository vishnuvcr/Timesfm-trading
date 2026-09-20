# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |
