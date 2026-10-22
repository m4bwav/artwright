# Changelog: artwright

Every change to [README.md](README.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

## Releases

- unreleased: C-20261021-1 to C-20261022-3 (0.1.0 waits for the owner's go-ahead).

## Changes

### C-20261022-3 · 2026-10-22 · Banner, wiki, doc fixes, calibration records
- because: user request (Step 3 launch set); the wiki pass's mismatch list (ai-docs/notes/2026-10-22-github-wiki.md)
- files: README.md (banner, credit), .github/images/ (workflow, prompt, four seeds, contact sheet, banner-verdict.json), skills/artwright/references/cli.md (exit 2 on usage errors, `--version`, `sheet --cell 384`, `pixel --tol 24`), skills/artwright-judge/references/verdict-contract.md (`close_to_next` is null on the last row), ai-docs (rulings C1-C8, wiki note), scripts/eval-wsl.sh (refuses an empty case glob, L-003)
- The banner was picked by artwright-judge from four Z-Image Turbo seeds. The wiki (10 pages) is live; its source note and verification script are in ai-docs/notes.

### C-20261022-2 · 2026-10-22 · Paid-tier fixes: taste calls, regions, AI-made, prompt rewrites; graders read only the reply
- because: T-20261022-1, T-20261022-3, T-20261022-4
- files: skills/artwright/SKILL.md (description: "is this AI-made"; guards: open with "pixels cannot tell", a file name is not provenance, never ask a living artist's name), skills/artwright-judge/SKILL.md (description: prompt rewrites into a style or artist, shorter pair wording; "Why two at a time": agreeing orders are not a wide call, taste between two intact works is said to be close; "Hand back": each reason tied to its region), skills/artwright-curate/SKILL.md (description trimmed one example for the budget), evals (graders for brief-fit, ming-price, pairwise-orders, golden-ratio, ai-generated; `files` on image cases for `worth --ab`; scaffolds fetch museum images), evals/fixtures/make_fixtures.py
- Descriptions at ~596 of 600 tokens; triggers 8/8 and decoys re-run on the new text.

### C-20261022-1 · 2026-10-22 · A tie in both orders is a tie
- because: the calibration run (rulings C5); found again by the wiki pass
- files: skills/artwright/scripts/aw.py (`resolve`), tests/test_aw.py (test_tie_both_orders)
- Both orders saying tie returned `decided` with no winner: `rank` counted it as a win and `cache agreement` crashed.

### C-20261021-3 · 2026-10-21 · Descriptions catch colours and contact sheets and name brandwright and sitewright; shell evals scaffolded
- because: T-20261021-2, T-20261021-3, L-001, L-002
- files: skills/artwright/SKILL.md (description; Image handling), skills/artwright-judge/SKILL.md (description), skills/artwright-curate/SKILL.md (description, shortened for the budget), evals/cases/action-*/ (case.yaml, fixture.sh, graders), evals/fixtures/make_fixtures.py (--emit-scaffold), tests/check_skills.py (.sh files checked; base64 fixtures exempt from the token check)
- The hub now names colour questions and contact sheets and says to answer them from aw.py; the hub and judge name the siblings that own brand palettes and website direction; the action cases unpack their fixtures in the run's workspace.

### C-20261021-2 · 2026-10-21 · Step 2 build: four skills, aw.py, knowledge files, tests, evals, CI
- because: user request (kickoff Step 2); R-20261021-1 to -30; ai-docs/decisions/2026-10-21-step2-build.md
- files: skills/artwright (SKILL.md, scripts/aw.py, references/), skills/artwright-judge, skills/artwright-pixel, skills/artwright-curate, tests/test_aw.py, tests/check_skills.py, scripts/budget.py, evals/, .github/workflows/tests.yml, README.md, AGENTS.md
- The hub (critique, style and movement, theory, facts), the judge (pairwise in both orders, Bradley-Terry, brief fit, prompt fixes, the verdict contract), pixel checks and the curator, on a standard-library aw.py with Pillow optional. Knowledge rows carry sources, dates and verified flags.

### C-20261021-1 · 2026-10-21 · Created as an evergreen unit
- because: user request
- files: README.md, RESEARCH.md, LEARNINGS.md, evergreen.json, TESTS.md, evals/evals.json
- Initial version. Tier `moderate`, interval 60 days (the synthesis). See R-20261021-1 for the research basis.
