import json
from pathlib import Path


def test_fee_manifest_has_current_verified_rules() -> None:
    data = json.loads(Path("configs/fee_manifest_2026-09-20.json").read_text())
    assert data["effective_date"] == "2026-04-01"
    assert data["nse_stt"]["option_sale_rate"] == 0.0015
    assert data["nse_stt"]["futures_sale_rate"] == 0.0005
    assert data["paytm_money"]["fno_brokerage_per_unique_executed_order_inr"] == 10.0
    assert data["paytm_money"]["intraday_squareoff_charge_per_order_inr"] == 50.0
