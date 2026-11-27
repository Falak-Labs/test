"""Episode 104 - Tokyo's G-Cans flood tunnel (the Metropolitan Area Outer Underground Discharge Channel).  v2 look.

Sets: hall (hook: the pressure-control tank seen in one-point perspective, a forest of giant concrete pillars with light
falling from the ceiling openings and tiny people at their feet; the camera starts close on a person by a pillar and
pulls out; cta, stat; closer with the hall lit for the cover), town (break1: a typhoon over a low town, rain, the river
over its banks and the water climbing up the houses), section (fix1: a cut through the ground, a river spilling into a
giant shaft; break2: the shaft full in minutes; fix2: five shafts joined by a tunnel 50 m down; break3: a surge racing
down the tunnel and slamming the end; fix3: it spreads into the pillar tank and calms; break4: the tank 50 m under the
Edo River, an arrow that cannot climb; fix4: four pumps with jet-engine turbines push it up into the river), pool
(reveal: a 25 m swimming pool emptying in about a second, again and again, with a stopwatch), tag (English: one noodle
clogs the kitchen sink; Arabic: ten minutes of rain and the street is a swimming pool).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

CONC = ("#9AA3AE", "#6B7480", "#3E4650")
WATER = "#2F80C8"
WATER_L = "#7CC4F5"
HZ, F = 880.0, 700.0                                   # horizon y and focal length of the hall
SURF = 470                                             # ground surface y in the section
TUN_Y = 900                                            # tunnel centre y (50 m down)
SHAFTS = (120, 290, 460, 630, 740)
TANK = (780, 850, 1060, 1030)                          # x0, y0, x1, y1 of the pillar tank in the section


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== the hall
def hall(c, t, lit=0.0, water=0.0, people=True, beams=1.0):
    """The pillar hall in one-point perspective: eye 2 m above the floor, the ceiling 16 m above the eye."""
    vrect(c, 0, 0, W, H, ["#0A1018", "#121B26", "#0B1219"], [0, 0.4, 1])
    def pr(X, Y, Z):
        return 540 + X * F / Z, HZ + Y * F / Z
    # floor and ceiling bands
    fl = skia.Path()
    fl.moveTo(0, H)
    fl.lineTo(0, HZ + 2 * F / 160)
    fl.lineTo(W, HZ + 2 * F / 160)
    fl.lineTo(W, H)
    fl.close()
    c.drawPath(fl, lin_paint(0, HZ, 0, H, ["#1C2631", "#2B3846", "#1A232E"]))
    c.drawRect(R(0, 0, W, HZ - 16 * F / 160), P("#0B1118"))
    for k in range(1, 14):                              # floor joints running to the vanishing point
        X = (k - 7) * 6.0
        x0, y0 = pr(X, 2, 4)
        x1, y1 = pr(X, 2, 160)
        c.drawLine(x0, y0, x1, y1, P("#3B4A5A", 0.5, stroke=2))
    if water > 0:                                       # a sheet of water on the floor
        c.drawRect(R(0, HZ + 8, W, H - HZ), P(WATER, 0.35 * water))
    pillars = []
    for Z in (14, 32, 50, 68, 86, 104, 122, 140):
        for X in (-24, -8, 8, 24):
            pillars.append((Z, X))
    pillars.sort(key=lambda p: -p[0])
    for Z, X in pillars:
        depth_k = clamp((Z - 14) / 130)
        col = mix(mix("#8E99A6", "#C3CCD6", lit * 0.6), "#1A2430", depth_k * 0.7)
        sx0, top = pr(X - 1.0, -16, Z)
        sx1, bot = pr(X + 1.0, 2, Z)
        side = X - 0.0
        # the side face that shows (towards the middle)
        bx0, btop = pr(X - 1.0 if X > 0 else X + 1.0, -16, Z + 7)
        _, bbot = pr(X - 1.0 if X > 0 else X + 1.0, 2, Z + 7)
        sp = skia.Path()
        ex = sx0 if X > 0 else sx1
        sp.moveTo(ex, top)
        sp.lineTo(bx0, btop)
        sp.lineTo(bx0, bbot)
        sp.lineTo(ex, bot)
        sp.close()
        c.drawPath(sp, P(shade(col, -0.25)))
        c.drawRect(R(sx0, top, sx1 - sx0, bot - top), lin_paint(sx0, 0, sx1, 0, [shade(col, 0.12), col, shade(col, -0.12)]))
        if water > 0:                                    # its reflection in the wet floor
            c.drawRect(R(sx0, bot, sx1 - sx0, (bot - top) * 0.25), P(col, 0.25 * water))
        del side
    if beams > 0:                                       # light falling from the openings in the ceiling
        for X, Z in ((0, 40), (-16, 76), (16, 110)):
            x0, y0 = pr(X, -16, Z)
            x1, y1 = pr(X, 2, Z)
            w0 = 4 * F / Z
            beam = skia.Path()
            beam.moveTo(x0 - w0, 0)
            beam.lineTo(x0 + w0, 0)
            beam.lineTo(x1 + w0 * 1.8, y1)
            beam.lineTo(x1 - w0 * 1.8, y1)
            beam.close()
            c.drawPath(beam, lin_paint(0, 0, 0, y1, [("#FFF1C9", 0.0), ("#FFF1C9", 0.32 * beams), ("#FFF1C9", 0.16 * beams)]))
            add_glow(c, x1, y1, 120 * 14 / Z * 2, "#FFE9B0", 0.5 * beams)
    if people:                                          # tiny people for scale
        for X, Z, col in ((-5.5, 22, "#F97316"), (-4.4, 22, "#FACC15"), (5.0, 40, "#22C55E"), (-2.0, 60, "#38BDF8")):
            x, y = pr(X, 2, Z)
            person(c, x, y, 1.75 * F / Z, col, t, pose="look", face=1 if X < 0 else -1, hat="hard", band=True)
    if lit > 0:
        add_glow(c, 540, HZ - 200, 700, "#FDE68A", 0.18 * lit)


# ====================================================================================== the town
def town(c, t, flood=0.0, storm=1.0):
    """A low town in a typhoon: dark sky, rain, houses, a river in front whose water climbs the streets."""
    vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B", "#334155"])
    if storm > 0 and (int(t * 3.1) % 7 == 0):
        c.drawRect(R(0, 0, W, H), P("#E0F2FE", 0.18 * storm))
    for k, (cx, cy, s) in enumerate(((200, 260, 1.4), (700, 220, 1.6), (980, 340, 1.1))):
        v2.cloud(c, cx + math.sin(t * 0.5 + k) * 30, cy, s, body="#1F2937", rim="#475569", a=0.9, seed=k)
    base = 980
    rng = random.Random(4)
    for k in range(9):                                  # houses
        x = 40 + k * 120 + rng.uniform(-10, 10)
        h = rng.uniform(150, 230)
        col = rng.choice(["#CBD5E1", "#E2E8F0", "#94A3B8", "#FDE68A"])
        c.drawRect(R(x, base - h, 100, h), P(col))
        roof = skia.Path()
        roof.moveTo(x - 12, base - h)
        roof.lineTo(x + 50, base - h - 60)
        roof.lineTo(x + 112, base - h)
        roof.close()
        c.drawPath(roof, P(rng.choice(["#7F1D1D", "#1E3A8A", "#374151"])))
        for j in range(2):
            c.drawRect(R(x + 18 + j * 40, base - h + 40, 24, 30), P("#FDE68A", 0.8))
    c.drawRect(R(0, base, W, 260), P("#3F3F46"))
    lvl = lerp(1180, 860, smooth(flood))               # the water climbing
    c.drawRect(R(0, lvl, W, H - lvl), lin_paint(0, lvl, 0, H, ["#4B6A86", "#2B4258"]))
    for k in range(14):
        xx = (k * 90 + t * 120) % (W + 100) - 50
        c.drawLine(xx, lvl + 6, xx + 50, lvl + 6, P("#BFDBFE", 0.5, stroke=3))
    rng = random.Random(9)
    for k in range(140):                                # rain
        x = (rng.uniform(0, W + 300) - t * 400 * rng.uniform(0.8, 1.2)) % (W + 300) - 150
        y = (rng.uniform(0, H) + t * 1600 * rng.uniform(0.8, 1.2)) % 1300
        c.drawLine(x, y, x - 18, y + 46, P("#BFDBFE", 0.45 * storm, stroke=2))


# ====================================================================================== the section
def ground(c, x0=0, x1=W):
    vrect(c, x0, 0, x1 - x0, SURF, ["#1E3A5F", "#3B82C4", "#93C5FD"], [0, 0.6, 1])
    vrect(c, x0, SURF, x1 - x0, H - SURF, ["#7A5A3A", "#5B4129", "#3B2A1C", "#2A1E14"], [0, 0.3, 0.7, 1])
    for k in range(6):                                  # soil layers
        y = SURF + 90 + k * 120
        c.drawLine(x0, y, x1, y + 10, P("#2A1E14", 0.35, stroke=3))


def shaft(c, x, fill, t, spill=0.0, w=86, bottom=1100):
    """A giant concrete shaft from the surface down to `bottom`, water inside up to `fill` (0..1)."""
    c.drawRect(R(x - w / 2 - 12, SURF, w + 24, bottom - SURF + 12), P(CONC[2]))
    c.drawRect(R(x - w / 2, SURF, w, bottom - SURF), P("#0B1220"))
    if fill > 0:
        lvl = lerp(bottom, SURF, clamp(fill))
        c.drawRect(R(x - w / 2, lvl, w, bottom - lvl), lin_paint(0, lvl, 0, bottom, [WATER_L, WATER]))
        c.drawLine(x - w / 2, lvl, x + w / 2, lvl, P("#DBEAFE", 0.8, stroke=3))
    if spill > 0:                                       # the river pouring over the rim
        rng = random.Random(int(x))
        for k in range(16):
            u = (t * 1.6 + rng.random()) % 1.0
            yy = lerp(SURF - 6, lerp(bottom, SURF, clamp(fill)) - 6, u)
            xx = x - w / 2 + 8 + rng.uniform(0, 14)
            c.drawLine(xx, yy, xx + 4, yy + 40, P(WATER_L, 0.8 * spill * (1 - u * 0.4), stroke=6))


def river_top(c, x0, x1, t, a=1.0, hi=0.0):
    """A small river at the surface (a blue band), hi lifts it over its banks."""
    if a <= 0:
        return
    c.drawRect(R(x0, SURF - 26 - 20 * hi, x1 - x0, 30 + 20 * hi), P(WATER, a))
    for k in range(4):
        xx = x0 + ((k * 40 + t * 60) % max(1.0, x1 - x0))
        c.drawLine(xx, SURF - 14, xx + 18, SURF - 14, P("#DBEAFE", 0.6 * a, stroke=3))


def tunnel(c, x0, x1, flow, t, surge=None, a=1.0):
    """The horizontal tunnel at TUN_Y from x0 to x1; flow 0..1 fills it; surge = x of a racing water front."""
    c.drawRRect(rr(x0, TUN_Y - 40, x1 - x0, 80, 40), P(CONC[2], a))
    c.drawRRect(rr(x0 + 8, TUN_Y - 32, x1 - x0 - 16, 64, 32), P("#0B1220", a))
    if flow > 0:
        xe = x0 + 8 + (x1 - x0 - 16) * clamp(flow) if surge is None else surge
        c.drawRRect(rr(x0 + 8, TUN_Y - 22, max(0.0, xe - x0 - 8), 54, 26), lin_paint(0, TUN_Y - 22, 0, TUN_Y + 32,
                                                                                   [WATER_L, WATER], a=a))
        for k in range(10):
            xx = x0 + 20 + ((k * 70 + t * 260) % max(1.0, xe - x0 - 40))
            c.drawLine(xx, TUN_Y, xx + 26, TUN_Y, P("#DBEAFE", 0.6 * a, stroke=3))
        if surge is not None:                            # the white front of the surge
            add_glow(c, xe, TUN_Y + 4, 60, "#FFFFFF", 0.6 * a)
            c.drawCircle(xe, TUN_Y + 4, 26, P("#E0F2FE", 0.9 * a))


def tank(c, t, level=0.0, calm=1.0, a=1.0):
    """The pillar tank in section, water up to `level` (0..1); calm 0 = choppy."""
    x0, y0, x1, y1 = TANK
    c.drawRect(R(x0 - 14, y0 - 14, x1 - x0 + 28, y1 - y0 + 28), P(CONC[2], a))
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#0B1220", a))
    if level > 0:
        lvl = lerp(y1, y0 + 20, clamp(level))
        p = skia.Path()
        p.moveTo(x0, y1)
        for k in range(31):
            xx = lerp(x0, x1, k / 30)
            p.lineTo(xx, lvl + math.sin(t * 9 + k * 0.9) * 16 * (1 - calm))
        p.lineTo(x1, y1)
        p.close()
        c.drawPath(p, lin_paint(0, lvl, 0, y1, [WATER_L, WATER], a=a))
    for k in range(6):                                  # the pillars
        px = x0 + 22 + k * ((x1 - x0 - 44) / 5)
        c.drawRect(R(px - 9, y0, 18, y1 - y0), P(CONC[0], 0.95 * a))


def pump_house(c, t, on=0.0, lift=0.0, a=1.0):
    """Four pumps beside the tank driven by jet-engine turbines, a pipe up to the Edo River at the surface."""
    if a <= 0:
        return
    c.drawRRect(rr(770, 600, 300, 230, 20), P("#1E293B", 0.9 * a))
    for k in range(4):
        px = 812 + (k % 2) * 140 + (k // 2) * 70
        py = 660 + (k // 2) * 110
        c.drawRRect(rr(px - 50, py - 45, 100, 90, 18), lin_paint(px - 50, 0, px + 50, 0, ["#64748B", "#CBD5E1", "#475569"], a=a))
        c.drawCircle(px, py, 34, P("#0F172A", a))
        c.save()                                          # the jet-engine turbine spinning
        c.translate(px, py)
        c.rotate(t * 900 * on)
        for j in range(8):
            c.rotate(45)
            c.drawLine(0, 0, 0, -30, P("#E2E8F0", a, stroke=7))
        c.restore()
        if on > 0:
            add_glow(c, px, py, 70, "#FB923C", 0.6 * on * a)
    c.drawRect(R(996, SURF - 10, 56, 600 - SURF + 10), P(CONC[2], a))          # the riser pipe
    if lift > 0:
        top = lerp(600, SURF - 10, clamp(lift))
        c.drawRect(R(1004, top, 40, 600 - top), P(WATER_L, a))
        if lift >= 1:
            rng = random.Random(3)
            for k in range(14):
                u = (t * 2 + rng.random()) % 1.0
                c.drawLine(1020, SURF - 20, 1020 - u * 80, SURF - 20 - math.sin(u * math.pi) * 70,
                           P(WATER_L, (1 - u) * a, stroke=7))


def edo_river(c, t, a=1.0, rise=0.0):
    """The big Edo River at the surface on the right."""
    c.drawRect(R(880, SURF - 46 - 10 * rise, 200, 56 + 10 * rise), P("#1D4ED8", a))
    for k in range(5):
        xx = 880 + ((k * 50 + t * 80) % 200)
        c.drawLine(xx, SURF - 30, xx + 24, SURF - 30, P("#DBEAFE", 0.6 * a, stroke=3))


def ruler(c, x, y0, y1, a=1.0):
    """A depth ruler with ticks."""
    if a <= 0:
        return
    c.drawLine(x, y0, x, y1, P("#F8FAFC", a, stroke=4))
    for k in range(6):
        yy = lerp(y0, y1, k / 5)
        c.drawLine(x - 12, yy, x + 12, yy, P("#F8FAFC", a, stroke=4))


def stopwatch(c, x, y, r, frac, a=1.0):
    """A stopwatch whose hand has gone round `frac` of a turn."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#F8FAFC", a))
    c.drawCircle(x, y, r, P("#0F172A", a, stroke=8))
    c.drawRRect(rr(x - 16, y - r - 30, 32, 26, 6), P("#0F172A", a))
    arc = skia.Path()
    arc.addArc(R(x - r * 0.8, y - r * 0.8, r * 1.6, r * 1.6), -90, 360 * clamp(frac))
    c.drawPath(arc, P("#EF4444", 0.85 * a, stroke=r * 0.2))
    ang = -math.pi / 2 + math.tau * frac
    c.drawLine(x, y, x + math.cos(ang) * r * 0.8, y + math.sin(ang) * r * 0.8, P("#0F172A", a, stroke=8))
    c.drawCircle(x, y, 10, P("#0F172A", a))


def pool(c, x0, y0, x1, y1, level, t, a=1.0):
    """A swimming pool seen from above: tiles, lane ropes, water down to `level` (0..1)."""
    c.drawRRect(rr(x0 - 30, y0 - 30, x1 - x0 + 60, y1 - y0 + 60, 20), P("#E5E7EB", a))
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#BAE6FD", a))
    for k in range(1, 12):                              # tiles
        yy = lerp(y0, y1, k / 12)
        c.drawLine(x0, yy, x1, yy, P("#7DD3FC", 0.5 * a, stroke=2))
    if level > 0:
        c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P("#0EA5E9", 0.85 * level * a))
        for k in range(8):
            xx = x0 + ((k * 60 + t * 40) % (x1 - x0))
            c.drawLine(xx, y0 + 20 + (k % 4) * 140, xx + 30, y0 + 20 + (k % 4) * 140, P("#FFFFFF", 0.4 * level * a, stroke=3))
    for k in range(1, 6):                               # lane lines on the floor and ropes
        xx = lerp(x0, x1, k / 6)
        c.drawLine(xx, y0 + 30, xx, y1 - 30, P("#1E3A8A", 0.6 * a, stroke=8))
    if level > 0.3:
        for k in range(1, 6):
            xx = lerp(x0, x1, (k - 0.5) / 6 + 1 / 12)
            for j in range(20):
                c.drawCircle(xx, lerp(y0, y1, j / 19), 6, P("#EF4444" if j % 4 < 2 else "#F8FAFC", a * level))


class GCans(EpisodeV2):
    BUILD_NO = 104
    FIRST_SET = "hall"
    CLEAR = "#0A1018"
    TITLE = {"en": "TOKYO'S FLOOD TUNNEL", "ar_sa": "نفق طوكيو"}
    EMPH = {"en": ["JAPAN", "GIANT", "HALL", "PILLARS", "UNDERGROUND", "FLOODS", "TYPHOONS", "FLOOD", "TOKYO",
                   "FAST", "EMPTY", "FIVE", "WELLS", "RIVERS", "OVERFLOW", "FILL", "TIME", "TUNNEL", "SIX",
                   "KILOMETERS", "FIFTY", "METERS", "RACES", "SLAMS", "TRAIN", "TANK", "CALM", "FIFTY-NINE", "CLIMB",
                   "ITSELF", "FOUR", "PUMPS", "JET", "ENGINES", "EDO", "RIVER", "FOLLOW", "BROOKLYN", "ELEPHANTS",
                   "SWIMMING", "POOL", "SECOND", "CONGRATS", "YOURSELF", "SWALLOWS", "SINK", "NOODLE"],
            "ar_sa": ["اليابان", "قاعة", "أعمدة", "الأرض", "للفيضانات", "الأعاصير", "تغرّق", "طوكيو", "سرعة",
                      "تطلّع", "خمس", "آبار", "فاضت", "تمتلي", "بدقايق", "بنفق", "ست", "خمسين", "تنطلق", "وتضرب",
                      "القطار", "خزان", "تهدى", "وخمسين", "عمود", "لحالها", "مضخات", "طيارات", "لنهر", "متابعة",
                      "بروكلين", "فيلة", "مسبح", "ثانية", "مبروك", "يبلع", "تمطر", "الشارع"]}
    KEYS = {"ar_sa": {
        ("hook", "JAPAN"): "اليابان", ("hook", "PILLARS"): "أعمدة", ("hook", "FLOODS"): "فيضانات",
        ("break1", "TYPHOONS"): "الأعاصير", ("break1", "FLOOD"): "تغرق", ("break1", "EMPTY"): "تطلع",
        ("fix1", "FIVE"): "خمس", ("fix1", "WELLS"): "آبار", ("fix1", "OVERFLOW"): "فاضت",
        ("break2", "FILL"): "تمتلي", ("break2", "TIME"): "بدقايق", ("break2", "WHAT"): "وبعدين",
        ("fix2", "TUNNEL"): "بنفق", ("fix2", "SIX"): "ست", ("fix2", "FIFTY"): "خمسين",
        ("break3", "RACES"): "تنطلق", ("break3", "SLAMS"): "وتضرب", ("break3", "TRAIN"): "القطار",
        ("fix3", "TANK"): "خزان", ("fix3", "CALM"): "تهدى", ("fix3", "PILLARS"): "عمود",
        ("break4", "FIFTY"): "خمسين", ("break4", "CLIMB"): "تطلع", ("break4", "ITSELF"): "لحالها",
        ("fix4", "PUMPS"): "مضخات", ("fix4", "JET"): "طيارات", ("fix4", "EDO"): "لنهر",
        ("cta", "FOLLOW"): "متابعة", ("cta", "BROOKLYN"): "بروكلين",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "POOL"): "مسبح", ("reveal", "SECOND"): "ثانية",
        ("stat", "SIX"): "ست", ("stat", "FIFTY"): "وخمسين", ("stat", "FOUR"): "وأربع",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SWALLOWS"): "يبلع", ("tag", "SINK"): "تمطر", ("tag", "NOODLE"): "مسبح"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Brooklyn Bridge"),
                   "stat": [("6.3 km", "OF TUNNEL"), ("59", "PILLARS"), ("4", "JET-ENGINE PUMPS")],
                   "L": {"hall": "A HALL OF PILLARS... FOR FLOODS", "deep": "UNDERGROUND", "typhoon": "TYPHOON!",
                         "fast": "HOW FAST CAN IT EMPTY?", "wells": "5 GIANT WELLS", "catch": "THEY CATCH THE RIVERS",
                         "full": "FULL IN MINUTES!", "what": "THEN WHAT?", "tunnel": "A TUNNEL JOINS THEM",
                         "km": "6 KM LONG, 50 M DOWN", "train": "IT SLAMS LIKE A TRAIN!", "races": "THE WATER RACES",
                         "tank": "A GIANT TANK", "calm": "IT CALMS DOWN", "climb": "WATER WON'T CLIMB!",
                         "down": "50 M DOWN", "pumps": "4 PUMPS", "jet": "SPUN BY JET ENGINES", "edo": "EDO RIVER",
                         "pool": "A SWIMMING POOL", "second": "EVERY SECOND!", "name": "G-CANS FLOOD TUNNEL",
                         "noodle": "1 NOODLE", "clog": "CLOGGED!", "m70": "70 M", "m50": "50 M"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: جسر بروكلين"),
                      "stat": [("6.3", "كيلو نفق"), ("59", "عمود"), ("4", "مضخات بمحركات طيارات")],
                      "L": {"hall": "قاعة أعمدة... للفيضانات", "deep": "تحت الأرض", "typhoon": "إعصار!",
                            "fast": "بأي سرعة تطلّع الموية؟", "wells": "خمس آبار عملاقة", "catch": "تمسك الأنهار",
                            "full": "تمتلي بدقايق!", "what": "وبعدين؟", "tunnel": "نفق يوصلها",
                            "km": "ست كيلو... خمسين متر تحت", "train": "تضرب مثل القطار!", "races": "الموية تنطلق",
                            "tank": "خزان عملاق", "calm": "تهدى فيه", "climb": "ما تطلع لحالها!",
                            "down": "خمسين متر تحت", "pumps": "أربع مضخات", "jet": "بمحركات طيارات", "edo": "نهر إيدو",
                            "pool": "مسبح كامل", "second": "كل ثانية!", "name": "نفق طوكيو للفيضانات",
                            "noodle": "عشر دقايق مطر", "clog": "صار مسبح!", "m70": "70 M", "m50": "50 M"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "japan": ("hook", "JAPAN", 0.15), "pillars": ("hook", "PILLARS", 0.5), "flood0": ("hook", "FLOODS", 0.9),
            "typhoons": ("break1", "TYPHOONS", 0.05), "flood1": ("break1", "FLOOD", 0.2), "empty": ("break1", "EMPTY", 0.9),
            "five": ("fix1", "FIVE", 0.2), "wells": ("fix1", "WELLS", 0.4), "overflow": ("fix1", "OVERFLOW", 0.9),
            "fill": ("break2", "FILL", 0.4), "time": ("break2", "TIME", 0.7), "what": ("break2", "WHAT", 0.9),
            "tunnel": ("fix2", "TUNNEL", 0.15), "six": ("fix2", "SIX", 0.45), "fifty": ("fix2", "FIFTY", 0.8),
            "races": ("break3", "RACES", 0.3), "slams": ("break3", "SLAMS", 0.6), "train": ("break3", "TRAIN", 0.9),
            "tank": ("fix3", "TANK", 0.35), "calm": ("fix3", "CALM", 0.6), "pillars3": ("fix3", "PILLARS", 0.9),
            "down4": ("break4", "FIFTY", 0.3), "climb": ("break4", "CLIMB", 0.7), "itself": ("break4", "ITSELF", 0.9),
            "pumps": ("fix4", "PUMPS", 0.2), "jet": ("fix4", "JET", 0.45), "edo": ("fix4", "EDO", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "answer": ("reveal", "ANSWER", 0.05), "pool": ("reveal", "POOL", 0.4), "second": ("reveal", "SECOND", 0.9),
            "s1": ("stat", "SIX", 0.05), "s2": ("stat", "FIFTY", 0.4), "s3": ("stat", "FOUR", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_swallow": ("tag", "SWALLOWS", 0.15), "t_sink": ("tag", "SINK", 0.6), "t_noodle": ("tag", "NOODLE", 0.9)})
        T["flood1b"] = max(T["flood1"], T["typhoons"] + 0.3)
        T["catch1"] = max(T["overflow"], T["wells"] + 0.3)
        T["full1"] = max(T["fill"], s("break2") + 0.3)
        T["km1"] = max(T["fifty"], T["six"] + 0.3)
        T["slam1"] = max(T["slams"], T["races"] + 0.4)
        T["calm1"] = max(T["calm"], T["tank"] + 0.3)
        T["climb1"] = max(T["climb"], T["down4"] + 0.3)
        T["edo1"] = max(T["edo"], T["jet"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "town", 1)
        self.cut(s("fix1") - 0.12, "section", -1)
        self.cut(s("cta") - 0.12, "hall", 1)
        self.cut(s("reveal") - 0.12, "pool", -1)
        self.cut(s("stat") - 0.12, "hall", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["flood1b"], T["catch1"]), (T["full1"], T["km1"]), (T["slam1"], T["calm1"]), (T["climb1"], T["edo1"])]
        self.shakes = [(T["pillars"], 0.3, 4), (T["flood1b"], 0.4, 7), (T["full1"], 0.3, 6), (T["slam1"], 0.5, 12),
                       (T["climb1"], 0.3, 5), (T["jet"], 0.4, 5), (s("closer") + 0.2, 0.35, 6), (T["t_noodle"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: hall (hook, cta, stat, closer)
    def draw_hall(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["japan"] - 0.4, T["flood0"]))
            z = lerp(2.4, 1.0, k)
            px, py = lerp(380, 540, k), lerp(1000, HZ, k)
            c.save()
            c.translate(540, HZ)
            c.scale(z, z)
            c.translate(-px, -py)
            hall(c, t, water=0.3)
            c.restore()
        else:
            hall(c, t, lit=1.0 if ph == "closer" else 0.4, water=0.3)

    def ui_hall(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "deep", T["japan"] - 0.1, T["pillars"] - 0.05, accent="#FDE68A", size=54)
            self.chip(540, 300, "hall", T["pillars"] - 0.05, s("break1") + 0.1, accent=HILITE, size=40)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=48)

    # ------------------------------------------------------------------ set: town (break1)
    def draw_town(self, c, t):
        T, s = self.T, self.tl.s
        town(c, t, flood=prog(t, T["flood1"] - 0.2, T["empty"]))

    def ui_town(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "typhoon", T["typhoons"] - 0.1, T["empty"] - 0.8, accent=WARN, size=60)
        self.chip(540, 300, "fast", T["empty"] - 0.8, s("fix1") - 0.1, accent=HILITE, size=46)
        self.badge("alert", T["flood1b"], s("fix1") - 0.2, x=920, y=440)
        self.red(T["flood1b"], 1.2)

    # ------------------------------------------------------------------ set: section (fix1 .. fix4)
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        order = ("fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4")
        i = order.index(ph) if ph in order else 6
        zk = e_io(prog(t, s("fix2") - 0.1, T["six"])) if i >= 2 else 0.0
        z = lerp(1.75, 1.0, zk)
        cx, cy = lerp(200, 540, zk), lerp(760, 820, zk)
        c.save()
        c.translate(540, 820)
        c.scale(z, z)
        c.translate(-cx, -cy)
        ground(c, -300, W + 300)
        n = 1 if i < 2 else 5
        if i >= 2:
            n = 1 + int(4 * clamp(prog(t, s("fix2"), T["tunnel"] + 0.4) * 1.0001))
        # rivers at the surface and the Edo on the right
        for k in range(n):
            river_top(c, SHAFTS[k] - 90, SHAFTS[k] + 40, t, hi=1.0 if i <= 1 else 0.3)
        edo_river(c, t, a=1.0 if i >= 2 else 0.0)
        # the shafts
        if i == 0:
            f = 0.25 * prog(t, T["wells"], T["overflow"] + 0.6)
        elif i == 1:
            f = lerp(0.25, 1.0, prog(t, s("break2"), T["time"]))
        else:
            f = lerp(1.0, 0.45, prog(t, s("fix2"), T["fifty"] + 0.6)) if i == 2 else 0.4
        for k in range(n):
            shaft(c, SHAFTS[k], f, t, spill=1.0 if (i <= 1 and k == 0) or i >= 2 else 0.0)
        if i == 0:
            ruler(c, SHAFTS[0] + 90, SURF, 1100, a=prog(t, T["five"], T["five"] + 0.3))
        if i >= 2:
            tun = prog(t, T["tunnel"] - 0.2, T["tunnel"] + 0.6)
            surge = None
            flow = prog(t, T["six"], T["fifty"] + 0.4)
            if i == 3:
                surge = lerp(SHAFTS[0], TANK[0] - 6, e_in(prog(t, s("break3"), T["slam1"])))
                flow = 1.0
            tunnel(c, SHAFTS[0], TANK[0] + 10, flow, t, surge=surge, a=tun)
            ruler(c, 70, SURF, TUN_Y, a=prog(t, T["fifty"] - 0.3, T["fifty"]) * (1 if i == 2 else 0))
            lvl = 0.0
            calm = 0.0
            if i == 3:
                lvl = 0.35 * prog(t, T["slam1"], T["slam1"] + 0.4)
                if t >= T["slam1"]:
                    v2.splash if False else None
            elif i >= 4:
                lvl = lerp(0.35, 0.7, prog(t, s("fix3"), T["calm"] + 0.4)) if i == 4 else 0.7
                calm = prog(t, T["calm"] - 0.2, T["calm1"] + 0.4) if i == 4 else 1.0
            tank(c, t, level=lvl, calm=calm, a=prog(t, s("fix2"), T["tunnel"] + 0.6) if i == 2 else 1.0)
            if i == 3 and t >= T["slam1"]:
                splash(c, TANK[0] + 30, TUN_Y, t, T["slam1"], dur=0.9, n=26, speed=520, col=WATER_L, seed=4)
        if i >= 5:
            up = prog(t, T["down4"], T["climb"]) if i == 5 else 0.0
            if i == 5:                                 # the arrow that cannot climb: it rises, stalls and sags back
                sag = prog(t, T["climb"] - 0.1, T["climb"] + 0.5)
                ay0, ay1 = 840, lerp(840, 560, up) + 120 * e_out(sag)
                c.drawLine(930, ay0, 930, ay1, P(WARN, 0.95, stroke=40))
                tri = skia.Path()
                tri.moveTo(930, ay1 - 60)
                tri.lineTo(880, ay1 + 10)
                tri.lineTo(980, ay1 + 10)
                tri.close()
                c.drawPath(tri, P(WARN, 0.95))
                dash = dash_paint("#F8FAFC", 0.8 * up, 6, t)
                c.drawLine(930, ay1 - 70, 960, SURF - 40, dash)
            on = prog(t, T["pumps"] - 0.2, T["jet"]) if i == 6 else 0.0
            pump_house(c, t, on=on, lift=prog(t, T["jet"], T["edo"] + 0.2) if i == 6 else 0.0,
                       a=prog(t, s("fix4") - 0.1, T["pumps"]) if i == 6 else 0.0)
        c.restore()

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix1":
            self.chip(540, 300, "wells", T["five"] - 0.1, T["overflow"] - 0.3, accent="#7DD3FC", size=54)
            self.chip(540, 300, "catch", T["overflow"] - 0.3, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["catch1"], s("break2") - 0.15, x=920, y=440)
        elif ph == "break2":
            self.chip(540, 300, "full", T["fill"] - 0.2, T["what"] - 0.1, accent=WARN, size=54)
            self.chip(540, 300, "what", T["what"] - 0.1, s("fix2") - 0.15, accent=HILITE, size=56)
            self.badge("alert", T["full1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["full1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "tunnel", T["tunnel"] - 0.1, T["six"] - 0.1, accent="#7DD3FC", size=52)
            self.chip(540, 300, "km", T["six"] - 0.1, s("break3") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["km1"], s("break3") - 0.15, x=920, y=440)
        elif ph == "break3":
            self.chip(540, 300, "races", T["races"] - 0.2, T["slams"] - 0.1, accent="#7DD3FC", size=52)
            self.chip(540, 300, "train", T["slams"] - 0.1, s("fix3") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["slam1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["slam1"], 1.2)
        elif ph == "fix3":
            self.chip(540, 300, "tank", T["tank"] - 0.2, T["calm"] - 0.1, accent="#CBD5E1", size=54)
            self.chip(540, 300, "calm", T["calm"] - 0.1, s("break4") - 0.15, accent=GOOD, size=54)
            self.badge("check", T["calm1"], s("break4") - 0.15, x=920, y=440)
        elif ph == "break4":
            self.chip(540, 300, "down", T["down4"] - 0.2, T["climb"] - 0.1, accent="#CBD5E1", size=54)
            self.chip(540, 300, "climb", T["climb"] - 0.1, s("fix4") - 0.15, accent=WARN, size=52)
            self.badge("alert", T["climb1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["climb1"], 1.2)
        elif ph == "fix4":
            self.chip(540, 300, "pumps", T["pumps"] - 0.2, T["jet"] - 0.1, accent="#FB923C", size=56)
            self.chip(540, 300, "jet", T["jet"] - 0.1, T["edo"] - 0.1, accent="#FB923C", size=50)
            self.chip(540, 300, "edo", T["edo"] - 0.1, s("cta") - 0.15, accent=GOOD, size=56)
            self.badge("check", T["edo1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: pool (reveal)
    def draw_pool(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B3B5C", "#0E4F73"])
        u = max(0.0, t - T["pool"])
        cyc = (u % 1.3) / 1.0 if t >= T["pool"] else 0.0
        level = 1.0 - clamp(cyc)
        pool(c, 200, 470, 880, 1180, level if t >= T["pool"] else 1.0, t, a=prog(t, s("reveal") - 0.1, T["answer"] + 0.3))
        stopwatch(c, 540, 820, 150, clamp(cyc), a=prog(t, T["pool"] - 0.2, T["pool"] + 0.2))

    def ui_pool(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "pool", T["pool"] - 0.2, T["second"] - 0.1, accent="#7DD3FC", size=56)
        self.chip(540, 300, "second", T["second"] - 0.1, s("stat") - 0.15, accent=HILITE, size=60)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:                              # one noodle clogs the kitchen sink
            vrect(c, 0, 0, W, H, ["#334155", "#1E293B"])
            for k in range(6):
                for j in range(3):
                    c.drawRect(R(k * 180 + 10, 60 + j * 150, 160, 130), P("#475569"))
            c.drawRect(R(0, 600, W, 40), P("#A16207"))
            c.drawRRect(rr(80, 640, 920, 520, 40), P("#6B7280"))
            c.drawRRect(rr(140, 690, 800, 420, 60), lin_paint(0, 690, 0, 1110, ["#9CA3AF", "#4B5563"]))
            rise = prog(t, T["t_sink"] - 0.3, T["t_noodle"] + 0.6)
            if rise > 0:
                top = lerp(1090, 760, rise)
                c.drawRRect(rr(146, top, 788, 1104 - top, 50), P("#3B82F6", 0.75))
            c.drawCircle(540, 1060, 34, P("#374151"))
            nood = skia.Path()
            nood.moveTo(470, 1050)
            nood.cubicTo(500, 1000, 560, 1110, 610, 1040)
            nood.cubicTo(640, 1000, 680, 1060, 700, 1020)
            c.drawPath(nood, P("#FCD34D", 1, stroke=10))
            c.drawLine(540, 640, 540, 520, P("#9CA3AF", 1, stroke=30))
            c.drawLine(540, 520, 700, 520, P("#9CA3AF", 1, stroke=30))
            c.drawLine(700, 520, 700, 600, P("#9CA3AF", 1, stroke=24))
            person(c, 900, 1260, 380, "#F97316", t, pose="shrug" if t >= T["t_noodle"] else "look", face=-1)
        else:                                         # ten minutes of rain and the street is a swimming pool
            vrect(c, 0, 0, W, H, ["#475569", "#64748B"])
            for k in range(4):
                c.drawRect(R(k * 280 - 20, 300 + (k % 2) * 80, 240, 700), P("#A8A29E" if k % 2 else "#78716C"))
                for j in range(5):
                    c.drawRect(R(k * 280 + 20, 360 + (k % 2) * 80 + j * 120, 60, 70), P("#1E293B", 0.7))
                    c.drawRect(R(k * 280 + 110, 360 + (k % 2) * 80 + j * 120, 60, 70), P("#1E293B", 0.7))
            c.drawRect(R(0, 1000, W, 400), P("#374151"))
            rise = prog(t, T["t_sink"] - 0.3, T["t_noodle"] + 0.4)
            car_y = 1080
            c.drawRRect(rr(180, car_y - 170, 520, 140, 30), P("#B91C1C"))
            c.drawRRect(rr(270, car_y - 250, 320, 100, 30), P("#991B1B"))
            c.drawRRect(rr(290, car_y - 235, 130, 70, 12), P("#1E293B"))
            c.drawRRect(rr(440, car_y - 235, 130, 70, 12), P("#1E293B"))
            for wx in (280, 600):
                c.drawCircle(wx, car_y - 20, 50, P("#111827"))
            lvl = lerp(1060, 990, rise)
            c.drawRect(R(0, lvl, W, H - lvl), P("#8B7B5E", 0.85))
            for k in range(12):
                xx = (k * 100 + t * 50) % (W + 60) - 30
                c.drawLine(xx, lvl + 8, xx + 40, lvl + 8, P("#E7E5E4", 0.6, stroke=3))
            person(c, 860, 990, 340, "#F8FAFC", t, pose="shrug" if t >= T["t_noodle"] else "look", face=-1,
                   hair="#111827")
            rng = random.Random(9)
            for k in range(80):
                x = (rng.uniform(0, W + 300) - t * 300) % (W + 300) - 150
                y = (rng.uniform(0, H) + t * 1400) % 1300
                c.drawLine(x, y, x - 12, y + 36, P("#E0F2FE", 0.5, stroke=2))
            stopwatch(c, 170, 560, 90, clamp(prog(t, T["t_swallow"], T["t_noodle"])) * 0.17, a=prog(t, T["t_sink"] - 0.3, T["t_sink"]))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "noodle", T["t_sink"] - 0.3, T["t_noodle"] - 0.1, accent="#FDE68A", size=50)
        self.chip(540, 300, "clog", T["t_noodle"] - 0.1, self.duration + 1, accent=WARN, size=58)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["japan"], rumble(1.6, 62), -16), (T["pillars"], sfx.riser(1.0, 63), -12),
              (T["flood0"], sfx.ding(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["typhoons"], sfx.hiss(2.4, 65), -14),
               (T["flood1b"], sfx.womp(), -10), (T["flood1b"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 66), -6), (T["wells"], sfx.hiss(1.4, 67), -14),
               (T["catch1"], sfx.ding(), -8), (T["catch1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["full1"], sfx.thud(0.4, 68), -8), (T["full1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["tunnel"], sfx.whirr(1.0, 120.0, 200.0, 69), -12), (T["km1"], sfx.ding(), -8), (T["km1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["races"], sfx.whoosh(1.0, True, 70), -6), (T["slam1"], boom(1.4, 71), -6),
               (T["slam1"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(T["tank"], sfx.hiss(1.0, 72), -14), (T["calm1"], sfx.ding(), -8), (T["calm1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["climb1"], sfx.womp(), -10), (T["climb1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["pumps"], sfx.charge_up(0.8), -10), (T["jet"], sfx.whirr(1.6, 300.0, 600.0, 73), -10),
               (T["edo1"], sfx.ding(), -8), (T["edo1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["pool"], sfx.hiss(1.2, 95), -10),
               (T["second"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_sink"], sfx.hiss(1.0, 104), -14),
               (T["t_noodle"], sfx.womp(), -8)]
        return ev


NAME = "gcans"
EPISODE = GCans
