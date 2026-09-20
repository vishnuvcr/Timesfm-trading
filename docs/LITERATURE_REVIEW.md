# Literature review — initial synthesis

TimesFM is a general time-series forecasting foundation model, not a stock-specific alpha model. TimesFM 2.5 is the practical open-weight lane; TimesFM 3.0 adds stronger multivariate/covariate support but its current pretrained-weight terms restrict commercial/production use.

Recent financial TSFM research finds strong model rankings in some equity return tasks but small and sparse gains over random-walk baselines. A 2026 base-rate-honest TimesFM study shows that raw direction accuracy can be dominated by the market up-rate and reports no directional skill for its LoRA equity experiments.

A 2026 NSE-inclusive TimesFM benchmark reports a negative directional gate for zero-shot TimesFM on Indian equities and explores volatility sizing instead. This is an external benchmark, not a result of this project.

Research implication: forecast quality, strategy quality and execution quality are separate gates. TimesFM may be useful as a filter, uncertainty/risk input, regime input or timing layer even when direct direction fails.
