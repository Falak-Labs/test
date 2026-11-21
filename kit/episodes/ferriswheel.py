"""Episode 58 - A giant Ferris wheel.  v2 look: a giant observation wheel on an island off Dubai at golden hour and at
night, its rim hung from thin cables like a bicycle wheel.

Sets: dubai (hook: from one cabin full of people out to the whole wheel turning over the Gulf, the cables glowing;
reveal: the cabins go on one by one and the wheel turns; stat; closer at night with the rim lit), spokes (break1: thick
spokes like a wagon wheel, the bottom ones buckle under the weight; fix1: tight cables from the hub hold the rim like a
bicycle wheel), cabin (break2: a cabin bolted to the rim turns with it and flips its riders; fix2: the cabin sits in its
own ring and a motor turns it back so the floor stays level), drive (break3: a gearbox the size of a building at the
axle; fix3: rows of tyres squeeze the rim at the bottom and roll it while people step on), lift (break4: half a wheel in
the sky with nothing to stand on; fix4: London's wheel built lying flat over the river and winched upright with cables
from a mast), chicago (second half of the reveal: the first wheel of 1893 with its 36 cars, built to beat the Eiffel
Tower), tag (EN: filming the whole ride for a video you'll never watch; AR: dad says it's for kids and screams first).
World (dubai): front view, the ground at y = 0, the hub at HUB_Y, rim radius R_RIM.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, sun  # noqa: E402
from burjalarab import path_of, sea_band, skyline, burj, palm_tree  # noqa: E402
from eiffel import eiffel  # noqa: E402
from phone import bubble  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2A2A60", "horizon": "#5A3A7A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
LONDON = {"top": "#141B2E", "upper": "#243049", "mid": "#3A4862", "low": "#52617A", "horizon": "#6B7890",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SEPIA = {"top": "#2A2018", "upper": "#4A3A2A", "mid": "#7A6448", "low": "#B8956A", "horizon": "#E8C99A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
R_RIM = 300.0                       # rim radius (world units)
HUB_Y = -372.0                      # hub height above the ground
NCAB = 48
STEELW = "#E2E8F0"
STEELD = "#94A3B8"
LEDS = ("#F472B6", "#60A5FA", "#A78BFA", "#34D399", "#FBBF24", "#F87171")


def polar(r, deg, cx=0.0, cy=HUB_Y):
    a = math.radians(deg)
    return cx + math.cos(a) * r, cy + math.sin(a) * r


def cabin(c, x, y, s, t, rot=0.0, a=1.0, lit=0.0, people=2, seed=0, ring=0.0, ring_rot=0.0, detail=False):
    """A glass capsule centred on (x, y), s = scale (1 = 32 x 24 units).  rot turns it (a cabin bolted to the rim);
    ring 0..1 draws the ring it turns in; detail draws real little people (for close-ups)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if ring > 0:
        c.save()
        c.rotate(ring_rot)
        c.drawCircle(0, 0, 22, P(STEELW, ring * a, stroke=3.2))
        for k in range(6):
            q = math.radians(k * 60)
            c.drawLine(math.cos(q) * 19, math.sin(q) * 19, math.cos(q) * 25, math.sin(q) * 25, P(STEELD, ring * a, stroke=2))
        c.restore()
    c.rotate(rot)
    body = rr(-16, -12, 32, 24, 11)
    c.drawRRect(body, P(mix("#7DD3FC", "#FDE68A", 0.6 * lit), (0.55 + 0.3 * lit) * a))
    if detail:
        cols = ("#F97316", "#2563EB", "#DB2777", "#16A34A")
        for k in range(people):
            person(c, -9 + k * 6, 10, 15, cols[(k + seed) % 4], t + k * 0.4, pose="look" if k % 2 else "point",
                   face=1 if k % 2 else -1, a=a)
    else:
        rng = random.Random(seed)
        for k in range(people):
            px = -8 + k * 7 + rng.uniform(-1, 1)
            c.drawCircle(px, -2, 2.6, P("#1E293B", 0.8 * a))
            c.drawRRect(rr(px - 3, 0.5, 6, 8, 2.5), P("#1E293B", 0.8 * a))
    c.drawRRect(body, P("#F8FAFC", a, stroke=2.2))
    c.drawRect(R(-15, 7, 30, 3), P("#CBD5E1", 0.9 * a))
    if lit > 0:
        add_glow(c, 0, 0, 26, "#FFE6A8", 0.35 * lit * a)
    c.restore()


def wheel(c, t, rot=0.0, cabins=1.0, spokes=1.0, thick=0.0, buckle=0.0, glow=0.0, lit=0.0, legs=1.0, a=1.0,
          cab_n=None, bolted=False, cx=0.0, cy=HUB_Y):
    """The wheel in world space around its hub (cx, cy).  rot in degrees; cabins 0..1 fades them in, cab_n hangs only
    the first n; spokes 0..1 the thin cables; thick 0..1 wagon-wheel beams instead; buckle 0..1 bends the bottom ones;
    glow 0..1 lights the cables up as the 'tension' highlight; lit 0..1 the night LEDs."""
    if a <= 0:
        return
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    sag = 26 * buckle
    if legs > 0:                                                   # the legs: two pairs leaning on the hub
        for sd in (-1, 1):
            for off, col in ((-14, STEELD), (14, STEELW)):
                foot = cx + sd * (R_RIM * 0.86 + off)
                lp = path_of([(cx + sd * 8, cy - 10), (cx + sd * 22, cy + 10), (foot, 0.0), (foot - sd * 20, 0.0)], close=True)
                c.drawPath(lp, P(mix(col, "#1E293B", 0.25 * lit), legs))
        c.drawLine(cx - R_RIM * 0.62, cy * 0.28, cx + R_RIM * 0.62, cy * 0.28, P(STEELD, legs, stroke=8))
    rim_y = cy + sag * 0.6
    # spokes
    if thick > 0:
        for k in range(12):
            ang = rot + k * 30
            hx, hy = polar(40, ang, cx, cy)
            rx, ry = polar(R_RIM - 14, ang, cx, rim_y)
            down = max(0.0, math.sin(math.radians(ang)))               # 1 for the spoke pointing straight down
            bend = buckle * down * 70 * (1 if k % 2 else -1)
            mx, my = (hx + rx) / 2, (hy + ry) / 2
            nx, ny = -(ry - hy), (rx - hx)
            ln = math.hypot(nx, ny) or 1
            sp = skia.Path()
            sp.moveTo(hx, hy)
            sp.quadTo(mx + nx / ln * bend, my + ny / ln * bend, rx, ry)
            col = mix("#64748B", WARN, buckle * down)
            c.drawPath(sp, P(col, thick, stroke=24))
            c.drawPath(sp, P("#94A3B8", 0.6 * thick, stroke=8))
    if spokes > 0:
        for k in range(64):
            ang = rot + k * 360.0 / 64
            off = 7 if k % 2 else -7
            hx, hy = polar(36, ang + off * 3, cx, cy)
            rx, ry = polar(R_RIM - 12, ang, cx, rim_y)
            c.drawLine(hx, hy, rx, ry, P(mix("#E5E7EB", HILITE, glow), (0.42 + 0.5 * glow) * spokes, stroke=1.6 + 1.6 * glow))
        if glow > 0:
            for k in range(0, 64, 4):
                ang = rot + k * 360.0 / 64
                px, py = polar(R_RIM * 0.55, ang, cx, cy)
                add_glow(c, px, py, 26, HILITE, 0.25 * glow * spokes)
    # rim: two rings and a zigzag truss between them
    c.save()
    c.translate(0, sag * 0.6)
    if buckle > 0:
        c.translate(cx, cy)
        c.scale(1.0 + 0.05 * buckle, 1.0 - 0.07 * buckle)
        c.translate(-cx, -cy)
    c.drawCircle(cx, cy, R_RIM, P(STEELW, 1.0, stroke=7))
    c.drawCircle(cx, cy, R_RIM - 16, P(STEELD, 1.0, stroke=5))
    zz = skia.Path()
    for k in range(97):
        ang = rot + k * 360.0 / 96
        r_ = R_RIM if k % 2 else R_RIM - 16
        px, py = polar(r_, ang, cx, cy)
        if k == 0:
            zz.moveTo(px, py)
        else:
            zz.lineTo(px, py)
    c.drawPath(zz, P("#CBD5E1", 0.9, stroke=2.4))
    if lit > 0:                                                    # LEDs running round the rim
        for k in range(96):
            ang = rot + k * 3.75
            px, py = polar(R_RIM - 8, ang, cx, cy)
            col = LEDS[int(k / 8 + t * 2.0) % len(LEDS)]
            add_glow(c, px, py, 10, col, 0.75 * lit)
    c.restore()
    # hub
    c.drawCircle(cx, cy, 42, P("#CBD5E1"))
    c.drawCircle(cx, cy, 42, P("#64748B", 1.0, stroke=4))
    c.drawCircle(cx, cy, 16, P("#475569"))
    if lit > 0:
        add_glow(c, cx, cy, 60, "#FFFFFF", 0.3 * lit)
    # cabins outside the rim
    if cabins > 0:
        n = NCAB if cab_n is None else int(cab_n)
        for k in range(n):
            ang = rot + k * 360.0 / NCAB - 90
            px, py = polar(R_RIM + 24, ang, cx, rim_y)
            cabin(c, px, py, 1.0, t, rot=(ang + 90) if bolted else 0.0, a=cabins, lit=lit, people=2 + k % 2, seed=k)
    if a < 1:
        c.restore()


def island(c, t, night=0.0):
    """The island under the wheel (world space) with palms, and the sea in front."""
    c.drawRect(R(-1500, -6, 3000, 30), P(mix("#D9B98A", "#3A3550", night)))
    c.drawRect(R(-1500, 18, 3000, 60), P(mix("#4F7A4A", "#1A2A30", night)))
    for x in (-470, -420, 430, 480, 540):
        palm_tree(c, x, 0, 0.7, t)
    c.drawRect(R(-300, -46, 600, 10), P(mix("#E5E7EB", "#3A3F5A", night)))           # the boarding deck
    c.drawRRect(rr(-90, -44, 180, 44, 6), P(mix("#F1F5F9", "#2A3050", night)))        # the boarding hall
    for k in range(6):
        c.drawRect(R(-80 + k * 28, -34, 18, 16), P("#FFD58A" if night > 0.4 else "#7DD3FC", 0.8))
    sea_band(c, -1600, 1600, 78, 700, t, col=mix("#1E7A9A", "#0E1E3A", night), dark=mix("#0B3A5A", "#060A1A", night))


def gear(c, x, y, r, ang, teeth=12, col="#64748B", a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    gp = skia.Path()
    for k in range(teeth * 2):
        q = math.radians(k * 180.0 / teeth)
        rr_ = r if k % 2 == 0 else r * 0.86
        q2 = math.radians((k + 1) * 180.0 / teeth)
        if k == 0:
            gp.moveTo(math.cos(q) * rr_, math.sin(q) * rr_)
        else:
            gp.lineTo(math.cos(q) * rr_, math.sin(q) * rr_)
        gp.lineTo(math.cos(q2) * rr_, math.sin(q2) * rr_)
    gp.close()
    c.drawPath(gp, P(col, a))
    c.drawCircle(0, 0, r * 0.3, P("#1F2937", a))
    c.restore()


def tyre(c, x, y, r, ang, a=1.0):
    c.drawCircle(x, y, r, P("#111827", a))
    c.drawCircle(x, y, r * 0.55, P("#6B7280", a))
    for k in range(5):
        q = math.radians(ang + k * 72)
        c.drawLine(x, y, x + math.cos(q) * r * 0.5, y + math.sin(q) * r * 0.5, P("#374151", a, stroke=3))


def bicycle(c, x, y, s, t, a=1.0):
    """A small bicycle (screen space), wheels with thin spokes."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for wx in (-60, 60):
        c.drawCircle(wx, 0, 44, P("#E5E7EB", a, stroke=5))
        for k in range(16):
            q = math.radians(t * 90 + k * 22.5)
            c.drawLine(wx, 0, wx + math.cos(q) * 42, math.sin(q) * 42, P(HILITE, a, stroke=1.4))
        c.drawCircle(wx, 0, 6, P("#9CA3AF", a))
    fr = path_of([(-60, 0), (-10, -50), (40, -50), (60, 0), (0, 0), (-10, -50)])
    c.drawPath(fr, P("#EF4444", a, stroke=6))
    c.drawLine(40, -50, 34, -66, P("#EF4444", a, stroke=5))
    c.drawLine(24, -68, 46, -68, P("#E5E7EB", a, stroke=5))
    c.drawLine(-10, -50, -14, -62, P("#EF4444", a, stroke=5))
    c.drawRRect(rr(-28, -68, 30, 8, 4), P("#1F2937", a))
    c.restore()


def old_wheel(c, x, y, s, t, rot=0.0, a=1.0):
    """The first Ferris wheel (Chicago, 1893): an iron wheel on two towers with 36 boxy cars."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rr_ = 250.0
    hy = -290.0
    for sd in (-1, 1):
        c.drawPath(path_of([(sd * 12, hy), (sd * 190, 0), (sd * 160, 0), (sd * 4, hy + 10)], close=True), P("#4A3A30", a))
    c.drawCircle(0, hy, rr_, P("#5A4636", a, stroke=6))
    c.drawCircle(0, hy, rr_ - 26, P("#5A4636", a, stroke=4))
    for k in range(36):
        q = math.radians(rot + k * 10)
        c.drawLine(math.cos(q) * 20, hy + math.sin(q) * 20, math.cos(q) * (rr_ - 26), hy + math.sin(q) * (rr_ - 26),
                   P("#6E5644", 0.8 * a, stroke=1.6))
    c.drawCircle(0, hy, 22, P("#3A2A20", a))
    for k in range(36):
        q = math.radians(rot + k * 10)
        px, py = math.cos(q) * (rr_ + 4), hy + math.sin(q) * (rr_ + 4)
        c.drawRRect(rr(px - 13, py, 26, 22, 3), P("#8A6A4A", a))
        c.drawRect(R(px - 10, py + 4, 20, 8), P("#F5DEB3", 0.8 * a))
        c.drawRect(R(px - 15, py - 3, 30, 5), P("#3A2A20", a))
    c.restore()


# ====================================================================================== the episode
class FerrisWheel(EpisodeV2):
    BUILD_NO = 58
    FIRST_SET = "dubai"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "FERRIS WHEEL", "ar_sa": "عجلة ملاهي"}
    EMPH = {"en": ["CONGRATS", "SEVENTEEN", "HUNDRED", "PEOPLE", "DUBAI", "WHEEL", "THIN", "CABLES", "GIANT", "FERRIS",
                   "YOURSELF", "THICK", "HEAVY", "BUCKLE", "BICYCLE", "TIGHT", "HUB", "RIM", "LIGHT", "STIFF", "FLIP",
                   "UPSIDE", "DOWN", "RING", "MOTORS", "LEVEL", "AXLE", "GIGANTIC", "GEARBOX", "PUSH", "TYRES",
                   "SQUEEZE", "ROLL", "SLOWLY", "STEP", "TALL", "NOTHING", "LONDON", "FLAT", "RIVER", "WINCHED",
                   "UPRIGHT", "JACKS", "FOLLOW", "STATUE", "LIBERTY", "CABINS", "TURN", "FIRST", "CHICAGO", "EIGHTEEN",
                   "NINETY-THREE", "BEAT", "EIFFEL", "TOWER", "TWO", "FIFTY", "METERS", "FORTY-EIGHT", "THIRTY-EIGHT",
                   "MINUTES", "CITY", "FILMING", "NEVER", "WATCH"],
            "ar_sa": ["مبروك", "وسبعمية", "دبي", "عجلة", "كابلات", "رفيعة", "ملاهي", "عملاقة", "بإيدك", "تخينة", "تقيلة",
                      "هتتني", "البسكلتة", "مشدودة", "المحور", "الإطار", "خفيفة", "وجامدة", "الكابينة", "هتقلب", "راسهم",
                      "حلقة", "وموتور", "مستوية", "جيربوكس", "العمارة", "تزق", "كاوتشات", "براحة", "تركب", "ماشية",
                      "بالطول", "واقفة", "مفيش", "لندن", "نايمة", "النهر", "رفعوها", "بالكابلات", "تابعني", "تمثال",
                      "الحرية", "الكباين", "تلف", "شيكاغو", "تغلب", "إيفل", "ميتين", "وخمسين", "متر", "تمانية",
                      "وأربعين", "كابينة", "وتلاتين", "دقيقة", "أبوك", "عيال", "يصرّخ"]}
    KEYS = {"ar_sa": {
        ("hook", "SEVENTEEN"): "وسبعمية", ("hook", "DUBAI"): "دبي", ("hook", "WHEEL"): "عجلة", ("hook", "CABLES"): "كابلات",
        ("hook", "CONGRATS"): "مبروك", ("hook", "FERRIS"): "ملاهي",
        ("break1", "THICK"): "تخينة", ("break1", "HEAVY"): "تقيلة", ("break1", "BUCKLE"): "هتتني",
        ("fix1", "BICYCLE"): "البسكلتة", ("fix1", "TIGHT"): "مشدودة", ("fix1", "HUB"): "المحور", ("fix1", "RIM"): "الإطار",
        ("fix1", "LIGHT"): "خفيفة",
        ("break2", "TURNS"): "بتلف", ("break2", "BOLTED"): "المربوطة", ("break2", "FLIP"): "هتقلب",
        ("fix2", "RING"): "حلقة", ("fix2", "MOTORS"): "وموتور", ("fix2", "LEVEL"): "مستوية",
        ("break3", "TURNING"): "تلف", ("break3", "AXLE"): "المحور", ("break3", "GIGANTIC"): "جيربوكس",
        ("break3", "GEARBOX"): "العمارة",
        ("fix3", "PUSH"): "فتزق", ("fix3", "TYRES"): "كاوتشات", ("fix3", "ROLL"): "وتلفّه", ("fix3", "SLOWLY"): "براحة",
        ("fix3", "STEP"): "تركب",
        ("break4", "TALL"): "بالطول", ("break4", "STANDING"): "واقفة", ("break4", "NOTHING"): "مفيش",
        ("fix4", "LONDON"): "لندن", ("fix4", "FLAT"): "نايمة", ("fix4", "RIVER"): "النهر", ("fix4", "WINCHED"): "رفعوها",
        ("fix4", "JACKS"): "شوية",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "HANG"): "علّق", ("reveal", "CABINS"): "الكباين", ("reveal", "TURN"): "تلف", ("reveal", "FIRST"): "وأول",
        ("reveal", "CHICAGO"): "شيكاغو", ("reveal", "BEAT"): "تغلب", ("reveal", "EIFFEL"): "إيفل",
        ("stat", "TWO"): "ميتين", ("stat", "FORTY-EIGHT"): "وأربعين", ("stat", "THIRTY-EIGHT"): "واللفة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "LIFTS"): "أبوك", ("tag", "CITY"): "عيال", ("tag", "FILMING"): "تطلعوا", ("tag", "NEVER"): "يصرّخ"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Statue of Liberty"),
                   "stat": [("250 m", "TALL"), ("48", "CABINS"), ("38 min", "ONE TURN")],
                   "L": {"people": "1,750 PEOPLE", "dubai": "OVER DUBAI", "cables": "HUNG FROM THIN CABLES",
                         "name": "A GIANT FERRIS WHEEL", "thick": "THICK SPOKES", "heavy": "TOO HEAVY",
                         "buckle": "THE BOTTOM ONES BUCKLE", "bike": "LIKE A BICYCLE WHEEL", "tight": "TIGHT CABLES",
                         "stiff": "LIGHT AND STIFF", "bolted": "BOLTED TO THE RIM", "flip": "UPSIDE DOWN!",
                         "ring": "ITS OWN RING", "level": "MOTORS KEEP IT LEVEL", "gearbox": "A GIGANTIC GEARBOX",
                         "push": "PUSH THE RIM", "tyres": "TYRES SQUEEZE AND ROLL IT", "step": "STEP ON WHILE IT MOVES",
                         "tall": "TOO TALL TO BUILD UPRIGHT", "nothing": "NOTHING TO STAND ON",
                         "flat": "BUILT FLAT OVER THE RIVER", "winch": "WINCHED UPRIGHT", "hang": "HANG THE CABINS",
                         "first": "CHICAGO, 1893", "beat": "BUILT TO BEAT THE EIFFEL TOWER", "film": "RECORDING...",
                         "never": "NEVER WATCHED"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: تمثال الحرية"),
                      "stat": [("250", "متر طول"), ("48", "كابينة"), ("38", "دقيقة اللفة")],
                      "L": {"people": "ألف وسبعمية واحد", "dubai": "فوق دبي", "cables": "متعلقة في كابلات رفيعة",
                            "name": "عجلة ملاهي عملاقة", "thick": "أسياخ تخينة", "heavy": "تقيلة أوي",
                            "buckle": "اللي تحت هتتني", "bike": "زي عجلة البسكلتة", "tight": "كابلات مشدودة",
                            "stiff": "خفيفة وجامدة", "bolted": "مربوطة في الإطار", "flip": "على راسهم!",
                            "ring": "حلقة لوحدها", "level": "الموتور يخليها مستوية", "gearbox": "جيربوكس قد العمارة",
                            "push": "زق الإطار نفسه", "tyres": "كاوتشات تمسكه وتلفّه", "step": "تركب وهي ماشية",
                            "tall": "ما تتبنيش واقفة", "nothing": "مفيش حاجة تقف عليها",
                            "flat": "نايمة فوق النهر", "winch": "رفعوها شوية شوية", "hang": "علّق الكباين",
                            "first": "شيكاغو، سنة 1893", "beat": "عشان تغلب برج إيفل", "film": "بيصرّخ!",
                            "never": "أول واحد يصرّخ", "bubble": "دي لعب عيال!"}}}
    COVER_T = ("closer", 0.55)
    SPEED = 5.0                                                    # degrees a second on screen (the real one: 38 min a turn)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "seventeen": ("hook", "SEVENTEEN", 0.1), "dubai": ("hook", "DUBAI", 0.3), "wheelw": ("hook", "WHEEL", 0.4),
            "cables": ("hook", "CABLES", 0.55), "congrats": ("hook", "CONGRATS", 0.68), "ferris": ("hook", "FERRIS", 0.9),
            "thick": ("break1", "THICK", 0.1), "heavy": ("break1", "HEAVY", 0.45), "buckle": ("break1", "BUCKLE", 0.9),
            "bike": ("fix1", "BICYCLE", 0.3), "tight": ("fix1", "TIGHT", 0.45), "hub": ("fix1", "HUB", 0.6),
            "rim": ("fix1", "RIM", 0.75), "light": ("fix1", "LIGHT", 0.88),
            "turns2": ("break2", "TURNS", 0.15), "bolted": ("break2", "BOLTED", 0.4), "flip": ("break2", "FLIP", 0.75),
            "ring": ("fix2", "RING", 0.35), "motors": ("fix2", "MOTORS", 0.6), "level": ("fix2", "LEVEL", 0.9),
            "turning": ("break3", "TURNING", 0.1), "axle": ("break3", "AXLE", 0.5), "gigantic": ("break3", "GIGANTIC", 0.75),
            "gearbox": ("break3", "GEARBOX", 0.9),
            "push": ("fix3", "PUSH", 0.1), "tyres": ("fix3", "TYRES", 0.35), "roll": ("fix3", "ROLL", 0.5),
            "slowly": ("fix3", "SLOWLY", 0.65), "step": ("fix3", "STEP", 0.8),
            "tall": ("break4", "TALL", 0.25), "standing": ("break4", "STANDING", 0.45), "nothing": ("break4", "NOTHING", 0.8),
            "london": ("fix4", "LONDON", 0.05), "flat": ("fix4", "FLAT", 0.25), "river": ("fix4", "RIVER", 0.4),
            "winched": ("fix4", "WINCHED", 0.6), "jacks": ("fix4", "JACKS", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "hang": ("reveal", "HANG", 0.05), "cabins": ("reveal", "CABINS", 0.15), "turn": ("reveal", "TURN", 0.3),
            "first": ("reveal", "FIRST", 0.42), "chicago": ("reveal", "CHICAGO", 0.55), "beat": ("reveal", "BEAT", 0.8),
            "eiffelw": ("reveal", "EIFFEL", 0.9),
            "s1": ("stat", "TWO", 0.05), "s2": ("stat", "FORTY-EIGHT", 0.4), "s3": ("stat", "THIRTY-EIGHT", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_lift": ("tag", "LIFTS", 0.05), "t_city": ("tag", "CITY", 0.3), "t_film": ("tag", "FILMING", 0.6),
            "t_never": ("tag", "NEVER", 0.85)})
        T["buckle1"] = max(T["buckle"], T["heavy"]) + 0.1
        T["flip1"] = max(T["flip"], T["bolted"]) + 0.1
        T["gear1"] = max(T["gearbox"], T["gigantic"]) + 0.1
        T["nothing1"] = max(T["nothing"], T["standing"]) + 0.1
        T["light1"] = max(T["light"], T["rim"]) + 0.2
        T["level1"] = max(T["level"], T["motors"]) + 0.2
        T["step1"] = max(T["step"], T["slowly"]) + 0.2
        T["jacks1"] = max(T["jacks"], T["winched"]) + 0.2
        T["first"] = max(T["first"], T["turn"] + 0.6)
        # ---- sets
        self.cut(s("break1") - 0.12, "spokes", 1)
        self.cut(s("break2") - 0.12, "cabin", -1)
        self.cut(s("break3") - 0.12, "drive", 1)
        self.cut(s("break4") - 0.12, "lift", -1)
        self.cut(s("reveal") - 0.12, "dubai", 1)
        self.cut(T["first"] - 0.12, "chicago", -1)
        self.cut(s("stat") - 0.12, "dubai", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- dubai camera: from one cabin at the top out to the whole wheel
        cm = Camera(0, -150, 2.0)                                  # from the boarding deck up to the whole wheel ("lift")
        cm.key(0.05, 0, -160, 1.95, 0.3)
        cm.key(0.35, 0, -241, 1.12, max(0.9, T["dubai"] - 0.35))
        cm.key(T["congrats"], 0, -233, 1.16, 1.4)
        cm.key(s("reveal") - 0.12, 0, -241, 1.12, 0.0).key(T["turn"], 0, -229, 1.18, 1.2)
        cm.key(s("stat") - 0.12, 0, -298, 0.86, 0.0).key(s("stat"), 0, -300, 0.87, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -245, 1.1, 1.0).key(s("closer") + 0.9, 0, -235, 1.15, 3.0)
        self.cam = cm
        self.spans = [(T["buckle1"], T["light1"] + 0.3), (T["flip1"], T["level1"] + 0.3), (T["gear1"], T["step1"] + 0.3),
                      (T["nothing1"], T["jacks1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["buckle1"], 0.5, 9), (T["flip1"], 0.4, 7), (T["gear1"], 0.4, 7),
                       (T["nothing1"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["t_never"], 0.25, 6)]

    def rot(self, t):
        return self.SPEED * t

    # ------------------------------------------------------------------ set: dubai (hook, reveal, stat, closer)
    def dubai_bg(self, c, t, cam, night):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy - 30 * z)
        if night > 0:
            c.save()
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy - 30 * z)
            v2.stars(c, W, H, t, 0.8)
            c.restore()
            c.restore()
        if night < 1:
            sun(c, 860 - cx * 0.05, gy - 520 * z, 50, heat=0.4, a=1 - night)
        for i, (px, py, s_) in enumerate(((200, 900, 1.0), (820, 1100, 0.8), (520, 1300, 0.7))):
            v2.cloud(c, (px + t * (6 + i * 3)) % (W + 600) - 300, gy - py * z, s_, body=mix("#7A6A9A", "#1A1E48", night),
                     rim=mix("#FFB37A", "#3A3A78", night), a=0.7, seed=i)
        c.save()                                                   # the far coast: skyline and the sail hotel
        c.translate(W / 2 - cx * z * 0.25, gy - 6 * z)
        c.scale(z * 0.55, z * 0.55)
        skyline(c, -1300, 1300, 0, t, a=1 - 0.4 * night)
        burj(c, 900, 0, t, s=0.32, lit=night)
        c.restore()

    def draw_dubai(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        night = prog(t, s("closer") - 0.6, s("closer") + 0.6)
        self.dubai_bg(c, t, cam, night)
        self.view(c, cam)
        hook = t < s("break1")
        glow = 0.0
        if hook:
            glow = prog(t, T["cables"] - 0.2, T["cables"] + 0.2) * (1 - prog(t, T["congrats"] + 0.2, T["congrats"] + 0.8))
        cab_n = None
        if s("reveal") - 0.12 <= t < s("stat") - 0.12:
            cab_n = NCAB * prog(t, T["hang"] - 0.2, T["turn"] + 0.2)
        rot = self.rot(t)
        wheel(c, t, rot=rot, glow=glow, lit=night, cab_n=cab_n)
        island(c, t, night)
        if hook:                                                   # people boarding on the deck
            for k, (px, col) in enumerate(((-150, "#F97316"), (-120, "#2563EB"), (110, "#DB2777"), (140, "#16A34A"))):
                person(c, px + math.sin(t * 0.8 + k) * 6, -44, 26, col, t + k * 0.3, pose="walk" if k % 2 else "stand",
                       face=1 if px < 0 else -1)
        c.restore()
        self.ui["cam"] = cam

    def ui_dubai(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "people", T["seventeen"] - 0.1, T["dubai"] - 0.1, accent=HILITE, size=46)
            self.chip(540, 300, "dubai", T["dubai"] - 0.1, T["cables"] - 0.15, accent="#FDBA74", size=46)
            self.chip(540, 300, "cables", T["cables"] - 0.15, T["ferris"] - 0.25, accent=HILITE, size=42)
            self.chip(540, 300, "name", T["ferris"] - 0.25, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 300, "hang", T["hang"] - 0.1, T["first"] - 0.15, accent="#7DD3FC", size=46)

    # ------------------------------------------------------------------ set: spokes (break1, fix1)
    def draw_spokes(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1180)
        cam = (0, -330, 1.18)
        self.view(c, cam)
        rot = self.rot(t) * 0.4
        if not fixed:
            th = prog(t, T["thick"] - 0.3, T["thick"])
            bk = e_io(prog(t, T["heavy"], T["buckle1"] + 0.4))
            wheel(c, t, rot=0.0, cabins=0.0, spokes=0.0, thick=th, buckle=bk, legs=1.0)
            hk = prog(t, T["heavy"] - 0.3, T["heavy"])
            if hk > 0:                                             # the weight pressing down
                for k in range(5):
                    q = (t * 0.9 + k / 5.0) % 1.0
                    arrow(c, -240 + k * 120, -720 + q * 120, -240 + k * 120, -640 + q * 120, WARN, a=hk * math.sin(q * math.pi), w=10, head=24)
        else:
            sp = prog(t, s("fix1") - 0.1, T["tight"])
            gl = prog(t, T["tight"] - 0.2, T["tight"] + 0.3) * (1 - prog(t, T["light1"], T["light1"] + 1.0) * 0.5)
            wheel(c, t, rot=rot, cabins=0.0, spokes=sp, glow=gl, legs=1.0)
            rk = prog(t, T["rim"] - 0.3, T["rim"] + 0.2)
            if rk > 0:
                c.drawCircle(0, HUB_Y, R_RIM - 8, P(HILITE, rk * 0.8, stroke=10))
            tk = prog(t, T["tight"] - 0.2, T["tight"] + 0.2)
            if tk > 0:                                             # pull arrows along a few cables
                for k in range(8):
                    ang = rot + k * 45 + 22
                    q = (t * 0.8 + k / 8.0) % 1.0
                    r0 = lerp(R_RIM - 40, 90, q)
                    x0_, y0_ = polar(r0, ang)
                    x1_, y1_ = polar(r0 - 50, ang)
                    arrow(c, x0_, y0_, x1_, y1_, HILITE, a=tk * math.sin(q * math.pi), w=7, head=18)
        c.drawRect(R(-1400, 0, 2800, 900), P("#3A4A5A"))
        c.restore()
        if fixed:
            bk2 = prog(t, T["bike"] - 0.3, T["bike"] + 0.1) * (1 - prog(t, T["tight"] + 0.3, T["tight"] + 0.6))
            if bk2 > 0:
                c.drawRRect(rr(330, 380, 420, 230, 30), P("#0B1A3A", 0.85 * bk2))
                bicycle(c, 540, 515, 1.25, t, a=bk2)

    def ui_spokes(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "thick", T["thick"] - 0.2, T["heavy"] - 0.1, accent="#94A3B8", size=46)
            self.chip(540, 300, "heavy", T["heavy"] - 0.1, T["buckle"] - 0.15, accent="#FDBA74", size=46)
            self.chip(540, 300, "buckle", T["buckle"] - 0.15, s("fix1") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["buckle1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["buckle1"], 1.2)
            return
        self.chip(540, 300, "bike", T["bike"] - 0.2, T["tight"] - 0.1, accent="#FCA5A5", size=44)
        self.chip(540, 300, "tight", T["tight"] - 0.1, T["light"] - 0.2, accent=HILITE, size=46)
        self.chip(540, 300, "stiff", T["light"] - 0.2, s("break2") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["light1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: cabin (break2, fix2), close-up of the rim
    def draw_cabin(self, c, t):
        """A smaller wheel with eight big cabins: bolted ones turn with the rim, then each sits in its own ring."""
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1250)
        c.save()                                                   # the city far below
        c.translate(540, 1250)
        c.scale(0.7, 0.7)
        skyline(c, -900, 900, 0, t)
        c.restore()
        c.drawRect(R(0, 1250, W, H - 1250), P("#1E5A7A"))
        hx, hy, rw = 540.0, 830.0, 300.0
        if not fixed:
            base = 90 - 180 * e_io(prog(t, T["turns2"] - 0.3, T["flip1"] + 0.3))
        else:
            base = -90 - 90 * prog(t, s("fix2") - 0.12, s("break3"))
        for k in range(8):                                         # cables
            q = math.radians(base + k * 45 + 22.5)
            c.drawLine(hx + math.cos(q) * 30, hy + math.sin(q) * 30, hx + math.cos(q) * rw, hy + math.sin(q) * rw,
                       P("#E5E7EB", 0.6, stroke=3))
        c.drawCircle(hx, hy, rw, P(STEELW, 1.0, stroke=14))
        c.drawCircle(hx, hy, rw - 18, P(STEELD, 1.0, stroke=5))
        c.drawCircle(hx, hy, 34, P("#CBD5E1"))
        rk = prog(t, T["ring"] - 0.3, T["ring"]) if fixed else 0.0
        mk = prog(t, T["motors"] - 0.3, T["motors"]) if fixed else 0.0
        lk = prog(t, T["level"] - 0.3, T["level"] + 0.2) if fixed else 0.0
        for k in range(8):
            ang = base + k * 45
            q = math.radians(ang)
            px, py = hx + math.cos(q) * (rw + 70), hy + math.sin(q) * (rw + 70)
            c.drawLine(hx + math.cos(q) * rw, hy + math.sin(q) * rw, px, py, P(STEELD, 1.0, stroke=8))
            if not fixed:
                cabin(c, px, py, 2.7, t, rot=ang - 90, people=3, seed=k, detail=True)
            else:
                cabin(c, px, py, 2.7, t, rot=0.0, people=3, seed=k, detail=True, ring=max(0.4, rk), ring_rot=ang * 2)
                if mk > 0:
                    gear(c, px + 52, py - 46, 12, -t * 160 + k * 20, teeth=8, col="#F59E0B", a=mk)
            if lk > 0:
                c.drawLine(px - 44, py + 40, px + 44, py + 40, P(GOOD, lk, stroke=4))
        if not fixed:
            fk = prog(t, T["flip1"] - 0.2, T["flip1"] + 0.3)
            if fk > 0:                                             # the riders at the top are upside down
                q = math.radians(base + 180 + 0.0)
                tx_, ty_ = hx + math.cos(math.radians(base)) * (rw + 70), hy + math.sin(math.radians(base)) * (rw + 70)
                for j in range(5):
                    a_ = t * 4 + j * 1.25
                    c.drawLine(tx_ + math.cos(a_) * 70, ty_ + math.sin(a_) * 70, tx_ + math.cos(a_) * 92,
                               ty_ + math.sin(a_) * 92, P(WARN, fk, stroke=5))

    def ui_cabin(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "bolted", T["bolted"] - 0.2, T["flip"] - 0.15, accent="#94A3B8", size=44)
            self.chip(540, 300, "flip", T["flip"] - 0.15, s("fix2") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["flip1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["flip1"], 1.2)
            return
        self.chip(540, 300, "ring", T["ring"] - 0.2, T["motors"] - 0.15, accent="#7DD3FC", size=46)
        self.chip(540, 300, "level", T["motors"] - 0.15, s("break3") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["level1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: drive (break3, fix3)
    def draw_drive(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1200)
        if not fixed:
            cam = (0, -360, 1.5)
            self.view(c, cam)
            wheel(c, t, rot=self.rot(t) * 0.3, cabins=1.0, legs=1.0)
            gk = e_back(prog(t, T["gigantic"] - 0.3, T["gigantic"] + 0.2))
            if gk > 0:                                             # the monster gearbox on the axle
                c.save()
                c.translate(0, HUB_Y)
                c.scale(gk, gk)
                c.drawRRect(rr(-190, -150, 380, 300, 24), P("#334155"))
                c.drawRRect(rr(-190, -150, 380, 300, 24), P("#0F172A", 1.0, stroke=6))
                gear(c, -70, -40, 90, t * 40, teeth=16, col="#64748B")
                gear(c, 80, 50, 70, -t * 52, teeth=12, col="#94A3B8")
                gear(c, 70, -90, 44, t * 80, teeth=10, col="#CBD5E1")
                c.restore()
                for k, px in enumerate((-150, 130)):               # two tiny engineers for scale
                    engineer(c, px, HUB_Y + 150, 34, SHIRTS[k], t + k, pose="look" if k else "shrug", face=1 if k == 0 else -1)
            c.drawRect(R(-1400, 0, 2800, 900), P("#3A4A5A"))
            c.restore()
            return
        cam = (0, -120, 2.0)                                       # the bottom of the rim and the boarding deck
        self.view(c, cam)
        rot = self.rot(t) * 1.6
        wheel(c, t, rot=rot, cabins=1.0, legs=1.0)
        tk = prog(t, T["tyres"] - 0.3, T["tyres"])
        by = HUB_Y + R_RIM - 8                                     # bottom of the rim
        for k in range(5):                                         # tyres above and below the rim, rolling it
            x_ = -120 + k * 60
            yy = HUB_Y + math.sqrt(max(0.0, R_RIM ** 2 - x_ ** 2))
            for sd in (-1, 1):
                tyre(c, x_, yy - 8 + sd * 26, 16, t * 400 * sd, a=tk)
        pk = prog(t, T["push"] - 0.3, T["push"])
        if pk > 0:
            for k in range(3):
                q = (t * 0.8 + k / 3.0) % 1.0
                arrow(c, -150 + q * 260, by + 60, -90 + q * 260, by + 60, HILITE, a=pk * math.sin(q * math.pi), w=8, head=20)
        c.drawRect(R(-400, -46, 800, 14), P("#E5E7EB"))            # the boarding deck
        stk = prog(t, T["step"] - 0.4, T["step1"] + 0.6)
        person(c, lerp(-150, -60, stk), -46, 30, "#F97316", t, pose="walk" if stk < 1 else "cheer", face=1)
        person(c, -190, -46, 28, "#2563EB", t + 0.5, pose="stand", face=1)
        island(c, t)
        c.restore()

    def ui_drive(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "gearbox", T["gigantic"] - 0.2, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["gear1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["gear1"], 1.2)
            return
        self.chip(540, 300, "push", T["push"] - 0.2, T["tyres"] - 0.15, accent=HILITE, size=48)
        self.chip(540, 300, "tyres", T["tyres"] - 0.15, T["slowly"] - 0.2, accent="#FDBA74", size=40)
        self.chip(540, 300, "step", T["slowly"] - 0.2, s("break4") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["step1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: lift (break4, fix4), side view of the river
    def draw_lift(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        v2.sky(c, W, H, 0.0, pal=LONDON, horizon_y=1220)
        cam = (0, -260, 1.0)
        self.view(c, cam)
        if not fixed:                                              # half a rim, a ghost of the rest, a worker on nothing
            nk = prog(t, T["nothing"] - 0.3, T["nothing1"] + 0.5)
            ghost = skia.Path()
            ghost.addCircle(0, HUB_Y, R_RIM)
            c.drawPath(ghost, dash_paint("#FFFFFF", 0.55, w=4, t=t))
            stub = skia.Path()
            stub.addArc(R(-R_RIM, HUB_Y - R_RIM, 2 * R_RIM, 2 * R_RIM), 10, 160)
            c.drawPath(stub, P(STEELW, 1.0, stroke=12))
            c.drawPath(stub, P(STEELD, 1.0, stroke=4))
            lattice(c, 170, 0, HUB_Y + 40, w=40)                    # a scaffold that stops halfway
            wy = HUB_Y - R_RIM + 60 + 520 * e_in(nk)
            wx = 40 + 60 * nk
            person(c, wx, wy, 120, "#F97316", t, pose="shrug" if nk < 0.15 else "duck", face=-1, hat="hard")
            if nk < 0.15:
                c.drawLine(wx - 70, wy + 2, wx + 70, wy + 2, dash_paint(WARN, 0.9, w=4, t=t))
            c.drawRect(R(-1400, 0, 2800, 900), P("#3A4A5A"))
            c.restore()
            return
        # London: the river and the wheel lying flat on platforms, then pulled up around its bottom edge
        c.drawRect(R(-1400, 0, 2800, 900), P("#3A4A5A"))
        vrect(c, -1400, 4, 2800, 220, ["#2A5A7A", "#163048"])
        for k in range(5):
            yy = 30 + k * 36
            c.drawLine(-1400, yy, 1400, yy + math.sin(t + k) * 3, P("#9FD3F0", 0.25, stroke=3))
        up = e_io(prog(t, T["winched"] - 0.3, T["jacks1"] + 0.8))
        ang = lerp(4, 90, up)                                      # degrees up from flat
        pivot = (0, 40)
        k_ = math.sin(math.radians(ang))
        for k in range(4):                                         # temporary platforms in the river
            c.drawRect(R(-300 + k * 170, -4, 90, 40), P("#57534E", 1 - up * 0.6))
        mast = (-420, -720)                                        # the lifting mast and its cables
        c.drawLine(-470, -10, mast[0], mast[1], P("#F59E0B", 1.0, stroke=12))
        c.drawLine(-370, -10, mast[0], mast[1], P("#F59E0B", 1.0, stroke=12))
        c.save()
        c.translate(pivot[0], pivot[1])
        c.scale(1.0, max(0.05, k_))
        c.drawCircle(0, -R_RIM, R_RIM + 6, P("#0F172A", 0.8, stroke=16))
        wheel(c, t, rot=0.0, cabins=0.0, legs=0.0, cx=0.0, cy=-R_RIM)
        c.restore()
        topx, topy = 0, pivot[1] - 2 * R_RIM * k_
        wk = prog(t, T["winched"] - 0.3, T["winched"])
        c.drawLine(mast[0], mast[1], topx, topy, P("#E5E7EB", max(0.3, wk), stroke=4))
        c.drawLine(mast[0], mast[1], -120, pivot[1] - 1.6 * R_RIM * k_, P("#E5E7EB", max(0.3, wk), stroke=3))
        box(c, mast[0] - 30, mast[1] - 40, 60, 46, "#B91C1C", r=6)  # the strand jack
        c.restore()

    def ui_lift(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "tall", T["tall"] - 0.2, T["nothing"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 300, "nothing", T["nothing"] - 0.15, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["nothing1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["nothing1"], 1.2)
            return
        self.chip(540, 300, "flat", T["london"] - 0.2, T["winched"] - 0.15, accent="#7DD3FC", size=42)
        self.chip(540, 300, "winch", T["winched"] - 0.15, s("cta") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["jacks1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: chicago (reveal, second half)
    def draw_chicago(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.0, pal=SEPIA, horizon_y=1180)
        c.save()                                                   # the Eiffel Tower far away, the one to beat
        ek = prog(t, T["beat"] - 0.4, T["beat"])
        c.translate(900, 1180)
        c.scale(0.5, 0.5)
        eiffel(c, 0, 0, 1.0, t, a=0.35 + 0.5 * ek)
        c.restore()
        old_wheel(c, 430, 1190, 1.35, t, rot=self.rot(t) * 0.6)
        c.drawRect(R(0, 1180, W, H - 1180), P("#5A4A38"))
        rng = random.Random(4)
        for k in range(40):                                        # the crowd of 1893
            px = rng.uniform(20, 1060)
            c.drawCircle(px, 1196 + rng.uniform(0, 30), 7, P("#2A1E16"))
        c.drawRect(R(0, 0, W, H), P("#704214", 0.12))

    def ui_chicago(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "first", T["first"] - 0.05, T["beat"] - 0.2, accent="#FDE68A", size=46)
        self.chip(540, 300, "beat", T["beat"] - 0.2, s("stat") - 0.15, accent=HILITE, size=40)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1300)
        c.save()                                                   # the city far below through the glass
        c.translate(540, 1300)
        c.scale(1.1, 1.1)
        skyline(c, -700, 700, 0, t)
        c.restore()
        c.drawRect(R(0, 1300, W, H - 1300), P("#1E5A7A"))
        c.drawRRect(rr(-60, 380, 1200, 1180, 160), P("#BAE6FD", 0.12))      # the cabin's glass
        c.drawRRect(rr(-60, 380, 1200, 1180, 160), P("#F8FAFC", 0.9, stroke=14))
        c.drawRect(R(0, 1420, W, 500), P("#CBD5E1"))
        if not self.rtl:
            pk = prog(t, T["t_film"] - 0.3, T["t_film"])
            person(c, 360, 1640, 560, "#2563EB", t, pose="point", face=1, a=1.0)
            c.save()                                               # the phone held up, recording
            c.translate(528, 990)
            c.rotate(-8)
            c.drawRRect(rr(-70, -120, 140, 240, 20), P("#111827"))
            c.drawRRect(rr(-60, -108, 120, 216, 12), P("#3E6AA8"))
            c.drawRect(R(-60, 30, 120, 78), P("#1E3A5F"))
            if int(t * 2) % 2 == 0:
                c.drawCircle(-40, -90, 8, P("#EF4444", pk))
            c.restore()
            nk = prog(t, T["t_never"] - 0.3, T["t_never"])
            if nk > 0:                                             # the camera roll: thousands of videos, all unwatched
                c.drawRRect(rr(620, 520, 380, 520, 26), P("#111827", nk))
                for j in range(5):
                    for i in range(3):
                        c.drawRRect(rr(640 + i * 120, 540 + j * 98, 108, 88, 10), P("#334155", nk))
                        c.drawPath(path_of([(684 + i * 120, 570 + j * 98), (684 + i * 120, 606 + j * 98),
                                            (712 + i * 120, 588 + j * 98)], close=True), P("#E5E7EB", nk))
        else:
            sk = prog(t, T["t_film"] - 0.2, T["t_film"] + 0.2)
            jig = math.sin(t * 40) * 8 * sk
            person(c, 420 + jig, 1640, 560, "#1F2937", t, pose="stand" if sk < 0.5 else "duck", face=1, hair="#111827", a=1.0)
            ky = 0.64 if sk >= 0.5 else 1.0
            c.drawRRect(rr(382 + jig, 1640 - 112 * 4 * ky - 2, 76, 16, 8), P("#111827"))   # the moustache
            if sk > 0:
                for k in range(6):
                    q = math.radians(-150 + k * 22)
                    c.drawLine(460 + math.cos(q) * 300, 980 + math.sin(q) * 300, 460 + math.cos(q) * 360,
                               980 + math.sin(q) * 360, P(WARN, sk, stroke=8))

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            self.chip(540, 300, "film", T["t_film"] - 0.2, T["t_never"] - 0.2, accent=WARN, size=44)
            self.chip(540, 300, "never", T["t_never"] - 0.2, self.duration + 1, accent=HILITE, size=46)
        else:
            bubble(c, 700, 560, self.L["bubble"], self.span(T["t_lift"], T["t_film"] - 0.1), tail_left=True, size=50)
            self.chip(540, 300, "never", T["t_film"] - 0.1, self.duration + 1, accent=WARN, size=46)

    def whip_backdrop(self, c, t, m):
        pal = SEPIA if m == "chicago" else LONDON if m == "lift" else GOLDEN
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whirr(max(1.5, T["dubai"] + 0.5), 60.0, 80.0, 61), -22), (T["seventeen"], sfx.pop(62), -10)]
        ev += [(max(0.3, T["dubai"] - 0.4), sfx.whoosh(0.7, False, 70), -10), (T["cables"], sfx.sparkle(0.8, 10, 71), -10),
               (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 72), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 73), -8),
               (T["ferris"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["thick"], sfx.clank(260.0, 0.6, 75), -10),
               (T["heavy"], sfx.creak(1.0, 76), -10), (T["buckle1"], rumble(1.0, 77), -12),
               (T["buckle1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["tight"], sfx.charge_up(0.6), -12),
               (T["rim"], sfx.sparkle(0.6, 8, 79), -10), (T["light1"], sfx.ding(), -8), (T["light1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 80), -4), (T["turns2"], sfx.whirr(1.2, 110.0, 150.0, 81), -16),
               (T["flip1"], sfx.womp(), -8), (T["flip1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 82), -4), (T["motors"], sfx.whirr(1.0, 300.0, 420.0, 83), -14),
               (T["level1"], sfx.ding(), -8), (T["level1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 84), -4), (T["gigantic"], sfx.clank(180.0, 0.8, 85), -8),
               (T["gear1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 86), -4), (T["tyres"], sfx.whirr(1.4, 160.0, 200.0, 87), -14),
               (T["step1"], sfx.ding(), -8), (T["step1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 88), -4), (T["nothing1"], sfx.whoosh(0.6, False, 89), -10),
               (T["nothing1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 90), -4), (T["winched"], sfx.creak(1.4, 91), -12)]
        for k in range(4):
            ev.append((T["winched"] + 0.3 + k * 0.35, sfx.clank(500.0, 0.2, 92 + k), -16))
        ev += [(T["jacks1"], sfx.thunk(96), -8), (T["jacks1"] + 0.2, sfx.ding(), -8), (T["jacks1"] + 0.4, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(97), 0), (T["follow"] - 0.15, sfx.pop(98), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 99), -6)]
        for k in range(6):
            ev.append((lerp(T["hang"], T["turn"], k / 6.0), sfx.pop(100 + k), -12))
        ev += [(T["first"] - 0.12, sfx.whoosh(0.45, True, 107), -6), (T["beat"], sfx.bell(660.0, 0.8, 0.8), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 108), -6), (T["s1"], sfx.pop(109), -3), (T["s2"], sfx.pop(110), -3),
               (T["s3"], sfx.pop(111), -3)]
        ev += [(T["cong2"], sfx.pop(112), -2), (T["cong2"], sfx.sparkle(1.4, 18, 113), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 114), -6), (T["t_film"], sfx.beep(1200.0, 0.12), -12),
               (T["t_never"], sfx.buzz(0.4), -14)]
        return ev


NAME = "ferriswheel"
EPISODE = FerrisWheel
