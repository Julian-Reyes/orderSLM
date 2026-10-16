"""Hosted decision providers (Jev, OpenAI Decisions): wire mapping, parsing, retries, cache, cost. No real HTTP."""

import json

import httpx
import pytest

from orderslm.interfaces.decision import DecisionError, DecisionRequest, Option, Question, QuestionType
from orderslm.providers.hosted import HostedDecisionProvider, load_hosted

REQ = DecisionRequest(
    request_id="r1",
    input="[0] customer: 2 cokes pls",
    prompt_version="test@0",
    questions=[
        Question(
            name="intent",
            type=QuestionType.choice,
            prompt="What does message [0] do?",
            options=[
                Option(id="PLACE_ORDER", description="orders"),
                Option(id="SMALL_TALK", description="chat"),
            ],
        ),
        Question(name="order_ok", type=QuestionType.boolean, prompt="Does the order match?"),
    ],
)

JEV_BODY = {
    "model": "jev-1.13.0",
    "answers": {
        "intent": {
            "choice": "PLACE_ORDER",
            "probabilities": {"PLACE_ORDER": 0.9, "SMALL_TALK": 0.1},
            "confidence": 0.8,
        },
        "order_ok": {"noul": 0.3},
    },
    "usage": {"input_tokens": 1000, "output_tokens": 20},
}
OAI_BODY = {
    "model": "gpt-6-luna",
    "answers": [
        {
            "type": "choice",
            "name": "intent",
            "choice": "SMALL_TALK",
            "probabilities": [
                {"value": "PLACE_ORDER", "probability": 0.2},
                {"value": "SMALL_TALK", "probability": 0.8},
            ],
            "confidence": 0.7,
        },
        {"type": "predicate", "name": "order_ok", "probability": 0.9},
    ],
    "usage": {"input_tokens": 400, "output_tokens": 0},
}


def _provider(name, handler, tmp_path, mode="record"):
    seen = []

    def wrapped(request: httpx.Request):
        seen.append(json.loads(request.content))
        return handler(request)

    p = HostedDecisionProvider(
        load_hosted()[name],
        cache_mode=mode,
        cache_dir=tmp_path,
        http=httpx.Client(transport=httpx.MockTransport(wrapped)),
        key=lambda: "test-key",
        sleep=lambda s: None,
    )
    return p, seen


def test_jev_wire_format_and_parsing(tmp_path):
    p, seen = _provider("jev", lambda r: httpx.Response(200, json=JEV_BODY), tmp_path)
    resp = p.decide(REQ)
    wire = seen[0]
    assert wire["model"] == "jev-latest" and wire["state"] == REQ.input
    assert wire["questions"]["intent"] == {
        "type": "choice",
        "instructions": "What does message [0] do?",
        "criteria": {"PLACE_ORDER": "orders", "SMALL_TALK": "chat"},
    }
    assert wire["questions"]["order_ok"] == {"type": "noul", "instructions": "Does the order match?"}
    assert resp.model == "jev-1.13.0" and resp.answers["intent"].choice == "PLACE_ORDER"
    assert resp.answers["order_ok"].boolean is False and resp.answers["order_ok"].probabilities["true"] == 0.3
    assert resp.cost_micros == 42  # 1,000 input tokens × $0.042/1M, output free


def test_openai_decisions_wire_format_and_parsing(tmp_path):
    p, seen = _provider("openai-decisions", lambda r: httpx.Response(200, json=OAI_BODY), tmp_path)
    resp = p.decide(REQ)
    wire = seen[0]
    assert wire["model"] == "gpt-6-luna" and wire["input"] == REQ.input
    assert wire["questions"][0]["choices"] == [
        {"value": "PLACE_ORDER", "description": "orders"},
        {"value": "SMALL_TALK", "description": "chat"},
    ]
    assert wire["questions"][1] == {
        "type": "predicate",
        "name": "order_ok",
        "instructions": "Does the order match?",
    }
    assert (
        resp.answers["intent"].choice == "SMALL_TALK"
        and resp.answers["intent"].probabilities["SMALL_TALK"] == 0.8
    )
    assert resp.answers["order_ok"].boolean is True
    assert resp.cost_micros == 40  # 400 × $0.10/1M


def test_cache_replays_for_free_and_replay_mode_never_calls(tmp_path):
    p, seen = _provider("jev", lambda r: httpx.Response(200, json=JEV_BODY), tmp_path)
    first = p.decide(REQ)
    again = p.decide(REQ)
    assert len(seen) == 1 and not first.cached and again.cached
    q, seen2 = _provider("jev", lambda r: pytest.fail("no call in replay"), tmp_path / "empty", mode="replay")
    with pytest.raises(DecisionError, match="cache miss"):
        q.decide(REQ)


def test_retries_then_fails_fast_on_auth(tmp_path):
    calls = iter([httpx.Response(429), httpx.Response(529), httpx.Response(200, json=JEV_BODY)])
    p, seen = _provider("jev", lambda r: next(calls), tmp_path, mode="off")
    assert p.decide(REQ).answers["intent"].choice == "PLACE_ORDER" and len(seen) == 3
    q, _ = _provider("jev", lambda r: httpx.Response(401, json={"error": "bad key"}), tmp_path, mode="off")
    with pytest.raises(DecisionError, match="HTTP 401"):
        q.decide(REQ)


def test_bad_answers_are_rejected(tmp_path):
    bad = json.loads(json.dumps(JEV_BODY))
    bad["answers"]["intent"]["choice"] = "NOT_AN_OPTION"
    p, _ = _provider("jev", lambda r: httpx.Response(200, json=bad), tmp_path, mode="off")
    with pytest.raises(DecisionError, match="not an offered option"):
        p.decide(REQ)
    refusal = {
        "answers": [
            {"type": "refusal", "name": "intent"},
            {"type": "predicate", "name": "order_ok", "probability": 1},
        ]
    }
    q, _ = _provider("openai-decisions", lambda r: httpx.Response(200, json=refusal), tmp_path, mode="off")
    assert q.decide(REQ).answers["intent"].refused
