"""Episode 105 - the Brooklyn Bridge.  v2 look.

Sets: bridge (hook: twenty-one elephants marching across the deck at sunset, the camera pulling out from the elephants
to the whole bridge: two granite towers with pointed arches, the main cables, the web of diagonal stays, Manhattan
behind; cta; stat; closer at night with the lamps lit, for the cover), office (break1: 1869, the drawing of the bridge on
an empty desk, a top hat and a candle: the designer died before work began), river (fix1: the East River cut open, a
giant upside-down wooden box sinking to the riverbed with stone piled on its roof; break2: water rushing in from below;
fix2: air pumped in pushes the water out and men dig inside by lamplight), bends (break3: a worker racing up the shaft,
an inset with bubbles fizzing in his blood, then the boss sinking into a chair; fix3: the boss in bed at his window
watching the towers through a telescope), cable (break4: a cable cut across, thousands of wires; a crook in a top hat,
some wires turn red and snap; fix4: 150 extra wires ring the cable), emily (reveal: Emily Roebling with the drawings, then
riding across first in an open carriage with a rooster on her lap while the crowd cheers), tag (a plastic chair at a
night-time rest house: the uncle sits down, crack).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

GRANITE = ("#D6C7A8", "#B8A27E", "#8C7556")
CABLE = "#334155"
DECK_Y = 820
WATER_Y = 1060
TOWERS = (270, 810)


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== the bridge
def sky(c, pal):
    vrect(c, 0, 0, W, WATER_Y, pal)


def skyline(c, t, lit=0.0):
    rng = random.Random(5)
    x = -20
    while x < W + 20:
        w = rng.uniform(40, 90)
        h = rng.uniform(80, 260)
        c.drawRect(R(x, WATER_Y - h, w - 6, h), P("#1E1B3A"))
        if lit > 0:
            for j in range(int(h / 30)):
                if rng.random() < 0.5:
                    c.drawRect(R(x + 8, WATER_Y - h + 10 + j * 30, w - 24, 8), P("#FDE68A", 0.6 * lit))
        x += w


def tower(c, x, top=330, w=130, lit=0.0):
    """A granite tower with two pointed arches, from the water to `top`."""
    c.drawRect(R(x - w / 2 - 8, WATER_Y - 40, w + 16, 40), P(GRANITE[2]))
    c.drawRect(R(x - w / 2, top, w, WATER_Y - 40 - top), lin_paint(x - w / 2, 0, x + w / 2, 0,
                                                                   [GRANITE[1], GRANITE[0], GRANITE[1], GRANITE[2]]))
    c.drawRect(R(x - w / 2 - 6, top - 14, w + 12, 18), P(GRANITE[2]))
    for sd in (-1, 1):                                   # the two pointed arches the roads run through
        ax = x + sd * w * 0.22
        aw = w * 0.3
        p = skia.Path()
        p.moveTo(ax - aw / 2, DECK_Y + 10)
        p.lineTo(ax - aw / 2, DECK_Y - 170)
        p.quadTo(ax - aw / 2, DECK_Y - 240, ax, DECK_Y - 270)
        p.quadTo(ax + aw / 2, DECK_Y - 240, ax + aw / 2, DECK_Y - 170)
        p.lineTo(ax + aw / 2, DECK_Y + 10)
        p.close()
        c.drawPath(p, P("#2A2340" if lit == 0 else "#3B2F5C"))
    for k in range(7):                                   # stone courses
        yy = top + 40 + k * 90
        c.drawLine(x - w / 2, yy, x + w / 2, yy, P(GRANITE[2], 0.4, stroke=2))
    if lit > 0:
        add_glow(c, x, top + 60, 120, "#FDE68A", 0.35 * lit)


def cable_y(x):
    """The main cable's height at x (screen space): catenary-ish spans between the towers and the anchorages."""
    a, b = TOWERS
    top = 350
    if x < a:
        return lerp(DECK_Y - 10, top, smooth((x + 120) / (a + 120)))
    if x > b:
        return lerp(top, DECK_Y - 10, smooth((x - b) / (W + 120 - b)))
    u = (x - a) / (b - a)
    return top + (DECK_Y - 60 - top) * (1 - (2 * u - 1) ** 2)


def bridge(c, t, lit=0.0, built=1.0, people=0.0):
    """The bridge side-on: deck, towers, main cables, the web of diagonal stays and the suspenders."""
    # deck
    c.drawRect(R(-120, DECK_Y - 12, W + 240, 34), P("#3F3A55"))
    c.drawRect(R(-120, DECK_Y - 18, W + 240, 8), P("#6B6385"))
    for x in TOWERS:
        tower(c, x, lit=lit)
    # suspenders and stays
    for k in range(-6, 62):
        x = k * 18
        cy = cable_y(x)
        if cy < DECK_Y - 16:
            c.drawLine(x, cy, x, DECK_Y - 14, P(CABLE, 0.6, stroke=1.6))
    for tx in TOWERS:
        for k in range(1, 9):
            for sd in (-1, 1):
                dx = tx + sd * (40 + k * 26)
                c.drawLine(tx + sd * 50, 370 + k * 6, dx, DECK_Y - 14, P(CABLE, 0.55, stroke=1.6))
    path = skia.Path()
    for k in range(0, 72):
        x = -120 + k * ((W + 240) / 71)
        (path.moveTo if k == 0 else path.lineTo)(x, cable_y(x))
    c.drawPath(path, P("#1F2937", 1, stroke=9))
    c.drawPath(path, P("#64748B", 0.6, stroke=3))
    if lit > 0:                                          # lamps along the deck
        for k in range(16):
            x = 30 + k * 66
            add_glow(c, x, DECK_Y - 26, 22, "#FDE68A", 0.8 * lit)
            c.drawCircle(x, DECK_Y - 26, 4, P("#FFF7D6", lit))
        for x in TOWERS:
            add_glow(c, x, 330, 60, "#FDE68A", 0.5 * lit)


def river(c, t, lit=0.0):
    c.drawRect(R(0, WATER_Y, W, H - WATER_Y), lin_paint(0, WATER_Y, 0, H, ["#1E3A5F", "#0F1E33"]))
    for k in range(18):
        xx = (k * 70 + t * 30) % (W + 60) - 30
        yy = WATER_Y + 20 + (k % 5) * 34
        c.drawLine(xx, yy, xx + 40, yy, P("#FDBA74" if lit == 0 else "#FDE68A", 0.35, stroke=3))


def elephant(c, x, y, s, t, a=1.0, ph=0.0):
    """A walking elephant seen from the side (facing right), feet on y; s = 1 is about 120 px tall."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    col = "#9CA3AF"
    dark = "#6B7280"
    sw = math.sin(t * 6 + ph)
    for k, lx in enumerate((-38, -20, 22, 40)):          # legs
        dx = sw * 6 * (1 if k % 2 else -1)
        c.drawRRect(rr(lx - 9 + dx, -48, 18, 48, 6), P(dark if k in (1, 2) else col, a))
    c.drawRRect(rr(-60, -112, 116, 72, 34), P(col, a))
    c.drawCircle(64, -98, 30, P(col, a))
    ear = skia.Path()
    ear.addOval(R(38, -122, 30, 42))
    c.drawPath(ear, P(dark, a))
    trunk = skia.Path()
    trunk.moveTo(86, -96)
    trunk.cubicTo(104, -80, 98, -50, 92 + sw * 4, -30)
    c.drawPath(trunk, P(col, a, stroke=13))
    c.drawCircle(72, -106, 3.5, P("#111827", a))
    c.drawLine(-60, -96, -72, -70, P(dark, a, stroke=4))
    c.restore()


def elephants(c, t, k=1.0, n=21, x0=-80, speed=36.0, s=0.42):
    for i in range(n):
        x = x0 + i * 52 + t * speed
        elephant(c, x, DECK_Y - 18, s, t, a=k, ph=i * 0.7)


# ====================================================================================== people and props
def lady(c, x, y, h, t, dress="#7C3AED", a=1.0, sit=False):
    """A woman in an 1880s dress with a bustle and a small hat (feet on y, facing right)."""
    if a <= 0:
        return
    u = h / 140.0
    c.save()
    c.translate(x, y)
    c.scale(u, u)
    if not sit:
        sk = skia.Path()
        sk.moveTo(-20, -70)
        sk.lineTo(20, -70)
        sk.lineTo(36, 0)
        sk.lineTo(-44, 0)
        sk.quadTo(-56, -40, -30, -60)
        sk.close()
        c.drawPath(sk, P(dress, a))
    else:
        c.drawRRect(rr(-34, -46, 70, 40, 14), P(dress, a))
    c.drawRRect(rr(-16, -110, 32, 46, 12), P(shade(dress, -0.15), a))
    c.drawLine(10, -100, 30, -76, P("#F1C9A5", a, stroke=7))
    c.drawCircle(-15, -128, 8, P("#3F2A1E", a))                  # hair bun, behind the head
    c.drawCircle(0, -124, 15, P("#F1C9A5", a))
    c.drawArc(R(-15, -140, 30, 22), 180, 180, True, P("#3F2A1E", a))
    c.drawRRect(rr(-18, -146, 36, 10, 4), P("#111827", a))      # little hat
    c.drawRect(R(-8, -158, 16, 14), P("#111827", a))
    c.drawCircle(5, -125, 1.8, P("#111827", a))
    c.restore()


def rooster(c, x, y, s, a=1.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for k, col in enumerate(("#065F46", "#1E3A8A", "#7C2D12")):
        c.drawLine(-14, -10, -34 - k * 4, -40 + k * 10, P(col, a, stroke=7))
    c.drawOval(R(-20, -24, 38, 24), P("#B45309", a))
    c.drawCircle(18, -30, 9, P("#B45309", a))
    c.drawCircle(18, -42, 5, P("#DC2626", a))
    c.drawCircle(23, -41, 4, P("#DC2626", a))
    tri = skia.Path()
    tri.moveTo(26, -32)
    tri.lineTo(34, -29)
    tri.lineTo(26, -26)
    tri.close()
    c.drawPath(tri, P("#FACC15", a))
    c.restore()


def carriage(c, x, y, s, t, a=1.0):
    """An open carriage drawn by a horse, wheels on y (facing right)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for wx in (-60, 50):
        c.drawCircle(wx, -30, 30, P("#111827", a, stroke=6))
        c.save()
        c.translate(wx, -30)
        c.rotate(t * 200)
        for k in range(4):
            c.rotate(45)
            c.drawLine(-28, 0, 28, 0, P("#111827", a, stroke=3))
        c.restore()
    c.drawRRect(rr(-90, -96, 170, 50, 14), P("#7F1D1D", a))
    c.drawLine(80, -70, 150, -60, P("#3F2A1E", a, stroke=5))
    hb = skia.Path()                                       # the horse
    hb.addRRect(rr(150, -110, 110, 50, 24))
    c.drawPath(hb, P("#78350F", a))
    for k, lx in enumerate((160, 178, 232, 248)):
        dx = math.sin(t * 8 + k) * 5
        c.drawLine(lx, -64, lx + dx, 0, P("#78350F", a, stroke=10))
    c.drawLine(250, -100, 280, -140, P("#78350F", a, stroke=22))
    c.drawCircle(288, -146, 16, P("#78350F", a))
    c.restore()


def desk(c, t, plan=1.0):
    """1869: a drafting desk with the drawing of the bridge, a top hat, a candle."""
    vrect(c, 0, 0, W, H, ["#1C1410", "#2A1E16"])
    c.drawRect(R(0, 300, W, 620), P("#3B2A1E"))
    for k in range(7):
        c.drawLine(k * 160, 300, k * 160, 920, P("#2A1E16", 1, stroke=6))
    c.drawRect(R(60, 900, 960, 60), P("#5B3A21"))
    c.drawRect(R(100, 960, 40, 280), P("#4A2E19"))
    c.drawRect(R(940, 960, 40, 280), P("#4A2E19"))
    c.drawRRect(rr(160, 560, 620, 360, 10), P("#BFB08E"))          # the drawing
    c.save()
    c.translate(180, 600)
    c.scale(0.53, 0.53)
    c.translate(0, -300)
    k = clamp(plan)
    for x in TOWERS:
        c.drawRect(R(x - 40, 330, 80, (DECK_Y - 330 + 60) * k), P("#1E3A8A", 0.8, stroke=4))
    c.drawLine(-60, DECK_Y, (W + 60) * k, DECK_Y, P("#1E3A8A", 0.8, stroke=4))
    path = skia.Path()
    for i in range(0, int(60 * k) + 2):
        x = -60 + i * ((W + 120) / 60)
        (path.moveTo if i == 0 else path.lineTo)(x, cable_y(x))
    c.drawPath(path, P("#1E3A8A", 0.8, stroke=4))
    c.restore()
    c.drawRRect(rr(820, 820, 140, 26, 8), P("#111827"))               # the top hat
    c.drawRRect(rr(846, 720, 88, 104, 10), P("#111827"))
    c.drawRect(R(846, 790, 88, 12), P("#7F1D1D"))
    c.drawRect(R(890, 840, 20, 60), P("#F1F5F9"))                    # the candle
    fl = 0.8 + 0.2 * math.sin(t * 13)
    c.drawOval(R(892, 812 - 10 * fl, 16, 30 * fl), P("#FDBA74"))
    add_glow(c, 900, 820, 120, "#FDBA74", 0.25)
    c.drawRRect(rr(380, 330, 280, 200, 10), P("#4A2E19"))           # an empty portrait frame on the wall
    c.drawRRect(rr(400, 350, 240, 160, 6), P("#1F2937"))
    c.drawLine(400, 350, 470, 350, P("#111827", 1, stroke=14))
    c.drawLine(400, 350, 400, 420, P("#111827", 1, stroke=14))


def caisson_section(c, t, sink=1.0, water_in=0.0, air=0.0, dig=0.0, stones=0.0):
    """The East River cut open: a giant upside-down wooden box on the riverbed, men in the working chamber."""
    vrect(c, 0, 0, W, 470, ["#F59E0B", "#FB923C", "#FDBA74"])
    c.drawRect(R(0, 470, W, 520), lin_paint(0, 470, 0, 990, ["#1E40AF", "#0C2340"]))
    for k in range(10):
        xx = (k * 120 + t * 40) % (W + 80) - 40
        c.drawLine(xx, 490, xx + 60, 490, P("#BFDBFE", 0.5, stroke=3))
    c.drawRect(R(0, 990, W, H - 990), lin_paint(0, 990, 0, H, ["#5B4129", "#3B2A1C"]))
    rng = random.Random(3)
    for k in range(40):
        c.drawCircle(rng.uniform(0, W), rng.uniform(1010, 1260), rng.uniform(4, 12), P("#2A1E14", 0.5))
    bottom = lerp(700, 1110, smooth(sink))
    x0, x1 = 230, 850
    top = bottom - 250
    c.drawRect(R(x0, top, x1 - x0, 90), P("#7C4A1E"))                 # the thick timber roof
    for k in range(6):
        c.drawLine(x0, top + 15 * k, x1, top + 15 * k, P("#5B3415", 0.7, stroke=3))
    for sd in (0, 1):                                                  # the sloping walls down to the cutting edge
        wx = x0 if sd == 0 else x1
        p = skia.Path()
        p.moveTo(wx, top + 90)
        p.lineTo(wx + (40 if sd == 0 else -40), bottom)
        p.lineTo(wx + (-10 if sd == 0 else 10), bottom)
        p.lineTo(wx + (-30 if sd == 0 else 30), top + 90)
        p.close()
        c.drawPath(p, P("#7C4A1E"))
    cx0, cx1 = x0 + 30, x1 - 30
    chamber = R(cx0, top + 90, cx1 - cx0, bottom - top - 90)
    c.drawRect(chamber, P("#1C1917"))
    for k in range(3):                                                 # lamps
        lx = cx0 + 90 + k * 190
        add_glow(c, lx, top + 120, 70, "#FDBA74", 0.6)
        c.drawCircle(lx, top + 120, 7, P("#FDE68A"))
    if water_in > 0:                                                   # water rushing up from the riverbed
        lvl = lerp(bottom, top + 120, clamp(water_in))
        c.drawRect(R(cx0, lvl, cx1 - cx0, bottom - lvl), P("#2563EB", 0.75))
        for k in range(8):
            u = (t * 2 + k / 8) % 1.0
            c.drawLine(cx0 + 40 + k * 70, bottom, cx0 + 40 + k * 70, bottom - 120 * u, P("#BFDBFE", 0.7 * (1 - u), stroke=5))
    if air > 0:                                                        # air pumped down the pipe, bubbles out under the edge
        c.drawLine(640, 0, 640, top + 100, P("#94A3B8", 1, stroke=18))
        for k in range(6):
            u = (t * 1.5 + k / 6) % 1.0
            c.drawCircle(640, lerp(470, top + 90, u), 10, P("#E0F2FE", 0.8 * air))
        for k in range(10):
            u = (t * 0.8 + k / 10) % 1.0
            bx = x1 + 20 + (k % 3) * 20 if k % 2 else x0 - 20 - (k % 3) * 20
            c.drawCircle(bx, lerp(bottom, 480, u), 8 + 6 * u, P("#E0F2FE", 0.6 * air * (1 - u)))
    n = 4
    for k in range(n):                                                 # men digging
        px = cx0 + 80 + k * 140
        dip = math.sin(t * 5 + k) * 0.5 + 0.5 if dig > 0 else 0.0
        person(c, px, bottom - 6, 150, SHIRTS[k % len(SHIRTS)], t + k, pose="duck" if dip > 0.6 else "carry",
               face=1 if k % 2 else -1, hat="hard", soot=0.4)
    c.drawRect(R(520, 0, 60, top), P("#57534E", 0.9))                  # the shaft up through the water
    c.drawRect(R(530, 0, 40, top), P("#1C1917"))
    if stones > 0:                                                     # stone piled on the roof: the tower's base
        rows = int(6 * clamp(stones)) + 1
        for r in range(rows):
            for k in range(7):
                bx = x0 + 10 + k * 88 + (44 if r % 2 else 0)
                if bx + 80 > x1:
                    continue
                c.drawRRect(rr(bx, top - 40 - r * 42, 82, 38, 4), P(GRANITE[0] if (r + k) % 2 else GRANITE[1]))


def blood_inset(c, x, y, r, t, k):
    """A round inset: a blood vessel with bubbles fizzing up in it."""
    if k <= 0:
        return
    c.save()
    c.translate(x, y)
    s_ = e_back(clamp(k))
    c.scale(s_, s_)
    c.drawCircle(0, 0, r, P("#0B1220", 0.9))
    c.save()
    c.clipPath(skia.Path().addCircle(0, 0, r - 4), skia.ClipOp.kIntersect, True)
    c.drawRect(R(-r, -r * 0.45, 2 * r, r * 0.9), P("#B91C1C"))
    for j in range(8):
        cx_ = -r + ((j * 60 + t * 90) % (2 * r))
        c.drawCircle(cx_, (j % 3 - 1) * 20, 8, P("#7F1D1D"))
    rng = random.Random(8)
    for j in range(int(16 * clamp(k * 1.4))):
        bx = rng.uniform(-r, r)
        by = rng.uniform(-r * 0.4, r * 0.4)
        c.drawCircle(bx, by, rng.uniform(5, 14), P("#F8FAFC", 0.85))
    c.restore()
    c.drawCircle(0, 0, r, P("#F87171", 1.0, stroke=6))
    c.restore()


def window_room(c, t, scope=1.0, note=0.0):
    """The boss in bed by his window, a telescope on the towers across the river."""
    vrect(c, 0, 0, W, H, ["#2B2118", "#3A2C20"])
    c.drawRRect(rr(140, 280, 800, 560, 16), P("#5B3A21"))
    c.save()
    c.clipRect(R(170, 310, 740, 500))
    vrect(c, 170, 310, 740, 500, ["#1E3A8A", "#F59E0B"])
    c.save()
    c.translate(170, 310)
    c.scale(0.68, 0.68)
    c.translate(0, -340)
    skyline(c, t)
    bridge(c, t, built=0.6)
    river(c, t)
    c.restore()
    c.restore()
    c.drawLine(540, 310, 540, 810, P("#5B3A21", 1, stroke=14))
    c.drawLine(170, 560, 910, 560, P("#5B3A21", 1, stroke=14))
    c.drawRRect(rr(80, 980, 640, 160, 30), P("#94A3B8"))                # the bed
    c.drawRRect(rr(60, 920, 60, 240, 20), P("#5B3A21"))
    c.drawRRect(rr(110, 960, 180, 70, 30), P("#CBD5E1"))
    c.drawRRect(rr(260, 1000, 420, 110, 40), P("#1E3A8A"))
    c.drawCircle(220, 960, 42, P("#F1C9A5"))
    c.drawRRect(rr(196, 976, 56, 14, 6), P("#6B4B3A"))                   # mustache
    c.drawCircle(206, 926, 30, P("#6B4B3A"))
    if scope > 0:                                                        # the telescope on a tripod at the window
        c.drawLine(760, 1150, 800, 960, P("#3F2A1E", 1, stroke=8))
        c.drawLine(840, 1150, 800, 960, P("#3F2A1E", 1, stroke=8))
        c.save()
        c.translate(800, 950)
        c.rotate(-28)
        c.drawRRect(rr(-120, -20, 240, 40, 16), P("#B7791F", scope))
        c.drawRRect(rr(110, -26, 30, 52, 10), P("#78350F", scope))
        c.restore()
    if note > 0:
        c.save()
        c.translate(lerp(340, 620, e_out(note)), lerp(940, 860, e_out(note)))
        c.rotate(-8)
        c.drawRect(R(-50, -36, 100, 72), P("#FEF3C7"))
        for j in range(4):
            c.drawLine(-36, -20 + j * 14, 36, -20 + j * 14, P("#92400E", 0.7, stroke=3))
        c.restore()


def cable_cut(c, x, y, r, t, bad=0.0, extra=0.0, snap=0.0):
    """A main cable cut across: hundreds of wires packed in a circle; bad wires turn red and snap; extra wires ring it."""
    c.drawCircle(x, y, r + 26, P("#1F2937"))
    c.drawCircle(x, y, r + 26, P("#64748B", 1, stroke=6))
    d = 13.0
    rng = random.Random(11)
    row = 0
    yy = y - r
    while yy <= y + r:
        xx = x - r + (d / 2 if row % 2 else 0)
        while xx <= x + r:
            if (xx - x) ** 2 + (yy - y) ** 2 <= (r - 6) ** 2:
                isbad = rng.random() < 0.18
                col = "#CBD5E1"
                if isbad and bad > 0:
                    col = mix("#CBD5E1", "#EF4444", clamp(bad))
                    if snap > 0 and rng.random() < 0.5:
                        c.drawCircle(xx + snap * rng.uniform(-30, 30), yy + snap * 40, 4, P(col, 1 - snap))
                        xx += d
                        continue
                c.drawCircle(xx, yy, 5.2, P(col))
            xx += d
        yy += d * 0.87
        row += 1
    if extra > 0:                                                         # 150 extra wires round the outside
        n = int(150 * clamp(extra))
        for k in range(n):
            ang = k / 150 * math.tau * 2.0
            rr_ = r + 6 + (k % 2) * 11
            c.drawCircle(x + math.cos(ang) * rr_, y + math.sin(ang) * rr_, 5.0, P("#22C55E"))


def crook(c, x, y, h, t, a=1.0):
    """A crook in a top hat holding out a spool of wire (feet on y, facing right)."""
    person(c, x, y, h, "#1F2937", t, pose="carry", face=1, hair="#111827", a=a)
    u = h / 140.0
    c.drawRRect(rr(x - 22 * u, y - 176 * u, 44 * u, 40 * u, 6 * u), P("#111827", a))
    c.drawRRect(rr(x - 32 * u, y - 140 * u, 64 * u, 8 * u, 4 * u), P("#111827", a))
    c.drawCircle(x + 70 * u, y - 86 * u, 26 * u, P("#9CA3AF", a))
    c.drawCircle(x + 70 * u, y - 86 * u, 26 * u, P("#EF4444", a, stroke=4 * u))
    c.drawCircle(x + 70 * u, y - 86 * u, 8 * u, P("#374151", a))


def plastic_chair(c, x, y, s, broke=0.0):
    """A white plastic garden chair (feet on y); broke 0..1 splays the legs and drops the seat."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    sp = 40 * broke
    drop = 50 * broke
    for sd in (-1, 1):
        c.drawLine(sd * 60, -110 + drop, sd * (70 + sp * 2), 0, P("#B8C0CC", 1, stroke=16))
        c.drawLine(sd * 40, -110 + drop, sd * (30 + sp), 0, P("#A3ADBA", 1, stroke=14))
    c.drawRRect(rr(-80, -130 + drop, 160, 28, 12), P("#C5CDD8"))
    c.drawRRect(rr(-72, -260 + drop, 144, 120, 30), P("#C5CDD8"))
    for k in range(3):
        c.drawLine(-46 + k * 46, -240 + drop, -46 + k * 46, -160 + drop, P("#94A3B8", 1, stroke=10))
    if broke > 0.2:
        c.drawLine(-70, -40, -40, -60, P("#111827", 1, stroke=4))
        c.drawLine(50, -50, 80, -20, P("#111827", 1, stroke=4))
    c.restore()


class Brooklyn(EpisodeV2):
    BUILD_NO = 105
    FIRST_SET = "bridge"
    CLEAR = "#120E1F"
    TITLE = {"en": "BROOKLYN BRIDGE", "ar_sa": "جسر بروكلين"}
    EMPH = {"en": ["TWENTY-ONE", "ELEPHANTS", "MARCHED", "BRIDGE", "PURPOSE", "ENGINEER", "DIED", "FINISHED", "SON",
                   "GIANT", "WOODEN", "BOXES", "RIVERBED", "WATER", "RUSHES", "BELOW", "AIR", "PUSHES", "DIG", "FAST",
                   "BENDS", "BOSS", "BED", "TELESCOPE", "CROOK", "BAD", "WIRE", "CABLES", "HUNDRED", "FIFTY", "EXTRA",
                   "WIRES", "CABLE", "FOLLOW", "METRO", "TRAINS", "WIFE", "EMILY", "MATH", "JOB", "FIRST", "FOUR",
                   "FIVE", "THOUSAND", "CONGRATS", "YOURSELF", "HELD", "UNCLE", "PLASTIC", "CHAIR", "CRACK"],
            "ar_sa": ["واحد", "وعشرين", "فيل", "مشوا", "قصد", "صمّمه", "مات", "كمّله", "فولده", "صناديق", "خشب",
                      "لقاع", "موية", "تدخل", "تحت", "هوا", "يطرد", "يحفرون", "بسرعة", "الغواصين", "المدير",
                      "سريره", "بالدربيل", "نصّاب", "مغشوش", "للكيابل", "مية", "وخمسين", "كيبل", "متابعة", "الرياض",
                      "سواق", "زوجته", "إميلي", "الحساب", "عبرته", "أربع", "آلاف", "مبروك", "وكرسي", "البلاستيك",
                      "الاستراحة", "ينكسر", "عمك"]}
    KEYS = {"ar_sa": {
        ("hook", "ELEPHANTS"): "فيل", ("hook", "MARCHED"): "مشوا", ("hook", "PURPOSE"): "قصد",
        ("break1", "ENGINEER"): "صممه", ("break1", "DIED"): "مات", ("break1", "FINISHED"): "كمله",
        ("fix1", "SON"): "ولده", ("fix1", "WOODEN"): "خشب", ("fix1", "RIVERBED"): "لقاع",
        ("break2", "WATER"): "موية", ("break2", "RUSHES"): "تدخل", ("break2", "BELOW"): "تحت",
        ("fix2", "AIR"): "هوا", ("fix2", "PUSHES"): "يطرد", ("fix2", "DIG"): "يحفرون",
        ("break3", "FAST"): "بسرعة", ("break3", "BENDS"): "الغواصين", ("break3", "BOSS"): "المدير",
        ("fix3", "BED"): "سريره", ("fix3", "TELESCOPE"): "بالدربيل",
        ("break4", "CROOK"): "نصاب", ("break4", "BAD"): "مغشوش", ("break4", "CABLES"): "للكيابل",
        ("fix4", "HUNDRED"): "مية", ("fix4", "EXTRA"): "سلك", ("fix4", "CABLE"): "كيبل",
        ("cta", "FOLLOW"): "متابعة", ("cta", "METRO"): "مترو",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "EMILY"): "إميلي", ("reveal", "MATH"): "الحساب",
        ("reveal", "FIRST"): "عبرته",
        ("stat", "FOUR"): "أربع", ("stat", "FIVE"): "خمسة", ("stat", "TWENTY"): "وعشرين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "HELD"): "صار", ("tag", "CHAIR"): "وكرسي", ("tag", "CRACK"): "ينكسر"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a metro with no drivers"),
                   "stat": [("4", "MAIN CABLES"), ("5,434", "WIRES IN EACH"), ("21", "ELEPHANTS, 1884")],
                   "L": {"elephants": "21 ELEPHANTS... ON PURPOSE", "y1869": "1869: ITS ENGINEER DIED",
                         "who": "SO WHO FINISHED IT?", "son": "HIS SON TOOK OVER", "boxes": "GIANT WOODEN BOXES",
                         "rush": "WATER RUSHES IN!", "air": "PUMPED-IN AIR", "dig": "MEN DIG INSIDE",
                         "fast": "CLIMB OUT TOO FAST...", "bends": "THE BENDS!", "boss": "EVEN THE BOSS!",
                         "bed": "BOSS IN BED", "scope": "WATCHING BY TELESCOPE", "crook": "A CROOK!",
                         "bad": "BAD WIRE!", "extra": "+150 WIRES PER CABLE", "safe": "STRONG ENOUGH",
                         "emily": "EMILY ROEBLING", "math": "SHE LEARNED THE MATH", "first": "FIRST ACROSS, 1883",
                         "name": "BROOKLYN BRIDGE", "held": "21 ELEPHANTS: IT HELD", "crack": "CRACK!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مترو بدون سواق"),
                      "stat": [("4", "كيابل"), ("5,434", "سلك في كل كيبل"), ("21", "فيل")],
                      "L": {"elephants": "واحد وعشرين فيل... عن قصد", "y1869": "1869: مات اللي صممه",
                            "who": "طيب مين كمّله؟", "son": "ولده مسك الشغل", "boxes": "صناديق خشب عملاقة",
                            "rush": "الموية تدخل!", "air": "هوا قوي يطرد الموية", "dig": "الرجال يحفرون",
                            "fast": "يطلع بسرعة...", "bends": "مرض الغواصين!", "boss": "حتى المدير!",
                            "bed": "المدير في سريره", "scope": "يراقبهم بالدربيل", "crook": "نصّاب!",
                            "bad": "سلك مغشوش!", "extra": "150+ سلك في كل كيبل", "safe": "احتياط",
                            "emily": "إميلي رووبلينغ", "math": "تعلّمت الحساب", "first": "أول وحدة عبرته",
                            "name": "جسر بروكلين", "held": "21 فيل: ولا صار شي", "crack": "طاخ!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "eleph": ("hook", "ELEPHANTS", 0.3), "marched": ("hook", "MARCHED", 0.55), "purpose": ("hook", "PURPOSE", 0.9),
            "designer": ("break1", "ENGINEER", 0.15), "died": ("break1", "DIED", 0.3), "finished": ("break1", "FINISHED", 0.85),
            "son": ("fix1", "SON", 0.2), "wooden": ("fix1", "WOODEN", 0.6), "riverbed": ("fix1", "RIVERBED", 0.9),
            "water": ("break2", "WATER", 0.3), "rushes": ("break2", "RUSHES", 0.5), "below": ("break2", "BELOW", 0.9),
            "air": ("fix2", "AIR", 0.2), "pushes": ("fix2", "PUSHES", 0.4), "dig": ("fix2", "DIG", 0.85),
            "fast": ("break3", "FAST", 0.3), "bends": ("break3", "BENDS", 0.55), "boss": ("break3", "BOSS", 0.85),
            "bed": ("fix3", "BED", 0.45), "scope": ("fix3", "TELESCOPE", 0.85),
            "crook": ("break4", "CROOK", 0.25), "bad": ("break4", "BAD", 0.55), "cables": ("break4", "CABLES", 0.9),
            "hundred": ("fix4", "HUNDRED", 0.35), "extra": ("fix4", "EXTRA", 0.65), "cable": ("fix4", "CABLE", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "answer": ("reveal", "ANSWER", 0.05), "emily": ("reveal", "EMILY", 0.25), "math": ("reveal", "MATH", 0.5),
            "first": ("reveal", "FIRST", 0.9),
            "s1": ("stat", "FOUR", 0.05), "s2": ("stat", "FIVE", 0.35), "s3": ("stat", "TWENTY", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_held": ("tag", "HELD", 0.3), "t_chair": ("tag", "CHAIR", 0.75), "t_crack": ("tag", "CRACK", 0.9)})
        T["died1"] = max(T["died"], T["designer"] + 0.2)
        T["sunk1"] = max(T["riverbed"], T["wooden"] + 0.3)
        T["rush1"] = max(T["rushes"], T["water"] + 0.2)
        T["dig1"] = max(T["dig"], T["pushes"] + 0.3)
        T["bends1"] = max(T["bends"], T["fast"] + 0.3)
        T["scope1"] = max(T["scope"], T["bed"] + 0.3)
        T["bad1"] = max(T["bad"], T["crook"] + 0.3)
        T["extra1"] = max(T["cable"], T["extra"] + 0.2)
        # ---- sets
        self.cut(s("break1") - 0.12, "office", 1)
        self.cut(s("fix1") - 0.12, "river", -1)
        self.cut(s("break3") - 0.12, "bends", 1)
        self.cut(s("break4") - 0.12, "cable", -1)
        self.cut(s("cta") - 0.12, "bridge", 1)
        self.cut(s("reveal") - 0.12, "emily", -1)
        self.cut(s("stat") - 0.12, "bridge", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["died1"], T["sunk1"]), (T["rush1"], T["dig1"]), (T["bends1"], T["scope1"]), (T["bad1"], T["extra1"])]
        self.shakes = [(T["marched"], 0.3, 4), (T["died1"], 0.3, 5), (T["sunk1"], 0.35, 7), (T["rush1"], 0.4, 8),
                       (T["bends1"], 0.35, 6), (T["bad1"] + 0.3, 0.35, 7), (s("closer") + 0.2, 0.35, 6),
                       (T["t_crack"], 0.35, 9)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: bridge (hook, cta, stat, closer)
    def draw_bridge(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        night = ph == "closer"
        if ph == "hook":
            k = e_io(prog(t, T["eleph"] - 0.2, T["purpose"] + 0.2))
            z = lerp(2.5, 1.0, k)
            px, py = lerp(420, 540, k), lerp(DECK_Y - 40, 760, k)
        else:
            z, px, py = 1.0, 540, 760
        c.save()
        c.translate(540, 760)
        c.scale(z, z)
        c.translate(-px, -py)
        sky(c, ["#1E1B4B", "#7C3AED", "#F97316", "#FDBA74"] if not night else ["#05060F", "#0F1033", "#1E1B4B", "#312E81"])
        if not night:
            add_glow(c, 820, 900, 260, "#FDBA74", 0.6)
        else:
            v2.stars(c, W, H, t, 0.8)
        skyline(c, t, lit=1.0 if night else 0.3)
        bridge(c, t, lit=1.0 if night else 0.0)
        if ph == "hook":
            elephants(c, t, k=1.0, x0=-80)
        elif ph == "stat":
            elephants(c, t - s("stat"), k=1.0, x0=-160)
        river(c, t, lit=1.0 if night else 0.0)
        c.restore()

    def ui_bridge(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "elephants", T["eleph"] - 0.1, s("break1") + 0.1, accent=HILITE, size=46)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=52)

    # ------------------------------------------------------------------ set: office (break1)
    def draw_office(self, c, t):
        T, s = self.T, self.tl.s
        desk(c, t, plan=prog(t, s("break1"), T["died"] + 0.6))

    def ui_office(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 1180, "y1869", T["designer"] - 0.1, T["finished"] - 0.6, accent=WARN, size=44)
        self.chip(540, 300, "who", T["finished"] - 0.6, s("fix1") - 0.1, accent=HILITE, size=50)
        self.badge("alert", T["died1"], s("fix1") - 0.2, x=920, y=440)
        self.red(T["died1"], 1.2)

    # ------------------------------------------------------------------ set: river (fix1, break2, fix2)
    def draw_river(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "fix1":
            caisson_section(c, t, sink=prog(t, T["wooden"] - 0.3, T["riverbed"] + 0.3),
                            stones=prog(t, T["wooden"], T["riverbed"] + 0.6))
        elif ph == "break2":
            caisson_section(c, t, sink=1.0, stones=1.0, water_in=prog(t, T["water"] - 0.2, T["below"]))
        else:
            caisson_section(c, t, sink=1.0, stones=1.0, water_in=0.75 * (1 - prog(t, T["air"], T["pushes"] + 0.6)),
                            air=prog(t, T["air"] - 0.3, T["air"]), dig=prog(t, T["dig"] - 0.4, T["dig"]))

    def ui_river(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix1":
            self.chip(540, 300, "son", T["son"] - 0.2, T["wooden"] - 0.15, accent="#FDE68A", size=50)
            self.chip(540, 300, "boxes", T["wooden"] - 0.15, s("break2") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["sunk1"], s("break2") - 0.15, x=920, y=440)
        elif ph == "break2":
            self.chip(540, 300, "rush", T["water"] - 0.2, s("fix2") - 0.15, accent=WARN, size=54)
            self.badge("alert", T["rush1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["rush1"], 1.2)
        else:
            self.chip(540, 300, "air", T["air"] - 0.2, T["dig"] - 0.2, accent="#7DD3FC", size=50)
            self.chip(540, 300, "dig", T["dig"] - 0.2, s("break3") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["dig1"], s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: bends (break3, fix3)
    def draw_bends(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break3":
            vrect(c, 0, 0, W, H, ["#1C1917", "#292524"])
            c.drawRect(R(380, 0, 320, 1250), P("#44403C"))
            c.drawRect(R(400, 0, 280, 1250), P("#0C0A09"))
            for k in range(14):
                yy = k * 90 + 20
                c.drawLine(440, yy, 640, yy, P("#A8A29E", 1, stroke=10))
            c.drawLine(440, 0, 440, 1250, P("#A8A29E", 1, stroke=10))
            c.drawLine(640, 0, 640, 1250, P("#A8A29E", 1, stroke=10))
            climb = prog(t, s("break3"), T["bends"])
            boss = prog(t, T["boss"] - 0.3, T["boss"] + 0.3)
            if boss < 1:
                person(c, 540, lerp(1240, 560, e_in(climb)), 300, "#0EA5E9", t, pose="cheer", face=1, hat="hard",
                       a=1 - boss)
            blood_inset(c, 820, 640, 170, t, prog(t, T["bends"] - 0.3, T["bends"] + 0.3) * (1 - boss))
            if boss > 0:                                 # the boss sinking into a chair
                c.drawRect(R(0, 0, W, H), P("#1C1917", 0.9 * boss))
                c.drawRRect(rr(380, 900, 320, 260, 40), P("#7F1D1D", boss))
                person(c, 540, 1100, 360, "#1F2937", t, pose="sit", face=1, hair="#6B4B3A", a=boss)
                blood_inset(c, 820, 640, 150, t, boss)
        else:
            window_room(c, t, scope=prog(t, T["bed"], T["scope"]), note=prog(t, T["scope"], T["scope"] + 0.8))

    def ui_bends(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "fast", T["fast"] - 0.2, T["bends"] - 0.1, accent="#FDE68A", size=50)
            self.chip(540, 300, "bends", T["bends"] - 0.1, T["boss"] - 0.2, accent=WARN, size=60)
            self.chip(540, 300, "boss", T["boss"] - 0.2, s("fix3") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["bends1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["bends1"], 1.2)
        else:
            self.chip(540, 300, "bed", T["bed"] - 0.3, T["scope"] - 0.1, accent="#FDE68A", size=50)
            self.chip(540, 300, "scope", T["scope"] - 0.1, s("break4") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["scope1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: cable (break4, fix4)
    def draw_cable(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
        if ph == "break4":
            k = prog(t, T["crook"] - 0.3, T["crook"] + 0.2)
            crook(c, lerp(-100, 200, e_out(k)), 1220, 420, t, a=k)
            cable_cut(c, 640, 760, 250, t, bad=prog(t, T["bad"] - 0.2, T["bad"] + 0.3),
                      snap=prog(t, T["bad1"] + 0.2, T["bad1"] + 0.8))
        else:
            cable_cut(c, 540, 760, 250, t, bad=1.0 - prog(t, s("fix4"), T["hundred"]), snap=0.0,
                      extra=prog(t, T["hundred"] - 0.2, T["cable"]))

    def ui_cable(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "crook", T["crook"] - 0.2, T["bad"] - 0.1, accent="#F8FAFC", size=56)
            self.chip(540, 300, "bad", T["bad"] - 0.1, s("fix4") - 0.15, accent=WARN, size=58)
            self.badge("alert", T["bad1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["bad1"], 1.2)
        else:
            self.chip(540, 300, "extra", T["hundred"] - 0.2, s("cta") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["extra1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: emily (reveal)
    def draw_emily(self, c, t):
        T, s = self.T, self.tl.s
        ride = prog(t, T["math"] + 0.3, T["first"])
        if ride < 1:                                    # Emily with the drawings at the boss's desk
            vrect(c, 0, 0, W, H, ["#2B2118", "#3A2C20"])
            c.drawRect(R(0, 900, W, 60), P("#5B3A21"))
            c.drawRRect(rr(140, 640, 520, 260, 10), P("#E8DCC0"))
            for j in range(6):
                c.drawLine(180, 680 + j * 34, 600, 680 + j * 34, P("#1E3A8A", 0.6, stroke=4))
            for j in range(5):                          # formulas: little squiggles
                c.drawLine(200 + j * 80, 860, 240 + j * 80, 840, P("#1E3A8A", 0.7, stroke=4))
            lady(c, 790, 1220, 520, t, a=1.0)
            if ride > 0:
                c.drawRect(R(0, 0, W, H), P("#000000", ride))
        if ride > 0:                                    # first across, 1883: the carriage and the rooster
            vrect(c, 0, 0, W, 1000, ["#1E3A8A", "#60A5FA", "#BFDBFE"], a=ride)
            c.drawRect(R(0, 1000, W, H - 1000), P("#57534E", ride))
            tower(c, 900, top=200, w=220)
            for k in range(16):
                person(c, 40 + k * 70, 1000 + (k % 2) * 30, 150, SHIRTS[k % len(SHIRTS)], t + k, pose="cheer",
                       face=1 if k < 8 else -1, a=ride)
            x = lerp(120, 300, prog(t, T["math"] + 0.3, s("stat")))
            carriage(c, x, 1220, 1.4, t, a=ride)
            lady(c, x - 20, 1220 - 96 * 1.4, 300, t, a=ride, sit=True)
            rooster(c, x + 40, 1220 - 120 * 1.4, 1.6, a=ride)

    def ui_emily(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "emily", T["emily"] - 0.2, T["math"] - 0.1, accent=HILITE, size=58)
        self.chip(540, 300, "math", T["math"] - 0.1, T["first"] - 0.3, accent="#FDE68A", size=48)
        self.chip(540, 300, "first", T["first"] - 0.3, s("stat") - 0.15, accent=GOOD, size=48)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#0B1026", "#1E1B4B"])
        for k in range(14):                             # string lights
            x = 40 + k * 76
            y = 260 + math.sin(k * 0.8) * 30
            add_glow(c, x, y, 26, "#FDE68A", 0.8)
            c.drawCircle(x, y, 7, P("#FFF7D6"))
        c.drawRect(R(0, 1060, W, 400), P("#3F6212"))
        c.drawRect(R(0, 1060, W, 18), P("#4D7C0F"))
        crack = prog(t, T["t_crack"] - 0.05, T["t_crack"] + 0.25)
        sit = prog(t, T["t_chair"] - 0.3, T["t_crack"])
        plastic_chair(c, 300, 1150, 1.2, broke=0.0)
        plastic_chair(c, 600, 1150, 1.4, broke=crack)
        y_uncle = lerp(1100, 1180, crack)
        person(c, 600, y_uncle - 150 * sit * (1 - crack), 420, "#D6DCE4", t, pose="sit" if sit > 0.5 else "stand",
               face=-1, hair="#111827")
        c.drawRRect(rr(820, 980, 160, 120, 20), P("#A16207"))         # a tray of tea
        for k in range(3):
            c.drawRRect(rr(836 + k * 46, 950, 30, 34, 6), P("#FDE68A", 0.9))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 360, "held", T["t_held"] - 0.15, T["t_crack"] - 0.1, accent="#F8FAFC", size=46)
        self.chip(540, 360, "crack", T["t_crack"] - 0.1, self.duration + 1, accent=WARN, size=64)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1F2937", "#111827"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["eleph"], sfx.thud(0.4, 62), -10), (T["marched"], sfx.thud(0.4, 63), -10),
              (T["marched"] + 0.5, sfx.thud(0.4, 64), -10), (T["purpose"], sfx.ding(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 65), -6), (T["died1"], sfx.womp(), -10),
               (T["died1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 66), -6), (T["wooden"], sfx.creak(1.0, 67), -10),
               (T["sunk1"], sfx.thud(0.4, 68), -6), (T["sunk1"] + 0.2, sfx.ding(), -8), (T["sunk1"] + 0.4, sfx.chime(), -6)]
        ev += [(T["water"], sfx.hiss(1.4, 69), -8), (T["rush1"], sfx.womp(), -10), (T["rush1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["air"], sfx.gas_hiss(1.2, 70) if False else sfx.hiss(1.2, 70), -10), (T["dig"], sfx.clank(500.0, 0.4, 71), -10),
               (T["dig1"], sfx.ding(), -8), (T["dig1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 72), -6), (T["bends"], sfx.sizzle(1.0, 73), -10),
               (T["boss"], sfx.thud(0.4, 74), -8), (T["bends1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["scope"], sfx.click(75), -6), (T["scope1"], sfx.ding(), -8), (T["scope1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 76), -6), (T["bad1"] + 0.3, sfx.snap(77), -4),
               (T["bad1"] + 0.5, sfx.alarm(3, 820.0), -12)]
        ev += [(T["hundred"], sfx.sparkle(1.0, 12, 78), -8), (T["extra1"], sfx.ding(), -8), (T["extra1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["emily"], sfx.ding(), -6),
               (T["first"] - 0.2, sfx.sparkle(1.0, 14, 95), -8)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_chair"], sfx.creak(0.6, 104), -8),
               (T["t_crack"], sfx.snap(105), -2), (T["t_crack"] + 0.1, sfx.thud(0.4, 106), -6)]
        return ev


NAME = "brooklyn"
EPISODE = Brooklyn
