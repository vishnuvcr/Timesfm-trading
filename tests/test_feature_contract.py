from datetime import datetime, timezone

import pytest

from src.regimes.feature_contract import validate_feature_timeline, validate_revision_order


def test_future_feature_is_rejected() -> None:
    origin = datetime(2026, 1, 10, 10, tzinfo=timezone.utc)
    rows = [{
        "feature_id": "india_vix_close",
        "event_time": "2026-01-10T15:30:00+00:00",
        "available_time": "2026-01-10T15:31:00+00:00",
        "is_future_known": False,
    }]
    with pytest.raises(ValueError):
        validate_feature_timeline(rows, origin)


def test_future_known_feature_is_allowed() -> None:
    origin = datetime(2026, 1, 10, 10, tzinfo=timezone.utc)
    rows = [{
        "feature_id": "scheduled_expiry_date",
        "event_time": "2026-01-10T00:00:00+00:00",
        "available_time": "2026-01-05T00:00:00+00:00",
        "is_future_known": True,
    }]
    validate_feature_timeline(rows, origin)


def test_revision_order_is_monotone() -> None:
    rows = [
        {"feature_id": "macro_cpi", "vintage_id": "2026Q1", "revision_number": 0},
        {"feature_id": "macro_cpi", "vintage_id": "2026Q1", "revision_number": 1},
    ]
    validate_revision_order(rows)


def test_revision_order_decrease_is_rejected() -> None:
    rows = [
        {"feature_id": "macro_cpi", "vintage_id": "2026Q1", "revision_number": 1},
        {"feature_id": "macro_cpi", "vintage_id": "2026Q1", "revision_number": 0},
    ]
    with pytest.raises(ValueError):
        validate_revision_order(rows)
