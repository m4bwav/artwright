# Learnings: artwright

Procedural lessons for [README.md](README.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-006 · 2026-10-22 · Trim a museum photograph's mat before any border measure
- Trigger: `comp` flagged tangents, border pull and a blocked entrance on four of seven Cleveland images; every one was the paper, mat or grey backdrop round the work, not the art.
- Hypothesis: collection photographs frame the object with a uniform margin; a border measure reads that margin's edge as a contour on the frame. AI stills have dark vignettes and plain skies that look the same to a loose test.
- Rule: trim only when all four sides have a uniform band that ends before an eighth of the side and three of them are light; report what was trimmed (`margin_trimmed`).
- Evidence: ai-docs/decisions/2026-10-22-books-track5.md E3
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-005 · 2026-10-22 · A degrade kind must force its direction, never match a target
- Trigger: on six real images, `haze-off` lowered the far band's contrast on four. It matched the far band to the near one, and there the far band was already crisper. `tangent` drew a black line that vanished on a dark poster. The synthetic tests passed.
- Hypothesis: a degradation defined as "make A equal B" moves either way depending on where the image starts; only "push A past B" is a broken input on every image.
- Rule: define each kind as a push with a floor (at least 1.3 times; ink opposite the mean). Check it on real images as well as the drawn fixture.
- Evidence: ai-docs/decisions/2026-10-22-books-track5.md E5
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-004 · 2026-10-22 · Set a new flag's threshold from how often it fires on real images
- Trigger: thresholds taken from the book notes flagged `competing_focal` on 32 of 48 AI stills, `frame_tangent` on 31 and `blocked_entrance` on all seven museum works.
- Hypothesis: a sketch's threshold is a guess about one picture; a pointer that fires on most pictures carries no information, whatever its theory.
- Rule: before shipping a flag, run it over a mixed real set (museum works and AI stills) and set the threshold so it fires on a minority. Publish the rate beside the rule, labelled uncalibrated until owner labels exist.
- Evidence: ai-docs/decisions/2026-10-22-books-track5.md E2
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-003 · 2026-10-22 · Put a looping eval batch in a script file; never inline `$var` in `wsl -- bash -lc '...'`
- Trigger: `wsl -d Ubuntu -- bash -lc 'for c in a b c; do bash scripts/eval-wsl.sh "$c" ...; done'` from PowerShell ran the whole suite on every pass: `$c` arrived empty, `eval-wsl.sh` fell back to its `*` default, and four full-suite passes spent about $14 before it was stopped.
- Hypothesis: wsl.exe hands the joined command line to the distribution's login shell, which expands `$c` once before `bash -lc` runs the loop.
- Rule: write the loop to a `.sh` file and run `wsl -d Ubuntu -- bash /mnt/<path>/file.sh`; a case glob has no character classes either (one family per call).
- Evidence: T-20261022-2
- Scope: repo:artwright, env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-002 · 2026-10-21 · Name the cheap mechanical jobs in the description, and name who owns their neighbours
- Trigger: "main colours and their shares" and "show these side by side" never fired a skill (0/3 each): the model wrote PIL scripts. Adding colours and contact sheets to the hub description fixed it, and at once pulled brand-palette and website requests in (2 of 9 decoy runs) until brandwright and sitewright-direction were named as owners.
- Hypothesis: a model only reaches for a skill for a job it believes it cannot do alone; plain image chores look easy, so the description must name them. Naming a broad noun (colours) widens the catch, so the exclusion must sit beside it.
- Rule: when a description adds a broad trigger noun, add the sibling that owns its neighbours in the same edit, and re-run the decoys.
- Evidence: T-20261021-3, C-20261021-3
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-21

### L-001 · 2026-10-21 · Shell eval cases need WSL2, a scaffold and `tool: Bash`
- Trigger: the action cases failed three ways in one session: native Windows refused the Bash grant (no sandbox backend); under WSL2 each run started in an empty workspace, so the fixture paths did not exist; and the `tool_used` grader with `tool: Bash|PowerShell` counted 0 calls although Bash ran.
- Hypothesis: `claude plugin eval` runs each case in a fresh temporary home and cwd, matches `tool` as a literal name, and needs an OS sandbox for shell tools. 2.1.307 makes every Bash path read-only in eval runs (a sibling plugin's finding), so the pinned 2.1.281 copy under WSL is the working harness.
- Rule: shell cases run under WSL2 with `~/.local/share/claude-pinned/claude-2.1.281 plugin eval . --scaffold --allow-tools Bash ...`; each case carries `case.yaml` with `context.scaffold_script: fixture.sh` (written by `python evals/fixtures/make_fixtures.py --emit-scaffold`); graders name `tool: Bash`.
- Evidence: T-20261021-2
- Scope: repo:artwright, env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-21

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-21 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261021-1, T-20261021-1, confirmed 2026-10-21
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-21
-->
