# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 3 P1 bootstrap | The pinned TimesFM 3.0 environment installed successfully, but the public NIFTY 50 TRI endpoint returned non-JSON content to the runner and the bootstrap failed before forecasting. | P1 pipeline validation did not produce a forecast artifact. | Hardened the TRI fetcher with a Cloudflare/browser-profiled session and historical-page warm-up; the next `[bootstrap-p1]` run will retry. |

| 2026-09-20 | Phase 3 P1 source switch | Official NIFTY Indices TRI endpoint remained HTML/non-JSON after session hardening. | Exploratory 3.0 pipeline could not obtain official TRI data from Actions. | P1 bootstrap switched to a fixed, explicitly secondary Google Finance-derived snapshot pinned by upstream commit/blob SHA and cached in Actions; it remains ineligible for primary evidence. |
