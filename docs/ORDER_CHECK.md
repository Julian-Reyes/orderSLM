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

### Next (not done)

1. **Checker v0.2, tuned on dev only:**
   - say that vague amounts and sizes must not become numbers;
   - show the cash change;
   - flag ids that aren't on the menu;
   - give the menu (or at least its defaults).
2. **Measure false alarms:** run the same check on orders the student got right. A matched set (42 right orders)
   costs about $0.003.
3. **The full §11b checker:** planted mistakes, the line-by-line version, Julia-1 / Jev / OpenAI Decisions next to the
   teacher, and the test-set score at final eval.
