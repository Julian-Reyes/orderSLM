"""Julia-1 tuning on dev: one change at a time from the label-audit baseline (docs/KAGGLE.md job A).

Dev is tuning data, so these numbers are not held out. Every variant is the baseline request with ONE change, run
in the same Kaggle job so they compare directly:

- `julia-1`            baseline: the exact label-audit requests (same as Jev / OpenAI Decisions)
- `julia-1-short`      intents: the state is only the business message before (if any) + the customer message
- `julia-1-shuf<k>`    intents: the 15 options in a seeded random order k (position bias)
- `julia-1-shuf-avg`   intents: probabilities averaged over the shuffled orders
- `julia-1-yesno`      order check: the yes/no answers get descriptions (Julia-1 / Jev only; Decisions has no field)

Answers a variant doesn't change come from the baseline, so each variant has a full row in the usual report.

    make julia-variants ARGS="export"
    make kaggle-push JOB=julia-audit   (then make kaggle-pull JOB=julia-audit)
    make julia-variants ARGS="import runs/label-audit/<id>"
"""

import argparse
import json
import random
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.core.plant import PLANT_VERSION
from orderslm.menus import load_menu
from orderslm.paths import RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Role, Split

from . import julia_audit as ja
from . import label_audit
from .dataset import load_eval_split

VARIANTS_VERSION = "julia-variants@0.1"
SHUFFLES = 3
SHORT_PROMPT = "What does the customer's last message do?"
YES_NO_CRITERIA = {
    "false": "The record differs from the chat in at least one item, quantity, size, option, pickup or delivery, "
    "payment or status.",
    "true": "The record matches the chat in every item, quantity, size, option, pickup or delivery, payment and status.",
}
VARIANTS = [
    "julia-1",
    "julia-1-short",
    *[f"julia-1-shuf{k}" for k in range(SHUFFLES)],
    "julia-1-shuf-avg",
    "julia-1-yesno",
]


def short_state(conversation, i: int, business_name: str) -> str:
    msgs = conversation.messages
    lines = [f"A text chat between a customer and {business_name}:"]
    if i > 0 and msgs[i - 1].role is Role.business:
        lines.append(f"business: {msgs[i - 1].text}")
    lines.append(f"customer: {msgs[i].text}")
    return "\n".join(lines)


def shuffled(criteria: dict[str, str], seed: str) -> dict[str, str]:
    keys = list(criteria)
    random.Random(seed).shuffle(keys)
    return {k: criteria[k] for k in keys}


def build(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Julia requests for every variant; ids are `<variant>|<job id>[|m<i>]`."""
    convs = {ac.conversation.id: ac.conversation for ac in load_eval_split(Split.dev)}
    out = []
    for j in jobs:
        base = ja.to_julia(j["request"])
        out.append({**base, "id": f"base|{j['id']}"})
        order = {"order_ok": {**base["questions"]["order_ok"], "criteria": YES_NO_CRITERIA}}
        out.append({"id": f"yesno|{j['id']}", "state": base["state"], "questions": order})
        intents = {n: q for n, q in base["questions"].items() if n.startswith("intent_m")}
        if not intents:
            continue
        conv = convs[j["id"]]
        name = load_menu(conv.business_id).name
        for n, q in intents.items():
            i = int(n.removeprefix("intent_m"))
            short = {n: {**q, "instructions": SHORT_PROMPT}}
            out.append(
                {"id": f"short|{j['id']}|m{i}", "state": short_state(conv, i, name), "questions": short}
            )
        for k in range(SHUFFLES):
            qs = {
                n: {**q, "criteria": shuffled(q["criteria"], f"{j['id']}|{n}|{k}")}
                for n, q in intents.items()
            }
            out.append({"id": f"shuf{k}|{j['id']}", "state": base["state"], "questions": qs})
    return out


def merge(job_id: str, outputs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Kernel output lines → one Julia-style record per variant (baseline answers where a variant changes none)."""
    related = {k: v for k, v in outputs.items() if k.split("|")[1] == job_id}
    errors = [v["error"] for v in related.values() if "error" in v]
    if errors:
        return {v: {"error": errors[0]} for v in VARIANTS}
    base = related[f"base|{job_id}"]

    def rec(answers: dict[str, Any], *keys: str) -> dict[str, Any]:
        parts = [base] + [related[k] for k in keys]
        return {
            "answers": answers,
            "latency_ms": sum(p["latency_ms"] for p in parts),
            "input_tokens": sum(p.get("input_tokens", 0) for p in parts),
        }

    out = {"julia-1": rec(dict(base["answers"]))}
    out["julia-1-yesno"] = rec(
        {**base["answers"], **related[f"yesno|{job_id}"]["answers"]}, f"yesno|{job_id}"
    )
    short_keys = sorted(k for k in related if k.startswith("short|"))
    shuf_keys = [f"shuf{k}|{job_id}" for k in range(SHUFFLES)]
    if not short_keys:
        for v in VARIANTS:
            out.setdefault(v, out["julia-1"])
        return out
    short = {n: a for k in short_keys for n, a in related[k]["answers"].items()}
    out["julia-1-short"] = rec({**base["answers"], **short}, *short_keys)
    for k, key in enumerate(shuf_keys):
        out[f"julia-1-shuf{k}"] = rec({**base["answers"], **related[key]["answers"]}, key)
    avg = {}
    for n in related[shuf_keys[0]]["answers"]:
        probs: dict[str, float] = {}
        for key in shuf_keys:
            for label, p in related[key]["answers"][n]["probabilities"].items():
                probs[label] = probs.get(label, 0.0) + p / SHUFFLES
        avg[n] = {"type": "choice", "choice": max(probs, key=probs.__getitem__), "probabilities": probs}
    out["julia-1-shuf-avg"] = rec({**base["answers"], **avg}, *shuf_keys)
    return out


def export(args: argparse.Namespace) -> Path:
    jobs = label_audit.dev_jobs()
    started = datetime.now(UTC)
    out_dir = RUNS / label_audit.EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}-julia-variants-dev"
    manifest = {
        "experiment": label_audit.EXPERIMENT,
        "audit_version": label_audit.AUDIT_VERSION,
        "variants_version": VARIANTS_VERSION,
        "plant_version": PLANT_VERSION,
        "set": "dev",
        "batches": None,
        "providers": VARIANTS,
        "provider_config": {
            "model": ja.MODEL,
            "revision": ja.REVISION,
            "runtime": "Kaggle script kernel, CPU (kaggle/julia-audit/run.py)",
            "short_prompt": SHORT_PROMPT,
            "shuffles": SHUFFLES,
            "yes_no_criteria": YES_NO_CRITERIA,
        },
        "exported_at": started.isoformat(),
        "git_commit": git_commit(),
        "job_ids": [j["id"] for j in jobs],
        "kaggle_dataset": ja.DATASET,
        "cost_micros": 0,
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    ja.stage(out_dir, build(jobs))
    return out_dir


def import_(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text())
    if env.get("run_dir") != run_dir.name:
        raise SystemExit(f"kernel output is for {env.get('run_dir')}, not {run_dir.name}")
    outputs = {}
    for line in (output_dir / "outputs.jsonl").read_text().splitlines():
        rec = json.loads(line)
        outputs[rec["id"]] = rec
    requests = {j["id"]: j["request"] for j in label_audit.dev_jobs() if j["id"] in set(manifest["job_ids"])}
    for jid, req in requests.items():
        for variant, rec in merge(jid, outputs).items():
            path = run_dir / "responses" / variant / f"{jid}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            out: dict[str, Any] = {"id": jid}
            if "error" in rec:
                out["error"] = rec["error"]
            else:
                resp = ja.from_julia(req, rec).model_copy(update={"provider": variant})
                out["response"] = resp.model_dump(mode="json")
            path.write_text(json.dumps(out, indent=1) + "\n")
    kernel = run_dir / "kernel"
    kernel.mkdir(exist_ok=True)
    for name in ("env.json", "outputs.jsonl", "run.log"):
        if (output_dir / name).exists():
            (kernel / name).write_bytes((output_dir / name).read_bytes())
    manifest.update(imported_at=datetime.now(UTC).isoformat(), kernel_env=env)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    metrics = label_audit.report(run_dir)
    print((run_dir / "report.md").read_text())
    print(f"Saved {run_dir}/")
    return metrics


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("export")
    i = sub.add_parser("import")
    i.add_argument("run_dir", type=Path)
    i.add_argument("--output", type=Path, default=ja.JOB_DIR / "output")
    args = ap.parse_args(argv)
    if args.cmd == "export":
        export(args)
    else:
        import_(args.run_dir, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
