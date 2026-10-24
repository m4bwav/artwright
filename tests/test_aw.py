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

    def test_cycle_is_close(self):
        # r1 beats everyone but r3, which r2 beats: 1.65x the runner-up and met directly, yet inside a cycle
        fs = self.files + [save(blocks(40, 40, 3, 40 + i), "cyc-%d.png" % i) for i in range(3)]
        r1, r2, r3, r4, r5, r6 = fs
        for w, l in ((r1, r2), (r2, r3), (r3, r1), (r1, r4), (r1, r5), (r1, r6)):
            self.match(w, l, "1", "2")
        code, r = run("rank", "--work", self.work)
        self.assertEqual(r["cycle_count"], 1)
        self.assertTrue(r["top_in_cycle"])
        self.assertEqual(sorted(r["cycles"][0]["files"]), sorted([r1, r2, r3]))
        self.assertEqual(r["ranking"][0]["file"], r1)
        self.assertTrue(r["ranking"][0]["close_to_next"])

    def test_no_cycle_in_order(self):
        A, B, C = self.files
        self.match(A, B, "1", "2")
        self.match(B, C, "1", "2")
        self.match(A, C, "1", "2")
        code, r = run("rank", "--work", self.work)
        self.assertEqual(r["cycle_count"], 0)
        self.assertFalse(r["top_in_cycle"])

    def test_label_order_share(self):
        A, B, C = self.files
        self.match(A, B, "1", "2")
        run("cache", "label", A, B, "a", "--shown-first", "a")
        run("cache", "label", A, C, "a", "--shown-first", "b")
        run("cache", "label", B, C, "tie", "--shown-first", "a")
        code, r = run("cache", "agreement", self.work)
        self.assertGreaterEqual(r["labels_with_order"], 2)
        self.assertIsNotNone(r["labels_first_shown_share"])

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

    def test_cache_sampling_key(self):
        f = save(blocks(20, 20, 2, 98), "cache-t.png")
        run("cache", "put", f, "--model", "m1", "--temperature", "0", "--verdict", '{"winner": "A"}')
        code, r = run("cache", "get", f, "--model", "m1", "--temperature", "1")
        self.assertFalse(r["hit"])
        code, r = run("cache", "get", f, "--model", "m1", "--temperature", "0")
        self.assertTrue(r["hit"])
        code, r = run("cache", "get", f, "--model", "m1", "--temperature", "0", "--seed", "7")
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


# ---------------------------------------------------------------- render-then-paint and painted sprites

ID_COLOURS = {"wheel": [1, 0, 0], "roof": [0, 0, 1], "building": [0.5, 0.5, 0.5], "water": [1, 0, 1]}
WHEEL = (60.0, 108.0, 42.0, 38.0)  # centre x, y, semi-axes x, y of the outer rim (render px)


def srgb8(v):
    return round((v * 12.92 if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055) * 255)


def mill_scene(squash=1.0, blob=False, noise=0, seed=1, rim=0.94):
    """A 192 px render: a building with a roof, water, and an eight-armed wheel; returns beauty and ID images.
    squash shrinks the wheel's vertical axis (a painting that lost the shape); blob paints a disc on the roof."""
    import math
    rnd = random.Random(seed)
    cx, cy, ax, ay = WHEEL
    ay *= squash
    beauty, ids = aw.Img(192, 192), aw.Img(192, 192)
    idc = {k: tuple(srgb8(v) for v in c) for k, c in ID_COLOURS.items()}
    for y in range(192):
        for x in range(192):
            col, reg = None, None
            if 85 <= x < 186 and 20 <= y < 50:
                col, reg = (170 - (y - 20) * 2, 70, 50), "roof"
            elif 90 <= x < 180 and 50 <= y < 170:
                col, reg = (150 + (x - 90) // 3, 140 + (x - 90) // 4, 120), "building"
            elif x < 130 and y >= 148:
                col, reg = (60, 90 + (y - 148), 150), "water"
            u, v = (x - cx) / ax, (y - cy) / ay
            r = math.hypot(u, v)
            if r <= 1.0:
                th = math.degrees(math.atan2(v, u)) % 45
                if r >= rim or r < 0.15 or min(th, 45 - th) < 4.5:
                    col, reg = (90, 60, 40) if r >= rim else (115, 80, 55), "wheel"
            if blob and (x - 135) ** 2 + (y - 35) ** 2 <= 49:
                col = (25, 25, 30)
            if col:
                if noise:
                    col = tuple(max(0, min(255, c + rnd.randint(-noise, noise))) for c in col)
                beauty.put(x, y, col + (255,))
            if reg:
                ids.put(x, y, idc[reg] + (255,))
    return beauty, ids


def mill_render(name="mill"):
    import math
    d = TMP / name
    d.mkdir(exist_ok=True)
    beauty, ids = mill_scene()
    aw.save_png(beauty, d / "beauty.png")
    aw.save_png(ids, d / "id.png")
    cx, cy, ax, ay = WHEEL
    rim = [[round(cx + ax * math.cos(2 * math.pi * k / 72), 2), round(cy + ay * math.sin(2 * math.pi * k / 72), 2)]
           for k in range(72)]
    (d / "sprite.json").write_text(json.dumps({"id_colours": ID_COLOURS, "render_px": [192, 192],
                                               "rings": {"wheel": {"rim_px": rim, "centre_px": [cx, cy], "arms": 8}},
                                               "contacts": [["wheel", "water"]]}))
    return d


class GeomGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render = mill_render()

    def gate(self, img, name, *extra):
        code, r = run("geomgate", self.render, save(img, name), "--no-edges", *extra)
        self.assertEqual(code, 0, r)
        return r

    def test_render_passes_itself(self):
        r = self.gate(aw.load(self.render / "beauty.png"), "self.png")
        self.assertTrue(r["pass"], r["failing_gates"])
        self.assertLess(r["gates"]["ellipse"]["rim_rms"], 0.005)
        self.assertEqual(r["part"], "wheel")
        self.assertEqual(r["gates"]["contact"]["pairs"], {"wheel:water": True})

    def test_textured_paint_passes(self):
        r = self.gate(mill_scene(noise=12, seed=3)[0], "brushy.png")
        self.assertTrue(r["pass"], r)

    def test_squashed_wheel_fails(self):
        r = self.gate(mill_scene(squash=0.8, noise=6)[0], "squashed.png")
        self.assertFalse(r["gates"]["ellipse"]["pass"], r["gates"]["ellipse"])
        self.assertFalse(r["gates"]["spokes"]["pass"], r["gates"]["spokes"])

    def test_new_object_fails_its_region(self):
        r = self.gate(mill_scene(blob=True, noise=6)[0], "blob.png")
        self.assertFalse(r["pass"])
        self.assertEqual(r["gates"]["regions"]["failing"], ["roof"])
        self.assertTrue(r["gates"]["ellipse"]["pass"])

    def test_contact_option_and_errors(self):
        r = self.gate(aw.load(self.render / "beauty.png"), "self2.png", "--contact", "roof:water")
        self.assertEqual(r["gates"]["contact"]["pairs"], {"roof:water": False})
        self.assertFalse(r["pass"])
        code, r = run("geomgate", self.render, self.render / "beauty.png", "--part", "gear")
        self.assertEqual(code, 1)
        self.assertIn("no ring", r["error"])
        code, r = run("geomgate", TMP, self.render / "beauty.png")
        self.assertEqual(code, 1)

    def test_edges_are_information(self):
        code, r = run("geomgate", self.render, save(mill_scene(noise=12, seed=4)[0], "edges.png"))
        self.assertIn("scores", r["edges_info"])
        self.assertNotIn("edges", r["gates"])

    def test_ellipse_fit(self):
        import math
        import aw_geom
        xs = [50 + 30 * math.cos(t / 10) * math.cos(0.3) - 12 * math.sin(t / 10) * math.sin(0.3) for t in range(63)]
        ys = [40 + 30 * math.cos(t / 10) * math.sin(0.3) + 12 * math.sin(t / 10) * math.cos(0.3) for t in range(63)]
        c, axes, tilt = aw_geom.fit_ellipse(xs, ys)
        self.assertAlmostEqual(c[0], 50, 4)
        self.assertAlmostEqual(c[1], 40, 4)
        self.assertAlmostEqual(axes[0], 30, 4)
        self.assertAlmostEqual(axes[1], 12, 4)
        self.assertAlmostEqual(tilt, math.degrees(0.3), 3)


def house_sprite(seed, flat=False, size=48):
    """A painted-looking building on a transparent canvas: value ramp, brush noise, a darker rim, soft edge pixels."""
    rnd = random.Random(seed)
    img = aw.Img(size, size)
    base = 120 + seed * 4
    for y in range(size):
        for x in range(size):
            wall = 8 <= x < 40 and 20 <= y < 44
            roof = 4 <= x < 44 and 8 <= y < 20 and abs(x - 24) <= (y - 4) * 1.4
            if not (wall or roof):
                continue
            edge = (x in (8, 39) and wall) or y == 43
            t = 0 if flat else rnd.randint(-14, 14)
            v = (base - (y - 8) * 2 + t) if wall else (150 + t)
            c = (v, int(v * 0.8), int(v * 0.6)) if wall else (v, 60 + t // 2, 45)
            if edge:
                c = tuple(int(k * 0.45) for k in c)
            c = tuple(max(0, min(255, k)) for k in c)
            img.put(x, y, c + (140 if edge and not flat and rnd.random() < 0.3 else 255,))
    return img


class Sprite(unittest.TestCase):
    def test_style_fit(self):
        refs = TMP / "sprite_refs"
        refs.mkdir(exist_ok=True)
        for s in range(1, 6):
            aw.save_png(house_sprite(s), refs / ("ref%d.png" % s))
        good = save(house_sprite(3), "cand_good.png")
        flat = save(house_sprite(3, flat=True), "cand_flat.png")
        code, r = run("sprite", good, flat, "--refs", refs)
        self.assertEqual(code, 0, r)
        self.assertEqual(r["references"], 5)
        g, f = r["candidates"]
        self.assertTrue(g["pass"], g)
        self.assertFalse(f["pass"])
        self.assertIn("texture", f["outside"])
        self.assertIn("colours", f["outside"])
        self.assertEqual(g["size"], [48, 48])
        self.assertLess(g["measures"]["coverage"], 0.8)

    def test_candidate_is_never_its_own_reference(self):
        d = TMP / "sprite_two"
        d.mkdir(exist_ok=True)
        a = aw.save_png(house_sprite(1), d / "a.png")
        aw.save_png(house_sprite(2), d / "b.png")
        code, r = run("sprite", a, "--refs", d)
        self.assertEqual(code, 1)
        self.assertIn("two reference", r["error"])


class Alpha(unittest.TestCase):
    def test_stats_skips_transparent_pixels(self):
        img = paint(64, 64, lambda x, y: (128, 128, 128, 255) if 16 <= x < 48 and 16 <= y < 48 else (0, 0, 0, 0))
        code, r = run("stats", save(img, "grey_sprite.png"))
        self.assertEqual(code, 0, r)
        self.assertEqual(r["value"]["clip_white"], 0)
        self.assertAlmostEqual(r["alpha"]["transparent_share"], 0.75, 3)
        self.assertTrue(r["alpha"]["excluded"])
        self.assertAlmostEqual(r["value"]["mean"], 0.502, 2)
        self.assertEqual(r["rms_contrast"], 0)
        code, o = run("stats", save(gradient(32, 32), "opaque.png"))
        self.assertEqual(o["alpha"], {"transparent_share": 0.0, "excluded": False})

    def test_measures_skip_transparent_pixels(self):
        img = paint(64, 64, lambda x, y: (200, 40, 40, 255) if x < 32 else (0, 0, 0, 0))
        code, g = run("gamut", save(img, "red_half.png"))
        self.assertEqual(code, 0, g)
        self.assertEqual(g["chromatic_share"], 1.0)
        self.assertTrue(g["alpha"]["excluded"])


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
