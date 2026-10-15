"""Confidence intervals for reported rates (ported from AgentDesk server/src/evals/judge/agreement.ts, `wilson`)."""

import math


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """Wilson score interval for a proportion (95% by default). None when n is 0."""
    if n <= 0:
        return None
    if not 0 <= successes <= n:
        raise ValueError(f"successes {successes} not in 0..{n}")
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))
