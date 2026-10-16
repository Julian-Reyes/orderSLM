"""Training-label audit by the decision providers (spec §11d).

Each provider gets the chat and the recorded order in plain English, with the identical wording for every provider,
and answers per chat: the intent of every customer message (15 labels, LABEL_DESCRIPTIONS) and "does the recorded
order match what the customer asked for?" (yes/no).

    make label-audit ARGS="--set dev"                       # estimate only
    make label-audit ARGS="--set dev --yes"                 # gold + planted mistakes: accuracy, false alarms, catches
    make label-audit ARGS="--set train --yes"               # the teacher's labels on the synthetic training chats
    make label-audit ARGS="--report runs/label-audit/<id>"  # rebuild metrics + report from saved responses

`dev` measures the auditors (dev is for tuning; numbers are not held out): intent agreement with reviewed gold,
how often a correct gold order is flagged (false alarm), and how often each planted mistake (core/plant.py) is
caught. `train` flags teacher labels: an intent that disagrees with the teacher's, or an order the provider says
doesn't match. Flags go to review, never straight to deletion (providers make mistakes too).
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

from orderslm.core.plant import PLANT_VERSION, plant
from orderslm.interfaces.decision import (
    DecisionError,
    DecisionRequest,
    DecisionResponse,
    Option,
    Question,
    QuestionType,
)
from orderslm.menus import load_menu
from orderslm.paths import ROOT, RUNS
from orderslm.providers.hosted import HostedDecisionProvider, load_hosted, make_provider
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Conversation, Split
from orderslm.schema.extraction import (
    Amount,
    DecisionState,
    ExtractionOutput,
    FulfillmentMethod,
    ItemProposal,
    ModificationKind,
    PaymentMethod,
    SlotState,
)
from orderslm.schema.menu import MenuCatalog
from orderslm.schema.routing import LABEL_DESCRIPTIONS
from orderslm.schema.synthetic import LabeledConversation

from .dataset import load_eval_split
from .stats import wilson

AUDIT_VERSION = "label-audit@0.2"  # 0.2 (dev): cancelled / no-order / unclear-item wording
EXPERIMENT = "label-audit"
OVER_LIMIT_MICROS = 2_000_000
CHARS_PER_TOKEN = 3.5
INTENT_PROMPT = "What does customer message [{i}] do, read in the context of the messages before it?"
ORDER_PROMPT = (
    "Does the record below match the chat: the same items, quantities, sizes and options after any changes, the same "
    "pickup or delivery and payment, and the same status (still open, confirmed or cancelled)? Something the customer "
    "never said is listed as 'not stated', and that is not a mismatch. If the record says no order was placed, answer "
    "yes only if the customer ordered nothing in this chat. Answer yes only if everything matches."
)
LABEL_OPTIONS = [Option(id=k.value, description=v) for k, v in LABEL_DESCRIPTIONS.items()]


# ---------------------------------------------------------------- what the providers see


def chat_text(conversation: Conversation) -> str:
    return "\n".join(f"[{m.index}] {m.role.value}: {m.text}" for m in conversation.messages)


def _line_text(line: ItemProposal, menu: MenuCatalog, unclear: bool = False) -> str:
    def mod_name(mid: str | None) -> str:
        m = menu.modifier(mid or "")
        return m.name if m else (mid or "")

    if line.unmatched_text is not None:
        qty = line.quantity if line.quantity is not None else "?"
        kind = "unclear which menu item" if unclear else "not on the menu"
        return f"{qty} × {line.unmatched_text!r} ({kind})"
    if line.halves:
        halves = " / ".join(
            "half "
            + menu.item(h.menu_item_id).name  # type: ignore[union-attr]
            + "".join(f", {m.kind.value} {mod_name(m.modifier_id)}" for m in h.modifications)
            for h in line.halves
        )
        base = menu.item(line.halves[0].menu_item_id)
        name = f"half-and-half pizza ({halves})"
    else:
        base = menu.item(line.menu_item_id or "")
        name = base.name if base else str(line.menu_item_id)
    qty = line.quantity if line.quantity is not None else "?"
    text = f"{qty} × {name}"
    variant = base.variant(line.variant_id) if base and line.variant_id else None
    if variant:
        text += f" ({variant.name})"
    elif line.unmatched_variant_text:
        text += f" (size asked: {line.unmatched_variant_text!r}, not on the menu)"
    parts = []
    for m in line.modifications:
        if m.not_on_menu or m.kitchen_note:
            parts.append(m.raw_text)
        elif m.kind is ModificationKind.remove:
            parts.append(f"no {mod_name(m.modifier_id)}")
        elif m.kind is ModificationKind.substitute:
            parts.append(f"{mod_name(m.replacement_modifier_id)} instead of {mod_name(m.modifier_id)}")
        else:
            amount = {Amount.extra: "extra ", Amount.light: "light "}.get(m.amount, "")
            parts.append(f"add {amount}{mod_name(m.modifier_id)}")
    for c in line.combo_selections:
        item = menu.item(c.menu_item_id)
        parts.append(f"{c.slot_id}: {item.name if item else c.menu_item_id}")
    return text + (": " + ", ".join(parts) if parts else "")


def order_text(out: ExtractionOutput | None, menu: MenuCatalog) -> str:
    if out is None or not out.items:
        return "No order was placed in this chat."
    unclear = {
        m.line_id
        for m in out.missing_or_ambiguous
        if m.field.value == "item_menu_match" and m.reason.value == "ambiguous"
    }
    status = {
        DecisionState.confirmed: "Status: confirmed by the customer",
        DecisionState.cancelled: "Status: CANCELLED by the customer (the items below are what was cancelled)",
    }.get(out.customer_decision.state, "Status: still open (not confirmed yet)")
    lines = [status] + [f"- {_line_text(x, menu, x.line_id in unclear)}" for x in out.items]
    method = out.fulfillment.method
    if method is FulfillmentMethod.delivery:
        where = (
            f" to {out.address.raw_text}" if out.address.state is SlotState.provided else " (no address yet)"
        )
        lines.append(f"Fulfillment: delivery{where}")
    elif method is FulfillmentMethod.pickup:
        lines.append("Fulfillment: pickup")
    else:
        lines.append("Fulfillment: not stated")
    if out.fulfillment.requested_time.state is SlotState.provided:
        lines.append(f"Time: {out.fulfillment.requested_time.raw_text}")
    pay = out.payment.method
    lines.append(f"Payment: {'not stated' if pay is PaymentMethod.unknown else pay.value}")
    if out.customer_name.state is SlotState.provided:
        lines.append(f"Name: {out.customer_name.value}")
    return "\n".join(lines)


def build_request(
    request_id: str,
    conversation: Conversation,
    order: ExtractionOutput | None,
    menu: MenuCatalog,
    *,
    intents: bool = True,
) -> DecisionRequest:
    questions = [Question(name="order_ok", type=QuestionType.boolean, prompt=ORDER_PROMPT)]
    if intents:
        questions = [
            Question(
                name=f"intent_m{i}",
                type=QuestionType.choice,
                prompt=INTENT_PROMPT.format(i=i),
                options=LABEL_OPTIONS,
            )
            for i in conversation.customer_indices()
        ] + questions
    text = (
        f"A text chat between a customer and {menu.name}:\n{chat_text(conversation)}\n\n"
        f"The order as recorded after the last message:\n{order_text(order, menu)}"
    )
    return DecisionRequest(
        request_id=request_id, input=text, questions=questions, prompt_version=AUDIT_VERSION
    )


# ---------------------------------------------------------------- the sets


def dev_jobs() -> list[dict[str, Any]]:
    """Gold (all intents + order) for every dev chat, and one order-only job per planted mistake."""
    jobs = []
    for ac in sorted(load_eval_split(Split.dev), key=lambda a: a.conversation.id):
        conv, menu = ac.conversation, load_menu(ac.conversation.business_id)
        gold_intents = {r.message_index: r.decision for r in ac.gold_routing}
        jobs.append(
            {
                "id": conv.id,
                "kind": "gold",
                "request": build_request(conv.id, conv, ac.gold_extraction, menu),
                "expected_order_ok": True,
                "intents": {
                    i: (d.primary.value, d.secondary.value if d.secondary else None)
                    for i, d in gold_intents.items()
                },
            }
        )
        if ac.gold_extraction is not None:
            for mistake, copy in plant(ac.gold_extraction, menu, seed=conv.id).items():
                jid = f"{conv.id}--{mistake.value.replace('_', '-')}"
                jobs.append(
                    {
                        "id": jid,
                        "kind": "planted",
                        "mistake": mistake.value,
                        "request": build_request(jid, conv, copy, menu, intents=False),
                        "expected_order_ok": False,
                    }
                )
    return jobs


def train_jobs(batches: list[str]) -> list[dict[str, Any]]:
    from orderslm.synth.run import _read_jsonl, batch_dir, load_conversations

    jobs = []
    for b in batches:
        convs = {s.card_id: s for s in load_conversations(b)}
        for r in _read_jsonl(batch_dir(b) / "labels.jsonl"):
            lc = LabeledConversation.model_validate(r)
            s = convs[lc.conversation_id]
            menu = load_menu(s.conversation.business_id)
            jobs.append(
                {
                    "id": lc.conversation_id,
                    "kind": "train",
                    "batch": b,
                    "generator": s.generator,
                    "request": build_request(lc.conversation_id, s.conversation, lc.extraction, menu),
                    "intents": {
                        i.message_index: (i.primary.value, i.secondary.value if i.secondary else None)
                        for i in lc.intents
                    },
                }
            )
    return jobs


# ---------------------------------------------------------------- run + score


def estimate_micros(provider: HostedDecisionProvider, req: DecisionRequest) -> int:
    chars = len(req.input) + sum(
        len(q.prompt) + sum(len(o.id) + len(o.description) for o in q.options) for q in req.questions
    )
    return -(-int(chars / CHARS_PER_TOKEN) * provider.config.price_input_per_1m // 1_000_000)


def score(jobs: list[dict[str, Any]], responses: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Per provider: intent agreement, order_ok on correct orders (false alarms) and on planted mistakes (catches)."""
    out: dict[str, Any] = {}
    for provider, by_id in responses.items():
        intent_n = intent_ok = intent_set_ok = 0
        confusions: Counter = Counter()
        correct_n = false_alarm = 0
        caught: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        cost = tokens = errors = 0
        latencies = []
        for job in jobs:
            rec = by_id.get(job["id"])
            if rec is None:
                continue
            if "error" in rec:
                errors += 1
                continue
            resp = DecisionResponse.model_validate(rec["response"])
            cost += 0 if resp.cached else resp.cost_micros
            tokens += resp.usage.input_tokens
            latencies.append(resp.latency_ms)
            for i, (primary, secondary) in (job.get("intents") or {}).items():
                a = resp.answers.get(f"intent_m{i}")
                if a is None or a.refused:
                    continue
                intent_n += 1
                intent_ok += a.choice == primary
                intent_set_ok += a.choice in (primary, secondary)
                if a.choice != primary:
                    confusions[(primary, a.choice)] += 1
            order = resp.answers["order_ok"]
            if order.refused:
                continue
            if job.get("expected_order_ok") is True or job["kind"] == "train":
                correct_n += 1
                false_alarm += not order.boolean
            elif job["kind"] == "planted":
                caught[job["mistake"]][1] += 1
                caught[job["mistake"]][0] += not order.boolean
        planted_total = sum(n for _, n in caught.values())
        planted_caught = sum(c for c, _ in caught.values())
        latencies.sort()
        out[provider] = {
            "intent_messages": intent_n,
            "intent_agree_primary": intent_ok,
            "intent_agree_rate": round(intent_ok / intent_n, 4) if intent_n else None,
            "intent_agree_ci95": wilson(intent_ok, intent_n) if intent_n else None,
            "intent_agree_primary_or_secondary": intent_set_ok,
            "intent_confusions": [
                {"expected": e, "provider": p, "count": c} for (e, p), c in confusions.most_common(15)
            ],
            "orders_expected_ok": correct_n,
            "order_flagged": false_alarm,
            "order_flag_rate": round(false_alarm / correct_n, 4) if correct_n else None,
            "planted": {
                k: {"caught": c, "of": n, "rate": round(c / n, 3)} for k, (c, n) in sorted(caught.items())
            },
            "planted_catch_rate": round(planted_caught / planted_total, 4) if planted_total else None,
            "errors": errors,
            "input_tokens": tokens,
            "cost_micros": cost,
            "latency_p50_ms": round(latencies[len(latencies) // 2]) if latencies else None,
            "latency_p95_ms": round(latencies[int(len(latencies) * 0.95)]) if latencies else None,
        }
    return out


def _load_jobs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return dev_jobs() if manifest["set"] == "dev" else train_jobs(manifest["batches"])


def report(out_dir: Path) -> dict[str, Any]:
    manifest = json.loads((out_dir / "manifest.json").read_text())
    jobs = [j for j in _load_jobs(manifest) if j["id"] in set(manifest["job_ids"])]
    responses = {
        p: {f.stem: json.loads(f.read_text()) for f in (out_dir / "responses" / p).glob("*.json")}
        for p in manifest["providers"]
    }
    metrics = score(jobs, responses)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    if manifest["set"] == "train":
        _write_flags(out_dir, jobs, responses)
    L = [f"# Label audit `{manifest['set']}` ({AUDIT_VERSION}, {PLANT_VERSION})", ""]
    if manifest["set"] == "dev":
        L.append(
            "Dev = tuning data, not held out. Intents compared with reviewed gold; gold orders should be judged"
            " matching, planted copies not."
        )
    else:
        L.append(
            "Training labels from the teacher. Agreement = provider's intent equals the teacher's primary."
            " Flags: `flags.jsonl` (for review, not deletion)."
        )
    L += [
        "",
        "| | " + " | ".join(manifest["providers"]) + " |",
        "|---|" + "---|" * len(manifest["providers"]),
    ]

    def row(name, f):
        L.append(f"| {name} | " + " | ".join(str(f(metrics[p])) for p in manifest["providers"]) + " |")

    ref = "gold" if manifest["set"] == "dev" else "teacher"
    row(
        f"intent = {ref} (primary)",
        lambda m: f"{m['intent_agree_primary']}/{m['intent_messages']} ({m['intent_agree_rate']})",
    )
    row("intent 95% CI", lambda m: m["intent_agree_ci95"])
    row(f"intent = {ref} primary or secondary", lambda m: m["intent_agree_primary_or_secondary"])
    row(
        f"{'correct' if ref == 'gold' else 'teacher'} orders judged NOT matching",
        lambda m: f"{m['order_flagged']}/{m['orders_expected_ok']} ({m['order_flag_rate']})",
    )
    if manifest["set"] == "dev":
        row("planted mistakes caught", lambda m: m["planted_catch_rate"])
        kinds = sorted({k for m in metrics.values() for k in m["planted"]})
        for k in kinds:
            row(
                f"… {k}",
                lambda m, k=k: (
                    f"{m['planted'].get(k, {}).get('caught', '–')}/{m['planted'].get(k, {}).get('of', '–')}"
                ),
            )
    row("errors", lambda m: m["errors"])
    row("input tokens", lambda m: f"{m['input_tokens']:,}")
    row("cost (USD)", lambda m: f"${m['cost_micros'] / 1e6:.4f}")
    row("latency p50 / p95 ms", lambda m: f"{m['latency_p50_ms']} / {m['latency_p95_ms']}")
    L += [
        "",
        "Jev's price ($0.042/1M input) is not yet verified on TypeSafe's pricing page: its cost is an estimate.",
        "",
    ]
    for p in manifest["providers"]:
        L.append(
            f"Top intent disagreements, {p}: "
            + "; ".join(
                f"{c['expected']}→{c['provider']} ×{c['count']}" for c in metrics[p]["intent_confusions"][:8]
            )
        )
    (out_dir / "report.md").write_text("\n".join(L) + "\n")
    return metrics


def _write_flags(out_dir: Path, jobs: list[dict[str, Any]], responses: dict[str, dict[str, Any]]) -> None:
    rows = []
    for job in jobs:
        flags: dict[str, Any] = {}
        for p, by_id in responses.items():
            rec = by_id.get(job["id"])
            if not rec or "error" in rec:
                continue
            resp = DecisionResponse.model_validate(rec["response"])
            mine = []
            for i, (primary, secondary) in job["intents"].items():
                a = resp.answers.get(f"intent_m{i}")
                if a and not a.refused and a.choice not in (primary, secondary):
                    mine.append(
                        {
                            "message_index": i,
                            "teacher": primary,
                            "provider": a.choice,
                            "confidence": a.confidence,
                        }
                    )
            order = resp.answers["order_ok"]
            if mine or (not order.refused and not order.boolean):
                flags[p] = {
                    "intents": mine,
                    "order_ok": order.boolean,
                    "p_order_ok": (order.probabilities or {}).get("true"),
                }
        if flags:
            rows.append(
                {
                    "id": job["id"],
                    "batch": job["batch"],
                    "generator": job["generator"],
                    "flags": flags,
                    "flagged_by": sorted(flags),
                }
            )
    (out_dir / "flags.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))


def run(args: argparse.Namespace) -> int:
    providers = {name: make_provider(name) for name in args.providers.split(",")}
    jobs = dev_jobs() if args.set == "dev" else train_jobs(args.batches.split(","))
    if args.limit:
        jobs = jobs[: args.limit]
    est = {n: sum(estimate_micros(p, j["request"]) for j in jobs) for n, p in providers.items()}
    print(f"Label audit `{args.set}`: {len(jobs)} requests × {len(providers)} providers. Estimate:")
    for n, e in est.items():
        verified = load_hosted()[n].price_verified
        print(f"  {n:20} ≈ ${e / 1e6:.4f}{'' if verified else ' (price not verified)'}")
    if not args.yes:
        print("Estimate only. Re-run with --yes.")
        return 0
    if sum(est.values()) > OVER_LIMIT_MICROS and not args.allow_over_2:
        print("Estimate is over $2: ask Julian first, then re-run with --allow-over-2.")
        return 2
    started = datetime.now(UTC)
    out_dir = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}-{args.set}"
    manifest = {
        "experiment": EXPERIMENT,
        "audit_version": AUDIT_VERSION,
        "plant_version": PLANT_VERSION,
        "set": args.set,
        "batches": args.batches.split(",") if args.set == "train" else None,
        "providers": list(providers),
        "provider_config": {n: p.config.model_dump() for n, p in providers.items()},
        "started_at": started.isoformat(),
        "git_commit": git_commit(),
        "job_ids": [j["id"] for j in jobs],
        "estimate_micros": est,
    }
    (out_dir / "responses").mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    max_cost = int(args.max_cost * 1e6) if args.max_cost else max(2 * sum(est.values()), 1)
    spent = [0]
    lock = threading.Lock()
    stop = threading.Event()

    def one(name: str, provider: HostedDecisionProvider, job: dict[str, Any]) -> None:
        if stop.is_set():
            return
        rec: dict[str, Any] = {"id": job["id"]}
        try:
            resp = provider.decide(job["request"])
            rec["response"] = resp.model_dump(mode="json")
            cost = 0 if resp.cached else resp.cost_micros
        except DecisionError as e:
            rec["error"] = str(e)
            cost = 0
        path = out_dir / "responses" / name / f"{job['id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rec, indent=1) + "\n")
        with lock:
            spent[0] += cost
            if spent[0] > max_cost and not stop.is_set():
                print(f"STOP: spent ${spent[0] / 1e6:.4f} > ${max_cost / 1e6:.4f}")
                stop.set()

    with ThreadPoolExecutor(max_workers=args.workers * len(providers)) as pool:
        futures = [pool.submit(one, n, p, j) for j in jobs for n, p in providers.items()]
        for k, f in enumerate(futures, 1):
            f.result()
            if k % 200 == 0:
                print(f"  {k}/{len(futures)} done, spent ${spent[0] / 1e6:.4f}")
    manifest.update(
        finished_at=datetime.now(UTC).isoformat(), actual_cost_micros=spent[0], stopped_early=stop.is_set()
    )
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    report(out_dir)
    print((out_dir / "report.md").read_text())
    print(f"Saved {out_dir.relative_to(ROOT)}/ (spent ${spent[0] / 1e6:.4f})")
    return 1 if stop.is_set() else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", choices=["dev", "train"], default="dev")
    ap.add_argument("--batches", default="p3,b1,m1", help="synthetic batches for --set train")
    ap.add_argument("--providers", default="jev,openai-decisions")
    ap.add_argument("--limit", type=int)
    ap.add_argument(
        "--workers", type=int, default=4, help="parallel requests per provider (rpm throttle applies)"
    )
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--allow-over-2", action="store_true")
    ap.add_argument("--max-cost", type=float)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args(argv)
    if args.report:
        report(args.report)
        print((args.report / "report.md").read_text())
        return 0
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
