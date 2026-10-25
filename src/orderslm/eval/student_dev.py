"""M6 trained students on dev at every customer message (Julian, 2026-10-20: score the mid-chat boxes too).

A student is trained on full chats and answers for the latest customer message, so it is asked once per customer
message: the chat cut after that message (`student-extract@0.1` prompt, built exactly as the training rows by
`train/data.py`). Dev gold has an intent for every customer message (`gold_routing`) and the final order
(`gold_extraction`):

- **intents:** each request's `intent` vs gold for that message (all 268), split into the last customer message
  (what training saw) and earlier ones (mid-chat);
- **order:** the answer at the last customer message, finalized in code (`core/finalize`), scored with the M3 scorer;
- **contract validity** at every message (a mid-chat order has no gold, but it must still be a valid StudentOutput).

The teacher's dev numbers (`teacher-label@0.7`, the label prompt behind the training data) are shown for reference.
Dev is for tuning: these are not held-out results. Requests go to Kaggle (dev chats + menus as model input, allowed
by docs/KAGGLE.md); gold stays here.

    make student-dev ARGS="report runs/student-dev/<id>"     # rebuild metrics + report from saved outputs
"""

import argparse
import dataclasses
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

from pydantic import ValidationError

from orderslm.core.finalize import FINALIZE_VERSION, finalize_order
from orderslm.menus import load_menu
from orderslm.paths import ROOT
from orderslm.schema.conversation import Split
from orderslm.schema.label import StudentOutput
from orderslm.train import data

from .dataset import load_eval_split
from .metrics import SCORER_VERSION, aggregate, score_conversation
from .stats import wilson
from .student_bakeoff import TEACHER_RUN, strip_fences

EXPERIMENT = "student-dev"


def request_id(conversation_id: str, message_index: int) -> str:
    return f"{conversation_id}#{message_index}"


def build_requests() -> list[dict[str, Any]]:
    """One request per dev customer message: the chat cut after it, as the training rows show a chat."""
    system = data.system_prompt()
    out = []
    for ac in load_eval_split(Split.dev):
        conv = ac.conversation
        menu = load_menu(conv.business_id)
        for k in conv.customer_indices():
            prefix = conv.model_copy(update={"messages": conv.messages[: k + 1]})
            out.append(
                {
                    "id": request_id(conv.id, k),
                    "conversation_id": conv.id,
                    "message_index": k,
                    "system": system,
                    "user": data.user_prompt(prefix, menu),
                }
            )
    return out


def parse(text: str) -> tuple[StudentOutput | None, str | None]:
    try:
        return StudentOutput.model_validate_json(strip_fences(text)), None
    except (ValueError, ValidationError) as e:
        return None, str(e).splitlines()[0][:200]


def report(run_dir: Path) -> dict[str, Any]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    outputs = {
        r["id"]: r for r in (json.loads(x) for x in (run_dir / "outputs.jsonl").read_text().splitlines())
    }
    dev = load_eval_split(Split.dev)
    scores, intents, errors = [], [], Counter()
    validity = {"last": [0, 0], "earlier": [0, 0]}
    for ac in dev:
        conv = ac.conversation
        menu = load_menu(conv.business_id)
        last = conv.customer_indices()[-1]
        parsed: dict[int, StudentOutput | None] = {}
        for k in conv.customer_indices():
            rec = outputs.get(request_id(conv.id, k))
            out, err = (
                (None, (rec or {}).get("error", "no output"))
                if not rec or "text" not in rec
                else parse(rec["text"])
            )
            parsed[k] = out
            pos = "last" if k == last else "earlier"
            validity[pos][0] += out is not None
            validity[pos][1] += 1
            if err:
                errors[err.split(" [")[0][:80]] += 1
        order = None
        if parsed[last] is not None:
            try:
                order = finalize_order(parsed[last].order, menu, conv.language)
            except (ValueError, ValidationError):
                errors["finalize error"] += 1
        scores.append(score_conversation(ac, order, menu))
        for r in ac.gold_routing:
            g, p = r.decision, parsed.get(r.message_index)
            pi = p.intent if p else None
            gold_set = {g.primary.value} | ({g.secondary.value} if g.secondary else set())
            pred_set = (
                ({pi.primary.value} | ({pi.secondary.value} if pi.secondary else set())) if pi else set()
            )
            intents.append(
                {
                    "conversation_id": conv.id,
                    "message_index": r.message_index,
                    "position": "last" if r.message_index == last else "earlier",
                    "gold": g.primary.value,
                    "pred": pi.primary.value if pi else None,
                    "primary_ok": bool(pi) and pi.primary == g.primary,
                    "set_ok": pred_set == gold_set,
                }
            )

    def acc(rows: list[dict]) -> dict[str, Any]:
        ok = sum(r["primary_ok"] for r in rows)
        return {
            "messages": len(rows),
            "primary_correct": ok,
            "primary_accuracy": round(ok / len(rows), 4) if rows else None,
            "primary_ci95": wilson(ok, len(rows)),
            "label_set_correct": sum(r["set_ok"] for r in rows),
        }

    per_label: dict[str, dict[str, int]] = defaultdict(lambda: {"gold": 0, "correct": 0, "predicted": 0})
    for r in intents:
        per_label[r["gold"]]["gold"] += 1
        per_label[r["gold"]]["correct"] += r["primary_ok"]
        if r["pred"]:
            per_label[r["pred"]]["predicted"] += 1
    recs = list(outputs.values())
    lat = sorted(r["latency_ms"] for r in recs if "text" in r)
    teacher = TEACHER_RUN / "metrics.json"
    metrics = {
        "student": manifest["student"],
        "prompt_version": data.STUDENT_PROMPT_VERSION,
        "data_version": manifest.get("data_version"),
        "scorer_version": SCORER_VERSION,
        "finalize_version": FINALIZE_VERSION,
        "requests": len(recs),
        "contract_valid": {k: {"valid": v[0], "of": v[1]} for k, v in validity.items()},
        "invalid_reasons": dict(errors.most_common(10)),
        "hit_token_limit": sum(r.get("finish_reason") == "length" for r in recs),
        "latency_ms": {"p50": lat[len(lat) // 2], "p95": lat[int(0.95 * (len(lat) - 1))]} if lat else None,
        "output_tokens_p50": median(r["output_tokens"] for r in recs if "text" in r) if lat else None,
        "order": aggregate(scores),
        "intent": {
            "all": acc(intents),
            "last_message": acc([r for r in intents if r["position"] == "last"]),
            "earlier_messages": acc([r for r in intents if r["position"] == "earlier"]),
            "per_gold_label": {k: dict(v) for k, v in sorted(per_label.items())},
            "confusions": [
                {"gold": g, "pred": p, "count": c}
                for (g, p), c in Counter(
                    (r["gold"], r["pred"]) for r in intents if not r["primary_ok"]
                ).most_common()
            ],
        },
        "teacher_reference": json.loads(teacher.read_text()) if teacher.exists() else None,
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (run_dir / "intent_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in intents))
    # per chat, for paired comparisons between students (student_compare)
    (run_dir / "order_rows.jsonl").write_text(
        "".join(json.dumps(dataclasses.asdict(s)) + "\n" for s in scores)
    )
    _write_report(run_dir, metrics)
    return metrics


def _write_report(run_dir: Path, m: dict[str, Any]) -> None:
    o, i, t = m["order"], m["intent"], m["teacher_reference"]
    cv = m["contract_valid"]

    def pct(x: dict) -> str:
        lo, hi = x["primary_ci95"]
        return f"{x['primary_correct']}/{x['messages']} ({100 * x['primary_accuracy']:.1f}%, 95% CI {lo:.3f}–{hi:.3f})"

    lines = [
        f"# `{m['student']}` on dev at every customer message",
        "",
        f"Prompt `{m['prompt_version']}`, data `{m['data_version']}`, scorer `{m['scorer_version']}`, "
        f"finalize `{m['finalize_version']}`. Dev numbers (tuning), not held-out results.",
        "",
        "| | Student | Teacher (`teacher-label@0.7`, reference) |",
        "|---|---|---|",
        f"| Valid answers, last customer message | {cv['last']['valid']}/{cv['last']['of']} | "
        f"{t['order']['json_valid'] if t else '?'}/{t['order']['conversations'] if t else '?'} |",
        f"| Valid answers, earlier messages | {cv['earlier']['valid']}/{cv['earlier']['of']} | n/a (one call per chat) |",
        f"| Intent, all customer messages | {pct(i['all'])} | "
        + (f"{t['intent']['primary_correct']}/{t['intent']['customer_messages']} |" if t else "? |"),
        f"| Intent, last message | {pct(i['last_message'])} | |",
        f"| Intent, earlier messages (mid-chat) | {pct(i['earlier_messages'])} | |",
        f"| Items (F1) | {o['item']['tp']} found / {o['item']['fp']} extra / {o['item']['fn']} missed "
        f"(F1 {o['item']['f1']}) | " + (f"F1 {t['order']['item']['f1']} |" if t else "? |"),
        f"| Fully correct orders | {o['exact_match']}/{o['conversations']} (95% CI {o['exact_match_ci95']}) | "
        + (f"{t['order']['exact_match']}/{t['order']['conversations']} |" if t else "? |"),
        "",
        f"Field accuracy: {o['field_accuracy']}",
        "",
        f"Hit the token limit: {m['hit_token_limit']}; latency p50/p95 {m['latency_ms']} ms (T4, fp16, greedy); "
        f"output tokens p50 {m['output_tokens_p50']}.",
        f"Invalid answers by reason: {m['invalid_reasons'] or 'none'}",
        "",
        "| gold label | messages | primary correct | predicted as this |",
        "|---|---|---|---|",
    ]
    for k, v in sorted(i["per_gold_label"].items(), key=lambda kv: -kv[1]["gold"]):
        lines.append(f"| {k} | {v['gold']} | {v['correct']} | {v['predicted']} |")
    lines += ["", "Mistakes (gold → predicted):", ""]
    lines += [f"- {c['gold']} → {c['pred']}: {c['count']}" for c in i["confusions"]]
    (run_dir / "report.md").write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report")
    r.add_argument("run_dir", type=Path)
    args = ap.parse_args(argv)
    m = report(args.run_dir)
    print((args.run_dir / "report.md").read_text())
    print(f"→ {args.run_dir.resolve().relative_to(ROOT)}  ({m['requests']} answers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
