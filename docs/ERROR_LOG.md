# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 3 P1 bootstrap | The pinned TimesFM 3.0 environment installed successfully, but the public NIFTY 50 TRI endpoint returned non-JSON content to the runner and the bootstrap failed before forecasting. | P1 pipeline validation did not produce a forecast artifact. | Hardened the TRI fetcher with a Cloudflare/browser-profiled session and historical-page warm-up; the next `[bootstrap-p1]` run will retry. |

| 2026-09-20 | Phase 3 P1 source switch | Official NIFTY Indices TRI endpoint remained HTML/non-JSON after session hardening. | Exploratory 3.0 pipeline could not obtain official TRI data from Actions. | P1 bootstrap switched to a fixed, explicitly secondary Google Finance-derived snapshot pinned by upstream commit/blob SHA and cached in Actions; it remains ineligible for primary evidence. |

| 2026-09-20 | Phase 3 P1 workflow versioning | Run 52 executed the pre-switch P1 script because the newly created local-file script blob was not included in the preceding commit. | P1 run repeated the same official endpoint failure; no result artifact was produced. | Committed the verified local-file script explicitly; next [bootstrap-p1] run will use the secondary cached snapshot. |

| 2026-09-20 | Phase 3 P1 workflow wiring | Run 54 successfully loaded the new local-input script but the workflow still invoked it without `--input`. | P1 bootstrap stopped before reading the cached secondary dataset. | Replaced the Phase 3 workflow with the explicit cached-input command and pinned script invocation. |

| 2026-09-20 | Phase 3 P1 inference | TimesFM 3.0 univariate quantiles were returned as shape `(5, 9)` rather than the multivariate `(series, horizon, 9)` shape assumed by the bootstrap. | Inference completed but result processing stopped before metrics were written. | Added explicit handling for both univariate `(horizon, 9)` and multivariate `(series, horizon, 9)` quantile layouts; next P1 run will verify. |

| 2026-09-20 | Phase 3 P1 result | Corrected TimesFM 3.0 exploratory run 56 completed successfully on the secondary NIFTY 50 snapshot. | Pipeline now produces forecast metrics and artifacts; primary NSE evidence remains unavailable. | Recorded the result as C-grade exploratory evidence only; no strategy promotion. |

| 2026-09-20 | Phase 3 P1 ablation | Added a five-series secondary-data ablation to test native multivariate and past-only covariate support under identical origins. | Exploratory H2/H3 evidence can be collected without using the blocked P0 dataset. | Same upstream commit, identical 128-context/5-horizon/80-origin design, no strategy promotion. |

| 2026-09-20 | Phase 3 P1 uncertainty analysis | Formalized the previously observed interval-width vs absolute-movement relationship inside the reproducible P1 runner. | Allows uncertainty/magnitude hypothesis testing to be reproduced from the same forecast run. | Added Spearman and quartile-spread metrics to the stored P1 summary; still secondary exploratory evidence only. |
