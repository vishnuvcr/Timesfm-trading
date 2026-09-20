from __future__ import annotations

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter


def main() -> None:
    rng = np.random.default_rng(7)
    context_len = 128
    horizon = 24

    target = np.stack([
        np.sin(np.linspace(0, 18, context_len)),
        np.cos(np.linspace(0, 16, context_len)),
        rng.normal(0, 0.05, context_len),
    ]).astype(np.float32)

    past_only = rng.normal(0, 1, (1, context_len)).astype(np.float32)

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=1,
    )
    outputs = model.predict_batch(
        [target],
        horizon=horizon,
        past_only_covariates=[past_only],
        return_quantiles=True,
        univariate=False,
    )
    out = outputs[0]
    assert out.forecast.shape == (3, horizon)
    assert out.quantiles is not None
    assert out.quantiles.shape == (3, horizon, 9)
    print("TimesFM 3.0 smoke test passed:", out.forecast.shape, out.quantiles.shape)


if __name__ == "__main__":
    main()
