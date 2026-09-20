from pathlib import Path

from src.data.validate_nifty50 import validate


def test_nifty50_validator_fixture(tmp_path: Path) -> None:
    path = tmp_path / "nifty.csv"
    path.write_text(
        "date,open,high,low,close,source_index\n"
        "2026-09-17,25000,25100,24900,25050,NIFTY 50\n"
        "2026-09-18,25050,25200,25000,25150,NIFTY 50\n",
        encoding="utf-8",
    )
    assert validate(path) == (2, "2026-09-17", "2026-09-18")
