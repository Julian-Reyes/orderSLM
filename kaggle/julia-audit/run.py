"""Kaggle script kernel: Julia-1 answers the label-audit requests (docs/KAGGLE.md job A).

Standalone (no orderslm import). Input: the private dataset staged by `orderslm.eval.julia_audit export`
(requests.jsonl + run.json). Output in /kaggle/working: outputs.jsonl (one line per request: answers or error),
env.json (versions, hardware, model revision and hash, timings), run.log. Scoring happens on the Mac.
"""

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

MODEL = "SupersonicLabs/Julia-1"
REVISION = "a85b127321d580d65176c89ced8273f305745d85"
WEIGHTS_SHA256 = "df853bf7fe424420011f3d0c47a05d7341aa9eefa7fb9f203ea4aada4ad95b72"
MAX_LENGTH, HEAD_LENGTH = 8192, 512  # model card defaults; every request is ≤ 624 tokens (checked at export)
OUT = Path("/kaggle/working")
LOG = (OUT / "run.log").open("a")


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def pip(*args: str) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *args])


def find_input() -> Path:
    hits = sorted(Path("/kaggle/input").rglob("requests.jsonl"))
    if len(hits) != 1:
        raise SystemExit(f"expected one requests.jsonl under /kaggle/input, found {hits}")
    return hits[0].parent


def main() -> None:
    t_start = time.time()
    src = find_input()
    run = json.loads((src / "run.json").read_text())
    log(f"input {src}, run {run['run_dir']}, {run['requests']} requests")

    import torch

    if tuple(int(x) for x in torch.__version__.split("+")[0].split(".")[:2]) < (2, 6):
        log(f"preinstalled torch {torch.__version__} < 2.6: installing CPU torch>=2.6")
        pip("torch>=2.6", "--index-url", "https://download.pytorch.org/whl/cpu")
        raise SystemExit("torch upgraded; re-run the kernel so the new torch is imported")
    pip("transformers>=5.0,<5.1", "safetensors>=0.5", "huggingface_hub")

    from huggingface_hub import snapshot_download

    path = Path(snapshot_download(MODEL, revision=REVISION, local_dir="/tmp/Julia-1"))
    with (path / "model.safetensors").open("rb") as f:
        sha = hashlib.file_digest(f, "sha256").hexdigest()
    if sha != WEIGHTS_SHA256:
        raise SystemExit(f"weights sha256 {sha} != {WEIGHTS_SHA256}")
    pip("--no-deps", str(path))

    import transformers
    from julia import load_model

    t0 = time.time()
    engine = load_model(
        str(path), device="cpu", strict_encoding=True, max_length=MAX_LENGTH, head_length=HEAD_LENGTH
    )
    load_s = time.time() - t0
    log(f"model loaded in {load_s:.1f}s; torch {torch.__version__}, threads {torch.get_num_threads()}")

    latencies = []
    errors = 0
    with (OUT / "outputs.jsonl").open("w") as out:
        for k, line in enumerate((src / "requests.jsonl").read_text().splitlines(), 1):
            req = json.loads(line)
            rec = {"id": req["id"]}
            try:
                t = time.perf_counter()
                result = engine.predict(state=req["state"], questions=req["questions"])
                rec["latency_ms"] = (time.perf_counter() - t) * 1000
                rows = [
                    {
                        "state": req["state"],
                        "question": q["instructions"],
                        "type": q["type"],
                        "options": list(q["criteria"].values())
                        if q["type"] == "choice"
                        else ["false", "true"],
                    }
                    for q in req["questions"].values()
                ]
                rec["input_tokens"] = sum(i["tokens"] for i in engine.encoding_info(rows))
                rec["answers"] = result["answers"]
                latencies.append(rec["latency_ms"])
            except Exception as e:  # one bad request must not lose the rest; recorded and counted
                rec["error"] = f"{type(e).__name__}: {e}"
                errors += 1
            out.write(json.dumps(rec) + "\n")
            if k % 100 == 0 or k == run["requests"]:
                log(f"{k}/{run['requests']} done, {errors} errors")

    latencies.sort()
    env = {
        "run_dir": run["run_dir"],
        "requests": run["requests"],
        "errors": errors,
        "model": MODEL,
        "revision": REVISION,
        "weights_sha256": sha,
        "max_length": MAX_LENGTH,
        "head_length": HEAD_LENGTH,
        "strict_encoding": True,
        "device": "cpu",
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "torch_threads": torch.get_num_threads(),
        "cpu_count": os.cpu_count(),
        "cpu": platform.processor() or platform.machine(),
        "platform": platform.platform(),
        "load_seconds": round(load_s, 1),
        "total_seconds": round(time.time() - t_start, 1),
        "latency_ms_p50": round(latencies[len(latencies) // 2], 1) if latencies else None,
        "latency_ms_p95": round(latencies[int(len(latencies) * 0.95)], 1) if latencies else None,
        "latency_ms_sum": round(sum(latencies), 1),
    }
    (OUT / "env.json").write_text(json.dumps(env, indent=2) + "\n")
    log(f"done: {json.dumps(env)}")


if __name__ == "__main__":
    main()
