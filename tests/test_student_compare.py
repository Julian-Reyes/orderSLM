import pytest

from orderslm.eval import student_compare as sc
from orderslm.eval.stats import holm, mcnemar_exact, percentile_interval


def test_mcnemar_exact_matches_hand_computed_values():
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(5, 0) == 2 / 32  # all 5 discordant one way: 2 × (1/2)^5
    assert mcnemar_exact(1, 9) == pytest.approx(2 * 11 / 1024)  # 2 × (C(10,0) + C(10,1)) / 2^10
    assert mcnemar_exact(9, 1) == mcnemar_exact(1, 9)
    assert mcnemar_exact(3, 3) == 1.0


def test_holm_adjusts_in_input_order_and_stays_monotone():
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert holm([0.5]) == [0.5]
    assert holm([0.9, 0.8]) == [1.0, 1.0]  # 0.8 × 2 caps at 1; monotone carries it


def test_percentile_interval():
    assert percentile_interval([float(i) for i in range(101)]) == (2.0, 97.0)


def _run(student, per_chat):
    """per_chat: {chat: (intent oks per message, exact, tp, fp, fn)}; an intent of None = invalid answer."""
    chats, messages = {}, {}
    for cid, (oks, exact, tp, fp, fn) in per_chat.items():
        chats[cid] = {
            "msgs": len(oks),
            "ok": sum(bool(o) for o in oks),
            "invalid": sum(o is None for o in oks),
            "exact": exact,
            "action": exact,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }
        messages |= {(cid, i): bool(o) for i, o in enumerate(oks)}
    return {"student": student, "versions": {"prompt_version": "p"}, "chats": chats, "messages": messages}


CHATS = {f"c{i}": ([True, True], 1, 2, 0, 0) for i in range(8)} | {"c8": ([False, True], 0, 1, 1, 1)}


def test_identical_students_differ_by_nothing():
    c = sc.compare([_run("a", CHATS), _run("b", CHATS)], resamples=200)
    p = c["pairs"][0]
    assert p["intent_messages"] == {"only_a_right": 0, "only_b_right": 0}
    assert p["exact_chats"]["mcnemar_p"] == 1.0
    for m in sc.METRICS:
        assert p["differences"][m]["a_minus_b"] == 0 and p["differences"][m]["ci95"] == [0, 0]


def test_paired_counts_and_signs():
    worse = dict(CHATS) | {"c0": ([None, True], 0, 1, 0, 1), "c1": ([False, True], 0, 2, 0, 0)}
    c = sc.compare([_run("good", CHATS), _run("worse", worse)], resamples=500)
    p = c["pairs"][0]
    assert p["intent_messages"] == {"only_a_right": 2, "only_b_right": 0}
    assert p["exact_chats"] | {} == {
        "only_a_right": 2,
        "only_b_right": 0,
        "mcnemar_p": 0.5,
        "mcnemar_p_holm": 0.5,
    }
    d = p["differences"]
    assert d["intent_accuracy"]["a_minus_b"] == pytest.approx(2 / 18)
    assert d["invalid_rate"]["a_minus_b"] == pytest.approx(-1 / 18)
    assert d["exact_rate"]["a_minus_b"] == pytest.approx(2 / 9)
    lo, hi = d["exact_rate"]["ci95"]
    assert 0 <= lo <= 2 / 9 <= hi  # the better student never loses on a resample of these chats
    assert c["students"]["good"]["item_f1"] == pytest.approx(2 * 17 / (2 * 17 + 1 + 1))


def test_same_seed_same_intervals():
    runs = [_run("a", CHATS), _run("b", dict(CHATS) | {"c0": ([False, False], 0, 0, 0, 2)})]
    assert sc.compare(runs, resamples=300) == sc.compare(runs, resamples=300)


def test_refuses_runs_on_different_messages_or_versions():
    other = dict(CHATS) | {"c9": ([True], 1, 1, 0, 0)}
    with pytest.raises(SystemExit, match="different messages"):
        sc.compare([_run("a", CHATS), _run("b", other)], resamples=10)
    b = _run("b", CHATS) | {"versions": {"prompt_version": "q"}}
    with pytest.raises(SystemExit, match="versions"):
        sc.compare([_run("a", CHATS), b], resamples=10)


def test_training_data_may_differ_but_nothing_else():
    v1 = _run("a", CHATS) | {"versions": {"prompt_version": "p", "data_version": "student-data@0.1"}}
    v2 = _run("b", CHATS) | {"versions": {"prompt_version": "p", "data_version": "student-data@0.2"}}
    assert sc.compare([v1, v2], resamples=10)["pairs"]
    v2["versions"] |= {"prompt_version": "q"}
    with pytest.raises(SystemExit, match="versions"):
        sc.compare([v1, v2], resamples=10)


def test_paused_run_is_refused_not_scored_as_invalid(tmp_path):
    """A paused scoring session leaves messages with no output record; comparing it would count them as
    invalid answers (v3 fresh, 2026-11-10), so the comparison refuses such a run."""
    import json

    import pytest

    from orderslm.eval.student_compare import load_run, unanswered

    messages = {("c1", 0): True, ("c1", 2): False, ("c2", 0): True}
    (tmp_path / "outputs.jsonl").write_text(
        json.dumps({"id": "c1#0", "text": "{}"})
        + "\n"
        + json.dumps({"id": "c1#2", "error": "bad json"})
        + "\n"
    )
    assert unanswered(tmp_path, messages) == ["c2#0"]  # an error record is answered (invalid), not missing
    rows = [
        {"conversation_id": c, "message_index": k, "primary_ok": ok, "pred": None}
        for (c, k), ok in messages.items()
    ]
    (tmp_path / "intent_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (tmp_path / "order_rows.jsonl").write_text("")
    (tmp_path / "metrics.json").write_text("{}")
    (tmp_path / "manifest.json").write_text("{}")
    with pytest.raises(SystemExit, match="incomplete run"):
        load_run(tmp_path)
    with (tmp_path / "outputs.jsonl").open("a") as f:
        f.write(json.dumps({"id": "c2#0", "text": "{}"}) + "\n")
    assert unanswered(tmp_path, messages) == []


def test_parts_split_fresh3_into_standard_and_future_day():
    parts = sc.split_parts("fresh3")
    assert parts is not None and len(parts["standard"]) == 90 and len(parts["future_day"]) == 20
    assert sc.split_parts("dev") is None and sc.split_parts("test") is None  # never opens the sealed split
    worse = dict(CHATS) | {"c0": ([True, True], 0, 1, 0, 1)}
    c = sc.compare(
        [_run("a", CHATS), _run("b", worse)],
        resamples=10,
        parts={"standard": ["c1", "c2"], "future_day": ["c0", "c8"]},
    )
    assert c["parts"]["future_day"]["students"]["a"]["exact_rate"] == 0.5
    assert c["parts"]["future_day"]["students"]["b"]["exact_rate"] == 0.0
    assert c["parts"]["future_day"]["pairs"][0] | {} == {
        "a": "a",
        "b": "b",
        "only_a_right": 1,
        "only_b_right": 0,
        "mcnemar_p": 1.0,
    }
    assert c["parts"]["standard"]["pairs"][0]["only_a_right"] == 0


def test_crashed_scoring_is_refused_not_scored_as_invalid(tmp_path):
    """Session A (2026-11-16): every constrained answer crashed in xgrammar; the records had an error and no text,
    and the report scored them as invalid (0/110 valid). A crash is no answer: the comparison refuses the run."""
    import json

    import pytest

    from orderslm.eval.student_compare import crashed, load_run

    messages = {("c1", 0): True, ("c2", 0): False}
    (tmp_path / "outputs.jsonl").write_text(
        json.dumps({"id": "c1#0", "text": "{}"})
        + "\n"
        + json.dumps({"id": "c2#0", "error": "RuntimeError: GrammarMatcher has terminated"})
        + "\n"
    )
    assert crashed(tmp_path, messages) == ["c2#0"]
    rows = [
        {"conversation_id": c, "message_index": k, "primary_ok": ok, "pred": None}
        for (c, k), ok in messages.items()
    ]
    (tmp_path / "intent_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (tmp_path / "order_rows.jsonl").write_text("")
    (tmp_path / "metrics.json").write_text("{}")
    (tmp_path / "manifest.json").write_text("{}")
    with pytest.raises(SystemExit, match="scoring code crashed on 1 of 2"):
        load_run(tmp_path)
    with (tmp_path / "outputs.jsonl").open("a") as f:  # a resumed session answered it after all
        f.write(json.dumps({"id": "c2#0", "text": "{}"}) + "\n")
    assert crashed(tmp_path, messages) == []


def test_same_name_runs_are_refused_and_constrained_runs_are_labelled(tmp_path, monkeypatch):
    """Plain vs constrained v4 (2026-11-24) both carried `qwen3.5-0.8b-single-v4`: results keyed by name merged
    into one row and every difference printed as +0.0. Same names are refused; a constrained run is labelled."""
    import json

    import pytest

    with pytest.raises(SystemExit, match="share a student name"):
        sc.compare([_run("a", CHATS), _run("a", CHATS)], resamples=10)
    monkeypatch.setattr(sc, "ROOT", tmp_path.parent)
    (tmp_path / "outputs.jsonl").write_text(json.dumps({"id": "c1#0", "text": "{}"}) + "\n")
    (tmp_path / "intent_rows.jsonl").write_text(
        json.dumps({"conversation_id": "c1", "message_index": 0, "primary_ok": True, "pred": "X"}) + "\n"
    )
    (tmp_path / "order_rows.jsonl").write_text(
        json.dumps({"conversation_id": "c1", "exact": True, "action_exact": True, "tp": 1, "fp": 0, "fn": 0})
        + "\n"
    )
    versions = {k: "v" for k in ("prompt_version", "data_version", "scorer_version", "finalize_version")}
    (tmp_path / "metrics.json").write_text(json.dumps({"student": "s"} | versions))
    (tmp_path / "manifest.json").write_text(json.dumps({"generation": {"constrained": {"library": "x"}}}))
    assert sc.load_run(tmp_path)["student"] == "s (constrained)"
    (tmp_path / "manifest.json").write_text(json.dumps({"generation": {}}))
    assert sc.load_run(tmp_path)["student"] == "s"
