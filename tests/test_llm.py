"""LLM client layer: config, costs, request shapes, usage parsing, retries, cache, throttle.
No test touches the network: HTTP goes through httpx.MockTransport."""

import json
from datetime import datetime

import httpx
import pytest

from orderslm.domain.clock import fixed_clock
from orderslm.llm.cache import CachedClient, CacheMiss, cache_key
from orderslm.llm.client import HttpChatClient
from orderslm.llm.config import get_model, load_models, lowest_variants
from orderslm.llm.env import api_key, read_dotenv
from orderslm.llm.fake import ScriptedChatClient
from orderslm.llm.throttle import Throttle
from orderslm.llm.types import ChatMessage, ChatRequest, LLMError, LLMUsage
from orderslm.paths import ROOT

SCHEMA = {
    "type": "object",
    "properties": {"n": {"type": "integer"}},
    "required": ["n"],
    "additionalProperties": False,
}
REQ = ChatRequest(
    system="Reply in JSON.", messages=[ChatMessage(role="user", content="n?")], json_schema=SCHEMA
)
# Tuesday 2026-10-13 at 02:00 UTC is DeepSeek peak; 12:00 UTC is off-peak.
PEAK = "2026-10-13T02:00:00+00:00"
OFF_PEAK = "2026-10-13T12:00:00+00:00"


def openai_reply(content='{"n": 1}', usage=None, **message):
    return {
        "model": "m",
        "choices": [{"message": {"content": content, **message}, "finish_reason": "stop"}],
        "usage": usage or {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


def client_for(config_id, handler, *, at=OFF_PEAK, sleeps=None):
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return HttpChatClient(
        get_model(config_id),
        lambda: "sk-test",
        clock=fixed_clock(at),
        http=http,
        sleep=(sleeps.append if sleeps is not None else lambda s: None),
    )


# --- config and costs ---------------------------------------------------------------------------


def test_models_config_loads_and_keys_are_documented():
    models = load_models()
    assert set(models) == {
        "openai/gpt-6-luna@none",
        "openai/gpt-6-luna@low",
        "openai/gpt-6-luna@medium",
        "anthropic/claude-haiku-5-5@off-low",
        "anthropic/claude-haiku-5-5@off-medium",
        "anthropic/claude-haiku-5-5@on-low",
        "anthropic/claude-haiku-5-5@on-medium",
        "google/gemini-3.1-flash-lite@minimal",
        "google/gemini-3.1-flash-lite@default",
        "deepseek/deepseek-flash@none",
        "deepseek/deepseek-flash@low",
        "deepseek/deepseek-flash@high",
    }
    assert lowest_variants() == [
        "openai/gpt-6-luna@none",
        "anthropic/claude-haiku-5-5@off-low",
        "google/gemini-3.1-flash-lite@minimal",
        "deepseek/deepseek-flash@none",
    ]
    defaults = sorted(m.id for m in models.values() if m.provider_default)
    assert defaults == [
        "anthropic/claude-haiku-5-5@on-medium",
        "deepseek/deepseek-flash@high",
        "google/gemini-3.1-flash-lite@default",
        "openai/gpt-6-luna@medium",
    ]
    env_example = (ROOT / ".env.example").read_text()
    costs = (ROOT / "docs" / "COSTS.md").read_text()
    for m in models.values():
        assert f"{m.key_env}=" in env_example
        assert f"`{m.model}`" in costs, f"{m.model} missing from docs/COSTS.md price table"
        assert m.price_verified in costs


def test_variants_differ_only_in_reasoning_settings():
    models = load_models()
    for m in models.values():
        base = models[[i for i in models if i.startswith(m.base_id + "@")][0]]
        assert m.model_dump(exclude={"id", "variant", "extra_body", "provider_default"}) == base.model_dump(
            exclude={"id", "variant", "extra_body", "provider_default"}
        )


def test_cost_is_integer_micros_rounded_up():
    luna = get_model("openai/gpt-6-luna@none")
    at = datetime.fromisoformat(OFF_PEAK)
    # 100K input at $0.10/M + 100K output at $0.50/M = $0.01 + $0.05
    assert luna.cost_micros(LLMUsage(input_tokens=100_000, output_tokens=100_000), at) == 60_000
    # 1 token of output = 0.5 micro-USD → rounds up to 1
    assert luna.cost_micros(LLMUsage(output_tokens=1), at) == 1
    # cached input billed at the cached price ($0.01/M)
    assert luna.cost_micros(LLMUsage(input_tokens=100_000, cached_input_tokens=100_000), at) == 1_000


def test_deepseek_peak_and_off_peak():
    ds = get_model("deepseek/deepseek-flash@none")
    usage = LLMUsage(input_tokens=1_000_000, output_tokens=1_000_000)
    assert ds.cost_micros(usage, datetime.fromisoformat(PEAK)) == 1_500_000
    assert ds.cost_micros(usage, datetime.fromisoformat(OFF_PEAK)) == 750_000
    saturday_peak_hour = datetime.fromisoformat("2026-10-17T02:00:00+00:00")
    assert ds.cost_micros(usage, saturday_peak_hour) == 750_000


def test_long_context_switches_price_or_refuses_unverified():
    haiku = get_model("anthropic/claude-haiku-5-5@off-low")
    at = datetime.fromisoformat(OFF_PEAK)
    assert haiku.cost_micros(LLMUsage(input_tokens=100_000), at) == 10_000
    assert haiku.cost_micros(LLMUsage(input_tokens=200_000), at) == 100_000  # $0.50/M above 100K
    with pytest.raises(ValueError, match="long-context price not verified"):
        get_model("openai/gpt-6-luna@none").cost_micros(LLMUsage(input_tokens=300_000), at)


def test_missing_cached_price_bills_as_input():
    gemini = get_model("google/gemini-3.1-flash-lite@minimal")
    usage = LLMUsage(input_tokens=1_000_000, cached_input_tokens=1_000_000)
    assert gemini.cost_micros(usage, datetime.fromisoformat(OFF_PEAK)) == 250_000


# --- request shapes -----------------------------------------------------------------------------


def test_openai_request_uses_json_schema_and_max_completion_tokens():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        seen["auth"] = request.headers["authorization"]
        seen["url"] = str(request.url)
        return httpx.Response(200, json=openai_reply())

    resp = client_for("openai/gpt-6-luna@none", handler).complete(REQ)
    body = seen["body"]
    assert seen["url"] == "https://api.openai.com/v1/chat/completions"
    assert seen["auth"] == "Bearer sk-test"
    assert body["max_completion_tokens"] == 2048 and "max_tokens" not in body
    assert body["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "output", "schema": SCHEMA, "strict": True},
    }
    assert body["reasoning_effort"] == "none"
    assert body["messages"][0] == {"role": "system", "content": "Reply in JSON."}
    assert resp.text == '{"n": 1}' and resp.cost_micros == 4  # 10×0.1 + 5×0.5 = 3.5 → 4


def test_deepseek_uses_json_object_and_needs_json_in_prompt():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json=openai_reply())

    client = client_for("deepseek/deepseek-flash@none", handler)
    client.complete(REQ)
    assert seen["body"]["response_format"] == {"type": "json_object"}
    assert seen["body"]["reasoning_effort"] == "none"
    assert seen["body"]["max_tokens"] == 2048
    no_json = REQ.model_copy(update={"system": "Answer briefly."})
    with pytest.raises(ValueError, match="must mention JSON"):
        client.complete(no_json)


def test_anthropic_request_and_usage():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        seen["headers"] = request.headers
        return httpx.Response(
            200,
            json={
                "model": "claude-haiku-5-5",
                "content": [{"type": "text", "text": '{"n": 2}'}],
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 100,
                    "cache_read_input_tokens": 1000,
                    "cache_creation_input_tokens": 0,
                    "output_tokens": 20,
                    "output_tokens_details": {"thinking_tokens": 12},
                },
            },
        )

    resp = client_for("anthropic/claude-haiku-5-5@off-low", handler).complete(REQ)
    body = seen["body"]
    assert seen["headers"]["x-api-key"] == "sk-test"
    assert seen["headers"]["anthropic-version"] == "2023-06-01"
    assert body["system"] == "Reply in JSON." and body["max_tokens"] == 2048
    assert body["output_config"] == {"format": {"type": "json_schema", "schema": SCHEMA}, "effort": "low"}
    assert body["thinking"] == {"type": "disabled"}
    assert resp.usage == LLMUsage(
        input_tokens=1100, cached_input_tokens=1000, output_tokens=20, reasoning_tokens=12
    )
    assert resp.cost_micros == 30  # 100×0.1 + 1000×0.01 + 20×0.5


def test_usage_parsing_variants():
    def run(config_id, usage):
        return client_for(config_id, lambda r: httpx.Response(200, json=openai_reply(usage=usage))).complete(
            REQ
        )

    openai = run(
        "openai/gpt-6-luna@none",
        {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
            "prompt_tokens_details": {"cached_tokens": 60},
            "completion_tokens_details": {"reasoning_tokens": 30},
        },
    )
    assert openai.usage == LLMUsage(
        input_tokens=100, cached_input_tokens=60, output_tokens=50, reasoning_tokens=30
    )
    deepseek = run(
        "deepseek/deepseek-flash@none",
        {"prompt_tokens": 100, "completion_tokens": 10, "total_tokens": 110, "prompt_cache_hit_tokens": 80},
    )
    assert deepseek.usage.cached_input_tokens == 80
    # thinking counted only in total_tokens is still billed as output
    gemini = run(
        "google/gemini-3.1-flash-lite@minimal",
        {"prompt_tokens": 100, "completion_tokens": 10, "total_tokens": 150},
    )
    assert gemini.usage.output_tokens == 50 and gemini.usage.reasoning_tokens == 40


def test_refusal_is_recorded():
    resp = client_for(
        "openai/gpt-6-luna@none",
        lambda r: httpx.Response(200, json=openai_reply(content=None, refusal="I can't help with that.")),
    ).complete(REQ)
    assert resp.finish_reason == "refusal" and resp.text == "I can't help with that."


@pytest.mark.parametrize(
    "config_id,extra",
    [
        ("openai/gpt-6-luna@none", {"model": "other"}),
        ("anthropic/claude-haiku-5-5@off-low", {"output_config": {"format": {"type": "text"}}}),
    ],
)
def test_extra_body_cannot_override_core_fields(config_id, extra):
    config = get_model(config_id).model_copy(update={"extra_body": extra})
    client = HttpChatClient(config, lambda: "k", clock=fixed_clock(OFF_PEAK), http=httpx.Client())
    with pytest.raises(ValueError, match="may not override"):
        client.complete(REQ)


# --- retries ------------------------------------------------------------------------------------


def test_retries_429_honoring_retry_after():
    calls, sleeps = [], []

    def handler(request):
        calls.append(1)
        if len(calls) < 3:
            return httpx.Response(429, headers={"retry-after": "1.5"}, text="rate limited")
        return httpx.Response(200, json=openai_reply())

    resp = client_for("openai/gpt-6-luna@none", handler, sleeps=sleeps).complete(REQ)
    assert resp.text == '{"n": 1}' and len(calls) == 3 and sleeps == [1.5, 1.5]


@pytest.mark.parametrize(
    "status,text",
    [(401, "invalid api key"), (400, "bad schema"), (429, '{"error": {"code": "insufficient_quota"}}')],
)
def test_fails_fast_on_auth_bad_request_and_quota(status, text):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(status, text=text)

    with pytest.raises(LLMError) as e:
        client_for("openai/gpt-6-luna@none", handler).complete(REQ)
    assert len(calls) == 1 and e.value.status == status and not e.value.retryable


def test_gives_up_after_max_attempts():
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(503, text="overloaded")

    with pytest.raises(LLMError) as e:
        client_for("openai/gpt-6-luna@none", handler).complete(REQ)
    assert len(calls) == 4 and e.value.retryable


# --- cache --------------------------------------------------------------------------------------


def test_cache_record_then_replay(tmp_path):
    luna = get_model("openai/gpt-6-luna@none")
    fake = ScriptedChatClient(['{"n": 1}'], config_id=luna.id)
    first = CachedClient(fake, luna, "record", tmp_path).complete(REQ)
    assert not first.cached and len(fake.requests) == 1
    replayed = CachedClient(fake, luna, "replay", tmp_path).complete(REQ)
    assert replayed.cached and replayed.text == first.text and len(fake.requests) == 1
    again = CachedClient(fake, luna, "record", tmp_path).complete(REQ)  # hit: no new call
    assert again.cached and len(fake.requests) == 1


def test_cache_replay_miss_and_off_mode(tmp_path):
    luna = get_model("openai/gpt-6-luna@none")
    with pytest.raises(CacheMiss):
        CachedClient(ScriptedChatClient([]), luna, "replay", tmp_path).complete(REQ)
    CachedClient(ScriptedChatClient(["{}"]), luna, "off", tmp_path).complete(REQ)
    assert not any(tmp_path.rglob("*.json"))


def test_cache_refresh_always_calls(tmp_path):
    luna = get_model("openai/gpt-6-luna@none")
    fake = ScriptedChatClient(['{"n": 1}', '{"n": 2}'], config_id=luna.id)
    CachedClient(fake, luna, "record", tmp_path).complete(REQ)
    refreshed = CachedClient(fake, luna, "refresh", tmp_path).complete(REQ)
    assert refreshed.text == '{"n": 2}' and not refreshed.cached
    assert CachedClient(fake, luna, "replay", tmp_path).complete(REQ).text == '{"n": 2}'


def test_cache_key_covers_request_and_config():
    luna = get_model("openai/gpt-6-luna@none")
    base = cache_key(luna, REQ)
    assert cache_key(luna, REQ.model_copy(update={"system": "Other JSON."})) != base
    assert cache_key(luna, REQ.model_copy(update={"max_output_tokens": 10})) != base
    low = luna.model_copy(update={"extra_body": {"reasoning_effort": "low"}})
    assert cache_key(low, REQ) != base
    assert cache_key(luna.model_copy(update={"rpm": 1}), REQ) == base  # pacing doesn't change the answer


# --- throttle, env, fake ------------------------------------------------------------------------


def test_throttle_spaces_calls():
    clock, sleeps = [0.0], []

    def sleep(s):
        sleeps.append(s)
        clock[0] += s

    t = Throttle(60, now=lambda: clock[0], sleep=sleep)
    t.wait()
    t.wait()
    clock[0] += 5.0
    t.wait()
    assert sleeps == [1.0]


def test_api_key_from_env_or_dotenv(tmp_path, monkeypatch):
    dotenv = tmp_path / ".env"
    dotenv.write_text('# comment\nA_KEY="from-file"\nEMPTY=\n')
    assert read_dotenv(dotenv) == {"A_KEY": "from-file", "EMPTY": ""}
    monkeypatch.delenv("A_KEY", raising=False)
    assert api_key("A_KEY", dotenv) == "from-file"
    monkeypatch.setenv("A_KEY", "from-env")
    assert api_key("A_KEY", dotenv) == "from-env"
    with pytest.raises(KeyError):
        api_key("EMPTY", dotenv)


def test_scripted_client_runs_out():
    fake = ScriptedChatClient(["{}"])
    fake.complete(REQ)
    with pytest.raises(IndexError):
        fake.complete(REQ)
