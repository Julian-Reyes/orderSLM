"""Order checker (spec §11b, whole-order version): does the picked student's final order match the chat?

The student is `qwen3.5-0.8b-single-v2`; its saved final orders (finalized in code) are rebuilt from the student-dev
runs. Checked: every dev and fresh chat whose order is not the same action as gold (scorer@0.3), the real mistakes,
plus a seeded sample of orders it got right (the same number per split), so each checker gets a catch rate and a
false-alarm rate. Every checker sees the identical text (the chat, the menu, the order) and question:

- `luna`: the teacher LLM (`synth.label.TEACHER`), JSON `{matches, problem}`;
- `jev`, `openai-decisions`: the decision providers, one boolean question (`order_ok`).

order-check@0.1 (pilot, 2026-11-03, `runs/order-check/20261103T225157Z-…`, its report is frozen): Luna only, wrong
orders only, no menu, the label audit's order text and question. 0.2: the menu, the order text in `detail` mode
(cash change, ids that aren't on the menu or the item, a size never chosen) and two rules: menu defaults count, and
a vague amount or size must not become a number or a size. The rules came from the pilot's misses on dev and fresh,
so fresh is no longer unseen for this checker: its fresh numbers are "seen while fixing", not held out.

    make order-check                                   # estimate only
    make order-check ARGS="--yes"                      # run (record/replay cache: reruns cost $0)
    make order-check ARGS="--report runs/order-check/<id>"   # rebuild metrics + report from saved outputs
"""

import argparse
import json
import random
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.interfaces.decision import (
    DecisionError,
    DecisionRequest,
    DecisionResponse,
    Question,
    QuestionType,
)
from orderslm.llm.config import load_models
from orderslm.llm.factory import cache_mode_from_env, make_client
from orderslm.llm.types import ChatMessage, ChatRequest, LLMError
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.providers.hosted import load_hosted, make_provider
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Conversation, Split
from orderslm.schema.menu import MenuCatalog, SoldAs
from orderslm.synth.label import TEACHER
from orderslm.synth.run import OVER_LIMIT_MICROS, _estimate

from .dataset import load_eval_split
from .label_audit import ORDER_PROMPT, chat_text, estimate_micros, order_text
from .stats import wilson
from .student_bakeoff import strip_fences
from .student_errors import chat_errors, student_predictions

EXPERIMENT = "order-check"
CHECK_VERSION = "order-check@0.2"
STUDENT = "qwen3.5-0.8b-single-v2"
STUDENT_RUNS = {
    Split.dev: RUNS / "student-dev" / "20261026T131201Z-qwen3.5-0.8b-single-v2",
    Split.fresh: RUNS / "student-dev" / "20261026T131201Z-qwen3.5-0.8b-single-v2-fresh",
}
CHECKERS = ("luna", "jev", "openai-decisions")
RIGHT_SEED = 20261103
ASSUMED_OUTPUT = 600  # verdict JSON + luna `low` reasoning
CHECK_PROMPT = (
    ORDER_PROMPT
    + " Use the menu: when the customer named no size, the size the menu marks as the default counts as "
    "what they asked for. A vague amount or size ('some', 'a few', 'big') is not a number or a menu size: the record "
    "must show it as unclear ('?' or 'size not stated'), and a number or size there is a mismatch."
)
SYSTEM = (
    "You check the work of a restaurant's chat bot. You get a text chat between a customer and the restaurant, the "
    "restaurant's menu, and the order the bot recorded from the chat. Answer the question about the record. Reply "
    'with JSON only: {"matches": true or false, "problem": "what is wrong, in one sentence, or an empty string if it '
    'matches"}.'
)
SCHEMA = {
    "type": "object",
    "properties": {"matches": {"type": "boolean"}, "problem": {"type": "string"}},
    "required": ["matches", "problem"],
    "additionalProperties": False,
}


def menu_text(menu: MenuCatalog) -> str:
    """The menu without prices: per item its sizes (default marked), what it comes with and what can be added."""

    def names(ids: list[str]) -> str:
        return ", ".join(getattr(menu.modifier(i), "name", i) for i in ids)

    lines = []
    for item in menu.items:
        parts = [item.name + ("" if item.available else " (not available)")]
        if item.variants:
            sizes = ", ".join(
                v.name + (" (default)" if v.id == item.default_variant_id else "") for v in item.variants
            )
            parts.append(
                f"sizes or kinds: {sizes}"
                + ("" if item.default_variant_id else " (no default: the customer chooses)")
            )
        if item.ingredient_ids:
            parts.append(f"comes with: {names(item.ingredient_ids)}")
        if item.addon_ids:
            parts.append(f"can add: {names(item.addon_ids)}")
        for slot in item.combo_slots:
            parts.append(
                f"{slot.name}: " + " or ".join(getattr(menu.item(c), "name", c) for c in slot.choices)
            )
        if item.splittable:
            parts.append("can be half-and-half")
        if item.sold_as is SoldAs.order:
            pieces = f" of {item.pieces_per_order} pieces" if item.pieces_per_order else ""
            parts.append(f"sold by the order{pieces}")
        lines.append("- " + "; ".join(parts))
    return "\n".join(lines)


def error_kinds(errors: dict[str, Any]) -> list[str]:
    """What is wrong with the order, in the student_errors vocabulary (one entry per wrong line or field)."""
    if "invalid" in errors:
        return ["broken_answer"]
    return [i["kind"] for i in errors["items"]] + [f"field:{k}" for k in errors["fields"]]


def _job(split: Split, ac, order, invalid: bool, wrong: bool) -> dict[str, Any]:
    conv, menu = ac.conversation, load_menu(ac.conversation.business_id)
    errors = (
        (chat_errors(ac, order, invalid) or {"items": [], "fields": {}})
        if wrong
        else {"items": [], "fields": {}}
    )
    recorded = order_text(order, menu, detail=True)
    text = input_text(conv, menu, recorded)
    jid = f"{split.value}__{conv.id}"
    return {
        "id": jid,
        "split": split.value,
        "conversation_id": conv.id,
        "wrong": wrong,
        "kinds": error_kinds(errors) if wrong else [],
        "errors": errors,
        "order_text": recorded,
        "request": chat_request(text),
        "decision_request": DecisionRequest(
            request_id=jid,
            input=text,
            questions=[Question(name="order_ok", type=QuestionType.boolean, prompt=CHECK_PROMPT)],
            prompt_version=CHECK_VERSION,
        ),
    }


def jobs() -> list[dict[str, Any]]:
    """Per split: every order not the same action as gold, then as many same-action orders, sampled with a seed."""
    out = []
    rng = random.Random(RIGHT_SEED)
    for split, run_dir in STUDENT_RUNS.items():
        acs = {ac.conversation.id: ac for ac in load_eval_split(split)}
        _, orders, _ = student_predictions(run_dir, acs)
        rows = [json.loads(x) for x in (run_dir / "order_rows.jsonl").read_text().splitlines() if x.strip()]
        rows.sort(key=lambda r: r["conversation_id"])
        wrong = [r["conversation_id"] for r in rows if not r["action_exact"]]
        right = rng.sample([r["conversation_id"] for r in rows if r["action_exact"]], len(wrong))
        for cid in wrong + sorted(right):
            out.append(_job(split, acs[cid], *orders[cid], wrong=cid in wrong))
    return out


def wrong_orders() -> list[dict[str, Any]]:
    """The student's real order mistakes on dev + fresh."""
    return [j for j in jobs() if j["wrong"]]


def input_text(conversation: Conversation, menu: MenuCatalog, recorded: str) -> str:
    return (
        f"A text chat between a customer and {menu.name}:\n{chat_text(conversation)}\n\n"
        f"The menu of {menu.name}:\n{menu_text(menu)}\n\n"
        f"The order as recorded after the last message:\n{recorded}"
    )


def chat_request(text: str) -> ChatRequest:
    return ChatRequest(
        system=SYSTEM,
        messages=[ChatMessage(role="user", content=f"{text}\n\n{CHECK_PROMPT}")],
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


def verdict(checker: str, rec: dict[str, Any]) -> dict[str, Any] | None:
    """{matches, problem} from a saved output, or None (error, refusal, unreadable)."""
    if "response" not in rec:
        return None
    if checker == "luna":
        return parse(rec["response"]["text"])
    a = DecisionResponse.model_validate(rec["response"]).answers["order_ok"]
    return None if a.refused else {"matches": a.boolean, "problem": ""}


def report(out_dir: Path) -> dict[str, Any]:
    manifest = json.loads((out_dir / "manifest.json").read_text())
    checkers = manifest["checkers"]
    rows: dict[str, dict[str, Any]] = {}
    for checker in checkers:
        for f in sorted((out_dir / "outputs" / checker).glob("*.json")):
            rec = json.loads(f.read_text())
            row = rows.setdefault(
                rec["id"],
                {"id": rec["id"], "split": rec["split"], "wrong": rec["wrong"], "kinds": rec["kinds"]},
            )
            v = verdict(checker, rec)
            row[checker] = {
                "verdict": v,
                "flagged": v is not None and not v["matches"],
                "error": rec.get("error"),
                "cost": 0
                if "response" not in rec or rec["response"].get("cached")
                else rec["response"]["cost_micros"],
            }
    rows_list = sorted(rows.values(), key=lambda r: (not r["wrong"], r["id"]))

    def rate(rs: list[dict], checker: str) -> dict[str, Any]:
        rs = [r for r in rs if checker in r]
        n, k = len(rs), sum(r[checker]["flagged"] for r in rs)
        return {"orders": n, "flagged": k, "rate": round(k / n, 4) if n else None, "ci95": wilson(k, n)}

    wrong = [r for r in rows_list if r["wrong"]]
    right = [r for r in rows_list if not r["wrong"]]
    by_kind: dict[str, list[dict]] = defaultdict(list)
    for r in wrong:
        for k in set(r["kinds"]):
            by_kind[k].append(r)
    per_checker = {}
    for c in checkers:
        per_checker[c] = {
            "caught": rate(wrong, c),
            "false_alarms": rate(right, c),
            "per_split": {
                s: {
                    "caught": rate([r for r in wrong if r["split"] == s], c),
                    "false_alarms": rate([r for r in right if r["split"] == s], c),
                }
                for s in ("dev", "fresh")
            },
            "broken_answers": rate([r for r in wrong if r["kinds"] == ["broken_answer"]], c),
            "per_kind": {k: rate(v, c) for k, v in sorted(by_kind.items())},
            "no_verdict": sum(c in r and r[c]["verdict"] is None for r in rows_list),
            "cost_micros": sum(r[c]["cost"] for r in rows_list if c in r),
        }
    metrics = {
        "check_version": CHECK_VERSION,
        "student": STUDENT,
        "wrong_orders": len(wrong),
        "right_orders": len(right),
        "checkers": per_checker,
        "cost_micros": manifest.get("actual_cost_micros"),
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")

    def pct(x: dict) -> str:
        if not x["orders"]:
            return "n/a"
        lo, hi = x["ci95"]
        return f"{x['flagged']}/{x['orders']} ({100 * x['rate']:.0f}%, {100 * lo:.0f}–{100 * hi:.0f}%)"

    def mark(r: dict, c: str) -> str:
        if c not in r:
            return ""
        if r[c]["verdict"] is None:
            return "no verdict"
        return "flag" if r[c]["flagged"] else "ok"

    head = " | ".join(checkers)
    lines = [
        f"# Order checker `{CHECK_VERSION}`: {', '.join(checkers)} on the student's orders",
        "",
        f"Whole-order check (spec §11b). Student `{STUDENT}`. {len(wrong)} orders that are not the same action as gold "
        f"(scorer@0.3) and {len(right)} that are (seeded sample, same number per split). Every checker sees the same "
        "chat, menu and order text. Fresh helped shape this version's rules: its numbers are seen while fixing, not "
        "held out.",
        "",
        "Caught = a wrong order flagged; false alarm = a right order flagged. 95% CI in brackets.",
        "",
        "| checker | wrong orders caught | false alarms | dev caught | dev false alarms | fresh caught | "
        "fresh false alarms | cost |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c, m in per_checker.items():
        d, f = m["per_split"]["dev"], m["per_split"]["fresh"]
        lines.append(
            f"| {c} | {pct(m['caught'])} | {pct(m['false_alarms'])} | {pct(d['caught'])} | {pct(d['false_alarms'])} "
            f"| {pct(f['caught'])} | {pct(f['false_alarms'])} | ${m['cost_micros'] / 1e6:.4f} |"
        )
    lines += [
        "",
        f"| what is wrong (a chat counts once per kind) | {head} |",
        "|---|" + "---|" * len(checkers),
    ]
    for k in sorted(by_kind, key=lambda k: -len(by_kind[k])):
        lines.append(f"| {k} | " + " | ".join(pct(per_checker[c]["per_kind"][k]) for c in checkers) + " |")
    lines += [
        "",
        f"| chat | student's order | what is wrong | {head} | luna's reason |",
        "|---|---|---|" + "---|" * len(checkers) + "---|",
    ]
    for r in rows_list:
        why = ""
        if "luna" in r:
            why = (r["luna"]["verdict"] or {}).get("problem") or r["luna"]["error"] or ""
        lines.append(
            f"| {r['id'].replace('__', ' ')} | {'wrong' if r['wrong'] else 'right'} | {', '.join(r['kinds'])} | "
            + " | ".join(mark(r, c) for c in checkers)
            + f" | {why.replace('|', '/')} |"
        )
    lines += ["", f"Cost: ${(metrics['cost_micros'] or 0) / 1e6:.4f}."]
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")
    return metrics


def run(args: argparse.Namespace) -> int:
    checkers = args.checkers.split(",")
    unknown = set(checkers) - set(CHECKERS)
    if unknown:
        print(f"Unknown checkers {sorted(unknown)}; choose from {', '.join(CHECKERS)}")
        return 2
    models = load_models()
    providers = {c: make_provider(c) for c in checkers if c != "luna"}
    all_jobs = jobs()
    est = {
        c: sum(
            _estimate(models[TEACHER], j["request"], ASSUMED_OUTPUT)
            if c == "luna"
            else estimate_micros(providers[c], j["decision_request"])
            for j in all_jobs
        )
        for c in checkers
    }
    counts = Counter((j["split"], "wrong" if j["wrong"] else "right") for j in all_jobs)
    print(
        f"Check {len(all_jobs)} orders of {STUDENT}, {CHECK_VERSION}: "
        + ", ".join(f"{s} {w}: {n}" for (s, w), n in sorted(counts.items()))
    )
    for c, e in est.items():
        verified = models[TEACHER].price_verified if c == "luna" else load_hosted()[c].price_verified
        print(f"  {c:18} ≈ ${e / 1e6:.4f}{'' if verified else ' (price not verified)'}")
    total = sum(est.values())
    print(f"  total              ≈ ${total / 1e6:.4f}")
    if not args.yes:
        print("Estimate only. Re-run with --yes.")
        return 0
    if total > OVER_LIMIT_MICROS:
        print("Estimate is over $2: ask Julian first.")
        return 2
    started = datetime.now(UTC)
    out_dir = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}-{CHECK_VERSION.split('@')[1]}"
    cache_mode = cache_mode_from_env()
    manifest: dict[str, Any] = {
        "experiment": EXPERIMENT,
        "check_version": CHECK_VERSION,
        "started_at": started.isoformat(),
        "git_commit": git_commit(),
        "checkers": checkers,
        "checker_config": {
            c: (
                {
                    "config_id": TEACHER,
                    "extra_body": models[TEACHER].extra_body,
                    "price_verified": models[TEACHER].price_verified,
                }
                if c == "luna"
                else providers[c].config.model_dump()
            )
            for c in checkers
        },
        "student": STUDENT,
        "student_runs": {s.value: str(p.relative_to(ROOT)) for s, p in STUDENT_RUNS.items()},
        "data": {
            "splits": ["dev", "fresh"],
            "source": "A (claude_written)",
            "selection": "student orders not the same action as gold (scorer@0.3), plus the same number per split "
            f"of same-action orders (random.Random({RIGHT_SEED}).sample)",
        },
        "ids": [j["id"] for j in all_jobs],
        "wrong_ids": [j["id"] for j in all_jobs if j["wrong"]],
        "cache_mode": cache_mode,
        "estimate_micros": est,
    }
    for c in checkers:
        (out_dir / "outputs" / c).mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    spent = [0]
    lock = threading.Lock()
    max_cost = min(2 * total, OVER_LIMIT_MICROS)

    def one(checker: str, job: dict[str, Any]) -> None:
        if spent[0] > max_cost:
            return
        rec = {
            k: job[k] for k in ("id", "split", "conversation_id", "wrong", "kinds", "errors", "order_text")
        }
        rec["checker"] = checker
        try:
            if checker == "luna":
                resp = make_client(TEACHER, cache_mode=cache_mode).complete(job["request"])
            else:
                resp = providers[checker].decide(job["decision_request"])
            rec["response"] = resp.model_dump(mode="json")
            cost = 0 if resp.cached else resp.cost_micros
        except (LLMError, DecisionError) as e:
            rec["error"] = str(e)
            cost = 0
        (out_dir / "outputs" / checker / f"{job['id']}.json").write_text(
            json.dumps(rec, indent=1, ensure_ascii=False) + "\n"
        )
        with lock:
            spent[0] += cost
            print(
                f"  {checker:18} {job['id']:22} {'error' if 'error' in rec else 'ok':6} ${spent[0] / 1e6:.4f}"
            )

    with ThreadPoolExecutor(max_workers=args.workers * len(checkers)) as pool:
        list(pool.map(lambda cj: one(*cj), [(c, j) for j in all_jobs for c in checkers]))
    manifest.update(finished_at=datetime.now(UTC).isoformat(), actual_cost_micros=spent[0])
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    report(out_dir)
    print((out_dir / "report.md").read_text())
    print(f"Saved {out_dir.relative_to(ROOT)}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkers", default=",".join(CHECKERS))
    ap.add_argument("--yes", action="store_true")
    ap.add_argument(
        "--workers", type=int, default=4, help="parallel requests per checker (rpm throttle applies)"
    )
    ap.add_argument("--report", type=Path)
    args = ap.parse_args(argv)
    if args.report:
        report(args.report)
        print((args.report / "report.md").read_text())
        return 0
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
