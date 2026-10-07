# Dev and test splits

Human-written, labeled conversations (spec §7): **dev ~80** (bake-offs, prompt tuning) and **test ~200, sealed**
(final results only). One `AnnotatedConversation` JSON per conversation: `data/dev/<id>.json`, `data/test/<id>.json`.
Written and labeled by Julian with the annotation tool; code in `src/orderslm/data/splits.py`.

## Writing and labeling

```
make annotate        # http://127.0.0.1:8765, dev split
make annotate-test   # also the test split (this process only gets ORDERSLM_UNSEAL_TEST)
```

The tool checks on every edit and refuses to save until these pass (same rules as `validate()`):

- schema (`extra="forbid"` contracts), `conversation.split` matches the split, `source: human`;
- grounding: every evidence quote is in the cited customer message; every id is on the menu, allowed on the
  item, at most one per exclusive group (`checks.check_all`);
- `missing_or_ambiguous` equals what the guide's rules derive (`core/missing.py`); the tool can fill it, plus
  the template question, with one click;
- the held-out menu (Lucky Lime) only in test;
- a message routed to the extractor needs a gold extraction (a gold extraction with no order label is a warning).

It also shows the deterministic quote for the gold order, so a mislabeled size or add-on shows up as a wrong
price. Unsaved edits are kept in the browser (localStorage) per conversation.

## Locking the test split

```
make lock-test       # ORDERSLM_UNSEAL_TEST="lock M2" python -m orderslm.data.splits lock
make verify-test
```

`lock` refuses unless every dev and test file validates and no test conversation is a near-duplicate of
another test or dev conversation (customer text, token-set Jaccard ≥ 0.8). It writes `data/test/LOCK.json`:
sha256 of every test file, counts per primary/secondary label, scenario, business, style, urgency and
conversation length for both splits, and the self-consistency sample. After the lock:

- no new test conversations;
- changing gold needs a reason; each change is appended to `data/test/CHANGES.jsonl` (id, time, reason,
  hashes) per annotation guide §4, and `verify` flags any edit that isn't logged.

## Self-consistency (blind relabel)

The lock picks 30 test conversations (`random.Random(20261007)`, sorted ids) and records `not_before` =
lock date + 7 days. From that date the tool's **blind relabel** tab shows only the conversation, never the
earlier labels, scenarios or notes, and saves to `data/test/relabel/<id>.json` without touching the locked
files. Agreement per field and per router label is computed with the M3 metrics.

## Counts

`make split-stats` prints the dev counts; the stats tab shows them for either split. The locked counts are
in `data/test/LOCK.json` and get copied into PROGRESS.md when the split is locked.
