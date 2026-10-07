"""Loading menus. The held-out menu (data/menus/held_out/) is for test conversations only.

`load_menus()` excludes it by default, so synthetic generation, prompt tuning and
training code that loads "all menus" can never pick it up by accident. Code that
legitimately needs it (writing/annotating test conversations, final eval) asks
with `include_held_out=True`.

Run `python -m orderslm.menus` (or `make menus`) to validate and summarize.
"""

import hashlib
import json
from pathlib import Path

from orderslm.paths import MENUS
from orderslm.schema.menu import MenuCatalog

HELD_OUT_DIR = MENUS / "held_out"


def _load(path: Path) -> MenuCatalog:
    return MenuCatalog.model_validate(json.loads(path.read_text()))


def load_menus(*, include_held_out: bool = False) -> dict[str, MenuCatalog]:
    paths = sorted(MENUS.glob("*.json"))
    if include_held_out:
        paths += sorted(HELD_OUT_DIR.glob("*.json"))
    menus: dict[str, MenuCatalog] = {}
    for p in paths:
        menu = _load(p)
        if menu.held_out != (p.parent == HELD_OUT_DIR):
            raise ValueError(f"{p}: held_out={menu.held_out} doesn't match its directory")
        if p.stem != menu.business_id:
            raise ValueError(f"{p}: file name must be the business_id ({menu.business_id})")
        menus[menu.business_id] = menu
    return menus


def load_menu(business_id: str, *, include_held_out: bool = False) -> MenuCatalog:
    menus = load_menus(include_held_out=include_held_out)
    if business_id not in menus:
        hint = " (held-out menus need include_held_out=True)" if not include_held_out else ""
        raise KeyError(f"unknown business {business_id!r}{hint}")
    return menus[business_id]


def menu_version(menu: MenuCatalog) -> str:
    """Content fingerprint recorded on every quote and run, e.g. 'corner-patty@3f9a1c0d2b4e'."""
    canonical = json.dumps(menu.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return f"{menu.business_id}@{hashlib.sha256(canonical.encode()).hexdigest()[:12]}"


def main() -> None:
    for menu in load_menus(include_held_out=True).values():
        variants = sum(len(i.variants) for i in menu.items)
        flags = [
            f
            for f, on in (
                ("HELD OUT", menu.held_out),
                ("name required for pickup", menu.name_required_for_pickup),
                ("no delivery", not menu.delivery.available),
            )
            if on
        ]
        print(
            f"{menu_version(menu):40} {menu.name:24} items={len(menu.items):3} variants={variants:3} "
            f"modifiers={len(menu.modifiers):3} {', '.join(flags)}"
        )


if __name__ == "__main__":
    main()
