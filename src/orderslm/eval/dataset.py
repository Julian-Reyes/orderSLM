"""Which conversations an evaluation may use.

Samples (split "sample") are few-shot material and never evaluated (CLAUDE.md); the test split stays sealed
(only orderslm.paths can open it). The teacher bake-off uses a fixed, seeded subset of dev (spec §8: ~40 conversations),
stratified so the share of conversations without an order matches dev.
"""

import random

from orderslm.data.splits import load_split
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.conversation import Split

BAKEOFF_SIZE = 40
BAKEOFF_SEED = 20261015


class EvalSplitError(ValueError):
    pass


def check_evaluable(convs: list[AnnotatedConversation], split: Split) -> list[AnnotatedConversation]:
    for ac in convs:
        if ac.conversation.split is Split.sample:
            raise EvalSplitError(f"{ac.conversation.id}: samples are few-shot only, never evaluated")
        if ac.conversation.split is not split:
            raise EvalSplitError(
                f"{ac.conversation.id}: split {ac.conversation.split.value}, expected {split.value}"
            )
    return convs


def load_eval_split(split: Split) -> list[AnnotatedConversation]:
    if split is Split.sample:
        raise EvalSplitError("samples are few-shot only, never evaluated")
    return check_evaluable(load_split(split), split)


def remaining_dev(convs: list[AnnotatedConversation]) -> list[AnnotatedConversation]:
    """Dev conversations outside the bake-off set, by id (Julian, 2026-10-15: the head-to-head round)."""
    used = {ac.conversation.id for ac in bakeoff_set(convs)}
    return sorted((ac for ac in convs if ac.conversation.id not in used), key=lambda ac: ac.conversation.id)


def bakeoff_set(
    convs: list[AnnotatedConversation], size: int = BAKEOFF_SIZE, seed: int = BAKEOFF_SEED
) -> list[AnnotatedConversation]:
    """Seeded and stable: the order is the run order, so a pilot of n is the first n with at least one
    no-order conversation once n ≥ 5."""
    rng = random.Random(seed)
    with_order = sorted((c for c in convs if c.gold_extraction is not None), key=lambda c: c.conversation.id)
    without = sorted((c for c in convs if c.gold_extraction is None), key=lambda c: c.conversation.id)
    n_without = round(size * len(without) / len(convs)) if convs else 0
    picked_with = rng.sample(with_order, min(size - n_without, len(with_order)))
    picked_without = rng.sample(without, min(n_without, len(without)))
    # Interleave: every fifth conversation has no order, so pilots see both kinds.
    out: list[AnnotatedConversation] = []
    while picked_with or picked_without:
        take_without = picked_without and (len(out) % 5 == 4 or not picked_with)
        out.append(picked_without.pop(0) if take_without else picked_with.pop(0))
    return out
