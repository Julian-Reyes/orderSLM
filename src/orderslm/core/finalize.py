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

The model's own missing list and question are ignored, so a mistake there can't make the output invalid.
"""

import json
from typing import Any

from pydantic import ValidationError

from orderslm.core.missing import required_missing
from orderslm.core.replies import template_question
from orderslm.schema.extraction import DecisionState, ExtractionOutput, FieldRef, MissingInfo, MissingReason
from orderslm.schema.menu import MenuCatalog

FINALIZE_VERSION = "finalize@0.1"
_JUDGMENT = {
    (FieldRef.item_menu_match, MissingReason.off_menu): MissingReason.ambiguous,
    (FieldRef.item_variant, MissingReason.missing): MissingReason.ambiguous,
}


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
    out = fill_default_variants(output, menu)
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
        data["missing_or_ambiguous"] = []
        data["clarification_question"] = None
        return finalize(ExtractionOutput.model_validate(data), menu, judgments, lang), None
    except (ValueError, ValidationError) as e:  # json.JSONDecodeError subclasses ValueError
        return None, str(e)
