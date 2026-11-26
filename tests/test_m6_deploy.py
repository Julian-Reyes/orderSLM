"""M6 deployment check (kaggle/m6-deploy): what the kernel sends llama-server, what it records, the job plan, and
the import (no network, no GPU)."""

import importlib.util
import json
import re
import shutil

import pytest

from orderslm import kaggle_jobs
from orderslm.paths import ROOT
from orderslm.train import kaggle_deploy as kd


def _kernel(tmp_path, monkeypatch):
    monkeypatch.setenv("ORDERSLM_KAGGLE_OUT", str(tmp_path / "out"))
    monkeypatch.setenv("ORDERSLM_KAGGLE_TMP", str(tmp_path / "tmp"))
    spec = importlib.util.spec_from_file_location("deploy_run", ROOT / "kaggle" / "m6-deploy" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_requests_are_greedy_uncached_token_ids(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    p = k.completion_payload([1, 2, 3], kd.GENERATION)
    assert p["prompt"] == [1, 2, 3]  # an id array: llama-server adds no BOS
    assert p["samplers"] == ["top_k"] and p["top_k"] == 1 and p["temperature"] == 0.0
    assert p["cache_prompt"] is False and p["n_predict"] == kd.GENERATION["max_new_tokens"]


def test_record_has_the_transformers_runs_shape(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    resp = {
        "content": '{"a": 1}',
        "tokens_predicted": 7,
        "stop_type": "eos",
        "timings": {"predicted_ms": 5.0},
    }
    r = k.record("a-dev-001#0", [1, 2], resp, 1234)
    assert {"id", "input_tokens", "text", "output_tokens", "finish_reason", "latency_ms", "at"} <= set(r)
    assert r["input_tokens"] == 2 and r["finish_reason"] == "stop" and r["output_tokens"] == 7
    assert k.record("x", [], {"stop_type": "limit"}, 1)["finish_reason"] == "length"


def test_missing_inputs_names_the_adapter_and_requests(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    run = {"adapter": "adapter", "jobs": [{"requests": "dev-requests.jsonl"}]}
    assert k.missing_inputs(run, tmp_path) == [
        "adapter/adapter_config.json",
        "adapter/adapter_model.safetensors",
        "dev-requests.jsonl",
    ]


def test_pull_skips_the_gguf_models():
    pat = re.compile(kaggle_jobs.PULL_PATTERNS["m6-deploy"])
    assert not pat.search("gguf/q4_k_m.gguf") and not pat.search("f16.gguf")
    assert pat.search("env.json") and pat.search("gpu-q8_0/outputs.jsonl") and pat.search("run.log")


def test_v6_plan_scores_q8_0_on_every_split_clean_ones_first_and_times_one_sample():
    dev_ids = [f"a-dev-{i:03d}#0" for i in range(1, 92)]
    jobs = kd.plan_jobs(dev_ids)
    sample = kd.cpu_sample(dev_ids)
    assert kd.STUDENT == "qwen3.5-0.8b-single-v6" and kd.FORMATS == [
        "Q8_0"
    ]  # the shipped format (2026-11-05)
    full = [(j["format"], j["split"]) for j in jobs if j["device"] == "cuda" and not j.get("request_ids")]
    # every scored split once, in the shipped format, each with a reference run of the same student
    assert sorted(full) == sorted(("Q8_0", s) for s in kd.REFERENCE)
    assert all(kd.STUDENT in str(v) for v in kd.REFERENCE.values())
    for g in (0, 1):  # the clean splits come first on their GPU, after at most the short timing sample
        first_full = next(j for j in jobs if j["gpu"] == g and not j.get("request_ids"))
        assert first_full["split"] in ("fresh4", "fresh5")
    timing = [j for j in jobs if j["device"] == "cuda" and j.get("request_ids")]
    assert [j["gpu"] for j in timing] == [0] and timing[0]["request_ids"] == sample
    assert jobs[0] is timing[0]  # a GPU problem shows in minutes
    cpu = [j for j in jobs if j["device"] == "cpu"]
    assert [j["format"] for j in cpu] == kd.CPU_FORMATS and all(j["request_ids"] == sample for j in cpu)
    assert len(sample) == kd.CPU_SAMPLE and set(sample) <= set(dev_ids)
    assert all("test" not in j["requests"] for j in jobs)  # the sealed test split never goes to Kaggle
    assert len({j["name"] for j in jobs}) == len(jobs)


def test_a_first_answer_off_the_gpu_stops_the_run(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    ok = {"text": "{}", "timings": {"predicted_per_second": 85.0}}
    assert k.gpu_problem(1900, ok, kd.GUARD) is None
    # run 1: no GPU memory in use and 7 output tok/s
    assert "not on the GPU" in k.gpu_problem(0, ok, kd.GUARD)
    assert "not GPU speed" in k.gpu_problem(1900, {"timings": {"predicted_per_second": 7.0}}, kd.GUARD)
    assert "failed" in k.gpu_problem(1900, {"error": "URLError"}, kd.GUARD)
    assert kd.DEADLINE_HOURS <= 4
    k.stop_all("test")
    k.run_queue([{"name": "gpu-x"}], {}, {}, 8080, 0)  # a stopped run starts no further job
    assert json.loads((tmp_path / "out" / "gpu-x" / "status.json").read_text())["status"] == "not started"


def test_import_scores_each_gpu_run_like_the_transformers_runs(tmp_path, monkeypatch):
    """A fake kernel output whose answers are copies of the reference runs' scores the same as them."""
    refs = {k: v for k, v in kd.REFERENCE.items()}
    if not all((v / "outputs.jsonl").exists() for v in refs.values()):
        pytest.skip("reference runs not present")
    monkeypatch.setattr(kd, "ROOT", tmp_path)
    monkeypatch.setattr(kd, "RUNS", tmp_path / "runs")
    dev_ids = [json.loads(x)["id"] for x in (refs["dev"] / "outputs.jsonl").read_text().splitlines()]
    session = "20990101T000000Z"
    run_dir = tmp_path / "runs" / kd.EXPERIMENT / session
    run_dir.mkdir(parents=True)
    jobs = kd.plan_jobs(dev_ids)
    manifest = {
        "session": session,
        "student": kd.STUDENT,
        "adapter_sha256": "abc",
        "data_version": "student-data@0.2",
        "prompt_version": "student-extract@0.1",
        "generation": kd.GENERATION,
        "model": kd.MODELS["0.8b"],
        "llama_cpp": kd.LLAMA_CPP,
        "server": kd.SERVER,
        "reference_runs": {k: str(v) for k, v in refs.items()},
        "jobs": jobs,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest))
    out = tmp_path / "output"
    files = {"Q8_0": {"file": "q8_0.gguf", "bytes": 810_000_000, "sha256": "f" * 64}}
    env = {"session": session, "steps": {"merge": {"adapter_sha256": "abc"}, "convert": {"files": files}}}
    (out).mkdir()
    (out / "env.json").write_text(json.dumps(env))
    for j in jobs:
        (out / j["name"]).mkdir()
        lines = (refs[j["split"]] / "outputs.jsonl").read_text().splitlines()
        if j.get("request_ids"):
            keep = set(j["request_ids"])
            lines = [x for x in lines if json.loads(x)["id"] in keep]
        (out / j["name"] / "outputs.jsonl").write_text("\n".join(lines) + "\n")
        (out / j["name"] / "status.json").write_text(json.dumps({"status": "done"}))
        gpu_mib = 0 if j["name"] == "gpu-q8_0-fresh" else 1900  # this one "ran" on the CPU, like run 1
        (out / j["name"] / "memory.json").write_text(json.dumps({"peak_gpu_used_mib": gpu_mib}))
    s = kd.import_(run_dir, out)
    ref_metrics = {k: json.loads((v / "metrics.json").read_text()) for k, v in refs.items()}
    for name, split in (("gpu-q8_0", "dev"), ("gpu-q8_0-fresh4", "fresh4"), ("gpu-q8_0-fresh5", "fresh5")):
        j = s["jobs"][name]
        o = ref_metrics[split]["order"]
        assert j["exact"] == f"{o['exact_match']}/{o['conversations']}"
        assert (
            j["vs_fp16_transformers"]["same_text"] == j["vs_fp16_transformers"]["compared"] == j["answered"]
        )
        m = json.loads((tmp_path / j["dev_run"] / "manifest.json").read_text())
        assert m["runtime"]["format"] == "Q8_0" and m["runtime"]["gguf"]["bytes"] == 810_000_000
        assert m["runtime"]["gpu_used"] is True and "did not load" not in m["runtime"]["engine"]
        assert j["timing_sample"] is None or j["timing_sample"]["answered"] == kd.CPU_SAMPLE
    assert s["jobs"]["gpu-q8_0-fresh"]["gpu_used"] is False
    m = json.loads((tmp_path / s["jobs"]["gpu-q8_0-fresh"]["dev_run"] / "manifest.json").read_text())
    assert "ran on the CPU" in m["runtime"]["engine"]
    assert "**GPU not used" in (run_dir / "report.md").read_text()
    # a timing-only job is not a scored run: it stays in the deploy run dir
    t = s["jobs"]["gpu-q8_0-timing"]
    assert "dev_run" not in t and t["timing_sample"]["answered"] == kd.CPU_SAMPLE
    assert (run_dir / "gpu-q8_0-timing" / "outputs.jsonl").exists()
    for fmt in ("q8_0",):
        cpu = s["jobs"][f"cpu-{fmt}"]
        assert cpu["answered"] == kd.CPU_SAMPLE and cpu["vs_same_format_on_gpu"]["same_text"] == kd.CPU_SAMPLE
        assert (run_dir / f"cpu-{fmt}" / "outputs.jsonl").exists()
    shutil.rmtree(tmp_path / "runs")


def test_llama_cpp_library_path_keeps_the_machines_own(tmp_path, monkeypatch):
    """Run 2 (2026-11-05): replacing LD_LIBRARY_PATH hid libcuda.so.1, so the CUDA backend never loaded."""
    k = _kernel(tmp_path, monkeypatch)
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "libggml-cuda.so").write_text("")
    monkeypatch.setenv("LD_LIBRARY_PATH", "/usr/local/nvidia/lib64:/usr/local/cuda/lib64")
    monkeypatch.setattr(k, "driver_lib", lambda: None)
    dirs = k.lib_dirs(tmp_path / "build").split(":")
    assert dirs == [str(tmp_path / "build"), "/usr/local/nvidia/lib64", "/usr/local/cuda/lib64"]
