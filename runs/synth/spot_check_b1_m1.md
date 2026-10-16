# Spot check of the bulk labels (`b1/audit.md`, `m1/audit.md`, 30 chats each)

Reviewed by Claude at Julian's request (2026-10-16); not a human review. Labels: `teacher-label@0.5`.

| | b1 (single menu) | m1 (mega-menu) |
|---|---|---|
| Order right | 28/30 | 30/30 |
| Intents fully right | ~26/30 | ~26/30 |

Teacher errors:
- b1-0438: "i need pizza for the kids" became 1 cheese pizza; a generic "pizza" at a place with 8 pizzas should be
  an ambiguous unmatched item.
- b1-1143: "ok no cheese then" on a veggie burger (cheese is only an add-on there) became "remove cheese". New check
  `check_removals` (synthetic labels only; PIZZA gold legitimately negates add-ons) now drops such labels: 4 across
  p3/b1/m1.
- m1-0281: mods while ordering ("but no pepperoni lol", "add green peppers instead") as MODIFY_ORDER (rule says
  PLACE_ORDER). m1-0116: details given after a re-confirm ("perfect. we'll pick it up, paying by card") as
  MODIFY_ORDER: v0.4's "after a confirm, anything added is MODIFY" is read too broadly.

Inconsistencies (open question for Julian):
- A yes to a read-back ending "Is that everything?" / "is that all?" is sometimes CONFIRM_ORDER (b1-0975, m1-0340),
  sometimes SMALL_TALK (b1-0698, m1-0370). Dev gold only has "Is that right?" read-backs (always CONFIRM_ORDER).
- "some fries" → quantity unclear (b1-0339) vs 1 (m1-0296).
