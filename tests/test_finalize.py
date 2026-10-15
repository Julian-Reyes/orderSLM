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
