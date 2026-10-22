# artwright log

Append-only, newest last.

## 2026-10-21: kickoff prompt written

Mark asked for a prompt to start the ultimate evergreen art plugin: artistic vision and analysis of every kind
(aesthetic comparisons, style and movement detection, art-history and market facts, theory), drawing to ceramics
to pixel and 3D digital art, used mostly by agent workflows and by sibling plugins (cinewright, polywright,
comfyui-gen, historywright). It must study art and its theory, how AI makes and judges art, and efficiency
scripts. Public repository with banner and the usual files.

- Name `artwright` is a small ruling (m4bwav/artwright did not exist on 2026-10-21); Step 1 may propose another.
- Step 1 = evergreen creation pass (passes A to H, about 25 searches each) plus verified gold answers, then stop
  for Mark. No repository until he answers the forks.
- Kickoff: `ai-docs/next-session-prompt.md`.

## 2026-10-21: Step 1 creation pass done; stopped for Mark

- Eight research passes (A–H) ran in parallel, each capped at about 25 searches; five hit a session usage limit
  and were resumed. Cost: searches 125 · fetches 218 · tool calls 429. Reports in
  `research/2026-10-21-creation-pass/`, synthesis `research/2026-10-21-creation-pass.md`, 22 `R-` entries in
  `../RESEARCH.md`.
- Gold answers verified from sources: Ming vase record (2011 Yongle meiping, HK$168.66m, medium confidence; chicken
  cup HK$281.24m for any Ming porcelain), oldest painting (the record changed in 2026: Muna Island stencil, at
  least 67,800 years; figurative Leang Karampuang, at least 51,200), Salvator Mundi $450.3m. Cleveland CC0 records
  for the cubism cases re-read by hand.
- Proposed: four skills (hub, judge, pixel, curate), stdlib `aw.py` with optional Pillow, knowledge files with a
  size budget, pairwise-both-orders judging, two-tier evals. Rulings R1–R8 in `decisions/2026-10-21-step1-rulings.md`.
- Four forks wait for Mark (synthesis section 8): no local aesthetic model in v1; he labels 30–50 pairs; one-line
  hand-offs in comfyui-gen and polywright; living-artist names rewritten to traits.
- No repository created, as the kickoff asked.

## 2026-10-21: Mark answered the four forks

All as recommended: no local aesthetic model in v1, he labels 30–50 pairs in Step 3, one-line hand-offs in
comfyui-gen and polywright in Step 3, living-artist names rewritten into traits. Recorded in
`decisions/2026-10-21-forks-mark.md`; next-session-prompt.md and HANDOFF.md updated so Step 2 can start.
