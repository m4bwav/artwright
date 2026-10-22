"""Writes the eval fixtures (images are never committed): python evals/fixtures/make_fixtures.py [--net]

Out: evals/fixtures/out/ (git-ignored). Synthetic images are drawn with aw.py's own writer; --net also fetches the
Cleveland CC0 museum fixtures by accession number, checked against the hashes pinned in tests/test_aw.py.
"""

import random
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills" / "artwright" / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import aw  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
PAL = [(20, 12, 28), (68, 36, 52), (133, 76, 48), (210, 125, 44), (218, 212, 94), (222, 238, 214)]


def sprite(seed):
    """A 16x16 creature: symmetric body, two-tone shading, outline, transparent background."""
    rnd = random.Random(seed)
    img = aw.Img(16, 16)
    for y in range(2, 14):
        half = [rnd.random() < 0.55 + 0.3 * (4 < y < 11) for _ in range(6)]
        for x in range(6):
            if half[x]:
                c = PAL[3] if y < 8 else PAL[2]
                img.put(2 + x, y, c)
                img.put(13 - x, y, c)
    for y in range(16):
        for x in range(16):
            if img.px(x, y)[3] == 0 and any(0 <= x + dx < 16 and 0 <= y + dy < 16 and img.px(x + dx, y + dy)[3]
                                            and img.px(x + dx, y + dy)[:3] != PAL[0]
                                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                img.put(x, y, PAL[0])
    img.put(6, 6, PAL[5])
    img.put(9, 6, PAL[5])
    return img


def emit_scaffold():
    """Writes fixture.sh into each action case: the synthetic PNGs as base64, unpacked into the run's workspace."""
    import base64
    lines = ["#!/usr/bin/env bash",
             "# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py",
             "# --emit-scaffold; synthetic images drawn in code, never committed as files.",
             "set -euo pipefail",
             "mkdir -p evals/fixtures/out/renders"]
    for p in sorted(OUT.rglob("*.png")):
        rel = p.relative_to(OUT).as_posix()
        b64 = base64.b64encode(p.read_bytes()).decode()
        lines.append("base64 -d > evals/fixtures/out/%s <<'B64'" % rel)
        lines += [b64[i:i + 76] for i in range(0, len(b64), 76)]
        lines.append("B64")
    body = "\n".join(lines) + "\n"
    for case in sorted((ROOT / "evals" / "cases").glob("action-*")):
        with open(case / "fixture.sh", "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        (case / "case.yaml").write_bytes(('schema_version: "1.1"\nname: %s\ncontext:\n  scaffold_script: fixture.sh\n'
                                          % case.name).encode())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    flag = aw.Img(90, 60)
    for y in range(60):
        for x in range(90):
            flag.put(x, y, (200, 30, 40) if x < 45 else ((240, 240, 240) if y < 30 else (30, 60, 160)))
    aw.save_png(flag, OUT / "flag.png")
    clean = aw.resize_nearest(sprite(4), 64, 64)
    aw.save_png(clean, OUT / "sprite_clean.png")
    fake = aw.resize_box(aw.resize_nearest(sprite(4), 97, 97), 64, 64)  # off-grid resample: blends and mixels
    aw.save_png(fake, OUT / "sprite_fake.png")
    rd = OUT / "renders"
    rd.mkdir(exist_ok=True)
    for i in range(6):
        aw.save_png(aw.resize_nearest(sprite(10 + i), 128, 128), rd / ("render_%02d.png" % (i + 1)))
    if "--emit-scaffold" in sys.argv:
        emit_scaffold()
    if "--net" in sys.argv:
        import test_aw
        for acc in test_aw.FIXTURES:
            shutil.copy(test_aw.museum_fixture(acc), OUT / ("cma-%s.jpg" % acc))
    print("fixtures in", OUT)


if __name__ == "__main__":
    main()
