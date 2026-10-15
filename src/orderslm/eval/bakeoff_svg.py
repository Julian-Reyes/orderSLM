"""Static accuracy-vs-cost chart (SVG, no dependencies) for docs/TEACHER_BAKEOFF.md.

One row per model setting, sorted by cost. Three aligned columns: cost per 1,000 conversations (bar), item F1 and
fully correct orders (dumbbells: hollow ring = before, raw output with scorer@0.1; filled dot = after, finalize +
scorer@0.2). Neutral ink for every row, the chosen teacher in the accent (blue, slot 1 of the dataviz reference
palette), labels at the row start so nothing collides.
"""

from html import escape
from pathlib import Path
from typing import Any

CHOSEN = "openai/gpt-6-luna@low"
INK, MUTED, GRID, SURFACE, ACCENT, BAR = "#2b2a27", "#6b6a64", "#e4e2dc", "#fcfcfb", "#2a78d6", "#b9b6ad"
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
NAMES = {
    "gpt-6-luna": "luna",
    "claude-haiku-5-5": "Haiku",
    "gemini-3.1-flash-lite": "Gemini",
    "deepseek-flash": "DeepSeek",
}
ROW_H, TOP, LABEL_W = 30, 74, 170
COLS = [  # key, title, x_min, x_max, ticks, width
    ("cost", "Cost per 1,000 conversations", 0.0, 3.0, [0, 1, 2, 3], 230),
    ("item_f1", "Item F1 (all item details right)", 0.70, 1.0, [0.7, 0.8, 0.9, 1.0], 300),
    ("exact_rate", "Fully correct orders", 0.40, 1.0, [0.4, 0.6, 0.8, 1.0], 300),
]
COL_GAP = 48


def _scale(val: float, x: float, lo: float, hi: float, w: float) -> float:
    return x + (min(max(val, lo), hi) - lo) / (hi - lo) * w


def write_svg(data: dict[str, Any], path: Path) -> None:
    bake = data["bakeoff"]
    rows = sorted(bake["variants"], key=lambda v: v["cost_per_1000_usd"])
    width = int(LABEL_W + sum(c[5] for c in COLS) + COL_GAP * len(COLS) + 60)
    plot_h = ROW_H * len(rows)
    height = TOP + plot_h + 96
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'font-family="{FONT}" role="img" aria-labelledby="t d">',
        '<title id="t">Teacher bake-off: accuracy and cost per model setting, before and after code rules</title>',
        f'<desc id="d">{len(rows)} model settings on {bake["conversations"]} dev conversations, prompt '
        f"{bake['prompt_version']}. Hollow ring: raw model output. Filled dot: after code computes the missing list and "
        "default sizes. Rows sorted by cost.</desc>",
        f'<rect width="{width}" height="{height}" fill="{SURFACE}"/>',
    ]
    x = LABEL_W + COL_GAP / 2
    for key, title, lo, hi, ticks, w in COLS:
        p.append(
            f'<text x="{x}" y="{TOP - 34}" font-size="13" font-weight="600" fill="{INK}">{escape(title)}</text>'
        )
        for t in ticks:
            tx = _scale(t, x, lo, hi, w)
            p.append(
                f'<line x1="{tx:.1f}" x2="{tx:.1f}" y1="{TOP - 8}" y2="{TOP + plot_h}" stroke="{GRID}" stroke-width="1"/>'
            )
            label = f"${t:.0f}" if key == "cost" else f"{t:.0%}"
            p.append(
                f'<text x="{tx:.1f}" y="{TOP - 14}" font-size="11" fill="{MUTED}" text-anchor="middle">{label}</text>'
            )
        for i, v in enumerate(rows):
            cy = TOP + i * ROW_H + ROW_H / 2
            chosen = v["id"] == CHOSEN
            color = ACCENT if chosen else INK
            if key == "cost":
                c = v["cost_per_1000_usd"]
                end = _scale(c, x, lo, hi, w)
                p.append(
                    f'<rect x="{x:.1f}" y="{cy - 6:.1f}" width="{end - x:.1f}" height="12" rx="2" '
                    f'fill="{ACCENT if chosen else BAR}"/>'
                )
                p.append(
                    f'<text x="{end + 6:.1f}" y="{cy + 4:.1f}" font-size="11" fill="{INK}">${c:.2f}</text>'
                )
                continue
            b, a = v["before"][key], v["after"][key]
            bx, ax = _scale(b, x, lo, hi, w), _scale(a, x, lo, hi, w)
            if abs(ax - bx) > 1:
                p.append(
                    f'<line x1="{bx:.1f}" x2="{ax:.1f}" y1="{cy}" y2="{cy}" stroke="{color}" stroke-width="2" '
                    'stroke-opacity="0.4"/>'
                )
            p.append(
                f'<circle cx="{bx:.1f}" cy="{cy}" r="4.5" fill="{SURFACE}" stroke="{color}" stroke-width="2"/>'
            )
            p.append(
                f'<circle cx="{ax:.1f}" cy="{cy}" r="5" fill="{color}" stroke="{SURFACE}" stroke-width="2"/>'
            )
            if key == "exact_rate":
                n = v["after"]["conversations"]
                before_n, after_n = v["before"]["exact"], v["after"]["exact"]
                text = f"{before_n}→{after_n} of {n}" if before_n != after_n else f"{after_n} of {n}"
            else:
                text = f"{b:.1%}→{a:.1%}" if abs(a - b) > 1e-9 else f"{a:.1%}"
            p.append(
                f'<text x="{x + w + 8:.1f}" y="{cy + 4:.1f}" font-size="10.5" fill="{MUTED}">{text}</text>'
            )
        x += w + COL_GAP
    for i, v in enumerate(rows):
        cy = TOP + i * ROW_H + ROW_H / 2
        chosen = v["id"] == CHOSEN
        name = f"{NAMES.get(v['model'], v['model'])} {v['variant']}" + (" (teacher)" if chosen else "")
        p.append(
            f'<text x="16" y="{cy + 4:.1f}" font-size="12.5" font-weight="{600 if chosen else 400}" '
            f'fill="{ACCENT if chosen else INK}">{escape(name)}</text>'
        )
    ly = TOP + plot_h + 32
    p += [
        f'<circle cx="22" cy="{ly}" r="4.5" fill="{SURFACE}" stroke="{INK}" stroke-width="2"/>',
        f'<text x="32" y="{ly + 4}" font-size="12" fill="{INK}">Before: raw model output, original scoring</text>',
        f'<circle cx="320" cy="{ly}" r="5" fill="{INK}"/>',
        f'<text x="330" y="{ly + 4}" font-size="12" fill="{INK}">'
        "After: code computes missing info; blank size = menu default</text>",
        f'<circle cx="720" cy="{ly}" r="5" fill="{ACCENT}"/>',
        f'<text x="730" y="{ly + 4}" font-size="12" fill="{INK}">Chosen teacher</text>',
        f'<text x="16" y="{ly + 28}" font-size="11" fill="{MUTED}">{bake["conversations"]} dev conversations (Source A, '
        f"Claude-written), prompt {bake['prompt_version']}. Same calls in both views, so cost doesn't change.</text>",
        f'<text x="16" y="{ly + 44}" font-size="11" fill="{MUTED}">Dev data guided the prompt fixes, so these are '
        "not held-out results.</text>",
        "</svg>",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(p) + "\n")
