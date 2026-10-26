"""aw_measure.py: light, colour and composition measures for aw.py (light, gamut, accents, depth, comp).

Imported by aw.py; run them through it (`aw.py light IMG`). Every number is a description in CIELAB and every flag a
pointer to look at, never a grade. Thresholds were set from flag rates on museum works and AI stills (ai-docs log,
2026-10-22) and stay uncalibrated against owner labels. Ideas after Gurney, *Color and Light*, and Roberts,
*Mastering Composition*; the wording and methods are artwright's own.
"""

import math

from aw import Fail, Img, Path, alpha_mask, crop, de2000, flatten, gray_img, lab, load, luma_list, mean_sd, out, resize_box, resize_nearest, save_png, small, sobel

HUES = ((20, "pink"), (50, "red"), (80, "orange"), (115, "yellow"), (165, "green"), (225, "cyan"), (290, "azure"),
        (315, "blue"), (345, "magenta"), (361, "pink"))
HEUR = "flags are uncalibrated heuristics (references/cli.md): confirm each by looking before writing it down"
SEP_WEAK = 0.5  # Otsu separation below this: one value family more than two (heuristic; see track 12 rulings)


def hue_of(a, b):
    return math.degrees(math.atan2(b, a)) % 360


def hue_name(h):
    return next(n for t, n in HUES if h < t)


def chroma(p):
    return math.hypot(p[1], p[2])


def hdist(h1, h2):
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


def pct(sv, q):
    return sv[min(len(sv) - 1, int(q * len(sv)))] if sv else 0.0


def med(v):
    return pct(sorted(v), 0.5)


def lab_rgb(L, a, b):
    def fi(t):
        return t ** 3 if t > 0.2069 else (t - 16 / 116) / 7.787
    fy = (L + 16) / 116
    x, y, z = fi(fy + a / 500) * 0.95047, fi(fy), fi(fy - b / 200) * 1.08883
    res = []
    for v in (3.2406 * x - 1.5372 * y - 0.4986 * z, -0.9689 * x + 1.8758 * y + 0.0415 * z,
              0.0557 * x - 0.2040 * y + 1.0570 * z):
        v = max(0.0, v)
        v = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        res.append(max(0, min(255, round(v * 255))))
    return tuple(res)


def lab_px(img, edge=256):
    s = small(img, edge)
    return s, [lab(c) for c in flatten(s)]


def lab_opaque(img, edge=256):
    """Like lab_px, plus which pixels are opaque enough to measure and the alpha note (transparent pixels are left
    out, never read as white)."""
    s = small(img, edge)
    keep, alpha = alpha_mask(s)
    cols = [c[:3] for c in s.pixels()] if alpha["excluded"] else flatten(s)
    return s, [lab(c) for c in cols], keep, alpha


def otsu(vals, bins=100, eta=False):
    """Otsu's threshold; with eta, also the separability (between-class over total variance, 0 to 1)."""
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-9:
        return (lo, 0.0) if eta else lo
    hist = [0] * bins
    for v in vals:
        hist[min(bins - 1, int((v - lo) / (hi - lo) * bins))] += 1
    n, tot = len(vals), sum(i * c for i, c in enumerate(hist))
    best, t, w0, s0 = -1, 0, 0, 0
    for i, c in enumerate(hist[:-1]):
        w0, s0 = w0 + c, s0 + i * c
        if 0 < w0 < n:
            var = w0 * (n - w0) * (s0 / w0 - (tot - s0) / (n - w0)) ** 2
            if var > best:
                best, t = var, i
    th = lo + (t + 1) * (hi - lo) / bins
    if not eta:
        return th
    tv = sum(i * i * c for i, c in enumerate(hist)) / n - (tot / n) ** 2
    return th, (best / n / n / tv if tv > 0 else 0.0)


def noise_sigma(L, w, h, g=16):
    """Noise SD in L* units from the flattest tenth of a g x g grid of cells (lowest mean Sobel), by Immerkaer's
    estimator (a 3x3 kernel that cancels flat, linear and most curved tone, leaving the grain)."""
    if w < 3 * g or h < 3 * g:
        g = max(1, min(w, h) // 3)
    mag = sobel(L, w, h)
    cells = []
    for gy in range(g):
        for gx in range(g):
            ys = range(max(1, gy * h // g), min(h - 1, (gy + 1) * h // g))
            xs = range(max(1, gx * w // g), min(w - 1, (gx + 1) * w // g))
            v = [mag[y * w + x] for y in ys for x in xs]
            if v:
                cells.append((sum(v) / len(v), ys, xs))
    cells.sort(key=lambda c: c[0])
    tot = cnt = 0
    for _, ys, xs in cells[:max(1, len(cells) // 10)]:
        for y in ys:
            for x in xs:
                i = y * w + x
                tot += abs(4 * L[i] - 2 * (L[i - 1] + L[i + 1] + L[i - w] + L[i + w])
                           + L[i - w - 1] + L[i - w + 1] + L[i + w - 1] + L[i + w + 1])
                cnt += 1
    sig = math.sqrt(math.pi / 2) * tot / (6 * cnt) if cnt else 0.0
    return round(sig, 2), ("clean" if sig < 1 else ("fine grain" if sig < 3 else "noisy"))


def regions(lbl, w, h, conn8=False, every=False):
    """Connected regions of equal labels (of truthy labels unless every): index lists, largest first."""
    seen = bytearray(len(lbl))
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1)) + (((1, 1), (1, -1), (-1, 1), (-1, -1)) if conn8 else ())
    res = []
    for i0, v in enumerate(lbl):
        if seen[i0] or not (every or v):
            continue
        seen[i0], st, reg = 1, [i0], []
        while st:
            i = st.pop()
            reg.append(i)
            x, y = i % w, i // w
            for dx, dy in steps:
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h:
                    j = yy * w + xx
                    if not seen[j] and lbl[j] == v:
                        seen[j] = 1
                        st.append(j)
        res.append(reg)
    return sorted(res, key=len, reverse=True)


def centre(reg, w, h):
    return (round(sum(i % w for i in reg) / len(reg) / w, 3), round(sum(i // w for i in reg) / len(reg) / h, 3))


def focal_cell(lum, w, h, g=8):
    """The cell of a g x g grid with the highest luminance SD, as its centre in fractions."""
    best, focal = -1, (0.5, 0.5)
    for gy in range(g):
        for gx in range(g):
            cell = [lum[y * w + x] for y in range(gy * h // g, (gy + 1) * h // g)
                    for x in range(gx * w // g, (gx + 1) * w // g)]
            if cell:
                v = mean_sd(cell)[1]
                if v > best:
                    best, focal = v, ((gx + 0.5) / g, (gy + 0.5) / g)
    return focal


def box_arg(spec, w, h):
    if not spec:
        return None
    v = [float(t) for t in spec.split(",")]
    if len(v) != 4 or not all(0 <= t <= 1 for t in v):
        raise Fail("a box is x,y,w,h as fractions of width and height, e.g. 0.3,0.2,0.4,0.6")
    x0, y0 = int(v[0] * w), int(v[1] * h)
    return x0, y0, max(x0 + 1, int((v[0] + v[2]) * w)), max(y0 + 1, int((v[1] + v[3]) * h))


def in_box(i, w, b):
    return b[0] <= i % w < b[2] and b[1] <= i // w < b[3]


def family(px):
    a, b = sum(p[1] for p in px) / len(px), sum(p[2] for p in px) / len(px)
    return {"share": len(px), "L_median": round(med([p[0] for p in px]), 1), "a_mean": round(a, 2),
            "b_mean": round(b, 2), "C_median": round(med([chroma(p) for p in px]), 2),
            "hue": hue_name(hue_of(a, b)) if math.hypot(a, b) > 3 else "neutral"}


def light_split(px):
    """Otsu threshold on L* after dropping the top and bottom 1%; returns (threshold, lights, shadows)."""
    sv = sorted(p[0] for p in px)
    lo, hi = pct(sv, 0.01), pct(sv, 0.99)
    keep = [p for p in px if lo <= p[0] <= hi] or px
    t, e = otsu([p[0] for p in keep], eta=True)
    return t, [p for p in keep if p[0] > t], [p for p in keep if p[0] <= t], e


def cmd_light(a):
    s, px, keep, alpha = lab_opaque(load(a.image), a.edge)
    b = box_arg(a.box, s.w, s.h)
    px = [p for i, p in enumerate(px) if keep[i] and (not b or in_box(i, s.w, b))]
    if not px:
        raise Fail("no opaque pixels in the box")
    t, li, sh, sep = light_split(px)
    if not li or not sh:
        raise Fail("one value family only: nothing to compare")
    fl, fs = family(li), family(sh)
    for f in (fl, fs):
        f["share"] = round(f["share"] / len(px), 3)
    gap = round(fl["L_median"] - fs["L_median"], 1)
    ts, tt = round(fl["b_mean"] - fs["b_mean"], 2), round(fl["a_mean"] - fs["a_mean"], 2)
    cr = round(fs["C_median"] / fl["C_median"], 2) if fl["C_median"] >= 3 else None
    read = ["lights %s than shadows by %.1f b*" % ("warmer" if ts >= 0 else "cooler", abs(ts)),
            "value gap %.1f steps of ten" % (gap / 10)]
    flags = []
    if fl["b_mean"] > 5 and ts < 1:
        flags.append("warm_shadows")
        read.append("warm light with shadows as warm or warmer: no cool fill from the sky (fine under artificial "
                    "or alien light)")
    if cr and cr > 1.15:
        flags.append("glowing_shadows")
        read.append("shadows more saturated than lights: the glowing-shadow look")
    if gap < 20:
        flags.append("low_value_gap")
        read.append("light and shadow sides close in value: reads overcast or over-filled (fine if the brief is)")
    if sep < SEP_WEAK:
        read.append("one value family more than two (separation %.2f): the light and shadow numbers are weak" % sep)
    return out({"file": a.image, "alpha": alpha,
                "proxy": "box" if b else "global (one surface with --box is more trustworthy)",
                "threshold_L": round(t, 1), "separation": round(sep, 3), "lights": fl, "shadows": fs, "value_gap": gap,
                "value_gap_steps": round(gap / 10, 1), "temp_shift_b": ts, "tint_shift_a": tt, "chroma_ratio": cr,
                "flags": flags, "readings": read, "note": HEUR})


def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def half(seq):
        hl = []
        for p in seq:
            while len(hl) >= 2 and ((hl[-1][0] - hl[-2][0]) * (p[1] - hl[-2][1])
                                    - (hl[-1][1] - hl[-2][1]) * (p[0] - hl[-2][0])) <= 0:
                hl.pop()
            hl.append(p)
        return hl[:-1]
    return half(pts) + half(pts[::-1])


def poly_area(poly):
    return abs(sum(poly[i - 1][0] * p[1] - p[0] * poly[i - 1][1] for i, p in enumerate(poly))) / 2


def srgb_area():
    """Area of the sRGB gamut's footprint in the a*b* plane (hull of the RGB cube's edges)."""
    pts = []
    for k in range(3):
        for u in (0, 255):
            for v in (0, 255):
                for t in range(0, 256, 15):
                    c = [u, v]
                    c.insert(k, t)
                    L, aa, bb = lab(c)
                    pts.append((round(aa), round(bb)))
    return poly_area(convex_hull(pts))


def draw_line(img, p, q, c):
    n = int(max(abs(q[0] - p[0]), abs(q[1] - p[1]))) + 1
    for k in range(n + 1):
        x, y = round(p[0] + (q[0] - p[0]) * k / n), round(p[1] + (q[1] - p[1]) * k / n)
        if 0 <= x < img.w and 0 <= y < img.h:
            img.put(x, y, c)


def cmd_gamut(a):
    s, px, keep, alpha = lab_opaque(load(a.image), a.edge)
    cols = [c[:3] for c, k in zip(s.pixels(), keep) if k]
    px = [p for p, k in zip(px, keep) if k]
    n = len(px)
    ca, cb = sum(p[1] for p in px) / n, sum(p[2] for p in px) / n
    res = {"file": a.image, "alpha": alpha, "cast": {"a": round(ca, 2), "b": round(cb, 2), "C": round(math.hypot(ca, cb), 2),
                                     "hue": hue_name(hue_of(ca, cb)) if math.hypot(ca, cb) > 2 else "neutral"}}
    chrom = sorted((p for p in px if chroma(p) > 8), key=chroma)
    res["chromatic_share"] = round(len(chrom) / n, 3)
    flags, read = [], []
    if res["cast"]["C"] > 10:
        read.append("everything sits in a %s cast" % res["cast"]["hue"])
    if not chrom:
        res.update(shape="neutral", hue_sectors=0, area_fraction=0.0, flags=flags, readings=read, note=HEUR)
        return out(res)
    mass = sum(chroma(p) for p in chrom)
    sec = [0.0] * 12
    for p in chrom:
        sec[int(hue_of(p[1], p[2]) // 30) % 12] += chroma(p) / mass
    occ = [v >= 0.02 for v in sec]
    clusters, cur = [], []
    start = occ.index(False) if not all(occ) else 0
    for k in range(1, 13):
        j = (start + k) % 12
        if occ[j]:
            cur.append(j)
        elif cur:
            clusters.append(cur)
            cur = []
    if cur:
        clusters.append(cur)

    def ctr(c):
        x = sum(sec[j] * math.cos(math.radians(30 * j + 15)) for j in c)
        y = sum(sec[j] * math.sin(math.radians(30 * j + 15)) for j in c)
        return math.degrees(math.atan2(y, x)) % 360
    cm = sorted(((sum(sec[j] for j in c), ctr(c)) for c in clusters), reverse=True)
    nocc = sum(occ)
    if nocc >= 7:
        shape = "full"
    elif len(cm) == 1:
        shape = "mono" if nocc == 1 else "analogous"
    elif len(cm) == 2 and cm[1][0] < 0.12 and hdist(cm[0][1], cm[1][1]) >= 90:
        shape = "mood+accent"
    elif len(cm) == 2 and hdist(cm[0][1], cm[1][1]) >= 140:
        shape = "complementary"
    elif len(cm) == 3 and min(hdist(x[1], y[1]) for x in cm for y in cm if x is not y) >= 90:
        shape = "triad"
    else:
        shape = "multi"
    kept = chrom[:max(3, int(len(chrom) * 0.96))]
    hl = convex_hull([(round(p[1]), round(p[2])) for p in kept])
    af = poly_area(hl) / srgb_area() if len(hl) >= 3 else 0.0
    mc = med([chroma(p) for p in chrom])
    if shape == "full" and mc > 30:
        flags.append("fruit_salad")
        read.append("every hue at high chroma: no family leads")
    res.update(shape=shape, hue_sectors=nocc, sectors=[round(v, 3) for v in sec], area_fraction=round(af, 3),
               chroma_median=round(mc, 1), families=[{"mass": round(m, 3), "hue": hue_name(hh)} for m, hh in cm],
               flags=flags, readings=read, note=HEUR + "; sectors are 30-degree CIELAB hue bins from 0 (a* axis)")
    if a.overlay:
        o = Img(257, 257, bytearray(b"\x80\x80\x80\xff" * (257 * 257)))
        draw_line(o, (0, 128), (256, 128), (100, 100, 100))
        draw_line(o, (128, 0), (128, 256), (100, 100, 100))
        for c, p in zip(cols, px):
            o.put(max(0, min(256, round(128 + p[1]))), max(0, min(256, round(128 - p[2]))), c)
        for i, p in enumerate(hl):
            q = hl[i - 1]
            draw_line(o, (128 + p[0], 128 - p[1]), (128 + q[0], 128 - q[1]), (0, 0, 0))
        res["overlay"] = save_png(o, a.overlay)
    return out(res)


def cmd_accents(a):
    s, px, keep, alpha = lab_opaque(load(a.image), a.edge)
    if alpha["excluded"]:
        px = [p if k else (100.0, 0.0, 0.0) for p, k in zip(px, keep)]  # transparent reads as neutral, no accent
    w, h, n = s.w, s.h, len(px)
    C = [chroma(p) for p in px]
    chrom = [i for i in range(n) if C[i] > 8]
    focal = focal_cell(luma_list(s), w, h)
    res = {"file": a.image, "alpha": alpha, "focal_cell": [round(v, 3) for v in focal], "accents": [], "note": HEUR}
    if not chrom:
        res["readings"] = ["no chroma: no accents"]
        return out(res)
    tot = sum(C[i] for i in chrom)
    dom = hue_of(sum(px[i][1] for i in chrom), sum(px[i][2] for i in chrom))
    cut = max(15.0, pct(sorted(C), 0.9))
    mask = [C[i] >= cut and hdist(hue_of(px[i][1], px[i][2]), dom) > 90 for i in range(n)]
    share = sum(mask) / n
    read, flags = [], []
    for reg in regions(mask, w, h, conn8=True):
        if len(reg) < max(3, n // 2000):
            break
        cx, cy = centre(reg, w, h)
        hh = hue_of(sum(px[i][1] for i in reg), sum(px[i][2] for i in reg))
        dist = math.hypot(cx - focal[0], cy - focal[1])
        if len(res["accents"]) < 6:
            res["accents"].append({"share": round(len(reg) / n, 4), "hue": hue_name(hh), "centre": [cx, cy],
                                   "focal_distance": round(dist, 3)})
        if dist > 0.35 and len(reg) >= n * 0.002 and share <= 0.05 and "competing_accent" not in flags:
            flags.append("competing_accent")
            read.append("%s accent at (%.2f, %.2f), away from the focal cell: it may pull the eye off the subject"
                        % (hue_name(hh), cx, cy))
    if not res["accents"]:
        read.append("no accent: the image is one colour family")
    if share > 0.05:
        read.append("off-hue high-chroma pixels cover %.0f%%: a second family rather than an accent" % (share * 100))
    res.update(dominant_hue=hue_name(dom), dominance=round(math.hypot(sum(px[i][1] for i in chrom),
                                                                          sum(px[i][2] for i in chrom)) / tot, 3),
               accent_share=round(share, 4), flags=flags, readings=read)
    return out(res)


def band_stats(px):
    Ls = sorted(p[0] for p in px)
    return {"contrast": round(mean_sd(Ls)[1], 2), "dark_p5": round(pct(Ls, 0.05), 1),
            "C_median": round(med([chroma(p) for p in px]), 2), "b_mean": round(sum(p[2] for p in px) / len(px), 2)}


def cmd_depth(a):
    s, px, keep, alpha = lab_opaque(load(a.image), a.edge)
    w, h, n = s.w, s.h, len(px)
    if a.depth:
        d = load(a.depth)
        dv = luma_list(d if (d.w, d.h) == (w, h) else resize_box(d, w, h))
        order = sorted(range(n), key=lambda i: dv[i], reverse=not a.far_bright)
        order = [i for i in order if keep[i]]
        bands = [[px[i] for i in order[k * len(order) // 3:(k + 1) * len(order) // 3]] for k in range(3)]
        proxy = "depth map (%s = near)" % ("dark" if a.far_bright else "bright")
    else:
        bands = [[px[i] for i in range((2 - k) * h // 3 * w, (3 - k) * h // 3 * w) if keep[i]] for k in range(3)]
        proxy = "bands (weak: assumes distance rises up the frame, as in a landscape; pass --depth)"
    if not all(bands):
        raise Fail("a depth band has no opaque pixels")
    near, mid, far = (band_stats(b) for b in bands)
    flags, read = [], []
    for key, word in (("contrast", "contrast"), ("C_median", "chroma")):
        read.append("%s near %.1f, middle %.1f, far %.1f" % (word, near[key], mid[key], far[key]))
    if far["contrast"] >= mid["contrast"] * 0.95 and far["C_median"] >= mid["C_median"] * 0.95:
        flags.append("no_recession")
        read.append("the far band is as crisp and saturated as the middle: the distance does not recede")
    if far["dark_p5"] + 2 < mid["dark_p5"]:
        read.append("darks get darker into the distance")
    if far["b_mean"] > mid["b_mean"] + 3:
        flags.append("warm_distance")
        read.append("distance warmer than the middle: right only toward a low sun")
    return out({"file": a.image, "alpha": alpha, "proxy": proxy, "near": near, "middle": mid, "far": far, "flags": flags,
                "readings": read, "note": HEUR})


def kmeans1(vals, k, it=25):
    sv = sorted(vals)
    cs = [pct(sv, (j + 0.5) / k) for j in range(k)]
    for _ in range(it):
        acc = [[0.0, 0] for _ in cs]
        for v in vals:
            j = min(range(k), key=lambda j: abs(v - cs[j]))
            acc[j][0] += v
            acc[j][1] += 1
        new = sorted(acc[j][0] / acc[j][1] if acc[j][1] else cs[j] for j in range(k))
        if new == cs:
            break
        cs = new
    cuts = [(cs[j] + cs[j + 1]) / 2 for j in range(k - 1)]
    return cs, [sum(v > t for t in cuts) for v in vals]


def zs(v):
    m, sd = mean_sd(v)
    return [(x - m) / (sd or 1) for x in v]


def trim_margin(s):
    """Crop a mat, paper or backdrop margin (museum photographs): every side a uniform band of 2 px up to 1/8,
    at least three of them light. Dark or soft edges in the art itself stay."""
    w, h = s.w, s.h
    lum = luma_list(s)
    lines = (lambda k: lum[k::w], lambda k: lum[k * w:(k + 1) * w], lambda k: lum[w - 1 - k::w],
             lambda k: lum[(h - 1 - k) * w:(h - k) * w])
    d, light = [], 0
    for f, size in zip(lines, (w, h, w, h)):
        k = 0
        while k < size // 8 and mean_sd(f(k))[1] < 0.08:
            k += 1
        if k == size // 8:
            return s, None
        d.append(k)
        light += mean_sd(f(0))[0] > 0.55
    if min(d) < 2 or light < 3:
        return s, None
    d = [k + z // 100 + 1 for k, z in zip(d, (w, h, w, h))]
    return crop(s, d[0], d[1], w - d[0] - d[2], h - d[1] - d[3]), [round(v / z, 3) for v, z in zip(d, (w, h, w, h))]


TEXT_BUSY = {"edge_pull": 1.0, "contrast_pull": 1.0}  # 3 of 10 bands on a five-screen series; 0.8 fired on 9


def text_bands(s, specs):
    """Edge and contrast pull inside each text band against the whole frame (untrimmed: the frame the text sits on).
    edge_pull is the band's mean Sobel magnitude on L* over the image's; contrast_pull the band's SD of L* over the
    image's. A band is busy when either reaches TEXT_BUSY: the text competes with the picture there."""
    w, h = s.w, s.h
    L = [lab(c)[0] for c in flatten(s)]
    mag = sobel([v / 100 for v in L], w, h)
    em, lsd = mean_sd(mag)[0] or 1e-9, mean_sd(L)[1] or 1e-9
    res = []
    for spec in specs:
        b = box_arg(spec, w, h)
        idx = [y * w + x for y in range(b[1], b[3]) for x in range(b[0], b[2])]
        bm, bsd = mean_sd([L[i] for i in idx])
        ep = mean_sd([mag[i] for i in idx])[0] / em
        cp = bsd / lsd
        res.append({"band": spec, "edge_pull": round(ep, 2), "contrast_pull": round(cp, 2), "mean_L": round(bm, 1),
                    "busy": ep >= TEXT_BUSY["edge_pull"] or cp >= TEXT_BUSY["contrast_pull"]})
    return res


def cmd_comp(a):
    img = load(a.image)
    s, trim = trim_margin(small(img, a.edge))
    px = [lab(c) for c in flatten(s)]
    w, h, n = s.w, s.h, len(px)
    L = [p[0] for p in px]
    lum = [v / 100 for v in L]
    sub = box_arg(a.subject, w, h)
    flags, res = [], {"file": a.image, "measured_at": [w, h], "margin_trimmed": trim,
                      "alpha": alpha_mask(s)[1]}
    if res["alpha"]["excluded"]:
        res["alpha"]["note"] = "composition reads the whole frame: transparent pixels on white"
    # 1. value masses: k-means on L* at 64 px, then connected masses of each value
    t = small(s, 64)
    tL = [lab(c)[0] for c in flatten(t)]
    tn = len(tL)
    masses = {}
    for k in (3, 4):
        cs, lbl = kmeans1(tL, k)
        regs = regions(lbl, t.w, t.h, every=True)
        masses[str(k)] = {"centres_L": [round(c, 1) for c in cs], "shares": [round(lbl.count(j) / tn, 3) for j in range(k)],
                          "masses_over_1pct": sum(1 for r in regs if len(r) > tn * 0.01),
                          "largest3_share": round(sum(len(r) for r in regs[:3]) / tn, 3)}
        if a.out:
            g = gray_img([cs[j] / 100 for j in lbl], t.w, t.h)
            masses[str(k)]["map"] = save_png(resize_nearest(g, t.w * 4, t.h * 4), Path(a.out) / ("masses%d.png" % k))
    m3 = masses["3"]
    if m3["shares"][1] > 0.6:
        flags.append("mid_dominant")
    if m3["masses_over_1pct"] > 12 or m3["largest3_share"] < 0.5:
        flags.append("fragmented")
    res["masses"] = masses
    # 2. focal peak on a 16x16 grid: z(L* SD) + z(Sobel mean) + 0.5 z(chroma), runner-up outside the peak's neighbours
    mag = sobel(lum, w, h)
    G, feats = 16, []
    for gy in range(G):
        for gx in range(G):
            idx = [y * w + x for y in range(gy * h // G, (gy + 1) * h // G) for x in range(gx * w // G, (gx + 1) * w // G)]
            idx = idx or [0]
            feats.append((mean_sd([L[i] for i in idx])[1], sum(mag[i] for i in idx) / len(idx),
                          sum(chroma(px[i]) for i in idx) / len(idx)))
    sal = [x + y + 0.5 * z for x, y, z in zip(*(zs([f[k] for f in feats]) for k in range(3)))]
    top = max(range(G * G), key=lambda i: sal[i])
    far = [i for i in range(G * G) if max(abs(i % G - top % G), abs(i // G - top // G)) > 1]
    run = max(far, key=lambda i: sal[i])
    margin = (sal[top] - sal[run]) / sal[top] if sal[top] > 0 else 0.0
    fc = ((top % G + 0.5) / G, (top // G + 0.5) / G)
    res["focal"] = {"peak": [round(v, 3) for v in fc], "runner_up": [(run % G + 0.5) / G, (run // G + 0.5) / G],
                    "margin": round(margin, 3)}
    if margin < 0.03:
        flags.append("competing_focal")
    if sub and not in_box(int(fc[1] * h) * w + int(fc[0] * w), w, sub):
        flags.append("focal_off_subject")
    # 3. border and corner pull: Sobel and chroma in 5% bands and 12% corners, against the whole image
    me = sum(mag) / n or 1e-9
    mcr = sum(chroma(p) for p in px) / n or 1e-9
    bx, by, cx, cy = max(2, w // 20), max(2, h // 20), max(2, w * 12 // 100), max(2, h * 12 // 100)
    zones = {"top": (1, 1, w - 1, by + 1), "bottom": (1, h - by - 1, w - 1, h - 1), "left": (1, 1, bx + 1, h - 1),
             "right": (w - bx - 1, 1, w - 1, h - 1), "top_left": (1, 1, cx, cy), "top_right": (w - cx, 1, w - 1, cy),
             "bottom_left": (1, h - cy, cx, h - 1), "bottom_right": (w - cx, h - cy, w - 1, h - 1)}
    pull = {}
    for z, (x0, y0, x1, y1) in zones.items():
        idx = [y * w + x for y in range(y0, y1) for x in range(x0, x1)] or [0]
        pull[z] = [round(sum(mag[i] for i in idx) / len(idx) / me, 2),
                   round(sum(chroma(px[i]) for i in idx) / len(idx) / mcr, 2)]
    res["border_pull"] = {"zones": pull, "columns": ["edges", "chroma"], "note": "1.0 is the image's mean"}
    if any(max(v) > 2 for v in pull.values()):
        flags.append("edge_pull")
    # 4 and 5. horizontal edge pixels: contours kissing the frame, the horizon, a blocked bottom edge
    hz = bytearray(n)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            i = y * w + x
            dy, dx = lum[i + w] - lum[i - w], lum[i + 1] - lum[i - 1]
            hz[i] = abs(dy) > 0.05 and abs(dy) > 2 * abs(dx)

    def cover(y0, y1):
        cols = [any(hz[y * w + x] for y in range(max(0, y0), min(h, y1))) for x in range(w)]
        best = cur = 0
        for c in cols:
            cur = cur + 1 if c else 0
            best = max(best, cur)
        return sum(cols) / w, best / w
    inset = max(2, h // 50)
    kiss = {"top": cover(1, inset + 1)[1], "bottom": cover(h - inset - 1, h - 1)[1]}
    vt = bytearray(n)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            i = y * w + x
            dy, dx = lum[i + w] - lum[i - w], lum[i + 1] - lum[i - 1]
            vt[i] = abs(dx) > 0.05 and abs(dx) > 2 * abs(dy)
    inset = max(2, w // 50)
    for side, xs in (("left", range(1, inset + 1)), ("right", range(w - inset - 1, w - 1))):
        rows = [any(vt[y * w + x] for x in xs) for y in range(h)]
        best = cur = 0
        for r in rows:
            cur = cur + 1 if r else 0
            best = max(best, cur)
        kiss[side] = best / h
    res["frame_tangents"] = {k: round(v, 3) for k, v in kiss.items() if v > 0.2}
    if res["frame_tangents"]:
        flags.append("frame_tangent")
    rows = [(cover(y - 2, y + 3)[0], y) for y in range(h // 20, h - h // 20)]
    cov, hy = max(rows) if rows else (0, 0)
    hor = {"found": cov >= 0.6, "coverage": round(cov, 3)}
    if hor["found"]:
        f = hy / h
        hor.update(y=round(f, 3), band="upper third" if f < 1 / 3 else ("lower third" if f > 2 / 3 else
                   ("middle" if 0.45 <= f <= 0.55 else "between")))
        if 0.45 <= f <= 0.55:
            flags.append("horizon_split")
        if sub and sub[1] <= hy <= sub[1] + (sub[3] - sub[1]) // 4 and sub[0] < w and sub[2] > 0:
            flags.append("horizon_through_head")
    res["horizon"] = hor
    bot = max([cover(y - 2, y + 3)[0] for y in range(h - h * 12 // 100, h - 2)] or [0])
    res["bottom_barrier"] = round(bot, 3)
    if bot > 0.85:
        flags.append("blocked_entrance")
    # 7. edge hierarchy: variance of the Laplacian per 8x8 cell
    lap = [0.0] * n
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            i = y * w + x
            lap[i] = 4 * lum[i] - lum[i - 1] - lum[i + 1] - lum[i - w] - lum[i + w]
    cells = []
    for gy in range(8):
        for gx in range(8):
            v = [lap[y * w + x] for y in range(gy * h // 8, (gy + 1) * h // 8) for x in range(gx * w // 8, (gx + 1) * w // 8)]
            cells.append(mean_sd(v)[1] ** 2 if v else 0.0)
    # grain lifts every cell by about 20 sigma^2 (the kernel's squared weights), so take that floor off first
    sig = noise_sigma(L, w, h)[0] / 100
    floor = 20 * sig * sig
    cells = [max(0.0, c - floor) for c in cells]
    sharp = max(range(64), key=lambda i: cells[i])
    sc = ((sharp % 8 + 0.5) / 8, (sharp // 8 + 0.5) / 8)
    ratio = cells[sharp] / (med(cells) or 1e-9)
    res["sharpness"] = {"sharpest_cell": sc, "ratio_to_median": round(min(ratio, 999), 2),
                        "noise_sigma": round(sig * 100, 2), "noise_floor": round(floor, 6),
                        "focal_distance": round(math.hypot(sc[0] - fc[0], sc[1] - fc[1]), 3)}
    if ratio < 3:
        flags.append("uniform_sharpness")
    # 8. hot spots: small regions far brighter than their neighbourhood, outside the subject box when given
    r = max(2, min(w, h) * 15 // 200)
    I1, I2 = [0.0] * ((w + 1) * (h + 1)), [0.0] * ((w + 1) * (h + 1))
    for y in range(h):
        s1 = s2 = 0.0
        for x in range(w):
            v = L[y * w + x]
            s1, s2 = s1 + v, s2 + v * v
            j = (y + 1) * (w + 1) + x + 1
            I1[j], I2[j] = I1[j - w - 1] + s1, I2[j - w - 1] + s2
    hot = bytearray(n)
    for y in range(h):
        y0, y1 = max(0, y - r), min(h, y + r + 1)
        for x in range(w):
            x0, x1 = max(0, x - r), min(w, x + r + 1)
            k = (y1 - y0) * (x1 - x0)
            s1 = I1[y1 * (w + 1) + x1] - I1[y0 * (w + 1) + x1] - I1[y1 * (w + 1) + x0] + I1[y0 * (w + 1) + x0]
            s2 = I2[y1 * (w + 1) + x1] - I2[y0 * (w + 1) + x1] - I2[y1 * (w + 1) + x0] + I2[y0 * (w + 1) + x0]
            m = s1 / k
            sd = math.sqrt(max(0.0, s2 / k - m * m))
            hot[y * w + x] = L[y * w + x] - m > max(2.5 * sd, 12)
    spots = []
    for reg in regions(hot, w, h, conn8=True):
        if n * 0.0005 <= len(reg) < n * 0.01:
            c = centre(reg, w, h)
            if not (sub and in_box(int(c[1] * h) * w + int(c[0] * w), w, sub)):
                spots.append({"centre": c, "share": round(len(reg) / n, 4),
                              "near_border": min(c[0], c[1], 1 - c[0], 1 - c[1]) < 0.1})
    res["hot_spots"] = {"count": len(spots), "items": spots[:5]}
    if any(sp["near_border"] for sp in spots):
        flags.append("hot_spot_near_border")
    # 9. figure and ground, when the subject box is given
    if sub:
        x0, y0, x1, y1 = sub
        gx, gy = (x1 - x0) // 4 + 1, (y1 - y0) // 4 + 1
        ring = (max(0, x0 - gx), max(0, y0 - gy), min(w, x1 + gx), min(h, y1 + gy))
        ins = [px[i] for i in range(n) if in_box(i, w, sub)]
        out_ = [px[i] for i in range(n) if in_box(i, w, ring) and not in_box(i, w, sub)] or ins
        mi, mo = [tuple(sum(p[c] for p in q) / len(q) for c in range(3)) for q in (ins, out_)]
        res["figure_ground"] = {"delta_L": round(mi[0] - mo[0], 1), "delta_E": round(de2000(mi, mo), 1),
                                "background_brighter": mo[0] > mi[0] + 10}
        if abs(mi[0] - mo[0]) < 10:
            flags.append("weak_figure_ground")
    # 10. text bands: where a title or a tip will sit, edges and contrast should be quieter than the image's mean
    if getattr(a, "text_band", None):
        res["text_bands"] = text_bands(small(img, a.edge), a.text_band)
        if any(b["busy"] for b in res["text_bands"]):
            flags.append("busy_text_band")
    res.update(flags=flags, note=HEUR + "; not measured here: armature lines, intervals, interior tangents (ask a "
                                        "vision model)")
    return out(res)
