"""Episode 112 - the Sydney Harbour Bridge, "the Coathanger" (two half-arches built out from each shore, held back by
cables tied into tunnels in the rock, joined one night in August 1930; opened 1932).  v2 look.

Sets: harbour (hook: the two half-arches reaching for each other over the harbour at dusk, creeper cranes on the tips,
a gap in the middle; the camera pulls out from the gap to the whole harbour; cta; stat: the finished bridge with a line
of steam locomotives on the deck; closer: the bridge lit at night with fireworks, for the cover), build (break1: no
pillars, ships sail through; fix1: each half grows out from its shore; break2: a half-arch tips into the water; fix2:
cables tie each half back into tunnels in the rock; break3: an ordinary crane cannot reach; fix3: creeper cranes crawl
up the arch as it grows), heat (break4: the sun on all that metal; fix4: built to move, the top rises 18 cm, hinge pins
at the feet), close (reveal: the cables let out bit by bit until the two tips touch one night), tag (the arch turns into
a coat hanger) and chair (your coat on a chair; Arabic: the thobe thrown on the couch).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

STEEL_C = ("#A3ADBD", "#7D8899", "#4E5869")          # bridge grey: light, mid, dark
GRANITE = ("#B8A88E", "#958670", "#6B5F4E")
SAND = ("#8C6A4C", "#6E513A", "#4A3526")
X0, X1, XC, HALF = 150, 930, 540, 390                  # bearings, middle, half span (screen px)
BEAR_Y, RISE = 840, 340
WATER_Y, LAND_Y, DECK_Y = 890, 830, 785
NP = 14                                                # panels in each half
PY_TOP = 650                                           # pylon tops
TUN_Y = 1010                                           # the cable tunnels in the rock
HEAT_Z, HEAT_SY, HEAT_WY = 1.75, 780, 540              # the heat close-up: zoom, screen y of world y


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def yb(x):
    u = (x - XC) / HALF
    return BEAR_Y - RISE * (1 - u * u)


def yt(x):
    u = (x - XC) / HALF
    return yb(x) - (34 + 66 * u * u)


def px_at(i):
    """x of panel point i (0 = left bearing, 2*NP = right bearing)."""
    return X0 + (X1 - X0) * i / (2 * NP)


# ====================================================================================== the harbour
def sky(c, night=0.0):
    day = ["#22305E", "#4A4F8C", "#B9677A", "#F2A65A"]
    ngt = ["#050A1C", "#0B1430", "#182247", "#26305A"]
    cols = [mix(a, b, night) for a, b in zip(day, ngt)]
    vrect(c, 0, 0, W, WATER_Y, cols, [0.0, 0.45, 0.8, 1.0])
    if night > 0:
        v2.stars(c, W, H, 0.0, 0.9 * night, n=180)


def city(c, t, lit=0.0):
    """Sydney's towers far behind the bridge."""
    rng = random.Random(11)
    x = -30
    while x < W + 30:
        w = rng.uniform(34, 70)
        h = rng.uniform(40, 200) if 300 < x < 800 else rng.uniform(20, 110)
        top = WATER_Y - 30 - h
        c.drawRect(R(x, top, w - 5, h + 40), P(mix("#2A2F55", "#111530", lit)))
        if lit > 0:
            for j in range(int(h / 22)):
                for q in range(int((w - 14) / 12)):
                    if rng.random() < 0.35:
                        c.drawRect(R(x + 5 + q * 12, top + 8 + j * 22, 6, 8), P("#FDE68A", 0.55 * lit))
        x += w


def water(c, t, night=0.0, y0=WATER_Y):
    c.drawRect(R(0, y0, W, H - y0), lin_paint(0, y0, 0, 1250, [mix("#35507E", "#0E1A33", night), mix("#1A2B4C", "#070D1C", night)]))
    for k in range(40):
        xx = (k * 53 + t * 24 * (1 if k % 2 else -0.6)) % (W + 80) - 40
        yy = y0 + 14 + (k % 10) * 34
        c.drawLine(xx, yy, xx + 30 + (k % 3) * 12, yy, P(mix("#F6B07A", "#FDE68A", night), 0.28, stroke=3))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B1224", "#05080F"]))


def shore(c, side, night=0.0, tunnel=0.0, t=0.0):
    """The rocky shore under one end, cut open; tunnel 0..1 shows the cable tunnel in the rock."""
    sd = -1 if side == "L" else 1
    xb = X0 if sd < 0 else X1
    p = skia.Path()
    edge = xb + sd * -6
    p.moveTo(edge, LAND_Y)
    p.lineTo(edge + sd * 1200, LAND_Y)
    p.lineTo(edge + sd * 1200, 1250)
    p.lineTo(edge - sd * 60, 1250)
    p.lineTo(edge - sd * 46, WATER_Y + 40)
    p.lineTo(edge - sd * 18, WATER_Y - 6)
    p.close()
    c.drawPath(p, lin_paint(0, LAND_Y, 0, 1250, [mix(SAND[0], "#3A2E2A", night * 0.6), mix(SAND[2], "#1C1512", night * 0.6)]))
    c.drawLine(edge, LAND_Y, edge + sd * 1200, LAND_Y, P(mix("#B08A62", "#5A4A3E", night), 1, stroke=5))
    for k in range(5):                                   # sandstone layers
        yy = LAND_Y + 40 + k * 44
        c.drawLine(edge - sd * 30, yy, edge + sd * 1200, yy + (k % 2) * 6, P(SAND[2], 0.5, stroke=2))
    if tunnel > 0:                                       # the horseshoe tunnel, cut open
        tx = xb + sd * 80
        c.drawRRect(rr(tx - 56, TUN_Y - 30, 112, 60, 30), P("#120C08", tunnel))
        c.drawRRect(rr(tx - 56, TUN_Y - 30, 112, 60, 30), P("#FACC15", 0.8 * tunnel, stroke=5))
        add_glow(c, tx, TUN_Y, 100, "#FACC15", 0.35 * tunnel)


def pylon(c, side, night=0.0, lit=0.0):
    sd = -1 if side == "L" else 1
    x0 = (X0 - 112) if sd < 0 else (X1 + 2)
    x1 = x0 + 110
    top = PY_TOP
    c.drawRect(R(x0 - 6, LAND_Y - 14, 122, 26), P(GRANITE[2]))
    c.drawRect(R(x0, top, 110, LAND_Y - top), lin_paint(x0, 0, x1, 0, [GRANITE[1], GRANITE[0], GRANITE[1], GRANITE[2]]))
    c.drawRect(R(x0 - 8, top - 16, 126, 20), P(GRANITE[2]))
    c.drawRect(R(x0 + 14, top - 40, 82, 26), P(GRANITE[1]))
    for k in range(6):
        yy = top + 26 + k * 26
        c.drawLine(x0, yy, x1, yy, P(GRANITE[2], 0.35, stroke=2))
    # the archway the road runs through
    p = skia.Path()
    p.moveTo(x0 + 24, DECK_Y + 6)
    p.lineTo(x0 + 24, DECK_Y - 46)
    p.quadTo(x0 + 55, DECK_Y - 86, x1 - 24, DECK_Y - 46)
    p.lineTo(x1 - 24, DECK_Y + 6)
    p.close()
    c.drawPath(p, P(mix("#3A2F45", "#1A1525", night)))
    if night > 0:
        c.drawRect(R(x0, top, 110, LAND_Y - top), P("#0A0F25", 0.45 * night))
    if lit > 0:
        add_glow(c, (x0 + x1) / 2, top + 30, 90, "#FDE68A", 0.4 * lit)


def half_arch(c, side, b, night=0.0, lit=0.0, col=None, a=1.0):
    """One half of the arch, built from its bearing out to fraction b of the half (1 = to the crown)."""
    if b <= 0 or a <= 0:
        return
    sd = -1 if side == "L" else 1
    n = b * NP
    full = int(n)
    pts = []
    for k in range(full + 1):
        i = k if sd < 0 else 2 * NP - k
        pts.append(px_at(i))
    if n > full:
        i = n if sd < 0 else 2 * NP - n
        pts.append(px_at(i))
    light, mid, dark = col or STEEL_C
    if night > 0:
        light, mid, dark = (mix(light, "#3A4458", 0.55 * night), mix(mid, "#262E3E", 0.55 * night), mix(dark, "#141A26", 0.4 * night))
    # web: verticals and diagonals
    for j in range(len(pts)):
        x = pts[j]
        c.drawLine(x, yt(x) + 4, x, yb(x) - 3, P(mid, a, stroke=5))
        if j > 0:
            xa = pts[j - 1]
            if j % 2:
                c.drawLine(xa, yt(xa) + 4, x, yb(x) - 3, P(mid, a, stroke=4))
            else:
                c.drawLine(xa, yb(xa) - 3, x, yt(x) + 4, P(mid, a, stroke=4))
    for f, wdt in ((yt, 15), (yb, 17)):
        path = skia.Path()
        x_from = pts[0]
        x_to = pts[-1]
        steps = max(2, int(abs(x_to - x_from) / 8))
        for k in range(steps + 1):
            x = lerp(x_from, x_to, k / steps)
            (path.moveTo if k == 0 else path.lineTo)(x, f(x))
        c.drawPath(path, P(dark, a, stroke=wdt + 4))
        c.drawPath(path, P(light, a, stroke=wdt - 5))
    if lit > 0:                                           # lights along the top chord
        for x in pts[::1]:
            add_glow(c, x, yt(x) - 4, 16, "#FFF1C2", 0.9 * lit)
            c.drawCircle(x, yt(x) - 4, 3.5, P("#FFFBEA", lit))
    # the bearing (hinge pin) at the foot
    xb = X0 if sd < 0 else X1
    c.drawCircle(xb, BEAR_Y - 2, 13, P(dark, a))
    c.drawCircle(xb, BEAR_Y - 2, 6, P(light, a))


def tip_x(side, b):
    n = b * NP
    return px_at(n) if side == "L" else px_at(2 * NP - n)


def deck(c, night=0.0, lit=0.0, full=True):
    x0, x1 = (-60, W + 60) if full else (-60, X0 - 100)
    for xa, xb_ in ((x0, x1),) if full else ((-60, X0 - 100), (X1 + 100, W + 60)):
        c.drawRect(R(xa, DECK_Y - 9, xb_ - xa, 22), P(mix("#5B6475", "#262C38", night)))
        c.drawRect(R(xa, DECK_Y - 13, xb_ - xa, 6), P(mix("#8D96A6", "#3A4250", night)))
    if full:
        for k in range(1, 2 * NP):                       # hangers
            x = px_at(k)
            if yb(x) < DECK_Y - 14:
                c.drawLine(x, yb(x), x, DECK_Y - 10, P(mix("#6B7586", "#2C3442", night), 1, stroke=3))
        if lit > 0:
            for k in range(22):
                x = 20 + k * 49
                add_glow(c, x, DECK_Y - 18, 14, "#FDE68A", 0.7 * lit)


def cables(c, side, k=1.0, glow=0.0, slack=0.0):
    """The cables that hold a half back: from its top chord, over the pylon, down into the tunnel."""
    if k <= 0:
        return
    sd = -1 if side == "L" else 1
    xb = X0 if sd < 0 else X1
    py = (X0 - 57) if sd < 0 else (X1 + 57)
    tx = xb + sd * 80
    for j in range(5):
        ax = xb - sd * (60 + j * 26)
        ay = yt(ax) + 2
        mx_, my_ = lerp(ax, py, 0.5), lerp(ay, PY_TOP - 30, 0.5) + 10 + slack * 30
        p = skia.Path()
        p.moveTo(ax, ay)
        p.quadTo(mx_, my_, py, PY_TOP - 30)
        p.lineTo(tx + (j - 2) * 7, TUN_Y)
        m = skia.PathMeasure(p, False)
        seg = skia.Path()
        m.getSegment(0, m.getLength() * clamp(k), seg, True)
        c.drawPath(seg, P("#1F2633", 1, stroke=6))
        c.drawPath(seg, P("#C9D1DC", 0.7, stroke=2))
        if glow > 0:
            c.drawPath(seg, P("#FACC15", 0.55 * glow, stroke=5))


def creeper(c, side, b, t, a=1.0, lift=0.5, load=True):
    """A creeper crane riding the top chord at the tip of a half: lattice mast, short jib out over the tip."""
    if a <= 0:
        return
    sd = -1 if side == "L" else 1
    x = tip_x(side, max(0.02, b)) + sd * 16
    y = yt(x) - 5
    slope = (yt(x + 2) - yt(x - 2)) / 4
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(math.atan(slope)))
    c.drawRRect(rr(-30, -16, 60, 16, 4), P("#9A3412", a))
    c.drawCircle(-18, 0, 6, P("#1F2937", a))
    c.drawCircle(18, 0, 6, P("#1F2937", a))
    c.restore()
    top = y - 120
    c.drawLine(x - 7, y - 14, x - 7, top, P("#F59E0B", a, stroke=4))
    c.drawLine(x + 7, y - 14, x + 7, top, P("#F59E0B", a, stroke=4))
    for k in range(6):
        y0_ = y - 14 - k * 18
        c.drawLine(x - 7, y0_, x + 7, y0_ - 18, P("#D97706", a, stroke=2))
    c.drawRect(R(x - 13, top - 16, 26, 18), P("#B45309", a))
    jx = x - sd * 84                                     # jib out over the tip (toward the gap)
    c.drawLine(x, top - 6, jx, top, P("#F59E0B", a, stroke=6))
    c.drawLine(x, top - 30, jx, top, P("#D97706", a, stroke=2))
    c.drawLine(x, top - 30, x, top - 8, P("#D97706", a, stroke=4))
    c.drawLine(x, top - 6, x + sd * 34, top - 4, P("#F59E0B", a, stroke=6))
    c.drawRect(R(x + sd * 34 - 10, top - 4, 20, 18), P("#6B7280", a))
    hook_y = lerp(WATER_Y - 30, top + 60, lift)
    c.drawLine(jx, top, jx, hook_y, P("#E5E7EB", 0.85 * a, stroke=2))
    if load:
        c.drawRect(R(jx - 26, hook_y, 52, 14), P(STEEL_C[1], a))
        c.drawRect(R(jx - 26, hook_y, 52, 4), P(STEEL_C[0], a))


def barge(c, x, t, a=1.0):
    c.drawRect(R(x - 70, WATER_Y - 18, 140, 26), P("#3F3A4A", a))
    c.drawRect(R(x - 62, WATER_Y - 30, 40, 14), P(STEEL_C[1], a))


def ship(c, x, s=1.0, night=0.0, a=1.0):
    """A ferry sailing across (side view)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, WATER_Y + 4)
    c.scale(s, s)
    hull = skia.Path()
    hull.moveTo(-120, -30)
    hull.lineTo(120, -30)
    hull.lineTo(96, 6)
    hull.lineTo(-104, 6)
    hull.close()
    c.drawPath(hull, P(mix("#1F6E43", "#0E3A24", night), a))
    c.drawRect(R(-90, -62, 170, 32), P(mix("#F1E7C8", "#6B6656", night), a))
    c.drawRect(R(-60, -86, 100, 24), P(mix("#E7DCC0", "#5C584A", night), a))
    for k in range(7):
        c.drawRect(R(-82 + k * 23, -54, 12, 12), P("#2B3A55", a))
    c.drawRect(R(-12, -112, 18, 28), P("#B91C1C", a))
    c.restore()


def ghost_pillars(c, t, a=1.0, cross=0.0):
    if a <= 0:
        return
    for x in (345, 540, 735):
        c.drawRect(R(x - 30, 560, 60, WATER_Y + 80 - 560), P("#F8FAFC", 0.12 * a))
        dashed(c, x - 30, WATER_Y + 80, x - 30, 560, "#F8FAFC", 5, 16, 10, t * 30, 0.85 * a)
        dashed(c, x + 30, WATER_Y + 80, x + 30, 560, "#F8FAFC", 5, 16, 10, t * 30, 0.85 * a)
        if cross > 0:
            k = e_back(clamp(cross))
            c.drawLine(x - 70 * k, 700 - 70 * k, x + 70 * k, 700 + 70 * k, P(WARN, a, stroke=16))
            c.drawLine(x + 70 * k, 700 - 70 * k, x - 70 * k, 700 + 70 * k, P(WARN, a, stroke=16))


def shore_crane(c, x, t, a=1.0, reach=0.0):
    """An ordinary crane on a barge: its jib stops far below the arch's tip."""
    if a <= 0:
        return
    base = WATER_Y + 6
    c.drawRect(R(x - 90, base - 22, 180, 30), P("#3F3A4A", a))
    c.drawRect(R(x - 40, base - 46, 80, 26), P("#B45309", a))
    c.drawLine(x - 7, base - 46, x - 7, base - 190, P("#F59E0B", a, stroke=5))
    c.drawLine(x + 7, base - 46, x + 7, base - 190, P("#F59E0B", a, stroke=5))
    for k in range(7):
        y0_ = base - 46 - k * 20
        c.drawLine(x - 7, y0_, x + 7, y0_ - 20, P("#D97706", a, stroke=2))
    jx, jy = x + 110, base - 198
    c.drawLine(x, base - 190, jx, jy, P("#F59E0B", a, stroke=7))
    c.drawLine(x, base - 190, x - 50, base - 186, P("#F59E0B", a, stroke=7))
    c.drawRect(R(x - 66, base - 190, 24, 26), P("#6B7280", a))
    if reach > 0:
        tx, ty = tip_x("L", 0.66), yt(tip_x("L", 0.66))
        dashed(c, jx, jy, lerp(jx, tx, reach), lerp(jy, ty, reach), WARN, 6, 14, 10, t * 40, a)
        if reach >= 1:
            c.drawCircle(tx, ty, 30, P(WARN, a, stroke=7))


def locomotive(c, x, y, s, t, ph=0.0, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-40, -34, 62, 28, 10), P("#1F2937", a))          # boiler
    c.drawRect(R(18, -48, 26, 42), P("#111827", a))                  # cab
    c.drawRect(R(-34, -52, 10, 20), P("#111827", a))                 # chimney
    c.drawRect(R(-44, -8, 92, 8), P("#B91C1C", a))
    for wx in (-28, -6, 16, 34):
        c.drawCircle(wx, 4, 9, P("#374151", a))
        c.drawCircle(wx, 4, 3, P("#9CA3AF", a))
    c.restore()
    if a > 0:
        for k in range(3):
            q = ((t * 0.7 + ph + k * 0.33) % 1.0)
            puff(c, x - 29 * s + q * 20, y - 60 * s - q * 70 * s, (10 + q * 22) * s, "#E5E7EB", 0.45 * (1 - q) * a)


def fireworks(c, t, t0, x, y, col, seed=0, r=150):
    if t < t0:
        return
    q = (t - t0) % 2.2
    if q > 1.6:
        return
    k = e_out(clamp(q / 0.9))
    fade = 1 - clamp((q - 0.8) / 0.8)
    rng = random.Random(seed)
    for j in range(26):
        ang = j / 26 * math.tau + rng.uniform(-0.05, 0.05)
        rr_ = r * k * rng.uniform(0.75, 1.0)
        px_, py_ = x + math.cos(ang) * rr_, y + math.sin(ang) * rr_ + q * q * 40
        c.drawCircle(px_, py_, 4.5, P(col, fade))
        add_glow(c, px_, py_, 14, col, 0.5 * fade)
    add_glow(c, x, y, r * 0.7, col, 0.18 * fade)


def opera(c, x, night=0.0, a=1.0):
    """The Opera House's sails on their point in the front right of the harbour."""
    base = 1085
    c.save()
    c.translate(x, base)
    c.scale(1.25, 1.25)
    c.translate(-x, -base)
    pt = skia.Path()
    pt.moveTo(x - 190, base + 10)
    pt.lineTo(x - 150, base - 18)
    pt.lineTo(x + 260, base - 18)
    pt.lineTo(x + 260, base + 40)
    pt.lineTo(x - 210, base + 40)
    pt.close()
    c.drawPath(pt, P(mix("#6B5A48", "#2A231C", night), a))
    c.drawRect(R(x - 120, base - 22, 250, 26), P(mix("#C9B48F", "#4A4234", night), a))
    for (dx, h, w, lean) in ((-80, 92, 70, 30), (-20, 120, 86, 38), (52, 86, 66, 28), (98, 54, 44, 18)):
        p = skia.Path()
        p.moveTo(x + dx - w / 2, base - 20)
        p.quadTo(x + dx - w * 0.1, base - 20 - h * 1.05, x + dx + lean, base - 20 - h)
        p.quadTo(x + dx + w * 0.25, base - 20 - h * 0.5, x + dx + w / 2, base - 20)
        p.close()
        c.drawPath(p, lin_paint(0, base - 20 - h, 0, base - 20, [mix("#F3EFE6", "#8E95A8", night), mix("#C9C4B8", "#4C5266", night)], a=a))
        c.drawPath(p, P(mix("#9A9488", "#2A2F3D", night), a, stroke=2))
    c.restore()


def bridge_scene(c, t, bl=1.0, br=1.0, night=0.0, lit=0.0, deck_full=True, cab=0.0, cab_glow=0.0, tunnel=0.0,
                 cranes=0.0, crane_lift=0.5, ships=0.0, tipL=0.0, closeL=0.0, closeR=0.0, trains=0.0, opera_a=0.0,
                 fw=0.0, ghost=0.0, cross=0.0, shore_cr=0.0, reach=0.0, join=0.0):
    sky(c, night)
    if night > 0.3:
        v2.moon(c, 900, 360, 46, a=night)
    city(c, t, lit=max(lit, night * 0.6))
    if fw > 0:
        for j, (x, y, col) in enumerate(((260, 420, "#F472B6"), (810, 400, "#FACC15"), (540, 350, "#60A5FA"), (130, 600, "#34D399"),
                                         (950, 590, "#F97316"))):
            fireworks(c, t, 0.0 + j * 0.45, x, y, col, seed=j, r=140 + 30 * (j % 2))
    water(c, t, night)
    if ships > 0:
        ship(c, lerp(-180, W + 200, ((t * 0.07) % 1.0)), 1.0, night, ships)
    ghost_pillars(c, t, ghost, cross)
    shore(c, "L", night, tunnel, t)
    shore(c, "R", night, tunnel, t)
    deck(c, night, lit, full=deck_full)
    cables(c, "L", cab, cab_glow)
    cables(c, "R", cab, cab_glow)
    # the left half may tip (break2) or be held a little up before the closing (reveal)
    c.save()
    c.rotate(tipL * 24 - closeL * 2.6, X0, BEAR_Y)
    half_arch(c, "L", bl, night, lit)
    creeper(c, "L", bl, t, cranes, crane_lift)
    c.restore()
    c.save()
    c.rotate(closeR * 2.6, X1, BEAR_Y)
    half_arch(c, "R", br, night, lit)
    creeper(c, "R", br, t, cranes, crane_lift)
    c.restore()
    if join > 0:
        add_glow(c, XC, yt(XC) + 14, 120, "#FDE68A", 0.8 * join)
    pylon(c, "L", night, lit)
    pylon(c, "R", night, lit)
    shore_crane(c, 300, t, shore_cr, reach)
    if trains > 0:
        n = 22
        for j in range(n):
            x = lerp(-40, W + 40, j / (n - 1))
            locomotive(c, x, DECK_Y - 12, 0.55, t, ph=j * 0.17, a=clamp(trains * n - j))
    if opera_a > 0:
        opera(c, 850, night, opera_a)


# ====================================================================================== the heat close-up
def thermo(c, x, y, h, frac, a=1.0):
    c.drawRRect(rr(x - 18, y - h, 36, h, 18), P("#F8FAFC", 0.85 * a))
    c.drawRRect(rr(x - 9, y - h * clamp(frac), 18, h * clamp(frac), 9), P(WARN, a))
    c.drawCircle(x, y + 12, 28, P(WARN, a))
    c.drawCircle(x, y + 12, 28, P("#F8FAFC", 0.85 * a, stroke=4))


def heat_scene(c, t, sun=1.0, rise=0.0, temp=0.0, pin=0.0, ruler=0.0):
    vrect(c, 0, 0, W, 1250, ["#3B2A5A", "#8A3B52", "#E0784A", "#F2A65A"], [0.0, 0.4, 0.8, 1.0])
    if sun > 0:                                          # the sun, hot
        add_glow(c, 230, 420, 360, "#FDBA74", 0.5 * sun)
        c.drawCircle(230, 420, 110, P("#FFE7A3", sun))
        for k in range(12):
            ang = k / 12 * math.tau + t * 0.4
            c.drawLine(230 + math.cos(ang) * 135, 420 + math.sin(ang) * 135, 230 + math.cos(ang) * 175,
                       420 + math.sin(ang) * 175, P("#FFE7A3", 0.8 * sun, stroke=8))
    c.save()                                             # the arch close up (crown region)
    c.translate(540, HEAT_SY)
    c.scale(HEAT_Z, HEAT_Z)
    c.translate(-540, -HEAT_WY)
    dash_a = clamp(rise * 3)
    if dash_a > 0:                                       # where it sat when cool
        for f in (yt, yb):
            path = skia.Path()
            for k in range(41):
                x = lerp(250, 830, k / 40)
                (path.moveTo if k == 0 else path.lineTo)(x, f(x))
            pp = P("#F8FAFC", 0.6 * dash_a, stroke=2.5)
            pp.setPathEffect(skia.DashPathEffect.Make([10, 8], t * 30))
            c.drawPath(path, pp)
    c.save()
    c.translate(0, -26 * smooth(rise))
    half_arch(c, "L", 1.0)
    half_arch(c, "R", 1.0)
    c.restore()
    for k in range(6):                                   # heat shimmer
        yy = yt(XC) - 70 + k * 22 + math.sin(t * 3 + k) * 4
        p = skia.Path()
        for j in range(21):
            x = 300 + j * 24
            (p.moveTo if j == 0 else p.lineTo)(x, yy + math.sin(t * 6 + j * 0.8 + k) * 5)
        c.drawPath(p, P("#FFF1D6", 0.25 * sun, stroke=2))
    c.restore()
    thermo(c, 900, 760, 300, 0.25 + 0.7 * temp, a=sun)
    if ruler > 0:                                        # +18 cm at the crown
        x = 720
        y0 = HEAT_SY + (yt(XC) - HEAT_WY) * HEAT_Z
        y1 = y0 - 26 * HEAT_Z * smooth(rise)
        c.drawLine(x, y0, x, y1, P(HILITE, ruler, stroke=8))
        poly(c, [(x - 16, y1 + 14), (x + 16, y1 + 14), (x, y1 - 8)], HILITE, ruler)
    if pin > 0:                                          # the hinge pin at the foot, in a lens
        cx, cy, r = 250, 1050, 150
        c.save()
        c.clipRRect(skia.RRect.MakeOval(R(cx - r, cy - r, 2 * r, 2 * r)), skia.ClipOp.kIntersect, True)
        c.drawRect(R(cx - r, cy - r, 2 * r, 2 * r), P("#1E2433", pin))
        c.drawRect(R(cx - r, cy + 40, 2 * r, r), P(GRANITE[2], pin))
        ang = math.sin(t * 2.2) * 6 * pin
        c.save()
        c.rotate(ang, cx, cy)
        c.drawRect(R(cx - 40, cy - 190, 80, 190), P(STEEL_C[1], pin))
        c.drawLine(cx - 40, cy - 190, cx + 40, cy - 60, P(STEEL_C[2], pin, stroke=6))
        c.restore()
        c.drawRRect(rr(cx - 80, cy + 10, 160, 40, 10), P(STEEL_C[2], pin))
        c.drawCircle(cx, cy, 44, P("#CBD5E1", pin))
        c.drawCircle(cx, cy, 44, P(STEEL_C[2], pin, stroke=6))
        c.drawCircle(cx, cy, 12, P(STEEL_C[2], pin))
        c.restore()
        c.drawCircle(cx, cy, r, P("#F8FAFC", 0.9 * pin, stroke=6))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#1A1222", "#07050C"]))


# ====================================================================================== the tag
def hanger_icon(c, k, t, a=1.0):
    """A coat hanger drawn over the arch: the hook on the crown."""
    if k <= 0:
        return
    p = skia.Path()
    p.moveTo(X0 - 20, BEAR_Y - 8)
    p.lineTo(X1 + 20, BEAR_Y - 8)
    p.lineTo(XC + 10, yt(XC) - 6)
    p.close()
    m = skia.PathMeasure(p, True)
    seg = skia.Path()
    m.getSegment(0, m.getLength() * clamp(k), seg, True)
    c.drawPath(seg, P(HILITE, a, stroke=10))
    hk = clamp((k - 0.6) / 0.4)
    if hk > 0:
        h = skia.Path()
        h.moveTo(XC + 10, yt(XC) - 6)
        h.lineTo(XC + 10, yt(XC) - 50)
        h.arcTo(R(XC - 40, yt(XC) - 150, 100, 100), 90, -250 * hk, False)
        c.drawPath(h, P(HILITE, a, stroke=10))
        add_glow(c, XC, yt(XC) - 60, 140, HILITE, 0.3 * hk * a)


def bedroom(c, t, ar=False, sad=0.0):
    vrect(c, 0, 0, W, 1250, ["#2B2F4A", "#3A3F5E"])
    c.drawRect(R(0, 1080, W, 170), lin_paint(0, 1080, 0, 1250, ["#4A3A30", "#2E241E"]))
    for k in range(10):
        c.drawLine(0, 1100 + k * 16, W, 1100 + k * 16, P("#3A2C24", 0.5, stroke=2))
    # the empty hook and hanger on the wall
    c.drawRect(R(700, 430, 220, 14), P("#8B6B4A"))
    c.drawCircle(810, 470, 10, P("#C9A24A"))
    hp = skia.Path()
    hp.moveTo(720, 600)
    hp.lineTo(900, 600)
    hp.lineTo(810, 520)
    hp.close()
    c.drawPath(hp, P("#E5E7EB", 1, stroke=7))
    c.drawLine(810, 520, 810, 478, P("#E5E7EB", 1, stroke=6))
    add_glow(c, 810, 560, 120, "#FDE68A", 0.25 + 0.25 * math.sin(t * 4) ** 2)
    if not ar:                                           # a chair buried in clothes, the coat on top
        c.drawRect(R(220, 760, 26, 330), P("#5B4636"))
        c.drawRect(R(440, 900, 26, 190), P("#5B4636"))
        c.drawRect(R(220, 740, 250, 40), P("#6E5642"))
        c.drawRect(R(200, 880, 290, 40), P("#6E5642"))
        for j, (dx, dy, w, h, col) in enumerate(((-10, -60, 300, 90, "#3B82F6"), (10, -110, 260, 70, "#F59E0B"),
                                                  (-30, -150, 320, 80, "#10B981"), (0, -205, 280, 90, "#7C3AED"))):
            c.drawRRect(rr(200 + dx, 900 + dy, w, h, 34), P(col))
        coat = skia.Path()
        coat.moveTo(180, 700)
        coat.quadTo(345, 620, 520, 700)
        coat.lineTo(560, 1000)
        coat.quadTo(470, 1020, 440, 960)
        coat.lineTo(250, 960)
        coat.quadTo(210, 1020, 140, 1000)
        coat.close()
        c.drawPath(coat, P("#9F2D2D"))
        c.drawPath(coat, P("#6F1D1D", 1, stroke=4))
    else:                                                # the couch with the white thobe thrown on it
        c.drawRRect(rr(90, 820, 560, 220, 50), P("#7C5A3A"))
        c.drawRRect(rr(60, 760, 120, 300, 40), P("#6A4C31"))
        c.drawRRect(rr(560, 760, 120, 300, 40), P("#6A4C31"))
        c.drawRRect(rr(150, 700, 440, 170, 40), P("#8D6A47"))
        thobe = skia.Path()
        thobe.moveTo(170, 830)
        thobe.quadTo(300, 760, 470, 820)
        thobe.lineTo(600, 900)
        thobe.quadTo(560, 1010, 440, 990)
        thobe.lineTo(230, 980)
        thobe.quadTo(150, 960, 170, 830)
        thobe.close()
        c.drawPath(thobe, P("#D9DEE6"))
        c.drawPath(thobe, P("#9AA3B2", 1, stroke=4))
        c.drawLine(330, 800, 300, 960, P("#AEB6C4", 1, stroke=3))
    if sad > 0:
        add_glow(c, 360, 860, 260, WARN, 0.15 * sad)


class HarbourBridge(EpisodeV2):
    BUILD_NO = 112
    FIRST_SET = "harbour"
    CLEAR = "#070B1C"
    COVER_T = ("closer", 0.55)
    STAT_Y = 1080
    TITLE = {"en": "SYDNEY HARBOUR BRIDGE", "ar_sa": "جسر ميناء سيدني"}
    EMPH = {"en": ["SYDNEY", "BRIDGE", "BOTH", "ENDS", "MEET", "PILLARS", "BUSY", "HARBOR", "HALVES", "HALF", "SHORE",
                   "PIECE", "TIP", "WATER", "THICK", "CABLES", "TUNNELS", "ROCK", "LIFT", "HIGH", "GIANT", "CRANES",
                   "CRAWLED", "GREW", "HOT", "SUN", "METAL", "GROW", "LOT", "MOVE", "EIGHTEEN", "CENTIMETERS", "FOLLOW",
                   "COASTER", "FIGHTER", "JET", "ANSWER", "BIT", "NIGHT", "TIPS", "TOUCHED", "NINETEEN", "MILLION",
                   "RIVETS", "NINETY-SIX", "TRAINS", "CONGRATS", "YOURSELF", "COATHANGER", "COAT", "CHAIR"],
            "ar_sa": ["سيدني", "الجسر", "الطرفين", "يتلاقون", "أعمدة", "ميناء", "سفن", "النصين", "شاطئه", "قطعة",
                      "قوس", "البحر", "بيطيح", "كيابل", "غليظة", "أنفاق", "الصخر", "ترفع", "لفوق", "رافعتين",
                      "زحفت", "يكبر", "الشمس", "تمدد", "الحديد", "كثير", "يتحرك", "بالحر", "يرتفع", "ثمنطعش", "متابعة",
                      "قطار", "الحربية", "الجواب", "رخوا", "شوي", "ليلة", "تلامسوا", "ملايين", "مسمار", "وتسعين",
                      "مبروك", "الشماعة", "ثوبك", "الكنب"]}
    KEYS = {"ar_sa": {
        ("hook", "SYDNEY"): "سيدني", ("hook", "BOTH"): "الطرفين", ("hook", "MEET"): "يتلاقون",
        ("break1", "PILLARS"): "أعمدة", ("break1", "BUSY"): "سفن", ("break1", "HOW"): "كيف",
        ("fix1", "HALF"): "نص", ("fix1", "SHORE"): "شاطئه", ("fix1", "PIECE"): "قطعة",
        ("break2", "WATER"): "البحر", ("break2", "TIP"): "بيطيح",
        ("fix2", "CABLES"): "كيابل", ("fix2", "TUNNELS"): "أنفاق", ("fix2", "ROCK"): "الصخر",
        ("break3", "LIFT"): "ترفع", ("break3", "HIGH"): "لفوق",
        ("fix3", "CRANES"): "رافعتين", ("fix3", "CRAWLED"): "زحفت", ("fix3", "GREW"): "يكبر",
        ("break4", "SUN"): "الشمس", ("break4", "GROW"): "تمدد", ("break4", "LOT"): "كثير",
        ("fix4", "MOVE"): "يتحرك", ("fix4", "HOT"): "بالحر", ("fix4", "EIGHTEEN"): "ثمنطعش",
        ("cta", "FOLLOW"): "متابعة", ("cta", "JET"): "الحربية",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "CABLES"): "الكيابل", ("reveal", "NIGHT"): "ليلة",
        ("reveal", "TOUCHED"): "تلامسوا",
        ("stat", "NINETEEN"): "ألف", ("stat", "SIX"): "ستة", ("stat", "TRAINS"): "قطار",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "COATHANGER"): "الشماعة", ("tag", "YOUR"): "ثوبك", ("tag", "CHAIR"): "الكنب"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a jet-launch coaster"),
                   "stat": [("1932", "OPENED"), ("6M", "RIVETS"), ("96", "TRAINS AS A TEST")],
                   "L": {"meet": "WILL THEY MEET?", "pillars": "NO PILLARS!", "how": "HOW DO THEY MEET?",
                         "shore": "EACH HALF FROM ITS SHORE", "tip": "IT WOULD TIP IN!", "cables": "CABLES IN ROCK TUNNELS",
                         "high": "TOO HIGH!", "cranes": "CRANES THAT CRAWL UP", "hot": "HOT METAL GROWS",
                         "move": "BUILT TO MOVE", "cm": "+18 CM", "letout": "LET THE CABLES OUT",
                         "touch": "AUG 1930: THEY TOUCH!", "name": "SYDNEY HARBOUR BRIDGE", "hanger": "THE COATHANGER",
                         "chair": "YOUR COAT..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قطار الموت"),
                      "stat": [("1932", "سنة الافتتاح"), ("6M", "مسمار"), ("96", "قطار للاختبار")],
                      "L": {"meet": "بيتلاقون؟", "pillars": "ممنوع أعمدة!", "how": "كيف يتلاقون؟",
                            "shore": "كل نص من شاطئه", "tip": "بيطيح في البحر!", "cables": "كيابل في أنفاق الصخر",
                            "high": "عالي مرة!", "cranes": "رافعات تزحف لفوق", "hot": "الحديد يتمدد",
                            "move": "مبني يتحرك", "cm": "+18 سانتي", "letout": "رخّوا الكيابل",
                            "touch": "أغسطس 1930: تلامسوا!", "name": "جسر ميناء سيدني", "hanger": "الشمّاعة",
                            "chair": "وثوبك..."}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "sydney": ("hook", "SYDNEY", 0.15), "both": ("hook", "BOTH", 0.5), "meet": ("hook", "MEET", 0.95),
            "pillars": ("break1", "PILLARS", 0.2), "busy": ("break1", "BUSY", 0.45), "how": ("break1", "HOW", 0.7),
            "half": ("fix1", "HALF", 0.1), "shore": ("fix1", "SHORE", 0.5), "piece": ("fix1", "PIECE", 0.8),
            "water": ("break2", "WATER", 0.5), "tip": ("break2", "TIP", 0.8),
            "cables": ("fix2", "CABLES", 0.15), "tunnels": ("fix2", "TUNNELS", 0.6), "rock": ("fix2", "ROCK", 0.9),
            "lift": ("break3", "LIFT", 0.4), "high": ("break3", "HIGH", 0.9),
            "cranes": ("fix3", "CRANES", 0.3), "crawled": ("fix3", "CRAWLED", 0.5), "grew": ("fix3", "GREW", 0.9),
            "sun": ("break4", "SUN", 0.15), "grow": ("break4", "GROW", 0.35), "lot": ("break4", "LOT", 0.8),
            "move": ("fix4", "MOVE", 0.25), "hot": ("fix4", "HOT", 0.5), "eighteen": ("fix4", "EIGHTEEN", 0.75),
            "follow": ("cta", "FOLLOW", 0.1), "jet": ("cta", "JET", 0.95),
            "answer": ("reveal", "ANSWER", 0.05), "letout": ("reveal", "CABLES", 0.25), "night": ("reveal", "NIGHT", 0.7),
            "touched": ("reveal", "TOUCHED", 0.92),
            "s1": ("stat", "NINETEEN", 0.05), "s2": ("stat", "SIX", 0.35), "s3": ("stat", "TRAINS", 0.8),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_hanger": ("tag", "COATHANGER", 0.3), "t_coat": ("tag", "YOUR", 0.65), "t_chair": ("tag", "CHAIR", 0.9)})
        T["pill1"] = max(T["pillars"], s("break1") + 0.3)
        T["shore1"] = max(T["shore"], T["half"] + 0.4)
        T["tip1"] = max(T["tip"], s("break2") + 0.3)
        T["rock1"] = max(T["rock"], T["cables"] + 0.5)
        T["high1"] = max(T["high"], s("break3") + 0.3)
        T["grew1"] = max(T["grew"], T["crawled"] + 0.4)
        T["lot1"] = max(T["lot"], s("break4") + 0.4)
        T["cm1"] = max(T["eighteen"], T["move"] + 0.4)
        T["touch1"] = max(T["touched"], T["letout"] + 0.8)
        T["t_coat1"] = max(T["t_coat"], s("tag") + 0.9)
        # ---- sets
        self.cut(s("break1") - 0.12, "build", 1)
        self.cut(s("break4") - 0.12, "heat", -1)
        self.cut(s("cta") - 0.12, "harbour", 1)
        self.cut(s("reveal") - 0.12, "close", -1)
        self.cut(s("stat") - 0.12, "harbour", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.cut(T["t_coat1"] - 0.12, "chair", 1)
        self.spans = [(T["pill1"], T["shore1"]), (T["tip1"], T["rock1"]), (T["high1"], T["grew1"]), (T["lot1"], T["cm1"])]
        self.shakes = [(T["meet"], 0.3, 4), (T["pill1"], 0.35, 6), (T["tip1"] + 0.3, 0.5, 9), (T["rock1"], 0.3, 5),
                       (T["high1"], 0.3, 5), (T["lot1"], 0.35, 5), (T["touch1"], 0.45, 8), (s("closer") + 0.2, 0.35, 6),
                       (T["t_chair"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: harbour (hook, cta, stat, closer)
    def draw_harbour(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["both"] - 0.3, s("break1") - 0.25))
            z = lerp(1.9, 1.0, k)
            fx, fy = XC, lerp(520, 700, k)
            c.save()
            c.translate(540, 700)
            c.scale(z, z)
            c.translate(-fx, -fy)
            grow = lerp(0.86, 0.93, prog(t, 0.0, T["meet"]))
            bridge_scene(c, t, bl=grow, br=grow, night=0.25, deck_full=False, cab=1.0, tunnel=0.0, cranes=1.0,
                         crane_lift=0.5 + 0.4 * math.sin(t * 1.3) ** 2)
            c.restore()
        elif ph == "stat":
            bridge_scene(c, t, night=0.1, lit=0.0, trains=prog(t, T["s3"] - 0.8, T["s3"] + 0.6), opera_a=1.0)
        elif ph == "closer":
            bridge_scene(c, t, night=1.0, lit=1.0, fw=1.0, opera_a=1.0)
        else:                                            # cta
            bridge_scene(c, t, night=0.55, lit=0.6, opera_a=1.0)

    def ui_harbour(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "meet", T["meet"] - 0.4, s("break1") + 0.1, accent=HILITE, size=58)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: build (break1 .. fix3)
    def draw_build(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break1":
            bridge_scene(c, t, bl=0.0, br=0.0, night=0.15, deck_full=False, ships=1.0,
                         ghost=prog(t, s("break1"), T["pillars"]), cross=prog(t, T["pill1"], T["pill1"] + 0.4))
        elif ph == "fix1":
            b = 0.55 * e_io(prog(t, T["half"] - 0.2, T["piece"] + 0.6))
            bridge_scene(c, t, bl=b, br=b, night=0.15, deck_full=False, ships=0.6)
        elif ph == "break2":
            tip = e_in(prog(t, T["water"] - 0.4, T["tip1"] + 0.3))
            bridge_scene(c, t, bl=0.55, br=0.55, night=0.15, deck_full=False, tipL=tip)
            if tip > 0.85:
                v2set.splash(c, tip_x("L", 0.55) + 120, WATER_Y, t, T["tip1"] + 0.25, dur=0.9, n=26, speed=620)
        elif ph == "fix2":
            k = prog(t, T["cables"] - 0.3, T["tunnels"])
            bridge_scene(c, t, bl=0.6, br=0.6, night=0.15, deck_full=False, cab=k, cab_glow=prog(t, T["tunnels"], T["rock1"] + 0.3),
                         tunnel=prog(t, T["tunnels"] - 0.3, T["tunnels"] + 0.2))
        elif ph == "break3":
            bridge_scene(c, t, bl=0.66, br=0.66, night=0.15, deck_full=False, cab=1.0, shore_cr=1.0,
                         reach=prog(t, T["lift"], T["high1"]))
        else:                                            # fix3
            b = lerp(0.66, 0.94, e_io(prog(t, T["crawled"] - 0.2, T["grew1"] + 0.6)))
            bridge_scene(c, t, bl=b, br=b, night=0.15, deck_full=False, cab=1.0, cranes=prog(t, T["cranes"] - 0.3, T["cranes"] + 0.2),
                         crane_lift=0.5 + 0.45 * math.sin(t * 1.6) ** 2)

    def ui_build(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "pillars", T["pillars"] - 0.2, T["how"] - 0.2, accent=WARN, size=62)
            self.chip(540, 300, "how", T["how"] - 0.2, s("fix1") - 0.1, accent=HILITE, size=56)
            self.badge("alert", T["pill1"], s("fix1") - 0.2, x=160, y=470)
            self.red(T["pill1"], 1.2)
        elif ph == "fix1":
            self.chip(540, 300, "shore", T["half"] - 0.2, s("break2") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["shore1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "tip", T["water"] - 0.3, s("fix2") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["tip1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["tip1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "cables", T["cables"] - 0.2, s("break3") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["rock1"], s("break3") - 0.15, x=160, y=470)
        elif ph == "break3":
            self.chip(540, 300, "high", T["lift"] - 0.2, s("fix3") - 0.15, accent=WARN, size=64)
            self.badge("alert", T["high1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["high1"], 1.2)
        else:
            self.chip(540, 300, "cranes", T["cranes"] - 0.2, s("break4") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["grew1"], s("break4") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: heat (break4, fix4)
    def draw_heat(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break4":
            heat_scene(c, t, sun=prog(t, s("break4"), T["sun"] + 0.3), temp=prog(t, T["sun"], T["lot1"] + 0.4))
        else:
            heat_scene(c, t, sun=1.0, temp=1.0, rise=prog(t, T["hot"] - 0.3, T["cm1"] + 0.3),
                       pin=prog(t, T["move"] - 0.3, T["move"] + 0.2), ruler=prog(t, T["cm1"] - 0.4, T["cm1"]))

    def ui_heat(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "hot", T["grow"] - 0.2, s("fix4") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["lot1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["lot1"], 1.2)
        else:
            self.chip(540, 300, "move", T["move"] - 0.2, T["cm1"] - 0.3, accent=GOOD, size=60)
            self.chip(540, 300, "cm", T["cm1"] - 0.3, s("cta") - 0.15, accent=HILITE, size=72)
            self.badge("check", T["cm1"], s("cta") - 0.15, x=880, y=470)

    # ------------------------------------------------------------------ set: close (reveal)
    def draw_close(self, c, t):
        T, s = self.T, self.tl.s
        let = e_io(prog(t, T["letout"] - 0.2, T["touch1"]))
        z = lerp(1.1, 1.55, e_io(prog(t, s("reveal"), T["letout"] + 0.6)))
        c.save()
        c.translate(540, 700)
        c.scale(z, z)
        c.translate(-XC, -560)
        bb = lerp(0.985, 1.0, let)
        bridge_scene(c, t, bl=bb, br=bb, night=1.0, lit=0.0, deck_full=False, cab=1.0, cab_glow=0.6 * (1 - prog(t, T["touch1"], T["touch1"] + 0.6)),
                     cranes=0.0,
                     closeL=1 - let, closeR=1 - let, join=prog(t, T["touch1"] - 0.05, T["touch1"] + 0.2) *
                     (1 - prog(t, T["touch1"] + 0.8, T["touch1"] + 1.6)))
        c.restore()
        if t >= T["touch1"] - 0.05:
            v2set.sparks_shower(c, 540, 700 + (yt(XC) - 560) * z, t, T["touch1"], dur=0.9, n=30, speed=640)

    def ui_close(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "letout", T["letout"] - 0.2, T["touch1"] - 0.2, accent=HILITE, size=56)
        self.chip(540, 300, "touch", T["touch1"] - 0.2, s("stat") - 0.15, accent=GOOD, size=52)

    # ------------------------------------------------------------------ set: tag (the coat hanger) + chair
    def draw_tag(self, c, t):
        T, s = self.T, self.tl.s
        bridge_scene(c, t, night=0.7, lit=0.7, opera_a=1.0)
        hanger_icon(c, e_io(prog(t, T["t_hanger"] - 0.3, T["t_hanger"] + 0.6)), t)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "hanger", T["t_hanger"] - 0.2, self.duration + 1, accent=HILITE, size=62)

    def draw_chair(self, c, t):
        T = self.T
        bedroom(c, t, ar=self.rtl, sad=prog(t, T["t_chair"] - 0.2, T["t_chair"] + 0.4))

    def ui_chair(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "chair", T["t_coat1"] - 0.1, self.duration + 1, accent=WARN, size=62)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1430", "#1A2246"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, rumble(3.0, 62), -22), (T["both"], sfx.clank(300.0, 0.6, 63), -12),
              (T["meet"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["busy"], sfx.hum(1.2, 70.0), -14),
               (T["pill1"], sfx.thunk(65), -6), (T["pill1"] + 0.2, sfx.alarm(3, 820.0), -14)]
        ev += [(T["half"], sfx.clank(420.0, 0.5, 66), -12), (T["shore"], sfx.clank(520.0, 0.5, 67), -12),
               (T["shore1"] + 0.3, sfx.chime(), -6)]
        ev += [(T["water"], sfx.creak(1.0, 68), -8), (T["tip1"] + 0.25, sfx.thud(0.6, 69), -4), (T["tip1"] + 0.35, sfx.hiss(0.6, 70), -12),
               (T["tip1"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(T["cables"], sfx.whirr(1.2, 140.0, 260.0, 71), -14), (T["tunnels"], sfx.thunk(72), -8), (T["rock1"] + 0.1, sfx.chime(), -6)]
        ev += [(T["lift"], sfx.creak(0.8, 73), -12), (T["high1"], sfx.buzz(), -12), (T["high1"] + 0.2, sfx.alarm(3, 820.0), -14)]
        ev += [(T["cranes"], sfx.whirr(1.6, 120.0, 200.0, 74), -14), (T["crawled"], sfx.clank(380.0, 0.5, 75), -12),
               (T["grew1"], sfx.ding(), -8), (T["grew1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 76), -6), (T["sun"], sfx.sizzle(0.8, 77), -12),
               (T["lot1"], sfx.creak(0.8, 78), -10), (T["lot1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(T["move"], sfx.creak(0.7, 79), -12), (T["cm1"], sfx.riser(0.6, 80), -12), (T["cm1"] + 0.2, sfx.ding(), -8),
               (T["cm1"] + 0.35, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["letout"], sfx.whirr(1.4, 90.0, 140.0, 95), -14),
               (T["touch1"], sfx.clank(240.0, 0.9, 96), -4), (T["touch1"] + 0.1, sfx.sparkle(1.0, 12, 97), -8),
               (T["touch1"] + 0.3, sfx.chime(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3),
               (T["s3"] - 0.6, sfx.hum(1.6, 60.0), -16)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (s("closer") + 0.4, boom(1.2, 103), -14),
               (s("closer") + 1.3, boom(1.2, 104), -16), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 105), -6), (T["t_hanger"], sfx.sparkle(0.8, 10, 106), -8),
               (T["t_coat1"] - 0.12, sfx.whoosh(0.4, True, 107), -8), (T["t_chair"], sfx.womp(), -8)]
        return ev


NAME = "harbourbridge"
EPISODE = HarbourBridge
