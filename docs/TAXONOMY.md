# Router taxonomy V1 (`taxonomy@0.1`)

One decision per **customer message**, made with the conversation context (up to 6 earlier messages, and
whether a draft or placed order exists). Source of truth: `src/orderslm/schema/routing.py`. The
descriptions below are sent **verbatim** to every provider and shown in the annotation tool;
`tests/test_docs_sync.py` fails if this table and the code drift apart.

15 labels: fits every provider in one call (Julia-1 allows 2–20 options per question, ≤ 48 tokens per
option; to be re-verified against Julia-1's docs and tokenizer in M7). Descriptions are ≤ 20 words.

## Primary labels

| Label | Description (sent to providers) | Example |
|---|---|---|
| `PLACE_ORDER` | Customer starts an order, adds items, or gives first details like time, address or payment. | "2 cheeseburgers and fries" · "pickup at 7, paying cash" |
| `MODIFY_ORDER` | Customer changes something already stated: items, sizes, extras, time, address or payment. | "swap the coke for a sprite" |
| `CANCEL_ORDER` | Customer cancels the whole order. | "nvm cancel it" |
| `CONFIRM_ORDER` | Customer agrees the order summary is correct. | "yep that's right" |
| `MENU_QUESTION` | Question about menu items, ingredients, sizes, prices or availability. | "do you have veggie burgers?" |
| `DELIVERY_QUESTION` | Question about delivery area, fee, pickup, or opening hours. | "do you deliver to Oak St? how much?" |
| `PAYMENT_QUESTION` | Question about how to pay or which payment methods work. | "can I pay cash?" |
| `PAYMENT_CLAIM` | Customer says they already paid or sent payment. | "I already paid" |
| `ORDER_STATUS` | Customer asks where a placed order is or when it will arrive. | "where's my food??" |
| `ORDER_PROBLEM` | Complaint about a received order: missing, wrong, late, cold or damaged. | "the bacon was missing" |
| `REFUND_REQUEST` | Customer asks for their money back or a refund. | "I want my money back" |
| `HUMAN_REQUEST` | Customer asks to talk to a person or staff member. | "let me talk to a person" |
| `SMALL_TALK` | Greeting, thanks, or chit-chat with no request. | "hi", "thanks!" |
| `OUT_OF_SCOPE` | Request unrelated to ordering food from this business. | "are you hiring?" |
| `UNKNOWN` | Too unclear to tell what the customer wants. | "??", "the thing" with no context |

`PLACE_ORDER`, `MODIFY_ORDER`, `CANCEL_ORDER`, `CONFIRM_ORDER` (as primary **or** secondary) send the
message to the extractor.

## Boundary rules

| Situation | Label | Why |
|---|---|---|
| First time giving time/address/payment for a draft | `PLACE_ORDER` | Still building the order. |
| Changing time/address/payment already given | `MODIFY_ORDER` | Something stated is replaced. |
| Removing one item ("no coke after all") | `MODIFY_ORDER` | `CANCEL_ORDER` is the whole order only. |
| Any change after the customer confirmed, including adding an item | `MODIFY_ORDER` | It changes a placed order. |
| "yes" / "yep" right after the business asks to confirm the order | `CONFIRM_ORDER` | Context-dependent yes. |
| "yes" answering a different question ("want fries with that?" → "yes") | `PLACE_ORDER` | It adds an item. |
| "where's my food, it's been an hour" | `ORDER_STATUS` | Asks where the order is. |
| "it came 40 min late and cold" | `ORDER_PROBLEM` | Complaint about a received order. |
| "the bacon was missing, I want a refund" | `ORDER_PROBLEM` + secondary `REFUND_REQUEST` | Two requests. |
| "how much is a large pizza?" | `MENU_QUESTION` | Item prices are menu questions; delivery fees are `DELIVERY_QUESTION`. |
| "thanks! also add a coke" | `PLACE_ORDER` (not `SMALL_TALK`) | Small talk never wins over a request. |
| Insults with no request | `UNKNOWN` | Don't guess intent from tone. |

## Secondary label (optional)

Set only when one message makes **two different requests** ("2 burgers, also do you deliver to Oak St?"
→ `PLACE_ORDER` + `DELIVERY_QUESTION`). Never the same as primary, never `UNKNOWN`, never `SMALL_TALK`
added to a real request. Primary is the request that needs action first; if equal, the earlier one in the message.
Providers get a 15-option secondary question: `NONE` + the 14 non-`UNKNOWN` labels.

## Urgency

| Value | Description (sent to providers) | Rubric |
|---|---|---|
| `normal` | No time pressure beyond a normal order. | Default, including ordinary orders "asap". |
| `time_sensitive` | A deadline or delay matters now: late order, pickup soon, time change. | Order overdue, pickup within ~15 min, a change to an order already being prepared. |
| `needs_staff_now` | Safety, allergy reaction, payment dispute, or wrong delivery needing staff now. | Allergic reaction, food safety, charged twice / disputed payment, order delivered to the wrong place. |

**Frustration alone is not urgency.** ALL CAPS, "!!!" and insults don't raise urgency; the situation does.

## Context flags

| Flag | Values | Description (sent to providers) |
|---|---|---|
| `refers_to` | `draft` | The order still being put together in this chat. |
| | `placed_order` | An order already placed or confirmed. |
| | `none` | No specific order. |
| | `unclear` | Can't tell which order. |
| `asks_for_human` | boolean | "Does the customer ask to talk to a person?" Must be true whenever `HUMAN_REQUEST` is primary or secondary. |

## Changing the taxonomy

Labels, descriptions and rubric changes bump `TAXONOMY_VERSION`. Router results are only comparable
within one taxonomy version. Keep the count ≤ 20 while Julia-1 is in the benchmark.
