"""Order checker: which orders are checked and what the checkers see (no network)."""

from orderslm.eval import order_check
from orderslm.eval.label_audit import ORDER_PROMPT


def _jobs() -> dict:
    return {j["id"]: j for j in order_check.jobs()}


def test_checks_the_students_real_mistakes_and_as_many_right_orders():
    jobs = _jobs()
    wrong = {k for k, j in jobs.items() if j["wrong"]}
    # dev 016 and 038 are wrong only in wording (same action as gold), so they are not mistakes
    assert "dev__a-dev-016" not in wrong and "dev__a-dev-038" not in wrong
    assert "fresh__a-fresh-051" in wrong  # "actually drop the muffin" ignored
    assert jobs["fresh__a-fresh-034"]["kinds"] == ["broken_answer"]
    assert all(jobs[k]["kinds"] for k in wrong)
    for split in ("dev", "fresh"):
        js = [j for j in jobs.values() if j["split"] == split]
        assert sum(j["wrong"] for j in js) == sum(not j["wrong"] for j in js) > 0
    assert all(not j["kinds"] for j in jobs.values() if not j["wrong"])
    assert [j["id"] for j in order_check.jobs()] == list(jobs)  # the right sample is seeded


def test_every_checker_sees_the_same_chat_menu_and_order():
    job = _jobs()["fresh__a-fresh-044"]
    chat = job["request"].messages[0].content
    text = job["decision_request"].input
    assert chat == f"{text}\n\n{order_check.CHECK_PROMPT}"
    assert job["decision_request"].questions[0].prompt == order_check.CHECK_PROMPT
    assert order_check.CHECK_PROMPT.startswith(ORDER_PROMPT)
    assert "a few blueberry muffins" in text and "2 × Muffin (Blueberry)" in text
    assert "The menu of Morning Crumb Café:" in text and "Medium 12 oz (default)" in text
    assert job["request"].json_schema == order_check.SCHEMA


def test_the_order_text_shows_what_the_pilot_could_not_see():
    jobs = _jobs()
    assert "'red_bull' (NOT on the menu)" in jobs["fresh__a-fresh-049"]["order_text"]
    assert "NOT a size of this item" in jobs["fresh__a-fresh-028"]["order_text"]
    assert "paying with $20.00 (needs change)" in jobs["dev__a-dev-075"]["order_text"]


def test_parse_needs_a_boolean_verdict():
    assert order_check.parse('{"matches": false, "problem": "2 muffins, asked for a few"}') == {
        "matches": False,
        "problem": "2 muffins, asked for a few",
    }
    assert order_check.parse('```json\n{"matches": true, "problem": ""}\n```')["matches"] is True
    assert order_check.parse('{"matches": "no"}') is None
    assert order_check.parse("not json") is None
