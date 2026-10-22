# Closed models (verify first)

Thin profiles for hosted image and video models. Most facts here come from secondary sources, so check the vendor's current docs before relying on any of them.

Checked 2026-10-21 · Back to [README.md](README.md)

Shared rules for all hosted models:

- Prompt in natural sentences.
- When editing, say what changes and what stays.
- Never use a living artist's name; most vendors refuse it anyway.

## GPT Image (OpenAI)

- **Model:** `gpt-image-2` is the "latest" GPT Image model, through the Image API (generate and edit) or as a tool in the Responses API. It may need organisation verification. `verified: yes` (developers.openai.com image-generation guide). Reported release 2026-04-21: `verified: no`.
- **Negatives:** no negative field. State positives. `verified: no`
- **Style policy:** refuses "the style of a living artist" (since March 2025) and allows studio styles. Describe traits instead. `verified: no` (press)

## Gemini image (Nano Banana family)

- **Models:** Nano Banana (Gemini 2.5 Flash Image), Nano Banana 2, and Nano Banana Pro (Gemini 3 Pro Image). Model IDs conflict across sources (`gemini-3-pro-image` or `-preview`). `verified: no`
- **Prompting:** Google's "golden rule" is to describe the scene in sentences, not keyword stacks. Strong at in-image text and conversational edits. Up to 14 reference images is reported for Pro. `verified: no` (secondary)
- **Imagen:** older Imagen generations had a negative prompt field; whether current Imagen models honour it is unconfirmed. `verified: no`

## Midjourney

- **Version:** V8.x (V8.1 April 2026; V8.2 reported as the default from 2026-07-24). The official docs refused automated reads. `verified: no`
- **Parameters:** `--no` (negative) is kept in V8.1. `--sref`, moodboards, `--stylize`, `--chaos` and personalisation are reported. `--oref` (omni reference) is reported unsupported on V8.1; use V7 for it. `verified: no`
- **Character:** strong default aesthetic (colour and mood). Push against it with `--style raw` and low `--stylize` when the brief wants plain. `verified: no`

## Veo 3.1 (Google)

- **Prompt elements:** subject, action, scene, camera angle, camera movement, lens and optics, style, temporal elements, audio, cinematic terms. Audio goes in separate sentences, with dialogue attributed to a described character. `verified: yes` (Vertex AI Veo prompt guide, updated 2026-10-21)
- **Negatives:** a negative prompt field exists. List the unwanted things ("wall, frame"), never "no" or "don't". `verified: yes`

## Sora 2 (OpenAI)

- **Status:** the app was reported shut down on 2026-04-26 and the API on 2026-09-24. Do not target it without checking OpenAI's deprecations page. `verified: no`

## Others to profile when used

Seedream 5.0 Pro (ByteDance), Kling, Runway. Not checked this pass.
