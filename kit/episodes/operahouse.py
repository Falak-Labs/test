"""Episode 57 - The Sydney Opera House.  v2 look: the harbour at golden hour and dusk, the shells cut from one sphere.

Sets: harbour (hook: slices peel off one giant ball and drop onto the point as the roof shells; reveal: opened in 1973,
fireworks, and the architect's boat sailing away; stat with a 67 m ruler; closer at dusk with the shells lit), sketch
(break1: the winning sketch, loose white sails, question marks), sphere (fix1: one sphere, an orange peeled into the
same slices, every shell the same curve), molds (break2: a different mold for every shape, the bill climbing; fix2: the
same few molds casting identical rib pieces on site), cranes (break3: a 15 t piece hanging in the air; fix3: cranes set
the pieces one by one into arched ribs and steel cables pull them tight), tiles (break4: a grubby roof and blinding
glare; fix4: chevron tiles, glossy and matte, rain washing them clean), tag (EN: the quick kitchen makeover, ten years
and fourteen times the bill; AR: the contractor who says two weeks).
World (harbour): side view, the water at y = 0, the podium top at y = -60; 1 m is about 6 units.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, sun  # noqa: E402
from burjalarab import path_of, saudi_man  # noqa: E402
from panama import word  # noqa: E402
from phone import bubble  # noqa: E402

GOLD = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#D98A66", "horizon": "#F2B07A",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DUSKP = {"top": "#060A22", "upper": "#14184A", "mid": "#352A66", "low": "#9A4A6A", "horizon": "#E08A6A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SHELL_A, SHELL_B, SHELL_D = "#E6E0D0", "#C9C0AA", "#8A8270"     # tile white, cream, shadow (kept mid-tone)
PODIUM = ("#B07A5A", "#7A5038")
WATER, WATER_D = "#1D4F86", "#0B2447"
PY = -60.0                                                       # podium top
# the shells: (base x, base width, height, direction: -1 tip leans left / 1 right, row 0 front / 1 back)
SHELLS = [(-330, 90, 150, -1, 0), (-250, 120, 230, -1, 0), (-150, 150, 330, -1, 0), (-20, 170, 400, -1, 0),
          (150, 120, 250, 1, 0), (-200, 120, 200, -1, 1), (-90, 140, 270, -1, 1), (60, 120, 210, 1, 1)]


def shell_path(bx, bw, h, d, y=PY):
    """A sail-like shell on the podium: base from bx to bx + bw, tip leaning toward d."""
    if d < 0:
        x0, x1 = bx, bx + bw
        tip = (x0 - bw * 0.25, y - h)
        p = skia.Path()
        p.moveTo(x0, y)
        p.cubicTo(x0 - bw * 0.05, y - h * 0.45, x0 - bw * 0.2, y - h * 0.8, tip[0], tip[1])
        p.cubicTo(x0 + bw * 0.35, y - h * 0.75, x1 - bw * 0.05, y - h * 0.3, x1, y)
    else:
        x0, x1 = bx, bx + bw
        tip = (x1 + bw * 0.25, y - h)
        p = skia.Path()
        p.moveTo(x1, y)
        p.cubicTo(x1 + bw * 0.05, y - h * 0.45, x1 + bw * 0.2, y - h * 0.8, tip[0], tip[1])
        p.cubicTo(x1 - bw * 0.35, y - h * 0.75, x0 + bw * 0.05, y - h * 0.3, x0, y)
    p.close()
    return p, tip


def shell(c, bx, bw, h, d, t, a=1.0, lit=0.0, dirt=0.0, glare=0.0, tiles=1.0, grow=1.0, y=PY, back=False):
    if a <= 0 or grow <= 0:
        return
    p, tip = shell_path(bx, bw, h * grow, d, y)
    top = mix(SHELL_A, "#FFD9A0", 0.35 * lit)
    base = mix(SHELL_B, "#A08060", 0.3 * lit)
    if back:
        top, base = shade(top, -0.18), shade(base, -0.18)
    c.drawPath(p, lin_paint(tip[0], tip[1], bx + bw * 0.5, y, [top, base, SHELL_D], [0, 0.65, 1], a=a))
    if tiles > 0:                                                  # chevron tile lines
        c.save()
        c.clipPath(p, doAntiAlias=True)
        for k in range(14):
            yy = y - (k + 0.5) * h * grow / 14
            c.drawLine(bx - bw, yy + bw * 0.4, bx + bw * 0.5, yy, P(SHELL_D, 0.22 * a * tiles, stroke=2))
            c.drawLine(bx + bw * 0.5, yy, bx + bw * 2, yy + bw * 0.4, P(SHELL_D, 0.22 * a * tiles, stroke=2))
        if dirt > 0:
            rng = random.Random(int(bx))
            for _ in range(16):
                c.drawCircle(bx + rng.uniform(0, bw), y - rng.uniform(0, h * grow), rng.uniform(10, 26), P("#5A5040", 0.45 * dirt * a))
        c.restore()
    c.drawPath(p, P(mix("#F8F4E8", "#FFE2B0", lit), 0.6 * a, stroke=3))
    if glare > 0:
        add_glow(c, tip[0] + d * -20, tip[1] + h * 0.3, h * 0.6, "#FFFFFF", 0.7 * glare * a)
    if lit > 0:
        add_glow(c, bx + bw * 0.5, y - 20, bw * 0.8, "#FFB860", 0.35 * lit * a)


def opera(c, t, a=1.0, lit=0.0, grow=1.0, dirt=0.0, glare=0.0, tiles=1.0):
    """The podium and all the shells (world space)."""
    c.drawRect(R(-420, PY, 880, -PY), lin_paint(0, PY, 0, 0, [PODIUM[0], PODIUM[1]], a=a))
    for k in range(6):                                             # the grand steps on the left
        c.drawRect(R(-470 + k * 8, PY + k * 10, 60, 10), P(shade(PODIUM[0], -0.05 * k), a))
    c.drawRect(R(-420, PY, 880, 5), P("#D9A07A", a))
    for i, (bx, bw, h, d, row) in enumerate(SHELLS):
        if row == 1:
            shell(c, bx, bw, h, d, t, a=a, lit=lit, dirt=dirt, tiles=tiles, grow=clamp(grow * 1.3 - i * 0.04), back=True)
    for i, (bx, bw, h, d, row) in enumerate(SHELLS):
        if row == 0:
            shell(c, bx, bw, h, d, t, a=a, lit=lit, dirt=dirt, glare=glare, tiles=tiles, grow=clamp(grow * 1.3 - i * 0.06))
    if lit > 0:                                                    # glass walls between the shells
        for bx, bw, h, d, row in SHELLS[:5]:
            c.drawRect(R(bx + bw * 0.2, PY - 26, bw * 0.6, 26), P("#FFC870", 0.6 * lit * a))


def bridge(c, x, y, s, a=1.0, lit=0.0):
    """The harbour's steel arch bridge, far away."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    arch = skia.Path()
    arch.moveTo(-500, 0)
    arch.quadTo(0, -420, 500, 0)
    c.drawPath(arch, P(mix("#3A4058", "#1A1E38", lit), a, stroke=26))
    arch2 = skia.Path()
    arch2.moveTo(-460, -10)
    arch2.quadTo(0, -330, 460, -10)
    c.drawPath(arch2, P(mix("#3A4058", "#1A1E38", lit), a, stroke=12))
    c.drawRect(R(-640, -140, 1280, 18), P(mix("#2A3048", "#141830", lit), a))
    for k in range(-9, 10):
        xx = k * 50
        yy = -(1 - (xx / 500.0) ** 2) * 210 * 0.98
        c.drawLine(xx, yy, xx, -122, P(mix("#3A4058", "#1A1E38", lit), a, stroke=4))
    for sx in (-560, 560):
        c.drawRect(R(sx - 40, -260, 80, 260), P(mix("#8A7A6A", "#3A3048", lit), a))
    if lit > 0:
        for k in range(-12, 13):
            add_glow(c, k * 48, -132, 10, "#FFE08A", 0.7 * lit * a)
    c.restore()


def sphere_ball(c, x, y, r, t, a=1.0, cut=0.0):
    """A big glass ball with meridians; cut 0..1 outlines one spherical-triangle slice."""
    c.drawCircle(x, y, r, rad_paint(x - r * 0.35, y - r * 0.4, r * 1.4, ["#E8F1FF", "#9DB7DE", "#4A6694"], a=0.85 * a))
    for k in range(6):
        w_ = r * abs(math.cos(math.radians(k * 30 + t * 20)))
        c.drawOval(R(x - w_, y - r, 2 * w_, 2 * r), P("#FFFFFF", 0.25 * a, stroke=2))
    for k in range(1, 4):
        hh = r * math.sin(math.radians(k * 22.5))
        c.drawOval(R(x - math.sqrt(r * r - hh * hh), y - hh - 8, 2 * math.sqrt(r * r - hh * hh), 16), P("#FFFFFF", 0.2 * a, stroke=2))
    if cut > 0:
        tri = path_of([(x - r * 0.15, y - r * 0.85), (x + r * 0.55, y + r * 0.2), (x - r * 0.45, y + r * 0.35)], close=True)
        c.drawPath(tri, P(HILITE, 0.3 * cut * a))
        c.drawPath(tri, P(HILITE, cut * a, stroke=5))


def orange(c, x, y, r, peel=0.0, a=1.0):
    c.drawCircle(x, y, r, rad_paint(x - r * 0.3, y - r * 0.3, r * 1.3, ["#FDBA74", "#F97316", "#C2410C"], a=a))
    for k in range(6):
        an = math.radians(k * 60)
        off = peel * r * 0.9
        if peel > 0:
            c.save()
            c.translate(x + math.cos(an) * off, y + math.sin(an) * off)
            c.rotate(k * 60 + 90)
            c.drawPath(path_of([(0, -r * 0.55), (r * 0.28, 0), (0, r * 0.55), (-r * 0.28, 0)], close=True),
                       P("#FB923C", a * peel))
            c.restore()
    if peel > 0:
        c.drawCircle(x, y, r * 0.8, P("#FDE68A", 0.8 * peel * a))


def crane(c, x, y, s, t, hook_y, a=1.0):
    """A simple tower crane standing on (x, y); its hook hangs at world height hook_y."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-10, -600, 20, 600), P("#F59E0B", a))
    for k in range(12):
        c.drawLine(-10, -k * 50, 10, -k * 50 - 50, P("#B45309", a, stroke=3))
    c.drawRect(R(-140, -620, 460, 16), P("#F59E0B", a))
    c.drawRect(R(-150, -650, 40, 40), P("#475569", a))
    c.restore()
    hx = x + 280 * s
    c.drawLine(hx, y - 604 * s, hx, hook_y, P("#1F2937", a, stroke=3))
    return hx


def rib_piece(c, x, y, w, h, ang=0.0, a=1.0, glow=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRRect(rr(-w / 2, -h / 2, w, h, 8), lin_paint(0, -h / 2, 0, h / 2, ["#D6D3D1", "#A8A29E"], a=a))
    c.drawLine(-w / 2 + 6, 0, w / 2 - 6, 0, P("#57534E", 0.6 * a, stroke=3))
    if glow > 0:
        add_glow(c, 0, 0, w * 0.8, HILITE, 0.4 * glow)
    c.restore()


def calendar(c, x, y, s, n, a=1.0):
    c.drawRRect(rr(x - 70 * s, y - 80 * s, 140 * s, 160 * s, 10 * s), P("#F8FAFC", a))
    c.drawRect(R(x - 70 * s, y - 80 * s, 140 * s, 40 * s), P("#DC2626", a))
    text(c, str(n), x, y + 50 * s, 70 * s, "#0F172A", "Poppins-Black", a=a)


# ====================================================================================== the episode
class OperaHouse(EpisodeV2):
    BUILD_NO = 57
    FIRST_SET = "harbour"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "OPERA HOUSE", "ar_sa": "أوبرا سيدني"}
    EMPH = {"en": ["CONGRATS", "CARVE", "ROOF", "SLICES", "ONE", "GIANT", "BALL", "SYDNEY", "OPERA", "HOUSE", "YOURSELF",
                   "SKETCH", "SAILS", "NOBODY", "KNOWS", "SHELL", "SAME", "SPHERE", "PEELING", "ORANGE", "CURVE",
                   "CONCRETE", "NEW", "MOLD", "EVERY", "SHAPE", "PIECES", "FEW", "MOLDS", "SITE", "FIFTEEN", "TONNES",
                   "HANG", "CRANES", "THREE", "HUNDRED", "FIFTY", "KILOMETERS", "STEEL", "CABLE", "TIGHT", "WHITE",
                   "DIRTY", "BLINDING", "MILLION", "SWEDISH", "TILES", "GLOSSY", "MATTE", "RAIN", "CLEAN", "FOLLOW",
                   "FERRIS", "WHEEL", "NINETEEN", "SEVENTY-THREE", "ARCHITECT", "QUIT", "NEVER", "SIXTY-SEVEN", "TALL",
                   "TWO", "THOUSAND", "TEN", "LATE", "FOURTEEN", "TIMES", "KITCHEN", "MAKEOVER"],
            "ar_sa": ["مبروك", "سقف", "شرايح", "كورة", "وحدة", "أوبرا", "سيدني", "بيدك", "رسمة", "أشرعة", "محد", "قشرة",
                      "نفس", "برتقالة", "الانحناءات", "منحني", "قالب", "شكل", "قطع", "الموقع", "خمسطعش", "طن", "قوس",
                      "الرافعات", "كيابل", "حديد", "أبيض", "يتوسخ", "يعمي", "مليون", "بلاطة", "سويدية", "لامعة",
                      "ومطفية", "المطر", "تابعني", "عجلة", "عملاقة", "مصممها", "سبعة", "وستين", "متر", "ألفين", "عشر",
                      "أربعطعش", "المقاول", "أسبوعين"]}
    KEYS = {"ar_sa": {
        ("hook", "ROOF"): "سقف", ("hook", "SLICES"): "شرايح", ("hook", "BALL"): "كورة", ("hook", "CONGRATS"): "مبروك",
        ("hook", "OPERA"): "أوبرا",
        ("break1", "SKETCH"): "رسمة", ("break1", "SAILS"): "أشرعة", ("break1", "NOBODY"): "محد",
        ("fix1", "SHELL"): "قشرة", ("fix1", "SPHERE"): "الكورة", ("fix1", "PEELING"): "تقشر", ("fix1", "CURVE"): "الانحناءات",
        ("break2", "CURVED"): "منحني", ("break2", "MOLD"): "قالب", ("break2", "SHAPE"): "شكل",
        ("fix2", "PIECES"): "قطع", ("fix2", "FEW"): "قالب", ("fix2", "SITE"): "الموقع",
        ("break3", "FIFTEEN"): "خمسطعش", ("break3", "HANG"): "تتعلق", ("break3", "CURVE"): "قوس",
        ("fix3", "CRANES"): "الرافعات", ("fix3", "ONE"): "وحدة", ("fix3", "THREE"): "ثلاثمية", ("fix3", "STEEL"): "حديد",
        ("fix3", "TIGHT"): "تشدها",
        ("break4", "WHITE"): "أبيض", ("break4", "DIRTY"): "يتوسخ", ("break4", "BLINDING"): "يعمي",
        ("fix4", "MILLION"): "مليون", ("fix4", "SWEDISH"): "سويدية", ("fix4", "GLOSSY"): "لامعة", ("fix4", "RAIN"): "المطر",
        ("fix4", "CLEAN"): "يغسلها",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "OPENED"): "انفتحت", ("reveal", "NINETEEN"): "ألف", ("reveal", "ARCHITECT"): "مصممها",
        ("reveal", "NEVER"): "رجع",
        ("stat", "SIXTY-SEVEN"): "سبعة", ("stat", "TWO"): "ألفين", ("stat", "MILLION"): "مليون",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "FINISHED"): "خلصت", ("tag", "TEN"): "عشر", ("tag", "FOURTEEN"): "أربعطعش", ("tag", "KITCHEN"): "المقاول",
        ("tag", "MAKEOVER"): "أسبوعين"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a giant Ferris wheel"),
                   "stat": [("67 m", "TALL"), ("2,194", "ROOF PIECES"), ("1,056,006", "TILES")],
                   "L": {"ball": "SLICES OF ONE GIANT BALL", "name": "THE SYDNEY OPERA HOUSE", "sketch": "THE WINNING SKETCH",
                         "nobody": "NOBODY KNOWS HOW TO BUILD IT", "sphere": "EVERY SHELL FROM ONE SPHERE",
                         "same": "SAME CURVE EVERYWHERE", "mold": "A NEW MOLD FOR EVERY SHAPE", "few": "THE SAME FEW MOLDS",
                         "site": "CAST RIGHT ON SITE", "t15": "UP TO 15 TONNES", "hang": "HANGING IN A CURVE?",
                         "cranes": "ONE BY ONE", "cable": "350 km OF STEEL CABLE", "dirty": "DIRTY BY THE SEA",
                         "blind": "BLINDING!", "tiles": "A MILLION SWEDISH TILES", "rain": "THE RAIN WASHES THEM",
                         "opened": "OPENED 1973", "quit": "THE ARCHITECT NEVER CAME BACK", "late": "10 YEARS LATE",
                         "x14": "14x THE ESTIMATE", "kitchen": "\"QUICK\" KITCHEN MAKEOVER", "m67": "67 m"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: عجلة دوّارة عملاقة"),
                      "stat": [("67", "متر طول"), ("2194", "قطعة"), ("1056006", "بلاطة")],
                      "L": {"ball": "شرايح من كورة وحدة", "name": "دار أوبرا سيدني", "sketch": "الرسمة اللي فازت",
                            "nobody": "محد يعرف كيف تنبني", "sphere": "كل قشرة من نفس الكورة",
                            "same": "كل الانحناءات وحدة", "mold": "قالب جديد لكل شكل", "few": "كم قالب بس",
                            "site": "تنصب في الموقع", "t15": "خمسطعش طن", "hang": "تتعلق في الهوا؟",
                            "cranes": "وحدة وحدة", "cable": "ثلاثمية وخمسين كيلو كيابل", "dirty": "يتوسخ جنب البحر",
                            "blind": "يعمي العيون!", "tiles": "مليون بلاطة سويدية", "rain": "المطر يغسلها",
                            "opened": "انفتحت سنة 1973", "quit": "ومصممها ما رجع يشوفها", "late": "متأخرة عشر سنين",
                            "x14": "أربعطعش ضعف", "contractor": "أسبوعين وأسلمك!", "m67": "67 م"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "roof": ("hook", "ROOF", 0.2), "slices": ("hook", "SLICES", 0.35), "ball": ("hook", "BALL", 0.55),
            "congrats": ("hook", "CONGRATS", 0.65), "opera": ("hook", "OPERA", 0.9),
            "sketch": ("break1", "SKETCH", 0.3), "sails": ("break1", "SAILS", 0.5), "nobody": ("break1", "NOBODY", 0.7),
            "shell": ("fix1", "SHELL", 0.15), "sphere": ("fix1", "SPHERE", 0.35), "peel": ("fix1", "PEELING", 0.5),
            "curve": ("fix1", "CURVE", 0.85),
            "curved": ("break2", "CURVED", 0.2), "mold": ("break2", "MOLD", 0.6), "shape": ("break2", "SHAPE", 0.9),
            "pieces": ("fix2", "PIECES", 0.3), "few": ("fix2", "FEW", 0.55), "site": ("fix2", "SITE", 0.9),
            "t15": ("break3", "FIFTEEN", 0.3), "hang": ("break3", "HANG", 0.7), "curve3": ("break3", "CURVE", 0.9),
            "cranes": ("fix3", "CRANES", 0.05), "one": ("fix3", "ONE", 0.2), "km": ("fix3", "THREE", 0.45),
            "steel": ("fix3", "STEEL", 0.75), "tight": ("fix3", "TIGHT", 0.95),
            "white": ("break4", "WHITE", 0.15), "dirty": ("break4", "DIRTY", 0.45), "blind": ("break4", "BLINDING", 0.9),
            "million": ("fix4", "MILLION", 0.2), "swedish": ("fix4", "SWEDISH", 0.35), "glossy": ("fix4", "GLOSSY", 0.55),
            "rain": ("fix4", "RAIN", 0.8), "clean": ("fix4", "CLEAN", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "opened": ("reveal", "OPENED", 0.05), "y1973": ("reveal", "NINETEEN", 0.2), "arch": ("reveal", "ARCHITECT", 0.5),
            "never": ("reveal", "NEVER", 0.8),
            "s1": ("stat", "SIXTY-SEVEN", 0.05), "s2": ("stat", "TWO", 0.35), "s3": ("stat", "MILLION", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_fin": ("tag", "FINISHED", 0.05), "t_ten": ("tag", "TEN", 0.15), "t_x14": ("tag", "FOURTEEN", 0.45),
            "t_kit": ("tag", "KITCHEN", 0.75), "t_make": ("tag", "MAKEOVER", 0.9)})
        T["nobody1"] = max(T["nobody"], T["sails"]) + 0.1
        T["shape1"] = max(T["shape"], T["mold"]) + 0.1
        T["curve31"] = max(T["curve3"], T["hang"]) + 0.1
        T["blind1"] = max(T["blind"], T["dirty"]) + 0.1
        T["curve1"] = max(T["curve"], T["peel"]) + 0.2
        T["site1"] = max(T["site"], T["few"]) + 0.2
        T["tight1"] = max(T["tight"], T["steel"]) + 0.2
        T["clean1"] = max(T["clean"], T["rain"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "sketch", 1)
        self.cut(s("fix1") - 0.12, "sphere", -1)
        self.cut(s("break2") - 0.12, "molds", 1)
        self.cut(s("break3") - 0.12, "cranes", -1)
        self.cut(s("break4") - 0.12, "tiles", 1)
        self.cut(s("reveal") - 0.12, "harbour", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        cm = Camera(0, -200, 1.25)
        cm.key(0.1, 0, -195, 1.22, max(1.0, T["congrats"] - 0.2))
        cm.key(T["congrats"] - 0.1, -10, -230, 1.38, 0.8)
        cm.key(s("reveal") - 0.12, 200, -260, 0.95, 0.0).key(s("reveal"), 180, -250, 1.0, max(1.0, s("stat") - s("reveal") - 0.3))
        cm.key(s("stat") - 0.1, 0, -260, 1.2, 0.5)
        cm.key(s("closer") - 0.1, -10, -230, 1.38, 0.6).key(s("closer") + 0.5, -10, -225, 1.42, max(1.0, e("closer") - s("closer")))
        self.cam = cm
        self.spans = [(T["nobody1"], T["curve1"] + 0.3), (T["shape1"], T["site1"] + 0.3), (T["curve31"], T["tight1"] + 0.3),
                      (T["blind1"], T["clean1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["nobody1"], 0.4, 6), (T["shape1"], 0.4, 7), (T["curve31"], 0.4, 8),
                       (T["blind1"], 0.4, 7), (T["y1973"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["t_x14"], 0.3, 6)]

    # ------------------------------------------------------------------ set: harbour (hook, reveal, stat, closer)
    def draw_harbour(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        night = 1.0 if t >= s("closer") - 0.12 else (0.6 if t >= s("reveal") - 0.12 and t < s("stat") - 0.12 else 0.0)
        hook = t < s("break1")
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=gy - 40 * z)
        if night > 0:
            c.save()
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=DUSKP, horizon_y=gy - 40 * z)
            v2.stars(c, W, H, t, 0.8)
            c.restore()
            c.restore()
        if night < 1:
            sun(c, 160 - cx * 0.04, gy - 520 * z, 46, heat=0.6, a=1 - night)
        for i, (px, py, s_) in enumerate(((240, 900, 0.9), (820, 1150, 0.7))):
            v2.cloud(c, (px + t * (5 + i * 3)) % (W + 600) - 300, gy - py * z, s_, body=mix("#7A6A9A", "#1A1E48", night),
                     rim=mix("#FFB37A", "#3A3A78", night), a=0.7, seed=i)
        self.view(c, cam)
        bridge(c, 760, -10, 0.55, lit=night)
        c.drawRect(R(-2000, -6, 4000, 10), P(mix("#3A4A3A", "#141A24", night)))   # far shore
        c.drawRect(R(-2000, 0, 4000, 900), lin_paint(0, 0, 0, 500, [mix(WATER, "#14204A", night), WATER_D]))
        for k in range(16):                                                         # glints on the water
            xx = -900 + ((k * 137 + t * 40) % 1800)
            c.drawLine(xx, 20 + (k % 5) * 30, xx + 40, 20 + (k % 5) * 30, P(mix("#BFE6FF", "#FFC870", night), 0.4, stroke=3))
        grow = 1.0
        if hook:
            grow = e_out(prog(t, T["slices"] - 0.1, T["congrats"] + 0.2))
        lit = night
        opera(c, t, lit=lit, grow=grow)
        if hook:                                                                    # the giant ball and its slices falling
            bk = prog(t, 0.0, 0.4) * (1 - prog(t, T["congrats"] + 0.2, T["congrats"] + 0.8))
            sphere_ball(c, -40, -650, 200, t, a=bk, cut=prog(t, T["slices"] - 0.3, T["slices"]))
            for i, (bx, bw, h, d, row) in enumerate(SHELLS[:5]):
                q = clamp((t - T["slices"] - i * 0.18) / 0.8)
                if 0 < q < 1:
                    p_, tip = shell_path(bx, bw, h, d)
                    c.save()
                    c.translate(lerp(-40 - bx, 0, e_in(q)), lerp(-480, 0, e_in(q)))
                    c.drawPath(p_, P(HILITE, 0.5 * (1 - q)))
                    c.restore()
        if s("reveal") - 0.12 <= t < s("stat") - 0.12:                            # 1973: fireworks; the architect's boat
            fk = prog(t, T["y1973"] - 0.2, T["y1973"] + 2.5)
            for k in range(4):
                q = (fk * 2.0 + k * 0.27) % 1.0
                if fk > 0:
                    add_glow(c, -300 + k * 200, -620 - k * 40, 40 + 90 * q, ["#FDE68A", "#F87171", "#93C5FD", "#A7F3D0"][k], 0.6 * (1 - q))
            bk = prog(t, T["arch"] - 0.3, T["never"] + 1.0)
            if bk > 0:
                bxp = lerp(-150, -650, bk)
                c.drawPath(path_of([(bxp - 40, 30), (bxp + 40, 30), (bxp + 26, 50), (bxp - 26, 50)], close=True), P("#1F2937"))
                c.drawLine(bxp, 30, bxp, -40, P("#E5E7EB", stroke=3))
                c.drawPath(path_of([(bxp, -40), (bxp + 34, 20), (bxp, 20)], close=True), P("#F1F5F9", 0.9))
                person(c, bxp - 18, 30, 40, "#1E3A8A", t, face=-1)
        if s("stat") - 0.12 <= t < s("closer") - 0.12:                            # the 67 m ruler
            rk = prog(t, T["s1"] - 0.2, T["s1"] + 0.3)
            x_ = 260
            c.drawLine(x_, PY, x_, PY - 400 * rk, P(HILITE, rk, stroke=5))
            for k in range(5):
                if k * 100 <= 400 * rk:
                    c.drawLine(x_ - 12, PY - k * 100, x_ + 12, PY - k * 100, P(HILITE, rk, stroke=4))
            self.ui["ruler"] = self.to_screen(cam, x_ + 20, PY - 400)
        c.restore()

    def ui_harbour(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "ball", T["slices"] - 0.1, T["congrats"] - 0.1, accent=HILITE, size=42)
            self.chip(540, 300, "name", T["opera"] - 0.2, s("break1") + 0.1, accent=HILITE, size=42)
        elif tw < s("stat") - 0.12:
            self.chip(540, 300, "opened", T["opened"] - 0.2, T["arch"] - 0.2, accent="#FDE68A", size=46)
            self.chip(540, 300, "quit", T["arch"] - 0.2, s("stat") - 0.15, accent="#93C5FD", size=36)
        elif tw < s("closer") - 0.12 and "ruler" in self.ui:
            rx, ry = self.ui["ruler"]
            v2.chip(c, rx + 70, ry, self.L["m67"], self.span(T["s1"], s("closer") - 0.2), accent=HILITE, size=36)

    # ------------------------------------------------------------------ break1: the sketch
    def draw_sketch(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#3A2A1E", "#2A1E16"])
        c.drawRRect(rr(90, 420, 900, 640, 12), lin_paint(0, 420, 0, 1060, ["#1E4A8A", "#163A6E"]))   # blueprint paper
        for k in range(10):
            c.drawLine(90, 460 + k * 60, 990, 460 + k * 60, P("#3A6AB0", 0.4, stroke=2))
        dk = prog(t, T["sketch"] - 0.6, T["sails"] + 0.3)
        c.save()
        c.translate(540, 900)
        c.scale(0.9, 0.9)
        for i, (bx, bw, h, d, row) in enumerate(SHELLS[:5]):                    # loose white sails, drawn by hand
            if dk * 5 > i:
                p_, tip = shell_path(bx, bw, h * 1.1, d, y=0)
                c.drawPath(p_, P("#F8FAFC", 0.9, stroke=5))
        c.drawLine(-430, 0, 430, 0, P("#F8FAFC", 0.8 * dk, stroke=4))
        c.restore()
        qk = prog(t, T["nobody"] - 0.3, T["nobody"] + 0.2)
        for k, (qx, qy) in enumerate(((220, 560), (820, 520), (560, 470))):
            text(c, "?", qx, qy + 20 * math.sin(t * 3 + k), 120, WARN, "Poppins-Black", a=qk)
        for k, px in enumerate((240, 540, 840)):                                   # puzzled engineers
            engineer(c, px, 1230, 170, SHIRTS[k], t + k, pose="shrug" if qk > 0.5 else "look", face=1 if px < 540 else -1)

    def ui_sketch(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "sketch", T["sketch"] - 0.2, T["nobody"] - 0.2, accent="#F8FAFC", size=44)
        self.chip(540, 300, "nobody", T["nobody"] - 0.2, s("fix1") - 0.15, accent=WARN, size=40)
        self.badge("alert", T["nobody1"], s("fix1") - 0.2, x=920, y=420)
        self.red(T["nobody1"], 1.2)

    # ------------------------------------------------------------------ fix1: one sphere, an orange
    def draw_sphere(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#0B1A3A", "#14285A", "#0B1A3A"])
        ok = prog(t, T["peel"] - 0.3, T["peel"] + 0.3)
        sphere_ball(c, 540, 720, 300, t, a=1 - 0.6 * ok, cut=prog(t, T["shell"] - 0.3, T["sphere"]))
        if ok > 0:
            orange(c, 540, 720, 150 * ok, peel=prog(t, T["peel"], T["curve"]), a=ok)
        ck = prog(t, T["curve"] - 0.3, T["curve1"])
        if ck > 0:                                                                 # identical slices, side by side
            for k in range(4):
                c.save()
                c.translate(220 + k * 210, 1140)
                c.rotate(-10 + k * 6)
                c.drawPath(path_of([(0, -120), (60, 40), (-60, 40)], close=True), P(SHELL_A, ck))
                c.drawPath(path_of([(0, -120), (60, 40), (-60, 40)], close=True), P(HILITE, ck, stroke=4))
                c.restore()

    def ui_sphere(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "sphere", T["shell"] - 0.2, T["curve"] - 0.2, accent=HILITE, size=40)
        self.chip(540, 300, "same", T["curve"] - 0.2, s("break2") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["curve1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ break2 / fix2: molds
    def draw_molds(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        vrect(c, 0, 0, W, H, ["#2A3348", "#1A2030"])
        c.drawRect(R(0, 1180, W, 740), lin_paint(0, 1180, 0, 1600, ["#6B6560", "#3A3632"]))
        if not fixed:
            mk = prog(t, s("break2") - 0.1, T["shape1"] + 0.4)
            gk = 1 - prog(t, T["mold"] - 0.3, T["mold"] + 0.3)
            if gk > 0:                                                             # a curved roof: how do you pour it?
                c.save()
                c.translate(540, 1100)
                c.scale(1.4, 1.4)
                p_, tip = shell_path(-60, 150, 330, -1, y=0)
                c.drawPath(p_, P("#94A3B8", 0.35 * gk))
                c.drawPath(p_, dash_paint("#E5E7EB", gk, 4, t, 14, 10))
                c.restore()
            rng = random.Random(3)
            for k in range(int(12 * mk)):                                          # a different mold for every shape
                x_, y_ = 150 + (k % 4) * 260, 1160 - (k // 4) * 170
                p_ = path_of([(x_ - 100, y_), (x_ - 100 + rng.uniform(0, 60), y_ - rng.uniform(60, 150)),
                              (x_ + rng.uniform(-20, 80), y_ - rng.uniform(80, 160)), (x_ + 100, y_)], close=True)
                c.drawPath(p_, P(["#8A6A4A", "#7A5A3A", "#9A7A5A"][k % 3]))
                c.drawPath(p_, P("#3A2A1A", stroke=3))
            text(c, "$" * (1 + int(6 * mk)), 540, 640, 110, WARN, "Poppins-Black", a=mk)
        else:
            for k in range(3):                                                     # the same few molds
                box(c, 120 + k * 300, 1060, 240, 110, "#7A5A3A", r=12)
            pk = prog(t, T["pieces"] - 0.3, T["site1"] + 1.0)
            n = int(18 * pk)
            for k in range(n):                                                     # identical rib pieces, stacked
                rib_piece(c, 180 + (k % 6) * 140, 1020 - (k // 6) * 70, 120, 50, a=1.0)
            q = (t * 0.8) % 1.0
            for k in range(3):
                rib_piece(c, 240 + k * 300, 1080 - 60 * q, 120, 50, a=1 - q)

    def ui_molds(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "mold", T["mold"] - 0.3, s("fix2") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["shape1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["shape1"], 1.2)
            return
        self.chip(540, 300, "few", T["pieces"] - 0.2, T["site"] - 0.2, accent=HILITE, size=44)
        self.chip(540, 300, "site", T["site"] - 0.2, s("break3") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["site1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ break3 / fix3: cranes and cables
    def draw_cranes(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=1150)
        cam = (0, -200, 1.25)
        self.view(c, cam)
        c.drawRect(R(-1200, 0, 2400, 900), lin_paint(0, 0, 0, 400, [WATER, WATER_D]))
        c.drawRect(R(-420, PY, 880, -PY), P(PODIUM[0]))
        p_, tip = shell_path(-150, 300, 420, -1)                                    # the shell to come, as a ghost
        c.drawPath(p_, P("#E6E0D0", 0.12))
        c.drawPath(p_, dash_paint("#E6E0D0", 0.5, 3, t, 14, 10))
        n = 9
        pts = []                                                                   # one rib: pieces up the shell's edge
        for k in range(n + 1):
            u = k / float(n)
            pts.append((lerp(-150, tip[0], u) - 70 * math.sin(u * math.pi), lerp(PY, tip[1], u)))
        placed = 3 if not fixed else min(n, 3 + int(prog(t, T["cranes"], T["steel"]) * (n - 3) + 0.0001))
        for k in range(placed):
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]
            rib_piece(c, (x0 + x1) / 2, (y0 + y1) / 2, 64, 40, ang=math.degrees(math.atan2(y1 - y0, x1 - x0)),
                      glow=prog(t, T["steel"], T["tight1"]) if fixed else 0.0)
        hook_y = PY - 560
        if not fixed:                                                              # one 15 t piece hanging in the air
            hk = prog(t, T["t15"] - 0.4, T["curve31"])
            hx = crane(c, 120, PY, 0.95, t, hook_y + 40 * math.sin(t * 2) * hk)
            rib_piece(c, hx, hook_y + 40 * math.sin(t * 2) * hk + 28, 64, 40, ang=12 * math.sin(t * 1.7) * hk)
        else:
            q = (t * 0.7) % 1.0
            hx = crane(c, 120, PY, 0.95, t, lerp(PY - 60, hook_y, q))
            rib_piece(c, hx, lerp(PY - 60, hook_y, q) + 28, 64, 40, a=0.9)
            ck = prog(t, T["steel"] - 0.3, T["tight1"])
            if ck > 0:                                                             # the steel cable through the rib
                c.drawPath(path_of(pts[:placed + 1]), P(HILITE, ck, stroke=5))
                tk = prog(t, T["tight"] - 0.2, T["tight1"])
                for k in range(0, placed + 1, 3):
                    add_glow(c, pts[k][0], pts[k][1], 26, HILITE, 0.6 * tk)
        c.restore()

    def ui_cranes(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "t15", T["t15"] - 0.2, T["hang"] - 0.2, accent="#FDBA74", size=46)
            self.chip(540, 300, "hang", T["hang"] - 0.2, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["curve31"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["curve31"], 1.2)
            return
        self.chip(540, 300, "cranes", T["cranes"] - 0.2, T["km"] - 0.2, accent=HILITE, size=46)
        self.chip(540, 300, "cable", T["km"] - 0.2, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["tight1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ break4 / fix4: the tiles
    def draw_tiles(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=1200)
        if not fixed:
            sun(c, 860, 360, 60, heat=1.0)
        cam = (-40, -230, 1.55)
        self.view(c, cam)
        c.drawRect(R(-1200, 0, 2400, 900), lin_paint(0, 0, 0, 400, [WATER, WATER_D]))
        if not fixed:
            dk = prog(t, T["dirty"] - 0.4, T["dirty"] + 0.2)
            gk = prog(t, T["blind"] - 0.3, T["blind1"] + 0.2)
            opera(c, t, dirt=dk, glare=gk, tiles=0.0)
        else:
            tk = prog(t, T["million"] - 0.4, T["glossy"] + 0.4)
            opera(c, t, tiles=tk)
            rk = prog(t, T["rain"] - 0.3, T["clean1"] + 0.3)
            if rk > 0:                                                             # rain washing them clean
                rng = random.Random(int(t * 10))
                for _ in range(90):
                    xx, yy = rng.uniform(-500, 500), rng.uniform(-700, 0)
                    c.drawLine(xx, yy, xx - 6, yy + 34, P("#BFE6FF", 0.55 * rk, stroke=2))
        c.restore()
        if not fixed:
            gk = prog(t, T["blind"] - 0.3, T["blind1"] + 0.2)
            if gk > 0:
                c.drawRect(R(0, 0, W, H), P("#FFF7E0", 0.35 * gk * (0.6 + 0.4 * math.sin(t * 12))))
                person(c, 200, 1240, 260, "#E11D48", t, pose="duck", face=1, a=gk)

    def ui_tiles(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "dirty", T["white"] - 0.2, T["blind"] - 0.2, accent="#D6C29A", size=44)
            self.chip(540, 300, "blind", T["blind"] - 0.2, s("fix4") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["blind1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["blind1"], 1.2)
            return
        self.chip(540, 300, "tiles", T["million"] - 0.2, T["rain"] - 0.2, accent=HILITE, size=40)
        self.chip(540, 300, "rain", T["rain"] - 0.2, s("cta") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["clean1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#3A3A48", "#26262F"])
        c.drawRect(R(0, 1180, W, 740), lin_paint(0, 1180, 0, 1500, ["#8A7A6A", "#4A4038"]))
        c.drawRect(R(120, 760, 840, 420), P("#5A4A3A"))                            # half-built kitchen cabinets
        for k in range(4):
            c.drawRect(R(140 + k * 205, 790, 185, 360), P("#7A6A5A" if k % 2 else "#6A5A4A"))
        c.drawRect(R(120, 740, 840, 30), P("#9CA3AF"))
        yk = prog(t, T["t_ten"] - 0.2, T["t_x14"])                                # the calendar flipping years
        calendar(c, 820, 560, 1.0, 1963 + int(10 * yk), a=1.0)
        if not self.rtl:
            bk = prog(t, T["t_x14"] - 0.2, T["t_x14"] + 0.6)
            c.drawRRect(rr(160, 420, 300, 120 + 300 * bk, 10), P("#F8FAFC"))         # the bill unrolling
            for k in range(int(3 + 10 * bk)):
                c.drawLine(190, 460 + k * 28, 420, 460 + k * 28, P("#94A3B8", stroke=4))
            text(c, "x14", 310, 520 + 300 * bk, 70, WARN, "Poppins-Black", a=bk)
            person(c, 540, 1230, 300, "#2563EB", t, pose="shrug" if bk > 0.5 else "look", face=-1)
        else:
            engineer(c, 360, 1230, 280, "#F59E0B", t, pose="point", face=1)
            saudi_man(c, 760, 1230, 300, t, pose="shrug" if yk > 0.5 else "look", face=-1)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "late", T["t_ten"] - 0.2, T["t_x14"] - 0.1, accent=WARN, size=44)
        if not self.rtl:
            self.chip(540, 300, "x14", T["t_x14"] - 0.1, T["t_kit"] - 0.2, accent=WARN, size=44)
            self.chip(540, 300, "kitchen", T["t_kit"] - 0.2, self.duration + 1, accent=HILITE, size=40)
        else:
            self.chip(540, 300, "x14", T["t_x14"] - 0.1, self.duration + 1, accent=WARN, size=44)
            bubble(c, 360, 860, self.L["contractor"], self.span(T["t_kit"] - 0.1, self.duration + 1), tail_left=True, size=46)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.riser(1.2, 61), -16), (T["slices"], sfx.whoosh(0.6, False, 62), -10),
              (T["slices"] + 0.5, sfx.thud(0.3, 63), -12), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8), (T["opera"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["sails"], sfx.tap(67), -10),
               (T["nobody1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["peel"], sfx.snap(69), -10),
               (T["curve1"], sfx.ding(), -8), (T["curve1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 70), -4), (T["mold"], sfx.thud(0.3, 71), -12),
               (T["shape1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 72), -4)]
        for k in range(4):
            ev.append((T["pieces"] + k * 0.35, sfx.thunk(73 + k), -14))
        ev += [(T["site1"], sfx.ding(), -8), (T["site1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 77), -4), (T["t15"], sfx.creak(0.9, 78), -10),
               (T["curve31"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 79), -4), (T["cranes"], sfx.whirr(1.2, 80.0, 120.0, 80), -14),
               (T["steel"], sfx.clank(500.0, 0.4, 81), -10), (T["tight1"], sfx.ding(), -8), (T["tight1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 82), -4), (T["blind"], sfx.buzz(0.4), -12),
               (T["blind1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 83), -4), (T["million"], sfx.sparkle(0.6, 8, 84), -10),
               (T["rain"], sfx.hiss(1.4, 85), -16), (T["clean1"], sfx.ding(), -8), (T["clean1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(86), 0), (T["follow"] - 0.15, sfx.pop(87), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 88), -6), (T["y1973"], sfx.sparkle(1.2, 14, 89), -8),
               (T["never"], sfx.bell(660.0, 1.0, 0.5), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 90), -6), (T["s1"], sfx.pop(91), -3), (T["s2"], sfx.pop(92), -3),
               (T["s3"], sfx.pop(93), -3)]
        ev += [(T["cong2"], sfx.pop(94), -2), (T["cong2"], sfx.sparkle(1.4, 18, 95), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 96), -6), (T["t_ten"], sfx.tick(), -8), (T["t_x14"], sfx.buzz(0.3), -12),
               (T["t_kit"], sfx.pop(97), -6)]
        return ev


NAME = "operahouse"
EPISODE = OperaHouse
