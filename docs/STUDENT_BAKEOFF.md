# M5 student bake-off (spec §9)

_Run 2026-10-19 on Kaggle (2 × T4, free). Run: `runs/student-bakeoff/20261019T182539Z/` (`report.md`,
`summary.json`, per-model `report.md` + raw outputs). Dev data: these numbers choose models, they are not held out._

## Decision

**Keep the default pair: Qwen3.5-0.8B and Qwen3.5-2B** as the M6 students. Per §9 the pair stays unless another
candidate is clearly better or tooling fails. Neither happened:

- **No candidate is clearly better.** Zero-shot, no model writes valid labels (only Qwen3.5-2B, on 3 chats with no
  items). On the diagnostics, Qwen3.5-2B is the closest: valid JSON on 19/20, its contract errors are small type
  slips, and it finds the most menu items. Gemma 4 E2B finds items about as well when its JSON parses, but it breaks
  the JSON on 9/20 and is ~15× slower here. Qwen3-1.7B puts item fields at the wrong level on every chat.
- **Tooling works for Qwen3.5:** it loads and runs in transformers 5.20 (multimodal class, text-only use); Unsloth
  documents LoRA for Qwen3.5 (checked in M5 prep); GGUF builds exist (`unsloth/Qwen3.5-0.8B-GGUF`, `-2B-GGUF`).
- **Risk to watch in M6:** Qwen3.5-0.8B never ended its answer (repeated `"ORDER_STATUS"` to the 3,072-token limit
  on 20/20). Fine-tuning teaches the output format, so this isn't disqualifying zero-shot, but if the 0.8B still
  can't produce valid labels after LoRA, Qwen3-1.7B (text-only, mature tooling) is the fallback small student.

## Setup

- 20 dev chats (seeded sample, seed `20261019`), Source A. Each student gets the exact request the teacher got for
  its training labels (`teacher-label@0.7`: instructions, TeacherLabel JSON schema, menu, chat; ~8–10k input tokens).
- fp32 (T4 has no bf16), greedy decoding, max 3,072 new tokens, `device_map="auto"` over both T4s, one process per
  model. Model cards' sampling settings were not used (greedy is reproducible). Thinking off for Qwen3-1.7B and Gemma
  (Qwen3.5 small models are non-thinking by default).
- One normalization before parsing: a surrounding ```json fence is stripped (counted separately; no model used one).
- Scored by the teacher's own scorer (`label_dev.report`) against reviewed gold; the teacher's saved outputs on the
  same 20 chats are the baseline.

## Results (contract scores)

| model | JSON parses | valid label | item F1 | exact orders | intents right | hit token limit | median latency | total |
|---|---|---|---|---|---|---|---|---|
| Qwen3.5-0.8B | 0/20 | 0/20 | 0.0 | 0/20 | 0/54 | 20/20 | 185 s | 64 min |
| Qwen3.5-2B | 19/20 | 3/20 | 0.0 | 3/20 | 5/54 | 1/20 | 59 s | 21 min |
| Qwen3-1.7B | 20/20 | 0/20 | 0.0 | 0/20 | 0/54 | 0/20 | 87 s | 34 min |
| Gemma 4 E2B | 11/20 | 0/20 | 0.0 | 0/20 | 0/54 | 0/20 | 923 s | 312 min |
| teacher (gpt-6-luna@low) | – | 20/20 | 1.0 | 20/20 | 54/54 | – | – | – |

An invalid label scores as nothing, as in the training pipeline (it would be dropped). Qwen3.5-2B's 3 valid labels are
chats with no items, so its exact orders don't show item skill.

## Diagnostics (not contract scores)

Because every item-bearing label is invalid, two diagnostics show how close each model is (`diagnose()` in
`src/orderslm/eval/student_bakeoff.py`, saved in `summary.json`):

| model | menu item ids right / extra / missed (vs teacher, 27) | F1 | most frequent contract errors |
|---|---|---|---|
| Qwen3.5-0.8B | 0 / 0 / 27 | 0.00 | not JSON ×20 (repetition loop) |
| Qwen3.5-2B | 20 / 6 / 7 | 0.75 | `combo_selections` not a list ×22; `notes` not a string ×20; fulfillment rules ×3 |
| Qwen3-1.7B | 14 / 19 / 13 | 0.47 | item fields (`quantity`, `variant_id`, …) placed on `order` ×20 each; item `evidence` missing ×18 |
| Gemma 4 E2B | 18 / 4 / 9 | 0.73 | `modifications` not a list ×18; item `evidence` missing ×17; not JSON ×9 |

The item-id diagnostic ignores structure (any `menu_item_id` anywhere in the JSON, counted as a multiset).

## Tooling notes (Kaggle T4)

- **Attention memory:** transformers 5.20 calls SDPA with `enable_gqa=True` when there's no mask, which on a T4 in
  fp32 falls back to the math kernel (full scores per head): Qwen3-1.7B ran out of memory at ~8k tokens. Turning the
  flag off (K/V heads repeated first, same attention) lets the memory-efficient kernel run: peak 15 GB → 7 GB.
- **Gemma 4 E2B in fp32 is ~20 GB:** with per-GPU caps (12.6 GiB each) part of it is still offloaded to CPU, so each
  answer took ~15 min. For M6 it would need 16-bit (fp16 on T4, overflow risk) or one bigger GPU.
- Qwen3.5 has few full-attention layers, so it was the cheapest at long inputs.

Smoke tests (1 chat each) that led to these fixes: `runs/student-bakeoff/20261019T144633Z-limit1` (OOM),
`…173309Z-limit1` (one process per model: still OOM), `…174223Z-limit1` (GQA flag + caps: all run).
