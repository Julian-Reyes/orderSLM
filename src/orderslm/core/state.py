"""Order status transitions. A model's output never changes status directly: it becomes an event,
and only the transitions below are allowed.

    draft ──summary_sent──► awaiting_confirmation ──customer_confirmed──► new ──► preparing ──► ready ──► completed
      ▲                         │
      └──customer_modified──────┘          (customer_cancelled from draft/awaiting; staff_cancelled from new/preparing)

Once an order is placed (new and later), customer changes or cancellations go to
staff (NEEDS_STAFF), never applied automatically.
"""

from enum import StrEnum

from orderslm.core.diff import diff_orders
from orderslm.core.missing import required_missing
from orderslm.schema.extraction import DecisionState, ExtractionOutput
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.order import OrderStatus, Quote, ToolErr, ToolError, ToolOk, ToolResult

STATE_VERSION = "state@0.1"
S = OrderStatus


class OrderEvent(StrEnum):
    summary_sent = "summary_sent"  # the bot sent a priced summary and asked "is that right?"
    customer_confirmed = "customer_confirmed"
    customer_modified = "customer_modified"
    customer_cancelled = "customer_cancelled"
    staff_started = "staff_started"
    staff_ready = "staff_ready"
    staff_completed = "staff_completed"
    staff_cancelled = "staff_cancelled"


TRANSITIONS: dict[tuple[OrderStatus, OrderEvent], OrderStatus] = {
    (S.draft, OrderEvent.summary_sent): S.awaiting_confirmation,
    (S.draft, OrderEvent.customer_modified): S.draft,
    (S.draft, OrderEvent.customer_cancelled): S.cancelled,
    (S.awaiting_confirmation, OrderEvent.customer_confirmed): S.new,
    (S.awaiting_confirmation, OrderEvent.customer_modified): S.draft,
    (S.awaiting_confirmation, OrderEvent.customer_cancelled): S.cancelled,
    (S.awaiting_confirmation, OrderEvent.summary_sent): S.awaiting_confirmation,
    (S.new, OrderEvent.staff_started): S.preparing,
    (S.new, OrderEvent.staff_cancelled): S.cancelled,
    (S.preparing, OrderEvent.staff_ready): S.ready,
    (S.preparing, OrderEvent.staff_cancelled): S.cancelled,
    (S.ready, OrderEvent.staff_completed): S.completed,
}
PLACED = {S.new, S.preparing, S.ready, S.completed}
CUSTOMER_EVENTS = {OrderEvent.customer_modified, OrderEvent.customer_cancelled, OrderEvent.customer_confirmed}


def transition(status: OrderStatus, event: OrderEvent) -> ToolResult[OrderStatus]:
    nxt = TRANSITIONS.get((status, event))
    if nxt is not None:
        return ToolOk[OrderStatus](data=nxt, verified_by=STATE_VERSION)
    if status in PLACED and event in CUSTOMER_EVENTS:
        code, msg = (
            "NEEDS_STAFF",
            f"order is {status.value}: customer {event.value.split('_')[1]} needs staff",
        )
    else:
        code, msg = "INVALID_TRANSITION", f"{event.value} is not allowed when the order is {status.value}"
    return ToolErr(error=ToolError(code=code, message=msg), verified_by=STATE_VERSION)


def ready_for_confirmation(proposal: ExtractionOutput, menu: MenuCatalog, quote: ToolResult[Quote]) -> bool:
    """A summary may only be sent when nothing is missing and pricing succeeded."""
    return quote.ok and not required_missing(proposal, menu) and not proposal.missing_or_ambiguous


def event_from_turn(
    status: OrderStatus, previous: ExtractionOutput | None, current: ExtractionOutput
) -> OrderEvent | None:
    """What the customer's latest turn means for the order, from the snapshots (not from model claims alone).

    - cancelled decision -> customer_cancelled
    - any change to the order -> customer_modified (a confirmation in the same turn doesn't count:
      the changed order needs a new summary and a new yes)
    - confirmed decision, no change, while awaiting confirmation -> customer_confirmed
    - "yes" when no summary was sent (draft) is not a confirmation -> None
    """
    if current.customer_decision.state is DecisionState.cancelled:
        return OrderEvent.customer_cancelled
    patch = diff_orders(previous, current)
    changes = [f for f in patch.fields_changed if f != "customer_decision"]
    if patch.items_changed or changes:
        return OrderEvent.customer_modified
    if current.customer_decision.state is DecisionState.confirmed and status is S.awaiting_confirmation:
        return OrderEvent.customer_confirmed
    return None
