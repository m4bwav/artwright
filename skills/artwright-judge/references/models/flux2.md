# FLUX.2 (dev, klein)

What to prompt and which fix channels work on Black Forest Labs' FLUX.2 open models.

Checked 2026-10-21 · Back to [README.md](README.md)

- **Models:**
  - [dev]: a 32B rectified-flow transformer. The example uses 50 steps (28 is "a good trade-off") at guidance 4, which is distilled guidance and not true CFG.
  - [klein] 9B and 4B: step-distilled to 4 steps at guidance 1.0. klein 9B uses an 8B Qwen3 text embedder.
  - `verified: yes` (HF cards FLUX.2-dev, FLUX.2-klein-9B, FLUX.2-klein-4B)
- **Encoder of dev:** not named on the card (the example calls a remote encoder). `verified: no`
- **Negatives:** "FLUX.2 does not support negative prompts". Describe the positive ("sharp focus throughout", not "no blur"). `verified: yes` (docs.bfl.ai FLUX.2 prompting guide)
- **Word order:** "Main subject → Key action → Critical style → Essential context → Secondary details". Earlier words weigh more. 30-80 words is usually ideal, 80+ for complex scenes. Structured JSON (scene, subjects, style, color_palette, lighting, camera) works as well as prose. `verified: yes` (BFL guide)
- **Colour and photo terms:** write hex codes with the word "color" or "hex" and tie each to a named object. For photorealism, name the camera, lens and film stock ("shot on Kodak Portra 400, natural grain") or an era ("2000s digicam"), not "professional photo". `verified: yes`
- **References:** native multi-reference editing. Give each image a role ("subject from image 1, style from image 2"). Up to 8 references at 1 MP output, per the guide (stated for the [pro] API; local limits depend on VRAM). `verified: yes` for roles; the local limit is `verified: no`.
- **Control:** reference images replace much IP-Adapter use. For depth and pose ControlNets, check what ComfyUI currently ships. `verified: no`
- **Defaults to steer against:** glossy commercial polish, generic "professional" light, over-clean surfaces. Fix with named light, imperfection and film stock. `verified: no`
- **Licence:** dev and klein 9B use the FLUX Non-Commercial License. klein 4B is Apache-2.0 ("available for commercial use"). `verified: yes`
