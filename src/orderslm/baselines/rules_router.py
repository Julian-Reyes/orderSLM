"""Rules baseline router: keyword patterns behind the same DecisionProvider interface as the hosted providers.

It receives exactly what Julia-1, Jev and OpenAI Decisions receive (a DecisionRequest
built by router.py) and reads the context back with router.parse_input. It has no
menu, so it can't tell "cancel the coke" (modify) from "cancel" (whole order)
except by wording. Confidence and probabilities are left empty: rules don't have them.
"""

import re
import time

from orderslm.interfaces.decision import Answer, DecisionRequest, DecisionResponse, QuestionType
from orderslm.router import NO_SECONDARY, parse_input
from orderslm.schema.routing import OrderReference, RouterLabel, Urgency

NAME = "rules"
MODEL = "keywords@0.1"
L = RouterLabel

PATTERNS: dict[RouterLabel, re.Pattern[str]] = {
    L.ORDER_PROBLEM: re.compile(
        r"\b(missing|wrong (?:order|item|food)|was wrong|got the wrong|cold|burnt|burned|undercooked|raw|spilled|"
        r"damaged|soggy|stale|forgot|forgotten|not what i ordered|(?:came|arrived|was) late|never (?:came|arrived))\b"
    ),
    L.REFUND_REQUEST: re.compile(r"\b(refund|money back|reimburse|charge ?back|want my money)\b"),
    L.PAYMENT_CLAIM: re.compile(
        r"\b(already paid|i paid|just paid|paid already|paid online|paid on the app|sent (?:the |u |you )?(?:payment|money))\b"
    ),
    L.ORDER_STATUS: re.compile(
        r"\b(where'?s my|where is my|wheres my|how (?:much )?long|eta|still waiting|taking so long|on (?:its|it's|the) way|"
        r"when will (?:it|my)|status|is it ready|ready yet|almost (?:ready|done))\b"
    ),
    L.CANCEL_ORDER: re.compile(r"\bcancel\b(?!\s+(?:the|my)\s+(?!order\b)\w)"),
    L.MODIFY_ORDER: re.compile(
        r"\b(actually|instead|swap|switch|change|replace|make (?:it|that|them|one of)|remove|take off|no more|"
        r"scratch that|on second thought|cancel (?:the|my) (?!order)\w+)\b"
    ),
    L.PLACE_ORDER: re.compile(
        r"\b(can i (?:get|have|grab|order)|could i (?:get|have)|i'?d like|i would like|i want (?:a|an|\d|two|three)|"
        r"lemme (?:get|have)|let me (?:get|have)|gimme|give me|i'?ll (?:have|take|get)|i'?m gonna get|"
        r"(?:\d+|two|three|four|five|a|an)\s+(?:\w+\s+)?(?:pizzas?|burgers?|cheeseburgers?|tacos?|lattes?|coffees?|"
        r"cokes?|fries|shakes?|muffins?|bagels?|wings|knots|combos?)|"
        r"for (?:pick ?up|delivery)|pick ?up at|delivery to|paying (?:cash|card|by)|(?:cash|card) please)\b"
    ),
    L.MENU_QUESTION: re.compile(
        r"\b(do (?:you|u)(?: guys)? (?:have|got|sell|make)|what(?:'s| is| are) (?:in|on) the|how much (?:is|are|does|for)|"
        r"(?:is|are) (?:it|they|the \w+) (?:vegan|vegetarian|gluten|spicy|dairy)|what (?:sizes|flavors|kinds|toppings)|menu)\b"
    ),
    L.DELIVERY_QUESTION: re.compile(
        r"\b((?:do|can|will) (?:you|u)(?: guys)? deliver|delivery (?:fee|charge|area|cost|time)|how much (?:is|for) delivery|"
        r"(?:what time|when) do (?:you|u) (?:close|open)|your hours|open (?:late|today|now)|still open)\b"
    ),
    L.PAYMENT_QUESTION: re.compile(
        r"\b((?:can|do|could) (?:i|we|u|you) (?:pay|use)|(?:take|accept)s? (?:cash|card|credit|apple pay|venmo)|"
        r"payment (?:options|methods))\b"
    ),
    L.HUMAN_REQUEST: re.compile(
        r"\b((?:talk|speak|chat) (?:to|with) (?:a |an |the |some )?(?:human|person|someone|somebody|staff|manager|real person|employee)|"
        r"(?:human|real person|manager) (?:please|pls|plz)|get me (?:a|the) (?:manager|human|person))\b"
    ),
    L.OUT_OF_SCOPE: re.compile(
        r"\b(hiring|job|jobs|apply|application|weather|parking|wifi|restroom|bathroom)\b"
    ),
    L.SMALL_TALK: re.compile(
        r"^\W*(hi|hey|hello|yo|sup|hiya|good (?:morning|afternoon|evening)|thanks|thank you|thx|ty|ok|okay|cool|great|"
        r"awesome|nice)\b[\W\s]*(?:(?:so much|guys|again|there)\W*)?$"
    ),
}
# Primary = the matched label that needs action first.
PRIORITY = [L.ORDER_PROBLEM, L.REFUND_REQUEST, L.PAYMENT_CLAIM, L.ORDER_STATUS, L.CANCEL_ORDER, L.CONFIRM_ORDER,
            L.MODIFY_ORDER, L.PLACE_ORDER, L.MENU_QUESTION, L.DELIVERY_QUESTION, L.PAYMENT_QUESTION,
            L.HUMAN_REQUEST, L.OUT_OF_SCOPE, L.SMALL_TALK]  # fmt: skip
AFFIRM = re.compile(
    r"^\W*(yes|yep|yeah|yup|ya|correct|that'?s right|sounds good|perfect|looks good|all good)\b"
)
DETAILS = re.compile(
    r"\b(pick ?up|deliver(?:y)?|cash|card|asap|at \d|\d+\s+\w+\s+(?:st|street|ave|avenue|rd|road))\b"
)
STAFF_NOW = re.compile(
    r"\b(allerg\w*|reaction|hives|epipen|can'?t breathe|food poisoning|got sick|vomit\w*|charged (?:me )?twice|"
    r"double charged|wrong (?:address|house|door)|delivered to the wrong)\b"
)
TIME_SENSITIVE = re.compile(
    r"\b(an hour|\d+ ?(?:min|mins|minutes) (?:ago|late)|late|still waiting|taking so long|hurry|in a rush|leaving soon)\b"
)
PLACED_LABELS = {L.ORDER_STATUS, L.ORDER_PROBLEM, L.REFUND_REQUEST, L.PAYMENT_CLAIM}
ORDER_LABELS = {L.PLACE_ORDER, L.MODIFY_ORDER, L.CANCEL_ORDER, L.CONFIRM_ORDER}


def classify(text: str, has_draft: bool, has_placed: bool, last_business: str | None) -> dict[str, object]:
    low = text.lower()
    hits = [label for label in PRIORITY if label in PATTERNS and PATTERNS[label].search(low)]
    if (
        last_business is not None
        and last_business.rstrip().endswith("?")
        and AFFIRM.search(low)
        and has_draft
    ):
        hits.insert(0, L.CONFIRM_ORDER)
    if has_draft and not hits and DETAILS.search(low):
        hits.append(L.PLACE_ORDER)  # first-time details for the order being built
    if (
        L.CANCEL_ORDER in hits
        and L.MODIFY_ORDER in hits
        and re.search(r"cancel (?:the|my) (?!order)\w+", low)
    ):
        hits.remove(L.CANCEL_ORDER)
    if not hits and has_placed and STAFF_NOW.search(low):
        hits.append(L.ORDER_PROBLEM)  # a safety issue with a placed order is a problem with it
    hits = sorted(set(hits), key=PRIORITY.index)
    primary = hits[0] if hits else L.UNKNOWN
    rest = [
        h for h in hits[1:] if h is not L.SMALL_TALK and not (h in ORDER_LABELS and primary in ORDER_LABELS)
    ]
    secondary = rest[0] if rest else None

    human = bool(PATTERNS[L.HUMAN_REQUEST].search(low))
    if STAFF_NOW.search(low):
        urgency = Urgency.needs_staff_now
    elif (
        TIME_SENSITIVE.search(low)
        or (primary is L.ORDER_STATUS and has_placed)
        or (primary in (L.MODIFY_ORDER, L.CANCEL_ORDER) and has_placed and not has_draft)
    ):
        urgency = Urgency.time_sensitive
    else:
        urgency = Urgency.normal

    if primary in PLACED_LABELS or (primary in ORDER_LABELS and has_placed and not has_draft):
        refers = OrderReference.placed_order
    elif primary in ORDER_LABELS:
        refers = OrderReference.draft
    elif primary is L.UNKNOWN:
        refers = OrderReference.unclear
    else:
        refers = OrderReference.none
    return {
        "primary": primary,
        "secondary": secondary,
        "urgency": urgency,
        "refers_to": refers,
        "asks_for_human": human,
    }


class KeywordDecisionProvider:
    """Implements interfaces.decision.DecisionProvider. Answers the five router questions only."""

    @property
    def name(self) -> str:
        return NAME

    @property
    def max_options(self) -> int | None:
        return None

    def decide(self, request: DecisionRequest) -> DecisionResponse:
        t0 = time.perf_counter()
        ctx = parse_input(request.input)
        last_business = next((t for r, t in reversed(ctx.earlier) if r == "business"), None)
        if ctx.earlier and ctx.earlier[-1][0] != "business":
            last_business = None  # the yes must directly follow the business's question
        out = classify(ctx.latest, ctx.has_draft, ctx.has_placed_order, last_business)
        answers: dict[str, Answer] = {}
        for q in request.questions:
            if q.name == "asks_for_human":
                answers[q.name] = Answer(
                    name=q.name, type=QuestionType.boolean, boolean=bool(out["asks_for_human"])
                )
            elif q.name == "secondary":
                value = out["secondary"]
                answers[q.name] = Answer(
                    name=q.name, type=QuestionType.choice, choice=value.value if value else NO_SECONDARY
                )
            elif q.name in out:
                answers[q.name] = Answer(name=q.name, type=QuestionType.choice, choice=out[q.name].value)
            else:
                answers[q.name] = Answer(name=q.name, type=q.type, refused=True)
        return DecisionResponse(
            provider=NAME, model=MODEL, answers=answers, latency_ms=(time.perf_counter() - t0) * 1000
        )
