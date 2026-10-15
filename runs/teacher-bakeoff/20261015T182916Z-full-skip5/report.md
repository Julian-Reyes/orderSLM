# Teacher bake-off: 20261015T182916Z-full-skip5

full 35 (bake-off set positions 6-40) conversations from dev (Source A, Claude-written), prompt `teacher-extract@0.2`, schema `extraction@0.4`, commit `f800c833ffda458392fbc60d495f40f4acc7cb24`, cache `record`. Actual cost of this run: $0.5811 (estimate $1.5234).

| Variant | JSON valid | Item F1 | Exact | Grounding issues | In tok/conv | Out tok/conv | Reasoning/conv | Cost (this run) | Cost/1k conv | p50 ms |
|---|---|---|---|---|---|---|---|---|---|---|
| `openai/gpt-6-luna@none` | 34/35 | 97.4% | 85.7% | 1 | 9778.8 | 371.1 | 0.0 | $0.0203 | $0.58 | 3612 |
| `openai/gpt-6-luna@low` | 35/35 | 98.3% | 91.4% | 2 | 9778.8 | 473.4 | 114.7 | $0.0221 | $0.63 | 5899 |
| `openai/gpt-6-luna@medium` | 32/35 | 90.1% | 82.9% | 1 | 9778.8 | 697.4 | 294.1 | $0.0260 | $0.74 | 4971 |
| `anthropic/claude-haiku-5-5@off-low` | 30/35 | 91.4% | 60.0% | 1 | 12285.1 | 613.3 | 0.0 | $0.0537 | $1.54 | 2643 |
| `anthropic/claude-haiku-5-5@off-medium` | 28/35 | 90.9% | 62.9% | 1 | 12285.1 | 610.1 | 0.0 | $0.0537 | $1.53 | 2527 |
| `anthropic/claude-haiku-5-5@on-low` | 32/35 | 96.4% | 88.6% | 0 | 12286.1 | 1182.3 | 599.4 | $0.0637 | $1.82 | 5267 |
| `anthropic/claude-haiku-5-5@on-medium` | 34/35 | 100.0% | 94.3% | 0 | 12286.1 | 1332.3 | 745.0 | $0.0663 | $1.90 | 5553 |
| `google/gemini-3.1-flash-lite@minimal` | 27/35 | 74.1% | 48.6% | 1 | 8111.1 | 530.9 | 0.0 | $0.0989 | $2.82 | 2183 |
| `google/gemini-3.1-flash-lite@default` | 30/35 | 78.2% | 62.9% | 1 | 8111.1 | 604.7 | 0.0 | $0.1027 | $2.94 | 2313 |
| `deepseek/deepseek-flash@none` | 31/35 | 80.7% | 71.4% | 2 | 8332.4 | 439.7 | 0.0 | $0.0132 | $0.38 | 2286 |
| `deepseek/deepseek-flash@low` | 33/35 | 95.5% | 94.3% | 0 | 8357.4 | 1198.7 | 810.6 | $0.0294 | $0.84 | 5386 |
| `deepseek/deepseek-flash@high` | 32/35 | 84.1% | 82.9% | 0 | 8357.4 | 1271.0 | 893.5 | $0.0309 | $0.88 | 5733 |
| **all variants** | | | | | | | | **$0.5811** | | |

Full metrics per variant: `metrics.json`. Raw outputs: `outputs/<variant>/<conversation>.json`.

## Errors and invalid outputs

- `openai/gpt-6-luna@none`: a-dev-064: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `openai/gpt-6-luna@medium`: a-dev-059: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `openai/gpt-6-luna@medium`: a-dev-064: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `openai/gpt-6-luna@medium`: a-dev-021: 1 validation error for ExtractionOutput
items.0
  Value error, L1: an off-menu item can't have variant, modifications or combo picks [type=value_error, input_value={'line_id': 'L1', 'menu_i...bout 30 
- `anthropic/claude-haiku-5-5@off-low`: a-dev-009: 1 validation error for ExtractionOutput
  Value error, clarification_question is required exactly when missing_or_ambiguous is non-empty [type=value_error, input_value={'schema_version': 'extra...icat
- `anthropic/claude-haiku-5-5@off-low`: a-dev-044: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ime would you like it?'}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@off-low`: a-dev-088: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@off-low`: a-dev-070: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@off-low`: a-dev-001: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-009: 1 validation error for ExtractionOutput
  Value error, clarification_question is required exactly when missing_or_ambiguous is non-empty [type=value_error, input_value={'schema_version': 'extra...icat
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-044: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...e sure it gets sorted."}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-020: 1 validation error for ExtractionOutput
  Value error, clarification_question is required exactly when missing_or_ambiguous is non-empty [type=value_error, input_value={'schema_version': 'extra...icat
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-016: 1 validation error for ExtractionOutput
missing_or_ambiguous.0
  Value error, missing_or_ambiguous: line_id is required for item fields only (items) [type=value_error, input_value={'field': 'items', '
- `anthropic/claude-haiku-5-5@off-medium`: a-dev-088: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@on-low`: a-dev-059: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `anthropic/claude-haiku-5-5@on-low`: a-dev-070: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@on-low`: a-dev-001: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `anthropic/claude-haiku-5-5@on-medium`: a-dev-001: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@minimal`: a-dev-080: 1 validation error for ExtractionOutput
  Value error, L3: off-menu item must be listed as item_menu_match/off_menu [type=value_error, input_value={'schema_version': 'extra...ication_question': None},
- `google/gemini-3.1-flash-lite@minimal`: a-dev-033: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@minimal`: a-dev-044: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...let me know your name?'}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@minimal`: a-dev-067: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `google/gemini-3.1-flash-lite@minimal`: a-dev-090: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@default`: a-dev-050: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `google/gemini-3.1-flash-lite@default`: a-dev-044: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...yment method you used?"}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@default`: a-dev-049: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...or pickup or delivery?'}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@default`: a-dev-070: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `google/gemini-3.1-flash-lite@default`: a-dev-005: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `deepseek/deepseek-flash@none`: a-dev-033: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...ication_question': None}, input_type=dict]
 
- `deepseek/deepseek-flash@none`: a-dev-059: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `deepseek/deepseek-flash@none`: a-dev-064: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `deepseek/deepseek-flash@none`: a-dev-049: 1 validation error for ExtractionOutput
  Value error, address is only not_applicable for pickup [type=value_error, input_value={'schema_version': 'extra...for your second shake?'}, input_type=dict]
 
- `deepseek/deepseek-flash@low`: a-dev-067: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `deepseek/deepseek-flash@low`: a-dev-064: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `deepseek/deepseek-flash@high`: a-dev-059: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `deepseek/deepseek-flash@high`: a-dev-067: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
- `deepseek/deepseek-flash@high`: a-dev-064: 1 validation error for ExtractionOutput
customer_decision
  Value error, customer_decision: evidence required for confirmed/cancelled or an agreement, forbidden otherwise [type=value_error, input_valu
