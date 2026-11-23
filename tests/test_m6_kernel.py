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


def test_file_listing_skips_cli_warnings():
    from orderslm import kaggle_jobs

    out = (
        "Warning: Looks like you're using an outdated `kaggle` version (installed: 2.2.4)\n"
        "name,size,creationDate\n"
        "adapters/b/README.md,5182,2026-10-23 11:57:55.679000\n"
        "run.json,2060,2026-10-23 11:57:55.675000\n"
    )
    assert kaggle_jobs.parse_file_listing(out) == {"adapters/b/README.md", "run.json"}


def test_bucket_pads_to_the_multiple_and_keeps_the_answer_logits(tmp_path, monkeypatch):
    k = _kernel(tmp_path, monkeypatch)
    assert k.bucket([5, 6, 7], None, 0) == [5, 6, 7]
    assert k.bucket([5, 6, 7], 4, 0) == [5, 6, 7, 0]
    assert k.bucket(list(range(8)), 4, 0) == list(range(8))
    for n, offset, multiple in ((300, 250, 128), (256, 10, 128), (1000, 999, 64)):
        big = len(k.bucket([1] * n, multiple, 0))
        assert big % multiple == 0 and 0 <= big - n < multiple
        keep = big - offset + 1  # logits_to_keep: the last `keep` positions
        kept = list(range(big - keep, big))[: n - offset]
        assert kept == list(range(offset - 1, n - 1))  # each predicts the next answer token, never padding


def test_other_scoring_waits_behind_the_training_that_finishes():
    """v0.2 session 2: GPU 1 trains 2B single v2 all session, so every other scoring queues behind GPU 0."""
    jobs = kaggle_train.assign_gpus(
        ["qwen3.5-2b-mixed-v2", "qwen3.5-2b-single-v2"],
        ["qwen3.5-2b-mixed-v2", "qwen3.5-2b-single", "qwen3.5-2b-mixed"],
    )
    assert [j for j in jobs if j[0] == "score"] == [
        ("score", "qwen3.5-2b-mixed-v2", 0),
        ("score", "qwen3.5-2b-single", 0),
        ("score", "qwen3.5-2b-mixed", 0),
    ]


def test_grammar_schema_drops_only_string_length_limits():
    from orderslm.schema.label import StudentOutput

    full, loose = StudentOutput.model_json_schema(), kaggle_train.grammar_schema()
    text = str(loose)
    assert "maxLength" not in text and "minLength" not in text
    assert "maxLength" in str(full)  # the contract still has them (validation checks them after decoding)

    def strip(x):
        if isinstance(x, dict):
            return {k: strip(v) for k, v in x.items() if k not in ("maxLength", "minLength")}
        return [strip(v) for v in x] if isinstance(x, list) else x

    assert strip(full) == loose


def test_constrained_scoring_needs_the_schema_file(tmp_path, monkeypatch):
    k = _kernel(tmp_path / "out", monkeypatch)
    src = tmp_path / "in"
    run = {
        "generation": {"constrained": {"schema": "student-schema.json"}},
        "jobs": [{"kind": "score", "requests": "fresh3-requests.jsonl", "constrained": True}],
    }
    _write(src / "fresh3-requests.jsonl")
    assert k.missing_inputs(run, src) == ["student-schema.json"]
    _write(src / "student-schema.json")
    assert k.missing_inputs(run, src) == []


def test_grammar_and_generate_share_every_stop_token(tmp_path, monkeypatch):
    """Session A (2026-11-16): the grammar knew only the tokenizer's EOS (248046) and `generate` stopped only on the
    model's (248044), so every constrained answer crashed after its last token. Both must get the union."""
    from types import SimpleNamespace as NS

    k = _kernel(tmp_path, monkeypatch)
    tok = NS(eos_token_id=248046)
    assert k.stop_token_ids(tok, NS(eos_token_id=248044)) == [248044, 248046]
    assert k.stop_token_ids(tok, NS(eos_token_id=[248044, 248046])) == [248044, 248046]
    assert k.stop_token_ids(tok, NS(eos_token_id=None)) == [248046]
    src = (ROOT / "kaggle" / "m6" / "run.py").read_text()
    assert "stop_token_ids=stop_ids" in src and '"eos_token_id": stop_ids' in src


def test_finished_grammar_allows_only_stop_tokens_and_asks_no_mask(tmp_path, monkeypatch):
    """After the grammar accepts a stop token, xgrammar raises if asked for another mask (the session A crash):
    the processor must not ask, and must leave only stop tokens."""
    import sys
    import types

    class T:
        """The few torch.Tensor operations the processor uses, batch of one (torch isn't installed locally)."""

        device = "cpu"

        def __init__(self, rows):
            self.rows = [list(r) for r in rows]

        def __getitem__(self, key):
            if isinstance(key, int):
                return Row(self.rows[key])
            i, j = key
            if isinstance(i, slice):
                return T([[r[c] for c in j] for r in self.rows])
            return self.rows[i][j]

        def __setitem__(self, key, value):
            _, cols = key
            for r, vals in zip(self.rows, value.rows, strict=True):
                for c, v in zip(cols, vals, strict=True):
                    r[c] = v

        def clone(self):
            return T(self.rows)

        def fill_(self, v):
            self.rows = [[v] * len(r) for r in self.rows]
            return self

        def to(self, device):
            return self

    class Row(list):
        def argmax(self):
            return max(range(len(self)), key=self.__getitem__)

    def tensor(x):
        return T(x)

    calls = {"fill": 0}

    class Matcher:
        def __init__(self, compiled):
            self.done = False

        def accept_token(self, t):
            assert not self.done, "accepted a token after terminating"
            self.done = t in (1, 2)

        def is_terminated(self):
            return self.done

        def is_completed(self):
            return self.done

        def fill_next_token_bitmask(self, bitmask):
            assert not self.done, "asked for a mask after terminating"
            calls["fill"] += 1

    fake = types.SimpleNamespace(
        GrammarMatcher=Matcher,
        allocate_token_bitmask=lambda n, v: tensor([[0.0] * v] * n),
        apply_token_bitmask_inplace=lambda scores, mask: None,
    )
    monkeypatch.setitem(sys.modules, "xgrammar", fake)
    k = _kernel(tmp_path, monkeypatch)
    transformers = types.SimpleNamespace(LogitsProcessor=object)
    compiled = types.SimpleNamespace(tokenizer_info=types.SimpleNamespace(vocab_size=5))
    p = k.grammar_processor_factory(compiled, transformers, [1, 2])()
    p(tensor([[0]]), tensor([[0.0] * 5]))
    p(tensor([[0, 3]]), tensor([[0.0] * 5]))  # a JSON token
    out = p(tensor([[0, 3, 2]]), tensor([[0.0, 0.5, 0.2, 9.0, 1.0]]))  # the stop token
    assert calls["fill"] == 2
    assert out[0, 3] == float("-inf") and out[0, 0] == float("-inf") and out[0, 4] == float("-inf")
    assert out[0, 1] == 0.5 and out[0, 2] == 0.2
    p(tensor([[0, 3, 2, 1]]), tensor([[0.0] * 5]))  # still no mask, no accept after the end


def _fake_scoring(monkeypatch, generate):
    """torch / transformers / peft stand-ins for score_job (none is installed locally); `generate` is the model's."""
    import contextlib
    import sys
    import types

    class Ids:
        shape = (1, 3)

        def to(self, dev):
            return self

    class Out:
        def __getitem__(self, key):
            return types.SimpleNamespace(shape=(2,))

    class Tok:
        pad_token_id, eos_token_id = 0, 1

        def apply_chat_template(self, *a, **kw):
            return {"input_ids": Ids()}

        def decode(self, ids, skip_special_tokens=True):
            return "{}"

    class Model:
        def eval(self):
            return self

        def generate(self, ids, **kw):
            generate()
            return Out()

    torch = types.SimpleNamespace(
        cuda=types.SimpleNamespace(is_available=lambda: False),
        device=lambda d: d,
        float16="f16",
        float32="f32",
        inference_mode=contextlib.nullcontext,
        ones_like=lambda x: x,
    )
    transformers = types.SimpleNamespace(
        AutoTokenizer=types.SimpleNamespace(from_pretrained=lambda p: Tok()),
        AutoModelForCausalLM=types.SimpleNamespace(from_pretrained=lambda p, **kw: Model()),
    )
    for name, mod in (
        ("torch", torch),
        ("transformers", transformers),
        ("peft", types.SimpleNamespace(PeftModel=None)),
    ):
        monkeypatch.setitem(sys.modules, name, mod)


def _score(k, tmp_path, n=8):
    import json

    src = tmp_path / "in"
    _write(
        src / "r.jsonl",
        "".join(json.dumps({"id": f"c{i}#0", "system": "s", "user": "u"}) + "\n" for i in range(n)),
    )
    k.no_gqa_flag, k.kernel_paths = (lambda: False), (lambda: {})
    run = {"models": {"0.8b": {"path": "x"}}, "generation": {"max_new_tokens": 5}, "deadline_hours": 1}
    job = {"name": "s", "model": "0.8b", "requests": "r.jsonl", "after_train": None}
    k.score_job(job, run, src, __import__("time").time())
    out = tmp_path / "out" / "s"
    recs = [json.loads(x) for x in (out / "outputs.jsonl").read_text().splitlines()]
    return json.loads((out / "status.json").read_text()), recs


def test_scoring_stops_when_every_first_request_crashes(tmp_path, monkeypatch):
    """Session A spent ~6 h of GPU on 1,485 requests that all crashed alike: stop after the first CRASH_STOP."""

    def crash():
        raise RuntimeError("GrammarMatcher has terminated")

    _fake_scoring(monkeypatch, crash)
    k = _kernel(tmp_path / "out", monkeypatch)
    status, recs = _score(k, tmp_path)
    assert status == {"status": "crashed", "answered": 0, "errors": k.CRASH_STOP}
    assert len(recs) == k.CRASH_STOP


def test_resumed_scoring_retries_crashed_requests(tmp_path, monkeypatch):
    """A crash is no answer: a resumed session answers it again, and status counts the last record per id."""
    import json

    _fake_scoring(monkeypatch, lambda: None)
    k = _kernel(tmp_path / "out", monkeypatch)
    _write(
        tmp_path / "out" / "s" / "outputs.jsonl",
        json.dumps({"id": "c0#0", "text": "{}"})
        + "\n"
        + json.dumps({"id": "c1#0", "error": "RuntimeError: x"})
        + "\n",
    )
    status, recs = _score(k, tmp_path, n=3)
    assert status == {"status": "done", "answered": 3, "errors": 0}
    assert [r["id"] for r in recs] == ["c0#0", "c1#0", "c1#0", "c2#0"]  # c0 kept, c1 retried, c2 new
