# ruff: noqa  (one-off check script kept as the record of what ran)
# Ran in a scratch venv: `uv venv && uv pip install xgrammar==0.2.8 transformers==5.20.2 pydantic`; HF_HOME pointed at a
# folder holding only the pinned Qwen3.5-0.8B tokenizer/config (no weights). Results: results.json.
exec(open(__file__.replace("xg_invalid", "xg_check")).read().split("R = ")[0])
import glob

R = "/Users/julianreyes/Documents/Github/orderslm/runs"
for f in sorted(glob.glob(f"{R}/student-dev/2026111[23]T*-qwen3.5-0.8b-single-v4*/outputs.jsonl")):
    for line in open(f):
        r = json.loads(line)
        if "text" not in r:
            continue
        try:
            StudentOutput.model_validate_json(r["text"])
            continue
        except Exception as e:
            err = str(e).splitlines()[1][:90] if len(str(e).splitlines()) > 1 else str(e)[:90]
        print(
            f.split("/")[-2][-14:],
            r["id"],
            "grammar blocks it" if not accepts(r["text"]) else "grammar allows (cross-field rule)",
            "|",
            err,
        )
