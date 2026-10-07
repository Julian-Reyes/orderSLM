"""Router taxonomy V1 (spec §5, docs/TAXONOMY.md).

The label descriptions here are the single source of truth: the identical
wording goes to every decision provider (Julia-1, Jev, OpenAI Decisions) and to
the annotation tool. Julia-1 limits each option to 48 tokens, so descriptions
stay short; tests enforce a conservative word budget until the real tokenizer
check runs in M7.
"""

from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from .common import ROUTER_SCHEMA_VERSION, Strict


class RouterLabel(StrEnum):
    PLACE_ORDER = "PLACE_ORDER"
    MODIFY_ORDER = "MODIFY_ORDER"
    CANCEL_ORDER = "CANCEL_ORDER"
    CONFIRM_ORDER = "CONFIRM_ORDER"
    MENU_QUESTION = "MENU_QUESTION"
    DELIVERY_QUESTION = "DELIVERY_QUESTION"
    PAYMENT_QUESTION = "PAYMENT_QUESTION"
    PAYMENT_CLAIM = "PAYMENT_CLAIM"
    ORDER_STATUS = "ORDER_STATUS"
    ORDER_PROBLEM = "ORDER_PROBLEM"
    REFUND_REQUEST = "REFUND_REQUEST"
    HUMAN_REQUEST = "HUMAN_REQUEST"
    SMALL_TALK = "SMALL_TALK"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    UNKNOWN = "UNKNOWN"


LABEL_DESCRIPTIONS: dict[RouterLabel, str] = {
    RouterLabel.PLACE_ORDER: "Customer starts an order, adds items, or gives first details like time, address or payment.",
    RouterLabel.MODIFY_ORDER: "Customer changes something already stated: items, sizes, extras, time, address or payment.",
    RouterLabel.CANCEL_ORDER: "Customer cancels the whole order.",
    RouterLabel.CONFIRM_ORDER: "Customer agrees the order summary is correct.",
    RouterLabel.MENU_QUESTION: "Question about menu items, ingredients, sizes, prices or availability.",
    RouterLabel.DELIVERY_QUESTION: "Question about delivery area, fee, pickup, or opening hours.",
    RouterLabel.PAYMENT_QUESTION: "Question about how to pay or which payment methods work.",
    RouterLabel.PAYMENT_CLAIM: "Customer says they already paid or sent payment.",
    RouterLabel.ORDER_STATUS: "Customer asks where a placed order is or when it will arrive.",
    RouterLabel.ORDER_PROBLEM: "Complaint about a received order: missing, wrong, late, cold or damaged.",
    RouterLabel.REFUND_REQUEST: "Customer asks for their money back or a refund.",
    RouterLabel.HUMAN_REQUEST: "Customer asks to talk to a person or staff member.",
    RouterLabel.SMALL_TALK: "Greeting, thanks, or chit-chat with no request.",
    RouterLabel.OUT_OF_SCOPE: "Request unrelated to ordering food from this business.",
    RouterLabel.UNKNOWN: "Too unclear to tell what the customer wants.",
}

ORDER_LABELS = frozenset(
    {RouterLabel.PLACE_ORDER, RouterLabel.MODIFY_ORDER, RouterLabel.CANCEL_ORDER, RouterLabel.CONFIRM_ORDER}
)
"""Labels that send the message to the extractor (spec §3)."""


class Urgency(StrEnum):
    """Written rubric in docs/TAXONOMY.md. Frustration alone is not urgency."""

    normal = "normal"
    time_sensitive = "time_sensitive"
    needs_staff_now = "needs_staff_now"


URGENCY_DESCRIPTIONS: dict[Urgency, str] = {
    Urgency.normal: "No time pressure beyond a normal order.",
    Urgency.time_sensitive: "A deadline or delay matters now: late order, pickup soon, time change.",
    Urgency.needs_staff_now: "Safety, allergy reaction, payment dispute, or wrong delivery needing staff now.",
}


class OrderReference(StrEnum):
    """Which order the message is about."""

    draft = "draft"  # the order being built in this conversation
    placed_order = "placed_order"  # an order already confirmed/sent to the kitchen
    none = "none"  # no order involved (greeting, menu question before ordering)
    unclear = "unclear"


REFERENCE_DESCRIPTIONS: dict[OrderReference, str] = {
    OrderReference.draft: "The order still being put together in this chat.",
    OrderReference.placed_order: "An order already placed or confirmed.",
    OrderReference.none: "No specific order.",
    OrderReference.unclear: "Can't tell which order.",
}


class ContextFlags(Strict):
    refers_to: OrderReference
    asks_for_human: bool = False


class RouterDecision(Strict):
    """One message's routing: the gold annotation and the normalized provider output share this shape."""

    schema_version: Literal["router@0.1"] = ROUTER_SCHEMA_VERSION
    primary: RouterLabel
    secondary: RouterLabel | None = None
    urgency: Urgency = Urgency.normal
    flags: ContextFlags

    @model_validator(mode="after")
    def _consistency(self) -> "RouterDecision":
        if self.secondary is not None:
            if self.secondary == self.primary:
                raise ValueError("secondary label must differ from primary")
            if RouterLabel.UNKNOWN in (self.primary, self.secondary):
                raise ValueError("UNKNOWN can't be combined with another label")
        if RouterLabel.HUMAN_REQUEST in (self.primary, self.secondary) and not self.flags.asks_for_human:
            raise ValueError("HUMAN_REQUEST implies flags.asks_for_human")
        return self

    @property
    def goes_to_extractor(self) -> bool:
        return self.primary in ORDER_LABELS or self.secondary in ORDER_LABELS


class MessageRouting(Strict):
    message_index: int = Field(ge=0)
    decision: RouterDecision
