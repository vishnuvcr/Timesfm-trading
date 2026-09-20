from __future__ import annotations

import csv
import json
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

import requests

REF_URL = "https://www.nseindia.com/reports-indices-historical-index-data"
API_BASE = "https://www.nseindia.com/api/historicalOR/indicesHistory"
INDEX = "NIFTY 50"
CHUNK_DAYS = 89


class NseIndexHistory:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": REF_URL,
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.nseindia.com",
                "Connection": "keep-alive",
            }
        )

    def warm(self) -> None:
        for url in ("https://www.nseindia.com", REF_URL):
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
        time.sleep(0.5)

    def fetch(self, start: date, end: date) -> list[dict]:
        if start > end:
            raise ValueError("start > end")
        self.warm()
        rows: list[dict] = []
        cursor = start
        while cursor <= end:
            chunk_end = min(cursor + timedelta(days=CHUNK_DAYS), end)
            url = (
                f"{API_BASE}?indexType={quote(INDEX)}"
                f"&from={cursor:%d-%m-%Y}&to={chunk_end:%d-%m-%Y}"
            )
            last_error = None
            for attempt in range(3):
                try:
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()
                    payload = response.json()
                    data = payload.get("data")
                    if not isinstance(data, list):
                        raise RuntimeError(
                            f"unexpected payload keys: {list(payload)[:10]}"
                        )
                    rows.extend(data)
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    time.sleep(2 + attempt * 3)
                    if attempt == 1:
                        self.warm()
            if last_error is not None:
                raise RuntimeError(
                    f"failed chunk {cursor:%Y-%m-%d} to {chunk_end:%Y-%m-%d}: {last_error}"
                ) from last_error
            cursor = chunk_end + timedelta(days=1)
            time.sleep(1.5)
        return rows


def normalize(rows: list[dict]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        required = (
            "EOD_TIMESTAMP",
            "EOD_OPEN_INDEX_VAL",
            "EOD_HIGH_INDEX_VAL",
            "EOD_LOW_INDEX_VAL",
            "EOD_CLOSE_INDEX_VAL",
        )
        if any(k not in row for k in required):
            continue
        values = {
            "date": str(row["EOD_TIMESTAMP"]),
            "open": f"{float(row['EOD_OPEN_INDEX_VAL']):.2f}",
            "high": f"{float(row['EOD_HIGH_INDEX_VAL']):.2f}",
            "low": f"{float(row['EOD_LOW_INDEX_VAL']):.2f}",
            "close": f"{float(row['EOD_CLOSE_INDEX_VAL']):.2f}",
            "index_name": str(row.get("EOD_INDEX_NAME", INDEX)),
        }
        if min(float(values[k]) for k in ("open", "high", "low", "close")) <= 0:
            raise ValueError(f"non-positive OHLC: {values}")
        if not (float(values["low"]) <= float(values["open"]) <= float(values["high"])):
            raise ValueError(f"open outside range: {values}")
        if not (float(values["low"]) <= float(values["close"]) <= float(values["high"])):
            raise ValueError(f"close outside range: {values}")
        out.append(values)
    dedup = {x["date"]: x for x in out}
    return [dedup[k] for k in sorted(dedup)]


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["date", "open", "high", "low", "close", "index_name"],
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = normalize(
        NseIndexHistory().fetch(
            date.fromisoformat(args.start),
            date.fromisoformat(args.end),
        )
    )
    if not rows:
        raise RuntimeError("No usable NIFTY 50 rows returned")

    write_csv(rows, Path(args.output))
    print(
        json.dumps(
            {
                "rows": len(rows),
                "first": rows[0]["date"],
                "last": rows[-1]["date"],
                "output": args.output,
                "source": API_BASE,
            },
            indent=2,
        )
    )
