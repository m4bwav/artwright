# Kickoff: artwright Step 2 (build)

Written 2026-10-21 at the end of Step 1. Paste this into a fresh session started in
the artwright folder. Step 1 (the creation pass) is done; no repository or code exists yet.

## Mark's answers (2026-10-21): all four as recommended

Recorded in `ai-docs/decisions/2026-10-21-forks-mark.md`. Build to them:

1. No local aesthetic-scoring model in v1. No torch and no model download. Name the GPU reward models (HPSv3,
   UnifiedReward) only as pointers.
2. Mark will label 30–50 image pairs in Step 3, one pair at a time, about 15 minutes. In Step 2, build the storage
   for them: `calibration/` under `ARTWRIGHT_HOME` and the agreement metrics in `aw.py rank` or `cache`.
3. Step 3 adds one-line hand-offs ("after a batch, call artwright-judge") in comfyui-gen and polywright, each as its
   own pull request. In Step 2, write artwright-judge's description and its `artwright/verdict.json` contract so
   those hand-offs have something stable to point at.
4. A living artist named in a prompt is rewritten into traits (medium, palette, line, subject, era), with one line
   saying so; never refused. Public-domain masters, movements and studio genres may be named (ruling R7).

## Read first

1. `ai-docs/HANDOFF.md`, then the synthesis `ai-docs/research/2026-10-21-creation-pass.md` in full (layout, rubric,
   gold answers, eval plan, size budget). Open the raw reports in `ai-docs/research/2026-10-21-creation-pass/` only
   for the section you are building.
2. `RESEARCH.md` (22 `R-` entries; open questions), `ai-docs/decisions/2026-10-21-step1-rulings.md` (R1–R8) and
   `ai-docs/decisions/2026-10-21-forks-mark.md`.
3. The owner's rules: the vault user PROFILE (`everlast.py vault where` prints the vault), section "Code and repos".
4. Sibling models of shape: `..\historywright` (AGENTS.md, hw.py layout, tests, evals, CI workflow), `..\musicwright`
   (the private studio under `MUSICWRIGHT_HOME`, `tests/check_skills.py` guarding paths), `..\polywright`
   (`pw.py` one-JSON-per-command style, the asset folder artwright writes `artwright/verdict.json` into).
5. The evergreen skills `evergreen-new` (for each new skill) and the protocol's §11 on testing.

## Step 2: build, test, publish, install

1. Repository: `m4bwav/artwright`, public, created with README stub, LICENSE (as the siblings), SECURITY.md (the
   tiered template from package-modernize; private vulnerability reporting on), CHANGELOG, AGENTS.md and CLAUDE.md
   (`@AGENTS.md` first line), `.github/copilot-instructions.md` pointer. Every later change goes through a pull
   request.
2. Skills (ruling R3): `artwright` (hub), `artwright-judge`, `artwright-pixel`, `artwright-curate`, each with the
   evergreen layer through `evergreen-new`, descriptions that state the sibling boundaries in synthesis section 2,
   and the guards in section 4.
3. `aw.py` (ruling R4): the commands in the synthesis table, stdlib first, Pillow optional, Python 3.9+, one JSON
   object per command. Start with `doctor`, `info`, `fit`, `sheet`, `pixel`, `palette`, `hash`/`dedupe`,
   `compare`, `rank`, `cache`, `degrade`; `stats` last. Keep `aw.py` under 100 KB.
4. Knowledge files: the table in synthesis section 3, inside the size budget. Rows not backed by a fetched source
   ship `verified: false` (the non-Western tracks especially). Verify the Hasler–Süsstrunk thresholds and the
   Lospec terms before shipping those parts.
5. Tests: stdlib unit tests with fixtures built in code; `tests/check_skills.py` for paths, names and sizes. Evals:
   the cheap tier (8 trigger, 3 decoy, 3 action cases) in `evals/cases/`; write the paid-tier cases but run them in
   Step 3. Museum fixtures fetched by accession number with pinned hashes (ruling R5).
6. CI: ubuntu, macOS, Windows on Python 3.9 and 3.14; pin the 3.9 Linux job to `ubuntu-24.04`.
7. Install as `artwright@mark-local`; register the evergreen units and the ai-docs with everlast.
8. Propose the new art sources to historywright-sources as a pull request in that repository (ruling R6): Getty
   Provenance CSV, Museo Egizio, the link-out price databases, the Met v1.1 and AIC header notes.

Limits: no banner, wiki or paid evals yet (Step 3). No release tag without Mark's go-ahead. Estimate in files,
lines, size and agent hours.

## Rules

- No AI attribution in commits, PRs or files. Commit with `git -c user.email=156112+m4bwav@users.noreply.github.com`.
- Merge your own PRs when CI passes, except changes to a release or publish workflow or a public API; those wait
  for Mark (assign m4bwav, label needs-review).
- Public repository: no absolute paths from this machine, no names, no keys in any file, ai-docs included.
- Image generation for tests: split batches across both ComfyUI hosts (comfyui-gen). Kill processes only by PID.
  Never index or walk AppData.
- The Bash tool's hook refuses heredocs holding a doubled backslash: use a scratch .py file or the Edit tool.
- Research subagents: cap each at about 25 web searches and prefer direct API fetches.

## When to stop and ask

- Before paying for or signing up to anything, requesting a key, or installing a large dependency (torch, a model).
- Before calling any live source faster than its published terms allow.
- At the end of Step 2: report the repository URL, merged PRs, test and eval results, and the install.

Decide small design rulings yourself, record each in `ai-docs/decisions/`, and flag it in one line.

## Last paragraph (keep it in every rewrite)

At each milestone, and before you finish, write what you learned to the repo's `ai-docs/`: the log, a HANDOFF of 50 lines at most, and decisions and research notes. Then rewrite this file, `ai-docs/next-session-prompt.md`, as the prompt for the next fresh session: what to read first, the next step and its limits, the rules, and when to stop. End the new prompt with this same paragraph, and paste it in your final message.
