"""Menu matching: find items, variants and modifiers mentioned in free text.

Deterministic and span-preserving: every match carries the (start, end) offsets
in the original message, so evidence quotes are exact substrings. Matching is
case-insensitive, tolerates plurals ("cokes", "tomatoes") and small typos in
single words ("chesburger"), and prefers the longest phrase ("pepperoni pizza"
beats "pepperoni").
"""

import difflib
import re
from dataclasses import dataclass
from enum import StrEnum

from orderslm.schema.menu import MenuCatalog

TYPO_CUTOFF = 0.86  # difflib ratio; single words of 5+ letters only
STOPWORDS = {"a", "an", "the", "and", "or", "with", "no", "of", "on", "for", "to", "in", "it", "me", "my", "i",
             "pls", "please", "can", "get", "some", "just", "also", "plus", "make", "one", "two", "extra",
             "light", "large", "small", "medium", "regular", "order", "want", "like", "pick", "up", "pickup",
             "delivery", "cash", "card"}  # fmt: skip


class Kind(StrEnum):
    item = "item"
    variant = "variant"
    modifier = "modifier"


@dataclass(frozen=True)
class Match:
    kind: Kind
    target: str  # item id, modifier id, or "item_id:variant_id"
    start: int
    end: int
    text: str  # the original substring
    fuzzy: bool = False


def lower_same_length(text: str) -> str:
    """Lowercase without changing string length, so offsets stay valid for the original text."""
    return "".join(c.lower() if len(c.lower()) == 1 else c for c in text)


def _norm_phrase(p: str) -> str:
    return re.sub(r"[^a-z0-9#'.&+ -]", "", lower_same_length(p)).replace("-", " ").strip()


def _phrase_regex(phrase: str) -> str:
    words = [re.escape(w) for w in phrase.split()]
    body = r"[\s-]+".join(words)
    plural = r"(?:e?s)?" if re.search(r"[a-z]$", phrase) else ""
    return rf"(?<![a-z0-9]){body}{plural}(?![a-z0-9])"


class MenuLexicon:
    def __init__(self, menu: MenuCatalog):
        self.menu = menu
        entries: list[tuple[str, Kind, str]] = []
        for item in menu.items:
            for p in [item.name, *item.aliases]:
                entries.append((_norm_phrase(p), Kind.item, item.id))
            for v in item.variants:
                for p in [v.name, *v.aliases]:
                    entries.append((_norm_phrase(p), Kind.variant, f"{item.id}:{v.id}"))
        for m in menu.modifiers:
            for p in [m.name, *m.aliases]:
                entries.append((_norm_phrase(p), Kind.modifier, m.id))
        entries = [(p, k, t) for p, k, t in entries if p]
        # Longest phrases first so "pepperoni pizza" wins over "pepperoni".
        entries.sort(key=lambda e: (-len(e[0]), e[0]))
        self._compiled = [(re.compile(_phrase_regex(p)), k, t) for p, k, t in entries]
        self._single_words = {p: (k, t) for p, k, t in entries if " " not in p and len(p) >= 5}

    def find(self, text: str, kinds: set[Kind] | None = None) -> list[Match]:
        """All non-overlapping matches, longest phrase first, then by position. Overlaps of different kinds
        at the same span are all returned (e.g. 'pepperoni' as item and as modifier); callers decide."""
        low = lower_same_length(text)
        taken: list[tuple[int, int]] = []
        found: list[Match] = []
        for rx, kind, target in self._compiled:
            if kinds and kind not in kinds:
                continue
            for m in rx.finditer(low):
                s, e = m.span()
                same_span = [f for f in found if (f.start, f.end) == (s, e)]
                if any(a < e and s < b for a, b in taken) and not same_span:
                    continue
                if any(f.kind == kind and f.target == target for f in same_span):
                    continue
                found.append(Match(kind, target, s, e, text[s:e]))
                taken.append((s, e))
        found += self._fuzzy(text, low, taken, kinds)
        return sorted(found, key=lambda f: (f.start, -f.end))

    def _fuzzy(
        self, text: str, low: str, taken: list[tuple[int, int]], kinds: set[Kind] | None
    ) -> list[Match]:
        out = []
        for m in re.finditer(r"[a-z]{5,}", low):
            s, e = m.span()
            word = m.group()
            if word in STOPWORDS or any(a < e and s < b for a, b in taken):
                continue
            close = difflib.get_close_matches(word, self._single_words, n=1, cutoff=TYPO_CUTOFF)
            if close:
                kind, target = self._single_words[close[0]]
                if not kinds or kind in kinds:
                    out.append(Match(kind, target, s, e, text[s:e], fuzzy=True))
        return out


NUMBER_WORDS = {"a": 1, "an": 1, "one": 1, "another": 1, "single": 1, "two": 2, "couple": 2, "pair": 2,
                "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                "eleven": 11, "twelve": 12, "dozen": 12, "fifteen": 15}  # fmt: skip
QTY_BEFORE = re.compile(
    r"(?<![a-z0-9])(?P<q>\d{1,2}|a couple(?: of)?|a pair of|a dozen|a few|some|"
    + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True))
    + r")(?:\s*x)?\s+(?:[a-z0-9-]+\s+){0,3}$"
)


def quantity_before(low_prefix: str) -> tuple[int | None, bool]:
    """(quantity, stated) from the words just before an item. 'some'/'a few' -> (None, True): stated but unclear."""
    m = QTY_BEFORE.search(low_prefix[-40:])
    if not m:
        return 1, False
    q = m.group("q")
    if q in ("some", "a few"):
        return None, True
    if q.isdigit():
        return max(1, min(int(q), 99)), True
    for word, n in NUMBER_WORDS.items():
        if q.endswith(word):
            return n, True
    return 1, True
