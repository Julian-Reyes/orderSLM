"""M5 student bake-off (spec §9): the candidate students zero-shot on ~20 dev chats, on a Kaggle T4 (docs/KAGGLE.md B).

Each student gets the exact request the teacher got for its labels (`synth/label.build_request`: label prompt
`teacher-label@0.7`, the TeacherLabel JSON schema, menu + chat), so a zero-shot student is asked the same task the
teacher answered, and is scored by the same code (`label_dev.report`: contract validity, item F1, exact orders,
intents per customer message). The teacher's saved dev outputs on the same chats are scored alongside (free).

    make student-bakeoff ARGS="export"                       # stage requests + run dir
    make kaggle-push JOB=student-bakeoff                     # upload, start the GPU kernel
    make kaggle-pull JOB=student-bakeoff                     # when it's done
    make student-bakeoff ARGS="import runs/student-bakeoff/<id>"

Dev is for tuning: these numbers choose models, they are not held-out results. Only requests go to Kaggle; gold
stays here.
"""

import argparse
import json
import random
import shutil
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from statistics import median
from typing import Any

from pydantic import ValidationError

from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Split
from orderslm.schema.label import TeacherLabel
from orderslm.synth import label as lab

from . import label_dev
from .dataset import load_eval_split

EXPERIMENT = "student-bakeoff"
SEED = 20261019
N_CHATS = 20
MAX_NEW_TOKENS = 3072
JOB_DIR = ROOT / "kaggle" / EXPERIMENT
STAGE = JOB_DIR / "upload"  # gitignored
DATASET = "JReyes33/orderslm-student-bakeoff"
TEACHER_RUN = RUNS / "label-dev" / "20261016T195121Z-openai__gpt-6-luna@low"  # teacher-label@0.7 on all dev

# Revisions pinned 2026-10-19 from the Hugging Face API; licenses in docs/PROVIDERS.md (all Apache 2.0).
CANDIDATES = [
    {
        "name": "qwen3.5-0.8b",
        "repo": "Qwen/Qwen3.5-0.8B",
        "revision": "2fc06364715b967f1860aea9cf38778875588b17",
        "loader": "multimodal",  # card: AutoProcessor + AutoModelForMultimodalLM; non-thinking by default
        "template_kwargs": {},
    },
    {
        "name": "qwen3.5-2b",
        "repo": "Qwen/Qwen3.5-2B",
        "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc",
        "loader": "multimodal",
        "template_kwargs": {},
    },
    {
        "name": "qwen3-1.7b",
        "repo": "Qwen/Qwen3-1.7B",
        "revision": "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e",
        "loader": "causal",  # card: AutoTokenizer + AutoModelForCausalLM
        "template_kwargs": {"enable_thinking": False},  # card: hard switch off
    },
    {
        "name": "gemma-4-e2b-it",
        "repo": "google/gemma-4-E2B-it",
        "revision": "3e22461f65e89153144f8adb70e3b8c2cc9845a7",
        "loader": "multimodal",  # card: AutoProcessor + AutoModelForMultimodalLM
        "template_kwargs": {"enable_thinking": False},
    },
]
# Decoding: greedy (reproducible) instead of the cards' sampling settings; fp32 (T4 has no bf16; fp16 can overflow
# on small models, docs/KAGGLE.md), spread over both T4s with device_map="auto".
GENERATION = {"do_sample": False, "max_new_tokens": MAX_NEW_TOKENS, "dtype": "float32"}


def select_ids() -> list[str]:
    ids = sorted(ac.conversation.id for ac in load_eval_split(Split.dev))
    return sorted(random.Random(SEED).sample(ids, N_CHATS))


def strip_fences(text: str) -> str:
    """The one normalization before parsing: drop a surrounding ```json … ``` fence (counted separately)."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def _json_ok(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


def _menu_item_ids(obj: Any, out: Counter) -> Counter:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "menu_item_id" and isinstance(v, str):
                out[v] += 1
            else:
                _menu_item_ids(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _menu_item_ids(v, out)
    return out


def diagnose(texts: dict[str, str], teacher_texts: dict[str, str]) -> dict[str, Any]:
    """Diagnostics, NOT contract scores: why labels fail the contract (field: error type, counted per error), and
    the menu_item_ids anywhere in the parsed JSON vs the teacher's (multiset), ignoring structure. Shows how close a
    zero-shot student is when every label is invalid."""
    errors: Counter = Counter()
    tp = fp = fn = 0
    for cid, text in texts.items():
        teacher = _menu_item_ids(json.loads(teacher_texts[cid]), Counter())
        try:
            obj = json.loads(text)
        except ValueError:
            errors["(not JSON)"] += 1
            fn += sum(teacher.values())
            continue
        try:
            TeacherLabel.model_validate(obj)
        except ValidationError as e:
            for x in e.errors():
                errors[".".join(str(p) for p in x["loc"] if not isinstance(p, int)) + ": " + x["type"]] += 1
        ids = _menu_item_ids(obj, Counter())
        tp += sum((ids & teacher).values())
        fp += sum((ids - teacher).values())
        fn += sum((teacher - ids).values())
    return {
        "contract_errors": dict(errors.most_common()),
        "item_ids_vs_teacher": {
            "right": tp,
            "extra": fp,
            "missed": fn,
            "f1": round(2 * tp / (2 * tp + fp + fn), 3) if tp + fp + fn else None,
        },
    }


def export(args: argparse.Namespace) -> Path:
    ids = select_ids()[: args.limit] if args.limit else select_ids()
    dev = {ac.conversation.id: ac for ac in load_eval_split(Split.dev)}
    requests = []
    for cid in ids:
        conv = dev[cid].conversation
        req = lab.build_request(conv, load_menu(conv.business_id))
        requests.append({"id": cid, "system": req.system, "user": req.messages[0].content})
    started = datetime.now(UTC)
    out_dir = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}{f'-limit{args.limit}' if args.limit else ''}"
    manifest = {
        "experiment": EXPERIMENT,
        "label_prompt_version": lab.LABEL_PROMPT_VERSION,
        "seed": SEED,
        "conversation_ids": ids,
        "candidates": CANDIDATES,
        "generation": GENERATION,
        "teacher_run": str(TEACHER_RUN.relative_to(ROOT)),
        "exported_at": started.isoformat(),
        "git_commit": git_commit(),
        "kaggle_dataset": DATASET,
        "cost_micros": 0,
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    (STAGE / "requests.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in requests))
    (STAGE / "models.json").write_text(
        json.dumps({"candidates": CANDIDATES, "generation": GENERATION}, indent=2)
    )
    (STAGE / "run.json").write_text(json.dumps({"run_dir": out_dir.name, "requests": len(requests)}) + "\n")
    (STAGE / "dataset-metadata.json").write_text(
        json.dumps({"title": "orderslm-student-bakeoff", "id": DATASET, "licenses": [{"name": "unknown"}]})
        + "\n"
    )
    print(f"Staged {len(requests)} requests × {len(CANDIDATES)} models in {STAGE.relative_to(ROOT)}/")
    print(f"Run dir: {out_dir.relative_to(ROOT)}/")
    return out_dir


def _write_model_dir(
    run_dir: Path, name: str, ids: list[str], records: dict[str, dict], prompt_version: str
) -> Path:
    d = run_dir / name
    (d / "outputs").mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(
        json.dumps(
            {
                "teacher": name,
                "label_prompt_version": prompt_version,
                "conversation_ids": ids,
                "actual_cost_micros": 0,
            },
            indent=2,
        )
        + "\n"
    )
    for cid in ids:
        (d / "outputs" / f"{cid}.json").write_text(json.dumps(records[cid], indent=1) + "\n")
    return d


def import_(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text())
    if env.get("run_dir") != run_dir.name:
        raise SystemExit(f"kernel output is for {env.get('run_dir')}, not {run_dir.name}")
    ids = manifest["conversation_ids"]
    by_model: dict[str, dict[str, dict]] = {}
    for line in (output_dir / "outputs.jsonl").read_text().splitlines():
        r = json.loads(line)
        by_model.setdefault(r["model"], {})[r["id"]] = r
    teacher: dict[str, dict] = {
        cid: json.loads((ROOT / manifest["teacher_run"] / "outputs" / f"{cid}.json").read_text())
        for cid in ids
    }
    teacher_texts = {cid: r["response"]["text"] for cid, r in teacher.items()}
    summary: dict[str, Any] = {}
    for cand in manifest["candidates"]:
        name = cand["name"]
        rows = by_model.get(name, {})
        records, raw_ok, fenced_ok, hit_limit, lat, out_tok, in_tok = {}, 0, 0, 0, [], 0, 0
        for cid in ids:
            r = rows.get(cid)
            if r is None or "error" in r:
                records[cid] = {"error": (r or {}).get("error", "no output")}
                continue
            text = strip_fences(r["text"])
            raw_ok += _json_ok(r["text"].strip())
            fenced_ok += _json_ok(text)
            hit_limit += r["finish_reason"] == "length"
            lat.append(r["latency_ms"])
            out_tok += r["output_tokens"]
            in_tok += r["input_tokens"]
            records[cid] = {
                "raw_text": r["text"],
                "response": {
                    "config_id": name,
                    "model": f"{cand['repo']}@{cand['revision'][:8]}",
                    "text": text,
                    "finish_reason": r["finish_reason"],
                    "usage": {"input_tokens": r["input_tokens"], "output_tokens": r["output_tokens"]},
                    "latency_ms": r["latency_ms"],
                    "cost_micros": 0,
                    "at": r["at"],
                },
            }
        m = label_dev.report(_write_model_dir(run_dir, name, ids, records, manifest["label_prompt_version"]))
        texts = {cid: v["response"]["text"] for cid, v in records.items() if "response" in v}
        summary[name] = {
            "outputs": sum("response" in v for v in records.values()),
            "run_errors": sum("error" in v for v in records.values()),
            "raw_json_valid": raw_ok,
            "json_valid_after_fence_strip": fenced_ok,
            "hit_token_limit": hit_limit,
            "latency_p50_ms": round(median(lat)) if lat else None,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "load": env.get("models", {}).get(name),
            **_headline(m),
            **diagnose(texts, teacher_texts),
        }
    tm = label_dev.report(
        _write_model_dir(run_dir, "teacher-gpt-6-luna@low", ids, teacher, manifest["label_prompt_version"])
    )
    summary["teacher-gpt-6-luna@low"] = {"note": "saved M4 dev outputs, same chats", **_headline(tm)}
    kernel = run_dir / "kernel"
    kernel.mkdir(exist_ok=True)
    for name in ("env.json", "outputs.jsonl", "run.log"):
        if (output_dir / name).exists():
            shutil.copy(output_dir / name, kernel / name)
    manifest.update(imported_at=datetime.now(UTC).isoformat(), kernel_env=env)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    _write_report(run_dir, manifest, summary)
    print((run_dir / "report.md").read_text())
    return summary


def _headline(m: dict[str, Any]) -> dict[str, Any]:
    o, i = m["order"], m["intent"]
    return {
        "contract_valid": o["json_valid"],
        "item_f1": o["item"]["f1"],
        "items_found": o["item"]["tp"],
        "items_extra": o["item"]["fp"],
        "items_missed": o["item"]["fn"],
        "exact_orders": o["exact_match"],
        "conversations": o["conversations"],
        "intent_primary_correct": i["primary_correct"],
        "intent_messages": i["customer_messages"],
    }


def _write_report(run_dir: Path, manifest: dict, summary: dict) -> None:
    n = len(manifest["conversation_ids"])
    L = [
        f"# Student bake-off, zero-shot ({manifest['label_prompt_version']}, {n} dev chats, seed {manifest['seed']})",
        "",
        "Dev numbers (model choice), not held out. Same request and scorer as the teacher's labels; fp32, greedy.",
        "",
        "| model | JSON (raw) | JSON (fence stripped) | contract valid | item F1 | items found/extra/missed |"
        " exact orders | intents right | hit token limit | run errors | latency p50 |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name, s in summary.items():
        raw = s.get("raw_json_valid", "–")
        fen = s.get("json_valid_after_fence_strip", "–")
        lim = s.get("hit_token_limit", "–")
        err = s.get("run_errors", "–")
        p50 = f"{s['latency_p50_ms'] / 1000:.1f} s" if s.get("latency_p50_ms") else "–"
        L.append(
            f"| {name} | {raw}/{n} | {fen}/{n} | {s['contract_valid']}/{n} | {s['item_f1']} |"
            f" {s['items_found']}/{s['items_extra']}/{s['items_missed']} | {s['exact_orders']}/{n} |"
            f" {s['intent_primary_correct']}/{s['intent_messages']} | {lim} | {err} | {p50} |"
        )
    L += [
        "",
        "Diagnostics (not contract scores): menu_item_ids anywhere in the parsed JSON vs the teacher's, ignoring"
        " structure; most frequent contract errors (field: type, per error).",
        "",
        "| model | item ids right/extra/missed | F1 vs teacher | top contract errors |",
        "|---|---|---|---|",
    ]
    for name, s in summary.items():
        if "item_ids_vs_teacher" not in s:
            continue
        d = s["item_ids_vs_teacher"]
        top = "; ".join(f"{k} ×{v}" for k, v in list(s["contract_errors"].items())[:3]) or "–"
        L.append(f"| {name} | {d['right']}/{d['extra']}/{d['missed']} | {d['f1']} | {top} |")
    L += [
        "",
        "Run errors (out of memory, load failure) score as invalid; the message is in `<model>/outputs/`.",
        "Per-model details: `<model>/report.md`. Raw outputs: `kernel/outputs.jsonl`.",
    ]
    (run_dir / "report.md").write_text("\n".join(L) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--limit", type=int, help="first N of the selected chats (smoke test)")
    i = sub.add_parser("import")
    i.add_argument("run_dir", type=Path)
    i.add_argument("--output", type=Path, default=JOB_DIR / "output")
    args = ap.parse_args(argv)
    if args.cmd == "export":
        export(args)
    else:
        import_(args.run_dir, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
