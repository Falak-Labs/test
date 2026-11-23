"""Episode 68 - Taipei 101 and its giant swinging ball.  v2 look: the tower in elevation (1 m = 2 units, ground y = 0,
eight flared sections of eight floors on a tapered base, a spire) bending in a typhoon, and a cut-open view of the
damper floors with the golden ball on its cables and the pistons under it.

Sets: city (hook: close on the golden ball swinging in a window cut into the top while rain lashes the tower, out to
the whole tower bending in the storm; break1: typhoon rain and a seismograph; fix1: a bamboo stalk grows beside the
tower, its nodes on the eight sections, then x-ray of the steel and concrete columns; stat: dusk; closer: night,
fireworks off the tower), room (break2: an office near the top tilting, a swinging lamp, seasick people; fix2: the
ball lowered on its cables), ball (break3: the ball swinging WITH the tower and the sway growing; fix3: tuned, the
ball swings against it and the sway dies; break4: the wind stops and the ball keeps going; fix4: eight pistons glow
and stop it; reveal: the 2015 typhoon, a full metre of swing on a ruler, visitors filming), tag (a car hits a speed
bump and the cup in the driver's hand empties into the lap; AR: tea on the white thobe).
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of  # noqa: E402
from liberty import rain, lightning  # noqa: E402
from bridge import wind  # noqa: E402

GOLD = ("#FDE68A", "#F59E0B", "#B45309")
GLASS_T = ("#2F6B6B", "#3E8A86", "#1E4E52")      # the tower's blue-green glass
SEG_H = 68.0                                     # one section of eight floors (34 m)
BASE_TOP = -200.0
SEG_TOP = BASE_TOP - 8 * SEG_H                   # -744
CROWN_TOP = -830.0
SPIRE_TOP = -1016.0
BALL_Y = -738.0                                  # the damper (drawn larger than life in the full view)


def bend(x, y, sway):
    """Horizontal offset of a point of the tower at height -y for a sway (units at the spire tip)."""
    h = clamp(-y / -SPIRE_TOP)
    return x + sway * h * h, y


def poly_b(c, pts, sway, paint):
    c.drawPath(path_of([bend(px, py, sway) for px, py in pts], close=True), paint)


def tower(c, t, sway=0.0, lit=0.0, night=0.0, xray=0.0, cut=0.0, ball_dx=0.0, hi=-1, a=1.0, rain_k=0.0):
    """Taipei 101 at x = 0 on y = 0 (world). sway: offset of the spire tip; cut 0..1 opens a window on the damper floors;
    ball_dx: the ball's swing inside it (units); xray 0..1 shows the steel and concrete columns; hi = section to light."""
    if a <= 0:
        return
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    g0, g1, g2 = (mix(col, "#0B1B2A", 0.45 * night) for col in GLASS_T)
    # podium (the mall)
    c.drawRect(R(-230, -52, 460, 52), lin_paint(0, -52, 0, 0, [mix("#5B7C86", "#1C2A3A", night), mix("#3B5560", "#121C28", night)]))
    for k in range(9):
        c.drawRect(R(-215 + k * 48, -40, 34, 26), P("#FDE68A", 0.25 + 0.6 * lit))
    # tapered base
    poly_b(c, [(-96, -52), (96, -52), (70, BASE_TOP), (-70, BASE_TOP)], sway,
           lin_paint(-96, 0, 96, 0, [g1, g0, g2], a=1.0))
    for k in range(1, 7):                                                  # floor bands on the base
        yy = -52 + (BASE_TOP + 52) * k / 7
        hw = lerp(96, 70, k / 7)
        x0, _ = bend(-hw, yy, sway)
        x1, _ = bend(hw, yy, sway)
        c.drawLine(x0, yy, x1, yy, P("#9FD3CF", 0.25, stroke=2))
    cx, cy = bend(0, -120, sway)                                           # the ruyi ornament on the base
    c.drawCircle(cx, cy, 20, P("#D9B45A", 0.85))
    c.drawCircle(cx, cy, 12, P(g2, 1.0))
    # eight flared sections
    for i in range(8):
        yb = BASE_TOP - i * SEG_H
        yt = yb - SEG_H
        k = 1.0 if hi == i else 0.0
        col0 = mix(g0, "#FDE68A", 0.35 * k)
        poly_b(c, [(-62, yb), (62, yb), (82, yt), (-82, yt)], sway, lin_paint(-82, 0, 82, 0, [g1, col0, g2]))
        for j in range(1, 8):                                              # the eight floors of each section
            yy = yb - SEG_H * j / 8
            hw = lerp(62, 82, j / 8)
            x0, _ = bend(-hw + 3, yy, sway)
            x1, _ = bend(hw - 3, yy, sway)
            c.drawLine(x0, yy, x1, yy, P("#BFE9E4", 0.18 + 0.2 * lit, stroke=2))
            if lit > 0:
                rng = random.Random(i * 31 + j)
                for q in range(6):
                    if rng.random() < 0.6:
                        wx = lerp(x0, x1, (q + 0.5) / 6)
                        c.drawRect(R(wx - 5, yy + 1, 10, 5), P("#FFE7A8", 0.55 * lit))
        xa, _ = bend(-82, yt, sway)
        xb, _ = bend(82, yt, sway)
        c.drawLine(xa, yt, xb, yt, P("#E7F7F5", 0.55, stroke=4))
    # the crown and the spire
    poly_b(c, [(-58, SEG_TOP), (58, SEG_TOP), (50, -790), (-50, -790)], sway, P(g0))
    poly_b(c, [(-40, -790), (40, -790), (32, CROWN_TOP), (-32, CROWN_TOP)], sway, P(g1))
    poly_b(c, [(-10, CROWN_TOP), (10, CROWN_TOP), (6, -930), (-6, -930)], sway, P("#94A3B8"))
    poly_b(c, [(-4, -930), (4, -930), (1, SPIRE_TOP), (-1, SPIRE_TOP)], sway, P("#CBD5E1"))
    tx, ty = bend(0, SPIRE_TOP, sway)
    beacon(c, tx, ty + 2, t, hz=0.8, r=5)
    if xray > 0:                                                           # columns of steel filled with concrete
        for xc in (-44, -16, 16, 44):
            pts = [bend(xc * (1.0 if y_ > BASE_TOP else 1.0), y_, sway) for y_ in range(0, int(SEG_TOP) - 1, -24)]
            c.drawPath(path_of(pts), P("#FACC15", 0.9 * xray, stroke=7))
            c.drawPath(path_of(pts), P("#9CA3AF", 0.6 * xray, stroke=3))
    if cut > 0:                                                            # a window cut into the damper floors
        wx, wy = bend(0, BALL_Y, sway)
        c.drawRRect(rr(wx - 46, wy - 34, 92, 64, 6), P("#0B1220", cut))
        bx, by = wx + ball_dx, wy + 2
        c.drawLine(wx - 14, wy - 34, bx - 6, by - 8, P("#CBD5E1", cut, stroke=2))
        c.drawLine(wx + 14, wy - 34, bx + 6, by - 8, P("#CBD5E1", cut, stroke=2))
        c.drawCircle(bx, by, 16, rad_paint(bx - 5, by - 6, 22, [GOLD[0], GOLD[1], GOLD[2]], [0.0, 0.5, 1.0], a=cut))
        add_glow(c, bx, by, 30, "#FDE68A", 0.35 * cut)
        c.drawRRect(rr(wx - 46, wy - 34, 92, 64, 6), P("#E7F7F5", cut, stroke=3))
    if rain_k > 0:                                                         # wet sheen on the windward face
        poly_b(c, [(-62, BASE_TOP), (-82, SEG_TOP), (-70, SEG_TOP), (-52, BASE_TOP)], sway, P("#E0F2FE", 0.2 * rain_k))
    if a < 1:
        c.restore()


def bamboo(c, x, t, grow=1.0, a=1.0):
    """A bamboo stalk beside the tower, its nodes level with the tower's sections (world)."""
    if a <= 0 or grow <= 0:
        return
    top = lerp(0, SEG_TOP - 40, grow)
    c.drawRect(R(x - 20, top, 40, -top), lin_paint(x - 20, 0, x + 20, 0, ["#4D7C0F", "#84CC16", "#3F6212"], a=a))
    for i in range(9):
        yy = BASE_TOP - i * SEG_H
        if yy >= top:
            c.drawRRect(rr(x - 26, yy - 5, 52, 10, 5), P("#365314", a))
    for i, yy in enumerate((-300, -480, -640)):
        if yy >= top:
            d = -1 if i % 2 else 1
            c.drawPath(path_of([(x, yy), (x + d * 70, yy - 40), (x + d * 120, yy - 30)]), P("#65A30D", a, stroke=8))


def city(c, t, night=0.0, a=1.0):
    """Mountains, the night city and the ground (world)."""
    c.save()
    v2.ridge(c, -1800, 1800, 0, 330, mix("#24425A", "#0C1626", night), mix("#1A2E40", "#08101C", night), seed=12, step=160,
             rough=0.45)
    c.restore()
    skyline_night(c, -1600, -250, 0, seed=7, hmin=50, hmax=230, lit=0.25 + 0.4 * night)
    skyline_night(c, 250, 1600, 0, seed=9, hmin=50, hmax=230, lit=0.25 + 0.4 * night)
    c.drawRect(R(-2000, 0, 4000, 1200), lin_paint(0, 0, 0, 700, [mix("#26323F", "#0E141C", night), "#05080C"]))


def seismo(c, x, y, w, h, t, k, a=1.0):
    """A seismograph strip (screen space)."""
    if a <= 0:
        return
    c.drawRRect(rr(x, y, w, h, 16), P("#F8FAFC", 0.94 * a))
    pts = []
    for i in range(int(w - 20)):
        u = i / (w - 20)
        amp = (h * 0.4) * k * (0.3 + 0.7 * math.sin(math.pi * u))
        pts.append((x + 10 + i, y + h / 2 + math.sin(i * 0.45 + t * 30) * amp * random.Random(i // 6).uniform(0.4, 1.0)))
    c.drawPath(path_of(pts), P(WARN, a, stroke=3))


def firework(c, x, y, t, t0, col, n=22, r=160, a=1.0):
    d = t - t0
    if d < 0 or d > 1.6:
        return
    k = e_out(clamp(d / 0.9))
    fade = 1 - clamp((d - 0.6) / 1.0)
    for i in range(n):
        q = math.radians(i * 360 / n)
        px, py = x + math.cos(q) * r * k, y + math.sin(q) * r * k + 40 * d * d
        c.drawCircle(px, py, 5, P(col, fade * a))
        c.drawLine(px, py, px - math.cos(q) * 26 * k, py - math.sin(q) * 26 * k, P(col, 0.5 * fade * a, stroke=3))
    add_glow(c, x, y, r * 0.8, col, 0.25 * fade * a)


def golden_ball(c, x, y, r, a=1.0, hot=0.0):
    """The damper sphere: 41 stacked plates seen from the side (screen space)."""
    c.drawCircle(x, y, r, rad_paint(x - r * 0.35, y - r * 0.4, r * 1.4, [GOLD[0], GOLD[1], GOLD[2]], [0.0, 0.45, 1.0], a=a))
    for k in range(-5, 6):                                                 # plate lines
        yy = y + k * r / 6
        hw = math.sqrt(max(0.0, r * r - (yy - y) ** 2))
        c.drawLine(x - hw, yy, x + hw, yy, P("#92400E", 0.35 * a, stroke=2))
    c.drawCircle(x - r * 0.35, y - r * 0.4, r * 0.22, P("#FFFBEB", 0.55 * a))
    if hot > 0:
        add_glow(c, x, y + r, r, "#F97316", 0.4 * hot * a)


def piston(c, x0, y0, x1, y1, hot=0.0, a=1.0):
    """A hydraulic damper between the ball (x1, y1) and the floor (x0, y0)."""
    mx, my = lerp(x0, x1, 0.55), lerp(y0, y1, 0.55)
    c.drawLine(x0, y0, mx, my, P(mix("#475569", "#EA580C", hot), a, stroke=30))
    c.drawLine(mx, my, x1, y1, P("#CBD5E1", a, stroke=14))
    c.drawCircle(x0, y0, 14, P("#334155", a))
    if hot > 0:
        add_glow(c, lerp(x0, mx, 0.5), lerp(y0, my, 0.5), 50, "#F97316", 0.55 * hot * a)


def office(c, t, tilt, a=1.0, sick=0.0, lamp=0.0):
    """An office near the top (screen space): windows on the storm, a desk, a hanging lamp swinging, two workers."""
    c.drawRect(R(-200, 160, W + 400, 1000), P("#1B2433", a))
    for k in range(5):
        c.drawRect(R(30 + k * 210, 300, 180, 520), P("#0E1A2B", a))
        c.drawRect(R(30 + k * 210, 300, 180, 520), P("#94A3B8", 0.5 * a, stroke=4))
    c.drawRect(R(-200, 980, W + 400, 300), P("#2A3445", a))
    lx = 540 + math.sin(lamp) * 180
    ly = 330 + math.cos(lamp) * 260
    c.drawLine(540, 160, lx, ly, P("#CBD5E1", a, stroke=4))
    c.drawPath(path_of([(lx - 60, ly + 40), (lx + 60, ly + 40), (lx + 26, ly), (lx - 26, ly)], close=True), P("#FDE68A", a))
    add_glow(c, lx, ly + 60, 120, "#FDE68A", 0.35 * a)
    c.drawRect(R(300, 860, 480, 26), P("#8A6A48", a))                       # desk
    for lx_ in (320, 740):
        c.drawRect(R(lx_, 886, 20, 100), P("#6B5236", a))
    gx = 640 + math.sin(tilt * 0.7) * 30                                    # a glass sliding on the desk
    c.drawRRect(rr(gx - 22, 790, 44, 70, 8), P("#BFDBFE", 0.6 * a))
    c.drawRect(R(gx - 18, 820 + math.sin(t * 6) * 6, 36, 36), P(WATER_C, 0.6 * a))
    for i, (px, col) in enumerate(((230, "#2563EB"), (880, "#DB2777"))):
        person(c, px, 985, 330, col, t + i, pose="shrug" if sick > 0.5 else "stand", face=1 if i == 0 else -1,
               skin=mix("#E8B48A", "#9BCB7A", sick), a=a)
        if sick > 0:                                                        # dizzy swirls
            for k in range(3):
                q = t * 5 + k * 2.1
                c.drawCircle(px + math.cos(q) * 40, 985 - 360 + math.sin(q) * 14, 7, P("#A3E635", sick * a))


WATER_C = "#60A5FA"


def car_side(c, x, y, s, t, bump=0.0, a=1.0, col="#DC2626"):
    """A small car in side view (screen space), wheels on y; bump lifts the front then the back."""
    c.save()
    c.translate(x, y - 40 * s * bump)
    c.rotate(-6 * bump)
    c.scale(s, s)
    c.drawRRect(rr(-150, -95, 300, 60, 24), P(col, a))
    c.drawPath(path_of([(-80, -95), (-50, -150), (60, -150), (95, -95)], close=True), P(col, a))
    c.drawPath(path_of([(-66, -100), (-44, -140), (6, -140), (6, -100)], close=True), P("#BAE6FD", 0.85 * a))
    c.drawPath(path_of([(16, -100), (16, -140), (54, -140), (80, -100)], close=True), P("#BAE6FD", 0.85 * a))
    for wx in (-90, 95):
        c.drawCircle(wx, -30, 34, P("#111827", a))
        c.drawCircle(wx, -30, 14, P("#9CA3AF", a))
    c.drawCircle(146, -70, 8, P("#FDE68A", a))
    c.restore()


def cup_inset(c, x, y, r, t, spill, a=1.0, tea=False):
    """A round inset: a hand holding a cup over a lap; spill 0..1 throws the drink out (screen space)."""
    if a <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(x, y, r)
    c.clipPath(cp, doAntiAlias=True)
    c.drawCircle(x, y, r, P("#334155", a))
    lap = "#F8FAFC" if tea else "#1E40AF"
    c.drawRRect(rr(x - r, y + r * 0.25, 2 * r, r, 40), P(lap, a))                   # the lap (thobe or jeans)
    if tea:
        c.drawPath(path_of([(x - 40, y - 40), (x + 40, y - 40), (x + 30, y + 50), (x - 30, y + 50)], close=True),
                   P("#E0F2FE", 0.55 * a))                                          # a tea glass
        liq = "#B45309"
    else:
        c.drawPath(path_of([(x - 46, y - 60), (x + 46, y - 60), (x + 34, y + 60), (x - 34, y + 60)], close=True),
                   P("#F5F5F4", a))                                                 # a paper cup
        c.drawRect(R(x - 44, y - 70, 88, 16), P("#57534E", a))
        liq = "#78350F"
    if spill > 0:
        for i in range(9):
            f = clamp(spill * 1.4 - i * 0.05)
            px = x + (i - 4) * 18 * f
            py = y - 50 - math.sin(f * math.pi) * 120 + f * 220
            c.drawCircle(px, py, 14 - i % 3 * 2, P(liq, a * (1 - 0.3 * f)))
        c.drawOval(R(x - 120 * spill, y + r * 0.35, 240 * spill, 60 * spill), P(liq, 0.8 * a))
    c.drawRRect(rr(x + 30, y - 10, 90, 50, 24), P("#E8B48A", a))                   # the hand
    c.restore()
    c.drawCircle(x, y, r, P("#F8FAFC", a, stroke=8))


# ====================================================================================== the episode
class Taipei(EpisodeV2):
    BUILD_NO = 68
    FIRST_SET = "city"
    CLEAR = "#0B1220"
    TITLE = {"en": "TAIPEI 101", "ar_sa": "برج تايبيه"}
    EMPH = {"en": ["CONGRATS", "GOLDEN", "BALL", "SWINGING", "SKYSCRAPER", "STEADY", "TYPHOON", "TAIPEI", "101",
                   "YOURSELF", "TYPHOONS", "EARTHQUAKES", "BAMBOO", "EIGHT", "SECTIONS", "FLOORS", "STEEL", "CONCRETE",
                   "SWAYS", "SEASICK", "HANG", "FIVE", "HUNDRED", "CARS", "CABLES", "WRONG", "RHYTHM", "SHAKES",
                   "TUNE", "LEANS", "OTHER", "STOP", "PISTONS", "SHOCK", "HEAT", "FOLLOW", "DISHWASHER", "METER",
                   "BIGGEST", "CALM", "SIXTY", "FORTY", "PERCENT", "SPEED", "BUMP", "COFFEE", "LAP"],
            "ar_sa": ["مبروك", "كورة", "ذهبية", "تتمرجح", "برجك", "الإعصار", "تايبيه", "بيدك", "أعاصير", "وزلازل",
                      "الخيزران", "ثمان", "قطع", "أدوار", "حديد", "خرسانة", "يتمايل", "يدوخون", "خمسمية", "سيارة",
                      "حبال", "تمرجحت", "إيقاعه", "تهز", "إيقاع", "يمين", "يسار", "توقف", "مكابس", "المساعدات",
                      "لحرارة", "تابعني", "غسالة", "الصحون", "إعصار", "متر", "أكبر", "ثابت", "ستمية", "أربعين", "مطب",
                      "الشاهي", "ثوبك"]}
    KEYS = {"ar_sa": {
        ("hook", "GOLDEN"): "ذهبية", ("hook", "BALL"): "كورة", ("hook", "SWINGING"): "تتمرجح", ("hook", "SKYSCRAPER"): "برجك",
        ("hook", "STEADY"): "تثبته", ("hook", "TYPHOON"): "الاعصار", ("hook", "CONGRATS"): "مبروك", ("hook", "TAIPEI"): "تايبيه",
        ("break1", "TYPHOONS"): "أعاصير", ("break1", "YEAR"): "سنة", ("break1", "EARTHQUAKES"): "زلازل",
        ("break1", "GROUND"): "الأرض",
        ("fix1", "BAMBOO"): "الخيزران", ("fix1", "EIGHT"): "ثمان", ("fix1", "SECTIONS"): "قطع", ("fix1", "FLOORS"): "أدوار",
        ("fix1", "STEEL"): "حديد", ("fix1", "CONCRETE"): "خرسانة",
        ("break2", "TALL"): "الطويل", ("break2", "SWAYS"): "يتمايل", ("break2", "SEASICK"): "يدوخون",
        ("fix2", "TOP"): "فوق", ("fix2", "HANG"): "تعلق", ("fix2", "BALL"): "كورة", ("fix2", "FIVE"): "خمسمية",
        ("fix2", "CARS"): "سيارة", ("fix2", "CABLES"): "حبال",
        ("break3", "SWINGS"): "تمرجحت", ("break3", "WRONG"): "غير", ("break3", "SHAKES"): "تهز", ("break3", "MORE"): "زيادة",
        ("fix3", "TUNE"): "تضبط", ("fix3", "RHYTHM"): "إيقاع", ("fix3", "LEANS"): "مال", ("fix3", "OTHER"): "يسار",
        ("break4", "BALL"): "الكورة", ("break4", "STOP"): "توقف",
        ("fix4", "PISTONS"): "مكابس", ("fix4", "SHOCK"): "المساعدات", ("fix4", "HEAT"): "حرارة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "TWENTY"): "ألفين", ("reveal", "TYPHOON"): "إعصار", ("reveal", "METER"): "متر",
        ("reveal", "BIGGEST"): "أكبر", ("reveal", "CALM"): "ثابت",
        ("stat", "SIX"): "ستمية", ("stat", "FIVE"): "خمسة", ("stat", "FORTY"): "أربعين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STEEL"): "حديد", ("tag", "TYPHOON"): "الاعصار", ("tag", "BUMP"): "مطب", ("tag", "COFFEE"): "الشاهي",
        ("tag", "LAP"): "ثوبك"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a dishwasher"),
                   "stat": [("660 t", "STEEL BALL"), ("5.5 m", "WIDE"), ("-40%", "SWAY")],
                   "L": {"steady": "STEADY IN A TYPHOON", "ball": "A GOLDEN STEEL BALL", "name": "TAIPEI 101",
                         "typhoon": "TYPHOONS EVERY YEAR", "quake": "+ EARTHQUAKES", "bamboo": "LIKE BAMBOO",
                         "eight": "8 SECTIONS x 8 FLOORS", "columns": "STEEL COLUMNS + CONCRETE", "sway": "IT SWAYS",
                         "sick": "SEASICK UP TOP", "hang": "HANG A STEEL BALL", "cars": "AS HEAVY AS 500 CARS",
                         "cables": "THICK CABLES", "wrong": "WRONG RHYTHM: WORSE", "tune": "TUNED TO THE TOWER",
                         "opposite": "TOWER ONE WAY, BALL THE OTHER", "nostop": "IT WON'T STOP", "pistons": "8 PISTONS",
                         "heat": "SWING -> HEAT", "record": "2015: A FULL METER", "calm": "TOWER: CALM",
                         "spill": "SPLASH!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: غسالة الصحون"),
                      "stat": [("660", "طن"), ("5.5", "متر عرض"), ("40%", "تمايل أقل")],
                      "L": {"steady": "ثابت وسط الإعصار", "ball": "كورة ذهبية", "name": "برج تايبيه 101",
                            "typhoon": "أعاصير كل سنة", "quake": "وزلازل", "bamboo": "مثل الخيزران",
                            "eight": "ثمان قطع × ثمان أدوار", "columns": "حديد مليان خرسانة", "sway": "يتمايل",
                            "sick": "اللي فوق يدوخون", "hang": "كورة حديد", "cars": "وزن خمسمية سيارة",
                            "cables": "حبال غليظة", "wrong": "إيقاع غلط: أسوأ", "tune": "على إيقاع البرج",
                            "opposite": "البرج يمين، الكورة يسار", "nostop": "ما تبي توقف", "pistons": "ثمان مكابس",
                            "heat": "المرجحة تصير حرارة", "record": "متر كامل!", "calm": "البرج ثابت",
                            "spill": "انكب!"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "golden": ("hook", "GOLDEN", 0.08), "ball": ("hook", "BALL", 0.15), "swinging": ("hook", "SWINGING", 0.22),
            "sky": ("hook", "SKYSCRAPER", 0.35), "steady": ("hook", "STEADY", 0.5), "typhoon": ("hook", "TYPHOON", 0.62),
            "congrats": ("hook", "CONGRATS", 0.75), "name": ("hook", "TAIPEI", 0.9),
            "typhoons": ("break1", "TYPHOONS", 0.2), "year": ("break1", "YEAR", 0.45), "quakes": ("break1", "EARTHQUAKES", 0.65),
            "ground": ("break1", "GROUND", 0.92),
            "bamboo": ("fix1", "BAMBOO", 0.15), "eight": ("fix1", "EIGHT", 0.3), "sections": ("fix1", "SECTIONS", 0.4),
            "floors": ("fix1", "FLOORS", 0.5), "steel": ("fix1", "STEEL", 0.7), "concrete": ("fix1", "CONCRETE", 0.92),
            "tall": ("break2", "TALL", 0.15), "sways": ("break2", "SWAYS", 0.4), "seasick": ("break2", "SEASICK", 0.9),
            "top": ("fix2", "TOP", 0.1), "hang": ("fix2", "HANG", 0.2), "ball2": ("fix2", "BALL", 0.35),
            "five": ("fix2", "FIVE", 0.5), "cars": ("fix2", "CARS", 0.65), "cables": ("fix2", "CABLES", 0.9),
            "swings": ("break3", "SWINGS", 0.2), "wrong": ("break3", "WRONG", 0.4), "shakes": ("break3", "SHAKES", 0.7),
            "more": ("break3", "MORE", 0.92),
            "tune": ("fix3", "TUNE", 0.1), "rhythm": ("fix3", "RHYTHM", 0.35), "leans": ("fix3", "LEANS", 0.6),
            "other": ("fix3", "OTHER", 0.92),
            "ball4": ("break4", "BALL", 0.3), "stop": ("break4", "STOP", 0.8),
            "pistons": ("fix4", "PISTONS", 0.25), "shock": ("fix4", "SHOCK", 0.5), "heat": ("fix4", "HEAT", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "y2015": ("reveal", "TWENTY", 0.15), "typhoon5": ("reveal", "TYPHOON", 0.3), "meter": ("reveal", "METER", 0.5),
            "biggest": ("reveal", "BIGGEST", 0.65), "calm": ("reveal", "CALM", 0.92),
            "s1": ("stat", "SIX", 0.05), "s2": ("stat", "FIVE", 0.4), "s3": ("stat", "FORTY", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_steel": ("tag", "STEEL", 0.05), "t_typhoon": ("tag", "TYPHOON", 0.3), "t_bump": ("tag", "BUMP", 0.6),
            "t_coffee": ("tag", "COFFEE", 0.75), "t_lap": ("tag", "LAP", 0.95)})
        T["ground1"] = max(T["ground"], T["quakes"]) + 0.1
        T["seasick1"] = max(T["seasick"], T["sways"]) + 0.1
        T["more1"] = max(T["more"], T["shakes"]) + 0.1
        T["stop1"] = max(T["stop"], T["ball4"]) + 0.1
        T["concrete1"] = max(T["concrete"], T["steel"]) + 0.2
        T["cables1"] = max(T["cables"], T["cars"]) + 0.2
        T["other1"] = max(T["other"], T["leans"]) + 0.2
        T["heat1"] = max(T["heat"], T["shock"]) + 0.2
        T["bump0"] = min(T["t_bump"], T["t_coffee"]) - 0.1
        # ---- sets
        self.cut(s("break2") - 0.12, "room", 1)
        self.cut(s("break3") - 0.12, "ball", -1)
        self.cut(s("stat") - 0.12, "city", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- city camera: from the ball in its window out to the whole tower, then the tower for break1 / fix1
        cm = Camera(0, BALL_Y + 40, 7.0)
        cm.key(0.05, 0, BALL_Y + 38, 6.6, 0.6)
        cm.key(max(0.6, T["steady"] - 0.6), 0, -520, 0.88, max(1.2, T["name"] - T["steady"] + 0.4))
        cm.key(s("fix1"), -80, -520, 0.88, 0.8)
        cm.key(s("stat") - 0.12, 0, -520, 0.88, 0.0)
        cm.key(s("closer") - 0.1, 0, -540, 0.95, 1.0)
        self.cam = cm
        self.spans = [(T["ground1"], T["concrete1"] + 0.3), (T["seasick1"], T["cables1"] + 0.3), (T["more1"], T["other1"] + 0.3),
                      (T["stop1"], T["heat1"] + 0.3)]
        self.shakes = [(T["typhoon"], 0.5, 6), (T["congrats"], 0.35, 8), (T["quakes"], 1.2, 14), (T["seasick1"], 0.3, 6),
                       (T["more1"], 0.6, 10), (T["stop1"], 0.3, 6), (T["meter"], 0.6, 8), (s("closer") + 0.2, 0.35, 9),
                       (T["bump0"], 0.4, 12)]

    def sway(self, t, amp=14.0):
        return amp * math.sin(t * 2 * math.pi / 2.8)

    # ------------------------------------------------------------------ set: city (hook, break1, fix1, stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        storm = t < s("fix1") - 0.12
        closer = t >= s("closer") - 0.1
        stat = s("stat") - 0.12 <= t < s("closer") - 0.1
        night = 1.0 if (storm or closer) else (0.7 if not stat else 0.35)
        if stat:
            v2.sky(c, W, H, 0.0, horizon_y=H * 0.62)
        else:
            vrect(c, 0, 0, W, H, ["#050A14", "#0B1628", "#132238"])
            if storm:
                for i in range(4):
                    v2.cloud(c, (i * 330 + t * 40) % (W + 600) - 300, 260 + (i % 2) * 120, 1.6, body="#1E293B", rim="#475569",
                             a=0.9, seed=i)
        self.view(c, cam)
        city(c, t, night)
        amp = 16.0 if storm else 4.0
        sw = self.sway(t, amp)
        bdx = -sw * 0.9                                                    # the ball swings against the sway
        tower(c, t, sway=sw, lit=1.0 if night > 0.5 else 0.4, night=0.6 * night, cut=1.0 if t < s("break1") else 0.0,
              ball_dx=bdx * 1.3, rain_k=1.0 if storm else 0.0,
              xray=prog(t, T["steel"] - 0.3, T["steel"] + 0.2) if s("fix1") - 0.12 <= t < s("break2") else 0.0,
              hi=int(clamp((t - T["sections"]) / max(0.4, T["floors"] - T["sections"] + 0.4), 0, 0.999) * 8)
              if T["sections"] <= t < T["steel"] and t >= s("fix1") - 0.12 else -1)
        if s("fix1") - 0.12 <= t < s("break2"):
            bamboo(c, -260, t, grow=e_out(prog(t, T["bamboo"] - 0.3, T["bamboo"] + 0.8)))
        c.restore()
        if storm:
            rain(c, t, a=0.9, seed=5)
            wind(c, 0, 600, W, t, n=8, a=0.7, spread=300, seed=1)
            wind(c, 0, 1000, W, t + 0.4, n=6, a=0.6, spread=200, seed=3)
            fl = max(0.0, math.sin(t * 2.3) - 0.92) * 12
            if fl > 0:
                lightning(c, 860, 120, 600, t, int(t * 2.3), a=clamp(fl))
                c.drawRect(R(0, 0, W, H), P("#C7D2FE", 0.12 * clamp(fl)))
            if t >= s("break1") - 0.12:
                qk = prog(t, T["quakes"] - 0.3, T["quakes"]) * (1 - prog(t, s("fix1") - 0.4, s("fix1") - 0.12))
                seismo(c, 650, 1020, 400, 150, t, qk, a=qk)
        if closer:
            fk = prog(t, s("closer"), s("closer") + 0.4)
            tx, ty = self.to_screen(cam, 0, -700)
            for i, (dx, dy, col) in enumerate(((-260, -120, "#F472B6"), (240, -60, "#FDE047"), (-160, 140, "#60A5FA"),
                                                (220, 220, "#34D399"), (0, -320, "#F97316"))):
                period = 1.7
                t0 = s("closer") + i * 0.33
                k = math.floor(max(0.0, t - t0) / period)
                firework(c, tx + dx, ty + dy, t, t0 + k * period, col, a=fk)

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "ball", T["golden"] - 0.1, T["steady"] - 0.2, accent=HILITE, size=44)
            self.chip(540, 300, "steady", T["steady"] - 0.2, T["name"] - 0.3, accent="#93C5FD", size=44)
            self.chip(540, 300, "name", T["name"] - 0.3, s("break1") + 0.1, accent=HILITE, size=54)
            return
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "typhoon", T["typhoons"] - 0.2, T["quakes"] - 0.2, accent="#93C5FD", size=44)
            self.chip(540, 300, "quake", T["quakes"] - 0.2, s("fix1") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["ground1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["ground1"], 1.2)
            return
        if tw < s("break2") - 0.12:
            self.chip(540, 300, "bamboo", T["bamboo"] - 0.2, T["eight"] - 0.2, accent=GOOD, size=50)
            self.chip(540, 300, "eight", T["eight"] - 0.2, T["steel"] - 0.2, accent="#5EEAD4", size=42)
            self.chip(540, 300, "columns", T["steel"] - 0.2, s("break2") - 0.15, accent="#FACC15", size=40)
            self.badge("check", T["concrete1"] + 0.1, s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: room (break2, fix2)
    def draw_room(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        if not fixed:
            tilt = 3.5 * math.sin(t * 2 * math.pi / 2.8) * prog(t, T["sways"] - 0.5, T["sways"])
            c.save()
            c.translate(540, 2600)
            c.rotate(tilt)
            c.translate(-540, -2600)
            office(c, t, tilt, sick=prog(t, T["seasick"] - 0.3, T["seasick"] + 0.2), lamp=math.radians(tilt * 6))
            rain(c, t, a=0.35, seed=8)
            c.restore()
            return
        self.draw_ball_room(c, t, drop=e_out(prog(t, T["hang"] - 0.2, T["ball2"] + 0.5)), swing=0.0)

    def ui_room(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "sway", T["sways"] - 0.3, T["seasick"] - 0.2, accent="#93C5FD", size=50)
            self.chip(540, 300, "sick", T["seasick"] - 0.2, s("fix2") - 0.15, accent="#A3E635", size=46)
            self.badge("alert", T["seasick1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["seasick1"], 1.2)
            return
        self.chip(540, 300, "hang", T["hang"] - 0.2, T["five"] - 0.2, accent=HILITE, size=46)
        self.chip(540, 300, "cars", T["five"] - 0.2, T["cables"] - 0.2, accent="#FDE68A", size=44)
        self.chip(540, 300, "cables", T["cables"] - 0.2, s("break3") - 0.15, accent="#CBD5E1", size=46)
        self.badge("check", T["cables1"] + 0.1, s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ the damper floors (screen space)
    def draw_ball_room(self, c, t, drop=1.0, swing=0.0, frame=0.0, hot=0.0, storm=0.6, people=1.0, ruler=0.0, trail=0.0):
        """Cut-open damper floors: storm windows, floor slabs with a hole for the ball, cables, pistons, visitors.
        swing = the ball's angle (degrees, + to the right); frame = the building's tilt (degrees)."""
        vrect(c, 0, 0, W, H, ["#0B1220", "#111B2E"])
        c.save()
        c.translate(540, 2600)
        c.rotate(frame)
        c.translate(-540, -2600)
        for k in range(6):                                                  # storm windows on both sides
            for side in (0, 1):
                wx = 20 + side * 900
                c.drawRect(R(wx, 260 + k * 150, 140, 120), P("#0E2236"))
        rain(c, t, a=0.5 * storm, seed=11)
        piv = (540, 230)
        L = 470.0
        q = math.radians(swing)
        bx, by = piv[0] + math.sin(q) * L, piv[1] + math.cos(q) * L - (1 - drop) * 900
        for yy in (230, 1080):                                              # slabs
            c.drawRect(R(-100, yy - 18, W + 200, 36), P("#475569"))
        for yy in (420, 610, 800):                                          # floors with a round hole for the ball
            c.drawRect(R(-100, yy - 12, 330, 24), P("#334155"))
            c.drawRect(R(850, yy - 12, 330, 24), P("#334155"))
        if trail > 0:
            for k in range(1, 6):
                qq = math.radians(swing - k * 6 * (1 if math.cos(t * 2.2) > 0 else -1))
                c.drawCircle(piv[0] + math.sin(qq) * L, piv[1] + math.cos(qq) * L, 170, P("#F59E0B", 0.08 * trail))
        for dx in (-60, -20, 20, 60):                                       # cables
            c.drawLine(piv[0] + dx * 2.2, piv[1], bx + dx, by - 150, P("#CBD5E1", 1, stroke=7))
        for k in range(4):                                                  # pistons under the ball
            fx_ = 300 + k * 160
            piston(c, fx_, 1062, bx + (fx_ - 540) * 0.35, by + 140, hot=hot)
        golden_ball(c, bx, by, 170, hot=hot)
        if ruler > 0:
            c.drawRect(R(260, 1000, 560, 46), P("#FDE68A", ruler))
            for k in range(11):
                c.drawLine(260 + k * 56, 1000, 260 + k * 56, 1020 + (10 if k % 5 == 0 else 0), P("#1F2937", ruler, stroke=4))
            text(c, "100 cm", 540, 990, 40, "#FDE68A", "Poppins-Black", a=ruler)
        if people > 0:
            c.drawRect(R(0, 1060, 230, 8), P("#94A3B8", people))
            c.drawRect(R(850, 1060, 230, 8), P("#94A3B8", people))
            for i, px in enumerate((70, 160, 930, 1010)):
                person(c, px, 1068, 150, ("#2563EB", "#DB2777", "#16A34A", "#F59E0B")[i], t + i, pose="look", face=1 if px < 540 else -1,
                       a=people)
        c.restore()
        self.ui["ball"] = (bx, by)

    # ------------------------------------------------------------------ set: ball (break3, fix3, break4, fix4, cta, reveal)
    def draw_ball(self, c, t):
        T, s = self.T, self.tl.s
        P_ = 2.8
        w = 2 * math.pi / P_
        if t < s("fix3") - 0.12:                                            # wrong rhythm: in step, growing
            g = 1 + 2.2 * prog(t, T["swings"] - 0.3, T["more1"] + 0.3)
            frame = 1.2 * g * math.sin(t * w)
            self.draw_ball_room(c, t, swing=6 * g * math.sin(t * w), frame=frame, storm=1.0)
        elif t < s("break4") - 0.12:                                        # tuned: against the sway, dying down
            g = 1 + 2.2 * (1 - prog(t, T["leans"] - 0.4, T["other1"] + 0.6))
            frame = 1.2 * g * math.sin(t * w) * (1 - 0.7 * prog(t, T["leans"], T["other1"] + 0.6))
            self.draw_ball_room(c, t, swing=-8 * math.sin(t * w), frame=frame, storm=1.0)
        elif t < s("reveal") - 0.12:                                        # wind gone, the ball keeps going; pistons stop it
            hk = prog(t, T["pistons"] - 0.3, T["heat"])
            dec = 1 - 0.85 * prog(t, T["pistons"], T["heat1"] + 0.6)
            self.draw_ball_room(c, t, swing=10 * dec * math.sin(t * w), frame=0.0, storm=0.0,
                                hot=hk if t >= s("fix4") - 0.12 else 0.0,
                                trail=1.0 if t < s("fix4") - 0.12 else 0.0)
        else:                                                               # the 2015 typhoon
            mk = prog(t, T["typhoon5"] - 0.3, T["meter"] + 0.3)
            self.draw_ball_room(c, t, swing=(4 + 9 * mk) * math.sin(t * w), frame=0.3 * math.sin(t * w), storm=1.0,
                                ruler=prog(t, T["meter"] - 0.3, T["meter"]))
            fl = max(0.0, math.sin(t * 3.1) - 0.9) * 10
            if fl > 0:
                c.drawRect(R(0, 0, W, H), P("#C7D2FE", 0.15 * clamp(fl)))
            pk = prog(t, T["biggest"] - 0.3, T["biggest"])
            if pk > 0:                                                      # phones up, filming
                for px in (100, 980):
                    c.drawRRect(rr(px - 16, 860, 32, 54, 6), P("#E0F2FE", pk))
                    add_glow(c, px, 887, 40, "#BAE6FD", 0.5 * pk)

    def ui_ball(self, c, t, tw):
        T, s = self.T, self.tl.s
        bx, by = self.ui.get("ball", (540, 700))
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "wrong", T["wrong"] - 0.3, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["more1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["more1"], 1.2)
            return
        if tw < s("break4") - 0.12:
            self.chip(540, 300, "tune", T["tune"] - 0.2, T["leans"] - 0.2, accent="#93C5FD", size=46)
            self.chip(540, 300, "opposite", T["leans"] - 0.2, s("break4") - 0.15, accent=GOOD, size=40)
            ak = self.span(T["leans"] - 0.2, s("break4") - 0.15)
            if ak > 0:
                ph = math.sin(tw * 2 * math.pi / 2.8)
                arrow(c, 540, 1180, 540 + 160 * ph, 1180, "#93C5FD", a=ak, w=12, head=34)
                arrow(c, bx, by - 230, bx - 160 * ph, by - 230, HILITE, a=ak, w=12, head=34)
            self.badge("check", T["other1"] + 0.1, s("break4") - 0.15, x=920, y=440)
            return
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "nostop", T["ball4"] - 0.2, s("fix4") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["stop1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["stop1"], 1.2)
            return
        if tw < s("reveal") - 0.12:
            self.chip(540, 300, "pistons", T["pistons"] - 0.2, T["heat"] - 0.2, accent="#CBD5E1", size=50)
            self.chip(540, 300, "heat", T["heat"] - 0.2, s("cta") - 0.15, accent="#FB923C", size=46)
            self.badge("check", T["heat1"] + 0.1, s("cta") - 0.15, x=920, y=440)
            return
        self.chip(540, 300, "record", T["meter"] - 0.3, T["calm"] - 0.2, accent=HILITE, size=46)
        self.chip(540, 300, "calm", T["calm"] - 0.2, s("stat") - 0.15, accent=GOOD, size=46)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.0, horizon_y=1000)
        c.drawRect(R(0, 1000, W, H - 1000), P("#374151"))
        for k in range(8):
            c.drawRect(R(((k * 180 - t * 300) % (W + 180)) - 90, 1110, 90, 10), P("#F8FAFC", 0.7))
        bump_x = 640
        c.drawPath(path_of([(bump_x - 70, 1100), (bump_x - 30, 1078), (bump_x + 30, 1078), (bump_x + 70, 1100)], close=True),
                   P("#FACC15"))
        for k in range(3):
            c.drawRect(R(bump_x - 50 + k * 40, 1082, 18, 14), P("#111827"))
        b0 = T["bump0"]
        cx = lerp(120, 920, prog(t, b0 - 1.6, b0 + 1.0))
        bump = bump_fn(t, b0)
        car_side(c, cx, 1100, 1.1, t, bump=bump, col="#2563EB" if not self.rtl else "#F8FAFC")
        sp = prog(t, b0, b0 + 0.8)
        cup_inset(c, 540, 620, 240, t, sp, tea=self.rtl)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "spill", T["bump0"] + 0.1, self.duration + 1, accent=WARN, size=56)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1220", "#1E293B"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.5, T["congrats"]), 61), -18), (T["golden"], sfx.creak(1.0, 62), -12),
              (T["typhoon"], sfx.whoosh(0.8, True, 63), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1"), sfx.hiss(2.0, 66), -16), (T["quakes"], rumble(1.4, 67), -8), (T["ground1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["bamboo"], sfx.whoosh(0.5, True, 68), -10), (T["steel"], sfx.clank(300.0, 0.5, 69), -10),
               (T["concrete1"], sfx.ding(), -8), (T["concrete1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 70), -4), (T["sways"], sfx.creak(1.2, 71), -10),
               (T["seasick1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["hang"], sfx.riser(0.8, 73), -12),
               (T["ball2"] + 0.4, sfx.thud(0.5, 74), -6), (T["cables1"], sfx.ding(), -8), (T["cables1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 75), -4), (T["shakes"], rumble(1.2, 76), -10),
               (T["more1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 77), -4), (T["tune"], sfx.click(78), -8),
               (T["other1"], sfx.ding(), -8), (T["other1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["stop1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 80), -4), (T["pistons"], gas_hiss(0.6, 81), -12),
               (T["heat1"], sfx.ding(), -8), (T["heat1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(82), 0), (T["follow"] - 0.15, sfx.pop(83), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 84), -6), (T["typhoon5"], sfx.hiss(1.6, 85), -14),
               (T["meter"], sfx.creak(1.0, 86), -10), (T["calm"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 87), -6), (T["s1"], sfx.pop(88), -3), (T["s2"], sfx.pop(89), -3),
               (T["s3"], sfx.pop(90), -3)]
        ev += [(T["cong2"], sfx.pop(91), -2), (T["cong2"], sfx.sparkle(1.4, 18, 92), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("closer") + 0.3, boom(1.2, 93), -18), (s("closer") + 1.0, boom(1.2, 97), -20)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 94), -6), (T["bump0"], sfx.thud(0.5, 95), -6),
               (T["bump0"] + 0.15, sfx.hiss(0.5, 96), -12)]
        return ev


def bump_fn(t, b0):
    """Height of the car's bounce over the bump (0..1) around b0."""
    d = t - b0
    if d < 0 or d > 0.9:
        return 0.0
    return math.sin(d / 0.9 * math.pi * 2) * (1 - d / 0.9) * (1 if d < 0.45 else 0.6)


NAME = "taipei"
EPISODE = Taipei
