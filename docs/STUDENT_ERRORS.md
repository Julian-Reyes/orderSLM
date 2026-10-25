# M6 error review: what the trained students get wrong on dev

_2026-10-25. Run: `runs/student-errors/20261025T193609Z/` (`make student-errors ARGS="<dev runs>"`,
`eval/student_errors.py`, `student-errors@0.1`; free, local, from saved outputs). Dev (tuning), not held-out: once
anything below is fixed, these dev numbers count as "used for fixes", and the effect must be measured on fresh data._

Three students (Qwen3.5-0.8B single, 2B single, 2B mixed; LoRA, `student-data@0.1`) on the 91 dev chats (Source A),
with the teacher (`teacher-label@0.7`, the labels they learned from) as reference. Every mistake is classified by
code: an invalid answer (which rule broke), item mistakes (paired on the dish: missing, extra, or wrong quantity /
variant / modifications / combo picks), order-field mistakes, and intent mistakes per customer message.

## The numbers

| | 0.8B single | 2B single | 2B mixed | teacher |
|---|---|---|---|---|
| chats not fully right (of 91) | 27 | 32 | 26 | 1 |
| · invalid answer | 1 | 5 | 2 | 1 |
| · item mistakes | 19 | 22 | 21 | 0 |
| · field mistakes only | 7 | 5 | 3 | 0 |
| missing items | 14 | 14 | 14 | 0 |
| extra items | 7 | 6 | 6 | 0 |
| wrong modifications (± quantity/variant) | 8 | 10 | 8 | 0 |
| wrong variant (± quantity) | 4 | 4 | 5 | 0 |
| missing-details list wrong | 10 | 11 | 8 | 0 |
| payment wrong | 7 | 4 | 1 | 0 |
| intents wrong (of 268) | 24 | 32 | 27 | 9 |

**The mistakes are shared, not one model's habits:** 19 chats are wrong for all three students (the teacher gets
every one right), 10 for just one; 12 messages get the wrong intent from all three. The three models fail on the
same kinds of chat, which points at the training data rather than model size.

## Why: patterns the training data barely has

| pattern (dev examples) | training answers (of 1,865) | dev gold | what the students do |
|---|---|---|---|
| **same dish on 2+ lines** ("4 cheeseburgers 2 no onion", "2 no pickles"; a-dev-063, 020) | **1 (0.1%)** | 3 of 64 orders (4.7%) | keep 4× and add a 2× "no onion" line (all three), or make "no pickles" an off-menu item that carries a modification (invalid: 10 of the 2Bs' invalid answers) |
| **big orders, 4+ lines** (a-dev-083, 074) | **10 (0.5%)** | 5 of 64 (7.8%) | drop items: a-dev-083 loses the cappuccino, muffin and bagel after a clarifying question about the croissant |
| **ambiguity flags** (a-dev-016, 038, 045, 049) | **5 (0.3%)**, all `item_menu_match` | 4 of 64 orders (incl. quantity and variant ambiguity) | never flag quantity or variant ambiguity; guess instead ("garlic knots" → 1×) |
| **`MODIFY_ORDER`** ("make the fries large", "swap the chocolate for a lemonade") | 54 rows (2.9%) vs 742 `PLACE_ORDER` | 14 messages (5.2%) | `PLACE_ORDER`: 3–5 per student, the same messages for all three |
| **`UNKNOWN`** (".", "👍 SOUNDS GOOD", "ok so the uhh 🤔 w tht") | 14 rows (0.8%) | 4 messages | `SMALL_TALK` (the teacher too, once) |

Each training row teaches the intent of the chat's **last** customer message only (per-prefix rows are still an
open decision), so mid-chat changes like "make the fries large" are rarely trained. Dev intents on earlier messages
are about as accurate as on the last (88–91%), so untrained positions mostly work; the gap is in the rare labels.

## Other recurring mistakes

- **Late corrections ignored:** "please remove the muffin" (a-dev-019) keeps the muffin; "can the burger be a
  double" after confirming (a-dev-067) stays single; a payment change after confirmation (a-dev-064) is missed.
- **Time of day:** "10:30" said at 21:05 is 22:30 (a-dev-073, gold right); all three write 10:30 or 10:00.
- **Off-menu add-ons** ("with artichoke hearts", a-dev-034): mapped to a real modifier (artichoke, anchovies,
  "unknown") instead of marked off-menu.
- **Out-of-scope questions** ("who invented the cheeseburger?", "what's the capital of Australia?") →
  `MENU_QUESTION`.
- **Invalid answers are mostly the 2B's:** 13 (2B single) and 9 (2B mixed) vs 2 (0.8B), mainly two rule breaks: an
  item with no identity (no menu id, off-menu text or halves; 8) and an off-menu item carrying modifications (10).
  `finalize`/validation reject them, so the whole answer scores as nothing.

## What this suggests (decisions for Julian)

1. **Targeted training data** for the five thin patterns above: new synthetic cards that call for same-dish line
   splits, 4+ line orders, ambiguous quantity/size, `MODIFY_ORDER` after a confirmation, removals, and vague
   `UNKNOWN` messages. Written from these pattern descriptions, never from dev chats (Source A is evaluation only).
   Cost: generation + labeling ran ≈ $1.2–1.7 per ~500 chats in M4; spend is $5.80 of $10 (ask before spending).
2. **Per-prefix training rows** (the open M6 question): train the intent at every customer message, not just the
   last. Free (rows from the existing labels), multiplies `MODIFY_ORDER` and mid-chat examples, but makes training
   longer (more rows ≈ more Kaggle hours).
3. **Measure any fix on fresh data**, not on this dev set (CLAUDE.md): dev has now been read closely.
