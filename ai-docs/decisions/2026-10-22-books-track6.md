---
kind: decision
status: active
date: 2026-10-22
title: Books track 6 rulings (craft text, AI-look tells, rubric 2, rank cycles, cache key)
tags: craft,ai-look,rubric,judge,rank,cache,calibration
---

# Books track 6 rulings: craft text, AI-look tells, rubric 2, rank cycles, cache key

Small design calls made while turning the book notes into text and judge changes. Sources: Gurney, *Color and
Light* and *Imaginative Realism*; Mateu-Mestre, *Framed Ink* 1 and 2; Roberts and Garvey-Williams, each
*Mastering Composition*; Chen, *Mastering Composition for Photographers*; Huyen, *AI Engineering* (R-20261022-1 to
-3). The notes live outside this repository; the build plan is the owner's plugin-learnings PROGRESS file.

## F1. Book rows are marked `book`, not `yes`

A craft row read in a book now says `book: Author short-title pp. N`. It is a practitioner's teaching, not an
experiment, so it does not count as evidence the way `yes` rows backed by studies do. The eye-path row is the one
exception the book itself makes: Gurney reports eye-tracking studies, and the row says so.

## F2. The eye-path row was rewritten, not extended

The old row said leading lines and a value path carry the eye. Gurney's eye-tracking pages say the eye jumps
between points of interest, goes to faces and figures whatever the design, and skips contrast that fits the
scene. The row is now "Where the eye goes", with lines and spokes kept as supports.

## F3. Rubric version 2

Light logic became its own criterion, composition checks are listed in order, a `focal_off_subject` flag must be
answered, look words in a brief expand into traits, and a batch winner must pass brief fit. That changes what the
judge decides, so the rubric is version 2: `cache` defaults to it and `verdict init` writes it. Verdicts cached
under version 1 no longer match, which is the point of the key. The verdict contract's schema did not change, so
the contract stays at version 1. The Step 4 calibration (0.825 against the owner) was measured on rubric 1;
recompute at the next calibration.

## F4. A cycle marks its whole span close

`aw.py rank` lists every three-way loop among decided pairs (ties are not edges). Every row from the highest to the
lowest-ranked member of a loop is marked `close_to_next`, and `top_in_cycle` says when the leader is in one. The
test tournament puts the leader 1.65 times ahead of the runner-up, met directly, so only the cycle rule can mark it
close. Real data: the only judged set on disk is the Step 4 calibration, 40 disjoint pairs, where no triad can
form: 0 cycles, so no false alarm, but no real test either. A round-robin batch will be the first real check.

## F5. Sampling settings join the cache key only when given

`--temperature` and `--seed` are appended to the key when passed. Entries written without them keep matching
lookups without them, so the existing store stays valid. A verdict cached at one temperature never answers a
lookup at another.

## F6. Side order on human labels

`cache label --shown-first a|b` stores which image the owner saw first; `cache agreement` reports
`labels_first_shown_share`. The owner's calibration page already randomised sides and kept them in its manifest:
on the 31 non-tie labels the owner picked the first-shown image 15 times (0.48), so no side bias. The private
import script now passes the side through.

## F7. Version 0.3.0

Rubric 2 changes cache keys and the judge's procedure, so this is a minor bump on top of the untagged 0.2.0.
Neither is tagged.

## F8. Skipped, with reasons

- vocabulary.md additions (terminator, core shadow, shapewelding and the rest): they are critique words, not
  prompt words that steer a model, and the craft rows now define them where they are used.
- Colour scripting across a sequence: that belongs to cinewright's colour script (books track 3).
- A guard eval for "warm light, cool shadow" under an artificial-light brief: the rule's exception is written into
  craft.md (Light logic) and the rubric (criterion 3); a fair fixture needs a night scene drawn in code, left for a
  later eval pass.
- Armature, intervals and clusters stay unmeasured: the craft rows send them to a vision model, checked against
  `comp`, as track 5 decided (E4).
- Descriptions untouched: the four sit at about 596 of 600 tokens, and the new behaviour runs inside skills that
  already trigger.
