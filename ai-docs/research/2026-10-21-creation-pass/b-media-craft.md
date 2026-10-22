# Creation pass 2026-10-21: B. media and craft (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation (no `last_checked`). Magnitudes are `n/a (initial)`. Where a statement comes from model memory and was not checked against a fetched page in this pass, it is marked **(memory, unverified)**.

## Findings (newest first)

### F1 · 2026-09-17 (repo push; paper 2025-03-14) · Aesthetics Toolbox: the reference implementation of pixel metrics used in empirical aesthetics
- What: Redies, Bartho et al., "A toolbox for calculating quantitative image properties in aesthetics research", Behavior Research Methods 57:117 (2025), merges the scripts of four labs (Redies, Spehar, Hübner, Mather) into Python 3 and checks them against the originals. It computes size and aspect ratio; channel means/SD in RGB, L\*a\*b\*, HSV; hue entropy; RMS contrast (SD of L\*); lightness entropy; HOG complexity; Gabor edge density (rho 0.85 with HOG complexity); mirror symmetry and CNN symmetry; Wilson-Chatterjee balance score and deviation of centre of mass (DCM); Fourier amplitude slope (natural scenes about -1.2, range -0.8 to -1.5; power slope about -2.4) and Fourier sigma; 2D and 3D box-counting fractal dimension; PHOG and CNN self-similarity; homogeneity; anisotropy; first- and second-order edge-orientation entropy; CNN sparseness and variability. Cautions in the paper: most values depend on image size (resize to at least 1024 px on the long side), forcing square crops changes the image, the three Fourier-slope implementations correlate only 0.77-0.84 with each other, and correlations with ratings are not causal. MIT licence, 40 stars, pushed 2026-09-17; August 2026 added DODA, a database of aesthetics datasets (arXiv 2608.00089). Heavy (Streamlit, AlexNet weights), so artwright should copy definitions, not depend on it.
- Track: tooling
- Affects: the planned pixel-metrics script (metric list, defaults, image-size rule)
- Magnitude: n/a (initial)
- Suggested response: adopt (use its definitions and naming so artwright numbers are comparable with the literature; cite it in the knowledge file)
- Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC11909096/, https://arxiv.org/abs/2408.10616, https://github.com/RBartho/Aesthetics-Toolbox

### F2 · 2026-01-14 · LAION-Aesthetics predictor is a photo-contest taste model with measured biases
- What: An audit (arXiv 2601.09896) shows the LAION-Aesthetics Predictor was trained on about 428k images, 60% from AVA (dpchallenge photo contests), 34% SAC, 6% logos; it favours realistic landscapes, cityscapes and portraits by Western and Japanese artists and skews by gender in captions. A 2026 vendor report (ERNIE-Image) says it over-scores anime and snapshots (vendor claim, unverified). NIMA on AVA reaches SRCC around 0.5-0.6 against mean ratings (0.534 for its MobileNet variant). Learned aesthetic scores measure agreement with one crowd's photo taste, not art quality.
- Track: tooling / testing
- Affects: any "aesthetic score" in the script; judge prompts for comparisons
- Magnitude: n/a (initial)
- Suggested response: note (never ship a single learned beauty score as a verdict; if a sibling uses one, label it "photo-contest taste, biased")
- Sources: https://arxiv.org/html/2601.09896, https://arxiv.org/pdf/1709.05424

### F3 · 2025-09 to 2026 · MLLM art-commentary benchmarks: models over-weight technique and lack interpretive depth
- What: VULCA / MHEB (arXiv 2509.23208) compares MLLM commentary on Castiglione's "Twelve Months" with 163 commentaries by nine art historians, coded on Evaluative Stance, Feature Focus and Commentary Quality (Profound Insight, Strong Argumentation, Detailed Analysis, Logical Clarity). Baseline outputs cluster on "generic or technique-oriented profiles"; one model scored brushwork focus at 0.937 against a human 0.199. Persona cards plus a knowledge base raised insight scores (Qwen 0.31 to 0.61), but the alignment metric is partly circular. Related: KidsArtBench (EACL 2026, 1k children's works, 9 rubric dimensions by 12 educators), ArtiMuse (8-dimension critique plus score), AesCanvas (critique plus fit-for-context; identifier looks odd, unverified).
- Track: testing / practice
- Affects: critique procedure; eval rubric for artwright's own critiques
- Magnitude: n/a (initial)
- Suggested response: adopt (grade artwright critiques on specificity, argument and evidence, not on length; use the VULCA quality dimensions as rubric names)
- Sources: https://arxiv.org/html/2509.23208v2, https://aclanthology.org/2026.eacl-long.267/

### F4 · 2025-01 · ArtCoT: structured describe-then-critique beats free chain-of-thought for aesthetic comparisons
- What: Jiang and Chen (arXiv 2501.09012) built MM-StyleBench (about 1k content and 1k style images, 21k expert preference judgements from 12 experts) and tested GPT-4o, Gemini 1.5 Flash and Claude 3.5 Sonnet on pairwise aesthetic judgements of stylised images. Zero-shot chain-of-thought made alignment with human preference worse (about -22% per-method, -18% per-instance) and filled answers with "feels", "sense", "somewhat". ArtCoT (1. describe concrete content and style features, 2. a critic phase that re-checks them against art principles and context, 3. a summariser that picks) improved alignment 56% per-method and 29% per-instance and cut subjective words from 20% to 5.5%. The critic phase mattered most in ablation.
- Track: practice
- Affects: the A/B comparison procedure ("which image is better")
- Magnitude: n/a (initial)
- Suggested response: adopt (three stages; ban vague hedges in the judge; require each claim to point at a region or feature; output structured JSON)
- Sources: https://arxiv.org/html/2501.09012v1

### F5 · 2025 (Ann. N.Y. Acad. Sci. 2022 meta-analysis, cited 2025) · Preference for curvature is real but moderate, and vanishes for experts and spatial design
- What: Chuquichambi et al. (2022), 61 studies, 106 samples, 309 effects, 11,023 participants: Hedges' g = 0.39 [0.25, 0.52], heterogeneity high. Stronger with brief presentation (g 0.75 vs 0.32 unlimited), meaningless shapes (0.56) and objects (0.42); null for spatial design (-0.04) and for architecture/design/art experts (-0.03). No small-study bias detected. "Reliable but not universal."
- Track: subject
- Affects: evidence file; claims in critiques ("curves are more pleasing")
- Magnitude: n/a (initial)
- Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC10091794

### F6 · 2022 · Composition "rules" are broken by good photos for nameable reasons
- What: Wang, Lee and Lee (PLoS ONE 2022) took the top and bottom 5% of AVA (about 25.5k photos); nine interpretable features classified quality at about 77-78% accuracy, with sharpness (clarity) the biggest gap. Centred horizons (10.6% of landscapes) were justified by reflections, crossing objects, leading lines; centred subjects by symmetry, circular shapes, framing. Rule-break categories were judged by one co-author, so subjective.
- Track: subject / practice
- Affects: critique checklist (a rule break needs a reason, not a penalty)
- Magnitude: n/a (initial)
- Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC9249203/

### F7 · 2014 (Amirshahi et al.) and VSS 2006-2014 (Palmer lab) · Rule of thirds does not predict aesthetic quality; centre and inward biases do
- What: Amirshahi, Hayn-Leichsenring, Denzler and Redies (Art & Perception 2014) computed a saliency-based thirds score: highly rated photos and a large set of paintings scored about as low as photos ignoring the rule; ratings did not correlate with the computed score and only weakly with subjective thirds scores (via search summary of the PDF; direct fetch failed). Palmer, Hara and Griscom (VSS 2014) found the frame centre most preferred for single objects, contradicting both claims of the rule. Palmer, Gardner and Wickens (2008): centre bias plus inward bias (objects should face into the frame); vertical "ecological" biases (eagles high, stingrays low); preferred size tracks real size; context justifies off-centre placement. Counter-evidence: a 2012 Berkeley cropping study found croppers follow thirds more than other guidelines; Sahyun (Electronic Imaging 2024) reports thirds adherence correlating with judgements. Verdict: a heuristic for off-centre placement, not a quality metric.
- Track: subject
- Affects: composition checklist; thirds metric in the script
- Magnitude: n/a (initial)
- Sources: https://uniklinikum-jena.de/anatomie1_media/Inhalte/AmirshahiARTP2014-font-1.pdf, https://palmerlab.berkeley.edu/spatial.html, https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-94.pdf, https://library.imaging.org/ei/articles/36/11/HVEI-229

### F8 · 2021 · Art preference is partly predictable from interpretable low- and high-level features
- What: Iigaya et al., Nature Human Behaviour 5(6), 2021: a linear model over low-level features (contrast, saturation, hue and others) plus high-level ones (dynamic vs still, and similar) predicted liking within and across people; similar features emerge in an object-recognition CNN. Required supervised human labels. Exact variance explained not read this pass.
- Track: subject / testing
- Affects: framing of pixel metrics (useful features, not verdicts)
- Magnitude: n/a (initial)
- Sources: https://authors.library.caltech.edu/109241/, https://ideas.repec.org/a/nat/nathum/v5y2021i6d10.1038_s41562-021-01124-6.html

### F9 · 2020-2025 · Order and complexity: order is almost never disliked, complexity depends on context
- What: Van Geert and Wagemans, "Order, complexity, and aesthetic appreciation" (Psych. Aesthetics, Creativity and the Arts 14:1-20, 2020) calls the literature "diffuse and contradictory" and treats order and complexity as two independent dimensions; follow-up OCTA studies: high order plus high complexity reads as fascinating, high order plus low complexity as soothing; a Dutch vs Chinese comparison (Empirical Studies of the Arts 2025) found similar preferences. Berlyne's inverted U holds on average but splits into opposite individual curves (Güçlütürk et al., Frontiers in Human Neuroscience 2016: one group's liking falls with complexity, another's rises).
- Track: subject
- Affects: evidence file; critique language about "busy" or "too simple"
- Magnitude: n/a (initial)
- Sources: https://lirias.kuleuven.be/retrieve/552894, https://www.frontiersin.org/articles/10.3389/fnhum.2016.00112/full

### F10 · 2016-2018 · Fractal dimension 1.3-1.5 preference holds for statistical fractals only
- What: Spehar, Taylor and colleagues report preference peaking at D about 1.3-1.5 for natural and statistical fractals, with consistent dislike of 1.1-1.2 and 1.6-1.9 (Viengkham and Spehar 2018 across image types). Bies et al. (Frontiers in Human Neuroscience 2016) found that for exact fractals, about 76% of people liked higher D, rising towards 2, with a 24% subgroup the reverse (small samples, 42 and 18). No 2021-2025 meta-analysis found. Box-counting D on a binarised artwork is threshold-sensitive.
- Track: subject
- Affects: evidence file; fractal-D metric (report, do not optimise)
- Magnitude: n/a (initial)
- Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC4873502, https://frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00350/text

### F11 · 2010-2013 · Colour harmony: preference and harmony are different judgements (Albers right, Itten conflated them)
- What: Schloss and Palmer (2011), 992 pairs of 32 colours: pair preference and harmony both rise with hue similarity, but preference depends more on liking of the component colours and on lightness contrast. Mean preference and harmony correlate about r = 0.79, individuals from -0.03 to 0.70. They note Chevreul and Itten treated preference and harmony as one; Albers argued harmonious need not mean liked. Preference for harmony varies by person and peaks with moderate colour training. Palmer and Schloss's ecological valence theory: colour preference follows liking of associated objects (memory, consistent with the cited lab pages). No experimental support found for Itten's colour-wheel schemes (complementary, triadic and so on) as predictors of liking; treat them as generators of candidate palettes, not tests.
- Track: subject
- Affects: colour section of the knowledge file; critique language
- Magnitude: n/a (initial)
- Sources: https://palmerlab.berkeley.edu/pdf/Schloss&Palmer(2011).pdf, https://pmc.ncbi.nlm.nih.gov/articles/PMC3037488

### F12 · 2003 (formula) · Hasler-Süsstrunk colourfulness: cheap, validated on its authors' data, implementations differ
- What: C = sqrt(sd_rg^2 + sd_yb^2) + 0.3 * sqrt(mean_rg^2 + mean_yb^2) with rg = R - G and yb = (R + G)/2 - B; authors report over 90% correlation with a 7-category rating experiment. No independent replication of that number found. The widely copied PyImageSearch code takes absolute values of rg and yb, which changes the means; the paper's category thresholds (memory, unverified: roughly 0, 15, 33, 45, 59, 82, 109 for not to extremely colourful on 0-255 sRGB) should be checked against the PDF before shipping.
- Track: tooling
- Affects: colourfulness metric in the script; its unit test
- Magnitude: n/a (initial)
- Suggested response: adopt (signed channels as in the paper; record the variant in output)
- Sources: https://infoscience.epfl.ch/record/33994, https://pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/

### F13 · 1980-2025 · Golden ratio: weak or no population preference; strong idiosyncratic individual preferences
- What: Fechner's golden-rectangle result fails under controlled methods (McManus 1980; McManus et al. 2010): group preference weak, individual rectangle preferences strong, stable and divergent (one factor near-square, one elongated). Redies' toolbox paper also states modern controlled studies do not support Fechner. One 2000 Perception study found mean ratios near 1.618 for context-free rectangles but none in painting proportions. Spiral overlays on paintings are post-hoc fitting.
- Track: subject
- Affects: myths file; critique language (never cite the golden ratio as a reason)
- Magnitude: n/a (initial)
- Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC4937063, https://journals.sagepub.com/doi/10.1068/p3037

### F14 · 2004-2019 · Processing fluency and expertise effects
- What: Reber, Schwarz and Winkielman (PSPR 2004) explain liking for symmetry, figure-ground contrast, prototypicality and repetition by ease of processing. No meta-analysis or registered replication was found this pass (open). Expertise changes judgements: experts weigh style and collative properties, rate abstract work closer to representational work, like negatively valenced art more, and in one study prefer asymmetric simple stimuli ("Symmetry is not a universal law of beauty", Weichselbaum, Leder, Ansorge 2018); the curvature effect disappears for design experts (F5). Leder et al. (2004) model remains the standard framing (memory: a 2014 revision by Leder and Nadal exists, unverified).
- Track: subject
- Affects: evidence file; who-is-the-audience step in critiques
- Magnitude: n/a (initial)
- Sources: https://pages.ucsd.edu/~pwinkielman/reber-schwarz-winkielman-beauty-PSPR-2004.pdf, https://pubmed.ncbi.nlm.nih.gov/30390421/, https://openhsu.ub.hsu-hh.de/handle/10.24405/4415

### F15 · Ceramics identification: body, firing and marks
- What: Body type from an image is a guess; from the object: porcelain is vitrified, white through the cross-section, translucent at thin edges (not reliable alone, hotel porcelain fails), rings when tapped; earthenware is porous, opaque, buff to red under the glaze (tin-glazed Delft shows the coloured body at chips); stoneware is vitrified but opaque, often grey or buff, salt glaze gives orange-peel texture. Typical firing (memory, unverified in this pass): earthenware about 1000-1150 °C, stoneware about 1200-1300 °C, porcelain about 1250-1400 °C. Chinese reign marks: six characters = dynasty (da Ming / da Qing), era name, nianzhi ("made in the period"), read top-to-bottom, right-to-left; four-character marks drop the dynasty; script is kaishu (regular) or zhuanshu (seal); underglaze blue or overglaze iron red, later sometimes stamped. Marks begin under Yongle (1403-1424). Kangxi potters put earlier Ming marks (Xuande, Chenghua) on wares as homage ("apocryphal" marks); Chenghua is the most copied mark and the Qianlong seal mark is heavily copied later. Rule for the agent: a mark never dates a piece alone; judge body, glaze, foot, potting and painting style, and say "mark and period" vs "mark of, not of the period".
- Track: subject
- Affects: ceramics knowledge file; "is this Ming?" answers
- Magnitude: n/a (initial)
- Sources: https://aziatischekeramiek.nl/en/learn/7579-reign-marks-on-chinese-ceramics, https://delftsaardewerk.nl/en/recognize/material, https://holst-porzellan.com/en/knowledge/characteristics/determination/, https://www.invaluable.com/blog/reading-reign-marks-an-essential-guide-to-antique-chinese-porcelain/

### F16 · Printmaking identification checks
- What: Relief (woodcut, linocut, wood engraving): large solid blacks, ink rim along line edges, embossing on the back, no plate mark. Intaglio (engraving, etching, drypoint, aquatint, mezzotint): plate mark (can be faked or trimmed), line dominates in engraving and etching, tone in aquatint and mezzotint (memory: engraved lines swell and taper; etched lines are even with blunt ends; drypoint has velvety burr). Planographic lithograph: flat ink, crayon grain. Screenprint: flat opaque ink layers, possible mesh texture. A regular dot or square pattern under magnification means a photomechanical reproduction (halftone, offset), not an original print. Reference book: Bamber Gascoigne, "How to Identify Prints" (1986/2004).
- Track: subject
- Affects: printmaking section; "is this an original print?" answers
- Magnitude: n/a (initial)
- Sources: https://docs.wellcomecollection.org/visual-and-material-culture-cataloguing/pre-cataloguing/about/untitled, https://www.crockerart.org/art/themes/theme-how-prints-are-made

### F17 · Pixel art: a named, checkable defect vocabulary
- What: Community canon (PixelJoint tutorials, a TU Delft thesis on fixing artefacts, Wayline lessons) agrees on: pillow shading (shading follows the outline, not a light source), banding (adjacent segments of different colours aligned end-to-end, often caused by bad anti-aliasing), jaggies (irregular step lengths on lines and curves; good lines use consistent 1-1, 2-1, 3-1 steps), orphan pixels, doubled pixels on 1 px lines, too many colours, and inconsistent pixel size ("mixels"). Mixels and off-grid pixels are the typical failure of AI-generated "pixel art", which a script can test (grid size detection, unique-colour count, colours per tile).
- Track: subject / testing
- Affects: pixel-art checklist; script checks
- Magnitude: n/a (initial)
- Sources: https://pixeljoint.com/forum/forum_posts.asp?TID=11299, https://repository.tudelft.nl/file/File_65d43acd-9779-4eab-999b-9bcd4f0a96a9, https://www.wayline.io/learn/pixel-art/1

### F18 · Existing art-critique skills are thin; one useful pattern each
- What: GitHub code search for `path:SKILL.md "art critique"` finds no maintained, used skill: yamatakeru/art-critique-skills (0 stars, Feb 2026) builds on Noël Carroll's "On Criticism" (2009) seven components (description, classification, contextualisation, elucidation, interpretation, analysis, evaluation) with evaluation central; the-vibey-project "art-theory-fundamentals" (3 stars, active) separates four kinds of claim: craft/perceptual (testable), historical (evidenced), philosophical (argued), interpretive (better or worse). afovea/game-dev-skills has an art-director persona (0 stars). Many others are AutoSkill-generated persona prompts. No skill computes pixel metrics or carries evidence grades.
- Track: tooling
- Affects: SKILL.md design; positioning
- Magnitude: n/a (initial)
- Suggested response: point (adopt the claim-type split and Carroll's components as ideas; nothing worth delegating to)
- Sources: https://github.com/yamatakeru/art-critique-skills, https://github.com/the-vibey-project/vibey

### F19 · Practice lesson: generic praise and "feels" language are the default failure
- What: Across ArtCoT (subjective-word rate 20%), VULCA (generic, technique-heavy commentary) and general VLM sycophancy work (arXiv 2408.11261: prompt-induced bias degrades answers; 2602.08311: models flip right-to-wrong under pushback more than the reverse), an uninstructed model praises, hedges and agrees with the asker's framing. No study specific to sycophancy in art feedback was found. Implied guards: blind the judge to who made the image and to the user's hoped-for answer, demand at least one concrete defect per critique with a location, and re-ask with order swapped for A/B comparisons (position bias, memory).
- Track: practice
- Affects: critique procedure; evals (a case where the image has a planted defect)
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://arxiv.org/html/2501.09012v1, https://arxiv.org/pdf/2408.11261, https://www.arxiv.org/pdf/2602.08311

### F20 · Practice lesson: rule overfitting and homogenised AI style
- What: Reviewers who score "follows rule of thirds" or "golden spiral fits" reward the wrong thing (F7, F13). Generated images drift to a default style (Utrecht thesis on SDXL "default style"; Patterns study where SDXL-captioner loops collapse to stock imagery; AIES 2025 paper: platform explains 54% of variance in visual outcomes). Art-direction guidance from practitioners is consistent but unpublished as a standard: silhouette readability, squint/notan test before colour, value grouping (a 70/25/5 split is a heuristic only), shape language, thumbnails distinct at small size.
- Track: practice
- Affects: critique checklist for AI-generated work (check for default-style sameness, not only defects)
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://export.arxiv.org/pdf/2410.06768, https://ojs.aaai.org/index.php/AIES/article/download/36799/38937/40874, https://www.creativebloq.com/how-to/concept-design-tips-for-artists/2, https://www.proko.com/community/topics/how-do-i-check-if-my-designs-are-clear-or-not

### F21 · Craft canon an agent needs (consolidated; mostly memory, sources are standard texts)
- What: Painting media cues from an image: oil (impasto, wet blending, glazes, craquelure), acrylic (fast-drying hard edges, less blending, plastic sheen), watercolour (transparency, paper white as the light, blooms/backruns, granulation), gouache (opaque, matte, flat), egg tempera (hatched strokes, no wet blending, often gold-ground panels), fresco (matte, giornate seams, limited lime-fast palette). Drawing: gesture first, construction from simple solids (Loomis, Bridgman, Vilppu), line weight varies with light, overlap and distance. Sculpture: subtractive (carving), additive (modelling), casting (lost-wax, sand; patina), construction/assemblage. Critique frameworks: Feldman's describe-analyse-interpret-judge (Art as Image and Idea, 1967), Carroll's seven components, studio crit (artist-silent or artist-first formats), Liz Lerman's Critical Response Process (memory). Design principles: contrast, repetition, alignment, proximity (Williams, The Non-Designer's Design Book), hierarchy; Gestalt: proximity, similarity, closure, continuity, figure-ground, common fate, Prägnanz. Value: notan (Arthur Wesley Dow, Composition, 1899), 3-5 value groups. Colour: Albers (Interaction of Color, 1963: relativity of colour), Itten's seven contrasts (The Art of Color, 1961). Perspective: one-, two-, three-point, atmospheric. Not re-verified page by page in this pass.
- Track: subject
- Affects: knowledge files' skeleton
- Magnitude: n/a (initial)
- Sources: standard texts as named; https://docs.wellcomecollection.org/visual-and-material-culture-cataloguing/pre-cataloguing/about/untitled

## Overall magnitude: n/a (initial)

## Open questions
- New: exact variance explained by Iigaya et al. 2021 features (paper not read in full).
- New: Hasler-Süsstrunk category thresholds and sign convention, check against the 2003 PDF.
- New: any meta-analysis or registered replication of processing-fluency effects on liking.
- New: whether symmetry preference has a meta-analysis (only single studies found).
- New: a published, citable art-direction review checklist for games or film (none found; practitioner posts only).
- New: firing temperature ranges and Qing seal-mark usage by reign are from memory; verify against a museum source (gotheborg.com refused the TLS handshake; Christie's guide mirror returned 403).
- New: Amirshahi 2014 PDF fetch failed twice (socket closed); findings come from a search summary of that PDF.

## Search plan notes
- Subject: author-name queries for specific papers worked best (Chuquichambi, Van Geert, Schloss Palmer, Iigaya). PMC full texts fetched cleanly. Wikipedia "Rule of thirds" has no empirical section; "Reign mark" redirects to a general ceramics article: poor finders here. gotheborg.com fails TLS for WebFetch; aziatischekeramiek.nl worked.
- Tooling: `gh search code --filename SKILL.md "art critique"` gave the skill landscape in one call; `gh api repos/...` gave stars and push dates. Aesthetics Toolbox found via the paper, not via skill search.
- Practice: generic "sycophancy art feedback" found only general VLM sycophancy papers; the MLLM art-critique benchmarks were the better practice source.
- Testing: arXiv benchmarks (MM-StyleBench, VULCA, KidsArtBench) give rubric dimensions; no promptfoo/Inspect art cases looked at (budget).
- Not reached: storyboard and shot-composition critique literature (left to the cinewright track), Gestalt primary sources (Wagemans et al. 2012 century review), fresco and tempera technical sources.

## Tracks covered: subject: 17 queries · tooling: 4 (2 web, 2 gh) · practice: 3 · testing: 2 (plus gh code search shared with tooling)

## Upcoming events: none found that change the answers.

## Nothing changed: no (creation pass).

## Cost: searches 25 · fetches 18 · tool calls 52

## Proposals for artwright
- **Critique procedure (SKILL.md core, about 60 lines):** 1) say what kind of claim is asked (craft/perceptual, historical, interpretive, taste); 2) describe concretely (subject, medium guess with confidence, value structure, palette, composition) before any judgement; 3) run the checklist; 4) a critic pass that re-checks each claim against a visible region; 5) verdict with at least one concrete fix and its location. For A/B comparisons use ArtCoT's three stages, run both orders, report disagreement. Ban "feels", "somewhat", "evokes a sense of" without a pointed-at feature.
- **Critique checklist contents (knowledge file, about 4-6 KB):** read at thumbnail size and in greyscale (notan, 3-5 value groups, focal point has the highest local contrast); silhouette and readability; focal point and eye path (leading lines, edges: hard where attention goes, lost elsewhere); balance and negative space; centre vs off-centre placement with a reason (inward facing, room in front of motion); colour (temperature logic, saturation hierarchy, harmony as a choice, not a rule); edges; rhythm and repetition; proportion, anatomy and perspective errors (horizon consistency, vanishing points); medium-appropriate handling; for AI images: default-style sameness, hands, text, mixels, lighting-direction mismatch.
- **Pixel metrics script (`aw.py metrics`, stdlib plus Pillow, numpy optional):** value histogram with key (low/mid/high) and clipping; RMS contrast on L\*; Hasler-Süsstrunk colourfulness (signed channels); saturation mean/SD; palette extraction via Pillow quantize (median cut) with percentages and a warm/cool split; Gabor-free edge density (Pillow FIND_EDGES mean) as complexity; mirror symmetry (L-R, T-B); Wilson-Chatterjee balance score and DCM; box-counting fractal dimension on a binarised image (report threshold); a notan render (2- and 3-value posterised thumbnail) and greyscale thumbnail written as PNGs for the model to look at. Fourier slope only when numpy is present. All at a fixed long side (1024 px). Output JSON with each metric's evidence grade; no single "beauty" score.
- **Pixel-art checks (`aw.py pixel`):** detect pixel grid scale and off-grid or mixed-scale pixels, unique colour count and ramp grouping, orphan pixels, doubled pixels on 1 px lines, colours per tile; emits a downscaled true-resolution copy.
- **Rule-of-thirds and golden ratio:** compute thirds distance of the estimated focal point only as a descriptive note; never score it. Myths file states the evidence (F7, F13).
- **Knowledge files and sizes:** `evidence.md` (empirical aesthetics with study, effect size, replication status: curvature, complexity/order, fractals, symmetry, fluency, colour harmony, centre/inward bias, expertise; about 8 KB); `media.md` (drawing, painting media cues, sculpture, printmaking identification; about 8 KB); `ceramics.md` (bodies, glazes, firing, Chinese reign marks with Ming and Qing era table and the apocryphal-mark rule; about 6 KB); `composition-colour.md` (principles, Gestalt, notan, colour theory with what is evidence vs convention; about 6 KB); `pixel-art.md` (defect vocabulary and fixes; about 4 KB); `critique-frameworks.md` (Feldman, Carroll, studio crit, art-direction review, rubric dimensions from VULCA; about 4 KB).
- **Evals:** a planted-defect case (an image with a clear tangent or muddy value structure; pass if the critique names it with location); an A/B case with a known expert preference; a "does it follow the golden ratio?" case where the pass is a correction of the premise; a reign-mark case where the pass is "mark alone cannot date it"; a fake pixel-art case where the pass names mixels.
- **Sibling contract:** expose the metrics JSON and checklist so cinewright (shot critique), comfyui-gen (pick the best of N generations) and polywright (render sheet critique) can call one command; keep the judge blind to which sibling produced the image.
