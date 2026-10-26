"""aw.py: artwright's image tools. Numbers first, pixels second.

Standard library Python 3.9+, Pillow optional (any version from 11), ffmpeg optional for JPEG and WebP when Pillow is
absent. Every command prints exactly one JSON object and fails soft (`ok: false` with `error`). No beauty score is
ever computed: the numbers describe an image, the judge reads them.

Commands (details: ../references/cli.md):
  doctor [--probe]                 what works here; --probe makes one request to each named route
  info IMG...                      size, alpha use, SHA-256, unique colours, token cost per tier
  fit IMG -o OUT [--long N | --tokens N] [--crop x,y,w,h | --cell RxC:i] [--pixel]
  sheet IMG|DIR... -o OUT [--cols N] [--cell PX]       contact sheet labelled A, B, C; map in the JSON
  stats IMG [--notan DIR]          value, contrast, colourfulness, edges, symmetry, balance, fractal dimension
  light IMG [--box x,y,w,h]        light and shadow families: value gap, temperature shift, chroma ratio
  gamut IMG [--overlay OUT]        hue sectors, gamut shape and area, colour cast
  accents IMG | depth IMG [--depth MAP [--far-bright]]  off-hue accents and where they sit; atmospheric recession
  comp IMG [--subject x,y,w,h] [--out DIR]  value masses, focal margin, border pull, tangents, horizon, hot spots
  palette IMG [-k N] [--against PAL]                    median-cut colours; delta-E 2000 to a palette
  pixel IMG... [--budget N] [--palette PAL] [--scale S] [--tile] [--frames] [--preview OUT]
  hash IMG... | dedupe IMG|DIR... [--threshold N]       64-bit aHash and dHash, Hamming groups
  compare prepare A B [--work DIR] | compare record PAIR ORDER PICK [--work DIR] [--confidence C] [--criteria ...]
  rank [--work DIR] [--next N] [--write]                Bradley-Terry with ties; Swiss pairs for the next round
  cache get|put|stats|label|agreement ...               verdict store and calibration under ARTWRIGHT_HOME
  verdict init|validate DIR ...                         the artwright/verdict.json contract
  degrade IMG -o OUT --kind K [--seed N]                deterministic degradations for test pairs
  geomgate RENDER_DIR PAINTED [--part P] [--contact A:B] [--out F]  a painting kept its 3D render's shapes
  sprite CAND... --refs DIR|IMG... [--pad 0.15]        a painted sprite's style against reference sprites
"""

import argparse
import colorsys
import datetime
import hashlib
import itertools
import json
import math
import os
import random
import re
import shutil
import struct
import subprocess
import sys
import urllib.request
import zlib
from pathlib import Path

VERSION = "0.6.0"
UA = "artwright/%s (+https://github.com/m4bwav/artwright)" % VERSION
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
TIERS = {"standard": (1568, 1568), "high": (2576, 4784)}  # long edge px, max visual tokens (R-20261021-11)
SHEET_MAX = 2000  # px a side; above 20 images per request a stricter per-image limit applies
VERDICTS = ("FITS", "FITS WITH FIXES", "DOES NOT FIT")
CHANNELS = ("prompt", "setting", "control", "reference", "inpaint", "model")
KINDS = ("pairwise", "brief-fit", "critique", "pixel")
# Hasler and Suesstrunk (2003) Table 2, M(3) anchor points on 0-255 sRGB; a value takes the nearest anchor's name.
HS_LEVELS = [(0, "not colourful"), (15, "slightly colourful"), (33, "moderately colourful"),
             (45, "averagely colourful"), (59, "quite colourful"), (82, "highly colourful"),
             (109, "extremely colourful")]
# Built in: only palettes with a stated open licence (PICO-8 is CC0 per Lexaloffle's FAQ). Any other Lospec slug is
# fetched once on the user's request and cached in ARTWRIGHT_HOME/palettes (Lospec's API page invites per-slug fetches).
PALETTES = {
    "pico-8": "000000 1d2b53 7e2553 008751 ab5236 5f574f c2c3c7 fff1e8 ff004d ffa300 ffec27 00e436 29adff 83769c"
              " ff77a8 ffccaa",
}


class Fail(Exception):
    pass


def out(obj, code=0):
    obj.setdefault("ok", code == 0)
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
    return code


def now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def home():
    return Path(os.environ.get("ARTWRIGHT_HOME") or Path.home() / ".artwright")


# ---------------------------------------------------------------- images

class Img:
    """RGBA, 8 bits per channel, rows top to bottom."""

    __slots__ = ("w", "h", "d")

    def __init__(self, w, h, d=None):
        self.w, self.h = w, h
        self.d = d if d is not None else bytearray(w * h * 4)

    def px(self, x, y):
        i = (y * self.w + x) * 4
        return tuple(self.d[i:i + 4])

    def put(self, x, y, c):
        i = (y * self.w + x) * 4
        self.d[i:i + 4] = bytes(c if len(c) == 4 else (c[0], c[1], c[2], 255))

    def pixels(self):
        d = self.d
        return list(zip(d[0::4], d[1::4], d[2::4], d[3::4]))

    def copy(self):
        return Img(self.w, self.h, bytearray(self.d))


def _pillow():
    try:
        import PIL
        from PIL import Image
        return Image, PIL.__version__
    except Exception:
        return None, None


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def read_png(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise Fail("not a PNG")
    pos, idat, plte, trns = 8, [], None, None
    w = h = bd = ct = il = None
    while pos < len(data):
        n, typ = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if typ == b"IHDR":
            w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", body)
        elif typ == b"PLTE":
            plte = body
        elif typ == b"tRNS":
            trns = body
        elif typ == b"IDAT":
            idat.append(body)
        elif typ == b"IEND":
            break
    if il:
        raise Fail("interlaced PNG: install Pillow or ffmpeg to read it")
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if ch is None:
        raise Fail("PNG colour type %s unsupported" % ct)
    raw = zlib.decompress(b"".join(idat))
    bits = ch * bd
    stride = (w * bits + 7) // 8
    bpp = max(1, bits // 8)
    rows, prev, p = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif f == 2:
            line = bytearray((a + b) & 255 for a, b in zip(line, prev))
        elif f == 3:
            for i in range(stride):
                line[i] = (line[i] + ((line[i - bpp] if i >= bpp else 0) + prev[i]) // 2) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                c = prev[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + _paeth(a, prev[i], c)) & 255
        rows.append(bytes(line))
        prev = line
    if bd == 16:
        rows = [r[0::2] for r in rows]
    elif bd < 8:
        mask, per = (1 << bd) - 1, 8 // bd
        unpacked = []
        for r in rows:
            vals = bytearray()
            for byte in r:
                for k in range(per):
                    vals.append((byte >> (8 - bd * (k + 1))) & mask)
            unpacked.append(bytes(vals[:w]))
        rows = unpacked
        if ct == 0:
            rows = [bytes(v * 255 // mask for v in r) for r in rows]
    flat = b"".join(rows)
    img = Img(w, h)
    d = img.d
    if ct == 6:
        d[:] = flat
    elif ct == 2:
        d[0::4], d[1::4], d[2::4], d[3::4] = flat[0::3], flat[1::3], flat[2::3], b"\xff" * (w * h)
        if trns and len(trns) >= 6:
            key = bytes(trns[1::2][:3])
            for i in range(w * h):
                if flat[i * 3:i * 3 + 3] == key:
                    d[i * 4 + 3] = 0
    elif ct == 0:
        d[0::4] = d[1::4] = d[2::4] = flat
        d[3::4] = b"\xff" * (w * h)
        if trns and len(trns) >= 2:
            key = trns[1]
            for i in range(w * h):
                if flat[i] == key:
                    d[i * 4 + 3] = 0
    elif ct == 4:
        d[0::4] = d[1::4] = d[2::4] = flat[0::2]
        d[3::4] = flat[1::2]
    else:
        if plte is None:
            raise Fail("palette PNG without PLTE")
        tabs = []
        for k in range(3):
            t = bytearray(256)
            t[:len(plte) // 3] = plte[k::3]
            tabs.append(bytes(t))
        at = bytearray(b"\xff" * 256)
        if trns:
            at[:len(trns)] = trns
        d[0::4], d[1::4], d[2::4] = flat.translate(tabs[0]), flat.translate(tabs[1]), flat.translate(tabs[2])
        d[3::4] = flat.translate(bytes(at))
    return img


def _ffmpeg_read(path):
    ff = shutil.which("ffmpeg")
    if not ff:
        raise Fail("cannot decode %s: install Pillow (pip install pillow) or ffmpeg" % Path(path).suffix)
    probe = subprocess.run([ff, "-hide_banner", "-i", str(path)], capture_output=True)
    m = re.search(rb"Video: .*?(\d{1,5})x(\d{1,5})", probe.stderr)
    if not m:
        raise Fail("ffmpeg could not read %s" % path)
    w, h = int(m.group(1)), int(m.group(2))
    r = subprocess.run([ff, "-v", "error", "-i", str(path), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                       capture_output=True)
    if r.returncode or len(r.stdout) < w * h * 4:
        raise Fail("ffmpeg decode failed: %s" % r.stderr.decode("utf-8", "replace")[:200])
    return Img(w, h, bytearray(r.stdout[:w * h * 4]))


def load(path, prefer=None):
    p = Path(path)
    if not p.is_file():
        raise Fail("no such file: %s" % path)
    Image, _ = _pillow() if prefer != "stdlib" else (None, None)
    if Image is not None:
        with Image.open(p) as im:
            im.seek(0)
            rgba = im.convert("RGBA")
            return Img(rgba.width, rgba.height, bytearray(rgba.tobytes()))
    data = p.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        try:
            return read_png(data)
        except Fail:
            if shutil.which("ffmpeg"):
                return _ffmpeg_read(p)
            raise
    return _ffmpeg_read(p)


def save_png(img, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stride = img.w * 4
    raw = b"".join(b"\x00" + bytes(img.d[y * stride:(y + 1) * stride]) for y in range(img.h))

    def chunk(t, b):
        return struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xFFFFFFFF)
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", img.w, img.h, 8, 6, 0, 0, 0))
                  + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))
    return str(p)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fmt_of(path):
    head = Path(path).read_bytes()[:12]
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if head[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    if head[:4] in (b"GIF8",):
        return "gif"
    return Path(path).suffix.lstrip(".").lower() or "unknown"


# ---------------------------------------------------------------- resampling

def resize_nearest(img, w, h):
    w, h = max(1, w), max(1, h)
    xs = [min(img.w - 1, int((x + 0.5) * img.w / w)) * 4 for x in range(w)]
    o = Img(w, h)
    sw = img.w * 4
    rows = []
    for y in range(h):
        sy = min(img.h - 1, int((y + 0.5) * img.h / h))
        row = img.d[sy * sw:(sy + 1) * sw]
        rows.append(b"".join(row[x:x + 4] for x in xs))
    o.d = bytearray(b"".join(rows))
    return o


def resize_box(img, w, h):
    """Area-average downscale (premultiplied by alpha). Upscaling falls back to nearest."""
    w, h = max(1, w), max(1, h)
    if w >= img.w and h >= img.h:
        return resize_nearest(img, w, h)
    if img.w > 4 * w and img.h > 4 * h:
        img = resize_nearest(img, 2 * w, 2 * h)
    sw, sh, d = img.w, img.h, img.d
    xr = [(int(x * sw / w), max(int(x * sw / w) + 1, int((x + 1) * sw / w))) for x in range(w)]
    yr = [(int(y * sh / h), max(int(y * sh / h) + 1, int((y + 1) * sh / h))) for y in range(h)]
    # horizontal pass into per-row sums
    tmp = []
    for y in range(sh):
        base = y * sw * 4
        r_, g_, b_, a_ = d[base:base + sw * 4:4], d[base + 1:base + sw * 4:4], d[base + 2:base + sw * 4:4], d[base + 3:base + sw * 4:4]
        row = []
        for x0, x1 in xr:
            aa = a_[x0:x1]
            sa = sum(aa)
            row.append((sum(p * q for p, q in zip(r_[x0:x1], aa)), sum(p * q for p, q in zip(g_[x0:x1], aa)),
                        sum(p * q for p, q in zip(b_[x0:x1], aa)), sa, x1 - x0))
        tmp.append(row)
    o = Img(w, h)
    od = o.d
    for y, (y0, y1) in enumerate(yr):
        for x in range(w):
            R = G = B = A = N = 0
            for yy in range(y0, y1):
                c = tmp[yy][x]
                R += c[0]
                G += c[1]
                B += c[2]
                A += c[3]
                N += c[4]
            i = (y * w + x) * 4
            if A:
                od[i], od[i + 1], od[i + 2] = R // A, G // A, B // A
            od[i + 3] = A // N if N else 0
    return o


def fit_dims(w, h, long_edge=None, tokens=None):
    s = 1.0
    if long_edge:
        s = min(s, long_edge / max(w, h))
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    if tokens:
        while math.ceil(nw / 28) * math.ceil(nh / 28) > tokens and max(nw, nh) > 28:
            f = (max(nw, nh) - 28) / max(nw, nh)
            nw, nh = max(1, int(nw * f)), max(1, int(nh * f))
    return nw, nh


def token_cost(w, h):
    res = {}
    for name, (edge, cap) in TIERS.items():
        nw, nh = fit_dims(w, h, edge, cap)
        res[name] = {"tokens": math.ceil(nw / 28) * math.ceil(nh / 28), "read_at": [nw, nh]}
    return res


def crop(img, x, y, w, h):
    x, y = max(0, x), max(0, y)
    w, h = min(w, img.w - x), min(h, img.h - y)
    if w <= 0 or h <= 0:
        raise Fail("crop box is outside the image")
    o = Img(w, h)
    sw = img.w * 4
    o.d = bytearray(b"".join(img.d[(y + r) * sw + x * 4:(y + r) * sw + (x + w) * 4] for r in range(h)))
    return o


def paste(dst, src, x, y):
    for r in range(src.h):
        ty = y + r
        if 0 <= ty < dst.h:
            x0, x1 = max(0, x), min(dst.w, x + src.w)
            if x1 > x0:
                s = src.d[(r * src.w + (x0 - x)) * 4:(r * src.w + (x1 - x)) * 4]
                dst.d[(ty * dst.w + x0) * 4:(ty * dst.w + x1) * 4] = s


def flatten(img, bg=(255, 255, 255)):
    """Composite over a background; returns RGB triples."""
    d = img.d
    res = []
    for i in range(0, len(d), 4):
        a = d[i + 3]
        if a == 255:
            res.append((d[i], d[i + 1], d[i + 2]))
        else:
            res.append(tuple((d[i + k] * a + bg[k] * (255 - a)) // 255 for k in range(3)))
    return res


# ---------------------------------------------------------------- 5x7 label font (no font files needed)

FONT = {
    "A": "0E11111F111111", "B": "1E11111E11111E", "C": "0E11101010110E", "D": "1E11111111111E",
    "E": "1F10101E10101F", "F": "1F10101E101010", "G": "0E11101711110F", "H": "1111111F111111",
    "I": "0E04040404040E", "J": "0702020202120C", "K": "11121418141211", "L": "1010101010101F",
    "M": "111B1515111111", "N": "11111915131111", "O": "0E11111111110E", "P": "1E11111E101010",
    "Q": "0E11111115120D", "R": "1E11111E141211", "S": "0F10100E01011E", "T": "1F040404040404",
    "U": "1111111111110E", "V": "11111111110A04", "W": "1111111515150A", "X": "11110A040A1111",
    "Y": "11110A04040404", "Z": "1F01020408101F", "0": "0E11131519110E", "1": "040C040404040E",
    "2": "0E11010204081F", "3": "1F02040201110E", "4": "02060A121F0202", "5": "1F101E0101110E",
    "6": "0608101E11110E", "7": "1F010204080808", "8": "0E11110E11110E", "9": "0E11110F01020C",
}


def draw_label(img, text, x, y, scale=3, fg=(255, 255, 255, 255), bg=(0, 0, 0, 255)):
    text = text.upper()
    bw, bh = (len(text) * 6 + 1) * scale, 9 * scale
    for yy in range(y, min(img.h, y + bh)):
        for xx in range(x, min(img.w, x + bw)):
            img.put(xx, yy, bg)
    for n, chr_ in enumerate(text):
        g = FONT.get(chr_)
        if not g:
            continue
        for row in range(7):
            bits = int(g[row * 2:row * 2 + 2], 16)
            for col in range(5):
                if bits & (1 << (4 - col)):
                    for sy in range(scale):
                        for sx in range(scale):
                            px_, py_ = x + (1 + n * 6 + col) * scale + sx, y + (1 + row) * scale + sy
                            if px_ < img.w and py_ < img.h:
                                img.put(px_, py_, fg)


def letters(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


# ---------------------------------------------------------------- colour

def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lab(rgb):
    r, g, b = (_lin(v) for v in rgb[:3])
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de2000(l1, l2):
    L1, a1, b1 = l1
    L2, a2, b2 = l2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = a1 * (1 + G), a2 * (1 + G)
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dth = 30 * math.exp(-((hbp - 275) / 25) ** 2)
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def hexc(c):
    return "#%02x%02x%02x" % tuple(c[:3])


def parse_hex(s):
    s = s.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise Fail("not a hex colour: %s" % s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def get_palette(spec):
    """A built-in name, a .hex/.txt/.gpl file, comma-separated hex, or a Lospec slug (fetched, cached in ARTWRIGHT_HOME)."""
    if spec in PALETTES:
        return spec, [parse_hex(x) for x in PALETTES[spec].split()]
    p = Path(spec)
    if p.is_file():
        cols = []
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"\s*(\d+)\s+(\d+)\s+(\d+)", line)
            if m and p.suffix.lower() == ".gpl":
                cols.append(tuple(int(m.group(k)) for k in (1, 2, 3)))
            else:
                cols += [parse_hex(h) for h in re.findall(r"#?\b[0-9a-fA-F]{6}\b", line)]
        return p.stem, cols
    if "," in spec or re.fullmatch(r"#?[0-9a-fA-F]{6}", spec):
        return "custom", [parse_hex(x) for x in spec.split(",") if x.strip()]
    if not re.fullmatch(r"[a-z0-9-]{2,64}", spec):
        raise Fail("unknown palette %s" % spec)
    cache = home() / "palettes" / (spec + ".json")
    if cache.is_file():
        data = json.loads(cache.read_text(encoding="utf-8"))
    else:
        data = http_json("https://lospec.com/palette-list/%s.json" % spec)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(data), encoding="utf-8")
    cols = [parse_hex(c.lower()) for c in data.get("colors", [])]
    if not cols:
        raise Fail("Lospec palette %s has no colours" % spec)
    return spec, cols


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        raise Fail("fetch failed: %s (%s)" % (url, e))


def median_cut(cols, k):
    """cols: list of (r,g,b). Returns [(mean colour, count)] largest first."""
    boxes = [cols]
    while len(boxes) < k:
        best, bi, bc = -1, None, None
        for i, b in enumerate(boxes):
            if len(b) < 2:
                continue
            for c in range(3):
                vals = [p[c] for p in b]
                rng = (max(vals) - min(vals)) * math.sqrt(len(b))
                if rng > best:
                    best, bi, bc = rng, i, c
        if bi is None or best <= 0:
            break
        b = sorted(boxes.pop(bi), key=lambda p: p[bc])
        m = len(b) // 2
        boxes += [b[:m], b[m:]]
    res = []
    for b in boxes:
        if b:
            n = len(b)
            res.append((tuple(sum(p[c] for p in b) // n for c in range(3)), n))
    return sorted(res, key=lambda t: -t[1])


# ---------------------------------------------------------------- helpers for analysis

def _halve(img):
    """2x2 area average (premultiplied by alpha)."""
    w, h, d, sw = img.w // 2, img.h // 2, img.d, img.w * 4
    o = Img(w, h)
    od = o.d
    for y in range(h):
        r0 = 2 * y * sw
        r1 = r0 + sw
        for x in range(w):
            i, j, k = r0 + 8 * x, r1 + 8 * x, (y * w + x) * 4
            a0, a1, a2, a3 = d[i + 3], d[i + 7], d[j + 3], d[j + 7]
            A = a0 + a1 + a2 + a3
            if A:
                for c in range(3):
                    od[k + c] = (d[i + c] * a0 + d[i + 4 + c] * a1 + d[j + c] * a2 + d[j + 4 + c] * a3) // A
            od[k + 3] = A // 4
    return o


def small(img, edge=256):
    """The measuring copy. Every source pixel counts: a reduction over 4x through resize_box's nearest pre-step
    reads fine detail as false texture (aliasing), so it goes through Pillow's BOX filter, or 2x2 halving without
    Pillow (slower)."""
    if max(img.w, img.h) <= edge:
        return img
    w, h = fit_dims(img.w, img.h, edge)
    if img.w > 4 * w and img.h > 4 * h:
        Image, _ = _pillow()
        if Image is not None:
            im = Image.frombytes("RGBA", (img.w, img.h), bytes(img.d)).resize((w, h), Image.BOX)
            return Img(w, h, bytearray(im.tobytes()))
        while img.w >= 4 * w and img.h >= 4 * h:
            img = _halve(img)
    return resize_box(img, w, h)


def luma_list(img, bg=(255, 255, 255)):
    return [(0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0 for r, g, b in flatten(img, bg)]


def alpha_mask(img, cut=128):
    """Which pixels a statistic reads: alpha at `cut` or above. Transparent pixels are left out instead of being
    read as white (a sprite on a transparent canvas otherwise reports its background as clipped highlights)."""
    keep = [v >= cut for v in img.d[3::4]]
    k = sum(keep)
    if not k:
        raise Fail("no opaque pixels (alpha %d or more)" % cut)
    share = 1 - k / len(keep)
    info = {"transparent_share": round(share, 4), "excluded": share > 0}
    if share > 0:
        info["note"] = "value and colour statistics read the opaque pixels only (alpha %d and up)" % cut
    return keep, info


def mean_sd(v):
    n = len(v)
    if not n:
        return 0.0, 0.0
    m = sum(v) / n
    return m, math.sqrt(sum((x - m) ** 2 for x in v) / n)


def sobel(lum, w, h):
    mag = [0.0] * (w * h)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            i = y * w + x
            a, b, c = lum[i - w - 1], lum[i - w], lum[i - w + 1]
            d, f = lum[i - 1], lum[i + 1]
            g, hh, k = lum[i + w - 1], lum[i + w], lum[i + w + 1]
            gx = (c + 2 * f + k) - (a + 2 * d + g)
            gy = (g + 2 * hh + k) - (a + 2 * b + c)
            mag[i] = math.hypot(gx, gy)
    return mag


def gray_img(vals, w, h):
    o = Img(w, h)
    g = bytes(max(0, min(255, int(v * 255))) for v in vals)
    o.d[0::4] = o.d[1::4] = o.d[2::4] = g
    o.d[3::4] = b"\xff" * (w * h)
    return o


def inputs(paths):
    res = []
    for p in paths:
        q = Path(p)
        if q.is_dir():
            res += sorted(str(f) for f in q.iterdir() if f.suffix.lower() in IMG_EXT)
        else:
            res.append(p)
    return res


# ---------------------------------------------------------------- commands

def cmd_doctor(a):
    Image, pv = _pillow()
    ff = shutil.which("ffmpeg")
    res = {"artwright": VERSION, "python": sys.version.split()[0], "python_ok": sys.version_info >= (3, 9),
           "pillow": pv, "ffmpeg": bool(ff), "home": str(home()), "home_exists": home().is_dir(),
           "decode": ["pillow"] if Image else (["png (stdlib)"] + (["jpeg, webp and more (ffmpeg)"] if ff else [])),
           "notes": []}
    if not Image and not ff:
        res["notes"].append("PNG only: install Pillow (pip install pillow) or ffmpeg to read JPEG and WebP")
    if a.probe:
        probes = {}
        for name, url in (("cleveland", "https://openaccess-api.clevelandart.org/api/artworks/1958.21"),
                          ("lospec", "https://lospec.com/palette-list/pico-8.json")):
            try:
                d = http_json(url)
                probes[name] = {"ok": True, "keys": sorted(d)[:6]}
            except Fail as e:
                probes[name] = {"ok": False, "error": str(e)}
        res["probe"] = probes
    return out(res)


def cmd_info(a):
    items = []
    for f in inputs(a.images):
        try:
            img = load(f)
        except Fail as e:
            items.append({"file": f, "ok": False, "error": str(e)})
            continue
        alpha = img.d[3::4]
        amin, amax = min(alpha), max(alpha)
        partial = sum(1 for v in alpha if 0 < v < 255)
        cols = len(set(zip(img.d[0::4], img.d[1::4], img.d[2::4], alpha)))
        items.append({"file": f, "ok": True, "format": fmt_of(f), "bytes": Path(f).stat().st_size,
                      "size": [img.w, img.h], "sha256": sha256(f),
                      "alpha": "none" if amin == 255 else ("binary" if partial == 0 else "partial"),
                      "partial_alpha_pixels": partial, "unique_colours": cols, "tokens": token_cost(img.w, img.h)})
    return out({"items": items}, 0 if all(i["ok"] for i in items) else 1)


def cmd_fit(a):
    img = load(a.image)
    if a.crop:
        x, y, w, h = (int(v) for v in a.crop.split(","))
        img = crop(img, x, y, w, h)
    if a.cell:
        m = re.fullmatch(r"(\d+)x(\d+):(\d+)", a.cell)
        if not m:
            raise Fail("--cell is RxC:i, e.g. 2x3:4 (row-major, from 0)")
        R, C, i = (int(v) for v in m.groups())
        cw, ch = img.w // C, img.h // R
        img = crop(img, (i % C) * cw, (i // C) * ch, cw, ch)
    if a.pixel:
        long_ = a.long or 1024
        k = max(1, long_ // max(img.w, img.h)) if max(img.w, img.h) <= long_ else None
        if k:
            img = resize_nearest(img, img.w * k, img.h * k)
        else:
            w, h = fit_dims(img.w, img.h, long_, a.tokens)
            img = resize_nearest(img, w, h)
    else:
        w, h = fit_dims(img.w, img.h, a.long or (None if a.tokens else 1024), a.tokens)
        if (w, h) != (img.w, img.h):
            img = resize_box(img, w, h)
    save_png(img, a.out)
    return out({"out": a.out, "size": [img.w, img.h], "tokens": token_cost(img.w, img.h)})


def cmd_sheet(a):
    files = inputs(a.images)
    if not files:
        raise Fail("no images")
    n = len(files)
    cols = a.cols or math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    pad = 6
    cell = min(a.cell, (SHEET_MAX - pad * (cols + 1)) // cols, (SHEET_MAX - pad * (rows + 1)) // rows)
    if cell < 32:
        raise Fail("too many images for one %d px sheet; split the batch" % SHEET_MAX)
    W, H = pad + cols * (cell + pad), pad + rows * (cell + pad)
    bg = tuple(int(v) for v in a.bg.split(","))
    if len(bg) != 3 or not all(0 <= v <= 255 for v in bg):
        raise Fail("--bg takes R,G,B")
    sheet = Img(W, H, bytearray(bytes(bg + (255,)) * (W * H)))
    mapping, scale = {}, max(2, cell // 96)
    for i, f in enumerate(files):
        lab_ = letters(i)
        try:
            img = load(f)
        except Fail as e:
            mapping[lab_] = {"file": f, "error": str(e)}
            continue
        w, h = fit_dims(img.w, img.h, cell)
        if a.pixel and max(img.w, img.h) <= cell:
            k = cell // max(img.w, img.h)
            w, h = img.w * k, img.h * k
        t = resize_nearest(img, w, h) if a.pixel else resize_box(img, w, h)
        t = Img(t.w, t.h, bytearray(b"".join(bytes(c) for c in
                                             ((r, g, b, 255) for r, g, b in flatten(t, bg)))))
        cx, cy = pad + (i % cols) * (cell + pad), pad + (i // cols) * (cell + pad)
        paste(sheet, t, cx + (cell - w) // 2, cy + (cell - h) // 2)
        if not a.no_labels:
            draw_label(sheet, lab_, cx, cy, scale)
        mapping[lab_] = {"file": f}
    save_png(sheet, a.out)
    return out({"out": a.out, "size": [W, H], "cell": cell, "map": mapping, "tokens": token_cost(W, H)})


def cmd_stats(a):
    img = load(a.image)
    s = small(img, a.edge)
    w, h = s.w, s.h
    keep, alpha = alpha_mask(s)
    flat = flatten(s)
    # spatial measures (edges, symmetry, balance, focal cell, notan) read the full grid on white
    lum_all = [(0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0 for r, g, b in flat]
    rgb = [c[:3] for c, k in zip(s.pixels(), keep) if k] if alpha["excluded"] else flat
    luma_m = mean_sd([(0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0 for r, g, b in rgb])[0]
    labs_grid = [lab(c) for c in (s.pixels() if alpha["excluded"] else flat)]
    labs = [p for p, k in zip(labs_grid, keep) if k]
    lstar = [p[0] for p in labs]
    # value is lightness (L*/100), not luma on encoded sRGB: luma reads pure blue as 0.07, L* as 0.32
    lum = [v / 100 for v in lstar]
    n = len(lum)
    m, sd = mean_sd(lum)
    hist = [0] * 10
    for v in lum:
        hist[min(9, int(v * 10))] += 1
    hist = [round(c / n, 3) for c in hist]
    sm = [0] * 16
    for v in lum:
        sm[min(15, int(v * 16))] += 1
    peaks = sum(1 for i in range(16) if sm[i] > n * 0.03 and sm[i] >= (sm[i - 1] if i else 0)
                and sm[i] >= (sm[i + 1] if i < 15 else 0))
    rg = [r - g for r, g, b in rgb]
    yb = [0.5 * (r + g) - b for r, g, b in rgb]
    mrg, srg = mean_sd(rg)
    myb, syb = mean_sd(yb)
    M = math.sqrt(srg ** 2 + syb ** 2) + 0.3 * math.sqrt(mrg ** 2 + myb ** 2)
    level = min(HS_LEVELS, key=lambda t: abs(M - t[0]))[1]
    sats, warm, cool, hot = [], 0, 0, 0
    for r, g, b in rgb:
        hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        sats.append(ss)
        if ss > 0.8 and vv > 0.8:
            hot += 1
        if ss > 0.15 and vv > 0.15:
            deg = hh * 360
            if deg < 90 or deg >= 300:
                warm += 1
            else:
                cool += 1
    mag = sobel(lum_all, w, h)
    edges = [v > 0.4 for v in mag]
    edens = sum(edges) / (w * h)
    diff_lr = sum(abs(lum_all[y * w + x] - lum_all[y * w + (w - 1 - x)]) for y in range(h) for x in range(w // 2))
    diff_tb = sum(abs(lum_all[y * w + x] - lum_all[(h - 1 - y) * w + x]) for y in range(h // 2) for x in range(w))
    sym_lr = 1 - diff_lr / max(1, h * (w // 2))
    sym_tb = 1 - diff_tb / max(1, w * (h // 2))
    m_all = mean_sd(lum_all)[0]
    wt = [abs(v - m_all) for v in lum_all]
    tw = sum(wt) or 1.0
    cx = sum(wt[i] * (i % w) for i in range(w * h)) / tw / max(1, w - 1)
    cy = sum(wt[i] * (i // w) for i in range(w * h)) / tw / max(1, h - 1)
    imbalance = min(100.0, 200 * math.hypot(cx - 0.5, cy - 0.5))
    focal = focal_cell(lum_all, w, h)
    thirds = min(math.hypot(focal[0] - tx, focal[1] - ty) for tx in (1 / 3, 2 / 3) for ty in (1 / 3, 2 / 3))
    # box-counting fractal dimension of the edge map
    pts, fd = [], None
    for size in (2, 4, 8, 16, 32, 64):
        if size * 4 > min(w, h):
            break
        boxes = set()
        for i, e in enumerate(edges):
            if e:
                boxes.add(((i % w) // size, (i // w) // size))
        if boxes:
            pts.append((math.log(1 / size), math.log(len(boxes))))
    if len(pts) >= 3:
        mx = sum(p[0] for p in pts) / len(pts)
        my = sum(p[1] for p in pts) / len(pts)
        fd = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
    # value structure in L*: the middle band, the two-family valley, clipping and the highlight tint
    lh = [0] * 20
    for v in lstar:
        lh[max(0, min(19, int(v / 5)))] += 1
    sm3 = [(lh[max(0, i - 1)] + lh[i] + lh[min(19, i + 1)]) / 3 for i in range(20)]
    pk = sorted((i for i in range(20) if sm3[i] >= (sm3[i - 1] if i else 0) and sm3[i] >= (sm3[i + 1] if i < 19 else 0)),
                key=lambda i: -sm3[i])
    bim = 0.0
    if pk:
        p2 = [j for j in pk if abs(j - pk[0]) >= 3]
        if p2:
            lo_, hi_ = sorted((pk[0], p2[0]))
            bim = 1 - min(sm3[lo_:hi_ + 1]) / (min(sm3[pk[0]], sm3[p2[0]]) or 1)
    top_ = sorted(labs, key=lambda p: -p[0])[:max(1, n // 200)]
    ha, hb = sum(p[1] for p in top_) / len(top_), sum(p[2] for p in top_) / len(top_)
    # saturation hierarchy: median chroma per cell of an 8x8 grid
    cc = []
    for gy in range(8):
        for gx in range(8):
            v = [chroma(labs_grid[y * w + x]) for y in range(gy * h // 8, (gy + 1) * h // 8)
                 for x in range(gx * w // 8, (gx + 1) * w // 8) if keep[y * w + x]]
            cc.append(med(v) if v else None)
    cpk = max((i for i in range(64) if cc[i] is not None), key=lambda i: cc[i])
    cpc = ((cpk % 8 + 0.5) / 8, (cpk // 8 + 0.5) / 8)
    cm_, csd = mean_sd([c for c in cc if c is not None])
    bvals = [p[2] for p in labs]
    res = {"file": a.image, "size": [img.w, img.h], "measured_at": [w, h], "alpha": alpha,
           "value": {"mean": round(m, 3), "scale": "L*/100", "luma_mean": round(luma_m, 3),
                     "key": "low" if m < 0.38 else ("high" if m > 0.68 else "middle"),
                     "histogram_10": hist, "groups_estimate": peaks,
                     "middle_share": round(sum(1 for v in lstar if 35 <= v <= 65) / n, 3), "bimodality": round(bim, 3),
                     "clip_black": round(sum(1 for v in lstar if v < 3) / n, 4),
                     "clip_white": round(sum(1 for v in lstar if v > 97) / n, 4),
                     "highlight_tint": {"C": round(math.hypot(ha, hb), 1), "hue": hue_name(hue_of(ha, hb))},
                     "note": "groups_estimate counts tones, not masses: comp counts masses"},
           "chroma_cells": {"mean": round(cm_, 2), "spread": round(csd / cm_, 3) if cm_ else 0.0,
                            "peak_cell": list(cpc), "peak_focal_distance": round(math.hypot(cpc[0] - focal[0], cpc[1] - focal[1]), 3)},
           "rms_contrast": round(mean_sd(lstar)[1], 2),
           "noise": dict(zip(("sigma_L", "reading"), noise_sigma([p[0] for p in labs_grid], w, h)),
                         proxy="flattest tenth of 16x16 cells", note="grain, not texture: SD in L* units"),
           "colourfulness": {"M": round(M, 1), "level": level, "method": "Hasler-Suesstrunk 2003, signed rg/yb, nearest Table 2 anchor"},
           "saturation": {"mean": round(sum(sats) / n, 3), "share_hot": round(hot / n, 3)},
           "temperature": {"warm_share": round(warm / max(1, warm + cool), 3), "chromatic_share": round((warm + cool) / n, 3),
                           "b_mean": round(mean_sd(bvals)[0], 2), "b_sd": round(mean_sd(bvals)[1], 2),
                           "note": "warm_share buckets HSV hue (yellow-green counts as warm); judge temperature "
                                   "relatively with light (lights against shadows)"},
           "edge_density": round(edens, 3),
           "mirror_symmetry": {"left_right": round(sym_lr, 3), "top_bottom": round(sym_tb, 3)},
           "balance": {"centre_of_mass": [round(cx, 3), round(cy, 3)], "imbalance_pct": round(imbalance, 1),
                       "note": "0 is centred; one centre-of-mass offset, not the Aesthetics Toolbox eight-axis Balance"},
           "focal_cell": [round(focal[0], 3), round(focal[1], 3)],
           "thirds_distance": round(thirds, 3),
           "fractal_dimension": round(fd, 3) if fd is not None else None,
           "note": "descriptions, not a beauty score; thirds_distance is never a reason (references/evidence.md)"}
    if a.notan:
        # cut where the values divide (Otsu; k-means for three), not at the median: the shares are the point
        d = Path(a.notan)
        L_all = [p[0] / 100 for p in labs_grid] if not alpha["excluded"] else [lab(c)[0] / 100 for c in flat]
        mid = otsu(lum)
        cs = kmeans1(lum, 3)[0]
        t1, t2 = (cs[0] + cs[1]) / 2, (cs[1] + cs[2]) / 2
        res["notan"] = {
            "grey": save_png(gray_img(L_all, w, h), d / "grey.png"),
            "two_value": save_png(gray_img([1.0 if v > mid else 0.0 for v in L_all], w, h), d / "notan2.png"),
            "three_value": save_png(gray_img([1.0 if v > t2 else (0.5 if v > t1 else 0.0) for v in L_all], w, h),
                                    d / "notan3.png"),
            "cut_two": round(mid, 3), "light_share": round(sum(v > mid for v in lum) / n, 3),
            "cuts_three": [round(t1, 3), round(t2, 3)],
            "shares_three": [round(sum(v <= t1 for v in lum) / n, 3), round(sum(t1 < v <= t2 for v in lum) / n, 3),
                             round(sum(v > t2 for v in lum) / n, 3)]}
    return out(res)


def cmd_palette(a):
    img = small(load(a.image), 128)
    cols = [(r, g, b) for r, g, b, al in img.pixels() if al >= 128]
    if not cols:
        raise Fail("the image is fully transparent")
    mc = median_cut(cols, a.k)
    n = len(cols)
    res = {"file": a.image, "colours": [{"hex": hexc(c), "share": round(k / n, 3)} for c, k in mc]}
    if a.against:
        name, pal = get_palette(a.against)
        pl = [(c, lab(c)) for c in pal]
        rows, total = [], 0.0
        for item, (c, k) in zip(res["colours"], mc):
            lc = lab(c)
            best = min(pl, key=lambda t: de2000(lc, t[1]))
            dE = de2000(lc, best[1])
            total += dE * k
            item.update({"nearest": hexc(best[0]), "delta_e": round(dE, 2)})
        res["against"] = {"palette": name, "size": len(pal), "weighted_delta_e": round(total / n, 2),
                          "note": "delta-E 2000; under 2 is hard to see, over 10 is a different colour"}
    return out(res)


# ----- pixel checks

def _profiles(img, tol):
    w, h, d = img.w, img.h, img.d
    colx, rowy = [0] * w, [0] * h
    for y in range(h):
        b = y * w * 4
        for x in range(1, w):
            i = b + x * 4
            if abs(d[i] - d[i - 4]) + abs(d[i + 1] - d[i - 3]) + abs(d[i + 2] - d[i - 2]) + abs(d[i + 3] - d[i - 1]) > tol:
                colx[x] += 1
    for y in range(1, h):
        b, p = y * w * 4, (y - 1) * w * 4
        for x in range(w):
            i, j = b + x * 4, p + x * 4
            if abs(d[i] - d[j]) + abs(d[i + 1] - d[j + 1]) + abs(d[i + 2] - d[j + 2]) + abs(d[i + 3] - d[j + 3]) > tol:
                rowy[y] += 1
    return colx, rowy


def _align(prof, s):
    total = sum(prof)
    if not total:
        return 1.0, 0
    best = max(range(s), key=lambda o: sum(prof[o::s]))
    return sum(prof[best::s]) / total, best


def _spacing_mode(prof):
    if not any(prof):
        return 1
    m, sd = mean_sd(prof)
    peaks = [i for i in range(1, len(prof) - 1) if prof[i] > m + 0.5 * sd and prof[i] >= prof[i - 1] and prof[i] >= prof[i + 1]]
    gaps = [b - a for a, b in zip(peaks, peaks[1:]) if b - a > 1]
    if not gaps:
        return 1
    cnt = {}
    for g in gaps:
        cnt[g] = cnt.get(g, 0) + 1
    return max(cnt, key=lambda g: (cnt[g], g))


def detect_grid(img, tol=24, max_scale=64):
    colx, rowy = _profiles(img, tol)
    clean = 1
    for s in range(2, min(max_scale, img.w, img.h) + 1):
        ax, _ = _align(colx, s)
        ay, _ = _align(rowy, s)
        if ax >= 0.98 and ay >= 0.98:
            clean = s
    if clean > 1:
        s = clean
    else:
        sx, sy = _spacing_mode(colx), _spacing_mode(rowy)
        s = max(1, round((sx + sy) / 2)) if abs(sx - sy) <= 1 else max(sx, sy)
        # a peak spacing counts only when the changes gather on that lattice well above chance (1/s)
        if s > 1 and min(_align(colx, s)[0], _align(rowy, s)[0]) < 1.6 / s:
            s = 1
    ax, ox = _align(colx, s)
    ay, oy = _align(rowy, s)
    return {"scale": s, "offset": [ox, oy], "lattice_alignment": round(min(ax, ay) * 100, 1),
            "alignment_x": round(ax * 100, 1), "alignment_y": round(ay * 100, 1)}


def downsample_dominant(img, s, ox, oy):
    """One pixel per block: the block's dominant colour. Returns (native image, uniform-block share)."""
    nw, nh = (img.w - ox) // s, (img.h - oy) // s
    o = Img(max(1, nw), max(1, nh))
    uniform = 0
    for by in range(nh):
        for bx in range(nw):
            cnt = {}
            for y in range(oy + by * s, oy + (by + 1) * s):
                i = (y * img.w + ox + bx * s) * 4
                row = img.d[i:i + s * 4]
                for k in range(0, s * 4, 4):
                    c = bytes(row[k:k + 4])
                    cnt[c] = cnt.get(c, 0) + 1
            c = max(cnt, key=cnt.get)
            if len(cnt) == 1:
                uniform += 1
            o.d[(by * o.w + bx) * 4:(by * o.w + bx) * 4 + 4] = c
    return o, uniform / max(1, nw * nh)


def transitional_share(img, tol=24):
    """Pixels lying between differing neighbours (blend pixels, not a hard edge). Measured on the raw image.
    A run touching a fully transparent pixel is skipped: its RGB is not a colour (often 0,0,0)."""
    w, h, d = img.w, img.h, img.d
    hits = total = 0
    for y in range(h):
        for x in range(1, w - 1):
            i = (y * w + x) * 4
            if not (d[i - 1] and d[i + 3] and d[i + 7]):
                continue
            a, c, b = d[i - 4:i - 1], d[i:i + 3], d[i + 4:i + 7]
            ab = sum(abs(p - q) for p, q in zip(a, b))
            if ab <= tol * 2:
                continue
            total += 1
            ac = sum(abs(p - q) for p, q in zip(a, c))
            cb = sum(abs(p - q) for p, q in zip(c, b))
            if ac > tol and cb > tol and ac < ab and cb < ab:
                hits += 1
    return hits / max(1, w * h)


def orphans(img):
    w, h, res = img.w, img.h, []
    for y in range(h):
        for x in range(w):
            c = img.px(x, y)
            if c[3] == 0:
                continue
            alone = True
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h and img.px(x + dx, y + dy) == c:
                        alone = False
                        break
                if not alone:
                    break
            if alone:
                res.append([x, y])
    return res


def jaggies(img):
    """Derek Yu's rule on the silhouette: along a curve, step lengths grow or shrink monotonically."""
    w, h = img.w, img.h
    op = [[img.px(x, y)[3] > 0 for x in range(w)] for y in range(h)]

    def count(seq):
        seq = [v for v in seq if v is not None]
        runs, k = [], 1
        for p, q in zip(seq, seq[1:]):
            if q == p:
                k += 1
            else:
                runs.append((k, (q > p) - (q < p)))
                k = 1
        bad = 0
        for (l0, d0), (l1, d1), (l2, d2) in zip(runs, runs[1:], runs[2:]):
            if d0 == d1 == d2 and l1 < l0 and l1 < l2:
                bad += 1
        return bad
    left = [next((x for x in range(w) if op[y][x]), None) for y in range(h)]
    right = [next((x for x in range(w - 1, -1, -1) if op[y][x]), None) for y in range(h)]
    top = [next((y for y in range(h) if op[y][x]), None) for x in range(w)]
    bottom = [next((y for y in range(h - 1, -1, -1) if op[y][x]), None) for x in range(w)]
    return sum(count(s) for s in (left, right, top, bottom))


def outline(img):
    w, h, cnt = img.w, img.h, {}
    for y in range(h):
        for x in range(w):
            c = img.px(x, y)
            if c[3] == 0:
                continue
            if any(not (0 <= x + dx < w and 0 <= y + dy < h) or img.px(x + dx, y + dy)[3] == 0
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                k = hexc(c)
                cnt[k] = cnt.get(k, 0) + 1
    tot = sum(cnt.values())
    top = sorted(cnt.items(), key=lambda t: -t[1])[:5]
    return {"pixels": tot, "colours": len(cnt), "top": [{"hex": k, "share": round(v / tot, 3)} for k, v in top]} if tot else None


def tile_seams(img):
    w, h = img.w, img.h

    def dist(p, q):
        return sum(abs(a - b) for a, b in zip(p[:3], q[:3]))
    inner = [dist(img.px(x, y), img.px(x + 1, y)) for y in range(h) for x in range(w - 1)]
    m_in = sum(inner) / max(1, len(inner))
    lr = sum(dist(img.px(w - 1, y), img.px(0, y)) for y in range(h)) / h
    tb = sum(dist(img.px(x, h - 1), img.px(x, 0)) for x in range(w)) / w
    return {"inner_mean": round(m_in, 1), "wrap_left_right": round(lr, 1), "wrap_top_bottom": round(tb, 1),
            "seam_suspected": lr > 2 * m_in + 10 or tb > 2 * m_in + 10}


def jpeg_blocks(img, tol):
    """Share of colour steps on the 8 px lattice (the lower of the two axes). A JPEG's block edges sit there, and
    every one of them is also on the 2 and 4 px lattices, so a smooth JPEG reads as scale 2 pixel art; real scale 2
    or 4 art has about a quarter or half of its steps on the 8 px lattice."""
    lx, ly = _profiles(img, tol)
    return min(_align(lx, 8)[0], _align(ly, 8)[0])


def pixel_one(path, a):
    img = load(path)
    g = detect_grid(img, a.tol) if not a.scale else {"scale": a.scale, "offset": [0, 0]}
    if not a.scale and g["scale"] in (2, 4, 8, 16) and fmt_of(path) == "jpeg":
        if g["scale"] < 8 and jpeg_blocks(img, a.tol) >= 0.8:
            g = {"scale": 1, "offset": [0, 0], "lattice_alignment": 100.0,
                 "note": "JPEG: the %d px lattice is the 8 px block edges, not a pixel grid; pass --scale if it is "
                         "real" % g["scale"]}
        elif g["scale"] >= 8:
            g["note"] = "JPEG blocks are 8 px: check a scale of 8 or 16 by eye before trusting it"
    if a.scale:
        colx, rowy = _profiles(img, a.tol)
        ax, ox = _align(colx, a.scale)
        ay, oy = _align(rowy, a.scale)
        g.update({"offset": [ox, oy], "lattice_alignment": round(min(ax, ay) * 100, 1)})
    s, (ox, oy) = g["scale"], g["offset"]
    native, uniform = downsample_dominant(img, s, ox, oy) if s > 1 else (img, 1.0)
    alpha = img.d[3::4]
    partial = sum(1 for v in alpha if 0 < v < 255)
    opaque = [c for c in native.pixels() if c[3] > 0]
    uniq = sorted(set(c[:3] for c in opaque))
    near = 0
    if len(uniq) <= 256:
        labs = [lab(c) for c in uniq]
        near = sum(1 for i in range(len(labs)) for j in range(i + 1, len(labs)) if de2000(labs[i], labs[j]) < 3)
    trans = transitional_share(img, a.tol)
    orph = orphans(native) if native.w * native.h <= 512 * 512 else None
    res = {"file": path, "size": [img.w, img.h], "grid": g, "native_size": [native.w, native.h],
           "uniform_blocks": round(uniform * 100, 1), "transitional_pixels": round(trans * 100, 2),
           "unique_colours": len(uniq), "budget": a.budget, "near_duplicate_colour_pairs": near,
           "partial_alpha_pixels": partial,
           "orphans": None if orph is None else {"count": len(orph), "first": orph[:20]}}
    if min(alpha) < 255 and native.w * native.h <= 512 * 512:
        res["jaggies"] = jaggies(native)
        res["outline"] = outline(native)
    if a.palette:
        name, pal = get_palette(a.palette)
        ps = set(pal)
        off = [c for c in uniq if c not in ps]
        inside = sum(1 for c in opaque if c[:3] in ps)
        pl = [(c, lab(c)) for c in pal]
        res["palette"] = {"name": name, "match": round(inside / max(1, len(opaque)) * 100, 1),
                          "off_palette": [{"hex": hexc(c), "nearest": hexc(min(pl, key=lambda t: de2000(lab(c), t[1]))[0])}
                                          for c in off[:20]], "off_palette_count": len(off)}
    if a.tile:
        res["tile"] = tile_seams(native)
        if a.preview:
            t = Img(native.w * 3, native.h * 3)
            for k in range(9):
                paste(t, native, (k % 3) * native.w, (k // 3) * native.h)
            res["tile"]["preview"] = save_png(resize_nearest(t, t.w * a.zoom, t.h * a.zoom),
                                              Path(a.preview).with_name(Path(a.preview).stem + "_tile3x3.png"))
    if a.preview and not a.tile:
        res["preview"] = save_png(resize_nearest(native, native.w * a.zoom, native.h * a.zoom), a.preview)
    fails = []
    if s < 1 or g.get("lattice_alignment", 100) < 100:
        fails.append("off-grid pixels (lattice alignment %s%%)" % g.get("lattice_alignment"))
    if uniform < 1:
        fails.append("blocks not uniform (%s%%)" % res["uniform_blocks"])
    # at a scale the caller states as 1 the image is native: a one-pixel shading step between two colours is a
    # ramp, not a blend, so the share is reported but does not fail it (palette and budget still apply)
    if trans > 0.001 and a.scale != 1:
        fails.append("transitional (blend) pixels %s%%" % res["transitional_pixels"])
    if a.budget and len(uniq) > a.budget:
        fails.append("%d colours over a budget of %d" % (len(uniq), a.budget))
    elif not a.budget and len(uniq) > 256:
        fails.append("%d colours: not pixel art, or AI output never reduced to a palette" % len(uniq))
    if partial:
        fails.append("%d semi-transparent pixels" % partial)
    res["clean_pixel_art"] = not fails
    res["problems"] = fails
    return res, native


def cmd_pixel(a):
    files = inputs(a.images)
    items, natives = [], []
    for f in files:
        try:
            r, nat = pixel_one(f, a)
            items.append(r)
            natives.append(nat)
        except Fail as e:
            items.append({"file": f, "ok": False, "error": str(e)})
    res = {"items": items, "pass_rule": "one integer scale, 100% lattice alignment, uniform blocks, no blend pixels,"
                                        " colours within budget, binary alpha (R-20261021-8)"}
    if a.frames and len(natives) > 1:
        def bbox(im):
            xs = [i % im.w for i, v in enumerate(im.d[3::4]) if v]
            ys = [i // im.w for i, v in enumerate(im.d[3::4]) if v]
            return [min(xs), min(ys), max(xs), max(ys)] if xs else None
        pals = [set(c[:3] for c in n.pixels() if c[3]) for n in natives]
        union = set().union(*pals)
        boxes = [bbox(n) for n in natives]
        res["frames"] = {"count": len(natives), "scales": sorted(set(i.get("grid", {}).get("scale") for i in items if "grid" in i)),
                         "sizes": sorted(set(tuple(n.w for n in natives))), "palette_union": len(union),
                         "palette_per_frame": [len(p) for p in pals], "bboxes": boxes,
                         "baselines": [b[3] if b else None for b in boxes],
                         "baseline_consistent": len(set(b[3] for b in boxes if b)) <= 1}
    return out(res, 0 if all(i.get("ok", True) for i in items) else 1)


# ----- hashes

def ahash(img):
    g = luma_list(resize_box(img, 8, 8))
    m = sum(g) / 64
    return sum(1 << i for i, v in enumerate(g) if v > m)


def dhash(img):
    g = luma_list(resize_box(img, 9, 8))
    bits, k = 0, 0
    for y in range(8):
        for x in range(8):
            if g[y * 9 + x] > g[y * 9 + x + 1]:
                bits |= 1 << k
            k += 1
    return bits


def ham(a, b):
    return bin(a ^ b).count("1")


def cmd_hash(a):
    items = []
    for f in inputs(a.images):
        img = load(f)
        items.append({"file": f, "ahash": "%016x" % ahash(img), "dhash": "%016x" % dhash(img), "sha256": sha256(f)})
    return out({"items": items, "algo": {"name": "ahash+dhash", "bits": 64, "version": 1}})


def cmd_dedupe(a):
    files = inputs(a.images)
    hs = [(f, dhash(load(f))) for f in files]
    parent = list(range(len(hs)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    close = []
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            d = ham(hs[i][1], hs[j][1])
            if d <= a.threshold:
                parent[find(i)] = find(j)
                close.append({"a": hs[i][0], "b": hs[j][0], "distance": d})
    groups = {}
    for i in range(len(hs)):
        groups.setdefault(find(i), []).append(hs[i][0])
    dup = [g for g in groups.values() if len(g) > 1]
    return out({"groups": dup, "pairs": close, "keep": [g[0] for g in groups.values()],
                "threshold": {"algo": "dhash", "version": 1, "max_distance": a.threshold}})


# ----- compare, rank

def work_dir(a):
    d = Path(a.work)
    d.mkdir(parents=True, exist_ok=True)
    return d


def jl_read(p):
    p = Path(p)
    if not p.is_file():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return rows


def write_json(p, obj):
    with open(p, "w", encoding="utf-8", newline="\n") as f:  # Path.write_text has no newline= before 3.10
        f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def jl_add(p, row):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def two_up(left, right, cell):
    tiles = []
    for im in (left, right):
        w, h = fit_dims(im.w, im.h, cell)
        t = resize_box(im, w, h)
        tiles.append(Img(t.w, t.h, bytearray(b"".join(bytes((r, g, b, 255)) for r, g, b in flatten(t)))))
    pad = 12
    W = pad * 3 + cell * 2
    H = pad * 2 + cell
    o = Img(W, H, bytearray(b"\x80\x80\x80\xff" * (W * H)))
    for k, t in enumerate(tiles):
        x = pad + k * (cell + pad)
        paste(o, t, x + (cell - t.w) // 2, pad + (cell - t.h) // 2)
        draw_label(o, str(k + 1), x, pad, max(2, cell // 160))
    return o


def cmd_compare(a):
    wd = work_dir(a)
    if a.action == "prepare":
        if len(a.args) != 2:
            raise Fail("compare prepare A B")
        fa, fb = a.args
        ha, hb = sha256(fa), sha256(fb)
        if ha == hb:
            raise Fail("the two files are identical")
        pid = hashlib.sha256("|".join(sorted((ha, hb))).encode()).hexdigest()[:12]
        ia, ib = load(fa), load(fb)
        imgs = {}
        for order, (l, r) in (("1", (ia, ib)), ("2", (ib, ia))):
            imgs[order] = save_png(two_up(l, r, a.cell), wd / "pairs" / ("%s-order%s.png" % (pid, order)))
        row = {"pair": pid, "a": {"file": fa, "sha256": ha}, "b": {"file": fb, "sha256": hb},
               "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "images": imgs, "at": now()}
        if not any(r.get("pair") == pid for r in jl_read(wd / "pairs.jsonl")):
            jl_add(wd / "pairs.jsonl", row)
        return out({"pair": pid, "images": imgs,
                    "instructions": "judge each image in a fresh call; it shows two candidates labelled 1 and 2 with"
                                    " no file names; record the pick per order with: compare record %s <order> 1|2|tie" % pid})
    if a.action == "record":
        if len(a.args) != 3:
            raise Fail("compare record PAIR ORDER PICK")
        pid, order, pick = a.args
        pairs = {r["pair"]: r for r in jl_read(wd / "pairs.jsonl")}
        if pid not in pairs:
            raise Fail("unknown pair %s (run compare prepare first)" % pid)
        if order not in ("1", "2") or pick not in ("1", "2", "tie"):
            raise Fail("ORDER is 1 or 2, PICK is 1, 2 or tie")
        p = pairs[pid]
        side = None if pick == "tie" else p["orders"][order][int(pick) - 1]
        jl_add(wd / "matches.jsonl", {"pair": pid, "order": order, "pick": pick, "winner": side,
                                      "winner_sha256": p[side]["sha256"] if side else None,
                                      "confidence": a.confidence, "criteria": a.criteria, "judge": a.judge, "at": now()})
        return out({"pair": pid, "resolved": resolve(pid, wd)})
    raise Fail("compare prepare|record")


def resolve(pid, wd):
    ms = [m for m in jl_read(wd / "matches.jsonl") if m["pair"] == pid]
    by = {}
    for m in ms:
        by.setdefault(m["order"], []).append(m["winner"])
    if "1" not in by or "2" not in by:
        return {"status": "waiting", "need_order": "2" if "1" in by else "1"}
    w1, w2 = by["1"][0], by["2"][0]
    if w1 == w2:
        return {"status": "tie" if w1 is None else "decided", "winner": w1, "flipped": False}
    extra = [w for w in (by["1"][1:] + by["2"][1:]) if w]
    if extra and extra[0] in (w1, w2):
        return {"status": "decided", "winner": extra[0], "flipped": True, "tiebreak": True}
    return {"status": "tie", "winner": None, "flipped": w1 is not None and w2 is not None,
            "flag": "orders disagree: show a human"}


def bradley_terry(ids, games, iters=500):
    """games: (i, j, score_i) with score 1, 0 or 0.5. One virtual tie against an average player keeps it finite."""
    p = {i: 1.0 for i in ids}
    wins = {i: 0.5 for i in ids}
    for i, j, s in games:
        wins[i] += s
        wins[j] += 1 - s
    for _ in range(iters):
        new = {}
        for i in ids:
            den = 1.0 / (p[i] + 1.0)
            for x, y, _s in games:
                if x == i or y == i:
                    den += 1.0 / (p[x] + p[y])
            new[i] = wins[i] / den
        g = math.exp(sum(math.log(v) for v in new.values()) / len(new))
        new = {i: v / g for i, v in new.items()}
        if max(abs(new[i] - p[i]) for i in ids) < 1e-9:
            p = new
            break
        p = new
    return p


def cmd_rank(a):
    wd = Path(a.work)
    pairs = jl_read(wd / "pairs.jsonl")
    if not pairs:
        raise Fail("no pairs in %s (run compare prepare)" % wd)
    files = {}
    for p in pairs:
        for k in ("a", "b"):
            files[p[k]["sha256"]] = p[k]["file"]
    ids = sorted(files)
    games, rec, ties = [], {i: [0, 0, 0] for i in ids}, []
    met, beat = set(), {}
    for p in pairs:
        r = resolve(p["pair"], wd)
        A, B = p["a"]["sha256"], p["b"]["sha256"]
        if r["status"] == "waiting":
            continue
        met.add(frozenset((A, B)))
        if r["status"] == "tie":
            games.append((A, B, 0.5))
            rec[A][2] += 1
            rec[B][2] += 1
            ties.append({"pair": p["pair"], "files": [files[A], files[B]], "reason": r.get("flag", "tie")})
        else:
            win = A if r["winner"] == "a" else B
            lose = B if win == A else A
            games.append((win, lose, 1.0))
            beat[(win, lose)] = True
            rec[win][0] += 1
            rec[lose][1] += 1
    st = bradley_terry(ids, games)
    order = sorted(ids, key=lambda i: -st[i])
    rows = []
    for k, i in enumerate(order):
        nxt = order[k + 1] if k + 1 < len(order) else None
        overlap = None
        if nxt:
            direct = frozenset((i, nxt)) in met
            overlap = (st[i] / st[nxt] < 1.5) or not direct
        rows.append({"rank": k + 1, "file": files[i], "sha256": i, "strength": round(st[i], 3),
                     "wins": rec[i][0], "losses": rec[i][1], "ties": rec[i][2], "close_to_next": overlap})
    # A beat B, B beat C, C beat A: no order among the three holds, whatever the strengths say (Huyen, AI Engineering)
    pos = {i: k for k, i in enumerate(order)}
    cycles = []
    for x, y, z in itertools.combinations(order, 3):
        for c in ((x, y, z), (x, z, y)):
            if beat.get((c[0], c[1])) and beat.get((c[1], c[2])) and beat.get((c[2], c[0])):
                cycles.append(c)
    for c in cycles:
        for k in range(min(pos[i] for i in c), max(pos[i] for i in c)):
            rows[k]["close_to_next"] = True
    res = {"ranking": rows, "games": len(games), "abstained": ties,
           "cycles": [{"files": [files[i] for i in c], "ranks": sorted(pos[i] + 1 for i in c)} for c in cycles[:20]],
           "cycle_count": len(cycles), "top_in_cycle": any(pos[i] == 0 for c in cycles for i in c),
           "note": "close_to_next: strengths within 1.5x, never compared directly, or inside a cycle (A beat B, B beat"
                   " C, C beat A); do not claim an order there. top_in_cycle: the winner is close, say so"}
    if a.next:
        sug, used = [], set()
        for k, i in enumerate(order):
            if i in used:
                continue
            for j in order[k + 1:]:
                if j not in used and frozenset((i, j)) not in met:
                    sug.append([files[i], files[j]])
                    used |= {i, j}
                    break
            if len(sug) >= a.next:
                break
        res["next_pairs"] = sug
    if a.write:
        vp = wd / "verdict.json"
        v = json.loads(vp.read_text(encoding="utf-8")) if vp.is_file() else new_verdict("pairwise", "", wd)
        base = wd.parent
        v["ranking"] = [{"file": rel_to(r["file"], base), "rank": r["rank"], "strength": r["strength"],
                         "wins": r["wins"], "losses": r["losses"], "ties": r["ties"],
                         "close_to_next": r["close_to_next"]} for r in rows]
        v["abstained"] = [{"files": [rel_to(f, base) for f in t["files"]], "reason": t["reason"]} for t in ties]
        v["updated"] = now()
        write_json(vp, v)
        res["verdict"] = str(vp)
    return out(res)


def rel_to(f, base):
    try:
        return Path(f).resolve().relative_to(Path(base).resolve()).as_posix()
    except ValueError:
        return Path(f).as_posix()


# ----- cache and calibration

def cache_key(a, sha):
    """Sampling settings are part of the judge; added only when given, so keys written without them still match."""
    parts = [sha, a.rubric, str(a.rubric_version), a.model or "-", str(a.prompt_version)]
    if a.temperature is not None:
        parts.append("t=%g" % a.temperature)
    if a.seed is not None:
        parts.append("s=%d" % a.seed)
    return "|".join(parts)


def cmd_cache(a):
    store = home() / "verdicts.jsonl"
    labels = home() / "calibration" / "labels.jsonl"
    if a.action in ("get", "put"):
        if not a.args:
            raise Fail("cache %s IMG ..." % a.action)
        sha = sha256(a.args[0])
        key = cache_key(a, sha)
        if a.action == "get":
            hits = [r for r in jl_read(store) if r.get("key") == key]
            return out({"hit": bool(hits), "key": key, "entry": hits[-1] if hits else None})
        try:
            verdict = json.loads(a.verdict) if a.verdict else None
        except ValueError:
            verdict = {"text": a.verdict}
        row = {"key": key, "sha256": sha, "file": a.args[0], "rubric": a.rubric, "rubric_version": a.rubric_version,
               "model": a.model, "prompt_version": a.prompt_version, "temperature": a.temperature, "seed": a.seed,
               "verdict": verdict, "at": now()}
        jl_add(store, row)
        return out({"stored": key, "store": str(store)})
    if a.action == "stats":
        rows = jl_read(store)
        return out({"store": str(store), "entries": len(rows), "labels": len(jl_read(labels)),
                    "rubrics": sorted(set("%s@%s" % (r.get("rubric"), r.get("rubric_version")) for r in rows))})
    if a.action == "label":
        if len(a.args) != 3 or a.args[2] not in ("a", "b", "tie"):
            raise Fail("cache label A B a|b|tie  (the human's pick)")
        fa, fb, pick = a.args
        row = {"a": {"file": fa, "sha256": sha256(fa)}, "b": {"file": fb, "sha256": sha256(fb)}, "pick": pick,
               "by": "human", "shown_first": a.shown_first, "note": a.note, "at": now()}
        jl_add(labels, row)
        return out({"stored": str(labels), "labels": len(jl_read(labels))})
    if a.action == "agreement":
        return out(agreement([Path(w) for w in (a.args or [a.work])], labels))
    raise Fail("cache get|put|stats|label|agreement")


def agreement(works, labels_path):
    both = agree = 0
    noise_n = noise_d = 0
    resolved = {}
    for wd in works:
        pairs = {p["pair"]: p for p in jl_read(wd / "pairs.jsonl")}
        ms = jl_read(wd / "matches.jsonl")
        by = {}
        for m in ms:
            by.setdefault(m["pair"], {}).setdefault(m["order"], []).append(m["winner"])
        for pid, orders in by.items():
            for picks in orders.values():
                if len(picks) > 1:
                    noise_n += len(picks) - 1
                    noise_d += sum(1 for x in picks[1:] if x != picks[0])
            if "1" in orders and "2" in orders:
                both += 1
                agree += orders["1"][0] == orders["2"][0]
            if pid in pairs:
                r = resolve(pid, wd)
                p = pairs[pid]
                if r["status"] != "waiting":
                    win = None if r["status"] == "tie" else p[r["winner"]]["sha256"]
                    resolved[frozenset((p["a"]["sha256"], p["b"]["sha256"]))] = win
    hit = right = first_n = first_d = 0
    for l in jl_read(labels_path):
        if l.get("shown_first") in ("a", "b") and l["pick"] != "tie":
            first_d += 1
            first_n += l["pick"] == l["shown_first"]
        k = frozenset((l["a"]["sha256"], l["b"]["sha256"]))
        if k in resolved:
            hit += 1
            human = None if l["pick"] == "tie" else l[l["pick"]]["sha256"]
            right += resolved[k] == human
    return {"pairs_both_orders": both,
            "both_orders_agreement": round(agree / both, 3) if both else None, "target": 0.8,
            "labelled_pairs_judged": hit, "accuracy_vs_labels": round(right / hit, 3) if hit else None,
            "requery_disagreement": round(noise_d / noise_n, 3) if noise_n else None,
            "labels_with_order": first_d, "labels_first_shown_share": round(first_n / first_d, 3) if first_d else None,
            "note": "recompute whenever the judge model changes; below 0.8 both-orders agreement, show ties to a human"}


# ----- verdict contract

def new_verdict(kind, brief, wd):
    return {"artwright": "1", "kind": kind, "brief": brief, "rubric": {"id": "artwright-judge", "version": "3"},
            "judge": {"model": None, "prompt_version": "1"}, "created": now(), "status": "draft",
            "items": [], "ranking": [], "fit": [], "fixes": [], "abstained": [], "notes": ""}


def validate_verdict(v, base):
    probs = []
    for k in ("artwright", "kind", "rubric", "judge", "items", "status"):
        if k not in v:
            probs.append("missing %s" % k)
    if v.get("kind") not in KINDS:
        probs.append("kind must be one of %s" % ", ".join(KINDS))
    if v.get("status") not in ("draft", "final"):
        probs.append("status is draft or final")
    ids = set()
    for it in v.get("items", []):
        f = it.get("file", "")
        ids.add(it.get("id"))
        if not it.get("id") or not f:
            probs.append("item without id or file")
            continue
        if re.match(r"^([a-zA-Z]:|/|\\)", f) or "\\" in f:
            probs.append("item %s: paths are relative with forward slashes" % it["id"])
        fp = base / f
        if it.get("sha256") and fp.is_file() and sha256(fp) != it["sha256"]:
            probs.append("item %s: file changed since the verdict (sha256 differs)" % it["id"])
        if not fp.is_file():
            probs.append("item %s: %s not found" % (it["id"], f))
    for fit in v.get("fit", []):
        if fit.get("verdict") not in VERDICTS:
            probs.append("fit verdict must be one of %s" % ", ".join(VERDICTS))
        if fit.get("id") not in ids:
            probs.append("fit refers to unknown id %s" % fit.get("id"))
        if fit.get("verdict") == "DOES NOT FIT" and not fit.get("hard_fails"):
            probs.append("DOES NOT FIT needs hard_fails")
    for fx in v.get("fixes", []):
        if fx.get("channel") not in CHANNELS:
            probs.append("fix channel must be one of %s" % ", ".join(CHANNELS))
    for r in v.get("ranking", []):
        if "rank" not in r:
            probs.append("ranking row without rank")
    if v.get("score") is not None and not v.get("score_anchors"):
        probs.append("an absolute score needs score_anchors (three labelled references)")
    return probs


def cmd_verdict(a):
    d = Path(a.dir)
    wd = d if d.name == "artwright" else d / "artwright"
    vp = wd / "verdict.json"
    if a.action == "init":
        wd.mkdir(parents=True, exist_ok=True)
        v = json.loads(vp.read_text(encoding="utf-8")) if vp.is_file() else new_verdict(a.kind, a.brief or "", wd)
        if a.brief:
            v["brief"] = a.brief
        base = wd.parent
        known = {i["file"] for i in v["items"]}
        for k, f in enumerate(inputs(a.images or [])):
            r = rel_to(f, base)
            if r not in known:
                v["items"].append({"id": letters(len(v["items"])), "file": r, "sha256": sha256(f)})
        write_json(vp, v)
        return out({"verdict": str(vp), "items": v["items"]})
    if a.action == "validate":
        if not vp.is_file():
            raise Fail("no %s" % vp)
        try:
            v = json.loads(vp.read_text(encoding="utf-8"))
        except ValueError as e:
            raise Fail("verdict.json is not JSON: %s" % e)
        probs = validate_verdict(v, wd.parent)
        return out({"verdict": str(vp), "valid": not probs, "problems": probs}, 0 if not probs else 1)
    raise Fail("verdict init|validate")


# ----- degrade

LAB_KINDS = ("warm-shadows", "glow-shadows", "uniform-sat", "midgrey", "haze-off")
DEGRADE_KINDS = ("saturate", "crush", "crop", "jpeg", "orphans", "mixels", "blur") + LAB_KINDS + ("hotspot", "tangent",
                                                                                                  "noise", "band", "alias")

def cmd_degrade(a):
    img = load(a.image)
    rnd = random.Random(a.seed)
    w, h = img.w, img.h
    o = img.copy()
    d = o.d
    k = a.kind
    if k == "saturate":
        for i in range(0, len(d), 4):
            hh, ss, vv = colorsys.rgb_to_hsv(d[i] / 255, d[i + 1] / 255, d[i + 2] / 255)
            r, g, b = colorsys.hsv_to_rgb(hh, min(1, ss * 1.9 + 0.1), min(1, vv * 1.15))
            d[i], d[i + 1], d[i + 2] = int(r * 255), int(g * 255), int(b * 255)
    elif k == "crush":
        for i in range(0, len(d), 4):
            for c in range(3):
                v = d[i + c]
                d[i + c] = 96 + (v - 96) // 3 if v > 96 else 96 - (96 - v) // 3
    elif k == "crop":
        cw, ch = int(w * 0.55), int(h * 0.55)
        o = resize_nearest(crop(img, w - cw, h - ch, cw, ch), w, h)
    elif k == "jpeg":
        for by in range(0, h, 8):
            for bx in range(0, w, 8):
                cells = [(x, y) for y in range(by, min(h, by + 8)) for x in range(bx, min(w, bx + 8))]
                mean = [sum(img.px(x, y)[c] for x, y in cells) // len(cells) for c in range(3)]
                for x, y in cells:
                    p = img.px(x, y)
                    o.put(x, y, tuple((mean[c] * 3 + p[c]) // 4 // 24 * 24 for c in range(3)) + (p[3],))
    elif k == "orphans":
        cols = list({img.px(rnd.randrange(w), rnd.randrange(h)) for _ in range(64)})
        for _ in range(max(8, w * h // 400)):
            x, y = rnd.randrange(w), rnd.randrange(h)
            if img.px(x, y)[3]:
                o.put(x, y, rnd.choice(cols)[:3] + (255,))
    elif k == "mixels":
        bw, bh = max(2, w // 3), max(2, h // 3)
        x0, y0 = rnd.randrange(0, max(1, w - bw)), rnd.randrange(0, max(1, h - bh))
        part = crop(img, x0, y0, bw, bh)
        part = resize_nearest(resize_box(part, max(1, bw // 3), max(1, bh // 3)), bw, bh)
        paste(o, part, x0, y0)
    elif k == "blur":
        for y in range(h):
            for x in range(w):
                acc, n = [0, 0, 0, 0], 0
                for yy in range(max(0, y - 2), min(h, y + 3)):
                    for xx in range(max(0, x - 2), min(w, x + 3)):
                        p = img.px(xx, yy)
                        for c in range(4):
                            acc[c] += p[c]
                        n += 1
                o.put(x, y, tuple(v // n for v in acc))
    elif k in LAB_KINDS:
        px = [lab(c) for c in zip(d[0::4], d[1::4], d[2::4])]
        if k in ("warm-shadows", "glow-shadows"):
            t, li, _, _ = light_split(px)
            la, lb = sum(p[1] for p in li) / len(li), sum(p[2] for p in li) / len(li)
        if k == "uniform-sat":
            mc = med([chroma(p) for p in px])
        if k == "haze-off":
            far, near = px[:h // 3 * w], px[(h - h // 3) * w:]
            fm, fs = mean_sd([p[0] for p in far])
            gl = max(1.3, mean_sd([p[0] for p in near])[1] / (fs or 1))
            gc = max(1.3, med([chroma(p) for p in near]) / (med([chroma(p) for p in far]) or 1))
        for i, (L, A, B) in enumerate(px):
            if k == "warm-shadows" and L <= t:
                A, B = la, lb
            elif k == "glow-shadows" and L <= t:
                A, B = A * 3, B * 3
            elif k == "uniform-sat" and chroma((L, A, B)) > 1:
                f = mc / chroma((L, A, B))
                A, B = A * f, B * f
            elif k == "midgrey":
                L = 50 + (L - 50) * 0.35
            elif k == "haze-off" and i < h // 3 * w:
                L, A, B = fm + (L - fm) * gl, A * gc, B * gc
            d[i * 4:i * 4 + 3] = bytes(lab_rgb(L, A, B))
    elif k == "hotspot":
        side, sz = rnd.randrange(4), max(3, min(w, h) // 25)
        u = rnd.randrange(min(w, h) // 5, min(w, h) * 4 // 5)
        x, y = [(u, min(w, h) // 25), (u, h - min(w, h) // 25 - sz), (min(w, h) // 25, u), (w - min(w, h) // 25 - sz, u)][side]
        for yy in range(y, y + sz):
            for xx in range(x, x + sz):
                o.put(xx, yy, (255, 255, 255))
    elif k == "noise":  # Gaussian grain, SD --amount (default 8) on each channel
        sg = 8.0 if a.amount is None else a.amount
        for i in range(0, len(d), 4):
            for c in range(3):
                d[i + c] = max(0, min(255, int(round(d[i + c] + rnd.gauss(0, sg)))))
    elif k == "band":  # false contours: L* posterised to --amount levels (default 16)
        lv = int(a.amount or 16)
        q = 100 / lv
        for i in range(0, len(d), 4):
            L, A, B = lab(d[i:i + 3])
            d[i:i + 3] = bytes(lab_rgb(min(100, (int(L / q) + 0.5) * q), A, B))
    elif k == "alias":  # nearest shrink by 2.7 and back: fine detail turns to false pattern (no whole factor)
        o = resize_nearest(resize_nearest(img, max(1, int(w / 2.7)), max(1, int(h / 2.7))), w, h)
    elif k == "tangent":
        side, ink = rnd.randrange(4), (255, 255, 255) if sum(d[0::4]) < 128 * w * h else (0, 0, 0)
        th, ins = max(2, min(w, h) // 120), max(2, min(w, h) // 80)
        span = range(w // 4, w * 3 // 4) if side < 2 else range(h // 4, h * 3 // 4)
        for t_ in span:
            for k_ in range(ins, ins + th):
                x, y = [(t_, k_), (t_, h - 1 - k_), (k_, t_), (w - 1 - k_, t_)][side]
                o.put(x, y, ink)
    else:
        raise Fail("unknown kind")
    save_png(o, a.out)
    return out({"out": a.out, "kind": k, "seed": a.seed, "size": [o.w, o.h]})


# ---------------------------------------------------------------- CLI

def build():
    ap = argparse.ArgumentParser(prog="aw.py", description=__doc__.split("\n")[0])
    ap.add_argument("--version", action="version", version=VERSION)
    sp = ap.add_subparsers(dest="cmd")
    p = sp.add_parser("doctor")
    p.add_argument("--probe", action="store_true")
    p = sp.add_parser("info")
    p.add_argument("images", nargs="+")
    p = sp.add_parser("fit")
    p.add_argument("image")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--long", type=int)
    p.add_argument("--tokens", type=int)
    p.add_argument("--crop")
    p.add_argument("--cell")
    p.add_argument("--pixel", action="store_true", help="nearest neighbour, integer upscale")
    p = sp.add_parser("sheet")
    p.add_argument("images", nargs="+")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--cols", type=int)
    p.add_argument("--cell", type=int, default=384)
    p.add_argument("--pixel", action="store_true")
    p.add_argument("--no-labels", action="store_true")
    p.add_argument("--bg", default="119,119,119", help="R,G,B behind the cells (neutral grey, L* 50; white skews colour)")
    p = sp.add_parser("stats")
    p.add_argument("image")
    p.add_argument("--edge", type=int, default=256)
    p.add_argument("--notan")
    for name in ("light", "gamut", "accents", "depth", "comp"):
        p = sp.add_parser(name)
        p.add_argument("image")
        p.add_argument("--edge", type=int, default=256)
    sp.choices["light"].add_argument("--box", help="x,y,w,h fractions: one surface")
    sp.choices["gamut"].add_argument("--overlay", help="PNG of the a*b* plane with the hull")
    sp.choices["depth"].add_argument("--depth", help="depth map image (bright = near, as Depth Anything writes)")
    sp.choices["depth"].add_argument("--far-bright", action="store_true", help="the map is bright far (a Mist pass)")
    sp.choices["comp"].add_argument("--subject", help="x,y,w,h fractions: the intended subject")
    sp.choices["comp"].add_argument("--text-band", action="append",
                                    help="x,y,w,h fractions where text will sit (repeatable): edge and contrast pull")
    sp.choices["comp"].add_argument("--out", help="folder for masses3.png and masses4.png")
    p = sp.add_parser("palette")
    p.add_argument("image")
    p.add_argument("-k", type=int, default=8)
    p.add_argument("--against")
    p = sp.add_parser("pixel")
    p.add_argument("images", nargs="+")
    p.add_argument("--budget", type=int)
    p.add_argument("--palette")
    p.add_argument("--scale", type=int)
    p.add_argument("--tol", type=int, default=24)
    p.add_argument("--tile", action="store_true")
    p.add_argument("--frames", action="store_true")
    p.add_argument("--preview")
    p.add_argument("--zoom", type=int, default=4)
    p = sp.add_parser("hash")
    p.add_argument("images", nargs="+")
    p = sp.add_parser("dedupe")
    p.add_argument("images", nargs="+")
    p.add_argument("--threshold", type=int, default=6)
    p = sp.add_parser("compare")
    p.add_argument("action", choices=["prepare", "record"])
    p.add_argument("args", nargs="*")
    p.add_argument("--work", default="artwright")
    p.add_argument("--cell", type=int, default=768)
    p.add_argument("--confidence", choices=["low", "medium", "high"])
    p.add_argument("--criteria", nargs="*")
    p.add_argument("--judge")
    p = sp.add_parser("rank")
    p.add_argument("--work", default="artwright")
    p.add_argument("--next", type=int, default=0)
    p.add_argument("--write", action="store_true")
    p = sp.add_parser("cache")
    p.add_argument("action", choices=["get", "put", "stats", "label", "agreement"])
    p.add_argument("args", nargs="*")
    p.add_argument("--rubric", default="artwright-judge")
    p.add_argument("--rubric-version", default="3")
    p.add_argument("--model")
    p.add_argument("--prompt-version", default="1")
    p.add_argument("--temperature", type=float)
    p.add_argument("--seed", type=int)
    p.add_argument("--shown-first", choices=["a", "b"])
    p.add_argument("--verdict")
    p.add_argument("--note")
    p.add_argument("--work", default="artwright")
    p = sp.add_parser("verdict")
    p.add_argument("action", choices=["init", "validate"])
    p.add_argument("dir")
    p.add_argument("images", nargs="*")
    p.add_argument("--kind", choices=KINDS, default="pairwise")
    p.add_argument("--brief")
    p = sp.add_parser("degrade")
    p.add_argument("image")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--kind", required=True, choices=DEGRADE_KINDS)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--amount", type=float, help="noise: SD (8); band: levels (16)")
    p = sp.add_parser("geomgate")
    p.add_argument("render_dir")
    p.add_argument("painted")
    p.add_argument("--part", help="the ring in sprite.json to check (default: the only one)")
    p.add_argument("--spokes", type=int, default=0, help="arm count when sprite.json gives none")
    p.add_argument("--contact", action="append", help="A:B, two ID regions that must touch (repeatable)")
    p.add_argument("--game-px", type=int, default=96, help="long edge the sprite ships at (regions gate)")
    p.add_argument("--no-edges", action="store_true", help="skip the edge precision and recall information")
    p.add_argument("--out", help="also write the report to this JSON file")
    p = sp.add_parser("sprite")
    p.add_argument("candidates", nargs="+")
    p.add_argument("--refs", nargs="+", required=True)
    p.add_argument("--pad", type=float, default=0.15)
    p.add_argument("--min-coverage", type=float, default=0.9,
                   help="fail a sprite whose opaque share is under this times the references' median (0: off)")
    p.add_argument("--out")
    p = sp.add_parser("setfit")
    p.add_argument("candidates", nargs="+")
    p.add_argument("--refs", nargs="+", required=True, help="the series: files or folders, comma-separated or spaced")
    p.add_argument("--treat", help="external command with {in} and {out}, e.g. 'python treat.py {in} {out}'")
    p.add_argument("--treated-out", help="folder for the candidates' treated images")
    p.add_argument("--widen", type=float, default=0.3, help="widen the references' range by this share of it, each side")
    p.add_argument("--width", type=int, default=960, help="width the texture measures read at")
    p.add_argument("--out")
    return ap


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = build()
    a = ap.parse_args(argv)
    if not a.cmd:
        return out({"commands": sorted(ap._subparsers._group_actions[0].choices), "help": "aw.py <command> -h"})
    try:
        return globals()["cmd_" + a.cmd](a)
    except Fail as e:
        return out({"ok": False, "error": str(e)}, 1)
    except (OSError, ValueError, zlib.error, struct.error) as e:
        return out({"ok": False, "error": "%s: %s" % (type(e).__name__, e)}, 1)


# light, colour and composition measures live in aw_measure.py (kept apart so each file stays under 100 KB)
sys.modules.setdefault("aw", sys.modules[__name__])
from aw_measure import *  # noqa: E402,F401,F403
from aw_geom import cmd_geomgate, cmd_setfit, cmd_sprite  # noqa: E402,F401


if __name__ == "__main__":
    sys.exit(main())
