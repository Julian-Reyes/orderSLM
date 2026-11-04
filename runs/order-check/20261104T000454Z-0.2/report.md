# Order checker `order-check@0.2`: luna, jev, openai-decisions on the student's orders

Whole-order check (spec §11b). Student `qwen3.5-0.8b-single-v2`. 42 orders that are not the same action as gold (scorer@0.3) and 42 that are (seeded sample, same number per split). Every checker sees the same chat, menu and order text. Fresh helped shape this version's rules: its numbers are seen while fixing, not held out.

Caught = a wrong order flagged; false alarm = a right order flagged. 95% CI in brackets.

| checker | wrong orders caught | false alarms | dev caught | dev false alarms | fresh caught | fresh false alarms | cost |
|---|---|---|---|---|---|---|---|
| luna | 33/42 (79%, 64–88%) | 6/42 (14%, 7–28%) | 15/19 (79%, 57–91%) | 4/19 (21%, 9–43%) | 18/23 (78%, 58–90%) | 2/23 (9%, 2–27%) | $0.0122 |
| jev | 28/42 (67%, 52–79%) | 2/42 (5%, 1–16%) | 12/19 (63%, 41–81%) | 2/19 (11%, 3–31%) | 16/23 (70%, 49–84%) | 0/23 (0%, 0–14%) | $0.0048 |
| openai-decisions | 25/42 (60%, 44–73%) | 4/42 (10%, 4–22%) | 11/19 (58%, 36–77%) | 2/19 (11%, 3–31%) | 14/23 (61%, 41–78%) | 2/23 (9%, 2–27%) | $0.0098 |

| what is wrong (a chat counts once per kind) | luna | jev | openai-decisions |
|---|---|---|---|
| field:missing | 11/15 (73%, 48–89%) | 10/15 (67%, 42–85%) | 8/15 (53%, 30–75%) |
| missing_item | 8/13 (62%, 36–82%) | 9/13 (69%, 42–87%) | 7/13 (54%, 29–77%) |
| extra_item | 10/13 (77%, 50–92%) | 11/13 (85%, 58–96%) | 8/13 (62%, 36–82%) |
| wrong_quantity | 5/8 (62%, 31–86%) | 3/8 (38%, 14–69%) | 2/8 (25%, 7–59%) |
| wrong_variant | 8/8 (100%, 68–100%) | 8/8 (100%, 68–100%) | 7/8 (88%, 53–98%) |
| wrong_modifications | 6/7 (86%, 49–97%) | 4/7 (57%, 25–84%) | 5/7 (71%, 36–92%) |
| broken_answer | 4/4 (100%, 51–100%) | 3/4 (75%, 30–95%) | 4/4 (100%, 51–100%) |
| wrong_quantity+modifications | 0/2 (0%, 0–66%) | 0/2 (0%, 0–66%) | 0/2 (0%, 0–66%) |
| field:time | 1/2 (50%, 9–91%) | 1/2 (50%, 9–91%) | 1/2 (50%, 9–91%) |
| field:payment | 2/2 (100%, 34–100%) | 2/2 (100%, 34–100%) | 2/2 (100%, 34–100%) |
| wrong_combo_picks | 1/1 (100%, 21–100%) | 0/1 (0%, 0–79%) | 0/1 (0%, 0–79%) |
| field:decision | 1/1 (100%, 21–100%) | 1/1 (100%, 21–100%) | 1/1 (100%, 21–100%) |

| chat | student's order | what is wrong | luna | jev | openai-decisions | luna's reason |
|---|---|---|---|---|---|---|
| dev a-dev-011 | wrong | wrong_combo_picks, field:missing | flag | ok | ok | The customer did not specify a drink, but the record lists Coke. |
| dev a-dev-012 | wrong | broken_answer | flag | ok | flag | The customer ordered two large cheese pizzas for delivery and said they would pay by card, but the record says no new order was placed. |
| dev a-dev-017 | wrong | missing_item, extra_item | flag | flag | flag | The pizza is recorded with invalid 'mushroom_pizza' and 'olives' halves instead of one extra-large pizza with mushrooms and olives on one half and sausage and jalapeños on the other; extra-large is a valid size. |
| dev a-dev-019 | wrong | extra_item | flag | flag | flag | The muffin should have been removed after the customer’s correction, but it remains on the order. |
| dev a-dev-020 | wrong | wrong_quantity+modifications, missing_item | ok | ok | ok |  |
| dev a-dev-039 | wrong | wrong_modifications | ok | ok | ok |  |
| dev a-dev-045 | wrong | wrong_quantity, field:missing | flag | ok | ok | The customer said “some” garlic knots, so the quantity should be recorded as unclear rather than 1. |
| dev a-dev-048 | wrong | missing_item, extra_item | flag | flag | flag | The customer ordered one Breakfast Sandwich on a croissant, but the record lists one plain Croissant. |
| dev a-dev-049 | wrong | wrong_variant, extra_item, field:missing | flag | flag | ok | The customer did not specify which other shake flavor they wanted, so recording a strawberry milkshake is unsupported. |
| dev a-dev-061 | wrong | missing_item, extra_item, field:missing | flag | flag | flag | The customer asked for a Mountain Dew, but the record lists a Dr Pepper. |
| dev a-dev-063 | wrong | wrong_quantity+modifications, missing_item | ok | ok | ok |  |
| dev a-dev-067 | wrong | wrong_variant, field:decision | flag | flag | flag | The customer changed the cheeseburger to a double, but the record still lists a single-patty cheeseburger. |
| dev a-dev-073 | wrong | field:time | ok | ok | ok |  |
| dev a-dev-074 | wrong | missing_item, wrong_modifications, missing_item, extra_item, extra_item, field:missing | flag | flag | flag | The three “BEC on bagels” are breakfast sandwiches on bagels, not plain bagels, and the two croissants should be marked warm. |
| dev a-dev-075 | wrong | field:payment | flag | flag | flag | The customer said they would pay with two $100 bills ($200), but the record says $20.00. |
| dev a-dev-079 | wrong | wrong_variant, field:missing | flag | flag | flag | The two pepperoni pizzas should be extra large after the customer accepted that XL was the biggest size, but the record lists them as personal. |
| dev a-dev-083 | wrong | missing_item, wrong_modifications | flag | flag | flag | The order is missing an everything bagel with cream cheese, and it adds butter to the chocolate croissant even though the customer did not request it. |
| dev a-dev-085 | wrong | missing_item | flag | flag | ok | The order is missing the large pepperoni pizza the customer requested. |
| dev a-dev-089 | wrong | field:payment | flag | flag | flag | The customer said they had already sent payment, but the record lists payment as cash. |
| fresh a-fresh-007 | wrong | wrong_quantity | ok | ok | ok |  |
| fresh a-fresh-009 | wrong | wrong_variant, field:missing | flag | flag | flag | The customer said “big,” which is not a menu size, so the recorded Large 14-inch size is incorrect. |
| fresh a-fresh-016 | wrong | wrong_variant, missing_item | flag | flag | flag | The record lists three chocolate chip muffins instead of two chocolate chip muffins and one banana nut muffin, and it omits the large latte with oat milk. |
| fresh a-fresh-024 | wrong | field:time | flag | flag | flag | The pickup time was changed to 11:30, but the record still says 11. |
| fresh a-fresh-028 | wrong | wrong_variant | flag | flag | flag | The customer asked for a bottled water without specifying a size, but the record assigns it a 20 oz size that is not available for this item. |
| fresh a-fresh-034 | wrong | broken_answer | flag | flag | flag | The customer placed a new order for a cheeseburger combo with large fries and lemonade, but the record says no new order was placed. |
| fresh a-fresh-037 | wrong | wrong_modifications | flag | ok | ok | The Americano is requested black, but black is not a menu option to add; the record should not list it as an add-on. |
| fresh a-fresh-039 | wrong | extra_item | flag | flag | flag | The customer cancelled the Coke, but the recorded order still includes one Coke. |
| fresh a-fresh-043 | wrong | wrong_quantity | flag | ok | ok | The customer ordered 4 veggie burgers total, with 2 of them having jalapeños, but the record lists 4 plain burgers plus 2 with jalapeños. |
| fresh a-fresh-044 | wrong | wrong_quantity, wrong_modifications, field:missing | flag | ok | flag | The customer said “a few” blueberry muffins, so the quantity is unclear, but the record lists 2. |
| fresh a-fresh-049 | wrong | missing_item, extra_item, field:missing | ok | ok | ok |  |
| fresh a-fresh-051 | wrong | extra_item | flag | flag | ok | The customer dropped the muffin, but the recorded order still includes one chocolate chip muffin. |
| fresh a-fresh-056 | wrong | wrong_quantity, field:missing | ok | flag | ok |  |
| fresh a-fresh-057 | wrong | wrong_quantity, missing_item, extra_item, field:missing | ok | flag | ok |  |
| fresh a-fresh-063 | wrong | wrong_variant, field:missing | flag | flag | flag | The customer said “big” without specifying a menu size, so the size should be recorded as unclear rather than Large 14-inch. |
| fresh a-fresh-065 | wrong | wrong_quantity | flag | ok | ok | The customer ordered one 2-liter Dr Pepper, but the record lists two. |
| fresh a-fresh-066 | wrong | missing_item, wrong_modifications, extra_item | flag | flag | flag | The customer ordered one breakfast sandwich on a croissant, but the record lists a plain croissant. |
| fresh a-fresh-073 | wrong | extra_item | flag | flag | flag | The customer cancelled the vanilla shake, but the recorded order still includes it. |
| fresh a-fresh-074 | wrong | broken_answer | flag | flag | flag | The customer placed a new order for 3 bacon burgers with BBQ sauce and 3 lemonades for pickup at 12:45, paying by card, but the record says no new order was placed. |
| fresh a-fresh-080 | wrong | wrong_modifications, wrong_variant, field:missing | flag | flag | flag | The pizza substitutes Fresh mozzarella, which the customer did not request and is not vegan cheese, and the bottled water is incorrectly assigned a 20 oz size. |
| fresh a-fresh-084 | wrong | broken_answer | flag | flag | flag | The customer placed an order for one double cheeseburger and one lemonade for delivery to 18 Primrose Ln, paying cash, but the record says no new order was placed. |
| fresh a-fresh-087 | wrong | missing_item, extra_item, field:missing | ok | ok | ok |  |
| fresh a-fresh-089 | wrong | wrong_quantity, field:missing | flag | flag | flag | The customer said “a few,” so the quantity should be recorded as unclear rather than 2. |
| dev a-dev-007 | right |  | ok | ok | ok |  |
| dev a-dev-014 | right |  | ok | ok | ok |  |
| dev a-dev-015 | right |  | ok | ok | ok |  |
| dev a-dev-018 | right |  | ok | ok | ok |  |
| dev a-dev-023 | right |  | flag | flag | flag | The customer corrected the delivery address to 104 River Rd, but the record still lists 140 River Rd. |
| dev a-dev-024 | right |  | ok | ok | ok |  |
| dev a-dev-026 | right |  | ok | ok | ok |  |
| dev a-dev-030 | right |  | ok | ok | ok |  |
| dev a-dev-034 | right |  | flag | ok | ok | Artichoke hearts are not an available Supreme Pizza topping on the menu, but the record lists them as an option. |
| dev a-dev-038 | right |  | flag | flag | flag | The drink is recorded as a literal non-menu item, but the customer’s previous drink is unknown and should be recorded as unclear or not stated. |
| dev a-dev-051 | right |  | ok | ok | ok |  |
| dev a-dev-058 | right |  | flag | ok | ok | The customer asked for the delivery charge with the order, indicating delivery, but the record lists fulfillment as not stated. |
| dev a-dev-066 | right |  | ok | ok | ok |  |
| dev a-dev-071 | right |  | ok | ok | ok |  |
| dev a-dev-078 | right |  | ok | ok | ok |  |
| dev a-dev-081 | right |  | ok | ok | ok |  |
| dev a-dev-087 | right |  | ok | ok | ok |  |
| dev a-dev-088 | right |  | ok | ok | ok |  |
| dev a-dev-091 | right |  | ok | ok | ok |  |
| fresh a-fresh-002 | right |  | ok | ok | ok |  |
| fresh a-fresh-003 | right |  | ok | ok | ok |  |
| fresh a-fresh-005 | right |  | flag | ok | flag | Honey is not an available latte add-in on the menu, but the order records it. |
| fresh a-fresh-006 | right |  | ok | ok | ok |  |
| fresh a-fresh-010 | right |  | ok | ok | ok |  |
| fresh a-fresh-011 | right |  | ok | ok | ok |  |
| fresh a-fresh-015 | right |  | ok | ok | ok |  |
| fresh a-fresh-017 | right |  | ok | ok | ok |  |
| fresh a-fresh-018 | right |  | ok | ok | ok |  |
| fresh a-fresh-019 | right |  | ok | ok | ok |  |
| fresh a-fresh-023 | right |  | ok | ok | ok |  |
| fresh a-fresh-029 | right |  | ok | ok | ok |  |
| fresh a-fresh-031 | right |  | flag | ok | ok | The customer ordered 5 Supreme pizzas, but the record lists 3 with olives and 2 without. |
| fresh a-fresh-032 | right |  | ok | ok | ok |  |
| fresh a-fresh-038 | right |  | ok | ok | ok |  |
| fresh a-fresh-040 | right |  | ok | ok | ok |  |
| fresh a-fresh-042 | right |  | ok | ok | ok |  |
| fresh a-fresh-048 | right |  | ok | ok | ok |  |
| fresh a-fresh-058 | right |  | ok | ok | ok |  |
| fresh a-fresh-078 | right |  | ok | ok | ok |  |
| fresh a-fresh-081 | right |  | ok | ok | ok |  |
| fresh a-fresh-082 | right |  | ok | ok | ok |  |
| fresh a-fresh-090 | right |  | ok | ok | flag |  |

Cost: $0.0268.
