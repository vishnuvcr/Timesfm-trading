from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
import zipfile
import io

UDIFF_START = date(2024, 7, 8)
MONTHS = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC")
HOSTS = ("https://archives.nseindia.com", "https://nsearchives.nseindia.com")

@dataclass(frozen=True)
class ArchivePlan:
    trade_date: date
    format: str
    filename: str
    urls: tuple[str, ...]


def _compact(d: date) -> str:
    return d.strftime("%Y%m%d")


def _legacy(d: date) -> str:
    return f"{d.day:02d}{MONTHS[d.month-1]}{d.year}"


def plan_for_date(trade_date: date) -> ArchivePlan:
    if trade_date >= UDIFF_START:
        filename = f"BhavCopy_NSE_FO_0_0_0_{_compact(trade_date)}_F_0000.csv.zip"
        path = f"/content/fo/{filename}"
        fmt = "udiff"
    else:
        filename = f"fo{_legacy(trade_date)}bhav.csv.zip"
        path = f"/content/historical/DERIVATIVES/{trade_date.year}/{MONTHS[trade_date.month-1]}/{filename}"
        fmt = "legacy"
    return ArchivePlan(trade_date, fmt, filename, tuple(h + path for h in HOSTS))


def iter_weekdays(start: date, end: date):
    cur = start
    while cur <= end:
        if cur.weekday() < 5:
            yield cur
        cur += timedelta(days=1)


def download_archive(trade_date: date, output_dir: Path, timeout_s: int = 45) -> Path | None:
    plan = plan_for_date(trade_date)
    destination = output_dir / str(trade_date.year) / f"{trade_date.month:02d}" / plan.filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        return destination

    headers = {
        "Accept": "application/zip,application/octet-stream;q=0.9,*/*;q=0.8",
        "Referer": "https://www.nseindia.com/all-reports-derivatives",
        "User-Agent": "Mozilla/5.0 (compatible; TimesFM-NSE-research/1.0)",
    }
    last_error: Exception | None = None
    for url in plan.urls:
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=timeout_s) as response:
                payload = response.read()
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                names = zf.namelist()
                csv_names = [n for n in names if n.lower().endswith(".csv")]
                if not csv_names:
                    raise ValueError("archive contains no CSV")
                if len(csv_names) != 1:
                    raise ValueError(f"expected one CSV entry, found {len(csv_names)}")
            tmp = destination.with_suffix(destination.suffix + ".part")
            tmp.write_bytes(payload)
            tmp.replace(destination)
            return destination
        except Exception as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    return None
