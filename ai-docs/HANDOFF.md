# artwright handoff

Updated 2026-10-26 (0.7.0 tagged; 0.7.1 JPEG grid fix). Older detail is in [log.md](log.md) and the decisions files.

## State

- Public repository https://github.com/m4bwav/artwright. Latest tag `v0.7.0` (2026-10-26; carries 0.5.0, 0.6.0
  and 0.7.0). Untagged on main: 0.7.1 (`pixel` finds a scale 2 or 3 grid in a quality 90 JPEG, L-020). Tags need
  the owner's go-ahead.
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
