"""Rules baseline extractor: regex + menu matching, no model (spec §10, "Rules baseline").

Its job is to show why the task is hard, not to be good. It reads customer
messages in order and handles the common patterns: quantities, sizes, add/remove/
extra/light, "swap X for Y", "make it N", "make one of them ...", removing an
item, cancelling, a contextual "yes", pickup/delivery, addresses, times, payment,
payment claims and names. Anything else it misses. It always returns schema-valid
output, built through the same parse path as model outputs.
"""

import re
import time as _time
from dataclasses import dataclass, field
from datetime import time

from orderslm.core.matching import Kind, Match, MenuLexicon, lower_same_length, quantity_before
from orderslm.core.missing import required_missing
from orderslm.core.replies import template_question
from orderslm.interfaces.extractor import ExtractionRequest, ExtractionResult, parse_model_output
from orderslm.schema.conversation import Message, Role
from orderslm.schema.extraction import (
    Address,
    Amount,
    CustomerDecision,
    CustomerName,
    DecisionState,
    Evidence,
    ExtractionOutput,
    Fulfillment,
    FulfillmentMethod,
    HalfSelection,
    ItemProposal,
    Modification,
    ModificationKind,
    Payment,
    PaymentMethod,
    RequestedTime,
    SlotState,
    TimeKind,
)
from orderslm.schema.menu import MenuCatalog

NAME = "rules/extractor@0.1"

# ---- cue patterns (lowercase text)
REMOVE_CUES = r"no|without|hold the|hold|minus|w/o"
EXTRA_CUES = r"extra|double|lots of|a lot of|heavy on(?: the)?|more"
LIGHT_CUES = (
    r"light on(?: the)?|light|easy on(?: the)?|a little(?: bit of)?|just a little|go light on(?: the)?"
)
ADD_CUES = r"with|add|plus|w/|w|and|topped with|on"
CUE_RX = re.compile(
    rf"(?<![a-z])(?P<cue>{REMOVE_CUES}|{EXTRA_CUES}|{LIGHT_CUES}|{ADD_CUES})\s+(?:[a-z]+\s+)?$"
)
AFFIRM = re.compile(r"^\W*(yes|yep|yeah|yup|ya|yea|correct|that'?s right|sounds good|perfect|ok|okay|sure)\b")
CANCEL_ALL = re.compile(
    r"\bcancel\b(?:\s+(?:it|that|the order|my order|everything|all|the whole (?:thing|order)))?(?!\s+the\s+\w)"
)
SWAP = re.compile(
    r"\b(?:swap|switch|change|replace)\s+(?:the\s+|my\s+)?(?P<x>[a-z0-9 '-]+?)\s+(?:for|to|with)\s+(?P<y>[a-z0-9 '-]+)"
)
INSTEAD = re.compile(r"(?P<y>[a-z0-9 '-]+?)\s+instead of\s+(?:the\s+|a\s+)?(?P<x>[a-z0-9 '-]+)")
MAKE_IT = re.compile(r"\bmake (?:it|that|them)\s+(?P<n>\d{1,2}|two|three|four|five|six)\b")
MAKE_ONE = re.compile(r"\bmake one of (?:them|those|the \w+)\b")
REMOVE_ITEM = re.compile(r"\b(?:remove|take off|no more|drop|scratch|forget|cancel)\s+(?:the\s+|that\s+)?")
PICKUP = re.compile(r"\b(pick\s?up|pick it up|picking up|collect|carry ?out|take ?out|to go)\b")
DELIVERY = re.compile(r"\b(deliver(?:y|ed)?|bring it|send it)\b")
DELIVERY_QUESTION = re.compile(r"\b(?:do|can|will|d'?you)\s+(?:you|u|y'?all)(?:\s+guys)?\s+deliver\b")
ASAP = re.compile(r"\b(asap|as soon as (?:possible|you can|u can)|right now)\b")
CLOCK = re.compile(
    r"\b(?:at|by|around)\s+(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>am|pm|a\.m\.|p\.m\.)?(?![\d:])"
)
BARE_CLOCK = re.compile(r"\b(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>am|pm)\b")
RELATIVE = re.compile(
    r"\bin\s+(?:about\s+)?(?:\d{1,3}|an?|half an)\s*(?:min|mins|minutes|hour|hr|hrs|hours)\b"
)
CASH = re.compile(r"\bcash\b")
CARD = re.compile(r"\b(card|credit|debit|apple pay|google pay|visa|amex|mastercard)\b")
CHANGE = re.compile(r"\bchange for (?:a\s+)?\$?(?P<n>\d{1,3})\b")
CLAIM = re.compile(
    r"\b(already paid|i paid|just paid|paid already|paid online|paid on the app|sent (?:the |u |you )?(?:payment|money))\b"
)
NAME_RX = re.compile(
    r"\b(?:my name is|my name's|name's|name is|it'?s for|under(?: the name)?)\s+(?P<n>[a-z][a-z'-]{1,20})\b",
    re.I,
)
ADDRESS = re.compile(
    r"\b(?P<num>\d{1,5})\s+(?P<street>(?:[a-z0-9]+\s){0,3}?(?:st|street|ave|avenue|rd|road|blvd|boulevard|ln|lane|dr|drive|way|ct|court|pl|place|pkwy|parkway|ter|terrace)\b\.?)"
    r"(?:,?\s*(?:apt|apartment|unit|suite|ste|#)\.?\s*(?P<unit>[a-z0-9-]+))?",
    re.I,
)
NOT_NAMES = {
    "pickup",
    "delivery",
    "here",
    "my",
    "me",
    "the",
    "a",
    "an",
    "him",
    "her",
    "them",
    "us",
    "you",
    "u",
    "now",
    "later",
    "today",
    "tonight",
    "lunch",
    "dinner",
}
NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6}


@dataclass
class Line:
    line_id: str
    item_id: str | None = None
    halves: list[str] | None = None
    quantity: int | None = 1
    variant_id: str | None = None
    mods: list[Modification] = field(default_factory=list)
    combo: dict[str, str] = field(default_factory=dict)
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class State:
    lines: list[Line] = field(default_factory=list)
    next_id: int = 1
    method: FulfillmentMethod = FulfillmentMethod.unknown
    method_ev: list[Evidence] = field(default_factory=list)
    time: RequestedTime = field(default_factory=lambda: RequestedTime(state=SlotState.not_mentioned))
    address: Address = field(default_factory=lambda: Address(state=SlotState.not_mentioned))
    pay_method: PaymentMethod = PaymentMethod.unknown
    change_for: int | None = None
    claims_paid: bool = False
    pay_ev: list[Evidence] = field(default_factory=list)
    name: CustomerName = field(default_factory=lambda: CustomerName(state=SlotState.not_mentioned))
    decision: DecisionState = DecisionState.pending
    decision_ev: list[Evidence] = field(default_factory=list)

    def new_line(self, **kw) -> Line:
        line = Line(line_id=f"L{self.next_id}", **kw)
        self.next_id += 1
        self.lines.append(line)
        return line


def _ev(msg: Message, start: int, end: int) -> Evidence:
    return Evidence(message_index=msg.index, quote=msg.text[start:end].strip() or msg.text)


class _Parser:
    def __init__(self, menu: MenuCatalog):
        self.menu = menu
        self.lex = MenuLexicon(menu)
        self.plain_pizza = next((i.id for i in menu.items if i.splittable and "pizza" in i.aliases), None)

    # ---------------------------------------------------------------- helpers
    def _line_for(self, st: State, text_low: str) -> Line | None:
        """The existing line whose item is mentioned in this text."""
        ids = {m.target for m in self.lex.find(text_low, {Kind.item})}
        for line in reversed(st.lines):
            if line.item_id in ids:
                return line
        return None

    def _variant_near(self, item_id: str, matches: list[Match], lo: int, hi: int) -> Match | None:
        for m in matches:
            if (
                m.kind is Kind.variant
                and lo <= m.start
                and m.end <= hi
                and m.target.startswith(f"{item_id}:")
            ):
                return m
        return None

    def _mods_in(
        self, msg: Message, low: str, item_ids: list[str], matches: list[Match], lo: int, hi: int
    ) -> list[Modification]:
        allowed: set[str] = set()
        for iid in item_ids:
            if (it := self.menu.item(iid)) is not None:
                allowed |= it.allowed_modifier_ids
        mods: list[Modification] = []
        last_cue: str | None = None
        prev_end = lo
        for m in matches:
            if m.kind is not Kind.modifier or not (lo <= m.start and m.end <= hi) or m.target not in allowed:
                continue
            window = low[prev_end : m.start]
            cue_m = CUE_RX.search(window)
            cue = cue_m.group("cue") if cue_m else None
            if cue in (None, "and", "w", "on") and last_cue is not None:
                cue = last_cue  # "no onions and pickles" -> both removed
            prev_end = m.end
            start = cue_m.start("cue") + (m.start - len(window)) if cue_m else m.start
            raw = msg.text[start : m.end]
            if cue and re.fullmatch(REMOVE_CUES, cue):
                mods.append(Modification(kind=ModificationKind.remove, modifier_id=m.target, raw_text=raw))
            elif cue and re.fullmatch(EXTRA_CUES, cue):
                mods.append(
                    Modification(
                        kind=ModificationKind.add, modifier_id=m.target, amount=Amount.extra, raw_text=raw
                    )
                )
            elif cue and re.fullmatch(LIGHT_CUES, cue):
                mods.append(
                    Modification(
                        kind=ModificationKind.add, modifier_id=m.target, amount=Amount.light, raw_text=raw
                    )
                )
            else:
                mods.append(Modification(kind=ModificationKind.add, modifier_id=m.target, raw_text=raw))
            last_cue = cue
        return mods

    # ---------------------------------------------------------------- per message
    def message(self, st: State, msg: Message, previous: Message | None) -> None:
        low = lower_same_length(msg.text)
        consumed: list[tuple[int, int]] = []
        changed = False

        if previous is not None and previous.role is Role.business and previous.text.rstrip().endswith("?"):
            if (a := AFFIRM.search(low)) and st.lines:
                st.decision, st.decision_ev = DecisionState.confirmed, [_ev(msg, a.start(1), a.end(1))]
                consumed.append(a.span())

        changed |= self._corrections(st, msg, low, consumed)
        if (c := CANCEL_ALL.search(low)) and not any(a <= c.start() < b for a, b in consumed):
            st.decision, st.decision_ev = DecisionState.cancelled, [_ev(msg, c.start(), c.end())]
            return
        changed |= self._new_items(st, msg, low, consumed)
        changed |= self._details(st, msg, low)
        if (
            changed
            and st.decision is DecisionState.confirmed
            and st.decision_ev[0].message_index != msg.index
        ):
            st.decision, st.decision_ev = DecisionState.pending, []  # a change needs a new "yes"

    def _corrections(self, st: State, msg: Message, low: str, consumed: list[tuple[int, int]]) -> bool:
        changed = False
        for rx in (SWAP, INSTEAD):
            for m in rx.finditer(low):
                old = self._line_for(st, m.group("x"))
                new_items = self.lex.find(m.group("y"), {Kind.item})
                if old is None or not new_items:
                    continue
                st.lines.remove(old)
                st.new_line(
                    item_id=new_items[0].target,
                    quantity=old.quantity,
                    evidence=[_ev(msg, m.start(), m.end())],
                )
                consumed.append(m.span())
                changed = True
        for m in MAKE_IT.finditer(low):
            target = self._line_for(st, low[m.end() :]) or (st.lines[-1] if st.lines else None)
            if target is not None:
                n = m.group("n")
                target.quantity = int(n) if n.isdigit() else NUM[n]
                target.evidence.append(_ev(msg, m.start(), min(len(low), m.end() + 30)))
                consumed.append((m.start(), len(low)))
                changed = True
        if (m := MAKE_ONE.search(low)) is not None:
            src = next((ln for ln in reversed(st.lines) if (ln.quantity or 0) > 1), None)
            if src is not None and src.item_id:
                matches = self.lex.find(msg.text)
                mods = self._mods_in(msg, low, [src.item_id], matches, m.end(), len(low))
                if mods:
                    src.quantity = (src.quantity or 2) - 1
                    st.new_line(item_id=src.item_id, variant_id=src.variant_id, quantity=1,
                                mods=[*src.mods, *mods], evidence=[*src.evidence, _ev(msg, m.start(), len(low))])  # fmt: skip
                    consumed.append((m.start(), len(low)))
                    changed = True
        for m in REMOVE_ITEM.finditer(low):
            rest = low[m.end() : m.end() + 40]
            hit = self.lex.find(rest, {Kind.item})
            if hit and hit[0].start == 0 and (line := self._line_for(st, rest[: hit[0].end])) is not None:
                st.lines.remove(line)
                consumed.append((m.start(), m.end() + hit[0].end))
                changed = True
        return changed

    def _new_items(self, st: State, msg: Message, low: str, consumed: list[tuple[int, int]]) -> bool:
        matches = [m for m in self.lex.find(msg.text) if not any(a <= m.start < b for a, b in consumed)]
        if (
            h := re.search(r"\bhalf\s+(?P<a>[a-z' -]+?)\s*(?:and\s+|/\s*)?half\s+(?P<b>[a-z' -]+)", low)
        ) and self.plain_pizza:
            halves = []
            for grp in ("a", "b"):
                seg = [m for m in matches if h.start(grp) <= m.start < h.end(grp)]
                item = next(
                    (m.target for m in seg if m.kind is Kind.item and self.menu.item(m.target).splittable),
                    None,
                )
                halves.append(item or self.plain_pizza)
            variant = next((m.target.split(":")[1] for m in matches if m.kind is Kind.variant
                            and m.target.startswith(f"{self.plain_pizza}:") and m.end <= h.end()), None)  # fmt: skip
            qty, _ = quantity_before(low[: h.start()])
            st.new_line(
                halves=halves,
                variant_id=variant,
                quantity=qty,
                evidence=[_ev(msg, max(0, h.start() - 15), h.end())],
            )
            consumed.append((max(0, h.start() - 15), h.end()))
            matches = [m for m in matches if not (h.start() - 15 <= m.start < h.end())]
            # the pizza word itself ("large pizza half ...") belongs to this line
            matches = [
                m
                for m in matches
                if not (m.kind is Kind.item and m.target == self.plain_pizza and m.end <= h.start())
            ]

        items: list[Match] = []
        for m in (x for x in matches if x.kind is Kind.item):
            # A topping named like a pizza ("with pepperoni") right after a cue is a modifier of the previous item.
            prev = items[-1] if items else None
            if prev is not None and CUE_RX.search(low[prev.end : m.start]):
                allowed = self.menu.item(prev.target).allowed_modifier_ids
                if any(
                    x.kind is Kind.modifier and x.start == m.start and x.target in allowed for x in matches
                ):
                    continue
            items.append(m)
        changed = False
        combo_line: Line | None = None
        for k, m in enumerate(items):
            seg_hi = items[k + 1].start if k + 1 < len(items) else len(low)
            seg_lo = items[k - 1].end if k > 0 else 0
            # A valid combo choice right after a combo item fills its slot.
            if combo_line is not None and combo_line.item_id:
                combo = self.menu.item(combo_line.item_id)
                slot = next(
                    (s for s in combo.combo_slots if m.target in s.choices and s.id not in combo_line.combo),
                    None,
                )
                if slot is not None:
                    combo_line.combo[slot.id] = m.target
                    combo_line.evidence[0] = _ev(msg, msg.text.find(combo_line.evidence[0].quote), m.end)
                    continue
            qty, _ = quantity_before(low[seg_lo : m.start])
            variant = self._variant_near(m.target, matches, max(seg_lo, m.start - 25), seg_hi)
            q_start = m.start
            if qm := re.search(
                r"(\d{1,2}|an?|another|two|three|four|five|six|some|a couple(?: of)?)\s+(?:[a-z0-9-]+\s+){0,2}$",
                low[seg_lo : m.start],
            ):
                q_start = seg_lo + qm.start()
            if variant is not None and variant.start < q_start:
                q_start = variant.start
            line = st.new_line(
                item_id=m.target,
                quantity=qty,
                variant_id=variant.target.split(":")[1] if variant else None,
                mods=self._mods_in(msg, low, [m.target], matches, m.end, seg_hi),
                evidence=[_ev(msg, q_start, m.end)],
            )
            combo_line = line if self.menu.item(m.target).combo_slots else None
            changed = True
        return changed

    def _details(self, st: State, msg: Message, low: str) -> bool:
        changed = False
        if (m := PICKUP.search(low)) is not None:
            st.method, st.method_ev, changed = FulfillmentMethod.pickup, [_ev(msg, m.start(), m.end())], True
        elif (m := DELIVERY.search(low)) is not None and not DELIVERY_QUESTION.search(low):
            st.method, st.method_ev, changed = (
                FulfillmentMethod.delivery,
                [_ev(msg, m.start(), m.end())],
                True,
            )
        if (a := ADDRESS.search(msg.text)) is not None:
            st.address = Address(
                state=SlotState.provided,
                number=a.group("num"),
                street=a.group("street").strip().rstrip("."),
                unit=a.group("unit"),
                raw_text=a.group(0).strip(),
                evidence=[_ev(msg, a.start(), a.end())],
            )
            changed = True
        changed |= self._time(st, msg, low)
        if (m := CASH.search(low)) is not None:
            st.pay_method, changed = PaymentMethod.cash, True
            st.pay_ev = [e for e in st.pay_ev if e.message_index != msg.index] + [
                _ev(msg, m.start(), m.end())
            ]
        elif (m := CARD.search(low)) is not None:
            st.pay_method, changed = PaymentMethod.card, True
            st.pay_ev = [e for e in st.pay_ev if e.message_index != msg.index] + [
                _ev(msg, m.start(), m.end())
            ]
        if (m := CHANGE.search(low)) is not None and st.pay_method is PaymentMethod.cash:
            st.change_for = int(m.group("n")) * 100
        if (m := CLAIM.search(low)) is not None:
            st.claims_paid, changed = True, True
            st.pay_ev.append(_ev(msg, m.start(), m.end()))
        if (m := NAME_RX.search(msg.text)) is not None and m.group("n").lower() not in NOT_NAMES:
            st.name = CustomerName(
                state=SlotState.provided,
                value=m.group("n").capitalize(),
                evidence=[_ev(msg, m.start(), m.end())],
            )
            changed = True
        return changed

    def _time(self, st: State, msg: Message, low: str) -> bool:
        if (m := ASAP.search(low)) is not None:
            st.time = RequestedTime(
                state=SlotState.provided,
                kind=TimeKind.asap,
                raw_text=m.group(0),
                evidence=[_ev(msg, m.start(), m.end())],
            )
            return True
        if (m := RELATIVE.search(low)) is not None:
            st.time = RequestedTime(
                state=SlotState.provided,
                kind=TimeKind.relative,
                raw_text=m.group(0),
                evidence=[_ev(msg, m.start(), m.end())],
            )
            return True
        addr = ADDRESS.search(msg.text)
        candidates = [c for rx in (CLOCK, BARE_CLOCK) for c in rx.finditer(low)]
        candidates = [
            c
            for c in candidates
            if int(c.group("h")) <= 23 and not (addr and addr.start() <= c.start("h") < addr.end())
        ]
        if not candidates:
            return False
        m = candidates[0]
        st.time = RequestedTime(
            state=SlotState.provided,
            kind=TimeKind.clock_time,
            raw_text=msg.text[m.start() : m.end()].strip(),
            normalized_local=self._normalize(int(m.group("h")), int(m.group("m") or 0), m.group("ap")),
            evidence=[_ev(msg, m.start(), m.end())],
        )
        return True

    def _normalize(self, h: int, mi: int, ap: str | None) -> str | None:
        """HH:MM only when unambiguous: am/pm stated, or exactly one reading falls within opening hours."""
        if ap:
            h = h % 12 + (12 if ap.startswith("p") else 0)
            return f"{h:02d}:{mi:02d}"
        if h >= 13:
            return f"{h:02d}:{mi:02d}"
        opens, closes = self.menu.opens_at, self.menu.closes_at
        fits = [c for c in {h % 12, h % 12 + 12} if opens <= time(c, mi) <= closes]
        return f"{fits[0]:02d}:{mi:02d}" if len(fits) == 1 else None

    # ---------------------------------------------------------------- output
    def output(self, st: State) -> ExtractionOutput:
        items = []
        for line in st.lines:
            if line.quantity == 0:
                continue
            ev = list({(e.message_index, e.quote): e for e in line.evidence}.values())
            if line.halves:
                items.append(ItemProposal(line_id=line.line_id, halves=[HalfSelection(menu_item_id=h) for h in line.halves],
                                          quantity=line.quantity, variant_id=line.variant_id, evidence=ev))  # fmt: skip
            else:
                items.append(ItemProposal(
                    line_id=line.line_id, menu_item_id=line.item_id, quantity=line.quantity, variant_id=line.variant_id,
                    modifications=line.mods, evidence=ev,
                    combo_selections=[{"slot_id": s, "menu_item_id": i} for s, i in line.combo.items()],
                ))  # fmt: skip
        method = st.method
        address = (
            Address(state=SlotState.not_applicable) if method is FulfillmentMethod.pickup else st.address
        )
        time_ = st.time  # a clock time without a unique reading stays provided, just not normalized
        payment = Payment(
            method=st.pay_method,
            change_for_cents=st.change_for if st.pay_method is PaymentMethod.cash else None,
            customer_claims_paid=st.claims_paid,
            evidence=st.pay_ev if (st.pay_method is not PaymentMethod.unknown or st.claims_paid) else [],
        )
        draft = ExtractionOutput(
            items=items,
            fulfillment=Fulfillment(method=method, method_evidence=st.method_ev, requested_time=time_),
            address=address,
            payment=payment,
            customer_name=st.name,
            customer_decision=CustomerDecision(state=st.decision, evidence=st.decision_ev),
        )
        missing = required_missing(draft, self.menu)
        if missing:
            draft.missing_or_ambiguous = missing
            draft.clarification_question = template_question(missing, draft, self.menu)
        return ExtractionOutput.model_validate(draft.model_dump())


def extract_rules(menu: MenuCatalog, messages: list[Message]) -> ExtractionOutput:
    parser = _Parser(menu)
    st = State()
    previous: Message | None = None
    for msg in messages:
        if msg.role is Role.customer:
            parser.message(st, msg, previous)
        previous = msg
    return parser.output(st)


class RulesExtractor:
    """OrderExtractor over the full conversation. The draft in the request is ignored: rules re-read everything."""

    @property
    def name(self) -> str:
        return NAME

    def extract(self, request: ExtractionRequest) -> ExtractionResult:
        t0 = _time.perf_counter()
        try:
            raw = extract_rules(request.menu, request.conversation.messages).model_dump_json()
        except Exception as e:  # a baseline bug must show up as an invalid output, not crash an eval
            raw = f"rules extractor error: {type(e).__name__}: {e}"
        return parse_model_output(NAME, raw, latency_ms=(_time.perf_counter() - t0) * 1000)
