"""Code-side completion of a model's extraction (Julian, 2026-10-15).

The model extracts the facts; the rules are applied in code, the same way every time:

1. An unstated variant of an item with a default is the default ("2 cheeseburgers" = 2 single cheeseburgers).
   A size the item doesn't have (`unmatched_variant_text`) stays null, so it is still asked about.
2. `missing_or_ambiguous` is recomputed by `core.missing.required_missing`. Only the reasons that need the text
   are taken from the model: an unmatched item it called `ambiguous` (not `off_menu`), a variant it called
   `ambiguous` (not `missing`).
3. `clarification_question` is the template question (core.replies.template_question): built from the menu and
   the missing list only, so it never offers what the business doesn't do and never states an amount.
4. A `confirmed` decision while something is missing becomes `pending` + `agreed_while_incomplete` (the guide's
   rule), keeping the customer's quoted yes as evidence.
5. An id the menu doesn't have is never passed on as a normal line (finalize@0.2, the gaps check_catalog reports):
   an unknown item, or a half-and-half with an unknown or non-splittable half, becomes an off-menu line (its first
   evidence quote as `unmatched_text`, so the bot asks); an unknown size becomes `unmatched_variant_text` (asked), or is dropped on an item with no sizes;
   a combo pick with an unknown slot, choice or size is dropped (the choice is asked); an add-on id not in the
   catalog or not allowed on the item loses its id and becomes an unverified request (asked, softly).

The model's own missing list and question are ignored, so a mistake there can't make the output invalid.
"""

import json
from typing import Any

from pydantic import ValidationError

from orderslm.core.missing import required_missing
from orderslm.core.replies import template_question
from orderslm.schema.extraction import (
    CustomerDecision,
    DecisionState,
    ExtractionOutput,
    FieldRef,
    ItemProposal,
    MissingInfo,
    MissingReason,
    Modification,
)
from orderslm.schema.label import ModelOrder
from orderslm.schema.menu import MenuCatalog, MenuItem

FINALIZE_VERSION = "finalize@0.2"
_JUDGMENT = {
    (FieldRef.item_menu_match, MissingReason.off_menu): MissingReason.ambiguous,
    (FieldRef.item_variant, MissingReason.missing): MissingReason.ambiguous,
}


def _known_mod(menu: MenuCatalog, item: MenuItem, mod: Modification) -> Modification:
    ids = [i for i in (mod.modifier_id, mod.replacement_modifier_id) if i is not None]
    if all(menu.modifier(i) is not None and i in item.allowed_modifier_ids for i in ids):
        return mod
    return mod.model_copy(update={"modifier_id": None, "replacement_modifier_id": None})


def _off_menu(line: ItemProposal) -> ItemProposal:
    return ItemProposal(
        line_id=line.line_id,
        unmatched_text=line.evidence[0].quote,
        quantity=line.quantity,
        notes=line.notes,
        evidence=line.evidence,
    )


def _known_line(menu: MenuCatalog, line: ItemProposal) -> ItemProposal:
    """Rule 5: the line with every id the menu doesn't have resolved to something the code asks about."""
    if line.unmatched_text is not None:
        return line
    if line.halves is not None:
        items = [menu.item(h.menu_item_id) for h in line.halves]
        if any(i is None or not i.splittable for i in items):
            return _off_menu(line)
        halves = [
            h.model_copy(update={"modifications": [_known_mod(menu, i, m) for m in h.modifications]})
            for h, i in zip(line.halves, items, strict=True)
        ]
        line = line.model_copy(update={"halves": halves})
        base = items[0]
    else:
        base = menu.item(line.menu_item_id or "")
        if base is None:
            return _off_menu(line)
        picks = []
        slots = {s.id: s for s in base.combo_slots}
        for sel in line.combo_selections:
            slot, choice = slots.get(sel.slot_id), menu.item(sel.menu_item_id)
            if slot is None or choice is None or sel.menu_item_id not in slot.choices:
                continue
            if sel.variant_id is not None and choice.variant(sel.variant_id) is None:
                continue
            picks.append(sel)
        line = line.model_copy(
            update={
                "modifications": [_known_mod(menu, base, m) for m in line.modifications],
                "combo_selections": picks,
            }
        )
    if line.variant_id is not None and base.variant(line.variant_id) is None:
        # An item with sizes asks which one; on an item with none there is nothing to choose, so the id goes.
        asked = line.variant_id if base.variants else None
        line = line.model_copy(update={"variant_id": None, "unmatched_variant_text": asked})
    return line


def known_ids(output: ExtractionOutput, menu: MenuCatalog) -> ExtractionOutput:
    return output.model_copy(update={"items": [_known_line(menu, line) for line in output.items]})


def _default_variant(menu: MenuCatalog, item_id: str | None, variant_id: str | None) -> str | None:
    if variant_id is not None or item_id is None:
        return variant_id
    item = menu.item(item_id)
    return item.default_variant_id if item is not None else None


def fill_default_variants(output: ExtractionOutput, menu: MenuCatalog) -> ExtractionOutput:
    out = output.model_copy(deep=True)
    for line in out.items:
        if line.menu_item_id is not None and line.unmatched_variant_text is None:
            line.variant_id = _default_variant(menu, line.menu_item_id, line.variant_id)
        for sel in line.combo_selections:
            sel.variant_id = _default_variant(menu, sel.menu_item_id, sel.variant_id)
    return out


def _model_judgments(raw_missing: Any) -> set[tuple[str, str, str | None]]:
    """(field, reason, line_id) the model marked ambiguous, read leniently from its raw JSON."""
    found = set()
    for m in raw_missing if isinstance(raw_missing, list) else []:
        if isinstance(m, dict) and m.get("reason") == MissingReason.ambiguous.value:
            found.add((str(m.get("field")), MissingReason.ambiguous.value, m.get("line_id")))
    return found


def finalize(
    output: ExtractionOutput,
    menu: MenuCatalog,
    judgments: set[tuple[str, str, str | None]] | None = None,
    lang: str = "en",
) -> ExtractionOutput:
    out = fill_default_variants(known_ids(output, menu), menu)
    judgments = (
        judgments
        if judgments is not None
        else _model_judgments([m.model_dump(mode="json") for m in output.missing_or_ambiguous])
    )
    missing: list[MissingInfo] = []
    for m in required_missing(out, menu):
        alt = _JUDGMENT.get((m.field, m.reason))
        if alt is not None and (m.field.value, alt.value, m.line_id) in judgments:
            m = MissingInfo(field=m.field, reason=alt, line_id=m.line_id)
        missing.append(m)
    decision = out.customer_decision
    if decision.state is DecisionState.confirmed and missing:
        decision = decision.model_copy(
            update={"state": DecisionState.pending, "agreed_while_incomplete": True}
        )
    if decision.state is DecisionState.cancelled:
        missing = []
    # The template reads only items, fulfillment and address, so it can run on the order before the missing list
    # and question are attached; the contract requires both together.
    question = template_question(missing, out, menu, lang) if missing else None
    data = out.model_dump(mode="json")
    data["customer_decision"] = decision.model_dump(mode="json")
    data["missing_or_ambiguous"] = [m.model_dump(mode="json") for m in missing]
    data["clarification_question"] = question or None
    return ExtractionOutput.model_validate(data)


def parse_and_finalize(
    raw_text: str, menu: MenuCatalog, lang: str = "en"
) -> tuple[ExtractionOutput | None, str | None]:
    """Validate a model's raw JSON with its missing list and question set aside, then finalize.
    Returns (output, error); never raises."""
    try:
        data = json.loads(raw_text)
        if not isinstance(data, dict):
            return None, "output is not a JSON object"
        judgments = _model_judgments(data.get("missing_or_ambiguous"))
        return finalize(_facts(data), menu, judgments, lang), None
    except (ValueError, ValidationError) as e:  # json.JSONDecodeError subclasses ValueError
        return None, str(e)


def _facts(data: dict[str, Any]) -> ExtractionOutput:
    """Validate the order facts with neutral placeholders for the three rules that tie the missing list to the
    rest (off-menu lines listed, no gaps on confirmed/cancelled, question iff gaps); finalize rebuilds all three
    and the result is validated again in full."""
    decision = CustomerDecision.model_validate(data.get("customer_decision") or {})
    items = data.get("items") if isinstance(data.get("items"), list) else []
    placeholder = [
        {"field": "item_menu_match", "reason": "off_menu", "line_id": it.get("line_id")}
        for it in items
        if isinstance(it, dict) and it.get("unmatched_text") is not None
    ]
    data = {
        **data,
        "missing_or_ambiguous": placeholder,
        "clarification_question": "?" if placeholder else None,
    }
    data["customer_decision"] = CustomerDecision().model_dump(mode="json")
    return ExtractionOutput.model_validate(data).model_copy(update={"customer_decision": decision})


def finalize_order(order: ModelOrder, menu: MenuCatalog, lang: str = "en") -> ExtractionOutput:
    """A model's order facts (schema/label.py) → the finalized ExtractionOutput. Its ambiguity flags are the
    only text judgments taken from the model."""
    judgments = {(f.field, MissingReason.ambiguous.value, f.line_id) for f in order.ambiguity_flags}
    data = order.model_dump(mode="json", exclude={"ambiguity_flags"})
    return finalize(_facts(data), menu, judgments, lang)
