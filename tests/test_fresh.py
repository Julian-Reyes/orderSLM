"""The fresh split (M6): Source A written after the dev-based fixes, to measure them. Evaluation-only."""

import inspect
import json
from collections import Counter

from orderslm.data import cards
from orderslm.data import splits as sp
from orderslm.menus import load_menus
from orderslm.paths import FRESH
from orderslm.schema.conversation import Split
from orderslm.synth import cards as synth_cards
from orderslm.synth import generate, label, run
from orderslm.train import data


def test_fresh_cards_file_matches_the_generator():
    saved = [json.loads(x) for x in (FRESH / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate_fresh()]


def test_fresh_is_half_targeted_half_dev_mix_on_the_training_menus():
    fresh = cards.generate_fresh()
    assert len(fresh) == cards.FRESH_MIX + sum(cards.FRESH_TARGETED.values())
    got = Counter(c.situation for c in fresh)
    assert {n: got[n] for n in cards.FRESH_TARGETED} == cards.FRESH_TARGETED
    assert sum(got[n] for n in cards.SITUATIONS) == cards.FRESH_MIX
    assert not set(cards.FRESH_SITUATIONS) & set(cards.SITUATIONS)
    held_out = {b for b, m in load_menus(include_held_out=True).items() if m.held_out}
    assert not {c.business_id for c in fresh} & held_out
    assert all(c.split is Split.fresh and c.id.startswith("a-fresh-") for c in fresh)


def test_dev_and_test_cards_are_unchanged_by_fresh():
    """Fresh draws from its own RNG; dev's cards file still matches the dev+test generator."""
    saved = [json.loads(x) for x in (sp.split_dir(Split.dev) / cards.CARDS_FILE).read_text().splitlines()]
    assert saved == [c.model_dump(mode="json") for c in cards.generate()[Split.dev]]


def test_training_and_generation_never_read_fresh():
    for module in (synth_cards, generate, label, run, data):
        src = inspect.getsource(module)
        assert "FRESH" not in src and "Split.fresh" not in src and "data/fresh" not in src, module.__name__


def test_fresh_is_an_editable_split_in_its_own_folder():
    assert Split.fresh in sp.EDITABLE and sp.split_dir(Split.fresh) == FRESH


def test_students_can_be_asked_at_every_fresh_customer_message():
    from orderslm.eval import student_dev

    reqs = student_dev.build_requests(Split.fresh)
    fresh = sp.load_split(Split.fresh)
    assert len(reqs) == sum(len(ac.conversation.customer_indices()) for ac in fresh) == 278
    assert all(r["conversation_id"].startswith("a-fresh-") for r in reqs)
    assert student_dev.build_requests()[0]["conversation_id"].startswith("a-dev-")  # dev stays the default
