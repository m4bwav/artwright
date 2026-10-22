# Creation pass 2026-10-21: C. digital and pixel art (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation. All magnitudes `n/a (initial)`. Star counts and push dates were read from the GitHub REST API on 2026-10-21; they are snapshots.

## Findings (newest first)

### F1 · 2026-10-21 · Aseprite-driving MCP servers and agent skills are now a crowded, active niche
- What: GitHub search (`aseprite mcp`, 81 repos; topic `pixel-art` + `mcp`) shows a live ecosystem. Leaders: diivi/aseprite-mcp (725 stars, pushed 2026-10-21, MIT), with-pebbly/aseprite-ai-artist (442, pushed 2026-10-18, MIT; 18 noun-grouped MCP tools, 14 skills, a read-only `pixel-critic` agent, 62 rules, ~2006 palettes), willibrandon/pixel-plugin (378, a Claude Code plugin, last push 2025-10-19, so stale) and willibrandon/pixel-mcp (154, same date), MalloyTheDev/aseprite-mcp (21, pushed 2026-10-20, 156 tools incl. `assess_sprite`), aigengame/aseprite-automation (22, pushed 2026-10-20), Gamezxz/pixel-art-studio (89, Pillow-only skill, no Aseprite), Snehil-Shah/LibreSprite-MCP (36, GPL-2.0, stale since 2025-08), kitao/pyxel-mcp and pyxel-skill (Pyxel author's own, pushed 2026-10-09). All require a user-owned Aseprite 1.3+ licence where Aseprite is involved.
- Track: tooling
- Affects: artwright's division of labour: drawing and editing inside Aseprite is owned by these servers; artwright should own judgement (critique, checks, art direction) and point to them.
- Magnitude: n/a (initial)
- Suggested response: point (aseprite-ai-artist and diivi/aseprite-mcp as the "edit in Aseprite" route; pixel-art-studio as the no-Aseprite route). Do not rebuild a drawing engine.
- Sources: https://api.github.com/search/repositories?q=aseprite+mcp&sort=stars, https://github.com/with-pebbly/aseprite-ai-artist, https://github.com/Gamezxz/pixel-art-studio

### F2 · 2026-10-20 · Sprite Fusion Pixel Snapper is the most-starred "fix AI pixel art" tool
- What: Hugo-Dz/spritefusion-pixel-snapper (Rust CLI + WASM, MIT, created 2025-11-24, 3316 stars, pushed 2026-10-20, 0 open issues). Detects the pixel grid, snaps to it and quantises to a palette (auto k colours, default 16, or `--palette hex,...`), batch over a directory, `--pixel-size` override. Install via cargo or Homebrew. Has ComfyUI wrappers (x0x0b, 29 stars) and Python bindings (NoRaincheck/pixel-snapper, 2 stars). GIGAZINE covered it 2026-05-16. The README does not document the algorithm or its failure cases.
- Track: tooling
- Affects: the "AI output to real pixel art" procedure; comfyui-gen hand-off.
- Magnitude: n/a (initial)
- Suggested response: point (first-choice fixer when cargo is available; ComfyUI node inside comfyui-gen graphs).
- Sources: https://github.com/Hugo-Dz/spritefusion-pixel-snapper, https://api.github.com/repos/Hugo-Dz/spritefusion-pixel-snapper, https://www.gigazine.net/gsc_news/en/20260516-spritefusion-pixel-snapper

### F3 · 2026-10-10 · proper-pixel-art 2.0.0: the best-documented Python fixer
- What: KennethJAllen/proper-pixel-art (585 stars, pushed 2026-10-10, MIT); PyPI `proper-pixel-art` 2.0.0 released 2026-10-10, Python >=3.11, depends on numpy, opencv-python-headless, pillow, scipy, pyyaml, tqdm and PyAV (bundles a GPL FFmpeg build). Pipeline: trim and alpha <50% to background, 2x nearest upscale, Canny edges, morphological closing, probabilistic Hough for near-axis lines, per-axis spacing estimate reconciled and validated by within-cell colour variance, then one colour per cell (`dominant` default or `palette` with `-c N`). Animations: grid and palette fitted once over sampled frames, then applied to every frame to avoid flicker. CLI: `ppa in.png -o out -c 16 -s 1 -t`, `-w` to force pixel width, `--intermediate-dir` to dump each step. Stated limits: works best when the input is already roughly grid-aligned; can lock onto 2x the true width; palette size needs trial and error.
- Track: tooling
- Affects: same procedure; animation consistency (shared grid across frames is the lesson).
- Magnitude: n/a (initial)
- Suggested response: point (Python route, video/GIF route). Adopt its "fit once, apply to all frames" rule in artwright's sprite-sheet guidance.
- Sources: https://github.com/KennethJAllen/proper-pixel-art, https://pypi.org/pypi/proper-pixel-art/json

### F4 · 2026-09-29 · unfake.js / unfake.py: browser and Rust core, named scale detectors
- What: jenissimo/unfake.js (935 stars, pushed 2026-09-29, MIT) now has a headless Rust core `unfake-core` (WASM + native CLI `unfake detect|snap|downscale|quantize`) using libimagequant. Scale detection "runs-based" or "edge-aware", fractional grids, elastic grid for hand-drawn drift; downscale "dominant", "median", "content-adaptive"; alpha binarisation; jaggy cleanup. painebenjamin/unfake.py (63 stars, pushed 2026-07-30) is the Python port. The author's 2025-07-30 write-up gives the reusable method: Sobel X/Y on the highest-variance tiles, row/column edge profiles, histogram of peak spacings (mode = scale), brute-force offset 0..scale-1, dominant-colour vote with a 5% margin else mean, Wu quantisation, second quantise after downscale.
- Track: tooling
- Affects: a stdlib grid detector in artwright can copy this (it needs no OpenCV).
- Magnitude: n/a (initial)
- Suggested response: point (browser tool for humans); adopt the edge-profile method for artwright's own `detect-grid` check.
- Sources: https://github.com/jenissimo/unfake.js, https://dev.to/jenissimo/how-to-tame-your-ai-pixel-art-3pk5, https://api.github.com/search/repositories?q=unfake+pixel

### F5 · 2026-09-22 · Aseprite v1.3.18.6; Lua API version 41; licence is a source-available EULA
- What: Aseprite (40,277 stars, 2028 open issues) shipped v1.3.18.2 to .6 between 2026-08-11 and 2026-09-22; 1.3.18.2 set the Lua API version to 41 and added `save`/`beforesave` sprite events. The GitHub API reports no licence: the EULA allows compiling the source only for personal use or contributions and forbids redistributing binaries. LibreSprite (8624 stars, GPL-2.0, pushed 2026-10-21) is the fork of the last GPLv2 commit. CLI essentials for pipelines: `-b/--batch`, `--sheet`, `--data` (json-hash or json-array via `--format`), `--sheet-type` (horizontal, vertical, rows, columns, packed), `--split-layers`, `--list-tags`, `--scale`, `--palette`, `--color-mode indexed`, `--script` with `--script-param`. The `.aseprite` format is documented (little-endian, header magic 0xA5E0, frame magic 0xF1FA, zlib cels, chunk ids 0x2004 layer, 0x2005 cel, 0x2018 tags, 0x2019 palette, 0x2023 tileset) and is parseable with Python `struct` + `zlib`.
- Track: tooling
- Affects: any "read the .aseprite file" or "export the sheet" step; licence wording in artwright docs.
- Magnitude: n/a (initial)
- Suggested response: point (Aseprite CLI for export when installed); adopt the spec for a stdlib `.aseprite` reader if palette/tag checks on source files are wanted. Never bundle Aseprite.
- Sources: https://api.github.com/repos/aseprite/aseprite/releases, https://raw.githubusercontent.com/aseprite/aseprite/main/EULA.txt, https://www.aseprite.org/docs/cli/, https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md, https://www.aseprite.org/api/, https://api.github.com/repos/LibreSprite/LibreSprite

### F6 · 2026-09-25 · Slynyrd Pixelblog is the live canonical curriculum (64 entries)
- What: Raymond Schlitter's Pixelblog catalogue reaches #64 "Ninja Platformer" (2026-09-25). Topic anchors: #1 Color Palettes (2018), #8 Intro to Animation, #20/#43 Top Down Tiles, #22 Top Down Character Sprites, #25 Motion Cycles, #28 Side View Tiles, #41/#54/#61 isometric, #55 Top Down Character Animation (2025), #59 Tiny Sci-Fi Pixels (8x8 tiles, 2025-11). #1 gives checkable ramp numbers: 9 swatches per ramp, hue shift up to +20 degrees per step (author: "20 is about as high as I go"), brightness strictly rising, saturation never 0% or 100% and peaking mid-ramp, avoid high saturation with high brightness; 8 ramps 45 degrees apart; neutrals from desaturated middle columns. #2 Texture defines orphan pixels ("single pixel units not connected to a cluster of the same color ... usually avoided") and allows them inside a texture.
- Track: subject
- Affects: palette and ramp knowledge file; orphan-pixel check thresholds.
- Magnitude: n/a (initial)
- Sources: https://www.slynyrd.com/pixelblog-catalogue, https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes, https://slynyrd.com/blog/2018/2/15/pixelblog-2-texture

### F7 · 2026-10-21 · Lospec: 4533 palettes, 586 tutorials, a keyless per-palette API
- What: Lospec's palette list shows 4,533 palettes, filterable by exact/min/max colour count and tags, sortable by downloads. API: `https://lospec.com/palette-list/{slug}.json` returns `{name, author, colors:[hex...]}` (verified on `endesga-32`: 32 colours, author ENDESGA), `.csv` the same flat, 404 returns `{error:"file not found"}`; downloads also as PNG, JASC PAL, .ASE, .GPL, .HEX, Paint.net TXT. The API page states no rate limit and no attribution rule; there is no search/list endpoint, so slugs must be known. Tutorials: 586, tagged antialiasing, dithering, clusters, outlines, selectiveoutlining, isometric, walkcycle and more; Pixel Logic is marked Featured.
- Track: subject / tooling
- Affects: palette-match check (fetch named palettes by slug, cache them in the repo with attribution).
- Magnitude: n/a (initial)
- Suggested response: adopt (ship a small cached set: pico-8, dawnbringer-16, dawnbringer-32, endesga-32, sweetie-16, the four-shade Game Boy palette; fetch others on demand; verify each slug before shipping, only endesga-32 was verified here).
- Sources: https://lospec.com/palettes/api, https://lospec.com/palette-list/endesga-32.json, https://lospec.com/palette-list, https://lospec.com/pixel-art-tutorials

### F8 · 2026 · Hosted pixel-art generators now ship MCP servers and free grid fixers
- What: Retro Diffusion API v2 (`https://api.retrodiffusion.ai/v2`, `X-RD-Token`) has styles RD Fast/Plus/Pro/Mini, start-frame animations and 8-direction rotate, tilesets 16-32 px, `input_palette` with `return_pre_palette`, a `palette_converter` and `color_reducer`, free `pixel-fixer/standard` and `/neural`, low-poly 3D routes, and a hosted MCP at `mcp.retrodiffusion.ai/mcp` (33 tools). Its Aseprite extension is a one-time $65 (Lite $20) on itch.io and uses different models from the website. PixelLab API v2 (`api.pixellab.ai/v2`) has a hosted MCP (`api.pixellab.ai/mcp`, async job ids, 30 s to 5 min), 4/8-direction characters, `animate_character`, top-down, sidescroller and isometric tilesets, an official Aseprite plugin and a Pixelorama plugin; monthly subscription, commercial use on all tiers. Both are paid and need keys.
- Track: tooling
- Affects: generation route options for comfyui-gen-less users; artwright judges their output, does not call them by default.
- Magnitude: n/a (initial)
- Suggested response: point (with "needs the user's own key and paid plan"). Note the free Retro Diffusion Pixel Fixer as a hosted alternative to local fixers.
- Sources: https://github.com/Retro-Diffusion/api-examples, https://astropulse.itch.io/retrodiffusion, https://www.pixellab.ai/llms.txt, https://pixellab.ai/pixellab-api

### F9 · 2026-08-14 · Measured "fake pixel art": the numbers that define the failure
- What: Rangy asked for a 32x32, ~12-colour sprite; the raw file had 44,725 unique colours, apparent block width wandering 26 to 32 px, about 2% of colour changes on the true 32x32 lattice and ~4.5% transitional pixels. After nearest-neighbour downsample then quantise (dithering off, downsample before quantise), 100% of changes sat on block boundaries. ComfyUI-PixelArt-Detector reports a similar drop (58,325 to 120 colours). Retro Diffusion's founder lists the symptoms as varying pixel sizes, inconsistent outlines, blur and noise; artists call off-grid pixels "mixels".
- Track: practice
- Affects: the definition of done for any AI sprite: unique colours <= palette budget, 100% lattice alignment, uniform block size, zero transitional pixels.
- Magnitude: n/a (initial)
- Suggested response: adopt (these four numbers become the `pixel-check` pass/fail line and eval cases).
- Sources: https://rangy.ai/blog/ai-pixel-art, https://runware.ai/blog/retro-diffusion-creating-authentic-pixel-art-with-ai-at-scale, https://arcade.pirillo.com/pixel-rehab.html

### F10 · 2026 · Existing checkers define the check list artwright should match
- What: MalloyTheDev/aseprite-mcp's `assess_sprite` flags stray pixels ("no neighbour of their own colour"), jagged diagonals (uneven stair-steps), canvas use and centring, symmetry, colours and ramps, `palette_conformance` (fraction of art exactly on a declared ramp) and tile seams; `diff_sprites` reports silhouette added/removed, repaints, alpha-only changes with an `expect=` pass/fail; its export refuses on a measured defect unless `allow_defects=True`. Astropulse's Adopt Pixels uses a same-colour neighbour threshold. aseprite-ai-artist's critic writes a "cold read" before scoring, ships at 7/10, and keeps a fix only if it wins a blind A/B; its own early benchmark (mage 3 to 4/10) is called "not a measurement".
- Track: testing
- Affects: artwright's script checks and its critique procedure (cold read first, blind A/B for fixes).
- Magnitude: n/a (initial)
- Suggested response: adopt (same check names where sensible; cold-read-then-score and blind A/B in the judging skill).
- Sources: https://github.com/MalloyTheDev/aseprite-mcp, https://github.com/with-pebbly/aseprite-ai-artist, https://astropulse.gumroad.com/l/AdoptPixels

### F11 · 2019-2021, live · Derek Yu's tutorial pair: the checkable craft rules
- What: "Pixel Art Tutorial: Basics" (derekyu.com/makegames/pixelart.html): jaggies are single pixels or segments that break a line's consistency; on curves segment lengths must grow or shrink monotonically; AA in-between colours at segment joins, longer AA for longer segments, never AA the outside when the background is unknown; selective outlining (lighter outline where light hits, darker shadow colours instead of black inside); dithering sparingly on large flats or rough textures; 16 or 32 colours typical; banding = thick uniform bands that draw the eye to the seams. "Common Mistakes" (pixelart2.html): too many similar colours (each colour needs a role), pillow shading (shading from the outline inward), stiff "cardboard" designs, and the chunky-pixels rule (no one-pixel-thick limbs).
- Track: subject
- Affects: rules knowledge file; jaggy/line-run check; "outside AA" check on transparent sprites.
- Magnitude: n/a (initial)
- Sources: https://www.derekyu.com/makegames/pixelart.html, https://www.derekyu.com/makegames/pixelart2.html

### F12 · Pixel Logic (Michael Azzi) and saint11 remain the other canonical references
- What: Pixel Logic, a 242-page PDF (2022 revision, free update), chapters run from line art, anti-aliasing, colours, readability, dithering, perspectives, clean-up, sub-pixeling to animation; sold at michafrar.gumroad.com, featured on Lospec. Pedro Medeiros's (saint11) tutorial index at saint11.art/blog/pixel-art-tutorials/ is dated 2020-07-12 (walk/run/attack cycles, effects, tiles, isometric, subpixel, 9-slice UI, 1-bit); a 2022 reply says no new ones are planned. Both are reference-only and frozen; cite them, do not expect updates.
- Track: subject
- Affects: reading list in artwright's pixel-art knowledge file.
- Magnitude: n/a (initial)
- Sources: https://michafrar.gumroad.com/l/pixel-logic, https://80.lv/articles/pixel-logic-a-pixel-art-tutorial-book/, https://saint11.art/blog/pixel-art-tutorials/

### F13 · Integer scaling, one pixel grid, point filtering: the game-side lesson people redraw for
- What: A 2024 itch.io devlog ("chasing a pixel perfect tail") found non-integer scaling "a catastrophe" and even integer-scaled sprites showed thicker outlines next to unscaled ones; the fix was redrawing at target resolution. Unity's Pixel Perfect Camera guarantees an integer number of screen pixels per sprite pixel and warns that scaled or rotated sprites lose it; jam guides recommend one shared pixels-per-unit and point filtering; Godot uses viewport stretch with integer scale mode. Mixed scales are fixed by redrawing, not filtering.
- Track: practice
- Affects: a "consistent pixel density across a set" check (detected grid size must match for every sprite in a set) and engine hand-off notes for unity-agent and roblox-agent.
- Magnitude: n/a (initial)
- Suggested response: adopt (set-level density check; engine import notes: point filter, no compression, integer PPU, no rotation of pixel sprites).
- Sources: https://squeakypig.itch.io/unicopia/devlog/787703/a-tale-about-chasing-a-pixel-perfect-tail, https://discussions.unity.com/t/released-pixel-perfect-camera/633246

### F14 · Animation conventions: few frames, uneven holds, shared grid
- What: Sources agree on 4 to 8 frames for walks (4-frame since NES; 6 as a smooth minimum), 2 to 4 for idles, 8 to 12 fps typical, 100 ms per frame as the common tool default, holds of 200 to 400 ms on anticipation and impact; extra in-betweens expose inconsistency. These are conventions, not standards. AI-generated sheets drift between frames (head size, light angle, detail level); remedies are a fixed reference, a locked idle pose and a shared grid and palette across frames (F3). Slynyrd #8, #25, #55 and saint11's cycle sheets are the visual references.
- Track: subject / practice
- Affects: animation-consistency check (same palette, same grid, bounding-box and baseline stability, silhouette-area variance across frames).
- Magnitude: n/a (initial)
- Suggested response: adopt (frame-consistency check reporting per-frame colour set, bbox, foot baseline, area delta).
- Sources: https://www.slynyrd.com/blog/2020/1/23/pixelblog-25-motion-cycles, https://www.sprite-ai.art/blog/sprite-animation-frames, https://morphic.com/ai-glossary/sprite-sheet

### F15 · Dithering: ordered (Bayer) reads as deliberate, error diffusion reads as noise
- What: Error diffusion (Floyd-Steinberg) spreads rounding error irregularly and speckles flat areas; ordered Bayer uses a fixed threshold matrix, keeps flats and edges hard and gives the regular pattern pixel artists use by hand. Quantisers used on AI output (Rangy) turn dithering off; Aseprite's `--color-mode indexed` exposes dithering options. Derek Yu: dither sparingly, on large flats or rough textures.
- Track: subject
- Affects: quantise defaults (no dither, or ordered only on request); a "diffusion noise" heuristic (many isolated pixels alternating between two ramp neighbours in flat regions).
- Magnitude: n/a (initial)
- Sources: https://www.graphicsmill.com/docs/gm5/BasicConceptsofColorReduction.htm, https://www.derekyu.com/makegames/pixelart.html

### F16 · Tiles: 16-tile corner sets vs 47-tile blob sets; generators exist
- What: Corner-based terrain (Tiled Wang/corner sets) caps at 2^4 = 16 tiles; full 8-neighbour blob sets need 47. Godot 4 terrains paint per tile with peering bits. Generators: Blobsmith (47 tiles from six bases, exports Godot 4 TileSet and Tiled .tsx), Blobsmith Autotile Wirer (MIT Godot addon), TerrainForge, AutoBlob (Aseprite script); a CC0 16 px blob-47 starter pack ships .tres and .tsx. Sheets often carry margin and spacing (4 px / 2 px in one pack) against bleeding. No primary source for an automated seam test was found; the obvious test is edge-pixel comparison of opposite borders and of declared neighbours.
- Track: subject / tooling
- Affects: tile seam check; tileset knowledge.
- Magnitude: n/a (initial)
- Suggested response: point (Blobsmith, AutoBlob); adopt a stdlib seam check (wrap-around edge diff, 2x2 and 3x3 tiled preview render).
- Sources: https://discourse.mapeditor.org/t/neither-terrain-nor-wang-can-handle-a-blob-tileset/4671, https://blobsmith.itch.io/blobsmith, https://godotengine.org/asset-library/asset/5343

### F17 · Open-source editors: Pixelorama and Piskel active, LibreSprite alive
- What: Pixelorama (Godot-based, MIT, 10,604 stars) released v1.2.3 on 2026-09-15 and has a PixelLab plugin. Piskel (Apache-2.0, 12,858 stars, pushed 2026-10-21, not archived). LibreSprite (GPL-2.0) active. Pyxel Edit and GraphicsGale were not checked in this pass (budget). Aseprite stays the de facto standard for agents because of its CLI, Lua API and documented file format.
- Track: tooling
- Affects: tool recommendations ("free and open" route = Pixelorama or LibreSprite).
- Magnitude: n/a (initial)
- Suggested response: point.
- Sources: https://api.github.com/repos/Orama-Interactive/Pixelorama/releases, https://api.github.com/repos/piskelapp/piskel, https://api.github.com/repos/LibreSprite/LibreSprite

### F18 · 3D art direction: Blender has no built-in toon mode yet; NPR project planned after 5.0; PS1 look is shader recipes
- What: Blender's NPR project (code.blender.org, 2025-05-23) redesigned NPR around per-object/material multi-stage compositing plus renderer features (ray queries, custom shading, depth offset) for both EEVEE and Cycles; development was to start after Blender 5.0 (Nov 2025); no shipped version was confirmed in this pass. Today stylisation uses Shader-to-RGB setups, community node groups, Goo Engine (a studio fork) or paid add-ons. PS1 style = vertex snapping (quantise clip/screen position), affine UV warping (undo perspective divide), low-res nearest textures, colour-depth reduction and dithering, and subdividing geometry to tame warping; Godot has an MIT "PS1 / PSX Visuals - GD4 Port" (2026-01-25) and MenacingMecha's demo.
- Track: subject
- Affects: 3D art-direction knowledge file and the hand-off to polywright (style briefs, not shader code).
- Magnitude: n/a (initial)
- Suggested response: point (polywright-blender for bpy work; the Godot PSX assets as references).
- Sources: https://code.blender.org/2025/05/npr-project/, https://www.strayspark.studio/blog/best-blender-toon-shader-addons-2026, https://github.com/MenacingMecha/godot-psx-style-demo, https://www.godotengine.org/asset-library/asset/4687

### F19 · LoRAs: still SDXL/Flux-era, outputs still need a grid fixer
- What: Pixel Art XL (nerijs, SDXL, OpenRAIL-M) tells users to downscale 8x with nearest neighbour; a Flux.1-dev pixel LoRA (deAPI-ai) carries the FLUX.1 [dev] non-commercial licence; Pixel Icon LoRA (SDXL, 522 hand-made 16x16 icons, use 0.6-0.8 weight). No Qwen-Image pixel LoRA was found. ComfyUI-PixelArt-Detector (451 stars) last pushed 2025-10-31; ComfyUI-DeGrid (94, 2026-10-17) removes a 2 px VAE grid artefact. Whatever generates, a grid fix plus palette step is still required.
- Track: practice / tooling
- Affects: comfyui-gen hand-off (generate at an integer multiple of the target size, then fix); licence warnings for Flux dev LoRAs in commercial games.
- Magnitude: n/a (initial)
- Suggested response: note (licence caveat), point (Pixel Snapper or ppa node after generation).
- Sources: https://www.promptlayer.com/models/pixel-art-xl, https://huggingface.co/deAPI-ai/pixelartdotfluxlora/blob/main/README.md, https://huggingface.co/lizozom/pixel-icon-lora-sdxl, https://api.github.com/repos/dimtoneff/ComfyUI-PixelArt-Detector

### F20 · No accepted metric or benchmark for pixel-art quality
- What: No 2025-2026 paper defining grid-alignment or palette-fidelity metrics was found; SD-piXL (arXiv 2410.06236, 2024) treats palette adherence as a decoding property. Pixel Art Bench has LLMs emit a 2-10 colour palette and a 24x24 index grid, judged pairwise by an LLM with Elo; its validity checks are structural only. aseprite-ai-artist's benchmark is self-described as early. The measurable checks are the deterministic ones (F9, F10); aesthetic judgement remains VLM-plus-rubric.
- Track: testing
- Affects: evals: deterministic checks get hard assertions; critique quality gets rubric/A-B cases.
- Magnitude: n/a (initial)
- Suggested response: adopt (two-tier evals: script assertions on fixture sprites; rubric-graded critique cases).
- Sources: https://arxiv.org/pdf/2410.06236, https://www.emergentmind.com/pixel-art-bench

## Overall magnitude: n/a (initial)

## Open questions
- new: Pixel Snapper's algorithm and failure cases are undocumented; a fixture comparison of Pixel Snapper vs proper-pixel-art vs unfake on the same AI sprites would settle which to recommend first.
- new: Lospec terms of use (caching palettes in a public repo) were not read; check lospec.com terms before shipping palette files; attribute each palette's author.
- new: Has Blender's NPR project shipped in 5.1 or 5.2? Not confirmed.
- new: Pyxel Edit, GraphicsGale, Krita, Procreate, Clip Studio current versions not checked (search budget); low risk for artwright's claims.
- new: r/PixelArt and Lospec policies on AI-generated art were not found by search; read the subreddit rules directly before advising users to post there.
- still open: no source for an automated tile-seam test; artwright will define its own.

## Search plan notes
- Subject: Slynyrd catalogue page and Derek Yu pages fetched directly were the best primary sources; search engines rarely surface them. saint11's index is at saint11.art (frozen 2020). Lospec's `palette-list/{slug}.json` and the tutorial tag list work without keys.
- Tooling: GitHub REST search (`q=unfake+pixel`, `q=proper-pixel-art`, `q=pixel+snapper`, `q=aseprite+mcp`, `topic:pixel-art+mcp`) was the most productive single source; PyPI JSON for versions; `llms.txt` (PixelLab) and the api-examples README (Retro Diffusion) beat marketing pages. A query for "pixel art AI downscale" returned only one zero-star repo: search by tool names instead.
- Practice: dated practitioner write-ups (jenissimo on dev.to, Rangy 2026-08-14, an itch.io devlog) beat forum searches; Reddit was not reachable through search. Generic "AI sprite sheet drift" queries returned SEO glossaries.
- Testing: arXiv search found nothing 2025-2026 specific; the testing track is best served by reading existing checkers (MalloyTheDev `assess_sprite`, aseprite-ai-artist critic loop).
- Forums lacking from a plan: community.aseprite.org, pixeljoint.com forum, lospec.com, discourse.mapeditor.org (Tiled).

## Tracks covered: subject: 9 queries · tooling: 9 · practice: 5 · testing: 4 (queries counted across WebSearch and API searches; several served two tracks)

## Upcoming events: none dated. Watch: Blender NPR project landing version; Aseprite 1.3.19 / 1.4; Lospec API changes.

## Nothing changed: no (creation pass)

## Proposals for artwright
- **Stdlib PNG reader first.** A ~150-line `zlib`+`struct` PNG decoder (8-bit RGBA/RGB/palette, non-interlaced; refuse others with a clear message) is enough for every check below on sprites up to a few hundred pixels; Pillow is optional, used when present for speed and odd formats. Keep numpy out of the core.
- **`detect-grid`**: estimate native pixel size and offset with the unfake edge-profile method (row/column colour-change profiles, histogram of run lengths/peak spacings, test offsets 0..s-1), report block size, uniformity (min/max apparent width) and lattice alignment % (Rangy's metric). Pass: one integer size, 100% alignment.
- **`colours` and `palette-match`**: unique colour count vs budget (default 16 at 64x64, 12 at 32x32, warn above 32), and nearest-colour distance to a named Lospec palette (CIEDE2000 or simple Lab in pure Python), reporting off-palette pixel share. Ship a cached handful of palettes with author attribution; fetch others from `lospec.com/palette-list/{slug}.json`.
- **`orphans` and `jaggies`**: count pixels with no same-colour 4- or 8-neighbour (threshold like Adopt Pixels), excluding pixels inside dither patterns; flag outline runs whose segment lengths are not monotonic along a curve (Derek Yu's rule). Report coordinates so a fixer or Aseprite MCP can act.
- **`alpha` and `outline`**: alpha must be binary (0/255) for pixel sprites; flag semi-transparent edge pixels and outside anti-aliasing; outline consistency = share of silhouette boundary pixels in the outline colour set, broken-outline gaps, one-pixel thickness.
- **`seams`** for tiles: compare opposite edges for wrap tiles and declared neighbour edges for sets; render a 3x3 tiled preview at integer scale for the VLM judge.
- **`frames`** for sheets: same palette, same detected grid, bbox and foot-baseline stability, silhouette-area delta per frame; slice by grid or by Aseprite JSON (`--data` output).
- **`upscale-preview`**: integer nearest-neighbour upscale (and contact sheet) for every human or VLM review; never show a bilinear-scaled sprite to a judge.
- **Point, do not rebuild**: grid fixing to Sprite Fusion Pixel Snapper (cargo/brew, ComfyUI node) or proper-pixel-art (`ppa`, pip; note the GPL FFmpeg in PyAV for redistribution) or unfake (browser); editing to aseprite-ai-artist / diivi aseprite-mcp (user's own Aseprite licence) or pixel-art-studio (Pillow); generation to comfyui-gen, Retro Diffusion or PixelLab (user's paid key); tilesets to Blobsmith/AutoBlob.
- **Judging procedure**: cold read before scoring, rubric covering readability at 1x, silhouette, palette roles, clusters, outlines, light direction (no pillow shading), banding, density consistency; fixes accepted only by blind A/B (aseprite-ai-artist's loop).
- **Knowledge files**: `pixel-art-rules.md` (the rules above with sources), `palettes.md` (ramps, hue shifting numbers from Slynyrd #1, named palettes), `ai-pixel-art.md` (why diffusion fails, the four numbers, fixer comparison), `sprites-and-tiles.md` (frame counts, timing, sheets, blob-47 vs 16, isometric 2:1), `engine-import.md` (point filter, integer PPU, pixel-perfect camera, no rotation), `3d-stylisation.md` (toon/NPR, low-poly, PS1 recipe) pointing to polywright.
- **Evals**: fixtures of a clean sprite, an AI-fake sprite, a mixed-scale set, a seamed and a seamless tile, and a drifting sheet, each with hard assertions on the check outputs.

## Cost: searches 21 · fetches 45 · tool calls 71
