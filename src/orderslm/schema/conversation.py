"""Conversations: the input every extractor and router sees."""

from datetime import datetime
from enum import StrEnum

from pydantic import Field, model_validator

from .common import ID_PATTERN, Strict


class Role(StrEnum):
    customer = "customer"
    business = "business"


class Split(StrEnum):
    """Which dataset a conversation belongs to. `test` is sealed (see orderslm.paths)."""

    sample = "sample"  # docs/examples in data/samples; never used for scoring
    dev = "dev"
    test = "test"
    synthetic = "synthetic"
    benchmark = "benchmark"  # third-party eval set (PIZZA), data/external only; evaluation-only


class Source(StrEnum):
    human = "human"
    synthetic = "synthetic"


class Message(Strict):
    index: int = Field(ge=0)
    role: Role
    text: str = Field(min_length=1, max_length=2000)
    sent_at: datetime


class Conversation(Strict):
    id: str = Field(pattern=ID_PATTERN)
    business_id: str = Field(pattern=ID_PATTERN)
    language: str = Field(
        default="en", pattern=r"^[a-z]{2}(-[A-Z]{2})?$", description="BCP-47, e.g. en, pt-BR"
    )
    split: Split
    source: Source
    messages: list[Message] = Field(min_length=1)

    @model_validator(mode="after")
    def _ordered(self) -> "Conversation":
        for i, m in enumerate(self.messages):
            if m.index != i:
                raise ValueError(f"message indices must be 0..n-1 in order; position {i} has index {m.index}")
            if m.sent_at.tzinfo is None:
                raise ValueError(f"message {i}: sent_at must be timezone-aware")
            if i and m.sent_at < self.messages[i - 1].sent_at:
                raise ValueError(f"message {i} is earlier than message {i - 1}")
        if not any(m.role is Role.customer for m in self.messages):
            raise ValueError("a conversation needs at least one customer message")
        return self

    def customer_indices(self) -> list[int]:
        return [m.index for m in self.messages if m.role is Role.customer]
