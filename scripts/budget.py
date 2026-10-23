"""Size budget for artwright: what every session loads (skill descriptions) and what an install weighs.

Run from the repository root: python scripts/budget.py   (red fails; yellow is reported)
Bands (synthesis section 3, ai-docs/research/2026-10-21-creation-pass.md): install green under 500 KB, yellow to
1 MB; aw.py and aw_measure.py each green under 60 KB, yellow to 100 KB; knowledge files green under 200 KB, yellow to 300 KB;
vocabulary.md red above 40 KB; descriptions green under 600 tokens in all, yellow to 900.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALLED = ["skills", ".claude-plugin", "README.md", "LICENSE", "SECURITY.md"]


def band(v, green, yellow):
    return "green" if v < green else ("yellow" if v <= yellow else "red")


def size(p):
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and "__pycache__" not in f.parts)


def main():
    rows = []
    inst = sum(size(ROOT / p) for p in INSTALLED if (ROOT / p).exists())
    rows.append(("install size", "%d KB" % (inst // 1024), band(inst, 500 * 1024, 1024 * 1024)))
    for script in ("aw.py", "aw_measure.py"):
        aw = size(ROOT / "skills" / "artwright" / "scripts" / script)
        rows.append((script, "%d KB" % (aw // 1024), band(aw, 60 * 1024, 100 * 1024)))
    know = sum(size(f) for f in (ROOT / "skills").glob("*/references/**/*.md"))
    rows.append(("knowledge files", "%d KB" % (know // 1024), band(know, 200 * 1024, 300 * 1024)))
    voc = ROOT / "skills" / "artwright-judge" / "references" / "vocabulary.md"
    v = size(voc) if voc.exists() else 0
    rows.append(("vocabulary.md", "%d bytes" % v, "green" if v <= 40000 else "red"))
    chars = 0
    for f in (ROOT / "skills").glob("*/SKILL.md"):
        m = re.search(r'(?m)^description:\s*"?(.*?)"?\s*$', f.read_text(encoding="utf-8"))
        chars += len(m.group(1)) if m else 0
    tokens = chars // 4
    rows.append(("descriptions (every session)", "~%d tokens" % tokens, band(tokens, 600, 900)))
    for name, val, b in rows:
        print("%-30s %-14s %s" % (name, val, b))
    reds = [r for r in rows if r[2] == "red"]
    if reds:
        print("RED: %s" % ", ".join(r[0] for r in reds))
    return 1 if reds else 0


if __name__ == "__main__":
    sys.exit(main())
