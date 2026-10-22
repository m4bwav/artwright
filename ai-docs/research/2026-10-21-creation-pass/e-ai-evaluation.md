# Creation pass 2026-10-21: E. AI evaluation (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation (no `last_checked`). Magnitudes are `n/a (initial)`. Arxiv IDs of the form 26MM.NNNNN are 2026 papers; numbers are quoted from the abstract or HTML pages fetched today unless marked "unverified".

## Findings (newest first)

### F1 · 2026-10-01 · Swapping the order flips up to 60.9% of MLLM judges' pairwise verdicts on image edits
- What: EditJudgeBias (1,196 real editing samples, 13 injected cues that verifiably preserve the edit's quality) audited five MLLM judges. Swapping candidate order reversed up to 60.9% of pairwise decisions. Fabricated "majority opinions" in the prompt pushed ratings up, which is sycophancy under another name. Irrelevant visual elements moved scores more than whole-image changes. The authors measure each shift against the judge's own re-query noise floor, not against zero, and say no single metric captures robustness.
- Track: practice / testing
- Affects: judging procedure (order handling, what context the judge sees), eval cases
- Magnitude: n/a (initial)
- Suggested response: adopt. Always judge pairs in both orders. Never put the user's stated preference, other judges' votes or the generator's name in the judge prompt. Measure the judge's own re-query noise before trusting a difference.
- Sources: https://arxiv.org/abs/2610.01670

### F2 · 2026-08 · Aesthetic and preference scorers mostly reward "fidelity"; the LAION predictor carries a documented gaze
- What: A FAccT 2026 audit of the LAION-Aesthetics Predictor (used to filter LAION-Aesthetics, about 1.2B images) found that it keeps captions that mention women and drops those that mention men or LGBTQ+ people. Across about 330k art images it rates realistic Western and Japanese landscapes, cityscapes and portraits highest. The authors trace the training ratings mainly to English-speaking photographers and Western AI enthusiasts. A second audit (2608.23593) of LAION-Aes, PickScore, ImageReward and HPSv2 found an inverted-U "fidelity preference": any pixel edit away from the original is penalised. It also found that bias audits on synthetic faces can get the direction of a bias wrong.
- Track: subject
- Affects: any claim that an aesthetic score measures "beauty". Optional local scorer.
- Magnitude: n/a (initial)
- Suggested response: note. Present scalar aesthetic scores as "photo-like polish", never as artistic merit, and never use them alone to rank abstract, stylised or deliberately rough work.
- Sources: https://arxiv.org/abs/2601.09896, https://arxiv.org/abs/2608.23593

### F3 · 2026-06-29 · MLLM photo critiques cover every aspect and lack human selectivity; judges prefer them anyway
- What: The study compared eight open MLLMs plus GPT-5.5 against ranked human critiques of 1,227 r/photocritique posts. Reference-similarity metrics barely changed when the image was withheld, so they track length and style, not seeing. All four LLM judges preferred frontier-model critiques to human ones. On identical pairs, 7–8B judges ranged from 9% to 81% preference. Humans and judges rated the substance of model and human critiques as "mostly different" (1.81–2.59 on a 1–5 scale). Models comment on nearly every aesthetic aspect and repeat themselves.
- Track: practice
- Affects: critique output format
- Magnitude: n/a (initial)
- Suggested response: adopt. Critiques must be selective (the top two or three issues, each tied to a visible region) and must not be graded by another LLM's preference alone.
- Sources: https://arxiv.org/abs/2606.29689

### F4 · 2026-06-12 · Cultural ambiguity: MLLM judges compress scales, default to one culture's norm, and reference demos make it worse
- What: VOIR DIRE has 626 image-prompt pairs (food, fashion, architecture) with US and mainland-Chinese annotator pools. Each pool agrees internally (alpha 0.86 and 0.74), but the pools disagree with each other (r = -0.12). Six MLLMs showed a "positivity floor" (rarely giving low scores) and an orientation failure toward one norm. Persona prompting partly fixed calibration. Reference-pool demonstrations strengthened the orientation bias and inflated high scores. Model origin added about 0.10 MAE.
- Track: subject / testing
- Affects: Likert scoring, few-shot anchors, "whose taste" framing
- Magnitude: n/a (initial)
- Suggested response: adopt. Avoid absolute Likert scores as the primary signal. When taste is plural, state whose criteria the verdict applies (the brief, a named tradition, the user's own past picks) and report disagreement instead of averaging it away.
- Sources: https://arxiv.org/abs/2606.20676

### F5 · 2026-06-12 · Reward-model frontier: HPSv3 (2025) and HPSv3++ (2026), UnifiedReward 2.0/Think/Flex on Qwen3-VL and Qwen3.5
- What: HPSv3 (ICCV 2025, released 2025-08-06) is a Qwen2-VL-7B reward model trained on HPDv3 (about 1.08M text-image pairs, 1.17M pairwise comparisons, including real photos and Midjourney). Its code is MIT; the weights licence is not stated. Preference accuracy is 76.9 on HPDv3, against 65.3 for HPSv2, 65.6 for PickScore and 58.6 for ImageReward. HPSv3++ (2606.14657) adds a 212K "dual-dimension" set covering text fidelity and aesthetics, annotated by Qwen-Image under human supervision. It reports +9.8% over HPSv3 on HPDv3 and +5.5% on GenAI-Bench. UnifiedReward (MIT) ships 2B–72B pairwise and pointwise image, video and edit judges on Qwen2.5-VL, Qwen3-VL and Qwen3.5, including a chain-of-thought "Think" variant (2025-11) and a personalised "Flex" variant (2026-03). VisionReward (Apache-2.0 code) uses a 19B CogVLM2 to answer weighted yes/no checklist questions across 60 image dimensions. None of these runs comfortably on a CPU: all are 2B–72B VLMs that want a GPU.
- Track: tooling
- Affects: optional local scorer
- Magnitude: n/a (initial)
- Suggested response: point. Name them as GPU-only options for batch prefiltering; do not bundle them.
- Sources: https://github.com/MizzenAI/HPSv3, https://arxiv.org/abs/2606.14657, https://github.com/CodeGoat24/UnifiedReward, https://github.com/THUDM/VisionReward

### F6 · 2026-05-12 · Visual Aesthetic Benchmark: frontier MLLMs judge beauty far below experts, and order instability is large
- What: VAB has 400 tasks over 1,195 matched-subject images (fine art, photography, illustration). Labels are the consensus of 10 expert judges per task, and the task is to pick the best and the worst image. Pass^3 (correct under all three candidate orderings) for best-and-worst: Claude Sonnet 4.6 26.5 (top), Opus 4.6 20.0, Opus 4.5 20.2, Sonnet 4.5 14.5, Haiku 4.5 12.5, Gemini 3.1 Pro 22.2, GPT-5 21.8. Human experts score 68.9; random is 5.3. Models keep only 34–65% of their single-trial accuracy when they must be right in all three orders. Going from two to four or more candidates degrades models 7.1x, against 2.0x for humans: the best model's best-and-worst pass^3 falls from 47.3% to 6.7%. Greedy decoding helped by 1–2 points. The authors' own human study is the strongest argument for comparisons over scores: score-derived rankings disagreed with the same expert's direct comparison (Kendall tau 0.188), while ranking gave 95.0% vs 52.9% best-image agreement. LoRA on 2,000 expert examples lifted a 35B model to roughly a 397B model's level. Dedicated reward models did no better: Q-Align scored 52.2 Top-1, below the best MLLMs' ~55. The paper is CC BY-NC-ND 4.0; the code repo shows no LICENSE file.
- Track: testing / subject
- Affects: core judging procedure, eval suite, expectations stated to users
- Magnitude: n/a (initial)
- Suggested response: adopt. Compare two images at a time, never four or more at once. Run every pair in both orders. Report "tie / uncertain" instead of forcing a pick. VAB's pass^k protocol is the model for artwright's own consistency check. Do not redistribute VAB data, because of the ND/NC licence.
- Sources: https://arxiv.org/abs/2605.12684, https://arxiv.org/html/2605.12684v1, https://github.com/BakeLab/Visual-Aesthetic-Benchmark

### F7 · 2026-05 · Rubric-first pairwise judging reduces but does not remove position bias; frontier judges still swing ~30 points by order
- What: Auto-Rubric as Reward (2605.08354) has a VLM write prompt-specific rubrics and then judge pairwise against them. The abstract claims reduced positional bias and better results than pairwise reward models and VLM judges. A search summary of the paper reported forward vs reversed accuracy of about 88.7 vs 56.1 for GPT-5 and 91.7 vs 61.5 for Gemini 3.1 Pro, with residual instability after rubrics. Those numbers are not verified on the abstract page. TASTE (2605.20731, CC BY 4.0; 10 professional designers, 9 criteria) found off-the-shelf VLM judges and text-to-image scorers below majority agreement with designers. It applied the both-orders correction, and a small MLP head trained on its labels narrowed the gap.
- Track: practice / testing
- Affects: rubric design
- Magnitude: n/a (initial)
- Suggested response: adopt. Write the rubric from the brief first, score each criterion per image in a pair, then give the overall verdict.
- Sources: https://arxiv.org/abs/2605.08354, https://arxiv.org/abs/2605.20731

### F8 · 2026-01 · Reward hacking with aesthetic and preference scores is documented; plain aesthetic scores prefer artifact images
- What: In text-to-image RL on Janus-Pro, an HPS reward drove oversaturated, vibrant, unrealistic colour and lost object fidelity. All reward setups produced structural artifacts: duplicated limbs, merged bodies. On artifact-vs-clean pairs, the LAION-style Aesthetic Score picked the clean image only 42% of the time and MANIQA 39%, both below chance. HPS scored 53%, ImageReward 68%, UnifiedReward 65%, and a small trained artifact reward 80%. Ensembling rewards only partly helps. A separate ICML 2026 position paper (2512.11883) shows aesthetic reward models penalise deliberately "anti-aesthetic" images that perfectly match the prompt, so these scorers fight briefs that ask for ugly, rough or raw looks.
- Track: practice
- Affects: any automated best-of-N or iterate-until-score loop
- Magnitude: n/a (initial)
- Suggested response: adopt. A separate artifact and anatomy check is needed (VLM checklist: hands, limbs, duplicated objects, text). Never loop generation against a single score. A brief that asks for an unpolished look overrides aesthetic scores.
- Sources: https://arxiv.org/abs/2601.03468, https://arxiv.org/html/2601.03468v2, https://arxiv.org/abs/2512.11883

### F9 · 2026-03 / 2024-09 · Movement and style recognition: VLMs well above chance, unreliable between neighbouring movements
- What: Zero-shot style accuracy on WikiArt (post-1900 subset) was CLIP 24.6%, LLaVA 28.3% and GPT-4o 53.4%. On JenAesthetics it was 36.0%, 37.0% and 54.4%; a fine-tuned CNN reaches 71.2%. Confusions: Baroque/Rococo/Classicism/Romanticism; Impressionism/Post-Impressionism/Expressionism; Colour Field/Abstract Expressionism/Minimalism. CLIP collapses Cubism into "Analytic Cubism". GPT-4o labels all of Manet Impressionist, ignoring his Realist phase, which points to artist-name priors. Giving LLaVA the author and year raised accuracy from 37% to 55%, which is prior knowledge rather than seeing. A 2026 interpretability study (2603.11024) found art historians judged 73% of VLM style concepts coherent and 90% of the predictive ones relevant. Some predictions lean on formal cues such as light/dark contrast rather than historians' criteria. No paper found frames "contains cubism" as multi-label influence detection; the only multi-label work is retrieval-oriented (MMArt 2608.10706, CANVAS 2607.16321, WeART 152 styles 2601.17697). Frontier 2026 models were not re-tested on style in anything found.
- Track: subject
- Affects: the "does this contain cubism" procedure
- Magnitude: n/a (initial)
- Suggested response: adopt. Answer movement questions as evidence-graded feature checks: for Cubism, faceted planes, multiple viewpoints, a flattened picture plane, a muted palette (analytic) or collage (synthetic). Use a three-way verdict (member / influenced by / no evidence) plus the neighbouring movements considered. Never take an artist or title in the filename as evidence; strip filenames.
- Sources: https://arxiv.org/html/2409.03521v2, https://arxiv.org/abs/2603.11024, http://export.arxiv.org/api/query (art-style listing)

### F10 · current docs · Claude image cost: ceil(w/28) x ceil(h/28) visual tokens, 2576 px / 4784 tokens on 4.7+ models
- What: Claude counts images in 28x28-pixel patches, so cost = ceil(width/28) x ceil(height/28) visual tokens. Claude 4.7 and later (including Opus 5.5) take a long edge of up to 2576 px and 4784 tokens; older models take 1568 px and 1568 tokens. Larger images are downscaled. Examples: 1000x1000 = 1296 tokens; 1920x1080 = 2691 (high-res) or 1560 (standard). At Opus 5.5's $4 per million input tokens, a 1000x1000 image costs about $5.18 per thousand. Limits: 8000x8000 px per image, 10 MB base64 per image on the API, 32 MB per request, and up to 600 images per request (100 on 200k-context models). Above 20 images per request a stricter per-image limit applies, so keep each image at 2000 px or less. claude.ai takes 20 images per message. Claude reads no metadata, is weaker below 200 px, and cannot tell whether an image is AI-generated. The docs advise putting images before text and labelling each one ("Image 1:"). Animation frames after the first are ignored.
- Track: tooling
- Affects: cost estimates, contact-sheet design, batch sizes
- Magnitude: n/a (initial)
- Suggested response: adopt. Downscale judge inputs to about 1024 px on the long edge (about 1300 tokens) by default and use full resolution only for detail checks. Two labelled separate images beat one side-by-side composite for pairwise judging (F11).
- Sources: https://platform.claude.com/docs/en/build-with-claude/vision

### F11 · 2025–2026 · Contact sheets: evidence is mixed; composites hurt fine-grained comparison
- What: No study tests pairwise aesthetic judging on a grid versus separate images. Adjacent evidence: a composite image cost GPT models about 4 points on 11Plus-Bench spatial reasoning (2508.20068). OddGridBench (2603.09326) shows MLLMs far below humans at spotting fine differences within grids. Frame grids helped video QA (2403.18406). VAB shows accuracy collapsing as candidate count rises (F6).
- Track: testing
- Affects: batch ranking design
- Magnitude: n/a (initial)
- Suggested response: adopt. Use contact sheets only for coarse triage (reject obvious failures, cluster near-duplicates). Final ranking runs on pairwise matches of separate, labelled images.
- Sources: https://arxiv.org/pdf/2508.20068, https://arxiv.org/abs/2603.09326, https://arxiv.org/pdf/2403.18406

### F12 · 2024–2025 · Foundational judge results still hold: pairwise beats scoring; visual tricks inflate scores; sycophancy carries over to vision
- What: MLLM-as-a-Judge (2402.04788) found MLLMs human-like in pair comparison but diverging from humans in scoring and batch ranking. FRAME (2505.15249, EMNLP 2025): all tested LVLM judges inflate scores for visually manipulated images, stacking manipulations makes it worse, pairwise judging is also vulnerable, and prompt-based mitigation did not remove it. PENDULUM (2512.19350) shows GPT-5 and Gemini 2.5 Pro adopting a user's wrong count when it is hinted in the prompt. Moral-sycophancy work (2602.08311) shows VLMs revising image judgements when the user pushes back.
- Track: subject / testing
- Affects: prompt hygiene, rubric, abstention
- Magnitude: n/a (initial)
- Suggested response: adopt. Judge prompts carry the brief and rubric only; the user's guess comes after the blind verdict, if at all.
- Sources: https://arxiv.org/abs/2402.04788, https://arxiv.org/abs/2505.15249, https://arxiv.org/abs/2512.19350, https://arxiv.org/html/2602.08311

### F13 · 2025-06 · Practitioner pattern: pairwise matches turned into Elo (Simon Willison's pelicans)
- What: Simon Willison ranked 34 pelican-on-bicycle images by running every pairing (560 matches) through gpt-4.1-mini with a JSON schema `{left_or_right, rationale}`. He turned the results into Elo starting at 1500 (top 1769.9, bottom 1196.2). Each pair was judged once in one order, which is the very flaw F1 and F6 quantify.
- Track: practice
- Affects: batch ranking procedure
- Magnitude: n/a (initial)
- Suggested response: adopt the shape (pairwise, schema output, rating aggregation) and fix the flaw: both orders, ties allowed, Bradley-Terry instead of sequential Elo, which depends on match order.
- Sources: https://simonwillison.net/2025/Jun/6/six-months-in-llms/

### F14 · 2024–2026 · Prompt or brief adherence: decompose into checkable questions
- What: VQAScore (P("yes") to "Does this image show {prompt}?") and GenAI-Bench (1,600 compositional prompts, scored by pairwise accuracy against humans) beat CLIPScore on composition. DSG and TIFA-style question decomposition and VisionReward's weighted yes/no checklist are the same idea. A 2026 rubric paper (DeltaRubric 2605.09269) reports large VL-RewardBench gains from plan-a-checklist-then-verify. No source found says GenEval or T2I-CompBench are the right tool for a single production brief; they are model-level benchmarks.
- Track: subject / testing
- Affects: "does this render fit the scene brief" procedure
- Magnitude: n/a (initial)
- Suggested response: adopt. Split the brief into atomic yes/no checks (subjects, count, attributes, relations, camera, lighting, style, mood, forbidden items). The judge answers each with visible evidence, and fit = weighted pass rate, with hard-fail items listed separately.
- Sources: https://arxiv.org/abs/2404.01291v1, https://arxiv.org/abs/2605.09269, https://github.com/THUDM/VisionReward

### F15 · Classic scorers: licences and footprints
- What: The LAION improved aesthetic predictor (CLIP ViT-L/14 embedding + MLP; trained on SAC + LAION-Logos + AVA ratings) is Apache-2.0. It is CPU-feasible because only CLIP-L inference is needed (~430M params; inferred, not stated). aesthetic-predictor-v2.5 (SigLIP backbone, 1–10 scale, "5.5+ is great") is AGPL-3.0, so avoid bundling it. PickScore v1 (CLIP-H fine-tune, ~1.0B params, Pick-a-Pic) has no licence on its model card. ImageReward (137k expert comparisons) has Apache-2.0 code and an unstated weights licence. Q-Align / OneAlign (mPLUG-Owl2-based, about 7–8B; AVA for aesthetics) has S-Lab licence files; Q-ReAlign moved to Qwen3.5 backbones. Q-Insight (GRPO-trained, 2025) adds reasoning about quality. NIMA, MPS, AesBench, UNIAA, AesExpert and ArtiMuse were not re-verified in this pass, except ArtiMuse's VAB score (44.2 Top-1).
- Track: tooling
- Affects: optional extra
- Magnitude: n/a (initial)
- Suggested response: point. If an optional local scorer ships at all, make it the Apache-2.0 LAION predictor as a cheap prefilter, labelled "photo-polish score".
- Sources: https://github.com/christophschuhmann/improved-aesthetic-predictor, https://github.com/discus0434/aesthetic-predictor-v2-5, https://huggingface.co/yuvalkirstain/PickScore_v1, https://github.com/THUDM/ImageReward, https://github.com/Q-Future/Q-Align, https://arxiv.org/abs/2503.22679

### F16 · Datasets: WikiArt is research-only; VAB is no-derivatives
- What: The HF `huggan/wikiart` card lists the licence as "unknown". It says the data "can be used only for non-commercial research purpose" under WikiArt.org's terms, and many images are in-copyright modern works. ArtBench-10 (60k images, 10 styles, 5,000 train and 1,000 test each, 32/256/original sizes) links a LICENSE whose terms were not stated on the page. Its WikiArt origin is from memory (unverified). VAB is CC BY-NC-ND 4.0, TASTE is CC BY 4.0, and PAMELA (2604.07427: 70k ratings, 15 raters per image, Flux 2 and Nano Banana images) was not checked.
- Track: testing
- Affects: eval fixtures in a public repo
- Magnitude: n/a (initial)
- Suggested response: adopt. A public repo bundles no WikiArt or VAB images. Use public-domain museum images (e.g. open-access collections) or self-generated renders for eval fixtures, and link benchmarks instead of copying them.
- Sources: https://huggingface.co/datasets/huggan/wikiart, https://github.com/liaopeiyuan/artbench, https://arxiv.org/abs/2605.20731

### F17 · Tooling track is quiet: no agent skill or plugin for image judging found
- What: A GitHub/skills search for SKILL.md image-judging, aesthetic-critique or generation-ranking skills found only skill-reviewing skills. A GitHub repo search for ComfyUI aesthetic or reward nodes updated recently found nothing relevant. This is the baseline: artwright's judging procedure would be first of its kind among published skills, as far as this pass could see.
- Track: tooling
- Affects: none
- Magnitude: n/a (initial)
- Suggested response: note
- Sources: GitHub search API (repositories, "comfyui aesthetic score OR reward node"), web search for SKILL.md image judge

## Overall magnitude: n/a (initial)

## Open questions:
- new: Position bias figures for Claude Opus 5.5 specifically. VAB tested Claude up to 4.6 and gave no per-model order-flip rate. Measure it in artwright's own eval.
- new: Whether thinking before the verdict helps aesthetic pairwise accuracy. VAB did not test it; UnifiedReward-Think claims gains for its own models only.
- new: Grid versus separate images for pairwise aesthetic judging. No direct study exists.
- new: Licence of HPSv3 and PickScore weights (not stated on their pages).
- new: The forward/reversed accuracy numbers attributed to 2605.08354 need checking against its full text.
- still open: Any benchmark of frontier VLMs on multi-label "influence" detection for art movements.

## Search plan notes:
- Subject: arXiv API listing queries (`export.arxiv.org/api/query`, sorted by submittedDate) were the best value. One fetch returned 30 dated abstracts. Good strings: `aesthetic AND "reward model" AND image`; `MLLM AND judge AND image AND bias`; `(art style OR art movement OR WikiArt) AND (VLM OR CLIP)`; `aesthetic AND MLLM AND (benchmark OR critique)`. Abstract pages often omit numbers; the arxiv.org/html/ version has the tables.
- Tooling: GitHub READMEs give licence and backbone. HF model cards are often empty (PickScore). Web search for SKILL.md image judges was noise (skill-reviewers).
- Practice: Simon Willison's pelican post is the one practitioner write-up found. Blog and HN searches for VLM best-of-N lessons returned papers, not postmortems.
- Testing: VAB's pass^3 protocol, TASTE's both-orders correction, and EditJudgeBias's noise-floor method are the reusable harness ideas.
- Not covered: NIMA, MPS, AesBench, UNIAA, AesExpert, ImagenHub, VisionArena and Multimodal RewardBench details were not fetched, to save budget. They are listed from memory as older background (2023–2024), none re-verified.

## Tracks covered: subject: 7 queries (incl. 4 arXiv listing queries) · tooling: 4 · practice: 4 · testing: 5

## Upcoming events: none dated found

## Nothing changed: no (creation pass)

## Proposals for artwright
- **Pairwise is the unit of judgement.** Every "which is better" or ranking question runs as two-image matches. Each pair is judged in both orders, A|B and B|A, in separate calls with fresh context. The images are labelled "Image 1:" and "Image 2:", placed before the text, with filenames stripped. A verdict counts only if both orders agree; disagreement becomes a tie. Never compare more than two in one call (VAB: 7x degradation at four or more).
- **Rubric first, verdict last.** The judge first writes 3–6 criteria from the brief (Auto-Rubric pattern), then a short per-criterion note for each image tied to a visible region, then an overall verdict, `{winner: 1|2|tie, confidence: low|med|high, decisive_criteria: [...]}`. Default rubric, scored per image: **Brief fit** (atomic yes/no checks, hard fails listed); **Composition** (focal point, balance, framing, eye path); **Colour and light** (harmony, value structure, consistency of light); **Rendering integrity** (anatomy, hands, duplicated or merged objects, text, seams; a hard gate, not a taste call); **Style coherence** (one consistent style, matches the requested reference or movement); **Expressive intent** (mood and story match the brief, including deliberately rough or "ugly" asks).
- **Abstain rules.** Return "tie / no confident preference" when the two orders disagree, when both images fail the same hard gate, or when the judge's own confidence is low on every decisive criterion. On a hard-to-call pair, a third run at temperature 0 can break the tie only if it agrees with one of the earlier verdicts. Otherwise the result stays a tie, flagged for a human.
- **Blind prompts.** The judge never sees the user's guess, the generator or model name, the seed, prior votes or the file name (F1, F12 sycophancy, F9 name priors). Show the user's own preference only after the blind verdict, as a comparison.
- **Batches: triage, then a tournament, then Bradley–Terry.** Use a contact sheet (≤ 16 thumbnails at about 256 px) only to discard obvious failures and near-duplicates. Survivors get a Swiss or round-robin pairwise schedule, about N·log N matches with both orders. Fit Bradley–Terry with ties (deterministic, independent of match order, unlike sequential Elo). Report the top pick with its win margin and flag any pick whose interval overlaps the runner-up.
- **Movement questions ("contains cubism?").** Return `member | influenced | no_evidence` plus listed formal features seen or absent and the neighbouring movements considered (e.g. Futurism, Orphism, Precisionism). Never just yes/no, and never trust title or artist cues.
- **Absolute scores only as a secondary signal.** If a 1–10 is asked for, anchor it with 3 labelled reference images from the same domain. Warn that scales compress at the top (F4 positivity floor), and do not compare scores across sessions without the same anchors.
- **Image prep.** Downscale to 1024 px on the long edge (~1300 tokens on Opus 5.5; ~$5 per thousand images per call side) for judging. Use full 2576 px only for the rendering-integrity check on finalists. Each pairwise match in both orders costs about 4 image inputs, so a 16-image round robin (120 pairs × 2 orders) is ~624k image tokens, roughly $2.50 on Opus 5.5. Prefer Swiss pairing or triage for bigger batches.
- **Verdict cache.** Store one JSONL record per call in the project, keyed by `sha256(image bytes after resize)` for each side, the order, the rubric hash, the model id and the prompt version: `{"a":"<sha>","b":"<sha>","order":"ab","rubric":"<sha>","model":"...","prompt_v":"1","winner":"a|b|tie","confidence":"low|med|high","criteria":{...},"ts":"..."}`. A cache hit skips the call. A rubric or model change invalidates the entry. The JSONL doubles as the calibration log.
- **Calibration set.** Ship a small eval set of 30–50 self-generated or public-domain pairs labelled by the owner, never WikiArt or VAB images (licences). Measure both-orders agreement rate (target ≥ 0.8), pairwise accuracy vs the human labels, Cohen's kappa, and the judge's re-query noise floor. Recompute these whenever the model changes.
- **Optional local scorer: probably skip in v1.** If added, use only the Apache-2.0 LAION improved aesthetic predictor (CLIP ViT-L/14 + MLP, CPU-feasible, roughly 1 GB download with CLIP) as a prefilter labelled "photo-polish". Never use it as the ranking judge (it picks artifact images over clean ones 58% of the time; F8) and never against stylised or anti-aesthetic briefs. GPU reward models (HPSv3 7B, UnifiedReward 2B–32B) belong in docs as pointers, not dependencies. Avoid aesthetic-predictor-v2.5 (AGPL-3.0).

## Cost: searches 9 · fetches 37 · tool calls 49
