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
