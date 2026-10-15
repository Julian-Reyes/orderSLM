"""Model config (config/models.json) and cost computation in integer micro-USD.

Costs are computed from the provider's reported usage × the verified price in the config, never
from a model's output. Ported from AgentDesk server/src/llm/config.ts (cost in micro-dollars).
"""

import json
from datetime import UTC, datetime
from functools import cache
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, model_validator

from orderslm.paths import ROOT
from orderslm.schema.common import Strict

from .types import LLMUsage

MODELS_JSON = ROOT / "config" / "models.json"


class Price(Strict):
    """Micro-USD per 1M tokens. A missing cached/cache-write price bills those tokens as input
    (conservative: never under-estimates)."""

    input: int = Field(ge=0)
    output: int = Field(ge=0)
    cached_input: int | None = Field(default=None, ge=0)
    cache_write: int | None = Field(default=None, ge=0)


class OffPeak(Strict):
    """DeepSeek-style time-of-day pricing. Peak windows are [start_hour, end_hour) UTC, Mon–Fri;
    everything else is off-peak. Public holidays count as peak here (over-estimates, never under)."""

    price: Price
    peak_windows_utc_weekdays: list[tuple[int, int]]


class LongContext(Strict):
    threshold_input_tokens: int = Field(gt=0)
    price: Price | None = Field(description="None: not verified; a longer prompt is refused, not guessed")


class ModelConfig(Strict):
    """One callable configuration: a model at one reasoning variant."""

    id: str = Field(pattern=r"^[a-z0-9-]+/[A-Za-z0-9._-]+@[a-z0-9-]+$")
    provider: str
    variant: str
    provider_default: bool = Field(description="this variant behaves like sending no reasoning settings")
    api: Literal["openai_chat", "anthropic_messages"]
    base_url: str
    model: str
    key_env: str
    structured_output: Literal["json_schema", "json_object"]
    max_tokens_param: Literal["max_tokens", "max_completion_tokens"]
    extra_body: dict[str, Any] = Field(default_factory=dict)
    rpm: int = Field(gt=0)
    price: Price
    off_peak: OffPeak | None = None
    long_context: LongContext | None = None
    price_verified: str
    price_source: str

    @model_validator(mode="after")
    def _id_matches(self) -> "ModelConfig":
        if self.id != f"{self.provider}/{self.model}@{self.variant}":
            raise ValueError(f"id {self.id!r} must be provider/model@variant")
        return self

    @property
    def base_id(self) -> str:
        return f"{self.provider}/{self.model}"

    def price_at(self, at: datetime, input_tokens: int) -> Price:
        if at.tzinfo is None:
            raise ValueError("pricing time must be timezone-aware")
        price = self.price
        if self.off_peak is not None and not _in_peak(at, self.off_peak.peak_windows_utc_weekdays):
            price = self.off_peak.price
        if self.long_context and input_tokens > self.long_context.threshold_input_tokens:
            if self.long_context.price is None:
                raise ValueError(
                    f"{self.id}: prompt of {input_tokens} tokens is over "
                    f"{self.long_context.threshold_input_tokens}; long-context price not verified"
                )
            price = self.long_context.price
        return price

    def cost_micros(self, usage: LLMUsage, at: datetime) -> int:
        p = self.price_at(at, usage.input_tokens)
        fresh = usage.input_tokens - usage.cached_input_tokens - usage.cache_write_tokens
        if fresh < 0:
            raise ValueError(f"{self.id}: cached + cache-write tokens exceed input tokens: {usage}")
        cached_price = p.input if p.cached_input is None else p.cached_input
        write_price = p.input if p.cache_write is None else p.cache_write
        total = (
            fresh * p.input
            + usage.cached_input_tokens * cached_price
            + usage.cache_write_tokens * write_price
            + usage.output_tokens * p.output
        )
        return -(-total // 1_000_000)  # ceil: never round a cost down


def _in_peak(at: datetime, windows: list[tuple[int, int]]) -> bool:
    utc = at.astimezone(UTC)
    if utc.weekday() >= 5:
        return False
    return any(start <= utc.hour < end for start, end in windows)


class Variant(Strict):
    name: str = Field(pattern=r"^[a-z0-9-]+$")
    extra_body: dict[str, Any]
    provider_default: bool = False


class ModelEntry(Strict):
    provider: str
    model: str
    api: Literal["openai_chat", "anthropic_messages"]
    base_url: str
    key_env: str
    structured_output: Literal["json_schema", "json_object"]
    max_tokens_param: Literal["max_tokens", "max_completion_tokens"]
    variants: list[Variant] = Field(min_length=1, description="lowest setting first")
    rpm: int
    price: Price
    off_peak: OffPeak | None = None
    long_context: LongContext | None = None
    price_verified: str
    price_source: str

    @model_validator(mode="after")
    def _one_default(self) -> "ModelEntry":
        if sum(v.provider_default for v in self.variants) != 1:
            raise ValueError(f"{self.provider}/{self.model}: exactly one variant must be provider_default")
        return self

    def configs(self) -> list[ModelConfig]:
        shared = self.model_dump(exclude={"variants"})
        return [
            ModelConfig(
                id=f"{self.provider}/{self.model}@{v.name}",
                variant=v.name,
                extra_body=v.extra_body,
                provider_default=v.provider_default,
                **shared,
            )
            for v in self.variants
        ]


class ModelsFile(Strict):
    comment: str = Field(alias="_comment")
    models: list[ModelEntry]


@cache
def _load(path: Path) -> dict[str, ModelConfig]:
    parsed = ModelsFile.model_validate(json.loads(path.read_text()))
    by_id: dict[str, ModelConfig] = {}
    for entry in parsed.models:
        for m in entry.configs():
            if m.id in by_id:
                raise ValueError(f"duplicate model id {m.id}")
            by_id[m.id] = m
    return by_id


def lowest_variants(path: Path = MODELS_JSON) -> list[str]:
    """The first (lowest-reasoning) variant of each model, in config order."""
    seen: dict[str, str] = {}
    for m in _load(path).values():
        seen.setdefault(m.base_id, m.id)
    return list(seen.values())


def load_models(path: Path = MODELS_JSON) -> dict[str, ModelConfig]:
    return dict(_load(path))


def get_model(config_id: str, path: Path = MODELS_JSON) -> ModelConfig:
    models = _load(path)
    if config_id not in models:
        raise KeyError(f"unknown model {config_id!r}; known: {sorted(models)}")
    return models[config_id]
