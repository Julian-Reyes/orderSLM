"""M6 error review: every dev mistake of each student (and the teacher, as reference) put in a category.

For each chat a model doesn't get fully right, from its saved outputs:

- **invalid:** no valid answer at the last customer message (the contract rule it broke);
- **items:** gold and predicted items left after exact matches are paired on the dish (menu id, off-menu, halves);
  a pair differs in quantity / variant / modifications / combo picks, an unpaired gold item is *missing*, an
  unpaired predicted one *extra* (variants normalized as the scorer does);
- **fields:** method, time, address, payment, name, decision, missing list (gold vs predicted values);
- **no-order chats:** items predicted where gold has no order;

plus every intent mistake (gold → predicted, invalid = None) with the customer's message. Chats and messages are
marked by which models got them wrong, so shared mistakes (hard or unclear cases) stand apart from one model's.

    make student-errors ARGS="runs/student-dev/<a> [...]"   # → runs/student-errors/<time>/

Dev only (tuning), not held-out.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from orderslm.core.finalize import fill_default_variants, finalize_order
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Split
from orderslm.schema.extraction import ExtractionOutput, ItemProposal
from orderslm.schema.label import StudentOutput

from . import label_dev
from .dataset import load_eval_split
from .metrics import FIELDS, field_values, item_key
from .student_bakeoff import TEACHER_RUN, strip_fences
from .student_dev import request_id

EXPERIMENT = "student-errors"
ERRORS_VERSION = "student-errors@0.1"
TEACHER = "teacher"
PARTS = ("quantity", "variant", "modifications", "combo_picks")


def describe(item: ItemProposal) -> str:
    if item.unmatched_text is not None:
        what = f"off-menu '{item.unmatched_text}'"
    elif item.halves is not None:
        what = "half " + " / ".join(h.menu_item_id for h in item.halves)
    else:
        what = item.menu_item_id or "?"
    bits = [f"{item.quantity}× {what}"]
    if item.variant_id:
        bits.append(item.variant_id)
    bits += [f"{m.kind.value} {m.modifier_id or m.raw_text}" for m in item.modifications]
    bits += [f"{c.slot_id}={c.menu_item_id}" for c in item.combo_selections]
    return ", ".join(bits)


def item_diffs(gold: ExtractionOutput, pred: ExtractionOutput) -> list[dict[str, Any]]:
    """Items left after exact matches, paired on the dish; a pair lists the parts that differ."""
    left_g = list(gold.items)
    left_p = list(pred.items)
    for g in list(left_g):
        k = item_key(g)
        match = next((p for p in left_p if item_key(p) == k), None)
        if match is not None:
            left_g.remove(g)
            left_p.remove(match)
    out = []
    for g in left_g:
        kg = item_key(g)
        same_dish = [p for p in left_p if item_key(p)[0] == kg[0]]
        if not same_dish:
            out.append({"kind": "missing_item", "gold": describe(g)})
            continue
        p = max(same_dish, key=lambda p: sum(a == b for a, b in zip(item_key(p), kg, strict=False)))
        left_p.remove(p)
        kp = item_key(p)
        parts = [n for n, a, b in zip(PARTS, kg[1:], kp[1:], strict=False) if a != b]
        out.append(
            {"kind": "wrong_" + "+".join(parts), "parts": parts, "gold": describe(g), "pred": describe(p)}
        )
    out += [{"kind": "extra_item", "pred": describe(p)} for p in left_p]
    return out


def chat_errors(ac, pred: ExtractionOutput | None, invalid: str | None) -> dict[str, Any] | None:
    """The mistakes in one chat's final order, or None if it is fully right (same rule as the scorer)."""
    if pred is None:
        return {"invalid": invalid or "no output"}
    menu = load_menu(ac.conversation.business_id)
    pred = fill_default_variants(pred, menu)
    if ac.gold_extraction is None:
        return {"items_without_order": [describe(i) for i in pred.items]} if pred.items else None
    gold = fill_default_variants(ac.gold_extraction, menu)
    items = item_diffs(gold, pred)
    gv, pv = field_values(gold), field_values(pred)
    fields = {f: {"gold": gv[f], "pred": pv[f]} for f in FIELDS if gv[f] != pv[f]}
    if not items and not fields:
        return None
    return {"items": items, "fields": fields}


def _validation_detail(text: str) -> str:
    try:
        StudentOutput.model_validate_json(strip_fences(text))
    except ValidationError as e:
        x = e.errors()[0]
        return f"{'.'.join(map(str, x['loc']))}: {x['msg']}"[:200]
    except ValueError as e:
        return str(e)[:200]
    return "finalize error"


def student_predictions(run_dir: Path, dev: dict) -> tuple[str, dict, dict]:
    """(student, {chat: (final order or None, invalid detail)}, {(chat, message): predicted intent or None})."""
    metrics = json.loads((run_dir / "metrics.json").read_text())
    outputs = {
        json.loads(x)["id"]: json.loads(x) for x in (run_dir / "outputs.jsonl").read_text().splitlines()
    }
    orders = {}
    for cid, ac in dev.items():
        conv = ac.conversation
        rec = outputs.get(request_id(cid, conv.customer_indices()[-1]), {})
        order, detail = None, rec.get("error", "no output")
        if "text" in rec:
            try:
                out = StudentOutput.model_validate_json(strip_fences(rec["text"]))
                order = finalize_order(out.order, load_menu(conv.business_id), conv.language)
                detail = None
            except (ValueError, ValidationError):
                detail = _validation_detail(rec["text"])
        orders[cid] = (order, detail)
    intents = {
        (r["conversation_id"], r["message_index"]): r["pred"]
        for r in (json.loads(x) for x in (run_dir / "intent_rows.jsonl").read_text().splitlines())
    }
    return metrics["student"], orders, intents


def teacher_predictions(dev: dict) -> tuple[str, dict, dict]:
    orders = {}
    for cid, ac in dev.items():
        rec = json.loads((TEACHER_RUN / "outputs" / f"{cid}.json").read_text())
        order, err = None, rec.get("error", "no output")
        if "response" in rec:
            _, order, err, _ = label_dev._parse(
                rec["response"]["text"],
                ac,
                json.loads((TEACHER_RUN / "manifest.json").read_text())["teacher"],
            )
        orders[cid] = (order, err)
    intents = {
        (r["conversation_id"], r["message_index"]): r["pred"]
        for r in (json.loads(x) for x in (TEACHER_RUN / "intent_rows.jsonl").read_text().splitlines())
    }
    return TEACHER, orders, intents


def review(run_dirs: list[Path]) -> dict[str, Any]:
    dev = {ac.conversation.id: ac for ac in load_eval_split(Split.dev)}
    models = [student_predictions(d, dev) for d in run_dirs] + [teacher_predictions(dev)]
    students = [m[0] for m in models if m[0] != TEACHER]
    chats, messages = [], []
    for cid, ac in sorted(dev.items()):
        per_model = {name: chat_errors(ac, *orders[cid]) for name, orders, _ in models}
        wrong = [n for n, e in per_model.items() if e]
        if wrong:
            chats.append(
                {
                    "conversation_id": cid,
                    "scenarios": [s.value for s in ac.scenarios],
                    "wrong": wrong,
                    "all_students_wrong": all(per_model[s] for s in students),
                    "errors": {n: e for n, e in per_model.items() if e},
                }
            )
        text = {m.index: m.text for m in ac.conversation.messages}
        for r in ac.gold_routing:
            key = (cid, r.message_index)
            preds = {name: intents.get(key) for name, _, intents in models}
            bad = {n: p for n, p in preds.items() if p != r.decision.primary.value}
            if bad:
                messages.append(
                    {
                        "conversation_id": cid,
                        "message_index": r.message_index,
                        "text": text[r.message_index],
                        "gold": r.decision.primary.value,
                        "pred": bad,
                        "all_students_wrong": all(s in bad for s in students),
                    }
                )
    return {"models": [m[0] for m in models], "students": students, "chats": chats, "messages": messages}


def summarize(r: dict[str, Any]) -> dict[str, Any]:
    """Counts per model: chats wrong by category, item-mistake kinds, field mistakes, intent confusions."""
    out: dict[str, Any] = {}
    for m in r["models"]:
        errs = [c["errors"][m] for c in r["chats"] if m in c["errors"]]
        cats = Counter()
        kinds, fields = Counter(), Counter()
        for e in errs:
            if "invalid" in e:
                cats["invalid answer"] += 1
                continue
            if "items_without_order" in e:
                cats["items where there is no order"] += 1
                continue
            cats["item mistakes" if e["items"] else "fields only"] += 1
            kinds.update(i["kind"] for i in e["items"])
            fields.update(list(e["fields"]))
        intents = [x for x in r["messages"] if m in x["pred"]]
        out[m] = {
            "chats_wrong": len(errs),
            "categories": dict(cats.most_common()),
            "item_kinds": dict(kinds.most_common()),
            "fields": dict(fields.most_common()),
            "intents_wrong": len(intents),
            "confusions": dict(Counter(f"{x['gold']} → {x['pred'][m]}" for x in intents).most_common()),
        }
    students = r["students"]
    out["overlap"] = {
        "chats_all_students_wrong": sum(c["all_students_wrong"] for c in r["chats"]),
        "chats_all_students_and_teacher_wrong": sum(
            c["all_students_wrong"] and TEACHER in c["errors"] for c in r["chats"]
        ),
        "chats_one_student_only": sum(len([w for w in c["wrong"] if w in students]) == 1 for c in r["chats"]),
        "messages_all_students_wrong": sum(x["all_students_wrong"] for x in r["messages"]),
        "messages_one_student_only": sum(
            len([s for s in x["pred"] if s in students]) == 1 for x in r["messages"]
        ),
    }
    by_scenario: dict[str, Counter] = defaultdict(Counter)
    for c in r["chats"]:
        for s in c["scenarios"]:
            for m in c["wrong"]:
                by_scenario[s][m] += 1
    out["chats_wrong_by_scenario"] = {s: dict(v) for s, v in sorted(by_scenario.items())}
    return out


def _fmt_errors(e: dict[str, Any]) -> list[str]:
    if "invalid" in e:
        return [f"invalid: {e['invalid']}"]
    if "items_without_order" in e:
        return [f"items with no gold order: {e['items_without_order']}"]
    lines = []
    for i in e["items"]:
        if i["kind"] == "missing_item":
            lines.append(f"missing {i['gold']}")
        elif i["kind"] == "extra_item":
            lines.append(f"extra {i['pred']}")
        else:
            lines.append(f"{'+'.join(i['parts'])}: gold {i['gold']} | pred {i['pred']}")
    lines += [f"{f}: gold {v['gold']} | pred {v['pred']}" for f, v in e["fields"].items()]
    return lines


def write_report(out: Path, r: dict[str, Any], s: dict[str, Any]) -> None:
    models = r["models"]
    lines = [
        "# M6 error review on dev",
        "",
        "Every chat or customer message a model got wrong, from saved outputs. Dev (tuning), not held-out. The teacher "
        "(`teacher-label@0.7`, the labels the students learned from) is shown as a reference.",
        "",
        "| | " + " | ".join(models) + " |",
        "|---|" + "---|" * len(models),
        "| chats not fully right (of 91) | " + " | ".join(str(s[m]["chats_wrong"]) for m in models) + " |",
    ]
    cats = sorted({c for m in models for c in s[m]["categories"]})
    lines += [
        f"| · {c} | " + " | ".join(str(s[m]["categories"].get(c, 0)) for m in models) + " |" for c in cats
    ]
    kinds = sorted(
        {k for m in models for k in s[m]["item_kinds"]},
        key=lambda k: -sum(s[m]["item_kinds"].get(k, 0) for m in models),
    )
    lines += [
        f"| item: {k} | " + " | ".join(str(s[m]["item_kinds"].get(k, 0)) for m in models) + " |"
        for k in kinds
    ]
    fields = sorted({f for m in models for f in s[m]["fields"]})
    lines += [
        f"| field: {f} | " + " | ".join(str(s[m]["fields"].get(f, 0)) for m in models) + " |" for f in fields
    ]
    lines += ["| intents wrong (of 268) | " + " | ".join(str(s[m]["intents_wrong"]) for m in models) + " |"]
    lines += ["", f"Overlap: {s['overlap']}", "", "Chats wrong by scenario (a chat can have several):", ""]
    lines += [f"- {k}: {v}" for k, v in s["chats_wrong_by_scenario"].items()]
    lines += ["", "## Intent mistakes", ""]
    for m in models:
        lines.append(f"- **{m}:** " + "; ".join(f"{k} ×{v}" for k, v in s[m]["confusions"].items()))
    lines += ["", "| chat#msg | customer message | gold | wrong answers |", "|---|---|---|---|"]
    for x in r["messages"]:
        t = x["text"].replace("|", "/").replace("\n", " ")[:120]
        preds = ", ".join(f"{m}: {p}" for m, p in x["pred"].items())
        lines.append(f"| {x['conversation_id']}#{x['message_index']} | {t} | {x['gold']} | {preds} |")
    lines += ["", "## Order mistakes, chat by chat", ""]
    for c in r["chats"]:
        flag = " — **all students**" if c["all_students_wrong"] else ""
        lines.append(f"### {c['conversation_id']} ({', '.join(c['scenarios'])}){flag}")
        for m, e in c["errors"].items():
            lines.append(f"- **{m}:** " + "; ".join(_fmt_errors(e)))
        lines.append("")
    (out / "report.md").write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dirs", type=Path, nargs="+")
    args = ap.parse_args(argv)
    r = review(args.run_dirs)
    s = summarize(r)
    started = datetime.now(UTC)
    out = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}"
    out.mkdir(parents=True)
    (out / "errors.json").write_text(json.dumps(r, indent=1, ensure_ascii=False, default=str) + "\n")
    (out / "summary.json").write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n")
    manifest = {
        "experiment": EXPERIMENT,
        "errors_version": ERRORS_VERSION,
        "inputs": [str(d.resolve().relative_to(ROOT)) for d in args.run_dirs]
        + [str(TEACHER_RUN.relative_to(ROOT))],
        "created_at": started.isoformat(),
        "git_commit": git_commit(),
        "cost_usd": 0.0,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_report(out, r, s)
    print(json.dumps(s, indent=1, ensure_ascii=False)[:4000])
    print(f"→ {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
