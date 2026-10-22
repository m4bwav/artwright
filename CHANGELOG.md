# Changelog: artwright

Every change to [README.md](README.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

## Releases

- unreleased: C-20261021-1 to C-20261021-2 (0.1.0 waits for the owner's go-ahead).

## Changes

### C-20261021-2 · 2026-10-21 · Step 2 build: four skills, aw.py, knowledge files, tests, evals, CI
- because: user request (kickoff Step 2); R-20261021-1 to -30; ai-docs/decisions/2026-10-21-step2-build.md
- files: skills/artwright (SKILL.md, scripts/aw.py, references/), skills/artwright-judge, skills/artwright-pixel, skills/artwright-curate, tests/test_aw.py, tests/check_skills.py, scripts/budget.py, evals/, .github/workflows/tests.yml, README.md, AGENTS.md
- The hub (critique, style and movement, theory, facts), the judge (pairwise in both orders, Bradley-Terry, brief fit, prompt fixes, the verdict contract), pixel checks and the curator, on a standard-library aw.py with Pillow optional. Knowledge rows carry sources, dates and verified flags.

### C-20261021-1 · 2026-10-21 · Created as an evergreen unit
- because: user request
- files: README.md, RESEARCH.md, LEARNINGS.md, evergreen.json, TESTS.md, evals/evals.json
- Initial version. Tier `moderate`, interval 60 days (the synthesis). See R-20261021-1 for the research basis.
