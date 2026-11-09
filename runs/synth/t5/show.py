"""Print compact card views for a range: uv run python runs/synth/t5/show.py 13 40"""

import sys

from orderslm.synth import run

a, b = int(sys.argv[1]), int(sys.argv[2])
for c in run.load_cards("t5")[a - 1 : b]:
    t = c.extras[-1].removeprefix("target:")
    print(f"## {c.id} {c.business_id} {c.style.value} msgs~{c.customer_messages} {t} @{c.start_at:%H:%M}")
    print("  " + c.brief)
