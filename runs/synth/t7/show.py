"""Print compact card views for a range: uv run python runs/synth/t7/show.py 13 40"""

import sys
from zoneinfo import ZoneInfo

from orderslm.menus import load_menu
from orderslm.synth import run

a, b = int(sys.argv[1]), int(sys.argv[2])
for c in run.load_cards("t7")[a - 1 : b]:
    t = c.extras[-1].removeprefix("target:")
    day = next((e.removeprefix("day:") for e in c.extras if e.startswith("day:")), "")
    local = c.start_at.astimezone(ZoneInfo(load_menu(c.business_id).timezone))
    print(
        f"## {c.id} {c.business_id} {c.style.value} msgs~{c.customer_messages} {t} {day} @{local:%a %b %d %H:%M}"
    )
    print("  " + c.brief)
