"""The business's order ticket, built only from verified results (Quote) and the structured order.

A ticket exists only for a complete, priced order: nothing missing, no unresolved request (a Quote
can't be made with one). A customer's "I already paid" is printed as an unverified claim, so staff
check before handing over the food; only `payment_confirmed` (set by staff or a payment system,
never by chat) prints as paid.
"""

from orderslm.core.missing import required_missing
from orderslm.core.replies import _line_text, _when
from orderslm.domain.money import format_cents
from orderslm.schema.extraction import ExtractionOutput, FulfillmentMethod, PaymentMethod
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.order import Quote

TICKET_VERSION = "ticket@0.1"

TICKET: dict[str, dict[str, str]] = {
    "en": {
        "pickup": "Pickup {when}",
        "delivery": "Delivery to {address} {when}",
        "name": "Name: {name}",
        "note": "Note: {text}",
        "total": "Total: {total}{fee}",
        "fee": " (incl. {fee} delivery)",
        "paid_verified": "Payment: paid (verified)",
        "paid_claimed": "Payment: customer says paid, not verified",
        "card": "Payment: card",
        "cash": "Payment: cash",
        "cash_change": "Payment: cash (change for {change})",
        "other": "Payment: other",
    }
}


def ticket_lines(
    menu: MenuCatalog,
    quote: Quote,
    proposal: ExtractionOutput,
    *,
    payment_confirmed: bool = False,
    lang: str = "en",
) -> list[str]:
    if required_missing(proposal, menu) or proposal.missing_or_ambiguous:
        raise ValueError("ticket: the order still has missing or unresolved parts")
    T = TICKET[lang]
    lines = [_line_text(menu, proposal, ql.line_id, lang) for ql in quote.lines]
    method = proposal.fulfillment.method
    when = _when(proposal, lang)
    if method is FulfillmentMethod.pickup:
        lines.append(T["pickup"].format(when=when))
    elif method is FulfillmentMethod.delivery:
        lines.append(T["delivery"].format(address=proposal.address.raw_text, when=when))
    if proposal.customer_name.value:
        lines.append(T["name"].format(name=proposal.customer_name.value))
    lines += [T["note"].format(text=n.text) for n in proposal.notes]
    fee = T["fee"].format(fee=format_cents(quote.delivery_fee_cents)) if quote.delivery_fee_cents else ""
    lines.append(T["total"].format(total=format_cents(quote.total_cents), fee=fee))
    pay = proposal.payment
    if payment_confirmed:
        lines.append(T["paid_verified"])
    elif pay.customer_claims_paid:
        lines.append(T["paid_claimed"])
    elif pay.method is PaymentMethod.cash and pay.change_for_cents:
        lines.append(T["cash_change"].format(change=format_cents(pay.change_for_cents)))
    else:
        lines.append(T[pay.method.value] if pay.method.value in T else T["other"])
    return lines
