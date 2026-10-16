"""Request pacing per model (simplified port of AgentDesk server/src/llm/throttle.ts).

Synchronous and requests-per-minute only: calls are spaced 60/rpm seconds apart. The token-window
limiter is not ported yet; OrderSLM's rpm settings sit far below every provider's limits. It sits
inside the cache, so replays never wait.
"""

import threading
import time
from collections.abc import Callable

from .types import ChatClient, ChatRequest, ChatResponse


class Throttle:
    def __init__(
        self,
        rpm: int,
        *,
        now: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ):
        if rpm <= 0:
            raise ValueError("rpm must be positive")
        self._interval = 60.0 / rpm
        self._now = now
        self._sleep = sleep
        self._next: float | None = None
        self._lock = threading.Lock()

    def wait(self) -> None:
        """Reserve the next slot under a lock (safe across threads), then sleep until it outside the lock."""
        with self._lock:
            t = self._now()
            slot = t if self._next is None or t >= self._next else self._next
            self._next = slot + self._interval
        if slot > t:
            self._sleep(slot - t)


class ThrottledClient:
    def __init__(self, inner: ChatClient, throttle: Throttle):
        self._inner = inner
        self._throttle = throttle

    @property
    def config_id(self) -> str:
        return self._inner.config_id

    def complete(self, request: ChatRequest) -> ChatResponse:
        self._throttle.wait()
        return self._inner.complete(request)
