"""Episode 42 - Venice, a city on wooden piles.  v2 look: a lagoon at dusk, palaces cut open down to the mud, and
under them an upside-down forest of tree trunks.

Sets: city (hook: palaces on the water, the ground cut open, a forest of upside-down trunks beneath, a tree flips into
a pile; the reveal: palaces, canals, the Rialto Bridge, a car turns into a boat; the stat; the closer), mud (break1: a
stone palace sinks into soft mud like a boot; fix1: the crew drives piles by hand with a drop weight, singing, nine per
square meter), deep (break2: the piles stop far above the rock; fix2: from above, piles go in on a spiral from the
outside in, the mud squeezes them, friction holds), rot (break3: a post in the air gets mushrooms and bugs and crumbles;
fix3: down in the mud and water there is no air, the bugs and fungi stay away, the pile lasts), wall (break4: bricks soak
up salt water like a sponge and crumble; fix4: piles sawn level, thick boards, a band of hard white stone, the salt
stops; the cta), cafe (the tag: a wobbly table and a folded napkin; in Arabic the dining table at home and folded paper).
World (city, mud, deep, wall): side view, the water surface is y = 0, the mud starts at MUD_Y, down is positive.
"""
from v2_base import *  # noqa: F401,F403

DUSK = {"top": "#0C1230", "upper": "#2A2160", "mid": "#6B3A78", "low": "#D2706E", "horizon": "#F6B07E",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
MUD_Y = 70.0
PILE_L = 340.0
LAGOON, LAGOON_D = "#2C7A86", "#123C4A"
MUD, MUD_D = "#5A4632", "#2A2016"
WOOD, WOOD_D = "#9A6B3F", "#5E3B1E"
STONE = "#CFC8B8"
FACADES = ("#B97E5C", "#A85C4A", "#B98F5E", "#9C5048", "#B5A383", "#8E4A3C", "#B38C58")
PALACES = [(-1500, -1080, 520, 0), (-860, -440, 600, 1), (440, 860, 640, 2), (1080, 1500, 540, 3)]


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


# ====================================================================================== pieces
def pile(c, x, y_top, L, w=22, a=1.0, rot_=0.0, fresh=1.0):
    """One wooden pile: a tree trunk driven tip down, top at y_top."""
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(x - w / 2, y_top)
    p.lineTo(x + w / 2, y_top)
    p.lineTo(x + w * 0.32, y_top + L * 0.86)
    p.lineTo(x, y_top + L)
    p.lineTo(x - w * 0.32, y_top + L * 0.86)
    p.close()
    col = mix(WOOD, "#3B3328", rot_ * 0.7)
    c.drawPath(p, lin_paint(x - w / 2, 0, x + w / 2, 0, [shade(col, 0.18), col, shade(col, -0.35)], a=a))
    for k in range(3):
        yy = y_top + L * (0.2 + k * 0.25)
        c.drawLine(x - w * 0.3, yy, x - w * 0.1, yy + 18, P(WOOD_D, 0.6 * a, stroke=2))
    c.drawOval(R(x - w / 2, y_top - 4, w, 8), P("#C9935A", a))


def mud(c, x0, x1, y0, y1, t, a=1.0):
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), lin_paint(0, y0, 0, y1, [MUD, "#43331F", MUD_D], a=a))
    rng = random.Random(int(x0))
    for i in range(int((x1 - x0) * (y1 - y0) / 26000)):
        c.drawCircle(rng.uniform(x0, x1), rng.uniform(y0 + 10, y1), rng.uniform(3, 8), P("#2E2214", 0.5 * a))


def lagoon(c, x0, x1, y0, y1, t, a=1.0):
    if y1 <= y0:
        return
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), lin_paint(0, y0, 0, y1, [LAGOON, "#1E5E6C", LAGOON_D], a=0.95 * a))
    c.drawRect(R(x0, y0, x1 - x0, 5), P("#BFF3F0", 0.5 * a))
    xx = x0 + 10
    while xx < x1 - 30:
        dx = math.sin(t * 1.6 + xx * 0.04) * 6
        c.drawLine(xx + dx, y0 + 12, xx + dx + 24, y0 + 12, P("#A5F3FC", 0.35 * a, stroke=2.5))
        xx += 64


def palace(c, x0, x1, h, idx, t, a=1.0, grow=1.0, stone=1.0):
    """A Venetian palace standing on y = 0: a white stone base, a coloured facade, pointed arched windows."""
    if a <= 0 or grow <= 0:
        return
    w = x1 - x0
    hh = h * grow
    top = -hh
    col = FACADES[idx % len(FACADES)]
    c.drawRect(R(x0, top, w, hh), lin_paint(x0, 0, x1, 0, [shade(col, 0.1), col, shade(col, -0.18)], a=a))
    c.drawRect(R(x0 - 8, top - 14, w + 16, 16), P(shade(col, -0.35), a))
    c.drawRect(R(x0, -60, w, 70), P(STONE, a * stone))                         # the white stone base
    floors = max(1, int(hh / 150))
    cols = max(2, int(w / 90))
    for f in range(floors):
        yb = -80 - f * 150
        if yb - 100 < top + 10:
            break
        for k in range(cols):
            wx = x0 + (k + 0.5) * w / cols
            arch = skia.Path()
            arch.moveTo(wx - 18, yb)
            arch.lineTo(wx - 18, yb - 66)
            arch.quadTo(wx - 18, yb - 92, wx, yb - 104)
            arch.quadTo(wx + 18, yb - 92, wx + 18, yb - 66)
            arch.lineTo(wx + 18, yb)
            arch.close()
            lit = 0.5 + 0.5 * math.sin(k * 2.1 + f * 1.3 + idx)
            c.drawPath(arch, P(mix("#2A1E2E", "#F5C26B", 0.15 + 0.5 * lit), a))
            c.drawPath(arch, P("#E7DCC8", 0.7 * a, stroke=3))
        if f == 0 and hh > 300:                                               # a balcony
            c.drawRect(R(x0 + w * 0.3, yb - 6, w * 0.4, 8), P("#F8F1E2", a))
    c.drawRect(R(x0 + w * 0.42, -60, w * 0.16, 60), P("#2B1D18", a))         # water door


def gondola(c, x, y, s=1.0, a=1.0, t=0.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y + math.sin(t * 2) * 3)
    c.scale(s, s)
    hull = skia.Path()
    hull.moveTo(-130, -20)
    hull.quadTo(0, 18, 120, -20)
    hull.quadTo(140, -40, 150, -64)
    hull.quadTo(120, -10, 0, -6)
    hull.quadTo(-120, -10, -150, -50)
    hull.close()
    c.drawPath(hull, P("#0B0B12", a))
    person(c, 80, -14, 120, "#F8FAFC", t, pose="stand", face=-1, hat="none", a=a)
    c.drawLine(40, -120, 10, 30, P("#8B5A2B", a, stroke=5))
    c.restore()


def tree(c, x, y, s, flip, a=1.0):
    """A tree that flips upside down (flip 0..1) and loses its crown on the way: it becomes a pile."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(180 * flip)
    c.scale(s, s)
    c.drawRect(R(-14, -200, 28, 200), lin_paint(-14, 0, 14, 0, [shade(WOOD, 0.2), WOOD, WOOD_D], a=a))
    ck = 1 - clamp(flip * 1.6)
    if ck > 0:
        for (bx, by, r) in ((0, -250, 70), (-50, -210, 50), (50, -210, 50), (0, -320, 50)):
            c.drawCircle(bx, by, r, P("#2F7A3E", a * ck))
    c.restore()


def boot(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    b = skia.Path()
    b.moveTo(-30, -120)
    b.lineTo(20, -120)
    b.lineTo(20, -40)
    b.quadTo(80, -30, 80, 0)
    b.lineTo(-30, 0)
    b.close()
    c.drawPath(b, P("#3F2E21", a))
    c.drawRect(R(-34, -128, 58, 14), P("#5B4332", a))
    c.restore()


def notes(c, x, y, t, a=1.0, n=5):
    """Musical notes floating up from a singing crew."""
    if a <= 0:
        return
    for i in range(n):
        q = (t * 0.6 + i / n) % 1.0
        nx = x + math.sin(t * 2 + i * 1.7) * 40 + i * 14
        ny = y - q * 220
        al = a * (1 - q)
        c.drawCircle(nx, ny, 9, P("#FDE68A", al))
        c.drawLine(nx + 8, ny, nx + 8, ny - 34, P("#FDE68A", al, stroke=3))
        c.drawLine(nx + 8, ny - 34, nx + 22, ny - 26, P("#FDE68A", al, stroke=3))


def mushroom(c, x, y, s, a=1.0):
    c.drawRect(R(x - 4 * s, y - 16 * s, 8 * s, 16 * s), P("#F5F5F4", a))
    c.drawArc(R(x - 16 * s, y - 28 * s, 32 * s, 24 * s), 180, 180, True, P("#B45309", a))


def bug(c, x, y, s, t, a=1.0):
    c.drawOval(R(x - 8 * s, y - 5 * s, 16 * s, 10 * s), P("#1F2937", a))
    for k in (-1, 0, 1):
        c.drawLine(x + k * 4 * s, y, x + k * 6 * s, y + (6 + math.sin(t * 20 + k) * 2) * s, P("#1F2937", a, stroke=2))


def table(c, x, y, s, t, wob=0.0, a=1.0, top="#E5E7EB", leg="#6B7280"):
    """A small round café table from the side, wobbling by wob degrees."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.rotate(wob)
    c.drawRect(R(-8, -170, 16, 170), P(leg, a))
    c.drawRect(R(-70, -6, 140, 10), P(leg, a))
    c.drawRRect(rr(-150, -186, 300, 20, 8), P(top, a))
    c.drawRRect(rr(-30, -224, 50, 38, 8), P("#D6D3D1", a))                      # a cup
    c.drawArc(R(14, -216, 22, 20), -90, 180, False, P("#D6D3D1", a, stroke=5))
    c.restore()


# ====================================================================================== the episode
class Venice(EpisodeV2):
    BUILD_NO = 42
    FIRST_SET = "city"
    CLEAR = "#0C1230"
    TITLE = {"en": "VENICE", "ar_sa": "فينيسيا"}
    EMPH = {"en": ["CONGRATS", "WHOLE", "CITY", "UPSIDE-DOWN", "FOREST", "MUD", "SEA", "VENICE", "LAGOON", "SOFT",
                   "STONE", "PALACE", "SINKS", "BOOT", "HAMMER", "WOODEN", "PILES", "HAND", "NINE", "SQUARE", "SINGS",
                   "BEAT", "SHORT", "SOLID", "ROCK", "SPIRAL", "OUTSIDE", "SQUEEZES", "FRICTION", "WEIGHT", "ROTTEN",
                   "NO", "AIR", "FUNGI", "INSECTS", "CENTURIES", "BRICKS", "SALT", "SPONGE", "EATS", "SAW", "LEVEL",
                   "BOARDS", "WHITE", "DENSE", "FOLLOW", "GREAT", "WALL", "CHINA", "PALACES", "CANALS", "BRIDGES",
                   "CAR", "BOAT", "SIXTEEN", "MILLIONS", "FOURTEEN", "RIALTO", "YOURSELF", "STICKS", "STANDING",
                   "CAFE", "TABLE", "NAPKIN", "LEG"],
            "ar_sa": ["مبروك", "مدينة", "كاملة", "غابة", "شجر", "مقلوبة", "طين", "البحر", "فينيسيا", "البحيرة", "طري",
                      "القصر", "الحجر", "يغرز", "الجزمة", "عواميد", "خشب", "بإيدك", "تسعة", "متر", "بيغنوا",
                      "الدقة", "قصيرة", "للصخر", "لفة", "برة", "لجوة", "يحضنها", "جامد", "والاحتكاك", "بيعفن",
                      "هوا", "عفن", "حشرات", "قرون", "الطوب", "بيشرب", "الإسفنجة", "والملح", "ياكل", "فتقص",
                      "ألواح", "تخينة", "بحجر", "استريا", "تابعني", "سور", "الصين", "القصور", "والقنوات", "والكباري",
                      "عربية", "بمركب", "ستاشر", "قرن", "ملايين", "وأربعتاشر", "ريالتو", "بإيدك", "واقفة",
                      "وترابيزة", "السفرة", "رجلها", "ورقة", "مطبقة"]}
    KEYS = {"ar_sa": {
        ("hook", "CITY"): "مدينة", ("hook", "UPSIDE-DOWN"): "مقلوبة", ("hook", "FOREST"): "غابة", ("hook", "MUD"): "طين",
        ("hook", "CONGRATS"): "مبروك", ("hook", "VENICE"): "فينيسيا",
        ("break1", "LAGOON"): "البحيرة", ("break1", "SOFT"): "طري", ("break1", "PALACE"): "القصر",
        ("break1", "SINKS"): "يغرز", ("break1", "BOOT"): "الجزمة",
        ("fix1", "HAMMER"): "فتدق", ("fix1", "PILES"): "عواميد", ("fix1", "HAND"): "بإيدك", ("fix1", "NINE"): "تسعة",
        ("fix1", "SINGS"): "بيغنوا", ("fix1", "BEAT"): "الدقة",
        ("break2", "SHORT"): "قصيرة", ("break2", "ROCK"): "للصخر",
        ("fix2", "SPIRAL"): "لفة", ("fix2", "OUTSIDE"): "برة", ("fix2", "SQUEEZES"): "يحضنها", ("fix2", "FRICTION"): "والاحتكاك",
        ("break3", "ROTTEN"): "بيعفن",
        ("fix3", "AIR"): "هوا", ("fix3", "FUNGI"): "عفن", ("fix3", "INSECTS"): "حشرات", ("fix3", "CENTURIES"): "قرون",
        ("break4", "BRICKS"): "الطوب", ("break4", "SPONGE"): "الإسفنجة", ("break4", "EATS"): "ياكل",
        ("fix4", "SAW"): "فتقص", ("fix4", "BOARDS"): "ألواح", ("fix4", "STONE"): "بحجر", ("fix4", "CLIMB"): "ميعرفش",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PALACES"): "القصور", ("reveal", "CANALS"): "والقنوات", ("reveal", "BRIDGES"): "والكباري",
        ("reveal", "BOAT"): "بمركب",
        ("stat", "SIXTEEN"): "ستاشر", ("stat", "MILLIONS"): "ملايين", ("stat", "FOURTEEN"): "وأربعتاشر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STICKS"): "خشب", ("tag", "TABLE"): "وترابيزة", ("tag", "NAPKIN"): "ورقة", ("tag", "LEG"): "رجلها"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Great Wall of China"),
                   "stat": [("1,600", "YEARS OLD"), ("MILLIONS", "OF WOODEN PILES"), ("14,000", "UNDER THE RIALTO")],
                   "L": {"city": "A WHOLE CITY", "forest": "ON AN UPSIDE-DOWN FOREST", "venice": "VENICE",
                         "soft": "SOFT MUD", "sinks": "SINKS LIKE A BOOT", "hammer": "PILES, BY HAND",
                         "nine": "9 PER m²", "sing": "SINGING TO THE BEAT", "short": "TOO SHORT",
                         "rock": "SOLID ROCK", "spiral": "A SPIRAL, OUTSIDE IN", "squeeze": "THE MUD SQUEEZES",
                         "friction": "FRICTION HOLDS IT", "rots": "WOOD ROTS?", "noair": "NO AIR DOWN THERE",
                         "nobugs": "NO FUNGI, NO INSECTS", "lasts": "LASTS CENTURIES", "sponge": "BRICKS SOAK UP SALT",
                         "eats": "SALT EATS THE WALL", "saw": "SAWN LEVEL", "boards": "THICK BOARDS",
                         "stone": "HARD WHITE STONE", "dense": "TOO DENSE FOR SALT", "palaces": "PALACES",
                         "canals": "CANALS", "bridges": "BRIDGES", "boat": "NO CARS, JUST BOATS", "rialto": "RIALTO BRIDGE",
                         "still": "1,600 YEARS: STANDING", "napkin": "FOLDED NAPKIN"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: سور الصين العظيم"),
                      "stat": [("1,600", "سنة واقفة"), ("1,000,000+", "ملايين العواميد"), ("14,000", "تحت كوبري ريالتو")],
                      "L": {"city": "مدينة كاملة", "forest": "على غابة شجر مقلوبة", "venice": "فينيسيا",
                            "soft": "طين طري", "sinks": "يغرز زي الجزمة", "hammer": "عواميد خشب بالإيد",
                            "nine": "9 في كل متر", "sing": "بيغنوا على الدقة", "short": "قصيرة",
                            "rock": "الصخر", "spiral": "لفة لفة، من برة لجوة", "squeeze": "الطين يحضنها جامد",
                            "friction": "الاحتكاك هو اللي شايل", "rots": "الخشب بيعفن؟", "noair": "مفيش هوا تحت",
                            "nobugs": "لا عفن ولا حشرات", "lasts": "تعيش قرون", "sponge": "الطوب بيشرب المية",
                            "eats": "الملح ياكل الحيطان", "saw": "مستوى واحد", "boards": "ألواح خشب تخينة",
                            "stone": "حجر استريا", "dense": "الملح ميطلعش", "palaces": "القصور",
                            "canals": "القنوات", "bridges": "الكباري", "boat": "العربية بقت مركب",
                            "rialto": "كوبري ريالتو", "still": "ستاشر قرن: واقفة", "napkin": "ورقة مطبقة"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "city": ("hook", "CITY", 0.15), "upside": ("hook", "UPSIDE-DOWN", 0.3), "forest": ("hook", "FOREST", 0.42),
            "mud": ("hook", "MUD", 0.55), "congrats": ("hook", "CONGRATS", 0.7), "venice": ("hook", "VENICE", 0.9),
            "lagoon": ("break1", "LAGOON", 0.12), "soft": ("break1", "SOFT", 0.3), "palace": ("break1", "PALACE", 0.6),
            "sinks": ("break1", "SINKS", 0.75), "boot": ("break1", "BOOT", 0.92),
            "hammer": ("fix1", "HAMMER", 0.08), "piles": ("fix1", "PILES", 0.2), "hand": ("fix1", "HAND", 0.38),
            "nine": ("fix1", "NINE", 0.5), "sings": ("fix1", "SINGS", 0.75), "beat": ("fix1", "BEAT", 0.92),
            "short": ("break2", "SHORT", 0.5), "rock": ("break2", "ROCK", 0.9),
            "spiral": ("fix2", "SPIRAL", 0.2), "outside": ("fix2", "OUTSIDE", 0.35), "squeeze": ("fix2", "SQUEEZES", 0.65),
            "friction": ("fix2", "FRICTION", 0.82),
            "rotten": ("break3", "ROTTEN", 0.6),
            "air": ("fix3", "AIR", 0.3), "fungi": ("fix3", "FUNGI", 0.5), "insects": ("fix3", "INSECTS", 0.65),
            "centuries": ("fix3", "CENTURIES", 0.92),
            "bricks": ("break4", "BRICKS", 0.1), "sponge": ("break4", "SPONGE", 0.6), "eats": ("break4", "EATS", 0.85),
            "saw": ("fix4", "SAW", 0.1), "boards": ("fix4", "BOARDS", 0.35), "stone": ("fix4", "STONE", 0.65),
            "climb": ("fix4", "CLIMB", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "palaces": ("reveal", "PALACES", 0.2), "canals": ("reveal", "CANALS", 0.38), "bridges": ("reveal", "BRIDGES", 0.55),
            "boat": ("reveal", "BOAT", 0.9),
            "s1": ("stat", "SIXTEEN", 0.04), "s2": ("stat", "MILLIONS", 0.35), "s3": ("stat", "FOURTEEN", 0.62),
            "cong2": ("closer", "CONGRATS", 0.16),
            "sticks": ("tag", "STICKS", 0.2), "table": ("tag", "TABLE", 0.55), "napkin": ("tag", "NAPKIN", 0.8),
            "leg": ("tag", "LEG", 0.9)})
        T["dig"] = 0.1
        T["sink"] = max(T["sinks"] - 0.3, T["palace"] + 0.1)
        T["fix_nap"] = max(T["napkin"] - 0.2, T["table"] + 0.3) if not self.rtl else max(T["leg"] - 0.4, T["table"] + 0.3)
        T["swap"] = max(T["boat"] - 0.5, T["bridges"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "mud", 1)
        self.cut(s("break2") - 0.12, "deep", -1)
        self.cut(s("break3") - 0.12, "rot", 1)
        self.cut(s("break4") - 0.12, "wall", -1)
        self.cut(s("reveal") - 0.12, "city", 1)
        self.cut(s("tag") - 0.2, "cafe", -1)
        cm = Camera(640, 110, 1.04)
        cm.key(0.05, 640, 120, 1.0, 2.5).key(T["congrats"], 560, 120, 0.94, 2.0)
        cm.key(s("reveal") - 0.12, 0, 160, 0.42, 0.0).key(T["boat"], 0, 140, 0.46, 1.5)
        cm.key(s("stat") - 0.12, 0, 60, 0.44, 0.0)
        cm.key(s("closer") - 0.1, 470, 150, 0.9, 0.0).key(self.duration, 500, 150, 0.93, 2.0)
        self.cam = cm
        self.spans = [(T["boot"], T["beat"] + 0.3), (T["rock"], T["friction"] + 0.3), (T["rotten"], T["centuries"] + 0.3),
                      (T["eats"], T["climb"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 7), (T["sink"] + 0.3, 0.5, 9), (T["hammer"] + 0.3, 0.2, 6),
                       (T["rock"], 0.3, 6), (T["eats"], 0.3, 8), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def city_world(self, c, t, cam, grow=1.0, canals=1.0, bridge=1.0, xray=1.0, swap=-1.0):
        """Palaces on piles along canals, cut open down into the mud (world space is set up here; caller restores)."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 20 * z)
        v2.stars(c, W, H, t, 0.5)
        v2.moon(c, 860 - cx * 0.02, gy - 760 * z - 120, 60)
        self.view(c, cam)
        for i in range(9):                                           # far campanili and domes on the horizon
            bx = -2200 + i * 520
            c.drawRect(R(bx, -260, 60, 260), P("#3B2D55", 0.8))
            tri = skia.Path()
            tri.moveTo(bx - 6, -260)
            tri.lineTo(bx + 30, -330)
            tri.lineTo(bx + 66, -260)
            tri.close()
            c.drawPath(tri, P("#3B2D55", 0.8))
            c.drawArc(R(bx + 140, -200, 160, 140), 180, 180, True, P("#3B2D55", 0.7))
        mud(c, -2600, 2600, MUD_Y, 4000, t)
        lagoon(c, -2600, 2600, 0, MUD_Y + 4 if canals > 0.5 else 0, t, a=canals)
        if canals <= 0.5:
            c.drawRect(R(-2600, 0, 5200, MUD_Y), P(MUD, 1.0))
        for (x0, x1, h, idx) in PALACES:                             # the forests under the palaces
            n = int((x1 - x0) / 30)
            for k in range(n):
                px = x0 + 15 + k * (x1 - x0 - 30) / max(1, n - 1)
                pile(c, px, MUD_Y - 30, PILE_L + (k % 3) * 18, w=24, a=xray)
            c.drawRect(R(x0 - 6, MUD_Y - 44, x1 - x0 + 12, 16), P("#7A5230", xray))        # the boards
        for (x0, x1, h, idx) in PALACES:
            gk = clamp(grow * 1.4 - idx * 0.12) if grow < 1 else 1.0
            palace(c, x0, x1, h, idx, t, grow=e_out(gk))
            c.drawRect(R(x0, -10, x1 - x0, MUD_Y - 34), P(STONE, 1.0))                     # stone base under water
        if bridge > 0:                                               # the Rialto Bridge across the Grand Canal
            bk = e_out(bridge)
            arch = skia.Path()
            arch.moveTo(-440, -40)
            arch.quadTo(0, -330 * bk, 440, -40)
            arch.lineTo(440, -10)
            arch.quadTo(0, -250 * bk, -440, -10)
            arch.close()
            c.drawPath(arch, lin_paint(0, -330, 0, 0, [STONE, "#C9C2B2"], a=bk))
            c.drawRect(R(-120, -246 * bk - 70, 240, 70), P(STONE, bk))
            for k in range(3):
                c.drawRect(R(-100 + k * 76, -246 * bk - 56, 40, 46), P("#5B4636", bk))
            tri = skia.Path()
            tri.moveTo(-130, -246 * bk - 70)
            tri.lineTo(0, -246 * bk - 130)
            tri.lineTo(130, -246 * bk - 70)
            tri.close()
            c.drawPath(tri, P("#E2DACB", bk))
        if canals > 0.5:
            gondola(c, -200 + math.sin(t * 0.3) * 60, 0, 0.9, t=t)
        return gy

    # ------------------------------------------------------------------ set: city (hook, reveal, stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        rv = s("reveal") - 0.12 <= t < s("stat") - 0.12
        if hook:
            xr = prog(t, T["dig"], max(1.4, T["city"]))
            self.city_world(c, t, cam, bridge=0.0, xray=1.0)
            if xr < 1:                                               # the ground is cut open from the top down
                yy = lerp(MUD_Y, 900, e_io(xr))
                mud(c, -2600, 2600, yy, 4000, t)
            fk = prog(t, T["upside"] - 0.6, T["upside"] + 0.3)
            if 0 < fk:                                               # a tree flips over and becomes a pile
                tk = 1 - prog(t, T["mud"], T["mud"] + 0.6)
                tree(c, 300, MUD_Y + 120, 1.0, e_io(fk), a=tk)
        elif rv:
            g = prog(t, T["palaces"] - 0.3, T["canals"])
            cn = prog(t, T["canals"] - 0.3, T["canals"] + 0.3)
            br = prog(t, T["bridges"] - 0.2, T["bridges"] + 0.6)
            self.city_world(c, t, cam, grow=g, canals=max(cn, 0.0), bridge=br)
            sk = prog(t, T["swap"], T["swap"] + 0.8)                 # a car drives off the quay and becomes a boat
            cx_ = lerp(-700, -180, prog(t, T["bridges"], T["swap"]))
            if sk < 0.5:
                carbody(c, cx_, -4, 1.2)
            else:
                gondola(c, cx_ + 40, 0, 0.9, a=prog(sk, 0.5, 0.8), t=t)
            if 0.3 < sk < 0.9:
                splash(c, cx_, 0, t, T["swap"] + 0.35, dur=0.7, n=18, speed=420)
        else:
            self.city_world(c, t, cam)
        c.restore()
        self.ui["cam"] = cam

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam.at(tw))
        if tw < s("break1"):
            self.chip(540, 380, "city", T["city"] - 0.2, T["upside"] - 0.1, accent=HILITE, size=44)
            px, py = self.at(cam, PALACES[2][0] + 60, MUD_Y + 160)
            self.label(px, py, 540, 380, "forest", T["upside"] - 0.1, T["venice"] - 0.1, "#FDBA74", size=34)
            self.chip(540, 380, "venice", T["venice"] - 0.1, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 380, "palaces", T["palaces"] - 0.1, T["canals"] - 0.1, accent=HILITE, size=40)
            self.chip(540, 380, "canals", T["canals"] - 0.1, T["bridges"] - 0.1, accent="#67E8F9", size=40)
            bx, by = self.at(cam, 0, -300)
            self.label(bx, by, 540, 470, "rialto", T["bridges"] - 0.1, T["boat"] - 0.1, "#E2E8F0", size=36)
            self.chip(540, 380, "boat", T["swap"], s("stat") - 0.15, accent=GOOD, size=40)

    # ------------------------------------------------------------------ set: mud (break1, fix1)
    def draw_mud(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, 160, 1.0)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 20 * z)
        self.view(c, cam)
        fixed = t >= s("fix1") - 0.12
        mud(c, -900, 900, MUD_Y, 3000, t)
        lagoon(c, -900, 900, 0, MUD_Y, t)
        if not fixed:                                                # a palace sinking into the mud
            sk = e_in(prog(t, T["sink"], T["sink"] + 1.6))
            c.save()
            c.translate(-60, 380 * sk)
            c.rotate(-7 * sk)
            palace(c, -260, 220, 520, 1, t)
            c.drawRect(R(-260, -10, 480, MUD_Y - 10), P(STONE))
            c.restore()
            bk = prog(t, T["boot"] - 0.3, T["boot"])
            if bk > 0:
                c.save()
                c.translate(500, MUD_Y + 30 + 80 * e_in(prog(t, T["boot"], T["boot"] + 1.2)))
                boot(c, 0, 0, 1.6, a=bk)
                c.restore()
            mud(c, -900, 900, MUD_Y + 10, 3000, t, a=0.85)                # the mud covers what sank
            for i in range(3):
                q = (t * 0.8 + i / 3.0) % 1.0
                c.drawOval(R(-60 - 260 * (0.4 + q), MUD_Y - 8, 520 * (0.4 + q), 16), P("#8B6B4A", 0.5 * (1 - q) * sk, stroke=4))
        else:                                                        # driving piles by hand with a drop weight
            for i in range(5):
                px = -360 + i * 180
                hk = prog(t, T["hammer"] + i * 0.35, T["beat"] + 0.6)
                depth = lerp(-160, MUD_Y + 40 - 30, e_out(hk))
                beat = (t * 1.6 + i * 0.37) % 1.0
                drop = 1 - beat if beat > 0.15 else beat / 0.15
                pile(c, px, depth - 40 - (1 - hk) * 0, PILE_L, w=34)
                if i == 2:                                           # the rig and its drop weight
                    c.drawLine(px - 120, MUD_Y - 2, px, -560, P("#7C4A21", 1, stroke=12))
                    c.drawLine(px + 120, MUD_Y - 2, px, -560, P("#7C4A21", 1, stroke=12))
                    wy = depth - 120 - 260 * drop
                    c.drawLine(px, -560, px, wy, P("#D6D3D1", 1, stroke=3))
                    c.drawRRect(rr(px - 40, wy - 60, 80, 70, 10), P("#57534E"))
                    for sd in (-1, 1):                               # the crew pulling the ropes, singing
                        rx = px + sd * 230
                        c.drawLine(px, -560, rx + sd * -10, -150, P("#D6D3D1", 0.8, stroke=3))
                        person(c, rx, -10 + 0, 150, ["#2563EB", "#DC2626"][sd > 0], t + sd, pose="cheer" if drop > 0.7 else "stand",
                               face=-sd, hat="cap")
                    notes(c, px + 160, -260, t, a=prog(t, T["sings"] - 0.3, T["sings"] + 0.1))
            c.drawRect(R(-900, -20, 1800, 30), P("#8B5E34"))         # a work platform on the water
        c.restore()
        self.ui["cam"] = cam

    def ui_mud(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 380, "soft", T["soft"] - 0.2, T["palace"] - 0.1, accent="#D6B38A", size=44)
            self.chip(540, 380, "sinks", T["palace"] - 0.1, s("fix1") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["boot"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["sink"] + 0.6, 1.4)
            return
        self.chip(540, 380, "hammer", T["hammer"] - 0.1, T["nine"] - 0.1, accent="#FDBA74", size=40)
        k = self.span(T["nine"] - 0.1, T["sings"] - 0.1)
        if k > 0:                                                    # nine piles in one square meter, from above
            c.drawRRect(rr(40, 300, 270, 270, 22), P("#0B1220", 0.9 * k))
            c.drawRect(R(75, 335, 200, 200), P("#D6B38A", 0.9 * k, stroke=4))
            for i in range(3):
                for j in range(3):
                    c.drawCircle(108 + i * 67, 368 + j * 67, 19, P("#C9935A", k))
            v2.chip(c, 175, 615, self.L["nine"], k, accent=HILITE, size=34)
        self.chip(540, 380, "sing", T["sings"] - 0.1, s("break2") - 0.15, accent=HILITE, size=40)
        self.badge("check", T["beat"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: deep (break2, fix2)
    def draw_deep(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        if not fixed:                                                # the piles stop far above the rock
            cam = (0, 520, 0.62)
            vrect(c, 0, 0, W, H, [MUD_D, MUD_D])
            self.view(c, cam)
            c.drawRect(R(-1200, -900, 2400, 900), lin_paint(0, -900, 0, 0, ["#2A2160", "#D2706E"]))
            mud(c, -1200, 1200, MUD_Y, 800, t)
            lagoon(c, -1200, 1200, 0, MUD_Y, t)
            c.drawRect(R(-1200, 800, 2400, 1900), lin_paint(0, 800, 0, 1500, ["#6B6B73", "#3F3F46"]))
            for k in range(14):
                c.drawLine(-1200 + k * 180, 800, -1100 + k * 180, 1000, P("#52525B", 0.7, stroke=4))
            palace(c, -420, 420, 560, 2, t)
            c.drawRect(R(-420, -10, 840, MUD_Y - 34), P(STONE))
            for k in range(26):
                pile(c, -405 + k * 32.4, MUD_Y - 30, PILE_L, w=26)
            gk = prog(t, T["short"] - 0.3, T["rock"])
            if gk > 0:                                               # the gap to the rock
                x = 560
                c.drawLine(x, MUD_Y + PILE_L - 30, x, lerp(MUD_Y + PILE_L - 30, 800, gk), P(WARN, 1, stroke=8))
                for yy, d in ((MUD_Y + PILE_L - 30, -1), (800, 1)):
                    if d < 0 or gk > 0.95:
                        hp = skia.Path()
                        hp.moveTo(x, yy)
                        hp.lineTo(x - 22, yy - 34 * d)
                        hp.lineTo(x + 22, yy - 34 * d)
                        hp.close()
                        c.drawPath(hp, P(WARN, 1))
            c.restore()
            self.ui["cam"] = cam
            return
        vrect(c, 0, 0, W, H, ["#3A2C1E", "#2A2016"])                 # from above: a spiral, outside in
        mud(c, 0, W, 0, H, t, a=0.6)
        n = 9
        order = []
        top, bot, lef, rig = 0, n - 1, 0, n - 1
        while top <= bot and lef <= rig:
            for j in range(lef, rig + 1):
                order.append((top, j))
            for i in range(top + 1, bot + 1):
                order.append((i, rig))
            if top < bot:
                for j in range(rig - 1, lef - 1, -1):
                    order.append((bot, j))
            if lef < rig:
                for i in range(bot - 1, top, -1):
                    order.append((i, lef))
            top, bot, lef, rig = top + 1, bot - 1, lef + 1, rig - 1
        sp = prog(t, s("fix2"), T["squeeze"] - 0.1)
        m = int(len(order) * sp)
        x0, y0, step = 260, 380, 70
        c.drawRect(R(x0 - 50, y0 - 50, step * (n - 1) + 100, step * (n - 1) + 100), P("#D6B38A", 0.8, stroke=5))
        for idx, (i, j) in enumerate(order[:m]):
            px, py = x0 + j * step, y0 + i * step
            fresh = clamp(1 - (idx - m + 6) / 6.0) if idx > m - 6 else 0.0
            c.drawCircle(px, py, 26, P("#C9935A"))
            c.drawCircle(px, py, 26, P("#7A5230", 1, stroke=4))
            if fresh > 0:
                add_glow(c, px, py, 50, "#FDE68A", 0.6 * fresh)
        if m > 1:                                                    # the path of the spiral
            pth = skia.Path()
            for idx, (i, j) in enumerate(order[:m]):
                (pth.moveTo if idx == 0 else pth.lineTo)(x0 + j * step, y0 + i * step)
            c.drawPath(pth, P(HILITE, 0.45, stroke=4))
        qk = prog(t, T["squeeze"] - 0.2, T["squeeze"] + 0.3)
        if qk > 0:                                                   # the mud squeezes in from every side
            cx_, cy_ = x0 + step * 4, y0 + step * 4
            for k in range(8):
                ang = k * math.pi / 4
                r1 = 420 - 40 * math.sin(t * 6) * qk
                c.drawLine(cx_ + math.cos(ang) * r1, cy_ + math.sin(ang) * r1, cx_ + math.cos(ang) * (r1 - 90),
                           cy_ + math.sin(ang) * (r1 - 90), P("#FDBA74", qk, stroke=10))
        fk = prog(t, T["friction"] - 0.2, T["friction"] + 0.2)
        if fk > 0:
            add_glow(c, x0 + step * 4, y0 + step * 4, 380, "#FDE68A", 0.25 * fk)

    def ui_deep(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            cam = self.ui.get("cam", (0, 520, 0.62))
            self.chip(540, 380, "short", T["short"] - 0.2, s("fix2") - 0.15, accent=WARN, size=44)
            rx, ry = self.at(cam, -300, 880)
            self.chip(rx, ry, "rock", T["rock"] - 0.2, s("fix2") - 0.15, accent="#E5E7EB", size=36)
            self.badge("alert", T["rock"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["rock"] + 0.05, 1.3)
            return
        self.chip(540, 1150, "spiral", T["spiral"] - 0.2, T["squeeze"] - 0.1, accent=HILITE, size=38)
        self.chip(540, 1150, "squeeze", T["squeeze"] - 0.1, T["friction"] - 0.1, accent="#FDBA74", size=40)
        self.chip(540, 1150, "friction", T["friction"] - 0.1, s("break3") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["friction"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: rot (break3, fix3)
    def draw_rot(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        if not fixed:                                                # in the air: mushrooms, bugs, it crumbles
            v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=1150)
            c.drawRect(R(0, 1150, W, H - 1150), lin_paint(0, 1150, 0, H, ["#5B4636", "#2A2016"]))
            rk = prog(t, s("break3"), T["rotten"] + 0.6)
            pile(c, 540, 380, 780, w=150, rot_=rk)
            rng = random.Random(3)
            for i in range(int(14 * rk)):
                mushroom(c, 540 + rng.uniform(-60, 60), 480 + rng.uniform(0, 600), rng.uniform(1.2, 2.2))
            for i in range(int(10 * rk)):
                bug(c, 540 + rng.uniform(-70, 70) + math.sin(t * 3 + i) * 10, 450 + rng.uniform(0, 640), 1.6, t)
            if rk > 0.8:
                v2.debris(c, 540, 1100, t, T["rotten"] + 0.3, dur=1.2, n=14, speed=300,
                          cols=("#7A5230", "#5E3B1E", "#3B3328"))
            return
        vrect(c, 0, 0, W, H, ["#1E5E6C", "#123C4A", "#2A2016"])     # down in the water and the mud
        c.drawRect(R(0, 760, W, H - 760), lin_paint(0, 760, 0, H, [MUD, MUD_D]))
        pile(c, 540, 260, 900, w=150, rot_=0.0)
        ak = prog(t, T["air"] - 0.3, T["air"] + 0.1)
        if ak > 0:                                                   # no air: an O2 bubble, crossed out
            c.drawCircle(250, 520, 80, P("#BFDBFE", 0.25 * ak))
            word(c, "O2", 250, 545, 64, "#E0F2FE", a=ak)
            c.drawLine(180, 590, 320, 450, P(WARN, ak, stroke=10))
        bk = prog(t, T["fungi"] - 0.3, T["insects"] + 0.4)
        if bk > 0:                                                   # fungi and bugs try, bounce off, fade
            for i in range(6):
                q = (bk * 1.2 + i * 0.13) % 1.0
                bx = 860 - q * 200
                by = 420 + i * 90
                bug(c, bx, by, 1.6, t, a=(1 - q) * (1 - prog(t, T["centuries"] - 0.4, T["centuries"])))
                mushroom(c, 840, by + 40, 1.3, a=0.6 * (1 - q))
        lk = prog(t, T["centuries"] - 0.3, T["centuries"] + 0.2)
        if lk > 0:
            add_glow(c, 540, 700, 300, "#FDE68A", 0.25 * lk)

    def ui_rot(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "rots", T["rotten"] - 0.4, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["rotten"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["rotten"] + 0.2, 1.3)
            return
        self.chip(540, 1150, "noair", T["air"] - 0.1, T["fungi"] - 0.1, accent="#93C5FD", size=40)
        self.chip(540, 1150, "nobugs", T["fungi"] - 0.1, T["centuries"] - 0.1, accent=GOOD, size=40)
        self.chip(540, 1150, "lasts", T["centuries"] - 0.1, s("break4") - 0.15, accent=HILITE, size=44)
        self.badge("check", T["centuries"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: wall (break4, fix4, cta)
    def draw_wall(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, -40, 1.25)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 20 * z)
        self.view(c, cam)
        fixed = t >= s("fix4") - 0.12
        mud(c, -700, 700, MUD_Y + 40, 2000, t)
        lagoon(c, -700, 700, 0, MUD_Y + 40, t)
        base_y = MUD_Y + 10                                          # top of the boards
        if fixed:
            sk = prog(t, T["saw"] - 0.2, T["saw"] + 0.5)
            for k in range(14):                                      # piles, sawn level
                px = -330 + k * 51
                cut = lerp(base_y - 70 - (k % 4) * 22, base_y, sk)
                pile(c, px, cut, PILE_L + base_y - cut, w=34)
            if 0 < sk < 1:
                sx_ = lerp(-380, 380, sk)
                c.drawRect(R(sx_ - 60, base_y - 16, 120, 10), P("#D1D5DB"))
                for i in range(6):
                    c.drawCircle(sx_ + math.sin(t * 30 + i) * 30, base_y + 10 + i * 6, 4, P("#FDE68A", 0.8))
            bk = prog(t, T["boards"] - 0.3, T["boards"] + 0.3)
            if bk > 0:                                               # two layers of thick boards
                c.drawRect(R(-360, base_y - 22 * bk, 720, 22 * bk), P("#8B5E34"))
                for k in range(8):
                    c.drawLine(-360 + k * 90, base_y - 22 * bk, -360 + k * 90, base_y, P("#5E3B1E", 1, stroke=3))
                c.drawRect(R(-360, base_y - 44 * bk, 720, 22 * bk), P("#9A6B3F"))
            stk = e_out(prog(t, T["stone"] - 0.3, T["stone"] + 0.3))
            stone_top = base_y - 44 - 230 * stk
            if stk > 0:                                              # the band of white stone
                c.drawRect(R(-340, stone_top, 680, base_y - 44 - stone_top), lin_paint(-340, 0, 340, 0, ["#D6D0C2", "#C2BBAB", "#A39C8C"]))
                for k in range(4):
                    yy = base_y - 44 - k * 58
                    if yy > stone_top:
                        c.drawLine(-340, yy, 340, yy, P("#BDB5A5", 1, stroke=2))
            wk = prog(t, T["climb"] - 0.6, T["climb"])
            self.bricks(c, t, -340, stone_top if stk > 0 else base_y - 44, 1.0)
            lv = lerp(0, -30, wk)                                    # the salt stops at the stone
            if stk > 0.9:
                c.drawRect(R(-340, stone_top - 4, 680, 8), P(GOOD, 0.6 * wk))
        else:
            for k in range(14):
                pile(c, -330 + k * 51, base_y, PILE_L, w=34)
            c.drawRect(R(-360, base_y - 44, 720, 44), P("#8B5E34"))
            wet = prog(t, T["bricks"], T["eats"])
            self.bricks(c, t, -340, base_y - 44, 1.0, wet=wet, crumble=prog(t, T["eats"] - 0.3, T["eats"] + 0.6))
        lagoon(c, -700, 700, 0, 6, t)
        c.restore()
        self.ui["cam"] = cam

    def bricks(self, c, t, x0, y_bottom, a, wet=0.0, crumble=0.0):
        """A brick wall from y_bottom up; wet 0..1: salt water creeps up through it; crumble: bricks fall off."""
        rows = 14
        for r_ in range(rows):
            yy = y_bottom - (r_ + 1) * 38
            off = 0 if r_ % 2 == 0 else 40
            for k in range(-1, 9):
                bx = x0 + off + k * 80
                if bx < x0 - 1 or bx + 76 > x0 + 681:
                    continue
                wetk = clamp(wet * 1.6 - r_ / rows * 1.3)
                col = mix("#B5523B", "#4C6C7A", wetk * 0.7)
                dy = 0.0
                if crumble > 0 and r_ < 4 and (k + r_) % 3 == 0:
                    dy = e_in(crumble) * 500
                c.drawRect(R(bx, yy + dy, 76, 34), P(col, a))
                if wetk > 0.3:
                    for i in range(3):
                        c.drawCircle(bx + 14 + i * 22, yy + 28 + dy, 3, P("#F8FAFC", 0.8 * wetk))

    def ui_wall(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 380, "sponge", T["bricks"] - 0.1, T["eats"] - 0.1, accent="#67E8F9", size=40)
            self.chip(540, 380, "eats", T["eats"] - 0.1, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["eats"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["eats"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 380, "saw", T["saw"] - 0.1, T["boards"] - 0.1, accent="#E5E7EB", size=40)
            self.chip(540, 380, "boards", T["boards"] - 0.1, T["stone"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 380, "stone", T["stone"] - 0.1, T["climb"] - 0.1, accent="#F5F3EE", size=40)
            self.chip(540, 380, "dense", T["climb"] - 0.1, s("cta") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["climb"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: cafe (tag)
    def draw_cafe(self, c, t):
        T = self.T
        if not self.rtl:                                             # a café by a canal
            v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=760)
            c.save()
            c.translate(0, 760)
            for i, (x0, x1, h) in enumerate(((-40, 420, 520), (440, 1120, 600))):
                palace(c, x0, x1, h, i + 3, t)
            c.restore()
            lagoon(c, -10, W + 10, 760, 900, t)
            gondola(c, 700, 760, 0.8, t=t)
            c.drawRect(R(0, 900, W, 360), lin_paint(0, 900, 0, 1260, ["#B7A58A", "#8C7B62"]))
            vrect(c, 0, 1240, W, H - 1240, ["#5A4D3C", "#2E271E"])
        else:                                                        # the dining room at home
            room(c, 0, 0, W, 1250, wall="#4A3F5C", floor="#3A3346", t=t, lamp=True, lamp_x=540)
            vrect(c, 0, 1250, W, H - 1250, ["#3A3346", "#1C1824"])
            c.drawRect(R(110, 320, 340, 250), P("#5C3A1A"))           # a framed Venice picture on the wall
            c.save()
            c.clipRect(R(126, 336, 308, 218))
            vrect(c, 126, 336, 308, 218, ["#2A2160", "#D2706E", "#F6B07E"])
            c.translate(280, 520)
            c.scale(0.22, 0.22)
            for i, (x0, x1, h, idx) in enumerate(PALACES[1:3]):
                palace(c, x0 + 300, x1 + 300, h, idx, t)
            c.restore()
        fx_ = prog(t, T["fix_nap"], T["fix_nap"] + 0.4)
        wob = math.sin(t * 14) * 5 * (1 - fx_) * prog(t, T["table"] - 0.4, T["table"])
        ty = 1180
        if not self.rtl:
            table(c, 600, ty, 2.0, t, wob=wob, top="#8D96A3", leg="#4B5563")
        else:
            table(c, 600, ty, 2.0, t, wob=wob, top="#7C4A21", leg="#5C3A1A")
        nk = prog(t, T["fix_nap"] - 0.5, T["fix_nap"])
        if nk > 0:                                                   # the folded napkin slides under one leg
            nx = lerp(200, 460, e_out(nk))
            c.drawRRect(rr(nx - 50, ty - 6, 100, 22, 4), P("#F1F5F9", 1))
            c.drawLine(nx - 50, ty + 5, nx + 50, ty + 5, P("#94A3B8", 1, stroke=3))
            if nk < 1:
                c.drawRRect(rr(nx - 120, ty - 70, 80, 50, 20), P("#E8B48A", 1))
            else:
                add_glow(c, nx, ty + 5, 90, "#FDE68A", 0.5 * (1 - prog(t, T["fix_nap"] + 0.1, T["fix_nap"] + 1.2)))

    def ui_cafe(self, c, t, tw):
        T = self.T
        self.chip(540, 380, "still", T["sticks"] - 0.2, self.duration + 1, accent=GOOD, size=40)
        k = self.span(T["fix_nap"] - 0.1, self.duration + 1)
        if k > 0:
            v2.chip(c, 400, 1080, self.L["napkin"], k, accent=HILITE, size=36)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(1.4, 61), -16), (T["dig"], sfx.whoosh(1.0, False, 62), -10), (T["upside"], sfx.creak(1.0), -10),
              (T["forest"], sfx.thud(0.4), -8), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 63), -9), (T["venice"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 64), -4), (T["sink"], sfx.creak(1.4), -8),
               (T["sink"] + 0.5, rumble(1.6, 65), -10), (T["boot"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["hammer"] + 0.2 + i * 0.62, sfx.thunk(66 + i), -6) for i in range(6)]
        ev += [(T["sings"], sfx.sparkle(0.8, 10, 72), -10), (T["beat"] + 0.1, sfx.ding(), -8), (T["beat"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 73), -4), (T["rock"], sfx.thud(0.5), -8),
               (T["rock"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["spiral"], sfx.whirr(1.4), -14), (T["squeeze"], sfx.creak(0.8), -10),
               (T["friction"] + 0.1, sfx.ding(), -8), (T["friction"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["rotten"], sfx.snap(75), -8),
               (T["rotten"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["air"], sfx.pop(76), -8), (T["fungi"], sfx.hiss(0.8, 77), -16), (T["centuries"] + 0.1, sfx.ding(), -8),
               (T["centuries"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["sponge"], sfx.hiss(1.2, 79), -12),
               (T["eats"], sfx.thud(0.4), -8), (T["eats"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["saw"], sfx.sizzle(0.6, 80), -10), (T["boards"], sfx.thunk(81), -6), (T["stone"], sfx.thud(0.5), -6),
               (T["climb"] + 0.1, sfx.ding(), -8), (T["climb"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(82), 0), (T["follow"] - 0.15, sfx.pop(83), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 84), -6), (T["palaces"], sfx.sparkle(0.8, 10, 85), -8),
               (T["canals"], sfx.hiss(1.0, 86), -14), (T["bridges"], sfx.thud(0.4), -8), (T["swap"] + 0.35, sfx.pop(87), -6)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, False, 88), -6), (T["s1"], sfx.pop(89), -3), (T["s2"], sfx.pop(90), -3),
               (T["s3"], sfx.pop(91), -3)]
        ev += [(T["cong2"], sfx.pop(92), -2), (T["cong2"], sfx.sparkle(1.0, 14, 93), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 94), -6), (T["table"], sfx.tap(95), -8), (T["table"] + 0.2, sfx.tap(96), -8),
               (T["fix_nap"], sfx.whoosh(0.3, False, 97), -10), (T["fix_nap"] + 0.4, sfx.ding(), -8)]
        return ev


def carbody(c, x, y, s=1.0, col="#EF4444"):
    """A small car from the side, wheels on y."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-60, -46, 120, 30, 10), P(col))
    c.drawRRect(rr(-36, -70, 66, 28, 10), P(shade(col, -0.15)))
    c.drawRRect(rr(-30, -64, 24, 18, 4), P("#BFE6FF"))
    c.drawRRect(rr(0, -64, 24, 18, 4), P("#BFE6FF"))
    for wx in (-36, 36):
        c.drawCircle(wx, -14, 14, P("#111827"))
    c.restore()


NAME = "venice"
EPISODE = Venice
