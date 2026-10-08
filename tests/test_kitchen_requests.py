"""Requests with no menu id, the summary guard, and payment claims (Julian's rulings, 2026-10-08).

- Gold must classify every request with no menu id: not_on_menu or kitchen_note.
- The menu's accepted_kitchen_requests are matched first: a match is a free kitchen note.
- At runtime, anything else unclassified is unverified: asked with softer wording, never priced,
  never on the ticket.
- No summary while anything is missing; a payment claim is never presented as a confirmed payment.
"""

import pytest

from orderslm.checks import check_requests
from orderslm.core.missing import required_missing
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.replies import next_reply, summary, template_question
from orderslm.core.requests import RequestStatus, accepted_request, request_status
from orderslm.core.ticket import ticket_lines
from orderslm.menus import load_menu, load_menus
from orderslm.schema.extraction import Modification

from .builders import line, order

P = DeterministicPricing()
CP = load_menu("corner-patty")
HM = load_menu("halfmoon-pizza")


def req(text: str, **flags) -> dict:
    return {"kind": "add", "modifier_id": None, "raw_text": text, **flags}


def gold(menu, *lines, **kw):
    """An order whose missing list and question are what the rules derive (as gold must be)."""
    draft = order(*lines, **kw)
    found = [(m.field.value, m.reason.value, m.line_id) for m in required_missing(draft, menu)]
    if not found:
        return draft
    full = order(*lines, missing=found, question="?", **kw)
    return order(
        *lines, missing=found, question=template_question(full.missing_or_ambiguous, full, menu), **kw
    )


# ---------------------------------------------------------------- gold must classify


def test_unclassified_request_fails_the_gold_check():
    unclassified = order(line("L1", "garlic_knots", mods=[req("warm")]))
    assert [i.code for i in check_requests(unclassified)] == ["UNCLASSIFIED_REQUEST"]
    assert check_requests(order(line("L1", "garlic_knots", mods=[req("warm", kitchen_note=True)]))) == []


def test_a_request_is_never_both():
    with pytest.raises(ValueError):
        Modification.model_validate(req("warm", kitchen_note=True, not_on_menu=True))


def test_kitchen_note_only_without_a_menu_id():
    with pytest.raises(ValueError):
        Modification.model_validate(
            {"kind": "add", "modifier_id": "bacon", "raw_text": "bacon", "kitchen_note": True}
        )


# ---------------------------------------------------------------- accepted list first


@pytest.mark.parametrize("flags", [{}, {"not_on_menu": True}, {"kitchen_note": True}])
def test_accepted_request_is_a_kitchen_note_whatever_the_model_said(flags):
    burger = CP.item("cheeseburger")
    assert request_status(CP, burger, Modification.model_validate(req("make it well done pls", **flags))) is (
        RequestStatus.kitchen_note
    )


def test_accepted_requests_respect_categories_and_whole_words():
    assert accepted_request(CP, CP.item("cheeseburger"), "well done") is not None
    assert accepted_request(CP, CP.item("coke"), "well done") is None  # drinks aren't cooked
    assert accepted_request(HM, HM.item("pepperoni_pizza"), "cut in squares").id == "square_cut"
    assert accepted_request(HM, HM.item("pepperoni_pizza"), "squaresville") is None


def test_accepted_kitchen_note_is_free_and_printed_on_the_ticket():
    o = order(line("L1", "cheeseburger", mods=[req("well done", kitchen_note=True)]))
    q = P.quote(CP, o)
    assert q.ok and q.data.total_cents == 899
    assert ticket_lines(CP, q.data, o)[0] == "1 Cheeseburger (well done)"


def test_every_menu_has_accepted_kitchen_requests():
    assert all(m.accepted_kitchen_requests for m in load_menus(include_held_out=True).values())


# ---------------------------------------------------------------- runtime fallback


@pytest.mark.parametrize("flags", [{}, {"kitchen_note": True}])
def test_unknown_request_is_asked_softly_and_never_priced(flags):
    burger = line("L1", "cheeseburger", mods=[req("with truffle oil", **flags)])
    assert [(m.field.value, m.reason.value) for m in required_missing(order(burger), CP)] == [
        ("item_modification", "ambiguous")
    ]
    o = gold(CP, burger)
    r = P.quote(CP, o)
    assert not r.ok and r.error.code == "REQUEST_UNVERIFIED"
    text, kind = next_reply(CP, o, r)
    assert kind == "question"
    assert text == (
        "Just checking, we may not be able to do truffle oil on the cheeseburger. "
        "Want it without, or keep it as a note for the kitchen?"
    )


def test_not_on_menu_request_is_told_firmly():
    o = gold(
        HM,
        line("L1", "supreme_pizza", variant="large", mods=[req("with artichoke hearts", not_on_menu=True)]),
    )
    text, kind = next_reply(HM, o, P.quote(HM, o))
    assert kind == "question" and text.startswith("We don't have artichoke hearts for the supreme pizza.")


def test_unresolved_request_never_reaches_the_ticket():
    o = gold(CP, line("L1", "cheeseburger", mods=[req("with truffle oil")]))
    quote = P.quote(CP, order(line("L1", "cheeseburger"))).data  # even with some valid quote in hand
    with pytest.raises(ValueError):
        ticket_lines(CP, quote, o)


# ---------------------------------------------------------------- no summary while anything is missing


def test_no_summary_while_something_is_missing():
    o = gold(CP, line("L1", "cheeseburger"), method="unknown")
    r = P.quote(CP, o)
    assert r.ok  # it can be priced...
    with pytest.raises(ValueError):
        summary(CP, r.data, o)  # ...but a summary is never sent
    text, kind = next_reply(CP, o, r)
    assert kind == "question" and text == "Is this for pickup or delivery?"


def test_complete_order_gets_the_summary():
    o = order(line("L1", "cheeseburger"))
    text, kind = next_reply(CP, o, P.quote(CP, o))
    assert kind == "summary" and text.startswith("Got it: 1 Cheeseburger.")


# ---------------------------------------------------------------- payment claims


def test_summary_never_says_a_claimed_payment_is_confirmed():
    o = order(line("L1", "cheeseburger"), payment="unknown", claims_paid=True)
    text = summary(CP, P.quote(CP, o).data, o)
    assert text == (
        "Got it: 1 Cheeseburger. Pickup as soon as possible. Total $8.99. "
        "You mentioned you've already paid, and the restaurant will confirm it. Is that right?"
    )


def test_ticket_flags_a_claimed_payment_for_staff():
    o = order(line("L1", "cheeseburger"), payment="unknown", claims_paid=True)
    q = P.quote(CP, o).data
    assert ticket_lines(CP, q, o)[-1] == "Payment: customer says paid, not verified"
    assert ticket_lines(CP, q, o, payment_confirmed=True)[-1] == "Payment: paid (verified)"


def test_ticket_payment_lines():
    o = order(line("L1", "cheeseburger"), payment="cash")
    assert ticket_lines(CP, P.quote(CP, o).data, o)[-2:] == ["Total: $8.99", "Payment: cash"]
