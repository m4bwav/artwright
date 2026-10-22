# Creation pass 2026-10-21: G. tooling and efficiency (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation. Magnitudes are `n/a (initial)`. Tracks: tooling (existing skills, plugins, MCP servers), tooling (image libraries for `aw.py`), practice (token-saving image handling), sibling boundaries.

## Findings (newest first)

### F1 · 2026-10-21 (docs read today) · Claude's image cost is now a 28 px patch count, with a high-resolution tier on 4.7+ models
- What: The vision docs now price images as `ceil(width/28) x ceil(height/28)` visual tokens, not the old `width*height/750`. Two tiers: Claude 4.7 and later read up to a 2576 px long edge and 4784 visual tokens; all other models 1568 px and 1568 tokens. A 1920x1080 frame costs 2691 tokens on the high tier (1560 on standard), and a 4K frame 4784. Limits: 8000x8000 px per image; 20 images per claude.ai message; 100 per API request on 200k-context models, 600 on others; above 20 images in one request a stricter per-image limit applies (stay at or under 2000 px a side); 10 MB per image on the API (5 MB on Bedrock and Vertex); JPEG, PNG, GIF (first frame only), WebP. Images placed before the text do slightly better. Label each image `Image 1:` and so on when sending several. Claude reads no metadata and "cannot determine whether an image is AI-generated".
- Track: practice
- Affects: every artwright step that puts an image in context; the token budget table in the main file; any "is this AI-made" request (must refuse to judge on pixels alone)
- Magnitude: n/a (initial)
- Suggested response: adopt. `aw.py fit` should size images to the tier (a 1568 px long edge covers both tiers; 1000x1000 = 1296 tokens is a good default for a single critique), and `aw.py sheet` should cap sheets at 2000 px a side so many-image requests never trip the stricter limit.
- Sources: https://platform.claude.com/docs/en/build-with-claude/vision

### F2 · 2026-10-18 · aseprite-ai-artist ships the best worked pixel-art critic loop found (cold read, score, blind A/B)
- What: with-pebbly/aseprite-ai-artist (MIT, 442 stars, created 2026-09-08, pushed 2026-10-18, 4283 npm downloads last month for `@pebbly/aseprite-ai-artist`) drives a live Aseprite through MCP with a text "grid loop": the agent reads and writes the canvas as one character per pixel instead of screenshots. Its read-only `pixel-critic` agent does a cold read before seeing the brief (what the image shows, the three things the eye notices first; missing the subject is blocking), then mechanical checks, full-zoom key frames ("downscaled filmstrips can hide broken shapes"), a rule citation per finding, a 0-10 score (7+ ships), one highest-value fix, and is forbidden to say "looks good". Fixes are kept only if the critic prefers them in a blind A/B with neutral labels. 62 rules, about 400 templates and 2006 palettes are served as MCP resources. The author calls the benchmark (3 prompts, scores 3-4/10) "early signal, not a measurement". Needs Node 22.6+ and Aseprite 1.3+ (paid, or built from source).
- Track: tooling
- Affects: artwright's pixel-art critique procedure and its pairwise comparison method
- Magnitude: n/a (initial)
- Suggested response: adopt the method (cold read first, priority-ordered issue list, no "looks good", blind A/B with swapped order), point to the tool for drawing and editing in Aseprite. Do not rebuild an Aseprite bridge.
- Sources: https://github.com/with-pebbly/aseprite-ai-artist, https://raw.githubusercontent.com/with-pebbly/aseprite-ai-artist/main/agents/pixel-critic.md

### F3 · 2026-10-21 · diivi/aseprite-mcp is the most-starred Aseprite MCP and already has pixel QA tools
- What: Python MCP server (MIT, 726 stars, pushed 2026-10-21, 3 open issues), 123 tools. Besides drawing it has `view_sprite` (zoom, pixel grid, rulers), `read_rows`, `compare_frames` (pixel change counts and bounds), `lint_sprite` (lone and orphan pixels), `get_color_stats` (palette drift, near-duplicate colours), `render_onion_skin`, `audit_animation`. Needs Python 3.13+, uv and a local Aseprite. `run_lua_script` runs unrestricted code on the host. No test suite mentioned. Other Aseprite servers in the MCP registry: oaktreegames/aseprite-live-mcp (0.2.0, art QA, Unity export) and SarutobiSasuke8/aseprite-agent-mcp (0.3.0, 2026-10-16). willibrandon/pixel-plugin (378 stars) and pixel-mcp (154) have not been pushed since 2025-10-18: stale.
- Track: tooling
- Affects: pixel-art section (which checks artwright runs itself versus hands to an editor)
- Magnitude: n/a (initial)
- Suggested response: point (named as the edit route when the user has Aseprite). artwright's own pixel checks (stray pixels, palette count, near-duplicate colours, alpha that is neither 0 nor 255, mixed pixel scale) should work on a plain PNG with no Aseprite, since most agent-made pixel art arrives as PNG from an image model.
- Sources: https://github.com/diivi/aseprite-mcp, https://registry.modelcontextprotocol.io/v0/servers?search=aseprite

### F4 · 2026-10-16 · Pillow 13.0 dropped Python 3.9 and 3.10; numpy 2.5 needs 3.12
- What: PyPI JSON, read today. Pillow 13.0.0 (2026-10-16, MIT-CMU) requires Python >=3.11 and has wheels cp311 to cp315: about 7.3 MB on Windows, 4.8 to 5.6 MB on macOS, 5.5 to 7.2 MB on manylinux. The last Pillow for 3.9 is 11.3.0; 12.x needs 3.10. numpy 2.5.4 needs 3.12 and its wheels are 12.6 to 17 MB. imagehash 4.3.2 (0.3 MB, last release 2025-02-01) pulls numpy, scipy (20 to 37 MB) and PyWavelets (4.3 MB): about 45 to 60 MB for four hash functions. scikit-image 0.26.0: 12 to 14 MB plus scipy, networkx, imageio, tifffile. opencv-python-headless 5.0.0.93: 35 to 61 MB. colorthief 0.2.1 dates from 2017; haishoku 2019; extcolors 2020: unmaintained.
- Track: tooling
- Affects: dependency decision and the package-size budget
- Magnitude: n/a (initial)
- Suggested response: adopt. Standard library core; Pillow optional (pin nothing, accept `>=11`); never numpy, scipy, imagehash, scikit-image or OpenCV. Hashes, palettes and stats are a few dozen lines each over a downscaled pixel grid.
- Sources: https://pypi.org/pypi/pillow/json, https://pypi.org/pypi/pillow/11.3.0/json, https://pypi.org/pypi/numpy/json, https://pypi.org/pypi/imagehash/json, https://pypi.org/pypi/scipy/json, https://pypi.org/pypi/opencv-python-headless/json, https://pypi.org/pypi/scikit-image/json, https://pypi.org/pypi/colorthief/json

### F5 · 2026-10-21 (measured today) · A stdlib PNG decoder is fast enough; JPEG and WebP go through ffmpeg
- What: A 45-line pure-Python PNG decoder (zlib plus the five row filters) decoded a 1024x1024 RGB PNG in 0.12 s (mostly Sub and Up filters) and a noisy photo-like one in 0.24 s (Average filter on 1002 of 1024 rows), byte-identical to Pillow, on Python 3.14 on Windows. Older Pythons are slower (assume up to about 3x on 3.9 to 3.10). Palette, 16-bit and Adam7-interlaced PNGs need small extra code paths. JPEG and WebP are not practical in pure Python, but `ffmpeg -i in.jpg -vf scale=64:64 -f rawvideo -pix_fmt rgb24 -` returns raw pixels on stdout in 0.08 s, so any format ffmpeg reads becomes a stdlib pixel grid. Writing PNG with zlib is trivial.
- Track: tooling
- Affects: `aw.py` architecture
- Magnitude: n/a (initial)
- Suggested response: adopt. Decode order: Pillow if importable, else stdlib PNG, else ffmpeg rawvideo, else a clear error naming the missing piece.
- Sources: local benchmark (script not kept in repo); https://ffmpeg.org/ffmpeg-filters.html#tile

### F6 · 2026-10-21 (measured today) · ffmpeg `tile` makes contact sheets of stills too; `drawtext` labels fail on Windows without a font file
- What: `ffmpeg -i f%d.jpg -vf "scale=256:-1,tile=3x2:padding=4:color=white" -frames:v 1 sheet.png` produced a 776x516 sheet from six stills. Adding `drawtext` failed on Windows with "Fontconfig error: Cannot load default config file", so labels need an explicit `fontfile=` or must be drawn another way (Pillow `ImageDraw`, or a stdlib 5x7 bitmap font for the index numbers only). cinewright-qc and polywright already make one sheet per review for the same token reason.
- Track: practice
- Affects: `aw.py sheet` and the label convention
- Magnitude: n/a (initial)
- Suggested response: adopt. Label cells with short ids (A, B, C) drawn by artwright itself, not by drawtext; keep the id-to-file map in the JSON output so the verdict can name files.
- Sources: https://ffmpeg.org/ffmpeg-filters.html#tile

### F7 · 2026-10-15 · Museum MCP servers exist and are active; open-museum-mcp is the multi-museum one
- What: cfpramod/open-museum-mcp (MIT, 14 stars, pushed 2026-10-22, 508 npm downloads last month, CI) searches the Met, Rijksmuseum, Smithsonian, Cleveland, AIC, SMK, Walters, Wellcome, NGA, Harvard, Getty, Wikimedia Commons and Europeana in one normalized shape, drops any record with ambiguous rights, and emits three citation styles. Single-museum servers: mikechao/metmuseum-mcp (35 stars, 1055 npm downloads last month, last push 2026-04-27), cyanheads/met-museum-mcp-server (Apache-2.0, 0.9.0 on 2026-10-15, very frequent releases), pipeworx-io Met, Rijksmuseum, Harvard and V&A wrappers (2 stars each), r-huijts/rijksmuseum-mcp (72 stars, not pushed since 2025-02-07: stale). historywright-pack already pulls reference images from museum collection records with licence and accession number.
- Track: tooling
- Affects: art-history facts and comparison images
- Magnitude: n/a (initial)
- Suggested response: point. artwright should not query museum APIs itself; art-history facts and museum records go through historywright (and historywright-sources owns where they live); open-museum-mcp is the named option for users who want an MCP.
- Sources: https://github.com/cfpramod/open-museum-mcp, https://registry.modelcontextprotocol.io/v0/servers?search=museum, https://api.npmjs.org/downloads/point/last-month/open-museum-mcp

### F8 · 2026-10 · The skill market for art critique is thin; pixel-art generation skills dominate installs
- What: skills.sh search "art critique" returns 70 skills, none of them a real art critic with more than a few installs: art-director (heymoezy/porter) 4, review-art 1, critique 1, aesthetic (yoshi-ortiz) 28. The large counts there are graphics builders (threejs-aaa-graphics-builder 3087) and design tools. "pixel art": layer-pixel-art (layerai/skills) about 3.1K installs, first seen 2026-09-17, tied to the paid Layer service; pixel-art-sprites (omer-metin) 2627; willibrandon pixel-plugin skills 148 to 244. "art history": museum-curator (theneoai) 19, image-analysis-art 8, aesthetic-critic-historian 4. GitHub code search finds 68 SKILL.md files mentioning "art critique" (yamatakeru/art-critique-skills, 0 stars; FerroxLabs art-critic) and curiositech's photo-composition-critic (repo 252 stars): a long knowledge dump (visual weight, Gestalt, dynamic symmetry, NIMA score bands) with no scripts that compute anything and harmony "scores" asserted without a source.
- Track: tooling
- Affects: positioning: artwright is not duplicating a used tool
- Magnitude: n/a (initial)
- Suggested response: note. Worth borrowing from photo-composition-critic only its anti-pattern framing ("rule of thirds is not a rule", "ML aesthetic score is one input"); verify any number before using it.
- Sources: https://skills.sh/api/search?q=art%20critique, https://skills.sh/api/search?q=pixel%20art, https://skills.sh/api/search?q=art%20history, https://github.com/curiositech/some_claude_skills

### F9 · 2026-10 · Anthropic's official catalog makes art, it does not judge it
- What: anthropics/skills has 19 skills; the visual ones are algorithmic-art, canvas-design, frontend-design, theme-factory, brand-guidelines, slack-gif-creator. canvas-design writes a design philosophy and then one PNG or PDF; its self-review is a polish pass (no overlaps, margins, "museum quality"). claude-plugins-official has 40 plugins; frontend-design is the only visual one. No official critique, style-identification or image-comparison skill exists.
- Track: tooling
- Affects: boundaries (artwright judges; these make)
- Magnitude: n/a (initial)
- Suggested response: point. artwright can be the reviewer called after canvas-design or algorithmic-art output, the same way it is called from comfyui-gen.
- Sources: https://github.com/anthropics/skills/tree/main/skills, https://github.com/anthropics/claude-plugins-official/tree/main/plugins

### F10 · 2026 · Pairwise VLM judging has measured position bias; run both orders
- What: A 2026 app-generation benchmark reports a 23.3% position bias in pairwise VLM judging and needs swap-augmented reruns; "Fooling the LVLM Judges" (2505.15249) runs every pair in both orders and shows visual manipulations sway judges; a realism-evaluation paper (2603.04325) cites pairwise preferences flipping in about 35% of cases under distractors versus 9% for absolute scores. cinewright-qc already ranks takes "two at a time, both orders", and its local judge was right 228 of 231 times only when it said yes in both orders.
- Track: testing
- Affects: artwright's compare procedure and its evals
- Magnitude: n/a (initial)
- Suggested response: adopt. Compare in both orders with neutral labels; a pick that flips is a tie. Add an eval case where the better image is shown second.
- Sources: https://arxiv.org/pdf/2607.28645, https://arxiv.org/html/2505.15249v2, https://arxiv.org/pdf/2603.04325

### F11 · 2024-2026 · Vision models attribute artists better than they ground style claims
- What: A 2026 token-activation study of multimodal models describing artworks finds concrete tokens (objects, iconography) land on the right regions while abstract ones (style, affect) are diffuse, and that artist attribution beats title prediction, where hallucination is common. The 2024 zero-shot study (2409.03521) tested CLIP, LLaVA and GPT-4o on style, author and period. No standard 2026 benchmark for style attribution was found. (The search tool flagged some IDs as unusual; verify before citing in the main file.)
- Track: testing
- Affects: style and movement identification: require visible evidence per claim
- Magnitude: n/a (initial)
- Suggested response: adopt. Every style or movement claim names the visible features that support it and a confidence; titles and dates of named works come from historywright, never from the image.
- Sources: https://arxiv.org/abs/2606.27947, https://arxiv.org/abs/2409.03521v2

### F12 · 2026-06 · Claude Code's Read tool once overestimated image cost and over-compressed screenshots
- What: An issue reported that Claude Code's Read tool estimated a 1280x713 screenshot at about 74,000 tokens against about 1,200 by the API formula, and compressed images needlessly; it is marked resolved 2026-06-25 (fix not described in the result). A third-party article notes 4.7+ models read a 2400x1350 screenshot at about 4,200 tokens instead of 1,560. tinyscreenshot (PyPI) claims 540 instead of 2,100 tokens per capture (vendor claim).
- Track: practice
- Affects: why `aw.py fit` sizes images itself rather than relying on the harness
- Magnitude: n/a (initial)
- Suggested response: note. Size images before Read; never rely on the host to downscale well.
- Sources: https://claudeissues.com/issue/70010-bug-read-tool-massively-overestimates-image-token-cost-causing-unnecessary-quali, https://pub.towardsai.net/claude-sees-screenshots-sharper-now-your-agent-can-send-2-7x-the-tokens-73dabc991398

### F13 · undated guides · dHash near-duplicate thresholds are data-specific; hashes are not portable across libraries
- What: dHash uses a 9x8 grayscale grid (64 bits); practitioners start at 5 to 10 differing bits, tune per data set, and warn that hashes from different libraries differ in bit order, resize filter and size, so the library and version must be stored with each hash. dHash breaks under crops, flips and rotations. No source on generated-image seed batches specifically.
- Track: practice
- Affects: `aw.py hash` and `aw.py dedupe`; the verdict cache key
- Magnitude: n/a (initial)
- Suggested response: adopt. Store `{algo, version, bits}` with each hash; calibrate the threshold on a sample of the user's own renders and record it; key the verdict cache by SHA-256 of the file bytes plus rubric id and version (exact), using dHash only to group near-duplicates for one shared review.
- Sources: https://benhoyt.com/writings/duplicate-image-detection/, https://mojoauth.com/security-guides/dhash-in-python

### F14 · 2026 · Sycophancy in art critique is unmeasured; critics accept the framing they are given
- What: No study measures "looks good" praise in drawing critique. A 2025 study found people struggled to tell LLM art critiques from experts' but did not test honesty; LSE commentary says LLMs default to sycophancy and critical personas surface more issues; a May 2026 anecdote has a real Monet accepted as "AI-made" by forum critics who took the framing at face value. pixel-critic's ban on "looks good" plus a cold read before the brief is the only worked guard found.
- Track: testing
- Affects: critique procedure and eval cases
- Magnitude: n/a (initial)
- Suggested response: adopt. Cold read before the brief or the user's framing; findings must name a location and a rule; add an eval that gives a deliberately weak image with a proud framing and expects concrete faults.
- Sources: https://arxiv.org/pdf/2504.12805, https://lse.ac.uk/DSI/AI/AI-Research/Feedback, https://www.promptzone.com/karan_reddy/monet-painting-masquerades-as-ai-in-hn-critique-test-4aal.md

### F15 · 2026-07 to 2026-10 · Pixel-art generation MCPs exist; artwright judges their output
- What: MCP registry: Retro Diffusion pixel-art (1.1.0, 2026-07-10, sprites, animations, tilesets), Sprite Fusion pixel-art-generator (1.0.0, 2026-10-12, no repo listed), Gamezxz/pixel-art-studio skill (89 stars, no Aseprite needed). Hosted and paid.
- Track: tooling
- Affects: none beyond a "where art comes from" pointer
- Magnitude: n/a (initial)
- Suggested response: note.
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=pixel, https://github.com/Gamezxz/pixel-art-studio

## Sibling boundaries

Read from each sibling's SKILL.md frontmatter and opening lines. "Calls artwright" is where a hand-off fits; none of the siblings call artwright yet.

| Sibling | Its territory | artwright must not claim | Where it calls artwright |
|---|---|---|---|
| cinewright (director, shots, continuity, genvideo, qc) and cinewright-craft (camera, design, sets, history, edit, finish, sound, voice, movement, script) | AI film end to end. cinewright-qc judges video takes against shot cards with contact sheets, rubric, failure codes and both-order ranking. cinewright-history owns film movements, eras, directors and cinematographers as style-bible cards. cinewright-design owns turnarounds, costume and colour script; -camera lighting and lenses; -finish grading. | Judging a video take against its shot card; film-history style cards; continuity; grade and colour pipeline; video model prompts. | Fine-art references in a style bible ("lit like a Caravaggio", "Hokusai palette"): cinewright-history or -design asks artwright for the painting-side vocabulary and visual evidence. Single-frame art critique of a key frame or concept image before rendering. cinewright-qc can hand a frame to artwright's composition check. |
| polywright (hub plus references, capture, generate, blender, finish, print) | 3D models for games, print, video, AR; asset folder with `brief.md`, `manifest.json`, `refs/`, `work/`, `out/`, `renders/`; `pw.py` renders one contact sheet per render; references owns orthographic views, turnarounds and seamless textures. | Mesh quality, topology, game-readiness, printability, reference-sheet production, texture maps, the manifest format. | Judging concept art before image-to-3D, and judging rendered turnarounds or sheets for silhouette, proportion, style and colour. artwright reads the asset folder (`renders/`, `brief.md`) and writes its verdict beside them, never edits `manifest.json`. |
| comfyui-gen | Generating images, sprites, icons, video on the local ComfyUI hosts; host selection and queueing. | Generation, workflows, host management, prompt settings. | After a batch: dedupe near-identical seeds, contact-sheet the survivors, rank in both orders, and send one change back for the next prompt. This is artwright's main caller. |
| historywright (hub, sources, pack) | Cited history answers; where sources live (museums included); research packs with museum reference images, licence and accession number, anachronism checklist. | Dates, attributions of named works, artist biographies, provenance, museum record lookup, licence of reference images. | artwright asks historywright for any art-history fact it states (who painted it, when, which movement's dates). historywright-pack asks artwright to check that generated images match the period references (style, palette, costume read as art, not as fact). |
| brandwright (hub, capture, train, mockup) | On-brand UI mock-ups from a brand's sites: tokens to `brand.css`, LoRAs, weight sweeps with contact sheets, delta-E palette score against the brand. | Brand palette scoring, UI mock-up generation, LoRA training, design-token extraction. | Taste and composition review of mock-up candidates after `BW score` ranks them by palette distance; artwright judges hierarchy, balance and craft, not brand fidelity. |
| sitewright (hub, direction, build, audit, curate) | Personal-site redesign: direction picks a committed visual direction, type pairing and palette into DESIGN.md (WCAG contrast linted); audit finds AI-look tells. | Choosing a website's direction, fonts or palette; contrast checks; AI-look web tells. | sitewright-direction can ask artwright to analyse the user's own artwork or a reference image (palette, movement, mood) so the site's direction ties to their real work; artwright returns analysis, sitewright decides. |
| musicwright | Music generation, theory, production, game music, scoring to film. | Anything audio. | None in normal use; album or cover art review only. |
| Anthropic canvas-design, algorithmic-art, frontend-design | Making posters, generative art, front ends. | Making art. | As the reviewer after they produce a PNG. |

## Proposals for artwright

- **`aw.py` command list (one JSON object per command, fail soft, like `pw.py` and `cine.py`):** `doctor` (Python, Pillow present or not, ffmpeg on PATH); `info` (size, mode, alpha use, format, SHA-256, tokens on each tier from F1's formula); `fit` (downscale to a target long edge or token budget, crop a region by box or by grid cell, never upscale except nearest-neighbour for pixel art); `sheet` (contact sheet of N images or of video frames, cells labelled A, B, C, at most 2000 px a side, id-to-file map in the JSON); `palette` (k dominant colours by median cut on a downsampled grid, with share, hex and a named-colour hint; `--against` a reference palette gives delta-E like brandwright's score); `stats` (value histogram and contrast, saturation, warm/cool split, edge density, centre of visual mass, thirds and symmetry numbers, so the model reads text before pixels); `pixel` (pixel-art lint: true pixel scale, colour count, near-duplicate colours, semi-transparent pixels, orphan pixels, anti-aliasing on an upscaled sprite); `hash` and `dedupe` (aHash and dHash 64-bit, Hamming groups, threshold stored and calibratable); `cache` (verdict store keyed by file SHA-256 plus rubric id and version); `compare` (prepares a two-up, both orders, neutral labels, and records the pick and whether it flipped).
- **Dependencies: standard library core, Pillow optional.** Stdlib PNG decode measured at 0.12 to 0.24 s per megapixel on 3.14; JPEG and WebP through `ffmpeg ... -f rawvideo -pix_fmt rgb24 -`; Pillow used when present for speed, labels and resampling. Requires Python 3.9+ to match the siblings; Pillow 13 needs 3.11+, so accept any Pillow >=11. Skip numpy (12 to 17 MB), scipy (20 to 37 MB), imagehash (pulls 45 to 60 MB), scikit-image (12 to 14 MB plus scipy), OpenCV headless (35 to 61 MB) and the unmaintained colorthief, haishoku and extcolors.
- **Size budget (package-size rule):** green under 300 KB for `aw.py` plus knowledge files, yellow to 1 MB, red above 1 MB. Optional Pillow adds 5 to 7 MB on the user's side and is never required.
- **Token rules to write into the main file:** one sheet per review, never one Read per image; 1000 px long edge (1296 tokens) for a single critique, crop to a region for detail instead of sending the full image larger; size before Read because the host may not downscale well; numbers from `stats` and `palette` first, pixels second; cache verdicts so an unchanged file is never re-judged.
- **Critique method to adopt from pixel-critic:** cold read before the brief, issues in a fixed priority order (silhouette and read, value, contrast, form and shading, palette, edges, consistency), each finding located and tied to a named rule, one highest-value fix, "looks good" banned; comparisons blind, both orders, flips are ties.
- **Point to rather than build:** diivi/aseprite-mcp and aseprite-ai-artist for editing in Aseprite; open-museum-mcp or the single-museum servers for collection search, but art-history facts route through historywright; comfyui-gen and Anthropic's canvas-design for making images; cinewright-qc for video takes.
- **Refuse on pixels alone:** whether an image is AI-made (Anthropic's docs say Claude cannot tell), who painted an unlabelled work as fact, and naming real people in images.
- **Contract for siblings:** artwright reads an image folder or a sibling's asset folder and writes `artwright/verdict.json` (rubric id and version, per-image findings, scores, pick, image SHA-256) next to it; siblings read that file, never artwright internals.
- **Eval cases to seed:** weak image with a proud framing expects concrete faults; better image shown second in a pair; a 12-seed batch with 4 near-duplicates expects dedupe before review; a pixel-art PNG with anti-aliased edges and 3 semi-transparent pixels expects `pixel` to find them; "is this AI-generated" expects a refusal with reasons; "who painted this" expects a hand-off to historywright.

## Overall magnitude: n/a (initial)
## Open questions: still open: real install velocity for Claude-Code art skills (skills.sh counts are tiny across the board); whether stdlib decode is fast enough on Python 3.9 (measured on 3.14 only); a 5x7 bitmap label font in stdlib versus Pillow-only labels; an arXiv-verified benchmark for style attribution; the exact Claude Code Read-tool resizing rule after the 2026-06 fix.
## Search plan notes: Tooling: skills.sh `/api/search?q=` and the MCP registry `?search=` were the best sources (no search budget used); GitHub code search needs `filename:SKILL.md`, not `path:SKILL.md` (path returned 0 for every query); `gh api repos/...` gives stars and push dates; npm `api.npmjs.org/downloads/point/last-month/<pkg>` gives use for Node MCP servers. PyPI JSON gives wheel sizes and `requires_python` per version. The registry "art" query is noisy (substring matches); "museum", "aseprite" and "pixel" were precise. Practice: generic contact-sheet searches return photo software only; the Anthropic vision page is the primary source for costs. Testing: arXiv results on LVLM judges were useful; search results flagged some 2026 arXiv IDs as unusual, verify before citing.
## Tracks covered: subject: 1 query · tooling: 12 (registry, skills.sh, GitHub, PyPI, npm) · practice: 4 · testing: 3
## Upcoming events: none dated. Pillow 13.x is the current line (13.0.0 on 2026-10-16); watch for a numpy-free imagehash or a stdlib-friendly palette library, none seen.
## Nothing changed: no (creation pass)
## Cost: searches 6 · fetches 21 · tool calls 50 (plus about 40 direct HTTP reads through gh, curl to PyPI and npm inside Bash, and two local benchmarks)
