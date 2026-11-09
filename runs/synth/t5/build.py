"""Batch t5 (training data v3): chats AND labels written by hand (Claude, claude-opus-5-5, Claude Code session).

Julian, 2026-11-09: "you write and label all of them I dont want to spend more money anymore the goal is just
improve the student now." No API calls: $0.

Chats are written from each card's view (generate.card_view) under synth-write@0.2, never from dev or fresh chats.
Labels follow teacher-label@0.7 as written, except the 2026-11-03 rule (Julian): an order announced with no items
is PLACE_ORDER (the prompt still says SMALL_TALK). Every label must pass the same checks as the teacher's
(synth.label.parse_label).

Entries live in chats_*.py (ENTRIES lists of `X(...)`). Quotes are located automatically: a quote is looked up in
the customer messages (the latest one containing it unless `(index, quote)` is given), so evidence can't point at
the wrong message.

    uv run python runs/synth/t5/build.py     # → hand_chats.jsonl, gen/ (import), label_fixes/, report
"""

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.menus import load_menu
from orderslm.synth import label as lab
from orderslm.synth import run

HERE = Path(__file__).parent
BATCH = "t5"
FIXED_BY = "claude-opus-5-5 (Claude Code session, by hand)"
LABEL_CODES = {
    "P": "PLACE_ORDER",
    "M": "MODIFY_ORDER",
    "X": "CANCEL_ORDER",
    "C": "CONFIRM_ORDER",
    "Q": "MENU_QUESTION",
    "D": "DELIVERY_QUESTION",
    "H": "HOURS_QUESTION",
    "S": "SMALL_TALK",
    "U": "UNKNOWN",
    "O": "OUT_OF_SCOPE",
    "ST": "ORDER_STATUS",
    "PR": "ORDER_PROBLEM",
    "R": "REFUND_REQUEST",
    "HU": "HUMAN_REQUEST",
    "PC": "PAYMENT_CLAIM",
}


# ---------------------------------------------------------------- label pieces (quotes resolved later)


@dataclass
class Mod:
    kind: str
    modifier_id: str | None
    raw: str
    replacement: str | None = None
    amount: str = "normal"
    not_on_menu: bool = False
    kitchen_note: bool = False


def add(mid, raw, amount="normal"):
    return Mod("add", mid, raw, amount=amount)


def rm(mid, raw):
    return Mod("remove", mid, raw)


def sub(mid, repl, raw):
    return Mod("substitute", mid, raw, replacement=repl)


def offmod(raw):
    return Mod("add", None, raw, not_on_menu=True)


def note(raw):
    return Mod("add", None, raw, kitchen_note=True)


@dataclass
class I:  # noqa: E742 - an order line
    menu_item_id: str | None
    quantity: int | None
    variant: str | None
    quotes: list
    mods: list = field(default_factory=list)
    unmatched: str | None = None
    unmatched_variant: str | None = None
    combo: dict | None = None  # slot id -> choice id, or (choice id, variant id)
    halves: list | None = None  # [(menu_item_id, [Mod])]
    flag: str | None = None  # item_menu_match / item_variant


@dataclass
class X:
    card_id: str
    chat: str
    intents: str  # one code per customer message ("P P Q/S" = secondary after a slash)
    items: list = field(default_factory=list)
    method: str = "unknown"
    method_q: Any = None
    time: tuple | None = None  # (kind, raw quote, normalized or None) / ("ambiguous", raw)
    addr: dict | None = None  # {"raw": quote, "number", "street", "unit", "reference"}
    pay: str = "unknown"
    pay_q: Any = None
    change: int | None = None
    paid: bool = False
    name: str | None = None
    name_q: Any = None
    decision: str = "pending"
    decision_q: Any = None
    notes: list = field(default_factory=list)  # [(text, quote)]


# ---------------------------------------------------------------- building


def parse_chat(text: str) -> list[dict[str, str]]:
    msgs = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        role, _, said = line.partition(": ")
        msgs.append({"role": {"c": "customer", "b": "business"}[role], "text": said})
    return msgs


class Chat:
    def __init__(self, msgs):
        self.msgs = msgs
        self.customer = [i for i, m in enumerate(msgs) if m["role"] == "customer"]

    def ev(self, q):
        if q is None:
            return []
        if isinstance(q, list):
            return [e for x in q for e in self.ev(x)]
        if isinstance(q, tuple):
            i, text = q
            if self.msgs[i]["role"] != "customer" or text not in self.msgs[i]["text"]:
                raise ValueError(f"quote {text!r} not in customer message {i}")
            return [{"message_index": i, "quote": text}]
        hits = [i for i in self.customer if q in self.msgs[i]["text"]]
        if not hits:
            raise ValueError(f"quote {q!r} not in any customer message")
        return [{"message_index": hits[-1], "quote": q}]


def mod_json(m: Mod) -> dict[str, Any]:
    return {
        "kind": m.kind,
        "modifier_id": m.modifier_id,
        "replacement_modifier_id": m.replacement,
        "amount": m.amount,
        "raw_text": m.raw,
        "not_on_menu": m.not_on_menu,
        "kitchen_note": m.kitchen_note,
    }


def label_of(x: X, chat: Chat) -> dict[str, Any]:
    codes = x.intents.split()
    if len(codes) != len(chat.customer):
        raise ValueError(f"{len(codes)} intents for {len(chat.customer)} customer messages")
    intents = []
    for i, code in zip(chat.customer, codes, strict=True):
        primary, _, secondary = code.partition("/")
        intents.append(
            {
                "message_index": i,
                "primary": LABEL_CODES[primary],
                "secondary": LABEL_CODES[secondary] if secondary else None,
            }
        )
    items, flags = [], []
    for n, it in enumerate(x.items, start=1):
        line = f"L{n}"
        items.append(
            {
                "line_id": line,
                "menu_item_id": it.menu_item_id,
                "unmatched_text": it.unmatched,
                "halves": (
                    [
                        {"menu_item_id": h, "modifications": [mod_json(m) for m in mods]}
                        for h, mods in it.halves
                    ]
                    if it.halves
                    else None
                ),
                "quantity": it.quantity,
                "variant_id": it.variant,
                "unmatched_variant_text": it.unmatched_variant,
                "modifications": [mod_json(m) for m in it.mods],
                "combo_selections": [
                    {
                        "slot_id": slot,
                        "menu_item_id": pick if isinstance(pick, str) else pick[0],
                        "variant_id": None if isinstance(pick, str) else pick[1],
                    }
                    for slot, pick in (it.combo or {}).items()
                ],
                "notes": None,
                "evidence": chat.ev(it.quotes),
            }
        )
        if it.flag:
            flags.append({"field": it.flag, "line_id": line})
    if x.time is None:
        when = {
            "state": "not_mentioned",
            "kind": None,
            "raw_text": None,
            "normalized_local": None,
            "evidence": [],
        }
    elif x.time[0] == "ambiguous":
        when = {
            "state": "ambiguous",
            "kind": None,
            "raw_text": x.time[1],
            "normalized_local": None,
            "evidence": chat.ev(x.time[1]),
        }
    else:
        kind, raw, norm = x.time
        when = {
            "state": "provided",
            "kind": kind,
            "raw_text": raw,
            "normalized_local": norm,
            "evidence": chat.ev(raw),
        }
    if x.method == "pickup":
        address = {"state": "not_applicable"}
    elif x.addr:
        address = {
            "state": "provided",
            **{k: x.addr.get(k) for k in ("street", "number", "unit", "reference")},
        }
        address["raw_text"] = x.addr["raw"]
        address["evidence"] = chat.ev(x.addr.get("q", x.addr["raw"]))
    else:
        address = {"state": "not_mentioned"}
    for k in ("street", "number", "unit", "reference", "raw_text"):
        address.setdefault(k, None)
    address.setdefault("evidence", [])
    order = {
        "items": items,
        "fulfillment": {"method": x.method, "method_evidence": chat.ev(x.method_q), "requested_time": when},
        "address": address,
        "payment": {
            "method": x.pay,
            "change_for_cents": x.change,
            "customer_claims_paid": x.paid,
            "evidence": chat.ev(x.pay_q),
        },
        "customer_name": {
            "state": "provided" if x.name else "not_mentioned",
            "value": x.name,
            "evidence": chat.ev(x.name_q if x.name_q is not None else x.name),
        },
        "customer_decision": {
            "state": x.decision,
            "agreed_while_incomplete": False,
            "evidence": chat.ev(x.decision_q),
        },
        "notes": [{"text": t, "evidence": chat.ev(q)} for t, q in x.notes],
        "ambiguity_flags": flags,
    }
    if not x.name:
        order["customer_name"]["evidence"] = []
    return {"schema_version": "label@0.1", "intents": intents, "order": order}


def load_entries() -> list[X]:
    entries: list[X] = []
    for path in sorted(HERE.glob("chats_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[path.stem] = mod
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        entries += mod.ENTRIES
    ids = [e.card_id for e in entries]
    if dupes := {i for i in ids if ids.count(i) > 1}:
        raise SystemExit(f"duplicate entries: {sorted(dupes)}")
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args()
    cards = {c.id: c for c in run.load_cards(BATCH)}
    entries = load_entries()
    rows, labels, problems = [], {}, []
    for x in entries:
        card = cards.get(x.card_id)
        if card is None:
            problems.append(f"{x.card_id}: no such card")
            continue
        msgs = parse_chat(x.chat)
        try:
            label = label_of(x, Chat(msgs))
        except (ValueError, KeyError) as e:
            problems.append(f"{x.card_id}: {e}")
            continue
        rows.append({"card_id": x.card_id, "messages": msgs})
        labels[x.card_id] = label
    if problems:
        print("\n".join(problems))
        return 1
    # import the chats (writer checks run in collect), then check every label against its conversation
    chats_file = HERE / "hand_chats.jsonl"
    if not args.check:
        chats_file.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        run.import_chats(argparse.Namespace(batch=BATCH, file=str(chats_file)))
    convs = {s.card_id: s.conversation for s in run.load_conversations(BATCH)} if not args.check else {}
    if args.check:  # build conversations in memory the same way collect would
        from orderslm.schema.conversation import Conversation  # noqa: F401  (validated on import)
    out = run.batch_dir(BATCH) / "label_fixes"
    out.mkdir(exist_ok=True)
    now = datetime.now(UTC).isoformat()
    bad = []
    for cid, label in labels.items():
        if args.check:
            continue
        conv = convs.get(cid)
        if conv is None:
            bad.append(f"{cid}: chat dropped by the writer checks (see gen_drops.jsonl)")
            continue
        lc, why = lab.parse_label(json.dumps(label), conv, load_menu(conv.business_id), FIXED_BY)
        if lc is None:
            bad.append(f"{cid}: {why}")
            continue
        record = {
            "card_id": cid,
            "kind": "hand_label",
            "reason": "training data v3: chat and label written by hand (Julian, 2026-11-09: no API spend)",
            "fixed_by": FIXED_BY,
            "fixed_at": now,
            "label_prompt_version": run.HAND_LABEL_VERSION,
            "label": label,
        }
        (out / f"{cid}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    if bad:
        print("\n".join(bad))
        return 1
    print(f"{len(labels)} chats and labels {'checked' if args.check else 'written'} for batch {BATCH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
