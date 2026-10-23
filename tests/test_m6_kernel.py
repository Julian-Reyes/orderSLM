import importlib.util

from orderslm.paths import ROOT
from orderslm.train import kaggle_train


def _kernel(tmp_path, monkeypatch):
    monkeypatch.setenv("ORDERSLM_KAGGLE_OUT", str(tmp_path))
    spec = importlib.util.spec_from_file_location("m6_run", ROOT / "kaggle" / "m6" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MEMINFO = """MemTotal:       32873904 kB
MemFree:         1203320 kB
MemAvailable:    2048000 kB
Cached:         12000000 kB
SwapFree:              0 kB
Shmem:           6500000 kB
"""

MOUNTS = """overlay / overlay rw,relatime 0 0
tmpfs /dev tmpfs rw,nosuid 0 0
/dev/sdb1 /kaggle/working ext4 rw 0 0
tmpfs /tmp tmpfs rw 0 0
"""


def test_meminfo_and_mounts(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    m = k.parse_meminfo(MEMINFO)
    assert m == {"MemTotal": 33.66, "MemAvailable": 2.1, "Cached": 12.29, "SwapFree": 0.0, "Shmem": 6.66}
    assert k.mount_types(MOUNTS) == {"/tmp": "tmpfs", "/kaggle/working": "ext4"}
    assert k.mount_types(MOUNTS, ("/tmp/models/2b", "/usr/lib")) == {
        "/tmp/models/2b": "tmpfs",
        "/usr/lib": "overlay",
    }
    assert k.mount_types("", ("/tmp",)) == {"/tmp": None}


def test_memory_summary():
    samples = [
        {
            "meminfo": {"MemTotal": 33.7, "MemAvailable": 20.0, "Shmem": 1.0},
            "cgroup": {"max": 32.0},
            "rss_gb": {"gpu0": 5.0, "gpu1": 6.0},
        },
        {
            "meminfo": {"MemTotal": 33.7, "MemAvailable": 2.5, "Shmem": 7.0},
            "cgroup": {"max": 32.0},
            "rss_gb": {"gpu0": 9.0, "gpu1": 5.5},
        },
        {"t": 90, "error": "ValueError: x"},
    ]
    assert kaggle_train.memory_summary(samples) == {
        "samples": 2,
        "total_gb": 33.7,
        "min_available_gb": 2.5,
        "max_shmem_gb": 7.0,
        "max_rss_gb": {"gpu0": 9.0, "gpu1": 6.0},
        "cgroup_max_gb": 32.0,
        "errors": 1,
    }
    assert kaggle_train.memory_summary([]) == {}
    assert kaggle_train.memory_summary([{"t": 0, "error": "x"}]) == {"errors": 1}


def test_session_2_puts_scoring_after_the_resumed_0_8b():
    jobs = kaggle_train.assign_gpus(["qwen3.5-2b-mixed", "qwen3.5-0.8b-single"], ["qwen3.5-2b-single"])
    assert jobs == [
        ("train", "qwen3.5-2b-mixed", 0),
        ("train", "qwen3.5-0.8b-single", 1),
        ("score", "qwen3.5-2b-single", 1),
    ]


def test_memory_sampling_never_raises_off_linux(tmp_path, monkeypatch):
    import subprocess

    k = _kernel(tmp_path, monkeypatch)
    p = subprocess.Popen(["sleep", "0"])
    p.wait()
    rec = k.host_memory({0: p})
    assert set(rec) == {"meminfo", "cgroup", "rss_gb"} and set(rec["rss_gb"]) == {"gpu0"}


def test_session_3_scores_each_training_after_it_on_its_gpu():
    jobs = kaggle_train.assign_gpus(
        ["qwen3.5-0.8b-single", "qwen3.5-2b-mixed"],
        ["qwen3.5-2b-single", "qwen3.5-0.8b-single", "qwen3.5-2b-mixed"],
    )
    assert jobs == [
        ("train", "qwen3.5-0.8b-single", 0),
        ("train", "qwen3.5-2b-mixed", 1),
        ("score", "qwen3.5-2b-single", 1),
        ("score", "qwen3.5-0.8b-single", 0),
        ("score", "qwen3.5-2b-mixed", 1),
    ]


def _write(path, text="x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_missing_inputs_names_lost_subfolders(tmp_path, monkeypatch):
    k = _kernel(tmp_path / "out", monkeypatch)
    src = tmp_path / "in"
    run = {
        "jobs": [
            {
                "kind": "train",
                "train_file": "s-train.jsonl",
                "valid_file": "s-valid.jsonl",
                "resume": "resume/a",
            },
            {"kind": "score", "requests": "dev.jsonl", "adapter": "adapters/b"},
            {"kind": "score", "requests": "dev.jsonl", "adapter": "a/best", "after_train": "a"},
        ]
    }
    for f in ("s-train.jsonl", "s-valid.jsonl", "dev.jsonl"):
        _write(src / f)
    # session 2: the top-level files arrived, the folders did not
    assert k.missing_inputs(run, src) == [
        "resume/a/state.pt",
        "resume/a/status.json",
        "adapters/b/adapter_config.json",
        "adapters/b/adapter_model.safetensors",
    ]
    for f in ("resume/a/state.pt", "resume/a/status.json", "adapters/b/adapter_config.json"):
        _write(src / f)
    _write(src / "adapters/b/adapter_model.safetensors")
    assert k.missing_inputs(run, src) == []


def test_score_after_training_runs_only_if_it_finished(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    job = {"after_train": "a"}
    assert k.unfinished_training({"after_train": None}) is None
    assert k.unfinished_training(job) == "a is missing"
    _write(tmp_path / "a" / "status.json", '{"status": "paused"}')
    assert k.unfinished_training(job) == "a is paused"
    _write(tmp_path / "a" / "status.json", '{"status": "done"}')
    assert k.unfinished_training(job) is None


def test_push_check_finds_staged_files_kaggle_did_not_list(tmp_path):
    from orderslm import kaggle_jobs

    for f in ("dataset-metadata.json", "run.json", "resume/a/state.pt", "adapters/b/adapter_config.json"):
        _write(tmp_path / f)
    assert kaggle_jobs.missing_uploads(tmp_path, {"run.json"}) == [
        "adapters/b/adapter_config.json",
        "resume/a/state.pt",
    ]
    listed = {"run.json", "resume/a/state.pt", "adapters/b/adapter_config.json"}
    assert kaggle_jobs.missing_uploads(tmp_path, listed) == []
