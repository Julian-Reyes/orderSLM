"""Fresh4 (M6 v5): Source A chats + gold written by Claude in a Claude Code session ($0), from data/fresh4/cards.jsonl.

Same compact entries as the t6 training batch (runs/synth/t6/build.py: `I`, mods, quotes looked up in the customer
messages), plus what gold needs: a start time inside opening hours (`start="Mon 18:20"`, the week of 2026-11-23,
business-local; messages 25-50 s apart) and routing for every customer message. A routing code is the label code
(`P`, `Q/S` = secondary), optionally followed by `!t` (time_sensitive) / `!n` (needs_staff_now) / `!o` (normal) and `@d` / `@p` /
`@n` / `@u` (refers_to draft / placed_order / none / unclear); `HU` sets asks_for_human. Defaults follow the guide:
order labels refer to the draft (a MODIFY_ORDER after a CONFIRM_ORDER to the placed order, time_sensitive), a
question or small talk to the draft once an order exists (else none), status / problem / refund to the placed order.

The missing list and question come from the rules (core/finalize: the tool's one-click fill); every chat must pass
data.splits.validate. Evaluation only: training and generation never read data/fresh4 (tests/test_fresh4.py).

    uv run python runs/source-a/fresh4/build.py        # → data/fresh4/a-fresh4-NNN.json
"""

import importlib.util
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
_spec = importlib.util.spec_from_file_location("t6build", ROOT / "runs/synth/t6/build.py")
t6 = importlib.util.module_from_spec(_spec)
sys.modules["t6build"] = t6
_spec.loader.exec_module(t6)  # type: ignore[union-attr]

from orderslm.core.finalize import finalize_order  # noqa: E402
from orderslm.data import cards as card_mod  # noqa: E402
from orderslm.data.splits import dump, split_dir, validate  # noqa: E402
from orderslm.menus import load_menu  # noqa: E402
from orderslm.schema.annotation import AnnotatedConversation  # noqa: E402
from orderslm.schema.conversation import Split  # noqa: E402
from orderslm.schema.label import ModelOrder  # noqa: E402

I, add, rm, sub, offmod, note = t6.I, t6.add, t6.rm, t6.sub, t6.offmod, t6.note  # noqa: E741 (t6 names)
ANNOTATOR = "claude-opus-5.5 (Claude Code session, 2026-11-13)"
WEEK = {
    d: datetime(2026, 11, 23 + i) for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
}
t6.LABEL_CODES["PQ"] = "PAYMENT_QUESTION"  # t6's builder had no payment question
CODES = {k: v for k, v in t6.LABEL_CODES.items() if k != "H"}
ORDER = {"PLACE_ORDER", "MODIFY_ORDER", "CANCEL_ORDER", "CONFIRM_ORDER"}


@dataclass
class F(t6.X):
    start: str = "Mon 12:00"
    scenarios: list | None = None  # default: the card's
    annotation: str | None = None
    order: bool | None = None  # None: an order exists if any message is an order label or there are items


def _routing(codes: str, customer: list[int]) -> tuple[str, list[dict]]:
    out, plain, has_order, confirmed = [], [], False, False
    for i, code in zip(customer, codes.split(), strict=True):
        base, urgency, ref = code, None, None
        for flag, val in (("!t", "time_sensitive"), ("!n", "needs_staff_now"), ("!o", "normal")):
            if flag in base:
                base, urgency = base.replace(flag, ""), val
        for flag, val in (("@d", "draft"), ("@p", "placed_order"), ("@n", "none"), ("@u", "unclear")):
            if flag in base:
                base, ref = base.replace(flag, ""), val
        prim, _, sec = base.partition("/")
        p, s = CODES[prim], CODES[sec] if sec else None
        plain.append(base)
        if ref is None:
            if p in ("ORDER_STATUS", "ORDER_PROBLEM", "REFUND_REQUEST"):
                ref = "placed_order"
            elif p == "MODIFY_ORDER" and confirmed:
                ref = "placed_order"
            elif p in ORDER or s in ORDER:
                ref = "draft"
            elif p == "PAYMENT_CLAIM":
                ref = "draft" if has_order else "placed_order"
            else:
                ref = "draft" if has_order else "none"
        if urgency is None:
            urgency = "time_sensitive" if p == "MODIFY_ORDER" and ref == "placed_order" else "normal"
        has_order = has_order or p in ORDER or s in ORDER
        confirmed = confirmed or p == "CONFIRM_ORDER"
        decision = {
            "primary": p,
            "secondary": s,
            "urgency": urgency,
            "flags": {"refers_to": ref, "asks_for_human": "HUMAN_REQUEST" in (p, s)},
        }
        out.append({"message_index": i, "decision": decision})
    return " ".join(plain), out


def build(x: F, card) -> AnnotatedConversation:
    menu = load_menu(card.business_id)
    msgs = t6.parse_chat(x.chat)
    day, hhmm = x.start.split()
    h, m = map(int, hhmm.split(":"))
    at = WEEK[day].replace(hour=h, minute=m, tzinfo=ZoneInfo(menu.timezone))
    messages = []
    for i, msg in enumerate(msgs):
        if i:
            at += timedelta(seconds=25 + (i * 7) % 26)
        messages.append({"index": i, "role": msg["role"], "text": msg["text"], "sent_at": at.isoformat()})
    chat = t6.Chat(msgs)
    plain, routing = _routing(x.intents, chat.customer)
    label = t6.label_of(
        t6.X(**{**{k: getattr(x, k) for k in t6.X.__dataclass_fields__}, "intents": plain}), chat
    )
    order_labels = any(
        r["decision"]["primary"] in ORDER or r["decision"]["secondary"] in ORDER for r in routing
    )
    has_order = x.order if x.order is not None else bool(label["order"]["items"]) or order_labels
    gold = finalize_order(ModelOrder.model_validate(label["order"]), menu) if has_order else None
    return AnnotatedConversation.model_validate(
        {
            "conversation": {
                "id": card.id,
                "business_id": card.business_id,
                "split": "fresh4",
                "source": "claude_written",
                "messages": messages,
            },
            "scenarios": x.scenarios or [s.value for s in card.scenarios],
            "style": card.style.value,
            "gold_extraction": gold.model_dump(mode="json") if gold else None,
            "gold_routing": routing,
            "annotator": ANNOTATOR,
            "card_id": card.id,
            "annotation_notes": x.annotation,
        }
    )


def main() -> int:
    cards = {c.id: c for c in card_mod.load(Split.fresh4)}
    entries = []
    for path in sorted(HERE.glob("chats_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        entries += mod.ENTRIES
    problems, out = [], split_dir(Split.fresh4)
    for x in entries:
        try:
            ac = build(x, cards[x.card_id])
        except Exception as e:  # report every bad entry at once
            problems.append(f"{x.card_id}: {type(e).__name__}: {e}")
            continue
        findings = validate(ac, Split.fresh4)
        if blocking := [f for f in findings if f.blocking]:
            problems.append(f"{x.card_id}: " + "; ".join(f"{f.code} {f.message}" for f in blocking))
            continue
        for f in findings:
            print(f"warn {x.card_id}: {f.code} {f.message}")
        (out / f"{ac.conversation.id}.json").write_text(dump(ac))
    print("\n".join(problems) or f"{len(entries)} fresh4 chats written")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
