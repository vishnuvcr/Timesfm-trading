# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 3 statistics | Local pytest initially failed because the repository `src` package was not on the test import path. | Unit tests could not collect. | Added `src/__init__.py` and made the manual workflow use `PYTHONPATH=.` before pytest. |

| 2026-09-20 | Literature audit | An external TimesFM Alpha Gate README describes no 3.0 directional skill in US and Indian equities, but its displayed table only reports a 3.0 US result and a 2.5 India result. | Treating prose as a measured Indian 3.0 result would overstate evidence. | Evidence ledger now requires exact table/result provenance; unreported 3.0 India figures are not used as measurements. |
