# TimesFM 3.0 license gate

## Current source-of-record wording

Google's current TimesFM 3.0 pretrained-weight license is the TimesFM Non-Commercial License v1.0.

The license defines Non-Commercial Purpose as testing, evaluation or research not tied to commercial gain, production deployment or revenue generation. It explicitly excludes revenue-generating activity and use of outputs in commercial decision-making, and it prohibits commercial or production use of the model or its outputs. citeturn670140view0

## Project consequence

The project has been deliberately scoped as **non-executing scientific research**. Under that scope:
- 3.0 remains the primary research/evaluation model;
- 3.0 may be used for forecasting evaluation, strategy-hypothesis generation, simulated/cost-aware backtesting, statistical analysis and manuscript preparation, provided the work remains within the license's Non-Commercial Purpose;
- simulated strategy results are research findings, not commercial trading decisions;
- no broker order placement, production system, paid service, client deliverable or revenue-generating use of 3.0 outputs is permitted within this project;
- TimesFM 2.5 is retained only as a benchmark/ablation model.

This does not provide a legal opinion about any external future use. The license should be reviewed whenever the project purpose, audience, distribution model or downstream use changes.

## What this gate does not mean

It does not mean TimesFM 3.0 is technically unsuitable for finance. It means the pretrained weights currently have a restrictive license.

The source repository's code is Apache-2.0, but that does not override the separate weight license. citeturn285712search1turn670140view0

## Review trigger

Re-check this file before any broker execution, production deployment, client-facing research, paid service, revenue-generating use, commercial model derivative, or other commercial decision-making using 3.0 outputs.

This is a research governance control, not legal advice.
