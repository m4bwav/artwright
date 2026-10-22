---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- judges the pair in both orders (two recorded orders in matches.jsonl or two separate judgements in the trace) and names the original as better
- ties each reason to a region; no 'looks good'
FAIL if any is missing or contradicted.
