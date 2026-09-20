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
