from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import zipfile
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

SYMBOLS = ("RELIANCE", "TCS", "HDFCBANK", "INFY", "SBIN")
IST = timezone(timedelta(hours=5, minutes=30))
EXPECTED_BARS = 375
MAX_RETURN_DIFF = 0.0010  # 10 bps absolute difference in overlapping daily log returns

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--raw-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="p4_intraday_release_validation")
    return ap.parse_args()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def load_eod(path: Path) -> dict[str, float]:
    out = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["date"][:10]] = float(row["close"])
    return out

def parse_time(v: str) -> datetime:
    t = datetime.fromtimestamp(int(v), tz=timezone.utc)
    return t.astimezone(IST)

def valid_ohlc(row: dict) -> bool:
    o, h, l, c = [float(row[k]) for k in ("open", "high", "low", "close")]
    return (
        o > 0 and h > 0 and l > 0 and c > 0
        and l <= min(o, c) <= max(o, c) <= h
    )

def read_symbol(zf: zipfile.ZipFile, symbol: str) -> list[dict]:
    target = f"{symbol}_1m.csv.gz"
    names = zf.namelist()
    if target not in names:
        # tolerate a directory prefix
        matches = [n for n in names if n.endswith("/" + target) or n.endswith(target)]
        if not matches:
            raise RuntimeError(f"{symbol}: {target} not found in release")
        target = matches[0]
    extracted = []
    with zf.open(target, "r") as raw:
        with gzip.GzipFile(fileobj=raw) as gz:
            text = gz.read().decode("utf-8")
    import io
    for row in csv.DictReader(io.StringIO(text)):
        extracted.append(row)
    return extracted

def analyze(symbol: str, rows: list[dict], eod: dict[str, float]) -> dict:
    parsed = []
    invalid = 0
    zero_vol = 0
    for r in rows:
        t = parse_time(r["time"])
        parsed.append((t, r))
        invalid += int(not valid_ohlc(r))
        zero_vol += int(float(r.get("Volume", 0) or 0) == 0)

    parsed.sort(key=lambda x: x[0])
    duplicates = len(parsed) - len({t for t, _ in parsed})
    by_day = defaultdict(list)
    for t, r in parsed:
        by_day[t.date().isoformat()].append((t, r))

    complete_days = []
    gap_days = []
    outside_rows = 0
    daily = {}
    for day, vals in sorted(by_day.items()):
        ts = [t for t, _ in vals]
        for t in ts:
            if not ((t.hour > 9 or (t.hour == 9 and t.minute >= 15)) and
                    (t.hour < 15 or (t.hour == 15 and t.minute <= 30))):
                outside_rows += 1
        # Expect regular session through 15:29; a 15:30 bar is not required.
        expected = [ts[0]] if ts else []
        minute_set = {(t.hour, t.minute) for t in ts}
        complete = len(vals) == EXPECTED_BARS and (9,15) in minute_set and (15,29) in minute_set
        if complete:
            complete_days.append(day)
        else:
            gap_days.append(day)
        close = float(vals[-1][1]["close"])
        open_ = float(vals[0][1]["open"])
        daily[day] = {
            "bars": len(vals),
            "first_ist": ts[0].isoformat() if ts else None,
            "last_ist": ts[-1].isoformat() if ts else None,
            "open": open_,
            "high": max(float(r["high"]) for _, r in vals),
            "low": min(float(r["low"]) for _, r in vals),
            "close": close,
            "eod_close": eod.get(day),
        }

    common = sorted(d for d, x in daily.items() if x["eod_close"] is not None)
    diffs = []
    paired_dates = []
    for prev, cur in zip(common, common[1:]):
        if cur not in daily or prev not in daily:
            continue
        a0, a1 = float(eod[prev]), float(eod[cur])
        b0, b1 = float(daily[prev]["close"]), float(daily[cur]["close"])
        if min(a0, a1, b0, b1) <= 0:
            continue
        eod_ret = math.log(a1 / a0)
        minute_ret = math.log(b1 / b0)
        diffs.append(abs(eod_ret - minute_ret))
        paired_dates.append(cur)

    return {
        "rows": len(rows),
        "first_ist": parsed[0][0].isoformat() if parsed else None,
        "last_ist": parsed[-1][0].isoformat() if parsed else None,
        "duplicate_timestamps": duplicates,
        "invalid_ohlc_rows": invalid,
        "zero_volume_rows": zero_vol,
        "zero_volume_fraction": zero_vol / len(rows) if rows else math.nan,
        "outside_session_rows": outside_rows,
        "days": len(by_day),
        "complete_session_days": len(complete_days),
        "complete_session_examples": complete_days[:10],
        "incomplete_session_fraction": len(gap_days) / len(by_day) if by_day else math.nan,
        "daily_close_return_pairs": len(diffs),
        "max_abs_daily_log_return_diff": max(diffs) if diffs else math.nan,
        "p95_abs_daily_log_return_diff": sorted(diffs)[max(0, int(0.95 * len(diffs)) - 1)] if diffs else math.nan,
        "daily_close_return_pass": bool(diffs) and max(diffs) <= MAX_RETURN_DIFF,
        "daily_samples": {k: daily[k] for k in list(sorted(daily))[:3] + list(sorted(daily))[-3:]},
    }

def main():
    args = parse_args()
    zip_path = Path(args.zip)
    digest = sha256_file(zip_path)
    expected_digest = "20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2"
    if digest != expected_digest:
        raise SystemExit(f"release SHA-256 mismatch: {digest} != {expected_digest}")

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    eod_cache = {s: load_eod(Path(args.raw_dir) / f"{s}.csv") for s in SYMBOLS}

    with zipfile.ZipFile(zip_path) as zf:
        for symbol in SYMBOLS:
            rows = read_symbol(zf, symbol)
            results[symbol] = analyze(symbol, rows, eod_cache[symbol])

    failures = {}
    for symbol, r in results.items():
        fail = []
        if r["duplicate_timestamps"] != 0:
            fail.append("duplicate_timestamps")
        if r["invalid_ohlc_rows"] != 0:
            fail.append("invalid_ohlc_rows")
        if r["outside_session_rows"] != 0:
            fail.append("outside_session_rows")
        if r["complete_session_days"] == 0:
            fail.append("no_complete_session_days")
        if not r["daily_close_return_pass"]:
            fail.append("daily_close_return_mismatch")
        failures[symbol] = fail

    payload = {
        "source": {
            "repo": "voletiramu/nse-fno-1min-data",
            "release": "v1.0.0",
            "asset": zip_path.name,
            "sha256": digest,
            "date_range": "2024-04-01 to 2026-04-30",
            "symbols_in_release": 214,
            "source_claim": "Zerodha Kite API",
        },
        "symbols": list(SYMBOLS),
        "expected_regular_session_bars": EXPECTED_BARS,
        "daily_return_tolerance_abs_log": MAX_RETURN_DIFF,
        "results": results,
        "failures": failures,
        "status": "pass" if not any(failures.values()) else "fail",
        "note": "Source-integrity gate only; pass does not establish spread/quote/fill accuracy.",
    }
    (out / "release_validation.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print(json.dumps(payload, indent=2, default=str))
    if payload["status"] != "pass":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
