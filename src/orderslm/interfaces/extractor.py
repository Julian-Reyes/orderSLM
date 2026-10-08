"""OrderExtractor: the teacher, every student, and the rules baseline implement this.

An extractor returns a *proposal*. `ExtractionResult.output` is None when the
model's text didn't parse or validate; the raw text is kept so the JSON
validity rate and failure examples come from saved outputs.
"""

from typing import Protocol, runtime_checkable

from pydantic import Field, model_validator

from orderslm.schema.common import Strict
from orderslm.schema.conversation import Conversation
from orderslm.schema.extraction import ExtractionOutput
from orderslm.schema.menu import MenuCatalog

from .decision import Usage


class ExtractionRequest(Strict):
    """Never carries the router's label (docs/ARCHITECTURE.md, design rules)."""

    menu: MenuCatalog = Field(description="menu.extractor_view(): no reply-only size facts")
    conversation: Conversation
    draft: ExtractionOutput | None = Field(default=None, description="current draft order state, if any")
    prompt_version: str

    @model_validator(mode="after")
    def _extractor_menu(self) -> "ExtractionRequest":
        if self.menu.has_reply_only_fields():
            raise ValueError("pass menu.extractor_view(): diameter_cm/slices are for the reply layer only")
        return self


class ExtractionResult(Strict):
    extractor: str = Field(description="config id, e.g. openai/gpt-6-luna or local/qwen3.5-0.8b-lora")
    output: ExtractionOutput | None
    raw_text: str
    error: str | None = None
    usage: Usage = Field(default_factory=Usage)
    latency_ms: float = Field(ge=0)
    cost_micros: int = Field(default=0, ge=0)
    cached: bool = False


@runtime_checkable
class OrderExtractor(Protocol):
    @property
    def name(self) -> str: ...

    def extract(self, request: ExtractionRequest) -> ExtractionResult: ...


def parse_model_output(
    extractor: str, raw_text: str, latency_ms: float, usage: Usage | None = None
) -> ExtractionResult:
    """Shared by every model-backed extractor: validate raw JSON text against the schema, never raise."""
    try:
        output = ExtractionOutput.model_validate_json(raw_text)
        error = None
    except ValueError as e:  # pydantic.ValidationError subclasses ValueError
        output, error = None, str(e)
    return ExtractionResult(
        extractor=extractor,
        output=output,
        raw_text=raw_text,
        error=error,
        usage=usage or Usage(),
        latency_ms=latency_ms,
    )
