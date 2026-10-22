# Wan (video)

How to brief and fix Alibaba's Wan video models; only 2.2 is downloadable.

Checked 2026-10-21 · Back to [README.md](README.md)

- **Downloadable:**
  - Wan 2.2 (July 2025), Apache-2.0. T2V-A14B and I2V-A14B are mixtures of experts: two 14B experts, 27B total, 14B active per step. The high-noise expert lays out the scene and the low-noise expert refines detail.
  - TI2V-5B is a dense model with a high-compression VAE, 720p at 24 fps. The A14B models give 5 s clips at 480p and 720p.
  - S2V-14B (speech-to-video, 2025-08-26) and Animate-14B (character animation and replacement, 2025-09-19).
  - `verified: yes` (HF card Wan-AI/Wan2.2-T2V-A14B, GitHub Wan-Video/Wan2.2)
- **Newer Wan:** 2.5, 2.6, 2.7 and 3.0 appear to be hosted-only (Alibaba Cloud Model Studio and resellers). Claims that they are Apache-2.0 on Hugging Face are contradicted. Treat them as closed until a Wan-AI repo exists. `verified: no` (secondary)
- **Encoder:** umT5-XXL, credited on the page and run with `--t5_cpu` flags. Reads prose; Chinese and English both work. `verified: yes` for the credit, the rest `no`.
- **CFG and negatives:** the base models sample with CFG above 1, and the reference code ships a default negative prompt (in Chinese), so negatives work. Lightning or distilled LoRAs at CFG 1 disable them. The Animate Diffusers example uses guidance 1.0. `verified: no` for the defaults (not on the pages read); the Animate value is `verified: yes`.
- **Prompt form:** the makers recommend prompt extension (rewriting a short prompt into a rich one with a Qwen model) because it "can effectively enrich the details". Describe subject, motion, camera move and light in sentences. Camera terms from [vocabulary.md](../vocabulary.md) apply. `verified: yes` for the extension advice.
- **References and control:** I2V takes a first frame. Animate replaces or drives a character from a reference video. Depth and pose control come through community VACE and Fun builds. `verified: no`
- **Defaults to steer against:** slow-motion drift, over-smooth faces, warping hands in fast motion. Fix with explicit speed words, shorter actions, and a first-frame image.
