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

## 2026-10-21: Step 2 built, tested, published and installed

- Repository m4bwav/artwright created public (scaffold commit on main, private vulnerability reporting on, topics,
  `needs-review` label). PR #1 (the build) and PR #2 (cheap eval tier fixes) merged after CI passed on Ubuntu,
  macOS and Windows with Python 3.9 and 3.14. PR #3 (release workflow) left open for Mark: publish workflow.
- Built: four skills (hub, judge, pixel, curate), `aw.py` (67 KB, stdlib, Pillow optional; 14 commands),
  knowledge files (about 154 KB; 123 movement rows, 97 verified), 34 offline unit tests plus a network test of 7
  pinned Cleveland CC0 fixtures, `check_skills.py`, `budget.py`, 32 eval cases (14 cheap, 18 paid).
- Five knowledge passes ran as parallel agents; findings logged as R-20261021-23 to -30. Verified: the
  Hasler–Süsstrunk formula and Table 2 anchors, the Aesthetics Toolbox metric names, the Lospec API and terms
  (only PICO-8 is CC0, so only it ships), model licences (FLUX.2 klein 9B is non-commercial), the law table.
- CI caught `Path.write_text(newline=)` on Python 3.9 (fixed with `open()`).
- Evals, cheap tier, final text: triggers 8/8, decoys 3/3, actions 3/3 (42/42 runs). On the way: shell cases need
  WSL2, a scaffold and `tool: Bash` (L-001); palette and sheet requests never fired a skill until the hub named
  them, and naming colours pulled brand and website decoys in until their owners were named (L-002). Spend $15.76.
- historywright PR #19 merged (by a delegated agent): 10 art sources (Getty Provenance CSV, Museo Egizio, eight
  link-out price databases) and the AIC fix (its API returned 403 without `AIC-User-Agent`).
- Installed as artwright@mark-local (0.1.0 at 2a9c1b3); evergreen unit registered (moderate, 60 days, due
  2026-12-20); ai-docs registered with everlast (mode repo, sync pr); ARTWRIGHT_HOME set to the vault sidecar's
  `studio/`.
- Rulings B1–B10 in `decisions/2026-10-21-step2-build.md`.
## [2026-10-21] index | rebuilt (7 entries)

## 2026-10-22: Mark's answers to the Step 2 questions

Mark merged PR #3 (release workflow). On the MiniMax H3 licence territory question he is in the USA and accepts
local use, so it is closed for him. HANDOFF and next-session-prompt.md updated; tagging still waits for his go.

## 2026-10-22: Step 3 session: paid evals tuned, calibration page live, hand-offs, banner, wiki

- Paid tier run for the first time (T-20261022-1 to -4): first pass 11/18 cases; after three tune iterations
  28 of 32 cases pass every run, four pass some (pairwise-orders 2/3, ai-generated 1/3, brief-fit 2/3,
  tie-pair 2/3). Triggers 8/8 and decoys 35/36 on the new descriptions (596 of 600 tokens). Fixes: the judge
  says a taste call between two intact works is close, ties each reason to a region; the hub opens AI-made
  questions with "pixels cannot tell", a file name is not provenance; descriptions name AI-made questions and
  prompt rewrites into a style; five graders reworded to what a last-message judge can see.
- Eval spend $33.99 (about $14 of it a mistaken loop that ran the whole suite four times, L-003). The A/B
  (`worth --ab`, about $10) was not run: it would pass the $40 cap. Waits for the owner.
- Calibration: 40 pairs built (16 degraded CC0, 3 pixel, 16 of the owner's own seed pairs, 5 ties) in
  ARTWRIGHT_HOME/calibration/set-2026-10-22; the judge's both-orders agreement on them is 0.775 (target 0.8; most
  flips on the close seed pairs). Labelling page https://claude.ai/artifact/TFZxKLEmSr41WXP1Gszs23 (private,
  picks in its `picks` collection); the owner had labelled 9 when the session ended. `import_picks.py` in the
  calibration folder writes the labels and prints the agreement. Relative image paths did not render in the
  artifact viewer; images are now embedded as data URIs.
- Bug fixed: a tie in both orders resolved as `decided` with no winner (rank counted it, agreement crashed).
- Hand-off PRs open for the owner: m4bwav/comfyui-gen#82, m4bwav/polywright#24.
- Banner: four Z-Image Turbo seeds on both hosts, picked by artwright-judge (seed 202, 3-0 in both orders).
- Wiki: 10 pages live at https://github.com/m4bwav/artwright/wiki (by an agent with wikiwright; note in
  notes/2026-10-22-github-wiki.md). It lists the double-tie bug as known until this PR merges.
- Rulings C1-C8 in decisions/2026-10-22-step3-rulings.md.
## [2026-10-22] index | rebuilt (9 entries)

## 2026-10-22: Step 4 session: calibration result, A/B, wiki fix, release PR

- The owner labelled all 40 calibration pairs. Judge accuracy against his picks 0.825 (target 0.8, passes);
  both-orders agreement 0.775 (does not). By kind, judge vs owner: degraded 0.88, pixel 1.00, his seed pairs 0.75,
  ties 0.80. Five of seven misses are the judge's own ties; he preferred the saturated image on 3 of 4 saturate
  pairs (a taste note in the private studio's taste.md, no public rubric change). Ruling D1.
- A/B (T-20261022-5, $10.25; day total $44.24): with 17/20, without 12/20, +25 points inside a 27-point margin;
  the tool says CUT, the paired 5-0 says keep (D5). action-palette's with arm tried to edit the repo's
  LEARNINGS.md from its run folder (open finding).
- Wiki: the both-orders tie known issue replaced by the fixed behaviour (Errors-and-Edge-Cases,
  How-Images-Are-Judged); live check 10 pages, 0 failures.
- Release: PR #7 (0.1.1 bump, CHANGELOG release line, exit codes in README and AGENTS.md) passed CI; the merge
  was refused by the session's permission classifier, so it is assigned to the owner (D4). No tag yet.
## [2026-10-22] index | rebuilt (10 entries)

## 2026-10-22: Books track 5: light, colour and composition measures (0.2.0, untagged)

- Built `light`, `gamut`, `accents`, `depth` and `comp` in a new `aw_measure.py`, plus `stats` fields (middle
  share, bimodality, clipping, highlight tint, chroma per cell, b* mean and spread) and seven degrade kinds. Rulings
  E1-E6 in decisions/2026-10-22-books-track5.md.
- Calibrated flag rates on 48 AI stills and 7 museum works; five thresholds from the notes changed (L-004). The
  museum mat trim (L-006) and two degrade definitions (L-005) were found only on real images.
- Skipped: armature and vanishing point, intervals, flat fills, `--mask` (built as `--box`). Reasons in E4.
- Tests 35 to 47, all pass (one network test skipped offline); eval action-light added (results in TESTS.md).
## [2026-10-22] index | rebuilt (11 entries)
