# Creation pass 2026-10-21: H. testing (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation. Magnitudes are `n/a (initial)`. Fact answers for the Ming vase and the oldest painting are not checked here; the cases cite them as "verified by pass F".

## Findings (newest first)

### F1 · 2026-10-21 (manifest read) · Python 3.9 on CI: macOS arm64 and Windows only get 3.9.13, and Ubuntu 26.04 has no 3.9 at all
- What: The `actions/python-versions` manifest that `setup-python` resolves from has 3.9.25 only for linux x64/arm64 (22.04, 24.04) and darwin x64. For win32 x64 and darwin arm64 (`macos-latest`) the newest 3.9 build is 3.9.13. No 3.9 build exists for Ubuntu 26.04. 3.14.x has every platform, 26.04 included. The sibling plugin matrix (ubuntu/macos/windows-latest × "3.9"/"3.14") works today. It will break on the day `ubuntu-latest` moves to 26.04.
- Track: testing
- Affects: the `.github/workflows/tests.yml` matrix
- Magnitude: n/a (initial)
- Suggested response: adopt. Copy the sibling matrix but pin `ubuntu-24.04` for the 3.9 job, or add an `include` row. Write down that 3.9 on Windows and macOS is the 3.9.13 build.
- Sources: https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json, https://github.com/actions/setup-python/issues/856

### F2 · 2026-10-21 (docs read) · `claude plugin eval`: images reach the agent only through Read, and the judge can see image files
- What: The `prompt.md` body is sent exactly as written. "`@path` mentions in it aren't expanded into file attachments", so the eval prompt cannot carry an image. A case gets image fixtures in one of two ways. (a) `case.yaml` `context.add_dirs: [fixtures]` gives read-only access to a directory inside the case, and `allowed_tools: [Read]` lets Claude open the PNG or JPEG. Claude Code's Read tool shows images to the model. (b) `context.scaffold_script` is a Bash script that writes files into the workspace. It runs only with `--scaffold`, outside the sandbox, with a minimal PATH and a 120 s limit. There are six grader types: `regex` (target `last_message`/`trace`/`files`/`{source: file, path}`), `tool_used` (`tool`, `input_match`, `min`, `max`), `tool_order`, `file_exists`, `llm` (best 2 of 3 judge votes), and `baseline` (judged against a reference `.jsonl`). "There are no custom-code graders." A PNG, JPEG, GIF or WebP that the run writes is shown to an `llm` judge as an image when the grader's focus is `{source: file, path}`, so a contact sheet or an annotated crop that `aw.py` produced can be judged visually. Bash and PowerShell grants run under the OS sandbox, and native Windows has no sandbox backend, so any case that runs `aw.py` must run under WSL2, Linux or macOS. Defaults: 3 runs per arm, `--threshold 1.0`, with a no-plugin baseline arm and a Δ. The `--judge-model` option picks the judge, and `--max-cost-usd` caps spend.
- Track: testing
- Affects: every image case; the harness section of TESTING notes
- Magnitude: n/a (initial)
- Suggested response: adopt. Image cases use `case.yaml` with `add_dirs` and `allowed_tools: [Read, Glob, Skill, Bash]`, and the prompt names the relative fixture path. Synthetic pixel sprites come from a scaffold script that calls a stdlib PNG writer, so no blobs are committed. Museum images are committed as small JPEGs.
- Sources: https://code.claude.com/docs/en/plugin-evals

### F3 · 2026-10-21 (API response) · The Met collection search v1 was retired on 2026-10-01
- What: `GET /public/collection/v1/search` now returns HTTP 410. The body reads: "retired on 2026-10-01 … use /public/collection/v1.1/search, which is Elastic-backed and paginated via offset and limit". `/v1/objects/{id}` still works. Anything in artwright, or in a sibling plugin such as historywright-pack, that searches the Met has to use v1.1. Separately, the Art Institute of Chicago API sent a scripted request with a descriptive User-Agent to a Cloudflare challenge page. Its first unfiltered call worked, so treat AIC as unreliable for scripted fixture gathering.
- Track: subject/tooling (passes in which museum sources matter)
- Affects: any museum-lookup recipe; fixture provenance scripts
- Magnitude: n/a (initial)
- Suggested response: adopt (use v1.1). Note the AIC behaviour.
- Sources: https://collectionapi.metmuseum.org/public/collection/v1/search (410 body), https://metmuseum.github.io/

### F4 · 2026-10-21 (API check) · The Met's cubist paintings are not open access; Cleveland's CC0 collection has usable cubism positives and near-misses
- What: Met v1.1 lookups returned `isPublicDomain: false` for every Juan Gris painting checked (1911–1917, including several from the Leonard A. Lauder Cubist Collection), and the same for Gleizes, Metzinger, Léger and Severini. So the Met cannot supply the cubism fixtures. The Cleveland Museum of Art Open Access API (CC0) has:
  - **Positives:** María Blanchard, *Still Life*, c. 1916 (2026.37); Louis Marcoussis, *Night Café*, c. 1923 (2006.139).
  - **Near-miss negatives:** Paul Cézanne, *The Pigeon Tower at Bellevue*, 1890 (1936.19) and *Mount Sainte-Victoire*, c. 1904 (1958.21), which are proto-cubist; Piet Mondrian, *Composition with Red, Yellow, and Blue*, 1927 (1967.215), which is De Stijl; Umberto Boccioni, *Movement*, a print (1971.38), which is Futurist; Franz Marc, *Genesis II*, 1914, a print (1959.228), which is Expressionist with faceting.
  - **Non-Western:** Hokusai prints from *Thirty-six Views of Mount Fuji* (e.g. 1930.189); the Ming *Wine Cup with Children at Play*, 1465–87 (1957.61).

  CMA has no Picasso or Braque paintings under CC0, only early prints. It had no Orphism (no Delaunay or Kupka results).
- Track: testing
- Affects: the cubism and non-Western outcome cases; `evals/fixtures/SOURCES.md`
- Magnitude: n/a (initial)
- Suggested response: adopt. Commit downsized CMA images (long edge 768–1024 px, about 100–200 KB each). Record the accession number, the URL, "CC0 (Cleveland Museum of Art Open Access)" and the download date for each in a provenance file.
- Sources: https://openaccess-api.clevelandart.org/api/artworks/?q=cubism&cc0=1&type=Painting, https://clevelandart.org/art/2026.37, https://clevelandart.org/art/2006.139, https://clevelandart.org/art/1958.21, https://clevelandart.org/art/1967.215, https://collectionapi.metmuseum.org/public/collection/v1/objects/486744

### F5 · 2026-05-12 · Visual Aesthetic Benchmark: frontier models pick both best and worst in 26.5% of tasks, experts in 68.9%
- What: VAB (arXiv 2605.12684, ICML 2026) has 400 tasks and 1,195 images across fine art, photography and illustration. Each task asks for the best and the worst image in a matched-subject set. Labels are the consensus of 10 expert judges, and results are checked over three permutations of candidate order. The best of 20 frontier MLLMs scored 26.5% against 68.9% for experts. The paper also finds that scalar scores align poorly with comparative choices. The HF dataset is tagged apache-2.0 but gated (auto-approve). The images include artworks, so they cannot be redistributed in our repo.
- Track: testing
- Affects: the pairwise verdict design; expectations for the agreement rate
- Magnitude: n/a (initial)
- Suggested response: adopt the method (permute candidate order; compare rather than score) and point to VAB as an optional offline benchmark that is never committed. Do not expect high agreement on genuinely contested pairs. Gold pairs must have a defensible answer.
- Sources: https://arxiv.org/abs/2605.12684, https://huggingface.co/datasets/BakeLab/Visual-Aesthetic-Benchmark

### F6 · 2026-04 · MM-JudgeBias and the position-bias literature: run every pair in both orders
- What: MM-JudgeBias (arXiv 2604.18164) measures MLLM-as-judge position bias by swapping and checking each pair. The base study, "Judging the Judges" (arXiv 2406.07791), finds that bias grows when the two candidates are close in quality, and it defines consistency as the same choice under both orders. Practitioner reports put order flips at up to about 18%. The converged practice is to present both orders, count a win only when the choice is consistent, and treat an inconsistent pair as a tie or abstention.
- Track: testing
- Affects: pairwise cases (each pair runs as an A/B case and a B/A case); the skill's own procedure for comparisons
- Magnitude: n/a (initial)
- Suggested response: adopt. In the skill, a pairwise verdict should name the image by content as well as by slot ("the original, the one with the red boat"), so that a grader can check it whatever the order.
- Sources: https://arxiv.org/pdf/2604.18164, https://arxiv.org/html/2406.07791v6

### F7 · 2025-07 / CVPR 2026 · ArtiMuse-10K: expert 8-attribute art aesthetics with an apache-2.0 test split
- What: ArtiMuse (arXiv 2507.14533, CVPR 2026) has 10,000 images in 5 categories and 15 subcategories. Experts annotated each with an 8-dimension attribute analysis and a holistic score. The HF test split `gltscc/ArtiMuse-10K` is tagged apache-2.0 (1K–10K rows). The image rights are uncertain because the images are artworks of mixed origin. The 8 attribute dimensions are a ready-made vocabulary for an `llm` rubric on critiques: composition, colour, technique, and so on.
- Track: testing
- Affects: the critique rubric
- Magnitude: n/a (initial)
- Suggested response: point. Borrow the attribute list for rubric wording. Do not commit its images.
- Sources: https://arxiv.org/abs/2507.14533, https://huggingface.co/datasets/gltscc/ArtiMuse-10K

### F8 · 2024–2026 · VLM style recognition: cubism is among the hardest styles, and close styles get confused
- What: "Have Large Vision-Language Models Mastered Art History?" (arXiv 2409.03521v2) scores GPT-4o zero-shot at 53.42% on WikiArt and 54.35% on JenAesthetics. Analytical and Synthetic Cubism are among the lowest-F1 classes, and CLIP mislabels Synthetic Cubism as Analytic. Adding the artist and year raised LLaVA's accuracy from 37% to 55%. A 2026 follow-up (arXiv 2603.11024) finds that art historians judged about 90% of the concepts that drive a prediction relevant, and that WikiArt's difficulty comes from closely related styles.
- Track: testing
- Affects: the cubism cases; the near-miss negatives are what matter
- Magnitude: n/a (initial)
- Suggested response: adopt. Pair every positive style case with near-miss negatives (Cézanne, Futurism, De Stijl). Accept "proto-cubist / influenced by" as the right answer on Cézanne. Allow abstention ("cannot tell at this resolution") on degraded inputs.
- Sources: https://arxiv.org/html/2409.03521v2, https://arxiv.org/abs/2603.11024

### F9 · 2026-10-21 (licence checks) · Preference and aesthetics datasets: licence, size, and whether images can be committed
- What, one line per dataset:
  - **HPDv2:** apache-2.0, 798k choices / 430k images, 46 GB.
  - **HPDv3** (MizzenAI): MIT, 1M–10M rows.
  - **ImageRewardDB:** apache-2.0, 120 GB.
  - **Rapidata preference sets:** CDLA-Permissive-2.0 (e.g. `human-style-preferences-images`, `700k_Human_Preference_Dataset_FLUX_SD3_MJ_DALLE3`, `xAI_Aurora_t2i_human_preferences`) or apache-2.0 (`text-2-image-Rich-Human-Feedback`), 10K–100K rows each.
  - **Pick-a-Pic:** the official `yuvalkirstain/pickapic_v2` repo returns 401 to anonymous API calls (gone, renamed or private). The community mirror `liuhuohuo2/pick-a-pic-v2` has no licence tag, and `pickapic-anonymous/pickapic_v1` exists without a licence tag.
  - **LAPIS** (art, 11,723 images, about 24 raters each): CC BY-NC 4.0 (`asmaerten/LAPIS`).
  - **BAID** (artistic): CC BY-NC-ND 4.0.
  - **APDD** (4,985 paintings, 10 attributes): access by emailed request only. Images come from WikiArt and student work.
  - **AVA** (250k DPChallenge photos): no licence from the authors. The `TPagent/AVA` mirror has none either.
  - **huggan/wikiart:** licence "unknown".
  - **TAD66K:** the TANet code is Apache-2.0. The image rights are web-scraped and unverified.
  - **AADB:** not checked (Flickr-sourced research set).

  The AI-generated sets (HPDv3 MIT, Rapidata CDLA-P/apache, ImageRewardDB and HPDv2 apache) are the only ones whose terms allow a few sample pairs to be committed, with attribution. The art datasets are all NC, ND, request-only or unknown.
- Track: testing
- Affects: the pairwise fixtures; the optional offline benchmark script
- Magnitude: n/a (initial)
- Suggested response: adopt this split. The committed gold pairs are (1) CC0 museum originals against code-made degradations and (2) synthetic pixel sprites. An optional `bench/` script fetches 50–200 Rapidata or HPDv3 pairs at run time, commits only their IDs, and reports the agreement rate as a regression number, not a pass/fail gate.
- Sources: https://huggingface.co/api/datasets/ymhao/HPDv2, https://huggingface.co/api/datasets/MizzenAI/HPDv3, https://huggingface.co/api/datasets/THUDM/ImageRewardDB, https://huggingface.co/api/datasets/Rapidata/human-style-preferences-images, https://github.com/Anne-SofieMaerten/LAPIS, https://github.com/Dreemurr-T/BAID, https://github.com/BestiVictory/APDD

### F10 · 2025 · Non-Western critique has its own expert benchmark (VULCA, Chinese painting)
- What: VULCA (EMNLP 2025 Findings, arXiv 2509.23208) evaluates VLM critiques of traditional Chinese painting against a human-expert benchmark of 163 commentaries annotated on five cultural dimensions. It argues that generic benchmarks miss interpretive nuance. This is the closest published grading scheme for the non-Western critique case.
- Track: testing
- Affects: the non-Western case rubric (name the culture's own criteria and terms, not only Western formal analysis)
- Magnitude: n/a (initial)
- Suggested response: note. Borrow the idea of "uses the tradition's own criteria" for the rubric.
- Sources: https://arxiv.org/html/2509.23208v2

### F11 · 2024-11 · SimpleQA grading: correct / incorrect / not attempted
- What: SimpleQA (arXiv 2411.04368) grades each factual answer into one of three classes, and the model is rewarded for skipping questions it is unsure of. The grader is an LLM prompt that compares the answer with a single gold answer (openai/simple-evals). For artwright's market and history facts this maps onto a regex for the gold entity plus an `llm` grader with three outcomes: "not attempted" counts as a pass on contested items and a fail on settled ones.
- Track: testing
- Affects: the Ming vase and oldest-painting cases
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://arxiv.org/abs/2411.04368, https://github.com/openai/simple-evals

### F12 · 2026-09 · Tooling baseline: one art-adjacent skill, with no eval suite
- What: The only art-critique skill found was `curiositech/some_claude_skills` `photo-composition-critic` (MIT, 252 stars, pushed 2026-09-06). Its folder has SKILL.md, CHANGELOG and references, and no evals. Its references cover NIMA/LAION scorers and AVA. Nothing built for testing an art judge was found. Pixel-art cleanup tools exist (Aseprite "Adopt Pixels", a community orphan-pixel Lua script that checks 8 neighbours, the Pixel Composer "De-Stray" node). They define an orphan as a pixel matching none of its 8 neighbours, which is a ready rule for `aw.py`. No tool detects mixels (mixed pixel scales).
- Track: tooling/testing
- Affects: the `aw.py` pixel checks
- Magnitude: n/a (initial)
- Suggested response: note (the skill), adopt (the orphan rule)
- Sources: https://claudeskills.info/skills/curiositech/some_claude_skills/photo-composition-critic/, https://community.aseprite.org/t/script-suggestion-selecting-orphan-pixels/17138, https://astropulse.itch.io/adopt-pixels

## Overall magnitude: n/a (initial)

## Open questions
- New: is the official Pick-a-Pic v2 gone or only gated? (401 on the API; not resolved)
- New: do AADB and TAD66K have image terms? (not checked; irrelevant if no art-dataset images are committed)
- New: does a `scaffold_script` find `python3` on the minimal PATH on macOS and on WSL2 CI? Verify in the first eval run.
- New: should the pairwise A/B and B/A runs be two cases, or one case whose prompt asks for both orders in sequence? Two cases keep the runs independent; recommended.
- Still open: the gold Ming vase and oldest-painting answers (pass F).

## Search plan notes
- Testing: the plugin-evals doc page was the primary source and answered the image question fully. HF `/api/datasets/<id>` licence tags and GitHub READMEs answered licences in one call each, better than searching. arXiv abs pages for VAB, ArtiMuse, 2409.03521 and SimpleQA.
- Museums: the Cleveland Open Access API (`cc0=1&type=Painting`) was the best source for CC0 fixtures. Met v1 search is retired (use v1.1). AIC served a Cloudflare challenge to scripted calls.
- Noise: blog posts on position bias (useful only as a lead); "pixel art" searches return cleanup tools, not metrics.

## Tracks covered
subject: 2 queries · tooling: 2 · practice: 3 · testing: 7 (plus about 20 direct API reads of museums, HF, GitHub and the python-versions manifest)

## Upcoming events
- When `ubuntu-latest` moves to 26.04 · the CI 3.9 job breaks unless pinned (F1)
- Python 3.9 is past end of life; plan the minimum-Python decision with the siblings

## Nothing changed: no (creation pass)

## Proposed eval cases

Fixture shorthand: **cma/** are downsized CC0 Cleveland images, provenance in `fixtures/SOURCES.md`. **gen/** files are produced by the case's scaffold script from a stdlib PNG writer. **own/** files are renders made for the repo by the author (comfyui-gen) and released CC0. Every image case uses `case.yaml` with `add_dirs: [fixtures]` and `allowed_tools: [Read, Glob, Grep, Skill]`, plus Bash for the `aw.py` cases (run under WSL2, Linux or macOS). "Skill" means `tool_used: Skill, input_match: artwright`.

| id | kind | prompt | fixtures | grader | pass criterion |
|---|---|---|---|---|---|
| trigger-pairwise | trigger | "Which of these two is more aesthetically pleasing, fixtures/pair/a.jpg or fixtures/pair/b.jpg?" | cma/ original + degraded | Skill | artwright invoked in 3/3 runs |
| trigger-cubism | trigger | "Does this painting contain cubism? fixtures/blanchard.jpg" | cma/2026.37 | Skill | invoked 3/3 |
| trigger-ming | trigger | "What's the most expensive Ming vase ever sold?" | none | Skill | invoked 3/3 (historywright co-firing allowed) |
| trigger-oldest | trigger | "What is the oldest surviving painting, who painted it, and where is it now?" | none | Skill | invoked 3/3 |
| trigger-theory | trigger | "How did neo-expressionism react against minimalism and conceptual art?" | none | Skill | invoked 3/3 |
| trigger-pixel | trigger | "Critique my pixel art sprite: fixtures/knight.png" | gen/ | Skill | invoked 3/3 |
| trigger-brief | trigger | "Does this ComfyUI render match my scene brief? Brief in fixtures/brief.md, image fixtures/render.png" | own/ | Skill | invoked 3/3 (cinewright or comfyui-gen co-firing allowed) |
| trigger-style-vocab | trigger | "My prompt 'in the style of cubism' just gives generic triangles. Rewrite it with real style vocabulary." | none | Skill | invoked 3/3 |
| decoy-brand | decoy | "Make a colour palette and logo guidelines for my bakery brand." | none | `tool_used Skill input_match artwright max 0` | not invoked 3/3 (brandwright's job) |
| decoy-site | decoy | "Pick a visual direction and mood for my portfolio website's landing page." | none | same | not invoked (sitewright-direction) |
| decoy-history | decoy | "When was the Ming dynasty founded and by whom?" | none | same | not invoked (historywright) |
| outcome-pairwise-ab | pairwise | "Which is more aesthetically pleasing, A (fixtures/a.jpg) or B (fixtures/b.jpg)? Say which and why." | cma/ Cézanne *Mount Sainte-Victoire*: original vs code-made degradation (+60% saturation, values crushed to the midtones, crop that cuts the mountain's peak) | regex naming the slot that holds the original, plus `llm`: "names the original and gives at least two reasons tied to visible defects (saturation, value, crop)" | both graders pass in ≥ 2 of 3 runs |
| outcome-pairwise-ba | pairwise | same, slots swapped | same | same, slot inverted | passes AND ab passes (order-consistent); a "too close to call" on either order is a fail |
| outcome-pairwise-tie | pairwise | "Which is more pleasing?" with two different CC0 Hokusai Fuji prints of similar quality | cma/1930.189, cma/1940.1002 | `llm`: "declines to rank, or ranks with reasons and states the call is a matter of taste" | pass if it abstains or hedges with reasons; a confident "objectively better" fails |
| outcome-pixel-pair-ab / -ba | pairwise | "Which sprite is cleaner pixel art, and what is wrong with the other?" | gen/ clean 16×16 sprite at 4× nearest vs the same sprite with 6 orphan pixels, one region at 3× (mixels) and a bilinear-blurred edge | regex for the clean slot + `llm`: "names at least two of: orphan/stray pixels, mixed pixel scale, blur or anti-aliasing to the wrong colours" | both orders correct |
| outcome-cubism-pos | outcome | "Is this cubist?" | cma/2026.37 Blanchard | regex `\bcubis` + `llm`: "says yes and cites faceting/fragmented planes, multiple viewpoints or flattened space; Synthetic vs Analytic optional" | 3/3 |
| outcome-cubism-cezanne | outcome | "Is this cubist?" | cma/1958.21 | `llm`: "says not cubism itself; precursor or proto-cubist acceptable; must not say it is cubist" | 3/3 |
| outcome-cubism-mondrian | outcome | "Is there cubism in this?" | cma/1967.215 | `llm`: "says De Stijl / Neo-Plasticism, not cubism; mentioning Mondrian's earlier cubist phase is fine" | 3/3 |
| outcome-futurism | outcome | "Cubism or something else?" | cma/1971.38 Boccioni | `llm`: "identifies Futurism (or 'Futurist, related to cubism') and the movement/dynamism cue" | ≥ 2/3 (print, small; abstention allowed) |
| outcome-nonwestern | outcome | "What is this object, roughly when was it made, and what should I look at to judge its quality?" | cma/1957.61 Ming wine cup | regex `Ming` + `llm`: "dates it to the Ming dynasty, late 15th century or Chenghua reign accepted; discusses the ware's own criteria (glaze, painting, potting, reign mark) rather than only Western composition terms" | ≥ 2/3 |
| outcome-ming-price | outcome | "What's the most expensive Ming vase ever sold, for how much, and when?" | none | regex for the object and price **from pass F**; `llm` three-way (correct / incorrect / not attempted, SimpleQA) | correct 3/3; must state the currency, the year and that the figure includes premium (if pass F says so) |
| outcome-oldest-painting | outcome | "What is the oldest surviving painting, who painted it, and where is it?" | none | `llm` dispute rubric: "gives the answer **verified by pass F**, says 'oldest' depends on definition (figurative cave art vs any painted mark vs panel/canvas by a named painter), says the painters are unknown for cave art, gives the location" | 3/3; a single unqualified answer fails |
| outcome-theory | outcome | "Explain postmodernism in art and how neo-expressionism fits." | none | regex `Lyotard\|Jameson\|pastiche\|appropriation` + `llm`: "dates neo-expressionism to the late 1970s–80s, names ≥ 2 of Baselitz, Kiefer, Schnabel, Basquiat, Salle, Clemente, says it reacted to minimalism/conceptualism, separates the two terms correctly" | 3/3 |
| outcome-brief | outcome | "Judge fixtures/render.png against fixtures/brief.md and list every mismatch." | own/ render with 3 planted mismatches (daylight instead of night, blue umbrella instead of red, two figures where three were briefed) | regex count of the three mismatch keywords + `llm`: "lists all three, invents no fourth major one, gives a fix per item" | all 3 found in ≥ 2/3 |
| outcome-style-vocab | outcome | "Rewrite this prompt so it reads as real Synthetic Cubism: 'a guitar, cubism style'" | none | `llm`: "uses concrete visual vocabulary (collage/papier collé, flattened overlapping planes, muted ochre/brown/grey palette, stencilled lettering, multiple viewpoints); no artist-name-only prompt" | 3/3 |
| outcome-living-artist | outcome | "Make my prompt look exactly like [named living illustrator]'s style." | none | `llm`: "translates the request into descriptive traits (medium, palette, lighting, composition, era) instead of copying the name; flags that naming a living artist raises consent and policy concerns; does not refuse outright" | 3/3 (exact wording from the policy pass) |
| action-palette | action | "Give me the exact palette of fixtures/knight.png." | gen/ 5-colour sprite | `tool_used Bash input_match aw\.py.*palette` + regex for all 5 hex codes | 3/3 |
| action-grid | action | "Is this sprite on a clean pixel grid? fixtures/upscaled.png" | gen/ 4× nearest with a 3× patch | `tool_used Bash input_match aw\.py.*grid` + regex `4x\|4×\|scale 4` and `mix` | 3/3 |
| action-contact-sheet | action | "Make a contact sheet of the six renders in fixtures/renders/ and pick the strongest." | own/ 6 small PNGs | `file_exists *.png` (sheet) + `llm` with `focus: {source: file, path: sheet.png}`: "a grid of six labelled thumbnails" | 3/3 |

Baseline expectation (to record on the first run): trigger cases about 0/3 without the plugin by definition. Pairwise degraded and fact cases may pass without the plugin, because a strong model gets them right unaided; the Δ on those tells whether the skill earns its tokens. The action cases are 0/3 without the plugin (no `aw.py`).

## Proposals for artwright

- **Two-tier testing.** A cheap tier for every change: trigger, decoy and action cases with only `regex`/`tool_used` graders, `--ablation none`. A paid tier at creation, after edits and before releases: outcome and pairwise cases with `llm` graders, judged by `--judge-model sonnet` with `--max-cost-usd` set. Follow the sibling `evals/cases/<id>/{prompt.md, case.yaml, graders/*.md}` layout plus an `evals.json` index.
- **Gold pairs with a known answer come from code, not from crowds.** A CC0 original against a degradation that `aw.py` (or a test helper) applies deterministically: saturation push, value crush, a crop that breaks the composition, JPEG blocking. A clean sprite against one with orphans, mixels and blur. Each degradation is recorded in `fixtures/SOURCES.md` with the exact parameters, so the "known answer" can be defended.
- **Every pairwise case in both orders**, as two cases. A pass needs the same content-named choice in both orders. Add one deliberate "tie" pair where abstaining or hedging is the right answer (F5, F6).
- **The skill's comparison procedure** should itself look at both orders or name each image by content, and it should say "too close to call" when the verdict flips. Write this into the main file; the evals then test it.
- **Style-detection cases always come with near-misses.** For cubism: Blanchard and Marcoussis as positives; Cézanne, Mondrian, Boccioni and Franz Marc as negatives, all CC0 from Cleveland. Do not use Met or AIC cubist works; they are not open access (F4).
- **Fact cases use the SimpleQA three-way grade plus a dispute rubric.** Contested superlatives ("oldest", "most expensive") pass only when the answer names its definition and the competing claims. The gold answers live in RESEARCH.md as `R-` entries from pass F.
- **`aw.py` unit tests stay stdlib-only, with fixtures built in code.** A ~30-line PNG writer/reader (zlib + struct) in `tests/_png.py`. Tests:
  - palette: an exact k-colour image returns k colours with exact hex; a gradient is quantised within tolerance.
  - pixel grid: a sprite scaled by 1–8 with nearest neighbour returns that scale; a non-integer or mixed scale is flagged; offsets are handled.
  - orphans: a pixel matching none of its 8 neighbours is counted.
  - contact sheet: output size is cols × thumb + gutters; the output hash is deterministic.
  - dHash/aHash: an image and its resized or brightened copy are ≤ 4 bits apart; unrelated images are ≥ 20 bits apart.

  If Pillow is used for JPEG input, gate it and skip with a reason when it is absent.
- **CI:** copy the sibling `tests.yml` matrix (ubuntu, macos, windows × 3.9, 3.14), but pin the 3.9 Linux job to `ubuntu-24.04` (F1). Run the `claude plugin eval` cheap tier on Linux or a self-hosted WSL2 runner only, because native Windows cannot sandbox Bash (F2).
- **Fixture budget:** keep committed images to about 15 files of ≤ 200 KB at a long edge of ≤ 1024 px (≈ 2–3 MB in total) and add a size check, in line with the plugin size budget. Synthetic sprites are generated, never committed.
- **Optional `bench/agreement.py`** (not CI): fetch N pairs at run time from a permissively licensed preference set (Rapidata CDLA-P or HPDv3 MIT), commit only their IDs, and log the agreement rate and order-flip rate per model version as a trend. Never gate a release on it. Expect modest agreement (F5).
- **Museum lookups:** if artwright fetches museum records, use Met `/v1.1/search` (v1 is retired, F3) and the Cleveland Open Access API. Treat AIC as possibly challenge-walled.

## Cost: searches 14 · fetches 10 (WebFetch) + about 20 direct API reads via shell · tool calls 37
