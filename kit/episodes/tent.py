"""Episode 62 - A Bedouin tent (bayt al-sha'ar, the house of hair).  v2 look: a black goat-hair tent on golden dunes,
deep shade inside, a red rug, a woven Sadu curtain, the coffee fire.

Sets: camp (hook: rain pours on the black roof and runs off its edge while the family drinks coffee dry inside, then a
breeze blows through; stat: by day; closer: at dusk with the fire lit), sun (break1: a thin white tent under the desert
sun turns into an oven; fix1: the black tent's deep shade, hot air slipping out through the weave), weave (break2: the
weave close up, air and rain both pass the gaps; fix2: the goat hair swells when wet, closes the gaps, the rain beads and
runs off), wind (break3: wind and sand blow into the open front; fix3: wall panels pinned down on the windy side, the
other side opened), move (break4: the family follows the herd; fix4: the tent comes down to strips, poles and ropes and
rides on a camel), loom (reveal: a woman weaving a strip on a ground loom, then the tent split by its curtain into the
guests' side and the family's), tag (an umbrella flipping inside out in the first breeze, the tent calm behind).
World (camp): front view, sand at y = 0, the tent 900 units wide centred on x = 0.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, sun, heat_lines, wind_lines, thermo  # noqa: E402
from burjalarab import path_of  # noqa: E402
from camel import camel, SANDS  # noqa: E402
from pyramid import palm  # noqa: E402
from liberty import rain  # noqa: E402
from dam import rain_snd  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STORM = {"top": "#0A0F1E", "upper": "#1A2238", "mid": "#2E3A52", "low": "#4A5468", "horizon": "#7A7484",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DUSKY = {"top": "#07071F", "upper": "#1E1650", "mid": "#5E2E68", "low": "#C9604A", "horizon": "#F49A5C",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
HAIR = ("#2A221D", "#1C1714", "#352B24")        # the roof strips, alternating
RUG = "#B91C1C"
SADU = ("#B91C1C", "#F5E6C8", "#111827", "#D97706")
COFFEE = "#D4A017"
POLES = ((-300.0, 262.0), (0.0, 282.0), (300.0, 262.0))
EAVE = 150.0                                     # height of the front edge
HALF = 450.0                                     # half width


def roof_pts(sag=1.0, lift=0.0):
    """Outline of the roof in front view: eave left, the three pole peaks with sagging cloth between, eave right."""
    pts = [(-HALF, -EAVE - lift)]
    peaks = [(x, -h - lift) for x, h in POLES]
    prev = pts[0]
    for px, py in peaks:
        for k in range(1, 9):
            q = k / 8
            sg = math.sin(math.pi * q) * 16 * sag
            pts.append((lerp(prev[0], px, q), lerp(prev[1], py, q) + sg))
        prev = (px, py)
    end = (HALF, -EAVE - lift)
    for k in range(1, 9):
        q = k / 8
        pts.append((lerp(prev[0], end[0], q), lerp(prev[1], end[1], q) + math.sin(math.pi * q) * 16 * sag))
    return pts


def eave_pts(lift=0.0):
    """The front edge of the roof, sagging between the short front poles (right to left)."""
    out = []
    xs = (HALF, 150.0, -150.0, -HALF)
    for i in range(3):
        for k in range(9):
            q = k / 8
            out.append((lerp(xs[i], xs[i + 1], q), -EAVE - lift + math.sin(math.pi * q) * 14))
    return out


def sadu_band(c, x, y, w, h, a=1.0, seed=0):
    """A woven Sadu panel: stripes and a row of red and white triangles."""
    c.drawRect(R(x, y, w, h), P(SADU[2], a))
    n = max(1, int(h / 26))
    for k in range(n):
        yy = y + k * h / n
        col = SADU[k % 4]
        c.drawRect(R(x, yy, w, h / n * 0.45), P(col, 0.9 * a))
        m = max(2, int(w / 22))
        for j in range(m):
            xx = x + j * w / m
            c.drawPath(path_of([(xx, yy + h / n * 0.45), (xx + w / m / 2, yy + h / n * 0.95), (xx + w / m, yy + h / n * 0.45)],
                               close=True), P(SADU[(k + j) % 2], 0.85 * a))


def tent(c, t, a=1.0, inside=1.0, fire=1.0, people=1.0, wall_l=0.0, wall_r=0.0, wet=0.0, lit=0.0, shade_k=1.0, ropes=1.0,
         curtain=1.0, hot=0.0, thin=0.0, duck=False):
    """The black tent standing on y = 0 (world). wall_l / wall_r 0..1 drop the side wall panels (left = windy side);
    wet 0..1 makes the roof glisten; thin 0..1 turns it into a thin white tent (break1)."""
    if a <= 0:
        return
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    # guy ropes and pegs
    if ropes > 0:
        for sd in (-1, 1):
            for px, h in ((sd * HALF, EAVE), (POLES[0 if sd < 0 else 2][0], POLES[0][1])):
                c.drawLine(px, -h, sd * 760, 0, P("#C8B48A", 0.8 * ropes, stroke=3))
            c.drawRect(R(sd * 760 - 5, -16, 10, 20), P("#6B4A2A", ropes))
    # inside: the back wall in deep shade, the rug, cushions, the curtain, the fire
    if inside > 0:
        back = mix("#3A2A20", "#F1E6D0", thin)
        c.drawRect(R(-HALF + 10, -EAVE - 10, 2 * HALF - 20, EAVE + 10), lin_paint(0, -EAVE, 0, 0, [shade(back, -0.2), back], a=inside))
        c.drawRect(R(-HALF + 20, -14, 2 * HALF - 40, 14), P(RUG, inside))
        for k in range(14):
            c.drawRect(R(-HALF + 30 + k * 62, -11, 30, 8), P("#F5E6C8", 0.45 * inside))
        for k in range(7):                                       # cushions along the back
            cx_ = -400 + k * 66
            if abs(cx_ - 60) < 40:
                continue
            c.drawRRect(rr(cx_ - 26, -52, 52, 40, 12), P(SADU[k % 4], 0.9 * inside))
        if curtain > 0:                                          # the Sadu curtain between guests and family
            sadu_band(c, 40, -EAVE - 4, 44, EAVE - 10, a=curtain * inside)
        if fire > 0:
            c.drawOval(R(-260, -14, 80, 16), P("#3A2A20", inside))
            v2.flame(c, -220, -10, 50, 60, t, power=fire, ang=-90.0)
            add_glow(c, -220, -40, 160, "#FF9A3D", 0.35 * fire * inside)
            dx, dy = -170, -22                                   # the coffee pot by the fire
            c.drawPath(path_of([(dx - 14, dy), (dx + 14, dy), (dx + 10, dy - 30), (dx - 10, dy - 30)], close=True), P(COFFEE, inside))
            c.drawPath(path_of([(dx - 10, dy - 30), (dx + 10, dy - 30), (dx, dy - 46)], close=True), P(COFFEE, inside))
            c.drawLine(dx + 12, dy - 22, dx + 30, dy - 36, P(COFFEE, inside, stroke=4))
        if people > 0:
            ps = "duck" if duck else "sit"
            person(c, -330, 0, 66, "#F5F5F4", t, pose=ps, face=1, a=people * inside, skin="#C68B59", hair="#1F2937")
            person(c, -120, 0, 66, "#E7E5E4", t + 1, pose=ps, face=-1, a=people * inside, skin="#B57A4A", hair="#111827")
            person(c, 230, 0, 62, "#7C2D12", t + 2, pose=ps, face=-1, a=people * inside, skin="#C68B59", hair="#1F2937")
            person(c, 320, 0, 44, "#2563EB", t + 3, pose="duck" if duck else "stand", face=-1, a=people * inside, skin="#C68B59",
                   hair="#111827")
        if shade_k > 0 and thin < 1:
            c.drawRect(R(-HALF, -EAVE, 2 * HALF, EAVE), P("#000000", 0.18 * shade_k * (1 - thin)))
        if hot > 0:
            c.drawRect(R(-HALF, -EAVE, 2 * HALF, EAVE), P("#FF6A2A", 0.35 * hot))
    # side walls (pinned panels)
    for sd, k in ((-1, wall_l), (1, wall_r)):
        if k > 0:
            x0 = sd * HALF
            pw = 150 * k
            c.drawPath(path_of([(x0, -EAVE), (x0 - sd * 6, -EAVE + pw), (x0 - sd * 40, -EAVE + pw), (x0 - sd * 40, -EAVE)], close=True),
                       P(HAIR[1], 1.0))
            for j in range(3):
                c.drawCircle(x0 - sd * 20, -EAVE + 6 + j * 2, 4, P("#C8B48A", k))
    # the roof
    rp = path_of(roof_pts() + eave_pts(), close=True)
    if thin > 0:
        c.drawPath(rp, lin_paint(0, -300, 0, -EAVE, ["#FFFFFF", "#E5E7EB"], a=thin))
    if thin < 1:
        c.save()
        c.clipPath(rp, doAntiAlias=True)
        for k in range(9):                                       # the woven strips, sewn edge to edge
            y0 = -300 + k * 18
            c.drawRect(R(-HALF - 10, y0, 2 * HALF + 20, 18), P(mix(HAIR[k % 3], "#F3D19C", 0.12 * lit), 1 - thin))
            c.drawLine(-HALF - 10, y0, HALF + 10, y0, P("#4A3C30", 0.7 * (1 - thin), stroke=2))
        rng = random.Random(5)
        for _ in range(60):                                      # hairy texture
            xx, yy = rng.uniform(-HALF, HALF), rng.uniform(-300, -EAVE)
            c.drawLine(xx, yy, xx + rng.uniform(-8, 8), yy + rng.uniform(-3, 3), P("#5A4A3C", 0.35 * (1 - thin), stroke=1.5))
        if wet > 0:
            for k in range(30):
                xx = rng.uniform(-HALF, HALF)
                yy = -300 + ((t * 60 + k * 37) % 150)
                c.drawCircle(xx, yy, 3.5, P("#BFE3FF", 0.7 * wet))
        c.restore()
    for px, h in POLES:                                          # the pole tips above the cloth
        c.drawRect(R(px - 4, -h - 10, 8, 14), P("#6B4A2A", a))
    for px in (-HALF, -150.0, 150.0, HALF):                      # the short front poles
        c.drawRect(R(px - 4, -EAVE, 8, EAVE), P("#6B4A2A", a))
    if a < 1:
        c.restore()


def dunes(c, cam, t, pal_k=0.0, night=0.0):
    """Far dunes in screen space with parallax, then the near sand in world space is drawn by the set."""
    cx, cy, z = cam
    gy = (0 - cy) * z + H / 2
    for i, (h_, col, par) in enumerate(((150, "#C98A52", 0.05), (90, "#B5733E", 0.12))):
        col = mix(col, "#2A1C2E", night)
        p_ = skia.Path()
        p_.moveTo(0, gy)
        for k in range(13):
            xx = k * 90
            p_.lineTo(xx, gy - h_ * z * 0.5 - math.sin((xx + cx * par * z) * 0.006 + i) * 40 * z)
        p_.lineTo(W, gy)
        p_.close()
        c.drawPath(p_, P(col))


def sand(c, night=0.0):
    c.drawRect(R(-3000, 0, 6000, 1600), lin_paint(0, 0, 0, 900, [mix(SANDS[0], "#3A2A2E", night), mix(SANDS[1], "#2A1E22", night),
                                                                   mix(SANDS[2], "#1A1216", night)]))
    rng = random.Random(8)
    for _ in range(40):
        xx, yy = rng.uniform(-1500, 1500), rng.uniform(10, 600)
        c.drawLine(xx, yy, xx + 60, yy - 4, P("#FFFFFF", 0.06, stroke=3))


def goat(c, x, y, s, t, walk=0.0, a=1.0, col="#1C1714"):
    """A small black goat, side view facing right, feet on y."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    sw = math.sin(t * 9 + x) * 6 * walk
    for lx, ph in ((-22, 0), (-12, 1), (14, 1), (24, 0)):
        c.drawLine(lx, -30, lx + (sw if ph else -sw), 0, P(col, a, stroke=6))
    c.drawRRect(rr(-32, -54, 66, 30, 14), P(col, a))
    c.drawPath(path_of([(26, -50), (46, -66), (52, -56), (38, -42)], close=True), P(col, a))
    c.drawLine(42, -64, 34, -80, P("#9CA3AF", a, stroke=4))
    c.drawLine(-32, -50, -40, -58, P(col, a, stroke=5))
    c.restore()


def umbrella(c, x, y, s, flip=0.0, a=1.0, col="#2563EB"):
    """An umbrella (screen or world), handle at (x, y); flip 0..1 turns it inside out."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawLine(0, 0, 0, -160, P("#374151", a, stroke=6))
    c.drawPath(path_of([(0, 0), (0, 12), (-14, 18)]), P("#374151", a, stroke=6))
    k = e_out(clamp(flip))
    bow = lerp(-60, 50, k)
    p_ = skia.Path()
    p_.moveTo(-110 - 20 * k, -150 + bow * 0.2 - 40 * k)
    p_.quadTo(0, -160 + bow * 1.4 - 60 * (1 - k), 110 + 20 * k, -150 + bow * 0.2 - 40 * k)
    p_.quadTo(0, -150 + bow * 0.6, -110 - 20 * k, -150 + bow * 0.2 - 40 * k)
    c.drawPath(p_, P(col, a))
    for sx in (-1, 0, 1):
        c.drawLine(0, -160, sx * 100 * (1 + 0.2 * k), -150 + bow * 0.2 - 40 * k, P("#1E3A8A", a, stroke=3))
    c.restore()


def weave(c, x, y, w, h, t, swell=0.0, a=1.0, n=7):
    """Close-up of the goat-hair weave (screen space): threads with gaps; swell 0..1 thickens them shut."""
    c.drawRect(R(x, y, w, h), P("#0B0A10", a))
    sp = w / n
    tw = sp * lerp(0.62, 1.04, swell)
    for k in range(n + 1):                                       # warp (vertical) and weft (horizontal)
        xx = x + k * sp
        c.drawRRect(rr(xx - tw / 2, y, tw, h, tw / 2), P(HAIR[k % 3], a))
        yy = y + k * sp * h / w
        c.drawRRect(rr(x, yy - tw / 2, w, tw, tw / 2), P(HAIR[(k + 1) % 3], a))
    rng = random.Random(4)
    for _ in range(140):                                         # hairs
        xx, yy = rng.uniform(x, x + w), rng.uniform(y, y + h)
        c.drawLine(xx, yy, xx + rng.uniform(-14, 14), yy + rng.uniform(-14, 14), P("#5A4A3C", 0.5 * a, stroke=2))


# ====================================================================================== the episode
class Tent(EpisodeV2):
    BUILD_NO = 62
    FIRST_SET = "camp"
    CLEAR = "#0A0F1E"
    TITLE = {"en": "BEDOUIN TENT", "ar_sa": "خيمة البدو"}
    EMPH = {"en": ["CONGRATS", "WEAVE", "HOUSE", "GOAT", "HAIR", "STOPS", "DESERT", "RAIN", "BREEZE", "BEDOUIN", "TENT",
                   "YOURSELF", "SUN", "BRUTAL", "THIN", "OVEN", "BLACK", "THICK", "DEEP", "SHADE", "HOT", "AIR", "SLIPS",
                   "OUT", "GOATS", "WET", "SWELLS", "CLOSES", "GAPS", "RUNS", "OFF", "WIND", "CHANGING", "DIRECTION",
                   "SAND", "FACE", "WALLS", "LOOSE", "PANELS", "PINS", "DROP", "WINDY", "OPEN", "FAMILY", "MOVES",
                   "HERDS", "AGAIN", "STRIPS", "WOODEN", "POLES", "ROPES", "CAMEL", "FOLLOW", "WASHING", "MACHINE",
                   "WOMEN", "STRIP", "HAND", "LOOM", "GROUND", "CURTAIN", "SPLITS", "GUESTS'", "ZERO", "NAILS",
                   "BRICKS", "THOUSANDS", "YEARS", "STORMS", "UMBRELLA", "FLIPS", "INSIDE"],
            "ar_sa": ["مبروك", "تنسج", "بيت", "شعر", "المعيز", "يصد", "مطر", "الصحرا", "النسمة", "خيمة", "البدو",
                      "الشعر", "بإيدك", "شمس", "نار", "الرقيقة", "فرن", "سودا", "وتقيلة", "ضل", "السخن", "الخيوط",
                      "الهوا", "المطر", "يتبل", "بينتفخ", "ويقفل", "الخروم", "يتزحلق", "هوا", "بيلف", "الرملة", "وشك",
                      "فالحيطان", "ستاير", "بتتشبك", "تنزّلها", "وتفتح", "العيلة", "الغنم", "شرايط", "منسوجة",
                      "وعواميد", "وحبال", "الجمل", "تابعني", "غسالة", "الستات", "شريط", "بإيديهم", "نول", "وستارة",
                      "بتقسم", "للضيوف", "للعيلة", "مسمار", "طوبة", "آلاف", "السنين", "عواصف", "الشمسية", "بتتقلب",
                      "نسمة"]}
    KEYS = {"ar_sa": {
        ("hook", "WEAVE"): "تنسج", ("hook", "GOAT"): "المعيز", ("hook", "RAIN"): "مطر", ("hook", "BREEZE"): "النسمة",
        ("hook", "CONGRATS"): "مبروك", ("hook", "BEDOUIN"): "البدو",
        ("break1", "SUN"): "شمس", ("break1", "THIN"): "الرقيقة", ("break1", "OVEN"): "فرن",
        ("fix1", "BLACK"): "سودا", ("fix1", "THICK"): "وتقيلة", ("fix1", "SHADE"): "ضل", ("fix1", "HOT"): "السخن",
        ("fix1", "WEAVE"): "الخيوط",
        ("break2", "AIR"): "الهوا", ("break2", "RAIN"): "المطر",
        ("fix2", "GOATS"): "المعيز", ("fix2", "WET"): "يتبل", ("fix2", "SWELLS"): "بينتفخ", ("fix2", "GAPS"): "الخروم",
        ("fix2", "RUNS"): "يتزحلق",
        ("break3", "WIND"): "هوا", ("break3", "CHANGING"): "بيلف", ("break3", "SAND"): "الرملة", ("break3", "FACE"): "وشك",
        ("fix3", "WALLS"): "فالحيطان", ("fix3", "PINS"): "بتتشبك", ("fix3", "DROP"): "تنزّلها", ("fix3", "WINDY"): "الهوا",
        ("fix3", "OPEN"): "وتفتح",
        ("break4", "FAMILY"): "العيلة", ("break4", "HERDS"): "الغنم", ("break4", "AGAIN"): "مرة",
        ("fix4", "STRIPS"): "شرايط", ("fix4", "POLES"): "وعواميد", ("fix4", "ROPES"): "وحبال", ("fix4", "CAMEL"): "الجمل",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "WOMEN"): "الستات", ("reveal", "STRIP"): "شريط", ("reveal", "LOOM"): "نول",
        ("reveal", "CURTAIN"): "وستارة", ("reveal", "SPLITS"): "بتقسم",
        ("stat", "ZERO"): "مسمار", ("stat", "BRICKS"): "طوبة", ("stat", "THOUSANDS"): "آلاف",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STORMS"): "عواصف", ("tag", "UMBRELLA"): "الشمسية", ("tag", "FLIPS"): "بتتقلب", ("tag", "BREEZE"): "نسمة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a washing machine"),
                   "stat": [("0", "NAILS"), ("0", "BRICKS"), ("1000s", "YEARS OF STORMS")],
                   "L": {"hair": "WOVEN FROM GOAT HAIR", "dry": "RAIN OUTSIDE, DRY INSIDE", "breeze": "AND THE BREEZE GETS IN",
                         "name": "A BEDOUIN TENT", "oven": "A THIN TENT = AN OVEN", "black": "BLACK + THICK",
                         "shade": "DEEP SHADE", "out": "HOT AIR SLIPS OUT", "air": "AIR GETS THROUGH...",
                         "rainin": "...SO DOES THE RAIN", "goat": "GOAT HAIR", "swells": "WET HAIR SWELLS",
                         "closed": "GAPS CLOSED, RAIN RUNS OFF", "sand": "SAND IN YOUR FACE", "walls": "WALL PANELS ON PINS",
                         "drop": "DOWN ON THE WINDY SIDE", "open": "OPEN ON THE OTHER", "moves": "AGAIN AND AGAIN",
                         "pack": "STRIPS + POLES + ROPES", "camel": "IT RIDES ON A CAMEL", "loom": "WOVEN BY HAND",
                         "guests": "GUESTS", "family": "FAMILY", "storms": "THOUSANDS OF YEARS OF STORMS",
                         "flip": "FIRST BREEZE..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: غسالة"),
                      "stat": [("0", "مسمار"), ("0", "طوبة"), ("1000+", "سنة عواصف")],
                      "L": {"hair": "منسوج من شعر المعيز", "dry": "مطر برة، ناشف جوه", "breeze": "والنسمة بتعدّي",
                            "name": "خيمة البدو", "oven": "الخيمة الرقيقة = فرن", "black": "سودا وتقيلة",
                            "shade": "ضل تقيل", "out": "الهوا السخن بيطلع", "air": "الهوا بيعدّي...",
                            "rainin": "...والمطر كمان", "goat": "شعر المعيز", "swells": "الشعر المبلول بينتفخ",
                            "closed": "الخروم اتقفلت", "sand": "الرملة في وشك", "walls": "ستاير بتتشبك وتتفك",
                            "drop": "تنزل ناحية الهوا", "open": "وتتفتح الناحية التانية", "moves": "مرة ورا مرة",
                            "pack": "شرايط وعواميد وحبال", "camel": "على ضهر الجمل", "loom": "بالإيد على النول",
                            "guests": "الضيوف", "family": "العيلة", "storms": "آلاف السنين قدام العواصف",
                            "flip": "أول نسمة..."}}}
    STAT_COLORS = (INK, "#FFB05C", HILITE)
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "weave": ("hook", "WEAVE", 0.1), "goat": ("hook", "GOAT", 0.25), "rain": ("hook", "RAIN", 0.4),
            "breeze": ("hook", "BREEZE", 0.55), "congrats": ("hook", "CONGRATS", 0.7), "bedouin": ("hook", "BEDOUIN", 0.9),
            "sun": ("break1", "SUN", 0.2), "thin": ("break1", "THIN", 0.6), "oven": ("break1", "OVEN", 0.9),
            "black": ("fix1", "BLACK", 0.15), "thick": ("fix1", "THICK", 0.25), "shade": ("fix1", "SHADE", 0.5),
            "hot": ("fix1", "HOT", 0.7), "weave1": ("fix1", "WEAVE", 0.95),
            "air": ("break2", "AIR", 0.3), "rain2": ("break2", "RAIN", 0.9),
            "goats": ("fix2", "GOATS", 0.15), "wet": ("fix2", "WET", 0.35), "swells": ("fix2", "SWELLS", 0.5),
            "gaps": ("fix2", "GAPS", 0.7), "runs": ("fix2", "RUNS", 0.9),
            "wind": ("break3", "WIND", 0.15), "changing": ("break3", "CHANGING", 0.4), "sand": ("break3", "SAND", 0.7),
            "face": ("break3", "FACE", 0.95),
            "walls": ("fix3", "WALLS", 0.1), "pins": ("fix3", "PINS", 0.35), "drop": ("fix3", "DROP", 0.55),
            "windy": ("fix3", "WINDY", 0.7), "open": ("fix3", "OPEN", 0.9),
            "family": ("break4", "FAMILY", 0.2), "herds": ("break4", "HERDS", 0.6), "again": ("break4", "AGAIN", 0.85),
            "strips": ("fix4", "STRIPS", 0.3), "poles": ("fix4", "POLES", 0.5), "ropes": ("fix4", "ROPES", 0.6),
            "camel": ("fix4", "CAMEL", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "women": ("reveal", "WOMEN", 0.1), "strip": ("reveal", "STRIP", 0.25), "loom": ("reveal", "LOOM", 0.4),
            "curtain": ("reveal", "CURTAIN", 0.6), "splits": ("reveal", "SPLITS", 0.7),
            "s1": ("stat", "ZERO", 0.05), "s2": ("stat", "BRICKS", 0.35), "s3": ("stat", "THOUSANDS", 0.6),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_storm": ("tag", "STORMS", 0.15), "t_umb": ("tag", "UMBRELLA", 0.55), "t_flip": ("tag", "FLIPS", 0.75),
            "t_breeze": ("tag", "BREEZE", 0.95)})
        T["oven1"] = max(T["oven"], T["thin"]) + 0.1
        T["rain21"] = max(T["rain2"], T["air"]) + 0.1
        T["face1"] = max(T["face"], T["sand"]) + 0.1
        T["again1"] = max(T["again"], T["herds"]) + 0.1
        T["weave11"] = max(T["weave1"], T["hot"]) + 0.2
        T["runs1"] = max(T["runs"], T["gaps"]) + 0.2
        T["open1"] = max(T["open"], T["windy"], T["drop"]) + 0.2
        T["camel1"] = max(T["camel"], T["ropes"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "sun", 1)
        self.cut(s("break2") - 0.12, "weave", -1)
        self.cut(s("break3") - 0.12, "wind", 1)
        self.cut(s("break4") - 0.12, "move", -1)
        self.cut(s("reveal") - 0.12, "loom", 1)
        self.cut(s("stat") - 0.12, "camp", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- camp camera: from the wet black roof in the rain, out to the whole tent with the family dry inside
        cm = Camera(-90, -230, 3.4)
        cm.key(0.05, -94, -232, 3.3, 0.4)
        cm.key(max(0.5, T["goat"] - 0.3), -20, -150, 1.6, max(1.2, T["rain"] - T["goat"] + 0.8))
        cm.key(T["congrats"], -10, -146, 1.66, max(1.0, s("break1") - T["congrats"]))
        cm.key(s("stat") - 0.12, 0, -150, 1.5, 0.0).key(s("stat"), 0, -152, 1.52, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, -20, -150, 1.6, 1.0).key(s("closer") + 0.9, -20, -148, 1.7, 3.0)
        self.cam = cm
        self.spans = [(T["oven1"], T["weave11"] + 0.3), (T["rain21"], T["runs1"] + 0.3), (T["face1"], T["open1"] + 0.3),
                      (T["again1"], T["camel1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["oven1"], 0.3, 6), (T["rain21"], 0.3, 6), (T["face1"], 0.45, 9),
                       (T["again1"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["t_flip"], 0.3, 8)]

    # ------------------------------------------------------------------ set: camp (hook, stat, closer)
    def draw_camp(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        closer = t >= s("closer") - 0.1
        night = prog(t, s("closer") - 0.1, s("closer") + 0.8) if closer else 0.0
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        storm = 0.0
        if hook:
            storm = 1.0 - prog(t, T["breeze"] - 0.2, T["congrats"] + 0.4)
        pal = DUSKY if closer else GOLDEN
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=gy)
        if closer:
            v2.stars(c, W, H, t, 0.8 * night)
        else:
            sun(c, 860 - cx * 0.03, gy - 380, 60, heat=0.6, a=1 - storm)
        if storm > 0:
            vrect(c, 0, 0, W, H, [("#1A2234", 0.92 * storm), ("#4A5468", 0.85 * storm)])
        dunes(c, cam, t, night=night)
        self.view(c, cam)
        sand(c, night)
        palm(c, -760, 0, 260, sway=math.sin(t * 2) * 0.3)
        palm(c, -640, 0, 200, sway=math.sin(t * 2 + 1) * 0.3)
        camel(c, 640, 0, 0.55, 0.0, run=0.0)
        for k, gx in enumerate((520, 580, 470)):
            goat(c, gx, 30 + k * 6, 0.9, t, walk=0.0)
        tent(c, t, wet=storm, fire=1.0, lit=night)
        if storm > 0:                                            # drips off the front edge
            for k, (ex, ey) in enumerate(eave_pts()[::2]):
                q = (t * 1.6 + k * 0.37) % 1.0
                c.drawLine(ex, ey + q * 140, ex, ey + q * 140 + 16, P("#BFE3FF", 0.8 * storm, stroke=3))
        if hook:
            bk = prog(t, T["breeze"] - 0.3, T["breeze"]) * (1 - prog(t, T["bedouin"] - 0.3, T["bedouin"] + 0.4))
            if bk > 0:
                wind_lines(c, -700, 700, -140, -40, t, a=bk, col="#E0F2FE", n=7, speed=500.0)
        c.restore()
        if storm > 0:
            rain(c, t, a=storm)
        if closer:
            add_glow(c, *self.to_screen(cam, -220, -40), 260 * z, "#FF9A3D", 0.35 * night)

    def ui_camp(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "hair", T["weave"] - 0.1, T["rain"] - 0.1, accent="#FDE68A", size=46)
            self.chip(540, 300, "dry", T["rain"] - 0.1, T["breeze"] - 0.1, accent="#7DD3FC", size=44)
            self.chip(540, 300, "breeze", T["breeze"] - 0.1, T["bedouin"] - 0.3, accent=GOOD, size=44)
            self.chip(540, 300, "name", T["bedouin"] - 0.3, s("break1") + 0.1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: sun (break1, fix1)
    def draw_sun(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        cam = (0, -150, 1.6)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        vrect(c, 0, 0, W, gy, [("#FFB347", 0.25), ("#FF8A3D", 0.15)])
        sun(c, 820, 330, 90, heat=1.0)
        dunes(c, cam, t)
        self.view(c, cam)
        sand(c)
        if not fixed:
            hk = prog(t, T["thin"] - 0.3, T["oven1"] + 0.4)
            tent(c, t, thin=1.0, hot=hk, fire=0.0, people=1.0, curtain=0.0, shade_k=0.0)
            heat_lines(c, -400, 400, -140, -20, t, a=hk)
        else:
            tent(c, t, fire=0.0, shade_k=prog(t, T["shade"] - 0.4, T["shade"]) * 2.5, curtain=1.0)
            ok = prog(t, T["hot"] - 0.3, T["weave11"])
            for k in range(6):                                   # hot air rising out through the roof
                x_ = -360 + k * 144
                q = (t * 0.7 + k * 0.17) % 1.0
                y0 = lerp(-120, -420, q)
                arrow(c, x_, y0 + 40, x_ + 6, y0 - 40, "#FB923C", a=ok * (1 - q * 0.6), w=8, head=20)
        c.restore()
        if not fixed:
            thermo(c, 930, 760, 1.4, lerp(0.3, 1.0, prog(t, T["thin"] - 0.3, T["oven1"])), a=prog(t, T["sun"] - 0.3, T["sun"]),
                   hot=True)

    def ui_sun(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "oven", T["thin"] - 0.2, s("fix1") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["oven1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["oven1"], 1.2)
            return
        self.chip(540, 300, "black", T["black"] - 0.2, T["shade"] - 0.2, accent="#FDE68A", size=48)
        self.chip(540, 300, "shade", T["shade"] - 0.2, T["hot"] - 0.2, accent="#93C5FD", size=48)
        self.chip(540, 300, "out", T["hot"] - 0.2, s("break2") - 0.15, accent="#FB923C", size=44)
        self.badge("check", T["weave11"] + 0.1, s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: weave (break2, fix2), close up
    def draw_weave(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        vrect(c, 0, 0, W, H, ["#2E3A52", "#1A2238"])
        sw = prog(t, T["wet"] - 0.2, T["gaps"] + 0.2) if fixed else 0.0
        x0, y0, ww = 190, 420, 700
        weave(c, x0, y0, ww, ww, t, swell=sw)
        if not fixed:
            ak = prog(t, T["air"] - 0.3, T["air"])
            for k in range(4):                                   # air through the gaps
                xx = x0 + (k + 1.5) * ww / 7
                q = (t * 0.9 + k * 0.25) % 1.0
                arrow(c, xx, y0 - 60 + q * 160, xx, y0 + 40 + q * 160, "#7DD3FC", a=ak * (1 - q), w=8, head=20)
            rk = prog(t, T["rain2"] - 0.3, T["rain2"])
            for k in range(9):                                   # rain falling through
                xx = x0 + ((k * 2 + 1.5) % 7 + 0.5) * ww / 7
                q = (t * 1.4 + k * 0.13) % 1.0
                yy = lerp(y0 - 300, y0 + ww + 300, q)
                c.drawPath(path_of([(xx, yy - 18), (xx + 10, yy + 6), (xx, yy + 14), (xx - 10, yy + 6)], close=True),
                           P("#60A5FA", rk))
        else:
            gk = prog(t, T["goats"] - 0.3, T["goats"]) * (1 - prog(t, T["wet"], T["wet"] + 0.3))
            if gk > 0:
                goat(c, 540, 1100, 3.0, t, a=gk)
            rk = prog(t, T["wet"] - 0.3, T["wet"])
            for k in range(10):                                  # drops beading and running off down the slope
                xx = x0 + 60 + (k * 83) % (ww - 120)
                q = (t * 0.8 + k * 0.11) % 1.0
                if sw < 0.7:
                    yy = lerp(y0 - 200, y0 + ww + 200, q)
                    c.drawCircle(xx, yy, 12, P("#60A5FA", rk))
                else:
                    yy = lerp(y0 - 100, y0 + 40, min(q * 2, 1.0))
                    xr = xx + max(0.0, q * 2 - 1.0) * 400
                    c.drawCircle(xr, yy + max(0.0, q * 2 - 1.0) * 60, 15, P("#93C5FD", rk))
                    c.drawCircle(xr - 4, yy - 4 + max(0.0, q * 2 - 1.0) * 60, 5, P("#FFFFFF", 0.7 * rk))

    def ui_weave(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "air", T["air"] - 0.2, T["rain2"] - 0.2, accent="#7DD3FC", size=46)
            self.chip(540, 300, "rainin", T["rain2"] - 0.2, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["rain21"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["rain21"], 1.2)
            return
        self.chip(540, 300, "goat", T["goats"] - 0.2, T["wet"] - 0.1, accent="#FDE68A", size=48)
        self.chip(540, 300, "swells", T["wet"] - 0.1, T["gaps"] - 0.1, accent="#93C5FD", size=44)
        self.chip(540, 300, "closed", T["gaps"] - 0.1, s("break3") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["runs1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: wind (break3, fix3)
    def draw_wind(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        cam = (-120, -150, 1.55)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        vrect(c, 0, 0, W, H, [("#C9A673", 0.35), ("#A8693A", 0.2)])
        dunes(c, cam, t)
        self.view(c, cam)
        sand(c)
        if not fixed:
            sk = prog(t, T["wind"] - 0.3, T["face1"])
            tent(c, t, fire=0.4, curtain=1.0, duck=t > T["sand"])
            rng = random.Random(6)
            for k in range(110):                                 # sand blowing in from the left
                q = (t * (0.9 + rng.random()) + rng.random()) % 1.0
                xx = lerp(-900, 500, q)
                yy = rng.uniform(-220, -6) + math.sin(t * 5 + k) * 8
                c.drawLine(xx, yy, xx - 26, yy + 3, P("#7A4A22", 0.9 * sk, stroke=rng.uniform(4, 7)))
            wind_lines(c, -900, 600, -220, -40, t, a=sk, col="#8A5A2A", n=8, speed=900.0)
            c.drawRect(R(-1500, -400, 3000, 420), P("#C08A4A", 0.25 * sk))
        else:
            dk = prog(t, T["drop"] - 0.3, T["windy"] + 0.2)
            ok = prog(t, T["open"] - 0.3, T["open1"])
            tent(c, t, fire=0.6, curtain=1.0, wall_l=dk, wall_r=0.0)
            if dk > 0:                                           # the windy side closed with a long wall panel
                c.drawRect(R(-HALF - 6, -EAVE, 26, EAVE), P(HAIR[1], dk))
                c.save()
                c.clipPath(path_of([(-HALF, -EAVE), (-60, -EAVE), (-60, 0), (-HALF, 0)], close=True), doAntiAlias=True)
                c.drawRect(R(-HALF, -EAVE, 400, EAVE * dk), lin_paint(0, -EAVE, 0, 0, [HAIR[0], HAIR[2]]))
                for j in range(5):
                    c.drawLine(-HALF, -EAVE + j * 30, -60, -EAVE + j * 30, P("#4A3C30", 0.7 * dk, stroke=2))
                c.restore()
                rng = random.Random(6)
                for k in range(60):                              # sand stopped by the wall
                    q = (t * (0.9 + rng.random()) + rng.random()) % 1.0
                    xx = lerp(-1000, -HALF - 20, q)
                    yy = rng.uniform(-200, -10)
                    c.drawLine(xx, yy, xx - 22, yy + 3, P("#7A4A22", 0.8, stroke=5))
            if ok > 0:
                wind_lines(c, 300, 800, -120, -40, t, a=ok * 0.7, col="#E0F2FE", n=4, speed=300.0)
        self.ui["wall"] = self.to_screen(cam, -300, -80)
        self.ui["openside"] = self.to_screen(cam, 380, -80)
        c.restore()

    def ui_wind(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "sand", T["sand"] - 0.3, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["face1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["face1"], 1.2)
            return
        self.chip(540, 300, "walls", T["walls"] - 0.2, T["drop"] - 0.2, accent="#FDE68A", size=46)
        wx, wy = self.ui.get("wall", (300, 900))
        self.label(wx, wy, 300, 560, "drop", T["drop"] - 0.2, s("break4") - 0.2, accent="#FCA5A5", size=34)
        ox, oy = self.ui.get("openside", (800, 900))
        self.label(ox, oy, 760, 680, "open", T["open"] - 0.2, s("break4") - 0.2, accent=GOOD, size=34)
        self.badge("check", T["open1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: move (break4, fix4)
    def draw_move(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = (40, -170, 1.3)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        dunes(c, cam, t)
        self.view(c, cam)
        sand(c)
        if not fixed:
            wk = prog(t, T["family"] - 0.4, T["again1"] + 0.5)
            tent(c, t, a=1.0 - 0.3 * wk, fire=0.0, people=0.0)
            for k in range(7):                                   # the herd walking off to the right
                gx = -420 + k * 80 + wk * 420 + (k % 2) * 20
                goat(c, gx, 40 + (k % 3) * 16, 1.5, t, walk=1.0)
            person(c, -460 + wk * 420, 30, 150, "#F5F5F4", t, pose="walk", face=1, skin="#C68B59", hair="#1F2937")
            ak = prog(t, T["again"] - 0.3, T["again1"])
            if ak > 0:                                           # a loop arrow: again and again
                p_ = skia.Path()
                p_.addArc(R(-160, -560, 320, 220), 200, 280 * ak)
                c.drawPath(p_, P("#FDE68A", ak, stroke=10))
        else:
            pk = prog(t, s("fix4") - 0.1, T["strips"] + 0.3)        # the tent comes down
            if pk < 1:
                c.save()
                c.translate(0, 0)
                c.scale(1, 1 - pk * 0.92)
                tent(c, t, fire=0.0, people=0.0, a=1 - pk * 0.4)
                c.restore()
            bk = prog(t, T["strips"] - 0.2, T["camel1"])
            # the bundle: rolled strips, a pile of poles, coiled ropes, rising onto the camel
            cx_ = lerp(-120, 250, prog(t, T["ropes"], T["camel1"]))
            cy_ = lerp(-30, -236, prog(t, T["ropes"], T["camel1"]))
            camel(c, 240, 0, 0.5, 0.0, run=0.0, a=prog(t, T["poles"] - 0.4, T["poles"]))
            if bk > 0:
                for k in range(3):
                    c.drawRRect(rr(cx_ - 110 + k * 10, cy_ - 30 - k * 26, 220, 28, 14), P(HAIR[k % 3], bk))
                    c.drawLine(cx_ - 100 + k * 10, cy_ - 16 - k * 26, cx_ + 100 + k * 10, cy_ - 16 - k * 26,
                               P("#4A3C30", bk, stroke=2))
                for k in range(4):
                    c.drawLine(cx_ - 160, cy_ - 90 - k * 8, cx_ + 160, cy_ - 100 - k * 8, P("#6B4A2A", bk * prog(t, T["poles"] - 0.2, T["poles"]), stroke=8))
                rk = prog(t, T["ropes"] - 0.2, T["ropes"])
                for k in range(3):
                    c.drawCircle(cx_ + 130, cy_ - 40, 22 - k * 6, P("#C8B48A", rk, stroke=4))
        self.ui["load"] = self.to_screen(cam, 250, -260)
        c.restore()

    def ui_move(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "moves", T["herds"] - 0.2, s("fix4") - 0.15, accent="#FDE68A", size=48)
            self.badge("alert", T["again1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["again1"], 1.2)
            return
        self.chip(540, 300, "pack", T["strips"] - 0.2, T["camel"] - 0.2, accent="#FDE68A", size=44)
        self.chip(540, 300, "camel", T["camel"] - 0.2, s("cta") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["camel1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: loom (reveal)
    def draw_loom(self, c, t):
        T, s = self.T, self.tl.s
        split = t >= T["curtain"] - 0.3
        if not split:
            cam = (-40, -110, 1.45)
            gy = (0 - cam[1]) * cam[2] + H / 2
            v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
            dunes(c, cam, t)
            self.view(c, cam)
            sand(c)
            # the ground loom: two beams pegged in the sand, warp threads, a woven strip growing
            gk = prog(t, T["strip"] - 0.3, T["curtain"])
            c.drawRect(R(-330, -12, 14, 18), P("#6B4A2A"))
            c.drawRect(R(330, -12, 14, 18), P("#6B4A2A"))
            for k in range(9):
                yy = -8 + k * 3
                c.drawLine(-320, yy - 10, 330, yy - 10, P("#D6C3A0", 0.8, stroke=2))
            wx = lerp(-300, 60, gk)
            c.drawRect(R(-316, -30, wx + 316, 26), P(HAIR[1]))
            for k in range(int((wx + 316) / 18)):
                c.drawLine(-316 + k * 18, -30, -316 + k * 18, -4, P("#4A3C30", 0.8, stroke=2))
            sadu_band(c, -316, -40, max(1, wx + 316), 10)
            person(c, wx + 60, 0, 120, "#7C2D12", t, pose="sit", face=-1, skin="#C68B59", hair="#111827")
            c.drawLine(wx + 30, -52, wx + 4, -24, P("#9A6A3A", 1.0, stroke=6))    # the beater
            c.restore()
        else:
            cam = (0, -150, 1.6)
            gy = (0 - cam[1]) * cam[2] + H / 2
            v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
            dunes(c, cam, t)
            self.view(c, cam)
            sand(c)
            tent(c, t, fire=1.0, curtain=prog(t, T["curtain"] - 0.3, T["curtain"] + 0.2))
            self.ui["guests"] = self.to_screen(cam, -230, -110)
            self.ui["family"] = self.to_screen(cam, 260, -110)
            c.restore()

    def ui_loom(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "loom", T["women"] - 0.1, T["curtain"] - 0.3, accent="#FDE68A", size=48)
        if tw >= T["curtain"] - 0.3:
            gx, gy = self.ui.get("guests", (300, 900))
            fx_, fy = self.ui.get("family", (800, 900))
            self.chip(gx, gy - 200, "guests", T["splits"] - 0.2, s("stat") - 0.15, accent="#FDBA74", size=44)
            self.chip(fx_, fy - 200, "family", T["splits"], s("stat") - 0.15, accent="#93C5FD", size=44)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        cam = (100, -170, 0.75)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=STORM, horizon_y=gy)
        dunes(c, cam, t)
        self.view(c, cam)
        sand(c)
        tent(c, t, fire=1.0, wet=1.0)
        c.restore()
        rain(c, t, a=0.8)
        fk = prog(t, T["t_flip"] - 0.2, T["t_flip"] + 0.25)
        wind_lines(c, 0, W, 900, 1200, t, a=prog(t, T["t_umb"], T["t_flip"]), col="#E0F2FE", n=6, speed=900.0)
        person(c, 760, 1250, 420, "#16A34A", t, pose="point", face=1, hair="#1F2937")
        umbrella(c, 790 + 40 * fk, 830 - 20 * fk, 1.6, flip=fk)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "flip", T["t_umb"] - 0.2, self.duration + 1, accent=HILITE, size=50)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1E3A6E", "#3E6AA8", "#E39A6A"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, rain_snd(max(1.5, T["breeze"] + 0.3), 61), -14), (T["goat"], sfx.pop(62), -10),
              (T["breeze"], sfx.whoosh(0.8, True, 63), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["bedouin"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["sun"], sfx.sizzle(0.8, 67), -14),
               (T["oven1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["shade"], sfx.whoosh(0.6, False, 69), -14),
               (T["weave11"], sfx.ding(), -8), (T["weave11"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 70), -4), (T["air"], sfx.whoosh(0.5, True, 71), -12),
               (T["rain21"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["goats"], sfx.pop(73), -8),
               (T["swells"], sfx.charge_up(0.6), -14), (T["runs1"], sfx.ding(), -8), (T["runs1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["wind"], sfx.hiss(1.4, 75), -10),
               (T["face1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["drop"], sfx.thud(0.4, 77), -8),
               (T["open"], sfx.whoosh(0.5, False, 78), -12), (T["open1"], sfx.ding(), -8), (T["open1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["herds"], sfx.pop(80), -10),
               (T["again1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 81), -4), (T["strips"], sfx.thunk(82), -8),
               (T["poles"], sfx.clank(500.0, 0.3, 83), -10), (T["camel1"], sfx.ding(), -8), (T["camel1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(84), 0), (T["follow"] - 0.15, sfx.pop(85), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 86), -6), (T["strip"], sfx.tap(87), -10),
               (T["splits"], sfx.whoosh(0.4, True, 88), -12)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 89), -6), (T["s1"], sfx.pop(90), -3), (T["s2"], sfx.pop(91), -3),
               (T["s3"], sfx.pop(92), -3)]
        ev += [(T["cong2"], sfx.pop(93), -2), (T["cong2"], sfx.sparkle(1.4, 18, 94), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 95), -6), (T["t_flip"], sfx.snap(96), -6)]
        return ev


NAME = "tent"
EPISODE = Tent
