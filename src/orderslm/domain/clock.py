"""The current time comes from an injected clock, never datetime.now() inside domain code.

Evals and tests run against a fixed time so an expected answer written today is
still right next year. Ported from AgentDesk server/src/domain/clock.ts.
"""

from collections.abc import Callable
from datetime import UTC, datetime

Clock = Callable[[], datetime]

DEFAULT_FIXED_NOW = "2026-10-07T18:00:00+00:00"


def fixed_clock(iso: str = DEFAULT_FIXED_NOW) -> Clock:
    at = datetime.fromisoformat(iso)
    if at.tzinfo is None:
        raise ValueError(f"Clock time must be timezone-aware: {iso}")
    return lambda: at


def system_clock() -> Clock:
    """Wall clock. Only the app entry points may use this; domain code receives a Clock."""
    return lambda: datetime.now(UTC)
