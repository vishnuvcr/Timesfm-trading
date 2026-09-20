# Phase 4B full-session minute-source validation

## Research question

Does the candidate 1-minute source have enough session-level structural integrity and cross-source reconciliation to support genuine BTST/intraday experimentation?

## Predeclared gate

Five liquid bootstrap names are checked on two dates (2022-01-03 and 2025-01-02). For each symbol/date:
- retrieve all 09:15–15:29 IST bars through the Hugging Face Dataset Viewer filter API;
- require 375 one-minute bars;
- require exact one-minute spacing, no duplicate timestamps and valid OHLC;
- report zero-volume bars;
- aggregate open/high/low/close/volume and compare with the TejHQ raw EOD cache;
- price relative tolerance = 0.5%;
- volume relative tolerance = 2%.

This is deliberately a source-quality gate, not proof of tradeability or fill accuracy.
