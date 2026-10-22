# artwright handoff

Updated 2026-10-21 (end of the Step 1 session).

## State

- Step 1 (creation pass) is done. No repository, no code, no skills yet: by design, until Mark answers the forks.
- Research: eight reports in [research/2026-10-21-creation-pass/](research/2026-10-21-creation-pass/index.md),
  synthesis [research/2026-10-21-creation-pass.md](research/2026-10-21-creation-pass.md) (layout, rubric, gold
  answers, eval plan, size budget, forks), 22 `R-` entries in [../RESEARCH.md](../RESEARCH.md).
- Rulings R1–R8: [decisions/2026-10-21-step1-rulings.md](decisions/2026-10-21-step1-rulings.md).
- Name `artwright` is free on GitHub, PyPI and npm (checked 2026-10-21).

## Mark's answers (2026-10-21)

All four forks as recommended: no aesthetic model in v1; he labels 30–50 pairs in Step 3; one-line hand-offs in
comfyui-gen and polywright in Step 3; living-artist names rewritten into traits. See
[decisions/2026-10-21-forks-mark.md](decisions/2026-10-21-forks-mark.md).

## Next

Step 2: build the four skills and `aw.py` to the synthesis, with unit tests and the cheap eval
tier; create the public repository m4bwav/artwright with SECURITY.md and private vulnerability reporting; push
through pull requests; install as artwright@mark-local; register the evergreen units and ai-docs with everlast.
Prompt: [next-session-prompt.md](next-session-prompt.md).

## Things learned that the build must not forget

- The Met v1 search is retired (410); use v1.1. AIC needs an `AIC-User-Agent` header. Getty SPARQL refuses scripts.
- The oldest-painting gold changed in January 2026; re-check golds by 2027-04-19.
- `claude plugin eval` does not attach `@path` images; use `context.add_dirs` with Read. Bash cases need WSL2 or Linux.
- Pin the Python 3.9 Linux CI job to ubuntu-24.04.
- Open questions are listed in RESEARCH.md; unverified non-Western rows must ship as `verified: false`.

## Read first

1. [next-session-prompt.md](next-session-prompt.md).
2. The synthesis, then the decisions folder and [log.md](log.md).
