# Annotation guide (V1, English)

For writing, labeling and reviewing the dev and test sets (M2): Source A (Claude-written from scenario cards,
reviewed by Julian) and Source C (optional, Julian-written); see docs/SPLITS.md. Format: `AnnotatedConversation`
(docs/SCHEMA.md); worked examples: `data/samples/conversations/`. Labels must pass `make test`-style
validation and the grounding checks before a conversation is accepted.

## 1. Writing conversations

- Write against one menu (`data/menus/`, M1). Never use real customer chats or real people's names/addresses.
- Write like real texting: abbreviations (u, ur, pls, thx, lemme, gimme, nvm, rn, idk), typos, no punctuation,
  ALL CAPS, emojis, several short messages in a row, number words ("a couple", "another one"), sizes
  ("large", "12 inch", "half pepperoni half hawaiian"), vague references ("one of them", "same as before").
- Include tricky cases on purpose: two requests in one message, corrections (also after confirmation),
  off-menu items, missing info, context-dependent "yes", chit-chat or a complaint mid-order.
- Business messages are optional. When you write one, prices in it must be the real menu prices
  (they are just text; gold never uses them).
- Tag every conversation with its `scenarios` and one `style` (`clean`, `texting`, `rapid_fire`, `shouty`, `emoji`).
- Test conversations: write them, label them, and don't look at them again. They are sealed after M2.

## 2. Gold extraction: the order after the last message

Label the state of the order **after the last message**, not the first version. If the conversation has
no order at all (only a status question, small talk), `gold_extraction` is `null`.

### Items
- One line per distinct thing. "2 cheeseburgers" = one line, quantity 2. "make one of them no onions"
  splits it into two lines of quantity 1 (one plain, one `no_onion`), both citing the original message.
- Corrections replace, not add: "swap the coke for a sprite" → the coke line disappears, a sprite line
  appears. "make it 2 garlic knots" changes the quantity of the existing line.
- Removing an item: it disappears from `items`. Cancelling the whole order: keep the items as they were,
  set `customer_decision` to `cancelled`, leave `missing_or_ambiguous` empty.
- `line_id`s: `L1`, `L2`, … in order of first mention; keep the number of a line that survives a correction.
- Off-menu ("chicken sandwiches" at a burger place): `unmatched_text` as written, the stated quantity,
  and a `missing_or_ambiguous` entry `item_menu_match / off_menu`. Don't map it to the closest item.
- Informal names map to the menu when unambiguous (aliases: "shake" → `milkshake`, "large" → the large
  variant). If several items fit equally ("a burger" at a place with three burgers), don't pick one:
  write `unmatched_text: "a burger"` and add `item_menu_match / ambiguous`.
- `variant_id`: only if stated. If the item has a `default_variant_id`, an unstated size is fine (no
  missing entry). If it has variants and no default (milkshake flavor, pizza size), add `item_variant / missing`.
- Quantity unclear ("some wings"): `quantity: null` + `item_quantity / ambiguous`.
- Modifications use the catalog `modifier_id` (an ingredient or add-on of that item):
  - "no onions", "hold the pickles" → `remove`.
  - "add bacon", "with mushrooms" → `add` (amount `normal`).
  - "extra cheese", "lots of", "heavy on" → `add` + `extra`; "light on the sauce", "just a little" → `add` + `light`.
    This applies whether or not the ingredient is already included.
  - "oat milk instead of whole", "mayo instead of ketchup" → `substitute`: `modifier_id` is the one removed,
    `replacement_modifier_id` the one added. "w oat milk" on a latte (no "instead") is also a substitute of the
    included milk.
  - Crust choices ("thin crust", "deep dish") are `add` of a crust modifier; only one crust per pizza.
  - Requests not in the catalog ("extra crispy") → `modifier_id: null` with `raw_text`; add
    `item_modification / off_menu` only if the business would need to answer it.
- Combos: `combo_selections` per slot. Missing choice → `combo_choice / missing`.
- Half-and-half: `halves` with two `menu_item_id`s; the size goes on the line's `variant_id`.

### Fulfillment, time, address, payment, name
- `method`: `pickup`/`delivery` only when the customer chooses it. "do you deliver to Oak St?" is a
  question, not a choice → `unknown`.
- Time: `provided` with `kind` (`asap`, `clock_time`, `relative`) and `raw_text` as written. Fill
  `normalized_local` (HH:MM, business's timezone) only for clock times that are unambiguous given opening
  hours ("at 7" at a place open 11–22 → `19:00`). "around 7 or 8" → `ambiguous` + `requested_time / ambiguous`.
  Not mentioned → `not_mentioned`, and it is **not** missing (default is ASAP).
- Address: `not_applicable` for pickup. For delivery or unknown: `provided` with components you can read
  (`street`, `number`, `unit`, `reference` landmark) + `raw_text`; or `not_mentioned`. Delivery with no
  address → `address / missing`. An address stated in a question still counts as `provided`.
  Delivery instructions ("ring the side door") go in `notes`, not the address.
- Payment: `card`, `cash`, `other`, `unknown`. "change for a 50" → `change_for_cents: 5000`.
  "I already paid" → `customer_claims_paid: true` (a claim; staff verify it). Unknown payment → `payment_method / missing`.
- Customer name: only when the customer gives it. Optional, except for pickup orders at a business with
  `name_required_for_pickup: true` (menu setting): there a missing name is `customer_name / missing`.
- `customer_decision`: `confirmed` only when the customer agrees to a summary of the **current** order.
  A change after confirming resets it to `pending` (the new order needs a new yes).

### What counts as missing (V1)
Missing (add to `missing_or_ambiguous`): no items; off-menu or ambiguous item; quantity unclear; required
variant or combo choice not stated; fulfillment method unknown; delivery without address; payment unknown;
an ambiguous time; no name on a pickup order when the business requires one. Not missing: name otherwise,
time when not mentioned, size when a default exists.

### Clarification question
One natural question covering **everything** in `missing_or_ambiguous`, in the conversation's language,
friendly and short. Offer the options when there are few ("vanilla, chocolate or strawberry"). Never state
prices or totals in it. Empty list ⇒ no question.

### Evidence
Every item and every provided field cites `{message_index, quote}`. The quote is an exact substring of
that **customer** message (case and spacing are ignored by the checker), as short as possible while still
showing the value. An item changed by a correction cites both the original and the correcting message.
Never cite a business message: gold must come from what the customer said.

## 3. Gold routing: every customer message

Label each customer message in order, using the context before it (not after). Use docs/TAXONOMY.md:
primary label, optional secondary, urgency, `refers_to`, `asks_for_human`. Key rules:
- Small talk never wins over a real request.
- "yes" is `CONFIRM_ORDER` only right after the business asks to confirm the order.
- Frustration alone is not urgency.
- `refers_to: draft` for messages building the current order (including the first one);
  `placed_order` after the order was confirmed/sent; `none` for greetings or questions with no order.

## 4. Quality process

1. Label with the annotation tool (`make annotate`, docs/SPLITS.md); it validates the schema, runs the grounding
   checks and compares missing info with the rules on every edit, and won't save until they pass.
2. Write `annotation_notes` for every judgment call; recurring ones become rules in this guide (bump the
   date below and note the change in PROGRESS.md).
3. **Review (Source A):** Julian reviews all of dev and at least 25% of test with "Save as reviewed"; every review
   is logged and the correction rate is reported. **Self-consistency** (a blind relabel a week later) is optional
   and only for Source C.
4. Disagreements found later: fix the gold, log the change (conversation id, field, old → new, reason).
   Don't change test gold after any model has been scored on it without recording why.

_Last updated 2026-10-07 (M0)._
