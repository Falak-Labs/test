"""Episode 30 - A self-cooling stadium.  v2 look: a desert stadium cut open, a close-up of the stands, whip cuts.

Sets: bowl (the stadium cut in half in the desert: cool blue air inside an open roof for the hook; the sun bakes the
stands, then the roof shades them and the light paint bounces the sun; the hot wind pours in, then the roof edge
curves like a wing and a bubble of cool air stays inside; the power bill of chilling all day, then water chilled at
night and stored in a tank, the used air pulled back and cooled again; the reveal: the switch two hours early, the
gates open; the stat and the cheer), stands (a close-up of the rows: forty thousand fans warm it up like laptops,
then cold air from a grille under every seat and big nozzles by the pitch; the tag: the one fan who is cold).
The pitch is y = 0 and the stadium is centred on x = 0.
"""
from v2_base import *  # noqa: F401,F403

MAROON = "#8D1B3D"
SAND = ("#B07A42", "#7A5230", "#4A3020", "#24170D")
ICE = "#7DD3FC"
DAYSKY = {"top": "#0B1A4A", "upper": "#1E3A7A", "mid": "#6B4A8E", "low": "#D9775A", "horizon": "#FFB066",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
TIERS, TREAD, RISE = 7, 66.0, 75.0          # the stands: 7 tiers, from x = 430 out to 892, up to y = TOP
SX0 = 430.0
TOP = -TIERS * RISE


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def stands_path(side):
    """One side's stands (side -1 left, 1 right), stepped, closed down to the ground."""
    p = skia.Path()
    p.moveTo(side * SX0, 0)
    x, y = side * SX0, 0.0
    for i in range(TIERS):
        y -= RISE
        p.lineTo(x, y)
        x += side * TREAD
        p.lineTo(x, y)
    p.lineTo(side * 960, y)
    p.lineTo(side * 960, 0)
    p.close()
    return p


def roof_path(side, inner, wing):
    """The roof over one side: from the outer wall's top to the inner edge at x = side * inner.  wing 0..1 rounds
    the inner edge up like a wing's leading edge."""
    p = skia.Path()
    p.moveTo(side * 1000, TOP + 20)
    p.cubicTo(side * 980, TOP - 160, side * (inner + 260), TOP - 290, side * (inner + 40), TOP - 280 - 24 * wing)
    p.cubicTo(side * (inner - 34 * wing), TOP - 276 - 34 * wing, side * (inner - 30 * wing), TOP - 222, side * inner, TOP - 232)
    p.cubicTo(side * (inner + 200), TOP - 250, side * 900, TOP - 160, side * 930, TOP)
    p.close()
    return p


def fans_on_stands(c, side, t, k, rng_seed=5, heat=0.0, cheer=0.0):
    """Little heads on every tier."""
    if k <= 0:
        return
    rng = random.Random(rng_seed + (side > 0))
    cols = ("#F8FAFC", MAROON, "#FACC15", "#38BDF8", "#F472B6", "#22C55E")
    for i in range(TIERS):
        y = -(i + 1) * RISE
        x0 = side * (SX0 + i * TREAD)
        for j in range(3):
            x = x0 + side * (12 + j * 20)
            col = rng.choice(cols)
            bob = abs(math.sin(t * 7 + i + j * 2)) * 8 * cheer
            c.drawRRect(rr(x - 7, y - 26 - bob, 14, 22, 5), P(col, k))
            c.drawCircle(x, y - 32 - bob, 7, P("#C68B5E" if (i + j) % 3 else "#E8B48A", k))
            if heat > 0 and (i + j) % 2 == 0:
                c.drawCircle(x, y - 32 - bob, 9, P(WARN, 0.35 * heat * k, stroke=2))


def thermo(c, x, y, temp, a=1.0, label=""):
    """A thermometer (screen space): temp in degrees C, scale 15..50."""
    if a <= 0:
        return
    h = 360
    v = clamp((temp - 15) / 35.0)
    col = mix(ICE, WARN, clamp((temp - 22) / 20.0))
    c.save()
    c.translate(x, y)
    k = e_back(clamp(a * 1.3))
    c.scale(k, k)
    c.drawRRect(rr(-44, -h - 30, 88, h + 110, 44), P("#000000", 0.4, blur=14))
    c.drawRRect(rr(-44, -h - 30, 88, h + 110, 44), P("#0F172A", 0.92))
    c.drawRRect(rr(-14, -h, 28, h, 14), P("#334155"))
    c.drawRRect(rr(-14, -h * v, 28, h * v, 14), P(col))
    c.drawCircle(0, 30, 34, P(col))
    add_glow(c, 0, 30, 70, col, 0.5)
    for i in range(8):
        yy = -h + i * h / 7
        c.drawLine(18, yy, 30, yy, P("#94A3B8", 0.8, stroke=3))
    c.restore()
    text(c, f"{int(round(temp))}°C", x, y + 120, 44, "#FFFFFF", "Poppins-Black", a=a)
    if label:
        word(c, label, x, y - h - 50, 26, "#CBD5E1", a)


def laptop(c, x, y, s, a=1.0, glow=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-30, -40, 60, 40, 4), P("#1F2937", a))
    c.drawRRect(rr(-26, -36, 52, 32, 3), P(mix("#60A5FA", "#F97316", glow), a))
    c.drawRRect(rr(-38, 0, 76, 8, 3), P("#9CA3AF", a))
    if glow > 0:
        add_glow(c, 0, -20, 50, "#F97316", 0.5 * glow * a)
    c.restore()


def tank(c, x, y, w, h, fill, t, a=1.0):
    """A big insulated cold-water tank standing on (x, y)."""
    c.drawRRect(rr(x - w / 2, y - h, w, h, 30), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#94A3B8", "#E2E8F0", "#94A3B8"], a=a))
    c.save()
    c.clipRRect(rr(x - w / 2 + 16, y - h + 16, w - 32, h - 32, 20), skia.ClipOp.kIntersect, True)
    c.drawRect(R(x - w / 2, y - h, w, h), P("#0F172A", a))
    lv = clamp(fill)
    wy = y - 16 - (h - 32) * lv
    path = skia.Path()
    path.moveTo(x - w / 2, wy)
    for xx in range(int(x - w / 2), int(x + w / 2) + 10, 10):
        path.lineTo(xx, wy + math.sin(xx * 0.05 + t * 3) * 5)
    path.lineTo(x + w / 2, y)
    path.lineTo(x - w / 2, y)
    path.close()
    c.drawPath(path, lin_paint(0, wy, 0, y, ["#7DD3FC", "#0EA5E9", "#0369A1"], a=a))
    c.restore()
    for k in range(4):
        c.drawLine(x - w / 2, y - h * (k + 1) / 5, x + w / 2, y - h * (k + 1) / 5, P("#64748B", 0.5 * a, stroke=3))


def chiller(c, x, y, t, work, a=1.0):
    """A chiller plant on the ground at (x, y): a box with two big fans on top; work 0..1 spins and heats it."""
    box(c, x - 160, y - 150, 320, 150, "#64748B", r=10, a=a)
    for k in range(5):
        c.drawRect(R(x - 140 + k * 60, y - 120, 30, 90), P("#334155", a))
    for fx in (x - 80, x + 80):
        c.drawOval(R(fx - 60, y - 170, 120, 30), P("#1E293B", a))
        ang = t * (2 + 30 * work)
        for b in range(3):
            q = ang + b * 2.094
            c.drawLine(fx, y - 155, fx + math.cos(q) * 54, y - 155 + math.sin(q) * 10, P("#94A3B8", a, stroke=6))
    if work > 0.3:
        add_glow(c, x, y - 80, 200, WARN, 0.4 * (work - 0.3) * a)


def nozzle(c, x, y, s, a=1.0):
    """A big round air nozzle by the pitch, pointing left, mouth at (x, y)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(0, -46, 150, 92, 30), lin_paint(0, -46, 0, 46, ["#E2E8F0", "#94A3B8", "#475569"], a=a))
    c.drawOval(R(-16, -46, 34, 92), P("#334155", a))
    c.drawOval(R(-10, -34, 22, 68), P("#0F172A", a))
    c.drawRect(R(120, 46, 24, 140), P("#475569", a))
    c.restore()


def puff_air(c, x, y, t, t0, dirx, diry, length, col=ICE, a=1.0, n=6, w=10, seed=0):
    """Moving air streaks from (x, y) along (dirx, diry)."""
    if a <= 0 or t < t0:
        return
    rng = random.Random(seed)
    for i in range(n):
        u = ((t - t0) * 1.6 + i / n + rng.uniform(0, 0.2)) % 1.0
        d = u * length
        off = math.sin(i * 2.1) * w * 1.5
        px_, py_ = x + dirx * d - diry * off, y + diry * d + dirx * off
        c.drawLine(px_, py_, px_ + dirx * 40, py_ + diry * 40, P(col, a * (1 - u) * 0.9, stroke=w * (1 - 0.5 * u)))


def jacket_guy(c, x, y, h, t, shiver, a=1.0):
    """A fan in a puffy jacket and a beanie, sitting, shaking with cold."""
    j = math.sin(t * 60) * 3 * shiver
    person(c, x + j, y, h, "#2563EB", t, pose="sit", face=1, hat="beanie", a=a)
    u = h / 140.0
    c.drawRRect(rr(x + j - 24 * u, y - 108 * u, 48 * u, 56 * u, 16 * u), P("#1D4ED8", a))      # the puffy jacket
    for k in range(3):
        c.drawLine(x + j - 22 * u, y - (100 - k * 16) * u, x + j + 22 * u, y - (100 - k * 16) * u, P("#3B82F6", a, stroke=3))
    c.drawRRect(rr(x + j - 22 * u, y - 116 * u, 44 * u, 12 * u, 6 * u), P("#DC2626", a))       # scarf


def mom(c, x, y, h, t, a=1.0):
    """A mother in the stands, with a headscarf, pointing."""
    person(c, x, y, h, "#7C3AED", t, pose="point", face=-1, hat="none", hair="#3F2A1A", a=a)
    u = h / 140.0
    sc = skia.Path()
    sc.addCircle(x, y - 132 * u, 21 * u)
    c.drawPath(sc, P("#16A34A", a))
    c.drawCircle(x - 4 * u, y - 128 * u, 12 * u, P("#E8B48A", a))
    c.drawRRect(rr(x - 20 * u, y - 116 * u, 40 * u, 16 * u, 8 * u), P("#16A34A", a))


def bubble(c, x, y, s, p):
    """A speech bubble (screen space) whose tail points down."""
    if p <= 0:
        return
    size = 40
    w = (arabic.width_ar(s, size * 1.15) if arabic.is_ar(s) else text_width(s, size, "Poppins-Black")) + 70
    c.save()
    c.translate(x, y)
    k = e_back(clamp(p * 1.2))
    c.scale(k, k)
    c.drawRRect(rr(-w / 2, -54, w, 108, 44), P("#000000", 0.35, blur=12))
    c.drawRRect(rr(-w / 2, -54, w, 108, 44), P("#FFFFFF"))
    tail = skia.Path()
    tail.moveTo(-30, 44)
    tail.lineTo(-10, 100)
    tail.lineTo(20, 46)
    tail.close()
    c.drawPath(tail, P("#FFFFFF"))
    word(c, s, 0, 14, size, "#0F172A")
    c.restore()


def lever(c, x, y, on, a=1.0, label="ON"):
    """A big switch panel (screen space) centred on (x, y): on 0..1 throws the handle up."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    k = e_back(clamp(a * 1.3))
    c.scale(k, k)
    c.drawRRect(rr(-130, -150, 260, 300, 30), P("#000000", 0.4, blur=14))
    c.drawRRect(rr(-130, -150, 260, 300, 30), P("#1E293B"))
    c.drawRRect(rr(-130, -150, 260, 300, 30), P("#64748B", 1, stroke=4))
    c.drawRRect(rr(-30, -100, 60, 200, 30), P("#0F172A"))
    tipx, tipy = 0, lerp(80, -80, e_back(clamp(on)))
    c.drawLine(0, 0, tipx, tipy, P("#CBD5E1", 1, stroke=18))
    c.drawCircle(tipx, tipy, 30, P(GOOD if on > 0.5 else WARN))
    c.drawCircle(0, 0, 16, P("#475569"))
    word(c, label, 0, 135, 30, GOOD if on > 0.5 else "#94A3B8")
    c.restore()


def sunglasses(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for sx in (-1, 1):
        c.drawRRect(rr(sx * 46 - 34, -22, 68, 44, 18), P("#0F172A", a))
        c.drawRRect(rr(sx * 46 - 26, -16, 20, 10, 5), P("#FFFFFF", 0.35 * a))
    c.drawLine(-12, -8, 12, -8, P("#0F172A", a, stroke=8))
    c.restore()


# ---------------------------------------------------------------------------------------------- sounds
def wind_snd(d=2.0, seed=70):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 200, 900)
    env = np.sin(np.linspace(0, np.pi, n)) * (0.7 + 0.3 * np.sin(np.linspace(0, 9, n)))
    return sfx._norm(x * env, 0.55)


def blow_snd(d=1.6, seed=71):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 900, 5000)
    return sfx._norm(x * sfx._ar(n, 0.15, 0.4), 0.45)


def crowd_snd(d=2.4, seed=72):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 250, 2500)
    return sfx._norm(x * np.sin(np.linspace(0, np.pi, n)) ** 0.5, 0.5)


def brr_snd(d=0.8, seed=73):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * 180 * tt) * (np.sin(2 * np.pi * 28 * tt) > 0) * 0.5
    return sfx._norm(x * sfx._ar(n, 0.02, 0.2), 0.4)


# ====================================================================================== the episode
class Stadium(EpisodeV2):
    BUILD_NO = 30
    COVER_T = ("closer", 0.9)                    # cover: the cool bubble in the desert, after the cheer rings
    FIRST_SET = "bowl"
    CLEAR = "#070B1F"
    TITLE = {"en": "SELF-COOLING STADIUM", "ar_sa": "استاد بيبرّد نفسه"}
    EMPH = {"en": ["CONGRATS", "STADIUM", "DESERT", "COLD", "ROOF", "OPEN", "SELF-COOLING", "SUN", "BAKES", "STANDS",
                   "OVEN", "SHADES", "SEATS", "PAINT", "LIGHT", "BOUNCES", "HOT", "WIND", "POURS", "CURVE", "EDGE",
                   "AIRPLANE", "WING", "SLIDES", "COOL", "STAYS", "INSIDE", "FORTY", "THOUSAND", "FANS", "HEAT",
                   "EIGHTY", "LAPTOPS", "GRILLE", "SEAT", "NOZZLES", "PITCH", "ONLY", "PEOPLE", "CHILLING", "DAY",
                   "BURNS", "POWER", "WATER", "NIGHT", "SAVE", "MATCH", "USED", "AGAIN", "FOLLOW", "TURBINE", "SWITCH",
                   "TWO", "HOURS", "DOCTOR", "QATAR", "GATES", "TWENTY-ONE", "DEGREES", "SEVEN", "WORLD", "CUP",
                   "YOURSELF", "JACKET", "AC", "DOWN!"],
            "ar_sa": ["مبروك", "استاد", "الصحرا", "مفتوح", "ساقع", "بيبرّد", "شمس", "المدرجات", "فرن", "يضلل",
                      "الكراسي", "وتدهنه", "فاتح", "الشمس", "السخن", "فهوا", "بيدخل", "فتقوّس", "جناح", "الطيارة",
                      "يعدي", "والساقع", "جوه", "ضل", "أربعين", "مشجع", "حرارة", "تمانين", "لابتوب", "كرسي", "فتحات",
                      "الملعب", "الناس", "تبريد", "كهربا", "مية", "بالليل", "وتخزنها", "وترجّع", "تابعني", "توربينة",
                      "شغّله", "بساعتين", "دكتور", "كول", "قطر", "البوابات", "واحد", "درجة", "وسبع", "بإيدك", "أمك",
                      "اقفل", "التكييف", "برد"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "STADIUM"): "استاد", ("hook", "DESERT"): "الصحرا", ("hook", "COLD"): "ساقع", ("hook", "ROOF"): "سقفه",
        ("hook", "OPEN"): "مفتوح", ("hook", "CONGRATS"): "مبروك", ("hook", "SELF"): "بيبرد",
        ("break1", "SUN"): "شمس", ("break1", "BAKES"): "بتخلي", ("break1", "STANDS"): "المدرجات", ("break1", "OVEN"): "فرن",
        ("fix1", "ROOF"): "السقف", ("fix1", "SHADES"): "يضلل", ("fix1", "SEATS"): "الكراسي", ("fix1", "PAINT"): "وتدهنه",
        ("fix1", "LIGHT"): "فاتح", ("fix1", "BOUNCES"): "يرجع", ("fix1", "AWAY"): "الشمس",
        ("break2", "OPEN"): "مفتوح", ("break2", "HOT"): "السخن", ("break2", "WIND"): "فهوا", ("break2", "POURS"): "بيدخل",
        ("break2", "TOP"): "فوق",
        ("fix2", "CURVE"): "فتقوس", ("fix2", "EDGE"): "حرف", ("fix2", "AIRPLANE"): "الطيارة", ("fix2", "WING"): "جناح",
        ("fix2", "SLIDES"): "يعدي", ("fix2", "COOL"): "والساقع", ("fix2", "STAYS"): "يفضل", ("fix2", "INSIDE"): "جوه",
        ("break3", "SHADED"): "ضل", ("break3", "FORTY"): "أربعين", ("break3", "FANS"): "مشجع", ("break3", "HEAT"): "حرارة",
        ("break3", "EIGHTY"): "تمانين", ("break3", "LAPTOPS"): "لابتوب",
        ("fix3", "COLD"): "ساقع", ("fix3", "GRILLE"): "تحت", ("fix3", "SEAT"): "كرسي", ("fix3", "NOZZLES"): "فتحات",
        ("fix3", "PITCH"): "الملعب", ("fix3", "ONLY"): "مكان", ("fix3", "PEOPLE"): "الناس",
        ("break4", "COOL"): "ساقع", ("break4", "CHILLING"): "تبريد", ("break4", "DAY"): "اليوم", ("break4", "BURNS"): "بياكل",
        ("break4", "POWER"): "كهربا",
        ("fix4", "WATER"): "مية", ("fix4", "NIGHT"): "بالليل", ("fix4", "SAVE"): "وتخزنها", ("fix4", "MATCH"): "للماتش",
        ("fix4", "PULL"): "وترجع", ("fix4", "USED"): "الهوا", ("fix4", "BACK"): "تنضفه", ("fix4", "AGAIN"): "تاني",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "SWITCH"): "شغله", ("reveal", "TWO"): "بساعتين", ("reveal", "HOURS"): "بساعتين",
        ("reveal", "PROFESSOR"): "دكتور", ("reveal", "DOCTOR"): "دكتور", ("reveal", "QATAR"): "قطر",
        ("reveal", "GATES"): "البوابات",
        ("stat", "TWENTY"): "واحد", ("stat", "FORTY"): "أربعين", ("stat", "SEVEN"): "سبع",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "AFTER"): "وبعد", ("tag", "GUY"): "أمك", ("tag", "JACKET"): "المدرج", ("tag", "YELLING"): "تقولك",
        ("tag", "TURN"): "اقفل", ("tag", "DOWN"): "برد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a wind turbine"),
                   "stat": [("21°C", "ON THE PITCH"), ("40,000", "FANS"), ("7", "COOLED STADIUMS")],
                   "L": {"stadium": "YOUR SELF-COOLING STADIUM", "open": "ROOF WIDE OPEN", "outside": "OUTSIDE",
                         "inside": "INSIDE", "oven": "LIKE AN OVEN", "shade": "SHADE", "paint": "LIGHT PAINT",
                         "bounce": "BOUNCES THE SUN", "wind": "HOT DESERT WIND", "pours": "POURS IN",
                         "wing": "SHAPED LIKE A WING", "slides": "WIND SLIDES OVER", "bubble": "COOL AIR STAYS INSIDE",
                         "fans": "40,000 FANS", "laptops": "= 80,000 LAPTOPS", "grille": "A GRILLE UNDER EVERY SEAT",
                         "nozzle": "BIG NOZZLES", "only": "ONLY WHERE PEOPLE ARE", "power": "CRAZY POWER",
                         "night": "CHILLED AT NIGHT", "tank": "STORED COLD WATER", "loop": "USED AIR COOLED AGAIN",
                         "switch": "ON", "early": "2 HOURS EARLY", "doc": "DOCTOR COOL", "gates": "GATES OPEN",
                         "yell": "TURN THE AC DOWN!", "cold": "TOO COLD"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: توربينة رياح"),
                      "stat": [("21°", "درجة في الملعب"), ("40,000", "مشجع"), ("7", "استادات متبردة")],
                      "L": {"stadium": "الاستاد بتاعك", "open": "السقف مفتوح", "outside": "برة",
                            "inside": "جوه", "oven": "فرن", "shade": "ضل", "paint": "لون فاتح",
                            "bounce": "بيرجّع الشمس", "wind": "هوا الصحرا السخن", "pours": "بيدخل جوه",
                            "wing": "زي جناح الطيارة", "slides": "الهوا بيعدي من فوق", "bubble": "الساقع يفضل جوه",
                            "fans": "40,000 مشجع", "laptops": "= 80,000 لابتوب", "grille": "فتحة تحت كل كرسي",
                            "nozzle": "فتحات كبيرة", "only": "مكان الناس بس", "power": "بياكل كهربا",
                            "night": "اتبردت بالليل", "tank": "مية ساقعة متخزنة", "loop": "الهوا بيرجع يتبرد",
                            "switch": "شغّال", "early": "قبل الماتش بساعتين", "doc": "دكتور كول",
                            "gates": "البوابات اتفتحت", "yell": "اقفل التكييف ده، هتاخد برد!", "cold": "ساقع أوي"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stadium": ("hook", "STADIUM", 0.1), "desert": ("hook", "DESERT", 0.25), "cold": ("hook", "COLD", 0.4),
            "roof": ("hook", "ROOF", 0.55), "open": ("hook", "OPEN", 0.62), "congrats": ("hook", "CONGRATS", 0.7),
            "self": ("hook", "SELF", 0.9),
            "sun": ("break1", "SUN", 0.2), "bakes": ("break1", "BAKES", 0.4), "stands": ("break1", "STANDS", 0.6),
            "oven": ("break1", "OVEN", 0.9),
            "roof1": ("fix1", "ROOF", 0.1), "shades": ("fix1", "SHADES", 0.2), "seats": ("fix1", "SEATS", 0.35),
            "paint": ("fix1", "PAINT", 0.5), "light": ("fix1", "LIGHT", 0.65), "bounces": ("fix1", "BOUNCES", 0.8),
            "away": ("fix1", "AWAY", 0.95),
            "open2": ("break2", "OPEN", 0.2), "hot": ("break2", "HOT", 0.4), "wind": ("break2", "WIND", 0.55),
            "pours": ("break2", "POURS", 0.7), "top": ("break2", "TOP", 0.95),
            "curve": ("fix2", "CURVE", 0.1), "edge": ("fix2", "EDGE", 0.2), "airplane": ("fix2", "AIRPLANE", 0.3),
            "wing": ("fix2", "WING", 0.4), "slides": ("fix2", "SLIDES", 0.6), "cool2": ("fix2", "COOL", 0.75),
            "stays": ("fix2", "STAYS", 0.85), "inside": ("fix2", "INSIDE", 0.95),
            "shaded": ("break3", "SHADED", 0.1), "forty": ("break3", "FORTY", 0.3), "fans": ("break3", "FANS", 0.45),
            "heat": ("break3", "HEAT", 0.6), "eighty": ("break3", "EIGHTY", 0.75), "laptops": ("break3", "LAPTOPS", 0.95),
            "cold3": ("fix3", "COLD", 0.1), "grille": ("fix3", "GRILLE", 0.3), "seat": ("fix3", "SEAT", 0.4),
            "nozzles": ("fix3", "NOZZLES", 0.6), "pitch": ("fix3", "PITCH", 0.7), "only": ("fix3", "ONLY", 0.8),
            "people": ("fix3", "PEOPLE", 0.95),
            "cool4": ("break4", "COOL", 0.15), "chilling": ("break4", "CHILLING", 0.35), "day": ("break4", "DAY", 0.6),
            "burns": ("break4", "BURNS", 0.75), "power": ("break4", "POWER", 0.95),
            "water": ("fix4", "WATER", 0.15), "night": ("fix4", "NIGHT", 0.25), "save": ("fix4", "SAVE", 0.4),
            "match": ("fix4", "MATCH", 0.5), "pull": ("fix4", "PULL", 0.62), "used": ("fix4", "USED", 0.72),
            "back": ("fix4", "BACK", 0.82), "again": ("fix4", "AGAIN", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "switch": ("reveal", "SWITCH", 0.1), "two": ("reveal", "TWO", 0.2), "hours": ("reveal", "HOURS", 0.3),
            "prof": ("reveal", "PROFESSOR", 0.5), "doc": ("reveal", "DOCTOR", 0.6), "qatar": ("reveal", "QATAR", 0.75),
            "gates": ("reveal", "GATES", 0.95),
            "s1": ("stat", "TWENTY", 0.04), "s2": ("stat", "FORTY", 0.4), "s3": ("stat", "SEVEN", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "after": ("tag", "AFTER", 0.1), "guy": ("tag", "GUY", 0.4), "jacket": ("tag", "JACKET", 0.55),
            "yelling": ("tag", "YELLING", 0.7), "turn": ("tag", "TURN", 0.8), "down": ("tag", "DOWN", 0.95)})
        T["wing0"] = min(T["curve"], T["edge"]) - 0.1                         # fix2: the roof edge curls up
        T["night0"] = min(T["water"], T["night"]) - 0.2                       # fix4: night falls
        T["day0"] = max(T["match"], T["save"] + 0.4) - 0.2                    # fix4: back to match day
        T["loop0"] = min(T["pull"], T["used"]) - 0.1
        T["bub"] = min(T["guy"], T["yelling"]) - 0.2                          # tag: the complaint
        # ---- sets
        self.cut(s("break1") - 0.12, "bowl", 1)
        self.cut(s("fix1") - 0.12, "bowl", -1)
        self.cut(s("break2") - 0.12, "bowl", 1)
        self.cut(s("fix2") - 0.12, "bowl", -1)
        self.cut(s("break3") - 0.12, "stands", 1)
        self.cut(s("fix3") - 0.12, "stands", -1)
        self.cut(s("break4") - 0.12, "bowl", 1)
        self.cut(s("fix4") - 0.12, "bowl", -1)
        self.cut(s("tag") - 0.2, "stands", 1)
        self.cams = {"bowl": Camera(0, -470, 0.56), "stands": Camera(40, -230, 1.05)}
        cm = self.cams["bowl"]
        cm.key(0.1, 0, -460, 0.57, max(1.0, T["roof"] - 0.3)).key(T["roof"] - 0.2, 0, -520, 0.64, 1.0)
        cm.key(T["self"] - 0.4, 0, -470, 0.56, 1.0)
        cm.key(s("break1") - 0.12, -420, -330, 0.8, 0.0).key(s("break1"), -440, -320, 0.84, 3.0)
        cm.key(s("fix1") - 0.12, -460, -380, 0.74, 0.0).key(s("fix1"), -440, -400, 0.72, 4.0)
        cm.key(s("break2") - 0.12, -300, -560, 0.6, 0.0).key(s("break2"), -280, -570, 0.62, 3.5)
        cm.key(s("fix2") - 0.12, -150, -580, 0.58, 0.0).key(s("fix2"), -120, -570, 0.57, 4.0)
        cm.key(s("break4") - 0.12, 700, -400, 0.52, 0.0).key(s("break4"), 720, -390, 0.53, 3.5)
        cm.key(s("fix4") - 0.12, 700, -400, 0.52, 0.0).key(s("fix4"), 680, -410, 0.52, 4.0)
        cm.key(s("cta") - 0.12, 0, -470, 0.56, 0.0)
        cm.key(s("reveal"), 0, -440, 0.56, 3.0)
        cm.key(s("stat") - 0.3, 0, -300, 0.58, 1.2)
        cm.key(s("closer") - 0.2, 0, -320, 0.6, 1.0)
        self.cams["stands"].key(s("break3"), 60, -240, 1.08, 4.0)
        self.cams["stands"].key(s("fix3") - 0.12, 0, -230, 1.0, 0.0).key(s("fix3"), -40, -220, 1.0, 4.0)
        self.cams["stands"].key(s("tag") - 0.2, 120, -300, 1.2, 0.0).key(s("tag"), 140, -310, 1.25, 3.0)
        # ---- tracks
        self.shade = Track(0.0).to(T["shades"] - 0.2, 1.0, 0.9)                   # roof shades the seats
        self.paint = Track(0.0).to(T["paint"] - 0.1, 1.0, max(0.6, T["light"] - T["paint"] + 0.3))
        self.wing = Track(0.0).to(T["wing0"], 1.0, max(0.8, T["wing"] - T["wing0"] + 0.4))
        self.night = Track(0.0).to(T["night0"], 1.0, 0.8).to(T["day0"], 0.0, 0.8)
        self.fill = Track(0.0).to(T["night0"] + 0.3, 1.0, max(0.8, T["day0"] - T["night0"] - 0.2))
        self.fill.to(T["day0"] + 0.4, 0.55, 2.4)
        self.temp = Track(21.0).to(s("break1") - 0.12, 30.0, 0.0).to(T["bakes"] - 0.2, 47.0, 1.6)
        self.temp.to(s("fix1") - 0.12, 47.0, 0.0).to(T["shades"], 38.0, 2.0)
        self.temp.to(s("break2") - 0.12, 38.0, 0.0).to(T["pours"] - 0.2, 44.0, 1.2)
        self.temp.to(s("fix2") - 0.12, 44.0, 0.0).to(T["slides"], 31.0, 2.0)
        self.temp.to(s("fix3") - 0.12, 36.0, 0.0).to(T["seat"], 21.0, 2.2)
        self.temp.to(s("cta") - 0.12, 21.0, 0.0)
        self.spans = [(T["oven"], T["away"] + 0.3), (T["pours"], T["inside"] + 0.3),
                      (T["laptops"], T["people"] + 0.3), (T["power"], T["again"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["oven"], 0.3, 6), (T["pours"], 0.4, 8), (T["laptops"], 0.3, 6),
                       (T["power"], 0.4, 8), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(30)
        self.dunes = [(rng.uniform(-3000, 3000), rng.uniform(200, 520), rng.uniform(60, 150)) for _ in range(14)]
        self.walkers = [(rng.uniform(0, 1), rng.choice(("#F8FAFC", MAROON, "#FACC15", "#38BDF8"))) for _ in range(16)]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ the bowl
    def sky_and_desert(self, c, t, cam, night=0.0):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        pal = {k: mix(DAYSKY[k], v2.NIGHT[k], night) for k in DAYSKY}
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=gy - 40 * z)
        if night > 0:
            v2.stars(c, W, H, t, night)
            v2.moon(c, 860, gy - 1100 * z ** 0.3, 60, a=night)
        sx, sy = 170 - cx * 0.05, gy - 560                                                # the desert sun, low and hot
        if night < 1:
            add_glow(c, sx, sy, 260, "#FFB347", 0.55 * (1 - night))
            c.drawCircle(sx, sy, 92, P("#FFD27A", 0.95 * (1 - night)))
            c.drawCircle(sx, sy, 70, P("#FFF1C9", 0.95 * (1 - night)))
        c.save()
        c.translate(W / 2 - cx * 0.08 * z, gy - 30 * z)
        v2.ridge(c, -1600, 1600, 0, 200, mix("#E2A65F", "#3A2E4A", night), mix("#C9884A", "#2A2238", night), seed=6, step=160, rough=0.4)
        c.restore()
        return gy, (sx, sy)

    def draw_bowl(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["bowl"].at(t)
        cx, cy, z = cam
        night = self.night.at(t) if s("fix4") - 0.12 <= t < s("cta") - 0.12 else 0.0
        gy, sun = self.sky_and_desert(c, t, cam, night)
        self.view(c, cam)
        x0, x1 = cx - 600 / z, cx + 600 / z
        vrect(c, x0, 0, x1 - x0, 2400, [mix(SAND[1], "#3A2E4A", night), mix(SAND[2], "#2A2238", night), SAND[3], "#2A1A0C"], [0, 0.1, 0.4, 1])
        for dx_, dy_, dh in self.dunes:
            c.drawOval(R(dx_ - 300, dy_ * 0.2 - dh * 0.2, 600, dh * 0.4), P(mix(SAND[0], "#4A3A5A", night), 0.35))
        # phase of the story
        hook = t < s("break1") - 0.12
        b1 = s("break1") - 0.12 <= t < s("fix1") - 0.12
        f1 = s("fix1") - 0.12 <= t < s("break2") - 0.12
        b2 = s("break2") - 0.12 <= t < s("fix2") - 0.12
        f2 = s("fix2") - 0.12 <= t < s("break3") - 0.12
        b4 = s("break4") - 0.12 <= t < s("fix4") - 0.12
        f4 = s("fix4") - 0.12 <= t < s("cta") - 0.12
        late = t >= s("cta") - 0.12
        shade = 0.0 if b1 else self.shade.at(t) if f1 else 1.0
        paint = 0.0 if b1 else self.paint.at(t) if f1 else 1.0
        wing = 0.0 if (b1 or f1 or b2) else self.wing.at(t) if f2 else 1.0
        cool = 1.0 if (hook or late or b4 or f4) else 0.0
        if f2:
            cool = prog(t, T["cool2"] - 0.3, T["stays"] + 0.2)
        if t >= s("reveal") - 0.12 and t < s("stat") - 0.12:
            cool = prog(t, T["switch"], T["hours"] + 1.0)
        heat = self.temp_heat(t)
        inner = lerp(760, 560, shade)
        if heat > 0:
            c.drawRect(R(-960, TOP - 300, 1920, -TOP + 300), lin_paint(0, TOP - 300, 0, 0, [(WARN, 0.0), ("#F97316", 0.28 * heat)]))
        # the pitch
        c.drawRect(R(-430, -8, 860, 14), P("#15803D"))
        for k in range(8):
            c.drawRect(R(-430 + k * 107.5, -8, 54, 14), P("#22C55E", 0.5))
        for gx in (-420, 420):
            c.drawRect(R(gx - 4, -54, 8, 50), P("#FFFFFF"))
        for k, (px_, col) in enumerate(((-200, MAROON), (-60, "#F8FAFC"), (90, MAROON), (250, "#F8FAFC"))):
            jx = px_ + math.sin(t * 1.3 + k) * 40
            person(c, jx, -6, 70, col, t + k, pose="walk", face=1 if k % 2 else -1)
        c.drawCircle(math.sin(t * 1.1) * 160, -14, 8, P("#FFFFFF"))
        # stands, concourse, fans
        for side in (-1, 1):
            base = mix("#6B7280", "#B45309", heat * 0.6)
            c.drawPath(stands_path(side), lin_paint(0, -420, 0, 0, [shade_c(base, 0.15), base, shade_c(base, -0.35)]))
            for i in range(TIERS):
                y = -(i + 1) * RISE
                x0_ = side * (SX0 + i * TREAD)
                c.drawLine(x0_, y, x0_ + side * TREAD, y, P(MAROON, 1, stroke=6))
            cheer = 1.0 if t >= s("closer") - 0.1 else 0.0
            fans_on_stands(c, side, t, 1.0, heat=heat, cheer=cheer)
            if shade > 0:                                                                # the roof's shade
                c.save()
                c.clipPath(stands_path(side), skia.ClipOp.kIntersect, True)
                c.drawRect(R(-1000, -700, 2000, 700), lin_paint(0, -700, 0, 0, [("#0B1020", 0.5 * shade), ("#0B1020", 0.25 * shade)]))
                c.restore()
            wall = mix("#8B5A2B", "#F5F0E6", paint)                                      # the outer shell
            sh = skia.Path()
            sh.moveTo(side * 1010, 0)
            sh.lineTo(side * 1000, TOP + 20)
            sh.lineTo(side * 960, TOP)
            sh.lineTo(side * 960, 0)
            sh.close()
            c.drawPath(sh, P(wall))
            for k in range(7):
                c.drawLine(side * 962, -40 - k * 70, side * 1006, -40 - k * 70, P(shade_c(wall, -0.2), 1, stroke=4))
            gk = prog(t, T["gates"] - 0.3, T["gates"] + 0.3) if (s("reveal") - 0.12 <= t < s("stat") - 0.12) else (1.0 if t >= s("stat") - 0.12 else 0.0)
            gx0 = 760 if side > 0 else -820                                                 # the gate under the stands
            c.drawRRect(rr(gx0, -130, 60, 130, 10), P(mix("#1F2937", "#FDE68A", gk)))
            if gk > 0:
                add_glow(c, side * 790, -65, 120, "#FDE68A", 0.6 * gk)
                for k, (u0, col) in enumerate(self.walkers):                              # fans walking in
                    u = (t * 0.45 + u0) % 1.0
                    person(c, side * lerp(1250, 800, u), 0, 90, col, t + k, pose="walk", face=-side, a=gk * min(1.0, (1 - u) * 5))
            rp = roof_path(side, inner, wing)
            c.drawPath(rp, lin_paint(0, TOP - 300, 0, TOP, [mix("#D6D3D1", "#FFFFFF", paint), mix("#78716C", "#CBD5E1", paint)]))
            c.drawPath(rp, P("#1E293B", 0.8, stroke=5))
        if cool > 0:                                                                     # the bubble of cool air
            bub = skia.Path()
            ry = -TOP + 150 + 40 * cool
            bub.addOval(R(-930, -ry, 1860, 2 * ry))
            c.save()
            c.clipRect(R(-1000, -1400, 2000, 1400))
            c.drawPath(bub, lin_paint(0, -ry, 0, 0, [("#60A5FA", 0.10 * cool), ("#38BDF8", 0.30 * cool), ("#0EA5E9", 0.42 * cool)]))
            c.drawPath(bub, P("#BAE6FD", 0.55 * cool, stroke=6))
            c.restore()
            for k in range(14):                                                        # little snow sparkles
                u = (t * 0.25 + k * 0.071) % 1.0
                fx_ = -760 + (k * 137) % 1520
                fy_ = -60 - u * (-TOP + 80)
                c.drawCircle(fx_, fy_, 6, P("#F0F9FF", 0.85 * cool * math.sin(u * math.pi)))
        if heat > 0:                                                                     # heat shimmer over the stands
            for side in (-1, 1):
                for k in range(6):
                    u = (t * 0.7 + k / 6) % 1.0
                    hx_ = side * (SX0 + 60 + k * 70)
                    hy_ = -(k + 1) * RISE - 40 - u * 220
                    path = skia.Path()
                    path.moveTo(hx_, hy_)
                    for q in range(7):
                        path.lineTo(hx_ + math.sin(q * 1.3 + t * 6 + k) * 10, hy_ - q * 16)
                    c.drawPath(path, P("#FFEDD5", 0.75 * heat * math.sin(u * math.pi), stroke=7))
        # the sun's rays (break1 / fix1)
        if b1 or f1:
            rk = 1.0 if b1 else 1 - 0.6 * shade
            for k in range(6):
                xs = -980 + k * 240
                c.drawLine(xs - 600, -1600, xs + 160, TOP + 100, P("#FDE68A", 0.35 * rk, stroke=10))
            if f1 and paint > 0:
                for k in range(3):                                                       # bounced off the light walls
                    bx, by = -1004, -120 - k * 140
                    c.drawLine(bx - 10, by - 10, bx - 260 * paint, by - 200 * paint, P("#FFF7DA", 0.9 * paint, stroke=8))
                    add_glow(c, bx, by, 40, "#FFF7DA", 0.6 * paint)
        # wind (break2 / fix2)
        if b2 or f2:
            self.wind(c, t, b2, wing)
        # break4 / fix4: the chiller, power and the tank
        if b4 or f4:
            work = prog(t, T["chilling"] - 0.2, T["burns"]) if b4 else (1.0 if night > 0.5 else 0.15)
            chiller(c, 1290, 0, t, work)
            if b4:
                for k in range(5):                                                      # power pouring in
                    u = ((t * 1.8 + k / 5) % 1.0)
                    c.drawLine(2000, -1100, 1360, -175, P("#475569", 1, stroke=8))
                    bx, by = lerp(2000, 1360, u), lerp(-1100, -175, u)
                    add_glow(c, bx, by, 60, HILITE, 0.8 * work)
            fill = self.fill.at(t) if f4 else 0.0
            tank(c, 1620, 0, 240, 560, fill, t)
            if f4:
                c.drawLine(1500, -60, 1010, -60, P("#0EA5E9", 1, stroke=18))
                if t >= T["day0"]:
                    for k in range(5):
                        u = ((t * 1.2 + k / 5) % 1.0)
                        c.drawCircle(lerp(1500, 1010, u), -60, 9, P("#E0F2FE"))
                if t >= T["loop0"]:                                                     # used air, back and around
                    lk = prog(t, T["loop0"], T["loop0"] + 0.5)
                    for side in (-1, 1):
                        path = skia.Path()
                        path.moveTo(side * 480, -140)
                        path.cubicTo(side * 620, TOP - 40, side * 900, TOP - 20, side * 930, -160)
                        path.cubicTo(side * 930, -40, side * 600, -30, side * 500, -70)
                        c.drawPath(path, dash_paint(ICE, 0.95 * lk, w=10, t=t * 2, dash=26, gap=18))
        if t >= T["cong2"]:                                                              # fireworks for the cheer
            for k in range(4):
                v2.shock_ring(c, -620 + k * 410, TOP - 520 - (k % 2) * 160, t, T["cong2"] + 0.2 * k, 0.9, r1=230,
                              col=("#FDE68A", "#F472B6", "#7DD3FC", "#A7F3D0")[k], width=10, squash=1.0)
        c.restore()
        self.ui["cam"] = cam
        self.ui["inner"] = inner
        self.ui["sun"] = sun

    def temp_heat(self, t):
        s = self.tl.s
        if s("break1") - 0.12 <= t < s("fix2") + 3.0:
            return clamp((self.temp.at(t) - 24) / 22.0)
        return 0.0

    def wind(self, c, t, bad, wing):
        """Hot desert wind from the left: it dives into the open roof (bad) or slides over the wing-shaped edge."""
        for k in range(4):
            y0 = TOP - 160 - k * 80
            path = skia.Path()
            path.moveTo(-2200, y0)
            if bad:
                path.cubicTo(-1300, y0, -1100, y0 - 160, -800, TOP - 300 - k * 20)
                path.cubicTo(-500, TOP - 360, -300, TOP - 80 + k * 40, -200 + k * 60, TOP + 160 + k * 30)
                path.cubicTo(-100 + k * 60, -150, 150, -260, 120 - k * 40, TOP + 80)
            else:
                lift = 150 * wing
                path.cubicTo(-1300, y0, -1100, y0 - 160 - lift * 0.5, -800, TOP - 320 - k * 30 - lift)
                path.cubicTo(-300, TOP - 360 - k * 30 - lift, 300, TOP - 360 - k * 30 - lift, 800, TOP - 320 - k * 30 - lift)
                path.cubicTo(1100, y0 - 160, 1300, y0, 2200, y0)
            col = "#FB923C" if bad else mix("#FB923C", "#FDE68A", wing)
            c.drawPath(path, dash_paint(col, 0.9, w=12, t=t * 3 + k, dash=60, gap=40))

    def ui_bowl(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            v2.chip(c, 760, 560, f"{self.L['outside']} 46°C", self.span(T["desert"] - 0.1, s("break1") + 0.2), accent=WARN, size=36)
            x1, y1 = self.at(0, -200)
            v2.chip(c, 540, y1, f"{self.L['inside']} 21°C", self.span(T["cold"] - 0.1, s("break1") + 0.2), accent=ICE, size=40)
            x0, y0 = self.at(0, TOP - 240)
            self.label(x0, y0, 540, 470, "open", T["roof"] - 0.1, T["self"] - 0.3, ICE, size=32)
            self.chip(540, 470, "stadium", T["self"] - 0.15, s("break1") + 0.2, accent=HILITE, size=36)
            return
        temp = self.temp.at(tw)
        if tw < s("fix1") - 0.12:
            thermo(c, 920, 760, temp, self.span(s("break1"), s("break2") - 0.15), self.L["inside"])
            self.chip(540, 470, "oven", T["oven"] - 0.1, s("fix1") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["oven"] + 0.2, s("fix1") - 0.2, x=880, y=330)
            self.red(T["oven"] + 0.2, 1.8)
            return
        if tw < s("break2") - 0.12:
            thermo(c, 920, 760, temp, self.span(s("break1"), s("break2") - 0.15), self.L["inside"])
            x0, y0 = self.at(-700, TOP - 240)
            self.label(x0, y0, 300, 600, "shade", T["shades"] - 0.1, T["paint"] - 0.1, "#CBD5E1", size=34)
            x1, y1 = self.at(-1004, -260)
            self.label(x1, y1, 330, 620, "paint", T["paint"], T["bounces"] - 0.1, "#FFF7DA", size=34)
            self.chip(540, 470, "bounce", T["bounces"] - 0.15, s("break2") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["away"] + 0.1, s("break2") - 0.15, x=880, y=330)
            return
        if tw < s("fix2") - 0.12:
            thermo(c, 920, 760, temp, self.span(s("break2"), s("break3") - 0.15), self.L["inside"])
            self.chip(540, 470, "wind", T["wind"] - 0.15, T["pours"] - 0.1, accent="#FB923C", size=40)
            self.chip(540, 470, "pours", T["pours"] - 0.05, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["pours"] + 0.2, s("fix2") - 0.2, x=880, y=330)
            self.red(T["pours"] + 0.2, 1.8)
            return
        if tw < s("break3") - 0.12:
            thermo(c, 920, 760, temp, self.span(s("break2"), s("break3") - 0.15), self.L["inside"])
            inner = self.ui.get("inner", 560)
            x0, y0 = self.at(-inner - 30, TOP - 280)
            self.label(x0, y0, 300, 600, "wing", T["wing0"] + 0.2, T["slides"], HILITE, size=34)
            self.chip(540, 470, "slides", T["slides"] - 0.1, T["cool2"] - 0.1, accent="#FDE68A", size=38)
            self.chip(540, 470, "bubble", T["cool2"] - 0.05, s("break3") - 0.15, accent=ICE, size=38)
            self.badge("check", T["inside"] + 0.1, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix4") - 0.12 and tw >= s("break4") - 0.12:
            pw = prog(tw, T["chilling"], T["power"])
            self.chip(540, 470, "power", T["burns"] - 0.1, s("fix4") - 0.15, accent=WARN, size=44)
            x0, y0 = self.at(1290, -170)
            self.label(x0, y0, 330, 640, "power", T["chilling"], T["burns"] - 0.2, HILITE, size=32)
            self.badge("alert", T["power"] + 0.2, s("fix4") - 0.2, x=880, y=330)
            self.red(T["power"] + 0.2, 1.8)
            return
        if tw < s("cta") - 0.12:
            x0, y0 = self.at(1620, -560)
            self.label(x0, y0, 760, 600, "night", T["night"] - 0.1, T["day0"], "#A5B4FC", size=32)
            self.label(x0, y0, 760, 600, "tank", T["day0"] + 0.1, T["loop0"], ICE, size=32)
            self.chip(540, 470, "loop", T["loop0"] + 0.2, s("cta") - 0.15, accent=ICE, size=38)
            self.badge("check", T["again"] + 0.1, s("cta") - 0.15, x=880, y=330)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.15:
            lever(c, 230, 620, prog(tw, T["switch"] - 0.1, T["switch"] + 0.3), self.span(s("reveal") - 0.1, s("stat") - 0.2),
                  self.L["switch"])
            self.chip(700, 500, "early", T["two"] - 0.1, s("stat") - 0.2, accent=HILITE, size=34)
            k = self.span(T["doc"] - 0.2, s("stat") - 0.2, 0.3, 0.2)
            if k > 0:
                v2.chip(c, 700, 690, self.L["doc"], k, accent=ICE, size=40)
                sunglasses(c, 700, 610, 0.9 * e_back(clamp(k * 1.3)), k)
            x0, y0 = self.at(790, -130)
            self.label(x0, y0, 820, 1100, "gates", T["gates"] - 0.1, s("stat") - 0.2, GOOD, size=32)

    # ------------------------------------------------------------------ set: the stands up close (break3, fix3, tag)
    def row(self, i):
        return -360 + i * 170, -i * 105

    def draw_stands(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["stands"].at(t)
        cx, cy, z = cam
        tag = t >= s("tag") - 0.2
        fixed = s("fix3") - 0.12 <= t and not tag
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2A5A", "#22346B", "#101A3A"]))
        add_glow(c, 300, 300, 600, "#FDE68A", 0.18)
        self.view(c, cam)
        c.drawRect(R(-1400, 0, 900, 900), P("#15803D"))                                  # the pitch
        for k in range(6):
            c.drawRect(R(-1400 + k * 150, 0, 75, 900), P("#22C55E", 0.4))
        c.drawRect(R(-1400, -2, 900, 4), P("#FFFFFF", 0.8))
        rows = 6
        steps = skia.Path()
        steps.moveTo(-500, 0)
        for i in range(rows):
            x, y = self.row(i)
            steps.lineTo(x - 60, y)
            steps.lineTo(x - 60, y - 105)
            steps.lineTo(x + 110, y - 105)
        steps.lineTo(1400, -rows * 105)
        steps.lineTo(1400, 1200)
        steps.lineTo(-500, 1200)
        steps.close()
        heat = 0.0 if fixed or tag else prog(t, T["fans"] - 0.2, T["heat"] + 0.3)
        c.drawPath(steps, lin_paint(0, -700, 0, 300, [mix("#6B7280", "#B45309", heat * 0.5), "#4B5563", "#1F2937"]))
        rng = random.Random(9)
        shirts = ("#F8FAFC", MAROON, "#FACC15", "#38BDF8", "#F472B6", "#22C55E", "#FB923C")
        for i in range(rows):
            x, y = self.row(i)
            for j in range(2):
                sx = x - 20 + j * 0
                if j == 1:
                    continue
                c.drawRRect(rr(sx - 10, y - 150, 70, 18, 6), P(MAROON))                    # the seat
                c.drawRRect(rr(sx + 40, y - 230, 18, 98, 6), P(MAROON))
                c.drawRRect(rr(sx - 20, y - 132, 22, 26, 4), P("#0F172A"))                 # the grille
                for g in range(3):
                    c.drawLine(sx - 17, y - 127 + g * 8, sx - 1, y - 127 + g * 8, P("#64748B", 1, stroke=2))
                special = tag and i == 2
                if special:
                    if self.rtl:
                        mom(c, sx + 20, y - 132, 150, t)
                    else:
                        jacket_guy(c, sx + 20, y - 132, 150, t, prog(t, T["jacket"] - 0.2, T["jacket"] + 0.3))
                else:
                    cheer = "cheer" if (tag and (i + int(t * 2)) % 3 == 0) else "sit"
                    person(c, sx + 20, y - 132, 150, rng.choice(shirts), t + i, pose=cheer if cheer == "cheer" else "sit",
                           face=-1, hair=rng.choice(("#2B2530", "#3F2A1A", "#111827")))
                if heat > 0:                                                              # heat rising off every fan
                    for k in range(3):
                        u = ((t * 0.9 + k / 3 + i * 0.13) % 1.0)
                        hx_, hy_ = sx + 10 + k * 14, y - 300 - u * 160
                        path = skia.Path()
                        path.moveTo(hx_, hy_)
                        for q in range(6):
                            path.lineTo(hx_ + math.sin(q * 1.4 + t * 5) * 8, hy_ - q * 10)
                        c.drawPath(path, P("#F97316", 0.7 * heat * math.sin(u * math.pi), stroke=4))
                    lk = prog(t, T["eighty"] + i * 0.08, T["eighty"] + 0.3 + i * 0.08)
                    if lk > 0:
                        laptop(c, sx - 10, y - 330, 0.9 * e_back(lk), glow=0.8)
                        laptop(c, sx + 50, y - 330, 0.9 * e_back(lk), glow=0.8)
                if fixed:                                                                  # cold air at ankle level
                    puff_air(c, sx - 22, y - 118, t, T["cold3"] - 0.2, -0.2, -1.0, 80, n=4, w=7, seed=i,
                             a=prog(t, T["grille"] - 0.3, T["grille"] + 0.2))
                    puff_air(c, sx - 22, y - 118, t, T["cold3"] - 0.2, 0.9, -0.4, 90, n=4, w=7, seed=i + 20,
                             a=prog(t, T["grille"] - 0.3, T["grille"] + 0.2))
                if tag:
                    for k in range(4):                                                       # it is cold now
                        u = ((t * 0.35 + k / 4 + i * 0.21) % 1.0)
                        add_glow(c, sx - 60 + k * 40, y - 380 + u * 260, 10, "#FFFFFF", 0.8 * math.sin(u * math.pi))
        nx, ny = -470, -40                                                                   # the big nozzle by the pitch
        nozzle(c, nx, ny, 1.0)
        if fixed:
            nk = prog(t, T["nozzles"] - 0.3, T["nozzles"] + 0.2)
            puff_air(c, nx - 20, ny, t, T["nozzles"] - 0.3, -1.0, -0.12, 900, n=10, w=16, seed=50, a=nk)
            if t >= T["only"] - 0.2:                                                         # only the people's layer
                ok = prog(t, T["only"] - 0.2, T["only"] + 0.3)
                band = skia.Path()
                band.moveTo(-500, -40)
                for i in range(rows):
                    x, y = self.row(i)
                    band.lineTo(x - 60, y - 290)
                    band.lineTo(x + 110, y - 290)
                band.lineTo(1400, -rows * 105 - 290)
                band.lineTo(1400, -rows * 105)
                for i in reversed(range(rows)):
                    x, y = self.row(i)
                    band.lineTo(x + 110, y - 105)
                    band.lineTo(x - 60, y - 105)
                band.lineTo(-500, 0)
                band.close()
                c.drawPath(band, P(ICE, 0.18 * ok))
                c.drawPath(band, P(ICE, 0.5 * ok, stroke=3))
        c.restore()
        self.ui["cam"] = cam
        self.ui["fixed"] = fixed
        self.ui["tag"] = tag

    def ui_stands(self, c, t, tw):
        T, s = self.T, self.tl.s
        if self.ui.get("tag"):
            x, y = self.row(2)
            x0, y0 = self.at(x + 20, y - 300)
            bubble(c, min(max(x0, 330), 750), y0 - 120, self.L["yell"], self.span(T["bub"], self.duration, 0.25, 0.1))
            return
        if not self.ui.get("fixed"):
            self.chip(540, 470, "fans", T["forty"] - 0.1, T["eighty"] - 0.1, accent="#FB923C", size=40)
            self.chip(540, 470, "laptops", T["eighty"] - 0.05, s("fix3") - 0.15, accent=WARN, size=40)
            thermo(c, 140, 720, self.temp_stands(tw), self.span(s("break3"), s("break4") - 0.15), self.L["inside"])
            self.badge("alert", T["laptops"] + 0.2, s("fix3") - 0.2, x=880, y=330)
            self.red(T["laptops"] + 0.2, 1.8)
            return
        thermo(c, 140, 720, self.temp_stands(tw), self.span(s("break3"), s("break4") - 0.15), self.L["inside"])
        x, y = self.row(1)
        x0, y0 = self.at(x - 30, y - 120)
        self.label(x0, y0, 330, 560, "grille", T["grille"] - 0.1, T["nozzles"] - 0.1, ICE, size=30)
        x1, y1 = self.at(-470, -80)
        self.label(x1, y1, 300, 1090, "nozzle", T["nozzles"] - 0.1, s("break4") - 0.15, "#CBD5E1", size=32)
        self.chip(540, 470, "only", T["only"] - 0.1, s("break4") - 0.15, accent=ICE, size=38)
        self.badge("check", T["people"] + 0.1, s("break4") - 0.15, x=880, y=330)

    def temp_stands(self, t):
        s, T = self.tl.s, self.T
        if t < s("fix3") - 0.12:
            return lerp(30.0, 38.0, prog(t, T["fans"] - 0.2, T["laptops"]))
        return self.temp.at(t)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DAYSKY, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (0.1, wind_snd(2.0, 61), -16), (T["cold"], blow_snd(1.4, 62), -12),
              (T["cold"] + 0.2, sfx.sparkle(0.8, 10, 63), -12), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9),
              (T["self"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["sun"], sfx.sizzle(1.4, 66), -10),
               (T["oven"], sfx.ding(), -8), (T["oven"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 67), -5), (T["shades"] - 0.2, sfx.whirr(1.0, 120.0, 200.0, 68), -12),
               (T["paint"], sfx.sparkle(0.8, 10, 69), -12), (T["bounces"], sfx.pop(70), -9), (T["away"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["wind"] - 0.3, wind_snd(2.4, 72), -6),
               (T["pours"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 73), -5), (T["wing0"], sfx.whirr(0.8, 140.0, 240.0, 74), -12),
               (T["slides"] - 0.3, wind_snd(1.6, 75), -12), (T["inside"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 76), -4), (T["forty"], crowd_snd(2.4, 77), -10),
               (T["eighty"], sfx.pop(78), -10), (T["eighty"] + 0.25, sfx.pop(79), -10), (T["laptops"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 80), -5), (T["grille"], blow_snd(1.6, 81), -10),
               (T["nozzles"], blow_snd(1.8, 82), -8), (T["people"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 83), -4), (T["chilling"], sfx.hum(2.4, 100.0), -10),
               (T["burns"], sfx.sizzle(0.8, 84), -10), (T["power"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 85), -5), (T["night0"] + 0.3, sfx.hiss(1.0, 86), -12),
               (T["day0"], sfx.whirr(1.2, 100.0, 160.0, 87), -12), (T["loop0"], blow_snd(1.4, 88), -12),
               (T["again"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(89), 0), (T["follow"] - 0.15, sfx.pop(90), -4)]
        ev += [(T["switch"] + 0.1, sfx.thunk(91), -6), (T["switch"] + 0.2, sfx.charge_up(0.8), -10),
               (T["doc"], sfx.pop(92), -8), (T["gates"], crowd_snd(2.0, 93), -10)]
        ev += [(T["s1"], sfx.pop(94), -3), (T["s2"], sfx.pop(95), -3), (T["s3"], sfx.pop(96), -3)]
        ev += [(T["cong2"], sfx.pop(97), -2), (T["cong2"], sfx.sparkle(1.0, 14, 98), -4), (T["cong2"] + 0.1, crowd_snd(1.8, 99), -10),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 100), -6), (T["jacket"], brr_snd(0.8, 101), -10),
               (T["bub"], sfx.pop(102), -8)]
        return ev


def shade_c(col, k):
    return shade(col, k)


NAME = "stadium"
EPISODE = Stadium
