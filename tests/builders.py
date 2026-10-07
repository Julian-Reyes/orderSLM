"""Terse constructors for orders and conversations in tests."""

from datetime import UTC, datetime, timedelta

from orderslm.schema.conversation import Conversation, Message
from orderslm.schema.extraction import ExtractionOutput

EV = [{"message_index": 0, "quote": "x"}]
T0 = datetime(2026, 10, 7, 18, 0, tzinfo=UTC)


def line(line_id: str, item: str | None = None, qty: int | None = 1, variant: str | None = None, mods=(), combo=(),
         halves=None, unmatched: str | None = None) -> dict:  # fmt: skip
    d: dict = {"line_id": line_id, "quantity": qty, "evidence": EV}
    if item:
        d["menu_item_id"] = item
    if variant:
        d["variant_id"] = variant
    if mods:
        d["modifications"] = [mod(*m) if isinstance(m, tuple) else m for m in mods]
    if combo:
        d["combo_selections"] = [
            {"slot_id": c[0], "menu_item_id": c[1], **({"variant_id": c[2]} if len(c) > 2 else {})}
            for c in combo
        ]
    if halves:
        d["halves"] = [{"menu_item_id": h} if isinstance(h, str) else h for h in halves]
    if unmatched:
        d["unmatched_text"] = unmatched
    return d


def mod(kind: str, modifier_id: str | None, amount: str = "normal", replacement: str | None = None) -> dict:
    d = {"kind": kind, "modifier_id": modifier_id, "amount": amount, "raw_text": f"{kind} {modifier_id}"}
    if replacement:
        d["replacement_modifier_id"] = replacement
    return d


def order(*lines: dict, method: str = "pickup", payment: str = "cash", address: str | None = None,
          name: str | None = None, decision: str = "pending", missing=(), question: str | None = None,
          time_: dict | None = None, claims_paid: bool = False) -> ExtractionOutput:  # fmt: skip
    if method == "pickup":
        addr = {"state": "not_applicable"}
    elif address:
        addr = {"state": "provided", "raw_text": address, "evidence": EV}
    else:
        addr = {"state": "not_mentioned"}
    pay: dict = {"method": payment, "customer_claims_paid": claims_paid}
    if payment != "unknown" or claims_paid:
        pay["evidence"] = EV
    return ExtractionOutput.model_validate(
        {
            "items": list(lines),
            "fulfillment": {
                "method": method,
                "method_evidence": EV if method != "unknown" else [],
                "requested_time": time_ or {"state": "not_mentioned"},
            },
            "address": addr,
            "payment": pay,
            "customer_name": {"state": "provided", "value": name, "evidence": EV}
            if name
            else {"state": "not_mentioned"},
            "customer_decision": {"state": decision, "evidence": EV if decision != "pending" else []},
            "missing_or_ambiguous": [
                dict(zip(("field", "reason", "line_id"), m, strict=False)) for m in missing
            ],
            "clarification_question": question,
        }
    )


def conversation(
    *messages: tuple[str, str], business: str = "corner-patty", cid: str = "t-1"
) -> Conversation:
    return Conversation(
        id=cid,
        business_id=business,
        split="dev",
        source="human",
        messages=[
            Message(index=i, role=role, text=text, sent_at=T0 + timedelta(seconds=10 * i))
            for i, (role, text) in enumerate(messages)
        ],
    )
