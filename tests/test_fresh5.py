"""The fresh5 split (M6 v6): Source A written after the v6 fixes (t8), which used dev, fresh, fresh2 and fresh3 (fresh5
untouched). Fresh5's shape (fresh's quotas + a block of orders for another day) from its own seed. Evaluation-only."""

import inspect
import json
from collections import Counter

from orderslm.core.schedule import resolve_schedule
from orderslm.data import cards
from orderslm.data import splits as sp
from orderslm.menus import load_menu, load_menus
from orderslm.paths import FRESH5
from orderslm.schema.conversation import Split
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate, label, run
from orderslm.train import data


def test_fresh5_cards_file_matches_the_generator():
    saved = [json.loads(x) for x in (FRESH5 / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(Split.fresh5)]


def test_fresh5_has_fresh4s_shape_from_its_own_seed():
    fresh4, fresh5 = cards.generate_fresh(Split.fresh4), cards.generate_fresh(Split.fresh5)
    assert Counter(c.situation for c in fresh5) == Counter(c.situation for c in fresh4)
    assert [c.brief for c in fresh5] != [c.brief for c in fresh4]
    held_out = {b for b, m in load_menus(include_held_out=True).items() if m.held_out}
    assert not {c.business_id for c in fresh5} & held_out
    assert all(c.split is Split.fresh5 and c.id.startswith("a-fresh5-") for c in fresh5)


def test_earlier_fresh_cards_are_unchanged_by_fresh5():
    for split in (Split.fresh, Split.fresh2, Split.fresh3, Split.fresh4):
        saved = [json.loads(x) for x in (sp.split_dir(split) / cards.CARDS_FILE).read_text().splitlines()]
        assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(split)]


def test_training_and_generation_never_read_fresh5():
    for module in (synth_cards, generate, label, run, data):
        src = inspect.getsource(module)
        assert "FRESH5" not in src and "Split.fresh5" not in src and "data/fresh5" not in src, module.__name__


def test_every_fresh5_chat_passes_the_annotation_checks_and_follows_its_card():
    fresh5 = sp.load_split(Split.fresh5)
    assert sorted(ac.conversation.id for ac in fresh5) == [c.id for c in cards.load(Split.fresh5)]
    for ac in fresh5:
        assert not [f for f in sp.validate(ac, Split.fresh5) if f.blocking], ac.conversation.id


def test_no_near_duplicates_within_fresh5_or_against_the_other_splits():
    fresh5 = sp.load_split(Split.fresh5)
    assert sp.near_duplicates(fresh5) == []
    for other in (Split.dev, Split.fresh, Split.fresh2, Split.fresh3, Split.fresh4):
        assert sp.near_duplicates(fresh5, sp.load_split(other)) == []


def test_every_future_day_gold_resolves_to_a_later_day_the_menus_take():
    n = 0
    for ac in sp.load_split(Split.fresh5):
        g = ac.gold_extraction
        if g is not None and g.fulfillment.requested_time.day is not None:
            r = resolve_schedule(load_menu(ac.conversation.business_id), g, ac.conversation)
            assert r.ok and r.data.days_ahead >= 1, ac.conversation.id
            n += 1
    assert n == 20


def test_students_can_be_asked_at_every_fresh5_customer_message():
    from orderslm.eval import student_dev

    reqs = student_dev.build_requests(Split.fresh5)
    fresh5 = sp.load_split(Split.fresh5)
    assert len(reqs) == sum(len(ac.conversation.customer_indices()) for ac in fresh5) == 358
    assert all(r["conversation_id"].startswith("a-fresh5-") for r in reqs)
