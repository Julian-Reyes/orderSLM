"""The mega-menu (spec §11e): the three training menus combined into one food-court menu, for the ~20% mega-menu
training chats (mixed student) and the menu-narrowing experiment (M7). Built by code from the menus, never by hand:

    make mega-menu      # writes data/menus/mega/food-court.json

Merging rules: an item id used by two stalls is one item when the names match (soft drinks: the version with
sizes wins); a modifier id used twice is one modifier when name and price match (group from the first stall),
otherwise the later stall's gets a suffixed id and every reference is rewritten; kitchen requests with the same
id combine their categories. The held-out menu is never included.
"""

import json
import sys
from collections.abc import Iterable
from datetime import time

from orderslm.menus import MEGA_DIR, load_menus
from orderslm.schema.menu import DeliveryPolicy, KitchenRequest, MenuCatalog, MenuItem, Modifier

MEGA_ID = "food-court"
STALLS = ("corner-patty", "halfmoon-pizza", "morning-crumb")


def _rename(ids: Iterable[str], renames: dict[str, str]) -> list[str]:
    return [renames.get(i, i) for i in ids]


def build(menus: dict[str, MenuCatalog] | None = None) -> MenuCatalog:
    menus = menus or load_menus()
    modifiers: dict[str, Modifier] = {}
    items: dict[str, MenuItem] = {}
    kitchen: dict[str, KitchenRequest] = {}
    for stall in STALLS:
        menu = menus[stall]
        if menu.held_out:
            raise ValueError("the held-out menu never goes into the mega-menu")
        renames: dict[str, str] = {}
        for m in menu.modifiers:
            seen = modifiers.get(m.id)
            if seen is None:
                modifiers[m.id] = m
            elif (seen.name, seen.price_cents) != (m.name, m.price_cents):
                new_id = f"{m.id}_{stall.split('-')[0]}"
                renames[m.id] = new_id
                modifiers[new_id] = m.model_copy(update={"id": new_id})
        for item in menu.items:
            item = item.model_copy(
                update={
                    "ingredient_ids": _rename(item.ingredient_ids, renames),
                    "addon_ids": _rename(item.addon_ids, renames),
                }
            )
            seen_item = items.get(item.id)
            if seen_item is None:
                items[item.id] = item
            elif seen_item.name != item.name:
                raise ValueError(
                    f"item id {item.id!r} names two different things: {seen_item.name} / {item.name}"
                )
            elif len(item.variants) > len(seen_item.variants):
                items[item.id] = item  # the soft drink with sizes
        for k in menu.accepted_kitchen_requests:
            seen_k = kitchen.get(k.id)
            if seen_k is None:
                kitchen[k.id] = k
            else:
                kitchen[k.id] = seen_k.model_copy(
                    update={
                        "aliases": sorted(set(seen_k.aliases) | set(k.aliases)),
                        "categories": sorted(set(seen_k.categories) | set(k.categories)),
                    }
                )
    return MenuCatalog(
        business_id=MEGA_ID,
        name="Food Court (Corner Patty, Halfmoon Pizza, Morning Crumb)",
        timezone="America/New_York",
        opens_at=time(7, 0),
        closes_at=time(23, 0),
        delivery=DeliveryPolicy(available=True, fee_cents=399, min_order_cents=1500),
        accepts_payment=["card", "cash"],
        name_required_for_pickup=True,
        exclusive_groups=sorted({g for s in STALLS for g in menus[s].exclusive_groups}),
        modifiers=list(modifiers.values()),
        items=list(items.values()),
        accepted_kitchen_requests=list(kitchen.values()),
    )


def main() -> int:
    menu = build()
    MEGA_DIR.mkdir(parents=True, exist_ok=True)
    path = MEGA_DIR / f"{MEGA_ID}.json"
    path.write_text(
        json.dumps(menu.model_dump(mode="json", exclude_none=True), indent=2, ensure_ascii=False) + "\n"
    )
    print(f"Wrote {path}: {len(menu.items)} items, {len(menu.modifiers)} modifiers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
