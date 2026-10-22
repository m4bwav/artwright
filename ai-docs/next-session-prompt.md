# Kickoff: artwright Step 4 (calibration result, A/B, release)

Written 2026-10-22 at the end of Step 3. Paste this into a fresh session started in the artwright folder (the
m4bwav/artwright clone). Step 3 is mostly done: the paid evals ran and were tuned, the banner and wiki are live, the
two hand-off PRs wait for Mark, and his calibration labelling is in progress.

## Read first

1. `ai-docs/HANDOFF.md`, then the last entry of `ai-docs/log.md`.
2. `ai-docs/decisions/2026-10-22-step3-rulings.md` (C1–C8) and `TESTS.md` (T-20261022-1 to -4).
3. `LEARNINGS.md` (L-001 harness, L-002 descriptions, L-003 eval loops in a script file).
4. The owner's rules: the vault user PROFILE ("Code and repos"); the vault sidecar note
   `projects/artwright/private/notes/2026-10-21-private-setup.md`. The calibration folder is the sidecar's
   `studio/calibration/` (ARTWRIGHT_HOME is the sidecar's `studio/`).

## Step 4

1. **Calibration result.** Read the labelling page's picks: ArtifactData `list` on
   https://claude.ai/artifact/TFZxKLEmSr41WXP1Gszs23, collection `picks`, `query.limit` 100, with `out_dir` set to a
   scratch folder. If fewer than 40, tell Mark how many remain and stop for him. Then
   `python <studio>/calibration/import_picks.py <out_dir>/picks` writes the labels and prints the agreement.
   Report both numbers: the judge's both-orders agreement (0.775 on this set) and its accuracy against his picks,
   against the 0.8 target, broken down by pair kind (degraded, pixel, his seed pairs, ties) from the manifest.
   If below target, record what the disagreements share (one ruling in `ai-docs/decisions/`), and note the
   taste lessons in `studio/taste.md` through artwright-curate; do not change public rubric files on taste
   alone.
2. **A/B, only if Mark agreed.** `python evals/fixtures/make_fixtures.py --net`, then
   `python <evergreen>/scripts/evergreen.py worth . --ab --runs 1` (about $10; Step 3 spent $33.99 of its $40).
   Record a T- entry with the gain and the noise margin.
3. **Wiki follow-up.** The tie fix merged, so update the wiki's known-issues line (the note
   `ai-docs/notes/2026-10-22-github-wiki.md` says where), and fix any doc mismatches still listed there.
4. **Release, only when Mark says go.** Packaged files changed since 0.1.0 was installed: bump to 0.1.1 in the
   manifest, write the CHANGELOG release line, tag `v0.1.1`, check the release zip on the release page, then
   reinstall artwright@mark-local.

Limits: no release tag without Mark's go-ahead. No new image models or torch. Calibration images must be CC0 or
the owner's own renders. Estimate in files, lines, size and agent hours. Eval spend: say the estimate and stop
before about $15 this session.

## Rules

- No AI attribution in commits, PRs or files. Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`.
- Every change through a pull request; merge your own once CI passes, except release or publish workflow changes,
  public API changes (the verdict contract) and other repositories' shared files; those wait for Mark (assign
  m4bwav, label needs-review).
- Public repository: no absolute paths from this machine, no names, no keys in any file, ai-docs included. The
  calibration manifest and his picks stay in the private studio folder.
- Image generation: split batches across both ComfyUI hosts (comfyui-gen). Kill processes only by PID. Never
  index or walk AppData.
- The Bash tool's hook refuses heredocs holding a doubled backslash: use a scratch .py file or the Edit tool.
- Shell eval cases run only under WSL2 (L-001); eval loops go in a script file (L-003); re-run the decoys after
  any description edit (L-002). The LLM grader sees only the last message.

## When to stop and ask

- Before spending more than about $15 on evals, paying for or signing up to anything, or installing a large
  dependency.
- Before tagging or publishing.
- At the end of Step 4: report the calibration numbers, the A/B, the wiki fix and the release state.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
