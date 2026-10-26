# Craft and critique

The working vocabulary of composition, value, colour and media, and the critique method that turns it into specific, checkable notes.

Checked 2026-10-22

Back to [SKILL.md](../SKILL.md).

Rows marked `verified: no` are standard teaching drawn from model knowledge and named texts, not checked against a fetched page in the research pass. Use them, but do not quote them as findings. What the experiments support is in [evidence.md](evidence.md).

## Composition

`book` rows are standard teaching read in the named book (R-20261022-1, -2): a practitioner's advice, not an
experiment, except where the row says the book reports one. Short names: Gurney CL = *Color and Light* (2010),
Gurney IR = *Imaginative Realism* (2009), Mateu-Mestre = *Framed Ink* 1 and 2, Roberts = *Mastering Composition*
(2007), Garvey-Williams = *Mastering Composition* (2014). A `comp` flag (in [cli.md](cli.md), "Light, colour and
composition flags") says where to look; confirm it by eye before it becomes a finding.

| Check | What to look for | verified |
|---|---|---|
| Thumbnail read | Shrink to about 100 px. Does the main shape still read? If not, the composition depends on detail | no (practice, B-F20) |
| Where the eye goes | Ask where a viewer looks first: faces and figures, then anything odd near the edges, then local contrast. Eye-tracking shows the eye jumps between points of interest a few times a second rather than gliding along lines, and skips strong contrast that fits the expected scene. Design supports that search; it cannot force a route. Leading lines, spokes converging on the head and gaze directions are supports, not a path | book: Gurney IR pp. 168-173 (reports eye-tracking studies) |
| Focal point | The subject should hold the highest local contrast in value, edge sharpness or saturation. Two equal competitors split attention (`competing_focal`); a peak off the stated subject is a finding to explain (`focal_off_subject`) | no (practice); flags measured |
| Armature | Name the underlying structure (S, L, diagonal, triangle, radiating, cross, zig-zag, arc) and say whether it ends on or turns at the subject. "No structure found" is a finding. Not measured: ask a vision model, then check it against `comp` | book: Roberts pp. 19-27; Mateu-Mestre FI2 pp. 26-29 |
| Placement | Centre or off-centre is a choice, judged by its reason: figures face into the frame, moving things get room ahead, symmetry and reflections justify a centred subject | yes, B-F6, B-F7 |
| Balance | Visual weight (size, value contrast, saturation, isolation, a face, text) on each side; a small strong element can balance a large weak one. Left-to-right reading habits shift weight and are culture-bound | no; weight list book: Garvey-Williams pp. 48-49 |
| Negative space | Shape of the gaps; a good empty area has a shape of its own and a job (release opposite a subject pressed to one side) | no; release book: Mateu-Mestre FI2 pp. 14-18 |
| Edge hierarchy | Hard, soft and lost edges. The hardest edges belong at the subject; equal edges everywhere read as a colouring book (`uniform_sharpness`). A subject with the same edge all round looks pasted on: let some edges merge with the ground (light on light, dark on dark) and state others | book: Roberts pp. 36, 87-88; Gurney IR pp. 166-167 |
| Frame edges and corners | Contrast, saturation or a bright spot in the border band (`edge_pull`, `hot_spot_near_border`), a strong line running into a corner, a key element touching the edge (`frame_tangent`) | book: Roberts pp. 31-32; Garvey-Williams pp. 66-67 |
| Way in and way back | An open entrance along the bottom (`blocked_entrance` when barred), and after the subject a route back into the picture rather than out at an edge | book: Roberts pp. 33, 101 |
| Hot spots | Small isolated light or high-chroma patches away from the subject compete with it | book: Roberts pp. 102-106 |
| Intervals and clusters | Neat rows, equal spacing and equal sizes look staged. Cluster faces and detail tightly against large quiet areas; a simple light shape behind the key head lifts it from a busy ground. Not measured | book: Roberts p. 30; Gurney IR pp. 174-175 |
| Tangents and mergers | Edges that just touch (a head against the frame, a horizon meeting a shoulder), a horizon through a head (`horizon_through_head`), a pole growing from a head, two silhouettes fused into one shape. Overlap clearly or separate | no; mergers book: Mateu-Mestre FI1 p. 26 |
| Horizon and camera height | Where the horizon sits (low, middle or high band, or none) and how high the camera is. Do they fit the feeling asked for? A horizon at exactly half splits the frame (`horizon_split`). Eye level cuts every standing figure on flat ground at the same height | book: Mateu-Mestre FI1 pp. 40-41; Gurney IR pp. 40-41 |
| Ground contact and scale | Feet on one ground plane; size falls off consistently with distance | book: Mateu-Mestre FI1 p. 71 |
| Silhouette | Fill the main figure black: the action, the face and both hands should still read, with limbs clear of the body | book: Gurney IR pp. 158-159 |
| Shape grouping | Neighbouring shapes of similar value fuse into a few big patterns, so a busy scene still reads; save the black-against-white jump for the subject (`fragmented` when no big shapes form) | book: Gurney IR pp. 162-163 |
| Depth devices | Overlap, size change, a dark foreground element framing the view (repoussoir), linear perspective with one horizon, atmosphere (below) | no; repoussoir book: Gurney IR pp. 180-181 |
| Open or closed | Is the story complete inside the frame, or do crops imply more outside it? Judge it against the brief | book: Chen ch. 4 |

Thirds is never a score. Say what the placement does, not which rule it meets. The golden ratio is never a reason.

**Questions for a vision model** (after Roberts, Mateu-Mestre and Gurney). Ask for one line each, tied to a
region:

1. The main subject and its box.
2. The armature.
3. Where the eye goes first, second and third, and whether it returns or leaves at an edge.
4. Every tangent, merger or border touch.
5. The horizon band and camera height, against the brief.
6. The silhouette read, and open or closed.

Then run `aw.py comp --subject x,y,w,h` and look again wherever the model and the measure disagree.

## Value

- Posterise to three and then four values. A strong design still reads as a few large shapes; a weak one turns
  mostly mid-grey with small scattered shapes (`mid_dominant`, `fragmented`). verified: book (Roberts pp. 44-47;
  Mateu-Mestre FI1 p. 34); notan after Arthur Wesley Dow, *Composition*, 1899
- The subject usually carries the strongest value contrast. A "70/25/5" split of dominant, secondary and accent
  values is a heuristic, not a rule. verified: no (practice, B-F20)
- Muddy values: middle tones everywhere, no clear light or dark mass. Common in AI images and in overworked
  paintings. A two-value study has a valley in the middle of its histogram (`stats` bimodality). verified: book
  (Gurney IR pp. 156-157)
- A gradient leads the eye from dark toward light. verified: book (Roberts p. 34)

## Light logic

Name the lights before judging them: the key (direction, colour, hardness), sky fill, ground bounce, any lamps in
the scene. Then check the rows. `aw.py light` gives the two families, their value gap, temperature shift and
chroma ratio; `--box` checks one object. These rows describe daylight and ordinary lamps. An artificial, alien or
stylised brief can break any of them on purpose: judge against the brief, never against the rule.

| Check | What to look for | verified |
|---|---|---|
| Two families | Lit and shadow sides stay apart in value; in sun the gap is wide (about half the value scale), and fill or bounce never rivals the key. Haze, cloud and light ground narrow it (`low_value_gap` is right for overcast) | book: Gurney CL p. 48 |
| Shadow colour | A shadow takes the colour of the bright things it can see: blue from a clear sky, grey under cloud. Up-facing shadow planes go cool, down-facing ones pick up warm bounce from the ground. Shadows as warm as the light (`warm_shadows`) mean no sky fill | book: Gurney CL pp. 50, 66-67 |
| Shadow chroma | In one surface, the shadow is darker, duller and cooler than the light, by about the same amount for every colour. Shadows more saturated than the lights (`glowing_shadows`) read as glowing | book: Gurney CL p. 52 |
| Form and cast shadows | Light side, terminator, core shadow, reflected light (darker than any lit part), and the darkest occlusion at contact. A cast shadow is sharp at its base and softens and widens away from the caster | book: Gurney CL pp. 46-47, 50 |
| Texture | Texture shows most in the half-tone next to the terminator, little in full light, almost none in shadow. Even texture everywhere is a rendering tell | book: Gurney CL p. 47 |
| Highlights and rims | A highlight is a reflection of the source and takes its colour on paint, plastic, skin, wood and glass; on metal it takes the metal's colour too (see Material cues); pure white is rare. A rim needs a source behind and a dark ground, takes a lighter version of the local colour, and varies in width | book: Gurney CL pp. 60, 162-165 |
| Backlit thin things | Leaves, sails and ears lit from behind are the most saturated notes in the scene | book: Gurney CL pp. 152-155 |
| Bright sources | A strong light wears a halo of its own colour that eats into nearby edges; starbursts, rings and hexagons are camera artefacts, not vision | book: Gurney CL p. 166 |
| One plan | Every element obeys one lighting plan: same side, same colour, same hardness. Two light directions in one composite is an integrity failure | book: Gurney CL p. 210; IR p. 72 |
| Photo look | Shadows clipped to black, highlights to white, weak colour shifts, snapshot framing, stiff gesture, random detail: the marks of copying a photo, and common in images trained on photos | book: Gurney CL pp. 170-171; IR pp. 64-65 |

## Material cues

How a surface's light says what it is made of. Use them to check a render or a painting, and to name a material in a prompt.

| Check | What to look for | verified |
|---|---|---|
| Metal or not | Non-metals (paint, plastic, skin, wood, glass) reflect the light's own colour in their highlights; metals tint highlights and reflections with their own colour and show almost no diffuse colour. A white highlight on gold, or an orange one on white plastic under white light, misreads the material | book: CGPP §14.9.3 p. 361, §27.8.1 p. 728 |
| Grazing angles | Glossy non-metals reflect more toward grazing: a polished floor mirrors the far end and shows its own colour near the viewer; even matte paint and cloth look shinier at grazing | book: CGPP §27.8.1 pp. 727-728 |
| Highlight size | Smoother is smaller and brighter, rougher broader and dimmer. A large, very bright highlight contradicts itself | book: CGPP §14.9.3 pp. 359-361 |
| Soft materials | Skin, wax, marble and milk carry light under the surface: the shadow edge softens and warms (red on skin), colour bleeds within the object | book: CGPP §27.13.2 pp. 738-739 |
| Coloured glass and water | Transmitted colour deepens with thickness: thick parts darker and more saturated, thin edges paler | book: CGPP §14.10.3 p. 368 |
| Grounding | A contact shadow decides whether an object touches the surface; even a faint, roughly shaped one does it. None reads as floating | book: CGPP §5.6 pp. 112-113 |

## Atmosphere and distance

| Check | What to look for | verified |
|---|---|---|
| Order of change | With distance, darks lighten and turn blue first, lit sides grey, warm colours dull fastest, and light-shadow contrast shrinks until far forms are flat pale shapes (`no_recession` when it does not happen; the band proxy is weak) | book: Gurney CL pp. 176-179 |
| Lit air only | Haze appears only where lit air lies between; distant whites go warmer. Toward a low sun in dust, distance can be warmer than the foreground (`warm_distance` is right only there) | book: Gurney CL pp. 176-179 |
| Edges and depth | The eye focuses one plane at a time: farther edges soften where contours cross; in dim light nearly everything is soft except the brightest places | book: Gurney CL pp. 140-141 |
| Sky and water | A clear sky grades in two directions, lighter toward the horizon and away from the sun. Reflections in water are darker than the object and stretched vertically by ripples; water mirrors only at low angles. Shadows on snow take the sky colour | book: Gurney CL pp. 84, 198-205 |
| Beams and dapples | Sunbeams need a screen that darkens the backdrop, dust or vapour, and a view toward the sun. Dappled spots are images of the sun: round on level ground, stretched on slopes | book: Gurney CL pp. 190-193 |

## Colour

- Colour is relative (Albers): judge each colour against its neighbours. verified: yes ([evidence.md](evidence.md))
- Temperature is relative: a colour reads warm or cool against its neighbours, and interest comes from warm notes
  beside cool ones. A golden picture still needs a cool note somewhere (the top of the sky, up-facing shadows).
  Warm light usually gives cool shadows, but see Light logic: the brief can overrule it. verified: book (Gurney CL
  pp. 112-115)
- Gamut: describe which slice of the colour wheel the image uses and, more telling, what it leaves out (`aw.py
  gamut`: hue sectors, shape, cast). A gamut is a description of what the image does, not a grade. verified: book
  (Gurney CL pp. 124-131)
- Accent: a small area clearly unlike the rest, often near the complement, pulls the eye; place it on the subject or
  scatter it as seasoning, never as a stray competitor (`competing_accent`). verified: book (Gurney CL p. 118)
- Too much colour fails more often than too much grey: everything at full strength ("fruit salad", `fruit_salad`)
  is the commoner fault, and "mud" usually comes from poor value planning, not from the mixture. One strong colour
  backed by greys mixed from the picture's own colours holds together. verified: book (Gurney CL pp. 80-81, 106-107)
- No flat colour: large areas grade in hue, value and chroma (a clear sky, a lawn, a wall). verified: book (Gurney
  CL pp. 82-85)
- Saturation hierarchy: the most saturated area should be where attention belongs; uniform high saturation flattens the image and is a common AI tell. verified: no (practice; reward tuning drives oversaturation, R-20261021-5)
- Harmony is a choice, not a test. Itten's schemes generate palettes; they do not grade them. Itten's seven contrasts (hue, light-dark, cold-warm, complementary, simultaneous, saturation, extension) are useful names for what a palette is doing. verified: yes for the schemes' lack of evidence (B-F11); the list of contrasts is from *The Art of Color* (1961), no

## Gestalt and design principles

| Principle | Use in a critique | verified |
|---|---|---|
| Proximity | Things close together read as a group | no |
| Similarity | Same colour, shape or size read as related | no |
| Closure | The eye completes broken shapes; lost edges can work | no |
| Continuity | The eye follows a line or curve past interruptions | no |
| Figure-ground | Which shapes read as objects and which as space; ambiguity should be deliberate | no |
| Common fate | Things moving or pointing together group | no |
| Prägnanz | The simplest reading wins | no |
| Contrast, repetition, alignment, proximity | Robin Williams's four layout principles (*The Non-Designer's Design Book*), plus hierarchy, for graphic design, posters and UI art | no |
| Rhythm | Repeated intervals; a break in rhythm draws the eye | no |

## Media cues

Telling the medium from an image is a guess with a confidence level. A photograph hides surface: relief, sheen, paper texture, plate marks and the back of the sheet are often invisible, and a reproduction can flatten oil into something that looks like gouache. Say "looks like", give the cue, and say what would settle it (raking light, magnification, the back, the catalogue record).

### Drawing

- Graphite: grey sheen, smudge, indented lines. Charcoal: matte black, dusty edges, grain of the paper catching the stick. Ink: uniform dark line; pen line swells with pressure, brush line tapers. verified: no
- Construction: figures built from simple solids (Loomis, Bridgman, Vilppu teaching); line weight varies with light, overlap and distance. Uniform weight everywhere reads as traced or generated. verified: no (B-F21, memory)

### Painting

| Medium | Cues | verified |
|---|---|---|
| Oil | Impasto, wet-into-wet blending, transparent glazes, craquelure on old work | no (B-F21) |
| Acrylic | Hard edges from fast drying, less blending, plastic sheen | no |
| Watercolour | Transparency, white paper as the lights, blooms and backruns, granulation | no |
| Gouache | Opaque, matte, flat colour areas | no |
| Egg tempera | Hatched strokes, no wet blending, often on gold-ground panels | no |
| Fresco | Matte surface, seams between day sections (giornate), limited lime-fast palette | no |
| Digital | Perfectly even gradients, layer-blend glows, repeated brush stamps; AI images add melted detail, inconsistent light and text errors | no |

### Sculpture

Subtractive (carving: tool marks, chisel facets), additive (modelling: thumb and tool marks in clay or wax), cast (lost-wax or sand: seams, patina, chasing), constructed or assembled. Judge silhouette from several views, mass and weight, surface against form, and the base. A single photo shows one view only; say so. verified: no (B-F21)

### Printmaking

| Process | Cues | verified |
|---|---|---|
| Relief (woodcut, linocut, wood engraving) | Large solid blacks, ink squeezed to a rim at line edges, embossing on the back, no plate mark | yes, B-F16 (Wellcome cataloguing guide) |
| Intaglio (engraving, etching, drypoint, aquatint, mezzotint) | Plate mark (can be trimmed or faked); line in engraving and etching, tone in aquatint and mezzotint; engraved lines swell and taper, etched lines are even with blunt ends, drypoint has a velvety burr | partly: the families yes (B-F16), line cues no |
| Lithograph | Flat ink, crayon grain | yes, B-F16 |
| Screenprint | Flat opaque ink layers, possible mesh texture | yes, B-F16 |
| Photomechanical reproduction | A regular dot or square pattern under magnification (halftone, offset): not an original print | yes, B-F16 |

Reference: Bamber Gascoigne, *How to Identify Prints* (1986, 2004).

## Critique frameworks

- **Feldman's four steps** (Edmund Feldman, *Art as Image and Idea*, 1967): describe, analyse, interpret, judge, in that order. Judgement comes last and rests on the first three. verified: no (standard text, B-F21)
- **Carroll's criticism as reasons** (Noël Carroll, *On Criticism*, 2009): criticism is evaluation backed by reasons; its parts are description, classification, contextualisation, elucidation, interpretation and analysis, all in the service of evaluation. Classification matters: judge a work by the category it belongs to (a Ming cup by its ware, a sprite by pixel-art rules), not by the wrong one. verified: yes for the components as summarised in B-F18; the book itself not read
- **Four kinds of claim**: craft or perceptual (testable against the image), historical (needs evidence), philosophical (argued), interpretive (better or worse readings). Name which kind each claim is. verified: yes, B-F18
- **Studio crit and Liz Lerman's Critical Response Process**: statements of meaning first, then the artist's questions, then neutral questions, then opinions with permission. Useful when the user made the work and wants feedback rather than a verdict. verified: no

## The critique procedure (ArtCoT)

ArtCoT (Jiang and Chen 2025) raised agreement with experts by 29-56% over plain answers; free chain-of-thought lowered it and filled answers with "feels" and "somewhat". The critic pass mattered most. verified: yes, R-20261021-4

1. **Cold read** before the brief: what the image shows, at thumbnail size and in greyscale, and the first thing the eye lands on.
2. **Describe**: subject, medium guess with confidence, value structure, palette, composition, style traits. Concrete, no judgement yet.
3. **Critic pass**: re-check each description and each planned claim against a visible region ("upper left", "the left hand", "the horizon at about one third") and against the brief or the tradition whose criteria apply. Drop any claim that cannot point at something.
4. **Verdict**: the top two or three issues, each with its location and one fix. Strengths only when specific. Say whose criteria the verdict uses.

Selectivity matters: models comment on every aspect and repeat themselves, while people pick the few that count (R-20261021-4). Banned without a pointed-at feature: "looks good", "feels", "somewhat", "evokes a sense of". A proud framing from the user ("my best work") changes nothing; every critique names at least one concrete fault or says plainly that it found none worth fixing and why.
