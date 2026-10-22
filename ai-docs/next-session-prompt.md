# Kickoff: artwright Step 3 (prove, calibrate, connect, launch)

Written 2026-10-21 at the end of Step 2. Paste this into a fresh session started in the artwright folder (the
m4bwav/artwright clone). Step 2 is done: the repository is public, the build is merged, the cheap eval tier passes
and the plugin is installed as artwright@mark-local.

## Read first

1. `ai-docs/HANDOFF.md`, then the last entry of `ai-docs/log.md`.
2. `ai-docs/decisions/2026-10-21-step2-build.md` (B1–B10), and the synthesis
   `ai-docs/research/2026-10-21-creation-pass.md` section 6 (eval plan) and section 4 (rubric).
3. `TESTS.md`, `LEARNINGS.md` (L-001 harness, L-002 descriptions), `evals/evals.json` (the paid-tier cases).
4. The owner's rules: the vault user PROFILE ("Code and repos"); the vault sidecar note
   `projects/artwright/private/notes/2026-10-21-private-setup.md`.
5. Sibling shapes: `../historywright` (wiki, release, worth A/B records in its TESTS.md), `../musicwright` (studio),
   `../polywright` (`references/contract.md`, where the hand-off line goes).

## Step 3

1. **Ask Mark first** (one short question each, plain words): merge PR #3 (release workflow)? Is local MiniMax H3
   use covered by its licence (R-20261021-27)? Then go on; do not wait for the answers to do the rest.
2. **Paid evals and the A/B.** `python evals/fixtures/make_fixtures.py --net --emit-scaffold`, then the 18 paid
   cases under WSL2 (`scripts/eval-wsl.sh "outcome-*" --judge-model sonnet --max-cost-usd N`, same for `guard-*`).
   Image cases need the fixtures in the run's workspace: extend the scaffold to carry the Cleveland images (fetch
   in the scaffold with the pinned hashes, or `context.add_dirs`; check which works on the pinned harness with one
   probe case first). Then `evergreen.py worth --ab` for the with/without comparison. Record T- entries, fix
   failures with `evergreen-tune` (three iterations at most). Budget: say the estimate and stop before spending
   more than about $40 in all.
3. **Calibration with Mark (fork 2).** Build the labelling page: one pair at a time, side by side, "which of these
   two?" plus an optional why, 30–50 pairs (degraded CC0 pairs from `aw.py degrade`, real comfyui-gen batches,
   and a few ties). Use an Artifact with stored answers (load `artifact-capabilities`), then write the picks with
   `aw.py cache label` into ARTWRIGHT_HOME and run `aw.py cache agreement`. Report agreement against the 0.8 target.
4. **Hand-offs (fork 3).** One line in comfyui-gen's skill ("after a batch, call artwright-judge; it writes
   artwright/verdict.json") and one in polywright's (concept art before image-to-3D and turnaround renders), each
   its own pull request in its own repository, pointing at `skills/artwright-judge/references/verdict-contract.md`.
5. **Launch set.** README banner (comfyui-gen, 1536x640, four seeds on a contact sheet, `.github/images/banner.jpg`
   with the workflow, prompt and seed beside it; judge the four with artwright-judge itself); GitHub wiki
   (wikiwright; the first page must be saved in the web interface before a push works).
6. **Release.** Only after Mark merges PR #3 and says go: bump nothing unless files changed since 0.1.0's notes,
   tag `v0.1.0`, verify the release zip.

Limits: no release tag without Mark's go-ahead. No new image models or torch. Calibration images must be CC0 or
the owner's own renders. Estimate in files, lines, size and agent hours.

## Rules

- No AI attribution in commits, PRs or files. Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`.
- Every change through a pull request; merge your own once CI passes, except release or publish workflow changes,
  public API changes (the verdict contract) and other repositories' shared files; those wait for Mark (assign
  m4bwav, label needs-review).
- Public repository: no absolute paths from this machine, no names, no keys in any file, ai-docs included.
- Image generation: split batches across both ComfyUI hosts (comfyui-gen). Kill processes only by PID. Never
  index or walk AppData.
- The Bash tool's hook refuses heredocs holding a doubled backslash: use a scratch .py file or the Edit tool.
- Shell eval cases run only under WSL2 (L-001); re-run the decoys after any description edit (L-002).

## When to stop and ask

- Before spending more than about $40 on evals, paying for or signing up to anything, or installing a large
  dependency.
- Before tagging or publishing.
- At the end of Step 3: report the eval and A/B results, the calibration agreement, the hand-off PRs, the banner
  and wiki, and the release state.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
