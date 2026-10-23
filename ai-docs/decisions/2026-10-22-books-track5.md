---
kind: decision
status: active
date: 2026-10-22
title: Books track 5 rulings (light, colour and composition measures)
tags: aw.py,aw_measure,comp,light,gamut,depth,thresholds
---

# Books track 5 rulings: light, colour and composition measures

Small design calls made while building the measurements proposed by the book notes (Gurney, *Color and Light* and
*Imaginative Realism*; Mateu-Mestre, *Framed Ink*; Roberts, *Mastering Composition*). The notes live outside this
repository; the build plan that names this track is the owner's plugin-learnings PROGRESS file.

## E1. A sibling module, not a bigger aw.py

The five commands and the shared helpers went to `skills/artwright/scripts/aw_measure.py` (25 KB). aw.py
(72 KB) imports it at its foot with `from aw_measure import *` after registering itself as `aw`. That way one
module object serves both `python aw.py` and `import aw`, and `Fail` is the same class in both. Built in place,
aw.py reached 99.9 KB against the 100 KB rule, with nothing left for the judge work that comes next. budget.py
checks both files against the same bands; AGENTS.md says so.

## E2. Thresholds come from flag rates, not labels

No owner labels exist for composition or light. The sample: 48 AI stills from the local ComfyUI output folder
(twelve series, four each, seed 7) and 7 Cleveland museum works. Each threshold was set so its flag fires on a
minority of them. A flag that fires on most images says nothing. Changes from the notes' sketches:

- `competing_focal`: the margin is taken against the strongest cell outside the peak's 3x3 neighbourhood. It
  fires under 0.03. The notes said 0.15 against the second cell, which flagged 60% of images: a peak's
  neighbours score almost the same as the peak.
- `edge_pull`: over 2.0 times the image mean, not 1.8 (23% of AI stills at 1.8, 6% at 2.0).
- `frame_tangent`: a run over 20% of the side, not 5% (ordinary content crossing the border band ran 5 to 15%).
- `blocked_entrance`: one horizontal line (a 5-row band) across 85% of the width, not any edge in the bottom 12%
  (that fired on all seven museum works).
- Hot spots: at least 12 L* and 2.5 local SD above the surroundings, 0.05% to 1% of the area. Brush texture
  otherwise counted.
- Colour cast: a reading, not a flag. Graded film stills carry a cast on purpose (17 of 48).

The cli.md flag table gives each rate. They are still uncalibrated; when owner labels exist, calibrate there.

## E3. Museum photographs: trim the mat first

Cleveland's web images show the paper, mat or backdrop round a print or a canvas. That margin read as tangents,
border pull and a blocked entrance. `comp` trims it under two tests. Every side needs a uniform band (row SD
under 0.08 in luma) at least 2 px deep that stops before an eighth of the side. At least three of those bands
must be light (mean over 0.55). Dark vignettes, space backgrounds and storm skies in AI stills are art, not margin, and were
being trimmed until the light test and the stop-before-the-cap test were added. A drawing on a sheet with a wide
margin keeps it (documented as a blind spot).

## E4. What was not built

- Armature lines and the vanishing point (structure tensor and a Hough transform): most bytes for the weakest
  signal. A vision model answers it better; cli.md says to ask one and check against `comp`.
- Intervals (even spacing of similar shapes): weak at 64 px and needs reliable object separation.
- Flat-fill detection (Gurney note A9): not built; `uniform-sat` and `chroma_cells` cover the cheaper half.
- `light --mask`: built as `--box x,y,w,h` (fractions), matching `comp --subject`; no mask file format to add.
- Shape count in `stats`: `comp` reports masses; `stats` says so beside `groups_estimate`.

## E5. Degrade kinds force a direction

Each new degrade kind must move its measure the same way on any image. Two did not on real images: `haze-off`
matched the far band to the near band (and lowered it where the far band was already crisper), and `tangent`
drew black on dark posters. Both now force the direction (far band at least 1.3 times crisper and more
saturated; line colour opposite the image's mean). Checked on 6 real images: 42 of 42 moves went the right way.

## E6. Version 0.2.0

New commands are new features: plugin and aw.py go to 0.2.0. Not tagged; the owner gives that go-ahead.
