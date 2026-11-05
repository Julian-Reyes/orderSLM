"""M6 deployment check on Kaggle (docs/KAGGLE.md job D): the picked student merged, converted to GGUF, quantized,
and run with llama.cpp on the same dev + fresh requests as its transformers scoring runs. Free.

Julian, 2026-11-04: "can we use kaggle for now" (no Mac mini at hand; Apple Silicon numbers and MLX come later).
Questions: (1) does a quantized GGUF give the same answers as the fp16 transformers runs (paired, same scorer),
and (2) how fast and how big is each format, on a T4 and on CPU.

    make deploy ARGS="export"                      # stage kaggle/m6-deploy/upload/ + runs/student-deploy/<id>/
    make kaggle-push JOB=m6-deploy                 # (ask Julian first; secrets check)
    make kaggle-pull JOB=m6-deploy                 # skips the GGUF files (they stay in the kernel output)
    make deploy ARGS="import runs/student-deploy/<id>"

Import writes one `runs/student-dev/<id>-<student>-<format>[-fresh]/` per GPU job (scored by `student_dev.report`,
so the numbers line up with the transformers runs) and, in the deploy run dir, the CPU jobs' outputs, the GGUF sizes
and sha256, peak memory, latency per job, and how often each format's final answer matches the fp16 run's text
(summary.json, report.md). The weights never leave Kaggle (docs/TERMS.md option b).
"""

import argparse
import hashlib
import json
import random
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from orderslm.eval import student_dev
from orderslm.paths import ROOT, RUNS
from orderslm.runinfo import git_commit
from orderslm.schema.conversation import Split
from orderslm.train.data import STUDENT_PROMPT_VERSION
from orderslm.train.kaggle_train import GENERATION, MODELS, PACKAGES, STUDENTS, WEIGHTS

EXPERIMENT = "student-deploy"
JOB_DIR = ROOT / "kaggle" / "m6-deploy"
STAGE = JOB_DIR / "upload"  # gitignored
DATASET = "JReyes33/orderslm-m6-deploy"
STUDENT = "qwen3.5-0.8b-single-v2"  # picked 2026-11-03 (Julian)
# the transformers fp16 runs of the same adapter on the same requests (the reference)
REFERENCE = {
    "dev": RUNS / "student-dev" / "20261026T131201Z-qwen3.5-0.8b-single-v2",
    "fresh": RUNS / "student-dev" / "20261026T131201Z-qwen3.5-0.8b-single-v2-fresh",
}
FORMATS = ["F16", "Q8_0", "Q4_K_M"]
# Run 2 (2026-11-05, Julian: "go ahead with the smaller run"). Run 1 (20261104T115735Z) answered every dev request in
# F16 and Q8_0, but on the CPU: the CUDA backend never loaded, so its speed numbers are void and it ran out of time.
# Its dev answers stay as accuracy runs; run 2 does the rest on a GPU that is checked first. Queue order per GPU:
# the timing samples first (so a GPU problem shows in minutes), then the full splits.
GPU_PLAN = [  # (gpu, format, split, timing sample only)
    (0, "F16", "dev", True),
    (0, "Q4_K_M", "dev", False),
    (0, "F16", "fresh", False),
    (1, "Q8_0", "dev", True),
    (1, "Q4_K_M", "fresh", False),
    (1, "Q8_0", "fresh", False),
]
CPU_FORMATS = ["Q8_0", "Q4_K_M"]
CPU_SAMPLE = 50  # dev requests, seeded: the same sample times every format on the GPU and on the CPU
SEED = 20261104
LLAMA_TAG = "b11700"  # 2026-10-16; registers Qwen3_5ForConditionalGeneration (conversion/qwen.py), src/models/qwen35.cpp
_REL = f"https://github.com/ggml-org/llama.cpp/releases/download/{LLAMA_TAG}"
LLAMA_CPP = {
    "tag": LLAMA_TAG,
    "urls": {
        "source": f"https://github.com/ggml-org/llama.cpp/archive/refs/tags/{LLAMA_TAG}.tar.gz",
        "cuda": f"{_REL}/llama-{LLAMA_TAG}-bin-ubuntu-cuda-12.8-x64.tar.gz",
        "cudart": f"{_REL}/cudart-llama-{LLAMA_TAG}-bin-ubuntu-cuda-12.8-x64.tar.gz",
        "cpu": f"{_REL}/llama-{LLAMA_TAG}-bin-ubuntu-x64.tar.gz",
    },
}
SERVER = {"ctx_size": 8192}  # longest dev/fresh prompt 5,448 tokens + 1,536 answer tokens
DEADLINE_HOURS = 4.0  # run 1 used its full 11.25 h on the CPU; run 2 should take about 2.5 h
# stop rules (Julian: "make sure it stops if it doesn't work"): after each GPU job's first answer the model must hold
# GPU memory and generate faster than any CPU run did (run 1 on the CPU: 6-9 output tok/s); otherwise every job stops
GUARD = {"min_gpu_mib": 256, "min_output_tok_s": 20.0}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cpu_sample(request_ids: list[str], n: int = CPU_SAMPLE, seed: int = SEED) -> list[str]:
    return sorted(random.Random(seed).sample(sorted(request_ids), min(n, len(request_ids))))


def plan_jobs(dev_ids: list[str]) -> list[dict[str, Any]]:
    sample = cpu_sample(dev_ids)
    jobs = []
    for gpu, fmt, split, timing in GPU_PLAN:
        name = f"gpu-{fmt.lower()}" + ("" if split == "dev" else f"-{split}") + ("-timing" if timing else "")
        job = {
            "name": name,
            "device": "cuda",
            "gpu": gpu,
            "format": fmt,
            "split": split,
            "requests": f"{split}-requests.jsonl",
        }
        if timing:
            job["request_ids"] = sample
        jobs.append(job)
    for fmt in CPU_FORMATS:
        jobs.append(
            {
                "name": f"cpu-{fmt.lower()}",
                "device": "cpu",
                "gpu": None,
                "format": fmt,
                "split": "dev",
                "requests": "dev-requests.jsonl",
                "request_ids": sample,
            }
        )
    return jobs


def export(args: argparse.Namespace) -> Path:
    student = STUDENTS[STUDENT]
    best = WEIGHTS / STUDENT / "best"
    if not (best / "adapter_model.safetensors").exists():
        raise SystemExit(f"no adapter in {best}")
    adapter_sha = _sha256(best / "adapter_model.safetensors")
    ref_sha = json.loads((REFERENCE["dev"] / "manifest.json").read_text())["adapter_sha256"]
    if adapter_sha != ref_sha:
        raise SystemExit(
            f"adapter {adapter_sha[:12]}… is not the one the reference runs scored ({ref_sha[:12]}…)"
        )
    started = datetime.now(UTC)
    session = f"{started:%Y%m%dT%H%M%SZ}"
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copytree(best, STAGE / "adapter")
    files = {"adapter/adapter_model.safetensors": adapter_sha}
    dev_ids: list[str] = []
    for split in ("dev", "fresh"):
        reqs = student_dev.build_requests(Split(split))
        f = STAGE / f"{split}-requests.jsonl"
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in reqs))
        files[f.name] = _sha256(f)
        ref_ids = {json.loads(x)["id"] for x in (REFERENCE[split] / "outputs.jsonl").read_text().splitlines()}
        if ref_ids != {r["id"] for r in reqs}:
            raise SystemExit(f"{split} requests differ from the reference run's")
        if split == "dev":
            dev_ids = [r["id"] for r in reqs]
    run = {
        "session": session,
        "student": STUDENT,
        "data_version": student["data_version"],
        "prompt_version": STUDENT_PROMPT_VERSION,
        "model": MODELS[student["model"]],
        "adapter": "adapter",
        "adapter_sha256": adapter_sha,
        "packages": {"main": PACKAGES["main"]},
        "llama_cpp": LLAMA_CPP,
        "server": SERVER,
        "generation": GENERATION,
        "formats": FORMATS,
        "deadline_hours": args.deadline_hours,
        "guard": GUARD,
        "timing_sample": cpu_sample(dev_ids),
        "jobs": plan_jobs(dev_ids),
    }
    (STAGE / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    (STAGE / "dataset-metadata.json").write_text(
        json.dumps({"title": "orderslm-m6-deploy", "id": DATASET, "licenses": [{"name": "unknown"}]}) + "\n"
    )
    out_dir = RUNS / EXPERIMENT / session
    out_dir.mkdir(parents=True)
    manifest = {
        "experiment": EXPERIMENT,
        **run,
        "reference_runs": {k: str(v.relative_to(ROOT)) for k, v in REFERENCE.items()},
        "staged_files_sha256": files,
        "exported_at": started.isoformat(),
        "git_commit": git_commit(),
        "kaggle_dataset": DATASET,
        "cost_usd": 0.0,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for j in run["jobs"]:
        where = f"gpu{j['gpu']}" if j["device"] == "cuda" else "cpu "
        print(
            f"  {where} {j['name']}"
            + (f" ({len(j['request_ids'])} requests)" if j.get("request_ids") else "")
        )
    print(f"Staged {STAGE.relative_to(ROOT)}/; run dir {out_dir.relative_to(ROOT)}/")
    return out_dir


# ---------------------------------------------------------------- import


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []


def percentiles(values: list[float]) -> dict[str, float] | None:
    v = sorted(values)
    if not v:
        return None
    return {"p50": v[len(v) // 2], "p95": v[int(0.95 * (len(v) - 1))], "n": len(v)}


def latency(records: list[dict]) -> dict[str, Any]:
    ok = [r for r in records if "text" in r]
    timings = [r["timings"] for r in ok if r.get("timings")]
    return {
        "answered": len(ok),
        "errors": len(records) - len(ok),
        "hit_token_limit": sum(r.get("finish_reason") == "length" for r in ok),
        "latency_ms": percentiles([r["latency_ms"] for r in ok]),
        "prompt_tokens_per_s": percentiles(
            [t["prompt_per_second"] for t in timings if "prompt_per_second" in t]
        ),
        "output_tokens_per_s": percentiles(
            [t["predicted_per_second"] for t in timings if "predicted_per_second" in t]
        ),
    }


def agreement(records: list[dict], reference: list[dict]) -> dict[str, Any]:
    """Same answer text as the reference, request by request (only where both answered); same input token count
    shows the prompt was identical."""
    ref = {r["id"]: r for r in reference if "text" in r}
    pairs = [(r, ref[r["id"]]) for r in records if "text" in r and r["id"] in ref]
    return {
        "compared": len(pairs),
        "same_text": sum(a["text"].strip() == b["text"].strip() for a, b in pairs),
        "same_input_tokens": sum(a["input_tokens"] == b["input_tokens"] for a, b in pairs),
    }


def import_(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    env = json.loads((output_dir / "env.json").read_text())
    if env.get("session") != manifest["session"]:
        raise SystemExit(f"kernel output is for session {env.get('session')}, not {manifest['session']}")
    merge = env.get("steps", {}).get("merge", {})
    if merge.get("adapter_sha256") and merge["adapter_sha256"] != manifest["adapter_sha256"]:
        raise SystemExit("the kernel merged a different adapter than the one staged")
    refs = {k: _read_jsonl(ROOT / v / "outputs.jsonl") for k, v in manifest["reference_runs"].items()}
    files = env.get("steps", {}).get("convert", {}).get("files", {})
    llama = env.get("steps", {}).get("llama_cpp", {})
    cuda_build = llama.get("cuda_build", "prebuilt CUDA 12.8")
    sample = set(
        manifest.get("timing_sample")
        or next(j["request_ids"] for j in manifest["jobs"] if j["device"] == "cpu")
    )
    summary: dict[str, Any] = {
        "env": {k: v for k, v in env.items() if k != "jobs"},
        "gguf": files,
        "reference_latency": {k: latency(v) for k, v in refs.items()},
        "jobs": {},
    }
    by_format_split: dict[tuple[str, str], list[dict]] = {}
    for job in manifest["jobs"]:
        name, src = job["name"], output_dir / job["name"]
        status = (
            json.loads((src / "status.json").read_text())
            if (src / "status.json").exists()
            else {"status": "missing"}
        )
        records = _read_jsonl(src / "outputs.jsonl")
        memory = json.loads((src / "memory.json").read_text()) if (src / "memory.json").exists() else None
        # run 1: the CUDA server answered with no GPU memory in use, i.e. on the CPU; its timings are not GPU timings
        gpu_used = (
            bool(memory and memory.get("peak_gpu_used_mib")) if job["device"] == "cuda" and records else None
        )
        full = not job.get("request_ids") and status.get("status") == "done"
        info: dict[str, Any] = {
            "status": status.get("status"),
            "format": job["format"],
            "device": job["device"],
            "split": job["split"],
            "gpu_used": gpu_used,
            "memory": memory,
            **latency(records),
            "timing_sample": latency([r for r in records if r["id"] in sample])
            if job["split"] == "dev"
            else None,
            "vs_fp16_transformers": agreement(records, refs[job["split"]]),
        }
        if job["device"] == "cuda" and job["split"] == "dev":
            by_format_split.setdefault((job["format"], "dev"), []).extend(records)
        if job["device"] == "cuda" and full:
            split = job["split"]
            dev_dir = (
                RUNS
                / student_dev.EXPERIMENT
                / (
                    f"{manifest['session']}-{manifest['student']}-{job['format'].lower()}"
                    + ("" if split == "dev" else f"-{split}")
                )
            )
            dev_dir.mkdir(parents=True, exist_ok=True)
            for f in ("outputs.jsonl", "status.json", "memory.json"):
                if (src / f).exists():
                    shutil.copy(src / f, dev_dir / f)
            (dev_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "experiment": student_dev.EXPERIMENT,
                        "student": f"{manifest['student']}-{job['format'].lower()}",
                        "split": split,
                        "adapter_sha256": manifest["adapter_sha256"],
                        "session": manifest["session"],
                        "data_version": manifest["data_version"],
                        "prompt_version": manifest["prompt_version"],
                        "generation": manifest["generation"],
                        "model": manifest["model"],
                        "runtime": {
                            "engine": f"llama.cpp llama-server ({cuda_build})"
                            + ("" if gpu_used else ", but the CUDA backend did not load: it ran on the CPU"),
                            "gpu_used": gpu_used,
                            "llama_cpp": manifest["llama_cpp"]["tag"],
                            "format": job["format"],
                            "gguf": files.get(job["format"]),
                            "server": manifest["server"],
                            "greedy": "samplers [top_k], top_k 1, temperature 0, no prompt cache",
                        },
                        "deploy_run": str(run_dir.relative_to(ROOT)),
                        "cost_usd": 0.0,
                    },
                    indent=2,
                )
                + "\n"
            )
            if (dev_dir / "outputs.jsonl").exists():
                m = student_dev.report(dev_dir)
                info |= {
                    "dev_run": str(dev_dir.relative_to(ROOT)),
                    "exact": f"{m['order']['exact_match']}/{m['order']['conversations']}",
                    "same_action": f"{m['order']['action_match']}/{m['order']['conversations']}",
                    "intent_all": m["intent"]["all"]["primary_correct"],
                    "items_f1": m["order"]["item"]["f1"],
                    "contract_valid": m["contract_valid"],
                }
        else:
            dst = run_dir / name
            dst.mkdir(parents=True, exist_ok=True)
            for f in ("outputs.jsonl", "status.json", "memory.json"):
                if (src / f).exists():
                    shutil.copy(src / f, dst / f)
        summary["jobs"][name] = info
    for name, job in ((j["name"], j) for j in manifest["jobs"] if j["device"] == "cpu"):
        gpu = by_format_split.get((job["format"], "dev"), [])
        summary["jobs"][name]["vs_same_format_on_gpu"] = agreement(
            _read_jsonl(output_dir / name / "outputs.jsonl"), gpu
        )
    kernel = run_dir / "kernel"
    kernel.mkdir(exist_ok=True)
    for f in ("env.json", "run.log"):
        if (output_dir / f).exists():
            shutil.copy(output_dir / f, kernel / f)
    manifest["imported_at"] = datetime.now(UTC).isoformat()
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    _write_report(run_dir, manifest, summary)
    print((run_dir / "report.md").read_text())
    return summary


def _ms(x: dict | None) -> str:
    return f"{x['p50'] / 1000:.1f} / {x['p95'] / 1000:.1f}" if x else "?"


def _tps(x: dict | None) -> str:
    return f"{x['p50']:.0f}" if x else "?"


def _write_report(run_dir: Path, manifest: dict, s: dict) -> None:
    hw = s["env"].get("hardware", {})
    lines = [
        f"# `{manifest['student']}` packaged with llama.cpp ({manifest['llama_cpp']['tag']}): session "
        f"{manifest['session']}",
        "",
        f"Merged fp16 (base `{manifest['model']['repo']}` @ `{manifest['model']['revision'][:12]}` + adapter "
        f"`{manifest['adapter_sha256'][:12]}`), converted to GGUF and quantized on Kaggle; greedy, the same "
        f"requests and token ids as the transformers runs. Hardware: {hw.get('gpus')}, CPU {hw.get('cpu_model')} "
        f"× {hw.get('cpu_count')}. Dev is tuning data; fresh helped shape finalize@0.2 (used for fixes). $0.",
        "",
        "| format | GGUF size |",
        "|---|---|",
    ]
    for fmt, f in s["gguf"].items():
        lines.append(f"| {fmt} | {f['bytes'] / 1e9:.2f} GB (`{f['sha256'][:12]}`) |")
    lines += [
        "",
        "| job | split | answered | exact / same action | same text as fp16 transformers | latency p50 / p95 (s) "
        "| prompt / output tok/s (p50) | peak memory |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for k, r in s["reference_latency"].items():
        lines.append(
            f"| transformers fp16 (reference) | {k} | {r['answered']} | | | {_ms(r['latency_ms'])} | | |"
        )
    for name, j in s["jobs"].items():
        a = j["vs_fp16_transformers"]
        mem = j.get("memory") or {}
        parts = [f"GPU {mem['peak_gpu_used_mib']} MiB"] if mem.get("peak_gpu_used_mib") else []
        parts += [f"RSS {mem['peak_server_rss_gb']:.2f} GB"] if mem.get("peak_server_rss_gb") else []
        peak = ", ".join(parts)
        if j.get("gpu_used") is False:
            peak += " (**GPU not used: ran on the CPU**)"
        lines.append(
            f"| {name} | {j['split']} | {j['answered']} ({j['status']}) | "
            f"{j.get('exact', '')}{' / ' + j['same_action'] if j.get('same_action') else ''} | "
            f"{a['same_text']}/{a['compared']} | {_ms(j['latency_ms'])} | "
            f"{_tps(j['prompt_tokens_per_s'])} / {_tps(j['output_tokens_per_s'])} | {peak} |"
        )
    timed = {k: v for k, v in s["jobs"].items() if v.get("timing_sample") and v["timing_sample"]["answered"]}
    if timed:
        lines += [
            "",
            "Speed on the same seeded sample of dev requests (one request at a time, no prompt cache):",
            "",
            "| job | where it ran | answered | latency p50 / p95 (s) | prompt / output tok/s (p50) |",
            "|---|---|---|---|---|",
        ]
        for name, j in timed.items():
            t = j["timing_sample"]
            where = "CPU" if j["device"] == "cpu" or j.get("gpu_used") is False else "GPU"
            lines.append(
                f"| {name} | {where} | {t['answered']} | {_ms(t['latency_ms'])} | "
                f"{_tps(t['prompt_tokens_per_s'])} / {_tps(t['output_tokens_per_s'])} |"
            )
    cpu = {k: v["vs_same_format_on_gpu"] for k, v in s["jobs"].items() if "vs_same_format_on_gpu" in v}
    if cpu:
        lines += [
            "",
            "CPU answers vs the same format on the GPU (same text): "
            + ", ".join(f"{k} {v['same_text']}/{v['compared']}" for k, v in cpu.items()),
        ]
    (run_dir / "report.md").write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--deadline-hours", type=float, default=DEADLINE_HOURS)
    i = sub.add_parser("import")
    i.add_argument("run_dir", type=Path)
    i.add_argument("--output", type=Path, default=JOB_DIR / "output")
    args = ap.parse_args(argv)
    if args.cmd == "export":
        export(args)
    else:
        import_(args.run_dir.resolve(), args.output.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
