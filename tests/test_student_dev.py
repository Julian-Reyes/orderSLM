"""M6 dev scoring at every customer message: requests match the training format; the scorer reproduces the
teacher's own dev numbers when fed the teacher's labels as per-message answers (positive control)."""

import json

from orderslm.eval import student_dev
from orderslm.eval.student_bakeoff import TEACHER_RUN
from orderslm.llm.types import ChatResponse
from orderslm.menus import load_menu
from orderslm.schema.label import StudentIntent, StudentOutput, TeacherLabel
from orderslm.train import data, kaggle_train


def test_one_request_per_customer_message_and_full_chat_matches_training():
    reqs = student_dev.build_requests()
    assert len(reqs) == 268 and len({r["id"] for r in reqs}) == 268
    from orderslm.eval.dataset import load_eval_split
    from orderslm.schema.conversation import Split

    ac = next(a for a in load_eval_split(Split.dev) if a.conversation.messages[-1].role.value == "customer")
    last = ac.conversation.customer_indices()[-1]
    req = next(r for r in reqs if r["id"] == student_dev.request_id(ac.conversation.id, last))
    assert req["user"] == data.user_prompt(ac.conversation, load_menu(ac.conversation.business_id))
    assert req["system"] == data.system_prompt()


def test_scorer_reproduces_the_teachers_dev_numbers(tmp_path):
    teacher = json.loads((TEACHER_RUN / "metrics.json").read_text())
    lines = []
    for r in student_dev.build_requests():
        rec = json.loads((TEACHER_RUN / "outputs" / f"{r['conversation_id']}.json").read_text())
        if "response" not in rec:
            continue
        try:
            label = TeacherLabel.model_validate_json(ChatResponse.model_validate(rec["response"]).text)
        except ValueError:
            continue
        it = next(i for i in label.intents if i.message_index == r["message_index"])
        out = StudentOutput(
            intent=StudentIntent(primary=it.primary, secondary=it.secondary), order=label.order
        )
        lines.append(
            json.dumps({"id": r["id"], "text": out.model_dump_json(), "latency_ms": 1, "output_tokens": 1})
        )
    (tmp_path / "outputs.jsonl").write_text("\n".join(lines) + "\n")
    (tmp_path / "manifest.json").write_text(json.dumps({"student": "teacher-as-student"}))
    m = student_dev.report(tmp_path)
    assert m["intent"]["all"]["primary_correct"] == teacher["intent"]["primary_correct"]
    assert m["order"]["exact_match"] == teacher["order"]["exact_match"]
    assert m["order"]["item"] == teacher["order"]["item"]


def test_gpu_assignment():
    a = kaggle_train.assign_gpus(["x", "y"], [])
    assert a == [("train", "x", 0), ("train", "y", 1)]
    assert kaggle_train.assign_gpus(["x"], ["s", "t"]) == [
        ("train", "x", 0),
        ("score", "s", 1),
        ("score", "t", 1),
    ]
    assert kaggle_train.assign_gpus([], ["s", "t"]) == [("score", "s", 0), ("score", "t", 1)]
    assert [j[2] for j in kaggle_train.assign_gpus(["x", "y"], ["s", "t"])] == [0, 1, 1, 0]


def test_settings_are_the_agreed_ones():
    t = kaggle_train.TRAIN
    assert t["lora"] == {"r": 16, "alpha": 32, "dropout": 0.05, "target_modules": "all-linear"}
    assert (t["epochs"], t["effective_batch"], t["warmup_share"], t["eval_every_epochs"]) == (2, 8, 0.05, 0.5)
    students = kaggle_train.STUDENTS
    assert {k: v["lr"] for k, v in students.items() if not k.endswith("-v2")} == {
        "qwen3.5-0.8b-single": 2e-4,
        "qwen3.5-2b-single": 1e-4,
        "qwen3.5-2b-mixed": 1e-4,
    }
    # the v0.2 retrains differ from the v0.1 students only in their data
    for name in ("qwen3.5-0.8b-single", "qwen3.5-2b-single", "qwen3.5-2b-mixed"):
        v1, v2 = students[name], students[f"{name}-v2"]
        assert (v1["data_version"], v2["data_version"]) == ("student-data@0.1", "student-data@0.2")
        assert {k: x for k, x in v1.items() if k != "data_version"} == {
            k: x for k, x in v2.items() if k != "data_version"
        }
