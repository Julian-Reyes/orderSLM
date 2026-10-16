"""The M4 label prompt scored on reviewed gold: every dev conversation labeled by the teacher with the synthetic-data
label prompt (intents + order, finalized in code), then scored against Julian's reviewed gold.

    make label-dev                 # estimate only
    make label-dev ARGS="--yes"    # run (record/replay cache: reruns cost $0)
    make label-dev ARGS="--report runs/label-dev/<id>"   # rebuild metrics + report from saved outputs

Orders are scored with the M3 scorer (eval/metrics.py). Intents are scored per customer message against
gold_routing: primary accuracy, exact label-set match (primary + secondary), and recall per gold label.
These are dev numbers: dev is for prompt tuning, so they are not held-out results.
"""

import argparse
import json
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from orderslm.core.finalize import FINALIZE_VERSION, finalize_order
from orderslm.llm.config import load_models
from orderslm.llm.factory import cache_mode_from_env, make_client
from orderslm.llm.types import ChatResponse, LLMError
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.common import LABEL_SCHEMA_VERSION
from orderslm.schema.conversation import Split
from orderslm.schema.label import TeacherLabel
from orderslm.synth import label as lab
from orderslm.synth.run import ASSUMED_LABEL_OUTPUT, OVER_LIMIT_MICROS, _estimate

from .dataset import load_eval_split
from .metrics import SCORER_VERSION, aggregate, score_conversation
from .stats import wilson

EXPERIMENT = "label-dev"


def _slug(config_id: str) -> str:
    return config_id.replace("/", "__")


def score_intents(gold: AnnotatedConversation, label: TeacherLabel | None) -> list[dict[str, Any]]:
    pred = {i.message_index: i for i in label.intents} if label else {}
    rows = []
    for r in gold.gold_routing:
        g = r.decision
        p = pred.get(r.message_index)
        gold_set = {g.primary.value} | ({g.secondary.value} if g.secondary else set())
        pred_set = ({p.primary.value} | ({p.secondary.value} if p.secondary else set())) if p else set()
        rows.append(
            {
                "conversation_id": gold.conversation.id,
                "message_index": r.message_index,
                "gold": g.primary.value,
                "gold_secondary": g.secondary.value if g.secondary else None,
                "pred": p.primary.value if p else None,
                "pred_secondary": p.secondary.value if p and p.secondary else None,
                "primary_ok": bool(p) and p.primary == g.primary,
                "set_ok": pred_set == gold_set,
            }
        )
    return rows


def _parse(
    text: str, ac: AnnotatedConversation, teacher: str
) -> tuple[TeacherLabel | None, Any, str | None, str | None]:
    """(label, finalized order or None, contract error, synthetic-pipeline drop reason)."""
    menu = load_menu(ac.conversation.business_id)
    try:
        label = TeacherLabel.model_validate(json.loads(text))
        order = finalize_order(label.order, menu, ac.conversation.language)
    except (ValueError, ValidationError) as e:
        return None, None, str(e)[:300], "invalid_contract"
    _, drop = lab.parse_label(text, ac.conversation, menu, teacher)
    return label, order, None, drop  # an empty order, not None: the scorer reads None as an invalid output


def report(out_dir: Path) -> dict[str, Any]:
    manifest = json.loads((out_dir / "manifest.json").read_text())
    teacher = manifest["teacher"]
    dev = {ac.conversation.id: ac for ac in load_eval_split(Split.dev)}
    scores, intents, drops = [], [], Counter()
    for cid in manifest["conversation_ids"]:
        ac = dev[cid]
        rec = json.loads((out_dir / "outputs" / f"{cid}.json").read_text())
        label = order = None
        if "response" in rec:
            label, order, _, drop = _parse(ChatResponse.model_validate(rec["response"]).text, ac, teacher)
            if drop:
                drops[drop.split(":")[0]] += 1
        else:
            drops["call_error"] += 1
        scores.append(score_conversation(ac, order, load_menu(ac.conversation.business_id)))
        intents += score_intents(ac, label)
    n = len(intents)
    primary_ok = sum(r["primary_ok"] for r in intents)
    set_ok = sum(r["set_ok"] for r in intents)
    per_label: dict[str, dict[str, int]] = defaultdict(lambda: {"gold": 0, "correct": 0, "predicted": 0})
    for r in intents:
        per_label[r["gold"]]["gold"] += 1
        per_label[r["gold"]]["correct"] += r["primary_ok"]
        if r["pred"]:
            per_label[r["pred"]]["predicted"] += 1
    confusions = Counter((r["gold"], r["pred"]) for r in intents if not r["primary_ok"])
    metrics = {
        "teacher": teacher,
        "label_prompt_version": manifest["label_prompt_version"],
        "scorer_version": SCORER_VERSION,
        "finalize_version": FINALIZE_VERSION,
        "order": aggregate(scores),
        "intent": {
            "customer_messages": n,
            "primary_correct": primary_ok,
            "primary_accuracy": round(primary_ok / n, 4),
            "primary_ci95": wilson(primary_ok, n),
            "label_set_correct": set_ok,
            "label_set_accuracy": round(set_ok / n, 4),
            "per_gold_label": {k: dict(v) for k, v in sorted(per_label.items())},
            "confusions": [{"gold": g, "pred": p, "count": c} for (g, p), c in confusions.most_common()],
        },
        "synthetic_pipeline_drops": dict(drops),
        "cost_micros": manifest.get("actual_cost_micros"),
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (out_dir / "intent_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in intents))
    o = metrics["order"]
    lines = [
        f"# Label prompt on dev: `{metrics['label_prompt_version']}`, {teacher}",
        "",
        "Dev numbers (prompt tuning), not held-out results. Built from the saved outputs in this folder.",
        "",
        "## Orders (M3 scorer, after finalize)",
        "",
        f"- Conversations: {o['conversations']} ({o['conversations_with_order']} with a gold order)",
        f"- Valid label (contract): {o['json_valid']}/{o['conversations']}",
        f"- Items: {o['item']['tp']} found / {o['item']['fp']} extra / {o['item']['fn']} missed of"
        f" {o['item']['gold_items']} (F1 {o['item']['f1']})",
        f"- Fully correct orders: {o['exact_match']}/{o['conversations']} (95% CI {o['exact_match_ci95']})",
        f"- Field accuracy: {o['field_accuracy']}",
        f"- Labels the synthetic pipeline would drop: {dict(drops) or 'none'}",
        "",
        "## Intents (per customer message, against reviewed gold)",
        "",
        f"- Primary label correct: {primary_ok}/{n} ({100 * primary_ok / n:.1f}%, 95% CI"
        f" {metrics['intent']['primary_ci95']})",
        f"- Primary + secondary exactly right: {set_ok}/{n} ({100 * set_ok / n:.1f}%)",
        "",
        "| gold label | messages | primary correct | predicted as this |",
        "|---|---|---|---|",
    ]
    for k, v in sorted(per_label.items(), key=lambda kv: -kv[1]["gold"]):
        lines.append(f"| {k} | {v['gold']} | {v['correct']} | {v['predicted']} |")
    lines += ["", "Mistakes (gold → predicted):", ""]
    lines += [f"- {g} → {p}: {c}" for (g, p), c in confusions.most_common()]
    lines += ["", f"Cost: ${(manifest.get('actual_cost_micros') or 0) / 1e6:.4f}"]
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")
    return metrics


def run(args: argparse.Namespace) -> int:
    models = load_models()
    teacher = args.teacher
    dev = sorted(load_eval_split(Split.dev), key=lambda ac: ac.conversation.id)
    reqs = {
        ac.conversation.id: lab.build_request(ac.conversation, load_menu(ac.conversation.business_id))
        for ac in dev
    }
    est = sum(_estimate(models[teacher], r, ASSUMED_LABEL_OUTPUT) for r in reqs.values())
    print(
        f"Label all {len(dev)} dev chats with {teacher}, prompt {lab.LABEL_PROMPT_VERSION}: ≈ ${est / 1e6:.4f}"
    )
    if not args.yes:
        print("Estimate only. Re-run with --yes.")
        return 0
    if est > OVER_LIMIT_MICROS:
        print("Estimate is over $2: ask Julian first.")
        return 2
    started = datetime.now(UTC)
    out_dir = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}-{_slug(teacher)}"
    cache_mode = cache_mode_from_env()
    manifest: dict[str, Any] = {
        "experiment": EXPERIMENT,
        "started_at": started.isoformat(),
        "git_commit": git_commit(),
        "teacher": teacher,
        "extra_body": models[teacher].extra_body,
        "price_verified": models[teacher].price_verified,
        "label_prompt_version": lab.LABEL_PROMPT_VERSION,
        "label_schema_version": LABEL_SCHEMA_VERSION,
        "finalize_version": FINALIZE_VERSION,
        "data": {"split": "dev", "source": "A (claude_written)", "selection": "all dev, sorted by id"},
        "conversation_ids": [ac.conversation.id for ac in dev],
        "cache_mode": cache_mode,
        "estimate_micros": est,
    }
    (out_dir / "outputs").mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    spent = [0]
    lock = threading.Lock()
    max_cost = min(2 * est, OVER_LIMIT_MICROS)

    def one(cid: str) -> None:
        if spent[0] > max_cost:
            return
        rec: dict[str, Any] = {"conversation_id": cid, "config_id": teacher}
        try:
            resp = make_client(teacher, cache_mode=cache_mode).complete(reqs[cid])
            rec["response"] = resp.model_dump(mode="json")
            cost = 0 if resp.cached else resp.cost_micros
        except LLMError as e:
            rec["error"] = str(e)
            cost = 0
        (out_dir / "outputs" / f"{cid}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
        with lock:
            spent[0] += cost
            print(
                f"  {cid:12} {'error' if 'error' in rec else rec['response']['finish_reason']:8} ${spent[0] / 1e6:.4f}"
            )

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(one, reqs))
    manifest.update(finished_at=datetime.now(UTC).isoformat(), actual_cost_micros=spent[0])
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    report(out_dir)
    print((out_dir / "report.md").read_text())
    print(f"Saved {out_dir.relative_to(ROOT)}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--teacher", default=lab.TEACHER)
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args(argv)
    if args.report:
        report(args.report)
        print((args.report / "report.md").read_text())
        return 0
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
