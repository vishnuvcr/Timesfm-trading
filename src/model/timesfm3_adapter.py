from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class ForecastBatch:
    forecast: np.ndarray
    quantiles: np.ndarray | None
    quantile_levels: tuple[float, ...]
    model_id: str
    checkpoint: str


class TimesFM3Adapter:
    DEFAULT_CHECKPOINT = "google/timesfm-3.0-pytorch"
    QUANTILES = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)

    def __init__(
        self,
        checkpoint: str = DEFAULT_CHECKPOINT,
        device: str = "cpu",
        per_core_batch_size: int = 8,
    ) -> None:
        try:
            from timesfm3 import ModelConfig, TimesFM3Evaluator
        except ImportError as exc:
            raise RuntimeError(
                "TimesFM 3.0 is not installed. Install the pinned research environment."
            ) from exc

        config = ModelConfig(
            checkpoint_path=checkpoint,
            per_core_batch_size=per_core_batch_size,
            device=device,
        )
        self._model = TimesFM3Evaluator(config)
        self.checkpoint = checkpoint
        self.device = device

    def predict_batch(
        self,
        contexts: Iterable[np.ndarray],
        horizon: int,
        past_only_covariates: Iterable[np.ndarray | None] | None = None,
        past_future_covariates: Iterable[np.ndarray | None] | None = None,
        *,
        univariate: bool = False,
        return_quantiles: bool = True,
        use_symmetric_averaging: bool = True,
    ) -> list[ForecastBatch]:
        contexts_list = [np.asarray(x, dtype=np.float32) for x in contexts]
        po = ([None if x is None else np.asarray(x, dtype=np.float32) for x in past_only_covariates]
              if past_only_covariates is not None else None)
        pf = ([None if x is None else np.asarray(x, dtype=np.float32) for x in past_future_covariates]
              if past_future_covariates is not None else None)

        outputs = self._model.predict_batch(
            contexts=contexts_list,
            horizon=horizon,
            past_only_covariates=po,
            past_future_covariates=pf,
            return_quantiles=return_quantiles,
            use_symmetric_averaging=use_symmetric_averaging,
            univariate=univariate,
        )

        result: list[ForecastBatch] = []
        for out in outputs:
            quantiles = None if out.quantiles is None else np.asarray(out.quantiles)
            forecast = np.asarray(out.forecast)
            result.append(ForecastBatch(
                forecast=forecast,
                quantiles=quantiles,
                quantile_levels=self.QUANTILES if quantiles is not None else (),
                model_id="timesfm-3.0-pytorch",
                checkpoint=self.checkpoint,
            ))
        return result
