# TimesFM 3.0 license gate

## Current source-of-record wording

Google's current TimesFM 3.0 pretrained-weight license is the TimesFM Non-Commercial License v1.0.

The license defines Non-Commercial Purpose as testing, evaluation or research not tied to commercial gain, production deployment or revenue generation. It explicitly excludes revenue-generating activity and use of outputs in commercial decision-making, and it prohibits commercial or production use of the model or its outputs. citeturn670140view0

## Project consequence

Because this project is intended to develop an NSE trading system that may generate trading returns, we do not treat 3.0 pretrained outputs as cleared for a profit-seeking trading decision under the current license.

Therefore:
- 3.0 remains the primary scientific/evaluation model.
- 3.0 may be used for qualifying non-commercial forecasting research.
- 3.0 outputs are not promoted into a revenue-generating trading rule unless explicit commercial permission/license is obtained.
- The production research lane currently uses TimesFM 2.5 or another separately licensed model.
- If Google grants commercial rights later, the 3.0-derived strategy must be revalidated end-to-end under the licensed setup.

## What this gate does not mean

It does not mean TimesFM 3.0 is technically unsuitable for finance. It means the pretrained weights currently have a restrictive license.

The source repository's code is Apache-2.0, but that does not override the separate weight license. citeturn285712search1turn670140view0

## Review trigger

Re-check this file before any trading-strategy optimization using 3.0, paper/live bridge, client-facing research or decision service, distribution of 3.0-derived outputs, or commercial fine-tuning/distillation.

This is a research governance control, not legal advice.
