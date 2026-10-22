# artwright handoff

Updated 2026-10-22 (end of the Step 4 session).

## State

- Public repository https://github.com/m4bwav/artwright; installed as artwright@mark-local 0.1.0; not released.
- PR #7 (0.1.1 bump, CHANGELOG release line, exit codes in README and AGENTS.md) passed CI and waits for the
  owner (the session's permission classifier refused the merge). After it merges: tag `v0.1.1`, check the zip on
  the release page, reinstall artwright@mark-local.
- Calibration done: 40 of 40 labelled; judge accuracy vs owner 0.825 (passes 0.8), both-orders agreement 0.775
  (does not). Taste notes in the private studio's `taste.md`; ruling D1.
- A/B done once (T-20261022-5): with 17/20, without 12/20, +25 points inside the 27-point margin; tool verdict CUT,
  paired 5-0 says keep (D5). Eval spend for the day $44.24.
- Wiki: tie known issue replaced by the fixed behaviour; still says 0.1.0 "not yet released" (footer, Home, FAQ,
  Development) until the tag.
- Hand-off PRs still wait for the owner: m4bwav/comfyui-gen#82, m4bwav/polywright#24.

## Waiting for Mark

- Merge PR #7, then the tag (or tell the next session to merge and tag).
- The two hand-off PRs.

## Next

Release 0.1.1 once PR #7 is merged; then the wiki's release pass (Versions page, "not yet released" lines). Open
finding: the with arm of action-palette tried to edit the repo's LEARNINGS.md; find the instruction. Optional
A/B top-up (`--runs 3` on the 8 differing cases, about $6). Prompt: [next-session-prompt.md](next-session-prompt.md).

## Things learned that the next session must not forget

- `evergreen.py worth --ab` takes one skill folder (`skills/artwright`), not the plugin root; it tracks only that
  skill's firing, so cases owned by judge and pixel show "never fired".
- The A/B run records keep no per-run skill trace; the run folders are under the system temp folder (do not walk
  AppData; read only the exact `aggregate-result.json` path the run prints).
- Eval loops go in a `.sh` file run as `wsl -d Ubuntu -- bash /mnt/...` (L-003). The LLM grader sees only the last
  message.
- Artifact pages: embed images as data URIs. Descriptions at ~596 of 600 tokens: trim before adding (L-002).
- `gh pr merge` can be refused by the auto-mode classifier even with the owner's go-ahead; assign and label then.

## Read first

1. [next-session-prompt.md](next-session-prompt.md), then [log.md](log.md) (last entry).
2. [decisions/2026-10-22-step4-rulings.md](decisions/2026-10-22-step4-rulings.md), `TESTS.md` (T-20261022-5).
