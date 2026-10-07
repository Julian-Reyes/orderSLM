"""PIZZA benchmark conversion (orderslm.data.pizza), on invented orders in PIZZA's file format.

No dataset text is used here: the rows and catalogs below are written for these tests.
"""

import json
import subprocess

import pytest

from orderslm.checks import check_all
from orderslm.data import pizza
from orderslm.data.sexp import parse
from orderslm.paths import ROOT, UNSEAL_ENV, SealedSplitError

CATALOGS = {
    "topping": ["ham\ttopping(HAM)", "onions\ttopping(ONIONS)", "onion\ttopping(ONIONS)", "cheese\ttopping(CHEESE)",
                "olives\ttopping(OLIVES)", "basil\ttopping(BASIL)", "kale\ttopping(KALE)"],
    "number": ["a\tnumber(1)", "one\tnumber(1)", "two\tnumber(2)", "three\tnumber(3)"],
    "size": ["small\tsize(SMALL)", "large\tsize(LARGE)", "medium\tsize(MEDIUM)"],
    "style": ["thin crust\tstyle(THIN_CRUST)", "deep dish\tstyle(DEEP_DISH)", "hawaiian\tstyle(HAWAIIAN)",
              "vegan\tstyle(VEGAN)"],
    "quant_qualifier": ["extra\tquantity(EXTRA)", "light\tquantity(LIGHT)"],
    "drinks": ["cola\tdrinkType(COLA)", "colas\tdrinkType(COLA)", "lime soda\tdrinkType(LIME_SODA)"],
    "drink_volume": ["two liter\tvolume(2,LITER)"],
    "container": ["can\tcontainerType(CAN)", "cans\tcontainerType(CAN)"],
}  # fmt: skip


def row(src: str, exr: str, top: str) -> dict:
    return {"test.SRC": src, "test.EXR": exr, "test.TOP": top, "test.PCFG_ERR": "False"}


ROWS = [
    row(
        "two large pizzas with ham and no onions",
        "(ORDER (PIZZAORDER (NOT (TOPPING ONIONS ) ) (NUMBER 2 ) (SIZE LARGE ) (TOPPING HAM ) ) )",
        "(ORDER (PIZZAORDER (NUMBER two ) (SIZE large ) pizzas with (TOPPING ham ) and no "
        "(NOT (TOPPING onions ) ) ) )",
    ),
    row(  # no number word: EXR has an implicit 1; "loads of" is not in the catalog -> value from EXR
        "large pie with olives and loads of cheese",
        "(ORDER (PIZZAORDER (NUMBER 1 ) (SIZE LARGE ) (COMPLEX_TOPPING (QUANTITY EXTRA ) (TOPPING CHEESE ) ) "
        "(TOPPING OLIVES ) ) )",
        "(ORDER (PIZZAORDER (SIZE large ) pie with (TOPPING olives ) and "
        "(COMPLEX_TOPPING (QUANTITY loads of ) (TOPPING cheese ) ) ) )",
    ),
    row(  # recipe style + negated crust + "no extra cheese" (kept at the default amount)
        "a hawaiian pizza not thin crust and no extra cheese",
        "(ORDER (PIZZAORDER (NOT (STYLE THIN_CRUST ) ) (NOT (COMPLEX_TOPPING (QUANTITY EXTRA ) (TOPPING CHEESE ) ) ) "
        "(NUMBER 1 ) (STYLE HAWAIIAN ) ) )",
        "(ORDER (PIZZAORDER (NUMBER a ) (STYLE hawaiian ) pizza not (NOT (STYLE thin crust ) ) and no "
        "(NOT (COMPLEX_TOPPING (QUANTITY extra ) (TOPPING cheese ) ) ) ) )",
    ),
    row(  # drinks: EXR sorts suborders differently from the utterance
        "three cans of cola and a two liter lime soda",
        "(ORDER (DRINKORDER (DRINKTYPE LIME_SODA ) (NUMBER 1 ) (VOLUME 2 LITER ) ) "
        "(DRINKORDER (CONTAINERTYPE CAN ) (DRINKTYPE COLA ) (NUMBER 3 ) ) )",
        "(ORDER (DRINKORDER (NUMBER three ) (CONTAINERTYPE cans ) of (DRINKTYPE cola ) ) and "
        "(DRINKORDER (NUMBER a ) (VOLUME two liter ) (DRINKTYPE lime soda ) ) )",
    ),
    row(  # two unknown words that could pair either way: ambiguous, reported
        "a pizza with hamm and onyons",
        "(ORDER (PIZZAORDER (NUMBER 1 ) (TOPPING HAM ) (TOPPING ONIONS ) ) )",
        "(ORDER (PIZZAORDER (NUMBER a ) pizza with (TOPPING hamm ) and (TOPPING onyons ) ) )",
    ),
    row(  # the parses disagree (TOP says olives, EXR says basil): reported, never guessed
        "one small pizza with olives",
        "(ORDER (PIZZAORDER (NUMBER 1 ) (SIZE SMALL ) (TOPPING BASIL ) ) )",
        "(ORDER (PIZZAORDER (NUMBER one ) (SIZE small ) pizza with (TOPPING olives ) ) )",
    ),
]


@pytest.fixture
def root(tmp_path):
    (tmp_path / "catalogs").mkdir()
    for name, lines in CATALOGS.items():
        (tmp_path / "catalogs" / f"{name}.txt").write_text("\n".join(lines) + "\n")
    (tmp_path / "PIZZA_test.json").write_text("".join(json.dumps(r) + "\n" for r in ROWS))
    return tmp_path


@pytest.fixture
def built(root):
    report = pizza.build(root=root, n=len(ROWS))
    menu = pizza.MenuCatalog.model_validate_json((root / "benchmark" / "pizza-benchmark.json").read_text())
    lines = (root / "benchmark" / "cases.jsonl").read_text().splitlines()
    cases = {c.source_index: c for c in map(pizza.PizzaCase.model_validate_json, lines)}
    return report, menu, cases


def items(case):
    return [
        (
            i.quantity,
            i.menu_item_id,
            i.variant_id,
            [(m.kind.value, m.modifier_id, m.amount.value, m.raw_text) for m in i.modifications],
            i.evidence[0].quote,
        )
        for i in case.gold_extraction.items
    ]


# ---- reader


def test_sexp_reader_keeps_words_and_nesting():
    tree = parse("(ORDER i want (PIZZAORDER (NUMBER a ) pizza ) )")
    assert tree.label == "ORDER" and tree.text() == "i want a pizza"
    (sub,) = tree.nodes("PIZZAORDER")
    assert sub.nodes("NUMBER")[0].text() == "a"


@pytest.mark.parametrize("bad", ["", "ORDER x", "(ORDER (X a )", "(ORDER a ) )", "(A ) (B )", "( )"])
def test_sexp_reader_rejects_malformed_parses(bad):
    with pytest.raises(ValueError):
        parse(bad)


# ---- sampling


def test_sample_is_fixed_by_seed_and_never_filtered():
    a = pizza.sample_indices(1357, 200, seed=pizza.SEED)
    assert a == pizza.sample_indices(1357, 200, seed=pizza.SEED)
    assert a != pizza.sample_indices(1357, 200, seed=pizza.SEED + 1)
    assert len(a) == len(set(a)) == 200 and a == sorted(a)


def test_every_sampled_order_is_converted_or_reported(built):
    report, _, cases = built
    assert report["sampled"] == len(ROWS)
    failed = {f["index"]: f["reason"] for f in report["failures"]}
    assert set(cases) | set(failed) == set(range(len(ROWS))) and not set(cases) & set(failed)
    assert "more than one way" in failed[4]
    assert "disagree" in failed[5]


# ---- conversion


def test_toppings_sizes_negation(built):
    _, _, cases = built
    assert items(cases[0]) == [
        (2, "pizza", "large", [("add", "ham", "normal", "ham"), ("remove", "onions", "normal", "onions")],
         "two large pizzas with ham and no onions"),
    ]  # fmt: skip


def test_implicit_quantity_and_unknown_word_take_values_from_exr(built):
    report, _, cases = built
    assert items(cases[1]) == [
        (1, "pizza", "large", [("add", "olives", "normal", "olives"), ("add", "cheese", "extra", "loads of cheese")],
         "large pie with olives and loads of cheese"),
    ]  # fmt: skip
    assert report["top_words_filled_from_exr"] == {1: 1}  # row 4 failed, so it is not counted


def test_recipe_style_negated_crust_and_no_extra(built):
    _, _, cases = built
    assert items(cases[2]) == [
        (1, "hawaiian_pizza", None, [("remove", "thin_crust", "normal", "thin crust")],
         "a hawaiian pizza not thin crust and no extra cheese"),
    ]  # fmt: skip
    assert cases[2].dropped_negated_amounts == 1


def test_drinks_keep_utterance_order_and_every_attribute(built):
    _, _, cases = built
    assert items(cases[3]) == [
        (3, "cola", "can", [], "three cans of cola"),
        (1, "lime_soda", "2_liter", [], "a two liter lime soda"),
    ]


def test_gold_passes_every_check_and_asks_for_what_pizza_never_states(built):
    _, menu, cases = built
    for case in cases.values():
        assert check_all(case.gold_extraction, case.conversation, menu) == []
        assert case.conversation.split.value == "benchmark"
        fields = [m.field.value for m in case.gold_extraction.missing_or_ambiguous]
        assert {"fulfillment_method", "payment_method"} <= set(fields)
        assert case.gold_extraction.clarification_question
    assert "item_variant" in [m.field.value for m in cases[2].gold_extraction.missing_or_ambiguous]


# ---- the benchmark catalog


def test_catalog_has_what_the_sample_uses_plus_distractors(built):
    report, menu, _ = built
    mods = {m.id for m in menu.modifiers if m.group == "topping"}
    assert {"ham", "onions", "olives", "cheese"} <= mods  # used by converted orders
    assert mods <= {"ham", "onions", "olives", "cheese", "basil", "kale"}
    e = report["entities"]["toppings"]
    assert e["menu"] == len(mods) == e["used"] + e["distractors"]
    assert {m.id for m in menu.modifiers if m.group == "crust"} == {"thin_crust", "deep_dish"}  # padded
    assert {"pizza", "hawaiian_pizza", "vegan_pizza"} <= {i.id for i in menu.items}
    cola = menu.item("cola")
    assert cola.default_variant_id == "regular" and {"can", "2_liter"} <= {v.id for v in cola.variants}
    assert all(i.default_variant_id is None for i in menu.items if i.category == "pizzas")


def test_build_is_reproducible(root):
    first = pizza.build(root=root, n=len(ROWS))
    menu_a = (root / "benchmark" / "pizza-benchmark.json").read_text()
    assert pizza.build(root=root, n=len(ROWS)) == first
    assert (root / "benchmark" / "pizza-benchmark.json").read_text() == menu_a


# ---- sealing and licensing


def test_benchmark_cases_are_evaluation_only(built, root, monkeypatch):
    monkeypatch.delenv(UNSEAL_ENV, raising=False)
    with pytest.raises(SealedSplitError):
        pizza.load_cases(root)
    monkeypatch.setenv(UNSEAL_ENV, "test")
    menu, cases = pizza.load_cases(root)
    assert menu.business_id == "pizza-benchmark" and len(cases) == len(built[2])


def test_benchmark_writes_only_under_data_external():
    assert pizza.PIZZA_DIR.is_relative_to(ROOT / "data" / "external")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert not [f for f in tracked.split() if "pizza-benchmark" in f or f.startswith("data/external")]


def test_downloads_are_pinned_to_a_commit():
    assert len(pizza.COMMIT) == 40 and "main" not in pizza.COMMIT
