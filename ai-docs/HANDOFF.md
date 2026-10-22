# artwright handoff

Updated 2026-10-21 (end of the Step 2 session).

## State

- Public repository https://github.com/m4bwav/artwright. main at the PR #2 merge (2a9c1b3) plus the end-of-session
  records PR. Installed as artwright@mark-local 0.1.0; not released or tagged.
- Four skills (hub, judge, pixel, curate), `aw.py` (stdlib, Pillow optional, 14 commands), knowledge files with
  verified flags, 34 offline unit tests, structure and budget checks, CI on 3 OSes x Python 3.9 and 3.14.
- Evals: cheap tier 14/14 (42/42 runs, T-20261021-4). Paid tier (18 outcome and guard cases) written, not run.
  No A/B baseline yet.
- Evergreen unit registered (moderate, 60 days, due 2026-12-20; volatile claims: law.md 45 d, model profiles 60 d,
  market golds 180 d). ai-docs registered with everlast (mode repo, sync pr).
- ARTWRIGHT_HOME is the vault sidecar's `studio/` on the owner's PC (private note in the sidecar).

## Waiting for Mark

- PR #3, the release workflow (assigned, `needs-review`): publish workflows wait for him.
- Tag v0.1.0 only on his go-ahead, after PR #3.
- MiniMax H3 licence: its Community License form names USA/EU/UK/South Korea; whether local use needs approval is
  open (R-20261021-27). Flagged to him.

## Next (Step 3)

Banner, paid evals and the A/B, Mark's 30–50 calibration pairs, the two hand-off PRs (comfyui-gen, polywright),
wiki, then a release when he says go. Prompt: [next-session-prompt.md](next-session-prompt.md).

## Things learned that the next session must not forget

- Shell eval cases: WSL2 + pinned 2.1.281 + `--scaffold` (`scripts/eval-wsl.sh`); graders name `tool: Bash`;
  regenerate scaffolds with `python evals/fixtures/make_fixtures.py --emit-scaffold` after changing fixtures (L-001).
- Descriptions: a broad trigger noun needs its neighbours' owners named beside it; re-run decoys after any
  description edit (L-002). The descriptions budget is at ~594 of 600 tokens: trim before adding.
- `Path.write_text(newline=)` does not exist on Python 3.9; write through `open()`.
- The eval sandbox has no sibling plugins, so decoys there are stricter than real use.
- Golds to re-check by 2027-04-19; Basquiat and Clemente as neo-expressionists still unverified by a fetched source.

## Read first

1. [next-session-prompt.md](next-session-prompt.md), then [log.md](log.md) (last entry).
2. [decisions/2026-10-21-step2-build.md](decisions/2026-10-21-step2-build.md), the synthesis section 6 (eval plan).
