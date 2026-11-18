"""Episode 38 - Petra, the city carved into rock.  v2 look: the Treasury (Al-Khazneh) glowing rose-red at the end of
the dark Siq canyon.

Sets: cliff (hook: the 40 m facade appears out of the cliff from the top down; the reveal: tombs and a theater carved
around it, hidden from Europe until 1812; the stat and the closer), carve (break1: carving from the bottom up, chips rain
on the finished columns and crack them; fix1: start at the very top and carve down), pipe (break2: desert, almost no
rain, 20,000 people with empty jars; fix2: a channel cut into the canyon wall, clay pipes laid in it, spring water runs
into a basin in the city), map (break3: a flash flood runs down the wadi into the narrow canyon and the city; fix3: a dam
at the canyon's mouth and a tunnel through the mountain send it around), siq (break4: a rich incense town and raiders on
the ridge; fix4: the city hidden at the end of a winding canyon only 3 m wide), urn (the tag: the urn with its old bullet
dents, solid rock, then grandma's cookie tin full of sewing things).
World (cliff, carve): front view of the cliff, the ground is y = 0, the facade is 800 units tall (20 units = 1 m).
"""
from v2_base import *  # noqa: F401,F403
from camel import camel as camel_fig  # noqa: E402

DUSK = {"top": "#0B0A22", "upper": "#2A1640", "mid": "#6E2C46", "low": "#C2604A", "horizon": "#F39A6B",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
ROCK = ("#9E5646", "#7E4036", "#5A2C26", "#3A1A18")
FACE = "#F2B59A"
FACE_D = "#B7634F"
DEEP = "#5A2A22"
WATER = "#3B82F6"
FH = 800.0                     # facade height (urn top)


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


# ====================================================================================== pieces
def striations(c, x0, x1, y0, y1, seed=2, a=1.0, cols=("#D98A6E", "#9C4E3E", "#E7A07F", "#8A4436")):
    """The swirling bands of Petra's sandstone."""
    rng = random.Random(seed)
    for i in range(int((y1 - y0) / 34)):
        yy = y0 + i * 34 + rng.uniform(-8, 8)
        p = skia.Path()
        p.moveTo(x0, yy)
        ph = rng.uniform(0, 6.3)
        amp = rng.uniform(6, 22)
        for k in range(1, 41):
            xx = lerp(x0, x1, k / 40.0)
            p.lineTo(xx, yy + math.sin(k * 0.45 + ph) * amp)
        c.drawPath(p, P(rng.choice(cols), a * rng.uniform(0.12, 0.3), stroke=rng.uniform(6, 16)))


def cliff(c, x0, x1, top, t, a=1.0, seed=3):
    p = skia.Path()
    rng = random.Random(seed)
    p.moveTo(x0, 40)
    n = 18
    for k in range(n + 1):
        xx = lerp(x0, x1, k / float(n))
        p.lineTo(xx, top + rng.uniform(-120, 120))
    p.lineTo(x1, 40)
    p.close()
    c.save()
    c.clipPath(p, doAntiAlias=True)
    vrect(c, x0, top - 200, x1 - x0, -top + 260, [ROCK[0], ROCK[1], ROCK[2]], [0, 0.6, 1], a=a)
    striations(c, x0, x1, top - 120, 40, seed=seed, a=a)
    c.restore()


def column(c, x, y0, y1, w, a=1.0, lit=1.0):
    c.drawRect(R(x - w / 2, y1, w, y0 - y1), lin_paint(x - w / 2, 0, x + w / 2, 0, [shade(FACE, 0.1), FACE, FACE_D], a=a))
    c.drawRect(R(x - w * 0.75, y1 - 22, w * 1.5, 24), P(shade(FACE, 0.05), a))
    c.drawRect(R(x - w * 0.65, y0 - 10, w * 1.3, 10), P(FACE_D, a))


def treasury(c, x, y, s, t, carved=1.0, mode="down", cracks=0.0, glow=0.0, dents=0.0, a=1.0):
    """Al-Khazneh, front view, base centre at (x, y), scale s. carved 0..1: how much of the facade is cut free, from
    the top (mode "down") or from the bottom (mode "up"). Outside that band the cliff's raw rock shows."""
    yl = lerp(-FH - 40, 0, carved) if mode == "down" else lerp(0, -FH - 40, carved)
    if carved <= 0.001:
        return yl
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if mode == "down":
        c.clipRect(R(-400, -FH - 60, 800, yl + FH + 60))
    else:
        c.clipRect(R(-400, yl, 800, -yl + 10))
    c.drawRect(R(-330, -FH - 30, 660, FH + 30), P(DEEP, a))                       # the recess cut into the cliff
    vrect(c, -330, -FH - 30, 660, FH + 30, [("#000000", 0.25), ("#000000", 0.0)], a=a)
    # ---- lower storey
    c.drawRect(R(-320, -24, 640, 24), P(FACE_D, a))
    c.drawRect(R(-44, -250, 88, 226), P("#2A120E", a))                            # the door
    c.drawRect(R(-56, -262, 112, 14), P(FACE, a))
    for cx_ in (-262, -158, -54, 54, 158, 262):
        column(c, cx_, -24, -300, 34, a=a)
    c.drawRect(R(-300, -352, 600, 30), P(FACE, a))                                # entablature
    c.drawRect(R(-300, -326, 600, 6), P(FACE_D, a))
    for k in range(14):
        c.drawRect(R(-292 + k * 42, -348, 18, 18), P(FACE_D, 0.6 * a))
    ped = skia.Path()
    ped.moveTo(-205, -352)
    ped.lineTo(205, -352)
    ped.lineTo(0, -445)
    ped.close()
    c.drawPath(ped, P(FACE, a))
    c.drawPath(ped, P(FACE_D, a, stroke=6))
    for sx in (-210, 210):                                                         # relief riders between columns
        c.drawOval(R(sx - 22, -230, 44, 120), P(FACE_D, 0.55 * a))
    # ---- upper storey: side pavilions with half pediments, the round tholos and the urn
    for sd in (-1, 1):
        x0, x1 = (-300, -130) if sd < 0 else (130, 300)
        c.drawRect(R(x0, -660, x1 - x0, 210), P(shade(DEEP, 0.15), a))
        for cx_ in ((x0 + 18, x1 - 18) if sd < 0 else (x0 + 18, x1 - 18)):
            column(c, cx_, -450, -650, 26, a=a)
        c.drawOval(R((x0 + x1) / 2 - 18, -620, 36, 120), P(FACE_D, 0.5 * a))
        c.drawRect(R(x0 - 8, -672, x1 - x0 + 16, 18), P(FACE, a))
        hp = skia.Path()
        if sd < 0:
            hp.moveTo(x0 - 8, -672)
            hp.lineTo(x1 + 8, -672)
            hp.lineTo(x1 + 8, -718)
        else:
            hp.moveTo(x0 - 8, -672)
            hp.lineTo(x1 + 8, -672)
            hp.lineTo(x0 - 8, -718)
        hp.close()
        c.drawPath(hp, P(FACE, a))
    c.drawRect(R(-110, -452, 220, 10), P(FACE, a))
    c.drawRect(R(-95, -660, 190, 210), lin_paint(-95, 0, 95, 0, [FACE_D, shade(FACE, 0.08), FACE, FACE_D], [0, 0.35, 0.6, 1], a=a))
    for cx_ in (-80, -27, 27, 80):
        column(c, cx_, -452, -650, 20, a=a)
    c.drawOval(R(-20, -620, 40, 110), P(FACE_D, 0.55 * a))
    c.drawRect(R(-104, -676, 208, 18), P(FACE, a))
    roof = skia.Path()
    roof.moveTo(-100, -676)
    roof.lineTo(100, -676)
    roof.quadTo(40, -720, 0, -742)
    roof.quadTo(-40, -720, -100, -676)
    roof.close()
    c.drawPath(roof, P(FACE, a))
    c.drawRect(R(-12, -760, 24, 20), P(FACE_D, a))                                 # the urn
    urn = skia.Path()
    urn.moveTo(-14, -760)
    urn.quadTo(-34, -780, -18, -800)
    urn.lineTo(18, -800)
    urn.quadTo(34, -780, 14, -760)
    urn.close()
    c.drawPath(urn, P(shade(FACE, 0.08), a))
    c.drawRect(R(-22, -808, 44, 10), P(FACE, a))
    if dents > 0:                                                                  # old bullet dents on the urn
        rng = random.Random(7)
        for i in range(int(14 * dents)):
            c.drawCircle(rng.uniform(-22, 22), rng.uniform(-798, -764), rng.uniform(2.0, 3.6), P("#4A2320", a))
    if cracks > 0:
        rng = random.Random(5)
        for cx_ in (-262, -158, -54, 54, 158, 262):
            p = skia.Path()
            yy = -260 + rng.uniform(-20, 20)
            p.moveTo(cx_ - 10, yy)
            for k in range(1, 6):
                p.lineTo(cx_ + rng.uniform(-14, 14), yy + k * 40 * cracks)
            c.drawPath(p, P("#3B0D0D", a, stroke=4))
    c.restore()
    if glow > 0:
        add_glow(c, x, y - FH * s * 0.5, 520 * s, "#FFD3B0", 0.18 * glow * a)
    return yl


def tomb(c, x, y, s, kind=0, a=1.0):
    """A smaller rock-cut tomb facade with crow-step ornaments."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    w, h = 300.0, 420.0
    c.drawRect(R(-w / 2 - 20, -h - 30, w + 40, h + 30), P(DEEP, 0.7 * a))
    c.drawRect(R(-w / 2, -h, w, h), lin_paint(-w / 2, 0, w / 2, 0, [shade(FACE, 0.05), FACE, FACE_D], a=a))
    c.drawRect(R(-40, -170, 80, 170), P("#2A120E", a))
    if kind == 0:
        for k in range(5):
            xx = -w / 2 + 20 + k * (w - 40) / 4.0
            c.drawRect(R(xx - 14, -h - 40, 28, 40), P(FACE, a))
            c.drawRect(R(xx - 7, -h - 64, 14, 24), P(FACE, a))
    else:
        for cx_ in (-110, -40, 40, 110):
            c.drawRect(R(cx_ - 10, -h + 60, 20, h - 60), P(FACE_D, 0.6 * a))
        tri = skia.Path()
        tri.moveTo(-w / 2, -h)
        tri.lineTo(w / 2, -h)
        tri.lineTo(0, -h - 80)
        tri.close()
        c.drawPath(tri, P(FACE, a))
    c.restore()


def theater(c, x, y, s, a=1.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for k in range(9):
        r = 120 + k * 34
        c.drawArc(R(-r, -r * 0.55, 2 * r, r * 1.1), 180, 180, False, P(shade(FACE, -0.05 * (k % 2)), a, stroke=20))
    c.drawRect(R(-120, -8, 240, 16), P(FACE_D, a))
    c.restore()


def jar(c, x, y, s, full=0.0, a=1.0):
    p = skia.Path()
    p.moveTo(x - 10 * s, y - 52 * s)
    p.quadTo(x - 34 * s, y - 30 * s, x - 18 * s, y)
    p.lineTo(x + 18 * s, y)
    p.quadTo(x + 34 * s, y - 30 * s, x + 10 * s, y - 52 * s)
    p.close()
    c.drawPath(p, P("#B45309", a))
    if full > 0:
        c.drawRect(R(x - 9 * s, y - 56 * s, 18 * s, 6 * s), P(WATER, a * full))


def raindrop_x(c, x, y, s, a=1.0):
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(x, y - 50 * s)
    p.quadTo(x + 36 * s, y, x, y + 26 * s)
    p.quadTo(x - 36 * s, y, x, y - 50 * s)
    c.drawPath(p, P("#60A5FA", a))
    c.drawCircle(x, y - 6 * s, 66 * s, P(WARN, a, stroke=9 * s))
    c.drawLine(x - 46 * s, y + 40 * s, x + 46 * s, y - 52 * s, P(WARN, a, stroke=9 * s))


def chips_fall(c, x0, x1, y_from, y_to, t, a=1.0, seed=9, n=16):
    if a <= 0:
        return
    rng = random.Random(seed)
    for i in range(n):
        q = (t * rng.uniform(0.7, 1.3) + rng.uniform(0, 1)) % 1.0
        xx = rng.uniform(x0, x1) + math.sin(i + t) * 6
        yy = lerp(y_from, y_to, q * q)
        sz = rng.uniform(5, 12)
        c.drawRect(R(xx - sz / 2, yy - sz / 2, sz, sz), P("#E3A387", a * (1 - q * 0.4)))
        c.drawCircle(xx, y_from + 10, 26 * (1 - q), P("#F5D0C0", 0.12 * a))


# ====================================================================================== the episode
class Petra(EpisodeV2):
    BUILD_NO = 38
    FIRST_SET = "cliff"
    CLEAR = "#12091C"
    TITLE = {"en": "PETRA", "ar_sa": "البترا"}
    EMPH = {"en": ["CONGRATS", "CARVE", "PALACE", "FORTY", "METERS", "CLIFF", "BRICK", "PETRA", "BOTTOM", "CHIP",
                   "FINISHED", "TOP", "DOWN", "DESERT", "RAINS", "TWENTY", "THOUSAND", "WATER", "CHANNEL", "WALL",
                   "CLAY", "PIPES", "SPRING", "CITY", "FLASH", "FLOOD", "DAM", "TUNNEL", "MOUNTAIN", "AROUND", "RICH",
                   "INCENSE", "RAIDER", "HIDE", "WINDING", "THREE", "FOLLOW", "JAPANESE", "PAGODA", "TOMBS", "THEATER",
                   "ROSE-RED", "EUROPE", "EIGHTEEN", "TWELVE", "KILOMETERS", "YEARS", "YOURSELF", "URN", "GOLD",
                   "SOLID", "ROCK", "COOKIE", "SEWING"],
            "ar_sa": ["مبروك", "حفرت", "قصر", "أربعين", "جبل", "صخر", "طوبة", "البترا", "تحت", "حتة", "هتبوظ", "خلصته",
                      "فوق", "لتحت", "صحرا", "والمطر", "نادر", "وعشرين", "مية", "قناة", "حيطة", "مواسير", "فخار", "عين",
                      "المدينة", "السيل", "الممر", "سد", "نفق", "الجبل", "يلف", "غنية", "بالبخور", "والحرامية",
                      "فتخبيها", "متعرج", "تلاتة", "تابعني", "ياباني", "الزلازل", "مقابر", "ومسرح", "الوردي",
                      "أوروبا", "ممر", "ألفين", "بإيدك", "الجرة", "دهب", "البسكوت", "إبرة", "وخيط"]}
    KEYS = {"ar_sa": {
        ("hook", "CARVE"): "حفرت", ("hook", "PALACE"): "قصر", ("hook", "FORTY"): "أربعين", ("hook", "CLIFF"): "جبل",
        ("hook", "BRICK"): "طوبة", ("hook", "CONGRATS"): "مبروك", ("hook", "PETRA"): "البترا",
        ("break1", "BOTTOM"): "تحت", ("break1", "CHIP"): "حتة", ("break1", "LANDS"): "هتبوظ", ("break1", "FINISHED"): "خلصته",
        ("fix1", "TOP"): "فوق", ("fix1", "DOWN"): "لتحت",
        ("break2", "DESERT"): "صحرا", ("break2", "RAINS"): "المطر", ("break2", "TWENTY"): "عشرين", ("break2", "WATER"): "مية",
        ("fix2", "CHANNEL"): "قناة", ("fix2", "WALL"): "حيطة", ("fix2", "PIPES"): "مواسير", ("fix2", "SPRING"): "عين",
        ("fix2", "CITY"): "المدينة",
        ("break3", "FLOOD"): "السيل", ("break3", "CANYON"): "الممر", ("break3", "CITY"): "المدينة",
        ("fix3", "DAM"): "سد", ("fix3", "TUNNEL"): "نفق", ("fix3", "MOUNTAIN"): "الجبل", ("fix3", "AROUND"): "يلف",
        ("break4", "RICH"): "غنية", ("break4", "INCENSE"): "بالبخور", ("break4", "RAIDER"): "والحرامية",
        ("fix4", "HIDE"): "فتخبيها", ("fix4", "WINDING"): "متعرج", ("fix4", "THREE"): "تلاتة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "TOMBS"): "مقابر", ("reveal", "THEATER"): "ومسرح", ("reveal", "ROSE"): "الوردي",
        ("reveal", "EUROPE"): "أوروبا", ("reveal", "EIGHTEEN"): "ألف",
        ("stat", "FORTY"): "أربعين", ("stat", "CANYON"): "ممر", ("stat", "THOUSAND"): "ألفين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "URN"): "الجرة", ("tag", "GOLD"): "دهب", ("tag", "SOLID"): "صخر", ("tag", "COOKIE"): "البسكوت",
        ("tag", "SEWING"): "إبرة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a Japanese pagoda"),
                   "stat": [("40 m", "TALL"), ("1.2 km", "OF CANYON"), ("2,000", "YEARS OLD")],
                   "L": {"cut": "CUT STRAIGHT OUT OF THE CLIFF", "brick": "NOT ONE BRICK", "petra": "PETRA",
                         "up": "CARVED BOTTOM UP", "chips": "CHIPS RAIN DOWN", "crack": "IT CRACKS", "top": "START AT THE TOP",
                         "down": "CARVE DOWN", "rain": "IT BARELY RAINS", "people": "20,000 PEOPLE", "channel": "A CHANNEL IN THE WALL",
                         "pipes": "CLAY PIPES", "spring": "SPRING", "city": "CITY", "flood": "FLASH FLOOD",
                         "into": "INTO THE CITY", "dam": "DAM", "tunnel": "TUNNEL", "around": "SENT AROUND",
                         "rich": "INCENSE = RICH", "raiders": "RAIDERS", "hidden": "HIDDEN AT THE END",
                         "narrow": "3 m WIDE", "tombs": "TOMBS AND A THEATER", "europe": "UNKNOWN TO EUROPE UNTIL 1812",
                         "gold": "GOLD INSIDE?", "solid": "SOLID ROCK", "tin": "GRANDMA'S COOKIE TIN",
                         "sew": "JUST SEWING STUFF", "siq": "THE SIQ"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: برج ياباني"),
                      "stat": [("40", "متر طول"), ("1.2", "كيلو ممر"), ("2,000", "سنة")],
                      "L": {"cut": "محفور في الجبل نفسه", "brick": "ولا طوبة", "petra": "البترا",
                            "up": "الحفر من تحت", "chips": "الحتت بتقع", "crack": "اتشرخ", "top": "ابدأ من فوق",
                            "down": "وانزل لتحت", "rain": "المطر نادر", "people": "عشرين ألف واحد", "channel": "قناة في الحيطة",
                            "pipes": "مواسير فخار", "spring": "عين مية", "city": "المدينة", "flood": "السيل",
                            "into": "على المدينة", "dam": "سد", "tunnel": "نفق", "around": "السيل لف بعيد",
                            "rich": "غنية بالبخور", "raiders": "حرامية", "hidden": "مستخبية في الآخر",
                            "narrow": "3 متر عرض", "tombs": "مقابر ومسرح", "europe": "أوروبا عرفتها سنة 1812",
                            "gold": "جواها دهب؟", "solid": "طلعت صخر", "tin": "علبة البسكوت",
                            "sew": "إبرة وخيط", "siq": "السيق"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "carve": ("hook", "CARVE", 0.05), "palace": ("hook", "PALACE", 0.12), "forty": ("hook", "FORTY", 0.25),
            "cliff": ("hook", "CLIFF", 0.45), "brick": ("hook", "BRICK", 0.6), "congrats": ("hook", "CONGRATS", 0.75),
            "petra": ("hook", "PETRA", 0.92),
            "bottom": ("break1", "BOTTOM", 0.2), "chip": ("break1", "CHIP", 0.45), "lands": ("break1", "LANDS", 0.65),
            "finished": ("break1", "FINISHED", 0.9),
            "top": ("fix1", "TOP", 0.4), "down": ("fix1", "DOWN", 0.85),
            "desert": ("break2", "DESERT", 0.15), "rains": ("break2", "RAINS", 0.35), "twenty": ("break2", "TWENTY", 0.6),
            "water": ("break2", "WATER", 0.9),
            "channel": ("fix2", "CHANNEL", 0.12), "wall": ("fix2", "WALL", 0.3), "pipes": ("fix2", "PIPES", 0.5),
            "spring": ("fix2", "SPRING", 0.7), "city": ("fix2", "CITY", 0.9),
            "flood": ("break3", "FLOOD", 0.35), "canyon": ("break3", "CANYON", 0.65), "city3": ("break3", "CITY", 0.9),
            "dam": ("fix3", "DAM", 0.1), "tunnel": ("fix3", "TUNNEL", 0.45), "mountain": ("fix3", "MOUNTAIN", 0.6),
            "around": ("fix3", "AROUND", 0.92),
            "rich": ("break4", "RICH", 0.2), "incense": ("break4", "INCENSE", 0.45), "raider": ("break4", "RAIDER", 0.85),
            "hide": ("fix4", "HIDE", 0.1), "winding": ("fix4", "WINDING", 0.5), "three": ("fix4", "THREE", 0.75),
            "follow": ("cta", "FOLLOW", 0.35),
            "tombs": ("reveal", "TOMBS", 0.1), "theater": ("reveal", "THEATER", 0.25), "rose": ("reveal", "ROSE", 0.45),
            "europe": ("reveal", "EUROPE", 0.7), "y1812": ("reveal", "EIGHTEEN", 0.85),
            "s1": ("stat", "FORTY", 0.04), "s2": ("stat", "CANYON", 0.3), "s3": ("stat", "THOUSAND", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "urn": ("tag", "URN", 0.25), "gold": ("tag", "GOLD", 0.4), "solid": ("tag", "SOLID", 0.55),
            "cookie": ("tag", "COOKIE", 0.8), "sewing": ("tag", "SEWING", 0.92)})
        T["cut0"] = 0.1
        T["cut1"] = max(min(T["brick"], T["congrats"]) - 0.2, 2.2)
        T["fall"] = max(T["chip"] - 0.2, s("break1") + 0.3)
        T["crack"] = max(T["lands"] - 0.1, T["fall"] + 0.5)
        T["topd"] = max(T["top"] - 0.4, s("fix1") + 0.05)
        T["lay"] = max(T["pipes"] - 0.4, T["wall"])
        T["flow"] = max(T["spring"] - 0.2, T["lay"] + 0.9)
        T["surge"] = max(T["flood"] - 0.3, s("break3") + 0.05)
        T["damup"] = max(T["dam"] - 0.15, s("fix3") + 0.05)
        T["tun"] = max(T["tunnel"] - 0.2, T["damup"] + 0.5)
        T["divert"] = max(T["mountain"] - 0.1, T["tun"] + 0.6)
        T["ride"] = max(T["raider"] - 0.6, T["incense"])
        T["tin"] = max(T["cookie"] - 0.4, T["solid"] + 0.6)
        # ---- sets
        self.cut(s("break1") - 0.12, "carve", 1)
        self.cut(s("break2") - 0.12, "pipe", -1)
        self.cut(s("break3") - 0.12, "map", 1)
        self.cut(s("break4") - 0.12, "siq", -1)
        self.cut(s("reveal") - 0.12, "cliff", 1)
        self.cut(s("tag") - 0.2, "urn", 1)
        # ---- cameras
        z0 = 0.95
        cm = Camera(0, -270 / z0 - 40, z0)
        cm.key(0.05, 0, -270 / z0 - 60, z0 * 1.04, 2.4)
        cm.key(s("reveal") - 0.12, 0, -270 / 0.62, 0.62, 0.0).key(T["tombs"], 0, -270 / 0.45, 0.45, 2.4)
        cm.key(s("stat") - 0.12, 0, -270 / 0.6, 0.6, 0.0)
        cm.key(s("closer") - 0.1, 0, -240 / 0.82 - 30, 0.82, 1.0)
        self.cam = cm
        cc = Camera(0, -270 / 0.95 - 40, 0.95)
        self.camc = cc
        self.shakes = [(T["cut1"], 0.3, 6), (T["congrats"], 0.3, 8), (T["crack"], 0.4, 10), (T["surge"] + 0.8, 0.4, 10),
                       (T["damup"] + 0.3, 0.3, 6), (T["ride"] + 0.5, 0.3, 6), (s("closer") + 0.2, 0.35, 10)]
        self.spans = [(T["finished"], T["down"] + 0.3), (T["water"], T["city"] + 0.3), (T["city3"], T["around"] + 0.3),
                      (T["raider"], T["three"] + 0.3)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def canyon(self, c, t, cam, wide=0.0):
        """Dusk sky, the cliff with the facade's recess, dark canyon walls on both sides (screen-space parallax)."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 300 * z)
        v2.stars(c, W, H, t, 0.5)
        self.view(c, cam)
        cliff(c, -2600, 2600, -1500, t, seed=3)
        vrect(c, cx - 1400 / z, -2, 2800 / z, 3000, ["#8A4A3A", "#6B3329", "#3A1814", "#1A0A08"], [0, 0.05, 0.3, 1])
        return gy

    def walls(self, c, open_=0.0):
        """The Siq's dark walls framing the shot (screen space)."""
        for sd in (-1, 1):
            p = skia.Path()
            x0 = 0 if sd < 0 else W
            xin = lerp(150, -260, open_) if sd < 0 else lerp(W - 150, W + 260, open_)
            p.moveTo(x0, 0)
            for k in range(13):
                yy = k * H / 12.0
                p.lineTo(xin + sd * (-40 * math.sin(k * 1.3) - 30 * math.cos(k * 2.1)), yy)
            p.lineTo(x0, H)
            p.close()
            c.drawPath(p, lin_paint(x0, 0, xin, 0, ["#1A0B0A", "#3A1A16", "#5E2C24"]))
            c.save()
            c.clipPath(p, doAntiAlias=True)
            striations(c, 0 if sd < 0 else W - 400, 400 if sd < 0 else W, 0, H, seed=11 + sd, a=0.35,
                       cols=("#7A3A2E", "#4A2018", "#8C4A3A"))
            c.restore()

    # ------------------------------------------------------------------ set: cliff (hook, reveal, stat, closer)
    def draw_cliff(self, c, t, cam=None):
        T, s = self.T, self.tl.s
        cam = cam or self.cam.at(t)
        self.canyon(c, t, cam)
        hook = t < s("break1")
        carved = lerp(0.14, 1.0, prog(t, T["cut0"], T["cut1"])) if hook else 1.0
        rv = t >= s("reveal") - 0.12
        if rv:                                                           # tombs and the theater around the Treasury
            k = prog(t, T["tombs"] - 0.3, T["tombs"] + 0.6)
            for i, (xx, sc, kind) in enumerate(((-650, 0.75, 0), (620, 0.7, 1), (-1020, 0.62, 1), (-1350, 0.55, 0))):
                tomb(c, xx, -30 - 50 * (i % 2), sc, kind, a=clamp(k * 1.5 - i * 0.15))
            theater(c, 980, -6, 0.55, a=prog(t, T["theater"] - 0.3, T["theater"] + 0.4))
        yl = treasury(c, 0, 0, 1.0, t, carved=e_out(carved), mode="down", glow=1.0 if not hook else prog(t, T["cut1"], T["cut1"] + 1.0))
        if hook and carved < 1:                                          # dust and chips at the cutting line
            chips_fall(c, -300, 300, yl, 0, t, a=1.0)
            for i in range(5):
                person(c, -240 + i * 120, yl - 2 + 0, 64, "#E7E5E4", t + i, pose="carry", face=1 if i % 2 else -1,
                       hat="none", hair="#1C1917", skin="#B07A4F", pants="#78350F")
        if hook:
            sh = 1 - prog(t, T["cut1"], T["cut1"] + 0.6)
            if sh > 0:
                c.drawRect(R(-330, yl, 660, 30), P("#FDE68A", 0.25 * sh, blur=8))
        c.restore()
        if not rv:
            self.walls(c, open_=0.0)
        self.ui["cam"] = cam

    def ui_cliff(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            self.chip(540, 400, "cut", T["palace"] - 0.1, T["brick"] - 0.1, accent="#FDBA74", size=34)
            self.chip(540, 400, "brick", T["brick"] - 0.1, T["petra"] - 0.1, accent=GOOD, size=40)
            self.chip(540, 400, "petra", T["petra"] - 0.1, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 470, "tombs", T["tombs"] - 0.1, T["europe"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 470, "europe", T["europe"] - 0.15, s("stat") - 0.15, accent=HILITE, size=34)

    # ------------------------------------------------------------------ set: carve (break1, fix1)
    def draw_carve(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.camc.at(t)
        self.canyon(c, t, cam)
        fixed = t >= s("fix1") - 0.12
        if not fixed:
            k = 0.5
            yl = treasury(c, 0, 0, 1.0, t, carved=k, mode="up", cracks=prog(t, T["crack"], T["crack"] + 0.6))
            chips_fall(c, -300, 300, yl - 20, -30, t, a=prog(t, T["fall"] - 0.3, T["fall"]), n=26)
            for i in range(4):                                           # carvers on a ledge, cutting upward
                person(c, -200 + i * 130, yl + 10, 64, "#E7E5E4", t + i, pose="point", face=1 if i % 2 else -1,
                       hat="none", hair="#1C1917", skin="#B07A4F", pants="#78350F")
        else:
            k = prog(t, T["topd"], s("break2") - 0.4)
            yl = treasury(c, 0, 0, 1.0, t, carved=lerp(0.06, 0.62, k), mode="down")
            chips_fall(c, -300, 300, yl, 0, t, a=1.0, n=18)
            for i in range(5):
                person(c, -240 + i * 120, yl - 2, 64, "#E7E5E4", t + i, pose="carry", face=1 if i % 2 else -1,
                       hat="none", hair="#1C1917", skin="#B07A4F", pants="#78350F")
            ak = prog(t, T["down"] - 0.4, T["down"])
            if ak > 0:
                arrow(c, 400, -760, 400, yl + 40, GOOD, a=ak, w=16, head=40)
        c.restore()
        self.ui["cam"] = cam
        self.ui["yl"] = yl

    def ui_carve(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.camc.at(tw))
        yl = self.ui.get("yl", -400)
        if tw < s("fix1") - 0.12:
            self.chip(540, 470, "up", T["bottom"] - 0.15, T["chip"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 470, "chips", T["chip"] - 0.1, T["crack"], accent=WARN, size=40)
            px, py = self.at(cam, 158, -200)
            self.label(px, py, 800, 600, "crack", T["crack"], s("fix1") - 0.15, WARN, size=40)
            self.badge("alert", T["finished"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["crack"] + 0.05, 1.4)
            return
        tx, ty = self.at(cam, -200, -790)
        self.label(tx, ty, 330, 380, "top", T["top"] - 0.3, s("break2") - 0.15, GOOD, size=38)
        self.chip(780, 1150, "down", T["down"] - 0.2, s("break2") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["down"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: pipe (break2, fix2)
    def draw_pipe(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#2A1220", "#5E2B2E", "#8A4436"])
        c.save()
        wall = skia.Path()
        wall.moveTo(0, 260)
        for k in range(12):
            wall.lineTo(k * 100, 300 + 40 * math.sin(k * 1.7))
        wall.lineTo(W, 300)
        wall.lineTo(W, 1060)
        wall.lineTo(0, 1060)
        wall.close()
        c.drawPath(wall, lin_paint(0, 300, 0, 1060, [ROCK[0], ROCK[1], ROCK[2]]))
        c.clipPath(wall, doAntiAlias=True)
        striations(c, 0, W, 260, 1060, seed=21, a=0.8)
        c.restore()
        vrect(c, 0, 1060, W, H - 1060, ["#B07A55", "#8A5A3C", "#3A2216", "#140A06"], [0, 0.15, 0.5, 1])
        for i in range(9):                                               # cracked dry ground
            c.drawLine(60 + i * 120, 1080, 100 + i * 120, 1150, P("#5A3A26", 0.8, stroke=3))
            c.drawLine(100 + i * 120, 1150, 70 + i * 120, 1200, P("#5A3A26", 0.8, stroke=3))
        fixed = t >= s("fix2") - 0.12
        y_of = lambda x: lerp(640, 700, x / W)                           # noqa: E731  the channel's line
        ck = prog(t, T["channel"] - 0.2, T["wall"] + 0.3) if fixed else 0.0
        if ck > 0:
            gp = skia.Path()
            gp.moveTo(0, y_of(0) - 34)
            gp.lineTo(W * ck, y_of(W * ck) - 34)
            gp.lineTo(W * ck, y_of(W * ck) + 34)
            gp.lineTo(0, y_of(0) + 34)
            gp.close()
            c.drawPath(gp, P("#3A1712"))
            c.drawLine(0, y_of(0) + 34, W * ck, y_of(W * ck) + 34, P("#E7A07F", 0.8, stroke=4))
        n = 9
        flowing = prog(t, T["flow"], T["flow"] + 1.6) if fixed else 0.0
        for i in range(n):                                               # clay pipes laid one by one
            q = prog(t, T["lay"] + i * 0.12, T["lay"] + i * 0.12 + 0.25) if fixed else 0.0
            if q <= 0:
                continue
            x0 = i * W / n
            yy = y_of(x0 + W / n / 2)
            c.save()
            c.translate(0, (1 - e_out(q)) * -120)
            c.drawRRect(rr(x0 + 4, yy - 24, W / n - 8, 48, 22), lin_paint(0, yy - 24, 0, yy + 24, ["#E58B5A", "#C2410C", "#7C2D12"], a=q))
            c.drawRRect(rr(x0 + W / n - 22, yy - 28, 22, 56, 8), P("#9A3412", q))
            if flowing > 0 and (i + 0.5) / n < flowing * 1.2:
                c.drawRect(R(x0 + 18, yy - 9, W / n - 44, 18), P("#1E3A8A", 0.9))
                pnt = P("#93C5FD", 0.95, stroke=8)
                pnt.setPathEffect(skia.DashPathEffect.Make([26, 18], -t * 160))
                c.drawLine(x0 + 18, yy, x0 + W / n - 26, yy, pnt)
            c.restore()
        if fixed:                                                        # the spring (left) and the basin (right)
            sk = prog(t, T["spring"] - 0.3, T["spring"] + 0.2)
            c.drawCircle(40, y_of(0), 60, P("#60A5FA", 0.5 * sk, blur=12))
            add_glow(c, 40, y_of(0), 120, "#93C5FD", 0.4 * sk)
            bk = prog(t, T["city"] - 0.4, T["city"])
            if flowing > 0.8:
                for i in range(6):
                    q = (t * 2.2 + i / 6.0) % 1.0
                    c.drawCircle(1000 + q * 10, y_of(1000) + 30 + q * 300, 7, P("#93C5FD", 0.9 * flowing))
            c.drawRRect(rr(880, 1010, 190, 60, 14), P("#7E3F33", bk))
            c.drawRRect(rr(890, 1018, 170, 26, 10), P(WATER, bk * flowing))
        k_people = 1.0
        for i in range(6):                                               # thirsty people with jars
            px = 140 + i * 120
            full = prog(t, T["city"] + 0.2 + i * 0.15, T["city"] + 0.6 + i * 0.15) if fixed else 0.0
            person(c, px, 1170, 120, ("#F5F5F4", "#FCA5A5", "#E7E5E4", "#FDE68A", "#E5E7EB", "#FBCFE8")[i], t + i,
                   pose="cheer" if full > 0.5 else "stand", face=1, hat="none", hair="#1C1917", skin="#B07A4F",
                   pants="#78350F", a=k_people)
            jar(c, px + 34, 1170, 0.9, full=full)
        if not fixed:
            sun_k = prog(t, s("break2"), s("break2") + 0.4)
            add_glow(c, 150, 230, 200, "#FFB37A", 0.6 * sun_k)
            c.drawCircle(150, 230, 50, P("#FFF1C9", sun_k))
            raindrop_x(c, 230, 470, 0.9, a=self.span(T["rains"] - 0.2, s("fix2") - 0.2))

    def ui_pipe(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(560, 470, "rain", T["rains"] - 0.15, s("fix2") - 0.15, accent="#93C5FD", size=40)
            self.chip(540, 920, "people", T["twenty"] - 0.15, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["water"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["water"] + 0.05, 1.3)
            return
        self.chip(540, 470, "channel", T["channel"] - 0.1, T["pipes"] - 0.15, accent="#E7A07F", size=40)
        self.chip(540, 470, "pipes", T["pipes"] - 0.15, s("break3") - 0.15, accent="#FB923C", size=42)
        self.label(40, 650, 230, 860, "spring", T["spring"] - 0.1, s("break3") - 0.15, "#93C5FD", size=34)
        self.label(975, 1010, 850, 860, "city", T["city"] - 0.1, s("break3") - 0.15, GOOD, size=34)
        self.badge("check", T["city"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: map (break3, fix3)
    WADI = [(1000, 300), (930, 390), (860, 470), (800, 560), (740, 650)]
    SIQ = [(740, 650), (700, 700), (650, 720), (620, 780), (560, 820), (540, 880), (480, 930), (450, 990), (400, 1030)]
    CITY_PTS = [(400, 1030), (320, 1080), (230, 1120)]
    TUNNEL = [(740, 650), (700, 600), (600, 560), (480, 540), (360, 560)]
    AROUND = [(360, 560), (240, 600), (150, 700), (110, 830), (110, 980), (90, 1150)]

    def pts_path(self, pts):
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        return p

    def grow(self, c, pts, k, paint):
        if k <= 0:
            return
        path = self.pts_path(pts)
        pm = skia.PathMeasure(path, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * clamp(k), seg, True)
        c.drawPath(seg, paint)

    def draw_map(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#D6B48A", "#C49A6C", "#A97B52"])
        rng = random.Random(4)
        for i in range(30):
            c.drawOval(R(rng.uniform(0, W), rng.uniform(250, 1250), rng.uniform(80, 220), rng.uniform(30, 70)), P("#E4C9A0", 0.35))
        mt = skia.Path()                                                 # the mountain the Siq cuts through
        mt.moveTo(330, 470)
        mt.quadTo(620, 420, 860, 600)
        mt.quadTo(760, 900, 560, 1100)
        mt.quadTo(380, 1100, 300, 900)
        mt.quadTo(250, 650, 330, 470)
        c.drawPath(mt, P("#9A4E3C"))
        for k in range(5):
            c.save()
            sc = 1 - k * 0.15
            c.translate(560 * (1 - sc), 760 * (1 - sc))
            c.scale(sc, sc)
            c.drawPath(mt, P("#6E3328", 0.5, stroke=4))
            c.restore()
        c.drawPath(self.pts_path(self.WADI + self.SIQ[1:] + self.CITY_PTS[1:]), P("#5B3A26", 0.9, stroke=30))
        c.drawPath(self.pts_path(self.SIQ), P("#2A1410", 1, stroke=14))
        for i, (bx, by) in enumerate(((180, 1150), (250, 1180), (320, 1140), (140, 1100), (380, 1180))):
            c.drawRect(R(bx - 26, by - 40, 52, 40), P("#F2B59A"))
            c.drawRect(R(bx - 8, by - 24, 16, 24), P("#5A2A22"))
        c.drawCircle(1000, 300, 26, P("#60A5FA"))
        fixed = t >= s("fix3") - 0.12
        fl = P("#2563EB", 0.95, stroke=26)
        if not fixed:
            k = prog(t, T["surge"], T["city3"] + 0.3)
            self.grow(c, self.WADI + self.SIQ[1:] + self.CITY_PTS[1:], k, fl)
            if k > 0.95:
                c.drawCircle(260, 1130, 120 * prog(t, T["city3"] + 0.2, T["city3"] + 0.8), P("#2563EB", 0.55))
        else:
            dk = prog(t, T["damup"], T["damup"] + 0.4)
            self.grow(c, self.WADI, 1.0, fl)
            if dk > 0:
                c.save()
                c.translate(740, 650)
                c.rotate(-40)
                c.drawRRect(rr(-70 * dk, -16, 140 * dk, 32, 8), P("#6B7280"))
                c.drawRRect(rr(-70 * dk, -16, 140 * dk, 32, 8), P("#E5E7EB", 1, stroke=4))
                c.restore()
            tk = prog(t, T["tun"], T["tun"] + 0.8)
            dash = P("#1F130C", 1, stroke=18)
            dash.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
            self.grow(c, self.TUNNEL, tk, dash)
            wk = prog(t, T["divert"], T["divert"] + 1.6)
            self.grow(c, self.TUNNEL + self.AROUND[1:], wk, P("#2563EB", 0.9, stroke=18))
            if wk > 0.98:
                add_glow(c, 260, 1140, 160, GOOD, 0.5)
        self.ui["fixed"] = fixed

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        word(c, self.L["siq"], 600, 860, 30, "#FDE68A", self.span(s("break3") - 0.1, s("break4") - 0.2), align="left")
        if tw < s("fix3") - 0.12:
            self.label(930, 390, 640, 330, "flood", T["flood"] - 0.2, s("fix3") - 0.15, "#93C5FD", size=40)
            self.label(260, 1130, 620, 1180, "into", T["city3"] - 0.1, s("fix3") - 0.15, WARN, size=40)
            self.badge("alert", T["city3"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["city3"] + 0.05, 1.3)
            return
        self.label(740, 650, 900, 760, "dam", T["damup"], T["around"] - 0.1, "#E5E7EB", size=40)
        self.label(600, 560, 600, 400, "tunnel", T["tun"], s("break4") - 0.15, "#FDE68A", size=40)
        self.label(110, 830, 330, 1010, "around", T["around"] - 0.4, s("break4") - 0.15, GOOD, size=36)
        self.badge("check", T["around"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: siq (break4, fix4, cta)
    def draw_siq(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        if not fixed:                                                    # the rich, open town and raiders on the ridge
            v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=900)
            v2.stars(c, W, H, t, 0.5)
            c.drawPath(self.ridge_path(), P("#3A1E26"))
            vrect(c, 0, 900, W, H - 900, ["#9A6A48", "#6E4A32", "#2E1C12"], [0, 0.4, 1])
            for i, bx in enumerate((300, 520, 760)):
                tomb(c, bx, 1130, 0.5, i % 2)
            for i in range(4):                                           # incense sacks and smoke
                sx = 220 + i * 190
                c.drawRRect(rr(sx - 40, 1120, 80, 90, 24), P("#C2A16B"))
                for k in range(4):
                    q = (t * 0.5 + k / 4.0 + i * 0.13) % 1.0
                    c.drawCircle(sx + math.sin(t * 2 + k + i) * 16, 1110 - q * 260, 14 + q * 26, P("#E5E7EB", 0.35 * (1 - q)))
            gk = prog(t, T["rich"] - 0.2, T["rich"] + 0.3)
            for i in range(10):
                add_glow(c, 200 + i * 75, 1100 + (i % 3) * 18, 20, "#FDE047", 0.6 * gk)
            rk = prog(t, T["ride"], T["ride"] + 0.8)
            for i in range(4):
                camel_fig(c, -200 + rk * 420 + i * 150, 900 - 6, 0.55, t * 8 + i, run=1.0, col="#1A0C10")
                c.drawCircle(-200 + rk * 420 + i * 150 + 10, 900 - 150, 14, P("#1A0C10"))
        else:                                                            # the winding Siq, the Treasury at the end
            v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=1300)
            vrect(c, 0, 0, W, H, ["#1A0B0A", "#2A1210", "#140707"])
            nk = prog(t, T["winding"] - 0.3, T["three"] + 0.3)
            gap = lerp(270, 175, nk)
            c.save()
            c.translate(540, 0)
            add_glow(c, 0, 900, 420, "#FFB08A", 0.55)
            treasury(c, 0, 1180, 0.55, t, glow=1.0)
            c.restore()
            for sd in (-1, 1):
                p = skia.Path()
                x0 = -200 if sd < 0 else W + 200
                p.moveTo(x0, -10)
                for k in range(15):
                    yy = -10 + k * 140
                    off = 60 * math.sin(k * 0.9 + 0.5) + 30 * math.sin(k * 2.3)
                    p.lineTo(540 + sd * (gap + 0.0 * k) + off, yy)
                p.lineTo(x0, H + 10)
                p.close()
                c.drawPath(p, lin_paint(540 + sd * gap, 0, x0, 0, ["#7E3F33", "#4A2320", "#1A0B0A"]))
                c.save()
                c.clipPath(p, doAntiAlias=True)
                striations(c, -200, W + 200, 0, H, seed=31 + sd, a=0.45, cols=("#A85A48", "#5A2A22", "#C7745E"))
                c.restore()
            person(c, 560, 1200, 110, "#F5F5F4", t, pose="walk", face=1, hat="none", hair="#1C1917",
                   skin="#B07A4F", pants="#78350F")
            ak = prog(t, T["three"] - 0.3, T["three"] + 0.1)
            if ak > 0:
                y_ = 1070
                xa, xb = 540 - gap * 0.8, 540 + gap * 0.8
                c.drawLine(xa, y_, xb, y_, P("#FFFFFF", ak, stroke=5))
                c.drawLine(xa, y_ - 20, xa, y_ + 20, P("#FFFFFF", ak, stroke=5))
                c.drawLine(xb, y_ - 20, xb, y_ + 20, P("#FFFFFF", ak, stroke=5))

    def ridge_path(self):
        p = skia.Path()
        p.moveTo(0, 900)
        for k in range(12):
            p.lineTo(k * 100, 880 - 40 * math.sin(k * 0.8) - 20 * math.cos(k * 1.9))
        p.lineTo(W, 900)
        p.close()
        return p

    def ui_siq(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 470, "rich", T["rich"] - 0.15, T["raider"] - 0.2, accent="#FDE047", size=40)
            self.chip(540, 470, "raiders", T["raider"] - 0.2, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["raider"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["raider"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 470, "hidden", T["hide"] - 0.1, T["three"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 470, "narrow", T["three"] - 0.15, s("cta") - 0.15, accent=HILITE, size=44)
            self.badge("check", T["three"] + 0.2, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: urn (tag)
    def draw_urn(self, c, t):
        T = self.T
        if t < T["tin"]:
            cam = (0, -720, 3.2)
            self.canyon(c, t, cam)
            treasury(c, 0, 0, 1.0, t, dents=prog(t, T["urn"] - 0.2, T["gold"] + 0.4), glow=0.6)
            rng = random.Random(3)
            for i in range(8):                                           # dust puffs where the old shots hit
                t0 = T["urn"] - 0.2 + i * 0.12
                q = prog(t, t0, t0 + 0.5)
                if 0 < q < 1:
                    c.drawCircle(rng.uniform(-22, 22), rng.uniform(-798, -764), 6 + q * 14, P("#F5D0C0", 0.6 * (1 - q)))
            c.restore()
            return
        room(c, 0, 0, W, 1250, wall="#6B4F3A", floor="#4A3426", t=t, lamp=True, lamp_x=540)
        vrect(c, 0, 1250, W, H - 1250, ["#4A3426", "#2E2018", "#150F0B"])
        c.drawRRect(rr(140, 1000, 800, 40, 10), P("#8B5A2B"))             # the table
        c.drawRect(R(180, 1040, 30, 210), P("#6B4423"))
        c.drawRect(R(870, 1040, 30, 210), P("#6B4423"))
        op = prog(t, T["tin"] + 0.3, T["sewing"])
        cx_, cy_ = 540, 990
        c.drawOval(R(cx_ - 210, cy_ - 50, 420, 70), P("#1E3A8A"))          # the blue tin
        c.drawRect(R(cx_ - 210, cy_ - 160, 420, 125), lin_paint(cx_ - 210, 0, cx_ + 210, 0, ["#1E40AF", "#3B82F6", "#1E3A8A"]))
        c.drawRect(R(cx_ - 210, cy_ - 120, 420, 34), P("#FDE68A", 0.8))
        if op > 0:                                                       # sewing things inside
            for i, col in enumerate(("#EF4444", "#22C55E", "#F59E0B", "#A855F7", "#EC4899")):
                c.drawRRect(rr(cx_ - 170 + i * 70, cy_ - 200 - 20 * op, 46, 56, 8), P(col, op))
                c.drawRect(R(cx_ - 172 + i * 70, cy_ - 206 - 20 * op, 50, 10), P("#F5F5F4", op))
            c.drawLine(cx_ + 160, cy_ - 260, cx_ + 120, cy_ - 160, P("#E5E7EB", op, stroke=5))
            for i in range(4):
                c.drawCircle(cx_ - 120 + i * 60, cy_ - 150, 12, P("#FDE68A", op))
        c.save()                                                         # the lid lifts off to the side
        k = e_out(op)
        c.translate(cx_ + 300 * k, cy_ - 160 - 260 * k)
        c.rotate(18 * k)
        c.drawOval(R(-222, -40, 444, 70), P("#1D4ED8"))
        c.drawRRect(rr(-222, -10, 444, 34, 10), P("#1E3A8A"))
        c.drawOval(R(-150, -30, 300, 44), P("#FDE68A", 0.9))
        c.drawOval(R(-110, -22, 220, 28), P("#1D4ED8", 0.8))
        c.restore()

    def ui_urn(self, c, t, tw):
        T = self.T
        if tw < T["tin"]:
            self.chip(540, 470, "gold", T["gold"] - 0.2, T["solid"] - 0.1, accent="#FDE047", size=44)
            self.chip(540, 470, "solid", T["solid"] - 0.1, T["tin"], accent="#F2B59A", size=44)
            return
        self.chip(540, 470, "tin", T["tin"], T["sewing"] - 0.05, accent="#93C5FD", size=40)
        k = self.span(T["sewing"] - 0.05, self.duration + 1, 0.25, 0.1)
        if k > 0:
            v2.chip(c, 540, 470, self.L["sew"], k, accent=HILITE, size=44)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8)]
        for k in range(9):
            ev.append((0.12 + k * (T["cut1"] - 0.2) / 9.0, sfx.click(61 + k), -14))
        ev += [(T["cut1"], sfx.thud(0.4), -10), (T["cut1"] + 0.2, sfx.sparkle(1.0, 12, 70), -8),
               (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 71), -9), (T["petra"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["fall"], sfx.creak(0.6), -14),
               (T["crack"], sfx.snap(73), -6), (T["crack"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["topd"] + k * 0.25, sfx.click(74 + k), -14) for k in range(6)]
        ev += [(T["down"] + 0.1, sfx.ding(), -8), (T["down"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 80), -4), (T["rains"], sfx.pop(81), -10),
               (T["water"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["channel"], sfx.creak(0.8), -12)]
        ev += [(T["lay"] + i * 0.12, sfx.thunk(82 + i), -14) for i in range(0, 9, 2)]
        ev += [(T["flow"], sfx.hiss(1.4, 90), -14), (T["city"] + 0.1, sfx.ding(), -8), (T["city"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 91), -4), (T["surge"], rumble(1.8, 92), -10),
               (T["city3"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["damup"], sfx.thud(0.4), -8), (T["tun"], sfx.creak(0.8), -12), (T["divert"], sfx.whoosh(1.2, False, 93), -12),
               (T["around"] + 0.1, sfx.ding(), -8), (T["around"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 94), -4), (T["rich"], sfx.sparkle(0.6, 8, 95), -12),
               (T["ride"], rumble(1.4, 96), -14), (T["raider"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.6, True, 97), -8), (T["three"], sfx.tick(), -10),
               (T["three"] + 0.3, sfx.ding(), -8), (T["three"] + 0.5, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(98), 0), (T["follow"] - 0.15, sfx.pop(99), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 100), -6), (T["tombs"], sfx.pop(101), -10),
               (T["theater"], sfx.pop(102), -10), (T["europe"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 103), -6), (T["s1"], sfx.pop(104), -3), (T["s2"], sfx.pop(105), -3),
               (T["s3"], sfx.pop(106), -3)]
        ev += [(T["cong2"], sfx.pop(107), -2), (T["cong2"], sfx.sparkle(1.0, 14, 108), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 109), -6)]
        ev += [(T["urn"] - 0.2 + i * 0.12, sfx.click(110 + i), -14) for i in range(6)]
        ev += [(T["solid"], sfx.thud(0.3), -10), (T["tin"], sfx.whoosh(0.4, True, 117), -8), (T["tin"] + 0.3, sfx.clank(900.0, 0.4, 118), -12),
               (T["sewing"], sfx.pop(119), -8)]
        return ev


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=10, head=26):
    if a <= 0:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    c.drawLine(x0, y0, x1 - math.cos(ang) * head * 0.6, y1 - math.sin(ang) * head * 0.6, P(col, a, stroke=w))
    hp = skia.Path()
    hp.moveTo(x1, y1)
    hp.lineTo(x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head)
    hp.lineTo(x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)
    hp.close()
    c.drawPath(hp, P(col, a))


NAME = "petra"
EPISODE = Petra
