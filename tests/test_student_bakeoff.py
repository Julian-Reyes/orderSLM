"""M5 student bake-off: the teacher's own request, one documented normalization, and the teacher's scorer."""

import json

from orderslm.eval import student_bakeoff as sb
from orderslm.paths import ROOT


def test_selection_is_seeded_and_from_dev():
    ids = sb.select_ids()
    assert ids == sb.select_ids() and len(ids) == sb.N_CHATS and all(i.startswith("a-dev-") for i in ids)


def test_fence_strip_is_the_only_normalization():
    assert sb.strip_fences('```json\n{"a": 1}\n```') == '{"a": 1}'
    assert sb.strip_fences('  {"a": 1} ') == '{"a": 1}'
    assert sb.strip_fences('Sure! {"a": 1}') == 'Sure! {"a": 1}'  # prose stays: counted as invalid


def test_import_scores_students_and_the_teacher_baseline(tmp_path):
    ids = sb.select_ids()[:3]
    teacher = {
        cid: json.loads((sb.TEACHER_RUN / "outputs" / f"{cid}.json").read_text())["response"]["text"]
        for cid in ids
    }
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    cands = sb.CANDIDATES[:2]
    manifest = {
        "label_prompt_version": "teacher-label@0.7",
        "seed": sb.SEED,
        "conversation_ids": ids,
        "candidates": cands,
        "teacher_run": str(sb.TEACHER_RUN.relative_to(ROOT)),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest))
    out = tmp_path / "out"
    out.mkdir()
    lines = []
    for cid in ids:  # model 0 echoes the teacher in a fence; model 1 writes prose
        base = {"id": cid, "input_tokens": 9000, "output_tokens": 500, "latency_ms": 2000.0, "at": "t"}
        lines.append(
            {
                **base,
                "model": cands[0]["name"],
                "text": f"```json\n{teacher[cid]}\n```",
                "finish_reason": "stop",
            }
        )
        lines.append({**base, "model": cands[1]["name"], "text": "I can't do that.", "finish_reason": "stop"})
    (out / "outputs.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    (out / "env.json").write_text(json.dumps({"run_dir": "run", "models": {}}))
    s = sb.import_(run_dir, out)
    good, bad, t = s[cands[0]["name"]], s[cands[1]["name"]], s["teacher-gpt-6-luna@low"]
    assert good["raw_json_valid"] == 0 and good["json_valid_after_fence_strip"] == 3
    assert good["item_f1"] == t["item_f1"] and good["exact_orders"] == t["exact_orders"]
    assert bad["contract_valid"] == 0 and bad["items_found"] == 0 and bad["run_errors"] == 0
    assert (run_dir / "report.md").exists() and (run_dir / cands[0]["name"] / "report.md").exists()


def test_kernel_is_private_gpu_and_reads_its_dataset():
    meta = json.loads((ROOT / "kaggle" / "student-bakeoff" / "kernel-metadata.json").read_text())
    assert meta["is_private"] and meta["enable_gpu"] and meta["dataset_sources"] == [sb.DATASET]
    assert meta["id"] != sb.DATASET


def test_diagnose_counts_item_ids_and_contract_errors():
    teacher = {"c": json.dumps({"order": {"items": [{"menu_item_id": "a"}, {"menu_item_id": "b"}]}})}
    student = {"c": json.dumps({"order": {"items": [{"menu_item_id": "a"}, {"menu_item_id": "z"}]}})}
    d = sb.diagnose(student, teacher)
    assert d["item_ids_vs_teacher"] == {"right": 1, "extra": 1, "missed": 1, "f1": 0.5}
    assert d["contract_errors"]  # not a valid label
    d = sb.diagnose({"c": "not json"}, teacher)
    assert d["contract_errors"] == {"(not JSON)": 1} and d["item_ids_vs_teacher"]["missed"] == 2
