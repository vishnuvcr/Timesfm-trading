#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import pandas as pd


HF_BASE = "https://huggingface.co/datasets/vishnun0027/indian-market-historical-ohlcv/resolve/main/stocks"


def download(symbol: str, path: Path) -> None:
    url = f"{HF_BASE}/{symbol}.parquet?download=true"
    subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error", url, "-o", str(path)], check=True)


def crosscheck(local_path: Path, hf_path: Path) -> dict:
    local = pd.read_csv(local_path, parse_dates=["date"])
    hf = pd.read_parquet(hf_path, columns=["date", "open", "high", "low", "close", "volume", "adj_close", "dividends", "stock_splits"])
    local["date"] = pd.to_datetime(local["date"])
    hf["date"] = pd.to_datetime(hf["date"])

    merged = local[["date", "open", "high", "low", "close", "volume"]].merge(
        hf[["date", "open", "high", "low", "close", "volume"]],
        on="date",
        suffixes=("_tejhq", "_yahoo"),
        how="inner",
    )
    if len(merged) < 100:
        raise RuntimeError(f"too little overlap: {len(merged)} rows for {local_path.name}")

    pct_diff = (merged["close_tejhq"] - merged["close_yahoo"]).abs() / merged["close_yahoo"].abs().replace(0, pd.NA)
    within_10bp = float((pct_diff <= 0.001).mean())
    return {
        "symbol": local_path.stem,
        "tejhq_rows": int(len(local)),
        "yahoo_rows": int(len(hf)),
        "overlap_rows": int(len(merged)),
        "overlap_start": str(merged["date"].min().date()),
        "overlap_end": str(merged["date"].max().date()),
        "median_abs_close_pct_diff": float(pct_diff.median()),
        "p95_abs_close_pct_diff": float(pct_diff.quantile(0.95)),
        "max_abs_close_pct_diff": float(pct_diff.max()),
        "share_close_within_0_10pct": within_10bp,
        "source_note": "Yahoo/yfinance dataset is an independent cross-check; no raw cross-check file is committed.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="RELIANCE,TCS,HDFCBANK,INFY,SBIN")
    ap.add_argument("--local-root", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--output", default="data/derived/stock_source_crosscheck.json")
    args = ap.parse_args()

    symbols = [x.strip().upper() for x in args.symbols.split(",") if x.strip()]
    out = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for symbol in symbols:
            hf = root / f"{symbol}.parquet"
            download(symbol, hf)
            out.append(crosscheck(Path(args.local_root) / f"{symbol}.csv", hf))

    payload = {
        "version": "2026-09-20.stock-source-crosscheck-1",
        "symbols": symbols,
        "source": "vishnun0027/indian-market-historical-ohlcv",
        "results": out,
        "raw_crosscheck_files_committed": False,
    }
    p = Path(args.output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
