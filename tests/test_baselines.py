"""Rules baselines (extractor + keyword router). Conversations here are written for these tests;
the sample conversations are deliberately not used, so they never serve as an evaluation set."""

import pytest

from orderslm.baselines.rules_extractor import RulesExtractor, extract_rules
from orderslm.baselines.rules_router import KeywordDecisionProvider
from orderslm.checks import check_all
from orderslm.interfaces.decision import DecisionProvider, validate_response
from orderslm.interfaces.extractor import ExtractionRequest, OrderExtractor
from orderslm.menus import load_menu
from orderslm.router import (
    RouterContext,
    build_router_request,
    parse_input,
    parse_router_response,
    render_input,
)
from orderslm.schema.extraction import ExtractionOutput
from orderslm.schema.routing import RouterLabel

from .builders import conversation

C, B = "customer", "business"
MENUS = {b: load_menu(b) for b in ("corner-patty", "halfmoon-pizza", "morning-crumb")}


def run(business: str, *messages: tuple[str, str]) -> ExtractionOutput:
    convo = conversation(*messages, business=business)
    out = extract_rules(MENUS[business], convo.messages)
    assert check_all(out, convo, MENUS[business]) == []  # always grounded: quotes exist, ids exist
    return out


def items(out: ExtractionOutput) -> list[tuple]:
    return [
        (i.menu_item_id or tuple(h.menu_item_id for h in i.halves), i.quantity, i.variant_id,
         tuple((m.kind.value, m.modifier_id, m.amount.value) for m in i.modifications))
        for i in out.items
    ]  # fmt: skip


# ---- extractor


def test_protocol_and_parse_path():
    ext = RulesExtractor()
    assert isinstance(ext, OrderExtractor)
    convo = conversation((C, "2 cokes pls, pickup, cash"))
    res = ext.extract(
        ExtractionRequest(menu=MENUS["corner-patty"], conversation=convo, prompt_version="rules")
    )
    assert res.output is not None and res.error is None and res.extractor == "rules/extractor@0.1"


def test_spec_example_with_corrections():
    out = run(
        "corner-patty",
        (C, "hey can i get 2 cheeseburgers and a coke"),
        (C, "actually make one of them no onions"),
        (C, "and swap the coke for a sprite"),
        (C, "pickup at 7, paying cash"),
    )
    assert items(out) == [
        ("cheeseburger", 1, None, ()),
        ("cheeseburger", 1, None, (("remove", "onion", "normal"),)),
        ("sprite", 1, None, ()),
    ]
    assert out.fulfillment.method.value == "pickup"
    assert out.fulfillment.requested_time.normalized_local == "19:00"  # open 11-22, so 7 means 7 pm
    assert out.payment.method.value == "cash" and out.missing_or_ambiguous == []


def test_quantity_correction_and_removal():
    out = run(
        "corner-patty",
        (C, "a cheeseburger, onion rings and a lemonade"),
        (C, "make it 3 cheeseburgers"),
        (C, "remove the lemonade"),
    )
    assert items(out) == [("cheeseburger", 3, None, ()), ("onion_rings", 1, None, ())]


def test_toppings_amounts_and_crust():
    out = run(
        "halfmoon-pizza",
        (C, "large pizza with pepperoni and mushrooms, thin crust, light on the sauce, extra cheese"),
    )
    assert items(out) == [
        ("cheese_pizza", 1, "large", (("add", "pepperoni", "normal"), ("add", "mushrooms", "normal"),
                                       ("add", "crust_thin", "normal"), ("add", "tomato_sauce", "light"),
                                       ("add", "cheese", "extra"))),
    ]  # fmt: skip


def test_half_and_half_and_missing_size():
    out = run(
        "halfmoon-pizza", (C, "can i get a pizza half pepperoni half hawaiian"), (C, "and 2 garlic knots")
    )
    assert items(out) == [(("pepperoni_pizza", "hawaiian_pizza"), 1, None, ()), ("garlic_knots", 2, None, ())]
    assert [(m.field.value, m.line_id) for m in out.missing_or_ambiguous][0] == ("item_variant", "L1")
    assert out.clarification_question.startswith("Which pizza would you like (personal 8-inch")


def test_combo_choices_and_contextual_yes():
    out = run(
        "corner-patty",
        (C, "cheeseburger combo with onion rings and a lemonade, pickup, card"),
        (B, "Got it: 1 Cheeseburger Combo. Pickup. Total $12.99. Is that right?"),
        (C, "yep"),
    )
    assert [(c.slot_id, c.menu_item_id) for c in out.items[0].combo_selections] == [("side", "onion_rings"),
                                                                                     ("drink", "lemonade")]  # fmt: skip
    assert out.customer_decision.state.value == "confirmed"


def test_yes_without_a_question_is_not_a_confirmation():
    out = run("corner-patty", (C, "a coke for pickup"), (C, "yes"))
    assert out.customer_decision.state.value == "pending"


def test_change_after_confirmation_resets_it():
    out = run(
        "corner-patty",
        (C, "2 veggie burgers for pickup, card"),
        (B, "2 Veggie Burgers, pickup, $19.98. Is that right?"),
        (C, "yes"),
        (C, "oh wait make one of them no tomato"),
    )
    assert out.customer_decision.state.value == "pending"
    assert items(out)[1] == ("veggie_burger", 1, None, (("remove", "tomato", "normal"),))


def test_cancel_whole_order_keeps_items():
    out = run("corner-patty", (C, "a bacon burger"), (C, "nvm cancel it"))
    assert out.customer_decision.state.value == "cancelled" and len(out.items) == 1
    assert out.missing_or_ambiguous == [] and out.clarification_question is None


def test_delivery_address_payment_claim_and_change():
    out = run(
        "corner-patty",
        (C, "3 bacon burgers delivered to 18 Elm Street apt 3B"),
        (C, "cash, change for a 50"),
        (C, "also i already paid on the app"),
    )
    a = out.address
    assert (a.number, a.street, a.unit) == ("18", "Elm Street", "3B")
    assert out.payment.change_for_cents == 5000 and out.payment.customer_claims_paid
    assert out.fulfillment.requested_time.state.value == "not_mentioned"  # "18 Elm" is not a time


def test_name_and_morning_time_at_the_cafe():
    out = run("morning-crumb", (C, "a large latte w oat milk, pickup at 8:15"), (C, "name's dana, card"))
    assert out.fulfillment.requested_time.normalized_local == "08:15"  # open 7-15: 8:15 pm is impossible
    assert out.customer_name.value == "Dana" and out.missing_or_ambiguous == []


@pytest.mark.parametrize(
    ("text", "expected"), [("at 9pm", "21:00"), ("at 11", "11:00"), ("around 9", "21:00")]
)
def test_time_normalization(text, expected):
    out = run("corner-patty", (C, f"a coke for pickup {text}"))
    assert out.fulfillment.requested_time.normalized_local == expected


def test_ambiguous_clock_time_is_not_normalized():
    menu = MENUS["corner-patty"].model_copy(
        update={"opens_at": MENUS["morning-crumb"].opens_at}
    )  # 07:00-22:00
    convo = conversation((C, "a coke, pickup at 9"))
    out = extract_rules(menu, convo.messages)
    assert out.fulfillment.requested_time.raw_text == "at 9"
    assert out.fulfillment.requested_time.normalized_local is None  # 9 am and 9 pm both open


def test_typos_and_number_words():
    out = run("corner-patty", (C, "two chesburgers and a sprit pls"))
    assert [(i.menu_item_id, i.quantity) for i in out.items] == [("cheeseburger", 2), ("sprite", 1)]


@pytest.mark.parametrize(
    "text",
    ["", "🍔🍔🍔", "???", "asdf qwer", "12345", "a" * 1500, "cancel", "make it 3", "swap it for a coke"],
)
def test_never_crashes_and_always_validates(text):
    msgs = [(C, text)] if text else [(C, "hi")]
    run("corner-patty", *msgs)


# ---- keyword router


def route(*messages: tuple[str, str], has_draft=False, has_placed=False):
    convo = conversation(*messages)
    ctx = RouterContext(convo, len(messages) - 1, has_draft=has_draft, has_placed_order=has_placed)
    provider = KeywordDecisionProvider()
    req = build_router_request(ctx)
    resp = provider.decide(req)
    validate_response(req, resp)
    return parse_router_response(resp).decision


def test_router_protocol():
    assert isinstance(KeywordDecisionProvider(), DecisionProvider)


@pytest.mark.parametrize(
    ("text", "kw", "primary", "secondary"),
    [
        ("hey can i get 2 cheeseburgers and a coke", {}, "PLACE_ORDER", None),
        ("swap the coke for a sprite", {"has_draft": True}, "MODIFY_ORDER", None),
        ("pickup at 7, paying cash", {"has_draft": True}, "PLACE_ORDER", None),
        ("nvm cancel it", {"has_draft": True}, "CANCEL_ORDER", None),
        ("cancel the coke", {"has_draft": True}, "MODIFY_ORDER", None),
        ("do u guys deliver to oak st?", {}, "DELIVERY_QUESTION", None),
        ("do you have veggie burgers?", {}, "MENU_QUESTION", None),
        ("can i pay cash?", {}, "PAYMENT_QUESTION", None),
        ("i already paid", {"has_placed": True}, "PAYMENT_CLAIM", None),
        ("WHERE IS MY FOOD", {"has_placed": True}, "ORDER_STATUS", None),
        ("the bacon was missing, i want a refund", {"has_placed": True}, "ORDER_PROBLEM", "REFUND_REQUEST"),
        ("let me talk to a person", {}, "HUMAN_REQUEST", None),
        ("thanks!", {"has_draft": True}, "SMALL_TALK", None),
        ("are you guys hiring?", {}, "OUT_OF_SCOPE", None),
        ("the thing", {}, "UNKNOWN", None),
    ],
)
def test_router_labels(text, kw, primary, secondary):
    d = route((C, text), **kw)
    assert d.primary.value == primary
    assert (d.secondary.value if d.secondary else None) == secondary


def test_router_contextual_yes():
    asked = route((C, "a coke"), (B, "1 Coke, pickup, $2.49. Is that right?"), (C, "yep"), has_draft=True)
    assert asked.primary is RouterLabel.CONFIRM_ORDER
    not_asked = route((C, "a coke"), (B, "Thanks, coming up."), (C, "yep"), has_draft=True)
    assert not_asked.primary is not RouterLabel.CONFIRM_ORDER


def test_router_urgency_and_flags():
    d = route((C, "where's my food it's been an hour"), has_placed=True)
    assert d.urgency.value == "time_sensitive" and d.flags.refers_to.value == "placed_order"
    d = route((C, "I'M SO ANGRY"), has_placed=True)
    assert d.urgency.value == "normal"  # frustration alone is not urgency
    d = route((C, "my kid is having an allergic reaction, get me a manager please"), has_placed=True)
    assert d.urgency.value == "needs_staff_now" and d.flags.asks_for_human


def test_parse_input_round_trips_render_input():
    convo = conversation((C, "hi\nthere"), (B, "Hello!  What can I get you?"), (C, "2 cokes\n\npls"))
    ctx = RouterContext(convo, 2, has_draft=True, has_placed_order=False)
    parsed = parse_input(render_input(ctx))
    assert parsed.latest == "2 cokes pls" and parsed.has_draft and not parsed.has_placed_order
    assert parsed.earlier == [("customer", "hi there"), ("business", "Hello! What can I get you?")]
