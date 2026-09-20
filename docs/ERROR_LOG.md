# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 2 validation | Direct container clone of GitHub repository failed because github.com could not be resolved. | End-to-end repository test could not run in the container. | Ran the exact validator logic in an isolated offline harness; GitHub Actions remains the canonical CI execution path. |
