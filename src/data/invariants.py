from __future__ import annotations

from datetime import date, datetime


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_equity_bar(row: dict) -> list[str]:
    errors=[]
    o,h,l,c=row.get("open"),row.get("high"),row.get("low"),row.get("close")
    if any(v is None for v in (o,h,l,c)):
        return ["OHLC contains null"]
    if h < max(o,c) or l > min(o,c) or h < l:
        errors.append("invalid OHLC ordering")
    if row.get("volume",0) < 0:
        errors.append("negative volume")
    if _dt(row["availability_timestamp"]) < _dt(row["event_timestamp"]):
        errors.append("availability precedes event")
    return errors


def validate_option_quote(row: dict) -> list[str]:
    errors=[]
    bid,ask=row.get("bid"),row.get("ask")
    if bid is not None and ask is not None and (bid < 0 or ask < 0 or bid > ask):
        errors.append("invalid bid/ask")
    if row.get("open_interest") is not None and row["open_interest"] < 0:
        errors.append("negative open interest")
    if row.get("volume") is not None and row["volume"] < 0:
        errors.append("negative volume")
    if date.fromisoformat(row["expiry"]) < _dt(row["event_timestamp"]).date():
        errors.append("quote occurs after expiry")
    if _dt(row["availability_timestamp"]) < _dt(row["event_timestamp"]):
        errors.append("availability precedes quote event")
    return errors


def validate_derivative_contract(row: dict) -> list[str]:
    errors=[]
    listing=_dt(row["listing_timestamp"]).date()
    expiry=date.fromisoformat(row["expiry"])
    if expiry < listing:
        errors.append("expiry precedes listing")
    last=row.get("last_trading_timestamp")
    if last is not None and _dt(last).date() < listing:
        errors.append("last trading date precedes listing")
    if row.get("lot_size") is not None and row["lot_size"] <= 0:
        errors.append("non-positive lot size")
    if row.get("tick_size") is not None and row["tick_size"] <= 0:
        errors.append("non-positive tick size")
    return errors


def validate_corporate_action(row: dict) -> list[str]:
    errors=[]
    announced=_dt(row["announcement_timestamp"]).date()
    for field in ("ex_date","record_date"):
        value=row.get(field)
        if value is not None and date.fromisoformat(value) < announced:
            errors.append(f"{field} precedes announcement")
    return errors
