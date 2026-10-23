# Agent rules for artwright

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex, Gemini CLI) working in this repository. `CLAUDE.md`
imports this file and `.github/copilot-instructions.md` points here.

Read [README.md](README.md) first. The four skills live under [skills/](skills/); the hub is `skills/artwright`,
which also holds the CLI (`scripts/aw.py`). Knowledge files sit in each skill's `references/`. The four skills
share one evergreen unit at the repository root: RESEARCH, CHANGELOG, LEARNINGS, TESTS, `evals/evals.json`,
MAINTENANCE and `evergreen.json`.

## Rules

- Evergreen unit in pointer mode: before editing a skill, read `evergreen.json`. If `next_due` has passed or
  `contradiction` is set, say so and refresh after the task (the evergreen plugin's `evergreen-refresh`, otherwise
  MAINTENANCE.md); a refresh runs `aw.py doctor --probe` first. Every edit to a SKILL.md or its references gets a
  CHANGELOG entry with its reason (`R-`, `L-` or `T-` ids, or "user request"). Re-run `evals/evals.json`
  (evergreen-test) when a change alters what a skill triggers on, decides or does.
- Research beats recall. Art facts, model behaviour, law and tool facts move. Never change a gold answer, a
  model profile, a law row or a `verified` flag from memory: cite the source in RESEARCH.md (an `R-` entry) and
  log the change. Rows not backed by a fetched source ship `verified: no`.
- `aw.py` stays standard-library Python 3.9+ with Pillow optional, prints exactly one JSON object per command,
  fails soft (`ok: false` with `error`, exit 1; argparse usage errors print usage text and exit 2), and runs on Windows, macOS and Linux. Never add numpy, scipy, OpenCV,
  scikit-image or imagehash. Every new command or option gets an offline test in `tests/test_aw.py` with its
  fixture drawn in code. Keep `aw.py` and `aw_measure.py` (the light, colour and composition measures it imports)
  each under 100 KB; when one nears the line, split or cut, never squeeze comments.
- No images in the repository except the README banner. Museum fixtures are fetched by accession number and
  checked against a pinned SHA-256 (`AW_NET=1 python tests/test_aw.py`); no WikiArt, VAB, LAPIS, BAID or AVA
  images, ever.
- The verdict contract (`skills/artwright-judge/references/verdict-contract.md`) is a public interface: a breaking
  change bumps its version and the plugin's minor version.
- Skills stay under 200 lines, with a description of at most 700 characters that says what the skill does and
  names the sibling that owns nearby requests.
- Judging guards hold in every skill: no attribution, authentication or valuation from pixels; no "is this
  AI-made" from pixels; no lone scores; a living artist's name becomes traits; never the golden ratio as a reason.
- Before committing, run from the repository root: `python tests/check_skills.py`, `python tests/test_aw.py`
  and `python scripts/budget.py`. CI runs them on three operating systems.
- This is a public repository. Nothing in it names a person other than the author credit and cited authors and
  artists, a private project, a machine, an absolute path on someone's machine, or a credential. The private taste
  record lives in `ARTWRIGHT_HOME` (default `~/.artwright`) and never enters the repository.
- Versions: when a packaged file changes, bump `.claude-plugin/plugin.json` and the CHANGELOG release notes. Tags
  and releases need the owner's go-ahead.
- Work on `main` through pull requests; delete merged branches.
- No AI attribution anywhere: no Co-Authored-By trailers and no "generated with" lines in commits, pull requests
  or files.

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here. At the start of a task, scan it and open only the
  entries that match; read `ai-docs/HANDOFF.md` when continuing unfinished work.
- Before finishing a task that hit a dead end, verified a non-obvious command or made a design choice, record it in
  `ai-docs/` and rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the owner's
  private notes, never here.
- Link documents with relative markdown links. Every markdown folder has an index that links its files. No
  wikilinks in the repository.
