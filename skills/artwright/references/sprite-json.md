# Render-then-paint gate: the render folder contract

`aw.py geomgate <render dir> <painted>` checks that a painting made over a 3D render kept the model's shapes. It
reads three files from the render folder, written by whatever renders the model (a Blender sprite script, a game
engine capture). This page is the contract. Back to [SKILL.md](../SKILL.md); command table:
[cli.md](cli.md).

## Files

| File | What it holds |
|---|---|
| `beauty.png` | the render the painting was made over, RGBA; transparent where nothing was drawn |
| `id.png` | the object ID pass at the same size: each part a flat colour, written through the sRGB transform |
| `sprite.json` | the keys below |

The painting may be any size with the same framing; it is resized to the render's size. A fully opaque painting
takes the render's alpha, so a painted background never counts as part of the model.

## sprite.json keys

| Key | Required | Meaning |
|---|---|---|
| `id_colours` | yes | `{"part": [r, g, b], ...}`: each part's object colour, **linear** 0 to 1, as the renderer stores it. The gate converts it to sRGB before matching `id.png` (within 0.12 per channel, alpha at least half). At most 254 parts. |
| `rings` | for the ellipse and spokes gates | `{"part": {...}}`: wheels, gears, dials. Each ring has `rim_px` (at least 12, typically 72, projected points of the rim's near face in render pixels, at equal angles in the wheel's own plane, in order), `centre_px` ([x, y], the projected centre) and optionally `arms` (spoke count). |
| `contacts` | no | `[["a", "b"], ...]`: pairs of parts that must touch in the render (a wheel in water, a shaft into a wall). `--contact a:b` on the command line replaces the list. |
| `beauty_image`, `id_image` | no | other file names for the two images |

Other keys (camera, ground base, loop, frames) are ignored, so a renderer's own metadata can share the file.

## Gates

- **ellipse** (a ring): along each ray from `centre_px` through each rim point, the painting's edge profile is
  cross-correlated with the render's within plus or minus 15% of the radius; the best lag (at most 8% of the
  radius) is how far the painted rim moved there. Passes when 80% of the angles where the render shows a rim
  match (correlation 0.3 or more), the lags' RMS is at most 5% of the radius, and an ellipse fitted to the moved
  points sits within 6% (centre), 8% (axes) and 8 degrees (tilt) of the true one. Angles the render hides
  (behind water) are skipped. A displacement larger than the lag window shows up as weak matches and an RMS near
  the window, never as its full size: read `coverage` and `rim_rms` before `axis_err`.
- **spokes** (a ring with `arms` or `--spokes N`): luma times alpha around the ring at the rim points' angles,
  from 40% to 78% of the radius. Passes when the painting's profile correlates with the render's at 0.6 or more
  and keeps at least half the render's energy at the arm count and its harmonics.
- **regions**: at game size (`--game-px`, default 96 on the long edge) each part's painted luma is fitted to the
  render's (paint = a times render + b) and the worst 3x3 patch of residual is divided by the part's median
  residual plus 0.01. Above 5 is a new object (a blade painted on a roof). Brush texture stays under it.
- **contact**: each pair touches within 3 px in the render (a ring counts with the space between its arms
  filled). This checks the model, so it fails the same way for every painting of it.
- `edges_info` (not a gate): edge precision and recall per part at 256 px. Painted texture moves edges, so a low
  precision is not a failure; `--no-edges` skips it.

The output has `pass`, `failing_gates`, each gate's numbers and `tol`. A failing gate is a finding, not an error:
the command exits 0. Tolerances were set on one sawmill's renders and paintings (2026-10-23); confirm a failure by
looking at the region named before rejecting a painting.
