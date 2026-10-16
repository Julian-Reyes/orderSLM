# Hand check of the training-label audit flags (Claude, 2026-10-16; not a human review)

## Orders judged not matching by both providers (31 of 2,356)
- ~7 real teacher errors: p3-0057 (kept combo dropped), b1-0356 (a drip coffee never ordered), m1-0019 (swapped-out
  iced tea still listed), p3-0085 (diet coke from the confirmed read-back missing), b1-0711 (stated card payment
  missed), p3-0160 (self-contradicting chat from a card bug: drop), b1-0264 ("same as usual" resolved by a read-back).
- 17 false alarms of one kind: status / payment-claim chats where the customer describes an earlier order, recorded as
  "No order was placed in this chat" (audit wording to fix: earlier orders are not part of the record).
- The rest follow our labeling rules (values only from the customer, default sizes) and were judged against them.
- Precision ≈ 50% on chats with an order, ≈ 23% overall.

## Intents where both providers agree against the teacher (425 messages in 351 chats; 25 sampled)
- ~6–9 real teacher errors: a "that's it" after a read-back + "anything else?" still SMALL_TALK (v0.6 says
  CONFIRM_ORDER; the targeted relabel's pattern missed "nope thats it"); follow-ups in status / complaint / refund chats
  labeled SMALL_TALK instead of keeping the request's label; "did the money on the app go through?" = PAYMENT_CLAIM.
- ~13 are the providers disagreeing with Julian's conventions: adding a detail while ordering ("no tomato pls") =
  PLACE_ORDER (providers: MODIFY_ORDER, 8 of 25); an announcement without items = SMALL_TALK (providers: PLACE_ORDER, 5).
- Precision ≈ 24–36%: the flags are a review queue, not a delete list.
