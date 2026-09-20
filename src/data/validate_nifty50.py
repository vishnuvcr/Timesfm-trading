from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

REQUIRED = {"date", "open", "high", "low", "close", "source_index"}


def validate(path: Path = Path("data/derived/nifty50_daily.csv")) -> tuple[int, str, str]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise ValueError("dataset is empty")
    missing = REQUIRED - set(rows[0])
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")

    dates = [date.fromisoformat(r["date"]) for r in rows]
    if dates != sorted(dates):
        raise ValueError("dates are not sorted")
    if len(set(dates)) != len(dates):
        raise ValueError("duplicate dates")

    for row in rows:
        values = {k: float(row[k]) for k in ("open", "high", "low", "close")}
        if min(values.values()) <= 0:
            raise ValueError(f"non-positive price: {row['date']}")
        if values["high"] < values["low"]:
            raise ValueError(f"high < low: {row['date']}")
        if not (values["low"] <= values["open"] <= values["high"]):
            raise ValueError(f"open outside range: {row['date']}")
        if not (values["low"] <= values["close"] <= values["high"]):
            raise ValueError(f"close outside range: {row['date']}")

    return len(rows), rows[0]["date"], rows[-1]["date"]


if __name__ == "__main__":
    n, start, end = validate()
    print(f"validated {n} NIFTY 50 rows: {start} -> {end}")
