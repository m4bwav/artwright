# Creation pass 2026-10-21: A. art history and theory (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation (no `last_checked`). Magnitudes are `n/a (initial)`. Live probes were one request each with a descriptive User-Agent (`artwright-research/0.1`), run on 2026-10-21. The pass was interrupted once by a session usage limit and resumed; one search and two fetches failed at that point and were retried.

## Findings (newest first)

### F1 · 2026-10-21 (probed) · The Met's v1 search is gone (HTTP 410); v1.1 is paginated and capped at 10,000
- What: `collectionapi.metmuseum.org/public/collection/v1/search?q=cubism` returns HTTP 410 with a JSON body: "retired on 2026-10-01 ... use /public/collection/v1.1/search, which is Elastic-backed and paginated via offset and limit." `v1.1/search?q=cubism&limit=2` returned `{"total":441,"objectIDs":[...]}`. The docs (metmuseum.github.io) say v1.1 was added 2026-09-04: `limit` defaults to 100 and goes up to 500, `offset + limit` cannot exceed 10,000, and the filters are unchanged (`q`, `isHighlight`, `title`, `tags`, `departmentId`, `isOnView`, `artistOrCulture`, `medium`, `hasImages`, `geoLocation`, `dateBegin`/`dateEnd`). `/v1/objects/{id}` still works (object 436535 returned 200, `isPublicDomain: true`). No key is needed, the rate limit is 80 requests per second, and the data is CC0. To enumerate the whole collection, use `/objects` or the CSV in `github.com/metmuseum/openaccess` (CC0, pushed 2026-10-19).
- Track: subject (sources)
- Affects: any aw.py museum route; any eval that hits the Met
- Magnitude: n/a (initial)
- Sources: https://metmuseum.github.io/, https://collectionapi.metmuseum.org/public/collection/v1/search?q=cubism (410 body), https://github.com/metmuseum/openaccess

### F2 · 2026-10-21 (probed) · Museum API status table
- What: one request each, today:

| Source | Endpoint | Key | Licence | Probe today |
|---|---|---|---|---|
| The Met | `collectionapi.metmuseum.org/public/collection/v1.1/search`, `/v1/objects/{id}` | none | CC0 (data and PD images) | 200 (v1 search: 410) |
| Art Institute of Chicago | `api.artic.edu/api/v1/artworks/search?q=&fields=` | none | data CC0; `description` field CC BY 4.0 | **403 Cloudflare challenge without an `AIC-User-Agent` header; 200 with one** |
| Cleveland Museum of Art | `openaccess-api.clevelandart.org/api/artworks/?q=` | none | per-record `share_license_status` (CC0 for most) | 200 (23 hits for "cubism") |
| Rijksmuseum | `data.rijksmuseum.nl/search/collection?title=` (Linked Art JSON-LD, `OrderedCollectionPage`), plus OAI-PMH, LDES, dumps, IIIF and a resolver | none stated | not stated on the docs index (historically CC0 for PD works, to confirm) | 200; **old `rijksmuseum.nl/api/en/collection` returns 410** |
| National Gallery of Art | `github.com/NationalGalleryOfArt/opendata` (CSV, no live API) | none | CC0 | repo pushed 2026-10-21 (daily), 843 stars |
| Smithsonian Open Access | `api.si.edu/openaccess/api/v1.0/search` | api.data.gov key | metadata CC0; media CC0 per item | 403 `API_KEY_MISSING` (expected) |
| Harvard Art Museums | `api.harvardartmuseums.org/object` | key | **non-commercial only, no caching beyond 2 weeks, 2,500 calls/day** | 401 (expected) |
| Europeana | `api.europeana.eu/record/v2/search.json` | `wskey` (historywright found demo key `api2demo` works) | rights per item | 401 without key |
| Getty Museum | `data.getty.edu/museum/collection/` (Linked Art) | none | CC0 with exceptions (per historywright) | root 200; `/object/search` 404 (wrong path; use the Linked Art activity stream or SPARQL) |
| Getty Vocabularies AAT/ULAN/TGN | `vocab.getty.edu/sparql(.json)`; monthly N-Triples dumps | none | ODC-By 1.0 | **403 to curl with a custom UA, twice**; XML services discontinued, final XML/relational sets 2026-01-30 |
| Paris Musées | `apicollections.parismusees.paris.fr/graphql` | token (per earlier reports; not confirmed) | CC0 for PD 2D works (about 150,000) | 200 GraphQL error asking for a query (endpoint alive) |
| National Palace Museum (Taipei) | open data portal `theme.npm.edu.tw/opendata` | none for downloads | Open Government Data Licence 1.0 / CC BY 4.0, attribution required | not probed (openaccess host did not resolve) |
| Wikidata | `query.wikidata.org/sparql` | none | CC0 | 200 |

- Track: subject (sources) and testing (probe routes)
- Affects: the aw.py `museum` or `lookup` subcommand and the sources reference file
- Magnitude: n/a (initial)
- Sources: probes above; https://github.com/harvardartmuseums/api-docs; https://data.rijksmuseum.nl/docs/; https://creativecommons.org/2020/01/10/paris-musees-releases-100000-works-into-the-public-domain/; https://theme.npm.edu.tw/opendata/?lang=2; https://www.getty.edu/research-conservation/tools-databases/vocabularies/data-services

### F3 · 2026-10-21 (probed) · Wikidata movement tags are sparse: 1.3% of paintings carry P135
- What: Wikidata has 1,085,204 items that are instances of painting (Q3305213). Only 14,508 of them have a movement (P135). There are 1,005 direct instances of "art movement" (Q968159), and 208 of those carry an AAT ID (P1014). The most-tagged movements are Art Nouveau (2,011), Early Netherlandish (1,898), Venetian school (738), abstract art (705) and academic art (613). The distribution reflects which batch uploads happened, not art history. A missing P135 therefore says nothing about a work. Use the tags to confirm a label, never to refute one.
- Track: subject (sources) and practice
- Affects: any "does this work belong to movement X" lookup; the eval for "is this cubist?"
- Magnitude: n/a (initial)
- Sources: https://query.wikidata.org/sparql (COUNT queries, 2026-10-21)

### F4 · 2026-10-21 (probed) · AIC search ranks everything and `style_title` is a single label
- What: `artworks/search?q=cubism` reports `total: 133169` out of a collection of roughly 130,000 works, because the search is a relevance-scored full-text match and the top hits are correct (Picasso's *Man with a Pipe*, `style_title: Cubism`). The record for 27992 (*La Grande Jatte*) gives `style_title: "Pointillism"`. That is useful ground truth for evals, but there is only one style per record. Read `total` only as an upper bound; to filter, use `style_title` or `style_ids` in an Elasticsearch `query` parameter. Without the `AIC-User-Agent` header the API answers with a Cloudflare 403.
- Track: tooling and testing
- Affects: aw.py HTTP client (headers); eval fixtures
- Magnitude: n/a (initial)
- Sources: https://api.artic.edu/docs/ (403 to WebFetch), probes

### F5 · 2026-05-19 · VLMs pick style labels from mostly art-historically relevant concepts, but some right answers come for wrong reasons
- What: "Does AI See like Art Historians?" (Limpijankit et al., Columbia with art historians; arXiv 2603.11024, v3 dated 2026-05-19) decomposed VLM latent space for style prediction. Art historians judged about 73% of the extracted concepts coherent, and about 90% of the concepts that drive predictions relevant. About 10% were irrelevant yet still produced correct predictions; experts suspected the model was reading formal cues such as light and dark contrast rather than the movement's actual traits. Practice lesson: a right label from a vision model does not show the reasoning is right. Have artwright cite **checkable visual traits** for any movement it names (for cubism: faceted planes, several viewpoints at once, a muted palette in the analytic phase, collage or papier collé in the synthetic phase), so a reviewer can verify them.
- Track: practice and testing
- Affects: the "does this image contain X" procedure; a trait-checklist requirement in the analysis output
- Magnitude: n/a (initial)
- Suggested response: adopt (require trait evidence with each label)
- Sources: https://arxiv.org/abs/2603.11024

### F6 · 2026-02-24 · Cross-cultural critique benchmark: VLMs score Western art higher, and depth falls off past description
- What: VULCA-Framework (Yu et al., arXiv 2601.07984 v3, 2026-02-24, submitted to ACL 2026) tested 15 VLMs on 294 evaluation pairs with 165 culture-specific dimensions across six traditions, using five levels from L1 (visual description) to L5 (cultural interpretation). Findings: "Western art samples consistently receive higher scores than non-Western ones"; quality drops from L1–L2 to L3–L5; single-judge scoring calibrated against experts beats automated metrics. Code: github.com/yha9806/VULCA-Framework. Related 2026 papers (from search snippets only, not read): StyleDecoupler/WeART (arXiv 2601.17697) calls WikiArt Western-centric and proposes a set three times larger that adds Chinese painting, digital art and children's illustration; HanMoVLM (arXiv 2603.10814) reports that VLMs struggle with non-Western artists.
- Track: testing and practice
- Affects: eval suite (needs non-Western cases); the analysis procedure (state which tradition's criteria are being applied)
- Magnitude: n/a (initial)
- Suggested response: adopt (L1–L5 layering as the shape of the analysis output; non-Western eval cases); point (VULCA as an external harness)
- Sources: https://arxiv.org/abs/2601.07984, https://arxiv.org/pdf/2601.17697, https://arxiv.org/pdf/2603.10814

### F7 · 2026-02-25 · New SEP entry on Chinese painting and calligraphy, which does not cover Xie He
- What: SEP published "Chinese Philosophy: aesthetics of painting and calligraphy" on 2026-02-25. It treats literati painting (*xieyi*, "writing intention") as "the only form of painting theorized in the Chinese tradition", built on brushstroke over colour and on deliberate incompleteness. It covers Zhang Yanyuan (9th c., *Lidai minghua ji*), Jing Hao (10th c., resemblance *si* versus truth *zhen* with *qi*), Deng Chun and Shen Zongqian, and Ji Cheng on gardens. It does **not** cover Xie He's Six Principles. For those, Wikipedia (flagged for needing more citations) gives: 1 *qiyun shengdong* (spirit resonance, vitality), 2 *gufa yongbi* (bone method, use of the brush), 3 *yingwu xiangxing* (correspondence to the object, depicting form), 4 *suilei fucai* (suitability to type, applying colour), 5 *jingying weizhi* (division and planning, placement), 6 *chuanyi muxie* (transmission by copying), from the preface to *Guhua pinlu* (6th c.). The translation of principle 1 is contested in the literature (Acker, Soper, Cahill); this pass did not verify that debate from a primary source.
- Track: subject
- Affects: the non-Western theory file
- Magnitude: n/a (initial)
- Sources: https://plato.stanford.edu/entries/chinese-painting-calligraphy/, https://en.wikipedia.org/wiki/Xie_He_(artist)

### F8 · 2026-03-02 · AI authorship: the Supreme Court declined Thaler, so the human-authorship rule stands
- What: the Supreme Court denied certiorari in *Thaler v. Perlmutter* (No. 25-449) on 2026-03-02, leaving the D.C. Circuit's March 2025 holding in place: the Copyright Act requires a human author. The Copyright Office's *Copyright and AI* report: Part 1 Digital Replicas (2024-07-31), Part 2 Copyrightability (2025-01-29), Part 3 Generative AI Training (pre-publication 2025-05-09, final "in the future"). The registration guidance is 88 FR 16190 (2023-03-16), with Review Board decisions on *Zarya of the Dawn*, *Théâtre D'opéra Spatial* and SURYAST. The practical advice that recurs across sources is to document the human contribution. On the theory side the debate continues (SEP has an entry on the philosophy of digital art), but the legal position in the US is settled for now.
- Track: subject
- Affects: the "AI and authorship" section; any advice artwright gives sibling plugins (comfyui-gen, brandwright, musicwright album art) about provenance notes
- Magnitude: n/a (initial)
- Sources: https://www.mayerbrown.com/en/insights/publications/2026/03/supreme-court-denies-review-in-ai-authorship-case, https://www.hklaw.com/en/insights/publications/2026/03/the-final-word-supreme-court-refuses-to-hear-case-on-ai-authorship, https://www.copyright.gov/ai/

### F9 · 2026-01-30 · Getty Vocabularies are linked-data only now; the SPARQL endpoint refuses scripted clients
- What: Getty discontinued the XML web services and the XML and relational releases for AAT, TGN and ULAN; the final sets were drawn on 2026-01-30. SPARQL (`vocab.getty.edu/sparql`), OpenRefine reconciliation and monthly N-Triples dumps remain, under ODC-By 1.0, so attribution is required (unlike Wikidata's CC0). Today two curl requests with an honest UA got 403 from nginx, and historywright's pass had flagged the same host. Treat AAT as a vocabulary to cite by ID (for example, Cubism is AAT 300021495), reached through Wikidata P1014 (208 movements carry it), rather than as a live dependency.
- Track: subject (sources) and tooling
- Affects: aw.py should not depend on vocab.getty.edu at run time; the movements file carries AAT and Wikidata IDs
- Magnitude: n/a (initial)
- Suggested response: adopt (IDs in the outline file; Wikidata as the live route)
- Sources: https://www.getty.edu/research-conservation/tools-databases/vocabularies/data-services, https://www.getty.edu/research/tools/vocabularies/lod/sparql.html

### F10 · 2026 (fall syllabi) · What surveys actually teach: Gardner/Stokstad plus Smarthistory; Art Since 1900 for the 20th century
- What: fall 2026 US survey syllabi (Youngstown State, Southern Utah, Northern Iowa, the Butte College outline for 2026–27) use *Gardner's Art Through the Ages: A Global History* (16th ed.) or Stokstad's *Art History* (7th ed., 2025), with Smarthistory essays as readings. Northern Iowa uses Smarthistory alone. Smarthistory has over 4,000 essays and 1,000 videos by more than 850 contributors and is openly reviewed. Its text is CC BY-NC-SA (4.0 per older terms), with image rights kept by the holders; its own pages refused WebFetch with 403. For the 20th century and after, *Art Since 1900* (Foster, Krauss, Bois, Buchloh, Joselit; third edition 2016, a newer edition possible but unconfirmed) structures modernism, antimodernism and postmodernism year by year. Contemporary-theory courses (Bologna 2026, Manchester 2027 catalogue) end with relational aesthetics and its antagonists (Bourriaud against Bishop), socially engaged art, and net and post-internet art. The "global" framing is now the default in survey titles, but the units still sit on a Western spine with world chapters inserted between them.
- Track: subject and practice
- Affects: the movements outline's ordering and the "theory waves" file; reference list
- Magnitude: n/a (initial)
- Sources: https://catalog.ysu.edu/syllabi/2026-fall/art-1541-01-42571/, https://my.suu.edu/syllabus/202630/ARTH-2710-30I/, https://syllabus.uni.edu/sites/default/files/inline-files/arthist-1111-01-fall2026.pdf, https://www.butte.edu/student-resources/academic-resources/curriculum-tools/course-outlines/2026-2027/pdf/ARTH-C1200-course-outline.pdf, https://wiki.creativecommons.org/wiki/Case_Studies/Smarthistory, https://ipmtoday.com/digital-humanities/the-brilliant-histories-of-art-belong-to-everyone/, https://www.unibo.it/en/study/course-units-transferable-skills-moocs/course-unit-catalogue/course-unit/2026/531319, https://www.manchester.ac.uk/study/undergraduate/courses/2027/12152/ba-art-history-and-english-literature/course-details/HART30561

### F11 · 2024-07-30 · SEP definition-of-art map, the backbone for "is this art?" and postmodern theory questions
- What: SEP "The Definition of Art" (substantive revision 2024-07-30) lays out the families: traditional (representational, expressive, formalist); institutional (Dickie 1974, revised 1984: "an artifact of a kind created to be presented to an artworld public"); historical (Levinson 1990); Danto's artworld (1964 essay, 1981 *Transfiguration of the Commonplace*); aesthetic-functional (Beardsley 1982); cluster (Gaut 2000, ten properties); anti-definition (Weitz 1956, "open concept"). SEP aesthetics entries worth linking by slug: `aesthetic-judgment`, `kant-aesthetics`, `plato-aesthetics`, `aristotle-aesthetics`, `hume-aesthetics`, `hegel-aesthetics`, `aesthetics-19th-romantic`, `aesthetics-critical-theory`, `aesthetics-race`, `feminism-aesthetics`, `conceptual-art`, `digital-art`, `depiction`, `beauty`, `japanese-aesthetics`, `chinese-painting-calligraphy`, `ethics-cultural-heritage`, `art-ontology-history`, `goodman-aesthetics`, `beardsley-aesthetics`, `collingwood-aesthetics`. SEP has no entry on Indian, Islamic or African aesthetics in the parts read (the contents page was only partly readable), so those need other references.
- Track: subject
- Affects: the theory file's references
- Magnitude: n/a (initial)
- Sources: https://plato.stanford.edu/entries/art-definition/, https://plato.stanford.edu/contents.html

### F12 · 2023-12-06 · Japanese aesthetic terms come with explicit cautions
- What: SEP "Japanese Aesthetics" (revised 2023-12-06) glosses *mono no aware* (pathos of impermanence), *wabi* (austere, understated), *sabi* (beauty of age and weathering), *yūgen* (mysterious depth), *iki* (refined, coquettish style with composure) and *kire* (cut, and cut-continuity). It does **not** treat *ma*, so artwright needs another source for that term. The entry warns against anachronism (these ideas predate Japanese "aesthetics" as a 19th-century discipline), against changes in meaning over time, against glosses that don't translate (Kuki on *iki*), and against exoticising them as a single "East Asian" essence. Practice lesson: when artwright uses these words to describe a Western or AI image ("this has wabi-sabi"), it should flag that as a loose borrowed sense. "Wabi-sabi" as one compound is largely a modern, Western-popular usage.
- Track: subject and practice
- Affects: the non-Western theory file; the style vocabulary guard
- Magnitude: n/a (initial)
- Suggested response: adopt (a usage note for borrowed terms)
- Sources: https://plato.stanford.edu/entries/japanese-aesthetics/

### F13 · undated secondary sources · Rasa: eight in the Natyashastra, a ninth (shanta) added later, and the attribution is disputed
- What: Bharata's *Natyashastra* (dated anywhere from about 500 BCE to 500 CE) names eight rasas: *śṛṅgāra* (erotic/love), *hāsya* (comic), *karuṇa* (pathos), *raudra* (fury), *vīra* (heroic), *bhayānaka* (terror), *bībhatsa* (disgust), *adbhuta* (wonder). A ninth, *śānta* (peace), is credited variously to Udbhaṭa, to Ānandavardhana (*Dhvanyāloka*, 9th c.) or to Abhinavagupta (*Abhinavabhāratī*, 10th–11th c.), who treats it as the ground of the others. Rasa arises in the audience: *vibhāva* (determinants), *anubhāva* (consequents) and *vyabhicāri bhāva* (transitory states) produce the *sthāyi bhāva* (stable emotion), which is savoured as rasa. These come from secondary sources and need a scholarly reference before shipping. The Shilpa Shastras (iconometry by *tāla* units) were not researched in this pass because the search budget went to API status.
- Track: subject
- Affects: the non-Western theory file
- Magnitude: n/a (initial)
- Sources: https://en.wikipedia.org/wiki/Shanta_Rasa, https://ebooks.inflibnet.ac.in/engp11/?p=110, https://mapacademy.io/?p=3060

### F14 · 2023 onward · AI attribution of Old Masters is a paid lesson: confident percentages, disputed by specialists
- What: Art Recognition's AI said the National Gallery's *Samson and Delilah* was not by Rubens "with 92 percent" certainty; Nils Büttner (Centrum Rubenianum) answered that "the results are not in accordance with what Rubens scholars say." For the de Brécy Tondo, two AI analyses reached opposite answers (Bradford's face matching said Raphael; Art Recognition said not Raphael at 85% or more). Critics note that the models and datasets are proprietary and cannot be checked. Lesson for artwright: never state an attribution, authenticity or "who painted this" verdict from pixels. Report the catalogue record (museum and accession number) and say that attribution is a matter of connoisseurship, technical analysis and provenance, not something the model can settle.
- Track: practice
- Affects: a hard guard in the analysis skill; an eval case ("is this a real Rubens?")
- Magnitude: n/a (initial)
- Suggested response: adopt
- Sources: https://news.artnet.com/market/rubens-art-recognition-ai-authentication-2017274, https://news.artnet.com/opinion/ai-art-authentication-2398765, https://adn.com/arts/2023/07/28/artificial-intelligence-identified-a-renaissance-masterpiece-art-historians-are-skeptical

### F15 · 2026-10-21 · Tooling: thin museum MCP wrappers; no art-history skill with evals
- What: MCP registry searches ("museum", "art", "artic", "rijks", "europeana", "getty") return `io.github.cyanheads/met-museum-mcp-server` (many versions, CC0 images), `io.github.mrfentmen/metmuseum-mcp`, and the generic pipeworx-io wrappers `metmuseum`, `artic`, `rijksmuseum` and `europeana`. Nothing exists for Getty vocabularies, Wikidata art properties or multi-museum search. Whether cyanheads moved to v1.1 search was not checked. GitHub `"art history" filename:SKILL.md` finds persona tutors (theneoai art-instructor, 24kchengYe arts-design-tutor), journal-submission skills (brycewang-stanford Art Bulletin, October, Burlington), and `alchaincyf/huashu-art-motion` (an "Art History Speedrun" animation of 16 eras, 2026-10-04). None ship evals or a sourced movements knowledge base. historywright already keeps a source registry covering the Met, AIC, Cleveland, Getty, Smithsonian, Rijksmuseum and Europeana.
- Track: tooling
- Affects: build vs reuse decisions
- Magnitude: n/a (initial)
- Suggested response: point (cyanheads Met MCP as optional); adopt (reuse historywright-sources' registry and the hw.py HTTP conventions rather than a second museum client)
- Sources: https://registry.modelcontextprotocol.io/v0/servers?search=museum, GitHub code search (gh CLI, 2026-10-21)

### F16 · 2026-10-21 · Reference access: Oxford Art Online (Grove, Benezit) needs a subscription; Heilbrunn and Smarthistory refuse scripted fetches
- What: Oxford Art Online bundles Grove Art Online and the Benezit Dictionary of Artists; university library listings mark it restricted (Rutgers: 13 simultaneous users). Treat it as paid and unusable by an agent. The Met's Heilbrunn Timeline essays (`metmuseum.org/essays`) returned 429 to WebFetch, and Smarthistory returned 403. Both are fine to cite by URL for people to read, but they are not a dependable agent route. For agent use, SEP (fetches cleanly), Wikidata and museum APIs are the reliable open routes, and fetchwright (Gemini URL context) is the fallback for pages that refuse scripts.
- Track: tooling and practice
- Affects: the references list; the fetch fallback
- Magnitude: n/a (initial)
- Suggested response: point (fetchwright as fallback)
- Sources: https://www.libraries.rutgers.edu/databases/oxford_art, fetch results 2026-10-21

## Overall magnitude: n/a (initial)

## Open questions:
- New: Rijksmuseum data licence today (the docs index states none; confirm on the subpages).
- New: Paris Musées API token rule and endpoint docs; National Palace Museum Open API endpoints (2021 hackathon description only).
- New: whether vocab.getty.edu's 403 blocks all scripted clients or only some UAs or IP ranges (historywright saw the same).
- New: whether *Art Since 1900* has a fourth edition (the Norton UK ISBN suggests a newer printing).
- New: the translation debate on Xie He's first principle and a scholarly source for rasa and the Shilpa Shastras (Wikipedia and secondary sources only so far).
- New: Islamic geometric and calligraphic, Persian miniature, Mesoamerican, African and Oceanic traditions, and the "primitivism" critique (MoMA 1984) were not reached with sources in this pass. The outline below lists them from model knowledge and must be verified before shipping.
- New: whether `cyanheads/met-museum-mcp-server` handles the v1 search retirement.

## Search plan notes:
- Subject: SEP pages fetch cleanly and are dated, so they are the best theory source. Syllabus searches with "fall 2026" found real catalogue pages. Wikipedia is acceptable for term lists but flagged.
- Sources: probing endpoints directly beat reading docs. The 410 bodies at the Met and Rijksmuseum explain themselves. AIC docs, Smarthistory, Heilbrunn and Getty pages refuse WebFetch, so probe the APIs instead. historywright's 2026-10-17 research already covers Smithsonian and Europeana limits; reuse it rather than searching again.
- Practice: the artnet coverage of AI authentication is the best documented failure case. arXiv 2026 has three relevant VLM art papers.
- Noise: the API reseller and listicle sites (oanor, jentic, apify) in AIC searches.
- Forums lacking: none apply directly; the museums' GitHub repo issue trackers (metmuseum/openaccess has 43 open issues) are the closest thing to an announcements channel.

## Tracks covered: subject: 7 queries · tooling: 3 (2 searches + registry and gh probes) · practice: 2 · testing: 1 (+ probes)

## Upcoming events:
- Copyright Office Part 3 final version · date not announced
- ACL 2026 proceedings (VULCA) · already past or pending; check
- Met v1.1 is new (2026-09-04); expect follow-up changes in its changelog

## Nothing changed: no (creation pass)

## Proposals for artwright

- **Movements outline file** (`knowledge/movements.md` or `.json`, about 80–110 entries, about 25–35 KB as JSON or about 15 KB as Markdown, within the package size budget): one row per period or movement with `name`, `aka`, `dates` (EDTF-style ranges), `region`, `traits` (four to six **visually checkable** traits a vision model can confirm or deny), `confusable_with`, `key_works` (with museum and accession number where CC0), `wikidata` QID and `aat` ID. Routing order: Prehistoric (Paleolithic cave painting about 40,000 BP, Neolithic) → Ancient Near East, Egypt, Aegean, Greek (Geometric, Archaic, Classical, Hellenistic), Roman → Early Christian and Byzantine → Islamic (Umayyad to Ottoman; geometric girih, arabesque, calligraphy, Persian miniature) → Medieval Europe (Insular, Carolingian, Romanesque, Gothic) → Renaissance (Proto, Early, High, Northern, Mannerism) → Baroque, Rococo → Neoclassicism, Romanticism, Realism, Academic → Impressionism, Post-Impressionism, Pointillism, Symbolism, Art Nouveau → Fauvism, Expressionism, Cubism (analytic and synthetic), Futurism, Dada, Surrealism, De Stijl, Constructivism, Bauhaus, Art Deco → Abstract Expressionism, Pop, Minimalism, Op, Conceptual, Fluxus, Performance, Land art → Postmodernism, Neo-Expressionism, Pictures Generation, YBAs → Relational, post-internet, new media, NFT/crypto art, AI art. Parallel tracks with the same fields: China (Six Dynasties to literati, Song landscape, Ming/Qing, ink), Japan (Yamato-e, Rinpa, ukiyo-e, Nihonga, Mono-ha, Superflat), South Asia (Gandhara, Mathura, Gupta, Chola bronze, Mughal and Rajput miniature, Bengal School, Progressive Artists' Group), Africa (Nok, Ife, Benin, Kongo, contemporary), Oceania, the Americas (Olmec, Maya, Aztec, Andean; Northwest Coast; Mexican muralism), plus 2D digital art (pixel art eras, demoscene, vaporwave). Mark every non-verified row `verified: false` until a source is attached.
- **Theory waves file** (`knowledge/theory.md`, about 8 KB): one paragraph per wave (mimesis and the canon; Kant's disinterested judgement; Romantic expression; formalism Bell/Fry/Greenberg; iconology Panofsky's three levels; social art history Clark/Baxandall; Danto, Dickie, Levinson, Weitz, Gaut per SEP; Krauss and Owens; feminist (Nochlin 1971, Pollock); postcolonial and the primitivism critique; Bourriaud against Bishop; post-internet; AI authorship), each with the question it lets artwright ask of an image and a SEP slug or other reference.
- **Non-Western theory file** with Xie He's six principles, the rasa scheme, Japanese terms with the SEP usage cautions (F12), Islamic geometry, and a "borrowed-term" guard.
- **Analysis output shape** borrowed from VULCA's L1–L5 (and Panofsky): description → formal analysis → style/movement with trait evidence → context → interpretation, and say which tradition's criteria are being applied (F5, F6).
- **Hard guards**: no attribution, authentication or valuation from pixels (F14); a missing Wikidata movement tag is not evidence (F3); cite which museum record a fact came from.
- **aw.py `lookup`**: reuse historywright's source registry and HTTP conventions. Use Met v1.1 (`offset`/`limit`, cap 10,000), AIC with the `AIC-User-Agent` header and `fields=`, Cleveland, Rijksmuseum Linked Art search, Wikidata SPARQL for P135/P136/P186/P195/P571/P1014. Use no keyed source by default; Smithsonian, Harvard and Europeana are opt-in with keys from a config file that is never committed. Harvard's non-commercial and no-caching terms rule it out of any cache. Do not use vocab.getty.edu at run time.
- **Ground-truth fixtures for evals**: AIC `style_title` (27992 is Pointillism; 109260 is Cubism), Met `isPublicDomain` records and Cleveland `share_license_status` give recorded answers for "does this contain cubism?" and licence checks. Add non-Western cases (a literati landscape, a Mughal miniature, an Edo ukiyo-e) and one authentication-refusal case.
- **Freshness checks** for the evergreen plan: probe the Met v1.1 response shape, AIC with and without the header, the Rijksmuseum search endpoint, and the Getty SPARQL status, each as a one-request smoke test in `evals` or `aw.py doctor`.

## Cost: searches 13 (one failed at the usage limit) · fetches 23 (3 failed at the usage limit, 5 refused or 404) · tool calls 45 (plus 9 curl/gh probe batches counted in tool calls)
