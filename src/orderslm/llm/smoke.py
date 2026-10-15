"""One tiny structured-output call per model, to prove each key, endpoint and JSON mode works.

    uv run python -m orderslm.llm.smoke            # estimate only, no calls
    uv run python -m orderslm.llm.smoke --yes      # live calls (cache off), results in runs/smoke/<id>/

Also records each provider's raw usage object, which settles what the docs leave open (Gemini:
is json_schema enforced on the OpenAI-compatible endpoint; are thinking tokens in completion_tokens).
"""

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime

from orderslm.paths import ROOT, RUNS

from .config import load_models
from .factory import make_client
from .types import ChatMessage, ChatRequest, LLMError, LLMUsage

SMOKE_PROMPT_VERSION = "smoke@0.1"
SCHEMA = {
    "type": "object",
    "properties": {"item": {"type": "string"}, "quantity": {"type": "integer"}},
    "required": ["item", "quantity"],
    "additionalProperties": False,
}
REQUEST = ChatRequest(
    system="You extract food orders. Reply with JSON only.",
    messages=[
        ChatMessage(
            role="user",
            content='Return JSON like {"item": "fries", "quantity": 1} for this message: "two cheeseburgers please"',
        )
    ],
    json_schema=SCHEMA,
    schema_name="smoke",
    max_output_tokens=200,
)
# Generous upper bound for the estimate: the prompt is ~60 tokens, the answer ~20.
ESTIMATE_USAGE = LLMUsage(input_tokens=150, output_tokens=200)


def _git_commit() -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip() or "unknown"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yes", action="store_true", help="make the live calls")
    ap.add_argument("--models", help="comma-separated config ids (default: all)")
    args = ap.parse_args(argv)

    models = load_models()
    ids = args.models.split(",") if args.models else list(models)
    now = datetime.now(UTC)
    print(f"Smoke test, {len(ids)} model(s), one call each ({SMOKE_PROMPT_VERSION}).")
    worst = 0
    for cid in ids:
        est = models[cid].cost_micros(ESTIMATE_USAGE, now)
        worst += est
        print(f"  {cid:32} estimate ≤ ${est / 1e6:.6f}")
    print(f"  total estimate ≤ ${worst / 1e6:.6f}")
    if not args.yes:
        print("Estimate only. Re-run with --yes to make the calls.")
        return 0

    results = []
    spent = 0
    for cid in ids:
        row: dict = {"config_id": cid, "price_verified": models[cid].price_verified}
        try:
            resp = make_client(cid, cache_mode="off").complete(REQUEST)
        except (LLMError, KeyError) as e:
            row.update(ok=False, error=str(e))
            print(f"  {cid:32} FAILED: {e}")
            results.append(row)
            continue
        spent += resp.cost_micros
        try:
            parsed = json.loads(resp.text)
            ok = set(parsed) == {"item", "quantity"} and isinstance(parsed["quantity"], int)
        except (ValueError, TypeError):
            parsed, ok = None, False
        row.update(ok=ok, parsed=parsed, response=resp.model_dump(mode="json"))
        u = resp.usage
        print(
            f"  {cid:32} {'ok ' if ok else 'BAD'} finish={resp.finish_reason} in={u.input_tokens} "
            f"out={u.output_tokens} (reasoning {u.reasoning_tokens}) {resp.latency_ms:.0f} ms "
            f"${resp.cost_micros / 1e6:.6f}  text={resp.text[:80]!r}"
        )
        results.append(row)

    run_id = now.strftime("%Y%m%dT%H%M%SZ")
    out_dir = RUNS / "smoke" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_id": run_id,
        "prompt_version": SMOKE_PROMPT_VERSION,
        "git_commit": _git_commit(),
        "request": REQUEST.model_dump(mode="json"),
        "actual_cost_micros": spent,
        "results": results,
    }
    (out_dir / "results.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Actual cost ${spent / 1e6:.6f}. Saved {out_dir.relative_to(ROOT)}/results.json")
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
