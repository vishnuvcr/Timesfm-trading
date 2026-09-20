from __future__ import annotations

import hashlib
import json
from pathlib import Path

REQUIRED = {
    "dataset_id",
    "source_id",
    "retrieved_at",
    "sha256",
    "schema_version",
    "storage_class",
}

ALLOWED_STORAGE = {
    "tier_a_public",
    "tier_b_artifact",
    "tier_c_private_licensed",
}


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    obj = json.loads(path.read_text(encoding="utf-8"))

    missing = REQUIRED - obj.keys()
    if missing:
        errors.append(f"{path}: missing required fields: {sorted(missing)}")

    if obj.get("storage_class") not in ALLOWED_STORAGE:
        errors.append(f"{path}: invalid storage_class")

    digest = obj.get("sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        errors.append(f"{path}: sha256 must be a 64-character lowercase hex string")
    elif any(c not in "0123456789abcdef" for c in digest):
        errors.append(f"{path}: sha256 contains non-hex characters")

    if obj.get("pit_validated") is not True:
        errors.append(f"{path}: pit_validated must be true before research use")

    availability = obj.get("availability_timestamp")
    retrieved = obj.get("retrieved_at")
    if availability and retrieved and availability > retrieved:
        errors.append(
            f"{path}: availability_timestamp must not be later than retrieved_at"
        )

    return errors


def validate_directory(directory: Path) -> int:
    files = sorted(directory.glob("*.json"))
    if not files:
        print("No manifest JSON files found.")
        return 0

    all_errors: list[str] = []
    for path in files:
        all_errors.extend(validate_manifest(path))

    if all_errors:
        print("\n".join(all_errors))
        return 1

    print(f"Validated {len(files)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate_directory(Path("data/manifests")))
