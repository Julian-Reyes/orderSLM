# Audit of `audit.md` (30 chats)

Reviewed by Claude at Julian's request (2026-10-16). This stands in for the hand audit in spec §7 and is **not** a
human review. The sample is half card-flagged chats by design (15 of 30), so "card followed" understates the batch
rate (89–93% card agreement overall, report.md).

✓ = right, ✗ = wrong, ~ = debatable.

| Chat | Writer | Realistic | Card followed | Intents | Order | Note |
|---|---|---|---|---|---|---|
| 0003 | DeepSeek | ✓ | ✗ | ✗ | ✓ | Never says they paid (an order-status chat). "sam" answering "what name was the order under?" was labeled UNKNOWN; it serves the status request: ORDER_STATUS |
| 0004 | DeepSeek | ✓ | ✓ | ✓ | ✓ | |
| 0072 | Haiku | ✓ | ✓ | ✓ | ✓ | |
| 0085 | Gemini | ✓ | ✓ | ✓ | ✓ | "do u guys have diet coke" is a question; the diet coke enters the order through the confirmed read-back. Fine |
| 0113 | Haiku | ✓ | ✓ | ✓ | ✓ | |
| 0115 | DeepSeek | ✓ | ✗ | ✓ | ✓ | The business invents "2"; the label correctly keeps the customer's 1 |
| 0123 | DeepSeek | ✓ | ✗ | ~ | ✓ | Nuggets only asked about. "yea thats it" after a read-back + "is that everything?": SMALL_TALK or CONFIRM_ORDER |
| 0144 | Haiku | ✓ | ✓ | ✓ | ✓ | "the regular one" leaked from the card (fixed in cards 0.4); can = the default, fine |
| 0160 | Haiku | ✗ | ✗ | ✓ | ~ | Card bug (onion rings swapped for onion rings, fixed): the chat contradicts itself. Drop |
| 0194 | Haiku | ✓ | ✓ | ✓ | ✓ | "iced tea (regular)" from the leaked card wording → size missing, correct by the rules |
| 0205 | Haiku | ✓ | ✗ | ✓ | ✓ | Changes before confirming |
| 0248 | DeepSeek | ✓ | ✓ | ✓ | ✓ | |
| 0256 | Gemini | ✓ | ✓ | ✓ | ✓ | |
| 0280 | Gemini | ✓ | ✗ | ~ | ✓ | New order inside a refund chat. Secondary SMALL_TALK for "THANKS!" on an order message is over-labeling |
| 0283 | Gemini | ✓ | ✗ | ✓ | ✓ | Changes before confirming |
| 0284 | DeepSeek | ✓ | ✗ | ✓ | ✗ | "add a 2 liter coke to it" is about the **placed** order: the label made a new order line. Should be no items (prompt rule exists, not applied) |
| 0297 | Haiku | ✓ | ✓ | ✓ | ✗ | Extra breakfast-sandwich line from "we'll go with the regular one" (leaked card wording) |
| 0298 | Gemini | ✓ | ✓ | ✓ | ✓ | |
| 0314 | Gemini | ~ | ✓ | ✓ | ✓ | Formal ("Hello, I would like to order…") |
| 0316 | Gemini | ✓ | ✗ | ✓ | ✓ | Changes before confirming |
| 0332 | Gemini | ✓ | ✗ | ✓ | ✓ | "SOME ONION RINGS" → quantity unclear, right by the rules |
| 0343 | DeepSeek | ✓ | ✓ | ✓ | ✓ | |
| 0365 | DeepSeek | ✓ | ✗ | ✓ | ✓ | Adds mods the card didn't have; the label splits "avocado on 2 of em" correctly |
| 0369 | Haiku | ✓ | ✓ | ✓ | ✓ | |
| 0406 | Haiku | ✓ | ✓ | ~ | ✓ | "Just the 2 onion rings then" as SMALL_TALK |
| 0425 | DeepSeek | ✓ | ✓ | ✓ | ✓ | |
| 0454 | Haiku | ✓ | ✓ | ✗ | ✗ | Garbled fragment: the teacher guessed "2 bagels". Should be UNKNOWN, no order |
| 0458 | Gemini | ✓ | ✗ | ✓ | ✓ | No menu question. Latte size never stated → combo choice missing, correct |
| 0460 | Gemini | ✓ | ✓ | ✗ | ✓ | "no house cheese blend though", "and add thick crust", "with onions" right after ordering the pizza → MODIFY_ORDER; dev gold labels this PLACE_ORDER (a-dev-020, a-dev-071). "okay so" → UNKNOWN |
| 0490 | DeepSeek | ✓ | ✓ | ✓ | ✓ | |

## Totals

- Realistic: 28/30 (+1 debatable: Gemini's formal style). Card followed: 19/30 (flag-heavy sample).
- Intents fully right: 26/30 chats (+3 debatable). Order right: 27/30 (+1 debatable, 0160 to drop).

## Teacher patterns to fix (label prompt v0.3; check on dev again)

1. PLACE vs MODIFY: adding a detail to an item while ordering it ("w hazelnut syrup", "no pickles on 2", "add thick
   crust") is PLACE_ORDER; MODIFY_ORDER changes something already stated ("make it 2", "swap", "make the fries
   large"). Remove the v0.2 size rule, which got a-dev-040 wrong.
2. A message answering the business's question takes the label of the request it serves ("sam" for a status
   lookup → ORDER_STATUS).
3. Garbled or cut-off text is UNKNOWN with no items; never guess an item from a fragment.
4. Adding to an already-placed order ("add a coke to it" after a status question) creates no new order lines.
