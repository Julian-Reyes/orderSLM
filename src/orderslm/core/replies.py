"""Customer replies, filled only from verified results (Quote, OrderRecord, tool results) and the menu.

Prices and totals come from the Quote; status from the OrderRecord. The only
model-written text that can reach a customer is the clarification question, and
it is used only if it states no amounts (otherwise the template question is used).
Strings are keyed by language so pt-BR can be added without touching the logic.
"""

import re
from datetime import time

from orderslm.core.missing import required_missing
from orderslm.core.requests import UNRESOLVED, RequestStatus, line_requests, request_status
from orderslm.domain.money import format_cents
from orderslm.schema.extraction import (
    Amount,
    ExtractionOutput,
    FieldRef,
    FulfillmentMethod,
    MissingInfo,
    MissingReason,
    Modification,
    ModificationKind,
    PaymentMethod,
    SlotState,
    TimeKind,
)
from orderslm.schema.menu import MenuCatalog, SoldAs
from orderslm.schema.order import HandoffTicket, OrderRecord, OrderStatus, Quote, ToolErr, ToolResult

SHOWN = {RequestStatus.catalog, RequestStatus.kitchen_note}

REPLIES_VERSION = "replies@0.3"

TEMPLATES: dict[str, dict[str, str]] = {
    "en": {
        "summary": "Got it: {items}. {fulfillment}. Total {total}{fee}{payment}. Is that right?",
        "pickup": "Pickup {when}",
        "delivery": "Delivery to {address} {when}",
        "fulfillment_unknown": "Pickup or delivery not chosen yet",
        "asap": "as soon as possible",
        "at": "at {time}",
        "fee": " (incl. {fee} delivery)",
        "pay_cash": ", paying cash",
        "pay_cash_change": ", paying cash (change for {change})",
        "pay_card": ", paying by card",
        "pay_other": "",
        "pay_claimed": ". You mentioned you've already paid, and the restaurant will confirm it",
        "remove": "no {name}",
        "add": "add {name}",
        "add_included": "{name}",
        "extra": "extra {name}",
        "light": "light {name}",
        "substitute": "{new} instead of {old}",
        "half": "half {name}",
        "q_items": "what would you like to order",
        "q_off_menu": "We don't have {text}. Would you like something else instead?",
        "q_ambiguous_item": "which one do you mean by “{text}”",
        "q_quantity": "how many {name} would you like",
        "q_quantity_orders": "how many orders of {name} would you like",
        "q_quantity_pieces": "how many orders of {name} would you like ({pieces} per order)",
        "q_variant": "which {name} would you like ({options})",
        "q_variant_not_on_menu": "We don't have a {text} for the {name}; we have {options}. Which would you like?",
        "q_option_not_on_menu": "We don't have {text} for the {name}. Would you like it as it comes, or with something else instead?",
        "q_option_unverified": "Just checking, we may not be able to do {text} on the {name}. Want it without, or keep it as a note for the kitchen?",
        "q_combo": "what would you like with the {name} ({options})",
        "q_method": "is this for pickup or delivery",
        "q_method_pickup_only": "is this for pickup",
        "q_size": "what size would you like for the {name} ({options})",
        "q_time": "what time would you like it",
        "q_address": "what's the delivery address",
        "q_payment": "will you pay by card or cash",
        "q_name": "can I get a name for the order",
        "and": "and",
        "or": "or",
        "placed": "Your order is in!{eta}",
        "eta": " It'll be ready in about {minutes} minutes.",
        "status_new": "We've got your order and will start it shortly.",
        "status_preparing": "Your order is being prepared.{eta}",
        "status_ready": "Your order is ready!",
        "status_completed": "Our records show your order was completed. If something's wrong, tell me and I'll get a staff member.",
        "status_cancelled": "That order was cancelled.",
        "status_unknown": "I couldn't find a placed order for this chat.",
        "handoff": "I've passed this to our staff. Someone will reply here shortly.",
        "payment_claim": "Thanks! A staff member will check the payment and confirm it. Until then it shows as pending.",
        "cancelled": "No problem, I've cancelled the order.",
        "needs_staff": "Your order is already with the kitchen, so I've asked a staff member to help with that change.",
        "cash_below_total": "You mentioned paying with {cash}, but the total is {total}. Could you bring a larger bill, or pay by card?",
        "below_minimum": "Delivery needs a minimum order of {minimum}; your order is {subtotal} so far. Want to add something or switch to pickup?",
        "no_delivery": "Sorry, {business} is pickup only. Would pickup work for you?",
        "unavailable": "Sorry, {detail}. Would you like something else?",
        "cannot_price": "Sorry, I couldn't put that order together yet. Could you tell me again what you'd like?",
    }
}

MONEY_IN_TEXT = re.compile(r"[$€£]\s?\d|\b\d+[.,]\d{2}\b|\bR\$")


def _t(lang: str) -> dict[str, str]:
    if lang not in TEMPLATES:
        raise KeyError(f"no reply templates for language {lang!r}")
    return TEMPLATES[lang]


def _join(parts: list[str], lang: str, word: str = "and", comma: bool = True) -> str:
    """'a, b, and c' for clauses; 'a, b or c' for options (comma=False)."""
    if len(parts) <= 1:
        return "".join(parts)
    sep = ", " if comma else " "
    return ", ".join(parts[:-1]) + sep + _t(lang)[word] + " " + parts[-1]


_REQUEST_WORDS = re.compile(r"^(?:with|w/?|add|extra|plus|and|\+|some|a|an)\s+", re.IGNORECASE)


def _option_text(raw: str) -> str:
    """'with artichoke hearts' -> 'artichoke hearts' (the customer's words, minus request words)."""
    text = raw.strip()
    while (m := _REQUEST_WORDS.match(text)) and m.end() < len(text):
        text = text[m.end() :]
    return text.lower()


def _format_time(hhmm: str) -> str:
    t = time.fromisoformat(hhmm)
    return f"{(t.hour % 12) or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}"


def _mod_text(menu: MenuCatalog, ingredient_ids: list[str], mod: Modification, lang: str) -> str:
    T = _t(lang)

    def name(mid: str | None) -> str:
        m = menu.modifier(mid) if mid else None
        return m.name.lower() if m else mod.raw_text

    if mod.modifier_id is None and mod.kind is not ModificationKind.substitute:
        return mod.raw_text  # a kitchen request ("warm"); not_on_menu options never get here (no Quote)
    if mod.kind is ModificationKind.remove:
        return T["remove"].format(name=name(mod.modifier_id))
    if mod.kind is ModificationKind.substitute:
        return T["substitute"].format(new=name(mod.replacement_modifier_id), old=name(mod.modifier_id))
    if mod.amount is Amount.extra:
        return T["extra"].format(name=name(mod.modifier_id))
    if mod.amount is Amount.light:
        return T["light"].format(name=name(mod.modifier_id))
    key = "add_included" if mod.modifier_id in ingredient_ids else "add"
    return T[key].format(name=name(mod.modifier_id))


def _line_text(menu: MenuCatalog, proposal: ExtractionOutput, line_id: str, lang: str) -> str:
    T = _t(lang)
    line = next(i for i in proposal.items if i.line_id == line_id)
    details: list[str] = []
    if line.halves:
        items = [menu.item(h.menu_item_id) for h in line.halves]
        title = "Pizza"
        variant = items[0].variant(line.variant_id) if items[0] and line.variant_id else None
        if variant:
            details.append(variant.name)
        for it, half in zip(items, line.halves, strict=True):
            shown = [m for m in half.modifications if request_status(menu, it, m) in SHOWN]
            mods = [_mod_text(menu, it.ingredient_ids, m, lang) for m in shown] if it else []
            details.append(
                T["half"].format(name=it.name.removesuffix(" Pizza") if it else half.menu_item_id)
                + "".join(f" {m}" for m in mods)
            )
    else:
        item = menu.item(line.menu_item_id or "")
        title = item.name if item else (line.unmatched_text or "")
        if item and line.variant_id and (v := item.variant(line.variant_id)):
            details.append(v.name)
        details += [
            _mod_text(menu, item.ingredient_ids if item else [], m, lang)
            for m in line.modifications
            if request_status(menu, item, m) in SHOWN  # unresolved requests are never shown
        ]
        for sel in line.combo_selections:
            choice = menu.item(sel.menu_item_id)
            details.append(choice.name if choice else sel.menu_item_id)
    return f"{line.quantity} {title}" + (f" ({', '.join(details)})" if details else "")


def _when(proposal: ExtractionOutput, lang: str) -> str:
    T = _t(lang)
    rt = proposal.fulfillment.requested_time
    if rt.state is SlotState.provided and rt.normalized_local:
        return T["at"].format(time=_format_time(rt.normalized_local))
    if rt.state is SlotState.provided and rt.kind is not TimeKind.asap and rt.raw_text:
        return rt.raw_text
    return T["asap"]


def summary(menu: MenuCatalog, quote: Quote, proposal: ExtractionOutput, lang: str = "en") -> str:
    """The confirmation question. Every amount comes from the Quote. Never sent while anything is missing:
    use next_reply(), which asks the missing question first."""
    if required_missing(proposal, menu) or proposal.missing_or_ambiguous:
        raise ValueError("summary: something is still missing; ask for it first (next_reply)")
    T = _t(lang)
    items = ", ".join(_line_text(menu, proposal, ql.line_id, lang) for ql in quote.lines)
    method = proposal.fulfillment.method
    if method is FulfillmentMethod.pickup:
        fulfillment = T["pickup"].format(when=_when(proposal, lang))
    elif method is FulfillmentMethod.delivery:
        fulfillment = T["delivery"].format(address=proposal.address.raw_text, when=_when(proposal, lang))
    else:
        fulfillment = T["fulfillment_unknown"]
    pay = proposal.payment
    if pay.method is PaymentMethod.cash and pay.change_for_cents:
        payment = T["pay_cash_change"].format(change=format_cents(pay.change_for_cents))
    else:
        payment = T[{"cash": "pay_cash", "card": "pay_card"}.get(pay.method.value, "pay_other")]
    if pay.customer_claims_paid:  # a claim, never stated as a confirmed payment
        payment += T["pay_claimed"]
    fee = T["fee"].format(fee=format_cents(quote.delivery_fee_cents)) if quote.delivery_fee_cents else ""
    text = T["summary"].format(
        items=items, fulfillment=fulfillment, total=format_cents(quote.total_cents), fee=fee, payment=payment
    )
    return text[0].upper() + text[1:]


def template_question(
    missing: list[MissingInfo], proposal: ExtractionOutput, menu: MenuCatalog, lang: str = "en"
) -> str:
    """One question covering everything missing, built only from the menu and the structured order."""
    T = _t(lang)
    lines = {i.line_id: i for i in proposal.items}
    statements: list[str] = []
    questions: list[str] = []
    for m in missing:
        line = lines.get(m.line_id) if m.line_id else None
        item = menu.item(line.menu_item_id or "") if line and line.menu_item_id else None
        if line and line.halves:
            item = menu.item(line.halves[0].menu_item_id)
            if item is not None:  # ask about "the pizza", not about one of its halves
                item = item.model_copy(update={"name": "pizza"})
        if m.field is FieldRef.items:
            questions.append(T["q_items"])
        elif m.field is FieldRef.item_menu_match and line:
            if m.reason is MissingReason.off_menu:
                statements.append(T["q_off_menu"].format(text=line.unmatched_text))
            else:
                questions.append(T["q_ambiguous_item"].format(text=line.unmatched_text))
        elif m.field is FieldRef.item_quantity and item:
            key = "q_quantity" if item.sold_as is SoldAs.each else "q_quantity_orders"
            if item.pieces_per_order:
                key = "q_quantity_pieces"
            questions.append(T[key].format(name=item.name.lower(), pieces=item.pieces_per_order))
        elif m.field is FieldRef.item_variant and item:
            options = _join([v.name.lower() for v in item.variants], lang, "or", comma=False)
            if line and line.unmatched_variant_text:
                statements.append(
                    T["q_variant_not_on_menu"].format(
                        text=line.unmatched_variant_text.lower(), name=item.name.lower(), options=options
                    )
                )
            elif line and line.halves:  # half-and-half: the pizza is known, only the size is missing
                questions.append(T["q_size"].format(name=item.name.lower(), options=options))
            else:
                questions.append(T["q_variant"].format(name=item.name.lower(), options=options))
        elif m.field is FieldRef.item_modification and item and line:
            for _, mod, status in line_requests(menu, line):
                if status in UNRESOLVED:
                    key = (
                        "q_option_not_on_menu"
                        if status is RequestStatus.not_on_menu
                        else "q_option_unverified"
                    )
                    statements.append(T[key].format(text=_option_text(mod.raw_text), name=item.name.lower()))
        elif m.field is FieldRef.combo_choice and item:
            picked = {s.slot_id for s in line.combo_selections} if line else set()
            for slot in item.combo_slots:
                if slot.id not in picked:
                    names = [c.name for cid in slot.choices if (c := menu.item(cid))]
                    questions.append(
                        T["q_combo"].format(
                            name=item.name.lower(), options=_join(names, lang, "or", comma=False)
                        )
                    )
        elif m.field is FieldRef.fulfillment_method:
            questions.append(T["q_method"] if menu.delivery.available else T["q_method_pickup_only"])
        elif m.field is FieldRef.requested_time:
            questions.append(T["q_time"])
        elif m.field is FieldRef.address:
            questions.append(T["q_address"])
        elif m.field is FieldRef.payment_method:
            questions.append(T["q_payment"])
        elif m.field is FieldRef.customer_name:
            questions.append(T["q_name"])
    text = " ".join(statements)
    if questions:
        q = _join(questions, lang)
        q = q[0].upper() + q[1:] + "?"
        if statements:  # the off-menu sentence already asks; continue with "Also, ..."
            q = "Also, " + q[0].lower() + q[1:]
        text = f"{text} {q}".strip()
    return text


def clarification(
    proposal: ExtractionOutput, menu: MenuCatalog, missing: list[MissingInfo], lang: str = "en"
) -> tuple[str, str]:
    """(text, source). Uses the model's question unless it mentions amounts; then the template."""
    q = proposal.clarification_question
    if q and not MONEY_IN_TEXT.search(q):
        return q, "model"
    return template_question(missing, proposal, menu, lang), "template"


def next_reply(
    menu: MenuCatalog, proposal: ExtractionOutput, quote: ToolResult[Quote], lang: str = "en"
) -> tuple[str, str]:
    """(text, kind): the missing-info question first; a summary only for a complete, priced order."""
    missing = required_missing(proposal, menu)
    if missing:
        return clarification(proposal, menu, missing, lang)[0], "question"
    if isinstance(quote, ToolErr):
        return pricing_problem(quote, menu, lang), "pricing_problem"
    return summary(menu, quote.data, proposal, lang), "summary"


def pricing_problem(err: ToolErr, menu: MenuCatalog, lang: str = "en") -> str:
    T = _t(lang)
    code, details = err.error.code, err.error.details or {}
    if code == "CASH_BELOW_TOTAL":
        return T["cash_below_total"].format(
            cash=format_cents(int(details["change_for_cents"])),
            total=format_cents(int(details["total_cents"])),
        )
    if code == "BELOW_DELIVERY_MINIMUM":
        return T["below_minimum"].format(
            minimum=format_cents(int(details["min_order_cents"])),
            subtotal=format_cents(int(details["subtotal_cents"])),
        )
    if code == "DELIVERY_UNAVAILABLE":
        return T["no_delivery"].format(business=menu.name)
    if code == "UNAVAILABLE":
        return T["unavailable"].format(detail=err.error.message)
    return T["cannot_price"]


def order_placed(order: OrderRecord, lang: str = "en") -> str:
    T = _t(lang)
    eta = T["eta"].format(minutes=order.eta_minutes) if order.eta_minutes else ""
    return T["placed"].format(eta=eta)


def order_status(order: OrderRecord | None, lang: str = "en") -> str:
    T = _t(lang)
    if order is None:
        return T["status_unknown"]
    eta = T["eta"].format(minutes=order.eta_minutes) if order.eta_minutes else ""
    key = {
        OrderStatus.new: "status_new",
        OrderStatus.preparing: "status_preparing",
        OrderStatus.ready: "status_ready",
        OrderStatus.completed: "status_completed",
        OrderStatus.cancelled: "status_cancelled",
    }.get(order.status, "status_unknown")
    return T[key].format(eta=eta)


def handoff(ticket: HandoffTicket, lang: str = "en") -> str:
    return _t(lang)["handoff"]


def payment_claim(lang: str = "en") -> str:
    return _t(lang)["payment_claim"]


def cancelled(lang: str = "en") -> str:
    return _t(lang)["cancelled"]


def needs_staff(lang: str = "en") -> str:
    return _t(lang)["needs_staff"]
