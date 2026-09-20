# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 2 validation | Direct container clone of GitHub repository failed because github.com could not be resolved. | End-to-end repository test could not run in the container. | Ran the exact validator logic in an isolated offline harness; GitHub Actions remains the canonical CI execution path. |

| 2026-09-20 | Phase 2 CI validation | Latest Phase 2 validation run 19 failed because src/data/validate_manifest.py contained an unterminated string literal at the multi-error print statement. | Data-validation job stopped before data-layer tests. | Replaced the malformed string with print("\\n".join(all_errors)); next CI run must confirm the fix. |

| 2026-09-20 | Phase 2 public P0 acquisition | GitHub Actions run 40 reached the official NIFTY 50 historical endpoint but received a non-JSON challenge/HTML response, causing JSON parsing to fail. | Official P0 cache was not created. | Switched the fetcher to a browser-profiled Cloudflare session with an initial historical-data page GET; next tagged acquisition run will retry with this handshake. |

| 2026-09-20 | Phase 2 CI wiring | Hardened acquisition code imported `cloudscraper`, but the acquisition job's dependency-install step had not been updated, causing run 44 to fail immediately with ModuleNotFoundError. | Second P0 acquisition attempt did not reach the endpoint. | Added `pip install cloudscraper` to the acquisition job; next tagged run will exercise the actual fetcher. |

| 2026-09-20 | Phase 2 official P0 acquisition | Final retry (run 51) still received the NIFTY Indices HTML application page with HTTP 200 instead of JSON. | Official NIFTY 50 P0 cache could not be created after four acquisition attempts. | Stop repeated retries; opened issue #6 and require an authorized/official data-delivery route or alternate official endpoint before resuming the P0 acquisition loop. |

| 2026-09-20 | Phase 2 source discovery | NSE's official Historical Index Data page exposes a distinct `/api/historicalOR/indicesHistory` route. Reproducible NSE clients use 89-day chunks with session warm-up. | Opens a potentially usable official P0 path without changing the research plan. | Added a bounded historical/current probe; promotion requires successful probes and full manifest validation. |

| 2026-09-20 | Phase 2 probe CI wiring | The new official NSE historical-index probe imported `requests`, but its job did not install the dependency; run 58 stopped with ModuleNotFoundError before network access. | Probe did not test the alternate official endpoint. | Added explicit `requests` installation to the probe job. |

| 2026-09-20 | Phase 2 source probe | Added a final test path using the official `nsearchives.nseindia.com/content/indices/ind_close_all_DDMMYYYY.csv` static archive, which community parsers document as containing NIFTY 50 OHLC. | Determines whether the static NSE archive host is reachable from GitHub Actions despite the main/API 403s. | Single-date probe only; promotion requires successful access and a scalable historical acquisition design. |
