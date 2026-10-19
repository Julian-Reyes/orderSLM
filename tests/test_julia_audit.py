"""Julia-1 label audit on Kaggle: the same wording as the hosted providers, and kernel output → saved responses."""

import json

from orderslm.eval import julia_audit as ja
from orderslm.eval import label_audit as la
from orderslm.paths import ROOT
from orderslm.providers.hosted import load_hosted, to_wire


def _dev_020():
    return [j for j in la.dev_jobs() if j["id"].startswith("a-dev-020")]


def _kernel_line(req: dict, choice: str = "PLACE_ORDER", p_true: float = 0.9) -> dict:
    answers = {}
    for name, q in req["questions"].items():
        if q["type"] == "choice":
            probs = {k: (0.9 if k == choice else 0.1 / (len(q["criteria"]) - 1)) for k in q["criteria"]}
            answers[name] = {
                "type": "choice",
                "choice": choice,
                "probabilities": probs,
                "max_probability": 0.9,
            }
        else:
            answers[name] = {
                "type": "noul",
                "noul": p_true,
                "probabilities": {"false": 1 - p_true, "true": p_true},
            }
    return {"id": req["id"], "latency_ms": 12.5, "input_tokens": 300, "answers": answers}


def test_julia_gets_the_same_state_and_questions_as_jev():
    req = _dev_020()[0]["request"]
    jev = to_wire(load_hosted()["jev"], req)
    julia = ja.to_julia(req)
    assert julia["state"] == jev["state"] and julia["questions"] == jev["questions"]


def test_kernel_answers_become_decision_responses_with_no_invented_confidence():
    req = _dev_020()[0]["request"]
    resp = ja.from_julia(req, _kernel_line(ja.to_julia(req), p_true=0.3))
    assert resp.provider == "julia-1" and resp.cost_micros == 0 and resp.usage.input_tokens == 300
    assert resp.answers["order_ok"].boolean is False and resp.answers["order_ok"].probabilities["true"] == 0.3
    assert all(a.confidence is None for a in resp.answers.values())


def test_import_saves_responses_and_scores_like_any_provider(tmp_path):
    jobs = _dev_020()
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    manifest = {"set": "dev", "batches": None, "providers": ["julia-1"], "job_ids": [j["id"] for j in jobs]}
    (run_dir / "manifest.json").write_text(json.dumps(manifest))
    out = tmp_path / "out"
    out.mkdir()
    lines = [
        _kernel_line(ja.to_julia(j["request"]), p_true=0.9 if j["kind"] == "gold" else 0.1) for j in jobs
    ]
    lines[-1] = {"id": jobs[-1]["id"], "error": "ValueError: boom"}
    (out / "outputs.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    (out / "env.json").write_text(json.dumps({"run_dir": "run", "torch": "x"}))
    m = ja.import_(run_dir, out)["julia-1"]
    assert m["errors"] == 1 and m["order_flagged"] == 0
    assert sum(v["caught"] for v in m["planted"].values()) == len(jobs) - 2
    assert (run_dir / "kernel" / "env.json").exists() and (run_dir / "report.md").exists()
    assert json.loads((run_dir / "manifest.json").read_text())["answered"] == len(jobs)


def test_kernel_pins_the_same_model_and_stays_private():
    script = (ROOT / "kaggle" / "julia-audit" / "run.py").read_text()
    assert f'REVISION = "{ja.REVISION}"' in script
    meta = json.loads((ROOT / "kaggle" / "julia-audit" / "kernel-metadata.json").read_text())
    assert meta["is_private"] is True and meta["dataset_sources"] == [ja.DATASET]
    assert not meta["enable_gpu"]


def test_sanity_cases_cover_every_group_and_convert():
    jobs = ja.sanity_jobs()
    ids = [j["id"] for j in jobs]
    assert len(ids) == len(set(ids)) and "card-example" in ids
    assert {i.split("-")[0] for i in ids} == {"card", "plain", "chat", "order"}
    assert all(ja.to_julia(j["request"])["questions"] for j in jobs)


def test_variants_change_one_thing_and_merge_back_to_full_rows():
    from orderslm.eval import julia_variants as jv

    jobs = _dev_020()
    reqs = jv.build(jobs)
    gold = jobs[0]
    by_id = {r["id"]: r for r in reqs}
    base = by_id[f"base|{gold['id']}"]
    assert base["questions"] == ja.to_julia(gold["request"])["questions"]
    shuf = by_id[f"shuf0|{gold['id']}"]["questions"]["intent_m0"]["criteria"]
    assert shuf == base["questions"]["intent_m0"]["criteria"] and list(shuf) != list(
        base["questions"]["intent_m0"]["criteria"]
    )
    short = [r for r in reqs if r["id"].startswith(f"short|{gold['id']}|")]
    assert len(short) == len(gold["intents"]) and all("[" not in r["state"].split("\n", 1)[1] for r in short)
    assert by_id[f"yesno|{gold['id']}"]["questions"]["order_ok"]["criteria"] == jv.YES_NO_CRITERIA
    outputs = {}
    for r in reqs:
        line = _kernel_line(r, choice="SMALL_TALK" if r["id"].startswith("short") else "PLACE_ORDER")
        outputs[r["id"]] = line
    merged = jv.merge(gold["id"], outputs)
    assert set(merged) == set(jv.VARIANTS)
    assert merged["julia-1-short"]["answers"]["intent_m0"]["choice"] == "SMALL_TALK"
    assert merged["julia-1"]["answers"]["intent_m0"]["choice"] == "PLACE_ORDER"
    assert merged["julia-1-shuf-avg"]["answers"]["intent_m0"]["choice"] == "PLACE_ORDER"
    for rec in merged.values():
        ja.from_julia(gold["request"], rec)
