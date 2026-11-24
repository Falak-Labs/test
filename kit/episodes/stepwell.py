"""Episode 75 - Chand Baori, the stepwell of Abhaneri (Rajasthan).  v2 look: the well cut open across its middle (ground
y = 0, the pool about 560 units down): the back wall covered in little zigzag flights of steps, the side walls stepping
in floor by floor like an upside-down pyramid, a green pool at the bottom.

Sets: well (hook: close on the zigzag stairs, out to the whole pit with people at the water; break1: the dry desert
above, the sun, a thermometer, "how much cooler down there?"; fix1: the square pit is dug, monsoon rain and ground
water fill it; break2: months pass and the water sinks out of reach; fix2: steps run down three walls, 3,500 of them;
break3: straight earth walls cave in and bury the water; fix3: the walls lean back in 13 stone floors; break4: one
narrow stair jams with people and pots; fix4: zigzag pairs, people up and down at once; reveal: summer, two
thermometers, people resting by the water; stat; closer at sunset), lobby (tag: 3,500 steps and you take the lift
up one floor).
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of  # noqa: E402
from windtower import sun, heat_lines  # noqa: E402
from bigben import thermometer  # noqa: E402

DAYP = {"top": "#0E2F5E", "upper": "#1B4F8F", "mid": "#2A62A4", "low": "#3E7AB8", "horizon": "#7FB2DE",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SUNSETP = {"top": "#1A1440", "upper": "#3B2A6A", "mid": "#8A4A7A", "low": "#E07A4E", "horizon": "#FFB061",
           "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STONE = ("#D9B98A", "#B8935E", "#8A6A3E", "#5E4426")   # lit, mid, shade, deep
EARTH = ("#9C6B3E", "#6E4826")
DEPTH = 560.0
TOP_HW, BOT_HW = 420.0, 110.0
FLOORS = 13


def wall_hw(y, lean):
    """Half width of the pit at depth y (0 at the top, DEPTH at the pool) for lean 0 (straight) .. 1 (pyramid)."""
    straight = 270.0
    pyr = lerp(TOP_HW, BOT_HW, clamp(y / DEPTH))
    return lerp(straight, pyr, lean)


def pit_path(lean, depth=DEPTH):
    p = skia.Path()
    n = 26
    pts_l = [(-wall_hw(depth * i / n, lean), depth * i / n) for i in range(n + 1)]
    pts_r = [(wall_hw(depth * i / n, lean), depth * i / n) for i in range(n + 1)]
    p.moveTo(*pts_l[0])
    for q in pts_l[1:]:
        p.lineTo(*q)
    for q in reversed(pts_r):
        p.lineTo(*q)
    p.close()
    return p


def zig_stairs(c, x0, x1, y0, y1, a=1.0, lit=1.0, unit=56.0, glow=0.0):
    """One floor of the back wall: little double flights of steps meeting in peaks (the stepwell's zigzag)."""
    if a <= 0 or x1 <= x0:
        return
    h = y1 - y0
    c.drawRect(R(x0, y0, x1 - x0, h), P(mix(STONE[2], "#3A2A40", 1 - lit), a))
    x = x0
    while x < x1 - 4:
        w = min(unit, x1 - x)
        # the two flights: a "Λ" of stone steps on a darker wall
        lp = path_of([(x, y1), (x + w / 2, y0 + 3), (x + w / 2 + 6, y0 + 3), (x + 6, y1)], close=True)
        rp = path_of([(x + w, y1), (x + w / 2, y0 + 3), (x + w / 2 - 6, y0 + 3), (x + w - 6, y1)], close=True)
        c.drawPath(lp, P(mix(STONE[0], "#6B5A70", 1 - lit), a))
        c.drawPath(rp, P(mix(STONE[1], "#4A3E58", 1 - lit), a))
        for k in range(1, 4):                                            # the step lines
            yy = y1 - k * h / 4
            c.drawLine(x + k * w / 8 + 2, yy, x + k * w / 8 + 8, yy, P(mix(STONE[3], "#20182A", 1 - lit), 0.8 * a, stroke=1.5))
            c.drawLine(x + w - k * w / 8 - 8, yy, x + w - k * w / 8 - 2, yy, P(mix(STONE[3], "#20182A", 1 - lit), 0.8 * a, stroke=1.5))
        x += w
    c.drawLine(x0, y0, x1, y0, P(mix(STONE[0], "#8A7A90", 1 - lit), a, stroke=3))
    if glow > 0:
        c.drawRect(R(x0, y0, x1 - x0, h), P(GOOD, 0.18 * glow * a))


def well(c, t, dug=1.0, lean=1.0, steps=1.0, water=0.35, lit=1.0, cave=0.0, single=0.0, a=1.0, rain=0.0):
    """The stepwell in section (world). dug 0..1 how deep the pit is; steps 0..1 how many floors have stairs (from the
    top); water = pool level 0 (dry) .. 1 (brim full); cave 0..1 straight earth walls falling in; single 0..1 shows
    one narrow stair instead of the zigzags."""
    depth = DEPTH * dug
    if depth <= 2:
        c.drawRect(R(-1400, 0, 2800, 1800), lin_paint(0, 0, 0, 900, [mix("#B07A44", "#3A2A40", 1 - lit), mix("#6E4826", "#1E1626", 1 - lit)], a=a))
        return
    p = pit_path(lean, depth)
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    c.drawRect(R(-600, 0, 1200, depth + 4), lin_paint(0, 0, 0, depth, [mix(EARTH[0], "#3A2A40", 1 - lit), mix(EARTH[1], "#1E1626", 1 - lit)], a=a))
    nfl = FLOORS
    fh = DEPTH / nfl
    shown = int(math.ceil(nfl * steps))
    for k in range(nfl):
        y0 = k * fh
        if y0 >= depth:
            break
        y1 = min(depth, y0 + fh)
        hw0 = wall_hw(y0, lean)
        if k < shown and single <= 0.5:
            f = clamp(nfl * steps - k)
            zig_stairs(c, -hw0, -hw0 + 2 * hw0 * f, y0, y1, a=a, lit=lit)
        elif single > 0.5:
            c.drawRect(R(-hw0, y0, 2 * hw0, y1 - y0), P(mix(STONE[2], "#3A2A40", 1 - lit), a))
            c.drawLine(-hw0, y0, hw0, y0, P(mix(STONE[0], "#8A7A90", 1 - lit), a, stroke=3))
    if single > 0:                                                       # one narrow staircase down the middle
        sp = path_of([(-150, 0), (-40, DEPTH * 0.45), (-150, DEPTH * 0.9)])
        c.drawPath(sp, P(STONE[0], single * a, stroke=26))
        c.drawPath(sp, P(STONE[3], single * a, stroke=3))
    # the water
    if water > 0:
        wl = lerp(depth, depth - DEPTH * 0.55, clamp(water))
        c.drawRect(R(-600, wl, 1200, depth - wl + 4), lin_paint(0, wl, 0, depth, ["#3FA37C", "#1E5A48"], a=0.92 * a))
        c.drawLine(-600, wl, 600, wl, P("#BEF264", 0.6 * a, stroke=3))
        for k in range(5):
            xx = -60 + k * 30 + math.sin(t * 1.2 + k) * 6
            c.drawLine(xx, wl + 6, xx + 20, wl + 6, P("#D9F99D", 0.4 * a, stroke=2))
    if rain > 0:
        rng = random.Random(3)
        for k in range(60):
            u = (t * 1.4 + rng.random()) % 1.0
            x = rng.uniform(-400, 400)
            y = lerp(-500, depth, u)
            c.drawLine(x, y, x - 6, y + 26, P("#BFDBFE", 0.7 * rain * a, stroke=2))
    c.restore()
    # the side walls in section (terraces when lean > 0)
    for sd in (-1, 1):
        pts = [(sd * 1400, 0), (sd * wall_hw(0, lean), 0)]
        for k in range(1, 27):
            y = depth * k / 26
            pts.append((sd * wall_hw(y, lean), y))
        pts += [(sd * wall_hw(depth, lean), depth + 60), (sd * 1400, depth + 60), (sd * 1400, 0)]
        c.drawPath(path_of(pts, close=True), lin_paint(0, 0, 0, depth + 60, [mix("#B07A44", "#3A2A40", 1 - lit), mix("#7A5030", "#1E1626", 1 - lit)], a=a))
        if lean > 0.3:
            for k in range(FLOORS):
                y = k * DEPTH / FLOORS
                if y > depth:
                    break
                x = sd * wall_hw(y, lean)
                c.drawLine(x, y, x + sd * 46, y, P(mix(STONE[0], "#8A7A90", 1 - lit), lean * a, stroke=4))
                c.drawLine(x, y, x, y + DEPTH / FLOORS, P(mix(STONE[3], "#20182A", 1 - lit), 0.6 * lean * a, stroke=3))
        if cave > 0:                                                     # chunks falling off the straight walls
            rng = random.Random(5 if sd < 0 else 6)
            for k in range(14):
                y0 = rng.uniform(40, depth - 60)
                u = clamp(cave * 1.3 - k * 0.04)
                x = sd * wall_hw(y0, lean) - sd * u * rng.uniform(30, 160)
                y = y0 + u * u * (depth - y0)
                c.drawCircle(x, y, rng.uniform(10, 26), P("#7A5030", a))
    c.drawRect(R(-1400, depth + 2, 2800, 1800), P(mix("#6E4826", "#1E1626", 1 - lit), a))
    if cave > 0:                                                         # the pile that buries the pool
        pile = path_of([(-260, depth + 4), (-120, depth - 120 * cave), (0, depth - 150 * cave), (120, depth - 110 * cave), (260, depth + 4)],
                       close=True)
        c.drawPath(pile, P("#8A5A32", a))


def surface(c, t, lit=1.0, crack=0.0, a=1.0):
    """The land around the well (world, above y = 0)."""
    c.drawRect(R(-1400, -30, 2800, 40), P(mix("#C99A62", "#3A2A40", 1 - lit), a))
    c.drawRect(R(-1400, -34, 2800, 6), P(mix("#E3C08A", "#5A4A60", 1 - lit), a))
    if crack > 0:
        rng = random.Random(8)
        for k in range(18):
            x = rng.uniform(-900, 900)
            c.drawLine(x, -28, x + rng.uniform(-30, 30), -6, P("#6E4826", crack * a, stroke=3))
    for x in (-520, 470):                                                # pavilion / walls around the top
        c.drawRect(R(x - 60, -130, 120, 100), P(mix("#D9B98A", "#5A4A60", 1 - lit), a))
        for k in range(3):
            c.drawRect(R(x - 48 + k * 36, -112, 20, 60), P(mix("#5E4426", "#20182A", 1 - lit), a))
        c.drawRect(R(x - 70, -140, 140, 12), P(mix("#E3C08A", "#6A5A70", 1 - lit), a))


def villager(c, x, y, h, t, col, pot=True, pose="walk", face=1, a=1.0):
    person(c, x, y, h, col, t, pose=pose, face=face, hair="#1F1A17", skin="#B97A50", a=a)
    if pot:
        u = h / 140.0
        c.drawCircle(x, y - 150 * u, 14 * u, P("#B45309", a))
        c.drawRect(R(x - 7 * u, y - 166 * u, 14 * u, 6 * u), P("#92400E", a))


def elevator(c, x, y, s, t, open_k=0.0, a=1.0):
    c.drawRect(R(x - 120 * s, y - 330 * s, 240 * s, 330 * s), P("#94A3B8", a))
    for sd in (-1, 1):
        c.drawRect(R(x + sd * 60 * s * open_k - 110 * s + (110 * s if sd > 0 else 0), y - 320 * s, 110 * s, 320 * s),
                   lin_paint(x - 110 * s, 0, x + 110 * s, 0, ["#64748B", "#8391A6", "#64748B"], a=a))
    c.drawRect(R(x - 30 * s, y - 380 * s, 60 * s, 36 * s), P("#0F172A", a))
    text(c, "1", x, y - 352 * s, 28 * s, "#F87171", "Poppins-Bold", a=a)
    c.drawCircle(x + 150 * s, y - 170 * s, 12 * s, P("#FDE68A", a))


# ====================================================================================== the episode
class Stepwell(EpisodeV2):
    BUILD_NO = 75
    FIRST_SET = "well"
    CLEAR = "#0B1220"
    TITLE = {"en": "CHAND BAORI", "ar_sa": "تشاند باوري"}
    EMPH = {"en": ["CONGRATS", "UPSIDE", "DOWN", "PYRAMID", "STAIRS", "CHAND", "BAORI", "YOURSELF", "RAINS", "HOT",
                   "DESERT", "COOLER", "BOTTOM", "PIT", "MONSOON", "UNDERGROUND", "DRY", "SINKS", "LOWER", "THREE",
                   "STEPS", "THIRTY", "FIVE", "HUNDRED", "WALLS", "CAVE", "BURY", "LEAN", "THIRTEEN", "FLOORS",
                   "NARROW", "JAM", "POTS", "ZIGZAG", "PAIRS", "ONCE", "FOLLOW", "PRESSURE", "COOKER", "DEGREES",
                   "SUMMER", "REST", "TWELVE", "YEARS", "ELEVATOR", "ONE", "FLOOR"],
            "ar_sa": ["مبروك", "هرم", "مقلوب", "الدرج", "تشاند", "باوري", "بيدك", "حر", "المطر", "أبرد", "تحت", "حفرة",
                      "الموسم", "الأرض", "تنزل", "ثلاث", "درجة", "آلاف", "وخمسمية", "جدران", "بتطيح", "وتدفن", "ترجع",
                      "ثلطعش", "دور", "وضيق", "بيزحم", "وجرار", "يتعرّج", "أزواج", "تابعني", "الضغط", "بخمس",
                      "الصيف", "يرتاحون", "ومتين", "المصعد", "واحد"]}
    KEYS = {"ar_sa": {
        ("hook", "DIG"): "تحفر", ("hook", "PYRAMID"): "هرم", ("hook", "CONGRATS"): "مبروك", ("hook", "CHAND"): "تشاند",
        ("break1", "RAINS"): "المطر", ("break1", "HOT"): "حر", ("break1", "COOLER"): "أبرد", ("break1", "BOTTOM"): "تحت",
        ("fix1", "PIT"): "حفرة", ("fix1", "MONSOON"): "الموسم", ("fix1", "UNDERGROUND"): "الأرض",
        ("break2", "DRY"): "شهر", ("break2", "SINKS"): "تنزل", ("break2", "LOWER"): "أكثر",
        ("fix2", "THREE"): "ثلاث", ("fix2", "STEPS"): "درج", ("fix2", "THIRTY"): "آلاف", ("fix2", "WATER"): "للموية",
        ("break3", "WALLS"): "جدران", ("break3", "CAVE"): "بتطيح", ("break3", "BURY"): "وتدفن",
        ("fix3", "LEAN"): "ترجع", ("fix3", "THIRTEEN"): "ثلطعش", ("fix3", "PYRAMID"): "هرم",
        ("break4", "NARROW"): "وضيق", ("break4", "JAM"): "بيزحم", ("break4", "POTS"): "وجرار",
        ("fix4", "ZIGZAG"): "يتعرّج", ("fix4", "PAIRS"): "أزواج", ("fix4", "LOTS"): "كثير", ("fix4", "ONCE"): "بعض",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "FIVE"): "بخمس", ("reveal", "COOLER"): "أبرد", ("reveal", "SUMMER"): "الصيف", ("reveal", "REST"): "يرتاحون",
        ("stat", "THIRTY"): "ثلاثة", ("stat", "THIRTEEN"): "وثلطعش", ("stat", "TWELVE"): "ومتين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STEPS"): "درجة", ("tag", "ELEVATOR"): "المصعد", ("tag", "ONE"): "واحد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a pressure cooker"),
                   "stat": [("3,500", "STEPS"), ("13", "FLOORS"), ("1,200", "YEARS OLD")],
                   "L": {"name": "CHAND BAORI, INDIA", "pyr": "AN UPSIDE-DOWN PYRAMID", "dry": "RAIN: A FEW WEEKS A YEAR",
                         "q": "HOW MUCH COOLER DOWN THERE?", "pit": "DIG A BIG SQUARE PIT", "fill": "RAIN + GROUND WATER",
                         "sinks": "THE WATER SINKS", "steps": "3,500 STEPS", "walls3": "STEPS ON 3 WALLS",
                         "cave": "THE WALLS CAVE IN", "lean": "13 STONE FLOORS", "jam": "ONE STAIR: A JAM",
                         "pairs": "ZIGZAG PAIRS", "both": "UP AND DOWN AT ONCE", "top": "TOP", "bottom": "BOTTOM",
                         "five": "ABOUT 5°C COOLER", "rest": "SUMMER: REST BY THE WATER", "lift": "1 FLOOR UP",
                         "stairs": "THE STAIRS", "months": "MONTH"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قدر الضغط"),
                      "stat": [("3500", "درجة"), ("13", "دور"), ("1200", "سنة")],
                      "L": {"name": "تشاند باوري، الهند", "pyr": "هرم مقلوب", "dry": "المطر: كم أسبوع بالسنة",
                            "q": "كم أبرد تحت؟", "pit": "حفرة مربعة كبيرة", "fill": "مطر + موية من تحت الأرض",
                            "sinks": "الموية تنزل", "steps": "3500 درجة", "walls3": "درج على 3 جدران",
                            "cave": "الجدران تطيح", "lean": "13 دور من الحجر", "jam": "درج واحد: زحمة",
                            "pairs": "درج متعرّج أزواج", "both": "طالع ونازل مع بعض", "top": "فوق", "bottom": "تحت",
                            "five": "أبرد بـ 5 درجات", "rest": "الصيف: راحة جنب الموية", "lift": "دور واحد بس",
                            "stairs": "الدرج", "months": "شهر"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "dig": ("hook", "DIG", 0.1), "pyramid": ("hook", "PYRAMID", 0.35), "congrats": ("hook", "CONGRATS", 0.6),
            "name": ("hook", "CHAND", 0.88),
            "rains": ("break1", "RAINS", 0.2), "hot": ("break1", "HOT", 0.45), "cooler": ("break1", "COOLER", 0.75),
            "bottom": ("break1", "BOTTOM", 0.92),
            "pit": ("fix1", "PIT", 0.25), "monsoon": ("fix1", "MONSOON", 0.6), "under": ("fix1", "UNDERGROUND", 0.9),
            "dry": ("break2", "DRY", 0.2), "sinks": ("break2", "SINKS", 0.5), "lower": ("break2", "LOWER", 0.8),
            "three": ("fix2", "THREE", 0.15), "steps": ("fix2", "STEPS", 0.3), "thirty": ("fix2", "THIRTY", 0.55),
            "water2": ("fix2", "WATER", 0.92),
            "walls": ("break3", "WALLS", 0.15), "cave": ("break3", "CAVE", 0.6), "bury": ("break3", "BURY", 0.85),
            "lean": ("fix3", "LEAN", 0.15), "thirteen": ("fix3", "THIRTEEN", 0.55), "pyr3": ("fix3", "PYRAMID", 0.9),
            "narrow": ("break4", "NARROW", 0.2), "jam": ("break4", "JAM", 0.5), "pots": ("break4", "POTS", 0.9),
            "zigzag": ("fix4", "ZIGZAG", 0.2), "pairs": ("fix4", "PAIRS", 0.4), "lots": ("fix4", "LOTS", 0.7),
            "once": ("fix4", "ONCE", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "five": ("reveal", "FIVE", 0.3), "cool5": ("reveal", "COOLER", 0.4), "summer": ("reveal", "SUMMER", 0.6),
            "rest": ("reveal", "REST", 0.8),
            "s1": ("stat", "THIRTY", 0.05), "s2": ("stat", "THIRTEEN", 0.4), "s3": ("stat", "TWELVE", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_steps": ("tag", "STEPS", 0.15), "t_elevator": ("tag", "ELEVATOR", 0.6), "t_one": ("tag", "ONE", 0.9)})
        T["cool1"] = max(T["cooler"], T["hot"], T["rains"]) + 0.15
        T["under1"] = max(T["under"], T["monsoon"]) + 0.2
        T["lower1"] = max(T["lower"], T["sinks"]) + 0.15
        T["water21"] = max(T["water2"], T["thirty"]) + 0.2
        T["bury1"] = max(T["bury"], T["cave"]) + 0.1
        T["pyr31"] = max(T["pyr3"], T["thirteen"]) + 0.2
        T["pots1"] = max(T["pots"], T["jam"]) + 0.15
        T["once1"] = max(T["once"], T["lots"]) + 0.2
        # ---- sets
        self.cut(s("tag") - 0.2, "lobby", 1)
        # ---- camera
        FULL = (0, 360, 1.3)
        cm = Camera(-150, 300, 3.0)
        cm.key(0.05, -120, 300, 2.8, 1.0)
        cm.key(max(1.0, T["congrats"] - 0.8), *FULL, max(1.0, T["name"] - T["congrats"] + 0.9))
        cm.key(s("break1") - 0.12, 0, -120, 1.3, 0.0)                     # the dry land above
        cm.key(s("fix1") - 0.1, *FULL, 1.2)
        cm.key(s("break4") - 0.12, -40, 330, 1.6, 0.0)
        cm.key(s("cta") - 0.1, *FULL, 1.0)
        cm.key(s("reveal") - 0.12, 0, 300, 1.25, 0.0)
        cm.key(s("stat") - 0.12, 0, 420, 1.35, 0.0)
        cm.key(s("closer") - 0.12, 0, 400, 1.25, 0.8)
        self.cam = cm
        self.spans = [(T["cool1"], T["under1"] + 0.3), (T["lower1"], T["water21"] + 0.3), (T["bury1"], T["pyr31"] + 0.3),
                      (T["pots1"], T["once1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["cool1"], 0.3, 6), (T["lower1"], 0.3, 6), (T["cave"], 0.9, 14),
                       (T["pots1"], 0.4, 8), (s("closer") + 0.2, 0.35, 8), (T["t_one"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1", "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: well
    def draw_well(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        ph = self.phase(t)
        gy = self.to_screen(cam, 0, -30)[1]
        pal = DAYP if ph not in ("stat", "closer") else SUNSETP
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=gy)
        if ph in ("break1", "reveal"):
            sun(c, 800, max(260, gy - 420), 56, heat=1.0)
        elif ph not in ("stat", "closer"):
            sun(c, 860, max(200, gy - 600), 40, heat=0.5)
        self.view(c, cam)
        dug, lean, steps, water, cave, single, rain, lit = 1.0, 1.0, 1.0, 0.35, 0.0, 0.0, 0.0, 1.0
        crack = 0.0
        if ph == "break1":
            dug, crack = 0.0, prog(t, T["hot"] - 0.3, T["hot"] + 0.3)
        elif ph == "fix1":
            dug = e_io(prog(t, T["pit"] - 0.3, T["pit"] + 0.8))
            lean, steps = 0.0, 0.0
            rain = prog(t, T["monsoon"] - 0.3, T["monsoon"]) * (1 - prog(t, T["under"], T["under"] + 0.5))
            water = 0.15 + 0.8 * prog(t, T["monsoon"] - 0.2, T["under1"] + 0.3)
        elif ph == "break2":
            lean, steps = 0.0, 0.0
            water = lerp(0.95, 0.12, prog(t, T["dry"] - 0.2, T["lower1"] + 0.3))
        elif ph == "fix2":
            lean = 0.0
            steps = prog(t, T["three"] - 0.2, T["water2"] + 0.2)
            water = 0.12
        elif ph == "break3":
            lean = 0.0
            cave = prog(t, T["cave"] - 0.3, T["bury1"] + 0.4)
            water = 0.12 * (1 - cave)
        elif ph == "fix3":
            lean = e_io(prog(t, T["lean"] - 0.3, T["thirteen"] + 0.3))
            water = 0.3
        elif ph == "break4":
            single = 1.0
        elif ph == "closer":
            lit = 1.0
        surface(c, t, lit=lit, crack=crack)
        well(c, t, dug=dug, lean=lean, steps=steps, water=water, lit=lit, cave=cave, single=single, rain=rain)
        if ph == "break1":
            heat_lines(c, -500, 500, -260, -40, t, a=0.8 * crack)
        # people
        if ph in ("hook", "closer", "stat", "reveal", "fix3", "fix4", "cta"):
            busy = 1.0 if ph in ("fix4", "cta", "reveal", "stat", "closer", "hook") else 0.4
            rng = random.Random(12)
            cols = ("#DC2626", "#F59E0B", "#2563EB", "#DB2777", "#16A34A", "#7C3AED")
            n = int(12 * busy)
            for i in range(n):
                k = rng.randint(1, FLOORS - 2)
                y = k * DEPTH / FLOORS
                hw = wall_hw(y, 1.0)
                if ph == "fix4" or ph == "cta":
                    u = (t * 0.08 * (1 if i % 2 else -1) + rng.random()) % 1.0
                    x = lerp(-hw + 20, hw - 20, u)
                    y = y + math.sin(u * 40) * 6
                else:
                    x = rng.uniform(-hw + 20, hw - 20)
                villager(c, x, y, 30, t + i, cols[i % 6], pot=i % 2 == 0, pose="walk" if ph in ("fix4", "cta") else "stand",
                         face=1 if i % 2 else -1)
            if ph in ("reveal", "stat", "closer", "hook"):
                for i, x in enumerate((-60, -20, 30, 70)):                  # resting by the water
                    person(c, x, DEPTH - DEPTH * 0.55 * 0.35 - 2, 26, cols[i], t + i, pose="sit", face=1 if i % 2 else -1,
                           skin="#B97A50", hair="#1F1A17")
        if ph == "break4":
            for i in range(9):                                              # stuck on the one stair
                u = 0.15 + i * 0.08
                x = lerp(-150, -40, u / 0.5) if u < 0.5 else lerp(-40, -150, (u - 0.5) / 0.4)
                y = DEPTH * 0.9 * u
                villager(c, x, y - 4, 30, t * 0.2 + i, ("#DC2626", "#F59E0B", "#2563EB")[i % 3], pot=True, pose="stand",
                         face=1 if i % 2 else -1)
        if ph == "break2" or ph == "fix2":
            villager(c, -300, -30, 34, t, "#DC2626", pot=True, pose="look", face=1)
            rk = prog(t, T["sinks"], T["lower1"]) if ph == "break2" else 0.0
            if ph == "break2":                                              # the rope that no longer reaches
                c.drawLine(-240, -40, -240, lerp(200, 330, rk), P("#E7C9A0", 0.9, stroke=3))
                c.drawCircle(-240, lerp(210, 340, rk), 10, P("#B45309"))
        c.restore()
        self.ui["cam"] = cam

    def ui_well(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        cam = self.ui.get("cam", self.cam.at(tw))
        if ph == "hook":
            self.chip(540, 300, "pyr", T["pyramid"] - 0.2, T["congrats"] - 0.15, accent="#FDBA74", size=46)
            self.chip(540, 300, "name", T["congrats"] - 0.15, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if ph == "break1":
            self.chip(540, 300, "dry", T["rains"] - 0.2, T["cooler"] - 0.2, accent=WARN, size=40)
            self.chip(540, 300, "q", T["cooler"] - 0.2, s("fix1") - 0.15, accent=HILITE, size=40)
            k = self.span(T["hot"] - 0.2, s("fix1") - 0.15)
            if k > 0:
                thermometer(c, 930, 820, 1.3, 0.9, hot=True, a=k)
            self.badge("alert", T["cool1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["cool1"], 1.2)
            return
        if ph == "fix1":
            self.chip(540, 300, "pit", T["pit"] - 0.2, T["monsoon"] - 0.2, accent="#FDBA74", size=46)
            self.chip(540, 300, "fill", T["monsoon"] - 0.2, s("break2") - 0.15, accent="#7DD3FC", size=44)
            self.badge("check", T["under1"] + 0.1, s("break2") - 0.15, x=920, y=440)
            return
        if ph == "break2":
            n = 1 + int(5 * prog(tw, T["dry"] - 0.2, T["lower1"] + 0.3))
            k = self.span(T["dry"] - 0.2, s("fix2") - 0.15)
            v2.chip(c, 540, 300, "%s %d" % (self.L["months"], n), k, accent="#FDBA74", size=46)
            self.chip(540, 410, "sinks", T["sinks"] - 0.2, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["lower1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["lower1"], 1.2)
            return
        if ph == "fix2":
            self.chip(540, 300, "walls3", T["three"] - 0.2, T["thirty"] - 0.2, accent="#FDBA74", size=46)
            self.chip(540, 300, "steps", T["thirty"] - 0.2, s("break3") - 0.15, accent=HILITE, size=54)
            self.badge("check", T["water21"] + 0.1, s("break3") - 0.15, x=920, y=440)
            return
        if ph == "break3":
            self.chip(540, 300, "cave", T["cave"] - 0.3, s("fix3") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["bury1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["bury1"], 1.2)
            return
        if ph == "fix3":
            self.chip(540, 300, "lean", T["lean"] - 0.2, s("break4") - 0.15, accent=HILITE, size=50)
            self.badge("check", T["pyr31"] + 0.1, s("break4") - 0.15, x=920, y=440)
            return
        if ph == "break4":
            self.chip(540, 300, "jam", T["narrow"] - 0.2, s("fix4") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["pots1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["pots1"], 1.2)
            return
        if ph == "fix4":
            self.chip(540, 300, "pairs", T["zigzag"] - 0.2, T["lots"] - 0.2, accent=HILITE, size=50)
            self.chip(540, 300, "both", T["lots"] - 0.2, s("cta") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["once1"] + 0.1, s("cta") - 0.15, x=920, y=440)
            return
        if ph == "reveal":
            k = self.span(T["five"] - 0.3, s("stat") - 0.15)
            if k > 0:
                x0, y0 = self.to_screen(cam, 330, -80)
                x1, y1 = self.to_screen(cam, 160, DEPTH - 120)
                thermometer(c, min(980, x0), y0, 1.1, 0.95, hot=True, a=k)
                thermometer(c, min(980, x1 + 120), y1, 1.1, 0.55, hot=False, a=k)
            self.chip(540, 300, "five", T["five"] - 0.2, T["summer"] - 0.2, accent="#7DD3FC", size=50)
            self.chip(540, 300, "rest", T["summer"] - 0.2, s("stat") - 0.15, accent=GOOD, size=42)

    # ------------------------------------------------------------------ set: lobby (tag)
    def draw_lobby(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#2A2F4A", "#3B4160"])
        c.drawRect(R(0, 1150, W, H - 1150), P("#4B5563"))
        # the stairs on the left, a lift on the right
        for k in range(9):
            c.drawRect(R(60 + k * 34, 1150 - (k + 1) * 46, 380 - k * 34, 46), P("#9CA3AF" if k % 2 else "#A8B0BC"))
            c.drawLine(60 + k * 34, 1150 - (k + 1) * 46, 440, 1150 - (k + 1) * 46, P("#6B7280", 1.0, stroke=3))
        ok = prog(t, T["t_elevator"] - 0.2, T["t_elevator"] + 0.6)
        elevator(c, 760, 1150, 1.0, t, open_k=ok)
        px = lerp(560, 760, e_io(prog(t, T["t_elevator"], T["t_one"])))
        person(c, px, 1150, 230, "#16A34A", t, pose="walk" if T["t_elevator"] < t < T["t_one"] else "stand", face=1)

    def ui_lobby(self, c, t, tw):
        T = self.T
        self.chip(260, 560, "stairs", T["t_steps"] - 0.1, self.duration + 1, accent=GOOD, size=40)
        self.chip(760, 560, "lift", T["t_elevator"] - 0.1, self.duration + 1, accent=WARN, size=44)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1220", "#1E293B"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["pyramid"], sfx.sparkle(1.0, 12, 62), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(T["hot"], sfx.hiss(1.2, 66), -16), (T["cool1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["pit"] - 0.2, sfx.thud(0.5, 67), -8), (T["monsoon"], sfx.hiss(1.6, 68), -10),
               (T["under1"], sfx.ding(), -8), (T["under1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["sinks"], sfx.power_down(1.0, 69), -14), (T["lower1"], sfx.alarm(3, 820.0), -12)]
        for k in range(8):
            ev.append((lerp(T["three"], T["water2"], k / 7), sfx.tap(70 + k), -12))
        ev += [(T["water21"], sfx.ding(), -8), (T["water21"] + 0.2, sfx.chime(), -6)]
        ev += [(T["cave"], v2set.rumble(1.6, 80), -6), (T["bury1"], sfx.thud(0.7, 81), -4), (T["bury1"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(T["lean"], sfx.whoosh(0.6, False, 82), -10)]
        for k in range(6):
            ev.append((lerp(T["lean"], T["thirteen"] + 0.3, k / 5), sfx.thunk(83 + k), -12))
        ev += [(T["pyr31"], sfx.ding(), -8), (T["pyr31"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 90), -6), (T["jam"], sfx.buzz(0.4), -14), (T["pots1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["zigzag"], sfx.whoosh(0.5, False, 91), -10), (T["once1"], sfx.ding(), -8), (T["once1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 94), -6), (T["five"], sfx.sparkle(0.9, 10, 95), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 96), -6), (T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3),
               (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"], sfx.pop(100), -2), (T["cong2"], sfx.sparkle(1.4, 18, 101), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 102), -6), (T["t_elevator"], sfx.ding(), -10), (T["t_one"], sfx.womp(), -8)]
        return ev


NAME = "stepwell"
EPISODE = Stepwell
