# Research: artwright

Findings that back the artwright skills (proposed: `artwright`, `artwright-judge`, `artwright-pixel`, `artwright-curate`) and `aw.py`. Changes they cause will be logged in CHANGELOG.md, procedural lessons in LEARNINGS.md, test runs in TESTS.md, and schedule and state in `evergreen.json` once the repository exists (Step 2). Protocol: the installed evergreen plugin's `protocol/PROTOCOL.md`.

Topic: artistic vision and analysis for agents and sibling plugins: judging and comparing images, style and movement, critique of all visual art (pixel and 2D/3D digital art especially), art theory, and art facts held to historywright's standard. Proposed tier `moderate`. Creation pass 2026-10-21; synthesis in [ai-docs/research/2026-10-21-creation-pass.md](ai-docs/research/2026-10-21-creation-pass.md), raw reports in [ai-docs/research/2026-10-21-creation-pass/](ai-docs/research/2026-10-21-creation-pass/index.md).

## Current understanding

- **Judging**:
  - AI aesthetic judgement is far below experts (26.5% against 68.9% on VAB).
  - It is order-sensitive (up to 60.9% of pairwise verdicts flip) and degrades sharply past two candidates.
  - Compare two at a time in both orders, call a split a tie, and keep the judge blind to the user's guess, the model and file names. (R-20261021-2, -3)
- **Critique**:
  - Structured describe, critic, verdict (ArtCoT) beats free reasoning.
  - Claims must point at regions.
  - Critiques must be selective; "looks good" and "feels" language are the default failure. (R-20261021-4)
- **Scores**: learned aesthetic scores measure photo polish, carry documented biases, prefer images with defects, and drive the "AI look" under reward tuning. Never a verdict. (R-20261021-5)
- **Style**:
  - Vision models label styles at about 53% zero-shot.
  - They confuse neighbouring movements and are sometimes right for irrelevant reasons.
  - Western art scores higher than non-Western art.
  - Answer with trait evidence, `member | influenced | no evidence`, and the neighbours considered.
  - Wikidata movement tags cover 1.3% of paintings; absence is not evidence. (R-20261021-6)
- **Evidence on composition and colour**: thirds and the golden ratio fail; curvature is a moderate effect that vanishes for experts; Albers over Itten; order is rarely disliked, complexity depends on context. (R-20261021-7)
- **Pixel art**: fake pixel art is defined by four numbers (colour count, lattice alignment, block uniformity, transitional pixels). Maintained fixers and Aseprite MCP servers exist; artwright checks and points. (R-20261021-8)
- **Generation**:
  - Modern open models read prose through LLM encoders.
  - Negative prompts work only where CFG is above 1: not on Z-Image Turbo or FLUX.2, yes on Qwen-Image.
  - Negation rules differ per model (MiniMax H3 against Veo 3.1).
  - Critic-in-the-loop revision beats parallel sampling. (R-20261021-9)
- **Law**:
  - Human authorship stands (Thaler cert denied 2026-03-02).
  - Andersen v. Stability will not reach summary judgment before late 2027.
  - EU AI Act Article 50 applies from 2026-08-02, with marking for older systems due 2026-12-02. (R-20261021-10)
- **Image cost**: `ceil(w/28) x ceil(h/28)` tokens, 2576 px on 4.7+ models. Size before Read; Claude cannot tell AI-made images. (R-20261021-11)
- **Tooling**: no used art critic exists. Copy the aseprite-ai-artist critic method; point to Aseprite MCPs, pixel fixers and museum MCPs. (R-20261021-12)
- **Sources**:
  - The Met v1 search is retired (use v1.1), and the old Rijksmuseum API is retired.
  - AIC needs an `AIC-User-Agent` header, and Getty SPARQL refuses scripts.
  - Price databases are paid and block agents.
  - Facts route through historywright. (R-20261021-13, -22)
- **Gold answers**:
  - The Ming vase record is the 2011 Yongle meiping (HK$168.66m); the Chenghua cup leads all Ming porcelain.
  - The oldest dated cave art is the Muna stencil (at least 67,800 years, 2026); the oldest figurative scene is Leang Karampuang (at least 51,200).
  - Salvator Mundi is the auction record at $450.3m. (R-20261021-14 to -16)
- **Testing**:
  - Cubism golds are CC0 Cleveland records.
  - Pairwise golds are built by deterministic degradation.
  - `claude plugin eval` passes images through Read and judges image files the run writes.
  - No art dataset can be committed. (R-20261021-17, -18)

## Open questions

- Position-bias rate of Claude Opus 5.5 on art pairs, and whether thinking before the verdict helps: measure in artwright's own eval.
- Grid against separate images for pairwise judging: no direct study; artwright uses separate images.
- Any Ming vase above HK$168.66m sold 2012–2026 (the auction archives sit behind logins).
- Palette licences for Sweetie 16, Endesga 32 and DawnBringer 16/32 (none found; fetched on request, not bundled; R-20261021-24).
- Rijksmuseum data licence today; Paris Musées token rule; National Palace Museum API.
- Sources for Islamic, African, Oceanic, Mesoamerican traditions, the primitivism critique, the Shilpa Shastras, and the Xie He translation debate: drafted from model knowledge, `verified: false` until sourced.
- MiniMax H3 licence territory (the Community License form names USA/EU/UK/South Korea; whether local use there needs approval); Qwen-Image 2.1 commercial terms; Midjourney V8 parameters (R-20261021-27).
- Basquiat and Clemente named as neo-expressionists by a fetched source (Tate names Baselitz, Kiefer, Schnabel, Salle).
- Christie's catalogue glossary (not reachable by the tools); the EU marking date for older systems against the Official Journal text.
- Getty v. Stability Court of Appeal date; Allen v. Perlmutter ruling; Copyright Office Part 3 final; Digital Omnibus changes to Article 50 dates.
- Whether stdlib PNG decoding is fast enough on Python 3.9 (measured on 3.14 only).

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the period since the last refresh. Run `aw.py doctor --probe` first: an endpoint move is the most likely change.

- Subject:
  - arXiv listing API (`export.arxiv.org/api/query`, sorted by date) for `aesthetic AND (MLLM OR VLM) AND (judge OR benchmark)`, `art style AND (VLM OR CLIP)`, `"reward model" AND image AND aesthetic`.
  - SEP aesthetics entries (dated revisions).
  - Museum API docs and change notes (metmuseum.github.io, data.rijksmuseum.nl/docs, api.artic.edu/docs, openaccess-api.clevelandart.org).
  - Generation model cards on huggingface.co and the vendors' prompt guides (docs.bfl.ai, Vertex Veo guide, blog.comfy.org).
  - Legal trackers: chatgptiseatingtheworld.com for Andersen, copyright.gov/ai, the EU Official Journal for Article 50.
  - Nature and Science for new rock-art dates.
  - Auction-house press releases for Ming and record sales.
- Tooling:
  - skills.sh `/api/search?q=art critique|pixel art|aesthetic`.
  - MCP registry `?search=museum|aseprite|pixel`.
  - GitHub `filename:SKILL.md` (not `path:`) art critique.
  - PyPI JSON for Pillow.
  - The pixel fixers' repositories (spritefusion-pixel-snapper, proper-pixel-art, unfake.js).
- Practice:
  - simonwillison.net, fal.ai learn guides, artnet news on AI attribution.
  - Slynyrd Pixelblog catalogue; community.aseprite.org; pixeljoint forum.
- Testing:
  - code.claude.com/docs/en/plugin-evals.
  - VAB and its successors.
  - HF dataset cards for licence changes.
  - actions/python-versions manifest.

## Findings log

### R-20261021-1 · 2026-10-21 · Creation pass
- Summary: Eight parallel research passes in creation mode (A art history and theory, B media and craft, C digital and pixel art, D AI generation, E AI evaluation, F facts and markets, G tooling and efficiency, H testing), each capped at about 25 searches and steered to direct API fetches. Result: AI art judging is weak and order-sensitive but improvable by procedure; no used art critic exists; museum and price sources moved or closed; the gold facts changed in 2026. Five passes hit a session usage limit and were resumed. Cost: searches 125 · fetches 218 · tool calls 429.
- Track: subject
- Sources: ai-docs/research/2026-10-21-creation-pass/ (eight reports)
- Magnitude: n/a (initial)
- Applied: the synthesis (ai-docs/research/2026-10-21-creation-pass.md)

### R-20261021-2 · 2026-05-12 / 2026-10-01 · Pairwise in both orders, two at a time
- Summary: VAB (arXiv 2605.12684, 400 tasks, 10 experts each): best model 26.5% best-and-worst under three orderings, experts 68.9%; four or more candidates degrade models 7.1x against 2.0x for humans; greedy decoding helps 1–2 points. EditJudgeBias (arXiv 2610.01670): swapping order flips up to 60.9% of pairwise verdicts; fabricated majority opinions inflate ratings.
- Track: testing
- Sources: https://arxiv.org/abs/2605.12684, https://arxiv.org/abs/2610.01670
- Magnitude: n/a (initial)
- Applied: rubric.md and artwright-judge (proposed)

### R-20261021-3 · 2026-06-12 · Scores compress and follow one culture's norm
- Summary: VOIR DIRE (arXiv 2606.20676): pools from two cultures agree internally but not with each other (r = -0.12); MLLMs show a positivity floor and orient to one norm; reference demonstrations make it worse. VAB's annotator study: an expert's scores against the same expert's comparisons, Kendall tau 0.188. MLLM-as-a-Judge (2402.04788): human-like on pairs, unlike humans on scores.
- Track: subject
- Sources: https://arxiv.org/abs/2606.20676, https://arxiv.org/abs/2605.12684, https://arxiv.org/abs/2402.04788
- Magnitude: n/a (initial)
- Applied: rubric.md (no lone scores; say whose criteria apply)

### R-20261021-4 · 2025-01 / 2026-06 · Structured critique, selective and grounded
- Summary: ArtCoT (arXiv 2501.09012): free chain-of-thought lowered agreement with experts; describe, critic pass, verdict raised it 29–56% and cut subjective words from 20% to 5.5%. Photo-critique study (arXiv 2606.29689): models comment on every aspect and repeat; judges prefer model critiques anyway. VULCA (2509.23208): technique over-weighted, interpretation thin. aseprite-ai-artist's pixel-critic: cold read before the brief, rule per finding, no "looks good".
- Track: practice
- Sources: https://arxiv.org/abs/2501.09012, https://arxiv.org/abs/2606.29689, https://arxiv.org/html/2509.23208v2, https://github.com/with-pebbly/aseprite-ai-artist
- Magnitude: n/a (initial)
- Applied: the hub's critique procedure (proposed)

### R-20261021-5 · 2026 · Aesthetic and reward scorers measure polish, not art
- Summary: LAION aesthetic predictor audit (arXiv 2601.09896): photo-contest training data, gender and Western skews. On artifact-against-clean pairs it chose the clean image 42% of the time (arXiv 2601.03468); HPS rewards drove oversaturation and structural artifacts. Aesthetic rewards penalise deliberately rough briefs (2512.11883). Reward tuning causes preference mode collapse (D²-Align, CVPR 2026). HPSv3, UnifiedReward and VisionReward are GPU-sized VLMs; aesthetic-predictor-v2.5 is AGPL.
- Track: subject
- Sources: https://arxiv.org/abs/2601.09896, https://arxiv.org/abs/2601.03468, https://arxiv.org/abs/2512.11883, https://arxiv.org/abs/2512.24146
- Magnitude: n/a (initial)
- Applied: no bundled scorer (fork 1); ai-look.md

### R-20261021-6 · 2024–2026 · Style labels need trait evidence
- Summary: Zero-shot WikiArt style accuracy CLIP 24.6%, LLaVA 28.3%, GPT-4o 53.4%; confusions among neighbouring movements; CLIP collapses Cubism into Analytic (2409.03521). About 10% of predictive concepts were irrelevant to art historians (2603.11024). Western art scores higher across 15 VLMs (VULCA-Framework 2601.07984). Wikidata: 14,508 of 1,085,204 painting items carry P135 (probe 2026-10-21).
- Track: subject
- Sources: https://arxiv.org/html/2409.03521v2, https://arxiv.org/abs/2603.11024, https://arxiv.org/abs/2601.07984, https://query.wikidata.org/sparql
- Magnitude: n/a (initial)
- Applied: movements.md (traits per row), the hub's movement procedure

### R-20261021-7 · 1980–2025 · Empirical aesthetics: what holds
- Summary: Thirds does not predict quality (Amirshahi et al. 2014; Palmer lab centre and inward bias). Golden-ratio preference weak in populations (McManus). Curvature g = 0.39, null for experts (Chuquichambi et al. 2022). Colour preference and harmony are separate judgements (Schloss and Palmer 2011). Order and complexity are independent dimensions (Van Geert and Wagemans 2020). Fractal D 1.3–1.5 for statistical fractals only. The Aesthetics Toolbox (MIT, BRM 2025) is the reference metric set.
- Track: subject
- Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC10091794, https://palmerlab.berkeley.edu/spatial.html, https://pmc.ncbi.nlm.nih.gov/articles/PMC4937063, https://pmc.ncbi.nlm.nih.gov/articles/PMC3037488, https://github.com/RBartho/Aesthetics-Toolbox
- Magnitude: n/a (initial)
- Applied: evidence.md, `aw.py stats` (proposed)

### R-20261021-8 · 2025–2026 · Pixel art: checks, rules and fixers
- Summary: Fake pixel art measured (Rangy 2026-08-14): 44,725 colours, 2% lattice alignment, wandering block width; after downsample-then-quantise, 100%. Fixers: Sprite Fusion Pixel Snapper (Rust, 3316 stars), proper-pixel-art 2.0.0 (one grid across all frames), unfake.js (edge-profile grid method, copyable without OpenCV). Rules: Derek Yu's two tutorials, Slynyrd's ramps (hue shift up to 20 degrees per step). Lospec `palette-list/{slug}.json` is keyless. Aseprite 1.3.18.6, EULA forbids redistributing binaries; the .aseprite format parses with struct and zlib.
- Track: subject
- Sources: https://rangy.ai/blog/ai-pixel-art, https://github.com/Hugo-Dz/spritefusion-pixel-snapper, https://github.com/KennethJAllen/proper-pixel-art, https://dev.to/jenissimo/how-to-tame-your-ai-pixel-art-3pk5, https://www.derekyu.com/makegames/pixelart.html, https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes, https://lospec.com/palettes/api
- Magnitude: n/a (initial)
- Applied: artwright-pixel and `aw.py pixel` (proposed)

### R-20261021-9 · 2025–2026 · Generation models and prompt revision
- Summary: Z-Image Turbo needs guidance 0 (negatives do nothing); FLUX.2 does not support negative prompts; Qwen-Image uses true CFG. MiniMax H3 (open weights 2026-08-03) wants timed shot lists, a job per reference, and in-prompt negation; Veo 3.1 wants negatives listed without "no". Iterative VLM-critic refinement beats compute-matched parallel sampling (arXiv 2601.15286). CLIP-era magic words ("trending on artstation", "8k") lose value on LLM-encoder models.
- Track: subject
- Sources: https://huggingface.co/Tongyi-MAI/Z-Image-Turbo, https://docs.bfl.ai/guides/prompting_guide_flux2, https://huggingface.co/Qwen/Qwen-Image, https://fal.ai/learn/devs/minimax-h3-prompting-guide, https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide, https://arxiv.org/abs/2601.15286
- Magnitude: n/a (initial)
- Applied: models/ profiles and artwright-judge's fix channels (proposed)

### R-20261021-10 · 2025–2026 · Law and ethics status (dated; not legal advice)
- Summary: Thaler v. Perlmutter cert denied 2026-03-02 (human authorship required). Andersen v. Stability in discovery; summary judgment not before late 2027 (schedule extended 2026-09-28). Getty v. Stability (UK): Getty largely lost 2025-11-04, permission to appeal the secondary-infringement point. Copyright Office Part 2 (2025-01-29); Part 3 pre-publication (2025-05-09). EU AI Act Article 50 from 2026-08-02; marking for systems on the market earlier by 2026-12-02. Steam disclosure narrowed to player-facing content (2026-01). OpenAI refuses living-artist styles since March 2025.
- Track: subject
- Sources: https://www.scotusblog.com/cases/thaler-v-perlmutter/, https://chatgptiseatingtheworld.com/category/andersen-v-stability-ai/, https://ipkitten.blogspot.com/2026/01/permission-to-appeal-granted-in-getty.html, https://www.copyright.gov/ai/, https://www.stephensonharwood.com/post/102nfqh/eu-ai-act-update-european-commission-adopts-guidelines-on-article-50-transparency-obligations/
- Magnitude: n/a (initial)
- Applied: law.md and the living-artist rule (proposed)

### R-20261021-11 · 2026-10-21 · Claude image cost and limits
- Summary: `ceil(w/28) x ceil(h/28)` visual tokens; Claude 4.7+ up to 2576 px and 4784 tokens, others 1568 px and 1568 tokens; above 20 images per request keep each at 2000 px or less; images before text, labelled "Image 1:"; Claude "cannot determine whether an image is AI-generated". ffmpeg `drawtext` fails on Windows without a font file.
- Track: practice
- Sources: https://platform.claude.com/docs/en/build-with-claude/vision
- Magnitude: n/a (initial)
- Applied: `aw.py fit`, `sheet`, `info` and the refusal guard (proposed)

### R-20261021-12 · 2026-10 · Tooling landscape
- Summary: skills.sh art-critique skills have 1–28 installs; Anthropic's catalog makes art (canvas-design, algorithmic-art, frontend-design) and does not judge it. Aseprite MCPs: diivi/aseprite-mcp (726 stars, lint and colour-stats tools), with-pebbly/aseprite-ai-artist (442 stars, pixel-critic). Museum MCPs: cfpramod/open-museum-mcp (multi-museum), cyanheads Met server. Provenance MCPs: rijksmuseum-mcp-plus, Provenio (beta). midjourney-cc-skill has a seven-dimension critic rubric. Nothing judges ComfyUI output.
- Track: tooling
- Sources: https://skills.sh/api/search?q=art%20critique, https://github.com/diivi/aseprite-mcp, https://github.com/with-pebbly/aseprite-ai-artist, https://github.com/cfpramod/open-museum-mcp, https://github.com/kintopp/rijksmuseum-mcp-plus, https://github.com/JustinPerea/midjourney-cc-skill
- Magnitude: n/a (initial)
- Applied: section 2 of the synthesis (point, do not rebuild)

### R-20261021-13 · 2026-10-21 · Museum and vocabulary routes (probed)
- Summary: Met v1 search returns 410 (retired 2026-10-01); v1.1 pages by offset and limit to 10,000; `/v1/objects/{id}` works; CC0. Old Rijksmuseum API 410; Linked Art search at data.rijksmuseum.nl answers. AIC gives a Cloudflare 403 without an `AIC-User-Agent` header. Cleveland open access healthy (per-record CC0). NGA CC0 CSV daily. Harvard non-commercial, no caching beyond two weeks. Getty vocabularies: XML ended 2026-01-30; SPARQL 403 to scripts; cite AAT by ID through Wikidata P1014.
- Track: subject
- Sources: https://metmuseum.github.io/, https://data.rijksmuseum.nl/docs/, https://api.artic.edu/docs/, https://openaccess-api.clevelandart.org/, https://github.com/NationalGalleryOfArt/opendata, https://www.getty.edu/research-conservation/tools-databases/vocabularies/data-services
- Magnitude: n/a (initial)
- Applied: proposed registry additions for historywright-sources; `aw.py doctor --probe`

### R-20261021-14 · 2011 / 2014 · Gold: the most expensive Ming vase
- Summary: Yongle blue-and-white meiping with fruit sprays (Meiyintang), Sotheby's Hong Kong HK0377 lot 11, October 2011: "sold for HK$168,660,000 / £14,032,792/ US$21,623,077" (Antiques & Art Ireland, 2011-10-05); Sotheby's page shows "MING DYNASTY, YONGLE PERIOD", result behind a login. Any Ming porcelain: Chenghua chicken cup, Sotheby's Hong Kong, 8 April 2014, HK$281.24m including premium (HK$250m hammer). Trap: Guinness's "most expensive vase" is the Qianlong (Qing) Bainbridges vase, unpaid at £43m in 2010. Confidence: medium on the vase, high on the cup.
- Track: subject
- Sources: https://antiquesandartireland.com/2011/10/world-record-ming-vase/, https://www.sothebys.com/en/auctions/ecatalogue/2011/ceramics-myt-hk0377/lot.11.html, https://www.timeslive.co.za/news/south-africa/2014-04-09-ming-dynasty-chicken-cup-smashes-auction-record/, https://www.guinnessworldrecords.com/world-records/498915-most-expensive-vase
- Magnitude: n/a (initial)
- Applied: eval cases outcome-ming-price and trap cases (proposed); re-check by 2027-04-19

### R-20261021-15 · 2026-01-21 · Gold: the oldest surviving painting
- Summary: Oldest dated cave art: hand stencil, Liang Metanduno, Muna Island, Sulawesi, minimum 67.8 ka (U-series 71.6 ± 3.8 ka); Oktaviana et al., Nature 650: 652–656, DOI 10.1038/s41586-025-09968-y. Oldest figurative scene: Leang Karampuang, at least 51,200 years (Nature 631, 2024). Neanderthal Spanish claim (over 64.8 ka, Hoffmann 2018) disputed (White 2020). Gebelein linen, Museo Egizio, 3600–3350 BCE. Pitsa panels, Athens, c. 550–500 BC. Painters unknown for prehistoric work; earliest named painters are Greek vase painters (Sophilos, c. 590–570 BCE).
- Track: subject
- Sources: https://api.crossref.org/works/10.1038/s41586-025-09968-y, https://api.openalex.org/works/doi:10.1038/s41586-025-09968-y, https://www.guinnessworldrecords.com/world-records/782566-oldest-painting-non-figurative-art, https://collezioni.museoegizio.it/en-GB/material/S_17138
- Magnitude: n/a (initial)
- Applied: eval case outcome-oldest-painting (proposed); re-check by 2027-04-19

### R-20261021-16 · 2017 / 2025 · Gold (sanity): the most expensive painting at auction
- Summary: Salvator Mundi, attributed to Leonardo, Christie's New York, 2017-11-15, $450,312,500 including premium ($400m hammer). Second: Klimt, Portrait of Elisabeth Lederer, Sotheby's New York, 2025-11-18, $236.4m (search snippets only). Wikidata's preferred owner statement on Q1892745 is unreferenced: read qualified statements, never the truthy value.
- Track: subject
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1892745, https://www.arabnews.com/art-culture/da-vinci-portrait-of-christ-sells-for-record-4503-million-in-new-york-1194191
- Magnitude: n/a (initial)
- Applied: eval sanity case (proposed)

### R-20261021-17 · 2026-10-21 · Cubism and non-Western fixtures (CC0, Cleveland)
- Summary: Records re-read 2026-10-21, all `share_license_status: CC0`: Blanchard Still Life c. 1916 (2026.37), Marcoussis Night Café c. 1923 (2006.139), Cézanne Mount Sainte-Victoire c. 1904 (1958.21), Mondrian Composition with Red, Yellow, and Blue 1927 (1967.215), Boccioni Movement print (1971.38), Ming Wine Cup with Children at Play 1465–87 (1957.61), Hokusai South Wind, Clear Sky (1930.189). The Met's Gris, Gleizes, Metzinger, Léger and Severini paintings are not public domain. AIC `style_title` gives single-label ground truth (27992 Pointillism).
- Track: testing
- Sources: https://openaccess-api.clevelandart.org/api/artworks/2026.37, https://openaccess-api.clevelandart.org/api/artworks/1958.21, https://openaccess-api.clevelandart.org/api/artworks/1967.215
- Magnitude: n/a (initial)
- Applied: eval fixtures, fetched by accession with pinned hashes (ruling R5)

### R-20261021-18 · 2026-10-21 · Eval harness and CI facts
- Summary: `claude plugin eval` does not expand `@path` into attachments; images reach the agent through `context.add_dirs` plus Read, or a `scaffold_script` (runs only with `--scaffold`). The `llm` grader sees PNG and JPEG files the run writes. No custom-code graders. Bash grants need the OS sandbox (not native Windows). CI: Python 3.9 on Windows and macOS arm64 is 3.9.13; Ubuntu 26.04 has no 3.9; pin the 3.9 Linux job to ubuntu-24.04. Datasets: WikiArt licence unknown, VAB CC BY-NC-ND, LAPIS CC BY-NC, BAID CC BY-NC-ND; HPDv3 MIT and Rapidata CDLA-P allow sample pairs.
- Track: testing
- Sources: https://code.claude.com/docs/en/plugin-evals, https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json, https://huggingface.co/datasets/huggan/wikiart, https://huggingface.co/api/datasets/MizzenAI/HPDv3
- Magnitude: n/a (initial)
- Applied: the eval plan (synthesis section 6)

### R-20261021-19 · 2026-10-16 · Dependencies and sizes
- Summary: Pillow 13.0.0 (2026-10-16) needs Python 3.11+, wheels 4.8–7.3 MB; the last Pillow for 3.9 is 11.3.0. numpy 2.5 needs 3.12 (12.6–17 MB); imagehash pulls numpy, scipy and PyWavelets (45–60 MB); OpenCV headless 35–61 MB; colorthief, haishoku, extcolors unmaintained. A 45-line stdlib PNG decoder ran 0.12–0.24 s per megapixel on 3.14; ffmpeg rawvideo decodes JPEG and WebP in 0.08 s.
- Track: tooling
- Sources: https://pypi.org/pypi/pillow/json, https://pypi.org/pypi/numpy/json, https://pypi.org/pypi/imagehash/json, https://pypi.org/pypi/opencv-python-headless/json
- Magnitude: n/a (initial)
- Applied: ruling R4 and the size budget

### R-20261021-20 · 2023–2026 · Theory and traditions: sources
- Summary: SEP "The Definition of Art" (2024-07-30) maps the families (Dickie, Danto, Levinson, Beardsley, Gaut, Weitz). SEP "Chinese Philosophy: aesthetics of painting and calligraphy" (2026-02-25) omits Xie He. SEP "Japanese Aesthetics" (2023-12-06) glosses terms with usage cautions and lacks *ma*. Fall 2026 surveys use Gardner or Stokstad plus Smarthistory; *Art Since 1900* for the 20th century. Rasa from secondary sources only. Oxford Art Online is paid; Heilbrunn (429) and Smarthistory (403) refuse scripts.
- Track: subject
- Sources: https://plato.stanford.edu/entries/art-definition/, https://plato.stanford.edu/entries/chinese-painting-calligraphy/, https://plato.stanford.edu/entries/japanese-aesthetics/, https://syllabus.uni.edu/sites/default/files/inline-files/arthist-1111-01-fall2026.pdf
- Magnitude: n/a (initial)
- Applied: theory.md and traditions.md (proposed)

### R-20261021-21 · 2023 onward · No attribution or authentication from pixels
- Summary: Art Recognition's AI said Samson and Delilah was not by Rubens at 92%; Rubens scholars disagreed. Two AI analyses reached opposite answers on the de Brécy Tondo. Models and data are proprietary. Pixel-only attribution, authentication and valuation are out of scope; report the catalogue record and say attribution rests on connoisseurship, technical analysis and provenance.
- Track: practice
- Sources: https://news.artnet.com/market/rubens-art-recognition-ai-authentication-2017274, https://news.artnet.com/opinion/ai-art-authentication-2398765
- Magnitude: n/a (initial)
- Applied: a hard guard in every skill; eval case "is this a real Rubens?"

### R-20261021-22 · 2026 · Price databases and attribution vocabulary
- Summary: artnet's terms ban robots and derivative services; Artprice's robots.txt blocks ClaudeBot and anthropic-ai by name; MutualArt full results are paid; Sotheby's results need a login; christies.com was refused to the search tool. Getty Provenance Index CSVs are open on GitHub. Sotheby's glossary (read raw; the fetch summariser had truncated "Attributed to") defines the qualifiers verbatim. Art Basel and UBS report 2026: 2025 sales $59.6 billion.
- Track: subject
- Sources: https://www.artnet.com/about/terms-and-conditions-of-use, https://www.artprice.com/robots.txt, https://github.com/thegetty/provenance-index-csv, https://help.sothebys.com/en/support/solutions/articles/44002518846, https://www.artbasel.com/stories/the-art-basel-and-ubs-global-art-market-report-2026?lang=en
- Magnitude: n/a (initial)
- Applied: market.md; link-out entries proposed to historywright-sources

### R-20261021-23 · 2003 · Hasler–Süsstrunk colourfulness, checked against the paper
- Summary: rg = R − G, yb = ½(R + G) − B on sRGB, signed (no absolute values); M(3) = σ_rgyb + 0.3·μ_rgyb. Table 2 anchors for M(3): not 0, slightly 15, moderately 33, averagely 45, quite 59, highly 82, extremely 109 colourful. Anchor points on a fitted scale, not band edges; 95.3% correlation with 20 viewers on 84 images. The live EPFL file fails; the Wayback copy reads. Closes the open question on thresholds and sign.
- Track: subject
- Sources: http://web.archive.org/web/20180325055754id_/https://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf (DOI 10.1117/12.477378)
- Magnitude: 0.1 (numbers confirmed; labelling changed to the nearest anchor)
- Applied: aw.py stats, skills/artwright/references/evidence.md

### R-20261021-24 · 2026-10-21 · Lospec palette API and terms (probed)
- Summary: `lospec.com/palette-list/<slug>.json` returns `{name, author, colors}` (hex without #, case varies, author often empty); a 404 body is `{"error":"palette not found"}`; no key, no rate headers, open CORS. The API page invites per-slug fetches on a user's request; the terms forbid copying "any portion of the Service" and scraping. PICO-8's palette is CC0 (Lexaloffle FAQ); no licence found for Sweetie 16, Endesga 32, DawnBringer 16/32. The NES slug is `nintendo-entertainment-system`.
- Track: tooling
- Sources: https://lospec.com/palettes/api, https://lospec.com/terms-and-conditions, https://www.lexaloffle.com/pico-8.php?page=faq
- Magnitude: 0.3 (only PICO-8 bundled; others fetched on request and cached in ARTWRIGHT_HOME)
- Applied: aw.py `get_palette`, artwright-pixel SKILL.md, ai-docs/decisions/2026-10-21-step2-build.md (B2)

### R-20261021-25 · 2026-09-17 · Aesthetics Toolbox metric names and directions
- Summary: RBartho/Aesthetics-Toolbox (MIT) names: RMS contrast (SD of L*, 0–50), Edge density, Mirror symmetry (percent on a binarised image), Balance (mean of eight weight-difference percentages: 0 is balanced), DCM distance and position, 2D Fractal dimension (box counting), Self-similarity, Anisotropy and more. It has no colourfulness metric.
- Track: tooling
- Sources: https://github.com/RBartho/Aesthetics-Toolbox (QIP_machine_script.py, AT/balance_qips.py)
- Magnitude: 0.2
- Applied: aw.py stats (RMS contrast on L*, `imbalance_pct` with 0 as centred, notes where aw.py differs), evidence.md

### R-20261021-26 · 2026-10-21 · Movement items on Wikidata and Wikipedia (verification route)
- Summary: 123 movement rows checked through the Wikipedia action API (20 titles per call) and one Wikidata SPARQL VALUES query (QID, AAT P1014, dates); 97 verified, 26 not. About 40 of 134 items lack an AAT ID; several titles resolve to the wrong item (Symbolism (arts), Literati painting, Zhe school, Olmec and Aztec art). The REST summary endpoint rate-limits after about 20 calls. SEP has no entry for rasa, Indian or Islamic aesthetics; SEP's Japanese Aesthetics never uses "wabi-sabi" as a compound (backs the borrowed-term guard). New SEP entry Race and Aesthetics (2026-09-22). Tate withdrew its primitivism text; Tate dates neo-expressionism to the 1980s as a reaction to minimalism and conceptual art.
- Track: subject
- Sources: https://en.wikipedia.org/w/api.php, https://query.wikidata.org/, https://plato.stanford.edu/entries/japanese-aesthetics/, https://plato.stanford.edu/entries/aesthetics-race/, https://www.tate.org.uk/art/art-terms/n/neo-expressionism
- Magnitude: 0.2
- Applied: skills/artwright/references/movements.md, theory.md, traditions.md

### R-20261021-27 · 2026-10-21 · Generation model facts re-checked
- Summary: FLUX.2 [klein] 9B is FLUX Non-Commercial (only klein 4B is Apache-2.0); both run 4 steps at guidance 1. Z-Image Turbo: guidance 0, Apache-2.0; Z-Image base honours negatives at CFG 3–5. Qwen-Image (original) is Apache-2.0 with true CFG 4; Qwen-Image 2.1 is 7B under the Qwen Research License. MiniMax H3: CFG-distilled checkpoints (negatives unlikely to work), a Community License whose form names USA/EU/UK/South Korea. Wan 2.2 is the newest downloadable Wan. `gpt-image-2` is OpenAI's current image model.
- Track: subject
- Sources: https://huggingface.co/black-forest-labs/FLUX.2-klein-9B, https://huggingface.co/black-forest-labs/FLUX.2-klein-4B, https://huggingface.co/MiniMaxAI/MiniMax-H3, https://huggingface.co/Qwen/Qwen-Image-2.1, https://github.com/Wan-Video/Wan2.2, https://developers.openai.com/api/docs/guides/image-generation
- Magnitude: 0.3 (the klein licence corrects D-F3)
- Applied: skills/artwright-judge/references/models/

### R-20261021-28 · 2026-10-21 · Law table re-verified
- Summary: Thaler cert denied 2026-03-02 (docket 25-449). No Court of Appeal judgment yet in Getty v. Stability. Andersen schedule extended about three months on 2026-09-28. Allen v. Perlmutter: no ruling found. Copyright Office Part 3 still pre-publication. The Digital Omnibus on AI is reported as Regulation (EU) 2026/1744 (secondary; EUR-Lex refused the fetch). Steam's Content Survey covers pre-generated and live-generated AI content.
- Track: subject
- Sources: https://www.supremecourt.gov/, https://caselaw.nationalarchives.gov.uk/, https://www.copyright.gov/ai/, https://partner.steamgames.com/doc/gettingstarted/contentsurvey
- Magnitude: 0.1
- Applied: skills/artwright/references/law.md

### R-20261021-29 · 2026-10-21 · Art source routes and the AIC header
- Summary: AIC's API answers 403 without an `AIC-User-Agent` header, whatever the User-Agent; historywright's `artic` route was broken. Getty Provenance Index CSVs are CC0 per dataset. Museo Egizio has HTML search only, images CC0. Sotheby's glossary re-read verbatim, including its Chinese-ceramics period rules; Christie's glossary unreachable. A year-to-date search found no Ming vase above HK$168.66m.
- Track: subject
- Sources: https://api.artic.edu/docs/, https://github.com/thegetty/provenance-index-csv, https://collezioneonline.museoegizio.it/, https://help.sothebys.com/en/support/solutions/articles/44002518846
- Magnitude: 0.2
- Applied: skills/artwright/references/market.md; the historywright-sources proposal (ai-docs/notes/2026-10-21-historywright-sources-proposal.md)

### R-20261021-30 · 2026-10-21 · Ceramics sources
- Summary: firing ranges (Science Museum Group: earthenware 926–1150 °C, stoneware 1205–1260 °C, porcelain 1280–1400 °C); reign marks regular from Xuande, Chenghua the most copied, Kangxi apocryphal Ming marks, "we cannot rely on them as proof of authenticity"; Ming 1368–1644 (Q9903), Qing 1644–1912 (Q8733). Cleveland's 1957.61 Chenghua wine cup is CC0 with the museum's own judging language.
- Track: subject
- Sources: https://collection.sciencemuseumgroup.org.uk/objects/co418180, https://aziatischekeramiek.nl/en/learn/7579-reign-marks-on-chinese-ceramics, https://openaccess-api.clevelandart.org/api/artworks/1957.61
- Magnitude: n/a (initial)
- Applied: skills/artwright/references/ceramics.md
