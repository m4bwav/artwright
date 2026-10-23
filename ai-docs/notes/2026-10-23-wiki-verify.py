"""Wiki verification for artwright (aw.py and aw_measure.py), run against a fresh clone of a release tag.

2026-10-23 (0.3.0): copies aw_measure.py beside aw.py, and adds the light, gamut, accents, depth and comp cases,
the measure-facing degrade kinds, a rank cycle, and the cache sampling key and --shown-first.

python wiki-verify.py CLONE WORKROOT [--python EXE] [--no-pillow] > out.txt

Draws every fixture in code inside WORKROOT/fox (never the repository), copies aw.py there, and runs each page's
command or snippet through bash with `python` pointing at the chosen interpreter (with Pillow hidden when asked).
HOME (and USERPROFILE) point at WORKROOT/home, so the default ARTWRIGHT_HOME is WORKROOT/home/.artwright.
The saved output masks WORKROOT/home as /home/you (as the pages show it) and ISO timestamps as <time>.
"""

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
PY = sys.argv[sys.argv.index("--python") + 1] if "--python" in sys.argv else sys.executable
NO_PILLOW = "--no-pillow" in sys.argv
sys.path.insert(0, str(CLONE / "skills" / "artwright" / "scripts"))
import aw  # noqa: E402

if ROOT.exists():
    shutil.rmtree(ROOT)
WORK, HOMEDIR, SHIM = ROOT / "fox", ROOT / "home", ROOT / "shim"
for d in (WORK, HOMEDIR, SHIM):
    d.mkdir(parents=True)


# ------------------------------------------------------------------ fixtures, drawn in code

def scene(w, h, sky_top, sky_low, sun, ground):
    """A snowy dusk or noon landscape: sky gradient, a sun disc, two mountain bands, snow and a small fox."""
    d = bytearray(w * h * 4)
    hz = int(h * 0.62)
    for y in range(h):
        t = min(1.0, y / hz)
        sky = tuple(int(sky_top[c] + (sky_low[c] - sky_top[c]) * t) for c in range(3))
        for x in range(w):
            ridge1 = hz - int(h * 0.18 * (1 - abs((x / w) * 2.2 - 0.9)) ** 2)
            ridge2 = hz - int(h * 0.10 * (1 - abs((x / w) * 1.6 - 1.2)) ** 2)
            if y >= hz:
                c = ground
                fx, fy = (x - w * 0.62) / (w * 0.06), (y - h * 0.78) / (h * 0.035)
                if fx * fx + fy * fy <= 1:
                    c = (196, 86, 30)
            elif y >= ridge2:
                c = (60, 64, 92)
            elif y >= ridge1:
                c = (40, 40, 66)
            else:
                dx, dy = x - sun[0] * w, y - sun[1] * h
                c = (255, 214, 140) if dx * dx + dy * dy < (h * 0.06) ** 2 else sky
            i = (y * w + x) * 4
            d[i:i + 4] = bytes((c[0], c[1], c[2], 255))
    return aw.Img(w, h, d)


aw.save_png(scene(2000, 1200, (28, 30, 74), (236, 128, 70), (0.25, 0.5), (226, 232, 240)), WORK / "dusk.png")
aw.save_png(scene(2000, 1200, (70, 140, 220), (190, 220, 245), (0.7, 0.15), (240, 244, 250)), WORK / "noon.png")
try:  # a JPEG for the no-Pillow decode route; drawn with Pillow when this interpreter has it
    from PIL import Image
    with Image.open(WORK / "dusk.png") as im:
        im.convert("RGB").resize((800, 480)).save(WORK / "photo.jpg", quality=90)
except ImportError:
    pass

subprocess.run([sys.executable, str(CLONE / "evals" / "fixtures" / "make_fixtures.py")], check=True,
               capture_output=True)
FX = CLONE / "evals" / "fixtures" / "out"
shutil.copy(FX / "sprite_clean.png", WORK / "sprite.png")
shutil.copy(FX / "sprite_fake.png", WORK / "sprite_ai.png")
(WORK / "batch").mkdir()
for i in range(1, 5):
    shutil.copy(FX / "renders" / ("render_%02d.png" % i), WORK / "batch" / ("fox_%02d.png" % i))
(WORK / "renders").mkdir()
for i in range(1, 7):
    shutil.copy(FX / "renders" / ("render_%02d.png" % i), WORK / "renders" / ("render_%02d.png" % i))

# animation frames: the clean sprite at native size, the third frame lifted one pixel (a jumping baseline)
native = aw.resize_nearest(aw.load(WORK / "sprite.png"), 16, 16)
(WORK / "walk").mkdir()
for k, lift in enumerate((0, 0, 1)):
    f = aw.Img(16, 16)
    for y in range(16):
        for x in range(16):
            if 0 <= y + lift < 16:
                f.put(x, y, native.px(x, y + lift))
    aw.save_png(aw.resize_nearest(f, 64, 64), WORK / "walk" / ("walk_%d.png" % (k + 1)))

# tiles (16x16 drawn at 4x): a checker that wraps cleanly, and speckled grass whose last three columns are a
# brown path that stops at the right edge (its left and right edges do not meet)
tile = aw.Img(16, 16)
seam = aw.Img(16, 16)
for y in range(16):
    for x in range(16):
        tile.put(x, y, (58, 120, 62) if (x // 4 + y // 4) % 2 else (90, 160, 80))
        if x >= 13:
            seam.put(x, y, (150, 100, 60))
        else:
            seam.put(x, y, (58, 120, 62) if (x * 7 + y * 3) % 11 == 0 else (90, 160, 80))
aw.save_png(aw.resize_nearest(tile, 64, 64), WORK / "grass.png")
aw.save_png(aw.resize_nearest(seam, 64, 64), WORK / "seam.png")
grad = aw.Img(16, 16)
for y in range(16):
    for x in range(16):
        grad.put(x, y, (40 + x * 12, 100, 60 + y * 10))
aw.save_png(aw.resize_nearest(grad, 64, 64), WORK / "gradient.png")
(WORK / "mypalette.hex").write_text("1a1c2c\n5d275d\nb13e53\nef7d57\nffcd75\na7f070\n", encoding="utf-8")
for name in ("aw.py", "aw_measure.py"):  # aw.py imports aw_measure.py from its own folder (0.2.0 and later)
    shutil.copy(CLONE / "skills" / "artwright" / "scripts" / name, WORK / name)

# a depth map for dusk.png in the Depth Anything convention: bright near (the bottom), dark far (the top)
dmap = aw.Img(200, 120)
for y in range(120):
    for x in range(200):
        v = int(255 * y / 119)
        dmap.put(x, y, (v, v, v))
aw.save_png(dmap, WORK / "dusk_depth.png")

# `python` on PATH: the chosen interpreter; for the no-Pillow run a stub PIL package that refuses to import comes first
shim = SHIM / "python"
shim.write_text('#!/bin/sh\nexec "%s" "$@"\n' % PY, encoding="utf-8", newline="\n")
shim.chmod(shim.stat().st_mode | stat.S_IEXEC)
if NO_PILLOW:
    (ROOT / "nopil" / "PIL").mkdir(parents=True)
    (ROOT / "nopil" / "PIL" / "__init__.py").write_text('raise ImportError("Pillow hidden for this run")\n')

ENV = dict(os.environ, HOME=str(HOMEDIR), USERPROFILE=str(HOMEDIR), PYTHONIOENCODING="utf-8",
           PATH=str(SHIM) + os.pathsep + os.environ["PATH"])
if NO_PILLOW:
    ENV["PYTHONPATH"] = str(ROOT / "nopil")
ENV.pop("ARTWRIGHT_HOME", None)
BASH = shutil.which("bash")  # on Windows, Git Bash from PATH, never System32's WSL launcher
ISO = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d")


def mask(text):
    for p in sorted({json.dumps(str(HOMEDIR))[1:-1], str(HOMEDIR), HOMEDIR.as_posix()}, key=len, reverse=True):
        text = text.replace(p, "/home/you")
    return ISO.sub("<time>", text.replace("\r\n", "\n"))


def run(label, cmd):
    """One page block: print the command as the page shows it, then stdout, stderr apart, and the exit code."""
    print("=== %s ===" % label)
    print("$ " + cmd.strip().replace("\n", "\n> "))
    r = subprocess.run([BASH, "-c", cmd], cwd=WORK, env=ENV, capture_output=True, text=True, encoding="utf-8")
    sys.stdout.write(mask(r.stdout))
    if r.stderr.strip():
        print("[stderr]")
        sys.stdout.write(mask(r.stderr))
    print("[exit %d]" % r.returncode)
    print()
    return r


def snippet(label, code):
    """A Python block from a page, run as written from a file in the work folder."""
    (WORK / "snippet.py").write_text(code, encoding="utf-8")
    return run(label, "python snippet.py")


def pair_id(a, b):
    ha, hb = (hashlib.sha256((WORK / f).read_bytes()).hexdigest() for f in (a, b))
    return hashlib.sha256("|".join(sorted((ha, hb))).encode()).hexdigest()[:12]


print("artwright wiki verification: aw.py from %s" % subprocess.run(
    ["git", "-C", str(CLONE), "log", "-1", "--format=%h %cs"], capture_output=True, text=True).stdout.strip())
print("aw.py sha256 %s" % hashlib.sha256((WORK / "aw.py").read_bytes()).hexdigest())
print("aw_measure.py sha256 %s" % hashlib.sha256((WORK / "aw_measure.py").read_bytes()).hexdigest())
print("interpreter: %s; Pillow hidden: %s; platform: %s" % (
    subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip(), NO_PILLOW, sys.platform))
print()

# ------------------------------------------------------------------ Getting started and Home

run("no command", "python aw.py")
run("version", "python aw.py --version")
run("doctor", "python aw.py doctor")
run("info dusk", "python aw.py info dusk.png")

# ------------------------------------------------------------------ Commands: looking at images

run("info several", "python aw.py info sprite.png photo.jpg")
run("fit long", "python aw.py fit dusk.png -o dusk_1024.png")
run("fit tokens", "python aw.py fit dusk.png -o dusk_small.png --tokens 400")
run("fit crop", "python aw.py fit dusk.png -o fox_crop.png --crop 1100,850,300,150")
run("fit cell", "python aw.py fit dusk.png -o cell4.png --cell 3x3:4")
run("fit pixel", "python aw.py fit sprite.png -o sprite_big.png --pixel --long 512")
run("sheet", "python aw.py sheet renders -o sheet.png")
run("sheet pixel", "python aw.py sheet renders/render_01.png renders/render_02.png -o pair.png --pixel --cols 2 --cell 256")
run("stats", "python aw.py stats dusk.png --notan notan")

# ------------------------------------------------------------------ Commands: light, colour and composition (0.2.0)

run("light", "python aw.py light dusk.png")
run("light box", "python aw.py light dusk.png --box 0,0.62,1,0.38")
run("gamut", "python aw.py gamut dusk.png --overlay gamut.png")
run("accents dusk", "python aw.py accents dusk.png")
run("accents noon", "python aw.py accents noon.png")
run("depth thirds", "python aw.py depth dusk.png")
run("depth map", "python aw.py depth dusk.png --depth dusk_depth.png")
run("comp", "python aw.py comp dusk.png")
run("comp subject", "python aw.py comp dusk.png --subject 0.56,0.745,0.12,0.07 --out masses")
run("masses written", "ls masses")
run("degrade warm-shadows", "python aw.py degrade dusk.png -o dusk_warm.png --kind warm-shadows")
run("light warm", "python aw.py light dusk_warm.png")
run("degrade glow-shadows", "python aw.py degrade dusk.png -o dusk_glow.png --kind glow-shadows")
run("light glow", "python aw.py light dusk_glow.png")
run("degrade hotspot", "python aw.py degrade dusk.png -o dusk_hot.png --kind hotspot --seed 2")
run("comp hotspot", "python aw.py comp dusk_hot.png --subject 0.56,0.745,0.12,0.07")
run("degrade tangent", "python aw.py degrade dusk.png -o dusk_tangent.png --kind tangent")
run("comp tangent", "python aw.py comp dusk_tangent.png")
run("degrade haze-off", "python aw.py degrade dusk.png -o dusk_clear.png --kind haze-off")
run("depth haze-off", "python aw.py depth dusk_clear.png")
run("degrade midgrey", "python aw.py degrade dusk.png -o dusk_grey.png --kind midgrey")
run("comp midgrey", "python aw.py comp dusk_grey.png")
run("degrade uniform-sat", "python aw.py degrade dusk.png -o dusk_flat.png --kind uniform-sat")
run("gamut uniform-sat", "python aw.py gamut dusk_flat.png")

run("palette", "python aw.py palette dusk.png -k 5")
run("palette against", "python aw.py palette sprite.png --against pico-8")
run("palette against file", "python aw.py palette sprite.png -k 4 --against mypalette.hex")
run("palette against hex", "python aw.py palette sprite.png -k 3 --against 140c1c,d27d2c,854c30")

# ------------------------------------------------------------------ Commands: pixel art

run("pixel clean", "python aw.py pixel sprite.png --budget 16 --preview sprite_x4.png")
run("pixel ai", "python aw.py pixel sprite_ai.png --budget 16")
run("pixel palette", "python aw.py pixel sprite.png --palette pico-8")
run("pixel frames", "python aw.py pixel walk --frames")
run("pixel tile", "python aw.py pixel grass.png --tile --preview grass.png")
run("pixel seam", "python aw.py pixel seam.png --tile --scale 4")
run("pixel tile false seam", "python aw.py pixel grass.png --tile --scale 4")
run("pixel tile scale", "python aw.py pixel grass.png --scale 4")
run("pixel gradient", "python aw.py pixel gradient.png")

# ------------------------------------------------------------------ Commands: batches

run("degrade", "python aw.py degrade renders/render_01.png -o renders/render_01_copy.png --kind jpeg")
run("hash", "python aw.py hash renders/render_01.png renders/render_01_copy.png")
run("dedupe", "python aw.py dedupe renders")

# ------------------------------------------------------------------ Commands: pairs and ranking (one pair)

P = pair_id("dusk.png", "noon.png")
run("compare prepare", "python aw.py compare prepare dusk.png noon.png")
run("compare record 1", "python aw.py compare record %s 1 2 --confidence medium --criteria value read" % P)
run("compare record 2", "python aw.py compare record %s 2 1 --confidence medium --criteria value read" % P)
run("rank one pair", "python aw.py rank")
run("work folder", "ls artwright artwright/pairs")

# ------------------------------------------------------------------ How images are judged: ties

run("tie prepare", "python aw.py compare prepare dusk.png noon.png --work flip")
run("tie record 1", "python aw.py compare record %s 1 1 --work flip" % P)
run("tie record 2", "python aw.py compare record %s 2 1 --work flip" % P)
run("tie re-query", "python aw.py compare record %s 1 1 --work flip" % P)
run("tie rank", "python aw.py rank --work flip")
run("double tie prepare", "python aw.py compare prepare dusk.png noon.png --work evens")
run("double tie record 1", "python aw.py compare record %s 1 tie --work evens" % P)
run("double tie record 2", "python aw.py compare record %s 2 tie --work evens" % P)
run("double tie rank", "python aw.py rank --work evens")

# ------------------------------------------------------------------ How images are judged: a cycle (0.3.0)

LOOP = ["renders/render_01.png", "renders/render_02.png", "renders/render_03.png"]
for i, a in enumerate(LOOP):
    for b in LOOP[i + 1:]:
        subprocess.run([BASH, "-c", "python aw.py compare prepare %s %s --work loop > /dev/null" % (a, b)],
                       cwd=WORK, env=ENV, check=True)
# scripted picks, the same in both orders: 01 beats 02, 02 beats 03, 03 beats 01
BEATS = {("renders/render_01.png", "renders/render_02.png"): "renders/render_01.png",
         ("renders/render_02.png", "renders/render_03.png"): "renders/render_02.png",
         ("renders/render_01.png", "renders/render_03.png"): "renders/render_03.png"}
for (a, b), win in BEATS.items():
    for o in ("1", "2"):
        left = a if o == "1" else b
        subprocess.run([BASH, "-c", "python aw.py compare record %s %s %s --work loop > /dev/null"
                        % (pair_id(a, b), o, "1" if left == win else "2")], cwd=WORK, env=ENV, check=True)
run("rank cycle", "python aw.py rank --work loop")

# ------------------------------------------------------------------ Verdict contract: a batch end to end

run("verdict init", 'python aw.py verdict init batch batch/fox_01.png batch/fox_02.png batch/fox_03.png batch/fox_04.png'
    ' --kind pairwise --brief "red fox in snow at dusk, side view, no text"')
run("verdict init kind kept", """python aw.py verdict init batch --kind critique > /dev/null
python -c "import json; print(json.load(open('batch/artwright/verdict.json'))['kind'])\"""")
run("verdict rubric", """python -c "import json; print(json.load(open('batch/artwright/verdict.json'))['rubric'])\"""")
ROUND = r"""
set -- batch/fox_01.png batch/fox_02.png batch/fox_03.png batch/fox_04.png
for a in "$@"; do
  shift
  for b in "$@"; do
    python aw.py compare prepare "$a" "$b" --work batch/artwright > /dev/null
  done
done
python aw.py rank --work batch/artwright --next 3
"""
run("round robin", ROUND)
batch = ["batch/fox_%02d.png" % i for i in range(1, 5)]
# scripted picks: fox_03 beats everyone, fox_01 beats 02 and 04, 02 against 04 split between the orders
order = {"batch/fox_03.png": 0, "batch/fox_01.png": 1, "batch/fox_04.png": 2, "batch/fox_02.png": 3}
for i, a in enumerate(batch):
    for b in batch[i + 1:]:
        pid = pair_id(a, b)
        win = a if order[a] < order[b] else b
        split = {a, b} == {"batch/fox_02.png", "batch/fox_04.png"}
        for o in ("1", "2"):
            # order 1 shows a | b, order 2 shows b | a
            left = a if o == "1" else b
            pick = "1" if left == win else "2"
            if split and o == "2":
                pick = "2" if pick == "1" else "1"
            subprocess.run([BASH, "-c", "python aw.py compare record %s %s %s --work batch/artwright > /dev/null"
                            % (pid, o, pick)], cwd=WORK, env=ENV, check=True)
run("rank write", "python aw.py rank --work batch/artwright --write")
run("verdict validate draft", "python aw.py verdict validate batch")

FINISH = '''
import json
from pathlib import Path

path = Path("batch/artwright/verdict.json")
v = json.loads(path.read_text(encoding="utf-8"))
v["judge"]["model"] = "claude-opus-5-5"
v["fit"] = [{"id": "C", "verdict": "FITS", "hard_fails": [],
             "checks": [{"check": "one fox", "pass": True, "region": "centre"}]}]
v["fixes"] = [{"id": "A", "channel": "prompt", "fix": "the fox faces the camera; the brief asks for a side view",
               "prompt": {"model": "z-image-turbo", "text": "red fox in profile walking through snow at dusk",
                          "diff": "+ in profile"}}]
v["status"] = "final"
path.write_text(json.dumps(v, indent=1) + "\\n", encoding="utf-8")
'''
snippet("finish verdict", FINISH)
run("verdict validate final", "python aw.py verdict validate batch")

READ = '''
import json
from pathlib import Path

v = json.loads(Path("batch/artwright/verdict.json").read_text(encoding="utf-8"))
if v["status"] != "final":
    raise SystemExit("artwright has not finished")
best = v["ranking"][0]
print("best:", best["file"], "strength", best["strength"])
if best["close_to_next"]:
    print("not clearly ahead of", v["ranking"][1]["file"])
for t in v["abstained"]:
    print("ask a person:", " vs ".join(t["files"]), "-", t["reason"])
for f in v["fixes"]:
    print("next prompt for", f["prompt"]["model"] + ":", f["prompt"]["text"])
'''
snippet("caller reads verdict", READ)

BREAK = '''
import json
from pathlib import Path

path = Path("batch/artwright/verdict.json")
v = json.loads(path.read_text(encoding="utf-8"))
v["items"][0]["file"] = "/home/you/renders/fox_01.png"
v["fit"][0]["verdict"] = "DOES NOT FIT"
v["fixes"][0]["channel"] = "negative prompt"
v["score"] = 8
path.write_text(json.dumps(v, indent=1) + "\\n", encoding="utf-8")
'''
snippet("break verdict", BREAK)
run("verdict validate broken", "python aw.py verdict validate batch")
CHANGED = """mkdir -p changed && cp batch/fox_01.png changed/
python aw.py verdict init changed changed/fox_01.png --kind critique > /dev/null
python aw.py degrade changed/fox_01.png -o changed/fox_01.png --kind blur > /dev/null
python aw.py verdict validate changed"""
run("changed file", CHANGED)

# ------------------------------------------------------------------ cache and calibration

run("cache put", """python aw.py cache put batch/fox_03.png --model claude-opus-5-5 --verdict '{"winner": true}'""")
run("cache get hit", "python aw.py cache get batch/fox_03.png --model claude-opus-5-5")
run("cache get miss", "python aw.py cache get batch/fox_03.png --model another-model")
run("cache label", 'python aw.py cache label batch/fox_03.png batch/fox_01.png a --note "warmer light"')
run("cache label 2", "python aw.py cache label batch/fox_02.png batch/fox_04.png b")
run("cache put sampling", """python aw.py cache put batch/fox_01.png --model claude-opus-5-5 --temperature 0.7 --seed 42 --verdict '{"winner": false}'""")
run("cache get sampling", "python aw.py cache get batch/fox_01.png --model claude-opus-5-5 --temperature 0.7 --seed 42")
run("cache get no sampling", "python aw.py cache get batch/fox_01.png --model claude-opus-5-5")
# a row as 0.1.0 stored it (rubric version 1), then read back by 0.3.0's default and by --rubric-version 1
run("cache put rubric 1", """python aw.py cache put batch/fox_04.png --model claude-opus-5-5 --rubric-version 1 --verdict '{"winner": false}'""")
run("cache get rubric default", "python aw.py cache get batch/fox_04.png --model claude-opus-5-5")
run("cache get rubric 1", "python aw.py cache get batch/fox_04.png --model claude-opus-5-5 --rubric-version 1")
run("cache label shown first", "python aw.py cache label batch/fox_01.png batch/fox_02.png a --shown-first a")
run("cache stats", "python aw.py cache stats")
run("cache agreement", "python aw.py cache agreement batch/artwright")

# ------------------------------------------------------------------ Recipes

SUB = '''
import json
import subprocess
import sys


def aw(*args):
    r = subprocess.run([sys.executable, "aw.py", *args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, json.loads(r.stdout)


code, info = aw("info", "dusk.png", "missing.png")
print("exit", code)
for item in info["items"]:
    if item["ok"]:
        print(item["file"], item["size"], item["tokens"]["standard"]["tokens"], "tokens")
    else:
        print(item["file"], "error:", item["error"])
'''
snippet("recipe subprocess", SUB)

READ_ONCE = r"""
for f in renders/*.png; do
  python aw.py info "$f" | python -c "import json,sys; i=json.load(sys.stdin)['items'][0]; print(i['file'], i['tokens']['standard']['tokens'])"
done
"""
run("recipe tokens loop", READ_ONCE)
run("recipe fix then recheck", "python aw.py pixel sprite_ai.png --scale 4 --budget 16")
DEGRADE = """
for k in saturate crush crop; do python aw.py degrade dusk.png -o dusk_$k.png --kind $k --seed 7; done
"""
run("recipe degrade pairs", DEGRADE)

# ------------------------------------------------------------------ Errors and edge cases

run("err missing file", "python aw.py fit missing.png -o x.png")
run("err same file", "python aw.py compare prepare dusk.png dusk.png --work err")
run("err unknown pair", "python aw.py compare record 000000000000 1 1 --work err")
run("err bad pick", "python aw.py compare record %s 3 1" % P)
run("err rank empty", "python aw.py rank --work nothing-here")
run("err bad cell", "python aw.py fit dusk.png -o x.png --cell 3:4")
run("err bad palette", "python aw.py palette dusk.png --against Not_A_Palette")
run("err bad hex", "python aw.py palette dusk.png --against 12345,abcdef")
run("err crop outside", "python aw.py fit dusk.png -o x.png --crop 2100,0,100,100")
run("crop past edge", "python aw.py fit dusk.png -o corner.png --crop 1900,1100,300,300")
run("err usage","python aw.py fit dusk.png")
run("err bad choice", "python aw.py degrade dusk.png -o x.png --kind sharpen")
run("err hash missing", "python aw.py hash renders/render_01.png missing.png")
run("err pixel missing", "python aw.py pixel sprite.png missing.png --budget 16")
run("err validate none", "python aw.py verdict validate renders")
run("err label pick", "python aw.py cache label batch/fox_01.png batch/fox_02.png 1")
run("err sheet empty", "mkdir -p empty && python aw.py sheet empty -o x.png")
run("jpeg decode", "python aw.py info photo.jpg")
aw.save_png(aw.Img(64, 64, bytearray([128, 128, 128, 255] * 64 * 64)), WORK / "grey.png")
run("err box short", "python aw.py comp dusk.png --subject 0.5,0.5")
run("err box words", "python aw.py light dusk.png --box left,top,half,half")
run("err light flat", "python aw.py light grey.png")
run("err depth map missing", "python aw.py depth dusk.png --depth missing.png")
run("err measure missing", """mkdir -p lone && cp aw.py lone/
python lone/aw.py --version 2>&1 | tail -n 1; echo "exit ${PIPESTATUS[0]}\"""")
