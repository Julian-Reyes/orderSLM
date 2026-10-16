# Decision providers and student models: verified facts

Checked against official pages on **2026-10-16** (CLAUDE.md: verify contracts, licenses and prices before
integrating). Re-check before each paid run or release.

## Decision providers (spec §11)

### Julia-1 (Supersonic Labs): local
Source: [huggingface.co/SupersonicLabs/Julia-1](https://huggingface.co/SupersonicLabs/Julia-1) (model card).

- License: Apache 2.0 for the model artifacts; the training pipeline is not published (so no fine-tuning, spec §11).
- 144.3M parameters (mmBERT-small encoder + decision head). FP32 weights 550.5 MiB.
- Downloaded 2026-10-16 (Julian approved) to `models/julia-1/` (gitignored), revision
  `a85b127321d580d65176c89ced8273f305745d85`; `model.safetensors` sha256 `df853bf7…ad95b72`, equal to
  `provenance.json` `weights_sha256`. Code read before use: safetensors only (no pickle), `trust_remote_code=False`
  everywhere, subprocess only in the optional native router build (not used for inference).
- Needs Python ≥ 3.11 and the bundled package `supersonic-julia` (`pip install -e ./Julia-1`), which depends on
  `torch>=2.6`, `transformers>=5.0,<5.1`, `safetensors>=0.5`, `numpy>=1.26`. **Not installed yet**: torch +
  transformers are major dependencies (ask first).
- API: `load_model(path, device="cpu", strict_encoding=True, max_length=8192, head_length=512)`, then
  `engine.predict(state=..., questions={name: {type, instructions, criteria}})`. Types: `choice` (2–20 options),
  `score` (2–20 ordered levels), `noul` (yes/no). Each option ≤ 48 tokens; 8,192 combined tokens by default
  (accuracy benchmarks used 1,024; 8k accuracy "not established"). Output: `choice` + `probabilities`
  (+ `max_probability`); probabilities are softmax values, "not guaranteed certainty".

### OpenAI Decisions: hosted
Source: [developers.openai.com/api/docs/guides/decisions](https://developers.openai.com/api/docs/guides/decisions).

- `POST https://api.openai.com/v1/decisions`. **Public beta** ("we expect to GA in the coming weeks").
- Model: `gpt-6-luna` only. Input: text, or user messages with `input_text` / `input_image` (base64 data URLs).
- `questions[]`, each with a unique `name`: `predicate` (`instructions`) → `probability`; `choice`
  (`instructions`, `choices[{value, description}]`) → `choice`, `probabilities[]`, `confidence`; `score`
  (`instructions`, `levels[{label, description}]`, low to high) → `score`, `probabilities[]`, `confidence`.
  An answer can be `type: "refusal"` (fields beyond `name` not documented).
- Limits on questions, choices or input size: **not documented** (test early with all 15 labels).
- Price: **$0.10 per 1M input tokens; no output, cache-read or cache-write charges.** Regional and long-context
  multipliers apply. Rate limits not stated. ZDR/HIPAA for eligible customers.

### Jev (TypeSafe): hosted
Source: [docs.typesafe.ai/api.md](https://docs.typesafe.ai/api.md) (HTTP API reference). The vendor's agent
"skill" (`typesafe-ai/skills`) was read as reference only and not installed: our adapter calls the HTTP API.

- `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer <key>`, JSON body (≤ 32 MiB; optional
  gzip/zstd).
- Body: `model` (e.g. `jev-latest`; other ids on the models page), `state` (string, object or array),
  `questions` (map of id → question; ids are not sent to the model). Types: `noul` (yes/no, optional `criteria`
  `{true, false}`), `choice` (`criteria` map option → description, **up to 255 options**), `score` (2–10 levels).
- Response: `model` (exact version, e.g. `jev-1.13.0`), `answers` per id (`choice` + `probabilities` +
  `confidence`; `noul` as a 0–1 number; `score` + `legend` + `probabilities` + `confidence`), `usage`
  (`input_tokens`, `output_tokens`).
- Errors: 400 (incl. `max_tokens_exceeded`), 401, 413, 415, 422, 429 (rate limit; back off), 529 (overloaded).
- **Not documented on that page: price per token, rate limits, context length, data retention / training use.**
  Check the pricing and data pages once Julian has an account, then run a tiny priced test before any bulk use.
- Smoke test 2026-10-16 (`runs/jev-smoke/20261016T174016Z`): HTTP 200, 343 ms, model `jev-1.13.0`, 715 input / 160
  output tokens for one 15-label choice; picked the gold label with confidence 1.0. Price reported by a Google
  summary: $0.042 per 1M input tokens, output free (to verify on TypeSafe's pricing page).

## Student candidates (spec §9)

Sources: the official Hugging Face model cards
([Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B), [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B),
[Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B), [Gemma 4 E2B-it](https://huggingface.co/google/gemma-4-E2B-it),
[Gemma 4 license](https://ai.google.dev/gemma/docs/gemma_4_license)).

| Model | License | Size | Modality | Notes |
|---|---|---|---|---|
| Qwen3.5-0.8B | Apache 2.0 | 0.8B (0.9B in safetensors) | text + vision encoder | "latest transformers" required (main branch); non-thinking by default; vLLM `--language-model-only` skips the vision encoder; intended for "task-specific fine-tuning" |
| Qwen3.5-2B | Apache 2.0 | 2B | text + vision encoder | same as 0.8B; "more prone to entering thinking loops" in thinking mode; a `-Base` model exists |
| Qwen3-1.7B | Apache 2.0 | 1.7B (2B in safetensors) | text only | transformers ≥ 4.51.0; mature tooling (many adapters/quantizations) |
| Gemma 4 E2B-it | Apache 2.0 (card + Google's Gemma 4 license page, which is the Apache 2.0 text) | 2.3B effective, **5.1B with embeddings** | text + image + audio | no gating notice on the card; "latest Transformers" |

All four allow fine-tuning and redistribution of derivatives under Apache 2.0 (keep the license and notices, mark
changes). Download size is not on the cards; from the parameter counts in BF16 it is roughly 1.8 GB, 4 GB, 4 GB and
10 GB (**estimate**). Local disk had 15 GB free on 2026-10-16.
