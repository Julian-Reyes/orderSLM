"""Training data v3 (t5): targeted cards and labels written by hand only (no teacher call)."""

import json
from collections import Counter

from orderslm.synth import run
from orderslm.synth.cards import V3_MODIFY_KIND_WEIGHTS, V3_WEIGHTS, plan_targeted_cards


def _plan(n=300):
    return plan_targeted_cards(
        n,
        seed=7,
        batch="tv3",
        generators=((run.HAND_WRITER, 1),),
        weights=V3_WEIGHTS,
        modify_weights=V3_MODIFY_KIND_WEIGHTS,
    )


def test_v3_plan_has_the_exact_target_counts_and_is_reproducible():
    cards = _plan()
    assert Counter(c.extras[-1].removeprefix("target:") for c in cards) == Counter(V3_WEIGHTS)
    assert [c.model_dump() for c in cards] == [c.model_dump() for c in _plan()]


def test_v3_targets_shape_the_cards():
    cards = _plan()
    for c in cards:
        t = c.extras[-1].removeprefix("target:")
        if t == "opener_only":
            assert c.items == [] and c.customer_messages <= 2 and "without naming any item" in c.brief
        if t == "milk_choice":
            assert c.business_id == "morning-crumb"
        if t in ("qty_unstated", "vague_ref", "unit_size"):
            assert c.brief.count(".") >= 2  # the target sentence was appended to the scenario brief


def test_hand_only_label_needs_no_teacher_record(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "batch_dir", lambda batch: tmp_path)
    (tmp_path / "label_fixes").mkdir()
    label = {"schema_version": "label@0.1", "intents": [], "order": {}}
    (tmp_path / "label_fixes" / "c1.json").write_text(
        json.dumps({"kind": "hand_label", "label": label, "label_prompt_version": run.HAND_LABEL_VERSION})
    )
    text, version, fix = run.label_record("tv3", "c1")
    assert json.loads(text) == label and version == run.HAND_LABEL_VERSION and fix["kind"] == "hand_label"
