"""Case-study data for the website (julianreyes.dev/orderslm): every number on the page, read from saved runs.

    make site-data      # → docs/site/case-study.json (copied next to the page as data.json)

Julian, 2026-11-05: "get the information and data we have live". Dev numbers are tuning numbers; fresh numbers
measure fixes made on dev (finalize@0.2 also used fresh: "used for fixes"); the sealed test split is not used yet.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

from orderslm.paths import ROOT, RUNS

OUT = ROOT / "docs" / "site" / "case-study.json"
TEACHER = "openai/gpt-6-luna@low"
STUDENT_BAKEOFF = RUNS / "student-bakeoff" / "20261019T182539Z"
M4 = RUNS / "m4-report" / "m4_report.json"
DATA = RUNS / "student-data"
CHECK = RUNS / "order-check" / "20261104T000454Z-0.2"
DEPLOY = RUNS / "student-deploy" / "20261105T121614Z"
COMPARE = {
    "dev": RUNS / "student-compare" / "20261105T143617Z",
    "fresh": RUNS / "student-compare" / "20261105T143627Z",
}
SD = RUNS / "student-dev"
# (label, data version, dev run, fresh run)
STUDENTS = [
    (
        "Qwen3.5-0.8B, v1 data",
        "v1",
        "20261023T140955Z-qwen3.5-0.8b-single",
        "20261026T131201Z-qwen3.5-0.8b-single-fresh",
    ),
    (
        "Qwen3.5-2B, v1 data",
        "v1",
        "20261023T115559Z-qwen3.5-2b-single",
        "20261027T123832Z-qwen3.5-2b-single-fresh",
    ),
    (
        "Qwen3.5-2B mixed, v1 data",
        "v1",
        "20261023T140955Z-qwen3.5-2b-mixed",
        "20261027T123832Z-qwen3.5-2b-mixed-fresh",
    ),
    (
        "Qwen3.5-0.8B, v2 data (picked)",
        "v2",
        "20261026T131201Z-qwen3.5-0.8b-single-v2",
        "20261026T131201Z-qwen3.5-0.8b-single-v2-fresh",
    ),
    (
        "Qwen3.5-2B, v2 data",
        "v2",
        "20261103T115227Z-qwen3.5-2b-single-v2",
        "20261103T115227Z-qwen3.5-2b-single-v2-fresh",
    ),
    (
        "Qwen3.5-2B mixed, v2 data",
        "v2",
        "20261027T123832Z-qwen3.5-2b-mixed-v2",
        "20261027T123832Z-qwen3.5-2b-mixed-v2-fresh",
    ),
]
FORMATS = [  # (format, dev run, fresh run, deploy job with the GPU timing on the 50-request sample)
    (
        "F16",
        "20261104T115735Z-qwen3.5-0.8b-single-v2-f16",
        "20261105T121614Z-qwen3.5-0.8b-single-v2-f16-fresh",
        "gpu-f16-timing",
    ),
    (
        "Q8_0",
        "20261104T115735Z-qwen3.5-0.8b-single-v2-q8_0",
        "20261105T121614Z-qwen3.5-0.8b-single-v2-q8_0-fresh",
        "gpu-q8_0-timing",
    ),
    (
        "Q4_K_M",
        "20261105T121614Z-qwen3.5-0.8b-single-v2-q4_k_m",
        "20261105T121614Z-qwen3.5-0.8b-single-v2-q4_k_m-fresh",
        "gpu-q4_k_m",
    ),
]


def _j(path: Path) -> Any:
    return json.loads(path.read_text())


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def student_scores(run: Path) -> dict[str, Any]:
    m = _j(run / "metrics.json")
    o, i = m["order"], m["intent"]["all"]
    return {
        "run": _rel(run),
        "chats": o["conversations"],
        "exact": o["exact_match"],
        "exact_ci95": o["exact_match_ci95"],
        "same_action": o["action_match"],
        "item_f1": round(o["item"]["f1"], 3),
        "messages": i["messages"],
        "intents_right": i["primary_correct"],
        "invalid_answers": m["requests"] - sum(v["valid"] for v in m["contract_valid"].values()),
        "latency_ms_p50": (m.get("latency_ms") or {}).get("p50"),
        "scorer": m["scorer_version"],
        "finalize": m["finalize_version"],
    }


def teacher() -> dict[str, Any]:
    c = _j(RUNS / "teacher-bakeoff" / "chart-data.json")
    rows = []
    for v in c["bakeoff"]["variants"]:
        rows.append(
            {
                "setting": v["id"],
                "cost_per_1000_usd": round(v["cost_per_1000_usd"], 2),
                "valid_json": v["after"]["json_valid"],
                "item_f1_before": round(v["before"]["item_f1"], 3),
                "item_f1_after": round(v["after"]["item_f1"], 3),
                "exact_before": v["before"]["exact"],
                "exact_after": v["after"]["exact"],
            }
        )
    rows.sort(key=lambda r: r["cost_per_1000_usd"])
    dev = _j(
        next(
            p
            for p in sorted((RUNS / "label-dev").glob("*luna@low"))
            if (p / "metrics.json").exists() and _j(p / "metrics.json").get("scorer_version") == "scorer@0.4"
        )
        / "metrics.json"
    )
    return {
        "chats": c["bakeoff"]["conversations"],
        "run": c["bakeoff"]["path"],
        "settings": rows,
        "picked": TEACHER,
        "dev_all": {"chats": dev["order"]["conversations"], "exact": dev["order"]["exact_match"]},
        "views": c["views"],
    }


def student_bakeoff() -> dict[str, Any]:
    s = _j(STUDENT_BAKEOFF / "summary.json")
    return {
        "run": _rel(STUDENT_BAKEOFF),
        "chats": 20,
        "models": {
            k: {
                "json_parses": v.get("json_valid_after_fence_strip"),
                "valid_labels": v.get("contract_valid"),
                "hit_token_limit": v.get("hit_token_limit"),
                "latency_s_p50": round(v["latency_p50_ms"] / 1000) if v.get("latency_p50_ms") else None,
                "parameters": (v.get("load") or {}).get("parameters"),
            }
            for k, v in s.items()
            if not k.startswith("teacher")
        },
    }


def training_data() -> dict[str, Any]:
    m4 = _j(M4) if M4.exists() else {}
    out = {}
    for ver in ("student-data@0.1", "student-data@0.2"):
        man = _j(DATA / ver / "manifest.json")
        single = man["sets"]["single"]
        out[ver] = {
            "train_chats": single["train"]["rows"],
            "valid_chats": single["valid"]["rows"],
            "per_generator": single["train"]["per_generator"],
            "hand_fixed_labels": single["train"].get("label_hand_fixed", 0),
        }
        if "mixed" in man["sets"]:
            out[ver]["mixed_train_chats"] = man["sets"]["mixed"]["train"]["rows"]
    out["m4_report"] = {k: m4[k] for k in ("training_set",) if k in m4}
    return out


def packaging() -> dict[str, Any]:
    s = _j(DEPLOY / "summary.json")
    ref = {k: student_scores(SD / v) for k, v in (("dev", STUDENTS[3][2]), ("fresh", STUDENTS[3][3]))}
    rows = [
        {
            "format": "fp16 (transformers)",
            "gguf_gb": None,
            "dev": ref["dev"],
            "fresh": ref["fresh"],
            "t4_latency_s_p50": round(s["reference_latency"]["dev"]["latency_ms"]["p50"] / 1000, 1),
        }
    ]
    for fmt, dev, fresh, timing in FORMATS:
        t = s["jobs"][timing]["timing_sample"]
        cpu = s["jobs"].get(f"cpu-{fmt.lower()}")
        rows.append(
            {
                "format": fmt,
                "gguf_gb": round(s["gguf"][fmt]["bytes"] / 1e9, 2),
                "dev": student_scores(SD / dev),
                "fresh": student_scores(SD / fresh),
                "t4_latency_s_p50": round(t["latency_ms"]["p50"] / 1000, 1),
                "t4_latency_s_p95": round(t["latency_ms"]["p95"] / 1000, 1),
                "t4_output_tok_s": round(t["output_tokens_per_s"]["p50"]),
                "peak_gpu_mib": s["jobs"][timing]["memory"]["peak_gpu_used_mib"],
                "cpu_latency_s_p50": round(cpu["timing_sample"]["latency_ms"]["p50"] / 1000, 1)
                if cpu
                else None,
            }
        )
    return {
        "run": _rel(DEPLOY),
        "llama_cpp": "b11700",
        "rows": rows,
        "picked": "Q8_0",
        "compare_runs": {k: _rel(v) for k, v in COMPARE.items()},
    }


def checker() -> dict[str, Any]:
    m = _j(CHECK / "metrics.json")
    names = {
        "luna": "GPT-6 Luna (LLM)",
        "jev": "Jev (decision model)",
        "decisions": "OpenAI Decisions",
        "openai-decisions": "OpenAI Decisions",
    }
    return {
        "run": _rel(CHECK),
        "wrong_orders": m["wrong_orders"],
        "right_orders": m["right_orders"],
        "checkers": {
            names.get(k, k): {"caught": v["caught"]["flagged"], "false_alarms": v["false_alarms"]["flagged"]}
            for k, v in m["checkers"].items()
        },
    }


EXAMPLE = (
    "a-dev-065",
    STUDENTS[3][2],
)  # short, all caps, typos, a correction, time, name and payment; exact match


def example() -> dict[str, Any]:
    """One dev chat, the picked student's own answer after its last message, and the code's price for it."""
    from orderslm.core.finalize import finalize_order
    from orderslm.core.pricing import DeterministicPricing
    from orderslm.eval.dataset import load_eval_split
    from orderslm.eval.student_dev import parse
    from orderslm.menus import load_menu
    from orderslm.schema.conversation import Split

    cid, run = EXAMPLE
    conv = next(ac.conversation for ac in load_eval_split(Split.dev) if ac.conversation.id == cid)
    outs = [json.loads(x) for x in (SD / run / "outputs.jsonl").read_text().splitlines()]
    last = max((r for r in outs if r["id"].startswith(f"{cid}#")), key=lambda r: int(r["id"].split("#")[1]))
    student, _ = parse(last["text"])
    menu = load_menu(conv.business_id)
    quote = DeterministicPricing().quote(menu, finalize_order(student.order, menu)).data
    o = student.order
    exact = next(
        json.loads(x)
        for x in (SD / run / "order_rows.jsonl").read_text().splitlines()
        if json.loads(x)["conversation_id"] == cid
    )["exact"]
    return {
        "chat_id": cid,
        "business": menu.name,
        "messages": [m.text for m in conv.messages],
        "intent": student.intent.primary.value,
        "model_order": {
            "items": [
                {
                    "menu_item_id": i.menu_item_id,
                    "variant_id": i.variant_id,
                    "quantity": i.quantity,
                    "evidence": [e.quote for e in i.evidence],
                }
                for i in o.items
            ],
            "method": o.fulfillment.method.value,
            "time": o.fulfillment.requested_time.normalized_local,
            "payment": o.payment.method.value if o.payment.method else None,
            "name": o.customer_name.value,
        },
        "priced_by_code": {
            "lines": [
                {
                    "name": q.display_name,
                    "quantity": q.quantity,
                    "unit_cents": q.unit_price_cents,
                    "total_cents": q.line_total_cents,
                }
                for q in quote.lines
            ],
            "total_cents": quote.total_cents,
            "verified_by": quote.verified_by,
        },
        "exact_match_with_gold": exact,
        "run": _rel(SD / run),
        "latency_ms": last["latency_ms"],
    }


def spend() -> dict[str, Any]:
    text = (ROOT / "docs" / "COSTS.md").read_text()
    total = float(re.search(r"Spent to date \| \*\*\$([0-9.]+)\*\*", text).group(1))
    return {
        "api_usd": total,
        "ceiling_usd": 10.0,
        "gpu": "Kaggle free tier (2 × T4)",
        "source": "docs/COSTS.md",
    }


def build() -> dict[str, Any]:
    return {
        "note": "Generated by `make site-data` from saved runs. Dev = tuning data; fresh = new chats written after the "
        "dev-based fixes (some fresh chats also led to fixes: 'used for fixes'); the sealed test split is not used yet.",
        "teacher_bakeoff": teacher(),
        "student_bakeoff": student_bakeoff(),
        "training_data": training_data(),
        "students": [
            {"student": n, "data": d, "dev": student_scores(SD / dev), "fresh": student_scores(SD / fresh)}
            for n, d, dev, fresh in STUDENTS
        ],
        "packaging": packaging(),
        "order_checker": checker(),
        "example": example(),
        "spend": spend(),
    }


def main(argv: list[str] | None = None) -> int:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {_rel(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
