"""Episode 39 - A Japanese five-storey pagoda that survives earthquakes.  v2 look: a wooden pagoda in a garden at dusk,
Mount Fuji behind, red maples in front.

Sets: temple (hook: the ground shakes and the five storeys sway like a snake, each the opposite way to the next, and it
stands; the reveal: painted red, Tokyo Skytree rises far away with the same centre column; the stat and the closer),
quake (break1: a stiff stone tower cracks and falls; fix1: a wooden joint that bends, twists and rubs, almost no nails),
xray (break2: one rigid tower whips at the top like a fishing rod; fix2: five loose boxes, each swaying opposite to the
next; break3: one floor swings too far and slides off; fix3: the giant trunk up the middle, a floor bumps it and comes
back), eaves (break4: rain and snow on bare walls, they rot; fix4: wide eaves keep the walls dry and steady the tower
like a tightrope walker's pole), home (the tag: a Jenga tower and a sneeze in English, a stack of dishes in the sink and
mom's look in Arabic).
World (temple, eaves): front view, the ground is y = 0; the pagoda is about 1,060 units tall.
"""
from v2_base import *  # noqa: F401,F403
from bullettrain import fuji  # noqa: E402
from phone import mom  # noqa: E402

DUSK = {"top": "#0B0B26", "upper": "#22184A", "mid": "#5A2E6A", "low": "#C25A6A", "horizon": "#F59E8B",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
WOOD = "#8B5A2B"
WOOD_D = "#5C3A1A"
VERM = "#D9381E"
WALL = "#EFE6D2"
TILE = "#2F3646"
TILE_L = "#6B7486"
TRUNK = "#A0662E"
NST = 5
BH, SH = 112.0, 162.0           # body height, storey pitch
BASE_Y = -44.0                  # top of the stone platform


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


# ====================================================================================== pieces
def storey_y(i):
    """(bottom of the body, bottom of the roof = top of the body, top of the roof) of storey i (0 = ground floor)."""
    yb = BASE_Y - i * SH
    return yb, yb - BH, yb - SH


def roof(c, cx, y0, y1, half, upturn=26.0, a=1.0, wet=0.0):
    """A tiled roof from y0 (eave line) up to y1, half-width 'half', corners turned up."""
    p = skia.Path()
    p.moveTo(cx - half - 8, y0 - upturn)
    p.quadTo(cx - half * 0.7, y0 + 4, cx - half * 0.35, y0 + 2)
    p.lineTo(cx + half * 0.35, y0 + 2)
    p.quadTo(cx + half * 0.7, y0 + 4, cx + half + 8, y0 - upturn)
    p.lineTo(cx + half * 0.42, y1 + 8)
    p.lineTo(cx - half * 0.42, y1 + 8)
    p.close()
    col = mix(TILE, "#1E2533", wet * 0.5)
    c.drawPath(p, lin_paint(0, y1, 0, y0, [shade(col, 0.12), col], a=a))
    for k in range(1, 7):                                            # tile rows
        u = k / 7.0
        yy = lerp(y0, y1 + 8, u)
        hw = lerp(half * 0.9, half * 0.42, u)
        c.drawLine(cx - hw, yy, cx + hw, yy, P(TILE_L, 0.35 * a, stroke=2.5))
    c.drawLine(cx - half * 0.35, y0 + 3, cx + half * 0.35, y0 + 3, P(VERM, 0.85 * a, stroke=6))   # the red rafter ends


def body(c, cx, yb, yt, half, red=1.0, rot=0.0, a=1.0, xray=0.0):
    wall = mix(WALL, "#5B4636", rot * 0.8)
    post = mix(WOOD, VERM, red)
    c.drawRect(R(cx - half, yt, half * 2, yb - yt), P(wall, a * (1 - xray * 0.75)))
    if rot > 0.02:                                                   # rot stains creeping up the walls
        rng = random.Random(int(cx * 3 + yb))
        for i in range(7):
            c.drawOval(R(cx - half + rng.uniform(0, half * 2 - 40), yb - rng.uniform(20, BH * 0.8) * rot, 40, 50 * rot),
                       P("#3F3A1E", 0.55 * rot * a))
    for k in (-1, -0.33, 0.33, 1):
        c.drawRect(R(cx + k * half - 8, yt, 16, yb - yt), P(post, a))
    c.drawRect(R(cx - half, yt, half * 2, 12), P(post, a))
    c.drawRect(R(cx - half, yb - 10, half * 2, 10), P(shade(post, -0.2), a))
    if xray < 0.5:
        c.drawRect(R(cx - half * 0.22, yt + 26, half * 0.44, BH - 40), P("#3B2410", a))
        for k in range(1, 4):
            c.drawLine(cx - half * 0.22 + k * half * 0.11, yt + 26, cx - half * 0.22 + k * half * 0.11, yb - 14,
                       P("#B08968", a, stroke=3))


def pagoda(c, x, y, s, t, offs=(0, 0, 0, 0, 0), red=0.0, eave=1.0, rot=0.0, xray=0.0, trunk=0.0, wet=0.0, a=1.0,
           gone=-1, gone_dx=0.0, gone_dy=0.0, gone_rot=0.0):
    """Five storeys, base centre at (x, y), scale s. offs = sideways sway of each storey. 'gone' = index of a storey
    that slides off (moved by gone_dx / gone_dy, turned by gone_rot)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-250, BASE_Y, 500, -BASE_Y), lin_paint(0, BASE_Y, 0, 0, ["#9CA3AF", "#4B5563"], a=a))   # stone base
    c.drawRect(R(-262, BASE_Y - 6, 524, 10), P("#D1D5DB", a))
    def draw_trunk():
        top = storey_y(NST - 1)[2] - 150
        c.drawRect(R(-17, top, 34, -top + BASE_Y + 30), lin_paint(-17, 0, 17, 0, [shade(TRUNK, 0.15), TRUNK, shade(TRUNK, -0.3)], a=a * trunk))
        for k in range(12):
            yy = lerp(top, BASE_Y, k / 12.0)
            c.drawLine(-12, yy, -4, yy + 30, P(shade(TRUNK, -0.35), 0.6 * a * trunk, stroke=2))
        add_glow(c, 0, (top + BASE_Y) / 2, 260, "#FDBA74", 0.18 * trunk * a)
    if trunk > 0 and xray < 0.3:
        draw_trunk()
    for i in range(NST):
        yb, yt, yr = storey_y(i)
        half = 150 - i * 17
        ox = offs[i] if i < len(offs) else 0.0
        c.save()
        if i == gone:
            c.translate(gone_dx, gone_dy)
            c.rotate(gone_rot)
        c.translate(ox, 0)
        body(c, 0, yb, yt, half, red=red, rot=rot, a=a, xray=xray)
        if trunk > 0 and xray > 0.3:                                 # the hole each floor leaves around the trunk
            c.drawRect(R(-30, yt + 8, 60, yb - yt - 10), P("#0F172A", 0.6 * xray * a))
        rh = half + 30 + 120 * eave
        roof(c, 0, yt, yr, rh, upturn=26 * (0.4 + 0.6 * eave), a=a, wet=wet)
        c.restore()
    if trunk > 0 and xray >= 0.3:                                    # x-ray: the trunk shows through every floor
        draw_trunk()
    # the spire: nine rings on a pole above the top roof
    ox = offs[NST - 1] if len(offs) >= NST else 0.0
    top = storey_y(NST - 1)[2]
    if gone != NST - 1:
        c.drawRect(R(ox - 7, top - 210, 14, 212), P("#B45309", a))
        for k in range(9):
            yy = top - 30 - k * 17
            c.drawOval(R(ox - 26 + k * 0.8, yy - 5, 52 - k * 1.6, 10), P("#D97706", a))
        c.drawCircle(ox, top - 222, 12, P("#FBBF24", a))
    c.restore()


def maple(c, x, y, s, t, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawLine(0, 0, -6, -160, P("#3B2410", a, stroke=18))
    c.drawLine(-6, -120, -60, -190, P("#3B2410", a, stroke=10))
    c.drawLine(-4, -140, 50, -210, P("#3B2410", a, stroke=10))
    rng = random.Random(int(x))
    for i in range(16):
        bx, by = rng.uniform(-120, 110), rng.uniform(-300, -150)
        c.drawCircle(bx + math.sin(t + i) * 3, by, rng.uniform(34, 56), P(rng.choice(["#DC2626", "#B91C1C", "#EA580C", "#F97316"]), 0.92 * a))
    c.restore()


def lantern_stone(c, x, y, s, a=1.0, glow=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-14, -90, 28, 90), P("#6B7280", a))
    c.drawRect(R(-40, -112, 80, 22), P("#9CA3AF", a))
    c.drawRect(R(-30, -170, 60, 58), P("#6B7280", a))
    c.drawRect(R(-16, -158, 32, 34), P("#FDE68A", a * glow))
    tri = skia.Path()
    tri.moveTo(-56, -168)
    tri.lineTo(56, -168)
    tri.lineTo(0, -215)
    tri.close()
    c.drawPath(tri, P("#9CA3AF", a))
    c.restore()
    add_glow(c, x, y - 141 * s, 70 * s, "#FDE68A", 0.5 * a * glow)


def skytree(c, x, y, s, t, core=0.0, a=1.0):
    """Tokyo Skytree in the distance: a tapering lattice tower, two observation decks, an antenna; its centre column."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = skia.Path()
    p.moveTo(-70, 0)
    p.lineTo(-18, -1300)
    p.lineTo(18, -1300)
    p.lineTo(70, 0)
    p.close()
    c.drawPath(p, P("#CBD5E1", 0.85 * a))
    for k in range(28):
        yy = -k * 46
        hw = lerp(70, 18, k / 28.0)
        c.drawLine(-hw, yy, hw * 0.9, yy - 46, P("#64748B", 0.6 * a, stroke=2))
        c.drawLine(hw, yy, -hw * 0.9, yy - 46, P("#64748B", 0.6 * a, stroke=2))
    for (yy, w) in ((-700, 90), (-900, 62)):
        c.drawRRect(rr(-w, yy - 30, w * 2, 40, 12), P("#E2E8F0", a))
        c.drawRect(R(-w + 6, yy - 18, w * 2 - 12, 10), P("#38BDF8", 0.8 * a))
    c.drawRect(R(-5, -1600, 10, 300), P("#E2E8F0", a))
    if core > 0:
        c.drawRect(R(-8, -1000, 16, 1000), P("#FDBA74", core * a))
        add_glow(c, 0, -500, 260, "#FDBA74", 0.4 * core * a)
    c.restore()


def jenga(c, x, y, s, t, fall=0.0, a=1.0):
    """A Jenga tower on a table, front view; fall 0..1 topples it."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rng = random.Random(4)
    n = 16
    for k in range(n):
        yy = -(k + 1) * 30
        lean = fall * (k / n) ** 1.5
        dx = lean * 420 + (fall ** 2) * rng.uniform(-60, 120) * (k / n)
        dy = (fall ** 2) * (n - k) * 22 * (k / n)
        c.save()
        c.translate(dx, yy + dy)
        c.rotate(fall * rng.uniform(10, 70) * (k / n))
        if k % 2 == 0:
            c.drawRect(R(-75, 0, 150, 28), P("#D9AE6F", a))
            c.drawRect(R(-75, 0, 150, 28), P("#8A5A2B", a, stroke=2))
        else:
            for j in range(3):
                c.drawRect(R(-75 + j * 50, 0, 48, 28), P("#DDB377", a))
                c.drawRect(R(-75 + j * 50, 0, 48, 28), P("#8A5A2B", a, stroke=2))
        c.restore()
    c.restore()


def dishes(c, x, y, s, t, fall=0.0, a=1.0):
    """A tall stack of plates and cups in a sink; fall 0..1 topples it."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rng = random.Random(9)
    n = 15
    for k in range(n):
        yy = -k * 26
        dx = fall * 380 * (k / n) ** 1.4 + (fall ** 2) * rng.uniform(-40, 80) * (k / n)
        dy = (fall ** 2) * (n - k) * 16 * (k / n)
        c.save()
        c.translate(dx + math.sin(k * 1.7) * 8, yy + dy)
        c.rotate(fall * rng.uniform(-40, 70) * (k / n))
        if k % 4 == 3:
            c.drawRRect(rr(-30, -40, 60, 44, 10), P("#CBD5E1", a))
            c.drawRRect(rr(26, -30, 18, 22, 8), P("#CBD5E1", a, stroke=6))
        else:
            c.drawOval(R(-90, -12, 180, 24), P("#D6DEE8", a))
            c.drawOval(R(-90, -12, 180, 24), P("#64748B", a, stroke=3))
        c.restore()
    c.restore()


# ====================================================================================== the episode
class Pagoda(EpisodeV2):
    BUILD_NO = 39
    FIRST_SET = "temple"
    CLEAR = "#100C24"
    TITLE = {"en": "JAPANESE PAGODA", "ar_sa": "الباجودا اليابانية"}
    EMPH = {"en": ["CONGRATS", "STACK", "FIVE", "WOODEN", "ROOFS", "SWAYS", "SNAKE", "EARTHQUAKE", "NEVER", "FALLS",
                   "JAPANESE", "PAGODA", "JAPAN", "SHAKES", "STIFF", "STONE", "CRACKS", "WOOD", "BENDS", "NAILS",
                   "THOUSAND", "JOINTS", "TWIST", "RUB", "TALL", "WHIPS", "FISHING", "ROD", "LOCK", "BOXES",
                   "OPPOSITE", "FAR", "SLIDES", "GIANT", "TREE", "TRUNK", "MIDDLE", "BUMPS", "BACK", "RAIN", "SNOW",
                   "ROT", "WIDE", "EAVES", "DRY", "STEADY", "TIGHTROPE", "POLE", "FOLLOW", "PANAMA", "CANAL", "LOCKS",
                   "RED", "THIRTEEN", "CENTURIES", "TOKYO", "SKYTREE", "COPY", "HUNDRED", "TWO", "FOURTEEN",
                   "YOURSELF", "STANDING", "JENGA", "SNEEZED"],
            "ar_sa": ["مبروك", "رصيت", "خمس", "سقوف", "خشب", "بيتلوى", "التعبان", "الزلزال", "ومبيقعش", "الباجودا",
                      "اليابانية", "اليابان", "بتتهز", "الحجر", "الناشف", "بيتشرخ", "ويقع", "يتني", "مسامير", "ألف",
                      "وصلة", "بتتلوى", "وتتحك", "السنارة", "فمتربطش", "صناديق", "عكس", "زيادة", "هيتزحلق", "جذع",
                      "شجرة", "النص", "يخبط", "ويرجع", "المطر", "والتلج", "بيبوظوا", "رفرف", "عريض", "يحمي", "يوازن",
                      "الحبل", "تابعني", "هويس", "بنما", "أحمر", "حلقات", "تلتاشر", "قرن", "طوكيو", "ينقل", "واتنين",
                      "أربعتاشر", "بإيدك", "واقفة", "المواعين", "وقع", "نظرة", "أمك"]}
    KEYS = {"ar_sa": {
        ("hook", "STACK"): "رصيت", ("hook", "FIVE"): "خمس", ("hook", "SWAYS"): "بيتلوى", ("hook", "SNAKE"): "التعبان",
        ("hook", "EARTHQUAKE"): "الزلزال", ("hook", "NEVER"): "ومبيقعش", ("hook", "CONGRATS"): "مبروك",
        ("hook", "PAGODA"): "الباجودا",
        ("break1", "JAPAN"): "اليابان", ("break1", "SHAKES"): "بتتهز", ("break1", "STONE"): "الحجر",
        ("break1", "CRACKS"): "بيتشرخ", ("break1", "FALLS"): "ويقع",
        ("fix1", "WOOD"): "خشب", ("fix1", "BENDS"): "يتني", ("fix1", "NAILS"): "مسامير", ("fix1", "THOUSAND"): "ألف",
        ("fix1", "TWIST"): "بتتلوى", ("fix1", "RUB"): "وتتحك",
        ("break2", "WHIPS"): "بتتهز", ("break2", "ROD"): "السنارة",
        ("fix2", "LOCK"): "فمتربطش", ("fix2", "BOXES"): "صناديق", ("fix2", "OPPOSITE"): "عكس",
        ("break3", "FAR"): "زيادة", ("break3", "SLIDES"): "هيتزحلق",
        ("fix3", "TRUNK"): "جذع", ("fix3", "MIDDLE"): "النص", ("fix3", "BUMPS"): "يخبط", ("fix3", "COMES"): "ويرجع",
        ("break4", "RAIN"): "المطر", ("break4", "SNOW"): "والتلج", ("break4", "ROT"): "بيبوظوا",
        ("fix4", "EAVES"): "رفرف", ("fix4", "DRY"): "يحمي", ("fix4", "STEADY"): "يوازن", ("fix4", "TIGHTROPE"): "الحبل",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "RED"): "أحمر", ("reveal", "TOKYO"): "طوكيو", ("reveal", "COPY"): "ينقل",
        ("stat", "THIRTEEN"): "تلتاشر", ("stat", "THOUSAND"): "ألف", ("stat", "TWO"): "واتنين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STANDING"): "واقفة", ("tag", "JENGA"): "المواعين", ("tag", "FELL"): "وقع", ("tag", "SNEEZED"): "نظرة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Panama Canal locks"),
                   "stat": [("1,300", "YEARS STANDING"), ("1,000", "WOODEN JOINTS"), ("2", "LOST IN 1,400 YEARS")],
                   "L": {"five": "5 WOODEN ROOFS", "snake": "SWAYS LIKE A SNAKE", "never": "NEVER FALLS",
                         "pagoda": "JAPANESE PAGODA", "shakes": "JAPAN SHAKES", "stiff": "STIFF STONE: CRACKS",
                         "wood": "WOOD BENDS BACK", "nails": "ALMOST NO NAILS", "joints": "1,000 JOINTS TWIST AND RUB",
                         "whip": "WHIPS LIKE A FISHING ROD", "loose": "FLOORS NOT LOCKED", "opp": "EACH SWAYS THE OTHER WAY",
                         "far": "TOO FAR...", "slides": "IT SLIDES OFF", "trunk": "A GIANT TREE TRUNK",
                         "bump": "BUMPS IT, COMES BACK", "rot": "RAIN AND SNOW ROT THE WALLS", "eaves": "WIDE EAVES",
                         "dry": "WALLS STAY DRY", "pole": "LIKE A TIGHTROPE POLE", "red": "PAINT IT RED",
                         "sky": "TOKYO SKYTREE, 634 m", "core": "SAME IDEA: A CENTRE COLUMN",
                         "still": "1,400 YEARS OF QUAKES: STANDING", "achoo": "ACHOO!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: هويس قناة بنما"),
                      "stat": [("1,300", "سنة واقفة"), ("1,000", "وصلة خشب"), ("2", "بس وقعوا في 1,400 سنة")],
                      "L": {"five": "خمس سقوف خشب", "snake": "بيتلوى زي التعبان", "never": "ومبيقعش",
                            "pagoda": "الباجودا اليابانية", "shakes": "اليابان بتتهز", "stiff": "الحجر الناشف بيتشرخ",
                            "wood": "الخشب يتني ويرجع", "nails": "من غير مسامير تقريبًا", "joints": "ألف وصلة بتتلوى",
                            "whip": "راسه بتتهز زي السنارة", "loose": "الأدوار مش مربوطة", "opp": "كل دور عكس اللي تحته",
                            "far": "زيادة...", "slides": "هيتزحلق ويقع", "trunk": "جذع شجرة ضخم",
                            "bump": "يخبط فيه ويرجع", "rot": "المطر والتلج بيبوظوا الخشب", "eaves": "رفرف عريض",
                            "dry": "الحيطان ناشفة", "pole": "زي عصاية اللي ماشي على الحبل", "red": "لونه أحمر",
                            "sky": "طوكيو سكاي تري، 634 متر", "core": "نفس الفكرة: عمود في النص",
                            "still": "1,400 سنة زلازل: لسه واقفة", "achoo": "هاتشو!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stack": ("hook", "STACK", 0.05), "five": ("hook", "FIVE", 0.12), "sways": ("hook", "SWAYS", 0.35),
            "snake": ("hook", "SNAKE", 0.45), "quake": ("hook", "EARTHQUAKE", 0.55), "never": ("hook", "NEVER", 0.65),
            "congrats": ("hook", "CONGRATS", 0.75), "pagoda": ("hook", "PAGODA", 0.92),
            "japan": ("break1", "JAPAN", 0.1), "shakes": ("break1", "SHAKES", 0.25), "stone": ("break1", "STONE", 0.55),
            "cracks": ("break1", "CRACKS", 0.75), "falls": ("break1", "FALLS", 0.9),
            "wood": ("fix1", "WOOD", 0.15), "bends": ("fix1", "BENDS", 0.3), "nails": ("fix1", "NAILS", 0.5),
            "thousand": ("fix1", "THOUSAND", 0.65), "twist": ("fix1", "TWIST", 0.8), "rub": ("fix1", "RUB", 0.92),
            "whips": ("break2", "WHIPS", 0.4), "rod": ("break2", "ROD", 0.85),
            "lock": ("fix2", "LOCK", 0.15), "boxes": ("fix2", "BOXES", 0.55), "opposite": ("fix2", "OPPOSITE", 0.8),
            "far": ("break3", "FAR", 0.5), "slides": ("break3", "SLIDES", 0.85),
            "trunk": ("fix3", "TRUNK", 0.25), "middle": ("fix3", "MIDDLE", 0.4), "bumps": ("fix3", "BUMPS", 0.8),
            "back": ("fix3", "COMES", 0.92),
            "rain": ("break4", "RAIN", 0.2), "snow": ("break4", "SNOW", 0.5), "rot": ("break4", "ROT", 0.75),
            "eaves": ("fix4", "EAVES", 0.25), "dry": ("fix4", "DRY", 0.45), "steady": ("fix4", "STEADY", 0.65),
            "tight": ("fix4", "TIGHTROPE", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "red": ("reveal", "RED", 0.2), "tokyo": ("reveal", "TOKYO", 0.6), "copy": ("reveal", "COPY", 0.88),
            "s1": ("stat", "THIRTEEN", 0.04), "s2": ("stat", "THOUSAND", 0.35), "s3": ("stat", "TWO", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "still": ("tag", "STANDING", 0.3), "jenga": ("tag", "JENGA", 0.55), "fell": ("tag", "FELL", 0.7),
            "sneeze": ("tag", "SNEEZED", 0.9)})
        T["topple"] = max(T["falls"] - 0.3, T["cracks"] + 0.4)
        T["slip"] = max(T["slides"] - 0.4, T["far"] + 0.3)
        T["core_in"] = max(T["trunk"] - 0.2, s("fix3") + 0.05)
        T["bump"] = max(T["bumps"] - 0.25, T["core_in"] + 0.8)
        T["wide"] = max(T["eaves"] - 0.2, s("fix4") + 0.05)
        T["paint"] = max(T["red"] - 0.3, s("reveal") + 0.05)
        T["rise"] = max(T["tokyo"] - 0.5, T["paint"] + 0.6)
        T["kick"] = max(min(T["fell"], T["sneeze"]) - 0.2, T["jenga"] + 0.3) if not self.rtl else max(T["sneeze"] - 0.1, T["fell"])
        # ---- sets
        self.cut(s("break1") - 0.12, "quake", 1)
        self.cut(s("break2") - 0.12, "xray", -1)
        self.cut(s("break4") - 0.12, "eaves", 1)
        self.cut(s("reveal") - 0.12, "temple", -1)
        self.cut(s("tag") - 0.2, "home", 1)
        # ---- cameras
        z0 = 0.82
        cm = Camera(0, -140 / z0, z0)
        cm.key(0.05, 0, -140 / z0 - 6, z0 * 1.02, 2.5)
        cm.key(s("reveal") - 0.12, 0, -230 / 0.8, 0.8, 0.0).key(T["rise"], 260, -290 / 0.55, 0.55, 2.0)
        cm.key(s("stat") - 0.12, 120, -300 / 0.62, 0.62, 0.0)
        cm.key(s("closer") - 0.1, 0, -230 / 0.7, 0.7, 1.0)
        self.cam = cm
        ce = Camera(0, -420, 1.3)
        ce.key(T["steady"] - 0.4, 0, -140 / z0, z0, 1.4)
        self.came = ce
        self.quake_env = Track(0.0).to(0.05, 1.0, 0.6).to(s("break1") - 0.6, 0.25, 0.5)
        self.spans = [(T["falls"], T["rub"] + 0.3), (T["rod"], T["opposite"] + 0.3), (T["slides"], T["back"] + 0.3),
                      (T["rot"], T["tight"] + 0.3)]
        self.shakes = [(0.1, 2.0, 7), (T["never"], 0.4, 6), (T["congrats"], 0.3, 8), (s("break1") + 0.2, 2.2, 9),
                       (T["topple"] + 0.6, 0.4, 12), (T["slip"] + 0.6, 0.35, 10), (T["bump"], 0.25, 6),
                       (T["kick"] + 0.5, 0.3, 8), (s("closer") + 0.2, 0.35, 10)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def sway(self, t, amp=1.0, alt=True):
        """Sideways offsets of the five storeys: the snake dance (alternating) or one rigid lean (alt=False)."""
        ph = math.sin(t * 2 * math.pi * 1.1)
        out = []
        for i in range(NST):
            k = (0.55 + 0.18 * i) * amp
            out.append(ph * k * 22 * ((-1) ** i if alt else (i + 1) * 0.9))
        return tuple(out)

    def garden(self, c, t, cam, sky=0.0):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 60 * z)
        v2.stars(c, W, H, t, 0.6)
        fuji(c, 760 - cx * 0.06, gy - 30 * z, 1100, 520, a=0.9)
        self.view(c, cam)
        vrect(c, cx - 1500 / z, -10, 3000 / z, 3000, ["#3F5A3A", "#2C4228", "#16231A", "#0A100B"], [0, 0.05, 0.3, 1])
        for (mx, ms) in ((-560, 1.1), (520, 1.0), (-900, 0.9), (880, 0.95)):
            maple(c, mx, 10, ms, t)
        lantern_stone(c, -330, 20, 0.9)
        lantern_stone(c, 330, 20, 0.9)
        return gy

    # ------------------------------------------------------------------ set: temple (hook, reveal, stat, closer)
    def draw_temple(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        rv = t >= s("reveal") - 0.12
        self.garden(c, t, cam)
        if rv:
            sk = prog(t, T["rise"], T["rise"] + 1.6)
            c.save()
            c.translate(0, (1 - e_out(sk)) * 900)
            skytree(c, 880, -10, 0.8, t, core=prog(t, T["copy"] - 0.4, T["copy"] + 0.2), a=sk)
            c.restore()
        amp = self.quake_env.at(t) if hook else (0.35 if rv and t < s("stat") - 0.12 else 0.0)
        red = 0.0 if not rv else prog(t, T["paint"], T["paint"] + 0.9)
        pagoda(c, 0, 0, 1.0, t, offs=self.sway(t, amp), red=red, trunk=prog(t, T["copy"] - 0.4, T["copy"] + 0.2) * 0.0)
        if hook:                                                         # seismic waves along the ground
            for i in range(4):
                q = (t * 0.9 + i / 4.0) % 1.0
                c.drawOval(R(-q * 1300, -40 * q, q * 2600, 80 * q), P("#FDE68A", 0.4 * (1 - q) * amp, stroke=6))
        c.restore()
        self.ui["cam"] = cam

    def ui_temple(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            self.chip(540, 1170, "five", T["five"] - 0.1, T["sways"] - 0.1, accent="#FDBA74", size=40)
            self.chip(540, 1170, "snake", T["sways"] - 0.1, T["never"] - 0.1, accent=HILITE, size=40)
            self.chip(540, 1170, "never", T["never"] - 0.1, T["pagoda"] - 0.1, accent=GOOD, size=44)
            self.chip(540, 1170, "pagoda", T["pagoda"] - 0.1, s("break1") + 0.1, accent=HILITE, size=44)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            cam = self.ui.get("cam", self.cam.at(tw))
            self.chip(330, 470, "red", T["red"] - 0.1, T["tokyo"] - 0.1, accent=VERM, size=40)
            sx, sy = self.at(cam, 880, -1100 * 0.8)
            self.label(sx, sy, 560, 470, "sky", T["tokyo"] - 0.1, T["copy"] - 0.1, "#E2E8F0", size=34)
            cx_, cy_ = self.at(cam, 880, -600 * 0.8)
            self.label(cx_, cy_, 560, 470, "core", T["copy"] - 0.1, s("stat") - 0.15, "#FDBA74", size=32)

    # ------------------------------------------------------------------ set: quake (break1, fix1)
    def draw_quake(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        if not fixed:
            cam = (0, -330, 0.95)
            self.garden(c, t, cam)
            tk = prog(t, T["topple"], T["topple"] + 1.0)
            ck = prog(t, T["cracks"] - 0.2, T["cracks"] + 0.4)
            c.save()
            c.translate(140, 0)
            c.rotate(e_in(tk) * 78)
            c.translate(-140, 0)
            for k in range(9):                                          # a stiff stone tower
                yy = -(k + 1) * 92
                w = 280 - k * 12
                jx = math.sin(t * 40 + k) * 4 * (1 - tk) * prog(t, s("break1"), s("break1") + 0.3)
                c.drawRect(R(-w / 2 + jx, yy, w, 90), lin_paint(-w / 2, 0, w / 2, 0, ["#D1D5DB", "#9CA3AF", "#6B7280"]))
                c.drawRect(R(-w / 2 + jx, yy, w, 90), P("#4B5563", 1, stroke=3))
                if ck > 0 and k % 2 == 0:
                    p = skia.Path()
                    p.moveTo(-w / 4 + jx, yy + 4)
                    p.lineTo(-w / 4 + 20 + jx, yy + 40 * ck)
                    p.lineTo(-w / 4 - 6 + jx, yy + 86 * ck)
                    c.drawPath(p, P("#111827", 1, stroke=5))
            c.restore()
            if tk > 0.7:
                v2.debris(c, 600, -40, t, T["topple"] + 0.8, dur=1.6, n=18, speed=700)
            for i in range(4):
                q = (t * 1.1 + i / 4.0) % 1.0
                c.drawOval(R(-q * 1300, -40 * q, q * 2600, 80 * q), P("#FDE68A", 0.4 * (1 - q), stroke=6))
            c.restore()
            self.ui["cam"] = cam
            return
        vrect(c, 0, 0, W, H, ["#1C1410", "#2E2018", "#140E0A"])                # a wooden joint, close up
        add_glow(c, 540, 760, 700, "#FDBA74", 0.15)
        bend = math.sin(t * 2 * math.pi * 1.2) * prog(t, T["bends"] - 0.3, T["bends"])
        tw_ = math.sin(t * 2 * math.pi * 1.2 + 0.6) * 4 * prog(t, T["twist"] - 0.3, T["twist"])
        post = skia.Path()                                              # the post, bending a little
        post.moveTo(470, 1240)
        post.quadTo(470 + bend * 40, 760, 470 + bend * 10, 280)
        post.lineTo(610 + bend * 10, 280)
        post.quadTo(610 + bend * 40, 760, 610, 1240)
        post.close()
        c.drawPath(post, lin_paint(470, 0, 610, 0, [shade(WOOD, 0.15), WOOD, WOOD_D]))
        for k in range(6):
            gx = 485 + k * 22
            c.drawLine(gx, 1230, gx + bend * 30, 290, P(WOOD_D, 0.5, stroke=3))
        c.save()                                                        # the beam through it, twisting
        c.translate(540 + bend * 25, 700)
        c.rotate(tw_)
        c.drawRect(R(-520, -70, 1040, 140), lin_paint(0, -70, 0, 70, [shade(WOOD, 0.2), WOOD, WOOD_D]))
        for k in range(5):
            c.drawLine(-520, -50 + k * 25, 520, -46 + k * 25, P(WOOD_D, 0.45, stroke=3))
        c.drawRect(R(-58, -90, 36, 180), P("#C08A4F"))                    # wooden wedges, no nails
        c.drawRect(R(22, -90, 36, 180), P("#C08A4F"))
        c.restore()
        rk = prog(t, T["rub"] - 0.3, T["rub"])
        if rk > 0:
            for i in range(10):
                q = (t * 2 + i / 10.0) % 1.0
                ang = i * 0.63
                c.drawCircle(540 + math.cos(ang) * (90 + q * 80), 700 + math.sin(ang) * (90 + q * 80), 5, P("#FDE68A", rk * (1 - q)))
        nk = prog(t, T["nails"] - 0.2, T["nails"] + 0.2)
        if nk > 0:                                                      # a nail, crossed out
            c.drawRect(R(160, 420, 16, 150), P("#9CA3AF", nk))
            c.drawRect(R(140, 410, 56, 14), P("#9CA3AF", nk))
            c.drawCircle(168, 490, 100, P(WARN, nk, stroke=10))
            c.drawLine(98, 560, 238, 420, P(WARN, nk, stroke=10))

    def ui_quake(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 380, "shakes", T["japan"] - 0.1, T["stone"] - 0.1, accent="#FDE68A", size=40)
            self.chip(540, 380, "stiff", T["stone"] - 0.1, s("fix1") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["falls"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["topple"] + 0.5, 1.4)
            return
        self.chip(540, 1150, "wood", T["wood"] - 0.1, T["nails"] - 0.1, accent="#FDBA74", size=40)
        self.chip(540, 1150, "nails", T["nails"] - 0.1, T["thousand"] - 0.1, accent=WARN, size=40)
        self.chip(540, 1150, "joints", T["thousand"] - 0.1, s("break2") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["rub"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: xray (break2, fix2, break3, fix3)
    def draw_xray(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0F172A", "#1E1B4B", "#0F172A"])
        for k in range(16):
            c.drawLine(k * 80, 0, k * 80, H, P("#312E81", 0.5, stroke=2))
        for k in range(26):
            c.drawLine(0, k * 80, W, k * 80, P("#312E81", 0.5, stroke=2))
        cam = (0, -140 / 0.82, 0.82)
        self.view(c, cam)
        c.drawRect(R(-700, 0, 1400, 30), P("#475569"))
        if t < s("fix2") - 0.12:                                        # one rigid tower whipping like a rod
            amp = prog(t, s("break2"), T["whips"])
            ph = math.sin(t * 2 * math.pi * 1.3)
            for i in range(NST):
                yb, yt, yr = storey_y(i)
                lean = ph * amp * 150 * ((i + 1) / NST) ** 2
                c.save()
                c.translate(lean, 0)
                c.rotate(ph * amp * 9 * (i + 1) / NST)
                body(c, 0, yb, yt, 150 - i * 17, red=0.0, xray=0.4)
                roof(c, 0, yt, yr, 150 - i * 17 + 150)
                c.restore()
            tip = ph * amp * 150
            for k in range(3):
                c.drawLine(tip - k * 30 * ph, storey_y(NST - 1)[2] - 40, tip - k * 30 * ph, storey_y(NST - 1)[2] - 160,
                           P("#E0F2FE", 0.35 * amp * (1 - k / 3.0), stroke=6))
        elif t < s("break3") - 0.12:                                    # five loose boxes, the snake dance
            amp = prog(t, s("fix2"), T["boxes"])
            offs = self.sway(t, 1.6 * amp)
            pagoda(c, 0, 0, 1.0, t, offs=offs, xray=0.6)
            ok = prog(t, T["opposite"] - 0.3, T["opposite"])
            for i in range(NST):
                yb, yt, yr = storey_y(i)
                d = 1 if offs[i] >= 0 else -1
                arrow(c, -240 * d * -1 + offs[i], (yb + yt) / 2, (-240 + 90) * d * -1 + offs[i], (yb + yt) / 2,
                      ["#FDE68A", "#93C5FD"][i % 2], a=ok, w=12, head=30)
        else:
            fixed = t >= s("fix3") - 0.12
            if not fixed:                                               # one floor goes too far and slides off
                sl = prog(t, T["slip"], T["slip"] + 1.0)
                offs = list(self.sway(t, 1.2))
                offs[2] += prog(t, s("break3"), T["far"]) * 40
                pagoda(c, 0, 0, 1.0, t, offs=tuple(offs), xray=0.6, gone=2, gone_dx=e_in(sl) * 520,
                       gone_dy=e_in(sl) ** 2 * 900, gone_rot=sl * 40)
            else:                                                       # the trunk: a floor bumps it and comes back
                ck = prog(t, T["core_in"], T["core_in"] + 0.6)
                offs = list(self.sway(t, 1.2))
                hit = prog(t, T["bump"] - 0.5, T["bump"]) * (1 - prog(t, T["bump"], T["bump"] + 0.5))
                offs[2] += 16 * hit
                pagoda(c, 0, 0, 1.0, t, offs=tuple(offs), xray=0.75, trunk=ck)
                if 0 < hit:
                    yb, yt, yr = storey_y(2)
                    add_glow(c, 30 + offs[2] * 0.2, (yb + yt) / 2, 80, "#FDE68A", hit)
        c.restore()
        self.ui["cam"] = cam

    def ui_xray(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 1170, "whip", T["whips"] - 0.2, s("fix2") - 0.15, accent=WARN, size=38)
            self.badge("alert", T["rod"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["rod"] + 0.05, 1.3)
            return
        if tw < s("break3") - 0.12:
            self.chip(540, 1170, "loose", T["lock"] - 0.1, T["opposite"] - 0.1, accent="#FDE68A", size=40)
            self.chip(540, 1170, "opp", T["opposite"] - 0.1, s("break3") - 0.15, accent=GOOD, size=38)
            self.badge("check", T["opposite"] + 0.2, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 1170, "far", T["far"] - 0.2, T["slip"], accent="#FDE68A", size=40)
            self.chip(540, 1170, "slides", T["slip"], s("fix3") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["slides"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["slides"] + 0.05, 1.3)
            return
        cam = self.ui.get("cam", (0, -140 / 0.82, 0.82))
        tx, ty = self.at(cam, 0, storey_y(NST - 1)[2] - 100)
        self.label(tx, ty, 300, 300, "trunk", T["core_in"], T["bumps"] - 0.1, "#FDBA74", size=36)
        self.chip(540, 1170, "bump", T["bumps"] - 0.1, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["back"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: eaves (break4, fix4, cta)
    def draw_eaves(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.came.at(t)
        fixed = t >= s("fix4") - 0.12
        self.garden(c, t, cam)
        eave = prog(t, T["wide"], T["wide"] + 0.8) if fixed else 0.0
        eave = 0.12 + 0.88 * e_out(eave)
        rot = prog(t, T["rot"] - 0.4, T["rot"] + 0.4) if not fixed else 1 - prog(t, T["dry"] - 0.3, T["dry"] + 0.6)
        pagoda(c, 0, 0, 1.0, t, offs=self.sway(t, 0.25 if t > T["steady"] - 0.3 else 0.0), eave=eave, rot=rot,
               wet=1.0 - (prog(t, T["dry"], T["dry"] + 0.8) if fixed else 0.0))
        rng = random.Random(6)                                           # rain and snow
        for i in range(70):
            x0 = rng.uniform(-700, 700)
            sp = rng.uniform(900, 1300)
            yy = -1400 + ((t * sp + rng.uniform(0, 2000)) % 1600)
            if i % 5 == 0:
                c.drawCircle(x0 + math.sin(t * 2 + i) * 20, yy, 6, P("#F8FAFC", 0.85))
            else:
                c.drawLine(x0, yy, x0 - 8, yy + 40, P("#BFDBFE", 0.55, stroke=3))
        if fixed and eave > 0.6:                                         # drips falling off the eave tips, away from the walls
            for i in range(NST):
                yb, yt, yr = storey_y(i)
                half = 150 - i * 17 + 30 + 120 * eave
                for sd in (-1, 1):
                    q = (t * 1.6 + i * 0.3) % 1.0
                    c.drawCircle(sd * (half + 6), yt - 20 + q * 70, 6, P("#93C5FD", 0.9 * (1 - q)))
        c.restore()
        self.ui["cam"] = cam
        self.ui["eave"] = eave

    def ui_eaves(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.came.at(tw))
        if tw < s("fix4") - 0.12:
            self.chip(540, 470, "rot", T["rain"] - 0.1, s("fix4") - 0.15, accent=WARN, size=36)
            self.badge("alert", T["rot"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["rot"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            ex, ey = self.at(cam, 150 - 17 + 30 + 120, storey_y(1)[1] - 10)
            self.label(ex, ey, 800, 470, "eaves", T["wide"], T["dry"] - 0.1, "#E2E8F0", size=38)
            self.chip(330, 470, "dry", T["dry"] - 0.1, T["steady"] - 0.1, accent=GOOD, size=40)
            pk = self.span(T["steady"] - 0.1, s("cta") - 0.15)
            if pk > 0:                                                   # a tightrope walker with his long pole
                c.drawRRect(rr(50, 300, 400, 300, 26), P(GLASS, 0.85 * pk))
                c.drawRRect(rr(50, 300, 400, 300, 26), P("#FFFFFF", 0.25 * pk, stroke=3))
                x0, y0 = 250, 420
                c.drawLine(x0 - 180, y0 + 120, x0 + 180, y0 + 120, P("#E2E8F0", pk, stroke=4))
                person(c, x0, y0 + 120, 110, "#F472B6", t, pose="stand", face=1, a=pk)
                tilt = math.sin(t * 3) * 6
                c.save()
                c.translate(x0, y0 + 50)
                c.rotate(tilt)
                c.drawLine(-170, 0, 170, 0, P("#FDE68A", pk, stroke=8))
                c.restore()
                v2.chip(c, 250, 660, self.L["pole"], pk, accent=HILITE, size=28)
            self.badge("check", T["tight"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: home (tag)
    def draw_home(self, c, t):
        T = self.T
        room(c, 0, 0, W, 1250, wall="#3B4A5C", floor="#2A3442", t=t, lamp=True, lamp_x=540)
        vrect(c, 0, 1250, W, H - 1250, ["#2A3442", "#1C232D", "#0E1218"])
        c.drawRect(R(120, 330, 300, 360), P("#5C3A1A"))                  # a framed pagoda on the wall
        c.save()
        c.clipRect(R(136, 346, 268, 328))
        vrect(c, 136, 346, 268, 328, ["#22184A", "#C25A6A", "#F59E8B"])
        pagoda(c, 270, 660, 0.27, t, red=1.0)
        c.restore()
        add_glow(c, 270, 510, 230, "#FDE68A", 0.25 * prog(t, T["still"] - 0.3, T["still"] + 0.3))
        fk = prog(t, T["kick"], T["kick"] + 0.9)
        if not self.rtl:                                                 # English: a Jenga tower and a sneeze
            c.drawRRect(rr(520, 1000, 480, 34, 10), P("#8B5A2B"))
            c.drawRect(R(560, 1034, 26, 216), P("#6B4423"))
            c.drawRect(R(934, 1034, 26, 216), P("#6B4423"))
            jenga(c, 760, 1000, 0.9, t, fall=e_in(fk))
            person(c, 320, 1250, 170, "#22C55E", t, pose="duck" if fk > 0 else "stand", face=1, hat="none",
                   hair="#3F2A1A")
            if t > T["kick"] - 0.1:
                k = prog(t, T["kick"] - 0.1, T["kick"] + 0.2)
                for i in range(8):                                       # the sneeze
                    q = (t * 2 + i / 8.0) % 1.0
                    c.drawCircle(380 + q * 260, 1080 - 60 + math.sin(i) * 30 * q, 6 + q * 6, P("#E0F2FE", 0.7 * k * (1 - q)))
        else:                                                            # Arabic: dishes in the sink and mom's look
            c.drawRRect(rr(480, 980, 540, 60, 12), P("#7C8796"))
            c.drawRRect(rr(520, 1040, 460, 120, 20), P("#556070"))
            c.drawRect(R(735, 900, 14, 84), P("#9CA3AF"))
            c.drawRect(R(700, 896, 70, 14), P("#9CA3AF"))
            dishes(c, 750, 1010, 0.9, t, fall=e_in(fk))
            mom(c, 260, 1250, 230, t)
            gk = prog(t, T["fell"] - 0.6, T["fell"] - 0.2)
            if gk > 0:                                                   # the look
                for dx in (-12, 12):
                    add_glow(c, 268 + dx, 1250 - 230 * 0.88, 26, "#EF4444", 0.9 * gk)
                for i in range(3):
                    c.drawLine(300, 1050 + i * 20, 300 + 300 * gk, 1040 + i * 20 - 60 * gk, P("#EF4444", 0.5 * gk, stroke=4))

    def ui_home(self, c, t, tw):
        T = self.T
        self.chip(270, 760, "still", T["still"] - 0.2, self.duration + 1, accent=GOOD, size=26)
        if not self.rtl:
            k = self.span(T["kick"] - 0.15, T["kick"] + 1.2, 0.15, 0.2)
            if k > 0:
                v2.chip(c, 400, 900, self.L["achoo"], k, accent=HILITE, size=44)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, rumble(2.4, 60), -8), (0.1, sfx.creak(1.2), -12), (T["sways"], sfx.creak(1.0), -12),
              (T["never"], sfx.thud(0.4), -10), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 61), -9), (T["pagoda"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 62), -4), (s("break1") + 0.2, rumble(2.2, 63), -8),
               (T["cracks"], sfx.snap(64), -6), (T["topple"] + 0.6, sfx.thud(0.6), -4), (T["topple"] + 0.8, sfx.clank(200.0, 0.6, 65), -10),
               (T["falls"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["bends"], sfx.creak(1.0), -10), (T["nails"], sfx.pop(66), -8), (T["twist"], sfx.creak(0.8), -10),
               (T["rub"], sfx.hiss(0.6, 67), -14), (T["rub"] + 0.2, sfx.ding(), -8), (T["rub"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["whips"], sfx.whoosh(0.6, True, 69), -10),
               (T["rod"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["boxes"], sfx.creak(1.0), -10), (T["opposite"] + 0.2, sfx.ding(), -8), (T["opposite"] + 0.4, sfx.chime(), -6)]
        ev += [(T["slip"], sfx.whoosh(0.6, False, 70), -10), (T["slip"] + 0.7, sfx.thud(0.5), -6), (T["slides"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["core_in"], sfx.thunk(71), -8), (T["bump"], sfx.thunk(72), -6), (T["back"] + 0.1, sfx.ding(), -8),
               (T["back"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["rain"], sfx.hiss(2.4, 74), -16),
               (T["rot"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["wide"], sfx.whoosh(0.6, False, 75), -10), (T["dry"], sfx.sparkle(0.6, 8, 76), -10),
               (T["tight"] + 0.1, sfx.ding(), -8), (T["tight"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(77), 0), (T["follow"] - 0.15, sfx.pop(78), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 79), -6), (T["paint"], sfx.sparkle(1.0, 12, 80), -8),
               (T["rise"], sfx.whoosh(1.2, True, 81), -10), (T["copy"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 82), -6), (T["s1"], sfx.pop(83), -3), (T["s2"], sfx.pop(84), -3),
               (T["s3"], sfx.pop(85), -3)]
        ev += [(T["cong2"], sfx.pop(86), -2), (T["cong2"], sfx.sparkle(1.0, 14, 87), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 88), -6), (T["still"], sfx.chime(), -10), (T["kick"], sfx.whoosh(0.3, True, 89), -10),
               (T["kick"] + 0.5, sfx.clank(700.0, 0.5, 90), -8), (T["kick"] + 0.7, sfx.clank(900.0, 0.4, 91), -10),
               (T["kick"] + 0.9, sfx.thud(0.4), -8)]
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


NAME = "pagoda"
EPISODE = Pagoda
