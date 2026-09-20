#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import pandas as pd

HF_BASE = "https://huggingface.co/datasets/tejhq/indian-markets/resolve/main"
PRICE_COLUMNS = [  # adjusted-price acquisition protocol v1
    "date", "symbol", "isin", "name", "open", "high", "low", "close",
    "volume", "turnover", "adj_factor_cumulative", "adj_close"
]


def download(url: str, out: Path) -> None:
    subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error", url, "-o", str(out)],
        check=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="RELIANCE,TCS,HDFCBANK,INFY,ICICIBANK,SBIN,ITC,BHARTIARTL,LT,AXISBANK,KOTAKBANK,HINDUNILVR,MARUTI,SUNPHARMA,BAJFINANCE,ASIANPAINT,TITAN,HCLTECH,WIPRO,ULTRACEMCO,NESTLEIND,M&M,NTPC,ONGC,POWERGRID,TATAMOTORS,TATASTEEL,ADANIENT,CIPLA,DRREDDY")
    ap.add_argument("--start-year", type=int, default=2010)
    ap.add_argument("--end-year", type=int, default=2026)
    ap.add_argument("--start-date", default="2010-01-04")
    ap.add_argument("--end-date", default="2026-09-18")
    ap.add_argument("--out", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--universe-out", default="data/cache/equities/tejhq_nse_pit_universe.csv")
    args = ap.parse_args()

    symbols = [x.strip().upper() for x in args.symbols.split(",") if x.strip()]
    start = pd.Timestamp(args.start_date)
    end = pd.Timestamp(args.end_date)
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    by_symbol = {s: [] for s in symbols}

    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        for year in range(args.start_year, args.end_year + 1):
            src = f"{HF_BASE}/prices_adjusted/nse_{year}.parquet?download=true"
            p = temp / f"nse_{year}.parquet"
            download(src, p)
            df = pd.read_parquet(p, columns=PRICE_COLUMNS)
            df["date"] = pd.to_datetime(df["date"])
            df = df[(df["date"] >= start) & (df["date"] <= end)]
            if df.empty:
                continue
            df = df[df["symbol"].isin(symbols)]
            for symbol, part in df.groupby("symbol", sort=False):
                by_symbol[symbol].append(part.copy())

        for symbol, frames in by_symbol.items():
            if not frames:
                raise RuntimeError(f"no adjusted data found for {symbol}")
            df = pd.concat(frames, ignore_index=True)
            df = df.sort_values("date").drop_duplicates("date")
            cols = [c for c in PRICE_COLUMNS if c in df.columns]
            df[cols].to_csv(out_root / f"{symbol}.csv", index=False)

        universe_url = f"{HF_BASE}/universe/nse_liquid.parquet?download=true"
        up = temp / "nse_liquid.parquet"
        download(universe_url, up)
        u = pd.read_parquet(up)
        u["rebalance_date"] = pd.to_datetime(u["rebalance_date"])
        u["valid_to"] = pd.to_datetime(u["valid_to"])
        u = u[
            u["symbol"].isin(symbols)
            & (u["valid_to"] >= start)
            & (u["rebalance_date"] <= end)
        ].copy()
        u = u.sort_values(["rebalance_date", "rank", "symbol"])
        u.to_csv(args.universe_out, index=False)

    manifest = {
        "dataset_id": "tejhq_nse_adjusted_stock_bootstrap",
        "source_id": "community_tejhq_indian_markets_prices_adjusted",
        "source_url": "https://huggingface.co/datasets/tejhq/indian-markets",
        "symbols": symbols,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "price_tree": "prices_adjusted/nse_YYYY.parquet",
        "universe_tree": "universe/nse_liquid.parquet",
        "pit_universe": True,
        "raw_files_not_duplicated": True,
    }
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
