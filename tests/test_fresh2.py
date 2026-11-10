"""The fresh2 split (M6 v3): Source A written after the v3 fixes that used fresh, to measure them. Evaluation-only."""

import inspect
import json
from collections import Counter

from orderslm.data import cards
from orderslm.data import splits as sp
from orderslm.menus import load_menus
from orderslm.paths import FRESH2
from orderslm.schema.conversation import Split
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate, label, run
from orderslm.train import data


def test_fresh2_cards_file_matches_the_generator():
    saved = [json.loads(x) for x in (FRESH2 / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh(Split.fresh2)]


def test_fresh2_has_fresh_quotas_from_its_own_seed():
    fresh, fresh2 = cards.generate_fresh(), cards.generate_fresh(Split.fresh2)
    assert Counter(c.situation for c in fresh2) == Counter(c.situation for c in fresh)
    assert [c.model_dump(exclude={"id", "split"}) for c in fresh2] != [
        c.model_dump(exclude={"id", "split"}) for c in fresh
    ]
    held_out = {b for b, m in load_menus(include_held_out=True).items() if m.held_out}
    assert not {c.business_id for c in fresh2} & held_out
    assert all(c.split is Split.fresh2 and c.id.startswith("a-fresh2-") for c in fresh2)


def test_fresh_cards_are_unchanged_by_fresh2():
    saved = [json.loads(x) for x in (sp.split_dir(Split.fresh) / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh()]


def test_training_and_generation_never_read_fresh2():
    for module in (synth_cards, generate, label, run, data):
        src = inspect.getsource(module)
        assert "FRESH2" not in src and "Split.fresh2" not in src and "data/fresh2" not in src, module.__name__


def test_fresh2_is_an_editable_split_in_its_own_folder():
    assert Split.fresh2 in sp.EDITABLE and sp.split_dir(Split.fresh2) == FRESH2


def test_every_fresh2_chat_passes_the_annotation_checks_and_follows_its_card():
    fresh2 = sp.load_split(Split.fresh2)
    assert sorted(ac.conversation.id for ac in fresh2) == [c.id for c in cards.load(Split.fresh2)]
    for ac in fresh2:
        assert not [f for f in sp.validate(ac, Split.fresh2) if f.blocking], ac.conversation.id


def test_no_near_duplicates_within_fresh2_or_against_dev_and_fresh():
    fresh2 = sp.load_split(Split.fresh2)
    assert sp.near_duplicates(fresh2) == []
    assert sp.near_duplicates(fresh2, sp.load_split(Split.dev)) == []
    assert sp.near_duplicates(fresh2, sp.load_split(Split.fresh)) == []


def test_students_can_be_asked_at_every_fresh2_customer_message():
    from orderslm.eval import student_dev

    reqs = student_dev.build_requests(Split.fresh2)
    fresh2 = sp.load_split(Split.fresh2)
    assert len(reqs) == sum(len(ac.conversation.customer_indices()) for ac in fresh2) == 275
    assert all(r["conversation_id"].startswith("a-fresh2-") for r in reqs)
