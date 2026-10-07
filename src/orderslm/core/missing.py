"""What must be clarified before an order can be confirmed (docs/ANNOTATION_GUIDE.md, "What counts as missing").

Derived from the structured order and the menu only. Judgment calls that need
the text (e.g. whether "a burger" is ambiguous rather than off-menu) are the
extractor's job; here an unmatched item is always reported as off_menu.
"""

from orderslm.schema.extraction import (
    DecisionState,
    ExtractionOutput,
    FieldRef,
    FulfillmentMethod,
    MissingInfo,
    MissingReason,
    PaymentMethod,
    SlotState,
)
from orderslm.schema.menu import MenuCatalog, MenuItem


def _needs_variant(item: MenuItem | None, variant_id: str | None) -> bool:
    return item is not None and bool(item.variants) and item.default_variant_id is None and variant_id is None


def required_missing(output: ExtractionOutput, menu: MenuCatalog) -> list[MissingInfo]:
    if output.customer_decision.state is DecisionState.cancelled:
        return []
    out: list[MissingInfo] = []

    def add(field: FieldRef, reason: MissingReason, line_id: str | None = None) -> None:
        out.append(MissingInfo(field=field, reason=reason, line_id=line_id))

    if not output.items:
        add(FieldRef.items, MissingReason.missing)
    for line in output.items:
        lid = line.line_id
        if line.unmatched_text is not None:
            add(FieldRef.item_menu_match, MissingReason.off_menu, lid)
            continue
        if line.quantity is None:
            add(FieldRef.item_quantity, MissingReason.ambiguous, lid)
        base_id = line.halves[0].menu_item_id if line.halves else line.menu_item_id
        if _needs_variant(menu.item(base_id or ""), line.variant_id):
            add(FieldRef.item_variant, MissingReason.missing, lid)
        item = menu.item(line.menu_item_id or "")
        if item is not None and item.combo_slots:
            picked = {s.slot_id: s for s in line.combo_selections}
            for slot in item.combo_slots:
                sel = picked.get(slot.id)
                if sel is None or _needs_variant(menu.item(sel.menu_item_id), sel.variant_id):
                    add(FieldRef.combo_choice, MissingReason.missing, lid)
                    break

    method = output.fulfillment.method
    if method is FulfillmentMethod.unknown:
        add(FieldRef.fulfillment_method, MissingReason.missing)
    if output.fulfillment.requested_time.state is SlotState.ambiguous:
        add(FieldRef.requested_time, MissingReason.ambiguous)
    if method is FulfillmentMethod.delivery and output.address.state is not SlotState.provided:
        reason = (
            MissingReason.ambiguous if output.address.state is SlotState.ambiguous else MissingReason.missing
        )
        add(FieldRef.address, reason)
    if output.payment.method is PaymentMethod.unknown and not output.payment.customer_claims_paid:
        add(FieldRef.payment_method, MissingReason.missing)
    if (
        method is FulfillmentMethod.pickup
        and menu.name_required_for_pickup
        and output.customer_name.state is not SlotState.provided
    ):
        add(FieldRef.customer_name, MissingReason.missing)
    return out
