"""Dev/test storage, validation, counts, dedup and the test lock (orderslm.data.splits).

Uses temporary dev/test directories filled from the M0 samples with their split changed;
nothing here touches data/dev or data/test.
"""

import json
import re

import pytest

from orderslm import paths
from orderslm.data import cards, splits
from orderslm.domain.clock import fixed_clock
from orderslm.paths import ROOT, SAMPLES, UNSEAL_ENV, SealedSplitError
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.conversation import Source, Split
from orderslm.schema.extraction import FieldRef, MissingInfo, MissingReason
from orderslm.schema.routing import RouterLabel


def sample(n: int, split: Split, new_id: str | None = None) -> AnnotatedConversation:
    ac = AnnotatedConversation.model_validate_json(
        (SAMPLES / "conversations" / f"sample-{n:03d}.json").read_text()
    )
    conv = ac.conversation.model_copy(update={"split": split, "id": new_id or f"{split.value}-{n:03d}"})
    return ac.model_copy(update={"conversation": conv})


@pytest.fixture
def dirs(tmp_path, monkeypatch):
    dev, test = tmp_path / "dev", tmp_path / "test"
    monkeypatch.setattr(splits, "DEV", dev)
    monkeypatch.setattr(paths, "_TEST", test)
    monkeypatch.setenv(UNSEAL_ENV, "unit test")
    return dev, test


CLOCK = fixed_clock("2026-10-20T15:00:00+00:00")


# ---- validation


def test_samples_relabelled_as_dev_validate_cleanly(dirs):
    for n in range(1, 13):
        assert [f for f in splits.validate(sample(n, Split.dev), Split.dev) if f.blocking] == [], n


def test_wrong_split_is_blocked(dirs):
    codes = [f.code for f in splits.validate(sample(1, Split.dev), Split.test)]
    assert "WRONG_SPLIT" in codes


def test_held_out_menu_only_in_test(dirs):
    ac = sample(1, Split.dev)
    conv = ac.conversation.model_copy(update={"business_id": "lucky-lime"})
    ac = ac.model_copy(update={"conversation": conv})
    assert "HELD_OUT_MENU" in [f.code for f in splits.validate(ac, Split.dev)]


def test_gold_missing_info_must_follow_the_rules(dirs):
    ac = sample(12, Split.dev)
    assert ac.gold_extraction.missing_or_ambiguous == []  # a complete order
    extra = MissingInfo(field=FieldRef.customer_name, reason=MissingReason.missing)
    gold = ac.gold_extraction.model_copy(
        update={"missing_or_ambiguous": [extra], "clarification_question": "Can I get a name?"}
    )
    findings = splits.validate(ac.model_copy(update={"gold_extraction": gold}), Split.dev)
    assert "MISSING_INFO_DIFFERS_FROM_RULES" in [f.code for f in findings]


def test_ungrounded_evidence_is_blocked(dirs):
    ac = sample(12, Split.dev)
    item = ac.gold_extraction.items[0]
    bad = item.model_copy(update={"evidence": [item.evidence[0].model_copy(update={"quote": "not said"})]})
    gold = ac.gold_extraction.model_copy(update={"items": [bad, *ac.gold_extraction.items[1:]]})
    findings = splits.validate(ac.model_copy(update={"gold_extraction": gold}), Split.dev)
    assert "EVIDENCE_NOT_FOUND" in [f.code for f in findings]


def test_schema_errors_are_reported_not_raised():
    ac, findings = splits.parse({"conversation": {}})
    assert ac is None and findings and all(f.code == "SCHEMA" for f in findings)


# ---- storage


def test_save_and_load_round_trip(dirs):
    dev, _ = dirs
    saved = [sample(n, Split.dev) for n in (1, 5, 12)]
    for ac in saved:
        splits.save(ac, Split.dev, clock=CLOCK)
    assert sorted(p.name for p in dev.iterdir()) == ["dev-001.json", "dev-005.json", "dev-012.json"]
    assert splits.load_split(Split.dev) == saved


def test_save_refuses_blocking_findings(dirs):
    with pytest.raises(splits.SplitError, match="WRONG_SPLIT"):
        splits.save(sample(1, Split.dev), Split.test)


def test_test_split_is_sealed_for_reading_and_writing(dirs, monkeypatch):
    monkeypatch.delenv(UNSEAL_ENV)
    with pytest.raises(SealedSplitError):
        splits.load_split(Split.test)
    with pytest.raises(SealedSplitError):
        splits.save(sample(1, Split.test), Split.test)


def test_loading_rejects_a_misfiled_conversation(dirs):
    dev, _ = dirs
    dev.mkdir()
    (dev / "dev-001.json").write_text(splits.dump(sample(1, Split.test, new_id="dev-001")))
    with pytest.raises(splits.SplitError, match="expected dev"):
        splits.load_split(Split.dev)


# ---- counts and dedup


def test_stats_count_labels_scenarios_and_businesses(dirs):
    convs = [sample(n, Split.dev) for n in range(1, 13)]
    s = splits.stats(convs)
    assert s["conversations"] == 12
    assert sum(s["by_business"].values()) == 12
    assert s["customer_messages"] == sum(s["primary_labels"].values())
    assert s["by_scenario"]["half_and_half"] >= 1
    assert s["held_out_menu"] == 0


def test_near_duplicates_within_and_across_splits(dirs):
    a = [sample(1, Split.dev), sample(2, Split.dev)]
    copy = sample(1, Split.test)
    assert splits.near_duplicates(a) == []
    assert splits.near_duplicates([copy], a) == [("test-001", "dev-001", 1.0)]


# ---- the lock


def fill_test(n_range=range(1, 13)) -> None:
    for n in n_range:
        splits.save(sample(n, Split.test), Split.test, clock=CLOCK)


def test_lock_records_hashes_and_counts_and_no_relabel_by_default(dirs):
    _, test = dirs
    fill_test()
    record = splits.lock(clock=CLOCK)
    on_disk = json.loads((test / splits.LOCK_FILE).read_text())
    assert on_disk == record
    assert len(record["files"]) == 12
    assert record["counts"]["test"]["conversations"] == 12
    assert record["counts"]["test"]["by_source"] == {"human": 12}
    assert record["self_consistency"] is None
    assert splits.verify() == []


def test_optional_blind_relabel_is_for_human_written_conversations_only(dirs):
    fill_test()
    record = splits.lock(clock=CLOCK, relabel_human=True)
    sc = record["self_consistency"]
    assert sc["source"] == "human"
    assert sc["ids"] == sorted(sc["ids"]) and len(sc["ids"]) == 12  # min(30, 12)
    assert sc["not_before"] == "2026-10-27" and sc["blind"]
    assert splits.verify() == []


def test_relabel_sample_is_fixed_by_seed(dirs):
    fill_test()
    first = splits.lock(clock=CLOCK, relabel_human=True)["self_consistency"]["ids"]
    (paths._TEST / splits.LOCK_FILE).unlink()
    assert splits.lock(clock=CLOCK, relabel_human=True)["self_consistency"]["ids"] == first


def test_lock_refuses_twice_and_refuses_duplicates_across_splits(dirs):
    fill_test()
    splits.save(sample(3, Split.dev), Split.dev)
    with pytest.raises(splits.SplitError, match="near-duplicate test-003 ~ dev-003"):
        splits.lock(clock=CLOCK)
    (splits.DEV / "dev-003.json").unlink()
    splits.lock(clock=CLOCK)
    with pytest.raises(splits.SplitError, match="already locked"):
        splits.lock(clock=CLOCK)


def test_after_lock_no_new_files_and_changes_need_a_logged_reason(dirs):
    _, test = dirs
    fill_test(range(1, 6))
    splits.lock(clock=CLOCK)
    with pytest.raises(splits.SplitError, match="no new conversations"):
        splits.save(sample(6, Split.test), Split.test)
    changed = sample(1, Split.test).model_copy(update={"annotation_notes": "fixed after review"})
    with pytest.raises(splits.SplitError, match="needs a reason"):
        splits.save(changed, Split.test)
    splits.save(changed, Split.test, change_reason="note added", clock=CLOCK)
    (entry,) = [json.loads(x) for x in (test / splits.CHANGES_FILE).read_text().splitlines()]
    assert entry["id"] == "test-001" and entry["reason"] == "note added"
    assert splits.verify() == []  # logged change


def test_verify_catches_an_unlogged_edit(dirs):
    _, test = dirs
    fill_test(range(1, 4))
    splits.lock(clock=CLOCK)
    p = test / "test-002.json"
    p.write_text(p.read_text().replace('"annotator"', '"annotator" ', 1))
    assert splits.verify() == ["changed without a logged reason: test-002.json"]


# ---- Source A: Claude-written conversations follow a scenario card and are reviewed


def card_for(ac: AnnotatedConversation, split: Split, card_id: str) -> cards.ScenarioCard:
    labels = sorted({r.decision.primary for r in ac.gold_routing})
    return cards.ScenarioCard(
        id=card_id,
        split=split,
        business_id=ac.conversation.business_id,
        situation="simple_order",
        expected_labels=labels,
        scenarios=ac.scenarios,
        style=ac.style,
        features=[],
        fulfillment="delivery",
        customer_messages=len(ac.conversation.customer_indices()),
        persona="test",
        brief="test card",
    )


def source_a(n: int, split: Split) -> tuple[AnnotatedConversation, cards.ScenarioCard]:
    card_id = f"a-{split.value}-{n:03d}"
    ac = sample(n, split, new_id=card_id)
    conv = ac.conversation.model_copy(update={"source": Source.claude_written})
    ac = ac.model_copy(update={"conversation": conv, "card_id": card_id, "annotator": "claude-opus-5-5"})
    return ac, card_for(ac, split, card_id)


def write_source_a(split: Split, numbers) -> list[AnnotatedConversation]:
    pairs = [source_a(n, split) for n in numbers]
    existing = cards.load(split)
    cards.write({split: existing + [c for _, c in pairs]}, force=True)
    for ac, _ in pairs:
        splits.save(ac, split, clock=CLOCK)
    return [ac for ac, _ in pairs]


def test_claude_written_needs_a_card_id():
    ac = sample(1, Split.dev)
    conv = ac.conversation.model_copy(update={"source": Source.claude_written})
    with pytest.raises(ValueError, match="card_id"):
        AnnotatedConversation.model_validate(ac.model_copy(update={"conversation": conv}).model_dump())


def test_source_a_must_follow_its_card(dirs):
    ac, card = source_a(12, Split.dev)
    assert [f.code for f in splits.validate(ac, Split.dev)] == ["UNKNOWN_CARD"]
    cards.write(
        {Split.dev: [card.model_copy(update={"expected_labels": [RouterLabel.CANCEL_ORDER]})]}, force=True
    )
    assert "CARD_LABELS_MISSING" in [f.code for f in splits.validate(ac, Split.dev)]
    cards.write({Split.dev: [card]}, force=True)
    assert [f for f in splits.validate(ac, Split.dev) if f.blocking] == []


def test_reviews_are_logged_with_the_correction_rate(dirs):
    a, b, c = write_source_a(Split.dev, (1, 5, 12))
    splits.review(a, Split.dev, "julian", clock=CLOCK)  # unchanged
    fixed = b.model_copy(update={"annotation_notes": "fixed a label"})
    entry = splits.review(fixed, Split.dev, "julian", clock=CLOCK)
    assert entry["changed"] and entry["reviewer"] == "julian"
    rv = splits.review_stats(Split.dev, splits.load_split(Split.dev))
    assert rv == {
        "source_a": 3,
        "reviewed": 2,
        "reviewed_share": 0.667,
        "corrected": 1,
        "correction_rate": 0.5,
    }
    with pytest.raises(splits.SplitError, match="saved conversation"):
        splits.review(source_a(2, Split.dev)[0], Split.dev, "julian")


def test_lock_needs_all_dev_and_a_quarter_of_test_reviewed(dirs):
    dev = write_source_a(Split.dev, (1, 2))
    test = write_source_a(Split.test, (5, 6, 7, 8, 9))
    with pytest.raises(splits.SplitError, match="dev review incomplete: 0/2"):
        splits.lock(clock=CLOCK)
    for ac in dev:
        splits.review(ac, Split.dev, "julian", clock=CLOCK)
    with pytest.raises(splits.SplitError, match="test spot-check below 25%: 0/5"):
        splits.lock(clock=CLOCK)
    splits.review(test[0], Split.test, "julian", clock=CLOCK)
    splits.review(test[1], Split.test, "julian", clock=CLOCK)
    record = splits.lock(clock=CLOCK)
    assert record["reviews"]["test"]["reviewed"] == 2 and record["reviews"]["dev"]["correction_rate"] == 0.0
    assert record["counts"]["test"]["by_source"] == {"claude_written": 5}


# ---- guards: the sealed split, the held-out menu and the PIZZA benchmark stay out of other code paths

ALLOWED = {  # regex -> the only modules that may contain it
    r"\btest_split_dir\b": {"paths.py", "data/splits.py"},
    r"include_held_out=True": {"menus.py", "data/splits.py", "data/cards.py", "app/main.py"},  # test only
    r"\bUNSEAL_ENV\b": {"paths.py", "data/pizza.py"},
    r"\bload_cases\b": {"data/pizza.py"},
    r"(?<![A-Z_])_TEST\b": {"paths.py"},
}


@pytest.mark.parametrize("pattern", ALLOWED)
def test_only_allowed_modules_reach_sealed_data(pattern):
    src = ROOT / "src" / "orderslm"
    hits = {str(p.relative_to(src)) for p in src.rglob("*.py") if re.search(pattern, p.read_text())}
    assert hits <= ALLOWED[pattern], sorted(hits - ALLOWED[pattern])
