---
name: artwright
description: "Use whenever art or an image needs an artist's eye: critique a painting, drawing, print, sculpture, ceramic, illustration or 3D render; style or movement ('is this cubist'); art theory ('what is postmodernism'); art facts ('most expensive Ming vase', 'oldest painting'); 'is this AI-made'; an image's main colours; many images side by side on one contact sheet. aw.py measures, claims tie to regions, facts go through historywright. Ranking or brief fit: artwright-judge. Pixel art: artwright-pixel. Not brand palettes (brandwright) or website direction (sitewright-direction). Also 'refresh artwright'."
---

# artwright

Gives an agent an artist's eye: it describes what is there, names what works and what does not, ties every claim
to a visible region, and says whose criteria it applies. It judges, explains and directs; it never generates,
edits, models, or owns a brand (generation: comfyui-gen; meshes: polywright; video takes: cinewright-qc; brands:
brandwright; site direction: sitewright-direction).

Script: `scripts/aw.py` in this folder (Python 3.9+, standard library, Pillow optional; one JSON object per
command). Run it by its full path from the user's folder. `aw.py doctor` once per session says what decodes here.
Commands: [references/cli.md](references/cli.md).

## Step 0: freshness and route

Read `evergreen.json` at the plugin root ([MAINTENANCE.md](../../MAINTENANCE.md)); if it is past due or has a
contradiction, say so in one line and refresh after the task. Then route:

| Request | Go to |
|---|---|
| "Which is better", rank a batch, does it fit the brief, what to change in the prompt | artwright-judge |
| Pixel art, sprites, tiles, "is this real pixel art" | artwright-pixel |
| Add or fix knowledge, the user's taste record, calibration labels | artwright-curate |
| Critique, analysis, style or movement, theory, art facts | this skill, below |

## Image handling (every image, before any Read)

- `aw.py info <img>` first: size and token cost. Never Read an image larger than 1568 px on its long edge; fit it:
  `aw.py fit <img> -o <out.png> --long 1024` (about 1,300 tokens).
- Detail goes by crop (`--crop x,y,w,h` or `--cell 3x3:4`), never by sending the whole image larger.
- Several images, or "show them side by side": one contact sheet (`aw.py sheet <files or folder> -o sheet.png`),
  then one Read of it. Never one Read per image, never a hand-written PIL or ImageMagick script.
- Colours ("main colours", "palette", "how much of it is red"): `aw.py palette <img>` gives the colours and their
  shares; answer from its JSON, not by eye or a one-off script.
- Numbers before pixels: `aw.py stats <img>` (value, contrast, colourfulness, edges, symmetry, balance). They
  describe; none is a beauty score ([references/evidence.md](references/evidence.md)).
- An unchanged file with the same rubric is never judged twice: `aw.py cache get <img>` first.

## Critique of one work

1. **Cold read, before the brief or the user's framing.** What the image shows, the three things the eye goes to
   first, the medium as it appears. Missing the subject is the first finding.
2. **Formal analysis** with [references/craft.md](references/craft.md): the greyscale read (`aw.py stats --notan`),
   value groups, focal point, eye path, balance, colour and temperature, line, edges, space, rendering integrity.
3. **Critic pass.** Each claim names a region ("upper left, the sky band", "the right hand") and a reason. Drop
   any claim that cannot point at something. No "looks good", no "feels", no "somewhat".
4. **Verdict:** the top two or three issues, most important first, one concrete fix each; then what works and
   should be kept. Whose criteria: the brief, a named tradition, or the user's own past picks (artwright-curate).

Proud framing ("my best work, isn't it perfect?") changes nothing: the faults are still named, concretely.
A brief that asks for rough, naive or "ugly" work is judged on whether it achieves that, not on polish.

## Style and movement questions

Use [references/movements.md](references/movements.md). Answer `member`, `influenced` or `no evidence`, never a
bare yes or no:

- list the visible traits seen and the expected traits missing;
- name the neighbouring movements considered and why they lost (Cézanne is proto-cubist: `influenced`, not cubist;
  Mondrian 1927 is De Stijl; Boccioni is Futurist);
- a missing Wikidata movement tag is not evidence (about 1.3% of painting items carry one);
- vision models confuse neighbouring movements and score non-Western art lower: for non-Western work, use the
  tradition's own terms ([references/traditions.md](references/traditions.md)) and say when a row is unverified.

## Theory questions

Answer from [references/theory.md](references/theory.md) with its sources: date the idea, name its key figures,
say what it reacted against, and give the question it lets you ask of an image. Borrowed terms (wabi-sabi, rasa)
keep their own sense; applied loosely, say so.

## Fact questions (oldest, largest, most expensive, first, who made it)

Run the superlative procedure in [references/market.md](references/market.md):

1. Name the readings ("Ming" strictly, or any period; painting or any cave art; public auction or private sale).
2. For each reading, the current holder, then a search of the year to date for a newer record.
3. Check the category: dynasty and reign (Ming is 1368–1644; Qianlong is Qing), medium, attribution qualifier.
4. Prices: currency, date, hammer or premium, public or private, paid or unpaid.
5. Hand historywright a pinned question for the dated facts and two independent sources; Guinness and Wikipedia
   are finders, never one of the two. With historywright absent, fetch the sources yourself to the same standard.
6. End with a confidence line, a sources-disagree note, and `Market qualifiers:` on any price. Minimum ages are
   "at least".

Ceramics: [references/ceramics.md](references/ceramics.md); a reign mark never dates a piece on its own.
Law and AI art (copyright, disclosure): [references/law.md](references/law.md), dated, not legal advice.

## Guards (every skill in this plugin)

- No attribution, authentication or valuation from pixels ("is this a real Rubens", "what is it worth"):
  decline with the reason, and say what would answer it (provenance, technical study, a specialist).
- No "is this AI-made" from pixels: Claude cannot tell, so open with that, not with yes or no. Describe visible
  traits, never as proof. Only provenance answers it (a museum record you fetched, C2PA or other embedded metadata);
  a file name is not provenance. When a fetched record decides it, say so; otherwise say what would.
- A living artist named in a prompt or a request for "in the style of" becomes descriptive traits (medium,
  palette, line, subject, era), with one line saying so. Never ask for the name. Public-domain masters,
  movements and studio genres may be named.
- The golden ratio is never a reason; thirds is a description, never a score.
- An absolute score (1–10) only when asked, anchored by three labelled references, with the warning that scores
  bunch at the top.

## Output

Lead with the answer. Then the evidence (traits, regions, numbers from aw.py with the command that made them),
then fixes or readings. Every fact carries its source. Say plainly what was not checked.

## Maintenance

Shared evergreen unit at the plugin root: [evergreen.json](../../evergreen.json),
[RESEARCH.md](../../RESEARCH.md), [CHANGELOG.md](../../CHANGELOG.md), [LEARNINGS.md](../../LEARNINGS.md),
[TESTS.md](../../TESTS.md), [MAINTENANCE.md](../../MAINTENANCE.md). Knowledge files carry `verified` flags and
dates; `law.md` and the judge's model profiles are volatile (recheck every 60–90 days). Edits go through
artwright-curate.
