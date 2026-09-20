from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

DATASET = "xxparthparekhxx/indian-stock-market-minute-data"
SYMBOLS = {
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "SBIN", "ITC", "BHARTIARTL", "LT", "AXISBANK",
}
EXPECTED_START = "09:15"
EXPECTED_END = "15:29"

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=150_000)
    ap.add_argument("--output", default="p4b_intraday_validation")
    return ap.parse_args()

def main() -> None:
    args = parse_args()
    from datasets import load_dataset

    ds = load_dataset(DATASET, split="minute", streaming=True)
    observed = 0
    matched = 0
    schema = None
    per_symbol = defaultdict(list)
    sample_rows = []

    for row in ds:
        observed += 1
        if schema is None:
            schema = sorted(row.keys())
        symbol = str(row.get("symbol", "")).upper()
        if symbol in SYMBOLS:
            matched += 1
            per_symbol[symbol].append(row)
            if len(sample_rows) < 20:
                sample_rows.append(row)
            if sum(len(v) for v in per_symbol.values()) >= 2_000:
                break
        if observed >= args.rows:
            break

    errors = []
    required = {"symbol", "timestamp", "open", "high", "low", "close", "volume"}
    if schema is None or not required.issubset(set(schema)):
        errors.append(f"schema missing required fields: expected={sorted(required)}, observed={schema}")

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
        symbol_stats[symbol] = {
            "rows": len(rows),
            "first_utc": ts_sorted[0].isoformat() if ts_sorted else None,
            "last_utc": ts_sorted[-1].isoformat() if ts_sorted else None,
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
        "observed_stream_rows_until_match_stop": observed,
        "matched_rows": matched,
        "schema": schema,
        "symbols_requested": sorted(SYMBOLS),
        "symbol_stats": symbol_stats,
        "sample_rows": sample_rows[:5],
        "declared_session_reference": {
            "nse_regular_open_ist": EXPECTED_START,
            "nse_regular_last_minute_ist": EXPECTED_END,
            "source_timestamp_storage": "UTC",
        },
        "validation_errors": errors,
        "status": "pass" if not errors and matched > 0 else "fail",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Source-integrity gate only; not evidence that the source is exchange-primary or fill-accurate.",
    }
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "intraday_source_validation.json").write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))
    if errors or matched == 0:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
