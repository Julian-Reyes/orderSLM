"""Teacher prompt + portable schema, eval data selection, scoring, and the saved-output report. No network."""

import json
from datetime import UTC, datetime

import pytest

from orderslm.eval.dataset import EvalSplitError, bakeoff_set, check_evaluable, load_eval_split
from orderslm.eval.metrics import aggregate, item_key, score_conversation
from orderslm.eval.teacher_bakeoff import _slug, report
from orderslm.extractors.teacher import (
    TEACHER_PROMPT_VERSION,
    build_chat_request,
    portable_schema,
    to_result,
)
from orderslm.interfaces.extractor import ExtractionRequest
from orderslm.llm.types import ChatResponse, LLMUsage
from orderslm.menus import load_menu
from orderslm.paths import SAMPLES
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.conversation import Role, Split
from orderslm.schema.extraction import Evidence, ExtractionOutput

DEV = load_eval_split(Split.dev)
WITH_ORDER = [ac for ac in DEV if ac.gold_extraction is not None]
NO_ORDER = [ac for ac in DEV if ac.gold_extraction is None]
FORBIDDEN_KEYS = {"$ref", "$defs", "const", "pattern", "minLength", "maxLength", "minimum", "maximum"}


def menu_of(ac):
    return load_menu(ac.conversation.business_id).extractor_view()


# --- data selection -----------------------------------------------------------------------------


def test_samples_are_never_evaluated():
    sample = AnnotatedConversation.model_validate_json(
        sorted((SAMPLES / "conversations").glob("*.json"))[0].read_text()
    )
    assert sample.conversation.split is Split.sample
    with pytest.raises(EvalSplitError, match="few-shot only"):
        check_evaluable([sample], Split.dev)
    with pytest.raises(EvalSplitError):
        load_eval_split(Split.sample)


def test_bakeoff_set_is_stable_and_stratified():
    a, b = bakeoff_set(DEV), bakeoff_set(list(reversed(DEV)))
    ids = [ac.conversation.id for ac in a]
    assert ids == [ac.conversation.id for ac in b]  # input order doesn't matter
    assert len(ids) == 40 and len(set(ids)) == 40
    no_order = sum(ac.gold_extraction is None for ac in a)
    assert no_order == round(40 * len(NO_ORDER) / len(DEV))
    assert sum(ac.gold_extraction is None for ac in a[:5]) == 1  # a 5-conversation pilot sees both kinds


# --- prompt and schema --------------------------------------------------------------------------


def _walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def test_portable_schema_is_closed_inlined_and_constraint_free():
    schema = portable_schema()
    for node in _walk(schema):
        assert not FORBIDDEN_KEYS & set(node), FORBIDDEN_KEYS & set(node)
        if node.get("type") == "object" and "properties" in node:
            assert node["required"] == list(node["properties"])
            assert node["additionalProperties"] is False


def _branch(schema, value):
    """Pick the anyOf branch that fits a value (null vs. object vs. other)."""
    if "anyOf" not in schema:
        return schema
    for b in schema["anyOf"]:
        t = b.get("type")
        if value is None and t == "null":
            return b
        if isinstance(value, dict) and t == "object":
            return b
        if isinstance(value, list) and t == "array":
            return b
        if value is not None and not isinstance(value, dict | list) and t not in ("null", "object", "array"):
            return b
    raise AssertionError(f"no branch for {value!r} in {schema}")


def _same_keys(schema, value, path="$"):
    schema = _branch(schema, value)
    if isinstance(value, dict):
        assert set(value) == set(schema["properties"]), path
        for k, v in value.items():
            _same_keys(schema["properties"][k], v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            _same_keys(schema["items"], v, f"{path}[{i}]")
    elif "enum" in schema:
        assert value in schema["enum"], (path, value)


def test_every_dev_gold_has_exactly_the_schema_shape():
    """The portable schema can express every gold answer: same keys everywhere, enum values allowed."""
    schema = portable_schema()
    for ac in WITH_ORDER:
        _same_keys(schema, json.loads(ac.gold_extraction.model_dump_json()), ac.conversation.id)


def test_chat_request_is_identical_input_for_every_provider():
    ac = next(a for a in WITH_ORDER if any(m.role is Role.business for m in a.conversation.messages))
    req = ExtractionRequest(
        menu=menu_of(ac), conversation=ac.conversation, prompt_version=TEACHER_PROMPT_VERSION
    )
    chat = build_chat_request(req)
    assert (
        "JSON" in chat.system and '"additionalProperties":false' in chat.system
    )  # DeepSeek needs it in text
    assert chat.json_schema == portable_schema()
    user = chat.messages[0].content
    for m in ac.conversation.messages:
        assert f"[{m.index}] {m.role.value} " in user and m.text in user
    assert ac.conversation.business_id in user
    fields = {k for node in _walk(chat.json_schema) for k in node.get("properties", {})}
    assert not {f for f in fields if "price" in f or "total" in f or "fee" in f}


def test_to_result_flags_truncation_and_keeps_cost():
    ac = WITH_ORDER[0]
    resp = ChatResponse(
        config_id="openai/gpt-6-luna@none",
        model="gpt-6-luna",
        text=ac.gold_extraction.model_dump_json(),
        finish_reason="length",
        usage=LLMUsage(input_tokens=10, output_tokens=5),
        latency_ms=3.0,
        cost_micros=7,
        at=datetime(2026, 10, 15, tzinfo=UTC).isoformat(),
    )
    result = to_result(resp)
    assert result.output is not None and result.error == "finish_reason=length" and result.cost_micros == 7
    assert to_result(resp.model_copy(update={"text": "{oops"})).output is None


# --- metrics ------------------------------------------------------------------------------------


def test_gold_scores_perfectly():
    # With no order, the perfect answer is the empty order.
    scores = [
        score_conversation(ac, ac.gold_extraction or ExtractionOutput.empty(), menu_of(ac)) for ac in DEV
    ]
    m = aggregate(scores)
    assert m["item"]["f1"] == 1.0 and m["exact_match_rate"] == 1.0
    assert all(v == 1.0 for v in m["field_accuracy"].values())
    assert m["grounding"]["conversations_with_issues"] == 0, m["grounding"]["issues"]


def test_wrong_quantity_is_one_fp_and_one_fn():
    ac = next(a for a in WITH_ORDER if a.gold_extraction.items and a.gold_extraction.items[0].quantity)
    pred = ac.gold_extraction.model_copy(deep=True)
    pred.items[0].quantity = pred.items[0].quantity + 1
    s = score_conversation(ac, pred, menu_of(ac))
    assert (s.tp, s.fp, s.fn) == (len(pred.items) - 1, 1, 1) and not s.exact
    assert item_key(pred.items[0]) != item_key(ac.gold_extraction.items[0])


def test_invalid_output_misses_every_gold_item():
    ac = next(a for a in WITH_ORDER if a.gold_extraction.items)
    s = score_conversation(ac, None, menu_of(ac))
    assert not s.valid and s.tp == 0 and s.fn == len(ac.gold_extraction.items) and not s.exact


def test_items_without_order_and_business_citations_are_grounding_issues():
    no_order = NO_ORDER[0]
    donor = next(a for a in WITH_ORDER if a.conversation.business_id == no_order.conversation.business_id)
    pred = donor.gold_extraction.model_copy(deep=True)
    s = score_conversation(no_order, pred, menu_of(no_order))
    assert "ITEMS_WITHOUT_ORDER" in s.grounding_issues and not s.exact and s.fp == len(pred.items)

    ac = next(
        a
        for a in WITH_ORDER
        if a.gold_extraction.items and any(m.role is Role.business for m in a.conversation.messages)
    )
    business = next(m for m in ac.conversation.messages if m.role is Role.business)
    pred = ac.gold_extraction.model_copy(deep=True)
    pred.items[0].evidence = [Evidence(message_index=business.index, quote=business.text[:20])]
    assert "EVIDENCE_BUSINESS_MESSAGE" in score_conversation(ac, pred, menu_of(ac)).grounding_issues


# --- report from saved outputs ------------------------------------------------------------------


def test_report_rebuilds_from_saved_outputs(tmp_path):
    convs = bakeoff_set(DEV)[:5]
    variant = "openai/gpt-6-luna@none"
    manifest = {
        "run_id": "test",
        "mode": "pilot 5",
        "prompt_version": TEACHER_PROMPT_VERSION,
        "schema_version": "extraction@0.4",
        "git_commit": "abc",
        "cache_mode": "replay",
        "estimate_micros": 100,
        "actual_cost_micros": 50,
        "data": {"conversation_ids": [ac.conversation.id for ac in convs]},
        "variants": {variant: {}},
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    out = tmp_path / "outputs" / _slug(variant)
    out.mkdir(parents=True)
    for i, ac in enumerate(convs):
        text = ac.gold_extraction.model_dump_json() if ac.gold_extraction else '{"items": []}'
        resp = ChatResponse(
            config_id=variant,
            model="gpt-6-luna",
            text=text,
            finish_reason="stop",
            usage=LLMUsage(input_tokens=1000, output_tokens=100 + i),
            latency_ms=100.0 * (i + 1),
            cost_micros=150,
            at="2026-10-15T00:00:00+00:00",
        )
        (out / f"{ac.conversation.id}.json").write_text(
            json.dumps({"conversation_id": ac.conversation.id, "response": resp.model_dump(mode="json")})
        )
    r = report(tmp_path)[variant]
    # The no-order conversation got invalid JSON ('{"items": []}' lacks required fields): 4/5 valid.
    assert r["json_valid"] == 4 and r["item"]["f1"] == 1.0
    assert r["tokens"]["input_tokens"] == 5000 and r["cost_micros"] == 750
    assert r["cost_per_1000_conversations_usd"] == 0.15
    assert "openai/gpt-6-luna@none" in (tmp_path / "report.md").read_text()


def test_remaining_dev_is_disjoint_from_the_bakeoff_set():
    from orderslm.eval.dataset import remaining_dev

    rest = remaining_dev(DEV)
    used = {ac.conversation.id for ac in bakeoff_set(DEV)}
    assert len(rest) == len(DEV) - 40 and not used & {ac.conversation.id for ac in rest}


def test_wilson_interval():
    from orderslm.eval.stats import wilson

    lo, hi = wilson(33, 35)
    assert round(lo, 2) == 0.81 and round(hi, 2) == 0.98
    assert wilson(0, 0) is None and wilson(0, 10)[0] == 0.0 and wilson(10, 10)[1] == 1.0
