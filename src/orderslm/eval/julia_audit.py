"""Label audit by Julia-1 on Kaggle (spec §11d, docs/KAGGLE.md job A).

Julia-1 needs torch ≥ 2.6, which this Intel Mac can't install, so it runs as a private Kaggle script kernel
(`kaggle/julia-audit/`). The requests are the label audit's own (`label_audit.build_request`: the identical wording
Jev and OpenAI Decisions got); this module turns them into Julia-1's named-question format, and the kernel's answers
back into `DecisionResponse`s saved under `responses/julia-1/`, so `label_audit.report` scores them like any provider.

    make julia-audit ARGS="export --set dev --limit 1"     # stage requests + a run dir (1-chat timing test)
    make kaggle-push JOB=julia-audit                       # upload the requests, start the kernel
    make kaggle-pull JOB=julia-audit                       # fetch the kernel's output when it's done
    make julia-audit ARGS="import runs/label-audit/<id>"   # responses + metrics + report from the output

The gold answers (expected intents, planted-mistake kinds) never leave this Mac: only requests go to Kaggle.
"""

import argparse
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.core.plant import PLANT_VERSION
from orderslm.interfaces.decision import (
    Answer,
    DecisionRequest,
    DecisionResponse,
    QuestionType,
    Usage,
    validate_response,
)
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit

from . import label_audit

PROVIDER = "julia-1"
MODEL = "SupersonicLabs/Julia-1"
REVISION = "a85b127321d580d65176c89ced8273f305745d85"  # docs/PROVIDERS.md
JOB_DIR = ROOT / "kaggle" / "julia-audit"
STAGE = JOB_DIR / "upload"  # gitignored: what `make kaggle-push` uploads as the private dataset
KAGGLE_USER = "JReyes33"
DATASET = f"{KAGGLE_USER}/orderslm-julia-audit"


def to_julia(request: DecisionRequest) -> dict[str, Any]:
    """Julia-1's `predict(state=..., questions=...)` arguments; same mapping as Jev's wire format (hosted.py)."""
    questions: dict[str, Any] = {}
    for q in request.questions:
        if q.type is QuestionType.choice:
            questions[q.name] = {
                "type": "choice",
                "instructions": q.prompt,
                "criteria": {o.id: o.description for o in q.options},
            }
        elif q.type is QuestionType.boolean:
            questions[q.name] = {"type": "noul", "instructions": q.prompt}
        else:
            raise ValueError(f"{q.name}: score questions are not used by the label audit")
    return {"id": request.request_id, "state": request.input, "questions": questions}


def from_julia(request: DecisionRequest, rec: dict[str, Any]) -> DecisionResponse:
    """One kernel output line → DecisionResponse. Julia-1 has no confidence field: only softmax probabilities."""
    answers: dict[str, Answer] = {}
    for q in request.questions:
        a = rec["answers"][q.name]
        if q.type is QuestionType.choice:
            answers[q.name] = Answer(
                name=q.name, type=q.type, choice=a["choice"], probabilities=a["probabilities"]
            )
        else:
            p = float(a["noul"])
            answers[q.name] = Answer(
                name=q.name,
                type=QuestionType.boolean,
                boolean=p >= 0.5,
                probabilities={"true": p, "false": 1 - p},
            )
    resp = DecisionResponse(
        provider=PROVIDER,
        model=f"{MODEL}@{REVISION[:8]}",
        answers=answers,
        usage=Usage(input_tokens=rec.get("input_tokens", 0)),
        latency_ms=rec["latency_ms"],
    )
    validate_response(request, resp)
    return resp


# ---------------------------------------------------------------- sanity check (is our setup right?)

# Made up for this check (not from dev, test or PIZZA). The model card's own example, then clear one-message cases
# asked two ways: the message alone, and in the audit's chat format (INTENT_PROMPT); then plain yes/no order checks.
_ONE_MESSAGE = [
    ("can i get 2 large pepperoni pizzas for delivery", "PLACE_ORDER"),
    ("actually cancel the whole order, sorry", "CANCEL_ORDER"),
    ("do you have any vegan options?", "MENU_QUESTION"),
    ("what time do you close tonight?", "DELIVERY_QUESTION"),
    ("can i pay with apple pay?", "PAYMENT_QUESTION"),
    ("i already sent the money on venmo", "PAYMENT_CLAIM"),
    ("where is my order? it's been an hour", "ORDER_STATUS"),
    ("my burger came cold and the fries were missing", "ORDER_PROBLEM"),
    ("i want my money back for that order", "REFUND_REQUEST"),
    ("can i talk to a real person please", "HUMAN_REQUEST"),
    ("thanks so much, have a good one!", "SMALL_TALK"),
    ("can you help me with my math homework", "OUT_OF_SCOPE"),
]
_ORDER_CHECKS = [
    (
        "2 large pepperoni pizzas for delivery please",
        "2 × Pepperoni Pizza (Large)\nFulfillment: delivery",
        True,
    ),
    (
        "2 large pepperoni pizzas for delivery please",
        "1 × Margherita Pizza (Small)\nFulfillment: pickup",
        False,
    ),
    ("one cheeseburger, no pickles, pickup", "1 × Cheeseburger: no Pickles\nFulfillment: pickup", True),
    ("one cheeseburger, no pickles, pickup", "3 × Cheeseburger\nFulfillment: delivery", False),
]


def sanity_jobs() -> list[dict[str, Any]]:
    from orderslm.interfaces.decision import Option, Question

    def job(jid: str, state: str, q: Question, expected: Any) -> dict[str, Any]:
        req = DecisionRequest(request_id=jid, input=state, questions=[q], prompt_version="julia-sanity@0.1")
        return {"id": jid, "kind": "sanity", "request": req, "expected": {q.name: expected}}

    team = Question(
        name="team",
        type=QuestionType.choice,
        prompt="Which team should handle this request?",
        options=[
            Option(id="billing", description="Billing and payment disputes"),
            Option(id="shipping", description="Shipping and delivery"),
            Option(id="access", description="Account access and login"),
        ],
    )
    jobs = [job("card-example", "I was charged twice for the same order.", team, "billing")]
    for k, (msg, label) in enumerate(_ONE_MESSAGE):
        plain = Question(
            name="intent",
            type=QuestionType.choice,
            prompt="What does this customer message do?",
            options=label_audit.LABEL_OPTIONS,
        )
        jobs.append(job(f"plain-{k:02d}", msg, plain, label))
        chat = Question(
            name="intent_m0",
            type=QuestionType.choice,
            prompt=label_audit.INTENT_PROMPT.format(i=0),
            options=label_audit.LABEL_OPTIONS,
        )
        state = f"A text chat between a customer and a restaurant:\n[0] customer: {msg}"
        jobs.append(job(f"chat-{k:02d}", state, chat, label))
    for k, (msg, record, ok) in enumerate(_ORDER_CHECKS):
        state = f"A text chat between a customer and a restaurant:\n[0] customer: {msg}\n\nThe order as recorded:\n{record}"
        for name, prompt in [
            ("simple", "Does the recorded order match what the customer asked for?"),
            ("audit", label_audit.ORDER_PROMPT),
        ]:
            q = Question(name="order_ok", type=QuestionType.boolean, prompt=prompt)
            jobs.append(job(f"order-{k}-{name}", state, q, ok))
    return jobs


def sanity_report(run_dir: Path, jobs: list[dict[str, Any]]) -> dict[str, Any]:
    rows, groups = [], {}
    for j in jobs:
        rec = json.loads((run_dir / "responses" / PROVIDER / f"{j['id']}.json").read_text())
        ((name, expected),) = j["expected"].items()
        if "error" in rec:
            got, p, ok = "error", None, False
        else:
            a = DecisionResponse.model_validate(rec["response"]).answers[name]
            got = a.choice if a.type is QuestionType.choice else a.boolean
            p = (a.probabilities or {}).get(str(expected).lower() if isinstance(expected, bool) else expected)
            ok = got == expected
        jid = j["id"]
        group = "order-" + jid.rsplit("-", 1)[1] if jid.startswith("order") else jid.split("-")[0]
        g = groups.setdefault(group, [0, 0])
        g[0] += ok
        g[1] += 1
        rows.append({"id": j["id"], "expected": expected, "got": got, "p_expected": p, "ok": ok})
    summary = {"groups": {k: {"right": r, "of": n} for k, (r, n) in groups.items()}, "cases": rows}
    (run_dir / "metrics.json").write_text(json.dumps(summary, indent=2) + "\n")
    L = ["# Julia-1 sanity check", "", "| group | right |", "|---|---|"]
    L += [f"| {k} | {r}/{n} |" for k, (r, n) in groups.items()]
    L += ["", "| case | expected | got | P(expected) |", "|---|---|---|---|"]
    L += [
        f"| {r['id']} | {r['expected']} | {r['got']} | {'' if r['p_expected'] is None else round(r['p_expected'], 3)} |"
        for r in rows
    ]
    (run_dir / "report.md").write_text("\n".join(L) + "\n")
    return summary


def _jobs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    if manifest["set"] == "sanity":
        return sanity_jobs()
    jobs = label_audit._load_jobs(manifest)
    keep = set(manifest["job_ids"])
    return [j for j in jobs if j["id"] in keep]


def export(args: argparse.Namespace) -> Path:
    if args.set == "sanity":
        jobs = sanity_jobs()
    elif args.set == "dev":
        jobs = label_audit.dev_jobs()
    else:
        jobs = label_audit.train_jobs(args.batches.split(","))
    if args.limit:
        jobs = jobs[: args.limit]
    started = datetime.now(UTC)
    tag = f"{args.set}-limit{args.limit}" if args.limit else args.set
    out_dir = RUNS / label_audit.EXPERIMENT / f"{started:%Y%m%dT%H%M%SZ}-julia-{tag}"
    manifest = {
        "experiment": label_audit.EXPERIMENT,
        "audit_version": label_audit.AUDIT_VERSION,
        "plant_version": PLANT_VERSION,
        "set": args.set,
        "batches": args.batches.split(",") if args.set == "train" else None,
        "providers": [PROVIDER],
        "provider_config": {
            PROVIDER: {
                "model": MODEL,
                "revision": REVISION,
                "runtime": "Kaggle script kernel, CPU (kaggle/julia-audit/run.py)",
                "max_length": 8192,
                "strict_encoding": True,
            }
        },
        "exported_at": started.isoformat(),
        "git_commit": git_commit(),
        "job_ids": [j["id"] for j in jobs],
        "kaggle_dataset": DATASET,
        "cost_micros": 0,
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    stage(out_dir, [to_julia(j["request"]) for j in jobs])
    return out_dir


def stage(out_dir: Path, julia_requests: list[dict[str, Any]]) -> None:
    """Write the requests + run.json + dataset metadata that `make kaggle-push JOB=julia-audit` uploads."""
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    with (STAGE / "requests.jsonl").open("w") as f:
        for r in julia_requests:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    run = {"run_dir": out_dir.name, "requests": len(julia_requests)}
    (STAGE / "run.json").write_text(json.dumps(run) + "\n")
    (STAGE / "dataset-metadata.json").write_text(
        json.dumps(
            {"title": "orderslm-julia-audit", "id": DATASET, "licenses": [{"name": "unknown"}]}, indent=2
        )
        + "\n"
    )
    questions = sum(len(r["questions"]) for r in julia_requests)
    print(f"Staged {len(julia_requests)} requests ({questions} questions) in {STAGE.relative_to(ROOT)}/")
    print(f"Run dir: {out_dir.relative_to(ROOT)}/")


def import_(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Kernel output (outputs.jsonl, env.json, log) → responses/julia-1/*.json, then the usual report."""
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text()) if (output_dir / "env.json").exists() else {}
    if env and env.get("run_dir") != run_dir.name:
        raise SystemExit(f"kernel output is for {env.get('run_dir')}, not {run_dir.name}")
    requests_jobs = _jobs(manifest)
    requests = {j["id"]: j["request"] for j in requests_jobs}
    resp_dir = run_dir / "responses" / PROVIDER
    resp_dir.mkdir(parents=True, exist_ok=True)
    seen = set()
    for line in (output_dir / "outputs.jsonl").read_text().splitlines():
        rec = json.loads(line)
        rid = rec["id"]
        out: dict[str, Any] = {"id": rid}
        if "error" in rec:
            out["error"] = rec["error"]
        else:
            out["response"] = from_julia(requests[rid], rec).model_dump(mode="json")
        (resp_dir / f"{rid}.json").write_text(json.dumps(out, indent=1) + "\n")
        seen.add(rid)
    kernel = run_dir / "kernel"
    kernel.mkdir(exist_ok=True)
    for name in ("env.json", "outputs.jsonl", "run.log"):
        if (output_dir / name).exists():
            shutil.copy(output_dir / name, kernel / name)
    manifest.update(
        imported_at=datetime.now(UTC).isoformat(),
        answered=len(seen),
        missing=sorted(set(requests) - seen),
        kernel_env=env,
    )
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if manifest["set"] == "sanity":
        metrics = sanity_report(run_dir, list(requests_jobs))
    else:
        metrics = label_audit.report(run_dir)
    print((run_dir / "report.md").read_text())
    return metrics


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--set", choices=["sanity", "dev", "train"], default="dev")
    e.add_argument("--batches", default="p3,b1,m1")
    e.add_argument("--limit", type=int)
    i = sub.add_parser("import")
    i.add_argument("run_dir", type=Path)
    i.add_argument("--output", type=Path, default=JOB_DIR / "output")
    args = ap.parse_args(argv)
    if args.cmd == "export":
        export(args)
    else:
        import_(args.run_dir, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
