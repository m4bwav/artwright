# Generation model profiles

One short profile per generation model, so the judge picks the fix channel and the prompt form that the target model actually honours.

Checked 2026-10-21 · Back to [SKILL.md](../../SKILL.md)

**Model facts are volatile.** Versions, licences, CFG defaults and reference limits change every few months. Recheck each profile every 60-90 days, and before any claim that decides money or licensing. Each claim group carries `verified: yes` (read on the maker's model card or docs on the date shown) or `verified: no` (secondary source or prior knowledge).

| Profile | Kind | Negatives honoured | Licence (check) |
| --- | --- | --- | --- |
| [z-image-turbo.md](z-image-turbo.md) | image, local (Turbo and base) | Turbo no (guidance 0); base yes | Apache-2.0 |
| [flux2.md](flux2.md) | image, local (dev, klein) | no | dev and klein 9B non-commercial; klein 4B Apache-2.0 |
| [qwen-image.md](qwen-image.md) | image, local (original, 2.1) | original yes (true CFG) | original Apache-2.0; 2.1 Qwen Research |
| [minimax-h3.md](minimax-h3.md) | video plus audio, local | in-prompt negation only | MiniMax H3 Community, territory limits |
| [wan.md](wan.md) | video, local (2.2) | yes (CFG > 1) | Apache-2.0 (2.2) |
| [closed-models.md](closed-models.md) | hosted: GPT Image, Gemini image, Midjourney, Veo, Sora | varies | terms of service |

Rules that hold across all of them:

- A negative prompt works only where real CFG is above 1. On guidance-distilled or CFG-1 models, rewrite each negative as a positive ("sharp focus throughout", not "no blur").
- Modern models read prose through LLM encoders. Write sentences, front-load the subject, and drop CLIP-era boosters (see the dead magic words in [vocabulary.md](../vocabulary.md)).
- When composition or pose is wrong, the fix is often a control image (depth, pose, canny) or a reference image, not more words.
