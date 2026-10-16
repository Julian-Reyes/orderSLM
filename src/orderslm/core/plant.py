"""Planted mistakes (spec §11b, §11d): copies of a correct order with exactly one known error, to measure what a
checker catches per error type. Deterministic: the same order, menu and seed always give the same copies.

Used on dev gold (tuning), on training labels (label audit) and, at final eval only, on test gold by this same
fixed code (Julian's ruling, 2026-10-13). A planted copy is never trained on.
"""

import random
from enum import StrEnum

from orderslm.schema.extraction import (
    Address,
    ExtractionOutput,
    FulfillmentMethod,
    ItemProposal,
    Modification,
    ModificationKind,
    Payment,
    PaymentMethod,
    SlotState,
)
from orderslm.schema.menu import MenuCatalog

PLANT_VERSION = "plant@0.1"


class Mistake(StrEnum):
    dropped_modification = "dropped_modification"
    added_modification = "added_modification"
    wrong_quantity = "wrong_quantity"
    swapped_item = "swapped_item"
    wrong_size = "wrong_size"
    missing_item = "missing_item"
    extra_item = "extra_item"
    fulfillment_flip = "fulfillment_flip"
    wrong_payment = "wrong_payment"


def _menu_lines(out: ExtractionOutput) -> list[ItemProposal]:
    return [x for x in out.items if x.menu_item_id is not None]


def _rebuild(out: ExtractionOutput, **update) -> ExtractionOutput:
    return ExtractionOutput.model_validate({**out.model_dump(mode="json"), **update})


def _items(lines: list[ItemProposal]) -> list[dict]:
    return [x.model_dump(mode="json") for x in lines]


def _next_line_id(out: ExtractionOutput) -> str:
    return f"L{max((int(x.line_id[1:]) for x in out.items), default=0) + 1}"


def _plant_one(
    out: ExtractionOutput, menu: MenuCatalog, mistake: Mistake, rng: random.Random
) -> ExtractionOutput | None:
    lines = list(out.items)
    menu_lines = _menu_lines(out)
    if mistake is Mistake.dropped_modification:
        with_mods = [x for x in menu_lines if x.modifications]
        if not with_mods:
            return None
        target = rng.choice(with_mods)
        drop = rng.randrange(len(target.modifications))
        new = target.model_copy(
            update={"modifications": [m for i, m in enumerate(target.modifications) if i != drop]}
        )
        return _rebuild(out, items=_items([new if x is target else x for x in lines]))
    if mistake is Mistake.added_modification:
        options = []
        for x in menu_lines:
            item = menu.item(x.menu_item_id or "")
            taken = {m.modifier_id for m in x.modifications}
            groups = {menu.modifier(m).group for m in taken if m and menu.modifier(m)}
            for a in item.addon_ids if item else []:
                mod = menu.modifier(a)
                if (
                    a not in taken
                    and mod
                    and not (mod.group in menu.exclusive_groups and mod.group in groups)
                ):
                    options.append((x, a))
        if not options:
            return None
        target, addon = rng.choice(options)
        mod = Modification(kind=ModificationKind.add, modifier_id=addon, raw_text=menu.modifier(addon).name)  # type: ignore[union-attr]
        new = target.model_copy(update={"modifications": [*target.modifications, mod]})
        return _rebuild(out, items=_items([new if x is target else x for x in lines]))
    if mistake is Mistake.wrong_quantity:
        counted = [x for x in lines if x.quantity is not None]
        if not counted:
            return None
        target = rng.choice(counted)
        q = target.quantity or 1
        new = target.model_copy(update={"quantity": q + 1 if q == 1 or rng.random() < 0.5 else q - 1})
        return _rebuild(out, items=_items([new if x is target else x for x in lines]))
    if mistake is Mistake.swapped_item:
        swappable = []
        for x in menu_lines:
            if x.combo_selections or x.modifications:
                continue
            item = menu.item(x.menu_item_id or "")
            same = [
                i for i in menu.items if i.category == item.category and i.id != item.id and not i.combo_slots
            ]  # type: ignore[union-attr]
            swappable += [(x, i) for i in same]
        if not swappable:
            return None
        target, other = rng.choice(swappable)
        variant = target.variant_id if other.variant(target.variant_id or "") else other.default_variant_id
        if other.variants and variant is None:
            variant = other.variants[0].id
        new = target.model_copy(update={"menu_item_id": other.id, "variant_id": variant})
        return _rebuild(out, items=_items([new if x is target else x for x in lines]))
    if mistake is Mistake.wrong_size:
        sized = []
        for x in lines:
            base = x.halves[0].menu_item_id if x.halves else x.menu_item_id
            item = menu.item(base or "")
            if item and x.variant_id and len(item.variants) > 1:
                sized += [(x, v.id) for v in item.variants if v.id != x.variant_id]
        if not sized:
            return None
        target, variant = rng.choice(sized)
        new = target.model_copy(update={"variant_id": variant})
        return _rebuild(out, items=_items([new if x is target else x for x in lines]))
    if mistake is Mistake.missing_item:
        if len(lines) < 2:
            return None
        drop = rng.randrange(len(lines))
        kept = [x for i, x in enumerate(lines) if i != drop]
        missing = [
            m.model_dump(mode="json") for m in out.missing_or_ambiguous if m.line_id != lines[drop].line_id
        ]
        question = out.clarification_question if missing else None
        return _rebuild(
            out, items=_items(kept), missing_or_ambiguous=missing, clarification_question=question
        )
    if mistake is Mistake.extra_item:
        present = {x.menu_item_id for x in lines}
        candidates = [i for i in menu.items if i.id not in present and not i.combo_slots and i.available]
        if not candidates or not lines:
            return None
        item = rng.choice(candidates)
        extra = ItemProposal(
            line_id=_next_line_id(out),
            menu_item_id=item.id,
            quantity=1,
            variant_id=item.default_variant_id or (item.variants[0].id if item.variants else None),
            evidence=lines[0].evidence,
        )
        return _rebuild(out, items=_items([*lines, extra]))
    if mistake is Mistake.fulfillment_flip:
        method = out.fulfillment.method
        if method is FulfillmentMethod.unknown:
            return None
        fulfillment = out.fulfillment.model_copy(
            update={
                "method": FulfillmentMethod.delivery
                if method is FulfillmentMethod.pickup
                else FulfillmentMethod.pickup
            }
        )
        address = (
            Address(state=SlotState.not_mentioned)
            if method is FulfillmentMethod.pickup
            else Address(state=SlotState.not_applicable)
        )
        return _rebuild(
            out,
            fulfillment=fulfillment.model_dump(mode="json"),
            address=address.model_dump(mode="json"),
            missing_or_ambiguous=[],
            clarification_question=None,
            customer_decision={"state": "pending", "agreed_while_incomplete": False, "evidence": []},
        )
    if mistake is Mistake.wrong_payment:
        method = out.payment.method
        if method not in (PaymentMethod.card, PaymentMethod.cash):
            return None
        other = PaymentMethod.cash if method is PaymentMethod.card else PaymentMethod.card
        payment = Payment(
            method=other, customer_claims_paid=out.payment.customer_claims_paid, evidence=out.payment.evidence
        )
        return _rebuild(out, payment=payment.model_dump(mode="json"))
    raise ValueError(mistake)


def plant(out: ExtractionOutput, menu: MenuCatalog, *, seed: str) -> dict[Mistake, ExtractionOutput]:
    """One copy per mistake type that applies to this order (types that don't apply are left out)."""
    copies: dict[Mistake, ExtractionOutput] = {}
    for mistake in Mistake:
        rng = random.Random(f"{PLANT_VERSION}|{seed}|{mistake.value}")
        try:
            copy = _plant_one(out, menu, mistake, rng)
        except ValueError:  # the copy would break the contract: skip this type for this order
            copy = None
        if copy is not None and copy != out:
            copies[mistake] = copy
    return copies
