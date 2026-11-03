# Order checker pilot: `openai/gpt-6-luna@low` on the student's wrong orders

`order-check@0.1`, whole-order check (spec §11b). Student `qwen3.5-0.8b-single-v2`; its final orders on dev and fresh that are not the same action as gold (scorer@0.3). **Every order here is wrong, so only the catch rate is measured, not false alarms.** Dev may tune the checker; fresh only measures it.

| set | wrong orders caught |
|---|---|
| all | 32/42 (76%, 95% CI 61–87%) |
| dev | 15/19 (79%, 95% CI 57–91%) |
| fresh | 17/23 (74%, 95% CI 54–87%) |
| readable orders (the student's answer was valid) | 28/38 (74%, 95% CI 58–85%) |
| broken answers (shown as 'no new order') | 4/4 (100%, 95% CI 51–100%) |

| what is wrong (a chat counts once per kind) | caught |
|---|---|
| field:missing | 9/15 (60%, 95% CI 36–80%) |
| extra_item | 11/13 (85%, 95% CI 58–96%) |
| missing_item | 11/13 (85%, 95% CI 58–96%) |
| wrong_quantity | 6/8 (75%, 95% CI 41–93%) |
| wrong_variant | 5/8 (62%, 95% CI 31–86%) |
| wrong_modifications | 6/7 (86%, 95% CI 49–97%) |
| broken_answer | 4/4 (100%, 95% CI 51–100%) |
| field:payment | 1/2 (50%, 95% CI 9–91%) |
| field:time | 1/2 (50%, 95% CI 9–91%) |
| wrong_quantity+modifications | 2/2 (100%, 95% CI 34–100%) |
| field:decision | 1/1 (100%, 95% CI 21–100%) |
| wrong_combo_picks | 1/1 (100%, 95% CI 21–100%) |

| chat | what is wrong | caught | checker's reason |
|---|---|---|---|
| dev a-dev-011 | wrong_combo_picks, field:missing | yes | The customer did not specify a drink, so recording Coke adds an unrequested option. |
| dev a-dev-012 | broken_answer | yes | The customer placed a new order for two large cheese pizzas for delivery, paying by card. |
| dev a-dev-017 | missing_item, extra_item | yes | The pizza is recorded with the wrong halves and omits the requested XL size: it should be half mushroom and olives, half sausage and jalapeños. |
| dev a-dev-019 | extra_item | yes | The chocolate chip muffin should have been removed, but it is still listed in the order. |
| dev a-dev-020 | wrong_quantity+modifications, missing_item | yes | Only 2 of the 4 cheeseburgers were specified as having no pickles, but the record applies no pickles to all 4. |
| dev a-dev-039 | wrong_modifications | **no** |  |
| dev a-dev-045 | wrong_quantity, field:missing | **no** |  |
| dev a-dev-048 | missing_item, extra_item | yes | The customer ordered a BEC on a croissant, but the record lists a plain croissant. |
| dev a-dev-049 | wrong_variant, extra_item, field:missing | yes | The customer replaced the chocolate milkshake with a lemonade, so the order should have one strawberry milkshake and one lemonade, not an additional lemonade alongside the chocolate milkshake. |
| dev a-dev-061 | missing_item, extra_item, field:missing | yes | The customer ordered a Mountain Dew, but the record lists a Dr Pepper. |
| dev a-dev-063 | wrong_quantity+modifications, missing_item | yes | The customer specified no onion for only 2 of the 4 cheeseburgers, but the record lists all 4 without onions. |
| dev a-dev-067 | wrong_variant, field:decision | yes | The customer requested a double burger, but the record lists a single-patty cheeseburger. |
| dev a-dev-073 | field:time | **no** |  |
| dev a-dev-074 | missing_item, wrong_modifications, missing_item, extra_item, extra_item, field:missing | yes | The record omits the request to warm the croissants and the medium size for the oat lattes. |
| dev a-dev-075 | field:payment | **no** |  |
| dev a-dev-079 | wrong_variant, field:missing | yes | The 2 pepperoni pizzas should be extra large, since the customer accepted that extra large was the biggest size. |
| dev a-dev-083 | missing_item, wrong_modifications | yes | The record omits the everything bagel with schmear and adds butter to the chocolate croissant, which the customer did not request. |
| dev a-dev-085 | missing_item | yes | The record omits the large pepperoni pizza the customer ordered. |
| dev a-dev-089 | field:payment | yes | The record lists payment as cash, but the customer said they had already sent the payment. |
| fresh a-fresh-007 | wrong_quantity | yes | The customer ordered 3 hot chocolates total, with caramel on 2 of them, but the record lists 5 drinks. |
| fresh a-fresh-009 | wrong_variant, field:missing | **no** |  |
| fresh a-fresh-016 | wrong_variant, missing_item | yes | The record lists the second muffin as chocolate chip instead of banana nut and omits the large oat milk latte. |
| fresh a-fresh-024 | field:time | yes | The pickup time should be 11:30, not 11. |
| fresh a-fresh-028 | wrong_variant | **no** |  |
| fresh a-fresh-034 | broken_answer | yes | The customer placed a new order for a cheeseburger combo with large fries and lemonade, but the record says no new order was placed. |
| fresh a-fresh-037 | wrong_modifications | yes | The hot chocolate was recorded as medium even though the customer did not specify a size. |
| fresh a-fresh-039 | extra_item | yes | The customer canceled the Coke, but it remains on the recorded order. |
| fresh a-fresh-043 | wrong_quantity | yes | The record lists 4 plain veggie burgers plus 2 with jalapeños, but the customer ordered 4 veggie burgers total, 2 with jalapeños. |
| fresh a-fresh-044 | wrong_quantity, wrong_modifications, field:missing | yes | “A few” blueberry muffins does not specify 2, so the recorded quantity is unsupported by the chat. |
| fresh a-fresh-049 | missing_item, extra_item, field:missing | **no** |  |
| fresh a-fresh-051 | extra_item | yes | The customer dropped the chocolate muffin, but the record still includes it. |
| fresh a-fresh-056 | wrong_quantity, field:missing | **no** |  |
| fresh a-fresh-057 | wrong_quantity, missing_item, extra_item, field:missing | yes | The customer requested one drink from the listed options, but no drink is recorded. |
| fresh a-fresh-063 | wrong_variant, field:missing | **no** |  |
| fresh a-fresh-065 | wrong_quantity | yes | The customer ordered one 2-liter Dr Pepper, but the record lists two. |
| fresh a-fresh-066 | missing_item, wrong_modifications, extra_item | yes | The customer ordered one breakfast sandwich on a croissant, but the record lists only a croissant. |
| fresh a-fresh-073 | extra_item | yes | The customer cancelled the vanilla shake, but it is still listed in the recorded order. |
| fresh a-fresh-074 | broken_answer | yes | The customer placed a new order for three bacon burgers with BBQ sauce and three lemonades, for pickup at 12:45 and payment by card, but the record says no new order was placed. |
| fresh a-fresh-080 | wrong_modifications, wrong_variant, field:missing | yes | The customer requested vegan cheese, but the record lists fresh mozzarella, which is not vegan. |
| fresh a-fresh-084 | broken_answer | yes | The customer placed an order for one double cheeseburger and one lemonade for delivery to 18 Primrose Ln, paying cash. |
| fresh a-fresh-087 | missing_item, extra_item, field:missing | **no** |  |
| fresh a-fresh-089 | wrong_quantity, field:missing | yes | The customer asked for “a few” muffins, but the record assigns a specific quantity of 2. |

No verdict: 0. Cost: $0.0032.
