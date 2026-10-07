"""Human-written dev and test sets: validation, storage, counts, dedup, and the test lock (docs/SPLITS.md).

Files are `AnnotatedConversation` JSON, one per conversation: `data/dev/<id>.json` and
`data/test/<id>.json`. The test directory is only reached through `paths.test_split_dir()`
(ORDERSLM_UNSEAL_TEST), including for writing it in the annotation tool.

    uv run python -m orderslm.data.splits stats dev
    ORDERSLM_UNSEAL_TEST="lock M2" uv run python -m orderslm.data.splits lock
    ORDERSLM_UNSEAL_TEST="verify" uv run python -m orderslm.data.splits verify
"""

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from pydantic import ValidationError

from orderslm.checks import check_all
from orderslm.core.missing import required_missing
from orderslm.domain.clock import Clock, system_clock
from orderslm.menus import load_menus
from orderslm.paths import DEV, test_split_dir
from orderslm.schema.annotation import AnnotatedConversation
from orderslm.schema.conversation import Role, Split
from orderslm.schema.routing import ORDER_LABELS

EDITABLE = (Split.dev, Split.test)
LOCK_FILE = "LOCK.json"
CHANGES_FILE = "CHANGES.jsonl"
RELABEL_DIR = "relabel"
RELABEL_COUNT = 30
RELABEL_SEED = 20261007
RELABEL_AFTER = timedelta(days=7)
DUPLICATE_JACCARD = 0.8


class SplitError(ValueError):
    pass


def split_dir(split: Split) -> Path:
    if split is Split.dev:
        return DEV
    if split is Split.test:
        return test_split_dir()  # raises SealedSplitError unless unsealed
    raise SplitError(f"{split.value} is not a human-written split")


def relabel_dir() -> Path:
    return test_split_dir() / RELABEL_DIR


# ---------------------------------------------------------------- validation


@dataclass
class Finding:
    code: str
    message: str
    blocking: bool = True


def validate(ac: AnnotatedConversation, split: Split) -> list[Finding]:
    """Everything the annotation tool checks on save. Blocking findings prevent saving."""
    out: list[Finding] = []
    conv = ac.conversation
    if conv.split is not split:
        out.append(
            Finding("WRONG_SPLIT", f"conversation.split is {conv.split.value}, saving to {split.value}")
        )
    if conv.source.value != "human":
        out.append(Finding("NOT_HUMAN", "dev and test conversations are human-written"))
    menus = load_menus(include_held_out=True)
    menu = menus.get(conv.business_id)
    if menu is None:
        out.append(Finding("UNKNOWN_BUSINESS", f"no menu {conv.business_id!r}"))
        return out
    if menu.held_out and split is not Split.test:
        out.append(Finding("HELD_OUT_MENU", f"{menu.name} is held out: test conversations only"))
    sends_to_extractor = any(r.decision.goes_to_extractor for r in ac.gold_routing)
    if ac.gold_extraction is None:
        if sends_to_extractor:
            out.append(
                Finding(
                    "ORDER_WITHOUT_GOLD", "a message is routed to the extractor but gold_extraction is null"
                )
            )
        return out
    for issue in check_all(ac.gold_extraction, conv, menu):
        out.append(Finding(issue.code, f"{issue.path}: {issue.message}"))
    expected = sorted((m.field.value, m.line_id or "") for m in required_missing(ac.gold_extraction, menu))
    got = sorted((m.field.value, m.line_id or "") for m in ac.gold_extraction.missing_or_ambiguous)
    if expected != got:
        out.append(
            Finding(
                "MISSING_INFO_DIFFERS_FROM_RULES",
                f"the guide's rules give {expected}, gold has {got} (docs/ANNOTATION_GUIDE.md, 'What counts as missing')",
            )
        )
    if not sends_to_extractor:
        out.append(
            Finding(
                "GOLD_WITHOUT_ORDER_LABEL", "gold_extraction is set but no message has an order label", False
            )
        )
    return out


def parse(data: dict) -> tuple[AnnotatedConversation | None, list[Finding]]:
    try:
        return AnnotatedConversation.model_validate(data), []
    except ValidationError as e:
        return None, [
            Finding("SCHEMA", f"{'.'.join(map(str, err['loc'])) or '(root)'}: {err['msg']}")
            for err in e.errors()
        ]


# ---------------------------------------------------------------- storage


def dump(ac: AnnotatedConversation) -> str:
    return json.dumps(ac.model_dump(mode="json", exclude_defaults=True), indent=2, ensure_ascii=False) + "\n"


def _sha(text: str | bytes) -> str:
    return hashlib.sha256(text.encode() if isinstance(text, str) else text).hexdigest()


def save(
    ac: AnnotatedConversation,
    split: Split,
    *,
    directory: Path | None = None,
    change_reason: str | None = None,
    clock: Clock | None = None,
) -> Path:
    """Write one conversation. Blocking findings raise. Once the test split is locked, changing a file
    needs a reason and is appended to CHANGES.jsonl (annotation guide §4)."""
    if blocking := [f for f in validate(ac, split) if f.blocking]:
        raise SplitError("; ".join(f"{f.code}: {f.message}" for f in blocking))
    root = directory or split_dir(split)
    path = root / f"{ac.conversation.id}.json"
    text = dump(ac)
    locked = directory is None and (root / LOCK_FILE).exists()
    if locked:
        if not path.exists():
            raise SplitError("the test split is locked: no new conversations")
        if not (change_reason or "").strip():
            raise SplitError("the test split is locked: changing gold needs a reason (it is logged)")
    root.mkdir(parents=True, exist_ok=True)
    before = path.read_text() if path.exists() else None
    path.write_text(text)
    if locked and before != text:
        entry = {
            "id": ac.conversation.id,
            "at": (clock or system_clock())().isoformat(),
            "reason": change_reason,
            "sha256_before": _sha(before or ""),
            "sha256_after": _sha(text),
        }
        with (root / CHANGES_FILE).open("a") as f:
            f.write(json.dumps(entry) + "\n")
    return path


def conversation_files(root: Path) -> list[Path]:
    return sorted(p for p in root.glob("*.json") if p.name != LOCK_FILE)


def load_dir(root: Path, split: Split) -> list[AnnotatedConversation]:
    out = []
    for p in conversation_files(root):
        ac = AnnotatedConversation.model_validate_json(p.read_text())
        if ac.conversation.split is not split:
            raise SplitError(f"{p.name}: split {ac.conversation.split.value}, expected {split.value}")
        if p.stem != ac.conversation.id:
            raise SplitError(f"{p.name}: file name doesn't match id {ac.conversation.id!r}")
        out.append(ac)
    return out


def load_split(split: Split) -> list[AnnotatedConversation]:
    root = split_dir(split)
    return load_dir(root, split) if root.exists() else []


# ---------------------------------------------------------------- counts and dedup


def stats(convs: list[AnnotatedConversation]) -> dict:
    menus = load_menus(include_held_out=True)
    labels: Counter = Counter()
    secondary: Counter = Counter()
    urgency: Counter = Counter()
    for ac in convs:
        for r in ac.gold_routing:
            labels[r.decision.primary.value] += 1
            if r.decision.secondary:
                secondary[r.decision.secondary.value] += 1
            urgency[r.decision.urgency.value] += 1
    customer_msgs = [len(ac.conversation.customer_indices()) for ac in convs]
    return {
        "conversations": len(convs),
        "customer_messages": sum(customer_msgs),
        "by_business": dict(sorted(Counter(ac.conversation.business_id for ac in convs).items())),
        "held_out_menu": sum(menus[ac.conversation.business_id].held_out for ac in convs),
        "by_style": dict(sorted(Counter(ac.style.value for ac in convs).items())),
        "by_scenario": dict(sorted(Counter(s.value for ac in convs for s in ac.scenarios).items())),
        "primary_labels": dict(sorted(labels.items())),
        "secondary_labels": dict(sorted(secondary.items())),
        "urgency": dict(sorted(urgency.items())),
        "with_order": sum(ac.gold_extraction is not None for ac in convs),
        "by_customer_message_count": dict(
            sorted(Counter("1" if n == 1 else "2-3" if n <= 3 else "4+" for n in customer_msgs).items())
        ),
        "order_labels_routed": sum(labels[label.value] for label in ORDER_LABELS),
    }


def _tokens(ac: AnnotatedConversation) -> set[str]:
    text = " ".join(m.text for m in ac.conversation.messages if m.role is Role.customer)
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def near_duplicates(
    a: list[AnnotatedConversation],
    b: list[AnnotatedConversation] | None = None,
    threshold: float = DUPLICATE_JACCARD,
) -> list[tuple[str, str, float]]:
    """Pairs whose customer text has token-set Jaccard >= threshold (within `a`, or between `a` and `b`)."""
    pairs: list[tuple[str, str, float]] = []
    left = [(ac.conversation.id, _tokens(ac)) for ac in a]
    right = left if b is None else [(ac.conversation.id, _tokens(ac)) for ac in b]
    for i, (ia, ta) in enumerate(left):
        for j, (ib, tb) in enumerate(right):
            if b is None and j <= i:
                continue
            union = ta | tb
            score = len(ta & tb) / len(union) if union else 1.0
            if score >= threshold:
                pairs.append((ia, ib, round(score, 3)))
    return pairs


# ---------------------------------------------------------------- lock


def lock(clock: Clock | None = None, seed: int = RELABEL_SEED) -> dict:
    """Seal the test split: file hashes, counts, cross-split dedup, and the blind relabel sample.
    Refuses if already locked or if any check fails. Needs ORDERSLM_UNSEAL_TEST."""
    root = split_dir(Split.test)
    if (root / LOCK_FILE).exists():
        raise SplitError("the test split is already locked")
    dev, test = load_split(Split.dev), load_split(Split.test)
    if not test:
        raise SplitError("no test conversations to lock")
    problems = [
        f"{ac.conversation.id}: {f.code}"
        for split, convs in ((Split.dev, dev), (Split.test, test))
        for ac in convs
        for f in validate(ac, split)
        if f.blocking
    ]
    dupes = near_duplicates(test) + near_duplicates(test, dev)
    problems += [f"near-duplicate {x} ~ {y} ({s})" for x, y, s in dupes]
    if problems:
        raise SplitError("can't lock: " + "; ".join(problems))
    now = (clock or system_clock())()
    ids = sorted(ac.conversation.id for ac in test)
    relabel = sorted(random.Random(seed).sample(ids, min(RELABEL_COUNT, len(ids))))
    record = {
        "locked_at": now.isoformat(),
        "files": {p.name: _sha(p.read_bytes()) for p in conversation_files(root)},
        "counts": {"test": stats(test), "dev": stats(dev)},
        "self_consistency": {
            "ids": relabel,
            "seed": seed,
            "not_before": (now + RELABEL_AFTER).date().isoformat(),
            "blind": True,
        },
    }
    record["sha256_all"] = _sha(json.dumps(record["files"], sort_keys=True))
    (root / LOCK_FILE).write_text(json.dumps(record, indent=2) + "\n")
    return record


def verify() -> list[str]:
    """Differences between the test files and LOCK.json, excluding changes logged in CHANGES.jsonl."""
    root = split_dir(Split.test)
    record = json.loads((root / LOCK_FILE).read_text())
    logged: dict[str, str] = {}
    if (root / CHANGES_FILE).exists():
        for line in (root / CHANGES_FILE).read_text().splitlines():
            entry = json.loads(line)
            logged[f"{entry['id']}.json"] = entry["sha256_after"]
    current = {p.name: _sha(p.read_bytes()) for p in conversation_files(root)}
    out = [f"added after lock: {n}" for n in sorted(current.keys() - record["files"].keys())]
    out += [f"removed after lock: {n}" for n in sorted(record["files"].keys() - current.keys())]
    for name, digest in sorted(current.items()):
        expected = logged.get(name, record["files"].get(name))
        if expected is not None and digest != expected:
            out.append(f"changed without a logged reason: {name}")
    return out


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stats", help="counts per label, scenario, business, style")
    s.add_argument("split", choices=[x.value for x in EDITABLE])
    sub.add_parser("dupes", help="near-duplicates within dev (and dev vs test if unsealed)")
    sub.add_parser("lock", help="seal the test split (needs ORDERSLM_UNSEAL_TEST)")
    sub.add_parser("verify", help="check test files against LOCK.json")
    args = ap.parse_args(argv)
    if args.cmd == "stats":
        print(json.dumps(stats(load_split(Split(args.split))), indent=2))
    elif args.cmd == "dupes":
        for x, y, score in near_duplicates(load_split(Split.dev)):
            print(f"{score:.3f}  {x}  {y}")
    elif args.cmd == "lock":
        r = lock()
        sc = r["self_consistency"]
        print(f"locked {len(r['files'])} test conversations; sha256 {r['sha256_all'][:16]}")
        print(f"blind relabel: {len(sc['ids'])} conversations, not before {sc['not_before']}")
    elif args.cmd == "verify":
        problems = verify()
        print("\n".join(problems) or "test split matches LOCK.json")
        raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
