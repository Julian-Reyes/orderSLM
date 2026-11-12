"""Customer replies, filled only from verified results (Quote, Schedule, OrderRecord, tool results) and the menu.

Prices and totals come from the Quote; the day and time from the Schedule (core/schedule.py), always with the
day named ("today at 6:30 PM", "tomorrow, Thu, Nov 13, at 6:30 PM"), so a "yes" confirms a date and not just a
clock time; status from the OrderRecord. The only
model-written text that can reach a customer is the clarification question, and
it is used only if it states no amounts (otherwise the template question is used).
Strings are keyed by language so pt-BR can be added without touching the logic.
"""

import re
from datetime import date, time

from orderslm.core.missing import required_missing
from orderslm.core.requests import UNRESOLVED, RequestStatus, line_requests, request_status
from orderslm.core.schedule import DAY_PROBLEMS, WEEKDAYS
from orderslm.domain.money import format_cents
from orderslm.schema.extraction import (
    Amount,
    DayKind,
    ExtractionOutput,
    FieldRef,
    FulfillmentMethod,
    MissingInfo,
    MissingReason,
    Modification,
    ModificationKind,
    PaymentMethod,
    RequestedDay,
    SlotState,
)
from orderslm.schema.menu import MenuCatalog, SoldAs
from orderslm.schema.order import (
    HandoffTicket,
    OrderRecord,
    OrderStatus,
    Quote,
    Schedule,
    ToolErr,
    ToolResult,
)

SHOWN = {RequestStatus.catalog, RequestStatus.kitchen_note}

REPLIES_VERSION = "replies@0.8"  # 0.8: the day in every time; schedule problems

TEMPLATES: dict[str, dict[str, str]] = {
    "en": {
        "summary": "Got it: {items}. {fulfillment}. Total {total}{fee}{payment}. Is that right?",
        "pickup": "Pickup {when}",
        "delivery": "Delivery to {address} {when}",
        "fulfillment_unknown": "Pickup or delivery not chosen yet",
        "asap": "as soon as possible",
        "today_at": "today at {time}",
        "tomorrow_at": "tomorrow, {date}, at {time}",
        "day_at": "on {date} at {time}",
        "today": "today",
        "tomorrow": "tomorrow",
        "on_day": "on {date}",
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
        "q_combo": "which {slot} would you like with the {name} ({options})",
        "q_combo_more": "which {slot} ({options})",
        "q_combo_variant": "which {choice} would you like in the {name} ({options})",
        "q_method": "is this for pickup or delivery",
        "q_method_to_address": "Would you like it delivered to {address}, or will you pick it up?",
        "q_method_pickup_only": "is this for pickup",
        "q_size": "what size would you like for the {name} ({options})",
        "q_time": "what time would you like it",
        "q_time_day": "what time {day} would you like it",
        "on_weekday": "on {weekday}",
        "on_the": "on the {nth}",
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
        "schedule_not_accepted": "Sorry, we can only take orders for today. Would you like it today instead?",
        "schedule_too_far": "Sorry, we take orders up to {days} days ahead, and {date} is further out. Could you pick an earlier day?",
        "schedule_closed": "Sorry, we're closed {day}. Would another day work?",
        "schedule_hours": "We're open {opens} to {closes} {day}. What time in that window works for you?",
        "schedule_past": "{time} has already passed today. What time would you like it instead?",
        "schedule_no_date": "Sorry, I couldn't find that date ({text}). Which day would you like it for?",
    }
}

DATE_WORDS: dict[str, dict[str, list[str]]] = {
    "en": {
        "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "weekdays_short": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "months_short": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    }
}

MONEY_IN_TEXT = re.compile(r"[$€£]\s?\d|\b\d+[.,]\d{2}\b|\bR\$")


def _t(lang: str) -> dict[str, str]:
    if lang not in TEMPLATES:
        raise KeyError(f"no reply templates for language {lang!r}")
    return TEMPLATES[lang]


def _plural_en(name: str) -> str:
    """'veggie burger' -> 'veggie burgers', 'breakfast sandwich' -> 'breakfast sandwiches'; names already ending
    in s ('nachos', 'jarritos') stay as they are."""
    if name.endswith("s"):
        return name
    if name.endswith(("ch", "sh", "x", "z")):
        return name + "es"
    if len(name) > 1 and name.endswith("y") and name[-2] not in "aeiou":
        return name[:-1] + "ies"
    return name + "s"


PLURALS = {"en": _plural_en}


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


def _format_time(hhmm: str | time) -> str:
    t = time.fromisoformat(hhmm) if isinstance(hhmm, str) else hhmm
    return f"{(t.hour % 12) or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}"


def _format_date(d: date, lang: str) -> str:
    """'Thu, Nov 13': weekday and date, so the customer can check both."""
    W = DATE_WORDS[lang]
    return f"{W['weekdays_short'][d.weekday()]}, {W['months_short'][d.month - 1]} {d.day}"


def _ordinal_en(n: int) -> str:
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _named_day(day: RequestedDay, lang: str) -> str:
    """The day the customer named, in the reply language, without working out the date ('tomorrow', 'on
    Saturday', 'on Nov 20', 'on the 15th'). Used by the question, which finalize builds without the chat."""
    T = _t(lang)
    if day.kind is DayKind.tomorrow:
        return T["tomorrow"]
    if day.kind is DayKind.weekday:
        return T["on_weekday"].format(weekday=DATE_WORDS[lang]["weekdays"][WEEKDAYS.index(day.weekday)])
    if day.month is not None:
        return T["on_day"].format(
            date=f"{DATE_WORDS[lang]['months_short'][day.month - 1]} {day.day_of_month}"
        )
    return T["on_the"].format(nth=_ordinal_en(day.day_of_month))


def _day_words(d: date, days_ahead: int, lang: str) -> str:
    """'today', 'tomorrow, Thu, Nov 13', 'on Sat, Nov 15'."""
    T = _t(lang)
    if days_ahead == 0:
        return T["today"]
    if days_ahead == 1:
        return f"{T['tomorrow']}, {_format_date(d, lang)}"
    return T["on_day"].format(date=_format_date(d, lang))


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
    if line.quantity and line.quantity > 1:
        title = PLURALS[lang](title)
    return f"{line.quantity} {title}" + (f" ({', '.join(details)})" if details else "")


def _when(schedule: Schedule, lang: str) -> str:
    """The day and time, from the verified Schedule only."""
    T = _t(lang)
    if schedule.local_time is not None:
        at = _format_time(schedule.local_time)
        if schedule.days_ahead == 0:
            return T["today_at"].format(time=at)
        key = "tomorrow_at" if schedule.days_ahead == 1 else "day_at"
        return T[key].format(date=_format_date(schedule.local_date, lang), time=at)
    if schedule.time_text:
        return schedule.time_text
    return T["asap"]


def summary(
    menu: MenuCatalog, quote: Quote, proposal: ExtractionOutput, schedule: Schedule, lang: str = "en"
) -> str:
    """The confirmation question. Every amount comes from the Quote. Never sent while anything is missing:
    use next_reply(), which asks the missing question first."""
    if required_missing(proposal, menu) or proposal.missing_or_ambiguous:
        raise ValueError("summary: something is still missing; ask for it first (next_reply)")
    T = _t(lang)
    items = ", ".join(_line_text(menu, proposal, ql.line_id, lang) for ql in quote.lines)
    method = proposal.fulfillment.method
    if method is FulfillmentMethod.pickup:
        fulfillment = T["pickup"].format(when=_when(schedule, lang))
    elif method is FulfillmentMethod.delivery:
        fulfillment = T["delivery"].format(address=proposal.address.raw_text, when=_when(schedule, lang))
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
            name = item.name.lower() if key != "q_quantity" else PLURALS[lang](item.name.lower())
            questions.append(T[key].format(name=name, pieces=item.pieces_per_order))
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
            picked = {s.slot_id: s for s in line.combo_selections} if line else {}
            first = True  # name the combo once; later missing slots just add "and which drink (...)"
            for slot in item.combo_slots:
                sel = picked.get(slot.id)
                if sel is None:
                    names = [c.name for cid in slot.choices if (c := menu.item(cid))]
                    key = "q_combo" if first else "q_combo_more"
                    first = False
                    questions.append(
                        T[key].format(
                            slot=slot.name.lower(),
                            name=item.name.lower(),
                            options=_join(names, lang, "or", comma=False),
                        )
                    )
                elif (
                    (choice := menu.item(sel.menu_item_id))
                    and choice.variants
                    and not (sel.variant_id or choice.default_variant_id)
                ):  # picked, but the choice needs a size/flavor ("a latte" in the coffee & pastry)
                    questions.append(
                        T["q_combo_variant"].format(
                            choice=choice.name.lower(),
                            name=item.name.lower(),
                            options=_join([v.name.lower() for v in choice.variants], lang, "or", comma=False),
                        )
                    )
        elif m.field is FieldRef.fulfillment_method:
            if not menu.delivery.available:
                questions.append(T["q_method_pickup_only"])
            elif proposal.address.state is SlotState.provided and proposal.address.raw_text:
                # an address given without choosing delivery ("do u deliver to …?"): ask about that address
                statements.append(T["q_method_to_address"].format(address=proposal.address.raw_text))
            else:
                questions.append(T["q_method"])
        elif m.field is FieldRef.requested_time:
            day = proposal.fulfillment.requested_time.day
            questions.append(T["q_time_day"].format(day=_named_day(day, lang)) if day else T["q_time"])
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
        if statements:  # the off-menu / address sentence already asks; continue with "Also, ..."
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
    menu: MenuCatalog,
    proposal: ExtractionOutput,
    quote: ToolResult[Quote],
    schedule: ToolResult[Schedule],
    lang: str = "en",
) -> tuple[str, str]:
    """(text, kind): a problem with the day first (no time on it can work), then the missing-info question; a
    summary only for a complete, priced, scheduled order."""
    if isinstance(schedule, ToolErr) and schedule.error.code in DAY_PROBLEMS:
        return schedule_problem(schedule, lang), "schedule_problem"
    missing = required_missing(proposal, menu)
    if missing:
        return clarification(proposal, menu, missing, lang)[0], "question"
    if isinstance(quote, ToolErr):
        return pricing_problem(quote, menu, lang), "pricing_problem"
    if isinstance(schedule, ToolErr):
        return schedule_problem(schedule, lang), "schedule_problem"
    return summary(menu, quote.data, proposal, schedule.data, lang), "summary"


def schedule_problem(err: ToolErr, lang: str = "en") -> str:
    """Why that day or time can't work, from the schedule check's details (core/schedule.py)."""
    T = _t(lang)
    code, details = err.error.code, err.error.details or {}
    on_date = details.get("date")
    day = (
        _day_words(date.fromisoformat(str(on_date)), int(details.get("days_ahead", 1)), lang)
        if on_date
        else ""
    )
    if code == "SCHEDULE_NOT_ACCEPTED":
        return T["schedule_not_accepted"]
    if code == "SCHEDULE_TOO_FAR_AHEAD":
        return T["schedule_too_far"].format(
            days=details["max_days_ahead"], date=_format_date(date.fromisoformat(str(on_date)), lang)
        )
    if code == "SCHEDULE_CLOSED_DAY":
        return T["schedule_closed"].format(day=day)
    if code == "SCHEDULE_OUTSIDE_HOURS":
        return T["schedule_hours"].format(
            opens=_format_time(str(details["opens_at"])),
            closes=_format_time(str(details["closes_at"])),
            day=day,
        )
    if code == "SCHEDULE_IN_PAST":
        return T["schedule_past"].format(time=_format_time(str(details["time"])))
    return T["schedule_no_date"].format(text=details.get("raw_text", ""))


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
