"""Verified results: what code (never a model) computed or a tool looked up.

Model proposals live in schema/extraction.py. Everything here is produced by the
deterministic core or a business tool, carries `verified_by`, and is the only
thing the reply layer may state as fact (prices, totals, order status).
"""

from datetime import date, datetime, time
from enum import StrEnum
from typing import Generic, Literal, TypeVar

from pydantic import Field, model_validator

from orderslm.domain.money import Cents

from .common import ID_PATTERN, Strict
from .extraction import FulfillmentMethod, Modification


class OrderStatus(StrEnum):
    draft = "draft"  # being built in chat; nothing sent to the kitchen
    awaiting_confirmation = "awaiting_confirmation"  # summary sent, waiting for "yes"
    new = "new"  # confirmed: shows on the business ticket board
    preparing = "preparing"
    ready = "ready"
    completed = "completed"
    cancelled = "cancelled"


class QuoteLine(Strict):
    line_id: str
    menu_item_id: str = Field(
        pattern=ID_PATTERN, description="for half-and-half: the half that sets the price"
    )
    half_menu_item_ids: list[str] | None = Field(default=None, min_length=2, max_length=2)
    display_name: str
    quantity: int = Field(ge=1, le=99)
    variant_id: str | None = None
    modifications: list[Modification] = Field(default_factory=list)
    unit_price_cents: Cents
    line_total_cents: Cents

    @model_validator(mode="after")
    def _math(self) -> "QuoteLine":
        if self.line_total_cents != self.unit_price_cents * self.quantity:
            raise ValueError(f"{self.line_id}: line_total_cents != unit_price_cents * quantity")
        return self


class Quote(Strict):
    """A priced order. Arithmetic consistency is enforced here, so a malformed quote can't exist."""

    business_id: str = Field(pattern=ID_PATTERN)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    lines: list[QuoteLine] = Field(min_length=1)
    fulfillment: FulfillmentMethod
    subtotal_cents: Cents
    delivery_fee_cents: Cents = 0
    total_cents: Cents
    verified_by: str = Field(description="pricing engine version, e.g. pricing@0.1")
    menu_version: str

    @model_validator(mode="after")
    def _math(self) -> "Quote":
        if self.subtotal_cents != sum(line.line_total_cents for line in self.lines):
            raise ValueError("subtotal_cents != sum of line totals")
        if self.fulfillment is not FulfillmentMethod.delivery and self.delivery_fee_cents:
            raise ValueError("delivery_fee_cents must be 0 unless delivering")
        if self.total_cents != self.subtotal_cents + self.delivery_fee_cents:
            raise ValueError("total_cents != subtotal_cents + delivery_fee_cents")
        return self


class Schedule(Strict):
    """When the order is for, worked out in code (core/schedule.py) from the customer's words, the time of the
    message they said it in, and the menu's hours. The reply layer states the day and time only from this."""

    business_id: str = Field(pattern=ID_PATTERN)
    local_date: date = Field(description="the order's day in the business's timezone")
    days_ahead: int = Field(ge=0, description="0 = today")
    asap: bool = Field(description="no time given: as soon as possible (today only)")
    local_time: time | None = Field(default=None, description="the clock time, if one was given")
    time_text: str | None = Field(
        default=None, description="a relative time as said ('in 20 min'); today only"
    )
    verified_by: str = Field(description="schedule version, e.g. schedule@0.1")

    @model_validator(mode="after")
    def _consistent(self) -> "Schedule":
        if (self.asap or self.time_text) and self.days_ahead:
            raise ValueError("asap and relative times are for today only")
        if self.asap and (self.local_time or self.time_text):
            raise ValueError("asap has no clock or relative time")
        return self


class OrderRecord(Strict):
    """A placed order as the business tools see it."""

    order_id: str = Field(pattern=r"^ord_[a-z0-9]+$")
    business_id: str = Field(pattern=ID_PATTERN)
    conversation_id: str
    status: OrderStatus
    quote: Quote
    payment_confirmed: bool = Field(
        default=False, description="set only by staff/payment system, never by chat"
    )
    created_at: datetime
    updated_at: datetime
    eta_minutes: int | None = Field(default=None, ge=0)


class HandoffReason(StrEnum):
    customer_asked = "customer_asked"
    order_problem = "order_problem"
    refund_request = "refund_request"
    payment_claim = "payment_claim"
    unclear = "unclear"


class HandoffTicket(Strict):
    ticket_id: str
    conversation_id: str
    reason: HandoffReason
    urgency: str
    summary: str
    created_at: datetime


# ---------------------------------------------------------------- tool results

T = TypeVar("T")


class ToolError(Strict):
    code: str = Field(pattern=r"^[A-Z][A-Z0-9_]*$")
    message: str
    details: dict[str, object] | None = None


class ToolOk(Strict, Generic[T]):  # noqa: UP046 (pydantic generic models subclass Generic)
    """Tools never raise for business outcomes ("order not found"). Exceptions are for bugs only.

    Same convention as AgentDesk's `{ ok, data } | { ok: false, error }`.
    """

    ok: Literal[True] = True
    data: T
    verified_by: str = Field(description="which tool produced this, e.g. tools.mock@0.1:order_status")


class ToolErr(Strict):
    ok: Literal[False] = False
    error: ToolError
    verified_by: str


type ToolResult[R] = ToolOk[R] | ToolErr
