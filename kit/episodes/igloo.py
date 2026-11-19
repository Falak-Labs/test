"""Episode 47 - An igloo.  v2 look: a snowfield in the Arctic night under a green aurora, the igloo glowing warm from
inside.

Sets: tundra (hook: a blizzard at minus forty, the igloo turns into a cutaway and a family sits warm inside around a
lamp; stat; closer), wind (break1: a hunter in the wind, frost creeping over the face in minutes), blocks (fix1:
blocks cut from wind-packed snow with a snow knife; a magnifier shows a block is mostly trapped air, like a down
jacket), build (break2: a flat white plain with no trees, a roof slab falls in; fix2: the blocks go up in a rising
spiral, each leaning on the last, and the dome closes itself), cut (break3/fix3/break4/fix4/reveal: the igloo in
section: warm air rises and the cold rushes in at a floor-level door; the doorway dug below the floor, cold air pooling
in the tunnel, the family asleep up high; drips from the melting wall; the melt refreezes into a skin of ice and
someone stands on top; the lamp, the air hole and the window of clear ice), tag (English: mom holding out a jacket on
a mild day; Arabic: a desert night at twenty degrees, the fur cloak and a fire).
World (tundra, cut, build): side view, the snow surface at y = 0, the dome centred on x = 0 (radius 300, height 320),
the tunnel to the right.
"""
from v2_base import *  # noqa: F401,F403
from falaj import word  # noqa: E402
from windtower import thermo, readout, arrow  # noqa: E402
from barrier import dallah  # noqa: E402

ARCTIC = {"top": "#020617", "upper": "#071233", "mid": "#0E2350", "low": "#1E3A6A", "horizon": "#3B6A94",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SNOW, SNOW_D = "#C3D3E6", "#7F9AB8"
ICE = "#BFE3F7"
WARM = "#FDBA74"
RX, RY = 300.0, 320.0


# ====================================================================================== pieces
def dome_y(x):
    """Height of the dome's outer surface at x (an ellipse arch, close to the catenary of a real igloo)."""
    u = clamp(1 - (x / RX) ** 2, 0.0, 1.0)
    return -RY * math.sqrt(u)


def aurora(c, t, a=1.0, y0=330, amp=1.0):
    """Green aurora curtains across the screen sky."""
    if a <= 0:
        return
    for band, (col, off, hgt) in enumerate((("#34D399", 0.0, 260), ("#22D3EE", 1.7, 200), ("#A7F3D0", 3.1, 150))):
        for i in range(60):
            x = i * 19 - 20
            yb = y0 + band * 60 + 70 * math.sin(x / 210.0 + t * 0.35 + off) * amp + 30 * math.sin(x / 70.0 + t * 0.8 + off)
            hh = hgt * (0.6 + 0.4 * math.sin(x / 90.0 + t * 0.5 + off * 2))
            c.drawRect(R(x, yb - hh, 21, hh), lin_paint(0, yb - hh, 0, yb, [(col, 0.0), (col, 0.16 * a), (col, 0.5 * a)]))
        add_glow(c, W / 2, y0 + band * 60, 520, col, 0.12 * a)


def blizzard(c, t, a=1.0, n=90, slant=0.5, speed=1.2, seed=3):
    if a <= 0:
        return
    rng = random.Random(seed)
    for i in range(n):
        x0, y0, sp = rng.uniform(-200, W + 200), rng.uniform(-100, H), rng.uniform(0.7, 1.3)
        q = (t * speed * sp + rng.random()) % 1.0
        x = (x0 + q * 1400) % (W + 400) - 200
        y = (y0 + q * 1400 * slant) % (H + 200) - 100
        c.drawLine(x, y, x - 46 * sp, y - 46 * sp * slant, P("#E0F2FE", 0.55 * a, stroke=3))


def ice_hills(c, cam, a=1.0):
    cx, cy, z = cam
    gy = (0 - cy) * z + H / 2
    c.save()
    c.translate(W / 2 - cx * 0.05, gy - 10)
    v2.ridge(c, -1700, 1700, 0, 160 * z, "#5E7FA8", "#2C4566", seed=41, step=120, rough=0.5, a=a)
    c.restore()
    return gy


def snowfield(c, x0, x1, a=1.0):
    c.drawRect(R(x0, 0, x1 - x0, 3000), lin_paint(0, 0, 0, 900, ["#AFC3DA", "#8EA7C4", "#5A7396"], a=a))
    rng = random.Random(6)
    for k in range(40):
        x = rng.uniform(x0, x1)
        y = rng.uniform(10, 600)
        c.drawOval(R(x - 60, y - 6, 120, 12), P("#D6E2EF", 0.3 * a))


def dome_path(r_out=1.0):
    p = skia.Path()
    n = 40
    for i in range(n + 1):
        x = lerp(-RX, RX, i / float(n)) * r_out
        y = dome_y(x / r_out) * r_out
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close()
    return p


def igloo_outside(c, t, a=1.0, glow=1.0, built=1.0, seams=1.0, window=0.0, hole=0.0, steam=0.0):
    """The igloo seen from outside: dome of snow blocks with spiral seams, the tunnel to the right, warm light."""
    if a <= 0:
        return
    dp = dome_path()
    c.save()
    if built < 1:
        c.clipRect(R(-2000, -RY * built - 4, 4000, 4000))
    c.drawPath(dp, rad_paint(-90, -230, 460, ["#DCE6F2", "#BFD0E4", "#93ABC7", "#6E88A8"], [0.0, 0.35, 0.8, 1.0], a=a))
    if seams > 0:                                                           # the rising spiral of blocks
        c.save()
        c.clipPath(dp, doAntiAlias=True)
        for r in range(9):
            y0 = -r * 38
            c.drawLine(-RX, y0 - 4, RX, y0 - 34, P("#8FA9C6", 0.75 * seams * a, stroke=3))
            hw = math.sqrt(max(0.0, 1 - ((y0 - 20) / -RY) ** 2)) * RX if y0 > -RY else 0
            nb = max(2, int(hw / 55))
            for j in range(nb * 2 + 1):
                xx = -hw + j * (2 * hw / max(1, nb * 2)) + (r % 2) * 20
                yy = y0 - 4 - 30 * (xx + RX) / (2 * RX)
                c.drawLine(xx, yy, xx + 4, yy - 34, P("#8FA9C6", 0.6 * seams * a, stroke=2.5))
        c.restore()
    c.restore()
    tp = skia.Path()                                                        # the entrance tunnel
    tp.moveTo(200, 0)
    tp.lineTo(200, -110)
    tp.cubicTo(260, -150, 420, -150, 480, -110)
    tp.lineTo(480, 0)
    tp.close()
    c.drawPath(tp, lin_paint(0, -150, 0, 0, ["#D2DEEC", "#98AECA"], a=a))
    c.drawOval(R(452, -104, 56, 104), P("#1E293B", a))
    if glow > 0:
        c.drawOval(R(458, -96, 44, 96), P(WARM, 0.85 * glow * a))
        add_glow(c, 480, -50, 120, WARM, 0.6 * glow * a)
    if window > 0:
        c.drawRRect(rr(-150, -190, 92, 70, 12), lin_paint(-150, -190, -58, -120, ["#E0F2FE", WARM], a=window * a))
        c.drawRRect(rr(-150, -190, 92, 70, 12), P("#FFFFFF", 0.8 * window * a, stroke=4))
        add_glow(c, -104, -155, 90, WARM, 0.6 * window * glow * a)
    if hole > 0:
        c.drawOval(R(-20, -RY - 6, 40, 14), P("#1E293B", hole * a))
    if steam > 0:
        for k in range(5):
            q = (t * 0.6 + k / 5.0) % 1.0
            c.drawCircle(0 + math.sin(t + k) * 12, -RY - 20 - q * 160, 14 + 20 * q, P("#F8FAFC", 0.45 * steam * (1 - q) * a))


def hood_person(c, x, y, h, col, t, pose="sit", face=1, a=1.0, frost=0.0):
    """Someone in a parka with a fur-trimmed hood."""
    person(c, x, y, h, col, t, pose=pose, face=face, hat="beanie", hair="#1C1917", skin="#C68B59", pants="#3F3F46", a=a)
    u = h / 140.0
    sq = 0.64 if pose == "duck" else 1.0
    if pose == "sit":
        hy = y - 127 * u + 12 * u
    else:
        hy = y - 127 * u * sq
    c.drawCircle(x, hy, 23 * u, P("#E7D5B8", a, stroke=7 * u))
    c.drawCircle(x, hy, 27 * u, P("#B4A189", 0.6 * a, stroke=3 * u))
    if frost > 0:
        for k in range(9):
            an = k * 0.7
            c.drawCircle(x + math.cos(an) * 10 * u * (k % 3) / 2.0, hy + math.sin(an) * 9 * u * (k % 3) / 2.0,
                         5 * u * frost, P("#F0F9FF", 0.85 * frost * a))
    return hy


def lamp(c, x, y, s, lit, t, a=1.0):
    """A qulliq: the half-moon soapstone lamp with a row of small flames."""
    lp = skia.Path()
    lp.moveTo(x - 60 * s, y)
    lp.quadTo(x, y + 40 * s, x + 60 * s, y)
    lp.close()
    c.drawPath(lp, lin_paint(x - 60 * s, 0, x + 60 * s, 0, ["#9CA3AF", "#6B7280"], a=a))
    c.drawLine(x - 60 * s, y, x + 60 * s, y, P("#4B5563", a, stroke=4 * s))
    if lit > 0:
        for k in range(6):
            fx_ = x - 45 * s + k * 18 * s
            hh = (16 + 6 * math.sin(t * 13 + k * 2)) * s * lit
            c.drawOval(R(fx_ - 5 * s, y - hh, 10 * s, hh), P("#FDE68A", a))
        add_glow(c, x, y - 14 * s, 260 * s * lit, WARM, 0.75 * lit * a)


def magnifier(c, x, y, r, t, a=1.0):
    """A close look into a snow block: thin ice grains and a lot of air between them."""
    if a <= 0:
        return
    c.save()
    pth = skia.Path()
    pth.addCircle(x, y, r)
    c.clipPath(pth, doAntiAlias=True)
    c.drawRect(R(x - r, y - r, 2 * r, 2 * r), P("#0B1736", 0.92 * a))
    rng = random.Random(9)
    for k in range(28):
        gx, gy_ = x + rng.uniform(-r, r), y + rng.uniform(-r, r)
        ang = rng.uniform(0, math.pi)
        L_ = rng.uniform(16, 34)
        for j in range(3):
            an = ang + j * math.pi / 3
            c.drawLine(gx - math.cos(an) * L_ / 2, gy_ - math.sin(an) * L_ / 2, gx + math.cos(an) * L_ / 2,
                       gy_ + math.sin(an) * L_ / 2, P("#E0F2FE", 0.95 * a, stroke=3))
    for k in range(14):                                                     # pockets of air
        ax, ay = x + rng.uniform(-r * 0.8, r * 0.8), y + rng.uniform(-r * 0.8, r * 0.8)
        c.drawCircle(ax, ay + math.sin(t * 2 + k) * 3, rng.uniform(8, 16), P("#7DD3FC", 0.35 * a, stroke=2))
    c.restore()
    c.drawCircle(x, y, r, P("#E2E8F0", a, stroke=12))
    c.drawLine(x + r * 0.72, y + r * 0.72, x + r * 1.15, y + r * 1.15, P("#E2E8F0", a, stroke=22))


def jacket_icon(c, x, y, s, a=1.0, col="#EF4444"):
    if a <= 0:
        return
    bp = skia.Path()
    bp.moveTo(x - 60 * s, y - 70 * s)
    bp.lineTo(x - 110 * s, y + 40 * s)
    bp.lineTo(x - 80 * s, y + 52 * s)
    bp.lineTo(x - 56 * s, y)
    bp.lineTo(x - 56 * s, y + 90 * s)
    bp.lineTo(x + 56 * s, y + 90 * s)
    bp.lineTo(x + 56 * s, y)
    bp.lineTo(x + 80 * s, y + 52 * s)
    bp.lineTo(x + 110 * s, y + 40 * s)
    bp.lineTo(x + 60 * s, y - 70 * s)
    bp.close()
    c.drawPath(bp, lin_paint(x - 110 * s, 0, x + 110 * s, 0, [shade(col, -0.2), col, shade(col, -0.3)], a=a))
    for k in range(4):
        c.drawLine(x - 56 * s, y - 40 * s + k * 34 * s, x + 56 * s, y - 40 * s + k * 34 * s, P(shade(col, -0.35), a, stroke=4 * s))
    c.drawLine(x, y - 70 * s, x, y + 90 * s, P("#F8FAFC", 0.8 * a, stroke=4 * s))


def tree_icon(c, x, y, s, a=1.0):
    c.drawRect(R(x - 10 * s, y - 20 * s, 20 * s, 60 * s), P("#78350F", a))
    for k in range(3):
        tp = skia.Path()
        tp.moveTo(x, y - 150 * s + k * 40 * s)
        tp.lineTo(x - (50 + k * 14) * s, y - 60 * s + k * 34 * s)
        tp.lineTo(x + (50 + k * 14) * s, y - 60 * s + k * 34 * s)
        tp.close()
        c.drawPath(tp, P("#15803D", a))


def fur_cloak(c, x, y, h, a=1.0):
    """A farwa: the long winter cloak with a wool collar, drawn over someone standing at (x, y)."""
    if a <= 0:
        return
    u = h / 140.0
    cp = skia.Path()
    cp.moveTo(x - 26 * u, y - 112 * u)
    cp.lineTo(x - 40 * u, y - 6 * u)
    cp.lineTo(x + 40 * u, y - 6 * u)
    cp.lineTo(x + 26 * u, y - 112 * u)
    cp.close()
    c.drawPath(cp, lin_paint(x - 40 * u, 0, x + 40 * u, 0, ["#7C4A21", "#A0612D", "#6B3F1D"], a=a))
    for sd in (-1, 1):
        c.drawLine(x + sd * 26 * u, y - 110 * u, x + sd * 34 * u, y - 10 * u, P("#F5E6C8", a, stroke=8 * u))
    c.drawLine(x - 24 * u, y - 112 * u, x + 24 * u, y - 112 * u, P("#F5E6C8", a, stroke=10 * u))


# ====================================================================================== the episode
class Igloo(EpisodeV2):
    BUILD_NO = 47
    FIRST_SET = "tundra"
    CLEAR = "#020617"
    TITLE = {"en": "IGLOO", "ar_sa": "بيت ثلج"}
    EMPH = {"en": ["CONGRATS", "FAMILY", "WARM", "MINUS", "FORTY", "NOTHING", "SNOW", "IGLOO", "WIND", "FREEZE", "SKIN",
                   "MINUTES", "CUT", "BLOCKS", "WIND-PACKED", "TRAPPED", "AIR", "HOLDS", "HEAT", "DOWN", "JACKET",
                   "TREES", "ROOF", "RISING", "SPIRAL", "LEANING", "DOME", "ITSELF", "RISES", "DOOR", "COLD", "RUSHES",
                   "DIG", "DOORWAY", "BELOW", "FLOOR", "SINKS", "TUNNEL", "STAYS", "SLEEP", "HIGH", "BODY", "MELTS",
                   "WALLS", "DRIP", "CAVE", "TRICK", "REFREEZES", "ICE", "STRONGER", "STAND", "FOLLOW", "MOROCCAN",
                   "RIAD", "SEAL-OIL", "LAMP", "HOLE", "TOP", "WINDOW", "CLEAR", "OUTSIDE", "ABOVE", "FREEZING",
                   "INSIDE", "SKILLED", "HOUR", "YOURSELF", "MOM", "CASE"],
            "ar_sa": ["مبروك", "دفّيت", "عيلة", "سالب", "أربعين", "بالثلج", "بيت", "ثلج", "الريح", "تجمّد", "جلدك", "دقايق",
                      "فتقص", "طوب", "دكّته", "محبوس", "والهوا", "الدفا", "الجاكيت", "شجر", "السقف", "فترص", "لولبي",
                      "مايلة", "والقبة", "نفسها", "الحار", "يطلع", "الباب", "البرد", "فتحفر", "المدخل", "أوطى", "ينزل",
                      "ويقعد", "تنام", "فوق", "حرارتك", "تذوّب", "الجدار", "يقطّر", "ويطيح", "السر", "يتجمّد", "جليد",
                      "تقوى", "توقف", "تابعني", "رياض", "مغربي", "ولّع", "سراج", "خرم", "شباك", "صافي", "برا", "الصفر",
                      "ساعة", "بيدك", "ينامون", "دافين", "عشرين", "الفروة", "وشبّينا", "النار"]}
    KEYS = {"ar_sa": {
        ("hook", "FAMILY"): "عيلة", ("hook", "WARM"): "دفّيت", ("hook", "MINUS"): "سالب", ("hook", "FORTY"): "أربعين",
        ("hook", "NOTHING"): "بس", ("hook", "SNOW"): "بالثلج", ("hook", "CONGRATS"): "مبروك", ("hook", "IGLOO"): "بيت",
        ("break1", "WIND"): "الريح", ("break1", "FREEZE"): "تجمّد", ("break1", "SKIN"): "جلدك", ("break1", "MINUTES"): "دقايق",
        ("fix1", "CUT"): "فتقص", ("fix1", "BLOCKS"): "طوب", ("fix1", "WIND"): "دكّته", ("fix1", "TRAPPED"): "محبوس",
        ("fix1", "AIR"): "هوا", ("fix1", "HEAT"): "الدفا", ("fix1", "JACKET"): "الجاكيت",
        ("break2", "TREES"): "شجر", ("break2", "NOTHING"): "شي", ("break2", "ROOF"): "السقف", ("break2", "BUILD"): "تبني",
        ("fix2", "LAY"): "فترص", ("fix2", "BLOCKS"): "الطوب", ("fix2", "SPIRAL"): "لولبي", ("fix2", "LEANING"): "مايلة",
        ("fix2", "DOME"): "والقبة", ("fix2", "ITSELF"): "نفسها",
        ("break3", "WARM"): "الحار", ("break3", "RISES"): "يطلع", ("break3", "DOOR"): "الباب", ("break3", "COLD"): "البرد",
        ("break3", "RUSHES"): "دخل",
        ("fix3", "DIG"): "فتحفر", ("fix3", "DOORWAY"): "المدخل", ("fix3", "BELOW"): "أوطى", ("fix3", "SINKS"): "ينزل",
        ("fix3", "TUNNEL"): "فيه", ("fix3", "STAYS"): "ويقعد", ("fix3", "SLEEP"): "تنام", ("fix3", "HIGH"): "فوق",
        ("break4", "BODY"): "حرارتك", ("break4", "MELTS"): "تذوّب", ("break4", "WALLS"): "الجدار", ("break4", "DRIP"): "يقطّر",
        ("break4", "CAVE"): "ويطيح",
        ("fix4", "TRICK"): "السر", ("fix4", "MELT"): "الذايب", ("fix4", "REFREEZES"): "يتجمّد", ("fix4", "ICE"): "جليد",
        ("fix4", "STRONGER"): "تقوى", ("fix4", "STAND"): "توقف",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "LIGHT"): "ولّع", ("reveal", "LAMP"): "سراج", ("reveal", "HOLE"): "خرم", ("reveal", "TOP"): "فوق",
        ("reveal", "WINDOW"): "شباك", ("reveal", "ICE"): "جليد",
        ("stat", "MINUS"): "سالب", ("stat", "ABOVE"): "فوق", ("stat", "SKILLED"): "ويبنونه",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SLEEP"): "ينامون", ("tag", "SNOW"): "عشرين", ("tag", "MOM"): "وحنا", ("tag", "JACKET"): "الفروة",
        ("tag", "CASE"): "وشبّينا"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a Moroccan riad"),
                   "stat": [("-40°", "OUTSIDE"), ("0°+", "INSIDE"), ("1 h", "TO BUILD")],
                   "L": {"name": "AN IGLOO", "snowonly": "NOTHING BUT SNOW", "frost": "FROSTBITE IN MINUTES",
                         "cut": "CUT BLOCKS", "packed": "WIND-PACKED SNOW", "air": "MOSTLY TRAPPED AIR",
                         "jacket": "LIKE A DOWN JACKET", "notrees": "NO TREES", "roof": "NOTHING HOLDS A ROOF",
                         "spiral": "A RISING SPIRAL", "lean": "EACH BLOCK LEANS IN", "itself": "IT HOLDS ITSELF UP",
                         "rises": "WARM AIR RISES", "rush": "COLD RUSHES IN", "below": "DOORWAY BELOW THE FLOOR",
                         "sinks": "COLD AIR SINKS + STAYS", "high": "SLEEP UP HIGH", "melt": "BODY HEAT MELTS IT",
                         "drip": "DRIP... CAVE IN?", "glaze": "A SKIN OF ICE", "stand": "STRONG ENOUGH TO STAND ON",
                         "lamp": "SEAL-OIL LAMP", "hole": "AIR HOLE", "window": "CLEAR ICE WINDOW",
                         "case": "JUST IN CASE!", "mild": "20°", "out": "OUTSIDE", "in": "INSIDE", "warmin": "WARM INSIDE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: رياض مغربي"),
                      "stat": [("-40°", "برا"), ("0°+", "داخل"), ("1", "ساعة بناء")],
                      "L": {"name": "بيت ثلج", "snowonly": "بس ثلج", "frost": "الجلد يتجمد في دقايق",
                            "cut": "قص طوب", "packed": "ثلج دكّته الريح", "air": "أغلبه هوا محبوس",
                            "jacket": "مثل الجاكيت", "notrees": "ما فيه شجر", "roof": "ولا شي يشيل السقف",
                            "spiral": "لولبي وهو يطلع", "lean": "كل طوبة مايلة", "itself": "القبة تشيل نفسها",
                            "rises": "الحار يطلع فوق", "rush": "البرد يدخل", "below": "المدخل أوطى من الأرضية",
                            "sinks": "البرد ينزل ويقعد", "high": "تنام فوق", "melt": "حرارتك تذوّبه",
                            "drip": "بيقطّر؟ بيطيح؟", "glaze": "طبقة جليد", "stand": "تقدر توقف فوقها",
                            "lamp": "سراج زيت", "hole": "خرم للهوا", "window": "شباك جليد",
                            "case": "برد!", "mild": "20°", "out": "برا", "in": "داخل", "warmin": "دافي داخل"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "family": ("hook", "FAMILY", 0.2), "warm": ("hook", "WARM", 0.3), "minus": ("hook", "MINUS", 0.38),
            "forty": ("hook", "FORTY", 0.45), "nothing": ("hook", "NOTHING", 0.55), "snow": ("hook", "SNOW", 0.66),
            "congrats": ("hook", "CONGRATS", 0.72), "igloo": ("hook", "IGLOO", 0.92),
            "wind": ("break1", "WIND", 0.2), "freeze": ("break1", "FREEZE", 0.45), "skin": ("break1", "SKIN", 0.6),
            "minutes": ("break1", "MINUTES", 0.85),
            "cut": ("fix1", "CUT", 0.08), "blocks": ("fix1", "BLOCKS", 0.15), "packed": ("fix1", "WIND", 0.25),
            "trapped": ("fix1", "TRAPPED", 0.48), "air": ("fix1", "AIR", 0.55), "heat": ("fix1", "HEAT", 0.78),
            "jacket": ("fix1", "JACKET", 0.92),
            "trees": ("break2", "TREES", 0.3), "nothing2": ("break2", "NOTHING", 0.4), "roof": ("break2", "ROOF", 0.72),
            "build": ("break2", "BUILD", 0.92),
            "lay": ("fix2", "LAY", 0.1), "blocks2": ("fix2", "BLOCKS", 0.18), "spiral": ("fix2", "SPIRAL", 0.35),
            "leaning": ("fix2", "LEANING", 0.5), "dome": ("fix2", "DOME", 0.78), "itself": ("fix2", "ITSELF", 0.88),
            "warm2": ("break3", "WARM", 0.1), "rises": ("break3", "RISES", 0.2), "door": ("break3", "DOOR", 0.55),
            "cold": ("break3", "COLD", 0.75), "rushes": ("break3", "RUSHES", 0.8),
            "dig": ("fix3", "DIG", 0.08), "doorway": ("fix3", "DOORWAY", 0.15), "below": ("fix3", "BELOW", 0.22),
            "sinks": ("fix3", "SINKS", 0.48), "tunnel": ("fix3", "TUNNEL", 0.6), "stays": ("fix3", "STAYS", 0.7),
            "sleep": ("fix3", "SLEEP", 0.85), "high": ("fix3", "HIGH", 0.95),
            "body": ("break4", "BODY", 0.1), "melts": ("break4", "MELTS", 0.3), "walls": ("break4", "WALLS", 0.45),
            "drip": ("break4", "DRIP", 0.7), "cave": ("break4", "CAVE", 0.85),
            "trick": ("fix4", "TRICK", 0.1), "melt": ("fix4", "MELT", 0.2), "refreezes": ("fix4", "REFREEZES", 0.3),
            "ice": ("fix4", "ICE", 0.48), "stronger": ("fix4", "STRONGER", 0.65), "stand": ("fix4", "STAND", 0.88),
            "follow": ("cta", "FOLLOW", 0.35),
            "light": ("reveal", "LIGHT", 0.05), "lamp": ("reveal", "LAMP", 0.2), "hole": ("reveal", "HOLE", 0.45),
            "top": ("reveal", "TOP", 0.55), "window": ("reveal", "WINDOW", 0.8), "ice2": ("reveal", "ICE", 0.92),
            "s1": ("stat", "MINUS", 0.04), "s2": ("stat", "ABOVE", 0.4), "s3": ("stat", "SKILLED", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "sleep2": ("tag", "SLEEP", 0.1), "t_n": ("tag", "SNOW", 0.4), "t_a": ("tag", "MOM", 0.45),
            "t_b": ("tag", "JACKET", 0.7), "t_c": ("tag", "CASE", 0.9)})
        T["cozy"] = min(T["family"], T["warm"])
        T["rise0"] = min(T["warm2"], T["rises"])
        # ---- sets
        self.cut(s("break1") - 0.12, "wind", 1)
        self.cut(s("fix1") - 0.12, "blocks", -1)
        self.cut(s("break2") - 0.12, "build", 1)
        self.cut(s("break3") - 0.12, "cut", -1)
        self.cut(s("stat") - 0.12, "tundra", 1)
        self.cut(s("closer") - 0.12, "tundra", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- tundra camera
        ct = Camera(70, -60, 1.42)
        ct.key(0.3, 40, -80, 1.36, max(1.0, T["congrats"] - 0.4))
        ct.key(T["congrats"], 60, -120, 1.2, 1.4)
        ct.key(s("stat") - 0.12, 60, -140, 1.1, 0.0).key(s("stat"), 60, -150, 1.12, 4.0)
        ct.key(s("closer") - 0.12, 80, -110, 1.3, 0.0).key(self.duration, 80, -110, 1.36, 4.0)
        self.cam = ct
        # ---- cutaway camera
        cc = Camera(70, -150, 1.42)
        cc.key(s("fix3") - 0.12, 150, -110, 1.3, 0.6)
        cc.key(s("break4") - 0.12, 20, -170, 1.5, 0.6)
        cc.key(T["stronger"] - 0.3, 20, -240, 1.2, 0.8)
        cc.key(s("reveal") - 0.12, 30, -160, 1.45, 0.4)
        self.cam_cut = cc
        self.spans = [(T["minutes"], T["jacket"] + 0.3), (T["build"], T["itself"] + 0.3), (T["rushes"], T["high"] + 0.3),
                      (T["cave"], T["stand"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["skin"], 0.3, 6), (T["roof"] + 0.3, 0.35, 8), (T["itself"], 0.3, 6),
                       (T["door"] + 0.1, 0.3, 6), (T["cave"], 0.3, 6), (T["stand"], 0.3, 7), (s("closer") + 0.2, 0.35, 9),
                       (T["t_b"], 0.3, 6)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def sky_back(self, c, t, cam, aur=1.0, amp=1.0):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=ARCTIC, horizon_y=gy - 40)
        v2.stars(c, W, H, t, 0.9, dx=-cx * 0.02)
        aurora(c, t, aur, y0=330, amp=amp)
        ice_hills(c, cam)
        return gy

    def interior(self, c, t, warm=1.0, people=True, pose="sit", lamp_on=1.0, lamp_x=-40):
        """The inside of the dome in section: floor, raised sleeping platform at the back, the family."""
        c.save()
        c.clipPath(dome_path(), doAntiAlias=True)
        c.drawRect(R(-RX + 30, -RY, 2 * RX - 60, RY), P("#1A2440"))
        if warm > 0:
            add_glow(c, -60, -140, 360, WARM, 0.55 * warm)
        c.drawRect(R(-RX + 30, -96, 300, 96), lin_paint(0, -96, 0, 0, ["#B9CADF", "#8EA4BF"]))   # sleeping platform
        c.drawRRect(rr(-RX + 40, -110, 280, 18, 8), P("#8B5E34"))                                  # furs
        if people:
            for i, (px, col) in enumerate(((-210, "#B91C1C"), (-140, "#1D4ED8"), (-70, "#15803D"))):
                hood_person(c, px, -96, 96 + (i % 2) * 10, col, t + i * 0.4, pose=pose, face=1)
        lamp(c, lamp_x, -96, 0.9, lamp_on, t)
        c.restore()

    def shell(self, c, inner=1.0, glaze=0.0, t=0.0):
        """The dome wall in section (outer surface to inner surface, about 40 thick), optional ice glaze inside."""
        ring = skia.Path()
        n = 40
        for i in range(n + 1):
            x = lerp(-RX, RX, i / float(n))
            (ring.moveTo if i == 0 else ring.lineTo)(x, dome_y(x))
        for i in range(n + 1):
            x = lerp(RX - 40, -RX + 40, i / float(n))
            y = dome_y(x * RX / (RX - 40)) * (RY - 40) / RY
            ring.lineTo(x, y)
        ring.close()
        c.drawPath(ring, lin_paint(0, -RY, 0, 0, ["#DCE6F2", "#B9CADF", "#90A8C4"]))
        for r in range(8):                                                  # block joints in the wall
            ang = math.radians(10 + r * 20)
            for sd in (-1, 1):
                x0, y0 = sd * RX * math.cos(ang), -RY * math.sin(ang)
                x1, y1 = sd * (RX - 40) * math.cos(ang), -(RY - 40) * math.sin(ang)
                c.drawLine(x0, y0, x1, y1, P("#8FA9C6", 0.8, stroke=3))
        if glaze > 0:
            gl = skia.Path()
            for i in range(n + 1):
                x = lerp(RX - 40, -RX + 40, i / float(n))
                y = dome_y(x * RX / (RX - 40)) * (RY - 40) / RY
                (gl.moveTo if i == 0 else gl.lineTo)(x, y)
            c.drawPath(gl, P("#7DD3FC", 0.9 * glaze, stroke=12))
            c.drawPath(gl, P("#FFFFFF", 0.6 * glaze, stroke=4))
            add_glow(c, 0, -RY + 60, 200, "#BAE6FD", 0.3 * glaze)

    # ------------------------------------------------------------------ set: tundra (hook, stat, closer)
    def draw_tundra(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1") - 0.12
        aur = 0.45 + 0.55 * prog(t, T["congrats"] - 0.2, T["congrats"] + 0.6) if hook else 1.0
        self.sky_back(c, t, cam, aur)
        self.view(c, cam)
        snowfield(c, -3000, 3000)
        contact_shadow(c, 40, 6, 760, 0.35, 40)
        cutk = e_io(prog(t, T["cozy"] - 0.2, T["cozy"] + 0.5)) * (1 - e_io(prog(t, T["congrats"] - 0.1, T["congrats"] + 0.5))) if hook else 0.0
        final = not hook
        igloo_outside(c, t, glow=1.0, seams=1.0, window=1.0 if final else 0.0, hole=1.0 if final else 0.0,
                      steam=1.0 if final else 0.0)
        if cutk > 0:                                                        # the cutaway: warm inside
            c.save()
            dp = dome_path()
            c.clipPath(dp, doAntiAlias=True)
            c.saveLayerAlpha(None, int(255 * cutk))
            self.interior(c, t, warm=1.0, people=True, pose="sit", lamp_on=1.0, lamp_x=-20)
            c.restore()
            c.restore()
            c.saveLayerAlpha(None, int(255 * cutk))
            self.shell(c)
            c.restore()
        for i in range(3):                                                  # sled tracks and a sled dog team's sled
            c.drawLine(-900 + i * 18, 60 + i * 30, 900, 120 + i * 30, P("#B8CDE2", 0.5, stroke=4))
        c.restore()
        if hook:
            blizzard(c, t, a=1 - 0.7 * prog(t, T["congrats"], T["congrats"] + 0.6), n=110, slant=0.35, speed=1.4)
        else:
            blizzard(c, t, a=0.25, n=40, slant=0.2, speed=0.5)
        self.ui["cam"] = cam

    def ui_tundra(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            k = self.span(T["minus"] - 0.2, T["congrats"] + 0.2)
            if k > 0:
                thermo(c, 150, 760, 1.1, 0.05, a=k)
                readout(c, 150, 560, -40, 46, "#7DD3FC", a=k)
            k2 = self.span(T["cozy"] + 0.2, T["congrats"] + 0.2)
            if k2 > 0:
                v2.chip(c, 760, 560, self.L["warmin"], k2, accent=WARM, size=36)
            self.chip(540, 420, "snowonly", T["nothing"] - 0.1, T["congrats"] - 0.1, accent="#BAE6FD", size=42)
            self.chip(540, 420, "name", T["igloo"] - 0.15, s("break1") + 0.1, accent=HILITE, size=48)

    # ------------------------------------------------------------------ set: wind (break1)
    def draw_wind(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B1736", "#1E3A6A", "#3B6A94"])
        c.drawRect(R(0, 1180, W, H - 1180), lin_paint(0, 1180, 0, H, [SNOW, "#7E9BBE"]))
        fr = prog(t, T["freeze"] - 0.2, T["minutes"] + 0.3)
        c.save()
        c.translate(540, 1180)
        c.scale(1.0, 1.0)
        hood_person(c, 0, 0, 560, "#1D4ED8", t, pose="stand", face=-1, frost=fr)
        c.restore()
        blizzard(c, t, a=1.0, n=140, slant=0.12, speed=1.8, seed=8)

    def ui_wind(self, c, t, tw):
        T, s = self.T, self.tl.s
        k = self.span(T["skin"] - 0.2, s("fix1") - 0.15)
        if k > 0:
            v2.chip(c, 540, 420, self.L["frost"], k, accent="#7DD3FC", size=40)
            frac = prog(tw, T["skin"], s("fix1"))
            c.drawCircle(860, 600, 74, P(GLASS, 0.85 * k))
            sw = skia.Path()
            sw.addArc(R(800, 540, 120, 120), -90, 360 * frac)
            c.drawPath(sw, P(WARN, k, stroke=12))
        self.badge("alert", T["minutes"] + 0.05, s("fix1") - 0.2, x=880, y=780)
        self.red(T["minutes"] + 0.05, 1.2)

    # ------------------------------------------------------------------ set: blocks (fix1)
    def draw_blocks(self, c, t):
        T, s = self.T, self.tl.s
        cam = (60, -150, 1.25)
        self.sky_back(c, t, cam, 0.6)
        self.view(c, cam)
        snowfield(c, -3000, 3000)
        for k in range(5):                                                  # layers of wind-packed snow
            c.drawLine(-3000, 40 + k * 46, 3000, 46 + k * 46, P("#9DB5CF", 0.5, stroke=3))
        n_cut = int(clamp((t - (T["cut"] - 0.1)) / 0.5, 0, 5))
        for i in range(5):                                                  # holes where blocks came out
            hx = -380 + i * 130
            if i < n_cut:
                c.drawRect(R(hx, 0, 110, 70), P("#5E7FA8"))
        for i in range(n_cut):                                              # the stack of cut blocks
            bx_ = 330 + (i % 3) * 120
            by_ = -60 - (i // 3) * 60
            c.drawRRect(rr(bx_, by_, 112, 58, 8), lin_paint(bx_, by_, bx_, by_ + 58, ["#D8E4F0", "#A9BDD6"]))
            c.drawRRect(rr(bx_, by_, 112, 58, 8), P("#8FA9C6", stroke=3))
        swing = math.sin(t * 6.0)
        px = -380 + min(4, n_cut) * 130 + 60
        hood_person(c, px - 70, 0, 230, "#B91C1C", t, pose="look", face=1)
        kx, ky = px - 40, -120
        c.drawLine(kx, ky, kx + 70 + 10 * swing, ky + 120 + 20 * swing, P("#E5E7EB", stroke=8))     # snow knife
        c.drawLine(kx - 16, ky - 10, kx, ky, P("#78350F", stroke=12))
        c.restore()

    def ui_blocks(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "cut", T["cut"] - 0.1, T["packed"] - 0.1, accent=HILITE, size=42)
        self.chip(540, 420, "packed", T["packed"] - 0.1, T["trapped"] - 0.15, accent="#BAE6FD", size=40)
        self.chip(540, 420, "air", T["trapped"] - 0.15, T["jacket"] - 0.1, accent="#7DD3FC", size=40)
        self.chip(540, 420, "jacket", T["jacket"] - 0.1, s("break2") - 0.15, accent=GOOD, size=40)
        magnifier(c, 380, 690, 150, tw, a=self.span(T["trapped"] - 0.4, s("break2") - 0.15))
        jacket_icon(c, 800, 680, 0.95, a=self.span(min(T["heat"], T["jacket"]) - 0.2, s("break2") - 0.15))
        self.badge("check", T["jacket"] + 0.1, s("break2") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: build (break2, fix2)
    def draw_build(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        cam = (0, -170, 1.35) if fixed else (0, -130, 1.2)
        self.sky_back(c, t, cam, 0.7)
        self.view(c, cam)
        snowfield(c, -3000, 3000)
        if not fixed:
            for i in range(9):                                              # two rows of blocks in a ring
                bx_ = -RX + i * 66
                c.drawRRect(rr(bx_, -60, 62, 58, 6), lin_paint(0, -60, 0, 0, ["#D8E4F0", "#A9BDD6"]))
                c.drawRRect(rr(bx_, -60, 62, 58, 6), P("#7F9AB8", stroke=3))
                if i < 8:
                    c.drawRRect(rr(bx_ + 30, -118, 62, 56, 6), lin_paint(0, -118, 0, -60, ["#D8E4F0", "#A9BDD6"]))
                    c.drawRRect(rr(bx_ + 30, -118, 62, 56, 6), P("#7F9AB8", stroke=3))
            fk = e_in(prog(t, T["roof"] - 0.2, T["roof"] + 0.45))
            ry = lerp(-520, -130, fk)
            ang = 18 * prog(t, T["roof"] + 0.3, T["roof"] + 0.7)
            c.save()
            c.translate(0, ry)
            c.rotate(ang)
            c.drawRRect(rr(-280, -30, 560, 40, 10), lin_paint(0, -30, 0, 10, ["#D8E4F0", "#8EA7C4"]))
            c.restore()
            if fk >= 1:
                splash(c, 0, -120, t, T["roof"] + 0.45, dur=0.8, n=24, speed=500, col="#F0F9FF")
        else:
            prog_b = clamp((t - (s("fix2") - 0.05)) / max(0.5, T["itself"] - s("fix2") + 0.05))
            hgt = RY * e_out(prog_b)
            dp = dome_path()
            c.save()
            c.clipRect(R(-2000, -hgt, 4000, 4000))
            c.drawPath(dp, rad_paint(-90, -230, 460, ["#DCE6F2", "#BFD0E4", "#93ABC7", "#6E88A8"], [0.0, 0.35, 0.8, 1.0]))
            c.clipPath(dp, doAntiAlias=True)
            for r in range(9):
                y0 = -r * 38
                c.drawLine(-RX, y0 - 4, RX, y0 - 34, P("#8FA9C6", 0.8, stroke=3))
                for j in range(-6, 7):
                    xx = j * 52 + (r % 2) * 24
                    yy = y0 - 4 - 30 * (xx + RX) / (2 * RX)
                    c.drawLine(xx, yy, xx - 6 * math.copysign(1, xx) * 0.5, yy - 34, P("#8FA9C6", 0.6, stroke=2.5))
            c.restore()
            if prog_b < 1:                                                  # the block being set, at the top edge
                bx_ = RX * 0.8 * math.cos(t * 3.0)
                yb = -hgt + 4
                c.drawRRect(rr(bx_ - 30, yb - 30, 60, 32, 6), P("#E1EAF5"))
                add_glow(c, bx_, yb - 14, 70, HILITE, 0.5)
            kb = prog(t, T["itself"] - 0.35, T["itself"])                    # the key block on top
            if kb > 0:
                c.drawRRect(rr(-34, lerp(-RY - 160, -RY - 10, e_in(kb)), 68, 34, 8), P("#E1EAF5"))
            pk = 1 - prog(t, T["itself"] - 0.3, T["itself"])
            if pk > 0:
                hood_person(c, 0, -max(0.0, hgt - 160), 140, "#B91C1C", t, pose="cheer" if prog_b > 0.9 else "look", a=pk)
            sp = self.span(T["spiral"] - 0.2, T["dome"])                     # the spiral path drawn on the dome
            if sp > 0:
                hp = skia.Path()
                for i in range(120):
                    u = i / 119.0
                    ang = u * math.pi * 2 * 4.2
                    yy = -u * RY * 0.95
                    xx = math.cos(ang) * RX * math.sqrt(max(0.0, 1 - (yy / RY) ** 2)) * 0.92
                    if math.sin(ang) < 0:
                        (hp.moveTo(xx, yy) if i == 0 else hp.moveTo(xx, yy))
                    else:
                        (hp.moveTo if i == 0 else hp.lineTo)(xx, yy)
                c.drawPath(hp, P(HILITE, 0.9 * sp, stroke=6))
        c.restore()
        self.ui["fixed"] = fixed

    def ui_build(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            k = self.span(T["trees"] - 0.2, s("fix2") - 0.15)
            if k > 0:
                c.drawCircle(220, 640, 110, P(GLASS, 0.85 * k))
                tree_icon(c, 220, 690, 0.9, a=k)
                c.drawCircle(220, 640, 100, P(WARN, k, stroke=10))
                c.drawLine(150, 710, 290, 570, P(WARN, k, stroke=12))
            self.chip(540, 420, "notrees", T["trees"] - 0.15, T["roof"] - 0.15, accent="#E2E8F0", size=40)
            self.chip(540, 420, "roof", T["roof"] - 0.15, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["build"] + 0.05, s("fix2") - 0.2, x=880, y=520)
            self.red(T["roof"] + 0.4, 1.2)
            return
        self.chip(540, 420, "spiral", T["spiral"] - 0.2, T["leaning"] - 0.1, accent=HILITE, size=42)
        self.chip(540, 420, "lean", T["leaning"] - 0.1, T["dome"] - 0.1, accent="#BAE6FD", size=42)
        self.chip(540, 420, "itself", T["dome"] - 0.1, s("break3") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["itself"] + 0.1, s("break3") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: cut (break3, fix3, break4, fix4, reveal)
    def draw_cut(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam_cut.at(t)
        self.sky_back(c, t, cam, 0.7)
        self.view(c, cam)
        good = t >= s("fix3") - 0.12
        dug = e_out(prog(t, T["dig"] - 0.1, T["below"] + 0.4)) if good else 0.0
        snowfield(c, -3000, 3000)
        if dug > 0:                                                         # the trench of the tunnel, below the floor
            tr = skia.Path()
            tr.moveTo(RX - 50, 0)
            tr.lineTo(RX - 50, 120 * dug)
            tr.lineTo(520, 120 * dug)
            tr.lineTo(580, 0)
            tr.close()
            c.drawPath(tr, lin_paint(0, 0, 0, 120, ["#2A3A5E", "#1E3A6A"]))
            c.drawPath(tr, P("#8FA9C6", stroke=4))
            tp = skia.Path()
            tp.moveTo(RX - 50, 0)
            tp.cubicTo(340, -110, 470, -100, 560, 0)
            c.drawPath(tp, P("#E8F1FA", stroke=34))
        reveal = t >= s("reveal") - 0.12
        lamp_on = prog(t, T["light"] - 0.1, T["lamp"] + 0.2) if reveal else (1.0 if t >= s("fix3") - 0.12 else 0.6)
        warm = 1.0
        if s("break3") - 0.12 <= t < s("fix3") - 0.12:
            warm = 1 - 0.6 * prog(t, T["door"], T["rushes"] + 0.4)
        pose = "sit"
        if good and t < s("break4") - 0.12:
            pose = "sit"
        self.interior(c, t, warm=warm, people=True, pose=pose, lamp_on=lamp_on, lamp_x=-20)
        if good and dug > 0.5 and t < s("break4") - 0.12:                   # cold air pooling in the trench
            ck = prog(t, T["sinks"] - 0.3, T["sinks"] + 0.3)
            for k in range(6):
                q = (t * 0.6 + k / 6.0) % 1.0
                x_ = lerp(540, RX - 30, q)
                y_ = lerp(-40, 90, min(1.0, q * 1.6))
                c.drawCircle(x_, y_, 18, P("#60A5FA", 0.55 * ck))
            c.drawRect(R(RX - 46, 60, 560 - RX, 58), P("#3B82F6", 0.35 * prog(t, T["stays"] - 0.3, T["stays"] + 0.3)))
        glaze = 0.0
        if t >= s("fix4") - 0.12:
            glaze = e_io(prog(t, T["refreezes"] - 0.2, T["ice"] + 0.3))
        self.shell(c, glaze=glaze, t=t)
        if not good:                                                        # break3: a door at floor level
            dk = prog(t, T["door"] - 0.2, T["door"] + 0.2)
            c.drawRect(R(RX - 46, -110, 46, 110), P("#1A2440"))
            c.save()
            c.translate(RX, -110)
            c.rotate(-70 * dk)
            c.drawRect(R(0, 0, 14, 110), P("#78350F"))
            c.restore()
            rk = self.span(T["rise0"] - 0.2, T["rushes"] + 1.5)
            for k in range(4):                                              # warm air goes up
                q = (t * 0.7 + k / 4.0) % 1.0
                arrow(c, -180 + k * 90, -60 - q * 120, -180 + k * 90, -120 - q * 120, WARM, a=rk * (1 - q), w=12, head=26)
            ck = prog(t, T["cold"] - 0.3, T["cold"] + 0.2)
            for k in range(5):                                              # cold in along the floor
                q = (t * 1.2 + k / 5.0) % 1.0
                x_ = lerp(RX + 200, -RX + 60, q)
                arrow(c, x_ + 70, -30 - k * 6, x_, -30 - k * 6, "#60A5FA", a=ck * (1 - q * 0.5), w=12, head=26)
        if s("break4") - 0.12 <= t < s("fix4") - 0.12:                      # drips from the melting wall
            mk = prog(t, T["melts"] - 0.3, T["melts"] + 0.3)
            for k in range(7):
                ang = math.radians(35 + k * 16)
                x0 = (RX - 44) * math.cos(ang) * (1 if k % 2 else -1)
                y0 = -(RY - 44) * math.sin(ang)
                q = (t * 1.1 + k * 0.29) % 1.0
                c.drawCircle(x0, y0 + q * 160, 7, P("#7DD3FC", mk * (1 - q)))
            ck = prog(t, T["cave"] - 0.2, T["cave"] + 0.2)
            if ck > 0:
                c.drawLine(-80, -RY + 30, -20, -RY + 80, P("#475569", ck, stroke=4))
                c.drawLine(-20, -RY + 80, 40, -RY + 60, P("#475569", ck, stroke=4))
        if t >= s("fix4") - 0.12 and t < s("reveal") - 0.12:                 # someone stands on top
            sk = prog(t, T["stand"] - 0.4, T["stand"])
            if sk > 0:
                hood_person(c, 30, -RY + 4 - 40 * (1 - e_out(sk)), 150, "#F59E0B", t, pose="cheer", face=1, a=sk)
        if reveal:
            hk = prog(t, T["hole"] - 0.2, T["hole"] + 0.2)
            if hk > 0:
                c.drawRect(R(-18, -RY - 4, 36, 44), P("#1A2440", hk))
                for k in range(5):
                    q = (t * 0.6 + k / 5.0) % 1.0
                    c.drawCircle(math.sin(t + k) * 10, -RY - 10 - q * 150, 12 + 18 * q, P("#F8FAFC", 0.5 * hk * (1 - q)))
            wk = prog(t, T["window"] - 0.2, T["window"] + 0.2)
            if wk > 0:
                wx, wy = (RX - 20) * math.cos(math.radians(140)), -(RY - 20) * math.sin(math.radians(140))
                c.save()
                c.translate(wx, wy)
                c.rotate(-40)
                c.drawRRect(rr(-46, -28, 92, 56, 10), lin_paint(-46, -28, 46, 28, ["#F0F9FF", "#7DD3FC"], a=wk))
                c.drawRRect(rr(-46, -28, 92, 56, 10), P("#FFFFFF", wk, stroke=4))
                c.restore()
                add_glow(c, wx, wy, 120, "#E0F2FE", 0.6 * wk)
        c.restore()
        self.ui["cam"] = cam

    def ui_cut(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam_cut.at(tw))
        if tw < s("fix3") - 0.12:
            self.chip(540, 420, "rises", T["rise0"] - 0.15, T["door"] - 0.1, accent=WARM, size=40)
            self.chip(540, 420, "rush", T["door"] - 0.1, s("fix3") - 0.15, accent="#60A5FA", size=40)
            self.badge("alert", T["rushes"] + 0.05, s("fix3") - 0.2, x=880, y=520)
            self.red(T["rushes"] + 0.05, 1.2)
            return
        if tw < s("break4") - 0.12:
            self.chip(540, 420, "below", T["dig"] - 0.1, T["sinks"] - 0.15, accent=HILITE, size=38)
            tx, ty = self.at(cam, 520, 70)
            self.label(tx, ty, 760, 1080, "sinks", T["sinks"] - 0.15, s("break4") - 0.15, "#60A5FA", size=34)
            self.chip(540, 420, "high", T["sleep"] - 0.15, s("break4") - 0.15, accent=WARM, size=40)
            self.badge("check", T["high"] + 0.05, s("break4") - 0.15, x=880, y=520)
            return
        if tw < s("fix4") - 0.12:
            self.chip(540, 420, "melt", T["body"] - 0.1, T["drip"] - 0.15, accent=WARM, size=40)
            self.chip(540, 420, "drip", T["drip"] - 0.15, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["cave"] + 0.05, s("fix4") - 0.2, x=880, y=520)
            self.red(T["cave"] + 0.05, 1.2)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 420, "glaze", T["refreezes"] - 0.1, T["stand"] - 0.3, accent="#7DD3FC", size=42)
            self.chip(540, 420, "stand", T["stand"] - 0.3, s("cta") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["stand"] + 0.1, s("cta") - 0.15, x=880, y=520)
            return
        if tw >= s("reveal") - 0.12:
            lx, ly = self.at(cam, -20, -110)
            self.label(lx, ly, 280, 1080, "lamp", T["lamp"] - 0.15, s("stat") - 0.15, WARM, size=36)
            hx, hy = self.at(cam, 0, -RY - 20)
            self.label(hx, hy, 300, 560, "hole", T["hole"] - 0.1, s("stat") - 0.15, "#E2E8F0", size=36)
            wx, wy = self.at(cam, (RX - 20) * math.cos(math.radians(140)), -(RY - 20) * math.sin(math.radians(140)))
            self.label(wx, wy, 760, 560, "window", T["window"] - 0.1, s("stat") - 0.15, "#7DD3FC", size=36)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:                                                    # a mild sunny day, mom and the jacket
            vrect(c, 0, 0, W, H, ["#7DD3FC", "#BAE6FD", "#E0F2FE"])
            add_glow(c, 860, 260, 220, "#FDE68A", 0.8)
            c.drawCircle(860, 260, 70, P("#FDE68A"))
            c.drawRect(R(0, 1150, W, H - 1150), lin_paint(0, 1150, 0, H, ["#86EFAC", "#15803D"]))
            c.drawRect(R(560, 420, 420, 740), lin_paint(560, 0, 980, 0, ["#E2B98A", "#C99A6A"]))   # the house front
            c.drawRect(R(640, 700, 200, 450), P("#7C2D12"))                 # the open door
            c.drawRect(R(660, 720, 160, 430), P("#1F2937"))
            mk = prog(t, T["t_a"] - 0.3, T["t_a"])
            person(c, 740, 1150, 300, "#DB2777", t, pose="point", face=-1, hat="none", hair="#7C2D12", a=mk)
            jk = prog(t, T["t_b"] - 0.2, T["t_b"] + 0.1)
            if jk > 0:
                jacket_icon(c, 560, 900, 0.9 * e_back(jk), a=jk, col="#EF4444")
            person(c, 300, 1150, 240, "#F59E0B", t, pose="shrug" if t >= T["t_c"] - 0.2 else "walk", face=-1,
                   hat="cap", hair="#1C1917")
            c.drawCircle(150, 300, 2, P("#FFFFFF", 0.0))
        else:                                                               # a desert winter night at twenty degrees
            sk = {"top": "#0B1033", "upper": "#1B1F4F", "mid": "#3B2F63", "low": "#6B4A6B", "horizon": "#B97E5E",
                  "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
            v2.sky(c, W, H, 0.0, pal=sk, horizon_y=1060)
            v2.stars(c, W, H, t, 0.9)
            v2.moon(c, 220, 300, 60)
            dune = skia.Path()
            dune.moveTo(-20, 1060)
            dune.quadTo(300, 980, 560, 1050)
            dune.quadTo(820, 1110, 1100, 1010)
            dune.lineTo(1100, 1300)
            dune.lineTo(-20, 1300)
            dune.close()
            c.drawPath(dune, lin_paint(0, 980, 0, 1300, ["#B98447", "#8F5E2B", "#6B451D"]))
            vrect(c, 0, 1240, W, H - 1240, ["#6B451D", "#3A2410"])
            fk = prog(t, T["t_c"] - 0.2, T["t_c"] + 0.3)
            for k in range(3):                                              # the fire
                if fk > 0:
                    v2.flame(c, 600 + (k - 1) * 30, 1150, 46, 150 * fk, t, power=fk, seed=k)
            if fk > 0:
                add_glow(c, 600, 1100, 360, "#FB923C", 0.6 * fk)
            for k in range(4):
                c.drawLine(540 + k * 40, 1160, 620 - k * 20, 1130, P("#5B3A22", stroke=10))
            dallah(c, 760, 1160, 1.0)
            ck = prog(t, T["t_b"] - 0.2, T["t_b"] + 0.2)
            shiver = (1 - ck) * math.sin(t * 40) * 3
            px, py, ph = 340 + shiver, 1185, 470
            u = ph / 140.0
            dr = skia.Path()                                                # the shemagh hanging behind the head
            dr.moveTo(px - 23 * u, py - 138 * u)
            dr.lineTo(px + 23 * u, py - 138 * u)
            dr.lineTo(px + 31 * u, py - 96 * u)
            dr.lineTo(px - 31 * u, py - 96 * u)
            dr.close()
            c.drawPath(dr, P("#DC2626"))
            for k in range(4):
                c.drawLine(px - 28 * u, py - (128 - k * 9) * u, px + 28 * u, py - (128 - k * 9) * u, P("#FEE2E2", 0.7, stroke=1.6 * u))
            person(c, px, py, ph, "#E7E5E4", t, pose="stand", face=1, hat="none", hair="#1F2937", pants="#D6D3D1",
                   skin="#C68B59")
            fur_cloak(c, px, py, ph, a=ck)
            cap = skia.Path()                                               # the cloth over the head, the black agal
            cap.moveTo(px - 22 * u, py - 128 * u)
            cap.cubicTo(px - 22 * u, py - 152 * u, px + 22 * u, py - 152 * u, px + 22 * u, py - 128 * u)
            cap.close()
            c.drawPath(cap, P("#DC2626"))
            c.drawOval(R(px - 20 * u, py - 145 * u, 40 * u, 8 * u), P("#111827", stroke=3 * u))

    def ui_tag(self, c, t, tw):
        T = self.T
        k = self.span(T["t_n"] - 0.2, self.duration + 1)
        if k > 0:
            thermo(c, 160 if self.rtl else 920, 760, 1.0, 0.62, a=k)
            readout(c, 160 if self.rtl else 920, 560, 20, 44, "#FDE68A", a=k)
        k2 = self.span(T["t_c"] - 0.15, self.duration + 1)
        if k2 > 0:
            bx, by = (430, 470) if not self.rtl else (520, 470)
            sz = 44
            lab = self.L["case"]
            wdt = (arabic.width_ar(lab, sz * 1.15, "Tajawal-Black") if arabic.is_ar(lab) else text_width(lab, sz, "Poppins-Black")) + 70
            kk = e_back(clamp(k2))
            c.save()
            c.translate(bx, by)
            c.scale(kk, kk)
            c.drawRRect(rr(-wdt / 2, -60, wdt, 110, 50), P("#F8FAFC"))
            tp = skia.Path()
            tp.moveTo(20, 46)
            tp.lineTo(50, 46)
            tp.lineTo(70, 96)
            tp.close()
            c.drawPath(tp, P("#F8FAFC"))
            word(c, lab, 0, 14, sz, "#111827")
            c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=ARCTIC, horizon_y=H * 0.62)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.0, T["congrats"]), 61), -10), (0.1, sfx.whoosh(1.2, True, 62), -14),
              (T["cozy"], sfx.whoosh(0.5, False, 63), -12), (T["cozy"] + 0.1, sfx.sparkle(0.6, 8, 64), -12),
              (T["minus"], sfx.tick(), -8), (T["snow"], sfx.pop(65), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 11, 66), -8), (T["igloo"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (s("break1"), sfx.hiss(2.4, 68), -8),
               (T["freeze"], sfx.sizzle(0.6, 69), -14), (T["minutes"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 70), -4)]
        for k in range(5):
            ev.append((T["cut"] - 0.1 + k * 0.5, sfx.snap(71 + k), -12))
        ev += [(T["trapped"], sfx.sparkle(0.6, 7, 76), -12), (T["jacket"], sfx.pop(77), -8), (T["jacket"] + 0.1, sfx.ding(), -8),
               (T["jacket"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 78), -4), (T["trees"], sfx.buzz(0.3), -12),
               (T["roof"] + 0.45, sfx.thud(0.5, 79), -6), (T["roof"] + 0.5, sfx.hiss(0.8, 80), -12),
               (T["build"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 81), -4)]
        for k in range(10):
            ev.append((s("fix2") + k * max(0.2, (T["itself"] - s("fix2")) / 10.0), sfx.tap(82 + k), -12))
        ev += [(T["itself"], sfx.thud(0.3, 93), -6), (T["itself"] + 0.1, sfx.ding(), -8), (T["itself"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 94), -4), (T["rise0"], sfx.riser(1.0, 95), -14),
               (T["door"], sfx.creak(0.6), -8), (T["cold"], sfx.whoosh(0.9, False, 96), -8),
               (T["rushes"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 97), -4)]
        for k in range(4):
            ev.append((T["dig"] + k * 0.2, sfx.snap(98 + k), -12))
        ev += [(T["sinks"], sfx.whoosh(0.8, False, 102), -14), (T["high"] + 0.1, sfx.ding(), -8), (T["high"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 103), -4)]
        for k in range(6):
            ev.append((T["melts"] + k * 0.35, sfx.tap(104 + k), -10))
        ev += [(T["cave"], sfx.creak(0.7), -8), (T["cave"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 110), -4), (T["refreezes"], sfx.sparkle(0.8, 10, 111), -10),
               (T["stand"] - 0.2, sfx.thud(0.3, 112), -8), (T["stand"] + 0.1, sfx.ding(), -8), (T["stand"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(113), 0), (T["follow"] - 0.15, sfx.pop(114), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 115), -6), (T["light"], sfx.click(116), -8),
               (T["lamp"], sfx.sizzle(0.5, 117), -14), (T["hole"], sfx.pop(118), -8), (T["window"], sfx.sparkle(0.6, 8, 119), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 120), -6), (T["s1"], sfx.pop(121), -3), (T["s2"], sfx.pop(122), -3),
               (T["s3"], sfx.pop(123), -3)]
        ev += [(T["cong2"], sfx.pop(124), -2), (T["cong2"], sfx.sparkle(1.0, 14, 125), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 126), -6), (T["t_n"], sfx.tick(), -8), (T["t_b"], sfx.pop(127), -6),
               (T["t_c"], sfx.pop(128), -6)]
        if self.rtl:
            ev += [(T["t_c"], sfx.sizzle(1.0, 129), -12)]
        return ev


NAME = "igloo"
EPISODE = Igloo
