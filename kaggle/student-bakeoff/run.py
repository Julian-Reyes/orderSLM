"""Kaggle script kernel (GPU): M5 student bake-off, zero-shot (docs/KAGGLE.md job B).

Standalone (no orderslm import). Input: the private dataset staged by `orderslm.eval.student_bakeoff export`
(requests.jsonl, models.json, run.json). For each candidate, in turn: download at the pinned revision, load in
fp32 over the GPUs, answer every request greedily. Each model runs in its own process, so it starts with
empty GPUs (in one process, memory left by the previous model ran the next ones out of memory). Output in /kaggle/working: outputs.jsonl (one
line per model × request: raw text, tokens, latency, finish reason, or error), env.json, run.log. Scoring on the Mac.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

OUT = Path("/kaggle/working")
LOG = (OUT / "run.log").open("a")


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def find_input() -> Path:
    hits = sorted(Path("/kaggle/input").rglob("models.json"))
    if len(hits) != 1:
        raise SystemExit(f"expected one models.json under /kaggle/input, found {hits}")
    return hits[0].parent


GPU_HEADROOM_GIB = (
    2.0  # per GPU, kept free for the prefill (3.5 pushed ~10 GB of Gemma to CPU: 9 min per answer)
)
CPU_OFFLOAD_GIB = 20  # whatever doesn't fit under the GPU caps (Gemma 4 E2B is ~20 GB in fp32)


def memory_caps() -> dict:
    import torch

    caps: dict = {
        i: f"{torch.cuda.get_device_properties(i).total_memory / 2**30 - GPU_HEADROOM_GIB:.1f}GiB"
        for i in range(torch.cuda.device_count())
    }
    caps["cpu"] = f"{CPU_OFFLOAD_GIB}GiB"
    return caps


def no_gqa_flag() -> bool:
    """transformers passes enable_gqa=True to SDPA when there is no mask; on a T4 in fp32 that falls back to the math
    kernel (full seq x seq scores per head: out of memory at ~8k tokens). Off, it repeats the K/V heads first and the
    memory-efficient kernel runs. Same attention, different kernel."""
    from transformers.integrations import sdpa_attention

    if not hasattr(sdpa_attention, "use_gqa_in_sdpa"):
        return False
    sdpa_attention.use_gqa_in_sdpa = lambda *a, **k: False
    return True


def load(cand: dict, dtype):
    import transformers
    from huggingface_hub import snapshot_download

    path = snapshot_download(cand["repo"], revision=cand["revision"], local_dir=f"/tmp/models/{cand['name']}")
    kw = {"dtype": dtype, "device_map": "auto", "max_memory": memory_caps()}
    if cand["loader"] == "causal":
        tok = transformers.AutoTokenizer.from_pretrained(path)
        model = transformers.AutoModelForCausalLM.from_pretrained(path, **kw)
        return tok, model, tok
    proc = transformers.AutoProcessor.from_pretrained(path)
    cls = getattr(transformers, "AutoModelForMultimodalLM", None) or transformers.AutoModelForImageTextToText
    model = cls.from_pretrained(path, **kw)
    return proc, model, proc.tokenizer


def messages(cand: dict, req: dict) -> list[dict]:
    if cand["loader"] == "causal":
        return [{"role": "system", "content": req["system"]}, {"role": "user", "content": req["user"]}]
    return [
        {"role": "system", "content": [{"type": "text", "text": req["system"]}]},
        {"role": "user", "content": [{"type": "text", "text": req["user"]}]},
    ]


def run_one(name: str) -> None:
    """Child process: one candidate over every request → /tmp/bakeoff/<name>.jsonl + <name>.json."""
    import torch

    src = find_input()
    cfg = json.loads((src / "models.json").read_text())
    cand = next(c for c in cfg["candidates"] if c["name"] == name)
    gen = cfg["generation"]
    requests = [json.loads(x) for x in (src / "requests.jsonl").read_text().splitlines()]
    n_gpus = torch.cuda.device_count()
    info: dict = {
        "repo": cand["repo"],
        "revision": cand["revision"],
        "sdpa_gqa_flag_off": no_gqa_flag(),
        "max_memory": memory_caps(),
    }
    part = Path("/tmp/bakeoff")
    part.mkdir(exist_ok=True)
    with (part / f"{name}.jsonl").open("w") as out:
        t0 = time.time()
        try:
            proc, model, tok = load(cand, getattr(torch, gen["dtype"]))
        except Exception as e:  # a model that won't load is a tooling result, not a crash
            info["error"] = f"{type(e).__name__}: {e}"[:2000]
            log(f"{name}: load failed: {info['error'][:300]}")
            for req in requests:
                out.write(json.dumps({"model": name, "id": req["id"], "error": info["error"]}) + "\n")
            (part / f"{name}.json").write_text(json.dumps(info))
            return
        info["load_seconds"] = round(time.time() - t0, 1)
        info["model_class"] = type(model).__name__
        info["parameters"] = sum(p.numel() for p in model.parameters())
        info["devices"] = sorted({str(p.device) for p in model.parameters()})
        info["memory_after_load_gb"] = [round(torch.cuda.memory_allocated(i) / 1e9, 2) for i in range(n_gpus)]
        log(
            f"{name}: loaded {info['model_class']} in {info['load_seconds']}s, {info['memory_after_load_gb']} GB"
        )
        for k, req in enumerate(requests, 1):
            rec = {"model": name, "id": req["id"]}
            try:
                inputs = proc.apply_chat_template(
                    messages(cand, req),
                    add_generation_prompt=True,
                    tokenize=True,
                    return_dict=True,
                    return_tensors="pt",
                    **cand["template_kwargs"],
                ).to(model.device)
                n_in = inputs["input_ids"].shape[1]
                torch.cuda.synchronize()
                t = time.perf_counter()
                with torch.inference_mode():
                    ids = model.generate(
                        **inputs,
                        do_sample=gen["do_sample"],
                        max_new_tokens=gen["max_new_tokens"],
                        pad_token_id=tok.pad_token_id or tok.eos_token_id,
                    )
                torch.cuda.synchronize()
                new = ids[0, n_in:]
                rec.update(
                    text=tok.decode(new, skip_special_tokens=True),
                    input_tokens=int(n_in),
                    output_tokens=int(new.shape[0]),
                    latency_ms=(time.perf_counter() - t) * 1000,
                    finish_reason="length" if new.shape[0] >= gen["max_new_tokens"] else "stop",
                    at=datetime.now(UTC).isoformat(),
                )
                del inputs, ids, new
            except Exception as e:  # recorded per request; the rest still run
                rec["error"] = f"{type(e).__name__}: {e}"[:2000]
            torch.cuda.empty_cache()
            out.write(json.dumps(rec) + "\n")
            out.flush()
            log(
                f"{name} {k}/{len(requests)} {req['id']}: "
                + (
                    rec.get("error", "")[:200]
                    or f"{rec['output_tokens']} tok, {rec['latency_ms'] / 1000:.1f}s"
                )
            )
    info["max_memory_gb"] = [round(torch.cuda.max_memory_allocated(i) / 1e9, 2) for i in range(n_gpus)]
    (part / f"{name}.json").write_text(json.dumps(info))


def main() -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-U", "transformers", "accelerate"])
    import torch
    import transformers

    src = find_input()
    run = json.loads((src / "run.json").read_text())
    cfg = json.loads((src / "models.json").read_text())
    n_requests = len((src / "requests.jsonl").read_text().splitlines())
    gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    log(
        f"run {run['run_dir']}: {n_requests} requests; torch {torch.__version__}, "
        f"transformers {transformers.__version__}, GPUs {gpus}"
    )
    env = {
        "run_dir": run["run_dir"],
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "cuda": torch.version.cuda,
        "gpus": gpus,
        "python": sys.version.split()[0],
        "generation": cfg["generation"],
        "process_per_model": True,
        "models": {},
    }
    child_env = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
    part = Path("/tmp/bakeoff")
    with (OUT / "outputs.jsonl").open("w") as out:
        for cand in cfg["candidates"]:
            name = cand["name"]
            r = subprocess.run([sys.executable, __file__, "--one", name], env=child_env)
            info_path, lines_path = part / f"{name}.json", part / f"{name}.jsonl"
            info = json.loads(info_path.read_text()) if info_path.exists() else {"repo": cand["repo"]}
            if r.returncode:
                info["exit_code"] = r.returncode
                log(f"{name}: process exited with {r.returncode}")
            done = set()
            if lines_path.exists():
                for line in lines_path.read_text().splitlines():
                    out.write(line + "\n")
                    done.add(json.loads(line)["id"])
            for req in (json.loads(x) for x in (src / "requests.jsonl").read_text().splitlines()):
                if req["id"] not in done:  # the process died before answering
                    out.write(
                        json.dumps({"model": name, "id": req["id"], "error": f"exit {r.returncode}"}) + "\n"
                    )
            out.flush()
            env["models"][name] = info
            shutil.rmtree(f"/tmp/models/{name}", ignore_errors=True)  # disk: the four models are ~20 GB
    (OUT / "env.json").write_text(json.dumps(env, indent=2) + "\n")
    log("done")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--one":
        run_one(sys.argv[2])
    else:
        main()
