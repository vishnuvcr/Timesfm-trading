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
MIN_COMPLETE_FRACTION = 0.99
MAX_INVALID_ROWS = 2
MAX_ZERO_VOLUME_FRACTION = 0.001
MAX_MEDIAN_RETURN_DIFF = 0.0010
MAX_P95_RETURN_DIFF = 0.0100

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_time(v: str) -> datetime:
    return datetime.fromtimestamp(int(v), tz=timezone.utc).astimezone(IST)

def load_eod(path: Path) -> dict[str, float]:
    out = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["date"][:10]] = float(row["close"])
    return out

def load_actions(path: Path) -> set[str]:
    out = set()
    if not path.exists():
        return out
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("exchange") == "NSE" and row.get("ex_date"):
                out.add(row["ex_date"][:10])
    return out

def valid_ohlc(r: dict) -> bool:
    o, h, l, c = [float(r[k]) for k in ("open", "high", "low", "close")]
    return o > 0 and h > 0 and l > 0 and c > 0 and l <= min(o, c) <= max(o, c) <= h

def read_symbol(zf: zipfile.ZipFile, symbol: str) -> list[dict]:
    name = f"{symbol}_1m.csv.gz"
    matches = [n for n in zf.namelist() if n == name or n.endswith("/" + name) or n.endswith(name)]
    if not matches:
        raise RuntimeError(f"{symbol}: file not found")
    import io
    with zf.open(matches[0], "r") as raw:
        with gzip.GzipFile(fileobj=raw) as gz:
            text = gz.read().decode("utf-8")
    return list(csv.DictReader(io.StringIO(text)))

def analyze(symbol: str, rows: list[dict], eod: dict[str, float], actions: set[str]) -> dict:
    parsed = []
    invalid_examples = []
    invalid = 0
    zero_volume = 0
    outside_rows = 0
    outside_bad = 0
    outside_examples = []

    for r in rows:
        t = parse_time(r["time"])
        parsed.append((t, r))
        if not valid_ohlc(r):
            invalid += 1
            if len(invalid_examples) < 10:
                invalid_examples.append({
                    "time": r.get("time"),
                    "open": r.get("open"),
                    "high": r.get("high"),
                    "low": r.get("low"),
                    "close": r.get("close"),
                })
        zero_volume += int(float(r.get("Volume", 0) or 0) == 0)
        in_regular = (t.hour > 9 or (t.hour == 9 and t.minute >= 15)) and (t.hour < 15 or (t.hour == 15 and t.minute <= 30))
        if not in_regular:
            outside_rows += 1
            outside_bad += 1
            if len(outside_examples) < 10:
                outside_examples.append(t.isoformat())

    # Some releases carry a small number of post-session records. They are quarantined, not used.
    regular = [(t, r) for t, r in parsed if 9*60+15 <= t.hour*60+t.minute <= 15*60+29]
    regular.sort(key=lambda x: x[0])

    by_day = defaultdict(list)
    for t, r in regular:
        by_day[t.date().isoformat()].append((t, r))

    daily = {}
    complete_days = 0
    for day, vals in sorted(by_day.items()):
        ts = [t for t, _ in vals]
        minute_set = {(t.hour, t.minute) for t in ts}
        complete = len(vals) == EXPECTED_BARS and (9, 15) in minute_set and (15, 29) in minute_set
        complete_days += int(complete)
        daily[day] = {
            "bars": len(vals),
            "first_ist": ts[0].isoformat(),
            "last_ist": ts[-1].isoformat(),
            "open": float(vals[0][1]["open"]),
            "high": max(float(r["high"]) for _, r in vals),
            "low": min(float(r["low"]) for _, r in vals),
            "close": float(vals[-1][1]["close"]),
            "eod_close": eod.get(day),
        }

    common = sorted(d for d, v in daily.items() if v["eod_close"] is not None)
    raw_diffs = []
    clean_diffs = []
    for prev, cur in zip(common, common[1:]):
        a0, a1 = eod[prev], eod[cur]
        b0, b1 = daily[prev]["close"], daily[cur]["close"]
        if min(a0, a1, b0, b1) <= 0:
            continue
        d = abs(math.log(a1 / a0) - math.log(b1 / b0))
        raw_diffs.append(d)
        if prev not in actions and cur not in actions:
            clean_diffs.append(d)

    def median(v):
        if not v:
            return math.nan
        w = sorted(v)
        return float(w[len(w)//2])

    def p95(v):
        if not v:
            return math.nan
        w = sorted(v)
        return float(w[max(0, int(0.95*len(w))-1)])

    med = median(clean_diffs)
    q95 = p95(clean_diffs)
    pass_close = bool(clean_diffs) and med <= MAX_MEDIAN_RETURN_DIFF and q95 <= MAX_P95_RETURN_DIFF

    return {
        "rows": len(rows),
        "regular_session_rows": len(regular),
        "first_ist": regular[0][0].isoformat() if regular else None,
        "last_ist": regular[-1][0].isoformat() if regular else None,
        "duplicate_timestamps": len(regular) - len({t for t, _ in regular}),
        "invalid_ohlc_rows": invalid,
        "invalid_examples": invalid_examples,
        "zero_volume_rows": zero_volume,
        "zero_volume_fraction": zero_volume / len(rows) if rows else math.nan,
        "outside_session_rows_quarantined": outside_rows,
        "outside_session_examples": outside_examples,
        "days": len(by_day),
        "complete_session_days": complete_days,
        "complete_session_fraction": complete_days / len(by_day) if by_day else math.nan,
        "daily_close_return_pairs": len(raw_diffs),
        "raw_max_abs_daily_log_return_diff": max(raw_diffs) if raw_diffs else math.nan,
        "raw_p95_abs_daily_log_return_diff": p95(raw_diffs),
        "corp_action_excluded_pairs": len(clean_diffs),
        "corp_action_excluded_median_abs_daily_log_return_diff": med,
        "corp_action_excluded_p95_abs_daily_log_return_diff": q95,
        "daily_close_return_pass": pass_close,
        "daily_samples": {k: daily[k] for k in list(sorted(daily))[:2] + list(sorted(daily))[-2:]},
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--raw-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="p4_intraday_release_validation")
    args = ap.parse_args()

    zip_path = Path(args.zip)
    digest = sha256_file(zip_path)
    expected = "20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2"
    if digest != expected:
        raise SystemExit(f"release SHA-256 mismatch: {digest} != {expected}")

    results = {}
    with zipfile.ZipFile(zip_path) as zf:
        for symbol in SYMBOLS:
            rows = read_symbol(zf, symbol)
            results[symbol] = analyze(
                symbol,
                rows,
                load_eod(Path(args.raw_dir) / f"{symbol}.csv"),
                load_actions(Path(args.raw_dir) / f"{symbol}_actions.csv"),
            )

    failures = {}
    for symbol, r in results.items():
        fail = []
        if r["duplicate_timestamps"] != 0:
            fail.append("duplicate_timestamps")
        if r["invalid_ohlc_rows"] > MAX_INVALID_ROWS:
            fail.append("too_many_invalid_ohlc_rows")
        if r["complete_session_fraction"] < MIN_COMPLETE_FRACTION:
            fail.append("session_completeness")
        if r["zero_volume_fraction"] > MAX_ZERO_VOLUME_FRACTION:
            fail.append("excess_zero_volume")
        if not r["daily_close_return_pass"]:
            fail.append("cross_source_return_reconciliation")
        failures[symbol] = fail

    payload = {
        "source": {
            "repository": "voletiramu/nse-fno-1min-data",
            "release": "v1.0.0",
            "asset": zip_path.name,
            "sha256": digest,
            "source_claim": "Zerodha Kite API",
            "date_range": "2024-04-01 to 2026-04-30",
            "release_symbols": 214,
        },
        "acceptance_thresholds": {
            "min_complete_session_fraction": MIN_COMPLETE_FRACTION,
            "max_invalid_rows_per_symbol": MAX_INVALID_ROWS,
            "max_zero_volume_fraction": MAX_ZERO_VOLUME_FRACTION,
            "max_median_abs_daily_log_return_diff": MAX_MEDIAN_RETURN_DIFF,
            "max_p95_abs_daily_log_return_diff": MAX_P95_RETURN_DIFF,
        },
        "results": results,
        "failures": failures,
        "status": "pass" if not any(failures.values()) else "fail",
        "note": "Source-integrity gate only; regular-session analysis quarantines post-session records and cross-source return checks exclude recorded corporate-action dates.",
    }

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "release_validation.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print(json.dumps(payload, indent=2, default=str))
    if payload["status"] != "pass":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
