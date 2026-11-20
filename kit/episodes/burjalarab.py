"""Episode 51 - The Burj Al Arab.  v2 look: the Gulf at golden hour and dusk, a white sail standing in a turquoise
sea, the Dubai skyline far behind.

Sets: coast (hook: the sail-shaped hotel standing in the sea on its own island; reveal: the helipad 210 m up with two
tennis players; stat; closer at night with the sail lit in colour), island (break1/fix1: open sea and no land, then a
ring of rocks filled with sand until an island rises, in section), piles (break2/fix2: soft sand with no bedrock, the
tower sinks; 230 concrete piles driven 40 m down, the sand grips their sides, friction holds it up), shore (break3/fix3:
waves chew the island's edge; hollow concrete blocks in a honeycomb take the waves, which crash, lose their power and
drain away), sail (break4/fix4: the giant atrium cooking in the desert sun; a glass-fibre fabric sail across the front
lets the light in and bounces the heat away), tag (EN: the tiny shampoo bottles in the suitcase; AR: the uncle who hears
you booked a hotel).
World (coast): side view, the sea level at y = 0, the hotel about 740 units tall (1 m = 2.3 units).
"""
from v2_base import *  # noqa: F401,F403
from falaj import word  # noqa: E402
from windtower import arrow, thermo, heat_lines, sun  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#3A3A78", "horizon": "#7A5A9A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SEA, SEA_D = "#1E7A9A", "#0B3A5A"
SAND, SAND_D = "#C9A46A", "#8A6A3E"
SAILC = "#C9D3E0"
STEEL = "#8C96A8"
HB = 740                                                                 # hotel height (world units)


def path_of(pts, close=False):
    p_ = skia.Path()
    p_.moveTo(*pts[0])
    for q in pts[1:]:
        p_.lineTo(*q)
    if close:
        p_.close()
    return p_


def sea_band(c, x0, x1, y0, depth, t, col=SEA, dark=SEA_D, a=1.0):
    vrect(c, x0, y0, x1 - x0, depth, [col, dark], a=a)
    for k in range(6):
        yy = y0 + 8 + k * 26
        p_ = skia.Path()
        p_.moveTo(x0, yy)
        xx = x0
        while xx < x1:
            xx += 40
            p_.lineTo(xx, yy + math.sin(xx * 0.013 + t * (1.4 + k * 0.3) + k) * (4 + k))
        c.drawPath(p_, P("#BDEBFF", (0.35 - k * 0.05) * a, stroke=3))


def burj(c, x, y, t, s=1.0, build=1.0, lit=0.0, helipad=1.0, tennis=0.0, a=1.0):
    """The hotel standing on (x, y) (its base), side view: the sail's curved face to the left, the steel mast on the
    right; build 0..1 grows it from the bottom; lit 0..1 the night colours on the sail; helipad 0..1."""
    if a <= 0 or build <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    clip = skia.Path()
    clip.addRect(R(-400, -HB * build - 60, 800, HB * build + 80))
    c.clipPath(clip, doAntiAlias=True)
    front = []
    for i in range(41):
        u = i / 40.0
        fx = (1 - u) ** 2 * -150 + 2 * (1 - u) * u * -175 + u * u * 20
        fy = (1 - u) ** 2 * 0 + 2 * (1 - u) * u * -430 + u * u * -(HB - 50)
        front.append((fx, fy))
    body = path_of(front + [(40, -(HB - 60)), (62, 0)], close=True)
    c.drawPath(body, lin_paint(-160, 0, 60, 0, ["#9AA8BC", "#7C8AA0", "#5E6B80"], a=a))
    for k in range(1, 28):                                                  # floors seen on the side wing
        yy = -k * 24
        xl = None
        for fx, fy in front:
            if fy <= yy:
                xl = fx
                break
        if xl is not None and yy > -(HB - 70):
            c.drawLine(xl + 8, yy, 50, yy, P("#3E4A5E", 0.55 * a, stroke=2))
            if lit > 0 and k % 2 == 0:
                c.drawLine(xl + 14, yy - 8, 44, yy - 8, P("#FFD58A", 0.6 * lit * a, stroke=4))
    sail = skia.Path()                                                      # the fabric face, a band along the front
    sail.moveTo(*front[0])
    for q in front[1:]:
        sail.lineTo(*q)
    for q in reversed(front):
        sail.lineTo(q[0] + 70 * (1 - abs(q[1]) / HB) + 10, q[1])
    sail.close()
    if lit > 0:
        hue = (t * 0.15) % 1.0
        cols = ["#6D28D9", "#DB2777", "#2563EB", "#0EA5E9", "#6D28D9"]
        i0 = int(hue * 4)
        col = mix(cols[i0], cols[i0 + 1], hue * 4 - i0)
        c.drawPath(sail, lin_paint(0, -HB, 0, 0, [mix(SAILC, col, lit), mix("#AEB9C9", shade(col, -0.2), lit)], a=a))
        add_glow(c, -110, -360, 260, col, 0.25 * lit * a)
    else:
        c.drawPath(sail, lin_paint(0, -HB, 0, 0, [SAILC, "#AEB9C9"], a=a))
    for k in range(1, 12):                                                  # fabric seams
        yy = -k * 62
        c.drawLine(-200, yy, 80, yy + 6, P("#8E9AAE", 0.4 * a, stroke=2))
    c.drawPath(path_of(front), P("#E8EEF5", 0.9 * a, stroke=6))
    for dx0, dx1 in ((62, 40), (88, 60)):                                   # the steel exoskeleton (two legs)
        c.drawLine(dx0, 0, dx1, -(HB - 10), P(STEEL, a, stroke=10))
    for k in range(9):
        y0 = -k * 82
        y1 = y0 - 82
        x0a, x1a = lerp(62, 40, -y0 / HB), lerp(88, 60, -y0 / HB)
        x0b, x1b = lerp(62, 40, -y1 / HB), lerp(88, 60, -y1 / HB)
        c.drawLine(x0a, y0, x1b, y1, P(STEEL, 0.8 * a, stroke=5))
        c.drawLine(x1a, y0, x0b, y1, P(STEEL, 0.8 * a, stroke=5))
    c.drawLine(50, -(HB - 10), 46, -HB - 40, P(STEEL, a, stroke=8))         # the mast top
    c.drawOval(R(-120, -HB + 70, 120, 34), P("#7C8AA0", a))                 # the restaurant pod near the top
    c.drawOval(R(-112, -HB + 76, 104, 12), P("#FFD58A", 0.7 * a))
    if helipad > 0:                                                         # the helipad, cantilevered out
        hk = e_out(clamp(helipad))
        hx, hy = 60 + 110 * hk, -505
        c.drawLine(62, hy + 40, hx - 20, hy + 6, P(STEEL, a, stroke=8))
        c.drawOval(R(hx - 70 * hk, hy - 14, 140 * hk, 30), P("#2F855A", a))
        c.drawOval(R(hx - 70 * hk, hy - 14, 140 * hk, 30), P("#E8EEF5", a, stroke=3))
        if hk > 0.6:
            text(c, "H", hx, hy + 9, 20, "#F8FAFC", "Poppins-Black", a=a)
        if tennis > 0:
            c.drawLine(hx, hy - 12, hx, hy - 2, P("#F8FAFC", tennis * a, stroke=2))
            for sd in (-1, 1):
                person(c, hx + sd * 44, hy, 26, "#F8FAFC" if sd < 0 else "#FDE68A", t + sd, pose="cheer" if sd < 0 else "stand",
                       face=-sd, hat="none", hair="#1C1917", a=tennis * a)
            q = (t * 1.3) % 1.0
            bx = hx + lerp(-40, 40, q if int(t * 1.3) % 2 == 0 else 1 - q)
            c.drawCircle(bx, hy - 12 - math.sin(q * math.pi) * 18, 3, P("#D9F99D", tennis * a))
    c.restore()


def island(c, t, x0=-250, x1=250, top=-24, blocks=1.0, a=1.0):
    """The island (world space, coast set): sand top, armour blocks on the slopes."""
    ip = skia.Path()
    ip.moveTo(x0 - 90, 60)
    ip.lineTo(x0, top)
    ip.lineTo(x1, top)
    ip.lineTo(x1 + 90, 60)
    ip.close()
    c.drawPath(ip, lin_paint(0, top, 0, 60, [SAND, SAND_D], a=a))
    for sd in (-1, 1):
        for k in range(10):
            bx = (x1 + 10 + k * 8) * sd if sd > 0 else (x0 - 10 - k * 8)
            c.drawCircle(bx, top + 6 + k * 6, 9, P("#9CA3AF", blocks * a))
            c.drawCircle(bx, top + 6 + k * 6, 4, P("#4B5563", blocks * a))
    c.drawRect(R(x0, top - 6, x1 - x0, 8), P("#E5D3B0", a))


def skyline(c, x0, x1, y, t, a=1.0):
    """Far Dubai skyline with the tallest tower (world space, base y)."""
    rng = random.Random(5)
    x = x0
    while x < x1:
        w = rng.uniform(30, 70)
        h = rng.uniform(40, 160)
        c.drawRect(R(x, y - h, w, h), P("#3A4A72", 0.85 * a))
        for k in range(int(h / 24)):
            if rng.random() < 0.5:
                c.drawRect(R(x + 8, y - h + 10 + k * 24, w - 16, 5), P("#FFD58A", 0.5 * a))
        x += w + rng.uniform(4, 30)
    bk = skia.Path()                                                        # the tallest tower, a needle
    kx = x0 + (x1 - x0) * 0.72
    bk.moveTo(kx - 26, y)
    bk.lineTo(kx - 12, y - 260)
    bk.lineTo(kx - 4, y - 360)
    bk.lineTo(kx, y - 430)
    bk.lineTo(kx + 4, y - 360)
    bk.lineTo(kx + 12, y - 260)
    bk.lineTo(kx + 26, y)
    bk.close()
    c.drawPath(bk, P("#4A5A86", 0.9 * a))
    add_glow(c, kx, y - 430, 8, "#FF4D4F", 0.8 * a)


def palm_tree(c, x, y, s, t, a=1.0):
    c.drawLine(x, y, x + 10 * s, y - 120 * s, P("#6B4A2A", a, stroke=10 * s))
    for k in range(6):
        an = math.radians(-160 + k * 28 + math.sin(t * 1.5 + k) * 4)
        tip = (x + 10 * s + math.cos(an) * 70 * s, y - 120 * s + math.sin(an) * 30 * s + 30 * s)
        c.drawLine(x + 10 * s, y - 120 * s, tip[0], tip[1], P("#2F6B3A", a, stroke=8 * s))


def wave(c, x, y, w, h, t, k=1.0, a=1.0):
    """A breaking wave moving left, crest at (x, y)."""
    if a <= 0 or k <= 0:
        return
    wp = skia.Path()
    wp.moveTo(x + w, y + h)
    wp.quadTo(x + w * 0.5, y + h * 0.9, x + w * 0.2, y + h * 0.2)
    wp.quadTo(x, y - h * 0.2 * k, x - w * 0.2, y + h * 0.3)
    wp.quadTo(x - w * 0.05, y + h * 0.6, x + w * 0.1, y + h)
    wp.close()
    c.drawPath(wp, lin_paint(0, y, 0, y + h, ["#3AA6C8", SEA_D], a=a))
    c.drawPath(wp, P("#E0F7FF", 0.7 * a, stroke=5))


def hexagon(c, x, y, r, a=1.0, hole=0.45, col="#9CA3AF"):
    pts = [(x + math.cos(math.radians(60 * k + 30)) * r, y + math.sin(math.radians(60 * k + 30)) * r) for k in range(6)]
    c.drawPath(path_of(pts, close=True), P(col, a))
    c.drawPath(path_of(pts, close=True), P("#4B5563", a, stroke=3))
    c.drawCircle(x, y, r * hole, P("#1F2937", a))


def saudi_man(c, px, py, ph, t, pose="stand", face=1, a=1.0):
    """A man in a white thobe with a red shemagh and black agal, feet at (px, py)."""
    u = ph / 140.0
    dr = skia.Path()
    dr.moveTo(px - 23 * u, py - 138 * u)
    dr.lineTo(px + 23 * u, py - 138 * u)
    dr.lineTo(px + 31 * u, py - 96 * u)
    dr.lineTo(px - 31 * u, py - 96 * u)
    dr.close()
    c.drawPath(dr, P("#DC2626", a))
    for k in range(4):
        c.drawLine(px - 28 * u, py - (128 - k * 9) * u, px + 28 * u, py - (128 - k * 9) * u, P("#FEE2E2", 0.7 * a, stroke=1.6 * u))
    person(c, px, py, ph, "#E7E5E4", t, pose=pose, face=face, hat="none", hair="#1F2937", pants="#D6D3D1", skin="#C68B59", a=a)
    cap = skia.Path()
    cap.moveTo(px - 22 * u, py - 128 * u)
    cap.cubicTo(px - 22 * u, py - 152 * u, px + 22 * u, py - 152 * u, px + 22 * u, py - 128 * u)
    cap.close()
    c.drawPath(cap, P("#DC2626", a))
    c.drawOval(R(px - 20 * u, py - 145 * u, 40 * u, 8 * u), P("#111827", a, stroke=3 * u))


def shampoo(c, x, y, s, col, a=1.0, rot=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.drawRRect(rr(-12 * s, -30 * s, 24 * s, 44 * s, 8 * s), P(col, a))
    c.drawRect(R(-6 * s, -40 * s, 12 * s, 12 * s), P("#E5E7EB", a))
    c.drawRect(R(-8 * s, -18 * s, 16 * s, 12 * s), P("#F8FAFC", 0.8 * a))
    c.restore()


# ====================================================================================== the episode
class BurjAlArab(EpisodeV2):
    BUILD_NO = 51
    FIRST_SET = "coast"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "BURJ AL ARAB", "ar_sa": "برج العرب"}
    EMPH = {"en": ["CONGRATS", "HOTEL", "SHAPED", "SAIL", "SEA", "ISLAND", "MADE", "YOURSELF", "BURJ", "AL", "ARAB", "NO",
                   "LAND", "OPEN", "RING", "ROCKS", "FILL", "SAND", "RISES", "SOFT", "BEDROCK", "TOWER", "DRIVE", "TWO",
                   "HUNDRED", "THIRTY", "CONCRETE", "PILES", "FORTY", "METERS", "DOWN", "GRIPS", "SIDES", "FRICTION",
                   "HOLDS", "WAVES", "CHEW", "AWAY", "ARMOR", "SHORE", "HOLLOW", "BLOCKS", "HONEYCOMB", "CRASH", "LOSE",
                   "POWER", "DRAIN", "DESERT", "SUN", "GIANT", "ATRIUM", "OVEN", "STRETCH", "GLASS-FIBER", "FABRIC",
                   "LIGHT", "BOUNCES", "HEAT", "FOLLOW", "PALM", "TREE", "HELIPAD", "TEN", "TENNIS", "LEGENDS", "THREE",
                   "TWENTY-ONE", "TALL", "LONGER", "GOLD", "WALLS", "ROOF", "TINY", "SHAMPOO", "BOTTLES"],
            "ar_sa": ["مبروك", "فندق", "شراع", "البحر", "جزيرة", "سويتها", "بنفسك", "برج", "العرب", "أرض", "بحر", "بصخور",
                      "رمل", "تطلع", "الرمل", "رخو", "صخر", "فتدق", "ميتين", "وثلاثين", "عمود", "خرسانة", "أربعين", "متر",
                      "يمسكها", "جوانبها", "الموج", "بياكل", "الجزيرة", "فتدرّع", "الشط", "مفرّغة", "خلية", "النحل",
                      "قوته", "شمس", "الصحرا", "البهو", "العملاق", "فرن", "فتشد", "قماش", "ألياف", "زجاج", "النور",
                      "الحر", "تابعني", "نخلة", "مهبط", "هليكوبتر", "وعشرة", "التنس", "ثلاثمية", "وواحد", "وعشرين",
                      "أكثر", "بيدك", "بنوا", "وخالك", "حاجز", "وبيتي"]}
    KEYS = {"ar_sa": {
        ("hook", "HOTEL"): "فندق", ("hook", "SAIL"): "شراع", ("hook", "SEA"): "البحر", ("hook", "ISLAND"): "جزيرة",
        ("hook", "MADE"): "سويتها", ("hook", "CONGRATS"): "مبروك", ("hook", "BURJ"): "برج",
        ("break1", "OUT"): "هناك", ("break1", "LAND"): "أرض", ("break1", "SEA"): "بحر",
        ("fix1", "MAKE"): "فتسوي", ("fix1", "RING"): "تحاوط", ("fix1", "ROCKS"): "بصخور", ("fix1", "FILL"): "وتعبّيه",
        ("fix1", "SAND"): "رمل", ("fix1", "RISES"): "تطلع",
        ("break2", "SAND"): "الرمل", ("break2", "SOFT"): "رخو", ("break2", "BEDROCK"): "صخر", ("break2", "TOWER"): "برج",
        ("fix2", "DRIVE"): "فتدق", ("fix2", "TWO"): "ميتين", ("fix2", "PILES"): "عمود", ("fix2", "FORTY"): "أربعين",
        ("fix2", "GRIPS"): "يمسكها", ("fix2", "SIDES"): "جوانبها", ("fix2", "FRICTION"): "جوانبها",
        ("break3", "WAVES"): "الموج", ("break3", "CHEW"): "بياكل", ("break3", "AWAY"): "شوي",
        ("fix3", "ARMOR"): "فتدرّع", ("fix3", "HOLLOW"): "مفرّغة", ("fix3", "HONEYCOMB"): "خلية", ("fix3", "CRASH"): "يدخلها",
        ("fix3", "LOSE"): "ويفقد", ("fix3", "DRAIN"): "قوته",
        ("break4", "DESERT"): "الصحرا", ("break4", "SUN"): "شمس", ("break4", "ATRIUM"): "البهو", ("break4", "OVEN"): "فرن",
        ("fix4", "STRETCH"): "فتشد", ("fix4", "SAIL"): "شراع", ("fix4", "FABRIC"): "قماش", ("fix4", "LIGHT"): "النور",
        ("fix4", "BOUNCES"): "ويرد", ("fix4", "HEAT"): "الحر",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "HELIPAD"): "مهبط", ("reveal", "TWO"): "ميتين", ("reveal", "TENNIS"): "التنس",
        ("reveal", "PLAYED"): "لعب",
        ("stat", "THREE"): "ثلاثمية", ("stat", "ISLAND"): "والجزيرة", ("stat", "HOTEL"): "الفندق",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "GOLD"): "بنوا", ("tag", "HELIPAD"): "فندق", ("tag", "STILL"): "وخالك", ("tag", "SHAMPOO"): "فندق",
        ("tag", "BOTTLES"): "وبيتي"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an island shaped like a palm"),
                   "stat": [("321 m", "TALL"), ("3 yrs", "THE ISLAND"), ("<3 yrs", "THE HOTEL")],
                   "L": {"sail": "A HOTEL SHAPED LIKE A SAIL", "island": "ON AN ISLAND YOU MADE", "name": "THE BURJ AL ARAB",
                         "noland": "NO LAND, JUST SEA", "rocks": "A RING OF ROCKS", "sand": "FILL IT WITH SAND",
                         "rises": "AN ISLAND RISES", "soft": "SAND IS SOFT", "norock": "NO BEDROCK",
                         "piles": "230 CONCRETE PILES", "deep": "40 m DOWN", "grip": "THE SAND GRIPS THEIR SIDES",
                         "fric": "FRICTION HOLDS IT UP", "chew": "WAVES CHEW THE ISLAND", "honey": "HOLLOW HONEYCOMB BLOCKS",
                         "lose": "WAVES LOSE THEIR POWER", "oven": "THE ATRIUM BECOMES AN OVEN", "fabric": "A FABRIC SAIL",
                         "light": "LIGHT IN", "heat": "HEAT OUT", "heli": "HELIPAD: 210 m UP", "tennis": "TENNIS UP THERE",
                         "bottles": "THE TINY SHAMPOO BOTTLES"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: جزيرة على شكل نخلة"),
                      "stat": [("321", "متر علو"), ("3", "سنين للجزيرة"), ("<3", "سنين للفندق")],
                      "L": {"sail": "فندق على شكل شراع", "island": "على جزيرة سويتها بنفسك", "name": "برج العرب",
                            "noland": "ما فيه أرض، كله بحر", "rocks": "صخور حوالين المكان", "sand": "تعبّيه رمل",
                            "rises": "تطلع جزيرة", "soft": "الرمل رخو", "norock": "ما تحته صخر",
                            "piles": "ميتين وثلاثين عمود", "deep": "أربعين متر لتحت", "grip": "الرمل يمسكها من جوانبها",
                            "fric": "الاحتكاك يشيلها", "chew": "الموج ياكل الجزيرة", "honey": "خرسانة مفرّغة مثل خلية النحل",
                            "lose": "الموج يفقد قوته", "oven": "البهو يصير فرن", "fabric": "شراع من قماش",
                            "light": "يدخّل النور", "heat": "ويرد الحر", "heli": "مهبط على علو ميتين وعشرة متر",
                            "tennis": "نجوم التنس لعبوا هنا", "bubble": "فندق؟! وبيتي وش فيه؟"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "hotel": ("hook", "HOTEL", 0.15), "sail": ("hook", "SAIL", 0.3), "sea": ("hook", "SEA", 0.38),
            "island": ("hook", "ISLAND", 0.48), "made": ("hook", "MADE", 0.55), "congrats": ("hook", "CONGRATS", 0.65),
            "burj": ("hook", "BURJ", 0.85),
            "out": ("break1", "OUT", 0.1), "land": ("break1", "LAND", 0.5), "sea1": ("break1", "SEA", 0.85),
            "make": ("fix1", "MAKE", 0.08), "ring": ("fix1", "RING", 0.22), "rocks": ("fix1", "ROCKS", 0.42),
            "fill": ("fix1", "FILL", 0.55), "sand": ("fix1", "SAND", 0.65), "rises": ("fix1", "RISES", 0.9),
            "sand2": ("break2", "SAND", 0.1), "soft": ("break2", "SOFT", 0.22), "bedrock": ("break2", "BEDROCK", 0.5),
            "tower": ("break2", "TOWER", 0.75),
            "drive": ("fix2", "DRIVE", 0.08), "two": ("fix2", "TWO", 0.12), "piles": ("fix2", "PILES", 0.33),
            "forty": ("fix2", "FORTY", 0.4), "grips": ("fix2", "GRIPS", 0.62), "sides": ("fix2", "SIDES", 0.7),
            "friction": ("fix2", "FRICTION", 0.8),
            "waves": ("break3", "WAVES", 0.2), "chew": ("break3", "CHEW", 0.45), "away": ("break3", "AWAY", 0.85),
            "armor": ("fix3", "ARMOR", 0.06), "hollow": ("fix3", "HOLLOW", 0.22), "honey": ("fix3", "HONEYCOMB", 0.42),
            "crash": ("fix3", "CRASH", 0.58), "lose": ("fix3", "LOSE", 0.72), "drain": ("fix3", "DRAIN", 0.88),
            "desert": ("break4", "DESERT", 0.15), "sun": ("break4", "SUN", 0.25), "atrium": ("break4", "ATRIUM", 0.6),
            "oven": ("break4", "OVEN", 0.9),
            "stretch": ("fix4", "STRETCH", 0.08), "sail2": ("fix4", "SAIL", 0.16), "fabric": ("fix4", "FABRIC", 0.3),
            "light": ("fix4", "LIGHT", 0.65), "bounces": ("fix4", "BOUNCES", 0.78), "heat": ("fix4", "HEAT", 0.88),
            "follow": ("cta", "FOLLOW", 0.35),
            "helipad": ("reveal", "HELIPAD", 0.1), "two2": ("reveal", "TWO", 0.22), "tennis": ("reveal", "TENNIS", 0.62),
            "played": ("reveal", "PLAYED", 0.85),
            "s1": ("stat", "THREE", 0.03), "s2": ("stat", "ISLAND", 0.45), "s3": ("stat", "HOTEL", 0.9),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_gold": ("tag", "GOLD", 0.03), "t_heli": ("tag", "HELIPAD", 0.2), "t_still": ("tag", "STILL", 0.5),
            "t_sham": ("tag", "SHAMPOO", 0.7), "t_bot": ("tag", "BOTTLES", 0.85)})
        T["drain0"] = max(T["drain"], T["lose"]) if not self.rtl else T["lose"] + 0.4
        if self.rtl:                                                         # the uncle's own "a hotel?!" (third فندق)
            T["t_sham"] = self.w("tag", "SHAMPOO", 0.7, nth=2)
        # ---- sets
        self.cut(s("break1") - 0.12, "island", 1)
        self.cut(s("break2") - 0.12, "piles", -1)
        self.cut(s("break3") - 0.12, "shore", 1)
        self.cut(s("break4") - 0.12, "sail", -1)
        self.cut(s("reveal") - 0.12, "coast", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- coast camera
        cm = Camera(-10, -330, 1.2)
        cm.key(0.1, -10, -320, 1.16, max(0.5, T["sail"] - 0.2))
        cm.key(T["sail"], -40, -150, 0.92, 1.2)
        cm.key(T["burj"], -40, -160, 0.95, 1.0)
        cm.key(s("reveal") - 0.12, 0, -440, 0.95, 0.0).key(T["helipad"] - 0.2, 80, -520, 1.9, 1.2)
        cm.key(s("stat") - 0.12, -60, -280, 0.8, 0.0).key(s("closer"), -60, -290, 0.84, 3.5)
        cm.key(s("closer") - 0.1, -40, -235, 0.98, 1.0).key(self.duration, -40, -238, 1.0, 4.0)
        self.cam = cm
        self.spans = [(T["sea1"], T["rises"] + 0.3), (T["tower"], T["friction"] + 0.3), (T["away"], T["drain0"] + 0.3),
                      (T["oven"], T["heat"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["sea1"], 0.3, 6), (T["tower"], 0.5, 8), (T["chew"], 0.4, 8),
                       (T["oven"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["t_sham"], 0.3, 6)]

    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    # ------------------------------------------------------------------ set: coast
    def draw_coast(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        night = prog(t, s("closer") - 0.6, s("closer") + 0.6)
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy - 30 * z)
        if night > 0:
            c.save()
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy - 30 * z)
            v2.stars(c, W, H, t, 0.9)
            c.restore()
            c.restore()
        if night < 1:
            sun(c, 900 - cx * 0.05, gy - 150 * z, 60, heat=0.6, a=1 - night)
        self.view(c, cam)
        c.save()
        c.translate(0, -26)
        c.scale(0.42, 0.42)
        skyline(c, -4200, 4200, 0, t, a=0.75)
        c.restore()
        sea_band(c, -3000, 3000, -28, 2000, t)
        if night < 1:
            for k in range(12):                                             # the sun's path on the water
                c.drawRect(R(700 + math.sin(t * 2 + k) * 20 - k * 6, -20 + k * 18, 80 + k * 12, 5), P("#FFD58A", 0.4 * (1 - night)))
        bp = skia.Path()                                                    # the curving bridge to the beach
        bp.moveTo(-250, -18)
        bp.quadTo(-520, -40, -900, -16)
        c.drawPath(bp, P("#D6D3D1", stroke=10))
        for k in range(8):
            u = k / 7.0
            px = lerp(-250, -900, u)
            c.drawLine(px, -16 - 14 * math.sin(u * math.pi), px, 6, P("#A8A29E", stroke=4))
        c.drawRect(R(-1700, -30, 800, 60), P(SAND))                         # the beach on the left
        for x in (-1500, -1300, -1120):
            palm_tree(c, x, -30, 0.9, t)
        island(c, t)
        rv = s("reveal") - 0.12 <= t < s("stat") - 0.12
        hel = prog(t, T["helipad"] - 0.2, T["two2"] + 0.4) if rv else 1.0
        ten = prog(t, T["tennis"] - 0.3, T["tennis"] + 0.2) if rv else 0.0
        if t >= s("stat") - 0.12:
            ten = 0.0
        burj(c, 20, -24, t, s=1.0, lit=night, helipad=hel, tennis=ten)
        if t < s("break1"):                                                 # the island outline glows in the hook
            ik = self.span(T["island"] - 0.2, T["congrats"] + 0.4)
            if ik > 0:
                c.drawPath(path_of([(-340, 60), (-250, -24), (250, -24), (340, 60)]), P(HILITE, ik, stroke=8))
        c.restore()
        self.ui["cam"] = cam

    def ui_coast(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, -300, 0.92))
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "sail", T["hotel"] - 0.1, T["island"] - 0.1, accent="#E2E8F0", size=40)
            self.chip(540, 300, "island", T["island"] - 0.1, T["congrats"] - 0.05, accent=HILITE, size=40)
            self.chip(540, 300, "name", T["burj"] - 0.15, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            hx, hy = self.at(cam, 20 + 170, -24 - 505)
            self.label(hx, hy, 640, 420, "heli", T["helipad"] - 0.1, T["tennis"] - 0.2, GOOD, size=36)
            self.label(hx, hy - 20, 640, 420, "tennis", T["tennis"] - 0.2, s("stat") - 0.15, "#D9F99D", size=38)

    # ------------------------------------------------------------------ set: island (break1, fix1), section
    def draw_island(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=820)
        sun(c, 860, 520, 56, heat=0.5)
        wl = 820
        c.drawRect(R(0, 1100, W, H - 1100), lin_paint(0, 1100, 0, H, ["#7A5E3A", "#3A2A18"]))  # the seabed
        rk = prog(t, T["ring"] - 0.2, T["rocks"] + 0.4) if fixed else 0.0
        sk = prog(t, T["fill"] - 0.2, T["sand"] + 0.5) if fixed else 0.0
        top = lerp(1100, 790, e_out(sk))
        if sk > 0:
            c.drawRect(R(390, top, 300, 1100 - top), lin_paint(0, top, 0, 1100, [SAND, SAND_D]))
            tex(c, R(390, top, 300, 1100 - top), "sand", 0.9, 0.4)
        for k, xr in enumerate((330, 690)):                                 # the ring of rocks, in section
            if rk <= 0:
                continue
            hgt = 330 * e_out(clamp(rk * 1.6 - k * 0.3))
            rp = skia.Path()
            rp.moveTo(xr - 60, 1100)
            rp.lineTo(xr - 20, 1100 - hgt)
            rp.lineTo(xr + 80, 1100 - hgt)
            rp.lineTo(xr + 120, 1100)
            rp.close()
            c.drawPath(rp, P("#6B7280"))
            rng = random.Random(k + 3)
            for _ in range(14):
                yy = rng.uniform(1100 - hgt, 1090)
                c.drawCircle(xr + 30 + rng.uniform(-50, 50) * (1100 - yy) / max(1.0, hgt), yy, rng.uniform(14, 26), P("#9CA3AF"))
        sea_band(c, 0, W, wl, 1100 - wl, t, a=0.82)
        if sk > 0.6:                                                        # the new island above the water
            c.drawRect(R(330, top, 460, wl - top + 4), P(SAND))
            c.drawRect(R(330, top, 460, 8), P("#E5D3B0"))
        if not fixed:
            pk = prog(t, T["out"] - 0.2, T["out"] + 0.3)
            bob = math.sin(t * 2.5) * 10
            c.drawLine(540, wl - 120 + bob, 540, wl + bob, P("#F8FAFC", pk, stroke=6))
            c.drawCircle(540, wl - 140 + bob, 30, P(WARN, pk))
            c.drawCircle(540, wl - 140 + bob, 12, P("#FFFFFF", pk))
        c.drawRect(R(-40, 700, 140, 130), P(SAND))                          # the beach far left
        palm_tree(c, 40, 704, 0.9, t)

    def ui_island(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "noland", T["land"] - 0.2, s("fix1") - 0.15, accent="#7DD3FC", size=44)
            self.badge("alert", T["sea1"] + 0.05, s("fix1") - 0.2, x=920, y=420)
            self.red(T["sea1"] + 0.05, 1.2)
            return
        self.chip(540, 300, "rocks", T["ring"] - 0.1, T["fill"] - 0.15, accent="#CBD5E1", size=44)
        self.chip(540, 300, "sand", T["fill"] - 0.15, T["rises"] - 0.15, accent="#E5D3B0", size=44)
        self.chip(540, 300, "rises", T["rises"] - 0.15, s("break2") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["rises"] + 0.2, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: piles (break2, fix2), section
    def draw_piles(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        vrect(c, 0, 0, W, H, ["#0B1A3A", "#1E3A6E"])
        top = 620
        for k in range(6):                                                  # sand layers down to the bottom
            y0 = top + k * 230
            c.drawRect(R(0, y0, W, 232), P(mix("#A8834E", "#3A2A18", k / 6.0)))
            for j in range(40):
                c.drawCircle((j * 97 + k * 31) % W, y0 + 30 + (j * 53) % 180, 3, P("#3A2A18", 0.35))
        c.drawRect(R(0, top - 14, W, 16), P("#E5D3B0"))
        sink = prog(t, T["soft"] - 0.2, T["tower"] + 0.6) if not fixed else 0.0
        if fixed:
            sink = 1 - prog(t, T["friction"] - 0.3, T["friction"] + 0.5)
        tilt = 7 * sink
        c.save()                                                            # the tower on the island, sinking
        c.translate(540, top + 120 * sink)
        c.rotate(tilt)
        c.scale(0.62, 0.62)
        burj(c, 0, 0, t, helipad=1.0)
        c.restore()
        if not fixed:
            bk = prog(t, T["bedrock"] - 0.3, T["bedrock"] + 0.2)
            c.drawLine(80, 1800, 1000, 1800, dash_paint("#F8FAFC", 0.6 * bk, w=5, t=t))
            if bk > 0:
                c.drawRRect(rr(470, 1700, 140, 70, 20), P("#6B7280", bk))   # no rock: crossed out
                c.drawLine(470, 1690, 610, 1780, P(WARN, bk, stroke=12))
                c.drawLine(610, 1690, 470, 1780, P(WARN, bk, stroke=12))
        else:
            n = 11
            for i in range(n):
                px = 260 + i * 56
                dk = e_out(prog(t, T["drive"] - 0.2 + i * 0.12, T["drive"] + 0.4 + i * 0.12))
                L_ = 1000 * dk
                c.drawRect(R(px - 12, top, 24, L_), lin_paint(px - 12, 0, px + 12, 0, ["#D1D5DB", "#9CA3AF", "#6B7280"]))
                gk = prog(t, T["grips"] - 0.3, T["sides"] + 0.2)
                if gk > 0 and i % 2 == 0:
                    for j in range(6):
                        yy = top + 120 + j * 150
                        if yy < top + L_:
                            c.drawLine(px - 34, yy + 10, px - 16, yy, P("#FDE68A", gk, stroke=4))
                            c.drawLine(px + 34, yy + 10, px + 16, yy, P("#FDE68A", gk, stroke=4))
                fk = prog(t, T["friction"] - 0.3, T["friction"] + 0.3)
                if fk > 0 and i % 2 == 1:
                    for j in range(3):
                        q = (t * 0.8 + j / 3.0) % 1.0
                        yy = top + L_ - q * L_ * 0.9
                        arrow(c, px, yy + 40, px, yy - 10, GOOD, a=fk * (1 - q * 0.5), w=8, head=20)
            dk = prog(t, T["forty"] - 0.3, T["forty"] + 0.3)
            if dk > 0:
                c.drawLine(990, top, 990, top + 1000, P(HILITE, dk, stroke=6))
                c.drawLine(970, top + 1000, 1010, top + 1000, P(HILITE, dk, stroke=6))
        self.ui["fixed"] = fixed

    def ui_piles(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "soft", T["soft"] - 0.2, T["bedrock"] - 0.2, accent="#E5D3B0", size=44)
            self.chip(540, 300, "norock", T["bedrock"] - 0.2, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["tower"] + 0.05, s("fix2") - 0.2, x=920, y=420)
            self.red(T["tower"] + 0.05, 1.2)
            return
        self.chip(540, 300, "piles", T["drive"] - 0.1, T["forty"] - 0.15, accent="#E5E7EB", size=44)
        self.chip(540, 300, "deep", T["forty"] - 0.15, T["grips"] - 0.2, accent=HILITE, size=46)
        self.chip(540, 300, "grip", T["grips"] - 0.2, T["friction"] - 0.2, accent="#FDE68A", size=38)
        self.chip(540, 300, "fric", T["friction"] - 0.2, s("break3") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["friction"] + 0.3, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: shore (break3, fix3)
    def draw_shore(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=760)
        wl = 900
        er = prog(t, T["chew"] - 0.3, T["away"] + 0.5) if not fixed else 0.0
        sl = skia.Path()                                                    # the island's slope, eaten away
        sl.moveTo(-50, 760)
        sl.lineTo(420 - 160 * er, 760 + 30 * er)
        sl.lineTo(880 - 120 * er, 1300)
        sl.lineTo(1000, H + 50)
        sl.lineTo(-50, H + 50)
        sl.close()
        c.drawPath(sl, lin_paint(0, 760, 0, 1500, ["#B08A55", "#5A4228"]))
        tex(c, sl, "sand", 0.9, 0.4)
        c.drawRect(R(-50, 754, 420 - 160 * er + 50, 10), P("#E5D3B0"))
        burj(c, 120, 760, t, s=0.5)
        if fixed:
            hk = prog(t, T["armor"] - 0.2, T["honey"] + 0.4)
            n = 0
            for j in range(5):                                              # honeycomb blocks laid up the slope
                for i in range(4):
                    u = (j + 0.5) / 5.0
                    bx = lerp(430, 860, u) + (i - 1.5) * 26 + (j % 2) * 13
                    by = lerp(780, 1260, u) - i * 46 + 30
                    if hk * 20 > n:
                        hexagon(c, bx, by, 34, a=clamp(hk * 20 - n))
                    n += 1
        sea = skia.Path()
        sea.moveTo(W + 50, wl)
        xs = lerp(420 - 160 * er, 880 - 120 * er, (wl - (760 + 30 * er)) / (1300 - (760 + 30 * er)))
        sea.lineTo(xs - 4, wl)
        sea.lineTo(880 - 120 * er - 4, 1300)
        sea.lineTo(1000, H + 50)
        sea.lineTo(W + 50, H + 50)
        sea.close()
        c.drawPath(sea, lin_paint(0, wl, 0, 1500, ["#2A8AAE", SEA_D], a=0.92))
        q = (t * 0.5) % 1.0                                                 # waves rolling in
        wx = lerp(1150, 640, q)
        wk = 1.0 if not fixed else 1 - 0.6 * prog(t, T["lose"] - 0.3, T["lose"] + 0.3)
        wave(c, wx, wl - 120 * wk, 260, 130 * wk, t, k=wk)
        if q > 0.75:                                                        # the hit: splash, then drain or erode
            hit = (q - 0.75) / 0.25
            v2.puff(c, 620, wl - 60, 40 + 120 * hit, "#E0F7FF", 0.7 * (1 - hit), k=2)
            if not fixed:
                for k in range(8):
                    c.drawCircle(560 - k * 20 + hit * 60, wl + 20 + k * 10 + hit * 80, 8, P(SAND_D, 1 - hit))
            else:
                dk = prog(t, T["drain0"] - 0.4, T["drain0"] + 0.2)
                for k in range(6):
                    c.drawLine(600 + k * 30, wl + 40, 640 + k * 30, wl + 140 * hit, P("#BDEBFF", 0.6 * (1 - hit) * max(dk, 0.3), stroke=5))

    def ui_shore(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "chew", T["waves"] - 0.15, s("fix3") - 0.15, accent="#7DD3FC", size=44)
            self.badge("alert", T["away"] + 0.05, s("fix3") - 0.2, x=920, y=420)
            self.red(T["away"] + 0.05, 1.2)
            return
        self.chip(540, 300, "honey", T["armor"] - 0.1, T["lose"] - 0.3, accent="#CBD5E1", size=36)
        self.chip(540, 300, "lose", T["lose"] - 0.3, s("break4") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["drain0"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: sail (break4, fix4), the atrium
    def draw_sail(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#3A2A5A", "#1A1238"])
        ap = skia.Path()                                                    # the atrium: a tall V of balconies
        ap.moveTo(170, 1240)
        ap.lineTo(470, 420)
        ap.lineTo(610, 420)
        ap.lineTo(910, 1240)
        ap.close()
        c.drawPath(ap, lin_paint(0, 420, 0, 1240, ["#2A2050", "#4A3A7A"]))
        for k in range(18):                                                 # balcony rows, gold edges
            y = 1220 - k * 45
            u = (1240 - y) / 820.0
            xl, xr = lerp(170, 470, u), lerp(910, 610, u)
            c.drawLine(xl, y, xl + 60, y, P("#E2B04A", 0.9, stroke=6))
            c.drawLine(xr - 60, y, xr, y, P("#E2B04A", 0.9, stroke=6))
            c.drawRect(R(xl - 40, y - 30, 40, 26), P("#3B82F6", 0.5))
            c.drawRect(R(xr, y - 30, 40, 26), P("#3B82F6", 0.5))
        sx_, sy_ = 960, 300
        hk = 1.0 if not fixed else 1 - prog(t, T["bounces"] - 0.3, T["heat"] + 0.3)
        sun(c, sx_, sy_, 70, heat=1.0)
        for k in range(5):                                                  # sun rays into the atrium
            c.drawLine(sx_ - 40, sy_ + 40, 400 + k * 70, 1150 - k * 40, P("#FFD58A", 0.25 * (0.5 + 0.5 * hk), stroke=10))
        if hk > 0:
            c.drawRect(R(0, 0, W, H), P("#F97316", 0.18 * hk * prog(t, T["sun"] - 0.3, T["atrium"])))
            heat_lines(c, 250, 830, 600, 1180, t, a=hk * prog(t, T["sun"] - 0.3, T["atrium"]))
        thermo(c, 140, 900, 1.5, lerp(0.45, 0.98, prog(t, T["atrium"] - 0.3, T["oven"] + 0.2)) if not fixed else
               lerp(0.98, 0.45, prog(t, T["bounces"] - 0.3, T["heat"] + 0.4)), a=1.0)
        for k, (px, col) in enumerate(((420, "#2563EB"), (560, "#DB2777"), (680, "#F59E0B"))):
            person(c, px, 1240, 110, col, t + k, pose="look", face=1, hat="none", hair="#1C1917")
            if not fixed and k == 1:
                for j in range(3):
                    q = (t * 1.3 + j * 0.33) % 1.0
                    c.drawCircle(px + (j - 1) * 12, 1240 - 102 + q * 30, 4, P("#93C5FD", 1 - q))
        if fixed:
            fk = prog(t, T["stretch"] - 0.2, T["fabric"] + 0.4)             # the fabric sail stretches across the front
            if fk > 0:
                fp = skia.Path()
                fp.moveTo(170, 1240)
                fp.quadTo(380, 820, 540, 420)
                fp.lineTo(540 + 370 * fk, 420 + 820 * fk)
                fp.quadTo(540 + 200 * fk, 830, 170 + 740 * fk, 1240)
                fp.close()
                c.drawPath(fp, P("#E2E8F0", 0.42 * fk))
                for k in range(1, 9):
                    c.drawLine(170 + k * 20, 1240 - k * 100, 170 + 740 * fk - k * 20, 1240 - k * 100, P("#F8FAFC", 0.25 * fk, stroke=3))
            lk = prog(t, T["light"] - 0.3, T["light"] + 0.3)
            if lk > 0:
                add_glow(c, 540, 820, 380, "#FFF1C9", 0.35 * lk)
            bk = prog(t, T["bounces"] - 0.3, T["bounces"] + 0.3)
            for k in range(3):                                              # heat arrows bouncing off
                if bk > 0:
                    yy = 560 + k * 200
                    xx = 760 + k * 40
                    arrow(c, 1040, yy - 140, xx, yy, WARN, a=bk * 0.6, w=10, head=26)
                    arrow(c, xx, yy, 1060, yy + 120, WARN, a=bk, w=12, head=30)

    def ui_sail(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "oven", T["sun"] - 0.1, s("fix4") - 0.15, accent="#FB923C", size=40)
            self.badge("alert", T["oven"] + 0.05, s("fix4") - 0.2, x=920, y=420)
            self.red(T["oven"] + 0.05, 1.2)
            return
        self.chip(540, 300, "fabric", T["stretch"] - 0.1, T["light"] - 0.2, accent="#E2E8F0", size=44)
        self.chip(370, 300, "light", T["light"] - 0.2, s("cta") - 0.15, accent="#FDE68A", size=42)
        self.chip(720, 300, "heat", T["bounces"] - 0.2, s("cta") - 0.15, accent=WARN, size=42)
        self.badge("check", T["heat"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:                                                    # the tiny shampoo bottles
            vrect(c, 0, 0, W, H, ["#5A4416", "#3A2A10"])
            for k in range(7):                                              # gold leaf walls
                c.drawRect(R(k * 160, 0, 150, 1100), lin_paint(k * 160, 0, k * 160 + 150, 0, ["#8A6420", "#B8903A", "#7A5418"]))
            c.drawRect(R(0, 1100, W, H - 1100), P("#2A1E10"))
            c.drawRRect(rr(180, 760, 720, 420, 40), P("#1F2937"))           # the open suitcase
            c.drawRRect(rr(200, 780, 680, 380, 30), P("#374151"))
            c.drawRRect(rr(180, 560, 720, 230, 40), P("#111827"))
            gk = prog(t, T["t_still"] - 0.3, T["t_bot"] + 0.4)
            n = int(14 * gk)
            for k in range(n):
                shampoo(c, 260 + (k % 7) * 90, 1060 - (k // 7) * 90, 1.8, ["#F472B6", "#60A5FA", "#FBBF24", "#34D399"][k % 4],
                        rot=(k * 17) % 30 - 15)
            hx = lerp(1100, 700, prog(t, T["t_still"] - 0.4, T["t_still"]))
            c.drawRRect(rr(hx, 900, 300, 70, 30), P("#C68B59"))             # a hand dropping one more in
            shampoo(c, hx + 30, 900, 1.5, "#F472B6", rot=-20)
            if gk >= 1:
                for k in range(3):
                    add_glow(c, 300 + k * 240, 960, 50, "#FDE68A", 0.3)
        else:                                                               # the uncle: "a hotel?!"
            vrect(c, 0, 0, W, H, ["#A8804E", "#8A6438"])
            c.drawRect(R(0, 1180, W, H - 1180), P("#6B4A2A"))
            c.drawRect(R(280, 420, 520, 760), P("#8A5A30"))                 # his door
            c.drawRect(R(300, 440, 480, 740), P("#5A3418"))
            for k in range(3):
                c.drawRect(R(330 + k * 150, 480, 120, 300), P("#7A4A24"))
            c.drawCircle(740, 820, 14, P("#E2B04A"))
            uk = prog(t, T["t_still"] - 0.3, T["t_still"])
            saudi_man(c, 540, 1180, 380, t, pose="cheer" if t < T["t_sham"] else "shrug", face=1, a=max(0.0, uk))

    def ui_tag(self, c, t, tw):
        T = self.T
        if self.rtl:
            k = self.span(T["t_sham"] - 0.2, self.duration + 1)
            if k > 0:
                kk = e_back(clamp(k))
                c.save()
                c.translate(560, 340)
                c.scale(kk, kk)
                lab = self.L["bubble"]
                wdt = arabic.width_ar(lab, 48 * 1.15, "Tajawal-Black") + 80
                c.drawRRect(rr(-wdt / 2, -64, wdt, 118, 50), P("#F8FAFC"))
                c.drawRRect(rr(-wdt / 2, -64, wdt, 118, 50), P("#1F2937", stroke=4))
                tp = skia.Path()
                tp.moveTo(-30, 52)
                tp.lineTo(10, 52)
                tp.lineTo(-20, 120)
                tp.close()
                c.drawPath(tp, P("#F8FAFC"))
                word(c, lab, 0, 14, 48, "#111827")
                c.restore()
        else:
            self.chip(540, 300, "bottles", T["t_sham"] - 0.2, self.duration + 1, accent="#F472B6", size=40)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["island"]), 61), -18), (T["sail"], sfx.whoosh(0.5, False, 62), -12),
              (T["sea"], sfx.hiss(0.8, 63), -14), (T["island"], sfx.sparkle(0.7, 9, 64), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8),
              (T["burj"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (s("break1"), sfx.hiss(2.4, 68), -14),
               (T["out"], sfx.pop(69), -8), (T["sea1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 70), -4), (T["rocks"], sfx.thud(0.4, 71), -8),
               (T["rocks"] + 0.3, sfx.thud(0.4, 72), -8), (T["sand"], sfx.hiss(1.0, 73), -12),
               (T["rises"], sfx.ding(), -8), (T["rises"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["soft"], sfx.creak(0.8), -12),
               (T["tower"], sfx.thud(0.5, 75), -8), (T["tower"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 76), -4)]
        for k in range(8):
            ev.append((T["drive"] + k * 0.24, sfx.clank(420.0, 0.25, 77 + k), -14))
        ev += [(T["grips"], sfx.whirr(0.6, 200.0, 260.0, 85), -16), (T["friction"] + 0.3, sfx.ding(), -8),
               (T["friction"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 86), -4), (T["waves"], sfx.hiss(1.2, 87), -8),
               (T["chew"], sfx.thud(0.4, 88), -10), (T["away"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 89), -4)]
        for k in range(5):
            ev.append((T["armor"] + k * 0.2, sfx.tap(90 + k), -12))
        ev += [(T["crash"], sfx.hiss(0.9, 95), -10), (T["drain0"] + 0.1, sfx.ding(), -8), (T["drain0"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 96), -4), (T["sun"], sfx.sizzle(0.8, 97), -12),
               (T["oven"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 98), -4), (T["stretch"], sfx.whoosh(0.7, False, 99), -12),
               (T["light"], sfx.sparkle(0.7, 10, 100), -10), (T["bounces"], sfx.pop(101), -8),
               (T["heat"] + 0.1, sfx.ding(), -8), (T["heat"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(102), 0), (T["follow"] - 0.15, sfx.pop(103), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 104), -6), (T["helipad"], sfx.whirr(0.8, 300.0, 420.0, 105), -14),
               (T["tennis"], sfx.tap(106), -6), (T["tennis"] + 0.5, sfx.tap(107), -6), (T["played"], sfx.tap(108), -6)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 109), -6), (T["s1"], sfx.pop(110), -3), (T["s2"], sfx.pop(111), -3),
               (T["s3"], sfx.pop(112), -3)]
        ev += [(T["cong2"], sfx.pop(113), -2), (T["cong2"], sfx.sparkle(1.0, 14, 114), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 115), -6), (T["t_still"], sfx.pop(116), -8),
               (T["t_sham"], sfx.pop(117), -6)]
        return ev


NAME = "burjalarab"
EPISODE = BurjAlArab
