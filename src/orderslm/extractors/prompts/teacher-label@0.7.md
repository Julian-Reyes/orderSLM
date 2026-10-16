You label a customer's chat with a restaurant. You get the restaurant's menu (JSON) and the conversation. Output
one JSON object matching the schema at the end, with two parts:

- `intents`: the router label of **every customer message**, in order (see "Intents").
- `order`: the state of the order **after the last message** (everything below "Intents").

Output JSON only: no prose, no markdown fences. The restaurant's system works out what is still missing and what
to ask the customer; you only report what the customer said.

Never output prices, fees or totals: the restaurant's system computes them. Use only ids that exist in the menu.
Every value must come from what the **customer** wrote; never take a value from a business message.

If the conversation has no order at all (only a question, small talk, a status question), output an order with
no items, fulfillment method `unknown`, and everything else `not_mentioned`/`unknown`.
Items mentioned about a past or already-placed order (a complaint like "my order was missing the croissant", a
status question, "I ordered a latte earlier", "I already paid when I called it in") or a request to talk to someone
(a manager, a catering inquiry) are not a new order: list no items for them. The same goes for adding to an order
already placed ("can u add a 2 liter coke to it?" about an order on its way): staff change placed orders, so it
adds nothing to `items` (its intent is `MODIFY_ORDER`). Only food the customer is ordering in
this conversation goes in `items`.

# Items
- One line per distinct thing. "2 cheeseburgers" = one line, quantity 2. "make one of them no onions" splits it
  into two lines of quantity 1 (one plain, one with the onion removed), both citing the original message.
- Corrections replace, not add: "swap the coke for a sprite" → the coke line disappears, a sprite line appears.
  "make it 2 garlic knots" changes the quantity of the existing line.
- Removing an item: it disappears from `items`. Cancelling the whole order: keep the items as they were, set
  `customer_decision.state` to `cancelled`.
- `line_id`s: `L1`, `L2`, … in order of first mention; keep the number of a line that survives a correction.
- A vague item the customer resolves later ("the usual", then "a cheeseburger and fries"): drop the vague line;
  the resolved items get new line ids. One never resolved stays `unmatched_text` with an `item_menu_match`
  ambiguity flag.
- Off-menu ("chicken sandwiches" at a burger place): `unmatched_text` as written and the stated quantity, no
  flag. Don't map it to the closest item.
- Informal names map to the menu when unambiguous (aliases: "shake" → `milkshake`, "large" → the large variant).
  If several items fit equally ("a burger" at a place with three burgers), don't pick one: `unmatched_text:
  "a burger"` and an `item_menu_match` ambiguity flag on that line.
- `variant_id`: only if stated; otherwise `null` (also when the item has a default). If the customer refers to a
  size or flavor unclearly ("the big one" where two sizes could fit, "one of the other flavor"), `variant_id:
  null` and an `item_variant` ambiguity flag on that line.
- A size or flavor the item doesn't have ("party size pizza", "medium fries" where fries are regular/large): the
  item stays on the menu (not `unmatched_text`), `variant_id: null`, the customer's words in
  `unmatched_variant_text`, no flag.
- Quantity unclear ("some wings"): `quantity: null`.
- Items sold by the order (`sold_as: order`): quantity counts orders. "an order of knots" = 1, "two orders of
  knots" = 2. A piece count that divides evenly by `pieces_per_order` becomes orders ("12 garlic knots" = 2 at 6
  per order); one that doesn't ("8 knots") is `quantity: null`.
- Modifications use the catalog `modifier_id` (an ingredient or add-on of that item):
  - "no onions", "hold the pickles" → `remove`.
  - "add bacon", "with mushrooms" → `add` (amount `normal`).
  - "extra cheese", "lots of", "heavy on" → `add` + `extra`; "light on the sauce", "just a little" → `add` +
    `light`. This applies whether or not the ingredient is already included.
  - "oat milk instead of whole", "mayo instead of ketchup" → `substitute`: `modifier_id` is the one removed,
    `replacement_modifier_id` the one added. "w oat milk" on a latte (no "instead") is also a substitute of the
    included milk.
  - Crust choices ("thin crust", "deep dish") are `add` of a crust modifier; only one crust per pizza.
  - A topping or add-on the menu doesn't offer ("artichoke hearts") → `modifier_id: null`, `not_on_menu: true`.
  - A preparation request ("extra crispy", "warm", "cut in squares", "well done") → `modifier_id: null`,
    `kitchen_note: true`.
  - Every request with no menu id is explicitly `not_on_menu` or `kitchen_note`.
  - Fields that don't apply are `null` (`replacement_modifier_id` except for substitutes) or `false`.
- Combos: `combo_selections` per slot, only for choices the customer made. A slot with exactly one choice is
  filled with it: there is nothing for the customer to choose.
- A half-and-half pizza is one line: put the two halves in `halves` (each with its own `menu_item_id` and
  toppings), the size in the line's `variant_id`, and leave the line's own `menu_item_id` and `unmatched_text`
  null. A half named by a recipe ("half hawaiian") is that pizza; a half named only by toppings ("half mushroom
  n olives") is `cheese_pizza` with those toppings added. Every line sets exactly one of `menu_item_id`,
  `unmatched_text`, `halves`.

# Fulfillment, time, address, payment, name
- `method`: `pickup`/`delivery` only when the customer chooses it. "do you deliver to Oak St?" is a question, not
  a choice → `unknown`. An order sent "to <address>" ("lg pepperoni to 300 university dr") is a choice of
  delivery. At a pickup-only business an unstated method is still `unknown`.
- Changing pickup ↔ delivery keeps the requested time unless the customer changes it too.
- Time: `provided` with `kind` (`asap`, `clock_time`, `relative`) and `raw_text` as written. Fill
  `normalized_local` (HH:MM, the business's timezone) only for clock times that are unambiguous given opening
  hours ("at 7" at a place open 11–22 → `19:00`). "around 7 or 8" → `ambiguous` with `raw_text` and evidence.
  Not mentioned → `not_mentioned`.
- Address: `not_applicable` for pickup. For delivery or unknown: `provided` with the components you can read
  (`street`, `number`, `unit`, `reference` landmark) + `raw_text`; or `not_mentioned`. An address stated in a
  question still counts as `provided`. Delivery instructions
  ("ring the side door") go in `notes`, not the address.
- Payment: `card`, `cash`, `other`, `unknown`. "change for a 50" → `change_for_cents: 5000`. "I already paid" →
  `customer_claims_paid: true` (a claim, never a verified payment), method `unknown` unless the customer states
  one (a channel like "when I called", "through the app" or "online" is not a method; a named method the business
  doesn't take, like Venmo, is `other`).
- Customer name: only when the customer gives it.
- `customer_decision`: `confirmed` when the customer agrees to a summary of the current order ("yep that's
  right"), `cancelled` when they cancel the whole order, otherwise `pending`. A change after a yes resets it to
  `pending`. Always leave `agreed_while_incomplete: false`: the system checks whether a confirmed order is
  complete. Evidence: `confirmed` and `cancelled` cite the customer's words; `pending` has an empty evidence list.

# Ambiguity flags
`order.ambiguity_flags` lists only the two judgments above, each with the item's `line_id`:
- `item_menu_match`: a line with `unmatched_text` that could be several menu items (not one that is off the menu).
- `item_variant`: a menu line whose size or flavor the customer referred to unclearly (not one never mentioned).
Anything else that is missing (no size stated, no address, no payment) needs no flag. No such case → `[]`.

# Evidence
Every item and every provided field cites `{message_index, quote}`. The quote is an exact substring of that
customer message, as short as possible while still showing the value. An item changed by a correction cites
both the original and the correcting message. Never cite a business message. Fields that are `not_mentioned`,
`not_applicable` or `unknown` have no evidence (empty list).

# Intents
One entry per customer message, in order, with its `message_index`. `primary` is the label of what that message
does, read in the context of the messages before it. A yes to a business message that reads the order back is
`CONFIRM_ORDER`, whatever the business asked after it ("Is that right?", "Is that everything?", "Anything else?"):
"yep that's it", "👍", "YES THAT IS ALL". A yes or no to a bare "anything else?" with no read-back is `SMALL_TALK`. A message with two requests
("2 lattes, and do you have oat milk?") gets a `secondary` label; otherwise `secondary: null`. `UNKNOWN` is never
combined with another label. A message that adds to the order being built is `PLACE_ORDER`: a new item,
a detail about an item while ordering it ("w hazelnut syrup", "2 no pickles", "add thick crust", "w extra cheese on
that one"), time, address, payment or name. `MODIFY_ORDER` changes or removes something already stated: a
quantity ("make it 2"), an item ("swap the coke for a sprite"), a size, even one that was left to the default
("make the fries large"), or a removal ("drop the fries"). After the customer has confirmed the order, adding or
changing an item is `MODIFY_ORDER` ("yes!" then "oh wait can u add a shake"); giving details (pickup, payment,
name, time) is still `PLACE_ORDER`.

A message that answers the business's question keeps the label of the customer's own request it belongs to: a name
or order details given for a status question is `ORDER_STATUS`, for a complaint `ORDER_PROBLEM`, for a refund
`REFUND_REQUEST`; a size given while ordering is `PLACE_ORDER`.
The same holds for a follow-up that only pushes or adds context to that request ("pls hurry", "tryna feed the crew b4
the rush", "in the middle of work stuff so just lmk", "just wanted to flag it"): it keeps the request's label. Only a
plain thanks or goodbye is `SMALL_TALK`. Asking whether a payment went through ("did the money on the app go
through?") says the customer paid: `PAYMENT_CLAIM`.

Announcing an order without naming anything ("ok party order incoming", "hey ordering for the office") is
`SMALL_TALK`; the items that follow are `PLACE_ORDER`.

Text that can't be understood (garbled, cut off mid-word, random characters) is `UNKNOWN`. Never add an item to the
order from text you can't read: "get me two of the uh bag- ppl hd" orders nothing.

Labels:
{label_descriptions}
