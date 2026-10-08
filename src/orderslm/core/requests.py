"""Requests with no catalog id ("warm", "well done", "artichoke hearts"): what the code makes of them.

Order of decisions, deterministic:
1. The menu's `accepted_kitchen_requests` first. A match is a free kitchen note, whatever the model said.
2. Otherwise `not_on_menu`: the business doesn't offer it. Never priced; the customer is told and asked.
3. Otherwise (nothing set, or a `kitchen_note` the menu doesn't list): unverified. Treated like an
   unavailable option with softer wording ("we may not be able to do X"), so it never reaches the
   ticket unresolved.

Used by core/missing.py (what to ask), core/pricing.py (what can be priced), core/replies.py and
core/ticket.py (what is shown).
"""

import re
from enum import StrEnum

from orderslm.schema.extraction import ItemProposal, Modification
from orderslm.schema.menu import KitchenRequest, MenuCatalog, MenuItem

REQUESTS_VERSION = "requests@0.1"


class RequestStatus(StrEnum):
    catalog = "catalog"  # names a menu option: priced by the normal rules
    kitchen_note = "kitchen_note"  # on the menu's accepted list: free, printed on the ticket
    not_on_menu = "not_on_menu"  # the business doesn't offer it: tell the customer
    unverified = "unverified"  # unknown to the menu and not flagged: ask, softly


def _words(text: str) -> str:
    return " " + re.sub(r"[^a-z0-9']+", " ", text.casefold()).strip() + " "


def accepted_request(menu: MenuCatalog, item: MenuItem | None, text: str) -> KitchenRequest | None:
    """The accepted kitchen request this text asks for, matched on whole words, if any applies to the item."""
    words = _words(text)
    for kr in menu.accepted_kitchen_requests:
        if kr.categories and (item is None or item.category not in kr.categories):
            continue
        if any(_words(phrase) in words for phrase in (kr.name, *kr.aliases)):
            return kr
    return None


def request_status(menu: MenuCatalog, item: MenuItem | None, mod: Modification) -> RequestStatus:
    if mod.catalog_id is not None:
        return RequestStatus.catalog
    if accepted_request(menu, item, mod.raw_text) is not None:
        return RequestStatus.kitchen_note
    if mod.not_on_menu:
        return RequestStatus.not_on_menu
    return RequestStatus.unverified


def line_requests(
    menu: MenuCatalog, line: ItemProposal
) -> list[tuple[MenuItem | None, Modification, RequestStatus]]:
    """Every modification on a line (both halves of a half-and-half) with its status."""
    if line.halves:
        pairs = [(menu.item(h.menu_item_id), m) for h in line.halves for m in h.modifications]
    else:
        item = menu.item(line.menu_item_id or "")
        pairs = [(item, m) for m in line.modifications]
    return [(item, m, request_status(menu, item, m)) for item, m in pairs]


UNRESOLVED = {RequestStatus.not_on_menu, RequestStatus.unverified}
