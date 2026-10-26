# Sprites, animation and tiles

What to check on sprite sheets, animations and tilesets, and where engine import and 3D style questions go.

Checked 2026-10-21

Back to [SKILL.md](../SKILL.md).

## Sprites and animation

Frame consistency is what `aw.py pixel` checks on a sheet (slice by grid, or by Aseprite's `--data` JSON):

| Check | Pass | Source | verified |
|---|---|---|---|
| Palette | Every frame uses the same colour set (a subset of the sheet palette) | R-20261021-8 | yes |
| Grid | Every frame has the same detected pixel scale and offset | R-20261021-8 | yes |
| Bounding box | Size changes only where the motion explains it | R-20261021-8 (proposal) | no |
| Baseline | Feet stay on one row unless the character jumps | R-20261021-8 (proposal) | no |
| Silhouette area | Area change per frame stays small; a jump means volume drift | R-20261021-8 (proposal) | no |

AI sheets drift between frames (head size, light angle, detail level). The remedies are a fixed reference, a locked idle pose, and one grid and palette fitted once over all frames and applied to each (proper-pixel-art's method, [repo](https://github.com/KennethJAllen/proper-pixel-art), verified: yes).

Timing conventions, not standards (R-20261021-8, verified: yes as sourced; no single authority):

- Walk cycles 4 to 8 frames (4 since the NES era; 6 as a smooth minimum); idles 2 to 4. Books agree: 8 typical, 16
  smooth, 2 or 3 barely a walk (Silber §8.5; Dawe and Humphries ch. 6).
- A loop needs 3 frames at least; a 2-frame idle works only slowly, at about 500 ms a frame (Azzi p. 232; Silber §8.3).
- Pixels that appear and vanish frame to frame read as flicker; when a row appears, pop 2 or 3 pixels, not 1, and
  keep faces and eyes out of shimmering or sub-pixel regions (Azzi pp. 199, 205; Silber §8.3).
- 8 to 12 fps typical; 100 ms per frame is the common tool default.
- Holds of 200 to 400 ms on anticipation and impact. Uniform timing everywhere reads as stiff.
- Extra in-betweens expose inconsistency; fewer, better frames beat many drifting ones.

Visual references: Slynyrd Pixelblog #8 (intro to animation), #25 (motion cycles), #55 (top-down character animation) at the [catalogue](https://www.slynyrd.com/pixelblog-catalogue); saint11's cycle sheets at [saint11.art](https://saint11.art/blog/pixel-art-tutorials/) (frozen since 2020).

## Tiles

- **Seams**: for a wrapping tile, the left edge must continue the right and the top the bottom; for a set, each declared neighbour edge must continue its partner. `aw.py pixel` diffs those edges and renders a **3x3 tiled preview** at integer scale for the judge. No published automated seam test was found; this check is artwright's own (R-20261021-8, verified: no).
- **Repetition**: in the 3x3 preview, look for a bright or dark spot that repeats as an obvious grid. `--tile` also
  reports a ramp across the tile (`gradient_lr`, `gradient_tb`: half against half, in L*), detail bunched in one
  place (`detail_spread`) and a flat border side, with `repetition_suspected` when one passes its line (6 L*, 1.0;
  heuristic, 4 of 20 real seamless tiles, the flagged ones striping visibly). The books' list: a gradient across a
  tile, one standout feature, details lined up along an edge (Silber §9.3; Dawe and Humphries ch. 5).
- **Starting a set**: sketch the base tile as a plus sign joined at the middle, so both wraps are tested at once
  (Dawe and Humphries ch. 5). Scatter props in odd counts. A 9-slice frame keeps its light direction; a three-tile
  stretch does not (Silber, exercise 9.1). Agree the tile size before drawing: a 32 px tile is four 16s of work (§9.1).
- **Autotile sets**: corner-based sets cap at 16 tiles (2^4); full 8-neighbour blob sets need 47. Godot 4 terrains use peering bits per tile. Generators to point to: Blobsmith (47 tiles from six bases, exports Godot 4 TileSet and Tiled .tsx), AutoBlob (Aseprite script) ([Tiled forum](https://discourse.mapeditor.org/t/neither-terrain-nor-wang-can-handle-a-blob-tileset/4671), [Blobsmith](https://blobsmith.itch.io/blobsmith); verified: yes via R-20261021-8).
- **Sheet spacing**: margin and spacing between tiles in a sheet (one pack uses 4 px and 2 px) stop texture bleeding at runtime.
- **One density per set**: every sprite and tile in a set should detect the same pixel scale; mixed scales are fixed by redrawing, not filtering.

## Isometric

- Lines step two across for one up (2:1, about 26.6 degrees), the standard pixel isometric; a diamond tile is a
  lineless checker of that step. Oblique (1:1) is the simpler alternative. To turn a side view isometric, skew and
  scale its height by about 0.87 (Azzi pp. 145-153; book).

## Engine import (pointers only)

These belong to the engine plugins (unity-agent, a Godot route, roblox-agent). artwright only names the rules when a check finds the symptom:

- Point (nearest) filtering, no texture compression, no mipmaps on pixel sprites.
- One shared, integer pixels-per-unit across the project; integer screen scaling.
- Unity: the Pixel Perfect Camera keeps an integer number of screen pixels per sprite pixel; scaled or rotated sprites lose it ([Unity discussion](https://discussions.unity.com/t/released-pixel-perfect-camera/633246), verified: yes via R-20261021-8).
- Godot: viewport stretch with integer scale mode (verified: no, re-check the Godot docs before quoting settings).
- Roblox: hand off to roblox-agent; artwright has no checked Roblox pixel-art settings (verified: no).
- Non-integer scaling and mixed scales were "a catastrophe" in one 2024 devlog; even integer-scaled sprites showed thicker outlines beside unscaled ones ([devlog](https://squeakypig.itch.io/unicopia/devlog/787703/a-tale-about-chasing-a-pixel-perfect-tail), verified: yes via R-20261021-8).

## 3D stylisation (pointers only)

Style briefs only; shader and bpy work goes to polywright (polywright-blender, polywright-finish).

- Toon or NPR in Blender: no built-in toon mode shipped as of this check; Shader-to-RGB setups, community node groups or paid add-ons. Blender's NPR project was planned to start after 5.0 ([code.blender.org](https://code.blender.org/2025/05/npr-project/), verified: no for any shipped version).
- PS1 look: vertex snapping, affine UV warping, low-res nearest textures, reduced colour depth with dithering, subdivided geometry to tame warping. Godot reference: MenacingMecha's [godot-psx-style-demo](https://github.com/MenacingMecha/godot-psx-style-demo) (R-20261021-8, verified: yes).
- Low-poly pixel look: render at low resolution with nearest upscale, then run the same `aw.py pixel` checks on the frames.
