"""Dev/test storage, validation, counts, dedup and the test lock (orderslm.data.splits).

Uses temporary dev/test directories filled from the M0 samples with their split changed;
nothing here touches data/dev or data/test.
"""

import json
import re

import pytest

from orderslm import paths
from orderslm.data import splits
from orderslm.domain.clock import fixed_clock
from orderslm.paths import ROOT, SAMPLES, UNSEAL_ENV, SealedSplitError
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.conversation import Split
from orderslm.schema.extraction import FieldRef, MissingInfo, MissingReason


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


def test_lock_records_hashes_counts_and_schedules_the_blind_relabel(dirs):
    _, test = dirs
    fill_test()
    record = splits.lock(clock=CLOCK)
    on_disk = json.loads((test / splits.LOCK_FILE).read_text())
    assert on_disk == record
    assert len(record["files"]) == 12
    assert record["counts"]["test"]["conversations"] == 12
    sc = record["self_consistency"]
    assert sc["ids"] == sorted(sc["ids"]) and len(sc["ids"]) == 12  # min(30, 12)
    assert sc["not_before"] == "2026-10-27" and sc["blind"]
    assert splits.verify() == []


def test_relabel_sample_is_fixed_by_seed(dirs):
    fill_test()
    first = splits.lock(clock=CLOCK)["self_consistency"]["ids"]
    (paths._TEST / splits.LOCK_FILE).unlink()
    assert splits.lock(clock=CLOCK)["self_consistency"]["ids"] == first


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


# ---- guards: the sealed split, the held-out menu and the PIZZA benchmark stay out of other code paths

ALLOWED = {  # regex -> the only modules that may contain it
    r"\btest_split_dir\b": {"paths.py", "data/splits.py"},
    r"include_held_out=True": {"menus.py", "data/splits.py", "app/main.py"},  # app: test split only
    r"\bUNSEAL_ENV\b": {"paths.py", "data/pizza.py"},
    r"\bload_cases\b": {"data/pizza.py"},
    r"(?<![A-Z_])_TEST\b": {"paths.py"},
}


@pytest.mark.parametrize("pattern", ALLOWED)
def test_only_allowed_modules_reach_sealed_data(pattern):
    src = ROOT / "src" / "orderslm"
    hits = {str(p.relative_to(src)) for p in src.rglob("*.py") if re.search(pattern, p.read_text())}
    assert hits <= ALLOWED[pattern], sorted(hits - ALLOWED[pattern])
