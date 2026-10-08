"""extraction@0.3 / menu@0.4 (Julian's dev-card rulings, 2026-10-08):

- an option the menu doesn't offer (`not_on_menu`) is flagged, never priced, never summarized;
- a size the item doesn't have (`unmatched_variant_text`) keeps the item on the menu and asks for a size;
- `confirmed` only when nothing is missing; a yes with gaps is `pending` + `agreed_while_incomplete`;
- pizza sizes carry diameter/slices for the reply layer only; the extractor never sees them.
"""

import pytest
from pydantic import ValidationError

from orderslm.core.missing import required_missing
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.replies import _line_text, template_question
from orderslm.interfaces.extractor import ExtractionRequest
from orderslm.menus import load_menu, load_menus
from orderslm.schema.extraction import CustomerDecision, Modification

from .builders import EV, conversation, line, order

P = DeterministicPricing()
CP = load_menu("corner-patty")
HM = load_menu("halfmoon-pizza")

ARTICHOKE = {"kind": "add", "modifier_id": None, "raw_text": "with artichoke hearts", "not_on_menu": True}
WARM = {"kind": "add", "modifier_id": None, "raw_text": "warm"}


def missing(menu, proposal) -> list[tuple[str, str, str | None]]:
    return [(m.field.value, m.reason.value, m.line_id) for m in required_missing(proposal, menu)]


def with_missing(menu, *lines, **kw):
    """An order whose missing list is exactly what the rules derive (as gold must be)."""
    draft = order(*lines, **kw)
    found = missing(menu, draft)
    return order(*lines, missing=found, question="?" if found else None, **kw)


# ---------------------------------------------------------------- options the menu doesn't offer


def test_not_on_menu_option_is_flagged_and_never_priced():
    pizza = line("L1", "supreme_pizza", variant="large", mods=[ARTICHOKE])
    assert missing(HM, order(pizza)) == [("item_modification", "off_menu", "L1")]
    r = P.quote(HM, with_missing(HM, pizza))
    assert not r.ok and r.error.code == "OPTION_NOT_ON_MENU"


def test_not_on_menu_on_a_half_is_flagged_too():
    pizza = line(
        "L1",
        variant="large",
        halves=[{"menu_item_id": "cheese_pizza", "modifications": [ARTICHOKE]}, "veggie_pizza"],
    )
    assert missing(HM, order(pizza)) == [("item_modification", "off_menu", "L1")]


def test_kitchen_request_is_a_free_note_not_a_flag():
    knots = line("L1", "garlic_knots", mods=[WARM])
    assert missing(HM, order(knots)) == []
    r = P.quote(HM, order(knots))
    assert r.ok and r.data.total_cents == 599  # garlic knots $5.99, the note is free


def test_not_on_menu_reply_names_the_option_and_offers_choices():
    proposal = with_missing(HM, line("L1", "supreme_pizza", variant="large", mods=[ARTICHOKE]))
    assert template_question(proposal.missing_or_ambiguous, proposal, HM) == (
        "We don't have artichoke hearts for the supreme pizza. Would you like it without, or something else?"
    )


def test_not_on_menu_option_never_appears_in_a_summary_line():
    proposal = with_missing(HM, line("L1", "supreme_pizza", variant="large", mods=[ARTICHOKE]))
    assert "artichoke" not in _line_text(HM, proposal, "L1", "en")


@pytest.mark.parametrize(
    "bad",
    [
        {
            "kind": "add",
            "modifier_id": "olives",
            "raw_text": "olives",
            "not_on_menu": True,
        },  # has a catalog id
        {"kind": "remove", "modifier_id": None, "raw_text": "no truffle", "not_on_menu": True},  # removal
    ],
)
def test_not_on_menu_shape(bad):
    with pytest.raises(ValidationError):
        Modification.model_validate(bad)


def test_not_on_menu_substitute_keeps_the_replaced_option():
    m = Modification(
        kind="substitute", modifier_id="whole_milk", raw_text="soy milk instead", not_on_menu=True
    )
    assert m.added_id is None


# ---------------------------------------------------------------- sizes the item doesn't have


def test_unmatched_size_keeps_the_item_and_asks_for_a_size():
    pizzas = {**line("L1", "pepperoni_pizza", qty=2), "unmatched_variant_text": "party size"}
    assert missing(HM, order(pizzas)) == [("item_variant", "missing", "L1")]
    proposal = with_missing(HM, pizzas)
    assert template_question(proposal.missing_or_ambiguous, proposal, HM).startswith(
        "We don't have a party size for the pepperoni pizza; we have personal 8-inch, small 10-inch"
    )


def test_unmatched_size_never_falls_back_to_the_default():
    fries = {**line("L1", "fries"), "unmatched_variant_text": "medium"}  # fries: regular (default) or large
    assert missing(CP, order(fries)) == [("item_variant", "missing", "L1")]
    r = P.quote(CP, with_missing(CP, fries))
    assert not r.ok and r.error.code == "MISSING_VARIANT"


def test_unmatched_size_only_without_a_variant():
    with pytest.raises(ValidationError):
        order({**line("L1", "fries", variant="large"), "unmatched_variant_text": "medium"})


# ---------------------------------------------------------------- confirmed means complete


def test_confirmed_with_something_missing_is_rejected():
    with pytest.raises(ValidationError, match="confirmed only when nothing is missing"):
        order(line("L1", "cheeseburger"), method="unknown", decision="confirmed",
              missing=[("fulfillment_method", "missing")], question="Pickup or delivery?")  # fmt: skip


def test_a_yes_with_gaps_is_pending_and_recorded():
    d = CustomerDecision(state="pending", agreed_while_incomplete=True, evidence=EV)
    assert d.state.value == "pending" and d.agreed_while_incomplete


@pytest.mark.parametrize(
    "bad",
    [
        {"state": "confirmed", "agreed_while_incomplete": True, "evidence": EV},
        {"state": "pending", "agreed_while_incomplete": True},  # an agreement needs evidence
    ],
)
def test_agreement_shape(bad):
    with pytest.raises(ValidationError):
        CustomerDecision.model_validate(bad)


# ---------------------------------------------------------------- pizza sizes: reply layer only


def test_every_pizza_size_has_diameter_and_slices():
    for menu in load_menus(include_held_out=True).values():
        for item in menu.items:
            if item.category == "pizzas":
                assert item.variants and all(v.diameter_cm and v.slices for v in item.variants), item.id


def test_extractor_view_drops_size_facts_and_nothing_else():
    view = HM.extractor_view()
    assert not view.has_reply_only_fields() and HM.has_reply_only_fields()
    strip = {"diameter_cm", "slices"}
    for full, seen in zip(HM.items, view.items, strict=True):
        assert full.model_dump(exclude={"variants"}) == seen.model_dump(exclude={"variants"})
        for v, w in zip(full.variants, seen.variants, strict=True):
            assert v.model_dump(exclude=strip) == w.model_dump(exclude=strip)


def test_extraction_request_rejects_a_menu_with_size_facts():
    convo = conversation(("customer", "large pepperoni"), business="halfmoon-pizza")
    with pytest.raises(ValidationError, match="extractor_view"):
        ExtractionRequest(menu=HM, conversation=convo, prompt_version="t")
    ExtractionRequest(menu=HM.extractor_view(), conversation=convo, prompt_version="t")


def test_size_facts_never_change_a_price():
    sizes = ("personal", "small", "medium", "large", "extra_large")
    pizzas = order(*(line(f"L{n}", "pepperoni_pizza", variant=v) for n, v in enumerate(sizes, 1)))
    assert P.quote(HM, pizzas).data.total_cents == P.quote(HM.extractor_view(), pizzas).data.total_cents
