# Mark's answers on the four Step 1 forks (2026-10-21)

The forks are in section 8 of [../research/2026-10-21-creation-pass.md](../research/2026-10-21-creation-pass.md).
Mark took the recommendation on all four.

1. **No local aesthetic-scoring model, for now.** v1 ships without one. GPU reward models (HPSv3, UnifiedReward)
   are named only as pointers. The question can be reopened later.
2. **He will label 30–50 image pairs in Step 3.** One pair at a time ("which of these two?"), on a page he opens
   once, about 15 minutes. The labels go into the private calibration set under `ARTWRIGHT_HOME`.
3. **One-line hand-offs in comfyui-gen and polywright in Step 3**, each as its own pull request in that sibling's
   repository ("after a batch, call artwright-judge"). cinewright-qc keeps judging video takes.
4. **Living-artist names are rewritten into traits, not refused.** artwright replaces the name with medium, palette,
   line, subject and era, and says so in one line. Public-domain masters, movements and studio genres may be named.
   This confirms ruling R7.
