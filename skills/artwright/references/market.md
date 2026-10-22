# Art market facts

How to answer "oldest", "most expensive", "first" and price questions about art without repeating the open web's errors.

Checked 2026-10-21 · Back to [SKILL.md](../SKILL.md)

artwright owns the reading and the vocabulary (painting or stencil, Ming or Qing, hammer or premium, "attributed to"). The fact itself comes from historywright: pass it a pinned question (entity, reading, properties wanted, candidate list) and wrap its cited answer.

## The superlative procedure

1. **Name the readings.** "Most expensive Ming vase" splits into: strictly Ming (1368–1644) at public auction; any Ming porcelain; private sales included; the popular sense (any old Chinese vase). Answer each reading you can, and say which one the headline number answers.
2. **Find the holder per reading, then check the year to date** for a newer record. Records fall (the oldest dated cave art changed in January 2026).
3. **Check the category:** dynasty and reign (a Qianlong piece is Qing, not Ming), medium (painting, stencil or drawing), object type (cup or vase), and the attribution qualifier below.
4. **For prices record:** currency, sale date, hammer or premium, public auction or private sale, paid or unpaid (a hammer the buyer never paid is not a sale).
5. **Two independent sources.** Guinness and Wikipedia are finders only, never one of the two. Wikipedia misdated the chicken cup sale to August; Guinness calls a Qing vase "the most expensive vase".
6. **Minimum ages:** U-series and similar dates are lower bounds. Write "at least 67,800 years", never "67,800 years old".

End with historywright's confidence line, a sources-disagree note, and on any price:

`Market qualifiers: <hammer | premium included> · <currency and amount> · <sale date> · <house, city> · <public | private> · <paid | unpaid | unknown>`

## Hammer and premium

The hammer price is the winning bid. The premium is the house's fee added to it; most reported records are premium-included totals (Salvator Mundi: $400 million hammer, $450,312,500 with premium). Never compare a hammer figure with a premium figure, and never convert currencies yourself when a source gives the converted figure for the sale date.

## Catalogue qualifiers (Sotheby's, verbatim)

Source: Sotheby's Glossary of Terms, https://help.sothebys.com/en/support/solutions/articles/44002518846, read raw 2026-10-21 (a fetch summariser had truncated "Attributed to"; quote from raw HTML). verified: yes. Each house's own glossary governs its own lots; Christie's wording was not read (christies.com refused the tools), so do not assume it matches. One dealer treats "Manner of" as "Follower of".

- General: "Any statement as to authorship, attribution, origin, date, age, provenance and condition is a statement of opinion and is not to be taken as a statement of fact."
- GIOVANNI BELLINI: "In our opinion a work by the artist."
- ATTRIBUTED TO: "In our opinion probably a work that was created at a time when the artist mentioned was active and there are serious grounds to believe that it is by the artist's hand, but less certainty as to authorship is expressed than in the preceding category."
- STUDIO OF: "In our opinion a work by an unknown hand in the studio of the artist which may or may not have been executed under the artist's direction."
- CIRCLE OF: "In our opinion a work by an artist as yet unidentified but distinct hand, closely associated with the named artist but not necessarily his pupil."
- FOLLOWER OF: "In our opinion a work by an artist, working in the style of the artist, contemporary or close to his time but not inevitably his pupil."
- STYLE OF OR MANNER OF: "In our opinion a work in the style of the artist and of a later date."
- AFTER: "In our opinion a copy of a known work of the artist."
- Signed: "from the hand of the artist"; bears a signature: "added by another hand".
- Chinese ceramics: "If there is no attribution in bold under the catalogue entry for an item, it means that we are unable to determine the period attributed to such item." and "Where no attribution is given to an item, it is our opinion that the period of origin of such item is unclear or that it is from the 19th or 20th century."

Museum records carry the same idea as data: the Met's API returns `"artistPrefix": "Attributed to"` (object 255574, Sophilos). Read Wikidata creators with their P5102 qualifier, never the bare value.

## Price databases: link out, never query

Paid, and most forbid automation. The plugin never scrapes them or signs in; the user reads them. When a result sits behind a login, say so and cite the best open copy (trade press on the sale date). verified: yes, 2026-10-21.

| Service | Status | verified (source) |
|---|---|---|
| artnet Price Database | "You may not use any robot, spider, other automatic device, or manual process to monitor or copy" | yes (terms page, updated 2023-04-27) |
| Artprice | "# BLOCK AI/Scrapers", names ClaudeBot and anthropic-ai | yes (robots.txt) |
| MutualArt | full results on Premium and VIP plans only | yes (FAQ) |
| Invaluable, LiveAuctioneers | crawl delays; results pages are for people | yes (robots.txt) |
| Sotheby's results | "Log in to view results" | yes (lot page, research pass) |
| Christie's results | refused to the search tool | yes (search tool) |
| Art Sales Index | site unreachable; terms unchecked | no |

## Worked examples (recheck by 2027-04-19)

**Most expensive Ming vase.** verified: yes.
- Strictly Ming, public auction: Yongle blue-and-white meiping with fruit sprays (Meiyintang), Sotheby's Hong Kong, October 2011 (HK0377 lot 11), HK$168,660,000 premium included (about US$21.6 million). Confidence medium: one trade report (Antiques & Art Ireland, 2011-10-05) plus the Sotheby's catalogue; result behind a login; 2012–2026 archives not fully searchable, and a 2026-10-21 search found no newer record.
- Any Ming porcelain: Chenghua "chicken cup", Sotheby's Hong Kong, 8 April 2014, HK$281.24 million premium included (HK$250 million hammer). A cup, not a vase. Confidence high.
- Trap: Guinness's "most expensive vase" is the Qianlong (Qing) Bainbridges vase: £43 million hammer in 2010, never paid, later sold privately. Not Ming.

**Oldest surviving painting.** verified: yes (Nature records via Crossref and OpenAlex).
- Oldest dated cave art: hand stencil, Liang Metanduno, Muna Island, Sulawesi, at least 67,800 years (Oktaviana et al., Nature, 21 January 2026). High on the date; "is a stencil a painting" is the reading.
- Oldest figurative scene: Leang Karampuang, Sulawesi, at least 51,200 years (Nature 2024). Never give 51,200 unqualified.
- Neanderthal Spanish art (over 64,800 years) is disputed. Painting on cloth: Gebelein linen, Museo Egizio, 3600–3350 BCE. Greek panel: Pitsa panels, c. 550–500 BC.
- Painter: unknown for every prehistoric work. Earliest painters known by name are Greek vase painters (Sophilos, c. 590–570 BCE; medium confidence).

**Most expensive painting.** verified: yes for the price; no for the runner-up (search snippets).
- Salvator Mundi, attributed to Leonardo (attribution disputed), Christie's New York, 15 November 2017, $450,312,500 premium included. Confidence high on the auction price, low on any private-sale reading.
- Second: Klimt, *Portrait of Elisabeth Lederer*, Sotheby's New York, 18 November 2025, $236.4 million.
