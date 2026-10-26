"""M6 LoRA training on Kaggle (2 × T4) and dev scoring of the trained students (docs/KAGGLE.md job C). Free.

Settings agreed with Julian (2026-10-21): fla + fp16; up to 2 epochs with validation loss every half epoch, the best
checkpoint by validation loss kept; LoRA r 16 / alpha 32 / dropout 0.05 on all linear layers (attention, MLP and
the Gated DeltaNet projections); LR 2e-4 (0.8B) / 1e-4 (2B), 5% warmup, cosine decay; effective batch 8 by gradient
accumulation. Sessions: (1) 0.8B + 2B single side by side, one per T4 (the 0.8B was killed at step 147, probably
host RAM); (2) 2B mixed on T4 #0, the 0.8B resumed and then the 2B single's dev scoring on T4 #1 (the training list's
order sets the GPUs; scoring follows the last one); more sessions resume whatever paused (Kaggle's 12 h limit).

    make train ARGS="export --train qwen3.5-0.8b-single,qwen3.5-2b-single"
    make train ARGS="export --train qwen3.5-2b-mixed,qwen3.5-0.8b-single --score qwen3.5-2b-single"
    make kaggle-push JOB=m6        # (ask Julian first; secrets check)
    make kaggle-pull JOB=m6
    make train ARGS="import runs/train/<id>"

Export stages kaggle/m6/upload/ (gitignored): run.json (jobs, settings, seeds, versions), the training rows each job
needs, `last/` of any job that paused (resumed exactly), the best adapters to score, and dev requests
(`eval/student_dev.build_requests`). Import writes per job `runs/train/<id>/<job>/` (config, steps, validation
history, status, adapter sha256) and keeps the weights in gitignored `models/m6/<job>/{best,last}` (weights stay
private, docs/TERMS.md option b); score jobs land in `runs/student-dev/<id>-<job>/` and are scored there.
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.eval import student_dev
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Split
from orderslm.train.data import OUT, STUDENT_PROMPT_VERSION

EXPERIMENT = "train"
JOB_DIR = ROOT / "kaggle" / "m6"
STAGE = JOB_DIR / "upload"  # gitignored
DATASET = "JReyes33/orderslm-m6"
WEIGHTS = ROOT / "models" / "m6"  # gitignored
SEED = 20261021
DEADLINE_HOURS = (
    11.25  # stop, save and exit cleanly before Kaggle's 12 h session limit (output is kept only then)
)
MODELS = {  # same revisions as M5 and the smoke test
    "0.8b": {"repo": "Qwen/Qwen3.5-0.8B", "revision": "2fc06364715b967f1860aea9cf38778875588b17"},
    "2b": {"repo": "Qwen/Qwen3.5-2B", "revision": "15852e8c16360a2fea060d615a32b45270f8a8fc"},
}
PACKAGES = {  # as in the smoke test (runs/train-smoke/20261021T145441Z)
    "main": ["transformers==5.20.2", "peft==0.21.2", "accelerate"],
    "fla": ["fla-core==0.5.2"],
}
STUDENTS = {
    "qwen3.5-0.8b-single": {
        "model": "0.8b",
        "data": "single",
        "lr": 2e-4,
        "data_version": "student-data@0.1",
    },
    "qwen3.5-2b-single": {"model": "2b", "data": "single", "lr": 1e-4, "data_version": "student-data@0.1"},
    "qwen3.5-2b-mixed": {"model": "2b", "data": "mixed", "lr": 1e-4, "data_version": "student-data@0.1"},
    # the same three retrained on v0.2 (+ targeted t3 and hand-written t4; Julian, 2026-10-25), same settings
    "qwen3.5-0.8b-single-v2": {
        "model": "0.8b",
        "data": "single",
        "lr": 2e-4,
        "data_version": "student-data@0.2",
    },
    "qwen3.5-2b-single-v2": {"model": "2b", "data": "single", "lr": 1e-4, "data_version": "student-data@0.2"},
    "qwen3.5-2b-mixed-v2": {"model": "2b", "data": "mixed", "lr": 1e-4, "data_version": "student-data@0.2"},
}
TRAIN = {
    "lora": {"r": 16, "alpha": 32, "dropout": 0.05, "target_modules": "all-linear"},
    "epochs": 2,
    "effective_batch": 8,  # gradient accumulation, batch 1 per forward pass
    "warmup_share": 0.05,
    "schedule": "cosine",
    "eval_every_epochs": 0.5,
    "optimizer": "adamw",
    "weight_decay": 0.0,
    "max_grad_norm": 1.0,
    "checkpoint_every": 20,  # optimizer steps (~160 rows, ~10–15 min)
    "dtype": "float16",
    # v0.2 runs: rows padded to a multiple of 128 tokens, so host memory stops growing per new row length (it reached
    # 26 of 32 GB on v0.1's 2,236 mixed rows; v0.2 mixed has 2,899). Same loss: causal model, padding not scored.
    "pad_to_multiple": 128,
}
GENERATION = {"do_sample": False, "max_new_tokens": 1536}  # longest training answer 2,562 chars (~800 tokens)


def assign_gpus(train: list[str], score: list[str]) -> list[tuple[str, str, int]]:
    """(kind, name, gpu): training jobs one per GPU; a student trained this session is scored after its training on
    the same GPU; other scoring on a GPU no training uses, else after the trainings."""
    if len(train) > 2:
        raise SystemExit("at most two training jobs per session (one per T4)")
    jobs = [("train", n, g) for g, n in enumerate(train)]
    other = [n for n in score if n not in train]
    free = [g for g in (0, 1) if g >= len(train)] or [
        len(train) - 1 - i % len(train) for i in range(len(other))
    ]
    for n in score:
        gpu = train.index(n) if n in train else free[other.index(n) % len(free)]
        jobs.append(("score", n, gpu))
    return jobs


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export(args: argparse.Namespace) -> Path:
    train = [n for n in (args.train or "").split(",") if n]
    score = [n for n in (args.score or "").split(",") if n]
    score_splits = [x for x in (args.score_splits or "dev").split(",") if x]
    if not set(score_splits) <= {"dev", "fresh"}:
        raise SystemExit(f"--score-splits takes dev and/or fresh, got {score_splits}")
    for n in train + score:
        if n not in STUDENTS:
            raise SystemExit(f"unknown student {n}; known: {sorted(STUDENTS)}")
    started = datetime.now(UTC)
    session = f"{started:%Y%m%dT%H%M%SZ}"
    out_dir = RUNS / EXPERIMENT / session
    versions = sorted({STUDENTS[n]["data_version"] for n in train + score})
    data_manifests = {v: json.loads((OUT / v / "manifest.json").read_text()) for v in versions}
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    jobs, files = [], {}
    for kind, name, gpu in assign_gpus(train, score):
        s = STUDENTS[name]
        tag = s["data_version"].split("@")[1]
        if kind == "train":
            for part in ("train", "valid"):
                f = f"{tag}-{s['data']}-{part}.jsonl"
                if f not in files:
                    shutil.copy(OUT / s["data_version"] / s["data"] / f"{part}.jsonl", STAGE / f)
                    files[f] = _sha256(STAGE / f)
            job = {
                "kind": "train",
                "name": name,
                "model": s["model"],
                "data": s["data"],
                "data_version": s["data_version"],
                "gpu": gpu,
                "lr": s["lr"],
                "epochs": TRAIN["epochs"],
                "seed": SEED,
                "dtype": TRAIN["dtype"],
                "train_file": f"{tag}-{s['data']}-train.jsonl",
                "valid_file": f"{tag}-{s['data']}-valid.jsonl",
                "resume": None,
            }
            if args.stop_after_steps:  # a probe: stop (paused, resumable) after this many steps this session
                job["stop_after_steps"] = args.stop_after_steps
            if args.pad_check and not (WEIGHTS / name / "last" / "status.json").exists():
                job["pad_check_rows"] = args.pad_check
            last = WEIGHTS / name / "last"
            if (last / "status.json").exists():
                st = json.loads((last / "status.json").read_text())
                if st["status"] == "done":
                    raise SystemExit(f"{name} already finished training ({last}); nothing to resume")
                shutil.copytree(last, STAGE / "resume" / name)
                job["resume"] = f"resume/{name}"
                job["resumed_at_step"] = st["opt_step"]
        else:
            best = WEIGHTS / name / "best"
            if (
                name in train
            ):  # scored after this session's training, from its best adapter, only if it finished
                adapter, adapter_sha256 = f"{name}/best", None
            elif not (best / "adapter_config.json").exists():
                raise SystemExit(f"no best adapter for {name} in {best}: import its training first")
            else:
                shutil.copytree(best, STAGE / "adapters" / name)
                adapter, adapter_sha256 = f"adapters/{name}", _sha256(best / "adapter_model.safetensors")
            for split in score_splits:  # one job per split, same GPU, one after another
                req_file = f"{split}-requests.jsonl"
                if req_file not in files:
                    reqs = student_dev.build_requests(Split(split))
                    (STAGE / req_file).write_text(
                        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in reqs)
                    )
                    files[req_file] = _sha256(STAGE / req_file)
                jobs.append(
                    {
                        "kind": "score",
                        "name": f"score-{name}" + ("" if split == "dev" else f"-{split}"),
                        "student": name,
                        "split": split,
                        "model": s["model"],
                        "gpu": gpu,
                        "adapter": adapter,
                        "adapter_sha256": adapter_sha256,
                        "after_train": name if name in train else None,
                        "requests": req_file,
                    }
                )
            continue
        jobs.append(job)
    run = {
        "session": session,
        "data_version": versions[0] if len(versions) == 1 else versions,
        "prompt_version": STUDENT_PROMPT_VERSION,
        "models": MODELS,
        "packages": PACKAGES,
        "train": TRAIN,
        "generation": GENERATION,
        "deadline_hours": args.deadline_hours,
        "jobs": jobs,
    }
    (STAGE / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    (STAGE / "dataset-metadata.json").write_text(
        json.dumps({"title": "orderslm-m6", "id": DATASET, "licenses": [{"name": "unknown"}]}) + "\n"
    )
    manifest = {
        "experiment": EXPERIMENT,
        **run,
        "seed": SEED,
        "staged_files_sha256": files,
        "data_manifest_sha256": {
            v: {k: m["sets"][k]["train"]["sha256"] for k in ("single", "mixed")}
            for v, m in data_manifests.items()
        },
        "data_built_at_commit": {v: m["git_commit"] for v, m in data_manifests.items()},
        "exported_at": started.isoformat(),
        "git_commit": git_commit(),
        "kaggle_dataset": DATASET,
        "cost_usd": 0.0,
    }
    out_dir.mkdir(parents=True)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for j in jobs:
        print(
            f"  gpu{j['gpu']} {j['kind']:5} {j['name']}"
            + (f" (resume @ {j['resumed_at_step']})" if j.get("resume") else "")
        )
    print(f"Staged {STAGE.relative_to(ROOT)}/; run dir {out_dir.relative_to(ROOT)}/")
    return out_dir


def _copy(src: Path, dst: Path, names: tuple[str, ...]) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for n in names:
        if (src / n).exists():
            shutil.copy(src / n, dst / n)


def memory_summary(samples: list[dict]) -> dict[str, Any]:
    """Lowest free host RAM, most tmpfs/shared memory and largest process-tree RSS per GPU over the session."""
    errors = sum("error" in s for s in samples)
    samples = [s for s in samples if "meminfo" in s]
    if not samples:
        return {"errors": errors} if errors else {}
    avail = [s["meminfo"]["MemAvailable"] for s in samples if "MemAvailable" in s["meminfo"]]
    shmem = [s["meminfo"]["Shmem"] for s in samples if "Shmem" in s["meminfo"]]
    rss: dict[str, float] = {}
    for s in samples:
        for g, v in s.get("rss_gb", {}).items():
            rss[g] = max(rss.get(g, 0.0), v)
    return {
        "samples": len(samples),
        "total_gb": samples[0]["meminfo"].get("MemTotal"),
        "min_available_gb": min(avail) if avail else None,
        "max_shmem_gb": max(shmem) if shmem else None,
        "max_rss_gb": rss,
        "cgroup_max_gb": samples[0].get("cgroup", {}).get("max"),
        "errors": errors,
    }


def import_(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text())
    if env.get("session") != manifest["session"]:
        raise SystemExit(f"kernel output is for session {env.get('session')}, not {manifest['session']}")
    summary: dict[str, Any] = {"env": {k: v for k, v in env.items() if k != "jobs"}, "jobs": {}}
    for job in manifest["jobs"]:
        name, src = job["name"], output_dir / job["name"]
        status = (
            json.loads((src / "status.json").read_text())
            if (src / "status.json").exists()
            else {"status": "missing"}
        )
        if job["kind"] == "train":
            dst = run_dir / name
            _copy(src, dst, ("config.json", "steps.jsonl", "val.jsonl", "status.json", "pad_check.json"))
            weights = WEIGHTS / name
            for part in ("best", "last"):
                if (src / part).exists():
                    shutil.rmtree(weights / part, ignore_errors=True)
                    shutil.copytree(src / part, weights / part)
            val = (
                [json.loads(x) for x in (src / "val.jsonl").read_text().splitlines()]
                if (src / "val.jsonl").exists()
                else []
            )
            best = weights / "best" / "adapter_model.safetensors"
            info = {
                "status": status,
                "val": val,
                "best_adapter_sha256": _sha256(best) if best.exists() else None,
                "best": json.loads((weights / "best" / "best.json").read_text())
                if (weights / "best" / "best.json").exists()
                else None,
            }
            if (src / "best" / "adapter_config.json").exists():
                shutil.copy(src / "best" / "adapter_config.json", dst / "best_adapter_config.json")
            steps = (
                [json.loads(x) for x in (src / "steps.jsonl").read_text().splitlines()]
                if (src / "steps.jsonl").exists()
                else []
            )
            if steps:
                secs = sum(s["seconds"] for s in steps)
                info |= {
                    "steps_logged": len(steps),
                    "skipped_updates": sum(s["skipped"] for s in steps),
                    "train_hours_logged": round(secs / 3600, 2),
                    "peak_memory_gb": max((s["peak_memory_gb"] or 0) for s in steps),
                    "tokens_per_second": round(sum(s["tokens"] for s in steps) / secs, 1),
                }
            (dst / "summary.json").write_text(json.dumps(info, indent=2) + "\n")
            summary["jobs"][name] = info
        else:
            split = job.get("split", "dev")
            dev_dir = (
                RUNS
                / student_dev.EXPERIMENT
                / (f"{manifest['session']}-{job['student']}" + ("" if split == "dev" else f"-{split}"))
            )
            _copy(src, dev_dir, ("outputs.jsonl", "config.json", "status.json"))
            scored = (
                json.loads((src / "config.json").read_text()).get("adapter_sha256")
                if (src / "config.json").exists()
                else None
            )
            # an in-session training's best adapter: the kernel's hash must match the imported weights
            expected = job["adapter_sha256"] or summary["jobs"].get(job.get("after_train"), {}).get(
                "best_adapter_sha256"
            )
            if scored and expected and scored != expected:
                raise SystemExit(f"{name} scored adapter {scored[:12]}…, expected {expected[:12]}…")
            (dev_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "experiment": student_dev.EXPERIMENT,
                        "student": job["student"],
                        "split": split,
                        "adapter_sha256": scored or expected,
                        "session": manifest["session"],
                        "data_version": STUDENTS[job["student"]]["data_version"],
                        "prompt_version": manifest["prompt_version"],
                        "generation": manifest["generation"],
                        "model": manifest["models"][job["model"]],
                        "kernel_env": summary["env"],
                        "cost_usd": 0.0,
                    },
                    indent=2,
                )
                + "\n"
            )
            m = student_dev.report(dev_dir) if (dev_dir / "outputs.jsonl").exists() else None
            summary["jobs"][name] = {"status": status, "dev_run": str(dev_dir.relative_to(ROOT))}
            if m:
                summary["jobs"][name] |= {
                    "intent_all": m["intent"]["all"],
                    "intent_earlier": m["intent"]["earlier_messages"],
                    "items_f1": m["order"]["item"]["f1"],
                    "exact": f"{m['order']['exact_match']}/{m['order']['conversations']}",
                    "contract_valid": m["contract_valid"],
                }
    kernel = run_dir / "kernel"
    _copy(output_dir, kernel, ("env.json", "run.log", "memory.jsonl"))
    if (kernel / "memory.jsonl").exists():
        summary["host_memory"] = memory_summary(
            [json.loads(x) for x in (kernel / "memory.jsonl").read_text().splitlines() if x.strip()]
        )
    manifest["imported_at"] = datetime.now(UTC).isoformat()
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["jobs"], indent=2))
    return summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--train", help="students to train (comma-separated, ≤ 2)")
    e.add_argument("--score", help="students to score on dev (their best adapter)")
    e.add_argument(
        "--deadline-hours",
        type=float,
        default=DEADLINE_HOURS,
        help="jobs stop themselves this long after the session start (lower it to fit the remaining GPU quota)",
    )
    e.add_argument("--score-splits", help="evaluation splits to score on: dev (default), fresh, or dev,fresh")
    e.add_argument("--stop-after-steps", type=int, help="probe: each training pauses after N steps")
    e.add_argument(
        "--pad-check", type=int, metavar="ROWS", help="score ROWS valid rows padded and unpadded first"
    )
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
