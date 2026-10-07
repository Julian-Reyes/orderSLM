# Dev and test splits

Evaluation data comes from three sources (spec §7), and **every result is reported per source**:

| Source | What | Where | Size |
|---|---|---|---|
| A | Claude-written chats from scenario cards (`source: claude_written`), reviewed by Julian | `data/dev/`, `data/test/` | dev ~80, test ~170 |
| B | PIZZA test orders, converted (`split: benchmark`); human-written, items only | `data/external/pizza/` (never committed) | 199 |
| C | Optional: Julian-written (`source: human`) | `data/test/` | ~30 |

Source A is **evaluation data only**: its cards and conversations never feed synthetic generation, few-shot
examples (other than dev for prompt tuning) or training. One `AnnotatedConversation` JSON per conversation:
`data/dev/<id>.json`, `data/test/<id>.json`. Code: `src/orderslm/data/splits.py`, `src/orderslm/data/cards.py`.

## Scenario cards (Source A)

```
uv run python -m orderslm.data.cards summary --split dev
ORDERSLM_UNSEAL_TEST="author Source A cards" uv run python -m orderslm.data.cards generate
```

80 dev + 170 test cards (`data/dev/cards.jsonl`, sealed `data/test/cards.jsonl`), seed 20261007. Each card fixes
the business, situation (+ variant), the router labels the conversation must contain, scenario tags, writing
style and features (typos, abbreviations, emoji, bursts, ALL CAPS), fulfillment, a target number of customer
messages, a persona and a brief. Coverage is by construction: fixed per-split quotas for 23 situations cover
every router label and tricky case in both splits (tested); every business menu appears in dev, and the held-out
menu (Lucky Lime) only in test. Claude writes exactly one conversation per card; the conversation id is the card
id. Splitting by card means no conversation is written from the same card in both splits; near-duplicates are
also checked across splits at lock time.

A Source A conversation must follow its card: same business, and every expected label present in the gold
routing (blocking). Missing scenario tags or a different style are warnings.

## Review (Source A)

Julian reviews **all of dev and at least 25% of test** in the tool. "Save as reviewed" saves his version and
appends to `REVIEWS.jsonl` in that split (reviewer, time, whether the gold changed, hashes). The correction rate
(conversations changed by a review / conversations reviewed) is shown in the stats tab, recorded in LOCK.json
and reported.

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
make lock-test       # ORDERSLM_UNSEAL_TEST="lock M2" python -m orderslm.data.splits lock [--relabel-human]
make verify-test
```

`lock` refuses unless every dev and test file validates, every Source A dev conversation is reviewed, at least
25% of Source A test is reviewed, and no test conversation is a near-duplicate of another test or dev
conversation (customer text, token-set Jaccard ≥ 0.8). It writes `data/test/LOCK.json`: sha256 of every test
file, counts per source, primary/secondary label, scenario, business, style, urgency and conversation length for
both splits, and the review coverage and correction rate. After the lock:

- no new test conversations;
- changing gold needs a reason; each change is appended to `data/test/CHANGES.jsonl` (id, time, reason,
  hashes) per annotation guide §4, and `verify` flags any edit that isn't logged.

## Optional blind relabel (Source C only)

The week-later blind relabel is no longer scheduled by default. `lock --relabel-human` picks up to 30
human-written (Source C) test conversations (`random.Random(20261007)`) with `not_before` = lock date + 7 days;
from then the tool's blind relabel tab shows only the conversation and saves to `data/test/relabel/<id>.json`
without touching the locked files.

## Counts

`make split-stats` prints the dev counts; the stats tab shows them, with review coverage, for either split.
The locked counts are in `data/test/LOCK.json` and get copied into PROGRESS.md when the split is locked.
