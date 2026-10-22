---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- verdict DOES NOT FIT with at least three hard fails named (not birds, not blue, no branch/night/text)
- writes artwright/verdict.json and it validates
FAIL if any is missing or contradicted.
