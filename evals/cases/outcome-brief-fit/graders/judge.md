---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- verdict DOES NOT FIT, with at least three of the brief's checks named as failing (birds, blue, branch, side view, night sky, HELLO text)
- says the verdict was written to a verdict.json (a validation note is enough; the file itself is not shown)
FAIL if any is missing or contradicted.
