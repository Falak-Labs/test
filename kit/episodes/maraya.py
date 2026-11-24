"""Episode 74 - Maraya, the mirrored concert hall in AlUla (the largest mirrored building in the world).  v2 look: a
desert valley in elevation between sandstone cliffs (sand floor y = 0); the hall is a plain box whose four walls are
covered in mirror panels, so it shows the cliffs and the sky behind you and seems to vanish.

Sets: valley (hook: the mirror box between the cliffs, a hiker walks past and only sees the canyon, the box flickers
out of sight; break1: a plain concrete box spoils the view, "?"; fix1: mirror panels go on row by row and the box
melts into the rocks; break2: noon sun, the box glows hot like an oven, a thermometer; fix2: the rays bounce off the
mirror back up to the sky, the thermometer drops; reveal: panels counted up to almost 10,000 m2; stat; closer: sunset
in the mirror, then the hall lit inside), panel (break3: glass grows in the day and shrinks at night and cracks; fix3:
a gap around every panel, they slide; break4: a sandstorm dulls the mirror; fix4: a tough coating, the sand bounces
off), home (tag: you hide behind a mirror; mom still finds you for the dishes / the corner shop).
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of  # noqa: E402
from windtower import sun, heat_lines  # noqa: E402
from bigben import thermometer  # noqa: E402

GOLDP = {"top": "#1B3A6E", "upper": "#2F5D99", "mid": "#5D86B8", "low": "#E4A877", "horizon": "#F7C98E",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NOONP = {"top": "#0E2F5E", "upper": "#1B4F8F", "mid": "#2A62A4", "low": "#3E7AB8", "horizon": "#7FB2DE",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SUNSETP = {"top": "#1A1440", "upper": "#3B2A6A", "mid": "#8A4A7A", "low": "#E07A4E", "horizon": "#FFB061",
           "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP2 = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2E3570", "horizon": "#4A4A8A",
           "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
ROCK = ("#D07848", "#9A4A2E", "#5E2A1C")         # sandstone: lit, mid, shade
SAND = ("#C98E58", "#8E5A30")
BW, BH = 200.0, 230.0                            # the hall: half width, height (world units)
CONCRETE = ("#B9B2A6", "#8E877C")


def cliff_shape(side, seed, inner, outer, top):
    """A rounded sandstone outcrop (world): side -1 = on the left (inner edge on its right), 1 = on the right."""
    rng = random.Random(seed)
    p = skia.Path()
    p.moveTo(inner, 40)
    y = 0.0
    x = inner
    while y > top + 90:                                                     # the inner wall, bulging
        ny = y - rng.uniform(70, 120)
        nx = inner - side * rng.uniform(-10, 34)
        p.quadTo(x - side * rng.uniform(10, 40), (y + ny) / 2, nx, ny)
        x, y = nx, ny
    n = 6
    for i in range(1, n + 1):                                               # the rounded top
        nx = lerp(inner, outer, i / n)
        ny = top + rng.uniform(-50, 50) + abs(i - 2) * 10
        p.quadTo((x + nx) / 2, min(y, ny) - rng.uniform(30, 70), nx, ny)
        x, y = nx, ny
    p.lineTo(outer, 40)
    p.close()
    return p


def acacia(c, x, y, s, tone=0.0, a=1.0):
    c.drawLine(x, y, x - 4 * s, y - 40 * s, P(mix("#5A3A22", "#1A1428", tone), a, stroke=5 * s))
    c.drawOval(R(x - 46 * s, y - 62 * s, 92 * s, 26 * s), P(mix("#5E7A3A", "#1E2A2A", tone), a))


def landscape(c, t, tone=0.0, flip=False, pal_k=0.0):
    """The valley: rounded sandstone cliffs on both sides, a far mesa, the sand floor (world). tone 0 day .. 1 night."""
    if flip:
        c.save()
        c.scale(-1, 1)
    rng = random.Random(3)
    far = path_of([(-1800, 0), (-1500, -260), (-1100, -300), (-900, -220), (-600, -240), (-300, -170), (100, -210),
                   (500, -190), (900, -280), (1300, -250), (1800, -320), (1800, 0)], close=True)
    c.drawPath(far, P(mix("#9A5E4A", "#2A2550", tone), 0.9))
    for side, seed, inner, outer, top in ((-1, 5, -175, -1200, -520), (1, 7, 175, 1200, -560)):
        p = cliff_shape(side, seed, inner, outer, top)
        c.drawPath(p, lin_paint(0, top - 60, 0, 0, [mix(ROCK[0], "#3A2A50", tone), mix(ROCK[1], "#2A1E40", tone),
                                                     mix(ROCK[2], "#1A1430", tone)]))
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        for k in range(10):                                                 # layers in the rock
            yy = top + 40 + k * 56
            c.drawLine(inner - 400, yy + rng.uniform(-8, 8), inner + 400 * -side + side * 0, yy + rng.uniform(-8, 8),
                       P(mix("#4A1E14", "#140F24", tone), 0.30, stroke=4))
            c.drawLine(inner - 1200, yy, inner + 1200, yy + 6, P(mix("#4A1E14", "#140F24", tone), 0.25, stroke=3))
        for k in range(7):                                                  # vertical cracks
            xx = inner + side * rng.uniform(30, 600)
            c.drawLine(xx, top - 40, xx + rng.uniform(-30, 30), 0, P(mix("#3A140C", "#120D20", tone), 0.4, stroke=5))
        c.drawRect(R(inner - (40 if side > 0 else -10), top - 100, 50 * -side if side < 0 else 50, -top + 100),
                   P(mix("#F2A070", "#3A2A60", tone), 0.18))                # sunlit inner edge
        c.restore()
    c.drawRect(R(-2400, 0, 4800, 1600), lin_paint(0, 0, 0, 700, [mix(SAND[0], "#2A2448", tone), mix(SAND[1], "#141026", tone)]))
    for k in range(5):
        yy = 30 + k * 60
        p = skia.Path()
        p.moveTo(-2400, yy)
        xx = -2400.0
        while xx < 2400:
            xx += 120
            p.lineTo(xx, yy + math.sin(xx * 0.004 + k) * 12)
        c.drawPath(p, P(mix("#E8B98A", "#3A3460", tone), 0.3, stroke=3))
    for x, sc in ((-280, 0.9), (250, 1.1), (-420, 0.7), (380, 0.8)):
        acacia(c, x, 4, sc, tone)
    for k in range(10):
        rx = rng.uniform(-600, 600)
        c.drawOval(R(rx, 30 + rng.uniform(0, 160), rng.uniform(12, 30), rng.uniform(6, 12)), P(mix("#7A4A2A", "#1A1428", tone), 0.8))
    if flip:
        c.restore()


def hall(c, t, cam_x, mirror=1.0, tone=0.0, sky_pal=None, heat=0.0, panels=1.0, lit=0.0, sheen=0.0, a=1.0, gy=0.0,
         fade=0.0):
    """The hall (world): a box from -BW..BW, -BH..0. mirror 0 = bare concrete, 1 = all mirror. panels 0..1 how many
    mirror panels are on (row by row from the top). fade 0..1 = how much the mirror melts into the landscape."""
    if a <= 0:
        return
    box_r = R(-BW, -BH, BW * 2, BH)
    c.drawRect(box_r, lin_paint(-BW, 0, BW, 0, [mix(CONCRETE[0], "#3A3650", tone), mix(CONCRETE[1], "#2A2640", tone)], a=a))
    if heat > 0:
        c.drawRect(box_r, P("#FF5A2A", 0.45 * heat * a))
        add_glow(c, 0, -BH / 2, 380, "#FF7A3D", 0.35 * heat * a)
    if mirror > 0 and panels > 0:
        rows = 6
        shown_h = BH * clamp(panels)
        c.save()
        cp = skia.Path()
        cp.addRect(R(-BW, -BH, BW * 2, shown_h))
        c.clipPath(cp, skia.ClipOp.kIntersect, True)
        # what the mirror shows: the valley behind you (the landscape flipped, a little darker and bluer)
        c.saveLayerAlpha(None, int(255 * a * mirror))
        if sky_pal is not None:
            c.save()
            c.resetMatrix()
            v2.sky(c, W, H, 0.0, pal=sky_pal, horizon_y=gy)
            c.restore()
        c.save()
        c.translate(cam_x * 0.25, 0)
        landscape(c, t, tone=tone, flip=True)
        c.restore()
        c.drawRect(box_r, P("#9CC3E6", 0.10 * (1 - fade)))
        c.restore()
        # panel seams
        cols = 12
        for i in range(1, cols):
            x = -BW + i * BW * 2 / cols
            c.drawLine(x, -BH, x, 0, P("#F8FAFC", (0.22 - 0.14 * fade) * a, stroke=1.5))
        for j in range(1, rows):
            y = -BH + j * BH / rows
            c.drawLine(-BW, y, BW, y, P("#F8FAFC", (0.22 - 0.14 * fade) * a, stroke=1.5))
        if sheen > 0:                                                       # a light sweep across the glass
            sx = lerp(-BW - 200, BW + 200, (t * 0.35) % 1.0)
            sp = lin_paint(sx - 80, 0, sx + 80, 0, [("#FFFFFF", 0.0), ("#FFFFFF", 0.45 * sheen), ("#FFFFFF", 0.0)], a=a)
            sp.setBlendMode(PLUS)
            c.drawPath(path_of([(sx - 60, -BH), (sx + 40, -BH), (sx - 20, 0), (sx - 120, 0)], close=True), sp)
        c.restore()
        if panels < 1:                                                      # the row being fitted
            yy = -BH + shown_h
            c.drawLine(-BW, yy, BW, yy, P("#FDE68A", 0.9 * a, stroke=3))
    c.drawRect(box_r, P(mix("#E5E7EB", "#94A3B8", tone), (0.5 - 0.42 * fade) * a, stroke=3))
    if lit > 0:                                                             # night: the hall glows from its doors
        c.drawRect(R(-40, -60, 80, 60), P("#FFD58A", lit * a))
        add_glow(c, 0, -30, 160, "#FFC470", 0.5 * lit * a)
        c.drawRect(R(-BW, -2, BW * 2, 4), P("#FFD58A", 0.7 * lit * a))


def ray(c, x0, y0, x1, y1, col, a=1.0, w=6, head=18):
    if a <= 0:
        return
    c.drawLine(x0, y0, x1, y1, P(col, a, stroke=w))
    an = math.atan2(y1 - y0, x1 - x0)
    hp = path_of([(x1, y1), (x1 - math.cos(an - 0.5) * head, y1 - math.sin(an - 0.5) * head),
                  (x1 - math.cos(an + 0.5) * head, y1 - math.sin(an + 0.5) * head)], close=True)
    c.drawPath(hp, P(col, a))


def hiker(c, x, y, h, t, a=1.0, face=1, look=0.0):
    person(c, x, y, h, "#0EA5E9", t, pose="walk" if look < 0.5 else "look", face=face, hat="cap", a=a)
    u = h / 140.0
    c.drawRRect(rr(x - 34 * u * face - 10 * u, y - 112 * u, 22 * u, 40 * u, 6 * u), P("#F97316", a))   # backpack


# ====================================================================================== the episode
class Maraya(EpisodeV2):
    BUILD_NO = 74
    FIRST_SET = "valley"
    CLEAR = "#0B1220"
    TITLE = {"en": "MARAYA", "ar_sa": "مرايا العلا"}
    EMPH = {"en": ["CONGRATS", "MIRRORS", "VANISHES", "MARAYA", "YOURSELF", "BOX", "SPOIL", "VALLEY", "MIRROR", "FOUR",
                   "ROCKS", "SKY", "SUN", "BAKE", "OVEN", "BOUNCE", "HEAT", "HOT", "COLD", "CRACK", "PANEL", "GAP",
                   "MOVE", "SANDSTORMS", "DULL", "COATING", "SAND", "FOLLOW", "WELL", "STEPS", "TEN", "THOUSAND",
                   "SQUARE", "METERS", "EARTH", "FIVE", "HUNDRED", "SEATS", "GUINNESS", "RECORD", "VANISH", "DISHES"],
            "ar_sa": ["مبروك", "مرايا", "يختفي", "العلا", "بيدك", "مبنى", "بيخرّب", "الوادي", "مراية", "الأربعة", "الجبال",
                      "شمس", "بتطبخ", "الفرن", "ترد", "وحرارتها", "حر", "برد", "ينكسر", "لوح", "فراغ", "يتحرك", "العواصف",
                      "لمعتها", "طبقة", "والرمل", "تابعني", "بير", "عشرة", "آلاف", "متر", "بالعالم", "خمسمية", "كرسي",
                      "غينيس", "تختفي", "البقالة"]}
    KEYS = {"ar_sa": {
        ("hook", "WRAP"): "تلبّس", ("hook", "MIRRORS"): "مرايا", ("hook", "VANISHES"): "يختفي",
        ("hook", "CONGRATS"): "مبروك", ("hook", "MARAYA"): "العلا",
        ("break1", "BOX"): "مبنى", ("break1", "SPOIL"): "بيخرّب", ("break1", "VALLEY"): "الوادي", ("break1", "MUCH"): "مراية",
        ("fix1", "COVER"): "فتغطي", ("fix1", "FOUR"): "الأربعة", ("fix1", "ROCKS"): "الجبال", ("fix1", "INSTEAD"): "بدال",
        ("break2", "SUN"): "شمس", ("break2", "BAKE"): "بتطبخ", ("break2", "OVEN"): "الفرن",
        ("fix2", "BOUNCE"): "ترد", ("fix2", "HEAT"): "حرارت", ("fix2", "SKY"): "للسما",
        ("break3", "HOT"): "بالنهار", ("break3", "COLD"): "وبرد", ("break3", "GROWS"): "يكبر", ("break3", "CRACK"): "ينكسر",
        ("fix3", "PANEL"): "لوح", ("fix3", "GAP"): "فراغ", ("fix3", "MOVE"): "يتحرك",
        ("break4", "SANDSTORMS"): "العواصف", ("break4", "DULL"): "وتطفي",
        ("fix4", "COATING"): "طبقة", ("fix4", "SAND"): "والرمل",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "TEN"): "عشرة", ("reveal", "MOST"): "أكبر", ("reveal", "EARTH"): "بالعالم",
        ("stat", "FIVE"): "خمسمية", ("stat", "FOUR"): "وأربع", ("stat", "GUINNESS"): "غينيس",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "VANISH"): "يختفي", ("tag", "TURN"): "أمك", ("tag", "DISHES"): "البقالة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a well with 3,500 steps"),
                   "stat": [("500", "SEATS"), ("4", "MIRROR WALLS"), ("#1", "LARGEST IN THE WORLD")],
                   "L": {"name": "MARAYA, ALULA", "means": "MARAYA = MIRRORS", "box": "A BIG BOX IN THE VIEW",
                         "much": "HOW MUCH MIRROR?", "cover": "4 MIRROR WALLS", "gone": "IT SHOWS THE ROCKS",
                         "sun": "DESERT SUN", "oven": "AN OVEN", "bounce": "SUN BOUNCES BACK", "cool": "COOLER INSIDE",
                         "day": "DAY: HOT", "night": "NIGHT: COLD", "grow": "GLASS GROWS & SHRINKS", "crack": "CRACK!",
                         "gap": "A GAP AROUND EVERY PANEL", "storm": "SANDSTORM", "dull": "SCRATCHED & DULL",
                         "coat": "TOUGH COATING", "shine": "SHINY AGAIN", "area": "9,740 m² OF MIRROR",
                         "record": "LARGEST MIRRORED BUILDING", "you": "MOM: DISHES!", "feet": "FOUND YOU"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: بير فيه 3500 درجة"),
                      "stat": [("500", "كرسي"), ("4", "جدران مرايا"), ("#1", "الأكبر بالعالم")],
                      "L": {"name": "مرايا العلا", "means": "مرايا", "box": "صندوق يخرّب المنظر",
                            "much": "كم مراية تحتاج؟", "cover": "4 جدران مرايا", "gone": "تبين الجبال بداله",
                            "sun": "شمس الصحرا", "oven": "فرن!", "bounce": "الشمس ترتد للسما", "cool": "أبرد من داخل",
                            "day": "النهار: حر", "night": "الليل: برد", "grow": "القزاز يكبر وينكمش", "crack": "انكسر!",
                            "gap": "فراغ حول كل لوح", "storm": "عاصفة رملية", "dull": "مخدوش وطافي",
                            "coat": "طبقة قوية", "shine": "يلمع من جديد", "area": "9740 متر مربع مرايا",
                            "record": "أكبر مبنى مرايا بالعالم", "you": "أمك: مين يروح البقالة؟", "feet": "شافتك!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "wrap": ("hook", "WRAP", 0.15), "mirrors": ("hook", "MIRRORS", 0.3), "vanishes": ("hook", "VANISHES", 0.45),
            "congrats": ("hook", "CONGRATS", 0.6), "name": ("hook", "MARAYA", 0.9),
            "box": ("break1", "BOX", 0.15), "spoil": ("break1", "SPOIL", 0.3), "valley": ("break1", "VALLEY", 0.45),
            "much": ("break1", "MUCH", 0.8),
            "cover": ("fix1", "COVER", 0.1), "four": ("fix1", "FOUR", 0.25), "rocks": ("fix1", "ROCKS", 0.6),
            "instead": ("fix1", "INSTEAD", 0.85),
            "sun": ("break2", "SUN", 0.2), "bake": ("break2", "BAKE", 0.55), "oven": ("break2", "OVEN", 0.9),
            "bounce": ("fix2", "BOUNCE", 0.25), "heat": ("fix2", "HEAT", 0.6), "sky": ("fix2", "SKY", 0.92),
            "hot": ("break3", "HOT", 0.2), "cold": ("break3", "COLD", 0.4), "grows": ("break3", "GROWS", 0.65),
            "crack": ("break3", "CRACK", 0.92),
            "panel": ("fix3", "PANEL", 0.15), "gap": ("fix3", "GAP", 0.45), "move": ("fix3", "MOVE", 0.8),
            "storms": ("break4", "SANDSTORMS", 0.15), "dull": ("break4", "DULL", 0.9),
            "coating": ("fix4", "COATING", 0.4), "sand": ("fix4", "SAND", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "ten": ("reveal", "TEN", 0.3), "most": ("reveal", "MOST", 0.65), "earth": ("reveal", "EARTH", 0.92),
            "s1": ("stat", "FIVE", 0.05), "s2": ("stat", "FOUR", 0.35), "s3": ("stat", "GUINNESS", 0.6),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_vanish": ("tag", "VANISH", 0.15), "t_turn": ("tag", "TURN", 0.6), "t_dishes": ("tag", "DISHES", 0.9)})
        T["spoil1"] = max(T["spoil"], T["box"], T["valley"]) + 0.15
        T["instead1"] = max(T["instead"], T["rocks"]) + 0.2
        T["oven1"] = max(T["oven"], T["bake"]) + 0.15
        T["sky1"] = max(T["sky"], T["heat"], T["bounce"]) + 0.2
        T["crack1"] = max(T["crack"], T["grows"]) + 0.1
        T["move1"] = max(T["move"], T["gap"]) + 0.2
        T["dull1"] = max(T["dull"], T["storms"]) + 0.15
        T["sand1"] = max(T["sand"], T["coating"]) + 0.2
        # ---- sets
        self.cut(s("break3") - 0.12, "panel", 1)
        self.cut(s("reveal") - 0.12, "valley", -1)
        self.cut(s("tag") - 0.2, "home", 1)
        # ---- valley camera
        FULL = (0, -150, 1.8)
        cm = Camera(70, -120, 3.4)
        cm.key(0.05, 40, -120, 3.1, 1.2)
        cm.key(max(1.2, T["congrats"] - 0.8), *FULL, max(1.0, T["name"] - T["congrats"] + 0.9))
        cm.key(s("break1") - 0.12, *FULL, 0.0)
        cm.key(s("fix1") + 0.2, 0, -130, 2.2, 1.2)
        cm.key(T["instead"] - 0.2, *FULL, 1.0)
        cm.key(s("break2") - 0.12, *FULL, 0.0)
        cm.key(s("reveal") - 0.12, 0, -110, 2.6, 0.0)
        cm.key(s("reveal") + 0.3, *FULL, 1.6)
        cm.key(s("stat") - 0.12, 0, -175, 1.55, 1.2)
        cm.key(s("closer") - 0.12, *FULL, 0.8)
        self.cam = cm
        self.spans = [(T["spoil1"], T["instead1"] + 0.3), (T["oven1"], T["sky1"] + 0.3), (T["crack1"], T["move1"] + 0.3),
                      (T["dull1"], T["sand1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["spoil1"], 0.35, 6), (T["oven1"], 0.35, 6), (T["crack1"], 0.45, 10),
                       (T["dull1"], 0.5, 8), (s("closer") + 0.2, 0.35, 8), (T["t_dishes"], 0.3, 6)]

    # ------------------------------------------------------------------ set: valley
    def phase(self, t):
        s = self.tl.s
        for lab in ("closer", "stat", "reveal", "break3", "fix2", "break2", "fix1", "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    def draw_valley(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        ph = self.phase(t)
        gy = self.to_screen(cam, 0, 0)[1]
        tone = 0.0
        pal = GOLDP
        if ph in ("break2", "fix2"):
            pal = NOONP
        elif ph == "stat":
            pal = SUNSETP
        elif ph == "closer":
            pal = SUNSETP
            tone = 0.0
        night = prog(t, s("closer") + 0.6, s("closer") + 2.0) if ph == "closer" else 0.0
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=gy)
        if night > 0:
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=NIGHTP2, horizon_y=gy)
            c.restore()
            v2.stars(c, W, H, t, 0.8 * night)
        if ph in ("break2", "fix2"):
            hk = prog(t, T["sun"] - 0.3, T["sun"] + 0.3)
            sun(c, 760, 470, 60, heat=0.7 + 0.5 * hk)
        elif ph in ("hook", "break1", "fix1", "reveal"):
            sun(c, 880, gy - 820, 40, heat=0.4)
        self.view(c, cam)
        tone_l = max(tone, 0.75 * night)
        landscape(c, t, tone=tone_l)
        mirror, panels, fade, heat, sheen, lit = 1.0, 1.0, 0.85, 0.0, 0.6, 0.0
        if ph == "hook":
            fade = 0.6 + 0.35 * prog(t, T["vanishes"] - 0.3, T["vanishes"] + 0.5)
            sheen = 1.0
        elif ph == "break1":
            mirror = 0.0
        elif ph == "fix1":
            panels = e_io(prog(t, T["cover"] - 0.2, T["rocks"] + 0.2))
            fade = prog(t, T["rocks"] - 0.2, T["instead"] + 0.3) * 0.9
            sheen = 0.5
        elif ph == "break2":
            mirror = 0.0
            heat = prog(t, T["bake"] - 0.3, T["oven1"] + 0.3)
        elif ph == "fix2":
            fade = 0.75
            heat = 1 - prog(t, T["bounce"], T["sky1"])
        elif ph == "reveal":
            fade = 0.4
            sheen = 0.8
        elif ph == "closer":
            lit = night
            fade = 0.8
        pal_m = pal if night < 0.5 else NIGHTP2
        hall(c, t, cam[0], mirror=mirror, tone=tone_l, sky_pal=pal_m, heat=heat, panels=panels, lit=lit, sheen=sheen,
             gy=gy, fade=fade)
        # people
        if ph == "hook":
            u = prog(t, 0.0, s("break1"))
            hiker(c, lerp(-300, -240, u), 0, 42, t, face=1, look=prog(t, T["vanishes"], T["vanishes"] + 0.3))
        elif ph == "break1":
            hk = prog(t, T["spoil"] - 0.3, T["spoil"])
            hiker(c, -260, 0, 42, t, face=1, look=1.0)
            if hk > 0:                                                      # a big red cross over the box
                c.drawLine(-BW + 30, -BH + 20, BW - 30, -20, P(WARN, 0.85 * hk, stroke=12))
                c.drawLine(BW - 30, -BH + 20, -BW + 30, -20, P(WARN, 0.85 * hk, stroke=12))
        elif ph == "fix2":
            for i in range(5):                                              # sun rays hit the mirror and bounce up
                y = -BH + 30 + i * 40
                k = prog(t, T["bounce"] - 0.5 + i * 0.08, T["bounce"] + 0.3 + i * 0.08)
                ray(c, -320, y - 260, -BW + 4, y, "#FDE68A", a=0.9 * k, w=5)
                ray(c, -BW + 4, y, -320, y + 140 - 420, "#FFF7D6", a=0.9 * prog(t, T["heat"] - 0.4 + i * 0.08, T["heat"] + 0.2 + i * 0.08), w=5)
        elif ph == "break2":
            heat_lines(c, -BW, BW, -BH - 160, -BH, t, a=0.8 * heat)
        elif ph == "closer":
            for i, px in enumerate((-150, -80, 70, 140)):
                person(c, px, 0, 34, ("#F59E0B", "#DB2777", "#16A34A", "#2563EB")[i], t + i, pose="walk", face=1 if i % 2 else -1,
                       a=prog(t, s("closer"), s("closer") + 0.5))
        c.restore()
        self.ui["cam"] = cam
        self.ui["heat"] = heat

    def ui_valley(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "means", T["mirrors"] - 0.2, T["congrats"] - 0.15, accent="#CBD5E1", size=44)
            self.chip(540, 300, "name", T["congrats"] - 0.15, s("break1") + 0.1, accent=HILITE, size=50)
            return
        if ph == "break1":
            self.chip(540, 300, "box", T["box"] - 0.1, T["much"] - 0.15, accent=WARN, size=44)
            self.chip(540, 300, "much", T["much"] - 0.15, s("fix1") - 0.15, accent=HILITE, size=48)
            self.badge("alert", T["spoil1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["spoil1"], 1.2)
            return
        if ph == "fix1":
            self.chip(540, 300, "cover", T["cover"] - 0.1, T["rocks"] - 0.2, accent="#93C5FD", size=48)
            self.chip(540, 300, "gone", T["rocks"] - 0.2, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["instead1"] + 0.1, s("break2") - 0.15, x=920, y=440)
            return
        if ph == "break2":
            self.chip(540, 300, "sun", T["sun"] - 0.2, T["bake"] - 0.1, accent=WARN, size=46)
            self.chip(540, 300, "oven", T["bake"] - 0.1, s("fix2") - 0.15, accent=WARN, size=52)
            k = self.span(T["sun"], s("fix2") + 1.0)
            if k > 0:
                thermometer(c, 900, 760, 1.2, 0.55 + 0.4 * self.ui.get("heat", 0.0), hot=True, a=k)
            self.badge("alert", T["oven1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["oven1"], 1.2)
            return
        if ph == "fix2":
            self.chip(540, 300, "bounce", T["bounce"] - 0.2, T["sky"] - 0.2, accent=HILITE, size=46)
            self.chip(540, 300, "cool", T["sky"] - 0.2, s("break3") - 0.15, accent=GOOD, size=46)
            k = self.span(s("fix2") - 0.1, s("break3") - 0.15)
            if k > 0:
                thermometer(c, 900, 760, 1.2, 0.55 + 0.4 * self.ui.get("heat", 0.0), hot=False, a=k)
            self.badge("check", T["sky1"] + 0.1, s("break3") - 0.15, x=920, y=440)
            return
        if ph == "reveal":
            n = prog(tw, T["ten"] - 0.4, T["most"])
            k = self.span(T["ten"] - 0.3, s("stat") - 0.15)
            if k > 0:
                v2.chip(c, 540, 300, ("%s m²" % format(int(9740 * n), ",")) if not self.rtl else ("%d متر مربع" % int(9740 * n)),
                        k, accent=HILITE, size=56)
            self.chip(540, 420, "record", T["most"] - 0.2, s("stat") - 0.15, accent=GOOD, size=40)

    # ------------------------------------------------------------------ set: panel (break3 .. fix4, cta)
    def draw_panel(self, c, t):
        T, s = self.T, self.tl.s
        b3, f3, b4, f4 = s("break3") - 0.12, s("fix3") - 0.12, s("break4") - 0.12, s("fix4") - 0.12
        day = 0.5 + 0.5 * math.sin((t - b3) * 2.4) if b3 <= t < f3 else 1.0
        vrect(c, 0, 0, W, H, [mix("#0B1440", "#2F6DB0", day), mix("#1A1640", "#E4A877", day)])
        if b3 <= t < f3:
            sun(c, 180, 360, 44, heat=0.6, a=day)
            v2.moon(c, 900, 360, 40, a=1 - day)
        # a steel frame with 2 x 3 mirror panels, big
        x0, y0, pw, ph_, gap = 150, 470, 380, 230, 8
        fixed3 = t >= f3
        gapk = prog(t, T["gap"] - 0.3, T["gap"] + 0.3) if fixed3 else 0.0
        g = gap + 22 * gapk
        c.drawRect(R(x0 - 30, y0 - 30, pw * 2 + 60 + 22, ph_ * 3 + 60 + 44), P("#475569"))
        storm = prog(t, T["storms"] - 0.3, T["storms"] + 0.3) if b4 <= t < f4 else 0.0
        dull = prog(t, T["storms"], T["dull1"]) if b4 <= t < f4 else 0.0
        coat = prog(t, T["coating"] - 0.4, T["coating"] + 0.4) if t >= f4 else 0.0
        if t >= f4:
            dull = 1 - coat
        grow = 0.0
        if b3 <= t < f3:
            grow = math.sin((t - b3) * 2.4) * prog(t, T["hot"] - 0.4, T["grows"])
        elif fixed3 and t < b4:
            grow = math.sin((t - f3) * 2.4) * 0.9
        cracked = prog(t, T["crack1"] - 0.1, T["crack1"] + 0.2) if b3 <= t < f3 else 0.0
        for j in range(3):
            for i in range(2):
                ex = grow * (6 + 10 * (1 - gapk))
                px = x0 + i * (pw + g) - ex
                py = y0 + j * (ph_ + g) - ex
                rw, rh = pw + 2 * ex, ph_ + 2 * ex
                c.save()
                cp = skia.Path()
                cp.addRect(R(px, py, rw, rh))
                c.clipPath(cp, skia.ClipOp.kIntersect, True)
                c.drawRect(R(px, py, rw, rh), lin_paint(px, py, px + rw, py + rh, [mix("#7FB2DE", "#9A9A92", dull),
                                                                                    mix("#C7E2F5", "#B5AFA0", dull),
                                                                                    mix("#E9B783", "#8C8577", dull)]))
                c.drawPath(path_of([(px + rw * 0.1, py), (px + rw * 0.35, py), (px + rw * 0.05, py + rh), (px - rw * 0.2, py + rh)],
                                   close=True), P("#FFFFFF", 0.35 * (1 - dull)))
                if dull > 0:
                    rng = random.Random(i * 3 + j)
                    for k in range(int(40 * dull)):
                        sx_, sy_ = px + rng.uniform(0, rw), py + rng.uniform(0, rh)
                        c.drawLine(sx_, sy_, sx_ + rng.uniform(-30, 30), sy_ + rng.uniform(-6, 6), P("#F1F5F9", 0.5 * dull, stroke=2))
                c.restore()
                c.drawRect(R(px, py, rw, rh), P("#CBD5E1", 1.0, stroke=4))
                if cracked > 0 and i == 1 and j == 1:
                    cx_, cy_ = px + rw * 0.4, py + rh * 0.5
                    rng = random.Random(9)
                    for k in range(7):
                        an = k * 0.9 + 0.3
                        L = rng.uniform(80, 200) * cracked
                        c.drawLine(cx_, cy_, cx_ + math.cos(an) * L, cy_ + math.sin(an) * L, P("#FFFFFF", 0.95, stroke=4))
                if coat > 0:
                    pa = P("#7DD3FC", 0.25 * coat)
                    c.drawRect(R(px, py, rw * coat, rh), pa)
        # the gaps glow when they appear
        if gapk > 0 and t < b4:
            for j in range(3):
                for i in range(2):
                    px = x0 + i * (pw + g)
                    py = y0 + j * (ph_ + g)
                    c.drawRect(R(px - g * 0.5, py - g * 0.5, pw + g, ph_ + g), P(GOOD, 0.8 * gapk, stroke=4))
        # sand
        if storm > 0 or coat > 0:
            rng = random.Random(4)
            n = 160
            for k in range(n):
                u = (t * (0.6 + rng.random() * 0.6) + rng.random()) % 1.0
                yy = rng.uniform(450, 1300)
                xx = lerp(-80, W + 80, u)
                if coat > 0.5 and xx > x0 - 20:                              # bounces off the coating
                    xx = x0 - 20 - (xx - x0) * 0.4
                c.drawCircle(xx, yy, rng.uniform(2, 5), P("#E9B783", 0.8 * max(storm, coat)))
            if storm > 0 and t < f4:
                c.drawRect(R(0, 0, W, H), P("#C98A55", 0.18 * storm))
        self.ui["day"] = day

    def ui_panel(self, c, t, tw):
        T, s = self.T, self.tl.s
        b3, f3, b4, f4 = s("break3") - 0.12, s("fix3") - 0.12, s("break4") - 0.12, s("fix4") - 0.12
        if tw < f3:
            day = self.ui.get("day", 1.0)
            k = self.span(T["hot"] - 0.2, T["grows"] - 0.1)
            v2.chip(c, 540, 300, self.L["day"] if day > 0.5 else self.L["night"], k, accent=WARN if day > 0.5 else "#93C5FD", size=46)
            self.chip(540, 300, "grow", T["grows"] - 0.1, T["crack1"] + 0.1, accent=HILITE, size=44)
            self.chip(540, 300, "crack", T["crack1"] + 0.1, s("fix3") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["crack1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["crack1"], 1.2)
            return
        if tw < b4:
            self.chip(540, 300, "gap", T["panel"] - 0.1, s("break4") - 0.15, accent=GOOD, size=42)
            self.badge("check", T["move1"] + 0.1, s("break4") - 0.15, x=920, y=440)
            return
        if tw < f4:
            self.chip(540, 300, "storm", T["storms"] - 0.2, T["dull"] - 0.2, accent=WARN, size=50)
            self.chip(540, 300, "dull", T["dull"] - 0.2, s("fix4") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["dull1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["dull1"], 1.2)
            return
        self.chip(540, 300, "coat", T["coating"] - 0.2, T["sand"] - 0.2, accent="#7DD3FC", size=50)
        self.chip(540, 300, "shine", T["sand"] - 0.2, s("cta") - 0.15, accent=GOOD, size=50)
        self.badge("check", T["sand1"] + 0.1, s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: home (tag)
    def draw_home(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#3B2F4A", "#2A2238"])
        c.drawRect(R(0, 1120, W, H - 1120), P("#5B4636"))
        for k in range(6):
            c.drawLine(0, 1120 + k * 60, W, 1120 + k * 60, P("#4A3828", 0.6, stroke=3))
        c.drawRect(R(80, 420, 320, 260), P("#1E3A5F"))                     # a window
        c.drawRect(R(80, 420, 320, 260), P("#CBD5E1", 1.0, stroke=10))
        v2.moon(c, 300, 500, 30)
        # you, hiding behind a tall mirror panel; mom walks in
        mk = prog(t, T["t_turn"] - 0.6, T["t_turn"])
        mx = lerp(1180, 820, e_out(mk))
        person(c, mx, 1150, 300, "#DB2777", t, pose="point" if mk > 0.6 else "walk", face=-1, hair="#3B2A20")
        hx = 470
        person(c, hx, 1150, 250, "#2563EB", t, pose="stand", face=1)
        c.drawRect(R(hx - 120, 620, 240, 470), lin_paint(hx - 120, 620, hx + 120, 1090, ["#5D7FA6", "#8FB1D3", "#46668C"]))
        c.drawRect(R(hx - 120, 620, 240, 470), P("#E5E7EB", 1.0, stroke=8))
        c.drawPath(path_of([(hx - 90, 620), (hx - 30, 620), (hx - 120, 900), (hx - 120, 760)], close=True), P("#FFFFFF", 0.22))
        fk = prog(t, T["t_dishes"] - 0.2, T["t_dishes"] + 0.2)
        if fk > 0:                                                          # the feet give you away
            add_glow(c, hx, 1130, 80, "#FDE68A", 0.5 * fk)
        if not self.rtl:                                                    # a pile of dishes on the counter
            c.drawRect(R(760, 900, 300, 220), P("#94A3B8"))
            for k in range(7):
                c.drawOval(R(800 + (k % 2) * 20, 880 - k * 16, 160, 26), P("#F8FAFC"))
                c.drawOval(R(800 + (k % 2) * 20, 880 - k * 16, 160, 26), P("#94A3B8", 1.0, stroke=3))

    def ui_home(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "you", T["t_turn"] - 0.2, self.duration + 1, accent=WARN, size=44)
        self.chip(540, 420, "feet", T["t_dishes"] - 0.1, self.duration + 1, accent=HILITE, size=46)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1220", "#1E293B"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.sparkle(1.4, 14, 61), -12), (T["vanishes"], sfx.whoosh(0.7, False, 62), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(T["spoil1"] - 0.1, sfx.thud(0.5, 66), -8), (T["spoil1"], sfx.alarm(3, 820.0), -12)]
        for k in range(6):
            ev.append((lerp(T["cover"], T["rocks"], k / 5), sfx.click(67 + k), -10))
        ev += [(T["instead1"], sfx.sparkle(1.0, 12, 74), -8), (T["instead1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["sun"], sfx.hiss(1.2, 75), -16), (T["bake"], sfx.sizzle(1.2, 76), -10), (T["oven1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["bounce"], sfx.riser(0.8, 77), -12), (T["sky1"], sfx.ding(), -8), (T["sky1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 78), -6), (T["grows"], sfx.creak(0.9, 79), -10),
               (T["crack1"], sfx.snap(80), -4), (T["crack1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["gap"], sfx.lock_click(81), -8), (T["move1"], sfx.ding(), -8), (T["move1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["storms"], sfx.hiss(1.8, 82), -8), (T["dull1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["coating"], sfx.whoosh(0.6, False, 83), -10), (T["sand1"], sfx.sparkle(0.9, 10, 84), -8),
               (T["sand1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(85), 0), (T["follow"] - 0.15, sfx.pop(86), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 87), -6)]
        for k in range(8):
            ev.append((lerp(T["ten"] - 0.4, T["most"], k / 7), sfx.tick(), -14))
        ev += [(T["most"], sfx.chime(), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 88), -6), (T["s1"], sfx.pop(89), -3), (T["s2"], sfx.pop(90), -3),
               (T["s3"], sfx.pop(91), -3)]
        ev += [(T["cong2"], sfx.pop(92), -2), (T["cong2"], sfx.sparkle(1.4, 18, 93), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 94), -6), (T["t_turn"], sfx.tap(95), -8),
               (T["t_dishes"], sfx.womp(), -8)]
        return ev


NAME = "maraya"
EPISODE = Maraya
