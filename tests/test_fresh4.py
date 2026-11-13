"""The fresh4 split (M6 v5): Source A written after the v5 fixes (t7, finalize@0.4), which used dev, fresh, fresh2 and
fresh3. Fresh3's shape (fresh's quotas + a block of orders for another day) from its own seed. Evaluation-only."""

import inspect
import json
from collections import Counter

from orderslm.core.schedule import resolve_schedule
from orderslm.data import cards
from orderslm.data import splits as sp
from orderslm.menus import load_menu, load_menus
from orderslm.paths import FRESH4
from orderslm.schema.conversation import Split
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate, label, run
from orderslm.train import data


def test_fresh4_cards_file_matches_the_generator():
    saved = [json.loads(x) for x in (FRESH4 / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(Split.fresh4)]


def test_fresh4_has_fresh3s_shape_from_its_own_seed():
    fresh3, fresh4 = cards.generate_fresh(Split.fresh3), cards.generate_fresh(Split.fresh4)
    assert Counter(c.situation for c in fresh4) == Counter(c.situation for c in fresh3)
    assert [c.brief for c in fresh4] != [c.brief for c in fresh3]
    held_out = {b for b, m in load_menus(include_held_out=True).items() if m.held_out}
    assert not {c.business_id for c in fresh4} & held_out
    assert all(c.split is Split.fresh4 and c.id.startswith("a-fresh4-") for c in fresh4)


def test_earlier_fresh_cards_are_unchanged_by_fresh4():
    for split in (Split.fresh, Split.fresh2, Split.fresh3):
        saved = [json.loads(x) for x in (sp.split_dir(split) / cards.CARDS_FILE).read_text().splitlines()]
        assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(split)]


def test_training_and_generation_never_read_fresh4():
    for module in (synth_cards, generate, label, run, data):
        src = inspect.getsource(module)
        assert "FRESH4" not in src and "Split.fresh4" not in src and "data/fresh4" not in src, module.__name__


def test_every_fresh4_chat_passes_the_annotation_checks_and_follows_its_card():
    fresh4 = sp.load_split(Split.fresh4)
    assert sorted(ac.conversation.id for ac in fresh4) == [c.id for c in cards.load(Split.fresh4)]
    for ac in fresh4:
        assert not [f for f in sp.validate(ac, Split.fresh4) if f.blocking], ac.conversation.id


def test_no_near_duplicates_within_fresh4_or_against_the_other_splits():
    fresh4 = sp.load_split(Split.fresh4)
    assert sp.near_duplicates(fresh4) == []
    for other in (Split.dev, Split.fresh, Split.fresh2, Split.fresh3):
        assert sp.near_duplicates(fresh4, sp.load_split(other)) == []


def test_every_future_day_gold_resolves_to_a_later_day_the_menus_take():
    n = 0
    for ac in sp.load_split(Split.fresh4):
        g = ac.gold_extraction
        if g is not None and g.fulfillment.requested_time.day is not None:
            r = resolve_schedule(load_menu(ac.conversation.business_id), g, ac.conversation)
            assert r.ok and r.data.days_ahead >= 1, ac.conversation.id
            n += 1
    assert n == 20


def test_students_can_be_asked_at_every_fresh4_customer_message():
    from orderslm.eval import student_dev

    reqs = student_dev.build_requests(Split.fresh4)
    fresh4 = sp.load_split(Split.fresh4)
    assert len(reqs) == sum(len(ac.conversation.customer_indices()) for ac in fresh4) == 343
    assert all(r["conversation_id"].startswith("a-fresh4-") for r in reqs)
