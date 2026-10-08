"""Deterministic pricing: menu + extraction proposal -> verified Quote. Rules: docs/PRICING.md.

Never guesses. Anything that can't be priced exactly (off-menu item, unclear
quantity, missing size or combo choice, unknown id) returns a ToolErr listing
every problem, so the reply layer asks instead of quoting a wrong total.
"""

from dataclasses import dataclass

from orderslm.checks import check_catalog
from orderslm.core.requests import RequestStatus, line_requests
from orderslm.menus import menu_version
from orderslm.schema.extraction import (
    Amount,
    ExtractionOutput,
    FulfillmentMethod,
    ItemProposal,
    Modification,
    ModificationKind,
    PaymentMethod,
)
from orderslm.schema.menu import MenuCatalog, MenuItem
from orderslm.schema.order import Quote, QuoteLine, ToolErr, ToolError, ToolOk, ToolResult

PRICING_VERSION = "pricing@0.1"


@dataclass(frozen=True)
class PricingIssue:
    code: str
    line_id: str | None
    message: str


def modifier_price(menu: MenuCatalog, item: MenuItem, mod: Modification) -> int:
    """Price of one modification on one item (whole item; halves are halved by the caller)."""
    if mod.kind is ModificationKind.remove:
        return 0
    added = mod.replacement_modifier_id if mod.kind is ModificationKind.substitute else mod.modifier_id
    if added is None:
        return 0  # off-menu request ("extra crispy"): a kitchen note, not priced
    m = menu.modifier(added)
    assert m is not None, "check_catalog runs first"
    if added in item.ingredient_ids:
        # Already included: only "extra" costs (one more portion). Light or plain "add" is free.
        return m.price_cents if mod.amount is Amount.extra else 0
    return m.price_cents * (2 if mod.amount is Amount.extra else 1)


def _variant_issue(
    item: MenuItem, variant_id: str | None, line_id: str, unmatched: str | None = None
) -> PricingIssue | None:
    if unmatched is not None:  # never fall back to the default size for a size the item doesn't have
        return PricingIssue("MISSING_VARIANT", line_id, f"{item.name} has no {unmatched!r}; choose a size")
    if variant_id is None and item.variants and item.default_variant_id is None:
        names = ", ".join(v.name for v in item.variants)
        return PricingIssue("MISSING_VARIANT", line_id, f"{item.name} needs a choice: {names}")
    return None


def _variant_delta(item: MenuItem, variant_id: str | None) -> int:
    vid = variant_id or item.default_variant_id
    v = item.variant(vid) if vid else None
    return v.price_delta_cents if v else 0


def _display(item: MenuItem, variant_id: str | None) -> str:
    vid = variant_id or item.default_variant_id
    v = item.variant(vid) if vid else None
    return f"{item.name}, {v.name}" if v and len(item.variants) > 1 else item.name


def _price_line(menu: MenuCatalog, line: ItemProposal, issues: list[PricingIssue]) -> QuoteLine | None:
    lid = line.line_id
    if line.unmatched_text is not None:
        issues.append(PricingIssue("UNMATCHED_ITEM", lid, f"{line.unmatched_text!r} is not on the menu"))
        return None
    if line.quantity is None:
        issues.append(PricingIssue("UNCLEAR_QUANTITY", lid, "quantity not clear"))
        return None
    requests = line_requests(menu, line)
    if off := [m.raw_text for _, m, s in requests if s is RequestStatus.not_on_menu]:
        # Never priced: the customer has to drop it or pick something else first.
        issues.append(PricingIssue("OPTION_NOT_ON_MENU", lid, f"not on the menu: {', '.join(off)}"))
        return None
    if unsure := [m.raw_text for _, m, s in requests if s is RequestStatus.unverified]:
        # Not on the menu's accepted kitchen requests and not flagged: ask before it reaches the ticket.
        issues.append(
            PricingIssue("REQUEST_UNVERIFIED", lid, f"check with the customer: {', '.join(unsure)}")
        )
        return None

    if line.halves is not None:
        halves = [menu.item(h.menu_item_id) for h in line.halves]
        if any(h is None for h in halves):
            return None  # reported by check_catalog
        if (
            issue := _variant_issue(halves[0], line.variant_id, lid, line.unmatched_variant_text)
        ) is not None:
            issues.append(issue)
            return None
        # The pizza costs as much as its more expensive half; each half's add-ons cost half, rounded up.
        base = max(h.base_price_cents + _variant_delta(h, line.variant_id) for h in halves)
        addons = sum(
            -(-modifier_price(menu, h, m) // 2)
            for h, half in zip(halves, line.halves, strict=True)
            for m in half.modifications
        )
        names = " / ".join(f"half {h.name}" for h in halves)
        v = halves[0].variant(line.variant_id) if line.variant_id else None
        priced = max(halves, key=lambda h: h.base_price_cents + _variant_delta(h, line.variant_id))
        unit = base + addons
        return QuoteLine(
            line_id=lid,
            menu_item_id=priced.id,
            half_menu_item_ids=[h.id for h in halves],
            display_name=f"Pizza, {v.name}: {names}" if v else f"Pizza: {names}",
            quantity=line.quantity,
            variant_id=line.variant_id,
            modifications=[m for half in line.halves for m in half.modifications],
            unit_price_cents=unit,
            line_total_cents=unit * line.quantity,
        )

    item = menu.item(line.menu_item_id or "")
    if item is None:
        return None  # reported by check_catalog
    if not item.available:
        issues.append(PricingIssue("UNAVAILABLE", lid, f"{item.name} is not available right now"))
        return None
    if (issue := _variant_issue(item, line.variant_id, lid, line.unmatched_variant_text)) is not None:
        issues.append(issue)
        return None
    unit = item.base_price_cents + _variant_delta(item, line.variant_id)
    unit += sum(modifier_price(menu, item, m) for m in line.modifications)

    picked = {s.slot_id: s for s in line.combo_selections}
    for slot in item.combo_slots:
        sel = picked.get(slot.id)
        if sel is None:
            issues.append(
                PricingIssue("MISSING_COMBO_CHOICE", lid, f"{item.name}: choose a {slot.name.lower()}")
            )
            continue
        choice = menu.item(sel.menu_item_id)
        if choice is None:
            continue  # reported by check_catalog
        if (issue := _variant_issue(choice, sel.variant_id, lid)) is not None:
            issues.append(issue)
            continue
        unit += _variant_delta(choice, sel.variant_id)  # included, but upsizing costs the size difference
    if any(i.line_id == lid for i in issues):
        return None
    return QuoteLine(
        line_id=lid,
        menu_item_id=item.id,
        display_name=_display(item, line.variant_id),
        quantity=line.quantity,
        variant_id=line.variant_id or item.default_variant_id,
        modifications=line.modifications,
        unit_price_cents=unit,
        line_total_cents=unit * line.quantity,
    )


def _err(issues: list[PricingIssue], **extra: object) -> ToolErr:
    first = issues[0]
    return ToolErr(
        error=ToolError(
            code=first.code,
            message=first.message,
            details={"issues": [i.__dict__ for i in issues], **extra},
        ),
        verified_by=PRICING_VERSION,
    )


class DeterministicPricing:
    """Implements interfaces.tools.PricingEngine."""

    def quote(self, menu: MenuCatalog, proposal: ExtractionOutput) -> ToolResult[Quote]:
        issues = [
            PricingIssue(i.code, i.path.removeprefix("items[").removesuffix("]"), i.message)
            for i in check_catalog(proposal, menu)
        ]
        if not proposal.items:
            issues.append(PricingIssue("NO_ITEMS", None, "the order has no items yet"))
        # Lines check_catalog rejected (e.g. an unknown modifier id) are not priced: an invented id must
        # come back as a ToolErr, never reach modifier_price.
        rejected = {i.line_id for i in issues}
        lines = [
            ql
            for line in proposal.items
            if line.line_id not in rejected and (ql := _price_line(menu, line, issues)) is not None
        ]
        if issues:
            return _err(issues)

        method = proposal.fulfillment.method
        subtotal = sum(line.line_total_cents for line in lines)
        fee = 0
        if method is FulfillmentMethod.delivery:
            if not menu.delivery.available:
                return _err([PricingIssue("DELIVERY_UNAVAILABLE", None, f"{menu.name} only does pickup")])
            if subtotal < menu.delivery.min_order_cents:
                return _err(
                    [PricingIssue("BELOW_DELIVERY_MINIMUM", None, "order is below the delivery minimum")],
                    subtotal_cents=subtotal,
                    min_order_cents=menu.delivery.min_order_cents,
                )
            fee = menu.delivery.fee_cents
        pay = proposal.payment
        if pay.method is PaymentMethod.cash and pay.change_for_cents is not None:
            if pay.change_for_cents < subtotal + fee:  # "change for a 100" on a $170 order
                return _err(
                    [
                        PricingIssue(
                            "CASH_BELOW_TOTAL",
                            None,
                            "the cash the customer will pay with is less than the total",
                        )
                    ],
                    change_for_cents=pay.change_for_cents,
                    total_cents=subtotal + fee,
                )
        quote = Quote(
            business_id=menu.business_id,
            currency=menu.currency,
            lines=lines,
            fulfillment=method,
            subtotal_cents=subtotal,
            delivery_fee_cents=fee,
            total_cents=subtotal + fee,
            verified_by=PRICING_VERSION,
            menu_version=menu_version(menu),
        )
        return ToolOk[Quote](data=quote, verified_by=PRICING_VERSION)
