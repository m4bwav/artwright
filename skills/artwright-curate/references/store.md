# Stores and formats

Where artwright keeps what it learns, and the exact record formats `aw.py` reads and writes.

Back to [SKILL.md](../SKILL.md).

## Private: `ARTWRIGHT_HOME` (default `~/.artwright`)

```
~/.artwright/
  verdicts.jsonl            aw.py cache put; one row per judged image and rubric
  taste.md                  the user's stated likes and dislikes, dated
  calibration/labels.jsonl  aw.py cache label; the user's own pairwise picks
  keywords/<model>.md       prompt words that worked or failed on a model, with run and date
  palettes/<slug>.json      Lospec palettes fetched on request
```

`verdicts.jsonl` row:

```json
{"key": "<sha256>|artwright-judge|1|<model>|1", "sha256": "...", "file": "...", "rubric": "artwright-judge",
 "rubric_version": "1", "model": "claude-opus-5-5", "prompt_version": "1", "verdict": {...}, "at": "..."}
```

The key is the image SHA-256, the rubric id and version, the judge model and the prompt version: change any one
and the image is judged afresh.

`calibration/labels.jsonl` row:

```json
{"a": {"file": "...", "sha256": "..."}, "b": {"file": "...", "sha256": "..."}, "pick": "a", "by": "human",
 "note": "warmer light, clearer face", "at": "..."}
```

## Per batch: `<folder>/artwright/`

```
artwright/
  verdict.json      the contract callers read (../../artwright-judge/references/verdict-contract.md)
  pairs.jsonl       aw.py compare prepare: pair id, the two files and hashes, which side is 1 in each order
  matches.jsonl     aw.py compare record: one row per judged order (pick, winner side, confidence, criteria)
  pairs/*.png       the two-up images, labelled 1 and 2, no file names
```

`aw.py cache agreement <folder>/artwright ...` reads `pairs.jsonl` and `matches.jsonl` across batches and the
labels file, and reports:

- `both_orders_agreement`: share of pairs whose two orders picked the same image (target 0.8 or above);
- `accuracy_vs_labels`: share of labelled pairs where the resolved verdict matches the user's pick;
- `requery_disagreement`: share of repeated judgements of the same order that changed (the noise floor).

## Public: the repository

Each knowledge file opens with a title, its purpose, a checked date and a back link. Rows carry a source and
`verified: yes|no`. Findings go to RESEARCH.md as `R-` entries; edits to CHANGELOG.md as `C-` entries.
