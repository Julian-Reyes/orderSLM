"""Synthetic training data, M4 (spec §7): plan cards → generate chats → label them → report.

    make synth ARGS="plan --batch p1 --n 500"                   # cards only, no calls
    make synth ARGS="generate --batch p1 --limit 5"              # estimate for 5 cards per generator
    make synth ARGS="generate --batch p1 --limit 5 --yes"        # write them
    make label ARGS="--batch p1 --limit 5 [--yes]"               # teacher labels for the kept chats
    make synth ARGS="report --batch p1"                          # rebuild summary + report from saved outputs

Everything lands in runs/synth/<batch>/: cards.jsonl, gen/<generator>/<card>.json (raw responses),
label/<teacher>/<card>.json, conversations.jsonl, labels.jsonl, drops, summary.json, report.md, and one
calls/<time>-<stage>.json per live stage (estimate, actual cost, versions). Responses go through the record/replay
cache (LLM_CACHE), so re-running a stage on cards already done costs $0.

Spend rules (spec §14) as in the bake-off: an estimate first; over $2 refuses without --allow-over-2; a stage
stops itself when actual cost passes --max-cost (default twice the estimate, at most $2).
"""

import argparse
import json
import statistics
import sys
import threading
from collections import Counter, defaultdict
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.core.finalize import FINALIZE_VERSION
from orderslm.data.splits import load_dir
from orderslm.llm.config import ModelConfig, load_models
from orderslm.llm.factory import cache_mode_from_env, make_client
from orderslm.llm.types import ChatRequest, ChatResponse, LLMError, LLMUsage
from orderslm.menus import load_menu, menu_version
from orderslm.paths import DEV, ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.common import LABEL_SCHEMA_VERSION, SYNTH_SCHEMA_VERSION
from orderslm.schema.conversation import Split
from orderslm.schema.synthetic import LabeledConversation, SynthCard, SyntheticConversation

from . import analysis as an
from . import generate as gen
from . import label as lab
from .cards import CARDS_VERSION, GENERATORS, plan_cards
from .dedup import THRESHOLD, near_duplicates

EXPERIMENT = "synth"
OVER_LIMIT_MICROS = 2_000_000  # $2: ask Julian first (CLAUDE.md)
SEED = 20261016
CHARS_PER_TOKEN = 3
ASSUMED_OVERHEAD = {"anthropic": 300}
ASSUMED_GEN_OUTPUT = 900  # chat JSON; generators run with reasoning off
ASSUMED_LABEL_OUTPUT = 1200 + 1500  # label JSON + luna `low` reasoning (bake-off: ~1.2K reasoning)
PEAK = datetime(2026, 10, 13, 2, 0, tzinfo=UTC)  # estimates never assume DeepSeek's off-peak price


def batch_dir(batch: str) -> Path:
    return RUNS / EXPERIMENT / batch


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def _slug(config_id: str) -> str:
    return config_id.replace("/", "__")


def _jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return (
        [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    )


def load_cards(batch: str) -> list[SynthCard]:
    return [SynthCard.model_validate(r) for r in _read_jsonl(batch_dir(batch) / "cards.jsonl")]


def _estimate(model: ModelConfig, req: ChatRequest, output_tokens: int) -> int:
    chars = len(req.system) + sum(len(m.content) for m in req.messages)
    usage = LLMUsage(
        input_tokens=chars // CHARS_PER_TOKEN + ASSUMED_OVERHEAD.get(model.provider, 0),
        output_tokens=output_tokens,
    )
    return model.cost_micros(usage, PEAK)


def _first_per_generator(cards: list[SynthCard], limit: int | None) -> list[SynthCard]:
    if limit is None:
        return cards
    taken: Counter[str] = Counter()
    out = []
    for c in sorted(cards, key=lambda c: c.id):
        if taken[c.generator] < limit:
            taken[c.generator] += 1
            out.append(c)
    return out


# ---------------------------------------------------------------- plan


def plan(args: argparse.Namespace) -> int:
    out = batch_dir(args.batch)
    if (out / "cards.jsonl").exists() and not args.force:
        print(f"{_rel(out)}/cards.jsonl exists; --force to replace it (only before any calls).")
        return 2
    cards = plan_cards(args.n, seed=args.seed, batch=args.batch)
    out.mkdir(parents=True, exist_ok=True)
    _jsonl(out / "cards.jsonl", [c.model_dump(mode="json") for c in cards])
    meta = {
        "batch": args.batch,
        "n": args.n,
        "seed": args.seed,
        "cards_version": CARDS_VERSION,
        "synth_schema_version": SYNTH_SCHEMA_VERSION,
        "generators": dict(GENERATORS),
        "menu_versions": {b: menu_version(load_menu(b)) for b in sorted({c.business_id for c in cards})},
        "planned_at": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "distribution": _card_distribution(cards),
    }
    (out / "plan.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Wrote {len(cards)} cards to {_rel(out)}/cards.jsonl")
    print(json.dumps(meta["distribution"]["generator"], indent=1))
    return 0


def _card_distribution(cards: list[SynthCard]) -> dict[str, dict[str, int]]:
    def count(f: Callable[[SynthCard], Any]) -> dict[str, int]:
        return dict(Counter(str(f(c)) for c in cards).most_common())

    return {
        "generator": count(lambda c: c.generator),
        "scenario": count(lambda c: c.scenario.value),
        "business": count(lambda c: c.business_id),
        "style": count(lambda c: c.style.value),
        "fulfillment": count(lambda c: c.fulfillment),
        "payment": count(lambda c: c.payment),
        "items": count(lambda c: len(c.items)),
        "expected_labels": dict(Counter(x.value for c in cards for x in c.expected_labels).most_common()),
    }


# ---------------------------------------------------------------- live calls


def _call_all(
    stage: str,
    batch: str,
    jobs: list[tuple[str, str, ChatRequest, Path]],  # (key, config id, request, output path)
    estimate: int,
    args: argparse.Namespace,
    versions: dict[str, Any],
) -> int:
    models = load_models()
    print(f"  {'total':40} ≈ ${estimate / 1e6:.4f} ({len(jobs)} calls)")
    if not args.yes:
        print(
            "Estimate only. Re-run with --yes to make the calls (cache mode from LLM_CACHE, default record)."
        )
        return 0
    if estimate > OVER_LIMIT_MICROS and not args.allow_over_2:
        print("Estimate is over $2: ask Julian first, then re-run with --allow-over-2.")
        return 2
    max_cost = int(args.max_cost * 1e6) if args.max_cost is not None else min(2 * estimate, OVER_LIMIT_MICROS)
    max_cost = max(max_cost, 1)
    cache_mode = cache_mode_from_env()
    started = datetime.now(UTC)
    record_path = batch_dir(batch) / "calls" / f"{started:%Y%m%dT%H%M%SZ}-{stage}.json"
    record: dict[str, Any] = {
        "stage": stage,
        "batch": batch,
        "started_at": started.isoformat(),
        "git_commit": git_commit(),
        "versions": versions,
        "models": {
            cid: {"extra_body": models[cid].extra_body, "price_verified": models[cid].price_verified}
            for cid in sorted({j[1] for j in jobs})
        },
        "calls": len(jobs),
        "cache_mode": cache_mode,
        "estimate_micros": estimate,
        "max_cost_micros": max_cost,
    }
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    spent = [0]
    lock = threading.Lock()
    stop = threading.Event()

    def worker(group: list[tuple[str, str, ChatRequest, Path]]) -> None:
        for key, cid, req, path in group:
            if stop.is_set():
                return
            out: dict[str, Any] = {"key": key, "config_id": cid}
            try:
                resp = make_client(cid, cache_mode=cache_mode).complete(req)
                out["response"] = resp.model_dump(mode="json")
                cost = 0 if resp.cached else resp.cost_micros
            except LLMError as e:
                out["error"] = str(e)
                cost = 0
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
            with lock:
                spent[0] += cost
                status = "error" if "error" in out else out["response"]["finish_reason"]
                print(f"  {cid:40} {key:14} {status:10} spent ${spent[0] / 1e6:.4f}")
                if spent[0] > max_cost:
                    print(f"STOP: actual ${spent[0] / 1e6:.4f} passed the limit ${max_cost / 1e6:.4f}")
                    stop.set()

    # One queue per provider, split over `workers` threads each; the shared per-model throttle still caps the rate.
    workers = max(getattr(args, "workers", 1) or 1, 1)
    by_provider: dict[str, list] = defaultdict(list)
    for j in jobs:
        by_provider[models[j[1]].provider].append(j)
    groups = [g[k::workers] for g in by_provider.values() for k in range(workers) if g[k::workers]]
    with ThreadPoolExecutor(max_workers=max(len(groups), 1)) as pool:
        list(pool.map(worker, groups))
    record.update(
        finished_at=datetime.now(UTC).isoformat(), actual_cost_micros=spent[0], stopped_early=stop.is_set()
    )
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(f"Actual cost ${spent[0] / 1e6:.4f}. Log: {_rel(record_path)}")
    return 1 if stop.is_set() else 0


# ---------------------------------------------------------------- generate


def generate(args: argparse.Namespace) -> int:
    models = load_models()
    cards = _first_per_generator(load_cards(args.batch), args.limit)
    if not cards:
        raise SystemExit(f"no cards in {batch_dir(args.batch)}; run plan first")
    jobs, per_gen = [], Counter()
    for c in cards:
        req = gen.build_request(c, load_menu(c.business_id))
        per_gen[c.generator] += _estimate(models[c.generator], req, ASSUMED_GEN_OUTPUT)
        jobs.append(
            (c.id, c.generator, req, batch_dir(args.batch) / "gen" / _slug(c.generator) / f"{c.id}.json")
        )
    print(
        f"Generate {len(cards)} chats, prompt {gen.GENERATOR_PROMPT_VERSION}. Estimate (assumptions, peak prices):"
    )
    for g, est in per_gen.items():
        print(f"  {g:40} ≈ ${est / 1e6:.4f}")
    versions = {"generator_prompt": gen.GENERATOR_PROMPT_VERSION, "cards": CARDS_VERSION}
    rc = _call_all("generate", args.batch, jobs, sum(per_gen.values()), args, versions)
    if args.yes:
        collect(args.batch)
    return rc


def _dev_conversations() -> list:
    return [ac.conversation for ac in load_dir(DEV, Split.dev)]


def collect(batch: str) -> None:
    """Rebuild conversations.jsonl / gen_drops.jsonl from every saved generator response."""
    out = batch_dir(batch)
    cards = {c.id: c for c in load_cards(batch)}
    kept: list[SyntheticConversation] = []
    drops: list[dict[str, Any]] = []
    for card in sorted(cards.values(), key=lambda c: c.id):
        path = out / "gen" / _slug(card.generator) / f"{card.id}.json"
        if not path.exists():
            continue
        rec = json.loads(path.read_text())
        if "error" in rec:
            drops.append({"card_id": card.id, "generator": card.generator, "reason": "call_error"})
            continue
        resp = ChatResponse.model_validate(rec["response"])
        conv, reason = gen.to_conversation(card, resp.text)
        if reason is None and resp.finish_reason in ("length", "max_tokens", "refusal"):
            reason = f"finish_reason={resp.finish_reason}"
        if conv is None or reason is not None:
            drops.append({"card_id": card.id, "generator": card.generator, "reason": reason})
        else:
            kept.append(conv)
    dupes = near_duplicates([k.conversation for k in kept], against=_dev_conversations())
    for k in kept:
        if k.conversation.id in dupes:
            other, sim = dupes[k.conversation.id]
            drops.append(
                {
                    "card_id": k.card_id,
                    "generator": k.generator,
                    "reason": f"near_duplicate_of {other} ({sim})",
                }
            )
    kept = [k for k in kept if k.conversation.id not in dupes]
    _jsonl(out / "conversations.jsonl", [k.model_dump(mode="json") for k in kept])
    _jsonl(out / "gen_drops.jsonl", drops)
    print(
        f"Kept {len(kept)} chats, dropped {len(drops)} ({dict(Counter(d['reason'].split(':')[0] for d in drops))})"
    )


def load_conversations(batch: str) -> list[SyntheticConversation]:
    return [
        SyntheticConversation.model_validate(r) for r in _read_jsonl(batch_dir(batch) / "conversations.jsonl")
    ]


# ---------------------------------------------------------------- label


def label(args: argparse.Namespace) -> int:
    models = load_models()
    teacher = args.teacher
    cards = {c.id: c for c in load_cards(args.batch)}
    convs = load_conversations(args.batch)
    if args.limit is not None:
        keep = {c.id for c in _first_per_generator([cards[s.card_id] for s in convs], args.limit)}
        convs = [s for s in convs if s.card_id in keep]
    jobs, est = [], 0
    for s in convs:
        req = lab.build_request(s.conversation, load_menu(s.conversation.business_id))
        est += _estimate(models[teacher], req, ASSUMED_LABEL_OUTPUT)
        jobs.append(
            (s.card_id, teacher, req, batch_dir(args.batch) / "label" / _slug(teacher) / f"{s.card_id}.json")
        )
    print(f"Label {len(convs)} chats with {teacher}, prompt {lab.LABEL_PROMPT_VERSION}. Estimate:")
    versions = {
        "label_prompt": lab.LABEL_PROMPT_VERSION,
        "label_schema": LABEL_SCHEMA_VERSION,
        "finalize": FINALIZE_VERSION,
    }
    rc = _call_all("label", args.batch, jobs, est, args, versions)
    if args.yes:
        collect_labels(args.batch, teacher)
    return rc


def collect_labels(batch: str, teacher: str) -> None:
    out = batch_dir(batch)
    cards = {c.id: c for c in load_cards(batch)}
    labels, drops, agreement = [], [], []
    for s in load_conversations(batch):
        path = out / "label" / _slug(teacher) / f"{s.card_id}.json"
        if not path.exists():
            continue
        rec = json.loads(path.read_text())
        card = cards[s.card_id]
        if "error" in rec:
            drops.append({"card_id": s.card_id, "generator": s.generator, "reason": "call_error"})
            continue
        resp = ChatResponse.model_validate(rec["response"])
        menu = load_menu(s.conversation.business_id)
        lc, reason = lab.parse_label(resp.text, s.conversation, menu, teacher)
        if lc is None:
            drops.append({"card_id": s.card_id, "generator": s.generator, "reason": reason})
            continue
        labels.append(lc.model_dump(mode="json"))
        agreement.append(
            {"card_id": s.card_id, "generator": s.generator, **lab.card_agreement(card, lc, menu)}
        )
    _jsonl(out / "labels.jsonl", labels)
    _jsonl(out / "label_drops.jsonl", drops)
    _jsonl(out / "agreement.jsonl", agreement)
    flagged = sum(1 for a in agreement if a["flags"])
    print(f"Labeled {len(labels)}, dropped {len(drops)}, card disagreements {flagged}")


# ---------------------------------------------------------------- report


def _usage(paths: list[Path]) -> dict[str, Any]:
    rows = []
    for p in paths:
        rec = json.loads(p.read_text())
        if "response" in rec:
            rows.append(ChatResponse.model_validate(rec["response"]))
    n = len(rows)
    cost = sum(r.cost_micros for r in rows)
    return {
        "calls": n,
        "input_tokens": sum(r.usage.input_tokens for r in rows),
        "cached_input_tokens": sum(r.usage.cached_input_tokens for r in rows),
        "output_tokens": sum(r.usage.output_tokens for r in rows),
        "reasoning_tokens": sum(r.usage.reasoning_tokens for r in rows),
        "cost_micros": cost,
        "cost_per_1k_usd": round(cost / n * 1000 / 1e6, 4) if n else None,
        "latency_p50_ms": round(statistics.median(r.latency_ms for r in rows)) if n else None,
    }


def report(args: argparse.Namespace) -> int:
    out = batch_dir(args.batch)
    # Rebuild the derived files from the saved responses first, so the report reflects the current checks ($0).
    collect(args.batch)
    for d in sorted((out / "label").glob("*")) if (out / "label").exists() else []:
        collect_labels(args.batch, d.name.replace("__", "/"))
    cards = load_cards(args.batch)
    convs = {s.card_id: s for s in load_conversations(args.batch)}
    gen_drops = _read_jsonl(out / "gen_drops.jsonl")
    labels = {
        r["conversation_id"]: LabeledConversation.model_validate(r) for r in _read_jsonl(out / "labels.jsonl")
    }
    label_drops = _read_jsonl(out / "label_drops.jsonl")
    agreement = {r["card_id"]: r for r in _read_jsonl(out / "agreement.jsonl")}
    card_by_id = {c.id: c for c in cards}
    by_gen: dict[str, Any] = {}
    for g in sorted({c.generator for c in cards}):
        mine = [c for c in cards if c.generator == g]
        attempted = [c for c in mine if (out / "gen" / _slug(g) / f"{c.id}.json").exists()]
        labeled_ids = [c.id for c in mine if c.id in labels]
        agr = [agreement[i] for i in labeled_ids if i in agreement]
        by_gen[g] = {
            "cards": len(mine),
            "generated": len(attempted),
            "kept": sum(1 for c in mine if c.id in convs),
            "repairs": dict(Counter(r for c in mine if c.id in convs for r in convs[c.id].repairs)),
            "gen_drops": dict(
                Counter(d["reason"].split(":")[0].split(" ")[0] for d in gen_drops if d["generator"] == g)
            ),
            "label_attempted": sum(1 for c in mine if any((out / "label").glob(f"*/{c.id}.json"))),
            "labeled": len(labeled_ids),
            "label_drops": dict(
                Counter(d["reason"].split(":")[0] for d in label_drops if d["generator"] == g)
            ),
            "card_agreement": {
                "labeled": len(agr),
                "all_agree": sum(1 for a in agr if not a["flags"]),
                "flags": dict(Counter(f for a in agr for f in a["flags"])),
            },
            "customer_messages_mean": round(
                statistics.mean(
                    len(convs[c.id].conversation.customer_indices()) for c in mine if c.id in convs
                ),
                2,
            )
            if any(c.id in convs for c in mine)
            else None,
            "generation_usage": _usage([out / "gen" / _slug(g) / f"{c.id}.json" for c in attempted]),
            "label_usage": _usage(sorted(p for c in mine for p in (out / "label").glob(f"*/{c.id}.json"))),
            "style": an.style_stats([convs[c.id] for c in mine if c.id in convs]),
            "diversity": an.diversity([convs[c.id] for c in mine if c.id in convs]),
            "addresses": an.addresses([convs[c.id] for c in mine if c.id in convs], card_by_id),
        }
    intents = Counter(i.primary.value for lc in labels.values() for i in lc.intents)
    summary = {
        "batch": args.batch,
        "built_at": datetime.now(UTC).isoformat(),
        "dedup_threshold": THRESHOLD,
        "by_generator": by_gen,
        "labeled_intents": dict(intents.most_common()),
        "planned": _card_distribution(cards),
        "agreement_by_scenario": an.agreement_by_scenario(agreement, card_by_id),
        "intents_by_generator": an.intents_by_generator(labels, card_by_id),
        "audit_sample": an.audit_sample(convs, agreement, card_by_id, args.audit_per_generator),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "report.md").write_text(an.render(summary, card_by_id))
    (out / "audit.md").write_text(
        an.render_audit(summary["audit_sample"], convs, labels, agreement, card_by_id)
    )
    print((out / "report.md").read_text())
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--batch", required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--force", action="store_true")
    for name in ("generate", "label"):
        p = sub.add_parser(name)
        p.add_argument("--batch", required=True)
        p.add_argument("--limit", type=int, help="only the first N cards per generator")
        p.add_argument("--yes", action="store_true", help="make the calls")
        p.add_argument("--allow-over-2", action="store_true")
        p.add_argument("--max-cost", type=float, help="stop when actual spend passes this many USD")
        p.add_argument(
            "--workers", type=int, default=1, help="parallel calls per provider (rpm throttle still applies)"
        )
        if name == "label":
            p.add_argument("--teacher", default=lab.TEACHER)
    p = sub.add_parser("report")
    p.add_argument("--batch", required=True)
    p.add_argument("--audit-per-generator", type=int, default=10)
    args = ap.parse_args(argv)
    return {"plan": plan, "generate": generate, "label": label, "report": report}[args.stage](args)


if __name__ == "__main__":
    sys.exit(main())
