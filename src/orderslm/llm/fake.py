"""Scripted chat client so tests never call a real API (port of AgentDesk server/src/llm/fake.ts):
plays back replies in order, records every request, raises when the script runs out."""

from .types import ChatRequest, ChatResponse, LLMUsage


class ScriptedChatClient:
    def __init__(self, replies: list[str | ChatResponse], *, config_id: str = "fake/chat"):
        self._config_id = config_id
        self._replies = list(replies)
        self.requests: list[ChatRequest] = []

    @property
    def config_id(self) -> str:
        return self._config_id

    def complete(self, request: ChatRequest) -> ChatResponse:
        self.requests.append(request)
        if not self._replies:
            raise IndexError(f"ScriptedChatClient {self._config_id}: no scripted reply left")
        reply = self._replies.pop(0)
        if isinstance(reply, ChatResponse):
            return reply
        return ChatResponse(
            config_id=self._config_id,
            model=self._config_id.split("/", 1)[-1],
            text=reply,
            finish_reason="stop",
            usage=LLMUsage(input_tokens=500, output_tokens=200),
            latency_ms=1.0,
            cost_micros=0,
            at="2026-10-07T18:00:00+00:00",
        )
