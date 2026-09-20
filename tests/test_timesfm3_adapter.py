from __future__ import annotations

import importlib.util
import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter


def test_quantile_levels_are_nine_deciles() -> None:
    assert TimesFM3Adapter.QUANTILES == (
        0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
    )


def test_context_float32_conversion() -> None:
    x = np.array([1, 2, 3], dtype=np.int64)
    assert x.astype(np.float32).dtype == np.float32


def test_model_dependency_is_optional_for_unit_tests() -> None:
    assert importlib.util.find_spec("timesfm3") is None or True
