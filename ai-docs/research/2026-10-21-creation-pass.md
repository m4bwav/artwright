# artwright creation pass, 2026-10-21

The evergreen creation pass (PROTOCOL §8) for artwright, run before any skill text. Eight research passes ran in parallel in creation mode, each in the evergreen-researcher format and each capped at about 25 web searches: A art history and theory, B media and craft, C digital and pixel art, D AI generation, E AI evaluation, F facts and markets, G tooling and efficiency, H testing. Their reports are in [2026-10-21-creation-pass/](2026-10-21-creation-pass/index.md), and the `R-` entries are in [../../RESEARCH.md](../../RESEARCH.md). This file is the synthesis: what the Step 2 build should rest on, and the forks for Mark.

Cost: searches 125 · fetches 218 · tool calls 429 (plus about 70 direct API reads through gh and curl). Five passes hit a session usage limit partway through and were resumed. No pass ran out of searches. The cap and the direct-API preference worked: the most decisive evidence was again live probes (museum endpoints, PyPI, the GitHub API, skills.sh, the MCP registry).

## 1. What the research says, in ten lines

1. **AI judges of beauty are weak, and order changes their answers.** On the Visual Aesthetic Benchmark (May 2026), the best model (Claude Sonnet 4.6) picked a set's best and worst image under all three orderings in 26.5% of tasks; experts managed 68.9%. Swapping two images flips up to 60.9% of verdicts (EditJudgeBias, 2026-10). Going from two candidates to four or more degrades models 7x, against 2x for humans. (E-F1, E-F6)
2. **Comparisons beat scores, for people and for models.** Even experts' own 1–10 scores disagree with their direct comparisons (Kendall tau 0.188). Judges rarely give low scores and lean towards one culture's norm. (E-F4, E-F6)
3. **Structured critique beats free reasoning.** ArtCoT (describe, then a critic pass, then a verdict) raised agreement with experts by 29–56%; free chain-of-thought lowered it and filled answers with "feels" and "somewhat". (B-F4)
4. **Learned aesthetic scores measure photo polish, with biases.** The LAION predictor prefers images with defects over clean ones 58% of the time and carries documented gender and Western-canon skews. Reward tuning drives the "AI look" (oversaturation, overexposure, one narrow style). (E-F2, E-F8, D-F9)
5. **Style labels are often right for the wrong reasons.** GPT-4o reached 53% zero-shot on WikiArt styles and confused neighbouring movements. About 10% of the concepts behind correct predictions were irrelevant to art historians, and Western art scores higher than non-Western art across 15 models. (E-F9, A-F5, A-F6)
6. **Most composition "rules" fail the evidence.** The rule of thirds does not predict quality, and the golden ratio has no population preference. Curvature preference is real but moderate (g = 0.39) and vanishes for experts. Itten's colour schemes predict nothing; Albers's relativity holds. (B-F5, B-F7, B-F11, B-F13)
7. **Fake pixel art is measurable.** Four numbers decide it: unique colours against the budget, lattice alignment (2% raw against 100% fixed), uniform block size and transitional pixels. Good fixers already exist. (C-F2 to C-F4, C-F9)
8. **Art facts move, and the open web garbles them.** The oldest dated cave art changed in January 2026. Auction results sit behind logins, and copies on the open web mix hammer and premium, dates and currencies. Guinness calls a Qing vase "the most expensive vase". (F-F1, F-F4, F-F5)
9. **No one has built a used art critic.** The art-critique skills on skills.sh have 1 to 28 installs, and Anthropic's catalog makes art but does not judge it. The best method to copy is a pixel critic in a 442-star Aseprite tool: a cold read before the brief, a rule cited for each finding, no "looks good", blind A/B for fixes. (G-F2, G-F8, G-F9)
10. **Images are cheap only when sized first.** Claude now counts `ceil(w/28) x ceil(h/28)` tokens, up to a 2576 px long edge (4784 tokens) on 4.7+ models. A 1024 px image costs about 1,300 tokens. Claude "cannot determine whether an image is AI-generated". (G-F1, E-F10)

## 2. Where artwright sits among the siblings

artwright judges, explains and directs. It does not generate, edit, model, fetch facts or own a brand. Each row is a boundary the skill descriptions must state so two skills never fight over one request (G, sibling table).

| Sibling | Owns | artwright's part |
|---|---|---|
| comfyui-gen | generating images and video, hosts, workflows | Its main caller. After a batch: dedupe, contact sheet, rank in both orders, judge fit to the brief, return the next prompt and settings. |
| cinewright (-qc, -history, -design) | judging a video take against its shot card, film-history style cards, continuity, grading | Single-frame art critique of concept frames and key frames; fine-art vocabulary for a style bible ("lit like a Caravaggio"). Never judges a take; cinewright-qc keeps that. |
| polywright | meshes, the asset folder and `manifest.json`, reference sheets, print and game readiness | Judges concept art before image-to-3D and rendered turnarounds (silhouette, proportion, stylisation, colour). Writes `artwright/verdict.json` beside the renders; never edits the manifest. |
| historywright | dated facts, attributions, provenance, museum records, the source registry | artwright owns the reference interview and the art vocabulary (painting or stencil, Ming or Qing, hammer or premium, "attributed to"). It hands historywright a pinned question and wraps the cited answer in an art verdict. New art sources go into historywright-sources, never into an artwright copy. |
| brandwright | brand palettes, delta-E scoring against a brand, mock-ups, LoRAs | Judges hierarchy, balance and craft of mock-up candidates after brandwright ranks them by brand distance. Never judges brand fidelity. |
| sitewright-direction | a website's visual direction, fonts, palette, contrast | Analyses the user's artwork or a reference image (palette, movement, mood) when asked; sitewright decides. |
| musicwright, madnesswright, unity-agent, roblox-agent | their domains | Album art and game-art critique and pixel checks when they ask. Engine import notes (point filter, integer pixels per unit) go to the engine plugin. |
| Aseprite MCP servers (diivi/aseprite-mcp, aseprite-ai-artist), Pixel Snapper, proper-pixel-art, unfake | editing sprites, fixing AI pixel grids | Points to them; does not rebuild an editor or a grid fixer. Its own checks report what is wrong; they fix it. |
| Anthropic canvas-design, algorithmic-art, frontend-design | making art | The reviewer after they produce an image. |

## 3. Proposed layout (for Mark's reply; Step 2 builds it)

### Skills: a hub and three siblings

- **`artwright`** (hub): any art question or image that needs an artist's eye, and the router.
  - Analysis in VULCA and Panofsky layers: describe, formal analysis, style or movement with trait evidence, context, interpretation. It says whose criteria apply (the brief, a named tradition, the user's own past picks).
  - Movement and style questions answer `member | influenced | no evidence`, list the visible traits seen and missing, and name the neighbouring movements considered. Never a bare yes or no.
  - Theory questions (postmodernism, neo-expressionism, the definition of art) come from the theory files, which cite their sources.
  - Fact questions (oldest, most expensive, who painted it) run the superlative procedure (section 5) and hand historywright a pinned question.
  - Critique of a single work: a cold read first, then the checklist, a critic pass that ties each claim to a region, the top two or three issues, and one fix each.
- **`artwright-judge`**: compare, rank and test fit to a brief. Siblings call this one.
  - Two images per call, each pair judged in both orders in fresh calls, with labels and filenames stripped. A split between the orders is a tie.
  - Batches go from a triage sheet to pairwise matches, then to a Bradley–Terry fit.
  - The brief splits into atomic yes/no checks; the verdict is FITS, FITS WITH FIXES or DOES NOT FIT, with hard fails listed.
  - Each fix is classed by channel: prompt wording, a model setting, control (depth, pose), a reference image, inpainting, or a model switch. The output is a revised prompt per target model plus a one-line diff.
- **`artwright-pixel`**: pixel art and 2D game art. It runs the `aw.py pixel` checks, then a pixel critique in the priority order: read at 1x, silhouette, value, palette roles, clusters, outlines, light. It also covers sprites, animation, tiles and engine import. It points to the fixers and editors.
- **`artwright-curate`**: the evergreen knowledge base and the private taste record.
  - Knowledge: add, retire and source the movements, theory, vocabulary and model profiles, and keep the dated law table current.
  - Taste: keep Mark's verdicts, picks and calibration labels, and promote general lessons into the public files.

### The script: `aw.py`, standard library first

Standard library core; Pillow optional (any version from 11 up, since Pillow 13 needs Python 3.11 and the siblings test 3.9). The decode order is Pillow if present, then a stdlib PNG reader (measured at 0.12–0.24 s per megapixel on 3.14), then ffmpeg rawvideo for JPEG and WebP, else a clear error naming what is missing. Never numpy, scipy, imagehash, scikit-image or OpenCV (each 12–61 MB). Every command prints one JSON object and fails soft, like `pw.py` and `cine.py`.

| Command | Does |
|---|---|
| `doctor` | Python, Pillow, ffmpeg; one-request probes of the museum routes it names |
| `info` | size, mode, alpha use, SHA-256, token cost on each tier |
| `fit` | downscale to a long edge or a token budget, crop a box or a grid cell; nearest-neighbour only for pixel art |
| `sheet` | contact sheet with cells labelled A, B, C (drawn by aw.py, not ffmpeg drawtext, which fails on Windows), at most 2000 px a side, id-to-file map in the JSON |
| `stats` | value histogram and key, RMS contrast, Hasler–Süsstrunk colourfulness (signed channels), saturation, warm/cool split, edge density, mirror symmetry, balance and centre of mass, box-counting fractal dimension, thirds distance as description only; greyscale and two- and three-value notan thumbnails. No beauty score. Metric names follow the Aesthetics Toolbox (MIT) so numbers match the literature. |
| `palette` | dominant colours by median cut with shares; `--against` a palette gives delta-E |
| `pixel` | grid scale and offset (the unfake edge-profile method), lattice alignment %, block uniformity, unique colours against a budget, palette match against a named Lospec palette, orphan pixels (no same-colour 8-neighbour), jaggies, non-binary alpha, outline consistency, tile seams with a 3x3 preview, frame consistency (palette, grid, bounding box, baseline), integer-scaled preview |
| `hash`, `dedupe` | 64-bit aHash and dHash, Hamming groups, threshold stored with `{algo, version}` |
| `compare` | prepare a pair in both orders with neutral labels; record each pick and whether it flipped |
| `rank` | Bradley–Terry with ties over recorded matches; win margins and overlap flags |
| `cache` | verdict store keyed by image SHA-256, rubric id and version, model and prompt version |
| `degrade` | deterministic degradations for test pairs (saturation push, value crush, a crop that breaks the composition, JPEG blocking, orphans, mixels, blur) |

Facts and museum records go through `hw.py` (historywright), never an artwright client. An optional local aesthetic model is not proposed (fork 1).

### Knowledge base

Public general knowledge lives in the repo, as references under each skill, with sources and dates and a `verified` flag on every row. Private taste lives in `ARTWRIGHT_HOME` (default `~/.artwright`), junctioned to the vault sidecar like musicwright's studio. It holds `verdicts.jsonl` (the cache, which doubles as the calibration log), `taste.md`, `calibration/` (Mark's labelled pairs) and `keywords/` (a per-model keyword-effectiveness log with evidence from real runs).

| File | Content | Target size |
|---|---|---|
| `movements.md` | about 100 periods and movements: dates, region, four to six visually checkable traits, confusable-with, Wikidata QID, AAT ID, `verified`. A Western spine plus parallel tracks for China, Japan, South Asia, the Islamic world, Africa, Oceania, the Americas, and 2D digital art | 15–25 KB |
| `theory.md` | one paragraph per wave of thinking (mimesis, Kant, Romantic expression, formalism, iconology, social art history, Danto, Dickie, Weitz, Gaut, Krauss and Owens, feminist, postcolonial and the primitivism critique, Bourriaud and Bishop, post-internet, AI authorship), each with the question it lets the agent ask of an image and an SEP slug | 8 KB |
| `traditions.md` | Xie He's six principles, rasa, Japanese terms with SEP's usage cautions, Islamic geometry and calligraphy; a borrowed-term guard ("wabi-sabi" applied to an AI image is a loose sense) | 6 KB |
| `evidence.md` | empirical aesthetics with study, effect size and replication status; the myths (thirds, golden ratio, Itten) | 8 KB |
| `craft.md` | composition, value and colour, Gestalt and design principles; media cues for drawing, painting, sculpture and printmaking; critique frameworks (Feldman, Carroll) | 10 KB |
| `ceramics.md` | bodies, glazes, firing, Chinese reign marks and the rule that a mark never dates a piece alone | 6 KB |
| `pixel-art.md`, `sprites-tiles.md` | rules with thresholds (Derek Yu, Slynyrd ramps), defect vocabulary, AI pixel art and fixers, frames, tiles, engine import, 3D stylisation pointers | 10 KB |
| `vocabulary.md` | 400–600 style terms, each with a one-line visual definition, usable both ways (prompt and description); a dead-magic-words list | ≤ 40 KB |
| `models/` | one short profile per generation model (Z-Image Turbo and base, FLUX.2, Qwen-Image, MiniMax H3, Wan; thin "verify first" profiles for closed models): encoder, CFG and negatives, word order, references, control, defaults to steer against, licence, date checked | 1.5 KB each |
| `ai-look.md` | about 15 tells, each with a model-conditional fix | 4 KB |
| `market.md` | the superlative procedure, Sotheby's qualifier glossary quoted verbatim, hammer against premium, link-out-only price databases | 5 KB |
| `law.md` | dated status table (Andersen, Getty appeal, Thaler and Allen, Copyright Office parts 2 and 3, EU AI Act Article 50, Steam disclosure); "not legal advice"; refreshed every 60–90 days | 4 KB |
| `rubric.md` | the judging rubric and the abstain rules (section 4) | 3 KB |

Tier: **moderate** (60 days) for the hub, judge and pixel skills; `law.md` and `models/` carry their own 60–90 day due dates as volatile claims. A scripted probe (`aw.py doctor --probe`) checks the museum and Lospec routes between refreshes.

### Size budget

- Plugin install (skills, knowledge, `aw.py`, tests without images): **green under 500 KB, yellow to 1 MB, red above 1 MB.**
- `aw.py`: green under 60 KB, yellow to 100 KB, red above.
- Knowledge files together: green under 200 KB, yellow to 300 KB, red above. `vocabulary.md` alone: red above 40 KB.
- Eval images: kept out of the install. Synthetic sprites and degradations are generated in code. Museum fixtures are fetched at test time from Cleveland's CC0 API by accession number with pinned SHA-256 and cached in a git-ignored folder (ruling R5).
- Optional Pillow adds 5–7 MB on the user's side and is never required.

## 4. The judging rubric

Every verdict is pairwise or checklist-based, never a lone score. An absolute 1–10 score is given only when asked for, anchored by three labelled reference images, and with a warning that scores bunch at the top.

1. **Brief fit**: atomic yes/no checks from the brief (subjects, count, attributes, relations, camera, light, style, mood, text, forbidden items). Hard fails are listed separately.
2. **Read and composition**: thumbnail and greyscale read, focal point (highest local contrast), eye path, balance, negative space, placement with a reason (facing into the frame, room ahead of motion). Thirds is never a score.
3. **Value and colour**: three to five value groups, light logic, temperature, saturation hierarchy, harmony as a choice.
4. **Rendering integrity** (a gate, not taste): anatomy and hands, duplicated or merged objects, text, seams, perspective, mixels.
5. **Style coherence**: one consistent style; it matches the movement or reference asked for, by named traits.
6. **Expressive intent**: mood and story match the brief, including briefs that ask for rough or "ugly" work (aesthetic scores fight those).

Procedure: cold read before the brief, then per-criterion notes for each image tied to a visible region, then `{winner: 1|2|tie, confidence, decisive_criteria}`. Abstain (tie, flagged for a human) when the two orders disagree, when both images fail the same gate, or when confidence is low on every decisive criterion. A third run may break a tie only by agreeing with one earlier verdict. The judge never sees the user's guess, the model or seed, other votes or file names; the user's preference is shown after the blind verdict.

Guards in every skill: no attribution, authentication or valuation from pixels (the Rubens and Raphael AI disputes); no "is this AI-made" from pixels (Anthropic's docs say Claude cannot tell); a missing Wikidata movement tag is not evidence (only 1.3% of 1.08 million painting items carry one); a living artist named in a prompt becomes descriptive traits, with one line saying so; no "looks good"; the golden ratio is never given as a reason.

Image handling: size before Read (1024 px long edge by default, about 1,300 tokens); one contact sheet for triage, never one Read per image; crop for detail rather than sending the full image larger; numbers from `stats` and `pixel` first, pixels second; an unchanged file with the same rubric is never re-judged. A 16-image round robin in both orders costs about 624k image tokens (about $2.50 on Opus 5.5), so batches above about 12 use triage plus Swiss pairing.

## 5. Facts: the superlative procedure and the gold answers

Procedure for "oldest", "largest", "most expensive", "first":
1. Name the readings.
2. For each reading, find the current holder and check the year to date for a newer record.
3. Check the category: dynasty and reign (Ming is 1368–1644), medium (painting against stencil or drawing), attribution qualifier.
4. For prices, record currency, date, hammer or premium, public or private, paid or unpaid.
5. Use two independent sources. Guinness and Wikipedia are finders, never one of the two.
6. For dates, say "at least" for minimum ages.

The answer ends with historywright's confidence line, a sources-disagree note, and a "Market qualifiers:" line on any price.

**Gold answers, verified 2026-10-21** (full quotes and sources in [f-facts-markets.md](2026-10-21-creation-pass/f-facts-markets.md); `R-20261021-14` to `-16`):

- **Most expensive Ming vase.**
  - At public auction, strictly Ming: the Yongle blue-and-white meiping with fruit sprays (Meiyintang Collection), Sotheby's Hong Kong, October 2011, HK$168.66 million including premium (about US$21.6 million). Confidence medium: the price rests on one trade report plus the Sotheby's catalogue, and the result sits behind a login.
  - Any Ming porcelain: the Chenghua "chicken cup", Sotheby's Hong Kong, 8 April 2014, HK$281.24 million including premium. Confidence high.
  - The trap: Guinness's "most expensive vase" is the Qianlong (Qing) vase, hammered at £43 million in 2010, never paid for, then sold privately. Wikipedia misdates the cup sale to August.
- **Oldest surviving painting.** "Oldest" depends on the reading, so the answer names it. The painter is unknown for every prehistoric work.
  - Oldest dated cave art of any kind: a hand stencil at Liang Metanduno, Muna Island, Sulawesi, Indonesia, at least 67,800 years old (Nature, 21 January 2026). Confidence high on the date; whether a stencil is a "painting" is the reading.
  - Oldest figurative scene: Leang Karampuang, Sulawesi, at least 51,200 years old (Nature 2024).
  - Neanderthal authorship of the Spanish cave art (over 64,800 years) is disputed.
  - Painting on cloth: the Gebelein linen, Museo Egizio, Turin, 3600–3350 BCE.
  - Greek panel painting: the Pitsa panels, Athens, c. 550–500 BC.
  - The earliest painters known by name are Greek vase painters (Sophilos, c. 590–570 BCE). Confidence medium on that reading.
- **Most expensive painting** (sanity gold): Salvator Mundi, attributed to Leonardo, Christie's New York, 15 November 2017, $450,312,500 including premium. Klimt's *Portrait of Elisabeth Lederer* is second ($236.4 million, November 2025).
- **"Does this contain cubism?"**: graded on museum records, all CC0 at the Cleveland Museum of Art, records re-read 2026-10-21.
  - Positives: Blanchard, *Still Life*, c. 1916 (2026.37); Marcoussis, *Night Café*, c. 1923 (2006.139).
  - Near misses: Cézanne, *Mount Sainte-Victoire*, c. 1904 (1958.21), where "proto-cubist, influenced" is right and "cubist" is wrong; Mondrian, *Composition with Red, Yellow, and Blue*, 1927 (1967.215), De Stijl; Boccioni, *Movement* (1971.38), Futurist.
  - The Met's cubist paintings are not public domain and cannot be fixtures.
- **"Which is more aesthetically pleasing?"**: no external truth exists, so the gold pairs are built: a CC0 original against a deterministic degradation (`aw.py degrade`), and a clean sprite against one with orphans, mixels and blur. Each pair runs in both orders, plus one tie pair (two Hokusai Fuji prints) where declining to rank is right.
- **Theory** (postmodernism, neo-expressionism): graded by rubric. Neo-expressionism is dated to the late 1970s–80s, at least two of Baselitz, Kiefer, Schnabel, Basquiat, Salle and Clemente are named, and the answer says it reacted against minimalism and conceptual art. The rubric's sources (SEP, *Art Since 1900*) get attached in Step 2. Not yet verified against a fetched source.

## 6. Eval plan

Two tiers, in the sibling layout (`evals/cases/<id>/{prompt.md, case.yaml, graders/}` plus `evals.json`):
- **Cheap tier**, on every change, with `regex` and `tool_used` graders only:
  - 8 trigger cases: pairwise, cubism, Ming, oldest, theory, pixel, brief, style vocabulary.
  - 3 decoys: a bakery brand palette for brandwright, a portfolio site direction for sitewright-direction, the founding of the Ming dynasty for historywright.
  - 3 action cases: `aw.py palette`, `pixel` and `sheet`, with fixtures from scaffold scripts.
- **Paid tier**, at creation, after edits and before releases, with `llm` graders and `--judge-model sonnet` and `--max-cost-usd`:
  - Pairwise in both orders, plus a tie pair and a pixel pair.
  - Cubism positive and three near misses; a Ming wine cup judged by the ware's own criteria.
  - Ming price and oldest painting (SimpleQA three-way plus the dispute rubric), and theory.
  - Brief fit with three planted mismatches.
  - Style vocabulary rewrite, and a living artist turned into traits.
  - Guard cases: a weak image with a proud framing must get concrete faults; "is this a real Rubens?" and "is this AI-generated?" must be declined with reasons; "does it follow the golden ratio?" must correct the premise; a reign mark alone must not date a piece.

  The full case table is in [h-testing.md](2026-10-21-creation-pass/h-testing.md). The F traps are added: the Qianlong vase called Ming, 51,200 years given unqualified, a named Lascaux painter.
- **Harness facts:**
  - `@path` does not attach images, so cases use `context.add_dirs` with Read.
  - The `llm` judge does see PNG and JPEG files the run writes, so a sheet can be graded visually.
  - Bash cases need a sandbox: WSL2, Linux or macOS, not native Windows.
- **Unit tests**: stdlib only, with a tiny PNG writer in `tests/`.
  - Palette exactness; grid scale 1–8 and mixed scales; orphan counts.
  - Deterministic sheet size; dHash distance (copies 4 bits or fewer, unrelated images 20 or more); Bradley–Terry on a known tournament.
- **CI**: ubuntu, macOS and Windows on Python 3.9 and 3.14, with the 3.9 Linux job pinned to `ubuntu-24.04`. `ubuntu-latest` will move to 26.04, which has no 3.9 build.
- **Calibration**: 30–50 pairs labelled by Mark (fork 2).
  - Measures: both-orders agreement (target 0.8 or above), accuracy against his labels, and the judge's re-query noise floor.
  - Recomputed whenever the model changes.
  - Optional `bench/agreement.py` fetches 50–200 pairs from Rapidata (CDLA-P) or HPDv3 (MIT) at run time and logs trends. Never a release gate.
- **Licences**: no WikiArt, VAB, LAPIS, BAID or AVA images in the repo (non-commercial, no-derivatives or unknown).

## 7. Rulings made (each in [../decisions/2026-10-21-step1-rulings.md](../decisions/2026-10-21-step1-rulings.md))

- R1: keep the name `artwright`; it is free on GitHub, PyPI and npm.
- R2: the passes ran as general-purpose agents in the evergreen-researcher format.
- R3: four skills (hub, judge, pixel, curate), not one large skill.
- R4: `aw.py` is stdlib first with Pillow optional; Python 3.9+ to match the siblings.
- R5: eval images are fetched by accession number with pinned hashes, not committed.
- R6: art facts route through historywright, and new art sources go into historywright-sources.
- R7: the living-artist rule rewrites the name into traits and does not refuse.
- R8: artwright ships no generator, editor or grid fixer; it points to the maintained ones.

## 8. Forks for Mark

1. **Local aesthetic model: none in v1?** The only one worth bundling (the Apache-2.0 LAION predictor, about 1 GB with CLIP) measures photo polish, prefers images with defects over clean ones 58% of the time, and would need torch. Recommendation: none in v1; name the GPU reward models (HPSv3, UnifiedReward) as pointers only.
2. **Will you label 30–50 image pairs so the judge learns your taste?** The questions come one pair at a time ("which of these two?"), on a page you open once, in Step 3, about 15 minutes. Without it, artwright judges by its rubric alone and cannot say how often it agrees with you. Recommendation: yes.
3. **Should Step 3 wire artwright into comfyui-gen and polywright?** That means one hand-off line in each sibling's skill: "after a batch, call artwright-judge". The alternative is leaving the siblings untouched and letting artwright be called by name. cinewright-qc keeps judging video takes either way. Recommendation: yes, the two one-line hand-offs, each as its own pull request.
4. **Should the living-artist rule rewrite rather than refuse?** When a prompt names a living artist, artwright replaces the name with the traits that make the look (medium, palette, line, subject, era) and says so in one line. Public-domain masters, movements and studio genres may be named. Recommendation: yes, rewrite.
