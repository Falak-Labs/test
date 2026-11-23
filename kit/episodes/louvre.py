"""Episode 70 - the Louvre Abu Dhabi and its dome that rains light.  v2 look: the museum in elevation on the sea
(1 m = 4 units, sea level y = 0): white galleries on a low stone platform, the flat dome (180 m = 720 units) floating
over them on four hidden legs, its star lattice letting spots of sun fall through onto the plaza.

Sets: sea (hook: close under the dome, sun spots raining on the plaza and the people, out to the whole dome over the sea
at golden hour; break1: no dome, the noon sun, an egg frying on the stone; fix1: the dome comes down and its shade cools
the plaza, 180 m; break2: solid, everything goes dark, phone torches and a bat; fix2 (second half): the light rains
through again, a palm-leaf inset; break3: a forest of columns; fix3: the columns go, four legs in x-ray inside the
buildings; stat: dusk; closer: blue hour, the dome lit from below), plan (fix2: top view, eight layers of stars laid one
by one; reveal: a palm grove from above turns into the dome, then the galleries below like an old Arab town), pit
(break4: the sea seeps into the basement; fix4: a dry pit behind steel walls, the basement sealed in a yellow tub, the
sea let in around it), beach (tag: dad drags the umbrella after its shade all day).
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of, GOLDEN, NIGHTP, saudi_man  # noqa: E402
from windtower import sun, heat_lines  # noqa: E402
from pyramid import palm  # noqa: E402
from tent import umbrella  # noqa: E402

NOONP = {"top": "#0E2F5E", "upper": "#1B4F8F", "mid": "#2F6DB0", "low": "#5E97CF", "horizon": "#8DBDE3",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DUSKP = {"top": "#0A0F2E", "upper": "#24215C", "mid": "#5B3A7A", "low": "#D0705E", "horizon": "#F6A86A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
BLUEP = {"top": "#030616", "upper": "#0A1640", "mid": "#173070", "low": "#2C4C8E", "horizon": "#5A7AB8",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SEA_C, SEA_D = "#1E8AA0", "#0B3A5A"
STONE = "#EFE8DA"
WHITE_B = ("#FBF8F1", "#E4DDCF", "#CFC6B4")       # gallery walls: lit, front, shade
RX = 360.0                                        # dome radius (90 m)
PLAZA = -12.0                                     # platform top
LEGS_X = (-216.0, 216.0)
# galleries under the dome: (x0, width, height)
BLD = [(-372, 60, 34), (-306, 70, 48), (-246, 60, 90), (-176, 80, 40), (-90, 64, 86), (-20, 52, 60), (38, 90, 96),
       (134, 48, 52), (186, 60, 90), (252, 70, 48), (330, 46, 30)]


def d_top(x):
    u = clamp(1 - (x / RX) ** 2)
    return -60 - 110 * u


def d_bot(x):
    u = clamp(1 - (x / RX) ** 2)
    return -54 - 82 * u


def dome_path(dy=0.0):
    p = skia.Path()
    xs = [lerp(-RX, RX, i / 48) for i in range(49)]
    p.moveTo(xs[0], d_top(xs[0]) + dy)
    for x in xs[1:]:
        p.lineTo(x, d_top(x) + dy)
    for x in reversed(xs):
        p.lineTo(x, d_bot(x) + dy)
    p.close()
    return p


def under_path(dy=0.0):
    """The space under the dome down to the plaza (for the shade)."""
    p = skia.Path()
    xs = [lerp(-RX, RX, i / 48) for i in range(49)]
    p.moveTo(-RX, PLAZA)
    for x in xs:
        p.lineTo(x, d_bot(x) + dy)
    p.lineTo(RX, PLAZA)
    p.close()
    return p


def star8(x, y, r, rot=0.0, inner=0.72):
    """An eight-pointed star (two squares) as one closed path."""
    p = skia.Path()
    for i in range(16):
        q = rot + i * math.pi / 8
        rr_ = r if i % 2 == 0 else r * inner
        px, py = x + math.cos(q) * rr_, y + math.sin(q) * rr_
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    return p


def floor_y(x):
    """Where a beam lands: the roof of the gallery under x, else the plaza."""
    for x0, w, h in BLD:
        if x0 <= x <= x0 + w:
            return PLAZA - h
    return PLAZA


HOLES = []
_rng = random.Random(70)
for _i in range(34):
    _x = _rng.uniform(-RX * 0.9, RX * 0.9)
    HOLES.append((_x, _rng.uniform(0.6, 1.3), _rng.uniform(0, 6.28)))
SPARK = []
_rng = random.Random(71)
for _i in range(220):
    _x = _rng.uniform(-RX * 0.97, RX * 0.97)
    _u = _rng.uniform(0.15, 0.95)
    SPARK.append((_x, lerp(d_bot(_x), d_top(_x), _u), _rng.uniform(1.2, 2.6), _rng.uniform(0, 6.28)))


def galleries(c, t, shade=0.0, night=0.0, xray=0.0, a=1.0):
    """The platform and the white galleries (world)."""
    c.drawRect(R(-400, PLAZA, 800, 14), lin_paint(0, PLAZA, 0, 2, [mix(STONE, "#D9B98A", night), mix("#B9AE98", "#6B5236", night)], a=a))
    for x0, w, h in BLD:
        legb = any(x0 <= lx <= x0 + w for lx in LEGS_X)
        al = a * (1 - 0.65 * xray) if legb else a
        top = PLAZA - h
        c.drawRect(R(x0, top, w, h), lin_paint(x0, 0, x0 + w, 0, [mix(WHITE_B[0], "#F3D9A8", night), mix(WHITE_B[1], "#C9A877", night)], a=al))
        c.drawRect(R(x0, top, w, 4), P(mix("#FFFFFF", "#FFE7B8", night), al))
        c.drawRect(R(x0 + w - 6, top, 6, h), P(mix(WHITE_B[2], "#8A6A48", night), al))
        if w > 50:                                                         # a door / a slot window
            c.drawRect(R(x0 + w * 0.3, PLAZA - 22, 12, 22), P(mix("#5B5246", "#FFD58A", night), 0.85 * al))
        if night > 0:
            c.drawRect(R(x0 + 6, top + 8, w - 18, 3), P("#FFD58A", 0.5 * night * al))
    if shade > 0:                                                          # the dome's shade over everything under it
        c.drawPath(under_path(), P("#0B1220", 0.42 * shade * a))


def legs(c, t, k, a=1.0):
    """The four hidden legs in x-ray (two in front, two behind them)."""
    if k <= 0:
        return
    for lx in LEGS_X:
        top = d_bot(lx)
        for dx, al, dash in ((12, 0.55, True), (0, 1.0, False)):
            x = lx + dx
            pp = path_of([(x - 13, PLAZA), (x + 13, PLAZA), (x + 8, top + 2), (x - 8, top + 2)], close=True)
            if dash:
                c.drawPath(pp, dash_paint("#FDE68A", k * al * a, w=3, t=t))
            else:
                c.drawPath(pp, P("#FACC15", 0.75 * k * a))
                c.drawPath(pp, P("#FFF7D6", k * a, stroke=5))
        add_glow(c, lx, (top + PLAZA) / 2, 70, "#FDE68A", 0.55 * k * a)


def columns(c, t, up, a=1.0):
    """A forest of columns under the dome; up 0..1 (each column with its own delay)."""
    if up <= 0:
        return
    rng = random.Random(5)
    x = -330.0
    while x <= 330:
        k = e_out(clamp(up * 1.6 - rng.uniform(0, 0.6)))
        if k > 0:
            top = lerp(PLAZA, d_bot(x), k)
            c.drawRect(R(x - 4, top, 8, PLAZA - top), lin_paint(x - 4, 0, x + 4, 0, ["#D6D3D1", "#9CA3AF"], a=a))
        x += 26


def dome(c, t, dy=0.0, solid=0.0, night=0.0, a=1.0, glow=0.0):
    """The dome (world): dark lens seen from below, its star lattice twinkling; solid 1 = no holes."""
    if a <= 0:
        return
    p = dome_path(dy)
    body = [mix("#7C8494", "#2A3350", night), mix("#3B4252", "#161C30", night), mix("#1F2533", "#0B1020", night)]
    c.drawPath(p, lin_paint(0, -170 + dy, 0, -54 + dy, body, a=a))
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    for k in range(-14, 15):                                               # the lattice ribs
        x = k * 26
        c.drawLine(x - 20, -200 + dy, x + 20, -40 + dy, P("#9CA3AF", 0.18 * a, stroke=2))
        c.drawLine(x + 20, -200 + dy, x - 20, -40 + dy, P("#9CA3AF", 0.18 * a, stroke=2))
    holes = (1 - solid) * a
    if holes > 0:
        for x, y, r, ph in SPARK:
            tw = 0.55 + 0.45 * math.sin(t * 2.2 + ph)
            col = "#FFE7A8" if night < 0.5 else "#FFD58A"
            c.drawPath(star8(x, y + dy, r * (1.3 + glow), ph), P(col, holes * tw))
    c.restore()
    c.drawPath(path_of([(x_, d_top(x_) + dy) for x_ in [lerp(-RX, RX, i / 48) for i in range(49)]]),
               P(mix("#F8E7C0", "#6B7AA8", night), 0.9 * a, stroke=3))             # the sunlit top edge
    if glow > 0:
        add_glow(c, 0, -110 + dy, 380, "#FFD58A", 0.25 * glow * a)


def beams(c, t, k, sun_dx=-0.32, a=1.0, warm=0.0):
    """Shafts of sun falling through the dome's holes and the spots they make (world, PLUS)."""
    if k <= 0:
        return
    for i, (x, w, ph) in enumerate(HOLES):
        y0 = d_bot(x)
        x1 = x + sun_dx * (PLAZA - y0)
        y1 = floor_y(x1)
        x1 = x + sun_dx * (y1 - y0)
        fl = (0.7 + 0.3 * math.sin(t * 1.7 + ph)) * k * a
        col = mix("#FFF3C4", "#FFB870", warm)
        bp = path_of([(x - 2.5 * w, y0), (x + 2.5 * w, y0), (x1 + 5 * w, y1), (x1 - 5 * w, y1)], close=True)
        pa = P(col, 0.16 * fl)
        pa.setBlendMode(PLUS)
        c.drawPath(bp, pa)
        sp = P(col, 0.85 * fl)
        sp.setBlendMode(PLUS)
        c.drawOval(R(x1 - 7 * w, y1 - 2.2, 14 * w, 4.4), sp)
        add_glow(c, x1, y1, 16 * w, col, 0.35 * fl)
        for j in range(3):                                                 # the "rain": specks falling down the shaft
            u = (t * 0.9 + j / 3 + ph) % 1.0
            dp = P("#FFFFFF", 0.7 * fl * math.sin(math.pi * u))
            dp.setBlendMode(PLUS)
            c.drawCircle(lerp(x, x1, u), lerp(y0, y1, u), 1.6, dp)


def far_city(c, t, night=0.0, a=1.0):
    """Abu Dhabi's skyline on the far shore (world, base y = -30)."""
    rng = random.Random(8)
    x = -1300.0
    while x < 1300:
        w = rng.uniform(16, 40)
        h = rng.uniform(16, 90) * (1.4 if abs(x) > 500 else 1.0)
        col = mix("#7A8AA8", "#1A2246", night)
        c.drawRect(R(x, -30 - h, w, h), P(col, 0.75 * a))
        if night > 0.3:
            for q in range(int(h / 10)):
                if rng.random() < 0.45:
                    c.drawRect(R(x + 3, -30 - h + 4 + q * 10, w - 6, 2.5), P("#FFD58A", 0.55 * night * a))
        x += w + rng.uniform(6, 30)


def water(c, t, night=0.0, refl=1.0, dome_a=1.0, a=1.0):
    """The sea: a thin band behind the platform and the sea in front with the dome's reflection (world)."""
    c.drawRect(R(-2000, -30, 4000, 30), lin_paint(0, -30, 0, 0, [mix("#7CC4D0", "#1B2A55", night), mix(SEA_C, "#122048", night)], a=a))
    c.drawRect(R(-2000, 0, 4000, 1400), lin_paint(0, 0, 0, 900, [mix(SEA_C, "#102050", night), mix(SEA_D, "#050A1C", night)], a=a))
    if refl > 0 and dome_a > 0:                                            # the dome upside down in the water
        c.save()
        c.translate(0, 8)
        c.scale(1, -0.62)
        c.drawPath(dome_path(), P(mix("#0B2A40", "#3A3020", night), 0.5 * refl * dome_a * a))
        for x, y, r, ph in SPARK[::3]:
            tw = 0.4 + 0.6 * max(0.0, math.sin(t * 3.1 + ph))
            gp = P(mix("#FFE7A8", "#FFC470", night), 0.5 * tw * refl * dome_a * a)
            gp.setBlendMode(PLUS)
            c.drawRect(R(x - 3, y - 1, 6, 5), gp)
        c.restore()
        for x0, w, h in BLD:                                               # the white galleries mirrored
            c.drawRect(R(x0, 4, w, h * 0.55), P(mix("#E9E3D6", "#F3D9A8", night), 0.16 * refl * a))
    for k in range(9):
        yy = 10 + k * 22
        p = skia.Path()
        p.moveTo(-1200, yy)
        xx = -1200.0
        while xx < 1200:
            xx += 30
            p.lineTo(xx, yy + math.sin(xx * 0.02 + t * (1.3 + k * 0.2) + k) * (2 + k * 0.5))
        c.drawPath(p, P(mix("#CFF6FF", "#8FA8E8", night), (0.32 - k * 0.03) * a, stroke=2))


def egg_inset(c, x, y, r, t, k, a=1.0):
    """A round inset: an egg frying on the hot stone (screen)."""
    if a <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(x, y, r)
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    c.drawCircle(x, y, r, lin_paint(x - r, y - r, x + r, y + r, ["#C9AE7E", "#9C7E50"], a=a))
    for i in range(6):
        c.drawLine(x - r, y - r + i * 70, x + r, y - r + i * 70 + 40, P("#7A5E36", 0.7 * a, stroke=4))
    s = e_back(clamp(k * 1.4))
    wp = skia.Path()
    for i in range(24):
        q = i / 24 * 2 * math.pi
        rr_ = r * 0.55 * s * (1 + 0.12 * math.sin(q * 3 + 1) + 0.06 * math.sin(q * 7))
        px, py = x + math.cos(q) * rr_, y + 10 + math.sin(q) * rr_ * 0.8
        wp.moveTo(px, py) if i == 0 else wp.lineTo(px, py)
    wp.close()
    c.drawPath(wp, P("#FFFFFF", a))
    c.drawPath(wp, P("#D6C7A6", 0.9 * a, stroke=4))
    c.drawCircle(x - 6, y, r * 0.2 * s, rad_paint(x - 14, y - 8, r * 0.25, ["#FFE08A", "#F59E0B"], a=a))
    for i in range(7):                                                     # sizzle bubbles
        q = t * 3 + i
        bx = x + math.cos(i * 2.1) * r * 0.45 * s
        by = y + 10 + math.sin(i * 2.1) * r * 0.32 * s
        c.drawCircle(bx, by, 4 + 3 * abs(math.sin(q)), P("#FFFFFF", 0.7 * a * k, stroke=2))
    heat_lines(c, x - r * 0.6, x + r * 0.6, y - r * 0.8, y - r * 0.1, t, a=0.8 * a * k)
    c.restore()
    c.drawCircle(x, y, r, P("#F8FAFC", a, stroke=8))


def palm_inset(c, x, y, r, t, a=1.0):
    """A round inset: the sun through palm fronds (screen)."""
    if a <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(x, y, r)
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    c.drawCircle(x, y, r, rad_paint(x + r * 0.3, y - r * 0.3, r * 1.6, ["#FFF7D6", "#FFD27A", "#C98A3A"], [0.0, 0.4, 1.0], a=a))
    for k in range(9):
        an = math.radians(-180 + k * 26 + math.sin(t * 1.2 + k) * 3)
        lf = skia.Path()
        bx, by = x - r * 0.9, y + r * 0.9
        tx, ty = bx + math.cos(an + 0.9) * r * 2.0, by + math.sin(an + 0.9) * r * 2.0
        lf.moveTo(bx, by)
        lf.quadTo((bx + tx) / 2 + 30, (by + ty) / 2 - 30, tx, ty)
        c.drawPath(lf, P("#24401F", a, stroke=10))
        for j in range(14):
            u = 0.15 + j / 16
            px = bx + (tx - bx) * u
            py = by + (ty - by) * u
            c.drawLine(px, py, px + math.cos(an + 2.2) * 46, py + math.sin(an + 2.2) * 46, P("#2F5A28", a, stroke=6))
            c.drawLine(px, py, px + math.cos(an - 0.4) * 46, py + math.sin(an - 0.4) * 46, P("#2F5A28", a, stroke=6))
    c.restore()
    c.drawCircle(x, y, r, P("#F8FAFC", a, stroke=8))


def star_layers(c, cx, cy, Rr, n, t, a=1.0, light=1.0):
    """Top view of the dome: a sunlit disc covered by n of its 8 layers of star lattices (screen)."""
    if a <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(cx, cy, Rr)
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    c.drawCircle(cx, cy, Rr, rad_paint(cx, cy, Rr, [mix("#FFFBEA", "#1F2937", 1 - light), mix("#FFD27A", "#111827", 1 - light)], a=a))
    for k in range(int(math.ceil(n))):
        part = clamp(n - k)
        d = 70 + 17 * k
        rot = math.radians(k * 11.25 + 7)
        col = ("#94A3B8", "#64748B", "#7C8798", "#475569")[k % 4]
        c.save()
        c.translate(cx, cy)
        c.rotate(math.degrees(rot))
        rng = int(Rr / d) + 2
        pa = P(col, a * part, stroke=9 + k * 0.8)
        pa.setStrokeJoin(skia.Paint.kMiter_Join)
        for gx in range(-rng, rng + 1):
            for gy in range(-rng, rng + 1):
                px, py = gx * d + (d / 2 if gy % 2 else 0), gy * d * 0.87
                if px * px + py * py < (Rr + d) ** 2:
                    c.drawPath(star8(px, py, d * 0.42, math.pi / 8), pa)
        c.restore()
    c.restore()
    c.drawCircle(cx, cy, Rr, P("#CBD5E1", a, stroke=14))
    c.drawCircle(cx, cy, Rr - 9, P("#64748B", a, stroke=3))


def palm_top(c, x, y, r, t, a=1.0, seed=0):
    """A date palm seen from above (screen)."""
    rng = random.Random(seed)
    for k in range(11):
        an = k * 2 * math.pi / 11 + rng.uniform(-0.15, 0.15) + math.sin(t * 0.8 + k) * 0.02
        tx, ty = x + math.cos(an) * r, y + math.sin(an) * r
        c.drawLine(x, y, tx, ty, P("#1E3A1A", a, stroke=r * 0.16))
        for j in range(1, 7):
            u = j / 7
            px, py = lerp(x, tx, u), lerp(y, ty, u)
            ln = r * 0.22 * (1 - u * 0.5)
            c.drawLine(px, py, px + math.cos(an + 1.0) * ln, py + math.sin(an + 1.0) * ln, P("#2E5A26", a, stroke=5))
            c.drawLine(px, py, px + math.cos(an - 1.0) * ln, py + math.sin(an - 1.0) * ln, P("#2E5A26", a, stroke=5))
    c.drawCircle(x, y, r * 0.12, P("#6B4A2A", a))


def town_plan(c, cx, cy, Rr, k, t, a=1.0):
    """The galleries from above, laid out like an old town: white blocks, narrow lanes, a water channel (screen)."""
    if a <= 0 or k <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(cx, cy, Rr * 1.05)
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    c.drawCircle(cx, cy, Rr * 1.05, P("#C9B48E", a * clamp(k * 2)))
    rng = random.Random(55)
    blocks = []
    for gy in range(-5, 6):
        for gx in range(-5, 6):
            bx = cx + gx * 78 + rng.uniform(-10, 10)
            by = cy + gy * 78 + rng.uniform(-10, 10)
            if (bx - cx) ** 2 + (by - cy) ** 2 < (Rr * 0.95) ** 2 and not (abs(gy) == 0 and abs(gx) < 4):
                blocks.append((bx, by, rng.uniform(46, 66), rng.uniform(46, 66), rng.random()))
    blocks.sort(key=lambda b: b[4])
    shown = int(len(blocks) * clamp(k * 1.2))
    for i, (bx, by, w, h, _) in enumerate(blocks[:shown]):
        c.drawRect(R(bx - w / 2 + 8, by - h / 2 + 8, w, h), P("#8C7F68", 0.8 * a))
        c.drawRect(R(bx - w / 2, by - h / 2, w, h), P("#FFFFFF", a))
        c.drawRect(R(bx - w / 2, by - h / 2, w, h), P("#A89C84", a, stroke=3))
    ch = skia.Path()                                                       # the water channel through the middle
    ch.moveTo(cx - Rr, cy + 6)
    ch.cubicTo(cx - Rr * 0.4, cy - 30, cx + Rr * 0.3, cy + 40, cx + Rr, cy - 4)
    c.drawPath(ch, P("#38BDF8", a * clamp(k * 2 - 0.4), stroke=26))
    c.restore()


def sheet_piles(c, x, y0, y1, a=1.0):
    for k in range(6):
        c.drawRect(R(x - 18 + k * 6, y0, 6, y1 - y0), P("#475569" if k % 2 else "#64748B", a))


def painting(c, x, y, w, h, seed, a=1.0, wet=0.0):
    rng = random.Random(seed)
    c.drawRect(R(x - 4, y - 4, w + 8, h + 8), P("#B45309", a))
    c.drawRect(R(x, y, w, h), P(mix(rng.choice(["#1E3A8A", "#7C2D12", "#14532D", "#831843"]), "#64748B", wet), a))
    c.drawCircle(x + w * 0.6, y + h * 0.4, min(w, h) * 0.22, P(rng.choice(["#FDE68A", "#FCA5A5", "#BFDBFE"]), a))


# ====================================================================================== the episode
class Louvre(EpisodeV2):
    BUILD_NO = 70
    FIRST_SET = "sea"
    CLEAR = "#0B1220"
    TITLE = {"en": "LOUVRE ABU DHABI", "ar_sa": "اللوفر أبوظبي"}
    EMPH = {"en": ["CONGRATS", "DOME", "HEAVY", "EIFFEL", "SEA", "LIGHT", "RAIN", "LOUVRE", "ABU", "DHABI", "YOURSELF",
                   "SUN", "FRYING", "PAN", "SHADE", "HUNDRED", "EIGHTY", "SOLID", "DARK", "CAVE", "STARS", "SEVEN",
                   "PALM", "LEAVES", "FOREST", "COLUMNS", "FOUR", "LEGS", "HIDDEN", "FLOAT", "BASEMENTS", "WATER", "DRY",
                   "PIT", "SEAL", "BATHTUB", "FOLLOW", "VACUUM", "NOUVEL", "GROVE", "ARAB", "TOWN", "THOUSAND", "EIGHT",
                   "LAYERS", "FIFTY", "FIVE", "BEACH", "DAD", "UMBRELLA", "CHASING"],
            "ar_sa": ["مبروك", "قبة", "إيفل", "البحر", "الشمس", "تمطر", "اللوفر", "أبوظبي", "بيدك", "فرن", "بقبة", "مية",
                      "وثمانين", "فتحات", "كهف", "مظلم", "آلاف", "نجمة", "النخل", "غابة", "أعمدة", "أربع", "رجول", "مخبّاة",
                      "طايرة", "القبو", "الموية", "حفرة", "ناشفة", "بانيو", "تابعني", "مكنسة", "نوفيل", "حارة", "طن",
                      "طبقات", "مبنى", "ملعبين", "أبوك", "الشمسية", "الظل"]}
    KEYS = {"ar_sa": {
        ("hook", "SEA"): "البحر", ("hook", "DOME"): "قبة", ("hook", "HEAVY"): "بوزن", ("hook", "EIFFEL"): "إيفل",
        ("hook", "LIGHT"): "الشمس", ("hook", "RAIN"): "تمطر", ("hook", "CONGRATS"): "مبروك", ("hook", "LOUVRE"): "اللوفر",
        ("break1", "SUN"): "شمس", ("break1", "PLAZA"): "الساحة", ("break1", "FRYING"): "فرن",
        ("fix1", "SHADE"): "تظلل", ("fix1", "DOME"): "قبة", ("fix1", "HUNDRED"): "مية", ("fix1", "WIDE"): "متر",
        ("break2", "SOLID"): "بدون", ("break2", "DARK"): "مظلم", ("break2", "CAVE"): "كهف",
        ("fix2", "WEAVE"): "تسويها", ("fix2", "SEVEN"): "سبعة", ("fix2", "STARS"): "نجمة", ("fix2", "LIGHT"): "النور",
        ("fix2", "FALLS"): "ينزل", ("fix2", "PALM"): "النخل",
        ("break3", "WIDE"): "العرض", ("break3", "FOREST"): "غابة", ("break3", "COLUMNS"): "أعمدة",
        ("fix3", "FOUR"): "أربع", ("fix3", "LEGS"): "رجول", ("fix3", "HIDDEN"): "مخب", ("fix3", "BUILDINGS"): "المباني",
        ("fix3", "FLOAT"): "طاير",
        ("break4", "MUSEUM"): "المتحف", ("break4", "SEA"): "البحر", ("break4", "BASEMENTS"): "القبو",
        ("break4", "WATER"): "الموي",
        ("fix4", "DRY"): "ناشف", ("fix4", "PIT"): "حفرة", ("fix4", "SEAL"): "تعزل", ("fix4", "BATHTUB"): "بانيو",
        ("fix4", "LET"): "تدخل", ("fix4", "SEA"): "البحر",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "ARCHITECT"): "المعماري", ("reveal", "JEAN"): "جان", ("reveal", "COPIED"): "قلد",
        ("reveal", "PALM"): "النخل", ("reveal", "GALLERIES"): "المعارض", ("reveal", "TOWN"): "حارة",
        ("stat", "SEVEN"): "سبعة", ("stat", "EIGHT"): "ثمان", ("stat", "FIFTY"): "خمسة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SHADE"): "ظل", ("tag", "BEACH"): "البحر", ("tag", "DAD"): "أبوك", ("tag", "UMBRELLA"): "الشمسي",
        ("tag", "CHASING"): "يلحق"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a vacuum cleaner"),
                   "stat": [("7,500 t", "STEEL DOME"), ("8", "LAYERS"), ("55", "BUILDINGS")],
                   "L": {"heavy": "AS HEAVY AS THE EIFFEL TOWER", "rain": "A RAIN OF LIGHT", "name": "LOUVRE ABU DHABI",
                         "sun": "SUMMER: 45°C+", "pan": "A FRYING PAN", "shade": "ONE GIANT SHADE", "wide": "180 m WIDE",
                         "cave": "A DARK CAVE", "stars": "7,850 METAL STARS", "layers": "LAYER", "palm": "LIKE SUN THROUGH PALMS",
                         "forest": "A FOREST OF COLUMNS", "legs": "JUST 4 LEGS", "hidden": "HIDDEN IN THE BUILDINGS",
                         "float": "IT FLOATS", "below": "BASEMENTS BELOW THE SEA", "dry": "A DRY PIT", "tub": "A GIANT BATHTUB",
                         "seain": "LET THE SEA IN", "nouvel": "ARCHITECT JEAN NOUVEL", "grove": "A PALM GROVE",
                         "town": "LIKE AN OLD ARAB TOWN", "allday": "ALL DAY LONG", "clock": "10:00"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مكنسة كهربا"),
                      "stat": [("7500", "طن"), ("8", "طبقات"), ("55", "مبنى")],
                      "L": {"heavy": "بوزن برج إيفل", "rain": "الشمس تمطر نور", "name": "متحف اللوفر أبوظبي",
                            "sun": "الصيف: فوق 45 درجة", "pan": "فرن!", "shade": "ظل واحد كبير", "wide": "عرضها 180 متر",
                            "cave": "كهف مظلم", "stars": "7850 نجمة حديد", "layers": "طبقة", "palm": "مثل الشمس بين سعف النخل",
                            "forest": "غابة أعمدة", "legs": "أربع رجول بس", "hidden": "مخبّاة داخل المباني",
                            "float": "كأنها طايرة", "below": "القبو تحت مستوى البحر", "dry": "حفرة ناشفة", "tub": "بانيو عملاق",
                            "seain": "دخّل البحر", "nouvel": "المعماري جان نوفيل", "grove": "ظل النخل",
                            "town": "مثل حارة عربية قديمة", "allday": "طول اليوم", "clock": "10:00"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "dome": ("hook", "DOME", 0.1), "heavy": ("hook", "HEAVY", 0.2), "eiffel": ("hook", "EIFFEL", 0.32),
            "sea": ("hook", "SEA", 0.45), "light": ("hook", "LIGHT", 0.55), "rain": ("hook", "RAIN", 0.62),
            "congrats": ("hook", "CONGRATS", 0.75), "name": ("hook", "LOUVRE", 0.9),
            "sun": ("break1", "SUN", 0.25), "plaza": ("break1", "PLAZA", 0.6), "frying": ("break1", "FRYING", 0.85),
            "shade": ("fix1", "SHADE", 0.1), "dome1": ("fix1", "DOME", 0.4), "hundred": ("fix1", "HUNDRED", 0.6),
            "wide": ("fix1", "WIDE", 0.9),
            "solid": ("break2", "SOLID", 0.2), "dark": ("break2", "DARK", 0.7), "cave": ("break2", "CAVE", 0.9),
            "weave": ("fix2", "WEAVE", 0.08), "seven": ("fix2", "SEVEN", 0.2), "stars": ("fix2", "STARS", 0.5),
            "light2": ("fix2", "LIGHT", 0.6), "falls": ("fix2", "FALLS", 0.7), "palm": ("fix2", "PALM", 0.88),
            "wide3": ("break3", "WIDE", 0.3), "forest": ("break3", "FOREST", 0.6), "columns": ("break3", "COLUMNS", 0.85),
            "four": ("fix3", "FOUR", 0.2), "legs": ("fix3", "LEGS", 0.3), "hidden": ("fix3", "HIDDEN", 0.45),
            "buildings": ("fix3", "BUILDINGS", 0.65), "float": ("fix3", "FLOAT", 0.92),
            "museum": ("break4", "MUSEUM", 0.15), "sea4": ("break4", "SEA", 0.4), "basements": ("break4", "BASEMENTS", 0.65),
            "water": ("break4", "WATER", 0.9),
            "dry": ("fix4", "DRY", 0.15), "pit": ("fix4", "PIT", 0.25), "seal": ("fix4", "SEAL", 0.4),
            "bathtub": ("fix4", "BATHTUB", 0.65), "let": ("fix4", "LET", 0.82),
            "follow": ("cta", "FOLLOW", 0.35),
            "architect": ("reveal", "ARCHITECT", 0.15), "jean": ("reveal", "JEAN", 0.22), "copied": ("reveal", "COPIED", 0.35),
            "palm5": ("reveal", "PALM", 0.48), "galleries": ("reveal", "GALLERIES", 0.65), "town": ("reveal", "TOWN", 0.92),
            "s1": ("stat", "SEVEN", 0.05), "s2": ("stat", "EIGHT", 0.45), "s3": ("stat", "FIFTY", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_shade": ("tag", "SHADE", 0.05), "t_beach": ("tag", "BEACH", 0.35), "t_dad": ("tag", "DAD", 0.45),
            "t_umbrella": ("tag", "UMBRELLA", 0.6), "t_chasing": ("tag", "CHASING", 0.85)})
        T["sea_in"] = self.w("fix4", "SEA", 0.92, nth=0 if self.lang != "en" else 1)
        T["frying1"] = max(T["frying"], T["plaza"]) + 0.15
        T["cave1"] = max(T["cave"], T["dark"]) + 0.15
        T["columns1"] = max(T["columns"], T["forest"]) + 0.15
        T["water1"] = max(T["water"], T["basements"]) + 0.15
        T["wide1"] = max(T["wide"], T["hundred"]) + 0.2
        T["palm1"] = max(T["palm"], T["falls"]) + 0.2
        T["float1"] = max(T["float"], T["buildings"]) + 0.2
        T["sea_in1"] = max(T["sea_in"], T["let"]) + 0.3
        T["back"] = max(s("fix2") + 1.2, T["light2"] - 0.15)           # cut back from the top view to the falling light
        # ---- sets
        self.cut(s("fix2") - 0.12, "plan", 1)
        self.cut(T["back"], "sea", -1)
        self.cut(s("break4") - 0.12, "pit", 1)
        self.cut(s("reveal") - 0.12, "plan", -1)
        self.cut(s("stat") - 0.12, "sea", 1)
        self.cut(s("tag") - 0.2, "beach", -1)
        # ---- sea camera: close under the dome, out to the whole museum on the sea
        cm = Camera(70, -40, 3.2)
        cm.key(0.05, 40, -40, 3.0, 1.2)
        cm.key(max(1.2, T["congrats"] - 0.9), 0, 24, 1.6, max(1.0, T["name"] - T["congrats"] + 0.9))
        cm.key(s("break1") - 0.12, 0, 24, 1.6, 0.0)
        cm.key(s("break3") - 0.1, 0, 10, 1.7, 0.8)
        cm.key(s("fix3") + 0.2, 0, 10, 1.7, 0.6)
        cm.key(s("stat") - 0.12, 0, 24, 1.6, 0.0)
        cm.key(s("closer") - 0.1, 0, 20, 1.62, 1.2)
        self.cam = cm
        self.spans = [(T["frying1"], T["wide1"] + 0.3), (T["cave1"], T["palm1"] + 0.3), (T["columns1"], T["float1"] + 0.3),
                      (T["water1"], T["sea_in1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["dome1"] + 0.5, 0.45, 12), (T["cave1"], 0.3, 6),
                       (T["columns1"], 0.4, 8), (T["water1"], 0.4, 8), (T["sea_in"], 0.5, 8), (s("closer") + 0.2, 0.35, 8),
                       (T["t_umbrella"], 0.3, 6)]

    # ------------------------------------------------------------------ set: sea
    def draw_sea(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        noon = s("break1") - 0.12 <= t < s("fix1") + 0.2
        stat = s("stat") - 0.12 <= t < s("closer") - 0.1
        night = clamp((t - (s("closer") - 0.1)) / 1.0) if t >= s("closer") - 0.1 else 0.0
        gy = self.to_screen(cam, 0, -30)[1]
        if noon:
            v2.sky(c, W, H, 0.0, pal=NOONP, horizon_y=gy)
        elif stat:
            v2.sky(c, W, H, 0.0, pal=DUSKP, horizon_y=gy)
        else:
            v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
            if night > 0:
                c.saveLayerAlpha(None, int(255 * night))
                v2.sky(c, W, H, 0.0, pal=BLUEP, horizon_y=gy)
                c.restore()
                v2.stars(c, W, H, t, 0.8 * night)
        if stat:
            v2.stars(c, W, H, t, 0.35)
        # the sun
        if noon:
            heat = prog(t, T["sun"] - 0.3, T["sun"] + 0.3) * (1 - prog(t, T["dome1"], T["dome1"] + 0.6))
            sun(c, 540, 430, 62, heat=0.8 + 0.4 * heat, a=1.0)
            if heat > 0:
                add_glow(c, 540, 430, 300, "#FFF7D6", 0.22 * heat)
        elif night < 1:
            sx, sy = (860, gy - 120) if not stat else (780, gy - 30)
            sun(c, sx, sy, 46, heat=0.6, a=1 - night)
        self.view(c, cam)
        far_city(c, t, night=max(night, 0.5 if stat else 0.0))
        dome_on = True
        dy, solid, shade = 0.0, 0.0, 1.0
        beam_k = 1.0
        cols = 0.0
        xray = 0.0
        if s("break1") - 0.12 <= t < s("break2") - 0.12:                     # no dome, then it comes down
            p = e_out(prog(t, T["dome1"] - 0.5, T["dome1"] + 0.5))
            dy = -(1 - p) * 900
            dome_on = t >= T["dome1"] - 0.5
            solid = 1.0
            shade = p
            beam_k = 0.0
        elif s("break2") - 0.12 <= t < T["back"]:                           # solid: a dark cave
            solid, shade, beam_k = 1.0, 1.0 + 1.3 * prog(t, T["solid"] - 0.2, T["dark"]), 0.0
        elif T["back"] <= t < s("break4"):                                   # the light rains again; columns; legs
            beam_k = prog(t, T["back"], T["back"] + 0.5)
            cols = prog(t, T["forest"] - 0.3, T["columns1"] + 0.4) if t < s("fix3") - 0.12 else \
                1 - prog(t, T["four"] - 0.4, T["four"] + 0.2)
            xray = prog(t, T["hidden"] - 0.3, T["hidden"] + 0.2) * (1 - prog(t, T["float"] + 0.1, T["float"] + 0.6)) \
                if t >= s("fix3") - 0.12 else 0.0
        if night > 0:
            beam_k = 1 - night
        water(c, t, night=night, refl=1.0, dome_a=1.0 if dome_on and dy > -100 else 0.0)
        galleries(c, t, shade=0.0, night=night, xray=xray)
        people = ((-150, "#2563EB", 1), (-60, "#DB2777", -1), (2, "#F59E0B", 1), (112, "#16A34A", -1), (160, "#7C3AED", 1),
                  (262, "#0EA5E9", -1))
        for i, (px, col, face) in enumerate(people):
            pose = "look" if t < s("break1") - 0.12 else ("shrug" if noon and t > T["frying1"] else "stand")
            person(c, px, PLAZA, 13, col, t + i, pose=pose, face=face)
        if dome_on and shade > 0:
            c.drawPath(under_path(dy if dy > -60 else 0.0), P("#0B1220", clamp(0.38 * shade, 0, 0.88)))
        if noon and t < T["dome1"]:
            heat_lines(c, -300, 300, -120, PLAZA, t, a=0.8 * prog(t, T["plaza"] - 0.3, T["plaza"]))
        if s("break2") - 0.12 <= t < T["back"]:                             # phone torches and a bat in the dark
            dk = prog(t, T["dark"] - 0.4, T["dark"])
            for i, (px, _, _) in enumerate(people[:4]):
                add_glow(c, px + 4, PLAZA - 11, 9, "#FFFFFF", 0.9 * dk)
                light_cone(c, px + 4, PLAZA - 11, -60 - i * 20, 40, 16, a=0.25 * dk)
            bx = lerp(-260, 260, prog(t, T["cave"] - 0.6, T["cave"] + 1.2))
            by = -100 + math.sin(t * 9) * 6
            if dk > 0:
                wing = math.sin(t * 22) * 6
                c.drawPath(path_of([(bx - 12, by - wing), (bx - 3, by), (bx, by - 3), (bx + 3, by), (bx + 12, by - wing),
                                    (bx + 4, by + 3), (bx - 4, by + 3)], close=True), P("#0B0B0B", dk))
        columns(c, t, cols)
        legs(c, t, xray)
        beams(c, t, beam_k, warm=0.5 if not noon else 0.0)
        if dome_on:
            dome(c, t, dy=dy, solid=solid, night=night, glow=night)
        if night > 0:                                                      # blue hour: the dome lit from below
            for x, w, ph in HOLES[::2]:
                add_glow(c, x * 0.95, d_bot(x) + 8, 34, "#FFC470", 0.45 * night)
            for x in (-250, -120, 0, 120, 250):
                add_glow(c, x, PLAZA - 30, 90, "#FFB870", 0.3 * night)
        c.restore()
        self.ui["cam"] = cam

    def ui_sea(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam.at(tw))
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "rain", 0.2, T["heavy"] - 0.15, accent=HILITE, size=48)
            self.chip(540, 300, "heavy", T["heavy"] - 0.15, T["congrats"] - 0.15, accent="#CBD5E1", size=40)
            self.chip(540, 300, "name", T["congrats"] - 0.15, s("break1") + 0.1, accent=HILITE, size=54)
            return
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "sun", T["sun"] - 0.2, T["frying"] - 0.2, accent=WARN, size=46)
            self.chip(540, 300, "pan", T["frying"] - 0.2, s("fix1") - 0.15, accent=WARN, size=50)
            self.egg(c, tw)
            self.badge("alert", T["frying1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["frying1"], 1.2)
            return
        if tw < s("break2") - 0.12:
            self.egg(c, tw)
            self.chip(540, 300, "shade", T["shade"] - 0.2, T["hundred"] - 0.2, accent="#93C5FD", size=46)
            self.chip(540, 300, "wide", T["hundred"] - 0.2, s("break2") - 0.15, accent=HILITE, size=50)
            dk = self.span(T["hundred"] - 0.2, s("break2") - 0.15)
            if dk > 0:
                x0, y0 = self.to_screen(cam, -RX, -205)
                x1, _ = self.to_screen(cam, RX, -205)
                c.drawLine(x0, y0, x1, y0, P("#FDE68A", dk, stroke=5))
                for xx in (x0, x1):
                    c.drawLine(xx, y0 - 18, xx, y0 + 18, P("#FDE68A", dk, stroke=5))
            self.badge("check", T["wide1"] + 0.1, s("break2") - 0.15, x=920, y=440)
            return
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "cave", T["dark"] - 0.3, s("fix2") - 0.15, accent="#94A3B8", size=50)
            self.badge("alert", T["cave1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["cave1"], 1.2)
            return
        if tw < s("break3") - 0.12:                                          # second half of fix2: the light
            self.chip(540, 300, "palm", T["falls"] - 0.3, s("break3") - 0.15, accent=GOOD, size=40)
            pk = self.span(T["palm"] - 0.3, s("break3") - 0.15)
            if pk > 0:
                palm_inset(c, 540, 600, 180, tw, a=pk)
            self.badge("check", T["palm1"] + 0.1, s("break3") - 0.15, x=920, y=440)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "forest", T["forest"] - 0.3, s("fix3") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["columns1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["columns1"], 1.2)
            return
        if tw < s("break4") - 0.12:
            self.chip(540, 300, "legs", T["four"] - 0.2, T["hidden"] - 0.2, accent=HILITE, size=50)
            self.chip(540, 300, "hidden", T["hidden"] - 0.2, T["float"] - 0.2, accent="#FDE68A", size=42)
            self.chip(540, 300, "float", T["float"] - 0.2, s("break4") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["float1"] + 0.1, s("break4") - 0.15, x=920, y=440)

    def egg(self, c, tw):
        T = self.T
        ek = self.span(min(T["plaza"], T["frying"] - 0.8) - 0.1, T["dome1"] + 0.1)
        if ek > 0:
            egg_inset(c, 540, 600, 190, tw, prog(tw, T["plaza"] - 0.2, T["frying"] + 0.4), a=ek)

    # ------------------------------------------------------------------ set: plan (fix2 first half, reveal)
    def draw_plan(self, c, t):
        T, s = self.T, self.tl.s
        cx, cy, Rr = 540, 830, 380
        if t < s("cta"):                                                    # fix2: the layers
            vrect(c, 0, 0, W, H, ["#0B1220", "#14213A"])
            n = 1 + 7 * prog(t, T["weave"] - 0.1, T["stars"] + 0.4)
            star_layers(c, cx, cy, Rr, n, t, light=1.0)
            self.ui["n"] = n
            return
        # reveal: a palm grove from above -> the dome -> the town under it
        vrect(c, 0, 0, W, H, ["#E3C99A", "#C9A46A"])
        rng = random.Random(3)
        for i in range(60):                                                 # dappled sun on the sand
            add_glow(c, rng.uniform(0, W), rng.uniform(300, 1400), rng.uniform(14, 30), "#FFF7D6", 0.5)
        pk = 1 - prog(t, T["copied"] + 0.2, T["copied"] + 1.0)
        if pk > 0:
            rng = random.Random(4)
            for i in range(14):
                px = 160 + (i % 4) * 250 + rng.uniform(-40, 40) + (125 if (i // 4) % 2 else 0)
                py = 430 + (i // 4) * 250 + rng.uniform(-30, 30)
                if px < W + 100:
                    palm_top(c, px, py, 150, t, a=pk, seed=i)
        dk = prog(t, T["copied"] - 0.1, T["copied"] + 0.8)
        tk = prog(t, T["galleries"] - 0.3, T["town"] + 0.4)
        if dk > 0:
            c.drawCircle(cx, cy, Rr * 1.25, P(SEA_C, dk))                   # the museum on the sea
            star_layers(c, cx, cy, Rr, 8, t, a=dk * (1 - 0.88 * prog(t, T["galleries"] - 0.3, T["galleries"] + 0.5)), light=1.0)
            town_plan(c, cx, cy, Rr, tk, t)

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("cta"):
            n = self.ui.get("n", 1)
            self.chip(540, 300, "stars", T["seven"] - 0.2, T["back"] + 0.2, accent=HILITE, size=46)
            lk = self.span(T["weave"], T["back"] + 0.2)
            if lk > 0:
                lab = "%s %d/8" % (self.L["layers"], int(clamp(n, 1, 8)))
                v2.chip(c, 540, 392, lab, lk, accent="#CBD5E1", size=40)
            return
        self.chip(540, 300, "nouvel", T["architect"] - 0.2, T["copied"] - 0.1, accent="#CBD5E1", size=40)
        self.chip(540, 300, "grove", T["copied"] - 0.1, T["galleries"] - 0.2, accent=GOOD, size=48)
        self.chip(540, 300, "town", T["galleries"] - 0.2, s("stat") - 0.15, accent=HILITE, size=44)

    # ------------------------------------------------------------------ set: pit (break4, fix4, cta)
    def draw_pit(self, c, t):
        T, s = self.T, self.tl.s
        SL = 760
        vrect(c, 0, 0, W, SL, ["#1B4F8F", "#3A7CC0", "#7FB2DE"])
        sun(c, 860, 260, 46, heat=0.6)
        fixed = t >= s("fix4") - 0.12
        dryk = prog(t, T["dry"] - 0.4, T["dry"] + 0.3) if fixed else 0.0
        sealk = prog(t, T["seal"] - 0.2, T["bathtub"] + 0.3) if fixed else 0.0
        letk = e_io(prog(t, T["let"] - 0.2, T["sea_in1"] + 0.3)) if fixed else 0.0
        # ground layers
        c.drawRect(R(0, SL, W, H - SL), lin_paint(0, SL, 0, H, ["#C9A46A", "#8A6A3E", "#5A4428"]))
        rng = random.Random(6)
        for i in range(90):
            c.drawCircle(rng.uniform(0, W), rng.uniform(SL + 20, H), rng.uniform(2, 6), P("#6B5030", 0.5))
        bx0, bx1, by0, by1 = 300, 780, SL, 1060                              # the basement box
        # the sea around: before the fix it is everywhere outside the walls; the pit pushes it away, then it comes back
        sea_out = 1.0 if not fixed else letk
        if sea_out > 0:
            lv = SL - 6
            for x0, x1 in ((0, bx0 - 30), (bx1 + 30, W)):
                c.drawRect(R(x0, lv, x1 - x0, 1200 - lv), lin_paint(0, lv, 0, 1200, [SEA_C, SEA_D], a=sea_out))
            if fixed and letk < 1:                                          # water pouring back in
                for sx in (bx0 - 30, bx1 + 30):
                    c.drawRect(R(sx - 30, lv, 60, 400 * letk), P(SEA_C, 0.6 * letk))
        if fixed and dryk > 0 and letk < 1:                                  # the dry pit: steel walls and the sea held back
            c.drawRect(R(0, SL - 6, 210, 1200 - SL), lin_paint(0, SL, 0, 1200, [SEA_C, SEA_D], a=dryk * (1 - letk)))
            c.drawRect(R(870, SL - 6, W - 870, 1200 - SL), lin_paint(0, SL, 0, 1200, [SEA_C, SEA_D], a=dryk * (1 - letk)))
            up = (1 - letk) * dryk
            sheet_piles(c, 225, SL - 60 - 0 * up, 1180, a=up)
            sheet_piles(c, 855, SL - 60, 1180, a=up)
            if dryk > 0.5 and letk <= 0:                                    # a pump throwing water over the wall
                for k in range(8):
                    u = (t * 1.5 + k / 8) % 1.0
                    c.drawCircle(lerp(240, 120, u), SL - 80 - math.sin(u * math.pi) * 120, 7, P("#7DD3FC", 0.8 * dryk))
                c.drawRRect(rr(230, SL - 30, 60, 40, 8), P("#F59E0B", dryk))
        # the building above the sea and the basement below it
        c.drawRect(R(bx0 - 30, 560, bx1 - bx0 + 60, SL - 560), lin_paint(bx0 - 30, 0, bx1 + 30, 0, ["#FBF8F1", "#E4DDCF", "#CFC6B4"]))
        c.drawRect(R(bx0 - 30, 560, bx1 - bx0 + 60, SL - 560), P("#8C7F68", 1.0, stroke=4))
        for k in range(4):
            c.drawRect(R(bx0 + 20 + k * 115, 610, 70, 90), P("#334155", 0.85))
        c.drawRect(R(bx0 - 50, 548, bx1 - bx0 + 100, 14), P("#64748B"))
        c.drawRect(R(bx0, by0, bx1 - bx0, by1 - by0), P("#F1ECE2"))
        c.drawRect(R(bx0, by0 + 140, bx1 - bx0, 12), P("#B8AC94"))
        flood = prog(t, T["basements"] - 0.2, T["water1"] + 1.0) if not fixed else 0.0
        for k in range(4):
            painting(c, bx0 + 40 + k * 115, by0 + 40, 70, 60, k, wet=flood)
            painting(c, bx0 + 40 + k * 115, by0 + 190, 70, 60, k + 7, wet=flood)
        if flood > 0:                                                       # the sea seeps in and rises
            lvl = by1 - (by1 - by0 - 20) * flood * 0.85
            c.drawRect(R(bx0, lvl, bx1 - bx0, by1 - lvl), P(SEA_C, 0.75))
            for k in range(10):
                u = (t * 1.2 + k / 10) % 1.0
                for sx in (bx0 + 4, bx1 - 4):
                    c.drawCircle(sx, lerp(by0 + 30, lvl, u), 5, P("#7DD3FC", 0.8))
        if sealk > 0:                                                       # the yellow tub, drawn around the basement
            tub = path_of([(bx0 - 14, by0 - 10), (bx0 - 14, by1 + 14), (bx1 + 14, by1 + 14), (bx1 + 14, by0 - 10)])
            pm = skia.PathMeasure(tub, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * clamp(sealk), seg, True)
            c.drawPath(seg, P("#FACC15", 1.0, stroke=22))
            c.drawPath(seg, P("#1F2937", 0.6, stroke=4))
        c.drawRect(R(bx0, by0, bx1 - bx0, by1 - by0), P("#64748B", 1.0, stroke=6))
        # the sea level line
        dashed(c, 0, SL - 6, W, SL - 6, "#E0F2FE", w=4, dash=18, gap=12, phase=t * 30, a=0.9)
        self.ui["SL"] = SL

    def ui_pit(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "below", T["basements"] - 0.3, s("fix4") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["water1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["water1"], 1.2)
            return
        self.chip(540, 300, "dry", T["dry"] - 0.2, T["seal"] - 0.2, accent="#FDBA74", size=50)
        self.chip(540, 300, "tub", T["seal"] - 0.2, T["let"] - 0.2, accent=HILITE, size=50)
        self.chip(540, 300, "seain", T["let"] - 0.2, s("cta") - 0.15, accent="#7DD3FC", size=48)
        self.badge("check", T["sea_in1"] + 0.1, s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: beach (tag)
    def draw_beach(self, c, t):
        T, s = self.T, self.tl.s
        t0, t1 = s("tag") - 0.2, self.duration
        u = prog(t, t0 + 0.4, t1 - 0.4)
        vrect(c, 0, 0, W, 900, ["#3B82C4", "#7DB8E8", "#D6ECFA"])
        sxp = lerp(150, 930, u)
        syp = 520 - math.sin(u * math.pi) * 260
        sun(c, sxp, syp, 54, heat=0.7)
        c.drawRect(R(0, 860, W, 120), lin_paint(0, 860, 0, 980, ["#2A9DB8", "#1E7A9A"]))
        for k in range(4):
            dashed(c, 0, 880 + k * 24, W, 880 + k * 24, "#E0F7FF", w=3, dash=40, gap=30, phase=t * 40 + k * 20, a=0.5)
        c.drawRect(R(0, 960, W, H - 960), lin_paint(0, 960, 0, H, ["#F2D9A6", "#D9B77A"]))
        # the family sits still; the sun moves, the shade drifts off them, dad drags the umbrella after it
        def off(uu):
            sx_ = lerp(150, 930, uu)
            return clamp((540 - sx_) * 0.55, -280, 280)
        steps = 5
        k = u * steps
        i, f = min(int(k), steps - 1), k - min(int(k), steps - 1)
        hop = e_io(clamp((f - 0.6) / 0.3))
        ua, ub = i / steps, (i + 1) / steps
        ux = lerp(540 - off(ua + 0.5 / steps * 0), 540 - off(ub), hop)
        shx = ux + off(u)
        c.drawOval(R(shx - 270, 1120, 540, 90), P("#7A5A30", 0.42))
        c.drawRRect(rr(540 - 170, 1140, 340, 46, 10), P("#2563EB"))         # the mat
        for k2 in range(5):
            c.drawRect(R(540 - 170 + k2 * 68 + 20, 1140, 22, 46), P("#FDE68A", 0.8))
        hot = clamp(abs(shx - 540) / 220)
        person(c, 470, 1170, 210, "#DB2777", t, pose="sit", face=1, hair="#3B2A20")
        person(c, 600, 1170, 150, "#16A34A", t + 1, pose="sit", face=-1)
        if hot > 0.3:                                                       # sweat drops when the shade has gone
            for k2, (px, py) in enumerate(((470, 950), (600, 1010))):
                c.drawCircle(px + 40 + math.sin(t * 6 + k2) * 4, py + (t * 80 % 40), 7, P("#7DD3FC", hot))
        dad_x = ux + 60
        walking = 0.6 < f < 0.95
        if self.rtl:
            saudi_man(c, dad_x, 1180, 230, t, pose="walk" if walking else "stand", face=1 if off(ub) < off(ua) else -1)
        else:
            person(c, dad_x, 1180, 230, "#F59E0B", t, pose="walk" if walking else "stand",
                   face=1 if off(ub) < off(ua) else -1, hat="cap")
        umbrella(c, ux, 1180, 2.3, col="#EF4444")
        self.ui["clock"] = 10 + int(u * 7)

    def ui_beach(self, c, t, tw):
        T = self.T
        hr = self.ui.get("clock", 10)
        v2.chip(c, 540, 300, "%02d:00" % hr, self.span(T["t_shade"], self.duration + 1), accent=HILITE, size=54)
        self.chip(540, 420, "allday", T["t_chasing"] - 0.3, self.duration + 1, accent=WARN, size=46)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1220", "#1E293B"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.sparkle(1.6, 14, 61), -12), (T["heavy"], sfx.thud(0.5, 62), -10),
              (T["rain"], sfx.sparkle(1.0, 12, 63), -8),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(T["sun"], sfx.hiss(1.2, 66), -16), (T["frying"] - 0.2, sfx.sizzle(1.2, 67), -8), (T["frying1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["dome1"] - 0.5, sfx.whoosh(0.8, False, 68), -8), (T["dome1"] + 0.5, sfx.thud(0.6, 69), -4),
               (T["wide1"], sfx.ding(), -8), (T["wide1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["dark"] - 0.3, sfx.power_down(1.0, 70), -10), (T["cave1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 71), -4)]
        for k in range(8):
            ev.append((lerp(T["weave"], T["stars"] + 0.4, k / 7), sfx.click(72 + k), -10))
        ev += [(T["back"], sfx.whoosh(0.4, True, 80), -4), (T["light2"], sfx.sparkle(1.2, 14, 81), -8),
               (T["palm1"], sfx.ding(), -8), (T["palm1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["forest"] - 0.2, sfx.clank(300.0, 0.5, 82), -12), (T["columns1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["four"], sfx.whoosh(0.5, False, 83), -10), (T["hidden"], sfx.charge_up(0.6), -14),
               (T["float1"], sfx.ding(), -8), (T["float1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 84), -4), (T["basements"], sfx.hiss(1.2, 85), -14),
               (T["water1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["dry"], sfx.whirr(1.4, 150.0, 230.0, 86), -14), (T["seal"], sfx.riser(0.8, 87), -14),
               (T["let"], sfx.hiss(1.4, 88), -10), (T["sea_in1"], sfx.ding(), -8), (T["sea_in1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(89), 0), (T["follow"] - 0.15, sfx.pop(90), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 91), -6), (T["copied"], sfx.sparkle(0.9, 10, 92), -10),
               (T["galleries"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 93), -6), (T["s1"], sfx.pop(94), -3), (T["s2"], sfx.pop(95), -3),
               (T["s3"], sfx.pop(96), -3)]
        ev += [(T["cong2"], sfx.pop(97), -2), (T["cong2"], sfx.sparkle(1.4, 18, 98), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 99), -6), (T["t_umbrella"], sfx.thud(0.3, 100), -10),
               (T["t_chasing"], sfx.womp(), -8)]
        return ev


NAME = "louvre"
EPISODE = Louvre
