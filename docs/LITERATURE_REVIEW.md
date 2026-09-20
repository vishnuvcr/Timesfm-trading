# Literature review — initial synthesis

## TimesFM 3.0

Google's August 2026 release describes TimesFM 3.0 as a zero-shot foundation model with native multivariate forecasting and flexible covariates, including past-only and past-and-future dynamic covariates. The official PyTorch model card describes a 20-layer transformer and quantile outputs.

The important distinction is licensing: the Google Research source code remains Apache-2.0, but the pretrained TimesFM 3.0 weights are distributed under the separate TimesFM Non-Commercial License v1.0. That license permits testing, evaluation and research not tied to commercial gain, production deployment or revenue generation. It states that commercial or production use requires a commercial license from Google.

**Research decision:** use TimesFM 3.0 as the primary model for this project. Do not treat the license restriction as a reason to exclude 3.0 from research. Treat it as a production-deployment gate.

## TimesFM 2.5

TimesFM 2.5 remains important as an Apache-licensed benchmark/ablation. It will tell us whether any NSE result is genuinely associated with 3.0's newer multivariate/covariate capabilities or can already be obtained from the older model.

## Financial evidence

Recent financial TSFM work finds strong model rankings in some equity-return tasks but small and sparse gains over random-walk baselines. A 2026 base-rate-honest TimesFM study shows that raw direction accuracy can be dominated by the market up-rate and reports no directional skill for its LoRA equity experiments.

A 2026 NSE-inclusive TimesFM benchmark reports a negative directional gate for zero-shot TimesFM on Indian equities and explores volatility sizing instead. This is an external benchmark, not a result of this project.

## Research implication

Do not assume 3.0 direction is alpha. Test:
- direction
- return magnitude
- range/volatility
- uncertainty calibration
- native multivariate inputs
- past-only causal covariates
- economic value after execution costs

Forecast quality, strategy quality and execution quality remain separate gates.


## New 3.0 options evidence — September 2026

A pre-registered September 2026 study tested TimesFM-3 on the SPY implied-volatility surface at 1- and 5-day horizons against random walk, AR(1), log-HAR, PCA-VAR and the market's own forward-variance-implied forecast. The study found that TimesFM configurations were competitive in forecast-loss terms, but recalibration removed much of the short-horizon advantage and the market's forward-variance forecast outperformed all models at ATM nodes. A residual signal remained on 25-delta wings, but the study stopped before an economic/fill test. This is strong methodological evidence for our options design, not evidence of a deployable NSE options edge. citeturn290367search0

**Protocol consequence:** Phase 5 will benchmark TimesFM 3.0 not only against statistical volatility models but also against the option market's own implied/forward-variance forecast. Any economic strategy must be tested after calibration, bid/ask, theta/vega/gamma effects and realistic fills.
