"""Episode 97 - the Museum of the Future, Dubai.  v2 look: a stainless-steel ring standing on a green hill, its windows
the shapes of Arabic calligraphy (world: the ring centred at (0, 0), outer ellipse 430 x 300 units, the void 250 x 128
centred at (0, -14); the hill's top at y 255).

Sets: ring (hook: close on the glowing script, pull out to the whole ring at dusk over the city; break1: x-ray, seven
empty floors and no column; reveal: x-ray, the steel diagrid lights up; stat; closer: the ring at night), grow (fix1:
thousands of trial frames jitter on a blueprint and settle into one net), street (break2: a giant curved beam stuck
under a road sign bridge; fix2: trucks carrying short tubes of one width), panel (break3: a flat sheet wrinkles on a
saddle mould; fix3: a robot arm carves one curved panel after another), glass (break4: a square pane will not fit a
letter-shaped window; fix4: a water jet cuts the letter out of glass; cta), mom (tag: a mom with a spray bottle in
front of the whole ring, a cleaner's cradle swinging down it).
"""
from v2_base import *  # noqa: F401,F403

OA, OB = 430.0, 300.0                    # outer ellipse of the ring
IA, IB, ICY = 250.0, 128.0, -14.0        # the void
HILL_Y = 255.0
STEEL_HI, STEEL_MID, STEEL_DK = "#B7C0CD", "#7C8696", "#3F4757"
GLOW = "#FFD27A"
DUSK = ["#0A1238", "#2A2466", "#7A3C6E", "#F08A5D"]
NIGHTP = ["#040818", "#0B1438", "#1D2350", "#3A2A5C"]
TEAL = "#5EEAD4"


def ea(s):
    return lerp(IA, OA, s)


def eb(s):
    return lerp(IB, OB, s)


def ecy(s):
    return lerp(ICY, 0.0, s)


def rp(u, s):
    """A point on the ring band: u the angle around the ring, s 0 (edge of the void) .. 1 (outer edge)."""
    return ea(s) * math.cos(u), ecy(s) + eb(s) * math.sin(u)


def oval(s):
    return R(-ea(s), ecy(s) - eb(s), 2 * ea(s), 2 * eb(s))


def ring_path(s0=0.0, s1=1.0):
    p = skia.Path()
    p.addOval(oval(s1))
    p.addOval(oval(s0))
    p.setFillType(skia.PathFillType.kEvenOdd)
    return p


def band_poly(pts):
    path = skia.Path()
    for i, (u, s) in enumerate(pts):
        x, y = rp(u, s)
        if i == 0:
            path.moveTo(x, y)
        else:
            path.lineTo(x, y)
    return path


# the calligraphy: strokes in (u, s) band space, from a fixed seed (abstract strokes, no real words)
def _script(seed=7):
    rng = random.Random(seed)
    strokes, dots = [], []
    u = 0.0
    while u < 2 * math.pi - 0.15:
        row = rng.choice((0.32, 0.5, 0.68))
        kind = rng.random()
        w = rng.uniform(0.16, 0.3)
        if kind < 0.4:                                    # a long baseline sweep that lifts at the end
            pts = [(u + w * k / 10, row + 0.05 * math.sin(k * 0.6) - (0.18 * (k - 7) / 3 if k > 7 else 0)) for k in range(11)]
        elif kind < 0.62:                                 # a tall upright stroke with a foot
            pts = [(u, row - 0.24), (u + 0.004, row), (u + 0.02, row + 0.12), (u + 0.08, row + 0.14)]
        elif kind < 0.88:                                 # a wide shallow bowl
            pts = [(u + w * 0.6 * (1 - math.cos(a)), row + 0.12 * math.sin(a)) for a in [k * math.pi / 8 for k in range(9)]]
        else:                                             # a slanted stroke
            pts = [(u, row + 0.14), (u + 0.1, row - 0.18)]
        strokes.append(pts)
        if rng.random() < 0.6:
            dots.append((u + rng.uniform(0.02, w), row + rng.choice((-0.2, 0.22))))
        u += w * rng.uniform(0.55, 0.9)
    return strokes, dots


SCRIPT = _script()


def sky_bg(c, t, night=0.0, cx=0.0):
    """Dubai at dusk (night 0) or at night (1), screen space, with a far skyline and a thin needle tower."""
    cols = [mix(a, b, night) for a, b in zip(DUSK, NIGHTP)]
    vrect(c, 0, 0, W, H, cols, [0.0, 0.35, 0.62, 0.82])
    v2.stars(c, W, H, t, 0.25 + 0.75 * night, dx=-cx * 0.02)
    hz = 1270
    c.save()
    c.translate(-cx * 0.05, 0)
    nx = 905                                              # a far needle tower
    nd = skia.Path()
    nd.moveTo(nx - 26, hz)
    nd.lineTo(nx - 9, hz - 560)
    nd.lineTo(nx, hz - 700)
    nd.lineTo(nx + 9, hz - 560)
    nd.lineTo(nx + 26, hz)
    nd.close()
    c.drawPath(nd, P(mix("#2A2C5E", "#141A3C", night)))
    c.drawCircle(nx, hz - 700, 4, P("#FF5A5A", 0.6 + 0.4 * math.sin(t * 3)))
    skyline_night(c, -200, W + 200, base_y=hz, seed=6, hmin=120, hmax=420,
                  cols=(mix("#2B2A63", "#121738", night), mix("#352F70", "#181E45", night), mix("#22245A", "#0F1430", night)),
                  lit=0.25 + 0.4 * night, t=t)
    c.restore()


def hill(c, t):
    """The green hill the ring stands on (world), drawn after the ring so it hides the ring's foot."""
    path = skia.Path()
    path.moveTo(-900, 420)
    path.cubicTo(-560, 300, -360, HILL_Y - 4, 0, HILL_Y)
    path.cubicTo(360, HILL_Y - 4, 560, 300, 900, 420)
    path.lineTo(900, 900)
    path.lineTo(-900, 900)
    path.close()
    c.drawPath(path, lin_paint(0, HILL_Y, 0, 700, ["#2F8F4E", "#1C6B3A", "#0E3B22"]))
    for k in range(3):                                    # terraces
        y = HILL_Y + 40 + k * 46
        c.drawLine(-700 + k * 40, y + 60, 700 - k * 40, y + 60, P("#0F4A2A", 0.5, stroke=4))
    rng = random.Random(3)
    for k in range(22):                                   # shrubs
        x = rng.uniform(-760, 760)
        y = HILL_Y + 20 + abs(x) * 0.18 + rng.uniform(0, 120)
        r_ = rng.uniform(16, 30)
        c.drawCircle(x, y, r_, P(rng.choice(["#3FA35F", "#2E8B4F", "#4CB26B"])))
        c.drawCircle(x - r_ * 0.3, y - r_ * 0.3, r_ * 0.4, P("#7BD88F", 0.35))
    c.drawRect(R(-1400, 600, 2800, 1600), lin_paint(0, 600, 0, 1400, ["#1F2937", "#111827"]))    # the plaza
    for k in range(9):
        c.drawLine(-900, 620 + k * 26, 900, 620 + k * 26, P("#374151", 0.5, stroke=2))


def ring(c, t, glow=0.0, xray=0.0, floors=0.0, net=0.0, dark=0.0, a=1.0, seed_off=0.0):
    """The museum (world). glow 0..1 the script windows lit; xray 0..1 the skin fades to show what is inside; floors
    0..1 seven empty floors seen through it; net 0..1 the steel diagrid lit; dark 0..1 a night tint on the steel."""
    if a <= 0:
        return
    body = ring_path()
    if glow > 0:
        add_glow(c, 0, 0, 560, GLOW, 0.22 * glow * a)
    skin = 1 - 0.82 * xray
    c.drawPath(body, lin_paint(-OA, -OB, OA, OB, [mix(STEEL_HI, "#4B5568", dark), mix(STEEL_MID, "#323A4C", dark),
                                                 mix(STEEL_DK, "#1C2232", dark)], a=a * skin))
    if xray > 0:                                          # the inside: dark
        c.drawPath(body, P("#0B1226", 0.9 * xray * a))
    c.save()
    c.clipPath(body, skia.ClipOp.kIntersect, True)
    c.drawOval(oval(0.5), P("#FFFFFF", 0.16 * a * skin, stroke=70))           # rounded tube: lit middle,
    c.drawOval(oval(0.03), P("#0B1020", 0.35 * a * skin, stroke=26))          # darker edges
    c.drawOval(oval(0.98), P("#0B1020", 0.3 * a * skin, stroke=26))
    if floors > 0:                                        # seven floors, no columns
        for k in range(7):
            y = -OB + 50 + k * (2 * OB - 70) / 7
            c.drawRect(R(-OA, y, 2 * OA, 9), P("#93C5FD", 0.75 * floors * a))
            c.drawRect(R(-OA, y + 9, 2 * OA, 40), P("#1E3A8A", 0.18 * floors * a))
    n = 36
    for i in range(n):                                    # the diagrid
        u0 = i * 2 * math.pi / n + seed_off
        du = 2 * math.pi / n
        for sg in (1, -1):
            path = band_poly([(u0 + sg * k / 8 * du, k / 8) for k in range(9)])
            if net > 0:
                c.drawPath(path, P(TEAL, 0.25 * net * a, stroke=16))
                c.drawPath(path, P("#E0FFFA", 0.95 * net * a, stroke=5))
            else:
                c.drawPath(path, P("#1F2633", 0.32 * a * skin, stroke=3))
    ws = 1 - 0.7 * xray
    for pts in SCRIPT[0]:                                 # the windows: calligraphy
        path = band_poly(pts)
        if glow > 0:
            c.drawPath(path, P(GLOW, 0.3 * glow * a * ws, stroke=24))
        c.drawPath(path, P(mix("#1B2333", "#FFE7B0", glow), a * ws, stroke=10))
    for (u, s) in SCRIPT[1]:
        x, y = rp(u, s)
        c.save()
        c.translate(x, y)
        c.rotate(45)
        c.drawRect(R(-7, -7, 14, 14), P(mix("#1B2333", "#FFE7B0", glow), a * ws))
        c.restore()
    c.restore()
    c.drawOval(oval(0.0), P("#0E1424", 0.8 * a, stroke=6))
    c.drawOval(oval(1.0), P(mix("#D7DEE8", "#5B6478", dark), 0.6 * a, stroke=4))
    vd = skia.Path()                                      # the inner wall seen through the top of the void
    vd.addOval(oval(0.0))
    vd2 = skia.Path()
    vd2.addOval(R(-IA * 0.97, ICY - IB * 0.86 + 18, IA * 1.94, IB * 1.72))
    c.save()
    c.clipPath(vd, skia.ClipOp.kIntersect, True)
    c.clipPath(vd2, skia.ClipOp.kDifference, True)
    c.drawRect(R(-IA, ICY - IB, 2 * IA, IB), lin_paint(0, ICY - IB, 0, ICY, [mix("#5B6575", "#262D3D", dark), "#1A2030"], a=a * skin))
    c.restore()


def blueprint(c):
    vrect(c, 0, 0, W, H, ["#0B1B3A", "#0A1530"])
    for x in range(0, W + 1, 60):
        c.drawLine(x, 0, x, H, P("#1E3A6B", 0.5, stroke=1))
    for y in range(0, H + 1, 60):
        c.drawLine(0, y, W, y, P("#1E3A6B", 0.5, stroke=1))


def trial_net(c, t, settle, a=1.0, seed=0):
    """A trial frame on the ring (world): settle 0 = wild, 1 = the final net."""
    rng = random.Random(seed)
    n = 36
    amp = (1 - settle) * 0.28
    for i in range(n):
        u0 = i * 2 * math.pi / n
        du = 2 * math.pi / n * (1 + (rng.uniform(-0.6, 0.6) * (1 - settle)))
        for sg in (1, -1):
            pts = []
            for k in range(9):
                s = k / 8
                jitter = amp * math.sin(k * 1.7 + i * 0.9 + seed + t * 2) * (1 if sg > 0 else -1)
                pts.append((u0 + sg * s * du + jitter * 0.3, clamp(s + jitter * 0.2)))
            col = mix("#F472B6", TEAL, settle)
            c.drawPath(band_poly(pts), P(col, a * (0.4 + 0.6 * settle), stroke=3 + 2 * settle))


def truck(c, x, y, s=1.0, load="beam", t=0.0, a=1.0):
    """A flatbed truck facing right, wheels on y (screen). load: beam (a giant curved beam) | tubes (short tubes)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-260, -70, 380, 26, 6), P("#475569", a))                  # bed
    c.drawRRect(rr(120, -150, 120, 110, 18), lin_paint(120, 0, 240, 0, ["#F59E0B", "#D97706"], a=a))   # cab
    c.drawRRect(rr(170, -136, 56, 44, 8), P("#BFDBFE", 0.9 * a))
    for wx in (-200, -120, 180):
        c.drawCircle(wx, -18, 30, P("#111827", a))
        c.drawCircle(wx, -18, 12, P("#9CA3AF", a))
    if load == "beam":                                    # a curved beam far too big for the truck
        path = skia.Path()
        path.moveTo(-420, -80)
        path.cubicTo(-300, -420, 60, -470, 200, -300)
        c.drawPath(path, P(STEEL_MID, a, stroke=60))
        c.drawPath(path, P(STEEL_HI, 0.8 * a, stroke=18))
    elif load == "tubes":
        for row in range(3):
            for k in range(6):
                cx_ = -230 + k * 58 + (row % 2) * 29
                cy_ = -98 - row * 46
                c.drawCircle(cx_, cy_, 24, lin_paint(cx_ - 24, cy_ - 24, cx_ + 24, cy_ + 24, [STEEL_HI, STEEL_DK], a=a))
                c.drawCircle(cx_, cy_, 13, P("#1F2937", a))
    c.restore()


def street_bg(c, t):
    vrect(c, 0, 0, W, H, ["#1E3A8A", "#7DD3FC", "#FDE68A"])
    for k, (x, w, h) in enumerate(((60, 200, 640), (290, 170, 500), (500, 240, 760), (780, 220, 560))):   # towers
        c.drawRect(R(x, 1000 - h, w, h), lin_paint(x, 0, x + w, 0, ["#475569", "#64748B", "#334155"]))
        for yy in range(int(1000 - h + 30), 970, 56):
            for xx in range(int(x + 18), int(x + w - 20), 40):
                c.drawRect(R(xx, yy, 22, 30), P("#BFDBFE", 0.55))
    c.drawRect(R(0, 1000, W, 190), P("#374151"))          # the road
    for x in range(0, W, 140):
        c.drawRect(R(x + 30, 1088, 70, 12), P("#F8FAFC", 0.8))
    c.drawRect(R(0, 1190, W, H - 1190), P("#1F2937"))


def sign_bridge(c, a=1.0):
    """A road-sign gantry over the street (screen)."""
    for x in (120, 960):
        c.drawRect(R(x - 12, 600, 24, 420), P("#9CA3AF", a))
    c.drawRect(R(108, 590, 864, 30), P("#9CA3AF", a))
    c.drawRRect(rr(380, 496, 320, 96, 10), P("#15803D", a))
    c.drawRRect(rr(388, 504, 304, 80, 8), P("#FFFFFF", a, stroke=4))
    for k in range(3):
        c.drawRRect(rr(410 + k * 90, 526, 70, 12, 6), P("#FFFFFF", 0.85 * a))


def saddle_mould(c, x, y, s, t, wrinkle=0.0, a=1.0):
    """A doubly curved mould (a saddle) with a flat sheet laid on it that wrinkles (screen)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    top = skia.Path()
    top.moveTo(-300, -40)
    top.cubicTo(-150, -150, 150, -150, 300, -40)
    top.lineTo(300, 160)
    top.lineTo(-300, 160)
    top.close()
    c.drawPath(top, lin_paint(0, -150, 0, 160, ["#FCD34D", "#B45309"], a=a))   # yellow foam mould
    sheet = skia.Path()                                   # the flat sheet, sagging and buckling
    sheet.moveTo(-320, -70)
    for k in range(1, 33):
        xx = -320 + k * 20
        yy = -70 - 60 * math.sin(math.pi * k / 32) + wrinkle * 22 * math.sin(k * 1.9 + t * 3)
        sheet.lineTo(xx, yy)
    c.drawPath(sheet, P(STEEL_HI, a, stroke=16))
    if wrinkle > 0.3:
        for k in range(6):
            xx = -240 + k * 96
            c.drawLine(xx, -110, xx + 18, -70, P("#1F2937", 0.6 * a, stroke=4))
    c.restore()


def robot_arm(c, x, y, t, reach=0.0, a=1.0):
    """An industrial robot arm on a base at (x, y), its tool tip sweeping (screen)."""
    c.save()
    c.translate(x, y)
    c.drawRRect(rr(-70, -40, 140, 60, 12), P("#F97316", a))
    a1 = -70 + 18 * math.sin(t * 2.2) - 20 * reach
    a2 = 70 + 25 * math.sin(t * 2.2 + 1.2)
    l1, l2 = 260, 220
    x1 = math.cos(math.radians(a1)) * l1
    y1 = -40 + math.sin(math.radians(a1)) * l1
    x2 = x1 + math.cos(math.radians(a1 + a2)) * l2
    y2 = y1 + math.sin(math.radians(a1 + a2)) * l2
    c.drawLine(0, -40, x1, y1, P("#EA580C", a, stroke=54))
    c.drawLine(x1, y1, x2, y2, P("#F97316", a, stroke=40))
    for (px, py, r_) in ((0, -40, 34), (x1, y1, 28), (x2, y2, 18)):
        c.drawCircle(px, py, r_, P("#1F2937", a))
        c.drawCircle(px, py, r_ * 0.45, P("#9CA3AF", a))
    c.drawLine(x2, y2, x2, y2 + 60, P("#CBD5E1", a, stroke=10))
    c.restore()
    return x + x2, y + y2 + 60


def curved_panel(c, x, y, s, cut=1.0, a=1.0, glow=0.0):
    """One curved steel panel with a letter-shaped window cut in it (screen)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    path = skia.Path()
    path.moveTo(-180, -110)
    path.cubicTo(-60, -160, 60, -160, 180, -110)
    path.lineTo(200, 110)
    path.cubicTo(60, 70, -60, 70, -200, 110)
    path.close()
    c.drawPath(path, lin_paint(-200, -150, 200, 110, [STEEL_HI, STEEL_MID, STEEL_DK], a=a))
    c.drawPath(path, P("#E2E8F0", 0.7 * a, stroke=3))
    if cut > 0:
        ltr = skia.Path()
        ltr.moveTo(-120, 20)
        ltr.cubicTo(-80, 60, 40, 60, 90, 10)
        ltr.lineTo(110, -70)
        c.drawPath(ltr, P(mix("#111827", GLOW, glow), a * cut, stroke=26))
        c.drawCircle(-30, -50, 13, P(mix("#111827", GLOW, glow), a * cut))
    c.restore()


def letter_hole(c, x, y, s, a=1.0):
    """The letter-shaped opening (screen) the glass must fill; returns nothing."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    ltr = skia.Path()
    ltr.moveTo(-160, 30)
    ltr.cubicTo(-100, 110, 60, 110, 130, 20)
    ltr.lineTo(150, -120)
    c.drawPath(ltr, P("#0B1020", a, stroke=58))
    c.drawCircle(-40, -60, 30, P("#0B1020", a))
    c.restore()


def letter_glass(c, x, y, s, a=1.0, shine=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    ltr = skia.Path()
    ltr.moveTo(-160, 30)
    ltr.cubicTo(-100, 110, 60, 110, 130, 20)
    ltr.lineTo(150, -120)
    c.drawPath(ltr, P("#7DD3FC", 0.75 * a, stroke=50))
    c.drawPath(ltr, P("#E0F2FE", (0.4 + 0.5 * shine) * a, stroke=8))
    c.drawCircle(-40, -60, 25, P("#7DD3FC", 0.75 * a))
    c.restore()


# ====================================================================================== the episode
class Museum(EpisodeV2):
    BUILD_NO = 97
    FIRST_SET = "ring"
    CLEAR = "#060A1E"
    TITLE = {"en": "MUSEUM OF THE FUTURE", "ar_sa": "متحف المستقبل"}
    EMPH = {"en": ["DUBAI", "SILVER", "RING", "WINDOWS", "ARABIC", "WRITING", "COLUMNS", "HOLDING", "COMPUTER",
                   "THOUSANDS", "NET", "GIANT", "STREETS", "SAME", "WIDTH", "SHORT", "TRUCK", "FLAT", "BEND", "TWO",
                   "ROBOT", "CURVED", "PANEL", "LETTERS", "SQUARE", "WATER", "TEN", "GLASS", "FOLLOW", "WATERFALL",
                   "AIRPORT", "OUTSIDE", "TWENTY-FOUR", "BEAMS", "BASKET", "SEVENTY-SEVEN", "THOUSAND", "FOURTEEN",
                   "LIGHTS", "CONGRATS", "MUSEUM", "FUTURE", "YOURSELF", "MOM", "CLEANING"],
            "ar_sa": ["دبي", "خاتم", "فضي", "وشبابيكه", "حروف", "عمود", "شايله", "الكمبيوتر", "آلاف", "شبكة", "قطع",
                      "شوارع", "بنفس", "وقصيرة", "تريلة", "المسطح", "ينثني", "جهتين", "روبوت", "منحني", "مربع",
                      "فموية", "عشرة", "زجاج", "متابعة", "شلال", "مطار", "برّاه", "ألفين", "السلة", "سبعة", "ألف",
                      "كيلو", "أنوار", "مبروك", "متحف", "المستقبل", "أمي", "بيمسح"]}
    KEYS = {"ar_sa": {
        ("hook", "DUBAI"): "دبي", ("hook", "RING"): "خاتم", ("hook", "WINDOWS"): "شبابيكه", ("hook", "WRITING"): "حروف",
        ("break1", "COLUMNS"): "عمود", ("break1", "HOLDING"): "شايله",
        ("fix1", "COMPUTER"): "الكمبيوتر", ("fix1", "THOUSANDS"): "آلاف", ("fix1", "NET"): "شبكة", ("fix1", "FIT"): "تركب",
        ("break2", "PARTS"): "قطع", ("break2", "STREETS"): "شوارع",
        ("fix2", "SAME"): "بنفس", ("fix2", "SHORT"): "وقصيرة", ("fix2", "TRUCK"): "تريلة",
        ("break3", "FLAT"): "المسطح", ("break3", "BEND"): "ينثني", ("break3", "TWO"): "جهتين",
        ("fix3", "ROBOT"): "روبوت", ("fix3", "CURVED"): "منحني",
        ("break4", "LETTERS"): "حروف", ("break4", "SQUARE"): "مربع",
        ("fix4", "WATER"): "فموية", ("fix4", "TEN"): "عشرة", ("fix4", "GLASS"): "زجاج",
        ("cta", "FOLLOW"): "متابعة",
        ("reveal", "OUTSIDE"): "براه", ("reveal", "TWENTY"): "ألفين", ("reveal", "BASKET"): "السلة",
        ("stat", "SEVENTY"): "سبعة", ("stat", "THOUSAND"): "ألف", ("stat", "FOURTEEN"): "كيلو",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "MOM"): "أمي", ("tag", "CLEANING"): "بيمسح", ("tag", "WINDOWS"): "هالشبابيك"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a waterfall inside an airport"),
                   "stat": [("77 m", "TALL"), ("1,024", "STEEL PANELS"), ("14 km", "OF LIGHTS")],
                   "L": {"name": "MUSEUM OF THE FUTURE", "words": "THE WINDOWS ARE WORDS", "nocol": "NO COLUMNS",
                         "hold": "SO WHAT HOLDS IT UP?", "tries": "THOUSANDS OF TRIES", "net": "ONE STEEL NET",
                         "big": "TOO BIG FOR THE STREETS", "same": "ONE WIDTH, SHORT PIECES", "flat": "FLAT STEEL",
                         "two": "CURVES TWO WAYS = WRINKLES", "robot": "ROBOT ARMS", "each": "ONE PANEL AT A TIME",
                         "letters": "WINDOWS = LETTERS", "square": "NO PLAIN SQUARES", "jet": "WATER JET",
                         "pieces": "10,000+ GLASS PIECES", "outside": "THE OUTSIDE HOLDS IT UP!",
                         "beams": "2,400 STEEL BEAMS", "who": "WHO CLEANS ALL THOSE?", "try": "TRY #"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: شلال داخل مطار"),
                      "stat": [("77", "متر طول"), ("1024", "لوح حديد"), ("14", "كيلو أنوار")],
                      "L": {"name": "متحف المستقبل", "words": "الشبابيك حروف", "nocol": "ولا عمود",
                            "hold": "وش اللي شايله؟", "tries": "آلاف المحاولات", "net": "شبكة حديد وحدة",
                            "big": "أكبر من الشوارع", "same": "نفس العرض، قطع قصيرة", "flat": "حديد مسطح",
                            "two": "انحناء من جهتين = تجاعيد", "robot": "أذرع روبوت", "each": "لوح لوح",
                            "letters": "الشبابيك = حروف", "square": "ولا شباك مربع", "jet": "موية بضغط قوي",
                            "pieces": "أكثر من 10000 قطعة زجاج", "outside": "برّاه هو اللي شايله!",
                            "beams": "2400 عارضة حديد", "who": "مين بيمسحها؟", "try": "محاولة "}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "dubai": ("hook", "DUBAI", 0.2), "ring": ("hook", "RING", 0.45), "windows": ("hook", "WINDOWS", 0.7),
            "writing": ("hook", "WRITING", 0.9),
            "columns": ("break1", "COLUMNS", 0.15), "holding": ("break1", "HOLDING", 0.8),
            "computer": ("fix1", "COMPUTER", 0.15), "thousands": ("fix1", "THOUSANDS", 0.4), "net": ("fix1", "NET", 0.8),
            "fit": ("fix1", "FIT", 0.95),
            "parts": ("break2", "PARTS", 0.3), "streets": ("break2", "STREETS", 0.85),
            "same": ("fix2", "SAME", 0.3), "short": ("fix2", "SHORT", 0.6), "truck": ("fix2", "TRUCK", 0.9),
            "flat": ("break3", "FLAT", 0.15), "bend": ("break3", "BEND", 0.4), "two": ("break3", "TWO", 0.85),
            "robot": ("fix3", "ROBOT", 0.15), "curved": ("fix3", "CURVED", 0.55),
            "letters": ("break4", "LETTERS", 0.3), "square": ("break4", "SQUARE", 0.85),
            "water": ("fix4", "WATER", 0.1), "ten": ("fix4", "TEN", 0.5), "glass": ("fix4", "GLASS", 0.8),
            "follow": ("cta", "FOLLOW", 0.35),
            "outside": ("reveal", "OUTSIDE", 0.25), "twenty": ("reveal", "TWENTY", 0.6), "basket": ("reveal", "BASKET", 0.9),
            "s1": ("stat", "SEVENTY", 0.05), "s2": ("stat", "THOUSAND", 0.35), "s3": ("stat", "FOURTEEN", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_mom": ("tag", "MOM", 0.15), "t_clean": ("tag", "CLEANING", 0.55), "t_win": ("tag", "WINDOWS", 0.8)})
        T["nocol1"] = T["columns"] + 0.2
        T["net1"] = max(T["net"], T["thousands"]) + 0.25
        T["big1"] = max(T["parts"], s("break2") + 0.3) + 0.2
        T["same1"] = max(T["same"], T["short"]) + 0.25
        T["flat1"] = max(T["bend"], T["flat"]) + 0.2
        T["robot1"] = max(T["robot"], T["curved"]) + 0.2
        T["sq1"] = max(T["letters"], s("break4") + 0.3) + 0.2
        T["jet1"] = max(T["ten"], T["water"]) + 0.2
        # ---- sets
        self.cut(s("fix1") - 0.12, "grow", 1)
        self.cut(s("break2") - 0.12, "street", -1)
        self.cut(s("break3") - 0.12, "panel", 1)
        self.cut(s("break4") - 0.12, "glass", -1)
        self.cut(s("reveal") - 0.12, "ring", 1)
        self.cut(s("tag") - 0.2, "mom", -1)
        # ---- camera (ring set)
        FULL = (0, 210, 1.08)
        cm = Camera(-150, -120, 2.6)
        cm.key(0.05, -110, -110, 2.4, max(0.4, T["ring"] - 0.1))
        cm.key(max(0.5, T["ring"] - 0.05), *FULL, max(0.8, abs(T["windows"] - T["ring"]) + 0.6))
        cm.key(s("break1") - 0.12, 0, 190, 1.12, 0.6)
        cm.key(s("reveal") - 0.12, 0, 190, 1.12, 0.0)
        cm.key(s("stat") - 0.12, 0, 60, 0.95, 0.6)
        cm.key(s("closer") - 0.12, 0, 190, 1.15, 1.4)
        self.cam = cm
        self.spans = [(T["nocol1"], T["net1"]), (T["big1"], T["same1"]), (T["flat1"], T["robot1"]), (T["sq1"], T["jet1"])]
        self.shakes = [(T["ring"], 0.3, 5), (T["nocol1"], 0.35, 6), (T["big1"], 0.4, 9), (T["flat1"], 0.35, 6),
                       (T["sq1"], 0.3, 6), (s("closer") + 0.2, 0.35, 8), (T["t_win"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: ring
    def draw_ring(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        ph = self.phase(t)
        night = {"hook": 0.35, "break1": 0.5, "reveal": 0.6, "stat": 1.0, "closer": 1.0}.get(ph, 0.6)
        if ph == "stat":
            night = lerp(0.6, 1.0, prog(t, s("stat"), s("stat") + 0.8))
        sky_bg(c, t, night, cam[0])
        self.view(c, cam)
        glow, xray, floors, net = 0.85, 0.0, 0.0, 0.0
        if ph == "hook":
            glow = 0.85
        elif ph == "break1":
            xray = prog(t, s("break1"), T["columns"] + 0.3)
            floors = xray
        elif ph == "reveal":
            xray = 1.0 - 0.0 * t
            floors = 1.0 - prog(t, T["twenty"], T["twenty"] + 0.5) * 0.6
            net = prog(t, T["outside"], T["outside"] + 0.5)
            glow = 0.2
        elif ph in ("stat", "closer"):
            glow = 1.0
        ring(c, t, glow=glow, xray=xray, floors=floors, net=net, dark=night * 0.6)
        if ph == "break1":                                # a few tiny visitors on the empty floors
            k = prog(t, T["columns"], T["columns"] + 0.4)
            for i, (px, fl) in enumerate(((-300, 4), (-200, 5), (180, 5), (300, 4), (-60, 6))):
                y = -OB + 50 + fl * (2 * OB - 70) / 7
                person(c, px, y, 34, SHIRTS[i % len(SHIRTS)], t + i, pose="look", face=1 if px < 0 else -1, a=k)
        hill(c, t)
        c.restore()
        self.ui["cam"] = cam

    def ui_ring(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "words", T["windows"] - 0.1, s("break1") + 0.1, accent=GLOW, size=48)
            return
        if ph == "break1":
            self.chip(540, 300, "nocol", T["columns"] - 0.1, T["holding"] - 0.3, accent=WARN, size=52)
            self.chip(540, 300, "hold", T["holding"] - 0.3, s("fix1") - 0.15, accent=HILITE, size=48)
            self.badge("alert", T["nocol1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["nocol1"], 1.2)
            return
        if ph == "reveal":
            self.chip(540, 300, "outside", T["outside"] - 0.2, T["twenty"] - 0.15, accent=TEAL, size=46)
            self.chip(540, 300, "beams", T["twenty"] - 0.15, s("stat") - 0.15, accent=HILITE, size=50)
            return
        if ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=48)

    # ------------------------------------------------------------------ set: grow (fix1)
    def draw_grow(self, c, t):
        T, s = self.T, self.tl.s
        blueprint(c)
        cam = (0, 200, 1.05)
        self.view(c, cam)
        c.drawPath(ring_path(), P("#1D4ED8", 0.18))
        c.drawOval(oval(0.0), P("#60A5FA", 0.8, stroke=3))
        c.drawOval(oval(1.0), P("#60A5FA", 0.8, stroke=3))
        settle = e_io(prog(t, T["thousands"] + 0.3, T["net"] + 0.2))
        if settle < 1:
            for k in range(3):
                trial_net(c, t, settle, a=0.5 * (1 - settle) + (0.5 if k == 0 else 0.0), seed=int(t * 6) * 3 + k)
        trial_net(c, t, 1.0, a=settle)
        c.restore()

    def ui_grow(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "tries", T["thousands"] - 0.2, T["net"] - 0.2, accent="#F472B6", size=46)
        self.chip(540, 300, "net", T["net"] - 0.2, s("break2") - 0.15, accent=TEAL, size=50)
        k = self.span(T["computer"], T["net"])
        if k > 0:
            n = int(lerp(1, 4987, prog(tw, T["computer"], T["net"])))
            txt = self.L["try"] + f"{n:,}"
            v2.chip(c, 540, 1160, txt, k, size=40, accent="#F472B6")
        self.badge("check", T["net1"], s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: street (break2, fix2)
    def draw_street(self, c, t):
        T, s = self.T, self.tl.s
        street_bg(c, t)
        if t < s("fix2") - 0.12:                          # the giant beam rolls in and jams under the sign
            x = lerp(-300, 400, e_out(prog(t, s("break2"), T["big1"])))
            truck(c, x, 1128, 1.3, "beam", t)
            sign_bridge(c)
            if t >= T["big1"]:
                v2.debris(c, 560, 600, t, T["big1"], n=12)
        else:                                             # trucks of short tubes pass under it
            for k in range(2):
                x = lerp(-420, 1500, prog(t, s("fix2") + k * 0.9, s("fix2") + k * 0.9 + 3.2))
                truck(c, x, 1128, 1.2, "tubes", t)
            sign_bridge(c)

    def ui_street(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "big", T["parts"] - 0.1, s("fix2") - 0.15, accent=WARN, size=46)
        self.chip(540, 300, "same", T["same"] - 0.2, s("break3") - 0.15, accent=GOOD, size=46)
        self.badge("alert", T["big1"], s("fix2") - 0.2, x=920, y=440)
        self.red(T["big1"], 1.2)
        self.badge("check", T["same1"], s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: panel (break3, fix3)
    def draw_panel(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1F2937", "#0F172A"])
        c.drawRect(R(0, 1080, W, 40), P("#374151"))
        if t < s("fix3") - 0.12:
            saddle_mould(c, 540, 840, 1.45, t, wrinkle=prog(t, T["bend"], T["two"] + 0.3))
        else:
            k = prog(t, s("fix3"), s("break4") - 0.2)
            tipx, tipy = robot_arm(c, 260, 1080, t * 1.4, reach=k)
            add_glow(c, tipx, tipy, 70, "#FDE68A", 0.6)
            sparks_shower(c, tipx, tipy, t, s("fix3") + 0.2, dur=3.0, n=18, speed=380)
            n_done = int(lerp(0, 5, prog(t, T["robot"], s("break4") - 0.3)))
            for i in range(n_done):                       # finished panels stacking up on the right
                curved_panel(c, 860, 1020 - i * 70, 0.55, a=1.0)
            curved_panel(c, 600, 800, 1.2, cut=prog(t, T["curved"], T["curved"] + 0.8))

    def ui_panel(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "flat", T["flat"] - 0.1, T["two"] - 0.15, accent=STEEL_HI, size=48)
        self.chip(540, 300, "two", T["two"] - 0.15, s("fix3") - 0.15, accent=WARN, size=40)
        self.chip(540, 300, "robot", T["robot"] - 0.1, T["curved"] - 0.1, accent="#F97316", size=48)
        self.chip(540, 300, "each", T["curved"] - 0.1, s("break4") - 0.15, accent=GOOD, size=48)
        self.badge("alert", T["flat1"], s("fix3") - 0.2, x=920, y=440)
        self.red(T["flat1"], 1.2)
        self.badge("check", T["robot1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: glass (break4, fix4, cta)
    def draw_glass(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#334155", "#1E293B"])
        c.drawRRect(rr(140, 420, 800, 460, 40), lin_paint(140, 420, 940, 880, [STEEL_HI, STEEL_MID, STEEL_DK]))   # a big panel
        letter_hole(c, 540, 650, 1.3)
        if t < s("fix4") - 0.12:                          # a square pane bumps against the letter and bounces off
            k = prog(t, s("break4"), T["sq1"])
            bx = 540 + 30 * math.sin(t * 18) * bump(t, T["sq1"] - 0.2, T["sq1"] + 0.6)
            by = lerp(1500, 650, e_out(k))
            c.drawRect(R(bx - 170, by - 170, 340, 340), P("#7DD3FC", 0.55))
            c.drawRect(R(bx - 170, by - 170, 340, 340), P("#E0F2FE", 0.9, stroke=6))
        else:                                             # a water jet cuts the letter from a sheet; it drops in
            cut = prog(t, T["water"], T["glass"] + 0.3)
            sx, sy = 540, 1040
            c.drawRect(R(sx - 330, sy - 150, 660, 300), P("#7DD3FC", 0.4))
            ltr = skia.Path()
            ltr.moveTo(-160, 30)
            ltr.cubicTo(-100, 110, 60, 110, 130, 20)
            ltr.lineTo(150, -120)
            meas = skia.PathMeasure(ltr, False)
            L_ = meas.getLength()
            pos, _tan = meas.getPosTan(L_ * cut)
            px, py = pos.x(), pos.y()
            seg = skia.Path()
            meas.getSegment(0, L_ * cut, seg, True)
            c.save()
            c.translate(sx, sy)
            c.scale(1.0, 1.0)
            c.drawPath(seg, P("#FFFFFF", 0.9, stroke=6))
            c.restore()
            jx, jy = sx + px, sy + py
            c.drawRRect(rr(jx - 26, jy - 260, 52, 200, 14), P("#94A3B8"))                 # the nozzle
            c.drawLine(jx, jy - 60, jx, jy, P("#BAE6FD", 0.95, stroke=8))
            splash(c, jx, jy, t, math.floor(t / 0.6) * 0.6, dur=0.6, n=8, speed=220)
            drop = prog(t, T["glass"] + 0.4, T["glass"] + 1.1)
            if drop > 0:
                letter_glass(c, 540, lerp(1040, 650, e_io(drop)), lerp(1.0, 1.3, drop), shine=drop)

    def ui_glass(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "letters", T["letters"] - 0.1, T["square"] - 0.15, accent=GLOW, size=48)
        self.chip(540, 300, "square", T["square"] - 0.15, s("fix4") - 0.15, accent=WARN, size=48)
        self.chip(540, 300, "jet", T["water"] - 0.1, T["ten"] - 0.15, accent="#7DD3FC", size=48)
        self.chip(540, 300, "pieces", T["ten"] - 0.15, s("cta") - 0.15, accent=GOOD, size=44)
        self.badge("alert", T["sq1"], s("fix4") - 0.2, x=920, y=440)
        self.red(T["sq1"], 1.2)
        self.badge("check", T["jet1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: mom (tag)
    def draw_mom(self, c, t):
        T = self.T
        cam = (0, 330, 0.8)
        sky_bg(c, t, 0.2, 0)
        self.view(c, cam)
        ring(c, t, glow=0.3, dark=0.1)
        sp = bump(t, T["t_win"] - 0.1, T["t_win"] + 1.6)          # every pane sparkles at once
        if sp > 0:
            rng = random.Random(4)
            for k in range(26):
                u, s_ = rng.uniform(0, 6.28), rng.uniform(0.2, 0.8)
                x, y = rp(u, s_)
                add_glow(c, x, y, 26, "#FFFFFF", 0.8 * sp * (0.5 + 0.5 * math.sin(t * 9 + k)))
        gx, gy = rp(-1.2, 1.0)                                    # a cleaner's cradle on ropes
        drop = 60 + 90 * math.sin(t * 1.3)
        c.drawLine(gx - 30, gy - 40, gx - 30, gy + drop, P("#E5E7EB", 0.8, stroke=3))
        c.drawLine(gx + 30, gy - 40, gx + 30, gy + drop, P("#E5E7EB", 0.8, stroke=3))
        c.drawRect(R(gx - 44, gy + drop, 88, 22), P("#F59E0B"))
        hill(c, t)
        c.restore()
        mx, my = 330, 1225                                        # mom, big in front, with her spray bottle
        person(c, mx, my, 380, "#DB2777", t, pose="point" if t > T["t_clean"] else "look", face=1, hair="#3B2416")
        c.drawRRect(rr(mx + 70, my - 270, 52, 88, 12), P("#38BDF8"))
        c.drawRRect(rr(mx + 80, my - 300, 32, 32, 8), P("#F8FAFC"))
        if t > T["t_clean"]:
            for k in range(8):
                u = (t * 2.5 + k / 8) % 1.0
                c.drawCircle(mx + 130 + u * 160, my - 300 - u * 60 + math.sin(k) * 20, 6 * (1 - u) + 2, P("#BAE6FD", 0.8 * (1 - u)))

    def ui_mom(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "who", T["t_clean"] - 0.2, self.duration + 1, accent=WARN, size=50)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, NIGHTP)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["ring"], sfx.riser(1.0, 62), -12), (T["windows"], sfx.sparkle(1.2, 14, 63), -8),
              (T["writing"] + 0.2, sfx.chime(), -9)]
        ev += [(T["columns"], sfx.whoosh(0.8, True, 64), -14), (T["nocol1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, True, 65), -6), (T["thousands"], sfx.whirr(1.6, 180.0, 420.0, 66), -16),
               (T["net1"], sfx.ding(), -8), (T["net1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, False, 67), -6), (T["big1"], sfx.clank(300.0, 0.8, 68), -4),
               (T["big1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["same"], sfx.hum(1.4, 90.0), -16), (T["same1"], sfx.ding(), -8), (T["same1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 69), -6), (T["bend"], sfx.creak(1.0, 70), -8),
               (T["flat1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["robot"], sfx.whirr(1.8, 150.0, 260.0, 71), -12), (T["robot1"], sfx.ding(), -8), (T["robot1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 72), -6), (T["sq1"], sfx.thunk(73), -4),
               (T["sq1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["water"], sfx.hiss(1.8, 74), -12), (T["jet1"], sfx.ding(), -8), (T["jet1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["outside"], sfx.charge_up(0.8), -10),
               (T["twenty"], sfx.sparkle(1.0, 12, 95), -9)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, False, 96), -6), (T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3),
               (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"], sfx.pop(100), -2), (T["cong2"], sfx.sparkle(1.4, 18, 101), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 102), -6), (T["t_clean"], sfx.hiss(0.4, 103), -10),
               (T["t_win"], sfx.sparkle(1.2, 16, 104), -6), (T["t_win"] + 0.5, sfx.womp(), -8)]
        return ev


NAME = "museum"
EPISODE = Museum
