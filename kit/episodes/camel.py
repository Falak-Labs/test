"""Episode 33 - A robot camel jockey.  v2 look: a desert racetrack at sunset, side view; the world scrolls past the
running camel while its owner chases it in an SUV on the road behind the rail.

Sets: track (the race: camel, robot on the hump, the SUV behind; the robot that just sits, the drill that spins a
plastic whip; the owner's voice through a walkie-talkie and a speaker by the camel's ear; the first robots that scared
the camels, then a little face, sunglasses, racing silks and perfume; the line-up and the start; the stat and the
closer), scale (a dial scale: the first robot weighs as much as a suitcase; strip it down to a drill, a battery and a
radio, about two kilos), road (the tag: the SUVs racing on the road beside the track).
World (track): the ground is y = 0; the camel runs to the right and stays near x = 0 while the ground scrolls.
"""
from v2_base import *  # noqa: F401,F403

SANDS = ("#A8693A", "#8A552C", "#5E391D", "#2E1C0E")
DUSKY = {"top": "#07071F", "upper": "#1E1650", "mid": "#5E2E68", "low": "#C9604A", "horizon": "#F49A5C",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
CAMEL = "#EBC38D"
SILKS = ("#E11D48", "#2563EB", "#16A34A", "#F59E0B", "#7C3AED")


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


class Run:
    """Distance (world units) from a Track of speed (units per second), integrated."""

    def __init__(self, track, t_end, dt=1 / 60.0):
        n = int(t_end / dt) + 3
        self.dt = dt
        self.d = np.zeros(n)
        acc = 0.0
        for i in range(1, n):
            acc += track.at((i - 0.5) * dt) * dt
            self.d[i] = acc

    def at(self, t):
        i = clamp(t / self.dt, 0, len(self.d) - 2.001)
        i0 = int(i)
        return float(self.d[i0] + (self.d[i0 + 1] - self.d[i0]) * (i - i0))


def _leg(c, hx, hy, a1, a2, col, w=24):
    """Two-segment leg from the hip (hx, hy): angles in degrees from straight down."""
    x1 = hx + math.sin(math.radians(a1)) * 120
    y1 = hy + math.cos(math.radians(a1)) * 120
    x2 = x1 + math.sin(math.radians(a1 + a2)) * 125
    y2 = y1 + math.cos(math.radians(a1 + a2)) * 125
    c.drawLine(hx, hy, x1, y1, P("#4A2C14", 0.55, stroke=w * 1.5 + 6))
    c.drawLine(x1, y1, x2, y2, P("#4A2C14", 0.55, stroke=w + 6))
    c.drawLine(hx, hy, x1, y1, P(col, 1, stroke=w * 1.5))
    c.drawLine(x1, y1, x2, y2, P(col, 1, stroke=w))
    c.drawCircle(x1, y1, w * 0.62, P(shade(col, -0.08)))
    c.drawOval(R(x2 - 20, y2 - 9, 44, 18), P(shade(col, -0.45)))


def camel(c, x, y, s, ph, run=1.0, scared=0.0, ear=0.0, col=CAMEL, a=1.0):
    """Side view, facing right, feet on (x, y), scale s.  ph = gait phase (radians), run 0..1 (0 = standing)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    rear = scared * 14
    c.rotate(-rear)
    bob = -abs(math.sin(ph)) * 16 * run
    c.translate(0, bob)
    far = shade(col, -0.32)
    legs = ((-120, 0.4, far), (95, math.pi + 0.4, far), (-120, 0.0, col), (95, math.pi, col))
    for i, (hx, o, lc) in enumerate(legs):
        if i == 2:                                             # body between the far and the near legs
            _body(c, col, ear, scared)
        sw = math.sin(ph + o) * run
        a1 = (6 + 28 * sw) * (1 if hx > 0 else 0.9)
        a2 = -(8 + 40 * max(0.0, math.sin(ph + o + 1.3))) * run - (0 if run > 0.2 else 4)
        if hx > 0:
            a2 = -a2 * 0.8
        _leg(c, hx, -235, a1 - scared * (20 if hx > 0 else 0), a2, lc)
    if a < 1:
        c.restore()
    c.restore()


def _body(c, col, ear, scared):
    p = skia.Path()
    p.moveTo(-170, -235)
    p.cubicTo(-195, -330, -110, -360, -50, -385)
    p.cubicTo(-10, -480, 75, -455, 95, -370)
    p.cubicTo(125, -335, 165, -330, 172, -285)
    p.cubicTo(182, -205, 125, -175, 60, -180)
    p.cubicTo(0, -172, -85, -168, -135, -182)
    p.cubicTo(-178, -192, -186, -212, -170, -235)
    p.close()
    c.drawPath(p, lin_paint(0, -470, 0, -170, [shade(col, 0.18), col, shade(col, -0.22)]))
    c.drawPath(p, P("#4A2C14", 0.6, stroke=5))
    tail = skia.Path()
    tail.moveTo(-172, -240)
    tail.quadTo(-205, -200, -196, -150)
    c.drawPath(tail, P(shade(col, -0.3), 1, stroke=10))
    nk = skia.Path()                                          # the neck, curving forward and up
    nk.moveTo(135, -340)
    nk.cubicTo(215, -320, 245, -380, 262, -455)
    nk.lineTo(312, -462)
    nk.cubicTo(292, -370, 245, -255, 160, -250)
    nk.close()
    c.drawPath(nk, lin_paint(140, 0, 310, 0, [col, shade(col, 0.1)]))
    c.drawPath(nk, P("#4A2C14", 0.5, stroke=4))
    c.save()
    c.translate(318, -478)
    c.rotate(12 - scared * 18)
    c.drawOval(R(-38, -26, 96, 50), P(shade(col, 0.08)))
    c.drawOval(R(30, -16, 44, 32), P(shade(col, -0.05)))
    c.drawCircle(64, -6, 4, P("#3B2414"))
    c.drawLine(40, 14, 66, 12, P("#3B2414", 0.7, stroke=3))
    er = -40 - ear * 25 - scared * 20
    ep = skia.Path()
    ep.moveTo(-20, -18)
    ep.lineTo(-30 + math.sin(math.radians(er)) * 4, -42)
    ep.lineTo(-8, -22)
    ep.close()
    c.drawPath(ep, P(shade(col, -0.2)))
    eye_r = 7 + scared * 6
    c.drawCircle(14, -8, eye_r, P("#FFFFFF" if scared > 0.2 else "#2B1A0E"))
    if scared > 0.2:
        c.drawCircle(16, -8, 4, P("#2B1A0E"))
    c.restore()


def drill(c, x, y, s, spin, a=1.0, whip=1.0):
    """A cordless drill pointing back, with a plastic whip in its chuck (spin in degrees)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-10, -14, 70, 28, 10), P("#F59E0B", a))
    c.drawRRect(rr(14, 6, 22, 44, 8), P("#111827", a))
    c.drawRRect(rr(6, 46, 38, 18, 6), P("#F59E0B", a))
    c.drawRRect(rr(-26, -8, 18, 16, 4), P("#374151", a))
    if whip > 0:
        c.save()
        c.translate(-26, 0)
        c.rotate(spin)
        c.drawLine(0, 0, -120, 30, P("#E5E7EB", a * whip, stroke=5))
        c.drawRRect(rr(-136, 22, 24, 16, 6), P("#EF4444", a * whip))
        c.restore()
    c.restore()


def robot_new(c, x, y, s, t, spin=0.0, whip=1.0, face=0.0, silk=0.0, silk_col="#E11D48", speaker=0.0, a=1.0, glow=0.0):
    """The modern jockey on the hump: a small frame with a battery, a radio and a drill.  face/silk/speaker 0..1."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-60, -16, 120, 26, 10), P("#7F1D1D", a))               # saddle pad
    c.drawRRect(rr(-36, -70, 70, 56, 8), P("#334155", a))                 # battery + radio box
    c.drawRRect(rr(-28, -62, 30, 40, 4), P("#22C55E", a))
    c.drawLine(24, -70, 34, -150, P("#CBD5E1", a, stroke=4))               # antenna
    c.drawCircle(34, -152, 6, P(WARN, a))
    if silk > 0:                                                           # racing silks over the box
        k = e_back(clamp(silk))
        c.save()
        c.scale(k, k)
        sp = skia.Path()
        sp.moveTo(-44, -18)
        sp.lineTo(-40, -86)
        sp.quadTo(0, -100, 40, -86)
        sp.lineTo(44, -18)
        sp.close()
        c.drawPath(sp, lin_paint(-44, 0, 44, 0, [shade(silk_col, 0.2), silk_col, shade(silk_col, -0.25)], a=a))
        c.drawRect(R(-40, -62, 80, 12), P("#FFFFFF", 0.85 * a))
        c.restore()
    if face > 0:                                                           # a little mannequin face with sunglasses
        k = e_back(clamp(face))
        c.save()
        c.translate(-4, -118)
        c.scale(k, k)
        c.drawCircle(0, 0, 26, P("#E8B48A", a))
        c.drawPath(_cap(), P(silk_col, a))
        c.drawRRect(rr(-4, -6, 30, 12, 5), P("#0F172A", a))
        c.drawLine(4, 12, 18, 12, P("#7C2D12", a, stroke=3))
        c.restore()
    if speaker > 0:
        k = e_back(clamp(speaker))
        c.save()
        c.translate(52, -44)
        c.scale(k, k)
        c.drawRRect(rr(-14, -18, 28, 36, 6), P("#111827", a))
        c.drawCircle(0, 0, 10, P("#475569", a))
        c.restore()
    drill(c, 30, -30, 0.9, spin, a, whip)
    if glow > 0:
        add_glow(c, 0, -60, 120, HILITE, 0.4 * glow * a)
    c.restore()


def _cap():
    p = skia.Path()
    p.moveTo(-27, -4)
    p.cubicTo(-27, -40, 27, -40, 27, -4)
    p.lineTo(40, -2)
    p.lineTo(27, 4)
    p.close()
    return p


def robot_old(c, x, y, s, a=1.0):
    """The first robot jockey: a boxy grey humanoid about as heavy as a suitcase."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-50, -20, 100, 30, 8), P("#7F1D1D", a))
    c.drawRRect(rr(-42, -150, 84, 132, 14), lin_paint(-42, 0, 42, 0, ["#9CA3AF", "#D1D5DB", "#6B7280"], a=a))
    c.drawRRect(rr(-30, -215, 60, 58, 12), P("#9CA3AF", a))
    c.drawRect(R(-18, -196, 36, 12), P("#111827", a))
    for sd in (-1, 1):
        c.drawLine(sd * 42, -130, sd * 70 + 40, -80, P("#6B7280", a, stroke=16))
    c.drawLine(0, -215, 0, -250, P("#CBD5E1", a, stroke=4))
    c.restore()


def suv(c, x, y, s, t, owner=1.0, yell=0.0, radio=0.0, col="#F8FAFC", a=1.0, honk=0.0):
    """Side view SUV facing right on (x, y), the owner at the open window with a walkie-talkie."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(-230, -40)
    body.lineTo(-230, -150)
    body.lineTo(-150, -160)
    body.lineTo(-120, -250)
    body.lineTo(120, -250)
    body.lineTo(170, -160)
    body.lineTo(240, -140)
    body.lineTo(250, -50)
    body.close()
    c.drawPath(body, lin_paint(0, -250, 0, -40, [shade(col, 0.1), col, shade(col, -0.25)], a=a))
    c.drawRect(R(-110, -236, 100, 72), P("#1E293B", a))
    c.drawRect(R(0, -236, 110, 72), P("#0F172A", a))                     # the open window
    if owner > 0:
        c.drawCircle(60, -190, 26, P("#C68B5E", a))
        gh = skia.Path()                                                     # white ghutra and black agal
        gh.moveTo(30, -186)
        gh.cubicTo(28, -232, 92, -232, 90, -186)
        gh.lineTo(96, -150)
        gh.lineTo(26, -150)
        gh.close()
        c.drawPath(gh, P("#F8FAFC", a))
        c.drawCircle(60, -190, 22, P("#C68B5E", a))
        c.drawRRect(rr(32, -222, 56, 8, 4), P("#111827", a))
        mo = 4 + 8 * yell * abs(math.sin(t * 14))
        c.drawOval(R(70, -184, 14, mo), P("#4A1D0F", a))
        if radio > 0:
            c.drawRRect(rr(86, -206, 18, 40, 4), P("#111827", a))
            c.drawLine(98, -206, 98, -232, P("#111827", a, stroke=4))
    for wx in (-140, 150):
        c.drawCircle(wx, -40, 48, P("#111827", a))
        c.drawCircle(wx, -40, 24, P("#9CA3AF", a))
        c.save()
        c.translate(wx, -40)
        c.rotate(t * 900)
        c.drawLine(-20, 0, 20, 0, P("#4B5563", a, stroke=6))
        c.restore()
    c.drawRect(R(236, -120, 16, 24), P("#FDE68A", a))
    if honk > 0:
        word(c, "BEEP!", 250, -300, 70, HILITE, honk * a)
    c.restore()


def scale_dial(c, x, y, kg, a=1.0):
    """A big dial scale: platform top at y, dial below; kg 0..30."""
    c.drawRRect(rr(x - 300, y, 600, 60, 20), lin_paint(0, y, 0, y + 60, ["#E2E8F0", "#94A3B8"], a=a))
    c.drawRRect(rr(x - 260, y + 60, 520, 120, 20), P("#334155", a))
    dx, dy = x, y + 120
    c.drawCircle(dx, dy, 92, P("#F8FAFC", a))
    c.drawCircle(dx, dy, 92, P("#0F172A", a, stroke=6))
    for i in range(7):
        an = math.radians(-210 + i * 40)
        c.drawLine(dx + math.cos(an) * 70, dy + math.sin(an) * 70, dx + math.cos(an) * 84, dy + math.sin(an) * 84,
                   P("#0F172A", a, stroke=4))
    an = math.radians(-210 + clamp(kg / 30.0) * 240)
    c.drawLine(dx, dy, dx + math.cos(an) * 74, dy + math.sin(an) * 74, P(WARN, a, stroke=8))
    c.drawCircle(dx, dy, 10, P("#0F172A", a))
    text(c, f"{kg:.0f} kg", dx, dy + 46, 34, "#0F172A", "Poppins-Black", a=a)


def suitcase(c, x, y, s, a=1.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-80, -150, 160, 150, 18), lin_paint(-80, 0, 80, 0, ["#1D4ED8", "#3B82F6", "#1E3A8A"], a=a))
    c.drawRRect(rr(-30, -178, 60, 30, 10), P("#1E293B", a, stroke=10))
    for xx in (-40, 40):
        c.drawLine(xx, -140, xx, -10, P("#1E3A8A", a, stroke=8))
    c.restore()


def keyfob(c, x, y, press, a=1.0):
    """A hand-held remote with one big button (screen space)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    k = e_back(clamp(a * 1.2))
    c.scale(k, k)
    c.drawRRect(rr(-60, -100, 120, 200, 40), P("#000000", 0.35 * a, blur=12))
    c.drawRRect(rr(-60, -100, 120, 200, 40), P("#1F2937", a))
    c.drawCircle(0, -20, 38 - press * 6, P(mix("#DC2626", "#F87171", press), a))
    if press > 0.5:
        add_glow(c, 0, -20, 80, WARN, 0.5 * a)
    c.drawRRect(rr(-28, 40, 56, 14, 7), P("#4B5563", a))
    c.restore()


# ====================================================================================== the episode
class Camel(EpisodeV2):
    BUILD_NO = 33
    COVER_T = ("closer", 0.55)
    FIRST_SET = "track"
    CLEAR = "#14123A"
    TITLE = {"en": "ROBOT CAMEL JOCKEY", "ar_sa": "روبوت سباق الهجن"}
    EMPH = {"en": ["CONGRATS", "ROBOT", "RIDES", "RACING", "CAMEL", "SIXTY", "KILOMETERS", "OWNER", "YELLS", "CAR",
                   "JOCKEY", "LIGHTER", "RIDERS", "SUITCASE", "STRIP", "CORDLESS", "DRILL", "BATTERY", "RADIO", "TWO",
                   "KILOS", "SITS", "SPEED", "SPINS", "PLASTIC", "WHIP", "BUTTON", "ONE", "VOICE", "OWNER'S", "TRACK",
                   "SPEAKER", "EAR", "SHOUTS", "WALKIE-TALKIE", "SCARED", "FACE", "SUNGLASSES", "SILKS", "PERFUME",
                   "FOLLOW", "ELECTRIC", "LINE", "CHASES", "SUV", "ROAD", "SIXTY-FIVE", "MILLION", "DIRHAMS",
                   "YOURSELF", "SCARIEST", "SUVS"],
            "ar_sa": ["مبروك", "روبوت", "بيركب", "جمل", "بستين", "وصاحبه", "بيزعقله", "العربية", "الهجن", "أسرع",
                      "خفيف", "تقيل", "شنطة", "فتشيل", "شنيور", "وبطارية", "ولاسلكي", "اتنين", "كيلو", "ساكت",
                      "يسرع", "كرباج", "بلاستيك", "بزرار", "صوت", "صاحبه", "الحلبة", "سماعة", "ودن", "يزعق",
                      "اللاسلكي", "خضت", "غريب", "وش", "ونضارة", "وهدوم", "برفان", "تابعني", "كهربا", "صفهم",
                      "جيب", "طريق", "وستين", "مليون", "درهم", "بإيدك", "الزحمة", "الدائري"]}
    KEYS = {"ar_sa": {
        ("hook", "ROBOT"): "روبوت", ("hook", "RIDES"): "بيركب", ("hook", "CAMEL"): "جمل", ("hook", "SIXTY"): "بستين",
        ("hook", "OWNER"): "وصاحبه", ("hook", "YELLS"): "بيزعقله", ("hook", "CAR"): "العربية",
        ("hook", "CONGRATS"): "مبروك", ("hook", "JOCKEY"): "الهجن",
        ("break1", "FASTER"): "اسرع", ("break1", "LIGHTER"): "خفيف", ("break1", "FIRST"): "اول",
        ("break1", "SUITCASE"): "شنطة",
        ("fix1", "STRIP"): "فتشيل", ("fix1", "DRILL"): "شنيور", ("fix1", "BATTERY"): "وبطارية",
        ("fix1", "RADIO"): "ولاسلكي", ("fix1", "KILOS"): "كيلو",
        ("break2", "SITS"): "ساكت", ("break2", "SPEED"): "يسرع",
        ("fix2", "SPINS"): "يلف", ("fix2", "WHIP"): "كرباج", ("fix2", "BUTTON"): "بزرار",
        ("break3", "VOICE"): "صوت", ("break3", "OWNER"): "صاحبه", ("break3", "TRACK"): "الحلبة",
        ("fix3", "SPEAKER"): "سماعة", ("fix3", "EAR"): "ودن", ("fix3", "SHOUTS"): "يزعق", ("fix3", "WALKIE"): "اللاسلكي",
        ("break4", "SCARED"): "خضت", ("break4", "NOTHING"): "غريب",
        ("fix4", "FACE"): "وش", ("fix4", "SUNGLASSES"): "ونضارة", ("fix4", "SILKS"): "وهدوم", ("fix4", "PERFUME"): "برفان",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "LINE"): "صفهم", ("reveal", "CHASES"): "يجري", ("reveal", "SUV"): "جيب", ("reveal", "ROAD"): "طريق",
        ("stat", "SIXTY"): "خمسة", ("stat", "ROBOTS"): "روبوت", ("stat", "CAMELS"): "وجمل",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SCARIEST"): "الزحمة", ("tag", "TRACK"): "السباق", ("tag", "SUVS"): "الطريق", ("tag", "NEXT"): "الدائري"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an electric car"),
                   "stat": [("65 km/h", "TOP SPEED"), ("2 kg", "ROBOT"), ("1,000,000+", "DIRHAMS A CAMEL")],
                   "L": {"robot": "YOUR ROBOT JOCKEY", "owner": "THE OWNER, IN A CAR", "jockey": "ROBOT CAMEL JOCKEY",
                         "lighter": "LIGHTER RIDER = FASTER", "suitcase": "= A SUITCASE", "drill": "CORDLESS DRILL",
                         "battery": "BATTERY", "radio": "RADIO", "kilos": "ABOUT 2 kg", "sits": "IT JUST SITS THERE",
                         "slow": "SLOWING DOWN", "whip": "PLASTIC WHIP", "button": "PRESS", "voice": "ONLY THE OWNER'S VOICE",
                         "where": "OWNER: NOT ON THE TRACK", "speaker": "SPEAKER BY THE EAR", "yalla": "YALLA! YALLA!",
                         "scared": "SCARED!", "face": "LITTLE FACE", "glasses": "SUNGLASSES", "silks": "RACING SILKS",
                         "perfume": "JOCKEYS' PERFUME", "line": "LINE THEM UP", "chase": "OWNERS CHASE IN SUVS",
                         "real": "THE REAL RACE", "kmh": "km/h"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: عربية كهربا"),
                      "stat": [("65 كم/س", "أقصى سرعة"), ("2 كيلو", "الروبوت"), ("+1,000,000", "درهم تمن الجمل")],
                      "L": {"robot": "الروبوت بتاعك", "owner": "صاحبه في العربية", "jockey": "روبوت سباق الهجن",
                            "lighter": "أخف = أسرع", "suitcase": "= شنطة سفر", "drill": "شنيور", "battery": "بطارية",
                            "radio": "لاسلكي", "kilos": "حوالي 2 كيلو", "sits": "قاعد ساكت", "slow": "بيهدّي",
                            "whip": "كرباج بلاستيك", "button": "زرار", "voice": "صوت صاحبه بس",
                            "where": "صاحبه مش في الحلبة", "speaker": "سماعة جنب ودنه", "yalla": "يلا! يلا!",
                            "scared": "اتخض!", "face": "وش صغير", "glasses": "نضارة شمس", "silks": "هدوم سباق",
                            "perfume": "برفان الجوكية", "line": "صفّهم", "chase": "أصحابهم وراهم بالجيب",
                            "real": "الدائري الساعة خمسة", "kmh": "كم/س"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "robot": ("hook", "ROBOT", 0.05), "rides": ("hook", "RIDES", 0.12), "camel": ("hook", "CAMEL", 0.25),
            "sixty": ("hook", "SIXTY", 0.33), "owner": ("hook", "OWNER", 0.5), "yells": ("hook", "YELLS", 0.58),
            "car": ("hook", "CAR", 0.65), "congrats": ("hook", "CONGRATS", 0.72), "jockey": ("hook", "JOCKEY", 0.95),
            "faster": ("break1", "FASTER", 0.15), "lighter": ("break1", "LIGHTER", 0.3), "first": ("break1", "FIRST", 0.55),
            "suitcase": ("break1", "SUITCASE", 0.9),
            "strip": ("fix1", "STRIP", 0.1), "drill": ("fix1", "DRILL", 0.4), "battery": ("fix1", "BATTERY", 0.55),
            "radio": ("fix1", "RADIO", 0.7), "kilos": ("fix1", "KILOS", 0.95),
            "sits": ("break2", "SITS", 0.3), "speed": ("break2", "SPEED", 0.9),
            "spins": ("fix2", "SPINS", 0.2), "whip": ("fix2", "WHIP", 0.5), "button": ("fix2", "BUTTON", 0.9),
            "voice": ("break3", "VOICE", 0.2), "owner3": ("break3", "OWNER", 0.4), "track": ("break3", "TRACK", 0.9),
            "speaker": ("fix3", "SPEAKER", 0.15), "ear": ("fix3", "EAR", 0.35), "shouts": ("fix3", "SHOUTS", 0.65),
            "walkie": ("fix3", "WALKIE", 0.85),
            "scared": ("break4", "SCARED", 0.3), "nothing": ("break4", "NOTHING", 0.8),
            "face": ("fix4", "FACE", 0.15), "glasses": ("fix4", "SUNGLASSES", 0.3), "silks": ("fix4", "SILKS", 0.55),
            "perfume": ("fix4", "PERFUME", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "line": ("reveal", "LINE", 0.15), "chases": ("reveal", "CHASES", 0.45), "suv": ("reveal", "SUV", 0.65),
            "road": ("reveal", "ROAD", 0.85),
            "s1": ("stat", "SIXTY", 0.04), "s2": ("stat", "ROBOTS", 0.4), "s3": ("stat", "CAMELS", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "scariest": ("tag", "SCARIEST", 0.1), "ttrack": ("tag", "TRACK", 0.35), "suvs": ("tag", "SUVS", 0.65),
            "next": ("tag", "NEXT", 0.85)})
        T["strip0"] = min(T["strip"], T["drill"]) - 0.15
        T["press"] = max(T["button"] - 0.1, T["whip"] + 0.4)
        T["sp0"] = min(T["speaker"], T["ear"]) - 0.1
        T["yell3"] = min(T["shouts"], T["walkie"]) - 0.1
        T["go"] = max(T["chases"] - 0.3, T["line"] + 0.8)                    # reveal: the gate opens
        T["jam"] = max(T["suvs"] - 0.2, T["ttrack"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "scale", 1)
        self.cut(s("break2") - 0.12, "track", -1)
        self.cut(s("tag") - 0.2, "road", 1)
        # ---- cameras (track world: camel at x ~ 0, ground y = 0)
        cm = Camera(80, -232, 1.25)
        cm.key(0.05, 70, -228, 1.22, 1.0).key(T["owner"] - 0.4, -150, -250, 0.95, 1.0)
        cm.key(T["jockey"] - 0.5, 20, -250, 1.05, 1.0)
        cm.key(s("break2") - 0.12, 60, -470, 1.6, 0.0).key(s("break2"), 50, -480, 1.62, 3.0)
        cm.key(s("break3") - 0.12, 230, -470, 1.5, 0.0).key(T["owner3"], -150, -330, 0.85, 1.0)
        cm.key(T["sp0"] - 0.1, 260, -480, 1.4, 0.6).key(T["yell3"], -100, -320, 0.85, 0.8)
        cm.key(s("break4") - 0.12, 60, -300, 1.25, 0.0).key(s("break4"), 70, -310, 1.28, 3.0)
        cm.key(s("cta") - 0.12, 0, -285, 0.95, 0.0)
        cm.key(s("reveal") - 0.12, 300, -260, 0.62, 0.0).key(T["go"], 340, -270, 0.6, 2.0)
        cm.key(s("stat") - 0.12, 120, -200, 0.62, 0.0).key(s("stat"), 140, -210, 0.64, 3.0)
        cm.key(s("closer") - 0.1, 60, -232, 1.2, 1.2)
        self.cam = cm
        # ---- tracks
        spd = Track(1500.0)
        spd.to(s("break2") - 0.12, 1300.0, 0.0).to(T["sits"] - 0.2, 420.0, 1.6)            # it just sits: the camel slows
        spd.to(T["spins"], 1500.0, 1.2)
        spd.to(s("break3") - 0.12, 1250.0, 0.0).to(T["track"] - 0.3, 700.0, 1.4)
        spd.to(T["yell3"], 1650.0, 1.2)
        spd.to(s("break4") - 0.12, 0.0, 0.0).to(s("cta") - 0.12, 0.0, 0.0)
        spd.to(T["go"], 1600.0, 1.4)
        spd.to(s("tag") - 0.2, 1500.0, 0.0)
        self.spd = spd
        self.run = Run(spd, self.duration + 1)
        self.whip_on = Track(0.0).to(T["spins"] - 0.15, 1.0, 0.3)
        self.spk = Track(0.0).to(T["sp0"], 1.0, 0.4)
        self.scare = Track(0.0).to(T["scared"] - 0.2, 1.0, 0.35).to(T["face"], 0.0, 0.8)
        self.kg = Track(25.0).to(T["strip0"] + 0.2, 2.0, max(0.8, T["kilos"] - T["strip0"]))
        self.spans = [(T["suitcase"], T["kilos"] + 0.3), (T["speed"], T["button"] + 0.3),
                      (T["track"], T["walkie"] + 0.3), (T["nothing"], T["perfume"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["suitcase"], 0.3, 6), (T["speed"], 0.3, 5), (T["track"], 0.3, 5),
                       (T["scared"], 0.5, 12), (T["go"], 0.4, 8), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(33)
        self.dunes = [(rng.uniform(0, 4000), rng.uniform(80, 220)) for _ in range(10)]

    # ------------------------------------------------------------------ helpers
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    def gait(self, t):
        return self.run.at(t) / 95.0

    def sky_and_dunes(self, c, t, cam, d):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSKY, horizon_y=gy - 140 * z)
        sx, sy = 860, gy - 520 * z - 200
        add_glow(c, sx, sy, 240, "#FF7A3D", 0.45)
        c.drawCircle(sx, sy, 70, P("#FFC98A", 0.95))
        for i, (dx, hgt) in enumerate(self.dunes):
            x = (dx - d * 0.05 - cx * 0.05) % 4000 - 1500
            c.drawOval(R(x, gy - 150 * z - hgt * 0.5, 900, hgt * 1.3), P(mix("#7A3E34", "#4E2A35", i % 2 * 0.5), 0.95))
        c.drawRect(R(0, gy - 150 * z + 40, W, 400), P("#6E3A2C", 0.95))
        return gy

    # ------------------------------------------------------------------ set: track
    def draw_track(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        self.ui["cam"] = cam
        d = self.run.at(t)
        ph = self.gait(t)
        sp = self.spd.at(t)
        runk = clamp(sp / 900.0)
        gy = self.sky_and_dunes(c, t, cam, d)
        self.view(c, cam)
        x0, x1 = cx - 620 / z, cx + 620 / z
        # the road behind the rail, with the owners' SUVs
        vrect(c, x0, -230, x1 - x0, 70, ["#3F3F46", "#27272A"])
        for k in range(int(x0 // 240) - 1, int(x1 // 240) + 2):
            xx = k * 240 - (d % 240)
            c.drawRect(R(xx, -200, 110, 8), P("#FDE68A", 0.8))
        in_reveal = s("reveal") - 0.12 <= t < s("closer") - 0.1
        yell = 1.0 if (t < s("break1") and T["yells"] - 0.1 <= t) or (T["yell3"] <= t < s("break4")) else 0.0
        radio = 1.0 if t >= T["yell3"] - 0.2 and t < s("break4") else 0.0
        if in_reveal:
            for i in range(4):
                lag = (i - 1.5) * 380 + (0 if t >= T["go"] else 600)
                suv(c, -420 + lag * 0.0 + i * 360 - (0 if t >= T["go"] else 900), -165, 0.62, t + i,
                    owner=1.0, yell=1.0 if t >= T["go"] else 0.0, radio=1.0, col=("#F8FAFC", "#E5E7EB", "#1F2937", "#B91C1C")[i])
        elif s("break4") - 0.12 <= t < s("cta") - 0.12:
            pass
        else:
            suv(c, -470, -165, 0.62, t, owner=1.0, yell=yell, radio=radio)
        if yell > 0 and not in_reveal:
            for i in range(3):
                ph_ = (t * 2.2 + i / 3.0) % 1.0
                c.drawArc(R(-470 + 60 - 40 * ph_ * 3, -300 - 40 * ph_ * 3, 80 * ph_ * 3 + 20, 80 * ph_ * 3 + 20), -60, 120, False,
                          P("#FDE68A", 0.8 * (1 - ph_), stroke=6))
        # the track: sand, rail posts in front of the camel's path
        vrect(c, x0, -160, x1 - x0, 3000, [SANDS[0], SANDS[1], SANDS[2], SANDS[3]], [0, 0.05, 0.3, 1])
        c.drawRect(R(x0, -150, x1 - x0, 10), P("#F8FAFC", 0.9))
        for k in range(int(x0 // 300) - 1, int(x1 // 300) + 2):
            xx = k * 300 - (d % 300)
            c.drawRect(R(xx, -150, 10, 70), P("#F1F5F9", 0.9))
        # dust behind the camel
        if runk > 0.2:
            rng = random.Random(int(t * 12))
            for i in range(10):
                q = rng.uniform(0, 1)
                c.drawCircle(-160 - q * 400, -20 - q * 60 + rng.uniform(-20, 20), 20 + q * 50, P("#E8C08F", 0.35 * (1 - q) * runk))
        # line-up / race: several camels
        if in_reveal:
            for i, (dx, dy, sc, col) in enumerate(((-520, -40, 0.7, 0), (-260, -20, 0.8, 1), (300, -10, 0.85, 3), (560, 6, 0.9, 4))):
                pp = ph * (1 + i * 0.07) + i
                rk = runk if t >= T["go"] else 0.0
                camel(c, dx + (0 if t >= T["go"] else 0), dy, sc, pp, run=rk, col=shade(CAMEL, -0.1 + i * 0.05))
                robot_new(c, dx + 20 * sc, dy - 470 * sc, sc * 0.9, t, spin=math.sin(t * 9 + i) * 40, face=1.0, silk=1.0,
                          silk_col=SILKS[col], speaker=1.0)
            if t < T["go"]:                                                   # the start gate
                for gx in range(-700, 900, 260):
                    c.drawRect(R(gx, -560, 16, 560), P("#F8FAFC", 0.9))
                c.drawRect(R(-700, -580, 1600, 30), P("#E11D48", 0.95))
        # the hero
        sc_k = self.scare.at(t) if s("break4") - 0.12 <= t < s("cta") - 0.12 else 0.0
        ear = self.spk.at(t) if s("fix3") - 0.12 <= t < s("break4") else 0.0
        camel(c, 0, 0, 1.0, ph, run=runk, scared=sc_k, ear=ear)
        old = s("break4") - 0.12 <= t < T["face"] + 0.1
        if old:
            robot_old(c, 20, -470, 0.85, a=1.0 - prog(t, T["face"] - 0.1, T["face"] + 0.1))
        if not old or t >= T["face"] - 0.1:
            spin = 0.0
            if t >= s("fix2") - 0.12:
                spin = (math.sin(t * 10) * 40 + 20) * self.whip_on.at(t) if t < s("break3") else math.sin(t * 9) * 30
            whip = self.whip_on.at(t) if s("fix2") - 0.12 <= t < s("break3") - 0.12 else (0.0 if s("break2") - 0.12 <= t < s("fix2") else 1.0)
            in4 = s("break4") - 0.12 <= t < s("cta") - 0.12
            face = prog(t, T["face"] - 0.1, T["face"] + 0.3) if in4 else (1.0 if t >= s("cta") - 0.12 else 0.0)
            silk = prog(t, T["silks"] - 0.1, T["silks"] + 0.3) if in4 else (1.0 if t >= s("cta") - 0.12 else 0.0)
            spk = self.spk.at(t) if s("fix3") - 0.12 <= t else 0.0
            if in4:
                spk = 1.0
            robot_new(c, 20, -470, 1.0, t, spin=spin, whip=whip, face=face, silk=silk, speaker=spk)
        if s("break4") - 0.12 <= t < s("cta") - 0.12:
            pk = prog(t, T["perfume"] - 0.1, T["perfume"] + 0.8) * (1 - prog(t, T["perfume"] + 1.4, T["perfume"] + 2.0))
            if pk > 0:
                for i in range(12):
                    q = (t * 0.8 + i / 12.0) % 1.0
                    c.drawCircle(60 + q * 160 + math.sin(i * 3) * 20, -560 - q * 120 + math.cos(i * 2) * 30, 8 + q * 14,
                                 P("#F9A8D4", 0.7 * pk * (1 - q)))
            if sc_k > 0.3:
                word(c, "!", 400, -620, 120, WARN, sc_k)
        # the speaker's sound waves into the camel's ear
        if ear > 0.3 and t < s("break4") - 0.12:
            for i in range(3):
                q = (t * 2.5 + i / 3.0) % 1.0
                c.drawArc(R(90 - 60 * q, -560 - 60 * q, 120 * q + 20, 120 * q + 20), -40, 80, False, P(HILITE, 0.8 * (1 - q), stroke=6))
        c.restore()
        self.ui["hump"] = self.at(20, -560)
        self.ui["ear"] = self.at(290, -510)
        self.ui["suv"] = self.at(-470 + 40, -300)

    def ui_track(self, c, t, tw):
        T, s = self.T, self.tl.s
        sp = self.spd.at(tw)
        if tw < s("break1") - 0.12 or s("break2") - 0.12 <= tw < s("break4") - 0.12 or s("stat") <= tw < s("tag"):
            if tw < s("break1") - 0.12 or tw < s("break4") - 0.12:
                kmh = sp / 1500.0 * 60
                v2.chip(c, 190, 330, f"{kmh:.0f} {self.L['kmh']}", self.span(T["sixty"] - 0.2, s("break1") + 0.1) if tw < s("break1")
                        else 1.0, accent=HILITE if kmh > 45 else WARN, size=40)
        if tw < s("break1") - 0.12:
            hx, hy = self.ui.get("hump", (560, 520))
            self.label(hx, hy, 300, 470, "robot", T["robot"] - 0.05, T["owner"] - 0.1, ACCENT, size=34)
            vx, vy = self.ui.get("suv", (300, 900))
            self.label(vx, vy, 300, 1120, "owner", T["owner"] - 0.1, T["congrats"], "#FDE68A", size=34)
            self.chip(540, 470, "jockey", T["jockey"] - 0.15, s("break1") + 0.1, accent=ACCENT, size=36)
            return
        if s("break2") - 0.12 <= tw < s("fix2") - 0.12:
            hx, hy = self.ui.get("hump", (560, 520))
            self.chip(hx, hy - 170, "sits", T["sits"] - 0.15, s("fix2") - 0.15, accent="#CBD5E1", size=36)
            self.chip(540, 1120, "slow", T["speed"] - 0.15, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["speed"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["speed"] + 0.05, 1.5)
            return
        if tw < s("break3") - 0.12:
            hx, hy = self.ui.get("hump", (560, 520))
            self.label(hx + 40, hy + 80, 300, 1120, "whip", T["whip"] - 0.15, s("break3") - 0.15, "#F87171", size=34)
            keyfob(c, 850, 1000, prog(tw, T["press"], T["press"] + 0.1) * (1 - prog(tw, T["press"] + 0.3, T["press"] + 0.4)),
                   self.span(T["button"] - 0.3, s("break3") - 0.15))
            self.badge("check", T["button"] + 0.15, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix3") - 0.12:
            ex, ey = self.ui.get("ear", (700, 500))
            self.chip(540, 470, "voice", T["voice"] - 0.1, T["track"] - 0.1, accent="#FDE68A", size=34)
            self.chip(540, 470, "where", T["track"] - 0.1, s("fix3") - 0.15, accent=WARN, size=34)
            self.badge("alert", T["track"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["track"] + 0.05, 1.5)
            return
        if tw < s("break4") - 0.12:
            ex, ey = self.ui.get("ear", (700, 500))
            self.chip(540, 470, "speaker", T["sp0"], T["yell3"], accent=HILITE, size=34)
            vx, vy = self.ui.get("suv", (300, 900))
            k = self.span(T["yell3"], s("break4") - 0.15)
            if k > 0:
                v2.chip(c, max(250, vx + 60), vy - 80, self.L["yalla"], k, accent=HILITE, size=40)
            self.badge("check", T["walkie"] + 0.15, s("break4") - 0.15, x=880, y=330)
            return
        if tw < s("cta") - 0.12:
            hx, hy = self.ui.get("hump", (560, 520))
            self.chip(540, 470, "scared", T["scared"] - 0.1, T["face"] - 0.1, accent=WARN, size=44)
            self.badge("alert", T["nothing"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["scared"], 1.6)
            self.label(hx, hy - 60, 280, 600, "face", T["face"] - 0.05, T["glasses"] + 0.4, "#E8B48A", size=32)
            self.label(hx + 10, hy - 70, 800, 600, "glasses", T["glasses"] - 0.05, T["silks"] + 0.3, "#94A3B8", size=32)
            self.label(hx, hy + 20, 280, 1100, "silks", T["silks"] - 0.05, s("cta") - 0.15, "#E11D48", size=32)
            self.label(hx + 60, hy - 40, 800, 1100, "perfume", T["perfume"] - 0.1, s("cta") - 0.15, "#F9A8D4", size=32)
            self.badge("check", T["perfume"] + 0.2, s("cta") - 0.15, x=880, y=330)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.1:
            self.chip(540, 470, "line", T["line"] - 0.1, T["go"], accent=HILITE, size=40)
            self.chip(540, 470, "chase", T["chases"] - 0.05, s("stat") - 0.15, accent="#FDE68A", size=34)

    # ------------------------------------------------------------------ set: the scale (break1, fix1)
    def draw_scale(self, c, t):
        T, s = self.T, self.tl.s
        room(c, 0, 0, W, 1060, wall="#3B2F2A", floor="#5A4636", t=t, lamp=True, lamp_x=540)
        vrect(c, 0, 1060, W, H - 1060, ["#5A4636", "#3B2F2A", "#21180F"])
        kg = self.kg.at(t)
        scale_dial(c, 540, 960, kg)
        k = prog(t, T["strip0"], T["strip0"] + 0.5) if t >= s("fix1") - 0.12 else 0.0
        if k < 1:
            robot_old(c, 540, 960, 2.2 * (1 - k * 0.3), a=1 - k)
            if k > 0:                                                      # parts fly off
                for i, (vx, vy) in enumerate(((-600, -500), (520, -620), (-380, -820), (700, -300))):
                    q = k
                    c.drawRRect(rr(540 + vx * q - 30, 700 + vy * q + 900 * q * q - 30, 60, 60, 10), P("#9CA3AF", 1 - q))
        if k > 0:
            c.save()
            c.translate(540, 960)
            c.scale(2.4, 2.4)
            c.translate(-540, -960)
            robot_new(c, 540, 952, 1.0, t, spin=0.0, whip=1.0, a=k, glow=prog(t, T["kilos"] - 0.2, T["kilos"] + 0.2))
            c.restore()
        if s("break1") <= t < s("fix1"):
            suitcase(c, 860, 1180, 1.0, prog(t, T["suitcase"] - 0.2, T["suitcase"] + 0.1))

    def ui_scale(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 470, "lighter", T["faster"] - 0.1, s("fix1") - 0.15, accent=HILITE, size=38)
            self.chip(860, 1240 - 330, "suitcase", T["suitcase"] - 0.1, s("fix1") - 0.15, accent=WARN, size=36)
            self.badge("alert", T["suitcase"] + 0.1, s("fix1") - 0.2, x=880, y=330)
            self.red(T["suitcase"] + 0.1, 1.5)
            return
        self.label(540 + 80, 960 - 75, 840, 640, "drill", T["drill"] - 0.1, s("break2") - 0.15, "#F59E0B", size=32)
        self.label(540 - 30, 960 - 110, 250, 640, "battery", T["battery"] - 0.1, s("break2") - 0.15, "#22C55E", size=32)
        self.label(540 + 80, 960 - 330, 820, 470, "radio", T["radio"] - 0.1, s("break2") - 0.15, "#CBD5E1", size=32)
        self.chip(540, 470, "kilos", T["kilos"] - 0.1, s("break2") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["kilos"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: road (tag)
    def draw_road(self, c, t):
        T = self.T
        cam = (100, -260, 0.62)
        gy = self.sky_and_dunes(c, t, cam, self.run.at(t))
        self.view(c, cam)
        vrect(c, -900, -160, 2200, 3000, [SANDS[1], SANDS[2], SANDS[3]], [0, 0.2, 1])
        q = (t - self.tl.s("tag")) * 0.6
        for i in range(3):                                                   # tiny camels far away on the track
            camel(c, 300 + i * 260 + q * 200, -330, 0.25, self.gait(t) + i, run=1.0)
        vrect(c, -900, -260, 2200, 200, ["#3F3F46", "#27272A"])
        jam = prog(t, T["jam"] - 0.6, T["jam"] + 0.4)
        cols = ("#F8FAFC", "#1F2937", "#B91C1C", "#E5E7EB", "#0F766E", "#F8FAFC", "#475569")
        for i in range(7):
            lane = i % 2
            x = -760 + i * 270 + math.sin(t * 3 + i) * 10 * (1 - jam) - lane * 60
            y = -120 + lane * 130
            hk = clamp(math.sin(t * 6 + i * 1.7) * 3) * jam
            suv(c, x, y, 0.75, t * (1 - jam * 0.95) + i, owner=1.0, yell=jam, radio=1.0, col=cols[i], honk=hk)
        rng = random.Random(int(t * 10))
        for i in range(16):
            c.drawCircle(rng.uniform(-900, 1300), rng.uniform(-260, 120), rng.uniform(30, 90), P("#E8C08F", 0.18))
        c.restore()
        self.ui["cam"] = cam

    def ui_road(self, c, t, tw):
        T = self.T
        k = self.span(T["jam"] - 0.1, self.duration + 1, 0.25, 0.1)
        if k > 0:
            v2.chip(c, 540, 470, self.L["real"], k, accent=WARN, size=44)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSKY, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        gallop = []
        for k in range(int(self.duration * 2.2)):
            tt = 0.2 + k / 2.2
            if self.spd.at(self.world_t(tt)) > 600 and not (s("tag") - 0.2 <= tt):
                gallop.append((tt, sfx.thud(0.18), -20))
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (T["owner"], sfx.beep(), -14), (T["yells"], sfx.buzz(), -16),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 61), -9), (T["jockey"], sfx.chime(), -9)] + gallop
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 62), -4), (T["first"], sfx.thud(0.4), -8),
               (T["suitcase"], sfx.ding(), -10), (T["suitcase"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 63), -5), (T["strip0"], sfx.clank(), -8),
               (T["drill"], sfx.whirr(0.6, 300.0, 500.0, 64), -10), (T["kilos"], sfx.ding(), -8), (T["kilos"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["speed"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["spins"], sfx.whirr(1.2, 260.0, 420.0, 66), -10), (T["press"], sfx.click(67), -6), (T["button"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["track"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["sp0"], sfx.pop(69), -8), (T["yell3"], sfx.buzz(), -12), (T["walkie"], sfx.beep(), -12),
               (T["walkie"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 70), -4), (T["scared"] - 0.1, sfx.womp(), -6),
               (T["nothing"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["face"], sfx.pop(71), -8), (T["glasses"], sfx.pop(72), -9), (T["silks"], sfx.whoosh(0.4, False, 73), -10),
               (T["perfume"], sfx.hiss(0.8, 74), -10), (T["perfume"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(75), 0), (T["follow"] - 0.15, sfx.pop(76), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 77), -6), (T["go"], sfx.ding(), -6), (T["go"] + 0.1, sfx.thud(0.6), -8),
               (T["suv"], sfx.whirr(1.4, 90.0, 140.0, 78), -12)]
        ev += [(T["s1"], sfx.pop(79), -3), (T["s2"], sfx.pop(80), -3), (T["s3"], sfx.pop(81), -3)]
        ev += [(T["cong2"], sfx.pop(82), -2), (T["cong2"], sfx.sparkle(1.0, 14, 83), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 84), -6), (T["jam"], sfx.beep(1200.0), -10), (T["jam"] + 0.3, sfx.beep(900.0), -10),
               (T["jam"] + 0.7, sfx.beep(1400.0), -10)]
        return ev


NAME = "camel"
EPISODE = Camel
