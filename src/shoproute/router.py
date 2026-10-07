"""Turns one customer message into a DecisionRequest and the answers back into a RouterDecision.

Every provider gets byte-identical questions and option descriptions from here
(spec §11: identical messages, context and label descriptions). Any repair
applied to a provider's answers is returned as a note so the benchmark can
count it instead of hiding it.
"""

from dataclasses import dataclass, field

from shoproute.interfaces.decision import (
    DecisionRequest,
    DecisionResponse,
    Option,
    Question,
    QuestionType,
)
from shoproute.schema.common import TAXONOMY_VERSION
from shoproute.schema.conversation import Conversation, Role
from shoproute.schema.routing import (
    LABEL_DESCRIPTIONS,
    REFERENCE_DESCRIPTIONS,
    URGENCY_DESCRIPTIONS,
    ContextFlags,
    OrderReference,
    RouterDecision,
    RouterLabel,
    Urgency,
)

ROUTER_PROMPT_VERSION = f"router-prompt@0.1+{TAXONOMY_VERSION}"
NO_SECONDARY = "NONE"
CONTEXT_MESSAGES = 6  # earlier messages shown with the one being routed


@dataclass(frozen=True)
class RouterContext:
    conversation: Conversation
    message_index: int
    has_draft: bool
    has_placed_order: bool


def _choice(name: str, prompt: str, options: dict[str, str]) -> Question:
    return Question(
        name=name,
        type=QuestionType.choice,
        prompt=prompt,
        options=[Option(id=k, description=v) for k, v in options.items()],
    )


def router_questions() -> list[Question]:
    labels = {label.value: desc for label, desc in LABEL_DESCRIPTIONS.items()}
    secondary = {NO_SECONDARY: "The message makes only one request."} | {
        k: v for k, v in labels.items() if k != RouterLabel.UNKNOWN
    }
    return [
        _choice("primary", "What does the customer mainly want in the latest message?", labels),
        _choice("secondary", "Does the latest message also make a second, different request?", secondary),
        _choice(
            "urgency",
            "How urgent is the latest message?",
            {u.value: d for u, d in URGENCY_DESCRIPTIONS.items()},
        ),
        _choice(
            "refers_to",
            "Which order is the latest message about?",
            {r.value: d for r, d in REFERENCE_DESCRIPTIONS.items()},
        ),
        Question(
            name="asks_for_human",
            type=QuestionType.boolean,
            prompt="Does the customer ask to talk to a person?",
        ),
    ]


def render_input(ctx: RouterContext) -> str:
    """The state text sent to every provider. Deterministic: same context, same bytes."""
    msgs = ctx.conversation.messages
    target = msgs[ctx.message_index]
    if target.role is not Role.customer:
        raise ValueError(f"message {ctx.message_index} is not a customer message")
    earlier = msgs[max(0, ctx.message_index - CONTEXT_MESSAGES) : ctx.message_index]
    lines = [
        f"Order in progress: {'yes' if ctx.has_draft else 'no'}.",
        f"Placed order exists: {'yes' if ctx.has_placed_order else 'no'}.",
    ]
    if earlier:
        lines.append("Earlier messages:")
        lines += [f"{m.role.value}: {m.text}" for m in earlier]
    lines.append(f"Latest customer message: {target.text}")
    return "\n".join(lines)


def build_router_request(ctx: RouterContext) -> DecisionRequest:
    return DecisionRequest(
        request_id=f"{ctx.conversation.id}:{ctx.message_index}",
        input=render_input(ctx),
        questions=router_questions(),
        prompt_version=ROUTER_PROMPT_VERSION,
    )


@dataclass
class ParsedRouting:
    decision: RouterDecision
    abstained: bool
    notes: list[str] = field(default_factory=list)


def parse_router_response(response: DecisionResponse) -> ParsedRouting:
    """Map validated answers onto a RouterDecision. A refused primary is an abstention (UNKNOWN)."""
    a = response.answers
    notes: list[str] = []
    abstained = a["primary"].refused
    primary = RouterLabel.UNKNOWN if abstained else RouterLabel(a["primary"].choice)

    secondary: RouterLabel | None = None
    sec = a["secondary"]
    if not sec.refused and sec.choice != NO_SECONDARY:
        secondary = RouterLabel(sec.choice)
        if secondary == primary or primary is RouterLabel.UNKNOWN:
            notes.append(f"dropped secondary {secondary.value} (same as primary or primary UNKNOWN)")
            secondary = None

    urgency = Urgency.normal if a["urgency"].refused else Urgency(a["urgency"].choice)
    refers_to = OrderReference.unclear if a["refers_to"].refused else OrderReference(a["refers_to"].choice)
    asks_for_human = bool(a["asks_for_human"].boolean)
    if RouterLabel.HUMAN_REQUEST in (primary, secondary) and not asks_for_human:
        notes.append("set asks_for_human because a HUMAN_REQUEST label was chosen")
        asks_for_human = True

    decision = RouterDecision(
        primary=primary,
        secondary=secondary,
        urgency=urgency,
        flags=ContextFlags(refers_to=refers_to, asks_for_human=asks_for_human),
    )
    return ParsedRouting(decision=decision, abstained=abstained, notes=notes)
