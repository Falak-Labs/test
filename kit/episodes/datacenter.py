"""Episode 22 - An AI data center.  v2 look: night, seven sets with whip cuts.

Sets: hall (a thousand computers plugged into one room; it turns into an oven and the chips shut down), chip (close-up
of a board: cold plates with water on the chips), roof (the building cut open: water pipes up to the roof coolers),
town (the data center drinks a city's power and the town flickers; a substation next door with thick cables),
backup (training lost when the power blinks; the battery room and diesel generators), door (somebody trips over the
most important cable; fences, guards, cameras, a door that scans your face), desert (the plain gray box in the
middle of nowhere), phone (the tag: naming a cat).
Ground sets: the floor is y = 0, up is negative.
"""
from v2_base import *  # noqa: F401,F403

RACK, LED_G, LED_B, HOT = "#2B3248", "#22C55E", "#38BDF8", "#FF5A3C"
GRAY, SAND = "#8A93A6", "#C9A46A"
SKINS = ("#E8B48A", "#C68B5E", "#F1C9A5", "#8D5A3B", "#E0A47A")


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def along(pts, u):
    segs = [(pts[i], pts[i + 1], math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]
    total = sum(s[2] for s in segs)
    d = (u % 1.0) * total
    for (a, b, ln) in segs:
        if d <= ln:
            k = d / ln if ln else 0
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        d -= ln
    return pts[-1]


def pipe(c, pts, col="#7C8499", w=22, a=1.0):
    path = skia.Path()
    path.moveTo(*pts[0])
    for p in pts[1:]:
        path.lineTo(*p)
    c.drawPath(path, P("#1B2236", a, stroke=w + 8))
    c.drawPath(path, P(col, a, stroke=w))
    c.drawPath(path, P("#FFFFFF", 0.18 * a, stroke=w * 0.3))


def flow(c, pts, t, k, n=10, speed=0.45, col="#7DD3FC", r=6, seed=1):
    if k <= 0:
        return
    for i in range(n):
        x, y = along(pts, (t * speed + i / n) % 1.0)
        c.drawCircle(x, y, r, P(col, 0.95 * k))


def rack(c, x, y, t, on=1.0, hot=0.0, w=110, h=330, seed=0, a=1.0):
    """A server rack standing on y, left edge x. on: LEDs, hot 0..1 turns it red."""
    if a <= 0:
        return
    box(c, x, y - h, w, h, mix(RACK, "#5A2A2A", hot * 0.7), r=8, a=a)
    for k in range(10):
        sy = y - h + 16 + k * (h - 26) / 10
        c.drawRRect(rr(x + 10, sy, w - 20, (h - 26) / 10 - 6, 4), P(mix("#3B4462", "#7A3030", hot * 0.6), a))
        for j in range(4):
            lit = math.sin(t * (4 + j + seed % 3) + k * 1.7 + seed) > -0.3
            c.drawCircle(x + 22 + j * 12, sy + 11, 3.2, P(LED_G if j % 2 == 0 else LED_B, a * on * (1.0 if lit else 0.3)))
    if hot > 0:
        add_glow(c, x + w / 2, y - h / 2, 170, HOT, 0.4 * hot * a)


def heat_waves(c, x0, x1, y, t, k, height=420):
    if k <= 0:
        return
    for i in range(9):
        x = lerp(x0, x1, (i + 0.5) / 9)
        path = skia.Path()
        u0 = (t * 0.6 + i * 0.13) % 1.0
        yy = y - u0 * height
        path.moveTo(x, yy)
        for s_ in range(1, 7):
            path.lineTo(x + math.sin(t * 6 + s_ + i) * 14, yy - s_ * 22)
        c.drawPath(path, P("#FF8A4C", 0.55 * k * (1 - u0), stroke=6))


def fan(c, x, y, r, t, speed=1.0, a=1.0):
    c.drawCircle(x, y, r, P("#1F2937", a))
    c.drawCircle(x, y, r, P("#94A3B8", a, stroke=5))
    for b in range(5):
        ang = t * 9 * speed + b * 2 * math.pi / 5
        p = skia.Path()
        p.moveTo(x, y)
        p.quadTo(x + math.cos(ang + 0.5) * r * 0.9, y + math.sin(ang + 0.5) * r * 0.9,
                 x + math.cos(ang) * r * 0.86, y + math.sin(ang) * r * 0.86)
        p.close()
        c.drawPath(p, P("#CBD5E1", 0.9 * a))
    c.drawCircle(x, y, r * 0.18, P("#64748B", a))


def house(c, x, y, s=1.0, lit=1.0, seed=0):
    """A small house standing on y, centred on x."""
    w, h = 90 * s, 70 * s
    box(c, x - w / 2, y - h, w, h, "#6B5B7B", r=4)
    roof = skia.Path()
    roof.moveTo(x - w / 2 - 8 * s, y - h)
    roof.lineTo(x, y - h - 40 * s)
    roof.lineTo(x + w / 2 + 8 * s, y - h)
    roof.close()
    c.drawPath(roof, P("#3F3550"))
    for i in range(2):
        wx = x - w / 2 + 14 * s + i * (w - 46 * s)
        c.drawRect(R(wx, y - h + 16 * s, 18 * s, 18 * s), P(mix("#1E2235", "#FFD98A", lit)))
        if lit > 0.5:
            add_glow(c, wx + 9 * s, y - h + 25 * s, 30 * s, "#FFD98A", 0.25 * lit)


def transformer(c, x, y, k, t):
    """A big transformer on y, centred on x; k 0..1 pops it in."""
    if k <= 0:
        return
    s_ = e_back(clamp(k))
    c.save()
    c.translate(x, y)
    c.scale(s_, s_)
    box(c, -90, -150, 180, 150, "#64748B", r=8)
    for i in range(7):
        c.drawRect(R(-84 + i * 25, -140, 9, 130), P("#475569"))
    for i in (-50, 0, 50):
        c.drawRect(R(i - 6, -210, 12, 60), P("#CBD5E1"))
        for j in range(4):
            c.drawOval(R(i - 13, -206 + j * 14, 26, 9), P("#94A3B8"))
    c.restore()


def generator(c, x, y, t, run=0.0):
    """A diesel generator set on y, left edge x. run 0..1: it shakes and smokes."""
    dx = math.sin(t * 60) * 2.5 * run
    box(c, x + dx, y - 150, 300, 150, "#F59E0B", r=10)
    c.drawRect(R(x + 20 + dx, y - 128, 120, 90), P("#1F2937"))
    for i in range(6):
        c.drawRect(R(x + 28 + dx + i * 18, y - 120, 8, 74), P("#374151"))
    c.drawRect(R(x + 230 + dx, y - 250, 26, 110), P("#4B5563"))
    word(c, "DIESEL", x + 220 + dx, y - 60, 26, "#1F2937")
    if run > 0:
        v2.smoke(c, x + 243 + dx, y - 256, t, 0.0, None, rate=12, life=1.6, spread=(60, -40), rise=-90, size=(14, 50),
                 col="#9CA3AF")


def battery(c, x, y, charge, t, on=1.0):
    box(c, x, y - 260, 120, 260, "#1F2937", r=8)
    for k in range(6):
        yy = y - 240 + k * 38
        c.drawRRect(rr(x + 14, yy, 92, 26, 5), P("#0B1220"))
        f = clamp(charge * 1.2 - k * 0.04)
        c.drawRRect(rr(x + 16, yy + 2, 88 * f, 22, 4), P(mix("#F59E0B", "#22C55E", charge), 0.95 * on))
    c.drawRect(R(x + 46, y - 276, 28, 16), P("#94A3B8"))


def camera(c, x, y, t, k):
    if k <= 0:
        return
    s_ = e_back(clamp(k))
    c.save()
    c.translate(x, y)
    c.scale(s_, s_)
    c.drawRect(R(-5, 0, 10, 160), P("#94A3B8"))
    c.save()
    c.rotate(18 + math.sin(t * 1.3) * 14)
    c.drawRRect(rr(-10, -26, 74, 34, 8), P("#E2E8F0"))
    c.drawCircle(64, -9, 11, P("#0B1220"))
    c.drawCircle(4, -16, 5, P("#EF4444", 0.5 + 0.5 * math.sin(t * 6)))
    c.restore()
    c.restore()


def fence(c, x0, x1, y, h, k):
    if k <= 0:
        return
    hh = h * e_out(clamp(k))
    c.save()
    c.clipRect(R(x0, y - hh, x1 - x0, hh))
    for xx in range(int(x0), int(x1), 26):
        c.drawLine(xx, y, xx + hh * 0.6, y - hh, P("#CBD5E1", 0.55, stroke=2.5))
        c.drawLine(xx + hh * 0.6, y, xx, y - hh, P("#CBD5E1", 0.55, stroke=2.5))
    c.restore()
    for xx in range(int(x0), int(x1) + 1, 160):
        c.drawRect(R(xx - 5, y - hh - 10, 10, hh + 10), P("#94A3B8"))
    c.drawLine(x0, y - hh, x1, y - hh, P("#94A3B8", 1, stroke=6))


def boom_snd(d=1.0, seed=50):
    return boom(d, seed)


def hum_up(d=1.4, seed=51):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 60 + 90 * tt / d
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / sfx.SR)
    return sfx._norm(x * sfx._ar(n, 0.3, 0.3), 0.6)


def engine_snd(d=1.6, seed=52):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sign(np.sin(2 * np.pi * 34 * tt)) * 0.5 + sfx._lp(sfx._rng(seed).standard_normal(n), 300)
    return sfx._norm(sfx._lp(x, 700) * sfx._ar(n, 0.15, 0.3), 0.7)


# ====================================================================================== the episode
class DataCenter(EpisodeV2):
    BUILD_NO = 22
    FIRST_SET = "hall"
    CLEAR = "#070B1F"
    TITLE = {"en": "AI DATA CENTER", "ar_sa": "مركز بيانات"}
    EMPH = {"en": ["CONGRATS", "AI", "DATA", "CENTER", "THOUSAND", "HOT", "OVEN", "SHUTS", "COLD", "PLATES", "COOLERS", "ROOF",
                   "CITY", "FLICKER", "SUBSTATION", "TRANSFORMERS", "HOUSES", "CABLES", "BLINKS", "HOURS", "VANISH",
                   "BATTERIES", "INSTANTLY", "DIESEL", "TEN", "TRIPS", "CABLE", "FENCES", "GUARDS", "CAMERAS", "FACE",
                   "FOLLOW", "PLAIN", "GRAY", "BOX", "NOWHERE", "HUNDRED", "ONE", "ZERO", "YOURSELF", "CAT"],
            "ar_sa": ["مبروك", "بيانات", "ألف", "بيسخنوا", "فرن", "تقفل", "ساقعة", "ألواح", "ومبردات", "مدينة", "بيرعش", "محطة",
                      "بمحولات", "البيوت", "وكابلات", "قطعت", "ساعات", "تطير", "بطاريات", "لحظة", "ديزل", "عشر", "ويتكعبل", "كابل",
                      "أسوار", "وأمن", "وكاميرات", "وشه", "تابعني", "صندوق", "رمادي", "الصحرا", "مية", "وصفر", "بإيدك", "لقطته"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "PLUG"): "وصلت", ("hook", "THOUSAND"): "ألف", ("hook", "ROOM"): "أوضة", ("hook", "CONGRATS"): "مبروك",
        ("hook", "DATA"): "بيانات",
        ("break1", "HOT"): "بيسخنوا", ("break1", "OVEN"): "فرن", ("break1", "MINUTES"): "دقايق", ("break1", "SHUTS"): "تقفل",
        ("fix1", "PUMP"): "فتعدي", ("fix1", "COLD"): "ساقعة", ("fix1", "PLATES"): "ألواح", ("fix1", "CHIPS"): "الشرايح",
        ("fix1", "COOLERS"): "ومبردات", ("fix1", "ROOF"): "السطح", ("fix1", "HEAT"): "الحرارة", ("fix1", "OUTSIDE"): "برة",
        ("break2", "COOL"): "ساقعة", ("break2", "DRINKS"): "بتشرب", ("break2", "POWER"): "كهربا", ("break2", "CITY"): "مدينة",
        ("break2", "LIGHTS"): "ونور", ("break2", "FLICKER"): "بيرعش",
        ("fix2", "SUBSTATION"): "محطة", ("fix2", "TRANSFORMERS"): "بمحولات", ("fix2", "HOUSES"): "البيوت",
        ("fix2", "CABLES"): "وكابلات", ("fix2", "ARM"): "دراعك",
        ("break3", "BLINKS"): "قطعت", ("break3", "SECOND"): "ثانية", ("break3", "HOURS"): "ساعات", ("break3", "VANISH"): "تطير",
        ("fix3", "BATTERIES"): "بطاريات", ("fix3", "INSTANTLY"): "لحظة", ("fix3", "DIESEL"): "ديزل",
        ("fix3", "GENERATORS"): "ومولدات", ("fix3", "TEN"): "عشر",
        ("break4", "STOPS"): "بتقف", ("break4", "WALKS"): "يدخل", ("break4", "TRIPS"): "ويتكعبل", ("break4", "CABLE"): "كابل",
        ("fix4", "FENCES"): "أسوار", ("fix4", "GUARDS"): "وأمن", ("fix4", "CAMERAS"): "وكاميرات", ("fix4", "DOOR"): "وباب",
        ("fix4", "SCANS"): "يتعرف", ("fix4", "FACE"): "وشه",
        ("cta", "START"): "تشغلها", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "HIDE"): "خبيها", ("reveal", "PLAIN"): "عادي", ("reveal", "GRAY"): "رمادي", ("reveal", "BOX"): "صندوق",
        ("reveal", "NOWHERE"): "الصحرا",
        ("stat", "HUNDRED"): "مية", ("stat", "ONE"): "كهربا", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "POWER"): "الكهربا", ("tag", "HALF"): "نص", ("tag", "NAME"): "اسم", ("tag", "CAT"): "لقطته"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a desalination plant"),
                   "stat": [("100,000", "CHIPS"), ("1", "CITY OF POWER"), ("0", "WINDOWS")],
                   "L": {"room": "ONE ROOM", "temp": "TEMPERATURE", "oven": "OVEN MODE", "plate": "COLD PLATE",
                         "water": "COLD WATER", "coolers": "ROOF COOLERS", "power": "POWER USE", "city": "= A WHOLE CITY",
                         "sub": "SUBSTATION", "trans": "BIGGER THAN A HOUSE", "cables": "ARM-THICK CABLES",
                         "train": "TRAINING", "lost": "HOURS LOST", "batt": "BATTERY ROOM", "gen": "DIESEL GENERATORS",
                         "ten": "10 SECONDS", "cable": "THE MOST IMPORTANT CABLE", "fence": "FENCES", "guards": "GUARDS",
                         "cams": "CAMERAS", "scan": "FACE SCAN", "box": "PLAIN GRAY BOX", "nowhere": "THE MIDDLE OF NOWHERE",
                         "ask": "Name my cat?", "reply": "Sir Meowsalot"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: محطة تحلية"),
                      "stat": [("100,000", "شريحة"), ("1", "مدينة كهربا"), ("0", "شبابيك")],
                      "L": {"room": "أوضة واحدة", "temp": "الحرارة", "oven": "بقت فرن", "plate": "لوح تبريد",
                            "water": "مية ساقعة", "coolers": "مبردات السطح", "power": "الكهربا", "city": "= مدينة كاملة",
                            "sub": "محطة كهربا", "trans": "أكبر من بيت", "cables": "كابلات قد الدراع",
                            "train": "التدريب", "lost": "ساعات طارت", "batt": "أوضة البطاريات", "gen": "مولدات ديزل",
                            "ten": "10 ثواني", "cable": "أهم كابل", "fence": "أسوار", "guards": "أمن",
                            "cams": "كاميرات", "scan": "بيتعرف على الوش", "box": "صندوق رمادي عادي", "nowhere": "نص الصحرا",
                            "ask": "أسمّي قطتي إيه؟", "reply": "مشمش"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "plug": ("hook", "PLUG", 0.1), "thousand": ("hook", "THOUSAND", 0.22), "room": ("hook", "ROOM", 0.4),
            "congrats": ("hook", "CONGRATS", 0.55), "data": ("hook", "DATA", 0.85),
            "hot": ("break1", "HOT", 0.25), "oven": ("break1", "OVEN", 0.5), "minutes": ("break1", "MINUTES", 0.6),
            "shuts": ("break1", "SHUTS", 0.85),
            "pump": ("fix1", "PUMP", 0.08), "cold": ("fix1", "COLD", 0.14), "plates": ("fix1", "PLATES", 0.3),
            "chips": ("fix1", "CHIPS", 0.45), "coolers": ("fix1", "COOLERS", 0.6), "roof": ("fix1", "ROOF", 0.72),
            "heat": ("fix1", "HEAT", 0.85), "outside": ("fix1", "OUTSIDE", 0.95),
            "cool": ("break2", "COOL", 0.12), "drinks": ("break2", "DRINKS", 0.3), "power": ("break2", "POWER", 0.42),
            "city": ("break2", "CITY", 0.6), "lights": ("break2", "LIGHTS", 0.75), "flicker": ("break2", "FLICKER", 0.92),
            "sub": ("fix2", "SUBSTATION", 0.2), "trans": ("fix2", "TRANSFORMERS", 0.45), "houses": ("fix2", "HOUSES", 0.6),
            "cables": ("fix2", "CABLES", 0.75), "arm": ("fix2", "ARM", 0.95),
            "blinks": ("break3", "BLINKS", 0.35), "second": ("break3", "SECOND", 0.6), "hours": ("break3", "HOURS", 0.75),
            "vanish": ("break3", "VANISH", 0.92),
            "batt": ("fix3", "BATTERIES", 0.2), "instant": ("fix3", "INSTANTLY", 0.4), "diesel": ("fix3", "DIESEL", 0.55),
            "gens": ("fix3", "GENERATORS", 0.65), "ten": ("fix3", "TEN", 0.85),
            "stops": ("break4", "STOPS", 0.15), "walks": ("break4", "WALKS", 0.45), "trips": ("break4", "TRIPS", 0.6),
            "cable": ("break4", "CABLE", 0.8),
            "fences": ("fix4", "FENCES", 0.12), "guards": ("fix4", "GUARDS", 0.22), "cams": ("fix4", "CAMERAS", 0.32),
            "door": ("fix4", "DOOR", 0.45), "scans": ("fix4", "SCANS", 0.8), "face": ("fix4", "FACE", 0.92),
            "start": ("cta", "START", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "hide": ("reveal", "HIDE", 0.2), "plain": ("reveal", "PLAIN", 0.45), "gray": ("reveal", "GRAY", 0.55),
            "box": ("reveal", "BOX", 0.65), "nowhere": ("reveal", "NOWHERE", 0.92),
            "s1": ("stat", "HUNDRED", 0.04), "s2": ("stat", "ONE", 0.42), "s3": ("stat", "ZERO", 0.72),
            "cong2": ("closer", "CONGRATS", 0.16),
            "power2": ("tag", "POWER", 0.15), "half": ("tag", "HALF", 0.4), "name": ("tag", "NAME", 0.75), "cat": ("tag", "CAT", 0.9)})
        T["trip"] = T["trips"] + 0.1
        # ---- sets
        self.cut(s("fix1") - 0.12, "chip", 1)
        self.cut(T["coolers"] - 0.25, "roof", -1)
        self.cut(s("break2") - 0.12, "town", -1)
        self.cut(s("break3") - 0.12, "backup", 1)
        self.cut(s("break4") - 0.12, "door", 1)
        self.cut(s("cta") + 0.05, "desert", -1)
        self.cut(s("tag") - 0.2, "phone", 1)
        self.cams = {"hall": Camera(0, -240, 1.3), "chip": Camera(0, 0, 1.0), "roof": Camera(0, -330, 0.9),
                     "town": Camera(-160, -240, 0.84), "backup": Camera(0, -260, 1.0), "door": Camera(0, -230, 1.1),
                     "desert": Camera(0, -260, 0.95), "phone": Camera(0, 0, 1.0)}
        cm = self.cams
        cm["hall"].key(0.05, 0, -230, 1.15, 1.0).key(T["thousand"] - 0.1, 0, -260, 0.82, 1.2)
        cm["hall"].key(s("break1") + 0.2, 0, -250, 0.95, 1.2)
        cm["chip"].key(s("fix1"), 0, 0, 1.05, 2.0)
        cm["roof"].key(T["coolers"], 0, -380, 0.95, 1.2)
        cm["town"].key(s("break2") + 0.3, -100, -240, 0.82, 2.0).key(s("fix2") - 0.1, -230, -220, 0.92, 1.0)
        cm["backup"].key(s("fix3") - 0.12, 300, -250, 0.95, 0.8).key(T["diesel"] - 0.3, 640, -240, 0.84, 0.9)
        cm["door"].key(T["walks"] - 0.3, 60, -230, 1.2, 1.4).key(s("fix4") - 0.1, 0, -260, 0.95, 0.8)
        cm["desert"].key(T["hide"] - 0.2, 0, -240, 0.9, 1.0).key(T["nowhere"] - 0.4, 0, -300, 0.42, 1.4)
        cm["desert"].key(T["s1"] - 0.3, 0, -360, 0.3, 1.0).key(s("closer") - 0.2, 0, -280, 0.55, 0.9)
        # ---- tracks
        self.racks = Track(1.0).to(T["thousand"] - 0.1, 18.0, max(0.8, T["room"] - T["thousand"] + 0.6), e_out)
        self.heat = Track(0.0).to(T["hot"] - 0.2, 1.0, max(0.8, T["oven"] - T["hot"] + 0.6))
        self.temp = Track(0.25).to(T["hot"] - 0.2, 0.98, max(1.0, T["shuts"] - T["hot"]))
        self.chipheat = Track(1.0).to(T["chips"] - 0.1, 0.0, 1.3)
        self.meter = Track(0.15).to(T["drinks"] - 0.2, 0.97, max(0.8, T["city"] - T["drinks"] + 0.4))
        self.train = Track(0.2).to(s("break3"), 0.87, max(0.6, T["blinks"] - s("break3") - 0.2))
        self.train.to(T["hours"] - 0.2, 0.0, 0.5)
        self.charge = Track(0.0).to(T["batt"] - 0.1, 1.0, 0.7)
        self.walk = Track(-700.0).to(T["walks"] - 0.4, -120.0, max(0.6, T["trip"] - T["walks"] + 0.4))
        self.wall = Track(0.0).to(T["hide"] - 0.05, 1.0, max(0.6, T["box"] - T["hide"] + 0.2), e_io)
        self.spans = [(T["shuts"], T["outside"] + 0.2), (T["flicker"], T["arm"] + 0.2), (T["blinks"], T["ten"] + 0.5),
                      (T["trip"], T["face"] + 0.4)]
        self.shakes = [(T["plug"], 0.3, 10), (T["shuts"], 0.3, 8), (T["plates"] + 0.2, 0.25, 8), (T["blinks"], 0.4, 10),
                       (T["gens"], 0.6, 10), (T["trip"], 0.5, 18), (s("closer") + 0.2, 0.35, 10)]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def interior(self, c, t, cam, wall="#1C2340", lights=1.0, tint=0.0):
        """A data hall: back wall, ceiling trays, floor. Screen space background + world floor."""
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, [mix(wall, "#3A1414", tint), mix("#10162C", "#200A0A", tint)]))
        self.view(c, cam)
        cx, cy, z = cam
        x0, x1 = cx - 700 / z, cx + 700 / z
        c.drawRect(R(x0, -640, x1 - x0, 30), P("#2E3656"))
        for xx in range(int(x0) // 220 * 220, int(x1), 220):
            c.drawRect(R(xx, -610, 8, 40), P("#3B4466"))
            c.drawRRect(rr(xx + 40, -600, 120, 14, 6), P("#E0F2FE", 0.8 * lights))
            if lights > 0.3:
                add_glow(c, xx + 100, -590, 140, "#C7E7FF", 0.18 * lights)
        c.drawRect(R(x0, 0, x1 - x0, 900), lin_paint(0, 0, 0, 400, ["#3B4160", "#202538"]))
        for xx in range(int(x0) // 120 * 120, int(x1), 120):
            c.drawLine(xx, 0, xx - 60, 400, P("#FFFFFF", 0.05, stroke=2))
        c.drawLine(x0, 0, x1, 0, P("#9AA6BF", 0.6, stroke=4))

    # ------------------------------------------------------------------ set: the hall (hook, break1)
    def draw_hall(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["hall"].at(t)
        heat = self.heat.at(t)
        self.interior(c, t, cam, tint=0.8 * heat)
        n = self.racks.at(t)
        off = prog(t, T["shuts"] - 0.1, T["shuts"] + 1.0)
        for i in range(18):                                                         # back row, smaller
            k = clamp(n - i)
            if k > 0:
                rack(c, -860 + i * 100, -40, t, on=1 - off, hot=heat * 0.8, w=80, h=250, seed=i + 7, a=0.55 * k)
        for i in range(9):                                                          # front row
            k = clamp(n * 0.5 - i)
            x = -560 + i * 128
            if k > 0:
                c.save()
                c.translate(x + 55, 0)
                c.scale(e_back(k), e_back(k))
                c.translate(-(x + 55), 0)
                rack(c, x, 0, t, on=1 - clamp(off * 9 - i), hot=heat, seed=i)
                c.restore()
        if t < T["thousand"] + 0.2:                                                 # the first computer
            box(c, -40, -150, 80, 150, "#334155", r=8)
            c.drawCircle(0, -120, 6, P(LED_B))
        plug = prog(t, T["plug"] - 0.4, T["plug"])                                  # the plug going into the wall
        c.drawRect(R(560, -120, 60, 90), P("#E5E7EB"))
        px = lerp(860, 620, e_in(plug))
        c.drawLine(px + 40, -75, 1000, -40, P("#111827", 1, stroke=14))
        box(c, px, -100, 46, 50, "#111827", r=6)
        sparks_shower(c, 620, -75, t, T["plug"], 0.6, n=18, speed=420, seed=5)
        heat_waves(c, -560, 600, -330, t, heat)
        c.restore()
        self.ui["cam"] = cam

    def ui_hall(self, c, t, tw):
        T, s = self.T, self.tl.s
        p = self.span(s("break1") - 0.1, s("fix1") - 0.12)
        if p > 0:
            k = self.temp.at(tw)
            v2.gauge(c, 60, 300, [(self.L["temp"], k, mix(GOOD, WARN, k))], p, w=330)
        self.chip(540, 560, "oven", T["oven"] - 0.05, s("fix1") - 0.15, accent=WARN, size=42)
        self.badge("alert", T["shuts"], s("fix1") - 0.2)
        self.red(T["hot"], 2.4)

    # ------------------------------------------------------------------ set: the chip close-up (fix1, first half)
    PIPE_A = [(-420, -520), (-260, -520), (-260, -150)]
    PIPE_B = [(260, -150), (260, -520), (420, -520)]

    def draw_chip(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["chip"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B132B", "#05081A"]))
        self.view(c, cam)
        c.drawRRect(rr(-460, -330, 920, 660, 26), lin_paint(0, -330, 0, 330, ["#166534", "#14532D"]))     # the board
        rng = random.Random(4)
        for _ in range(40):
            x, y = rng.uniform(-440, 440), rng.uniform(-310, 310)
            c.drawLine(x, y, x + rng.choice((-1, 1)) * rng.uniform(40, 160), y, P("#FCD34D", 0.25, stroke=3))
        hot = self.chipheat.at(t)
        plates = prog(t, T["plates"] - 0.35, T["plates"])
        for cx_ in (-200, 200):                                                       # two chips
            box(c, cx_ - 120, -120, 240, 240, "#111827", r=12)
            c.drawRRect(rr(cx_ - 80, -80, 160, 160, 10), P(mix("#475569", "#FF3B1F", hot)))
            if hot > 0.05:
                add_glow(c, cx_, 0, 240, HOT, 0.55 * hot)
            if plates > 0:
                py = lerp(-700, -130, e_in(plates))
                box(c, cx_ - 130, py, 260, 260, "#C2793E", r=14)
                for k in range(6):
                    c.drawRect(R(cx_ - 110 + k * 40, py + 30, 16, 200), P("#9A5B2B"))
        flowing = t >= T["plates"] + 0.1
        if flowing:
            for pts, col in ((self.PIPE_A, "#38BDF8"), (self.PIPE_B, "#60A5FA")):
                pipe(c, pts, col, 26)
            c.drawLine(-70, -20, 70, -20, P("#38BDF8", 1, stroke=26))
            flow(c, self.PIPE_A + [(-70, -20), (70, -20)] + self.PIPE_B[0:1] + self.PIPE_B[1:], t, 1.0, n=18, speed=0.4, r=8)
        c.restore()
        self.ui["cam"] = cam

    def ui_chip(self, c, t, tw):
        T = self.T
        x0, y0 = self.at(-200, -130)
        self.label(x0 - 100, y0, 280, 420, "plate", T["plates"] + 0.1, T["coolers"] - 0.3, "#FDBA74")
        x1, y1 = self.at(-260, -400)
        self.label(x1, y1, 760, 420, "water", T["cold"] + 0.4, T["coolers"] - 0.3, "#38BDF8")

    # ------------------------------------------------------------------ set: the roof (fix1, second half)
    def building(self, c, t, inside=1.0, w=900, h=480, x=-450):
        """The data center cut open: racks inside, a flat roof at y = -h."""
        box(c, x, -h, w, h, "#4B5568", r=6)
        if inside > 0:
            c.drawRect(R(x + 20, -h + 20, w - 40, h - 20), P("#141A30", inside))
            for i in range(7):
                rack(c, x + 40 + i * 120, 0, t, w=90, h=300, seed=i + 3, a=inside)
        c.drawRect(R(x - 10, -h - 16, w + 20, 18), P("#6B7385"))

    def draw_roof(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["roof"].at(t)
        v2.sky(c, W, H, 0.0, horizon_y=(0 - cam[1]) * cam[2] + H / 2)
        v2.stars(c, W, H, t, 0.8)
        self.view(c, cam)
        c.drawRect(R(-3000, 0, 6000, 3000), P("#2A2F45"))
        self.building(c, t)
        up = [(-300, -60), (-300, -520), (-240, -520)]
        pipe(c, up, "#38BDF8", 18)
        flow(c, up, t, 1.0, n=10, speed=0.5, col="#FDBA74", r=6)
        for i, fx in enumerate((-260, 0, 260)):                                       # roof coolers
            k = prog(t, T["coolers"] + i * 0.12, T["coolers"] + 0.35 + i * 0.12)
            if k <= 0:
                continue
            sk = e_back(k)
            c.save()
            c.translate(fx, -500)
            c.scale(sk, sk)
            box(c, -110, -90, 220, 90, "#94A3B8", r=10)
            c.restore()
            fan(c, fx, -545, 34 * sk, t, 1.6)
            if t >= T["heat"] - 0.2:
                heat_waves(c, fx - 90, fx + 90, -600, t, prog(t, T["heat"] - 0.2, T["heat"] + 0.3), height=380)
        c.restore()
        self.ui["cam"] = cam

    def ui_roof(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(260, -560)
        self.label(x0 + 40, y0, 800, 420, "coolers", T["coolers"] + 0.3, s("break2") - 0.2, "#38BDF8")
        self.badge("check", T["outside"] + 0.1, s("break2") - 0.15, x=230, y=470)

    # ------------------------------------------------------------------ set: the town (break2, fix2)
    def draw_town(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["town"].at(t)
        v2.sky(c, W, H, 0.0, horizon_y=(0 - cam[1]) * cam[2] + H / 2)
        v2.stars(c, W, H, t, 0.8)
        self.view(c, cam)
        c.drawRect(R(-3000, 0, 6000, 3000), P("#1E2235"))
        self.building(c, t, inside=0.0, x=-860, w=480, h=400)
        for k in range(4):
            c.drawRect(R(-840, -340 + k * 86, 440, 10), P("#7DD3FC", 0.6))
        flick = prog(t, T["lights"] - 0.2, T["lights"] + 0.2) * (1 - prog(t, T["cables"], T["cables"] + 0.4))
        for i in range(7):                                                           # the town
            hx = 40 + i * 112
            n = (math.sin(t * 23 + i * 7) + math.sin(t * 13 + i)) * 0.5
            lit = 1.0 - flick * (0.85 if n > -0.2 else 0.2)
            house(c, hx, 0, 1.1 if i % 3 else 1.3, lit)
        for tx in (-330, 160, 650):                                                  # power line
            lattice(c, tx, 0, -330, w=40, col=STEEL)
        for k in range(3):
            path = skia.Path()
            path.moveTo(-380, -300 + k * 16)
            for tx in (160, 650, 900):
                path.quadTo(tx - 245, -230 + k * 16, tx, -300 + k * 16)
            c.drawPath(path, P("#94A3B8", 0.8, stroke=3))
        sub = prog(t, T["sub"] - 0.2, T["sub"] + 0.2)
        if sub > 0:
            fence(c, -350, 10, 0, 110, sub)
            for i, tx in enumerate((-270, -100)):
                transformer(c, tx, 0, prog(t, T["trans"] - 0.15 + i * 0.12, T["trans"] + 0.25 + i * 0.12), t)
            hk = prog(t, T["houses"] - 0.1, T["houses"] + 0.3)
            if hk > 0:                                                               # a house, for scale
                house(c, -20 + 0 * hk, 0, 0.62 * e_back(hk), 1.0)
            ck = prog(t, T["cables"] - 0.1, T["cables"] + 0.5)
            for k in range(3):
                x0 = -270 + (k % 2) * 170
                c.drawLine(x0, -200, lerp(x0, -382, ck), lerp(-200, -150 - k * 50, ck), P("#0B1220", 1, stroke=20))
                if ck >= 1:
                    u = (t * 1.2 + k * 0.3) % 1.0
                    add_glow(c, lerp(x0, -382, u), lerp(-200, -150 - k * 50, u), 40, "#FDE047", 0.7)
        c.restore()
        self.ui["cam"] = cam

    def ui_town(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2"):
            p = self.span(T["drinks"] - 0.3, s("fix2") - 0.1)
            if p > 0:
                k = self.meter.at(tw)
                v2.gauge(c, 60, 300, [(self.L["power"], k, mix("#38BDF8", WARN, k))], p, w=330)
            self.chip(540, 560, "city", T["city"] - 0.05, s("fix2") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["flicker"], s("fix2") - 0.2)
            self.red(T["flicker"], 2.0)
            return
        x0, y0 = self.at(-180, -120)
        self.label(x0, y0, 760, 430, "sub", T["sub"] + 0.2, T["trans"] - 0.05, HILITE)
        x1, y1 = self.at(-20, -60)
        self.label(x1, y1, 760, 430, "trans", T["houses"] + 0.2, T["cables"] - 0.1, "#E5E7EB", size=30)
        x2, y2 = self.at(-330, -180)
        self.label(x2, y2, 300, 430, "cables", T["cables"] + 0.3, s("break3") - 0.2, "#FDE047", size=30)
        self.badge("check", T["arm"], s("break3") - 0.15, x=880, y=560)

    # ------------------------------------------------------------------ set: backup power (break3, fix3)
    def draw_backup(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["backup"].at(t)
        dark = 0.0
        if t < s("fix3"):
            dark = bump(t, T["blinks"] - 0.05, T["blinks"] + 0.6) * 0.9
        else:                                                                        # the same blink, now caught by the batteries
            dark = bump(t, T["instant"] - 0.05, T["instant"] + 0.25) * 0.35
        self.interior(c, t, cam, lights=1 - dark)
        k = self.train.at(t)
        lost = T["hours"] - 0.2 <= t < s("fix3")
        box(c, -380, -520, 560, 300, "#0B1220", r=16)                                # the big screen
        c.drawRRect(rr(-360, -500, 520, 260, 10), P(mix("#0F172A", "#020617", dark)))
        word(c, self.L["train"], -100, -430, 44, mix("#E2E8F0", "#475569", dark))
        c.drawRRect(rr(-330, -390, 460, 40, 20), P("#1E293B"))
        c.drawRRect(rr(-330, -390, max(8.0, 460 * k), 40, 20), P(WARN if lost else GOOD))
        text(c, f"{int(round(k * 100))}%", -100, -290, 40, WARN if lost else "#E2E8F0", "Poppins-Black")
        for i in range(4):
            rack(c, -560 + i * 130, 0, t, on=1 - dark, w=100, h=200, seed=i)
        bk = prog(t, T["batt"] - 0.25, T["batt"] + 0.2)
        if bk > 0:
            for i in range(4):
                c.save()
                c.translate(240 + i * 130 + 60, 0)
                c.scale(e_back(bk), e_back(bk))
                c.translate(-(240 + i * 130 + 60), 0)
                battery(c, 240 + i * 130, 0, self.charge.at(t), t)
                c.restore()
        gk = prog(t, T["gens"] - 0.3, T["gens"])
        if gk > 0:
            run = prog(t, T["ten"] + 0.2, T["ten"] + 0.5)
            generator(c, 790, 0, t, run)
            generator(c, 1120, 0, t + 0.3, run)
        c.restore()
        self.ui["cam"] = cam

    def ui_backup(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3"):
            self.chip(540, 560, "lost", T["hours"], s("fix3") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["blinks"] + 0.3, s("fix3") - 0.2)
            self.red(T["blinks"] + 0.3, 2.0)
            return
        x0, y0 = self.at(430, -270)
        self.label(x0, y0, 300, 430, "batt", T["batt"] + 0.2, T["diesel"] - 0.1, GOOD)
        x1, y1 = self.at(950, -160)
        self.label(x1, y1, 760, 430, "gen", T["gens"] + 0.1, s("break4") - 0.2, "#F59E0B")
        self.chip(540, 560, "ten", T["ten"], s("break4") - 0.15, accent=HILITE, size=42)
        self.badge("check", T["ten"] + 0.5, s("break4") - 0.15, x=880, y=700)

    # ------------------------------------------------------------------ set: the door (break4, fix4)
    def draw_door(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["door"].at(t)
        self.interior(c, t, cam)
        unplugged = t >= T["trip"]
        for i in range(6):
            rack(c, -720 + i * 130, 0, t, on=0.0 if unplugged and t < s("fix4") else 1.0, w=110, h=330, seed=i)
        cable = skia.Path()                                                           # the most important cable
        cable.moveTo(-50, -60)
        end_x = -40 if not unplugged else 120
        cable.cubicTo(-30, 10, 60, 6, end_x, 4 if not unplugged else -30)
        cable.lineTo(600, 6)
        c.drawPath(cable, P("#FACC15", 1, stroke=12))
        if unplugged and t < s("fix4"):
            sparks_shower(c, -50, -60, t, T["trip"], 0.6, n=20, speed=380, seed=3)
        if t < s("fix4"):
            wx = self.walk.at(t)
            if t < T["trip"]:
                person(c, -wx, 0, 128, SHIRTS[2], t * 1.6, "walk", face=-1, skin=SKINS[0])
            else:
                c.save()
                c.translate(-wx, 0)
                c.rotate(-80 * e_out(prog(t, T["trip"], T["trip"] + 0.35)))
                person(c, 0, 0, 128, SHIRTS[2], t, "duck", face=-1, skin=SKINS[0])
                c.restore()
        else:
            fk = prog(t, T["fences"] - 0.2, T["fences"] + 0.3)
            fence(c, -900, 900, 120, 170, fk)
            for i, gx in enumerate((-430, 380)):
                gk = prog(t, T["guards"] - 0.15 + i * 0.1, T["guards"] + 0.2 + i * 0.1)
                if gk > 0:
                    person(c, gx, 0, 132, "#1E293B", t + i, "stand", face=1 if i else -1, hat="cap", skin=SKINS[3 - i], a=gk)
            camera(c, -620, -460, t, prog(t, T["cams"] - 0.15, T["cams"] + 0.2))
            camera(c, 560, -460, t + 1, prog(t, T["cams"] - 0.05, T["cams"] + 0.3))
            dk = prog(t, T["door"] - 0.2, T["door"] + 0.2)
            if dk > 0:                                                               # the face-scanning door
                sk = e_back(dk)
                c.save()
                c.translate(0, 0)
                c.scale(sk, sk)
                c.drawRRect(rr(-110, -330, 220, 330, 14), P("#BFE6FF", 0.18))
                c.drawRRect(rr(-110, -330, 220, 330, 14), P("#E0F2FE", 0.8, stroke=5))
                c.restore()
                scan = prog(t, T["scans"] - 0.1, T["scans"] + 0.6)
                person(c, 0, 0, 128, SHIRTS[0], t, "stand" if scan < 1 else "cheer", face=1, skin=SKINS[1])
                if 0 < scan < 1:
                    sy = lerp(-150, -110, (math.sin(t * 9) + 1) / 2)
                    c.drawLine(-60, sy, 60, sy, P(GOOD, 0.95, stroke=5))
                    add_glow(c, 0, sy, 80, GOOD, 0.6)
        c.restore()
        self.ui["cam"] = cam

    def ui_door(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4"):
            x0, y0 = self.at(200, 6)
            self.label(x0, y0, 760, 430, "cable", T["cable"] - 0.1, s("fix4") - 0.15, HILITE, size=30)
            self.badge("alert", T["trip"], s("fix4") - 0.2)
            self.red(T["trip"], 2.0)
            return
        self.chip(260, 430, "fence", T["fences"], T["door"] - 0.2, size=36)
        self.chip(540, 430, "guards", T["guards"], T["door"] - 0.2, size=36)
        self.chip(820, 430, "cams", T["cams"], T["door"] - 0.2, size=36)
        x0, y0 = self.at(0, -130)
        self.label(x0 + 50, y0, 780, 520, "scan", T["scans"] - 0.1, s("cta") - 0.1, GOOD)
        self.badge("check", T["face"] + 0.3, s("cta") - 0.05, x=880, y=700)

    # ------------------------------------------------------------------ set: the desert (cta, reveal, stat, closer)
    def draw_desert(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["desert"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, horizon_y=gy)
        v2.stars(c, W, H, t, 1.0)
        v2.moon(c, 230, gy - 900 * z - 60, 70)
        self.view(c, cam)
        for k, (yy, col) in enumerate(((0, "#7A5A3A"), (60, "#9A7448"), (160, SAND))):        # dunes
            p = skia.Path()
            p.moveTo(-6000, yy + 2000)
            for xx in range(-6000, 6001, 400):
                p.lineTo(xx, yy - 40 * math.sin(xx * 0.003 + k * 2))
            p.lineTo(6000, yy + 2000)
            p.close()
            c.drawPath(p, P(col))
        c.drawRect(R(-6000, 150, 12000, 26), P("#3F3F46"))                          # a lone road
        for xx in range(-6000, 6000, 180):
            c.drawRect(R(xx, 160, 80, 6), P("#FDE68A", 0.7))
        wall = self.wall.at(t)
        self.building(c, t, inside=1.0 - wall, x=-450, w=900, h=480)
        if wall > 0:                                                                 # the plain gray front, sliding in
            c.save()
            c.clipRect(R(-450, -480, 900, 480))
            c.drawRect(R(-450, -480 + 480 * (1 - wall), 900, 480), P(GRAY))
            c.drawRect(R(-450, -480 + 480 * (1 - wall), 900, 6), P("#A3ACBE"))
            c.restore()
        for i, fx in enumerate((-260, 0, 260)):
            box(c, fx - 110, -590, 220, 90, "#94A3B8", r=10)
            fan(c, fx, -635, 34, t, 1.6)
        c.restore()
        self.ui["cam"] = cam

    def ui_desert(self, c, t, tw):
        T, s = self.T, self.tl.s
        if s("reveal") <= tw < T["s1"] - 0.3:
            x0, y0 = self.at(300, -240)
            self.label(x0, y0, 780, 420, "box", T["box"] - 0.1, T["nowhere"] - 0.1, "#E5E7EB")
            self.chip(540, 560, "nowhere", T["nowhere"], T["s1"] - 0.35, accent=HILITE, size=40)

    # ------------------------------------------------------------------ set: the phone (tag)
    @staticmethod
    def text_w(s, size):
        return arabic.width_ar(s, size * 1.15, "Tajawal-Black") if arabic.is_ar(s) else text_width(s, size, "Poppins-Black")

    def draw_phone(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["phone"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B1C4A", "#0B0C24"]))
        self.view(c, cam)
        c.drawRRect(rr(-260, -600, 520, 760, 60), P("#0B1220"))                   # the phone
        c.drawRRect(rr(-236, -572, 472, 704, 44), P("#F8FAFC"))
        ask = prog(t, T["half"] - 0.2, T["half"] + 0.1)
        if ask > 0:                                                                  # bubbles sized to their text
            bw = self.text_w(self.L["ask"], 40) + 64
            c.drawRRect(rr(206 - bw, -440, bw, 96, 40), P("#2563EB", ask))
            word(c, self.L["ask"], 206 - bw / 2, -378, 40, "#FFFFFF", a=ask)
        if T["half"] + 0.3 <= t < T["name"]:
            for i in range(3):
                c.drawCircle(-170 + i * 26, -272, 10, P("#94A3B8", 0.5 + 0.5 * math.sin(t * 8 + i)))
        rep = prog(t, T["name"] - 0.05, T["name"] + 0.25)
        if rep > 0:
            bw = self.text_w(self.L["reply"], 40) + 64
            c.drawRRect(rr(-206, -320, bw, 96, 40), P("#475569", rep))
            word(c, self.L["reply"], -206 + bw / 2, -258, 40, "#FFFFFF", a=rep)
        ck = prog(t, T["cat"] - 0.2, T["cat"] + 0.2)                                # the cat
        if ck > 0:
            c.save()
            c.translate(250, 130)
            c.scale(0.8 * e_back(ck), 0.8 * e_back(ck))
            c.drawOval(R(-110, -60, 220, 140), P("#F59E0B"))
            c.drawCircle(0, -110, 80, P("#F59E0B"))
            for sd in (-1, 1):
                ear = skia.Path()
                ear.moveTo(sd * 30, -170)
                ear.lineTo(sd * 70, -230)
                ear.lineTo(sd * 80, -150)
                ear.close()
                c.drawPath(ear, P("#F59E0B"))
                c.drawCircle(sd * 30, -115, 10, P("#111827"))
            c.drawLine(-60, -90, -120, -100, P("#111827", 1, stroke=3))
            c.drawLine(60, -90, 120, -100, P("#111827", 1, stroke=3))
            c.restore()
        c.restore()
        self.ui["cam"] = cam

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["plug"] - 0.05, sfx.clank(700, 0.3, 61), -4), (T["plug"], sfx.sparkle(0.4, 5, 62), -8),
              (T["thousand"], hum_up(1.4), -10)]
        ev += [(T["thousand"] + 0.12 * i, sfx.pop(63 + i), -12) for i in range(9)]
        ev += [(T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 72), -9), (T["hot"], sfx.hum(2.4, 120), -12),
               (T["oven"], sfx.alarm(3, 820), -11), (T["shuts"], sfx.power_down(1.2, 73), -6)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["plates"] - 0.05, sfx.thud(0.4, 75), -4),
               (T["plates"] + 0.1, sfx.whirr(1.6, 140, 200, 76), -12), (T["coolers"] - 0.25, sfx.whoosh(0.4, False, 77), -6),
               (T["coolers"] + 0.2, sfx.whirr(1.8, 160, 260, 78), -10), (T["outside"] + 0.1, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 79), -4), (T["drinks"], hum_up(1.2, 80), -8),
               (T["flicker"], sfx.power_down(0.6, 81), -8), (T["flicker"] + 0.05, sfx.alarm(3, 820), -11)]
        ev += [(T["sub"] - 0.1, sfx.clank(300, 0.4, 82), -6), (T["trans"], sfx.thud(0.5, 83), -4), (T["trans"] + 0.12, sfx.thud(0.5, 84), -5),
               (T["trans"] + 0.24, sfx.thud(0.5, 85), -5), (T["cables"] + 0.3, sfx.hum(1.6, 60), -10), (T["arm"], sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 86), -4), (T["blinks"], sfx.power_down(0.6, 87), -4),
               (T["hours"], sfx.womp(), -6), (T["blinks"] + 0.3, sfx.alarm(3, 820), -11)]
        ev += [(T["batt"] - 0.2, sfx.clank(500, 0.3, 88), -6), (T["instant"], sfx.click(89), -5), (T["gens"] - 0.3, sfx.thud(0.5, 90), -4),
               (T["ten"] + 0.2, engine_snd(2.0), -6), (T["ten"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 91), -4), (T["walks"], sfx.creak(0.3, 92), -12), (T["trip"], sfx.thud(0.5, 93), -2),
               (T["trip"] + 0.02, sfx.power_down(1.0, 94), -6), (T["trip"] + 0.1, sfx.alarm(3, 820), -10)]
        ev += [(T["fences"], sfx.clank(800, 0.3, 95), -8), (T["guards"], sfx.pop(96), -8), (T["cams"], sfx.click(97), -6),
               (T["door"] - 0.1, sfx.whoosh(0.4, False, 98), -8), (T["scans"], sfx.beep(1400, 0.1), -8),
               (T["face"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(99), 0), (T["follow"] - 0.15, sfx.pop(100), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 101), -7)]
        ev += [(T["hide"], sfx.whoosh(0.8, False, 102), -7), (T["box"], sfx.thud(0.4, 103), -6), (T["nowhere"] - 0.3, sfx.whoosh(1.2, False, 104), -10)]
        ev += [(T["s1"], sfx.pop(105), -3), (T["s2"], sfx.pop(106), -3), (T["s3"], sfx.pop(107), -3)]
        ev += [(T["cong2"], sfx.pop(108), -2), (T["cong2"], sfx.sparkle(1.0, 14, 109), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 110), -6), (T["half"], sfx.pop(111), -8), (T["name"], sfx.ding(), -7),
               (T["cat"] + 0.2, sfx.womp(), -6)]
        return ev


NAME = "datacenter"
EPISODE = DataCenter
