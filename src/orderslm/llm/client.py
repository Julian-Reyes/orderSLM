"""HTTP chat clients: one for OpenAI-compatible APIs (OpenAI, Gemini, DeepSeek), one for Anthropic.

Ported from AgentDesk server/src/llm/openai-compatible.ts (plain HTTP, retry 429/5xx honoring
Retry-After, fail fast on exhausted quota, cost in micro-dollars). Tool-call repair is not ported:
OrderSLM makes single-shot structured calls.

Request/response contracts were checked against each provider's docs on 2026-10-15:
- OpenAI Chat Completions: response_format {type: json_schema, json_schema: {name, schema, strict}};
  max_completion_tokens (max_tokens is deprecated); usage.prompt_tokens_details.cached_tokens and
  completion_tokens_details.reasoning_tokens; message.refusal.
- Gemini OpenAI-compatible endpoint (base .../v1beta/openai): bearer key, reasoning_effort. Whether
  json_schema is enforced there and how thinking tokens are counted are not stated in the docs; the
  smoke test (orderslm.llm.smoke) checks both on a live call.
- DeepSeek: response_format json_object only (prompt must say "json" and show the format);
  usage.prompt_cache_hit_tokens; thinking {type: disabled}.
- Anthropic Messages: output_config.format {type: json_schema, schema} (no beta header);
  stop_reason "refusal" / "max_tokens"; usage cache_read_input_tokens / cache_creation_input_tokens.
"""

import time
from collections.abc import Callable
from typing import Any

import httpx

from orderslm.domain.clock import Clock

from .config import ModelConfig
from .types import ChatRequest, ChatResponse, LLMError, LLMUsage

ANTHROPIC_VERSION = "2023-06-01"
RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504, 529}
QUOTA_MARKERS = ("insufficient_quota", "insufficient balance", "credit balance is too low")
MAX_RETRY_WAIT_S = 60.0


class HttpChatClient:
    def __init__(
        self,
        config: ModelConfig,
        key: Callable[[], str],
        *,
        clock: Clock,
        http: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
        max_attempts: int = 4,
        timeout_s: float = 120.0,
    ):
        self._config = config
        self._key = key  # looked up on first real call, so replay runs need no key
        self._clock = clock
        self._http = http or httpx.Client(timeout=timeout_s)
        self._sleep = sleep
        self._max_attempts = max_attempts

    @property
    def config_id(self) -> str:
        return self._config.id

    def complete(self, request: ChatRequest) -> ChatResponse:
        c = self._config
        if c.api == "openai_chat":
            url, body = f"{c.base_url}/chat/completions", openai_body(c, request)
            headers = {"Authorization": f"Bearer {self._key()}"}
        else:
            url, body = f"{c.base_url}/messages", anthropic_body(c, request)
            headers = {"x-api-key": self._key(), "anthropic-version": ANTHROPIC_VERSION}

        for attempt in range(1, self._max_attempts + 1):
            at = self._clock()
            started = time.perf_counter()
            try:
                resp = self._http.post(url, json=body, headers=headers)
            except httpx.TransportError as e:
                if attempt == self._max_attempts:
                    raise LLMError(c.id, f"network error: {e!r}", retryable=True) from e
                self._sleep(_backoff(attempt, None))
                continue
            latency_ms = (time.perf_counter() - started) * 1000
            if resp.status_code == 200:
                data = resp.json()
                parse = parse_openai if c.api == "openai_chat" else parse_anthropic
                text, finish, model, usage = parse(data)
                return ChatResponse(
                    config_id=c.id,
                    model=model or c.model,
                    text=text,
                    finish_reason=finish,
                    usage=usage,
                    latency_ms=latency_ms,
                    cost_micros=c.cost_micros(usage, at),
                    at=at.isoformat(),
                    raw_usage=data.get("usage") or {},
                )
            detail = resp.text[:500]
            quota = any(m in detail.lower() for m in QUOTA_MARKERS)
            retryable = resp.status_code in RETRYABLE_STATUS and not quota
            if not retryable or attempt == self._max_attempts:
                why = "quota/balance exhausted" if quota else f"HTTP {resp.status_code}"
                raise LLMError(c.id, f"{why}: {detail}", status=resp.status_code, retryable=retryable)
            self._sleep(_backoff(attempt, resp.headers.get("retry-after")))
        raise AssertionError("unreachable")


def _backoff(attempt: int, retry_after: str | None) -> float:
    if retry_after:
        try:
            return min(max(float(retry_after), 0.0), MAX_RETRY_WAIT_S)
        except ValueError:
            pass  # an HTTP date; fall back to exponential
    return min(2.0**attempt, MAX_RETRY_WAIT_S)


def _merge(config: ModelConfig, body: dict[str, Any]) -> dict[str, Any]:
    clash = set(body) & set(config.extra_body)
    if clash:
        raise ValueError(f"{config.id}: extra_body may not override {sorted(clash)}")
    return {**body, **config.extra_body}


def openai_body(config: ModelConfig, request: ChatRequest) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": config.model,
        "messages": [{"role": "system", "content": request.system}]
        + [m.model_dump() for m in request.messages],
        config.max_tokens_param: request.max_output_tokens,
    }
    if request.json_schema is not None:
        if config.structured_output == "json_schema":
            body["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": request.schema_name, "schema": request.json_schema, "strict": True},
            }
        else:
            prompt = request.system + "".join(m.content for m in request.messages)
            if "json" not in prompt.lower():
                raise ValueError(
                    f"{config.id} has JSON-object mode only: the prompt must mention JSON and show "
                    "the format (the client never edits the prompt)"
                )
            body["response_format"] = {"type": "json_object"}
    return _merge(config, body)


def anthropic_body(config: ModelConfig, request: ChatRequest) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": config.model,
        "system": request.system,
        "messages": [m.model_dump() for m in request.messages],
        "max_tokens": request.max_output_tokens,
    }
    if request.json_schema is not None:
        body["output_config"] = {"format": {"type": "json_schema", "schema": request.json_schema}}
    return _merge(config, body)


def parse_openai(data: dict[str, Any]) -> tuple[str, str, str, LLMUsage]:
    choice = data["choices"][0]
    message = choice.get("message") or {}
    text = message.get("content") or ""
    finish = choice.get("finish_reason") or ""
    if message.get("refusal"):
        text, finish = message["refusal"], "refusal"
    u = data.get("usage") or {}
    prompt = int(u.get("prompt_tokens") or 0)
    completion = int(u.get("completion_tokens") or 0)
    if "prompt_cache_hit_tokens" in u:  # DeepSeek
        cached = int(u["prompt_cache_hit_tokens"] or 0)
    else:
        cached = int((u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0)
    reasoning = int((u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0)
    output = completion
    # If a provider reports thinking only in total_tokens (not in completion_tokens), bill it as
    # output anyway: the smoke test records which case each provider is in.
    total = u.get("total_tokens")
    if total is not None and int(total) > prompt + completion:
        hidden = int(total) - prompt - completion
        output += hidden
        reasoning = max(reasoning, hidden)
    usage = LLMUsage(
        input_tokens=prompt, cached_input_tokens=cached, output_tokens=output, reasoning_tokens=reasoning
    )
    return text, finish, data.get("model") or "", usage


def parse_anthropic(data: dict[str, Any]) -> tuple[str, str, str, LLMUsage]:
    text = "".join(b.get("text", "") for b in data.get("content") or [] if b.get("type") == "text")
    u = data.get("usage") or {}
    read = int(u.get("cache_read_input_tokens") or 0)
    write = int(u.get("cache_creation_input_tokens") or 0)
    usage = LLMUsage(
        input_tokens=int(u.get("input_tokens") or 0) + read + write,
        cached_input_tokens=read,
        cache_write_tokens=write,
        output_tokens=int(u.get("output_tokens") or 0),
    )
    return text, data.get("stop_reason") or "", data.get("model") or "", usage
