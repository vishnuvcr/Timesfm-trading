from __future__ import annotations

from datetime import datetime
from typing import Iterable


def validate_feature_timeline(rows: Iterable[dict], forecast_origin: datetime) -> None:
    for row in rows:
        available = datetime.fromisoformat(row["available_time"])
        event = datetime.fromisoformat(row["event_time"])
        if available < event and not row.get("is_future_known", False):
            raise ValueError(f"availability precedes event without future-known flag: {row['feature_id']}")
        if available > forecast_origin and not row.get("is_future_known", False):
            raise ValueError(f"future information leaked at {forecast_origin.isoformat()}: {row['feature_id']}")


def validate_revision_order(rows: Iterable[dict]) -> None:
    state: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["feature_id"], row["vintage_id"])
        revision = int(row.get("revision_number", 0))
        if revision < 0:
            raise ValueError(f"negative revision: {key}")
        if key in state and revision < state[key]:
            raise ValueError(f"revision order decreased: {key}")
        state[key] = revision
