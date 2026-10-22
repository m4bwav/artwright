# Movements and periods

A lookup table of art movements and periods, each with traits you can check in an image, so a style label comes with evidence.

Checked 2026-10-21

Back to [SKILL.md](../SKILL.md).

## How to use it

1. Answer every "is this X?" or "does this contain X?" with one of `member | influenced | no evidence`. Never a bare yes or no.
2. List the row's traits you **see** and the traits you **do not see**, each tied to a region of the image ("faceted planes, upper left"; "no collage elements").
3. Name the neighbours you considered from the `Confusable with` column and say which trait ruled each one out. Vision models are about 53% right on WikiArt styles zero-shot and mix up exactly these neighbours: Baroque, Rococo, Neoclassicism and Romanticism; Impressionism, Post-Impressionism and Expressionism; Colour Field, Abstract Expressionism and Minimalism (R-20261021-6).
4. A right label can come for the wrong reason (about 10% of the concepts behind correct predictions were irrelevant to art historians), so the trait list is the answer, not the label (R-20261021-6).
5. Never use a filename, title or artist name as evidence. Strip them first.
6. A missing Wikidata movement tag (P135) is **not** evidence: only 14,508 of 1,085,204 painting items carry one (about 1.3%) (R-20261021-6). Use tags to confirm a label, never to refute one.
7. Say which tradition's criteria you are applying. Models score Western art higher than non-Western art (R-20261021-6); use the parallel tracks below and [traditions.md](traditions.md) rather than forcing a Western label.
8. Dates are approximate and contested at the edges. A row's date is a guide to plausibility, not a test.

Columns: **QID** is the Wikidata item; **AAT** is the Getty Art and Architecture Thesaurus ID as recorded on Wikidata (property P1014), `-` when Wikidata carries none (Getty's own SPARQL refuses scripted clients, R-20261021-13); **v** is `yes` when this session fetched the QID (Wikidata SPARQL and the Wikipedia article linked to it) and a source stating the dates (Wikidata P571/P580/P582 or the linked article's lead), `no` otherwise. Traits are drafted from art-historical knowledge and are **not** individually sourced in any row; treat them as a checklist, not a citation.

Sources for every QID, AAT and date check: https://query.wikidata.org/sparql (labels, descriptions, P1014, P571, P580, P582) and https://en.wikipedia.org/w/api.php (lead sections with `pageprops.wikibase_item`), both fetched 2026-10-21.

## Western spine

| Movement | Dates | Region | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|---|
| Cave painting | at least 67,800 BP on | worldwide | rock surface; red/black/ochre mineral pigment; hand stencils; animals in profile; no ground line or frame | Aboriginal rock art, San rock art | Q214334 | 300178308 | no |
| Ancient Egyptian | c. 3100 BCE–4th c. CE | Egypt | composite pose (frontal eye, profile head and legs); register bands; hierarchic scale; hieroglyphs; flat colour, black outline | Assyrian relief, Art Deco revival | Q318394 | - | yes |
| Ancient Greek (Archaic, Classical) | c. 900–146 BCE | Greece | black- or red-figure vases; contrapposto; idealised nude; meander borders | Hellenistic, Roman, Neoclassicism | Q1747618 | - | yes |
| Hellenistic | 323–30 BCE | E. Mediterranean | twisting dramatic bodies; strong emotion; old age and realism; deep-cut drapery | Classical Greek, Roman, Baroque sculpture | Q221375 | - | yes |
| Roman | c. 200 BCE–400 CE | Roman Empire | veristic portrait heads; fresco with illusionistic architecture; mosaic floors; Latin inscriptions | Greek, Neoclassicism | Q3354732 | - | yes |
| Byzantine | c. 330–1453 | E. Mediterranean | gold ground; frontal elongated saints; no cast shadows; tesserae mosaic; Greek letters | Romanesque, Russian icons, Gothic | Q211884 | - | yes |
| Romanesque | c. 1000–1200 | Europe | heavy outlines; stylised drapery folds; figures squeezed to fit frames; flat bright colour; round arches | Byzantine, Insular, Gothic | Q46805 | 300020768 | yes |
| Gothic | c. 1140–1530 | Europe | pointed arches and tracery; S-curve figures; stained-glass colour; gold leaf; elongated forms | International Gothic, Romanesque | Q46825 | 300020775 | yes |
| International Gothic | late 14th–early 15th c. | Europe | courtly elegance; flowing gilt drapery; decorative detail over space; tiny naturalistic flora | Gothic, Early Netherlandish | Q867769 | 300020786 | yes |
| Early Netherlandish | c. 1420–1560 | Low Countries | oil glaze jewel colour; microscopic detail; mirrors and window views; still interiors | Northern Renaissance, International Gothic | Q443153 | 300387753 | yes |
| Italian Renaissance (early) | late 13th–16th c. | Italy | linear perspective with vanishing point; classical architecture; modelled volume; tempera or fresco | High Renaissance, Gothic | Q2914470 | - | yes |
| High Renaissance | c. 1490–1527 | Italy | pyramidal composition; sfumato; balanced calm figures; idealised anatomy | Mannerism, Early Renaissance, Neoclassicism | Q1474884 | 300021142 | yes |
| Northern Renaissance | late 15th–16th c. | N. Europe | oil detail; landscape panoramas; print-like line; everyday objects as symbols | Early Netherlandish, Mannerism | Q610877 | 300252246 | yes |
| Mannerism | c. 1520–1600 | Italy, then N. Europe | elongated limbs; serpentine poses; acid colour; crowded or ambiguous space | High Renaissance, Baroque | Q131808 | 300021144 | yes |
| Baroque painting | c. 1600–early 18th c. | Europe | strong diagonals; dramatic light; movement and climax; rich dark ground | Tenebrism, Rococo, Mannerism | Q808561 | - | yes |
| Tenebrism | 17th c. | Italy, Spain, Utrecht | near-black background; single hard light source; figures cut out of darkness | Baroque, chiaroscuro photography | Q1464842 | 300343524 | no |
| Dutch Golden Age | 17th c. | Dutch Republic | quiet interiors with window light; still life; flat polder landscapes with big skies; group portraits | Baroque, Early Netherlandish | Q2352880 | - | yes |
| Rococo | c. 1730–1780 | France, Europe | pastel palette; S- and C-curves; frothy foliage; playful aristocratic scenes | Baroque, Neoclassicism | Q122960 | 300021155 | yes |
| Neoclassicism | c. 1760–1830 | Europe, US | crisp outlines; frieze-like staging; classical dress and columns; smooth finish; restrained colour | Academic art, High Renaissance, Romanticism | Q14378 | 300021477 | yes |
| Romanticism | late 18th–mid 19th c. | Europe | sublime nature; storms and ruins; loose expressive brushwork; small figure against vast scene | Baroque, Realism, Hudson River School | Q37068 | 300172863 | yes |
| Realism | 1840s–1880s | France, Europe | ordinary workers; muted earth palette; unidealised bodies; large canvases for low subjects | Academic art, Barbizon, Impressionism | Q2642826 | 300172861 | yes |
| Academic art | 16th–early 20th c. (peak 19th) | Europe | invisible brushwork; perfect anatomy; history and myth subjects; licked finish | Neoclassicism, Pre-Raphaelite | Q189458 | 300055954 | yes |
| Pre-Raphaelite | from 1848 | England | hard-edged detail everywhere; saturated jewel colour; medieval or literary subjects; pale women with masses of hair | Academic art, Symbolism | Q184814 | 300021225 | yes |
| Impressionism | 1860s–1880s | France | visible broken strokes; outdoor light; coloured shadows; cropped casual views; no black | Post-Impressionism, Barbizon | Q40415 | 300021503 | yes |
| Neo-Impressionism (Pointillism) | from 1886 | France, Belgium | dots of pure colour; optical mixing; static ordered composition | Impressionism, Divisionism, halftone print | Q150091 | 300021505 | yes |
| Post-Impressionism | c. 1886–1905 | France | bold outlines; flat colour areas; structural brushwork; emotional colour | Impressionism, Fauvism, Expressionism | Q166713 | 300021508 | yes |
| Symbolism | c. 1857 (literature)–1900 | France, Belgium, Europe | dreamlike myth; femme fatale; muted mystical palette; flattened decorative space | Pre-Raphaelite, Art Nouveau, Surrealism | Q164800 | 300021514 | yes |
| Art Nouveau | 1890–1910 | Europe, US | whiplash curves; plant and flower motifs; flat decorative outline; long-haired women | Art Deco, Symbolism, Arts and Crafts | Q34636 | 300021430 | yes |
| Fauvism | 1904–1908 | France | arbitrary pure colour (green faces, red trees); flat patches; raw canvas showing | Expressionism, Post-Impressionism | Q166593 | 300021300 | yes |
| Expressionism | c. 1905–1920s | Germany, N. Europe | distorted figures; harsh clashing colour; jagged woodcut line; anxiety | Fauvism, Neo-expressionism | Q80113 | 300021502 | yes |
| Cubism | from 1907 | France | faceted planes; several viewpoints at once; flattened picture plane; muted browns and greys (analytic); collage, lettering (synthetic) | Futurism, Orphism, Precisionism, Cézanne | Q42934 | 300021495 | yes |
| Orphism | c. 1912–1914 | France | cubist faceting with bright prismatic colour; concentric discs | Cubism, Futurism, Synchromism | Q519443 | 300134101 | yes |
| Futurism | from 1909 | Italy | repeated forms showing motion; speed lines; machines and cities; force lines | Cubism, Vorticism | Q131221 | 300021374 | yes |
| Suprematism | from 1913 | Russia | flat geometric shapes floating on white; few colours; diagonal tilt | Constructivism, De Stijl | Q191970 | 300021405 | yes |
| Constructivism | from 1913–1915 | Russia, USSR | photomontage; red, black and diagonal type; industrial materials | Suprematism, Bauhaus | Q207103 | 300021393 | yes |
| De Stijl | 1917–1932 | Netherlands | black horizontal and vertical grid; primary colours plus white; asymmetric balance | Bauhaus, Suprematism | Q207445 | 300021259 | yes |
| Bauhaus | 1919–1933 | Germany | sans-serif type; simple geometry; primary colours; function-led layout | De Stijl, Constructivism, Swiss Style | Q124354 | 300021432 | yes |
| Dada | from 1916 | Zurich, Europe, NY | collage of found print; absurd juxtaposition; readymades; nonsense type | Surrealism, Constructivism | Q6034 | 300021500 | yes |
| Surrealism | from 1920s | France, international | dream scenes rendered realistically; impossible juxtaposition; melting or hybrid objects; deep empty plains | Symbolism, Magic realism, Dada | Q39427 | 300021512 | yes |
| Art Deco | 1910s–1930s | France, international | stepped and sunburst geometry; chrome and gold; streamlined symmetry | Art Nouveau, Bauhaus | Q173782 | 300021426 | yes |
| New Objectivity | 1920s | Germany | cold sharp realism; satirical portraits; hard light; urban types | Magic realism, Precisionism | Q160218 | 300056541 | yes |
| Precisionism | 1920s–early 1930s | US | clean industrial forms; smooth planes; crisp edges; few or no people | Cubism, New Objectivity | Q1578378 | - | yes |
| Socialist realism | from 1932–1934 | USSR, then bloc | heroic workers; upward gaze; red banners; optimistic legible scenes | Academic art, Mexican muralism | Q180902 | 300021404 | yes |
| Abstract Expressionism | 1940s–1950s | US | large scale; gestural drips or slashes; all-over field; no figure | Tachisme, Colour Field | Q177725 | 300022099 | yes |
| Colour Field | 1940s–1950s on | US | large flat or stained areas of colour; few edges; soaked canvas | Abstract Expressionism, Minimalism, Hard-edge | Q1164982 | 300022120 | yes |
| Pop art | mid-1950s on | UK, US | mass-media imagery; Ben-Day dots; flat commercial colour; repetition | Neo-Dada, Superflat | Q134147 | 300022205 | yes |
| Op art | 1960s | Europe, US | high-contrast patterns that seem to move; moiré; precise geometry | Hard-edge, Kinetic art | Q182331 | 300022195 | yes |
| Hard-edge painting | from 1959 | US | sharp boundaries between flat colours; no texture | Colour Field, Minimalism | Q369418 | 300022175 | yes |
| Minimalism | 1960s | US | single units or grids; industrial finish; no illusion; monochrome | Colour Field, Conceptual art | Q173436 | 300065758 | no |
| Photorealism | late 1960s on | US | painting that reads as a photo; reflections; lens effects; urban surfaces | Hyperrealism, Pop art | Q939559 | 300022201 | yes |
| Conceptual art | 1960s on | international | text as image; documents, diagrams, instructions; low visual craft | Minimalism, Fluxus | Q203209 | 300264827 | yes |
| Land art | 1960s–1970s | US, UK | earth, rock or landscape as material; documented by aerial photo | Minimalism | Q326478 | 300047857 | yes |
| Neo-expressionism | late 1970s–1980s | Germany, Italy, US | crude figuration; thick impasto; large canvases; raw colour; myth and history | Expressionism, Street art | Q589655 | 300022189 | yes |
| Pictures Generation | 1974–1984 | US | appropriated media images; rephotography; cool deadpan; text over image | Pop art, Conceptual | Q115045796 (the 2009 Met exhibition) | - | yes |
| Young British Artists | from 1988 | UK | provocative objects; vitrines; shock subjects; installation | Conceptual, Neo-pop | Q516316 | 300263412 | yes |
| Street art | 1980s on | worldwide | spray paint; stencils; walls and street furniture; tags | Neo-expressionism, Pop | Q17516 | 300056477 | no |
| Postmodern art | from 1960s | international | quotation and pastiche; mixed styles; irony; text and image | Pop, Conceptual | Q3318563 | - | yes |
| Relational art | 1990s | international | photos of social events or meals; people as the material | Conceptual, Fluxus | Q2566149 | 300391190 | yes |
| Post-Internet | from 2006 | international | screen-native imagery; stock and render aesthetics; branded surfaces | Vaporwave, Net.art | Q17299972 | - | yes |

## China

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Shan shui (monumental landscape) | peak Song, 10th–13th c. | towering mountains; mist bands separating planes; tiny figures; ink texture strokes; vertical scroll | Literati landscape, Kanō | Q516583 | 300387301 | no |
| Gongbi | Tang on | fine even outlines; filled flat colour; meticulous detail on silk | Bird-and-flower, Persian miniature | Q5581733 | 300310140 | no |
| Bird-and-flower | Tang origin, Song peak | single branch with birds; empty ground; precise or loose ink | Gongbi, Rinpa | Q2566458 | 300266169 | yes |
| Literati painting (Southern School) | named c. 1600; practice older | dry brush; sparse composition; poem and seals on the image; ink over colour | Zhe school, Four Wangs | Q1142000 | 300106501 | no |
| Zhe school | 15th c. (early Ming) | bold wet brushwork; corner composition (Ma–Xia); dramatic contrasts | Southern Song academy, Literati | Q1150941 | - | yes |
| Wu School | 15th–16th c. | literati landscapes; gentle colour; scholars in gardens | Literati, Four Wangs | Q558875 | - | yes |
| Four Wangs (Orthodox) | 17th c. | dense layered landscape built from old masters' brush types | Wu School, Literati | Q3099098 | - | yes |
| Shanghai School | mid-19th–early 20th c. | bright colour with ink; flowers, figures; commercial scale | Literati, Lingnan | Q15896937 (Haipai culture item) | - | no |
| Political Pop | c. 1989–1990s | Cultural Revolution posters mixed with brand logos; flat pop colour | Pop art, Socialist realism | Q2462197 | - | no |

## Japan

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Yamato-e | from 12th c. | blown-off-roof interiors; mineral colour; narrative handscroll; stylised faces | Kara-e, Tosa school | Q597365 | 300018589 | yes |
| Kanō school | late 15th c.–1868 | gold-leaf screens; strong ink outlines; Chinese themes; tigers, pines | Rinpa, Chinese academic | Q252801 | 300018653 | yes |
| Rinpa | from 17th c. | gold or silver ground; bold flat flowers and waves; tarashikomi pooled ink | Kanō, Art Nouveau | Q3179819 | 300106734 | yes |
| Ukiyo-e | 17th–19th c. | woodblock line; flat colour areas; actors, courtesans, landscapes; cartouche text | Shin-hanga, Art Nouveau posters | Q185905 | 300106769 | yes |
| Shin-hanga | 1915–1950 | woodblock with Western light and shadow; soft gradients; night and rain scenes | Ukiyo-e, Sōsaku-hanga | Q842183 | 300262954 | yes |
| Nihonga | from Meiji (1868–1912) | mineral pigment on silk or paper; soft outline; Japanese subjects | Yōga, Rinpa | Q1989975 | 300114441 | yes |
| Gutai | 1954–1972 | action traces; mud, feet, torn paper; performance photos | Abstract Expressionism, Art informel | Q1028956 | - | yes |
| Mono-ha | late 1960s–1970s | raw stone, steel, wood set in simple relations; no image | Minimalism, Arte Povera | Q3321083 | - | no |
| Superflat | from 2000 | anime and manga flatness; no depth; dense cute motifs; commercial gloss | Pop art, Ukiyo-e | Q1444581 | 300266360 | yes |

## South Asia

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Gandhara (Greco-Buddhist) | 1st–5th c. CE | Buddha with Greek drapery folds; wavy hair; grey schist | Mathura, Roman | Q1008014 | - | yes |
| Mathura | from 2nd c. BCE | red sandstone; fleshy rounded bodies; thin clinging drapery | Gandhara, Gupta | Q28173968 | - | yes |
| Gupta | c. 300–550 CE | serene downcast eyes; transparent wet drapery; balanced calm | Mathura, Pala | Q283562 | - | yes |
| Chola bronze | c. 850–1250 | lost-wax bronze; dancing Shiva in ring of fire; slender poised limbs | Pala bronze, Khmer | Q5260101 | - | yes |
| Mughal painting | 16th–19th c. | naturalistic portraits; Persian-style borders; court and hunt scenes; fine detail | Persian miniature, Rajput, Company | Q1049336 | - | yes |
| Rajput painting | late 16th–mid 19th c. | flat saturated colour; Krishna themes; strong profiles; ornamental borders | Mughal, Pahari | Q2988788 | - | yes |
| Pahari painting | early 17th–mid 19th c. | lyrical line; cool palette; hill landscapes; Basohli or Kangra types | Rajput, Mughal | Q3631050 | 300018997 | yes |
| Company painting | 18th–19th c. | watercolour on paper; Indian trades and costumes for British buyers; European shading | Mughal, botanical illustration | Q861297 | 300018959 | yes |
| Bengal School | early 20th c. | wash technique; soft muted tones; Indian myth; Japanese influence | Nihonga, Pahari | Q948504 | - | yes |
| Progressive Artists' Group | from 1947 | modernist distortion; bold colour; Indian subjects in European idioms | Expressionism, Cubism | Q4940574 | - | yes |
| Madhubani | traditional; on paper from 1960s | double outlines; no empty space; fish, peacocks, deities; natural dyes | Gond, Kalighat | Q2547125 | - | no |

## Islamic world

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Islamic geometric pattern (incl. girih) | from 9th c. | star polygons (6- to 16-point); interlaced strapwork; repeat tiling | Celtic knotwork, Op art | Q3325173 | - | yes |
| Arabesque | from 9th c. | endless scrolling vine; split palmettes; no figures | Rococo scroll, Art Nouveau | Q186599 | 300010206 | yes |
| Kufic script | from late 7th c. | angular strokes; long horizontals; square or foliated forms | Naskh, Square Kufic tiles | Q29647 | 300194434 | yes |
| Persian miniature | 13th c. on; peak 15th–16th c. | high viewpoint; jewel colour; no cast shadow; text panels; gold sky | Mughal, Ottoman miniature | Q678664 | - | yes |
| Ottoman miniature | c. 15th–18th c. | flatter, documentary scenes; processions; less landscape | Persian miniature | Q268639 | - | no |
| Iznik pottery | late 15th–17th c. | cobalt blue, turquoise and tomato red on white; tulips, carnations | Chinese blue-and-white, Delft | Q2696793 | 300021623 | yes |
| Hurufiyya | later 20th c. | Arabic letters as abstract forms; modernist painting | Abstract Expressionism, Lettrism | Q55614094 | - | yes |

## Africa

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Nok | c. 1500–1 BCE (range disputed) | terracotta heads; triangular or D-shaped eyes with pierced pupils; elaborate hair | Ife | Q927291 | 300015822 | yes |
| Ife (Yoruba) | c. 12th–15th c. | naturalistic copper-alloy and terracotta heads; fine vertical face striations | Benin, Nok | Q8055874 | - | no |
| Benin bronzes | from 14th c. | cast plaques with court figures in high relief; hierarchic scale; coral-bead regalia | Ife | Q248101 | - | yes |
| Nkisi (Kongo) | 19th–20th c. collected | wooden figure with nails or blades; medicine pack at belly; mirror | Songye power figures | Q1460155 | 300262566 | no |
| Ethiopian Christian painting | 4th c. on | large almond eyes; frontal figures; bright flat colour; Ge'ez text | Byzantine, Coptic | Q2688661 | - | no |
| San rock art | thousands of years to 19th c. | eland and human figures in red ochre; trance scenes; fine-line brushwork | Cave painting, Aboriginal rock art | Q7354778 | - | no |
| Tingatinga | from 1960s | enamel paint on board; bright flat animals; repeated patterned ground | Naive art, Pop | Q1536024 | - | no |

## Oceania

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Indigenous Australian art | tens of millennia on | dot fields; concentric circles; tracks; ochre or acrylic | Op art, Pointillism | Q420716 | 300264787 | no |
| Papunya Tula (Western Desert acrylic) | from 1972 | acrylic dot painting on canvas; map-like aerial structure | Indigenous rock art, Op art | Q18005 | - | yes |
| X-ray style | rock art; recent bark painting | animals with skeleton and organs shown; cross-hatching (rarrk) | Cave painting | Q60762307 | - | no |
| Māori carving (whakairo) | pre-contact on | spirals (koru); paua-shell eyes; surface fully patterned; red ochre | Northwest Coast, Celtic | Q7990459 | - | no |
| Tapa cloth | traditional | bark cloth; stamped or stencilled geometric bands in brown and black | Kente, Islamic geometric | Q972724 | 300072237 | no |

## The Americas

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Olmec | c. 1200–400 BCE | colossal basalt heads; helmets; jade; down-turned "were-jaguar" mouths | Maya, Aztec | Q16488887 | - | yes |
| Maya | Classic c. 250–950 CE | profile figures with glyph columns; sloping foreheads; polychrome vases | Aztec, Olmec | Q1626940 | - | yes |
| Aztec | c. 1300–1521 | blocky stone sculpture; skulls and serpents; codex figures with thick outlines | Maya, Mixtec | Q2864582 | - | yes |
| Moche | c. 100–800 CE | stirrup-spout portrait vessels; fine-line red-on-cream painting | Nazca, Chimú | Q208188 | 300017287 | yes |
| Northwest Coast | traditional | formline; ovoids and U-forms; black and red; split symmetric animals | Māori carving | Q7059995 | 300017594 | no |
| Mexican muralism | from 1920s | huge public walls; history and labour; monumental figures; fresco | Socialist realism, Social realism | Q938864 | 300107850 | yes |

## 2D digital art

These rows describe looks, often with fuzzy dates; pixel checks live in the artwright-pixel skill.

| Movement | Dates | Visible traits | Confusable with | QID | AAT | v |
|---|---|---|---|---|---|---|
| Pixel art | 1970s on | visible square pixels on one grid; small palette; hand-placed clusters; no blur | AI "fake pixel", low-res photo | Q811179 | - | no |
| ASCII art | 1960s on | images built from text characters; monospace grid | Concrete poetry, ANSI art | Q193097 | - | yes |
| Demoscene | early 1980s on | copper bars; plasma, starfields; logos with gradients; low-res tracker-era palette | Pixel art, Synthwave | Q824340 | - | yes |
| Net.art | mid-1990s | browser windows; HTML errors; early web colours and GIFs | Glitch, Post-Internet | Q2553758 | - | yes |
| Glitch art | 2000s on (with earlier roots) | datamosh smears; pixel sorting; RGB channel offset; compression blocks | Vaporwave, Net.art | Q5569949 | - | no |
| Vaporwave | early 2010s | pink and teal; Greek busts; Windows 95 UI; Japanese text; grid floor | Synthwave, Frutiger Aero | Q15733887 | - | yes |
| Synthwave (outrun) | from 2000s | neon magenta and cyan; wireframe grid to horizon; striped setting sun; chrome type | Vaporwave, Demoscene | Q19938910 (music-genre item) | - | yes |
| Frutiger Aero | mid-2000s–early 2010s | glossy glass bubbles; water, sky and green leaves; humanist sans; lens flare | Y2K, Vaporwave | Q118114289 | - | yes |
| Flat design | 2010s | no gradients or shadows; solid colour blocks; simple icons | Bauhaus, Swiss Style | Q15266360 | - | no |
| Generative art | 1960s on | rule-made repetition with variation; plotter lines; flow fields | Op art, Glitch | Q1502032 | 300266042 | no |
