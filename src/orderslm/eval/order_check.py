"""Order checker pilot (spec §11b, whole-order version): the teacher LLM asked whether the student's final order
matches the chat, on the orders the picked student got wrong (Julian, 2026-11-03: "test on the ones missed only").

The student is `qwen3.5-0.8b-single-v2`; its saved final orders (finalized in code) are rebuilt from the student-dev
runs, and every chat whose order is not the same action as gold (scorer@0.3) is checked: real mistakes, not
wording-level ones. The checker sees the chat and the order in plain text and gets the label audit's order question
(`label_audit.ORDER_PROMPT`, the wording Jev and OpenAI Decisions answer), so the providers stay comparable.

Every order here is wrong, so this measures the catch rate only: there is no false-alarm rate (a checker that always
says "no" would score 100%). Dev results may tune the checker; fresh results only measure it.

    make order-check                                   # estimate only
    make order-check ARGS="--yes"                      # run (record/replay cache: reruns cost $0)
    make order-check ARGS="--report runs/order-check/<id>"   # rebuild metrics + report from saved outputs
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

from orderslm.llm.config import load_models
from orderslm.llm.factory import cache_mode_from_env, make_client
from orderslm.llm.types import ChatMessage, ChatRequest, LLMError
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Split
from orderslm.synth.label import TEACHER
from orderslm.synth.run import OVER_LIMIT_MICROS, _estimate

from .dataset import load_eval_split
from .label_audit import ORDER_PROMPT, chat_text, order_text
from .stats import wilson
from .student_bakeoff import strip_fences
from .student_errors import chat_errors, student_predictions

EXPERIMENT = "order-check"
CHECK_VERSION = "order-check@0.1"
STUDENT = "qwen3.5-0.8b-single-v2"
STUDENT_RUNS = {
    Split.dev: RUNS / "student-dev" / "20261026T131201Z-qwen3.5-0.8b-single-v2",
    Split.fresh: RUNS / "student-dev" / "20261026T131201Z-qwen3.5-0.8b-single-v2-fresh",
}
ASSUMED_OUTPUT = 600  # verdict JSON + luna `low` reasoning
SYSTEM = (
    "You check the work of a restaurant's chat bot. You get a text chat between a customer and the restaurant, and "
    "the order the bot recorded from it. Answer the question about the record. Reply with JSON only: "
    '{"matches": true or false, "problem": "what is wrong, in one sentence, or an empty string if it matches"}.'
)
SCHEMA = {
    "type": "object",
    "properties": {"matches": {"type": "boolean"}, "problem": {"type": "string"}},
    "required": ["matches", "problem"],
    "additionalProperties": False,
}


def error_kinds(errors: dict[str, Any]) -> list[str]:
    """What is wrong with the order, in the student_errors vocabulary (one entry per wrong line or field)."""
    if "invalid" in errors:
        return ["broken_answer"]
    return [i["kind"] for i in errors["items"]] + [f"field:{k}" for k in errors["fields"]]


def wrong_orders() -> list[dict[str, Any]]:
    """The student's real order mistakes on dev + fresh: chats whose order is not the same action as gold."""
    jobs = []
    for split, run_dir in STUDENT_RUNS.items():
        acs = {ac.conversation.id: ac for ac in load_eval_split(split)}
        _, orders, _ = student_predictions(run_dir, acs)
        rows = [json.loads(x) for x in (run_dir / "order_rows.jsonl").read_text().splitlines() if x.strip()]
        for r in sorted(rows, key=lambda r: r["conversation_id"]):
            if r["action_exact"]:
                continue
            cid = r["conversation_id"]
            ac, (order, invalid) = acs[cid], orders[cid]
            menu = load_menu(ac.conversation.business_id)
            errors = chat_errors(ac, order, invalid) or {"items": [], "fields": {}}
            jobs.append(
                {
                    "id": f"{split.value}__{cid}",
                    "split": split.value,
                    "conversation_id": cid,
                    "kinds": error_kinds(errors),
                    "errors": errors,
                    "order_text": order_text(order, menu),
                    "request": build_request(ac.conversation, order_text(order, menu), menu.name),
                }
            )
    return jobs


def build_request(conversation, recorded: str, business: str) -> ChatRequest:
    text = (
        f"A text chat between a customer and {business}:\n{chat_text(conversation)}\n\n"
        f"The order as recorded after the last message:\n{recorded}\n\n{ORDER_PROMPT}"
    )
    return ChatRequest(
        system=SYSTEM,
        messages=[ChatMessage(role="user", content=text)],
        json_schema=SCHEMA,
        schema_name="order_check",
        max_output_tokens=4096,
    )


def parse(text: str) -> dict[str, Any] | None:
    try:
        v = json.loads(strip_fences(text))
    except ValueError:
        return None
    if not isinstance(v, dict) or not isinstance(v.get("matches"), bool):
        return None
    return {"matches": v["matches"], "problem": str(v.get("problem") or "")}


def report(out_dir: Path) -> dict[str, Any]:
    manifest = json.loads((out_dir / "manifest.json").read_text())
    rows = []
    for f in sorted((out_dir / "outputs").glob("*.json")):
        rec = json.loads(f.read_text())
        verdict = parse(rec["response"]["text"]) if "response" in rec else None
        rows.append(
            {
                "id": rec["id"],
                "split": rec["split"],
                "kinds": rec["kinds"],
                "verdict": verdict,
                "caught": verdict is not None and not verdict["matches"],
                "error": rec.get("error"),
            }
        )

    def rate(rs: list[dict]) -> dict[str, Any]:
        n, k = len(rs), sum(r["caught"] for r in rs)
        return {"orders": n, "caught": k, "rate": round(k / n, 4) if n else None, "ci95": wilson(k, n)}

    by_kind: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        for k in set(r["kinds"]):
            by_kind[k].append(r)
    metrics = {
        "check_version": CHECK_VERSION,
        "checker": manifest["checker"],
        "student": STUDENT,
        "all": rate(rows),
        "per_split": {s: rate([r for r in rows if r["split"] == s]) for s in ("dev", "fresh")},
        "broken_answers": rate([r for r in rows if r["kinds"] == ["broken_answer"]]),
        "readable_orders": rate([r for r in rows if r["kinds"] != ["broken_answer"]]),
        "per_kind": {k: rate(v) for k, v in sorted(by_kind.items())},
        "no_verdict": sum(r["verdict"] is None for r in rows),
        "cost_micros": manifest.get("actual_cost_micros"),
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")

    def pct(x: dict) -> str:
        if not x["orders"]:
            return "n/a"
        lo, hi = x["ci95"]
        return f"{x['caught']}/{x['orders']} ({100 * x['rate']:.0f}%, 95% CI {100 * lo:.0f}–{100 * hi:.0f}%)"

    lines = [
        f"# Order checker pilot: `{manifest['checker']}` on the student's wrong orders",
        "",
        f"`{CHECK_VERSION}`, whole-order check (spec §11b). Student `{STUDENT}`; its final orders on dev and fresh "
        "that are not the same action as gold (scorer@0.3). **Every order here is wrong, so only the catch rate is "
        "measured, not false alarms.** Dev may tune the checker; fresh only measures it.",
        "",
        "| set | wrong orders caught |",
        "|---|---|",
        f"| all | {pct(metrics['all'])} |",
        f"| dev | {pct(metrics['per_split']['dev'])} |",
        f"| fresh | {pct(metrics['per_split']['fresh'])} |",
        f"| readable orders (the student's answer was valid) | {pct(metrics['readable_orders'])} |",
        f"| broken answers (shown as 'no new order') | {pct(metrics['broken_answers'])} |",
        "",
        "| what is wrong (a chat counts once per kind) | caught |",
        "|---|---|",
    ]
    lines += [
        f"| {k} | {pct(v)} |" for k, v in sorted(metrics["per_kind"].items(), key=lambda kv: -kv[1]["orders"])
    ]
    lines += ["", "| chat | what is wrong | caught | checker's reason |", "|---|---|---|---|"]
    for r in rows:
        why = (
            (r["verdict"] or {}).get("problem")
            or r["error"]
            or ("no verdict" if r["verdict"] is None else "")
        )
        lines.append(
            f"| {r['id'].replace('__', ' ')} | {', '.join(r['kinds'])} | {'yes' if r['caught'] else '**no**'} | "
            f"{why.replace('|', '/')} |"
        )
    lines += ["", f"No verdict: {metrics['no_verdict']}. Cost: ${(metrics['cost_micros'] or 0) / 1e6:.4f}."]
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")
    return metrics


def run(args: argparse.Namespace) -> int:
    models = load_models()
    checker = args.checker
    jobs = wrong_orders()
    est = sum(_estimate(models[checker], j["request"], ASSUMED_OUTPUT) for j in jobs)
    print(f"Check {len(jobs)} wrong orders of {STUDENT} with {checker}, {CHECK_VERSION}: ≈ ${est / 1e6:.4f}")
    print("  " + ", ".join(f"{s}: {n}" for s, n in Counter(j["split"] for j in jobs).items()))
    if not args.yes:
        print("Estimate only. Re-run with --yes.")
        return 0
    if est > OVER_LIMIT_MICROS:
        print("Estimate is over $2: ask Julian first.")
        return 2
    started = datetime.now(UTC)
    out_dir = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}-{checker.replace('/', '__')}"
    cache_mode = cache_mode_from_env()
    manifest: dict[str, Any] = {
        "experiment": EXPERIMENT,
        "check_version": CHECK_VERSION,
        "started_at": started.isoformat(),
        "git_commit": git_commit(),
        "checker": checker,
        "extra_body": models[checker].extra_body,
        "price_verified": models[checker].price_verified,
        "student": STUDENT,
        "student_runs": {s.value: str(p.relative_to(ROOT)) for s, p in STUDENT_RUNS.items()},
        "data": {
            "splits": ["dev", "fresh"],
            "source": "A (claude_written)",
            "selection": "student orders not the same action as gold (scorer@0.3); wrong orders only",
        },
        "ids": [j["id"] for j in jobs],
        "cache_mode": cache_mode,
        "estimate_micros": est,
    }
    (out_dir / "outputs").mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    spent = [0]
    lock = threading.Lock()
    max_cost = min(2 * est, OVER_LIMIT_MICROS)

    def one(job: dict[str, Any]) -> None:
        if spent[0] > max_cost:
            return
        rec = {k: job[k] for k in ("id", "split", "conversation_id", "kinds", "errors", "order_text")}
        rec["config_id"] = checker
        try:
            resp = make_client(checker, cache_mode=cache_mode).complete(job["request"])
            rec["response"] = resp.model_dump(mode="json")
            cost = 0 if resp.cached else resp.cost_micros
        except LLMError as e:
            rec["error"] = str(e)
            cost = 0
        (out_dir / "outputs" / f"{job['id']}.json").write_text(
            json.dumps(rec, indent=1, ensure_ascii=False) + "\n"
        )
        with lock:
            spent[0] += cost
            print(f"  {job['id']:22} {'error' if 'error' in rec else 'ok':6} ${spent[0] / 1e6:.4f}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(one, jobs))
    manifest.update(finished_at=datetime.now(UTC).isoformat(), actual_cost_micros=spent[0])
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    report(out_dir)
    print((out_dir / "report.md").read_text())
    print(f"Saved {out_dir.relative_to(ROOT)}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checker", default=TEACHER)
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
