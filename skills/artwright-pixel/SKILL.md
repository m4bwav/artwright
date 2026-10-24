---
name: artwright-pixel
description: "Use whenever pixel art or 2D game art is made, checked or critiqued: 'is this real pixel art', 'check my sprite', 'why does this AI sprite look off', 'fix the grid', 'too many colours', 'does this tile seam', 'check these animation frames'. Runs aw.py pixel (grid scale and offset, lattice alignment, uniform blocks, blend pixels, colour budget, palette match, orphans, jaggies, alpha, outlines, tile seams, frame consistency), then a pixel critique in priority order, and points to fixers and editors (Pixel Snapper, proper-pixel-art, unfake, Aseprite MCP). Engine import belongs to the engine plugins. Also 'refresh artwright-pixel'."
---

# artwright-pixel

Checks and critiques pixel art and 2D game art. The script measures; this skill reads the numbers, then looks.
It does not fix grids or edit sprites: it reports what is wrong, with coordinates, and points to the tools that
fix it (ruling R8).

Script: `../artwright/scripts/aw.py` (commands: [../artwright/references/cli.md](../artwright/references/cli.md)).
Rules and vocabulary: [references/pixel-art.md](references/pixel-art.md); sprites, animation, tiles and
engine pointers: [references/sprites-tiles.md](references/sprites-tiles.md).

## Step 0

Freshness: the plugin's [evergreen.json](../../evergreen.json) (past due: say so in one line, refresh after).
Ask (or infer from the request) the intended native size, the colour budget and any named palette.

## Step 1: measure

```
aw.py pixel <img> --budget 16 [--palette pico-8|<lospec-slug>|<file.hex>] [--preview native_x4.png]
```

Read the JSON before looking at the image:

- `grid.scale` and `grid.offset`: the apparent pixel size. `lattice_alignment` under 100% means off-grid pixels.
- `uniform_blocks` under 100%: blocks of mixed colour (mixels or resampling).
- `transitional_pixels` above 0: blend pixels between colours (blur, anti-aliasing from resampling).
- `unique_colours` against the budget; `near_duplicate_colour_pairs` (each colour needs a role).
- `orphans` (with coordinates), `jaggies`, `outline` colours, `partial_alpha_pixels`.
- `clean_pixel_art` and `problems`: one integer scale, 100% alignment, uniform blocks, no blend pixels, colours
  within budget, binary alpha. That is the definition of done for an AI sprite (R-20261021-8).

A raw AI "pixel art" image typically shows thousands of colours, a wandering block size and about 2% alignment.
That is a fixer's job before any critique: say so and point to the fixers below.

Named palettes: `pico-8` is built in (CC0); any other Lospec slug is fetched once on request and cached
(`nintendo-entertainment-system`, `endesga-32`, `sweetie-16`, `dawnbringer-32`...). Never crawl Lospec.

## Step 2: look (critique in priority order)

View the native-size preview at an integer zoom (`--preview`, or `aw.py fit <img> -o x.png --pixel --long 512`),
never a smoothed resize. Then, in this order, stopping at the first level that fails badly:

1. **Read at 1x**: is the subject readable at native size? A cold read before the brief.
2. **Silhouette**: clear shape filled black; limbs at least two pixels thick; a pose that reads.
3. **Value**: three or more value steps; light and shadow sides separate in greyscale.
4. **Palette roles**: each colour has a job; ramps hue-shift (up to about 20 degrees a step), brightness rises
   steadily, saturation peaks mid-ramp; no near-duplicates.
5. **Clusters**: no noise, no orphan pixels outside textures, no pillow shading, no banding.
6. **Outlines**: consistent; selective outlining (lighter where light hits); jaggies follow monotonic steps.
7. **Light**: one source, consistent across the sprite and its frames.

Each finding cites the rule it breaks and the pixel region or coordinates. No "looks good". One highest-value fix.

## Painted sprites are not pixel art

A painted game sprite at native size (soft edges, brush texture, thousands of colours, a 96 px building) is not
pixel art: `aw.py pixel` would call it broken and a fixer would posterize it. Check it with
`aw.py sprite <candidate> --refs <the sprites it will sit beside>` instead: value mean and spread, chroma,
colours, soft edges, texture and outline value on opaque pixels, each against the references' range. Measure
the size it ships at; read `outside` for what to change; then look at it at 1x beside two references.
If it was painted over a 3D render, `aw.py geomgate` first (artwright).

## Sprites, frames and tiles

- Frames: `aw.py pixel f1.png f2.png ... --frames`: scale, size, palette per frame, bounding boxes and baseline
  consistency. A baseline that jumps is a bug unless the motion asks for it.
- Tiles: `aw.py pixel tile.png --tile --preview t.png` writes a 3x3 preview; `seam_suspected` means the wrap edges
  differ from the inside. Look at the preview.
- Engine import (point filter, no compression, integer pixels per unit) goes to the engine plugin (unity-agent,
  roblox-agent, madnesswright); name it, do not configure it here.

## Fixers and editors (point, do not rebuild)

Grid snapping: Pixel Snapper, proper-pixel-art (`ppa`), unfake. Editing: the Aseprite MCP servers
(aseprite-mcp, aseprite-ai-artist; the user's own Aseprite). Generation: comfyui-gen. Details, licences and
links: [references/pixel-art.md](references/pixel-art.md). After a fix, re-run `aw.py pixel` and compare; keep
the fix only if the numbers improve and a blind A/B (artwright-judge) prefers it.

## Guards

The hub's guards apply ([../artwright/SKILL.md](../artwright/SKILL.md)). "Is this AI-made" is never answered from
pixels; the numbers say whether it is clean pixel art, not who or what made it.

## Maintenance

Shared evergreen unit at the plugin root: [evergreen.json](../../evergreen.json),
[RESEARCH.md](../../RESEARCH.md), [CHANGELOG.md](../../CHANGELOG.md), [LEARNINGS.md](../../LEARNINGS.md),
[TESTS.md](../../TESTS.md), [MAINTENANCE.md](../../MAINTENANCE.md). Fixer and MCP tool facts are volatile
(stars, licences, maintenance): recheck at each refresh.
