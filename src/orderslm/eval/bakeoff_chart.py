"""Chart data for the teacher bake-off write-up and the case study (Julian, 2026-10-15).

Every number is recomputed from saved run outputs, in two views:
- before: the model's raw JSON, scored with scorer@0.1 (an unstated default variant counts as different).
- after:  the same JSON through core.finalize (code computes the missing list, question and default variants),
          scored with scorer@0.2 (blank = default variant).

    uv run python -m orderslm.eval.bakeoff_chart     # writes runs/teacher-bakeoff/chart-data.json + the SVG chart
"""

import json
import statistics
import sys
from typing import Any

from orderslm.core.finalize import FINALIZE_VERSION, parse_and_finalize
from orderslm.extractors.teacher import to_result
from orderslm.llm.types import ChatResponse
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.schema.conversation import Split

from .dataset import load_eval_split
from .metrics import SCORER_VERSION, aggregate, score_conversation

EXPERIMENT_DIR = RUNS / "teacher-bakeoff"
BAKEOFF_RUN = "20261015T182916Z-full-skip5"  # all 12 variants, 35 conversations, prompt v0.2
HEAD_TO_HEAD_RUN = "20261015T185040Z-full-remaining"  # luna low vs Haiku on-medium, 51 conversations
LUNA_DEV_RUNS = [  # luna low on all 91 dev, prompt fixes and the repeat
    ("prompt v0.3", "20261015T190341Z-full-all"),
    ("prompt v0.4, run 1", "20261015T191233Z-full-all"),
    ("prompt v0.4, run 2 (repeat)", "20261015T192653Z-full-all"),
]
OUT_JSON = EXPERIMENT_DIR / "chart-data.json"
OUT_SVG = ROOT / "docs" / "figures" / "teacher-bakeoff-accuracy-cost.svg"


def _view(scores: list) -> dict[str, Any]:
    m = aggregate(scores)
    it = m["item"]
    return {
        "json_valid": m["json_valid"],
        "conversations": m["conversations"],
        "items": {k: it[k] for k in ("gold_items", "tp", "fp", "fn")},
        "item_f1": it["f1"],
        "exact": m["exact_match"],
        "exact_rate": m["exact_match_rate"],
        "exact_ci95": m["exact_match_ci95"],
        "field_accuracy": m["field_accuracy"],
        "grounding_issues": m["grounding"]["conversations_with_issues"],
    }


def run_data(run_id: str) -> dict[str, Any]:
    d = EXPERIMENT_DIR / run_id
    manifest = json.loads((d / "manifest.json").read_text())
    ids = manifest["data"]["conversation_ids"]
    gold = {ac.conversation.id: ac for ac in load_eval_split(Split.dev) if ac.conversation.id in ids}
    variants = []
    for v, settings in manifest["variants"].items():
        before, after, costs, latencies, tokens = [], [], [], [], {}
        for cid in ids:
            rec = json.loads((d / "outputs" / v.replace("/", "__") / f"{cid}.json").read_text())
            ac = gold[cid]
            menu = load_menu(ac.conversation.business_id)
            view_menu = menu.extractor_view()
            if "error" in rec:  # provider error: nothing to score in either view
                before.append(score_conversation(ac, None, view_menu, normalize_variants=False))
                after.append(score_conversation(ac, None, view_menu))
                continue
            resp = ChatResponse.model_validate(rec["response"])
            before.append(score_conversation(ac, to_result(resp).output, view_menu, normalize_variants=False))
            finalized, _ = parse_and_finalize(resp.text, menu, ac.conversation.language)
            after.append(score_conversation(ac, finalized, view_menu))
            costs.append(resp.cost_micros)
            latencies.append(resp.latency_ms)
            for k, val in resp.usage.model_dump().items():
                tokens[k] = tokens.get(k, 0) + val
        n = len(costs)
        provider, rest = v.split("/", 1)
        model, variant = rest.split("@")
        variants.append(
            {
                "id": v,
                "provider": provider,
                "model": model,
                "variant": variant,
                "provider_default": settings.get("provider_default"),
                "settings": settings.get("extra_body"),
                "calls": n,
                "cost_usd": sum(costs) / 1e6,
                "cost_per_1000_usd": (sum(costs) / n * 1000 / 1e6) if n else None,
                "tokens_per_conversation": {k: round(val / n, 1) for k, val in tokens.items()} if n else {},
                "latency_ms_p50": round(statistics.median(latencies)) if latencies else None,
                "before": _view(before),
                "after": _view(after),
            }
        )
    return {
        "run_id": run_id,
        "path": str(d.relative_to(ROOT)),
        "prompt_version": manifest["prompt_version"],
        "conversations": len(ids),
        "cost_usd": manifest.get("actual_cost_micros", 0) / 1e6,
        "variants": variants,
    }


def build() -> dict[str, Any]:
    return {
        "views": {
            "before": "raw model JSON, scorer@0.1 (unstated default variant counts as different)",
            "after": f"model JSON through {FINALIZE_VERSION}, {SCORER_VERSION} (blank = default variant)",
        },
        "data": "dev split, Source A (Claude-written, reviewed by Julian); prompt-tuning data, not held-out results",
        "bakeoff": run_data(BAKEOFF_RUN),
        "head_to_head": run_data(HEAD_TO_HEAD_RUN),
        "luna_dev": [{"label": label, **run_data(run_id)} for label, run_id in LUNA_DEV_RUNS],
    }


def main() -> int:
    data = build()
    OUT_JSON.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    from .bakeoff_svg import write_svg

    write_svg(data, OUT_SVG)
    print(f"Wrote {OUT_SVG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
