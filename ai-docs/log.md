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
- Tests 35 to 47, all pass (one network test skipped offline). Eval action-light 6/6 once the hub description
  named light and composition (T-20261022-6, $6.39); decoys 9/9, triggers 24/24.
## [2026-10-22] index | rebuilt (11 entries)

## 2026-10-22: Books track 6: craft text, AI-look tells, rubric 2, judge changes (0.3.0, untagged)

- craft.md: light logic and atmosphere sections, eighteen composition rows, the eye-path row rewritten after
  Gurney's eye-tracking pages, colour rows (relative temperature, gamut, accent, too much colour), questions for a
  vision model. Each row cites its book and page and the `light`, `depth` or `comp` flag that points at it.
- ai-look.md rows 17-29 with their flags; rim-light rules on row 7.
- Rubric 2: look words expand into traits, ordered composition checks, light logic as its own criterion, two light
  directions as an integrity failure, the batch winner must pass brief fit, cycles abstain.
- aw.py: `rank` lists three-way loops and marks their span close (`top_in_cycle`); `cache` keys on temperature
  and seed when given; `cache label --shown-first` and `labels_first_shown_share`. Tests 48-51.
- Real data: the calibration set is 40 disjoint pairs (no triads, 0 cycles); agreement unchanged (0.775, 0.825);
  the owner picked the first-shown image 15 of 31 times (0.48).
- Evals: action-rank-cycle 3/3, action-winner-fit 5/6 (T-20261022-7). Rulings F1-F8 in
  decisions/2026-10-22-books-track6.md; skipped items in F8.
## [2026-10-22] index | rebuilt (12 entries)
## [2026-10-23] release | 0.3.0, the first tag
- Owner's go-ahead (book-learnings resume, 2026-10-23) covered tagging 0.3.0. 0.1.1 and 0.2.0 were never tagged; they ship inside 0.3.0 and the CHANGELOG Releases list says so. Tag `v0.3.0` on the merge of this change; the release workflow packs the skills.
## [2026-10-23] wiki | updated for 0.3.0 (wiki commit 2e40f7f)
- Pages added: Versions-and-Upgrading, Light-Colour-and-Composition. Updated: Home, Getting-Started, Skills, Commands, How-Images-Are-Judged (cycles, rubric 2, calibration fields), Verdict-Contract, Errors-and-Edge-Cases (tie known issue moved to Versions; new measure errors; aw.py without aw_measure.py), FAQ, Development, sidebar, footer (0.3.0 at 2c13c08). `wikiwright.py live`: 12 pages, 0 failures, 43 anchor links, 0 broken.
- Verified against a fresh clone of v0.3.0 (aw.py and aw_measure.py match the release zip by SHA-256): Linux (WSL2) Python 3.14.4 + Pillow 13.0.0 (shown), Linux with Pillow hidden, Windows Python 3.9.25 without Pillow. 0.1.0 (997f5b9) replayed with the 2026-10-22 script for the Versions page. outputs 80 checked, 0 missing; snippets 0 missing; check 0 errors; prose checker 0 strong.
- Found: the 2026-10-22 verify script copies aw.py only, so on 0.2.0+ every command fails (ModuleNotFoundError: aw_measure); it must copy aw_measure.py too. Its saved copy had been edited after its output was saved (the broken-verdict path and the home mask became `<home>`, the pages show `/home/you`), so it no longer reproduced its own output. The extended script (new measure, cycle, cache and error cases) and its output were kept outside the repository for this run; commit them as `ai-docs/notes/2026-10-23-wiki-verify.*` and update the wiki note with them before the next wiki update.
## [2026-10-23] build | 0.4.0: geomgate, sprite, alpha-aware stats (C-20261023-1)
- Ported two numpy and scipy prototypes from a render-then-paint sawmill job to standard-library Python in `aw_geom.py` (aw.py stays under 100 KB). The gradient is computed lazily where the rim rays sample it, so a 1024 px render takes about 2 s with Pillow and 7 s without. On the sawmill set (render, a 20% squash, a disc on the roof, four paintings) every gate verdict and number matched the prototype.
- Found while writing the synthetic test: the rim lag window is 8% of the radius, so a squash bigger than the window registers as weak matches and an RMS near 0.05, never as its full size; `axis_err` cannot exceed about 0.08. On a clean synthetic ring a 20% squash passed the ellipse gate with a thick rim (0.85 to 1.0 of the radius) and failed it with a thin one (0.94); the spokes gate failed it either way. Written into references/sprite-json.md. A saturated-lag rule (count a lag at the window edge as unmatched) would close it; not done, to keep the prototype's tolerances.
- `stats` counted transparent pixels as white (clip_white 0.478 on a 96 px sprite was its transparent share); `stats`, `light`, `gamut` and `depth` now read opaque pixels, `accents` and `comp` report `alpha`. L-008 to L-010.
- Unit tests 51 to 62 (1 skipped without AW_NET; 2 skipped with Pillow hidden), green both ways. The 5 failing cases in evergreen.json are eval cases (claude plugin eval), not unit tests; not re-run here.

## [2026-10-24] release | 0.4.2 tagged (C-20261024-3)
- `pixel`: a run touching a fully transparent pixel is left out of `transitional_pixels`; test
  `Pixel.test_outline_on_transparent_black_is_not_a_blend` failed at 11.11% before the fix. 65 unit tests green, CI
  green on six jobs. PR #18 merged, `v0.4.2` tagged on the owner's go-ahead; 0.4.0 and 0.4.1 ship inside it.

## [2026-10-24] build | 0.5.0: setfit, comp --text-band, rubric 3 mechanism criterion (C-20261024-4)
- Generalised a loading-screen job's series gate into `aw.py setfit` (aw_geom.py, standard library; texture at `--width` 960 via a separable Gaussian in pure Python, about 6 s for five 1920 px screens with Pillow). On that job's five-screen series it reproduces the prototype: edge density 0.24 to 0.36, the held-out screen's fine grain at position 1.30, passing at widen 0.3. The treatment is an external command run without a shell (`{in}`, `{out}`).
- Tried and dropped: a leave-one-out self-check of every reference. On a four-image set the extreme member always falls outside the other three's range, so it fired on every member and would have pushed the widen far too wide. Calibration stays a held-out member plus a known-bad image (L-014).
- `comp --text-band`: edge and contrast pull against the frame; `busy_text_band` at 1.0 fired on 3 of 10 top and bottom 15% bands of that series (0.8 fired on 9). Checked by eye on three screens: the busy ones are dense crops and dark trees across a bright sky, the calm one snow.
- Rubric 3 adds criterion 6, Mechanism (a gate for any picture of a working machine). Cache and verdict defaults moved to rubric 3.
- Tests 70 (1 skipped without AW_NET). Evals not re-run (descriptions unchanged). L-014 to L-016.

## [2026-10-25] build | 0.6.0: measure fixes from the round 2 books (C-20261025-1)
- Book-learnings round 2 track 12 (Gonzalez and Woods, CGPP). Reproduced each proposed fault on a fixture before fixing it: aliased measuring copy above 4x, value as luma, median notan, grain read as sharpness, JPEG blocks read as a 2 px grid. The luma-only JPEG check the notes proposed did not work (block edges are in luma too); the guard tests the 8 px lattice instead (L-018).
- Real data: 60 random AI stills from the local render folder. Keys changed on 2 (both at 0.37, on the line), `uniform_sharpness` fired on the same 3, every still read clean grain (median 0.06 L*), separation 0.67 to 0.95 (10th to 90th). On 30 stills of 1216 to 1824 px the area-averaged copy lowered edge density by 0 to 8%. A carpet photo with no flat cell read as noisy (texture), documented.
- Tests 79 (8 new; 1 skipped without AW_NET); mutations of the reduction, the noise floor and the notan cut each caught. Budget: aw.py 82 KB (yellow, under 100). Rulings H1-H10.
## [2026-10-25] index | rebuilt (13 entries)

## [2026-10-25] build | 0.7.0: pixel-art measures and rows from the round 2 books (C-20261025-2)
- Book-learnings round 2 track 13 (Azzi, Silber, Dawe and Humphries; CGPP and Gonzalez for corner doubles and material cues). New `pixel` numbers in aw_measure.py: banding, corner doubles (the same stair-step rule as pixelwright's `clean.corners`), interior jaggies, pillow, `--bg` edge loss, tile repetition; degrade banding and pillow.
- The exact-span banding rule missed a hugging ring on a curve (offsets 0 and 1 now); on 30 AI renders quantised to 48 px sprites banding ran 0 to 6.5 per 100 edge pixels, so it is a locator (L-019). Pillow fired on 0 of 30. Tile repetition flagged 4 of 20 seamless tiles made from render crops; the flagged ones stripe in a 3x3 repeat, an unflagged one does not.
- Tests 85 (6 new); five mutations (each measure blanked, the stair condition dropped, the tile lines raised) caught. aw.py 83 KB, aw_measure.py 39 KB, knowledge files 192 KB (green). Rulings I1-I9.
## [2026-10-25] index | rebuilt (14 entries)
## [2026-10-26] fix | 0.7.1: `pixel` finds a scale 2 or 3 grid in a quality 90 JPEG (C-20261026-1)

- The round 2 handoff's open bug, reproduced first: scale 2 and 3 palette art at quality 90 and 95 read as scale 1, and a low-contrast scale 2 JPEG as 8. JPEG input now counts only steps that peak along their row or column (L-020). Peaks alone read smooth JPEGs as 2, 4 or 8 from their block edges (11 of 31 video contact sheets read 8), so the peak reading counts only below 8 and with a lattice contrast of at least 1.6 (mean step on the lattice over off it, block rows and columns left out; smooth 1.05-1.10, real 2.2-7.6). 112 real JPEG renders keep their scale; both checks are covered by mutation. A higher tolerance also worked but would drop close palette colours. New test fails with the peak test removed; 86 tests pass. aw.py 86 KB (yellow). 0.7.0 was tagged the same day; 0.7.1 waits for the owner.
