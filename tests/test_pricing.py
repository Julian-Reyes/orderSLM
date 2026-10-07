"""Deterministic pricing. Every expected amount is worked out by hand from the menu JSON in the comment beside it."""

import pytest

from orderslm.core.pricing import PRICING_VERSION, DeterministicPricing
from orderslm.interfaces.tools import PricingEngine
from orderslm.menus import load_menu, menu_version
from orderslm.schema.order import ToolErr, ToolOk

from .builders import line, order

P = DeterministicPricing()
CP = load_menu("corner-patty")
HM = load_menu("halfmoon-pizza")
MC = load_menu("morning-crumb")


def total(menu, proposal) -> int:
    r = P.quote(menu, proposal)
    assert isinstance(r, ToolOk), r
    return r.data.total_cents


def codes(menu, proposal) -> list[str]:
    r = P.quote(menu, proposal)
    assert isinstance(r, ToolErr), r
    return [i["code"] for i in r.error.details["issues"]]


def test_implements_the_pricing_engine_protocol():
    assert isinstance(P, PricingEngine)


def test_spec_example_order():
    # 2 cheeseburgers (one no onions) 899 + 899, sprite 249 = 2047
    o = order(
        line("L1", "cheeseburger"),
        line("L2", "cheeseburger", mods=[("remove", "onion")]),
        line("L3", "sprite"),
    )
    r = P.quote(CP, o)
    assert isinstance(r, ToolOk)
    q = r.data
    assert (q.subtotal_cents, q.delivery_fee_cents, q.total_cents) == (2047, 0, 2047)
    assert q.verified_by == PRICING_VERSION and q.menu_version == menu_version(CP)
    assert [ln.line_id for ln in q.lines] == ["L1", "L2", "L3"]


def test_quantity_and_variant_delta():
    # double cheeseburger 899 + 300 = 1199, x3 = 3597
    assert total(CP, order(line("L1", "cheeseburger", qty=3, variant="double"))) == 3597


def test_default_variant_applies_when_unstated():
    # fries default regular: 349; stated large: 349 + 150
    assert total(CP, order(line("L1", "fries"))) == 349
    assert total(CP, order(line("L1", "fries", variant="large"))) == 499


def test_required_variant_is_never_guessed():
    assert codes(CP, order(line("L1", "milkshake"))) == ["MISSING_VARIANT"]
    assert codes(HM, order(line("L1", "pepperoni_pizza"))) == ["MISSING_VARIANT"]  # pizza size must be stated


@pytest.mark.parametrize(
    ("mods", "expected"),
    [
        ([("remove", "onion")], 899),  # removing is free
        ([("add", "bacon")], 899 + 200),  # add-on
        ([("add", "bacon", "extra")], 899 + 2 * 200),  # extra of something not included = two portions
        ([("add", "cheese", "extra")], 899 + 100),  # extra of an included ingredient = one more portion
        ([("add", "cheese", "light")], 899),  # light on an included ingredient is free
        ([("add", "cheese")], 899),  # "with cheese" on a cheeseburger: already included
        ([("add", None)], 899),  # off-menu request ("extra crispy"): a note, not priced
    ],
)
def test_modifier_pricing(mods, expected):
    assert total(CP, order(line("L1", "cheeseburger", mods=mods))) == expected


def test_substitution_charges_the_replacement():
    # large latte 475 + 75; whole milk -> oat milk (+70, not included) = 620
    o = order(line("L1", "latte", variant="large", mods=[("substitute", "whole_milk", "normal", "oat_milk")]))
    assert total(MC, o) == 620


def test_extra_ingredient_amount_from_pizza_dataset_style_order():
    # medium pepperoni 1449; thin crust 0; light sauce 0; extra cheese (included) 175 = 1624
    o = order(
        line(
            "L1",
            "pepperoni_pizza",
            variant="medium",
            mods=[("add", "crust_thin"), ("add", "tomato_sauce", "light"), ("add", "cheese", "extra")],
        )
    )
    assert total(HM, o) == 1624


def test_half_and_half_costs_the_dearer_half_plus_half_priced_toppings():
    # large: pepperoni 1449+400 = 1849, hawaiian 1499+400 = 1899 -> 1899
    o = order(line("L1", halves=["pepperoni_pizza", "hawaiian_pizza"], variant="large"))
    assert total(HM, o) == 1899
    # + mushrooms on one half: 150 / 2 = 75; + anchovies on the other: 250 / 2 = 125
    halves = [
        {
            "menu_item_id": "pepperoni_pizza",
            "modifications": [line("x", mods=[("add", "mushrooms")])["modifications"][0]],
        },
        {
            "menu_item_id": "cheese_pizza",
            "modifications": [line("x", mods=[("add", "anchovies")])["modifications"][0]],
        },
    ]
    assert total(HM, order(line("L1", halves=halves, variant="large"))) == 1849 + 75 + 125
    r = P.quote(HM, order(line("L1", halves=halves, variant="large")))
    assert r.data.lines[0].half_menu_item_ids == ["pepperoni_pizza", "cheese_pizza"]


def test_half_topping_rounds_up_to_the_cent():
    # an odd-priced topping on a half: 75 (sauce) / 2 = 37.5 -> 38
    sauce = line("x", mods=[("add", "bbq_sauce")])["modifications"][0]
    halves = [{"menu_item_id": "cheese_pizza", "modifications": [sauce]}, {"menu_item_id": "cheese_pizza"}]
    assert total(HM, order(line("L1", halves=halves, variant="medium"))) == 1199 + 38


def test_combo_choices_are_included():
    # cheeseburger combo 1299 with onion rings + lemonade (both included)
    o = order(line("L1", "cheeseburger_combo", combo=[("side", "onion_rings"), ("drink", "lemonade")]))
    assert total(CP, o) == 1299


def test_combo_needs_every_choice():
    o = order(line("L1", "cheeseburger_combo", combo=[("side", "fries")]))
    assert codes(CP, o) == ["MISSING_COMBO_CHOICE"]


def test_combo_choice_upsizing_costs_the_size_difference():
    # coffee & pastry 650; large latte +75; plain croissant (default) +0 = 725
    o = order(line("L1", "coffee_pastry_combo", combo=[("drink", "latte", "large"), ("pastry", "croissant")]))
    assert total(MC, o) == 725
    # a latte has no default size: the combo's drink choice still needs one
    o = order(line("L1", "coffee_pastry_combo", combo=[("drink", "latte"), ("pastry", "croissant")]))
    assert codes(MC, o) == ["MISSING_VARIANT"]


def test_delivery_fee_and_minimum():
    # 2 cheeseburgers 1798 >= 1500 minimum, + 399 fee = 2197
    assert total(CP, order(line("L1", "cheeseburger", qty=2), method="delivery", address="1 Main St")) == 2197
    r = P.quote(CP, order(line("L1", "cheeseburger"), method="delivery", address="1 Main St"))
    assert isinstance(r, ToolErr) and r.error.code == "BELOW_DELIVERY_MINIMUM"
    assert r.error.details["subtotal_cents"] == 899 and r.error.details["min_order_cents"] == 1500


def test_no_fee_when_method_unknown():
    assert total(CP, order(line("L1", "cheeseburger", qty=2), method="unknown")) == 1798


def test_delivery_from_a_pickup_only_business():
    r = P.quote(MC, order(line("L1", "drip_coffee"), method="delivery", address="1 Main St"))
    assert isinstance(r, ToolErr) and r.error.code == "DELIVERY_UNAVAILABLE"


def test_unavailable_item():
    menu = CP.model_copy(deep=True)
    menu.item("onion_rings").available = False
    assert codes(menu, order(line("L1", "onion_rings"))) == ["UNAVAILABLE"]


def test_things_that_cannot_be_priced_are_all_reported():
    o = order(
        line("L1", unmatched="chicken sandwich", qty=2),
        line("L2", "cheeseburger", qty=None),
        line("L3", "milkshake"),
        line("L4", "tacos_al_pastor"),
        missing=[("item_menu_match", "off_menu", "L1"), ("item_quantity", "ambiguous", "L2")],
        question="?",
    )
    assert sorted(codes(CP, o)) == sorted(
        ["UNMATCHED_ITEM", "UNCLEAR_QUANTITY", "MISSING_VARIANT", "UNKNOWN_ITEM"]
    )


def test_empty_order():
    assert codes(CP, order()) == ["NO_ITEMS"]


def test_two_crusts_is_an_error_not_a_guess():
    o = order(
        line("L1", "cheese_pizza", variant="medium", mods=[("add", "crust_thin"), ("add", "crust_stuffed")])
    )
    assert codes(HM, o) == ["EXCLUSIVE_GROUP_CONFLICT"]


def test_modifier_not_allowed_on_item():
    assert codes(CP, order(line("L1", "coke", mods=[("add", "bacon")]))) == ["MODIFIER_NOT_ALLOWED"]
