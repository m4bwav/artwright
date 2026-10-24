# aw.py commands

`python <plugin>/skills/artwright/scripts/aw.py <command> ...`. Python 3.9+, standard library; Pillow (11 or
later) when present for speed and every format; otherwise PNG is read in pure Python and JPEG or WebP through
ffmpeg. Each command prints one JSON object; failures print `{"ok": false, "error": ...}` and exit 1. Usage mistakes (a missing or unknown option) print argparse's usage text and exit 2; `--version` prints plain text.

Back to [SKILL.md](../SKILL.md).

| Command | Does |
|---|---|
| `doctor [--probe]` | Python, Pillow, ffmpeg, `ARTWRIGHT_HOME`; `--probe` makes one request to Cleveland's API and Lospec |
| `info IMG...` | format, bytes, size, SHA-256, alpha (`none`, `binary`, `partial`), unique colours, token cost per tier |
| `fit IMG -o OUT [--long N] [--tokens N] [--crop x,y,w,h] [--cell RxC:i] [--pixel]` | downscale (area average) to a long edge (default 1024) or a token budget; crop a box or a grid cell (row-major from 0); `--pixel` uses nearest neighbour and integer upscales |
| `sheet IMG|DIR... -o OUT [--cols N] [--cell 384] [--pixel] [--no-labels]` | contact sheet, cells labelled A, B, C with a built-in bitmap font, at most 2000 px a side; `map` gives letter to file |
| `stats IMG [--edge 256] [--notan DIR]` | value mean, key and histogram, value groups, RMS contrast (SD of L*), colourfulness (Hasler–Süsstrunk), saturation, warm share, edge density, mirror symmetry, centre of mass and imbalance, focal cell, thirds distance (description only), box-counting fractal dimension; middle-value share, bimodality (the two-family valley), black and white clipping, highlight tint, chroma per cell (`chroma_cells`: spread, and the peak against the focal cell), b* mean and spread; `--notan` writes grey, two- and three-value thumbnails; `alpha` gives the transparent share, and value and colour statistics read the opaque pixels only (alpha 128 and up) while edges, symmetry, balance and the notan read the image on white |
| `light IMG [--box x,y,w,h]` | light and shadow families (Otsu on L*, top and bottom 1% dropped): value gap in steps of ten, temperature shift (b* of lights minus shadows), tint shift (a*), shadow-to-light chroma ratio; `--box` (fractions) measures one surface |
| `gamut IMG [--overlay OUT]` | chroma mass in twelve 30-degree hue sectors, a shape (`mono`, `analogous`, `complementary`, `triad`, `mood+accent`, `multi`, `full`, `neutral`), hull area as a share of sRGB's a*b* footprint, colour cast; `--overlay` draws the a*b* plane with the hull |
| `accents IMG` | high-chroma regions more than 90 degrees from the dominant hue: share, hue, centre, distance from the focal cell |
| `depth IMG [--depth MAP] [--far-bright]` | contrast, darkest darks, chroma and b* in near, middle and far bands; bands come from a depth map (bright = near, as Depth Anything writes; `--far-bright` for a Mist pass) or, weakly, from the bottom, middle and top thirds |
| `comp IMG [--subject x,y,w,h] [--out DIR]` | value masses (k-means on L* at 64 px, k = 3 and 4; `--out` writes `masses3.png` and `masses4.png`), the focal peak and its margin over the strongest cell elsewhere, border and corner pull, contours kissing the frame, horizon, bottom barrier, sharpness hierarchy, hot spots, figure and ground against `--subject`; a light mat or backdrop round a photographed work is trimmed first (`margin_trimmed`) |
| `palette IMG [-k 8] [--against PAL]` | dominant colours by median cut with shares; `--against` gives nearest palette colour and delta-E 2000 |
| `pixel IMG... [--budget N] [--palette PAL] [--scale S] [--tile] [--frames] [--preview OUT] [--zoom 4] [--tol 24]` | pixel-art checks (`--tol`: neighbours whose summed RGBA difference is at most this count as one colour); see artwright-pixel |
| `hash IMG...` | 64-bit aHash and dHash, SHA-256 |
| `dedupe IMG|DIR... [--threshold 6]` | groups by dHash Hamming distance; `keep` lists one file per group |
| `compare prepare A B [--work DIR] [--cell 768]` | writes the pair in both orders, labelled 1 and 2; returns the pair id |
| `compare record PAIR ORDER PICK [--work DIR] [--confidence C] [--criteria ...] [--judge M]` | records one judged order (`PICK` is 1, 2 or tie) and returns the resolved result |
| `rank [--work DIR] [--next N] [--write]` | Bradley–Terry with ties; `close_to_next` flags; `cycles`, `cycle_count` and `top_in_cycle` list loops among decided pairs (members are marked close); `--next` suggests Swiss pairs; `--write` updates `verdict.json` |
| `cache get|put IMG [--model M] [--rubric R] [--rubric-version V] [--prompt-version P] [--temperature T] [--seed N] [--verdict JSON]` | verdict store in `ARTWRIGHT_HOME/verdicts.jsonl`; rubric version defaults to 2; temperature and seed join the key only when given |
| `cache stats` · `cache label A B a|b|tie [--shown-first a|b] [--note]` · `cache agreement [WORK...]` | store counts; a human calibration label with the side shown first; agreement metrics, with `labels_first_shown_share` |
| `verdict init DIR [IMG...] [--kind K] [--brief B]` · `verdict validate DIR` | the `artwright/verdict.json` contract |
| `geomgate RENDER_DIR PAINTED [--part P] [--spokes N] [--contact A:B] [--game-px 96] [--no-edges] [--out F]` | a painting kept its 3D render's shapes: ring rim (ellipse), spokes, a new object inside a part (regions), parts that must touch (contact); reads `beauty.png`, `id.png` and `sprite.json` ([sprite-json.md](sprite-json.md)); a failing gate exits 0 with `pass: false` |
| `sprite CAND... --refs DIR|IMG... [--pad 0.15] [--min-coverage 0.9] [--out F]` | a painted game sprite's style against reference sprites, at native size on opaque pixels: value mean and spread (L*), chroma, unique colours, soft-edge share, texture, outline value; each must sit inside the references' range widened by `--pad`; coverage (opaque share of the canvas) has a floor only, `--min-coverage` times the references' median, so a building drawn too small for its canvas fails; never posterizes (see artwright-pixel) |
| `degrade IMG -o OUT --kind K [--seed N]` | deterministic degradations for test pairs: saturate, crush, crop, jpeg, orphans, mixels, blur; for the measures below: warm-shadows (shadows take the lights' colour), glow-shadows (shadow chroma tripled), uniform-sat (every pixel at the median chroma), midgrey (L* pressed toward 50), haze-off (far third at least 1.3 times crisper and more saturated), hotspot (a white patch near a border), tangent (a line kissing a border) |

`PAL` is `pico-8` (built in), a Lospec slug (fetched once and cached), a `.hex`, `.txt` or `.gpl` file, or
comma-separated hex colours. `--work` defaults to `./artwright`.

Token cost: images are read at `ceil(w/28) x ceil(h/28)` visual tokens after fitting to the tier: 1568 px and
1568 tokens on the standard tier, 2576 px and 4784 tokens on the high-resolution tier (Claude 4.7 and later).
Speed without Pillow: about 0.1–0.3 s per megapixel to decode a PNG; `stats` measures at 256 px.

## Light, colour and composition flags

`light`, `gamut`, `accents`, `depth` and `comp` live in `aw_measure.py` beside aw.py and run through it (`geomgate` and `sprite` live in `aw_geom.py`). On an image with transparency, `light`, `gamut` and `depth` measure the opaque pixels only, `accents` reads transparent pixels as neutral and `comp` reads the frame on white; each says so in `alpha`. Each
returns numbers, `readings` in words and `flags`. A flag says where to look. It is never a grade and never a
reason on its own: open the region, confirm it, then write the finding with the region named. Ideas after
Gurney (*Color and Light*), Mateu-Mestre (*Framed Ink*) and Roberts (*Mastering Composition*).

Thresholds were set on 2026-10-22 from how often each flag fired on 7 museum works and 48 AI stills. A flag
that fires on most images says nothing. No owner labels were used, so treat the thresholds as uncalibrated. The
share of the AI set each one flagged is in brackets.

| Flag | Fires when | Means |
|---|---|---|
| `warm_shadows` (light) | lights' b* above 5 and shadows within 1 of them (6%) | no cool fill from the sky; right under artificial or alien light |
| `glowing_shadows` (light) | shadow chroma over 1.15 times the lights' (13%) | the glowing-shadow look |
| `low_value_gap` (light) | light and shadow medians under 2 steps apart (21%) | overcast or over-filled; wrong only when the brief says sun |
| `fruit_salad` (gamut) | seven or more hue sectors and median chroma over 30 (0%) | no colour family leads |
| `competing_accent` (accents) | an accent of 0.2% or more, 0.35 from the focal cell, accents under 5% in all (4%) | an off-hue spot pulls the eye off the subject |
| `no_recession` (depth) | far band's contrast and chroma both at least 95% of the middle band's (15%) | the distance does not recede (the band proxy is weak) |
| `warm_distance` (depth) | far band's b* 3 above the middle's (4%) | right only toward a low sun |
| `mid_dominant` (comp) | the middle of three value masses covers over 60% (0%) | middle-value mumbling |
| `fragmented` (comp) | over 12 masses above 1%, or the largest three under half the area (13%) | a busy design with no big shapes |
| `competing_focal` (comp) | the focal peak beats the strongest cell outside its neighbours by under 3% (23%) | two places claim the eye |
| `focal_off_subject` (comp) | the peak falls outside `--subject` | the eye lands off the subject |
| `edge_pull` (comp) | edges or chroma in a 5% border band or 12% corner over twice the image mean (6%) | the border pulls the eye out |
| `frame_tangent` (comp) | a contour runs parallel to a side, within 2% of it, for over 20% of its length (13%) | a contour kisses the frame |
| `horizon_split` (comp) | a horizontal edge crossing 60% of the width sits between 45% and 55% of the height (6%) | the frame is cut in half |
| `horizon_through_head` (comp) | that line crosses the top quarter of `--subject` | the horizon runs through the head |
| `blocked_entrance` (comp) | one horizontal edge crosses over 85% of the width in the bottom 12% (4%) | a bar across the way in |
| `uniform_sharpness` (comp) | the sharpest cell's Laplacian variance under 3 times the median cell's (6%) | everything equally in focus |
| `hot_spot_near_border` (comp) | a region of 0.05% to 1%, at least 12 L* and 2.5 local SD above its surroundings, within 10% of a border and outside `--subject` (17%) | a bright spot at the edge pulls the eye out |
| `weak_figure_ground` (comp) | under 10 L* between `--subject` and a ring around it | the subject does not separate |

Known blind spots. A photographed sheet with a wide paper margin keeps it, because the trim needs every side's
band under an eighth of the side; its edges then read as tangents. Designs built on lines to the edge (Mondrian)
flag `edge_pull` and `frame_tangent` by intent. The `depth` band proxy assumes distance rises up the frame. Not
measured: armature lines, intervals, interior tangents. Ask a vision model and check its answer against `comp`.
