"""Business tools and the pricing engine: the only sources of facts the reply layer may state.

Tools return ToolOk | ToolErr and never raise for business outcomes. Model
proposals (ExtractionOutput) go in; verified records come out.
"""

from typing import Protocol, runtime_checkable

from orderslm.schema.extraction import ExtractionOutput
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.order import HandoffReason, HandoffTicket, OrderRecord, Quote, ToolResult
from orderslm.schema.routing import Urgency


@runtime_checkable
class BusinessTools(Protocol):
    """Mocked in V1 (in-memory). A real backend could implement the same protocol later."""

    def lookup_order(self, conversation_id: str) -> ToolResult[OrderRecord]:
        """The most recent placed order for this conversation/customer."""
        ...

    def order_status(self, order_id: str) -> ToolResult[OrderRecord]: ...

    def request_handoff(
        self, conversation_id: str, reason: HandoffReason, urgency: Urgency, summary: str
    ) -> ToolResult[HandoffTicket]: ...


@runtime_checkable
class PricingEngine(Protocol):
    """Deterministic: menu + proposal -> Quote. Implemented in M1 (orderslm.core.pricing).

    Returns ToolErr (e.g. UNMATCHED_ITEM, MISSING_VARIANT, UNKNOWN_MODIFIER,
    UNAVAILABLE) when the proposal can't be priced yet; never guesses.
    """

    def quote(self, menu: MenuCatalog, proposal: ExtractionOutput) -> ToolResult[Quote]: ...
