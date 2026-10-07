"""A labeled conversation: the file format for samples, dev and test sets.

Gold extraction is the order state after the last message. Gold routing covers
every customer message. Scenario tags drive coverage reports and eval slices.
"""

from enum import StrEnum

from pydantic import Field, model_validator

from .common import ID_PATTERN, Strict
from .conversation import Conversation, Role
from .extraction import ExtractionOutput
from .routing import MessageRouting


class Scenario(StrEnum):
    simple_order = "simple_order"
    multi_message_order = "multi_message_order"
    correction = "correction"
    correction_after_confirmation = "correction_after_confirmation"
    cancellation = "cancellation"
    missing_info = "missing_info"
    two_requests = "two_requests"
    off_menu = "off_menu"
    ambiguous_reference = "ambiguous_reference"
    contextual_yes = "contextual_yes"
    half_and_half = "half_and_half"
    combo = "combo"
    menu_question = "menu_question"
    delivery_question = "delivery_question"
    payment_question = "payment_question"
    status_question = "status_question"
    order_problem = "order_problem"
    refund_request = "refund_request"
    payment_claim = "payment_claim"
    human_request = "human_request"
    small_talk = "small_talk"
    out_of_scope = "out_of_scope"
    unclear_message = "unclear_message"


class WritingStyle(StrEnum):
    clean = "clean"
    texting = "texting"  # abbreviations, no punctuation
    rapid_fire = "rapid_fire"  # many short messages
    shouty = "shouty"  # ALL CAPS, !!!
    emoji = "emoji"


class AnnotatedConversation(Strict):
    conversation: Conversation
    scenarios: list[Scenario] = Field(min_length=1)
    style: WritingStyle
    gold_extraction: ExtractionOutput | None = Field(
        description="null when the conversation has no order at all (pure status question, small talk)"
    )
    gold_routing: list[MessageRouting]
    annotator: str = Field(min_length=1)
    card_id: str | None = Field(
        default=None, pattern=ID_PATTERN, description="scenario card it was written from (Source A)"
    )
    annotation_notes: str | None = None

    @model_validator(mode="after")
    def _covers_customer_messages(self) -> "AnnotatedConversation":
        routed = [r.message_index for r in self.gold_routing]
        customer = self.conversation.customer_indices()
        if routed != customer:
            raise ValueError(
                f"gold_routing must cover each customer message once, in order: {customer}, got {routed}"
            )
        if (self.conversation.source.value == "claude_written") != (self.card_id is not None):
            raise ValueError("card_id is required for claude_written conversations and only for them")
        roles = {m.index: m.role for m in self.conversation.messages}
        if self.gold_extraction is not None:
            for path, ev in self.gold_extraction.iter_evidence():
                if ev.message_index not in roles:
                    raise ValueError(f"{path}: evidence points at missing message {ev.message_index}")
        return self


# Re-exported for callers that only need to know who wrote a message.
__all__ = ["AnnotatedConversation", "Role", "Scenario", "WritingStyle"]
