# Provider terms on training with outputs

Spec §7: before bulk labeling, check each provider's terms on using outputs to train models. This check was due before
M4's bulk labeling and was done late, on 2026-10-19 (after the labels existed). Read from the official pages on that
date. This is our reading of the text, not legal advice.

## How each provider's output is used

| Provider | Model / service | Used for | Output ends up in training data? |
|---|---|---|---|
| OpenAI | `gpt-6-luna` (teacher) | Labels (intents + order) for all training chats | **Yes: the training targets** |
| DeepSeek | flash (generator) | Writes synthetic chats | Yes: training inputs |
| Google | `gemini-3.1-flash-lite` (generator, paid tier) | Writes synthetic chats | Yes: training inputs |
| Anthropic | Haiku 5.5 (generator) | Writes synthetic chats | Yes: training inputs |
| TypeSafe | Jev (auditor) | Flags label errors; flagged chats were relabeled by the teacher or excluded | No: only decides which chats to recheck/exclude |
| OpenAI | Decisions API (auditor) | Same as Jev | No: same as Jev |
| Supersonic Labs | Julia-1 (auditor, open weights) | Same, run on Kaggle | No |

## What the terms say

| Provider | Terms (date) | Clause | Reading for us |
|---|---|---|---|
| **DeepSeek** | [Open Platform Terms](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html) (effective 2026-04-29) | §4.2: outputs assigned to us; permitted uses include "training other models (such as model distillation)" | ✅ Explicitly allowed |
| **Julia-1** | [Model card](https://huggingface.co/SupersonicLabs/Julia-1): Apache 2.0 | No output restrictions | ✅ Allowed |
| **Google** | [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) (updated 2026-04-28) | "You may not use the Services to develop models that compete with the Services (e.g., Gemini API or Google AI Studio)." Google claims no ownership of generated content. Paid tier: prompts/responses not used to improve Google's products | ⚠️ Allowed unless our model "competes with" the Gemini API |
| **Anthropic** | [Commercial Terms](https://www.anthropic.com/legal/commercial-terms) (effective 2025-06-17) | D.4: may not "access the Services to build a competing product or service, including to train competing AI models … except as expressly approved by Anthropic". B: customer owns Outputs | ⚠️ Allowed unless our model is a "competing AI model" |
| **OpenAI** | [Services Agreement](https://cdn.openai.com/osa/openai-services-agreement.pdf) (online v.010126; openai.com/policies/services-agreement returned 403 to our fetcher, so the official PDF was read) | §3.3(e): "except for a Permitted Exception, use Output to develop artificial intelligence models that compete with OpenAI's products and services". Permitted Exception (a): models "primarily intended to categorize, classify, or organize data (e.g., embeddings or classifiers), if these models are not distributed or made commercially available to third parties". §4.1: customer owns Output | ⚠️ **Most important:** the teacher's labels are the training targets. See below |
| **TypeSafe (Jev)** | [Master Customer Agreement](https://typesafe.ai/legal/mca) (updated 2026-09-23) | §2.3(b): may not "use the Services or any Output … to perform model distillation, train a model to imitate the output of the Services, or develop (or to facilitate the development of) a similar or competing product or service" | ⚠️ Fine as an auditor; Jev output must never become training labels |

## Conclusions

1. **DeepSeek and Julia-1: no problem.**
2. **Jev: no problem as long as its output is never a label.** The audit only chose which chats to relabel (the
   relabel came from the teacher) or exclude. Rule from now on: Jev decisions never become training targets, and we
   never train a model to imitate Jev (M7's router comparison is fine; a student trained on Jev's choices is not).
3. **OpenAI, Anthropic, Google: all ban using outputs to build models that *compete* with their own.** Our student is
   a small model that classifies customer messages (intents) and pulls order fields out of a chat for one restaurant
   menu. That is a narrow extractor/classifier, not a general assistant or API, so our reading is that it does not
   compete with GPT, Claude or Gemini. This is a judgement call, not something the terms settle.
4. **The OpenAI risk is the M8 release.** OpenAI's safe-harbour (Permitted Exception (a)) covers classifier-type models
   only **if they are not distributed**. The plan (spec §17) releases LoRA adapters and quantized models on Hugging Face.
   Once released, we rely only on the "does not compete" reading, and OpenAI's labels are the training targets.
   **Julian decides before M6/M8.** Options:
   - (a) Go ahead on the "narrow extractor doesn't compete" reading and say so in the model card (outputs from a
     commercial teacher; trained for one task).
   - (b) Release the code, data recipe, menus and eval sets, but keep the trained weights private (inside the
     Permitted Exception for the intent classifier; the order extractor is arguably "organize data" too).
   - (c) Relabel the training set with a teacher whose terms allow distillation (e.g., DeepSeek, or an open-weights
     model under Apache 2.0) before a public release; costs a relabel of the ~2,350 training chats (estimate first) and a new teacher check on dev.
   - (d) Ask OpenAI support.
5. **Nothing found that forbids M5/M6 as research.** Training and evaluating the student privately is covered by
   point 3's reading and, for the intent part, by OpenAI's Permitted Exception.

Not checked here (check when they are used): student model licenses (Qwen3.5, Qwen3, Gemma 4) for M5/M8, and Kaggle's
terms for private datasets.
