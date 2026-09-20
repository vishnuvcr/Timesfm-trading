from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path("data/cache/equities/tejhq_nse_adjusted")
UNIVERSE = Path("data/cache/equities/tejhq_nse_pit_universe.csv")


def validate_price(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows, f"{path}: empty"
    required = {"date","symbol","open","high","low","close","volume","turnover","adj_factor_cumulative","adj_close"}
    assert required <= set(rows[0]), f"{path}: missing {required - set(rows[0])}"
    dates = [r["date"][:10] for r in rows]
    assert dates == sorted(dates), f"{path}: unsorted dates"
    assert len(dates) == len(set(dates)), f"{path}: duplicate dates"
    assert len({r["symbol"] for r in rows}) == 1, f"{path}: multiple symbols"
    for r in rows:
        h = float(r["high"]); l = float(r["low"])
        o = float(r["open"]); c = float(r["close"])
        adj = float(r["adj_close"]); factor = float(r["adj_factor_cumulative"])
        v = float(r["volume"])
        assert h >= l > 0 and l <= o <= h and l <= c <= h, f"{path}: invalid raw OHLC"
        assert v >= 0, f"{path}: negative volume"
        assert adj > 0 and factor > 0, f"{path}: invalid adjusted values"
    return len(rows)


def validate_universe(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows, f"{path}: empty"
    required = {"exchange","rebalance_date","valid_to","rank","symbol","avg_turnover_63d"}
    assert required <= set(rows[0]), f"{path}: missing {required - set(rows[0])}"
    keys = [(r["symbol"], r["rebalance_date"]) for r in rows]
    assert len(keys) == len(set(keys)), f"{path}: duplicate symbol/rebalance rows"
    for r in rows:
        rank = int(r["rank"])
        assert 1 <= rank <= 500, f"{path}: rank outside liquid500"
        assert r["rebalance_date"] <= r["valid_to"], f"{path}: invalid interval"
        assert float(r["avg_turnover_63d"]) >= 0, f"{path}: negative turnover"
    return len(rows)


def main() -> None:
    files = sorted(ROOT.glob("*.csv"))
    files = [p for p in files if p.name != "manifest.csv"]
    assert files, "no adjusted stock files"
    total = sum(validate_price(p) for p in files)
    universe_rows = validate_universe(UNIVERSE)
    print(f"validated {len(files)} adjusted stock files / {total} rows and {universe_rows} PIT universe rows")


if __name__ == "__main__":
    main()
