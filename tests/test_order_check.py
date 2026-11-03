"""Order checker pilot: which orders are checked and what the checker sees (no network)."""

from orderslm.eval import order_check
from orderslm.eval.label_audit import ORDER_PROMPT


def test_checks_only_the_students_real_mistakes():
    jobs = {j["id"]: j for j in order_check.wrong_orders()}
    # dev 016 and 038 are wrong only in wording (same action as gold), so they are not checked
    assert "dev__a-dev-016" not in jobs and "dev__a-dev-038" not in jobs
    assert "fresh__a-fresh-051" in jobs  # "actually drop the muffin" ignored
    assert jobs["fresh__a-fresh-034"]["kinds"] == ["broken_answer"]
    assert all(j["kinds"] for j in jobs.values())


def test_the_checker_gets_the_audit_question_and_the_recorded_order():
    job = next(j for j in order_check.wrong_orders() if j["id"] == "fresh__a-fresh-044")
    text = job["request"].messages[0].content
    assert text.endswith(ORDER_PROMPT)
    assert "a few blueberry muffins" in text and "2 × Muffin (Blueberry)" in text
    assert job["request"].json_schema == order_check.SCHEMA


def test_parse_needs_a_boolean_verdict():
    assert order_check.parse('{"matches": false, "problem": "2 muffins, asked for a few"}') == {
        "matches": False,
        "problem": "2 muffins, asked for a few",
    }
    assert order_check.parse('```json\n{"matches": true, "problem": ""}\n```')["matches"] is True
    assert order_check.parse('{"matches": "no"}') is None
    assert order_check.parse("not json") is None
