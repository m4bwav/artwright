# Judging rubric

The rubric every pairwise, brief-fit and critique verdict uses, with the abstain rules. Rubric id
`artwright-judge`, version `1` (the `--rubric` and `--rubric-version` that `aw.py cache` keys on).

Back to [SKILL.md](../SKILL.md). Sources: synthesis section 4 and R-20261021-2 to -7 in the repository's
RESEARCH.md.

## Criteria, in order

1. **Brief fit.** Atomic yes/no checks from the brief: subjects, count, attributes, relations, camera, light,
   style, mood, text, forbidden items. Hard fails are listed separately.
2. **Read and composition.** Thumbnail and greyscale read; focal point (highest local contrast); eye path; balance;
   negative space; placement with a reason (facing into the frame, room ahead of motion). Thirds is never a score.
3. **Value and colour.** Three to five value groups; one light logic; temperature; saturation hierarchy; harmony
   as a choice, not a formula (Itten's schemes predict nothing; Albers's relativity holds).
4. **Rendering integrity** (a gate, not taste). Anatomy and hands; duplicated or merged objects; text; seams;
   perspective; mixels.
5. **Style coherence.** One consistent style; it matches the movement or reference asked for, by named traits.
6. **Expressive intent.** Mood and story match the brief, including briefs that ask for rough or "ugly" work.

## Procedure

1. Cold read before the brief: what the image shows, the three things the eye goes to first.
2. Per-criterion notes for each image, each tied to a visible region.
3. Output: `{"winner": 1|2|"tie", "confidence": "low"|"medium"|"high", "decisive_criteria": [...]}`.

## Abstain (tie, flagged for a human)

- The two orders disagree.
- Both images fail the same gate.
- Confidence is low on every decisive criterion.

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
