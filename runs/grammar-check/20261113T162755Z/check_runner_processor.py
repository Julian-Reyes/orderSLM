# ruff: noqa  (one-off check script kept as the record of what ran)
# Ran in a scratch venv: `uv venv && uv pip install xgrammar==0.2.8 transformers==5.20.2 pydantic`; HF_HOME pointed at a
# folder holding only the pinned Qwen3.5-0.8B tokenizer/config (no weights). Results: results.json.
import importlib.util
import json
import sys

import torch
import transformers
import xgrammar as xgr
from transformers import AutoTokenizer

sys.path.insert(0, "/Users/julianreyes/Documents/Github/orderslm/src")
grammar_schema = lambda: json.load(
    open(
        "/private/tmp/claude-501/-Users-julianreyes-Documents-Github-orderslm/fc1f13d2-2456-471a-855b-58ff3902a4b1/scratchpad/student-schema.json"
    )
)

spec = importlib.util.spec_from_file_location(
    "kr", "/Users/julianreyes/Documents/Github/orderslm/kaggle/m6/run.py"
)
kr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kr)
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-0.8B", revision="2fc06364715b967f1860aea9cf38778875588b17")
V = 248320
info = xgr.TokenizerInfo.from_huggingface(tok, vocab_size=V, stop_token_ids=[tok.eos_token_id])
compiled = xgr.GrammarCompiler(info).compile_json_schema(
    json.dumps(grammar_schema()), any_whitespace=False, separators=(",", ":"), strict_mode=True
)
G = kr.grammar_processor_factory(compiled, transformers)


def run(wanted):
    """Greedy loop where the 'model' always prefers the next token of `wanted` (then EOS)."""
    p, out = G(), []
    ids = torch.tensor([[0]])
    for step in range(1500):
        scores = torch.full((1, V), -10.0)
        scores[0, tok.eos_token_id] = -5.0
        if step < len(wanted):
            scores[0, wanted[step]] = 10.0
        scores = p(ids, scores)
        nxt = int(scores[0].argmax())
        if nxt == tok.eos_token_id:
            break
        out.append(nxt)
        ids = torch.cat([ids, torch.tensor([[nxt]])], 1)
        if step < len(wanted) and nxt != wanted[step]:
            wanted = out[:]  # model 'follows' the steered path: stop preferring the old continuation
    return tok.decode(out), p.steered


target = json.loads(
    open(
        "/Users/julianreyes/Documents/Github/orderslm/runs/student-data/student-data@0.5/single/valid.jsonl"
    ).readline()
)["messages"][2]["content"]
text, steered = run(tok.encode(target + "\n", add_special_tokens=False))
print("valid answer unchanged:", text == target.rstrip("\n"), "steered", steered)
bad = target.replace('"primary":"', '"primary":"PLACE_', 1)
text, steered = run(tok.encode(bad, add_special_tokens=False))
print("invalid intent steered:", steered > 0, "| result:", text[:80])
