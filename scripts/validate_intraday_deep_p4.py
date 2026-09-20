from __future__ import annotations

import argparse
import json
import math
import time
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import csv
import numpy as np

DATASET = "xxparthparekhxx/indian-stock-market-minute-data"
CONFIG = "default"
SPLIT = "minute"
SYMBOLS = ("RELIANCE", "TCS", "HDFCBANK", "INFY", "SBIN")
ANCHORS = (0, 375, 750, 5000, 50000)
PAGE = 100
EXPECTED_BARS = 375
IST = timezone(timedelta(hours=5, minutes=30))

def fetch_rows(symbol: str, offset: int) -> dict:
    where = f'"symbol"=\'{symbol}\''
    q = urlencode({
        "dataset": DATASET,
        "config": CONFIG,
        "split": SPLIT,
        "where": where,
        "orderby": '"timestamp"',
        "offset": offset,
        "length": PAGE,
    })
    url = "https://datasets-server.huggingface.co/filter?" + q
    req = Request(url, headers={"User-Agent": "TimesFM-trading/phase4-intraday-gate"})
    last = None
    for attempt in range(4):
        try:
            with urlopen(req, timeout=45) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"filter API failed symbol={symbol} offset={offset}: {last}")

def load_eod(raw_dir: Path) -> dict[str, dict[str, float]]:
    result = {}
    for symbol in SYMBOLS:
        path = raw_dir / f"{symbol}.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            rows = {}
            for row in csv.DictReader(fh):
                day = row["date"][:10]
                rows[day] = float(row["close"])
        result[symbol] = rows
    return result

def valid_ohlc(r: dict) -> bool:
    o, h, l, c = [float(r[k]) for k in ("open","high","low","close")]
    return o > 0 and h > 0 and l > 0 and c > 0 and l <= min(o,c) <= max(o,c) <= h

def analyze_symbol(symbol: str, rows: list[dict], eod: dict[str,float]) -> dict:
    stamps = []
    invalid = 0
    zero_vol = 0
    outside = 0
    for r in rows:
        t = r["timestamp"]
        if not isinstance(t, datetime):
            t = datetime.fromisoformat(str(t).replace("Z","+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        t = t.astimezone(IST)
        stamps.append(t)
        invalid += int(not valid_ohlc(r))
        zero_vol += int(int(r.get("volume", 0) or 0) == 0)
        if not (t.hour > 9 or (t.hour == 9 and t.minute >= 15)):
            outside += 1
        elif t.hour > 15 or (t.hour == 15 and t.minute > 29):
            outside += 1
    stamps.sort()
    duplicates = len(stamps) - len(set(stamps))
    gaps = []
    for a, b in zip(stamps, stamps[1:]):
        delta = int((b - a).total_seconds() // 60)
        if delta != 1:
            gaps.append(delta)
    by_day = defaultdict(list)
    for r, t in zip(rows, sorted(stamps)):
        by_day[t.date().isoformat()].append(r)
    day_stats = {}
    for day, rs in by_day.items():
        ts = []
        for r in rs:
            t = r["timestamp"]
            if not isinstance(t, datetime):
                t = datetime.fromisoformat(str(t).replace("Z","+00:00"))
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
            ts.append(t.astimezone(IST))
        ts = sorted(ts)
        close = float(rs[-1]["close"])
        open_ = float(rs[0]["open"])
        high = max(float(r["high"]) for r in rs)
        low = min(float(r["low"]) for r in rs)
        count = len(rs)
        eod_close = eod.get(day)
        ret_diff = None
        if eod_close is not None and close > 0:
            ret_diff = None
        day_stats[day] = {
            "bars": count,
            "first_ist": ts[0].isoformat() if ts else None,
            "last_ist": ts[-1].isoformat() if ts else None,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "eod_close_available": eod_close is not None,
        }
    return {
        "rows": len(rows),
        "first_ist": stamps[0].isoformat() if stamps else None,
        "last_ist": stamps[-1].isoformat() if stamps else None,
        "duplicate_timestamps": duplicates,
        "invalid_ohlc_rows": invalid,
        "zero_volume_rows": zero_vol,
        "zero_volume_fraction": zero_vol / len(rows) if rows else math.nan,
        "outside_regular_session_rows": outside,
        "non_one_minute_gaps": gaps[:20],
        "daily_samples": day_stats,
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="p4_intraday_validation")
    args = ap.parse_args()

    eod = load_eod(Path(args.raw_dir))
    results = {}
    errors = []
    api_meta = {"dataset": DATASET, "config": CONFIG, "split": SPLIT, "page_size": PAGE}

    for symbol in SYMBOLS:
        rows = []
        offsets = []
        for anchor in ANCHORS:
            offsets.append(anchor)
            try:
                payload = fetch_rows(symbol, anchor)
            except Exception as exc:
                errors.append(str(exc))
                continue
            for item in payload.get("rows", []):
                row = item.get("row", {})
                if str(row.get("symbol","")).upper() == symbol:
                    rows.append(row)
        # Deduplicate on exact timestamp across overlapping slices.
        unique = {}
        for r in rows:
            unique[str(r["timestamp"])] = r
        rows = list(unique.values())
        results[symbol] = {
            "queried_offsets": offsets,
            "analysis": analyze_symbol(symbol, rows, eod[symbol]),
        }
        # A complete gate must see at least one day with an exactly complete session in the queried sample.
        complete_days = [
            d for d, x in results[symbol]["analysis"]["daily_samples"].items()
            if x["bars"] == EXPECTED_BARS and x["first_ist"].endswith("09:15:00+05:30")
        ]
        results[symbol]["complete_session_days_found"] = complete_days

    status = "pass"
    for symbol, data in results.items():
        a = data["analysis"]
        if a["duplicate_timestamps"] or a["invalid_ohlc_rows"] or a["outside_regular_session_rows"]:
            status = "fail"
        if not data["complete_session_days_found"]:
            status = "fail"
    if errors:
        status = "fail"

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": api_meta,
        "symbols": list(SYMBOLS),
        "anchors": list(ANCHORS),
        "expected_session_bars": EXPECTED_BARS,
        "errors": errors,
        "status": status,
        "results": results,
        "note": "Data-integrity gate only. Pass does not establish spread/fill accuracy or economic strategy validity.",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (out / "deep_validation.json").write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, default=str))
    if status != "pass":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
