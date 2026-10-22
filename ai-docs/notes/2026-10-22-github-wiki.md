---
title: GitHub wiki written and published for 0.1.0 (unreleased, main at 997f5b9)
kind: note
date: 2026-10-22
verified: 2026-10-22
stale_after: 2027-04-22
tags: [wiki, docs, 0.1.0, github]
summary: "the wiki's pages, where their git working copy is, how every aw.py example was verified against main at 997f5b9, the facts found on the way, the inaccuracies in the shipped docs, and how to update the wiki; read before touching the wiki or the docs listed under inaccuracies"
---

# GitHub wiki for 0.1.0 (unreleased)

## Summary

Asked: write the GitHub wiki for m4bwav/artwright with the wikiwright skill. Written: 10 pages plus sidebar and
footer, from the README, AGENTS.md, CHANGELOG, the four SKILL.md files, their references (cli.md,
verdict-contract.md, rubric.md, store.md), aw.py itself, the CI and release workflows and SECURITY.md. No issues
exist yet; PRs #1-#5 were read. artwright has no registry package and no tag, so "published" meant the `main`
branch at 997f5b9. Every aw.py example was run by `2026-10-22-wiki-verify.py` and pasted from its output. Wiki
commit 2cd14e1; live check 10 pages, 0 failures; prose checker 0 strong findings.

Pages: Home, Getting-Started, Skills, Commands, How-Images-Are-Judged, Verdict-Contract, Errors-and-Edge-Cases,
Recipes, FAQ, Development, _Sidebar, _Footer. No Versions page: nothing is released.

## Where the pages are

`../artwright.wiki` (a sibling of this clone, outside this repository), branch `master`, remote `origin` =
`https://github.com/m4bwav/artwright.wiki.git`. Plain markdown links, LF line endings. The pages were generated
from sources with `@@OUT label@@` and `@@PART label :: start :: end@@` markers by `build.py`, which copies output
from the saved runs; the sources and build.py were kept in the session's scratch folder, not committed. Editing the
pages directly is fine; rerun the gates afterwards.

## How it was published

Preflight: `placeholder` (GitHub's Home.md only). Pages committed on top of the clone, plain push 61d4cc4..2cd14e1.
`wikiwright.py live`: 10 pages 200 (Home 301 to /wiki), footer and sidebar render, 29 anchor links, 0 broken.

## Updating the wiki later

1. `git -C ../artwright.wiki pull --ff-only`, then edit the pages.
2. Re-verify: clone `main` fresh into a scratch folder, run `python 2026-10-22-wiki-verify.py <clone> <scratch
   root> > new.txt` on Linux with Pillow (the pages show that run), again with `--no-pillow`, and on Windows with
   `--python <a 3.9 interpreter>`. `wikiwright.py diffout 2026-10-22-wiki-verify.out.txt new.txt`; every
   difference is a page to fix.
3. `wikiwright.py outputs ../artwright.wiki <the three outputs> <plugin details output> --address ''`,
   `wikiwright.py snippets ../artwright.wiki 2026-10-22-wiki-verify.py`, `wikiwright.py check ../artwright.wiki
   --version <v>`, then the everwrite checker.
4. Commit, push, `wikiwright.py live m4bwav/artwright ../artwright.wiki`. Pages naming the version or commit:
   _Footer (0.1.0, 997f5b9), Home ("not yet released", 997f5b9), Errors-and-Edge-Cases (997f5b9 in the opening
   line and the double-tie section), Development (997f5b9, test counts), FAQ ("Is there a release?").

At the first release: add a Versions-and-Upgrading page, change "not yet released" on Home, FAQ, Development and
the footer, and drop the double-tie known issue once the fix (`resolve()` returning `tie` when both picks are
`None`, already in the Step 3 working tree) is merged.

## How the examples were verified

- Script: `2026-10-22-wiki-verify.py` (stdlib Python; draws every fixture in code, runs make_fixtures.py from the
  clone for the sprites, copies aw.py into a scratch folder, runs each page block through bash with `python` on
  PATH pointing at the chosen interpreter; HOME is a scratch folder masked as `/home/you`; ISO times masked as
  `<time>`).
- Runs on 2026-10-22, aw.py sha256 ff8ec4c3...: Linux (WSL2) Python 3.14.4 + Pillow 13.0.0 (shown on the pages,
  `2026-10-22-wiki-verify.out.txt`); Linux with Pillow hidden by a stub PIL package (differs only in doctor and JPEG
  decoding); Windows Python 3.9.25, no Pillow, ffmpeg on PATH (differs in backslash paths, PNG bytes and hashes,
  argparse wording, JPEG unique colours via ffmpeg).
- `claude --plugin-dir <clone> plugin details artwright` (Claude Code 2.1.281): 4 skills, ~925 always-on tokens.
- outputs: 65 checked, 0 missing, 2 skipped (usage synopsis; repository test output). snippets: 7 blocks checked,
  61 commands counted.
- Repository's own checks on the fresh clone (Windows, Python 3.14, Pillow 12.3.0): test_aw.py 34 tests OK
  (1 skipped: museum fixtures need AW_NET=1), check_skills 0 problems, budget all green.
- Not tested (marked on the pages): `/plugin marketplace add` and `/plugin install`, copying skills into other
  agents, Lospec palette fetching, `doctor --probe`, macOS.

## Facts verified while writing (not in the README)

- Usage errors (argparse) print usage to stderr, nothing on stdout, exit 2; `--version` prints plain `0.1.0`.
- `info` and `pixel` fail per item; `hash`, `dedupe` and `compare` abort on the first unreadable file.
- `fit --tokens` alone has no long-edge cap; without `--pixel` fit never enlarges; a crop past an edge is clipped;
  a crop fully outside errors.
- `sheet --cell` default 384; `pixel --tol` default 24 (undocumented in cli.md); `--scale` drops alignment_x/y.
- Grid detection reports the largest clean block (a 4-px checker drawn at 4x reads as scale 16); a gradient with
  steps under `--tol` reads as one 64 px block.
- `seam_suspected` fires on a perfectly repeating checker whose squares end at the tile edge.
- `palette` median cut can return the same colour twice.
- `close_to_next` is `null` on the last ranking row; equal strengths are ordered by SHA-256.
- `verdict validate` accepts a draft as valid; `verdict init` keeps the existing `kind`.
- PNG bytes, SHA-256 and pair ids differ between Windows and Linux for the same drawing (zlib builds).
- On Windows, folder-listed paths and output paths print with backslashes.

## Inaccuracies found in the shipped docs

1. README ("Every command prints one JSON object"), cli.md ("failures print {ok: false} and exit 1") and AGENTS.md:
   argparse usage errors print no JSON and exit 2; `--version` prints plain text. Waits for the owner.
2. verdict-contract.md shows `close_to_next` as a boolean; aw.py writes `null` on the last row.
3. Bug, not a doc: on main, both orders recorded as `tie` resolve as `decided` with `winner: null`, and `rank`
   counts that pair as a win for side b. The README and rubric describe it as a tie. Fixed in the Step 3 working
   tree (aw.py `resolve()`), not yet merged; documented on Errors-and-Edge-Cases as a known issue.
4. cli.md omits `pixel --tol` and the `sheet --cell` default (384).

## Gotchas

- The snippets gate needs each held block to start and end on its own lines in the program: put the opening and
  closing triple quotes on separate lines.
- The everwrite checker flags two `prints:` lines in a row (code blocks are skipped): alternate with `gives:`.
- On Windows, subprocess `bash` resolves to System32's WSL launcher before Git Bash; use `shutil.which("bash")`.
- Hiding Pillow with `sys.modules['PIL'] = None` in a `-c` wrapper breaks `python -c` snippets; a stub `PIL`
  package on PYTHONPATH that raises ImportError works for every call.

Related: see also [../HANDOFF.md](../HANDOFF.md), [../log.md](../log.md).
