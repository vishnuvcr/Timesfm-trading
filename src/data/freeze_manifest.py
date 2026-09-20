from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_manifest(path: Path, dataset_id: str, source_id: str, schema_version: str, storage_class: str, source_url: str, pit_validated: bool, availability_timestamp: str | None = None, row_count: int | None = None) -> dict:
    return {
        "dataset_id": dataset_id,
        "source_id": source_id,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "availability_timestamp": availability_timestamp,
        "sha256": sha256_file(path),
        "row_count": row_count,
        "schema_version": schema_version,
        "storage_class": storage_class,
        "revision": None,
        "source_url": source_url,
        "pit_validated": pit_validated,
        "notes": None,
    }


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--dataset-id", required=True)
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--schema-version", required=True)
    ap.add_argument("--storage-class", required=True)
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--pit-validated", action="store_true")
    ap.add_argument("--availability-timestamp")
    ap.add_argument("--row-count", type=int)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()
    obj=make_manifest(Path(args.file), args.dataset_id, args.source_id, args.schema_version, args.storage_class, args.source_url, args.pit_validated, args.availability_timestamp, args.row_count)
    Path(args.output).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
