"""An OrderExtractor that returns scripted raw text, so tests exercise the same parse path as real models."""

from orderslm.interfaces.decision import Usage
from orderslm.interfaces.extractor import ExtractionRequest, ExtractionResult, parse_model_output
from orderslm.schema.extraction import ExtractionOutput


class ScriptedExtractor:
    """Answers by conversation id. A value may be an ExtractionOutput (serialized first) or raw text
    (to simulate a model emitting broken JSON)."""

    def __init__(self, answers: dict[str, ExtractionOutput | str], *, name: str = "fake/extractor"):
        self._name = name
        self._answers = dict(answers)
        self.requests: list[ExtractionRequest] = []

    @property
    def name(self) -> str:
        return self._name

    def extract(self, request: ExtractionRequest) -> ExtractionResult:
        self.requests.append(request)
        answer = self._answers.get(request.conversation.id)
        if answer is None:
            raise KeyError(f"ScriptedExtractor has no answer for {request.conversation.id!r}")
        raw = answer.model_dump_json() if isinstance(answer, ExtractionOutput) else answer
        return parse_model_output(
            self._name, raw, latency_ms=1.0, usage=Usage(input_tokens=500, output_tokens=200)
        )
