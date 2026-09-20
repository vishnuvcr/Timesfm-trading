# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 3 statistics | Local pytest initially failed because the repository `src` package was not on the test import path. | Unit tests could not collect. | Added `src/__init__.py` and made the manual workflow use `PYTHONPATH=.` before pytest. |

| 2026-09-20 | Literature audit | An external TimesFM Alpha Gate README describes no 3.0 directional skill in US and Indian equities, but its displayed table only reports a 3.0 US result and a 2.5 India result. | Treating prose as a measured Indian 3.0 result would overstate evidence. | Evidence ledger now requires exact table/result provenance; unreported 3.0 India figures are not used as measurements. |

| 2026-09-20 | License audit | Earlier project notes described 3.0 research/backtesting as permissible without clearly separating research intent from revenue-generating use. Official license language is stricter: Non-Commercial Purpose excludes revenue generation/commercial decision-making and restrictions extend to outputs. | Could have blurred the boundary between non-commercial research and commercial decision-making. | Scoped the project explicitly to non-executing scientific research/simulation; 3.0 remains the primary research model and 2.5 is benchmark/ablation only. |

| 2026-09-20 | CI validation | Phase 3 pull-request CI failed because a unit-test fixture expected MAE 1/3 while the correct value for the fixture is 0.5. | CI blocked despite correct implementation. | Corrected the test expectation to 0.5; later CI passed. |
| 2026-09-20 | Tooling | Attempted to call an unavailable GitHub pull-request lookup tool. | No repository impact. | Use available GitHub PR/workflow tools and commit SHA queries. |

| 2026-09-20 | CI validation | Phase 3 pull-request CI run 25 found a second fixture arithmetic error: RMSE expectation used 0.25/3 instead of 1.25/3. | CI remained red even though the metric implementation matched the mathematical definition. | Corrected the fixture; later CI passed. |

| 2026-09-20 | Tooling | A GitHub workflow-job tool call used the wrong repository argument field name. | Tool validation failure only; no repository impact. | Corrected the argument to the connector's required `repo_full_name` field. |
| 2026-09-20 | Phase 2 CI validation | Phase 2 run 19 failed because `src/data/validate_manifest.py` contained an unterminated string literal in the multi-error print statement. | Data-validation stopped before data-layer tests. | Fixed the statement to `print("\\n".join(all_errors))`; Phase 2 run 30 then passed source-registry, manifest and data-layer validation. |

| 2026-09-20 | Phase 5 CI validation | First options CI run failed on exact equality of a floating-point residual (0.015000000000000003 vs 0.015). | CI red despite correct arithmetic. | Corrected the fixture to use pytest.approx; run 38 passed. |

| 2026-09-20 | Phase 2 official acquisition | Final public P0 NIFTY attempt again returned HTML/non-JSON with HTTP 200. | Primary NIFTY P0 dataset unavailable from the runner route. | Closed the repeated retry loop; issue #6 tracks the blocker. Primary research now requires authorized/alternate official data delivery. |
