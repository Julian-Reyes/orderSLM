"""Router taxonomy and the provider-neutral request/response mapping."""

import re

import pytest
from pydantic import ValidationError

from orderslm.interfaces.decision import (
    Answer,
    DecisionError,
    DecisionRequest,
    QuestionType,
    check_against_limits,
    validate_response,
)
from orderslm.mocks.decision import ScriptedDecisionProvider, router_answers
from orderslm.router import RouterContext, build_router_request, parse_router_response, render_input
from orderslm.schema.routing import (
    LABEL_DESCRIPTIONS,
    ORDER_LABELS,
    ContextFlags,
    OrderReference,
    RouterDecision,
    RouterLabel,
)

SPEC_LABELS = [
    "PLACE_ORDER", "MODIFY_ORDER", "CANCEL_ORDER", "CONFIRM_ORDER", "MENU_QUESTION", "DELIVERY_QUESTION",
    "PAYMENT_QUESTION", "PAYMENT_CLAIM", "ORDER_STATUS", "ORDER_PROBLEM", "REFUND_REQUEST", "HUMAN_REQUEST",
    "SMALL_TALK", "OUT_OF_SCOPE", "UNKNOWN",
]  # fmt: skip
JULIA_MAX_OPTIONS = 20  # spec §11, to be re-verified in M7


def test_labels_match_spec_exactly_and_in_order():
    assert [label.value for label in RouterLabel] == SPEC_LABELS


def test_every_label_has_a_short_description():
    assert set(LABEL_DESCRIPTIONS) == set(RouterLabel)
    for label, desc in LABEL_DESCRIPTIONS.items():
        # Proxy for Julia-1's 48-token option limit until the real tokenizer check in M7:
        # 20 words is ~30 tokens in English BPE tokenizers, leaving room for the label id.
        assert len(desc.split()) <= 20, label
        assert len(desc) <= 120, label


def test_order_labels():
    assert {label.value for label in ORDER_LABELS} == {
        "PLACE_ORDER",
        "MODIFY_ORDER",
        "CANCEL_ORDER",
        "CONFIRM_ORDER",
    }


# ---- RouterDecision rules


def flags(**kw):
    return ContextFlags(refers_to=kw.pop("refers_to", OrderReference.draft), **kw)


def test_secondary_must_differ_from_primary():
    with pytest.raises(ValidationError, match="must differ"):
        RouterDecision(primary=RouterLabel.PLACE_ORDER, secondary=RouterLabel.PLACE_ORDER, flags=flags())


def test_unknown_cannot_combine():
    with pytest.raises(ValidationError, match="UNKNOWN"):
        RouterDecision(primary=RouterLabel.UNKNOWN, secondary=RouterLabel.SMALL_TALK, flags=flags())


def test_human_request_implies_flag():
    with pytest.raises(ValidationError, match="asks_for_human"):
        RouterDecision(primary=RouterLabel.ORDER_PROBLEM, secondary=RouterLabel.HUMAN_REQUEST, flags=flags())


def test_goes_to_extractor_on_secondary_order_label():
    d = RouterDecision(primary=RouterLabel.MENU_QUESTION, secondary=RouterLabel.PLACE_ORDER, flags=flags())
    assert d.goes_to_extractor


# ---- request building


@pytest.fixture
def ctx(sample_by_id):
    return RouterContext(sample_by_id["sample-001"].conversation, 2, has_draft=True, has_placed_order=False)


def test_request_fits_every_provider_limit(ctx):
    req = build_router_request(ctx)
    for q in req.questions:
        if q.type is QuestionType.choice:
            assert 2 <= len(q.options) <= JULIA_MAX_OPTIONS, q.name
    check_against_limits(ScriptedDecisionProvider(max_options=JULIA_MAX_OPTIONS), req)


def test_request_uses_the_shared_label_descriptions_verbatim(ctx):
    primary = next(q for q in build_router_request(ctx).questions if q.name == "primary")
    assert {o.id: o.description for o in primary.options} == {
        k.value: v for k, v in LABEL_DESCRIPTIONS.items()
    }


def test_secondary_offers_none_but_not_unknown(ctx):
    secondary = next(q for q in build_router_request(ctx).questions if q.name == "secondary")
    ids = [o.id for o in secondary.options]
    assert ids[0] == "NONE" and "UNKNOWN" not in ids


def test_identical_request_for_every_provider(ctx):
    providers = [ScriptedDecisionProvider([router_answers("MODIFY_ORDER")], name=n) for n in ("a", "b", "c")]
    for p in providers:
        p.decide(build_router_request(ctx))
    first = providers[0].requests[0].model_dump_json()
    assert all(p.requests[0].model_dump_json() == first for p in providers)


def test_input_shows_context_and_marks_latest_message(ctx):
    text = render_input(ctx)
    assert text.endswith("Latest customer message: and swap the coke for a sprite")
    assert "customer: hey can i get 2 cheeseburgers and a coke" in text
    assert "Order in progress: yes." in text


def test_routing_a_business_message_is_an_error(sample_by_id):
    convo = sample_by_id["sample-006"].conversation
    with pytest.raises(ValueError, match="not a customer message"):
        render_input(RouterContext(convo, 1, has_draft=True, has_placed_order=False))


def test_limit_check_rejects_too_many_options(ctx):
    with pytest.raises(DecisionError, match="limit 3"):
        check_against_limits(ScriptedDecisionProvider(max_options=3), build_router_request(ctx))


# ---- response parsing


def test_round_trip_through_scripted_provider(ctx):
    provider = ScriptedDecisionProvider([router_answers("MODIFY_ORDER", secondary="MENU_QUESTION")])
    req = build_router_request(ctx)
    resp = provider.decide(req)
    validate_response(req, resp)
    parsed = parse_router_response(resp)
    assert parsed.decision.primary is RouterLabel.MODIFY_ORDER
    assert parsed.decision.secondary is RouterLabel.MENU_QUESTION
    assert not parsed.abstained and parsed.notes == []


def test_refused_primary_is_an_abstention(ctx):
    resp = router_answers("", refuse_primary=True)
    validate_response(build_router_request(ctx), resp)
    parsed = parse_router_response(resp)
    assert parsed.abstained and parsed.decision.primary is RouterLabel.UNKNOWN


def test_repairs_are_reported_not_hidden(ctx):
    parsed = parse_router_response(
        router_answers("HUMAN_REQUEST", secondary="HUMAN_REQUEST", asks_for_human=False)
    )
    assert parsed.decision.secondary is None and parsed.decision.flags.asks_for_human
    assert len(parsed.notes) == 2


def test_choice_outside_offered_options_is_rejected(ctx):
    req = build_router_request(ctx)
    resp = router_answers("REORDER")  # not a V1 label
    with pytest.raises(DecisionError, match="not an offered option"):
        validate_response(req, resp)


def test_missing_answer_is_rejected(ctx):
    req = build_router_request(ctx)
    resp = router_answers("PLACE_ORDER")
    del resp.answers["urgency"]
    with pytest.raises(DecisionError, match="no answer for 'urgency'"):
        validate_response(req, resp)


def test_answer_shape_rules():
    with pytest.raises(ValidationError, match="no choice value"):
        Answer(name="primary", type=QuestionType.choice)
    with pytest.raises(ValidationError, match="refused answer"):
        Answer(name="primary", type=QuestionType.choice, choice="X", refused=True)
    with pytest.raises(ValidationError):
        Answer(name="primary", type=QuestionType.choice, choice="X", confidence=1.5)


def test_choice_question_needs_two_options():
    with pytest.raises(ValidationError, match="at least 2"):
        DecisionRequest(
            request_id="r",
            input="x",
            prompt_version="p",
            questions=[
                {"name": "q", "type": "choice", "prompt": "?", "options": [{"id": "A", "description": "a"}]}
            ],
        )


def test_gold_routing_labels_are_all_valid_codes(samples):
    for s in samples:
        for r in s.gold_routing:
            assert re.fullmatch(r"[A-Z_]+", r.decision.primary.value)
