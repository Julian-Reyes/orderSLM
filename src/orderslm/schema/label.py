"""What a model outputs for training labels (M4; Julian, 2026-10-16). See docs/SCHEMA.md, "Model output".

`ModelOrder` is the order *facts* a model reads from the text: ExtractionOutput without `missing_or_ambiguous`
and `clarification_question`, which code computes (core/finalize). The only judgments about missing information
that need the text stay with the model, as `ambiguity_flags`:

- `item_menu_match`: an unmatched item that fits several menu items ("a burger" at a place with three burgers),
  as opposed to one that is off the menu;
- `item_variant`: a size or flavor the customer stated unclearly, as opposed to not at all.

`TeacherLabel` is the teacher's label for a whole chat: the router intent of every customer message (spec §4, §7)
and the order after the last message. `StudentOutput` is what the trained student outputs for a chat so far:
the order plus the intent of the latest customer message (spec §4).

ExtractionOutput (schema/extraction.py) is unchanged: it is the finalized order that gold, scoring and the app
use. `finalize_order` turns a ModelOrder into one.
"""

from typing import Literal

from pydantic import Field, model_validator

from .common import LABEL_SCHEMA_VERSION, STUDENT_SCHEMA_VERSION, Strict
from .extraction import (
    Address,
    CustomerDecision,
    CustomerName,
    Fulfillment,
    FulfillmentMethod,
    ItemProposal,
    Note,
    Payment,
    SlotState,
)
from .routing import RouterLabel


class AmbiguityFlag(Strict):
    field: Literal["item_menu_match", "item_variant"]
    line_id: str = Field(pattern=r"^L[0-9]+$")


class ModelOrder(Strict):
    items: list[ItemProposal] = Field(default_factory=list)
    fulfillment: Fulfillment
    address: Address
    payment: Payment
    customer_name: CustomerName
    customer_decision: CustomerDecision = Field(default_factory=CustomerDecision)
    notes: list[Note] = Field(default_factory=list)
    ambiguity_flags: list[AmbiguityFlag] = Field(default_factory=list)

    @model_validator(mode="after")
    def _consistency(self) -> "ModelOrder":
        lines = {i.line_id: i for i in self.items}
        if len(lines) != len(self.items):
            raise ValueError("items: duplicate line_id")
        for f in self.ambiguity_flags:
            line = lines.get(f.line_id)
            if line is None:
                raise ValueError(f"ambiguity flag refers to unknown line {f.line_id}")
            if f.field == "item_menu_match" and line.unmatched_text is None:
                raise ValueError(f"{f.line_id}: item_menu_match flag only on a line with unmatched_text")
            if f.field == "item_variant" and (line.variant_id is not None or line.unmatched_text is not None):
                raise ValueError(f"{f.line_id}: item_variant flag only on a menu line with no variant_id")
        method = self.fulfillment.method
        if method is FulfillmentMethod.pickup and self.address.state is not SlotState.not_applicable:
            raise ValueError("address must be not_applicable for pickup")
        if method is not FulfillmentMethod.pickup and self.address.state is SlotState.not_applicable:
            raise ValueError("address is only not_applicable for pickup")
        return self


class MessageIntent(Strict):
    """The router label of one customer message, in the context of the chat before it."""

    message_index: int = Field(ge=0)
    primary: RouterLabel
    secondary: RouterLabel | None = Field(default=None, description="only for a message with two requests")

    @model_validator(mode="after")
    def _labels(self) -> "MessageIntent":
        if self.secondary is not None:
            if self.secondary == self.primary:
                raise ValueError("secondary label must differ from primary")
            if RouterLabel.UNKNOWN in (self.primary, self.secondary):
                raise ValueError("UNKNOWN can't be combined with another label")
        return self


class TeacherLabel(Strict):
    schema_version: Literal["label@0.1"] = LABEL_SCHEMA_VERSION
    intents: list[MessageIntent] = Field(min_length=1, description="one per customer message, in order")
    order: ModelOrder


class StudentIntent(Strict):
    primary: RouterLabel
    secondary: RouterLabel | None = None


class StudentOutput(Strict):
    """Spec §4: the order so far plus the intent of the latest customer message."""

    schema_version: Literal["student@0.1"] = STUDENT_SCHEMA_VERSION
    intent: StudentIntent
    order: ModelOrder
