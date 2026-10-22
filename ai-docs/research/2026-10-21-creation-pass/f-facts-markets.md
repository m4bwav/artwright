# Creation pass 2026-10-21: F. facts and markets (raw researcher report)

Verbatim report of the research pass for this track. Synthesis: [../2026-10-21-creation-pass.md](../2026-10-21-creation-pass.md).

Mode: creation. Magnitudes are `n/a (initial)`. Every retrieval below happened on 2026-10-21 unless a line says otherwise. Quotes are exact strings from the fetched page or API record. Where a page could only be read through the fetch tool's summariser, the report says so; one summarised quote was wrong (F9), so treat those quotes as leads until someone reads the raw page.

## Findings (newest first)

### F1 · 2026-01-21 · The oldest dated cave art is now a 67,800-year-old hand stencil, not the 51,200-year-old Sulawesi scene
- What: Oktaviana et al., "Rock art from at least 67,800 years ago in Sulawesi", *Nature* 650 (8102): 652–656, online 21 January 2026, DOI 10.1038/s41586-025-09968-y. I matched the title, first author and year in Crossref, and read the abstract through OpenAlex. The art is a hand stencil in Liang Metanduno on Muna Island, off southeastern Sulawesi, dated by laser-ablation U-series to 71.6 ± 3.8 ka, so its minimum age is 67.8 ka. The abstract says this minimum is "1.1 kyr greater than the published minimum for a hand stencil from Spain attributed to Neanderthals, which until now represented the oldest demonstrated minimum-age constraint for cave art worldwide." The figurative record did not change: the Leang Karampuang pig-and-figures scene (Nature 2024) is still the oldest representational art. Guinness now splits the record in two: "oldest painting – non-figurative art" goes to the stencil (record dated 21 January 2026), and it calls the stencil "some 16,000 years older than the oldest figurative rock art".
- Track: subject
- Affects: the "oldest painting" gold answer. Any answer that says 51,200 years with no qualifier is out of date.
- Magnitude: n/a (initial)
- Sources: https://api.crossref.org/works/10.1038/s41586-025-09968-y, https://api.openalex.org/works/doi:10.1038/s41586-025-09968-y, https://news.griffith.edu.au/?p=85777 (22 Jan 2026), https://www.guinnessworldrecords.com/world-records/782566-oldest-painting-non-figurative-art. nature.com redirected to a login page, so I read the abstract through OpenAlex.

### F2 · 2025-11-18 · Salvator Mundi still holds the auction record; Klimt's Lederer portrait is second
- What: Wikidata Q1892745 carries P2284 (price) = 450,312,500 USD with point in time 2017-11-15. The statement has no reference. Arab News (16 Nov 2017) reports it "sold for a record-smashing $450.3 million on Wednesday at Christie's in New York" and gives the previous record as "Picasso's 'Les Femmes D'Alger,' which sold for $179.4 million in May 2015". Secondary reports give a $400 million hammer plus fees. Klimt's *Portrait of Elisabeth Lederer* sold at Sotheby's New York on 18 November 2025 for $236.4 million (about $205 million hammer). Reports call it the second most expensive work ever sold at auction. One outlet gives Salvator Mundi as "$405m". That figure is an error and shows how fast these numbers get garbled.
- Track: subject
- Affects: the sanity gold for "most expensive painting"
- Magnitude: n/a (initial)
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1892745, https://www.arabnews.com/art-culture/da-vinci-portrait-of-christ-sells-for-record-4503-million-in-new-york-1194191, https://www.aljazeera.com/news/2025/11/20/gustav-klimt-portrait-breaks-modern-art-record-with-236m-sale (search snippet only, not fetched)

### F3 · 2026 · Wikidata records attribution and ownership as qualified, sometimes disputed statements
- What: On Q1892745, the creator is Leonardo (Q762) with qualifier P5102 "nature of statement" = Q230768 "attribution". A second creator statement names Leonardeschi (Q1089243), imported from a Wikipedia edition. The *preferred* owner statement is Mohammed bin Salman, with no reference, although press reports name a different stand-in buyer. Wikidata's art statements are leads. A tool that reads only the truthy value would print a disputed owner as fact. This is historywright's R-20261017-2 rule applied to art.
- Track: practice
- Affects: the provenance and attribution steps
- Magnitude: n/a (initial)
- Suggested response: adopt (read P170 with P5102, P1480 and P127 with qualifiers through `hw.py wd claims`, and never trust the truthy value alone)
- Sources: https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q1892745

### F4 · 2024-11-14 · Ming record prices: the cup is the porcelain record and the 2011 Yongle meiping is the vase record
- What: The Meiyintang Chenghua doucai "chicken cup" sold at Sotheby's Hong Kong on 8 April 2014. Sotheby's sale page HK0545 shows "08 April 2014", but the price sits behind a login. The Times (SA) report of 9 April 2014 gives "a bid of HK$250m plus fees" and HK$281.2 million in total, and names the buyer as Liu Yiqian. For vases, Sotheby's Hong Kong lot 11 of sale HK0377 (Meiyintang II, 4–5 October 2011) is catalogued "AN OUTSTANDING BLUE AND WHITE VASE WITH FRUIT SPRAYS, MEIPING, MING DYNASTY, YONGLE PERIOD", estimate HKD 80–120 million, result behind a login. Antiques & Art Ireland (5 Oct 2011) reports it "sold for HK$168,660,000 / £14,032,792/ US$21,623,077" and "set a world record for any Ming porcelain at auction". An artfixdaily report, seen only as a search snippet, gives HK$167.8 million. The most recent Ming headline is a pair of Jiajing wucai "fish jars" at Sotheby's London on 6 November 2024 for "£9.6 million ($12.5 million)". That is a pair of jars, not a vase, and much lower. The best Ming lot I found in 2026 was a Yongle dish at Poly HK for about HKD 24.6 million (search snippet only). I found no Ming vase above HK$168.66 million in 2012–2026, but the Sotheby's, Christie's and Poly results archives sit behind logins and bot walls, so absence is not proven.
- Track: subject
- Affects: the Ming vase gold
- Magnitude: n/a (initial)
- Sources: https://antiquesandartireland.com/2011/10/world-record-ming-vase/, https://www.sothebys.com/en/auctions/ecatalogue/2011/ceramics-myt-hk0377/lot.11.html, https://www.timeslive.co.za/news/south-africa/2014-04-09-ming-dynasty-chicken-cup-smashes-auction-record/, http://www.sothebys.com/en/auctions/2014/meiyintang-chicken-cup-hk0545.html, https://sothebys.com/en/articles/how-two-stunning-wucai-fish-jars-achieved-9-6m-at-auction

### F5 · 2013 to now · Traps in "most expensive vase" questions: the Qing vase, the Republican vase and Guinness
- What: (a) Guinness "Most expensive vase" says "The most expensive vase – and the most expensive piece of porcelain – is a 16-in-tall (40.64-cm) 18th-century vase" of the Qianlong period, sold in January 2013. That is the Bainbridges vase: hammered at £43 million in November 2010, the buyer never paid, and it later sold privately through Bonhams for a reported £20–25 million. It is Qing, not Ming. Guinness's "most expensive porcelain" claim also conflicts with the chicken cup's 2014 auction price of HK$281.24 million (about £21.5 million). (b) The 2010 Sotheby's Hong Kong double-gourd vase ($32.4 million) is Qianlong, so also Qing. (c) A vase catalogued "Probably Republican" (early 20th century) sold at Sotheby's New York in March 2011 for $18,002,500 against an estimate of $800–1,200 (theartwolf). (d) Wikipedia dates the chicken cup sale to "August 8, 2014", but the Sotheby's source it cites says 8 April. A finder page can be wrong about its own footnote.
- Track: practice
- Affects: the superlative method and the Ming gold
- Magnitude: n/a (initial)
- Suggested response: adopt (a "dynasty and reign check" and an "unpaid or private sale check" in the superlative procedure; Guinness counts as tier 3 and is never one of the two sources)
- Sources: https://www.guinnessworldrecords.com/world-records/498915-most-expensive-vase, https://theartwolf.com/news/chinese-vase-sothebys-2011/, https://en.wikipedia.org/wiki/Chicken_Cup_(Chenghua), https://paulfrasercollectibles.com/blogs/art-photography/looted-chinese-qianlong-vase-finally-sells-for-40m-in-private-deal (search snippet)

### F6 · 2026 · Art Basel and UBS Global Art Market Report 2026: the primary market-size source
- What: Written by Dr Clare McAndrew (Arts Economics). Global sales in 2025 "rise 4% to $59.6 billion". Dealers $34.8 billion, public auction $20.7 billion, and "Reported private sales declined by 5% to just under $4.2 billion". The press release is a free PDF. The page does not say whether the full report needs registration.
- Track: subject
- Affects: market-context answers
- Magnitude: n/a (initial)
- Sources: https://www.artbasel.com/stories/the-art-basel-and-ubs-global-art-market-report-2026?lang=en

### F7 · 2026 · Price databases are paid, and most forbid automated copying or block AI agents
- What: artnet's terms (updated 27 April 2023) say: "You may not use any robot, spider, other automatic device, or manual process to monitor or copy", and its Price Database subscription forbids creating "any derivative work, product or service" and downloading to storage. artnet's robots.txt returned 403. Artprice's robots.txt starts "# BLOCK AI/Scrapers" and disallows ClaudeBot, anthropic-ai, Claude-Web, GPTBot, PerplexityBot and others. MutualArt sells full results only on Premium and VIP plans; Essentials covers the last year only. Invaluable sets `Crawl-delay: 10`, and Sotheby's sets `Crawl-delay: 15`. Sotheby's lot results need a login ("Log in to view results"). The web search tool refused christies.com outright ("not accessible to our user agent"), and artnet and Antiques Trade Gazette news pages returned 403. Art Sales Index was not checked. Conclusion: the plugin cannot query the price databases. They are link-out only, and the user reads them.
- Track: tooling
- Affects: the market-sources registry entries
- Magnitude: n/a (initial)
- Suggested response: adopt (add artprice, artnet-pdb, mutualart, invaluable, liveauctioneers, sothebys-results, christies-results and art-sales-index as `route: link-out` with access notes)
- Sources: https://www.artnet.com/about/terms-and-conditions-of-use, https://www.artprice.com/robots.txt, https://www.mutualart.com/faq, https://www.sothebys.com/robots.txt

### F8 · 2026-01-26 · Getty Provenance Index: open CSV exports on GitHub, with Linked Open Data planned
- What: thegetty/provenance-index-csv (last push 2026-01-26) holds CSV exports of the Knoedler, Sales Catalogs and Goupil databases, all "Active", with files on S3. The README says: "These data will eventually be superseded by the Linked Open Data release". On licences: "rights may vary between datasets". The suggested citation names release v3 (June 2022). getty.edu's provenance page redirects twice and its content did not load in the fetch. Interpol's Stolen Works of Art database holds "almost 57,000 items", and "Anyone can apply to become an authorized user" (an account is required; the ID-Art app exists). The Art Loss Register lists "700000" items and calls itself "the leading due diligence provider for the art market". It is a paid service, and the homepage does not list fees. lostart.de and proveana.de both returned "Access Denied" from the BotStopper bot wall. ifar.org failed with "certificate has expired".
- Track: tooling
- Affects: the provenance step and the registry
- Magnitude: n/a (initial)
- Suggested response: adopt (Getty CSVs as a downloadable tier-1 source; Interpol, ALR, Lost Art, Proveana and IFAR as link-out with their status)
- Sources: https://github.com/thegetty/provenance-index-csv, https://www.interpol.int/en/Crimes/Cultural-heritage-crime/Stolen-Works-of-Art-Database, https://www.artloss.com/

### F9 · current · Sotheby's glossary of attribution qualifiers, read raw (the summariser corrupted it)
- What: Sotheby's "Glossary of Terms" (help.sothebys.com, article 44002518846) says, verbatim: "GIOVANNI BELLINI In our opinion a work by the artist." · "ATTRIBUTED TO GIOVANNI BELLINI In our opinion probably a work that was created at a time when the artist mentioned was active and there are serious grounds to believe that it is by the artist's hand, but less certainty as to authorship is expressed than in the preceding category." · "STUDIO OF … a work by an unknown hand in the studio of the artist which may or may not have been executed under the artist's direction." · "CIRCLE OF … a work by an artist as yet unidentified but distinct hand, closely associated with the named artist but not necessarily his pupil." · "FOLLOWER OF … working in the style of the artist, contemporary or close to his time but not inevitably his pupil." · "STYLE OF OR MANNER OF … a work in the style of the artist and of a later date." · "AFTER … a copy of a known work of the artist." "Signed" means "from the hand of the artist", and "bears a signature" means "added by another hand". The general rule: "Any statement as to authorship, attribution, origin, date, age, provenance and condition is a statement of opinion". For Chinese ceramics the example is "A Blue and White Dish, Ming Dynasty, Jiajing period", and a heading with no bold attribution means "we are unable to determine the period". Dealers' glossaries differ: one treats "Manner of" as the same as "Follower of". The fetch summariser cut the "Attributed to" sentence off before its final clause, which changed what it means. A raw-HTML grep recovered the full text.
- Track: practice
- Affects: the attribution vocabulary reference
- Magnitude: n/a (initial)
- Suggested response: adopt (verify quotes against raw HTML, the hw.py verify quote route, not a summariser; name the auction house whose glossary applies)
- Sources: https://help.sothebys.com/en/support/solutions/articles/44002518846

### F10 · current · Museum APIs expose attribution qualifiers and open images for the gold objects
- What: The Met's v1 object endpoint answered for 255574 and returned `"artistPrefix":"Attributed to"`, `"artistDisplayName":"Sophilos"`, `"objectDate":"early 6th century BCE"`, with ULAN and Wikidata links. The museum's attribution qualifier is a structured field. Museo Egizio's collection page for the Gebelein painted linen (Suppl. 17138) gives "3600–3350 BCE", "Predynastic Period, Naqada II", provenance "Egypt, Gebelein", and links its downloads to CC0 1.0. Museo Egizio is not in historywright's registry.
- Track: tooling
- Affects: the registry hand-off
- Magnitude: n/a (initial)
- Suggested response: point (propose Museo Egizio to historywright-sources; artwright reads `artistPrefix`-style fields)
- Sources: https://collectionapi.metmuseum.org/public/collection/v1/objects/255574, https://collezioni.museoegizio.it/en-GB/material/S_17138

### F11 · 2026 · Tooling: two art-provenance MCP servers exist; neither verifies prices
- What: kintopp/rijksmuseum-mcp-plus (MIT, 17 stars, pushed 2026-10-21) offers provenance search over Rijksmuseum data copied on 2 May 2026, with an experimental provenance parser and a bundled skill. It warns: "Please do not treat the data made available by this resource as current or authoritative". mildo-ai/provenio (pushed 2026-07-19) is a free beta remote MCP. It claims a 282,731-node graph over the Getty Provenance Index, Knoedler and ERR, with "Hallucination is held under 1%", which is self-reported. GitHub code search for `path:SKILL.md "auction" "provenance"` returned 0 results. No skill checks art-market superlatives.
- Track: tooling
- Affects: none (artwright's niche is open)
- Magnitude: n/a (initial)
- Suggested response: point (rijksmuseum-mcp-plus as an optional route; provenio noted, unverified, a third-party beta, never a sole source)
- Sources: https://github.com/kintopp/rijksmuseum-mcp-plus, https://github.com/mildo-ai/provenio

### F12 · 2018–2020 · The Neanderthal cave-art claim is real but contested
- What: Hoffmann et al. 2018, *Science*, DOI 10.1126/science.aap7778 (Crossref-checked): "cave art in Iberia is older than 64.8 thousand years (ka) … which implies Neandertal authorship" (La Pasiega, Maltravieso, Ardales). The rebuttal is White et al. 2020, *J. Hum. Evol.*, DOI 10.1016/j.jhevol.2019.102640, "Still no archaeological evidence that Neanderthals created Iberian cave art" (title read; abstract not available in OpenAlex). The 2026 Muna paper describes the Spanish minimum as the previous oldest. Also relevant: Henshilwood et al. 2018, *Nature*, DOI 10.1038/s41586-018-0514-3, "An abstract drawing from the 73,000-year-old levels at Blombos Cave". That is an ochre-crayon drawing on a stone flake, a portable surface, and drawing, not painting.
- Track: subject
- Affects: the "oldest painting" readings
- Magnitude: n/a (initial)
- Sources: https://api.openalex.org/works/doi:10.1126/science.aap7778, https://api.crossref.org/works/10.1016/j.jhevol.2019.102640, https://api.crossref.org/works/10.1038/s41586-018-0514-3

### F13 · current · Oldest panel painting and oldest named painter
- What: The Pitsa panels are "the earliest surviving examples of Greek panel painting", in the National Archaeological Museum, Athens (NAMA 16464–16467), "stylistically dated to 550–500 BC". Other sources say c. 540–530 BC. An inscription "in the Corinthian alphabet names two woman dedicators, Euthydika and Eucholis". A damaged vertical inscription contains "Corinthian" and "is presumed to refer to the donor, or possibly the painter". So the painter's name is not known. This comes from the Wikipedia extract; the Brecoulaki technical PDF answered 503. For a named painter of a surviving painting, the candidates are vase painters. Sophilos (Attic, active c. 590–570 BCE) is "the oldest Attic vase painter so far to be known by his true name". The Aristonothos krater (c. 670–660 BCE, Capitoline Museums) carries a maker's signature whose reading ("epoiesen", made) is debated. I read both only as search snippets.
- Track: subject
- Affects: the "oldest painting with a known painter" reading
- Magnitude: n/a (initial)
- Sources: https://en.wikipedia.org/wiki/Pitsa_panels (finder), https://en.wikipedia.org/wiki/Sophilos (snippet), https://riviste.unimi.it/index.php/aristonothos/article/view/569 (snippet)

### F14 · method · Lessons people already paid for
- What: (1) Auction houses publish results behind logins, so the open web carries secondary copies with wrong dates, wrong currency conversions, and hammer and premium mixed up (the $405m and HK$167.8m variants, the April/August date). (2) Guinness rulings lag the scholarship or disagree with it (porcelain record). (3) The "Ming" label gets attached to Yuan, Qing and even Republican pieces. (4) Unpaid sales count as hammer records but not as sales (Bainbridges). (5) Minimum ages from U-series dating are lower bounds and get reported as ages. (6) Fetch summarisers truncate legal and glossary sentences. (7) Dendrochronology and pigment analysis are evidence types (Pitsa: pigments identified include "Egyptian blue … cinnabar, orpiment and realgar"). This pass did not research technical art history further and leaves it open.
- Track: practice
- Affects: the superlative procedure and the answer format
- Magnitude: n/a (initial)
- Suggested response: adopt (each lesson becomes a check in the superlative procedure; 1, 3 and 4 become eval cases)
- Sources: as in F2, F4, F5 and F9

### F15 · testing · How to test the gold answers
- What: There is no external benchmark for art-market facts. The checkers that work: a rubric with required elements (the reading named, the date of the sale, the currency and whether the price includes premium, the auction house, the dynasty and reign checked) and forbidden elements (calling the Qianlong vase Ming, giving 51,200 years as the oldest painting of any kind with no qualifier, naming a painter for prehistoric art). historywright's `hw.py verify sources` checks quotes against their pages and counts independent sources.
- Track: testing
- Affects: evals/evals.json
- Magnitude: n/a (initial)
- Suggested response: adopt (the two golds below become cases with must and must-not lists)
- Sources: historywright repository (AGENTS.md, skills/historywright/SKILL.md Steps 5 and 7)

## Gold answers (verified)

### G1. "What is the most expensive Ming vase?"
Readings: (a) a Ming vase sold at public auction, Ming meaning strictly 1368–1644; (b) any Ming porcelain, not only vases; (c) including private sales; (d) the popular sense, where people say "Ming vase" for any Chinese vase.
- (a) The Yongle-period blue-and-white meiping with fruit sprays, Meiyintang Collection, Sotheby's Hong Kong, October 2011 (sale HK0377, lot 11): HK$168,660,000 including premium (about US$21.6 million). Sources: Sotheby's lot page for the title, period and estimate ("MING DYNASTY, YONGLE PERIOD", "80,000,000 - 120,000,000 HKD", result behind a login). Antiques & Art Ireland, 5 Oct 2011, for the price: "sold for HK$168,660,000 / £14,032,792/ US$21,623,077" and "set a world record for any Ming porcelain at auction". Both read 2026-10-21. One snippet gives HK$167.8 million.
- (b) The Chenghua doucai "chicken cup", Sotheby's Hong Kong, 8 April 2014: HK$281.24 million including premium (HK$250 million hammer, about US$36 million). The buyer was Liu Yiqian. It is a cup, not a vase, and it is the auction record for any Chinese porcelain. Sources: Sotheby's HK0545 page ("08 April 2014"); Times (SA) of 9 April 2014: "a bid of HK$250m plus fees", "HK$281.2-million".
- (c) Private sales are rarely disclosed. None found.
- (d) If the asker means any Chinese vase, the Qianlong (Qing) vase from Bainbridges answers: £43 million hammer in 2010, unpaid, then sold privately in 2013 for a reported £20–25 million. Guinness calls it "the most expensive vase". It is not Ming, and the answer must say so.
- Confidence: medium on (a), because the price comes from one trade report plus the Sotheby's catalogue and the result itself is behind a login, and the 2012–2026 archives could not be fully searched. High on (b).
- Sources disagree (outdated source / different frame): Guinness ranks the Qianlong vase as the most expensive porcelain, which conflicts with the chicken cup; Wikipedia dates the cup sale to August instead of April.
- A grader must require: the reading named; Ming against Qing (or Yuan) kept apart; the cup-versus-vase distinction; price with currency, year, auction house and whether premium is included; a note that newer sales might exist. A grader must not require: an exact US$ conversion, the buyer of the 2011 vase, or a single number with no reading.

### G2. "What is the oldest surviving painting, who painted it, and where is it?"
- Oldest dated cave art of any kind: a hand stencil in Liang Metanduno, Muna Island (Southeast Sulawesi, Indonesia), at least 67,800 years old (U-series 71.6 ± 3.8 ka). Oktaviana et al., *Nature* 650: 652–656, published online 21 Jan 2026 (Crossref and OpenAlex, read 2026-10-21). Quote: "providing a minimum-age constraint of 67.8 ka for the underlying motif". Griffith University says it was made by "our species". Whether a hand stencil counts as a painting is itself a reading; Guinness files it as "non-figurative art".
- Oldest figurative painting or narrative scene: Leang Karampuang, Maros-Pangkep, South Sulawesi, at least 51,200 years old. Oktaviana et al., *Nature* 631: 814–818, 3 July 2024. Quote: "Painted at least 51,200 years ago, this narrative composition, which depicts human-like figures interacting with a pig, is now the earliest known surviving example of representational art". (The older Leang Tedongnge pig, about 45,500 years, was the previous figurative record.)
- Neanderthal claim: Spanish caves (La Pasiega, Maltravieso, Ardales) at "older than 64.8 thousand years" (Hoffmann et al. 2018). Disputed (White et al. 2020), and now younger than Muna.
- Oldest on a portable or textile surface: the Gebelein painted linen, Museo Egizio, Turin (Suppl. 17138), "3600–3350 BCE". Museum record read 2026-10-21. "Oldest painting on cloth" is a researchers' "could be", not a ranking. For drawing rather than painting: the Blombos ochre drawing on a flake, about 73,000 years.
- Oldest Greek panel painting: the Pitsa panels, National Archaeological Museum, Athens, c. 550–500 BC. Painter unknown.
- Who painted it: unknown for every prehistoric work. The answer must say so, and must not invent a culture-hero name. The earliest painters known by name are Greek vase painters (Sophilos, c. 590–570 BCE; Aristonothos, 7th century BCE, signature reading debated). The confident version of this reading is "earliest named painter whose work survives". Medium confidence; "oldest signed artwork" was not settled in this pass.
- Where and access: the Sulawesi caves are protected sites. Coverage mentions Indonesian government protection but this pass did not verify any public access. The Pitsa panels and the Gebelein linen are in museum collections.
- Confidence: high on the two Nature dates (read in the primary record). Medium on "painting" as a category, because it depends on the reading. Low to medium on the named-painter reading.
- Sources disagree (different frame and scholarly dispute): figurative against non-figurative; Neanderthal authorship.
- A grader must require: the reading named; the 2026 stencil, or an explicit "figurative" qualifier when the answer is 51,200; "minimum age" or "at least"; the painter unknown; the location (cave, island, country). A grader must not require: one single answer, a named prehistoric painter, or the old 45,500 or 64,800 figures as the current record.

### G3 (sanity). "What is the most expensive painting?"
At public auction: Salvator Mundi, attributed to Leonardo da Vinci, Christie's New York, 15 November 2017, $450,312,500 including premium ($400 million hammer). Sources: Wikidata P2284 (no reference) and Arab News, 16 Nov 2017, both read 2026-10-21. Second: Klimt, *Portrait of Elisabeth Lederer*, Sotheby's New York, 18 Nov 2025, $236.4 million (search snippets only). Private sales (for example the reported de Kooning and Cézanne sales) were not checked in this pass. A grader must require the attribution caveat ("attributed to"; disputed). Confidence: high on the auction price, low on any private-sale reading.

## Proposals for artwright
- Hand-off contract: artwright owns the reference interview and the art vocabulary (what counts as a painting, vase or Ming piece; hammer against premium; the attribution qualifiers; dynasty and reign labels; figurative against non-figurative). It passes historywright a pinned question: entity, reading, required properties (date, price, place, owner) and the candidate list. historywright returns its standard answer block (cited answer, confidence, sources-disagree note, exact quotes, retrieval dates), and artwright wraps it in the art-specific verdict. artwright never rebuilds a source registry and uses historywright's `hw.py wd`, `oa`, `doi`, `verify quote` and `verify sources` routes.
- Superlative procedure (`oldest`, `largest`, `most expensive`, `first`): 1) name the readings; 2) for each reading, find the current holder and check whether the record has been broken since (search the year to date); 3) check the category: dynasty and reign, medium (painting against stencil or drawing), and attribution; 4) for prices, record currency, date, hammer or premium, public or private, and paid or unpaid; 5) two independent sources, Guinness and Wikipedia never among them; 6) for dates, check minimum against range against estimate.
- Add the attribution glossary as a reference file, quoting Sotheby's verbatim and noting that each house's own glossary governs its lots.
- Propose these registry additions to historywright-sources, not to an artwright copy: Getty Provenance Index CSV (tier 1, download); Museo Egizio (CC0); price databases (artprice, artnet, MutualArt, Invaluable, LiveAuctioneers, Sotheby's and Christie's results, Art Sales Index) as `link-out` with "paid / blocks AI agents" notes; Interpol, Art Loss Register, Lost Art, Proveana and IFAR as link-out with their access status. Add the Art Basel and UBS report as a tier-1 market source.
- Never scrape the price databases, and never sign in to auction results. When a price sits behind a login, the answer says so and cites the best open copy (a trade press report on the sale date).
- Quote verification reads raw pages, through `hw.py verify quote` or an HTML grep, never a summariser's paraphrase (F9).
- Evals: G1 and G2 as cases with must and must-not lists. Add trap cases: "most expensive Ming vase" where the Qianlong vase must not be called Ming; "oldest painting" where 51,200 must not be called the oldest of any kind; "who painted Lascaux" where the answer is unknown; the "Probably Republican" vase sale.
- Optional route: rijksmuseum-mcp-plus for Rijksmuseum provenance, with its own "not authoritative" warning carried into the answer. Provenio stays a lead only.
- Answer footer as in historywright, plus a "Market qualifiers:" line (hammer or premium, currency, date, public or private) on any price answer.
- Record cache: store each gold with its retrieval date and re-check it at least every 180 days, since records fall (the 2026 cave-art paper is the example).

## Overall magnitude: n/a (initial)
## Open questions: still open: any Ming vase above HK$168.66m sold in 2012–2026 (archives behind logins); Art Sales Index terms; Lost Art, Proveana and IFAR access (bot walls and an expired certificate); oldest signed painting across all media; technical art history evidence norms; whether the Getty Provenance LOD has shipped.
## Search plan notes: subject: Crossref and OpenAlex by DOI beat publisher pages (nature.com redirects to a login); Wikidata wbgetclaims with a contact User-Agent works; the Met v1 objects endpoint works. Noise: Wikipedia dates, Guinness. Blocked: christies.com (search tool refused), artnet, ATG, The Drinks Business and Business Standard (403), lostart and proveana (BotStopper), ifar (expired certificate), getty.edu (redirect chain, content truncated). Tooling: GitHub repository search sorted by updated date found the MCP servers; code search for SKILL.md found nothing. Practice and testing: mined from the failures in this pass.
## Tracks covered: subject: 13 queries · tooling: 2 (plus GitHub API and robots.txt checks) · practice: 2 · testing: 0 (from the historywright method)
## Upcoming events: Art Basel and UBS Art Market Report 2027 (expected spring 2027) · Getty Provenance Index LOD release (no date) · Hong Kong autumn sales (late October and November 2026), possible new Ming results
## Nothing changed: no
## Cost: searches 18 (1 refused) · fetches 36 · tool calls 72
