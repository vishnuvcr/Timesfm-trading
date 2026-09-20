import pytest

from src.model.timesfm3_adapter import TimesFM3Adapter


def test_timesfm3_adapter_blocks_non_research_purpose() -> None:
    with pytest.raises(PermissionError):
        TimesFM3Adapter(purpose="production")
