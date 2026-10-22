# artwright handoff

Updated 2026-10-22 (end of the Step 3 session).

## State

- Public repository https://github.com/m4bwav/artwright; installed as artwright@mark-local 0.1.0; not released.
- Evals: cheap tier 14/14; paid tier run and tuned (T-20261022-1 to -4): 28 of 32 cases pass every run;
  pairwise-orders 2/3, ai-generated 1/3, brief-fit 2/3, tie-pair 2/3. Spend so far $33.99. No A/B yet.
- Calibration: the judge's both-orders agreement on the 40-pair set is 0.775 (target 0.8). The owner's labelling
  page is https://claude.ai/artifact/TFZxKLEmSr41WXP1Gszs23 (picks in its `picks` collection, 9 of 40 done when
  the session ended). Set, manifest, judge records and `import_picks.py` are in
  `ARTWRIGHT_HOME/calibration/` (the vault sidecar's `studio/`; images git-ignored there).
- Banner in the README (picked by the judge); wiki live, 10 pages.
- Hand-off PRs wait for the owner: m4bwav/comfyui-gen#82, m4bwav/polywright#24.

## Waiting for Mark

- The rest of his 40 picks; then import and report agreement against 0.8.
- The A/B (`evergreen.py worth --ab`, about $10): it would pass the session's $40 eval cap, so it needs his go.
- The two hand-off PRs; a release tag (only on his go-ahead).

## Next

Import his picks, report agreement; run the A/B if he agrees; refresh the wiki's known-issues line now the tie fix
is merged; then a release when he says go. Prompt: [next-session-prompt.md](next-session-prompt.md).

## Things learned that the next session must not forget

- Eval loops go in a `.sh` file run as `wsl -d Ubuntu -- bash /mnt/...`; `$var` inside `wsl -- bash -lc '...'` is
  expanded away and the runner then ran the whole suite (L-003; the runner now refuses an empty glob). A case glob
  has no character classes.
- The LLM grader sees only the last message: never ask it to confirm a file or a trace.
- Image cases: `make_fixtures.py --net --emit-scaffold`; scaffolds curl the museum images and check their hashes;
  `worth --ab` copies `evals/fixtures/out` via each case's `files`.
- Artifact pages: relative paths to published files did not render as `<img>` in the viewer; embed data URIs.
- Descriptions at ~596 of 600 tokens: trim before adding; re-run decoys after any description edit (L-002).
- Don't edit a shell script while bash is executing it (it reads by offset).
- Shell eval cases: WSL2 + pinned 2.1.281 + `--scaffold` (L-001).

## Read first

1. [next-session-prompt.md](next-session-prompt.md), then [log.md](log.md) (last entry).
2. [decisions/2026-10-22-step3-rulings.md](decisions/2026-10-22-step3-rulings.md), `TESTS.md` (T-20261022-*).
