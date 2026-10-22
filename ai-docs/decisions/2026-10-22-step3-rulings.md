---
title: Step 3 rulings
date: 2026-10-22
tags: [evals, calibration, banner, hand-offs, verdict]
---

# Step 3 rulings (2026-10-22)

Small rulings made during Step 3, each flagged in one line in the session's final message.

## C1. Image eval cases fetch the museum images in their scaffold

`make_fixtures.py --emit-scaffold` now writes a `fixture.sh` for every case whose prompt names a fixture: the
synthetic PNGs as base64 (only the ones the prompt names, except action cases, which get all), and each Cleveland
CC0 image fetched with curl and checked with `sha256sum -c` against the hash pinned in `tests/test_aw.py`. Base64
of the seven museum JPEGs (2.4 MB) in every case would have bloated the repository; `context.add_dirs` was not
needed because the probe case showed the scaffold has network. For `evergreen.py worth --ab`, which copies a case's
`files` into each run folder, the image cases carry `"files": ["evals/fixtures/out"]` (run `make_fixtures.py --net`
first).

## C2. The calibration set: 40 pairs, four kinds, 1024 px JPEG canonical files

16 degraded pairs from 17 Cleveland CC0 paintings and prints (`aw.py degrade`: saturate, crush, crop, jpeg, blur),
3 pixel-art pairs (off-grid resample, orphans, mixels), 16 same-prompt seed pairs from the owner's own ComfyUI
renders (grouped by the prompt in the PNG metadata), and 5 ties (the canonical file against a quality-84
re-encode). Every image is stored as a 1024 px JPEG so the labels and the judge hash the same file. Sides are
shuffled with a fixed seed; the manifest (which side is which, the kind) stays in the private studio folder and is
never published. The set, the manifest and the judge's records live in `ARTWRIGHT_HOME/calibration/`; the images
are git-ignored there (123 MB with the two-up pair renders) and rebuild from the manifest.

## C3. The labelling page stores picks in the artifact's database

A private claude.ai artifact shows one pair at a time (left, same, right; arrow keys; an optional why) and writes
each pick to its `picks` collection, keyed by the pair id. A session reads them with ArtifactData, maps left and
right to a and b through the manifest and writes `aw.py cache label` rows. Picks save as the owner goes, so he can
stop and resume.

## C4. The judge's calibration run uses blind agents, the two orders in different agents

Four agents judged 20 two-up images each; no agent saw both orders of a pair, the sources, or the manifest. This is
the closest stand-in for "each order in a fresh call" without 80 separate sessions.

## C5. A tie in both orders is a tie

`resolve` returned `decided` with no winner when both orders said tie, and `cache agreement` then crashed on it.
Now it returns `tie`; a unit test covers it.

## C6. The banner is picked by the judge and kept as JPEG

Four Z-Image Turbo seeds (two per host), a contact sheet for triage, then a blind round robin in both orders;
seed 202 won all three of its pairs. The seeds and sheet are committed as JPEG (1.3 MB in all, not 8 MB of PNG);
the judge's finished `verdict.json` sits beside them as `banner-verdict.json`.

## C7. Graders that asked for what the judge cannot see were reworded

The LLM grader reads only the last message, so "writes verdict.json and it validates" became "says the verdict was
written", the golden-ratio regex now accepts the ways replies actually correct the premise ("no real empirical
support", "never a reason", "wouldn't be why it works"), and the Ming case asks that the price is said to include
the premium rather than for the word "hammer".

## C8. Hand-off PRs wait for the owner

The comfyui-gen and polywright rows are in other repositories' shared files, which the kickoff reserves for the
owner: both PRs are assigned to him with `needs-review`, not merged.
