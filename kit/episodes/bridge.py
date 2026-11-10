"""Episode 16 - A suspension bridge.  v2 look: one world and two close-up boards.

span     the strait from the side: water surface at y = 0, banks beyond x = +-470, the road at y = -130, towers at
         x = +-260 (tops at y = -520), anchorages at x = +-560.  (Cartoon proportions: a real span is far longer.)
section  the deck cut across, with the wind going past it (drawn straight on the screen)
joint    the road from above, with its finger joint (drawn straight on the screen)
"""
from v2_base import *  # noqa: F401,F403

TW, TOP, DECK, ANCH, MID, BANK = 260, -520, -130, 560, -200, 470
GRAY, ORANGE, ORANGE_D = "#9AA6BA", "#F0603A", "#B8391C"


def cable_y(x):
    ax = abs(x)
    if ax <= TW:
        return MID + (TOP - MID) * (x / TW) ** 2
    u = clamp((ANCH - ax) / (ANCH - TW))                    # 0 at the anchorage, 1 at the tower
    return lerp(-150, TOP, u) + 26 * math.sin(math.pi * u)


def car(c, x, y, col="#F8FAFC", rot=0.0, s=1.0, face=1):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s * face, s)
    c.drawRRect(rr(-24, -20, 48, 14, 5), P(col))
    c.drawRRect(rr(-13, -31, 26, 14, 6), P(col))
    c.drawRRect(rr(-9, -28, 18, 8, 3), P("#1B2238"))
    c.drawCircle(-13, -6, 6.5, P("#111827"))
    c.drawCircle(13, -6, 6.5, P("#111827"))
    c.drawCircle(24, -14, 3, P("#FDE68A"))
    c.restore()


def wind(c, x0, y0, x1, t, n=6, a=1.0, spread=90, seed=0, col="#BAE6FD"):
    for i in range(n):
        u = (t * 0.8 + i / n + seed * 0.3) % 1.0
        yy = y0 + math.sin(i * 7.3 + seed) * spread
        xx = lerp(x0, x1, u)
        p = skia.Path()
        p.moveTo(xx, yy)
        p.cubicTo(xx + 30, yy - 10, xx + 60, yy + 10, xx + 96, yy)
        pr = P(col, 0.8 * a * math.sin(math.pi * u), stroke=5)
        pr.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPath(p, pr)


def buzz_snd(d=1.0):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 210 + 25 * np.sin(2 * np.pi * 5 * tt)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR)) * (0.6 + 0.4 * np.sin(2 * np.pi * 27 * tt))
    return sfx._norm(sfx._bp(x, 150, 2600) * sfx._ar(n, 0.06, 0.25), 0.45)


def creak_snd(d=1.2, seed=3):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 90 + 60 * np.sin(2 * np.pi * 1.4 * tt)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR)) * 0.5 + sfx._bp(sfx._rng(seed).standard_normal(n), 300, 1800) * 0.3
    return sfx._norm(sfx._bp(x, 80, 1500) * sfx._ar(n, 0.2, 0.4), 0.5)


def gust(d=1.4, seed=5):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 250, 1800)
    tt = np.arange(n) / sfx.SR
    return sfx._norm(x * sfx._ar(n, d * 0.35, d * 0.5) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.7 * tt)), 0.6)


# ====================================================================================== the episode
class Bridge(EpisodeV2):
    BUILD_NO = 16
    FIRST_SET = "span"
    CLEAR = "#0B1024"
    TITLE = {"en": "SUSPENSION BRIDGE", "ar_sa": "جسر معلّق"}
    EMPH = {"en": ["CONGRATS", "BRIDGE", "PLANK", "SNAPS", "SWIMMING", "TOWERS", "CABLES", "HANGERS", "LAUNDRY", "YANK", "PEGS", "STRANDS", "EYEBARS",
                   "ANCHORAGE", "CONCRETE", "WIND", "GALLOP", "TWISTED", "TRUSS", "STREAMLINED", "HOT", "GROW", "BUCKLES", "EXPANSION", "FINGERS",
                   "COMBS", "FOLLOW", "MACHINE", "ORANGE", "BEE", "WIRES", "YOURSELF", "PAINT", "DONE"],
            "ar_sa": ["مبروك", "جسر", "لوح", "ينكسر", "يسبح", "برجين", "كيبلين", "بحبال", "الغسيل", "تقلع", "الخيمة", "لخيوط", "قضبان", "قاعدة",
                      "خرسانة", "الهوا", "يتموج", "التوى", "بشبك", "انسيابي", "حار", "يتمدد", "ويتقوّس", "تمدد", "بأصابع", "مشطين", "تابعني",
                      "مكينة", "برتقالي", "نحلة", "سلك", "بيدك", "والصبغ", "خلص"]}
    KEYS = {"ar_sa": {
        ("hook", "PLANK"): "لوح", ("hook", "ACROSS"): "فوق", ("hook", "RIVER"): "نهر", ("hook", "CONGRATS"): "مبروك",
        ("break1", "MILE"): "كيلو", ("break1", "WIDE"): "عرضه", ("break1", "PLANK"): "ولوحك", ("break1", "SNAPS"): "ينكسر", ("break1", "SWIMMING"): "يسبح",
        ("fix1", "TOWERS"): "برجين", ("fix1", "DRAPE"): "وتمد", ("fix1", "CABLES"): "كيبلين", ("fix1", "HANG"): "وتعلّق", ("fix1", "ROAD"): "الطريق",
        ("fix1", "HANGERS"): "بحبال", ("fix1", "LAUNDRY"): "الغسيل", ("fix1", "CLOTHESLINE"): "حبل",
        ("break2", "HANGS"): "معلّق", ("break2", "CABLES"): "الكيابل", ("break2", "YANK"): "تقلع", ("break2", "GROUND"): "الأرض", ("break2", "PEGS"): "الخيمة",
        ("fix2", "FAN"): "فتفرد", ("fix2", "STRANDS"): "لخيوط", ("fix2", "HOOK"): "وتشبكها", ("fix2", "EYEBARS"): "قضبان", ("fix2", "BURY"): "وتدفنها",
        ("fix2", "ANCHORAGE"): "قاعدة", ("fix2", "SIXTY"): "ستين", ("fix2", "TONS"): "طن", ("fix2", "CONCRETE"): "خرسانة",
        ("break3", "WIND"): "الهوا", ("break3", "GALLOP"): "يتموج", ("break3", "NINETEEN"): "ألف", ("break3", "DRIVERS"): "الناس", ("break3", "RIDE"): "يجربون",
        ("break3", "TWISTED"): "التوى", ("break3", "APART"): "وطاح",
        ("fix3", "STIFFEN"): "فتقوّي", ("fix3", "TRUSS"): "بشبك", ("fix3", "SHAPE"): "تخليه", ("fix3", "STREAMLINED"): "انسيابي", ("fix3", "BOX"): "صندوق",
        ("fix3", "SLIDES"): "ينزلق", ("fix3", "PAST"): "الهوا",
        ("break4", "STEADY"): "ثابت", ("break4", "HOT"): "حار", ("break4", "GROW"): "يتمدد", ("break4", "BUCKLES"): "ويتقوّس",
        ("fix4", "CUT"): "فتقص", ("fix4", "GAPS"): "فتحات", ("fix4", "EXPANSION"): "فواصل", ("fix4", "FINGERS"): "بأصابع", ("fix4", "SLIDE"): "تدخل",
        ("fix4", "COMBS"): "مشطين",
        ("cta", "RIBBON"): "الشريط", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PAINT"): "اصبغه", ("reveal", "ORANGE"): "برتقالي", ("reveal", "NAVY"): "البحرية", ("reveal", "BLACK"): "أسود", ("reveal", "STRIPES"): "مخطط",
        ("reveal", "BEE"): "نحلة",
        ("stat", "ONE"): "جسر", ("stat", "TWO"): "برجين", ("stat", "FIFTY"): "وخمسة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "PAINT"): "والصبغ", ("tag", "STARTED"): "بدأ", ("tag", "NINETEEN"): "ألف", ("tag", "STILL"): "ولسا", ("tag", "DONE"): "خلص"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a vending machine"),
                   "stat": [("1", "BRIDGE"), ("2", "TOWERS"), ("55K", "WIRES")],
                   "L": {"plank": "YOUR PLANK", "mile": "1 MILE", "tower": "TOWER", "cable": "MAIN CABLE", "hanger": "HANGERS", "peg": "TENT PEG",
                         "strands": "STRANDS", "eyebar": "EYEBARS", "anch": "ANCHORAGE", "tons": "60,000 TONS", "year": "1940", "truss": "STEEL TRUSS",
                         "flat": "FLAT DECK", "box": "STREAMLINED BOX", "hot": "HOT DAY", "grow": "STEEL GROWS", "joint": "EXPANSION JOINT",
                         "fingers": "STEEL FINGERS", "cold": "COLD", "warm": "HOT", "bee": "THE NAVY'S IDEA", "since": "SINCE 1937"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مكينة بيع"),
                      "stat": [("1", "جسر"), ("2", "برجين"), ("55K", "سلك")],
                      "L": {"plank": "لوحك", "mile": "كيلو ونص", "tower": "برج", "cable": "كيبل رئيسي", "hanger": "حبال حديد", "peg": "وتد خيمة",
                            "strands": "خيوط", "eyebar": "قضبان حديد", "anch": "قاعدة خرسانة", "tons": "ستين ألف طن", "year": "1940", "truss": "شبك حديد",
                            "flat": "طريق مسطّح", "box": "صندوق انسيابي", "hot": "يوم حار", "grow": "الحديد يتمدد", "joint": "فاصل تمدد",
                            "fingers": "أصابع حديد", "cold": "برد", "warm": "حر", "bee": "فكرة البحرية", "since": "من 1937"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "plank": ("hook", "PLANK", 0.3), "across": ("hook", "ACROSS", 0.36), "river": ("hook", "RIVER", 0.5), "congrats": ("hook", "CONGRATS", 0.58),
            "mile": ("break1", "MILE", 0.34), "wide": ("break1", "WIDE", 0.4), "plank2": ("break1", "PLANK", 0.62), "snaps": ("break1", "SNAPS", 0.7),
            "swimming": ("break1", "SWIMMING", 0.92),
            "towers": ("fix1", "TOWERS", 0.16), "drape": ("fix1", "DRAPE", 0.26), "cables": ("fix1", "CABLES", 0.36), "hang": ("fix1", "HANG", 0.54),
            "road": ("fix1", "ROAD", 0.6), "hangers": ("fix1", "HANGERS", 0.7), "laundry": ("fix1", "LAUNDRY", 0.8), "clothesline": ("fix1", "CLOTHESLINE", 0.92),
            "hangs": ("break2", "HANGS", 0.14), "cables2": ("break2", "CABLES", 0.38), "yank": ("break2", "YANK", 0.48), "ground": ("break2", "GROUND", 0.76),
            "pegs": ("break2", "PEGS", 0.94),
            "fan": ("fix2", "FAN", 0.08), "strands": ("fix2", "STRANDS", 0.24), "hook": ("fix2", "HOOK", 0.28), "eyebars": ("fix2", "EYEBARS", 0.38),
            "bury": ("fix2", "BURY", 0.48), "anchorage": ("fix2", "ANCHORAGE", 0.64), "sixty": ("fix2", "SIXTY", 0.74), "tons": ("fix2", "TONS", 0.84),
            "concrete": ("fix2", "CONCRETE", 0.94),
            "wind": ("break3", "WIND", 0.1), "gallop": ("break3", "GALLOP", 0.24), "nineteen": ("break3", "NINETEEN", 0.36), "drivers": ("break3", "DRIVERS", 0.5),
            "ride": ("break3", "RIDE", 0.6), "twisted": ("break3", "TWISTED", 0.84), "apart": ("break3", "APART", 0.94),
            "stiffen": ("fix3", "STIFFEN", 0.1), "truss": ("fix3", "TRUSS", 0.36), "shape": ("fix3", "SHAPE", 0.46), "streamlined": ("fix3", "STREAMLINED", 0.66),
            "box": ("fix3", "BOX", 0.74), "slides": ("fix3", "SLIDES", 0.88), "past": ("fix3", "PAST", 0.95),
            "steady": ("break4", "STEADY", 0.14), "hot": ("break4", "HOT", 0.38), "grow": ("break4", "GROW", 0.68), "buckles": ("break4", "BUCKLES", 0.94),
            "cut": ("fix4", "CUT", 0.1), "gaps": ("fix4", "GAPS", 0.16), "expansion": ("fix4", "EXPANSION", 0.28), "fingers": ("fix4", "FINGERS", 0.62),
            "slide": ("fix4", "SLIDE", 0.72), "combs": ("fix4", "COMBS", 0.95),
            "ribbon": ("cta", "RIBBON", 0.28), "follow": ("cta", "FOLLOW", 0.4),
            "paint": ("reveal", "PAINT", 0.12), "orange": ("reveal", "ORANGE", 0.22), "navy": ("reveal", "NAVY", 0.36), "black": ("reveal", "BLACK", 0.52),
            "stripes": ("reveal", "STRIPES", 0.66), "bee": ("reveal", "BEE", 0.94),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "TWO", 0.3), "s3": ("stat", "FIFTY", 0.52),
            "cong2": ("closer", "CONGRATS", 0.16),
            "paint2": ("tag", "PAINT", 0.14), "started": ("tag", "STARTED", 0.32), "year": ("tag", "NINETEEN", 0.5), "still": ("tag", "STILL", 0.8),
            "done": ("tag", "DONE", 0.95)})
        T["mile0"] = min(T["mile"], T["wide"]) - 0.1
        T["snap"] = T["snaps"] + 0.05
        T["tw"] = T["towers"] - 0.15
        T["cab"] = min(T["drape"], T["cables"]) - 0.1
        T["pull"] = T["yank"] + 0.1                                     # the peg comes out
        T["fan0"] = min(T["fan"], T["strands"])
        T["eye0"] = min(T["hook"], T["eyebars"])
        T["block"] = min(T["bury"], T["anchorage"])
        T["gal"] = T["gallop"] - 0.2
        T["break"] = T["apart"] - 0.1
        T["seccut"] = min(T["shape"], T["streamlined"]) - 0.35
        T["pop"] = T["buckles"] - 0.05
        T["bee0"] = min(T["black"], T["stripes"]) - 0.2
        self.cut(s("fix1") - 0.12, "span", 1)
        self.cut(s("break2") - 0.1, "span", -1)
        self.cut(s("break3") - 0.1, "span", 1)
        self.cut(s("fix3") - 0.12, "span", 1)
        self.cut(T["seccut"], "section", 1)
        self.cut(s("break4") - 0.12, "span", -1)
        self.cut(s("fix4") - 0.12, "joint", 1)
        self.cut(s("cta") + 0.05, "span", -1)
        self.cut(s("reveal") - 0.1, "span", 1)
        self.cut(T["s1"] - 0.35, "span", 1)
        self.cut(s("tag") - 0.2, "span", -1)
        cm = Camera(-440, -150, 2.0)
        cm.key(0.05, -430, -150, 2.2, 1.5)
        cm.key(s("break1") - 0.1, -60, -170, 0.92, 1.0).key(T["plank2"] - 0.5, -220, -170, 1.25, 0.8)
        cm.key(s("fix1") - 0.12, 0, -175, 1.05, 0.0).key(T["laundry"] - 0.6, -120, -270, 1.6, 0.8)
        cm.key(s("break2") - 0.1, -470, -210, 1.7, 0.0)
        cm.key(s("fix2") - 0.1, -600, -164, 2.0, 0.8)
        cm.key(s("break3") - 0.1, 0, -190, 1.15, 0.0).key(T["twisted"] - 0.4, 0, -185, 1.3, 0.8)
        cm.key(s("fix3") - 0.12, 0, -215, 2.2, 0.0)
        cm.key(s("break4") - 0.12, -120, -200, 1.9, 0.0).key(T["pop"] - 0.3, -150, -195, 2.2, 0.6)
        cm.key(s("cta") + 0.05, -500, -185, 2.0, 0.0)
        cm.key(s("reveal") - 0.1, 0, -175, 1.05, 0.0)
        cm.key(T["s1"] - 0.35, 0, -180, 0.9, 0.0).key(s("closer"), 0, -190, 0.96, 2.4)
        cm.key(s("tag") - 0.2, -200, -400, 2.3, 0.0).key(T["still"] - 0.3, -205, -385, 2.5, 0.8)
        self.cam = cm
        self.spans = [(T["snap"], T["hangers"]), (T["pull"], T["concrete"]), (T["gal"], T["past"]), (T["pop"], T["combs"])]
        self.shakes = [(T["snap"], 0.3, 12), (T["pull"], 0.35, 12), (T["block"] + 0.5, 0.4, 14), (T["break"], 0.6, 18), (T["pop"], 0.3, 12)]

    # ------------------------------------------------------------------ the moving deck
    def phase(self, t):
        s = self.tl.s
        for name, t0 in (("tag", s("tag") - 0.2), ("stat", self.T["s1"] - 0.35), ("reveal", s("reveal") - 0.1), ("cta", s("cta") + 0.05),
                         ("hot", s("break4") - 0.12), ("truss", s("fix3") - 0.12), ("wind", s("break3") - 0.1), ("anchor", s("break2") - 0.1),
                         ("build", s("fix1") - 0.12), ("plank", 0.0)):
            if t >= t0:
                return name

    def dy(self, x, t, ph):
        """How far the road is off its line at x (down is positive)."""
        T = self.T
        if ph == "wind" and abs(x) < TW:
            amp = 30 * prog(t, T["gal"], T["gal"] + 0.8) + 34 * prog(t, T["twisted"] - 0.6, T["break"])
            return amp * math.sin(2 * math.pi * (x / 190 - 1.5 * t)) * math.cos(math.pi * x / (2 * TW))
        if ph == "anchor":                                                           # the cable lets go: the road drops
            return 60 * e_out(prog(t, T["pull"], T["pull"] + 0.5)) * clamp((ANCH - abs(x)) / 200) * (1 if x < 100 else 0.4)
        if ph == "hot":
            return -46 * e_back(prog(t, T["pop"], T["pop"] + 0.25)) * max(0.0, 1 - abs(x + 150) / 46)
        return 0.0

    # ------------------------------------------------------------------ the bridge
    def bridge(self, c, t, col, ph, parts=(1, 1, 1, 1), truss=0.0):
        """parts: how much of (towers, cables, hangers, road) is built, each 0..1."""
        T = self.T
        k_tw, k_cab, k_hang, k_road = parts
        dark = shade(col, -0.35)
        gone = ph == "wind" and t >= T["break"]
        sag = 60 * e_out(prog(t, T["pull"], T["pull"] + 0.5)) if ph == "anchor" else 0.0
        # the road
        if k_road > 0:
            x = -620
            while x < 620:
                x1 = x + 40
                shown = abs((x + x1) / 2) / 620 <= k_road if k_road < 1 else True
                if shown and not (gone and abs((x + x1) / 2) < 112):
                    y0, y1 = DECK + self.dy(x, t, ph), DECK + self.dy(x1, t, ph)
                    p = skia.Path()
                    p.moveTo(x, y0)
                    p.lineTo(x1, y1)
                    p.lineTo(x1, y1 + 14)
                    p.lineTo(x, y0 + 14)
                    p.close()
                    c.drawPath(p, P(col))
                    c.drawLine(x, y0, x1, y1, P("#FFFFFF", 0.35, stroke=2))
                    if truss > 0 and abs(x + 20) / 620 <= truss:
                        zz = skia.Path()
                        zz.moveTo(x, y0 + 14)
                        zz.lineTo(x + 20, y0 + 42)
                        zz.lineTo(x1, y1 + 14)
                        c.drawPath(zz, P(dark, 1, stroke=4))
                        c.drawLine(x, y0 + 42, x1, y1 + 42, P(dark, 1, stroke=4))
                x = x1
            if gone:                                                                 # the middle of it, on its way down
                dt = t - T["break"]
                for i in range(5):
                    sx = -96 + i * 48
                    fy = DECK + 30 + 520 * dt * dt * (0.8 + 0.1 * i)
                    if fy < 10:
                        c.save()
                        c.translate(sx, fy)
                        c.rotate((i - 2) * 50 * dt + i * 20 * dt)
                        c.drawRect(R(-22, -7, 44, 14), P(col))
                        c.restore()
                    else:
                        splash(c, sx, 0, t, T["break"] + math.sqrt(max(0.0, (140 - 30) / (520 * (0.8 + 0.1 * i)))), 0.9, n=16, speed=420, seed=i)
        # towers
        if k_tw > 0:
            for tx in (-TW, TW):
                h = (0 - TOP) * e_out(k_tw)
                c.drawRRect(rr(tx - 44, -24, 88, 60, 10), P("#55607F"))
                c.drawRect(R(tx - 20, -h, 40, h), lin_paint(tx - 20, 0, tx + 20, 0, [shade(col, 0.18), col, dark]))
                for by in range(-60, int(-h), -92):
                    c.drawRect(R(tx - 26, by, 52, 12), P(dark))
                if k_tw >= 1:
                    c.drawRRect(rr(tx - 30, TOP - 16, 60, 22, 6), P(col))
                    c.drawRect(R(tx - 9, DECK - 150, 18, 120), P("#0B1024", 0.35))
        # cables and hangers
        if k_cab > 0:
            p = skia.Path()
            x_end = lerp(-ANCH, ANCH, k_cab)
            p.moveTo(-ANCH, cable_y(-ANCH) + 0)
            x = -ANCH
            while x < x_end:
                x = min(x + 20, x_end)
                yy = cable_y(x)
                if ph == "anchor" and x < -TW:                                       # the loose end whips up
                    lift = e_out(prog(t, T["pull"], T["pull"] + 0.45))
                    u = clamp((-TW - x) / (ANCH - TW))
                    yy = yy - 150 * lift * u * u + 30 * math.sin(t * 9) * lift * u
                p.lineTo(x, yy)
            c.drawPath(p, P(dark, 1, stroke=12))
            c.drawPath(p, P(col, 1, stroke=8))
        if k_hang > 0:
            xs = [x for x in range(-520, 521, 40) if abs(abs(x) - TW) > 30]
            n = len(xs)
            for i, x in enumerate(xs):
                kk = clamp(k_hang * n - i) if k_hang < 1 else 1.0
                if kk <= 0 or (gone and abs(x) < 112):
                    continue
                y0 = cable_y(x)
                y1 = DECK + self.dy(x, t, ph)
                c.drawLine(x, y0, x, lerp(y0, y1, kk), P(shade(col, 0.1), 0.9, stroke=3))

    def painted(self, c, t, ph, **kw):
        """Steel grey until the reveal, then orange sweeps across it from the left."""
        T, s = self.T, self.tl.s
        if t < s("reveal") - 0.1:
            self.bridge(c, t, GRAY, ph, **kw)
            return
        wx = lerp(-700, 700, e_io(prog(t, T["paint"] - 0.1, T["orange"] + 0.6)))
        if wx < 700:
            self.bridge(c, t, GRAY, ph, **kw)
        c.save()
        c.clipRect(R(-2000, -2000, 2000 + wx, 4000))
        self.bridge(c, t, ORANGE, ph, **kw)
        c.restore()
        if -700 < wx < 700:
            c.drawRect(R(wx - 5, -560, 10, 470), P("#FFFFFF", 0.7))
        bee = e_back(prog(t, T["bee0"], T["bee0"] + 0.3)) * (1 - prog(t, T["s1"] - 0.5, T["s1"] - 0.35)) if ph == "reveal" else 0.0
        if bee > 0:                                                                  # what the navy wanted
            for tx in (-TW, TW):
                for i in range(9):
                    c.drawRect(R(tx - 20, TOP + i * 58, 40, 29), P("#111827" if i % 2 == 0 else "#FACC15", clamp(bee)))
                c.drawRRect(rr(tx - 30, TOP - 16, 60, 22, 6), P("#111827", clamp(bee)))
                flap = 20 * math.sin(t * 50)
                for sd in (-1, 1):
                    c.save()
                    c.translate(tx + sd * 20, TOP + 120)
                    c.rotate(sd * (40 + flap))
                    c.drawOval(R(0 if sd > 0 else -84 * bee, -22, 84 * bee, 44), P("#E0F2FE", 0.75 * clamp(bee)))
                    c.restore()
                for sd in (-1, 1):
                    c.drawLine(tx + sd * 8, TOP - 14, tx + sd * 26, TOP - 50 * bee, P("#111827", clamp(bee), stroke=4))
                    c.drawCircle(tx + sd * 26, TOP - 50 * bee, 6 * bee, P("#111827"))
                c.drawCircle(tx - 9, TOP + 14, 4, P("#FFFFFF", clamp(bee)))
                c.drawCircle(tx + 9, TOP + 14, 4, P("#FFFFFF", clamp(bee)))

    # ------------------------------------------------------------------ set: the strait
    def draw_span(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.cam.at(t)
        cam = (cam[0] + math.sin(t * 0.5) * 3, cam[1], cam[2])
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        ph = self.phase(t)
        hot = prog(t, T["hot"] - 0.3, T["grow"]) if ph == "hot" else 0.0
        v2.sky(c, W, H, 0.0, horizon_y=gy + 30)
        v2.stars(c, W, H, t, 0.45)
        if hot > 0:                                                                  # one very hot sun
            add_glow(c, W * 0.8, 430, 520, "#FF9A3D", 0.7 * hot)
            c.drawCircle(W * 0.8, 430, 80 + 30 * hot, P("#FFE08A", hot))
        c.save()
        c.translate(W / 2 - cx * 0.2 * z, gy)
        c.scale(z, z)
        v2.ridge(c, -1700, 1700, 0, 250, "#2A2C5E", "#1A1C42", seed=5, step=80, rough=0.6)
        c.restore()
        self.view(c, cam)
        # the banks
        for sd in (-1, 1):
            p = skia.Path()
            p.moveTo(sd * BANK, 60)
            p.lineTo(sd * (BANK + 6), DECK + 18)
            p.lineTo(sd * (BANK + 40), DECK + 2)
            p.lineTo(sd * 2600, DECK + 2)
            p.lineTo(sd * 2600, 900)
            p.lineTo(sd * BANK, 900)
            p.close()
            c.drawPath(p, lin_paint(0, DECK, 0, 300, ["#3A4466", "#232A45", "#11162B"]))
            c.drawLine(sd * (BANK + 40), DECK + 2, sd * 2600, DECK + 2, P("#5C6B96", 1, stroke=5))
        sea(c, -BANK - 4, BANK + 4, t, moon_x=None)
        if ph == "plank":
            self.plank(c, t)
        elif ph == "build":
            self.painted(c, t, ph, parts=(prog(t, T["tw"], T["tw"] + 0.5), prog(t, T["cab"], T["cab"] + 0.8),
                                          prog(t, T["hang"] - 0.2, T["road"] + 0.2), prog(t, T["road"] - 0.2, T["hangers"])))
            if t >= T["laundry"] - 0.25:                                             # ...like laundry
                for i, (lx, kind) in enumerate(((-205, 0), (-160, 1), (-110, 2), (-64, 0))):
                    k = e_back(prog(t, T["laundry"] - 0.25 + i * 0.09, T["laundry"] + i * 0.09))
                    ly = cable_y(lx) + 6
                    sw = math.sin(t * 4 + i) * 6
                    c.save()
                    c.translate(lx, ly)
                    c.rotate(sw)
                    c.scale(k, k)
                    colr = ("#F472B6", "#7DD3FC", "#FDE68A")[kind]
                    if kind == 0:
                        c.drawRRect(rr(-13, 0, 26, 30, 4), P(colr))
                        c.drawRect(R(-21, 0, 9, 13), P(colr))
                        c.drawRect(R(12, 0, 9, 13), P(colr))
                    elif kind == 1:
                        c.drawRect(R(-11, 0, 22, 14), P(colr))
                        c.drawRect(R(-11, 12, 9, 22), P(colr))
                        c.drawRect(R(2, 12, 9, 22), P(colr))
                    else:
                        c.drawRRect(rr(-5, 0, 11, 24, 4), P(colr))
                        c.drawRRect(rr(-5, 18, 19, 9, 4), P(colr))
                    c.drawRect(R(-3, -6, 6, 9), P("#E5E9F2"))
                    c.restore()
        elif ph == "anchor":
            fix = t >= s("fix2") - 0.1
            if fix:
                self.anchorage(c, t)
            self.painted(c, t, "build" if fix else ph)
            if not fix:                                                              # one tent peg
                out = prog(t, T["pull"], T["pull"] + 0.5)
                px, py = -ANCH - 6, cable_y(-ANCH)
                c.save()
                c.translate(px - 60 * out, py - 190 * math.sin(math.pi * min(1.0, out * 0.85)) + 40 * out * out)
                c.rotate(-30 + 500 * out + (math.sin(t * 30) * 6 if T["cables2"] < t < T["pull"] else 0))
                c.drawRRect(rr(-5, -8, 10, 50, 4), P("#E5E9F2"))
                c.drawRRect(rr(-12, -12, 24, 8, 4), P("#E5E9F2"))
                c.restore()
        elif ph == "wind":
            self.painted(c, t, ph)
            wind(c, -620, -330, 620, t, n=9, a=prog(t, T["wind"] - 0.3, T["wind"] + 0.2), spread=150, seed=1)
            if t < T["break"]:                                                       # the people who came for the ride
                for i, col in enumerate(("#F8FAFC", "#FDE68A")):
                    cxp = lerp(-560 - i * 150, 520, prog(t, T["drivers"] - 0.6 + i * 0.3, T["break"] + 0.6 + i * 0.3))
                    yy = DECK + self.dy(cxp, t, ph)
                    slope = math.degrees(math.atan2(self.dy(cxp + 20, t, ph) - self.dy(cxp - 20, t, ph), 40))
                    car(c, cxp, yy, col, slope)
        elif ph == "truss":
            self.painted(c, t, ph, truss=prog(t, T["stiffen"] - 0.1, T["truss"] + 0.3))
            wind(c, -620, -260, 620, t, n=8, a=1.0, spread=120, seed=2)
            car(c, lerp(-300, 300, prog(t, s("fix3"), T["seccut"] + 0.3)), DECK, "#F8FAFC")
        elif ph == "hot":
            self.painted(c, t, ph, truss=1.0)
            cxp = lerp(-420, 60, prog(t, T["pop"] - 0.9, T["pop"] + 1.1))
            jump = bump(t, T["pop"] + 0.1, T["pop"] + 0.9) * 70 if cxp > -160 else 0.0
            car(c, cxp, DECK + self.dy(cxp, t, ph) - jump, "#F8FAFC", -jump * 0.4 + bump(t, T["pop"] + 0.1, T["pop"] + 0.9) * 30)
            if hot > 0:
                for i in range(6):
                    u = (t * 0.6 + i / 6) % 1.0
                    c.drawLine(-330 + i * 70, DECK - 6 - u * 60, -322 + i * 70 + math.sin(t * 5 + i) * 6, DECK - 26 - u * 60,
                               P("#FF9A62", 0.7 * hot * (1 - u), stroke=4))
                gk = prog(t, T["grow"] - 0.3, T["pop"])                                # the steel grows: arrows pushing at each other
                for sd in (-1, 1):
                    ax = -150 + sd * (120 - 50 * gk)
                    c.drawLine(ax, DECK - 44, ax - sd * 46, DECK - 44, P("#FDE68A", hot, stroke=6))
                    for dyy in (-12, 12):
                        c.drawLine(ax - sd * 46, DECK - 44, ax - sd * 30, DECK - 44 + dyy, P("#FDE68A", hot, stroke=6))
        else:
            self.painted(c, t, ph, truss=1.0)
            self.anchorage(c, t, done=True)
            if ph == "cta":                                                          # the ribbon
                c.drawRect(R(-474, DECK - 62, 6, 64), P("#E5E9F2"))
                c.drawRect(R(-420, DECK - 62, 6, 64), P("#E5E9F2"))
                c.drawLine(-471, DECK - 50, -417, DECK - 50, P("#EF4444", 1, stroke=9))
                c.drawCircle(-444, DECK - 50, 9, P("#EF4444"))
            if ph in ("stat", "reveal"):
                for i in range(5):                                                   # evening traffic
                    u = (t * 0.07 + i / 5) % 1.0
                    car(c, lerp(-640, 640, u), DECK, ("#F8FAFC", "#FDE68A", "#7DD3FC")[i % 3], 0.0, 0.8)
                for i in range(6):                                                   # fog on the water
                    fxp = -520 + i * 210 + math.sin(t * 0.3 + i) * 60
                    puff(c, fxp, -44 + (i % 2) * 20, 130, "#C7D2FE", 0.16, k=i)
            if ph == "tag":
                self.painter(c, t)
        self.people(c, t, ph)
        c.restore()
        self.ui["cam"] = cam

    def plank(self, c, t):
        T, s = self.T, self.tl.s
        first = t < s("break1") - 0.1
        rk = skia.Path()                                                             # a rock to rest it on
        rk.moveTo(-372, 60)
        rk.lineTo(-352, DECK + 30)
        rk.lineTo(-338, DECK)
        rk.lineTo(-262, DECK)
        rk.lineTo(-244, DECK + 44)
        rk.lineTo(-226, 60)
        rk.close()
        c.drawPath(rk, lin_paint(0, DECK, 0, 60, ["#4B5578", "#2B3352", "#1A2038"]))
        c.drawLine(-338, DECK, -262, DECK, P("#6B7699", 1, stroke=5))
        if first or t < T["mile0"]:
            drop = e_in(prog(t, 0.12, T["plank"] - 0.05))
            yy = lerp(DECK - 620, DECK - 10, drop)
            c.save()
            c.translate(-400, yy)
            c.rotate(lerp(-18, 0, drop))
            box(c, -100, 0, 200, 12, "#C08A52", r=3)
            for gx in (-60, 0, 60):
                c.drawLine(gx, 2, gx + 16, 10, P("#8B5E3C", 0.7, stroke=2))
            c.restore()
        else:                                                                        # a plank for a mile of water
            ext = e_out(prog(t, T["mile0"], T["plank2"] + 0.1))
            x_end = lerp(-300, 330, ext)
            snapped = t >= T["snap"]
            if not snapped:
                p = skia.Path()
                p.moveTo(-480, DECK - 10)
                n = 24
                for i in range(1, n + 1):
                    u = i / n
                    x = lerp(-480, x_end, u)
                    sagv = (150 * ext + 26 * math.sin(t * 11) * prog(t, T["plank2"] - 0.4, T["snap"])) * math.sin(math.pi * min(1.0, u * 0.86)) * (0.4 + 0.6 * ext)
                    p.lineTo(x, DECK - 10 + sagv * (0.35 if x < -330 else 1.0))
                pr = P("#C08A52", 1, stroke=11)
                pr.setStrokeCap(skia.Paint.kRound_Cap)
                c.drawPath(p, pr)
            else:
                dt = t - T["snap"]
                for sd, x0, x1 in ((-1, -480, -80), (1, -80, 330)):
                    fall = min(DECK - 10 + 140 + 620 * dt * dt, 6 + 5 * math.sin(t * 3 + sd))
                    c.save()
                    c.translate((x0 + x1) / 2 + (40 * dt if fall >= 0 else 0) * (dt > 0.5), fall)
                    c.rotate(sd * min(26, 80 * dt) * (1 if fall < 0 else 0.15))
                    c.drawRRect(rr(-(x1 - x0) / 2, -6, x1 - x0, 11, 4), P("#C08A52"))
                    c.restore()
                tsp = math.sqrt(max(0.0, (-(DECK - 10 + 140)) / 620))
                splash(c, -280, 0, t, T["snap"] + tsp, 1.0, n=22, speed=520, seed=1)
                splash(c, 120, 0, t, T["snap"] + tsp + 0.05, 1.0, n=22, speed=520, seed=2)
            if t >= T["mile0"]:                                                      # how wide it really is
                mk = prog(t, T["mile0"], T["mile0"] + 0.5)
                yy = DECK - 250
                c.drawLine(-BANK, yy, lerp(-BANK, BANK, mk), yy, P(HILITE, 1, stroke=5))
                for bx in (-BANK, BANK):
                    c.drawLine(bx, yy - 22, bx, yy + 22, P(HILITE, mk if bx > 0 else 1, stroke=5))

    def anchorage(self, c, t, done=False):
        """The left end: strands, eyebars and the block of concrete they are buried in."""
        T = self.T
        bk = 1.0 if done else e_out(prog(t, T["block"] - 0.1, T["block"] + 0.6))
        fk = 1.0 if done else prog(t, T["fan0"] - 0.1, T["fan0"] + 0.5)
        ek = 1.0 if done else prog(t, T["eye0"] - 0.1, T["eye0"] + 0.4)
        x0, y0 = -ANCH + 4, cable_y(-ANCH)
        if bk > 0:
            c.save()
            c.clipRect(R(-760, -640, 260, 640 + (DECK + 2 if done else 200)))
            drop = (1 - bk) * -300
            vrect(c, -752, -238 + drop, 196, 214, ["#B4BCCB", "#8E96AA", "#5C6580"], [0.0, 0.4, 1.0], r=8, a=1.0)
            rng = random.Random(3)
            for _ in range(70):
                c.drawCircle(rng.uniform(-748, -560), rng.uniform(-234, -28) + drop, rng.uniform(1.5, 4), P("#000000" if rng.random() < 0.6 else "#FFFFFF", 0.10))
            c.restore()
        if done:
            return
        for i in range(7):
            ty = y0 - 54 + i * 26
            if fk > 0:
                c.drawLine(x0, y0, lerp(x0, -612, fk), lerp(y0, ty, fk), P(GRAY, 1, stroke=4))
            if ek > 0:
                kk = clamp(ek * 7 - i)
                if kk > 0:
                    c.drawLine(-612, ty, -612 - 96 * kk, ty + 10, P("#E5E9F2", 1, stroke=6))
                    c.drawCircle(-612, ty, 8, P("#E5E9F2"))
                    c.drawCircle(-612, ty, 3.5, P("#1B2238"))

    def painter(self, c, t):
        T = self.T
        tx = -TW
        py = lerp(TOP + 70, TOP + 150, prog(t, T["started"] - 0.4, T["done"] + 0.5))
        old = prog(t, T["started"], T["still"] + 0.2)
        for i in range(5):                                                           # what he painted first is already peeling
            yy = TOP + 6 + i * 13
            if yy < py - 30:
                c.drawRect(R(tx - 20 + (i * 17) % 22, yy, 16, 9), P(GRAY, clamp(old * 1.4 - i * 0.15)))
                c.drawRect(R(tx + 2 - (i * 11) % 18, yy + 4, 12, 7), P("#7C4A2D", clamp(old * 1.4 - i * 0.15)))
        c.drawLine(tx + 44, TOP - 10, tx + 44, py - 60, P("#E5E9F2", 1, stroke=3))
        c.drawRRect(rr(tx + 26, py + 2, 40, 7, 3), P("#8B5E3C"))
        engineer(c, tx + 46, py + 2, 88, SHIRTS[1], t, "point" if t < T["still"] else "shrug", face=-1)
        c.drawRRect(rr(tx + 70, py - 14, 16, 18, 3), P("#CBD5E1"))
        c.drawRect(R(tx + 71, py - 14, 14, 6), P(ORANGE))
        bx = tx + 22 + math.sin(t * 7) * 5
        c.drawRect(R(bx - 4, py - 62 + math.sin(t * 7) * 8, 8, 18), P("#FDE68A"))

    def people(self, c, t, ph):
        T, s = self.T, self.tl.s
        if ph == "plank":
            if t < s("break1") - 0.1:
                self.crew(c, t, "cheer" if t >= T["congrats"] - 0.1 else "look", xs=(-590, -548, -506), y=DECK + 2, face=1, h=104)
            else:
                self.crew(c, t, "shrug" if t >= T["snap"] + 0.2 else "look", xs=(-590, -548, -506), y=DECK + 2, face=1, h=104)
        elif ph == "build":
            self.crew(c, t, "cheer" if t >= T["hangers"] + 0.2 else "look", xs=(-590, -548, -506), y=DECK + 2, face=1, h=84)
        elif ph == "anchor":
            fix = t >= s("fix2") - 0.1
            if not fix:
                self.crew(c, t, "duck" if t >= T["pull"] else "look", xs=(-420, -382, -344), y=DECK + self.dy(-380, t, ph), face=-1, h=84)
            else:
                self.crew(c, t, "cheer" if t >= T["concrete"] else "look", xs=(-470, -436, -402), y=DECK, face=-1, h=78)
        elif ph == "cta":
            self.crew(c, t, "look", xs=(-560, -524, -488), y=DECK + 2, face=1, h=92)
            sx = -470                                                                # the big scissors
            op = 14 + 10 * math.sin(t * 5)
            for sd in (-1, 1):
                c.save()
                c.translate(sx, DECK - 54)
                c.rotate(sd * op)
                c.drawRRect(rr(0, -3, 40, 6, 3), P("#E5E9F2"))
                c.drawCircle(-9, 0, 8, P("#FACC15", 1, stroke=4))
                c.restore()
        elif ph == "stat":
            self.crew(c, t, "cheer", xs=(-590, -548, -506), y=DECK + 2, face=1, h=84)
            if t >= T["cong2"]:
                hats_in_the_air(c, (-590, -548, -506), DECK - 150, t, T["cong2"])

    # ------------------------------------------------------------------ set: the deck, cut across
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.2, horizon_y=H * 1.2)
        v2.stars(c, W, H, t, 0.5)
        k = e_io(prog(t, T["streamlined"] - 0.3, T["box"] + 0.1))                     # 0: a flat plate, 1: a streamlined box
        cx, cy = 540, 780
        hw = 300
        top, bot = 26 + 14 * k, 26 + 60 * k
        p = skia.Path()
        p.moveTo(cx - hw, cy)
        p.lineTo(cx - hw + 110 * k, cy - top)
        p.lineTo(cx + hw - 110 * k, cy - top)
        p.lineTo(cx + hw, cy)
        p.lineTo(cx + hw - 150 * k, cy + bot)
        p.lineTo(cx - hw + 150 * k, cy + bot)
        p.close()
        wob = math.sin(t * 9) * 26 * (1 - k)                                         # the flat one will not sit still
        c.save()
        c.translate(0, wob)
        c.rotate(math.sin(t * 7) * 5 * (1 - k), cx, cy)
        for sd in (-1, 1):                                                           # hangers going up out of the picture
            c.drawLine(cx + sd * (hw - 60), cy - top, cx + sd * (hw - 60), 200, P(GRAY, 0.9, stroke=6))
        c.drawPath(p, lin_paint(0, cy - 40, 0, cy + 90, ["#CBD5E1", GRAY, "#55607F"]))
        c.drawPath(p, P("#FFFFFF", 0.5, stroke=3))
        c.drawRect(R(cx - hw + 110 * k + 10, cy - top - 10, 2 * hw - 220 * k - 20, 10), P("#334155"))
        for i, lane in enumerate((-150, -50, 50, 150)):
            car(c, cx + lane * (1 - 0.25 * k), cy - top - 8, ("#F8FAFC", "#FDE68A", "#7DD3FC", "#F472B6")[i], 0, 0.9)
        c.restore()
        for i in range(8):                                                           # the wind
            u = (t * 0.55 + i / 8) % 1.0
            yy0 = cy - 130 + i * 38
            pth = skia.Path()
            x = -60 + u * 300
            pth.moveTo(x - 240, yy0)
            for j in range(1, 30):
                xx = x - 240 + j * 44
                d = (xx - cx) / (hw + 60)
                near = math.exp(-d * d * 1.6)
                off = (yy0 - cy)
                push = (1 if off >= 0 else -1) * near * max(0.0, 96 - abs(off) * 0.7)
                swirl = (1 - k) * 40 * math.sin(xx * 0.03 + t * 8 + i) * clamp((xx - cx + 80) / 260)
                pth.lineTo(xx, yy0 + push + swirl)
            pr = P("#BAE6FD", 0.75, stroke=5)
            pr.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawPath(pth, pr)
        self.ui["cam"] = (0, 0, 1)

    # ------------------------------------------------------------------ set: the road from above
    def draw_joint(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.2, horizon_y=H * 1.2)
        y0, y1 = 470, 1090
        cutk = prog(t, T["cut"] - 0.1, T["gaps"] + 0.2)
        temp = math.sin((t - T["slide"]) * 2.4) if t >= T["slide"] - 0.3 else -1.0   # -1 cold: gap wide.  +1 hot: gap almost shut
        gap = lerp(0, 90, cutk) * (0.62 - 0.38 * temp)
        fk = e_out(prog(t, T["fingers"] - 0.5, T["fingers"]))
        c.drawRect(R(0, y0 - 26, W, y1 - y0 + 52), P("#94A3B8"))                      # kerbs
        for sd, xa, xb in ((-1, 0, W / 2 - gap / 2), (1, W / 2 + gap / 2, W)):
            c.drawRect(R(xa, y0, xb - xa, y1 - y0), lin_paint(0, y0, 0, y1, ["#3B4560", "#2A324A"]))
        c.drawRect(R(W / 2 - gap / 2, y0 - 26, gap, y1 - y0 + 52), P("#05081A"))        # the gap: water far below
        for yy in range(y0 + 40, y1, 60):
            c.drawOval(R(W / 2 - gap / 2 + 4, yy, max(0.0, gap - 8), 9), P("#1D4ED8", 0.5))
        for ly in (y0 + 205, y0 + 415):                                               # lane lines
            for lx in range(-40, W, 120):
                xx = lx + (0 if lx < W / 2 else 0)
                if abs(xx + 35 - W / 2) > gap / 2 + 60:
                    c.drawRRect(rr(xx, ly - 5, 70, 10, 5), P("#E5E9F2", 0.85))
        if fk > 0:                                                                   # the fingers: two combs
            n = 11
            ln = 74
            for i in range(n):
                yy = y0 + 8 + i * (y1 - y0 - 16) / n
                hh = (y1 - y0 - 16) / n / 2 - 3
                c.drawRect(R(W / 2 - gap / 2 - 36, yy, 36 + ln * fk, hh), P("#CBD5E1"))
                c.drawRect(R(W / 2 + gap / 2 - ln * fk, yy + hh + 3, 36 + ln * fk, hh), P("#F8FAFC"))
            c.drawRect(R(W / 2 - gap / 2 - 44, y0, 16, y1 - y0), P("#94A3B8"))
            c.drawRect(R(W / 2 + gap / 2 + 28, y0, 16, y1 - y0), P("#94A3B8"))
        if t >= T["slide"] - 0.2:                                                     # and the traffic never notices
            for i, (lane, col, dly) in enumerate(((y0 + 105, "#F8FAFC", 0.0), (y0 + 310, "#FDE68A", 0.7), (y0 + 515, "#7DD3FC", 0.3))):
                u = prog(t, T["slide"] - 0.2 + dly, T["slide"] + 1.5 + dly)
                if 0 < u < 1:
                    xx = lerp(-140, W + 140, u) if i != 1 else lerp(W + 140, -140, u)
                    c.drawRRect(rr(xx - 70, lane - 38, 140, 76, 22), P(col))
                    c.drawRRect(rr(xx - 30, lane - 30, 62, 60, 12), P("#1B2238"))
        self.ui["cam"] = (0, 0, 1)
        self.ui["gap"] = gap
        self.ui["temp"] = temp

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -250, 1.0)), x, y)

    def ui_span(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        ph = self.phase(tw)
        if ph == "plank":
            if tw < s("break1") - 0.1:
                x0, y0 = self.at(-400, DECK - 10)
                self.label(x0, y0, x0 + 120, y0 - 300, "plank", T["plank"], T["congrats"] + 0.3, HILITE)
            else:
                x0, y0 = self.at(0, DECK - 250)
                self.chip(x0, y0 - 56, "mile", T["mile0"] + 0.2, T["plank2"] + 0.1, accent=HILITE, size=44)
                self.badge("alert", T["snap"], s("fix1") - 0.2)
                self.red(T["snap"], 1.8)
        elif ph == "build":
            x0, y0 = self.at(TW, TOP + 60)
            self.label(x0, y0, x0 - 150, y0 - 110, "tower", T["tw"] + 0.3, T["cab"] - 0.05, GRAY)
            x1, y1 = self.at(110, cable_y(110))
            self.label(x1, y1, x1 + 110, y1 - 250, "cable", T["cab"] + 0.5, T["hang"] - 0.2, GRAY)
            x2, y2 = self.at(-20, -165)
            self.label(x2, y2, x2 + 170, y2 - 210, "hanger", T["hangers"] - 0.2, T["laundry"] - 0.3, HILITE)
            self.badge("check", T["hangers"] + 0.2, s("break2") - 0.15, x=880, y=420)
        elif ph == "anchor":
            if tw < s("fix2") - 0.1:
                x0, y0 = self.at(-ANCH - 6, cable_y(-ANCH))
                self.label(x0, y0, x0 + 100, y0 - 330, "peg", T["cables2"], T["pull"] + 0.2, HILITE)
                self.badge("alert", T["pull"], s("fix2") - 0.2)
                self.red(T["pull"], 1.8)
            else:
                x0, y0 = self.at(-585, cable_y(-ANCH) - 40)
                self.label(x0, y0, x0 + 240, y0 - 250, "strands", T["fan0"] + 0.2, T["eye0"] - 0.1, GRAY)
                x1, y1 = self.at(-660, cable_y(-ANCH) + 20)
                self.label(x1, y1, x1 + 40, y1 - 400, "eyebar", T["eye0"] + 0.2, T["block"] - 0.1, "#E5E9F2")
                self.chip(540, 400, "tons", T["sixty"] - 0.1, s("break3") - 0.25, accent=HILITE, size=46)
                self.badge("check", T["concrete"], s("break3") - 0.15, x=880, y=560)
        elif ph == "wind":
            self.chip(540, 400, "year", T["nineteen"] - 0.1, T["twisted"] - 0.2, accent=WARN, size=54)
            self.badge("alert", T["gal"] + 0.2, s("fix3") - 0.2, x=880, y=560)
            self.red(T["break"], 2.0)
        elif ph == "truss":
            x0, y0 = self.at(-60, DECK + 44)
            self.label(x0, y0, x0 - 100, y0 - 520, "truss", T["truss"] - 0.25, T["seccut"] - 0.05, HILITE)
        elif ph == "hot":
            self.chip(300, 420, "hot", T["hot"] - 0.2, T["grow"] - 0.2, accent=WARN, size=44)
            self.chip(300, 420, "grow", T["grow"] - 0.1, s("fix4") - 0.25, accent="#FDE68A", size=40)
            self.badge("alert", T["pop"], s("fix4") - 0.2, x=880, y=640)
            self.red(T["pop"], 1.8)
        elif ph == "reveal":
            x0, y0 = self.at(TW + 30, TOP + 60)
            self.label(x0, y0, x0 - 60, y0 - 210, "bee", T["bee0"] + 0.2, T["s1"] - 0.5, "#FACC15")
        elif ph == "tag":
            self.chip(760, 560, "since", T["started"] + 0.1, self.duration + 1, accent=ORANGE, size=42)

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "flat", T["seccut"] + 0.2, T["streamlined"] - 0.35, accent=WARN, size=42)
        self.chip(540, 420, "box", T["streamlined"], s("break4") - 0.25, accent=GOOD, size=42)
        self.badge("check", T["past"], s("break4") - 0.15, x=880, y=560)

    def ui_joint(self, c, t, tw):
        T, s = self.T, self.tl.s
        gap = self.ui.get("gap", 40)
        self.label(W / 2, 470, 760, 330, "joint", T["expansion"] - 0.1, T["fingers"] - 0.55, HILITE)
        self.label(W / 2 + 20, 520, 300, 330, "fingers", T["fingers"] - 0.1, s("cta") - 0.3, "#F8FAFC")
        if tw >= T["slide"] - 0.3:
            hotk = (self.ui.get("temp", 0) + 1) / 2
            p = self.span(T["slide"] - 0.3, s("cta") - 0.3)
            v2.chip(c, 800, 330, self.L["warm"] if hotk > 0.5 else self.L["cold"], p, size=40, accent=mix("#38BDF8", WARN, hotk))
        self.badge("check", T["combs"], s("cta") - 0.15, x=900, y=1180)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["plank"] - 0.6, sfx.whoosh(0.5, False, 61), -10), (T["plank"] - 0.05, sfx.thud(0.3, 62), -3),
              (T["plank"] + 0.05, sfx.clank(300, 0.2, 63), -9), (T["congrats"] + 0.1, sfx.chime(), -8)]
        ev += [(s("break1") - 0.1, sfx.whoosh(0.7, False, 64), -8), (T["mile0"] + 0.2, sfx.pop(65), -6), (T["plank2"] - 0.4, creak_snd(0.7, 3), -8),
               (T["snap"], sfx.snap(66), 0), (T["snap"] + 0.02, sfx.clank(240, 0.3, 67), -4), (T["snap"] + 0.05, sfx.alarm(3, 820), -11),
               (T["snap"] + 0.5, sfx.hiss(0.6, 68), -8), (T["swimming"] + 0.25, sfx.womp(), -9)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 69), -4), (T["tw"], rumble(0.6, 70), -9), (T["tw"] + 0.5, sfx.thud(0.3, 71), -5),
               (T["cab"], sfx.whoosh(0.8, True, 72), -9), (T["cab"] + 0.8, sfx.clank(500, 0.3, 73), -8)]
        ev += [(T["hang"] - 0.2 + i * 0.07, sfx.tick(), -10) for i in range(10)]
        ev += [(T["hangers"], sfx.thunk(74), -5), (T["laundry"] - 0.25, sfx.pop(75), -7), (T["laundry"] - 0.07, sfx.pop(76), -8),
               (T["laundry"] + 0.1, sfx.pop(77), -8), (T["hangers"] + 0.2, sfx.chime(), -7)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 78), -5), (T["cables2"], creak_snd(0.8, 4), -7), (T["pull"], sfx.snap(79), -1),
               (T["pull"] + 0.03, sfx.whoosh(0.4, True, 80), -5), (T["pull"] + 0.1, sfx.alarm(3, 820), -10), (T["pegs"] + 0.25, sfx.womp(), -9)]
        ev += [(T["fan0"] - 0.1, sfx.whoosh(0.4, True, 81), -9)]
        ev += [(T["eye0"] - 0.1 + i * 0.06, sfx.clank(600 + i * 40, 0.15, 82 + i), -9) for i in range(7)]
        ev += [(T["block"] - 0.1, rumble(0.7, 90), -8), (T["block"] + 0.5, sfx.thud(0.5, 91), -2), (T["sixty"] - 0.1, sfx.pop(92), -5),
               (T["concrete"], sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, True, 93), -5), (T["wind"] - 0.3, gust(1.6, 5), -8), (T["gallop"] + 0.5, sfx.alarm(3, 820), -12),
               (T["gallop"] + 0.55, creak_snd(1.0, 5), -11), (T["nineteen"] - 0.1, sfx.pop(94), -6), (T["drivers"], sfx.beep(520, 0.12), -12),
               (T["drivers"] + 0.2, sfx.beep(520, 0.2), -12), (T["twisted"] - 0.5, creak_snd(1.0, 6), -6), (T["break"], sfx.snap(95), 0),
               (T["break"] + 0.03, sfx.clank(200, 0.5, 96), -3), (T["break"] + 0.45, sfx.hiss(0.8, 97), -7)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 98), -4)]
        ev += [(T["stiffen"] - 0.1 + i * 0.1, sfx.tick(), -9) for i in range(8)]
        ev += [(T["truss"] + 0.3, sfx.thunk(99), -5), (T["seccut"], sfx.whoosh(0.4, True, 100), -5), (T["streamlined"] - 0.3, sfx.whoosh(0.6, True, 101), -9),
               (T["box"] + 0.1, sfx.pop(102), -5), (T["slides"], gust(0.9, 6), -11), (T["past"], sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 103), -5), (T["hot"] - 0.3, sfx.riser(1.0, 104), -12), (T["grow"] - 0.3, creak_snd(0.6, 7), -10),
               (T["pop"], sfx.clank(260, 0.25, 105), -9), (T["pop"] + 0.03, sfx.thud(0.25, 106), -9), (T["pop"] + 0.45, sfx.alarm(3, 820), -12),
               (T["pop"] + 0.45, sfx.whoosh(0.4, True, 107), -10)]     # kept low: the word "buckles" sits right on it
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 108), -4), (T["cut"] - 0.1, zip_(0), -3), (T["expansion"] - 0.1, sfx.pop(109), -6),
               (T["fingers"] - 0.5, sfx.clank(700, 0.25, 110), -5), (T["fingers"], sfx.thunk(111), -5), (T["slide"], sfx.hum(1.2, 90), -13),
               (T["slide"] + 0.4, sfx.tap(112), -8), (T["slide"] + 0.5, sfx.tap(113), -9), (T["slide"] + 1.1, sfx.tap(114), -8),
               (T["combs"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(115), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 116), -7), (T["follow"] - 0.15, sfx.pop(117), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 118), -6), (T["paint"] - 0.1, sfx.whoosh(0.9, True, 119), -8), (T["orange"] + 0.6, sfx.sparkle(0.7, 9, 120), -8),
               (T["bee0"] + 0.1, sfx.pop(121), -7), (T["bee0"] + 0.2, buzz_snd(max(0.6, T["s1"] - 0.6 - T["bee0"])), -12)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 122), -6), (T["s1"], sfx.pop(123), -3), (T["s2"], sfx.pop(124), -3), (T["s3"], sfx.pop(125), -3)]
        ev += [(T["cong2"], sfx.pop(126), -2), (T["cong2"], sfx.sparkle(1.0, 14, 127), -4), (T["cong2"] + 0.1, sfx.snap(128), -6), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 129), -6), (T["started"] + 0.1, sfx.pop(130), -6), (T["year"], sfx.tick(), -8),
               (T["done"] + 0.35, sfx.womp(), -3)]
        return ev


def zip_(seed=0):
    n = int(0.22 * sfx.SR)
    x = sfx._bp(sfx._rng(seed + 40).standard_normal(n), 1500, 6500) * np.linspace(0.2, 1.0, n) ** 2
    return sfx._norm(x * sfx._ar(n, 0.01, 0.03), 0.7)


NAME = "bridge"
EPISODE = Bridge
