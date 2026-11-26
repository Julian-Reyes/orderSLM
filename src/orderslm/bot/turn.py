"""One bot turn: the student's answer for the latest customer message → checked order, state change, reply.

The student is the only model (architecture C, extractor-only: its own intent label routes the message; the router
of spec §3 is M7 and not built). Everything after the student is code: finalize (menu ids), pricing, schedule, the
order state machine (core/state.py) and the reply layer (core/replies.py). A model never writes reply text.

Routing by the student's intent (bot@0.1):

- HUMAN_REQUEST, ORDER_PROBLEM, REFUND_REQUEST, ORDER_STATUS: handed to staff (the chat ends: `handoff`).
- CANCEL_ORDER, or a cancelled decision: the order is cancelled (`cancelled`).
- Otherwise the order flow: a "yes" to a summary that still checks out places the order (`placed`); any change
  sends a new summary; anything missing gets a question (`next_reply`).
- With no order started: small talk and off-topic messages get the fixed sentences of spec §16; menu, delivery and
  payment questions get "can't answer that here" (the menu-data answers of §16 are M8, not built).
- An invalid student answer: the bot asks the customer to say it again and keeps the previous order.

Once placed, the chat ends (the simulated test scores the placed order); later turns are not handled here.
"""

from dataclasses import dataclass, field

from orderslm.core.finalize import finalize_order
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.replies import _t, cancelled, next_reply
from orderslm.core.schedule import resolve_schedule
from orderslm.core.state import OrderEvent, event_from_turn, ready_for_confirmation, transition
from orderslm.eval.student_bakeoff import strip_fences
from orderslm.schema.conversation import Conversation
from orderslm.schema.extraction import ExtractionOutput
from orderslm.schema.label import StudentOutput
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.order import OrderStatus, ToolOk
from orderslm.schema.routing import RouterLabel

BOT_VERSION = "bot@0.1"
L = RouterLabel
TO_STAFF = {L.HUMAN_REQUEST, L.ORDER_PROBLEM, L.REFUND_REQUEST, L.ORDER_STATUS}
QUESTIONS = {L.MENU_QUESTION, L.DELIVERY_QUESTION, L.PAYMENT_QUESTION}
TEXT = {  # bot@0.1 sentences not in the reply layer (English only)
    "repeat": "Sorry, I didn't quite get that. Could you say it again?",
    "greeting": "Hi! What can I get you?",
    "off_topic": "I can only help with orders at {business}. Want to order something?",
    "cant_answer": "Sorry, I can't answer that one here.",
    "what_order": "What can I get you?",
}


@dataclass
class BotState:
    status: OrderStatus = OrderStatus.draft
    proposal: ExtractionOutput | None = (
        None  # the latest checked order (finalized), None before the first one
    )
    ended: str | None = None  # placed | handoff | cancelled


@dataclass
class TurnResult:
    reply: str
    kind: str  # question | summary | placed | handoff | cancelled | repeat | greeting | off_topic | cant_answer | …
    state: BotState
    intent: str | None
    valid: bool
    notes: list[str] = field(default_factory=list)


def parse_student(text: str) -> StudentOutput | None:
    try:
        return StudentOutput.model_validate_json(strip_fences(text))
    except ValueError:
        return None


def bot_turn(menu: MenuCatalog, conversation: Conversation, state: BotState, student_text: str) -> TurnResult:
    """`conversation` ends with the customer message the student answered."""
    if state.ended:
        raise ValueError(f"the chat has ended ({state.ended})")
    student = parse_student(student_text)
    if student is None:
        return TurnResult(TEXT["repeat"], "repeat", state, None, False)
    intent = student.intent.primary
    if intent in TO_STAFF:
        return TurnResult(
            _t(conversation.language)["handoff"], "handoff", _end(state, "handoff"), intent.value, True
        )
    if intent is L.CANCEL_ORDER:
        return TurnResult(
            cancelled(conversation.language), "cancelled", _end(state, "cancelled"), intent.value, True
        )

    proposal = finalize_order(student.order, menu)
    if not proposal.items and state.proposal is None:  # nothing ordered yet
        if intent is L.SMALL_TALK:
            return TurnResult(TEXT["greeting"], "greeting", state, intent.value, True)
        if intent is L.OUT_OF_SCOPE:
            return TurnResult(
                TEXT["off_topic"].format(business=menu.name), "off_topic", state, intent.value, True
            )
        if intent in QUESTIONS:
            return TurnResult(
                f"{TEXT['cant_answer']} {TEXT['what_order']}", "cant_answer", state, intent.value, True
            )
    quote = DeterministicPricing().quote(menu, proposal)
    schedule = resolve_schedule(menu, proposal, conversation)
    event = event_from_turn(state.status, state.proposal, proposal)
    new = BotState(status=state.status, proposal=proposal)
    if event is OrderEvent.customer_cancelled:
        return TurnResult(
            cancelled(conversation.language), "cancelled", _end(new, "cancelled"), intent.value, True
        )
    if event is OrderEvent.customer_confirmed:
        if ready_for_confirmation(proposal, menu, quote) and isinstance(schedule, ToolOk):
            placed = transition(new.status, event)
            new.status = placed.data if isinstance(placed, ToolOk) else new.status
            return TurnResult(
                _t(conversation.language)["placed"].format(eta=""),
                "placed",
                _end(new, "placed"),
                intent.value,
                True,
            )
    if event is OrderEvent.customer_modified and new.status is OrderStatus.awaiting_confirmation:
        new.status = OrderStatus.draft
    reply, kind = next_reply(menu, proposal, quote, schedule, conversation.language)
    if kind == "summary" and new.status is OrderStatus.draft:
        sent = transition(new.status, OrderEvent.summary_sent)
        new.status = sent.data if isinstance(sent, ToolOk) else new.status
    if intent in QUESTIONS:
        reply = f"{TEXT['cant_answer']} {reply}"
    return TurnResult(reply, kind, new, intent.value, True)


def _end(state: BotState, how: str) -> BotState:
    return BotState(status=state.status, proposal=state.proposal, ended=how)
