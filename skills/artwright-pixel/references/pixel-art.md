# Pixel art rules and defects

What to check and how to critique a pixel-art image, with the numbers `aw.py pixel` reports against.

Checked 2026-10-21

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

## Defect vocabulary

- **Orphan (stray) pixel**: no same-colour 8-neighbour; reads as dirt. Not a defect inside a deliberate dither or texture.
- **Jaggy**: a single pixel or short segment that breaks a line's run pattern (Derek Yu).
- **Banding**: thick uniform bands of colour that draw the eye to the seams (Derek Yu).
- **Pillow shading**: shading from the outline inward instead of from a light source (Derek Yu).
- **Mixels**: pixels of mixed sizes in one image, or off the grid (R-20261021-8).
- **Doubles**: lines two pixels thick where one was meant; doubled corners on a run.
- **Noise**: speckle from error-diffusion dither or a generator, alternating ramp neighbours in flat areas.
- **Soft edges**: blur or in-between colours from bilinear resizing.
- **Non-binary alpha**: any alpha other than 0 or 255 on a sprite.
- **Too many similar colours** and **cardboard designs** (stiff, grid-led shapes) (Derek Yu).

## Critique priority order

Work top down; a failure higher up outranks everything below it.

1. **Read at 1x** (and at the game's integer scale). Never judge from a bilinear-scaled image.
2. **Silhouette**: fill it black; does it still say what it is?
3. **Value**: lit side among the lightest values, core shadow among the darkest; survives desaturation.
4. **Palette roles**: each colour earns its place; no near-duplicates; ramps hue-shift.
5. **Clusters**: clean shapes, no orphans or noise.
6. **Outlines**: consistent thickness, no jaggies or doubles, selective outlining where it helps.
7. **Light**: one direction across the sprite and across frames; no pillow shading.

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
