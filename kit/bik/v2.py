"""Build-It v2 look (Episode 6 on): light, volume and depth on top of the flat kit.

Everything here is drawn with Skia like the rest of the kit.  The ideas:
  * light instead of flat colour: gradient skies, additive glows, light cones, bloom, grain, vignette;
  * volume from simple shading: cylinders and boxes get a lit side, a core shadow and a rim light;
  * depth: far / mid / near layers with haze between them, soft contact shadows;
  * one UI language: progress HUD, leader-line callouts, phrase captions with the spoken word lit up.
World convention as before: ground at y = 0, up is negative, one unit = one pixel at zoom 1.
"""
import bisect
import math
import random

import numpy as np
import skia

from .core import clamp, lerp, prog, e_back, e_out, e_io
from .draw import C, P, R, rect, circle, poly, line, text, text_width, mix, shade, font
from .arabic import is_ar, text_ar, width_ar

PLUS = skia.BlendMode.kPlus
SCREEN = skia.BlendMode.kScreen
ACCENT, WARN, GOOD, HILITE = "#2DD4BF", "#FF4D4F", "#34D399", "#FFD43B"
GLASS, INK = "#0B1220", "#F8FAFC"


# ---------------------------------------------------------------------------------------------- paint helpers
def lin_paint(x0, y0, x1, y1, colors, pos=None, a=1.0):
    p = skia.Paint(AntiAlias=True)
    cols = [C(col, a) if isinstance(col, str) else C(col[0], col[1] * a) for col in colors]
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], cols, pos))
    return p


def rad_paint(x, y, r, colors, pos=None, a=1.0):
    p = skia.Paint(AntiAlias=True)
    cols = [C(col, a) if isinstance(col, str) else C(col[0], col[1] * a) for col in colors]
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), max(r, 0.01), cols, pos))
    return p


def rr(x, y, w, h, r):
    return skia.RRect.MakeRectXY(R(x, y, w, h), r, r)


def vrect(c, x, y, w, h, colors, pos=None, r=0, a=1.0):
    """Rect filled with a top-to-bottom gradient."""
    p = lin_paint(x, y, x, y + h, colors, pos, a)
    c.drawRRect(rr(x, y, w, h, r), p) if r else c.drawRect(R(x, y, w, h), p)


def cyl_colors(base, depth=1.0):
    """Left-to-right shading of an upright cylinder lit from the upper left, with a cool rim on the right."""
    return ([shade(base, -0.30 * depth), shade(base, 0.10), shade(base, 0.32 * depth), base, shade(base, -0.42 * depth),
             shade(base, -0.22 * depth)], [0.0, 0.14, 0.30, 0.52, 0.86, 1.0])


def cyl(c, x, y, w, h, base, r=0, a=1.0, depth=1.0):
    """Upright cylinder: rect shaded across its width."""
    cols, pos = cyl_colors(base, depth)
    p = lin_paint(x, y, x + w, y, cols, pos, a)
    c.drawRRect(rr(x, y, w, h, r), p) if r else c.drawRect(R(x, y, w, h), p)


def cyl_path(c, path, x0, x1, base, a=1.0, depth=1.0):
    cols, pos = cyl_colors(base, depth)
    c.drawPath(path, lin_paint(x0, 0, x1, 0, cols, pos, a))


def box(c, x, y, w, h, base, r=0, a=1.0, top=0.16, bottom=-0.22):
    """Box face lit from above: lighter top edge, darker toward the bottom."""
    vrect(c, x, y, w, h, [shade(base, top), base, shade(base, bottom)], [0.0, 0.35, 1.0], r, a)


def add_glow(c, x, y, rad, color, a=1.0, mode=PLUS):
    """Additive radial light."""
    if a <= 0 or rad <= 0:
        return
    p = rad_paint(x, y, rad, [(color, a), (color, a * 0.35), (color, 0.0)], [0.0, 0.35, 1.0])
    p.setBlendMode(mode)
    c.drawCircle(x, y, rad, p)


def contact_shadow(c, x, y, w, a=0.45, h=None):
    """Soft dark ellipse on the ground under something."""
    h = h or w * 0.16
    p = rad_paint(0, 0, 1, [("#000000", a), ("#000000", a * 0.5), ("#000000", 0.0)], [0.0, 0.5, 1.0])
    c.save()
    c.translate(x, y)
    c.scale(w / 2, h / 2)
    c.drawCircle(0, 0, 1, p)
    c.restore()


def light_cone(c, x, y, ang_deg, length, spread_deg, color="#FFF1C9", a=0.35):
    """Volumetric beam from a lamp at (x, y); ang 90 = straight down."""
    if a <= 0:
        return
    a0, a1 = math.radians(ang_deg - spread_deg / 2), math.radians(ang_deg + spread_deg / 2)
    path = skia.Path()
    path.moveTo(x, y)
    path.lineTo(x + math.cos(a0) * length, y + math.sin(a0) * length)
    path.lineTo(x + math.cos(a1) * length, y + math.sin(a1) * length)
    path.close()
    p = rad_paint(x, y, length, [(color, a), (color, a * 0.35), (color, 0.0)], [0.0, 0.45, 1.0])
    p.setBlendMode(PLUS)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, max(2.0, length * 0.012)))
    c.drawPath(path, p)


# ---------------------------------------------------------------------------------------------- sky and far layers
NIGHT = {"top": "#060A1E", "upper": "#101542", "mid": "#2B2466", "low": "#74406F", "horizon": "#F0805A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}


def sky(c, W, H, alt=0.0, pal=NIGHT, horizon_y=None):
    """Screen-space twilight sky. alt 0 = standing on the ground, 1 = edge of space."""
    alt = clamp(alt)
    hy = H * 0.66 if horizon_y is None else horizon_y
    top = mix(pal["top"], pal["space_top"], alt)
    upper = mix(pal["upper"], pal["space_mid"], alt)
    midc = mix(pal["mid"], pal["space_mid"], alt)
    low = mix(pal["low"], pal["space_low"], alt)
    hor = mix(pal["horizon"], pal["space_low"], alt)
    k = clamp(hy / H, 0.2, 2.0)
    vrect(c, 0, 0, W, H, [top, upper, midc, low, hor, hor], [0.0, 0.30 * k, 0.60 * k, 0.86 * k, min(0.999, k), 1.0])
    if alt < 1:  # afterglow hugging the horizon
        add_glow(c, W * 0.28, hy, W * 1.1, "#FF9A62", 0.38 * (1 - alt))
        add_glow(c, W * 0.75, hy + 40, W * 0.9, "#FF6F7D", 0.20 * (1 - alt))


_STARS = {}


def stars(c, W, H, t, a=1.0, seed=4, n=260, dx=0.0, dy=0.0):
    """Screen-space star field with slow twinkle; dx, dy shift it (parallax)."""
    if a <= 0:
        return
    key = (seed, n, W, H)
    if key not in _STARS:
        rng = random.Random(seed)
        _STARS[key] = [(rng.uniform(-200, W + 200), rng.uniform(-200, H + 200), rng.uniform(0.7, 2.6) ** 1.6 * 0.55,
                        rng.uniform(0, 6.28), rng.uniform(0.6, 2.2), rng.choice(["#FFFFFF", "#DCE7FF", "#FFE9C9", "#CFE0FF"]))
                       for _ in range(n)]
    for x, y, r, ph, sp, col in _STARS[key]:
        tw = 0.62 + 0.38 * math.sin(t * sp + ph)
        xx, yy = (x + dx) % (W + 400) - 200, (y + dy) % (H + 400) - 200
        c.drawCircle(xx, yy, r, P(col, a * tw))
        if r > 2.0:
            add_glow(c, xx, yy, r * 6, col, 0.30 * a * tw)


def moon(c, x, y, r, a=1.0):
    add_glow(c, x, y, r * 3.6, "#9DB7FF", 0.16 * a)
    add_glow(c, x, y, r * 1.7, "#C9D8FF", 0.20 * a)
    c.drawCircle(x, y, r, rad_paint(x - r * 0.38, y - r * 0.40, r * 1.7, [("#EEF2FF", a), ("#C9D3EE", a), ("#8E9CC4", a)]))
    for dx, dy, rr_ in ((-0.30, -0.18, 0.22), (0.26, 0.10, 0.15), (-0.05, 0.44, 0.12), (0.40, -0.36, 0.09), (-0.48, 0.30, 0.08),
                        (0.10, -0.52, 0.07)):
        c.drawCircle(x + dx * r, y + dy * r, rr_ * r, P("#7C8AB5", 0.55 * a))
        c.drawCircle(x + dx * r + rr_ * r * 0.20, y + dy * r + rr_ * r * 0.20, rr_ * r * 0.80, P("#B4C0E2", 0.60 * a))


def ridge(c, x0, x1, base_y, height, top, bottom, seed=1, step=90, rough=0.55, a=1.0, depth=600, peaks=5):
    """Mountain range between x0 and x1: a few big peaks, broken up by midpoint displacement, filled with a
    vertical gradient (hazy toward the base)."""
    rng = random.Random(seed)
    pts = [(x0 + (x1 - x0) * i / peaks, height * (rng.uniform(0.55, 1.0) if i % 2 else rng.uniform(0.12, 0.42)))
           for i in range(peaks + 1)]
    amp = height * rough * 0.45
    while pts[1][0] - pts[0][0] > step:
        nxt = []
        for (xa, ha), (xb, hb) in zip(pts, pts[1:]):
            nxt.append((xa, ha))
            nxt.append(((xa + xb) / 2, clamp((ha + hb) / 2 + rng.uniform(-amp, amp), height * 0.04, height)))
        nxt.append(pts[-1])
        pts, amp = nxt, amp * 0.55
    path = skia.Path()
    path.moveTo(x0, base_y + depth)
    for x, h in pts:
        path.lineTo(x, base_y - h)
    path.lineTo(x1, base_y + depth)
    path.close()
    c.drawPath(path, lin_paint(0, base_y - height, 0, base_y + 20, [top, bottom], None, a))


_SPRITES = []


def _sprites():
    """Billowy cloud balls rendered once: soft edge, lit from the upper left. Tinted when drawn."""
    if _SPRITES:
        return _SPRITES
    size = 192
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    for k in range(6):
        rng = np.random.default_rng(100 + k)
        lobes = [(0.0, 0.05, 0.60)] + [(rng.uniform(-0.36, 0.36), rng.uniform(-0.34, 0.30), rng.uniform(0.24, 0.40)) for _ in range(10)]
        hgt = np.zeros((size, size), np.float32)
        for lx, ly, lr in lobes:
            d2 = ((xx - size * (0.5 + lx * 0.5)) ** 2 + (yy - size * (0.5 + ly * 0.5)) ** 2) / (lr * size * 0.5) ** 2
            hgt = np.maximum(hgt, np.sqrt(np.clip(1 - d2, 0, 1)) * lr)
        alpha = np.clip(hgt / hgt.max() * 3.4, 0, 1) ** 1.3
        gy, gx = np.gradient(hgt * size * 0.5)
        nz = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
        lum = np.clip(0.50 + 0.62 * ((-gx * 0.58 - gy * 0.66) * nz) + 0.30 * nz, 0.22, 1.0)
        g = (lum * 255).astype(np.uint8)
        arr = np.dstack([g, g, g, (alpha * 255).astype(np.uint8)])
        _SPRITES.append(skia.Image.fromarray(arr, skia.ColorType.kRGBA_8888_ColorType, skia.AlphaType.kUnpremul_AlphaType))
    return _SPRITES


_LIN = skia.SamplingOptions(skia.FilterMode.kLinear)


def puff(c, x, y, r, col, a, lit=None, lit_a=0.0, k=0, rot=0.0, mode=None):
    """One shaded smoke ball (sprite k) tinted col; optional warm light from inside (additive)."""
    if a <= 0 or r <= 0:
        return
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(a))
    p.setColorFilter(skia.ColorFilters.Blend(C(col), skia.BlendMode.kModulate))
    if mode is not None:
        p.setBlendMode(mode)
    img = _sprites()[k % 6]
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(rot)
    c.drawImageRect(img, R(-r * 1.25, -r * 1.25, r * 2.5, r * 2.5), _LIN, p)
    c.restore()
    if lit and lit_a > 0:
        add_glow(c, x, y + r * 0.25, r * 1.25, lit, 0.55 * lit_a * a)


def cloud(c, x, y, s=1.0, body="#3A3568", rim="#FF9D73", a=0.9, seed=0):
    """Dusk cloud: dark billows with a warm underside (lit by the horizon)."""
    rng = random.Random(seed)
    balls = [(-170, 14, 54), (-100, -6, 74), (-20, -26, 96), (70, -10, 80), (150, 12, 58), (215, 22, 40)]
    balls = [(dx + rng.uniform(-14, 14), dy + rng.uniform(-8, 8), r * rng.uniform(0.85, 1.15), rng.randint(0, 5)) for dx, dy, r, in balls]
    for dx, dy, r, k in balls:
        puff(c, x + dx * s, y + (dy + 16) * s, r * s, rim, a * 0.55, k=k)
    for dx, dy, r, k in balls:
        puff(c, x + dx * s, y + dy * s, r * s, shade(body, 0.34), a, k=k)


def earth_limb(c, W, H, a=1.0, y=None):
    """Screen-space curve of the Earth seen from very high up: dark globe, thin blue atmosphere."""
    if a <= 0:
        return
    y = H * 0.80 if y is None else y
    rad = W * 2.6
    cx, cy = W * 0.5, y + rad
    for i, (grow, col, al) in enumerate(((150, "#1D4ED8", 0.10), (90, "#3B82F6", 0.18), (44, "#60A5FA", 0.34), (16, "#BFDBFE", 0.55))):
        p = P(col, al * a, stroke=grow)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, grow * 0.45))
        p.setBlendMode(PLUS)
        c.drawCircle(cx, cy, rad + grow * 0.25, p)
    c.drawCircle(cx, cy, rad, rad_paint(cx - W * 0.5, cy - rad * 0.9, rad * 1.3,
                                        [("#16357A", a), ("#0B1E4D", a), ("#050B22", a)], [0.0, 0.5, 1.0]))
    rng = random.Random(21)  # cloud streaks and city lights on the night side
    c.save()
    clip = skia.Path()
    clip.addCircle(cx, cy, rad)
    c.clipPath(clip, doAntiAlias=True)
    for _ in range(26):
        ang = rng.uniform(-0.42, 0.42)
        d = rad - rng.uniform(20, 330)
        px, py = cx + math.sin(ang) * d, cy - math.cos(ang) * d
        c.save()
        c.translate(px, py)
        c.rotate(math.degrees(ang))
        c.drawRRect(rr(-rng.uniform(60, 220), -8, rng.uniform(120, 440), rng.uniform(8, 22), 10), P("#DDEBFF", 0.10 * a, blur=8))
        c.restore()
    for _ in range(90):
        ang = rng.uniform(-0.40, 0.40)
        d = rad - rng.uniform(30, 300)
        px, py = cx + math.sin(ang) * d, cy - math.cos(ang) * d
        add_glow(c, px, py, rng.uniform(3, 9), "#FFD9A0", 0.5 * a)
    c.restore()


# ---------------------------------------------------------------------------------------------- ground
def ground(c, x0, x1, depth=2600, surface="#39425A", pal=("#232A45", "#161B33", "#0C1024", "#05070F"), seed=11):
    """Night ground with a cutaway: lit surface strip, dark strata fading to near black (captions sit here)."""
    vrect(c, x0, 0, x1 - x0, depth, list(pal), [0.0, 0.14, 0.42, 1.0])
    rng = random.Random(seed)
    for i, (y, hh) in enumerate(((120, 26), (300, 34), (560, 46), (900, 60))):  # strata bands
        vrect(c, x0, y, x1 - x0, hh, [("#FFFFFF", 0.035), ("#000000", 0.10)])
    for _ in range(int((x1 - x0) / 120)):  # buried stones
        rx, ry, rad = rng.uniform(x0, x1), rng.uniform(70, 1300), rng.uniform(9, 30)
        c.drawCircle(rx, ry, rad, rad_paint(rx - rad * 0.4, ry - rad * 0.4, rad * 1.6, [("#3A4466", 0.75), ("#151A30", 0.75)]))
    vrect(c, x0, -6, x1 - x0, 26, [shade(surface, 0.22), surface, shade(surface, -0.35)], [0.0, 0.3, 1.0])
    vrect(c, x0, 18, x1 - x0, 44, [("#000000", 0.38), ("#000000", 0.0)])


# ---------------------------------------------------------------------------------------------- fire, smoke, debris
def flame(c, x, y, w, length, t, power=1.0, seed=0, ang=90.0):
    """Engine plume leaving a nozzle at (x, y), pointing along ang (90 = straight down). Additive."""
    if power <= 0:
        return
    fl = 0.86 + 0.09 * math.sin(t * 47 + seed) + 0.05 * math.sin(t * 83 + seed * 2.3)
    L = length * power * fl
    c.save()
    c.translate(x, y)
    c.rotate(ang - 90)
    add_glow(c, 0, L * 0.25, w * 3.2 + L * 0.35, "#FF8A3D", 0.50 * power)
    for k, (ww, ll, cols) in enumerate(((2.10, 1.00, [("#FF6A2B", 0.0), ("#FF5A2A", 0.55), ("#E5484D", 0.0)]),
                                        (1.45, 0.86, [("#FFB347", 0.9), ("#FF8A3D", 0.75), ("#FF5A2A", 0.0)]),
                                        (0.95, 0.66, [("#FFE9A8", 1.0), ("#FFC857", 0.9), ("#FF8A3D", 0.0)]),
                                        (0.52, 0.44, [("#FFFFFF", 1.0), ("#FFF4D6", 0.95), ("#FFD27A", 0.0)]))):
        hw = w * ww / 2
        ln = L * ll
        wob = math.sin(t * 31 + k * 1.7 + seed) * hw * 0.10
        path = skia.Path()
        path.moveTo(-hw * 0.72, 0)
        path.cubicTo(-hw * 1.25, ln * 0.22, -hw * 0.75 + wob, ln * 0.68, wob * 1.6, ln)
        path.cubicTo(hw * 0.75 + wob, ln * 0.68, hw * 1.25, ln * 0.22, hw * 0.72, 0)
        path.close()
        p = lin_paint(0, 0, 0, ln, cols, [0.0, 0.42, 1.0], power)
        p.setBlendMode(PLUS)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, max(1.5, hw * (0.34 - 0.06 * k))))
        c.drawPath(path, p)
    for i in range(3):  # shock diamonds in the core
        yy = L * (0.13 + 0.115 * i) + (t * 60 % 6)
        add_glow(c, 0, yy, w * (0.36 - 0.07 * i), "#FFFFFF", 0.75 * power)
    c.restore()


def smoke(c, x, y, t, t0, t1=None, rate=26, life=3.2, spread=(260, -60), rise=-70, size=(26, 120), col="#8B93A8",
          lit="#FF8A3D", lit_until=0.9, seed=1, a=0.95, gravity=0.0, drag=1.4, origin=None):
    """Deterministic smoke emitter running from t0 to t1. Puffs leave (x, y) - or origin(birth_time) - with
    spread (vx range, vy), slow down (drag), rise, grow and fade. Hot at birth (lit), cooling to col."""
    if t < t0:
        return
    t1 = t if t1 is None else t1
    n0 = max(0, int((t - life - t0) * rate))
    n1 = int((min(t, t1) - t0) * rate) + 1
    items = []
    for i in range(n0, n1):
        tb = t0 + i / rate
        age = t - tb
        if age < 0 or age > life:
            continue
        rng = random.Random(seed * 7919 + i)
        ox, oy = origin(tb) if origin else (x, y)
        vx = rng.uniform(-spread[0], spread[0])
        vy = spread[1] * rng.uniform(0.3, 1.0)
        k = (1 - math.exp(-drag * age)) / drag
        px = ox + vx * k + math.sin(age * 1.7 + i) * 10
        py = oy + vy * k + rise * age * age * 0.5 + 0.5 * gravity * age * age
        u = age / life
        r = lerp(size[0], size[1], e_out(clamp(u * 1.25))) * rng.uniform(0.75, 1.2)
        al = a * clamp(u * 9) * (1 - u) ** 1.2
        hot = clamp(1 - age / lit_until) if lit_until > 0 else 0.0
        items.append((r, px, py, al, hot, i, rng.uniform(0, 360) + age * rng.uniform(-25, 25)))
    for r, px, py, al, hot, i, rot in sorted(items, key=lambda it: -it[0]):
        puff(c, px, py, r, mix(col, "#FFD9B0", hot * 0.55), al, lit, hot, k=i, rot=rot)


def embers(c, x, y, t, t0, dur=1.6, n=40, speed=900, seed=3, gravity=900, col="#FFC857", size=5.0, cone=(200, 340)):
    """Additive sparks thrown from (x, y) at t0, flying inside the angle range cone (degrees, 270 = up)."""
    age = t - t0
    if age < 0 or age > dur:
        return
    rng = random.Random(seed)
    for _ in range(n):
        ang = math.radians(rng.uniform(*cone))
        sp = speed * rng.uniform(0.25, 1.0)
        life = dur * rng.uniform(0.45, 1.0)
        if age > life:
            continue
        px = x + math.cos(ang) * sp * age
        py = y + math.sin(ang) * sp * age + 0.5 * gravity * age * age
        u = age / life
        vx, vy = math.cos(ang) * sp, math.sin(ang) * sp + gravity * age
        ln = clamp(math.hypot(vx, vy) * 0.035, 4, 46)
        d = math.hypot(vx, vy) or 1
        p = P(col, (1 - u) ** 0.8, stroke=size * (1 - u * 0.6))
        p.setBlendMode(PLUS)
        c.drawLine(px, py, px - vx / d * ln, py - vy / d * ln, p)


def debris(c, x, y, t, t0, dur=2.2, n=16, speed=900, seed=5, gravity=1300, cols=("#DDE3EE", "#6B7385", "#2A3042"),
           floor=None, cone=(205, 335), size=(10, 34)):
    """Tumbling chunks thrown from (x, y); they stop at floor (world y) if given."""
    age = t - t0
    if age < 0 or age > dur:
        return
    rng = random.Random(seed)
    for i in range(n):
        ang = math.radians(rng.uniform(*cone))
        sp = speed * rng.uniform(0.35, 1.0)
        w, h = rng.uniform(*size), rng.uniform(size[0] * 0.5, size[1] * 0.6)
        rot = rng.uniform(-720, 720)
        col = cols[i % len(cols)]
        px = x + math.cos(ang) * sp * age
        py = y + math.sin(ang) * sp * age + 0.5 * gravity * age * age
        if floor is not None and py > floor - h * 0.3 and age > 0.2:
            py = floor - h * 0.3
            rot_now = rot * 0.4
        else:
            rot_now = rot * age
        c.save()
        c.translate(px, py)
        c.rotate(rot_now)
        box(c, -w / 2, -h / 2, w, h, col, r=3, a=clamp((dur - age) * 3))
        c.restore()


def shock_ring(c, x, y, t, t0, dur=0.7, r1=900, col="#FFFFFF", width=26, squash=0.32):
    u = prog(t, t0, t0 + dur)
    if 0 < u < 1:
        p = P(col, (1 - u) ** 1.5 * 0.9, stroke=width * (1 - u * 0.7))
        p.setBlendMode(PLUS)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.save()
        c.translate(x, y)
        c.scale(1, squash)
        c.drawCircle(0, 0, r1 * e_out(u), p)
        c.restore()


def fireball(c, x, y, t, t0, dur=1.6, r=420, seed=2):
    """Explosion: flash, a ball of fire that swells and cools from white-yellow to dark smoke."""
    age = t - t0
    if age < 0 or age > dur:
        return
    u = age / dur
    rng = random.Random(seed)
    grow = e_out(clamp(u * 2.4))
    add_glow(c, x, y - r * 0.2, r * 3.6 * e_out(clamp(u * 3)), "#FF8A3D", 0.85 * (1 - u) ** 1.3)
    balls = []
    for i in range(26):
        ang = rng.uniform(math.pi * 1.02, math.pi * 1.98)
        d = r * rng.uniform(0.05, 1.0) * grow
        rr_ = r * rng.uniform(0.30, 0.56) * (0.45 + grow * 0.75)
        cool = rng.uniform(1.25, 2.6)
        balls.append((rr_, x + math.cos(ang) * d * 1.15, y + math.sin(ang) * d * 0.95 - 90 * u, cool, i, rng.uniform(0, 360)))
    for rr_, px, py, cool, i, rot in sorted(balls, key=lambda b_: -b_[0]):
        heat = clamp(1 - u * cool)
        col = mix("#4A4F63", mix("#FF6A2B", "#FFF1C2", heat), clamp(heat * 1.6))
        puff(c, px, py, rr_, col, clamp((1 - u) * 2.4), "#FFC766", heat, k=i, rot=rot + age * 30)
    add_glow(c, x, y - r * 0.15, r * 1.5 * (1 - u * 0.6), "#FFFFFF", clamp(1 - u * 3.4))


def speed_streaks(c, W, H, t, a=1.0, ang=90.0, seed=6, n=26, col="#FFFFFF"):
    """Screen-space streaks rushing along ang (90 = downward on screen, so the subject seems to fall... upward)."""
    if a <= 0:
        return
    rng = random.Random(seed)
    dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    for _ in range(n):
        x0, y0 = rng.uniform(-100, W + 100), rng.uniform(-200, H + 200)
        sp, ln = rng.uniform(1400, 3200), rng.uniform(120, 420)
        ph = (t * sp + rng.uniform(0, 4000)) % (H + 800) - 400
        x, y = x0 + dx * ph * 0.0, (y0 + ph) % (H + 800) - 400
        p = P(col, a * rng.uniform(0.10, 0.34), stroke=rng.uniform(2, 5))
        p.setBlendMode(PLUS)
        c.drawLine(x, y, x - dx * ln, y - dy * ln, p)


# ---------------------------------------------------------------------------------------------- finishing pass
class Post:
    """Bloom + grain + vignette for a finished frame. One per process (surfaces are made lazily)."""

    def __init__(self, W, H, bloom=0.55, grain=0.07, vignette=0.42, threshold=0.62):
        self.W, self.H, self.k_bloom, self.k_grain, self.k_vig, self.thr = W, H, bloom, grain, vignette, threshold
        self.small = None
        self.noise = None

    def _init(self):
        W, H = self.W, self.H
        self.small = skia.Surface(W // 4, H // 4)
        self.tiny = skia.Surface(W // 12, H // 12)
        rng = np.random.default_rng(5)
        self.noise = []
        for _ in range(6):
            g = np.clip(rng.normal(128, 46, (H // 2 + 64, W // 2 + 64)), 0, 255).astype(np.uint8)
            self.noise.append(skia.Image.fromarray(np.dstack([g, g, g, np.full_like(g, 255)]), skia.ColorType.kRGBA_8888_ColorType))
        g, o = 1.0 / (1.0 - self.thr), -self.thr / (1.0 - self.thr)
        self.high = skia.ColorFilters.Matrix([g, 0, 0, 0, o, 0, g, 0, 0, o, 0, 0, g, 0, o, 0, 0, 0, 1, 0])
        vp = skia.Paint(AntiAlias=True)
        vp.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.46), H * 0.80,
                                                    [C("#000000", 0), C("#000000", 0), C("#02030A", self.k_vig)], [0.0, 0.52, 1.0]))
        self.vig = vp

    def apply(self, c, image, frame=0):
        """Draw image onto canvas c with the finishing pass."""
        if self.small is None:
            self._init()
        W, H = self.W, self.H
        lin = skia.SamplingOptions(skia.FilterMode.kLinear)
        c.drawImage(image, 0, 0)
        for surf, sigma, gain in ((self.small, 5.0, 0.62), (self.tiny, 4.0, 0.50)):
            sc = surf.getCanvas()
            sc.clear(0xFF000000)
            hp = skia.Paint()
            hp.setColorFilter(self.high)
            sc.drawImageRect(image, R(0, 0, W, H), R(0, 0, surf.width(), surf.height()), lin, hp)
            bp = skia.Paint()
            bp.setBlendMode(PLUS)
            bp.setAlphaf(self.k_bloom * gain)
            bp.setImageFilter(skia.ImageFilters.Blur(sigma, sigma))
            c.save()
            c.scale(W / surf.width(), H / surf.height())
            c.drawImage(surf.makeImageSnapshot(), 0, 0, lin, bp)
            c.restore()
        c.drawRect(R(0, 0, W, H), self.vig)
        if self.k_grain > 0:
            rng = random.Random(frame)
            gp = skia.Paint()
            gp.setBlendMode(skia.BlendMode.kSoftLight)
            gp.setAlphaf(self.k_grain * 2.2)
            c.save()
            c.scale(2, 2)
            c.drawImage(self.noise[frame % len(self.noise)], -rng.randint(0, 31), -rng.randint(0, 31), lin, gp)
            c.restore()


# ---------------------------------------------------------------------------------------------- UI: HUD, callouts, badges
def glass(c, x, y, w, h, r=18, a=1.0, tint=GLASS, stroke="#FFFFFF"):
    """Dark glass card with a hairline edge and a soft shadow."""
    c.drawRRect(rr(x, y + 8, w, h, r), P("#000000", 0.38 * a, blur=14))
    c.drawRRect(rr(x, y, w, h, r), lin_paint(x, y, x, y + h, [(shade(tint, 0.10), 0.86 * a), (tint, 0.86 * a)]))
    c.drawRRect(rr(x + 0.75, y + 0.75, w - 1.5, h - 1.5, r), P(stroke, 0.16 * a, stroke=1.5))


def hud(c, W, t, number, title, states, y=150, rtl=False, a=1.0):
    """Top progress HUD. states: four values per fix: 0 idle, ('break', t0) flashing red, ('fix', t0) filled green."""
    if a <= 0:
        return
    seg_w, gap, n = 118, 12, len(states)
    bar_w = n * seg_w + (n - 1) * gap
    num = f"{number:02d}"
    tw_num = text_width(num, 34, "Poppins-Black")
    tw_title = width_ar(title, 34, "Tajawal-Black") if is_ar(title) else text_width(title, 30, "Poppins-Bold")
    w = 34 + tw_num + 22 + tw_title + 34 + bar_w + 34
    x0 = (W - w) / 2
    glass(c, x0, y - 38, w, 76, r=38, a=a)
    order = list(range(n))
    if rtl:  # mirror: bar on the left, title + number on the right
        bx = x0 + 34
        tx_right = x0 + w - 34
        text(c, num, tx_right, y + 12, 34, HILITE, "Poppins-Black", align="right", a=a)
        text_ar(c, title, tx_right - tw_num - 22 - tw_title, y + 12, 34, INK, "Tajawal-Black", align="left", a=a)
        order = order[::-1]
    else:
        text(c, num, x0 + 34, y + 12, 34, HILITE, "Poppins-Black", align="left", a=a)
        text(c, title, x0 + 34 + tw_num + 22, y + 11, 30, INK, "Poppins-Bold", align="left", a=a)
        bx = x0 + 34 + tw_num + 22 + tw_title + 34
    for slot, i in enumerate(order):
        st = states[i]
        sx = bx + slot * (seg_w + gap)
        c.drawRRect(rr(sx, y - 8, seg_w, 16, 8), P("#FFFFFF", 0.16 * a))
        if not st:
            continue
        kind, t0 = st
        if kind == "break":
            pulse = 0.55 + 0.45 * math.sin((t - t0) * 13)
            c.drawRRect(rr(sx, y - 8, seg_w, 16, 8), P(WARN, a * pulse))
            add_glow(c, sx + seg_w / 2, y, seg_w * 0.9, WARN, 0.45 * a * pulse)
        else:
            p = e_out(prog(t, t0, t0 + 0.45))
            fw = seg_w * p
            fx0 = sx + (seg_w - fw if rtl else 0)
            c.drawRRect(rr(fx0, y - 8, max(fw, 0.01), 16, 8), lin_paint(sx, 0, sx + seg_w, 0, ["#34D399", "#2DD4BF"], None, a))
            flash = 1 - prog(t, t0 + 0.2, t0 + 1.0)
            if flash > 0:
                add_glow(c, sx + seg_w / 2, y, seg_w * 1.1, GOOD, 0.75 * a * flash)


def callout(c, ax, ay, lx, ly, label, p, accent=ACCENT, size=34, a=1.0, t=0.0, rtl=False):
    """Leader-line label: pulsing dot on the part at (ax, ay), elbow line, glass card centred at (lx, ly)."""
    if p <= 0:
        return
    a *= clamp(p * 4)
    ar = is_ar(label)
    tw = width_ar(label, size * 1.08, "Tajawal-Bold") if ar else text_width(label, size, "Poppins-Bold")
    w, h = tw + 62, size * 1.72
    k = e_back(clamp(p * 1.15))
    grow = e_out(clamp(p * 1.6))
    ex = lx - w / 2 * (1 if lx > ax else -1) * 0.0
    ey = ly
    mx = ax + (ex - ax) * 0.0
    # dot + ring
    ring = (t * 1.6) % 1.0
    c.drawCircle(ax, ay, 9 + 26 * ring, P(accent, 0.55 * (1 - ring) * a, stroke=3))
    add_glow(c, ax, ay, 34, accent, 0.5 * a)
    c.drawCircle(ax, ay, 9, P("#FFFFFF", a))
    c.drawCircle(ax, ay, 5, P(accent, a))
    # leader: vertical then horizontal, drawn on
    path = skia.Path()
    path.moveTo(ax, ay)
    path.lineTo(ax, ey)
    path.lineTo(lx, ey)
    meas = skia.PathMeasure(path, False)
    seg = skia.Path()
    meas.getSegment(0, meas.getLength() * grow, seg, True)
    c.drawPath(seg, P("#000000", 0.35 * a, stroke=7))
    c.drawPath(seg, P("#FFFFFF", 0.92 * a, stroke=3))
    c.save()
    c.translate(lx, ly)
    c.scale(k, k)
    glass(c, -w / 2, -h / 2, w, h, r=14, a=a)
    bar_x = w / 2 - 20 if rtl or ar else -w / 2 + 14
    c.drawRRect(rr(bar_x, -h / 2 + 12, 6, h - 24, 3), P(accent, a))
    if ar:
        text_ar(c, label, -w / 2 + 22, size * 0.36, size * 1.08, INK, "Tajawal-Bold", align="left", a=a)
    else:
        text(c, label, -w / 2 + 34, size * 0.36, size, INK, "Poppins-Bold", align="left", a=a)
    c.restore()


def badge(c, x, y, p, kind="alert", t=0.0, size=1.0):
    """Round status badge with ring bursts: kind 'alert' (red !) or 'check' (green tick)."""
    if p <= 0:
        return
    col = WARN if kind == "alert" else GOOD
    s = e_back(clamp(p)) * size * (1 + (0.05 * math.sin(t * 13) if kind == "alert" else 0))
    for k in (0.0, 0.33, 0.66) if kind == "alert" else (0.0,):
        u = ((t * 1.3 + k) % 1.0) if kind == "alert" else clamp(p * 0.9)
        c.drawCircle(x, y, (52 + 70 * u) * size, P(col, 0.55 * (1 - u) * clamp(p * 3), stroke=5 * size))
    add_glow(c, x, y, 150 * size, col, 0.45 * clamp(p * 2))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawCircle(0, 8, 50, P("#000000", 0.35, blur=10))
    c.drawCircle(0, 0, 50, rad_paint(-16, -20, 86, [shade(col, 0.30), col, shade(col, -0.28)]))
    c.drawCircle(0, 0, 50, P("#FFFFFF", 0.95, stroke=6))
    if kind == "alert":
        c.drawRRect(rr(-7, -29, 14, 36, 7), P("#FFFFFF"))
        c.drawCircle(0, 21, 8, P("#FFFFFF"))
    else:
        path = skia.Path()
        path.moveTo(-22, 2)
        path.lineTo(-7, 17)
        path.lineTo(24, -15)
        c.drawPath(path, P("#FFFFFF", 1, stroke=11))
    c.restore()


def chip(c, x, y, s, p, fg=INK, bg=GLASS, size=40, accent=None):
    """Small glass chip with text, centred at (x, y)."""
    if p <= 0 or not s:
        return
    ar = is_ar(s)
    tw = width_ar(s, size * 1.08, "Tajawal-Black") if ar else text_width(s, size, "Poppins-Black")
    w, h = tw + 52, size * 1.7
    k = e_back(clamp(p))
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    glass(c, -w / 2, -h / 2, w, h, r=h / 2, a=clamp(p * 3), tint=bg)
    if accent:
        c.drawRRect(rr(-w / 2 + 1, -h / 2 + 1, w - 2, h - 2, h / 2), P(accent, 0.9 * clamp(p * 3), stroke=3))
    if ar:
        text_ar(c, s, -tw / 2, size * 0.36, size * 1.08, fg, "Tajawal-Black", align="left", a=clamp(p * 3))
    else:
        text(c, s, 0, size * 0.36, size, fg, "Poppins-Black", a=clamp(p * 3))
    c.restore()


def follow_pill(c, W, label, sub, p, y=320, rtl=False):
    """Glass pill under the HUD: (+) FOLLOW  next: ..."""
    if p <= 0:
        return
    ar = is_ar(label) or is_ar(sub)
    f1, f2 = ("Tajawal-Black", "Tajawal-Bold") if ar else ("Poppins-Black", "Poppins-SemiBold")
    m1 = (lambda s_: width_ar(s_, 66, f1)) if ar else (lambda s_: text_width(s_, 62, f1))
    m2 = (lambda s_: width_ar(s_, 44, f2)) if ar else (lambda s_: text_width(s_, 42, f2))
    w1, w2 = m1(label), m2(sub)
    w, h = 118 + w1 + 26 + w2 + 46, 124
    k = min(1.0, (W - 60) / w) * e_back(clamp(p))
    c.save()
    c.translate(W / 2, y)
    c.scale(k, k)
    c.drawRRect(rr(-w / 2, -h / 2 + 10, w, h, h / 2), P("#000000", 0.45, blur=16))
    c.drawRRect(rr(-w / 2, -h / 2, w, h, h / 2), lin_paint(-w / 2, 0, w / 2, 0, ["#FF5A3C", "#FF3D6E"]))
    c.drawRRect(rr(-w / 2 + 2, -h / 2 + 2, w - 4, h - 4, h / 2), P("#FFFFFF", 0.35, stroke=3))
    cx = (w / 2 - 62) if (rtl or ar) else (-w / 2 + 62)
    c.drawCircle(cx, 0, 44, P("#FFFFFF"))
    c.drawRRect(rr(cx - 22, -6, 44, 12, 6), P("#FF4D4F"))
    c.drawRRect(rr(cx - 6, -22, 12, 44, 6), P("#FF4D4F"))
    if rtl or ar:
        x = w / 2 - 118
        text_ar(c, label, x - w1, 22, 66, "#FFFFFF", f1, align="left")
        text_ar(c, sub, x - w1 - 26 - w2, 18, 44, "#FFE7DF", f2, align="left")
    else:
        x = -w / 2 + 118
        text(c, label, x, 22, 62, "#FFFFFF", f1, align="left")
        text(c, sub, x + w1 + 26, 18, 42, "#FFE7DF", f2, align="left")
    c.restore()


def stat_card(c, x, y, big, small, p, accent=INK, w=290, h=250):
    """Glass card with a big number and a small label, centred at (x, y)."""
    if p <= 0:
        return
    k = e_back(clamp(p))
    a = clamp(p * 3)
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    glass(c, -w / 2, -h / 2, w, h, r=30, a=a)
    c.drawRRect(rr(-w / 2 + 22, -h / 2 + 18, w - 44, 6, 3), P(accent, 0.9 * a))
    ar = is_ar(small)
    text(c, big, 0, 34, 138, accent, "Poppins-Black", a=a)
    if ar:
        text_ar(c, small, 0, 96, 44, INK, "Tajawal-Bold", a=a)
    else:
        text(c, small, 0, 92, 36, INK, "Poppins-Bold", a=a)
    c.restore()


def gauge(c, x, y, rows, p, w=300, title=None):
    """Glass panel with labelled bars. rows: [(label, fraction 0..1, colour)]."""
    if p <= 0:
        return
    a = clamp(p * 3)
    h = 34 + 78 * len(rows)
    c.save()
    c.translate(x, y)
    c.scale(e_back(clamp(p)), e_back(clamp(p)))
    glass(c, 0, 0, w, h, r=22, a=a)
    for i, (label, frac, col) in enumerate(rows):
        yy = 30 + i * 78
        if is_ar(label):
            text_ar(c, label, w - 24, yy + 22, 30, INK, "Tajawal-Bold", align="right", a=a)
        else:
            text(c, label, 24, yy + 20, 26, INK, "Poppins-Bold", align="left", a=a * 0.9)
        c.drawRRect(rr(24, yy + 32, w - 48, 18, 9), P("#FFFFFF", 0.14 * a))
        fw = max(0.0, (w - 48) * clamp(frac))
        if fw > 1:
            c.drawRRect(rr(24, yy + 32, fw, 18, 9), lin_paint(24, 0, 24 + w - 48, 0, [col, shade(col, 0.25)], None, a))
            add_glow(c, 24 + fw, yy + 41, 26, col, 0.6 * a)
    c.restore()


def pause_overlay(c, W, H, p, y=None):
    """Fake 'video paused' moment: dim + pause icon."""
    if p <= 0:
        return
    y = H * 0.42 if y is None else y
    c.drawRect(R(0, 0, W, H), P("#02030A", 0.38 * clamp(p)))
    k = e_back(clamp(p * 1.4))
    a = clamp(p * 4)
    c.save()
    c.translate(W / 2, y)
    c.scale(k, k)
    c.drawCircle(0, 0, 150, P("#0B1220", 0.62 * a))
    c.drawCircle(0, 0, 150, P("#FFFFFF", 0.35 * a, stroke=4))
    c.drawRRect(rr(-52, -68, 36, 136, 10), P("#FFFFFF", a))
    c.drawRRect(rr(16, -68, 36, 136, 10), P("#FFFFFF", a))
    c.restore()


# ---------------------------------------------------------------------------------------------- captions v2
class Captions:
    """Phrase captions: two to four words on screen, the spoken word lit up and slightly bigger.

    words: the list from bik.captions.word_timings (word, key, start, end, label)."""

    def __init__(self, words, emphasis=(), y=1330, size=86, max_w=960, max_chars=15, max_words=3, hide=(), rtl=False,
                 breaks=()):
        from .captions import word_key
        self.words, self.y, self.size, self.max_w, self.hide, self.rtl = words, y, size, max_w, list(hide), rtl
        self.emph = {word_key(e if is_ar(e) else e.upper()) for e in emphasis}
        self.breaks = set(breaks)  # word indexes (global) that must start a new chunk
        self.chunks = []
        cur, chars = [], 0
        for i, w in enumerate(words):
            new_line = cur and (words[cur[-1]]["label"] != w["label"] or w["start"] - words[cur[-1]]["end"] > 0.28
                                or len(cur) >= max_words or chars + len(w["word"]) > max_chars or i in self.breaks
                                or words[cur[-1]].get("brk"))
            if new_line:
                self.chunks.append(cur)
                cur, chars = [], 0
            cur.append(i)
            chars += len(w["word"]) + 1
        if cur:
            self.chunks.append(cur)
        self.starts = [words[ch[0]]["start"] for ch in self.chunks]

    def draw(self, c, W, t):
        for a, b in self.hide:
            if a <= t < b:
                return
        ci = bisect.bisect_right(self.starts, t) - 1
        if ci < 0:
            return
        ch = self.chunks[ci]
        first, last = self.words[ch[0]], self.words[ch[-1]]
        nxt = self.starts[ci + 1] if ci + 1 < len(self.chunks) else last["end"] + 0.5
        if t > min(nxt, last["end"] + 0.45):
            return
        size = self.size
        ar = any(is_ar(self.words[i]["word"]) for i in ch)
        fname = "Tajawal-Black" if ar else "Poppins-Black"
        fs = size * (1.06 if ar else 1.0)
        meas = (lambda s, z: width_ar(s, z, fname)) if ar else (lambda s, z: text_width(s, z, fname))
        gap = fs * 0.40
        ws = [meas(self.words[i]["word"], fs) for i in ch]
        total = sum(ws) + gap * (len(ch) - 1)
        if total > self.max_w:
            k = self.max_w / total
            fs, gap, ws, total = fs * k, gap * k, [w * k for w in ws], self.max_w
        pin = prog(t, first["start"], first["start"] + 0.14)
        pop = lerp(0.86, 1.0, e_back(pin))
        al = clamp(pin * 4)
        c.save()
        c.translate(W / 2, self.y)
        c.scale(pop, pop)
        # soft dark cushion so the words read on any picture
        c.drawRRect(rr(-total / 2 - 60, -fs * 0.80, total + 120, fs * 1.50, fs * 0.5), P("#000000", 0.34 * al, blur=34))
        x = total / 2 if (self.rtl or ar) else -total / 2
        for i, w_px in zip(ch, ws):
            w = self.words[i]
            active = w["start"] <= t < (self.words[i + 1]["start"] if i + 1 < len(self.words) and i != ch[-1] else w["end"] + 0.3)
            said = t >= w["start"]
            emph = w["key"] in self.emph or (ar and any(e and e in w["key"] for e in self.emph))
            col = HILITE if (active or (emph and said)) else INK
            k = 1.0 + 0.10 * e_back(prog(t, w["start"], w["start"] + 0.16)) * (1 - prog(t, w["start"] + 0.16, w["start"] + 0.42)) if said else 1.0
            a_w = al * (1.0 if said else 0.62)
            cx = x - w_px / 2 if (self.rtl or ar) else x + w_px / 2
            c.save()
            c.translate(cx, 0)
            c.scale(k, k)
            if ar:
                text_ar(c, w["word"], -w_px / 2, fs * 0.34, fs, col, fname, stroke_color="#05070F", stroke_w=fs * 0.13,
                        shadow_a=0.55, a=a_w, align="left")
            else:
                text(c, w["word"], 0, fs * 0.36, fs, col, fname, stroke_color="#05070F", stroke_w=fs * 0.13, shadow_a=0.55, a=a_w)
            c.restore()
            x += -(w_px + gap) if (self.rtl or ar) else (w_px + gap)
        c.restore()
