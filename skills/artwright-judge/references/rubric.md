# Judging rubric

The rubric every pairwise, brief-fit and critique verdict uses, with the abstain rules. Rubric id
`artwright-judge`, version `3` (the `--rubric` and `--rubric-version` that `aw.py cache` keys on). Version 3
(2026-10-24) added the mechanism criterion (6). Version 2 (2026-10-22) split light logic into its own criterion,
listed the composition checks in order and made brief fit gate the batch winner. Verdicts cached under an older
version no longer match.

Back to [SKILL.md](../SKILL.md). Sources: synthesis section 4 and R-20261021-2 to -7 in the repository's
RESEARCH.md.

## Criteria, in order

1. **Brief fit.** Atomic yes/no checks from the brief: subjects, count, attributes, relations, camera, light,
   style, mood, text, forbidden items. Hard fails are listed separately. A word that names a look becomes the
   traits that show it, each tested on its own. "Golden hour": low orange sun, blue shadows, light only on the tops
   of tall things. "Overcast": no cast shadows, the sky the lightest note. "Moonlit": blue-green against warm
   lamps. "Low angle": the horizon below the subject's eyes, the camera looking up.
2. **Read and composition**, in this order, each tied to a region: thumbnail and three-value read; the brief's
   subject against the measured focal peak (`aw.py comp --subject`); the armature; edges and corners; tangents and
   mergers; horizon and camera height against the brief; depth planes; the main figure's silhouette. A
   `focal_off_subject` flag must be answered in the notes, either explained or counted against the image.
   Placement is judged by its reason. Thirds is never a score.
3. **Light logic.** One plan for the whole image: the key, a shadow family filled by sky or bounce, cast shadows
   that sharpen at contact, highlights tinted by their source, distance that recedes. `aw.py light` and `depth`
   point at where to look. An artificial or stylised brief can ask for broken daylight rules; judge against it.
4. **Value and colour.** A few large value masses, not mid-grey mush; temperature as relative; one leading colour
   and accents placed with intent; harmony as a choice, not a formula (Itten's schemes predict nothing; Albers's
   relativity holds).
5. **Rendering integrity** (a gate, not taste). Anatomy and hands; duplicated or merged objects; text; seams;
   perspective; mixels; two light directions in one composite.
6. **Mechanism: does the machine work as drawn** (a gate, like 5). Apply it to any image whose subject or brief
   includes a working machine or device: a mill, a pump, a forge bellows, a crane, a clock, a vehicle, a weapon.
   Skip it for a ruin, a toy, a pure ornament, or a brief that asks for a broken or impossible machine. Trace the
   power from its source to the tool and check each link is drawn: water or wind reaches the wheel or sails, a
   shaft or belt carries the motion through the wall, the saw, stones or hammer sit at the end of it. Parts sit
   where the physics needs them: water meets a wheel where its type takes it (low on the upstream side for an
   undershot or breastshot wheel, over the top for an overshot one) and leaves downstream; nothing pours from an
   axle or a hub; a lever has a pivot, a belt has two pulleys, a load hangs from something that can hold it. Name
   the broken link and its region ("the race stops a wheel's width short of the wheel, lower left"). When the
   painting was made over a 3D render, the render shows the working layout: compare against it, and judge any
   measure on the painting relative to the render's own score in the same zone, never against a fixed number
   (L-015).
7. **Style coherence.** One consistent style; it matches the movement or reference asked for, by named traits.
8. **Expressive intent.** Mood and story match the brief, including briefs that ask for rough or "ugly" work.

## Procedure

1. Cold read before the brief: what the image shows, the three things the eye goes to first.
2. Per-criterion notes for each image, each tied to a visible region.
3. Output: `{"winner": 1|2|"tie", "confidence": "low"|"medium"|"high", "decisive_criteria": [...]}`.
4. A batch winner is the best of what was made, not proof that it fits. Run the brief-fit checks on it before
   reporting it, and say so plainly when every candidate is DOES NOT FIT. A ranking orders candidates; it does
   not grade them (after Huyen, *AI Engineering*).

## Abstain (tie, flagged for a human)

- The two orders disagree.
- Both images fail the same gate.
- Confidence is low on every decisive criterion.
- In a ranking, candidates inside a cycle (A beat B, B beat C, C beat A; `aw.py rank` lists them) have no order:
  report them as close, whatever the strengths say.

A third run may break a tie only by agreeing with one earlier verdict (`aw.py compare record` resolves it).

## Blindness

The judge never sees the user's guess, the model or seed, other votes or file names. The user's preference is
shown after the blind verdict.

## Scores

Never a lone score. An absolute 1–10 only when asked, anchored by three labelled reference images (low, middle,
high), with a warning that model scores bunch at the top. In `verdict.json`, `score` requires `score_anchors`.

## Language

Each finding names a region and a reason. Forbidden: "looks good", "feels", "somewhat", "stunning", the golden
ratio as a reason. Selective: the top two or three issues, not a list of everything.
