"""In-memory business tools for the demo, tests and evals. Deterministic: injected clock, sequential ids."""

from orderslm.domain.clock import Clock
from orderslm.schema.order import (
    HandoffReason,
    HandoffTicket,
    OrderRecord,
    ToolErr,
    ToolError,
    ToolOk,
    ToolResult,
)
from orderslm.schema.routing import Urgency

TOOLS_VERSION = "tools.mock@0.1"


class InMemoryBusinessTools:
    def __init__(self, clock: Clock, orders: list[OrderRecord] | None = None):
        self._clock = clock
        self._orders: dict[str, OrderRecord] = {o.order_id: o for o in orders or []}
        self.handoff_queue: list[HandoffTicket] = []

    def _err(self, tool: str, code: str, message: str) -> ToolErr:
        return ToolErr(error=ToolError(code=code, message=message), verified_by=f"{TOOLS_VERSION}:{tool}")

    def lookup_order(self, conversation_id: str) -> ToolResult[OrderRecord]:
        matches = [o for o in self._orders.values() if o.conversation_id == conversation_id]
        if not matches:
            return self._err("lookup_order", "NOT_FOUND", "No placed order for this conversation.")
        latest = max(matches, key=lambda o: o.created_at)
        return ToolOk[OrderRecord](data=latest, verified_by=f"{TOOLS_VERSION}:lookup_order")

    def order_status(self, order_id: str) -> ToolResult[OrderRecord]:
        order = self._orders.get(order_id)
        if order is None:
            return self._err("order_status", "NOT_FOUND", f"Unknown order {order_id}.")
        return ToolOk[OrderRecord](data=order, verified_by=f"{TOOLS_VERSION}:order_status")

    def request_handoff(
        self, conversation_id: str, reason: HandoffReason, urgency: Urgency, summary: str
    ) -> ToolResult[HandoffTicket]:
        if not summary.strip():
            return self._err("request_handoff", "INVALID_ARGS", "A handoff needs a summary for staff.")
        ticket = HandoffTicket(
            ticket_id=f"hand_{len(self.handoff_queue) + 1:04d}",
            conversation_id=conversation_id,
            reason=reason,
            urgency=urgency.value,
            summary=summary,
            created_at=self._clock(),
        )
        self.handoff_queue.append(ticket)
        return ToolOk[HandoffTicket](data=ticket, verified_by=f"{TOOLS_VERSION}:request_handoff")
