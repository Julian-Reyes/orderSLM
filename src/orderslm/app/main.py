"""Annotation tool API (M2). Serves the built frontend from web/dist when present.

    make annotate        # dev split only
    make annotate-test   # also the sealed test split (sets ORDERSLM_UNSEAL_TEST for this process)

Storage, validation and sealing all go through orderslm.data.splits; the test split
answers 403 unless the process was started with ORDERSLM_UNSEAL_TEST.
"""

import json
import re
from datetime import date
from typing import Any

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from orderslm.core.missing import required_missing
from orderslm.core.pricing import DeterministicPricing
from orderslm.core.replies import template_question
from orderslm.data import splits
from orderslm.domain.clock import Clock, system_clock
from orderslm.menus import load_menus, menu_version
from orderslm.paths import ROOT, SealedSplitError
from orderslm.schema.annotation import AnnotatedConversation, Scenario, WritingStyle
from orderslm.schema.common import ID_PATTERN
from orderslm.schema.conversation import Split
from orderslm.schema.routing import LABEL_DESCRIPTIONS, REFERENCE_DESCRIPTIONS, URGENCY_DESCRIPTIONS

WEB_DIST = ROOT / "web" / "dist"


def _split(name: str) -> Split:
    try:
        split = Split(name)
    except ValueError:
        split = None
    if split not in splits.EDITABLE:
        raise HTTPException(404, f"unknown split {name!r}")
    return split


def _conv_path(split: Split, conv_id: str):
    if not re.fullmatch(ID_PATTERN, conv_id):
        raise HTTPException(400, f"invalid conversation id {conv_id!r}")
    return splits.split_dir(split) / f"{conv_id}.json"


def _findings(items: list[splits.Finding]) -> list[dict]:
    return [{"code": f.code, "message": f.message, "blocking": f.blocking} for f in items]


def _test_open() -> bool:
    try:
        splits.split_dir(Split.test)
    except SealedSplitError:
        return False
    return True


def _lock_record() -> dict | None:
    lock = splits.split_dir(Split.test) / splits.LOCK_FILE
    return json.loads(lock.read_text()) if lock.exists() else None


def create_app(clock: Clock | None = None) -> FastAPI:
    now = clock or system_clock()
    app = FastAPI(title="OrderSLM annotation tool")

    @app.exception_handler(SealedSplitError)
    async def _sealed(_: Request, exc: SealedSplitError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=403)

    @app.exception_handler(splits.SplitError)
    async def _split_error(_: Request, exc: splits.SplitError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=400)

    @app.get("/api/meta")
    def meta() -> dict:
        test_open = _test_open()
        lock = _lock_record() if test_open else None
        return {
            "splits": ["dev", "test"] if test_open else ["dev"],
            "test_locked": lock is not None,
            "labels": {k.value: v for k, v in LABEL_DESCRIPTIONS.items()},
            "urgency": {k.value: v for k, v in URGENCY_DESCRIPTIONS.items()},
            "references": {k.value: v for k, v in REFERENCE_DESCRIPTIONS.items()},
            "scenarios": [s.value for s in Scenario],
            "styles": [s.value for s in WritingStyle],
        }

    @app.get("/api/{split}/menus")
    def menus(split: str) -> dict:
        s = _split(split)
        if s is Split.test:
            splits.split_dir(s)  # sealed check: the held-out menu is for test conversations only
        found = load_menus(include_held_out=s is Split.test)
        return {
            b: {"version": menu_version(m), "menu": m.model_dump(mode="json")}
            for b, m in sorted(found.items())
        }

    @app.get("/api/{split}/conversations")
    def list_conversations(split: str) -> list[dict]:
        s = _split(split)
        log = splits.review_log(s)
        reviewed = {e["id"] for e in log}
        corrected = {e["id"] for e in log if e["changed"]}
        out = []
        for ac in splits.load_split(s):
            out.append(
                {
                    "id": ac.conversation.id,
                    "business_id": ac.conversation.business_id,
                    "scenarios": [s.value for s in ac.scenarios],
                    "style": ac.style.value,
                    "messages": len(ac.conversation.messages),
                    "annotator": ac.annotator,
                    "source": ac.conversation.source.value,
                    "card_id": ac.card_id,
                    "reviewed": ac.conversation.id in reviewed,
                    "corrected": ac.conversation.id in corrected,
                }
            )
        return out

    @app.get("/api/{split}/stats")
    def stats(split: str) -> dict:
        s = _split(split)
        convs = splits.load_split(s)
        return {
            "stats": splits.stats(convs),
            "reviews": splits.review_stats(s, convs),
            "near_duplicates": splits.near_duplicates(convs),
        }

    @app.get("/api/{split}/conversations/{conv_id}")
    def get_conversation(split: str, conv_id: str) -> dict:
        path = _conv_path(_split(split), conv_id)
        if not path.is_file():
            raise HTTPException(404, f"no conversation {conv_id!r}")
        return json.loads(path.read_text())

    @app.post("/api/{split}/check")
    def check(split: str, data: dict[str, Any] = Body(...)) -> dict:  # noqa: B008
        """Validate without saving; also show what the deterministic core derives from the gold."""
        s = _split(split)
        if s is Split.test:
            splits.split_dir(s)
        ac, findings = splits.parse(data)
        if ac is None:
            return {"valid": False, "findings": _findings(findings)}
        result: dict[str, Any] = {"findings": _findings(splits.validate(ac, s))}
        result["valid"] = not any(f["blocking"] for f in result["findings"])
        menu = load_menus(include_held_out=True).get(ac.conversation.business_id)
        if menu is not None and ac.gold_extraction is not None:
            missing = required_missing(ac.gold_extraction, menu)
            result["derived_missing"] = [m.model_dump(mode="json") for m in missing]
            result["template_question"] = (
                template_question(missing, ac.gold_extraction, menu) if missing else None
            )
            quote = DeterministicPricing().quote(menu, ac.gold_extraction)
            result["pricing"] = quote.model_dump(mode="json")
        return result

    @app.put("/api/{split}/conversations/{conv_id}")
    def put_conversation(split: str, conv_id: str, body: dict[str, Any] = Body(...)) -> dict:  # noqa: B008
        s = _split(split)
        ac, findings = splits.parse(body.get("annotated") or {})
        if ac is None:
            raise HTTPException(400, {"findings": _findings(findings)})
        if ac.conversation.id != conv_id:
            raise HTTPException(400, f"conversation.id {ac.conversation.id!r} doesn't match the URL")
        if review := body.get("review"):
            entry = splits.review(
                ac, s, str(review.get("reviewer", "")), change_reason=body.get("change_reason"), clock=now
            )
            return {"saved": f"{conv_id}.json", "review": entry}
        path = splits.save(ac, s, change_reason=body.get("change_reason"), clock=now)
        return {"saved": path.name}

    # ---- blind relabel (self-consistency): the earlier labels are never sent to the browser

    def _relabel_ids() -> tuple[list[str], str]:
        lock = _lock_record()
        if lock is None:
            raise HTTPException(409, "the test split isn't locked yet")
        sc = lock["self_consistency"]
        if sc is None:
            raise HTTPException(
                409, "no blind relabel scheduled (optional, Source C only: lock --relabel-human)"
            )
        if now().date() < date.fromisoformat(sc["not_before"]):
            raise HTTPException(409, f"blind relabel opens on {sc['not_before']}")
        return sc["ids"], sc["not_before"]

    @app.get("/api/relabel")
    def relabel_list() -> dict:
        ids, not_before = _relabel_ids()
        done = (
            {p.stem for p in splits.relabel_dir().glob("*.json")} if splits.relabel_dir().exists() else set()
        )
        return {"ids": ids, "not_before": not_before, "done": sorted(done & set(ids))}

    @app.get("/api/relabel/{conv_id}")
    def relabel_get(conv_id: str) -> dict:
        ids, _ = _relabel_ids()
        if conv_id not in ids:
            raise HTTPException(404, f"{conv_id!r} is not in the relabel sample")
        ac = AnnotatedConversation.model_validate_json(_conv_path(Split.test, conv_id).read_text())
        return {"conversation": ac.conversation.model_dump(mode="json")}  # conversation only: blind

    @app.put("/api/relabel/{conv_id}")
    def relabel_put(conv_id: str, body: dict[str, Any] = Body(...)) -> dict:  # noqa: B008
        ids, _ = _relabel_ids()
        if conv_id not in ids:
            raise HTTPException(404, f"{conv_id!r} is not in the relabel sample")
        ac, findings = splits.parse(body.get("annotated") or {})
        if ac is None:
            raise HTTPException(400, {"findings": _findings(findings)})
        original = AnnotatedConversation.model_validate_json(_conv_path(Split.test, conv_id).read_text())
        if ac.conversation != original.conversation:
            raise HTTPException(400, "the relabel must keep the conversation unchanged")
        path = splits.save(ac, Split.test, directory=splits.relabel_dir(), clock=now)
        return {"saved": path.name}

    if WEB_DIST.is_dir():
        app.mount("/", StaticFiles(directory=WEB_DIST, html=True), name="web")
    return app


app = create_app()
