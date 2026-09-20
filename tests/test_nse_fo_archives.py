from datetime import date

from src.data.nse_fo_archives import UDIFF_START, plan_for_date


def test_legacy_archive_before_udiff() -> None:
    plan=plan_for_date(date(2024,7,5))
    assert plan.format=="legacy"
    assert plan.filename=="fo05JUL2024bhav.csv.zip"
    assert all("historical/DERIVATIVES/2024/JUL/" in u for u in plan.urls)


def test_udiff_archive_from_transition_date() -> None:
    plan=plan_for_date(UDIFF_START)
    assert plan.format=="udiff"
    assert plan.filename=="BhavCopy_NSE_FO_0_0_0_20240708_F_0000.csv.zip"
    assert all("/content/fo/" in u for u in plan.urls)
