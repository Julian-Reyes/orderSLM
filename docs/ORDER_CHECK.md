# Order checker (spec §11b)

## Pilot: the teacher checks the student's real mistakes (2026-11-03)

**Question.** Before building the full checker (planted mistakes, line-by-line version, the decision providers), can
an LLM spot the picked student's real order mistakes? Julian, 2026-11-03: "test on the ones missed only".

**Setup.**

- **Checker:** `openai/gpt-6-luna@low` (the teacher), standard API, price re-verified 2026-11-03 ($0.10 / $0.50 per
  1M input / output tokens, unchanged since 2026-10-16).
- **Prompt:** `order-check@0.1`, the whole-order check: one yes/no on the chat plus the order written out in plain
  text. The question is the label audit's order question (`label_audit.ORDER_PROMPT`), the same wording Jev and OpenAI
  Decisions answered in the label audit, so the checkers stay comparable. JSON reply `{matches, problem}`. Code
  `src/orderslm/eval/order_check.py`, `make order-check`.
- **Orders:** the picked student (`qwen3.5-0.8b-single-v2`), its final orders as saved in the student-dev runs and
  finalized in code. Every dev and fresh chat whose order is **not the same action as gold** (scorer@0.3): 42 real
  mistakes (dev 19, fresh 23). The 2 dev orders that are wrong only in wording (016, 038) are left out.
- **Run:** `runs/order-check/20261103T225157Z-openai__gpt-6-luna@low/` (manifest, every request and response,
  metrics, report). 42 calls, 0 errors, 0 unreadable answers. **Cost $0.0032** (estimate $0.0144).

**Limits.** Every order checked is wrong, so this measures the **catch rate only**. There is no false-alarm rate: a
checker that always says "no" would score 100% here. The checker is the teacher, and the student learned from the
teacher's labels, so they may share blind spots. 42 orders give wide intervals. Dev results may tune the checker;
fresh results only measure it.

### Results

| set | wrong orders caught |
|---|---|
| all | **32/42 (76%, 95% CI 61–87%)** |
| dev | 15/19 (79%, 57–91%) |
| fresh | 17/23 (74%, 54–87%) |
| the student's answer was valid | 28/38 (74%, 58–85%) |
| the student's answer was broken (shown as "no new order") | 4/4 |

31 of the 32 catches name a real problem in the order. One is caught for the wrong reason: in fresh 037 the real
mistake is "add black" on the Americano, but the checker objects to the hot chocolate's size. That size is the menu
default (Medium), and the checker can't see the menu. On a correct order, this would have been a false alarm.

**Caught well:** removals the student ignored ("drop the muffin", "no coke", "no shake": 4/4), items swapped or left
out ("1 on a croissant", Mountain Dew → Dr Pepper, a missing pizza), counting ("4 veggie burgers, 2 w jalapeños"),
a changed pickup time, "a few muffins" turned into 2 (2/2), and all 4 broken answers.

**The 10 misses:**

| why | chats |
|---|---|
| **Vague amount or size accepted** ("some" → 1, "big" → Large). It caught "a few", but not these | dev 045 ("some garlic knots"), fresh 056 ("some onion rings"), 009 ("the big margherita"), 063 ("the big pepperoni pizzas") |
| **Not shown to the checker** | dev 075 (pays with "2 hundreds": the change amount, $200 vs the student's $20, isn't in the order text), fresh 028 (an invented size on a water with no sizes; the text doesn't show it), fresh 049 (`red_bull` isn't on the menu: the text shows the raw id and the checker can't see the menu) |
| **Needs the menu** | dev 039 ("almond milk instead of whole milk" on an Americano, which has no milk) |
| **Debatable** | dev 073 ("at 10… make it 10:30" at a pizza place: gold reads 22:30, the record says 10:30 with no am/pm), fresh 087 ("oh right its the bac" → Bacon Burger; gold leaves it unclear) |

### What this means

- An LLM checker catches most of the mistakes that would hurt a customer: ignored removals, wrong or missing items,
  counting, broken answers.
- Its weak spot is the student's own weak spot: **vague amounts and sizes**. The order question never says that
  "some" or "big" must not become a number or a size.
- Some mistakes can't be caught from what the checker is shown: the cash change, and an item id that isn't on the
  menu. Without the menu, it can't tell a menu default from a guess (fresh 037).

### Found along the way

`core/finalize` let an item id that isn't on the menu through as a normal line (fresh 049 `red_bull`; dev 017 has a
pizza half `olives`). The order text used to crash on that unknown half id; it now shows the id as-is
(`label_audit._line_text`, no change to any earlier audit text). The finalize gap itself is not fixed yet.

### Next

Done in v0.2 below: the vague-amount rule, the cash change, ids that aren't on the menu, the menu, and the false-alarm
check. Still open: the full §11b checker (planted mistakes, the line-by-line version, Julia-1, the test-set score at
final eval).

## v0.2: the menu, three checkers, wrong and right orders (2026-11-03)

**Question.** With the menu and the pilot's fixes, how many wrong orders does each checker stop, and how many right
orders does it stop by mistake? Is a cheap yes/no service close to the LLM? Julian, 2026-11-03: "ok do it".

**What changed from the pilot (`order-check@0.2`):**

- **The menu**, without prices: every item's sizes or kinds (the default marked, or "no default: the customer
  chooses"), what it comes with, what can be added, combo choices, half-and-half, "sold by the order".
- **The order text in `detail` mode** (`label_audit.order_text(..., detail=True)`; the label audit's text is
  unchanged): the cash change ("paying with $20.00"), an id that isn't on the menu ("'red_bull' (NOT on the menu)"),
  a size the item doesn't have, and "size not stated" when no size was chosen.
- **Two rules added to the order question:** a menu default size counts as asked for, and a vague amount or size
  ("some", "a few", "big") must show as unclear, not as a number or a size.
- **Three checkers, the identical text:** Luna (the teacher LLM, JSON `{matches, problem}`), and the two decision
  services, Jev and OpenAI Decisions (one yes/no question, `order_ok`).
- **84 orders:** the same 42 wrong orders, plus 42 the student got right (same action as gold), a seeded random
  sample, as many per split as it got wrong (dev 19, fresh 23).

**Not held out.** The new rules came from the pilot's misses on dev **and fresh**, so the fresh numbers below were seen
while fixing. They show what the checker does on these chats, not how it does on new ones. A clean measure needs new
chats (a fresh2 batch or the test set at final eval).

**Run:** `runs/order-check/20261104T000454Z-0.2/` (manifest, every request and response, metrics, report). 252 calls,
0 errors. **Cost $0.0268** (estimate $0.0504): Luna $0.0122, OpenAI Decisions $0.0098, Jev $0.0048 (Jev's price is
still not verified on TypeSafe's own page).

### Results

Caught = a wrong order flagged. False alarm = a right order flagged. 95% CI in brackets.

| checker | wrong orders caught | false alarms on right orders | cost for 84 orders |
|---|---|---|---|
| **Luna** (LLM) | **33/42 (79%, 64–88%)** | 6/42 (14%, 7–28%) | $0.0122 |
| **Jev** (yes/no) | 28/42 (67%, 52–79%) | **2/42 (5%, 1–16%)** | $0.0048 |
| **OpenAI Decisions** (yes/no) | 25/42 (60%, 44–73%) | 4/42 (10%, 4–22%) | $0.0098 |

Pilot (no menu, wrong orders only): Luna caught 32/42. With the menu and the rules it catches 33/42, but not the
same ones:

- **Newly caught (6):** 3 of the 4 vague amounts or sizes (dev 045, fresh 009, 063; fresh 056 still missed), the change
  amount (dev 075), the invented water size (fresh 028), and fresh 037 now for the right reason ("black" recorded as
  an add-on), not the default hot-chocolate size.
- **Newly missed (4):** all are about how many of an item get an option: dev 020 (4 cheeseburgers all without pickles,
  asked 2 + 2), dev 063, fresh 007 (3 + 2 hot chocolates, asked 1 + 2), fresh 057. The longer input (the menu) may
  have cost attention on counting. One run each: Luna's answers vary a little from run to run.

Per split: Luna dev 15/19 caught, 4/19 false alarms; fresh 18/23 and 2/23. Jev dev 12/19 and 2/19; fresh 16/23 and
0/23. Decisions dev 11/19 and 2/19; fresh 14/23 and 2/23.

By what is wrong: all three catch every wrong size (8/8 Luna and Jev, 7/8 Decisions), ignored removals and broken
answers. Luna is clearly ahead on wrong quantities (5/8 vs Jev 3/8, Decisions 2/8) and wrong options (6/7 vs 4/7 and
5/7). Full tables: the run's `report.md`.

### The false alarms are not all false

| chat | flagged by | what the checker said | who is right |
|---|---|---|---|
| dev 023 | all three | the customer corrected the address to 104 River Rd, the record says 140 | **the checker**: the student kept the old address. Our scorer only checks that an address is given, not what it says, so it counted this order as right |
| dev 038 | all three | the drink is an off-menu line; it should be unclear | debatable: gold has the same line; this is one of the two wording-only differences |
| dev 034, fresh 005 | Luna; 005 also Decisions | "artichoke hearts" / "honey" aren't on the menu | the student: gold records them the same way, as kitchen requests. The order text shows them as bare words, so they look like menu options |
| dev 058 | Luna | asking about the delivery charge means delivery | the student: the customer never chose delivery |
| fresh 031 | Luna | 5 Supremes ordered, the record has 3 + 2 without olives | the student: 3 + 2 is 5, 2 without olives. A counting slip by Luna |
| fresh 090 | Decisions | (no reason given) | the student, by our gold |

So of Luna's 6 false alarms, one (dev 023) is a real mistake the scorer missed, and two come from how the order text
shows kitchen requests. Counting dev 023 as caught, Luna stops 34 of 43 wrong orders and raises 5 false alarms on 41
right ones.

### Still missed by all three

dev 020 and 063 (wrong quantity on a line with options, and a missing item), dev 039 (the record says "Almond milk instead of Whole milk" on an Americano, which
comes with no milk: the menu shows this, but no checker objected), dev 073
(10:30 vs 22:30, debatable), fresh 007 (quantity), fresh 049 (Red Bull: the record now says "NOT on the menu", but the
customer did ask for a Red Bull, so the checkers call it a match), fresh 087 ("the bac", debatable).

### What this means

- **Luna is the best checker**: it catches about 4 in 5 wrong orders, and stops about 1 in 8 right orders.
- **Jev is the cheapest and quietest**: it catches 2 in 3 wrong orders with the fewest false alarms (2/42), at 40% of
  Luna's cost. OpenAI Decisions is behind both on catches.
- **The intervals overlap.** With 42 orders each, Luna vs Jev on catches (79% vs 67%) is not a settled difference.
- **In the bot:** a flagged order goes to "please confirm" or to staff instead of the kitchen. The student gets 23 of 90
  fresh orders wrong. With Luna, about 18 of those would be stopped and about 9 of the 67 right ones would get an extra
  question.

### Found along the way

1. **Scorer gap: the address.** `eval/metrics.field_values` compares only whether an address was given, so a delivery
   to the wrong address scores as correct (dev 023). Not fixed: fixing it changes every order score, so it needs a
   decision and a re-score.
2. **Kitchen requests in the order text** show as bare words ("honey"), which reads like a menu option the item can't
   take. A v0.3 text should say "request not on the menu: honey".
3. The off-menu id gap in `core/finalize` (above) is still open.
