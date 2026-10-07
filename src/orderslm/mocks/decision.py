"""A DecisionProvider that never touches the network (port of AgentDesk's FakeProvider).

Tests hand it a script; it plays the steps back in order and records every
request, so a test can assert both what the router did and exactly what it sent.
A step is a DecisionResponse, a function of the request, or an exception to raise.
"""

from collections.abc import Callable

from orderslm.interfaces.decision import (
    Answer,
    DecisionRequest,
    DecisionResponse,
    QuestionType,
    Usage,
)

Step = DecisionResponse | Callable[[DecisionRequest], DecisionResponse] | Exception


class ScriptedDecisionProvider:
    def __init__(
        self, script: list[Step] | None = None, *, name: str = "fake", max_options: int | None = None
    ):
        self._name = name
        self._max_options = max_options
        self._script: list[Step] = list(script or [])
        self.requests: list[DecisionRequest] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def max_options(self) -> int | None:
        return self._max_options

    @property
    def remaining(self) -> int:
        return len(self._script)

    def push(self, *steps: Step) -> None:
        self._script.extend(steps)

    def decide(self, request: DecisionRequest) -> DecisionResponse:
        self.requests.append(request.model_copy(deep=True))
        if not self._script:
            raise RuntimeError(
                f"ScriptedDecisionProvider: script exhausted after {len(self.requests) - 1} responses"
            )
        step = self._script.pop(0)
        if isinstance(step, Exception):
            raise step
        return step(request) if callable(step) else step


def router_answers(
    primary: str,
    *,
    secondary: str = "NONE",
    urgency: str = "normal",
    refers_to: str = "draft",
    asks_for_human: bool = False,
    provider: str = "fake",
    refuse_primary: bool = False,
) -> DecisionResponse:
    """Terse helper for scripting a router answer."""

    def choice(name: str, value: str) -> Answer:
        return Answer(name=name, type=QuestionType.choice, choice=value, probabilities={value: 1.0})

    answers = {
        "primary": Answer(name="primary", type=QuestionType.choice, refused=True)
        if refuse_primary
        else choice("primary", primary),
        "secondary": choice("secondary", secondary),
        "urgency": choice("urgency", urgency),
        "refers_to": choice("refers_to", refers_to),
        "asks_for_human": Answer(name="asks_for_human", type=QuestionType.boolean, boolean=asks_for_human),
    }
    return DecisionResponse(
        provider=provider, model="scripted", answers=answers, usage=Usage(input_tokens=100), latency_ms=1.0
    )
