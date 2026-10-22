# Creation pass 2026-10-21: D. AI generation (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation (no last_checked). Magnitudes are `n/a (initial)`. Not legal advice: legal findings report what the cited sources say, with their dates.

## Findings (newest first)

### F1 · 2026-10-21 · Veo 3.1 prompt guide: element list, camera vocabulary, and "no negation words" in negative prompts
- What: Google's Vertex AI Veo prompt guide (page "last updated 2026-10-21", Veo 3.1 the only Veo model listed) breaks a video prompt into subject, action, scene/context, camera angle, camera movement, lens and optical effects, visual style (lighting, mood, artistic style), temporal elements, audio, cinematic terms; not every prompt needs all of them. It gives a controlled vocabulary: angles (eye-level, low, high, bird's-eye, worm's-eye, Dutch, close-up through establishing, over-the-shoulder, POV), moves (static, pan, tilt, dolly, truck, pedestal, zoom, crane, aerial, handheld, whip pan, arc; zoom changes focal length, dolly moves the camera), optics (wide, telephoto, shallow/deep DOF, flare, rack focus, fisheye, dolly zoom). The negative prompt field should list the unwanted things ("wall, frame"), not instructions such as "no" or "don't". Audio goes in separate sentences; dialogue is attributed to a described character.
- Track: subject
- Affects: style-vocabulary file (camera and lens section); prompt-revision rules for video
- Magnitude: n/a (initial)
- Sources: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide

### F2 · 2026-10-10 · The owner's local video model, MiniMax H3, is open-weights (2026-08-03) and takes shot lists, labelled references and audio direction
- What: Comfy's day-0 post (2026-08-03) says MiniMax H3 shipped with open weights, up to 2K and 15 s per clip, native stereo audio in the same pass, four modes (text-to-video, image-to-video, first-and-last-frame, reference-to-video), and runs locally with offloading; the post gives no licence, text encoder, CFG or negative-prompt settings. fal's guide (2026-07-31) gives the working rules: prompts up to 7,000 characters; "Give every reference an explicit job, write timed shot lists, and direct the sound as deliberately as the picture"; reference-to-video takes up to 9 images, 3 video clips and 3 audio clips; first-and-last-frame only when the image literally is the first or last frame; describe transitions as physical events, not effect names; name what must stay fixed. Unlike Veo, in-prompt negative direction is "unusually effective" ("No soft dissolves or fluid morphs", "Do not introduce Chinese text, garbled characters, or misspellings"). A 2026-10-10 news roundup shows a community ecosystem forming around H3 (FastH3 Trim 8-step int8 build for 8 GB, sparse-attention node, person-remover LoRA).
- Track: subject / practice
- Affects: hand-off contract with comfyui-gen and cinewright (shot-list format, reference roles); negation rule must be per model
- Magnitude: n/a (initial)
- Suggested response: adopt (shot-list and reference-role template for H3 prompts)
- Sources: https://blog.comfy.org/minimax-h3-day-0-support-in-comfyui/, https://fal.ai/learn/devs/minimax-h3-prompting-guide, https://www.kombitz.com/2026/10/10/ai-image-video-model-news-roundup-october-10-2026/

### F3 · 2026-10 · Open image model landscape: Z-Image, FLUX.2 (dev and klein), Qwen-Image 2.x, HiDream-O1 and others; LLM text encoders are now the norm
- What: Z-Image-Turbo (Tongyi-MAI, papers dated Nov 2025) is a 6B single-stream DiT, Apache-2.0, distilled to 8 forward passes, and its card says "Guidance should be 0 for the Turbo models" (CFG unsupported), so negative prompts do nothing on Turbo; the non-distilled Z-Image base (50 steps, CFG) supports "effective negative prompting"; Z-Image-Edit and Omni-Base were still listed "to be released" on the card. ComfyUI's Z-Image setup uses a Qwen3-4B text encoder. FLUX.2 [dev] is a 32B guidance-distilled rectified-flow transformer (example guidance 4, 28 to 50 steps) under a non-commercial weights licence, with multi-reference editing; FLUX.2 [klein] 4B/9B (Jan 2026, Apache-2.0, 4 steps, CFG off) is the small local option. Qwen-Image (original) is Apache-2.0 with true CFG (example `true_cfg_scale=4.0`, a blank negative prompt) and a "positive magic" suffix (", Ultra HD, 4K, cinematic composition."); secondary sources report Qwen-Image 2.1 (Sep 2026) and 2.1-Turbo (Oct 2026: 8 steps, CFG 1, RGBA, 2K) under a licence that needs a separate agreement for commercial use. A local-model guide (dated 6 Oct 2026, but claiming a "last updated 30 October 2026", which is after today, so it is treated as unreliable) also lists HiDream-O1-Image 8B (MIT, pixel-space), Iris-3B and 1-bit "Bonsai" models. The common thread: modern open models read prose through LLM encoders (Qwen3, Mistral-class, umT5 for Wan), not CLIP tag soup with the 77-token limit; prompt weighting like `(word:1.3)` and tag lists are SD1.5/SDXL habits.
- Track: subject
- Affects: per-model prompt profiles; the claim "use negative prompts" must be conditional on CFG > 1
- Magnitude: n/a (initial)
- Sources: https://huggingface.co/Tongyi-MAI/Z-Image-Turbo, https://huggingface.co/black-forest-labs/FLUX.2-dev, https://huggingface.co/Qwen/Qwen-Image, https://docs.comfy.org/tutorials/image/z-image/z-image-turbo, https://local-ai-zone.github.io/blog/local-image-generation-2026.html, https://www.kombitz.com/2026/10/10/ai-image-video-model-news-roundup-october-10-2026/

### F4 · 2026 (undated page) · FLUX.2 prompting guide: word order, prose over keywords, no negative prompts, hex colours, camera and film stock names
- What: Black Forest Labs' guide says to prompt Subject, Action, Style, Context, with the priority order "Main subject → Key action → Critical style → Essential context → Secondary details" because earlier words weigh more; 30 to 80 words is usually ideal. "FLUX.2 does not support negative prompts": state the positive ("sharp focus throughout", not "no blur"). Structured JSON (scene, subjects, style, color_palette, lighting, camera) suits automation and multi-subject scenes; the model reads JSON and prose equally. Hex codes work when tied to a named object. Specific cameras, lenses, film stocks and eras ("Kodak Portra 400", "2000s digicam style") give more authentic photographs than "professional photo". Multi-reference: say what each image contributes (up to 8 at 1MP on [pro]). Text: quote it, place it, style it.
- Track: subject / practice
- Affects: prompt-construction template; the "describe the positive" rewrite rule
- Magnitude: n/a (initial)
- Suggested response: adopt (JSON brief as the hand-off format; positive rephrasing rule)
- Sources: https://docs.bfl.ai/guides/prompting_guide_flux2

### F5 · 2026-09-28 · Andersen v. Stability AI: still in discovery; schedule pushed again; summary judgment not before late 2027
- What: The artists' class action (Stability AI, Midjourney, DeviantArt, Runway; N.D. Cal., Judge Orrick) has had no merits ruling since the August 2024 order that let core claims proceed. A February 2026 order moved the summary-judgment hearing from 4 Nov 2026 to 17 Feb 2027; on 28 Sep 2026 the schedule was extended another three months, and the tracker says summary judgment "won't get resolved until the end of 2027 at the earliest". March 2026: the magistrate ordered Stability's enterprise-customer list produced as relevant to fair use. Nothing yet decides whether style imitation or training infringes.
- Track: subject
- Affects: ethics/law reference file (status line with date)
- Magnitude: n/a (initial)
- Sources: https://chatgptiseatingtheworld.com/category/andersen-v-stability-ai/, https://chatgptiseatingtheworld.com/2026/02/03/sarah-andersens-copyright-lawsuit-the-1st-filed-v-ai-companies-gets-pushed-back-again-at-her-request/

### F6 · 2026-08-03 (on guidelines of 2026-07-20) · EU AI Act Article 50 transparency applies from 2 Aug 2026; artistic deepfakes get a lighter regime, not an exemption
- What: Per Stephenson Harwood's summary of the Commission's Article 50 guidelines (published 20 July 2026): providers of generative systems must mark image, audio and video outputs in a machine-readable way (Art. 50(2)); systems already on the EU market before 2 Aug 2026 have until 2 Dec 2026 (a Digital Omnibus transitional window). Deployers must give deepfakes a "clear and distinguishable label" at first exposure (Art. 50(4)); deepfake means content resembling existing persons, objects, places or events that would falsely appear authentic. Evidently artistic, creative, satirical or fictional works get a lighter disclosure regime, read strictly. A voluntary Code of Practice on marking and labelling was reported final around 10 June 2026. Sources conflict on how far the Digital Omnibus postpones other parts; check the Official Journal before quoting.
- Track: subject
- Affects: ethics/law file; a "label if photoreal and depicts a real person or place" rule in the judge output
- Magnitude: n/a (initial)
- Sources: https://www.stephensonharwood.com/post/102nfqh/eu-ai-act-update-european-commission-adopts-guidelines-on-article-50-transparency-obligations/, https://emerging-europe.com/europes-ai-labelling-rules-arrive/, https://jonesday.com/en/insights/2026/01/european-commission-publishes-draft-code-of-practice-on-ai-labelling-and-transparency

### F7 · 2026-05-12 · Visual Aesthetic Benchmark: frontier models judge beauty far worse than experts; compare sets, do not score singly
- What: VAB (arXiv 2605.12684) has 400 set-based tasks, 1,195 images across fine art, photography and illustration, labelled by 10 experts each. The best of 20 frontier MLLMs and 6 reward models picked both the best and worst image correctly (stable across three orderings) in 26.5% of tasks, against 68.9% for human experts. In an annotator study, scalar scores ranked poorly against the same people's direct comparisons; direct ranking gave much higher agreement. Fine-tuning a 35B model on 2,000 expert comparisons closed much of the gap.
- Track: testing
- Affects: the judge procedure (pairwise or best/worst selection over candidates, not 1 to 10 scores); evals that check the judge's choices
- Magnitude: n/a (initial)
- Suggested response: adopt (judge by comparing candidates; randomise order and re-ask; never present a single absolute aesthetic score as fact)
- Sources: https://arxiv.org/abs/2605.12684

### F8 · 2026-01-21 · Iterative VLM-critic refinement beats compute-matched parallel sampling
- What: "Iterative Refinement Improves Compositional Image Generation" (Jaiswal, Prabhudesai, ..., Fragkiadaki, Pathak; arXiv 2601.15286) runs a training-free VLM critic in a loop with a generator or editor, issuing targeted corrections. Against parallel sampling at equal compute: +16.9% all-correct on ConceptMix (k=7), +13.8% on T2I-CompBench 3D-spatial, humans preferred it 58.7% vs 41.3%. Lineage: Idea2Img (Yang et al., ECCV 2024, arXiv 2310.08541) had GPT-4V revise prompts, pick drafts and reflect, keeping a memory of the target model's quirks; later loops include LumiGen (2508.04732), PromptSculptor (2509.12446) and a safety-focused refiner (2509.13760); IntroSVG (2603.09312) shows the generate-critique-refine loop also helps general models zero-shot.
- Track: practice / testing
- Affects: the prompt-critique procedure (loop with a stop rule; per-model memory of quirks)
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://arxiv.org/abs/2601.15286, https://arxiv.org/abs/2310.08541, https://arxiv.org/html/2509.12446v1, https://arxiv.org/pdf/2603.09312

### F9 · 2026 (CVPR) · The "AI look" has a measured cause: preference mode collapse under reward tuning
- What: D²-Align (arXiv 2512.24146, CVPR 2026) names "Preference Mode Collapse": reward-tuned diffusion models converge on narrow high-scoring outputs, "monolithic styles or pervasive overexposure", by over-optimising the reward model's biases; it adds DivGenBench to measure it. TMPO (arXiv 2605.10983) makes the same diagnosis. Earlier: reward-diversity trade-off (arXiv 2409.06493). This supports treating glow, overexposure, oversmooth skin, saturated teal-orange and centred hero framing as model defaults to steer against rather than as chance.
- Track: subject
- Affects: the "AI look" checklist in the judge; rationale section
- Magnitude: n/a (initial)
- Sources: https://arxiv.org/abs/2512.24146v1, https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Taming_Preference_Mode_Collapse_via_Directional_Decoupling_Alignment_in_Diffusion_CVPR_2026_paper.html, https://www.alphaxiv.org/abs/2605.10983

### F10 · 2026-03-02 · Thaler cert denied; human authorship rule stands; Allen v. Perlmutter (600+ Midjourney prompts) still pending
- What: The US Supreme Court denied certiorari in Thaler v. Perlmutter on 2 Mar 2026, leaving the D.C. Circuit's March 2025 human-authorship holding in place; the D.C. Circuit expressly did not decide how much human direction suffices. Allen v. Perlmutter (D. Colo., 1:24-cv-02665) tests whether 600+ iterated prompts plus Photoshop work make an image registrable; the Copyright Office moved for summary judgment; no ruling found. The Office's AI report page lists Part 2 Copyrightability (29 Jan 2025: prompts alone do not give sufficient control; human selection, arrangement and modification can be protected) and Part 3 Training as a pre-publication version (9 May 2025), final version still "later", with no 2026 entries.
- Track: subject
- Affects: ethics/law file; artwright advice on keeping a record of human edits and selection
- Magnitude: n/a (initial)
- Sources: https://www.scotusblog.com/cases/thaler-v-perlmutter/, https://www.bakerdonelson.com/supreme-court-denies-certiorari-in-thaler-v-perlmutter-ai-cannot-be-an-author-under-the-copyright-act, https://www.copyright.gov/ai/

### F11 · 2026-01 · Getty v. Stability (UK): Getty largely lost at first instance (4 Nov 2025) and has permission to appeal the secondary-infringement point
- What: The High Court (Joanna Smith J) ruled mostly for Stability: the secondary copyright claim failed (the model was not an "infringing copy"); trade mark claims succeeded only in part, on older model versions. In December 2025 the judge granted Getty permission to appeal the secondary-infringement ruling and refused Stability permission on trade marks. The appeal's key question is whether a model must store a copy of a work to be an infringing copy. No Court of Appeal hearing date or ruling was found as of this pass.
- Track: subject
- Affects: ethics/law file
- Magnitude: n/a (initial)
- Sources: https://ipkitten.blogspot.com/2026/01/permission-to-appeal-granted-in-getty.html, https://www.burges-salmon.com/articles/102lydc/getty-images-v-stability-ai-getty-granted-permission-to-appeal

### F12 · 2026-01-16/17 · Steam's AI disclosure narrowed to player-facing content
- What: Valve rewrote its rules in January 2026: disclosure covers AI-generated content players consume (pre-generated assets, and live-generated content with a description of guardrails); coding assistants and behind-the-scenes tools are exempt. Disclosures show under "About This Game"; the Content Survey has an AI section; live-generated adult sexual content is prohibited. Sources are secondary; the primary text is the Steamworks post.
- Track: subject
- Affects: ethics/law file (platform policies); hand-off note for game assets
- Magnitude: n/a (initial)
- Sources: https://tbreak.com/steam-ai-disclosure-policy-update-developers/, https://www.videogameschronicle.com/news/steam-pages-will-now-disclose-which-games-use-ai-generated-content/

### F13 · 2026-02-09 · Closest existing tool: a Midjourney critic skill with a 7-dimension rubric and evidence-backed pattern memory
- What: JustinPerea/midjourney-cc-skill (MIT, 16 stars, created 2026-02-06, last push 2026-02-09, 0 issues) makes the model the "visual critic, gap analyzer, and prompt rewriter". It scores every iteration on seven dimensions: subject, lighting, color, mood, composition, material, spatial ("All 7 always scored (1.0 for 'not applicable')"), treats scores as preliminary until the user validates them, and stores sessions, iterations and patterns in SQLite plus files (failure-modes, learned-patterns, keyword-effectiveness) with confidence levels and graduation/decay; "every pattern must have logged evidence". Midjourney-only, browser automation, no evals found, low use. Other registry skills found (claude-office-skills image-generation, wells1137 image-studio, danielmiessler "art", g1joshi midjourney) are prompt writers or generators, not critics; none ties critique to ComfyUI. Tooling is thin: artwright has no strong incumbent.
- Track: tooling
- Affects: rubric dimensions; per-model keyword-effectiveness file
- Magnitude: n/a (initial)
- Suggested response: point (borrow the rubric and the evidence-required pattern memory; do not depend on it)
- Sources: https://api.github.com/repos/JustinPerea/midjourney-cc-skill, https://raw.githubusercontent.com/JustinPerea/midjourney-cc-skill/main/SKILL.md, https://skills.cat/u/JustinPerea

### F14 · 2026 (Aug-Oct) · Closed models: Midjourney V8 alpha, Nano Banana 2 and Pro, Seedream 5.0 Pro, GPT-Image-2, Veo 3.1
- What: Only secondary sources were reachable (Midjourney's docs returned 403). They describe Midjourney V8 in alpha (V8.1 personalization, HD mode, 2K max), still judged strongest on colour and mood; Nano Banana Pro/2 (Gemini image) strongest on realism, text and conversational editing, with Google's "golden rule" to describe scenes in natural sentences rather than keyword stacks and to say what changes and what stays when editing; Seedream 5.0 Pro (ByteDance) for cinematic realism and region edits; GPT-Image-2 named without details. OpenAI's image tool has refused "the style of a living artist" since March 2025 while allowing studio styles, and suggests describing the style instead.
- Track: subject
- Affects: per-model profiles (closed models get a short "verify" profile)
- Magnitude: n/a (initial)
- Sources: https://framia.converge.ai/blog/midjourney-v8-review/, https://invideo.io/faq/seedream-50-pro-vs-midjourney-vs-gpt-image-2-which-ai/, https://en.kocpc.com.tw/?p=14441, https://the-decoder.com/openai-blocks-artist-names-in-image-prompts-but-allows-studio-styles/, https://tech.yahoo.com/articles/openai-just-made-harder-turn-092240391.html

### F15 · 2025-12 · Control for the owner's main image model: Z-Image-Turbo Fun ControlNet Union
- What: Alibaba PAI released Z-Image-Turbo-Fun-Controlnet-Union (2 Dec 2025) with canny, HED, depth, pose and MLSD in one patch, officially supported in ComfyUI (model_patches folder). FLUX.2 and Qwen-Image-Edit/Nano Banana-style models replace much IP-Adapter use with native multi-reference conditioning (say which image supplies what). LoRA-plus-ControlNet compatibility for Z-Image was not confirmed.
- Track: tooling
- Affects: "what to change" vocabulary: when a judge finds composition or pose wrong, the fix is often control (depth/pose) not words
- Magnitude: n/a (initial)
- Suggested response: point
- Sources: https://comfyui-wiki.com/en/news/2025-12-02-z-image-turbo-controlnet-union, https://docs.comfy.org/tutorials/image/z-image/z-image-turbo

### F16 · 2025-07-18 · Artist names are recognisable in outputs; the US Copyright Office notes living-artist style guardrails
- What: Su et al. (arXiv 2507.18633) built a 1.95M-image benchmark over 110 artists across SD1.5, SDXL, PixArt-Σ and Midjourney and show the prompted artist can often be identified from the image (harder for held-out artists and multi-artist prompts). Earlier CLIP studies (2202.13562, 2410.09566) find CLIP aligns artist names with their paintings; Somepalli et al. (2404.01292) measure style similarity and attribute generated styles to training images. USCO Part 3 (pre-publication, May 2025, p. 60) lists industry guardrails including "internal system prompts that instruct it not to ... create images in the style of living artists", and (p. 65) says outputs stylistically similar to training works can cause market dilution even though copyright does not protect style as such.
- Track: subject
- Affects: living-artist rule; vocabulary file (movements, media and techniques preferred over names)
- Magnitude: n/a (initial)
- Sources: https://arxiv.org/abs/2507.18633v1, https://arxiv.org/abs/2404.01292, https://arxiv.org/pdf/2202.13562, https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf

### F17 · 2025-08 / 2025-01 · MLLM art critique hallucinates unless grounded in visible evidence
- What: Jiang and Chen (arXiv 2501.09012, ACM MM 2025) find MLLMs hallucinate subjective, unsupported interpretations in aesthetic reasoning; an evidence-based, objective reasoning prompt (ArtCoT) aligns significantly better with human judgment. A 2026 photo-critique study (alphaXiv 2606.29689) warns that word overlap with reference critiques is a poor score for critique quality. AesBiasBench (2509.11620, EMNLP 2025) documents bias in personalised aesthetic judgments.
- Track: testing / practice
- Affects: judge output format (each claim tied to a visible region or feature); eval grading (do not grade critiques by keyword overlap)
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://arxiv.org/abs/2501.09012, https://www.alphaxiv.org/abs/2606.29689.md, https://arxiv.org/abs/2509.11620v1

### F18 · 2025-07 · Glaze and Nightshade can be stripped (LightShed); protections are not a guarantee
- What: LightShed (Foerster et al., USENIX Security 2025) detects Nightshade-poisoned images with 99.98% TPR and removes Glaze/Nightshade perturbations, weaker on unseen poisons (MetaCloak) or light perturbation; authors' own evaluation, no independent replication found. The Glaze site shows Glaze 2.2 (Windows, RTX 50xx) and says 2.1 resisted "a new attack", undated. Opt-out registries (Spawning "Do Not Train", EU TDM machine-readable opt-out) were not verified this pass.
- Track: subject
- Affects: ethics file: respect artists' signals (NoAI tags, opt-outs) as intent, do not tell users protections were defeated or how
- Magnitude: n/a (initial)
- Sources: https://www.usenix.org/conference/usenixsecurity25/presentation/foerster, https://www.theregister.com/2025/07/11/defenses_against_ai_scrapers_beaten/, https://glaze.cs.uchicago.edu/

### F19 · 2026 · Practitioner fixes for the "AI look" (vendor blogs, treat as hypotheses)
- What: Recurring advice across 2026 guides: describe texture and imperfection (pores, fine hairs, uneven skin, wear) because "too perfect" reads as AI; name a camera, lens and a specific natural light (overcast afternoon, hard raking key) instead of "studio lighting"; add grain and upscale last; on CFG models, negative terms such as "airbrushed, plastic skin, CGI, oversaturated, video game render"; switch model when a model's default is plastic. Tells to check: plastic skin, perfect symmetry, hands, impossible lighting, warped objects, fake text, over-smooth detail. None addressed composition; artwright must bring the composition side itself (off-centre placement, negative space, cropping, eye-level variety).
- Track: practice
- Affects: the "AI look" checklist and its fixes
- Magnitude: n/a (initial)
- Suggested response: adopt as checklist items, each with a model-conditional fix
- Sources: https://invideo.io/faq/how-do-you-avoid-plastic-looking-skin-and-generic-ai/, https://magicshot.ai/blog/why-your-ai-images-still-look-fake-12-tells-and-how-to-kill-them, https://skinbase.org/academy/lessons/negative-prompts-and-common-ai-image-problems

### F20 · 2021-2023 · Prompt-vocabulary studies: subject plus style keywords carry the result
- What: Liu and Chilton (arXiv 2109.06977; 5,493 generations, 51 subjects x 51 styles) derived design guidelines centred on subject and style keywords. Oppenlaender's taxonomy (arXiv 2204.13988) identifies six modifier types from a three-month ethnography (from the full text, not re-verified on the abstract page this pass: subject terms, style modifiers, image prompts, quality boosters, repetition, magic terms). These are CLIP-era findings; quality boosters ("trending on artstation", "8k") are CLIP-era magic words with weak or negative value on LLM-encoder models, which prefer concrete description (F3, F4, F14).
- Track: subject
- Affects: vocabulary file structure (subject, medium/technique, movement, lighting, lens, composition, palette, era), and a list of dead "magic words"
- Magnitude: n/a (initial)
- Sources: https://arxiv.org/abs/2109.06977, https://arxiv.org/abs/2204.13988

## Overall magnitude: n/a (initial)

## Open questions:
- new: Qwen-Image 2.1 licence: Qwen-Image (original) card says Apache-2.0; two secondary sources say 2.1 needs a separate commercial agreement. Confirm on the 2.1 model card.
- new: MiniMax H3 licence, text encoder, and whether it honours a negative-prompt field or CFG (fal's guide only covers in-prompt negation).
- new: Getty v. Stability Court of Appeal hearing date; Allen v. Perlmutter ruling; USCO Part 3 final version date.
- new: Digital Omnibus: exactly which Article 50 dates moved (sources conflict); check the Official Journal.
- new: Midjourney V8 current parameters (--sref, --oref, --no, --stylize, personalization); official docs returned 403.
- new: Opt-out registries (Spawning Do Not Train, EU TDM opt-out, ArtStation NoAI) current status not verified.
- still open: movement-level vocabulary evidence (does "Ukiyo-e", "Bauhaus", "chiaroscuro" land reliably on Z-Image and FLUX.2?). No study found; artwright should build its own keyword-effectiveness log.

## Search plan notes:
- Subject: HF model cards and vendor guides (docs.bfl.ai, Vertex Veo guide) were the best sources; the Veo guide needs a second fetch with offset 100000. Comfy blog is primary for local model releases. kombitz.com weekly roundups are a useful news feed for open models. local-ai-zone guide had an impossible future "last updated" date: noise. Legal: chatgptiseatingtheworld.com tracks Andersen docket entries reliably; copyright.gov/ai lists report parts; Part 3 PDF is readable with the Read tool page by page after WebFetch saves it.
- Tooling: skills.cat/openskillindex/claudemarketplaces surfaced registry skills; GitHub API for repo stats. No skills.sh install counts read. MCP registry not queried (budget).
- Practice: vendor "AI look" blogs are commercial; useful only as checklist seeds. fal's model guides are good practitioner sources.
- Testing: arXiv for VAB and ArtCoT was productive. Not covered: promptfoo/Inspect assertion types, VQAScore/DSG/TIFA for prompt adherence (known from prior knowledge, not verified this pass).
- Forums not checked: Comfy forum/Discord, r/StableDiffusion (Reddit blocked in this environment), BFL Discord.

## Tracks covered: subject: 11 queries · tooling: 2 · practice: 3 · testing: 2 (plus fetches across all four; creation-mode target of five queries per track not met on tooling and testing because of the shared search budget)

## Upcoming events:
- 2026-12-02 · EU AI Act Art. 50(2) machine-readable marking applies to generative systems already on the market before 2 Aug 2026
- 2027-02-17 or later · Andersen v. Stability summary-judgment hearing (schedule extended again on 2026-09-28; resolution end of 2027 at the earliest)
- undated · Getty v. Stability Court of Appeal hearing; Allen v. Perlmutter summary-judgment ruling; USCO Part 3 final; Z-Image-Edit and Omni-Base releases; Midjourney V8 leaving alpha

## Nothing changed: no (creation pass)

## Cost: searches 19 · fetches 28 · tool calls 53

## Proposals for artwright

- **Prompt-critique procedure (judge then revise):** (1) restate the brief as checkable claims (subject, action, composition, palette, light, medium, mood, text, must-keep items); (2) generate 2 to 4 candidates and judge by comparison (pick best and worst, then why), never a lone 1 to 10 score (F7); randomise order and re-ask once when the pick is close; (3) every criticism names visible evidence: where in the frame, what is wrong (F17); (4) classify each fault by fix channel: prompt wording, model setting (CFG, steps, seed), control (depth, pose, canny), reference image, inpaint region, or model switch (F15); (5) emit a revised prompt plus a one-line diff of what changed and why; (6) stop after a fixed number of rounds or when all must-have claims pass (F8). Fit/deny verdict is a separate line: FITS, FITS WITH FIXES, DOES NOT FIT.
- **Rubric:** seven dimensions borrowed from the existing Midjourney critic (subject, lighting, colour, mood, composition, material, spatial) plus brief fit and "AI look" (F13), each pass/fix/fail with evidence rather than numeric.
- **"AI look" checklist (about 15 items)** with a model-conditional fix for each: plastic skin, HDR glow and overexposure, teal-orange grade, oversaturation, dead-centre subject, perfect symmetry, shallow-DOF-on-everything, generic "epic" lighting, garbled text, extra fingers, set drift between shots (F9, F19). Fixes differ by model: negative prompt only where CFG > 1; positive rephrasing on FLUX.2 and Z-Image Turbo.
- **Per-model profile files** (one short file each, about 40 to 80 lines): Z-Image Turbo, Z-Image base, FLUX.2 dev/klein, Qwen-Image 2.x, MiniMax H3, Wan 2.x, plus thin "verify first" profiles for Nano Banana, Midjourney, GPT-Image, Seedream, Veo. Fields: text encoder, CFG/negatives honoured, prompt length sweet spot, word order, reference syntax, control options, known defaults to steer against, licence note, date checked.
- **Style vocabulary file, about 400 to 600 terms in one file (target under 40 KB)**, grouped: art movements and periods; media and techniques (gouache, linocut, cel shading, impasto); lighting (Rembrandt, rim, low-key, golden hour, overcast); lens and camera (focal lengths, film stocks, angles and moves from the Veo list); composition (rule of thirds, leading lines, negative space, Dutch angle, frame within frame); palette and colour harmony; mood. Each term gets a one-line visual definition, so the judge can also use it in reverse to name what it sees. A "dead magic words" list ("trending on artstation", "8k", "masterpiece") for LLM-encoder models (F20). A keyword-effectiveness log per model, appended with evidence from real runs (F13).
- **Living-artist rule:** when a prompt names a living artist (or a deceased one whose estate is active), artwright replaces the name with the traits that define the look (medium, palette, line quality, subject matter, composition habits, era/movement) and says so in one line; it never re-inserts the name. Movements, historical masters long in the public domain, and studio-wide genres may be named. Rationale with dates: style is not copyrightable but outputs can infringe and style imitation counts in market-dilution arguments (USCO Part 3, May 2025); OpenAI refuses living-artist styles since March 2025; Andersen v. Stability is unresolved (F5, F10, F16).
- **Ethics and law reference file** with a dated status table (Andersen, Getty appeal, Thaler/Allen, USCO Parts 2 and 3, EU AI Act Art. 50 dates, Steam disclosure, Glaze/LightShed) and a "not legal advice" header; refresh every 60 to 90 days. Practical outputs: remind to keep a record of human selection and edits when copyright matters (Part 2); flag photoreal depictions of real people or places for labelling in the EU (F6); note Steam disclosure for game assets (F12).
- **Hand-off contract with comfyui-gen (and cinewright/brandwright):** artwright returns a JSON brief (BFL-style fields: scene, subjects, style, palette with hex, lighting, camera, composition, must_keep, must_avoid) plus a rendered prose prompt per target model, settings hints (CFG, steps, negative prompt only if honoured), control suggestions (depth/pose/canny source), and reference roles ("Image 1: mood and palette only"). comfyui-gen returns image paths, the exact prompt and settings used, seed and model; artwright judges and returns the verdict, the fix list and the next prompt. For MiniMax H3 the brief is a timed shot list with labelled references and an audio line (F2).
- **Evals:** cases that check (a) a living-artist name is replaced by traits, (b) negative prompts are not suggested for Z-Image Turbo or FLUX.2, (c) the judge picks the worse of a known good/bad pair (seeded from saved runs), (d) every criticism cites a location in the image, (e) the revised prompt changes only what the critique named.
