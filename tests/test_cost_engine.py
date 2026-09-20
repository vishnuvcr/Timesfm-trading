from src.backtest.costs import ExecutionEvent, FeePolicy, estimate_execution_cost


def test_futures_sale_includes_brokerage_stt_and_slippage() -> None:
    event = ExecutionEvent(
        asset_class="futures",
        side="sell",
        quantity=1,
        price=100000,
        spread_bps=2.0,
        slippage_bps=1.0,
    )
    cost = estimate_execution_cost(event)
    assert cost.brokerage_inr == 10.0
    assert cost.stt_inr == 50.0
    assert cost.spread_slippage_inr == 30.0
    assert cost.total_inr == 90.0


def test_option_sale_stt_uses_premium_not_intrinsic() -> None:
    event = ExecutionEvent(
        asset_class="option",
        side="sell",
        quantity=100,
        price=100,
        premium=10000,
    )
    cost = estimate_execution_cost(event)
    assert cost.stt_inr == 15.0


def test_forced_squareoff_adds_broker_fee() -> None:
    event = ExecutionEvent(
        asset_class="futures",
        side="sell",
        quantity=1,
        price=100000,
        forced_squareoff=True,
    )
    cost = estimate_execution_cost(event)
    assert cost.squareoff_inr == 50.0
    assert cost.brokerage_inr == 10.0


def test_negative_quantity_rejected() -> None:
    event = ExecutionEvent(
        asset_class="cash_delivery",
        side="buy",
        quantity=-1,
        price=100,
    )
    try:
        estimate_execution_cost(event)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
