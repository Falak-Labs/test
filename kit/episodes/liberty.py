"""Episode 59 - The Statue of Liberty.  v2 look: New York harbour in a storm, at golden hour and at night; the statue as
she was when new, shiny brown copper, turning green for the reveal.

Sets: harbor (hook: from her copper face in a storm with lightning out to the whole statue on its pedestal, a two-coin
inset for the skin; reveal: the sea air paints her green over about thirty years; stat; closer at night with the torch
lit), frame (break1: the thin skin alone crumples like foil; fix1: x-ray, Eiffel's iron tower inside carries her, a tiny
Eiffel Tower for "the tower guy"), skin (break2: a copper panel bolted tight to its bar tears in wind and summer heat;
fix2: thin iron bars follow her shape and loose clips let the skin slide and sway), battery (break3: copper touching iron
in salty air makes a battery and the iron rusts away; fix3: varnished cloth between them, then steel bars a century
later), paris (break4: she stands over the rooftops of Paris with an ocean to cross; fix4: taken apart into 350 pieces,
packed in crates and shipped), tag (EN: a cheap ring turns a finger green, "REFUND!"; AR: arguing at the shop).
World (harbor): front view, the island at y = 0; foundation, pedestal, then the statue's feet at FEET_Y (about 6.5 units a
metre: the torch about 605 units up).
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, sun, thermo, heat_lines  # noqa: E402
from burjalarab import path_of, sea_band, saudi_man  # noqa: E402
from eiffel import eiffel, rooftops  # noqa: E402
from fridge import ship  # noqa: E402
from phone import bubble  # noqa: E402

STORMP = {"top": "#0A0F1E", "upper": "#1A2238", "mid": "#2E3A52", "low": "#4A5468", "horizon": "#6A7284",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2A2A60", "horizon": "#4A3A7A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
COPPER = ("#C8733A", "#A35A2C", "#E8A070")                # base, shade, highlight (new, like a shiny coin)
VERD = ("#5FA58E", "#3F7A68", "#9AD3BF")                  # the green patina
FEET_Y = -305.0
IRONC = "#3A3F4A"


def skin_cols(g):
    return tuple(mix(a, b, g) for a, b in zip(COPPER, VERD))


def statue(c, x, y, s, t, green=0.0, xray=0.0, crumple=0.0, sway=0.0, lit=0.0, steel=0.0, a=1.0, glint=0.0):
    """The statue standing on (x, y) (her feet), front view, 300 units tall at s = 1.  green 0..1 copper -> patina;
    xray 0..1 fades the skin and shows the iron tower and the thin bars; crumple 0..1 the skin collapsing like foil;
    sway (degrees) leans her from the feet; lit 0..1 the torch at night; steel 0..1 bars turn to shiny steel."""
    if a <= 0:
        return
    base, dark, hi = skin_cols(green)
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if sway:
        c.rotate(sway)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    sk_a = 1.0 - 0.72 * xray
    if crumple > 0:                                                # the skin sagging and wrinkling
        c.save()
        c.scale(1.0 + 0.25 * crumple, 1.0 - 0.55 * crumple)
    robe = path_of([(-38, 0), (38, 0), (37, -70), (34, -140), (31, -188), (22, -208), (9, -216), (-9, -216), (-22, -208),
                    (-31, -188), (-34, -140), (-37, -70)], close=True)
    c.drawPath(robe, lin_paint(-38, 0, 38, 0, [dark, base, hi, base, dark], [0, 0.25, 0.45, 0.7, 1], a=sk_a))
    for k in range(7):                                             # the folds of the robe
        fx_ = -28 + k * 9
        fp = skia.Path()
        fp.moveTo(fx_, -6)
        fp.cubicTo(fx_ + 4, -60, fx_ - 3, -120, fx_ + 2 * (k - 3), -180)
        c.drawPath(fp, P(dark, 0.55 * sk_a, stroke=2.2))
    sash = path_of([(-30, -170), (30, -130), (30, -118), (-30, -158)], close=True)
    c.drawPath(sash, P(hi, 0.35 * sk_a))
    if crumple > 0:
        rng = random.Random(3)
        for _ in range(int(30 * crumple)):
            x0_, y0_ = rng.uniform(-34, 34), rng.uniform(-200, -10)
            c.drawLine(x0_, y0_, x0_ + rng.uniform(-14, 14), y0_ + rng.uniform(-14, 14), P(dark, crumple, stroke=2))
    # the left arm holding the tablet (viewer's right)
    c.drawLine(22, -205, 34, -180, P(base, sk_a, stroke=10))
    c.save()
    c.translate(32, -160)
    c.rotate(-12)
    c.drawRRect(rr(-10, -24, 20, 48, 3), P(mix(base, dark, 0.3), sk_a))
    c.drawRRect(rr(-10, -24, 20, 48, 3), P(dark, sk_a, stroke=1.6))
    c.restore()
    # the raised arm with the torch (viewer's left)
    c.drawLine(-22, -204, -34, -272, P(base, sk_a, stroke=12))
    c.drawLine(-22, -204, -34, -272, P(hi, 0.35 * sk_a, stroke=4))
    c.drawRect(R(-38, -284, 8, 12), P(dark, sk_a))
    cup = path_of([(-44, -292), (-24, -292), (-28, -284), (-40, -284)], close=True)
    c.drawPath(cup, P(mix(base, "#D4A537", 0.5 * (1 - green)), sk_a))
    flame = skia.Path()
    flame.moveTo(-42, -292)
    flame.cubicTo(-46, -298, -38, -304, -34, -308)
    flame.cubicTo(-30, -302, -24, -298, -26, -292)
    flame.close()
    c.drawPath(flame, P("#F5C542" if green > 0.5 else mix(base, "#F5C542", 0.6), sk_a))
    if lit > 0:
        add_glow(c, -34, -300, 40, "#FFD27A", 0.8 * lit)
    # neck, head and crown
    c.drawRect(R(-6, -228, 12, 14), P(base, sk_a))
    c.drawCircle(0, -236, 11, P(base, sk_a))
    c.drawCircle(-3, -239, 5, P(hi, 0.4 * sk_a))
    for k in range(7):
        q = math.radians(-160 + k * 23.3)
        x0_, y0_ = math.cos(q) * 11, -238 + math.sin(q) * 11
        x1_, y1_ = math.cos(q) * 30, -238 + math.sin(q) * 30
        sp = path_of([(x0_ - math.sin(q) * 2.6, y0_ + math.cos(q) * 2.6), (x1_, y1_),
                      (x0_ + math.sin(q) * 2.6, y0_ - math.cos(q) * 2.6)], close=True)
        c.drawPath(sp, P(base, sk_a))
    c.drawRect(R(-13, -246, 26, 6), P(dark, sk_a))
    if glint > 0:                                                  # a shine sweeping over the new copper
        gx = lerp(-60, 60, glint)
        c.save()
        c.clipPath(robe)
        c.drawRect(R(gx - 8, -230, 16, 240), P("#FFFFFF", 0.35 * math.sin(glint * math.pi)))
        c.restore()
    if crumple > 0:
        c.restore()
    if xray > 0:                                                   # the iron inside
        ironc = mix(IRONC, "#D1D5DB", steel)
        for k in range(10):                                        # the central tower (pylon)
            y0_, y1_ = -k * 20, -(k + 1) * 20
            w0, w1 = lerp(16, 9, k / 10.0), lerp(16, 9, (k + 1) / 10.0)
            c.drawLine(-w0, y0_, w1, y1_, P(ironc, xray, stroke=2.4))
            c.drawLine(w0, y0_, -w1, y1_, P(ironc, xray, stroke=2.4))
        for sd in (-1, 1):
            c.drawLine(sd * 16, 0, sd * 9, -200, P(ironc, xray, stroke=4))
        c.drawLine(-9, -196, -33, -268, P(ironc, xray, stroke=3.4))     # the truss up the raised arm
        c.drawLine(-15, -190, -38, -262, P(ironc, xray, stroke=2.4))
        bars = mix("#6B4F3A", "#E5E7EB", steel)
        for k in range(1, 11):                                     # the thin bars following her shape
            yy = -k * 19
            wd = lerp(37, 30, k / 11.0)
            bp = skia.Path()
            bp.moveTo(-wd, yy)
            bp.quadTo(0, yy - 6, wd, yy)
            c.drawPath(bp, P(bars, xray, stroke=1.8))
            c.drawLine(-wd + 2, yy, -10, yy - 3, P(ironc, 0.7 * xray, stroke=1.2))
            c.drawLine(wd - 2, yy, 10, yy - 3, P(ironc, 0.7 * xray, stroke=1.2))
        c.drawPath(robe, P(bars, 0.8 * xray, stroke=2))
    if a < 1:
        c.restore()
    c.restore()


def pedestal(c, t, night=0.0, a=1.0):
    """The star-shaped fort, the granite foundation and the pedestal (world space, island at y = 0)."""
    stone = mix("#B9B2A4", "#3A3D52", night)
    stone_d = mix("#8E8676", "#262A3E", night)
    star = path_of([(-300, 0), (-260, -40), (-150, -50), (-120, -90), (120, -90), (150, -50), (260, -40), (300, 0)], close=True)
    c.drawPath(star, P(mix("#9A9282", "#2E3246", night), a))
    c.drawPath(path_of([(-110, -90), (110, -90), (100, -130), (-100, -130)], close=True), P(stone_d, a))
    c.drawPath(path_of([(-76, -130), (76, -130), (64, -290), (-64, -290)], close=True),
               lin_paint(-76, 0, 76, 0, [stone_d, stone, stone_d], a=a))
    c.drawRect(R(-80, -134, 160, 10), P(stone, a))
    c.drawRect(R(-72, -250, 144, 12), P(stone, a))                  # the balcony band
    for k in range(4):
        c.drawRect(R(-54 + k * 30, -246, 14, 26), P(stone_d, a))
    c.drawRect(R(-70, -298, 140, 10), P(stone, a))
    c.drawRect(R(-58, -305, 116, 8), P(stone_d, a))
    if night > 0:
        add_glow(c, 0, -200, 160, "#FFE3A3", 0.25 * night * a)


def coin(c, x, y, r, a=1.0, edge=False):
    if edge:
        c.drawRRect(rr(x - r, y - 7, 2 * r, 14, 4), P("#C08A4A", a))
        c.drawRRect(rr(x - r, y - 7, 2 * r, 14, 4), P("#7A5220", a, stroke=2))
        return
    c.drawCircle(x, y, r, P("#C88A4A", a))
    c.drawCircle(x, y, r * 0.8, P("#7A5220", a, stroke=2))


def crate(c, x, y, w, h, a=1.0, lid=0.0):
    c.drawRect(R(x - w / 2, y - h, w, h), P("#B08350", a))
    for k in range(3):
        c.drawLine(x - w / 2, y - h + (k + 0.5) * h / 3, x + w / 2, y - h + (k + 0.5) * h / 3, P("#8A6238", a, stroke=3))
    c.drawLine(x - w / 2, y - h, x + w / 2, y, P("#8A6238", a, stroke=3))
    c.drawRect(R(x - w / 2, y - h - 6 * lid, w, 6), P("#9A7040", a))


def rain(c, t, a=1.0, seed=5):
    if a <= 0:
        return
    rng = random.Random(seed)
    for _ in range(110):
        x0_ = rng.uniform(-200, W + 200)
        sp = rng.uniform(1400, 2000)
        y0_ = (rng.uniform(0, H) + t * sp) % (H + 200) - 100
        c.drawLine(x0_, y0_, x0_ - 26, y0_ + 60, P("#BFD3EA", 0.35 * a, stroke=2))


def lightning(c, x, y, len_, t, seed, a=1.0):
    if a <= 0:
        return
    rng = random.Random(seed)
    pts = [(x, y)]
    for k in range(9):
        x, y = x + rng.uniform(-40, 40), y + len_ / 9
        pts.append((x, y))
    c.drawPath(path_of(pts), P("#F5F3FF", a, stroke=6))
    add_glow(c, pts[3][0], pts[3][1], 200, "#C7D2FE", 0.5 * a)


# ====================================================================================== the episode
class Liberty(EpisodeV2):
    BUILD_NO = 59
    FIRST_SET = "harbor"
    CLEAR = "#0A0F1E"
    TITLE = {"en": "STATUE OF LIBERTY", "ar_sa": "تمثال الحرية"}
    EMPH = {"en": ["CONGRATS", "COPPER", "GIANT", "HARBOR", "STORMS", "SKIN", "THIN", "TWO", "COINS", "STATUE",
                   "LIBERTY", "YOURSELF", "SHAPE", "CRUMPLE", "FOIL", "GUSTAVE", "EIFFEL", "TOWER", "IRON", "INSIDE",
                   "BOLT", "TIGHT", "WIND", "SUMMER", "HEAT", "RIP", "BARS", "LOOSE", "CLIPS", "SLIDE", "SWAY", "SALTY",
                   "BATTERY", "RUSTS", "APART", "VARNISHED", "CLOTH", "CENTURY", "STEEL", "PARIS", "OCEAN", "FIRST",
                   "THREE", "HUNDRED", "FIFTY", "PIECES", "SHIP", "FOLLOW", "MICROWAVE", "OVEN", "PAINT", "THIRTY",
                   "YEARS", "BROWN", "GREEN", "PROTECTS", "FORTY-SIX", "NINETY-THREE", "PEDESTAL", "TORCH", "SWAYS",
                   "THIRTEEN", "CENTIMETERS", "WORLD", "LOVES", "RING", "FINGER", "REFUND"],
            "ar_sa": ["مبروك", "عملاقة", "نحاس", "عواصف", "البحر", "وجلدها", "رقيق", "عملتين", "تمثال", "الحرية", "بيدك",
                      "بهالرقة", "شكله", "بينطوي", "القصدير", "غوستاف", "إيفل", "البرج", "حديد", "داخل", "ثبّت", "الريح",
                      "الصيف", "بيشقّونه", "أسياخ", "رفيعة", "بمشابك", "مرتخية", "يتحرك", "لمس", "بطارية", "يصدّي",
                      "قماش", "ورنيش", "مية", "سنة", "ستيل", "باريس", "المحيط", "تفكّه", "ثلاثمية", "قطعة", "وتشحنه",
                      "تابعني", "مايكرويف", "يصبغها", "ثلاثين", "أخضر", "يحميه", "وأربعين", "وتسعين", "القاعدة",
                      "شعلتها", "تتمايل", "ثلاثطعش", "سانتي", "العالم", "خاتمك", "صبعك", "تهاوش", "المحل"]}
    KEYS = {"ar_sa": {
        ("hook", "COPPER"): "نحاس", ("hook", "GIANT"): "عملاقة", ("hook", "STORMS"): "عواصف", ("hook", "SKIN"): "وجلدها",
        ("hook", "COINS"): "عملتين", ("hook", "CONGRATS"): "مبروك", ("hook", "LIBERTY"): "الحرية",
        ("break1", "THIN"): "بهالرقة", ("break1", "SHAPE"): "شكله", ("break1", "CRUMPLE"): "بينطوي", ("break1", "FOIL"): "القصدير",
        ("fix1", "GUSTAVE"): "غوستاف", ("fix1", "TOWER"): "البرج", ("fix1", "IRON"): "حديد", ("fix1", "INSIDE"): "داخل",
        ("break2", "BOLT"): "ثبّت", ("break2", "WIND"): "الريح", ("break2", "HEAT"): "الصيف", ("break2", "RIP"): "بيشقّونه",
        ("fix2", "BARS"): "أسياخ", ("fix2", "CLIPS"): "بمشابك", ("fix2", "SLIDE"): "يتحرك", ("fix2", "SWAY"): "براحته",
        ("break3", "SALTY"): "البحر", ("break3", "TOUCHING"): "لمس", ("break3", "BATTERY"): "بطارية",
        ("break3", "RUSTS"): "يصدّي",
        ("fix3", "APART"): "بينهم", ("fix3", "CLOTH"): "قماش", ("fix3", "CENTURY"): "مية", ("fix3", "STEEL"): "ستيل",
        ("break4", "PARIS"): "باريس", ("break4", "OCEAN"): "المحيط",
        ("fix4", "STAND"): "فتوقّفه", ("fix4", "APART"): "تفكّه", ("fix4", "PIECES"): "قطعة", ("fix4", "SHIP"): "وتشحنه",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PAINT"): "يصبغها", ("reveal", "THIRTY"): "ثلاثين", ("reveal", "GREEN"): "أخضر",
        ("reveal", "PROTECTS"): "يحميه",
        ("stat", "FORTY-SIX"): "ستة", ("stat", "NINETY-THREE"): "ثلاثة", ("stat", "TORCH"): "شعلتها",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "COPPER"): "النحاس", ("tag", "WORLD"): "العالم", ("tag", "RING"): "خاتمك", ("tag", "REFUND"): "تهاوش"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a microwave oven"),
                   "stat": [("46 m", "TALL"), ("93 m", "WITH PEDESTAL"), ("13 cm", "TORCH SWAY")],
                   "L": {"copper": "A COPPER GIANT", "storm": "HARBOR STORMS", "coins": "SKIN: 2.4 mm = 2 COINS",
                         "name": "THE STATUE OF LIBERTY", "thin": "TOO THIN TO HOLD ITS SHAPE", "foil": "CRUMPLES LIKE FOIL",
                         "eiffel": "GUSTAVE EIFFEL, THE TOWER GUY", "tower": "AN IRON TOWER INSIDE",
                         "bolt": "BOLTED TIGHT", "rip": "WIND + HEAT = RIP", "bars": "THIN IRON BARS",
                         "clips": "LOOSE CLIPS: FREE TO SLIDE", "battery": "COPPER + IRON + SALT = BATTERY",
                         "rust": "THE IRON RUSTS AWAY", "cloth": "VARNISHED CLOTH BETWEEN", "steel": "100 YEARS LATER: STEEL",
                         "paris": "BUILT IN PARIS", "ocean": "AN OCEAN TO CROSS", "pieces": "350 PIECES",
                         "ship": "SHIPPED IN CRATES", "paint": "THE SEA AIR PAINTS HER", "years": "ABOUT 30 YEARS",
                         "protect": "THE GREEN PROTECTS IT", "loves": "THE WORLD LOVES IT", "refund": "REFUND!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مايكرويف"),
                      "stat": [("46", "متر طول"), ("93", "متر مع القاعدة"), ("13", "سانتي تتمايل الشعلة")],
                      "L": {"copper": "عملاقة نحاس", "storm": "عواصف البحر", "coins": "جلدها مثل عملتين فوق بعض",
                            "name": "تمثال الحرية", "thin": "ما يقدر يشيل شكله", "foil": "بينطوي مثل ورق القصدير",
                            "eiffel": "غوستاف إيفل، صاحب البرج", "tower": "برج حديد من داخل",
                            "bolt": "مثبّت بقوة", "rip": "الريح والحر بيشقّونه", "bars": "أسياخ رفيعة على شكلها",
                            "clips": "مشابك مرتخية: يتحرك براحته", "battery": "نحاس + حديد + ملح = بطارية",
                            "rust": "الحديد يصدّي", "cloth": "قماش مشرّب ورنيش", "steel": "بعد مية سنة: ستيل",
                            "paris": "انصنع في باريس", "ocean": "لازم يقطع المحيط", "pieces": "ثلاثمية وخمسين قطعة",
                            "ship": "انشحن بالبحر", "paint": "هوا البحر يصبغها", "years": "ثلاثين سنة تقريبًا",
                            "protect": "الأخضر يحميه", "loves": "حبّها العالم", "refund": "تهاوش صاحب المحل",
                            "bubble": "وش هالغش؟!"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "copper": ("hook", "COPPER", 0.15), "giant": ("hook", "GIANT", 0.22), "storms": ("hook", "STORMS", 0.35),
            "skin": ("hook", "SKIN", 0.45), "coins": ("hook", "COINS", 0.6), "congrats": ("hook", "CONGRATS", 0.68),
            "liberty": ("hook", "LIBERTY", 0.92),
            "thin": ("break1", "THIN", 0.15), "shape": ("break1", "SHAPE", 0.45), "crumple": ("break1", "CRUMPLE", 0.7),
            "foil": ("break1", "FOIL", 0.9),
            "gustave": ("fix1", "GUSTAVE", 0.1), "towerw": ("fix1", "TOWER", 0.4), "iron": ("fix1", "IRON", 0.7),
            "inside": ("fix1", "INSIDE", 0.9),
            "bolt": ("break2", "BOLT", 0.1), "wind": ("break2", "WIND", 0.5), "heat": ("break2", "HEAT", 0.7),
            "rip": ("break2", "RIP", 0.9),
            "bars": ("fix2", "BARS", 0.15), "clips": ("fix2", "CLIPS", 0.55), "slide": ("fix2", "SLIDE", 0.8),
            "swayw": ("fix2", "SWAY", 0.92),
            "salty": ("break3", "SALTY", 0.2), "touching": ("break3", "TOUCHING", 0.4), "battery": ("break3", "BATTERY", 0.65),
            "rusts": ("break3", "RUSTS", 0.9),
            "apart": ("fix3", "APART", 0.15), "cloth": ("fix3", "CLOTH", 0.35), "century": ("fix3", "CENTURY", 0.6),
            "steel": ("fix3", "STEEL", 0.75),
            "paris": ("break4", "PARIS", 0.3), "ocean": ("break4", "OCEAN", 0.9),
            "stand": ("fix4", "STAND", 0.05), "apart4": ("fix4", "APART", 0.4), "pieces": ("fix4", "PIECES", 0.7),
            "ship": ("fix4", "SHIP", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "paint": ("reveal", "PAINT", 0.2), "thirty": ("reveal", "THIRTY", 0.35), "green": ("reveal", "GREEN", 0.7),
            "protects": ("reveal", "PROTECTS", 0.9),
            "s1": ("stat", "FORTY-SIX", 0.05), "s2": ("stat", "NINETY-THREE", 0.35), "s3": ("stat", "TORCH", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_copper": ("tag", "COPPER", 0.05), "t_world": ("tag", "WORLD", 0.3), "t_ring": ("tag", "RING", 0.55),
            "t_refund": ("tag", "REFUND", 0.9)})
        T["foil1"] = max(T["foil"], T["crumple"]) + 0.1
        T["rip1"] = max(T["rip"], T["heat"]) + 0.1
        T["rust1"] = max(T["rusts"], T["battery"]) + 0.1
        T["ocean1"] = max(T["ocean"], T["paris"]) + 0.1
        T["inside1"] = max(T["inside"], T["iron"]) + 0.2
        T["sway1"] = max(T["swayw"], T["slide"]) + 0.2
        T["steel1"] = max(T["steel"], T["century"]) + 0.2
        T["ship1"] = max(T["ship"], T["pieces"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "frame", 1)
        self.cut(s("break2") - 0.12, "skin", -1)
        self.cut(s("break3") - 0.12, "battery", 1)
        self.cut(s("break4") - 0.12, "paris", -1)
        self.cut(s("reveal") - 0.12, "harbor", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- harbor camera: from her face in the storm out to the whole statue (ground near y 1230)
        cm = Camera(-6, -545, 4.0)
        cm.key(0.05, -6, -548, 3.9, 0.3)
        cm.key(max(0.4, T["giant"] - 0.2), 0, -270, 1.3, max(1.2, T["storms"] - T["giant"] + 0.6))
        cm.key(T["congrats"], 0, -265, 1.34, 1.4)
        cm.key(s("reveal") - 0.12, -10, -520, 2.4, 0.0).key(T["thirty"], 0, -330, 1.45, max(1.0, T["protects"] - T["thirty"]))
        cm.key(s("stat") - 0.12, 0, -330, 1.12, 0.0).key(s("stat"), 0, -332, 1.13, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -420, 1.62, 1.0).key(s("closer") + 0.9, 0, -425, 1.7, 3.0)
        self.cam = cm
        self.spans = [(T["foil1"], T["inside1"] + 0.3), (T["rip1"], T["sway1"] + 0.3), (T["rust1"], T["steel1"] + 0.3),
                      (T["ocean1"], T["ship1"] + 0.3)]
        self.shakes = [(T["storms"], 0.4, 8), (T["congrats"], 0.35, 8), (T["foil1"], 0.5, 9), (T["rip1"], 0.4, 8),
                       (T["rust1"], 0.3, 6), (T["ocean1"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["t_refund"], 0.3, 7)]

    # ------------------------------------------------------------------ set: harbor (hook, reveal, stat, closer)
    def draw_harbor(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        hook = t < s("break1")
        night = prog(t, s("closer") - 0.6, s("closer") + 0.6)
        storm = 1.0 - prog(t, T["congrats"] - 0.2, T["congrats"] + 0.8) if hook else 0.0
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy - 30 * z)
        if storm > 0:
            c.save()
            c.saveLayerAlpha(None, int(255 * storm))
            v2.sky(c, W, H, 0.0, pal=STORMP, horizon_y=gy - 30 * z)
            c.restore()
            c.restore()
        if night > 0:
            c.save()
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy - 30 * z)
            v2.stars(c, W, H, t, 0.8)
            c.restore()
            c.restore()
        if storm < 1 and night < 1:
            sun(c, 860 - cx * 0.05, gy - 380 * z, 46, heat=0.4, a=(1 - storm) * (1 - night))
        for i, (px, py, s_) in enumerate(((180, 820, 1.1), (760, 1020, 0.9), (460, 1240, 0.8))):
            v2.cloud(c, (px + t * (8 + i * 4)) % (W + 600) - 300, gy - py * z, s_,
                     body=mix(mix("#7A6A9A", "#2A3042", storm), "#1A1E48", night),
                     rim=mix(mix("#FFB37A", "#5A6478", storm), "#3A3A78", night), a=0.8, seed=i)
        if storm > 0:
            fl = prog(t, T["storms"] - 0.05, T["storms"] + 0.05) * (1 - prog(t, T["storms"] + 0.15, T["storms"] + 0.5))
            lightning(c, 820, gy - 1500 * z, 1000 * z, t, 7, a=fl * storm)
            if fl > 0:
                c.drawRect(R(0, 0, W, H), P("#E0E7FF", 0.25 * fl * storm))
        c.save()                                                   # the far city across the water
        c.translate(W / 2 - cx * z * 0.3, gy - 4 * z)
        c.scale(z * 0.32, z * 0.32)
        skyline_night(c, -2600, 2600, 0, seed=8, hmin=90, hmax=420,
                      cols=(mix("#3A4A6A", "#1A1F45", night), mix("#4A5A7A", "#242A5C", night), mix("#2A3A5A", "#15193A", night)),
                      lit=0.2 + 0.5 * night, t=t)
        c.restore()
        self.view(c, cam)
        sea_band(c, -1800, 1800, -4, 900, t, col=mix(mix("#2A6A8A", "#2A3A4A", storm), "#0E1E3A", night),
                 dark=mix(mix("#0B3A5A", "#141E2A", storm), "#060A1A", night))
        c.drawRect(R(-420, -8, 840, 26), P(mix("#5A7A4A", "#1A2A30", night)))            # the island
        pedestal(c, t, night)
        if hook:
            green = 0.0
        elif t < s("stat") - 0.12:
            green = e_io(prog(t, T["thirty"] - 0.2, T["green"] + 0.3))
        else:
            green = 1.0
        glint = prog(t, T["copper"] - 0.1, T["copper"] + 0.9) if hook else 0.0
        sway = math.sin(t * 2.4) * 0.6 * storm
        statue(c, 0, FEET_Y, 1.0, t, green=green, lit=night, sway=sway, glint=glint)
        if not hook and s("reveal") - 0.12 <= t < s("stat") - 0.12:  # the salty breeze painting her
            pk = prog(t, T["paint"] - 0.3, T["green"] + 0.4)
            for k in range(8):
                q = (t * 0.5 + k / 8.0) % 1.0
                v2.puff(c, lerp(-300, 300, q), FEET_Y - 40 - k * 28, 26, "#B9E4D8", 0.25 * pk * math.sin(q * math.pi), k=k)
        c.restore()
        if storm > 0:
            rain(c, t, storm)
        self.ui["cam"] = cam

    def ui_harbor(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "copper", T["copper"] - 0.1, T["storms"] - 0.1, accent="#FDBA74", size=46)
            self.chip(540, 300, "storm", T["storms"] - 0.1, T["skin"] - 0.15, accent="#93C5FD", size=46)
            self.chip(540, 300, "coins", T["skin"] - 0.15, T["liberty"] - 0.25, accent=HILITE, size=40)
            self.chip(540, 300, "name", T["liberty"] - 0.25, s("break1") + 0.1, accent=HILITE, size=46)
            ck = self.span(T["coins"] - 0.4, T["liberty"] - 0.25)
            if ck > 0:                                             # two coins next to a sliver of skin
                c.drawRRect(rr(640, 560, 400, 180, 26), P("#0B1426", 0.85 * ck))
                coin(c, 750, 640, 60, ck, edge=True)
                coin(c, 750, 656, 60, ck, edge=True)
                c.drawRRect(rr(900, 634, 100, 28, 6), P(COPPER[0], ck))
                text(c, "=", 850, 670, 54, "#FFFFFF", "Poppins-Black", a=ck, align="center")
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            self.chip(540, 300, "paint", T["paint"] - 0.15, T["thirty"] - 0.1, accent="#9AD3BF", size=46)
            self.chip(540, 300, "years", T["thirty"] - 0.1, T["protects"] - 0.2, accent="#FDBA74", size=46)
            self.chip(540, 300, "protect", T["protects"] - 0.2, s("stat") - 0.15, accent=GOOD, size=46)

    # ------------------------------------------------------------------ set: frame (break1, fix1)
    def draw_frame(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1180)
        cam = (0, -440, 2.05)
        self.view(c, cam)
        c.drawRect(R(-600, -305, 1200, 900), P("#6B6458"))          # the top of the pedestal
        if not fixed:
            cr = e_in(prog(t, T["shape"] - 0.2, T["foil1"] + 0.3))
            statue(c, 0, FEET_Y, 1.0, t, crumple=cr)
        else:
            xk = prog(t, s("fix1") - 0.1, T["towerw"])
            ik = prog(t, T["iron"] - 0.3, T["iron"] + 0.2)
            statue(c, 0, FEET_Y, 1.0, t, xray=max(0.15, xk))
            if ik > 0:
                for k in range(3):
                    q = (t * 0.7 + k / 3.0) % 1.0
                    arrow(c, -60, FEET_Y - 200 + q * 160, -60, FEET_Y - 160 + q * 160, HILITE, a=ik * math.sin(q * math.pi), w=6, head=14)
        c.restore()
        if fixed:                                                  # the tower guy, with his tower
            ek = prog(t, T["gustave"] - 0.2, T["gustave"] + 0.2) * (1 - prog(t, T["inside1"] + 0.3, T["inside1"] + 0.7))
            if ek > 0:
                c.drawRRect(rr(730, 760, 300, 420, 30), P("#0B1A3A", 0.85 * ek))
                c.save()
                c.translate(880, 1140)
                c.scale(0.45, 0.45)
                eiffel(c, 0, 0, 1.0, t, a=ek)
                c.restore()

    def ui_frame(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "thin", T["thin"] - 0.2, T["crumple"] - 0.15, accent="#FDBA74", size=40)
            self.chip(540, 300, "foil", T["crumple"] - 0.15, s("fix1") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["foil1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["foil1"], 1.2)
            return
        self.chip(540, 300, "eiffel", T["gustave"] - 0.2, T["iron"] - 0.2, accent="#D6A77A", size=38)
        self.chip(540, 300, "tower", T["iron"] - 0.2, s("break2") - 0.15, accent=HILITE, size=44)
        self.badge("check", T["inside1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: skin (break2, fix2), a panel close up
    def draw_skin(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        vrect(c, 0, 0, W, H, ["#1E3A6E", "#3E6AA8", "#E39A6A"])
        if not fixed:
            wk = prog(t, T["wind"] - 0.3, T["wind"])
            hk = prog(t, T["heat"] - 0.3, T["heat"])
            rk = prog(t, T["rip1"] - 0.1, T["rip1"] + 0.3)
            c.drawRect(R(220, 440, 70, 760), P(IRONC))                 # the bar
            for k in range(5):                                     # the panel bolted tight
                py = 480 + k * 140
                c.drawRRect(rr(290, py, 520, 130, 14), P(COPPER[0]))
                c.drawRRect(rr(290, py, 520, 130, 14), P(COPPER[1], 1.0, stroke=4))
                for j in range(3):
                    c.drawCircle(255, py + 25 + j * 40, 10, P("#9CA3AF"))
                if rk > 0:
                    cp = path_of([(560 + 30 * math.sin(k), py + 10), (590, py + 50), (560, py + 80), (600, py + 125)])
                    c.drawPath(cp, P("#1A0A04", rk, stroke=8))
            for k in range(7):                                     # wind
                q = (t * 1.1 + k / 7.0) % 1.0
                arrow(c, lerp(1100, 860, q), 500 + k * 100, lerp(1000, 760, q), 500 + k * 100, "#E0F2FE",
                      a=wk * math.sin(q * math.pi), w=10, head=24)
            sun(c, 900, 360, 60, heat=1.0, a=hk)
            heat_lines(c, 320, 800, 440, 1180, t, a=0.6 * hk)
            thermo(c, 150, 1180, 1.1, 0.4 + 0.5 * hk, a=hk, hot=hk > 0.6)
            return
        bk = prog(t, T["bars"] - 0.3, T["bars"])
        ck = prog(t, T["clips"] - 0.3, T["clips"])
        sl = prog(t, T["slide"] - 0.3, T["slide"] + 0.4)
        sway = math.sin(t * 3.0) * 22 * sl
        for k in range(5):
            py = 480 + k * 140
            c.save()
            c.translate(sway * (1 if k % 2 else 0.6), 0)
            c.drawRRect(rr(290, py, 520, 130, 14), P(COPPER[0]))
            c.drawRRect(rr(290, py, 520, 130, 14), P(COPPER[1], 1.0, stroke=4))
            c.restore()
        for k in range(5):                                         # thin bars following the panels, flexing
            yy = 545 + k * 140
            bp = skia.Path()
            bp.moveTo(250, yy + 30)
            bp.quadTo(550 + sway * 0.4, yy - 20, 850, yy + 30)
            c.drawPath(bp, P("#4B3A2E", bk, stroke=12))
            for j in range(3):                                     # the loose clips (saddles)
                cx_ = 380 + j * 170 + sway * 0.8
                c.drawRRect(rr(cx_ - 26, yy - 18, 52, 30, 8), P("#B87333", ck))
                c.drawRRect(rr(cx_ - 26, yy - 18, 52, 30, 8), P("#5A3A20", ck, stroke=3))
        if sl > 0:
            for sd in (-1, 1):
                arrow(c, 540, 1230, 540 + sd * 120, 1230, GOOD, a=sl, w=8, head=20)

    def ui_skin(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "bolt", T["bolt"] - 0.2, T["wind"] - 0.15, accent="#94A3B8", size=46)
            self.chip(540, 300, "rip", T["wind"] - 0.15, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["rip1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["rip1"], 1.2)
            return
        self.chip(540, 300, "bars", T["bars"] - 0.2, T["clips"] - 0.15, accent="#D6A77A", size=46)
        self.chip(540, 300, "clips", T["clips"] - 0.15, s("break3") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["sway1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: battery (break3, fix3)
    def draw_battery(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        vrect(c, 0, 0, W, H, ["#0B2A3A", "#1A4A5A", "#2A5A6A"])
        rng = random.Random(6)
        for _ in range(40):                                        # salty droplets in the air
            x0_ = rng.uniform(0, W)
            y0_ = (rng.uniform(0, H) + t * rng.uniform(40, 90)) % H
            c.drawCircle(x0_, y0_, rng.uniform(4, 9), P("#BFE9FF", 0.35))
        c.drawRRect(rr(140, 520, 800, 200, 20), P(COPPER[0]))         # the copper skin
        c.drawRRect(rr(140, 520, 800, 200, 20), P(COPPER[1], 1.0, stroke=5))
        if not fixed:
            rk = prog(t, T["rusts"] - 0.4, T["rust1"] + 0.6)
            ironw = 120 * (1 - 0.55 * rk)
            c.drawRect(R(480 - ironw / 2, 720, ironw, 560), P(mix(IRONC, "#B45309", rk)))
            for k in range(int(14 * rk)):                          # rust flakes falling
                q = (t * 0.6 + k / 14.0) % 1.0
                c.drawRect(R(420 + (k * 37) % 120, 760 + q * 500, 12, 8), P("#C2410C", rk * (1 - q)))
            bk = prog(t, T["battery"] - 0.3, T["battery"])
            if bk > 0:                                             # the battery that forms where they touch
                c.drawRRect(rr(640, 820, 150, 240, 20), P("#111827", bk))
                c.drawRect(R(690, 800, 50, 22), P("#111827", bk))
                text(c, "+", 715, 900, 70, "#FCA5A5", "Poppins-Black", a=bk, align="center")
                text(c, "-", 715, 1030, 80, "#93C5FD", "Poppins-Black", a=bk, align="center")
                for k in range(4):                                 # current flowing
                    q = (t * 1.4 + k / 4.0) % 1.0
                    c.drawCircle(lerp(560, 640, q), 740 + q * 40, 8, P(HILITE, bk))
            return
        ck = prog(t, T["cloth"] - 0.3, T["cloth"])
        st = prog(t, T["century"] - 0.2, T["steel1"])
        c.drawRect(R(420, 720, 120, 560), P(mix(IRONC, "#D1D5DB", st)))
        if st > 0:
            add_glow(c, 480, 1000, 160, "#FFFFFF", 0.15 * st)
        c.drawRect(R(380, 712, 200, 26 * ck + 0.01), P("#8A5A2A", ck))          # the varnished cloth
        for k in range(8):
            c.drawLine(390 + k * 24, 716, 400 + k * 24, 734, P("#5A3A1A", ck, stroke=2))

    def ui_battery(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "battery", min(T["salty"], T["touching"]) - 0.2, T["rusts"] - 0.2, accent=HILITE, size=38)
            self.chip(540, 300, "rust", T["rusts"] - 0.2, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["rust1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["rust1"], 1.2)
            return
        self.chip(540, 300, "cloth", T["apart"] - 0.2, T["century"] - 0.2, accent="#D6A77A", size=42)
        self.chip(540, 300, "steel", T["century"] - 0.2, s("break4") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["steel1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: paris (break4, fix4)
    def draw_paris(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=1150)
        if not fixed or t < T["apart4"]:
            c.save()                                               # 1884: she stands over the rooftops of Paris
            c.translate(540, 1150)
            rooftops(c, -700, 700, 0, t, seed=9)
            c.restore()
            vrect(c, 0, 1150, W, H - 1150, ["#4A4458", "#2A2638"])
            ak = 1.0 if not fixed else 1 - prog(t, T["apart4"] - 0.3, T["apart4"])
            statue(c, 540, 1150 - 40, 2.3, t, a=ak)
            for k in range(3):                                     # scaffolding
                c.drawLine(380 + k * 160, 1150, 380 + k * 160, 500, P("#6B4F3A", 0.6 * ak, stroke=5))
            if not fixed:
                ok = prog(t, T["ocean"] - 0.3, T["ocean1"] + 0.3)
                if ok > 0:                                         # the ocean in the way
                    vrect(c, 0, 1150, W, 300, ["#1E5A7A", "#0B2A4A"], a=ok)
                    arrow(c, 120, 1060, 960, 1060, WARN, a=ok, w=12, head=30)
            return
        pk = prog(t, T["apart4"] - 0.2, T["pieces"] + 0.4)          # pieces flying into crates, crates onto the ship
        sk = prog(t, T["ship"] - 0.4, T["ship1"] + 1.0)
        vrect(c, 0, 1150, W, 770, ["#1E5A7A", "#0B2A4A"])
        for k in range(6):
            c.drawLine(0, 1180 + k * 40, W, 1180 + k * 40 + math.sin(t + k) * 4, P("#9FD3F0", 0.25, stroke=3))
        sx = lerp(540, 380, sk)
        ship(c, sx, 1170, 0.9, t, blocks=0.0)
        for k in range(8):                                         # crates on deck
            crate(c, sx - 150 + (k % 4) * 80, 1116 - (k // 4) * 56, 70, 52)
        rng = random.Random(11)
        for k in range(24):
            q = clamp(pk * 1.4 - k / 34.0)
            if 0 < q < 1:
                x0_, y0_ = 540 + rng.uniform(-120, 120), 600 + rng.uniform(-200, 200)
                x1_, y1_ = sx - 150 + (k % 4) * 80, 1090
                px, py = lerp(x0_, x1_, e_in(q)), lerp(y0_, y1_, e_in(q)) - math.sin(q * math.pi) * 80
                c.save()
                c.translate(px, py)
                c.rotate(t * 90 + k * 30)
                c.drawRRect(rr(-24, -16, 48, 32, 6), P(COPPER[k % 3]))
                c.restore()
            else:
                rng.uniform(-120, 120)

    def ui_paris(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "paris", T["paris"] - 0.2, T["ocean"] - 0.2, accent="#93C5FD", size=46)
            self.chip(540, 300, "ocean", T["ocean"] - 0.2, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["ocean1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["ocean1"], 1.2)
            return
        self.chip(540, 300, "pieces", T["apart4"] - 0.2, T["ship"] - 0.2, accent="#FDBA74", size=48)
        self.chip(540, 300, "ship", T["ship"] - 0.2, s("cta") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["ship1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#3A2A4A", "#5A3A5A", "#7A4A5A"])
        c.drawRect(R(0, 1180, W, 740), P("#4A3A30"))                 # the shop counter
        c.drawRect(R(0, 1180, W, 18), P("#8A6A50"))
        sk = prog(t, T["t_copper"] - 0.2, T["t_world"] + 0.2) * (1 - prog(t, T["t_ring"] - 0.4, T["t_ring"] - 0.1))
        if sk > 0:                                                 # she is green and the world loves her
            c.save()
            c.translate(540, 1150)
            c.scale(2.6, 2.6)
            statue(c, 0, 0, 1.0, t, green=1.0, a=sk)
            c.restore()
            for k in range(6):
                heart(c, 300 + k * 90, 560 + (k % 2) * 60 - (t * 40 % 80), 1.1, sk * 0.9)
        rk = prog(t, T["t_ring"] - 0.3, T["t_ring"])
        if rk > 0:                                                 # the hand with the cheap ring and a green finger
            c.save()
            c.translate(560, 820)
            c.rotate(-14)
            c.drawRRect(rr(-150, -40, 260, 230, 70), P("#E8B48A", rk))
            for k, (fx_, fl) in enumerate(((-120, 170), (-60, 210), (0, 220), (60, 190))):
                col = "#E8B48A" if k != 2 else mix("#E8B48A", "#4ADE80", rk)
                c.drawRRect(rr(fx_ - 24, -40 - fl, 50, fl + 30, 25), P(col, rk))
            c.drawRRect(rr(-26, -128, 54, 28, 12), P("#D4AF37", rk))
            c.drawCircle(1, -114, 10, P("#F472B6", rk))
            c.restore()
        fk = prog(t, T["t_refund"] - 0.3, T["t_refund"])
        if fk > 0:
            if self.rtl:
                saudi_man(c, 300, 1700, 520, t, pose="point", face=1, a=fk)
            else:
                person(c, 300, 1700, 520, "#2563EB", t, pose="point", face=1, a=fk)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "loves", T["t_world"] - 0.2, T["t_ring"] - 0.3, accent="#9AD3BF", size=46)
        if self.rtl:
            self.chip(540, 300, "refund", T["t_refund"] - 0.2, self.duration + 1, accent=WARN, size=44)
            bubble(c, 720, 600, self.L["bubble"], self.span(T["t_refund"], self.duration + 1), tail_left=True, size=54)
        else:
            self.chip(540, 300, "refund", T["t_refund"] - 0.2, self.duration + 1, accent=WARN, size=54)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["congrats"]), 61), -18), (T["copper"], sfx.sparkle(0.7, 8, 62), -12),
              (T["storms"], rumble(1.4, 63), -8), (T["storms"] + 0.05, sfx.snap(64), -10),
              (T["coins"], sfx.clank(1400.0, 0.4, 65), -12), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 66), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 67), -8), (T["liberty"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["crumple"], sfx.creak(0.9, 69), -10),
               (T["foil1"], sfx.womp(), -8), (T["foil1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 70), -4), (T["towerw"], sfx.riser(1.0, 71), -14),
               (T["inside1"], sfx.clank(500.0, 0.4, 72), -8), (T["inside1"] + 0.2, sfx.ding(), -8),
               (T["inside1"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["wind"], sfx.hiss(1.6, 74), -12),
               (T["rip1"], sfx.snap(75), -6), (T["rip1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["clips"], sfx.click(77), -8),
               (T["slide"], sfx.creak(1.0, 78), -14), (T["sway1"], sfx.ding(), -8), (T["sway1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["battery"], sfx.buzz(0.5), -12),
               (T["rust1"], sfx.sizzle(0.8, 80), -10), (T["rust1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 81), -4), (T["cloth"], sfx.whoosh(0.4, False, 82), -12),
               (T["steel"], sfx.sparkle(0.7, 9, 83), -10), (T["steel1"], sfx.ding(), -8), (T["steel1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 84), -4), (T["ocean1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 85), -4)]
        for k in range(6):
            ev.append((T["apart4"] + k * 0.22, sfx.clank(700.0 + k * 40, 0.2, 86 + k), -16))
        ev += [(T["ship1"], sfx.bell(520.0, 1.0, 0.8), -10), (T["ship1"] + 0.2, sfx.ding(), -8), (T["ship1"] + 0.4, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(93), 0), (T["follow"] - 0.15, sfx.pop(94), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 95), -6), (T["paint"], sfx.hiss(1.2, 96), -16),
               (T["green"], sfx.sparkle(0.9, 12, 97), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 98), -6), (T["s1"], sfx.pop(99), -3), (T["s2"], sfx.pop(100), -3),
               (T["s3"], sfx.pop(101), -3)]
        ev += [(T["cong2"], sfx.pop(102), -2), (T["cong2"], sfx.sparkle(1.4, 18, 103), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 104), -6), (T["t_ring"], sfx.sparkle(0.5, 6, 105), -12),
               (T["t_refund"], sfx.buzz(0.4), -12)]
        return ev


NAME = "liberty"
EPISODE = Liberty
