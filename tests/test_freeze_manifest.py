from pathlib import Path

from src.data.freeze_manifest import make_manifest


def test_manifest_hash_is_deterministic(tmp_path: Path) -> None:
    payload=tmp_path / "sample.bin"
    payload.write_bytes(b"timesfm-nse")
    a=make_manifest(payload,"sample","test","v1","tier_a_public","https://example.invalid",True)
    b=make_manifest(payload,"sample","test","v1","tier_a_public","https://example.invalid",True)
    assert a["sha256"] == b["sha256"]
    assert len(a["sha256"]) == 64
