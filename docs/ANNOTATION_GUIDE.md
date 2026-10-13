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
  (they are just text; gold never uses them). Write them as the system would behave: no confirmation summary
  while anything is missing (ask the missing question first), replies within opening hours, nothing that
  contradicts the menu (e.g. accepting a payment channel the business doesn't take), and **no allergen or
  dietary claims** the menu can't back up (the menus have no allergen data: say it can't be confirmed here).
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
- A vague item the customer resolves later ("the usual", then "a cheeseburger and fries"): the vague line is
  dropped and the resolved items get new line ids. One never resolved stays `unmatched_text` +
  `item_menu_match / ambiguous`.
- Off-menu ("chicken sandwiches" at a burger place): `unmatched_text` as written, the stated quantity,
  and a `missing_or_ambiguous` entry `item_menu_match / off_menu`. Don't map it to the closest item.
- Informal names map to the menu when unambiguous (aliases: "shake" → `milkshake`, "large" → the large
  variant). If several items fit equally ("a burger" at a place with three burgers), don't pick one:
  write `unmatched_text: "a burger"` and add `item_menu_match / ambiguous`.
- `variant_id`: only if stated. If the item has a `default_variant_id`, an unstated size is fine (no
  missing entry). If it has variants and no default (milkshake flavor, pizza size), add `item_variant / missing`.
- A size or flavor the item doesn't have ("party size pizza", "medium fries" where fries are regular/large): the
  item **stays on the menu** (not `unmatched_text`), `variant_id: null`, the customer's words in
  `unmatched_variant_text`, and `item_variant / missing` (even if a default exists). The business asks which size;
  it doesn't reject the item.
- Quantity unclear ("some wings"): `quantity: null` + `item_quantity / ambiguous`.
- Items sold by the order (`sold_as: order`: garlic knots, breadsticks, fries, onion rings): quantity counts
  orders. "an order of knots" = 1, "two orders of knots" = 2. A piece count that divides evenly by
  `pieces_per_order` becomes orders ("12 garlic knots" = 2 at 6 per order); one that doesn't ("8 knots") is
  `quantity: null` + `item_quantity / ambiguous`.
- Modifications use the catalog `modifier_id` (an ingredient or add-on of that item):
  - "no onions", "hold the pickles" → `remove`.
  - "add bacon", "with mushrooms" → `add` (amount `normal`).
  - "extra cheese", "lots of", "heavy on" → `add` + `extra`; "light on the sauce", "just a little" → `add` + `light`.
    This applies whether or not the ingredient is already included.
  - "oat milk instead of whole", "mayo instead of ketchup" → `substitute`: `modifier_id` is the one removed,
    `replacement_modifier_id` the one added. "w oat milk" on a latte (no "instead") is also a substitute of the
    included milk.
  - Crust choices ("thin crust", "deep dish") are `add` of a crust modifier; only one crust per pizza.
  - A topping or add-on the menu doesn't offer ("artichoke hearts") → `modifier_id: null`, `not_on_menu: true`,
    and `item_modification / off_menu`. It is never priced or summarized until the customer resolves it.
  - Kitchen requests the business can simply do ("extra crispy", "warm", "cut in squares") → `modifier_id: null`,
    `kitchen_note: true`, nothing missing. They should be on the menu's `accepted_kitchen_requests`; one that isn't
    is treated as unverified by the rules (`item_modification / ambiguous`), so either add it to the menu or ask.
  - **Every request with no menu id is explicitly `not_on_menu` or `kitchen_note`**; the tool won't save one that
    is neither (`UNCLASSIFIED_REQUEST`).
- Combos: `combo_selections` per slot. Missing choice → `combo_choice / missing`.
- Half-and-half: `halves` with two `menu_item_id`s; the size goes on the line's `variant_id`. A half named by a
  recipe ("half hawaiian") is that pizza; a half named only by toppings ("half mushroom n olives") is
  `cheese_pizza` with those toppings added.

### Fulfillment, time, address, payment, name
- `method`: `pickup`/`delivery` only when the customer chooses it. "do you deliver to Oak St?" is a
  question, not a choice → `unknown`. An order sent "to <address>" ("lg pepperoni to 300 university dr") is a
  choice of delivery. At a pickup-only business an unstated method is still `unknown` and missing; the question is
  "Is this for pickup…?" and, where the business requires a name for pickup, the name is missing too.
- Changing pickup ↔ delivery keeps the requested time unless the customer changes it too.
- Time: `provided` with `kind` (`asap`, `clock_time`, `relative`) and `raw_text` as written. Fill
  `normalized_local` (HH:MM, business's timezone) only for clock times that are unambiguous given opening
  hours ("at 7" at a place open 11–22 → `19:00`). "around 7 or 8" → `ambiguous` + `requested_time / ambiguous`.
  Not mentioned → `not_mentioned`, and it is **not** missing (default is ASAP).
- Address: `not_applicable` for pickup. For delivery or unknown: `provided` with components you can read
  (`street`, `number`, `unit`, `reference` landmark) + `raw_text`; or `not_mentioned`. Delivery with no
  address → `address / missing`. An address stated in a question still counts as `provided`.
  Delivery instructions ("ring the side door") go in `notes`, not the address.
- Payment: `card`, `cash`, `other`, `unknown`. "change for a 50" → `change_for_cents: 5000`.
  "I already paid" → `customer_claims_paid: true` (a claim; staff verify it), method `unknown` unless the customer
  states one (a channel like "when I called" is not a method). Unknown payment → `payment_method / missing`.
  Cash with a bill smaller than the total ("pay w a 100" on a $170 order) can't be right: the code flags it
  (`CASH_BELOW_TOTAL`), so don't write it unless that is the point of the conversation.
  A claim during an order: `PLACE_ORDER` + secondary `PAYMENT_CLAIM` in the same message as the items, or primary
  `PAYMENT_CLAIM` in its own message; method stays `unknown` unless stated, and payment isn't asked again. The
  summary says "You mentioned you've already paid, and the restaurant will confirm it"; the ticket says "Payment:
  customer says paid, not verified".
- Customer name: only when the customer gives it. Optional, except for pickup orders at a business with
  `name_required_for_pickup: true` (menu setting): there a missing name is `customer_name / missing`.
- `customer_decision`: `confirmed` only when the customer agrees to a summary of the **current** order **and
  nothing is missing** (a confirmed order must be complete enough to send to the kitchen). A yes while something is
  still missing: `pending` + `agreed_while_incomplete: true`, citing the yes; the missing info is asked next.
  A change after confirming resets it to `pending` (the new order needs a new yes), and any change resets
  `agreed_while_incomplete` too.

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
- "yes" is `CONFIRM_ORDER` only right after the business asks to confirm the order. A "👍"/"sounds good" that
  answers a different question without answering it ("pickup or delivery?" → "👍 sounds good") is `UNKNOWN`.
- Adding a detail to an item just stated ("4 cheeseburgers" → "2 no pickles", "w hazelnut syrup") is
  `PLACE_ORDER`: nothing stated is replaced. `MODIFY_ORDER` is for replacing or removing something stated.
- One message that changes something and also gives a first detail ("make it a medium. pickup, card"):
  `MODIFY_ORDER` + secondary `PLACE_ORDER`.
- Frustration alone is not urgency. Urgency of changes: changes to a draft are `normal`; after confirming,
  a change to the food, time or address is `time_sensitive`, a payment switch `normal`. A pickup within ~15
  minutes of the message is `time_sensitive`. A charge for an order that never arrived, like a double charge, is a
  disputed payment: `needs_staff_now`.
- `refers_to: draft` for messages building the current order (including the first one);
  `placed_order` after the order was confirmed/sent; `none` for greetings or questions with no order.
- A menu question in the middle of an order is `refers_to: draft`; before any order, `none`. An `UNKNOWN`
  message with no order in the chat is `none`; a message about an order that isn't in this chat (and isn't
  clearly placed) is `unclear`.
- Any change after the customer confirmed, **including adding an item**, is `MODIFY_ORDER` about the
  `placed_order` (urgency as above).

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

_Last updated 2026-10-08 (M2 dev review: confirmed = complete, sizes/options not on the menu, changes after confirming)._
