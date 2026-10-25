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


def mcnemar_exact(a_only: int, b_only: int) -> float:
    """Two-sided exact McNemar p-value from the discordant pairs (items only A got right, only B got right)."""
    n = a_only + b_only
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(a_only, b_only) + 1)) / 2**n
    return min(1.0, 2 * tail)


def holm(pvalues: list[float]) -> list[float]:
    """Holm–Bonferroni adjusted p-values, in the input order."""
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    adjusted, running = [0.0] * len(pvalues), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(pvalues) - rank) * pvalues[i]))
        adjusted[i] = running
    return adjusted


def percentile_interval(values: list[float], level: float = 0.95) -> tuple[float, float]:
    """Percentile interval of bootstrap replicates (nearest rank)."""
    v = sorted(values)
    lo = v[int((1 - level) / 2 * (len(v) - 1))]
    hi = v[int((1 + level) / 2 * (len(v) - 1))]
    return (lo, hi)
