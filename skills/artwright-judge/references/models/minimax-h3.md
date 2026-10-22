# MiniMax H3 (video)

How to brief and fix MiniMax H3, the open-weights video-with-audio model.

Checked 2026-10-21 · Back to [README.md](README.md)

- **Model:**
  - Weights released 2026-08-03: a 33B dense single-stream Omni Transformer, BF16.
  - Output runs 4-15 s at 24 fps, with 32 kHz stereo audio generated in the same pass. The short side is 768 px by default; 2K needs H3-Regenerate-2K, which is not open-sourced.
  - `verified: yes` (HF card MiniMaxAI/MiniMax-H3)
- **Encoder:** H3-Encoder uses Qwen3-VL-32B, hidden states from layer 50. In bf16 it is large (about 51 GB in the Comfy repack; 4-bit and int8 variants exist). `verified: yes` for the encoder; the repack size is `verified: no`.
- **Modes:**
  - FL2VA: text-only, first frame, last frame, or first and last frames.
  - Ref2VA: up to 9 images, 3 video clips and 3 audio clips (each 2-15 s, 15 s in total), 12 files at most.
  - `verified: yes`
- **CFG and negatives:** the released checkpoints are "CFG-distilled", so a negative-prompt field is unlikely to do anything. In-prompt negation is "unusually effective" ("No soft dissolves or fluid morphs", "Do not introduce Chinese text, garbled characters, or misspellings"). `verified: yes` for CFG-distilled (card); the negation advice is `verified: no` (fal guide, 2026-07-31).
- **Prompt form:** up to about 7,000 characters. Write a timed shot list. Give every reference an explicit job ("Image 1: the woman's face and coat only"). Use first and last frames only when the image literally is that frame. Describe transitions as physical events, not effect names. Name what must stay fixed. Direct the sound in its own sentences. `verified: no` (fal guide); the official writing guides ship in the repo (VIDEO_PROMPT_WRITING_GUIDE_base_en.md, _ref_en.md) and should be read before relying on this.
- **Licence:** "MiniMax H3 Community License Agreement". The card links an application form "only for USA/EU/UK/South Korea", and secondary sources say local deployment is excluded in those territories without separate approval. Read the licence before using it there. `verified: yes` for the name and the form, `no` for the scope.
- **Defaults to steer against:** morphing transitions, drifting faces and sets between shots, garbled signage. Fix these with reference roles and in-prompt negation.
