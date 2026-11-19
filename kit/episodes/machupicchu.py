"""Episode 45 - Machu Picchu (Peru).  v2 look: a misty Andes dusk, the green tooth of Huayna Picchu behind a grey stone
city on a knife-edge ridge, terraces stepping down both sides into clouds, rain.

Sets: city (hook: rain pours on the city on its ridge, a rain gauge fills to 2 m, 500 years and no slide; the reveal:
palaces rise on the ridge for the emperor Pachacuti, the Spanish never found it; the stat; the closer), slope (break1: a
steep slope in section, rain turns the soil to mud and it slides; fix1: the slope is carved into terraces, each held by
a stone wall), layers (break2: one terrace in section, rain soaks the flat soil, the wall bulges and bursts; fix2: the
fill in layers: stones, gravel, sand, topsoil, rain runs straight through and out), water (break3: a flood rushes down
the stairs; fix3: a stone canal feeds a staircase of fountains, drain holes spout storm water into the main drain),
quake (break4: fault lines glow under the city, the ground shakes; fix4: a close-up of stones cut so tight a sheet of
paper won't go in, a trapezoid doorway leaning inward, the stones jiggle and settle; the cta), ac (the tag: an AC unit
upstairs drips on your head).
World (city): side view, the ridge top (city level) about y = -450, the valleys far below; up is negative.
"""
from v2_base import *  # noqa: F401,F403
from panama import rain  # noqa: E402
from windtower import arrow  # noqa: E402

MIST = {"top": "#0B1A2E", "upper": "#1E3A52", "mid": "#4D6E7E", "low": "#C0907A", "horizon": "#F2C08C",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STORMY = {"top": "#0A1322", "upper": "#1B2A3D", "mid": "#33495A", "low": "#5E7180", "horizon": "#8B97A0",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
GRANITE, GRANITE_L, GRANITE_D = "#A8A49B", "#D6D2C8", "#625E57"
THATCH, THATCH_D = "#B8893E", "#7A5520"
GREEN, GREEN_D = "#4C8A3A", "#25502A"
SOIL, SOIL_D = "#7A5232", "#3F2A1A"
MUDC = "#4A3524"


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def huayna(c, x, y, s, a=1.0):
    """Huayna Picchu: the steep green tooth behind the city, base centred at (x, y)."""
    p = skia.Path()
    p.moveTo(x - 420 * s, y)
    p.cubicTo(x - 300 * s, y - 300 * s, x - 190 * s, y - 760 * s, x - 70 * s, y - 900 * s)
    p.quadTo(x + 10 * s, y - 960 * s, x + 80 * s, y - 880 * s)
    p.cubicTo(x + 200 * s, y - 700 * s, x + 280 * s, y - 320 * s, x + 460 * s, y)
    p.close()
    c.drawPath(p, lin_paint(0, y - 950 * s, 0, y, ["#5E8F5A", "#2E5A34", "#1A3A24"], a=a))
    c.save()
    c.clipPath(p, doAntiAlias=True)
    rng = random.Random(5)
    for i in range(18):                                       # rock faces and tree texture
        rx, ry = x + rng.uniform(-300, 300) * s, y - rng.uniform(80, 860) * s
        c.drawOval(R(rx, ry, rng.uniform(40, 110) * s, rng.uniform(20, 60) * s), P("#1F4027", 0.5 * a))
    for i in range(6):
        rx = x + (-150 + i * 50) * s
        c.drawLine(rx, y - 700 * s + i * 40 * s, rx + 40 * s, y - 520 * s + i * 30 * s, P("#7C8C7A", 0.35 * a, stroke=8 * s))
    c.restore()


def ridge_shape(x):
    """The city's ridge: flat-topped near y -450 between x -340 and 340, falling steeply into the valleys."""
    if -340 <= x <= 340:
        return -450 + 10 * math.sin(x / 90.0)
    if x < -340:
        return -450 + (-340 - x) * 1.12
    return -450 + (x - 340) * 1.12


def terraces_side(c, x_top, y_top, n, dx, dy, sgn, k=1.0, a=1.0):
    """n terraces stepping down from (x_top, y_top), each dx wide and dy high, going right (sgn 1) or left (-1)."""
    for i in range(n):
        if (i + 1) / n > k + 1e-6:
            break
        x0 = x_top + sgn * i * dx
        y0 = y_top + i * dy
        x1 = x0 + sgn * dx
        lo, hi = min(x0, x1), max(x0, x1)
        c.drawRect(R(lo, y0 - 14, hi - lo, 18), P(GREEN, a))
        c.drawRect(R(lo, y0 + 4, hi - lo, 8), P("#2F6A2A", a))
        wx = x1
        c.drawRect(R(wx - (12 if sgn > 0 else 0) - (0 if sgn > 0 else 12), y0 - 14, 12, dy + 14),
                   P(GRANITE_D, a))
        face = R(min(wx, wx + sgn * 10), y0 - 14, 10, dy + 14)
        c.drawRect(face, P(GRANITE, a))
        for j in range(int(dy / 22)):
            yy = y0 - 6 + j * 22
            c.drawLine(face.left(), yy, face.right(), yy, P(GRANITE_D, 0.6 * a, stroke=2))


def front_terraces(c, y0, n, quake=0.0, t=0.0, a=1.0):
    """The terraced slope below the city, seen from the front: grey stone walls and green steps, widening downward."""
    for i in range(n):
        y = y0 + i * 60
        half = 360 + i * 70
        jig = math.sin(t * 37 + i) * 5 * quake
        wall = skia.Path()
        wall.moveTo(-half + jig, y)
        wall.quadTo(jig, y + 16, half + jig, y)
        wall.lineTo(half + jig, y + 26)
        wall.quadTo(jig, y + 42, -half + jig, y + 26)
        wall.close()
        c.drawPath(wall, lin_paint(0, y, 0, y + 30, [GRANITE_L, GRANITE], a=a))
        for k in range(int(half * 2 / 46)):
            xx = -half + 23 + k * 46 + (12 if i % 2 else 0) + jig
            c.drawLine(xx, y + 4 + 16 * (1 - (xx / half) ** 2), xx, y + 24 + 16 * (1 - (xx / half) ** 2), P(GRANITE_D, 0.6 * a, stroke=2))
        step = skia.Path()
        step.moveTo(-half - 35 + jig, y + 26)
        step.quadTo(jig, y + 42, half + 35 + jig, y + 26)
        step.lineTo(half + 35 + jig, y + 60)
        step.quadTo(jig, y + 76, -half - 35 + jig, y + 60)
        step.close()
        c.drawPath(step, lin_paint(0, y + 26, 0, y + 70, [GREEN, "#3B7330"], a=a))


def house(c, x, y, w, h, a=1.0, roof=1.0, lit=0.0, door=True):
    """A granite Inca house with a trapezoid doorway and a steep thatched gable roof, standing on (x, y)."""
    side = skia.Path()
    side.moveTo(x + w / 2, y)
    side.lineTo(x + w / 2 + w * 0.22, y - w * 0.12)
    side.lineTo(x + w / 2 + w * 0.22, y - h - w * 0.12)
    side.lineTo(x + w / 2, y - h)
    side.close()
    c.drawPath(side, P(GRANITE_D, a))
    c.drawRect(R(x - w / 2, y - h, w, h), lin_paint(0, y - h, 0, y, [GRANITE_L, GRANITE], a=a))
    for j in range(int(h / 18)):
        yy = y - h + 9 + j * 18
        c.drawLine(x - w / 2, yy, x + w / 2, yy, P(GRANITE_D, 0.35 * a, stroke=2))
    if door:
        dp = skia.Path()
        dp.moveTo(x - w * 0.16, y)
        dp.lineTo(x - w * 0.11, y - h * 0.62)
        dp.lineTo(x + w * 0.11, y - h * 0.62)
        dp.lineTo(x + w * 0.16, y)
        dp.close()
        c.drawPath(dp, P("#211A14", a))
        if lit > 0:
            c.drawPath(dp, P("#FDBA74", lit * a))
    if roof > 0:
        rp = skia.Path()
        rh = h * 0.8 * roof
        rp.moveTo(x - w / 2 - 8, y - h)
        rp.lineTo(x, y - h - rh)
        rp.lineTo(x + w / 2 + 8, y - h)
        rp.close()
        c.drawPath(rp, lin_paint(x - w / 2, 0, x + w / 2, 0, [THATCH, THATCH_D], a=a))
        for j in range(5):
            c.drawLine(x - w * 0.4 + j * w * 0.2, y - h, x, y - h - rh, P(THATCH_D, 0.35 * a, stroke=2))


def mist(c, x0, x1, y, t, a=0.6, n=10, seed=3, s=1.0):
    rng = random.Random(seed)
    for i in range(n):
        px = x0 + ((rng.uniform(0, 1) * (x1 - x0) + t * 12) % (x1 - x0))
        v2.puff(c, px, y + rng.uniform(-40, 40) * s, rng.uniform(90, 170) * s, "#E2E8F0", a * rng.uniform(0.5, 1.0), k=i)


def gauge(c, x, y, h, fill, a=1.0):
    """A tall rain gauge (glass tube) filled to fraction fill, with a person for scale."""
    c.drawRRect(rr(x - 46, y - h, 92, h, 18), P("#E0F2FE", 0.22 * a))
    c.drawRRect(rr(x - 46, y - h, 92, h, 18), P("#E0F2FE", 0.9 * a, stroke=5))
    fh = h * clamp(fill)
    if fh > 2:
        c.drawRRect(rr(x - 40, y - fh, 80, fh - 6, 14), lin_paint(0, y - fh, 0, y, ["#7DD3FC", "#0369A1"], a=a))
    for j in range(5):
        yy = y - h * j / 4.0
        c.drawLine(x + 46, yy, x + 70, yy, P("#E0F2FE", a, stroke=4))
    person(c, x - 210, y, h * 0.85, "#F59E0B", 0.0, pose="look", face=1, hat="none", hair="#1C1917", a=a)


def helmet(c, x, y, s, a=1.0):
    """A Spanish conquistador's helmet (morion) with a question mark."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    hp = skia.Path()
    hp.moveTo(-90, 10)
    hp.quadTo(0, -20, 90, 10)
    hp.quadTo(60, -10, 40, -40)
    hp.quadTo(0, -110, -40, -40)
    hp.quadTo(-60, -10, -90, 10)
    hp.close()
    c.drawPath(hp, lin_paint(-90, 0, 90, 0, ["#9CA3AF", "#E5E7EB", "#6B7280"], a=a))
    c.drawLine(-10, -96, 30, -50, P("#E5E7EB", a, stroke=10))
    c.restore()


def ashlar_stones():
    """Polygons of a tight Inca wall (screen-space units around 0..800 x 0..600)."""
    return [
        [(0, 0), (260, 0), (250, 170), (0, 160)],
        [(260, 0), (520, 0), (540, 140), (380, 190), (250, 170)],
        [(520, 0), (800, 0), (800, 210), (540, 140)],
        [(0, 160), (250, 170), (380, 190), (360, 360), (0, 340)],
        [(380, 190), (540, 140), (800, 210), (800, 380), (560, 400), (360, 360)],
        [(0, 340), (360, 360), (330, 600), (0, 600)],
        [(360, 360), (560, 400), (600, 600), (330, 600)],
        [(560, 400), (800, 380), (800, 600), (600, 600)],
    ]


def stone_poly(c, pts, dx, dy, col, a=1.0, shade_k=0.0):
    p = skia.Path()
    cx_ = sum(q[0] for q in pts) / len(pts)
    cy_ = sum(q[1] for q in pts) / len(pts)
    inset = 3.0
    for i, (px, py) in enumerate(pts):
        qx = px + (cx_ - px) * inset / max(1.0, math.hypot(cx_ - px, cy_ - py)) + dx
        qy = py + (cy_ - py) * inset / max(1.0, math.hypot(cx_ - px, cy_ - py)) + dy
        (p.moveTo if i == 0 else p.lineTo)(qx, qy)
    p.close()
    c.drawPath(p, rad_paint(cx_ + dx - 40, cy_ + dy - 40, 260, [mix(GRANITE_L, col, 0.3), col, shade(col, -0.25 + shade_k)], a=a))
    c.drawPath(p, P("#3A362F", 0.8 * a, stroke=3))


def window_ac(c, x, y, s, t, a=1.0):
    """An outdoor AC box sticking out of a window, a drip at its corner."""
    c.drawRRect(rr(x - 90 * s, y - 60 * s, 180 * s, 120 * s, 10 * s), P("#CBD5E1", a))
    c.drawRRect(rr(x - 90 * s, y - 60 * s, 180 * s, 120 * s, 10 * s), P("#64748B", a, stroke=4 * s))
    for k in range(7):
        c.drawLine(x - 70 * s, y - 40 * s + k * 13 * s, x + 70 * s, y - 40 * s + k * 13 * s, P("#94A3B8", a, stroke=3 * s))
    c.drawCircle(x + 50 * s, y, 26 * s, P("#94A3B8", a, stroke=4 * s))
    c.save()
    c.translate(x + 50 * s, y)
    c.rotate(t * 720)
    for k in range(3):
        c.rotate(120)
        c.drawLine(0, 0, 20 * s, 0, P("#475569", a, stroke=5 * s))
    c.restore()


def facade(c, t):
    """The tag's apartment block: warm windows, balconies, a street below."""
    vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
    c.drawRect(R(60, 160, 960, 1000), lin_paint(60, 0, 1020, 0, ["#C2A27C", "#A8865F"]))
    for r_ in range(4):
        for q in range(3):
            wx, wy = 130 + q * 300, 220 + r_ * 230
            c.drawRect(R(wx, wy, 200, 150), P("#3B2F2A"))
            c.drawRect(R(wx + 8, wy + 8, 184, 134), P("#FDE68A", 0.55 + 0.2 * ((r_ + q) % 2)))
            c.drawLine(wx + 100, wy + 8, wx + 100, wy + 142, P("#3B2F2A", stroke=6))
            c.drawRect(R(wx - 10, wy + 150, 220, 14), P("#8B6A4E"))
    c.drawRect(R(0, 1160, W, 90), P("#475569"))
    c.drawRect(R(0, 1150, W, 14), P("#94A3B8"))
    vrect(c, 0, 1240, W, H - 1240, ["#334155", "#0F172A"])


# ====================================================================================== the episode
class MachuPicchu(EpisodeV2):
    BUILD_NO = 45
    FIRST_SET = "city"
    CLEAR = "#0B1A2E"
    TITLE = {"en": "MACHU PICCHU", "ar_sa": "ماتشو بيتشو"}
    EMPH = {"en": ["CONGRATS", "CITY", "KNIFE-EDGE", "MOUNTAIN", "TWO", "METERS", "RAIN", "SLID", "FIVE", "CENTURIES",
                   "MACHU", "PICCHU", "STEEP", "SOIL", "MUD", "SLIDES", "CARVE", "GIANT", "STEPS", "HUNDREDS",
                   "TERRACES", "WALL", "FLAT", "HOLD", "SOAKED", "HEAVY", "BURST", "LAYERS", "STONES", "GRAVEL",
                   "SAND", "TOPSOIL", "STRAIGHT", "WATER", "FLOODS", "CANAL", "SIXTEEN", "FOUNTAINS", "HUNDRED",
                   "DRAIN", "HOLES", "STORMS", "FAULT", "LINES", "EARTHQUAKES", "SHAKING", "TIGHT", "PAPER",
                   "LEAN", "DOORS", "INWARD", "FOLLOW", "ASWAN", "HIGH", "DAM", "PALACES", "EMPEROR",
                   "PACHACUTI", "SPANISH", "NEVER", "FOUND", "TWENTY-FOUR", "SIXTY", "PERCENT", "UNDERGROUND",
                   "SLIDE", "YOURSELF", "DROP", "PLANNED", "NEIGHBOR'S", "AC", "DRIPS", "HEAD"],
            "ar_sa": ["مبروك", "مدينة", "حجر", "حاد", "مترين", "مطر", "انزلقت", "قرون", "ماتشو", "بيتشو", "بهالحدة",
                      "التراب", "طين", "ينزلق", "فتقص", "درج", "مئات", "المدرجات", "جدار", "تحبس", "المبلول", "يثقل",
                      "يفجر", "طبقات", "حصى", "رمل", "تربة", "ينزل", "موية", "سيول", "فقناة", "العين", "للنوافير",
                      "فتحة", "السيول", "صدوع", "والزلازل", "تهزها", "جاره", "الورقة", "تدخل", "وتميل", "الأبواب",
                      "تابعني", "السد", "العالي", "قصور", "إمبراطور", "الإنكا", "والإسبان", "لقوها", "ألفين",
                      "ستين", "الأرض", "انزلاق", "بيدك", "نقطة", "خططوا", "الجيران", "ينقط", "راسك"]}
    KEYS = {"ar_sa": {
        ("hook", "BUILD"): "بنيت", ("hook", "KNIFE"): "حاد", ("hook", "TWO"): "مترين", ("hook", "RAIN"): "مطر",
        ("hook", "SLID"): "انزلقت", ("hook", "CENTURIES"): "قرون", ("hook", "CONGRATS"): "مبروك",
        ("hook", "MACHU"): "ماتشو",
        ("break1", "STEEP"): "بهالحدة", ("break1", "SOIL"): "التراب", ("break1", "MUD"): "طين",
        ("break1", "SLIDES"): "ينزلق",
        ("fix1", "CARVE"): "فتقص", ("fix1", "STEPS"): "درج", ("fix1", "HUNDREDS"): "مئات",
        ("fix1", "TERRACES"): "المدرجات", ("fix1", "WALL"): "جدار",
        ("break2", "HOLD"): "تحبس", ("break2", "SOAKED"): "المبلول", ("break2", "HEAVY"): "يثقل",
        ("break2", "BURST"): "يفجر",
        ("fix2", "LAYERS"): "طبقات", ("fix2", "STONES"): "حجر", ("fix2", "GRAVEL"): "حصى", ("fix2", "SAND"): "رمل",
        ("fix2", "TOPSOIL"): "تربة", ("fix2", "RUNS"): "ينزل",
        ("break3", "WATER"): "موية", ("break3", "FLOODS"): "سيول",
        ("fix3", "CANAL"): "فقناة", ("fix3", "SIXTEEN"): "العين", ("fix3", "FOUNTAINS"): "للنوافير",
        ("fix3", "DRAIN"): "فتحة", ("fix3", "STORMS"): "السيول",
        ("break4", "FAULT"): "صدوع", ("break4", "EARTHQUAKES"): "والزلازل", ("break4", "SHAKING"): "تهزها",
        ("fix4", "CUT"): "فتقص", ("fix4", "TIGHT"): "جاره", ("fix4", "PAPER"): "الورقة", ("fix4", "SLIP"): "تدخل",
        ("fix4", "LEAN"): "وتميل", ("fix4", "DOORS"): "الأبواب",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PALACES"): "قصور", ("reveal", "EMPEROR"): "إمبراطور", ("reveal", "PACHACUTI"): "الإنكا",
        ("reveal", "SPANISH"): "والإسبان", ("reveal", "NEVER"): "لقوها",
        ("stat", "TWENTY"): "ألفين", ("stat", "SIXTY"): "ستين", ("stat", "FIVE"): "وخمس",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STORMS"): "سيول", ("tag", "DROP"): "نقطة", ("tag", "PLANNED"): "خططوا", ("tag", "NEIGHBOR"): "الجيران",
        ("tag", "DRIPS"): "ينقط", ("tag", "HEAD"): "راسك"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Aswan High Dam"),
                   "stat": [("2,430 m", "ABOVE THE SEA"), ("60%", "UNDERGROUND"), ("500+", "YEARS, NO SLIDE")],
                   "L": {"knife": "A KNIFE-EDGE RIDGE", "rain2": "2 m OF RAIN A YEAR", "noslide": "500 YEARS, NO SLIDE",
                         "name": "MACHU PICCHU", "steep": "A STEEP SLOPE", "mud": "SOIL TURNS TO MUD",
                         "slides": "AND IT SLIDES", "steps": "GIANT STEPS", "terr": "HUNDREDS OF TERRACES",
                         "wall": "A STONE WALL EACH", "hold": "FLAT STEPS HOLD RAIN", "heavy": "SOAKED = HEAVY",
                         "burst": "THE WALL BURSTS", "stones": "STONES", "gravel": "GRAVEL", "sand": "SAND",
                         "topsoil": "TOPSOIL", "runs": "RAIN RUNS THROUGH", "floods": "NOT FLOODS",
                         "canal": "STONE CANAL", "f16": "16 FOUNTAINS", "drains": "100+ DRAIN HOLES",
                         "fault": "FAULT LINES", "quake": "EARTHQUAKES", "tight": "NO MORTAR, CUT TIGHT",
                         "paper": "PAPER WON'T GO IN", "lean": "DOORS LEAN INWARD", "palaces": "PALACES",
                         "emperor": "FOR EMPEROR PACHACUTI", "spanish": "THE SPANISH NEVER FOUND IT",
                         "drip": "DRIP.", "planned": "EVERY DROP PLANNED"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: السد العالي"),
                      "stat": [("2,430", "متر فوق البحر"), ("60%", "تحت الأرض"), ("500+", "سنة بدون انزلاق")],
                      "L": {"knife": "جبل حاد زي السكين", "rain2": "مترين مطر بالسنة", "noslide": "خمس قرون بدون انزلاق",
                            "name": "ماتشو بيتشو", "steep": "منحدر حاد", "mud": "التراب يصير طين",
                            "slides": "والطين ينزلق", "steps": "درج عملاق", "terr": "مئات المدرجات",
                            "wall": "كل وحدة لها جدار", "hold": "الدرجة تحبس المطر", "heavy": "مبلول = ثقيل",
                            "burst": "الجدار ينفجر", "stones": "حجر", "gravel": "حصى", "sand": "رمل",
                            "topsoil": "تربة", "runs": "المطر ينزل ويطلع", "floods": "مو سيول",
                            "canal": "قناة حجر", "f16": "16 نافورة", "drains": "أكثر من 100 فتحة",
                            "fault": "صدوع", "quake": "زلازل", "tight": "كل حجر على جاره",
                            "paper": "الورقة ما تدخل", "lean": "الأبواب مايلة لداخل", "palaces": "قصور",
                            "emperor": "لإمبراطور الإنكا", "spanish": "الإسبان ما لقوها",
                            "drip": "نقط.", "planned": "كل نقطة مخطط لها"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "build": ("hook", "BUILD", 0.05), "knife": ("hook", "KNIFE", 0.25), "two": ("hook", "TWO", 0.4),
            "rain": ("hook", "RAIN", 0.5), "slid": ("hook", "SLID", 0.65), "centuries": ("hook", "CENTURIES", 0.72),
            "congrats": ("hook", "CONGRATS", 0.8), "machu": ("hook", "MACHU", 0.92),
            "steep": ("break1", "STEEP", 0.3), "soil": ("break1", "SOIL", 0.55), "mud": ("break1", "MUD", 0.7),
            "slides": ("break1", "SLIDES", 0.92),
            "carve": ("fix1", "CARVE", 0.1), "steps": ("fix1", "STEPS", 0.35), "hundreds": ("fix1", "HUNDREDS", 0.55),
            "terraces": ("fix1", "TERRACES", 0.65), "wall": ("fix1", "WALL", 0.92),
            "hold": ("break2", "HOLD", 0.25), "soaked": ("break2", "SOAKED", 0.5), "heavy": ("break2", "HEAVY", 0.7),
            "burst": ("break2", "BURST", 0.88),
            "layers": ("fix2", "LAYERS", 0.25), "stones": ("fix2", "STONES", 0.4), "gravel": ("fix2", "GRAVEL", 0.5),
            "sand": ("fix2", "SAND", 0.6), "topsoil": ("fix2", "TOPSOIL", 0.7), "runs": ("fix2", "RUNS", 0.88),
            "water": ("break3", "WATER", 0.4), "floods": ("break3", "FLOODS", 0.85),
            "canal": ("fix3", "CANAL", 0.15), "sixteen": ("fix3", "SIXTEEN", 0.35), "fountains": ("fix3", "FOUNTAINS", 0.45),
            "drain": ("fix3", "DRAIN", 0.7), "storms": ("fix3", "STORMS", 0.9),
            "fault": ("break4", "FAULT", 0.35), "quake": ("break4", "EARTHQUAKES", 0.7), "shaking": ("break4", "SHAKING", 0.9),
            "cut": ("fix4", "CUT", 0.1), "tight": ("fix4", "TIGHT", 0.35), "paper": ("fix4", "PAPER", 0.5),
            "slip": ("fix4", "SLIP", 0.62), "lean": ("fix4", "LEAN", 0.82), "doors": ("fix4", "DOORS", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "palaces": ("reveal", "PALACES", 0.2), "emperor": ("reveal", "EMPEROR", 0.4),
            "pacha": ("reveal", "PACHACUTI", 0.55), "spanish": ("reveal", "SPANISH", 0.8), "never": ("reveal", "NEVER", 0.9),
            "s1": ("stat", "TWENTY", 0.04), "s2": ("stat", "SIXTY", 0.35), "s3": ("stat", "FIVE", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "storms2": ("tag", "STORMS", 0.15), "drop": ("tag", "DROP", 0.35), "planned": ("tag", "PLANNED", 0.55),
            "neighbor": ("tag", "NEIGHBOR", 0.7), "drips": ("tag", "DRIPS", 0.85), "head": ("tag", "HEAD", 0.95)})
        # ---- sets
        self.cut(s("break1") - 0.12, "slope", 1)
        self.cut(s("break2") - 0.12, "layers", -1)
        self.cut(s("break3") - 0.12, "water", 1)
        self.cut(s("break4") - 0.12, "quake", -1)
        self.cut(T["cut"] - 0.12, "stones", 1)
        self.cut(s("reveal") - 0.12, "city", -1)
        self.cut(s("tag") - 0.2, "ac", 1)
        cm = Camera(0, -470, 1.15)
        cm.key(0.05, 0, -400, 1.0, max(2.0, T["congrats"])).key(T["congrats"], 0, -390, 0.97, 2.0)
        cm.key(s("reveal") - 0.12, 0, -440, 1.2, 0.0).key(s("reveal"), 0, -430, 1.1, max(1.0, s("stat") - s("reveal")))
        cm.key(s("stat") - 0.12, 0, -300, 0.8, 0.0)
        cm.key(s("closer") - 0.1, 0, -470, 1.05, 0.0).key(self.duration, 0, -470, 1.09, 3.0)
        self.cam = cm
        self.spans = [(T["slides"], T["wall"] + 0.3), (T["burst"], T["runs"] + 0.3), (T["floods"], T["storms"] + 0.3),
                      (T["shaking"], T["doors"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 7), (T["slides"], 0.6, 10), (T["burst"], 0.5, 12), (T["floods"], 0.5, 8),
                       (T["quake"], 1.2, 16), (T["shaking"], 0.8, 12), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def world(self, c, t, cam, rain_a=0.0, palaces=1.0, lit=0.4, quake=0.0, faults=0.0):
        """The city on its ridge with Huayna Picchu behind, terraces down both sides, mist in the valleys."""
        cx, cy, z = cam
        v2.sky(c, W, H, 0.0, pal=MIST if rain_a < 0.5 else STORMY, horizon_y=(-300 - cy) * z + H / 2)
        c.save()
        c.translate(W / 2 - cx * 0.1, (-250 - cy) * z * 0.6 + H / 2)
        v2.ridge(c, -1700, 1700, 0, 420, "#3E5C6E", "#22394A", seed=31, step=110, rough=0.7)
        c.restore()
        self.view(c, cam)
        huayna(c, 260, -300, 1.0)
        mist(c, -1400, 1400, -420, t, a=0.22, n=8, seed=4)
        rp = skia.Path()
        rp.moveTo(-1700, 1400)
        x = -1700
        while x <= 1700:
            rp.lineTo(x, ridge_shape(x))
            x += 25
        rp.lineTo(1700, 1400)
        rp.close()
        c.drawPath(rp, lin_paint(0, -470, 0, 600, ["#3F6B3A", "#24402A", "#122218"]))
        front_terraces(c, -440, 13, quake=quake, t=t)
        if faults > 0:
            for k, (fx_, fang) in enumerate(((-260, 1.2), (200, 1.9))):
                fp = skia.Path()
                fp.moveTo(fx_, -440)
                rng = random.Random(k)
                yy, xx = -440, fx_
                while yy < 900:
                    yy += 60
                    xx += rng.uniform(-30, 30) + (fang - 1.5) * 20
                    fp.lineTo(xx, yy)
                c.drawPath(fp, P("#FF6A3D", 0.9 * faults, stroke=10))
                c.drawPath(fp, P("#FFB37A", 0.6 * faults, stroke=26, blur=10))
        c.drawRect(R(-340, -470, 680, 30), P(GREEN_D))
        rng = random.Random(9)
        houses = [(-245, 1), (-155, 1), (-65, 1), (25, 1), (115, 1), (205, 1),
                  (-290, 0), (-200, 0), (-110, 0), (-20, 0), (70, 0), (160, 0), (250, 0)]
        for i, (hx, row) in enumerate(houses):
            jig = math.sin(t * 40 + i) * 6 * quake
            base = ridge_shape(hx) - (40 if row else 0)
            house(c, hx + jig, base, 84 + rng.uniform(-6, 12), 64 + rng.uniform(0, 18), roof=0.75, lit=lit)
        if palaces > 0:                                            # the royal compound on the highest point
            for k, (px_, w_, h_) in enumerate(((-120, 130, 92), (20, 160, 108), (160, 130, 92))):
                pk = clamp(palaces * 3 - k)
                if pk > 0:
                    base = ridge_shape(px_) - 60
                    house(c, px_, base, w_, h_ * e_out(pk), roof=pk, lit=lit + 0.3)
        c.drawRect(R(-2000, -100, 4000, 1400), lin_paint(0, -100, 0, 500, [("#DCE4EE", 0.0), ("#DCE4EE", 0.38)]))
        c.restore()
        if rain_a > 0:
            rain(c, -100, W + 100, -100, H, t, a=rain_a, n=110, seed=17)

    # ------------------------------------------------------------------ set: city (hook, reveal, stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        if hook:
            self.world(c, t, cam, rain_a=1.0 - 0.6 * prog(t, T["slid"], T["congrats"]), palaces=1.0, lit=0.3)
        elif t < s("stat") - 0.12:
            self.world(c, t, cam, rain_a=0.0, palaces=prog(t, T["palaces"] - 0.3, T["emperor"] + 0.3), lit=0.5)
        else:
            self.world(c, t, cam, rain_a=0.0, palaces=1.0, lit=0.55)
        self.ui["cam"] = cam

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam.at(tw))
        if tw < s("break1"):
            self.chip(540, 420, "knife", T["knife"] - 0.15, T["two"] - 0.1, accent="#E2E8F0", size=40)
            k = self.span(T["two"] - 0.15, T["slid"] - 0.05)
            if k > 0:
                c.drawRRect(rr(500, 470, 520, 660, 40), P("#0B1220", 0.88 * k))
                gauge(c, 880, 1060, 500, prog(tw, T["two"] - 0.1, T["rain"] + 0.5), a=k)
                v2.chip(c, 540, 420, self.L["rain2"], k, accent="#7DD3FC", size=40)
            self.chip(540, 420, "noslide", T["slid"] - 0.1, T["machu"] - 0.1, accent=GOOD, size=40)
            self.chip(540, 420, "name", T["machu"] - 0.1, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if tw < s("stat") - 0.12:
            self.chip(540, 420, "palaces", T["palaces"] - 0.15, T["emperor"] - 0.1, accent=HILITE, size=44)
            self.chip(540, 420, "emperor", T["emperor"] - 0.1, T["spanish"] - 0.15, accent="#FDE68A", size=38)
            k = self.span(T["spanish"] - 0.15, s("stat") - 0.15)
            if k > 0:
                v2.chip(c, 540, 420, self.L["spanish"], k, accent=WARN, size=36)
                helmet(c, 540, 580, 1.2 * e_back(clamp(k)), a=k)
                word(c, "?", 640, 560, 90, HILITE, a=k)

    # ------------------------------------------------------------------ set: slope (break1, fix1)
    def draw_slope(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        cam = (0, -40, 0.9)
        v2.sky(c, W, H, 0.0, pal=STORMY, horizon_y=H * 0.5)
        self.view(c, cam)
        top = (-700.0, -720.0)
        bot = (700.0, 480.0)
        slope = skia.Path()                                      # the mountain in section
        slope.moveTo(-1400, -720)
        slope.lineTo(*top)
        slope.lineTo(*bot)
        slope.lineTo(1400, 480)
        slope.lineTo(1400, 1600)
        slope.lineTo(-1400, 1600)
        slope.close()
        c.drawPath(slope, lin_paint(0, -720, 0, 900, ["#5A5048", "#3A332E"]))
        c.save()
        c.clipPath(slope, doAntiAlias=True)
        for k in range(14):
            c.drawLine(-1400, -700 + k * 120, 1400, -500 + k * 120, P("#2A2420", 0.4, stroke=6))
        c.restore()
        if not fixed:
            mud = prog(t, T["soil"] - 0.3, T["mud"] + 0.2)
            sl = e_in(prog(t, T["slides"] - 0.25, T["slides"] + 0.9))
            ang = math.atan2(bot[1] - top[1], bot[0] - top[0])
            ox, oy = math.cos(ang) * 600 * sl, math.sin(ang) * 600 * sl
            c.save()
            c.translate(ox, oy)
            c.rotate(-6 * sl)
            sp = skia.Path()                                     # the soil layer on top of the rock
            sp.moveTo(*top)
            sp.lineTo(*bot)
            sp.lineTo(bot[0] - 70, bot[1] + 70)
            sp.lineTo(top[0] - 70, top[1] + 70)
            sp.close()
            c.drawPath(sp, P(mix(SOIL, MUDC, mud)))
            for k in range(16):                                  # grass and bushes on it
                u = k / 15.0
                gx, gy = lerp(top[0], bot[0], u), lerp(top[1], bot[1], u)
                c.drawCircle(gx, gy - 10, 26, P(mix(GREEN, "#3B4A2A", mud)))
            if mud > 0.2:
                for k in range(10):
                    u = (k * 0.097 + t * 0.15) % 1.0
                    gx, gy = lerp(top[0], bot[0], u), lerp(top[1], bot[1], u)
                    c.drawCircle(gx + 20, gy + 40, 9, P("#93C5FD", 0.6 * mud))
            c.restore()
            if sl > 0:
                for k in range(14):
                    rng = random.Random(k)
                    u = rng.uniform(0.2, 1.0)
                    px = lerp(top[0], bot[0], u) + ox + rng.uniform(-40, 40)
                    py = lerp(top[1], bot[1], u) + oy + rng.uniform(-30, 60)
                    c.drawCircle(px, py, rng.uniform(10, 24), P(MUDC, sl))
        else:
            k = prog(t, T["carve"] - 0.2, T["terraces"] + 0.2)
            n = 9
            dx = (bot[0] - top[0]) / n
            dy = (bot[1] - top[1]) / n
            for i in range(n):
                if (i + 1) / n > k + 1e-6:
                    break
                x0 = top[0] + i * dx
                y0 = top[1] + i * dy
                plat = R(x0, y0, dx, 26)
                c.drawRect(R(x0 - 2, y0, dx + 4, dy + 6), P("#3A332E"))
                c.drawRect(plat, P(GREEN))
                c.drawRect(R(x0, y0 + 26, dx, 30), P(SOIL))
                wk = prog(t, T["wall"] - 0.6 + i * 0.03, T["wall"] - 0.2 + i * 0.03)
                c.drawRect(R(x0 + dx - 26, y0, 26, dy), P(mix("#5A5048", GRANITE, max(0.6, wk))))
                for j in range(int(dy / 26)):
                    c.drawLine(x0 + dx - 26, y0 + 13 + j * 26, x0 + dx, y0 + 13 + j * 26, P(GRANITE_D, 0.8, stroke=3))
                for q in range(3):
                    c.drawCircle(x0 + 30 + q * 40, y0 - 8, 14, P("#6DAA4A"))
        c.restore()
        rain(c, -100, W + 100, -100, H, t, a=0.8 if not fixed else 0.45, n=90, seed=3)
        self.ui["cam"] = cam

    def ui_slope(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 420, "steep", T["steep"] - 0.15, T["mud"] - 0.15, accent="#E2E8F0", size=40)
            self.chip(540, 420, "mud", T["mud"] - 0.15, T["slides"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 420, "slides", T["slides"] - 0.1, s("fix1") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["slides"] + 0.05, s("fix1") - 0.2, x=880, y=520)
            self.red(T["slides"] + 0.05, 1.3)
            return
        self.chip(540, 420, "steps", T["steps"] - 0.15, T["hundreds"] - 0.1, accent=HILITE, size=42)
        self.chip(540, 420, "terr", T["hundreds"] - 0.1, T["wall"] - 0.15, accent=GOOD, size=40)
        self.chip(540, 420, "wall", T["wall"] - 0.15, s("break2") - 0.15, accent="#E2E8F0", size=40)
        self.badge("check", T["wall"] + 0.1, s("break2") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: layers (break2, fix2)
    def draw_layers(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        v2.sky(c, W, H, 0.0, pal=STORMY, horizon_y=H * 0.45)
        x0, x1, ytop, ybot = 120.0, 820.0, 640.0, 1150.0
        mp = skia.Path()                                             # the mountain behind (left), the terrace below
        mp.moveTo(0, 300)
        mp.lineTo(x0 + 10, 520)
        mp.lineTo(x0 + 10, ybot)
        mp.lineTo(W, ybot)
        mp.lineTo(W, H)
        mp.lineTo(0, H)
        mp.close()
        c.drawPath(mp, lin_paint(0, 300, 0, H, ["#4A423B", "#2A2420", "#16120F"]))
        c.drawRect(R(0, ybot, W, 16), P(GREEN))
        c.drawRect(R(x1 + 120, ybot - 10, W, 20), P(GREEN))
        if not fixed:
            soak = prog(t, T["hold"] - 0.2, T["heavy"] + 0.2)
            bulge = e_in(prog(t, T["heavy"] - 0.2, T["burst"])) * 50
            burst = prog(t, T["burst"], T["burst"] + 0.6)
            c.drawRect(R(x0, ytop, x1 - x0, ybot - ytop), P(mix(SOIL, MUDC, soak)))
            if soak > 0:
                lvl = lerp(ybot, ytop + 40, soak)
                c.drawRect(R(x0, lvl, x1 - x0, ybot - lvl), P("#3B82F6", 0.35 * soak))
            c.drawRect(R(x0, ytop - 30, x1 - x0, 32), P(GREEN))
            for j in range(10):                                      # the retaining wall, bulging
                yy = ytop + j * 51
                u = (yy - ytop) / (ybot - ytop)
                bx = math.sin(u * math.pi) * bulge
                off = 0.0
                if burst > 0 and 3 <= j <= 7:
                    off = burst * (120 + j * 30)
                c.drawRRect(rr(x1 + bx + off, yy + off * 0.4 * (j % 2), 90, 48, 6), P(GRANITE))
                c.drawRRect(rr(x1 + bx + off, yy + off * 0.4 * (j % 2), 90, 48, 6), P(GRANITE_D, stroke=3))
            if burst > 0:
                sp = skia.Path()
                sp.moveTo(x1, ytop + 150)
                sp.quadTo(x1 + 200 * burst, ytop + 300, x1 + 260 * burst, ybot)
                sp.lineTo(x1, ybot)
                sp.close()
                c.drawPath(sp, P(MUDC, burst))
        else:
            c.drawRect(R(x0, ytop, x1 - x0, ybot - ytop), P("#1E1712"))
            k = prog(t, T["layers"] - 0.3, T["topsoil"] + 0.2)
            bands = [("stones", 0.3, "#8F8A80"), ("gravel", 0.22, "#A8A29E"), ("sand", 0.2, "#D6B97A"),
                     ("topsoil", 0.28, SOIL)]
            yb = ybot
            keys = (T["stones"], T["gravel"], T["sand"], T["topsoil"])
            for i, (nm, frac, col) in enumerate(bands):
                hh = (ybot - ytop) * frac
                kk = prog(t, keys[i] - 0.35, keys[i] + 0.1)
                if kk <= 0:
                    yb -= hh
                    continue
                c.drawRect(R(x0, yb - hh * kk, x1 - x0, hh * kk), P(col))
                rng = random.Random(i)
                if nm == "stones":
                    for _ in range(26):
                        c.drawCircle(rng.uniform(x0 + 30, x1 - 30), rng.uniform(yb - hh * kk + 20, yb - 20), rng.uniform(22, 38),
                                     P(rng.choice(["#9CA3AF", "#6B7280", "#A8A29E"])))
                elif nm == "gravel":
                    for _ in range(140):
                        c.drawCircle(rng.uniform(x0 + 6, x1 - 6), rng.uniform(yb - hh * kk + 6, yb - 6), rng.uniform(5, 10),
                                     P(rng.choice(["#78716C", "#57534E", "#D6D3D1"])))
                elif nm == "sand":
                    for _ in range(200):
                        c.drawCircle(rng.uniform(x0 + 4, x1 - 4), rng.uniform(yb - hh * kk + 4, yb - 4), 2.5, P("#B08A4A"))
                yb -= hh
            if k >= 0.95:
                c.drawRect(R(x0, ytop - 30, x1 - x0, 32), P(GREEN))
                for q in range(8):
                    c.drawCircle(x0 + 50 + q * 90, ytop - 36, 16, P("#6DAA4A"))
            for j in range(10):
                yy = ytop + j * 51
                c.drawRRect(rr(x1, yy, 90, 48, 6), P(GRANITE))
                c.drawRRect(rr(x1, yy, 90, 48, 6), P(GRANITE_D, stroke=3))
            c.drawRect(R(x1, ybot - 40, 90, 34), P("#1A1612"))      # the drain at the foot
            rk = prog(t, T["runs"] - 0.5, T["runs"])
            if rk > 0:
                for i in range(14):
                    q = (t * 0.7 + i / 14.0) % 1.0
                    px = x0 + 40 + (i * 53) % int(x1 - x0 - 80)
                    py = lerp(ytop - 200, ybot - 20, q)
                    c.drawCircle(px, py, 9, P("#7DD3FC", 0.9 * rk))
                for i in range(3):
                    q = (t * 1.2 + i / 3.0) % 1.0
                    c.drawCircle(x1 + 90 + q * 120, ybot - 24 + q * q * 80, 10, P("#7DD3FC", rk * (1 - q)))
        rain(c, -100, W + 100, -100, H, t, a=0.7 if not fixed else 0.5, n=80, seed=6)
        self.ui["box"] = (x0, x1, ytop, ybot)

    def ui_layers(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, x1, ytop, ybot = self.ui.get("box", (120.0, 820.0, 640.0, 1150.0))
        if tw < s("fix2") - 0.12:
            self.chip(540, 420, "hold", T["hold"] - 0.15, T["heavy"] - 0.15, accent="#7DD3FC", size=40)
            self.chip(540, 420, "heavy", T["heavy"] - 0.15, T["burst"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 420, "burst", T["burst"] - 0.1, s("fix2") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["burst"] + 0.05, s("fix2") - 0.2, x=880, y=520)
            self.red(T["burst"], 1.3)
            return
        fr = (0.3, 0.22, 0.2, 0.28)
        keys = (("stones", T["stones"]), ("gravel", T["gravel"]), ("sand", T["sand"]), ("topsoil", T["topsoil"]))
        yb = ybot
        for (key, t0), f_ in zip(keys, fr):
            hh = (ybot - ytop) * f_
            self.chip(470, yb - hh / 2, key, t0 - 0.2, s("break3") - 0.15, accent="#E2E8F0", size=32)
            yb -= hh
        self.chip(540, 420, "runs", T["runs"] - 0.2, s("break3") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["runs"] + 0.1, s("break3") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: water (break3, fix3)
    def draw_water(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        v2.sky(c, W, H, 0.0, pal=MIST, horizon_y=H * 0.5)
        c.drawRect(R(0, 700, W, H - 700), lin_paint(0, 700, 0, H, ["#3F6B3A", "#24402A", "#0E1A12"]))
        huayna(c, 820, 760, 0.55)
        n = 7
        for i in range(n):                                          # stone stairs going down to the right
            sx, sy = 40 + i * 140, 560 + i * 90
            c.drawRect(R(sx, sy, 140, 1300 - sy), lin_paint(0, sy, 0, 1300, ["#8F8B83", "#4F4B45"]))
            c.drawRect(R(sx, sy, 140, 14), P(GRANITE_L))
            c.drawLine(sx, sy, sx, sy + 90, P(GRANITE_D, stroke=3))
            for j in range(int((1300 - sy) / 40)):
                yy = sy + 30 + j * 40
                c.drawLine(sx, yy, sx + 140, yy, P("#3F3B36", 0.6, stroke=3))
                xo = sx + (35 if j % 2 else 75)
                c.drawLine(xo, yy, xo, yy + 40, P("#3F3B36", 0.5, stroke=3))
        if not fixed:
            fk = prog(t, T["water"] - 0.1, T["floods"] + 0.4)
            if fk > 0:
                fp = skia.Path()                                      # a flood wave rushing down the stairs
                fx_ = lerp(-200, 1100, fk)
                fp.moveTo(-50, 520)
                fp.quadTo(fx_ * 0.6, 520 + fx_ * 0.6, fx_, 560 + fx_ * 0.66)
                fp.lineTo(fx_ - 60, 1300)
                fp.lineTo(-50, 1300)
                fp.close()
                c.drawPath(fp, lin_paint(0, 500, 0, 1300, ["#93C5FD", "#2563EB"], a=0.8 * prog(t, T["floods"] - 0.6, T["floods"])))
                for k in range(10):
                    q = (t * 1.5 + k / 10.0) % 1.0
                    c.drawCircle(lerp(0, fx_, q), 520 + lerp(0, fx_, q) * 0.62, 12, P("#F8FAFC", 0.7 * prog(t, T["floods"] - 0.6, T["floods"])))
        else:
            ck = prog(t, T["canal"] - 0.3, T["canal"] + 0.3)
            if ck > 0:                                                # the canal along the top
                c.drawRect(R(0, 470, 260 * ck + 40, 26), P(GRANITE_D))
                c.drawRect(R(0, 476, 260 * ck + 40, 14), P("#38BDF8"))
            fk = prog(t, T["fountains"] - 0.4, T["drain"])
            for i in range(n):
                sx, sy = 40 + i * 140, 560 + i * 90
                if i / n <= fk:
                    c.drawRect(R(sx + 30, sy - 24, 80, 26), P(GRANITE_D))
                    c.drawRect(R(sx + 36, sy - 18, 68, 14), P("#38BDF8"))
                    if i < n - 1:                                     # water pours into the next basin
                        pp = skia.Path()
                        pp.moveTo(sx + 104, sy - 12)
                        pp.quadTo(sx + 150, sy + 10, sx + 172, sy + 66)
                        c.drawPath(pp, P("#7DD3FC", 0.95, stroke=10))
            dk = prog(t, T["drain"] - 0.3, T["storms"])
            if dk > 0:                                                # drain holes spouting into the main drain
                for i in range(n):
                    sx, sy = 40 + i * 140, 560 + i * 90
                    hx, hy = sx + 70, sy + 50
                    c.drawRect(R(hx - 12, hy - 10, 24, 20), P("#14110E"))
                    q = (t * 1.4 + i * 0.2) % 1.0
                    for j in range(3):
                        qq = (q + j / 3.0) % 1.0
                        c.drawCircle(hx + qq * 40, hy + qq * qq * 90, 7, P("#93C5FD", dk * (1 - qq)))
                c.drawRect(R(0, 1180, W, 40), P("#1E3A5F", dk))
                c.drawRect(R(0, 1186, W, 26), P("#3B82F6", 0.8 * dk))
        rain(c, -100, W + 100, -100, H, t, a=0.4, n=60, seed=9)

    def ui_water(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 420, "floods", T["floods"] - 0.15, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["floods"] + 0.05, s("fix3") - 0.2, x=880, y=520)
            self.red(T["floods"] + 0.05, 1.3)
            return
        self.chip(540, 420, "canal", T["canal"] - 0.15, T["sixteen"] - 0.1, accent="#7DD3FC", size=42)
        self.chip(540, 420, "f16", T["sixteen"] - 0.1, T["drain"] - 0.15, accent=HILITE, size=42)
        self.chip(540, 420, "drains", T["drain"] - 0.15, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["storms"] + 0.1, s("break4") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: quake (break4)
    def draw_quake(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, -300, 0.78)
        qk = prog(t, T["quake"] - 0.2, T["quake"] + 0.2)
        self.world(c, t, cam, rain_a=0.0, palaces=1.0, lit=0.35, quake=qk, faults=prog(t, T["fault"] - 0.3, T["fault"] + 0.2))

    def ui_quake(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "fault", T["fault"] - 0.15, T["quake"] - 0.1, accent=WARN, size=44)
        self.chip(540, 420, "quake", T["quake"] - 0.1, T["cut"] - 0.15, accent=WARN, size=44)
        self.badge("alert", T["shaking"] + 0.05, T["cut"] - 0.2, x=880, y=520)
        self.red(T["quake"], 1.4)

    # ------------------------------------------------------------------ set: stones (fix4, cta)
    def draw_stones(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1B2A33", "#24323A", "#121A20"])
        add_glow(c, 300, 300, 700, "#F2C08C", 0.18)
        ox, oy = 140.0, 560.0
        jig = prog(t, T["doors"] + 0.2, T["doors"] + 0.4) * (1 - prog(t, T["doors"] + 1.0, T["doors"] + 1.8))
        stones = ashlar_stones()
        c.drawRect(R(ox - 10, oy - 10, 820, 620), P("#2A2622"))
        for i, pts in enumerate(stones):
            dx = math.sin(t * 50 + i * 1.7) * 7 * jig
            dy = math.cos(t * 43 + i) * 5 * jig
            stone_poly(c, [(ox + px, oy + py) for px, py in pts], dx, dy, "#8E8A80")
        pk = prog(t, T["paper"] - 0.35, T["slip"] + 0.1)
        if pk > 0 and t < T["lean"] - 0.2:                          # a sheet of paper that won't go in
            jx, jy = ox + 380, oy + 190
            push = e_out(pk)
            c.save()
            c.translate(jx + 240 - 200 * push, jy - 200 + 170 * push)
            c.rotate(-38)
            bend = prog(t, T["slip"] - 0.1, T["slip"] + 0.3)
            pp = skia.Path()
            pp.moveTo(0, 0)
            pp.lineTo(220, 0)
            pp.quadTo(240, 80 * bend, 220, 150)
            pp.lineTo(0, 150)
            pp.close()
            c.drawPath(pp, P("#F8FAFC", 0.97))
            for k in range(5):
                c.drawLine(24, 26 + k * 24, 190, 26 + k * 24, P("#CBD5E1", stroke=3))
            c.restore()
            if bend > 0.3:
                c.drawCircle(jx, jy, 46, P(WARN, stroke=9))
                c.drawLine(jx - 30, jy - 30, jx + 30, jy + 30, P(WARN, stroke=9))
                c.drawLine(jx + 30, jy - 30, jx - 30, jy + 30, P(WARN, stroke=9))
        dk = prog(t, T["lean"] - 0.35, T["lean"] + 0.1)
        if dk > 0:                                                  # a trapezoid doorway leaning inward
            c.drawRect(R(0, 0, W, H), P("#0B1220", 0.55 * dk))
            cx_, by = 540, 1180
            wall = R(cx_ - 330, 560, 660, 620)
            c.drawRect(wall, lin_paint(cx_ - 330, 0, cx_ + 330, 0, [GRANITE_L, GRANITE, GRANITE_D], a=dk))
            for j in range(12):
                yy = 560 + j * 52
                c.drawLine(cx_ - 330, yy, cx_ + 330, yy, P(GRANITE_D, 0.6 * dk, stroke=3))
            dp = skia.Path()
            dp.moveTo(cx_ - 150, by)
            dp.lineTo(cx_ - 95, 700)
            dp.lineTo(cx_ + 95, 700)
            dp.lineTo(cx_ + 150, by)
            dp.close()
            c.drawPath(dp, P("#14110E", dk))
            c.drawRect(R(cx_ - 120, 680, 240, 30), P(GRANITE_L, dk))
            arrow(c, cx_ - 220, by - 60, cx_ - 130, 760, HILITE, a=dk, w=10, head=28)
            arrow(c, cx_ + 220, by - 60, cx_ + 130, 760, HILITE, a=dk, w=10, head=28)
        self.ui["ox"] = ox

    def ui_stones(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("cta") - 0.12:
            self.chip(540, 420, "tight", T["cut"] - 0.1, T["paper"] - 0.2, accent=HILITE, size=40)
            self.chip(540, 420, "paper", T["paper"] - 0.2, T["lean"] - 0.2, accent=WARN, size=40)
            self.chip(540, 420, "lean", T["lean"] - 0.2, s("cta") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["doors"] + 0.1, s("cta") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: ac (tag)
    def draw_ac(self, c, t):
        T = self.T
        facade(c, t)
        ax, ay = 760, 540
        window_ac(c, ax, ay, 1.1, t)
        walk = prog(t, T["neighbor"] - 0.8, T["drips"])
        px = lerp(150, ax + 60, e_out(walk))
        look = prog(t, T["drips"] + 0.15, T["drips"] + 0.4)
        person(c, px, 1160, 230, "#2563EB", t, pose="walk" if walk < 1 else ("look" if look < 0.5 else "shrug"), face=1,
               hat="none", hair="#1C1917")
        for k in range(4):                                          # drips from the AC
            q = (t * 1.1 + k / 4.0) % 1.0
            dy = lerp(ay + 70, 900, q * q)
            c.drawCircle(ax + 60, dy, 9, P("#7DD3FC", 0.95))
        hk = prog(t, T["drips"], T["head"] + 0.3)
        if hk > 0 and walk >= 1:
            v2set.splash(c, ax + 60, 910, t, t - (t % 0.9), dur=0.5, n=8, speed=180, col="#BAE6FD")

    def ui_ac(self, c, t, tw):
        T = self.T
        self.chip(540, 160 + 260, "planned", T["drop"] - 0.15, T["neighbor"] - 0.2, accent=GOOD, size=40)
        k = self.span(T["drips"] - 0.1, self.duration + 1)
        if k > 0:
            v2.chip(c, 540, 420, self.L["drip"], k, accent=WARN, size=56)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=MIST, horizon_y=H * 0.6)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(3.0, 61), -20), (0.1, rumble(1.6, 62), -20), (T["knife"] + 0.5, sfx.whoosh(0.5, False, 63), -17),
              (T["two"], sfx.pop(64), -10), (T["slid"], sfx.ding(), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 65), -9), (T["machu"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["mud"], sfx.hiss(1.2, 67), -12),
               (T["slides"], rumble(1.4, 68), -6), (T["slides"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4)]
        for k in range(9):
            ev.append((T["carve"] + k * 0.18, sfx.thud(0.15, 70 + k % 3), -12))
        ev += [(T["wall"] + 0.1, sfx.ding(), -8), (T["wall"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["soaked"], sfx.hiss(1.0, 74), -14),
               (T["heavy"], sfx.creak(1.0), -10), (T["burst"], boom(1.2, 75), -6),
               (T["burst"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["stones"], sfx.thud(0.3), -10), (T["gravel"], sfx.click(76), -10), (T["sand"], sfx.hiss(0.5, 77), -14),
               (T["topsoil"], sfx.thud(0.25), -12), (T["runs"] + 0.1, sfx.ding(), -8), (T["runs"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["floods"] - 0.4, sfx.hiss(1.6, 79), -8),
               (T["floods"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["canal"], sfx.hiss(1.2, 80), -14), (T["fountains"], sfx.sparkle(0.6, 8, 81), -10),
               (T["drain"], sfx.hiss(1.0, 82), -14), (T["storms"] + 0.1, sfx.ding(), -8), (T["storms"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 83), -4), (T["fault"], sfx.buzz(0.4), -12),
               (T["quake"] - 0.1, rumble(2.2, 84), -4), (T["shaking"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["cut"] - 0.12, sfx.whoosh(0.4, False, 85), -4), (T["tight"], sfx.lock_click(86), -8),
               (T["paper"], sfx.whoosh(0.3, False, 87), -12), (T["slip"], sfx.snap(88), -12),
               (T["lean"], sfx.thunk(89), -8), (T["doors"] + 0.25, rumble(0.9, 90), -12),
               (T["doors"] + 0.1, sfx.ding(), -8), (T["doors"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(91), 0), (T["follow"] - 0.15, sfx.pop(92), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 93), -6), (T["palaces"], sfx.thud(0.3), -10),
               (T["emperor"], sfx.sparkle(0.6, 8, 94), -10), (T["spanish"], sfx.womp(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 95), -6), (T["s1"], sfx.pop(96), -3), (T["s2"], sfx.pop(97), -3),
               (T["s3"], sfx.pop(98), -3)]
        ev += [(T["cong2"], sfx.pop(99), -2), (T["cong2"], sfx.sparkle(1.0, 14, 100), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 101), -6), (T["drop"], sfx.tap(102), -8), (T["neighbor"], sfx.hum(1.4), -14)]
        for k in range(4):
            ev.append((T["drips"] + k * 0.27, sfx.tap(103 + k), -6))
        ev += [(T["head"] + 0.1, sfx.womp(), -8)]
        return ev


NAME = "machupicchu"
EPISODE = MachuPicchu
