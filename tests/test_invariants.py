from src.data.invariants import validate_corporate_action, validate_derivative_contract, validate_equity_bar, validate_option_quote


def test_good_equity_bar() -> None:
    row={"open":100,"high":105,"low":99,"close":104,"volume":10,"event_timestamp":"2026-09-20T10:00:00+05:30","availability_timestamp":"2026-09-20T10:00:01+05:30"}
    assert validate_equity_bar(row)==[]


def test_bad_option_quote() -> None:
    row={"bid":11,"ask":10,"open_interest":1,"volume":1,"expiry":"2026-09-23","event_timestamp":"2026-09-20T10:00:00+05:30","availability_timestamp":"2026-09-20T10:00:00+05:30"}
    assert "invalid bid/ask" in validate_option_quote(row)


def test_bad_derivative_contract() -> None:
    row={"listing_timestamp":"2026-09-20T00:00:00+05:30","expiry":"2026-09-19","lot_size":1,"tick_size":0.05}
    assert "expiry precedes listing" in validate_derivative_contract(row)


def test_bad_corporate_action() -> None:
    row={"announcement_timestamp":"2026-09-20T10:00:00+05:30","ex_date":"2026-09-19","record_date":None}
    assert "ex_date precedes announcement" in validate_corporate_action(row)
