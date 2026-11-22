"""Episode 66 - Tower Bridge.  v2 look: London at golden hour over the Thames; the bridge seen from the side (the road
runs left-right): two stone towers on river piers, the two road halves (bascules) between them, the high walkways,
the side-span chains going off to the banks.

Sets: river (hook: both road halves stand up while a tall ship sails through the gap toward us, then they lie back
down and a red bus crosses; stat: wide by day; closer: at night, lit), map (break1: the Thames from above, the docks
upstream, a tall ship stopped by a low bridge), pier (fix1: the road cut in two, each half a seesaw on an axle with
its heavy end inside the tower; break2: 1,000+ tons that a worker cannot move; fix2: a counterweight, one small push
tips it up), engine (break3: 1894, a ship's horn and cold engines; fix3: steam engines pump water into accumulators
whose weights rise, then the stored water drives the road up), walk (break4: the road up, people stuck at the gate;
fix4: stairs inside the tower and the walkways 42 m up), bus (reveal: 1952, a double-decker on a rising half floors
it and jumps the gap), tag (EN: your bus leaving as you reach the stop; AR: the light turns green and the car behind
honks).
World: 1 m = 10 units, the road on y = 0, the river surface at y = 90, the gap at x = 0, the towers' inner faces at
x = +-300, each half turns on its axle at (+-300, 14).
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of, saudi_man  # noqa: E402
from bridge import car  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2A2A60", "horizon": "#4A3A7A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DUSKP = {"top": "#0A0A2A", "upper": "#24215C", "mid": "#6A3A78", "low": "#D0705E", "horizon": "#F6A86A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DAYP = {"top": "#1E3A8A", "upper": "#2F5DB8", "mid": "#5B8BD9", "low": "#9CC3EE", "horizon": "#E8D7B8",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STONE = "#DCCFB6"
STONE_S = "#BDAF95"
STONE_D = "#8E836C"
SLATE = "#47505E"
BLUE = "#8CC0E0"
BLUE_D = "#4E83AE"
STEELW = "#F1F5F9"
ROAD = "#3A3B42"
WATER = "#2E5560"
WATER_D = "#0F2329"
GRANITE = "#8A8A90"
BUSRED = "#DC2626"
PIV = 300.0          # distance of each axle from the gap
LEAF = 300.0         # axle to tip
TAIL = 118.0         # axle to the end of the heavy tail inside the pier


def river(c, x0, x1, t, night=0.0, a=1.0, y0=90.0):
    """The Thames from y0 down, with ripples and a shimmer under the bridge (world)."""
    c.drawRect(R(x0, y0, x1 - x0, 1600), lin_paint(0, y0, 0, y0 + 700, [mix(WATER, "#1A2A44", night), mix(WATER_D, "#060B18", night)], a=a))
    for k in range(9):
        yy = y0 + 14 + k * k * 9
        p_ = skia.Path()
        p_.moveTo(x0, yy)
        xx = x0
        while xx < x1:
            xx += 50
            p_.lineTo(xx, yy + math.sin(xx * 0.011 + t * (1.2 + k * 0.25) + k) * (2 + k * 0.8))
        c.drawPath(p_, P(mix("#BFE3EE", "#FFD98A", night), (0.28 - k * 0.025) * a, stroke=2.5 + k * 0.3))


def front_water(c, t, night=0.0, a=1.0):
    """The river in front of the piers, so they stand in the water (world)."""
    c.drawRect(R(-1800, 96, 3600, 1600), lin_paint(0, 96, 0, 700, [(mix(WATER, "#1A2A44", night), 0.92), (mix(WATER_D, "#060B18", night), 1.0)], a=a))
    c.drawRect(R(-1800, 88, 3600, 10), lin_paint(0, 88, 0, 98, [(mix(WATER, "#1A2A44", night), 0.0), (mix(WATER, "#1A2A44", night), 0.92)], a=a))
    for k in range(7):
        yy = 104 + k * k * 10
        p_ = skia.Path()
        p_.moveTo(-1800, yy)
        xx = -1800
        while xx < 1800:
            xx += 50
            p_.lineTo(xx, yy + math.sin(xx * 0.011 + t * (1.2 + k * 0.25) + k) * (2 + k * 0.8))
        c.drawPath(p_, P(mix("#BFE3EE", "#FFD98A", night), (0.26 - k * 0.03) * a, stroke=2.5 + k * 0.3))
    for sx in (-395, 395):                                       # reflections of the towers
        c.drawRect(R(sx - 80, 100, 160, 260), lin_paint(0, 100, 0, 360, [(mix("#E8D9B8", "#FFC46A", night), 0.22), ("#E8D9B8", 0.0)], a=a))


def far_bank(c, x0, x1, t, night=0.0, a=1.0, y=86.0):
    """London on the far bank: a row of buildings and a distant glass spire (world, standing on y)."""
    rng = random.Random(11)
    x = x0
    while x < x1:
        w, h = rng.uniform(40, 110), rng.uniform(40, 170)
        col = mix("#6A6E84", "#1C2142", night)
        c.drawRect(R(x, y - h, w, h), P(col, 0.9 * a))
        if night > 0:
            for k in range(int(h / 26)):
                if rng.random() < 0.55:
                    c.drawRect(R(x + 6, y - h + 10 + k * 26, w - 12, 5), P("#FFD58A", 0.6 * night * a))
        else:
            rng.random()
        x += w + rng.uniform(2, 24)
    sp = path_of([(560, y), (610, y - 560), (622, y - 600), (640, y)], close=True)      # the glass spire
    c.drawPath(sp, lin_paint(560, 0, 640, 0, [mix("#9FB4C8", "#2A3560", night), mix("#C9D8E6", "#3A4A7A", night)], a=0.85 * a))
    if night > 0:
        add_glow(c, 618, y - 590, 14, "#FF4D4F", 0.8 * night * a)
    c.drawRect(R(x0, y - 4, x1 - x0, 10), P(mix("#5A5E70", "#141832", night), a))


def chains(c, t, night=0.0, a=1.0):
    """The side spans: a curved steel truss from each tower down to the bank (world)."""
    for sd in (-1, 1):
        pts = []
        for k in range(21):
            u = k / 20.0
            x = sd * (490 + 900 * u)
            y = -300 + 300 * (1 - (1 - u) ** 2)
            pts.append((x, y))
        col = mix(BLUE, "#6A8FB8", night)
        c.drawPath(path_of(pts), P(col, a, stroke=16))
        c.drawPath(path_of([(x, y - 22) for x, y in pts]), P(STEELW, 0.8 * a, stroke=5))
        for x, y in pts[1::2]:                                   # hangers to the road
            c.drawLine(x, y, x, -2, P(col, 0.8 * a, stroke=4))
        c.drawRect(R(sd * 490 if sd > 0 else -1600, -4, 1110, 34), P(mix("#6B7A8C", "#2A3048", night), a))
        c.drawRect(R(sd * 490 if sd > 0 else -1600, -10, 1110, 8), P(ROAD, a))


def walkways(c, t, night=0.0, a=1.0, people=0.0):
    """The two high walkways between the towers (the front one shown), a light blue lattice (world)."""
    y0, y1 = -385.0, -330.0
    col = mix(BLUE, "#7A9CC8", night)
    c.drawRect(R(-300, y0, 600, 10), P(STEELW, a))
    c.drawRect(R(-300, y1 - 10, 600, 10), P(STEELW, a))
    for k in range(13):
        xa = -300 + k * 50
        c.drawLine(xa, y0 + 10, xa + 25, y1 - 10, P(col, a, stroke=6))
        c.drawLine(xa + 25, y1 - 10, xa + 50, y0 + 10, P(col, a, stroke=6))
    c.drawRect(R(-300, y0 + 10, 600, y1 - y0 - 20), P(col, 0.18 * a))
    if night > 0:
        for k in range(12):
            add_glow(c, -275 + k * 50, y1 - 4, 10, "#FFE9B0", 0.7 * night * a)
    if people > 0:
        for k in range(7):
            q = (t * 0.05 + k / 7.0) % 1.0
            person(c, lerp(-280, 280, q), y1 - 10, 30, ("#EF4444", "#2563EB", "#F59E0B", "#10B981")[k % 4], t + k,
                   pose="walk", face=1, a=a * people)


def tower(c, cx, t, lit=0.0, a=1.0, night=0.0, cut=0.0, stairs=0.0):
    """One tower, its river face, centred at x = cx, from the road (y = 0) up to its spires. cut 0..1 opens the face to
    show the stairs inside; stairs 0..1 moves people up them."""
    w = 190.0
    x0, x1 = cx - w / 2, cx + w / 2
    st, ss, sd = mix(STONE, "#8E8AA6", night * 0.6), mix(STONE_S, "#6E6A88", night * 0.6), mix(STONE_D, "#4A4862", night * 0.6)
    c.drawRect(R(x0, -470, w, 476), lin_paint(x0, 0, x1, 0, [ss, st, st, ss, sd], a=a))
    for yy in (-118, -250, -392):                                # string courses
        c.drawRect(R(x0 - 6, yy - 8, w + 12, 12), P(st, a))
        c.drawLine(x0 - 6, yy + 4, x1 + 6, yy + 4, P(sd, 0.6 * a, stroke=3))
    win = mix("#2A3550", "#FFD27A", lit)

    def lancet(xc, yb, ww, hh):
        p_ = skia.Path()
        p_.moveTo(xc - ww / 2, yb)
        p_.lineTo(xc - ww / 2, yb - hh + ww * 0.6)
        p_.quadTo(xc - ww / 2, yb - hh, xc, yb - hh - ww * 0.15)
        p_.quadTo(xc + ww / 2, yb - hh, xc + ww / 2, yb - hh + ww * 0.6)
        p_.lineTo(xc + ww / 2, yb)
        p_.close()
        c.drawPath(p_, P(win, a))
        c.drawPath(p_, P(sd, 0.8 * a, stroke=3))
    for k in (-1, 0, 1):
        lancet(cx + k * 44, -150, 26, 90)
        lancet(cx + k * 44, -280, 24, 80)
    for k in (-0.5, 0.5):
        lancet(cx + k * 60, -405, 30, 52)
    for sx in (x0, x1):                                          # corner turrets with pointed roofs
        tx = sx - 14 if sx == x0 else sx - 26
        c.drawRect(R(tx, -500, 40, 500), lin_paint(tx, 0, tx + 40, 0, [ss, st, sd], a=a))
        for yy in range(-470, -10, 60):
            c.drawRect(R(tx + 14, yy, 12, 26), P(win, 0.8 * a))
        rf = path_of([(tx - 4, -500), (tx + 20, -610), (tx + 44, -500)], close=True)
        c.drawPath(rf, lin_paint(tx, 0, tx + 44, 0, [shade(SLATE, 0.2), SLATE, shade(SLATE, -0.3)], a=a))
        c.drawLine(tx + 20, -610, tx + 20, -634, P("#E5C76B", a, stroke=4))
        c.drawCircle(tx + 20, -636, 5, P("#F2D27A", a))
    rf = path_of([(x0 + 22, -470), (cx, -560), (x1 - 22, -470)], close=True)        # the main roof and its lantern
    c.drawPath(rf, lin_paint(x0, 0, x1, 0, [shade(SLATE, 0.15), SLATE, shade(SLATE, -0.3)], a=a))
    c.drawRect(R(cx - 16, -592, 32, 36), P(ss, a))
    c.drawPath(path_of([(cx - 20, -592), (cx, -640), (cx + 20, -592)], close=True), P(SLATE, a))
    c.drawLine(cx, -640, cx, -664, P("#E5C76B", a, stroke=4))
    if lit > 0:
        add_glow(c, cx, -300, 260, "#FFC46A", 0.22 * lit * a)
    if cut > 0:                                                  # the face opened: stairs from the road to the walkway
        c.drawRect(R(x0 + 30, -380, w - 60, 372), P("#1C1A22", cut * a))
        pts = []
        for k in range(9):
            yy = -8 - k * 41
            pts += [(x0 + 40, yy), (x1 - 40, yy - 20)] if k % 2 == 0 else [(x1 - 40, yy), (x0 + 40, yy - 20)]
        c.drawPath(path_of(pts), P("#E8D9B8", cut * a, stroke=6))
        if stairs > 0:
            L = len(pts) - 1
            for k in range(5):
                q = (stairs * 1.2 - k * 0.16)
                if 0 < q < 1:
                    i = min(L - 1, int(q * L))
                    f = q * L - i
                    px_, py_ = lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)
                    person(c, px_, py_, 30, ("#EF4444", "#2563EB", "#F59E0B", "#10B981", "#A855F7")[k], t + k,
                           pose="walk", face=1, a=cut * a)


def pier(c, cx, t, night=0.0, a=1.0, cut=0.0):
    """The granite pier under a tower, from the road down into the river (world). cut 0..1 opens the chamber."""
    x0, x1 = cx - 110, cx + 110
    if cx < 0:
        x1 = -300.0
        x0 = x1 - 220
    else:
        x0 = 300.0
        x1 = x0 + 220
    col = mix(GRANITE, "#3A3A48", night)
    c.drawRect(R(x0, -4, x1 - x0, 900), lin_paint(x0, 0, x1, 0, [shade(col, -0.15), col, shade(col, -0.3)], a=a))
    for k in range(8):
        c.drawLine(x0, 20 + k * 40, x1, 20 + k * 40, P(shade(col, -0.35), 0.5 * a, stroke=2))
    if cut > 0:
        ix0, ix1 = (x0 + 18, x1) if cx < 0 else (x0, x1 - 18)
        c.drawRect(R(ix0, 8, ix1 - ix0, 176), P("#16141C", cut * a))
        c.drawRect(R(ix0, 8, ix1 - ix0, 176), P("#FDE047", 0.6 * cut * a, stroke=3))


def leaf(c, side, ang, t, a=1.0, night=0.0, tail=False, cw=0.0, traffic=0.0, jam=0.0):
    """One road half (bascule): side -1 = the left one, +1 = the right one, raised by ang degrees about its axle.
    tail=True also draws its heavy end (inside the pier: only for the cut-open views); cw 0..1 lights the counterweight."""
    if a <= 0:
        return
    d = -side                                                    # direction from the axle to the tip
    c.save()
    c.translate(side * PIV, 14)
    c.rotate(side * ang)
    xa, xb = min(0.0, d * LEAF), max(0.0, d * LEAF)
    gc = mix("#5E7F99", "#2A3A58", night)
    c.drawRect(R(xa, -12, xb - xa, 30), lin_paint(0, -12, 0, 18, [shade(gc, 0.2), gc, shade(gc, -0.3)], a=a))
    for k in range(int((xb - xa) / 30)):                         # the girder's lattice
        xx = xa + k * 30
        c.drawLine(xx, -10, xx + 30, 16, P(shade(gc, -0.35), 0.7 * a, stroke=3))
    c.drawRect(R(xa, -18, xb - xa, 7), P(mix(ROAD, "#1A1A22", night), a))
    for k in range(int((xb - xa) / 40)):                         # centre line
        c.drawRect(R(xa + 8 + k * 40, -16, 18, 2.5), P("#F8FAFC", 0.8 * a))
    c.drawLine(xa, -34, xb, -34, P(STEELW, 0.9 * a, stroke=3))   # railing
    for k in range(int((xb - xa) / 25) + 1):
        c.drawLine(xa + k * 25, -34, xa + k * 25, -18, P(STEELW, 0.7 * a, stroke=2))
    if night > 0:
        for k in range(3):
            xx = xa + 50 + k * 100
            c.drawLine(xx, -18, xx, -64, P("#9CA3AF", a, stroke=3))
            add_glow(c, xx, -66, 18, "#FFE3A0", 0.8 * night * a)
    if tail:
        tx0, tx1 = min(0.0, side * TAIL), max(0.0, side * TAIL)
        c.drawRect(R(tx0, -12, tx1 - tx0, 30), P(shade(gc, -0.1), a))
        bx0, bx1 = (side * TAIL, side * (TAIL - 62)) if side < 0 else (side * (TAIL - 62), side * TAIL)
        bx0, bx1 = min(bx0, bx1), max(bx0, bx1)
        c.drawRRect(rr(bx0, -24, bx1 - bx0, 74, 6), lin_paint(bx0, 0, bx1, 0, ["#5A5F6A", "#3A3F4A", "#2A2E36"], a=a))
        if cw > 0:
            c.drawRRect(rr(bx0, -24, bx1 - bx0, 74, 6), P("#FACC15", 0.55 * cw * a))
            c.drawRRect(rr(bx0, -24, bx1 - bx0, 74, 6), P("#FDE047", cw * a, stroke=4))
        c.drawCircle(0, 0, 16, P("#CBD5E1", a))                  # the axle
        c.drawCircle(0, 0, 16, P("#64748B", a, stroke=4))
        c.drawCircle(0, 0, 5, P("#334155", a))
    if traffic > 0 or jam > 0:
        for k in range(2):
            fx = d * (80 + k * 120)
            car(c, fx, -18, ("#F8FAFC", "#FCD34D")[k], 0.0, 1.1, face=-side if k == 0 else side)
    c.restore()


def leaf_tip(side, ang):
    """World position of a half's tip (on the road surface)."""
    q = math.radians(side * ang)
    lx, ly = -side * LEAF, -18.0
    return side * PIV + lx * math.cos(q) - ly * math.sin(q), 14 + lx * math.sin(q) + ly * math.cos(q)


def on_leaf(side, ang, dist):
    """World position on a half's road surface, dist units from the axle toward the tip, and its angle in degrees."""
    q = math.radians(side * ang)
    lx, ly = -side * dist, -18.0
    return side * PIV + lx * math.cos(q) - ly * math.sin(q), 14 + lx * math.sin(q) + ly * math.cos(q)


def ship_bow(c, x, y, s, t, a=1.0, night=0.0):
    """A tall ship seen bow-on: hull, one mast with square sails and rigging; waterline at (x, y), scale s."""
    if a <= 0 or s <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    sway = math.sin(t * 1.3) * 1.2
    c.rotate(sway)
    hull = path_of([(-62, -46), (62, -46), (40, 6), (-40, 6)], close=True)
    c.drawPath(hull, lin_paint(-62, 0, 62, 0, ["#1F2937", "#374151", "#111827"], a=a))
    c.drawRect(R(-60, -46, 120, 9), P("#F8FAFC", a))
    c.drawRect(R(-48, -24, 96, 6), P("#B45309", a))
    c.drawRect(R(-4, -380, 8, 334), P("#7C5A3A", a))             # the mast
    for k, (yy, hw) in enumerate(((-110, 92), (-190, 80), (-262, 62), (-322, 44))):
        c.drawLine(-hw, yy, hw, yy, P("#5B4630", a, stroke=6))   # yards
        sail = skia.Path()
        sail.moveTo(-hw + 6, yy + 4)
        sail.lineTo(hw - 6, yy + 4)
        sail.quadTo(hw * 0.95, yy + 40, hw - 10, yy + (70 if k < 3 else 52))
        sail.lineTo(-hw + 10, yy + (70 if k < 3 else 52))
        sail.quadTo(-hw * 0.95, yy + 40, -hw + 6, yy + 4)
        sail.close()
        c.drawPath(sail, lin_paint(-hw, 0, hw, 0, [mix("#E9DFC8", "#7A7690", night), mix("#FFF8E8", "#9A96B0", night),
                                                    mix("#D9CDB2", "#6A6680", night)], a=a))
    for sd in (-1, 1):
        c.drawLine(0, -380, sd * 60, -46, P("#3F3428", 0.7 * a, stroke=2))
        c.drawLine(0, -300, sd * 58, -46, P("#3F3428", 0.6 * a, stroke=2))
    flag = path_of([(4, -380), (40, -372 + math.sin(t * 6) * 3), (4, -362)], close=True)
    c.drawPath(flag, P("#EF4444", a))
    c.restore()


def bus(c, x, y, s, ang, t, a=1.0, face=-1, speed=0.0):
    """A red double-decker in side view, wheels on (x, y), tilted ang degrees, facing left (face -1) or right."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s * face, s)
    c.drawRRect(rr(-42, -46, 84, 40, 6), lin_paint(0, -46, 0, -6, ["#EF4444", BUSRED, "#991B1B"], a=a))
    c.drawRect(R(-40, -26, 80, 3), P("#F8FAFC", 0.9 * a))
    for row, yy in enumerate((-42, -22)):
        for k in range(5):
            c.drawRRect(rr(-36 + k * 15, yy, 12, 11 if row == 0 else 10, 2), P("#1E293B", a))
            c.drawRect(R(-35 + k * 15, yy + 1, 4, 4), P("#93C5FD", 0.5 * a))
    c.drawRRect(rr(30, -44, 10, 12, 2), P("#FDE68A", a))          # the front route sign
    c.drawCircle(-26, -6, 7, P("#111827", a))
    c.drawCircle(26, -6, 7, P("#111827", a))
    c.drawCircle(-26, -6, 3, P("#9CA3AF", a))
    c.drawCircle(26, -6, 3, P("#9CA3AF", a))
    c.drawCircle(41, -12, 2.6, P("#FEF3C7", a))
    if speed > 0:
        for k in range(4):
            c.drawLine(-50 - k * 6, -40 + k * 10, -90 - k * 16, -40 + k * 10, P("#FFFFFF", 0.6 * speed * a, stroke=3))
    c.restore()


def gate(c, x, y, a=1.0, shut=1.0):
    """A red-and-white barrier across the road (world, standing on y)."""
    c.drawRect(R(x - 5, y - 46, 10, 46), P("#E5E7EB", a))
    ln = 90 * shut
    for k in range(6):
        xa = x + k * ln / 6
        c.drawLine(xa, y - 38, xa + ln / 6, y - 38, P("#EF4444" if k % 2 else "#F8FAFC", a, stroke=7))


def finger(c, x, y, s, a=1.0, ang=0.0):
    """A pointing hand pressing down at (x, y) (screen or world)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    c.drawRRect(rr(-14, -120, 28, 100, 14), P("#E8B48A", a))
    c.drawRRect(rr(-30, -150, 60, 60, 22), P("#E8B48A", a))
    c.drawRRect(rr(-8, -40, 16, 18, 6), P("#F5D0B5", a))
    c.drawRRect(rr(-34, -200, 68, 56, 10), P("#2563EB", a))
    c.restore()


def balance_icon(c, x, y, s, tilt=0.0, a=1.0):
    """A simple scale: a beam on a post with two pans (screen)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-6, -10, 12, 80), P("#E5E7EB", a))
    c.drawRect(R(-40, 66, 80, 10), P("#E5E7EB", a))
    c.rotate(tilt)
    c.drawRect(R(-90, -14, 180, 8), P("#FDE047", a))
    for sx in (-80, 80):
        c.drawLine(sx, -10, sx - 18, 30, P("#FDE047", a, stroke=2.5))
        c.drawLine(sx, -10, sx + 18, 30, P("#FDE047", a, stroke=2.5))
        c.drawPath(path_of([(sx - 26, 30), (sx + 26, 30), (sx + 16, 40), (sx - 16, 40)], close=True), P("#FDE047", a))
    c.restore()


# ------------------------------------------------------------------------------------------ the map (break1)
RIVER_PTS = [(-120, 470), (180, 520), (420, 640), (600, 820), (720, 960), (860, 1060), (1220, 1130)]


def smooth(pts, n=10):
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i - 1)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(len(pts) - 1, i + 2)]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            out.append((0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * u + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2
                               + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3),
                        0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2
                               + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)))
    out.append(pts[-1])
    return out


RIVER_LINE = smooth(RIVER_PTS)


def along(pts, u):
    """Point and direction (degrees) at fraction u of a polyline."""
    L = [0.0]
    for i in range(1, len(pts)):
        L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    d = clamp(u) * L[-1]
    for i in range(1, len(pts)):
        if L[i] >= d:
            f = (d - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            x = lerp(pts[i - 1][0], pts[i][0], f)
            y = lerp(pts[i - 1][1], pts[i][1], f)
            return x, y, math.degrees(math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0]))
    return pts[-1][0], pts[-1][1], 0.0


def ship_top(c, x, y, ang, s, a=1.0, col="#F8FAFC"):
    """A sailing ship seen from above (screen), bow pointing along ang."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    hull = skia.Path()
    hull.moveTo(40, 0)
    hull.quadTo(20, -14, -34, -12)
    hull.lineTo(-40, 0)
    hull.lineTo(-34, 12)
    hull.quadTo(20, 14, 40, 0)
    hull.close()
    c.drawPath(hull, P("#7C5A3A", a))
    for k in (-18, 2, 22):
        c.drawLine(k, -22, k, 22, P(col, a, stroke=4))
        c.drawCircle(k, 0, 3, P("#3F2A1A", a))
    c.restore()


def thames_map(c, t, ship_u, blocked, a=1.0, lab=None):
    """The Thames from above: land, the river, the docks upstream with moored ships, the bridge (screen)."""
    c.drawRect(R(0, 0, W, H), P("#1A2335", a))
    rng = random.Random(4)
    for k in range(26):                                          # streets
        x0, y0 = rng.uniform(-100, W), rng.uniform(300, 1300)
        c.drawLine(x0, y0, x0 + rng.uniform(-300, 300), y0 + rng.uniform(-200, 200), P("#2B3650", 0.9 * a, stroke=rng.uniform(4, 9)))
    c.drawPath(path_of(RIVER_LINE), P("#2C5C86", a, stroke=170))
    c.drawPath(path_of(RIVER_LINE), P("#4F86B4", a, stroke=130))
    for k, (u, sd) in enumerate(((0.10, -1), (0.16, 1), (0.22, -1), (0.28, 1), (0.34, -1), (0.40, 1), (0.13, 1), (0.31, -1))):
        x, y, ang = along(RIVER_LINE, u)
        nx, ny = -math.sin(math.radians(ang)), math.cos(math.radians(ang))
        c.drawRect(R(x + nx * sd * 95 - 30, y + ny * sd * 95 - 20, 60, 40), P("#3A4660", a))     # dock basins
        ship_top(c, x + nx * sd * 48, y + ny * sd * 48, ang, 0.9, a)
    bx, by, bang = along(RIVER_LINE, 0.62)                       # the bridge across the river
    c.save()
    c.translate(bx, by)
    c.rotate(bang + 90)
    c.drawRect(R(-120, -14, 240, 28), P("#E5E7EB", a))
    for sx in (-60, 60):
        c.drawRect(R(sx - 18, -24, 36, 48), P("#CBD5E1", a))
    c.restore()
    if lab is not None:
        lab["bridge"] = (bx, by)
        lab["docks"] = along(RIVER_LINE, 0.25)[:2]
    if ship_u > 0:
        u = lerp(0.98, 0.665, ship_u)
        x, y, ang = along(RIVER_LINE, u)
        ship_top(c, x, y, ang + 180, 1.5, a, col="#FDE68A")
        if blocked > 0:
            c.drawCircle(bx, by, 70 + 20 * math.sin(t * 9), P(WARN, 0.8 * blocked * a, stroke=8))


# ------------------------------------------------------------------------------------------ the engine room (break3, fix3)
def engine_room(c, t, on=0.0, fill=0.0, release=0.0, cold=1.0, a=1.0):
    """Cutaway engine room (screen): a boiler, a steam engine with its flywheel, a pump, two accumulators whose
    weights rise as water is pumped in (fill 0..1), and the pipe out to the bridge; release 0..1 sends the water out."""
    c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#3A2418", "#5A3626", "#2A1810"]))
    for row in range(0, 40):                                     # brick courses
        yy = 380 + row * 24
        if yy > 1190:
            break
        off = 0 if row % 2 else 30
        for k in range(-1, 20):
            c.drawRect(R(k * 60 + off, yy, 56, 20), P("#7A4A36", 0.45))
    add_glow(c, 540, 420, 520, "#FFD9A0", 0.25)
    c.drawRect(R(0, 1190, W, 60), P("#33333A"))
    fire = on
    c.drawRRect(rr(50, 880, 250, 300, 36), lin_paint(50, 0, 300, 0, ["#5B6573", "#8A94A3", "#4B5563"]))      # the boiler
    for k in range(6):
        c.drawCircle(70 + k * 42, 900, 4, P("#2F3640"))
        c.drawCircle(70 + k * 42, 1160, 4, P("#2F3640"))
    c.drawRRect(rr(130, 1060, 90, 80, 10), P(mix("#1F2937", "#FB923C", fire)))
    if fire > 0:
        add_glow(c, 175, 1100, 130, "#FB923C", 0.7 * fire)
    c.drawRect(R(160, 740, 30, 140), P("#4B5563"))
    if fire > 0:
        for k in range(3):
            puff(c, 175 + k * 8, 720 - ((t * 70 + k * 40) % 120), 30 + k * 6, "#C7CCD4", 0.4 * fire)
    c.drawRRect(rr(310, 1040, 150, 76, 14), lin_paint(0, 1040, 0, 1116, ["#B0B8C4", "#7C8796", "#566070"]))   # the engine
    ang = t * 280 * on
    fx, fy, fr = 590, 1000, 112
    cxk, cyk = fx + 46 * math.cos(math.radians(ang)), fy + 46 * math.sin(math.radians(ang))
    c.drawLine(460, 1078, lerp(470, 520, 0.5 + 0.5 * math.cos(math.radians(ang))), 1078, P("#E5E7EB", stroke=12))
    c.drawLine(lerp(470, 520, 0.5 + 0.5 * math.cos(math.radians(ang))), 1078, cxk, cyk, P("#F3F4F6", stroke=10))
    c.drawCircle(fx, fy, fr, P("#5B6573", stroke=24))
    for k in range(6):
        q = math.radians(ang + k * 60)
        c.drawLine(fx, fy, fx + fr * math.cos(q), fy + fr * math.sin(q), P("#8A94A3", stroke=11))
    c.drawCircle(fx, fy, 22, P("#CBD5E1"))
    c.drawRRect(rr(660, 1110, 80, 70, 10), P("#475569"))         # the pump
    c.drawLine(740, 1160, 960, 1160, P("#1D4ED8", stroke=16))
    for k, axx in enumerate((800, 920)):                         # accumulators: a water ram under a heavy weight
        lift_k = fill * 130
        c.drawRect(R(axx - 34, 600, 68, 580), lin_paint(axx - 34, 0, axx + 34, 0, ["#7C8796", "#B0B8C4", "#566070"]))
        lvl = 1170 - fill * 540
        c.drawRect(R(axx - 24, lvl, 48, 1170 - lvl), P("#38BDF8", 0.9))
        c.drawRect(R(axx - 14, 600 - lift_k, 28, lift_k + 4), P("#E5E7EB"))
        c.drawRRect(rr(axx - 58, 470 - lift_k, 116, 130, 12), lin_paint(0, 470, 0, 600, ["#78716C", "#57534E", "#3A3633"]))
        c.drawRRect(rr(axx - 58, 470 - lift_k, 116, 130, 12), P("#D6D3D1", stroke=3))
    if 0 < fill < 1 and on > 0:
        for k in range(8):
            q = (t * 0.9 + k / 8) % 1.0
            c.drawCircle(lerp(745, 955, q), 1160, 6, P("#E0F2FE", 0.95))
    pipe = [(990, 1160), (990, 760), (500, 760)]                 # out to the bridge
    c.drawPath(path_of(pipe), P("#1D4ED8", stroke=16))
    if release > 0:
        L1, L2 = 400.0, 490.0
        for k in range(12):
            q = (t * 1.3 + k / 12) % 1.0
            d_ = q * (L1 + L2)
            px_, py_ = (990, 1160 - d_) if d_ < L1 else (990 - (d_ - L1), 760)
            c.drawCircle(px_, py_, 7, P("#E0F2FE", release))
    if cold > 0:
        c.drawRect(R(0, 0, W, H), P("#0B1220", 0.22 * cold))


def leaf_inset(c, x, y, w, h, t, ang, a=1.0, ship=1.0, horn=0.0):
    """A window on the bridge: the two halves raised by ang, a tall ship waiting behind the gap (screen)."""
    if a <= 0:
        return
    c.save()
    c.clipRRect(rr(x, y, w, h, 24))
    vrect(c, x, y, w, h, ["#24215C", "#6A3A78", "#D0705E", "#F6A86A"], a=a)
    c.translate(x + w / 2, y + h * 0.8)
    sc = w / 1120
    c.scale(sc, sc)
    c.drawRect(R(-900, 72, 1800, 600), P(WATER, a))
    if ship > 0:
        ship_bow(c, 0, 80, 0.62, t, a=a * ship)
        if horn > 0:
            for k in range(3):
                r_ = 50 + k * 50 + (t * 160) % 50
                p_ = skia.Path()
                p_.addArc(R(70 - r_, -200 - r_, 2 * r_, 2 * r_), -50, 100)
                c.drawPath(p_, P("#FFFFFF", 0.85 * horn * (1 - k / 3), stroke=12))
    for sd in (-1, 1):
        pier(c, sd * 395, t)
        tower(c, sd * 395, t, night=0.2)
    leaf(c, -1, ang, t, a=a)
    leaf(c, 1, ang, t, a=a)
    c.restore()
    c.drawRRect(rr(x, y, w, h, 24), P("#FFFFFF", 0.75 * a, stroke=4))


# ====================================================================================== the episode
class TowerBridge(EpisodeV2):
    BUILD_NO = 66
    FIRST_SET = "river"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "TOWER BRIDGE", "ar_sa": "جسر البرج"}
    EMPH = {"en": ["CONGRATS", "ROAD", "STAND", "LONDON", "SHIP", "THROUGH", "DOWN", "TOWER", "BRIDGE", "YOURSELF",
                   "BUSIEST", "DOCKS", "UPSTREAM", "TALL", "SHIPS", "PAST", "CUT", "TWO", "HALF", "GIANT", "SEESAW",
                   "AXLE", "HEAVY", "HIDDEN", "WEIGHS", "THOUSAND", "TONS", "BALANCE", "COUNTERWEIGHT", "SMALL",
                   "PUSH", "TIPS", "EIGHTEEN", "NINETY-FOUR", "POWER", "READY", "MOMENT", "STEAM", "ENGINES", "PUMP",
                   "WATER", "TANKS", "PRESSURE", "STORED", "PUSHES", "PEOPLE", "FOOT", "STUCK", "WAITING",
                   "WALKWAYS", "FORTY-TWO", "METERS", "CROSS", "TOP", "FOLLOW", "COLOSSEUM", "STORY", "NINETEEN",
                   "FIFTY-TWO", "OPENED", "DOUBLE-DECKER", "BUS", "DRIVER", "FLOORED", "JUMPED", "GAP", "EIGHT",
                   "HUNDRED", "LIFTS", "FREE", "FLEW", "LEAVES", "STOP"],
            "ar_sa": ["مبروك", "طريقك", "يوقف", "لندن", "سفينة", "ينسدح", "جسر", "البرج", "بيدك", "ميناء", "الجسر",
                      "والسفن", "الطويلة", "تمر", "فتقسم", "نصين", "الميزان", "محور", "الثقيل", "يوزن", "ألف", "طن",
                      "فتوازنه", "بثقل", "ودفّة", "صغيرة", "ترفع", "وثمنمية", "وتسعين", "والقوة", "جاهزة", "فمكاين",
                      "بخار", "تضخ", "خزانات", "ضغط", "مرفوع", "يوقفون", "ينتظرون", "ممرات", "البرجين", "اثنين",
                      "وأربعين", "يعبرون", "تابعني", "الكولوسيوم", "والسالفة", "سبعين", "انفتح", "باص", "دورين",
                      "والسوّاق", "دعس", "ونط", "الفتحة", "ثمنمية", "ببلاش", "طار", "تخضر", "يزمّر"]}
    KEYS = {"ar_sa": {
        ("hook", "STAND"): "يوقف", ("hook", "LONDON"): "لندن", ("hook", "SHIP"): "سفينه", ("hook", "THEN"): "وبعدين",
        ("hook", "DOWN"): "ينسدح", ("hook", "CONGRATS"): "مبروك", ("hook", "TOWER"): "جسر",
        ("break1", "DOCKS"): "ميناء", ("break1", "UPSTREAM"): "ورا", ("break1", "TALL"): "الطويله", ("break1", "PAST"): "تمر",
        ("fix1", "CUT"): "فتقسم", ("fix1", "TWO"): "نصين", ("fix1", "SEESAW"): "الميزان", ("fix1", "AXLE"): "محور",
        ("fix1", "HEAVY"): "الثقيل", ("fix1", "TOWER"): "البرج",
        ("break2", "WEIGHS"): "يوزن", ("break2", "THOUSAND"): "الف", ("break2", "TONS"): "طن",
        ("fix2", "BALANCE"): "فتوازنه", ("fix2", "COUNTERWEIGHT"): "بثقل", ("fix2", "SMALL"): "صغيره",
        ("fix2", "PUSH"): "ودفه", ("fix2", "TIPS"): "ترفع", ("fix2", "UP"): "كله",
        ("break3", "EIGHTEEN"): "الف", ("break3", "POWER"): "والقوه", ("break3", "READY"): "جاهزه",
        ("break3", "ARRIVES"): "طول",
        ("fix3", "STEAM"): "بخار", ("fix3", "PUMP"): "تضخ", ("fix3", "TANKS"): "خزانات", ("fix3", "PRESSURE"): "ضغط",
        ("fix3", "STORED"): "وهالمويه", ("fix3", "PUSHES"): "ترفع", ("fix3", "DEMAND"): "الطريق",
        ("break4", "ROAD"): "مرفوع", ("break4", "PEOPLE"): "يمشون", ("break4", "STUCK"): "يوقفون",
        ("break4", "WAITING"): "ينتظرون",
        ("fix4", "WALKWAYS"): "ممرات", ("fix4", "TOWERS"): "البرجين", ("fix4", "FORTY-TWO"): "اثنين",
        ("fix4", "CROSS"): "يعبرون", ("fix4", "TOP"): "فوق",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "STORY"): "والسالفه", ("reveal", "NINETEEN"): "سبعين", ("reveal", "OPENED"): "انفتح",
        ("reveal", "BUS"): "باص", ("reveal", "DRIVER"): "والسواق", ("reveal", "FLOORED"): "دعس",
        ("reveal", "JUMPED"): "ونط", ("reveal", "GAP"): "الفتحه",
        ("stat", "THOUSAND"): "الف", ("stat", "EIGHT"): "ثمنميه", ("stat", "FREE"): "ببلاش",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "BUS"): "باص", ("tag", "FLEW"): "طار", ("tag", "YOURS"): "وانت", ("tag", "LEAVES"): "تخضر",
        ("tag", "STOP"): "يزمر"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Colosseum"),
                   "stat": [("1,000+ t", "EACH HALF"), ("~800", "LIFTS A YEAR"), ("£0", "TO OPEN IT")],
                   "L": {"stand": "THE ROAD STANDS UP", "ship": "A TALL SHIP GOES THROUGH", "name": "TOWER BRIDGE, LONDON",
                         "docks": "LONDON'S BUSIEST DOCKS", "upstream": "UPSTREAM", "bridge": "YOUR BRIDGE",
                         "blocked": "TALL SHIPS CAN'T PASS", "cut": "CUT IN TWO", "seesaw": "A GIANT SEESAW",
                         "axle": "AXLE", "heavy": "HEAVY END, INSIDE THE TOWER", "tons": "1,000+ TONS A HALF",
                         "stuck": "WON'T BUDGE", "counter": "COUNTERWEIGHT", "push": "ONE SMALL PUSH",
                         "y1894": "1894", "ready": "POWER READY ANY MOMENT", "steam": "STEAM ENGINES",
                         "tank": "WATER UNDER PRESSURE", "stored": "STORED AND WAITING", "lift": "IT PUSHES THE ROAD UP",
                         "waitp": "PEOPLE STUCK WAITING", "walk": "WALKWAYS 42 M UP", "m42": "42 M",
                         "y1952": "1952", "floored": "THE DRIVER FLOORED IT!", "jumped": "AND JUMPED THE GAP",
                         "wait": "WAIT!!", "toot": "TOOT!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: الكولوسيوم"),
                      "stat": [("1,000+", "طن كل جهة"), ("800", "فتحة في السنة"), ("0", "ريال، ببلاش")],
                      "L": {"stand": "الطريق يوقف", "ship": "تمر سفينة", "name": "جسر البرج، لندن",
                            "docks": "أكبر ميناء في لندن", "upstream": "ورا الجسر", "bridge": "جسرك",
                            "blocked": "السفن الطويلة ما تمر", "cut": "نصين", "seesaw": "مثل الميزان",
                            "axle": "المحور", "heavy": "الطرف الثقيل داخل البرج", "tons": "أكثر من ألف طن",
                            "stuck": "ما يتحرك", "counter": "ثقل يقابله", "push": "دفّة صغيرة",
                            "y1894": "1894", "ready": "القوة جاهزة على طول", "steam": "مكاين بخار",
                            "tank": "موية تحت ضغط", "stored": "مخزّنة وجاهزة", "lift": "ترفع الطريق",
                            "waitp": "الناس ينتظرون", "walk": "ممرات فوق", "m42": "42 م",
                            "y1952": "1952", "floored": "السوّاق دعس!", "jumped": "ونط الفتحة",
                            "beep": "بيييب!", "green": "خضرا!", "toot": "توووت!"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stand": ("hook", "STAND", 0.15), "london": ("hook", "LONDON", 0.35), "ship": ("hook", "SHIP", 0.5),
            "then": ("hook", "THEN", 0.6), "down": ("hook", "DOWN", 0.7), "congrats": ("hook", "CONGRATS", 0.78),
            "tower": ("hook", "TOWER", 0.92),
            "docks": ("break1", "DOCKS", 0.25), "upstream": ("break1", "UPSTREAM", 0.4), "tall": ("break1", "TALL", 0.6),
            "past": ("break1", "PAST", 0.85),
            "cut": ("fix1", "CUT", 0.1), "two": ("fix1", "TWO", 0.25), "seesaw": ("fix1", "SEESAW", 0.45),
            "axle": ("fix1", "AXLE", 0.6), "heavy": ("fix1", "HEAVY", 0.75), "tower1": ("fix1", "TOWER", 0.92),
            "weighs": ("break2", "WEIGHS", 0.3), "thousand": ("break2", "THOUSAND", 0.6), "tons": ("break2", "TONS", 0.85),
            "balance": ("fix2", "BALANCE", 0.1), "counter": ("fix2", "COUNTERWEIGHT", 0.3), "small": ("fix2", "SMALL", 0.55),
            "push": ("fix2", "PUSH", 0.65), "tips": ("fix2", "TIPS", 0.75), "up": ("fix2", "UP", 0.95),
            "y1894": ("break3", "EIGHTEEN", 0.1), "power": ("break3", "POWER", 0.4), "ready": ("break3", "READY", 0.6),
            "arrives": ("break3", "ARRIVES", 0.92),
            "steam": ("fix3", "STEAM", 0.05), "pump": ("fix3", "PUMP", 0.2), "tanks": ("fix3", "TANKS", 0.35),
            "pressure": ("fix3", "PRESSURE", 0.5), "stored": ("fix3", "STORED", 0.65), "pushes": ("fix3", "PUSHES", 0.8),
            "demand": ("fix3", "DEMAND", 0.95),
            "rup": ("break4", "ROAD", 0.2), "people": ("break4", "PEOPLE", 0.45), "stuck": ("break4", "STUCK", 0.75),
            "waiting": ("break4", "WAITING", 0.92),
            "walkways": ("fix4", "WALKWAYS", 0.1), "towers": ("fix4", "TOWERS", 0.35), "f42": ("fix4", "FORTY-TWO", 0.5),
            "cross": ("fix4", "CROSS", 0.8), "top": ("fix4", "TOP", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "story": ("reveal", "STORY", 0.05), "y1952": ("reveal", "NINETEEN", 0.15), "opened": ("reveal", "OPENED", 0.3),
            "bus": ("reveal", "BUS", 0.45), "driver": ("reveal", "DRIVER", 0.65), "floored": ("reveal", "FLOORED", 0.75),
            "jumped": ("reveal", "JUMPED", 0.88), "gap": ("reveal", "GAP", 0.97),
            "s1": ("stat", "THOUSAND", 0.05), "s2": ("stat", "EIGHT", 0.4), "s3": ("stat", "FREE", 0.85),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_bus": ("tag", "BUS", 0.1), "t_flew": ("tag", "FLEW", 0.25), "t_yours": ("tag", "YOURS", 0.5),
            "t_leaves": ("tag", "LEAVES", 0.7), "t_stop": ("tag", "STOP", 0.95)})
        T["down"] = max(T["down"], T["ship"] + 0.6)
        T["past1"] = max(T["past"], T["tall"]) + 0.15
        T["tons1"] = max(T["tons"], T["thousand"]) + 0.15
        T["arr1"] = max(T["arrives"], T["ready"]) + 0.15
        T["wait1"] = max(T["waiting"], T["stuck"]) + 0.15
        T["up1"] = max(T["up"], T["tips"]) + 0.25
        T["heavy1"] = max(T["tower1"], T["heavy"]) + 0.25
        T["dem1"] = max(T["demand"], T["pushes"]) + 0.25
        T["top1"] = max(T["top"], T["cross"]) + 0.25
        T["jump1"] = max(T["jumped"], T["floored"] + 0.4)
        # ---- sets
        self.cut(s("break1") - 0.12, "map", 1)
        self.cut(s("fix1") - 0.12, "pier", -1)
        self.cut(s("break3") - 0.12, "engine", 1)
        self.cut(s("break4") - 0.12, "walk", -1)
        self.cut(s("reveal") - 0.12, "bus", 1)
        self.cut(s("stat") - 0.12, "river", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- river camera: close on the gap while the road stands up, out to the whole bridge by "congrats"
        cm = Camera(0, -170, 1.18)
        cm.key(0.05, 0, -172, 1.17, 0.5)
        cm.key(max(0.6, T["then"] - 0.4), 0, -190, 1.0, max(1.0, T["congrats"] - T["then"] + 0.5))
        cm.key(s("stat") - 0.12, 0, -200, 0.86, 0.0).key(s("stat"), 0, -202, 0.87, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -215, 1.08, 1.0).key(s("closer") + 0.9, 0, -218, 1.1, 3.0)
        self.cam = cm
        # ---- pier camera: the whole span while it is cut in two, then close on the left pier
        pc = Camera(0, -190, 1.0)
        pc.key(s("fix1") - 0.12, 0, -190, 1.0, 0.0)
        pc.key(T["axle"] - 0.45, -295, 105, 2.1, 0.7)
        pc.key(s("break2") - 0.12, -240, 90, 1.85, 0.0)
        pc.key(T["push"] - 0.3, -215, 40, 1.6, 1.2)
        self.pcam = pc
        wc = Camera(-560, -110, 2.0)
        wc.key(s("break4") - 0.12, -560, -110, 2.0, 0.0)
        wc.key(T["walkways"] - 0.3, -250, -210, 1.12, max(0.8, T["towers"] - T["walkways"] + 0.3))
        self.wcam = wc
        self.spans = [(T["past1"], T["heavy1"] + 0.3), (T["tons1"], T["up1"] + 0.3), (T["arr1"], T["dem1"] + 0.3),
                      (T["wait1"], T["top1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["past1"], 0.4, 7), (T["two"], 0.3, 6), (T["tons1"], 0.4, 7),
                       (T["arr1"], 0.35, 6), (T["wait1"], 0.3, 6), (T["jump1"] + 0.45, 0.5, 12), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ shared: the bridge in the world
    def bridge(self, c, t, angl, angr, night=0.0, lit=0.0, people=0.0, traffic=0.0, tint=0.0):
        chains(c, t, night)
        walkways(c, t, night, people=people)
        for cx in (-395.0, 395.0):
            pier(c, cx, t, night)
            tower(c, cx, t, lit=lit, night=max(night, tint))
        leaf(c, -1, angl, t, night=night, traffic=traffic)
        leaf(c, 1, angr, t, night=night, traffic=traffic)
        front_water(c, t, night)

    # ------------------------------------------------------------------ set: river (hook, stat, closer)
    def draw_river(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        closer = t >= s("closer") - 0.1
        stat = s("stat") - 0.12 <= t < s("closer") - 0.1
        night = prog(t, s("closer") - 0.1, s("closer") + 0.8) if closer else 0.0
        cx, cy, z = cam
        gy = (80 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=NIGHTP if closer else DAYP if stat else DUSKP, horizon_y=gy)
        if closer:
            v2.stars(c, W, H, t, 0.8 * night)
        elif not stat:
            add_glow(c, 820 - cx * 0.03, gy - 200, 460, "#FFB07A", 0.35)
        self.view(c, cam)
        far_bank(c, -1700, 1700, t, night, y=72)
        river(c, -1800, 1800, t, night, y0=72)
        hook = t < s("break1")
        ang = 0.0
        sq = -1.0
        if hook:
            up = e_io(prog(t, 0.1, T["stand"] + 0.45))
            dn = e_io(prog(t, T["down"] - 0.6, T["down"] + 0.35))
            ang = 86.0 * up * (1 - dn)
            sq = prog(t, 0.15, T["ship"] + 1.3)                  # the ship: far behind -> the gap -> toward us
        ss = lerp(0.42, 1.75, sq ** 1.4) if sq >= 0 else 0.0
        wl = (74 + 16 * (ss - 0.42) / 0.58) if ss < 1 else 90 + (ss - 1) * 170
        sa = 1 - prog(ss, 1.45, 1.75) if sq >= 0 else 0.0
        if 0 < ss < 1:
            ship_bow(c, 0, wl, ss, t, a=sa, night=night)
        bus_on = (T["congrats"] - 0.4 <= t < s("break1")) or stat or closer
        self.bridge(c, t, ang, ang, night=night, lit=max(night, 0.0 if stat else 0.35), traffic=1.0 if (stat or closer) else 0.0,
                    tint=0.0 if stat else 0.22)
        if bus_on:
            bt = (t - (T["congrats"] - 0.4)) if hook or t < s("break1") else (t - s("stat") + 2.0)
            bx = -640 + ((bt * 150) % 1400)
            c.save()                                             # the road runs through the towers: hide the bus there
            c.clipRect(R(-490, -700, 190, 760), skia.ClipOp.kDifference)
            c.clipRect(R(300, -700, 190, 760), skia.ClipOp.kDifference)
            bus(c, bx, -18, 1.0, 0.0, t, face=1)
            c.restore()
        if ss >= 1 and sa > 0:
            ship_bow(c, 0, wl, ss, t, a=sa, night=night)
        if hook:
            self.ui["gap"] = self.to_screen(cam, 0, -150)
        c.restore()
        self.ui["cam"] = cam

    def ui_river(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "stand", T["stand"] - 0.1, T["ship"] - 0.2, accent="#FDE047", size=46)
            self.chip(540, 300, "ship", T["ship"] - 0.2, T["congrats"] - 0.2, accent="#93C5FD", size=44)
            self.chip(540, 300, "name", T["tower"] - 0.3, s("break1") + 0.1, accent=HILITE, size=46)

    # ------------------------------------------------------------------ set: map (break1)
    def draw_map(self, c, t):
        T = self.T
        su = e_io(prog(t, T["tall"] - 0.5, T["past1"]))
        blk = prog(t, T["past1"] - 0.1, T["past1"] + 0.2)
        lab = {}
        thames_map(c, t, su, blk, lab=lab)
        dx, dy = lab["docks"]
        self.ui["docks"] = (dx, dy)
        self.ui["bridge"] = lab["bridge"]
        k = prog(t, T["upstream"] - 0.3, T["upstream"] + 0.3)
        if k > 0:
            bx, by = lab["bridge"]
            arrow(c, bx - 30, by - 60, dx + 90, dy + 60, "#FDE047", a=k, w=10, head=28)

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        dx, dy = self.ui.get("docks", (300, 600))
        self.label(dx, dy, 330, 470, "docks", T["docks"] - 0.2, s("fix1") - 0.2, accent="#93C5FD", size=38)
        bx, by = self.ui.get("bridge", (700, 980))
        self.label(bx, by, 780, 860, "bridge", T["docks"] + 0.2, s("fix1") - 0.2, accent="#E5E7EB", size=36)
        self.chip(540, 300, "upstream", T["upstream"] - 0.2, T["tall"] - 0.1, accent="#FDE047", size=46)
        self.chip(540, 300, "blocked", T["past1"] - 0.2, s("fix1") - 0.15, accent=WARN, size=44)
        self.badge("alert", T["past1"], s("fix1") - 0.2, x=920, y=420)
        self.red(T["past1"], 1.2)

    # ------------------------------------------------------------------ set: pier (fix1, break2, fix2)
    def draw_pier(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.pcam.at(t)
        cx, cy, z = cam
        gy = (72 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        add_glow(c, 820, gy - 240, 520, "#FFC98A", 0.45)
        self.view(c, cam)
        far_bank(c, -1700, 1700, t, y=72)
        river(c, -1800, 1800, t, y0=72)
        close = t >= T["axle"] - 0.45
        cut = prog(t, T["axle"] - 0.3, T["axle"] + 0.3) if close else 0.0
        rock = 0.0
        if T["two"] - 0.1 <= t < T["heavy1"] + 0.6:              # each half rocks on its axle like a seesaw
            rk = prog(t, T["two"] - 0.1, T["two"] + 0.3) * (1 - prog(t, T["heavy1"], T["heavy1"] + 0.6))
            rock = 5.0 * math.sin((t - T["two"]) * 4.2) * rk
        angl = rock
        if t >= s("break2") - 0.12:
            angl = -0.6 * prog(t, T["weighs"], T["tons1"]) * (1 - prog(t, s("fix2") - 0.3, s("fix2")))
        if t >= s("fix2") - 0.12:
            angl = 42.0 * e_io(prog(t, T["push"] - 0.1, T["up1"] + 0.2))
        angr = -rock if t < T["seesaw"] + 0.2 else 0.0
        chains(c, t)
        walkways(c, t)
        pier(c, 395, t)
        tower(c, 395, t)
        leaf(c, 1, angr, t)
        pier(c, -395, t, cut=cut)
        tower(c, -395, t)
        cw = prog(t, T["counter"] - 0.2, T["counter"] + 0.3) if t >= s("fix2") - 0.12 else 0.0
        leaf(c, -1, angl, t, tail=cut > 0, cw=cw)
        front_water(c, t)
        k = prog(t, T["cut"] - 0.2, T["cut"] + 0.2) * (1 - prog(t, T["seesaw"] - 0.3, T["seesaw"]))
        if k > 0:                                                # the cut line through the middle of the road
            c.drawLine(0, -90, 0, 70, dash_paint("#FDE047", k, w=6, t=t, dash=16, gap=10))
        if t >= s("break2") - 0.12 and t < s("fix2") - 0.12:     # a worker cannot lift the tip
            tx, ty = leaf_tip(-1, angl)
            person(c, tx - 50, ty, 48, "#F59E0B", t, pose="carry", face=1, hat="hard")
            wk = prog(t, T["tons1"] - 0.3, T["tons1"])
            if wk > 0:
                for k2 in range(3):
                    arrow(c, -180 + k2 * 70, -120, -180 + k2 * 70, -40, WARN, a=wk, w=8, head=20)
        if t >= s("fix2") - 0.12:
            pk = prog(t, T["push"] - 0.4, T["push"]) * (1 - prog(t, T["up1"] + 0.3, T["up1"] + 0.7))
            if pk > 0:                                           # the small push on the heavy end
                q = math.radians(-angl)
                ex, ey = -PIV + (-TAIL) * math.cos(q), 14 + (-TAIL) * math.sin(q)
                arrow(c, ex, ey - 120, ex, ey - 40, GOOD, a=pk, w=10, head=26)
        q = math.radians(-angl)
        self.ui["axle"] = self.to_screen(cam, -PIV, 14)
        self.ui["tail"] = self.to_screen(cam, -PIV - 0.7 * TAIL * math.cos(q), 14 - 0.7 * TAIL * math.sin(q) + 20)
        self.ui["half"] = self.to_screen(cam, *on_leaf(-1, angl, 200))
        c.restore()
        self.ui["cam"] = cam

    def ui_pier(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break2") - 0.12:
            self.chip(540, 300, "cut", T["cut"] - 0.2, T["seesaw"] - 0.2, accent="#FDE047", size=50)
            self.chip(540, 300, "seesaw", T["seesaw"] - 0.2, s("break2") - 0.15, accent="#93C5FD", size=46)
            ax, ay = self.ui.get("axle", (540, 900))
            self.label(ax, ay, 760, 1150, "axle", T["axle"] - 0.2, s("break2") - 0.2, accent="#E5E7EB", size=36)
            tx, ty = self.ui.get("tail", (400, 1000))
            self.label(tx, ty, 330, 560, "heavy", T["heavy"] - 0.2, s("break2") - 0.2, accent="#FDE047", size=32)
            self.badge("check", T["heavy1"] + 0.1, s("break2") - 0.15, x=920, y=420)
            return
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "tons", T["weighs"] - 0.2, s("fix2") - 0.15, accent=WARN, size=48)
            hx, hy = self.ui.get("half", (700, 800))
            self.label(hx, hy, 760, 560, "stuck", T["tons1"] - 0.1, s("fix2") - 0.2, accent=WARN, size=36)
            self.badge("alert", T["tons1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["tons1"], 1.2)
            return
        tx, ty = self.ui.get("tail", (400, 1000))
        self.label(tx, ty, 330, 520, "counter", T["counter"] - 0.2, T["small"] - 0.1, accent="#FDE047", size=38)
        self.chip(540, 300, "push", T["small"] - 0.2, s("break3") - 0.15, accent=GOOD, size=48)
        bk = self.span(T["balance"] - 0.2, T["small"])
        if bk > 0:
            balance_icon(c, 860, 520, 1.0, tilt=0.0, a=bk)
        self.badge("check", T["up1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: engine (break3, fix3)
    def draw_engine(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        on = prog(t, T["steam"] - 0.3, T["steam"] + 0.2) if fixed else 0.0
        fill = prog(t, T["pump"], T["stored"]) if fixed else 0.0
        rel = prog(t, T["pushes"] - 0.2, T["pushes"] + 0.1) if fixed else 0.0
        cold = 1.0 - on
        engine_room(c, t, on=on, fill=fill, release=rel, cold=cold)
        ang = 80.0 * e_io(prog(t, T["pushes"], T["dem1"])) if fixed else 0.0
        horn = 0.0 if fixed else prog(t, T["ready"] - 0.4, T["ready"])
        leaf_inset(c, 60, 400, 440, 330, t, ang, horn=horn * (0.6 + 0.4 * math.sin(t * 12)))
        self.ui["acc"] = (860, 900)
        self.ui["fly"] = (590, 1000)

    def ui_engine(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "y1894", s("break3") - 0.1, T["power"] - 0.1, accent="#FDE68A", size=56)
            self.chip(540, 300, "ready", T["power"] - 0.1, s("fix3") - 0.15, accent=WARN, size=42)
            hk = self.span(T["ready"] - 0.4, s("fix3") - 0.15)
            if hk > 0:
                v2.chip(c, 400, 440, self.L["toot"], hk, accent="#FDE68A", size=34)
            self.badge("alert", T["arr1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["arr1"], 1.2)
            return
        fx, fy = self.ui.get("fly", (800, 980))
        self.label(fx, fy, 640, 860, "steam", T["steam"] - 0.2, T["tanks"] - 0.1, accent="#FB923C", size=38)
        ax, ay = self.ui.get("acc", (860, 900))
        self.label(ax, ay, 700, 1150, "tank", T["tanks"] - 0.1, T["stored"] - 0.1, accent="#38BDF8", size=36)
        self.chip(540, 300, "stored", T["stored"] - 0.2, T["pushes"] - 0.1, accent="#38BDF8", size=44)
        self.chip(540, 300, "lift", T["pushes"] - 0.1, s("break4") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["dem1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: walk (break4, fix4)
    def draw_walk(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = self.wcam.at(t)
        cx, cy, z = cam
        gy = (72 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        add_glow(c, 860, gy - 260, 520, "#FFC98A", 0.45)
        self.view(c, cam)
        far_bank(c, -1700, 1700, t, y=72)
        river(c, -1800, 1800, t, y0=72)
        chains(c, t)
        wp = prog(t, T["towers"] - 0.3, T["towers"] + 0.3) if fixed else 0.0
        walkways(c, t, people=wp)
        leaf(c, -1, 84.0, t)
        leaf(c, 1, 84.0, t)
        for cx_ in (395.0, -395.0):
            pier(c, cx_, t)
        tower(c, 395, t)
        cut = prog(t, T["walkways"] - 0.2, T["walkways"] + 0.3) if fixed else 0.0
        tower(c, -395, t, cut=cut, stairs=prog(t, T["walkways"], T["top1"] + 0.6) if fixed else 0.0)
        gate(c, -560, 0, shut=1.0)
        crowd = (-600, -640, -680, -720, -760, -800)
        for k, px_ in enumerate(crowd):
            pose = "look" if not fixed else "point" if k == 1 else "look"
            person(c, px_, -10, 40 + (k % 3) * 3, ("#EF4444", "#2563EB", "#F59E0B", "#10B981", "#A855F7", "#F472B6")[k], t + k * 0.3,
                   pose=pose if k % 2 else "stand", face=1)
        if fixed:                                                # the height of the walkway over the river
            mk = prog(t, T["f42"] - 0.3, T["f42"] + 0.1)
            if mk > 0:
                c.drawLine(-140, 90, -140, -330, P("#FDE047", mk, stroke=5))
                for yy in (90, -330):
                    c.drawLine(-160, yy, -120, yy, P("#FDE047", mk, stroke=5))
        self.ui["crowd"] = self.to_screen(cam, -680, -55)
        self.ui["walk"] = self.to_screen(cam, -100, -360)
        self.ui["m42"] = self.to_screen(cam, -140, -120)
        c.restore()

    def ui_walk(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            cx_, cy_ = self.ui.get("crowd", (200, 1100))
            self.label(cx_, cy_, 330, 640, "waitp", T["people"] - 0.2, s("fix4") - 0.2, accent=WARN, size=38)
            self.badge("alert", T["wait1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["wait1"], 1.2)
            return
        wx, wy = self.ui.get("walk", (600, 700))
        self.label(wx, wy, 760, 520, "walk", T["walkways"] - 0.1, s("cta") - 0.15, accent="#93C5FD", size=38)
        mx, my = self.ui.get("m42", (400, 900))
        v2.chip(c, mx + 110, my, self.L["m42"], self.span(T["f42"] - 0.2, s("cta") - 0.15), accent="#FDE047", size=40)
        self.badge("check", T["top1"] + 0.1, s("cta") - 0.15, x=920, y=640)

    # ------------------------------------------------------------------ set: bus (reveal), 1952
    def draw_bus(self, c, t):
        T, s = self.T, self.tl.s
        cam = (-30, -40, 2.25)
        cx, cy, z = cam
        gy = (72 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSKP, horizon_y=gy)
        add_glow(c, 820, gy - 260, 460, "#FFB07A", 0.4)
        self.view(c, cam)
        far_bank(c, -1700, 1700, t, y=72)
        river(c, -1800, 1800, t, y0=72)
        walkways(c, t)
        angr = 5.0 * e_io(prog(t, T["opened"] - 0.1, T["jump1"] + 0.2))
        for cx_ in (-395.0, 395.0):
            pier(c, cx_, t)
            tower(c, cx_, t, night=0.2)
        leaf(c, -1, 0.0, t)
        leaf(c, 1, angr, t)
        front_water(c, t)
        # the bus: rolls on the right half, floors it, flies over the gap, lands on the left half
        t0, t1, t2 = s("reveal") - 0.1, T["floored"], T["jump1"]
        if t < t1:
            dist = lerp(110, 165, prog(t, t0, t1))
        else:
            dist = lerp(165, LEAF + 10, prog(t, t1, t2) ** 1.6)
        fly = prog(t, t2, t2 + 0.5)
        if fly <= 0:
            bx, by = on_leaf(1, angr, dist)
            bang, sp = angr, prog(t, t1, t1 + 0.3)
        else:
            x0_, y0_ = on_leaf(1, angr, LEAF + 10)
            x1_, y1_ = -95.0, -18.0
            bx = lerp(x0_, x1_, fly)
            by = lerp(y0_, y1_, fly) - math.sin(math.pi * fly) * 26
            bang, sp = lerp(angr, -4.0, fly) if fly < 0.8 else lerp(-4.0, 0.0, (fly - 0.8) / 0.2), 1.0
            if t >= t2 + 0.5:
                bx = lerp(-95, -175, prog(t, t2 + 0.5, s("stat") - 0.2))
                by, bang, sp = -18.0 + max(0.0, math.sin((t - t2 - 0.5) * 18) * 4 * (1 - prog(t, t2 + 0.5, t2 + 0.9))), 0.0, 0.3
        bus(c, bx, by, 1.0, bang, t, face=-1, speed=sp)
        self.ui["bus"] = self.to_screen(cam, bx, by - 60)
        self.ui["gap"] = self.to_screen(cam, 0, -40)
        c.restore()

    def ui_bus(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "y1952", s("reveal") - 0.1, T["floored"] - 0.2, accent="#FDE68A", size=56)
        self.chip(540, 300, "floored", T["floored"] - 0.2, T["jump1"] + 0.1, accent=WARN, size=46)
        self.chip(540, 300, "jumped", T["jump1"] + 0.1, s("stat") - 0.15, accent=GOOD, size=46)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1E2A4A", "#3A4A7A", "#E39A6A"])
        rng = random.Random(6)
        x = -20
        while x < W:                                             # a street of houses at dusk
            w_, h_ = rng.uniform(120, 200), rng.uniform(380, 620)
            c.drawRect(R(x, 1180 - h_, w_, h_), P(rng.choice(["#3A2E3E", "#2E2A44", "#44323A"])))
            for k in range(int(h_ / 90)):
                c.drawRect(R(x + 24, 1180 - h_ + 40 + k * 90, w_ - 48, 44), P("#FFD58A", 0.35 + 0.3 * rng.random()))
            x += w_ + 8
        c.drawRect(R(0, 1180, W, 60), P("#6B7280"))
        c.drawRect(R(0, 1240, W, 680), P("#2A2B33"))
        if not self.rtl:
            go = prog(t, T["t_leaves"] - 0.4, T["t_stop"] + 0.6)
            bus(c, lerp(640, 1500, e_in(go)), 1236, 4.2, 0.0, t, face=1, speed=go)
            c.drawRect(R(860, 760, 10, 420), P("#9CA3AF"))       # the bus stop
            c.drawCircle(865, 760, 46, P("#DC2626"))
            c.drawCircle(865, 760, 30, P("#F8FAFC"))
            run = prog(t, T["t_yours"] - 0.3, T["t_stop"])
            px_ = lerp(80, 520, run)
            person(c, px_, 1236, 330, "#2563EB", t * (1 + run), pose="walk" if run < 1 else "cheer", face=1)
        else:
            c.drawRect(R(900, 600, 16, 600), P("#4B5563"))       # the traffic light
            c.drawRRect(rr(860, 480, 96, 230, 18), P("#111827"))
            g = prog(t, T["t_leaves"] - 0.1, T["t_leaves"] + 0.1)
            for k, col in enumerate(("#EF4444", "#F59E0B", "#22C55E")):
                on_ = (1 - g) if k == 0 else g if k == 2 else 0.0
                c.drawCircle(908, 520 + k * 72, 28, P(mix("#1F2937", col, 0.25 + 0.75 * on_)))
                if on_ > 0:
                    add_glow(c, 908, 520 + k * 72, 80, col, 0.6 * on_)
            car(c, 600, 1236, "#F8FAFC", 0.0, 6.0, face=1)
            hk = prog(t, T["t_stop"] - 0.15, T["t_stop"])
            car(c, 200, 1236, "#FCD34D", 0.0, 6.0, face=1)
            if hk > 0:
                for k in range(3):
                    r_ = 40 + k * 46 + (t * 200) % 46
                    p_ = skia.Path()
                    p_.addArc(R(360 - r_, 1100 - r_, 2 * r_, 2 * r_), -50, 100)
                    c.drawPath(p_, P("#FDE047", hk * (1 - k / 3), stroke=8))

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            self.chip(300, 760, "wait", T["t_stop"] - 0.2, self.duration + 1, accent=WARN, size=56)
        else:
            self.chip(700, 360 + 0 * t, "green", T["t_leaves"] - 0.1, self.duration + 1, accent=GOOD, size=46)
            self.chip(330, 860, "beep", T["t_stop"] - 0.15, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1E3A6E", "#3E6AA8", "#E39A6A"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.1, sfx.creak(1.4, 61), -10), (0.3, sfx.whirr(1.4, 120.0, 200.0, 62), -16), (T["stand"], sfx.thunk(63), -8),
              (T["ship"] - 0.3, sfx.hum(1.1, 110.0), -12), (T["down"], sfx.thud(0.4, 64), -8),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8),
              (T["tower"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["docks"], sfx.pop(68), -8),
               (T["upstream"], sfx.whoosh(0.4, False, 69), -12), (T["past1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 70), -4), (T["cut"], sfx.snap(71), -8), (T["two"], sfx.creak(1.0, 72), -10),
               (T["axle"], sfx.clank(500.0, 0.5, 73), -10), (T["heavy1"], sfx.ding(), -8), (T["heavy1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["thousand"], sfx.thud(0.5, 75), -6),
               (T["tons1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["counter"], sfx.clank(260.0, 0.6, 77), -8),
               (T["push"], sfx.tap(78), -6), (T["tips"], sfx.creak(1.0, 79), -10), (T["up1"], sfx.ding(), -8),
               (T["up1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 80), -4), (T["y1894"], sfx.tick(), -8),
               (T["ready"] - 0.3, sfx.hum(1.0, 98.0), -10), (T["arr1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 81), -4), (T["steam"], sfx.hiss(0.8, 82), -10),
               (T["steam"] + 0.2, sfx.whirr(2.4, 90.0, 160.0, 83), -16), (T["pump"], gas_hiss(0.6, 84), -14),
               (T["pushes"], sfx.hiss(0.6, 85), -10), (T["dem1"], sfx.ding(), -8), (T["dem1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 86), -4), (T["people"], sfx.tick(), -10),
               (T["wait1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 87), -4), (T["walkways"], sfx.pop(88), -8),
               (T["f42"], sfx.pop(89), -6), (T["top1"], sfx.ding(), -8), (T["top1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(90), 0), (T["follow"] - 0.15, sfx.pop(91), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 92), -6), (T["opened"], sfx.creak(1.4, 93), -10),
               (T["floored"], sfx.riser(0.9, 94), -10), (T["jump1"], sfx.whoosh(0.5, True, 95), -8),
               (T["jump1"] + 0.45, sfx.thud(0.5, 96), -4), (T["jump1"] + 0.5, sfx.clank(300.0, 0.4, 97), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 98), -6), (T["s1"], sfx.pop(99), -3), (T["s2"], sfx.pop(100), -3),
               (T["s3"], sfx.pop(101), -3)]
        ev += [(T["cong2"], sfx.pop(102), -2), (T["cong2"], sfx.sparkle(1.4, 18, 103), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 104), -6)]
        if self.rtl:
            ev += [(T["t_leaves"], sfx.ding(), -10), (T["t_stop"] - 0.1, sfx.beep(440.0, 0.45), -6)]
        else:
            ev += [(T["t_leaves"] - 0.3, sfx.riser(0.8, 105), -12), (T["t_stop"], sfx.pop(106), -6)]
        return ev


NAME = "towerbridge"
EPISODE = TowerBridge
