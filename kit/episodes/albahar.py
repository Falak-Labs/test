"""Episode 102 - Abu Dhabi's Al Bahar Towers.  v2 look.

Sets: towers (hook: two round towers wrapped in a honeycomb of umbrella-like shades; the sun comes up on the right and
the shades on the sunny side unfold in a wave while the shaded side stays folded; cta, reveal: a heat bar from the sun,
half of it stopped by the shades, the glass clear and bright behind them; stat; closer at dusk with the lights on),
city (break1: plain glass towers under a white noon sun, heat shimmer, a thermometer climbing; fix1: the glass turns dark
bronze, the glare gone), office (break2: inside behind dark glass at noon, every ceiling light on, people from behind),
lattice (fix2: an old house with a carved wooden mashrabiya, sun through it dapples the floor; break3: the sun moves
round, the fixed screen still shades the room and cuts the sea view into little pieces), unit (fix3: one umbrella up
close, a motor in the middle pushes the panels open, then a field of them following a sun on a screen), storm (break4:
a sandstorm hits the open shades and they flap like sails; fix4: wind cups spin on a roof mast and every shade folds
halfway), tag (a car's round sun shade that will not fold: it springs open in your face).
Side views: the ground is y = 1200 in screen space; a tower is drawn centred on x with its base on the ground.
"""
from v2_base import *  # noqa: F401,F403

GROUND = 1200
SKY = ["#0B3B7A", "#1765B0", "#5FA6DC"]
DUSK = ["#1E1B4B", "#7C3AED", "#F97316"]
GLASSB = "#2F6FB0"
FAB_LIT, FAB_SH, FAB_EDGE = "#DCCBA8", "#7D8796", "#3F4756"


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def unit(c, x, y, r, o, fx=1.0, lit=1.0, a=1.0, spin=0.0):
    """One umbrella shade seen from the front: six triangular panels around a hub. o = 1 open (a flat hexagon), o = 0
    folded (six thin spikes). fx squeezes it sideways (the cylinder's curve), lit 0..1 the sun on its fabric."""
    if a <= 0 or fx <= 0.02:
        return
    half = math.radians(lerp(3.0, 29.0, clamp(o)))
    col = mix(FAB_SH, FAB_LIT, clamp(lit))
    for k in range(6):
        ang = math.radians(k * 60 + 30 + spin)
        p = skia.Path()
        p.moveTo(x, y)
        p.lineTo(x + math.cos(ang - half) * r * fx, y + math.sin(ang - half) * r)
        p.lineTo(x + math.cos(ang + half) * r * fx, y + math.sin(ang + half) * r)
        p.close()
        c.drawPath(p, P(shade(col, 0.06 * math.cos(ang)), a))
        c.drawPath(p, P(FAB_EDGE, 0.7 * a, stroke=1.8))
    c.drawCircle(x, y, max(2.0, r * 0.12), P("#334155", a))


def glass_tower(c, cx, w, h, t, tint=0.0, glare=1.0, lit=0.0):
    """A round glass tower (no shades), base on GROUND."""
    top = GROUND - h
    cyl(c, cx - w / 2, top, w, h, mix(GLASSB, "#5B3A1E", tint))
    for k in range(1, int(h / 40)):
        yy = top + k * 40
        c.drawLine(cx - w / 2, yy, cx + w / 2, yy, P("#0F172A", 0.25, stroke=2))
    cap = skia.Path()
    cap.addOval(R(cx - w / 2, top - w * 0.18, w, w * 0.36))
    c.drawPath(cap, lin_paint(cx - w / 2, 0, cx + w / 2, 0, [shade(GLASSB, -0.3), shade(GLASSB, 0.25), shade(GLASSB, -0.4)]))
    if glare > 0 and tint < 1:                        # a hot white glare stripe
        c.drawRect(R(cx - w * 0.18, top, w * 0.1, h), P("#FFFFFF", 0.35 * glare * (1 - tint)))
        add_glow(c, cx - w * 0.13, top + h * 0.3, w * 0.5, "#FFFFFF", 0.25 * glare * (1 - tint))
    if lit > 0:
        rng = random.Random(int(cx))
        for k in range(1, int(h / 40)):
            for j in range(6):
                if rng.random() < 0.6:
                    xx = cx - w / 2 + 14 + j * (w - 28) / 6
                    c.drawRect(R(xx, top + k * 40 + 10, (w - 28) / 6 - 8, 16), P("#FFE2A8", 0.7 * lit))


def shaded_tower(c, cx, w, h, t, sun, storm=0.0, half=0.0, lit=0.0, shades=1.0, ncol=18, seed=0, open_all=None):
    """A round tower wrapped in umbrella shades. sun = the sun's direction in degrees (0 = towards us, +90 = from the
    right / east, -90 = from the left / west): shades facing it unfold. half 0..1 folds every shade to half (a storm);
    storm 0..1 makes them flap. open_all overrides the openness of every shade."""
    top = GROUND - h
    glass_tower(c, cx, w, h, t, glare=0.0, lit=lit)
    if shades <= 0:
        return
    r = math.pi * w / ncol * 0.62
    rows = int((h - 120) / (r * 1.55))
    items = []
    for i in range(rows):
        yy = top + 70 + i * r * 1.55
        for j in range(ncol):
            th = (j + 0.5 * (i % 2)) * 360.0 / ncol
            ct = math.cos(math.radians(th))
            if ct <= 0.06:
                continue
            items.append((ct, i, j, th, yy))
    for ct, i, j, th, yy in sorted(items):
        x = cx + (w / 2 + r * 0.35) * math.sin(math.radians(th))
        sunk = math.cos(math.radians(th - sun))
        o = smooth((sunk - 0.05) / 0.45)
        if open_all is not None:
            o = open_all
        o = lerp(o, 0.5, half)
        if storm > 0:
            o = clamp(o + storm * 0.22 * math.sin(t * 19 + i * 1.7 + j * 2.3))
        unit(c, x, yy, r * shades, o, fx=ct, lit=clamp(0.35 + 0.65 * max(0.0, sunk)), spin=storm * 6 * math.sin(t * 23 + i + j))
    for k, yy in enumerate((top + 40, GROUND - 60)):     # the rings at the top and bottom
        c.drawRect(R(cx - w / 2 - 6, yy - 6, w + 12, 12), P("#CBD5E1", 0.8))


def sky_and_city(c, t, pal=SKY, sun=None, sun_r=70, sea=True):
    vrect(c, 0, 0, W, GROUND, pal)
    if sun is not None:
        sx, sy = sun
        add_glow(c, sx, sy, sun_r * 5, "#FFF1C9", 0.55)
        c.drawCircle(sx, sy, sun_r, P("#FFF7DB"))
    rng = random.Random(4)
    for k in range(16):                               # a low skyline far away
        bx = k * 72 - 20
        bh = rng.uniform(90, 260)
        c.drawRect(R(bx, GROUND - 60 - bh, 60, bh), P(mix(pal[-1], "#1E3A5F", 0.55), 0.9))
    if sea:
        c.drawRect(R(0, GROUND - 60, W, 60), lin_paint(0, GROUND - 60, 0, GROUND, ["#1D4ED8", "#0E7490"]))
        for k in range(10):
            xx = (k * 130 + t * 30) % (W + 130) - 65
            c.drawLine(xx, GROUND - 40 + (k % 3) * 12, xx + 60, GROUND - 40 + (k % 3) * 12, P("#BAE6FD", 0.5, stroke=3))
    c.drawRect(R(0, GROUND, W, H - GROUND), lin_paint(0, GROUND, 0, H, ["#6B5B45", "#3F3428"]))


def palm(c, x, y, h, t, a=1.0):
    c.drawLine(x, y, x + 10, y - h, P("#78350F", a, stroke=12))
    for k in range(7):
        ang = math.radians(-160 + k * 23 + math.sin(t * 1.3 + k) * 3)
        c.drawLine(x + 10, y - h, x + 10 + math.cos(ang) * h * 0.45, y - h + math.sin(ang) * h * 0.25 + h * 0.08,
                   P("#166534", a, stroke=10))


def thermometer(c, x, y, h, k, a=1.0):
    """A thermometer standing at (x, y) (bottom bulb), filled to k."""
    c.drawRRect(rr(x - 22, y - h, 44, h, 22), P("#F8FAFC", 0.9 * a))
    c.drawRRect(rr(x - 10, y - 12 - (h - 30) * k, 20, (h - 30) * k + 12, 10), P(WARN, a))
    c.drawCircle(x, y, 34, P(WARN, a))
    c.drawCircle(x, y, 34, P("#F8FAFC", 0.9 * a, stroke=5))


def lattice_window(c, x, y, w, h, t, a=1.0):
    """A projecting wooden mashrabiya box (front view) with a turned-wood lattice."""
    c.drawRRect(rr(x - 16, y - 30, w + 32, h + 50, 10), lin_paint(x, 0, x + w, 0, ["#5B3416", "#8B5A2B", "#5B3416"], a=a))
    c.save()
    c.clipRect(R(x, y, w, h))
    c.drawRect(R(x, y, w, h), P("#2B1708", a))
    step = 26
    for gx in range(0, int(w) + step, step):
        for gy in range(0, int(h) + step, step):
            c.drawCircle(x + gx, y + gy, 7, P("#A0703F", a))
            c.drawLine(x + gx - 13, y + gy, x + gx + 13, y + gy, P("#8B5A2B", a, stroke=5))
            c.drawLine(x + gx, y + gy - 13, x + gx, y + gy + 13, P("#8B5A2B", a, stroke=5))
    c.restore()


def dappled(c, x, y, w, h, k, t, skew=0.0):
    """Little patches of sun on a floor: the mashrabiya's pattern."""
    if k <= 0:
        return
    for gx in range(0, int(w), 40):
        for gy in range(0, int(h), 30):
            px = x + gx + gy * skew
            c.drawOval(R(px, y + gy, 22, 12), P("#FDE68A", 0.55 * k))


def office_dark(c, t, lights=1.0):
    """Inside an office behind dark bronze glass at noon."""
    vrect(c, 0, 0, W, H, ["#1C1917", "#292524"])
    c.drawRect(R(60, 380, 960, 560), P("#3A2A1A"))   # the dark window wall: a bright day outside, brown through the glass
    for k in range(1, 4):
        c.drawLine(60 + k * 240, 380, 60 + k * 240, 940, P("#0C0A09", 1.0, stroke=10))
    rng = random.Random(3)
    for k in range(9):                                # the city outside, dull brown
        bx = 80 + k * 105
        bh = rng.uniform(160, 420)
        c.drawRect(R(bx, 940 - bh, 80, bh), P("#5C4128"))
    c.drawRect(R(60, 380, 960, 560), P("#000000", 0.25))
    c.drawRect(R(0, 300, W, 60), P("#111827"))       # the ceiling with lights
    for k in range(4):
        lx = 160 + k * 250
        c.drawRect(R(lx - 60, 350, 120, 14), P("#FEF9C3", lights))
        if lights > 0:
            light_cone(c, lx, 364, 90, 700, 40, "#FEF3C7", 0.18 * lights)
            add_glow(c, lx, 360, 120, "#FEF08A", 0.4 * lights)
    c.drawRect(R(0, 1130, W, H - 1130), P("#292524"))
    for k in range(3):                                # desks and people from behind
        dx = 220 + k * 320
        c.drawRect(R(dx - 120, 1010, 240, 20), P("#78716C"))
        c.drawRect(R(dx - 60, 920, 120, 80), P("#111827"))
        c.drawRect(R(dx - 52, 928, 104, 60), P("#38BDF8", 0.45))
        person(c, dx, 1180, 250, ["#F97316", "#0EA5E9", "#A855F7"][k], t + k, pose="sit", face=-1)


def old_house(c, t, sun_side=1.0, view_k=0.0):
    """An old house in a desert town by the sea: a room with a mashrabiya window. sun_side 1: the sun is on the screen
    (bright dapples), 0: the sun has gone round (the room is dim and the sea view cut into pieces)."""
    vrect(c, 0, 0, W, H, ["#3B2A1E", "#2A1D14"])
    wall = mix("#5A4634", "#C9A27A", 0.4 * sun_side)
    c.drawRect(R(0, 300, W, 900), P(wall))
    wx, wy, ww, wh = 300, 420, 480, 520
    c.save()                                          # the sea and sky behind the screen
    c.clipRect(R(wx, wy, ww, wh))
    vrect(c, wx, wy, ww, wh * 0.6, ["#1D4ED8", "#60A5FA"])
    c.drawRect(R(wx, wy + wh * 0.6, ww, wh * 0.4), P("#0E7490"))
    c.restore()
    lattice_window(c, wx, wy, ww, wh, t)
    c.drawRect(R(0, 1060, W, H - 1060), P(mix("#3B2A1E", "#7C5A3A", 0.5 * sun_side)))
    dappled(c, 200, 1080, 640, 120, sun_side, t, skew=0.4)
    if sun_side > 0:
        light_cone(c, 540, 700, 110, 560, 26, "#FDE68A", 0.14 * sun_side)
    if view_k > 0:                                    # someone peeking: the view comes in little pieces
        person(c, 860, 1180, 330, "#0EA5E9", t, pose="look", face=-1)
        c.drawRect(R(0, 0, W, H), P("#000000", 0.25 * view_k))


def actuator_unit(c, x, y, r, o, t, a=1.0):
    """One shade up close: the fabric panels on arms, the motor and its rod in the middle."""
    for k in range(6):
        ang = math.radians(k * 60 + 30)
        ex, ey = x + math.cos(ang) * r, y + math.sin(ang) * r
        c.drawLine(x, y, ex, ey, P("#94A3B8", a, stroke=8))
    unit(c, x, y, r, o, lit=1.0, a=a)
    c.drawCircle(x, y, r * 0.16, P("#1F2937", a))
    c.drawCircle(x, y, r * 0.16, P("#FACC15", a, stroke=6))
    push = lerp(0.2, 1.0, o)
    c.drawRRect(rr(x - 12, y - r * 0.16 - 60 * push, 24, 60 * push, 8), P("#64748B", a))
    add_glow(c, x, y, r * 0.4, "#FACC15", 0.3 * a)


def screen_sun(c, x, y, w, h, k, a=1.0):
    """A little computer screen: the sun's path across a day, a dot moving along it."""
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, 16), P("#0F172A", 0.92 * a))
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, 16), P("#38BDF8", a, stroke=4))
    pth = skia.Path()
    pth.moveTo(x - w * 0.4, y + h * 0.3)
    pth.quadTo(x, y - h * 0.6, x + w * 0.4, y + h * 0.3)
    c.drawPath(pth, P("#FDE68A", 0.7 * a, stroke=4))
    m = skia.PathMeasure(pth, False)
    pos, _ = m.getPosTan(m.getLength() * clamp(k))
    c.drawCircle(pos.x(), pos.y(), 16, P("#FDE047", a))
    add_glow(c, pos.x(), pos.y(), 50, "#FDE047", 0.6 * a)


def sandstorm(c, t, k=1.0):
    if k <= 0:
        return
    c.drawRect(R(0, 0, W, H), lin_paint(0, 300, 0, H, [("#C2884A", 0.0), ("#B07A3E", 0.55 * k), ("#8A5A2B", 0.75 * k)]))
    rng = random.Random(6)
    for i in range(70):
        u = (t * 1.3 + rng.random()) % 1.0
        y = rng.uniform(250, 1250)
        x = lerp(-120, W + 120, u)
        c.drawLine(x, y, x - 90, y + 6, P("#F5D0A0", 0.5 * k, stroke=3))


def anemometer(c, x, y, t, spin=1.0, a=1.0):
    """A weather mast with three spinning wind cups (top at (x, y))."""
    c.drawLine(x, y, x, y + 200, P("#CBD5E1", a, stroke=8))
    for k in range(3):
        ang = t * 14 * spin + k * 2.094
        ex, ey = x + math.cos(ang) * 70, y + math.sin(ang) * 18
        c.drawLine(x, y, ex, ey, P("#E5E7EB", a, stroke=5))
        c.drawCircle(ex, ey, 14, P("#F8FAFC", a))
    c.drawCircle(x, y, 9, P("#F59E0B", a))


def sunshade(c, x, y, s, t, fight=0.0, opened=0.0, a=1.0):
    """A car's round twisty sun shade. opened 0: twisted into a bundle of loops in your hands (fight shakes it);
    opened 1: sprung open into two big silver discs."""
    if opened < 1:                                    # the twisted bundle: three loops
        wob = math.sin(t * 11) * 16 * fight
        for k in range(3):
            c.save()
            c.translate(x + wob, y + (k - 1) * 18 * s)
            c.rotate(-20 + k * 25 + wob * 0.6)
            c.drawOval(R(-120 * s, -70 * s, 240 * s, 140 * s), P("#E2E8F0", 0.9 * a * (1 - opened)))
            c.drawOval(R(-120 * s, -70 * s, 240 * s, 140 * s), P("#334155", a * (1 - opened), stroke=9 * s))
            c.restore()
    if opened > 0:
        k = e_back(opened)
        for j, dx in enumerate((-215, 215)):
            c.save()
            c.translate(x + dx * k, y)
            c.scale(k, k)
            c.drawOval(R(-210, -170, 420, 340), lin_paint(-210, 0, 210, 0, ["#94A3B8", "#F8FAFC", "#CBD5E1", "#94A3B8"], a=a))
            for r_ in (60, 110, 160):
                c.drawOval(R(-r_ * 1.25, -r_, r_ * 2.5, r_ * 2), P("#94A3B8", 0.5 * a, stroke=3))
            c.drawOval(R(-210, -170, 420, 340), P("#1F2937", a, stroke=12))
            c.restore()


def car_inside(c, t):
    vrect(c, 0, 0, W, H, ["#0EA5E9", "#7DD3FC"])
    c.drawCircle(820, 420, 80, P("#FEF9C3"))
    add_glow(c, 820, 420, 300, "#FEF08A", 0.5)
    dash = skia.Path()                                # the windshield frame and dashboard
    dash.moveTo(0, 300)
    dash.lineTo(W, 300)
    dash.lineTo(W, 360)
    dash.lineTo(0, 360)
    dash.close()
    c.drawPath(dash, P("#111827"))
    c.drawRect(R(0, 960, W, H - 960), lin_paint(0, 960, 0, 1200, ["#1F2937", "#0B0F1A"]))
    c.drawCircle(300, 1060, 150, P("#111827", 1.0, stroke=26))     # steering wheel
    c.drawLine(300, 1060, 300, 1200, P("#111827", 1.0, stroke=24))


# ====================================================================================== the episode
class AlBahar(EpisodeV2):
    BUILD_NO = 102
    FIRST_SET = "towers"
    CLEAR = "#0B1530"
    TITLE = {"en": "AL BAHAR TOWERS", "ar_sa": "أبراج البحر"}
    EMPH = {"en": ["TOWERS", "ABU", "DHABI", "UMBRELLAS", "SUN", "DESERT", "BAKES", "GLASS", "HEAT", "STOP", "DARK",
                   "TINTED", "GLARE", "GLOOMY", "LIGHTS", "NOON", "MASHRABIYA", "ARAB", "WOODEN", "SCREEN", "FIXED",
                   "SHUT", "MOVE", "MOTOR", "COMPUTER", "SANDSTORM", "WIND", "SAILS", "SENSORS", "ROOF", "HALFWAY",
                   "STORM", "FOLLOW", "BUBBLE", "WRAP", "WALLPAPER", "HALF", "CLEAR", "TWO", "THOUSAND", "CONGRATS",
                   "YOURSELF", "FOLD", "SHADE"],
            "ar_sa": ["أبراج", "أبوظبي", "مظلاتها", "الشمس", "الصحرا", "أفران", "الحر", "غامق", "الوهج", "كئيب",
                      "الأنوار", "الظهر", "المشربية", "خشب", "ثابتة", "تتحرك", "موتور", "وكمبيوتر", "العجاج",
                      "أشرعة", "حساسات", "السطح", "لنصها", "متابعة", "الفقاعات", "جدران", "نص", "شفاف", "برجين",
                      "ألفين", "مبروك", "لحالها", "تتهاوش", "تطويها"]}
    KEYS = {"ar_sa": {
        ("hook", "TOWERS"): "أبراج", ("hook", "UMBRELLAS"): "مظلاتها", ("hook", "SUN"): "الشمس",
        ("break1", "DESERT"): "الصحرا", ("break1", "OFFICES"): "مكاتب", ("break1", "HEAT"): "الحر",
        ("fix1", "DARK"): "غامق", ("fix1", "GLARE"): "الوهج",
        ("break2", "GLOOMY"): "كئيب", ("break2", "LIGHTS"): "الأنوار", ("break2", "NOON"): "الظهر",
        ("fix2", "BORROWED"): "أخذوا", ("fix2", "MASHRABIYA"): "المشربية", ("fix2", "SCREEN"): "شباك",
        ("break3", "FIXED"): "ثابتة", ("break3", "SUN"): "راحت",
        ("fix3", "MOVE"): "تتحرك", ("fix3", "MOTOR"): "موتور", ("fix3", "COMPUTER"): "وكمبيوتر",
        ("break4", "SANDSTORM"): "العجاج", ("break4", "SAILS"): "أشرعة",
        ("fix4", "SENSORS"): "حساسات", ("fix4", "HALFWAY"): "لنصها", ("fix4", "STORM"): "العاصفة",
        ("cta", "FOLLOW"): "متابعة", ("cta", "BUBBLE"): "الفقاعات",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "HALF"): "نص", ("reveal", "CLEAR"): "شفاف",
        ("stat", "TWO"): "برجين", ("stat", "THOUSAND"): "ألفين", ("stat", "COMPUTER"): "وكمبيوتر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TWO"): "ألفين", ("tag", "FOLD"): "تتسكر", ("tag", "SHADE"): "تطويها"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: bubble wrap"),
                   "stat": [("2", "TOWERS"), ("2,098", "SUN SHADES"), ("50%", "LESS SUN HEAT")],
                   "L": {"umbrellas": "THEY OPEN IN THE SUN", "oven": "GLASS IN THE DESERT = OVEN",
                         "how": "HOW MUCH HEAT CAN THEY STOP?", "tint": "DARK TINTED GLASS", "glare": "GLARE GONE!",
                         "gloomy": "GLOOMY... LIGHTS ON AT NOON", "mash": "THE MASHRABIYA", "old": "AN OLD ARAB SCREEN",
                         "fixed": "A FIXED SCREEN STAYS SHUT", "move": "THESE ONES MOVE!", "motor": "A MOTOR IN EACH ONE",
                         "track": "A COMPUTER TRACKS THE SUN", "storm": "SANDSTORM!", "sails": "LIKE SAILS!",
                         "sensors": "SENSORS ON THE ROOF", "halfway": "FOLDED HALFWAY", "half": "ABOUT HALF THE HEAT",
                         "clear": "CLEAR GLASS", "heat": "SUN HEAT", "name": "AL BAHAR TOWERS", "nope": "NOPE.",
                         "fold": "2,000 FOLD BY THEMSELVES"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: نايلون الفقاعات"),
                      "stat": [("2", "برجين"), ("2,098", "مظلة"), ("50%", "أقل حر شمس")],
                      "L": {"umbrellas": "تفتح مع الشمس", "oven": "زجاج في الصحرا = فرن",
                            "how": "كم توقف من الحر؟", "tint": "زجاج غامق", "glare": "راح الوهج!",
                            "gloomy": "كئيب... والأنوار شغالة الظهر", "mash": "المشربية", "old": "شباك خشب عربي قديم",
                            "fixed": "المشربية العادية ثابتة", "move": "هذي تتحرك!", "motor": "موتور في كل مظلة",
                            "track": "كمبيوتر يلحق الشمس", "storm": "عجاج!", "sails": "تصير أشرعة!",
                            "sensors": "حساسات فوق السطح", "halfway": "تتسكر لنصها", "half": "تقريباً نص الحر",
                            "clear": "زجاج شفاف", "heat": "حر الشمس", "name": "أبراج البحر", "nope": "لا والله",
                            "fold": "ألفين تتسكر لحالها"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "towers": ("hook", "TOWERS", 0.2), "umbrellas": ("hook", "UMBRELLAS", 0.55), "sun0": ("hook", "SUN", 0.85),
            "desert": ("break1", "DESERT", 0.05), "offices": ("break1", "OFFICES", 0.3), "heat1": ("break1", "HEAT", 0.75),
            "dark": ("fix1", "DARK", 0.4), "glare": ("fix1", "GLARE", 0.8),
            "gloomy": ("break2", "GLOOMY", 0.3), "lights": ("break2", "LIGHTS", 0.6), "noon": ("break2", "NOON", 0.9),
            "borrowed": ("fix2", "BORROWED", 0.15), "mash": ("fix2", "MASHRABIYA", 0.4), "screen": ("fix2", "SCREEN", 0.85),
            "fixed": ("break3", "FIXED", 0.2), "moves": ("break3", "SUN", 0.7),
            "move": ("fix3", "MOVE", 0.1), "motor": ("fix3", "MOTOR", 0.45), "computer": ("fix3", "COMPUTER", 0.75),
            "sandstorm": ("break4", "SANDSTORM", 0.35), "sails": ("break4", "SAILS", 0.85),
            "sensors": ("fix4", "SENSORS", 0.15), "halfway": ("fix4", "HALFWAY", 0.55), "storm": ("fix4", "STORM", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "answer": ("reveal", "ANSWER", 0.05), "half": ("reveal", "HALF", 0.3), "clear": ("reveal", "CLEAR", 0.85),
            "s1": ("stat", "TWO", 0.05), "s2": ("stat", "THOUSAND", 0.35), "s3": ("stat", "COMPUTER", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_two": ("tag", "TWO", 0.05), "t_fold": ("tag", "FOLD", 0.3), "t_shade": ("tag", "SHADE", 0.85)})
        T["oven1"] = max(T["offices"], T["desert"]) + 0.2
        T["tint1"] = max(T["glare"], T["dark"]) + 0.1
        T["gloom1"] = max(T["gloomy"], s("break2") + 0.3) + 0.1
        T["mash1"] = max(T["screen"], T["mash"]) + 0.1
        T["fixed1"] = max(T["fixed"], s("break3") + 0.2) + 0.2
        T["track1"] = max(T["computer"], T["motor"]) + 0.2
        T["storm1"] = max(T["sandstorm"], s("break4") + 0.2) + 0.1
        T["half1"] = max(T["halfway"], T["sensors"]) + 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "city", 1)
        self.cut(s("break2") - 0.12, "office", -1)
        self.cut(s("fix2") - 0.12, "lattice", 1)
        self.cut(s("fix3") - 0.12, "unit", -1)
        self.cut(s("break4") - 0.12, "storm", 1)
        self.cut(s("cta") - 0.12, "towers", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        self.spans = [(T["oven1"], T["tint1"]), (T["gloom1"], T["mash1"]), (T["fixed1"], T["track1"]), (T["storm1"], T["half1"])]
        self.shakes = [(T["umbrellas"], 0.3, 5), (T["oven1"], 0.3, 5), (T["gloom1"], 0.3, 5), (T["fixed1"], 0.3, 5),
                       (T["storm1"], 0.6, 10), (s("closer") + 0.2, 0.35, 6), (T["t_shade"], 0.3, 7)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: towers (hook, cta .. closer)
    def draw_towers(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        cam = (540, GROUND, 1.0)
        if ph == "hook":
            sun = lerp(100, 40, prog(t, 0.0, T["sun0"] + 0.6))
            sky_and_city(c, t, sun=(990, lerp(640, 430, prog(t, 0.0, T["sun0"] + 0.6))))
            k = e_io(prog(t, T["towers"] - 0.6, T["sun0"]))
            cam = (lerp(790, 540, k), lerp(700, GROUND, k), lerp(2.3, 1.0, k))
            z = 1.0
        elif ph == "closer":
            sun = -40
            sky_and_city(c, t, pal=DUSK, sun=(180, 900), sun_r=60)
            z = 1.0
        else:
            sun = 30
            sky_and_city(c, t, sun=(985, 430))
            z = 1.0
        c.save()
        c.translate(540, GROUND)
        c.scale(z * cam[2], z * cam[2])
        c.translate(-cam[0], -cam[1])
        lit = 1.0 if ph == "closer" else 0.0
        shaded_tower(c, 310, 330, 860, t, sun, lit=lit, seed=1)
        shaded_tower(c, 730, 330, 860, t + 0.4, sun, lit=lit, seed=2)
        for k, px in enumerate((90, 560, 1010)):
            palm(c, px, GROUND + 20, 170, t + k)
        c.restore()
        if ph == "reveal":                            # the sun's heat: half stopped by the shades
            k = prog(t, T["half"] - 0.3, T["half"] + 0.4)
            big_arrow_l(c, 900, 420, 640, 760, 90, "#FB923C", 0.9 * k)
            big_arrow_l(c, 640, 760, 500, 900, 46, "#FDBA74", 0.8 * prog(t, T["half"], T["half"] + 0.5))
            c.drawRRect(rr(140, 420, 60, 300, 30), P("#0B1220", 0.8 * k))
            hk = lerp(1.0, 0.5, prog(t, T["half"], T["half"] + 0.6))
            c.drawRRect(rr(148, 428 + 284 * (1 - hk), 44, 284 * hk, 22), P("#F97316", k))

    def ui_towers(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "umbrellas", T["umbrellas"] - 0.1, s("break1") + 0.1, accent=HILITE, size=50)
        elif ph == "reveal":
            self.chip(540, 300, "half", T["half"] - 0.1, T["clear"] - 0.1, accent="#FDBA74", size=50)
            self.chip(540, 300, "clear", T["clear"] - 0.1, s("stat") - 0.15, accent=GOOD, size=52)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: city (break1, fix1)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        sky_and_city(c, t, pal=["#1E5FA8", "#4C93D6", "#A9D3F2"], sun=(800, 380), sun_r=90)
        tint = prog(t, T["dark"] - 0.2, T["dark"] + 0.5) if ph == "fix1" else 0.0
        for k, (cx, w, h) in enumerate(((210, 230, 760), (540, 270, 880), (870, 230, 700))):
            glass_tower(c, cx, w, h, t, tint=tint, glare=1.0 - tint)
        heat = prog(t, s("break1"), T["heat1"]) * (1 - 0.7 * tint)
        rng = random.Random(2)
        for k in range(22):                           # heat shimmer
            u = (t * 0.6 + rng.random()) % 1.0
            x = rng.uniform(60, 1020)
            pth = skia.Path()
            y0 = lerp(1180, 600, u)
            pth.moveTo(x, y0)
            for j in range(1, 7):
                pth.lineTo(x + math.sin(t * 3 + j + k) * 10, y0 - j * 16)
            c.drawPath(pth, P("#FDE68A", 0.4 * heat * (1 - u), stroke=4))
        if ph == "break1":
            thermometer(c, 980, 1120, 360, lerp(0.3, 0.95, prog(t, s("break1"), T["heat1"])))

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "oven", T["offices"] - 0.2, T["heat1"] - 0.4, accent=WARN, size=44)
            self.chip(540, 300, "how", T["heat1"] - 0.4, s("fix1") - 0.1, accent=HILITE, size=44)
            self.badge("alert", T["oven1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["oven1"], 1.2)
        else:
            self.chip(540, 300, "tint", T["dark"] - 0.2, T["glare"] - 0.1, accent="#D6A770", size=50)
            self.chip(540, 300, "glare", T["glare"] - 0.1, s("break2") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["tint1"], s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: office (break2)
    def draw_office(self, c, t):
        T = self.T
        office_dark(c, t, lights=prog(t, T["lights"] - 0.3, T["lights"] + 0.1))

    def ui_office(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 260, "gloomy", T["gloomy"] - 0.1, s("fix2") - 0.15, accent=WARN, size=44)
        self.badge("alert", T["gloom1"], s("fix2") - 0.2, x=920, y=440)
        self.red(T["gloom1"], 1.2)

    # ------------------------------------------------------------------ set: lattice (fix2, break3)
    def draw_lattice(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "fix2":
            old_house(c, t, sun_side=prog(t, T["mash"] - 0.4, T["mash"] + 0.3))
        else:
            old_house(c, t, sun_side=1 - prog(t, T["fixed"], T["moves"] + 0.3), view_k=prog(t, T["moves"], T["moves"] + 0.5))

    def ui_lattice(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix2":
            self.chip(540, 300, "mash", T["mash"] - 0.2, T["screen"] - 0.1, accent="#D6A770", size=54)
            self.chip(540, 300, "old", T["screen"] - 0.1, s("break3") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["mash1"], s("break3") - 0.15, x=920, y=440)
        else:
            self.chip(540, 300, "fixed", T["fixed"] - 0.2, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["fixed1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["fixed1"], 1.2)

    # ------------------------------------------------------------------ set: unit (fix3)
    def draw_unit(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B3B7A", "#1765B0"])
        k = prog(t, T["computer"] - 0.2, T["computer"] + 0.6)
        if k < 1:                                     # one shade up close, its motor pushing it open
            o = smooth(prog(t, T["move"], T["motor"] + 0.4))
            cyl(c, 0, 440, W, 760, GLASSB)
            actuator_unit(c, 540, 800, 330 * (1 - 0.5 * k), o, t, a=1 - k)
        if k > 0:                                     # a field of shades following the sun on a screen
            sunk = prog(t, T["computer"], s("break4") - 0.2)
            cyl(c, 0, 600, W, 640, GLASSB)
            for i in range(5):
                for j in range(7):
                    x = 120 + j * 140 + (70 if i % 2 else 0)
                    y = 680 + i * 120
                    face = (x - 540) / 540
                    sun = lerp(-1.0, 1.0, sunk)
                    o = smooth(1 - abs(face - sun) * 1.4)
                    unit(c, x, y, 62, o, lit=0.4 + 0.6 * o, a=k)
            screen_sun(c, 540, 470, 380, 190, sunk, a=k)

    def ui_unit(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "move", T["move"] - 0.1, T["motor"] - 0.1, accent=HILITE, size=54)
        self.chip(540, 300, "motor", T["motor"] - 0.1, T["computer"] - 0.1, accent="#FACC15", size=48)
        self.chip(540, 300, "track", T["computer"] - 0.1, s("break4") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["track1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: storm (break4, fix4)
    def draw_storm(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        sky_and_city(c, t, pal=["#7C5A3A", "#A0754A", "#C9A06A"], sea=False)
        if ph == "break4":
            st = prog(t, s("break4"), T["sandstorm"] + 0.3)
            shaded_tower(c, 540, 420, 900, t, 20, storm=st)
            sandstorm(c, t, st)
        else:
            hf = prog(t, T["halfway"] - 0.3, T["halfway"] + 0.4)
            calm = prog(t, T["storm"], T["storm"] + 0.6)
            shaded_tower(c, 540, 420, 900, t, 20, storm=(1 - hf) * 0.7, half=hf)
            sandstorm(c, t, 1 - 0.7 * calm)
            ink = prog(t, T["sensors"] - 0.3, T["sensors"] + 0.2)
            if ink > 0:                               # an inset: the wind cups on the roof mast
                c.drawLine(540, GROUND - 900, 820, 640, P("#F8FAFC", 0.8 * ink, stroke=4))
                c.save()
                c.translate(860, 560)
                c.scale(e_back(ink), e_back(ink))
                c.drawCircle(0, 0, 150, P("#0B1220", 0.85))
                c.drawCircle(0, 0, 150, P("#FACC15", 1.0, stroke=6))
                c.save()
                c.clipPath(skia.Path().addCircle(0, 0, 146), skia.ClipOp.kIntersect, True)
                anemometer(c, 0, -40, t, spin=1 - 0.6 * calm)
                c.restore()
                c.restore()

    def ui_storm(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "storm", T["sandstorm"] - 0.2, T["sails"] - 0.1, accent=WARN, size=56)
            self.chip(540, 300, "sails", T["sails"] - 0.1, s("fix4") - 0.15, accent=WARN, size=54)
            self.badge("alert", T["storm1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["storm1"], 1.2)
        else:
            self.chip(540, 300, "sensors", T["sensors"] - 0.2, T["halfway"] - 0.1, accent="#FACC15", size=48)
            self.chip(540, 300, "halfway", T["halfway"] - 0.1, s("cta") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["half1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        car_inside(c, t)
        fight = prog(t, T["t_fold"], T["t_fold"] + 0.4)
        pop = prog(t, T["t_shade"] - 0.1, T["t_shade"] + 0.25)
        person(c, 800, 1250, 440, "#F97316", t, pose="shrug" if pop > 0.5 else "carry", face=-1)
        sunshade(c, 560, 700, 1.0, t, fight=fight * (1 - pop), opened=pop)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "fold", T["t_two"] - 0.1, T["t_shade"] - 0.15, accent="#F8FAFC", size=46)
        self.chip(540, 300, "nope", T["t_shade"] - 0.15, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, SKY)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["towers"], sfx.riser(1.0, 62), -12),
              (T["umbrellas"], sfx.sparkle(1.0, 12, 63), -8), (T["sun0"], sfx.ding(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["oven1"], sfx.sizzle(1.2, 65), -10),
               (T["oven1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["dark"], sfx.power_down(0.8, 66), -10), (T["tint1"], sfx.ding(), -8), (T["tint1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, False, 67), -6), (T["lights"], sfx.click(68), -4),
               (T["lights"] + 0.1, sfx.hum(1.2, 110.0), -16), (T["gloom1"] + 0.3, sfx.womp(), -10)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.45, True, 69), -6), (T["mash1"], sfx.ding(), -8), (T["mash1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["fixed1"], sfx.thud(0.3, 70), -6), (T["fixed1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, False, 71), -6), (T["motor"], sfx.whirr(1.0, 150.0, 260.0, 72), -10),
               (T["track1"], sfx.ding(), -8), (T["track1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 73), -6), (T["sandstorm"], rumble(2.0, 74), -10),
               (T["storm1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["sensors"], sfx.whirr(0.8, 300.0, 420.0, 75), -12), (T["halfway"], sfx.lock_click(76), -6),
               (T["half1"], sfx.ding(), -8), (T["half1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["half"], sfx.riser(0.8, 95), -12),
               (T["clear"], sfx.sparkle(0.8, 10, 96), -8)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_fold"], sfx.creak(0.8, 104), -8),
               (T["t_shade"], sfx.snap(105), -4), (T["t_shade"] + 0.3, sfx.womp(), -8)]
        return ev


def big_arrow_l(c, x0, y0, x1, y1, w, col, a):
    """A fat arrow from (x0, y0) to (x1, y1)."""
    if a <= 0:
        return
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    L = math.hypot(x1 - x0, y1 - y0)
    c.save()
    c.translate(x0, y0)
    c.rotate(ang)
    p = skia.Path()
    p.moveTo(0, -w / 2)
    p.lineTo(L - w, -w / 2)
    p.lineTo(L - w, -w)
    p.lineTo(L, 0)
    p.lineTo(L - w, w)
    p.lineTo(L - w, w / 2)
    p.lineTo(0, w / 2)
    p.close()
    c.drawPath(p, P(col, a))
    c.restore()


NAME = "albahar"
EPISODE = AlBahar
