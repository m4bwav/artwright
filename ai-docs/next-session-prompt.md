# Kickoff: artwright Step 5 (release 0.1.1, wiki release pass, loose ends)

Written 2026-10-22 at the end of Step 4. Paste this into a fresh session started in the artwright folder (the
m4bwav/artwright clone). Step 4 is done except the release: calibration imported and reported, the A/B ran once,
the wiki's tie issue is fixed, and PR #7 (the 0.1.1 bump) passed CI but waits for Mark's merge.

## Read first

1. `ai-docs/HANDOFF.md`, then the last entry of `ai-docs/log.md`.
2. `ai-docs/decisions/2026-10-22-step4-rulings.md` (D1–D5) and `TESTS.md` (T-20261022-5).
3. `LEARNINGS.md` (L-001 harness, L-002 descriptions, L-003 eval loops in a script file).
4. `ai-docs/notes/2026-10-22-github-wiki.md` ("Updating the wiki later" and "At the first release").
5. The owner's rules: the vault user PROFILE ("Code and repos"); the vault sidecar note
   `projects/artwright/private/notes/2026-10-21-private-setup.md`.

## Step 5

1. **Release.** If PR #7 is merged (`gh pr view 7`), and Mark has said go: `git pull`, tag `v0.1.1` on that merge
   commit, push the tag, watch the release workflow, check `artwright-0.1.1.zip` on the release page (skills,
   README, LICENSE, SECURITY.md; no ai-docs, no evals), then reinstall artwright@mark-local and confirm 0.1.1
   loads. If PR #7 is still open, ask Mark to merge it (or to allow the merge) and stop for him.
2. **Wiki release pass.** Add a Versions-and-Upgrading page, change "not yet released" on Home, FAQ, Development
   and the footer to 0.1.1 at the tag's commit; run the gates listed in the wiki note, push, `wikiwright.py live`.
3. **Open finding (D5).** In the A/B, action-palette's with arm asked to edit the repository's own LEARNINGS.md
   from its run folder. Find the instruction in the skills that sends it there (the Maintenance sections name
   LEARNINGS.md by relative path) and make it write learnings only when working in the artwright repository.
   Through a PR; re-run the decoys if a description changes (L-002).
4. **Optional A/B top-up.** Only if Mark agrees: `worth skills/artwright --ab --runs 2 --append` on the cases that
   differed or both failed (about $6), and an A/B pointed at `skills/artwright-judge` and `skills/artwright-pixel`
   once they have value cases. Record a T- entry.

Limits: no release tag without Mark's go-ahead. No new image models or torch. Estimate in files, lines, size and
agent hours. Eval spend: say the estimate and stop before about $10 this session (Step 4 spent $10.25).

## Rules

- No AI attribution in commits, PRs or files. Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`.
- Every change through a pull request; merge your own once CI passes, except release or publish workflow changes,
  public API changes (the verdict contract) and other repositories' shared files; those wait for Mark (assign
  m4bwav, label needs-review). If the merge is refused by a permission check, assign and label and say so.
- Public repository: no absolute paths from this machine, no names, no keys in any file, ai-docs included. The
  calibration manifest, his picks and taste.md stay in the private studio folder.
- Image generation: split batches across both ComfyUI hosts (comfyui-gen). Kill processes only by PID. Never
  index or walk AppData.
- The Bash tool's hook refuses heredocs holding a doubled backslash: use a scratch .py file or the Edit tool.
- `worth --ab` takes one skill folder, not the plugin root. Shell eval cases run only under WSL2 (L-001); eval
  loops go in a script file (L-003).

## When to stop and ask

- Before spending more than about $10 on evals, paying for or signing up to anything, or installing a large
  dependency.
- Before tagging or publishing, and when PR #7 is still open.
- At the end of Step 5: report the release state, the wiki pass, the LEARNINGS fix and any A/B.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
