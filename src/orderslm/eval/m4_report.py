"""M4 data report: every drop, repair, relabel, flag and catch rate, rebuilt from the saved run folders.

    make m4-report      # writes runs/m4-report/m4_report.json (dashboard / chart data) and M4_REPORT.md

Julian (2026-10-15/16): the case study shows every option and every drop with its reason, so nothing here is typed
by hand except the hand-check results of the audit flags, which are read from runs/label-audit/*/review.json.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from orderslm.paths import ROOT, RUNS

SYNTH = RUNS / "synth"
BATCHES = {"p1": "mini-pilot 1", "p2": "mini-pilot 2", "p3": "pilot", "b1": "bulk", "m1": "mega-menu"}
TRAINING_BATCHES = ("p3", "b1", "m1")


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []


def _reason(text: str) -> str:
    """'check_failed: EVIDENCE_NOT_FOUND items[L2]; ...' → 'check_failed: EVIDENCE_NOT_FOUND'."""
    head, _, rest = text.partition(":")
    if head == "check_failed":
        codes = sorted({part.strip().split(" ")[0] for part in rest.split(";") if part.strip()})
        return "check_failed: " + "+".join(codes)
    return head.split(" ")[0]


def batches() -> dict[str, Any]:
    out = {}
    for b, what in BATCHES.items():
        d = SYNTH / b
        if not (d / "summary.json").exists():
            continue
        summary = json.loads((d / "summary.json").read_text())
        labels = _jsonl(d / "labels.jsonl")
        per_gen = {}
        for g, row in summary["by_generator"].items():
            gen_drops = [x for x in _jsonl(d / "gen_drops.jsonl") if x["generator"] == g]
            label_drops = [x for x in _jsonl(d / "label_drops.jsonl") if x["generator"] == g]
            per_gen[g] = {
                "cards": row["cards"],
                "generated": row["generated"],
                "kept": row["kept"],
                "generation_drops": dict(Counter(_reason(x["reason"]) for x in gen_drops)),
                "repairs": row["repairs"],
                "labeled": row["labeled"],
                "label_drops": dict(Counter(_reason(x["reason"]) for x in label_drops)),
                "card_agreement": row["card_agreement"],
                "generation_cost_usd": row["generation_usage"]["cost_micros"] / 1e6,
                "label_cost_usd_current_labels": row["label_usage"]["cost_micros"] / 1e6,
            }
        relabels = {
            f.stem.removeprefix("relabel_").removesuffix("_ids"): len(json.loads(f.read_text()))
            for f in sorted(d.glob("relabel_*_ids.json"))
        }
        out[b] = {
            "what": what,
            "by_generator": per_gen,
            "label_prompt_versions": dict(Counter(x["label_prompt_version"] for x in labels)),
            "relabeled_chats": relabels,
            "calls_cost_usd": round(
                sum(
                    json.loads(f.read_text()).get("actual_cost_micros", 0)
                    for f in (d / "calls").glob("*.json")
                )
                / 1e6,
                6,
            ),
        }
    return out


def training_set() -> dict[str, Any]:
    excluded = (
        json.loads((SYNTH / "excluded.json").read_text())["excluded"]
        if (SYNTH / "excluded.json").exists()
        else []
    )
    ex = {x["id"] for x in excluded}
    counts: dict[str, Any] = {
        "single_menu": 0,
        "mega_menu": 0,
        "by_generator": Counter(),
        "intents": Counter(),
    }
    for b in TRAINING_BATCHES:
        for r in _jsonl(SYNTH / b / "labels.jsonl"):
            if r["conversation_id"] in ex:
                continue
            counts["mega_menu" if b == "m1" else "single_menu"] += 1
            for i in r["intents"]:
                counts["intents"][i["primary"]] += 1
    gens = Counter()
    for b in TRAINING_BATCHES:
        convs = {
            json.loads(x)["card_id"]: json.loads(x)["generator"]
            for x in (SYNTH / b / "conversations.jsonl").read_text().splitlines()
        }
        for r in _jsonl(SYNTH / b / "labels.jsonl"):
            if r["conversation_id"] not in ex:
                gens[convs[r["conversation_id"]]] += 1
    counts["by_generator"] = dict(gens)
    counts["intents"] = dict(counts["intents"].most_common())
    counts["excluded"] = excluded
    return counts


def label_prompt_history() -> list[dict[str, Any]]:
    rows = []
    for d in sorted((RUNS / "label-dev").glob("*/")):
        if not (d / "metrics.json").exists():
            continue
        m = json.loads((d / "metrics.json").read_text())
        o, i = m["order"], m["intent"]
        rows.append(
            {
                "run": str(d.relative_to(ROOT)),
                "label_prompt": m["label_prompt_version"],
                "orders_fully_correct": o["exact_match"],
                "orders": o["conversations"],
                "items_found": o["item"]["tp"],
                "items_extra": o["item"]["fp"],
                "items_missed": o["item"]["fn"],
                "intents_correct": i["primary_correct"],
                "intent_messages": i["customer_messages"],
                "labels_dropped_by_checks": m["synthetic_pipeline_drops"],
                "cost_usd": (m.get("cost_micros") or 0) / 1e6,
            }
        )
    return rows


def audits() -> list[dict[str, Any]]:
    rows = []
    for d in sorted((RUNS / "label-audit").glob("*/")):
        if not (d / "metrics.json").exists():
            continue
        manifest = json.loads((d / "manifest.json").read_text())
        metrics = json.loads((d / "metrics.json").read_text())
        row: dict[str, Any] = {
            "run": str(d.relative_to(ROOT)),
            "set": manifest["set"],
            "audit_version": manifest["audit_version"],
            "cost_usd": manifest.get("actual_cost_micros", 0) / 1e6,
            "providers": {},
        }
        for p, m in metrics.items():
            row["providers"][p] = {
                k: m[k]
                for k in (
                    "intent_agree_primary",
                    "intent_messages",
                    "intent_agree_rate",
                    "order_flagged",
                    "orders_expected_ok",
                    "order_flag_rate",
                    "planted",
                    "planted_catch_rate",
                    "input_tokens",
                    "cost_micros",
                    "latency_p50_ms",
                    "latency_p95_ms",
                    "errors",
                )
            }
        if manifest["set"] == "dev":
            row["missed_by_all_examples"] = _missed_examples(d, manifest["providers"])
        if manifest["set"] == "train" and (d / "flags.jsonl").exists():
            flags = _jsonl(d / "flags.jsonl")
            row["chats_flagged_by_any"] = len(flags)
            row["chats_flagged_by_all"] = sum(
                len(f["flagged_by"]) == len(manifest["providers"]) for f in flags
            )
        if (d / "review.json").exists():
            row["hand_check"] = json.loads((d / "review.json").read_text())
        rows.append(row)
    return rows


def _missed_examples(d: Path, providers: list[str], per_type: int = 3) -> dict[str, list[str]]:
    """Planted copies that every provider judged matching, per mistake type (ids; the run folder has the texts)."""
    by_type: dict[str, list[str]] = defaultdict(list)
    files = sorted((d / "responses" / providers[0]).glob("*--*.json"))
    for f in files:
        ok = []
        for p in providers:
            rec = json.loads((d / "responses" / p / f.name).read_text())
            ok.append("response" in rec and rec["response"]["answers"]["order_ok"]["boolean"])
        if all(ok):
            mistake = f.stem.split("--", 1)[1].replace("-", "_")
            if len(by_type[mistake]) < per_type:
                by_type[mistake].append(f.stem)
    return dict(by_type)


def build() -> dict[str, Any]:
    return {
        "batches": batches(),
        "training_set": training_set(),
        "label_prompt_on_dev": label_prompt_history(),
        "label_audits": audits(),
    }


def render(r: dict[str, Any]) -> str:
    L = [
        "# M4 data report",
        "",
        "Generated by `make m4-report` from the saved run folders. Dev numbers are tuning results,"
        " not held out.",
        "",
        "## Drops and repairs per batch and generator",
        "",
    ]
    L += [
        "| batch | generator | kept / generated | generation drops | repairs | labeled | label drops | card agrees |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for b, row in r["batches"].items():
        for g, x in row["by_generator"].items():
            ca = x["card_agreement"]
            L.append(
                f"| {b} ({row['what']}) | {g.split('/')[1]} | {x['kept']}/{x['generated']} | "
                f"{', '.join(f'{k} {v}' for k, v in x['generation_drops'].items()) or '0'} | "
                f"{', '.join(f'{k} {v}' for k, v in x['repairs'].items()) or '0'} | {x['labeled']} | "
                f"{', '.join(f'{k} {v}' for k, v in x['label_drops'].items()) or '0'} | {ca['all_agree']}/{ca['labeled']} |"
            )
    L += ["", "Relabels and label versions:", ""]
    for b, row in r["batches"].items():
        if row["relabeled_chats"]:
            L.append(f"- {b}: relabeled {row['relabeled_chats']}; labels now {row['label_prompt_versions']}")
    t = r["training_set"]
    L += [
        "",
        "## Training set",
        "",
        f"- Single-menu chats: {t['single_menu']}; mega-menu: {t['mega_menu']}",
        f"- By generator: {t['by_generator']}",
        f"- Excluded: {[x['id'] + ' (' + x['reason'] + ')' for x in t['excluded']]}",
        f"- Intents (primary): {t['intents']}",
        "",
        "## Label prompt on dev (reviewed gold)",
        "",
        "| label prompt | orders fully correct | items found/extra/missed | intents correct | dropped by checks | cost |",
        "|---|---|---|---|---|---|",
    ]
    for x in r["label_prompt_on_dev"]:
        L.append(
            f"| {x['label_prompt']} | {x['orders_fully_correct']}/{x['orders']} | {x['items_found']}/{x['items_extra']}/"
            f"{x['items_missed']} | {x['intents_correct']}/{x['intent_messages']} | {x['labels_dropped_by_checks'] or 0} | "
            f"${x['cost_usd']:.4f} |"
        )
    L += ["", "## Label audits (Jev, OpenAI Decisions)", ""]
    for a in r["label_audits"]:
        L.append(f"### {a['set']} · {a['audit_version']} · `{a['run']}` · ${a['cost_usd']:.4f}")
        for p, m in a["providers"].items():
            line = (
                f"- {p}: intents {m['intent_agree_primary']}/{m['intent_messages']}; orders judged not matching "
                f"{m['order_flagged']}/{m['orders_expected_ok']}"
            )
            if m["planted"]:
                line += (
                    f"; planted caught {m['planted_catch_rate']} ("
                    + ", ".join(f"{k} {v['caught']}/{v['of']}" for k, v in m["planted"].items())
                    + ")"
                )
            L.append(line + f"; p50 {m['latency_p50_ms']} ms")
        if a.get("missed_by_all_examples"):
            L.append(f"- Missed by every provider (examples): {a['missed_by_all_examples']}")
        if "chats_flagged_by_any" in a:
            L.append(
                f"- Chats flagged by any provider: {a['chats_flagged_by_any']}; by all: {a['chats_flagged_by_all']}"
            )
        if a.get("hand_check"):
            L.append(f"- Hand check: {a['hand_check']}")
        L.append("")
    return "\n".join(L) + "\n"


def main() -> int:
    report = build()
    out = RUNS / "m4-report"
    out.mkdir(parents=True, exist_ok=True)
    (out / "m4_report.json").write_text(json.dumps(report, indent=2) + "\n")
    (out / "M4_REPORT.md").write_text(render(report))
    print(f"Wrote {(out / 'm4_report.json').relative_to(ROOT)} and M4_REPORT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
