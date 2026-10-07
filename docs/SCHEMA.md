# Schema

Code is the source of truth: `src/orderslm/schema/`. This page explains the design. Versions live in
`schema/common.py` and are logged with every run.

| Contract | Version | File |
|---|---|---|
| Extraction output (model proposal) | `extraction@0.2` | `schema/extraction.py` |
| Router decision | `router@0.1` | `schema/routing.py` |
| Router taxonomy (labels + descriptions) | `taxonomy@0.1` | `schema/routing.py`, docs/TAXONOMY.md |
| Conversation | `conversation@0.1` | `schema/conversation.py` |
| Menu catalog | `menu@0.3` | `schema/menu.py` |
| Verified results (quote, order, tool results) | — (internal) | `schema/order.py` |
| Annotated conversation (samples, dev, test) | — | `schema/annotation.py` |

## Principles

1. **Proposals vs. verified results.** A model's output (`ExtractionOutput`) is a proposal: ids, quantities,
   quotes. Prices, totals, order status and payment confirmation exist only in verified types
   (`Quote`, `OrderRecord`, `ToolOk`), produced by code or tools and stamped with `verified_by`.
2. **No prices from models.** `ExtractionOutput` has no price/total/fee field, and every contract uses
   `extra="forbid"`, so a model that adds `"total_cents": ...` fails validation. A test scans the JSON
   schema for price-like field names.
3. **Integer cents, strict.** `Cents` rejects floats and strings. `Quote` refuses to exist unless
   `line_total = unit × qty`, `subtotal = Σ lines`, `total = subtotal + fee`, and the fee is 0 unless delivering.
4. **Language-neutral.** Every enum value is a code (`pickup`, `no_onion`, `PLACE_ORDER`). Only message
   text, evidence quotes, `raw_text`, notes and `clarification_question` are in the conversation's
   `language` (BCP-47, `en` for V1). Adding Portuguese needs new data and reply templates, not schema changes.
5. **Unknown ≠ absent ≠ not applicable.** Slots carry an explicit `SlotState`.
6. **Evidence for everything stated.** Each item and each provided field cites `{message_index, quote}`;
   `orderslm.checks` verifies the quote is in that message (case/whitespace-insensitive) and every id is in the menu.

## Extraction output (`extraction@0.2`)

0.2 (M1) added `Modification.amount` (`normal | extra | light`), needed for "extra cheese" / "light on the
sauce" and for the PIZZA dataset's EXTRA/LIGHT qualifiers.

**Input** (`ExtractionRequest`): menu catalog + conversation (customer and business messages, timestamped)
+ current draft (`ExtractionOutput | null`) + prompt version.

**Output: a full snapshot**, not a diff. The model states what the order *is* now, after all corrections.
The patch shown to the business ("changed: coke → sprite") is computed in code by comparing the snapshot
with the previous draft. Rationale: snapshots are easier for small models (no patch algebra), gradable by
exact match, and can't be "applied wrong". (Spec §3 calls the extractor's output an "order patch";
see PROGRESS.md open question 1.)

```jsonc
{
  "schema_version": "extraction@0.2",
  "items": [{
    "line_id": "L2",                      // stable within the conversation
    "menu_item_id": "cheeseburger",       // exactly one of menu_item_id | unmatched_text | halves
    "unmatched_text": null,               // off-menu, as written ("chicken sandwiches")
    "halves": null,                       // half-and-half: two {menu_item_id, modifications}
    "quantity": 1,                        // 1-99, or null if stated but unclear ("some wings")
    "variant_id": null,                   // null = not stated (catalog default applies if any)
    "modifications": [{"kind": "remove", "modifier_id": "onion", "amount": "normal", "raw_text": "no onions"}],
    "combo_selections": [],               // [{slot_id, menu_item_id, variant_id?}]
    "notes": null,
    "evidence": [{"message_index": 0, "quote": "2 cheeseburgers"},
                 {"message_index": 1, "quote": "make one of them no onions"}]
  }],
  "fulfillment": {
    "method": "pickup",                   // delivery | pickup | unknown
    "method_evidence": [{"message_index": 3, "quote": "pickup at 7"}],
    "requested_time": {"state": "provided", "kind": "clock_time", "raw_text": "at 7",
                       "normalized_local": "19:00", "evidence": [...]}
  },
  "address": {"state": "not_applicable"}, // street, number, unit, reference, raw_text when provided
  "payment": {"method": "cash", "change_for_cents": null, "customer_claims_paid": false, "evidence": [...]},
  "customer_name": {"state": "not_mentioned"},
  "customer_decision": {"state": "pending"},   // pending | confirmed | cancelled (+ evidence)
  "notes": [],                             // [{text, evidence}] e.g. "ring the side door"
  "missing_or_ambiguous": [],              // [{field, reason, line_id?}]
  "clarification_question": null           // required iff missing_or_ambiguous is non-empty
}
```

### Slot states

| `SlotState` | Meaning | Value | Evidence |
|---|---|---|---|
| `provided` | Stated clearly | required | required |
| `ambiguous` | Mentioned but unclear ("around 7 or 8") | none (`raw_text` kept for time) | required |
| `not_mentioned` | Nothing said yet | none | none |
| `not_applicable` | Doesn't apply (address for pickup) | none | none |

`fulfillment.method` and `payment.method` use `unknown` instead of a slot state (spec wording); evidence is
required for every non-`unknown` value.

### Validation rules (enforced in code, tested)

- Item identity: exactly one of `menu_item_id`, `unmatched_text`, `halves`; off-menu items can't have
  variants/modifications and must appear in `missing_or_ambiguous` as `item_menu_match`.
- `line_id`s unique; item-level missing entries must reference an existing line.
- `clarification_question` present **iff** `missing_or_ambiguous` is non-empty; a cancelled order has nothing to clarify.
- Pickup ⇒ address `not_applicable`; delivery/unknown ⇒ address is not `not_applicable`.
- `normalized_local` is strict `HH:MM`, only for `provided` + `clock_time`.
- `change_for_cents` only for cash. `customer_claims_paid` records a claim; there is no "paid" field in model output.
- `replacement_modifier_id` only for `substitute` modifications; `amount` other than `normal` only for `add`.
- Modification meaning: `remove` an ingredient ("no onions"); `add` an add-on ("add bacon") or, with `extra`/`light`,
  change the amount of any ingredient ("extra cheese", "light sauce"); `substitute` swaps one modifier for another
  ("oat milk instead of whole"). Pricing of each case: docs/PRICING.md.

### Checks beyond the schema (`orderslm.checks`)

`check_evidence`: every quote occurs in the cited message. `check_catalog`: items, variants, modifiers
(allowed on that item; at most one per exclusive group, e.g. one crust), combo slots/choices and splittable
halves exist in the menu. Used on gold
annotations (tests), teacher labels (drop + log the drop rate, M4), and model outputs (hallucination rate, M6).

### `missing_or_ambiguous` fields

`items`, `item_menu_match`, `item_quantity`, `item_variant`, `item_modification`, `combo_choice` (these
five take a `line_id`), `fulfillment_method`, `requested_time`, `address`, `payment_method`, `customer_name`.
Reasons: `missing`, `ambiguous`, `off_menu`, `conflicting`. What counts as required is in docs/ANNOTATION_GUIDE.md.

## Router decision (`router@0.1`)

`{primary, secondary?, urgency, flags: {refers_to, asks_for_human}}`; see docs/TAXONOMY.md. Rules:
secondary ≠ primary; `UNKNOWN` never combines; any `HUMAN_REQUEST` label implies `asks_for_human`.
The same shape is used for gold annotations and for normalized provider output.

## Decision providers (`interfaces/decision.py`)

OrderSLM's own provider-neutral abstraction, *not* any provider's wire format:
`DecisionRequest {request_id, input, questions[{name, type: choice|score|boolean, prompt, options[{id, description}]}], prompt_version}`
→ `DecisionResponse {provider, model, answers{name: {choice|score|boolean, confidence?, probabilities?, refused}}, usage, latency_ms, cost_micros, cached}`.
`check_against_limits` rejects requests over a provider's option limit before sending;
`validate_response` rejects missing answers, wrong types and choices that weren't offered.
Adapters (M7) map this to each provider's documented API after verifying it.

## Verified results (`schema/order.py`)

`QuoteLine`, `Quote` (arithmetic-checked), `OrderRecord` (`status`, `payment_confirmed` set only by
staff/payment systems), `HandoffTicket`, and `ToolOk[T] | ToolErr` (`error.code` is `UPPER_SNAKE`).
Order statuses: `draft → awaiting_confirmation → new → preparing → ready → completed`, or `cancelled`.
Allowed transitions: `core/state.py` (customer changes to a placed order go to staff).

## Menu catalog (`menu@0.3`)

Business id, currency, timezone, hours, delivery policy (`available`, `fee_cents`, `min_order_cents`),
`name_required_for_pickup` (0.2), `exclusive_groups` (0.3), modifiers, and items.
- **Modifiers** (0.3) are ingredients/add-ons with a `group` (topping, sauce, crust, milk…), `aliases` and a
  `price_cents` for adding one portion. They no longer have an add/remove kind.
- **Items**: aliases, base price, variants (price delta, aliases, optional default), `ingredient_ids`
  (included: removable, adjustable), `addon_ids` (may be added), `splittable`, combo slots, `available`.
- `held_out: true` marks the test-only menu, which lives in `data/menus/held_out/` and is loaded only with
  `load_menus(include_held_out=True)`.
References are validated (unknown modifier ids, combo choices, unused exclusive groups fail). The menus
themselves: docs/MENUS.md.

## Annotated conversation

`{conversation, scenarios[], style, gold_extraction | null, gold_routing[], annotator, annotation_notes}`.
Gold extraction is the order state after the last message (null if the conversation has no order);
gold routing covers every customer message, in order. Format for samples, dev and test sets.

## Changing a contract

Bump the version in `schema/common.py`, update this file and the samples, and note it in PROGRESS.md.
Runs record the versions they used, so old results stay interpretable.
