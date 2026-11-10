"""Episode 15 - A space station.  v2 look: three sets.

space   the station from outside, centred on the origin, with the curve of the Earth below (screen space)
inside  the module cut open from the side: the cabin x -520..520, y -410..0, machines standing on the "floor" (y = 0)
wall    a slice of the hull, very close, drawn straight on the screen: bumper, fabric, pressure wall
"""
from v2_base import *  # noqa: F401,F403

OX, SCR, TOI, DRUM, TANK, TREAD, ARED = -440, -300, -140, 10, 190, 300, 450
CO2C, O2C = "#A78BFA", "#BAE6FD"


def fan(c, x, y, r, ang, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawCircle(0, 0, r, P("#0B1220", 0.7 * a))
    c.drawCircle(0, 0, r, P("#CBD5E1", a, stroke=max(2.5, r * 0.1)))
    c.rotate(ang)
    for i in range(4):
        c.save()
        c.rotate(i * 90)
        c.drawOval(R(r * 0.1, -r * 0.2, r * 0.74, r * 0.4), P("#E5E9F2", 0.9 * a))
        c.restore()
    c.restore()


def floaty(c, x, y, ang, col, t, pose="stand", h=118, face=1):
    """An engineer adrift: centred on (x, y), turned by ang degrees."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    engineer(c, 0, h / 2, h, col, t, pose, face=face)
    c.restore()


def panel(c, x, y, w, h, a=1.0):
    c.drawRRect(rr(x, y, w, h, 4), lin_paint(x, y, x + w, y + h, [("#1D4ED8", a), ("#1E3A8A", a), ("#0B1E4D", a)]))
    for i in range(1, 4):
        c.drawLine(x + w * i / 4, y, x + w * i / 4, y + h, P("#93C5FD", 0.5 * a, stroke=1.5))
    c.drawLine(x, y + h / 2, x + w, y + h / 2, P("#93C5FD", 0.5 * a, stroke=1.5))
    c.drawRRect(rr(x, y, w, h, 4), P("#FDE68A", 0.9 * a, stroke=2.5))


def station(c, t, wings=0.0, cup=0.0, shield=0.0, hole=0.0, hatch=1.0, faces=True):
    """The module from outside, centred on the origin: 520 long, 190 across. wings / cup / shield 0..1 grow those parts."""
    if wings > 0:                                                                    # solar wings, unfolding up and down
        for sd in (-1, 1):
            c.drawRect(R(-5, 95 * sd if sd > 0 else -95 - 316 * wings, 10, 316 * wings), P("#94A3B8"))
            for row in range(4):
                k = clamp(wings * 4 - row)
                if k <= 0:
                    continue
                y0 = sd * (135 + row * 68)
                hh = 60 * k
                for sx in (-128, 8):
                    panel(c, sx, y0 - (hh if sd < 0 else 0) + (0 if sd < 0 else 0), 120, hh, 1.0)
    if shield > 0:                                                                   # shield panels standing off the hull
        for i in range(8):
            k = e_back(clamp(shield * 8 - i))
            if k <= 0:
                continue
            x0 = -236 + i * 60
            for sy in (-116, 104):
                c.drawRRect(rr(x0, sy, 52 * k, 12, 4), lin_paint(0, sy, 0, sy + 12, ["#F8FAFC", "#94A3B8"]))
                c.drawLine(x0 + 26, sy + (12 if sy < 0 else 0), x0 + 26, sy + (22 if sy < 0 else -10), P("#64748B", k, stroke=3))
    c.drawRRect(rr(260, -42, 46, 84, 10), lin_paint(0, -42, 0, 42, ["#CBD5E1", "#64748B"]))                 # docking port
    c.drawRRect(rr(-260, -95, 520, 190, 90), lin_paint(0, -95, 0, 95, ["#FFFFFF", "#CBD5E1", "#64748B"], [0.0, 0.45, 1.0]))
    for bx in (-150, 0, 150):
        c.drawRect(R(bx - 5, -95, 10, 190), P("#475569", 0.55))
    c.drawRRect(rr(-260, -95, 520, 190, 90), P("#FFFFFF", 0.35, stroke=3))
    c.drawCircle(-236, 0, 44, P("#334155"))                                          # the hatch
    c.save()
    c.translate(-236, 0)
    c.drawCircle(0, 0, 38, lin_paint(-38, -38, 38, 38, ["#E5E9F2", "#94A3B8"]) if hatch >= 1 else P("#0B1220"))
    if hatch < 1:
        c.save()
        c.translate(-38, 0)
        c.scale(max(0.05, hatch), 1)
        c.drawCircle(38, 0, 38, lin_paint(-38, -38, 38, 38, ["#E5E9F2", "#94A3B8"]))
        c.restore()
    else:
        c.drawCircle(0, 0, 16, P("#475569", 1, stroke=5))
        for an in (0, 60, 120):
            dx, dy = math.cos(math.radians(an)) * 16, math.sin(math.radians(an)) * 16
            c.drawLine(-dx, -dy, dx, dy, P("#475569", 1, stroke=4))
    c.restore()
    for i, px in enumerate((-90, 30, 150)):                                           # windows, and who is home
        c.drawCircle(px, -18, 30, P("#1B2238"))
        c.drawCircle(px, -18, 24, rad_paint(px, -18, 26, ["#FFE9B8", "#F5B861"]))
        if faces:
            bob = math.sin(t * 2 + i * 2) * 3
            c.drawCircle(px, -12 + bob, 11, P("#E8B48A"))
            c.drawArc(R(px - 13, -30 + bob, 26, 22), 180, 180, True, P("#FACC15"))
        c.drawCircle(px, -18, 24, P("#F8FAFC", 1, stroke=4))
    if cup > 0:                                                                      # the big window, facing down
        k = e_back(clamp(cup))
        c.save()
        c.translate(180, 92)
        c.scale(k, k)
        p = skia.Path()
        p.moveTo(-46, 0)
        p.lineTo(46, 0)
        p.lineTo(30, 44)
        p.lineTo(-30, 44)
        p.close()
        c.drawPath(p, P("#475569"))
        p2 = skia.Path()
        p2.moveTo(-38, 4)
        p2.lineTo(38, 4)
        p2.lineTo(25, 38)
        p2.lineTo(-25, 38)
        p2.close()
        c.drawPath(p2, lin_paint(0, 4, 0, 38, ["#FFE9B8", "#7DD3FC"]))
        for dx in (-13, 13):
            c.drawLine(dx, 4, dx * 0.7, 38, P("#475569", 1, stroke=3))
        c.drawCircle(0, 20, 9, P("#E8B48A"))
        c.drawArc(R(-11, 5, 22, 18), 180, 180, True, P("#FACC15"))
        c.restore()
    if hole > 0:                                                                     # a hole, and the air leaving through it
        c.drawCircle(-150, -93, 9, P("#0B1220"))
        for i in range(7):
            u = (t * 1.6 + i / 7) % 1.0
            puff(c, -150 - u * 150 + math.sin(i * 7) * 30 * u, -100 - u * 190, 10 + 34 * u, "#E0F2FE", 0.8 * (1 - u) * hole, k=i)


def shop(c, x, y, s=1.0, a=1.0):
    """The nearest store, standing on the edge of the Earth."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    box(c, -46, -62, 92, 62, "#F8FAFC", r=4, a=a)
    c.drawRect(R(-10, -34, 22, 34), P("#7C5A3C", a))
    c.drawRect(R(-38, -40, 20, 20), P("#7DD3FC", a))
    c.drawRect(R(20, -40, 18, 20), P("#7DD3FC", a))
    for i in range(6):
        c.drawRect(R(-52 + i * 17.4, -80, 17.4, 20), P("#EF4444" if i % 2 == 0 else "#FFFFFF", a))
    c.drawRRect(rr(-52, -84, 104, 6, 3), P("#B91C1C", a))
    c.restore()


def junk(c, kind, x, y, rot, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if kind == 0:                                                                    # a wrench
        c.drawRRect(rr(-30, -5, 60, 10, 4), P("#CBD5E1", a))
        c.drawCircle(-30, 0, 11, P("#CBD5E1", a))
        c.drawCircle(-34, 0, 5, P("#1B2238", a))
    elif kind == 1:                                                                  # a sandwich
        c.drawRRect(rr(-24, -14, 48, 10, 4), P("#E7B872", a))
        c.drawRRect(rr(-26, -5, 52, 7, 3), P("#22C55E", a))
        c.drawRRect(rr(-24, 2, 48, 10, 4), P("#E7B872", a))
    elif kind == 2:                                                                  # a laptop
        c.drawRRect(rr(-30, -24, 60, 38, 4), P("#475569", a))
        c.drawRRect(rr(-26, -20, 52, 30, 2), P("#7DD3FC", a))
        c.drawRRect(rr(-36, 14, 72, 7, 3), P("#94A3B8", a))
    elif kind == 3:                                                                  # a rubber duck
        c.drawOval(R(-22, -8, 44, 28), P("#FACC15", a))
        c.drawCircle(14, -14, 13, P("#FACC15", a))
        c.drawOval(R(24, -16, 14, 7), P("#F97316", a))
        c.drawCircle(17, -17, 2.5, P("#111827", a))
    else:                                                                            # a spoon
        c.drawRRect(rr(-28, -3, 40, 6, 3), P("#E5E9F2", a))
        c.drawOval(R(8, -9, 24, 18), P("#E5E9F2", a))
    c.restore()


def strap(c, x, y, k, w=84):
    if k <= 0:
        return
    c.drawRRect(rr(x - w / 2 * k, y - 7, w * k, 14, 5), P("#F97316"))
    c.drawRRect(rr(x - 9, y - 10, 18, 20, 4), P("#E5E9F2", clamp(k * 2 - 1)))


def bubble_snd(seed=0):
    n = int(0.14 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 500 + 1400 * tt / 0.14 + seed * 70
    return sfx._norm(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * sfx._env(n, 0.004, 0.05), 0.7)


def zip_snd(seed=0):
    n = int(0.16 * sfx.SR)
    x = sfx._bp(sfx._rng(seed + 30).standard_normal(n), 1800, 7000) * np.linspace(0.3, 1.0, n) ** 2
    return sfx._norm(x * sfx._ar(n, 0.01, 0.02), 0.7)


def vent_snd(d=1.4, seed=5):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 900, 6000)
    return sfx._norm(x * sfx._ar(n, 0.02, d * 0.7), 0.6)


# ====================================================================================== the episode
class Station(EpisodeV2):
    BUILD_NO = 15
    FIRST_SET = "space"
    CLEAR = "#05081A"
    TITLE = {"en": "SPACE STATION", "ar_sa": "محطة فضاء"}
    EMPH = {"en": ["CONGRATS", "STATION", "ORBIT", "BREATH", "POISONS", "OXYGEN", "SCRUBBERS", "WATER", "STORE", "DOWN", "FILTERS", "DISTILLER", "PEE",
                   "COFFEE", "MUSCLES", "BONES", "TREADMILL", "VACUUM", "SPECK", "PAINT", "SHIELDS", "ALUMINUM", "BULLETPROOF", "FOLLOW", "BRIDGE",
                   "SOLAR", "WINDOW", "EVERYTHING", "SIXTEEN", "ZERO", "YOURSELF", "TOILET", "BELT", "CAREFULLY"],
            "ar_sa": ["مبروك", "محطة", "المدار", "نفَسك", "يسمّم", "أكسجين", "وفلاتر", "الموية", "بقالة", "تحتك", "فلاتر", "تقطير", "بولك", "قهوة",
                      "وعضلاتك", "وعظامك", "سير", "الفراغ", "قشرة", "بوية", "بدروع", "ألمنيوم", "الرصاص", "تابعني", "جسر", "شمسية", "شباك", "شي",
                      "ستطعش", "وصفر", "بيدك", "والحمام", "أمان", "زين"]}
    KEYS = {"ar_sa": {
        ("hook", "SEAL"): "قفلت", ("hook", "ROOM"): "غرفة", ("hook", "THROW"): "ورميتها", ("hook", "ORBIT"): "المدار", ("hook", "CONGRATS"): "مبروك",
        ("break1", "BREATH"): "نفَسك", ("break1", "POISONS"): "يسمّم", ("break1", "AIR"): "الهوا", ("break1", "WEEKEND"): "الأسبوع",
        ("fix1", "MACHINE"): "جهاز", ("fix1", "SPLITS"): "يفصل", ("fix1", "WATER"): "الموية", ("fix1", "OXYGEN"): "أكسجين", ("fix1", "SCRUBBERS"): "وفلاتر",
        ("fix1", "TRAP"): "تمسك", ("fix1", "DIOXIDE"): "الكربون",
        ("break2", "BREATHE"): "تتنفس", ("break2", "WATER"): "الموية", ("break2", "OUT"): "تخلص", ("break2", "NEAREST"): "وأقرب", ("break2", "STORE"): "بقالة",
        ("break2", "HUNDRED"): "بأربعمية", ("break2", "DOWN"): "تحتك",
        ("fix2", "FILTERS"): "فلاتر", ("fix2", "DISTILLER"): "تقطير", ("fix2", "RECYCLE"): "وتعيد", ("fix2", "SWEAT"): "عرقك", ("fix2", "BREATH"): "ونفَسك",
        ("fix2", "PEE"): "بولك", ("fix2", "YESTERDAY"): "أمس", ("fix2", "TOMORROW"): "بكرة",
        ("break3", "FLOATING"): "الطفو", ("break3", "YEAR"): "سنة", ("break3", "BED"): "السرير", ("break3", "MUSCLES"): "وعضلاتك", ("break3", "BONES"): "وعظامك",
        ("break3", "WASTE"): "تضعف",
        ("fix3", "TREADMILL"): "سير", ("fix3", "BUNGEE"): "بحبال", ("fix3", "WEIGHT"): "تمارين", ("fix3", "PULLS"): "يسحب", ("fix3", "VACUUM"): "الفراغ",
        ("fix3", "WORK"): "وتتمرن", ("fix3", "TWO"): "ساعتين", ("fix3", "DAY"): "يوم",
        ("break4", "FIT"): "تمام", ("break4", "SPECK"): "قشرة", ("break4", "PAINT"): "بوية", ("break4", "HITS"): "تضرب", ("break4", "WALL"): "الجدار",
        ("break4", "THOUSAND"): "ألف", ("break4", "HOUR"): "الساعة",
        ("fix4", "WRAP"): "فتلف", ("fix4", "SHIELDS"): "بدروع", ("fix4", "ALUMINUM"): "ألمنيوم", ("fix4", "BUMPER"): "لوح", ("fix4", "SHATTERS"): "يفتت",
        ("fix4", "BULLETPROOF"): "الرصاص", ("fix4", "FABRIC"): "وقماش", ("fix4", "CATCHES"): "يمسك", ("fix4", "BITS"): "الفتات",
        ("cta", "FLOAT"): "تطير", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "UNFOLD"): "افرد", ("reveal", "WINGS"): "أجنحة", ("reveal", "WINDOW"): "شباك", ("reveal", "EARTH"): "الأرض", ("reveal", "TIE"): "واربط",
        ("reveal", "ABSOLUTELY"): "كل", ("reveal", "EVERYTHING"): "شي",
        ("stat", "ONE"): "محطة", ("stat", "SIXTEEN"): "ستطعش", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TOILET"): "والحمام", ("tag", "VACUUM"): "مكنسة", ("tag", "SEAT"): "حزام", ("tag", "AIM"): "وصوّب", ("tag", "CAREFULLY"): "زين"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a suspension bridge"),
                   "stat": [("1", "STATION"), ("16", "SUNRISES"), ("0", "SHOWERS")],
                   "L": {"orbit": "ORBIT", "air": "CLEAN AIR", "co2": "CO2", "o2": "MAKES OXYGEN", "scrub": "SCRUBBER", "water": "WATER",
                         "store": "NEAREST STORE", "km": "400 KM", "filters": "FILTERS", "dist": "DISTILLER", "coffee": "TOMORROW'S COFFEE",
                         "muscle": "MUSCLE", "bone": "BONE", "year": "A YEAR IN BED", "tread": "TREADMILL", "bungee": "BUNGEE STRAPS",
                         "vac": "VACUUM CYLINDERS", "hours": "2 HOURS A DAY", "speck": "A SPECK OF PAINT", "speed": "28,000 KM/H",
                         "bumper": "ALUMINUM BUMPER", "fabric": "BULLETPROOF FABRIC", "hull": "YOUR WALL", "wings": "SOLAR WINGS",
                         "window": "THE WINDOW", "aim": "AIM HERE", "out": "SPACE", "in": "INSIDE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: جسر معلق"),
                      "stat": [("1", "محطة"), ("16", "شروق"), ("0", "دش")],
                      "L": {"orbit": "المدار", "air": "هوا نظيف", "co2": "CO2", "o2": "يطلّع أكسجين", "scrub": "فلتر الكربون", "water": "الموية",
                            "store": "أقرب بقالة", "km": "أربعمية كيلو", "filters": "فلاتر", "dist": "جهاز تقطير", "coffee": "قهوة بكرة",
                            "muscle": "العضلات", "bone": "العظام", "year": "سنة في السرير", "tread": "سير مشي", "bungee": "حبال مطاط",
                            "vac": "اسطوانات فراغ", "hours": "ساعتين كل يوم", "speck": "قشرة بوية", "speed": "أسرع من الرصاصة بعشر مرات",
                            "bumper": "لوح ألمنيوم", "fabric": "قماش ضد الرصاص", "hull": "جدارك", "wings": "أجنحة شمسية",
                            "window": "الشباك", "aim": "صوّب هنا", "out": "الفضاء", "in": "داخل المحطة"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "seal": ("hook", "SEAL", 0.12), "room": ("hook", "ROOM", 0.22), "throw": ("hook", "THROW", 0.32), "orbit": ("hook", "ORBIT", 0.48),
            "congrats": ("hook", "CONGRATS", 0.58),
            "breath": ("break1", "BREATH", 0.28), "poisons": ("break1", "POISONS", 0.38), "air": ("break1", "AIR", 0.55), "weekend": ("break1", "WEEKEND", 0.9),
            "machine": ("fix1", "MACHINE", 0.2), "splits": ("fix1", "SPLITS", 0.3), "water": ("fix1", "WATER", 0.36), "oxygen": ("fix1", "OXYGEN", 0.5),
            "scrubbers": ("fix1", "SCRUBBERS", 0.66), "trap": ("fix1", "TRAP", 0.78), "dioxide": ("fix1", "DIOXIDE", 0.94),
            "breathe": ("break2", "BREATHE", 0.14), "water2": ("break2", "WATER", 0.32), "out": ("break2", "OUT", 0.42), "nearest": ("break2", "NEAREST", 0.54),
            "store": ("break2", "STORE", 0.6), "hundred": ("break2", "HUNDRED", 0.72), "down": ("break2", "DOWN", 0.95),
            "filters": ("fix2", "FILTERS", 0.12), "distiller": ("fix2", "DISTILLER", 0.24), "recycle": ("fix2", "RECYCLE", 0.34), "sweat": ("fix2", "SWEAT", 0.42),
            "breath2": ("fix2", "BREATH", 0.5), "pee": ("fix2", "PEE", 0.6), "yesterday": ("fix2", "YESTERDAY", 0.68), "tomorrow": ("fix2", "TOMORROW", 0.86),
            "floating": ("break3", "FLOATING", 0.1), "year": ("break3", "YEAR", 0.3), "bed": ("break3", "BED", 0.42), "muscles": ("break3", "MUSCLES", 0.62),
            "bones": ("break3", "BONES", 0.76), "waste": ("break3", "WASTE", 0.86),
            "treadmill": ("fix3", "TREADMILL", 0.16), "bungee": ("fix3", "BUNGEE", 0.26), "weight": ("fix3", "WEIGHT", 0.4), "pulls": ("fix3", "PULLS", 0.54),
            "vacuum": ("fix3", "VACUUM", 0.64), "work": ("fix3", "WORK", 0.76), "two": ("fix3", "TWO", 0.82), "day": ("fix3", "DAY", 0.95),
            "fit": ("break4", "FIT", 0.14), "speck": ("break4", "SPECK", 0.3), "paint": ("break4", "PAINT", 0.38), "hits": ("break4", "HITS", 0.44),
            "wall": ("break4", "WALL", 0.52), "thousand": ("break4", "THOUSAND", 0.68), "hour": ("break4", "HOUR", 0.94),
            "wrap": ("fix4", "WRAP", 0.1), "shields": ("fix4", "SHIELDS", 0.24), "aluminum": ("fix4", "ALUMINUM", 0.36), "bumper": ("fix4", "BUMPER", 0.42),
            "shatters": ("fix4", "SHATTERS", 0.5), "bulletproof": ("fix4", "BULLETPROOF", 0.68), "fabric": ("fix4", "FABRIC", 0.76),
            "catches": ("fix4", "CATCHES", 0.84), "bits": ("fix4", "BITS", 0.95),
            "float": ("cta", "FLOAT", 0.22), "follow": ("cta", "FOLLOW", 0.4),
            "unfold": ("reveal", "UNFOLD", 0.12), "wings": ("reveal", "WINGS", 0.26), "window": ("reveal", "WINDOW", 0.42), "earth": ("reveal", "EARTH", 0.55),
            "tie": ("reveal", "TIE", 0.64), "absolutely": ("reveal", "ABSOLUTELY", 0.76), "everything": ("reveal", "EVERYTHING", 0.9),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "SIXTEEN", 0.36), "s3": ("stat", "ZERO", 0.72),
            "cong2": ("closer", "CONGRATS", 0.16),
            "toilet": ("tag", "TOILET", 0.16), "vacuum2": ("tag", "VACUUM", 0.36), "seat": ("tag", "SEAT", 0.62), "aim": ("tag", "AIM", 0.8),
            "carefully": ("tag", "CAREFULLY", 0.92)})
        T["dry"] = max(T["out"], T["water2"]) + 0.1                    # the tank is empty
        T["storecut"] = T["nearest"] - 0.3
        T["speck0"] = min(T["speck"], T["hits"]) - 0.35                # the speck shows up
        T["impact"] = max(T["hits"], T["paint"]) + 0.12                # ...and goes through the wall
        T["bump0"] = min(T["aluminum"], T["bumper"])
        T["fab0"] = min(T["bulletproof"], T["fabric"])
        T["wallcut"] = T["bump0"] - 0.35
        T["tiecut"] = T["tie"] - 0.35
        self.cut(s("break1") - 0.1, "inside", 1)
        self.cut(s("fix1") - 0.12, "inside", 1)
        self.cut(s("break2") - 0.1, "inside", -1)
        self.cut(T["storecut"], "space", -1)
        self.cut(s("fix2") - 0.12, "inside", 1)
        self.cut(s("break3") - 0.1, "inside", -1)
        self.cut(s("fix3") - 0.12, "inside", 1)
        self.cut(s("break4") - 0.12, "space", -1)
        self.cut(T["wallcut"], "wall", 1)
        self.cut(s("cta") + 0.05, "inside", -1)
        self.cut(s("reveal") - 0.1, "space", 1)
        self.cut(T["tiecut"], "inside", -1)
        self.cut(T["s1"] - 0.35, "space", 1)
        self.cut(s("tag") - 0.2, "inside", -1)
        sc = Camera(0, 170, 0.9)                                       # outside
        sc.key(0.05, -60, 185, 0.95, 0.5).key(T["throw"] - 0.2, 0, 120, 1.2, max(0.6, T["orbit"] - T["throw"] + 0.5))
        sc.key(T["storecut"], 0, 640, 0.7, 0.0)
        sc.key(s("break4") - 0.12, -40, 150, 1.15, 0.0).key(T["impact"] + 0.2, -70, 120, 1.3, 0.8)
        sc.key(s("fix4") - 0.1, 0, 150, 1.2, 0.6)
        sc.key(s("reveal") - 0.1, 0, 210, 0.95, 0.0).key(T["window"] - 0.35, 110, 110, 1.25, 0.7)
        sc.key(T["s1"] - 0.35, 0, 206, 0.62, 0.0).key(s("closer"), 0, 190, 0.68, 2.4)
        self.scam = sc
        self.limb = (Track(1290.0).to(T["storecut"], 1120.0, 0.01).to(s("break4") - 0.12, 1300.0, 0.01).to(s("reveal") - 0.1, 1260.0, 0.01)
                     .to(T["window"] - 0.35, 1330.0, 0.7).to(T["s1"] - 0.35, 1190.0, 0.01))
        ic = Camera(0, -175, 1.55)                                     # inside
        ic.key(s("break1") - 0.1, 0, -185, 1.45, 0.0).key(T["poisons"], 0, -175, 1.55, 1.2)
        ic.key(s("fix1") - 0.12, -350, -142, 1.9, 0.0)
        ic.key(s("break2") - 0.1, -390, -128, 2.1, 0.0).key(T["water2"] - 0.4, -430, -112, 2.4, 0.8)
        ic.key(s("fix2") - 0.12, 40, -126, 2.15, 0.0).key(T["yesterday"] - 0.5, 70, -126, 2.15, 0.8)
        ic.key(s("break3") - 0.1, 0, -175, 1.55, 0.0)
        ic.key(s("fix3") - 0.12, 370, -142, 1.9, 0.0)
        ic.key(s("cta") + 0.05, 30, -175, 1.55, 0.0)
        ic.key(T["tiecut"], 0, -175, 1.55, 0.0)
        ic.key(s("tag") - 0.2, -150, -123, 2.2, 0.0).key(T["aim"] - 0.3, -146, -108, 2.5, 0.6)
        self.icam = ic
        self.wl = Track(1.0).to(T["breathe"] + 0.2, 0.0, max(0.5, T["dry"] - T["breathe"] - 0.2)).to(T["recycle"], 1.0, 1.5)
        self.clean = Track(0.0).to(T["recycle"] + 0.3, 1.0, max(0.8, T["yesterday"] - T["recycle"]))
        self.haze = Track(0.0).to(T["breath"] - 0.2, 1.0, max(0.6, T["weekend"] - T["breath"])).to(T["trap"] - 0.1, 0.0, max(0.5, T["dioxide"] - T["trap"] + 0.3))
        self.body = Track(1.0).to(T["muscles"] - 0.2, 0.4, max(0.5, T["waste"] - T["muscles"] + 0.5)).to(T["work"], 1.0, max(0.5, T["day"] - T["work"]))
        self.spans = [(T["poisons"], T["dioxide"]), (T["dry"], T["tomorrow"]), (T["waste"], T["day"]), (T["impact"], T["bits"])]
        self.shakes = [(T["seal"], 0.15, 5), (T["poisons"], 0.25, 6), (T["dry"], 0.25, 6), (T["impact"], 0.5, 18), (T["shatters"], 0.3, 12),
                       (T["everything"], 0.2, 6)]

    # ------------------------------------------------------------------ set: outside
    def draw_space(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.scam.at(t)
        cam = (cam[0] + math.sin(t * 0.5) * 4, cam[1] + math.cos(t * 0.4) * 3, cam[2])
        limb = self.limb.at(t)
        v2.sky(c, W, H, 1.0)
        v2.stars(c, W, H, t, 1.0)
        statv = t >= T["s1"] - 0.35
        if statv:                                                                    # sixteen sunrises a day
            u = (t * 1.25) % 1.0
            add_glow(c, W * 0.86, limb + 40 - 90 * math.sin(math.pi * u), 420, "#FFD27A", 0.9 * math.sin(math.pi * u))
            add_glow(c, W * 0.86, limb + 40 - 90 * math.sin(math.pi * u), 150, "#FFFFFF", 0.9 * math.sin(math.pi * u))
        v2.earth_limb(c, W, H, 1.0, y=limb)
        store = T["storecut"] <= t < s("fix2") - 0.12
        if store:
            sk = e_back(prog(t, T["store"] - 0.25, T["store"] + 0.05))
            shop(c, W / 2, limb + 6, 1.5 * sk)
            lk = prog(t, T["store"] - 0.1, max(T["down"], T["hundred"]) - 0.1)
            sx, sy = self.to_screen(cam, 0, 100)
            if lk > 0:
                c.drawLine(sx, sy, sx, lerp(sy, limb - 126, lk), dash_paint("#FFFFFF", 0.9, 5, t, dash=16, gap=14))
                if lk >= 1:
                    for dx in (-14, 14):
                        c.drawLine(sx, limb - 124, sx + dx, limb - 146, P("#FFFFFF", 0.9, stroke=5))
        self.view(c, cam)
        hook = t < s("break1") - 0.1
        if hook:
            u = e_out(prog(t, T["throw"] - 0.25, T["orbit"] + 0.1))
            px, py = lerp(-230, 0, u), lerp(330, 0, u) - 110 * math.sin(math.pi * u)
            rot = lerp(-22, -360, e_io(prog(t, T["throw"] - 0.25, T["orbit"] + 0.2)))
            if u >= 1:                                                               # the orbit it now rides
                ok = prog(t, T["orbit"] + 0.1, T["orbit"] + 0.7)
                c.drawArc(R(-2600, -40, 5200, 5200), 270 - 14 * ok, 28 * ok, False, dash_paint("#7DD3FC", 0.75, 5, t, dash=22, gap=16))
            if 0 < u < 1:
                for i in range(5):
                    uu = max(0.0, u - 0.05 * (i + 1))
                    qx, qy = lerp(-230, 0, uu), lerp(330, 0, uu) - 110 * math.sin(math.pi * uu)
                    c.drawCircle(qx, qy, 60 - i * 9, P("#FFFFFF", 0.10))
            c.save()
            c.translate(px, py)
            c.rotate(rot)
            k = e_back(prog(t, 0.05, 0.4))
            c.scale(k, k)
            station(c, t, hatch=prog(t, T["seal"] - 0.3, T["seal"]))
            c.restore()
        else:
            holed = T["impact"] <= t < T["wallcut"]
            late = t >= s("reveal") - 0.1
            station(c, t, wings=e_io(prog(t, T["unfold"] - 0.1, T["wings"] + 0.4)) if late else 0.0,
                    cup=prog(t, T["window"] - 0.2, T["window"] + 0.15) if late else 0.0,
                    shield=1.0 if late else prog(t, T["wrap"] - 0.1, min(T["shields"] + 0.5, T["wallcut"] - 0.05)) if t >= s("fix4") - 0.1 else 0.0,
                    hole=1.0 if holed else 0.0)
            if T["speck0"] <= t < T["impact"] + 0.5:                                   # the speck: a slow look, then gone
                if t < T["impact"] - 0.14:
                    wob = math.sin(t * 20) * 2
                    c.drawCircle(-470 + wob, -300, 7, P("#F87171"))
                    c.drawCircle(-470 + wob, -300, 16, P("#FFFFFF", 0.5, stroke=2))
                else:
                    u = prog(t, T["impact"] - 0.14, T["impact"])
                    x1, y1 = lerp(-470, -150, u), lerp(-300, -95, u)
                    c.drawLine(-470, -300, x1, y1, P("#FFFFFF", 0.9 * (1 - prog(t, T["impact"], T["impact"] + 0.4)), stroke=5))
                    if u >= 1:
                        v2.shock_ring(c, -150, -95, t, T["impact"], 0.5, r1=260, col="#FFFFFF", width=14, squash=1.0)
                        sparks_shower(c, -150, -95, t, T["impact"], 0.6, n=20, speed=600, seed=4, cone=(180, 360))
        c.restore()
        self.ui["cam"] = cam
        self.ui["limb"] = limb

    # ------------------------------------------------------------------ set: inside
    def cabin(self, c, t):
        c.drawRRect(rr(-560, -450, 1120, 490, 80), lin_paint(0, -450, 0, 40, ["#B4BFD0", "#7C8AA3", "#56627C"]))
        c.drawRRect(rr(-560, -450, 1120, 490, 80), P("#FFFFFF", 0.35, stroke=3))
        c.drawRRect(rr(-524, -414, 1048, 418, 56), lin_paint(0, -414, 0, 4, ["#26375C", "#1D2A49", "#162038"]))
        for px in range(-440, 520, 110):
            c.drawRect(R(px, -414, 2, 418), P("#000000", 0.16))
        c.drawRect(R(-524, -24, 1048, 28), P("#111A30"))
        for px in (-250, 20, 250):                                                    # portholes
            c.drawCircle(px, -318, 38, P("#94A3B8"))
            c.drawCircle(px, -318, 30, rad_paint(px + 10, -300, 44, ["#1D4ED8", "#0B1E4D", "#050B22"]))
            for i in range(4):
                c.drawCircle(px - 16 + i * 9, -332 + (i * 7) % 13, 1.4, P("#FFFFFF", 0.8))
        for px in (-380, -120, 130, 400):                                             # handrails
            c.drawRRect(rr(px, -396, 70, 8, 4), P("#FACC15"))
        for lx in (-200, 200):
            c.drawRRect(rr(lx - 50, -410, 100, 10, 5), P("#FFF3C4"))
            add_glow(c, lx, -380, 300, "#FFE9B8", 0.18)

    def draw_inside(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.icam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1] + math.cos(t * 0.5) * 2, cam[2])
        v2.sky(c, W, H, 1.0)
        v2.stars(c, W, H, t, 0.9)
        self.view(c, cam)
        self.cabin(c, t)
        seg = self.seg(t)
        self.machines(c, t, seg)
        self.crew_in(c, t, seg)
        hz = self.haze.at(t)
        if hz > 0:                                                                   # the air going bad
            rng = random.Random(6)
            sucked = prog(t, T["trap"] - 0.1, T["dioxide"] + 0.3) if t >= s("fix1") - 0.12 else 0.0
            for i in range(26):
                hx, hy, hr = rng.uniform(-480, 480), rng.uniform(-380, -40), rng.uniform(36, 80)
                if i / 26 > hz and sucked <= 0:
                    continue
                hx, hy = lerp(hx, SCR, e_in(sucked)), lerp(hy, -120, e_in(sucked))
                puff(c, hx + math.sin(t * 0.8 + i) * 14, hy + math.cos(t * 0.7 + i) * 10, hr * (1 - 0.6 * sucked), CO2C, 0.36 * (1 - sucked), k=i)
        c.restore()
        self.ui["cam"] = cam

    def seg(self, t):
        s, T = self.tl.s, self.T
        for name, t0 in (("tag", s("tag") - 0.2), ("tie", T["tiecut"]), ("cta", s("cta") + 0.05), ("gym", s("fix3") - 0.12), ("bed", s("break3") - 0.1),
                         ("recycle", s("fix2") - 0.12), ("dry", s("break2") - 0.1), ("air", s("fix1") - 0.12), ("breath", 0.0)):
            if t >= t0:
                return name

    def machines(self, c, t, seg):
        T, s = self.T, self.tl.s
        # ---- the oxygen maker
        k = e_back(prog(t, T["machine"] - 0.2, T["machine"] + 0.1))
        if k > 0:
            wl = self.wl.at(t)
            c.save()
            c.translate(OX, 0)
            c.scale(k, k)
            box(c, -64, -184, 128, 184, "#475569", r=12)
            c.drawRRect(rr(-50, -164, 100, 112, 10), P("#0B1220"))
            c.drawRRect(rr(-46, -56 - 104 * wl, 92, 104 * wl, 8), P("#38BDF8", 0.75))
            for ex in (-22, 22):
                c.drawRect(R(ex - 3, -156, 6, 96), P("#E5E9F2"))
            run = t >= T["splits"] - 0.1 and wl > 0.05
            if run:
                for i in range(10):
                    u = (t * 0.9 + i / 10) % 1.0
                    ex = -22 if i % 2 == 0 else 22
                    by = lerp(-62, -56 - 100 * wl, u)
                    c.drawCircle(ex + math.sin(t * 5 + i) * 5, by, 4 + (i % 3), P("#FFFFFF" if i % 2 == 0 else "#FDE68A", 0.9))
            c.drawRRect(rr(-50, -164, 100, 112, 10), P("#CBD5E1", 1, stroke=3))
            c.drawRRect(rr(-40, -38, 80, 22, 6), P("#0B1220"))
            c.drawCircle(-26, -27, 6, P(GOOD if run else "#EF4444"))
            c.restore()
            if run and t >= T["oxygen"] - 0.4:                                          # oxygen into the cabin
                for i in range(7):
                    u = (t * 0.45 + i / 7) % 1.0
                    bx, by = OX - 22 + u * 150 + math.sin(t * 2 + i) * 14, -190 - u * 150
                    c.drawCircle(bx, by, 9 + 5 * math.sin(i), P(O2C, 0.55 * math.sin(math.pi * u)))
                    c.drawCircle(bx, by, 9 + 5 * math.sin(i), P("#FFFFFF", 0.8 * math.sin(math.pi * u), stroke=2))
        # ---- the scrubber
        k = e_back(prog(t, T["scrubbers"] - 0.2, T["scrubbers"] + 0.1))
        if k > 0:
            c.save()
            c.translate(SCR, 0)
            c.scale(k, k)
            box(c, -50, -160, 100, 160, "#64748B", r=16)
            fan(c, 0, -116, 30, t * 500)
            c.drawRRect(rr(-34, -72, 68, 54, 8), P("#0B1220"))
            got = prog(t, T["trap"], T["dioxide"] + 0.4)
            rng = random.Random(2)
            for i in range(int(16 * got)):
                c.drawCircle(rng.uniform(-28, 28), rng.uniform(-66, -24), 5, P(CO2C, 0.9))
            for gx in range(-30, 34, 9):
                c.drawLine(gx, -72, gx, -18, P("#94A3B8", 0.6, stroke=1.5))
            c.restore()
        # ---- the toilet
        box(c, TOI - 34, -64, 68, 64, "#F1F5F9", r=10)
        c.drawOval(R(TOI - 22, -70, 44, 14), P("#1B2238"))
        c.drawRRect(rr(TOI + 30, -100, 12, 60, 6), P("#CBD5E1"))
        c.drawLine(TOI + 36, -96, TOI + 58, -128, P("#FACC15", 1, stroke=8))
        cone = skia.Path()
        cone.moveTo(TOI + 50, -142)
        cone.lineTo(TOI + 74, -130)
        cone.lineTo(TOI + 58, -122)
        cone.close()
        c.drawPath(cone, P("#FACC15"))
        # ---- the recycler
        fk = e_back(prog(t, T["filters"] - 0.2, T["filters"] + 0.1))
        dk = e_back(prog(t, T["distiller"] - 0.2, T["distiller"] + 0.1))
        pk = prog(t, T["recycle"] - 0.2, T["recycle"] + 0.3)
        cl = self.clean.at(t)
        if pk > 0:                                                                   # pipes: toilet -> drum -> filters -> tank; cabin air -> drum
            pp = P("#94A3B8", pk, stroke=9)
            pp.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawLine(TOI + 34, -30, DRUM - 44, -30, pp)
            c.drawLine(DRUM, -116, DRUM, -400, pp)
            c.drawLine(DRUM + 44, -30, TANK - 30, -30, pp)
            flow = t >= T["sweat"] - 0.1
            if flow:
                for i in range(4):
                    u = (t * 0.9 + i / 4) % 1.0
                    c.drawCircle(DRUM + math.sin(i * 5) * 2, lerp(-400, -120, u), 5, P("#BAE6FD", 0.95))
                    if t >= T["pee"] - 0.1:
                        c.drawCircle(lerp(TOI + 34, DRUM - 44, u), -30, 5, P("#FACC15"))
                    c.drawCircle(lerp(DRUM + 44, TANK - 30, u), -30, 5, P("#38BDF8"))
        if dk > 0:
            c.save()
            c.translate(DRUM, -70)
            c.scale(dk, dk)
            c.drawCircle(0, 0, 48, lin_paint(-48, -48, 48, 48, ["#E5E9F2", "#94A3B8", "#475569"]))
            c.drawCircle(0, 0, 38, P("#0B1220"))
            c.rotate(t * 240 if t >= T["recycle"] - 0.1 else 0)
            for i in range(3):
                c.drawArc(R(-30, -30, 60, 60), i * 120, 70, False, P("#7DD3FC", 1, stroke=7))
            c.drawCircle(0, 0, 8, P("#E5E9F2"))
            c.restore()
        if fk > 0:
            for i, (fx_, col) in enumerate(((74, "#22C55E"), (104, "#F59E0B"), (134, "#A78BFA"))):
                kk = e_back(clamp(fk * 1.4 - i * 0.2))
                c.drawRRect(rr(fx_ - 11 * kk, -128, 22 * kk, 100, 10), lin_paint(fx_ - 11, 0, fx_ + 11, 0, ["#F8FAFC", "#94A3B8"]))
                c.drawRRect(rr(fx_ - 7 * kk, -116, 14 * kk, 76, 6), P(col, 0.9))
        if pk > 0:
            box(c, TANK - 30, -134, 60, 134, "#475569", r=10, a=pk)
            c.drawRRect(rr(TANK - 22, -124, 44, 112, 6), P("#0B1220", pk))
            c.drawRRect(rr(TANK - 20, -14 - 108 * cl, 40, 108 * cl, 5), P("#38BDF8", 0.85 * pk))
            c.drawRRect(rr(TANK + 30, -96, 26, 10, 4), P("#94A3B8", pk))
        # ---- the gym
        tk = e_back(prog(t, T["treadmill"] - 0.2, T["treadmill"] + 0.1))
        if tk > 0:
            c.save()
            c.translate(TREAD, 0)
            c.scale(tk, tk)
            box(c, -86, -24, 172, 24, "#334155", r=10)
            off = (t * 160) % 24 if t >= T["bungee"] - 0.1 else 0
            c.save()
            c.clipRRect(rr(-80, -24, 160, 9, 4))
            for i in range(-1, 9):
                c.drawRect(R(-80 + i * 24 - off, -24, 12, 9), P("#94A3B8"))
            c.restore()
            c.drawLine(70, -24, 84, -120, P("#94A3B8", 1, stroke=7))
            c.drawRRect(rr(58, -128, 40, 10, 5), P("#CBD5E1"))
            c.restore()
        ak = e_back(prog(t, T["weight"] - 0.2, T["weight"] + 0.1))
        if ak > 0:
            lift = 0.5 + 0.5 * math.sin(t * 4.2) if t >= T["pulls"] - 0.1 else 0.0
            c.save()
            c.translate(ARED, 0)
            c.scale(ak, ak)
            box(c, -62, -12, 124, 12, "#334155", r=5)
            for cx_ in (-48, 48):
                c.drawRRect(rr(cx_ - 11, -118, 22, 106, 8), lin_paint(cx_ - 11, 0, cx_ + 11, 0, ["#E5E9F2", "#64748B"]))
                c.drawRect(R(cx_ - 4, -150 - 44 * lift, 8, 40 + 44 * lift), P("#F8FAFC"))
            c.drawRRect(rr(-62, -160 - 44 * lift, 124, 12, 6), P("#F59E0B"))
            c.restore()
            self.ui["lift"] = lift

    def crew_in(self, c, t, seg):
        T, s = self.T, self.tl.s
        b = lambda i, a=8: math.sin(t * 1.3 + i * 2.1) * a                           # a slow bob
        if seg == "breath":
            dizzy = self.haze.at(t) > 0.55
            for i, (px, py, an) in enumerate(((-170, -205, -10), (0, -232, 8), (170, -200, -5))):
                floaty(c, px + b(i, 5), py + b(i + 3), an + b(i, 4) + (math.sin(t * 3 + i) * 14 if dizzy else 0), SHIRTS[i], t + i, "duck" if dizzy else "look")
                if t >= T["breath"] - 0.3:
                    u = (t * 0.8 + i * 0.3) % 1.0
                    puff(c, px + 30 + u * 46, py - 30 - u * 30, 8 + 16 * u, CO2C, 0.8 * (1 - u), k=i)
        elif seg in ("air", "dry"):
            ok = t >= T["dioxide"] and seg == "air"
            floaty(c, -180 + b(0, 5), -250 + b(1), 8 + b(2, 4), SHIRTS[1], t, "cheer" if ok else "point" if seg == "air" else "shrug", face=-1)
        elif seg == "recycle":
            got = prog(t, T["tomorrow"] - 0.35, T["tomorrow"] + 0.1)
            floaty(c, 262 + b(0, 4), -215 + b(1, 6), -6 + b(2, 3), SHIRTS[0], t, "cheer" if got >= 1 else "look", face=-1)
            floaty(c, -40 + b(3, 5), -285 + b(4, 6), 12 + b(5, 4), SHIRTS[2], t + 1, "look", face=1)
            if t >= T["sweat"] - 0.2:                                                # sweat and breath, heading for the vent
                for i in range(4):
                    u = (t * 0.7 + i / 4) % 1.0
                    c.drawOval(R(lerp(-30, DRUM, u) - 4, lerp(-330, -398, u) - 6, 8, 12), P("#BAE6FD", 1 - u))
            ck = e_back(prog(t, T["yesterday"] - 0.2, T["yesterday"] + 0.1))
            if ck > 0:                                                               # the coffee pouch
                fx_, fy = lerp(TANK + 64, 228, e_io(got)), lerp(-92, -246, e_io(got))
                c.save()
                c.translate(fx_, fy)
                c.rotate(-10 + 14 * math.sin(t * 2))
                c.scale(ck, ck)
                c.drawRRect(rr(-17, -22, 34, 44, 7), P("#E5E9F2"))
                c.drawRRect(rr(-13, -10, 26, 28, 5), P("#7C4A1E"))
                c.drawRect(R(-3, -36, 6, 16), P("#F8FAFC"))
                c.restore()
        elif seg == "bed":
            weak = 1 - self.body.at(t)
            for i, (px, py, an) in enumerate(((-190, -150, 84), (10, -260, 96), (200, -170, 80))):
                floaty(c, px + b(i, 6), py + b(i + 2, 8), an + b(i, 3), SHIRTS[i], t * 0.4 + i, "stand")
                for j in range(2):
                    u = (t * 0.5 + j * 0.5 + i * 0.3) % 1.0
                    text(c, "z", px + 40 + u * 40, py - 50 - u * 50, 26 + 22 * u, "#FFFFFF", "Poppins-Black", a=0.9 * (1 - u))
        elif seg == "gym":
            run = t >= T["bungee"] - 0.1
            rx = lerp(TREAD - 30, TREAD - 6, prog(t, T["treadmill"], T["bungee"]))
            if run:                                                                  # the straps that hold him down
                for dx in (-70, 58):
                    zz = skia.Path()
                    zz.moveTo(rx, -92)
                    n = 7
                    for i in range(1, n + 1):
                        zz.lineTo(lerp(rx, TREAD + dx, i / n) + (5 if i % 2 else -5), lerp(-92, -26, i / n))
                    c.drawPath(zz, P("#F97316", 1, stroke=5))
                engineer(c, rx, -24 - abs(math.sin(t * 11)) * 5, 116, SHIRTS[0], t * 1.8, "walk", face=1)
                c.drawRRect(rr(rx - 20, -98, 40, 10, 4), P("#F97316"))
            else:
                floaty(c, rx, -150 + b(0, 6), 14 + b(1, 4), SHIRTS[0], t, "look")
            lift = self.ui.get("lift", 0.0)
            if t >= T["weight"] - 0.1:
                engineer(c, ARED, -12 - 30 * lift * 0.5, 112, SHIRTS[2], t, "cheer", face=-1)
            floaty(c, 372 + b(2, 5), -310 + b(3, 6), -8 + b(4, 4), SHIRTS[1], t + 2, "cheer" if t >= T["day"] else "look", face=1)
        elif seg == "cta":
            u = e_in(prog(t, s("cta") + 0.2, T["pause"] if T["pause"] > s("cta") else s("cta") + 3)) if False else prog(t, s("cta") + 0.1, s("cta") + 4.0)
            floaty(c, -160 + b(0, 4), -205 + b(1, 5), -6 + b(2, 3), SHIRTS[0], t, "point", face=1)
            floaty(c, 10 + b(3, 4), -225 + b(4, 5), 8 + b(5, 3), SHIRTS[1], t + 1, "look", face=1)
            floaty(c, lerp(150, 330, u), lerp(-200, -360, u), lerp(10, 170, u), SHIRTS[2], t + 2, "cheer", face=1)
        elif seg == "tie":
            items = ((0, -270, -300, T["tie"]), (1, -190, -175, T["tie"] + 0.25), (2, 190, -305, T["absolutely"]), (3, 262, -185, T["absolutely"] + 0.3),
                     (4, -70, -345, T["everything"]))
            for kind, hx, hy, t0 in items:
                k = e_back(prog(t, t0 - 0.12, t0 + 0.08))
                fx_ = hx + (1 - clamp(k)) * math.sin(t * 1.5 + kind) * 46
                fy = hy + (1 - clamp(k)) * math.cos(t * 1.2 + kind * 2) * 30
                c.save()
                c.translate(fx_, fy)
                c.scale(1.5, 1.5)
                junk(c, kind, 0, 0, (1 - clamp(k)) * (t * 60 + kind * 50))
                c.restore()
                strap(c, hx, hy, k, w=110)
            sk = e_back(prog(t, T["everything"] + 0.25, T["everything"] + 0.45))             # and the last thing left floating
            floaty(c, 30 + b(0, 9) * (1 - clamp(sk)), -215 + b(1, 9) * (1 - clamp(sk)), 8 * (1 - clamp(sk)), SHIRTS[1], t, "shrug" if sk > 0.5 else "look", face=1)
            strap(c, 30, -205, sk, w=130)
        elif seg == "tag":
            sit = e_io(prog(t, T["seat"] - 0.45, T["seat"] - 0.1))
            px, py = lerp(TOI - 70, TOI, sit), lerp(-170, -64, sit)
            if sit < 1:
                floaty(c, px + b(0, 3), py - 59 + b(1, 4), lerp(-14, 0, sit), SHIRTS[0], t, "look", face=1)
            else:
                engineer(c, TOI, -64, 112, SHIRTS[0], t, "sit", face=1)
                bk = e_back(prog(t, T["seat"] - 0.1, T["seat"] + 0.1))
                c.drawRRect(rr(TOI - 40 * bk, -92, 80 * bk, 12, 5), P("#F97316"))
                c.drawRRect(rr(TOI - 9, -96, 18, 20, 4), P("#E5E9F2", clamp(bk)))
            if t >= T["vacuum2"] - 0.2:                                              # it pulls
                for i in range(5):
                    u = (t * 1.8 + i / 5) % 1.0
                    c.drawLine(TOI + 96 - u * 30, -150 + i * 4 - u * 4, TOI + 84 - u * 30, -146 + i * 4 - u * 4, P("#FFFFFF", 0.8 * (1 - u), stroke=3))

    # ------------------------------------------------------------------ set: a slice of the hull
    def draw_wall(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 1.0)
        v2.stars(c, W, H, t, 1.0)
        y0, y1, ym = 330, 1230, 760
        c.drawRect(R(690, y0, W - 690, y1 - y0), lin_paint(0, y0, 0, y1, ["#26375C", "#162038"]))            # the cabin
        engineer(c, 880, y1 - 40, 300, SHIRTS[1], t, "cheer" if t >= T["bits"] - 0.1 else "duck" if t >= T["shatters"] - 0.2 else "look", face=-1)
        c.drawRect(R(630, y0, 60, y1 - y0), lin_paint(630, 0, 690, 0, ["#E5E9F2", "#94A3B8", "#64748B"]))       # the wall itself
        fk = 1.0
        hit = prog(t, T["shatters"] + 0.28, T["shatters"] + 0.5)                       # the bits reach the fabric
        for i in range(6):                                                           # the fabric
            fx_ = 470 + i * 17
            bulge = math.exp(-((0) ** 2)) * 0
            p = skia.Path()
            p.moveTo(fx_, y0)
            for yy in range(y0, y1 + 1, 30):
                d = abs(yy - ym) / 150
                p.lineTo(fx_ + 22 * math.exp(-d * d) * bump(t, T["shatters"] + 0.28, T["shatters"] + 0.9) * (1 - i / 7), yy)
            c.drawPath(p, P("#EAB308" if i % 2 == 0 else "#CA8A04", fk, stroke=13))
        for yy in range(y0, y1, 22):
            c.drawLine(462, yy, 566, yy + 11, P("#713F12", 0.35, stroke=2))
        for yy in (y0 + 60, y1 - 60):                                                 # stand-offs holding the bumper off the wall
            c.drawRect(R(262, yy - 7, 370, 14), lin_paint(0, yy - 7, 0, yy + 7, ["#94A3B8", "#475569"]))
        c.drawRect(R(240, y0, 30, y1 - y0), lin_paint(240, 0, 270, 0, ["#FFFFFF", "#CBD5E1", "#64748B"]))       # the bumper
        for yy in range(y0 + 30, y1, 90):
            c.drawCircle(255, yy, 5, P("#475569"))
        broke = t >= T["shatters"]
        if broke:
            c.drawOval(R(236, ym - 20, 38, 40), P("#05081A"))
            v2.shock_ring(c, 259, ym, t, T["shatters"], 0.5, r1=240, col="#FFFFFF", width=12, squash=1.0)
            sparks_shower(c, 259, ym, t, T["shatters"], 0.5, n=18, speed=520, seed=3, cone=(120, 240))
            rng = random.Random(9)
            for i in range(22):                                                      # the cloud of bits
                an = rng.uniform(-0.62, 0.62)
                tx = rng.uniform(476, 548)
                ty = ym + math.tan(an) * (tx - 268)
                u = prog(t, T["shatters"], T["shatters"] + rng.uniform(0.25, 0.42))
                c.drawCircle(lerp(268, tx, e_out(u)), lerp(ym, ty, e_out(u)), rng.uniform(3, 6.5), P("#F87171" if i % 3 else "#FFFFFF"))
        else:                                                                        # the speck, coming in
            u = e_in(prog(t, T["bump0"] - 0.2, T["shatters"]))
            sx = lerp(-40, 250, u)
            tr = lin_paint(sx - 220, 0, sx, 0, [("#FFFFFF", 0.0), ("#FFFFFF", 0.85)])
            tr.setStyle(skia.Paint.kStroke_Style)
            tr.setStrokeWidth(8)
            c.drawLine(sx - 220 * u, ym, sx, ym, tr)
            c.drawCircle(sx, ym, 13, P("#F87171"))
            c.drawCircle(sx - 4, ym - 4, 4, P("#FFFFFF", 0.8))
        self.ui["cam"] = (0, 0, 1)

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B1024", "#1B2238", "#0B1024"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def ui_space(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        if tw < s("break1") - 0.1:
            x0, y0 = self.at(190, -62)
            self.label(x0, y0, x0 + 40, y0 - 250, "orbit", T["orbit"] + 0.3, s("break1") - 0.3, "#7DD3FC")
        elif tw < s("fix2") - 0.12:
            limb = self.ui.get("limb", 1120)
            self.label(W / 2 + 70, limb - 90, W / 2 + 250, limb - 250, "store", T["store"], s("fix2") - 0.3, HILITE)
            sx, sy = self.at(0, 100)
            self.chip(W / 2, (sy + limb - 126) / 2, "km", T["hundred"] - 0.1, s("fix2") - 0.3, accent=WARN, size=46)
            self.badge("alert", T["storecut"] + 0.1, s("fix2") - 0.2, x=880, y=420)
        elif tw < T["wallcut"]:
            if tw < s("fix4") - 0.1:
                x0, y0 = self.at(-470, -300)
                self.label(x0, y0, x0 + 150, y0 - 150, "speck", T["speck0"] + 0.05, T["impact"] - 0.1, "#F87171")
                self.chip(540, 420, "speed", T["thousand"] - 0.4, s("fix4") - 0.25, accent=WARN, size=44 if self.lang == "en" else 36)
                self.badge("alert", T["impact"], s("fix4") - 0.2, x=880, y=560)
                self.red(T["impact"], 2.0)
        elif tw < T["s1"] - 0.35:
            x0, y0 = self.at(70, -330)
            self.label(x0, y0, x0 + 190, y0 - 110, "wings", T["wings"], T["window"] - 0.3, HILITE)
            x1, y1 = self.at(200, 126)
            self.label(x1, y1, x1 + 190, y1 + 130, "window", T["window"] + 0.1, T["tiecut"] - 0.05, "#7DD3FC")

    def ui_inside(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        seg = self.seg(tw)
        if seg == "breath":
            p = self.span(T["breath"] - 0.2, s("fix1") - 0.2)
            air = 1 - 0.85 * self.haze.at(tw)
            v2.gauge(c, 60, 250, [(self.L["air"], air, mix(WARN, GOOD, air))], p, w=330)
            self.badge("alert", T["poisons"], s("fix1") - 0.2)
            self.red(T["poisons"], 1.8)
        elif seg == "air":
            p = self.span(s("fix1"), s("break2") - 0.2)
            air = 1 - 0.85 * self.haze.at(tw)
            v2.gauge(c, 60, 250, [(self.L["air"], air, mix(WARN, GOOD, air))], p, w=330)
            x0, y0 = self.at(OX, -190)
            self.label(x0, y0, x0 + 60, y0 - 250, "o2", T["oxygen"] - 0.3, T["scrubbers"] - 0.2, O2C)
            x1, y1 = self.at(SCR, -164)
            self.label(x1, y1, x1 + 150, y1 - 330, "scrub", T["scrubbers"] + 0.1, s("break2") - 0.3, CO2C)
            self.badge("check", T["dioxide"], s("break2") - 0.15)
        elif seg == "dry":
            p = self.span(s("break2"), T["storecut"])
            v2.gauge(c, 60, 250, [(self.L["water"], self.wl.at(tw), mix(WARN, "#38BDF8", self.wl.at(tw)))], p, w=330)
            self.badge("alert", T["dry"], T["storecut"])
            self.red(T["dry"], 1.8)
        elif seg == "recycle":
            x0, y0 = self.at(104, -132)
            self.label(x0, y0, x0 + 40, y0 - 250, "filters", T["filters"] + 0.1, T["distiller"] - 0.15, GOOD)
            x1, y1 = self.at(DRUM, -120)
            self.label(x1, y1, x1 - 110, y1 - 330, "dist", T["distiller"] + 0.1, T["sweat"] - 0.1, "#7DD3FC")
            x2, y2 = self.at(228, -272)
            self.label(x2, y2, x2 - 150, y2 - 250, "coffee", T["tomorrow"], s("break3") - 0.3, HILITE)
            self.badge("check", T["tomorrow"] + 0.3, s("break3") - 0.15, x=880, y=420)
        elif seg == "bed":
            p = self.span(T["year"] - 0.2, s("fix3") - 0.2)
            bd = self.body.at(tw)
            v2.gauge(c, 60, 250, [(self.L["muscle"], bd, mix(WARN, GOOD, bd)), (self.L["bone"], bd * 0.9 + 0.1, mix(WARN, GOOD, bd))], p, w=330)
            self.chip(720, 330, "year", T["year"] - 0.1, T["muscles"] - 0.2, accent=HILITE, size=40)
            self.badge("alert", T["waste"], s("fix3") - 0.2)
            self.red(T["waste"], 1.8)
        elif seg == "gym":
            p = self.span(s("fix3"), s("break4") - 0.25)
            bd = self.body.at(tw)
            v2.gauge(c, 60, 250, [(self.L["muscle"], bd, mix(WARN, GOOD, bd)), (self.L["bone"], bd * 0.9 + 0.1, mix(WARN, GOOD, bd))], p, w=330)
            x0, y0 = self.at(TREAD - 60, -40)
            self.label(x0, y0, x0 - 40, y0 - 480, "bungee", T["bungee"] + 0.1, T["weight"] - 0.15, "#F97316")
            x1, y1 = self.at(ARED + 48, -110)
            self.label(x1, y1, x1 - 40, y1 - 400, "vac", T["vacuum"] - 0.1, T["two"] - 0.2, "#CBD5E1")
            self.chip(540, 600, "hours", T["two"] - 0.1, s("break4") - 0.25, accent=HILITE, size=42)
            self.badge("check", T["day"], s("break4") - 0.15, x=880, y=760)
        elif seg == "tag":
            x0, y0 = self.at(TOI + 62, -134)
            self.label(x0, y0, x0 + 150, y0 - 260, "aim", T["aim"], self.duration + 1, WARN)
            if tw >= T["aim"] - 0.1:
                k = e_back(prog(tw, T["aim"] - 0.1, T["aim"] + 0.15))
                c.drawCircle(x0, y0, 34 * k, P(WARN, 0.95, stroke=5))
                for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    c.drawLine(x0 + dx * 20 * k, y0 + dy * 20 * k, x0 + dx * 48 * k, y0 + dy * 48 * k, P(WARN, 0.95, stroke=5))

    def ui_wall(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(130, 540, "out", T["wallcut"] + 0.2, s("cta") - 0.3, size=30)
        self.chip(900, 400, "in", T["wallcut"] + 0.2, s("cta") - 0.3, size=30)
        self.label(259, 420, 240, 250, "bumper", T["bump0"], T["fab0"] - 0.15, "#E5E9F2")
        self.label(520, 1010, 330, 1140, "fabric", T["fab0"], s("cta") - 0.3, "#EAB308")
        self.label(660, 470, 850, 300, "hull", T["catches"], s("cta") - 0.3, "#94A3B8")
        self.badge("check", T["bits"], s("cta") - 0.15, x=880, y=640)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.pop(61), -6), (T["seal"] - 0.3, sfx.creak(0.3, 62), -9), (T["seal"], sfx.lock_click(63), -2),
              (T["throw"] - 0.25, sfx.whoosh(0.7, True, 64), -3), (T["orbit"] + 0.1, sfx.sparkle(0.7, 9, 65), -8), (T["congrats"] + 0.1, sfx.chime(), -8)]
        ev += [(s("break1") - 0.1, sfx.whoosh(0.4, True, 66), -5), (T["breath"] - 0.2, gas_hiss(0.5, 67), -10), (T["poisons"], sfx.alarm(3, 820), -10),
               (T["weekend"], sfx.womp(), -11)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["machine"] - 0.2, sfx.thunk(69), -4)]
        ev += [(T["splits"] + i * 0.22, bubble_snd(i), -9) for i in range(6)]
        ev += [(T["oxygen"], sfx.sparkle(0.6, 8, 70), -9), (T["scrubbers"] - 0.2, sfx.thunk(71), -4), (T["scrubbers"], sfx.whirr(1.2, 150, 240, 72), -12),
               (T["trap"], vent_snd(0.9, 6), -12), (T["dioxide"], sfx.chime(), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 73), -5), (T["water2"], sfx.power_down(0.9, 74), -9), (T["dry"], sfx.alarm(3, 820), -10),
               (T["storecut"], sfx.whoosh(0.4, False, 75), -5), (T["store"] - 0.25, sfx.pop(76), -5), (T["store"], sfx.ding(), -8),
               (T["hundred"] - 0.1, sfx.pop(77), -6), (T["down"] + 0.2, sfx.womp(), -8)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 78), -4), (T["filters"] - 0.2, sfx.pop(79), -5), (T["filters"], sfx.pop(80), -7),
               (T["distiller"] - 0.2, sfx.thunk(81), -4), (T["recycle"] - 0.1, sfx.whirr(1.4, 130, 200, 82), -12), (T["sweat"], bubble_snd(1), -8),
               (T["breath2"], bubble_snd(3), -8), (T["pee"], bubble_snd(5), -6), (T["yesterday"] - 0.2, sfx.pop(83), -6),
               (T["tomorrow"] - 0.35, sfx.whoosh(0.3, True, 84), -11), (T["tomorrow"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 85), -5), (T["year"] - 0.1, sfx.pop(86), -7), (T["muscles"], sfx.power_down(1.0, 87), -10),
               (T["waste"], sfx.alarm(3, 820), -10)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 88), -4), (T["treadmill"] - 0.2, sfx.thunk(89), -4), (T["bungee"] - 0.1, sfx.snap(90), -4)]
        ev += [(T["bungee"] + 0.1 + i * 0.27, sfx.tap(91 + i), -11) for i in range(int(max(2, (s("break4") - T["bungee"] - 0.4) / 0.27)))]
        ev += [(T["weight"] - 0.2, sfx.thunk(100), -4), (T["pulls"], sfx.hiss(0.4, 101), -10), (T["pulls"] + 0.75, sfx.hiss(0.4, 102), -11),
               (T["two"] - 0.1, sfx.pop(103), -6), (T["day"], sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 104), -5), (T["speck0"], sfx.beep(2200, 0.05), -10), (T["impact"] - 0.14, sfx.whoosh(0.2, True, 105), -3),
               (T["impact"], sfx.clank(900, 0.4, 106), 0), (T["impact"] + 0.03, sfx.thud(0.4, 107), -2), (T["impact"] + 0.1, vent_snd(1.6, 7), -7),
               (T["impact"] + 0.15, sfx.alarm(4, 820), -10)]
        ev += [(s("fix4") - 0.1, sfx.whoosh(0.4, True, 108), -6)]
        ev += [(T["wrap"] - 0.1 + i * 0.09, sfx.tap(109 + i), -8) for i in range(8)]
        ev += [(T["wallcut"], sfx.whoosh(0.4, True, 120), -5), (T["shatters"] - 0.12, sfx.whoosh(0.2, True, 121), -5), (T["shatters"], sfx.clank(1200, 0.3, 122), -1),
               (T["shatters"] + 0.02, sfx.snap(123), -3), (T["shatters"] + 0.3, sfx.thud(0.3, 124), -5), (T["catches"], sfx.pop(125), -6),
               (T["bits"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(126), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 127), -7), (T["follow"] - 0.15, sfx.pop(128), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 129), -6), (T["unfold"] - 0.1, sfx.whirr(1.0, 160, 320, 130), -9)]
        ev += [(T["unfold"] + i * 0.12, sfx.tick(), -8) for i in range(5)]
        ev += [(T["window"] - 0.2, sfx.pop(131), -5), (T["window"] + 0.2, sfx.sparkle(0.6, 8, 132), -9), (T["tiecut"], sfx.whoosh(0.35, False, 133), -6),
               (T["tie"], zip_snd(0), -3), (T["tie"] + 0.25, zip_snd(1), -4), (T["absolutely"], zip_snd(2), -3), (T["absolutely"] + 0.3, zip_snd(3), -4),
               (T["everything"], zip_snd(4), -2), (T["everything"] + 0.3, zip_snd(5), -2)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 134), -6), (T["s1"], sfx.pop(135), -3), (T["s2"], sfx.pop(136), -3), (T["s3"], sfx.pop(137), -3)]
        ev += [(T["cong2"], sfx.pop(138), -2), (T["cong2"], sfx.sparkle(1.0, 14, 139), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 140), -6), (T["vacuum2"] - 0.2, sfx.whirr(1.5, 200, 260, 141), -9), (T["vacuum2"] - 0.2, vent_snd(1.4, 8), -13),
               (T["seat"] - 0.1, sfx.lock_click(142), -2), (T["aim"] - 0.1, sfx.beep(1800, 0.08), -7), (T["carefully"] + 0.35, sfx.womp(), -3)]
        return ev


NAME = "station"
EPISODE = Station
