from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DATASET = "xxparthparekhxx/indian-stock-market-minute-data"
CONFIG = "default"
SPLIT = "minute"
PROBE_SYMBOL = "20MICRONS"
PAGE_SIZE = 100
PAGES = 20

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=PAGES)
    ap.add_argument("--output", default="p4b_intraday_validation")
    return ap.parse_args()

def fetch_rows(offset: int, length: int) -> dict:
    query = urlencode({
        "dataset": DATASET,
        "config": CONFIG,
        "split": SPLIT,
        "offset": offset,
        "length": length,
    })
    url = "https://datasets-server.huggingface.co/rows?" + query
    req = Request(url, headers={"User-Agent": "TimesFM-trading-research/4B"})
    with urlopen(req, timeout=30) as response:
        import json as _json
        return _json.loads(response.read().decode("utf-8"))

def main() -> None:
    args = parse_args()
    observed = 0
    matched = 0
    schema = None
    per_symbol = defaultdict(list)
    sample_rows = []
    errors = []

    for page in range(max(1, args.pages)):
        offset = page * PAGE_SIZE
        try:
            payload = fetch_rows(offset, PAGE_SIZE)
        except Exception as exc:
            errors.append(f"rows API failed at offset {offset}: {type(exc).__name__}: {exc}")
            break

        if schema is None:
            schema = sorted(
                f.get("name", "") for f in payload.get("features", [])
            )

        rows = payload.get("rows", [])
        if not rows:
            break

        for item in rows:
            row = item.get("row", {})
            observed += 1
            symbol = str(row.get("symbol", "")).upper()
            if symbol != PROBE_SYMBOL:
                continue
            matched += 1
            per_symbol[symbol].append(row)
            if len(sample_rows) < 20:
                sample_rows.append(row)

        if len(per_symbol[PROBE_SYMBOL]) >= PAGE_SIZE * args.pages:
            break
        time.sleep(0.1)

    required = {"symbol", "timestamp", "open", "high", "low", "close", "volume"}
    if schema is None or not required.issubset(set(schema)):
        errors.append(
            f"schema missing required fields: expected={sorted(required)}, observed={schema}"
        )

    symbol_stats = {}
    for symbol, rows in sorted(per_symbol.items()):
        ts = []
        invalid_ohlc = 0
        zero_volume = 0
        for r in rows:
            stamp = r["timestamp"]
            if not isinstance(stamp, datetime):
                stamp = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                errors.append(f"{symbol}: timestamp without timezone")
                stamp = stamp.replace(tzinfo=timezone.utc)
            ts.append(stamp.astimezone(timezone.utc))
            o, h, l, c = [float(r[k]) for k in ("open", "high", "low", "close")]
            if not (min(o, c, l) <= h and l <= min(o, c)):
                invalid_ohlc += 1
            if int(r.get("volume", 0) or 0) == 0:
                zero_volume += 1

        ts_sorted = sorted(ts)
        duplicate_ts = len(ts_sorted) - len(set(ts_sorted))
        ist_times = [
            stamp.astimezone(__import__("datetime").timezone(__import__("datetime").timedelta(hours=5, minutes=30)))
            for stamp in ts_sorted
        ]
        symbol_stats[symbol] = {
            "rows": len(rows),
            "first_utc": ts_sorted[0].isoformat() if ts_sorted else None,
            "last_utc": ts_sorted[-1].isoformat() if ts_sorted else None,
            "first_ist": ist_times[0].isoformat() if ist_times else None,
            "last_ist": ist_times[-1].isoformat() if ist_times else None,
            "duplicate_timestamps": duplicate_ts,
            "invalid_ohlc_rows": invalid_ohlc,
            "zero_volume_rows": zero_volume,
        }
        if duplicate_ts:
            errors.append(f"{symbol}: duplicate timestamps in sampled rows")
        if invalid_ohlc:
            errors.append(f"{symbol}: invalid OHLC rows in sampled rows")

    result = {
        "dataset": DATASET,
        "config": CONFIG,
        "split": SPLIT,
        "pages_requested": int(args.pages),
        "page_size": PAGE_SIZE,
        "observed_rows": observed,
        "matched_rows": matched,
        "schema": schema,
        "probe_symbol": PROBE_SYMBOL,
        "symbol_stats": symbol_stats,
        "sample_rows": sample_rows[:5],
        "declared_session_reference": {
            "nse_regular_open_ist": "09:15",
            "nse_regular_last_minute_ist": "15:29",
            "source_timestamp_storage": "UTC",
        },
        "validation_errors": errors,
        "status": "pass" if not errors and matched > 0 else "fail",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Source-integrity gate only; not evidence that the source is exchange-primary or fill-accurate.",
    }
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "intraday_source_validation.json").write_text(
        json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, default=str))
    if errors or matched == 0:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
