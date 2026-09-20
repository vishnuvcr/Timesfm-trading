from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeePolicy:
    fno_brokerage_per_order_inr: float = 10.0
    intraday_squareoff_per_order_inr: float = 50.0
    option_sale_stt_rate: float = 0.0015
    futures_sale_stt_rate: float = 0.0005
    cash_delivery_buy_stt_rate: float = 0.0010
    cash_delivery_sell_stt_rate: float = 0.0010
    cash_intraday_sell_stt_rate: float = 0.00025


@dataclass(frozen=True)
class ExecutionEvent:
    asset_class: str
    side: str
    quantity: float
    price: float
    unique_order: bool = True
    forced_squareoff: bool = False
    spread_bps: float = 0.0
    slippage_bps: float = 0.0
    premium: float | None = None
    intrinsic_value: float | None = None


@dataclass(frozen=True)
class CostBreakdown:
    brokerage_inr: float
    stt_inr: float
    spread_slippage_inr: float
    squareoff_inr: float
    total_inr: float


def _notional(event: ExecutionEvent) -> float:
    return abs(event.quantity * event.price)


def _slippage_cost(event: ExecutionEvent) -> float:
    notional = _notional(event)
    return notional * (max(0.0, event.spread_bps) + max(0.0, event.slippage_bps)) / 10000.0


def estimate_execution_cost(event: ExecutionEvent, policy: FeePolicy = FeePolicy()) -> CostBreakdown:
    if event.quantity <= 0 or event.price < 0:
        raise ValueError("quantity must be positive and price must be non-negative")
    side = event.side.lower()
    if side not in {"buy", "sell"}:
        raise ValueError("side must be buy or sell")

    notional = _notional(event)
    brokerage = policy.fno_brokerage_per_order_inr if event.unique_order and event.asset_class in {"futures", "option"} else 0.0
    squareoff = policy.intraday_squareoff_per_order_inr if event.forced_squareoff else 0.0

    stt = 0.0
    if event.asset_class == "option" and side == "sell":
        stt = notional * policy.option_sale_stt_rate
    elif event.asset_class == "futures" and side == "sell":
        stt = notional * policy.futures_sale_stt_rate
    elif event.asset_class == "cash_delivery" and side == "buy":
        stt = notional * policy.cash_delivery_buy_stt_rate
    elif event.asset_class == "cash_delivery" and side == "sell":
        stt = notional * policy.cash_delivery_sell_stt_rate
    elif event.asset_class == "cash_intraday" and side == "sell":
        stt = notional * policy.cash_intraday_sell_stt_rate
    elif event.asset_class == "option_exercise":
        intrinsic = max(0.0, event.intrinsic_value or 0.0)
        stt = intrinsic * policy.option_sale_stt_rate

    spread_slippage = _slippage_cost(event)
    total = brokerage + stt + spread_slippage + squareoff
    return CostBreakdown(
        brokerage_inr=brokerage,
        stt_inr=stt,
        spread_slippage_inr=spread_slippage,
        squareoff_inr=squareoff,
        total_inr=total,
    )
