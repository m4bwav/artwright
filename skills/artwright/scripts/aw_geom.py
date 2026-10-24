"""aw_geom.py: render-then-paint and painted-sprite gates for aw.py (geomgate, sprite).

Imported by aw.py; run them through it (`aw.py geomgate RENDER_DIR PAINTED`, `aw.py sprite CAND --refs DIR`).
Standard library only (Pillow, when present, does the resizes). The render directory contract is in
../references/sprite-json.md. Both gates describe and compare; neither is a beauty score.

geomgate compares a painting to the 3D render it was painted over. The render's projected rim of a ring part is
the truth: along each ray from the centre through it, the painting's edge profile is cross-correlated with the
render's (a max-gradient search wanders between the inner and outer rim edges and float tips; L-008). Spokes are
the angular light and dark profile at fixed wheel-plane angles. A new object inside a region shows as a tone-fitted
residual outlier at game size; edge precision cannot tell it from brush texture and is information only (L-009).

sprite measures a painted game sprite at its native size on its opaque pixels only and checks each measure against
a reference set's range widened by 15%. It never posterizes: painted sprites are not pixel art.
"""

import json
import math

from aw import Fail, Img, Path, inputs, lab, load, out, resize_box, resize_nearest, _pillow

TOL = {"centre_frac": 0.06, "axis_frac": 0.08, "tilt_deg": 8.0, "rim_coverage": 0.8, "rim_rms_frac": 0.05,
       "spoke_corr": 0.6, "region_anomaly": 5.0}


# ---------------------------------------------------------------- small numeric helpers (no numpy)

def _mean(v):
    return sum(v) / len(v) if v else 0.0


def _std(v):
    m = _mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / len(v)) if v else 0.0


def _pctl(v, q):
    """numpy.percentile with linear interpolation."""
    s = sorted(v)
    if not s:
        return 0.0
    k = (len(s) - 1) * q / 100.0
    f = int(math.floor(k))
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def _median(v):
    return _pctl(v, 50)


def _corr(a, b):
    ma, mb = _mean(a), _mean(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a)
    sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb) if saa > 0 and sbb > 0 else 0.0


def _rfft_mag(v):
    n = len(v)
    cs = [math.cos(2 * math.pi * k / n) for k in range(n)]
    sn = [math.sin(2 * math.pi * k / n) for k in range(n)]
    res = []
    for f in range(n // 2 + 1):
        re = im = 0.0
        for t, x in enumerate(v):
            j = (f * t) % n
            re += x * cs[j]
            im -= x * sn[j]
        res.append(math.hypot(re, im))
    return res


def _inv3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    if abs(det) < 1e-300:
        raise ValueError("singular matrix")
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


def _mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _eig3_real(m):
    """Real eigenpairs of a 3x3 matrix: roots of the characteristic cubic, vectors from row cross products."""
    tr = m[0][0] + m[1][1] + m[2][2]
    mn = (m[0][0] * m[1][1] - m[0][1] * m[1][0] + m[0][0] * m[2][2] - m[0][2] * m[2][0]
          + m[1][1] * m[2][2] - m[1][2] * m[2][1])
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    p2, p1, p0 = -tr, mn, -det
    p = p1 - p2 * p2 / 3
    q = 2 * p2 ** 3 / 27 - p2 * p1 / 3 + p0
    disc = (q / 2) ** 2 + (p / 3) ** 3
    if disc > 0:
        sd = math.sqrt(disc)
        cb = lambda x: math.copysign(abs(x) ** (1 / 3), x)
        roots = [cb(-q / 2 + sd) + cb(-q / 2 - sd)]
    else:
        r = math.sqrt(max(0.0, -p / 3))
        if r < 1e-300:
            roots = [0.0]
        else:
            phi = math.acos(max(-1.0, min(1.0, -q / (2 * r ** 3))))
            roots = [2 * r * math.cos((phi - 2 * math.pi * k) / 3) for k in range(3)]
    pairs = []
    for t in roots:
        lam = t - p2 / 3
        a = [[m[i][j] - (lam if i == j else 0) for j in range(3)] for i in range(3)]
        best, bn = None, -1.0
        for i, j in ((0, 1), (0, 2), (1, 2)):
            u, v = a[i], a[j]
            c = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
            n = math.sqrt(sum(x * x for x in c))
            if n > bn:
                best, bn = c, n
        if bn > 0:
            pairs.append((lam, [x / bn for x in best]))
    return pairs


def fit_ellipse(xs, ys):
    """Direct least-squares ellipse (Fitzgibbon, in Halir and Flusser's stable form); returns centre, semi-axes
    (major, minor) and tilt in degrees, as the prototype's numpy version did."""
    mx, my = _mean(xs), _mean(ys)
    sc = max(1e-9, max(max(abs(x - mx) for x in xs), max(abs(y - my) for y in ys)))
    X = [(x - mx) / sc for x in xs]
    Y = [(y - my) / sc for y in ys]
    D1 = [(x * x, x * y, y * y) for x, y in zip(X, Y)]
    D2 = [(x, y, 1.0) for x, y in zip(X, Y)]
    S1 = [[sum(r[i] * r[j] for r in D1) for j in range(3)] for i in range(3)]
    S2 = [[sum(r[i] * s[j] for r, s in zip(D1, D2)) for j in range(3)] for i in range(3)]
    S3 = [[sum(r[i] * r[j] for r in D2) for j in range(3)] for i in range(3)]
    T = [[-v for v in row] for row in _mm(_inv3(S3), [list(r) for r in zip(*S2)])]
    M = [[S1[i][j] + v for j, v in enumerate(row)] for i, row in enumerate(_mm(S2, T))]
    M = [[v / 2 for v in M[2]], [-v for v in M[1]], [v / 2 for v in M[0]]]
    cands = [(4 * v[0] * v[2] - v[1] ** 2, v) for _, v in _eig3_real(M)]
    cands = [c for c in cands if c[0] > 0]
    if not cands:
        raise ValueError("no ellipse fits these points")
    a1 = max(cands)[1]
    a2 = [sum(T[i][k] * a1[k] for k in range(3)) for i in range(3)]
    a, b, c = a1
    d, e, f = a2
    den = b * b - 4 * a * c
    x0 = (2 * c * d - b * e) / den
    y0 = (2 * a * e - b * d) / den
    num = 2 * (a * e * e + c * d * d - b * d * e + den * f)
    s = math.sqrt((a - c) ** 2 + b * b)
    ax1 = -math.sqrt(abs(num * (a + c + s))) / den
    ax2 = -math.sqrt(abs(num * (a + c - s))) / den
    tilt = 0.5 * math.degrees(math.atan2(-b, c - a))
    maj, mnr = (abs(ax1), abs(ax2)) if abs(ax1) >= abs(ax2) else (abs(ax2), abs(ax1))
    if abs(ax2) > abs(ax1):
        tilt += 90
    tilt = (tilt + 90) % 180 - 90
    return (x0 * sc + mx, y0 * sc + my), (maj * sc, mnr * sc), tilt


# ---------------------------------------------------------------- images as lazily sampled grids

def resize(img, w, h, filt="lanczos"):
    """RGBA resize: Pillow (premultiplied, Lanczos or bilinear) when present, else area average or nearest."""
    if (img.w, img.h) == (w, h):
        return img
    Image, _ = _pillow()
    if Image is not None:
        im = Image.frombytes("RGBA", (img.w, img.h), bytes(img.d))
        f = Image.LANCZOS if filt == "lanczos" else Image.BILINEAR
        r = im.resize((w, h), f)
        return Img(w, h, bytearray(r.tobytes()))
    if w <= img.w and h <= img.h:
        return resize_box(img, w, h)
    return resize_nearest(img, w, h)


def _refl(i, n):
    while i < 0 or i >= n:
        i = -i - 1 if i < 0 else 2 * n - i - 1
    return i


def _bilinear(fn, w, h, x, y):
    """map_coordinates(order=1, mode='constant') on a grid given as fn(ix, iy)."""
    if x < 0 or y < 0 or x > w - 1 or y > h - 1:
        return 0.0
    x0, y0 = int(x), int(y)
    x1, y1 = min(x0 + 1, w - 1), min(y0 + 1, h - 1)
    fx, fy = x - x0, y - y0
    return ((fn(x0, y0) * (1 - fx) + fn(x1, y0) * fx) * (1 - fy) + (fn(x0, y1) * (1 - fx) + fn(x1, y1) * fx) * fy)


def _luma601(d, i):
    return (0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]) / 255.0


class Grad:
    """Gradient magnitude of the luma composited on white: Gaussian (sigma, truncate 4), then Sobel, both with
    scipy's reflect border. Computed only where sampled, so a 1024 px render costs what its rim band costs."""

    def __init__(self, img, sigma=1.0):
        self.d, self.w, self.h = img.d, img.w, img.h
        r = int(4.0 * sigma + 0.5)
        k = [math.exp(-0.5 * (i / sigma) ** 2) for i in range(-r, r + 1)]
        t = sum(k)
        self.k, self.r = [v / t for v in k], r
        self.hc, self.bc, self.gc = {}, {}, {}

    def lum(self, x, y):
        i = (y * self.w + x) * 4
        a = self.d[i + 3] / 255.0
        return _luma601(self.d, i) * a + 1 - a

    def hb(self, x, y):
        key = y * self.w + x
        v = self.hc.get(key)
        if v is None:
            w, r = self.w, self.r
            v = sum(kk * self.lum(_refl(x + j - r, w), y) for j, kk in enumerate(self.k))
            self.hc[key] = v
        return v

    def b(self, x, y):
        x, y = _refl(x, self.w), _refl(y, self.h)
        key = y * self.w + x
        v = self.bc.get(key)
        if v is None:
            h, r = self.h, self.r
            v = sum(kk * self.hb(x, _refl(y + j - r, h)) for j, kk in enumerate(self.k))
            self.bc[key] = v
        return v

    def g(self, x, y):
        key = y * self.w + x
        v = self.gc.get(key)
        if v is None:
            b = self.b
            gx = (b(x + 1, y - 1) - b(x - 1, y - 1)) + 2 * (b(x + 1, y) - b(x - 1, y)) + (b(x + 1, y + 1) - b(x - 1, y + 1))
            gy = (b(x - 1, y + 1) - b(x - 1, y - 1)) + 2 * (b(x, y + 1) - b(x, y - 1)) + (b(x + 1, y + 1) - b(x + 1, y - 1))
            v = math.hypot(gx, gy)
            self.gc[key] = v
        return v

    def at(self, x, y):
        return _bilinear(self.g, self.w, self.h, x, y)


# ---------------------------------------------------------------- the render's ID regions

def _srgb(c):
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def id_labels(idimg, colours):
    """One byte per pixel: 1 + the index of the ID colour within 0.12 (sRGB) of it, 0 elsewhere. sprite.json keeps
    the linear object colour; the ID pass is written through the sRGB transform, hence the conversion."""
    names = list(colours)
    if len(names) > 254:
        raise Fail("at most 254 ID colours")
    ref = [[_srgb(float(v)) * 255 for v in colours[n][:3]] for n in names]
    cache = {}
    d = idimg.d
    lab_ = bytearray(idimg.w * idimg.h)
    for i, px in enumerate(zip(d[0::4], d[1::4], d[2::4], d[3::4])):
        v = cache.get(px)
        if v is None:
            v = 0
            if px[3] >= 128:
                best = 30.6
                for k, c in enumerate(ref):
                    dd = max(abs(px[0] - c[0]), abs(px[1] - c[1]), abs(px[2] - c[2]))
                    if dd < best:
                        best, v = dd, k + 1
            cache[px] = v
        lab_[i] = v
    return names, bytes(lab_)


def mask_of(labels, k):
    """Bytes of 255 where the label is k (1-based), 0 elsewhere."""
    t = bytearray(256)
    t[k] = 255
    return labels.translate(bytes(t))


def _erode(m, w, h, it=1):
    """Binary erosion with the cross (scipy's default structure), border counts as background."""
    for _ in range(it):
        n = [False] * (w * h)
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                i = y * w + x
                n[i] = m[i] and m[i - 1] and m[i + 1] and m[i - w] and m[i + w]
        m = n
    return m


def _small_mask(mb, w, h, gw, gh):
    """The mask at game size, bilinear, kept where above 200 of 255 (as the prototype did)."""
    Image, _ = _pillow()
    if Image is not None:
        r = Image.frombytes("L", (w, h), mb).resize((gw, gh), Image.BILINEAR).tobytes()
        return [v > 200 for v in r]
    img = Img(w, h)
    img.d[0::4] = mb
    img.d[3::4] = b"\xff" * (w * h)
    s = resize_box(img, gw, gh) if gw <= w and gh <= h else resize_nearest(img, gw, gh)
    return [v > 200 for v in s.d[0::4]]


def _poly_fill(buf, w, h, poly):
    """Scanline fill of a polygon (render px) into a bytearray mask."""
    ys = [p[1] for p in poly]
    for y in range(max(0, int(min(ys))), min(h, int(max(ys)) + 1)):
        yc = y + 0.5
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i - 1], poly[i]
            if (y1 <= yc < y2) or (y2 <= yc < y1):
                xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            a, b = max(0, int(math.ceil(xs[j] - 0.5))), min(w - 1, int(math.floor(xs[j + 1] - 0.5)))
            if b >= a:
                buf[y * w + a:y * w + b + 1] = b"\xff" * (b - a + 1)


def _touches(ma, mb_, w, h, grow=3):
    """Does mask A grown by `grow` cross steps (a diamond) meet mask B?"""
    offs = [(dx, dy) for dx in range(-grow, grow + 1) for dy in range(-grow, grow + 1) if abs(dx) + abs(dy) <= grow]
    for i, v in enumerate(ma):
        if not v:
            continue
        x, y = i % w, i // w
        if 0 < x < w - 1 and 0 < y < h - 1 and ma[i - 1] and ma[i + 1] and ma[i - w] and ma[i + w]:
            continue
        for dx, dy in offs:
            xx, yy = x + dx, y + dy
            if 0 <= xx < w and 0 <= yy < h and mb_[yy * w + xx]:
                return True
    return False


# ---------------------------------------------------------------- gates

def ring_gate(render, paint, ring):
    """Along each ray from the centre through the projected rim, the painting's edge profile (inner rim edge,
    outer rim edge, float tips together) is cross-correlated with the render's; the best lag is how far the
    painted rim moved there. Angles where the render shows no rim (behind water) are skipped."""
    c = [float(v) for v in ring["centre_px"]]
    rim = [[float(v) for v in p] for p in ring["rim_px"]]
    tr = [math.hypot(p[0] - c[0], p[1] - c[1]) for p in rim]
    R = max(tr)
    band, step = 0.15 * R, 0.5
    max_lag = int(round(0.08 * R / step))
    offs = [-band + k * step for k in range(int(math.ceil((2 * band + step) / step)))]
    g_r, g_p = Grad(render), Grad(paint)

    def prof(g, p, r):
        u = ((p[0] - c[0]) / r, (p[1] - c[1]) / r)
        return [g.at(p[0] + u[0] * s, p[1] + u[1] * s) for s in offs]
    prof_r = [prof(g_r, p, r) for p, r in zip(rim, tr)]
    prof_p = [prof(g_p, p, r) for p, r in zip(rim, tr)]
    energy = [max(pr) for pr in prof_r]
    cut = 0.35 * _pctl(energy, 90)
    vis = [e >= cut for e in energy]
    lags, peaks = [], []
    for pr, pp in zip(prof_r, prof_p):
        ma, sa, mb, sb = _mean(pr), _std(pr), _mean(pp), _std(pp)
        a = [(v - ma) / (sa + 1e-9) for v in pr]
        b = [(v - mb) / (sb + 1e-9) for v in pp]
        n = len(a)
        best, bl = -2.0, 0
        for lag in range(-max_lag, max_lag + 1):
            if lag >= 0:
                v = sum(x * y for x, y in zip(a[lag:], b[:n - lag])) / (n - lag)
            else:
                v = sum(x * y for x, y in zip(a[:lag], b[-lag:])) / (n + lag)
            if v > best:
                best, bl = v, lag
        lags.append(bl * step)
        peaks.append(best)
    keep = [v and p >= 0.3 for v, p in zip(vis, peaks)]
    nvis = sum(vis)
    coverage = sum(keep) / max(1, nvis)
    off = [l / R for l, k in zip(lags, keep) if k]
    rms = math.sqrt(_mean([o * o for o in off])) if off else 1.0
    worst = max(abs(o) for o in off) if off else 1.0
    res = {"visible_angles": nvis, "coverage": round(coverage, 3), "rim_rms": round(rms, 4),
           "rim_worst": round(worst, 4), "radius_px": round(R, 1),
           "match_mean": round(_mean([p for p, v in zip(peaks, vis) if v]), 3)}
    ok = coverage >= TOL["rim_coverage"] and rms <= TOL["rim_rms_frac"]
    pts = [(c[0] + (p[0] - c[0]) * (r + l) / r, c[1] + (p[1] - c[1]) * (r + l) / r)
           for p, r, l, k in zip(rim, tr, lags, keep) if k]
    if len(pts) >= 12:
        c_t, ax_t, tl_t = fit_ellipse([p[0] for p in rim], [p[1] for p in rim])
        c_p, ax_p, tl_p = fit_ellipse([p[0] for p in pts], [p[1] for p in pts])
        dc = math.hypot(c_p[0] - c_t[0], c_p[1] - c_t[1]) / ax_t[0]
        da = max(abs(ax_p[0] - ax_t[0]) / ax_t[0], abs(ax_p[1] - ax_t[1]) / ax_t[1])
        dt = 0.0 if ax_t[1] / ax_t[0] > 0.9 else abs((tl_p - tl_t + 90) % 180 - 90)
        res.update(centre_off=round(dc, 4), axis_err=round(da, 4), tilt_err=round(dt, 2))
        ok = ok and dc <= TOL["centre_frac"] and da <= TOL["axis_frac"] and dt <= TOL["tilt_deg"]
    else:
        ok = False
        res["note"] = "under 12 rim angles matched: no ellipse to fit"
    res["pass"] = bool(ok)
    return res


def ring_profile(img, ring, frac=(0.4, 0.78)):
    """Luma times alpha around the ring at fixed wheel-plane angles (the rim points), averaged over radii."""
    c = [float(v) for v in ring["centre_px"]]
    rim = [[float(v) for v in p] for p in ring["rim_px"]]
    d, w, h = img.d, img.w, img.h

    def la(x, y):
        i = (y * w + x) * 4
        return _luma601(d, i) * d[i + 3] / 255.0
    radii = [frac[0] + (frac[1] - frac[0]) * k / 7 for k in range(8)]
    n, fine, prof = len(rim), 4, []
    for k in range(n * fine):
        t = k / fine
        i, f = int(t) % n, t - int(t)
        p = (rim[i][0] * (1 - f) + rim[(i + 1) % n][0] * f, rim[i][1] * (1 - f) + rim[(i + 1) % n][1] * f)
        prof.append(_mean([_bilinear(la, w, h, c[0] + (p[0] - c[0]) * s, c[1] + (p[1] - c[1]) * s) for s in radii]))
    return prof


def spokes_gate(render, paint, ring, arms):
    """The painting's light and dark around the ring follow the render's (arms where the model put them), and the
    energy at the arm count and its harmonics (the comb) keeps at least half of the render's."""
    pr, pp = ring_profile(render, ring), ring_profile(paint, ring)

    def comb(p):
        m = _mean(p)
        s = _rfft_mag([v - m for v in p])
        return sum(s[arms * hh] for hh in (1, 2, 3) if arms * hh < len(s)) / (sum(s[1:]) + 1e-9)
    corr, cr, cp = _corr(pr, pp), comb(pr), comb(pp)
    return {"arms": arms, "profile_corr": round(corr, 3), "comb_render": round(cr, 3), "comb_painted": round(cp, 3),
            "pass": bool(corr >= TOL["spoke_corr"] and cp >= 0.5 * cr)}


def _box3(v, w, h):
    """3x3 sum with reflect border (uniform_filter(size=3) * 9)."""
    res = [0.0] * (w * h)
    for y in range(h):
        rows = [_refl(y - 1, h) * w, y * w, _refl(y + 1, h) * w]
        for x in range(w):
            xs = (_refl(x - 1, w), x, _refl(x + 1, w))
            res[y * w + x] = sum(v[r + xx] for r in rows for xx in xs)
    return res


def region_anomalies(render, paint, names, labels, gw, gh):
    """At game size, fit the painting's tone to the render per region (paint = a * render + b) and find the worst
    3x3 patch of residual. A new object (a blade painted on a roof) is a patch far above the region's own paint
    noise; brush texture is not. Score = worst patch / (median residual + 0.01)."""
    sr, sp = resize(render, gw, gh), resize(paint, gw, gh)
    Lr = [_luma601(sr.d, i) for i in range(0, len(sr.d), 4)]
    Lp = [_luma601(sp.d, i) for i in range(0, len(sp.d), 4)]
    res_ = {}
    for k, name in enumerate(names, 1):
        ms = _erode(_small_mask(mask_of(labels, k), render.w, render.h, gw, gh), gw, gh)
        idx = [i for i, v in enumerate(ms) if v]
        if len(idx) < 12:
            continue
        xr, yp = [Lr[i] for i in idx], [Lp[i] for i in idx]
        mx, my = _mean(xr), _mean(yp)
        vx = sum((x - mx) ** 2 for x in xr)
        a = sum((x - mx) * (y - my) for x, y in zip(xr, yp)) / vx if vx > 1e-12 else 0.0
        b = my - a * mx
        res = [0.0] * (gw * gh)
        for i in idx:
            res[i] = abs(Lp[i] - (a * Lr[i] + b))
        cnt = _box3([1.0 if v else 0.0 for v in ms], gw, gh)
        tot = _box3(res, gw, gh)
        loc = [tot[i] / max(cnt[i], 1) if ms[i] else 0.0 for i in range(gw * gh)]
        med = _median([res[i] for i in idx])
        j = max(range(gw * gh), key=lambda i: loc[i])
        res_[name] = {"median": round(med, 4), "worst": round(loc[j], 4),
                      "score": round(loc[j] / (med + 0.01), 2), "at_game_px": [j % gw, j // gw]}
    return res_


def edges_info(render, paint, names, labels, edge=256):
    """Edge precision and recall per region at `edge` px: information only. Painted texture moves edges without
    changing a shape, so a low precision is not a failure (L-009)."""
    w, h = (edge, max(1, round(render.h * edge / render.w))) if render.w >= render.h else \
        (max(1, round(render.w * edge / render.h)), edge)
    w, h = min(w, render.w), min(h, render.h)

    def edges(img):
        g = Grad(img)
        mag = [g.g(x, y) for y in range(h) for x in range(w)]
        op = [mag[i] for i in range(w * h) if img.d[i * 4 + 3] > 127]
        thr = 0.3 * _pctl(op, 95) if op else 1.0
        e = [False] * (w * h)
        for y in range(h):
            for x in range(w):
                v = mag[y * w + x]
                if v > thr and all(mag[_refl(y + dy, h) * w + _refl(x + dx, w)] <= v
                                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                    e[y * w + x] = True
        return e
    sr, sp = resize(render, w, h), resize(paint, w, h)
    er, ep = edges(sr), edges(sp)
    tol = max(1, int(round(max(2.0, render.w / 192) * w / render.w)))

    def near(e):
        rows = [any(e[y * w + max(0, x - tol):y * w + min(w, x + tol + 1)]) for y in range(h) for x in range(w)]
        return [any(rows[yy * w + x] for yy in range(max(0, y - tol), min(h, y + tol + 1)))
                for y in range(h) for x in range(w)]
    nr, np_ = near(er), near(ep)
    res = {}
    for k, name in enumerate(names, 1):
        mm = _erode(_small_mask(mask_of(labels, k), render.w, render.h, w, h), w, h, 2)
        pe = [i for i in range(w * h) if ep[i] and mm[i]]
        re_ = [i for i in range(w * h) if er[i] and mm[i]]
        if sum(mm) < 12:
            continue
        res[name] = {"precision": round(sum(nr[i] for i in pe) / len(pe), 3) if pe else 1.0,
                     "recall": round(sum(np_[i] for i in re_) / len(re_), 3) if re_ else 1.0,
                     "paint_edges": len(pe), "render_edges": len(re_)}
    return {"measured_at": [w, h], "tol_px": tol, "scores": res,
            "note": "information only: brush texture moves edges; regions.anomaly is the gate"}


def cmd_geomgate(a):
    rd = Path(a.render_dir)
    meta_p = rd / "sprite.json"
    if not meta_p.is_file():
        raise Fail("no sprite.json in %s (contract: references/sprite-json.md)" % rd)
    meta = json.loads(meta_p.read_text(encoding="utf-8"))
    if not meta.get("id_colours"):
        raise Fail("sprite.json has no id_colours")
    idimg = load(rd / (meta.get("id_image") or "id.png"))
    render = load(rd / (meta.get("beauty_image") or "beauty.png"))
    if (render.w, render.h) != (idimg.w, idimg.h):
        raise Fail("beauty and ID images differ in size")
    paint = resize(load(a.painted), render.w, render.h)
    if min(paint.d[3::4]) >= 253:
        paint = paint.copy()
        paint.d[3::4] = render.d[3::4]
    names, labels = id_labels(idimg, meta["id_colours"])
    rings = meta.get("rings") or {}
    part = a.part or (next(iter(rings)) if len(rings) == 1 else None)
    if a.part and a.part not in rings:
        raise Fail("no ring '%s' in sprite.json (rings: %s)" % (a.part, ", ".join(rings) or "none"))
    if part is None and len(rings) > 1:
        raise Fail("several rings (%s): name one with --part" % ", ".join(rings))
    res = {"painted": a.painted, "render": str(rd), "size": [render.w, render.h], "part": part, "tol": TOL,
           "gates": {}}
    if part:
        ring = rings[part]
        if len(ring.get("rim_px") or []) < 12:
            raise Fail("rings.%s.rim_px needs at least 12 points" % part)
        res["gates"]["ellipse"] = ring_gate(render, paint, ring)
        arms = a.spokes or ring.get("arms")
        if arms:
            res["gates"]["spokes"] = spokes_gate(render, paint, ring, int(arms))
    gw = a.game_px if render.w >= render.h else max(1, round(render.w * a.game_px / render.h))
    gh = a.game_px if render.h >= render.w else max(1, round(render.h * a.game_px / render.w))
    anom = region_anomalies(render, paint, names, labels, gw, gh)
    bad = [n for n, r in anom.items() if r["score"] > TOL["region_anomaly"]]
    res["gates"]["regions"] = {"game_px": [gw, gh], "anomaly": anom, "failing": bad, "pass": not bad}
    if not a.no_edges:
        res["edges_info"] = edges_info(render, paint, names, labels)
    pairs = [c.split(":", 1) for c in a.contact] if a.contact else meta.get("contacts") or []
    contact = {}
    if pairs:
        masks = {}

        def m(name):
            if name not in names:
                raise Fail("contact names '%s', not an ID region (%s)" % (name, ", ".join(names)))
            if name not in masks:
                mb = bytearray(mask_of(labels, names.index(name) + 1))
                if name in rings:  # a ring counts with the space between its arms filled
                    _poly_fill(mb, render.w, render.h, rings[name]["rim_px"])
                masks[name] = mb
            return masks[name]
        for p in pairs:
            if len(p) != 2:
                raise Fail("a contact is two region names, A:B")
            contact["%s:%s" % tuple(p)] = _touches(m(p[0]), m(p[1]), render.w, render.h)
        res["gates"]["contact"] = {"pairs": contact, "pass": all(contact.values()),
                                   "note": "checked in the render: the model's parts meet within 3 px"}
    res["pass"] = all(g["pass"] for g in res["gates"].values())
    res["failing_gates"] = [k for k, g in res["gates"].items() if not g["pass"]]
    if not part:
        res["note"] = "no ring part in sprite.json: only the regions and contact gates ran"
    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(res, indent=1), encoding="utf-8")
        res["report"] = str(p)
    return out(res)


# ---------------------------------------------------------------- painted sprite style fit

SPRITE_KEYS = ("value_mean", "value_spread", "chroma_mean", "colours", "soft_edge_share", "texture",
               "outline_value", "coverage")


def sprite_measures(img):
    """Opaque pixels only (alpha above 200; seen above 8), at native size. Lab L* value mean and 5-95% spread,
    chroma mean, unique colours at 6 bits a channel, soft-edge share, texture (mean L* gradient inside the
    opaque area: low for flat 3D shading, high for brushwork), outline value (L* of the outer two-pixel ring)."""
    w, h, d = img.w, img.h, img.d
    n = w * h
    al = d[3::4]
    opaque = [v > 200 for v in al]
    seen = [v > 8 for v in al]
    if not any(opaque):
        raise Fail("no opaque pixels")
    cache, L, C = {}, [0.0] * n, [0.0] * n
    for i in range(n):
        if seen[i]:
            px = (d[4 * i], d[4 * i + 1], d[4 * i + 2])
            v = cache.get(px)
            if v is None:
                v = cache[px] = lab(px)
            L[i], C[i] = v[0], math.hypot(v[1], v[2])
    Lo = [L[i] for i in range(n) if opaque[i]]
    inner = _erode(opaque, w, h)
    ring = [o and not e for o, e in zip(opaque, _erode(opaque, w, h, 2))]
    g = [math.hypot((L[i + 1] - L[i - 1]) / 2, (L[i + w] - L[i - w]) / 2) for i in range(n) if inner[i]]
    q = {(d[4 * i] // 4, d[4 * i + 1] // 4, d[4 * i + 2] // 4) for i in range(n) if seen[i]}
    ns = sum(seen)
    return {"value_mean": _mean(Lo), "value_spread": _pctl(Lo, 95) - _pctl(Lo, 5),
            "chroma_mean": _mean([C[i] for i in range(n) if opaque[i]]), "colours": len(q),
            "soft_edge_share": sum(1 for v in al if 8 < v < 247) / max(1, ns),
            "texture": _mean(g), "outline_value": _mean([L[i] for i in range(n) if ring[i]]),
            "coverage": ns / n}


def cmd_sprite(a):
    cands = inputs(a.candidates)
    refs = inputs(a.refs)
    cset = {str(Path(c).resolve()) for c in cands}
    refs = [r for r in refs if str(Path(r).resolve()) not in cset]
    if len(refs) < 2:
        raise Fail("need at least two reference sprites (a candidate is never its own reference)")
    rm, sizes = {}, []
    for r in refs:
        img = load(r)
        sizes.append((img.w, img.h))
        rm[r] = sprite_measures(img)
    rng, raw = {}, {}
    for k in SPRITE_KEYS:
        v = [m[k] for m in rm.values()]
        lo, hi = min(v), max(v)
        pad = a.pad * (hi - lo)
        raw[k] = (lo - pad, hi + pad)
        rng[k] = [round(lo - pad, 3), round(hi + pad, 3), round(_median(v), 3)]
    rows = []
    for c in cands:
        img = load(c)
        m = sprite_measures(img)
        outside = {k: [round(m[k], 3)] + rng[k][:2] for k in SPRITE_KEYS
                   if k != "coverage" and not raw[k][0] - 1e-9 <= m[k] <= raw[k][1] + 1e-9}
        floor = a.min_coverage * rng["coverage"][2]
        if a.min_coverage and m["coverage"] < floor:
            outside["coverage"] = [round(m["coverage"], 3), round(floor, 3), None]
        row = {"file": c, "size": [img.w, img.h], "measures": {k: round(v, 3) for k, v in m.items()},
               "outside": outside, "pass": not outside}
        if (img.w, img.h) not in sizes:
            row["warning"] = "size differs from every reference: measure the sprite at the size it ships"
        rows.append(row)
    res = {"references": len(refs), "reference_range": rng, "pad": a.pad, "min_coverage": a.min_coverage,
           "candidates": rows,
           "pass": all(r["pass"] for r in rows),
           "note": "opaque pixels at native size, never posterized; [low, high, median] of the references widened "
                   "by pad times their range; coverage has a floor only: min_coverage times the references' median (0 turns it off), "
                   "because bigger is fine and too small breaks the size ladder"}
    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(res, indent=1), encoding="utf-8")
        res["report"] = str(p)
    return out(res)
