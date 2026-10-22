# Z-Image Turbo and Z-Image base

What to prompt and which fix channels work on Tongyi-MAI's Z-Image family.

Checked 2026-10-21 · Back to [README.md](README.md)

- **Model:** a 6B single-stream DiT. Turbo is distilled to 8 function evaluations (9 steps in the example code). The base model takes 28-50 steps. Z-Image-Edit and Omni-Base were still "to be released" on the card. `verified: yes` (HF cards Tongyi-MAI/Z-Image-Turbo and Tongyi-MAI/Z-Image)
- **Encoder:** Qwen3-4B (ComfyUI file `qwen_3_4b.safetensors`). Reads long prose, with bilingual English and Chinese text rendering. `verified: yes` (docs.comfy.org Z-Image tutorial)
- **CFG and negatives:**
  - Turbo: "Guidance should be 0 for the Turbo models", so negative prompts do nothing. Rewrite them as positives.
  - Base: full CFG (3.0-5.0, example 4) and "high fidelity to negative prompting". Negatives work there.
  - `verified: yes` (both cards)
- **Word order:** subject first, then action, setting, light, medium and camera. Long detailed descriptions are the card's own examples. `verified: no` (no vendor ordering rule; general LLM-encoder practice)
- **Resolution:** 1024x1024 in the Turbo example; base takes 512-2048 total area at any aspect. `verified: yes`
- **References and control:** Z-Image-Turbo-Fun-Controlnet-Union (canny, HED, depth, pose, MLSD) as a ComfyUI model patch. The base is "a good base for LoRA training". Whether LoRA and ControlNet combine cleanly is unconfirmed. `verified: yes` for the union patch, `no` for the LoRA combination.
- **Defaults to steer against:** smooth plastic skin, centred hero framing, bright even "clean" light, glossy saturated colour. Fix on Turbo with concrete positives (pores, a named lens, overcast or raking light, off-centre placement). On base, also add negatives. `verified: no` (practitioner reports; log evidence)
- **Licence:** Apache-2.0. `verified: yes`
- **Model switch:** use base when a fault needs negatives or more steps; use Turbo for fast iteration.
