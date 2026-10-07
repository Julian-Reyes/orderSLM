"""Missing-info rules, snapshot diff, and the order state machine."""

import pytest

from orderslm.core.diff import diff_orders
from orderslm.core.missing import required_missing
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.state import OrderEvent, event_from_turn, ready_for_confirmation, transition
from orderslm.menus import load_menu
from orderslm.schema.order import OrderStatus, ToolErr, ToolOk

from .builders import line, order

CP = load_menu("corner-patty")
MC = load_menu("morning-crumb")
S, E = OrderStatus, OrderEvent


def fields(missing) -> list[tuple[str, str | None]]:
    return [(m.field.value, m.line_id) for m in missing]


# ---- missing info


def test_complete_order_needs_nothing():
    assert required_missing(order(line("L1", "cheeseburger")), CP) == []


def test_each_missing_field():
    o = order(line("L1", "milkshake"), line("L2", "cheeseburger_combo"), method="delivery", payment="unknown")
    assert fields(required_missing(o, CP)) == [
        ("item_variant", "L1"),
        ("combo_choice", "L2"),
        ("address", None),
        ("payment_method", None),
    ]
    assert fields(required_missing(order(method="unknown"), CP)) == [
        ("items", None),
        ("fulfillment_method", None),
    ]


def test_payment_claim_without_method_is_not_asked_again():
    assert required_missing(order(line("L1", "coke"), payment="unknown", claims_paid=True), CP) == []


def test_name_required_only_for_pickup_at_that_business():
    assert fields(required_missing(order(line("L1", "drip_coffee")), MC)) == [("customer_name", None)]
    assert required_missing(order(line("L1", "drip_coffee"), name="Dana"), MC) == []
    assert required_missing(order(line("L1", "cheeseburger")), CP) == []  # Corner Patty doesn't require it


def test_cancelled_order_needs_nothing():
    assert required_missing(order(line("L1", "milkshake"), payment="unknown", decision="cancelled"), CP) == []


def test_sample_gold_missing_info_follows_the_rules(samples, menus):
    """Annotation consistency: gold missing_or_ambiguous equals what the guide's rules derive."""
    for s in samples:
        if s.gold_extraction is not None:
            g = s.gold_extraction
            assert fields(required_missing(g, menus[s.conversation.business_id])) == fields(
                g.missing_or_ambiguous
            ), s.conversation.id


# ---- diff (the patch shown to the business)


def test_first_snapshot_adds_everything():
    p = diff_orders(None, order(line("L1", "cheeseburger"), line("L2", "coke")))
    assert p.lines_added == ["L1", "L2"] and p.lines_removed == [] and "payment" in p.fields_changed


def test_swap_and_correction():
    before = order(line("L1", "cheeseburger", qty=2), line("L2", "coke"))
    after = order(
        line("L1", "cheeseburger", qty=1),
        line("L3", "cheeseburger", mods=[("remove", "onion")]),
        line("L4", "sprite"),
    )
    p = diff_orders(before, after)
    assert p.lines_added == ["L3", "L4"] and p.lines_removed == ["L2"]
    assert [(c.line_id, c.fields) for c in p.lines_changed] == [("L1", ["quantity"])]


def test_requoting_the_same_order_is_not_a_change():
    a = order(line("L1", "cheeseburger", mods=[("remove", "onion")]))
    b = a.model_copy(deep=True)
    b.items[0].evidence[0].quote = "different quote"
    b.items[0].modifications[0].raw_text = "hold the onions"
    assert diff_orders(a, b).is_empty


def test_field_changes():
    p = diff_orders(order(line("L1", "coke")), order(line("L1", "coke"), payment="card", name="Al"))
    assert p.fields_changed == ["payment", "customer_name"] and not p.items_changed


# ---- state machine


@pytest.mark.parametrize(
    ("path", "end"),
    [
        (
            [E.summary_sent, E.customer_confirmed, E.staff_started, E.staff_ready, E.staff_completed],
            S.completed,
        ),
        ([E.summary_sent, E.customer_modified, E.summary_sent, E.customer_confirmed], S.new),
        ([E.customer_cancelled], S.cancelled),
        ([E.summary_sent, E.customer_confirmed, E.staff_cancelled], S.cancelled),
    ],
)
def test_valid_paths(path, end):
    status = S.draft
    for ev in path:
        r = transition(status, ev)
        assert isinstance(r, ToolOk), (status, ev)
        status = r.data
    assert status is end


def test_confirmation_needs_a_summary_first():
    r = transition(S.draft, E.customer_confirmed)
    assert isinstance(r, ToolErr) and r.error.code == "INVALID_TRANSITION"


@pytest.mark.parametrize("status", [S.new, S.preparing, S.ready])
@pytest.mark.parametrize("event", [E.customer_modified, E.customer_cancelled])
def test_customer_changes_to_a_placed_order_go_to_staff(status, event):
    r = transition(status, event)
    assert isinstance(r, ToolErr) and r.error.code == "NEEDS_STAFF"


def test_terminal_states():
    for status in (S.completed, S.cancelled):
        for ev in E:
            assert isinstance(transition(status, ev), ToolErr)


def test_event_from_turn():
    base = order(line("L1", "cheeseburger"))
    yes = order(line("L1", "cheeseburger"), decision="confirmed")
    assert event_from_turn(S.awaiting_confirmation, base, yes) is E.customer_confirmed
    assert event_from_turn(S.draft, base, yes) is None  # "yes" with no summary sent
    changed_and_yes = order(line("L1", "cheeseburger", qty=2), decision="confirmed")
    assert event_from_turn(S.awaiting_confirmation, base, changed_and_yes) is E.customer_modified
    assert (
        event_from_turn(S.draft, base, order(line("L1", "cheeseburger"), decision="cancelled"))
        is E.customer_cancelled
    )
    assert event_from_turn(S.draft, base, base) is None


def test_ready_for_confirmation_needs_complete_info_and_a_price():
    pricing = DeterministicPricing()
    ok = order(line("L1", "cheeseburger"))
    assert ready_for_confirmation(ok, CP, pricing.quote(CP, ok))
    no_pay = order(
        line("L1", "cheeseburger"), payment="unknown", missing=[("payment_method", "missing")], question="?"
    )
    assert not ready_for_confirmation(no_pay, CP, pricing.quote(CP, no_pay))
    no_size = order(line("L1", "milkshake"))  # model forgot to flag it; the rules still catch it
    assert not ready_for_confirmation(no_size, CP, pricing.quote(CP, no_size))
