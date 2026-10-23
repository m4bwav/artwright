# Tests: artwright

Test runs for [README.md](README.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261022-6 · 2026-10-22 · claude plugin eval 2.1.281 under WSL2 --scaffold, sonnet · books track 5 · action-light 6/6, actions 3 others 8/9, decoys 9/9, triggers 24/24
- action-light (new): 1/3 on the first run, then 3/6 after the body line said "run aw.py before answering, not by eye alone". The failing runs ended in 2 or 3 turns: the hub never loaded, and the model judged the picture by eye. After the hub description named light and composition (and dropped "claims tie to regions" to stay in the budget), 6/6.
- action-palette 3/3, action-sheet 3/3, action-pixel 2/3 (one run ran 16 turns without aw.py; it passed 12/12 in T-20261022-2, so a flake, not this change).
- Decoys 9/9 and triggers 8/8 (24/24) on the new description.
- Spend $6.39.
- led to: C-20261022-6; L-002 confirmed

### T-20261022-5 · 2026-10-22 · evergreen.py worth skills/artwright --ab --runs 1 (claude -p, native Windows, plugin-dir) · A/B 20 graded cases · with 17/20, without 12/20
- Gain +25 points, noise margin 27 at one run per arm: the tool's verdict is CUT (no gain beyond noise at 1.99x the cost, 2.37x the turns). Paired by case: 5 with-only passes (action-sheet, action-pixel, guard-rubens, outcome-brief-fit, outcome-ming-price), 0 without-only passes, 12 both pass, 3 both fail (guard-ai-generated, guard-golden-ratio, outcome-pairwise-orders). A one-sided sign test on 5-0 gives p ≈ 0.03, so the gain is likely real; the cost is where the verdict bites. Not re-run: a second run per arm (about $10) would pass this session's $15 eval limit.
- action-palette · environment · the with arm asked to edit the repository's own LEARNINGS.md (outside the run folder) and was refused; left out.
- 7 cases "skill never fired in the with arm": the A/B watches only the hub; these cases (pairwise-orders, tie-pair, brief-fit, pixel-pair, action-pixel, vocab-rewrite, living-artist) belong to the judge and pixel skills. Not verified: the run records keep no per-run skill trace.
- Spend $10.25; day total $44.24.
- led to: decisions/2026-10-22-step4-rulings.md D2, D5

### T-20261022-4 · 2026-10-22 · claude plugin eval 2.1.281 under WSL2 --scaffold, sonnet, judge sonnet · tune iteration 3 · 3/6 runs
- outcome-pairwise-orders 2/3 · grader-strict · after the grader stopped asking for trace evidence it cannot see, one run still judged FAIL by all three votes although the reply names both orders, the original and regions.
- guard-ai-generated 1/3 · mixed · the LLM grader passed 2 of 3 and the regex 2 of 3, on different runs; the replies now open with "pixels cannot decide" and stopped treating the file name as provenance.
- No A/B: `worth --ab` (21 value cases, both arms, about $10) would pass the session's $40 cap. Spend for the day $33.99.
- led to: C-20261022-2

### T-20261022-3 · 2026-10-22 · same harness · tune iteration 2 (failing cases plus triggers) · 7 cases 13/21 runs, triggers 8/8 (24/24)
- Now passing: outcome-living-artist 3/3, outcome-ming-price 3/3, outcome-vocab-rewrite 3/3 (the judge's description now names prompt rewrites into a style or artist, and the skill fires: 6 turns instead of 1).
- outcome-brief-fit 2/3, outcome-tie-pair 2/3 · partial · one tie-pair run still declared a clear winner between two intact Hokusai prints.
- outcome-pairwise-orders 0/3 · grader-blind · reasons were tied to regions, but the grader asked for proof of both orders from the trace, which the LLM grader never sees.
- guard-ai-generated 0/3 · skill · replies opened "provenance answers this" and cited the file name as the provenance.
- led to: C-20261022-2

### T-20261022-2 · 2026-10-22 · same harness, by mistake the whole suite four times (L-003) · actions 12/12, decoys 35/36, on the new descriptions
- A loop's `$c` was expanded away before `bash -lc` ran it, so every pass ran all 32 cases under a $3 cap until stopped; about $14. The replicates still measured the new descriptions: action cases 12/12, decoys 35/36 (decoy-brand 2/3 once), guard-golden-ratio LLM grader 12/12 with the regex too narrow.
- guard-proud-framing 1/9 graded · cost-cap · most runs were skipped by the $3 ceiling before their LLM grader ran; one graded FAIL (the critique called the sprite "flat" without a region-level reason). Its clean run in T-20261022-1 was 3/3.
- led to: L-003

### T-20261022-1 · 2026-10-22 · claude plugin eval 2.1.281 under WSL2 --scaffold (museum images fetched and hash-checked in the scaffold), sonnet, judge sonnet · paid tier, first run · 11/18 cases, 39/54 runs
- outcome-brief-fit 0/3 · grader-blind · the reply was right (DOES NOT FIT, every check named, verdict written and validated); the criterion asked the judge to confirm a file it cannot see.
- outcome-living-artist 1/3, outcome-vocab-rewrite 0/3 · undertrigger · answered in one turn with no skill: a negative prompt for Z-Image Turbo, and an offer to take the living artist's name.
- outcome-ming-price 2/3 · grader-strict · asked for the word "hammer".
- outcome-pairwise-orders 0/3 · skill · reasons not tied to regions.
- outcome-tie-pair 0/3 · skill · both orders agreed, so the reply called it "not a close call" and Red Fuji "more universally pleasing".
- guard-ai-generated 0/3 · undertrigger and skill · "No, this isn't AI-generated", from the paper texture and the file name.
- guard-golden-ratio 0/3 · grader-narrow · the LLM grader passed every run; the regex missed "no real empirical support", "never a reason", "wouldn't be why it works".
- Passing: the four cubism cases, oldest painting, theory, pixel pair (all 3/3), guard-rubens, guard-reign-mark, guard-proud-framing (3/3). Cost $9.46 plus a $0.18 probe.
- led to: C-20261022-2, L-002 (confirmed again: a request the description does not name answers without the skill)

### T-20261021-4 · 2026-10-21 · claude plugin eval (triggers, decoys: 2.1.281 Windows; actions: pinned 2.1.281 under WSL2 Ubuntu with --scaffold), --ablation none, sonnet · cheap tier, final text · 14/14 cases, 42/42 runs
- Triggers 8/8 (24/24 runs), decoys 3/3 (9/9), actions 3/3 (9/9) on the descriptions in C-20261021-3. Cost of this round $4.0; the whole session's eval spend $15.76 across 14 runs of the harness.
- No baseline arm yet: the A/B (`evergreen.py worth --ab`) and the paid tier (18 outcome and guard cases) are Step 3.
- led to: none

### T-20261021-3 · 2026-10-21 · claude plugin eval, sonnet · actions 2/3 then 8/9 runs, decoys 1/3 after the colour wording
- action-palette 0/3 and action-sheet 0/3 · undertrigger · no artwright skill fired; the model wrote its own PIL scripts for the colour shares and the contact sheet. After the hub description named colours and contact sheets: palette 3/3, sheet 2/3.
- decoy-brand 2/3, decoy-site 2/3 · overtrigger · the colour wording pulled brand-palette and website-direction requests into the hub (the eval sandbox has no brandwright or sitewright to route to). Fixed by naming both owners in the hub description.
- led to: L-002, C-20261021-3

### T-20261021-2 · 2026-10-21 · claude plugin eval, sonnet · actions 0/3 (harness), decoys 2/3
- Actions under native Windows: refused (no sandbox backend for Bash). Under WSL2 with the pinned 2.1.281: ran, but every run started in an empty workspace (the fixtures were not there), and `tool: Bash|PowerShell` in the grader matched no call. Fixed with a `fixture.sh` scaffold per case (`--scaffold`) and `tool: Bash`; action-pixel then 3/3.
- decoy-brand 0/3 · overtrigger · "score these mock-ups for how on-brand they are" fired the judge. Fixed by naming brandwright in the judge's description; decoys then 3/3.
- led to: L-001, C-20261021-3

### T-20261021-1 · 2026-10-21 · claude plugin eval 2.1.281, --ablation none, sonnet, Windows 11 · triggers 8/8 (24/24 runs)
- First run of the cheap tier's trigger cases on the Step 2 text. $2.07.
- led to: none
