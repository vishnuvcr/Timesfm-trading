from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DATASET = "xxparthparekhxx/indian-stock-market-minute-data"
CONFIG = "default"
SPLIT = "minute"
SYMBOLS = ("RELIANCE", "TCS", "HDFCBANK", "INFY", "SBIN")
DATES = ("2022-01-03", "2025-01-02")
OPEN_UTC = "03:45:00+00:00"
CLOSE_UTC = "10:00:00+00:00"
EXPECTED_BARS = 375


def fetch_rows(where: str, offset: int, length: int = 100) -> dict:
    params = urlencode({
        "dataset": DATASET,
        "config": CONFIG,
        "split": SPLIT,
        "where": where,
        "orderby": '"timestamp"',
        "offset": offset,
        "length": length,
    })
    req = Request(
        "https://datasets-server.huggingface.co/filter?" + params,
        headers={"User-Agent": "TimesFM-trading-P4B-intraday-validation/1.0"},
    )
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_day(symbol: str, date: str) -> list[dict]:
    where = (
        f'"symbol"=\'{symbol}\' AND '
        f'"timestamp">=\'{date}T{OPEN_UTC}\' AND '
        f'"timestamp"<\'{date}T{CLOSE_UTC}\''
    )
    rows = []
    for offset in (0, 100, 200, 300):
        payload = fetch_rows(where, offset, 100)
        rows.extend([item["row"] for item in payload.get("rows", [])])
        if len(payload.get("rows", [])) < 100:
            break
        time.sleep(0.10)
    return rows[:EXPECTED_BARS]


def parse_ts(value: str) -> datetime:
    stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def validate_day(rows: list[dict]) -> dict:
    errors = []
    timestamps = [parse_ts(r["timestamp"]) for r in rows]
    timestamps = sorted(timestamps)
    duplicate_count = len(timestamps) - len(set(timestamps))
    intervals = [
        int((timestamps[i + 1] - timestamps[i]).total_seconds())
        for i in range(len(timestamps) - 1)
    ]
    gap_count = sum(1 for x in intervals if x != 60)

    invalid_ohlc = 0
    zero_volume = 0
    for r in rows:
        o, h, l, c = [float(r[k]) for k in ("open", "high", "low", "close")]
        if not (min(o, c, l) <= h and l <= min(o, c)):
            invalid_ohlc += 1
        if int(r.get("volume", 0) or 0) == 0:
            zero_volume += 1

    if len(rows) != EXPECTED_BARS:
        errors.append(f"expected {EXPECTED_BARS} rows, observed {len(rows)}")
    if duplicate_count:
        errors.append(f"duplicate timestamps: {duplicate_count}")
    if gap_count:
        errors.append(f"non-60-second intervals: {gap_count}")
    if invalid_ohlc:
        errors.append(f"invalid OHLC rows: {invalid_ohlc}")
    if not timestamps or timestamps[0].strftime("%H:%M:%S") != OPEN_UTC[:8]:
        errors.append("first timestamp is not 09:15 IST")
    if not timestamps or timestamps[-1].strftime("%H:%M:%S") != "09:59:00":
        errors.append("last timestamp is not 15:29 IST")

    return {
        "rows": len(rows),
        "first_utc": timestamps[0].isoformat() if timestamps else None,
        "last_utc": timestamps[-1].isoformat() if timestamps else None,
        "duplicate_timestamps": duplicate_count,
        "non_60s_intervals": gap_count,
        "invalid_ohlc_rows": invalid_ohlc,
        "zero_volume_rows": zero_volume,
        "open": float(rows[0]["open"]) if rows else None,
        "high": max(float(r["high"]) for r in rows) if rows else None,
        "low": min(float(r["low"]) for r in rows) if rows else None,
        "close": float(rows[-1]["close"]) if rows else None,
        "volume_sum": int(sum(int(r.get("volume", 0) or 0) for r in rows)),
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }


def load_eod_row(path: Path, date: str) -> dict | None:
    import csv
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["date"][:10] == date:
                return row
    return None


def compare_to_eod(aggregate: dict, eod: dict | None) -> dict:
    if eod is None:
        return {"status": "missing_eod_row"}
    checks = {}
    for key in ("open", "high", "low", "close"):
        minute_value = float(aggregate[key])
        eod_value = float(eod[key])
        rel = abs(minute_value - eod_value) / max(abs(eod_value), 1e-9)
        checks[key] = {"minute": minute_value, "eod": eod_value, "relative_diff": rel}
    minute_vol = float(aggregate["volume_sum"])
    eod_vol = float(eod["volume"])
    checks["volume"] = {
        "minute": minute_vol,
        "eod": eod_vol,
        "relative_diff": abs(minute_vol - eod_vol) / max(abs(eod_vol), 1.0),
    }
    return checks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eod-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="p4b_intraday_validation_full")
    args = ap.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    results = []
    all_pass = True
    for symbol in SYMBOLS:
        for date in DATES:
            try:
                rows = fetch_day(symbol, date)
                agg = validate_day(rows)
                eod = load_eod_row(Path(args.eod_dir) / f"{symbol}.csv", date)
                comparison = compare_to_eod(agg, eod)
                price_fail = any(
                    isinstance(v, dict) and v.get("relative_diff", 0.0) > 0.005
                    for k, v in comparison.items()
                    if k != "volume"
                )
                volume_fail = bool(
                    isinstance(comparison.get("volume"), dict)
                    and comparison["volume"].get("relative_diff", 0.0) > 0.02
                )
                if price_fail:
                    agg["errors"].append("minute-vs-EOD price aggregation differs by >0.5%")
                if volume_fail:
                    agg["errors"].append("minute-vs-EOD volume aggregation differs by >2%")
                if agg["errors"]:
                    agg["status"] = "fail"
                result = {
                    "symbol": symbol,
                    "date": date,
                    "validation": agg,
                    "eod_comparison": comparison,
                }
                results.append(result)
                all_pass = all_pass and (agg["status"] == "pass")
            except Exception as exc:
                results.append({
                    "symbol": symbol,
                    "date": date,
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                })
                all_pass = False

    summary = {
        "dataset": DATASET,
        "split": SPLIT,
        "symbols": SYMBOLS,
        "dates": DATES,
        "session_ist": "09:15-15:30 regular session; bars expected 09:15 through 15:29",
        "expected_bars_per_session": EXPECTED_BARS,
        "price_tolerance_relative": 0.005,
        "volume_tolerance_relative": 0.02,
        "all_pass": all_pass,
        "results": results,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Full-session structural and EOD reconciliation gate only; not exchange-primary provenance or execution-fill validation.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
