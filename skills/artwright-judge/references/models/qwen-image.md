# Qwen-Image (original and 2.1)

What to prompt and which fix channels work on Alibaba Qwen's image models.

Checked 2026-10-21 · Back to [README.md](README.md)

- **Qwen-Image (original, 2025-08-04):**
  - A 20B model, Apache-2.0.
  - True CFG: the example uses `true_cfg_scale=4.0` with `negative_prompt=" "` (a space; "use an empty string if there's no concept to remove") at 50 steps.
  - The card appends a "positive magic" suffix: `", Ultra HD, 4K, cinematic composition."`
  - Native sizes include 1328x1328, 1664x928 and 928x1664.
  - `verified: yes` (HF card Qwen/Qwen-Image)
- **Encoder:** Qwen2.5-VL-7B (ComfyUI file `qwen_2.5_vl_7b_fp8_scaled.safetensors`). Strong at in-image text, Chinese and English. `verified: yes` (docs.comfy.org Qwen-Image tutorial)
- **Negatives:** these work on the original at CFG > 1. On the community distilled build and on Lightning LoRAs, the recommended CFG is 1.0, so negatives do nothing there. `verified: yes` (Comfy docs)
- **Qwen-Image 2.1:**
  - A 7B single-stream DiT, 40 steps in the examples. Sizes run up to 2048x2048 and 2752x1536. It has an RGBA transparent mode (prompt opens "This is an RGBA image with transparency.").
  - The card's examples show no CFG or negative-prompt settings.
  - `verified: yes` (HF card Qwen/Qwen-Image-2.1). A 2.1 Turbo at 8 steps and CFG 1 is reported by secondary sources: `verified: no`.
- **Licence of 2.1:** "Qwen Research License Agreement", which secondary sources read as non-commercial only. Check before commercial use. `verified: yes` for the name, `no` for the scope.
- **Control:** InstantX Union ControlNet (canny, soft edge, depth, pose), DiffSynth canny, depth and inpaint patches, and a DiffSynth union LoRA. Qwen-Image-Edit models handle reference-based edits. `verified: yes` (Comfy docs) for the original only.
- **Word order:** describe in full sentences, subject first. Quote any text that must appear. `verified: no`
- **Defaults to steer against:** saturated "cinematic" grade (the positive magic pulls toward it), centred composition. Drop the suffix when the brief wants a rough or flat look. `verified: no`
