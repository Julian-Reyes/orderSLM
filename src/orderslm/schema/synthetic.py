"""Synthetic training chats (spec §7, M4): the scenario card a chat is written from, the chat, and its label.

The cards are planned by code from (menu × persona × scenario × writing style), independently of Source A: no
Source A card, chat or persona list feeds them. A card names the order the chat must end with, so the card can be
compared with the teacher's label (a free cross-check for the label audit, spec §11d).
"""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from .annotation import Scenario, WritingStyle
from .common import ID_PATTERN, SYNTH_SCHEMA_VERSION, Strict
from .conversation import Conversation, Role, Source, Split
from .extraction import ExtractionOutput
from .label import MessageIntent
from .routing import RouterLabel


class SynthFeature(StrEnum):
    typos = "typos"
    abbreviations = "abbreviations"
    emoji = "emoji"
    burst = "burst"  # several short messages in a row
    all_caps = "all_caps"
    number_words = "number_words"  # "two", "a couple"
    no_punctuation = "no_punctuation"


class PlannedItem(Strict):
    """One line of the order a card asks for. Exactly one of menu_item_id, halves, off_menu_text."""

    menu_item_id: str | None = Field(default=None, pattern=ID_PATTERN)
    halves: list[str] | None = Field(default=None, min_length=2, max_length=2, description="pizza ids")
    off_menu_text: str | None = Field(default=None, min_length=1, description="a dish the menu doesn't have")
    quantity: int = Field(ge=1, le=20)
    variant_id: str | None = Field(
        default=None, pattern=ID_PATTERN, description="null = customer doesn't say"
    )
    remove: list[str] = Field(default_factory=list, description="modifier ids")
    add: list[str] = Field(default_factory=list, description="modifier ids")
    substitute: dict[str, str] = Field(default_factory=dict, description="modifier removed → modifier added")
    combo: dict[str, str] = Field(default_factory=dict, description="slot id → item id")

    @model_validator(mode="after")
    def _one(self) -> "PlannedItem":
        if sum(x is not None for x in (self.menu_item_id, self.halves, self.off_menu_text)) != 1:
            raise ValueError("exactly one of menu_item_id, halves, off_menu_text")
        return self


class SynthCard(Strict):
    schema_version: Literal["synth@0.1"] = SYNTH_SCHEMA_VERSION
    id: str = Field(pattern=ID_PATTERN)
    generator: str = Field(description="config id of the model that writes the chat")
    business_id: str = Field(pattern=ID_PATTERN)
    scenario: Scenario
    extras: list[str] = Field(default_factory=list, description="overlays: greets_first, asks_menu_mid_order")
    expected_labels: list[RouterLabel] = Field(min_length=1)
    style: WritingStyle
    features: list[SynthFeature]
    persona: str
    customer_messages: int = Field(ge=1, le=12)
    fulfillment: Literal["delivery", "pickup", "unstated", "not_applicable"]
    payment: Literal["card", "cash", "unstated", "not_applicable"]
    customer_name: str | None = None
    address: str | None = Field(default=None, description="made-up delivery address, picked by code")
    items: list[PlannedItem] = Field(default_factory=list, description="the order the chat ends with")
    first_ask: PlannedItem | None = Field(
        default=None, description="what the customer asks for first, then replaces (corrections)"
    )
    brief: str = Field(min_length=1)
    start_at: datetime

    @property
    def builds_order(self) -> bool:
        return bool(self.items)


class GeneratedMessage(Strict):
    role: Role
    text: str = Field(min_length=1, max_length=2000)


class GeneratedChat(Strict):
    """What the generator outputs."""

    messages: list[GeneratedMessage] = Field(min_length=1, max_length=30)


class SyntheticConversation(Strict):
    schema_version: Literal["synth@0.1"] = SYNTH_SCHEMA_VERSION
    conversation: Conversation
    card_id: str = Field(pattern=ID_PATTERN)
    generator: str
    generator_prompt_version: str
    repairs: list[str] = Field(default_factory=list, description="fixes code made to the generated chat")

    @model_validator(mode="after")
    def _synthetic(self) -> "SyntheticConversation":
        c = self.conversation
        if c.split is not Split.synthetic or c.source is not Source.synthetic:
            raise ValueError("a synthetic conversation has split and source 'synthetic'")
        return self


class LabeledConversation(Strict):
    """The teacher's label after finalize. `extraction` is null when the chat has no order (no items), like gold."""

    schema_version: Literal["synth@0.1"] = SYNTH_SCHEMA_VERSION
    conversation_id: str = Field(pattern=ID_PATTERN)
    teacher: str
    label_prompt_version: str
    finalize_version: str
    intents: list[MessageIntent]
    extraction: ExtractionOutput | None
