"""Order checker: which orders are checked and what the checkers see (no network)."""

from orderslm.eval import order_check
from orderslm.eval.dataset import load_eval_split
from orderslm.eval.label_audit import ORDER_PROMPT, order_text
from orderslm.menus import load_menu
from orderslm.schema.conversation import Split


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
    # finalize@0.2 turns the student's unknown id 'red_bull' into the off-menu line gold has, so fresh 049 is
    # no longer a mistake; the order text still marks a raw unknown id for an order that skips finalize
    assert not jobs.get("fresh__a-fresh-049", {}).get("wrong")
    ac = next(a for a in load_eval_split(Split.fresh) if a.conversation.id == "a-fresh-049")
    gold = ac.gold_extraction
    raw = gold.model_copy(
        update={
            "items": [gold.items[0].model_copy(update={"menu_item_id": "red_bull", "unmatched_text": None})]
        }
    )
    menu = load_menu(ac.conversation.business_id)
    assert "'red_bull' (NOT on the menu)" in order_text(raw, menu, detail=True)
    # fresh 028: finalize@0.2 drops the invented size 'bottle_20oz' on a water with no sizes; raw, it is marked
    croissant = gold.items[1].model_copy(update={"variant_id": "bottle_20oz"})
    raw = gold.model_copy(update={"items": [croissant]})
    assert "NOT a size of this item" in order_text(raw, menu, detail=True)
    assert "bottle_20oz" not in jobs.get("fresh__a-fresh-028", {}).get("order_text", "")
    assert "paying with $20.00 (needs change)" in jobs["dev__a-dev-075"]["order_text"]


def test_parse_needs_a_boolean_verdict():
    assert order_check.parse('{"matches": false, "problem": "2 muffins, asked for a few"}') == {
        "matches": False,
        "problem": "2 muffins, asked for a few",
    }
    assert order_check.parse('```json\n{"matches": true, "problem": ""}\n```')["matches"] is True
    assert order_check.parse('{"matches": "no"}') is None
    assert order_check.parse("not json") is None
