"""DecisionProvider: one interface for Julia-1, Jev, OpenAI Decisions and the rules baseline.

Per the spec (§11), all three providers accept an input/state plus named
questions of type choice, score or boolean, and return a choice with
probabilities and (for hosted ones) a confidence. This module is OUR
abstraction; it does not describe any provider's wire format. Each adapter
(M7) maps it to the provider's documented API after the contract has been
verified against official docs, and records anything that doesn't map.

Confidence and probabilities are provider-specific and not comparable across
providers without calibration on dev data.
"""

from enum import StrEnum
from typing import Protocol, runtime_checkable

from pydantic import Field, model_validator

from orderslm.schema.common import ID_PATTERN, Strict


class QuestionType(StrEnum):
    choice = "choice"
    score = "score"
    boolean = "boolean"


class Option(Strict):
    id: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=300)


class Question(Strict):
    name: str = Field(pattern=ID_PATTERN)
    type: QuestionType
    prompt: str = Field(min_length=1)
    options: list[Option] = Field(default_factory=list)

    @model_validator(mode="after")
    def _options(self) -> "Question":
        if self.type is QuestionType.choice:
            if len(self.options) < 2:
                raise ValueError(f"{self.name}: a choice question needs at least 2 options")
            ids = [o.id for o in self.options]
            if len(ids) != len(set(ids)):
                raise ValueError(f"{self.name}: duplicate option ids")
        elif self.options:
            raise ValueError(f"{self.name}: only choice questions take options")
        return self


class DecisionRequest(Strict):
    request_id: str
    input: str = Field(min_length=1, description="the state: message + context, rendered as text")
    questions: list[Question] = Field(min_length=1)
    prompt_version: str

    @model_validator(mode="after")
    def _unique(self) -> "DecisionRequest":
        names = [q.name for q in self.questions]
        if len(names) != len(set(names)):
            raise ValueError("duplicate question names")
        return self


class Answer(Strict):
    name: str
    type: QuestionType
    choice: str | None = None
    score: float | None = None
    boolean: bool | None = None
    confidence: float | None = Field(
        default=None, ge=0, le=1, description="provider-specific; not comparable"
    )
    probabilities: dict[str, float] | None = None
    refused: bool = False

    @model_validator(mode="after")
    def _shape(self) -> "Answer":
        if self.refused:
            if any(v is not None for v in (self.choice, self.score, self.boolean)):
                raise ValueError(f"{self.name}: a refused answer carries no value")
            return self
        value = {
            QuestionType.choice: self.choice,
            QuestionType.score: self.score,
            QuestionType.boolean: self.boolean,
        }
        if value[self.type] is None:
            raise ValueError(f"{self.name}: {self.type.value} answer has no {self.type.value} value")
        if self.probabilities is not None and any(not 0 <= p <= 1 for p in self.probabilities.values()):
            raise ValueError(f"{self.name}: probabilities must be in [0, 1]")
        return self


class Usage(Strict):
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)


class DecisionResponse(Strict):
    provider: str
    model: str
    answers: dict[str, Answer]
    usage: Usage = Field(default_factory=Usage)
    latency_ms: float = Field(ge=0)
    cost_micros: int = Field(default=0, ge=0, description="1e-6 USD, computed from usage and config pricing")
    cached: bool = False


class DecisionError(Exception):
    """Transport or contract failure (bad response, auth, unreachable). Not a refusal."""


@runtime_checkable
class DecisionProvider(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def max_options(self) -> int | None:
        """Most options one choice question may have; None = no documented limit."""
        ...

    def decide(self, request: DecisionRequest) -> DecisionResponse: ...


def check_against_limits(provider: DecisionProvider, request: DecisionRequest) -> None:
    """Fail before sending a request a provider can't accept."""
    limit = provider.max_options
    if limit is None:
        return
    for q in request.questions:
        if q.type is QuestionType.choice and len(q.options) > limit:
            raise DecisionError(
                f"{provider.name}: question {q.name!r} has {len(q.options)} options, limit {limit}"
            )


def validate_response(request: DecisionRequest, response: DecisionResponse) -> None:
    """Every question answered, with the right type, and choices from the offered options."""
    for q in request.questions:
        a = response.answers.get(q.name)
        if a is None:
            raise DecisionError(f"{response.provider}: no answer for {q.name!r}")
        if a.type is not q.type:
            raise DecisionError(
                f"{response.provider}: {q.name!r} answered as {a.type.value}, asked {q.type.value}"
            )
        if q.type is QuestionType.choice and not a.refused and a.choice not in {o.id for o in q.options}:
            raise DecisionError(f"{response.provider}: {q.name!r} chose {a.choice!r}, not an offered option")
    extra = set(response.answers) - {q.name for q in request.questions}
    if extra:
        raise DecisionError(f"{response.provider}: answers for questions not asked: {sorted(extra)}")
