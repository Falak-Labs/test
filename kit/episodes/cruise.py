"""Episode 21 - A cruise ship.  v2 look: the sea at dusk, six sets with whip cuts.

Sets: sea (a hotel lands on a small boat; the first big wave tips it over), hull (the ship seen from the bow, cut
open: a wide hull, the heavy stuff at the bottom, the rocking guests, the stabilizer fins), inside (cabins with
showers above, the water factory below), harbor (from above: no room to turn; pods and bow thrusters slide it
sideways onto the dock), wide (the finished ship from the side: twenty decks, pools, a water park, a theater), pier
(the tag: a late guest runs down the pier while the ship leaves).
Side views: the sea surface is y = 0, down is positive.  The harbor is seen from above (x right, y down the screen).
"""
from v2_base import *  # noqa: F401,F403

NAVY, WHITE, ORANGE, POOL = "#1D3B72", "#EEF2F8", "#F97316", "#38BDF8"
LIT, DARKWIN = "#FFE3A3", "#2E3858"
DECK_H = 17                                   # one deck of the finished ship (set "wide")
TOP0 = -150                                   # the hull's top edge in the side view
SKINS = ("#E8B48A", "#C68B5E", "#F1C9A5", "#8D5A3B", "#E0A47A")


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    """A word drawn into the world: Poppins for English, Tajawal for Arabic."""
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def along(pts, u):
    """Point at fraction u (0..1) of a polyline's length."""
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


def flow(c, pts, t, k, n=10, speed=0.45, col="#7DD3FC", r=6, salt=0.0, seed=1):
    """Drops running along a pipe. salt > 0: that share of them are white salt grains."""
    if k <= 0:
        return
    rng = random.Random(seed)
    for i in range(n):
        u = (t * speed + i / n + rng.uniform(0, 0.03)) % 1.0
        x, y = along(pts, u)
        is_salt = rng.random() < salt
        c.drawCircle(x, y, r * (0.75 if is_salt else 1.0), P("#F8FAFC" if is_salt else col, 0.95 * k))


def small_boat(c):
    p = skia.Path()
    p.moveTo(-212, -36)
    p.lineTo(216, -36)
    p.quadTo(198, 26, 132, 42)
    p.lineTo(-160, 42)
    p.quadTo(-214, 24, -212, -36)
    p.close()
    c.drawPath(p, lin_paint(0, -36, 0, 42, ["#F8FAFC", "#B8C3D6", "#5B6680"]))
    c.drawRect(R(-212, -36, 428, 9), P(ORANGE))
    c.drawPath(p, P("#0B1220", 0.45, stroke=3))


def hotel(c, t, sign, w=236, floors=6, sway=0.0):
    """A hotel block standing on y = 0, sign on the roof."""
    fh = 62
    h = floors * fh
    c.save()
    c.rotate(sway)
    box(c, -w / 2, -h, w, h, "#CDB9A2", r=6)
    for f in range(floors):
        y = -h + f * fh + 14
        for i in range(3):
            x = -w / 2 + 24 + i * (w - 88) / 2
            on = ((f * 7 + i * 3) % 4) != 0
            c.drawRRect(rr(x, y, 40, 34, 5), P("#F6C66B" if on else DARKWIN))
            c.drawRect(R(x, y + 15, 40, 3), P("#8E7A64"))
    c.drawRect(R(-w / 2 - 8, -h - 12, w + 16, 14), P("#8E7A64"))
    c.drawRRect(rr(-w / 2 + 26, -h - 78, w - 52, 58, 12), P("#1B1235"))
    add_glow(c, 0, -h - 48, 150, "#FF5EA8", 0.45 + 0.1 * math.sin(t * 6))
    word(c, sign, 0, -h - 34, 40, "#FF8AC2")
    c.restore()


def big_wave(c, x, h, t):
    """A wave rolling in from the right, its face to the left, crest at height h."""
    if h < 2:
        return
    c.save()
    c.translate(x, 0)
    c.scale(-1, 1)
    p = skia.Path()
    p.moveTo(-760, 6)
    p.cubicTo(-380, 6, -220, -h, 10, -h)
    p.cubicTo(120, -h, 170, -h * 0.82, 104, -h * 0.62)
    p.cubicTo(210, -h * 0.70, 330, -h * 0.25, 640, 6)
    p.lineTo(640, 260)
    p.lineTo(-760, 260)
    p.close()
    c.drawPath(p, lin_paint(0, -h, 0, 160, ["#3B82C4", "#15407E", "#0B2149"]))
    crest = skia.Path()
    crest.moveTo(-380, -h * 0.30)
    crest.cubicTo(-220, -h * 0.9, -60, -h, 10, -h)
    crest.cubicTo(120, -h, 170, -h * 0.82, 104, -h * 0.62)
    c.drawPath(crest, P("#EAF6FF", 0.9, stroke=12))
    for i in range(16):
        sx = -50 + i * 12 + math.sin(t * 8 + i) * 6
        c.drawCircle(sx, -h - 10 - (i % 4) * 9 + math.sin(t * 9 + i) * 5, 5 + (i % 3) * 2, P("#EAF6FF", 0.7))
    c.restore()


def towel_person(c, x, y, h, t, pose="stand", skin=SKINS[0], face=1, a=1.0):
    """Somebody in a bath towel."""
    person(c, x, y, h, skin, t, pose, face=face, skin=skin, pants=skin, a=a)
    u = h / 140.0
    c.drawRRect(rr(x - 22 * u, y - 62 * u, 44 * u, 34 * u, 8 * u), P("#F8FAFC", a))
    c.drawLine(x - 22 * u, y - 50 * u, x + 22 * u, y - 50 * u, P("#93C5FD", 0.8 * a, stroke=3 * u))


def phone(c, x, y, k, t):
    c.drawRRect(rr(x - 7, y - 12, 14, 24, 3), P("#0B1220"))
    c.drawRRect(rr(x - 5, y - 10, 10, 18, 2), P("#BFE3FF", 0.9))
    if k > 0:
        add_glow(c, x, y, 44, "#FFFFFF", 0.7 * k)


def horn_snd(d=1.8):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.zeros(n)
    for f, g in ((92.0, 1.0), (138.0, 0.7), (184.0, 0.35)):
        ph = 2 * np.pi * f * tt
        x += g * (2 * ((ph / (2 * np.pi)) % 1.0) - 1)
    x = sfx._lp(x, 900)
    return sfx._norm(x * sfx._ar(n, 0.08, 0.35), 0.75)


def water_snd(d=0.7, seed=60):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 400, 5200)
    return sfx._norm(x * sfx._env(n, 0.004, d * 0.3), 0.8)


def wave_snd(d=1.6, seed=61):
    n = int(d * sfx.SR)
    x = sfx._lp(sfx._rng(seed).standard_normal(n), 900) + 0.3 * sfx._bp(sfx._rng(seed + 1).standard_normal(n), 800, 4000)
    return sfx._norm(x * sfx._ar(n, d * 0.45, d * 0.5), 0.85)


def shower_snd(d=1.4, seed=62):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 2000, 9000)
    return sfx._norm(x * sfx._ar(n, 0.05, 0.25), 0.4)


# ====================================================================================== the episode
class Cruise(EpisodeV2):
    BUILD_NO = 21
    FIRST_SET = "sea"
    CLEAR = "#06102A"
    TITLE = {"en": "CRUISE SHIP", "ar_sa": "سفينة سياحية"}
    EMPH = {"en": ["CONGRATS", "CRUISE", "SHIP", "HOTEL", "TIPS", "OVER", "HULL", "WIDE", "HEAVIEST", "BOTTOM", "ROLLS",
                   "ROCKS", "GREEN", "STABILIZER", "FINS", "NINETY", "SHOWERS", "WEEK", "FACTORY", "FILTERS", "ONLY",
                   "HARBOR", "TURN", "PODS", "THRUSTERS", "SIDEWAYS", "FOLLOW", "TWENTY", "POOLS", "THEATER", "SEVEN",
                   "ZERO", "YOURSELF", "LATE", "LEAVES", "VIDEOS", "THOUSANDS"],
            "ar_sa": ["مبروك", "سفينة", "فندق", "تقلبه", "عريض", "الثقيلة", "تعتدل", "تهزّها", "يدوخون", "زعانف", "تسعين",
                      "يتروشون", "أسبوع", "مصنع", "فلاتر", "ميناء", "تلف", "قواعد", "جانبية", "فتنزلق", "تابعني", "عشرين",
                      "مسابح", "ومسرح", "سبعة", "وصفر", "بيدك", "تأخرت", "تمشي", "مقاطع", "بالآلاف"]}
    KEYS = {"ar_sa": {
        ("hook", "HOTEL"): "فندق", ("hook", "BOAT"): "قارب", ("hook", "CONGRATS"): "مبروك", ("hook", "CRUISE"): "سفينة",
        ("break1", "TALL"): "طويل", ("break1", "WAVE"): "موجة", ("break1", "TIPS"): "تقلبه", ("break1", "OVER"): "جنبه",
        ("fix1", "HULL"): "جسم", ("fix1", "WIDE"): "عريض", ("fix1", "HEAVIEST"): "الثقيلة", ("fix1", "BOTTOM"): "خالص",
        ("fix1", "ENGINES"): "المكاين", ("fix1", "FUEL"): "والوقود", ("fix1", "WATER"): "والموية", ("fix1", "ROLLS"): "تعتدل",
        ("break2", "STAYS"): "تنقلب", ("break2", "ROCKS"): "تهزّها", ("break2", "THOUSAND"): "آلاف", ("break2", "GREEN"): "يدوخون",
        ("break2", "BUFFET"): "البوفيه",
        ("fix2", "STABILIZER"): "زعانف", ("fix2", "WINGS"): "جناحين", ("fix2", "TILT"): "يميلون", ("fix2", "NINETY"): "تسعين",
        ("break3", "SEVEN"): "سبعة", ("break3", "SHOWERS"): "يتروشون", ("break3", "TAP"): "حنفية", ("break3", "WEEK"): "أسبوع",
        ("fix3", "FACTORY"): "مصنع", ("fix3", "SQUEEZES"): "يعصر", ("fix3", "FILTERS"): "فلاتر", ("fix3", "ONLY"): "إلا",
        ("break4", "FLOATING"): "عايمة", ("break4", "PARK"): "توقفها", ("break4", "HARBOR"): "ميناء", ("break4", "TURN"): "تلف",
        ("fix4", "PODS"): "قواعد", ("fix4", "SPIN"): "دورة", ("fix4", "THRUSTERS"): "جانبية", ("fix4", "SIDEWAYS"): "فتنزلق",
        ("fix4", "DOCK"): "الرصيف",
        ("cta", "PORT"): "الميناء", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "STACK"): "ركّب", ("reveal", "TWENTY"): "عشرين", ("reveal", "POOLS"): "مسابح", ("reveal", "PARK"): "ألعاب",
        ("reveal", "THEATER"): "ومسرح",
        ("stat", "TWENTY"): "عشرين", ("stat", "SEVEN"): "سبعة", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "LATE"): "تأخرت", ("tag", "LEAVES"): "تمشي", ("tag", "VIDEOS"): "مقاطع", ("tag", "THOUSANDS"): "بالآلاف"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an AI data center"),
                   "stat": [("20", "DECKS"), ("7,000", "GUESTS"), ("0", "PARKING")],
                   "L": {"hotel": "HOTEL", "ship": "YOUR CRUISE SHIP", "wide": "WIDE HULL", "g": "CENTER OF GRAVITY",
                         "engines": "ENGINES", "fuel": "FUEL", "water": "WATER", "roll": "ROLLING", "fins": "STABILIZER FINS",
                         "m90": "-90% ROCKING", "people": "7,000 PEOPLE", "tank": "FRESH WATER", "week": "NEAREST TAP: 1 WEEK", "factory": "WATER FACTORY",
                         "filter": "FILTER", "salt": "SALT STAYS OUT", "circle": "TURNING CIRCLE", "pods": "PODS SPIN 360°",
                         "thr": "BOW THRUSTERS", "decks": "20 DECKS", "pools": "POOLS", "wpark": "WATER PARK",
                         "theater": "THEATER", "videos": "1000s OF VIDEOS"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مركز بيانات"),
                      "stat": [("20", "دور"), ("7000", "راكب"), ("0", "مواقف")],
                      "L": {"hotel": "فندق", "ship": "سفينتك السياحية", "wide": "جسم عريض", "g": "مركز الثقل",
                            "engines": "مكاين", "fuel": "وقود", "water": "موية", "roll": "التمايل", "fins": "زعانف تثبيت",
                            "m90": "-90% تمايل", "people": "7000 شخص", "tank": "موية حلوة", "week": "أقرب حنفية: أسبوع", "factory": "مصنع موية",
                            "filter": "فلتر", "salt": "الملح يبقى برّا", "circle": "دايرة اللف", "pods": "تلف 360°",
                            "thr": "مراوح جانبية", "decks": "20 دور", "pools": "مسابح", "wpark": "ألعاب مائية",
                            "theater": "مسرح", "videos": "مقاطع بالآلاف"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "hotel": ("hook", "HOTEL", 0.2), "boat": ("hook", "BOAT", 0.35), "congrats": ("hook", "CONGRATS", 0.55),
            "cruise": ("hook", "CRUISE", 0.85),
            "tall": ("break1", "TALL", 0.3), "wave": ("break1", "WAVE", 0.6), "tips": ("break1", "TIPS", 0.75),
            "over": ("break1", "OVER", 0.9),
            "hull": ("fix1", "HULL", 0.1), "wide": ("fix1", "WIDE", 0.17), "heavy": ("fix1", "HEAVIEST", 0.3),
            "bottom": ("fix1", "BOTTOM", 0.45), "engines": ("fix1", "ENGINES", 0.55), "fuel": ("fix1", "FUEL", 0.65),
            "water": ("fix1", "WATER", 0.72), "rolls": ("fix1", "ROLLS", 0.9),
            "stays": ("break2", "STAYS", 0.12), "rocks": ("break2", "ROCKS", 0.35), "thousand": ("break2", "THOUSAND", 0.55),
            "green": ("break2", "GREEN", 0.8), "buffet": ("break2", "BUFFET", 0.92),
            "fins": ("fix2", "STABILIZER", 0.12), "wings": ("fix2", "WINGS", 0.3), "tilt": ("fix2", "TILT", 0.55),
            "ninety": ("fix2", "NINETY", 0.85),
            "seven": ("break3", "SEVEN", 0.12), "showers": ("break3", "SHOWERS", 0.4), "tap": ("break3", "TAP", 0.72),
            "week": ("break3", "WEEK", 0.88),
            "factory": ("fix3", "FACTORY", 0.2), "squeeze": ("fix3", "SQUEEZES", 0.4), "filters": ("fix3", "FILTERS", 0.62),
            "only": ("fix3", "ONLY", 0.82),
            "city": ("break4", "FLOATING", 0.2), "park": ("break4", "PARK", 0.5), "harbor": ("break4", "HARBOR", 0.7),
            "turn": ("break4", "TURN", 0.92),
            "pods": ("fix4", "PODS", 0.15), "spin": ("fix4", "SPIN", 0.3), "thrusters": ("fix4", "THRUSTERS", 0.6),
            "sideways": ("fix4", "SIDEWAYS", 0.85), "dock": ("fix4", "DOCK", 0.95),
            "port": ("cta", "PORT", 0.25), "follow": ("cta", "FOLLOW", 0.4),
            "stack": ("reveal", "STACK", 0.15), "decks20": ("reveal", "TWENTY", 0.3), "pools": ("reveal", "POOLS", 0.6),
            "wpark": ("reveal", "PARK", 0.78), "theater": ("reveal", "THEATER", 0.92),
            "s1": ("stat", "TWENTY", 0.04), "s2": ("stat", "SEVEN", 0.38), "s3": ("stat", "ZERO", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "late": ("tag", "LATE", 0.15), "leaves": ("tag", "LEAVES", 0.38), "videos": ("tag", "VIDEOS", 0.65),
            "thousands": ("tag", "THOUSANDS", 0.85)})
        T["land"] = max(T["boat"], 0.9)                               # the hotel lands on the boat
        T["capsize"] = T["tips"] - 0.15
        T["push"] = max(T["water"] + 0.45, T["rolls"] - 0.9)          # the wave that the wide hull shrugs off
        T["bump"] = T["turn"] + 0.1
        # ---- sets
        self.cut(s("fix1") - 0.12, "hull", 1)
        self.cut(s("break3") - 0.12, "inside", 1)
        self.cut(s("break4") - 0.12, "harbor", -1)
        self.cut(s("cta") + 0.05, "wide", -1)
        self.cut(s("tag") - 0.2, "pier", 1)
        self.cams = {"sea": Camera(30, -150, 1.32), "hull": Camera(0, -120, 1.22), "inside": Camera(0, -70, 1.12),
                     "harbor": Camera(-300, -130, 0.84), "wide": Camera(0, -330, 0.72), "pier": Camera(-120, -250, 1.08)}
        cm = self.cams
        cm["sea"].key(0.05, 20, -170, 1.22, 1.0).key(T["tall"] - 0.3, 110, -230, 0.98, 0.9)
        cm["sea"].key(T["over"], 40, -170, 1.05, 0.8)
        cm["hull"].key(T["heavy"] - 0.2, 0, -60, 1.3, 0.8).key(T["push"] - 0.2, 0, -120, 1.22, 0.7)
        cm["hull"].key(s("break2") - 0.1, 0, -130, 1.18, 0.6).key(T["green"] - 0.4, -40, -150, 1.5, 0.7)
        cm["hull"].key(s("fix2") - 0.1, 0, -20, 1.12, 0.7)
        cm["inside"].key(s("break3") + 0.3, 0, -150, 1.25, 1.0).key(T["factory"] - 0.4, 0, 0, 1.22, 0.8)
        cm["inside"].key(T["only"] + 0.2, 0, -70, 1.12, 0.9)
        cm["harbor"].key(s("break4") + 0.2, 150, -110, 0.9, 1.6).key(s("fix4") - 0.1, 170, -100, 0.92, 0.8)
        cm["harbor"].key(T["sideways"] - 0.3, 170, -200, 0.92, 1.2)
        cm["wide"].key(s("reveal") - 0.1, 0, -330, 0.7, 1.3).key(T["s1"] - 0.3, 0, -200, 0.4, 1.0)
        cm["wide"].key(s("closer") - 0.2, 0, -300, 0.72, 0.9)
        cm["pier"].key(s("tag") - 0.2, -150, -250, 1.08, 0.0).key(T["leaves"] - 0.3, 210, -290, 0.95, 1.7)
        # ---- tracks
        self.drop = Track(-1300.0).to(0.1, 0.0, max(0.5, T["land"] - 0.1), e_in)
        self.capsize = Track(0.0).to(T["capsize"], -96.0, max(0.5, T["over"] - T["capsize"] + 0.35), e_in)
        self.wavex = Track(1500.0).to(T["wave"] - 0.6, -60.0, max(0.8, T["capsize"] - T["wave"] + 0.75), e_in)
        self.waveh = Track(0.0).to(T["wave"] - 0.6, 560.0, 0.6, e_out)
        self.hb = Track(150.0).to(T["wide"] - 0.05, 320.0, 0.55, e_back)
        self.gy = Track(-210.0).to(T["engines"] + 0.2, -90.0, 0.4).to(T["fuel"] + 0.2, -10.0, 0.4).to(T["water"] + 0.2, 70.0, 0.4)
        self.fin = Track(0.0).to(T["fins"] - 0.05, 1.0, 0.45, e_back)
        self.tank = Track(0.65).to(T["seven"], 0.03, max(0.6, T["tap"] - T["seven"]))
        self.tank.to(T["only"], 0.9, max(0.8, e("fix3") - T["only"]))
        self.sx = Track(-1150.0).to(s("break4") - 0.1, 168.0, max(1.0, T["bump"] - s("break4") + 0.1), e_out)
        self.sy = Track(30.0).to(T["sideways"] - 0.2, -228.0, max(0.9, T["dock"] - T["sideways"] + 0.6), e_io)
        self.decks = Track(5.0).to(T["stack"], 20.0, max(0.8, T["decks20"] - T["stack"] + 0.7))
        self.spans = [(T["tips"], T["rolls"] + 0.3), (T["rocks"], T["ninety"] + 0.3), (T["tap"], T["only"] + 0.4),
                      (T["turn"], T["dock"] + 0.2)]
        self.shakes = [(T["land"], 0.4, 12), (T["capsize"] + 0.35, 0.5, 16), (T["engines"] + 0.25, 0.25, 9),
                       (T["fuel"] + 0.25, 0.25, 9), (T["water"] + 0.25, 0.25, 9), (T["bump"], 0.6, 24),
                       (T["dock"], 0.3, 8), (s("closer") + 0.2, 0.35, 10)]

    # ------------------------------------------------------------------ shared drawing
    def surface_y(self, cam):
        cx, cy, z = cam
        return (0 - cy) * z + H / 2

    def sea_back(self, c, t, cam, moon=True):
        """Sky (screen space) and the sea body (world space; call inside view())."""
        cx, cy, z = cam
        self.backdrop(c, t, cx, cy, self.surface_y(cam), sea_=True, moon=moon)

    def sea_world(self, c, t, cam, moon_x=None):
        cx, cy, z = cam
        sea(c, cx - 640 / z, cx + 640 / z, t, moon_x=moon_x)

    def veil(self, c, t, cam, a=0.55):
        """The sea's surface in front of hulls: a translucent veil and three wave lines."""
        cx, cy, z = cam
        x0, x1 = cx - 640 / z, cx + 640 / z
        c.drawRect(R(x0, 0, x1 - x0, 3000), P("#0E2A5C", a))
        for k in range(3):
            path = skia.Path()
            xx = x0
            path.moveTo(xx, k * 12)
            while xx < x1:
                xx += 36
                path.lineTo(xx, k * 12 + math.sin(xx * 0.012 + t * (1.2 + k * 0.3) + k) * (4 + k))
            c.drawPath(path, P("#D6EEFF", 0.6 - k * 0.18, stroke=3.5 - k * 0.5))

    def guests(self, c, t, xs, y, h, pose, green=0.0):
        for i, x in enumerate(xs):
            skin = mix(SKINS[i % len(SKINS)], "#7CC24B", 0.85 * green)
            person(c, x, y, h, SHIRTS[i % len(SHIRTS)], t + i * 0.4, pose, face=1 if i % 2 else -1, skin=skin)

    # ------------------------------------------------------------------ set: the sea (hook, break1)
    def draw_sea(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["sea"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        self.sea_back(c, t, cam)
        self.view(c, cam)
        self.sea_world(c, t, cam, moon_x=-380)
        big_wave(c, self.wavex.at(t), self.waveh.at(t) * (1 - prog(t, T["over"] + 0.2, T["over"] + 1.2)), t)
        bob = math.sin(t * 1.7) * 5
        land = t - T["land"]
        dip = 26 * math.exp(-land * 4) * math.cos(land * 10) if land > 0 else 0.0
        rot = self.capsize.at(t)
        sink = 70 * e_in(prog(t, T["over"], T["over"] + 1.2))
        sway = math.sin(t * 5) * 2.5 * prog(t, T["tall"] - 0.2, T["tall"] + 0.2) * (1 - prog(t, T["capsize"], T["capsize"] + 0.2))
        c.save()
        c.translate(0, bob + dip + sink)
        c.rotate(rot)
        small_boat(c)
        c.save()
        c.translate(0, -36 + min(0.0, self.drop.at(t)))
        hotel(c, t, self.L["hotel"], sway=sway)
        c.restore()
        c.restore()
        self.veil(c, t, cam, 0.5)
        splash(c, 0, 0, t, T["land"], 0.9, n=26, speed=620, width=1.6)
        splash(c, -160, 0, t, T["capsize"] + 0.45, 1.1, n=36, speed=820, width=2.2, seed=9)
        if t >= T["over"]:
            bubbles(c, -120, 40, t, T["over"], T["over"] + 1.6, rate=18, life=1.4, spread=160, rise=200, seed=5)
        c.restore()
        self.ui["cam"] = cam
        self.ui["boat"] = (0, bob + dip)

    def ui_sea(self, c, t, tw):
        T, s = self.T, self.tl.s
        bx, by = self.ui.get("boat", (0, 0))
        px, py = self.at(170, by - 20)
        self.label(px, py, 820, 470, "ship", T["cruise"] - 0.15, s("break1") + 0.3, HILITE)
        self.badge("alert", T["tips"], s("fix1") - 0.2)
        self.red(T["tips"], 2.0)

    # ------------------------------------------------------------------ set: the hull from the bow (fix1, break2, fix2)
    def roll(self, t):
        T, s = self.T, self.tl.s
        if t < s("break2") - 0.12:
            if t < T["push"]:
                return math.sin(t * 2.1) * 3.0 * (1 - prog(t, T["wide"], T["wide"] + 0.4))
            u = t - T["push"]
            return -28 * math.sin(u * 4.4) * math.exp(-u * 1.5)
        amp = 13.0 * prog(t, s("break2"), T["rocks"] + 0.2)
        amp *= 1 - 0.9 * e_out(prog(t, T["tilt"], T["ninety"] + 0.3))
        return amp * math.sin((t - s("break2")) * 2.5)

    def ship_front(self, c, t, hb, decks=5):
        """The ship seen from the bow, cut open. Waterline y = 0, main deck y = -60, keel y = 150."""
        T = self.T
        sw = max(118.0, hb - 34)
        for d in range(decks):                                                   # superstructure, deck by deck
            y0 = -60 - (d + 1) * 64
            w2 = sw - d * 7
            box(c, -w2, y0, 2 * w2, 64, WHITE, r=4)
            for k in range(int((2 * w2 - 24) // 44)):
                wx = -w2 + 16 + k * 44
                c.drawRRect(rr(wx, y0 + 20, 26, 22, 4), P(LIT if (k + d) % 3 else DARKWIN))
            c.drawRect(R(-w2, y0 + 56, 2 * w2, 6), P("#9AA6BF"))
        c.drawRRect(rr(-30, -60 - decks * 64 - 70, 60, 74, 10), P("#C2410C"))          # funnel
        c.drawRect(R(-30, -60 - decks * 64 - 52, 60, 12), P(NAVY))
        hull = skia.Path()
        hull.moveTo(-hb, -60)
        hull.lineTo(hb, -60)
        hull.lineTo(hb, 66)
        hull.quadTo(hb - 4, 150, hb - 110, 150)
        hull.lineTo(-hb + 110, 150)
        hull.quadTo(-hb + 4, 150, -hb, 66)
        hull.close()
        c.drawPath(hull, lin_paint(-hb, 0, hb, 0, [shade(NAVY, -0.35), NAVY, shade(NAVY, 0.18), NAVY, shade(NAVY, -0.35)]))
        inner = skia.Path()
        inner.addRRect(rr(-hb + 16, -46, 2 * hb - 32, 180, 60))
        c.save()
        c.clipPath(inner, skia.ClipOp.kIntersect, True)
        vrect(c, -hb, -60, 2 * hb, 220, ["#2B3755", "#1A2238", "#10162A"])
        for fx in range(int(-hb + 40), int(hb - 30), 46):
            c.drawRect(R(fx, -46, 5, 190), P("#FFFFFF", 0.05))
        c.drawRect(R(-hb, 4, 2 * hb, 4), P("#7C8499", 0.5))
        c.restore()
        c.drawPath(hull, P("#F1F5F9", 0.85, stroke=3))
        c.drawRect(R(-hb - 2, -66, 2 * hb + 4, 8), P(WHITE))
        # buffet on the first deck
        c.drawRRect(rr(-70, -84, 140, 14, 4), P("#F8FAFC"))
        for i, fx in enumerate((-50, -16, 18, 50)):
            c.drawOval(R(fx - 12, -94, 24, 10), P(("#F59E0B", "#EF4444", "#22C55E", "#F472B6")[i]))

    def draw_hull(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["hull"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        self.sea_back(c, t, cam, moon=False)
        self.view(c, cam)
        self.sea_world(c, t, cam)
        hb = self.hb.at(t)
        th = self.roll(t)
        green = prog(t, T["green"] - 0.2, T["green"] + 0.3) * (1 - prog(t, T["ninety"], T["ninety"] + 1.0))
        c.save()
        c.translate(0, 30)
        c.rotate(th)
        c.translate(0, -30)
        fin = self.fin.at(t)
        if fin > 0:                                                              # stabilizer fins under the water
            for sd in (-1, 1):
                c.save()
                c.translate(sd * hb, 92)
                c.rotate(-sd * clamp(th * 1.7, -32, 32) * prog(t, T["tilt"] - 0.3, T["tilt"]))
                ln = 200 * fin
                c.drawRRect(rr(0 if sd > 0 else -ln, -18, ln, 36, 18), lin_paint(0, -18, 0, 18, ["#FDBA74", ORANGE, "#9A3412"]))
                c.drawRRect(rr(0 if sd > 0 else -ln, -18, ln, 36, 18), P("#FFFFFF", 0.7, stroke=3))
                if t >= T["wings"]:
                    add_glow(c, sd * ln * 0.5, 0, 90, ORANGE, 0.35 * (0.6 + 0.4 * math.sin(t * 6)))
                c.restore()
        self.ship_front(c, t, hb)
        # the heavy stuff, dropped in from above
        for key, x, w, h, col, lab in (("engines", 0, 150, 70, "#64748B", "engines"), ("fuel", -0.62, 110, 62, ORANGE, "fuel"),
                                       ("water", 0.62, 110, 62, "#0EA5E9", "water")):
            t0 = T[key] - 0.15
            if t < t0:
                continue
            u = prog(t, t0, t0 + 0.4)
            bx = x * hb if key != "engines" else 0
            by = lerp(-560, 132 - h, e_in(u)) - (8 * math.sin((t - t0 - 0.4) * 18) * math.exp(-(t - t0 - 0.4) * 6) if u >= 1 else 0)
            box(c, bx - w / 2, by, w, h, col, r=8)
            if key == "engines":
                for k in range(3):
                    c.drawCircle(bx - 44 + k * 44, by + 22, 12, P("#334155"))
            word(c, self.L[lab], bx, by + h / 2 + 10, 24, "#FFFFFF")
        # centre of gravity
        if t >= T["heavy"] - 0.4:
            gy = self.gy.at(t)
            a = prog(t, T["heavy"] - 0.4, T["heavy"])
            c.drawCircle(0, gy, 22, P("#FFFFFF", a))
            c.drawArc(R(-22, gy - 22, 44, 44), 0, 90, True, P("#111827", a))
            c.drawArc(R(-22, gy - 22, 44, 44), 180, 90, True, P("#111827", a))
            c.drawCircle(0, gy, 22, P("#111827", a, stroke=3))
            self.ui["g"] = gy
        # guests at the buffet
        pose = "duck" if T["green"] - 0.2 <= t < T["ninety"] else "cheer" if t >= T["ninety"] + 0.3 else "stand"
        self.guests(c, t, (-126, -98, 98, 126), -60, 58, pose, green)
        c.restore()
        self.veil(c, t, cam, 0.5)
        if t >= T["push"] - 0.4 and t < s("break2"):
            splash(c, -hb - 40, 0, t, T["push"] - 0.05, 0.8, n=18, speed=460, seed=13)
        c.restore()
        self.ui["cam"] = cam
        self.ui["hb"] = hb
        self.ui["th"] = th

    def ui_hull(self, c, t, tw):
        T, s = self.T, self.tl.s
        hb = self.ui.get("hb", 300)
        if tw < s("break2") - 0.12:
            x0, y0 = self.at(hb - 8, 40)
            self.label(x0, y0, 820, 440, "wide", T["wide"] + 0.25, T["heavy"] - 0.1, HILITE)
            if "g" in self.ui:
                gx, gyy = self.at(28, self.ui["g"])
                self.label(gx, gyy, 280, 440, "g", T["water"] + 0.3, s("break2") - 0.3, "#E5E7EB", size=30)
            self.badge("check", T["rolls"] + 0.35, s("break2") - 0.15)
            return
        p = self.span(s("break2") + 0.2, self.tl.e("fix2") + 0.6)
        if p > 0:
            k = clamp(abs(self.roll(tw)) / 14.0)
            v2.gauge(c, 60, 300, [(self.L["roll"], k, mix(GOOD, WARN, k))], p, w=320)
        if tw < s("fix2"):
            self.badge("alert", T["rocks"], s("fix2") - 0.2)
            self.red(T["green"] - 0.2, 2.0)
        else:
            x1, y1 = self.at(-hb - 120, 92)
            self.label(x1, y1, 300, min(1200, y1 + 150), "fins", T["fins"] + 0.3, T["ninety"] - 0.2, ORANGE)
            self.chip(760, 560, "m90", T["ninety"] + 0.1, self.tl.e("fix2") + 0.5, accent=GOOD, size=40)
            self.badge("check", T["ninety"] + 0.3, s("break3") - 0.15, x=230, y=470)

    # ------------------------------------------------------------------ set: inside (break3, fix3)
    PIPE_IN = [(-520, 110), (-330, 110)]
    PIPE_MEM = [(-330, 110), (-280, 110), (-280, 40), (-220, 40)]
    PIPE_OUT = [(170, 40), (230, 40), (230, -60), (270, -60)]
    PIPE_BRINE = [(170, 52), (210, 52), (210, 120), (520, 120)]
    PIPE_UP = [(410, -60), (440, -60), (440, -326), (-380, -326)]

    def draw_inside(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["inside"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        self.sea_back(c, t, cam, moon=False)
        self.view(c, cam)
        self.sea_world(c, t, cam)
        # the cut-open slice of the ship
        box(c, -470, -350, 940, 520, "#3A4566", r=10)
        vrect(c, -456, -336, 912, 200, ["#4A5578", "#3B4565"])                     # cabin deck
        vrect(c, -456, -122, 912, 280, ["#27304A", "#1B2338"])                     # the deck below: the factory
        c.drawRect(R(-470, -136, 940, 14), P("#9AA6BF"))
        for wx in (-160, 160):
            c.drawRect(R(wx - 5, -336, 10, 200), P("#2B3352"))
        tank = self.tank.at(t)
        showers_on = (t < T["tap"]) or (t >= T["only"] + 0.4)
        drip = T["tap"] <= t < T["only"] + 0.4
        for i, cx_ in enumerate((-310, 0, 310)):                                    # three cabins, three showers
            c.drawCircle(cx_ - 90, -260, 22, P("#0B1630"))
            c.drawCircle(cx_ - 90, -260, 22, P("#9AA6BF", 1, stroke=5))
            add_glow(c, cx_ - 90, -260, 30, "#9DB7FF", 0.25)
            gx = cx_ + 18
            c.drawRRect(rr(gx, -320, 104, 180, 8), P("#BFE6FF", 0.16))
            c.drawRRect(rr(gx, -320, 104, 180, 8), P("#E0F2FE", 0.6, stroke=3))
            c.drawRect(R(gx + 44, -322, 16, 10), P("#CBD5E1"))
            c.drawRRect(rr(gx + 32, -314, 40, 10, 5), P("#E2E8F0"))
            if showers_on:
                for k in range(9):
                    yy = -300 + ((t * 420 + k * 23) % 150)
                    c.drawLine(gx + 36 + k * 4, yy, gx + 36 + k * 4, yy + 14, P("#7DD3FC", 0.8, stroke=2.5))
            elif drip:
                yy = -300 + ((t * 260) % 140)
                c.drawCircle(gx + 52, yy, 4, P("#7DD3FC", 0.9))
            pose = "cheer" if t >= T["only"] + 0.4 else "shrug" if t >= T["tap"] else "stand"
            towel_person(c, gx + 52, -140, 112, t + i * 0.5, pose, SKINS[i], face=-1 if i % 2 else 1)
            if drip:
                text(c, "?", gx + 52, -284 - 6 * math.sin(t * 5 + i), 40, HILITE, "Poppins-Black")
        # the water factory
        fk = prog(t, T["factory"] - 0.2, T["factory"] + 0.3)
        sk = fk * (1 if t >= T["squeeze"] - 0.1 else 0)
        box(c, 270, -110, 140, 150, "#64748B", r=12)                                  # fresh water tank
        c.save()
        c.clipRRect(rr(282, -98, 116, 126, 8), skia.ClipOp.kIntersect, True)
        c.drawRect(R(282, -98, 116, 126), P("#0B1220"))
        hgt = 126 * clamp(tank)
        vrect(c, 282, 28 - hgt, 116, hgt + 1, ["#38BDF8", "#0369A1"])
        c.drawRect(R(282, 28 - hgt, 116, 3), P("#E0F7FF", 0.9))
        c.restore()
        pipe(c, self.PIPE_UP, "#94A3B8", 16)
        flow(c, self.PIPE_UP, t, 1.0 if showers_on else 0.0, n=14, speed=0.35, r=5, seed=7)
        if fk > 0:
            c.save()
            c.translate(-30, 60)
            c.scale(e_back(fk), e_back(fk))
            c.translate(30, -60)
            pipe(c, self.PIPE_IN, "#64748B")
            pipe(c, self.PIPE_MEM, "#64748B")
            pipe(c, self.PIPE_OUT, "#38BDF8", 18)
            pipe(c, self.PIPE_BRINE, "#94A3B8", 18)
            cyl(c, -360, 70, 70, 80, "#1D4ED8", r=10)                                 # the pump
            for b in range(3):
                ang = t * 14 * sk + b * 2.09
                c.drawLine(-325, 110, -325 + math.cos(ang) * 22, 110 + math.sin(ang) * 22, P("#E0F2FE", 0.9, stroke=5))
            hi = prog(t, T["filters"] - 0.2, T["filters"] + 0.2)
            cyl(c, -220, 12, 390, 56, mix("#94A3B8", "#E2E8F0", hi), r=26)            # the membrane tube
            for k in range(14):
                c.drawLine(-200 + k * 26, 18, -200 + k * 26, 62, P("#334155", 0.8, stroke=3))
            c.drawLine(-210, 40, 160, 40, P("#F8FAFC", 0.5 + 0.4 * hi, stroke=2))
            if hi > 0:
                add_glow(c, -25, 40, 240, "#A5F3FC", 0.35 * hi)
            c.restore()
            flow(c, self.PIPE_IN + self.PIPE_MEM[1:], t, sk, n=16, speed=0.55, col="#2563EB", r=7, salt=0.45, seed=3)
            only = t >= T["only"] - 0.2
            for k in range(12):                                                       # through the membrane
                u = (t * 0.5 + k / 12) % 1.0
                x = -210 + 370 * u
                if only:
                    c.drawCircle(x, 30 + (k % 3) * 8, 6, P("#7DD3FC", sk))
                    c.drawCircle(x - 10, 50 - (k % 2) * 6, 4.5, P("#F8FAFC", sk))
                else:
                    c.drawCircle(x, 40 + math.sin(k) * 10, 6, P("#2563EB", sk))
            flow(c, self.PIPE_OUT, t, sk * (1 if only else 0.4), n=8, speed=0.5, r=6, seed=4)
            flow(c, self.PIPE_BRINE, t, sk, n=12, speed=0.5, col="#93A3B8", r=5, salt=0.8, seed=5)
        c.restore()
        self.ui["cam"] = cam

    def ui_inside(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3"):
            p = self.span(s("break3") + 0.2, s("fix3") - 0.1)
            if p > 0:
                v2.gauge(c, 60, 300, [(self.L["tank"], self.tank.at(tw), mix(WARN, "#38BDF8", self.tank.at(tw)))], p, w=320)
            self.chip(540, 560, "people", T["seven"] - 0.1, T["week"] - 0.15, accent=HILITE, size=40)
            self.chip(540, 560, "week", T["week"] - 0.1, s("fix3") - 0.1, accent=WARN, size=40)
            self.badge("alert", T["tap"], s("fix3") - 0.2)
            self.red(T["tap"], 2.0)
            return
        x0, y0 = self.at(-360, 70)
        self.label(x0, y0, 300, 1210, "factory", T["factory"] + 0.2, T["filters"] - 0.1, "#38BDF8")
        x1, y1 = self.at(-20, 66)
        self.label(x1, y1, 640, 1210, "filter", T["filters"] + 0.05, T["only"] - 0.1, HILITE)
        x2, y2 = self.at(400, 132)
        self.label(x2, y2, 780, 1210, "salt", T["only"] + 0.05, self.tl.e("fix3") + 0.5, "#E5E7EB", size=30)
        self.badge("check", T["only"] + 0.4, s("break4") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: the harbor from above (break4, fix4)
    def ship_top(self, c, t, pods=0.0, pod_ang=90.0, jets=0.0, thr=0.0):
        p = skia.Path()
        p.moveTo(-450, -66)
        p.lineTo(240, -75)
        p.quadTo(420, -62, 466, 0)
        p.quadTo(420, 62, 240, 75)
        p.lineTo(-450, 66)
        p.quadTo(-472, 0, -450, -66)
        p.close()
        c.drawPath(p, P("#0B1220", 0.35, blur=18))
        c.drawPath(p, P(NAVY))
        c.save()
        c.translate(4, 0)
        c.scale(0.95, 0.84)
        c.drawPath(p, lin_paint(0, -70, 0, 70, ["#FFFFFF", "#E2E8F0", "#CBD5E1"]))
        c.restore()
        for k in range(8):                                                         # lifeboats
            for sd in (-1, 1):
                c.drawRRect(rr(-300 + k * 64, sd * 54 - 7, 44, 14, 7), P(ORANGE))
        c.drawRRect(rr(-120, -34, 150, 68, 16), P(POOL))                           # pools
        c.drawRRect(rr(60, -26, 90, 52, 14), P(POOL))
        c.drawRRect(rr(-120, -34, 150, 68, 16), P("#E0F7FF", 0.5, stroke=3))
        c.drawOval(R(-290, -30, 80, 60), P("#C2410C"))                              # funnel
        c.drawCircle(330, 0, 34, P("#94A3B8"))
        text(c, "H", 330, 12, 34, "#FFFFFF", "Poppins-Black")
        if thr > 0:                                                                # bow thrusters: a tunnel across the bow
            c.drawRect(R(370, -72, 34, 144), P("#0B1220", thr))
            for k in range(3):
                yy = 76 + ((t * 300 + k * 50) % 150)
                c.drawLine(377 + k * 10, yy, 377 + k * 10, yy + 26, P("#BFE6FF", 0.9 * thr * jets, stroke=6))
        if pods > 0:                                                               # azimuth pods at the stern
            for sd in (-1, 1):
                px, py = -470, sd * 36
                c.save()
                c.translate(px, py)
                c.scale(pods, pods)
                c.drawCircle(0, 0, 24, P("#475569"))
                c.drawCircle(0, 0, 24, P(HILITE, 0.9, stroke=4))
                a = math.radians(pod_ang)
                c.drawLine(0, 0, math.cos(a) * 40, math.sin(a) * 40, P(HILITE, 1, stroke=8))
                c.restore()
                if jets > 0:
                    a = math.radians(pod_ang)
                    for k in range(4):
                        d = 50 + ((t * 320 + k * 40) % 160)
                        c.drawCircle(px + math.cos(a) * d, py + math.sin(a) * d, 7 - k, P("#BFE6FF", 0.8 * jets))

    def draw_harbor(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["harbor"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0E3F6E", "#0A2E57", "#082345"]))
        self.view(c, cam)
        rng = random.Random(3)
        for i in range(70):                                                        # ripples
            x, y = rng.uniform(-1300, 1300), rng.uniform(-300, 900)
            w = 30 + 20 * math.sin(t * 1.3 + i)
            c.drawLine(x - w, y, x + w, y, P("#7DB7E8", 0.25, stroke=3))
        box(c, -1400, -700, 2800, 370, "#6B7385", r=0)                             # the dock
        c.drawRect(R(-1400, -340, 2800, 14), P("#F8FAFC", 0.8))
        for bx in range(-1300, 1300, 160):
            c.drawCircle(bx, -346, 11, P("#1F2937"))
        for k in range(5):                                                         # the terminal on the dock
            box(c, -1200 + k * 520, -660, 380, 200, ("#94A3B8", "#A3AEC2")[k % 2], r=10)
        box(c, 640, -330, 110, 1300, "#6B7385", r=0)                                # the end of the basin
        c.drawRect(R(640, -330, 14, 1300), P("#F8FAFC", 0.7))
        turn = prog(t, T["turn"] - 0.3, T["turn"]) * (1 - prog(t, s("fix4") + 0.3, s("fix4") + 0.8))
        sx, sy = self.sx.at(t), self.sy.at(t)
        ang = -4 * bump(t, T["turn"] - 0.2, T["bump"] + 0.6)
        moving = s("break4") - 0.1 <= t < T["turn"]
        if moving:                                                                 # the wake
            for k in range(10):
                d = k * 70 + (t * 200) % 70
                c.drawLine(sx - 470 - d, -40 - k * 8, sx - 470 - d - 40, -40 - k * 8, P("#E0F2FE", 0.5 - k * 0.04, stroke=5))
                c.drawLine(sx - 470 - d, 40 + k * 8, sx - 470 - d - 40, 40 + k * 8, P("#E0F2FE", 0.5 - k * 0.04, stroke=5))
        if turn > 0:                                                               # the circle it would need to turn
            r = 470
            c.drawCircle(sx, sy, r, P(WARN, 0.9 * turn, stroke=6))
            c.drawCircle(sx, sy, r, P(WARN, 0.14 * turn))
        pods = prog(t, T["pods"] - 0.2, T["pods"] + 0.2)
        spin = 90 + 360 * e_io(prog(t, T["spin"] - 0.2, T["spin"] + 0.8))
        jets = prog(t, T["sideways"] - 0.5, T["sideways"] - 0.2) * (1 - prog(t, T["dock"] + 0.3, T["dock"] + 0.8))
        thr = prog(t, T["thrusters"] - 0.2, T["thrusters"] + 0.2)
        c.save()
        c.translate(sx, sy)
        c.rotate(ang)
        self.ship_top(c, t, pods, spin, jets, thr)
        c.restore()
        if t >= T["dock"]:                                                          # mooring lines
            for lx in (-380, 0, 380):
                k = prog(t, T["dock"], T["dock"] + 0.4)
                c.drawLine(sx + lx, sy - 66, sx + lx + 40, lerp(sy - 66, -346, k), P("#F8FAFC", 0.9, stroke=4))
        if t >= T["bump"]:
            splash(c, sx + 460, sy - 40, t, T["bump"], 0.7, n=16, speed=380, seed=21, gravity=0)
        c.restore()
        self.ui["cam"] = cam
        self.ui["ship"] = (sx, sy)

    def ui_harbor(self, c, t, tw):
        T, s = self.T, self.tl.s
        sx, sy = self.ui.get("ship", (0, 0))
        if tw < s("fix4"):
            self.chip(540, 560, "circle", T["turn"] - 0.1, s("fix4") + 0.2, accent=WARN, size=38)
            self.badge("alert", T["bump"], s("fix4") - 0.2)
            self.red(T["bump"], 2.0)
            return
        x1, y1 = self.at(sx - 470, sy + 36)
        self.label(x1, y1, 300, min(1210, y1 + 200), "pods", T["pods"] + 0.2, T["thrusters"] - 0.1, HILITE)
        x2, y2 = self.at(sx + 387, sy + 72)
        self.label(x2, y2, 760, min(1210, y2 + 200), "thr", T["thrusters"] + 0.2, T["dock"] + 0.3, "#7DD3FC")
        self.badge("check", T["dock"] + 0.2, s("cta") - 0.05, x=880, y=520)

    # ------------------------------------------------------------------ set: the finished ship (cta, reveal, stat, closer)
    def ship_side(self, c, t, decks, pools=0.0, slides=0.0, theater=0.0, puff_t=None):
        """The finished ship from the side, bow to the right, on the waterline (y = 0)."""
        top_y = TOP0 - decks * DECK_H
        n = int(math.ceil(decks))
        for i in range(n):                                                          # decks, bottom up
            k = clamp(decks - i)
            y0 = TOP0 - (i + 1) * DECK_H
            x0 = -640 + max(0, i - 15) * 34
            x1 = 590 - i * 11
            yy = y0 + DECK_H * (1 - k)
            c.drawRect(R(x0, yy, x1 - x0, DECK_H * k), P(WHITE))
            if k >= 1:
                c.drawRect(R(x0 + 6, y0 + 3, x1 - x0 - 12, DECK_H - 7), P("#35558C"))
                for wx in range(int(x0 + 10), int(x1 - 14), 15):
                    if (wx // 15 * 7 + i * 3) % 5:
                        c.drawRect(R(wx, y0 + 5, 9, DECK_H - 11), P("#F6D58A", 0.92))
                c.drawRect(R(x0, y0 + DECK_H - 4, x1 - x0, 3), P("#F8FAFC"))
        if decks >= 6:                                                              # lifeboats
            ly = TOP0 - 3 * DECK_H - 8
            for k in range(13):
                c.drawRRect(rr(-560 + k * 74, ly, 56, 20, 10), P(ORANGE))
                c.drawRect(R(-560 + k * 74 + 6, ly + 13, 44, 3), P("#9A3412"))
        if theater > 0:                                                             # the theater, lit through the side
            tk = e_back(clamp(theater))
            c.save()
            c.translate(220, TOP0 - 7 * DECK_H)
            c.scale(tk, tk)
            c.drawRRect(rr(-150, -64, 300, 104, 14), P("#7C1D3F"))
            for k in range(16):
                c.drawCircle(-135 + k * 18, -54, 4.5, P(HILITE, 0.6 + 0.4 * math.sin(t * 8 + k)))
            word(c, self.L["theater"], 0, 10, 40, "#FFE4F1")
            add_glow(c, 0, -10, 170, "#FF5EA8", 0.3)
            c.restore()
        if decks >= 19.5:
            c.drawRect(R(-110, top_y - 8, 520, 8), P("#CBD5E1"))
        if pools > 0:
            pk = e_back(clamp(pools))
            for px_, pw in ((-90, 190), (150, 120)):
                c.drawRRect(rr(px_, top_y - 22 * pk, pw, 22 * pk, 7), P(POOL))
                c.drawRect(R(px_ + 6, top_y - 17 * pk, pw - 12, 4), P("#E0F7FF", 0.6 + 0.3 * math.sin(t * 5 + px_)))
        if slides > 0:
            sk = clamp(slides)
            tx, ty = -300, top_y - 190 * sk
            c.drawRect(R(tx - 12, ty, 24, top_y - ty), P("#94A3B8"))
            for j, col in enumerate(("#F43F5E", "#22C55E", "#FACC15")):
                sp = skia.Path()
                sp.moveTo(tx, ty + 14 + j * 22)
                sp.cubicTo(tx + 150, ty - 40 + j * 10, tx + 80 + j * 30, top_y - 30, tx + 230 + j * 26, top_y - 4)
                c.drawPath(sp, P(col, sk, stroke=16))
        fx = -520 if decks < 15 else -470
        c.drawRRect(rr(fx, top_y - 110, 96, 114, 18), P("#C2410C"))                  # funnel
        c.drawRect(R(fx, top_y - 88, 96, 18), P(NAVY))
        if puff_t is not None and t >= puff_t:
            v2.smoke(c, fx + 48, top_y - 114, t, puff_t, puff_t + 0.5, rate=20, life=1.8, size=(20, 80), col="#E2E8F0")
        hull = skia.Path()                                                         # the hull, on the waterline
        hull.moveTo(-690, TOP0)
        hull.lineTo(640, TOP0)
        hull.lineTo(720, TOP0 - 22)
        hull.quadTo(700, 0, 610, 80)
        hull.lineTo(-640, 80)
        hull.quadTo(-690, 40, -690, TOP0)
        hull.close()
        c.drawPath(hull, lin_paint(0, TOP0 - 22, 0, 80, [shade(NAVY, 0.2), NAVY, shade(NAVY, -0.4)]))
        c.drawRect(R(-690, TOP0, 1340, 9), P(WHITE))
        for k in range(46):
            c.drawCircle(-640 + k * 28, -96, 5, P("#F6D58A", 0.85))

    def draw_wide(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["wide"].at(t)
        cam = (cam[0] + math.sin(t * 0.5) * 3, cam[1], cam[2])
        self.sea_back(c, t, cam)
        self.view(c, cam)
        self.sea_world(c, t, cam, moon_x=-520)
        decks = self.decks.at(t)
        pools = prog(t, T["pools"] - 0.15, T["pools"] + 0.35)
        slides = prog(t, T["wpark"] - 0.15, T["wpark"] + 0.55)
        theater = prog(t, T["theater"] - 0.15, T["theater"] + 0.3)
        bob = math.sin(t * 1.1) * 4
        c.save()
        c.translate(0, bob)
        self.ship_side(c, t, decks, pools, slides, theater, puff_t=s("closer") + 0.2)
        c.restore()
        dk = 1 - prog(t, s("reveal") - 0.4, s("reveal") + 0.2)
        if dk > 0:                                                                 # still at the dock: it hasn't left port
            box(c, -1100, -26, 2200, 46, "#6B7385", a=dk)
            for bx in range(-1000, 1001, 250):
                cyl(c, bx, -50, 22, 26, "#1F2937", r=6, a=dk)
        self.veil(c, t, cam, 0.55)
        if t >= s("reveal"):
            sparks_shower(c, 0, TOP0 - decks * DECK_H, t, T["decks20"] + 0.5, 0.7, n=18, speed=420, seed=8, col=HILITE)
        c.restore()
        self.ui["cam"] = cam
        self.ui["top"] = TOP0 - decks * DECK_H + bob

    def ui_wide(self, c, t, tw):
        T, s = self.T, self.tl.s
        if s("reveal") <= tw < T["s1"] - 0.3:
            top = self.ui.get("top", -650)
            x0, y0 = self.at(560, top + 40)
            self.label(x0, y0, 800, max(330, y0 - 160), "decks", T["decks20"] + 0.1, T["pools"] - 0.1, HILITE)
            x1, y1 = self.at(10, top - 12)
            self.label(x1, y1, 300, max(330, y1 - 190), "pools", T["pools"] + 0.15, T["wpark"] - 0.1, "#38BDF8")
            x2, y2 = self.at(-330, top - 120)
            self.label(x2, y2, 330, max(330, y2 - 150), "wpark", T["wpark"] + 0.25, s("stat") - 0.1, "#F43F5E")

    # ------------------------------------------------------------------ set: the pier (tag)
    def draw_pier(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["pier"].at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        self.sea_back(c, t, cam)
        self.view(c, cam)
        self.sea_world(c, t, cam, moon_x=300)
        go = max(0.0, t - (T["leaves"] - 0.3))
        sx = 70 + 60 * go * go + 70 * go                                            # the ship's stern, pulling away
        c.drawRect(R(sx, -780, 1500, 630), P(WHITE))
        for row in range(11):
            y0 = -770 + row * 56
            c.drawRect(R(sx + 10, y0, 1480, 40), P("#35558C"))
            for k in range(18):
                if (row * 5 + k * 3) % 7:
                    c.drawRect(R(sx + 22 + k * 80, y0 + 6, 46, 28), P("#F6D58A", 0.92))
        stern = skia.Path()
        stern.moveTo(sx, -150)
        stern.lineTo(sx + 1500, -150)
        stern.lineTo(sx + 1500, 90)
        stern.lineTo(sx + 60, 90)
        stern.quadTo(sx, 40, sx, -150)
        stern.close()
        c.drawPath(stern, lin_paint(0, -150, 0, 90, [shade(NAVY, 0.2), NAVY]))
        c.drawRect(R(sx, -156, 1500, 10), P(WHITE))
        c.drawRect(R(sx - 30, -300, 420, 14), P("#94A3B8"))                         # the aft terrace and its rail
        c.drawRect(R(sx - 30, -352, 420, 4), P("#CBD5E1"))
        film = prog(t, T["videos"] - 0.2, T["videos"] + 0.2)
        for i in range(5):
            px = sx + 20 + i * 74
            person(c, px, -300, 100, SHIRTS[i % 3], t + i * 0.3, "point" if film > 0 else "look", face=-1,
                   skin=SKINS[i % 5])
            if film > 0:
                phone(c, px - 34, -372, film * (0.5 + 0.5 * math.sin(t * 9 + i)), t)
        if go > 0:
            for k in range(12):                                                    # churned water under the stern
                c.drawCircle(sx + 30 + k * 36, 6 + math.sin(t * 7 + k) * 4, 16 + (k % 3) * 6, P("#E0F2FE", 0.35))
        box(c, -1500, -62, 1440, 26, "#8B5E3C", r=3)                               # the pier
        for px in range(-1480, -60, 130):
            cyl(c, px, -38, 18, 300, "#5B3A22")
        cyl(c, -90, -86, 26, 26, "#1F2937", r=6)
        run = prog(t, s("tag") - 0.2, T["leaves"] + 0.1)
        rx = lerp(-760, -150, e_out(run))
        pose = "walk" if run < 1 else "cheer"
        person(c, rx, -62, 130, SHIRTS[0], t * (2.2 if run < 1 else 1), pose, face=1, skin=SKINS[1], hat="cap")
        box(c, rx - 50, -116, 26, 36, "#7C3AED", r=6)
        self.veil(c, t, cam, 0.35)
        c.restore()
        self.ui["cam"] = cam

    def ui_pier(self, c, t, tw):
        T = self.T
        self.chip(540, 560, "videos", T["thousands"] - 0.15, self.duration + 1, accent=HILITE, size=44)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.62)
        v2.stars(c, W, H, t, 0.8)

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 60), -9), (T["land"] - 0.05, sfx.thud(0.5, 61), -2), (T["land"], water_snd(0.9, 62), -4),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 63), -9), (T["cruise"], sfx.pop(64), -8)]
        ev += [(T["tall"], sfx.creak(0.6, 65), -9), (T["wave"] - 0.6, wave_snd(1.8, 66), -4), (T["capsize"], sfx.creak(0.8, 67), -6),
               (T["tips"], sfx.alarm(3, 820), -11), (T["capsize"] + 0.45, water_snd(1.2, 68), -2), (T["over"] + 0.2, sfx.womp(), -9)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 69), -4), (T["wide"] - 0.05, sfx.whoosh(0.5, False, 70), -8),
               (T["wide"] + 0.2, sfx.clank(300, 0.4, 71), -6)]
        ev += [(T[k] + 0.25, sfx.thud(0.45, 72 + i), -3) for i, k in enumerate(("engines", "fuel", "water"))]
        ev += [(T["push"], wave_snd(1.2, 76), -8), (T["push"] + 0.3, sfx.creak(0.6, 77), -9), (T["rolls"] + 0.35, sfx.chime(), -6)]
        ev += [(T["rocks"], sfx.creak(1.0, 78), -8), (T["rocks"] + 0.05, sfx.alarm(3, 820), -11), (T["green"], sfx.womp(), -7),
               (T["buffet"], sfx.clank(900, 0.25, 79), -10)]
        ev += [(T["fins"] - 0.05, sfx.whirr(0.7, 140, 260, 80), -8), (T["fins"] + 0.3, sfx.clank(420, 0.3, 81), -7),
               (T["tilt"], sfx.whirr(1.2, 180, 220, 82), -12), (T["ninety"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 83), -4), (s("break3"), shower_snd(1.6, 84), -12),
               (T["tap"], sfx.power_down(0.8, 85), -9), (T["tap"] + 0.05, sfx.alarm(3, 820), -11), (T["week"], sfx.womp(), -8)]
        ev += [(T["factory"] - 0.2, sfx.thud(0.4, 86), -5), (T["squeeze"] - 0.1, sfx.hum(2.6, 82), -12),
               (T["squeeze"], water_snd(1.2, 87), -12), (T["filters"], sfx.pop(88), -7), (T["only"] + 0.4, sfx.chime(), -6),
               (T["only"] + 0.45, shower_snd(1.2, 89), -13)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 90), -4), (s("break4"), horn_snd(1.2), -12), (T["turn"] - 0.2, sfx.alarm(3, 820), -11),
               (T["bump"], sfx.clank(160, 0.8, 91), -2), (T["bump"] + 0.02, sfx.thud(0.6, 92), -3)]
        ev += [(T["pods"] - 0.1, sfx.pop(93), -6), (T["spin"] - 0.2, sfx.whirr(1.0, 120, 320, 94), -8),
               (T["thrusters"] - 0.1, sfx.pop(95), -6), (T["sideways"] - 0.5, sfx.whirr(1.6, 150, 240, 96), -9),
               (T["dock"] + 0.05, sfx.thud(0.3, 97), -6), (T["dock"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(98), 0), (T["follow"] - 0.15, sfx.pop(99), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 100), -7)]
        ev += [(T["stack"] + 0.2 * i, sfx.clank(500 + 30 * i, 0.12, 101 + i), -11) for i in range(8)]
        ev += [(T["pools"], water_snd(0.6, 110), -9), (T["wpark"], sfx.whoosh(0.6, True, 111), -9), (T["theater"], sfx.sparkle(0.6, 7, 112), -9)]
        ev += [(T["s1"], sfx.pop(113), -3), (T["s2"], sfx.pop(114), -3), (T["s3"], sfx.pop(115), -3), (T["s1"] - 0.3, sfx.whoosh(1.2, False, 116), -12)]
        ev += [(s("closer") + 0.2, horn_snd(1.8), -4), (T["cong2"], sfx.pop(117), -2), (T["cong2"], sfx.sparkle(1.0, 14, 118), -4),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 119), -6), (T["leaves"] - 0.4, horn_snd(1.0), -10),
               (T["videos"], sfx.click(120), -6), (T["videos"] + 0.15, sfx.click(121), -7), (T["thousands"] + 0.4, sfx.womp(), -4)]
        return ev


NAME = "cruise"
EPISODE = Cruise
