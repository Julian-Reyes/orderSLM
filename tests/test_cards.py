"""Scenario cards for Source A: coverage by construction, constraints, reproducibility."""

import pytest

from orderslm.data import cards
from orderslm.menus import load_menus
from orderslm.schema.annotation import Scenario, WritingStyle
from orderslm.schema.conversation import Split
from orderslm.schema.routing import RouterLabel

TRICKY = {
    Scenario.two_requests,
    Scenario.correction,
    Scenario.correction_after_confirmation,
    Scenario.ambiguous_reference,
    Scenario.off_menu,
    Scenario.missing_info,
    Scenario.contextual_yes,
}


@pytest.fixture(scope="module")
def generated():
    return cards.generate()


def test_split_sizes(generated):
    assert len(generated[Split.dev]) == 80
    assert len(generated[Split.test]) == 170
    ids = [c.id for split in generated.values() for c in split]
    assert len(ids) == len(set(ids))
    assert all(c.split is split for split, cs in generated.items() for c in cs)


@pytest.mark.parametrize("split", [Split.dev, Split.test])
def test_every_router_label_style_feature_and_tricky_case_in_each_split(generated, split):
    cs = generated[split]
    labels = {lab for c in cs for lab in c.expected_labels}
    assert labels == set(RouterLabel)
    assert {c.style for c in cs} == set(WritingStyle)
    assert {f for c in cs for f in c.features} == set(cards.Feature)
    assert TRICKY <= {s for c in cs for s in c.scenarios}
    for name, sit in cards.SITUATIONS.items():
        assert sum(c.situation == name for c in cs) == sit.counts[split is Split.test], name


def test_menus_held_out_only_in_test(generated):
    menus = load_menus(include_held_out=True)
    business = sorted(b for b, m in menus.items() if not m.held_out)
    assert sorted({c.business_id for c in generated[Split.dev]}) == business
    assert sorted({c.business_id for c in generated[Split.test]}) == sorted(menus)


def test_situation_constraints(generated):
    menus = load_menus(include_held_out=True)
    for c in (c for cs in generated.values() for c in cs):
        if c.situation == "half_and_half":
            assert c.business_id == "halfmoon-pizza"
        if c.situation == "combo":
            assert any(i.combo_slots for i in menus[c.business_id].items)
        if c.fulfillment == "delivery":
            assert menus[c.business_id].delivery.available, c.id
        if not cards.SITUATIONS[c.situation].order:
            assert c.fulfillment == "not_applicable"


def test_generation_is_reproducible(generated):
    assert cards.generate() == generated
    assert cards.generate(seed=cards.SEED + 1) != generated


def test_summary_counts(generated):
    s = cards.summary(generated[Split.dev])
    assert s["cards"] == 80 and sum(s["menus"].values()) == 80 and sum(s["styles"].values()) == 80
