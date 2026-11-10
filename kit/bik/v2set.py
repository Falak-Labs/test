"""Reusable set pieces, characters and sounds for the v2 look (see bik/v2.py and episodes/v2_base.py).

World convention: ground at y = 0, up is negative, one unit = one pixel at zoom 1.
"""
import math
import random

import numpy as np
import skia

from .core import clamp, lerp, prog, e_out, e_in, e_io, e_back
from .draw import C, P, R, text, text_width, mix, shade
from . import sfx, v2
from .v2 import (lin_paint, rad_paint, rr, vrect, cyl, cyl_path, box, add_glow, contact_shadow, light_cone, puff,
                 ACCENT, WARN, GOOD, HILITE, INK, PLUS)

STEEL = "#2B3248"
SHIRTS = ("#F97316", "#3B82F6", "#F97316")      # the crew: two orange vests and a blue one


def dash_paint(col, a=1.0, w=4, t=0.0, dash=18, gap=14):
    """Stroke paint with moving dashes (guide lines, paths)."""
    p = P(col, a, stroke=w)
    p.setPathEffect(skia.DashPathEffect.Make([dash, gap], -t * 60))
    return p


def hard_hat(c, x, y, rot=0.0, s=1.0, a=1.0):
    """A loose yellow hard hat (tossed in the air at the end of an episode)."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    hat = skia.Path()
    hat.moveTo(-20, 8)
    hat.cubicTo(-20, -22, 20, -22, 20, 8)
    hat.close()
    c.drawPath(hat, lin_paint(-20, 0, 20, 0, ["#FDE68A", "#FACC15", "#CA8A04"], None, a))
    c.drawRRect(rr(-25, 5, 50, 7, 3), P("#EAB308", a))
    c.restore()


def hats_in_the_air(c, xs, y, t, t0, height=230):
    """The crew throws its hard hats: loop from t0 on. xs: world x of each thrower, y: hand height."""
    if t < t0:
        return
    for i, hx in enumerate(xs):
        u = ((t - t0) * 0.9 + i * 0.23) % 1.0
        hard_hat(c, hx + math.sin(u * 6 + i) * 14, y - math.sin(u * math.pi) * height, u * 540 + i * 40)


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


def person(c, x, y, h, shirt, t, pose="stand", soot=0.0, face=1, hat="none", hair="#2B2530", skin="#E8B48A",
           pants="#1F2538", band=False, wet=0.0, a=1.0):
    """Small rounded character, feet at (x, y), h = height in world units (an adult is about 120-140).
    pose: stand | cheer | look | point | duck | walk | sit | carry (arms forward) | shrug.
    hat: "hard" (yellow hard hat) | "none" (hair) | "beanie" (dark, pulled low) | "cap".  band: reflective vest stripe.
    soot 0..1 darkens them, wet 0..1 adds drips.  face: 1 looks right, -1 left."""
    if a <= 0:
        return
    u = h / 140.0
    skin = mix(skin, "#2A2A30", soot * 0.7)
    shirt = mix(shirt, "#22242C", soot * 0.75)
    c.save()
    c.translate(x, y)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    if pose == "duck":
        c.scale(1, 0.64)
    if pose == "cheer":
        c.translate(0, -abs(math.sin(t * 9 + x)) * 10 * u)
    contact_shadow(c, 0, 0, 70 * u, 0.45, 12 * u)
    sw = math.sin(t * 9 + x * 0.05) * 9 * u if pose == "walk" else 0.0
    if pose == "sit":
        for dx in (-13, 3):
            box(c, dx * u, -40 * u, 30 * u * face if face > 0 else -30 * u, 11 * u, pants, r=5 * u)
            box(c, (dx + 26 * face) * u, -40 * u, 11 * u, 40 * u, pants, r=5 * u)
        c.translate(0, 12 * u)
    else:
        box(c, -13 * u + sw, -52 * u, 11 * u, 52 * u, pants, r=5 * u)
        box(c, 3 * u - sw, -52 * u, 11 * u, 52 * u, pants, r=5 * u)
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
    elif pose == "carry":
        for sd in (-1, 1):
            c.drawLine(sd * 12 * u, -96 * u, (sd * 8 + 38 * face) * u, -84 * u, arm)
    elif pose == "shrug":
        for sd in (-1, 1):
            c.drawLine(sd * 18 * u, -100 * u, sd * 40 * u, -104 * u, arm)
            c.drawLine(sd * 40 * u, -104 * u, sd * 46 * u, -122 * u, arm)
    else:
        for sd in (-1, 1):
            c.drawLine(sd * 18 * u, -98 * u, sd * 22 * u - sw * sd * 0.6, -58 * u, arm)
    box(c, -21 * u, -110 * u, 42 * u, 64 * u, shirt, r=15 * u)
    if band:
        vrect(c, -21 * u, -80 * u, 42 * u, 9 * u, [("#F8FAFC", 0.85 * (1 - soot)), ("#CBD5E1", 0.85 * (1 - soot))])
    tilt = -16 * face if pose in ("look", "point") else 0
    c.save()
    c.translate(0, -112 * u)
    c.rotate(tilt)
    c.drawCircle(0, -15 * u, 18 * u, rad_paint(-6 * u, -22 * u, 30 * u, [shade(skin, 0.15), skin, shade(skin, -0.25)]))
    dome = skia.Path()
    dome.moveTo(-20 * u, -18 * u)
    dome.cubicTo(-20 * u, -44 * u, 20 * u, -44 * u, 20 * u, -18 * u)
    dome.close()
    if hat == "hard":
        c.drawPath(dome, lin_paint(-20 * u, 0, 20 * u, 0, ["#FDE68A", "#FACC15", "#CA8A04"]))
        c.drawRRect(rr(-25 * u, -21 * u, 50 * u, 7 * u, 3 * u), P(mix("#EAB308", "#3A3A3A", soot * 0.5)))
    elif hat == "beanie":
        c.drawPath(dome, lin_paint(-20 * u, 0, 20 * u, 0, ["#3A4258", "#1F2538", "#11151F"]))
        c.drawRRect(rr(-21 * u, -22 * u, 42 * u, 9 * u, 4 * u), P("#11151F"))
    elif hat == "cap":
        c.drawPath(dome, lin_paint(-20 * u, 0, 20 * u, 0, [shade(shirt, 0.25), shirt, shade(shirt, -0.3)]))
        c.drawRRect(rr((0 if face > 0 else -32) * u, -21 * u, 32 * u, 6 * u, 3 * u), P(shade(shirt, -0.35)))
    else:
        c.drawPath(dome, lin_paint(-20 * u, 0, 20 * u, 0, [shade(hair, 0.2), hair, shade(hair, -0.3)]))
    c.restore()
    if wet > 0:
        for i, dx in enumerate((-16, 2, 15)):
            yy = -120 * u + ((t * 60 + i * 23) % 50) * u
            c.drawCircle(dx * u, yy, 3.2 * u, P("#9AD7FF", 0.85 * wet))
    if a < 1:
        c.restore()
    c.restore()


def engineer(c, x, y, h, shirt, t, pose="stand", soot=0.0, face=1, wet=0.0):
    """One of the crew: a small engineer in a yellow hard hat and a vest, feet at (x, y).
    pose: stand | cheer | look | point | duck | walk | sit | carry | shrug."""
    person(c, x, y, h, shirt, t, pose, soot, face, hat="hard", band=True, wet=wet)


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


def building_ghost(c, x, w, h, floors, a):
    """Dashed outline of a building, for scale."""
    if a <= 0:
        return
    p = P("#FFFFFF", 0.75 * a, stroke=4)
    p.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
    c.drawRect(R(x, -h, w, h), P("#93C5FD", 0.10 * a))
    c.drawRect(R(x, -h, w, h), p)
    for i in range(1, floors):
        yy = -h * i / floors
        c.drawRect(R(x + 6, yy - 1, w - 12, 2), P("#FFFFFF", 0.28 * a))
        for wx in range(int(x) + 22, int(x + w) - 20, 38):
            c.drawRect(R(wx, yy + 12, 18, h / floors - 26), P("#FFE29A", 0.20 * a))


def sea(c, x0, x1, t, moon_x=None, depth=2600):
    """Night sea from the surface (y = 0) down: gradient, moon path, drifting crests."""
    vrect(c, x0, 0, x1 - x0, depth, ["#16295A", "#0C1738", "#060A1C", "#03040C"], [0.0, 0.10, 0.35, 1.0])
    rng = random.Random(17)
    if moon_x is not None:
        for i in range(26):
            yy = 6 + i * 13 + rng.uniform(-3, 3)
            ww = (30 + i * 9) * (0.6 + 0.4 * math.sin(t * 2.2 + i))
            c.drawRRect(rr(moon_x - ww / 2 + math.sin(t * 1.3 + i * 0.7) * 10, yy, ww, 5, 2.5), P("#DCE6FF", 0.62 * (1 - i / 30)))
        add_glow(c, moon_x, 40, 420, "#9DB7FF", 0.16)
    for k in range(5):
        yy = 14 + k * 46
        path = skia.Path()
        path.moveTo(x0, yy)
        xx = x0
        while xx < x1:
            xx += 40
            path.lineTo(xx, yy + math.sin(xx * 0.012 + t * (1.2 + k * 0.25) + k) * (5 + k))
        c.drawPath(path, P("#7DA2E8", 0.22 - k * 0.035, stroke=3))


def heart(c, x, y, s, a, col="#FB7185"):
    if a <= 0:
        return
    path = skia.Path()
    path.moveTo(0, 30)
    path.cubicTo(-70, -20, -30, -70, 0, -32)
    path.cubicTo(30, -70, 70, -20, 0, 30)
    path.close()
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    add_glow(c, 0, -10, 110, col, 0.5 * a)
    c.drawPath(path, lin_paint(0, -60, 0, 30, [shade(col, 0.25), col, shade(col, -0.2)], None, a))
    c.restore()


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


# ---------------------------------------------------------------------------------------------- more sets
def skyline_night(c, x0, x1, base_y=0.0, seed=3, hmin=220, hmax=900, cols=("#1A1F45", "#242A5C", "#15193A"), lit=0.33, t=0.0):
    """Row of city buildings standing on base_y, with lit windows and a few roof beacons."""
    rng = random.Random(seed)
    x = x0
    while x < x1:
        w, h = rng.randint(90, 240), rng.randint(hmin, hmax)
        body = rng.choice(cols)
        vrect(c, x, base_y - h, w, h, [shade(body, 0.12), body, shade(body, -0.28)], [0.0, 0.3, 1.0])
        c.drawRect(R(x, base_y - h, 4, h), P("#FFFFFF", 0.06))
        wr = random.Random(int(x) * 7 + seed)
        for wy in range(int(base_y - h) + 22, int(base_y) - 20, 34):
            for wx in range(int(x) + 12, int(x + w) - 16, 26):
                if wr.random() < lit:
                    c.drawRect(R(wx, wy, 12, 16), P(wr.choice(["#FFD98A", "#FFE9C9", "#9AD7FF", "#FFB37A"]), 0.85))
        if rng.random() < 0.3:
            beacon(c, x + w / 2, base_y - h - 12, t, hz=0.6 + rng.random(), r=4, ph=rng.random())
        x += w + rng.randint(6, 50)


def window_night(c, x, y, w, h, t=0.0, frame="#141829", moon=True, seed=2):
    """A window in a wall showing the night sky."""
    c.drawRRect(rr(x - 8, y - 8, w + 16, h + 16, 8), P(frame))
    c.save()
    c.clipRect(R(x, y, w, h))
    vrect(c, x, y, w, h, ["#0B1030", "#2B2466", "#74406F"], [0.0, 0.6, 1.0])
    rng = random.Random(seed)
    for _ in range(int(w * h / 2600)):
        c.drawCircle(x + rng.uniform(0, w), y + rng.uniform(0, h * 0.8), rng.uniform(0.8, 2.0), P("#FFFFFF", 0.5 + 0.4 * math.sin(t * 2 + rng.random() * 6)))
    if moon:
        v2.moon(c, x + w * 0.7, y + h * 0.3, min(w, h) * 0.12)
    c.restore()
    c.drawRect(R(x + w / 2 - 3, y, 6, h), P(frame))
    c.drawRect(R(x, y + h / 2 - 3, w, 6), P(frame))
    vrect(c, x, y, w, h, [("#FFFFFF", 0.07), ("#FFFFFF", 0.0)])


def room(c, x, y, w, h, wall="#2A2F4A", floor="#3B4160", t=0.0, lamp=True, lamp_x=None, window=None, panels=140):
    """Interior seen from the side: back wall (x, y, w, h) lit from above, floor slab under it (floor line = y + h),
    optional hanging lamp with a cone of light, optional window=(wx, wy, ww, wh)."""
    vrect(c, x, y, w, h, [shade(wall, 0.14), wall, shade(wall, -0.24)], [0.0, 0.4, 1.0])
    if panels:
        for px in range(int(x) + panels, int(x + w), panels):
            c.drawRect(R(px, y, 2, h), P("#000000", 0.10))
    if window:
        window_night(c, *window, t=t)
    vrect(c, x, y + h - 70, w, 70, [("#000000", 0.0), ("#000000", 0.28)])
    box(c, x, y + h, w, 26, floor)
    c.drawRect(R(x, y + h, w, 3), P("#FFFFFF", 0.14))
    if lamp:
        lx = x + w * 0.5 if lamp_x is None else lamp_x
        c.drawRect(R(lx - 2, y, 4, 46), P("#11151F"))
        shade_ = skia.Path()
        shade_.moveTo(lx - 34, y + 74)
        shade_.lineTo(lx - 16, y + 46)
        shade_.lineTo(lx + 16, y + 46)
        shade_.lineTo(lx + 34, y + 74)
        shade_.close()
        c.drawPath(shade_, lin_paint(lx - 34, 0, lx + 34, 0, ["#4A5270", "#2B3248", "#161A2B"]))
        light_cone(c, lx, y + 72, 90, h * 1.05, 62, "#FFE9B8", 0.22)
        add_glow(c, lx, y + 78, 90, "#FFE9B8", 0.85)
        c.drawCircle(lx, y + 76, 8, P("#FFF7DA"))


def underwater(c, W, H, t, top="#0F4468", mid="#0A2540", bottom="#040C1C", rays=True, seed=5, surface_y=None):
    """Screen-space underwater backdrop: depth gradient, slow light shafts from above, drifting specks.
    surface_y: screen y of the water surface if it is in frame (the sky above it is left untouched)."""
    y0 = 0 if surface_y is None else surface_y
    vrect(c, 0, y0, W, H - y0, [top, mid, bottom], [0.0, 0.45, 1.0])
    if rays:
        for i in range(5):
            x = (W * (0.1 + 0.2 * i) + math.sin(t * 0.3 + i) * 60)
            light_cone(c, x, y0 - 40, 90 + math.sin(t * 0.2 + i * 2) * 6 + (i - 2) * 5, H * 0.95, 9 + (i % 2) * 5, "#9AE6FF", 0.11)
    rng = random.Random(seed)
    for _ in range(70):
        px = (rng.uniform(0, W) + t * rng.uniform(-14, 14)) % W
        py = y0 + (rng.uniform(0, H - y0) - t * rng.uniform(4, 16)) % max(1.0, H - y0)
        c.drawCircle(px, py, rng.uniform(1.0, 2.6), P("#CFF3FF", rng.uniform(0.10, 0.34)))


def bubbles(c, x, y, t, t0=0.0, t1=None, rate=9, life=2.4, spread=34, rise=240, size=(4, 13), seed=3, a=0.8):
    """Stream of bubbles rising from (x, y) between t0 and t1."""
    if t < t0:
        return
    t1 = t if t1 is None else t1
    n0, n1 = max(0, int((t - life - t0) * rate)), int((min(t, t1) - t0) * rate) + 1
    for i in range(n0, n1):
        age = t - (t0 + i / rate)
        if not 0 <= age <= life:
            continue
        rng = random.Random(seed * 977 + i)
        u = age / life
        bx = x + rng.uniform(-spread, spread) * (0.3 + u) + math.sin(age * 5 + i) * 6
        by = y - rise * age * (0.7 + 0.3 * rng.random())
        r = lerp(size[0], size[1], rng.random()) * (0.7 + 0.5 * u)
        al = a * clamp(u * 8) * (1 - u) ** 0.6
        c.drawCircle(bx, by, r, P("#BFEFFF", 0.20 * al))
        c.drawCircle(bx, by, r, P("#E6FAFF", 0.85 * al, stroke=max(1.2, r * 0.18)))
        c.drawCircle(bx - r * 0.3, by - r * 0.3, r * 0.22, P("#FFFFFF", 0.9 * al))


def splash(c, x, y, t, t0, dur=0.9, n=22, speed=560, col="#BDE6FF", seed=4, gravity=1500, width=1.0):
    """Water splash: droplets thrown up from (x, y) at t0, plus a spreading ring on the surface."""
    age = t - t0
    if not 0 <= age <= dur:
        return
    u = age / dur
    rng = random.Random(seed)
    for _ in range(n):
        ang = math.radians(rng.uniform(205, 335))
        sp = speed * rng.uniform(0.35, 1.0)
        px = x + math.cos(ang) * sp * age * width
        py = y + math.sin(ang) * sp * age + 0.5 * gravity * age * age
        if py > y + 4:
            continue
        c.drawCircle(px, py, rng.uniform(3, 8) * (1 - u * 0.5), P(col, 0.9 * (1 - u)))
    c.save()
    c.translate(x, y)
    c.scale(1, 0.22)
    c.drawCircle(0, 0, 30 + 190 * e_out(u) * width, P("#FFFFFF", 0.7 * (1 - u), stroke=10 * (1 - u * 0.6)))
    c.restore()


def sparks_shower(c, x, y, t, t0, dur=0.8, n=26, speed=700, seed=6, col="#FFD27A", cone=(200, 340)):
    """Short burst of sparks (cutting, short circuits, grinding). Thin wrapper over v2.embers."""
    v2.embers(c, x, y, t, t0, dur, n=n, speed=speed, seed=seed, gravity=1100, col=col, size=4.0, cone=cone)
