"""Episode 9 - A submarine.  v2 look: the sea at dusk and below it, six cameras ("sets") with whip cuts.

Sets: shore (a barrel rolls off the pier), tanks (the barrel with ballast tanks, half above and half under water),
deep (the dive, the crushed barrel, the pressure hull, the mountain, the sonar), peri (periscope depth), inside
(the hull in close-up: stale air, scrubber, oxygen maker, pantry, the game controller), wide (the finished boat).
The sea surface is y = 0 in every set, down is positive.
"""
from v2_base import *  # noqa: F401,F403

STEELC, BLACKC, WOODC = "#8E97AD", "#171A26", "#A9744A"
HL, HR, WALL = 280, 120, 14                   # pressure hull: half length, radius, wall thickness
HY = 1380                                     # the depth where the pressure hull gets built
RINGS = [-200 + i * 50 for i in range(9)]


# ====================================================================================== pieces
def gull(c, x, y, s, t, sit=False, face=-1):
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    if sit:
        c.drawOval(R(-20, -22, 40, 24), P("#F1F5F9"))
        c.drawOval(R(-22, -20, 26, 14), P("#94A3B8"))
        c.drawLine(-4, 0, -4, 10, P("#FB923C", 1, stroke=3))
        c.drawLine(6, 0, 6, 10, P("#FB923C", 1, stroke=3))
    else:
        fl = math.sin(t * 9) * 16
        for sd in (-1, 1):
            w = skia.Path()
            w.moveTo(0, -8)
            w.quadTo(sd * 22, -26 - fl, sd * 46, -10 + fl * 0.4)
            c.drawPath(w, P("#F1F5F9", 1, stroke=7))
        c.drawOval(R(-18, -14, 36, 16), P("#F1F5F9"))
    c.drawCircle(18, -20 if sit else -12, 9, P("#FFFFFF"))
    c.drawCircle(21, -22 if sit else -14, 2, P("#11151F"))
    beak = skia.Path()
    by = -19 if sit else -11
    beak.moveTo(26, by - 3)
    beak.lineTo(40, by)
    beak.lineTo(26, by + 3)
    beak.close()
    c.drawPath(beak, P("#FB923C"))
    c.restore()


def barrel(c, crush=0.0, lid=1.0, cut=0.0, seed=4):
    """A wooden barrel on its side, centred on the origin: 250 long, 150 across. crush 0..1 squeezes it like a can,
    lid 0 (hatch open) .. 1 (shut), cut > 0 opens a window into it."""
    rng = random.Random(seed)
    top, bot, n = [], [], 10
    for i in range(n + 1):
        u = i / n
        bulge = 14 * math.sin(u * math.pi)
        k = 0.4 + math.sin(u * math.pi)
        top.append((-125 + 250 * u, -62 - bulge + crush * rng.uniform(8, 58) * k))
        bot.append((-125 + 250 * u, 62 + bulge - crush * rng.uniform(8, 50) * k))
    path = skia.Path()
    path.moveTo(*top[0])
    for p in top[1:]:
        path.lineTo(*p)
    for p in reversed(bot):
        path.lineTo(*p)
    path.close()
    c.drawPath(path, lin_paint(0, -80, 0, 80, [shade(WOODC, 0.25), WOODC, shade(WOODC, -0.4)], [0.0, 0.4, 1.0]))
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    for yy in (-44, -22, 0, 22, 44):
        c.drawLine(-125, yy, 125, yy, P("#3A2414", 0.30, stroke=2))
    for hx in (-92, 0, 92):
        c.drawRect(R(hx - 9, -90, 18, 180), lin_paint(0, -80, 0, 80, ["#DDE3EE", "#7C8499", "#3F465A"]))
    for _ in range(int(crush * 10)):
        x0, y0 = rng.uniform(-110, 110), rng.uniform(-50, 50)
        c.drawLine(x0, y0, x0 + rng.uniform(-34, 34), y0 + rng.uniform(-28, 28), P("#1B1210", 0.85, stroke=3))
    if cut > 0:
        c.drawRRect(rr(-104, -54, 208, 108, 26), P("#2A1A12", cut))
        add_glow(c, -66, -30, 80, "#FFC766", 0.55 * cut)
        c.drawCircle(-66, -34, 6, P("#FFE9B8", cut))
    c.restore()
    dy = crush * 30
    c.drawRect(R(-34, -78 + dy, 68, 6), P("#3F465A"))
    c.save()
    c.translate(-30, -80 + dy)
    c.rotate(-105 * (1 - lid))
    c.drawRRect(rr(0, -8, 60, 11, 5), P("#8E97AD"))
    c.restore()


def tanks(c, fill=0.0, vent=0.0, blow=0.0, pop=1.0):
    """Two ballast tanks slung under the barrel (shown cut open), vents on their shoulders, the air flask between."""
    if pop <= 0:
        return
    for sd in (-1, 1):
        x0 = -118 if sd < 0 else 18
        c.save()
        c.translate(x0 + 50, 70)
        c.scale(pop, pop)
        c.translate(-(x0 + 50), -70)
        c.drawRect(R(x0 + 46, 44, 8, 30), P("#3F465A"))
        c.drawRRect(rr(x0, 70, 100, 72, 16), lin_paint(0, 70, 0, 142, ["#B4BCD0", "#6B7385", "#3F465A"]))
        c.drawRRect(rr(x0 + 7, 77, 86, 58, 11), P("#0D1730"))
        if fill > 0:
            hgt = 58 * clamp(fill)
            c.save()
            c.clipRRect(rr(x0 + 7, 77, 86, 58, 11), skia.ClipOp.kIntersect, True)
            vrect(c, x0 + 7, 135 - hgt, 86, hgt + 1, ["#38BDF8", "#0E6BA8"])
            c.drawRect(R(x0 + 7, 135 - hgt, 86, 3), P("#E0F7FF", 0.85))
            c.restore()
        c.drawRect(R(x0 + 40, 135, 20, 8), P("#0D1730"))
        vx = x0 + (10 if sd < 0 else 90)
        c.drawRect(R(vx - 6, 54, 12, 20), P("#8E97AD"))
        c.drawRRect(rr(vx - 12, 46 - 13 * vent, 24, 8, 3), P(mix("#EF4444", "#4ADE80", vent)))
        c.restore()
    c.drawRRect(rr(-36, 150, 72, 26, 13), lin_paint(0, 150, 0, 176, ["#FDBA74", "#F97316", "#9A3412"]))
    for sd in (-1, 1):
        c.drawLine(sd * 34, 163, sd * 62, 140, P("#F97316", 1, stroke=4))
    if blow > 0:
        add_glow(c, 0, 163, 70, "#FDBA74", 0.8 * blow)


def arrows_in(c, cx, cy, rx, ry, n, k, t, col="#FFFFFF", push=18):
    """n arrows around an ellipse, all pointing at it (water pressure). k 0..1 fades them in."""
    if k <= 0:
        return
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        pulse = push * (0.5 + 0.5 * math.sin(t * 7 + i))
        ox, oy = math.cos(a), math.sin(a)
        x0, y0 = cx + ox * (rx + 78 - pulse), cy + oy * (ry + 78 - pulse)
        x1, y1 = cx + ox * (rx + 26 - pulse), cy + oy * (ry + 26 - pulse)
        c.drawLine(x0, y0, x1, y1, P(col, 0.85 * k, stroke=7))
        hd = skia.Path()
        hd.moveTo(x1 - ox * 10, y1 - oy * 10)
        hd.lineTo(x1 + ox * 8 - oy * 14 + ox * 6, y1 + oy * 8 + ox * 14 + oy * 6)
        hd.lineTo(x1 + ox * 8 + oy * 14 + ox * 6, y1 + oy * 8 - ox * 14 + oy * 6)
        hd.close()
        tip = skia.Path()
        tip.moveTo(x1 - ox * 16, y1 - oy * 16)
        tip.lineTo(x1 + 4 * ox - oy * 14, y1 + 4 * oy + ox * 14)
        tip.lineTo(x1 + 4 * ox + oy * 14, y1 + 4 * oy - ox * 14)
        tip.close()
        c.drawPath(tip, P(col, 0.9 * k))


def sub_out(c, t, paint=0.0, tail=1.0, prop=1.0, mast=0.0, glow=0.0):
    """The boat from outside, centred on the origin, bow to the right. paint 0 (bare steel) .. 1 (black)."""
    def shell(col, rim):
        c.drawRRect(rr(-30, -200, 118, 100, 26), lin_paint(0, -200, 0, -100, [shade(col, 0.3), col]))        # the sail
        c.drawRRect(rr(20, -160, 96, 10, 5), P(shade(col, 0.15)))
        if tail > 0:
            c.save()
            c.translate(-160, 0)
            c.scale(tail, 1)
            c.drawRRect(rr(-262, -84, 40, 168, 10), P(shade(col, -0.1)))                                     # rudder
            tp = skia.Path()
            tp.moveTo(0, -120)
            tp.quadTo(-170, -112, -282, -15)
            tp.lineTo(-282, 15)
            tp.quadTo(-170, 112, 0, 120)
            tp.close()
            c.drawPath(tp, lin_paint(0, -120, 0, 120, [shade(col, 0.28), col, shade(col, -0.5)], [0.0, 0.35, 1.0]))
            c.restore()
        c.drawRRect(rr(-HL, -HR, 2 * HL, 2 * HR, HR), lin_paint(0, -HR, 0, HR, [shade(col, 0.28), col, shade(col, -0.5)], [0.0, 0.35, 1.0]))
        c.drawRRect(rr(-HL + 60, -HR + 14, 2 * HL - 150, 12, 6), P(rim, 0.22))
    shell(STEELC, "#FFFFFF")
    if paint > 0:
        c.save()
        c.clipRect(R(lerp(320, -480, paint), -420, 900, 700))
        shell(BLACKC, "#7FB2FF")
        c.restore()
        if paint < 1:
            px = lerp(320, -480, paint)
            c.drawRect(R(px - 5, -210, 10, 340), P("#FFFFFF", 0.5))
    if mast > 0:
        c.drawRect(R(34, -200 - 150 * mast, 10, 150 * mast + 4), lin_paint(34, 0, 44, 0, ["#DDE3EE", "#5B657E"]))
        c.drawRRect(rr(28, -200 - 150 * mast - 16, 30, 18, 5), P("#3F465A"))
        c.drawCircle(53, -200 - 150 * mast - 7, 5, P("#7DD3FC"))
        add_glow(c, 53, -200 - 150 * mast - 7, 18, "#7DD3FC", 0.8)
    if glow > 0:
        add_glow(c, 232, 16, 90, "#22D3EE", 0.7 * glow)
        c.drawCircle(232, 16, 40, P("#22D3EE", 0.35 * glow))
    if prop > 0 and tail > 0:
        px = -160 - 290 * tail
        c.drawRRect(rr(px - 8, -10, 20, 20, 8), P("#B7791F"))
        for ph in (0.0, 1.57):
            hgt = 116 * abs(math.sin(t * 16 + ph)) * prop
            c.drawOval(R(px - 9, -hgt / 2, 18, hgt), lin_paint(px - 9, 0, px + 9, 0, ["#FDE68A", "#B7791F"]))
        c.drawOval(R(px - 6, -60 * prop, 12, 120 * prop), P("#FDE68A", 0.18))


def whale(c, x, y, s, t, a=0.5):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = skia.Path()
    p.moveTo(-190, 0)
    p.cubicTo(-150, -70, 60, -86, 170, -18)
    p.lineTo(232, -52 + math.sin(t * 1.5) * 12)
    p.lineTo(214, 0)
    p.lineTo(236, 44 + math.sin(t * 1.5) * 12)
    p.lineTo(168, 14)
    p.cubicTo(60, 56, -150, 50, -190, 0)
    p.close()
    c.drawPath(p, P("#2A6496", a))
    c.drawCircle(-140, -8, 4, P("#BFE4FF", a))
    c.restore()


def can(c, x, y, col, a=1.0):
    cyl(c, x, y - 20, 15, 20, col, r=3, a=a)
    c.drawRect(R(x, y - 13, 15, 6), P("#F8FAFC", 0.85 * a))


def crunch(seed=40, d=0.45):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 350, 3800) * sfx._env(n, 0.002, d * 0.22)
    x[::7] *= 0.2
    return sfx._norm(x + 0.6 * sfx._lp(sfx._rng(seed + 1).standard_normal(n), 220) * sfx._env(n, 0.002, d * 0.3), 0.8)


def ping_snd(f=1500.0, d=1.1):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    return sfx._norm(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3.6) * sfx._ar(n, 0.004, 0.2), 0.6)


def water_snd(d=0.6, seed=60):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 500, 5000)
    return sfx._norm(x * sfx._env(n, 0.004, d * 0.28), 0.8)


def bubble_snd(d=0.9, seed=70):
    n = int(d * sfx.SR)
    out = np.zeros(n)
    rng = sfx._rng(seed)
    for _ in range(int(d * 16)):
        i = int(rng.uniform(0, d - 0.08) * sfx.SR)
        m = int(0.06 * sfx.SR)
        tt = np.arange(m) / sfx.SR
        f0 = rng.uniform(500, 1300)
        out[i:i + m] += np.sin(2 * np.pi * (f0 + 2600 * tt) * tt) * sfx._ar(m, 0.004, 0.03)
    return sfx._norm(out, 0.5)


# ====================================================================================== the episode
class Submarine(EpisodeV2):
    BUILD_NO = 9
    FIRST_SET = "shore"
    CLEAR = "#04101F"
    TITLE = {"en": "SUBMARINE", "ar_sa": "غواصة"}
    EMPH = {"en": ["CONGRATS", "SUBMARINE", "CORK", "SEAGULLS", "BALLAST", "SINK", "RISE", "SQUEEZES", "SODA", "PRESSURE", "THICK",
                   "RINGS", "DARK", "WINDOWS", "MOUNTAIN", "SONAR", "ECHO", "PERISCOPE", "STALE", "HEADACHE", "SCRUBBERS", "OXYGEN",
                   "FOOD", "FOLLOW", "TOILET", "PROPELLER", "BLACK", "NOBODY", "ZERO", "YOURSELF", "CONTROLLER", "TRAINING"],
            "ar_sa": ["مبروك", "غواصة", "الفلينة", "لطيور", "خزانات", "وتنزل", "وتطلع", "تعصر", "علبة", "الضغط", "سميك", "بحلقات",
                      "ظلام", "شبابيك", "جبل", "سونار", "صداها", "ومنظار", "يثقل", "يصدّع", "فلاتر", "أكسجين", "الأكل", "تابعني",
                      "حمام", "مروحة", "أسود", "أحد", "وصفر", "بيدك", "تحكم", "تدريب"]}
    KEYS = {"ar_sa": {
        ("hook", "SEAL"): "قفّلت", ("hook", "BARREL"): "برميل", ("hook", "ROLL"): "ودحرجته", ("hook", "SEA"): "البحر",
        ("hook", "CONGRATS"): "مبروك",
        ("break1", "FLOATS"): "يطفو", ("break1", "CORK"): "الفلينة", ("break1", "BOB"): "تتمرجح", ("break1", "WAVING"): "وتلوّح",
        ("break1", "SEAGULLS"): "لطيور",
        ("fix1", "BALLAST"): "خزانات", ("fix1", "VENTS"): "الفتحات", ("fix1", "FLOODS"): "تدخل", ("fix1", "SINK"): "وتنزل",
        ("fix1", "PUSH"): "تنفخها", ("fix1", "AIR"): "مضغوط", ("fix1", "RISE"): "وتطلع",
        ("break2", "DIVE"): "تغوص", ("break2", "DEEP"): "العميقة", ("break2", "SQUEEZES"): "تعصر", ("break2", "SODA"): "علبة",
        ("fix2", "PRESSURE"): "يتحمل", ("fix2", "THICK"): "سميك", ("fix2", "ROUNDED"): "مدورة", ("fix2", "RINGS"): "بحلقات",
        ("fix2", "SPREADS"): "يتوزع",
        ("break3", "DARK"): "ظلام", ("break3", "WINDOWS"): "شبابيك", ("break3", "DROVE"): "صدمت", ("break3", "MOUNTAIN"): "جبل",
        ("fix3", "SONAR"): "سونار", ("fix3", "PING"): "نبضة", ("fix3", "ECHO"): "صداها", ("fix3", "PERISCOPE"): "ومنظار",
        ("fix3", "PEEK"): "تطل", ("fix3", "SURFACE"): "سطح",
        ("break4", "WAY"): "طريقك", ("break4", "STALE"): "يثقل", ("break4", "CREW"): "والطاقم", ("break4", "HEADACHE"): "يصدّع",
        ("fix4", "SCRUBBERS"): "فلاتر", ("fix4", "DIOXIDE"): "الكربون", ("fix4", "MACHINE"): "وجهاز", ("fix4", "SPLITS"): "يفصل",
        ("fix4", "OXYGEN"): "أكسجين", ("fix4", "FOOD"): "الأكل",
        ("cta", "DIVE"): "تغوص", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PROPELLER"): "مروحة", ("reveal", "PAINT"): "وادهنها", ("reveal", "BLACK"): "أسود", ("reveal", "NOBODY"): "أحد",
        ("reveal", "PARKED"): "وقّفتها",
        ("stat", "ONE"): "جسم", ("stat", "HUNDRED"): "مية", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "PERISCOPE"): "والمنظار", ("tag", "STEER"): "تحركه", ("tag", "CONTROLLER"): "تحكم", ("tag", "MOM"): "لأمك",
        ("tag", "TRAINING"): "تدريب"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a toilet"),
                   "stat": [("1", "HULL"), ("100+", "SAILORS"), ("0", "WINDOWS")],
                   "L": {"barrel": "YOUR BARREL", "tank": "BALLAST TANK", "vent": "VENT", "air": "COMPRESSED AIR", "depth": "DEPTH",
                         "hull": "PRESSURE HULL", "thick": "THICK STEEL", "rings": "STEEL RINGS", "nowin": "NO WINDOWS",
                         "sonar": "SONAR", "peri": "PERISCOPE", "co2": "CARBON DIOXIDE", "o2": "OXYGEN", "scrub": "SCRUBBER",
                         "o2m": "OXYGEN MAKER", "food": "FOOD: 3 MONTHS", "prop": "PROPELLER", "train": "IT'S TRAINING"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: كرسي حمام"),
                      "stat": [("1", "جسم"), ("+100", "بحّار"), ("0", "شبابيك")],
                      "L": {"barrel": "برميلك", "tank": "خزان موية", "vent": "فتحة", "air": "هوا مضغوط", "depth": "العمق",
                            "hull": "جسم يتحمل الضغط", "thick": "حديد سميك", "rings": "حلقات حديد", "nowin": "بدون شبابيك",
                            "sonar": "سونار", "peri": "منظار", "co2": "ثاني أكسيد الكربون", "o2": "أكسجين", "scrub": "فلتر",
                            "o2m": "جهاز الأكسجين", "food": "أكل ثلاث شهور", "prop": "مروحة", "train": "هذا تدريب"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "seal": ("hook", "SEAL", 0.1), "barrel": ("hook", "BARREL", 0.25), "roll": ("hook", "ROLL", 0.35), "sea": ("hook", "SEA", 0.55),
            "congrats": ("hook", "CONGRATS", 0.62),
            "floats": ("break1", "FLOATS", 0.15), "cork": ("break1", "CORK", 0.3), "bob": ("break1", "BOB", 0.55),
            "waving": ("break1", "WAVING", 0.7), "seagulls": ("break1", "SEAGULLS", 0.85),
            "ballast": ("fix1", "BALLAST", 0.12), "vents": ("fix1", "VENTS", 0.33), "floods": ("fix1", "FLOODS", 0.47),
            "sink": ("fix1", "SINK", 0.62), "blow": ("fix1", "PUSH", 0.68), "air": ("fix1", "AIR", 0.84), "rise": ("fix1", "RISE", 0.96),
            "dive": ("break2", "DIVE", 0.18), "deep": ("break2", "DEEP", 0.42), "squeezes": ("break2", "SQUEEZES", 0.55),
            "soda": ("break2", "SODA", 0.85),
            "pressure": ("fix2", "PRESSURE", 0.17), "thick": ("fix2", "THICK", 0.3), "rounded": ("fix2", "ROUNDED", 0.45),
            "rings": ("fix2", "RINGS", 0.7), "spreads": ("fix2", "SPREADS", 0.87),
            "dark": ("break3", "DARK", 0.15), "windows": ("break3", "WINDOWS", 0.52), "drove": ("break3", "DROVE", 0.75),
            "mountain": ("break3", "MOUNTAIN", 0.9),
            "sonar": ("fix3", "SONAR", 0.13), "ping": ("fix3", "PING", 0.35), "echo": ("fix3", "ECHO", 0.55),
            "periscope": ("fix3", "PERISCOPE", 0.7), "peek": ("fix3", "PEEK", 0.84), "surface": ("fix3", "SURFACE", 0.94),
            "way": ("break4", "WAY", 0.25), "stale": ("break4", "STALE", 0.5), "crew": ("break4", "CREW", 0.73),
            "headache": ("break4", "HEADACHE", 0.88),
            "scrubbers": ("fix4", "SCRUBBERS", 0.1), "dioxide": ("fix4", "DIOXIDE", 0.34), "machine": ("fix4", "MACHINE", 0.45),
            "splits": ("fix4", "SPLITS", 0.53), "oxygen": ("fix4", "OXYGEN", 0.67), "food": ("fix4", "FOOD", 0.86),
            "dive2": ("cta", "DIVE", 0.28), "follow": ("cta", "FOLLOW", 0.4),
            "propeller": ("reveal", "PROPELLER", 0.23), "paint": ("reveal", "PAINT", 0.4), "black": ("reveal", "BLACK", 0.45),
            "nobody": ("reveal", "NOBODY", 0.6), "parked": ("reveal", "PARKED", 0.84),
            "s1": ("stat", "ONE", 0.04), "s2": ("stat", "HUNDRED", 0.38), "s3": ("stat", "ZERO", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "peri2": ("tag", "PERISCOPE", 0.1), "steer": ("tag", "STEER", 0.35), "controller": ("tag", "CONTROLLER", 0.55),
            "mom": ("tag", "MOM", 0.8), "training": ("tag", "TRAINING", 0.9)})
        T["sea"] = self.w("hook", "SEA", 0.55, nth=1 if self.lang == "en" else 0)      # (in English "seal" comes first)
        T["splash"] = T["sea"]
        T["crush3"] = T["soda"] + 0.15                             # the barrel is as flat as it gets
        T["crash"] = T["mountain"] - 0.15                          # bow meets rock
        T["food0"] = max(min(T["food"], e("fix4") - 1.0) - 0.75, T["oxygen"] + 0.45)   # the camera wanders over to the pantry
        T["gone"] = T["parked"] + 0.45
        # ---- sets
        self.cut(s("fix1") - 0.12, "tanks", 1)
        self.cut(s("break2") - 0.1, "deep", 1)
        self.cut(s("fix2") - 0.12, "deep", -1)
        self.cut(T["periscope"] - 0.35, "peri", -1)
        self.cut(s("break4") - 0.12, "inside", 1)
        self.cut(s("cta") + 0.05, "wide", -1)
        self.cut(s("tag") - 0.2, "inside", 1)
        self.cams = {"shore": Camera(-330, -190, 1.3), "tanks": Camera(0, 110, 2.1), "peri": Camera(60, 256, 1.25),
                     "inside": Camera(40, 92, 2.4), "wide": Camera(-70, 190, 0.95)}
        cm = self.cams
        cm["shore"].key(0.05, -400, -200, 1.42, 1.2).key(T["roll"] - 0.1, -150, -170, 1.3, T["sea"] - T["roll"] + 0.3)
        cm["shore"].key(s("break1") - 0.1, 0, -120, 1.5, 1.2)
        cm["tanks"].key(T["sink"] - 0.3, 0, 395, 1.9, 0.8).key(T["rise"] - 0.55, 0, 110, 2.1, 0.8)
        cm["peri"].key(T["periscope"] - 0.35, 40, 256, 1.2, 0.0).key(T["peek"] - 0.3, 110, 230, 1.3, 0.8)
        cm["inside"].key(s("break4") - 0.12, 40, 92, 2.4, 0.0).key(T["stale"] - 0.5, 50, 92, 2.55, 1.2)
        cm["inside"].key(s("fix4") - 0.1, -90, 92, 2.55, 0.7).key(T["food0"], 150, 92, 2.6, 0.7)
        cm["inside"].key(s("tag") - 0.2, 30, 82, 3.1, 0.0).key(T["mom"] - 0.3, 46, 82, 3.3, 0.8)
        cm["wide"].key(s("cta") + 0.05, -70, 190, 0.95, 0.0).key(s("reveal") - 0.1, -110, 190, 1.0, 0.9)
        cm["wide"].key(T["nobody"], -70, 200, 0.95, 0.8)
        cm["wide"].key(T["s1"] - 0.3, -70, 1022, 0.9, 0.9).key(s("closer") - 0.3, -70, 190, 0.95, 0.85)
        # ---- the barrel with tanks (set "tanks")
        self.vy = Track(6.0).to(T["sink"] - 0.3, 330.0, 0.8, e_io).to(T["rise"] - 0.55, 6.0, 0.8, e_io)
        self.fill = Track(0.0).to(T["floods"] - 0.15, 1.0, max(0.5, T["sink"] - T["floods"])).to(T["blow"] + 0.3, 0.0, max(0.5, T["rise"] - T["blow"] - 0.7))
        self.vent = Track(0.0).to(T["vents"], 1.0, 0.2).to(T["sink"] + 0.2, 0.0, 0.2)
        self.blowk = Track(0.0).to(T["blow"], 1.0, 0.2).to(T["rise"] - 0.2, 0.0, 0.3)
        # ---- the dive (set "deep"), then the pressure hull at depth HY
        self.dy = Track(60.0).to(T["dive"] - 0.4, 1500.0, max(0.8, T["squeezes"] - T["dive"] + 0.25), e_io)
        self.crush = Track(0.0).to(T["squeezes"], 0.35, 0.12).to((T["squeezes"] + T["crush3"]) / 2, 0.7, 0.12).to(T["crush3"], 1.0, 0.12)
        self.hx = Track(0.0).to(T["dark"] - 0.4, 1160.0, T["crash"] - T["dark"] + 0.4, e_in).to(T["crash"], 1090.0, 0.5, e_out)
        self.hx.to(T["sonar"] - 0.4, 1040.0, 0.6)
        self.dark = Track(0.0).to(T["dark"] - 0.3, 0.55, 0.7).to(T["ping"] + 0.3, 0.3, 0.5)
        # ---- inside
        self.stale = Track(0.0).to(T["stale"] - 0.6, 1.0, 1.5).to(T["scrubbers"] + 0.3, 0.0, max(0.8, T["dioxide"] - T["scrubbers"]))
        self.oxy = Track(0.75).to(T["stale"] - 0.6, 0.3, 1.8).to(T["splits"], 0.95, 1.0)
        # ---- the finished boat (set "wide"): depth of its centre line
        self.wy = Track(95.0).to(T["nobody"] + 0.35, 900.0, T["gone"] - T["nobody"] + 0.4, e_in).to(s("closer") - 0.3, 95.0, 0.8, e_out)
        self.paintk = Track(0.0).to(T["paint"] - 0.05, 1.0, max(0.45, T["black"] - T["paint"] + 0.35))
        self.spans = [(T["bob"], T["rise"] + 0.2), (T["squeezes"], T["spreads"] + 0.4), (T["crash"], T["surface"]),
                      (T["crew"], T["oxygen"] + 0.3)]
        self.shakes = [(T["seal"], 0.2, 8), (T["splash"], 0.35, 12), (T["squeezes"], 0.3, 12), ((T["squeezes"] + T["crush3"]) / 2, 0.3, 14),
                       (T["crush3"], 0.4, 20), (T["crash"], 0.6, 30), (T["rounded"], 0.25, 8), (s("closer") + 0.25, 0.35, 12)]
        self.shakes += [(T["rings"] - 0.15 + i * 0.07, 0.12, 5) for i in range(len(RINGS))]

    # ------------------------------------------------------------------ shared drawing
    def water(self, c, t, cam, dark=0.0):
        """Sky above the surface (if it is in frame) and the water under it, screen space. Returns the surface's screen y."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        if gy > 0:
            self.backdrop(c, t, cx, cy, gy, sea_=True)
        d = clamp(cy / 1400)
        underwater(c, W, H, t, mix("#1B6C9C", "#0A2742", d), mix("#0D3A66", "#061A33", d), mix("#051630", "#02060F", d),
                   rays=d < 0.8, surface_y=gy if gy > 0 else None)
        if dark > 0:
            c.drawRect(R(0, max(gy, 0), W, H), P("#01030A", dark))
        return gy

    def waves(self, c, t, cam):
        cx, cy, z = cam
        x0, x1 = cx - 620 / z, cx + 620 / z
        c.drawRect(R(x0, 0, x1 - x0, 2600), P("#0D3A66", 0.22))                    # everything under water sits behind a veil
        for k in range(3):
            path = skia.Path()
            xx = x0
            path.moveTo(xx, k * 12)
            while xx < x1:
                xx += 36
                path.lineTo(xx, k * 12 + math.sin(xx * 0.012 + t * (1.2 + k * 0.3) + k) * (4 + k))
            c.drawPath(path, P("#D6EEFF", 0.6 - k * 0.18, stroke=3.5 - k * 0.5))

    def hull_cut(self, c, t, tube=1.0, ends=1.0, rings=1.0, sail=0.0, mast=0.0, dome=0.0, inner=None):
        """The pressure hull cut open, centred on the origin. inner(c, t) draws what is inside (clipped to the hull)."""
        k = e_back(clamp(tube))
        if k <= 0:
            return
        c.save()
        c.scale(lerp(0.3, 1.0, k), k)
        if sail > 0:
            sk = e_back(clamp(sail))
            c.drawRRect(rr(-30, -HR - 80 * sk, 118, 100, 26), lin_paint(0, -200, 0, -100, [shade(STEELC, 0.3), STEELC]))
            if mast > 0:
                c.drawRect(R(34, -200 - 150 * mast, 10, 150 * mast + 4), lin_paint(34, 0, 44, 0, ["#DDE3EE", "#5B657E"]))
                c.drawRRect(rr(28, -200 - 150 * mast - 16, 30, 18, 5), P("#3F465A"))
                c.drawCircle(53, -200 - 150 * mast - 7, 5, P("#7DD3FC"))
                add_glow(c, 53, -200 - 150 * mast - 7, 18, "#7DD3FC", 0.8)
        ek = e_back(clamp(ends))
        tube_l = 160 + (HL - 160) * 0.0
        outer, inner_p = skia.Path(), skia.Path()
        if ek <= 0:
            outer.addRect(R(-tube_l, -HR, 2 * tube_l, 2 * HR))
            inner_p.addRect(R(-tube_l + 4, -HR + WALL, 2 * tube_l - 8, 2 * HR - 2 * WALL))
        else:
            ext = (HL - 160) * ek
            outer.addRRect(rr(-160 - ext, -HR, 320 + 2 * ext, 2 * HR, HR * ek))
            inner_p.addRRect(rr(-160 - ext + WALL, -HR + WALL, 320 + 2 * ext - 2 * WALL, 2 * HR - 2 * WALL, max(1.0, (HR - WALL) * ek)))
        c.drawPath(outer, lin_paint(0, -HR, 0, HR, ["#DDE3EE", "#9AA3B8", "#5B657E"]))
        c.save()
        c.clipPath(inner_p, skia.ClipOp.kIntersect, True)
        vrect(c, -HL, -HR, 2 * HL, 2 * HR, ["#33405F", "#232C46", "#182036"], [0.0, 0.55, 1.0])
        c.drawRect(R(-HL, 60, 2 * HL, 60), P("#101626"))                             # under the deck: batteries
        for bx in range(-230, 231, 46):
            c.drawRRect(rr(bx - 17, 72, 34, 26, 4), P("#2B3550"))
            c.drawRect(R(bx - 9, 68, 6, 5), P("#F59E0B"))
        c.drawRect(R(-HL, 58, 2 * HL, 6), P("#7C8499"))
        c.drawLine(-HL, -92, HL, -92, P("#F97316", 0.75, stroke=5))
        c.drawLine(-HL, -80, HL, -80, P("#38BDF8", 0.6, stroke=4))
        for lx in (-150, 0, 150):                                                    # lamps
            c.drawRRect(rr(lx - 16, -74, 32, 7, 3), P("#FFF3C4"))
            add_glow(c, lx, -62, 110, "#FFE9B8", 0.30)
        for i, rx in enumerate(RINGS):                                               # ring frames
            rk = e_back(clamp(rings * len(RINGS) - i))
            if rk > 0:
                c.drawRect(R(rx - 7, -HR, 14, 2 * HR), P("#FFFFFF", 0.05 * rk))
                c.drawRect(R(rx - 7, -HR + WALL - 2, 14, 20 * rk), lin_paint(rx - 7, 0, rx + 7, 0, ["#E5E9F2", "#7C8499"]))
                c.drawRect(R(rx - 7, HR - WALL + 2 - 20 * rk, 14, 20 * rk), lin_paint(rx - 7, 0, rx + 7, 0, ["#E5E9F2", "#7C8499"]))
        if dome > 0:                                                                 # the sonar in the bow
            dk = e_back(clamp(dome))
            c.drawCircle(214, 0, 42 * dk, rad_paint(204, -10, 60, ["#A5F3FC", "#22D3EE", "#0E7490"]))
            add_glow(c, 214, 0, 100, "#22D3EE", 0.5 * dk * (0.7 + 0.3 * math.sin(t * 6)))
        if inner:
            inner(c, t)
        c.restore()
        c.drawPath(outer, P("#F1F5F9", 0.9, stroke=3))
        c.restore()

    def crew_in(self, c, t, pose, xs=(-40, 52, 140), face=1, sore=0.0):
        for i, (px, col) in enumerate(zip(xs, SHIRTS)):
            engineer(c, px, 58, 92 + (i % 2) * 6, col, t + i * 0.37, pose, face=face if i != 1 else -face)
            if sore > 0:
                for j in range(3):
                    a = math.radians(-90 + (j - 1) * 38)
                    r0 = 14 + 8 * math.sin(t * 9 + i + j)
                    hx, hy = px, 58 - (92 + (i % 2) * 6) * (0.64 if pose == "duck" else 1.0) - 26
                    c.drawLine(hx + math.cos(a) * r0, hy + math.sin(a) * r0, hx + math.cos(a) * (r0 + 14), hy + math.sin(a) * (r0 + 14),
                               P("#FF4D4F", sore, stroke=4))

    # ------------------------------------------------------------------ set: the shore
    def barrel_pose(self, t):
        T = self.T
        if t < T["roll"]:
            return -430.0, -135.0, 0.0
        u = prog(t, T["roll"], T["splash"])
        if u < 1:
            x = lerp(-430, -30, e_in(u) * 0.55 + u * 0.45)
            y = -135.0 if x < -250 else lerp(-135, -60, clamp((x + 250) / 200))
            rot = u * 360
            return x, y - 50 * abs(math.sin(math.radians(rot))), rot
        v = t - T["splash"]
        return (lerp(-30, 90, e_out(clamp(v / 1.3))), -18 + 30 * math.exp(-v * 3) * math.cos(v * 9) + math.sin(t * 1.7) * 6,
                math.sin(t * 1.3) * 5 * (1 - math.exp(-v * 2)))

    def draw_shore(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["shore"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        self.water(c, t, cam)
        self.view(c, cam)
        for px in range(-1900, -240, 150):                                           # the pier
            cyl(c, px - 9, -60, 18, 420, "#5B3A22")
        box(c, -2000, -62, 1752, 20, "#8B5E3C", r=3)
        for px in range(-1990, -250, 58):
            c.drawRect(R(px, -62, 3, 20), P("#3A2414", 0.5))
        ramp = skia.Path()
        ramp.moveTo(-250, -62)
        ramp.lineTo(-60, 14)
        ramp.lineTo(-60, 28)
        ramp.lineTo(-250, -44)
        ramp.close()
        c.drawPath(ramp, lin_paint(-250, 0, -60, 0, ["#8B5E3C", "#5B3A22"]))
        floodlight(c, -700, 330, -430, -100, t, on=1.0)
        bx, by, rot = self.barrel_pose(t)
        inside = T["seal"] - 0.25 <= t < T["floats"] - 0.1                            # one of the crew travels in it
        up = 1 - prog(t, T["seal"] - 0.25, T["seal"] - 0.1) if t < T["seal"] else prog(t, T["floats"] - 0.1, T["floats"] + 0.15)
        if not inside or up > 0:
            c.save()
            c.translate(bx, by)
            c.rotate(rot)
            engineer(c, 0, -18 + 70 * (1 - up), 100, SHIRTS[1], t, "cheer" if (t >= T["waving"] - 0.2 or t < T["seal"] - 0.4) else "look", face=1)
            c.restore()
        c.save()
        c.translate(bx, by)
        c.rotate(rot)
        lid = prog(t, T["seal"] - 0.1, T["seal"]) if t < T["floats"] - 0.2 else 1 - prog(t, T["floats"] - 0.2, T["floats"])
        barrel(c, 0.0, lid)
        c.restore()
        sparks_shower(c, bx, by - 80, t, T["seal"], 0.5, n=16, speed=420, seed=3)
        # the other two, on the pier
        push = prog(t, T["roll"] - 0.15, T["roll"] + 0.35)
        xs = (lerp(-640, -400, e_out(push)), lerp(-596, -340, e_out(push)))
        pose = "stand" if t < T["roll"] - 0.15 else "carry" if t < T["roll"] + 0.35 else "cheer" if t < s("break1") else "look"
        if t >= s("break1") - 0.1:
            xs = (-316, -276)
        for i, px in enumerate(xs):
            engineer(c, px, -62, 112 + i * 8, SHIRTS[(0, 2)[i]], t + i * 0.4, pose, face=1)
        # gulls
        if t >= s("break1") - 0.3:
            for i in range(3):
                u = prog(t, s("break1") - 0.3 + i * 0.35, T["seagulls"] + 0.2 + i * 0.5)
                if i == 0:
                    gx, gy = lerp(760, bx + 92, e_out(u)), lerp(-430, by - 84, e_io(u)) - 60 * math.sin(u * math.pi)
                    gull(c, gx, gy, 1.0, t, sit=u >= 1, face=-1)
                elif 0 < u < 1:
                    gull(c, lerp(820, -700, u), -330 - i * 70 + math.sin(u * 9 + i) * 24, 0.8, t + i, face=-1)
        self.waves(c, t, cam)
        splash(c, -20, 0, t, T["splash"], 1.0, n=34, speed=720, width=1.4)
        splash(c, 10, 0, t, T["splash"] + 0.12, 0.8, n=18, speed=520, seed=7)
        c.restore()
        self.ui["cam"] = cam
        self.ui["barrel"] = (bx, by)

    # ------------------------------------------------------------------ set: ballast tanks
    def draw_tanks(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["tanks"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        self.water(c, t, cam)
        self.view(c, cam)
        vy = self.vy.at(t) + math.sin(t * 1.7) * 5 * (1 - self.fill.at(t))
        fill, vent, blow = self.fill.at(t), self.vent.at(t), self.blowk.at(t)
        gull(c, 420 + (t - s("fix1")) * 60, -260 - (t - s("fix1")) * 30, 0.9, t, face=1)
        c.save()
        c.translate(0, vy)
        c.rotate(math.sin(t * 1.3) * 3 * (1 - fill))
        tanks(c, fill, vent, blow, prog(t, T["ballast"] - 0.15, T["ballast"] + 0.2))
        barrel(c, 0.0, 1.0, cut=1.0)
        engineer(c, 30, 50, 86, SHIRTS[1], t, "sit" if blow <= 0 else "cheer", face=1)
        c.restore()
        if vent > 0.5 and fill < 1:                                                  # air leaves by the vents
            for sd in (-1, 1):
                bubbles(c, sd * 108, vy + 40, t, T["vents"] + 0.1, T["sink"], rate=14, life=1.2, spread=14, rise=260, seed=3 + sd)
        if blow > 0:                                                                 # ... and water by the holes in the bottom
            for sd in (-1, 1):
                bubbles(c, sd * 68, vy + 150, t, T["blow"] + 0.1, T["rise"] - 0.2, rate=18, life=1.0, spread=30, rise=200, seed=6 + sd)
        self.waves(c, t, cam)
        c.restore()
        self.ui["cam"] = cam
        self.ui["vy"] = vy

    # ------------------------------------------------------------------ set: deep water
    def draw_deep(self, c, t):
        T, s = self.T, self.tl.s
        first = t < s("fix2") - 0.12
        if first:                                                                    # ---- the dive and the crushed barrel
            vy = self.dy.at(t)
            if t >= T["crush3"] + 0.3:
                vy += 700 * e_in(prog(t, T["crush3"] + 0.3, T["crush3"] + 1.6))
            cam = (math.sin(t * 0.6) * 4, self.dy.at(t) + 70, 1.9)
            self.water(c, t, cam)
            self.view(c, cam)
            cr = self.crush.at(t)
            c.save()
            c.translate(0, vy)
            c.rotate(math.sin(t * 2.3) * 2 + cr * 6)
            tanks(c, 1.0, 0.0, 0.0, 1.0)
            barrel(c, cr, 1.0, seed=4)
            c.restore()
            arrows_in(c, 0, self.dy.at(t) + 30, 150, 110, 8, prog(t, T["deep"], T["deep"] + 0.4) * (1 - prog(t, T["crush3"] + 0.2, T["crush3"] + 0.5)), t)
            bubbles(c, 0, vy - 60, t, s("break2"), None, rate=7, life=1.6, spread=60, rise=300, seed=9)
            if t >= T["crush3"] + 0.1:                                               # the crew leaves in a bubble
                u = e_out(prog(t, T["crush3"] + 0.1, T["crush3"] + 1.1))
                self.crew_bubble(c, t, math.sin(t * 2) * 10, lerp(1500 - 30, HY, u), u)
                bubbles(c, 0, 1500 - 40, t, T["crush3"], T["crush3"] + 0.5, rate=40, life=1.4, spread=120, rise=420, seed=11)
            self.waves(c, t, cam)
            c.restore()
            self.ui["cam"] = cam
            self.ui["depth"] = clamp(self.dy.at(t) / 1500)
            return
        # ---- the pressure hull, the mountain, the sonar
        hx = self.hx.at(t)
        cam = (hx + clamp(hx / 1100) * 110 + math.sin(t * 0.6) * 4, HY + 130, 1.5 - 0.12 * clamp(hx / 1100))
        self.water(c, t, cam, self.dark.at(t))
        self.view(c, cam)
        # the mountain
        lit = (prog(t, T["ping"] + 0.3, T["ping"] + 0.5) * (1 - prog(t, T["ping"] + 1.6, T["ping"] + 2.4))) if t >= T["ping"] else 0.0
        flash = 1 - prog(t, T["crash"], T["crash"] + 0.7) if t >= T["crash"] else 0.0
        mt = skia.Path()
        pts = ((1380, HY + 900), (1440, HY + 300), (1400, HY + 130), (1452, HY - 60), (1500, HY - 300), (1700, HY - 620), (2100, HY - 900),
               (2600, HY - 1000), (2600, HY + 900))
        mt.moveTo(*pts[0])
        for p in pts[1:]:
            mt.lineTo(*p)
        mt.close()
        c.drawPath(mt, lin_paint(1380, 0, 2300, 0, [mix("#0E1E36", "#31506F", clamp(flash + lit * 0.5)), "#070E1C"]))
        edge = skia.Path()
        edge.moveTo(*pts[0])
        for p in pts[1:8]:
            edge.lineTo(*p)
        c.drawPath(edge, P("#5B7FA6", 0.25 + 0.4 * flash, stroke=5))
        if lit > 0:
            c.drawPath(edge, P("#22D3EE", 0.9 * lit, stroke=7))
            c.drawPath(edge, P("#22D3EE", 0.4 * lit, stroke=22, blur=12))
        # the hull
        built = t >= T["pressure"] - 0.1
        if not built:
            self.crew_bubble(c, t, math.sin(t * 2) * 10, HY + math.sin(t * 1.5) * 6, 1.0)
        else:
            moving = T["dark"] - 0.4 <= t < T["crash"]
            c.save()
            c.translate(hx, HY + math.sin(t * 1.2) * 4)
            c.rotate(-6 * bump(t, T["crash"], T["crash"] + 0.5))

            def inner(c, t):
                lost = T["windows"] - 0.1 <= t < T["sonar"] - 0.2
                pose = "cheer" if t < T["dark"] - 0.4 and t >= T["spreads"] + 0.3 else "stand"
                pose = "duck" if T["crash"] <= t < T["crash"] + 0.8 else "shrug" if lost else "point" if T["ping"] <= t else pose
                self.crew_in(c, t, pose, xs=(-70, 20, 110))
                if lost and t < T["crash"]:
                    for i, px in enumerate((-70, 20, 110)):
                        text(c, "?", px + 4, -62 - 6 * math.sin(t * 5 + i), 40, HILITE, "Poppins-Black")

            self.hull_cut(c, t, tube=prog(t, T["pressure"] - 0.1, T["pressure"] + 0.3), ends=prog(t, T["rounded"] - 0.05, T["rounded"] + 0.25),
                          rings=clamp((t - T["rings"] + 0.15) / (0.07 * len(RINGS))), dome=prog(t, T["sonar"] - 0.05, T["sonar"] + 0.25), inner=inner)
            if t >= T["spreads"] + 0.3 and t < T["dark"]:
                c.drawRRect(rr(-HL - 6, -HR - 6, 2 * HL + 12, 2 * HR + 12, HR + 6), P(GOOD, 0.8 * (1 - prog(t, T["spreads"] + 0.3, T["spreads"] + 1.4)), stroke=8))
            c.restore()
            arrows_in(c, hx, HY, HL - 10, HR - 6, 14, prog(t, T["spreads"] - 0.4, T["spreads"]) * (1 - prog(t, T["dark"] - 0.6, T["dark"] - 0.2)), t, "#E0F2FE", 12)
            if moving:
                bubbles(c, hx - HL, HY, t, T["dark"] - 0.3, T["crash"], rate=16, life=1.0, spread=40, rise=120, seed=13)
            if t >= T["crash"]:
                v2.debris(c, 1440, HY + 10, t, T["crash"], 1.6, n=14, speed=520, seed=5, gravity=420, cols=("#5B7FA6", "#31506F", "#1B2E4A"),
                          cone=(120, 240), size=(10, 30))
                bubbles(c, 1420, HY, t, T["crash"], T["crash"] + 0.4, rate=40, life=1.3, spread=90, rise=320, seed=15)
            for k0, back in ((T["ping"], False), (T["ping"] + 0.22, False), (T["echo"], True), (T["echo"] + 0.22, True)):
                u = prog(t, k0, k0 + 0.75)                                           # the ping goes out, the echo comes back
                if 0 < u < 1:
                    px = (hx + 250 + 190 * u) if not back else (1440 - 190 * u)
                    r = 60 + 90 * (u if not back else 1 - u * 0.5)
                    c.drawArc(R(px - r, HY - r, 2 * r, 2 * r), -50 if not back else 130, 100, False,
                              P("#67E8F9" if not back else "#FDE047", (1 - u) * 0.95, stroke=7))
        c.restore()
        self.ui["cam"] = cam
        self.ui["hx"] = hx

    def crew_bubble(self, c, t, x, y, k):
        c.drawCircle(x, y, 96, P("#BFEFFF", 0.14))
        c.drawCircle(x, y, 96, P("#E6FAFF", 0.9, stroke=4))
        c.drawArc(R(x - 80, y - 80, 160, 160), 200, 50, False, P("#FFFFFF", 0.8, stroke=6))
        for i, col in enumerate(SHIRTS):
            engineer(c, x - 46 + i * 46, y + 62, 84, col, t + i * 0.4, "shrug" if k >= 1 else "duck", wet=1.0)

    # ------------------------------------------------------------------ set: periscope depth
    def draw_peri(self, c, t):
        T = self.T
        cam = self.cams["peri"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        self.water(c, t, cam)
        self.view(c, cam)
        bob = math.sin(t * 1.6) * 5
        c.drawLine(330, 0, 330, 260, P("#3F465A", 0.8, stroke=3))                     # a buoy, and somebody on it
        c.save()
        c.translate(330, bob)
        c.rotate(math.sin(t * 1.4) * 4)
        box(c, -26, -40, 52, 56, "#EF4444", r=10)
        c.drawRect(R(-26, -18, 52, 12), P("#F8FAFC"))
        c.drawRect(R(-3, -74, 6, 34), P("#8E97AD"))
        gull(c, 0, -76, 1.0, t, sit=True, face=-1)
        c.restore()
        mast = e_out(prog(t, T["periscope"] - 0.05, T["periscope"] + 0.45))

        def inner(c, t):
            self.station(c, t, 0.0)
            self.crew_in(c, t, "look", xs=(-90, 6, 120))

        c.save()
        c.translate(0, 215 + math.sin(t * 1.2) * 3)
        self.hull_cut(c, t, sail=1.0, mast=mast, dome=1.0, inner=inner)
        c.restore()
        self.waves(c, t, cam)
        if mast > 0.6:
            c.save()
            c.translate(48, 0)
            c.scale(1, 0.25)
            for i in range(2):
                u = (t * 0.8 + i * 0.5) % 1.0
                c.drawCircle(0, 0, 14 + 60 * u, P("#FFFFFF", 0.6 * (1 - u), stroke=5))
            c.restore()
        c.restore()
        self.ui["cam"] = cam

    # ------------------------------------------------------------------ set: inside the hull
    def station(self, c, t, game=0.0):
        """The periscope column and the sonar desk (inside the hull, hull coordinates)."""
        c.drawRect(R(16, -HR, 12, 108), lin_paint(16, 0, 28, 0, ["#DDE3EE", "#5B657E"]))
        c.drawRRect(rr(0, -22, 44, 9, 4), P("#3F465A"))
        c.drawRRect(rr(12, -32, 20, 22, 5), P("#2B3550"))
        box(c, 76, 14, 92, 46, "#3F4A68", r=6)                                       # the desk
        if game <= 0:
            c.drawCircle(122, -22, 30, P("#04120F"))
            c.drawCircle(122, -22, 30, P("#34D399", 0.8, stroke=3))
            c.drawCircle(122, -22, 15, P("#34D399", 0.35, stroke=2))
            a = t * 3.2
            c.drawLine(122, -22, 122 + math.cos(a) * 28, -22 + math.sin(a) * 28, P("#6EE7B7", 0.9, stroke=3))
            c.drawCircle(136, -34, 4, P("#FDE047", 0.5 + 0.5 * math.sin(t * 5)))
            add_glow(c, 122, -22, 60, "#34D399", 0.35)
        else:                                                                        # the periscope picture, on a screen
            pan = math.sin(t * 2.6) * 10 * game
            c.drawRRect(rr(72, -70, 100, 72, 6), P("#11151F"))
            c.save()
            c.clipRect(R(77, -65, 90, 62))
            vrect(c, 77, -65, 90, 40, ["#2B2466", "#B25A72"])
            vrect(c, 77, -27, 90, 26, ["#16295A", "#0C1738"])
            box(c, 112 + pan, -40, 14, 16, "#EF4444", r=3)
            gull(c, 119 + pan, -42, 0.36, t, sit=True, face=-1)
            c.restore()
            c.drawLine(122, -65, 122, -3, P("#4ADE80", 0.8, stroke=1.5))
            c.drawLine(77, -30, 167, -30, P("#4ADE80", 0.8, stroke=1.5))
            c.drawCircle(122, -30, 14, P("#4ADE80", 0.8, stroke=1.5))
            add_glow(c, 122, -34, 80, "#7DD3FC", 0.3)

    def inside_stuff(self, c, t):
        T, s = self.T, self.tl.s
        tag = t >= s("tag") - 0.2
        self.station(c, t, 1.0 if tag else 0.0)
        # pantry
        box(c, 176, -52, 78, 112, "#3F4A68", r=5)
        left = 12
        if t >= T["food0"] + 0.5:
            left = max(1, 12 - int((t - T["food0"] - 0.5) / 0.11))
        if tag:
            left = 1
        for i in range(12):
            if i < left:
                can(c, 183 + (i % 4) * 18, -22 + (i // 4) * 36, ("#EF4444", "#22C55E", "#FACC15", "#38BDF8")[(i * 7) % 4])
        for sy in (-22, 14, 50):
            c.drawRect(R(178, sy, 74, 4), P("#7C8499"))
        # scrubber and oxygen maker
        if t >= T["scrubbers"] - 0.1:
            k = e_back(prog(t, T["scrubbers"] - 0.1, T["scrubbers"] + 0.2))
            c.save()
            c.translate(-176, 58)
            c.scale(k, k)
            box(c, -36, -104, 72, 104, "#64748B", r=8)
            c.drawCircle(0, -70, 24, P("#11151F"))
            for b in range(4):
                a = t * 14 + b * math.pi / 2
                c.drawLine(0, -70, math.cos(a) * 20, -70 + math.sin(a) * 20, P("#CBD5E1", 0.9, stroke=6))
            for i in range(3):
                c.drawRect(R(-24, -34 + i * 10, 48, 5), P("#22D3EE", 0.8))
            c.drawCircle(22, -96, 4, P(GOOD))
            c.restore()
        if t >= T["machine"] - 0.1:
            k = e_back(prog(t, T["machine"] - 0.1, T["machine"] + 0.2))
            c.save()
            c.translate(-84, 58)
            c.scale(k, k)
            box(c, -34, -16, 68, 16, "#475569", r=4)
            c.drawRRect(rr(-30, -98, 60, 84, 10), P("#0B2A4A"))
            vrect(c, -30, -74, 60, 60, ["#38BDF8", "#0E6BA8"], r=8)
            c.drawRRect(rr(-30, -98, 60, 84, 10), P("#E0F2FE", 0.8, stroke=3))
            for ex in (-14, 14):
                c.drawRect(R(ex - 3, -92, 6, 70), P("#E5E9F2"))
            c.drawRect(R(-4, -116, 8, 20), P("#94A3B8"))
            c.restore()
            if k >= 1:
                bubbles(c, -98, 30, t, T["machine"] + 0.2, None, rate=9, life=0.5, spread=3, rise=110, size=(2, 5), seed=21)
                bubbles(c, -70, 30, t, T["machine"] + 0.2, None, rate=14, life=0.5, spread=3, rise=110, size=(2, 5), seed=22)
                for i in range(5):                                                   # oxygen drifting into the room
                    u = ((t - T["machine"]) * 0.5 + i / 5) % 1.0
                    ox, oy = -84 + (i - 2) * 26 + math.sin(u * 6 + i) * 14, -104 + 40 * math.sin(u * math.pi) - 10 * u
                    c.drawCircle(ox + 60 * u * (1 if i % 2 else -0.4), oy, 7, P("#7DD3FC", 0.75 * (1 - u), stroke=3))
        # the crew
        if tag:
            engineer(c, -14, 58, 96, SHIRTS[1], t, "sit", face=1)                    # the helmsman and his controller
            wig = math.sin(t * 9) * 3 if t >= T["steer"] else 0.0
            c.save()
            c.translate(26, -2 + wig * 0.3)
            c.rotate(wig)
            c.drawRRect(rr(-22, -9, 44, 18, 9), P("#1F2937"))
            c.drawCircle(-18, 6, 9, P("#1F2937"))
            c.drawCircle(18, 6, 9, P("#1F2937"))
            c.drawCircle(-11, -1, 4, P("#94A3B8"))
            for j, col in enumerate(("#4ADE80", "#EF4444", "#38BDF8", "#FACC15")):
                c.drawCircle(11 + (j % 2) * 7 - 3, -3 + (j // 2) * 6, 2.6, P(col))
            c.restore()
            engineer(c, -110, 58, 100, SHIRTS[0], t + 0.4, "look" if t < T["mom"] else "shrug", face=1)
            if t >= T["mom"] - 0.15:                                                 # the phone on the desk lights up
                pk = e_back(prog(t, T["mom"] - 0.15, T["mom"] + 0.1))
                c.save()
                c.translate(150, 12)
                c.rotate(math.sin(t * 40) * 4)
                c.scale(pk, pk)
                c.drawRRect(rr(-11, -40, 22, 40, 5), P("#0B1220"))
                c.drawRRect(rr(-8, -36, 16, 28, 3), P("#FDF2F8"))
                heart(c, 0, -24, 0.5, 1.0)
                c.restore()
                add_glow(c, 150, -10, 44, "#FB7185", 0.6 * pk)
        else:
            st = self.stale.at(t)
            sore = prog(t, T["crew"], T["crew"] + 0.3) * (1 - prog(t, T["scrubbers"] + 0.4, T["dioxide"] + 0.3))
            pose = "duck" if sore > 0.5 else "cheer" if T["oxygen"] + 0.2 <= t < T["food0"] + 0.4 else "look" if t >= T["food0"] + 0.4 else "stand"
            self.crew_in(c, t, pose, xs=(-36, 60, 150) if t < self.tl.s("fix4") + 0.3 else (-30, 48, 128), sore=sore)
            if st > 0:                                                               # stale air
                c.drawRect(R(-HL, -HR, 2 * HL, 2 * HR), P("#A3B32A", 0.34 * st))
                rng = random.Random(5)
                for i in range(16):
                    px = (rng.uniform(-260, 260) + t * rng.uniform(-18, 18))
                    py = rng.uniform(-90, 40) + math.sin(t * 0.9 + i) * 10
                    if t >= T["scrubbers"] + 0.3:                                    # ... on its way into the scrubber
                        u = prog(t, T["scrubbers"] + 0.3, T["dioxide"] + 0.3)
                        px, py = lerp(px, -176, e_in(u)), lerp(py, -12, e_in(u))
                    puff(c, px, py, rng.uniform(26, 44), "#C7D64A", 0.42 * st, k=i)

    def draw_inside(self, c, t):
        cam = self.cams["inside"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 2, cam[1], cam[2])
        z = cam[2]
        underwater(c, W, H, t, "#0D3558", "#082240", "#030A18", rays=False)
        self.view(c, cam)
        bubbles(c, -330, 40, t, 0.0, None, rate=3, life=2.6, spread=30, rise=90, seed=31)
        self.hull_cut(c, t, sail=1.0, dome=1.0, inner=self.inside_stuff)
        c.restore()
        self.ui["cam"] = cam

    # ------------------------------------------------------------------ set: the finished boat
    def draw_wide(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["wide"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        self.water(c, t, cam)
        self.view(c, cam)
        wy = self.wy.at(t) + math.sin(t * 1.2) * 4
        cruising = T["s1"] - 0.3 <= t < s("closer") - 0.3
        if cruising:
            whale(c, 330 - (t - T["s1"]) * 30, 900 + 190, 1.25, t, 0.5)
        up = wy < 140
        tail = prog(t, s("reveal") - 0.1, T["propeller"] - 0.1) if t < T["propeller"] else 1.0
        if t < s("reveal") - 0.1:
            tail = 0.0
        onto = up and (t < T["nobody"] + 0.1 or t >= s("closer") + 0.35)
        if onto:                                                                     # the crew on deck
            hop = prog(t, T["nobody"] - 0.25, T["nobody"] + 0.1) if t < s("closer") else 0.0
            pose = "cheer" if (t >= s("closer") or T["black"] + 0.3 <= t) else "stand" if t < T["propeller"] else "look"
            for i, col in enumerate(SHIRTS):
                px = lerp((-150, -96, 150)[i], 30, e_in(hop))
                engineer(c, px, wy - HR + 4 + 40 * hop, 104 + (i % 2) * 8, col, t + i * 0.37, pose, face=1 if i < 2 else -1)
            if t >= s("closer"):
                hats_in_the_air(c, (-150, -96, 150), wy - HR - 150, t, T["cong2"])
        c.save()
        c.translate(0, wy)
        c.rotate(8 * bump(t, T["nobody"] + 0.35, T["gone"]) - 10 * bump(t, s("closer") - 0.3, s("closer") + 0.4))
        sub_out(c, t, self.paintk.at(t), tail, e_back(prog(t, T["propeller"] - 0.1, T["propeller"] + 0.2)))
        c.restore()
        if tail >= 1:
            bubbles(c, -470, wy, t, T["propeller"], None, rate=12, life=1.0, spread=30, rise=110, seed=41)
        if T["nobody"] + 0.35 <= t < T["s1"]:
            bubbles(c, 0, min(wy, 500), t, T["nobody"] + 0.4, T["gone"] + 0.4, rate=26, life=1.8, spread=240, rise=300, seed=43)
        self.waves(c, t, cam)
        splash(c, 150, 0, t, s("closer") + 0.25, 1.1, n=40, speed=820, width=1.8)
        splash(c, -180, 0, t, s("closer") + 0.32, 1.0, n=30, speed=700, width=1.6, seed=9)
        if T["nobody"] + 0.5 <= t < T["s1"] - 0.2:                                    # only a gull knows
            gull(c, 60, -6 + math.sin(t * 1.6) * 3, 1.1, t, sit=True, face=-1)
        c.restore()
        self.ui["cam"] = cam
        self.ui["wy"] = wy

    def whip_backdrop(self, c, t, m):
        underwater(c, W, H, t, "#0D3558", "#082240", "#030A18", rays=False)

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def ui_shore(self, c, t, tw):
        T, s = self.T, self.tl.s
        bx, by = self.ui.get("barrel", (0, 0))
        px, py = self.at(bx, by - 70)
        if tw < T["roll"] - 0.1:
            self.label(px + 40, py, px + 250, py - 190, "barrel", T["barrel"] - 0.25, T["roll"] - 0.15, HILITE)
        self.badge("alert", T["bob"], s("fix1") - 0.2)
        self.red(T["bob"], 1.8)

    def ui_tanks(self, c, t, tw):
        T, s = self.T, self.tl.s
        vy = self.ui.get("vy", 0)
        tx, ty = self.at(70, vy + 108)
        self.label(tx + 40, ty + 20, 840, ty + 110, "tank", T["ballast"] + 0.2, T["vents"] - 0.1, "#38BDF8")
        vx, vyy = self.at(108, vy + 44)
        self.label(vx, vyy, 840, vyy - 190, "vent", T["vents"] + 0.1, T["floods"] + 0.3, GOOD)
        ax, ay = self.at(0, vy + 165)
        self.label(ax - 60, ay + 4, 215, ay + 4, "air", T["blow"] + 0.15, T["rise"] - 0.1, "#FDBA74")
        self.badge("check", T["rise"] + 0.2, s("break2") - 0.15)

    def ui_deep(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            p = self.span(s("break2") + 0.1, s("fix2") - 0.25)
            if p > 0:
                v2.gauge(c, 60, 300, [(self.L["depth"], self.ui.get("depth", 0), mix("#38BDF8", WARN, self.ui.get("depth", 0)))], p, w=320)
            self.badge("alert", T["squeezes"], s("fix2") - 0.2)
            self.red(T["squeezes"], 2.0)
            return
        hx = self.ui.get("hx", 0)
        if tw < s("break3"):
            x0, y0 = self.at(hx - 60, HY - HR)
            self.label(x0, y0, 300, y0 - 190, "hull", T["pressure"] + 0.25, T["thick"] - 0.05)
            x1, y1 = self.at(hx + 120, HY + HR - 7)
            self.label(x1, y1, 800, y1 + 150, "thick", T["thick"] + 0.05, T["rounded"] - 0.05, HILITE)
            x2, y2 = self.at(hx + RINGS[2], HY - HR + 24)
            self.label(x2, y2, 300, y2 - 250, "rings", T["rings"] + 0.3, T["spreads"] - 0.2)
            self.badge("check", T["spreads"] + 0.4, s("break3") - 0.15)
        elif tw < s("fix3"):
            x0, y0 = self.at(hx, HY - HR)
            self.chip(x0, y0 - 100, "nowin", T["windows"] - 0.15, T["drove"] + 0.1, accent=WARN, size=38)
            self.badge("alert", T["crash"], s("fix3") - 0.2)
            self.red(T["crash"], 2.0)
        else:
            x0, y0 = self.at(hx + 214, HY)
            self.label(x0, y0 - 30, x0 - 250, y0 - 330, "sonar", T["sonar"] + 0.2, T["ping"] + 0.5, "#22D3EE")

    def ui_peri(self, c, t, tw):
        T, s = self.T, self.tl.s
        mx, my = self.at(39, -100)
        self.label(mx - 14, my, mx - 250, my - 150, "peri", T["periscope"] + 0.35, T["peek"] + 0.1, "#7DD3FC")
        p = self.span(T["peek"], s("break4") - 0.2, 0.3, 0.2)
        if p > 0:                                                                    # what the periscope sees
            cx_, cy_, r = 800, 400, 150 * e_back(p)
            c.save()
            cp = skia.Path()
            cp.addCircle(cx_, cy_, r)
            c.clipPath(cp, skia.ClipOp.kIntersect, True)
            vrect(c, cx_ - r, cy_ - r, 2 * r, r * 1.2, ["#1B1C4A", "#74406F", "#FF9D73"])
            vrect(c, cx_ - r, cy_ + r * 0.2, 2 * r, r * 0.8, ["#16295A", "#0C1738"])
            bob = math.sin(t * 1.6) * 4
            box(c, cx_ - 30, cy_ - 20 + bob, 60, 64, "#EF4444", r=10)
            c.drawRect(R(cx_ - 30, cy_ + 4 + bob, 60, 13), P("#F8FAFC"))
            gull(c, cx_, cy_ - 24 + bob, 1.7, t, sit=True, face=-1)
            c.restore()
            c.drawCircle(cx_, cy_, r, P("#0B1220", p, stroke=14))
            c.drawCircle(cx_, cy_, r, P("#4ADE80", 0.9 * p, stroke=3))
            c.drawLine(cx_ - r, cy_, cx_ + r, cy_, P("#4ADE80", 0.7 * p, stroke=2))
            c.drawLine(cx_, cy_ - r, cx_, cy_ + r, P("#4ADE80", 0.7 * p, stroke=2))
        self.badge("check", T["surface"], s("break4") - 0.15, x=230, y=470)

    def ui_inside(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw >= s("tag") - 0.2:
            self.chip(540, 400, "train", T["training"] - 0.05, self.duration + 1, accent=HILITE, size=44)
            return
        p = self.span(s("break4") + 0.3, T["food0"] + 0.2)
        if p > 0:
            st = self.stale.at(tw)
            v2.gauge(c, 60, 250, [(self.L["co2"], 0.12 + 0.8 * st, mix(GOOD, WARN, st)), (self.L["o2"], self.oxy.at(tw), "#38BDF8")], p, w=380)
        if tw < s("fix4"):
            self.badge("alert", T["crew"], s("fix4") - 0.2, x=880, y=330)
            self.red(T["crew"], 1.8)
        else:
            x0, y0 = self.at(-176, -46)
            self.label(x0, y0, 250, y0 + 440, "scrub", T["scrubbers"] + 0.2, T["machine"] - 0.2, "#22D3EE")
            x1, y1 = self.at(-84, -40)
            self.label(x1, y1, 760, y1 + 430, "o2m", T["machine"] + 0.2, T["food0"] + 0.1, "#38BDF8")
            self.badge("check", T["oxygen"] + 0.3, 1e9, x=880, y=330)
            x2, y2 = self.at(215, -52)
            self.label(x2, y2, 330, y2 - 190, "food", T["food0"] + 0.75, self.tl.e("fix4") + 0.8, HILITE)

    def ui_wide(self, c, t, tw):
        T, s = self.T, self.tl.s
        if s("reveal") <= tw < T["s1"] - 0.3:
            wy = self.ui.get("wy", 95)
            px, py = self.at(-450, wy)
            self.label(px, py - 20, 250, py - 330, "prop", T["propeller"] + 0.15, T["paint"] + 0.3, HILITE)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["seal"], sfx.clank(520, 0.3, 61), -3), (T["roll"], rumble(0.9, 62), -8),
              (T["roll"] + 0.3, sfx.thud(0.3, 63), -7), (T["roll"] + 0.62, sfx.thud(0.3, 64), -7), (T["splash"], water_snd(0.9, 65), -2),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 66), -9)]
        ev += [(T["floats"] - 0.3, sfx.pop(67), -9), (T["bob"], sfx.alarm(3, 820), -11), (T["bob"] + 0.1, water_snd(0.5, 68), -12),
               (T["seagulls"] - 0.3, sfx.creak(0.35, 69), -9), (T["seagulls"] + 0.1, sfx.creak(0.3, 70), -8), (T["seagulls"] + 0.3, sfx.womp(), -11)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["ballast"] - 0.15, sfx.clank(300, 0.3, 72), -5),
               (T["ballast"], sfx.clank(280, 0.3, 73), -6), (T["vents"], sfx.lock_click(74), -4), (T["vents"] + 0.1, gas_hiss(0.8, 75), -8),
               (T["floods"] - 0.15, water_snd(1.0, 76), -7), (T["sink"] - 0.3, bubble_snd(1.0, 77), -7),
               (T["blow"] + 0.25, gas_hiss(1.2, 78), -8), (T["blow"] + 0.5, bubble_snd(1.1, 79), -9), (T["rise"] + 0.1, water_snd(0.5, 80), -8),
               (T["rise"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, True, 81), -4), (T["dive"] - 0.4, bubble_snd(1.4, 82), -9),
               (T["deep"], rumble(1.6, 83), -9), (T["squeezes"], crunch(84), -2), (T["squeezes"] + 0.02, sfx.alarm(3, 820), -11),
               ((T["squeezes"] + T["crush3"]) / 2, crunch(85), -2), (T["crush3"], crunch(86, 0.6), 0), (T["crush3"] + 0.1, bubble_snd(1.2, 87), -5)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 88), -4), (T["pressure"] - 0.1, sfx.thud(0.4, 89), -4),
               (T["thick"], sfx.pop(90), -7), (T["rounded"] - 0.05, sfx.clank(240, 0.5, 91), -3)]
        ev += [(T["rings"] - 0.15 + i * 0.07, sfx.clank(700 + i * 40, 0.14, 92 + i), -8) for i in range(len(RINGS))]
        ev += [(T["spreads"] - 0.4, rumble(1.0, 103), -9), (T["spreads"] + 0.3, sfx.chime(), -6)]
        ev += [(T["dark"] - 0.3, sfx.power_down(1.0, 104), -9), (T["dark"] - 0.3, sfx.hum(2.4, 70), -14),
               (T["windows"] - 0.1, sfx.pop(105), -7), (T["crash"], boom(1.2, 106), 0), (T["crash"] + 0.02, sfx.clank(180, 0.8, 107), -3),
               (T["crash"] + 0.1, sfx.alarm(3, 820), -10)]
        ev += [(T["sonar"] - 0.05, sfx.pop(108), -5), (T["ping"], ping_snd(1500), -3), (T["echo"], ping_snd(1100, 0.9), -9),
               (T["periscope"] - 0.35, sfx.whoosh(0.4, False, 109), -5), (T["periscope"] - 0.05, sfx.whirr(0.5, 180, 300, 110), -9),
               (T["peek"], sfx.pop(111), -6), (T["peek"] + 0.3, sfx.creak(0.3, 112), -9), (T["surface"], sfx.chime(), -7)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 113), -4), (T["stale"] - 0.5, sfx.power_down(1.3, 114), -11),
               (T["crew"], sfx.alarm(3, 820), -11), (T["headache"], sfx.womp(), -9)]
        ev += [(T["scrubbers"] - 0.1, sfx.thud(0.3, 115), -5), (T["scrubbers"] + 0.2, sfx.whirr(1.6, 200, 320, 116), -12),
               (T["machine"] - 0.1, sfx.thud(0.3, 117), -5), (T["machine"] + 0.2, bubble_snd(1.3, 118), -9), (T["oxygen"] + 0.3, sfx.chime(), -6)]
        ev += [(T["food0"] + 0.5 + i * 0.11, sfx.pop(119 + i), -10) for i in range(11)]
        ev += [(T["pause"], sfx.click(131), 0), (T["follow"] - 0.15, sfx.pop(132), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 133), -7),
               (s("cta") + 0.2, water_snd(0.6, 134), -10)]
        ev += [(T["propeller"] - 0.1, sfx.clank(320, 0.4, 135), -4), (T["propeller"] + 0.1, sfx.whirr(1.2, 90, 190, 136), -10),
               (T["paint"] - 0.05, sfx.whoosh(0.7, False, 137), -6), (T["black"] + 0.3, sfx.sparkle(0.5, 6, 138), -9),
               (T["nobody"] + 0.35, bubble_snd(1.4, 139), -6), (T["nobody"] + 0.3, gas_hiss(0.9, 140), -9), (T["gone"] + 0.3, sfx.creak(0.3, 141), -9)]
        ev += [(T["s1"], sfx.pop(142), -3), (T["s2"], sfx.pop(143), -3), (T["s3"], sfx.pop(144), -3), (T["s1"] - 0.3, sfx.whoosh(1.2, False, 145), -12),
               (T["s2"] + 0.2, ping_snd(1300, 1.2), -13)]
        ev += [(s("closer") + 0.25, water_snd(1.0, 146), -3), (T["cong2"], sfx.pop(147), -2), (T["cong2"], sfx.sparkle(1.0, 14, 148), -4),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 149), -6), (T["steer"], sfx.beep(1300, 0.06), -9), (T["steer"] + 0.18, sfx.beep(1600, 0.06), -9),
               (T["controller"], sfx.beep(1900, 0.08), -8), (T["mom"] - 0.15, sfx.ring(0.6), -9), (T["training"] + 0.4, sfx.womp(), -3)]
        return ev


NAME = "submarine"
EPISODE = Submarine
