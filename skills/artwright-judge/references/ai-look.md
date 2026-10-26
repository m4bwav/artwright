# AI-look tells

Common defaults of generation models that make an image read as generic, each with a fix that depends on the target model.

Checked 2026-10-22 · Back to [SKILL.md](../SKILL.md)

Verification: the tells and fixes come from practitioner reports and the research pass, `verified: no` unless a line cites an R- entry. Rows 17 to 29 apply light and composition teaching read in Gurney, Roberts and Mateu-Mestre (R-20261022-1, -2; the craft rows are in [craft.md](../../artwright/references/craft.md)); rows 30 to 34 apply *Computer Graphics: Principles and Practice* and three pixel-art books (2026-10-25); that a model does them by default is practitioner observation.

**Measure first.** Where a row names a flag, run the command (`aw.py light`, `depth` or `comp`, see "Light, colour and composition flags" in [cli.md](../../artwright/references/cli.md)) and open the region it points to. A flag is a place to look, never the finding.

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
| 7 | Rim light everywhere | bright edge outline on every subject with no source; a real rim needs a light behind and a dark ground, takes a lighter local colour and varies in width | P: name one motivated source ("window at left, no backlight"); I: edge pass |
| 8 | Teal-and-orange grade | warm skin, cyan shadows, regardless of scene | P: name the grade ("overcast neutral", "Kodak Portra 400"); N: "teal and orange" |
| 9 | Generic epic light | god rays, haze and sunset in every scene | P: specific weather and hour ("flat noon overcast"); N: "volumetric light, god rays" |
| 10 | One narrow style | every output glossy semi-real "concept art" | P: name medium and technique from [vocabulary.md](vocabulary.md); R: a style reference; M: a model with that range |
| 11 | Over-smooth detail | uniform micro-detail, no texture variation, surfaces like CG | P: wear, grain, "film grain", named materials; S: fewer steps on some distills; M |
| 12 | Garbled text and signage | near-letters, misspellings | P: quote exact text and place it; M: Qwen-Image or a text-strong model; I: text region; on H3 in-prompt "Do not introduce garbled characters" |
| 13 | Hands and anatomy | extra or fused fingers, broken limbs | C: pose map; I: hand region; P: simpler hand action |
| 14 | Warped objects and physics | bent cutlery, melting furniture, impossible reflections | I: object region; P: fewer objects; C: depth map |
| 15 | Glamour faces | same young idealised face, model-perfect proportions | P: age, build, specific features, "ordinary person"; R: a character reference |
| 16 | Drift between shots (sets) | faces, costumes, props change across a series | R: one fixed character and set reference per shot; P: "same coat, same scar"; video: name what must stay fixed |
| 17 | Glowing shadows | shadows as saturated as the lights or more (`glowing_shadows`), or as warm as the sunlight in daylight (`warm_shadows`) | P: "shadows filled with cool skylight, less saturated than the lit side"; S: lower CFG; grade the shadows down after |
| 18 | No air | the distance as sharp, dark and saturated as the foreground (`no_recession`) | P: "distant hills pale, blue-grey and soft"; S: lower CFG; C: a depth map |
| 19 | Beams without cause | sunbeams with no screen, no dust, or with the viewer facing away from the sun | P: name the screen and the dust ("light through a barn's slats, dusty air"), or drop the beams; N: "god rays" |
| 20 | Wrong dapples | round sun spots on a slope, or dapples with no canopy above | P: name the canopy; I: the ground |
| 21 | White highlights and starbursts | pure white specular hits on every surface, star flares around lamps | P: "highlights tinted by the warm lamp", "no lens flare"; N: "lens flare, starburst" |
| 22 | Mirror water | perfect reflections on rippled water, or reflections brighter than the object | P: "rippled reflections, darker than the boats"; I: the water |
| 23 | Even texture | the same detail in light, half-tone and shadow | P: "texture lost in shadow"; I: shadow areas |
| 24 | Colouring-book edges | every edge equally crisp, nothing lost (`uniform_sharpness`); or a subject with one hard edge all round, pasted on | P: "soft lost edges in shadow, sharp only on the face"; S: depth of field; I: edge pass |
| 25 | Scattered hot spots | small bright or saturated spots everywhere competing with the subject, worst near the border (`hot_spot_near_border`, `edge_pull`) | P: "one bright area on the subject, the rest subdued"; I: the spots |
| 26 | Mid-grey mush | no dominant light or dark mass (`mid_dominant`, `fragmented`) | P: "large shadow masses, a single light source"; C: a value sketch as the control image |
| 27 | Horizon at half | the horizon cutting the frame in two (`horizon_split`), or through a head (`horizon_through_head`) | P: "horizon on the lower third", or a camera height that moves it |
| 28 | Background beats subject | a bright patch or sharp detail behind out-contrasting the subject (`competing_focal`, `focal_off_subject`, `weak_figure_ground`) | P: "background darker and softer than the subject"; I: the background |
| 29 | Toy soldiers and eye-level default | figures evenly spaced and sized in rows; every shot from standing eye height whatever the mood | P: "clustered group, one figure apart", a named camera height ("low angle from knee height"); C: a pose map |

| 30 | Floating objects | feet, cups and cars with no contact shadow, hovering over the ground | P: "a soft dark contact shadow under each foot"; I: the contact area |
| 31 | Moire and shimmer | fine regular patterns (chain-link, window screens, pinstripes, distant brick, rows of seats) turning into false bands or swirls; in video they crawl | P: describe the pattern as a tone at that distance, or bring it close; I: the patch |
| 32 | Detail ignores distance | far objects drawn with as many marks, as crisply, as near ones | P: "distant buildings simplified to a few shapes"; overlaps 18 |
| 33 | Metal and plastic confused | white highlights on gold or brass; tinted highlights on plastic under white light | P: "gold with warm yellow reflections", "white plastic with clean white highlights" |
| 34 | Quantised-render pixel art | rings of colour hugging the outline (`banding`), shading from the rim inward (`pillow`), value-only ramps, pure black shadows, dither on a tiny sprite (`aw.py pixel`, artwright-pixel) | M: draw at native size or snap first (pixelwright); P: "light from the top left"; fix the ramps by hand |

Describe each tell with evidence ("highlights blown on the left cheek and sky") and judge it against the brief. A deliberately glossy commercial brief may want 1, 2 and 6.
