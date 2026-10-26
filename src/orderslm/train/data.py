"""M6 training data: the teacher's kept labels (M4) → chat rows for LoRA (spec §10). Free, local.

One row per labeled synthetic chat (Julian, 2026-10-20: full chats only; rows cut at earlier customer messages are
not added unless the student struggles mid-chat). A row is the student prompt (`student-extract@0.N`: short
instructions, menu, chat) and the target `StudentOutput`: the intent of the last customer message + the teacher's
`ModelOrder`, taken from the teacher's raw answer (the label code checked it; code still computes the missing list
and question at run time, `core/finalize`).

Two training sets (spec §10–11e): `single` = the per-restaurant batches; `mixed` = the same + the food-court batch
m1. v0.1: p3 + b1 (+ m1). v0.2 (M6 error review, Julian 2026-10-25): + the targeted batch t3 and the hand-written
top-up t4. Validation chats are drawn 5% per group (VERSIONS[...]["valid_groups"]), so v0.2 keeps exactly v0.1's
validation chats and adds 5% of t3 + t4; the same chats are in both sets, plus 5% of m1 in `mixed`. Chats listed in
runs/synth/excluded.json (label audit) are left out; hand-fixed labels (synth label_fixes) are used, and counted
per set. Only synthetic chats: never dev, test or PIZZA.

    make student-data                                   # → runs/student-data/<DATA_VERSION>/... + manifest
    make student-data ARGS="--version student-data@0.1" # rebuild an earlier version (byte-identical)

`train.jsonl` / `valid.jsonl` hold `{"messages": [system, user, assistant]}` only (the format Unsloth/TRL and
MLX-LM read); `rows.jsonl` has the same rows' ids, batch, generator, menu and sizes. The jsonl files are gitignored
(rebuilt from the committed labels; their sha256 is in the manifest).
"""

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from datetime import UTC, datetime
from importlib.resources import files
from pathlib import Path
from typing import Any

from orderslm.extractors.teacher import conversation_prompt
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.label import StudentIntent, StudentOutput, TeacherLabel
from orderslm.schema.routing import RouterLabel
from orderslm.synth import label as lab
from orderslm.synth import run as synth

VERSIONS = {
    "student-data@0.1": {
        "single": ("p3", "b1"),
        "mixed": ("p3", "b1", "m1"),
        "valid_groups": (("p3", "b1"), ("m1",)),
    },
    "student-data@0.2": {
        "single": ("p3", "b1", "t3", "t4"),
        "mixed": ("p3", "b1", "m1", "t3", "t4"),
        "valid_groups": (("p3", "b1"), ("m1",), ("t3", "t4")),
    },
}
DATA_VERSION = "student-data@0.2"
STUDENT_PROMPT_VERSION = "student-extract@0.1"
SINGLE_BATCHES = VERSIONS[DATA_VERSION]["single"]
MIXED_BATCHES = VERSIONS[DATA_VERSION]["mixed"]
VALID_SHARE = 0.05
SEED = 20261020
OUT = RUNS / "student-data"
USER_SUFFIX = "\n\nReturn the intent of the latest customer message and the order so far as one JSON object."


def system_prompt(version: str = STUDENT_PROMPT_VERSION) -> str:
    text = (files("orderslm.extractors") / "prompts" / f"{version}.md").read_text()
    return text.replace("{label_codes}", ", ".join(f"`{x.value}`" for x in RouterLabel))


def user_prompt(conversation, menu) -> str:
    return conversation_prompt(menu.extractor_view(), conversation) + USER_SUFFIX


def target(label: TeacherLabel) -> StudentOutput:
    last = label.intents[-1]
    return StudentOutput(
        intent=StudentIntent(primary=last.primary, secondary=last.secondary), order=label.order
    )


def _excluded() -> set[str]:
    path = RUNS / "synth" / "excluded.json"
    return {e["id"] for e in json.loads(path.read_text())["excluded"]} if path.exists() else set()


def build_rows(batch: str) -> tuple[list[dict[str, Any]], Counter]:
    """Rows for one batch's kept labels (labels.jsonl), skipping excluded chats."""
    kept = {
        json.loads(x)["conversation_id"]
        for x in (synth.batch_dir(batch) / "labels.jsonl").read_text().splitlines()
    }
    excluded = _excluded()
    system = system_prompt()
    rows, skipped = [], Counter()
    for s in synth.load_conversations(batch):
        conv = s.conversation
        if conv.id not in kept:
            continue
        if conv.id in excluded:
            skipped["excluded"] += 1
            continue
        text, label_version, fix = synth.label_record(batch, s.card_id, lab.TEACHER)  # a hand fix, if any
        label = TeacherLabel.model_validate_json(text)
        if label.intents[-1].message_index != conv.customer_indices()[-1]:
            raise SystemExit(f"{conv.id}: last intent is not the last customer message")
        menu = load_menu(conv.business_id)
        user = user_prompt(conv, menu)
        answer = target(label).model_dump_json()
        rows.append(
            {
                "id": conv.id,
                "batch": batch,
                "generator": s.generator,
                "business_id": conv.business_id,
                "label_prompt_version": label_version,
                "label_hand_fixed": fix is not None,
                "intent": label.intents[-1].primary.value,
                "items": len(label.order.items),
                "chars": {"system": len(system), "user": len(user), "assistant": len(answer)},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": answer},
                ],
            }
        )
    return rows, skipped


def split_valid(ids: list[str], seed: int = SEED) -> set[str]:
    ids = sorted(ids)
    return set(random.Random(seed).sample(ids, round(len(ids) * VALID_SHARE)))


def _write(path: Path, rows: list[dict[str, Any]]) -> str:
    text = "".join(json.dumps({"messages": r["messages"]}, ensure_ascii=False) + "\n" for r in rows)
    path.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()


def _stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    def q(xs: list[int], p: float) -> int:
        xs = sorted(xs)
        return xs[min(len(xs) - 1, int(p * len(xs)))]

    total = [sum(r["chars"].values()) for r in rows]
    answer = [r["chars"]["assistant"] for r in rows]
    return {
        "rows": len(rows),
        "per_batch": dict(Counter(r["batch"] for r in rows)),
        "per_generator": dict(Counter(r["generator"] for r in rows)),
        "per_business": dict(Counter(r["business_id"] for r in rows)),
        "latest_intent": dict(Counter(r["intent"] for r in rows).most_common()),
        "rows_with_items": sum(r["items"] > 0 for r in rows),
        "label_hand_fixed": sum(r["label_hand_fixed"] for r in rows),
        "chars_total": {"p50": q(total, 0.5), "p95": q(total, 0.95), "max": max(total)},
        "chars_answer": {"p50": q(answer, 0.5), "p95": q(answer, 0.95), "max": max(answer)},
    }


def build(out_dir: Path, version: str = DATA_VERSION) -> dict[str, Any]:
    spec = VERSIONS[version]
    by_batch = {b: build_rows(b) for b in spec["mixed"]}
    valid = set().union(
        *(split_valid([r["id"] for b in group for r in by_batch[b][0]]) for group in spec["valid_groups"])
    )
    manifest: dict[str, Any] = {
        "data_version": version,
        "student_prompt_version": STUDENT_PROMPT_VERSION,
        "student_schema": StudentOutput.model_fields["schema_version"].default,
        "teacher": lab.TEACHER,
        "seed": SEED,
        "valid_share": VALID_SHARE,
        "built_at": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "skipped": {b: dict(by_batch[b][1]) for b in spec["mixed"]},
        "sets": {},
    }
    for name in ("single", "mixed"):
        batches = spec[name]
        rows = [r for b in batches for r in by_batch[b][0]]
        d = out_dir / name
        d.mkdir(parents=True, exist_ok=True)
        train = [r for r in rows if r["id"] not in valid]
        val = [r for r in rows if r["id"] in valid]
        manifest["sets"][name] = {
            "batches": list(batches),
            "train": {**_stats(train), "sha256": _write(d / "train.jsonl", train)},
            "valid": {**_stats(val), "sha256": _write(d / "valid.jsonl", val)},
            "valid_ids": sorted(r["id"] for r in val),
        }
        (d / "rows.jsonl").write_text(
            "".join(json.dumps({k: v for k, v in r.items() if k != "messages"}) + "\n" for r in rows)
        )
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", choices=sorted(VERSIONS), default=DATA_VERSION)
    ap.add_argument("--out", type=Path, help="default: runs/student-data/<version>")
    args = ap.parse_args(argv)
    args.out = args.out or OUT / args.version
    m = build(args.out, args.version)
    for name, s in m["sets"].items():
        t, v = s["train"], s["valid"]
        print(
            f"{name}: train {t['rows']} / valid {v['rows']} rows; chars per row p50 {t['chars_total']['p50']}, "
            f"max {t['chars_total']['max']}; answer p50 {t['chars_answer']['p50']}, max {t['chars_answer']['max']}"
        )
    print(f"skipped: {m['skipped']}")
    print(f"Saved {args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
