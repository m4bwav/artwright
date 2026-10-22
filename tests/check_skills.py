"""Structure and public-safety checks for the artwright repository. Standard library only.

Run from the repository root: python tests/check_skills.py
Checks: the plugin manifest; each skill's frontmatter, description length and body length; relative links in every
markdown file; every reference file reachable from its SKILL.md; knowledge files dated and carrying verified flags;
LF line endings; no images outside .github/images; no secrets, no home-folder paths, no AI attribution; the evergreen
companions; aw.py runs and prints JSON.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".toml", ".cfg", ".hex", ".gpl"}
IMAGES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "dist", "node_modules", ".fixtures-cache"}
SKIP_PREFIXES = ("evals/cases/results/", "evals/fixtures/out/")  # local eval output and fixtures, git-ignored
DESC_MAX = 700  # this repository's budget; the Agent Skills spec allows 1,024
BODY_MAX = 200
# Knowledge files must say when they were checked and flag what is verified.
KNOWLEDGE = ["skills/artwright/references/%s.md" % n for n in
             ("movements", "theory", "traditions", "evidence", "craft", "ceramics", "market", "law")] + \
            ["skills/artwright-judge/references/%s.md" % n for n in ("vocabulary", "ai-look")] + \
            ["skills/artwright-pixel/references/%s.md" % n for n in ("pixel-art", "sprites-tiles")]
problems = []


def rel(p):
    return p.relative_to(ROOT).as_posix()


def files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS) and not rel(p).startswith(SKIP_PREFIXES):
            yield p


def check_manifest():
    try:
        m = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        problems.append("plugin.json unreadable: %s" % e)
        return
    for k in ("name", "version", "description", "skills", "license", "repository"):
        if not m.get(k):
            problems.append("plugin.json missing %s" % k)
    if not re.fullmatch(r"\d+\.\d+\.\d+", m.get("version", "")):
        problems.append("plugin.json version is not X.Y.Z")
    aw = (ROOT / "skills" / "artwright" / "scripts" / "aw.py").read_text(encoding="utf-8")
    v = re.search(r'VERSION = "([^"]+)"', aw)
    if not v or v.group(1) != m.get("version"):
        problems.append("aw.py VERSION must match plugin.json version")


def check_skills():
    for sk in sorted((ROOT / "skills").iterdir()):
        if not sk.is_dir():
            continue
        f = sk / "SKILL.md"
        if not f.exists():
            problems.append("%s has no SKILL.md" % rel(sk))
            continue
        t = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", t, re.S)
        if not m:
            problems.append("%s: no frontmatter" % rel(f))
            continue
        fm = m.group(1)
        name = re.search(r"(?m)^name:\s*(.+)$", fm)
        desc = re.search(r'(?m)^description:\s*"?(.*?)"?\s*$', fm)
        if not name or name.group(1).strip() != sk.name:
            problems.append("%s: name must be %s" % (rel(f), sk.name))
        if not desc:
            problems.append("%s: no description" % rel(f))
        elif len(desc.group(1)) > DESC_MAX:
            problems.append("%s: description is %d characters (budget %d)" % (rel(f), len(desc.group(1)), DESC_MAX))
        body = t[m.end():].count("\n")
        if body > BODY_MAX:
            problems.append("%s: body is %d lines (budget %d)" % (rel(f), body, BODY_MAX))
        if "## Maintenance" not in t:
            problems.append("%s: no Maintenance section" % rel(f))


LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def md_links(p):
    text = re.sub(r"```.*?```", "", p.read_text(encoding="utf-8"), flags=re.S)
    for target in LINK.findall(text):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        path = target.split("#")[0]
        if path:
            yield target, (p.parent / path).resolve()


def check_links():
    for p in files():
        if p.suffix == ".md":
            for target, dest in md_links(p):
                if not dest.exists():
                    problems.append("%s: broken link %s" % (rel(p), target))


def check_reachable():
    """Every file under a skill's references/ is linked from its SKILL.md, directly or through another reference."""
    for sk in sorted((ROOT / "skills").iterdir()):
        refs = sk / "references"
        if not refs.is_dir():
            continue
        seen, todo = set(), [sk / "SKILL.md"]
        while todo:
            p = todo.pop()
            if p in seen or not p.is_file() or p.suffix != ".md":
                continue
            seen.add(p)
            todo += [d for _, d in md_links(p)]
        for f in refs.rglob("*.md"):
            if f.resolve() not in {s.resolve() for s in seen}:
                problems.append("%s: not linked from %s/SKILL.md (unreachable)" % (rel(f), sk.name))


def check_knowledge():
    for k in KNOWLEDGE:
        p = ROOT / k
        if not p.exists():
            problems.append("knowledge file missing: %s" % k)
            continue
        t = p.read_text(encoding="utf-8")
        if not re.search(r"(?i)checked[^\n]{0,20}20\d\d-\d\d-\d\d", t):
            problems.append("%s: no 'Checked YYYY-MM-DD' line" % k)
        if not re.search(r"(?i)verified|\bv: (yes|no)|\| v \|", t):
            problems.append("%s: no verified flags" % k)


TOKEN = re.compile(r"[A-Za-z0-9_\-]{40,}")
HOME = re.compile(r"(?i)([a-z]:[\\/]+users[\\/]+\w+|/users/(?!shared)[a-z0-9_]+/|/home/[a-z0-9_]+/|[a-z]:[\\/]+m4bwa)")
ATTRIB = re.compile(r"(?i)(co-authored-by:\s*claude|generated with \[?claude|\U0001F916 generated)")


def looks_like_token(s, line):
    if not (re.search(r"[0-9]", s) and re.search(r"[A-Za-z]", s)):
        return False
    if re.fullmatch(r"[0-9a-f]{40,64}", s):  # git and sha256 hashes
        return False
    if re.fullmatch(r"[A-Za-z0-9]+([-_][A-Za-z0-9]+){3,}", s) and not re.search(r"[A-Za-z0-9]{24,}", s):
        return False  # kebab or snake names and dated file names, not secrets
    i = line.find(s)
    word_start = max(line.rfind(" ", 0, i), line.rfind("(", 0, i), line.rfind('"', 0, i), line.rfind("<", 0, i))
    if "://" in line[word_start + 1:i] or line[max(0, i - 1):i] in ("/", "=", "."):
        return False  # part of a URL path or query
    return True


def check_text():
    for p in files():
        r = rel(p)
        if p.suffix.lower() in IMAGES:
            if not r.startswith(".github/images/"):
                problems.append("%s: images stay out of the repository (fixtures are drawn in code or fetched)" % r)
            continue
        if p.suffix not in TEXT and p.name not in (".gitignore", ".gitattributes"):
            continue
        data = p.read_bytes()
        if b"\r\n" in data:
            problems.append("%s: CRLF line endings (use LF)" % r)
        text = data.decode("utf-8", "replace")
        for n, line in enumerate(text.splitlines(), 1):
            if r != "tests/check_skills.py":
                for tok in TOKEN.findall(line):
                    if looks_like_token(tok, line):
                        problems.append("%s:%d: token-like string (%d chars); keys never go in the repository" % (r, n, len(tok)))
                if HOME.search(line):
                    problems.append("%s:%d: home-folder or owner path; generalise it" % (r, n))
                if ATTRIB.search(line):
                    problems.append("%s:%d: AI attribution line" % (r, n))


def check_evergreen():
    for f in ("evergreen.json", "RESEARCH.md", "CHANGELOG.md", "LEARNINGS.md", "TESTS.md", "MAINTENANCE.md",
              "evals/evals.json"):
        p = ROOT / f
        if not p.exists():
            problems.append("evergreen companion missing: %s" % f)
        elif p.suffix == ".json":
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except ValueError as e:
                problems.append("%s: %s" % (f, e))


def check_cli():
    aw = ROOT / "skills" / "artwright" / "scripts" / "aw.py"
    r = subprocess.run([sys.executable, str(aw), "doctor"], capture_output=True, text=True, encoding="utf-8")
    try:
        d = json.loads(r.stdout)
        if not d.get("python_ok"):
            problems.append("aw.py doctor: python_ok is false")
    except ValueError:
        problems.append("aw.py doctor printed no JSON: %s" % (r.stderr or r.stdout)[:300])


if __name__ == "__main__":
    check_manifest()
    check_skills()
    check_links()
    check_reachable()
    check_knowledge()
    check_text()
    check_evergreen()
    check_cli()
    for p in problems:
        print("FAIL", p)
    print("check_skills: %d problem(s)" % len(problems))
    sys.exit(1 if problems else 0)
