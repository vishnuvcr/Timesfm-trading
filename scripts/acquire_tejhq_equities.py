#!/usr/bin/env python3
"""Acquire cached NSE individual-stock EOD data from TejHQ's public API.

Alternate access path only. Existing files are reused unless --refresh is supplied.
"""

from __future__ import annotations
import argparse, csv, hashlib, json, time
from pathlib import Path
from urllib.parse import quote
import requests

BASE = "https://api.tejhq.dev/v1"
DEFAULT_START = "2010-01-04"
DEFAULT_END = "2026-09-18"
UA = "TimesFM-trading-research/1.0 (+https://github.com/vishnuvcr/Timesfm-trading)"


def extract_rows(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        raise ValueError(f"unexpected JSON payload type: {type(payload).__name__}")
    for key in ("data", "rows", "results", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    raise ValueError(f"could not find row list in payload keys={sorted(payload)}")


def normalise_ohlcv(rows: list[dict], symbol: str) -> list[dict]:
    aliases = {
        "date": ("date", "trade_date"),
        "open": ("open", "Open"),
        "high": ("high", "High"),
        "low": ("low", "Low"),
        "close": ("close", "Close"),
        "volume": ("volume", "Volume"),
        "turnover": ("turnover", "Turnover"),
        "isin": ("isin", "ISIN"),
        "series": ("series", "Series"),
    }
    out = []
    for row in rows:
        d = {}
        for dst, keys in aliases.items():
            for key in keys:
                if key in row:
                    d[dst] = row[key]
                    break
        if "date" in d:
            d["symbol"] = symbol
            out.append(d)
    return sorted(out, key=lambda x: str(x["date"]))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalise_actions(rows: list[dict], symbol: str) -> list[dict]:
    fields = ("exchange", "symbol", "isin", "company", "ex_date", "record_date", "type", "ratio_num", "ratio_den", "cash_amount", "face_value_from", "face_value_to", "raw_subject")
    out = []
    for row in rows:
        d = {k: row.get(k, "") for k in fields}
        if not d["symbol"]:
            d["symbol"] = symbol
        if d["ex_date"]:
            out.append(d)
    return sorted(out, key=lambda x: str(x["ex_date"]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols-file", type=Path, default=Path("configs/equity_research_universe.json"))
    ap.add_argument("--symbols", default="", help="Comma-separated symbols overriding the configured universe")
    ap.add_argument("--out", type=Path, default=Path("data/cache/equities/tejhq_nse"))
    ap.add_argument("--start", default=DEFAULT_START)
    ap.add_argument("--end", default=DEFAULT_END)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--actions", action="store_true", help="Also cache corporate actions for each selected symbol")
    ap.add_argument("--sleep", type=float, default=0.25)
    args = ap.parse_args()

    cfg = json.loads(args.symbols_file.read_text(encoding="utf-8"))
    symbols = [x.strip().upper() for x in args.symbols.split(",") if x.strip()] if args.symbols else list(cfg["symbols"])
    manifest = {
        "dataset_id": "tejhq_nse_equity_eod_stock_bootstrap",
        "source_id": "community_tejhq_nse_bhavcopy",
        "source_url": "https://api.tejhq.dev/v1/ohlcv/nse/{symbol}",
        "source_lineage": "TejHQ states that the dataset is built from NSE official EOD bhavcopy and corporate-action feeds.",
        "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "start": args.start,
        "end": args.end,
        "symbols": {},
        "pit_status": "bootstrap_fixed_universe_not_final_evidence",
    }

    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "application/json"})

    for symbol in symbols:
        out_path = args.out / f"{symbol}.csv"
        price_cached = out_path.exists() and not args.refresh

        if price_cached:
            digest = hashlib.sha256(out_path.read_bytes()).hexdigest()
            rows_count = max(0, len(out_path.read_text(encoding="utf-8").splitlines()) - 1)
            first_date = last_date = ""
        else:
            url = f"{BASE}/ohlcv/nse/{quote(symbol)}?from={args.start}&to={args.end}"
            r = session.get(url, timeout=60)
            r.raise_for_status()
            rows = normalise_ohlcv(extract_rows(r.json()), symbol)
            if len(rows) < 200:
                raise RuntimeError(f"{symbol}: only {len(rows)} rows from {url}")
            digest = write_csv(
                out_path,
                rows,
                ["date","symbol","series","isin","open","high","low","close","volume","turnover"],
            )
            rows_count = len(rows)
            first_date = str(rows[0]["date"])
            last_date = str(rows[-1]["date"])
            time.sleep(args.sleep)

        action_url = ""
        action_digest = ""
        action_rows = 0
        if args.actions:
            action_path = args.out / f"{symbol}_actions.csv"
            action_cached = action_path.exists() and not args.refresh
            if action_cached:
                action_digest = hashlib.sha256(action_path.read_bytes()).hexdigest()
                action_rows = max(0, len(action_path.read_text(encoding="utf-8").splitlines()) - 1)
            else:
                action_url = f"{BASE}/actions/{quote(symbol)}"
                ar = session.get(action_url, timeout=60)
                ar.raise_for_status()
                action_rows_data = normalise_actions(extract_rows(ar.json()), symbol)
                action_digest = write_csv(
                    action_path,
                    action_rows_data,
                    ["exchange","symbol","isin","company","ex_date","record_date","type",
                     "ratio_num","ratio_den","cash_amount","face_value_from","face_value_to","raw_subject"],
                )
                action_rows = len(action_rows_data)
                time.sleep(args.sleep)

        manifest["symbols"][symbol] = {
            "path": str(out_path),
            "sha256": digest,
            "rows": rows_count,
            "first_date": first_date,
            "last_date": last_date,
            "cached": price_cached,
            "url": f"{BASE}/ohlcv/nse/{quote(symbol)}?from={args.start}&to={args.end}",
            "actions_path": str(args.out / f"{symbol}_actions.csv") if args.actions else "",
            "actions_url": action_url,
            "actions_rows": action_rows,
            "actions_sha256": action_digest,
        }

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
