"""Episode 6 - A rocket that lands itself.  First episode in the v2 look (bik/v2.py).

This file currently holds the opening (hook, break 1, fix 1) used as the style sample; the remaining beats
plug into the same three sets: the launch pad, the falling close-up and the high-altitude view.
"""
import math
import os
import random
import sys

import numpy as np
import skia

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)

from bik.core import Timeline, Camera, Track, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump  # noqa: E402
from bik.draw import C, P, R, rect, circle, poly, line, text, text_width, mix, shade  # noqa: E402
from bik import sfx, v2  # noqa: E402
from bik.captions import word_timings  # noqa: E402
from bik.v2 import (lin_paint, rad_paint, rr, vrect, cyl, cyl_path, box, add_glow, contact_shadow, light_cone,  # noqa: E402
                    ACCENT, WARN, GOOD, HILITE, PLUS)

W, H = 1080, 1920
LABELS = ["hook", "break1", "fix1"]
BW, BH, NH = 84, 600, 124          # rocket body width / height, nose height
PAD_Y = -46                        # top of the launch mount: the engines sit here
HULL, BAND, STEEL = "#EEF1F6", "#232936", "#2B3248"


# ====================================================================================== the rocket
def draw_rocket(c, x, y, ang, t, flame=0.0, heat=0.0, gas=(0.0, 0.0), soot=0.0, warm=0.0, s=1.0, fl_len=520):
    """Rocket with its centre at (x, y), rotated ang degrees (0 = nose up). flame 0..1 engine power; heat 0..1
    re-entry glow on the nose; gas (left, right) cold-gas jets at the top; soot 0..1 burnt lower body;
    warm 0..1 orange bounce light on the hull from its own flame."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    hw, top, bot = BW / 2, -BH / 2, BH / 2
    tip = top - NH
    if heat > 0:                                                     # plasma sheath streaming back from the nose
        sheath = skia.Path()
        sheath.moveTo(-200, tip + 640)
        sheath.cubicTo(-150, tip + 230, -96, tip - 4, 0, tip - 36)
        sheath.cubicTo(96, tip - 4, 150, tip + 230, 200, tip + 640)
        sheath.close()
        p = lin_paint(0, tip - 36, 0, tip + 640, [("#FFFFFF", 0.95), ("#FFD27A", 0.78), ("#FF7A2F", 0.40), ("#FF5A2A", 0.0)],
                      [0.0, 0.10, 0.42, 1.0], heat)
        p.setBlendMode(PLUS)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 24))
        c.drawPath(sheath, p)
    if flame > 0:
        v2.flame(c, 0, bot + 54, 62, fl_len, t, flame, seed=3)
    for nx in (-27, 0, 27):                                         # engine bells
        path = skia.Path()
        path.moveTo(nx - 8, bot + 30)
        path.lineTo(nx + 8, bot + 30)
        path.lineTo(nx + 13, bot + 58)
        path.lineTo(nx - 13, bot + 58)
        path.close()
        cyl_path(c, path, nx - 13, nx + 13, "#59607A", depth=1.3)
        if flame > 0:
            add_glow(c, nx, bot + 56, 22, "#FFE9A8", 0.9 * flame)
    cyl(c, -hw - 3, bot - 2, BW + 6, 36, "#171B26", r=5)             # engine skirt
    cyl(c, -hw, top, BW, BH, HULL)                                   # hull
    if soot > 0:
        vrect(c, -hw, top + BH * 0.42, BW, BH * 0.58, [("#14161D", 0.0), ("#14161D", 0.50 * soot), ("#0C0D12", 0.86 * soot)],
              [0.0, 0.55, 1.0])
    cyl(c, -hw, top, BW, 92, BAND)                                   # interstage band
    for yy in (top + 92, -150, -30, 90, 210):                        # panel seams
        c.drawRect(R(-hw, yy - 1.5, BW, 3), P("#0B1020", 0.22))
    c.drawRect(R(hw * 0.42, top + 96, 5, BH - 100), P("#0B1020", 0.16))   # raceway
    for i, yy in enumerate((top + 112, top + 126)):                  # accent rings
        cyl(c, -hw, yy, BW, 7, ACCENT if i == 0 else "#3B82F6", depth=0.8)
    c.save()                                                         # name down the side
    c.translate(-6, 60)
    c.rotate(-90)
    text(c, "CE-06", 0, 0, 34, "#1F2637", "Poppins-Black", a=0.82 * (1 - 0.6 * soot))
    c.restore()
    nose = skia.Path()                                               # nose cone
    nose.moveTo(-hw, top)
    nose.cubicTo(-hw, top - NH * 0.55, -hw * 0.35, top - NH * 0.95, 0, top - NH)
    nose.cubicTo(hw * 0.35, top - NH * 0.95, hw, top - NH * 0.55, hw, top)
    nose.close()
    cyl_path(c, nose, -hw, hw, HULL)
    c.drawRect(R(-hw, top - 2, BW, 4), P("#0B1020", 0.30))
    for side in (-1, 1):                                             # cold-gas thruster pods
        box(c, side * hw - (0 if side > 0 else 12), top + 20, 12, 30, "#3A4258", r=3)
    c.drawRect(R(hw - 4, top - NH * 0.3, 3, BH + NH * 0.3), P("#BFD8FF", 0.50))        # cool rim light (moon)
    if warm > 0:                                                     # warm bounce from the flame
        vrect(c, -hw, top + BH * 0.55, BW, BH * 0.45, [("#FF9A4D", 0.0), ("#FF9A4D", 0.42 * warm)])
    for side, g in zip((-1, 1), gas):                                # gas jets
        if g > 0:
            gx, gy = side * (hw + 10), top + 35
            for k in range(5):
                u = ((t * 3.1 + k * 0.2) % 1.0)
                r_ = (10 + 46 * u) * g
                p = rad_paint(gx + side * (16 + 120 * u) * g, gy + math.sin(k * 2.1 + t * 9) * 8, r_, [("#FFFFFF", 0.85 * (1 - u) * g), ("#DDEBFF", 0.0)])
                c.drawCircle(gx + side * (16 + 120 * u) * g, gy + math.sin(k * 2.1 + t * 9) * 8, r_, p)
            add_glow(c, gx + side * 20, gy, 60 * g, "#DCEBFF", 0.55 * g)
    if heat > 0:                                                     # the nose itself glows
        c.save()
        c.clipPath(nose, doAntiAlias=True)
        vrect(c, -hw, tip, BW, NH, [("#FFFFFF", 0.95 * heat), ("#FFC766", 0.80 * heat), ("#FF7A2F", 0.35 * heat)])
        c.restore()
        vrect(c, -hw, top, BW, 150, [("#FF8A3D", 0.42 * heat), ("#FF8A3D", 0.0)])
        add_glow(c, 0, tip + 8, 170, "#FF9A4D", 0.50 * heat)
        add_glow(c, 0, tip - 6, 62, "#FFFFFF", 0.95 * heat)
        rng = random.Random(8)
        for _ in range(18):                                          # plasma streaks trailing back along the hull
            sx = rng.uniform(-hw - 90, hw + 90)
            ph = (t * rng.uniform(900, 1600) + rng.uniform(0, 900)) % 900
            p = P(rng.choice(["#FFD27A", "#FF9A4D", "#FFFFFF"]), 0.5 * heat * (1 - ph / 900), stroke=rng.uniform(2, 5))
            p.setBlendMode(PLUS)
            c.drawLine(sx, tip + 60 + ph, sx * 1.05, tip + 60 + ph + rng.uniform(60, 170), p)
    c.restore()


# ====================================================================================== set pieces
def lattice(c, x, y0, y1, w=44, col=STEEL, lit=0.0):
    """Steel lattice tower from ground y0 up to y1 (y1 < y0)."""
    c.drawRect(R(x - w / 2, y1, 7, y0 - y1), lin_paint(x - w / 2, 0, x - w / 2 + 7, 0, [shade(col, 0.25), shade(col, -0.2)]))
    c.drawRect(R(x + w / 2 - 7, y1, 7, y0 - y1), lin_paint(x + w / 2 - 7, 0, x + w / 2, 0, [shade(col, 0.10), shade(col, -0.35)]))
    yy, k = y0, 0
    while yy > y1 + 20:
        a, b = (x - w / 2 + 3, x + w / 2 - 3) if k % 2 == 0 else (x + w / 2 - 3, x - w / 2 + 3)
        c.drawLine(a, yy, b, yy - 46, P(shade(col, 0.12), 1, stroke=4))
        c.drawRect(R(x - w / 2, yy - 48, w, 4), P(shade(col, -0.1)))
        yy -= 46
        k += 1
    if lit > 0:
        vrect(c, x - w / 2, y1, w, y0 - y1, [("#FF9A4D", 0.0), ("#FF9A4D", 0.45 * lit)])


def beacon(c, x, y, t, col="#FF4D4F", hz=1.1, r=7, ph=0.0):
    on = 0.35 + 0.65 * (math.sin((t * hz + ph) * 2 * math.pi) > 0.2)
    add_glow(c, x, y, r * 9, col, 0.65 * on)
    c.drawCircle(x, y, r, P(mix(col, "#FFFFFF", 0.3 * on)))


def floodlight(c, x, h, tx, ty, t, on=1.0, flip=False):
    """Pole with a lamp bank at (x, -h) aimed at (tx, ty)."""
    c.drawRect(R(x - 5, -h, 10, h), lin_paint(x - 5, 0, x + 5, 0, [shade(STEEL, 0.3), shade(STEEL, -0.3)]))
    c.drawRect(R(x - 16, -8, 32, 8), P(shade(STEEL, -0.2)))
    ang = math.degrees(math.atan2(ty + h, tx - x))
    if on > 0:
        light_cone(c, x, -h, ang, math.hypot(tx - x, ty + h) * 1.25, 17, "#FFF1C9", 0.30 * on)
    c.save()
    c.translate(x, -h)
    c.rotate(ang)
    box(c, -8, -22, 26, 44, "#3A4258", r=4)
    for dy in (-12, 0, 12):
        c.drawCircle(18, dy, 5, P(mix("#59607A", "#FFF7DA", on)))
    c.restore()
    if on > 0:
        add_glow(c, x + math.cos(math.radians(ang)) * 18, -h + math.sin(math.radians(ang)) * 18, 64, "#FFF1C9", 0.85 * on)


def bunker(c, x, t, lit=0.0, w=250, h=128):
    """Control building with lit windows and a dish."""
    contact_shadow(c, x + w / 2, 4, w * 1.2, 0.5, 26)
    box(c, x, -h, w, h, "#2A3149", r=4)
    box(c, x - 8, -h - 12, w + 16, 16, "#46506E", r=4)
    box(c, x + 18, -84, 70, 84, "#1A2036", r=3)                      # door
    for i in range(3):                                               # lit windows
        wx = x + 104 + i * 46
        c.drawRRect(rr(wx, -92, 32, 40, 4), P("#FFD98A"))
        add_glow(c, wx + 16, -72, 62, "#FFC766", 0.34)
        c.drawRect(R(wx + 15, -92, 2, 40), P("#7A5A22", 0.6))
    c.drawRect(R(x + w - 46, -h - 70, 5, 60), P(STEEL))              # antenna + dish
    beacon(c, x + w - 44, -h - 74, t, hz=0.8, r=5, ph=0.4)
    c.drawArc(R(x + w - 118, -h - 62, 56, 56), 200, 140, True, P("#5A6482"))
    if lit > 0:
        vrect(c, x, -h, w * 0.45, h, [("#FF9A4D", 0.34 * lit), ("#FF9A4D", 0.0)])


def engineer(c, x, y, h, shirt, t, pose="stand", soot=0.0, face=1):
    """Small rounded engineer in a hard hat, feet at (x, y). pose: stand | cheer | look | point | duck."""
    u = h / 140.0
    skin = mix("#E8B48A", "#2A2A30", soot * 0.7)
    shirt = mix(shirt, "#22242C", soot * 0.75)
    c.save()
    c.translate(x, y)
    if pose == "duck":
        c.scale(1, 0.64)
    if pose == "cheer":
        c.translate(0, -abs(math.sin(t * 9 + x)) * 10 * u)
    contact_shadow(c, 0, 0, 70 * u, 0.45, 12 * u)
    for dx in (-13, 3):
        box(c, dx * u, -52 * u, 11 * u, 52 * u, "#1F2538", r=5 * u)
    arm = P(skin, 1, stroke=10 * u)
    if pose == "cheer":
        for sd in (-1, 1):
            c.drawLine(sd * 17 * u, -98 * u, sd * 34 * u, -150 * u, arm)
    elif pose in ("look", "point"):
        c.drawLine(-17 * u, -98 * u, -24 * u, -58 * u, arm)
        c.drawLine(17 * u, -98 * u, (40 if pose == "point" else 14) * u * face, (-150 if pose == "point" else -134) * u, arm)
    elif pose == "duck":
        for sd in (-1, 1):
            c.drawLine(sd * 17 * u, -98 * u, sd * 12 * u, -148 * u, arm)
    else:
        for sd in (-1, 1):
            c.drawLine(sd * 18 * u, -98 * u, sd * 22 * u, -58 * u, arm)
    box(c, -21 * u, -110 * u, 42 * u, 64 * u, shirt, r=15 * u)
    vrect(c, -21 * u, -80 * u, 42 * u, 9 * u, [("#F8FAFC", 0.85 * (1 - soot)), ("#CBD5E1", 0.85 * (1 - soot))])   # reflective band
    tilt = -16 * face if pose in ("look", "point") else 0
    c.save()
    c.translate(0, -112 * u)
    c.rotate(tilt)
    c.drawCircle(0, -15 * u, 18 * u, rad_paint(-6 * u, -22 * u, 30 * u, [shade(skin, 0.15), skin, shade(skin, -0.25)]))
    hat = skia.Path()                                                # hard hat
    hat.moveTo(-20 * u, -18 * u)
    hat.cubicTo(-20 * u, -44 * u, 20 * u, -44 * u, 20 * u, -18 * u)
    hat.close()
    c.drawPath(hat, lin_paint(-20 * u, 0, 20 * u, 0, ["#FDE68A", "#FACC15", "#CA8A04"]))
    c.drawRRect(rr(-25 * u, -21 * u, 50 * u, 7 * u, 3 * u), P(mix("#EAB308", "#3A3A3A", soot * 0.5)))
    c.restore()
    c.restore()


def buried_line(c, pts, col, t, flow=0.0, w=10):
    """Pipe under the ground along pts, with dashes of light flowing along it."""
    path = skia.Path()
    path.moveTo(*pts[0])
    for pt in pts[1:]:
        path.lineTo(*pt)
    pr = P("#0A0D1A", 0.9, stroke=w + 6)
    pr.setPathEffect(skia.CornerPathEffect.Make(18))
    c.drawPath(path, pr)
    pr = P(shade(col, -0.55), 1, stroke=w)
    pr.setPathEffect(skia.CornerPathEffect.Make(18))
    c.drawPath(path, pr)
    if flow > 0:
        pr = P(col, flow, stroke=w * 0.5)
        pr.setPathEffect(skia.PathEffect.MakeCompose(skia.DashPathEffect.Make([26, 44], -t * 150), skia.CornerPathEffect.Make(18)))
        pr.setBlendMode(PLUS)
        c.drawPath(path, pr)


def tank(c, x, t):
    """Spherical propellant tank on legs."""
    for dx in (-44, 44):
        c.drawLine(x + dx, 0, x + dx * 0.55, -70, P(STEEL, 1, stroke=7))
    contact_shadow(c, x, 4, 190, 0.45, 26)
    c.drawCircle(x, -118, 74, rad_paint(x - 28, -150, 130, ["#F2F5FA", "#B9C2D6", "#5C667F"], [0.0, 0.5, 1.0]))
    c.drawArc(R(x - 74, -192, 148, 148), 20, 140, False, P("#0B1020", 0.18, stroke=3))
    c.drawRect(R(x - 2, -230, 4, 40), P(STEEL))
    beacon(c, x, -232, t, hz=0.9, r=5, ph=0.2)


def crater(c, x, k, t):
    """Blast crater replacing the pad; k 0..1 how far it has opened."""
    if k <= 0:
        return
    w, d = 620 * k, 150 * k
    path = skia.Path()
    path.moveTo(x - w / 2 - 40, -6)
    path.cubicTo(x - w / 2, -4, x - w * 0.36, d, x, d)
    path.cubicTo(x + w * 0.36, d, x + w / 2, -4, x + w / 2 + 40, -6)
    path.close()
    c.drawPath(path, lin_paint(0, -6, 0, d, ["#0A0C16", "#191322", "#3A1B1F"]))
    hot = 0.55 + 0.25 * math.sin(t * 5)
    add_glow(c, x, d * 0.7, w * 0.42, "#FF5A2A", 0.55 * hot * k)
    add_glow(c, x - w * 0.16, d * 0.5, w * 0.18, "#FFC857", 0.45 * hot * k)
    rng = random.Random(4)
    for i in range(12):                                              # rubble on the rim
        rx = x + rng.uniform(-w / 2 - 110, w / 2 + 110)
        if abs(rx - x) < w * 0.33:
            continue
        ww, hh = rng.uniform(20, 58), rng.uniform(12, 30)
        c.save()
        c.translate(rx, -6)
        c.rotate(rng.uniform(-28, 28))
        box(c, -ww / 2, -hh, ww, hh, rng.choice(["#6B7488", "#4A5368", "#2A3042"]), r=3)
        c.restore()


# ====================================================================================== sounds made for this episode
def rumble(d=2.4, seed=40):
    n = int(d * sfx.SR)
    x = np.cumsum(sfx._rng(seed).standard_normal(n))
    x = sfx._hp(x, 28) + 0.5 * sfx._bp(sfx._rng(seed + 1).standard_normal(n), 300, 1800)
    env = np.minimum(1, np.arange(n) / (0.25 * sfx.SR)) * np.exp(-np.arange(n) / (d * 0.55 * sfx.SR))
    return sfx._norm(sfx._lp(x, 900) * env, 0.9)


def boom(d=1.8, seed=41):
    n = int(d * sfx.SR)
    t = np.arange(n) / sfx.SR
    thump = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-t * 5) + 28) / sfx.SR) * np.exp(-t * 3.2)
    noise = sfx._lp(sfx._rng(seed).standard_normal(n), 1400) * np.exp(-t * 2.6)
    crack = sfx._hp(sfx._rng(seed + 1).standard_normal(n), 2500) * np.exp(-t * 22) * 0.6
    return sfx._norm(thump * 1.2 + noise + crack, 0.95)


def gas_hiss(d=0.5, seed=42):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 2500, 9000)
    return sfx._norm(x * sfx._ar(n, 0.02, d * 0.6), 0.5)


# ====================================================================================== the episode
class Rocket:
    BUILD_NO, TITLE = 6, {"en": "ROCKET"}
    EMPH = {"en": ["CONGRATS", "LANDS", "ITSELF", "CRATER", "FLIP", "TAIL", "FIRST", "BULLET"]}
    TAIL = 1.2

    def __init__(self, vo_json, vo_wav, lang="en"):
        self.lang, self.rtl = lang, lang.startswith("ar")
        self.tl = tl = Timeline(vo_json, LABELS, lead=0.5, pause=0.6, tail=self.TAIL)
        self.words = word_timings(vo_wav, tl)
        self.cap = v2.Captions(self.words, self.EMPH.get(lang, self.EMPH["en"]), rtl=self.rtl)
        self.duration = tl.duration
        self.post = v2.Post(W, H)
        self.buf = None
        self._tracks()

    # ------------------------------------------------------------------ timing
    def w(self, lab, key, frac=0.5, nth=0):
        from bik.captions import Captions as _C1
        if not hasattr(self, "_finder"):
            self._finder = _C1(self.words)
        t = self._finder.find(lab, key, nth)
        return lerp(self.tl.s(lab), self.tl.e(lab), frac) if t is None else t

    def _tracks(self):
        w, s, e = self.w, self.tl.s, self.tl.e
        T = self.T = {}
        T["launch"] = w("hook", "LAUNCH", 0.15)
        T["wait"] = w("hook", "WAIT", 0.4)
        T["congrats"] = w("hook", "CONGRATS", 0.5)
        T["lands"] = w("hook", "LANDS", 0.85)
        T["cut_fall"] = s("break1") - 0.10                      # whip up to the falling rocket
        T["nose"] = w("break1", "NOSE", 0.2)
        T["faster"] = w("break1", "FASTER", 0.35)
        T["bullet"] = w("break1", "BULLET", 0.5)
        T["cut_pad"] = w("break1", "AND", 0.55) + 0.02          # whip back down to the pad
        T["impact"] = w("break1", "LAUNCH", 0.75) + 0.02
        T["crater"] = w("break1", "CRATER", 0.9)
        T["cut_space"] = s("fix1") - 0.12
        T["gas"] = w("fix1", "GAS", 0.15)
        T["flip"] = w("fix1", "FLIP", 0.35)
        T["relight"] = w("fix1", "RELIGHT", 0.5)
        T["brake"] = w("fix1", "BRAKE", 0.7)
        T["tail"] = w("fix1", "TAIL", 0.9)
        T["end"] = e("fix1")
        # launch pad camera (world units)
        self.cam = Camera(0, -360, 0.80)
        self.cam.key(0.05, 0, -340, 0.90, 0.9)
        self.cam.key(T["launch"] + 0.10, 0, -620, 0.86, 1.0)     # tilt up after the rocket
        self.cam.key(T["wait"] + 0.1, 0, -700, 0.84, 1.2)
        self.cam.key(T["cut_pad"], 0, -330, 0.84, 0.0)
        self.cam.key(T["impact"] + 0.5, 0, -250, 0.92, 1.6)
        # rocket height above the mount during the launch (accelerating)
        self.shakes = [(T["launch"], 1.3, 16), (T["nose"] - 0.4, 1.9, 7), (T["impact"], 1.1, 46), (T["relight"], 0.9, 9)]
        self.flip = Track(180.0).to(T["flip"], -8.0, 0.80, e_io).to(T["flip"] + 0.80, 0.0, 0.35, e_io)

    # ------------------------------------------------------------------ helpers
    def mode(self, t):
        T = self.T
        if t >= T["cut_space"]:
            return "space"
        if T["cut_fall"] <= t < T["cut_pad"]:
            return "fall"
        return "pad"

    def whip(self, t):
        """Vertical offset (pixels) and blur amount for the whip cuts. (offset, amount)."""
        T = self.T
        for tc, sign in ((T["cut_fall"], 1), (T["cut_pad"], -1), (T["cut_space"], 1)):
            if tc - 0.13 <= t < tc:
                p = e_in(prog(t, tc - 0.13, tc))
                return sign * p * H * 0.9, p
            if tc <= t < tc + 0.16:
                p = 1 - e_out(prog(t, tc, tc + 0.16))
                return -sign * p * H * 0.9, p
        return 0.0, 0.0

    def shake(self, t):
        dx = dy = 0.0
        for t0, d, amp in self.shakes:
            if t0 <= t < t0 + d:
                k = (1 - (t - t0) / d) ** 1.5 * amp
                dx += math.sin(t * 91) * k
                dy += math.cos(t * 77) * k
        return dx, dy

    # ------------------------------------------------------------------ frame
    def draw(self, c, t):
        if self.buf is None:
            self.buf = skia.Surface(W, H)
        b = self.buf.getCanvas()
        b.clear(C("#070B1F"))
        off, amt = self.whip(t)
        sx, sy = self.shake(t)
        m = self.mode(t)
        if amt > 0:                                              # sky behind the sliding picture, so no edge shows
            v2.sky(b, W, H, {"pad": 0.0, "fall": 0.42, "space": 1.0}[m], horizon_y=H * (1.5 if m == "fall" else 0.66))
            v2.stars(b, W, H, t, 0.8)
        b.save()
        b.translate(sx, sy + off)
        (self.draw_space if m == "space" else self.draw_fall if m == "fall" else self.draw_pad)(b, t)
        b.restore()
        if amt > 0:                                              # smear during the whip
            v2.speed_streaks(b, W, H, t, 0.9 * amt, seed=12, n=60)
            b.drawRect(R(0, 0, W, H), P("#0B1026", 0.25 * amt))
        self.post.apply(c, self.buf.makeImageSnapshot(), int(round(t * 30)))
        self.draw_ui(c, t)
        self.cap.draw(c, W, t)

    # ------------------------------------------------------------------ set 1: the launch pad
    def draw_pad(self, c, t):
        T = self.T
        cx, cy, z = self.cam.at(t)
        cx += math.sin(t * 0.7) * 3
        gy = (0 - cy) * z + H / 2                                 # screen y of the ground line
        launched = t >= T["launch"]
        tl_ = t - T["launch"]
        rise = 0.0 if not launched else 0.5 * 1750 * max(0.0, tl_ - 0.12) ** 2
        burn = clamp(tl_ * 6) if launched else 0.0
        back = t >= T["cut_pad"]                                 # the wreck comes back
        hit = t - T["impact"]
        glow_k = burn * clamp(1 - rise / 2600) if not back else 0.0
        # ---- far layers (screen space, parallax)
        v2.sky(c, W, H, 0.0, horizon_y=gy)
        v2.stars(c, W, H, t, 0.9, dx=-cx * 0.02, dy=(cy + 360) * -0.03)
        v2.moon(c, 236 - cx * 0.02, gy - 880, 74)
        for i, (px, py, s_, par) in enumerate(((260, 640, 1.0, 0.05), (840, 470, 0.72, 0.035), (-60, 400, 0.6, 0.03))):
            v2.cloud(c, (px + t * (5 + i * 2) - cx * par) % (W + 700) - 250, gy - py, s_, a=0.85, seed=i)
        c.save()
        c.translate(W / 2 - cx * 0.06, gy)
        v2.ridge(c, -1500, 1500, 0, 250, "#3A3378", "#B25A72", seed=5, step=150, rough=0.5)
        rng = random.Random(9)
        for _ in range(46):                                      # far town lights
            lx = rng.uniform(-900, 900)
            add_glow(c, lx, rng.uniform(-22, -4), rng.uniform(4, 9), rng.choice(["#FFD98A", "#FFE9C9", "#FFB37A"]), 0.8)
        c.restore()
        c.save()
        c.translate(W / 2 - cx * 0.16, gy)
        v2.ridge(c, -1700, 1700, 0, 120, "#1B1C4A", "#3B2A5E", seed=8, step=70, rough=0.75)
        c.restore()
        # ---- world
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)
        v2.ground(c, -3200, 3200)
        k_cr = e_out(prog(t, T["impact"], T["impact"] + 0.5)) if back else 0.0
        fuel = clamp(1 - tl_ * 2) if launched else 1.0
        buried_line(c, [(-430, 0), (-430, 176), (-52, 176), (-52, 10)], ACCENT, t, 0.9 * fuel * (1 - k_cr))          # fuel
        buried_line(c, [(470, 0), (470, 214), (40, 214), (40, 10)], "#60A5FA", t, 0.8 * (1 - k_cr), w=7)              # power + data
        tank(c, -430, t)
        c.drawRect(R(300, -830, 6, 830), lin_paint(300, 0, 306, 0, [shade(STEEL, 0.35), shade(STEEL, -0.3)]))     # lightning mast
        beacon(c, 303, -836, t, hz=1.3, ph=0.5)
        bunker(c, 352, t, lit=glow_k)
        lean = -24 * e_out(prog(t, T["impact"] + 0.05, T["impact"] + 0.9)) if back else 0.0
        if k_cr < 1:                                             # pad apron + launch mount
            box(c, -330, -16, 660, 22, "#59627A", r=4, a=1 - k_cr)
            for sx_ in range(-300, 301, 60):
                c.drawRect(R(sx_ - 18, -15, 36, 5), P("#FACC15", 0.75 * (1 - k_cr)))
            box(c, -76, PAD_Y, 152, -PAD_Y - 14, "#343C52", r=5, a=1 - k_cr)
            contact_shadow(c, 0, -14, 300, 0.5 * (1 - k_cr), 30)
        crater(c, 0, k_cr, t)
        if glow_k > 0:                                           # the plume lights the ground
            add_glow(c, 0, -20, 1100, "#FF8A3D", 0.50 * glow_k)
            add_glow(c, 0, -20, 420, "#FFD27A", 0.50 * glow_k)
        c.save()                                                 # service tower (falls over after the hit)
        c.translate(-178, 0)
        c.rotate(lean)
        lattice(c, 0, 0, -690, 52, lit=glow_k * 0.8)
        for ay in (-560, -300):
            ext = lerp(138, 40, clamp((tl_ + 0.5) * 2.2)) if launched else 138
            box(c, 20, ay, ext, 16, "#3A4258", r=3)
        for wy in (-640, -470, -300, -130):
            add_glow(c, 26, wy, 38, "#FFF1C9", 0.75)
            c.drawCircle(26, wy, 4, P("#FFFFFF"))
        beacon(c, 0, -702, t)
        c.restore()
        on = 1.0 if not back else clamp(1 - (hit + 0.1) * 6) if hit > -0.1 else 1.0
        floodlight(c, -560, 250, -20, -420, t, on)
        floodlight(c, 560, 228, 20, -380, t, on)
        rise_at = lambda tb: 0.5 * 1750 * max(0.0, tb - T["launch"] - 0.12) ** 2      # noqa: E731
        if launched and not back:                                # exhaust: a rolling ground cloud and a trail up the sky
            v2.smoke(c, 0, -30, t, T["launch"], T["launch"] + 1.6, rate=30, life=3.8, spread=(700, -30), rise=-24,
                     size=(54, 230), col="#B9BFD0", lit="#FF8A3D", lit_until=1.0, seed=2, drag=1.8)
            v2.smoke(c, 0, 0, t, T["launch"] + 0.16, T["launch"] + 1.5, rate=90, life=3.4, spread=(46, 30), rise=-6,
                     size=(40, 135), col="#BFC5D6", lit="#FFB05C", lit_until=0.45, seed=5, drag=1.4, a=0.8,
                     origin=lambda tb: (math.sin(tb * 7) * 8, PAD_Y + 40 - rise_at(tb)))
        if not back:
            ry = PAD_Y - 58 - BH / 2 - rise
            if ry > cy - H / z:                                  # still in (or near) frame
                if not launched:
                    contact_shadow(c, 0, PAD_Y, 160, 0.6, 16)
                draw_rocket(c, 0, ry, 0, t, flame=burn, warm=burn * 0.8, fl_len=600)
                if launched:
                    v2.embers(c, 0, PAD_Y, t, T["launch"] + 0.02, 1.2, n=46, speed=1100, seed=7, cone=(185, 355))
        else:
            fall = prog(t, T["impact"] - 0.20, T["impact"])
            if 0 < fall < 1:                                     # the last instant of the fall
                ry = lerp(-2300, -330, fall)
                p = P("#FF9A4D", 0.55, stroke=70)
                p.setBlendMode(PLUS)
                p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
                c.drawLine(0, ry - 1100, 0, ry - 300, p)
                draw_rocket(c, 0, ry, 180, t, heat=1.0)
            if hit >= 0:
                v2.smoke(c, 0, 20, t, T["impact"] + 0.2, T["impact"] + 9, rate=12, life=3.8, spread=(120, -300), rise=-80,
                         size=(50, 200), col="#6A7086", lit="#FF7A2F", lit_until=1.4, seed=11, drag=1.0)
                v2.fireball(c, 0, -40, t, T["impact"], 1.8, 440)
                v2.shock_ring(c, 0, -20, t, T["impact"], 0.75, 1500)
                v2.debris(c, 0, -30, t, T["impact"], 3.2, n=22, speed=1250, floor=0, seed=6)
                v2.embers(c, 0, -30, t, T["impact"], 1.8, n=70, speed=1500, seed=9)
                add_glow(c, 0, -60, 1700, "#FFE9C9", clamp(1 - hit * 5) * 0.95)
        # the launch crew
        if back and hit >= 0:
            pose, soot = "duck" if hit < 1.0 else "stand", clamp(hit * 3)
        elif t >= T["lands"] - 0.5:
            pose, soot = "point", 0.0
        elif t >= T["wait"]:
            pose, soot = "look", 0.0
        elif launched:
            pose, soot = "cheer", 0.0
        else:
            pose, soot = "stand", 0.0
        for i, (px, col) in enumerate(((392, "#F97316"), (438, "#3B82F6"), (486, "#F97316"))):
            engineer(c, px, 0, 118 + (i % 2) * 8, col, t + i * 0.37, pose if not (pose == "point" and i != 1) else "look", soot, face=-1)
        c.restore()
        # ---- the returning rocket, far away: a falling star with a tail
        if T["wait"] + 0.55 <= t < T["cut_fall"]:
            u = prog(t, T["wait"] + 0.55, T["cut_fall"] + 0.4)
            fx_, fy_ = lerp(690, 640, u), lerp(250, 560, e_in(u) * 0.8 + u * 0.2)
            ln = 60 + 260 * u
            p = lin_paint(fx_ + ln * 0.16, fy_ - ln, fx_, fy_, [("#FF9A4D", 0.0), ("#FFE9A8", 0.95)])
            p.setStrokeWidth(5 + 5 * u)
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setBlendMode(PLUS)
            c.drawLine(fx_ + ln * 0.16, fy_ - ln, fx_, fy_, p)
            add_glow(c, fx_, fy_, 30 + 60 * u, "#FFB05C", 0.9)
            c.drawCircle(fx_, fy_, 5 + 4 * u, P("#FFFFFF"))
            self.star_xy = (fx_, fy_)

    # ------------------------------------------------------------------ set 2: falling, close up
    def draw_fall(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.42, horizon_y=H * 1.5)
        v2.stars(c, W, H, t, 0.8, dy=-(t * 260))
        for i in range(5):                                       # cloud deck rushing up past the camera
            rng = random.Random(30 + i)
            sp = rng.uniform(1100, 1900)
            y = H + 400 - ((t - T["cut_fall"]) * sp + rng.uniform(0, 3000)) % 3200
            v2.cloud(c, rng.uniform(-60, W + 60), y, rng.uniform(1.3, 2.3), body="#1E1C45", rim="#8E4A6E", a=0.9, seed=i)
        v2.speed_streaks(c, W, H, t, 0.9, seed=3, n=34)
        u = prog(t, T["cut_fall"], T["cut_pad"])
        rx = W / 2 + math.sin(t * 2.1) * 10
        ry = lerp(700, 800, u) + math.sin(t * 3.3) * 8
        # the bullet it overtakes
        bu = prog(t, T["faster"] - 0.15, T["bullet"] + 0.55)
        if 0 < bu < 1:
            bx, by = W / 2 + 290, lerp(1250, 190, e_io(bu))
            c.save()
            c.translate(bx, by)
            c.scale(1.9, 1.9)
            c.translate(-bx, -by)
            pl = lin_paint(bx, by - 170, bx, by - 30, [("#FFFFFF", 0.0), ("#FFFFFF", 0.6)])
            pl.setStyle(skia.Paint.kStroke_Style)
            pl.setStrokeWidth(6)
            c.drawLine(bx, by - 170, bx, by - 30, pl)
            path = skia.Path()
            path.moveTo(bx - 13, by - 34)
            path.lineTo(bx + 13, by - 34)
            path.lineTo(bx + 13, by + 8)
            path.quadTo(bx + 11, by + 34, bx, by + 42)
            path.quadTo(bx - 11, by + 34, bx - 13, by + 8)
            path.close()
            cyl_path(c, path, bx - 13, bx + 13, "#D9A441", depth=1.2)
            c.drawRect(R(bx - 13, by - 34, 26, 6), P("#7A5A22", 0.8))
            c.restore()
        c.save()
        c.translate(rx, ry)
        c.rotate(math.sin(t * 2.7) * 2.5)
        draw_rocket(c, 0, 0, 180, t, heat=clamp((t - T["cut_fall"]) * 3), s=1.22)
        c.restore()
        self.fall_xy = (rx, ry)

    # ------------------------------------------------------------------ set 3: high up, the fix
    def draw_space(self, c, t):
        T = self.T
        braking = e_io(prog(t, T["relight"] + 0.1, T["brake"] + 0.9))
        v2.sky(c, W, H, 1.0)
        v2.stars(c, W, H, t, 1.0, n=320, seed=2, dy=-(t * lerp(90, 14, braking)))
        v2.earth_limb(c, W, H, 1.0, y=H * 0.80 - 30 * braking)
        v2.speed_streaks(c, W, H, t, 0.75 * (1 - 0.85 * braking), seed=9, n=30)
        ang = self.flip.at(t)
        burn = clamp((t - T["relight"]) * 5) * (0.82 + 0.18 * math.sin(t * 5))
        g0 = bump(t, T["gas"], T["flip"] + 0.25)                # first jet starts the turn
        g1 = bump(t, T["flip"] + 0.55, T["flip"] + 1.15)        # opposite jet stops it
        rx = W / 2 + math.sin(t * 1.3) * 6
        ry = lerp(700, 760, e_io(prog(t, T["cut_space"], T["end"] + 1.0))) + math.sin(t * 2.1) * 5
        if burn > 0:
            add_glow(c, rx, ry + 520, 520, "#FF8A3D", 0.30 * burn)
        draw_rocket(c, rx, ry, ang, t, flame=burn, gas=(g1, g0), warm=burn * 0.7, s=1.12, fl_len=560,
                    heat=clamp(1 - (t - T["cut_space"]) * 0.9) * 0.55 * (1 - prog(t, T["flip"], T["flip"] + 0.5)))
        self.space = (rx, ry, ang)

    # ------------------------------------------------------------------ UI on top of the finished picture
    def draw_ui(self, c, t):
        T = self.T
        m = self.mode(t)
        st = [0, 0, 0, 0]
        if t >= T["tail"]:
            st[0] = ("fix", T["tail"])
        elif t >= T["impact"]:
            st[0] = ("break", T["impact"])
        v2.hud(c, W, t, self.BUILD_NO, self.TITLE.get(self.lang, self.TITLE["en"]), st, a=prog(t, 0.15, 0.5), rtl=self.rtl)
        if m == "pad":
            p = prog(t, T["wait"] + 0.05, T["wait"] + 0.3) * (1 - prog(t, T["congrats"] + 0.5, T["congrats"] + 0.75))
            if p > 0:
                mins = int(lerp(1, 8, prog(t, T["wait"], T["congrats"] + 0.5)))
                v2.chip(c, W / 2, 470, f"T+ 0{mins}:00", p, accent=ACCENT)
            if hasattr(self, "star_xy") and T["lands"] - 0.5 <= t < T["cut_fall"]:
                fx_, fy_ = self.star_xy
                v2.callout(c, fx_, fy_, fx_ - 300, fy_ + 150, "YOUR ROCKET", prog(t, T["lands"] - 0.5, T["lands"] - 0.15), HILITE, t=t)
            if t >= T["impact"]:
                v2.badge(c, W / 2 + 300, 520, prog(t, T["impact"] + 0.25, T["impact"] + 0.5) * (1 - prog(t, T["cut_space"] - 0.3, T["cut_space"] - 0.1)), "alert", t, 1.25)
                red = clamp(1 - (t - T["impact"]) * 0.45) * 0.8
                if red > 0:
                    p = rad_paint(W / 2, H / 2, H * 0.75, [(WARN, 0.0), (WARN, 0.0), (WARN, 0.5 * red)], [0.0, 0.55, 1.0])
                    c.drawRect(R(0, 0, W, H), p)
        elif m == "fall":
            rx, ry = getattr(self, "fall_xy", (W / 2, 750))
            v2.callout(c, rx, ry + 440, rx - 280, ry + 250, "NOSE FIRST", prog(t, T["nose"] - 0.05, T["nose"] + 0.3) * (1 - prog(t, T["faster"] + 0.1, T["faster"] + 0.3)), WARN, t=t)
        else:
            rx, ry, ang = getattr(self, "space", (W / 2, 720, 180))
            a_ = math.radians(ang)
            def pt(lx, ly):                                      # rocket-local point -> screen
                lx, ly = lx * 1.12, ly * 1.12
                return rx + lx * math.cos(a_) - ly * math.sin(a_), ry + lx * math.sin(a_) + ly * math.cos(a_)
            p = prog(t, T["gas"], T["gas"] + 0.3) * (1 - prog(t, T["flip"] + 0.10, T["flip"] + 0.30))
            gx, gy = pt(BW / 2 + 6, -BH / 2 + 35)
            v2.callout(c, gx, gy, 800, 1090 if ang > 90 else 300, "GAS THRUSTERS", p, ACCENT, t=t)
            p = prog(t, T["relight"] + 0.05, T["relight"] + 0.35) * (1 - prog(t, T["tail"] - 0.1, T["tail"] + 0.15))
            ex, ey = pt(-BW / 2 - 4, BH / 2 + 20)
            v2.callout(c, ex, ey, 250, ey + 10, "3 ENGINES RELIT", p, "#FFB05C", t=t)
            v2.badge(c, W / 2 + 310, 500, prog(t, T["tail"], T["tail"] + 0.3), "check", t, 1.25)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T = self.T
        ev = [(0.05, sfx.whoosh(0.6, True, 60), -10), (0.2, sfx.pop(61), -8)]
        ev += [(T["launch"] - 0.05, rumble(2.6), 0), (T["launch"], sfx.whoosh(1.2, True, 62), -4)]
        ev += [(T["wait"] + 0.05 + i * 0.16, sfx.tick(), -12) for i in range(5)]
        ev += [(T["lands"] - 0.5, sfx.pop(63), -6)]
        ev += [(T["cut_fall"] - 0.12, sfx.whoosh(0.4, True, 64), -3), (T["cut_fall"], rumble(2.2, 44), -7),
               (T["nose"] - 0.05, sfx.pop(65), -6), (T["faster"] - 0.1, sfx.whoosh(0.7, True, 66), -6)]
        ev += [(T["cut_pad"] - 0.12, sfx.whoosh(0.4, False, 67), -3), (T["impact"] - 0.2, sfx.whoosh(0.25, False, 68), -2),
               (T["impact"], boom(), 2), (T["impact"] + 0.3, sfx.alarm(3, 820), -10)]
        ev += [(T["cut_space"] - 0.12, sfx.whoosh(0.45, True, 69), -3), (T["gas"], gas_hiss(0.9), -4),
               (T["gas"], sfx.pop(70), -8), (T["flip"] + 0.55, gas_hiss(0.6, 43), -5),
               (T["relight"], rumble(2.4, 45), -5), (T["relight"], sfx.charge_up(0.5), -8), (T["relight"] + 0.05, sfx.pop(71), -8),
               (T["tail"], sfx.chime(), -4), (T["tail"], sfx.sparkle(0.7, 9, 72), -8)]
        return ev


NAME = "rocket"
EPISODE = Rocket
