# Phase 4 intraday strategy status

Updated: 2026-09-20 IST

## Status

**Strategy gate active. Source gate passed on ten fixed liquid F&O underlyings.**

The immediate experiment is the frozen 15/30/60-minute TimesFM-vs-VWAP matrix defined in docs/PHASE_4_INTRADAY_STRATEGY_MATRIX.md.

No tuning or execution recommendation is permitted.

## Source gate result

Workflow: 35532034119
Artifact: 10611856047
Release SHA-256: 20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2

All ten symbols passed the frozen source-integrity rules.

## Next gate

Run the 15/30/60-minute development/holdout experiment exactly as defined. If a development cell survives, fold 4 remains an untouched holdout.


## Matrix execution marker — 2026-09-20

Running the predeclared 15/30/60-minute TimesFM-vs-VWAP experiment with the validated ten-stock minute release.


## Inference optimization — 2026-09-20

The first matrix implementation is computationally expensive because it invokes TimesFM once per origin. A second workflow batches eight origins (up to 80 stock contexts) per model call while keeping the exact same horizon, origin, fold, baseline, cost and promotion protocol. This is an engineering optimization only.


## Batched execution marker — 2026-09-20

Run the identical predeclared matrix using batched model calls.


## Final development result — 2026-09-20

The frozen 15/30/60-minute TimesFM-vs-VWAP matrix completed successfully (workflow 35532255630; artifact 10612146229).

No horizon passed the development rule:
- 15m block p=0.4381, BH q=0.6125;
- 30m p=0.3043, BH q=0.6125;
- 60m p=0.6125, BH q=0.6125.

TimesFM return MAE was worse than persistence at every horizon. No fold-4 holdout was opened.

Decision: close this intraday strategy family. Move to the predeclared BTST/overnight lane rather than adding intraday indicators or thresholds.
