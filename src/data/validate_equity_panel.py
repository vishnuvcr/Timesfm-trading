from __future__ import annotations

import csv
import sys
from pathlib import Path

REQUIRED = {"date","symbol","open","high","low","close","volume"}


def as_float(v: str, field: str, path: Path) -> float:
    try:
        return float(v)
    except Exception as exc:
        raise AssertionError(f"{path}: non-numeric {field}={v!r}") from exc


def validate_file(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows, f"{path}: empty"
    assert REQUIRED <= set(rows[0]), f"{path}: missing columns {REQUIRED - set(rows[0])}"
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


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/cache/equities/tejhq_nse")
    files = sorted(p for p in root.glob("*.csv") if p.name != "manifest.csv")
    assert files, f"no CSV files under {root}"
    total = sum(validate_file(p) for p in files)
    print(f"validated {len(files)} stock files / {total} rows")


if __name__ == "__main__":
    main()
