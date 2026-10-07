"""The extraction contract: what the teacher and every student must output.

This is a model *proposal*. It names menu ids and quantities, never prices:
prices, fees and totals are computed by the deterministic core (schema/order.py),
and `extra="forbid"` makes a model that invents a price field fail validation.

The output is a full snapshot of the order as the conversation stands, not a
diff. The patch shown to the business (what changed this turn) is computed in
code by comparing the snapshot with the current draft. See docs/SCHEMA.md.
"""

from collections.abc import Iterator
from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from shoproute.domain.money import Cents

from .common import EXTRACTION_SCHEMA_VERSION, ID_PATTERN, Evidence, Strict

LINE_ID_PATTERN = r"^L[0-9]+$"
HHMM_PATTERN = r"^([01][0-9]|2[0-3]):[0-5][0-9]$"


class SlotState(StrEnum):
    """Keeps "unknown" distinct from "absent" and "not applicable" (spec §4)."""

    provided = "provided"  # stated clearly: value set, evidence required
    ambiguous = "ambiguous"  # mentioned but unclear ("around 7 or 8"): evidence required, no value
    not_mentioned = "not_mentioned"  # nothing said yet
    not_applicable = "not_applicable"  # does not apply (address for pickup)


def _check_slot(state: SlotState, has_value: bool, evidence: list[Evidence], where: str) -> None:
    if state is SlotState.provided and not has_value:
        raise ValueError(f"{where}: state 'provided' needs a value")
    if state is not SlotState.provided and has_value:
        raise ValueError(f"{where}: only state 'provided' may carry a value (got {state.value})")
    if state in (SlotState.provided, SlotState.ambiguous) and not evidence:
        raise ValueError(f"{where}: state {state.value!r} needs evidence")
    if state in (SlotState.not_mentioned, SlotState.not_applicable) and evidence:
        raise ValueError(f"{where}: state {state.value!r} must not carry evidence")


# ---------------------------------------------------------------- items


class ModificationKind(StrEnum):
    remove = "remove"  # "no onions"
    add = "add"  # "extra bacon"
    substitute = "substitute"  # "mayo instead of ketchup"


class Modification(Strict):
    kind: ModificationKind
    modifier_id: str | None = Field(
        default=None,
        pattern=ID_PATTERN,
        description="catalog modifier; null if the request is not on the menu",
    )
    replacement_modifier_id: str | None = Field(default=None, pattern=ID_PATTERN)
    raw_text: str = Field(min_length=1, description="the request as the customer wrote it")

    @model_validator(mode="after")
    def _replacement(self) -> "Modification":
        if self.replacement_modifier_id is not None and self.kind is not ModificationKind.substitute:
            raise ValueError("replacement_modifier_id is only for kind 'substitute'")
        return self


class HalfSelection(Strict):
    """One half of a half-and-half pizza."""

    menu_item_id: str = Field(pattern=ID_PATTERN)
    modifications: list[Modification] = Field(default_factory=list)


class ComboSelection(Strict):
    slot_id: str = Field(pattern=ID_PATTERN)
    menu_item_id: str = Field(pattern=ID_PATTERN)
    variant_id: str | None = Field(default=None, pattern=ID_PATTERN)


class ItemProposal(Strict):
    line_id: str = Field(pattern=LINE_ID_PATTERN, description="stable within a conversation: L1, L2, ...")
    menu_item_id: str | None = Field(default=None, pattern=ID_PATTERN)
    unmatched_text: str | None = Field(default=None, min_length=1, description="off-menu request, as written")
    halves: list[HalfSelection] | None = Field(default=None, min_length=2, max_length=2)
    quantity: int | None = Field(ge=1, le=99, description="null = stated but unclear ('some wings')")
    variant_id: str | None = Field(default=None, pattern=ID_PATTERN, description="null = not stated")
    modifications: list[Modification] = Field(default_factory=list)
    combo_selections: list[ComboSelection] = Field(default_factory=list)
    notes: str | None = None
    evidence: list[Evidence] = Field(min_length=1)

    @model_validator(mode="after")
    def _one_identity(self) -> "ItemProposal":
        set_ = [self.menu_item_id is not None, self.unmatched_text is not None, self.halves is not None]
        if sum(set_) != 1:
            raise ValueError(
                f"{self.line_id}: exactly one of menu_item_id, unmatched_text, halves must be set (spec §4)"
            )
        if self.unmatched_text is not None and (
            self.variant_id or self.modifications or self.combo_selections
        ):
            raise ValueError(
                f"{self.line_id}: an off-menu item can't have variant, modifications or combo picks"
            )
        return self


# ---------------------------------------------------------------- order-level fields


class FulfillmentMethod(StrEnum):
    delivery = "delivery"
    pickup = "pickup"
    unknown = "unknown"


class TimeKind(StrEnum):
    asap = "asap"  # "asap", "now", "as soon as u can"
    clock_time = "clock_time"  # "at 7", "7:30pm"
    relative = "relative"  # "in 20 min"


class RequestedTime(Strict):
    state: SlotState
    kind: TimeKind | None = None
    raw_text: str | None = Field(default=None, description="as stated, e.g. 'at 7'")
    normalized_local: str | None = Field(
        default=None,
        pattern=HHMM_PATTERN,
        description="HH:MM in the business's timezone, only if unambiguous",
    )
    evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def _slot(self) -> "RequestedTime":
        _check_slot(self.state, self.kind is not None, self.evidence, "requested_time")
        if self.state is not SlotState.provided and self.normalized_local is not None:
            raise ValueError("requested_time: normalized_local only when provided")
        if self.normalized_local is not None and self.kind is not TimeKind.clock_time:
            raise ValueError("requested_time: normalized_local only for kind 'clock_time'")
        if self.state in (SlotState.provided, SlotState.ambiguous) and not self.raw_text:
            raise ValueError("requested_time: raw_text required when the time was mentioned")
        return self


class Fulfillment(Strict):
    method: FulfillmentMethod
    method_evidence: list[Evidence] = Field(default_factory=list)
    requested_time: RequestedTime

    @model_validator(mode="after")
    def _evidence(self) -> "Fulfillment":
        if (self.method is FulfillmentMethod.unknown) == bool(self.method_evidence):
            raise ValueError("fulfillment: evidence required for delivery/pickup and forbidden for unknown")
        return self


class Address(Strict):
    state: SlotState
    street: str | None = None
    number: str | None = None
    unit: str | None = None
    reference: str | None = Field(default=None, description="landmark: 'blue door next to the gym'")
    raw_text: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def _slot(self) -> "Address":
        _check_slot(self.state, bool(self.raw_text), self.evidence, "address")
        if self.state is not SlotState.provided and any(
            [self.street, self.number, self.unit, self.reference]
        ):
            raise ValueError("address: components only when provided")
        return self


class PaymentMethod(StrEnum):
    card = "card"
    cash = "cash"
    other = "other"
    unknown = "unknown"


class Payment(Strict):
    method: PaymentMethod
    change_for_cents: Cents | None = Field(
        default=None, description="cash only: the bill the customer says they'll pay with ('change for a 50')"
    )
    customer_claims_paid: bool = Field(
        default=False, description="'I already paid' is a claim, never a verified payment"
    )
    evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def _payment(self) -> "Payment":
        if self.change_for_cents is not None and self.method is not PaymentMethod.cash:
            raise ValueError("payment: change_for_cents only for cash")
        stated = self.method is not PaymentMethod.unknown or self.customer_claims_paid
        if stated != bool(self.evidence):
            raise ValueError(
                "payment: evidence required when a method or claim is stated, forbidden otherwise"
            )
        return self


class CustomerName(Strict):
    state: SlotState
    value: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def _slot(self) -> "CustomerName":
        _check_slot(self.state, self.value is not None, self.evidence, "customer_name")
        return self


class DecisionState(StrEnum):
    """What the customer said about the order as a whole. A statement, not a state transition:
    the deterministic core decides whether a confirmation is valid."""

    pending = "pending"
    confirmed = "confirmed"  # "yep that's right" after a summary
    cancelled = "cancelled"  # "nvm cancel it"


class CustomerDecision(Strict):
    state: DecisionState = DecisionState.pending
    evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def _evidence(self) -> "CustomerDecision":
        if (self.state is DecisionState.pending) == bool(self.evidence):
            raise ValueError(
                "customer_decision: evidence required for confirmed/cancelled, forbidden for pending"
            )
        return self


class Note(Strict):
    text: str = Field(min_length=1)
    evidence: list[Evidence] = Field(min_length=1)


# ---------------------------------------------------------------- missing info


class FieldRef(StrEnum):
    items = "items"  # no items yet
    item_menu_match = "item_menu_match"
    item_quantity = "item_quantity"
    item_variant = "item_variant"
    item_modification = "item_modification"
    combo_choice = "combo_choice"
    fulfillment_method = "fulfillment_method"
    requested_time = "requested_time"
    address = "address"
    payment_method = "payment_method"
    customer_name = "customer_name"


ITEM_FIELDS = {
    FieldRef.item_menu_match,
    FieldRef.item_quantity,
    FieldRef.item_variant,
    FieldRef.item_modification,
    FieldRef.combo_choice,
}


class MissingReason(StrEnum):
    missing = "missing"
    ambiguous = "ambiguous"
    off_menu = "off_menu"
    conflicting = "conflicting"


class MissingInfo(Strict):
    field: FieldRef
    reason: MissingReason
    line_id: str | None = Field(default=None, pattern=LINE_ID_PATTERN)

    @model_validator(mode="after")
    def _line(self) -> "MissingInfo":
        if (self.field in ITEM_FIELDS) != (self.line_id is not None):
            raise ValueError(
                f"missing_or_ambiguous: line_id is required for item fields only ({self.field.value})"
            )
        return self


# ---------------------------------------------------------------- the output


class ExtractionOutput(Strict):
    schema_version: Literal["extraction@0.1"] = EXTRACTION_SCHEMA_VERSION
    items: list[ItemProposal] = Field(default_factory=list)
    fulfillment: Fulfillment
    address: Address
    payment: Payment
    customer_name: CustomerName
    customer_decision: CustomerDecision = Field(default_factory=CustomerDecision)
    notes: list[Note] = Field(default_factory=list)
    missing_or_ambiguous: list[MissingInfo] = Field(default_factory=list)
    clarification_question: str | None = Field(
        default=None, min_length=1, max_length=400, description="one question covering everything missing"
    )

    @model_validator(mode="after")
    def _consistency(self) -> "ExtractionOutput":
        line_ids = [i.line_id for i in self.items]
        if len(line_ids) != len(set(line_ids)):
            raise ValueError("items: duplicate line_id")
        for m in self.missing_or_ambiguous:
            if m.line_id is not None and m.line_id not in line_ids:
                raise ValueError(f"missing_or_ambiguous refers to unknown line {m.line_id}")
        if self.customer_decision.state is DecisionState.cancelled and self.missing_or_ambiguous:
            raise ValueError("a cancelled order has nothing left to clarify")
        if bool(self.missing_or_ambiguous) != (self.clarification_question is not None):
            raise ValueError(
                "clarification_question is required exactly when missing_or_ambiguous is non-empty"
            )
        method = self.fulfillment.method
        if method is FulfillmentMethod.pickup and self.address.state is not SlotState.not_applicable:
            raise ValueError("address must be not_applicable for pickup")
        if method is not FulfillmentMethod.pickup and self.address.state is SlotState.not_applicable:
            raise ValueError("address is only not_applicable for pickup")
        for item in self.items:
            if item.unmatched_text is not None and not any(
                m.line_id == item.line_id and m.field is FieldRef.item_menu_match
                for m in self.missing_or_ambiguous
            ):
                raise ValueError(f"{item.line_id}: off-menu item must be listed as item_menu_match/off_menu")
        return self

    def iter_evidence(self) -> Iterator[tuple[str, Evidence]]:
        """Every evidence entry with a readable path, for the consistency checks."""
        for item in self.items:
            for e in item.evidence:
                yield f"items[{item.line_id}]", e
        groups = {
            "fulfillment.method": self.fulfillment.method_evidence,
            "fulfillment.requested_time": self.fulfillment.requested_time.evidence,
            "address": self.address.evidence,
            "payment": self.payment.evidence,
            "customer_name": self.customer_name.evidence,
            "customer_decision": self.customer_decision.evidence,
        }
        for path, evs in groups.items():
            for e in evs:
                yield path, e
        for n, note in enumerate(self.notes):
            for e in note.evidence:
                yield f"notes[{n}]", e
