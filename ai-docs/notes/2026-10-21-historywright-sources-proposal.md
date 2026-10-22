# Proposal: art sources for historywright-sources

Draft registry changes for the sister plugin historywright, so artwright's fact questions (provenance, Egyptian objects, auction prices) route through its source registry (ruling R6). Not applied: a historywright session opens the pull request against `skills/historywright-sources/references/registry.json` and, for item 3, `skills/historywright/scripts/hw.py`.

Written 2026-10-21 by the artwright Step 2 knowledge pass. Every route below was checked with one direct request that day. The proposed entries plus the AIC edit were linted with historywright's own `lint_registry` (no problems, no warnings).

## Summary

| Change | What | Checked 2026-10-21 by |
|---|---|---|
| add `getty-provenance` | Getty Provenance Index CSV exports, tier 1, bulk-only, CC0 per dataset | GitHub API on thegetty/provenance-index-csv (pushed 2026-01-26, not archived, tags v1-v3); README and the three dataset READMEs (CC0 1.0 each); HEAD on the S3 knoedler.csv (200, 18,060,930 bytes, last modified 2022-08-01); old getty.edu search URL 308-redirects to the current provenance page (200) |
| add `museo-egizio` | Turin collection online, tier 1, browse-only, images CC0 | record page S_17138 (200; "3600–3350 BCE", "Naqada II", "Suppl. 17138", CC0 sentence); HTML search `description=linen` (200, 85 record links); robots.txt; /api/ 302 (no API) |
| add 8 link-out price sources | artnet-pdb, artprice, mutualart, invaluable, liveauctioneers, sothebys-results, christies-results, art-sales-index | artnet terms page (200, robot clause, "Last Updated: April 27th, 2023"); artnet robots 403; artprice robots ("# BLOCK AI/Scrapers", ClaudeBot); MutualArt FAQ (Premium/VIP); robots.txt of Invaluable, LiveAuctioneers, Sotheby's, Christie's; artsalesindex.com unreachable |
| edit `artic` | add the `AIC-User-Agent` header; access `ua-required` | see item 2: the current entry fails |
| edit `hw.py probe` | send a source's search headers when probing | see item 3 |
| `met` | no change needed | v1 search 410, v1.1 search 200 (`{"total":7619,...}`), v1 objects/255574 200; the entry already uses v1.1 and `retired` already lists `met-v1-search` |

Each new entry cites `"research": "R-20261021-1"` as a placeholder: the historywright session gives it the next free id in historywright's own RESEARCH.md (artwright's matching entries are R-20261021-13 and -22).

## 1. New entries (append to `sources`)

```json
{
 "id": "getty-provenance",
 "name": "Getty Provenance Index (CSV exports)",
 "use": "Art-market provenance: Knoedler and Goupil stock books and auction sales catalogue contents, with buyers, sellers and prices",
 "kind": "catalogue",
 "regions": [
  "europe",
  "us"
 ],
 "eras": [
  "early-modern",
  "modern"
 ],
 "tier": 1,
 "licence": "CC0 1.0 per dataset README (Knoedler, Sales Catalogs, Goupil)",
 "access": "bulk-only",
 "key": null,
 "host": "github.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://github.com/thegetty/provenance-index-csv",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "Getty Research Institute. CSV files on S3, linked from each dataset README (knoedler.csv 18 MB, sales_contents_1-5.csv 107-260 MB each, goupil.csv 52.5 MB); S3 files last modified 2022-08-01, tags v1-v3 (v3 = 2022-06-01), repo last push 2026-01-26. README: 'These data will eventually be superseded by the Linked Open Data release' and 'rights may vary between datasets'. Search the live index at https://www.getty.edu/research-conservation/tools-databases/provenance/ (browse-only). Download once and grep locally; never page the S3 files per question.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "museo-egizio",
 "name": "Museo Egizio, Turin: collection online",
 "use": "Egyptian objects with dates, period, provenance and inventory number (Suppl., Cat., S.)",
 "kind": "museum",
 "regions": [
  "africa",
  "mediterranean"
 ],
 "eras": [
  "prehistory",
  "ancient"
 ],
 "tier": 1,
 "licence": "images CC0 1.0 ('freely downloadable and reusable under a Creative Commons CC0 Public Domain licence'); data provided 'as is'",
 "access": "browse-only",
 "key": null,
 "host": "collezioni.museoegizio.it",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://collezioni.museoegizio.it/en-GB/search/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "No JSON API found (/api/ redirects). HTML search works: /en-GB/search/?action=s&description={q}&searchLng=en-GB; record pages /en-GB/material/{id} (e.g. S_17138, the Gebelein painted linen, '3600-3350 BCE', Naqada II). robots.txt disallows only /xml/, /js/, /libs/, /Error.aspx.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "artnet-pdb",
 "name": "artnet Price Database",
 "use": "Auction results for fine and decorative art (subscription)",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "paid",
 "key": null,
 "host": "www.artnet.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.artnet.com/price-database/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "Terms (last updated 2023-04-27): 'You may not use any robot, spider, other automatic device, or manual process to monitor or copy' the site; subscriptions forbid derivative products. robots.txt answered 403. Link out; the user reads it.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "artprice",
 "name": "Artprice",
 "use": "Auction results and artist price indices (subscription)",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "paid",
 "key": null,
 "host": "www.artprice.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.artprice.com/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "robots.txt opens '# BLOCK AI/Scrapers' and disallows anthropic-ai, ClaudeBot and Claude-Web by name. Link out only.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "mutualart",
 "name": "MutualArt",
 "use": "Auction results and artist data (subscription tiers)",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "paid",
 "key": null,
 "host": "www.mutualart.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.mutualart.com/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "FAQ: full results on Premium and VIP plans; Essentials covers recent results only. Link out only.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "invaluable",
 "name": "Invaluable",
 "use": "Online auctions and past results from many houses",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "browse-only",
 "key": null,
 "host": "www.invaluable.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.invaluable.com/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "robots.txt sets crawl delays (1-10 s by agent). Past-result detail often needs an account. Link out; cite the auction house's own lot page where open.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "liveauctioneers",
 "name": "LiveAuctioneers",
 "use": "Online auctions and price results from many houses",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "browse-only",
 "key": null,
 "host": "www.liveauctioneers.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.liveauctioneers.com/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "robots.txt Crawl-delay: 10. Link out only.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "sothebys-results",
 "name": "Sotheby's lot pages and results",
 "use": "Catalogue entries, estimates and results for Sotheby's sales",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "browse-only",
 "key": null,
 "host": "www.sothebys.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.sothebys.com/en/results",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "Lot pages are open (title, period, estimate); results say 'Log in to view results'. robots.txt crawl delays up to 15 s. Never sign in. Cite the lot page for what it shows and trade press on the sale date for the price. Attribution terms: https://help.sothebys.com/en/support/solutions/articles/44002518846.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "christies-results",
 "name": "Christie's lot pages and results",
 "use": "Catalogue entries and results for Christie's sales",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "browse-only",
 "key": null,
 "host": "www.christies.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.christies.com/en/results",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "The web search tool refused christies.com ('not accessible to our user agent') on 2026-10-21; robots.txt answered 200. Link out; the user reads it.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

```json
{
 "id": "art-sales-index",
 "name": "Art Sales Index",
 "use": "Auction results database (subscription)",
 "kind": "catalogue",
 "regions": [
  "world"
 ],
 "eras": [
  "modern",
  "contemporary"
 ],
 "tier": 2,
 "licence": "proprietary",
 "access": "paid",
 "key": null,
 "host": "www.artsalesindex.com",
 "pace_s": 0.5,
 "route": "link-out",
 "url": "https://www.artsalesindex.com/",
 "search": null,
 "detail": null,
 "probe": null,
 "notes": "Unreachable on 2026-10-21 (https connect failed; http empty reply). Terms unchecked. Re-check before linking; drop to retired if still down at the next refresh.",
 "checked": "2026-10-21",
 "research": "R-20261021-1"
}
```

## 2. Edit `artic` (the current route is broken)

Tested 2026-10-21 with curl against `https://api.artic.edu/api/v1/artworks/search?q=helmet&limit=1&fields=id,title`:

| Request | Status |
|---|---|
| no extra header (curl, browser or historywright-style User-Agent) | 403 (Cloudflare) |
| `AIC-User-Agent: historywright` (any value tried: name, name with URL, name with email) | 200 |
| `AIC-User-Agent` with an empty `User-Agent` | 403 |

`python hw.py src artic helmet` from the current historywright checkout returned `"error": "HTTP 403"`; the same command against a copy of the registry with the header added returned 10 results. `python hw.py probe --only artic,met` reported artic `blocked` (403) and met `ok`.

Field edits:

```json
"access": "ua-required",
"search": {
 "url": "https://api.artic.edu/api/v1/artworks/search?q={q}&limit=10&fields=id,title,date_display,image_id,is_public_domain",
 "headers": {"AIC-User-Agent": "historywright (https://github.com/m4bwav/historywright)"},
 "items": "data",
 "fields": {"title": "title", "date": "date_display", "id": "id", "image_id": "image_id", "public_domain": "is_public_domain"},
 "link": "https://www.artic.edu/artworks/{id}"
},
"notes": "Cloudflare answers 403 unless the request carries an AIC-User-Agent header (checked 2026-10-21; the docs call it optional). 60 requests/min per IP. Image URL: https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg. Nightly dumps on GitHub art-institute-of-chicago/api-data.",
"checked": "2026-10-21"
```

Source: https://api.artic.edu/docs/ (itself 403 to curl without the header on 2026-10-21; the header name comes from the docs as read in the artwright research pass, R-20261021-13).

## 3. Edit `hw.py` `cmd_probe` so header-gated sources probe correctly

`cmd_probe` sends only the `ua: plain` User-Agent, so with the AIC fix the search works but the probe keeps reporting `blocked`. Replace the `hdr = ...` line with:

```python
        hdr = dict((s.get("search") or {}).get("headers") or {})
        if s.get("ua") == "plain":
            hdr["User-Agent"] = ("historywright " + contact()).strip()
        r = fetch(url, accept=pr.get("accept", "application/json,*/*"), headers=hdr or None, retries=0)
```

and add a unit test that a source with `search.headers` passes them to `fetch` in `probe`.

## 4. `met`: notes only

The entry is current. Optional: bump `checked` to 2026-10-21 and add to `notes`: "The v1 objects record carries artistPrefix, the museum's attribution qualifier: keep it with the name (object 255574: 'Attributed to' Sophilos)."

## Left out on purpose

- Interpol Stolen Works of Art, Art Loss Register, Lost Art, Proveana, IFAR and the Art Basel and UBS market report were proposed in the research pass (f-facts-markets F6, F8) but not re-checked in this pass; add them in the same PR only after one direct request each (Lost Art and Proveana served a bot wall and IFAR an expired certificate on 2026-10-21 in the research pass).
- No price database gets a `search` block: `lint_registry` already enforces "paid sources are link-out only", and artnet's and Artprice's terms forbid automated access.
