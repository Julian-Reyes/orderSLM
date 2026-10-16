"""Near-duplicate detection for synthetic chats (spec §7): word 3-gram Jaccard similarity of the customer text.

A chat is a near-duplicate when its similarity to an earlier kept chat, or to any dev chat, reaches the
threshold. The sealed test split is never read here (it is sealed, CLAUDE.md); the generators
never see Source A, so a match with test would be a coincidence of short chats ("hi", "thanks").
"""

import re
from collections.abc import Iterable

from orderslm.schema.conversation import Conversation, Role

THRESHOLD = 0.8
K = 3


def customer_text(conversation: Conversation) -> str:
    return " ".join(m.text for m in conversation.messages if m.role is Role.customer)


def shingles(text: str, k: int = K) -> frozenset[tuple[str, ...]]:
    words = re.findall(r"[a-z0-9']+", text.casefold())
    if len(words) < k:
        return frozenset({tuple(words)}) if words else frozenset()
    return frozenset(tuple(words[i : i + k]) for i in range(len(words) - k + 1))


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def near_duplicates(
    convs: Iterable[Conversation], against: Iterable[Conversation] = (), threshold: float = THRESHOLD
) -> dict[str, tuple[str, float]]:
    """{conversation id: (the id it duplicates, similarity)} for every chat to drop, in input order."""
    reference = [(c.id, shingles(customer_text(c))) for c in against]
    kept: list[tuple[str, frozenset]] = []
    dupes: dict[str, tuple[str, float]] = {}
    for c in convs:
        s = shingles(customer_text(c))
        best = max(((oid, jaccard(s, o)) for oid, o in reference + kept), key=lambda x: x[1], default=None)
        if best is not None and best[1] >= threshold:
            dupes[c.id] = (best[0], round(best[1], 3))
        else:
            kept.append((c.id, s))
    return dupes
