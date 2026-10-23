# The verdict contract: `artwright/verdict.json`

How other plugins read artwright's judgement. A caller (comfyui-gen after a batch, polywright after a turnaround
render, brandwright after ranking mock-ups) hands artwright-judge a folder of images and a brief; artwright writes
one file, `<folder>/artwright/verdict.json`, and nothing else in the caller's folder. It never edits the caller's
own files (polywright's `manifest.json` included). Version `1`; a breaking change bumps `artwright` and the
plugin's minor version.

Back to [SKILL.md](../SKILL.md).

## Calling

```
python <plugin>/skills/artwright/scripts/aw.py verdict init <folder> <images...> --kind pairwise --brief "..."
```

then "after a batch, call artwright-judge on <folder> with the brief". When done, `status` is `final` and
`aw.py verdict validate <folder>` prints `valid: true`.

## Shape

```json
{
  "artwright": "1",
  "kind": "pairwise",
  "brief": "red fox in snow at dusk, side view, no text",
  "rubric": {"id": "artwright-judge", "version": "2"},
  "judge": {"model": "claude-opus-5-5", "prompt_version": "1"},
  "created": "2026-10-21T21:00:00",
  "updated": "2026-10-21T21:20:00",
  "status": "final",
  "items": [{"id": "A", "file": "renders/fox_001.png", "sha256": "..."}],
  "ranking": [{"file": "renders/fox_003.png", "rank": 1, "strength": 2.4, "wins": 5, "losses": 1, "ties": 0,
               "close_to_next": false}],
  "fit": [{"id": "A", "verdict": "FITS WITH FIXES", "hard_fails": [],
           "checks": [{"check": "one fox", "pass": true, "region": "centre"}]}],
  "fixes": [{"id": "A", "channel": "prompt", "fix": "light comes from above; the brief asks for dusk",
             "prompt": {"model": "z-image-turbo", "text": "...", "diff": "+ low sun from the left"}}],
  "abstained": [{"files": ["renders/fox_002.png", "renders/fox_004.png"], "reason": "orders disagree"}],
  "notes": ""
}
```

## Rules for both sides

- `kind`: `pairwise`, `brief-fit`, `critique` or `pixel`.
- Paths are relative to the folder that holds `artwright/`, with forward slashes.
- `items[].sha256` lets a caller see whether a file changed after the verdict; `validate` reports a mismatch.
- `fit[].verdict`: `FITS`, `FITS WITH FIXES` or `DOES NOT FIT`; `DOES NOT FIT` lists `hard_fails`.
- `fixes[].channel`: `prompt`, `setting`, `control`, `reference`, `inpaint` or `model`.
- `close_to_next: true` means the order between that row and the next is not established; the last row has `null`
  (there is no next row).
- `abstained` lists pairs a human should see. A caller must not silently pick between them.
- No absolute score unless the user asked; then `score` with `score_anchors` (three labelled references).
- Working files beside it (`pairs.jsonl`, `matches.jsonl`, `pairs/*.png`) are artwright's own; callers ignore them.
