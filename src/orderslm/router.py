"""Turns one customer message into a DecisionRequest and the answers back into a RouterDecision.

Every provider gets byte-identical questions and option descriptions from here
(spec §11: identical messages, context and label descriptions). Any repair
applied to a provider's answers is returned as a note so the benchmark can
count it instead of hiding it.
"""

from dataclasses import dataclass, field

from orderslm.interfaces.decision import (
    DecisionRequest,
    DecisionResponse,
    Option,
    Question,
    QuestionType,
)
from orderslm.schema.common import TAXONOMY_VERSION
from orderslm.schema.conversation import Conversation, Role
from orderslm.schema.routing import (
    LABEL_DESCRIPTIONS,
    REFERENCE_DESCRIPTIONS,
    URGENCY_DESCRIPTIONS,
    ContextFlags,
    OrderReference,
    RouterDecision,
    RouterLabel,
    Urgency,
)

ROUTER_PROMPT_VERSION = f"router-prompt@0.2+{TAXONOMY_VERSION}"  # 0.2: whitespace collapsed per message
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
        lines += [f"{m.role.value}: {_one_line(m.text)}" for m in earlier]
    lines.append(f"{LATEST} {_one_line(target.text)}")
    return "\n".join(lines)


def _one_line(text: str) -> str:
    return " ".join(text.split())


LATEST = "Latest customer message:"


@dataclass(frozen=True)
class ParsedInput:
    """render_input's text read back, for local providers (rules) that only receive the DecisionRequest."""

    has_draft: bool
    has_placed_order: bool
    earlier: list[tuple[str, str]]  # (role, text)
    latest: str


def parse_input(text: str) -> ParsedInput:
    lines = text.split("\n")
    if not (lines[0].startswith("Order in progress:") and lines[-1].startswith(LATEST)):
        raise ValueError("not a router input rendered by render_input")
    earlier = []
    for line in lines[2:-1]:
        role, sep, body = line.partition(": ")
        if sep and role in ("customer", "business"):
            earlier.append((role, body))
    return ParsedInput(
        has_draft=lines[0].endswith("yes."),
        has_placed_order=lines[1].endswith("yes."),
        earlier=earlier,
        latest=lines[-1].removeprefix(LATEST).strip(),
    )


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
