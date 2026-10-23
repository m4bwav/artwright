# Empirical aesthetics

What experiments say about composition, colour and liking, so a critique states only what the evidence allows.

Checked 2026-10-21

Back to [SKILL.md](../SKILL.md).

## How to use this file

Each row gives the study, the effect, how well it has held up, and what the agent may and may not say. A finding about averages never decides one image: it can explain a reaction, never overrule the brief or a named tradition. `verified: yes` means the research pass or this file's author read the source.

## What holds

| Finding | Study and effect | Replication | May say | May not say | verified |
|---|---|---|---|---|---|
| Curvature preference | Chuquichambi et al. 2022 meta-analysis: 61 studies, 11,023 people, Hedges' g = 0.39 [0.25, 0.52]; stronger with brief viewing (0.75), null for spatial design (-0.04) and for art, design and architecture experts (-0.03) | Meta-analysis, high heterogeneity, no small-study bias | "Lay viewers on average lean towards curved forms, moderately" | "Curves are more beautiful"; any use with an expert audience | yes, R-20261021-7 (PMC10091794) |
| Colour is relative | Albers, *Interaction of Color* (1963): one colour reads differently on different grounds | Demonstrations, standard in teaching; consistent with Schloss and Palmer | "This grey reads warmer against the blue field"; judge colour in context, not swatch by swatch | That a colour is right or wrong in isolation | yes for the claim as used by Schloss and Palmer (PMC3037488); the book is a standard text |
| Preference and harmony differ | Schloss and Palmer 2011: 992 pairs of 32 colours; both rise with hue similarity; mean correlation about r = 0.79, individuals -0.03 to 0.70 | One lab, large design | "Harmonious and liked are different judgements" | "Harmonious, therefore better" | yes, R-20261021-7 |
| Order and complexity are two dimensions | Van Geert and Wagemans 2020 review: order is rarely disliked; liking of complexity depends on context and person (high order with high complexity reads as fascinating, with low complexity as soothing) | Review plus OCTA follow-ups; Dutch and Chinese samples similar (2025) | "Busy" or "too simple" only against the brief's purpose | "Too complex" as a defect on its own | yes, B-F9 (lirias.kuleuven.be) |
| Berlyne's inverted U | Holds on average but splits into opposite individual curves (Güçlütürk et al. 2016) | Mixed | "Some viewers will find this too dense" | One optimum complexity for everyone | yes, B-F9 |
| Centre and inward bias | Palmer lab: a single object is preferred at the centre; objects should face into the frame; vertical position follows the object (eagles high, stingrays low) | Several VSS studies, one lab | "The figure faces out of the frame; room ahead would help" | That centring is a fault | yes, R-20261021-7 (palmerlab.berkeley.edu/spatial.html) |
| Fractal dimension 1.3 to 1.5 | Spehar, Taylor and colleagues: preference peaks at D about 1.3-1.5 for statistical fractals; for exact fractals most people like higher D (Bies et al. 2016, small samples) | Several studies, no recent meta-analysis | Report D as a description of texture | A target D to optimise towards; any claim for non-fractal images | yes, B-F10 (PMC4873502) |
| Interpretable features predict some liking | Iigaya et al. 2021: a linear model over contrast, saturation, hue and high-level features predicted liking within and across people | One study, needs human labels | "Contrast and saturation are among the features that track liking" | A beauty number from features | yes, B-F8 |
| Fluency | Reber, Schwarz and Winkielman 2004: ease of processing explains liking for symmetry, contrast, prototypes | Influential, no meta-analysis found | "Clearer figure-ground makes it easier to read" | That symmetry is universally liked; experts can prefer asymmetry (Weichselbaum et al. 2018) | partly: source read, replication open (B-F14) |
| Expertise changes judgement | Experts weigh style, accept negative valence, lose the curvature effect | Several studies | Say whose criteria apply (lay, expert, a tradition, the brief) | One judgement for all audiences | yes, B-F5, B-F14 |

## The myths

| Claim | Evidence | May say | May not say | verified |
|---|---|---|---|---|
| Rule of thirds marks good pictures | Amirshahi et al. 2014: highly rated photos and paintings scored no higher on a computed thirds score; Palmer lab found the centre most preferred for single objects. Some cropping studies find people use thirds when asked to crop | "Off-centre placement here gives the eye a path", with the reason | A thirds score, or "breaks the rule of thirds" as a fault. Thirds is never a score | yes, R-20261021-7 (thirds 2014 via a search summary of the PDF; direct fetch failed) |
| The golden ratio is the most pleasing proportion | McManus 1980 and McManus et al. 2010: weak or no group preference, strong and divergent individual preferences; spiral overlays on paintings are post-hoc fitting | Correct the premise when asked "does it follow the golden ratio?" | The golden ratio as a reason for any verdict | yes, R-20261021-7 (PMC4937063) |
| Itten's schemes (complementary, triadic, split) predict harmony | No experimental support found; Itten and Chevreul treated preference and harmony as one, which Schloss and Palmer separate | Use the schemes to generate candidate palettes | "The palette fails because it is not triadic" | yes as absence of support in the pass (B-F11); a later study could change this |
| Learned aesthetic scores measure art quality | LAION predictor: photo-contest data, Western and gender skews, picks the defective image over the clean one 58% of the time | Call such a score "photo polish, biased" | Use it as a verdict | yes, R-20261021-5 |

## Image statistics

`aw.py stats` reports numbers that describe an image so a critique can point at evidence. None is a beauty score, none has a "good" value, and most change with image size, so stats run at a fixed long edge (256 px by default). Names follow the Aesthetics Toolbox (Redies, Bartho et al., Behavior Research Methods 2025, MIT) where it has the measure, so numbers can be compared with the literature (verified: yes, its `QIP_machine_script.py` and documentation page, read 2026-10-21).

- **Value histogram and key**: the spread of lightness; key says whether most values sit low, middle or high, and whether shadows or highlights clip.
- **RMS contrast**: the standard deviation of L\* in CIELAB (toolbox range about 0-50). Higher means a wider spread of light and dark, not a better picture.
- **Colourfulness**: Hasler and Süsstrunk 2003, M = sqrt(sd_rg² + sd_yb²) + 0.3 × sqrt(mean_rg² + mean_yb²), with rg = R − G and yb = ½(R + G) − B on signed sRGB values (0-255). Their anchor points: not colourful 0, slightly 15, moderately 33, averagely 45, quite 59, highly 82, extremely 109. These are points on a scale fitted to 20 viewers rating 84 versions of 10 scenes, not bands, and the 95.3% correlation is the authors' own, not replicated. The toolbox has no colourfulness measure. Verified: yes (the paper, read via its archived EPFL copy).
- **Saturation**: mean and spread of HSV S; the warm/cool split is the share of chromatic pixels on each side of the hue circle.
- **Edge density**: the share of the image taken by edges; a rough measure of detail or clutter. The toolbox computes it from Gabor filters on a 120,000-pixel greyscale copy; aw.py uses a cheaper edge filter, so its values are close in rank but not equal.
- **Mirror symmetry**: percentage (0-100) of matching pixels across the vertical and horizontal axes of a binarised image (toolbox definition).
- **Balance**: the toolbox's Hübner score, the mean of eight percentage weight differences (left-right, top-bottom, both diagonals and inner-outer for each). 0 is perfectly even, so higher means less balanced. **DCM** is the distance of the centre of mass of darkness from the frame centre, with its x and y position.
- **Fractal dimension**: 2D box-counting on a binarised copy, between 1 and 2; sensitive to the threshold, which the output records.
- **Thirds distance**: how far the estimated focal point sits from the nearest thirds intersection. Description only, never scored.

Use: say "RMS contrast 12, low for a night scene meant to feel tense" with the brief as the reason. Never rank two images by any of these numbers alone.
