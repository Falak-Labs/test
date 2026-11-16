"""Episode 31 - A wind turbine.  v2 look: a wind farm at dusk, a blade cross-section, a top view, the gearbox.

Sets: farm (the hero turbine on a hill at dusk with a ghost skyscraper for scale and a little house it powers; the
flat paddles that the wind only pushes; the storm, the blades turning their edges into the wind and the brake; the
black blade an eagle can see; a hundred turbines on the ridges; the tag), foil (the blade cut through: a flat plate
the wind pushes, then a wing the wind lifts), top (seen from above: the wind turns, the head points the wrong way,
then the wind vane and the yaw motors turn it back), gear (the nacelle cut open: the slow main shaft, the generator
that wants a thousand turns, then the gearbox).
World: the ground is y = 0, the hero tower stands at x = 0, its hub at y = -HUB.
"""
from v2_base import *  # noqa: F401,F403

HUB, BL = 1520.0, 820.0                      # hub height and blade length (world units)
DUSK = {"top": "#0B1640", "upper": "#22306E", "mid": "#5B4A8E", "low": "#D9775A", "horizon": "#FFB066",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STORM = {"top": "#05070F", "upper": "#0D1220", "mid": "#1B2333", "low": "#2C3446", "horizon": "#3E475C",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
WHITE = "#EEF2F7"
GRASS = ("#3F5F3A", "#2E4A2E", "#1F3322", "#101C14")


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


class Spin:
    """Angle in degrees from a Track of turns per second (integrated, so speed changes never jump)."""

    def __init__(self, track, t_end, dt=1 / 120.0):
        n = int(t_end / dt) + 3
        self.dt = dt
        self.a = np.zeros(n)
        acc = 0.0
        for i in range(1, n):
            acc += track.at((i - 0.5) * dt) * 360.0 * dt
            self.a[i] = acc

    def at(self, t):
        i = clamp(t / self.dt, 0, len(self.a) - 2.001)
        i0 = int(i)
        f = i - i0
        return float(self.a[i0] * (1 - f) + self.a[i0 + 1] * f)


def blade_pts(L, air, wk):
    """Outline of one blade pointing up from the hub (local y < 0): air 0 = a flat wooden paddle, 1 = a tapered wing;
    wk squeezes the width (1 = face on, small = edge on)."""
    rs = (0.05, 0.12, 0.22, 0.38, 0.55, 0.72, 0.88, 1.0)
    lead = (22, 40, 46, 40, 32, 24, 15, 5)           # the wing: curved leading edge
    trail = (22, 30, 30, 25, 20, 15, 10, 4)
    left, right = [], []
    for r, a_, b_ in zip(rs, lead, trail):
        rp = 0.06 + r * 0.62                         # the paddle is shorter, a plain plank
        y = -lerp(rp, r, air) * L
        left.append((-lerp(34, a_, air) * wk, y))
        right.append((lerp(34, b_, air) * wk, y))
    return left + right[::-1]


def blade(c, L, air, wk, col, black=0.0, a=1.0):
    pts = blade_pts(L, air, wk)
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.drawPath(p, lin_paint(-46 * wk - 1, 0, 40 * wk + 1, 0, [shade(col, 0.12), col, shade(col, -0.28)], a=a))
    if air < 0.5:                                    # wood grain on the paddle
        for k in (-14, 0, 14):
            c.drawLine(k * wk, -0.1 * L, k * wk, -0.66 * L, P("#7C5A3A", 0.5 * a * (1 - air * 2), stroke=3))
    if black > 0:
        c.save()
        c.clipRect(R(-80, -L * 1.02 * black, 160, L * 1.02 * black))
        c.drawPath(p, lin_paint(-46 * wk - 1, 0, 40 * wk + 1, 0, ["#3B3F4A", "#1B1E26", "#0B0D12"], a=a))
        c.restore()
    c.drawPath(p, P("#0F172A", 0.35 * a, stroke=3))


def turbine(c, x, s, ang, air=1.0, wk=1.0, black=0.0, blur=0.0, sway=0.0, col=WHITE, dark=0.0, a=1.0, ring=0.0):
    """Front view, feet at (x, 0), scale s. ang = rotor angle (degrees); blur 0..1 adds ghost blades."""
    if a <= 0:
        return
    c.save()
    c.translate(x, 0)
    c.scale(s, s)
    if sway:
        c.rotate(sway)
    tc = mix(col, "#1E2638", dark)
    p = skia.Path()
    p.moveTo(-40, 0)
    p.lineTo(-19, -HUB + 30)
    p.lineTo(19, -HUB + 30)
    p.lineTo(40, 0)
    p.close()
    c.drawPath(p, lin_paint(-40, 0, 40, 0, [shade(tc, -0.3), shade(tc, 0.1), shade(tc, -0.15)], a=a))
    c.drawRRect(rr(-26, -60, 52, 34, 6), P(shade(tc, -0.35), a))            # door
    c.drawRRect(rr(-72, -HUB - 52, 144, 104, 40), lin_paint(0, -HUB - 52, 0, -HUB + 52, [shade(tc, 0.15), shade(tc, -0.25)], a=a))
    bc = mix(col, "#20283A", dark)
    for k in range(int(blur * 5)):                                          # motion ghosts
        for i in range(3):
            c.save()
            c.translate(0, -HUB)
            c.rotate(ang + i * 120 - (k + 1) * 9)
            blade(c, BL, air, wk, bc, a=a * 0.16 * blur)
            c.restore()
    for i in range(3):
        c.save()
        c.translate(0, -HUB)
        c.rotate(ang + i * 120)
        blade(c, BL, air, wk, bc, black if i == 0 else 0.0, a=a)
        c.restore()
    c.drawCircle(0, -HUB, 50, rad_paint(-14, -HUB - 16, 70, [shade(tc, 0.3), tc, shade(tc, -0.4)], a=a))
    c.drawCircle(0, -HUB, 16, P(shade(tc, -0.3), a))
    if ring > 0:                                                            # one turn: a ring fills around the hub
        c.drawCircle(0, -HUB, 210, P("#000000", 0.25 * a, stroke=30))
        c.drawArc(R(-210, -HUB - 210, 420, 420), -90, 360 * ring, False, P(HILITE, a, stroke=26))
    c.restore()


def house(c, x, w, h, lit, a=1.0):
    """Little house standing on (x, 0)."""
    c.drawRect(R(x - w / 2, -h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#7C4A3A", "#A0634B", "#6B3E31"], a=a))
    p = skia.Path()
    p.moveTo(x - w / 2 - 18, -h)
    p.lineTo(x, -h - w * 0.45)
    p.lineTo(x + w / 2 + 18, -h)
    p.close()
    c.drawPath(p, P("#3B2A33", a))
    for k in (-1, 1):
        wx = x + k * w * 0.24
        c.drawRect(R(wx - w * 0.11, -h * 0.72, w * 0.22, h * 0.3), P(mix("#1B2333", "#FFD27A", lit), a))
        if lit > 0:
            add_glow(c, wx, -h * 0.57, w * 0.35, "#FFB347", 0.55 * lit * a)
    c.drawRect(R(x - w * 0.08, -h * 0.5, w * 0.16, h * 0.5), P("#2A1A12", a))


def skyscraper(c, x, w, h, a=1.0):
    """A glass tower standing on (x, 0), for scale."""
    c.drawRect(R(x - w / 2, -h, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#1E2A4A", "#33467A", "#18213D"], a=a))
    c.drawRect(R(x - w * 0.3, -h - 120, w * 0.6, 120), P("#26355F", a))
    c.drawLine(x, -h - 120, x, -h - 300, P("#94A3B8", a, stroke=10))
    rng = random.Random(12)
    for fl in range(40):
        for col in range(5):
            if rng.random() < 0.45:
                c.drawRect(R(x - w / 2 + 20 + col * (w - 40) / 5, -h + 30 + fl * (h - 60) / 40, (w - 40) / 5 - 10, 16),
                           P("#FFD98A", 0.75 * a))
    word(c, "", x, 0, 10, "#FFFFFF", 0)


def far_turbine(c, x, y, s, ang, col="#2A2F55", a=1.0):
    """A small silhouette on a ridge (screen space), feet at (x, y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = skia.Path()
    p.moveTo(-6, 0)
    p.lineTo(-3, -150)
    p.lineTo(3, -150)
    p.lineTo(6, 0)
    p.close()
    c.drawPath(p, P(col, a))
    for i in range(3):
        c.save()
        c.translate(0, -152)
        c.rotate(ang + i * 120)
        c.drawPath(_far_blade(), P(col, a))
        c.restore()
    c.drawCircle(0, -152, 6, P(col, a))
    c.restore()


_FB = None


def _far_blade():
    global _FB
    if _FB is None:
        _FB = skia.Path()
        _FB.moveTo(-4, 0)
        _FB.lineTo(-5, -30)
        _FB.lineTo(0, -82)
        _FB.lineTo(3, -30)
        _FB.lineTo(3, 0)
        _FB.close()
    return _FB


def foil_path(k, chord=560.0, aoa=0.0):
    """Blade cross-section centred at (0, 0): k 0 = a flat plate facing the wind (upright), 1 = a wing (lying
    nearly flat, nose into the wind on the left).  aoa = extra tilt in degrees."""
    n = 18
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        th = 0.12 * (2.97 * math.sqrt(u) - 1.26 * u - 3.52 * u * u + 2.84 * u ** 3 - 1.04 * u ** 4) * 1.4
        camber = 0.05 * math.sin(math.pi * u)
        x = (u - 0.4) * chord
        top.append((x, -(camber + th) * chord))
        bot.append((x, -(camber - th * 0.55) * chord))
    plate_t = [((u / n - 0.5) * chord * 0.9, -9) for u in range(n + 1)]
    plate_b = [((u / n - 0.5) * chord * 0.9, 9) for u in range(n + 1)]
    ang = math.radians(lerp(90.0, 8.0, e_io(k)) + aoa)
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for (x0, y0), (x1, y1) in zip(plate_t + plate_b[::-1], top + bot[::-1]):
        x, y = lerp(x0, x1, k), lerp(y0, y1, k)
        pts.append((x * ca - y * sa, x * sa + y * ca))
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def gear(c, x, y, r, teeth, ang, col, a=1.0, hub=None):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    tw = 2 * math.pi * r / teeth * 0.5
    for i in range(teeth):
        c.save()
        c.rotate(i * 360.0 / teeth)
        c.drawRRect(rr(-tw / 2, -r - 16, tw, 26, 4), P(shade(col, -0.15), a))
        c.restore()
    c.drawCircle(0, 0, r, rad_paint(-r * 0.3, -r * 0.3, r * 1.4, [shade(col, 0.25), col, shade(col, -0.35)], a=a))
    c.drawCircle(0, 0, r * 0.72, P(shade(col, -0.2), a, stroke=6))
    for i in range(4 if r > 60 else 0):
        c.save()
        c.rotate(i * 90 + 45)
        c.drawRRect(rr(-r * 0.12, -r * 0.62, r * 0.24, r * 0.4, 6), P(shade(col, -0.45), a))
        c.restore()
    c.drawCircle(0, 0, hub or r * 0.2, P("#1E293B", a))
    c.restore()


def eagle(c, x, y, s, t, ang=0.0, a=1.0):
    """A white-tailed eagle gliding / flapping, heading right (rotate with ang)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    fl = math.sin(t * 9) * 26
    for sd in (-1, 1):
        p = skia.Path()
        p.moveTo(-10, 0)
        p.cubicTo(-30, sd * 20, -60, sd * (60 + fl * 0.4), -40, sd * (110 + fl))
        p.lineTo(10, sd * (90 + fl * 0.8))
        p.cubicTo(20, sd * 40, 20, sd * 14, 16, 0)
        p.close()
        c.drawPath(p, P("#5B3A22", a))
    c.drawOval(R(-60, -14, 110, 28), P("#6B4423", a))
    c.drawPath(_tail(), P("#F1F5F9", a))
    c.drawCircle(56, -2, 16, P("#E7E2D6", a))
    beak = skia.Path()
    beak.moveTo(68, -8)
    beak.lineTo(88, 0)
    beak.lineTo(68, 6)
    beak.close()
    c.drawPath(beak, P("#FACC15", a))
    c.drawCircle(60, -6, 3.5, P("#0F172A", a))
    c.restore()


def _tail():
    p = skia.Path()
    p.moveTo(-56, -10)
    p.lineTo(-96, -20)
    p.lineTo(-100, 18)
    p.lineTo(-56, 10)
    p.close()
    return p


def desk_fan(c, x, y, s, t, a=1.0):
    """A huge desk fan standing on (x, y), seen from the side and a little from behind, blowing to the right."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawOval(R(-130, -30, 260, 48), P("#1E293B", a))
    c.drawOval(R(-130, -40, 260, 48), lin_paint(-130, 0, 130, 0, ["#475569", "#94A3B8", "#475569"], a=a))
    c.drawRRect(rr(-16, -330, 32, 300, 12), lin_paint(-16, 0, 16, 0, ["#64748B", "#E2E8F0", "#64748B"], a=a))
    c.drawRRect(rr(-110, -500, 120, 120, 40), lin_paint(0, -500, 0, -380, ["#E2E8F0", "#94A3B8"], a=a))   # motor
    c.save()
    c.translate(40, -440)
    c.scale(0.55, 1.0)                                  # the cage seen at an angle, facing right
    c.drawCircle(0, 0, 210, P("#0F172A", 0.25 * a))
    for i in range(3):
        c.save()
        c.rotate(t * 1100 + i * 120)
        c.drawOval(R(-46, -196, 92, 186), P("#7DD3FC", 0.65 * a))
        c.restore()
    for i in range(12):
        c.save()
        c.rotate(i * 15)
        c.drawLine(0, -210, 0, 210, P("#E2E8F0", 0.75 * a, stroke=4))
        c.restore()
    c.drawCircle(0, 0, 210, P("#E2E8F0", a, stroke=12))
    c.drawCircle(0, 0, 36, P("#475569", a))
    c.restore()
    c.restore()


def mustache_dad(c, x, y, h, t, a=1.0, pose="point"):
    person(c, x, y, h, "#2563EB", t, pose=pose, face=1, hair="#1F1A17", skin="#C68B5E", a=a)
    u = h / 140.0
    p = skia.Path()
    p.moveTo(x - 12 * u, y - 118 * u)
    p.cubicTo(x - 6 * u, y - 124 * u, x + 6 * u, y - 124 * u, x + 14 * u, y - 118 * u)
    p.cubicTo(x + 6 * u, y - 114 * u, x - 6 * u, y - 114 * u, x - 12 * u, y - 118 * u)
    c.drawPath(p, P("#1F1A17", a))


def comment_card(c, x, y, s, p, likes="24.1K"):
    """A social-media comment (screen space)."""
    if p <= 0:
        return
    k = e_back(clamp(p * 1.25))
    w = min(1000, max(560, text_width(s, 34, "Poppins-Bold") + 270))
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    c.drawRRect(rr(-w / 2, -70, w, 140, 30), P("#000000", 0.35 * p, blur=16))
    c.drawRRect(rr(-w / 2, -70, w, 140, 30), P("#F8FAFC", 0.97 * p))
    c.drawCircle(-w / 2 + 58, -6, 34, P("#F59E0B", p))
    text(c, "?", -w / 2 + 58, 8, 40, "#FFFFFF", "Poppins-Black", a=p)
    text(c, "@just_asking", -w / 2 + 110, -26, 24, "#64748B", "Poppins-Bold", align="left", a=p)
    text(c, s, -w / 2 + 110, 22, 34, "#0F172A", "Poppins-Bold", align="left", a=p)
    heart(c, w / 2 - 70, -14, 0.8, p, "#F43F5E")
    text(c, likes, w / 2 - 70, 40, 22, "#64748B", "Poppins-Bold", a=p)
    c.restore()


def bubble(c, x, y, s, p, rtl=True):
    """Speech bubble with a tail pointing down-left (screen space)."""
    if p <= 0:
        return
    k = e_back(clamp(p * 1.25))
    size = 44
    w = (arabic.width_ar(s, size * 1.15, "Tajawal-Black") if arabic.is_ar(s) else text_width(s, size, "Poppins-Black")) + 80
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    tail = skia.Path()
    tail.moveTo(-w * 0.25, 40)
    tail.lineTo(-w * 0.32, 100)
    tail.lineTo(-w * 0.1, 40)
    tail.close()
    c.drawRRect(rr(-w / 2, -60, w, 120, 40), P("#000000", 0.35 * p, blur=14))
    c.drawPath(tail, P("#FFFFFF", p))
    c.drawRRect(rr(-w / 2, -60, w, 120, 40), P("#FFFFFF", p))
    word(c, s, 0, 16, size, "#0F172A", p)
    c.restore()


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=10, head=26):
    if a <= 0:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - math.cos(ang) * head * 0.8, y1 - math.sin(ang) * head * 0.8
    c.drawLine(x0, y0, bx, by, P(col, a, stroke=w))
    p = skia.Path()
    p.moveTo(x1, y1)
    p.lineTo(x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head)
    p.lineTo(x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)
    p.close()
    c.drawPath(p, P(col, a))


# ====================================================================================== the episode
class Turbine(EpisodeV2):
    BUILD_NO = 31
    COVER_T = ("closer", 0.6)
    FIRST_SET = "farm"
    CLEAR = "#070B1F"
    TITLE = {"en": "WIND TURBINE", "ar_sa": "توربينة رياح"}
    EMPH = {"en": ["CONGRATS", "FAN", "TALLER", "SKYSCRAPERS", "TURN", "HOME", "TWO", "DAYS", "WIND", "TURBINE",
                   "PUSHES", "FLAT", "PADDLE", "SLOW", "SHAPE", "AIRPLANE", "WING", "LIFTS", "AROUND", "CHANGING",
                   "DIRECTION", "WRONG", "VANE", "MOTORS", "HEAD", "TEN", "MINUTE", "GENERATOR", "THOUSAND", "GEARBOX",
                   "MULTIPLIES", "HUNDRED", "STORM", "FAST", "TEAR", "APART", "TWIST", "EDGES", "SLOWS", "BRAKE",
                   "LOCKS", "FOLLOW", "SPACE", "TELESCOPE", "PAINT", "BLACK", "BIRDS", "PLANT", "NEVER", "STOPS",
                   "BLADES", "FOOTBALL", "FIELD", "THREE", "KILOMETERS", "SEVENTY", "PERCENT", "FEWER", "YOURSELF",
                   "COMMENT", "FRONT"],
            "ar_sa": ["مبروك", "مروحة", "أطول", "ناطحة", "ولفة", "بيت", "يومين", "توربينة", "رياح", "بيزق",
                      "المفرودة", "بطيء", "جناح", "الطيارة", "يرفعها", "ويلفها", "اتجاهه", "الغلط", "دوارة",
                      "للمواتير", "الراس", "عشر", "الدقيقة", "والمولد", "ألف", "فتيس", "يكبر", "مية", "عاصفة",
                      "بسرعة", "تفرتك", "بحرفها", "فتهدى", "والفرامل", "تقفلها", "تابعني", "تلسكوب", "فضائي",
                      "ادهن", "إسود", "الطيور", "وازرع", "الزعفرانة", "بيقفش", "ملعب", "بتلتمية", "سبعين",
                      "بإيدك", "أبوك", "اطفي", "النور", "غالية"]}
    KEYS = {"ar_sa": {
        ("hook", "FAN"): "مروحة", ("hook", "TALLER"): "أطول", ("hook", "SKYSCRAPERS"): "ناطحة",
        ("hook", "TURN"): "لفة", ("hook", "HOME"): "بيت", ("hook", "DAYS"): "يومين", ("hook", "CONGRATS"): "مبروك",
        ("hook", "WIND"): "توربينة",
        ("break1", "PUSHES"): "بيزق", ("break1", "FLAT"): "المفرودة", ("break1", "SLOW"): "بطيء",
        ("fix1", "SHAPE"): "فتعمل", ("fix1", "AIRPLANE"): "الطيارة", ("fix1", "WING"): "جناح",
        ("fix1", "LIFTS"): "يرفعها", ("fix1", "AROUND"): "ويلفها",
        ("break2", "CHANGING"): "يغير", ("break2", "DIRECTION"): "اتجاهه", ("break2", "WRONG"): "الغلط",
        ("fix2", "VANE"): "دوارة", ("fix2", "MOTORS"): "للمواتير", ("fix2", "HEAD"): "الراس", ("fix2", "INTO"): "وش",
        ("break3", "TEN"): "عشر", ("break3", "MINUTE"): "الدقيقة", ("break3", "GENERATOR"): "والمولد",
        ("break3", "THOUSAND"): "ألف",
        ("fix3", "GEARBOX"): "فتيس", ("fix3", "MULTIPLIES"): "يكبر", ("fix3", "HUNDRED"): "مية",
        ("break4", "STORM"): "عاصفة", ("break4", "FAST"): "بسرعة", ("break4", "TEAR"): "تفرتك",
        ("fix4", "TWIST"): "تلف", ("fix4", "EDGES"): "بحرفها", ("fix4", "SLOWS"): "فتهدى",
        ("fix4", "BRAKE"): "والفرامل", ("fix4", "PASSES"): "تعدي",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PAINT"): "ادهن", ("reveal", "BLACK"): "اسود", ("reveal", "BIRDS"): "الطيور",
        ("reveal", "PLANT"): "وازرع", ("reveal", "HUNDRED"): "مية", ("reveal", "NEVER"): "بيقفش",
        ("stat", "BLADES"): "ريشة", ("stat", "TIPS"): "طرفها", ("stat", "SEVENTY"): "سبعين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "COMMENT"): "أبوك", ("tag", "FAN"): "اطفي", ("tag", "FRONT"): "غالية"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a space telescope"),
                   "stat": [("107 m", "BLADES"), ("300 km/h", "AT THE TIPS"), ("70%", "FEWER BIRDS HIT")],
                   "L": {"turbine": "YOUR WIND TURBINE", "taller": "TALLER THAN MOST SKYSCRAPERS", "turn": "1 TURN",
                         "days": "= A HOME FOR 2 DAYS", "push": "WIND JUST PUSHES", "slow": "TOO SLOW",
                         "wing": "SHAPED LIKE A WING", "lift": "LIFT", "wind": "WIND", "wrong": "FACING THE WRONG WAY",
                         "vane": "WIND VANE", "motors": "YAW MOTORS", "head": "HEAD TURNS INTO THE WIND",
                         "rpm10": "10 TURNS / MIN", "need": "GENERATOR WANTS 1,000+", "gearbox": "GEARBOX",
                         "x100": "x 100", "fast": "1,000+ TURNS / MIN", "storm": "STORM", "tear": "TOO FAST!",
                         "edges": "EDGES INTO THE WIND", "brake": "BRAKE LOCKED", "black": "ONE BLACK BLADE",
                         "birds": "BIRDS SEE IT", "hundred": "x 100", "never": "WHERE THE WIND NEVER STOPS",
                         "comment": "why not just put a fan in front of it?", "dad": ""}},
            "ar_sa": {"follow": ("تابعني", "الجاي: تلسكوب فضائي"),
                      "stat": [("107", "متر طول الريشة"), ("300", "كم/س سرعة الطرف"), ("70%", "خبطات طيور أقل")],
                      "L": {"turbine": "التوربينة بتاعتك", "taller": "أطول من ناطحة سحاب", "turn": "لفة واحدة",
                            "days": "= بيت يومين", "push": "الهوا بيزق وبس", "slow": "بطيء",
                            "wing": "زي جناح الطيارة", "lift": "بيرفعها", "wind": "الهوا",
                            "wrong": "في الناحية الغلط", "vane": "دوّارة الهوا", "motors": "المواتير",
                            "head": "الراس في وش الهوا", "rpm10": "10 لفات في الدقيقة",
                            "need": "المولّد عايز أكتر من 1000", "gearbox": "الفتيس", "x100": "مية مرة",
                            "fast": "أكتر من 1000 لفة", "storm": "عاصفة", "tear": "هتتفرتك!",
                            "edges": "الحرف في وش الهوا", "brake": "الفرامل مقفولة", "black": "ريشة سودا",
                            "birds": "الطيور شايفاها", "hundred": "مية توربينة", "never": "الزعفرانة: الهوا ما بيقفش",
                            "comment": "", "dad": "اطفي النور، الكهربا غالية!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "fan": ("hook", "FAN", 0.08), "taller": ("hook", "TALLER", 0.15), "sky": ("hook", "SKYSCRAPERS", 0.25),
            "turn": ("hook", "TURN", 0.4), "home": ("hook", "HOME", 0.55), "days": ("hook", "DAYS", 0.65),
            "congrats": ("hook", "CONGRATS", 0.72), "wind": ("hook", "WIND", 0.9),
            "pushes": ("break1", "PUSHES", 0.3), "flat": ("break1", "FLAT", 0.5), "slow": ("break1", "SLOW", 0.9),
            "shape": ("fix1", "SHAPE", 0.1), "airplane": ("fix1", "AIRPLANE", 0.35), "wing": ("fix1", "WING", 0.45),
            "lifts": ("fix1", "LIFTS", 0.75), "around": ("fix1", "AROUND", 0.9),
            "changing": ("break2", "CHANGING", 0.3), "direction": ("break2", "DIRECTION", 0.4),
            "wrong": ("break2", "WRONG", 0.9),
            "vane": ("fix2", "VANE", 0.2), "motors": ("fix2", "MOTORS", 0.45), "head": ("fix2", "HEAD", 0.7),
            "into": ("fix2", "INTO", 0.85),
            "ten": ("break3", "TEN", 0.3), "minute": ("break3", "MINUTE", 0.45),
            "generator": ("break3", "GENERATOR", 0.65), "thousand": ("break3", "THOUSAND", 0.9),
            "gearbox": ("fix3", "GEARBOX", 0.2), "multiplies": ("fix3", "MULTIPLIES", 0.45),
            "hundred": ("fix3", "HUNDRED", 0.8),
            "storm": ("break4", "STORM", 0.2), "fast": ("break4", "FAST", 0.5), "tear": ("break4", "TEAR", 0.75),
            "twist": ("fix4", "TWIST", 0.15), "edges": ("fix4", "EDGES", 0.25), "slows": ("fix4", "SLOWS", 0.5),
            "brake": ("fix4", "BRAKE", 0.65), "passes": ("fix4", "PASSES", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "paint": ("reveal", "PAINT", 0.1), "black": ("reveal", "BLACK", 0.25), "birds": ("reveal", "BIRDS", 0.38),
            "plant": ("reveal", "PLANT", 0.6), "hundred2": ("reveal", "HUNDRED", 0.7), "never": ("reveal", "NEVER", 0.92),
            "s1": ("stat", "BLADES", 0.04), "s2": ("stat", "TIPS", 0.4), "s3": ("stat", "SEVENTY", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "comment": ("tag", "COMMENT", 0.3), "fan2": ("tag", "FAN", 0.65), "front": ("tag", "FRONT", 0.9)})
        T["sky0"] = min(T["taller"], T["sky"]) - 0.1
        T["turn0"] = T["turn"] - 0.1
        T["days1"] = max(T["days"], T["turn"] + 0.9)
        T["foil1"] = max(T["lifts"], T["wing"] + 0.6) - 0.1                   # fix1: the lift arrow
        T["back1"] = max(T["around"] - 0.1, T["foil1"] + 0.8)                 # fix1: back to the spinning rotor
        T["wd"] = min(T["changing"], T["direction"]) - 0.2                     # break2: the wind turns
        T["yaw"] = max(T["motors"], T["vane"] + 0.5) - 0.1
        T["bx"] = min(T["gearbox"], T["multiplies"]) - 0.15
        T["tw"] = min(T["twist"], T["edges"]) - 0.1
        T["stop"] = max(T["brake"], T["slows"] + 0.5)
        T["paint0"] = min(T["paint"], T["black"]) - 0.1
        T["wide"] = min(T["plant"], T["hundred2"]) - 0.25
        # ---- sets
        self.cut(s("break1") - 0.12, "farm", 1)
        self.cut(s("fix1") - 0.12, "foil", -1)
        self.cut(T["back1"], "farm", 1)
        self.cut(s("break2") - 0.12, "top", -1)
        self.cut(s("break3") - 0.12, "gear", 1)
        self.cut(s("break4") - 0.12, "farm", -1)
        self.cut(s("cta") - 0.12, "farm", 1)
        self.cut(s("tag") - 0.2, "farm", -1)
        # ---- cameras
        cm = self.cams = {"farm": Camera(0, -1300, 0.6)}
        f = cm["farm"]
        f.key(0.05, 0, -1250, 0.52, max(0.6, T["sky0"] - 0.1))
        f.key(T["sky0"], -260, -1130, 0.40, 1.1)
        f.key(T["turn0"] - 0.2, 140, -1100, 0.46, 1.0)
        f.key(T["wind"] - 0.3, 60, -1150, 0.43, 1.2)
        f.key(s("break1") - 0.12, 0, -1460, 0.9, 0.0).key(s("break1"), 0, -1480, 0.86, 3.0)
        f.key(T["back1"], 0, -1380, 0.62, 0.0).key(T["back1"] + 0.05, 0, -1340, 0.58, 1.0)
        f.key(s("break4") - 0.12, 0, -1170, 0.43, 0.0).key(s("break4"), 0, -1200, 0.45, 3.0)
        f.key(T["stop"], 0, -1180, 0.44, 2.0)
        f.key(s("cta") - 0.12, 0, -1200, 0.47, 0.0)
        f.key(s("reveal"), 0, -1420, 0.66, 1.2)
        f.key(T["wide"], 0, -1100, 0.24, 1.6)
        f.key(s("stat") - 0.2, 0, -980, 0.24, 1.0)
        f.key(s("closer") - 0.1, 0, -1112, 0.49, 1.3)
        if self.rtl:                                                       # tag: the dad at the house
            f.key(s("tag") - 0.2, 250, -270, 1.0, 0.0).key(s("tag"), 262, -262, 1.04, 3.0)
        else:                                                              # tag: a desk fan in front of it
            f.key(s("tag") - 0.2, -260, -900, 0.5, 0.0).key(s("tag"), -240, -910, 0.51, 3.0)
        # ---- tracks
        n = 1.0 / max(0.6, T["days1"] - T["turn0"])                          # exactly one turn between "turn" and "days"
        sp = Track(0.22).to(T["turn0"] - 0.3, n, 0.3).to(T["days1"], 0.24, 0.5)
        sp.to(s("break1") - 0.12, 0.05, 0.0).to(T["back1"], 0.36, 0.0).to(s("break2") - 0.12, 0.3, 0.0)
        sp.to(s("break4") - 0.12, 0.35, 0.0).to(T["storm"], 1.15, max(0.6, T["fast"] - T["storm"] + 0.3))
        sp.to(T["tw"] + 0.2, 0.0, max(1.2, T["stop"] - T["tw"]))
        sp.to(s("cta") - 0.12, 0.25, 0.0)
        self.speed = sp
        self.spin = Spin(sp, self.duration + 1)
        self.air = Track(1.0).to(s("break1") - 0.12, 0.0, 0.0).to(T["back1"], 1.0, 0.0)
        self.foil = Track(0.0).to(T["shape"], 1.0, max(0.8, T["wing"] - T["shape"] + 0.2))
        self.feather = Track(0.0).to(T["tw"], 1.0, 1.0).to(T["passes"] + 0.2, 0.0, 1.0)
        self.storm = Track(0.0).to(s("break4") - 0.12, 1.0, 0.0).to(T["passes"] - 0.4, 0.0, 1.2)
        self.black = Track(0.0).to(T["paint0"], 1.0, max(0.7, T["black"] - T["paint0"] + 0.3))
        self.farm_k = Track(0.0).to(T["wide"], 1.0, max(1.2, T["never"] - T["wide"]))
        self.wdir = Track(0.0).to(T["wd"], -62.0, 1.4)                        # top view: where the wind blows to
        self.vane = Track(0.0).to(T["vane"] - 0.1, -62.0, 0.6)
        self.yaw = Track(180.0).to(T["yaw"], 118.0, max(1.2, T["into"] - T["yaw"] + 0.2))
        self.gbox = Track(0.0).to(T["bx"], 1.0, 0.6)
        self.spans = [(T["slow"], T["around"] + 0.3), (T["wrong"], T["into"] + 0.3),
                      (T["thousand"], T["hundred"] + 0.3), (T["tear"], T["passes"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["slow"], 0.3, 5), (T["wrong"], 0.3, 6), (T["thousand"], 0.3, 6),
                       (T["storm"], 0.5, 10), (T["tear"], 0.6, 14), (T["stop"], 0.3, 6), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(31)
        self.far = [(rng.uniform(-1.2, 1.2), rng.uniform(0, 360), rng.uniform(0.7, 1.1)) for _ in range(26)]
        self.rows = [(i, rng.uniform(0, 360)) for i in range(-6, 7) if i]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def rotor_ang(self, t):
        return self.spin.at(t)

    # ------------------------------------------------------------------ set: the farm
    def draw_farm(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["farm"].at(t)
        cx, cy, z = cam
        self.ui["cam"] = cam
        st = self.storm.at(t) if s("break4") - 0.12 <= t < s("cta") - 0.12 else 0.0
        pal = {k: mix(DUSK[k], STORM[k], st) for k in DUSK}
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=gy - 60 * z)
        v2.stars(c, W, H, t, 0.5 * (1 - st))
        sx, sy = 820 - cx * 0.03, gy - 300 - 120 * z
        add_glow(c, sx, sy, 300, "#FF9A4D", 0.5 * (1 - st))
        c.drawCircle(sx, sy, 70, P("#FFD9A0", 0.9 * (1 - st)))
        for i, (px, py, s_) in enumerate(((180, 820, 1.0), (760, 660, 0.8), (430, 980, 0.7))):
            v2.cloud(c, (px + t * (8 + st * 120) - cx * 0.03 * z) % (W + 700) - 300, gy - py * (0.6 + z * 0.5), s_ * (1 + st * 0.6),
                     body=mix("#3A3568", "#1A1F2E", st), rim=mix("#FF9D73", "#4B5568", st), a=0.85, seed=i)
        # far ridges with turbines
        far_k = self.farm_k.at(t)
        for layer, (par, base, col, sc, cnt) in enumerate(((0.03, 150, "#3A3378", 0.55, 14), (0.07, 60, "#262A5A", 0.8, 12))):
            c.save()
            c.translate(W / 2 - cx * par * z, gy - base * (0.4 + z))
            v2.ridge(c, -1500, 1500, 0, 160, mix(col, "#20242E", st), mix("#1B1C4A", "#151820", st), seed=5 + layer, step=150, rough=0.5)
            c.restore()
            for i in range(cnt):
                fx_, ph, ss = self.far[i + layer * 13]
                x = W / 2 + fx_ * 900 + i * 0 - cx * par * z
                k = clamp(far_k * 2.2 - i * 0.09) if layer == 0 or i % 3 else max(clamp(far_k * 2.2 - i * 0.09), 0.0)
                base_k = 0.35 if (i % 4 == 0 and layer == 1) else 0.0
                k = max(k, base_k)
                if k > 0:
                    far_turbine(c, x, gy - base * (0.4 + z) + 6, sc * ss * (0.5 + z * 0.7) * e_back(clamp(k * 1.2)),
                                self.rotor_ang(t) * (0.8 + ss * 0.3) + ph, col=mix("#4A4F86" if layer else "#5A5B9A", "#262B36", st),
                                a=clamp(k * 2))
        self.view(c, cam)
        x0, x1 = cx - 620 / z, cx + 620 / z
        vrect(c, x0, 0, x1 - x0, 3000, [mix(GRASS[0], "#1E2A22", st), GRASS[1], GRASS[2], GRASS[3]], [0, 0.08, 0.3, 1])
        c.drawRect(R(x0, -8, x1 - x0, 16), P(mix("#5E8A4E", "#2A3A2C", st), 0.9))
        # scale ghost: a skyscraper
        gk = self.span(T["sky0"], T["turn0"] + 0.2, 0.4, 0.4) if t < s("break1") else 0.0
        if gk > 0:
            skyscraper(c, -760, 300, 1500, gk)
        # the little house and its power line
        lit = clamp(prog(t, T["days1"] - 0.15, T["days1"] + 0.25)) if t < s("break1") else 1.0 - st * 0.8
        if self.rtl and t >= s("tag") - 0.2:
            lit = 1 - prog(t, T["fan2"] + 0.1, T["fan2"] + 0.3)
        house(c, 470, 210, 150, lit)
        cab = skia.Path()
        cab.moveTo(30, -20)
        cab.quadTo(200, 30, 360, -20)
        c.drawPath(cab, P("#0F172A", 0.6, stroke=6))
        if t < s("break1") and T["turn0"] <= t < T["days1"] + 0.3:
            q = prog(t, T["turn0"], T["days1"])
            add_glow(c, lerp(30, 360, q), 4 + math.sin(q * math.pi) * 20, 40, HILITE, 0.9)
        # the other turbines of the row (after "plant")
        for i, ph in self.rows:
            k = clamp(far_k * 1.8 - abs(i) * 0.12) if t < s("tag") - 0.2 else 0.0
            if k > 0:
                turbine(c, i * 1250, 0.9 * e_back(clamp(k * 1.2)), self.rotor_ang(t) + ph, dark=0.15, a=clamp(k * 2))
        # the hero
        ang = self.rotor_ang(t)
        spd = self.speed.at(t)
        blur = clamp((spd - 0.45) / 0.6) if st > 0 else 0.0
        sway = math.sin(t * 7.0) * 0.5 * clamp(blur * 1.2) * (1 - self.feather.at(t))
        wk = lerp(1.0, 0.2, self.feather.at(t)) if s("break4") - 0.12 <= t < s("cta") - 0.12 else 1.0
        ring = prog(t, T["turn0"], T["days1"]) if t < s("break1") else 0.0
        black = self.black.at(t) if t >= s("reveal") - 0.2 else 0.0
        turbine(c, 0, 1.0, ang, air=self.air.at(t), wk=wk, black=black, blur=blur, sway=sway, dark=st * 0.3,
                ring=ring if ring < 1 else 0.0)
        self.ui["hub"] = self.at(0, -HUB)
        # wind streaks
        wa = 0.5 if s("break1") - 0.12 <= t < T["back1"] else 0.0
        wa = max(wa, 0.7 * st)
        if wa > 0:
            rng = random.Random(7)
            for i in range(26):
                yy = -HUB - 900 + rng.uniform(0, 1500)
                xx = x0 + ((t * (900 + st * 1600) + rng.uniform(0, 3000)) % (x1 - x0 + 600)) - 300
                c.drawLine(xx, yy, xx + 160 + st * 140, yy + st * 40, P("#E2E8F0", wa * 0.6, stroke=4 / z ** 0.5))
        # storm rain and lightning
        if st > 0:
            rng = random.Random(9)
            for i in range(70):
                xx = x0 + (rng.uniform(0, 1) * (x1 - x0) + t * 300) % (x1 - x0)
                yy = cy - 1000 / z + ((rng.uniform(0, 1) * 2200 / z + t * 2600) % (2200 / z))
                c.drawLine(xx, yy, xx + 30, yy + 90, P("#9FB3C8", 0.45 * st, stroke=3 / z ** 0.5))
        # eagle in the reveal
        if s("reveal") - 0.1 <= t < s("stat"):
            q = prog(t, T["birds"] - 0.6, T["birds"] + 1.6)
            if 0 < q < 1:
                ex = lerp(950, -650, q)
                ey = -HUB - 380 + math.sin(q * math.pi) * -200 - q * 260
                turn_k = clamp((q - 0.35) * 3)
                eagle(c, ex, ey, 2.0, t, ang=180 + lerp(0, -38, turn_k), a=clamp(q * 8) * clamp((1 - q) * 6))
                self.ui["eagle"] = self.at(ex, ey)
        # the tag
        if t >= s("tag") - 0.2:
            if not self.rtl:
                fk = prog(t, T["fan2"] - 0.2, T["fan2"] + 0.15)
                c.save()
                c.translate(-600, 0)
                c.scale(e_back(fk), e_back(fk))
                desk_fan(c, 0, 0, 1.9, t, a=clamp(fk * 3))
                c.restore()
                cord = skia.Path()
                cord.moveTo(-640, -10)
                cord.quadTo(-330, 50, -44, -30)
                c.drawPath(cord, P("#111827", 0.9, stroke=10))
                c.drawRRect(rr(-54, -54, 18, 34, 4), P("#F8FAFC"))
                for i in range(6):
                    yy = -1100 + i * 90
                    ph = (t * 1.6 + i * 0.23) % 1.0
                    c.drawLine(-380 + ph * 300, yy, -260 + ph * 300, yy, P("#BFDBFE", 0.8 * (1 - ph), stroke=12))
            else:
                q = prog(t, T["comment"] - 0.4, T["comment"] + 0.5)
                mustache_dad(c, lerp(80, 290, e_out(q)), 0, 180, t, pose="walk" if q < 1 else "point")
        c.restore()

    def ui_farm(self, c, t, tw):
        T, s = self.T, self.tl.s
        hx, hy = self.ui.get("hub", (540, 600))
        if tw < s("break1") - 0.12:
            self.chip(540, 1120, "taller", T["sky0"] + 0.1, T["turn0"] + 0.1, accent=HILITE, size=36)
            self.chip(hx, hy + 170, "turn", T["turn0"], T["days1"] + 0.2, accent=HILITE, size=38)
            x0, y0 = self.at(470, -200)
            self.label(x0, y0, 760, 1080, "days", T["days1"] - 0.1, s("break1") - 0.1, HILITE, size=34)
            self.chip(540, 470, "turbine", T["wind"] - 0.15, s("break1") + 0.1, accent=ACCENT, size=38)
            return
        if tw < T["back1"] and tw < s("fix1"):
            self.chip(540, 1110, "push", T["pushes"] - 0.1, s("fix1") - 0.15, accent="#CBD5E1", size=38)
            self.chip(540, 470, "slow", T["slow"] - 0.1, s("fix1") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["slow"] + 0.1, s("fix1") - 0.2, x=880, y=330)
            self.red(T["slow"] + 0.1, 1.6)
            return
        if tw < s("break2"):
            self.badge("check", T["back1"] + 0.1, s("break2") - 0.15, x=880, y=330)
            self.chip(540, 470, "wing", T["back1"], s("break2") - 0.15, accent=GOOD, size=38)
            return
        if s("break4") - 0.12 <= tw < s("cta") - 0.12:
            self.chip(540, 470, "storm", T["storm"] - 0.1, T["tear"] - 0.1, accent="#94A3B8", size=40)
            self.chip(540, 470, "tear", T["tear"] - 0.05, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["tear"] + 0.1, s("fix4") - 0.2, x=880, y=330)
            self.red(T["tear"] + 0.1, 2.0)
            k = self.span(T["tw"], T["passes"])
            if k > 0:
                self.pitch_inset(c, 820, 700, k, prog(tw, T["tw"], T["tw"] + 1.0))
                word(c, self.L["edges"], 820, 900, 30, "#F8FAFC", k)
            self.chip(540, 470, "brake", T["brake"] - 0.05, s("cta") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["passes"] + 0.05, s("cta") - 0.15, x=880, y=330)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.1:
            x0, y0 = self.at(0, -HUB - 560)
            self.label(x0, y0, 290, 560, "black", T["paint0"] + 0.2, T["plant"] - 0.1, "#94A3B8", size=34)
            ex, ey = self.ui.get("eagle", (700, 500))
            self.chip(780, 760, "birds", T["birds"], T["plant"] - 0.1, accent=GOOD, size=36)
            self.chip(540, 520, "hundred", T["hundred2"] - 0.1, T["never"] - 0.1, accent=HILITE, size=44)
            self.chip(540, 520, "never", T["never"] - 0.1, s("stat") - 0.15, accent=ACCENT, size=36)
            return
        if tw >= s("tag") - 0.2:
            if not self.rtl:
                comment_card(c, 540, 380, self.L["comment"], self.span(T["comment"] - 0.1, self.duration + 1, 0.3, 0.1))
            else:
                bubble(c, 610, 640, self.L["dad"], self.span(T["fan2"] - 0.25, self.duration + 1, 0.3, 0.1))

    def pitch_inset(self, c, x, y, k, q):
        """Round inset: the blade's cross-section turning its edge into the wind."""
        c.save()
        c.translate(x, y)
        c.scale(e_back(clamp(k * 1.2)), e_back(clamp(k * 1.2)))
        c.drawCircle(0, 0, 150, P("#000000", 0.35 * k, blur=14))
        c.drawCircle(0, 0, 150, P("#0F172A", 0.92 * k))
        c.drawCircle(0, 0, 150, P("#94A3B8", 0.8 * k, stroke=4))
        for i in range(4):
            yy = -90 + i * 60
            ph = (self._t * 1.5 + i * 0.3) % 1.0
            arrow(c, -130 + ph * 60, yy, -70 + ph * 60, yy, "#BFDBFE", 0.6 * k, w=5, head=14)
        c.save()
        c.scale(0.36, 0.36)
        c.rotate(lerp(-80, 0, e_io(q)))
        c.drawPath(foil_path(1.0, 560, 0), lin_paint(0, -60, 0, 60, ["#F8FAFC", "#94A3B8"], a=k))
        c.restore()
        c.restore()

    # ------------------------------------------------------------------ set: the blade cut through (fix1)
    def draw_foil(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.2, pal=DUSK, horizon_y=H * 0.8)
        k = self.foil.at(t)
        lift = prog(t, T["foil1"], T["foil1"] + 0.5)
        # background streaks rushing down once the wing lifts (it flies up)
        rng = random.Random(3)
        for i in range(30):
            xx = rng.uniform(0, W)
            yy = (rng.uniform(0, H) + t * 1600 * lift) % (H + 200) - 100
            c.drawLine(xx, yy, xx, yy - 120, P("#CBD5E1", 0.18 * lift, stroke=4))
        c.save()
        c.translate(540, 820)
        # streamlines: straight, bunched against the plate, or curving over the wing
        for i in range(9):
            yy = -420 + i * 105
            pth = skia.Path()
            first = True
            for xx in range(-560, 580, 20):
                d = math.exp(-(xx / 260.0) ** 2)
                bend = -k * d * 90 * (1 if yy < 40 else 0.4) * clamp(1 - abs(yy) / 520)
                block = (1 - k) * d * (60 if abs(yy) < 280 else 0) * (1 if yy > 0 else -1)
                py = yy + bend + block
                if first:
                    pth.moveTo(xx, py)
                    first = False
                else:
                    pth.lineTo(xx, py)
            c.drawPath(pth, P("#BFDBFE", 0.35, stroke=4))
            ph = (t * (0.6 + k * 0.6) + i * 0.17) % 1.0
            xx = -560 + ph * 1120
            d = math.exp(-(xx / 260.0) ** 2)
            py = yy - k * d * 90 * (1 if yy < 40 else 0.4) * clamp(1 - abs(yy) / 520) + (1 - k) * d * (60 if abs(yy) < 280 else 0) * (1 if yy > 0 else -1)
            if (1 - k) > 0.5 and abs(yy) < 280 and xx > -120:
                continue
            arrow(c, xx - 50, py, xx + 30, py, "#E0F2FE", 0.8, w=7, head=22)
        c.drawPath(foil_path(k), lin_paint(0, -140, 0, 140, [mix("#C79A6B", "#F8FAFC", k), mix("#8A6440", "#94A3B8", k)]))
        c.drawPath(foil_path(k), P("#0F172A", 0.5, stroke=4))
        if lift > 0:
            arrow(c, 0, -60, 0, -60 - 330 * e_back(lift), HILITE, lift, w=26, head=60)
            add_glow(c, 0, -300, 160, HILITE, 0.3 * lift)
        if k < 0.5:
            push = prog(t, s("fix1") - 0.12, s("fix1") + 0.2) * (1 - k * 2)
            for yy in (-150, 0, 150):
                arrow(c, -330, yy, -60, yy, WARN, push * 0.85, w=14, head=36)
        c.restore()

    def ui_foil(self, c, t, tw):
        T = self.T
        self.chip(540, 1120, "wing", T["airplane"] - 0.1, T["back1"], accent=GOOD, size=38)
        k = self.span(T["foil1"], T["back1"] + 0.2, 0.25, 0.1)
        if k > 0:
            v2.chip(c, 760, 380, self.L["lift"], k, accent=HILITE, size=46)
        v2.chip(c, 200, 470, self.L["wind"], self.span(self.tl.s("fix1") - 0.1, T["back1"] + 0.2), accent="#BFDBFE", size=36)

    # ------------------------------------------------------------------ set: seen from above (break2, fix2)
    def draw_top(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1E3524", "#18301F", "#112218"])
        rng = random.Random(4)
        for i in range(14):                                            # fields far below
            x, y = rng.uniform(-100, W), rng.uniform(-100, H)
            c.drawRRect(rr(x, y, rng.uniform(160, 380), rng.uniform(120, 300), 18), P(rng.choice(("#24412A", "#2B4626", "#33492B")), 0.5))
        for i in range(6):
            y = 200 + i * 300
            c.drawLine(0, y, W, y + 120, P("#3B5B3A", 0.35, stroke=10))
        wd = math.radians(self.wdir.at(t))
        dx, dy = math.cos(wd), math.sin(wd)
        cx, cy = 540, 820
        # wind arrows streaming across
        for i in range(36):
            r1 = random.Random(100 + i)
            off = r1.uniform(-900, 900)
            ph = (t * 0.55 + r1.uniform(0, 1)) % 1.0
            d = -900 + ph * 1800
            px, py = cx + dx * d - dy * off, cy + dy * d + dx * off
            arrow(c, px - dx * 80, py - dy * 80, px + dx * 50, py + dy * 50, "#E0F2FE", 0.8 * math.sin(ph * math.pi), w=9, head=26)
        yaw = math.radians(self.yaw.at(t))
        fx_, fy_ = math.cos(yaw), math.sin(yaw)
        mis = abs(((self.yaw.at(t) - (self.wdir.at(t) + 180) + 540) % 360) - 180)
        bad = clamp((mis - 15) / 30.0)
        contact_shadow(c, cx + 30, cy + 40, 240, 0.4)
        c.drawCircle(cx, cy, 52, P("#94A3B8"))
        # yaw ring with its motors
        spinning = 1.0 if T["yaw"] - 0.2 <= t < T["into"] + 0.4 else 0.0
        for i in range(8):
            a = i * math.pi / 4
            mx, my = cx + math.cos(a) * 92, cy + math.sin(a) * 92
            c.drawCircle(mx, my, 16, P("#475569"))
            c.save()
            c.translate(mx, my)
            c.rotate(t * 720 * spinning)
            c.drawLine(-12, 0, 12, 0, P("#FACC15" if spinning else "#94A3B8", 1, stroke=4))
            c.restore()
        c.save()
        c.translate(cx, cy)
        c.rotate(math.degrees(yaw))
        c.drawRRect(rr(-150, -56, 300, 112, 44), lin_paint(0, -56, 0, 56, ["#F8FAFC", "#CBD5E1", "#94A3B8"]))
        c.drawRRect(rr(-150, -56, 300, 112, 44), P("#0F172A", 0.35, stroke=4))
        c.drawCircle(196, 0, 50, rad_paint(186, -12, 70, ["#FFFFFF", "#CBD5E1", "#64748B"]))
        rot = mix("#F8FAFC", WARN, bad)
        c.drawRRect(rr(214, -540, 16, 1080, 8), P(rot, 0.18))             # the spinning rotor seen from above
        ra = self.rotor_ang(t)
        for i in range(3):
            ln = 520 * math.sin(math.radians(ra + i * 120))
            bp = skia.Path()
            bp.moveTo(206, -30 * (1 if ln > 0 else -1))
            bp.lineTo(222, -ln)
            bp.lineTo(234, -30 * (1 if ln > 0 else -1))
            bp.close()
            c.drawPath(bp, P(rot, 0.95))
        c.restore()
        # the wind vane on the back of the nacelle
        vx, vy = cx - fx_ * 110, cy - fy_ * 110
        va = math.radians(self.vane.at(t) if t >= T["vane"] - 0.1 else math.degrees(yaw) + 180)
        c.drawCircle(vx, vy, 10, P("#0F172A"))
        arrow(c, vx - math.cos(va) * 50, vy - math.sin(va) * 50, vx + math.cos(va) * 50, vy + math.sin(va) * 50,
              HILITE if t >= T["vane"] - 0.1 else "#CBD5E1", 1.0, w=10, head=26)
        self.ui["vane"] = (vx, vy)
        self.ui["rotor"] = (cx + fx_ * 230, cy + fy_ * 230)
        self.ui["bad"] = bad

    def ui_top(self, c, t, tw):
        T, s = self.T, self.tl.s
        rx, ry = self.ui.get("rotor", (700, 800))
        if tw < s("fix2") - 0.12:
            v2.chip(c, 200, 470, self.L["wind"], self.span(s("break2"), s("fix2") - 0.1), accent="#BFDBFE", size=36)
            self.chip(540, 470, "wrong", T["wrong"] - 0.1, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["wrong"] + 0.1, s("fix2") - 0.2, x=880, y=330)
            self.red(T["wrong"] + 0.1, 1.6)
            return
        vx, vy = self.ui.get("vane", (400, 800))
        self.label(vx, vy, 270, 1110, "vane", T["vane"] - 0.1, T["yaw"] + 0.3, HILITE, size=34)
        self.label(540 + 92, 820, 800, 1110, "motors", T["motors"] - 0.1, T["into"], "#FACC15", size=34)
        self.chip(540, 470, "head", T["head"] - 0.1, s("break3") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["into"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: inside the nacelle (break3, fix3)
    def draw_gear(self, c, t):
        vrect(c, 0, 0, W, H, ["#0B1226", "#121A33", "#0A0F1F"])
        c.drawRRect(rr(60, 520, 960, 640, 120), P("#1E293B"))
        c.drawRRect(rr(60, 520, 960, 640, 120), P("#475569", 1, stroke=8))
        g = self.gbox.at(t)
        ang = self.rotor_ang(t) * 0.35
        c.save()                                                   # the hub with the blade roots, at the left
        c.translate(190, 840)
        c.rotate(ang)
        for i in range(3):
            c.save()
            c.rotate(i * 120)
            c.drawRRect(rr(-26, -200, 52, 130, 20), P("#E2E8F0"))
            c.restore()
        c.restore()
        c.drawCircle(190, 840, 86, rad_paint(170, 820, 110, ["#FFFFFF", "#CBD5E1", "#64748B"]))
        x_end = lerp(690, 500, clamp(g * 3))                       # the slow main shaft
        c.drawRRect(rr(270, 818, x_end - 270, 44, 10), lin_paint(0, 818, 0, 862, ["#CBD5E1", "#64748B"]))
        for i in range(5):
            xx = 280 + ((ang * 2 + i * 60) % max(60.0, x_end - 290))
            c.drawLine(xx, 822, xx, 858, P("#334155", 0.6, stroke=4))
        gx, gy_ = 830, 840                                         # the generator, at the right
        c.drawRRect(rr(gx - 140, gy_ - 150, 280, 300, 40), lin_paint(gx - 140, 0, gx + 140, 0, ["#334155", "#475569", "#1E293B"]))
        gr = ang if g <= 0 else ang * (1 + 40 * g)
        c.save()
        c.clipRRect(rr(gx - 120, gy_ - 130, 240, 260, 30))
        for i in range(10):
            yy = gy_ - 130 + ((gr * 2 + i * 26) % 260)
            c.drawLine(gx - 120, yy, gx + 120, yy, P("#B45309", 0.8, stroke=8))
        c.restore()
        if g > 0:
            add_glow(c, gx, gy_, 220, "#FACC15", 0.45 * g)
            bolt = skia.Path()
            bolt.moveTo(gx + 10, gy_ - 70)
            bolt.lineTo(gx - 30, gy_ + 10)
            bolt.lineTo(gx, gy_ + 10)
            bolt.lineTo(gx - 16, gy_ + 80)
            bolt.lineTo(gx + 34, gy_ - 10)
            bolt.lineTo(gx + 4, gy_ - 10)
            bolt.close()
            c.drawPath(bolt, P(HILITE, g))
            kk = e_back(g)
            c.save()
            c.translate(560, 840)
            c.scale(kk, kk)
            c.translate(-560, -840)
            c.drawRRect(rr(330, 640, 420, 400, 40), P("#0F172A", 0.8))
            c.drawRRect(rr(330, 640, 420, 400, 40), P(HILITE, 0.7, stroke=5))
            gear(c, 500, 840, 140, 28, ang, "#94A3B8")
            gear(c, 678, 840, 34, 7, -ang * 140 / 34.0 + 12, "#FACC15")
            c.drawRRect(rr(678, 822, 14, 36, 6), P("#64748B"))
            c.restore()
        self.ui["gen"] = (gx, gy_ - 150)
        self.ui["shaft"] = (360, 818)

    def ui_gear(self, c, t, tw):
        T, s = self.T, self.tl.s
        sx, sy = self.ui.get("shaft", (330, 818))
        gx, gy = self.ui.get("gen", (820, 690))
        if tw < s("fix3") - 0.12:
            self.label(sx, sy, 300, 1240 - 100, "rpm10", T["ten"] - 0.1, s("fix3") - 0.15, "#CBD5E1", size=32)
            self.label(gx, gy, 760, 430 + 30, "need", T["generator"] - 0.1, s("fix3") - 0.15, WARN, size=32)
            self.badge("alert", T["thousand"] + 0.1, s("fix3") - 0.2, x=880, y=330)
            self.red(T["thousand"] + 0.1, 1.6)
            return
        self.label(560, 640, 300, 460, "gearbox", T["bx"] + 0.2, s("break4") - 0.15, HILITE, size=36)
        self.chip(560, 1110, "x100", T["multiplies"] - 0.1, s("break4") - 0.15, accent=HILITE, size=48)
        self.label(gx, gy, 780, 460, "fast", T["hundred"] - 0.1, s("break4") - 0.15, GOOD, size=32)
        self.badge("check", T["hundred"] + 0.1, s("break4") - 0.15, x=880, y=330)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (0.1, sfx.whirr(2.4, 60.0, 90.0, 61), -16),
              (T["sky0"], sfx.riser(1.0), -14), (T["days1"], sfx.ding(), -8), (T["days1"] + 0.05, sfx.sparkle(0.6, 9, 62), -12),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 63), -9), (T["wind"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 64), -4), (T["pushes"], sfx.thud(0.4), -10),
               (T["slow"], sfx.creak(1.0), -12), (T["slow"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 65), -5), (T["shape"], sfx.whirr(0.8, 140.0, 260.0, 66), -12),
               (T["foil1"], sfx.riser(0.6), -10), (T["back1"], sfx.whoosh(0.5, True, 67), -6), (T["back1"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["wd"], sfx.hiss(1.2, 69), -12),
               (T["wrong"] + 0.15, sfx.alarm(3, 820.0), -12)]
        ev += [(T["vane"], sfx.click(70), -8), (T["yaw"], sfx.whirr(1.4, 180.0, 260.0, 71), -10), (T["into"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["ten"], sfx.hum(1.6, 60.0), -12),
               (T["thousand"] + 0.15, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 73), -5), (T["bx"], sfx.clank(), -8),
               (T["multiplies"], sfx.whirr(1.6, 200.0, 900.0, 74), -10), (T["hundred"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 75), -4), (T["storm"] - 0.1, boom(1.6, 76), -6),
               (T["fast"], sfx.whirr(2.0, 300.0, 600.0, 77), -10), (T["tear"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["tw"], sfx.whirr(1.0, 300.0, 120.0, 78), -10), (T["brake"], sfx.thunk(79), -6),
               (T["passes"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(80), 0), (T["follow"] - 0.15, sfx.pop(81), -4)]
        ev += [(T["paint0"], sfx.hiss(0.8, 82), -12), (T["birds"], sfx.whoosh(0.6, False, 83), -10),
               (T["wide"], sfx.riser(1.2), -12)]
        ev += [(T["s1"], sfx.pop(84), -3), (T["s2"], sfx.pop(85), -3), (T["s3"], sfx.pop(86), -3)]
        ev += [(T["cong2"], sfx.pop(87), -2), (T["cong2"], sfx.sparkle(1.0, 14, 88), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 89), -6)]
        if self.rtl:
            ev += [(T["fan2"], sfx.click(90), -6)]
        else:
            ev += [(T["comment"], sfx.pop(90), -8), (T["fan2"], sfx.whirr(1.2, 120.0, 180.0, 91), -14)]
        return ev


NAME = "turbine"
EPISODE = Turbine
