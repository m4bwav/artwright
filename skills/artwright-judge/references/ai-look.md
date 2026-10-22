# AI-look tells

Common defaults of generation models that make an image read as generic, each with a fix that depends on the target model.

Checked 2026-10-21 · Back to [SKILL.md](../SKILL.md)

Verification: the tells and fixes come from practitioner reports and the research pass, `verified: no` unless a line cites an R- entry.

**These tells describe an image. They never prove it is AI-made.** Painters, photographers and 3D artists produce every one of them. Anthropic's docs say Claude cannot tell whether an image is AI-generated (R-20261021-11), so never give an "AI-made" verdict. Name the tell, point to where it is, and offer the fix only when it conflicts with the brief. A brief may ask for any of these on purpose.

Why they recur: reward tuning pushes models toward narrow high-scoring outputs, "monolithic styles or pervasive overexposure" (preference mode collapse, D²-Align, CVPR 2026). Aesthetic scorers reward polish and penalise rough briefs (R-20261021-5).

Fix channels: **P** prompt wording · **N** negative prompt (only where CFG > 1: Z-Image base, Qwen-Image original, Wan base; never Z-Image Turbo, FLUX.2 or CFG-1 distills) · **S** model setting · **C** control image · **R** reference image · **I** inpaint · **M** model switch.

| # | Tell | What to look for | Fix |
| --- | --- | --- | --- |
| 1 | Oversaturation | colours past what the light allows, candy skies | P: "muted", "limited palette", name 3 hues or hex; N: "oversaturated"; S: lower CFG |
| 2 | Overexposure and HDR glow | blown highlights, glow around everything, no deep darks | P: "low-key", a named single source, "deep shadows"; N: "HDR, bloom"; S: lower CFG |
| 3 | Plastic skin | poreless airbrushed faces, waxy sheen | P: "visible pores, fine hairs, uneven skin tone", named film stock; N: "airbrushed, plastic skin"; M: switch if the model default is plastic; I: face pass |
| 4 | Dead-centre subject | hero in the exact middle, symmetrical framing by default | P: "in the lower left third", "wide negative space to the right"; C: depth or pose map with the placement |
| 5 | Perfect symmetry | mirrored faces, buildings, arrangements | P: "candid", "three-quarter view", "slightly off-axis"; R: an asymmetric layout reference |
| 6 | Bokeh everywhere | shallow depth of field on every shot, melted backgrounds | P: "deep focus", "f/8, everything sharp", "wide lens" |
| 7 | Rim light everywhere | bright edge outline on every subject with no source | P: name one motivated source ("window at left, no backlight"); I: edge pass |
| 8 | Teal-and-orange grade | warm skin, cyan shadows, regardless of scene | P: name the grade ("overcast neutral", "Kodak Portra 400"); N: "teal and orange" |
| 9 | Generic epic light | god rays, haze and sunset in every scene | P: specific weather and hour ("flat noon overcast"); N: "volumetric light, god rays" |
| 10 | One narrow style | every output glossy semi-real "concept art" | P: name medium and technique from [vocabulary.md](vocabulary.md); R: a style reference; M: a model with that range |
| 11 | Over-smooth detail | uniform micro-detail, no texture variation, surfaces like CG | P: wear, grain, "film grain", named materials; S: fewer steps on some distills; M |
| 12 | Garbled text and signage | near-letters, misspellings | P: quote exact text and place it; M: Qwen-Image or a text-strong model; I: text region; on H3 in-prompt "Do not introduce garbled characters" |
| 13 | Hands and anatomy | extra or fused fingers, broken limbs | C: pose map; I: hand region; P: simpler hand action |
| 14 | Warped objects and physics | bent cutlery, melting furniture, impossible reflections | I: object region; P: fewer objects; C: depth map |
| 15 | Glamour faces | same young idealised face, model-perfect proportions | P: age, build, specific features, "ordinary person"; R: a character reference |
| 16 | Drift between shots (sets) | faces, costumes, props change across a series | R: one fixed character and set reference per shot; P: "same coat, same scar"; video: name what must stay fixed |

Describe each tell with evidence ("highlights blown on the left cheek and sky") and judge it against the brief. A deliberately glossy commercial brief may want 1, 2 and 6.
