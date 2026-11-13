# ruff: noqa  (one-off check script kept as the record of what ran)
# Ran in a scratch venv: `uv venv && uv pip install xgrammar==0.2.8 transformers==5.20.2 pydantic`; HF_HOME pointed at a
# folder holding only the pinned Qwen3.5-0.8B tokenizer/config (no weights). Results: results.json.
"""Does the student@0.2 JSON-schema grammar accept every training answer and every valid v4 answer, token by token?"""

import glob
import json
import sys
import time

import xgrammar as xgr
from transformers import AutoTokenizer

sys.path.insert(0, "/Users/julianreyes/Documents/Github/orderslm/src")
from orderslm.schema.label import StudentOutput

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-0.8B", revision="2fc06364715b967f1860aea9cf38778875588b17")
info = xgr.TokenizerInfo.from_huggingface(tok, vocab_size=248320, stop_token_ids=[tok.eos_token_id])


def loosen(x):
    if isinstance(x, dict):
        return {k: loosen(v) for k, v in x.items() if k not in ("maxLength", "minLength")}
    return [loosen(v) for v in x] if isinstance(x, list) else x


t = time.time()
compiled = xgr.GrammarCompiler(info).compile_json_schema(
    json.dumps(loosen(StudentOutput.model_json_schema())),
    any_whitespace=False,
    separators=(",", ":"),
    strict_mode=True,
)
print(f"compiled in {time.time() - t:.1f}s")


def accepts(text):
    m = xgr.GrammarMatcher(compiled)
    for i in tok.encode(text.rstrip("\n"), add_special_tokens=False):
        if not m.accept_token(i):
            return False
    return m.accept_token(tok.eos_token_id) and m.is_terminated()


R = "/Users/julianreyes/Documents/Github/orderslm/runs"
bad, n = [], 0
for part in ("train", "valid"):
    for line in open(f"{R}/student-data/student-data@0.5/single/{part}.jsonl"):
        a = json.loads(line)["messages"][2]["content"]
        n += 1
        if not accepts(a):
            bad.append(("target", a[:200]))
print(f"targets: {n - len([b for b in bad if b[0] == 'target'])}/{n} accepted")
vn = vbad = 0
for f in glob.glob(f"{R}/student-dev/2026111[23]T*-qwen3.5-0.8b-single-v4*/outputs.jsonl"):
    for line in open(f):
        r = json.loads(line)
        if "text" not in r:
            continue
        try:
            StudentOutput.model_validate_json(r["text"])
        except Exception:
            continue
        vn += 1
        if not accepts(r["text"]):
            vbad += 1
            bad.append(("v4", r["id"], r["text"][:200]))
print(f"valid v4 outputs: {vn - vbad}/{vn} accepted")
for b in bad[:5]:
    print(b)

for b in bad:
    if b[0] == "target":
        full = next(
            json.loads(l)["messages"][2]["content"]
            for p in ("train", "valid")
            for l in open(f"{R}/student-data/student-data@0.5/single/{p}.jsonl")
            if json.loads(l)["messages"][2]["content"].startswith(b[1])
        )
        m = xgr.GrammarMatcher(compiled)
        ok = m.accept_string(full.rstrip("\n"))
        # find failing prefix by binary search on characters
        lo, hi = 0, len(full)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            mm = xgr.GrammarMatcher(compiled)
            if mm.accept_string(full[:mid]):
                lo = mid
            else:
                hi = mid - 1
        print("fails at", lo, repr(full[max(0, lo - 150) : lo + 60]))
