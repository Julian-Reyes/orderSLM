# PIZZA benchmark

The PIZZA dataset ([amazon-science/pizza-semantic-parsing-dataset](https://github.com/amazon-science/pizza-semantic-parsing-dataset))
is used for one thing only: an extraction evaluation on third-party, human-written pizza and drink orders.
It is **CC-BY-NC-4.0** (confirmed from its LICENSE and README), so no dataset file and nothing derived from it
(catalog, coverage map, converted cases, reports) is committed. Everything lives in the gitignored
`data/external/pizza/`; only the script `src/orderslm/data/pizza.py` is in the repo.

```
uv run python -m orderslm.data.pizza --download --convert
```

| Step | What happens | Output (all under `data/external/pizza/`) |
|---|---|---|
| Download | The test split, LICENSE, README and the entity catalogs, pinned to commit `814d6d0` (last change 2022-12-07); sha256 recorded | `PIZZA_test.json`, `catalogs/`, `MANIFEST.json` |
| Sample | 200 of the 1,357 test orders, `random.Random(20261007)`, drawn by row index before reading any order. **Orders are never filtered to fit a menu**; an order that can't be converted is reported. | `benchmark/report.json` (`sample_indices`) |
| Catalog | The PIZZA benchmark catalog: every topping, style, size and drink the sample mentions, plus unused catalog entities as distractors up to 35 toppings, 6 recipe pizzas, 4 crusts, 4 sizes, 8 drinks (padding only, never trimming) | `benchmark/pizza-benchmark.json`, `benchmark/coverage.json` |
| Convert | Each order becomes a one-message conversation (`split: benchmark`) with a gold `ExtractionOutput` | `benchmark/cases.jsonl` |

The benchmark catalog is separate from Halfmoon Pizza, which is a realistic menu for chat data and the demo
(docs/MENUS.md). It is used only for the PIZZA evaluation. `load_cases()` needs `ORDERSLM_UNSEAL_TEST`, like
the sealed test split: no prompt tuning, few-shot examples or training data from it.

## Current build (seed 20261007)

| Entity | Used by the sample | Distractors | On the menu |
|---|---|---|---|
| Toppings | 29 | 6 | 35 |
| Recipe pizzas (styles) | 7 | 0 | 7 + plain `pizza` |
| Crusts (styles) | 4 | 0 | 4 |
| Pizza sizes | 6 | 0 | 6 |
| Drinks | 10 | 0 | 10 |
| Drink variants | 6 | 0 | 6 |
| Topping amounts | 2 (`extra`, `light`) | | |

199 of 200 sampled orders convert (263 items; 45 orders have more than one suborder). The one failure,
row 784, has two crust styles ("pan" and "stuff crust") plus a recipe ("veggies lover"), and its words not
in the catalog can be paired with the parse in more than one way. It is reported, not guessed.

## Conversion rules

- **Values come from EXR, wording from TOP.** EXR is the dataset's canonical parse; TOP marks the customer's
  words. The two are paired suborder by suborder and attribute by attribute, and must agree. A TOP word that
  isn't in the dataset's own catalog ("bell peppers", "more cheese") takes its value from the EXR attribute
  it pairs with. If that pairing isn't unique, the order is reported (`failures`). This happened for 10
  sampled orders, 1 word each (`top_words_filled_from_exr`).
- **Implicit quantity:** a suborder without a number word ("large pie with onions") has EXR `NUMBER 1`.
- **Pizza item:** a recipe style (`HAWAIIAN`, `MEAT_LOVER`, …) → that pizza item; otherwise the plain `pizza`.
  Crust styles (`THIN_CRUST`, `DEEP_DISH`, `NEW_YORK_STYLE`, …; listed in `CRUST_STYLES`) → an exclusive
  `crust` modifier. Two recipe styles, or a negated recipe style, can't be converted and are reported.
- **Toppings:** `TOPPING` → add; `COMPLEX_TOPPING` → add with `amount` extra/light; `NOT` → remove (crusts
  too: "no thin crust" → remove `thin_crust`). **"No extra cheese"** (a negated amount) means the default
  amount, so it produces no modification; counted in `dropped_negated_amounts` (15 in this build).
- **Drinks:** one variant per distinct size/volume/container combination the sample uses (`large`, `can`,
  `2_liter`, …), so nothing is lost; a drink with none of them is `regular` (the default). These choices are
  for review against `drink_variant_examples` in the report (M1 review, item 2).
- **Order-level fields:** PIZZA orders never state fulfillment, time, address, payment or name, so they are
  `not_mentioned`, and `missing_or_ambiguous` + `clarification_question` come from the deterministic rules
  (`core/missing.py`, `core/replies.template_question`). Pizza sizes have no default, so an order without a
  size also has `item_variant` missing.
- **Scoring:** PIZZA results are scored on `gold_extraction.items` only (menu item, quantity, size,
  modifications), since everything else is filled by rules rather than by the dataset.
- Prices on the benchmark catalog are placeholders (prices are never scored).
