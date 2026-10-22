# artwright

Four self-maintaining ("evergreen") skills and a command-line tool that give an AI agent an artist's eye. It
critiques and analyses art of every kind, from drawing and ceramics to pixel art and 3D renders. It compares and
ranks generated images the way the evidence says works: two at a time, in both orders, blind to file names. It
names styles and movements with the traits that prove them, explains art theory, and answers art-market and
art-history questions to a historian's standard. Written in October 2026 for Claude Code, GitHub Copilot, Cursor
and Codex, from an eight-part research pass whose dated reports are in
[ai-docs/research](ai-docs/research/2026-10-21-creation-pass.md).

## Why

AI judges of beauty are weak and easily swayed. On a 2026 aesthetics benchmark, the best model picked a set's best
and worst image consistently in about a quarter of tasks, where experts managed two thirds. Swapping the order
of two images flips up to 61% of verdicts. Learned aesthetic scores reward photo polish and prefer images with
defects over clean ones more often than not. Style labels are right about half the time, often for the wrong
reasons, and worse for non-Western art. The open web garbles art facts: the "most expensive vase" on a record
list is Qing, not Ming, and the oldest dated cave art changed in January 2026. Each of these is a rule in the
skills, with its source in [RESEARCH.md](RESEARCH.md).

## The skills

| Skill | Use it for |
|---|---|
| `artwright` | critique of a single work, style and movement ("is this cubist?"), art theory, art facts (oldest, most expensive), ceramics; the router |
| `artwright-judge` | "which is better", ranking a batch, fit to a brief, the next prompt and settings per model; writes `artwright/verdict.json` for the plugin that called it |
| `artwright-pixel` | pixel art and 2D game art: is it real pixel art, grid, palette, orphans, jaggies, tiles, animation frames |
| `artwright-curate` | the knowledge files (sourced, dated, `verified` flags) and the user's private taste record and calibration labels |

artwright judges, explains and directs. It does not generate images (comfyui-gen), model meshes (polywright),
judge video takes (cinewright-qc), score brand fidelity (brandwright) or fix pixel grids (Pixel Snapper,
proper-pixel-art, unfake; it points to them).

## What a run looks like

> Which of these eight fox renders is best for the brief "red fox in snow at dusk, side view, no text"?

The judge dedupes the batch, reads one contact sheet to strike broken renders, then judges the rest in pairs. Each
pair is shown twice, as `1 | 2` and `2 | 1`, in fresh calls, with no file names. A split between the two orders
is a tie and goes to the user. `aw.py rank` fits a Bradley–Terry model, marks the places where the order is not
established, and writes the ranking, the brief checks and the next prompt into `artwright/verdict.json`.

## aw.py

`skills/artwright/scripts/aw.py` is one standard-library Python file (3.9 or later). Pillow is used when present
and never required; without it, PNG is decoded in pure Python and JPEG or WebP through ffmpeg. Every command prints
one JSON object.

```
python aw.py info photo.jpg                 # size, alpha, SHA-256, token cost before any Read
python aw.py sheet renders/ -o sheet.png    # one labelled contact sheet instead of many reads
python aw.py stats painting.jpg --notan n/  # value, contrast, colourfulness, symmetry; no beauty score
python aw.py pixel sprite.png --budget 16 --palette pico-8
python aw.py compare prepare a.png b.png    # the pair in both orders, labelled 1 and 2
python aw.py rank --write                   # Bradley-Terry with ties into artwright/verdict.json
```

All commands: [skills/artwright/references/cli.md](skills/artwright/references/cli.md).

## Install

Claude Code: add this repository as a plugin marketplace and install `artwright`:

```
/plugin marketplace add m4bwav/artwright
/plugin install artwright@artwright
```

Other agents: link or copy each folder under `skills/` into your agent's skills folder (`~/.claude/skills`,
`~/.agents/skills`, `~/.copilot/skills` or `.cursor/skills`). The skills share `artwright/scripts`, so install all
four together. Optional: `pip install pillow` for speed and every image format.

## Privacy

The skills store the images they judge only where you point them. The private taste record (your verdicts, your
picks, calibration labels) lives in `~/.artwright` (or `ARTWRIGHT_HOME`) on your machine and is never sent
anywhere. `aw.py` makes network requests only to fetch a Lospec palette you name or for `doctor --probe`.

## Maintenance

The skills keep themselves current with the [evergreen protocol](https://github.com/m4bwav/evergreen-protocol):
research refresh every 60 days or so ([evergreen.json](evergreen.json)), findings in [RESEARCH.md](RESEARCH.md),
reasoned changes in [CHANGELOG.md](CHANGELOG.md), lessons in [LEARNINGS.md](LEARNINGS.md), test runs in
[TESTS.md](TESTS.md), maintenance steps in [MAINTENANCE.md](MAINTENANCE.md). Agent rules: [AGENTS.md](AGENTS.md).
Security: [SECURITY.md](SECURITY.md).

## Licence

MIT. See [LICENSE](LICENSE).
