"""Grounding checks for an extraction against its conversation and menu (spec §7).

Schema validation proves the shape; these prove the content is anchored:
every quote appears in the message it cites, and every id exists in the
catalog. Used for gold annotations, teacher labels (drop + log failures) and
model outputs (hallucination metrics).
"""

import re
from dataclasses import dataclass

from orderslm.schema.conversation import Conversation
from orderslm.schema.extraction import ExtractionOutput, Modification, ModificationKind
from orderslm.schema.menu import MenuCatalog


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
    allowed = item.allowed_modifier_ids if item else set()
    for mod in mods:
        for mid in filter(None, (mod.modifier_id, mod.replacement_modifier_id)):
            if menu.modifier(mid) is None:
                issues.append(Issue("UNKNOWN_MODIFIER", path, f"{mid!r} is not in the catalog"))
            elif mid not in allowed:
                issues.append(Issue("MODIFIER_NOT_ALLOWED", path, f"{mid!r} is not allowed on {item_id!r}"))
    # At most one choice per exclusive group (one crust, one milk), counting what is added.
    chosen: dict[str, list[str]] = {}
    for mod in mods:
        added = mod.replacement_modifier_id if mod.kind is ModificationKind.substitute else mod.modifier_id
        if mod.kind is not ModificationKind.remove and added and (m := menu.modifier(added)):
            if m.group in menu.exclusive_groups:
                chosen.setdefault(m.group, []).append(added)
    for group, ids in chosen.items():
        if len(ids) > 1:
            issues.append(Issue("EXCLUSIVE_GROUP_CONFLICT", path, f"more than one {group}: {ids}"))
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


def check_requests(output: ExtractionOutput) -> list[Issue]:
    """Every request with no catalog id must say what it is: not_on_menu or kitchen_note (extraction@0.4).
    Blocking for gold labels; a model output that leaves it open is handled at runtime (core/requests.py)."""
    issues: list[Issue] = []
    for item in output.items:
        mods = [m for h in item.halves for m in h.modifications] if item.halves else item.modifications
        for mod in mods:
            if mod.unclassified:
                issues.append(
                    Issue(
                        "UNCLASSIFIED_REQUEST",
                        f"items[{item.line_id}]",
                        f"{mod.raw_text!r} has no menu id: mark it not_on_menu or kitchen_note",
                    )
                )
    return issues


def check_all(output: ExtractionOutput, conversation: Conversation, menu: MenuCatalog) -> list[Issue]:
    return check_evidence(output, conversation) + check_catalog(output, menu) + check_requests(output)
