"""Planted mistakes (core/plant.py): deterministic, one mistake per copy, every copy a valid contract."""

from orderslm.core.plant import Mistake, plant
from orderslm.eval.dataset import load_eval_split
from orderslm.eval.metrics import item_key
from orderslm.menus import load_menu
from orderslm.schema.conversation import Split

DEV = [ac for ac in load_eval_split(Split.dev) if ac.gold_extraction is not None]


def _keys(o):
    return sorted(repr(item_key(i)) for i in o.items)


def test_planting_is_deterministic_and_changes_exactly_the_planted_thing():
    seen = set()
    for ac in DEV:
        gold, menu = ac.gold_extraction, load_menu(ac.conversation.business_id)
        copies = plant(gold, menu, seed=ac.conversation.id)
        assert copies == plant(gold, menu, seed=ac.conversation.id)
        for mistake, copy in copies.items():
            seen.add(mistake)
            assert copy != gold
            if mistake in (Mistake.fulfillment_flip, Mistake.wrong_payment):
                assert _keys(copy) == _keys(gold)  # items untouched
                field = "fulfillment" if mistake is Mistake.fulfillment_flip else "payment"
                assert getattr(copy, field).method != getattr(gold, field).method
            else:
                assert _keys(copy) != _keys(gold), (ac.conversation.id, mistake)
                assert copy.fulfillment == gold.fulfillment and copy.payment == gold.payment
            if mistake is Mistake.missing_item:
                assert len(copy.items) == len(gold.items) - 1
            if mistake is Mistake.extra_item:
                assert len(copy.items) == len(gold.items) + 1
    assert seen == set(Mistake)  # every type occurs on dev


def test_different_seeds_can_plant_differently():
    ac = max(DEV, key=lambda a: len(a.gold_extraction.items))
    menu = load_menu(ac.conversation.business_id)
    a = plant(ac.gold_extraction, menu, seed="one")
    b = plant(ac.gold_extraction, menu, seed="two")
    assert set(a) == set(b) and a != b


def test_scorer_handles_modifications_without_menu_ids():
    from orderslm.schema.extraction import Modification

    ac = DEV[0]
    line = ac.gold_extraction.items[0]
    mods = [
        Modification(kind="add", modifier_id=None, raw_text="artichoke", not_on_menu=True),
        Modification(kind="add", modifier_id="bacon", raw_text="bacon"),
    ]
    assert item_key(line.model_copy(update={"modifications": mods})) == item_key(
        line.model_copy(update={"modifications": mods[::-1]})
    )
