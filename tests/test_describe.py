"""The plain-English gold view (core/describe.py) shows every part of the order, with menu names."""

from orderslm.core.describe import describe_gold
from orderslm.menus import load_menu

from .builders import line, order

CP = load_menu("corner-patty")
HM = load_menu("halfmoon-pizza")


def text(menu, o) -> str:
    return "\n".join(describe_gold(o, menu))


def test_items_options_and_fields():
    o = order(
        line("L1", "cheeseburger", qty=2, variant="double", mods=[("remove", "onion"), ("add", "bacon")]),
        line("L2", "cheeseburger_combo", combo=[("side", "fries", "large"), ("drink", "coke")]),
        method="delivery",
        address="12 Oak St",
        payment="cash",
    )
    t = text(CP, o)
    assert "L1  2 × Cheeseburger, Double patty — no onions; add bacon" in t
    assert "L2  1 × Cheeseburger Combo — side: Fries (Large); drink: Coke" in t
    assert "Delivery" in t and "Address: “12 Oak St”" in t and "Payment: cash" in t
    assert "NOTHING MISSING" in t


def test_missing_requests_and_claims_are_spelled_out():
    pizza = line("L1", "supreme_pizza", variant="large",
                 mods=[{"kind": "add", "modifier_id": None, "raw_text": "artichoke hearts", "not_on_menu": True}])  # fmt: skip
    o = order(
        pizza,
        line("L2", "pepperoni_pizza"),
        method="unknown",
        payment="unknown",
        claims_paid=True,
        missing=[
            ("item_modification", "off_menu", "L1"),
            ("item_variant", "missing", "L2"),
            ("fulfillment_method", "missing"),
        ],
        question="?",
    )
    t = text(HM, o)
    assert "NOT ON THE MENU: “artichoke hearts”" in t
    assert "L2  1 × Pepperoni Pizza, size not stated" in t
    assert "customer SAYS they already paid (a claim, not verified)" in t
    assert "STILL NEEDED BEFORE THE ORDER CAN BE CONFIRMED" in t
    assert "L2: size / flavor (not given)" in t and "pickup or delivery (not given)" in t
