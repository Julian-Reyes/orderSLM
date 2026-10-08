# Pricing (`pricing@0.1`)

Implemented in `src/orderslm/core/pricing.py` (`DeterministicPricing`, the `PricingEngine`). Input: a menu
and a model's `ExtractionOutput` proposal. Output: a verified `Quote` (integer cents, arithmetic-checked by
the schema), or a `ToolErr` listing **every** reason the order can't be priced yet. The engine never
guesses: no default for a required size, no closest match for an off-menu item.

## Line price

`unit price = base price + variant delta + modifier prices + combo upsizing`, and
`line total = unit price × quantity`.

| Case | Price |
|---|---|
| Variant stated | its `price_delta_cents` (may be negative) |
| Variant not stated, item has a default | the default's delta |
| Variant not stated, no default | **error** `MISSING_VARIANT` |
| A size the item doesn't have (`unmatched_variant_text`) | **error** `MISSING_VARIANT`, even if a default exists |
| An option the menu doesn't offer (`not_on_menu`) | **error** `OPTION_NOT_ON_MENU`: the line is never priced |
| A request with no menu id that isn't an accepted kitchen request and isn't `not_on_menu` (unverified) | **error** `REQUEST_UNVERIFIED` until the customer answers |
| `remove` a modifier | free |
| `add` an add-on (not included) | `price_cents` |
| `add` + `extra`, not included | 2 × `price_cents` (a double portion) |
| `add` + `extra`, already included | `price_cents` (one more portion) |
| `add` / `add` + `light`, already included | free |
| `add` + `light`, not included | `price_cents` |
| `substitute` A → B | as adding B (free if B is included); removing A is free |
| Accepted kitchen request (on the menu's `accepted_kitchen_requests`: "well done", "warm") | free (a kitchen note) |
| Combo | combo base price; slot choices included; a chosen size adds that size's delta |
| Half-and-half | the dearer half's base + size delta, plus each half's modifier prices at **half, rounded up** to the cent |

## Order total

`subtotal = Σ line totals`; `total = subtotal + delivery fee`. The fee applies only when fulfillment is
`delivery`; with `unknown` fulfillment the quote has no fee (the reply never presents it as final).

## Errors (`ToolErr`, never an exception)

`error.code` is the first problem; `error.details.issues` lists all of them with their `line_id`.

| Code | When |
|---|---|
| `NO_ITEMS` | nothing ordered yet |
| `UNMATCHED_ITEM` | off-menu / ambiguous item (`unmatched_text`) |
| `UNCLEAR_QUANTITY` | `quantity: null` |
| `MISSING_VARIANT` | required size/flavor not stated (also inside a combo choice) |
| `MISSING_COMBO_CHOICE` | a combo slot not chosen |
| `OPTION_NOT_ON_MENU` | a requested topping/add-on the menu doesn't offer (`not_on_menu`), until the customer resolves it |
| `CASH_BELOW_TOTAL` | cash with `change_for_cents` smaller than the total ("pay w a 100" on a $170 order); `details` has both amounts; the reply asks for a larger bill or card |
| `REQUEST_UNVERIFIED` | a request with no menu id the menu doesn't list as an accepted kitchen request (core/requests.py) |
| `UNKNOWN_ITEM`, `UNKNOWN_VARIANT`, `UNKNOWN_MODIFIER`, `UNKNOWN_COMBO_SLOT`, `INVALID_COMBO_CHOICE`, `NOT_SPLITTABLE`, `MODIFIER_NOT_ALLOWED` | ids that don't exist or don't apply (from `checks.check_catalog`) |
| `EXCLUSIVE_GROUP_CONFLICT` | two choices from one exclusive group (two crusts) |
| `UNAVAILABLE` | item marked `available: false` |
| `DELIVERY_UNAVAILABLE` | delivery requested from a pickup-only business |
| `BELOW_DELIVERY_MINIMUM` | delivery subtotal under `min_order_cents` (`details` has both amounts) |

## Where the numbers go

Every `Quote` records `verified_by: pricing@0.1` and `menu_version` (a content hash of the menu, e.g.
`corner-patty@066e89f75d8e`). The reply layer (`core/replies.py`) takes amounts only from the Quote; a
model's clarification question is discarded in favor of a template if it states any amount.
Changing any rule above bumps `PRICING_VERSION`.
