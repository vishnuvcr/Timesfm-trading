from __future__ import annotations

import csv
import sys
from pathlib import Path

PRICE_REQUIRED = {"date","symbol","open","high","low","close","volume"}
ACTION_REQUIRED = {"symbol","ex_date","type"}


def as_float(v: str, field: str, path: Path) -> float:
    try:
        return float(v)
    except Exception as exc:
        raise AssertionError(f"{path}: non-numeric {field}={v!r}") from exc


def validate_price_file(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows, f"{path}: empty"
    assert PRICE_REQUIRED <= set(rows[0]), f"{path}: missing columns {PRICE_REQUIRED - set(rows[0])}"
    dates = [r["date"][:10] for r in rows]
    assert dates == sorted(dates), f"{path}: dates not sorted"
    assert len(dates) == len(set(dates)), f"{path}: duplicate dates"
    symbols = {r["symbol"] for r in rows}
    assert len(symbols) == 1, f"{path}: multiple symbols {symbols}"
    for r in rows:
        o, h, l, c = [as_float(r[k], k, path) for k in ("open", "high", "low", "close")]
        v = as_float(r["volume"], "volume", path)
        assert h >= l > 0, f"{path}: invalid H/L {h}/{l}"
        assert l <= o <= h, f"{path}: open outside range"
        assert l <= c <= h, f"{path}: close outside range"
        assert v >= 0, f"{path}: negative volume"
    return len(rows)


def validate_actions_file(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return 0
    assert ACTION_REQUIRED <= set(rows[0]), f"{path}: missing action columns {ACTION_REQUIRED - set(rows[0])}"
    symbols = {r["symbol"] for r in rows if r.get("symbol")}
    assert len(symbols) <= 1, f"{path}: multiple symbols {symbols}"
    dates = [r["ex_date"][:10] for r in rows if r.get("ex_date")]
    assert dates == sorted(dates), f"{path}: action dates not sorted"
    for r in rows:
        assert r.get("type"), f"{path}: blank action type"
    return len(rows)


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/cache/equities/tejhq_nse")
    price_files = sorted(p for p in root.glob("*.csv") if not p.name.endswith("_actions.csv"))
    action_files = sorted(p for p in root.glob("*_actions.csv"))
    assert price_files, f"no stock CSV files under {root}"
    total_prices = sum(validate_price_file(p) for p in price_files)
    total_actions = sum(validate_actions_file(p) for p in action_files)
    print(f"validated {len(price_files)} stock files / {total_prices} rows and {len(action_files)} action files / {total_actions} rows")


if __name__ == "__main__":
    main()
