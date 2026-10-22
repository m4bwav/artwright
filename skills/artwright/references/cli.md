# aw.py commands

`python <plugin>/skills/artwright/scripts/aw.py <command> ...`. Python 3.9+, standard library; Pillow (11 or
later) when present for speed and every format; otherwise PNG is read in pure Python and JPEG or WebP through
ffmpeg. Each command prints one JSON object; failures print `{"ok": false, "error": ...}` and exit 1.

Back to [SKILL.md](../SKILL.md).

| Command | Does |
|---|---|
| `doctor [--probe]` | Python, Pillow, ffmpeg, `ARTWRIGHT_HOME`; `--probe` makes one request to Cleveland's API and Lospec |
| `info IMG...` | format, bytes, size, SHA-256, alpha (`none`, `binary`, `partial`), unique colours, token cost per tier |
| `fit IMG -o OUT [--long N] [--tokens N] [--crop x,y,w,h] [--cell RxC:i] [--pixel]` | downscale (area average) to a long edge (default 1024) or a token budget; crop a box or a grid cell (row-major from 0); `--pixel` uses nearest neighbour and integer upscales |
| `sheet IMG|DIR... -o OUT [--cols N] [--cell PX] [--pixel] [--no-labels]` | contact sheet, cells labelled A, B, C with a built-in bitmap font, at most 2000 px a side; `map` gives letter to file |
| `stats IMG [--edge 256] [--notan DIR]` | value mean, key and histogram, value groups, RMS contrast (SD of L*), colourfulness (Hasler–Süsstrunk), saturation, warm share, edge density, mirror symmetry, centre of mass and imbalance, focal cell, thirds distance (description only), box-counting fractal dimension; `--notan` writes grey, two- and three-value thumbnails |
| `palette IMG [-k 8] [--against PAL]` | dominant colours by median cut with shares; `--against` gives nearest palette colour and delta-E 2000 |
| `pixel IMG... [--budget N] [--palette PAL] [--scale S] [--tile] [--frames] [--preview OUT] [--zoom 4]` | pixel-art checks; see artwright-pixel |
| `hash IMG...` | 64-bit aHash and dHash, SHA-256 |
| `dedupe IMG|DIR... [--threshold 6]` | groups by dHash Hamming distance; `keep` lists one file per group |
| `compare prepare A B [--work DIR] [--cell 768]` | writes the pair in both orders, labelled 1 and 2; returns the pair id |
| `compare record PAIR ORDER PICK [--work DIR] [--confidence C] [--criteria ...] [--judge M]` | records one judged order (`PICK` is 1, 2 or tie) and returns the resolved result |
| `rank [--work DIR] [--next N] [--write]` | Bradley–Terry with ties; `close_to_next` flags; `--next` suggests Swiss pairs; `--write` updates `verdict.json` |
| `cache get|put IMG [--model M] [--rubric R] [--rubric-version V] [--prompt-version P] [--verdict JSON]` | verdict store in `ARTWRIGHT_HOME/verdicts.jsonl` |
| `cache stats` · `cache label A B a|b|tie [--note]` · `cache agreement [WORK...]` | store counts; a human calibration label; agreement metrics |
| `verdict init DIR [IMG...] [--kind K] [--brief B]` · `verdict validate DIR` | the `artwright/verdict.json` contract |
| `degrade IMG -o OUT --kind K [--seed N]` | deterministic degradations for test pairs: saturate, crush, crop, jpeg, orphans, mixels, blur |

`PAL` is `pico-8` (built in), a Lospec slug (fetched once and cached), a `.hex`, `.txt` or `.gpl` file, or
comma-separated hex colours. `--work` defaults to `./artwright`.

Token cost: images are read at `ceil(w/28) x ceil(h/28)` visual tokens after fitting to the tier: 1568 px and
1568 tokens on the standard tier, 2576 px and 4784 tokens on the high-resolution tier (Claude 4.7 and later).
Speed without Pillow: about 0.1–0.3 s per megapixel to decode a PNG; `stats` measures at 256 px.
