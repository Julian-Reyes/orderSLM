"""Verified results (quotes, tool results) and the money/clock conventions."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from orderslm.domain.clock import fixed_clock
from orderslm.domain.money import format_cents, percent_of
from orderslm.mocks.tools import InMemoryBusinessTools
from orderslm.schema.order import HandoffReason, OrderRecord, OrderStatus, Quote, ToolErr, ToolOk
from orderslm.schema.routing import Urgency

NOW = datetime(2026, 10, 7, 18, 0, tzinfo=UTC)


def quote(**over) -> dict:
    q = {
        "business_id": "corner-patty",
        "currency": "USD",
        "fulfillment": "pickup",
        "lines": [
            {"line_id": "L1", "menu_item_id": "cheeseburger", "display_name": "Cheeseburger", "quantity": 2,
             "unit_price_cents": 899, "line_total_cents": 1798},
            {"line_id": "L2", "menu_item_id": "sprite", "display_name": "Sprite", "quantity": 1,
             "unit_price_cents": 249, "line_total_cents": 249},
        ],
        "subtotal_cents": 2047,
        "total_cents": 2047,
        "verified_by": "pricing@test",
        "menu_version": "corner-patty@sample",
    }  # fmt: skip
    q.update(over)
    return q


def test_consistent_quote_validates():
    assert Quote.model_validate(quote()).total_cents == 2047


@pytest.mark.parametrize(
    "over",
    [
        {"subtotal_cents": 2048, "total_cents": 2048},  # subtotal doesn't add up
        {"total_cents": 2000},  # total doesn't add up
        {"delivery_fee_cents": 399, "total_cents": 2446},  # fee on a pickup order
    ],
)
def test_inconsistent_quote_cannot_exist(over):
    with pytest.raises(ValidationError):
        Quote.model_validate(quote(**over))


def test_line_total_must_be_unit_times_quantity():
    q = quote()
    q["lines"][0]["line_total_cents"] = 1800
    with pytest.raises(ValidationError, match="unit_price_cents \\* quantity"):
        Quote.model_validate(q)


@pytest.mark.parametrize("bad", [20.47, "2047", -1])
def test_money_is_strict_non_negative_integer_cents(bad):
    with pytest.raises(ValidationError):
        Quote.model_validate(quote(subtotal_cents=bad, total_cents=bad))


def test_delivery_quote_with_fee():
    q = Quote.model_validate(quote(fulfillment="delivery", delivery_fee_cents=399, total_cents=2446))
    assert format_cents(q.total_cents) == "$24.46"


def test_money_helpers():
    assert percent_of(1999, 10) == 200  # 199.9 rounds half-up
    assert percent_of(1995, 10) == 200  # 199.5 rounds up
    assert format_cents(5) == "$0.05"
    with pytest.raises(TypeError):
        percent_of(19.99, 10)


def test_clock_must_be_timezone_aware():
    assert fixed_clock("2026-10-07T18:00:00+00:00")() == NOW
    with pytest.raises(ValueError):
        fixed_clock("2026-10-07T18:00:00")


# ---- tool results and mock tools


def order(order_id="ord_1", convo="sample-007", created=NOW) -> OrderRecord:
    return OrderRecord(
        order_id=order_id,
        business_id="corner-patty",
        conversation_id=convo,
        status=OrderStatus.preparing,
        quote=Quote.model_validate(quote()),
        created_at=created,
        updated_at=created,
        eta_minutes=15,
    )


def test_tool_result_discriminates_on_ok():
    ok = ToolOk[OrderRecord](data=order(), verified_by="t")
    assert ok.ok is True
    with pytest.raises(ValidationError):
        ToolOk[OrderRecord](ok=False, data=order(), verified_by="t")
    with pytest.raises(ValidationError):
        ToolErr(error={"code": "not found", "message": "x"}, verified_by="t")  # codes are UPPER_SNAKE


def test_lookup_and_status():
    tools = InMemoryBusinessTools(
        fixed_clock(), [order("ord_1"), order("ord_2", created=NOW.replace(hour=19))]
    )
    found = tools.lookup_order("sample-007")
    assert isinstance(found, ToolOk) and found.data.order_id == "ord_2"  # most recent
    assert found.verified_by.endswith(":lookup_order")
    status = tools.order_status("ord_1")
    assert isinstance(status, ToolOk) and status.data.status is OrderStatus.preparing


def test_business_outcomes_are_results_not_exceptions():
    tools = InMemoryBusinessTools(fixed_clock())
    missing = tools.lookup_order("nobody")
    assert isinstance(missing, ToolErr) and missing.error.code == "NOT_FOUND"
    assert isinstance(tools.order_status("ord_x"), ToolErr)


def test_handoff_queue_uses_injected_clock():
    tools = InMemoryBusinessTools(fixed_clock())
    res = tools.request_handoff(
        "sample-008", HandoffReason.refund_request, Urgency.normal, "Missing bacon; wants refund"
    )
    assert isinstance(res, ToolOk)
    assert res.data.created_at == NOW and res.data.ticket_id == "hand_0001"
    assert tools.handoff_queue == [res.data]
    assert isinstance(
        tools.request_handoff("sample-008", HandoffReason.unclear, Urgency.normal, "  "), ToolErr
    )


def test_payment_confirmation_lives_only_on_the_verified_record():
    assert order().payment_confirmed is False
