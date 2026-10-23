"""Offline tests for aw.py. Standard library only; every fixture is drawn in code.

Run from the repository root: python tests/test_aw.py
The museum fixture test (pinned SHA-256, Cleveland CC0) runs only with AW_NET=1 and skips with a reason otherwise.
"""

import contextlib
import io
import json
import os
import random
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "artwright" / "scripts"))
import aw  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="aw-test-"))
os.environ["ARTWRIGHT_HOME"] = str(TMP / "home")


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = aw.main([str(a) for a in argv])
    return code, json.loads(buf.getvalue())


def noise(w, h, colours, seed=1, alpha=False):
    rnd = random.Random(seed)
    img = aw.Img(w, h)
    for y in range(h):
        for x in range(w):
            c = rnd.choice(colours)
            img.put(x, y, c + (255,) if len(c) == 3 else c)
    return img


def up(img, s):
    return aw.resize_nearest(img, img.w * s, img.h * s)


def gradient(w, h, horizontal=True, rising=True):
    img = aw.Img(w, h)
    for y in range(h):
        for x in range(w):
            t = (x / (w - 1)) if horizontal else (y / (h - 1))
            v = int(255 * (t if rising else 1 - t))
            img.put(x, y, (v, v, v))
    return img


def blocks(w, h, n, seed):
    rnd = random.Random(seed)
    vals = [[rnd.randrange(256) for _ in range(n)] for _ in range(n)]
    img = aw.Img(w, h)
    for y in range(h):
        for x in range(w):
            v = vals[y * n // h][x * n // w]
            img.put(x, y, (v, 255 - v, (v * 3) % 256))
    return img


def waves(w, h):
    import math
    img = aw.Img(w, h)
    for y in range(h):
        for x in range(w):
            v = int(128 + 100 * math.sin(x / 7.0) * math.cos(y / 9.0))
            img.put(x, y, (v, (v + 60) % 256, 255 - v))
    return img


def save(img, name):
    return aw.save_png(img, TMP / name)


PAL4 = [(20, 12, 28), (68, 36, 52), (210, 170, 153), (109, 194, 202)]


class PngIO(unittest.TestCase):
    def test_roundtrip_rgba(self):
        img = noise(13, 7, [(1, 2, 3, 255), (200, 100, 50, 128), (0, 0, 0, 0)])
        back = aw.read_png((Path(save(img, "rt.png"))).read_bytes())
        self.assertEqual((back.w, back.h, bytes(back.d)), (img.w, img.h, bytes(img.d)))

    def test_palette_png(self):
        import struct
        import zlib
        w, h = 4, 2
        idx = bytes([0, 1, 2, 1, 2, 2, 0, 0])
        raw = b"".join(b"\x00" + idx[y * w:(y + 1) * w] for y in range(h))

        def chunk(t, b):
            return struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xFFFFFFFF)
        data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0))
                + chunk(b"PLTE", bytes([255, 0, 0, 0, 255, 0, 0, 0, 255])) + chunk(b"tRNS", bytes([0]))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
        img = aw.read_png(data)
        self.assertEqual(img.px(0, 0), (255, 0, 0, 0))
        self.assertEqual(img.px(1, 0), (0, 255, 0, 255))
        self.assertEqual(img.px(2, 0), (0, 0, 255, 255))

    def test_stdlib_matches_pillow(self):
        Image, _ = aw._pillow()
        if Image is None:
            self.skipTest("Pillow not installed")
        p = save(blocks(40, 30, 5, 3), "pil.png")
        self.assertEqual(bytes(aw.load(p).d), bytes(aw.load(p, prefer="stdlib").d))


class Tokens(unittest.TestCase):
    def test_formula(self):
        self.assertEqual(aw.token_cost(1000, 1000)["standard"]["tokens"], 1296)
        self.assertEqual(aw.token_cost(1920, 1080)["high"]["tokens"], 2691)
        self.assertLessEqual(aw.token_cost(1920, 1080)["standard"]["tokens"], 1568)
        self.assertLessEqual(aw.token_cost(4000, 3000)["high"]["tokens"], 4784)


class Palette(unittest.TestCase):
    def test_exact_colours_and_shares(self):
        img = aw.Img(10, 10)
        for y in range(10):
            for x in range(10):
                img.put(x, y, (255, 0, 0) if x < 5 else ((0, 0, 255) if y < 5 else (0, 255, 0)))
        code, r = run("palette", save(img, "pal.png"), "-k", "3")
        self.assertEqual(code, 0)
        got = {c["hex"]: c["share"] for c in r["colours"]}
        self.assertEqual(got, {"#ff0000": 0.5, "#0000ff": 0.25, "#00ff00": 0.25})

    def test_against_builtin(self):
        img = noise(8, 8, [(0, 0, 0), (255, 0, 77)])
        code, r = run("palette", save(img, "pal2.png"), "--against", "pico-8")
        self.assertEqual(r["against"]["weighted_delta_e"], 0.0)

    def test_de2000_reference_pair(self):
        # Sharma, Wu and Dalal (2005) test data, pair 1: 2.0425
        self.assertAlmostEqual(aw.de2000((50, 2.6772, -79.7751), (50, 0, -82.7485)), 2.0425, places=3)


class Pixel(unittest.TestCase):
    def test_grid_scale_1_to_8(self):
        native = noise(12, 12, PAL4, seed=7)
        for s in range(1, 9):
            g = aw.detect_grid(up(native, s))
            self.assertEqual(g["scale"], s, "scale %d" % s)
            self.assertEqual(g["lattice_alignment"], 100.0)

    def test_offset_found(self):
        native = up(noise(10, 10, PAL4, seed=2), 4)
        shifted = aw.Img(native.w + 2, native.h + 1, None)
        aw.paste(shifted, native, 2, 1)
        g = aw.detect_grid(shifted)
        self.assertEqual((g["scale"], g["offset"]), (4, [2, 1]))

    def test_clean_sprite_passes(self):
        native = noise(16, 16, PAL4 + [(0, 0, 0, 0)], seed=3)
        code, r = run("pixel", save(up(native, 4), "clean.png"), "--budget", "8")
        it = r["items"][0]
        self.assertEqual(it["grid"]["scale"], 4)
        self.assertEqual(it["uniform_blocks"], 100.0)
        self.assertEqual(it["unique_colours"], 4)
        self.assertTrue(it["clean_pixel_art"], it["problems"])

    def test_fake_sprite_fails(self):
        native = up(noise(16, 16, PAL4, seed=3), 4)
        fake = Path(TMP / "fake.png")
        run("degrade", save(native, "fake_src.png"), "-o", fake, "--kind", "blur")
        code, r = run("pixel", fake, "--budget", "8")
        it = r["items"][0]
        self.assertFalse(it["clean_pixel_art"])
        self.assertGreater(it["transitional_pixels"], 0)

    def test_mixels_break_uniformity(self):
        native = up(noise(18, 18, PAL4, seed=4), 3)
        mixed = TMP / "mixed.png"
        run("degrade", save(native, "mix_src.png"), "-o", mixed, "--kind", "mixels", "--seed", "2")
        code, r = run("pixel", mixed, "--scale", "3")
        self.assertLess(r["items"][0]["uniform_blocks"], 100.0)

    def test_orphan_count(self):
        img = aw.Img(8, 8)
        for y in range(8):
            for x in range(8):
                img.put(x, y, (0, 0, 0))
        img.put(2, 2, (255, 0, 0))
        img.put(6, 5, (0, 255, 0))
        self.assertEqual(sorted(aw.orphans(img)), [[2, 2], [6, 5]])

    def test_palette_match(self):
        img = noise(8, 8, [(0, 0, 0), (255, 241, 232), (1, 2, 3)], seed=5)
        code, r = run("pixel", save(img, "pm.png"), "--palette", "pico-8", "--scale", "1")
        self.assertEqual(r["items"][0]["palette"]["off_palette_count"], 1)

    def test_tile_seam(self):
        code, r = run("pixel", save(gradient(16, 16), "tile.png"), "--tile", "--scale", "1")
        self.assertTrue(r["items"][0]["tile"]["seam_suspected"])


class Sheet(unittest.TestCase):
    def test_deterministic_size_and_map(self):
        files = [save(blocks(64, 48, 4, i), "s%d.png" % i) for i in range(5)]
        code, r = run("sheet", *files, "-o", TMP / "sheet.png", "--cell", "100")
        self.assertEqual(code, 0)
        self.assertEqual(r["size"], [6 + 3 * 106, 6 + 2 * 106])
        self.assertEqual(sorted(r["map"]), ["A", "B", "C", "D", "E"])
        self.assertEqual(r["map"]["C"]["file"], files[2])

    def test_cap(self):
        files = [save(blocks(32, 32, 2, i), "c%d.png" % i) for i in range(9)]
        code, r = run("sheet", *files, "-o", TMP / "big.png", "--cell", "900")
        self.assertLessEqual(max(r["size"]), aw.SHEET_MAX)

    def test_letters(self):
        self.assertEqual([aw.letters(i) for i in (0, 25, 26, 27)], ["A", "Z", "AA", "AB"])


class Hashes(unittest.TestCase):
    def test_copies_and_strangers(self):
        a = waves(120, 90)
        pa, pb = save(a, "h1.png"), str(TMP / "h1j.png")
        run("degrade", pa, "-o", pb, "--kind", "jpeg")
        near = aw.ham(aw.dhash(aw.load(pa)), aw.dhash(aw.load(pb)))
        self.assertLessEqual(near, 4)
        far = aw.ham(aw.dhash(gradient(64, 64, rising=True)), aw.dhash(gradient(64, 64, rising=False)))
        self.assertGreaterEqual(far, 20)

    def test_dedupe_groups(self):
        a = save(blocks(64, 64, 4, 1), "d1.png")
        b = save(blocks(64, 64, 4, 1), "d2.png")
        c = save(gradient(64, 64), "d3.png")
        code, r = run("dedupe", a, b, c)
        self.assertEqual(len(r["groups"]), 1)
        self.assertEqual(r["threshold"]["algo"], "dhash")


class CompareRank(unittest.TestCase):
    def setUp(self):
        self.work = TMP / ("work-%s" % self._testMethodName) / "artwright"
        self.files = [save(blocks(40, 40, 3, 20 + i), "%s-%d.png" % (self._testMethodName, i)) for i in range(3)]

    def match(self, fa, fb, pick1, pick2):
        code, r = run("compare", "prepare", fa, fb, "--work", self.work, "--cell", "64")
        pid = r["pair"]
        run("compare", "record", pid, "1", pick1, "--work", self.work)
        code, r = run("compare", "record", pid, "2", pick2, "--work", self.work)
        return r["resolved"]

    def test_known_tournament(self):
        A, B, C = self.files
        self.assertEqual(self.match(A, B, "1", "2")["winner"], "a")
        self.match(B, C, "1", "2")
        self.match(A, C, "1", "2")
        code, r = run("rank", "--work", self.work)
        self.assertEqual([x["file"] for x in r["ranking"]], [A, B, C])

    def test_flip_is_tie(self):
        A, B, _ = self.files
        res = self.match(A, B, "1", "1")
        self.assertEqual(res["status"], "tie")
        self.assertTrue(res["flipped"])
        code, r = run("rank", "--work", self.work, "--next", "2", "--write")
        self.assertEqual(len(r["abstained"]), 1)
        v = json.loads((self.work / "verdict.json").read_text(encoding="utf-8"))
        self.assertEqual(len(v["ranking"]), 2)

    def test_bt_strengths(self):
        p = aw.bradley_terry(["x", "y"], [("x", "y", 1.0)] * 3)
        self.assertGreater(p["x"], p["y"])

    def test_agreement(self):
        A, B, C = self.files
        self.match(A, B, "1", "2")
        self.match(A, C, "1", "1")
        run("cache", "label", A, B, "a")
        code, r = run("cache", "agreement", self.work)
        self.assertEqual(r["both_orders_agreement"], 0.5)
        self.assertEqual(r["accuracy_vs_labels"], 1.0)

    def test_tie_both_orders(self):
        _, B, C = self.files
        res = self.match(B, C, "tie", "tie")
        self.assertEqual(res["status"], "tie")
        self.assertFalse(res["flipped"])
        run("cache", "label", B, C, "tie")
        code, r = run("cache", "agreement", self.work)
        self.assertEqual(code, 0)
        self.assertEqual(r["accuracy_vs_labels"], 1.0)


class CacheVerdict(unittest.TestCase):
    def test_cache_roundtrip(self):
        f = save(blocks(20, 20, 2, 99), "cache.png")
        code, r = run("cache", "get", f, "--model", "m1")
        self.assertFalse(r["hit"])
        run("cache", "put", f, "--model", "m1", "--verdict", '{"winner": "A"}')
        code, r = run("cache", "get", f, "--model", "m1")
        self.assertTrue(r["hit"])
        code, r = run("cache", "get", f, "--model", "m2")
        self.assertFalse(r["hit"])

    def test_verdict_contract(self):
        asset = TMP / "asset"
        img = save(blocks(20, 20, 2, 5), "asset/renders/front.png")
        code, r = run("verdict", "init", asset, img, "--kind", "critique", "--brief", "a red fox")
        self.assertEqual(r["items"][0]["file"], "renders/front.png")
        code, r = run("verdict", "validate", asset)
        self.assertTrue(r["valid"], r)
        vp = asset / "artwright" / "verdict.json"
        v = json.loads(vp.read_text(encoding="utf-8"))
        v["fit"] = [{"id": "A", "verdict": "DOES NOT FIT"}]
        v["fixes"] = [{"id": "A", "channel": "magic"}]
        vp.write_text(json.dumps(v), encoding="utf-8")
        code, r = run("verdict", "validate", asset)
        self.assertEqual(code, 1)
        self.assertEqual(len(r["problems"]), 2)


class StatsInfoMisc(unittest.TestCase):
    def test_stats_grey_has_no_colour(self):
        code, r = run("stats", save(gradient(64, 48), "g.png"), "--notan", TMP / "notan")
        self.assertEqual(code, 0)
        self.assertEqual(r["colourfulness"]["M"], 0.0)
        self.assertEqual(r["colourfulness"]["level"], "not colourful")
        self.assertGreater(r["mirror_symmetry"]["top_bottom"], 0.99)
        self.assertTrue(Path(r["notan"]["three_value"]).is_file())

    def test_stats_colourful(self):
        code, r = run("stats", save(noise(64, 64, [(255, 0, 0), (0, 0, 255), (0, 255, 0)]), "c.png"))
        self.assertGreater(r["colourfulness"]["M"], 82)

    def test_info(self):
        code, r = run("info", save(noise(30, 20, [(1, 1, 1, 255), (2, 2, 2, 0)]), "i.png"))
        it = r["items"][0]
        self.assertEqual((it["size"], it["alpha"], it["format"]), ([30, 20], "binary", "png"))

    def test_fit_and_crop(self):
        p = save(blocks(300, 200, 5, 1), "fit.png")
        code, r = run("fit", p, "-o", TMP / "fit_o.png", "--long", "150")
        self.assertEqual(r["size"], [150, 100])
        code, r = run("fit", p, "-o", TMP / "cell.png", "--cell", "2x3:4", "--long", "1000")
        self.assertEqual(r["size"], [100, 100])
        code, r = run("fit", save(noise(16, 16, PAL4), "px.png"), "-o", TMP / "pxo.png", "--pixel", "--long", "64")
        self.assertEqual(r["size"], [64, 64])

    def test_degrade_kinds_deterministic(self):
        p = save(blocks(48, 48, 4, 8), "deg.png")
        for k in aw.DEGRADE_KINDS:
            o1, o2 = TMP / ("deg_%s_1.png" % k), TMP / ("deg_%s_2.png" % k)
            run("degrade", p, "-o", o1, "--kind", k, "--seed", "3")
            run("degrade", p, "-o", o2, "--kind", k, "--seed", "3")
            self.assertEqual(o1.read_bytes(), o2.read_bytes(), k)
            self.assertNotEqual(bytes(aw.load(o1).d), bytes(aw.load(p).d), k)

    def test_fail_soft(self):
        code, r = run("info", TMP / "missing.png")
        self.assertEqual(code, 1)
        code, r = run("palette", TMP / "missing.png")
        self.assertFalse(r["ok"])

    def test_label_font_complete(self):
        for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            self.assertEqual(len(aw.FONT[ch]), 14, ch)

    def test_stats_value_structure(self):
        code, two = run("stats", save(paint(64, 64, lambda x, y: (20, 20, 20) if x < 32 else (235, 235, 235)), "two.png"))
        code, ramp = run("stats", save(gradient(64, 64), "ramp.png"))
        self.assertGreater(two["value"]["bimodality"], 0.9)
        self.assertLess(ramp["value"]["bimodality"], 0.5)
        self.assertGreater(ramp["value"]["middle_share"], 0.25)
        code, r = run("stats", save(paint(64, 64, lambda x, y: (0, 0, 0) if x < 16 else (255, 255, 255)), "clip.png"))
        self.assertAlmostEqual(r["value"]["clip_black"], 0.25, 2)
        self.assertGreater(r["value"]["clip_white"], 0.7)


def paint(w, h, fn):
    img = aw.Img(w, h)
    for y in range(h):
        for x in range(w):
            img.put(x, y, fn(x, y))
    return img


def lit_scene(x, y):
    """Warm sunlit left half, cool shadow right half, with a little texture so the families have spread."""
    t = ((x * 7 + y * 13) % 11) - 5
    return aw.lab_rgb(75 + t, 8, 30) if x < 48 else aw.lab_rgb(32 + t, -2, -14)


def landscape(x, y, h=96):
    """Far third pale and soft, near third dark and contrasty: atmospheric perspective."""
    t = ((x * 5 + y * 3) % 9) - 4
    if y < h // 3:
        return aw.lab_rgb(70 + t * 0.6, -2, -6)
    if y < 2 * h // 3:
        return aw.lab_rgb(55 + t * 2, -10, 12)
    return aw.lab_rgb(40 + t * 4, -22, 26)


def degrade(img, name, kind, seed=1):
    src, dst = save(img, name + ".png"), TMP / ("%s_%s.png" % (name, kind))
    run("degrade", src, "-o", dst, "--kind", kind, "--seed", str(seed))
    return src, dst


class Measures(unittest.TestCase):
    def test_lab_roundtrip(self):
        for c in ((255, 0, 0), (12, 200, 90), (128, 128, 128), (250, 240, 10)):
            self.assertEqual(aw.lab_rgb(*aw.lab(c)), c)

    def test_light_warm_light_cool_shadow(self):
        src, warm = degrade(paint(96, 64, lit_scene), "lit", "warm-shadows")
        code, r = run("light", src)
        self.assertEqual(code, 0)
        self.assertGreater(r["temp_shift_b"], 30)
        self.assertGreater(r["value_gap_steps"], 3)
        self.assertEqual(r["flags"], [])
        code, r = run("light", warm)
        self.assertLess(abs(r["temp_shift_b"]), 2)
        self.assertIn("warm_shadows", r["flags"])
        code, r = run("light", degrade(paint(96, 64, lit_scene), "lit2", "glow-shadows")[1])
        self.assertGreater(r["chroma_ratio"], 1.15)
        self.assertIn("glowing_shadows", r["flags"])
        code, r = run("light", src, "--box", "0.3,0,0.4,1")
        self.assertEqual(r["proxy"], "box")
        self.assertGreater(r["temp_shift_b"], 30)
        self.assertFalse(run("light", src, "--box", "1,2,3")[1]["ok"])

    def test_gamut_shapes(self):
        code, r = run("gamut", save(paint(48, 48, lambda x, y: aw.lab_rgb(30 + x, 20, 40)), "mono.png"),
                      "--overlay", TMP / "hull.png")
        self.assertEqual(r["shape"], "mono")
        self.assertTrue(Path(r["overlay"]).is_file())
        code, r = run("gamut", save(paint(48, 48, lambda x, y: aw.lab_rgb(60, 30, 60) if x < 24
                                         else aw.lab_rgb(45, 10, -50)), "comp.png"))
        self.assertEqual(r["shape"], "complementary")
        code, r = run("gamut", save(noise(48, 48, [(255, 0, 0), (0, 200, 0), (0, 0, 255), (255, 220, 0), (255, 0, 255),
                                                   (0, 220, 220), (255, 128, 0), (128, 0, 255), (0, 128, 255),
                                                   (255, 100, 150)]), "salad.png"))
        self.assertEqual(r["shape"], "full")
        self.assertIn("fruit_salad", r["flags"])
        code, r = run("gamut", save(gradient(32, 32), "grey.png"))
        self.assertEqual(r["shape"], "neutral")

    def test_uniform_sat_flattens_chroma(self):
        src, flat = degrade(paint(64, 64, lambda x, y: aw.lab_rgb(55, x - 10, 20 + y // 2)), "sat", "uniform-sat")
        self.assertLess(run("stats", flat)[1]["chroma_cells"]["spread"],
                        run("stats", src)[1]["chroma_cells"]["spread"] / 3)

    def test_accents(self):
        def scene(ax, ay):
            def f(x, y):
                if abs(x - ax) < 3 and abs(y - ay) < 3:
                    return aw.lab_rgb(50, 70, 50)
                return aw.lab_rgb(50 + ((x // 8 + y // 8) % 2) * 30 * (abs(x - 20) < 9 and abs(y - 20) < 9), -30, 25)
            return f
        code, near = run("accents", save(paint(64, 64, scene(22, 22)), "acc_near.png"))
        code, far = run("accents", save(paint(64, 64, scene(58, 58)), "acc_far.png"))
        self.assertEqual(near["dominant_hue"], "green")
        self.assertEqual(near["accents"][0]["hue"], "red")
        self.assertNotIn("competing_accent", near["flags"])
        self.assertIn("competing_accent", far["flags"])
        code, r = run("accents", save(paint(32, 32, lambda x, y: aw.lab_rgb(40 + x, -30, 25)), "acc_none.png"))
        self.assertEqual(r["accents"], [])

    def test_depth_recession(self):
        src, flat = degrade(paint(96, 96, landscape), "land", "haze-off")
        code, r = run("depth", src)
        self.assertEqual(r["flags"], [])
        self.assertLess(r["far"]["contrast"], r["near"]["contrast"])
        code, r = run("depth", flat)
        self.assertIn("no_recession", r["flags"])
        dm = save(paint(96, 96, lambda x, y: (y * 2, y * 2, y * 2)), "depthmap.png")
        code, r = run("depth", src, "--depth", dm)
        self.assertEqual((r["proxy"].startswith("depth map"), r["flags"]), (True, []))
        code, r = run("depth", src, "--depth", dm, "--far-bright")
        self.assertIn("no_recession", r["flags"])

    def test_comp_masses(self):
        bands = paint(96, 96, lambda x, y: (30, 30, 30) if y < 32 else ((130, 130, 130) if y < 64 else (230, 230, 230)))
        src, grey = degrade(bands, "bands", "midgrey")
        code, r = run("comp", src, "--out", TMP / "masses")
        self.assertEqual(code, 0)
        self.assertEqual((r["masses"]["3"]["masses_over_1pct"], r["flags"].count("fragmented")), (3, 0))
        self.assertTrue(Path(r["masses"]["4"]["map"]).is_file())
        self.assertIn("horizon", r)
        code, r = run("comp", save(blocks(96, 96, 12, 4), "busy.png"))
        self.assertIn("fragmented", r["flags"])
        code, r = run("comp", grey)
        self.assertNotIn("mid_dominant", run("comp", src)[1]["flags"])
        flat = paint(96, 96, lambda x, y: (120 + (x + y) % 3, 120, 120) if 14 < y < 82 else ((40, 40, 40) if y < 50 else (220, 220, 220)))
        self.assertIn("mid_dominant", run("comp", save(flat, "mid.png"))[1]["flags"])

    def test_comp_focal(self):
        def discs(*cs):
            return lambda x, y: (240, 230, 200) if any((x - cx) ** 2 + (y - cy) ** 2 < 36 for cx, cy in cs) else (40, 50, 60)
        code, one = run("comp", save(paint(128, 96, discs((40, 40))), "disc1.png"))
        code, two = run("comp", save(paint(128, 96, discs((32, 24), (96, 72))), "disc2.png"))
        self.assertNotIn("competing_focal", one["flags"])
        self.assertIn("competing_focal", two["flags"])
        code, r = run("comp", save(paint(128, 96, discs((40, 40))), "disc1.png"), "--subject", "0.6,0.5,0.3,0.4")
        self.assertIn("focal_off_subject", r["flags"])
        self.assertIn("weak_figure_ground", r["flags"])
        code, r = run("comp", TMP / "disc1.png", "--subject", "0.2,0.3,0.2,0.3")
        self.assertNotIn("focal_off_subject", r["flags"])

    def test_comp_border(self):
        def calm(x, y):
            return (90 + y // 2, 100 + y // 3, 120) if (x - 64) ** 2 + (y - 48) ** 2 > 200 else (230, 200, 150)
        src, tan = degrade(paint(128, 96, calm), "calm", "tangent", 2)
        _, hot = degrade(paint(128, 96, calm), "calm2", "hotspot", 3)
        code, r = run("comp", src)
        for f in ("frame_tangent", "hot_spot_near_border", "edge_pull", "blocked_entrance"):
            self.assertNotIn(f, r["flags"])
        self.assertIn("frame_tangent", run("comp", tan)[1]["flags"])
        self.assertIn("hot_spot_near_border", run("comp", hot)[1]["flags"])
        striped = paint(128, 96, lambda x, y: ((255, 255, 255) if (y // 2) % 2 else (0, 0, 0)) if x < 8 else calm(x, y))
        self.assertIn("edge_pull", run("comp", save(striped, "pull.png"))[1]["flags"])
        barred = paint(128, 96, lambda x, y: (10, 10, 10) if y > 86 else calm(x, y))
        self.assertIn("blocked_entrance", run("comp", save(barred, "bar.png"))[1]["flags"])

    def test_comp_horizon_and_sharpness(self):
        def sea(at):
            return lambda x, y: (150, 180, 220) if y < at else (30 + (x * 7 + y * 3) % 40, 60, 90)
        code, r = run("comp", save(paint(128, 96, sea(48)), "sea_mid.png"))
        self.assertEqual(r["horizon"]["band"], "middle")
        self.assertIn("horizon_split", r["flags"])
        code, r = run("comp", save(paint(128, 96, sea(68)), "sea_low.png"))
        self.assertEqual((r["horizon"]["band"], "horizon_split" in r["flags"]), ("lower third", False))
        self.assertIn("uniform_sharpness", run("comp", save(noise(96, 96, PAL4), "sharp.png"))[1]["flags"])
        self.assertNotIn("uniform_sharpness", run("comp", TMP / "disc1.png")[1]["flags"])

    def test_comp_trims_a_mat(self):
        def matted(x, y):
            return (235, 232, 225) if min(x, y, 127 - x, 95 - y) < 8 else (x * 2, y * 2, 90)
        code, r = run("comp", save(paint(128, 96, matted), "mat.png"))
        self.assertIsNotNone(r["margin_trimmed"])
        self.assertNotIn("frame_tangent", r["flags"])
        code, r = run("comp", save(paint(128, 96, lambda x, y: (5, 5, 5) if min(x, y, 127 - x, 95 - y) < 8
                                         else (x * 2, y * 2, 90)), "black_mat.png"))
        self.assertIsNone(r["margin_trimmed"])


# Museum fixtures (ruling R5): fetched by accession number, checked against a pinned hash, cached git-ignored.
FIXTURES = {
    "2026.37": "6068ee295ad619357929200f1a586a45089d1f3c2097d190d09222fb08ebaa01",
    "2006.139": "54b03bc03c745fcc3edd523b315dd9fda942c30c633988170c1cbeb24b780c5c",
    "1958.21": "b8508d3dafd5c7e5abbf7acd8223654326918d5b6941f560d575d9c762d0fda0",
    "1967.215": "79f82c7e28afc064bd19199dd6883d90d3bb42af26cd61517b6cd28e27dbe58e",
    "1971.38": "af8d1984c6c5526f12d055f58abb3754b6a445886d47e2e6da45008a5122270b",
    "1930.189": "b0f546cc1972fb8e7ef84d21eb7d30805de189297a22a248b1ecaf11c5b5468d",
    "1940.1002": "cf8c01bdc069c8d8dd79028fc55e74c58032eb09e7982fd95d38b7d3fd8ddbe9",
}


def museum_fixture(acc):
    cache = ROOT / "tests" / ".fixtures-cache" / ("cma-%s.jpg" % acc)
    if not cache.is_file():
        url = "https://openaccess-cdn.clevelandart.org/%s/%s_web.jpg" % (acc, acc)
        req = urllib.request.Request(url, headers={"User-Agent": aw.UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        cache.parent.mkdir(exist_ok=True)
        cache.write_bytes(data)
    if aw.sha256(cache) != FIXTURES[acc]:
        raise AssertionError("fixture %s changed upstream (sha256 differs); re-pin after checking it" % acc)
    return cache


class Museum(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("AW_NET") == "1", "network fixtures: set AW_NET=1")
    def test_pinned_fixtures(self):
        for acc in FIXTURES:
            p = museum_fixture(acc)
            if aw._pillow()[0] or aw.shutil.which("ffmpeg"):
                img = aw.load(p)
                self.assertGreater(img.w, 500)


if __name__ == "__main__":
    unittest.main(verbosity=1)
