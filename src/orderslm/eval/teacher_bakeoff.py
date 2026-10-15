"""Experiment 1, teacher bake-off (spec §8): the same prompt and schema for every model variant on a fixed dev
subset; scores, tokens and cost per variant.

    make teacher-bakeoff                        # estimate for the full run, no calls
    make teacher-bakeoff ARGS="--pilot 5"       # estimate for a 5-conversation pilot
    make teacher-bakeoff ARGS="--pilot 5 --yes" # run it (record/replay cache: reruns cost $0)
    make teacher-bakeoff ARGS="--report runs/teacher-bakeoff/<id>"   # rebuild metrics + report from saved outputs

Spend rules (spec §14): every live run prints an estimate first; a run estimated over $2 refuses without
--allow-over-2 (ask Julian first); a run stops itself if its actual cost passes --max-cost (default: twice the
estimate, at most $2). Outputs: runs/teacher-bakeoff/<run_id>/{manifest.json, outputs/<variant>/<conv>.json,
metrics.json, report.md}. Every number in the report comes from those saved outputs.
"""

import argparse
import hashlib
import json
import statistics
import subprocess
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.data.splits import conversation_files
from orderslm.extractors.teacher import (
    TEACHER_PROMPT_VERSION,
    build_chat_request,
    portable_schema,
    prompt_text,
    to_result,
)
from orderslm.interfaces.extractor import ExtractionRequest
from orderslm.llm.cache import CacheMode
from orderslm.llm.config import ModelConfig, load_models
from orderslm.llm.factory import cache_mode_from_env, make_client
from orderslm.llm.types import ChatRequest, ChatResponse, LLMError, LLMUsage
from orderslm.menus import load_menu, menu_version
from orderslm.paths import DEV, ROOT, RUNS
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.common import EXTRACTION_SCHEMA_VERSION
from orderslm.schema.conversation import Split

from .dataset import BAKEOFF_SEED, BAKEOFF_SIZE, bakeoff_set, load_eval_split, remaining_dev
from .metrics import aggregate, score_conversation

EXPERIMENT = "teacher-bakeoff"
OVER_LIMIT_MICROS = 2_000_000  # $2: ask Julian first (CLAUDE.md)
# Pre-pilot assumptions (no tokenizer for every provider): ~3 characters per token for this JSON-heavy prompt,
# output ≈ gold JSON size, and assumed reasoning tokens per variant tier. Replaced by measured numbers once a
# pilot exists (the pilot report projects the full run from actual usage).
CHARS_PER_TOKEN = 3
ASSUMED_REASONING = {"none": 0, "minimal": 0, "off-low": 0, "off-medium": 0, "low": 1500, "on-low": 1500}
ASSUMED_REASONING_DEFAULT = 4000  # medium/high/default/on-medium
ASSUMED_OVERHEAD = {"anthropic": 300}  # structured-output instructions the provider adds (smoke: ~200)


def _request(ac: AnnotatedConversation, schema: dict) -> ChatRequest:
    menu = load_menu(ac.conversation.business_id).extractor_view()
    req = ExtractionRequest(menu=menu, conversation=ac.conversation, prompt_version=TEACHER_PROMPT_VERSION)
    return build_chat_request(req, schema)


def estimate_micros(model: ModelConfig, chat: ChatRequest, ac: AnnotatedConversation) -> tuple[int, LLMUsage]:
    chars = len(chat.system) + sum(len(m.content) for m in chat.messages)
    input_tokens = chars // CHARS_PER_TOKEN + ASSUMED_OVERHEAD.get(model.provider, 0)
    gold = ac.gold_extraction.model_dump_json() if ac.gold_extraction else "{}"
    reasoning = ASSUMED_REASONING.get(model.variant, ASSUMED_REASONING_DEFAULT)
    usage = LLMUsage(
        input_tokens=input_tokens, output_tokens=max(len(gold) // CHARS_PER_TOKEN, 300) + reasoning
    )
    # Price at peak time where it matters (DeepSeek): estimates never assume the cheaper window.
    peak = datetime(2026, 10, 13, 2, 0, tzinfo=UTC)
    return model.cost_micros(usage, peak), usage


def _git_commit() -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    return (out.stdout.strip() or "unknown") + ("-dirty" if dirty.stdout.strip() else "")


def _dev_hash(ids: list[str]) -> str:
    h = hashlib.sha256()
    by_name = {p.stem: p for p in conversation_files(DEV)}
    for cid in sorted(ids):
        h.update(by_name[cid].read_bytes())
    return h.hexdigest()[:16]


def _slug(config_id: str) -> str:
    return config_id.replace("/", "__")


def run(args: argparse.Namespace) -> int:
    models = load_models()
    variants = args.variants.split(",") if args.variants else list(models)
    unknown = [v for v in variants if v not in models]
    if unknown:
        raise SystemExit(f"unknown variants {unknown}; known: {sorted(models)}")
    dev = load_eval_split(Split.dev)
    if args.set == "all":
        pool = sorted(dev, key=lambda ac: ac.conversation.id)
    else:
        pool = remaining_dev(dev) if args.set == "remaining" else bakeoff_set(dev, BAKEOFF_SIZE, BAKEOFF_SEED)
    convs = pool[args.skip :]
    if args.pilot:
        convs = convs[: args.pilot]
    schema = portable_schema()
    chats = {ac.conversation.id: _request(ac, schema) for ac in convs}

    total_est = 0
    per_variant_est: dict[str, int] = {}
    for v in variants:
        est = sum(estimate_micros(models[v], chats[ac.conversation.id], ac)[0] for ac in convs)
        per_variant_est[v] = est
        total_est += est
    mode = f"pilot {len(convs)}" if args.pilot else f"full {len(convs)}"
    if args.skip:
        mode += f" (bake-off set positions {args.skip + 1}-{args.skip + len(convs)})"
    if args.set != "bakeoff":
        mode += {"remaining": " (remaining dev: not in the bake-off set)", "all": " (all dev)"}[args.set]
    print(
        f"Teacher bake-off ({mode} conversations × {len(variants)} variants = {len(convs) * len(variants)} calls)"
    )
    print(
        f"Prompt {TEACHER_PROMPT_VERSION}, schema {EXTRACTION_SCHEMA_VERSION}. Estimate (assumptions, peak prices):"
    )
    for v in variants:
        print(f"  {v:40} ≈ ${per_variant_est[v] / 1e6:.4f}")
    print(f"  {'total':40} ≈ ${total_est / 1e6:.4f}")
    if not args.yes:
        print(
            "Estimate only. Re-run with --yes to make the calls (cache mode from LLM_CACHE, default record)."
        )
        return 0
    if total_est > OVER_LIMIT_MICROS and not args.allow_over_2:
        print("Estimate is over $2: ask Julian first, then re-run with --allow-over-2.")
        return 2
    max_cost = (
        int(args.max_cost * 1e6) if args.max_cost is not None else min(2 * total_est, OVER_LIMIT_MICROS)
    )
    max_cost = max(max_cost, 1)

    started = datetime.now(UTC)
    run_id = started.strftime("%Y%m%dT%H%M%SZ") + (f"-pilot{len(convs)}" if args.pilot else "-full")
    run_id += f"-skip{args.skip}" if args.skip else ""
    run_id += f"-{args.set}" if args.set != "bakeoff" else ""
    out_dir = RUNS / EXPERIMENT / run_id
    cache_mode: CacheMode = cache_mode_from_env()
    manifest: dict[str, Any] = {
        "run_id": run_id,
        "experiment": EXPERIMENT,
        "mode": mode,
        "started_at": started.isoformat(),
        "git_commit": _git_commit(),
        "prompt_version": TEACHER_PROMPT_VERSION,
        "prompt_sha256": hashlib.sha256(prompt_text().encode()).hexdigest()[:16],
        "schema_version": EXTRACTION_SCHEMA_VERSION,
        "portable_schema_sha256": hashlib.sha256(json.dumps(schema, sort_keys=True).encode()).hexdigest()[
            :16
        ],
        "data": {
            "split": "dev",
            "source": "A (claude_written)",
            "selection": {
                "remaining": "remaining_dev()",
                "all": "all dev, sorted by id",
                "bakeoff": f"bakeoff_set(size={BAKEOFF_SIZE}, seed={BAKEOFF_SEED})",
            }[args.set]
            + f"[{args.skip}:]"
            + (f"[:{args.pilot}]" if args.pilot else ""),
            "conversation_ids": [ac.conversation.id for ac in convs],
            "dev_files_sha256": _dev_hash([ac.conversation.id for ac in convs]),
            "menu_versions": {
                b: menu_version(load_menu(b)) for b in sorted({ac.conversation.business_id for ac in convs})
            },
        },
        "variants": {
            v: {
                "provider": models[v].provider,
                "model": models[v].model,
                "extra_body": models[v].extra_body,
                "provider_default": models[v].provider_default,
                "price_verified": models[v].price_verified,
            }
            for v in variants
        },
        "cache_mode": cache_mode,
        "estimate_micros": total_est,
        "max_cost_micros": max_cost,
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    spent = [0]
    lock = threading.Lock()
    stop = threading.Event()

    def provider_worker(vs: list[str]) -> None:
        for ac in convs:
            for v in vs:
                if stop.is_set():
                    return
                path = out_dir / "outputs" / _slug(v) / f"{ac.conversation.id}.json"
                record: dict[str, Any] = {"conversation_id": ac.conversation.id, "config_id": v}
                try:
                    resp = make_client(v, cache_mode=cache_mode).complete(chats[ac.conversation.id])
                    record["response"] = resp.model_dump(mode="json")
                    cost = 0 if resp.cached else resp.cost_micros
                except LLMError as e:
                    record["error"] = str(e)
                    cost = 0
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(record, indent=1) + "\n")
                with lock:
                    spent[0] += cost
                    status = "error" if "error" in record else record["response"]["finish_reason"]
                    print(f"  {v:40} {ac.conversation.id:12} {status:10} spent ${spent[0] / 1e6:.4f}")
                    if spent[0] > max_cost:
                        print(f"STOP: actual ${spent[0] / 1e6:.4f} passed the limit ${max_cost / 1e6:.4f}")
                        stop.set()

    by_provider: dict[str, list[str]] = defaultdict(list)
    for v in variants:
        by_provider[models[v].provider].append(v)
    with ThreadPoolExecutor(max_workers=len(by_provider)) as pool:
        list(pool.map(provider_worker, by_provider.values()))

    manifest["finished_at"] = datetime.now(UTC).isoformat()
    manifest["actual_cost_micros"] = spent[0]
    manifest["stopped_early"] = stop.is_set()
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    report(out_dir)
    print(f"Actual cost ${spent[0] / 1e6:.4f}. Saved {out_dir.relative_to(ROOT)}/")
    return 1 if stop.is_set() else 0


def _pct(x: float | None) -> str:
    return "—" if x is None else f"{100 * x:.1f}%"


def report(out_dir: Path) -> dict[str, Any]:
    """Rebuild metrics.json and report.md from saved outputs only."""
    manifest = json.loads((out_dir / "manifest.json").read_text())
    ids = manifest["data"]["conversation_ids"]
    gold = {ac.conversation.id: ac for ac in load_eval_split(Split.dev) if ac.conversation.id in ids}
    n_full = BAKEOFF_SIZE
    results: dict[str, Any] = {}
    for v in manifest["variants"]:
        scores, usage, costs, latencies, errors, finishes = [], defaultdict(int), [], [], [], defaultdict(int)
        for cid in ids:
            path = out_dir / "outputs" / _slug(v) / f"{cid}.json"
            if not path.exists():
                continue
            rec = json.loads(path.read_text())
            ac = gold[cid]
            menu = load_menu(ac.conversation.business_id).extractor_view()
            if "error" in rec:
                errors.append(rec["error"][:200])
                scores.append(score_conversation(ac, None, menu))
                continue
            resp = ChatResponse.model_validate(rec["response"])
            result = to_result(resp)
            finishes[resp.finish_reason] += 1
            if result.output is None:
                errors.append(f"{cid}: {(result.error or '')[:200]}")
            scores.append(score_conversation(ac, result.output, menu))
            for k, val in resp.usage.model_dump().items():
                usage[k] += val
            costs.append(resp.cost_micros)
            latencies.append(resp.latency_ms)
        m = aggregate(scores) if scores else {}
        done = len(costs)
        mean_cost = sum(costs) / done if done else 0
        results[v] = {
            **m,
            "calls_answered": done,
            "provider_errors": [e for e in errors if not e.startswith(tuple(ids))],
            "invalid_examples": [e for e in errors if e.startswith(tuple(ids))][:5],
            "finish_reasons": dict(finishes),
            "tokens": dict(usage),
            "tokens_per_conversation": {k: round(val / done, 1) for k, val in usage.items()} if done else {},
            "cost_micros": sum(costs),
            "cost_per_1000_conversations_usd": round(mean_cost * 1000 / 1e6, 4),
            f"projected_cost_{n_full}_conversations_usd": round(mean_cost * n_full / 1e6, 4),
            "latency_ms_p50": round(statistics.median(latencies)) if latencies else None,
            "latency_ms_p95": round(statistics.quantiles(latencies, n=20)[-1])
            if len(latencies) >= 2
            else None,
        }
    (out_dir / "metrics.json").write_text(json.dumps(results, indent=2) + "\n")
    _write_report(out_dir, manifest, results)
    return results


def _write_report(out_dir: Path, manifest: dict, results: dict) -> None:
    n = len(manifest["data"]["conversation_ids"])
    lines = [
        f"# Teacher bake-off: {manifest['run_id']}",
        "",
        f"{manifest['mode']} conversations from dev (Source A, Claude-written), prompt `{manifest['prompt_version']}`, "
        f"schema `{manifest['schema_version']}`, commit `{manifest['git_commit']}`, cache `{manifest['cache_mode']}`. "
        f"Actual cost of this run: ${manifest.get('actual_cost_micros', 0) / 1e6:.4f} "
        f"(estimate ${manifest['estimate_micros'] / 1e6:.4f}).",
        "",
    ]
    if n < 20:
        lines += [
            f"**Pilot: {n} conversations is far too few to compare accuracy.** Use it for validity, tokens, cost "
            "and latency; accuracy differences here are noise.",
            "",
        ]
    lines += [
        "| Variant | JSON valid | Items found / extra / missed (of gold) | Item F1 | Fully correct (95% CI) "
        "| Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for v, r in results.items():
        t = r.get("tokens_per_conversation", {})
        it, ci = r.get("item", {}), r.get("exact_match_ci95")
        ci_text = f" ({_pct(ci[0])}–{_pct(ci[1])})" if ci else ""
        lines.append(
            f"| `{v}` | {r.get('json_valid', 0)}/{r.get('conversations', 0)} "
            f"| {it.get('tp', 0)} / {it.get('fp', 0)} / {it.get('fn', 0)} (of {it.get('gold_items', 0)}) "
            f"| {_pct(it.get('f1'))} | {r.get('exact_match', 0)}/{r.get('conversations', 0)}{ci_text} "
            f"| {r.get('grounding', {}).get('conversations_with_issues', '—')} "
            f"| {t.get('input_tokens', '—')} | {t.get('output_tokens', '—')} | {t.get('reasoning_tokens', '—')} "
            f"| ${r['cost_micros'] / 1e6:.4f} | ${r['cost_per_1000_conversations_usd']:.2f} "
            f"| {r.get('latency_ms_p50', '—')} |"
        )
    total = sum(r["cost_micros"] for r in results.values())
    lines.append(f"| **all variants** | | | | | | | | | **${total / 1e6:.4f}** | | |")
    lines += [
        "",
        "Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.",
    ]
    problems = {v: r for v, r in results.items() if r.get("provider_errors") or r.get("invalid_examples")}
    if problems:
        lines += ["", "## Errors and invalid outputs", ""]
        for v, r in problems.items():
            for e in r.get("provider_errors", []) + r.get("invalid_examples", []):
                lines.append(f"- `{v}`: {e}")
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")


def write_summary() -> Path:
    """One file for the case study / dashboard: every saved run's manifest facts and per-variant metrics,
    read from the run folders (never recomputed from memory). Rebuild after each run."""
    runs = []
    for d in sorted((RUNS / EXPERIMENT).iterdir()):
        if not (d / "manifest.json").exists():
            continue
        m = json.loads((d / "manifest.json").read_text())
        metrics = report(d)
        runs.append(
            {
                "run_id": m["run_id"],
                "path": str(d.relative_to(ROOT)),
                "mode": m["mode"],
                "started_at": m["started_at"],
                "git_commit": m["git_commit"],
                "prompt_version": m["prompt_version"],
                "schema_version": m["schema_version"],
                "data": {k: m["data"][k] for k in ("split", "source", "selection") if k in m["data"]},
                "conversations": len(m["data"]["conversation_ids"]),
                "estimate_usd": m["estimate_micros"] / 1e6,
                "actual_cost_usd": m.get("actual_cost_micros", 0) / 1e6,
                "variants": {v: {"settings": m["variants"][v], **metrics.get(v, {})} for v in m["variants"]},
            }
        )
    out = RUNS / EXPERIMENT / "summary.json"
    out.write_text(json.dumps({"experiment": EXPERIMENT, "runs": runs}, indent=2) + "\n")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pilot", type=int, help="only the first N conversations of the bake-off set")
    ap.add_argument(
        "--set",
        choices=["bakeoff", "remaining", "all"],
        default="bakeoff",
        help="bakeoff: the 40-conversation bake-off set; remaining: dev outside it; all: every dev conversation",
    )
    ap.add_argument(
        "--summary", action="store_true", help="write runs/teacher-bakeoff/summary.json, no calls"
    )
    ap.add_argument("--skip", type=int, default=0, help="skip the first N conversations of the bake-off set")
    ap.add_argument("--variants", help="comma-separated config ids (default: all in config/models.json)")
    ap.add_argument("--yes", action="store_true", help="make the calls")
    ap.add_argument("--allow-over-2", action="store_true", help="run even if the estimate is over $2")
    ap.add_argument("--max-cost", type=float, help="stop when actual spend passes this many USD")
    ap.add_argument("--report", type=Path, help="rebuild metrics + report for a saved run, no calls")
    args = ap.parse_args(argv)
    if args.report:
        report(args.report)
        print((args.report / "report.md").read_text())
        return 0
    if args.summary:
        path = write_summary()
        print(f"Wrote {path.relative_to(ROOT)}")
        return 0
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
