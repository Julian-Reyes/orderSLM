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
