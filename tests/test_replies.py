"""Replies use only verified results: amounts from the Quote, status from the OrderRecord."""

from datetime import UTC, datetime

import pytest

from orderslm.core import replies
from orderslm.core.missing import required_missing
from orderslm.core.pricing import DeterministicPricing
from orderslm.menus import load_menu
from orderslm.schema.order import HandoffReason, HandoffTicket, OrderRecord, OrderStatus

from .builders import line, order

CP = load_menu("corner-patty")
HM = load_menu("halfmoon-pizza")
MC = load_menu("morning-crumb")
P = DeterministicPricing()
SEVEN_PM = {"state": "provided", "kind": "clock_time", "raw_text": "at 7", "normalized_local": "19:00",
            "evidence": [{"message_index": 0, "quote": "x"}]}  # fmt: skip


def test_spec_example_summary():
    o = order(
        line("L1", "cheeseburger"),
        line("L2", "cheeseburger", mods=[("remove", "onion")]),
        line("L3", "sprite"),
        time_=SEVEN_PM,
    )
    assert replies.summary(CP, P.quote(CP, o).data, o) == (
        "Got it: 1 Cheeseburger, 1 Cheeseburger (no onions), 1 Sprite. Pickup at 7:00 PM. "
        "Total $20.47, paying cash. Is that right?"
    )


def test_summary_amounts_come_from_the_quote_not_the_proposal():
    o = order(line("L1", "cheeseburger"))
    q = P.quote(CP, o).data
    tampered = q.model_copy(update={"total_cents": 12345})  # whatever the verified quote says is what we say
    assert "$123.45" in replies.summary(CP, tampered, o)


def test_delivery_summary_shows_fee_and_details():
    o = order(
        line(
            "L1", "pepperoni_pizza", variant="large", mods=[("add", "crust_thin"), ("add", "cheese", "extra")]
        ),
        method="delivery",
        address="410 Birch Ave",
        payment="card",
    )
    text = replies.summary(HM, P.quote(HM, o).data, o)
    # large pepperoni 1449 + 400, extra cheese 175 = 2024; fee 299 -> 2323
    assert text == (
        "Got it: 1 Pepperoni Pizza (Large 14-inch, add thin crust, extra house cheese blend). Delivery to 410 Birch Ave "
        "as soon as possible. Total $23.23 (incl. $2.99 delivery), paying by card. Is that right?"
    )


def test_template_question_covers_everything_missing():
    o = order(line("L1", "milkshake"), method="delivery", payment="unknown")
    q = replies.template_question(required_missing(o, CP), o, CP)
    assert q == (
        "Which milkshake would you like (vanilla, chocolate or strawberry), what's the delivery address, "
        "and will you pay by card or cash?"
    )


def test_template_question_off_menu_and_name():
    o = order(line("L1", unmatched="chicken sandwich"), line("L2", "drip_coffee"), payment="unknown",
              missing=[("item_menu_match", "off_menu", "L1")], question="?")  # fmt: skip
    q = replies.template_question(required_missing(o, MC), o, MC)
    assert q == (
        "We don't have chicken sandwich. Would you like something else instead? "
        "Also, will you pay by card or cash, and can I get a name for the order?"
    )


def test_model_question_used_unless_it_states_amounts():
    missing = [("payment_method", "missing")]
    ok = order(line("L1", "coke"), payment="unknown", missing=missing, question="Card or cash?")
    assert replies.clarification(ok, CP, required_missing(ok, CP)) == ("Card or cash?", "model")
    for bad in ("That's $2.49, card or cash?", "Total 2.49 - card or cash?"):
        o = order(line("L1", "coke"), payment="unknown", missing=missing, question=bad)
        text, source = replies.clarification(o, CP, required_missing(o, CP))
        assert source == "template" and "$" not in text


def test_pricing_problems():
    r = P.quote(CP, order(line("L1", "coke"), method="delivery", address="1 Main St"))
    assert replies.pricing_problem(r, CP) == (
        "Delivery needs a minimum order of $15.00; your order is $2.49 so far. Want to add something or switch to pickup?"
    )
    r = P.quote(MC, order(line("L1", "drip_coffee"), method="delivery", address="1 Main St"))
    assert (
        replies.pricing_problem(r, MC)
        == "Sorry, Morning Crumb Café is pickup only. Would pickup work for you?"
    )


def _record(status: OrderStatus, eta: int | None = None) -> OrderRecord:
    o = order(line("L1", "coke"))
    now = datetime(2026, 10, 7, 18, tzinfo=UTC)
    return OrderRecord(order_id="ord_1", business_id="corner-patty", conversation_id="c", status=status,
                       quote=P.quote(CP, o).data, created_at=now, updated_at=now, eta_minutes=eta)  # fmt: skip


def test_status_replies_come_from_the_record():
    assert replies.order_status(_record(OrderStatus.preparing, 15)) == (
        "Your order is being prepared. It'll be ready in about 15 minutes."
    )
    assert replies.order_status(_record(OrderStatus.ready)) == "Your order is ready!"
    assert replies.order_status(None) == "I couldn't find a placed order for this chat."
    assert (
        replies.order_placed(_record(OrderStatus.new, 20))
        == "Your order is in! It'll be ready in about 20 minutes."
    )


def test_payment_claim_reply_is_explicitly_pending():
    assert "pending" in replies.payment_claim()


def test_other_replies():
    ticket = HandoffTicket(ticket_id="hand_0001", conversation_id="c", reason=HandoffReason.customer_asked,
                           urgency="normal", summary="s", created_at=datetime(2026, 10, 7, tzinfo=UTC))  # fmt: skip
    assert "staff" in replies.handoff(ticket)
    assert replies.cancelled() and replies.needs_staff()


def test_unknown_language_is_an_error_not_english():
    with pytest.raises(KeyError, match="pt-BR"):
        replies.payment_claim("pt-BR")
