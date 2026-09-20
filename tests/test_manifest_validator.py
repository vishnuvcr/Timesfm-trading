from pathlib import Path

from src.data.validate_manifest import validate_manifest


def test_phase2_smoke_manifest_is_valid() -> None:
    path = Path("data/manifests/phase2_smoke.json")
    assert validate_manifest(path) == []


def test_future_availability_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(
        (
            '{"dataset_id":"bad","source_id":"x","retrieved_at":'
            '"2026-09-20T13:00:00+00:00","sha256":"'
            '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",'
            '"schema_version":"x","storage_class":"tier_a_public",'
            '"availability_timestamp":"2026-09-20T14:00:00+00:00",'
            '"pit_validated":true}'
        ),
        encoding="utf-8",
    )
    errors = validate_manifest(path)
    assert any("availability_timestamp" in error for error in errors)
