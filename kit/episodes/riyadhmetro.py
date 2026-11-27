"""Episode 106 - The Riyadh Metro, the longest driverless metro on Earth.  v2 look.

Sets: city (hook: close on the front window of a driverless train where a kid has the driver's seat, out to the train
gliding along its viaduct over the Riyadh skyline at dusk; cta, stat; closer at night with the towers lit), traffic
(break1: a desert highway jammed bumper to bumper in the heat haze), section (fix1: a cut through the city, a boring
machine digs a tunnel underneath while concrete legs lift the track over the street; break2: groundwater under the desert
bursts into the dig; fix2: pumps drain it and concrete rings line the tunnel), net (break3: six coloured lines full of
trains and a driver's cap with a question mark; fix3: the map turns out to be the screen wall of a control room), platform
(break4: a passenger on the phone wanders to the platform edge; fix4: a glass wall rises and its doors open with the
train's), map (reveal: the six lines draw themselves while a counter runs to 176 km and a record medal drops in), tag (the
uncle in the front seat of the driverless train, steering a wheel that is not there).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

DECK = 980                                             # rail top on the viaduct in the city set
CAR_L, CAR_H, GAP = 250, 120, 10
LINES = (("#2563EB", "BLUE"), ("#DC2626", "RED"), ("#F97316", "ORANGE"), ("#EAB308", "YELLOW"), ("#16A34A", "GREEN"),
         ("#9333EA", "PURPLE"))
SKIN = ("#E8B48A", "#C68E62", "#A8754E", "#F1C7A3")


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== the train (side view)
def train(c, front, y, t, n=3, col="#2563EB", kid=0.0, uncle=0.0, lit=0.6, doors=0.0, glow=1.0, a=1.0):
    """A driverless metro running to the right; `front` is the x of its nose, `y` the rail top. kid / uncle: who sits in
    the big front window."""
    if a <= 0:
        return
    for i in range(n):
        x1 = front - i * (CAR_L + GAP)
        x0 = x1 - CAR_L
        yt, yb = y - CAR_H - 14, y - 14
        body = skia.Path()
        if i == 0:                                     # the nose: a rounded glass front, no cab
            body.moveTo(x0, yt)
            body.lineTo(x1 - 70, yt)
            body.cubicTo(x1 - 18, yt + 2, x1, yt + 40, x1, yb - 18)
            body.lineTo(x1, yb)
            body.lineTo(x0, yb)
            body.close()
        else:
            body.addRRect(rr(x0, yt, CAR_L, CAR_H, 18))
        c.drawPath(body, lin_paint(0, yt, 0, yb, ["#FFFFFF", "#E5E7EB", "#9CA3AF"], [0, 0.6, 1], a=a))
        c.save()
        c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawRect(R(x0, yb - 34, CAR_L + 4, 12), P(col, a))
        c.drawRect(R(x0, yb - 10, CAR_L + 4, 10), P("#4B5563", a))
        win = mix("#1E293B", "#FFE7B0", lit)
        for k in range(4):                             # side windows and doors
            wx = x0 + 22 + k * 56
            if i == 0 and k == 3:
                continue
            if k in (1, 3) or (i == 0 and k == 1):
                op = 14 * doors
                c.drawRRect(rr(wx - op, yt + 18, 20, CAR_H - 34, 4), P("#CBD5E1", a))
                c.drawRRect(rr(wx + 20 + op, yt + 18, 20, CAR_H - 34, 4), P("#CBD5E1", a))
                c.drawRRect(rr(wx + 3 - op, yt + 24, 14, 40, 3), P(win, 0.95 * a))
                c.drawRRect(rr(wx + 23 + op, yt + 24, 14, 40, 3), P(win, 0.95 * a))
                if doors > 0:
                    c.drawRect(R(wx + 20 - op, yt + 18, 2 * op, CAR_H - 34), P("#FFF3D6", 0.9 * a * doors))
            else:
                c.drawRRect(rr(wx, yt + 22, 40, 44, 7), P(win, 0.95 * a))
        if i == 0:                                     # the big front window
            fw = skia.Path()
            fw.moveTo(x1 - 92, yt + 10)
            fw.lineTo(x1 - 66, yt + 10)
            fw.cubicTo(x1 - 26, yt + 12, x1 - 10, yt + 40, x1 - 8, yb - 40)
            fw.lineTo(x1 - 92, yb - 40)
            fw.close()
            c.drawPath(fw, lin_paint(x1 - 92, yt, x1, yb, [mix("#0F172A", "#FDE68A", 0.35 * lit), "#1E293B", "#0B1220"], a=a))
            if kid > 0:                                # a kid with both hands on the glass
                hx, hy = x1 - 46, yt + 52
                c.drawRRect(rr(hx - 16, hy + 14, 32, 40, 12), P("#F97316", a * kid))
                c.drawCircle(hx, hy, 15, P(SKIN[0], a * kid))
                c.drawArc(R(hx - 16, hy - 17, 32, 22), 180, 180, True, P("#1F2937", a * kid))
                for sd in (-1, 1):
                    c.drawLine(hx + sd * 10, hy + 22, hx + 22 + sd * 4, hy + 2 + sd * 6, P(SKIN[0], a * kid, stroke=6))
                    c.drawCircle(hx + 24 + sd * 4, hy + 1 + sd * 6, 5, P(SKIN[0], a * kid))
            if uncle > 0:
                hx, hy = x1 - 50, yt + 50
                c.drawRRect(rr(hx - 18, hy + 14, 36, 44, 12), P("#F8FAFC", a * uncle))
                c.drawCircle(hx, hy, 15, P(SKIN[1], a * uncle))
            c.drawLine(x1 - 66, yt + 14, x1 - 30, yt + 24, P("#FFFFFF", 0.35 * a, stroke=3))
        c.restore()
        if i == 0 and glow > 0:
            add_glow(c, x1 - 4, yb - 22, 60, "#FFF3C4", 0.8 * glow * a)
            c.drawCircle(x1 - 6, yb - 22, 6, P("#FFF7DA", a))
        for bx in (x0 + 50, x1 - 50):                  # bogies
            c.drawRRect(rr(bx - 38, yb - 2, 76, 12, 5), P("#1F2937", a))
            for wx in (-20, 20):
                c.drawCircle(bx + wx, yb + 8, 8, P("#111827", a))


# ====================================================================================== the city
def sky_dusk(c, night=0.0):
    vrect(c, 0, 0, W, 1250, [mix("#3B2A63", "#070B1F", night), mix("#B4537A", "#111A3A", night),
                            mix("#F59E5B", "#1E2A55", night), mix("#FCD38A", "#2B3A66", night)], [0, 0.45, 0.8, 1])
    if night < 1:
        add_glow(c, 820, 900, 260, "#FFD58A", 0.6 * (1 - night))
        c.drawCircle(820, 905, 46, P("#FFE3A3", 0.9 * (1 - night)))


def kingdom(c, x, base, top, w, night=0.0, a=1.0):
    """A tall tower that narrows to two tips with a parabolic opening near the top (Riyadh's skyline)."""
    body = skia.Path()
    body.moveTo(x - w / 2, base)
    body.cubicTo(x - w / 2, base - (base - top) * 0.5, x - w * 0.3, top + 60, x - w * 0.16, top)
    body.lineTo(x + w * 0.16, top)
    body.cubicTo(x + w * 0.3, top + 60, x + w / 2, base - (base - top) * 0.5, x + w / 2, base)
    body.close()
    c.drawPath(body, lin_paint(x - w / 2, 0, x + w / 2, 0, [mix("#4B5A7A", "#1B2340", night), mix("#7C8AA8", "#2A3558", night),
                                                            mix("#3A4766", "#141B33", night)], a=a))
    hole = skia.Path()
    hole.moveTo(x - w * 0.13, top + 6)
    hole.cubicTo(x - w * 0.11, top + 150, x + w * 0.11, top + 150, x + w * 0.13, top + 6)
    hole.close()
    c.drawPath(hole, P(mix("#E9A06A", "#1E2A55", night), a))
    c.drawRect(R(x - w * 0.16, top + 104, w * 0.32, 10), P(mix("#5B6A8A", "#FDE68A", night * 0.8), a))
    if night > 0:
        rng = random.Random(int(x))
        for k in range(26):
            yy = rng.uniform(top + 170, base - 20)
            ww = w * (0.3 + 0.6 * (yy - top) / (base - top))
            c.drawRect(R(x - ww / 2 + rng.uniform(0, ww - 10), yy, 8, 4), P("#FDE68A", 0.7 * night * a))


def faisaliah(c, x, base, top, w, night=0.0, a=1.0):
    """A pointed tower with a golden ball high up."""
    p = skia.Path()
    p.moveTo(x - w / 2, base)
    p.lineTo(x - 6, top)
    p.lineTo(x + 6, top)
    p.lineTo(x + w / 2, base)
    p.close()
    c.drawPath(p, lin_paint(x - w / 2, 0, x + w / 2, 0, [mix("#516080", "#1B2340", night), mix("#8E9BB8", "#2D3A5E", night),
                                                         mix("#3E4B6B", "#141B33", night)], a=a))
    by = top + (base - top) * 0.24
    add_glow(c, x, by, 50, "#FDE68A", (0.35 + 0.5 * night) * a)
    c.drawCircle(x, by, 22, lin_paint(x - 22, by - 22, x + 22, by + 22, ["#FEF3C7", "#F59E0B", "#B45309"], a=a))


def skyline(c, night=0.0, base=1000):
    rng = random.Random(3)
    for k in range(16):                                # far blocks
        x = k * 72 - 20 + rng.uniform(-10, 10)
        h = rng.uniform(60, 220)
        c.drawRect(R(x, base - h, 64, h), P(mix("#6B5A7E", "#141A33", night), 0.9))
        if night > 0:
            for j in range(int(h // 34)):
                c.drawRect(R(x + 10 + (j % 2) * 26, base - h + 14 + j * 30, 12, 8), P("#FDE68A", 0.55 * night))
    faisaliah(c, 300, base, base - 430, 120, night)
    kingdom(c, 700, base, base - 600, 150, night)
    for x, h, w in ((120, 260, 70), (470, 300, 80), (900, 330, 90), (1000, 200, 80)):
        c.drawRect(R(x - w / 2, base - h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, [mix("#55678A", "#1A2142", night),
                                                                                       mix("#33405F", "#121831", night)]))
        if night > 0:
            for j in range(int(h // 30)):
                c.drawRect(R(x - w / 2 + 10, base - h + 12 + j * 28, w - 20, 5), P("#93C5FD", 0.35 * night))


def viaduct(c, night=0.0, x0=-400, x1=1500, legs=1.0, built=1.0):
    """The elevated track: a deck at DECK on concrete legs down to the city floor at y 1180."""
    xe = lerp(x0, x1, clamp(built))
    k = 0
    for lx in range(int(x0) // 240 * 240, int(x1) + 240, 240):
        if lx > xe:
            break
        h = (1180 - (DECK + 30)) * smooth(clamp(legs * 1.6 - k * 0.12))
        if h > 1:
            c.drawRect(R(lx - 22, 1180 - h, 44, h), lin_paint(lx - 22, 0, lx + 22, 0,
                                                              [mix("#B8B0A0", "#3C4460", night), mix("#8C8478", "#262C44", night)]))
        k += 1
    c.drawRect(R(x0, DECK, xe - x0, 30), lin_paint(0, DECK, 0, DECK + 30, [mix("#D6CFC2", "#4A5272", night),
                                                                          mix("#9A9284", "#2B314C", night)]))
    c.drawRect(R(x0, DECK - 4, xe - x0, 4), P("#6B7280"))


def city(c, t, front, night=0.0, kid=1.0, uncle=0.0, lit=None):
    sky_dusk(c, night)
    if night > 0:
        v2.stars(c, W, H, t, 0.8 * night)
    skyline(c, night)
    c.drawRect(R(0, 1000, W, 260), lin_paint(0, 1000, 0, 1260, [mix("#C9A27A", "#2A2238", night), mix("#8C6A4E", "#171425", night)]))
    rng = random.Random(8)
    for k in range(10):                                # low houses and palms on the city floor
        x = k * 118 + rng.uniform(-14, 14)
        c.drawRect(R(x, 1110, 90, 70), P(mix("#E7D2B0", "#2E2840", night)))
        c.drawRect(R(x + 12, 1128, 18, 18), P(mix("#8B6B4A", "#FDE68A", night * 0.7)))
        c.drawRect(R(x + 52, 1128, 18, 18), P(mix("#8B6B4A", "#FDE68A", night * 0.7)))
    for k in range(5):
        px = 60 + k * 230
        c.drawLine(px, 1180, px + 8, 1080, P(mix("#6B4F32", "#241A2E", night), 1, stroke=10))
        for j in range(6):
            ang = -2.6 + j * 0.42
            c.drawLine(px + 8, 1080, px + 8 + math.cos(ang) * 46, 1080 + math.sin(ang) * 26 + 10,
                       P(mix("#3F7A3A", "#1C2A2A", night), 1, stroke=8))
    viaduct(c, night)
    train(c, front, DECK, t, n=4, col=LINES[0][0], kid=kid, uncle=uncle, lit=lerp(0.55, 1.0, night) if lit is None else lit)
    if night > 0:
        add_glow(c, 540, 980, 600, "#FDE68A", 0.08 * night)


# ====================================================================================== traffic
def jam(c, t, heat=1.0, honk=0.0):
    vrect(c, 0, 0, W, H, ["#F2A65A", "#F6C67C", "#E8B98A"])
    add_glow(c, 820, 260, 260, "#FFF1C9", 0.8)
    c.drawCircle(820, 260, 90, P("#FFF7D6"))
    skyline(c, 0.0, base=640)
    road = skia.Path()                                 # a highway running away from the camera
    road.moveTo(-200, 1240)
    road.lineTo(470, 640)
    road.lineTo(610, 640)
    road.lineTo(1280, 1240)
    road.close()
    c.drawRect(R(0, 640, W, 620), P("#C79A6B"))
    c.drawRect(R(0, 1180, W, H - 1180), lin_paint(0, 1180, 0, 1500, ["#8A6646", "#2A1E16"]))
    c.drawPath(road, lin_paint(0, 640, 0, 1240, ["#5B5B66", "#3A3A44"]))
    cols = ("#F8FAFC", "#DC2626", "#1E40AF", "#9CA3AF", "#111827", "#F59E0B", "#E5E7EB", "#0F766E")
    rng = random.Random(5)
    for row in range(9):                               # cars bumper to bumper, far rows first
        z = 1.0 - row / 9.5
        yy = lerp(660, 1210, z ** 1.6)
        s = lerp(0.18, 1.0, z ** 1.6)
        for lane in (-1.5, -0.5, 0.5, 1.5):
            cx = 540 + lane * 300 * s + math.sin(t * 1.3 + row + lane) * 2 * s
            w_, h_ = 210 * s, 110 * s
            col = cols[rng.randrange(len(cols))]
            c.drawRRect(rr(cx - w_ / 2, yy - h_, w_, h_ * 0.62, 18 * s), P(col))
            c.drawRRect(rr(cx - w_ * 0.36, yy - h_ * 1.28, w_ * 0.72, h_ * 0.42, 14 * s), P(shade(col, -0.18)))
            c.drawRRect(rr(cx - w_ * 0.3, yy - h_ * 1.22, w_ * 0.6, h_ * 0.3, 10 * s), P("#1F2937", 0.85))
            for sd in (-1, 1):                         # brake lights
                c.drawCircle(cx + sd * w_ * 0.38, yy - h_ * 0.62, 9 * s, P("#EF4444"))
                add_glow(c, cx + sd * w_ * 0.38, yy - h_ * 0.62, 28 * s, "#EF4444", 0.6)
    if heat > 0:                                       # heat haze
        for k in range(10):
            yy = 700 + k * 52
            p = skia.Path()
            p.moveTo(0, yy)
            for j in range(13):
                p.lineTo(j * 90, yy + math.sin(t * 5 + j * 1.3 + k) * 6)
            c.drawPath(p, P("#FFF7ED", 0.12 * heat, stroke=6))
    if honk > 0:
        for k, (hx, hy) in enumerate(((300, 900), (760, 980), (520, 780))):
            u = ((t * 2.2 + k * 0.33) % 1.0)
            c.drawArc(R(hx - 30 - u * 60, hy - 30 - u * 60, 60 + u * 120, 60 + u * 120), -60, 120, False,
                      P("#FFFFFF", 0.8 * (1 - u) * honk, stroke=6))


def thermo(c, x, y, h, frac, a=1.0, col=WARN):
    if a <= 0:
        return
    c.drawRRect(rr(x - 26, y - h, 52, h, 26), P("#F8FAFC", 0.95 * a))
    c.drawRRect(rr(x - 26, y - h, 52, h, 26), P("#0F172A", a, stroke=6))
    hh = (h - 60) * clamp(frac)
    c.drawRRect(rr(x - 12, y - 30 - hh, 24, hh + 10, 12), P(col, a))
    c.drawCircle(x, y, 40, P(col, a))
    c.drawCircle(x, y, 40, P("#0F172A", a, stroke=6))


# ====================================================================================== the section
SURF = 600
TUN_Y = 930
AQ = (990, 1160)                                       # the water-bearing layer


def section(c, t, bore=0.0, legs=0.0, water=0.0, burst=0.0, pump=0.0, rings=0.0, train_x=None):
    vrect(c, 0, 0, W, SURF, ["#2B2F5A", "#C76B6B", "#F4B37A"], [0, 0.65, 1])
    skyline(c, 0.0, base=SURF - 70)
    c.drawRect(R(0, SURF - 70, W, 70), P("#6B6F7A"))                     # the street
    for k in range(6):
        c.drawRect(R(k * 200 + (t * 60) % 200 - 100, SURF - 46, 120, 5), P("#F8FAFC", 0.7))
    rng = random.Random(2)
    for k in range(5):                                 # cars keep moving on the street above the dig
        x = (k * 260 + t * 90) % (W + 300) - 150
        col = rng.choice(["#F8FAFC", "#DC2626", "#1E40AF", "#F59E0B"])
        c.drawRRect(rr(x, SURF - 60, 110, 34, 12), P(col))
        c.drawRRect(rr(x + 20, SURF - 82, 66, 26, 10), P(shade(col, -0.2)))
    vrect(c, 0, SURF, W, 1250 - SURF, ["#D8B98E", "#C2A27A", "#A98A68", "#8E7356"], [0, 0.25, 0.6, 1])
    for k in range(7):
        y = SURF + 60 + k * 90
        c.drawLine(0, y, W, y + 12, P("#7A6248", 0.3, stroke=3))
    if water > 0:                                      # the water-bearing layer under the desert
        c.drawRect(R(0, AQ[0], W, AQ[1] - AQ[0]), lin_paint(0, AQ[0], 0, AQ[1], [("#3B82F6", 0.35 * water), ("#1D4ED8", 0.6 * water)]))
        for k in range(18):
            xx = (k * 70 + t * 30) % W
            c.drawLine(xx, AQ[0] + 30 + (k % 4) * 34, xx + 30, AQ[0] + 30 + (k % 4) * 34, P("#BFDBFE", 0.5 * water, stroke=3))
    # the tunnel being bored from the left
    xe = lerp(-60, 780, smooth(bore))
    if bore > 0:
        c.drawRect(R(-60, TUN_Y - 104, xe + 60, 208), P("#3A2E22"))
        c.drawRect(R(-60, TUN_Y - 90, xe + 60, 180), P("#14110D"))
        if rings > 0:                                  # concrete rings line it
            n = int(16 * clamp(rings) + 0.999)
            for k in range(n):
                rx = 20 + k * 48
                if rx > xe - 60:
                    break
                c.drawRRect(rr(rx, TUN_Y - 100, 40, 200, 10), lin_paint(rx, 0, rx + 40, 0, ["#9CA3AF", "#E5E7EB", "#9CA3AF"]))
                c.drawRRect(rr(rx + 6, TUN_Y - 80, 28, 160, 6), P("#1F2937"))
        if burst > 0:                                  # water bursting in through the cracks
            lvl = lerp(TUN_Y + 90, TUN_Y - 50, clamp(burst) * (1 - clamp(rings)))
            c.save()
            c.clipRect(R(-60, TUN_Y - 90, xe + 60, 180))
            c.drawRect(R(-60, lvl, xe + 60, TUN_Y + 90 - lvl), P("#3B82F6", 0.85))
            c.restore()
            rngw = random.Random(7)
            for k in range(10):
                jx = rngw.uniform(40, xe - 80)
                u = (t * 2.0 + rngw.random()) % 1.0
                k2 = clamp(burst * 2) * (1 - clamp(rings))
                c.drawLine(jx, TUN_Y + 98, jx + 6, TUN_Y + 98 - 80 * u - 30, P("#93C5FD", 0.9 * k2 * (1 - u), stroke=10))
        # the boring machine at the head
        mx = xe
        c.drawRRect(rr(mx - 220, TUN_Y - 86, 220, 172, 20), lin_paint(0, TUN_Y - 86, 0, TUN_Y + 86, ["#FCD34D", "#F59E0B", "#B45309"]))
        c.drawRect(R(mx - 206, TUN_Y - 26, 180, 16), P("#7C2D12"))
        for k in range(3):
            c.drawCircle(mx - 180 + k * 60, TUN_Y + 40, 12, P("#7C2D12"))
        c.save()
        c.translate(mx + 8, TUN_Y)
        c.scale(0.35, 1.0)
        c.drawCircle(0, 0, 100, P("#6B7280"))
        c.rotate(t * 240 * (1 if bore < 1 else 0.2))
        for k in range(6):
            c.rotate(60)
            c.drawLine(0, 0, 0, -96, P("#E5E7EB", 1, stroke=16))
        c.restore()
        if bore < 1:
            v2.puff(c, mx + 26, TUN_Y, 30, "#C2A27A", 0.5)
    # the viaduct on concrete legs over the street (right side)
    if legs > 0:
        deck_y = 430
        for k, lx in enumerate((640, 800, 960, 1120)):
            h = (SURF - 70 - (deck_y + 24)) * smooth(clamp(legs * 1.8 - k * 0.25))
            c.drawRect(R(lx - 18, SURF - 70 - h, 36, h), lin_paint(lx - 18, 0, lx + 18, 0, ["#E5E0D6", "#A8A096"]))
        dk = smooth(clamp(legs * 1.4 - 0.3))
        if dk > 0:
            c.drawRect(R(600, deck_y, 520 * dk, 24), lin_paint(0, deck_y, 0, deck_y + 24, ["#EDE8DF", "#B6AEA2"]))
        if train_x is not None and dk >= 1:
            c.save()
            c.translate(0, deck_y)
            c.scale(1, 1)
            train(c, train_x, 0, t, n=2, col=LINES[0][0], lit=0.6)
            c.restore()
    if pump > 0:                                       # pumps on the surface, a pipe down to the tunnel
        px = 300
        c.drawRect(R(px - 14, SURF - 40, 28, TUN_Y - 90 - SURF + 40), P("#475569", pump))
        c.drawRRect(rr(px - 70, SURF - 130, 140, 96, 16), lin_paint(0, SURF - 130, 0, SURF - 34, ["#60A5FA", "#1D4ED8"], a=pump))
        c.save()
        c.translate(px, SURF - 82)
        c.rotate(t * 400)
        for k in range(4):
            c.rotate(90)
            c.drawLine(0, 0, 0, -30, P("#E0F2FE", pump, stroke=8))
        c.restore()
        for k in range(5):                             # water rising up the pipe
            u = (t * 1.5 + k / 5) % 1.0
            yy = lerp(TUN_Y - 94, SURF - 40, u)
            c.drawCircle(px, yy, 8, P("#BFDBFE", 0.9 * pump))
        jet = skia.Path()
        jet.moveTo(px + 70, SURF - 100)
        jet.quadTo(px + 160, SURF - 150, px + 220, SURF - 72)
        c.drawPath(jet, P("#93C5FD", 0.7 * pump, stroke=14))


# ====================================================================================== the network
def net_pts(i):
    """Six stylised lines across the map (screen space)."""
    if i == 0:
        return [(150, 380), (320, 560), (460, 760), (560, 980), (640, 1160)]
    if i == 1:
        return [(80, 760), (300, 780), (540, 720), (780, 650), (1000, 600)]
    if i == 2:
        return [(60, 980), (300, 930), (560, 880), (820, 900), (1020, 960)]
    if i == 3:
        return [(860, 380), (780, 560), (700, 760), (720, 980), (900, 1160)]
    if i == 4:
        return [(360, 420), (420, 600), (520, 740), (640, 820)]
    return [(240, 1140), (380, 1040), (540, 880), (700, 720), (900, 470)]


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def poly_at(pts, u):
    L = poly_len(pts) * clamp(u)
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if L <= d:
            k = L / max(d, 1e-6)
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        L -= d
    return pts[-1]


def network(c, t, draw=1.0, trains=1.0, n_trains=5, stations=1.0, a=1.0):
    for i, (col, _) in enumerate(LINES):
        pts = net_pts(i)
        u = clamp(draw * 1.25 - i * 0.05)
        if u <= 0:
            continue
        p = skia.Path()
        p.moveTo(*pts[0])
        L = poly_len(pts) * u
        acc = 0.0
        for a_, b_ in zip(pts, pts[1:]):
            d = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
            if acc + d <= L:
                p.lineTo(*b_)
            else:
                k = (L - acc) / max(d, 1e-6)
                p.lineTo(a_[0] + (b_[0] - a_[0]) * k, a_[1] + (b_[1] - a_[1]) * k)
                break
            acc += d
        c.drawPath(p, P(col, 0.95 * a, stroke=16))
        if stations > 0:
            for k in range(1, 9):
                if k / 9 <= u:
                    sx, sy = poly_at(pts, k / 9)
                    c.drawCircle(sx, sy, 10, P("#F8FAFC", a * stations))
                    c.drawCircle(sx, sy, 10, P("#0F172A", a * stations, stroke=3))
        if trains > 0 and u >= 1:
            for k in range(n_trains):
                v = (k / n_trains + t * 0.045 * (1 + i * 0.13) * (1 if i % 2 else -1)) % 1.0
                tx, ty = poly_at(pts, v)
                add_glow(c, tx, ty, 26, "#FFFFFF", 0.5 * trains * a)
                c.drawCircle(tx, ty, 9, P("#FFFFFF", trains * a))


def driver_cap(c, x, y, s, a=1.0, q=1.0, t=0.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawOval(R(-90, -10, 180, 40), P("#111827", a))
    top = skia.Path()
    top.moveTo(-80, 6)
    top.cubicTo(-90, -70, 90, -70, 80, 6)
    top.close()
    c.drawPath(top, lin_paint(0, -70, 0, 6, ["#334155", "#0F172A"], a=a))
    c.drawRect(R(-70, -14, 140, 14), P("#EAB308", a))
    c.drawCircle(0, -36, 12, P("#EAB308", a))
    c.restore()
    if q > 0:
        k = 1 + 0.08 * math.sin(t * 6)
        text(c, "?", x + 110 * s, y - 40 * s, 150 * s * k, HILITE, "Poppins-Black", a=a * q)


def control_room(c, t, k=1.0, a=1.0):
    """The map becomes the wall screen of a control room: desks and two operators seen from behind."""
    if a <= 0:
        return
    vrect(c, 0, 0, W, H, ["#0B1020", "#111833"])
    c.drawRect(R(0, 1040, W, 220), lin_paint(0, 1040, 0, 1260, ["#1F2937", "#0F172A"]))
    for dx in (210, 540, 870):                         # desks with monitors
        c.drawRRect(rr(dx - 150, 1010, 300, 36, 10), P("#334155"))
        for mx in (-70, 70):
            c.drawRRect(rr(dx + mx - 60, 920, 120, 80, 8), P("#0F172A"))
            c.drawRRect(rr(dx + mx - 54, 926, 108, 68, 6), P("#1D4ED8", 0.6))
            for j in range(3):
                c.drawLine(dx + mx - 44, 940 + j * 18, dx + mx - 44 + 60 + 20 * math.sin(t * 2 + j + dx), 940 + j * 18,
                           P("#93C5FD", 0.8, stroke=4))
    for px, col in ((380, "#F8FAFC"), (720, "#F8FAFC")):
        person(c, px, 1180, 260, col, t, pose="stand", face=1, hair="#111827")


# ====================================================================================== the platform
EDGE = 900                                              # platform edge (far side) y; trains run behind it


def platform(c, t, glass_up=0.0, train_x=None, doors=0.0, wander=0.0, wobble=0.0, people=True):
    vrect(c, 0, 0, W, H, ["#1A2238", "#232D48"])
    c.drawRect(R(0, 330, W, 380), lin_paint(0, 330, 0, 710, ["#E8DFD0", "#CDBFA8"]))          # the far wall
    for k in range(6):
        c.drawRect(R(k * 190 + 30, 380, 130, 220), P("#B8A78C", 0.5))
        add_glow(c, k * 190 + 95, 360, 80, "#FFF1C9", 0.35)
    c.drawRect(R(0, 300, W, 34), P("#9C8B70"))
    c.drawRect(R(0, 710, W, EDGE - 710), P("#0B0F19"))                                           # the track bed
    for ry in (790, 840):
        c.drawLine(0, ry, W, ry, P("#9CA3AF", 0.8, stroke=6))
    if train_x is not None:
        c.save()
        c.translate(0, 0)
        train(c, train_x, 860, t, n=4, col=LINES[0][0], lit=0.9, doors=doors, glow=0.6)
        c.restore()
    c.drawRect(R(0, EDGE, W, 1250 - EDGE), lin_paint(0, EDGE, 0, 1250, ["#EDE6DA", "#BFB3A0"]))   # the platform floor
    c.drawRect(R(0, EDGE, W, 16), P("#FACC15"))
    for k in range(12):
        c.drawLine(k * 96, EDGE + 16, k * 96 - 60, 1250, P("#A89C88", 0.4, stroke=2))
    if glass_up > 0:                                   # glass walls with doors along the edge
        top = lerp(EDGE, 640, smooth(glass_up))
        for k in range(5):
            gx = 20 + k * 216
            for half in (0, 1):
                op = 26 * doors if k in (1, 3) else 0.0
                hx = gx + half * 100 + (-op if half == 0 else op)
                c.drawRect(R(hx, top, 96, EDGE - top), P("#BFE3FF", 0.22))
                c.drawRect(R(hx, top, 96, EDGE - top), P("#E0F2FE", 0.7, stroke=4))
            c.drawRect(R(gx - 6, top - 14, 212, 14), P("#94A3B8"))
            if k in (1, 3) and doors > 0:
                add_glow(c, gx + 98, top + 30, 26, GOOD, 0.8 * doors)
                c.drawCircle(gx + 98, top + 30, 8, P(GOOD, doors))
    if people:
        for k, (px, col) in enumerate(((150, "#F472B6"), (330, "#60A5FA"), (760, "#34D399"), (930, "#FBBF24"))):
            person(c, px, 1200, 300, col, t + k, pose="stand", face=1 if px < 540 else -1, hair="#1F2937", skin=SKIN[k % 4])
        if wander > 0:                                 # the one on the phone drifting to the edge
            wy = lerp(1210, EDGE + 40, smooth(wander))
            wx = 560 + math.sin(t * 9) * 10 * wobble
            c.save()
            c.translate(wx, wy)
            c.rotate(math.sin(t * 11) * 6 * wobble)
            c.translate(-wx, -wy)
            person(c, wx, wy, lerp(300, 250, smooth(wander)), "#A78BFA", t, pose="walk" if wander < 1 else "look", face=1,
                   hair="#111827")
            c.drawRRect(rr(wx + 12, wy - lerp(300, 250, smooth(wander)) * 0.8, 22, 34, 5), P("#0F172A"))
            c.restore()


# ====================================================================================== the record map
def record_map(c, t, draw, km, medal=0.0, rtl=False):
    vrect(c, 0, 0, W, H, ["#0B1226", "#14203F"])
    rng = random.Random(1)
    for k in range(60):                                # the city's blocks, faint
        x, y = rng.uniform(40, W - 40), rng.uniform(380, 1200)
        c.drawRect(R(x, y, rng.uniform(20, 60), rng.uniform(16, 40)), P("#1E2B4F", 0.8))
    network(c, t, draw=draw, trains=prog(draw, 0.9, 1.0), n_trains=4)
    if rtl:                                            # Arabic: the number in Poppins, the unit in Arabic beside it
        text(c, f"{int(round(km))}", 620, 610, 150, "#FFFFFF", "Poppins-Black", a=prog(km, 1, 12), shadow_a=0.6)
        arabic.text_ar(c, "كيلو", 380, 600, 110, "#FFFFFF", "Tajawal-Black", a=prog(km, 1, 12), shadow_a=0.6)
    else:
        text(c, f"{int(round(km))} KM", 540, 610, 150, "#FFFFFF", "Poppins-Black", a=prog(km, 1, 12), shadow_a=0.6)
    if medal > 0:
        k = e_back(clamp(medal))
        c.save()
        c.translate(820, 920)
        c.scale(k, k)
        c.drawLine(-30, -160, 0, -60, P("#DC2626", 1, stroke=22))
        c.drawLine(30, -160, 0, -60, P("#2563EB", 1, stroke=22))
        add_glow(c, 0, 0, 120, "#FDE68A", 0.7)
        c.drawCircle(0, 0, 78, lin_paint(-78, -78, 78, 78, ["#FEF3C7", "#F59E0B", "#B45309"]))
        c.drawCircle(0, 0, 58, P("#FDE68A", 1, stroke=6))
        text(c, "1", 0, 30, 90, "#78350F", "Poppins-Black")
        c.restore()


class RiyadhMetro(EpisodeV2):
    BUILD_NO = 106
    FIRST_SET = "city"
    CLEAR = "#0B1020"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "THE RIYADH METRO", "ar_sa": "مترو الرياض"}
    EMPH = {"en": ["RIYADH", "BEST", "SEAT", "TRAIN", "DRIVER'S", "MILLIONS", "TRAFFIC", "BIG", "METRO", "MACHINES",
                   "TUNNELS", "TRACKS", "CONCRETE", "LEGS", "DESERT", "WATER", "GROUNDWATER", "PUMPS", "DRY", "WATERTIGHT",
                   "LINING", "WHO", "HUNDRED", "EIGHTY", "TRAINS", "NOBODY", "COMPUTERS", "CONTROL", "ROOM", "DRIVER",
                   "FALLING", "GLASS", "WALLS", "PLATFORMS", "FOLLOW", "CHAIRLIFT", "PURPOSE", "SEVENTY-SIX",
                   "KILOMETERS", "LONGEST", "DRIVERLESS", "EARTH", "SIX", "LINES", "EIGHTY-FIVE", "STATIONS", "MINUTES",
                   "CONGRATS", "YOURSELF", "HONKING", "UNCLE", "BETTER"],
            "ar_sa": ["الرياض", "أحلى", "القطار", "السواق", "ملايين", "الزحمة", "طول", "المترو", "فحفروا", "أنفاق", "السكة",
                      "أعمدة", "الصحرا", "موية", "جوفية", "بالمضخات", "بخرسانة", "مين", "وثمانين", "قطار", "أحد",
                      "الكمبيوتر", "تحكم", "تراقب", "سواق", "يطيحون", "زجاج", "الرصيف", "تنفتح", "متابعة", "تلفريك",
                      "الكيبل", "قصد", "وسبعين", "كيلو", "أطول", "العالم", "ست", "خطوط", "وثمانين", "محطة", "دقيقتين",
                      "مبروك", "بوري", "وعمك", "أحسن"]}
    KEYS = {"ar_sa": {
        ("hook", "RIYADH"): "الرياض", ("hook", "SEAT"): "أحلى", ("hook", "DRIVER"): "السواق",
        ("break1", "MILLIONS"): "ملايين", ("break1", "TRAFFIC"): "الزحمة", ("break1", "BIG"): "طول",
        ("fix1", "MACHINES"): "حفروا", ("fix1", "TUNNELS"): "أنفاق", ("fix1", "TRACKS"): "السكة", ("fix1", "LEGS"): "أعمدة",
        ("break2", "DESERT"): "الصحرا", ("break2", "WATER"): "موية", ("break2", "GROUNDWATER"): "جوفية",
        ("fix2", "PUMPS"): "المضخات", ("fix2", "DRY"): "شفطوها", ("fix2", "LINING"): "خرسانة",
        ("break3", "WHO"): "مين", ("break3", "HUNDRED"): "مية", ("break3", "TRAINS"): "قطار", ("break3", "DAY"): "اليوم",
        ("fix3", "NOBODY"): "أحد", ("fix3", "COMPUTERS"): "الكمبيوتر", ("fix3", "CONTROL"): "تحكم", ("fix3", "WATCHES"): "تراقب",
        ("break4", "DRIVER"): "سواق", ("break4", "FALLING"): "يطيحون", ("break4", "TRACKS"): "السكة",
        ("fix4", "GLASS"): "زجاج", ("fix4", "PLATFORMS"): "الرصيف", ("fix4", "OPENING"): "تنفتح", ("fix4", "TRAIN"): "القطار",
        ("cta", "FOLLOW"): "متابعة", ("cta", "CHAIRLIFT"): "تلفريك",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "HUNDRED"): "مية", ("reveal", "KILOMETERS"): "كيلو",
        ("reveal", "LONGEST"): "أطول", ("reveal", "EARTH"): "العالم",
        ("stat", "SIX"): "ست", ("stat", "EIGHTY"): "خمسة", ("stat", "EVERY"): "دقيقتين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "HONKING"): "بوري", ("tag", "UNCLE"): "عمك", ("tag", "BETTER"): "أحسن"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a chairlift that lets go"),
                   "stat": [("6", "LINES"), ("85", "STATIONS"), ("2.5 MIN", "A TRAIN EVERY")],
                   "L": {"seat": "THE DRIVER'S SEAT?", "nodriver": "NO DRIVER!", "stuck": "STUCK IN TRAFFIC",
                         "big": "HOW BIG A METRO?", "dig": "TUNNELS UNDERNEATH", "legs": "TRACKS ON CONCRETE LEGS",
                         "water": "WATER UNDER THE DESERT!", "pumps": "PUMPS KEEP IT DRY", "rings": "A WATERTIGHT LINING",
                         "trains": "180+ TRAINS", "who": "WHO DRIVES THEM?", "nobody": "NOBODY!",
                         "computers": "COMPUTERS DRIVE", "control": "A CONTROL ROOM WATCHES", "edge": "THE EDGE!",
                         "glass": "GLASS WALLS", "open": "THEY OPEN WITH THE TRAIN", "record": "LONGEST DRIVERLESS METRO",
                         "name": "THE RIYADH METRO", "uncle": "\"I DRIVE BETTER!\"", "temp": "50°C"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: تلفريك يفك الكيبل"),
                      "stat": [("6", "خطوط"), ("85", "محطة"), ("2.5", "دقيقة بين القطارين")],
                      "L": {"seat": "مكان السواق؟", "nodriver": "ما فيه سواق!", "stuck": "الكل في الزحمة",
                            "big": "كم طول المترو؟", "dig": "أنفاق تحت المدينة", "legs": "سكة على أعمدة خرسانة",
                            "water": "موية تحت الصحرا!", "pumps": "المضخات تشفطها", "rings": "خرسانة ما تسرّب",
                            "trains": "أكثر من 180 قطار", "who": "مين يسوقها؟", "nobody": "ولا أحد!",
                            "computers": "الكمبيوتر يسوق", "control": "غرفة تحكم تراقب", "edge": "انتبه للحافة!",
                            "glass": "جدران زجاج", "open": "تنفتح مع القطار", "record": "أطول مترو بدون سواق",
                            "name": "مترو الرياض", "uncle": "أنا أسوق أحسن!", "temp": "50°C"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "riyadh": ("hook", "RIYADH", 0.2), "seat": ("hook", "SEAT", 0.5), "driver0": ("hook", "DRIVER", 0.9),
            "millions": ("break1", "MILLIONS", 0.15), "traffic": ("break1", "TRAFFIC", 0.45), "big": ("break1", "BIG", 0.85),
            "machines": ("fix1", "MACHINES", 0.1), "tunnels": ("fix1", "TUNNELS", 0.3), "tracks": ("fix1", "TRACKS", 0.6),
            "legs": ("fix1", "LEGS", 0.9),
            "desert": ("break2", "DESERT", 0.2), "water": ("break2", "WATER", 0.5), "gw": ("break2", "GROUNDWATER", 0.85),
            "pumps": ("fix2", "PUMPS", 0.15), "dry": ("fix2", "DRY", 0.4), "lining": ("fix2", "LINING", 0.85),
            "who": ("break3", "WHO", 0.1), "hundred": ("break3", "HUNDRED", 0.45), "trains": ("break3", "TRAINS", 0.7),
            "day": ("break3", "DAY", 0.9),
            "nobody": ("fix3", "NOBODY", 0.05), "computers": ("fix3", "COMPUTERS", 0.3), "control": ("fix3", "CONTROL", 0.6),
            "watches": ("fix3", "WATCHES", 0.85),
            "driver4": ("break4", "DRIVER", 0.25), "falling": ("break4", "FALLING", 0.7), "tracks4": ("break4", "TRACKS", 0.9),
            "glass": ("fix4", "GLASS", 0.15), "platforms": ("fix4", "PLATFORMS", 0.4), "opening": ("fix4", "OPENING", 0.65),
            "train4": ("fix4", "TRAIN", 0.85),
            "follow": ("cta", "FOLLOW", 0.1), "chair": ("cta", "CHAIRLIFT", 0.5),
            "answer": ("reveal", "ANSWER", 0.05), "hundred2": ("reveal", "HUNDRED", 0.2), "km": ("reveal", "KILOMETERS", 0.45),
            "longest": ("reveal", "LONGEST", 0.7), "earth": ("reveal", "EARTH", 0.95),
            "s1": ("stat", "SIX", 0.05), "s2": ("stat", "EIGHTY", 0.35), "s3": ("stat", "EVERY", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_honk": ("tag", "HONKING", 0.3), "t_uncle": ("tag", "UNCLE", 0.6), "t_better": ("tag", "BETTER", 0.9)})
        T["stuck1"] = max(T["traffic"], T["millions"] + 0.3)
        T["legs1"] = max(T["legs"], T["tracks"] + 0.3)
        T["water1"] = max(T["water"], T["desert"] + 0.3)
        T["lining1"] = max(T["lining"], T["dry"] + 0.3)
        T["trains1"] = max(T["trains"], T["hundred"] + 0.3)
        T["watch1"] = max(T["watches"], T["control"] + 0.3)
        T["fall1"] = max(T["falling"], T["driver4"] + 0.3)
        T["open1"] = max(T["opening"], T["platforms"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "traffic", 1)
        self.cut(s("fix1") - 0.12, "section", -1)
        self.cut(s("break3") - 0.12, "net", 1)
        self.cut(s("break4") - 0.12, "platform", -1)
        self.cut(s("cta") - 0.12, "city", 1)
        self.cut(s("reveal") - 0.12, "map", -1)
        self.cut(s("stat") - 0.12, "city", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["stuck1"], T["legs1"]), (T["water1"], T["lining1"]), (T["trains1"], T["watch1"]),
                      (T["fall1"], T["open1"])]
        self.shakes = [(T["driver0"], 0.3, 4), (T["stuck1"], 0.4, 6), (T["water1"], 0.5, 10), (T["trains1"], 0.3, 5),
                       (T["fall1"], 0.4, 8), (T["longest"], 0.35, 6), (s("closer") + 0.2, 0.35, 6), (T["t_better"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: city (hook, cta, stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            front = 700 + (t - T["riyadh"]) * 30
            k = e_io(prog(t, T["seat"] - 0.2, s("break1") - 0.3))
            z = lerp(3.0, 1.0, k)
            fx, fy = lerp(front - 40, 540, k), lerp(DECK - 80, 820, k)
            c.save()
            c.translate(540, 760)
            c.scale(z, z)
            c.translate(-fx, -fy)
            city(c, t, front, night=0.0, kid=1.0)
            c.restore()
        elif ph == "closer":
            city(c, t, 860 + (t - s("closer")) * 26, night=1.0, kid=1.0)
        else:
            night = 0.0 if ph == "cta" else prog(t, s("stat"), s("stat") + 1.0) * 0.6
            city(c, t, 820 + (t - s(ph)) * 26, night=night, kid=1.0)

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "seat", T["seat"] - 0.1, T["driver0"], accent=HILITE, size=54)
            self.chip(540, 300, "nodriver", T["driver0"], s("break1") + 0.1, accent=GOOD, size=60)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=54)

    # ------------------------------------------------------------------ set: traffic (break1)
    def draw_traffic(self, c, t):
        T, s = self.T, self.tl.s
        jam(c, t, heat=1.0, honk=prog(t, T["stuck1"], T["stuck1"] + 0.3))
        thermo(c, 930, 560, 300, 0.9 * prog(t, s("break1"), T["traffic"] + 0.4), a=prog(t, s("break1"), s("break1") + 0.3))

    def ui_traffic(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "stuck", T["millions"] - 0.1, T["big"] - 0.3, accent=WARN, size=56)
        self.chip(540, 300, "big", T["big"] - 0.3, s("fix1") - 0.1, accent=HILITE, size=56)
        self.chip(930, 640, "temp", s("break1") + 0.2, s("fix1") - 0.1, accent=WARN, size=40)
        self.badge("alert", T["stuck1"], s("fix1") - 0.2, x=160, y=470)
        self.red(T["stuck1"], 1.2)

    # ------------------------------------------------------------------ set: section (fix1, break2, fix2)
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "fix1":
            section(c, t, bore=prog(t, T["machines"] - 0.2, T["tracks"]), legs=prog(t, T["tracks"] - 0.2, T["legs"] + 0.6))
        elif ph == "break2":
            section(c, t, bore=1.0, legs=1.0, water=prog(t, T["desert"], T["water"]), burst=prog(t, T["water"] - 0.1,
                                                                                               T["gw"] + 0.6))
        else:
            section(c, t, bore=1.0, legs=1.0, water=1.0, burst=1.0 - 0.0, pump=prog(t, T["pumps"] - 0.2, T["pumps"] + 0.3),
                    rings=prog(t, T["dry"], T["lining"] + 0.5), train_x=lerp(1125, 1700, prog(t, T["lining"], s("break3"))))

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix1":
            self.chip(540, 300, "dig", T["machines"] - 0.1, T["tracks"] - 0.1, accent="#FDE68A", size=52)
            self.chip(540, 300, "legs", T["tracks"] - 0.1, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["legs1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "water", T["desert"] - 0.1, s("fix2") - 0.15, accent=WARN, size=52)
            self.badge("alert", T["water1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["water1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "pumps", T["pumps"] - 0.2, T["lining"] - 0.3, accent="#93C5FD", size=54)
            self.chip(540, 300, "rings", T["lining"] - 0.3, s("break3") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["lining1"], s("break3") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: net (break3, fix3)
    def draw_net(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break3":
            vrect(c, 0, 0, W, H, ["#0B1226", "#14203F"])
            n = 2 + int(5 * prog(t, T["hundred"] - 0.3, T["trains"] + 0.3))
            network(c, t, draw=1.0, trains=1.0, n_trains=n)
            ca = prog(t, T["who"] - 0.1, T["who"] + 0.3)
            if ca > 0:
                c.drawCircle(500, 1040, 170 * e_back(ca), P("#0B1226", 0.92))
                c.drawCircle(500, 1040, 170 * e_back(ca), P(WARN, ca, stroke=6))
            driver_cap(c, 470, 1070, 1.3, a=ca, q=prog(t, T["who"], T["who"] + 0.3), t=t)
        else:
            k = e_io(prog(t, T["control"] - 0.4, T["control"] + 0.4))
            if k > 0:
                control_room(c, t, k)
            z = lerp(1.0, 0.56, k)
            c.save()
            c.translate(540, lerp(800, 560, k))
            c.scale(z, z)
            c.translate(-540, -800)
            if k > 0:
                c.drawRRect(rr(-30, 300, W + 60, 980, 30), P("#1F2937"))
            c.drawRect(R(0, 330, W, 930), P("#0B1226"))
            network(c, t, draw=1.0, trains=1.0, n_trains=7)
            c.restore()
            ck = prog(t, T["computers"] - 0.2, T["computers"] + 0.3) * (1 - k)
            if ck > 0:                                 # a computer chip that "drives"
                cx, cy = 540, 1060
                c.drawRRect(rr(cx - 90, cy - 90, 180, 180, 24), P("#0F172A", ck))
                c.drawRRect(rr(cx - 90, cy - 90, 180, 180, 24), P(GOOD, ck, stroke=6))
                for j in range(5):
                    for sd in (-1, 1):
                        c.drawLine(cx + sd * 90, cy - 60 + j * 30, cx + sd * 120, cy - 60 + j * 30, P(GOOD, ck, stroke=6))
                        c.drawLine(cx - 60 + j * 30, cy + sd * 90, cx - 60 + j * 30, cy + sd * 120, P(GOOD, ck, stroke=6))
                add_glow(c, cx, cy, 90, GOOD, 0.5 * ck)

    def ui_net(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "trains", T["hundred"] - 0.2, T["day"] - 0.4, accent="#FDE68A", size=56)
            self.chip(540, 300, "who", T["day"] - 0.4, s("fix3") - 0.1, accent=WARN, size=56)
            self.badge("alert", T["trains1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["trains1"], 1.2)
        else:
            self.chip(540, 300, "nobody", s("fix3") - 0.05, T["computers"] - 0.1, accent=GOOD, size=60)
            self.chip(540, 300, "computers", T["computers"] - 0.1, T["control"] - 0.1, accent=GOOD, size=52)
            self.chip(540, 300, "control", T["control"] - 0.1, s("break4") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["watch1"], s("break4") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: platform (break4, fix4)
    def draw_platform(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break4":
            platform(c, t, wander=prog(t, s("break4"), T["fall1"]), wobble=prog(t, T["fall1"] - 0.2, T["fall1"]))
        else:
            arrive = e_out(prog(t, T["platforms"] - 0.4, T["opening"]))
            platform(c, t, glass_up=prog(t, T["glass"] - 0.2, T["glass"] + 0.5), train_x=lerp(-200, 1080, arrive),
                     doors=prog(t, T["open1"], T["open1"] + 0.5))

    def ui_platform(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "edge", T["driver4"], s("fix4") - 0.15, accent=WARN, size=58)
            self.badge("alert", T["fall1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["fall1"], 1.2)
        else:
            self.chip(540, 300, "glass", T["glass"] - 0.1, T["opening"] - 0.2, accent="#BFE3FF", size=56)
            self.chip(540, 300, "open", T["opening"] - 0.2, s("cta") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["open1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: map (reveal)
    def draw_map(self, c, t):
        T, s = self.T, self.tl.s
        draw = prog(t, s("reveal"), T["km"] + 0.6)
        km = 176 * e_out(prog(t, T["hundred2"] - 0.3, T["km"] + 0.3))
        record_map(c, t, draw, km, medal=prog(t, T["longest"] - 0.2, T["longest"] + 0.3), rtl=self.rtl)

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "record", T["longest"] - 0.1, s("stat") - 0.15, accent=HILITE, size=46)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
        c.save()                                       # the view out of the front window
        c.clipRRect(rr(60, 360, 960, 700, 110))
        vrect(c, 60, 360, 960, 700, ["#3B2A63", "#B4537A", "#F59E5B"], [0, 0.55, 1])
        skyline(c, 0.0, base=820)
        c.drawRect(R(0, 820, W, 260), P("#B9956E"))
        for k in range(9):                             # the track ahead, rushing at us
            u = (k / 9 + t * 0.6) % 1.0
            yy = lerp(825, 1080, u ** 2)
            c.drawLine(lerp(520, -200, u ** 2), yy, lerp(560, 1280, u ** 2), yy, P("#6B6157", 0.7, stroke=lerp(2, 16, u)))
        c.drawLine(520, 825, -200, 1080, P("#D1D5DB", 1, stroke=10))
        c.drawLine(560, 825, 1280, 1080, P("#D1D5DB", 1, stroke=10))
        c.restore()
        c.drawRRect(rr(60, 360, 960, 700, 110), P("#64748B", 1, stroke=16))
        c.drawRect(R(0, 1060, W, H - 1060), lin_paint(0, 1060, 0, 1500, ["#334155", "#0F172A"]))
        go = prog(t, T["t_uncle"] - 0.4, T["t_uncle"])
        steer = math.sin(t * 3.4) * 24 * go
        ux = 540
        c.drawRRect(rr(ux - 230, 980, 460, 320, 150), lin_paint(0, 980, 0, 1300, ["#B6C0CE", "#5B6678"]))   # his back
        cloth = skia.Path()                            # a red-checked head cloth seen from behind, falling to the shoulders
        cloth.moveTo(ux - 92, 860)
        cloth.cubicTo(ux - 96, 760, ux + 96, 760, ux + 92, 860)
        cloth.lineTo(ux + 150, 1080)
        cloth.lineTo(ux - 150, 1080)
        cloth.close()
        c.drawPath(cloth, lin_paint(0, 760, 0, 1080, ["#D9DEE6", "#9AA4B3"]))
        c.save()
        c.clipPath(cloth, skia.ClipOp.kIntersect, True)
        for k in range(-8, 9):
            c.drawLine(ux + k * 26 - 200, 740, ux + k * 26 + 200, 1100, P("#B91C1C", 0.75, stroke=7))
            c.drawLine(ux + k * 26 + 200, 740, ux + k * 26 - 200, 1100, P("#B91C1C", 0.75, stroke=7))
        c.restore()
        c.drawOval(R(ux - 84, 776, 168, 40), P("#111827"))                  # the black cord on top
        c.drawOval(R(ux - 70, 768, 140, 30), P("#0B0F19"))
        c.save()                                       # hands on a steering wheel that is not there
        c.translate(ux, 900)
        c.rotate(steer)
        if go > 0:
            c.drawCircle(0, 0, 190, P("#FDE68A", 0.35 * go, stroke=8))
        for sd in (-1, 1):
            c.drawLine(sd * 150, 160, sd * 186, 10, P("#A8B3C4", 1, stroke=58))
            c.drawCircle(sd * 186, -6, 34, P(SKIN[1]))
        c.restore()

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "uncle", T["t_uncle"] - 0.1, self.duration + 1, accent=HILITE, size=58)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.hum(3.0, 110.0), -18), (T["seat"], sfx.ding(), -10),
              (T["driver0"], sfx.pop(62), -6)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["stuck1"], sfx.buzz(0.5), -12),
               (T["stuck1"] + 0.2, sfx.beep(520.0, 0.25), -10), (T["stuck1"] + 0.5, sfx.beep(470.0, 0.3), -12),
               (T["stuck1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 64), -6), (T["machines"], sfx.whirr(1.6, 90.0, 160.0, 65), -10),
               (T["tracks"], sfx.thunk(66), -8), (T["legs1"], sfx.ding(), -8), (T["legs1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["water1"], sfx.hiss(1.4, 67), -8), (T["water1"], sfx.womp(), -10), (T["water1"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(T["pumps"], sfx.whirr(1.4, 160.0, 240.0, 68), -10), (T["lining1"], sfx.ding(), -8),
               (T["lining1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 69), -6), (T["trains1"], sfx.thud(0.4, 70), -8),
               (T["trains1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["computers"], sfx.charge_up(0.8), -10), (T["watch1"], sfx.ding(), -8), (T["watch1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 71), -6), (T["fall1"], sfx.womp(), -8),
               (T["fall1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["glass"], sfx.whoosh(0.6, True, 72), -10), (T["platforms"], rumble(1.2, 73), -14),
               (T["open1"], sfx.ding(), -6), (T["open1"] + 0.15, sfx.bell(660.0, 0.6), -10)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["hundred2"], sfx.riser(1.0, 95), -12),
               (T["longest"], sfx.ding(), -6), (T["longest"] + 0.1, sfx.sparkle(1.0, 12, 96), -8)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_honk"], sfx.beep(520.0, 0.3), -14),
               (T["t_better"], sfx.womp(), -8)]
        return ev


NAME = "riyadhmetro"
EPISODE = RiyadhMetro
