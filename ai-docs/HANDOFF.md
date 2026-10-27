# artwright handoff

Updated 2026-10-26 (0.7.2 fix validated; release and wiki publication pending). Older detail is in
[log.md](log.md) and the decisions files.

## State

- Public repository https://github.com/m4bwav/artwright. Latest tag `v0.7.1` (2026-10-26: `pixel` finds a scale 2
  or 3 grid in a quality 90 JPEG, L-020); `v0.7.0` the same day carries 0.5.0, 0.6.0 and 0.7.0. Tags need the
  owner's standing release authorization applies after version bumps and passing checks.
- Wiki updated to 0.7.1 on 2026-10-26 (wiki commit 41c7ba3): how in
  [notes/2026-10-22-github-wiki.md](notes/2026-10-22-github-wiki.md), "Since 0.7.1". Its findings for the next
  release are under "Wiki findings (2026-10-26)" below.
- Hand-off PRs comfyui-gen#82 and polywright#24 and the scene-illustration PR #17 are merged.
- Still open: the 5 failing eval cases in evergreen.json (paid evals, not re-run).

## Books round 2, track 12 (2026-10-25)

- 0.6.0: anti-aliased measuring copy, value in L* (key cuts 0.38/0.68), notan by Otsu and k-means, `light`
  separation, `stats` noise and comp's noise floor, JPEG block guard in `pixel`, grey sheets, degrade noise, band,
  alias. Rulings H1-H10 in [decisions/2026-10-25-books-track12.md](decisions/2026-10-25-books-track12.md).
- The grain readings (1 and 3 L*) are set from synthetic noise only; no real grainy photo was labelled.

## Books round 2, track 13 (2026-10-25)

- 0.7.0: `pixel` reports banding, corner doubles, interior jaggies, pillow, `--bg` edge loss and tile repetition
  (all reported, none failed); degrade banding and pillow; pixel-art, sprites-tiles, ai-look (30-34), craft.md
  Material cues. Rulings I1-I9 in [decisions/2026-10-25-books-track13.md](decisions/2026-10-25-books-track13.md).
- No hand-made pixel art was available locally: thresholds come from fixtures and AI renders quantised to sprites.
  Score real hand-made sprites before giving any of these a pass line (L-019).

## Wiki findings (2026-10-26)

The 0.7.2 follow-up fixes findings 1, 2 and 4 and documents the filter difference in finding 5.
PR #24 already fixed finding 3. Tests: 87 run, one museum skip, zero failures; 112 real JPEGs across
both decoders (224 decodes) keep their grid scales. The ffmpeg fixture's extra 2 px steps come from chroma
upsampling; the guard now checks luma as well as RGB. Finding 6 is cosmetic and unchanged.

1. Bug: the 0.6.0 JPEG block guard in `pixel` does not fire when ffmpeg decodes the JPEG (no Pillow). A smooth
   quality 55 JPEG had 0.665 of its steps on the 8 px lattice through ffmpeg 9.0.1 (0.952 through Pillow), under
   the guard's 0.8, so it read as scale 2 with 146005 orphans on Windows, Python 3.9. Still so in 0.7.1.
2. `stats` noise is measured on the 256 px copy, so Gaussian grain of SD 16 on a 2000 x 1200 image reads `clean`
   (0.5 L*) and the same grain on a 256 px copy reads `noisy` (3.93). cli.md does not say the estimate is at
   256 px.
3. CHANGELOG Releases list at v0.7.1: 0.7.1 still "not tagged yet", and 0.4.0 "never tagged, shipped inside 0.4.2",
   but tags and releases `v0.4.0` (2026-10-24) and `v0.7.1` (2026-10-26) exist.
4. sprite-json.md says `edges_info` is per part "at 256 px"; it is at most 256 px (a 192 px render is measured at
   192), and a part with no edges inside it reports precision and recall 1.0.
5. Measures differ slightly with and without Pillow since 0.6.0 (box filter against 2x2 halving); one test flag
   flipped (`competing_focal` on the tangent degrade, focal margin 0.015 against 0.042). Not a doc claim either
   way; worth one line in cli.md.
6. Cosmetic: Windows, Python 3.9 printed `"gradient_tb": -0.0` for a flat tile where Linux printed `0.0`.

## Carried forward

- The `busy_text_band` threshold (1.0) comes from one five-screen series; recheck it on another game's screens.
- Scene mechanism gates (rim, hub, feed, tail) stay in their job's folder until a scene contract exists.
- Rubric 3 changed cache keys (as rubric 2 did); recompute calibration agreement at the next calibration (the
  0.825 was rubric 1).
- action-winner-fit is 5/6: about one run in five never loads the judge. Descriptions are at ~596 of 600 tokens;
  trim before adding (L-002).
- No round-robin judged batch exists yet, so the cycle rule has had no real test.
- Flag thresholds are set from flag rates, not labels (L-004). Calibrate on owner labels when they exist.

## Things the next session must not forget

- `claude plugin eval --keep-temp` keeps each run's `out/trace.jsonl`; read it before blaming the skill (L-007).
- `evergreen.py worth --ab` takes one skill folder, not the plugin root; it tracks only that skill's firing.
- Eval loops go in a `.sh` file run under WSL (L-003). The LLM grader sees only the last message.
- Keep `resize_box` for the perceptual hashes; measures read `small()` (L-017).
- `gh pr merge` can be refused by the auto-mode classifier even with the owner's go-ahead; assign and label then.

## Read first

1. [log.md](log.md) (last entries), then the newest decisions file.
2. `TESTS.md` for eval history; `references/cli.md` for every command.
