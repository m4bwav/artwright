---
name: artwright-judge
description: "Use whenever images must be compared, ranked or checked against a brief: 'which is better', 'pick the best of these', 'rank this batch', 'does this match my prompt', 'what should I change in the prompt', 'rewrite my prompt as a style or artist'. Judges pairs blind in both orders, ties when they disagree; ranks batches (Bradley-Terry); splits a brief into yes/no checks (FITS, FITS WITH FIXES, DOES NOT FIT); returns the next prompt and settings per model. Writes artwright/verdict.json for calling plugins. Not for brand palettes or on-brand scoring (brandwright) or video takes (cinewright-qc). Also 'refresh artwright-judge'."
---

# artwright-judge

The entry point sibling plugins call after they make images. It compares, ranks and tests fit to a brief, and
says what to change next. It never generates (comfyui-gen), never judges a video take against its shot card
(cinewright-qc keeps that), and never scores brand fidelity (brandwright ranks by brand distance first).

Script: `../artwright/scripts/aw.py` (commands: [../artwright/references/cli.md](../artwright/references/cli.md)).
Rubric and abstain rules: [references/rubric.md](references/rubric.md). Output contract for callers:
[references/verdict-contract.md](references/verdict-contract.md).

## Step 0

Freshness: the plugin's [evergreen.json](../../evergreen.json) (past due: say so in one line, refresh after).
Work folder: `<asset or batch folder>/artwright/` (default `./artwright`); pass it as `--work`. Start the contract:
`aw.py verdict init <folder> <images...> --kind pairwise|brief-fit --brief "<brief>"`.

## Why two at a time, in both orders

Models judging beauty are weak and order-sensitive: swapping two images flips up to 61% of verdicts, and going
from two candidates to four or more degrades models about seven times as much as people (R-20261021-2, -3). So:

- one pair per call, each pair judged twice in fresh calls, once per order;
- labels are neutral (1 and 2); file names, the model, the seed, the user's guess and other votes are never shown;
- a split between the two orders is a tie, flagged for a human, never a coin toss;
- orders that agree show the judge is consistent, not that the call is wide. When no craft defect separates two
  finished works (both intact, both skilled), the pick is taste: say it is close, name the taste axis (calm
  against drama, say) and never call one "objectively" or "universally" better.

## A batch

1. Dedupe: `aw.py dedupe <dir>`; drop near-copies (keep the first of each group). When the candidates were
   painted over a 3D render and the render folder exists, run `aw.py geomgate <render dir> <img>` on each and
   rank only those with `pass: true`; list the rest with their `failing_gates`, never as close losers. A
   candidate that joins a series (loading screens, chapter plates) runs `aw.py setfit <img> --refs <the series>`
   the same way: one that fails a measure is listed with it, not ranked.
2. Triage: `aw.py sheet <dir> -o sheet.png`; one Read; strike only rendering-integrity failures (hands, merged
   objects, broken text) and clear brief misses, naming each by its letter. Never rank from the sheet.
3. Pairs: up to about 12 candidates, round robin; above that, Swiss rounds: `aw.py rank --work W --next 6` gives
   the next pairs between neighbours that have not met.
4. Each pair: `aw.py compare prepare A B --work W` writes `order1` and `order2` images. Judge each in a fresh
   call with the rubric (cold read, per-criterion notes tied to regions, then the pick). Record:
   `aw.py compare record <pair> 1 <1|2|tie> --work W --confidence medium --criteria read value`, same for order 2.
5. Rank: `aw.py rank --work W --write` fits Bradley–Terry with ties and writes the ranking into
   `verdict.json`; on a work folder judged earlier (`pairs.jsonl`, `matches.jsonl`), run it too, never tally the
   records by hand. Rows marked `close_to_next` are not ordered with confidence; say so. `cycles` lists loops
   (A beat B, B beat C, C beat A); when `top_in_cycle` is true the winner is close, whatever its strength.
6. Winner check: run the brief-fit steps below on the top image before reporting it. Winning a batch is not
   fitting the brief; if it is DOES NOT FIT, check the next ones, and say plainly when none fits.

Cost: a 16-image round robin in both orders is about 624k image tokens. Keep pair images at the default cell
(768 px) and use Swiss rounds for large batches.

## Fit to a brief

1. Split the brief into atomic yes/no checks: subjects, count, attributes, relations, camera and framing, light,
   style (by named traits), mood, text, forbidden items. A word naming a look ("golden hour", "overcast",
   "moonlit", "low angle", "horizon low") becomes the traits that show it, each its own check
   ([references/rubric.md](references/rubric.md), criterion 1). Write them before looking.
2. Cold read the image, then answer each check with the region that decides it.
3. Verdict: `FITS`, `FITS WITH FIXES` or `DOES NOT FIT`; hard fails (wrong subject, wrong count, forbidden item,
   broken text the brief asked for) listed separately.
4. Integrity gate: anatomy, hands, duplicated or merged objects, seams, perspective, mixels. A gate, not taste.
   A working machine in the picture also takes the mechanism gate (rubric criterion 6): power source to tool
   connected, water or wind where the machine's type needs it, nothing pouring from an axle.

## What to change next

Each fix is classed by channel, cheapest first:

| Channel | Use when |
|---|---|
| `prompt` | a missing or misread element; word order (the subject first on LLM-encoder models) |
| `setting` | steps, CFG, sampler, size; a negative prompt only where CFG is above 1 |
| `control` | pose, depth or edges wrong; layout must hold |
| `reference` | identity, style or palette drift across a set |
| `inpaint` | one local defect in an otherwise good image |
| `model` | the model cannot do it (text, a style, a count) |

Before naming a light or composition fix, run `aw.py light` and `aw.py comp` on the image; their flags point at
the AI-look rows that apply (rows 17 to 29). Use the model's profile
([references/models/README.md](references/models/README.md)): Z-Image Turbo and FLUX.2
ignore negatives; Qwen-Image honours them. Write a revised prompt per target model plus a one-line diff
(`+ "low sun from the left" / - "dramatic lighting"`). Vocabulary that works both ways:
[references/vocabulary.md](references/vocabulary.md); the "AI look" and its fixes:
[references/ai-look.md](references/ai-look.md). Quality boosters ("masterpiece", "8k") are dead words: drop them.
A living artist's name becomes traits, with one line saying so.

## Hand back

Fill `verdict.json` (items, ranking, fit, fixes, abstained, notes), set `status: final`, then
`aw.py verdict validate <folder>`; it must print `valid: true` before you report. Reply with the winner or
the fit verdict first, the decisive criteria each tied to the region that shows it, ties shown to the user
with both images, and the next prompt. The user's own preference is shown only after the blind verdict. Cache each verdict:
`aw.py cache put <img> --model <judge model> --verdict '<json>'`, adding `--temperature` and `--seed` when the
judge's sampling is set: a different temperature is a different judge.

## Calibration

The owner's labelled pairs live in `ARTWRIGHT_HOME/calibration/` (artwright-curate). `aw.py cache agreement W`
reports both-orders agreement (target 0.8 or above), accuracy against the labels and the re-query noise floor.
Below target, say so in the verdict and lean on ties. Recompute whenever the judge model changes.

## Guards

All of the hub's guards apply ([../artwright/SKILL.md](../artwright/SKILL.md)): nothing about attribution, value
or "AI-made" from pixels; no lone scores; no "looks good"; never the golden ratio as a reason.

## Maintenance

Shared evergreen unit at the plugin root: [evergreen.json](../../evergreen.json),
[RESEARCH.md](../../RESEARCH.md), [CHANGELOG.md](../../CHANGELOG.md), [LEARNINGS.md](../../LEARNINGS.md),
[TESTS.md](../../TESTS.md), [MAINTENANCE.md](../../MAINTENANCE.md). Model profiles are volatile: recheck every
60–90 days. The verdict contract is a public interface: change it only with a version bump in `artwright`.
