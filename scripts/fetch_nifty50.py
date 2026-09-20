from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

ENDPOINT = "https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString"
INDEX_NAME = "NIFTY 50"
START_DATE = "01-Jan-2000"
END_DATE = "18-Sep-2026"


def fetch_rows(name: str = INDEX_NAME, start_date: str = START_DATE, end_date: str = END_DATE) -> list[dict[str, str]]:
    cinfo = (
        f"{{'name':'{name}','startDate':'{start_date}',"
        f"'endDate':'{end_date}','indexName':'{name}'}}"
    )
    payload = json.dumps({"cinfo": cinfo}).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.niftyindices.com/reports/historical-data",
        "User-Agent": "Mozilla/5.0 (compatible; TimesFM-NSE-research/1.0)",
    }
    req = Request(ENDPOINT, data=payload, headers=headers, method="POST")
    with urlopen(req, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))
    raw = body.get("d", "")
    rows = json.loads(raw) if isinstance(raw, str) else raw
    if not rows:
        raise RuntimeError("NIFTY 50 historical endpoint returned no rows")
    return rows


def normalize(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        dt = datetime.strptime(row["HistoricalDate"], "%d %b %Y").date()
        values = {
            "date": dt.isoformat(),
            "open": f"{float(row['OPEN']):.2f}",
            "high": f"{float(row['HIGH']):.2f}",
            "low": f"{float(row['LOW']):.2f}",
            "close": f"{float(row['CLOSE']):.2f}",
            "source_index": INDEX_NAME,
        }
        if float(values["high"]) < float(values["low"]):
            raise ValueError(f"high < low for {values['date']}")
        if min(float(values[k]) for k in ("open", "high", "low", "close")) <= 0:
            raise ValueError(f"non-positive price for {values['date']}")
        out.append(values)
    return sorted(out, key=lambda x: x["date"])


def main() -> None:
    output = Path("data/derived/nifty50_daily.csv")
    rows = normalize(fetch_rows())
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["date", "open", "high", "low", "close", "source_index"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"date range {rows[0]['date']} -> {rows[-1]['date']}")


if __name__ == "__main__":
    main()
