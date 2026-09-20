# Error log

| Date | Stage | Error / surprise | Impact | Fix / control |
|---|---|---|---|---|
| 2026-09-20 | Repo bootstrap | GitHub connector issue-list query first used unsupported state value `all`. | Validation failure only; no data loss. | Retried with supported state value. |
| 2026-09-20 | Repo bootstrap | README fetch returned repository-empty 404. | Confirmed no prior repo state to preserve. | Treat empty repo as baseline and record initialization explicitly. |
| 2026-09-20 | Repo bootstrap | One batched repository-write request was blocked by tool safety validation. | No content loss; some files in the batch were committed before the block. | Re-read the branch after the failed batch and resumed with smaller sequential writes. |

| 2026-09-20 | Research design | Initial plan treated TimesFM 3.0 as evaluation-only for the research stage. | Research scope was narrower than the user's requested model. | Verified current official 3.0 license/README; promoted 3.0 to primary research model and retained 2.5 as benchmark/fallback. | 

| 2026-09-20 | Phase 3 statistics | Local pytest initially failed because the repository `src` package was not on the test import path. | Unit tests could not collect. | Added `src/__init__.py` and made the manual workflow use `PYTHONPATH=.` before pytest. |

| 2026-09-20 | Literature audit | An external TimesFM Alpha Gate README describes no 3.0 directional skill in US and Indian equities, but its displayed table only reports a 3.0 US result and a 2.5 India result. | Treating prose as a measured Indian 3.0 result would overstate evidence. | Evidence ledger now requires exact table/result provenance; unreported 3.0 India figures are not used as measurements. |

| 2026-09-20 | Phase 4 risk-engine extension | Phase 3 P1 evidence showed forecast interval width may contain movement-magnitude information, but the risk engine previously required an already-computed scalar uncertainty. | Could not pass native quantile uncertainty directly into the shared sizing primitive. | Added a half-width `interval_uncertainty` adapter with tests; it is simulation-only and does not alter the empirical promotion gate. |

| 2026-09-20 | Phase 4 CI validation | New interval-width test compared floating-point half-width to exact decimal 0.10 and failed at 0.10000000000000003. | One strategy-unit test failed despite correct arithmetic. | Changed test to `pytest.approx`; regression control retains the crossed-bound assertion. |


| 2026-09-20 | Phase 4.1 stock overlay | Initial draft mixed 30-name signal vectors with a 6-name portfolio state and would have produced a dimension mismatch at the first rebalance. | Backtest was intentionally stopped before inference results were interpreted. | Corrected portfolio weights to length 30 and separated buy/sell fixed-order costs; syntax/unit checks then passed before the empirical run. |
| 2026-09-20 | Phase 4.1 empirical result | Completed successfully on 30 stocks and 32 five-session rebalances, but TimesFM-only and hybrid selection were weaker than the momentum control and became more negative under cost stress. | No runtime failure; this is an empirical negative result. | Stored diagnostics and rejected promotion of the simple TimesFM stock-selection overlays. |


| 2026-09-20 | Phase 4.2 nested regime test | A simple low-breadth TimesFM-minus-momentum residual looked positive only when evaluated with a threshold influenced by all folds. | That apparent improvement would contain look-ahead/selection bias. | Recast the rule as a strict nested walk-forward: each fold's breadth threshold uses only prior folds; the resulting residual strategy lost to momentum at every cost scenario. |
| 2026-09-20 | Phase 4 daily stock overlay gate | Standalone TimesFM ranking, simple hybrid, momentum-gated TimesFM and nested regime-conditioned residual all failed their respective gates on the 30-name bootstrap. | No daily individual-stock TimesFM strategy is validated from the current evidence. | Close this strategy lane unless a material new economic mechanism or authorized/PIT-clean dataset justifies a protocol amendment. |
