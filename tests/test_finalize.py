"""core.finalize: code applies the missing-info rules, the question template and default variants to a model's facts."""

import json

from orderslm.core.finalize import fill_default_variants, finalize, parse_and_finalize
from orderslm.eval.dataset import load_eval_split
from orderslm.eval.metrics import score_conversation
from orderslm.menus import load_menu
from orderslm.schema.conversation import Split
from orderslm.schema.extraction import DecisionState, ExtractionOutput, FieldRef, MissingReason, PaymentMethod

DEV = [ac for ac in load_eval_split(Split.dev) if ac.gold_extraction is not None]


def _by_id(cid):
    return next(ac for ac in DEV if ac.conversation.id == cid)


def _judgments(output: ExtractionOutput):
    return {
        (m.field.value, m.reason.value, m.line_id)
        for m in output.missing_or_ambiguous
        if m.reason is MissingReason.ambiguous
    }


def _key(o: ExtractionOutput) -> list[tuple[str, str, str]]:
    return sorted((m.field.value, m.reason.value, m.line_id or "") for m in o.missing_or_ambiguous)


def test_code_rebuilds_every_dev_gold_missing_list():
    """Strip the gold's missing list and question; finalize (given only the gold's 'ambiguous' calls, which need the
    text) must rebuild the same missing list for every dev conversation with an order."""
    for ac in DEV:
        gold = ac.gold_extraction
        menu = load_menu(ac.conversation.business_id)
        stripped = gold.model_copy(update={"missing_or_ambiguous": [], "clarification_question": None})
        out = finalize(stripped, menu, _judgments(gold))
        assert _key(out) == _key(gold), ac.conversation.id
        assert (out.clarification_question is None) == (not gold.missing_or_ambiguous)


def test_default_variant_is_filled_but_an_unknown_size_is_not():
    menu = load_menu("corner-patty")
    burger = menu.item("cheeseburger")
    assert burger.default_variant_id == "single"
    base = next(ac for ac in DEV if ac.conversation.business_id == "corner-patty").gold_extraction
    line = base.items[0].model_copy(
        update={
            "menu_item_id": "cheeseburger",
            "variant_id": None,
            "unmatched_variant_text": None,
            "halves": None,
        }
    )
    odd = line.model_copy(update={"line_id": "L99", "unmatched_variant_text": "triple"})
    out = fill_default_variants(base.model_copy(update={"items": [line, odd]}), menu)
    assert out.items[0].variant_id == "single"
    assert out.items[1].variant_id is None  # "triple" isn't a variant: still asked about


def test_blank_and_default_variant_score_the_same():
    ac = next(
        a
        for a in DEV
        if any(
            i.menu_item_id
            and i.variant_id is None
            and (it := load_menu(a.conversation.business_id).item(i.menu_item_id))
            and it.default_variant_id
            and i.unmatched_variant_text is None
            for i in a.gold_extraction.items
        )
    )
    menu = load_menu(ac.conversation.business_id)
    pred = fill_default_variants(ac.gold_extraction, menu)
    assert pred != ac.gold_extraction
    s = score_conversation(ac, pred, menu.extractor_view())
    assert s.exact and s.fp == 0 and s.fn == 0


def test_confirmed_with_something_missing_becomes_pending_agreed():
    ac = next(a for a in DEV if a.gold_extraction.customer_decision.state is DecisionState.confirmed)
    menu = load_menu(ac.conversation.business_id)
    gold = ac.gold_extraction
    no_payment = gold.payment.model_copy(
        update={"method": PaymentMethod.unknown, "change_for_cents": None, "evidence": []}
    )
    out = finalize(gold.model_copy(update={"payment": no_payment}), menu)
    assert out.customer_decision.state is DecisionState.pending
    assert out.customer_decision.agreed_while_incomplete
    assert out.customer_decision.evidence == gold.customer_decision.evidence
    assert [m.field for m in out.missing_or_ambiguous] == [FieldRef.payment_method]


def test_model_mistakes_in_its_missing_list_are_ignored():
    """The three luna mistakes from the v0.4 dev run, reproduced on gold facts."""
    for cid in ("a-dev-046", "a-dev-054", "a-dev-089"):
        ac = _by_id(cid)
        menu = load_menu(ac.conversation.business_id)
        data = json.loads(ac.gold_extraction.model_dump_json())
        data["missing_or_ambiguous"] = [{"field": "payment_method", "reason": "missing", "line_id": None}]
        data["clarification_question"] = "Would you like these for pickup or delivery?"
        out, err = parse_and_finalize(json.dumps(data), menu)
        assert err is None, err
        assert sorted(m.field.value for m in out.missing_or_ambiguous) == sorted(
            m.field.value for m in ac.gold_extraction.missing_or_ambiguous
        ), cid


def test_pickup_only_question_never_offers_delivery():
    ac = _by_id("a-dev-054")  # Morning Crumb is pickup-only
    menu = load_menu(ac.conversation.business_id)
    assert not menu.delivery.available
    out, _ = parse_and_finalize(ac.gold_extraction.model_dump_json(), menu)
    assert "deliver" not in out.clarification_question.lower()
    assert "name" in out.clarification_question.lower()


def test_parse_and_finalize_reports_invalid_json():
    menu = load_menu("corner-patty")
    assert parse_and_finalize("{oops", menu)[0] is None
    assert parse_and_finalize("[]", menu) == (None, "output is not a JSON object")


def test_raw_json_path_rebuilds_every_dev_gold():
    """The model path: raw JSON whose missing list and question are wrong (here: empty) must still finalize to the
    gold's missing list, including off-menu lines and confirmed/cancelled orders."""
    for ac in DEV:
        gold = ac.gold_extraction
        data = json.loads(gold.model_dump_json())
        data["missing_or_ambiguous"] = [
            m for m in data["missing_or_ambiguous"] if m["reason"] == "ambiguous"
        ]  # keep only the text judgments
        data["clarification_question"] = None
        out, err = parse_and_finalize(json.dumps(data), load_menu(ac.conversation.business_id))
        assert err is None, (ac.conversation.id, err)
        assert _key(out) == _key(gold), ac.conversation.id
        assert out.customer_decision == gold.customer_decision, ac.conversation.id


# ---------------------------------------------------------------- rule 5: ids the menu doesn't have (finalize@0.2)

from orderslm.checks import check_catalog  # noqa: E402
from orderslm.core.finalize import known_ids  # noqa: E402


def _with_line(cid: str, line_id: str, **update):
    ac = _by_id(cid)
    gold = ac.gold_extraction
    items = [it.model_copy(update=update) if it.line_id == line_id else it for it in gold.items]
    stripped = gold.model_copy(
        update={"items": items, "missing_or_ambiguous": [], "clarification_question": None}
    )
    menu = load_menu(ac.conversation.business_id)
    return finalize(stripped, menu, _judgments(gold)), menu


def _line(out: ExtractionOutput, line_id: str):
    return next(it for it in out.items if it.line_id == line_id)


def _missing_for(out: ExtractionOutput, line_id: str) -> set[tuple[str, str]]:
    return {(m.field.value, m.reason.value) for m in out.missing_or_ambiguous if m.line_id == line_id}


def test_every_dev_gold_has_only_known_ids():
    for ac in DEV:
        menu = load_menu(ac.conversation.business_id)
        assert known_ids(ac.gold_extraction, menu) == ac.gold_extraction, ac.conversation.id


def test_unknown_item_id_becomes_an_off_menu_line_with_its_quote():
    """Fresh 049 shape: the student wrote menu_item_id 'red_bull'; gold has the off-menu line 'a red bull'."""
    out, menu = _with_line("a-dev-006", "L1", menu_item_id="red_bull", variant_id=None)
    line = _line(out, "L1")
    assert line.menu_item_id is None and line.unmatched_text == line.evidence[0].quote
    assert ("item_menu_match", "off_menu") in _missing_for(out, "L1")
    assert out.clarification_question and not check_catalog(out, menu)


def test_unknown_half_makes_the_whole_line_off_menu():
    """Dev 017 shape: a pizza half 'olives' (a topping, not a pizza)."""
    ac = _by_id("a-dev-017")
    halves = [h.model_copy() for h in _line(ac.gold_extraction, "L1").halves]
    halves[1] = halves[1].model_copy(update={"menu_item_id": "olives", "modifications": []})
    out, menu = _with_line("a-dev-017", "L1", halves=halves)
    line = _line(out, "L1")
    assert line.halves is None and line.unmatched_text == line.evidence[0].quote
    assert ("item_menu_match", "off_menu") in _missing_for(out, "L1")
    assert not check_catalog(out, menu)


def test_unknown_size_is_asked_not_defaulted():
    out, menu = _with_line("a-dev-006", "L1", variant_id="party_size")
    line = _line(out, "L1")
    assert line.variant_id is None and line.unmatched_variant_text == "party_size"
    assert ("item_variant", "missing") in _missing_for(out, "L1")
    assert not check_catalog(out, menu)


def test_unknown_add_on_id_becomes_an_unverified_request():
    ac = _by_id("a-dev-002")
    mods = list(_line(ac.gold_extraction, "L1").modifications)
    i = next(k for k, m in enumerate(mods) if m.modifier_id)
    mods[i] = mods[i].model_copy(update={"modifier_id": "unicorn_sauce", "replacement_modifier_id": None})
    out, menu = _with_line("a-dev-002", "L1", modifications=mods)
    mod = _line(out, "L1").modifications[i]
    assert mod.modifier_id is None and mod.raw_text == mods[i].raw_text and not mod.not_on_menu
    assert ("item_modification", "ambiguous") in _missing_for(out, "L1")
    assert not check_catalog(out, menu)


def test_combo_pick_with_unknown_choice_is_dropped_and_asked():
    ac = _by_id("a-dev-002")
    picks = list(_line(ac.gold_extraction, "L1").combo_selections)
    picks[0] = picks[0].model_copy(update={"menu_item_id": "lobster_roll", "variant_id": None})
    out, menu = _with_line("a-dev-002", "L1", combo_selections=picks)
    assert len(_line(out, "L1").combo_selections) == len(picks) - 1
    assert ("combo_choice", "missing") in _missing_for(out, "L1")
    assert not check_catalog(out, menu)


def test_unknown_size_on_an_item_without_sizes_is_dropped():
    """Fresh 028 shape: 'bottle_20oz' on a bottled water that has no sizes; nothing to ask."""
    ac = _by_id("a-dev-006")
    menu = load_menu(ac.conversation.business_id)
    sizeless = next(i for i in menu.items if not i.variants and not i.combo_slots)
    out, _ = _with_line(
        "a-dev-006", "L1", menu_item_id=sizeless.id, variant_id="bottle_20oz", modifications=[]
    )
    line = _line(out, "L1")
    assert line.variant_id is None and line.unmatched_variant_text is None
    assert ("item_variant", "missing") not in _missing_for(out, "L1")
    assert not check_catalog(out, menu)
