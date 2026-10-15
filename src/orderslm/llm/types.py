"""Request/response types shared by every chat client, the cache and the fake."""

from typing import Any, Literal, Protocol

from pydantic import Field

from orderslm.schema.common import Strict


class ChatMessage(Strict):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(Strict):
    """One single-shot call. The prompt is passed as-is: clients never add text to it, so every
    provider sees the identical prompt (spec §8). Where a provider has no schema-constrained mode
    (DeepSeek: json_object only), the prompt itself must describe the JSON."""

    system: str
    messages: list[ChatMessage] = Field(min_length=1)
    json_schema: dict[str, Any] | None = None
    schema_name: str = Field(default="output", pattern=r"^[A-Za-z0-9_-]{1,64}$")
    max_output_tokens: int = Field(default=2048, gt=0)


class LLMUsage(Strict):
    """Normalized across providers. input_tokens counts the whole prompt, including cache reads and
    writes; output_tokens counts everything billed as output, including reasoning."""

    input_tokens: int = Field(default=0, ge=0)
    cached_input_tokens: int = Field(default=0, ge=0)
    cache_write_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    reasoning_tokens: int = Field(default=0, ge=0)


class ChatResponse(Strict):
    config_id: str
    model: str = Field(description="model name the provider reports, if any")
    text: str
    finish_reason: str = Field(description="provider value; 'refusal' when the model refused")
    usage: LLMUsage
    latency_ms: float = Field(ge=0)
    cost_micros: int = Field(ge=0, description="1e-6 USD for the original call, from usage × config price")
    at: str = Field(description="ISO time of the original call (prices can depend on it)")
    cached: bool = Field(default=False, description="replayed from .llm-cache: this call cost $0")
    raw_usage: dict[str, Any] = Field(default_factory=dict, description="provider's usage object, verbatim")


class LLMError(Exception):
    """Transport/provider failure (not a business outcome). `retryable` is False for auth errors,
    bad requests and exhausted quotas, which fail fast."""

    def __init__(self, config_id: str, message: str, *, status: int | None = None, retryable: bool = False):
        super().__init__(f"{config_id}: {message}")
        self.config_id = config_id
        self.status = status
        self.retryable = retryable


class ChatClient(Protocol):
    @property
    def config_id(self) -> str: ...

    def complete(self, request: ChatRequest) -> ChatResponse: ...
