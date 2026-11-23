"""Episode 71 - a vacuum cleaner.  v2 look: a cordless stick vacuum in x-ray on a living-room rug (world: floor y = 0,
1 unit = 1 px at zoom 1): the floor head with its brush roll, dust rushing up the wand, a little tornado in the clear
bin, the motor's fan spinning over a hundred thousand times a minute, the filter at the back.

Sets: room (hook: close on the clear bin and the motor, crumbs rushing up the wand, out to the whole vacuum gliding
over the rug leaving a clean stripe; break1: a broom throws a cloud of dust that settles back; stat; closer), can
(fix1: a cut-open sealed can, the fan throws the air out, the gauge drops, the room's air rushes in with the crumbs),
carpet (break2: dirt deep between the fibres, a breeze passes over; fix2: the brush roll beats it up into the flow),
bin (break3: a dust bag clogs and the suction dies; fix3: a cyclone, dust flung to the wall and down into the bin),
filter (break4: the finest dust puffs out of the back, a sneeze; fix4: a pleated filter, a hair under a magnifier),
street (reveal: 1901, Hubert Booth sucks a dusty chair through a handkerchief, then his horse-drawn machine with hoses
through the windows), tag (a robot vacuum stuck under the same couch every day).
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of  # noqa: E402
from windtower import arrow  # noqa: E402

PURPLE = ("#A78BFA", "#7C3AED", "#4C1D95")
GOLD = ("#FDE68A", "#F59E0B", "#B45309")
METAL = ("#E5E7EB", "#9CA3AF", "#4B5563")
DUST = ("#8B7355", "#A08A6A", "#6B5A44", "#B8A07E")
RUG = ("#B4533A", "#8E3B28", "#D9785A")
ANG = 28.0                                       # the stick leans back this many degrees
L_TOP = -860.0                                   # the top of the vacuum, local units along the stick


def local(x, y, ang=ANG):
    """A point of the vacuum (local, origin at the floor head) turned into the room (relative)."""
    q = math.radians(ang)
    return x * math.cos(q) - y * math.sin(q), x * math.sin(q) + y * math.cos(q)


def fan_disc(c, x, y, r, t, rpm=1.0, a=1.0):
    """A fan seen face-on, blades blurred by speed."""
    c.drawCircle(x, y, r, P("#1F2937", a))
    rot = t * 360 * 6 * rpm
    for k in range(9):
        q = math.radians(rot + k * 40)
        p = skia.Path()
        p.moveTo(x, y)
        p.lineTo(x + math.cos(q) * r * 0.95, y + math.sin(q) * r * 0.95)
        p.lineTo(x + math.cos(q + 0.35) * r * 0.9, y + math.sin(q + 0.35) * r * 0.9)
        p.close()
        c.drawPath(p, P("#CBD5E1", a * (0.5 if rpm > 0.5 else 0.9)))
    if rpm > 0.5:
        c.drawCircle(x, y, r * 0.8, P("#E5E7EB", 0.25 * a, stroke=r * 0.5))
    c.drawCircle(x, y, r * 0.2, P(GOLD[1], a))


def stick_vac(c, x, y, t, s=1.0, xray=0.0, dust=1.0, swirl=1.0, rpm=1.0, fill=0.25, a=1.0, glow=0.0):
    """The stick vacuum standing on (x, y), leaning back ANG degrees. xray 0..1 shows the brush roll, the dust in the
    wand, the motor's fan and the air leaving through the filter; swirl = the tornado in the clear bin."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    contact_shadow(c, 0, 0, 260, 0.45, 16)
    c.rotate(ANG)
    # wand
    c.drawRect(R(-17, -520, 34, 470), lin_paint(-17, 0, 17, 0, [METAL[2], METAL[0], METAL[1]]))
    if xray > 0:
        c.drawRect(R(-12, -515, 24, 460), P("#0B1220", 0.6 * xray))
        rng = random.Random(3)
        for k in range(26):                                                # crumbs rushing up the wand
            u = (t * 1.6 + k / 26) % 1.0
            px = rng.uniform(-8, 8)
            c.drawCircle(px, lerp(-60, -515, u), rng.uniform(2.5, 5), P(rng.choice(DUST), xray * dust))
    # floor head
    c.drawRRect(rr(-118, -58, 236, 58, 24), lin_paint(0, -58, 0, 0, [PURPLE[1], PURPLE[2]]))
    c.drawRRect(rr(-118, -58, 236, 14, 7), P(PURPLE[0], 0.8))
    c.drawRect(R(-26, -76, 52, 26), P(METAL[1]))
    if xray > 0:                                                           # the brush roll inside
        c.drawRRect(rr(-100, -46, 200, 40, 20), P("#0B1220", 0.7 * xray))
        for k in range(14):
            bx = -92 + ((k * 14 + t * 220) % 184)
            c.drawLine(bx, -42, bx - 10, -8, P("#F87171", xray, stroke=4))
    c.drawCircle(-96, -8, 9, P("#111827"))
    c.drawCircle(96, -8, 9, P("#111827"))
    # clear bin with the tornado
    c.drawRRect(rr(-62, -740, 124, 226, 30), P("#DBEAFE", 0.22))
    lvl = clamp(fill)
    c.drawRRect(rr(-58, -520 - 200 * lvl, 116, 200 * lvl, 24), P(DUST[2], 0.85))
    if swirl > 0:
        for k in range(7):
            yy = -540 - k * 26
            w_ = 50 - k * 2
            ph = t * 14 + k * 0.9
            sx = math.sin(ph) * w_
            c.drawLine(-w_, yy, w_, yy - 8, P("#E0F2FE", 0.25 * swirl, stroke=2))
            c.drawCircle(sx, yy - 4 + math.cos(ph) * 3, 3.5, P(DUST[(k + int(t * 10)) % 4], 0.9 * swirl))
        cone = path_of([(-22, -700), (22, -700), (8, -600), (-8, -600)], close=True)
        c.drawPath(cone, P("#E5E7EB", 0.55))
    c.drawRRect(rr(-62, -740, 124, 226, 30), P("#E0F2FE", 0.9, stroke=4))
    # motor housing and the filter cap
    c.drawRRect(rr(-50, -840, 100, 108, 20), lin_paint(-50, 0, 50, 0, [PURPLE[2], PURPLE[1], PURPLE[2]]))
    c.drawRRect(rr(-42, -872, 84, 36, 12), lin_paint(-42, 0, 42, 0, [GOLD[2], GOLD[1], GOLD[2]]))
    for k in range(5):
        c.drawLine(-30 + k * 15, -868, -30 + k * 15, -842, P(GOLD[0], 0.7, stroke=3))
    if xray > 0:
        c.drawRRect(rr(-44, -834, 88, 96, 16), P("#0B1220", 0.75 * xray))
        fan_disc(c, 0, -786, 40, t, rpm=rpm, a=xray)
        add_glow(c, 0, -786, 70, "#C4B5FD", 0.4 * xray * rpm)
        for k in range(3):                                                 # air out of the back
            u = (t * 1.3 + k / 3) % 1.0
            c.drawLine(-20 + k * 20, -880 - u * 60, -20 + k * 20, -900 - u * 60, P("#BAE6FD", 0.8 * xray * (1 - u), stroke=5))
    # handle and the battery
    c.drawPath(path_of([(58, -640), (124, -700), (122, -790), (64, -790)]), P(PURPLE[1], 1.0, stroke=24))
    c.drawRRect(rr(58, -690, 46, 120, 12), P("#374151"))
    c.drawRect(R(110, -730, 14, 22), P(GOLD[1]))
    if glow > 0:
        add_glow(c, 0, -620, 200, "#C4B5FD", 0.25 * glow)
    if a < 1:
        c.restore()
    c.restore()


def rug(c, x0, x1, t, clean_x=1e9, a=1.0):
    """A rug on the floor (world, floor y = 0): crumbs on it beyond clean_x."""
    c.drawRect(R(x0, -12, x1 - x0, 12), lin_paint(0, -12, 0, 0, [RUG[2], RUG[0]], a=a))
    for k in range(int((x1 - x0) / 18)):
        xx = x0 + 9 + k * 18
        c.drawLine(xx, -12, xx, -2, P(RUG[1], 0.5 * a, stroke=3))
    for side in (x0, x1):
        for k in range(5):
            c.drawLine(side, -10 + k * 2, side + (-14 if side == x0 else 14), -6 + k * 2, P("#F5E6C8", 0.8 * a, stroke=2))
    rng = random.Random(9)
    for k in range(70):
        cx = rng.uniform(x0 + 10, x1 - 10)
        if cx > clean_x:
            c.drawCircle(cx, -14 - rng.uniform(0, 4), rng.uniform(2.5, 5.5), P(rng.choice(DUST), a))


def room_bg(c, t, a=1.0, night=0.0):
    """Wall, window, plant and the wooden floor (world)."""
    c.drawRect(R(-1400, -1800, 2800, 1800), lin_paint(0, -1800, 0, 0, [mix("#3A4A6B", "#141C30", night), mix("#56688C", "#1E2840", night)], a=a))
    c.drawRect(R(-620, -1060, 380, 500), P(mix("#BFE3F5", "#22305A", night), a))           # window
    c.drawRect(R(-620, -1060, 380, 500), P("#E5E7EB", a, stroke=14))
    c.drawLine(-430, -1060, -430, -560, P("#E5E7EB", a, stroke=10))
    c.drawLine(-620, -810, -240, -810, P("#E5E7EB", a, stroke=10))
    if night < 0.5:
        light_cone(c, -430, -810, 60, 900, 18, a=0.18 * a)
    c.drawRect(R(-1400, -40, 2800, 40), P("#E7E5E4", a))                                    # baseboard
    c.drawRect(R(-1400, 0, 2800, 1400), lin_paint(0, 0, 0, 900, ["#B07A4A", "#7A4E2C"], a=a))
    for k in range(-20, 20):
        c.drawLine(k * 140, 0, k * 140 - 80, 900, P("#6B4226", 0.4 * a, stroke=3))
    # a plant
    c.drawRRect(rr(560, -150, 120, 150, 18), P("#E07A5F", a))
    for k in range(7):
        q = math.radians(-150 + k * 20)
        c.drawLine(620, -150, 620 + math.cos(q) * 170, -150 + math.sin(q) * 230, P("#3F7D3A", a, stroke=16))


def broom(c, x, y, ang, a=1.0):
    """A broom with its bristles on (x, y)."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawLine(0, -40, 0, -560, P("#B45309", a, stroke=14))
    c.drawPath(path_of([(-70, 0), (70, 0), (40, -60), (-40, -60)], close=True), P("#F4C542", a))
    for k in range(13):
        c.drawLine(-64 + k * 10.6, 0, -54 + k * 9, -50, P("#C99A1E", a, stroke=3))
    c.drawRect(R(-44, -66, 88, 14), P("#DC2626", a))
    c.restore()


def dust_cloud(c, x, y, t, t0, rise=1.0, settle=0.0, n=60, a=1.0, seed=4):
    """Fine dust thrown up (rise) and falling back down (settle) around (x, y) (world)."""
    if a <= 0 or rise <= 0:
        return
    rng = random.Random(seed)
    for k in range(n):
        dx = rng.uniform(-260, 260)
        hy = rng.uniform(60, 420)
        drift = math.sin(t * 1.4 + k) * 20
        yy = y - hy * rise * (1 - settle) - 4
        c.drawCircle(x + dx * rise + drift, yy, rng.uniform(3, 7), P(rng.choice(("#C8B8A0", "#A89880", "#DCCFB8")), 0.75 * a))


def molecule(c, x, y, r, col, a=1.0):
    c.drawCircle(x, y, r, P(col, a))
    c.drawCircle(x - r * 0.3, y - r * 0.3, r * 0.35, P("#FFFFFF", 0.5 * a))


def gauge(c, x, y, r, v, a=1.0, label=""):
    """A round pressure gauge, v 0..1 (screen)."""
    c.drawCircle(x, y, r, P("#F8FAFC", a))
    c.drawCircle(x, y, r, P("#334155", a, stroke=8))
    for k in range(11):
        q = math.radians(150 + k * 24)
        c.drawLine(x + math.cos(q) * r * 0.72, y + math.sin(q) * r * 0.72, x + math.cos(q) * r * 0.88, y + math.sin(q) * r * 0.88,
                   P("#334155", a, stroke=4))
    c.drawArc(R(x - r * 0.8, y - r * 0.8, r * 1.6, r * 1.6), 150, 60, False, P(WARN, 0.8 * a, stroke=8))
    q = math.radians(150 + 240 * clamp(v))
    c.drawLine(x, y, x + math.cos(q) * r * 0.75, y + math.sin(q) * r * 0.75, P("#DC2626", a, stroke=7))
    c.drawCircle(x, y, 9, P("#111827", a))


def fibres(c, x0, x1, y_top, y_bot, t, bend=0.0, a=1.0):
    """Carpet fibres in close-up (screen): wavy tufts standing on a backing."""
    c.drawRect(R(x0, y_bot, x1 - x0, 60), P("#5A2A1C", a))
    rng = random.Random(12)
    x = x0
    while x < x1:
        h = rng.uniform(0.8, 1.0) * (y_bot - y_top)
        sway = math.sin(t * 2 + x * 0.05) * 6 + bend * math.sin(t * 18 + x * 0.3) * 26
        p = skia.Path()
        p.moveTo(x, y_bot)
        p.cubicTo(x + 10, y_bot - h * 0.4, x - 10 + sway * 0.5, y_bot - h * 0.7, x + sway, y_bot - h)
        c.drawPath(p, P(rng.choice(RUG), a, stroke=rng.uniform(12, 18)))
        x += rng.uniform(16, 26)


def brush_roll(c, x, y, r, w, t, a=1.0):
    """The brush roll seen from the side (screen): a drum with tufts of bristles, spinning."""
    c.drawRRect(rr(x - w / 2, y - r, w, 2 * r, r), lin_paint(0, y - r, 0, y + r, ["#64748B", "#CBD5E1", "#475569"], a=a))
    for k in range(12):
        ph = (t * 3.5 + k / 12) % 1.0
        bx = x - w / 2 + ph * w
        c.drawLine(bx, y - r, bx - 26, y - r - 34, P("#F87171", a, stroke=7))
        c.drawLine(bx, y + r, bx + 26, y + r + 34, P("#F87171", 0.8 * a, stroke=7))


def hair_mag(c, x, y, r, t, a=1.0):
    """A magnifier: one hair across it and specks of dust hundreds of times thinner (screen)."""
    if a <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(x, y, r)
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    c.drawCircle(x, y, r, P("#F1F5F9", a))
    c.drawPath(path_of([(x - r, y + 60), (x + r, y - 40), (x + r, y + 40), (x - r, y + 140)], close=True), P("#6B4423", a))
    rng = random.Random(2)
    for k in range(40):
        c.drawCircle(x + rng.uniform(-r, r), y + rng.uniform(-r, r), 1.6, P("#334155", a))
    c.restore()
    c.drawCircle(x, y, r, P("#0F172A", a, stroke=12))
    c.drawLine(x + r * 0.7, y + r * 0.7, x + r * 1.15, y + r * 1.15, P("#0F172A", a, stroke=22))


def horse(c, x, y, s, t, a=1.0):
    """A cart horse standing / stepping (screen), feet on y, facing left."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    col = "#7C4A2D"
    for k, lx in enumerate((-60, -30, 40, 70)):
        step = math.sin(t * 6 + k * 1.6) * 6
        c.drawLine(lx, -90, lx + step, 0, P(col, a, stroke=14))
    c.drawRRect(rr(-80, -170, 170, 90, 40), P(col, a))
    c.drawPath(path_of([(-70, -150), (-120, -230), (-150, -222), (-118, -150)], close=True), P(col, a))
    c.drawRRect(rr(-178, -246, 70, 36, 16), P(col, a))
    c.drawLine(-120, -236, -60, -160, P("#3B2416", a, stroke=10))
    c.drawPath(path_of([(88, -160), (120, -120), (110, -110)]), P("#3B2416", a, stroke=8))
    c.drawCircle(-160, -232, 4, P("#111827", a))
    c.restore()


def booth_wagon(c, x, y, t, a=1.0):
    """Booth's 'Puffing Billy': a red horse-drawn wagon with a pump engine (screen), wheels on y."""
    c.drawRRect(rr(x - 170, y - 240, 340, 170, 14), lin_paint(0, y - 240, 0, y - 70, ["#DC2626", "#991B1B"], a=a))
    c.drawRect(R(x - 150, y - 220, 120, 80), P("#FDE68A", 0.9 * a))
    c.drawCircle(x + 70, y - 160, 46, P("#475569", a))
    c.drawCircle(x + 70, y - 160, 22, P("#94A3B8", a))
    c.drawRect(R(x + 110, y - 330, 26, 100), P("#334155", a))
    for k in range(4):
        u = (t * 0.8 + k / 4) % 1.0
        c.drawCircle(x + 123 + u * 30, y - 340 - u * 160, 16 + u * 30, P("#CBD5E1", 0.5 * (1 - u) * a))
    for wx in (x - 110, x + 110):
        c.drawCircle(wx, y - 40, 40, P("#1F2937", a))
        c.drawCircle(wx, y - 40, 40, P("#B45309", a, stroke=8))
        for k in range(6):
            q = math.radians(k * 30 + t * 120)
            c.drawLine(wx - math.cos(q) * 36, y - 40 - math.sin(q) * 36, wx + math.cos(q) * 36, y - 40 + math.sin(q) * 36,
                       P("#B45309", a, stroke=4))


def robot_vac(c, x, y, s, t, stuck=0.0, a=1.0):
    """A robot vacuum disc seen from the side (screen), resting on y; stuck blinks a red light."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-110, -44, 220, 44, 20), lin_paint(0, -44, 0, 0, ["#374151", "#111827"], a=a))
    c.drawRRect(rr(-110, -44, 220, 10, 5), P("#6B7280", a))
    c.drawCircle(40, -50, 14, P("#1F2937", a))
    blink = 1.0 if stuck > 0 and math.sin(t * 12) > 0 else 0.0
    c.drawCircle(-50, -26, 7, P("#EF4444" if blink else "#22C55E", a))
    if blink:
        add_glow(c, -50, -26, 30, "#EF4444", 0.6 * a)
    c.restore()


def couch(c, x, y, a=1.0):
    """A couch in side view (screen), legs on y, a low gap under it."""
    c.drawRRect(rr(x - 300, y - 300, 600, 220, 40), lin_paint(0, y - 300, 0, y - 80, ["#2563EB", "#1E3A8A"], a=a))
    c.drawRRect(rr(x - 330, y - 360, 90, 280, 30), P("#1D4ED8", a))
    c.drawRRect(rr(x + 240, y - 360, 90, 280, 30), P("#1D4ED8", a))
    c.drawRRect(rr(x - 250, y - 380, 500, 100, 30), P("#3B82F6", a))
    for lx in (x - 280, x + 280):
        c.drawRect(R(lx - 8, y - 80, 16, 80), P("#78350F", a))


# ====================================================================================== the episode
class Vacuum(EpisodeV2):
    BUILD_NO = 71
    FIRST_SET = "room"
    CLEAR = "#0B1220"
    TITLE = {"en": "VACUUM CLEANER", "ar_sa": "مكنسة كهربا"}
    EMPH = {"en": ["CONGRATS", "SPIN", "FAN", "HUNDRED", "THOUSAND", "MINUTE", "AIR", "SHOVES", "DIRT", "TUBE", "VACUUM",
                   "CLEANER", "YOURSELF", "BROOM", "DUST", "LANDS", "SEALED", "PRESSURE", "DROPS", "RUSHES", "CARPET",
                   "IGNORES", "BREEZE", "SPINNING", "BRUSH", "BEATS", "BAG", "CLOGS", "SUCTION", "DIES", "TORNADO",
                   "BIN", "FINEST", "BACK", "FILTER", "HAIR", "FOLLOW", "TOWERS", "BRIDGE", "BOOTH", "HANDKERCHIEF",
                   "HORSE", "HOSES", "WINDOWS", "NINETY", "PERCENT", "ZERO", "BAGS", "MOTOR", "RACE", "ROBOT", "STUCK",
                   "COUCH"],
            "ar_sa": ["مبروك", "مروحة", "مية", "ألف", "لفة", "الهوا", "يدف", "الوساخة", "أنبوب", "مكنسة", "كهربا", "بيدك",
                      "المقشة", "الغبار", "ينزل", "مقفلة", "الضغط", "يطيح", "يندفع", "الزولية", "يهمها", "فرشاة", "تضرب",
                      "الكيس", "ينسد", "يموت", "الإعصار", "الجدار", "العلبة", "أنعم", "يفلت", "فلتر", "الشعرة", "بميتين",
                      "تابعني", "برجين", "جسر", "هيوبرت", "منديل", "حصان", "الشبابيك", "صفر", "أكياس", "موتور", "سباق",
                      "الروبوت", "تعلق", "الكنبة"]}
    KEYS = {"ar_sa": {
        ("hook", "SPIN"): "تلف", ("hook", "FAN"): "مروحة", ("hook", "HUNDRED"): "مية", ("hook", "MINUTE"): "بالدقيقة",
        ("hook", "AIR"): "الهوا", ("hook", "SHOVES"): "يدف", ("hook", "DIRT"): "الوساخة", ("hook", "TUBE"): "أنبوب",
        ("hook", "CONGRATS"): "مبروك", ("hook", "VACUUM"): "مكنسة",
        ("break1", "BROOM"): "المقشة", ("break1", "DUST"): "الغبار", ("break1", "AIR"): "تطير", ("break1", "LANDS"): "ينزل",
        ("fix1", "FAN"): "مروحة", ("fix1", "PUSHES"): "تطلع", ("fix1", "SEALED"): "مقفل", ("fix1", "PRESSURE"): "الضغط",
        ("fix1", "DROPS"): "يطيح", ("fix1", "ROOM"): "الغرفة", ("fix1", "RUSHES"): "يندفع", ("fix1", "DIRT"): "الوساخة",
        ("break2", "DIRT"): "الوساخة", ("break2", "CARPET"): "الزولية", ("break2", "IGNORES"): "يهمها",
        ("fix2", "SPINNING"): "تلف", ("fix2", "BRUSH"): "فرشا", ("fix2", "BEATS"): "تضرب", ("fix2", "FLOW"): "للهوا",
        ("break3", "BAG"): "الكيس", ("break3", "FILLS"): "تعبي", ("break3", "CLOGS"): "ينسد", ("break3", "DIES"): "يموت",
        ("fix3", "SPIN"): "تلف", ("fix3", "TORNADO"): "اعصار", ("fix3", "FLIES"): "ينرمي", ("fix3", "FALLS"): "يطيح",
        ("fix3", "BIN"): "علب",
        ("break4", "FINEST"): "أنعم", ("break4", "SLIPS"): "يفلت", ("break4", "BLOWS"): "يطلع", ("break4", "BACK"): "ورا",
        ("fix4", "FILTER"): "فلتر", ("fix4", "CATCHES"): "يمسك", ("fix4", "HUNDREDS"): "ميتين", ("fix4", "HAIR"): "الشعر",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "NINETEEN"): "تسعمي", ("reveal", "HUBERT"): "هيوبرت", ("reveal", "SUCKED"): "شفط",
        ("reveal", "HANDKERCHIEF"): "منديل", ("reveal", "HORSE"): "حصان", ("reveal", "HOSES"): "تشفط",
        ("reveal", "WINDOWS"): "الشبابيك",
        ("stat", "HUNDRED"): "مية", ("stat", "NINETY"): "تسعه", ("stat", "ZERO"): "صفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "MOTOR"): "موتور", ("tag", "RACE"): "سباق", ("tag", "ROBOT"): "الروبوت", ("tag", "STUCK"): "تعلق",
        ("tag", "COUCH"): "الكنب"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: twin towers + a sky bridge"),
                   "stat": [("125,000", "TURNS A MINUTE"), ("99.97%", "DUST CAUGHT"), ("0", "BAGS")],
                   "L": {"rpm": "100,000+ TURNS A MINUTE", "push": "THE AIR SHOVES THE DIRT", "name": "VACUUM CLEANER",
                         "broom": "A BROOM", "lands": "...AND IT LANDS AGAIN", "sealed": "A SEALED CAN",
                         "low": "PRESSURE DROPS", "rush": "THE ROOM'S AIR RUSHES IN", "deep": "DIRT DEEP IN THE CARPET",
                         "breeze": "A BREEZE? NOTHING", "brush": "A SPINNING BRUSH", "beat": "BEATS IT UP",
                         "bag": "THE BAG CLOGS", "suction": "SUCTION", "tornado": "A TORNADO INSIDE", "nobag": "NO BAG TO CLOG",
                         "finest": "THE FINEST DUST GETS OUT", "achoo": "ACHOO!", "filter": "A FILTER",
                         "hair": "100s OF TIMES THINNER THAN A HAIR", "booth": "1901: HUBERT BOOTH",
                         "hanky": "TESTED WITH HIS MOUTH", "wagon": "A HORSE-DRAWN VACUUM", "stuck": "STUCK. AGAIN.",
                         "day": "DAY"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: برجين بينهم جسر"),
                      "stat": [("125,000", "لفة بالدقيقة"), ("99.97%", "من الغبار"), ("0", "أكياس")],
                      "L": {"rpm": "أكثر من 100,000 لفة بالدقيقة", "push": "الهوا يدف الوساخة", "name": "مكنسة كهربا",
                            "broom": "المقشة", "lands": "ويرجع ينزل", "sealed": "علبة مقفلة",
                            "low": "الضغط يطيح", "rush": "هوا الغرفة يندفع داخل", "deep": "وساخة داخل الزولية",
                            "breeze": "الهوا؟ ما يهمها", "brush": "فرشاة تلف", "beat": "تضرب وتطيّر",
                            "bag": "الكيس انسد", "suction": "الشفط", "tornado": "إعصار داخلها", "nobag": "بدون كيس",
                            "finest": "أنعم غبار يفلت", "achoo": "عطسة!", "filter": "فلتر",
                            "hair": "أنعم من الشعرة بميتين مرة", "booth": "1901: هيوبرت بوث",
                            "hanky": "جرّبها بفمه", "wagon": "مكنسة يجرها حصان", "stuck": "علقت... مرة ثانية",
                            "day": "يوم"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "spin": ("hook", "SPIN", 0.08), "fan": ("hook", "FAN", 0.12), "hundred": ("hook", "HUNDRED", 0.25),
            "minute": ("hook", "MINUTE", 0.4), "air": ("hook", "AIR", 0.5), "shoves": ("hook", "SHOVES", 0.55),
            "dirt": ("hook", "DIRT", 0.6), "tube": ("hook", "TUBE", 0.68), "congrats": ("hook", "CONGRATS", 0.78),
            "name": ("hook", "VACUUM", 0.9),
            "broom": ("break1", "BROOM", 0.15), "dust": ("break1", "DUST", 0.4), "air1": ("break1", "AIR", 0.55),
            "lands": ("break1", "LANDS", 0.9),
            "fan1": ("fix1", "FAN", 0.08), "pushes": ("fix1", "PUSHES", 0.15), "sealed": ("fix1", "SEALED", 0.3),
            "pressure": ("fix1", "PRESSURE", 0.45), "drops": ("fix1", "DROPS", 0.55), "room": ("fix1", "ROOM", 0.65),
            "rushes": ("fix1", "RUSHES", 0.75), "dirt1": ("fix1", "DIRT", 0.95),
            "dirt2": ("break2", "DIRT", 0.1), "carpet": ("break2", "CARPET", 0.45), "ignores": ("break2", "IGNORES", 0.7),
            "spinning": ("fix2", "SPINNING", 0.1), "brush": ("fix2", "BRUSH", 0.25), "beats": ("fix2", "BEATS", 0.45),
            "flow": ("fix2", "FLOW", 0.9),
            "bag": ("break3", "BAG", 0.15), "fills": ("break3", "FILLS", 0.45), "clogs": ("break3", "CLOGS", 0.3),
            "dies": ("break3", "DIES", 0.92),
            "spin3": ("fix3", "SPIN", 0.08), "tornado": ("fix3", "TORNADO", 0.3), "flies": ("fix3", "FLIES", 0.55),
            "falls": ("fix3", "FALLS", 0.75), "bin": ("fix3", "BIN", 0.92),
            "finest": ("break4", "FINEST", 0.2), "slips": ("break4", "SLIPS", 0.4), "blows": ("break4", "BLOWS", 0.65),
            "back": ("break4", "BACK", 0.9),
            "filter": ("fix4", "FILTER", 0.12), "catches": ("fix4", "CATCHES", 0.25), "hundreds": ("fix4", "HUNDREDS", 0.5),
            "hair": ("fix4", "HAIR", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "y1901": ("reveal", "NINETEEN", 0.1), "hubert": ("reveal", "HUBERT", 0.18), "sucked": ("reveal", "SUCKED", 0.3),
            "hanky": ("reveal", "HANDKERCHIEF", 0.42), "horse": ("reveal", "HORSE", 0.65), "hoses": ("reveal", "HOSES", 0.8),
            "windows": ("reveal", "WINDOWS", 0.92),
            "s1": ("stat", "HUNDRED", 0.05), "s2": ("stat", "NINETY", 0.45), "s3": ("stat", "ZERO", 0.8),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_motor": ("tag", "MOTOR", 0.05), "t_race": ("tag", "RACE", 0.25), "t_robot": ("tag", "ROBOT", 0.5),
            "t_stuck": ("tag", "STUCK", 0.7), "t_couch": ("tag", "COUCH", 0.85)})
        T["lands1"] = max(T["lands"], T["air1"]) + 0.15
        T["ignores1"] = max(T["ignores"], T["carpet"]) + 0.15
        T["dies1"] = max(T["dies"], T["clogs"], T["fills"]) + 0.1
        T["back1"] = max(T["back"], T["blows"]) + 0.15
        T["dirt1b"] = max(T["dirt1"], T["rushes"]) + 0.2
        T["flow1"] = max(T["flow"], T["beats"]) + 0.2
        T["bin1"] = max(T["bin"], T["falls"]) + 0.2
        T["hair1"] = max(T["hair"], T["hundreds"]) + 0.2
        T["wagon"] = min(T["horse"], T["hoses"]) - 0.35
        # ---- sets
        self.cut(s("fix1") - 0.12, "can", 1)
        self.cut(s("break2") - 0.12, "carpet", -1)
        self.cut(s("break3") - 0.12, "bin", 1)
        self.cut(s("break4") - 0.12, "filter", -1)
        self.cut(s("reveal") - 0.12, "street", 1)
        self.cut(s("stat") - 0.12, "room", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- room camera: close on the clear bin and the motor, out to the whole vacuum on the rug
        cm = Camera(220, -500, 2.4)
        cm.key(0.05, 213, -482, 2.3, 1.0)
        cm.key(max(1.0, T["congrats"] - 0.8), 70, -202, 1.09, max(1.0, T["name"] - T["congrats"] + 0.8))
        cm.key(s("break1") - 0.12, -40, -202, 1.09, 0.0)
        cm.key(s("stat") - 0.12, 90, -338, 0.8, 0.0)
        cm.key(s("closer") - 0.1, 60, -230, 1.05, 1.2)
        self.cam = cm
        self.spans = [(T["lands1"], T["dirt1b"] + 0.3), (T["ignores1"], T["flow1"] + 0.3), (T["dies1"], T["bin1"] + 0.3),
                      (T["back1"], T["hair1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["lands1"], 0.3, 6), (T["rushes"], 0.4, 8), (T["ignores1"], 0.3, 6),
                       (T["beats"], 0.5, 8), (T["dies1"], 0.4, 8), (T["back1"], 0.3, 6), (s("closer") + 0.2, 0.35, 8),
                       (T["t_stuck"], 0.4, 10)]

    # ------------------------------------------------------------------ set: room
    def draw_room(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        night = 0.0
        self.view(c, cam)
        room_bg(c, t, night=night)
        hook = t < s("break1") - 0.12
        broom_on = s("break1") - 0.12 <= t < s("fix1")
        if broom_on:
            rug(c, -520, 520, t, clean_x=1e9)
            sweep = math.sin((t - s("break1")) * 5.5) * 22
            broom(c, -150 + sweep * 2, 0, 18 + sweep * 0.4)
            rise = prog(t, T["dust"] - 0.4, T["dust"] + 0.4)
            settle = prog(t, T["lands"] - 0.6, T["lands"] + 0.4)
            dust_cloud(c, -40, -20, t, T["dust"], rise=rise, settle=settle, n=70)
            c.restore()
            self.ui["cam"] = cam
            return
        if hook:
            vx = lerp(-110, -80, prog(t, 0, s("break1")))
            clean_x = vx + 120
        else:
            vx = -80 + math.sin(t * 1.4) * 40
            clean_x = -1e9
        rug(c, -520, 520, t, clean_x=clean_x)
        closer = t >= s("closer") - 0.1
        stick_vac(c, vx, 0, t, xray=1.0 if not closer else 0.6, dust=1.0 if hook else 0.6, swirl=1.0,
                  rpm=1.0, fill=0.22 if hook else 0.3, glow=1.0 if closer else 0.0)
        c.restore()
        if closer:                                                          # sparkles over the clean rug
            for k in range(6):
                ph = t * 2 + k * 1.3
                sx, sy = self.to_screen(cam, -420 + k * 170, -40)
                add_glow(c, sx, sy - 20 * abs(math.sin(ph)), 26, "#FFFFFF", 0.6 * abs(math.sin(ph)))
        self.ui["cam"] = cam

    def ui_room(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "rpm", 0.15, T["air"] - 0.2, accent=HILITE, size=42)
            self.chip(540, 300, "push", T["air"] - 0.2, T["congrats"] - 0.15, accent="#93C5FD", size=44)
            self.chip(540, 300, "name", T["congrats"] - 0.15, s("break1") + 0.1, accent=HILITE, size=54)
            return
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "broom", T["broom"] - 0.2, T["lands"] - 0.3, accent="#FDE68A", size=50)
            self.chip(540, 300, "lands", T["lands"] - 0.3, s("fix1") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["lands1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["lands1"], 1.2)

    # ------------------------------------------------------------------ set: can (fix1)
    def draw_can(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1E2A44", "#0F172A"])
        x0, x1, y0, y1 = 300, 900, 640, 1080
        mid = (y0 + y1) / 2
        out = prog(t, T["pushes"] - 0.2, T["drops"] + 0.2)                   # how much air has been thrown out
        inflow = prog(t, T["room"] - 0.4, T["rushes"])
        c.drawRRect(rr(x0, y0, x1 - x0, y1 - y0, 60), P("#334155"))
        c.drawRRect(rr(x0 + 14, y0 + 14, x1 - x0 - 28, y1 - y0 - 28, 50), P("#0B1220"))
        c.drawRRect(rr(x0, y0, x1 - x0, y1 - y0, 60), P("#94A3B8", 1.0, stroke=8))
        c.drawRect(R(100, mid - 50, x0 - 100 + 20, 100), P("#475569"))         # the hose mouth on the left
        c.drawRect(R(100, mid - 36, x0 - 100 + 20, 72), P("#0B1220"))
        fan_disc(c, x1 - 90, mid, 120, t, rpm=1.0)
        for k in range(5):                                                  # vents at the back
            c.drawRect(R(x1 - 6, y0 + 60 + k * 70, 16, 40), P("#64748B"))
        rng = random.Random(5)
        n_in = int(lerp(70, 20, out))
        for k in range(70):                                                 # air inside: fewer and fewer
            px = rng.uniform(x0 + 40, x1 - 220)
            py = rng.uniform(y0 + 40, y1 - 40)
            if k < n_in:
                jx = math.sin(t * 7 + k) * 8
                jy = math.cos(t * 6 + k * 1.7) * 8
                molecule(c, px + jx, py + jy, 11, "#7DD3FC")
        for k in range(14):                                                 # air thrown out of the back
            u = (t * 1.2 + k / 14) % 1.0
            molecule(c, x1 + 20 + u * 220, mid + math.sin(k * 2.1) * 160, 11, "#7DD3FC", a=out * (1 - u))
        rng = random.Random(8)
        for k in range(26):                                                 # the room's air pushing in, with crumbs
            u = (t * 0.9 + k / 26) % 1.0
            py = mid + rng.uniform(-30, 30)
            px = lerp(-40, x0 + 260, u)
            if px < 120:
                py = mid + rng.uniform(-260, 260) * (1 - px / 120) * 0.8 + rng.uniform(-30, 30)
            if k % 4 == 0:
                c.drawCircle(px, py, 9, P(DUST[k % 4], inflow))
            else:
                molecule(c, px, py, 10, "#BAE6FD", a=inflow)
        if inflow > 0:
            arrow(c, 40, mid, 260, mid, "#93C5FD", a=inflow, w=14, head=40)
        gauge(c, 600, 500, 90, 0.8 - 0.65 * out)

    def ui_can(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "sealed", T["fan1"] - 0.1, T["pressure"] - 0.2, accent="#CBD5E1", size=48)
        self.chip(540, 300, "low", T["pressure"] - 0.2, T["room"] - 0.2, accent=WARN, size=50)
        self.chip(540, 300, "rush", T["room"] - 0.2, s("break2") - 0.15, accent="#93C5FD", size=42)
        self.badge("check", T["dirt1b"] + 0.1, s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: carpet (break2, fix2)
    def draw_carpet(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1F1A2E", "#2A1F2A"])
        fixed = t >= s("fix2") - 0.12
        beat = prog(t, T["beats"] - 0.3, T["beats"] + 0.3) if fixed else 0.0
        fibres(c, -20, W + 20, 760, 1180, t, bend=beat)
        rng = random.Random(21)
        for k in range(36):                                                 # dirt deep between the fibres
            bx = rng.uniform(40, W - 40)
            by = rng.uniform(1080, 1170)
            up = clamp((t - (T["beats"] + rng.uniform(-0.2, 0.6))) / 1.0) if fixed else 0.0
            yy = by - up * (by - 380) - math.sin(up * math.pi) * 60
            xx = bx + up * (540 - bx) * 0.6 + math.sin(t * 5 + k) * 6 * up
            c.drawCircle(xx, yy, rng.uniform(6, 11), P(rng.choice(DUST), 1.0 - 0.4 * clamp(up * 1.5 - 0.6)))
        if not fixed:                                                       # a breeze glides over the top
            bk = prog(t, T["carpet"] - 0.2, T["carpet"] + 0.3)
            for k in range(6):
                u = (t * 0.8 + k / 6) % 1.0
                yy = 640 + k * 22
                c.drawLine(lerp(-100, W, u), yy, lerp(-100, W, u) + 180, yy, P("#BAE6FD", 0.6 * bk * math.sin(math.pi * u), stroke=6))
        else:
            dk = e_out(prog(t, T["brush"] - 0.5, T["brush"] + 0.2))
            brush_roll(c, 540, lerp(300, 700, dk), 70, 900, t)
            fk = prog(t, T["flow"] - 0.5, T["flow"])
            for k in range(5):                                              # the air stream going up
                u = (t * 1.1 + k / 5) % 1.0
                c.drawLine(200 + k * 170, 560 - u * 200, 200 + k * 170, 500 - u * 200, P("#93C5FD", 0.8 * fk * (1 - u), stroke=8))

    def ui_carpet(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "deep", T["dirt2"] - 0.2, T["ignores"] - 0.3, accent="#FDBA74", size=44)
            self.chip(540, 300, "breeze", T["ignores"] - 0.3, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["ignores1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["ignores1"], 1.2)
            return
        self.chip(540, 300, "brush", T["spinning"] - 0.2, T["beats"] - 0.2, accent="#F87171", size=50)
        self.chip(540, 300, "beat", T["beats"] - 0.2, s("break3") - 0.15, accent=GOOD, size=50)
        self.badge("check", T["flow1"] + 0.1, s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: bin (break3, fix3)
    def draw_bin(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#16213A", "#0B1220"])
        if t < s("fix3") - 0.12:                                            # a bag that clogs
            fill = prog(t, T["bag"] - 0.3, T["dies1"])
            c.drawRRect(rr(220, 560, 640, 560, 60), P("#334155"))
            bag = skia.Path()
            bag.moveTo(300, 640)
            bag.cubicTo(250, 800, 260, 1020, 360, 1060)
            bag.lineTo(720, 1060)
            bag.cubicTo(820, 1020, 830, 800, 780, 640)
            bag.close()
            c.drawPath(bag, P("#C9BFA8"))
            c.save()
            c.clipPath(bag, skia.ClipOp.kIntersect, True)
            c.drawRect(R(200, 1060 - 440 * fill, 700, 440 * fill + 20), P("#8B7B62"))
            rng = random.Random(4)
            for k in range(int(140 * fill)):
                c.drawCircle(rng.uniform(260, 820), rng.uniform(1060 - 440 * fill, 1070), rng.uniform(4, 9), P(rng.choice(DUST)))
            c.restore()
            c.drawPath(bag, P("#B8AE98", 1.0, stroke=6))
            flow = 1 - fill
            for k in range(5):                                              # air in: weaker and weaker
                u = (t * 1.4 + k / 5) % 1.0
                c.drawLine(lerp(40, 280, u), 820 + k * 16, lerp(40, 280, u) + 60, 820 + k * 16, P("#93C5FD", flow * math.sin(math.pi * u), stroke=8))
            gauge(c, 880, 470, 80, 0.85 * flow + 0.05)
            return
        # a cyclone: the air spins, the dust is thrown to the wall and slides into the bin
        cone = path_of([(300, 560), (780, 560), (600, 1000), (480, 1000)], close=True)
        c.drawPath(cone, P("#DBEAFE", 0.16))
        c.drawPath(cone, P("#E0F2FE", 0.9, stroke=6))
        c.drawRRect(rr(380, 1000, 320, 170, 24), P("#DBEAFE", 0.16))
        lvl = prog(t, T["falls"] - 0.4, T["bin1"] + 1.0)
        c.drawRRect(rr(388, 1160 - 120 * lvl, 304, 120 * lvl + 4, 18), P(DUST[2], 0.9))
        c.drawRRect(rr(380, 1000, 320, 170, 24), P("#E0F2FE", 0.9, stroke=6))
        sk = prog(t, T["spin3"] - 0.3, T["tornado"])
        for k in range(46):                                                 # a spiral of air going down
            u = (k / 46 + t * 0.35) % 1.0
            yy = lerp(590, 980, u)
            wd = lerp(230, 50, u)
            q = u * 26 - t * 9
            px = 540 + math.sin(q) * wd
            front = math.cos(q) > 0
            c.drawCircle(px, yy, 6 if front else 4, P("#93C5FD", (0.85 if front else 0.35) * sk))
        rng = random.Random(7)
        for k in range(30):                                                 # dust flung out to the wall, sliding down
            ph = rng.random()
            u = (t * 0.5 + ph) % 1.0
            yy = lerp(600, 990, u)
            wd = lerp(230, 50, u)
            side = 1 if k % 2 else -1
            px = 540 + side * wd * (0.96 + 0.04 * math.sin(t * 9 + k))
            c.drawCircle(px, yy, rng.uniform(4, 8), P(rng.choice(DUST), sk))
        ck = prog(t, T["flies"] - 0.3, T["flies"] + 0.3)
        if ck > 0:                                                          # clean air up the middle
            arrow(c, 540, 900, 540, 480, "#E0F2FE", a=ck, w=16, head=44)

    def ui_bin(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "bag", T["clogs"] - 0.3, s("fix3") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["dies1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["dies1"], 1.2)
            return
        self.chip(540, 300, "tornado", T["spin3"] - 0.1, T["falls"] - 0.2, accent="#93C5FD", size=50)
        self.chip(540, 300, "nobag", T["falls"] - 0.2, s("break4") - 0.15, accent=GOOD, size=50)
        self.badge("check", T["bin1"] + 0.1, s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: filter (break4, fix4, cta)
    def draw_filter(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#26324A", "#141C2E"])
        fixed = t >= s("fix4") - 0.12
        # the back end of the vacuum: motor housing with the outlet on the right
        c.drawRRect(rr(-120, 700, 520, 300, 50), lin_paint(0, 700, 0, 1000, [PURPLE[1], PURPLE[2]]))
        fan_disc(c, 230, 850, 110, t, rpm=1.0)
        c.drawRect(R(400, 760, 70, 180), P(GOLD[2]))
        if fixed:                                                           # the pleated filter in the outlet
            fk = e_back(prog(t, T["filter"] - 0.3, T["filter"] + 0.2))
            pts = []
            for k in range(13):
                pts.append((420 + (30 if k % 2 else 0), lerp(760, 940, k / 12)))
            c.save()
            c.translate(0, (1 - fk) * -500)
            c.drawPath(path_of(pts), P("#F8FAFC", 1.0, stroke=10))
            c.drawPath(path_of(pts), P("#CBD5E1", 1.0, stroke=3))
            c.restore()
        rng = random.Random(15)
        leak = prog(t, T["slips"] - 0.3, T["blows"] + 0.3)
        for k in range(60):                                                 # the finest dust coming out of the back
            u = (t * 0.7 + rng.random()) % 1.0
            px = 470 + u * 520
            py = 850 + rng.uniform(-60, 60) + math.sin(u * 6 + k) * 70 * u
            caught = fixed and prog(t, T["catches"] - 0.3, T["catches"] + 0.2) > 0
            if not caught:
                c.drawCircle(px, py, rng.uniform(2.5, 4.5), P("#D6D3D1", 0.8 * leak * (1 - u * 0.6)))
        if fixed:
            ck = prog(t, T["catches"] - 0.3, T["catches"] + 0.2)
            for k in range(30):                                             # specks stuck on the filter
                c.drawCircle(430 + rng.uniform(-6, 30), rng.uniform(770, 930), 3, P("#78716C", ck))
            for k in range(4):                                              # clean air out
                u = (t * 1.3 + k / 4) % 1.0
                c.drawLine(480 + u * 400, 790 + k * 40, 540 + u * 400, 790 + k * 40, P("#BAE6FD", 0.8 * ck * (1 - u), stroke=6))
        if not fixed:                                                       # a sneeze in the dust
            sk = prog(t, T["back"] - 0.3, T["back"])
            person(c, 880, 1180, 300, "#16A34A", t, pose="shrug" if sk > 0.5 else "stand", face=-1)

    def ui_filter(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "finest", T["finest"] - 0.2, s("fix4") - 0.15, accent=WARN, size=44)
            self.chip(880, 560, "achoo", T["back"] - 0.1, s("fix4") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["back1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["back1"], 1.2)
            return
        self.chip(540, 300, "filter", T["filter"] - 0.2, T["hundreds"] - 0.3, accent="#F8FAFC", size=50)
        self.chip(540, 300, "hair", T["hundreds"] - 0.3, s("cta") - 0.15, accent=HILITE, size=36)
        hk = self.span(T["hundreds"] - 0.3, s("cta") - 0.15)
        if hk > 0:
            hair_mag(c, 780, 560, 150, tw, a=hk)
        self.badge("check", T["hair1"] + 0.1, s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: street (reveal)
    def draw_street(self, c, t):
        T, s = self.T, self.tl.s
        if t < T["wagon"]:                                                  # the chair and the handkerchief
            vrect(c, 0, 0, W, H, ["#3B2416", "#2A180E"])
            c.drawRect(R(0, 1060, W, 400), P("#4A2C18"))
            for k in range(6):                                              # wallpaper stripes
                c.drawRect(R(k * 200, 0, 90, 1060), P("#4A2E1C", 0.6))
            c.drawRRect(rr(300, 760, 420, 90, 30), lin_paint(0, 760, 0, 850, ["#B91C1C", "#7F1D1D"]))     # the plush seat
            c.drawRRect(rr(320, 420, 380, 360, 40), lin_paint(0, 420, 0, 780, ["#B91C1C", "#7F1D1D"]))
            for lx in (330, 690):
                c.drawRect(R(lx - 10, 850, 20, 210), P("#78350F"))
            hk = prog(t, T["hanky"] - 0.4, T["hanky"])
            c.drawPath(path_of([(440, 752), (600, 748), (620, 790), (430, 796)], close=True), P("#F8FAFC", hk))
            dk = prog(t, T["sucked"], T["wagon"])
            c.drawOval(R(480, 760, 90 * dk, 26 * dk), P("#57534E", 0.8 * hk))
            # Booth kneeling, his face on the handkerchief
            c.save()
            c.translate(200, 1060)
            c.rotate(38)
            person(c, 0, 0, 330, "#1F2937", t, pose="stand", face=1, hat="none", hair="#3B2A20", pants="#111827")
            c.restore()
            for k in range(3):                                              # dust pulled up into his mouth
                u = (t * 2 + k / 3) % 1.0
                c.drawCircle(lerp(520, 470, u), lerp(770, 760, u), 4, P("#A8A29E", dk * (1 - u)))
            return
        # the horse-drawn machine in the street, hoses into the windows
        vrect(c, 0, 0, W, H, ["#8FA3B8", "#C9D3DC"])
        c.drawRect(R(560, 260, 520, 900), P("#9A6B4F"))                    # the house
        for k in range(3):
            for j in range(2):
                c.drawRect(R(620 + j * 220, 330 + k * 250, 140, 170), P("#1E293B"))
                c.drawRect(R(620 + j * 220, 330 + k * 250, 140, 170), P("#F1F5F9", 1.0, stroke=10))
        c.drawRect(R(0, 1160, W, 300), P("#57534E"))
        for k in range(14):
            c.drawLine(k * 80, 1160, k * 80 - 40, 1440, P("#44403C", 1.0, stroke=3))
        wk = prog(t, T["wagon"], T["wagon"] + 0.4)
        booth_wagon(c, 300, 1160, t, a=wk)
        horse(c, 70, 1160, 0.9, t, a=wk)
        hk = prog(t, T["hoses"] - 0.4, T["windows"] + 0.4)
        for k, (wx, wy) in enumerate(((690, 600), (910, 850))):              # hoses up into the windows
            p = skia.Path()
            p.moveTo(420, 960)
            p.cubicTo(520, 900 - k * 60, wx - 120, wy + 200, wx, wy)
            pm = skia.PathMeasure(p, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * hk, seg, True)
            c.drawPath(seg, P("#111827", 1.0, stroke=18))
            c.drawPath(seg, P("#374151", 1.0, stroke=8))

    def ui_street(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "booth", T["y1901"] - 0.2, T["hanky"] - 0.2, accent=HILITE, size=48)
        self.chip(540, 300, "hanky", T["hanky"] - 0.2, T["wagon"] + 0.1, accent="#FDE68A", size=46)
        self.chip(540, 300, "wagon", T["wagon"] + 0.1, s("stat") - 0.15, accent="#FCA5A5", size=46)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#3A4A6B", "#56688C"])
        c.drawRect(R(0, 1100, W, H - 1100), lin_paint(0, 1100, 0, H, ["#B07A4A", "#6A4226"]))
        couch(c, 600, 1100)
        t0 = T["t_robot"] - 0.8
        u = t - t0
        if u < 1.0:
            rx = lerp(-150, 520, e_out(clamp(u)))
            stuck = 0.0
        else:
            rx = 520 + math.sin((u - 1.0) * 9) * 14
            stuck = 1.0
        robot_vac(c, rx, 1100, 1.3, t, stuck=stuck)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "stuck", T["t_stuck"] - 0.1, self.duration + 1, accent=WARN, size=54)
        dk = self.span(T["t_robot"] - 0.2, self.duration + 1)
        if dk > 0:
            day = 1 + int(max(0.0, tw - T["t_robot"]) / 0.7)
            v2.chip(c, 540, 420, "%s %d" % (self.L["day"], day), dk, accent=HILITE, size=46)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1220", "#1E293B"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whirr(max(1.5, T["congrats"]), 150.0, 420.0, 61), -14), (T["fan"], sfx.riser(0.8, 62), -14),
              (T["dirt"], sfx.hiss(0.6, 63), -14),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(T["broom"], sfx.hiss(0.5, 66), -14), (T["dust"], sfx.whoosh(0.5, True, 67), -12),
               (T["lands1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["pushes"], sfx.whirr(1.2, 200.0, 380.0, 69), -14),
               (T["rushes"], sfx.hiss(0.8, 70), -12), (T["dirt1b"], sfx.ding(), -8), (T["dirt1b"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["carpet"], sfx.hiss(0.7, 72), -16),
               (T["ignores1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["brush"] - 0.3, sfx.whirr(1.2, 120.0, 180.0, 73), -12), (T["beats"], sfx.thunk(74), -8),
               (T["flow1"], sfx.ding(), -8), (T["flow1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 75), -4), (T["dies1"] - 0.3, sfx.power_down(0.9, 76), -10),
               (T["dies1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["spin3"], sfx.whoosh(0.9, True, 77), -10), (T["falls"], sfx.tap(78), -10),
               (T["bin1"], sfx.ding(), -8), (T["bin1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["back"], sfx.pop(80), -6),
               (T["back1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["filter"], sfx.snap(81), -8), (T["hundreds"], sfx.click(82), -8),
               (T["hair1"], sfx.ding(), -8), (T["hair1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(83), 0), (T["follow"] - 0.15, sfx.pop(84), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 85), -6), (T["sucked"], sfx.hiss(0.6, 86), -12),
               (T["wagon"], sfx.whoosh(0.4, True, 87), -6), (T["horse"], sfx.clank(240.0, 0.4, 88), -14),
               (T["hoses"], sfx.whirr(1.0, 120.0, 160.0, 89), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 90), -6), (T["s1"], sfx.pop(91), -3), (T["s2"], sfx.pop(92), -3),
               (T["s3"], sfx.pop(93), -3)]
        ev += [(T["cong2"], sfx.pop(94), -2), (T["cong2"], sfx.sparkle(1.4, 18, 95), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 96), -6), (T["t_robot"], sfx.whirr(0.8, 300.0, 340.0, 97), -14),
               (T["t_stuck"], sfx.thud(0.3, 98), -8), (T["t_stuck"] + 0.4, sfx.beep(900.0, 0.12), -10),
               (T["t_stuck"] + 0.8, sfx.beep(900.0, 0.12), -10)]
        return ev


NAME = "vacuum"
EPISODE = Vacuum
