# Project instructions

This repository implements the research workflow for TimesFM trading research on NSE.

## Governance
- Maintain a phased plan and do not silently change it; material plan changes update docs/RESEARCH_PLAN.md and are logged.
- Each research phase gets a separate Git branch named phase-<n>-<slug>.
- Every phase has a manually runnable GitHub Actions workflow.
- Important datasets and forecast caches are versioned or content-addressed where licensing permits. Do not redistribute data whose terms prohibit redistribution.
- Every execution outcome is recorded in experiment/status logs.
- Every error is recorded in docs/ERROR_LOG.md with date, stage, symptom, root cause (when known), fix and regression control.
- README.md is updated with phase status and links.
- No research conclusion is promoted to paper/live trading without a reproducible walk-forward result and cost-aware validation.
- Do not store secrets in Git; use GitHub Actions secrets or local environment variables.

## Model policy
- TimesFM 3.0 is the primary research model.
- TimesFM 2.5 is the comparison/ablation/fallback model.
- Record the exact model repository, commit/version, configuration and model hash in every run manifest.
- Treat the current TimesFM 3.0 pretrained-weight license as a research/non-production constraint. Do not move 3.0 outputs into live/production trading until licensing is explicitly cleared.
- Do not infer that 3.0's stronger general forecasting benchmarks imply trading alpha.

## Scope
Unless a sub-study explicitly excludes them, the research universe should consider NSE cash equity, NIFTY-family indices, futures/options, India VIX, FII/FPI and DII activity, option-chain/OI/IV/skew, market regimes/sentiment, global market cross-effects, corporate actions, and timestamped news.

## Trading realism
All net-performance calculations must model brokerage, exchange/SEBI statutory charges, STT, stamp duty, GST where applicable, slippage/spread, liquidity/participation constraints, option-specific effects, expiry/settlement mechanics, and financing/MTF costs when used.

## Scientific standards
Use walk-forward validation, point-in-time datasets, explicit naive/statistical baselines, confidence intervals, forecast-loss comparisons, FDR control for multiple testing, and sensitivity analysis.

## Reproducibility
Every experiment should have run id, code/model commit, data manifest/hash, model checkpoint/version, feature configuration, horizon/context, execution assumptions, random seeds where applicable, output paths, and a pass/fail gate.

Private chain-of-thought is not stored. The chat log stores user requests, observable decisions, tool/data outcomes, errors and repository changes.
