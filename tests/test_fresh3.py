"""The fresh3 split (M6 v4): Source A written after the v4 fixes (t6, finalize@0.3), which used dev, fresh and fresh2.
Fresh's quotas from its own seed plus a block of orders for another day. Evaluation-only."""

import inspect
import json
from collections import Counter

from orderslm.core.schedule import resolve_schedule
from orderslm.data import cards
from orderslm.data import splits as sp
from orderslm.menus import load_menu, load_menus
from orderslm.paths import FRESH3
from orderslm.schema.conversation import Split
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate, label, run
from orderslm.train import data


def test_fresh3_cards_file_matches_the_generator():
    saved = [json.loads(x) for x in (FRESH3 / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(Split.fresh3)]


def test_fresh3_has_fresh_quotas_plus_a_future_day_block():
    fresh, fresh3 = cards.generate_fresh(), cards.generate_fresh(Split.fresh3)
    want = Counter(c.situation for c in fresh) + Counter({"future_day": cards.FRESH3_FUTURE_DAY})
    assert Counter(c.situation for c in fresh3) == want
    held_out = {b for b, m in load_menus(include_held_out=True).items() if m.held_out}
    assert not {c.business_id for c in fresh3} & held_out
    assert all(c.split is Split.fresh3 and c.id.startswith("a-fresh3-") for c in fresh3)


def test_earlier_fresh_cards_are_unchanged_by_fresh3():
    for split in (Split.fresh, Split.fresh2):
        saved = [json.loads(x) for x in (sp.split_dir(split) / cards.CARDS_FILE).read_text().splitlines()]
        assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(split)]


def test_training_and_generation_never_read_fresh3():
    for module in (synth_cards, generate, label, run, data):
        src = inspect.getsource(module)
        assert "FRESH3" not in src and "Split.fresh3" not in src and "data/fresh3" not in src, module.__name__


def test_every_fresh3_chat_passes_the_annotation_checks_and_follows_its_card():
    fresh3 = sp.load_split(Split.fresh3)
    assert sorted(ac.conversation.id for ac in fresh3) == [c.id for c in cards.load(Split.fresh3)]
    for ac in fresh3:
        assert not [f for f in sp.validate(ac, Split.fresh3) if f.blocking], ac.conversation.id


def test_no_near_duplicates_within_fresh3_or_against_the_other_splits():
    fresh3 = sp.load_split(Split.fresh3)
    assert sp.near_duplicates(fresh3) == []
    for other in (Split.dev, Split.fresh, Split.fresh2):
        assert sp.near_duplicates(fresh3, sp.load_split(other)) == []


def test_every_future_day_gold_resolves_to_a_later_day_the_menus_take():
    for ac in sp.load_split(Split.fresh3):
        g = ac.gold_extraction
        if g is not None and g.fulfillment.requested_time.day is not None:
            r = resolve_schedule(load_menu(ac.conversation.business_id), g, ac.conversation)
            assert r.ok and r.data.days_ahead >= 1, ac.conversation.id


def test_students_can_be_asked_at_every_fresh3_customer_message():
    from orderslm.eval import student_dev

    reqs = student_dev.build_requests(Split.fresh3)
    fresh3 = sp.load_split(Split.fresh3)
    assert len(reqs) == sum(len(ac.conversation.customer_indices()) for ac in fresh3) == 321
    assert all(r["conversation_id"].startswith("a-fresh3-") for r in reqs)
