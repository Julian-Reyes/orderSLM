"""Money is always an integer number of cents.

Floats can't represent most decimal amounts exactly (0.1 + 0.2 != 0.3), so every
price, fee and total is stored and computed as whole cents, and rounding happens
in one place: here. Ported from AgentDesk server/src/domain/money.ts.
"""

from typing import Annotated

from pydantic import Field, StrictInt

Cents = Annotated[StrictInt, Field(ge=0)]
"""A non-negative amount in cents. Strict: a float or "4.50" is rejected, never coerced."""


def assert_cents(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Not an integer cent amount: {value!r}")
    return value


def percent_of(amount: int, percent: int) -> int:
    """`percent`% of `amount`, rounded half-up to the nearest cent (integer math only)."""
    return (assert_cents(amount) * percent + 50) // 100


def format_cents(amount: int, symbol: str = "$") -> str:
    """Display only. Locale-aware formatting (e.g. "R$ 4,50") is a V2 concern."""
    assert_cents(amount)
    sign = "-" if amount < 0 else ""
    a = abs(amount)
    return f"{sign}{symbol}{a // 100}.{a % 100:02d}"
