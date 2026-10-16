"""Hosted decision providers behind the DecisionProvider interface: TypeSafe Jev and OpenAI Decisions.

Wire formats are from the official docs, checked 2026-10-16 (docs/PROVIDERS.md):

- Jev: POST /v1/systemone {model, state, questions: {name: {type, instructions, criteria}}} → {model, answers:
  {name: {choice, probabilities: {option: p}, confidence} | {noul: p}}, usage: {input_tokens, output_tokens}}.
- OpenAI Decisions: POST /v1/decisions {model, input, questions: [{type, name, instructions, choices: [{value,
  description}]}]} → {answers: [{name, type, choice, probabilities: [{value, probability}], confidence} |
  {name, type: "predicate", probability} | {name, type: "refusal"}]}.

Our `boolean` question is Jev's `noul` and OpenAI's `predicate`; the answer is true when P(true) ≥ 0.5 and keeps the
probability. Score questions are not used yet and are refused here rather than guessed. Responses go through a
record/replay cache (LLM_CACHE, same modes as the chat cache) under .llm-cache/decisions/. Cost = input tokens ×
the configured price (both bill input only); a price without `price_verified` makes the cost an estimate.
"""

import hashlib
import json
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

import httpx

from orderslm.interfaces.decision import (
    Answer,
    DecisionError,
    DecisionRequest,
    DecisionResponse,
    QuestionType,
    Usage,
    check_against_limits,
    validate_response,
)
from orderslm.llm.cache import CACHE_DIR, CacheMode
from orderslm.llm.env import api_key
from orderslm.llm.factory import cache_mode_from_env
from orderslm.llm.throttle import Throttle
from orderslm.paths import ROOT
from orderslm.schema.common import Strict

CONFIG = ROOT / "config" / "decision_providers.json"
RETRY_STATUS = {429, 500, 502, 503, 504, 529}


class HostedConfig(Strict):
    name: str
    api: Literal["typesafe_systemone", "openai_decisions"]
    url: str
    model: str
    key_env: str
    max_options: int | None
    rpm: int
    price_input_per_1m: int
    price_verified: str | None
    price_source: str


def load_hosted() -> dict[str, HostedConfig]:
    data = json.loads(CONFIG.read_text())
    return {p["name"]: HostedConfig.model_validate(p) for p in data["providers"]}


# ---------------------------------------------------------------- wire mapping


def to_wire(config: HostedConfig, request: DecisionRequest) -> dict[str, Any]:
    for q in request.questions:
        if q.type is QuestionType.score:
            raise DecisionError(f"{config.name}: score questions are not supported by this adapter yet")
    if config.api == "typesafe_systemone":
        questions: dict[str, Any] = {}
        for q in request.questions:
            if q.type is QuestionType.choice:
                questions[q.name] = {
                    "type": "choice",
                    "instructions": q.prompt,
                    "criteria": {o.id: o.description for o in q.options},
                }
            else:
                questions[q.name] = {"type": "noul", "instructions": q.prompt}
        return {"model": config.model, "state": request.input, "questions": questions}
    wire_questions = []
    for q in request.questions:
        if q.type is QuestionType.choice:
            wire_questions.append(
                {
                    "type": "choice",
                    "name": q.name,
                    "instructions": q.prompt,
                    "choices": [{"value": o.id, "description": o.description} for o in q.options],
                }
            )
        else:
            wire_questions.append({"type": "predicate", "name": q.name, "instructions": q.prompt})
    return {"model": config.model, "input": request.input, "questions": wire_questions}


def from_wire(
    config: HostedConfig, request: DecisionRequest, body: dict[str, Any]
) -> tuple[dict[str, Answer], Usage, str]:
    types = {q.name: q.type for q in request.questions}
    answers: dict[str, Answer] = {}
    if config.api == "typesafe_systemone":
        for name, a in (body.get("answers") or {}).items():
            if name not in types:
                raise DecisionError(f"{config.name}: answer for unknown question {name!r}")
            if types[name] is QuestionType.choice:
                answers[name] = Answer(
                    name=name,
                    type=QuestionType.choice,
                    choice=a.get("choice"),
                    confidence=a.get("confidence"),
                    probabilities=a.get("probabilities"),
                )
            else:
                p = float(a["noul"])
                answers[name] = Answer(
                    name=name,
                    type=QuestionType.boolean,
                    boolean=p >= 0.5,
                    probabilities={"true": p, "false": 1 - p},
                )
    else:
        for a in body.get("answers") or []:
            name = a.get("name")
            if name not in types:
                raise DecisionError(f"{config.name}: answer for unknown question {name!r}")
            if a.get("type") == "refusal":
                answers[name] = Answer(name=name, type=types[name], refused=True)
            elif types[name] is QuestionType.choice:
                answers[name] = Answer(
                    name=name,
                    type=QuestionType.choice,
                    choice=a.get("choice"),
                    confidence=a.get("confidence"),
                    probabilities={p["value"]: p["probability"] for p in a.get("probabilities") or []},
                )
            else:
                p = float(a["probability"])
                answers[name] = Answer(
                    name=name,
                    type=QuestionType.boolean,
                    boolean=p >= 0.5,
                    probabilities={"true": p, "false": 1 - p},
                )
    usage = body.get("usage") or {}
    return (
        answers,
        Usage(
            input_tokens=int(usage.get("input_tokens") or 0),
            output_tokens=int(usage.get("output_tokens") or 0),
        ),
        str(body.get("model") or config.model),
    )


# ---------------------------------------------------------------- the provider


class HostedDecisionProvider:
    def __init__(
        self,
        config: HostedConfig,
        *,
        cache_mode: CacheMode | None = None,
        cache_dir: Path = CACHE_DIR / "decisions",
        http: httpx.Client | None = None,
        key: Callable[[], str] | None = None,
        sleep: Callable[[float], None] = time.sleep,
        max_retries: int = 4,
    ):
        self._config = config
        self._mode = cache_mode or cache_mode_from_env()
        self._dir = cache_dir / config.name
        self._http = http or httpx.Client(timeout=120)
        self._key = key or (lambda: api_key(config.key_env))
        self._sleep = sleep
        self._retries = max_retries
        self._throttle = Throttle(config.rpm)

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def max_options(self) -> int | None:
        return self._config.max_options

    @property
    def config(self) -> HostedConfig:
        return self._config

    def cache_key(self, request: DecisionRequest) -> str:
        material = {
            "provider": self._config.model_dump(include={"name", "api", "url", "model"}),
            "wire": to_wire(self._config, request),
        }
        return hashlib.sha256(
            json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def cost_micros(self, usage: Usage) -> int:
        return -(-usage.input_tokens * self._config.price_input_per_1m // 1_000_000)

    def decide(self, request: DecisionRequest) -> DecisionResponse:
        check_against_limits(self, request)
        path = self._dir / f"{self.cache_key(request)}.json"
        if self._mode in ("record", "replay") and path.exists():
            saved = json.loads(path.read_text())
            response = DecisionResponse.model_validate(saved["response"]).model_copy(update={"cached": True})
            validate_response(request, response)
            return response
        if self._mode == "replay":
            raise DecisionError(f"{self.name}: cache miss in replay mode")
        response = self._call(request)
        if self._mode != "off":
            self._dir.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"response": response.model_dump(mode="json")}, indent=1) + "\n")
        return response

    def _call(self, request: DecisionRequest) -> DecisionResponse:
        wire = to_wire(self._config, request)
        for attempt in range(self._retries + 1):
            self._throttle.wait()
            started = time.monotonic()
            try:
                r = self._http.post(
                    self._config.url, json=wire, headers={"Authorization": f"Bearer {self._key()}"}
                )
            except httpx.HTTPError as e:
                if attempt == self._retries:
                    raise DecisionError(f"{self.name}: {type(e).__name__}") from e
                self._sleep(2**attempt)
                continue
            latency = (time.monotonic() - started) * 1000
            if r.status_code in RETRY_STATUS and attempt < self._retries:
                retry_after = r.headers.get("retry-after")
                self._sleep(float(retry_after) if retry_after and retry_after.isdigit() else 2**attempt)
                continue
            if r.status_code != 200:
                raise DecisionError(f"{self.name}: HTTP {r.status_code}: {r.text[:300]}")
            answers, usage, model = from_wire(self._config, request, r.json())
            response = DecisionResponse(
                provider=self.name,
                model=model,
                answers=answers,
                usage=usage,
                latency_ms=latency,
                cost_micros=self.cost_micros(usage),
            )
            validate_response(request, response)
            return response
        raise DecisionError(f"{self.name}: retries exhausted")


def make_provider(name: str, **kwargs: Any) -> HostedDecisionProvider:
    return HostedDecisionProvider(load_hosted()[name], **kwargs)
