"""Episode 46 - The Aswan High Dam (Egypt).  v2 look: a golden afternoon over the Nile valley at Aswan, dark granite
hills, date palms, mud-brick villages, the lake behind the dam.

Sets: valley (hook: seventeen Great Pyramids of rock drop across the Nile in two rows and turn into the dam, the lake
fills behind it; break1: before the dam the summer flood drowns the villages, the next year the river barely comes and
the fields crack; fix1: the dam blocks the valley, the flood waits in the lake and comes out slowly, twelve equal
months; the start of the reveal: the lake to the horizon, 500 km; the stat at dusk with the power station and the
villages lit; the closer), section (break2: the lake pushes a thin wall over; fix2: a hill of rock and sand almost a
kilometre thick at the bottom; break3: water seeps through the rock and sand and under it, like coffee through a
filter; fix3: a clay core and a cement curtain pumped down to the granite stop it), divert (break4/fix4 from above:
rocks thrown into the river are swept away; a channel blasted through the granite takes the Nile around and a wall of
rock closes the gap), temple (the reveal: the four giant statues of Abu Simbel, the water rising, cut into blocks and
lifted up the cliff), shower (the tag: a head full of shampoo and the water cuts off).
World (valley): a raised view looking upstream. The dam crest is at y = -180, its toe at y = 40, the lake fills the
valley behind it up to the horizon at y = -640; below the dam the river comes toward the viewer.
World (section): side view, the riverbed at y = 0, the lake on the left, the granite below y = 460.
"""
from v2_base import *  # noqa: F401,F403
from pyramid import palm  # noqa: E402
from falaj import mudhouse, word, stars_sky  # noqa: E402,F401
from windtower import sun, arrow, heat_lines  # noqa: E402

GOLD = {"top": "#16204C", "upper": "#3E3F7C", "mid": "#B25F78", "low": "#F2A15E", "horizon": "#FFD58C",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SAND, SAND_D = "#E0B070", "#A8733A"
GRANITE, GRANITE_D = "#5E4440", "#2E2020"
NILE, NILE_D = "#2E6FD8", "#173A8C"
LAKE_C, LAKE_D = "#3B82F6", "#1E3A8A"
FIELD, FIELD_D = "#4D8B31", "#2F5E1E"
DRY, DRY_D = "#B98A4C", "#8A6234"
DAM, DAM_D = "#A39484", "#5E5248"
CLAY = "#A0522D"
CEMENT = "#C3C7CF"
BED = "#C9A46A"

HZ = -640.0          # horizon (valley set)
CREST, TOE = -180.0, 40.0


# ====================================================================================== pieces
def lake_half(y):
    """Half width of the valley floor between the granite hills (valley set, upstream of the dam), with the inlets
    (khors) of the lake shore."""
    u = clamp((CREST - y) / (CREST - HZ))
    base = lerp(700, 120, u ** 0.6)
    return base * (1 + 0.10 * math.sin(y / 21.0) + 0.06 * math.sin(y / 7.3 + 1.0))


def up_half(y):
    """The Nile before the dam (upstream part): narrow, converging to the horizon."""
    u = clamp((TOE - y) / (TOE - HZ))
    return lerp(120, 18, u ** 0.8)


def dn_half(y):
    return lerp(95, 230, clamp((y - TOE) / 1300.0))


def mini_pyramid(c, x, y, s, a=1.0, lit=1.0):
    """A small Great Pyramid (two faces) standing on (x, y)."""
    if a <= 0:
        return
    A = (x, y - 100 * s)
    L_ = (x - 70 * s, y)
    F = (x + 14 * s, y + 8 * s)
    Rr = (x + 66 * s, y - 4 * s)
    lp = skia.Path()
    lp.moveTo(*A)
    lp.lineTo(*L_)
    lp.lineTo(*F)
    lp.close()
    rp = skia.Path()
    rp.moveTo(*A)
    rp.lineTo(*F)
    rp.lineTo(*Rr)
    rp.close()
    c.drawPath(lp, lin_paint(L_[0], 0, F[0], 0, [mix("#E8B46A", "#F6D79A", lit * 0.4), "#D49A55"], a=a))
    c.drawPath(rp, lin_paint(F[0], 0, Rr[0], 0, ["#8A5A2B", "#5E3A1C"], a=a))
    for k in range(1, 6):
        q = k / 6.0
        c.drawLine(lerp(L_[0], A[0], q), lerp(L_[1], A[1], q), lerp(F[0], A[0], q), lerp(F[1], A[1], q),
                   P("#7A4E26", 0.45 * a, stroke=1.6 * s))


def statue(c, x, y, s, broken=False, a=1.0, lit=1.0):
    """One seated colossus of Abu Simbel (front view), feet on (x, y), about 430 * s tall."""
    if a <= 0:
        return
    st, st_d = mix("#D9A273", "#F0C496", 0.3 * lit), "#9A6440"
    def bx(x0, y0, w, h, col=None):
        c.drawRect(R(x + x0 * s, y + y0 * s, w * s, h * s), lin_paint(x + x0 * s, 0, x + (x0 + w) * s, 0,
                                                                          [shade(col or st, 0.08), col or st, st_d], a=a))
    bx(-92, -160, 184, 160, shade(st, -0.12))                              # throne
    for dx in (-62, 14):                                                    # shins and feet
        bx(dx, -150, 48, 136)
        bx(dx - 6, -18, 60, 18, shade(st, 0.06))
    bx(-74, -186, 148, 40)                                                  # lap
    if broken:
        bx(-60, -232, 120, 46, shade(st, -0.06))                            # what is left of the body
        hp = skia.Path()
        hp.moveTo(x - 60 * s, y - 232 * s)
        for k in range(7):
            hp.lineTo(x + (-60 + k * 20) * s, y - (232 + (12 if k % 2 else 0)) * s)
        hp.lineTo(x + 60 * s, y - 232 * s)
        hp.close()
        c.drawPath(hp, P(shade(st, -0.06), a))
        c.drawOval(R(x - 128 * s, y - 70 * s, 92 * s, 70 * s), P(shade(st, -0.1), a))    # the fallen head
        c.drawOval(R(x - 112 * s, y - 52 * s, 48 * s, 26 * s), P(st, a))
        return
    tp = skia.Path()                                                        # body with arms on the knees
    tp.moveTo(x - 70 * s, y - 186 * s)
    tp.lineTo(x - 66 * s, y - 318 * s)
    tp.lineTo(x + 66 * s, y - 318 * s)
    tp.lineTo(x + 70 * s, y - 186 * s)
    tp.close()
    c.drawPath(tp, lin_paint(x - 64 * s, 0, x + 64 * s, 0, [shade(st, 0.1), st, st_d], a=a))
    for sd in (-1, 1):
        c.drawLine(x + sd * 52 * s, y - 300 * s, x + sd * 60 * s, y - 192 * s, P(st_d, 0.6 * a, stroke=6 * s))
    c.drawRect(R(x - 40 * s, y - 236 * s, 80 * s, 10 * s), P(st_d, 0.5 * a))           # belt
    c.save()                                                                # the head, 1.35x about the neck
    c.translate(x, y - 300 * s)
    c.scale(1.35, 1.35)
    c.translate(-x, -(y - 300 * s))
    np_ = skia.Path()                                                       # nemes headdress
    np_.moveTo(x - 30 * s, y - 392 * s)
    np_.lineTo(x - 62 * s, y - 330 * s)
    np_.lineTo(x - 56 * s, y - 300 * s)
    np_.lineTo(x + 56 * s, y - 300 * s)
    np_.lineTo(x + 62 * s, y - 330 * s)
    np_.lineTo(x + 30 * s, y - 392 * s)
    np_.close()
    c.drawPath(np_, lin_paint(x - 62 * s, 0, x + 62 * s, 0, [shade(st, 0.05), shade(st, -0.05), st_d], a=a))
    for k in range(5):
        yy = y - (384 - k * 16) * s
        c.drawLine(x - (34 + k * 6) * s, yy, x - (24 + k * 4) * s, yy, P(st_d, 0.6 * a, stroke=3 * s))
        c.drawLine(x + (24 + k * 4) * s, yy, x + (34 + k * 6) * s, yy, P(st_d, 0.6 * a, stroke=3 * s))
    c.drawOval(R(x - 24 * s, y - 392 * s, 48 * s, 64 * s), P(shade(st, 0.12), a))      # face
    c.drawRect(R(x - 7 * s, y - 330 * s, 14 * s, 22 * s), P(st_d, a))                   # beard
    for sd in (-1, 1):
        c.drawLine(x + sd * 12 * s, y - 368 * s, x + sd * 5 * s, y - 368 * s, P("#5A3A22", 0.8 * a, stroke=3 * s))
    cp = skia.Path()                                                        # double crown
    cp.moveTo(x - 24 * s, y - 392 * s)
    cp.cubicTo(x - 26 * s, y - 440 * s, x - 12 * s, y - 452 * s, x, y - 456 * s)
    cp.cubicTo(x + 12 * s, y - 452 * s, x + 26 * s, y - 440 * s, x + 24 * s, y - 392 * s)
    cp.close()
    c.drawPath(cp, lin_paint(x - 26 * s, 0, x + 26 * s, 0, [shade(st, 0.12), st, st_d], a=a))
    c.restore()


def facade(c, x, y, t, a=1.0, cut=0.0, gap=0.0, lit=1.0):
    """The rock-cut front of the Great Temple of Abu Simbel: four colossi, the door, the cornice. cut 0..1 draws
    the saw lines of the blocks, gap pulls the blocks apart."""
    if a <= 0:
        return
    pp = skia.Path()
    pp.moveTo(x - 520, y)
    pp.lineTo(x - 486, y - 560)
    pp.lineTo(x + 486, y - 560)
    pp.lineTo(x + 520, y)
    pp.close()
    c.drawPath(pp, lin_paint(x - 520, 0, x + 520, 0, ["#C98D62", "#E2AA7C", "#B0744C"], a=a))
    c.drawRect(R(x - 488, y - 584, 976, 26), P("#B0744C", a))
    for k in range(22):                                                     # the frieze of baboons on top
        c.drawCircle(x - 460 + k * 44, y - 571, 9, P("#8A5634", 0.8 * a))
    c.drawRect(R(x - 46, y - 190, 92, 190), P("#2A160E", a))                # door
    c.drawRect(R(x - 30, y - 290, 60, 90), P("#B0744C", a))                 # the niche above it
    for i, sx in enumerate((-360, -130, 130, 360)):
        statue(c, x + sx, y, 1.0, broken=(i == 1), a=a, lit=lit)
    if cut > 0:
        for k in range(1, 14):
            xx = x - 520 + k * 80
            c.drawLine(xx, y - 560, xx, y, P("#3B1F12", 0.75 * a * clamp(cut * 2 - k / 14.0), stroke=4))
        for k in range(1, 8):
            yy = y - k * 70
            c.drawLine(x - 520, yy, x + 520, yy, P("#3B1F12", 0.75 * a * clamp(cut * 2 - 0.5 - k / 16.0), stroke=4))
    _ = gap


def village_house(c, x, y, w, h, a=1.0, lit=0.0, sub=0.0, seed=0, wcol="#9A6B3E"):
    """A flat-roofed mud-brick house in the raised view (front face + roof), standing on (x, y)."""
    if a <= 0:
        return
    rng = random.Random(seed)
    d = h * 0.35
    c.drawRect(R(x - w / 2, y - h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#D49B62", "#B97C47"], a=a))
    rp = skia.Path()
    rp.moveTo(x - w / 2, y - h)
    rp.lineTo(x - w / 2 + d * 0.6, y - h - d)
    rp.lineTo(x + w / 2 + d * 0.6, y - h - d)
    rp.lineTo(x + w / 2, y - h)
    rp.close()
    c.drawPath(rp, P("#E8BC86", a))
    for k in range(2):
        wx = x - w * 0.3 + k * w * 0.4
        c.drawRect(R(wx, y - h * 0.7, w * 0.16, h * 0.22), P("#3B2416", a))
        if lit > 0:
            c.drawRect(R(wx, y - h * 0.7, w * 0.16, h * 0.22), P("#FDBA74", a * lit * rng.uniform(0.5, 1.0)))
            add_glow(c, wx + w * 0.08, y - h * 0.6, 26, "#FDBA74", 0.4 * lit * a)
    c.drawRect(R(x + w * 0.12, y - h * 0.45, w * 0.16, h * 0.45), P("#5B3A22", a))
    if sub > 0:                                                             # standing in flood water
        c.drawRect(R(x - w / 2 - 14, y - h * sub, w + 28, h * sub + 6), lin_paint(0, y - h * sub, 0, y,
                                                                                [wcol, shade(wcol, -0.25)], a=0.95 * a))
        c.drawLine(x - w / 2 - 14, y - h * sub, x + w / 2 + 14, y - h * sub, P("#F5DEB3", 0.7 * a, stroke=3))


def pylon(c, x, y, s, a=1.0):
    """A small power-line tower standing on (x, y)."""
    pc = P("#94A3B8", a, stroke=3 * s)
    c.drawLine(x - 16 * s, y, x - 4 * s, y - 120 * s, pc)
    c.drawLine(x + 16 * s, y, x + 4 * s, y - 120 * s, pc)
    for k in range(4):
        y0 = y - k * 30 * s
        c.drawLine(x - 15 * s + k * 3 * s, y0, x + 12 * s - k * 3 * s, y0 - 30 * s, P("#94A3B8", a, stroke=1.6 * s))
    c.drawLine(x - 30 * s, y - 100 * s, x + 30 * s, y - 100 * s, pc)
    c.drawLine(x - 22 * s, y - 118 * s, x + 22 * s, y - 118 * s, pc)


def shower_guy(c, t, foam=1.0, water=1.0, squint=0.0, rtl=False, a=1.0):
    """The tag: a bathroom with a shower head, someone with a head full of shampoo."""
    vrect(c, 0, 0, W, H, ["#1E4E5C", "#163A46"])
    for i in range(12):                                                     # tiles
        for j in range(16):
            x0, y0 = i * 96 - (48 if j % 2 else 0), j * 90
            c.drawRect(R(x0 + 3, y0 + 3, 90, 84), P("#2B6575" if (i + j) % 3 else "#2F6E80"))
    vrect(c, 0, 1150, W, H - 1150, ["#0F2A33", "#081A20"])
    c.drawRect(R(0, 1140, W, 14), P("#5EA3B5", 0.6))
    hx, hy = 770, 330                                                       # shower head
    c.drawLine(980, 180, 980, 300, P("#CBD5E1", stroke=16))
    c.drawLine(980, 300, hx + 40, 300, P("#CBD5E1", stroke=16))
    c.drawRRect(rr(hx - 70, hy - 26, 140, 44, 20), lin_paint(hx - 70, 0, hx + 70, 0, ["#F1F5F9", "#94A3B8"]))
    px, py, h = 520, 1170, 640                                              # the person
    person(c, px, py, h, "#F97316", t, pose="duck" if squint > 0.5 else "stand", face=1, hat="none", hair="#1C1917",
           skin="#C68B59", pants="#1E3A8A")
    u = h / 140.0
    sq = 0.64 if squint > 0.5 else 1.0
    hx_, hy_ = px, py - 127 * u * sq
    for sd in (-1, 1):                                                      # eyes shut tight
        ex = hx_ + sd * 6 * u + 4 * u
        c.drawLine(ex - 4 * u, hy_ - 2 * u, ex + 4 * u, hy_ + (2 if squint > 0.5 else 0) * u, P("#1C1917", stroke=1.4 * u))
    if foam > 0:
        rng = random.Random(4)
        for k in range(30):
            an = rng.uniform(math.pi * 1.0, math.pi * 2.0)
            rr_ = rng.uniform(6, 11) * u
            fx_ = hx_ + math.cos(an) * rng.uniform(4, 19) * u
            fy_ = hy_ - 16 * u + math.sin(an) * rng.uniform(2, 13) * u
            c.drawCircle(fx_, fy_, rr_ * (0.6 + 0.4 * foam), P("#F8FAFC", foam * 0.95))
            c.drawCircle(fx_ - rr_ * 0.3, fy_ - rr_ * 0.3, rr_ * 0.25, P("#FFFFFF", foam))
        for sd in (-1, 1):                                                  # eyes shut tight, drawn over the foam
            ex = hx_ + sd * 6 * u + 4 * u
            c.drawLine(ex - 4 * u, hy_ - 2 * u, ex + 4 * u, hy_ + (2 if squint > 0.5 else 0) * u, P("#1C1917", stroke=1.4 * u))
        if squint > 0.5:
            c.drawOval(R(hx_ + 1 * u, hy_ + 6 * u, 7 * u, 6 * u), P("#5B1F14"))
        for k in range(3):                                                  # foam running down the face
            q = (t * 0.4 + k * 0.33) % 1.0
            c.drawCircle(hx_ - 10 * u + k * 9 * u, hy_ + lerp(-2, 16, q) * u, 3.2 * u, P("#F8FAFC", foam * (1 - q)))
    if water > 0:                                                           # the water from the head
        for k in range(16):
            xx = hx - 60 + k * 8
            ph = (t * 3.2 + k * 0.13) % 1.0
            c.drawLine(xx, hy + 20 + ph * 60, xx - 140 + k * 6, hy + 20 + ph * 60 + 360,
                       P("#BAE6FD", 0.5 * water, stroke=3))
    else:
        q = (t * 1.3) % 1.0                                                 # one last drip
        c.drawCircle(hx, hy + 26 + q * 260, 7, P("#BAE6FD", 0.9 * (1 - q)))


# ====================================================================================== the episode
class Aswan(EpisodeV2):
    BUILD_NO = 46
    FIRST_SET = "valley"
    CLEAR = "#16204C"
    TITLE = {"en": "ASWAN HIGH DAM", "ar_sa": "السد العالي"}
    EMPH = {"en": ["CONGRATS", "SEVENTEEN", "GREAT", "PYRAMIDS", "ROCK", "NILE", "ASWAN", "HIGH", "DAM", "SUMMER",
                   "FLOODS", "DROWNS", "VILLAGES", "BARELY", "BLOCK", "VALLEY", "TRAP", "FLOOD", "GIANT", "LAKE",
                   "SLOWLY", "YEAR", "WATER", "PUSHES", "KNOCK", "WALL", "HILL", "SAND", "KILOMETER", "THICK",
                   "BOTTOM", "SEEPS", "COFFEE", "FILTER", "CLAY", "CORE", "PUMP", "CEMENT", "DEEP", "RIVERBED",
                   "SNEAKS", "UNDER", "RIVER", "NEVER", "STOPS", "BLAST", "CHANNEL", "GRANITE", "AROUND", "CLOSE",
                   "GAP", "FOLLOW", "IGLOO", "FIVE", "HUNDRED", "KILOMETERS", "STATUES", "ABU", "SIMBEL", "CUT",
                   "LIFTED", "SAFETY", "ELEVEN", "METERS", "FOUR", "HALF", "EGYPT'S", "ELECTRICITY", "YOURSELF",
                   "SHAMPOO", "HAIR", "CUTS"],
            "ar_sa": ["مبروك", "كوّمت", "صخر", "سبعتاشر", "هرم", "النيل", "السد", "العالي", "بيفيض", "صيف", "يغرّق",
                      "القرى", "ميجيش", "فتقفل", "الوادي", "وتحبس", "الفيضان", "بحيرة", "بالراحة", "السنة", "بتزق",
                      "جامد", "حيطة", "هتقع", "جبل", "ورمل", "تخنه", "الكيلو", "بتنشّ", "القهوة", "الفلتر", "طين",
                      "وتحقن", "أسمنت", "قاع", "النهر", "متعديش", "وإزاي", "نهر", "وقف", "قناة", "الجرانيت", "تعدّي",
                      "تقفل", "الفتحة", "تابعني", "التلج", "خمسمية", "كيلو", "وتماثيل", "أبو", "سمبل", "تتقطّع",
                      "وتطلع", "الجبل", "ارتفاعه", "وحداشر", "متر", "أربعة", "نص", "كهربا", "مصر", "بإيدك", "تقطع",
                      "راسك", "شامبو"]}
    KEYS = {"ar_sa": {
        ("hook", "PILE"): "كوّمت", ("hook", "SEVENTEEN"): "سبعتاشر", ("hook", "PYRAMIDS"): "هرم", ("hook", "ROCK"): "صخر",
        ("hook", "NILE"): "النيل", ("hook", "CONGRATS"): "مبروك", ("hook", "ASWAN"): "السد",
        ("break1", "SUMMER"): "صيف", ("break1", "FLOODS"): "بيفيض", ("break1", "DROWNS"): "يغرّق",
        ("break1", "VILLAGES"): "القرى", ("break1", "NEXT"): "وسنة", ("break1", "BARELY"): "ميجيش",
        ("fix1", "BLOCK"): "فتقفل", ("fix1", "VALLEY"): "الوادي", ("fix1", "TRAP"): "وتحبس", ("fix1", "LAKE"): "بحيرة",
        ("fix1", "SLOWLY"): "بالراحة", ("fix1", "YEAR"): "السنة",
        ("break2", "WATER"): "المية", ("break2", "PUSHES"): "بتزق", ("break2", "KNOCK"): "هتقع", ("break2", "WALL"): "حيطة",
        ("fix2", "HILL"): "جبل", ("fix2", "ROCK"): "صخر", ("fix2", "SAND"): "ورمل", ("fix2", "KILOMETER"): "الكيلو",
        ("fix2", "BOTTOM"): "تحت",
        ("break3", "SEEPS"): "بتنشّ", ("break3", "COFFEE"): "القهوة", ("break3", "FILTER"): "الفلتر",
        ("fix3", "CLAY"): "طين", ("fix3", "CORE"): "قلبه", ("fix3", "PUMP"): "وتحقن", ("fix3", "CEMENT"): "أسمنت",
        ("fix3", "RIVERBED"): "قاع", ("fix3", "UNDER"): "تحت",
        ("break4", "HOW"): "وإزاي", ("break4", "RIVER"): "نهر", ("break4", "NEVER"): "عمره", ("break4", "STOPS"): "وقف",
        ("fix4", "BLAST"): "تفتح", ("fix4", "CHANNEL"): "قناة", ("fix4", "GRANITE"): "الجرانيت", ("fix4", "SEND"): "تعدّي",
        ("fix4", "AROUND"): "النيل", ("fix4", "CLOSE"): "تقفل", ("fix4", "GAP"): "الفتحة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "LAKE"): "بحيرة", ("reveal", "FIVE"): "خمسمية", ("reveal", "STATUES"): "وتماثيل",
        ("reveal", "ABU"): "أبو", ("reveal", "CUT"): "تتقطّع", ("reveal", "LIFTED"): "وتطلع", ("reveal", "SAFETY"): "الجبل",
        ("stat", "A"): "ارتفاعه", ("stat", "FOUR"): "أربعة", ("stat", "HALF"): "نص",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "HOLDS"): "بيحجز", ("tag", "WATER"): "والمية", ("tag", "CUTS"): "تقطع", ("tag", "HAIR"): "راسك",
        ("tag", "SHAMPOO"): "شامبو"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an igloo"),
                   "stat": [("111 m", "TALL"), ("3.8 km", "LONG"), ("50%", "OF EGYPT'S POWER, AT FIRST")],
                   "L": {"pyr": "{n} GREAT PYRAMIDS OF ROCK", "name": "THE ASWAN HIGH DAM", "much": "TOO MUCH WATER",
                         "little": "THEN TOO LITTLE", "block": "BLOCK THE VALLEY", "lake": "THE FLOOD WAITS IN A LAKE",
                         "slow": "OUT SLOWLY, ALL YEAR", "push": "IT PUSHES THE WALL OVER", "hill": "A HILL OF ROCK + SAND",
                         "km": "ALMOST 1 km THICK", "seep": "IT SEEPS THROUGH", "under": "AND UNDER IT",
                         "core": "CLAY CORE", "curtain": "CEMENT CURTAIN", "stops": "IT NEVER STOPS",
                         "blast": "BLAST A CHANNEL", "around": "THE NILE GOES AROUND", "gap": "CLOSE THE GAP",
                         "km500": "500 km LONG", "abu": "ABU SIMBEL", "cut": "CUT INTO 1,000+ BLOCKS",
                         "lift": "LIFTED 65 m UP", "nowater": "NO WATER!", "month": "EVERY MONTH",
                         "aug": "ALL IN SUMMER", "flood": "FLOOD"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: بيت من التلج"),
                      "stat": [("111", "متر ارتفاع"), ("3.8", "كيلو طول"), ("50%", "من كهربا مصر زمان")],
                      "L": {"pyr": "{n} هرم صخر", "name": "السد العالي", "much": "مية كتير قوي",
                            "little": "وبعدين مفيش", "block": "اقفل الوادي", "lake": "الفيضان يستنى في بحيرة",
                            "slow": "تنزل بالراحة طول السنة", "push": "المية تزق الحيطة", "hill": "جبل صخر ورمل",
                            "km": "تخنه قرب كيلو", "seep": "المية بتنش", "under": "ومن تحته كمان",
                            "core": "قلب طين", "curtain": "ستارة أسمنت", "stops": "النهر عمره ما وقف",
                            "blast": "افتح قناة في الجرانيت", "around": "النيل يلف منها", "gap": "اقفل الفتحة",
                            "km500": "500 كيلو طول", "abu": "أبو سمبل", "cut": "أكتر من 1000 حتة",
                            "lift": "طلعت 65 متر لفوق", "nowater": "المية قطعت!", "month": "كل شهر",
                            "aug": "كله في الصيف", "flood": "فيضان"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "pile": ("hook", "PILE", 0.05), "seventeen": ("hook", "SEVENTEEN", 0.12), "pyramids": ("hook", "PYRAMIDS", 0.25),
            "rock": ("hook", "ROCK", 0.38), "nile": ("hook", "NILE", 0.5), "congrats": ("hook", "CONGRATS", 0.6),
            "aswan": ("hook", "ASWAN", 0.85),
            "summer": ("break1", "SUMMER", 0.15), "floods": ("break1", "FLOODS", 0.3), "drowns": ("break1", "DROWNS", 0.5),
            "villages": ("break1", "VILLAGES", 0.6), "next": ("break1", "NEXT", 0.72), "barely": ("break1", "BARELY", 0.85),
            "block": ("fix1", "BLOCK", 0.1), "valley": ("fix1", "VALLEY", 0.2), "trap": ("fix1", "TRAP", 0.3),
            "lake": ("fix1", "LAKE", 0.55), "slowly": ("fix1", "SLOWLY", 0.8), "year": ("fix1", "YEAR", 0.92),
            "water": ("break2", "WATER", 0.15), "pushes": ("break2", "PUSHES", 0.3), "knock": ("break2", "KNOCK", 0.6),
            "wall": ("break2", "WALL", 0.85),
            "hill": ("fix2", "HILL", 0.2), "rock2": ("fix2", "ROCK", 0.35), "sand": ("fix2", "SAND", 0.45),
            "kilometer": ("fix2", "KILOMETER", 0.65), "bottom": ("fix2", "BOTTOM", 0.88),
            "seeps": ("break3", "SEEPS", 0.2), "coffee": ("break3", "COFFEE", 0.62), "filter": ("break3", "FILTER", 0.85),
            "clay": ("fix3", "CLAY", 0.2), "core": ("fix3", "CORE", 0.28), "pump": ("fix3", "PUMP", 0.4),
            "cement": ("fix3", "CEMENT", 0.48), "riverbed": ("fix3", "RIVERBED", 0.68), "under": ("fix3", "UNDER", 0.92),
            "how": ("break4", "HOW", 0.1), "river": ("break4", "RIVER", 0.5), "never": ("break4", "NEVER", 0.7),
            "stops": ("break4", "STOPS", 0.88),
            "blast": ("fix4", "BLAST", 0.05), "channel": ("fix4", "CHANNEL", 0.2), "granite": ("fix4", "GRANITE", 0.32),
            "send": ("fix4", "SEND", 0.55), "around": ("fix4", "AROUND", 0.65), "close": ("fix4", "CLOSE", 0.8),
            "gap": ("fix4", "GAP", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "lake2": ("reveal", "LAKE", 0.1), "five": ("reveal", "FIVE", 0.2), "statues": ("reveal", "STATUES", 0.5),
            "abu": ("reveal", "ABU", 0.58), "cut": ("reveal", "CUT", 0.7), "lifted": ("reveal", "LIFTED", 0.8),
            "safety": ("reveal", "SAFETY", 0.92),
            "s1": ("stat", "A", 0.04), "s2": ("stat", "FOUR", 0.4), "s3": ("stat", "HALF", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "holds": ("tag", "HOLDS", 0.05), "water2": ("tag", "WATER", 0.5), "cuts": ("tag", "CUTS", 0.62),
            "hair": ("tag", "HAIR", 0.8), "shampoo": ("tag", "SHAMPOO", 0.92)})
        T["fall"] = max(T["knock"], T["wall"]) - 0.25            # the wall goes over (both languages)
        T["drown0"] = min(T["drowns"], T["villages"])
        # the pyramids land one by one from 0.15 s to just before "congrats"
        n = 17
        t0, t1 = 0.15, max(1.6, T["congrats"] - 0.35)
        self.land = [lerp(t0, t1, i / (n - 1.0)) for i in range(n)]
        # ---- sets
        self.cut(s("break1") - 0.12, "valley", -1)
        self.cut(s("break2") - 0.12, "section", 1)
        self.cut(s("break4") - 0.12, "divert", -1)
        self.cut(s("reveal") - 0.12, "valley", 1)
        self.cut(T["statues"] - 0.15, "temple", -1)
        self.cut(s("stat") - 0.12, "valley", 1)
        self.cut(s("closer") - 0.12, "valley", -1)
        self.cut(s("tag") - 0.2, "shower", -1)
        # ---- valley camera
        cv = Camera(0, -40, 1.22)
        cv.key(0.2, 0, -50, 1.25, max(1.0, T["congrats"] - 0.3))
        cv.key(T["congrats"] - 0.1, 0, -70, 1.1, 1.4)
        cv.key(s("break1") - 0.12, -150, 200, 1.3, 0.0).key(s("break1"), -170, 210, 1.34, 4.0)
        cv.key(s("fix1") - 0.12, 0, 80, 0.98, 0.8).key(T["lake"] - 0.4, 0, -10, 0.96, 1.6)
        cv.key(s("reveal") - 0.12, 0, -40, 0.96, 0.0).key(s("reveal"), 0, -230, 0.78, 1.8)
        cv.key(s("stat") - 0.12, 0, 40, 0.9, 0.0).key(s("stat"), 0, 60, 0.94, 5.0)
        cv.key(s("closer") - 0.1, 0, -70, 1.18, 0.0).key(self.duration, 0, -80, 1.26, 4.0)
        self.cam = cv
        # ---- section camera
        cs = Camera(-60, -170, 1.0)
        cs.key(T["pushes"] - 0.2, -20, -160, 0.95, 0.8)
        cs.key(s("fix2") - 0.12, 0, 60, 0.6, 0.0).key(s("fix2"), 0, 60, 0.62, 3.0)
        cs.key(s("break3") - 0.12, 0, 80, 0.6, 0.0).key(s("break3"), 0, 90, 0.62, 3.0)
        cs.key(s("fix3") - 0.12, 0, 110, 0.6, 0.0).key(T["cement"], 0, 150, 0.6, 1.6)
        self.cam_sec = cs
        self.spans = [(T["barely"], T["year"] + 0.3), (T["fall"], T["bottom"] + 0.3), (T["filter"], T["under"] + 0.3),
                      (T["stops"], T["gap"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 9), (T["drown0"], 0.3, 6), (T["block"] + 0.2, 0.3, 7), (T["fall"] + 0.3, 0.4, 9),
                       (T["hill"] + 0.2, 0.3, 6), (T["blast"] + 0.1, 0.35, 8), (T["close"] + 0.1, 0.3, 6),
                       (s("closer") + 0.2, 0.35, 9), (T["cuts"], 0.3, 6)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def far(self, c, t, cam, dusk=0.0):
        cx, cy, z = cam
        gy = (HZ - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=gy)
        if dusk > 0:
            c.drawRect(R(0, 0, W, H), P("#0B1033", 0.55 * dusk))
            stars_sky(c, t, dusk * 0.8)
        sun(c, 820 - cx * 0.03, gy - 120 + 160 * dusk, 58, heat=0.4, a=1 - 0.6 * dusk)
        c.save()
        c.translate(W / 2 - cx * 0.05, gy)
        v2.ridge(c, -1700, 1700, 0, 90 * z, "#8E5A4A", "#5A3530", seed=31, step=110, rough=0.6)
        c.restore()
        return gy

    # ------------------------------------------------------------------ set: valley
    def valley_state(self, t):
        """(dam 0..1, lake 0..1, flood 0..1, dry 0..1, outflow 0..1, dusk 0..1) for the valley set at time t."""
        T, s = self.T, self.tl.s
        if t < s("break1") - 0.12:                                          # hook
            dam = e_out(prog(t, T["congrats"] - 0.3, T["congrats"] + 0.5))
            lake = e_io(prog(t, T["congrats"], T["aswan"] + 0.4))
            return dam, lake, 0.0, 0.0, lake, 0.0
        if t < s("fix1") - 0.12:                                            # break1: no dam yet
            fl = e_out(prog(t, T["floods"] - 0.2, T["drown0"] + 0.2)) * (1 - e_io(prog(t, T["next"] - 0.2, T["barely"])))
            dry = e_io(prog(t, T["next"] - 0.1, T["barely"] + 0.2))
            return 0.0, 0.0, fl, dry, 0.0, 0.0
        if t < s("break2") - 0.12:                                          # fix1
            dam = e_out(prog(t, T["block"] - 0.15, T["valley"] + 0.4))
            lake = e_io(prog(t, T["trap"] - 0.1, T["lake"] + 0.5))
            dry = 1 - e_io(prog(t, T["slowly"] - 0.4, T["slowly"] + 0.5))
            return dam, lake, 0.0, dry, prog(t, T["slowly"] - 0.4, T["slowly"] + 0.2), 0.0
        if t < s("stat") - 0.12:                                            # reveal
            return 1.0, 1.0, 0.0, 0.0, 1.0, 0.0
        if t < s("closer") - 0.1:                                           # stat at dusk
            return 1.0, 1.0, 0.0, 0.0, 1.0, prog(t, s("stat") - 0.1, s("stat") + 0.8)
        return 1.0, 1.0, 0.0, 0.0, 1.0, 0.0

    VILLAGES = [(-330, 170, 92, 54), (-450, 214, 80, 46), (-300, 290, 104, 60), (-480, 330, 90, 52),
                (320, 186, 90, 56), (450, 246, 84, 48), (350, 318, 98, 58), (500, 360, 80, 50)]

    def draw_valley(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        dam, lake, flood, dry, outflow, dusk = self.valley_state(t)
        self.far(c, t, cam, dusk)
        self.view(c, cam)
        land = mix(SAND, DRY, 0.3 * dry)
        c.drawRect(R(-3000, HZ, 6000, 4000), lin_paint(0, HZ, 0, 1400, [shade(land, -0.1), land, shade(land, -0.2)]))
        # granite hills along the valley sides, upstream of the dam
        for sd in (-1, 1):
            hp = skia.Path()
            hp.moveTo(sd * 3000, HZ - 30)
            y = HZ
            pts = []
            while y <= CREST + 60:
                pts.append((sd * (lake_half(y) + 30), y))
                y += 20
            hp.lineTo(sd * 3000, HZ)
            hp.lineTo(sd * lake_half(HZ), HZ - 20)
            for k, (x_, y_) in enumerate(pts):
                hp.lineTo(x_ + sd * 18 * math.sin(k * 1.7), y_ - 36 - 10 * math.sin(k * 0.9))
            hp.lineTo(sd * 3000, CREST + 120)
            hp.close()
            c.drawPath(hp, lin_paint(0, HZ, 0, CREST + 100, [GRANITE, shade(GRANITE, -0.2), GRANITE_D]))
            rng = random.Random(7 if sd < 0 else 8)
            for k in range(26):                                             # boulders
                y_ = rng.uniform(HZ + 20, CREST + 70)
                x_ = sd * (lake_half(y_) + rng.uniform(40, 260))
                r_ = rng.uniform(16, 40) * lerp(0.5, 1.0, (y_ - HZ) / (CREST - HZ + 70))
                c.drawOval(R(x_ - r_, y_ - r_ * 0.7, 2 * r_, 1.4 * r_), P(shade(GRANITE, rng.uniform(-0.2, 0.15))))
                c.drawOval(R(x_ - r_ * 0.6, y_ - r_ * 0.6, r_ * 0.9, r_ * 0.5), P("#8A6A60", 0.35))
        # upstream: the valley floor with the river (before) or the lake (after)
        floor = skia.Path()
        floor.moveTo(-lake_half(HZ), HZ)
        y = HZ
        while y <= CREST:
            floor.lineTo(-lake_half(y), y)
            y += 20
        floor.lineTo(lake_half(CREST), CREST)
        y = CREST
        while y >= HZ:
            floor.lineTo(lake_half(y), y)
            y -= 20
        floor.close()
        fl_col = mix(FIELD, DRY, dry)
        if lake < 1:
            c.save()
            c.clipPath(floor, doAntiAlias=True)
            rp = skia.Path()                                                # fields along the old river
            yy = HZ
            rp.moveTo(-up_half(HZ) * 3, HZ)
            while yy <= CREST + 10:
                rp.lineTo(-up_half(yy) * 3.2, yy)
                yy += 20
            while yy >= HZ:
                rp.lineTo(up_half(yy) * 3.2, yy)
                yy -= 20
            rp.close()
            c.drawPath(rp, P(fl_col, 0.9))
            c.restore()
        wp = skia.Path()                                                    # water upstream: river -> lake
        yy = HZ
        wp.moveTo(-lerp(up_half(HZ), lake_half(HZ), lake), HZ)
        while yy <= CREST:
            hw = lerp(up_half(yy) * (1 + 1.4 * flood) * (1 - 0.7 * dry), lake_half(yy) - 6, e_io(lake))
            wp.lineTo(-hw, yy)
            yy += 20
        while yy >= HZ:
            hw = lerp(up_half(yy) * (1 + 1.4 * flood) * (1 - 0.7 * dry), lake_half(yy) - 6, e_io(lake))
            wp.lineTo(hw, yy)
            yy -= 20
        wp.close()
        wc = mix(NILE, "#9C7A4A", 0.5 * dry * (1 - lake))
        c.drawPath(wp, lin_paint(0, HZ, 0, CREST, [shade(LAKE_C, 0.25), wc, shade(wc, -0.15)]))
        if lake > 0:                                                        # glints on the lake
            for k in range(28):
                gy_ = lerp(HZ + 20, CREST - 16, ((k * 0.37) % 1.0))
                gx_ = lake_half(gy_) * (((k * 0.61) % 1.0) * 1.6 - 0.8)
                gw = lerp(10, 50, (gy_ - HZ) / (CREST - HZ))
                ph = math.sin(t * 2.0 + k)
                c.drawLine(gx_ - gw + ph * 8, gy_, gx_ + gw + ph * 8, gy_, P("#E0F2FE", 0.45 * lake * (0.5 + 0.5 * ph),
                                                                             stroke=3))
            add_glow(c, 260, HZ + 30, 300, "#FFE7B0", 0.25 * lake * (1 - dusk))
            sxw = ((820 - cam[0] * 0.03) - W / 2) / cam[2] + cam[0]          # the sun's path on the water
            for k in range(24):
                gy_ = lerp(HZ + 8, CREST - 14, (k / 24.0) ** 1.3)
                if abs(sxw) > lake_half(gy_) - 20:
                    continue
                gw = lerp(14, 70, (gy_ - HZ) / (CREST - HZ)) * (0.6 + 0.4 * math.sin(t * 3 + k * 1.7))
                c.drawLine(sxw - gw, gy_, sxw + gw, gy_, P("#FFF1C9", 0.7 * lake * (1 - dusk), stroke=4))
        c.drawRect(R(-3000, HZ - 4, 6000, 110), lin_paint(0, HZ - 4, 0, HZ + 106, [("#FFD58C", 0.5 * (1 - dusk)),
                                                                                  ("#FFD58C", 0.0)]))
        # downstream: fields, palms, villages, the river
        dpf = skia.Path()
        yy = TOE - 20
        dpf.moveTo(-dn_half(yy) - 260, yy)
        while yy <= 1500:
            dpf.lineTo(-dn_half(yy) - 260 - (yy - TOE) * 0.25, yy)
            yy += 40
        while yy >= TOE - 20:
            dpf.lineTo(dn_half(yy) + 260 + (yy - TOE) * 0.25, yy)
            yy -= 40
        dpf.close()
        c.drawPath(dpf, lin_paint(0, TOE, 0, 1300, [shade(fl_col, 0.08), fl_col, shade(fl_col, -0.15)]))
        for k in range(7):                                                  # field furrows
            yy = TOE + 40 + k * 90
            for sd in (-1, 1):
                c.drawLine(sd * (dn_half(yy) + 20), yy, sd * (dn_half(yy) + 250 + (yy - TOE) * 0.25), yy,
                           P(shade(fl_col, -0.25), 0.5, stroke=3))
        if dry > 0.3:                                                       # cracks in the dry fields
            rng = random.Random(3)
            for k in range(40):
                sd = -1 if k % 2 else 1
                x0 = sd * rng.uniform(140, 520)
                y0 = rng.uniform(TOE + 30, 700)
                pth = skia.Path()
                pth.moveTo(x0, y0)
                for j in range(4):
                    x0, y0 = x0 + rng.uniform(-30, 30), y0 + rng.uniform(-14, 14)
                    pth.lineTo(x0, y0)
                c.drawPath(pth, P("#5E3F20", 0.7 * (dry - 0.3) / 0.7, stroke=2.5))
        rp = skia.Path()                                                    # the river below the dam
        yy = TOE - 30
        hw0 = (1 + 2.2 * flood) * (1 - 0.7 * dry)
        rp.moveTo(-dn_half(yy) * hw0, yy)
        while yy <= 1500:
            rp.lineTo(-dn_half(yy) * hw0, yy)
            yy += 40
        while yy >= TOE - 30:
            rp.lineTo(dn_half(yy) * hw0, yy)
            yy -= 40
        rp.close()
        rcol = mix(mix(NILE, "#9C6631", clamp(flood * 1.5)), "#B08552", dry)
        c.drawPath(rp, lin_paint(0, TOE, 0, 1300, [shade(rcol, 0.15), rcol, shade(rcol, -0.3)]))
        if dry > 0.2:                                                       # the thin thread of water left
            tp_ = skia.Path()
            tp_.moveTo(0, TOE)
            for k in range(1, 14):
                yy = TOE + k * 100
                tp_.lineTo(18 * math.sin(k * 1.3), yy)
            c.drawPath(tp_, P(NILE, (dry - 0.2) / 0.8, stroke=10))
        for k in range(14):                                                 # flow streaks
            q = (t * (0.25 + 0.2 * flood) + k / 14.0) % 1.0
            yy = lerp(TOE + 10, 1300, q)
            xx = dn_half(yy) * hw0 * (((k * 0.53) % 1.0) * 1.4 - 0.7)
            c.drawLine(xx, yy, xx, yy + 30 + 30 * q, P("#BFDBFE", 0.5 * (1 - dry * 0.7), stroke=3))
        for i in range(14):                                                 # palms along the banks
            sd = -1 if i % 2 else 1
            yy = TOE + 80 + (i // 2) * 120
            xx = sd * (dn_half(yy) + 60 + (i % 3) * 40)
            palm(c, xx, yy, 120 + (i % 3) * 18, sway=math.sin(t * 1.2 + i) * 0.3, a=1 - 0.5 * dry)
        lit = 0.9 * dusk
        for i, (vx, vy, vw, vh) in enumerate(self.VILLAGES):
            reach = dn_half(vy) * (1 + 2.2 * flood)
            sub = clamp((reach - (abs(vx) - vw / 2)) / vw) * 0.7 if flood > 0.05 else 0.0
            village_house(c, vx, vy, vw, vh, lit=lit, sub=sub, seed=i)
        if flood > 0.05:                                                    # flood water over the fields
            for k in range(10):
                yy = TOE + 60 + k * 70
                for sd in (-1, 1):
                    xx = sd * dn_half(yy) * (1 + 2.2 * flood) * 0.85
                    c.drawLine(xx - 20, yy, xx + 20, yy, P("#BFDBFE", 0.6 * flood, stroke=3))
        # the pyramids (hook)
        if t < s("break1") - 0.12:
            fade = 1 - prog(t, T["congrats"] - 0.1, T["congrats"] + 0.45)
            for i in range(17):
                row = i % 2                                                 # 0 = back row (9), 1 = front row (8)
                j = i // 2
                if row == 0:
                    x_, y_, sc = -520 + j * 130, -110, 1.35
                else:
                    x_, y_, sc = -455 + j * 130, -30, 1.55
                k = prog(t, self.land[i] - 0.28, self.land[i])
                if k <= 0:
                    continue
                drop = (1 - e_in(k)) * 520
                mini_pyramid(c, x_, y_ - drop, sc, a=fade, lit=1 - dusk)
                if 0 < t - self.land[i] < 0.6:                              # dust where it lands
                    q = prog(t, self.land[i], self.land[i] + 0.6)
                    for sd in (-1, 1):
                        c.drawCircle(x_ + sd * (30 + 50 * q), y_ - 6, 14 + 16 * q, P("#E9CFA0", 0.6 * (1 - q) * fade))
        # the dam
        if dam > 0:
            top = lerp(TOE + 4, CREST, e_out(dam))
            c.save()
            c.clipRect(R(-3000, top, 6000, TOE - top + 6))
            fp = skia.Path()
            fp.moveTo(-760, CREST)
            fp.lineTo(760, CREST)
            fp.lineTo(840, TOE)
            fp.lineTo(-840, TOE)
            fp.close()
            c.drawPath(fp, lin_paint(0, CREST, 0, TOE, ["#D8C7AE", "#B8A48C", "#8C7A66", "#6E5E50"],
                                     [0.0, 0.35, 0.8, 1.0]))
            tex(c, fp, "stone", 0.7, 0.35)
            for k in range(1, 5):                                           # the stepped berms
                yy = lerp(CREST, TOE, k / 5.0)
                xw = 760 + 80 * k / 5.0
                c.drawRect(R(-xw, yy - 5, 2 * xw, 7), P("#E7DCCB", 0.55))
                c.drawLine(-xw, yy + 3, xw, yy + 3, P("#5E5248", 0.6, stroke=3))
            for sd in (-1, 1):                                              # the ends meet the granite hills
                ab = skia.Path()
                ab.moveTo(sd * 700, CREST - 40)
                ab.quadTo(sd * 820, CREST - 90, sd * 1300, CREST - 120)
                ab.lineTo(sd * 1300, TOE + 30)
                ab.lineTo(sd * 840, TOE + 10)
                ab.close()
                c.drawPath(ab, lin_paint(0, CREST - 120, 0, TOE, [shade(GRANITE, 0.1), GRANITE_D]))
            c.drawRect(R(-760, CREST - 16, 1520, 18), P("#EFE8DC"))         # the road on the crest
            c.drawLine(-760, CREST - 16, 760, CREST - 16, P("#94A3B8", stroke=3))
            for k in range(17):
                lx = -720 + k * 90
                c.drawLine(lx, CREST - 16, lx, CREST - 40, P("#CBD5E1", stroke=3))
                c.drawCircle(lx, CREST - 42, 5, P("#FDE68A", 0.4 + 0.6 * dusk))
                if dusk > 0:
                    add_glow(c, lx, CREST - 38, 28, "#FDE68A", 0.8 * dusk)
            c.drawRect(R(120, TOE - 48, 380, 48), lin_paint(0, TOE - 48, 0, TOE, ["#F1EDE6", "#A8A29E"]))   # power house
            for k in range(12):
                wx = 136 + k * 30
                c.drawRect(R(wx, TOE - 34, 16, 12), P("#1E293B"))
                if dusk > 0:
                    c.drawRect(R(wx, TOE - 34, 16, 12), P("#FDE68A", dusk))
            c.restore()
            if outflow > 0:                                                 # water out of the turbines, steady
                for k in range(12):
                    wx = 144 + k * 30
                    q = (t * 1.6 + k * 0.17) % 1.0
                    c.drawLine(wx, TOE + 2, wx - 60 * q, TOE + 30 + 60 * q, P("#E0F2FE", 0.75 * outflow * (1 - q), stroke=5))
                add_glow(c, 300, TOE + 20, 160, "#BAE6FD", 0.25 * outflow)
            if dusk > 0:
                add_glow(c, 310, TOE - 20, 260, "#FDE68A", 0.35 * dusk)
        if dusk > 0:                                                        # power lines lighting the valley
            for k in range(4):
                py = TOE + 120 + k * 200
                pylon(c, 620 + k * 40, py, 0.8 + 0.25 * k)
            for k in range(3):
                x0, y0 = 620 + k * 40, TOE + 120 + k * 200 - 100 * (0.8 + 0.25 * k)
                x1, y1 = 660 + k * 40, TOE + 320 + k * 200 - 100 * (0.8 + 0.25 * (k + 1))
                c.drawLine(x0, y0, x1, y1, P("#FDE68A", 0.7 * dusk, stroke=2))
                q = (t * 0.8 + k * 0.3) % 1.0
                add_glow(c, lerp(x0, x1, q), lerp(y0, y1, q), 30, "#FDE68A", dusk)
        c.restore()
        self.ui["cam"] = cam
        self.ui["state"] = (dam, lake, flood, dry, outflow, dusk)

    def months(self, c, x, y, even, a):
        """Twelve month bars: one huge flood in summer (even = 0) or the same every month (even = 1)."""
        if a <= 0:
            return
        c.drawRRect(rr(x - 290, y - 140, 580, 210, 26), P(GLASS, 0.82 * a))
        flood = [0.06, 0.05, 0.04, 0.04, 0.05, 0.08, 0.3, 1.0, 0.9, 0.35, 0.12, 0.07]
        for k in range(12):
            hgt = lerp(flood[k], 0.42, even) * 112
            bx = x - 250 + k * 42
            col = mix("#FB923C" if flood[k] > 0.5 else "#60A5FA", "#34D399", even)
            c.drawRRect(rr(bx, y + 46 - hgt, 28, hgt, 6), P(col, a))
        lab = self.L["month"] if even > 0.5 else self.L["aug"]
        word(c, lab, x, y - 100, 30, INK, a=a)

    def ui_valley(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam.at(tw))
        if tw < s("break1") - 0.12:
            n = sum(1 for tl_ in self.land if tw >= tl_)
            if n > 0:
                k = self.span(self.land[0], T["congrats"] - 0.05, 0.2, 0.25)
                if k > 0:
                    v2.chip(c, 540, 420, self.L["pyr"].format(n=n), k, accent=HILITE, size=40)
            self.chip(540, 420, "name", T["aswan"] - 0.15, s("break1") + 0.1, accent=HILITE, size=46)
            return
        if tw < s("fix1") - 0.12:
            self.chip(540, 420, "much", T["floods"] - 0.1, T["next"] - 0.1, accent="#60A5FA", size=42)
            self.chip(540, 420, "little", T["next"] - 0.1, s("fix1") - 0.15, accent="#FB923C", size=42)
            self.months(c, 540, 640, 0.0, self.span(T["floods"], s("fix1") - 0.15))
            self.badge("alert", T["barely"] + 0.05, s("fix1") - 0.2, x=880, y=520)
            self.red(T["drown0"], 1.2)
            return
        if tw < s("break2") - 0.12:
            dx, dy = self.at(cam, -300, CREST + 40)
            self.label(dx, dy, 300, 760, "block", T["block"] - 0.1, T["trap"] - 0.1, HILITE, size=38)
            self.chip(540, 420, "lake", T["trap"] - 0.1, T["slowly"] - 0.15, accent="#60A5FA", size=40)
            self.chip(540, 420, "slow", T["slowly"] - 0.15, s("break2") - 0.15, accent=GOOD, size=40)
            ev = e_io(prog(tw, T["slowly"] - 0.3, T["year"] + 0.2))
            self.months(c, 540, 640, ev, self.span(T["slowly"] - 0.3, s("break2") - 0.15))
            self.badge("check", T["year"] + 0.05, s("break2") - 0.15, x=880, y=520)
            return
        if tw < s("stat") - 0.12:
            lx, ly = self.at(cam, 120, HZ + 120)
            self.label(lx, ly, 760, 520, "km500", T["five"] - 0.1, T["statues"] - 0.1, "#60A5FA", size=40)

    # ------------------------------------------------------------------ set: section (break2..fix3)
    LAKE_Y = -380.0
    DH = 430.0

    @staticmethod
    def x_up(y):
        return lerp(-700, -40, clamp(-y / 430.0))

    @staticmethod
    def x_dn(y):
        return lerp(700, 40, clamp(-y / 430.0))

    def paths(self):
        """Seepage paths: through the body of the dam and under it, (points, barrier x)."""
        out = []
        for h in (-70.0, -150.0, -230.0, -310.0):
            pts = [(self.x_up(h) - 260, h), (self.x_up(h), h), (self.x_dn(h + 30), h + 30), (self.x_dn(h + 30) + 60, -20)]
            core_x = lerp(-150, -30, clamp(-h / 415.0))
            out.append((pts, core_x, "body"))
        for d in (90.0, 200.0, 330.0):
            pts = [(-1100, 30), (-650, d), (650, d), (900, 20)]
            out.append((pts, -26.0, "under"))
        return out

    @staticmethod
    def along(pts, u):
        segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
        L_ = sum(segs) * clamp(u)
        for (a, b), sl in zip(zip(pts, pts[1:]), segs):
            if L_ <= sl:
                k = L_ / max(sl, 1e-6)
                return lerp(a[0], b[0], k), lerp(a[1], b[1], k)
            L_ -= sl
        return pts[-1]

    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam_sec.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=gy - 40)
        sun(c, 860, gy - 520 * z - 200, 56, heat=0.4)
        c.save()
        c.translate(W / 2 - cx * 0.05, gy - 10)
        v2.ridge(c, -1700, 1700, 0, 160 * z, "#8E5A4A", "#5A3530", seed=33, step=110, rough=0.6)
        c.restore()
        self.view(c, cam)
        wallmode = t < s("fix2") - 0.12
        c.drawRect(R(-3000, 0, 6000, 460), lin_paint(0, 0, 0, 460, [BED, shade(BED, -0.3)]))
        rng = random.Random(5)
        for k in range(160):                                                # sand and gravel
            px, py = rng.uniform(-2400, 2400), rng.uniform(8, 450)
            c.drawCircle(px, py, rng.uniform(3, 9), P(shade(BED, rng.uniform(-0.35, 0.2)), 0.8))
        c.drawRect(R(-3000, 460, 6000, 2000), lin_paint(0, 460, 0, 1300, [GRANITE, GRANITE_D]))
        for k in range(90):
            px, py = rng.uniform(-2400, 2400), rng.uniform(470, 1200)
            c.drawCircle(px, py, rng.uniform(2, 6), P("#C9A4A0", 0.35))
        c.drawLine(-3000, 460, 3000, 460, P("#2A1C1A", 0.6, stroke=6))
        if wallmode:
            fall = e_in(prog(t, T["fall"], T["fall"] + 0.7))
            lvl = self.LAKE_Y + 200 * fall
            lake = skia.Path()
            lake.moveTo(-3000, lvl)
            lake.lineTo(-22 + 380 * fall, lvl + 60 * fall)
            lake.lineTo(-22 + 380 * fall, 0)
            lake.lineTo(-3000, 0)
            lake.close()
            c.drawPath(lake, lin_paint(0, self.LAKE_Y, 0, 0, [shade(LAKE_C, 0.15), LAKE_D]))
            if fall > 0:                                                    # the surge on the far side
                sp = skia.Path()
                sp.moveTo(-10, -140 * fall)
                sp.quadTo(400 * fall, -120 * fall, 1100 * fall, -10)
                sp.lineTo(1100 * fall, 0)
                sp.lineTo(-10, 0)
                sp.close()
                c.drawPath(sp, P(LAKE_C, 0.9))
                splash(c, 1100 * fall, -20, t, T["fall"] + 0.2, dur=0.9, n=24, speed=600)
            else:
                c.drawRect(R(20, -40, 3000, 40), lin_paint(0, -40, 0, 0, [LAKE_C, LAKE_D]))
            pk = self.span(T["pushes"] - 0.3, T["fall"] + 0.2)
            for k in range(4):                                              # the push
                yy = -60 - k * 80
                q = (t * 1.5 + k * 0.25) % 1.0
                arrow(c, -360 + 120 * q, yy, -60 + 20 * q, yy, "#BFDBFE", a=pk * (0.4 + 0.6 * (1 - q)), w=12, head=28)
            c.save()
            c.translate(20, 0)
            c.rotate(76 * fall)
            c.drawRect(R(-42, -420, 42, 420), lin_paint(-42, 0, 0, 0, ["#D1D5DB", "#9CA3AF"]))
            c.drawRect(R(-42, -420, 42, 420), P("#6B7280", stroke=3))
            for k in range(1, 7):
                c.drawLine(-42, -k * 60, 0, -k * 60, P("#6B7280", 0.6, stroke=2))
            c.restore()
            c.restore()
            self.ui["cam"] = cam
            return
        # the hill (fix2 on)
        lake = skia.Path()
        lake.moveTo(-3000, self.LAKE_Y)
        lake.lineTo(self.x_up(self.LAKE_Y), self.LAKE_Y)
        lake.lineTo(-700, 0)
        lake.lineTo(-3000, 0)
        lake.close()
        c.drawPath(lake, lin_paint(0, self.LAKE_Y, 0, 0, [shade(LAKE_C, 0.15), LAKE_D]))
        for k in range(10):
            q = (t * 0.15 + k * 0.1) % 1.0
            c.drawLine(-2200 + q * 1400, self.LAKE_Y + 8, -2140 + q * 1400, self.LAKE_Y + 8, P("#E0F2FE", 0.5, stroke=3))
        dn = skia.Path()
        dn.moveTo(self.x_dn(-40), -40)
        dn.lineTo(3000, -40)
        dn.lineTo(3000, 0)
        dn.lineTo(700, 0)
        dn.close()
        c.drawPath(dn, lin_paint(0, -40, 0, 0, [LAKE_C, LAKE_D]))
        hk = e_out(prog(t, T["hill"] - 0.35, max(T["sand"], T["rock2"]) + 0.5))
        top = -self.DH * hk
        body = skia.Path()
        body.moveTo(-700, 0)
        body.lineTo(-40, -self.DH)
        body.lineTo(40, -self.DH)
        body.lineTo(700, 0)
        body.close()
        c.save()
        c.clipRect(R(-3000, top, 6000, 3000))
        c.drawPath(body, lin_paint(-700, 0, 700, 0, [shade(DAM, 0.12), DAM, DAM_D]))
        rng = random.Random(11)
        for k in range(220):                                                # rock and sand fill
            px, py = rng.uniform(-680, 680), rng.uniform(-420, -6)
            if self.x_up(py) + 12 < px < self.x_dn(py) - 12:
                c.drawCircle(px, py, rng.uniform(5, 15), P(shade(DAM, rng.uniform(-0.3, 0.25)), 0.85))
        c.drawPath(body, P("#4A4038", stroke=4))
        ck = e_out(prog(t, min(T["clay"], T["core"]) - 0.2, max(T["clay"], T["core"]) + 0.5)) if t >= s("fix3") - 0.12 else 0.0
        if ck > 0:                                                          # the clay core
            core = skia.Path()
            core.moveTo(-150, 0)
            core.lineTo(-30, -415)
            core.lineTo(30, -415)
            core.lineTo(150, 0)
            core.close()
            c.save()
            c.clipRect(R(-3000, -415 * ck, 6000, 3000))
            c.drawPath(core, lin_paint(-150, 0, 150, 0, [shade(CLAY, 0.15), CLAY, shade(CLAY, -0.25)]))
            tex(c, core, "grain", 0.6, 0.3)
            c.restore()
        c.restore()
        if 0 < hk < 1:                                                      # rock falling onto the growing hill
            for k in range(14):
                q = (t * 1.8 + k / 14.0) % 1.0
                px = lerp(-560, 560, (k * 0.37) % 1.0)
                c.drawCircle(px, lerp(-700, top, q), 9, P(shade(DAM, -0.1), 0.9))
        if t >= s("fix3") - 0.12:                                           # the cement curtain
            gk = e_io(prog(t, min(T["pump"], T["cement"]) - 0.1, T["riverbed"] + 0.5))
            if gk > 0:
                c.drawRect(R(-26, 0, 52, 460 * gk), lin_paint(-26, 0, 26, 0, [shade(CEMENT, 0.1), CEMENT, shade(CEMENT, -0.25)]))
                c.drawRect(R(-26, 0, 52, 460 * gk), P("#6B7280", stroke=3))
                for k in range(int(9 * gk)):
                    c.drawCircle(lerp(-14, 14, (k * 0.61) % 1.0), 30 + k * 48, 8, P("#E5E7EB", 0.8))
            rk = self.span(min(T["pump"], T["cement"]) - 0.3, s("break4"))
            if rk > 0:                                                      # the drill rig on the crest
                c.drawLine(-36, -self.DH, 0, -self.DH - 120, P("#F59E0B", rk, stroke=6))
                c.drawLine(36, -self.DH, 0, -self.DH - 120, P("#F59E0B", rk, stroke=6))
                c.drawLine(0, -self.DH - 120, 0, 460 * gk, P("#475569", rk * 0.8, stroke=4))
                beacon(c, 0, -self.DH - 124, t)
        if t >= s("break3") - 0.12:                                         # seepage
            fixed = t >= s("fix3") - 0.12
            ck2 = e_out(prog(t, min(T["clay"], T["core"]) - 0.2, max(T["clay"], T["core"]) + 0.5)) if fixed else 0.0
            gk2 = e_io(prog(t, min(T["pump"], T["cement"]) - 0.1, T["riverbed"] + 0.5)) if fixed else 0.0
            sk = prog(t, T["seeps"] - 0.3, T["seeps"] + 0.3)
            for pi, (pts, bx, kind) in enumerate(self.paths()):
                blocked = (ck2 > 0.8) if kind == "body" else (gk2 * 460 > pts[1][1])
                for j in range(7):
                    u = (t * 0.32 + j / 7.0 + pi * 0.13) % 1.0
                    x_, y_ = self.along(pts, u)
                    a_ = sk
                    if blocked and x_ > bx - 10:
                        x_ = bx - 14 - j * 3
                        a_ = sk * 0.5 * (1 - prog(t, T["under"], T["under"] + 1.0) * 0.5)
                    c.drawCircle(x_, y_, 9, P("#60A5FA", a_))
                    add_glow(c, x_, y_, 22, "#93C5FD", 0.5 * a_)
            if not fixed or ck2 < 0.8:                                      # wet patches on the dry side
                wk = prog(t, T["seeps"], T["coffee"])
                for k in range(4):
                    yy = -60 - k * 80
                    c.drawOval(R(self.x_dn(yy) - 40, yy - 12, 70, 26), P("#1E3A8A", 0.45 * wk * (1 - ck2)))
        c.restore()
        self.ui["cam"] = cam

    def filter_icon(self, c, x, y, a):
        if a <= 0:
            return
        c.drawRRect(rr(x - 110, y - 120, 220, 240, 28), P(GLASS, 0.85 * a))
        fp = skia.Path()
        fp.moveTo(x - 70, y - 80)
        fp.lineTo(x + 70, y - 80)
        fp.lineTo(x + 14, y + 10)
        fp.lineTo(x - 14, y + 10)
        fp.close()
        c.drawPath(fp, P("#F5F5F4", a))
        c.drawRect(R(x - 66, y - 80, 132, 22), P("#6B3E26", a))
        for k in range(3):
            q = (self._t * 1.4 + k / 3.0) % 1.0
            c.drawCircle(x, y + 14 + q * 70, 7, P("#7C4A2D", a * (1 - q)))
        c.drawRRect(rr(x - 46, y + 60, 92, 46, 10), P("#E7E5E4", a))
        c.drawRect(R(x - 40, y + 76, 80, 26), P("#6B3E26", a))

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam_sec.at(tw))
        if tw < s("fix2") - 0.12:
            self.chip(540, 420, "push", T["pushes"] - 0.15, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["fall"] + 0.2, s("fix2") - 0.2, x=880, y=520)
            self.red(T["fall"] + 0.2, 1.2)
            return
        if tw < s("break3") - 0.12:
            hx, hy = self.at(cam, 300, -200)
            self.label(hx, hy, 760, 560, "hill", T["hill"] - 0.1, s("break3") - 0.15, HILITE, size=38)
            k = self.span(min(T["kilometer"], T["bottom"]) - 0.2, s("break3") - 0.15)
            if k > 0:                                                       # the base ruler
                x0, y0 = self.at(cam, -700, 30)
                x1, _ = self.at(cam, 700, 30)
                c.drawLine(x0, y0, x1, y0, P(HILITE, k, stroke=6))
                for xx in (x0, x1):
                    c.drawLine(xx, y0 - 18, xx, y0 + 18, P(HILITE, k, stroke=6))
                v2.chip(c, 540, y0 + 64, self.L["km"], k, accent=HILITE, size=38)
            self.badge("check", T["bottom"] + 0.1, s("break3") - 0.15, x=880, y=520)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 420, "seep", T["seeps"] - 0.15, s("fix3") - 0.15, accent="#60A5FA", size=40)
            self.filter_icon(c, 860, 640, self.span(T["coffee"] - 0.2, s("fix3") - 0.15))
            self.badge("alert", T["filter"] + 0.05, s("fix3") - 0.2, x=880, y=470)
            self.red(T["filter"] + 0.05, 1.2)
            return
        kx, ky = self.at(cam, -80, -250)
        self.label(kx, ky, 270, 560, "core", min(T["clay"], T["core"]) - 0.1, s("break4") - 0.15, "#FDBA74", size=38)
        gx, gy_ = self.at(cam, 20, 300)
        self.label(gx, gy_, 800, 560, "curtain", min(T["pump"], T["cement"]) + 0.1, s("break4") - 0.15, "#E5E7EB", size=38)
        self.badge("check", T["under"] + 0.05, s("break4") - 0.15, x=880, y=420)

    # ------------------------------------------------------------------ set: divert (break4, fix4), seen from above
    @staticmethod
    def rx(y):
        return 50 * math.sin(y / 600.0)

    CHAN = [(150, -560), (300, -430), (460, -180), (500, 100), (380, 380), (160, 560)]

    def draw_divert(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = (lerp(20, 170, e_io(prog(t, s("fix4") - 0.12, s("fix4") + 0.6))), -20, 0.92)
        vrect(c, 0, 0, W, H, ["#D9A866", "#C99556"])
        self.view(c, cam)
        rng = random.Random(21)
        for k in range(40):                                                 # dunes on the west bank
            y0 = rng.uniform(-1200, 1200)
            c.drawLine(-900, y0, -200, y0 + rng.uniform(-40, 40), P("#B9813F", 0.3, stroke=5))
        gp = skia.Path()                                                    # the granite east bank
        gp.moveTo(self.rx(-1300) + 175, -1300)
        yy = -1300
        while yy <= 1300:
            gp.lineTo(self.rx(yy) + 175 + 14 * math.sin(yy / 47.0), yy)
            yy += 40
        gp.lineTo(1400, 1300)
        gp.lineTo(1400, -1300)
        gp.close()
        c.drawPath(gp, lin_paint(0, 0, 1400, 0, [shade(GRANITE, 0.15), GRANITE, GRANITE_D]))
        for k in range(70):
            bx_, by_ = rng.uniform(260, 1200), rng.uniform(-1200, 1200)
            r_ = rng.uniform(14, 44)
            c.drawCircle(bx_, by_, r_, P(shade(GRANITE, rng.uniform(-0.25, 0.2))))
            c.drawCircle(bx_ - r_ * 0.3, by_ - r_ * 0.3, r_ * 0.4, P("#8A6A60", 0.4))
        bk = e_io(prog(t, T["blast"] - 0.1, T["granite"] + 0.5)) if fixed else 0.0
        wk = e_io(prog(t, min(T["send"], T["around"]) - 0.2, max(T["send"], T["around"]) + 0.4)) if fixed else 0.0
        gk = e_out(prog(t, T["close"] - 0.2, T["gap"] + 0.2)) if fixed else 0.0
        pts = self.CHAN
        if bk > 0:                                                          # the trench, then water in it
            cp = skia.Path()
            n = 40
            for i in range(n + 1):
                x_, y_ = self.along(pts, i / float(n) * bk)
                (cp.moveTo if i == 0 else cp.lineTo)(x_, y_)
            c.drawPath(cp, P("#2A1A14", stroke=120))
            c.drawPath(cp, P("#4A3028", stroke=96))
            if wk > 0:
                wp = skia.Path()
                for i in range(n + 1):
                    x_, y_ = self.along(pts, i / float(n) * wk)
                    (wp.moveTo if i == 0 else wp.lineTo)(x_, y_)
                c.drawPath(wp, P(NILE, stroke=80))
                for j in range(10):
                    u = (t * 0.35 + j / 10.0) % 1.0
                    if u < wk:
                        x_, y_ = self.along(pts, u)
                        c.drawCircle(x_, y_, 8, P("#BFDBFE", 0.8))
        rv = skia.Path()                                                    # the river
        yy = -1300
        rv.moveTo(self.rx(yy) - 150, yy)
        while yy <= 1300:
            rv.lineTo(self.rx(yy) - 150, yy)
            yy += 40
        while yy >= -1300:
            rv.lineTo(self.rx(yy) + 150, yy)
            yy -= 40
        rv.close()
        c.drawPath(rv, lin_paint(-200, 0, 200, 0, [NILE_D, NILE, NILE_D]))
        if gk > 0:                                                          # the old bed drains behind the barrier
            dp = skia.Path()
            yy = -300
            dp.moveTo(self.rx(yy) - 150, yy)
            while yy <= 540:
                dp.lineTo(self.rx(yy) - 150, yy)
                yy += 40
            while yy >= -300:
                dp.lineTo(self.rx(yy) + 150, yy)
                yy -= 40
            dp.close()
            c.drawPath(dp, P("#B58A55", 0.9 * gk))
        speed = 1.6 if not fixed else lerp(1.6, 0.9, gk)
        for k in range(26):                                                 # flow streaks
            q = (t * speed * 0.5 + k / 26.0) % 1.0
            yy = lerp(-1300, 1300, q)
            if gk > 0.5 and -300 < yy < 540:
                continue
            xx = self.rx(yy) + (((k * 0.47) % 1.0) * 220 - 110)
            c.drawLine(xx, yy, xx, yy + 70, P("#DBEAFE", 0.6, stroke=4))
        if gk > 0:                                                          # the barrier of rock
            for k in range(int(26 * gk)):
                bx_ = self.rx(-300) - 160 + (k % 13) * 26
                by_ = -320 + (k // 13) * 28
                c.drawCircle(bx_, by_, 17, P(shade(DAM, (k % 5) * 0.05 - 0.1)))
        if not fixed:                                                       # break4: rocks thrown in are swept away
            tx_, ty_ = -330, -260
            for sd in (-1, 1):                                              # wheels
                for wx in (-150, -40, 50):
                    c.drawRRect(rr(tx_ + wx - 18, ty_ + sd * 62 - 12, 36, 24, 6), P("#111827"))
            c.drawRRect(rr(tx_ - 200, ty_ - 58, 110, 116, 20), lin_paint(0, ty_ - 58, 0, ty_ + 58, ["#FCD34D", "#F59E0B", "#B45309"]))
            c.drawRRect(rr(tx_ - 130, ty_ - 44, 30, 88, 8), P("#1E293B", 0.85))
            tilt = 0.5 + 0.5 * math.sin(t * 3.0)
            c.drawRRect(rr(tx_ - 84, ty_ - 64, 184 + 14 * tilt, 128, 14), lin_paint(tx_ - 84, 0, tx_ + 100, 0, ["#94A3B8", "#475569"]))
            for k in range(5):
                c.drawCircle(tx_ - 50 + k * 30, ty_ - 20 + (k % 2) * 34, 15, P("#9CA3AF"))
            for k in range(16):
                t0 = s("break4") + 0.05 + k * 0.17
                if t < t0:
                    continue
                q = t - t0
                fly = min(1.0, q / 0.35)
                xr = lerp(tx_ + 100, self.rx(ty_) - 110 + (k % 4) * 55, fly)
                yr = ty_ - 20 + (k % 3) * 22 - math.sin(fly * math.pi) * 60 + max(0.0, q - 0.35) * 1100
                xr += max(0.0, q - 0.35) * 40 * math.sin(k)
                ak = 1 - prog(q, 1.2, 1.8)
                c.drawCircle(xr, yr, 18, P("#9CA3AF", ak))
                c.drawCircle(xr, yr, 18, P("#4B5563", ak, stroke=3))
            for k in range(3):                                              # the current
                q = (t * 0.9 + k / 3.0) % 1.0
                yy = lerp(-700, 900, q)
                arrow(c, self.rx(yy), yy - 120, self.rx(yy), yy + 60, "#E0F2FE", a=0.85 * (1 - abs(q - 0.5) * 1.6), w=16, head=40)
        else:                                                               # fix4: the blasts along the channel
            for i in range(6):
                tb = T["blast"] + i * 0.16
                if tb <= t < tb + 1.0:
                    x_, y_ = self.along(pts, (i + 0.5) / 6.0)
                    q = prog(t, tb, tb + 1.0)
                    add_glow(c, x_, y_, 140 * (1 - q) + 40, "#FDBA74", 0.9 * (1 - q))
                    for j in range(6):
                        an = j * 1.05 + i
                        c.drawCircle(x_ + math.cos(an) * 110 * q, y_ + math.sin(an) * 110 * q, 26 * (1 - q) + 8,
                                     P("#D6C4B0", 0.7 * (1 - q)))
        c.restore()
        self.ui["cam"] = cam

    def ui_divert(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (20, -20, 0.92))
        if tw < s("fix4") - 0.12:
            self.chip(540, 420, "stops", T["river"] - 0.2, s("fix4") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["stops"] + 0.05, s("fix4") - 0.2, x=880, y=520)
            self.red(T["stops"] + 0.05, 1.2)
            return
        bx, by = self.at(cam, 480, -180)
        self.label(bx, by, 700, 560, "blast", T["blast"] - 0.1, min(T["send"], T["around"]) - 0.1, "#FDBA74", size=38)
        self.chip(540, 420, "around", min(T["send"], T["around"]) - 0.1, T["close"] - 0.15, accent="#60A5FA", size=40)
        self.chip(540, 420, "gap", T["close"] - 0.15, s("cta") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["gap"] + 0.1, s("cta") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: temple (the reveal)
    def draw_temple(self, c, t):
        T, s = self.T, self.tl.s
        lk = e_io(prog(t, T["lifted"] - 0.1, T["safety"] + 0.35))
        cam = (0, lerp(-197, -497, lk), 1.2)
        cx, cy, z = cam
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=(-900 - cy) * z + H / 2)
        self.view(c, cam)
        cl = skia.Path()                                                    # the sandstone cliff
        cl.moveTo(-1600, 400)
        cl.lineTo(-1600, -1000)
        for k in range(17):
            cl.lineTo(-1600 + k * 200, -1000 - 40 * math.sin(k * 1.3) - (60 if k % 3 == 0 else 0))
        cl.lineTo(1600, 400)
        cl.close()
        c.drawPath(cl, lin_paint(0, -1100, 0, 400, ["#C27A50", "#9A5A3A", "#6E3E28"]))
        for k in range(14):
            c.drawLine(-1600, -900 + k * 90, 1600, -880 + k * 90 + 20 * math.sin(k), P("#5A321F", 0.25, stroke=5))
        rise = 300 * lk
        cut = prog(t, T["cut"] - 0.15, T["cut"] + 0.6)
        if lk > 0:                                                          # the empty niche left behind
            c.drawRect(R(-520, -560, 1040, 560), P("#7A4630", 0.6 * lk))
        facade(c, 0, -rise, t, cut=cut)
        wl = lerp(200, -10, e_io(prog(t, T["statues"] - 0.15, T["lifted"]))) - 250 * e_io(prog(t, T["lifted"], T["safety"] + 0.5))
        wp = skia.Path()
        wp.moveTo(-1600, wl)
        for k in range(33):
            wp.lineTo(-1600 + k * 100, wl + 6 * math.sin(t * 2 + k))
        wp.lineTo(1600, 900)
        wp.lineTo(-1600, 900)
        wp.close()
        c.drawPath(wp, lin_paint(0, wl, 0, 700, [shade(LAKE_C, 0.2), LAKE_D], a=0.92))
        for k in range(12):
            q = (t * 0.2 + k / 12.0) % 1.0
            c.drawLine(-900 + q * 1800, wl + 20 + (k % 3) * 30, -860 + q * 1800, wl + 20 + (k % 3) * 30,
                       P("#E0F2FE", 0.5, stroke=3))
        if 0 < lk < 1:                                                      # cranes lifting the blocks
            for sd in (-1, 1):
                c.drawLine(sd * 620, -rise - 700, sd * 620, 100, P("#F59E0B", stroke=10))
                c.drawLine(sd * 620, -rise - 700, sd * 300, -rise - 660, P("#F59E0B", stroke=8))
                c.drawLine(sd * 300, -rise - 660, sd * 300, -rise - 586, P("#E5E7EB", stroke=3))
        c.restore()
        self.ui["cam"] = cam

    def ui_temple(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "abu", T["statues"] - 0.1, T["cut"] - 0.1, accent=HILITE, size=44)
        self.chip(540, 420, "cut", T["cut"] - 0.1, T["lifted"] - 0.05, accent="#FDBA74", size=40)
        self.chip(540, 420, "lift", T["lifted"] - 0.05, s("stat") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["safety"] + 0.1, s("stat") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: shower (the tag)
    def draw_shower(self, c, t):
        T = self.T
        foam = 0.6 + 0.4 * prog(t, T["hair"] - 0.3, T["shampoo"])
        water = 1 - prog(t, T["cuts"] - 0.05, T["cuts"] + 0.15)
        shower_guy(c, t, foam=foam, water=water, squint=prog(t, T["cuts"] + 0.2, T["cuts"] + 0.3), rtl=self.rtl)

    def ui_shower(self, c, t, tw):
        T = self.T
        k = self.span(T["cuts"] + 0.1, self.duration + 1)
        if k > 0:
            bx, by = 760, 560
            sz = 46
            lab = self.L["nowater"]
            wdt = (arabic.width_ar(lab, sz * 1.15, "Tajawal-Black") if arabic.is_ar(lab) else text_width(lab, sz, "Poppins-Black")) + 70
            kk = e_back(clamp(k))
            c.save()
            c.translate(bx, by)
            c.scale(kk, kk)
            c.drawRRect(rr(-wdt / 2, -60, wdt, 110, 50), P("#F8FAFC"))
            tp = skia.Path()
            tp.moveTo(-30, 46)
            tp.lineTo(0, 46)
            tp.lineTo(-60, 96)
            tp.close()
            c.drawPath(tp, P("#F8FAFC"))
            word(c, lab, 0, 14, sz, "#111827")
            c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=GOLD, horizon_y=H * 0.6)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.8, True, 61), -14)]
        for i, tl_ in enumerate(self.land):
            ev.append((tl_, sfx.thud(0.25, 62 + i), -9 if i % 2 else -11))
        ev += [(T["congrats"] - 0.2, rumble(1.4, 80), -10), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 81), -9),
               (T["congrats"] + 0.3, sfx.hiss(1.6, 82), -16), (T["aswan"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 83), -4), (T["floods"], sfx.hiss(1.4, 84), -10),
               (T["drown0"] + 0.1, sfx.alarm(3, 820.0), -12), (T["next"], sfx.whoosh(0.5, False, 85), -12),
               (T["barely"], sfx.sizzle(0.5, 86), -12), (T["barely"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 87), -4), (T["block"], rumble(1.0, 88), -10),
               (T["block"] + 0.3, sfx.thud(0.4, 89), -8), (T["trap"], sfx.hiss(1.4, 90), -14),
               (T["slowly"], sfx.whirr(1.2, 160.0, 220.0, 91), -16), (T["year"] + 0.1, sfx.ding(), -8),
               (T["year"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 92), -4), (T["pushes"], sfx.creak(0.9), -10),
               (T["fall"], sfx.creak(0.6), -8), (T["fall"] + 0.5, sfx.thud(0.5, 93), -6),
               (T["fall"] + 0.5, sfx.hiss(1.2, 94), -10), (T["fall"] + 0.6, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 95), -4)]
        for k in range(7):
            ev.append((T["hill"] - 0.2 + k * 0.18, sfx.thud(0.2, 96 + k), -13))
        ev += [(min(T["kilometer"], T["bottom"]), sfx.tick(), -8), (T["bottom"] + 0.1, sfx.ding(), -8),
               (T["bottom"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 103), -4), (T["seeps"], sfx.hiss(1.6, 104), -14),
               (T["coffee"], sfx.tap(105), -8), (T["coffee"] + 0.4, sfx.tap(106), -10),
               (T["filter"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 107), -4), (min(T["clay"], T["core"]), sfx.thud(0.4, 108), -8),
               (min(T["pump"], T["cement"]), sfx.whirr(1.6, 120.0, 180.0, 109), -12), (T["under"] + 0.1, sfx.ding(), -8),
               (T["under"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 110), -4), (s("break4") + 0.1, sfx.hiss(2.2, 111), -12)]
        for k in range(5):
            ev.append((s("break4") + 0.2 + k * 0.4, sfx.tap(112 + k), -12))
        ev += [(T["stops"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 118), -4)]
        for i in range(6):
            ev.append((T["blast"] + i * 0.16, boom(0.9, 119 + i), -10 - i))
        ev += [(min(T["send"], T["around"]), sfx.hiss(1.4, 126), -12), (T["close"], rumble(0.9, 127), -10),
               (T["gap"] + 0.1, sfx.ding(), -8), (T["gap"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(128), 0), (T["follow"] - 0.15, sfx.pop(129), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 130), -6), (T["lake2"], sfx.hiss(1.6, 131), -14),
               (T["five"], sfx.pop(132), -8), (T["statues"] - 0.15, sfx.whoosh(0.4, True, 133), -6),
               (T["cut"], sfx.whirr(0.8, 600.0, 900.0, 134), -16), (T["lifted"], sfx.creak(1.0), -12),
               (T["safety"] + 0.1, sfx.ding(), -8), (T["safety"] + 0.3, sfx.chime(), -6)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 135), -6), (T["s1"], sfx.pop(136), -3), (T["s2"], sfx.pop(137), -3),
               (T["s3"], sfx.pop(138), -3), (T["s3"] + 0.1, sfx.hum(1.6), -16)]
        ev += [(T["cong2"], sfx.pop(139), -2), (T["cong2"], sfx.sparkle(1.0, 14, 140), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 141), -6), (s("tag"), sfx.hiss(max(0.5, T["cuts"] - s("tag")), 142), -14),
               (T["cuts"], sfx.power_down(0.6, 143), -10), (T["cuts"] + 0.5, sfx.tap(144), -6),
               (T["cuts"] + 1.2, sfx.tap(145), -8), (T["shampoo"] + 0.2, sfx.pop(146), -6)]
        return ev


NAME = "aswan"
EPISODE = Aswan
