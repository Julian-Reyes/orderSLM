from orderslm.eval import student_errors as se
from orderslm.eval.dataset import load_eval_split
from orderslm.schema.conversation import Split


def _dev(cid):
    return next(ac for ac in load_eval_split(Split.dev) if ac.conversation.id == cid)


AC = _dev("a-dev-004")  # L1 1× veggie_pizza large + 1 modification, L2 1× garlic_knots


def _with_items(items):
    return AC.gold_extraction.model_copy(update={"items": items})


def test_gold_itself_has_no_errors():
    assert se.chat_errors(AC, AC.gold_extraction, None) is None
    assert se.item_diffs(AC.gold_extraction, AC.gold_extraction) == []


def test_invalid_answer_is_reported_with_its_reason():
    assert se.chat_errors(AC, None, "order.items.0: bad") == {"invalid": "order.items.0: bad"}


def test_same_dish_pairs_and_names_the_parts_that_differ():
    pizza, knots = AC.gold_extraction.items
    wrong = pizza.model_copy(update={"quantity": 2, "variant_id": "medium"})
    diffs = se.item_diffs(AC.gold_extraction, _with_items([wrong, knots]))
    assert [d["kind"] for d in diffs] == ["wrong_quantity+variant"]
    assert diffs[0]["parts"] == ["quantity", "variant"]
    no_mods = pizza.model_copy(update={"modifications": []})
    assert [d["kind"] for d in se.item_diffs(AC.gold_extraction, _with_items([no_mods, knots]))] == [
        "wrong_modifications"
    ]


def test_dropped_and_invented_items():
    pizza, knots = AC.gold_extraction.items
    extra = knots.model_copy(update={"line_id": "L3", "menu_item_id": "breadsticks"})
    diffs = se.item_diffs(AC.gold_extraction, _with_items([pizza, extra]))
    assert sorted(d["kind"] for d in diffs) == ["extra_item", "missing_item"]
    e = se.chat_errors(AC, _with_items([pizza]), None)
    assert [d["kind"] for d in e["items"]] == ["missing_item"] and e["fields"] == {}


def test_field_mistakes_list_gold_and_predicted_values():
    gold = AC.gold_extraction
    pred = gold.model_copy(update={"payment": gold.payment.model_copy(update={"customer_claims_paid": True})})
    e = se.chat_errors(AC, pred, None)
    assert e["items"] == [] and list(e["fields"]) == ["payment"]
    assert e["fields"]["payment"]["gold"] != e["fields"]["payment"]["pred"]


def test_items_in_a_chat_with_no_order():
    no_order = next(ac for ac in load_eval_split(Split.dev) if ac.gold_extraction is None)
    assert se.chat_errors(no_order, _with_items([]), None) is None
    e = se.chat_errors(no_order, _with_items(list(AC.gold_extraction.items)), None)
    assert len(e["items_without_order"]) == 2
