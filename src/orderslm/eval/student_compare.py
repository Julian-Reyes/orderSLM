"""M6 students compared on the same requests, paired (docs/AGENTDESK_REUSE.md row 9: paired tests on the same items).

Every student answered the same requests of one split (dev: 268 requests, 91 chats; fresh: 278, 90), so each
difference is measured on identical items. Students may differ in training data (v0.1 vs v0.2 is what M6 measures);
prompt, scorer and finalize versions must match.

- **fully correct orders** (one per chat, chats independent): discordant chats + exact McNemar p-value, Holm-adjusted
  over the pairs compared;
- **intents, invalid answers, item F1, fully correct orders:** difference A − B with a 95% paired bootstrap interval
  over chats (resample the 91 chats with replacement, both students on the same resample). Messages in one chat are
  not independent, so intents get no per-message test; the chat-level bootstrap carries that.

Reads `intent_rows.jsonl` + `order_rows.jsonl` of each `runs/student-dev/<id>/` (rebuild older runs with
`make student-dev ARGS="report …"`). Dev numbers are tuning numbers; fresh numbers measure the dev-based fixes.

    make student-compare ARGS="runs/student-dev/<a> runs/student-dev/<b> [...]"   # → runs/student-compare/<time>/
"""

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict
from datetime import UTC, datetime
from itertools import combinations
from pathlib import Path
from typing import Any

from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit

from .stats import holm, mcnemar_exact, percentile_interval

EXPERIMENT = "student-compare"
COMPARE_VERSION = "student-compare@0.1"
SEED = 20261025
RESAMPLES = 10_000
METRICS = ("intent_accuracy", "invalid_rate", "item_f1", "exact_rate")


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def load_run(run_dir: Path) -> dict[str, Any]:
    """Per-chat counts of one student's dev run: messages, intents right, invalid answers, exact, tp/fp/fn."""
    if not (run_dir / "order_rows.jsonl").exists():
        raise SystemExit(
            f'{run_dir}: no order_rows.jsonl; run `make student-dev ARGS="report {run_dir}"` first'
        )
    metrics = json.loads((run_dir / "metrics.json").read_text())
    manifest = json.loads((run_dir / "manifest.json").read_text())
    chats: dict[str, dict[str, int]] = defaultdict(lambda: dict.fromkeys(("msgs", "ok", "invalid"), 0))
    messages = {}
    for r in _read_jsonl(run_dir / "intent_rows.jsonl"):
        c = chats[r["conversation_id"]]
        c["msgs"] += 1
        c["ok"] += r["primary_ok"]
        c["invalid"] += r["pred"] is None
        messages[(r["conversation_id"], r["message_index"])] = r["primary_ok"]
    orders = {r["conversation_id"]: r for r in _read_jsonl(run_dir / "order_rows.jsonl")}
    if set(orders) != set(chats):
        raise SystemExit(f"{run_dir}: intent and order rows cover different chats")
    for cid, o in orders.items():
        chats[cid] |= {"exact": int(o["exact"]), "tp": o["tp"], "fp": o["fp"], "fn": o["fn"]}
    return {
        "student": metrics["student"],
        "run_dir": str(run_dir.resolve().relative_to(ROOT)),
        "split": manifest.get("split", "dev"),
        "versions": {
            k: metrics[k] for k in ("prompt_version", "data_version", "scorer_version", "finalize_version")
        },
        "outputs_sha256": hashlib.sha256((run_dir / "outputs.jsonl").read_bytes()).hexdigest(),
        "chats": dict(chats),
        "messages": messages,
    }


def summarize(chats: dict[str, dict[str, int]], ids: list[str]) -> dict[str, float]:
    """The four metrics over a list of chat ids (repeats count again, as in a bootstrap resample)."""
    t = dict.fromkeys(("msgs", "ok", "invalid", "exact", "tp", "fp", "fn"), 0)
    for cid in ids:
        for k in t:
            t[k] += chats[cid][k]
    f1_den = 2 * t["tp"] + t["fp"] + t["fn"]
    return {
        "intent_accuracy": t["ok"] / t["msgs"],
        "invalid_rate": t["invalid"] / t["msgs"],
        "item_f1": 2 * t["tp"] / f1_den if f1_den else 1.0,
        "exact_rate": t["exact"] / len(ids),
    }


def _same_setup(versions: dict[str, str]) -> dict[str, str]:
    """The versions two compared runs must share: training data may differ (that is a compared variable)."""
    return {k: v for k, v in versions.items() if k != "data_version"}


def compare(runs: list[dict[str, Any]], resamples: int = RESAMPLES, seed: int = SEED) -> dict[str, Any]:
    ids = sorted(runs[0]["chats"])
    for r in runs[1:]:
        if set(r["messages"]) != set(runs[0]["messages"]):
            raise SystemExit(f"{r['student']} answered different messages than {runs[0]['student']}")
        if _same_setup(r["versions"]) != _same_setup(runs[0]["versions"]):
            raise SystemExit(f"{r['student']} versions {r['versions']} differ from {runs[0]['versions']}")
    point = {r["student"]: summarize(r["chats"], ids) for r in runs}
    rng = random.Random(seed)
    draws: dict[str, list[dict[str, float]]] = {r["student"]: [] for r in runs}
    for _ in range(resamples):
        sample = rng.choices(ids, k=len(ids))
        for r in runs:
            draws[r["student"]].append(summarize(r["chats"], sample))
    pairs = []
    for a, b in combinations(runs, 2):
        na, nb = a["student"], b["student"]
        msg = list(a["messages"])
        diffs = {}
        for m in METRICS:
            reps = [x[m] - y[m] for x, y in zip(draws[na], draws[nb], strict=True)]
            lo, hi = percentile_interval(reps)
            diffs[m] = {
                "a_minus_b": point[na][m] - point[nb][m],
                "ci95": [lo, hi],
                "ci_excludes_0": lo > 0 or hi < 0,
            }
        a_only = sum(a["chats"][c]["exact"] and not b["chats"][c]["exact"] for c in ids)
        b_only = sum(b["chats"][c]["exact"] and not a["chats"][c]["exact"] for c in ids)
        pairs.append(
            {
                "a": na,
                "b": nb,
                "intent_messages": {
                    "only_a_right": sum(a["messages"][k] and not b["messages"][k] for k in msg),
                    "only_b_right": sum(b["messages"][k] and not a["messages"][k] for k in msg),
                },
                "exact_chats": {
                    "only_a_right": a_only,
                    "only_b_right": b_only,
                    "mcnemar_p": mcnemar_exact(a_only, b_only),
                },
                "differences": diffs,
            }
        )
    for p, adj in zip(pairs, holm([p["exact_chats"]["mcnemar_p"] for p in pairs]), strict=True):
        p["exact_chats"]["mcnemar_p_holm"] = adj
    return {
        "compare_version": COMPARE_VERSION,
        "split": runs[0].get("split", "dev"),
        "chats": len(ids),
        "messages": len(runs[0]["messages"]),
        "resamples": resamples,
        "seed": seed,
        "students": {r["student"]: point[r["student"]] for r in runs},
        "pairs": pairs,
    }


def _pp(x: float) -> str:
    return f"{100 * x:+.1f}"


def write_report(out: Path, c: dict[str, Any], runs: list[dict[str, Any]]) -> None:
    lines = [
        f"# M6 students compared on {c['split']}, paired ({c['chats']} chats, {c['messages']} customer messages)",
        "",
        "Same requests for every student. "
        + (
            "Dev numbers (tuning), not held-out results. "
            if c["split"] == "dev"
            else "Fresh chats, written after the dev-based fixes (evaluation-only). "
        )
        + "Differences are A − B in "
        f"percentage points with a 95% paired bootstrap interval over chats ({c['resamples']:,} resamples, seed "
        f"{c['seed']}); * = interval excludes 0. Fully correct orders also get an exact McNemar test on the chats where "
        "the two disagree, Holm-adjusted over the pairs.",
        "",
        "| student | intents right | invalid answers | item F1 | fully correct orders |",
        "|---|---|---|---|---|",
    ]
    for s, m in c["students"].items():
        lines.append(
            f"| {s} | {100 * m['intent_accuracy']:.1f}% | {100 * m['invalid_rate']:.1f}% | {m['item_f1']:.3f} | "
            f"{100 * m['exact_rate']:.1f}% |"
        )
    lines += [
        "",
        "| A vs B | intents (pp) | invalid answers (pp) | item F1 (pp) | fully correct orders (pp) | "
        "messages only A / only B right | chats only A / only B fully correct | McNemar p (Holm) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in c["pairs"]:
        d = p["differences"]

        def cell(m: str, d: dict = d) -> str:
            lo, hi = d[m]["ci95"]
            return f"{_pp(d[m]['a_minus_b'])} [{_pp(lo)}, {_pp(hi)}]{'*' if d[m]['ci_excludes_0'] else ''}"

        e = p["exact_chats"]
        lines.append(
            f"| {p['a']} vs {p['b']} | {cell('intent_accuracy')} | {cell('invalid_rate')} | {cell('item_f1')} | "
            f"{cell('exact_rate')} | {p['intent_messages']['only_a_right']} / {p['intent_messages']['only_b_right']} | "
            f"{e['only_a_right']} / {e['only_b_right']} | {e['mcnemar_p']:.3f} ({e['mcnemar_p_holm']:.3f}) |"
        )
    lines += ["", "Inputs:", ""] + [
        f"- `{r['student']}` ({r['versions']['data_version']}): `{r['run_dir']}`" for r in runs
    ]
    (out / "report.md").write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dirs", type=Path, nargs="+")
    args = ap.parse_args(argv)
    if len(args.run_dirs) < 2:
        raise SystemExit("compare at least two runs")
    runs = [load_run(d) for d in args.run_dirs]
    c = compare(runs)
    started = datetime.now(UTC)
    out = RUNS / EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}"
    out.mkdir(parents=True)
    (out / "compare.json").write_text(json.dumps(c, indent=2) + "\n")
    manifest = {
        "experiment": EXPERIMENT,
        "compare_version": COMPARE_VERSION,
        "inputs": [{k: r[k] for k in ("student", "run_dir", "outputs_sha256", "versions")} for r in runs],
        "created_at": started.isoformat(),
        "git_commit": git_commit(),
        "cost_usd": 0.0,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_report(out, c, runs)
    print((out / "report.md").read_text())
    print(f"→ {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
