# Tests: artwright

Test runs for [README.md](README.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261021-4 · 2026-10-21 · claude plugin eval (triggers, decoys: 2.1.281 Windows; actions: pinned 2.1.281 under WSL2 Ubuntu with --scaffold), --ablation none, sonnet · cheap tier, final text · 14/14 cases, 42/42 runs
- Triggers 8/8 (24/24 runs), decoys 3/3 (9/9), actions 3/3 (9/9) on the descriptions in C-20261021-3. Cost of this round $4.0; the whole session's eval spend $15.76 across 14 runs of the harness.
- No baseline arm yet: the A/B (`evergreen.py worth --ab`) and the paid tier (18 outcome and guard cases) are Step 3.
- led to: none

### T-20261021-3 · 2026-10-21 · claude plugin eval, sonnet · actions 2/3 then 8/9 runs, decoys 1/3 after the colour wording
- action-palette 0/3 and action-sheet 0/3 · undertrigger · no artwright skill fired; the model wrote its own PIL scripts for the colour shares and the contact sheet. After the hub description named colours and contact sheets: palette 3/3, sheet 2/3.
- decoy-brand 2/3, decoy-site 2/3 · overtrigger · the colour wording pulled brand-palette and website-direction requests into the hub (the eval sandbox has no brandwright or sitewright to route to). Fixed by naming both owners in the hub description.
- led to: L-002, C-20261021-3

### T-20261021-2 · 2026-10-21 · claude plugin eval, sonnet · actions 0/3 (harness), decoys 2/3
- Actions under native Windows: refused (no sandbox backend for Bash). Under WSL2 with the pinned 2.1.281: ran, but every run started in an empty workspace (the fixtures were not there), and `tool: Bash|PowerShell` in the grader matched no call. Fixed with a `fixture.sh` scaffold per case (`--scaffold`) and `tool: Bash`; action-pixel then 3/3.
- decoy-brand 0/3 · overtrigger · "score these mock-ups for how on-brand they are" fired the judge. Fixed by naming brandwright in the judge's description; decoys then 3/3.
- led to: L-001, C-20261021-3

### T-20261021-1 · 2026-10-21 · claude plugin eval 2.1.281, --ablation none, sonnet, Windows 11 · triggers 8/8 (24/24 runs)
- First run of the cheap tier's trigger cases on the Step 2 text. $2.07.
- led to: none
