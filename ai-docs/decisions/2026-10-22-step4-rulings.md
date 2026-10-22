---
title: Step 4 rulings
date: 2026-10-22
tags: [calibration, a-b, wiki, release]
---

# Step 4 rulings (2026-10-22)

Small rulings made during Step 4, each flagged in one line in the session's final message.

## D1. Calibration: accuracy passes, both-orders agreement does not; no public rubric change

The owner labelled all 40 pairs. Against his picks the judge scored 0.825 (target 0.8); its both-orders agreement
stays 0.775. By pair kind (judge vs owner): degraded CC0 0.88 (16), pixel art 1.00 (3), the owner's seed pairs
0.75 (16), re-encode ties 0.80 (5). Both-orders agreement by kind: 0.88, 1.00, 0.62, 0.80.

What the seven misses share: five are the judge's own ties (its orders flipped) where the owner picked a side, or
one identical re-encode he picked as better (label noise). Where both orders agreed (27 pairs) the judge matched
him 25 times. The other two: a saturate pair where he preferred the saturated image, and a seed pair he called a
tie. On the four saturate pairs he preferred the saturated image three times, so "more saturation" being scored a
degradation is a taste mismatch for this owner, not a general rubric error; it went into the private
`taste.md`, and the public rubric is unchanged (curate's rule: promote a taste lesson only when it is general and
seen three times across different sets). The rule "below 0.8 both-orders agreement, show ties to a human" stays,
and the numbers confirm it: the judge's ties are where a person adds the most.

## D2. The A/B targets the hub skill folder

`evergreen.py worth . --ab` refuses a plugin root ("--ab and --probe take one skill folder"). All 21 value cases sit
on the hub (the lite scan attributes them to `skills/artwright`), so the A/B runs `worth skills/artwright --ab
--runs 1`. The lite scan's "unreachable" warning for `references/models/*` is a false positive (they are linked
from `models/README.md`, which SKILL.md links), and its `<living artist>` placeholder warning is the case's literal
text, not a variable.

## D5. The A/B's CUT verdict is not acted on

`worth --ab --runs 1` (T-20261022-5): with the plugin 17 of 20 graded cases passed, without it 12 of 20; the tool
calls +25 points inside its 27-point noise margin at 1.99x the cost and prints CUT. Paired by case the plugin won 5
and lost none, which one run per arm cannot separate from luck by the tool's margin but a sign test can (one-sided
p ≈ 0.03). The cost multiple is expected for a skill that renders contact sheets and runs aw.py. The plugin stays;
the next A/B should use `--runs 3` on the 8 cases that differ or both fail (about $6) to narrow the margin, and the
A/B should be pointed at the judge and pixel skills for their own cases. Open finding: in action-palette the with
arm tried to edit the repository's LEARNINGS.md from a run folder; find which instruction sends it there.

## D3. Wiki: the fix is described, not re-pasted with new hashes

The known-issue section became "A tie in both orders", showing the fixed `compare record` output (pair id and
fields identical to the wiki's fixtures) and describing the `rank` result in prose, because the hashes from a fresh
run would not match the wiki's `dusk.png` and `noon.png` drawings without re-running the verify script.

## D4. Release PR left for the owner

The owner gave a go-ahead for the release. PR #7 (version 0.1.1, release line, exit codes in README and AGENTS.md)
passed CI, but merging it was refused by the session's permission classifier, so it is assigned to the owner with
`needs-review`. The tag `v0.1.1` and the reinstall follow its merge.
