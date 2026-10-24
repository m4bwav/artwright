# Changelog: artwright

Every change to [README.md](README.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

## Releases

- 0.4.0 · not tagged yet: C-20261023-1, render-then-paint gate (`geomgate`), painted-sprite style check (`sprite`),
  transparent pixels left out of `stats` and the measures.
- 0.3.0 · 2026-10-23, the first tagged release (owner's go-ahead 2026-10-23): C-20261022-7 and -8, craft light logic and composition rows, AI-look rows
  17-29, rubric 2, rank cycles, winner must fit the brief, cache sampling key, label side order.
- 0.2.0 · never tagged, shipped inside 0.3.0: C-20261022-5 and -6, light, colour and composition measures (`light`, `gamut`, `accents`,
  `depth`, `comp`), new `stats` fields and degrade kinds.
- 0.1.1 · never tagged (planned for 8ee7740 on 2026-10-22), shipped inside 0.3.0: C-20261021-1 to C-20261022-4
  (0.1.0 was installed locally, never tagged).

## Changes

### C-20261023-1 · 2026-10-23 · geomgate and sprite commands; transparent pixels left out of stats and measures (0.4.0)
- because: user request (a render-then-paint game sprite job, gates proven on a sawmill's renders and paintings); L-008, L-009, L-010
- files: skills/artwright/scripts/aw_geom.py (new: `geomgate` ring rim by profile cross-correlation, spokes, region anomalies at game size, contact, edges as information; `sprite` style fit against references; standard library ports of numpy and scipy prototypes), skills/artwright/scripts/aw.py (`alpha_mask`; `stats` reads opaque pixels for value and colour and reports `alpha`; parsers; version 0.4.0), skills/artwright/scripts/aw_measure.py (`light`, `gamut`, `depth` measure opaque pixels; `accents` and `comp` report `alpha`), skills/artwright/references/sprite-json.md (new: the render folder contract), skills/artwright/references/cli.md (rows; flags section), skills/artwright/SKILL.md (Image handling: transparency, the geometry gate), skills/artwright-judge/SKILL.md (A batch step 1: rank only candidates that pass geomgate), skills/artwright-pixel/SKILL.md (Painted sprites are not pixel art), tests/test_aw.py (GeomGate, Sprite, Alpha), scripts/budget.py and AGENTS.md (aw_geom.py under 100 KB), README.md (examples), .claude-plugin/plugin.json (0.4.0)
- A painting made over a 3D render can now be checked against the render's shapes before it is judged, and a painted sprite against the set it joins. On the sawmill set the port reproduces the prototype's numbers. Descriptions are unchanged, so triggers are unchanged; the evals were not re-run.

### C-20261022-8 · 2026-10-22 · Judge: rubric 2, winner must fit, rank cycles, cache sampling key, label side order (0.3.0)
- because: user request (book-learnings build, track 6: ideas after Huyen, *AI Engineering*); R-20261022-3; ai-docs/decisions/2026-10-22-books-track6.md F3-F7; T-20261022-7
- files: skills/artwright-judge/references/rubric.md (version 2: brief-fit look words, ordered composition checks, light logic criterion, two light directions as an integrity failure, winner check, cycles abstain), skills/artwright-judge/SKILL.md (batch steps 5-6, brief-fit step 1, measures before light and composition fixes, cache sampling flags), skills/artwright-judge/references/verdict-contract.md (example rubric 2), skills/artwright-curate/SKILL.md (labels shown in random order, `--shown-first`), skills/artwright/scripts/aw.py (`rank` cycles, `cycle_count`, `top_in_cycle`; `cache` `--temperature`, `--seed`, `--shown-first`, rubric default 2; `labels_first_shown_share`; version 0.3.0), skills/artwright/references/cli.md (rank and cache rows), tests/test_aw.py (cycle, no cycle, label order, sampling key), evals (action-rank-cycle, action-winner-fit, judged fixtures), .claude-plugin/plugin.json (0.3.0)
- A batch winner is now checked against the brief before it is reported, a three-way loop among the leaders makes the win close, and the cache keeps verdicts from different sampling settings apart.

### C-20261022-7 · 2026-10-22 · Craft: light logic, atmosphere, composition rows, eye path rewritten; AI-look rows 17-29
- because: user request (book-learnings build, track 6: ideas after Gurney, Mateu-Mestre, Roberts, Garvey-Williams and Chen); R-20261022-1, R-20261022-2; ai-docs/decisions/2026-10-22-books-track6.md F1, F2
- files: skills/artwright/references/craft.md (Composition: where the eye goes, armature, edge hierarchy, frame edges, way in and back, hot spots, intervals and clusters, mergers, horizon and camera height, ground contact, silhouette, shape grouping, depth devices, open or closed, questions for a vision model; Value: posterise test, gradients; new Light logic and Atmosphere and distance sections; Colour: relative temperature, gamut, accent, too much colour, no flat colour), skills/artwright-judge/references/ai-look.md (measure first; row 7 rim rules; rows 17-29)
- The eye-path row said lines carry the eye; Gurney's eye-tracking pages say the eye jumps to faces and figures, so the row now says where a viewer looks first. Each new row cites the `comp`, `light` or `depth` flag that points at it.

### C-20261022-6 · 2026-10-22 · Hub description names light and composition
- because: T-20261022-6, L-002
- files: skills/artwright/SKILL.md (description: "an image's light, composition or main colours"; "claims tie to regions" cut for the budget; Image handling: run the measures before answering)
- The new action case asked "is the light consistent" and half the runs answered by eye without loading the hub. Naming the job in the description fixed it (6/6); decoys and triggers re-run clean.

### C-20261022-5 · 2026-10-22 · Light, colour and composition measures: light, gamut, accents, depth, comp
- because: user request (book-learnings build, track 5: ideas after Gurney, Mateu-Mestre and Roberts); L-004, L-005, L-006; ai-docs/decisions/2026-10-22-books-track5.md
- files: skills/artwright/scripts/aw_measure.py (new: the five commands and their helpers), skills/artwright/scripts/aw.py (stats: middle share, bimodality, clipping, highlight tint, chroma per cell, b* mean and spread; degrade kinds warm-shadows, glow-shadows, uniform-sat, midgrey, haze-off, hotspot, tangent; parsers; version 0.2.0), skills/artwright/references/cli.md (rows; Light, colour and composition flags), skills/artwright/references/evidence.md (stats edge is 256 px), skills/artwright/SKILL.md (Image handling; Critique step 2), tests/test_aw.py (Measures, test_stats_value_structure), evals (action-light, street.png fixture), scripts/budget.py and AGENTS.md (both scripts under 100 KB), .claude-plugin/plugin.json (0.2.0)
- Five commands describe light logic, gamut shape, accents, atmospheric recession and composition (value masses, focal margin, border pull, tangents, horizon, hot spots, figure and ground). Their flags are pointers with thresholds set from flag rates on real images, not grades.

### C-20261022-4 · 2026-10-22 · 0.1.1: exit codes in the README and AGENTS.md
- because: the wiki pass's mismatch list (ai-docs/notes/2026-10-22-github-wiki.md, item 1)
- files: README.md (aw.py), AGENTS.md (rules), .claude-plugin/plugin.json and skills/artwright/scripts/aw.py (version 0.1.1)
- "Every command prints one JSON object" now says what a failure, a usage error and `--version` print.

### C-20261022-3 · 2026-10-22 · Banner, wiki, doc fixes, calibration records
- because: user request (Step 3 launch set); the wiki pass's mismatch list (ai-docs/notes/2026-10-22-github-wiki.md)
- files: README.md (banner, credit), .github/images/ (workflow, prompt, four seeds, contact sheet, banner-verdict.json), skills/artwright/references/cli.md (exit 2 on usage errors, `--version`, `sheet --cell 384`, `pixel --tol 24`), skills/artwright-judge/references/verdict-contract.md (`close_to_next` is null on the last row), ai-docs (rulings C1-C8, wiki note), scripts/eval-wsl.sh (refuses an empty case glob, L-003)
- The banner was picked by artwright-judge from four Z-Image Turbo seeds. The wiki (10 pages) is live; its source note and verification script are in ai-docs/notes.

### C-20261022-2 · 2026-10-22 · Paid-tier fixes: taste calls, regions, AI-made, prompt rewrites; graders read only the reply
- because: T-20261022-1, T-20261022-3, T-20261022-4
- files: skills/artwright/SKILL.md (description: "is this AI-made"; guards: open with "pixels cannot tell", a file name is not provenance, never ask a living artist's name), skills/artwright-judge/SKILL.md (description: prompt rewrites into a style or artist, shorter pair wording; "Why two at a time": agreeing orders are not a wide call, taste between two intact works is said to be close; "Hand back": each reason tied to its region), skills/artwright-curate/SKILL.md (description trimmed one example for the budget), evals (graders for brief-fit, ming-price, pairwise-orders, golden-ratio, ai-generated; `files` on image cases for `worth --ab`; scaffolds fetch museum images), evals/fixtures/make_fixtures.py
- Descriptions at ~596 of 600 tokens; triggers 8/8 and decoys re-run on the new text.

### C-20261022-1 · 2026-10-22 · A tie in both orders is a tie
- because: the calibration run (rulings C5); found again by the wiki pass
- files: skills/artwright/scripts/aw.py (`resolve`), tests/test_aw.py (test_tie_both_orders)
- Both orders saying tie returned `decided` with no winner: `rank` counted it as a win and `cache agreement` crashed.

### C-20261021-3 · 2026-10-21 · Descriptions catch colours and contact sheets and name brandwright and sitewright; shell evals scaffolded
- because: T-20261021-2, T-20261021-3, L-001, L-002
- files: skills/artwright/SKILL.md (description; Image handling), skills/artwright-judge/SKILL.md (description), skills/artwright-curate/SKILL.md (description, shortened for the budget), evals/cases/action-*/ (case.yaml, fixture.sh, graders), evals/fixtures/make_fixtures.py (--emit-scaffold), tests/check_skills.py (.sh files checked; base64 fixtures exempt from the token check)
- The hub now names colour questions and contact sheets and says to answer them from aw.py; the hub and judge name the siblings that own brand palettes and website direction; the action cases unpack their fixtures in the run's workspace.

### C-20261021-2 · 2026-10-21 · Step 2 build: four skills, aw.py, knowledge files, tests, evals, CI
- because: user request (kickoff Step 2); R-20261021-1 to -30; ai-docs/decisions/2026-10-21-step2-build.md
- files: skills/artwright (SKILL.md, scripts/aw.py, references/), skills/artwright-judge, skills/artwright-pixel, skills/artwright-curate, tests/test_aw.py, tests/check_skills.py, scripts/budget.py, evals/, .github/workflows/tests.yml, README.md, AGENTS.md
- The hub (critique, style and movement, theory, facts), the judge (pairwise in both orders, Bradley-Terry, brief fit, prompt fixes, the verdict contract), pixel checks and the curator, on a standard-library aw.py with Pillow optional. Knowledge rows carry sources, dates and verified flags.

### C-20261021-1 · 2026-10-21 · Created as an evergreen unit
- because: user request
- files: README.md, RESEARCH.md, LEARNINGS.md, evergreen.json, TESTS.md, evals/evals.json
- Initial version. Tier `moderate`, interval 60 days (the synthesis). See R-20261021-1 for the research basis.
