"""The API teacher: one prompt and one JSON schema, identical for every provider (spec §8).

The prompt is versioned (TEACHER_PROMPT_VERSION; text in prompts/). The schema sent to providers is a
*portable* rendering of ExtractionOutput: inlined (no $ref), every property required, objects closed, and
without the constraints some providers reject (Anthropic: numeric/length limits, minItems > 1). The schema
text is also in the prompt, because DeepSeek has a JSON-object mode only. Full validation always happens in
code (parse_model_output), so the portable schema only guides the model.
"""

import copy
import json
from importlib.resources import files
from typing import Any

from orderslm.interfaces.decision import Usage
from orderslm.interfaces.extractor import ExtractionRequest, ExtractionResult, parse_model_output
from orderslm.llm.types import ChatClient, ChatMessage, ChatRequest, ChatResponse
from orderslm.schema.extraction import ExtractionOutput

TEACHER_PROMPT_VERSION = "teacher-extract@0.4"  # 0.2: half-and-half line shape; 0.3: no items for
# past orders; 0.4: plain pending decision has no evidence
MAX_OUTPUT_TOKENS = 16000  # room for reasoning variants; billing is for tokens used
_DROP = {
    "title",
    "default",
    "pattern",
    "format",
    "minLength",
    "maxLength",
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "multipleOf",
    "minItems",
    "maxItems",
}


def prompt_text(version: str = TEACHER_PROMPT_VERSION) -> str:
    return (files("orderslm.extractors") / "prompts" / f"{version}.md").read_text()


def portable_schema(model: type = ExtractionOutput) -> dict[str, Any]:
    full = model.model_json_schema()
    defs = full.pop("$defs", {})

    def walk(node: Any, seen: tuple[str, ...]) -> Any:
        if isinstance(node, list):
            return [walk(n, seen) for n in node]
        if not isinstance(node, dict):
            return node
        if "$ref" in node:
            name = node["$ref"].rsplit("/", 1)[-1]
            if name in seen:
                raise ValueError(f"recursive schema at {name}: not portable")
            target = copy.deepcopy(defs[name])
            if "description" in node:
                target["description"] = node["description"]
            return walk(target, (*seen, name))
        out = {k: walk(v, seen) for k, v in node.items() if k not in _DROP}
        if "allOf" in out and len(out["allOf"]) == 1:  # pydantic wraps a described $ref this way
            inner = out.pop("allOf")[0]
            out = {**inner, **out}
        if "const" in out:
            out["enum"] = [out.pop("const")]
        if out.get("type") == "object" and "properties" in out:
            out["required"] = list(out["properties"])
            out["additionalProperties"] = False
        return out

    return walk(full, ())


def build_chat_request(request: ExtractionRequest, schema: dict[str, Any] | None = None) -> ChatRequest:
    schema = schema if schema is not None else portable_schema()
    system = (
        prompt_text()
        + "\n# JSON schema\nThe output must be one JSON object valid against this schema:\n"
        + json.dumps(schema, separators=(",", ":"))
        + "\n"
    )
    menu = request.menu.model_dump_json(exclude_none=True)
    lines = [
        f"[{m.index}] {m.role.value} {m.sent_at.isoformat()}: {m.text}" for m in request.conversation.messages
    ]
    user = (
        f"Menu (JSON):\n{menu}\n\n"
        f"Conversation (language {request.conversation.language}; [message_index] role time: text):\n"
        + "\n".join(lines)
        + "\n\nReturn the order after the last message as one JSON object."
    )
    if request.draft is not None:
        user += f"\n\nCurrent draft order (JSON):\n{request.draft.model_dump_json()}"
    return ChatRequest(
        system=system,
        messages=[ChatMessage(role="user", content=user)],
        json_schema=schema,
        schema_name="order_extraction",
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )


def to_result(response: ChatResponse) -> ExtractionResult:
    result = parse_model_output(
        response.config_id,
        response.text,
        latency_ms=response.latency_ms,
        usage=Usage(input_tokens=response.usage.input_tokens, output_tokens=response.usage.output_tokens),
    )
    if response.finish_reason in ("length", "max_tokens", "refusal") and result.error is None:
        result.error = f"finish_reason={response.finish_reason}"
    return result.model_copy(update={"cost_micros": response.cost_micros, "cached": response.cached})


class TeacherExtractor:
    """OrderExtractor over any ChatClient (cached + throttled in practice)."""

    def __init__(self, client: ChatClient):
        self._client = client
        self._schema = portable_schema()

    @property
    def name(self) -> str:
        return self._client.config_id

    def extract(self, request: ExtractionRequest) -> ExtractionResult:
        return to_result(self._client.complete(build_chat_request(request, self._schema)))
