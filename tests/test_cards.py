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


RARE = {
    RouterLabel.HUMAN_REQUEST,
    RouterLabel.ORDER_PROBLEM,
    RouterLabel.ORDER_STATUS,
    RouterLabel.PAYMENT_CLAIM,
    RouterLabel.OUT_OF_SCOPE,
    RouterLabel.REFUND_REQUEST,
    RouterLabel.UNKNOWN,
}


def test_split_sizes(generated):
    assert len(generated[Split.dev]) == 91  # 80 + supplement 11
    assert len(generated[Split.test]) == 199  # 170 + supplement 29
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
    for name in cards.SITUATIONS:
        assert sum(c.situation == name for c in cs) == cards.quota(name, split), name


@pytest.mark.parametrize(("split", "minimum"), [(Split.dev, 3), (Split.test, 7)])
def test_rare_labels_have_enough_cards(generated, split, minimum):
    labels = [lab for c in generated[split] for lab in c.expected_labels]
    for lab in RARE:
        assert labels.count(lab) >= minimum, lab


@pytest.mark.parametrize(("split", "menus"), [(Split.dev, 3), (Split.test, 4)])
def test_implicit_category_cards_spread_across_menus(generated, split, menus):
    implicit = [c for c in generated[split] if c.situation == "implicit_category"]
    assert all(Scenario.implicit_category in c.scenarios for c in implicit)
    assert len({c.business_id for c in implicit}) == menus


def test_held_out_menu_is_about_a_quarter_of_test(generated):
    test = generated[Split.test]
    share = sum(c.business_id == "lucky-lime" for c in test) / len(test)
    assert 0.23 <= share <= 0.27


def test_supplement_appends_without_changing_earlier_cards(generated):
    """The second batch has its own RNG stream: the first-batch cards are exactly what a generator
    without the supplement produces, so reviewed cards never change."""
    original = dict(cards.SUPPLEMENT)
    try:
        cards.SUPPLEMENT.clear()
        first = cards.generate()
    finally:
        cards.SUPPLEMENT.update(original)
    for split, cs in first.items():
        assert generated[split][: len(cs)] == cs
        assert [c.id for c in generated[split]] == [
            f"a-{split.value}-{n:03d}" for n in range(1, len(generated[split]) + 1)
        ]


def test_committed_dev_cards_match_the_generator(generated):
    assert cards.load(Split.dev) == generated[Split.dev]


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
    assert s["cards"] == 91 and sum(s["menus"].values()) == 91 and sum(s["styles"].values()) == 91
