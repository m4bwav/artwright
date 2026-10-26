# Pixel art rules and defects

What to check and how to critique a pixel-art image, with the numbers `aw.py pixel` reports against.

Checked 2026-10-21; book rows added 2026-10-25 (Azzi, *Pixel Logic*; Silber, *Pixel Art for Game Developers*;
Dawe and Humphries, *Make Your Own Pixel Art*; Hughes et al., *Computer Graphics: Principles and Practice*).

Back to [SKILL.md](../SKILL.md).

## Craft rules with thresholds

| Rule | Threshold or test | Source | verified |
|---|---|---|---|
| Palette size | 16 or 32 colours is typical; every colour needs a role | [Derek Yu, Basics](https://www.derekyu.com/makegames/pixelart.html), [Common Mistakes](https://www.derekyu.com/makegames/pixelart2.html) | yes |
| Colour budget (artwright default) | 12 unique colours at 32x32, 16 at 64x64, warn above 32 | artwright proposal (R-20261021-8) | no |
| Lines one pixel thick | Outlines reduced to single-pixel lines, stray pixels removed | Derek Yu, Basics | yes |
| Curves | Segment lengths grow or shrink steadily along a curve; a break is a jaggy | Derek Yu, Basics | yes |
| Outside anti-aliasing | Never anti-alias the outer edge of a game sprite (background unknown) | Derek Yu, Basics | yes |
| Selective outlining | Lighter outline where light hits, darker shade instead of black inside | Derek Yu, Basics | yes |
| Dithering | Sparingly, on large flats or rough textures; ordered (Bayer) reads as deliberate, error diffusion as noise | Derek Yu, Basics; R-20261021-8 | yes |
| Chunky pixels | Nothing rendered one pixel thick (limbs, branches) | Derek Yu, Common Mistakes | yes |
| Ramps | 9 swatches per ramp; hue shift up to +20 degrees per step ("20 is about as high as I go"); brightness rises steadily; saturation peaks mid-ramp and never reaches 0 or 100 | [Slynyrd Pixelblog 1](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes) | yes |
| Ramp spacing | 8 ramps 45 degrees apart; neutrals from desaturated middle columns | Slynyrd Pixelblog 1 | yes |
| Straight ramps | Brightness-only ramps are allowed but lack interest and harmonise poorly | Slynyrd Pixelblog 1 | yes |
| Orphans | Single pixels not joined to a same-colour cluster are usually avoided, except inside a texture | [Slynyrd Pixelblog 2](https://slynyrd.com/blog/2018/2/15/pixelblog-2-texture) | yes |
| Anti-aliasing amount | An AA run is about half the length of the step it softens; one or two in-between shades, three at most; none on clean 45-degree lines; convex curves take the lighter in-between, concave the darker | Azzi pp. 45-49 | book |
| Interior edges | Boundaries between colours inside the sprite (cel and shadow shapes) follow the same step rules as the outline (`jaggies_interior`) | Azzi p. 28 | book |
| Outline type by background | None, black, coloured (each part's darkest shade) or selective. Selective outlines suit dark or neutral grounds; on light or busy grounds a dark contour keeps the sprite apart (`--bg` reports the silhouette share lost on a ground) | Azzi pp. 30-37, 106, 197-198; Dawe and Humphries ch. 3 | book |
| Ramp direction | Lights drift toward yellow, shadows toward purple or blue (or red); near-blacks keep a tint instead of #000000; small sprites need only 2 or 3 colours a ramp; skin ramps stay tight | Azzi pp. 69, 72-76; Silber §6.6 | book |
| Dither limits | Only between neighbouring, low-contrast ramp steps; never on parts that animate (it shimmers) or on small sprites | Azzi pp. 111, 116-120; Silber §9.5 | book |
| Native size | The smallest feature that must read (an eye, a button) sets the sprite's size, not the other way round | Azzi p. 95 | book |
| Value separation | A detail of one to three pixels must differ from its neighbours in value, not hue alone: equal-value blue edges read fuzzy, blue on black barely separates, yellow on white is weak | CGPP §28.19 p. 780 (the pixel translation is ours) | book |
| Line rhythm | Irregular run patterns (2, 1, 2, 2, 1) are aliasing; long straight lines read cleanest on whole ratios (1:1, 2:1, 3:1) | CGPP §18.2 pp. 498-499 | book |
| Dark seam | A thin dark line between two clashing colours settles them, one reason outlines work | CGPP §28.19 p. 779 | book |

## Defect vocabulary

- **Orphan (stray) pixel**: no same-colour 8-neighbour; reads as dirt. Not a defect inside a deliberate dither or texture.
- **Jaggy**: a single pixel or short segment that breaks a line's run pattern (Derek Yu).
- **Banding**: two runs of different colours and the same length hugging each other, straight under or one pixel along (on a diagonal, Silber's super pixel), so two thin lines read as one thick blurred one. The usual result of quantising a smooth render: rings that follow the outline. Fix by lengthening or shortening one band's end, or with anti-aliasing (Azzi pp. 55-57; Silber §10.1). `banding` gives the count and the first coordinates.
- **Pillow shading**: shading from the outline inward instead of from a light source (Derek Yu). `pillow` correlates lightness with the distance from the silhouette (`edge_corr`) and with each of eight light directions (`light_corr`).
- **Mixels**: pixels of mixed sizes in one image, or off the grid (R-20261021-8).
- **Doubles**: lines two pixels thick where one was meant; doubled corners on a run. `corner_doubles` counts the stair-step corner pixels of one-pixel lines (removable without breaking the line; square corners are not counted). pixelwright's `clean.corners` removes them.
- **Noise**: speckle from error-diffusion dither or a generator, alternating ramp neighbours in flat areas.
- **Soft edges**: blur or in-between colours from bilinear resizing.
- **Non-binary alpha**: any alpha other than 0 or 255 on a sprite.
- **Too many similar colours** and **cardboard designs** (stiff, grid-led shapes) (Derek Yu).

## Critique priority order

Work top down; a failure higher up outranks everything below it.

1. **Read at 1x** (and at the game's integer scale). Never judge from a bilinear-scaled image.
2. **Silhouette**: fill it black; does it still say what it is? Then blur it (`aw.py degrade <img> -o b.png --kind blur`): the main shapes should survive (Azzi p. 112).
3. **Colour design and spacing**: one main colour, one contrasting second colour, and a charm point (a scarf, an eye colour) that still reads at 1x; every feature has a pixel of space round it (Azzi pp. 79, 104, 106-108; Dawe and Humphries ch. 5).
4. **Value**: lit side among the lightest values, core shadow among the darkest; survives desaturation.
5. **Palette roles**: each colour earns its place; no near-duplicates; ramps hue-shift.
6. **Clusters**: clean shapes, no orphans or noise, no banding.
7. **Outlines**: consistent thickness, no jaggies or doubles, selective outlining where it helps.
8. **Light**: one direction across the sprite and across frames; no pillow shading. A mirrored sprite mirrors its light: re-light it or accept it knowingly (Silber §7.3).

The pixel-critic agent in aseprite-ai-artist uses a close order: silhouette, too dark or flat, value contrast, flat shading, palette sprawl, semi-transparent pixels, strays, lines, light, animation ([pixel-critic.md](https://github.com/with-pebbly/aseprite-ai-artist/blob/main/agents/pixel-critic.md), verified: yes).

## AI pixel art: the four numbers

Image models paint pictures that look like pixel art without a pixel grid. Tells: thousands of colours, block sizes that wander, blurred or noisy edges, outlines that change thickness, semi-transparent fringes, and detail finer than the apparent pixel (R-20261021-8).

A measured case asked for a 32x32, about 12-colour sprite (Rangy, 2026-08-14; [write-up](https://rangy.ai/blog/ai-pixel-art), verified: yes via R-20261021-8):

| Number | Raw output | After fix | Pass line |
|---|---|---|---|
| Unique colours vs budget | 44,725 | about 12 | at or under the budget |
| Lattice alignment (colour changes on the true grid) | about 2% | 100% | 100% |
| Block size | wandering 26 to 32 px | uniform | one integer size |
| Transitional pixels | about 4.5% | 0 | 0 |

The fix that produced 100% was nearest-neighbour downsample first, then quantise with dithering off. `aw.py pixel` finds scale and offset with the unfake edge-profile method: row and column colour-change profiles, a histogram of peak spacings (the mode is the scale), then each offset 0 to scale-1 tried ([jenissimo write-up](https://dev.to/jenissimo/how-to-tame-your-ai-pixel-art-3pk5), verified: yes via R-20261021-8).

## Fixers and editors to point to

artwright reports what is wrong; these tools fix or edit. Do not rebuild them.

| Tool | Use | Licence | Link |
|---|---|---|---|
| Sprite Fusion Pixel Snapper | Grid snap and palette quantise, Rust CLI, batch, `--palette hex,...`; ComfyUI wrappers exist | MIT | https://github.com/Hugo-Dz/spritefusion-pixel-snapper |
| proper-pixel-art (`ppa`, PyPI 2.0.0) | Python fixer; fits one grid and palette over all animation frames. Its PyAV dependency bundles a GPL FFmpeg | MIT | https://github.com/KennethJAllen/proper-pixel-art |
| unfake.js / unfake-core | Browser tool and Rust CLI: detect, snap, downscale, quantise; Python port unfake.py | MIT | https://github.com/jenissimo/unfake.js |
| diivi/aseprite-mcp | Edit in Aseprite over MCP; `lint_sprite`, `get_color_stats`, `compare_frames`. `run_lua_script` runs any code on the host | MIT | https://github.com/diivi/aseprite-mcp |
| aseprite-ai-artist | Draw and edit in Aseprite over MCP; read-only pixel-critic agent, 62 rules | MIT | https://github.com/with-pebbly/aseprite-ai-artist |

Both MCP servers need the user's own Aseprite 1.3+ (paid, or built from source for personal use; the EULA forbids redistributing binaries). Licences and activity checked on the GitHub API 2026-10-21 (verified: yes). Which fixer fails least on the same sprites is untested (verified: no).

## Critic method (from aseprite-ai-artist)

Adopted from the pixel-critic agent (R-20261021-12, verified: yes):

1. **Cold read before the brief.** Write what the image shows and the three things the eye notices first, then read the brief. If the cold read missed the subject, that is the top finding.
2. **Mechanical checks next** (`aw.py pixel` numbers), then key frames one at a time at full zoom; downscaled strips hide broken shapes.
3. **A rule cited for every finding**, with a location (pixel coordinates or region).
4. **A score out of 10** (7 or more ships) and **one highest-value fix**.
5. **Never "looks good".** If nothing is wrong, say what was checked and what works.
6. **Fixes by blind A/B.** Show before and after with neutral labels, in both orders; keep the fix only if it wins both. A flip is a tie.
