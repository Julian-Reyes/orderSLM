"""A gold extraction in plain English, for reviewers (the annotation tool's "Plain English" view).

Read-only and lossless enough to review against: every item, option, field and evidence quote is shown,
with names from the menu. Editing still happens in the JSON. English only (it's a reviewer aid, not a
customer reply).
"""

from orderslm.core.requests import RequestStatus, request_status
from orderslm.domain.money import format_cents
from orderslm.schema.common import Evidence
from orderslm.schema.extraction import (
    Amount,
    DecisionState,
    ExtractionOutput,
    FulfillmentMethod,
    ItemProposal,
    MissingReason,
    Modification,
    ModificationKind,
    PaymentMethod,
    SlotState,
)
from orderslm.schema.menu import MenuCatalog, MenuItem

FIELD_NAMES = {
    "items": "what to order",
    "item_menu_match": "which menu item",
    "item_quantity": "how many",
    "item_variant": "size / flavor",
    "item_modification": "a requested option",
    "combo_choice": "a combo choice",
    "fulfillment_method": "pickup or delivery",
    "requested_time": "the time",
    "address": "the delivery address",
    "payment_method": "how they'll pay",
    "customer_name": "a name for the order",
}
REASONS = {
    MissingReason.missing: "not given",
    MissingReason.ambiguous: "unclear",
    MissingReason.off_menu: "not on the menu",
    MissingReason.conflicting: "conflicting",
}


def _ev(evidence: list[Evidence]) -> str:
    return "   ← " + ", ".join(f"#{e.message_index} “{e.quote}”" for e in evidence) if evidence else ""


def _mod_name(menu: MenuCatalog, modifier_id: str | None) -> str:
    m = menu.modifier(modifier_id) if modifier_id else None
    return m.name.lower() if m else str(modifier_id)


def _mod(menu: MenuCatalog, item: MenuItem | None, mod: Modification) -> str:
    status = request_status(menu, item, mod)
    if status is RequestStatus.kitchen_note:
        return f"kitchen note: “{mod.raw_text}”"
    if status is RequestStatus.not_on_menu:
        return f"NOT ON THE MENU: “{mod.raw_text}”"
    if status is RequestStatus.unverified:
        flag = (
            "marked kitchen note, but not on the menu's accepted list" if mod.kitchen_note else "unclassified"
        )
        return f"UNVERIFIED request ({flag}): “{mod.raw_text}”"
    if mod.kind is ModificationKind.remove:
        return f"no {_mod_name(menu, mod.modifier_id)}"
    if mod.kind is ModificationKind.substitute:
        return f"{_mod_name(menu, mod.replacement_modifier_id)} instead of {_mod_name(menu, mod.modifier_id)}"
    name = _mod_name(menu, mod.modifier_id)
    included = item is not None and mod.modifier_id in item.ingredient_ids
    if mod.amount is Amount.extra:
        return f"extra {name}"
    if mod.amount is Amount.light:
        return f"light {name}"
    return f"with {name} (already included)" if included else f"add {name}"


def _size(item: MenuItem | None, line: ItemProposal) -> str:
    if item is None or not item.variants:
        return ""
    if line.variant_id and (v := item.variant(line.variant_id)):
        return f", {v.name}"
    if line.unmatched_variant_text:
        return f", size “{line.unmatched_variant_text}” (not a size we have)"
    if item.default_variant_id and (v := item.variant(item.default_variant_id)):
        return f", {v.name} (default; not stated)"
    return ", size not stated"


def _item(menu: MenuCatalog, line: ItemProposal, out: ExtractionOutput) -> str:
    qty = f"{line.quantity} ×" if line.quantity is not None else "? × (quantity unclear)"
    if line.unmatched_text is not None:
        reasons = {m.reason for m in out.missing_or_ambiguous if m.line_id == line.line_id}
        kind = "UNCLEAR ITEM" if MissingReason.ambiguous in reasons else "NOT ON THE MENU"
        return f"{line.line_id}  {qty} {kind}: “{line.unmatched_text}”"
    if line.halves:
        halves = [(menu.item(h.menu_item_id), h) for h in line.halves]
        first = halves[0][0]
        parts = []
        for it, h in halves:
            mods = "; ".join(_mod(menu, it, m) for m in h.modifications)
            parts.append(f"half {it.name if it else h.menu_item_id}" + (f" ({mods})" if mods else ""))
        return f"{line.line_id}  {qty} Pizza{_size(first, line)}: {' / '.join(parts)}"
    item = menu.item(line.menu_item_id or "")
    text = f"{line.line_id}  {qty} {item.name if item else line.menu_item_id}{_size(item, line)}"
    details = [_mod(menu, item, m) for m in line.modifications]
    for sel in line.combo_selections:
        choice = menu.item(sel.menu_item_id)
        v = choice.variant(sel.variant_id) if choice and sel.variant_id else None
        details.append(
            f"{sel.slot_id}: {choice.name if choice else sel.menu_item_id}" + (f" ({v.name})" if v else "")
        )
    if line.notes:
        details.append(f"note: {line.notes}")
    return text + (f" — {'; '.join(details)}" if details else "")


def describe_gold(out: ExtractionOutput, menu: MenuCatalog) -> list[str]:
    lines = ["ITEMS"] + (
        [_item(menu, i, out) + _ev(i.evidence) for i in out.items] if out.items else ["(nothing ordered yet)"]
    )

    lines.append("")
    lines.append("HOW AND WHEN")
    f = out.fulfillment
    method = {
        FulfillmentMethod.pickup: "Pickup",
        FulfillmentMethod.delivery: "Delivery",
        FulfillmentMethod.unknown: "Pickup or delivery: not chosen",
    }[f.method]
    lines.append(method + _ev(f.method_evidence))
    rt = f.requested_time
    if rt.state is SlotState.provided:
        when = "as soon as possible" if rt.kind and rt.kind.value == "asap" else f"“{rt.raw_text}”"
        norm = f" = {rt.normalized_local}" if rt.normalized_local else ""
        lines.append(f"Time: {when}{norm}" + _ev(rt.evidence))
    elif rt.state is SlotState.ambiguous:
        lines.append(f"Time: UNCLEAR “{rt.raw_text}”" + _ev(rt.evidence))
    else:
        lines.append("Time: not mentioned (as soon as possible)")
    a = out.address
    if a.state is SlotState.provided:
        parts = [f"{k} {v}" for k, v in (("number", a.number), ("street", a.street), ("unit", a.unit),
                                          ("landmark", a.reference)) if v]  # fmt: skip
        lines.append(
            f"Address: “{a.raw_text}”" + (f" ({', '.join(parts)})" if parts else "") + _ev(a.evidence)
        )
    elif a.state is SlotState.ambiguous:
        lines.append("Address: UNCLEAR" + _ev(a.evidence))
    elif a.state is SlotState.not_mentioned:
        lines.append("Address: not given")

    lines.append("")
    lines.append("PAYMENT AND NAME")
    p = out.payment
    pay = {
        PaymentMethod.card: "card",
        PaymentMethod.cash: "cash",
        PaymentMethod.other: "other",
        PaymentMethod.unknown: "not chosen",
    }[p.method]
    if p.change_for_cents is not None:
        pay += f", paying with {format_cents(p.change_for_cents)}"
    if p.customer_claims_paid:
        pay += "; customer SAYS they already paid (a claim, not verified)"
    lines.append(f"Payment: {pay}" + _ev(p.evidence))
    n = out.customer_name
    lines.append(f"Name: {n.value}" + _ev(n.evidence) if n.state is SlotState.provided else "Name: not given")
    d = out.customer_decision
    decision = {
        DecisionState.pending: "not confirmed yet",
        DecisionState.confirmed: "CONFIRMED the order",
        DecisionState.cancelled: "CANCELLED the order",
    }[d.state]
    if d.agreed_while_incomplete:
        decision = "said yes, but something is still missing, so not confirmed"
    lines.append(f"Customer decision: {decision}" + _ev(d.evidence))
    for note in out.notes:
        lines.append(f"Note: {note.text}" + _ev(note.evidence))

    lines.append("")
    if out.missing_or_ambiguous:
        lines.append("STILL NEEDED BEFORE THE ORDER CAN BE CONFIRMED")
        for m in out.missing_or_ambiguous:
            where = f"{m.line_id}: " if m.line_id else ""
            lines.append(f"{where}{FIELD_NAMES[m.field.value]} ({REASONS[m.reason]})")
        lines.append(f"Question to the customer: “{out.clarification_question}”")
    else:
        lines.append("NOTHING MISSING")
    return lines
