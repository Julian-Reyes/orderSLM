"""Grounding checks for an extraction against its conversation and menu (spec §7).

Schema validation proves the shape; these prove the content is anchored:
every quote appears in the message it cites, and every id exists in the
catalog. Used for gold annotations, teacher labels (drop + log failures) and
model outputs (hallucination metrics).
"""

import re
from dataclasses import dataclass

from shoproute.schema.conversation import Conversation
from shoproute.schema.extraction import ExtractionOutput, Modification
from shoproute.schema.menu import MenuCatalog, ModifierKind


@dataclass(frozen=True)
class Issue:
    code: str  # EVIDENCE_NOT_FOUND, UNKNOWN_ITEM, UNKNOWN_VARIANT, ...
    path: str
    message: str


def _norm(text: str) -> str:
    """Case- and whitespace-insensitive, so a quote's capitalization doesn't fail a correct citation."""
    return re.sub(r"\s+", " ", text).strip().casefold()


def check_evidence(output: ExtractionOutput, conversation: Conversation) -> list[Issue]:
    issues: list[Issue] = []
    by_index = {m.index: m for m in conversation.messages}
    for path, ev in output.iter_evidence():
        msg = by_index.get(ev.message_index)
        if msg is None:
            issues.append(Issue("EVIDENCE_BAD_INDEX", path, f"message {ev.message_index} does not exist"))
        elif _norm(ev.quote) not in _norm(msg.text):
            issues.append(
                Issue("EVIDENCE_NOT_FOUND", path, f"{ev.quote!r} is not in message {ev.message_index}")
            )
    return issues


def _check_mods(menu: MenuCatalog, item_id: str, mods: list[Modification], path: str) -> list[Issue]:
    issues: list[Issue] = []
    item = menu.item(item_id)
    allowed = set(item.modifier_ids) if item else set()
    for mod in mods:
        for mid in filter(None, (mod.modifier_id, mod.replacement_modifier_id)):
            if menu.modifier(mid) is None:
                issues.append(Issue("UNKNOWN_MODIFIER", path, f"{mid!r} is not in the catalog"))
            elif mid not in allowed:
                issues.append(Issue("MODIFIER_NOT_ALLOWED", path, f"{mid!r} is not allowed on {item_id!r}"))
        if mod.modifier_id and (m := menu.modifier(mod.modifier_id)):
            expected = {"add": ModifierKind.add, "remove": ModifierKind.remove}.get(mod.kind.value)
            if expected is not None and m.kind is not expected:
                issues.append(
                    Issue("MODIFIER_KIND", path, f"{mod.modifier_id!r} is a {m.kind.value} modifier")
                )
    return issues


def check_catalog(output: ExtractionOutput, menu: MenuCatalog) -> list[Issue]:
    issues: list[Issue] = []
    for item in output.items:
        path = f"items[{item.line_id}]"
        if item.halves is not None:
            for half in item.halves:
                entry = menu.item(half.menu_item_id)
                if entry is None:
                    issues.append(
                        Issue("UNKNOWN_ITEM", path, f"half {half.menu_item_id!r} is not on the menu")
                    )
                    continue
                if not entry.splittable:
                    issues.append(
                        Issue("NOT_SPLITTABLE", path, f"{half.menu_item_id!r} can't be half-and-half")
                    )
                issues += _check_mods(menu, half.menu_item_id, half.modifications, path)
            base = menu.item(item.halves[0].menu_item_id)
            if base and item.variant_id and item.variant_id not in {v.id for v in base.variants}:
                issues.append(
                    Issue("UNKNOWN_VARIANT", path, f"{item.variant_id!r} is not a size of the pizza")
                )
            continue
        if item.menu_item_id is None:
            continue  # off-menu: unmatched_text, nothing to check against the catalog
        entry = menu.item(item.menu_item_id)
        if entry is None:
            issues.append(Issue("UNKNOWN_ITEM", path, f"{item.menu_item_id!r} is not on the menu"))
            continue
        if item.variant_id is not None and item.variant_id not in {v.id for v in entry.variants}:
            issues.append(
                Issue("UNKNOWN_VARIANT", path, f"{item.variant_id!r} is not a variant of {entry.id!r}")
            )
        issues += _check_mods(menu, entry.id, item.modifications, path)
        slots = {s.id: s for s in entry.combo_slots}
        for sel in item.combo_selections:
            slot = slots.get(sel.slot_id)
            if slot is None:
                issues.append(
                    Issue("UNKNOWN_COMBO_SLOT", path, f"{sel.slot_id!r} is not a slot of {entry.id!r}")
                )
            elif sel.menu_item_id not in slot.choices:
                issues.append(
                    Issue("INVALID_COMBO_CHOICE", path, f"{sel.menu_item_id!r} not allowed in {slot.id!r}")
                )
    return issues


def check_all(output: ExtractionOutput, conversation: Conversation, menu: MenuCatalog) -> list[Issue]:
    return check_evidence(output, conversation) + check_catalog(output, menu)
