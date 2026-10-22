---
name: artwright-curate
description: "Use to maintain artwright's knowledge and the user's private taste record: add, fix, source or retire a movement, theory entry, style term, model profile or law row; record which image the user preferred and why; label calibration pairs ('remember I liked this one', 'add this movement', 'label pairs for the judge'); promote a lesson from taste into the public files. Public rows get a source, date and verified flag; private taste stays in ARTWRIGHT_HOME. Judging is artwright-judge. Also 'refresh artwright-curate'."
---

# artwright-curate

Keeps artwright's two stores right: the public knowledge in the repository and the private taste record on the
user's machine. Nothing private ever enters the repository.

Store layout and file formats: [references/store.md](references/store.md). Script:
`../artwright/scripts/aw.py` (`cache`, `cache label`, `cache agreement`).

## Step 0

Freshness: the plugin's [evergreen.json](../../evergreen.json) (past due: say so in one line, refresh after).
Decide which store the change belongs to:

| Change | Store |
|---|---|
| A movement, theory paragraph, tradition term, style term, model fact, law row, market rule | public (repository) |
| The user's verdict, a pick, why they liked it, a calibration label, a keyword that worked on their setup | private (`ARTWRIGHT_HOME`) |
| A general lesson seen three times in the private record | promote to public, written without the user's specifics |

## Public knowledge (the repository)

Files: the hub's references (movements, theory, traditions, evidence, craft, ceramics, market, law), the judge's
(rubric, vocabulary, ai-look, models/), the pixel skill's (pixel-art, sprites-tiles).

1. Research beats recall: fetch the source this session. A row backed by a fetched source gets `verified: yes`
   and the date; anything else ships `verified: no`. Never upgrade a row from memory.
2. Log the source as an `R-YYYYMMDD-n` entry in RESEARCH.md (track, source URL, magnitude) and the edit as a
   `C-YYYYMMDD-n` line in CHANGELOG.md with `because:`.
3. Keep each file inside its size budget (`python scripts/budget.py`); `vocabulary.md` is red above 40 KB.
   Retire before adding when a file is full.
4. Gold answers (market.md) and volatile files (law.md, models/) carry a recheck-by date; move it when re-checked.
5. Movements: four to six visually checkable traits, named neighbours, Wikidata QID; non-Western rows use the
   tradition's own terms and stay `verified: no` until fetched.
6. A living artist is never added as a style term; describe the traits instead.
7. Run the checks before committing: `python tests/check_skills.py`, `python tests/test_aw.py`,
   `python scripts/budget.py`.

## Private taste (`ARTWRIGHT_HOME`, default `~/.artwright`)

- `verdicts.jsonl`: every judged image (written by `aw.py cache put`); doubles as the calibration log.
- `taste.md`: the user's stated likes and dislikes, each with a date and the image or project it came from.
- `calibration/labels.jsonl`: the user's own picks on pairs (`aw.py cache label A B a|b|tie --note "why"`).
  Ask one pair at a time, plainly ("which of these two?"), with both images side by side.
- `keywords/<model>.md`: prompt words that did or did not work on a model in real runs, with the run and date.
- `palettes/`: Lospec palettes fetched on request.

On a machine with a private notes vault, `ARTWRIGHT_HOME` may be a junction into it; the skill only needs the
environment variable or the default path.

Agreement: `aw.py cache agreement <work dirs>` reports both-orders agreement (target 0.8), accuracy against the
labels and the re-query noise floor. Record the numbers in `taste.md` with the judge model and date; recompute
when the model changes.

## Promotion

A taste lesson becomes public only when it is general ("hue-shifted ramps read better than flat ramps at 16
colours") and seen three times. Write it without the user's names, projects or images, cite the evidence count,
and mark it `verified: no` unless an outside source backs it.

## Guards

Never write names, private projects, machine paths or images into the repository. Never delete the private record
without the user's yes. The hub's judging guards apply.

## Maintenance

Shared evergreen unit at the plugin root: [evergreen.json](../../evergreen.json),
[RESEARCH.md](../../RESEARCH.md), [CHANGELOG.md](../../CHANGELOG.md), [LEARNINGS.md](../../LEARNINGS.md),
[TESTS.md](../../TESTS.md), [MAINTENANCE.md](../../MAINTENANCE.md).
