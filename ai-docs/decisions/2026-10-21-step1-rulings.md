# Step 1 rulings (2026-10-21)

Small design rulings made during the creation pass, each flagged in one line in the session's final message. The
real forks for Mark are at the end of the synthesis, [../research/2026-10-21-creation-pass.md](../research/2026-10-21-creation-pass.md).

## R1. Name: keep `artwright`

Checked 2026-10-21: `m4bwav/artwright` returns 404 on GitHub, a repository search for "artwright" returns 0
results, and the name is unregistered on PyPI and npm. No known product clashes. It fits the -wright family
(historywright, musicwright, polywright).

## R2. Research passes ran as general-purpose agents in the evergreen-researcher format

The evergreen-researcher agent is read-only, so each pass ran as a general-purpose agent. Each one followed the
researcher's method and output structure in creation mode and wrote its own report. Each pass was capped at
about 25 web searches and told to prefer direct API fetches, as the kickoff asked.

## R3. Four skills: hub, judge, pixel, curate

`artwright` (analysis, critique, movements, theory, facts through historywright), `artwright-judge` (compare, rank,
fit to a brief, prompt fixes; the one siblings call), `artwright-pixel` (pixel and 2D game art with `aw.py pixel`),
`artwright-curate` (knowledge base and private taste). Pixel art got its own skill because it is a large, distinct
trigger area with hard script checks. Judging got its own because siblings need a narrow, stable entry point.

## R4. `aw.py` is standard library first, Pillow optional, Python 3.9+

The siblings test Python 3.9 and 3.14. Pillow 13 needs 3.11+, so any Pillow from 11 up is accepted when present.
Decode order: Pillow, stdlib PNG, ffmpeg rawvideo. No numpy, scipy, imagehash, scikit-image or OpenCV (12–61 MB
each). Source: g-tooling-efficiency F4, F5.

## R5. Eval images are fetched, not committed

Synthetic sprites and degradations are generated in code. Museum fixtures (Cleveland CC0) are fetched at test time
by accession number, checked against a pinned SHA-256 and cached in a git-ignored folder. This keeps the plugin
install inside its size budget. If Cleveland's API fails in CI, the image cases skip with a reason and the rest still
run.

## R6. Art facts route through historywright

artwright owns the reference interview and the art vocabulary and hands historywright a pinned question. New art
sources (Getty Provenance CSV, Museo Egizio, the link-out price databases) are proposed to historywright-sources, not
kept in an artwright registry. Source: f-facts-markets proposals.

## R7. The living-artist rule rewrites, it does not refuse

Pending Mark's confirmation as fork 4; this is the default the build assumes.

## R8. No generator, editor or grid fixer in artwright

It points to comfyui-gen, the Aseprite MCP servers, Pixel Snapper, proper-pixel-art and unfake, and its own checks
report what those tools should fix.
