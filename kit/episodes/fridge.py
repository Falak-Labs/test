"""Episode 53 - A refrigerator.  v2 look: a kitchen in a heatwave, a fridge cut open from the side with its refrigerant
loop drawn as a glowing pipe (blue = cold, red = hot).

Sets: kitchen (hook: a heatwave, an ice cube melting on the counter, the fridge door swings open on cold milk; stat;
closer with the door open and the light on), ice (break1: blocks sawn from a frozen lake, packed in sawdust and shipped
as far as India), loop (fix1..fix4, cta, reveal: the fridge in section; the evaporator boils the liquid and soaks up the
food's heat; the gas is used up; the compressor squeezes it hot like a bike pump; the coils on the back throw the heat
into the kitchen and it turns back to liquid; the pressure gauge in the red; the spaghetti-thin capillary tube drops the
pressure and it comes out icy; the thermostat switches the compressor; the magnet in the door seal), tag (EN: standing
at the open fridge waiting for new food to appear; AR: the same, and mom shouting "close the fridge!").
World (loop): the fridge seen from the side, door on the left, back on the right; the cabinet x -260..260, y -560..560.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow, thermo, heat_lines, sun  # noqa: E402
from burjalarab import path_of, sea_band, wave  # noqa: E402
from phone import bubble  # noqa: E402

HOT, WARM, COOL, COLD = "#EF4444", "#F59E0B", "#7DD3FC", "#38BDF8"
BODY, BODY_D = "#8E98A6", "#6E7685"
FOAM = "#A88A44"
KITCH = ("#5A3E2A", "#3A281C")

# the refrigerant loop, in order: compressor -> condenser (back) -> capillary -> evaporator (freezer) -> suction line
LOOP = ([(330, 452), (330, 400), (470, 400)] +
        [p for k in range(7) for p in (((470, 400 - k * 130), (300, 400 - k * 130 - 65)) if k % 2 == 0 else
                                       ((300, 400 - k * 130), (470, 400 - k * 130 - 65)))] +
        [(300, -510), (330, -540)])
CAP_START = len(LOOP) - 1
LOOP += [(330 + 26 * math.cos(a_ / 8.0 * 6.283) + a_ * 4, -580 + 22 * math.sin(a_ / 8.0 * 6.283)) for a_ in range(25)]
LOOP += [(250, -540), (230, -480)]
EVAP_START = len(LOOP) - 1
for k in range(4):
    y_ = -480 + k * 50
    LOOP += [(60, y_), (60, y_ + 25), (230, y_ + 25), (230, y_ + 50)] if k < 3 else [(60, y_), (60, y_ + 30), (230, y_ + 30)]
EVAP_END = len(LOOP) - 1
LOOP += [(275, -300), (275, 440), (300, 470)]


def _cum(pts):
    d = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.append(d[-1] + math.hypot(x1 - x0, y1 - y0))
    return d


LOOP_D = _cum(LOOP)
LOOP_LEN = LOOP_D[-1]


def loop_at(s):
    """Point on the loop at arc length s (wraps)."""
    s %= LOOP_LEN
    for i in range(len(LOOP) - 1):
        if LOOP_D[i + 1] >= s:
            u = (s - LOOP_D[i]) / max(1e-6, LOOP_D[i + 1] - LOOP_D[i])
            return lerp(LOOP[i][0], LOOP[i + 1][0], u), lerp(LOOP[i][1], LOOP[i + 1][1], u)
    return LOOP[-1]


def temp_col(s):
    """Refrigerant colour along the loop: hot after the compressor, cooling on the coils, icy after the capillary."""
    s %= LOOP_LEN
    cap0, evap0, evap1 = LOOP_D[CAP_START], LOOP_D[EVAP_START], LOOP_D[EVAP_END]
    if s < LOOP_D[3]:
        return HOT
    if s < cap0:
        return mix(HOT, WARM, (s - LOOP_D[3]) / max(1.0, cap0 - LOOP_D[3]))
    if s < evap0:
        return mix(WARM, COLD, (s - cap0) / max(1.0, evap0 - cap0))
    if s < evap1:
        return COLD
    return mix(COOL, "#A5B4FC", (s - evap1) / max(1.0, LOOP_LEN - evap1))


def pipe(c, pts, col, w, a=1.0):
    if len(pts) >= 2 and a > 0:
        c.drawPath(path_of(pts), P(col, a, stroke=w))


def compressor(c, x, y, s, t, run=0.0, hot=0.0, squeeze=0.0, a=1.0):
    """The black compressor dome (world), with a cutaway piston when squeeze > 0."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    vib = math.sin(t * 70) * 2.5 * run
    c.translate(vib, 0)
    c.drawRRect(rr(-90, 30, 180, 22, 8), P("#374151", a))
    c.drawPath(path_of([(-80, 34), (-80, -30), (-60, -70), (60, -70), (80, -30), (80, 34)], close=True),
               lin_paint(-80, 0, 80, 0, ["#1F2937", "#4B5563", "#111827"], a=a))
    if hot > 0:
        add_glow(c, 0, -10, 120, HOT, 0.35 * hot * a)
    if squeeze > 0:                                                  # cutaway: a piston pushing gas into a small space
        c.drawRRect(rr(-50, -56, 100, 76, 10), P("#0F172A", a))
        py_ = lerp(14, -24, squeeze)
        c.drawRect(R(-40, py_, 80, 16), P("#9CA3AF", a))
        n = 14
        rng = random.Random(4)
        for k in range(n):
            gx = rng.uniform(-38, 38)
            gy = lerp(-50, py_ - 6, rng.random())
            c.drawCircle(gx, gy, 5, P(mix(COOL, HOT, squeeze), a))
    c.restore()


def gauge(c, x, y, r, frac, a=1.0, lab=""):
    """Round pressure gauge, needle at frac 0..1 (red zone at the top end)."""
    c.drawCircle(x, y, r + 8, P("#374151", a))
    c.drawCircle(x, y, r, P("#F8FAFC", a))
    for k in range(9):
        an = math.radians(lerp(220, -40, k / 8.0))
        c.drawLine(x + math.cos(an) * r * 0.78, y - math.sin(an) * r * 0.78, x + math.cos(an) * r * 0.92,
                   y - math.sin(an) * r * 0.92, P("#1F2937", a, stroke=3))
    rz = skia.Path()
    rz.addArc(R(x - r * 0.85, y - r * 0.85, r * 1.7, r * 1.7), -40 + 40, -60)
    c.drawPath(rz, P(HOT, a, stroke=r * 0.14))
    an = math.radians(lerp(220, -40, clamp(frac)))
    c.drawLine(x, y, x + math.cos(an) * r * 0.8, y - math.sin(an) * r * 0.8, P("#DC2626", a, stroke=6))
    c.drawCircle(x, y, 8, P("#1F2937", a))


def food(c, x, y, kind, s=1.0, a=1.0, frost=0.0):
    """Things on the shelves (world or screen), standing on (x, y)."""
    if kind == "milk":
        c.drawRRect(rr(x - 26 * s, y - 120 * s, 52 * s, 120 * s, 10 * s), P("#F1F5F9", a))
        c.drawRect(R(x - 18 * s, y - 136 * s, 36 * s, 18 * s), P("#2563EB", a))
        c.drawRect(R(x - 26 * s, y - 80 * s, 52 * s, 30 * s), P("#60A5FA", a))
        if frost > 0:
            for k in range(8):
                c.drawCircle(x - 18 * s + (k * 13 % 36) * s, y - 110 * s + (k * 29 % 90) * s, 3 * s, P("#E0F2FE", frost * a))
    elif kind == "melon":
        c.drawCircle(x, y - 40 * s, 42 * s, P("#16A34A", a))
        c.drawCircle(x, y - 40 * s, 30 * s, P("#EF4444", a))
    elif kind == "eggs":
        for k in range(4):
            c.drawOval(R(x - 50 * s + k * 26 * s, y - 34 * s, 22 * s, 30 * s), P("#FDE7C8", a))
        c.drawRect(R(x - 54 * s, y - 16 * s, 108 * s, 16 * s), P("#94A3B8", a))
    elif kind == "juice":
        c.drawRRect(rr(x - 20 * s, y - 90 * s, 40 * s, 90 * s, 8 * s), P("#F97316", 0.9 * a))
        c.drawRect(R(x - 10 * s, y - 104 * s, 20 * s, 14 * s), P("#E5E7EB", a))
    elif kind == "veg":
        for k, col in enumerate(("#22C55E", "#F97316", "#EF4444")):
            c.drawCircle(x - 30 * s + k * 30 * s, y - 20 * s, 20 * s, P(col, a))


def fridge_front(c, x, y, w, h, t, door=0.0, light=1.0, frost=0.0, lit=1.0, food_k=1.0):
    """Front view (screen): body top-left (x, y); the freezer on top; door 0..1 opens the main door (hinged right)."""
    fh = h * 0.3
    contact_shadow(c, x + w / 2, y + h, w * 1.1, 0.6, 30)
    box(c, x, y, w, h, BODY, r=22)
    c.drawRRect(rr(x + 10, y + 10, w - 20, fh - 16, 16), P("#9AA4B2"))
    c.drawRRect(rr(x + w - 50, y + fh * 0.3, 14, fh * 0.4, 7), P("#6B7280"))           # freezer handle
    my = y + fh
    c.drawRect(R(x + 12, my - 4, w - 24, 8), P("#6B7280"))
    if door > 0:                                                     # inside: lit shelves
        ix, iy, iw, ih = x + 18, my + 12, w - 36, h - fh - 40
        c.drawRRect(rr(ix, iy, iw, ih, 12), lin_paint(0, iy, 0, iy + ih, [mix("#1E3A5F", "#7FA8CC", light), mix("#0F2440", "#5E86AE", light)]))
        if light > 0:
            add_glow(c, ix + iw / 2, iy + 40, iw * 0.6, "#BDEFFF", 0.16 * light * lit)
        for k in range(1, 3):
            c.drawRect(R(ix, iy + ih * k / 3, iw, 8), P("#E5E7EB", 0.9))
        if food_k > 0:
            food(c, ix + iw * 0.25, iy + ih / 3, "milk", 1.15, frost=frost)
            food(c, ix + iw * 0.62, iy + ih / 3, "juice", 1.1)
            food(c, ix + iw * 0.35, iy + ih * 2 / 3, "eggs", 1.0)
            food(c, ix + iw * 0.72, iy + ih * 2 / 3, "melon", 0.9)
            food(c, ix + iw * 0.5, iy + ih - 6, "veg", 1.0)
        if frost > 0:
            for k in range(6):                                       # cold mist rolling out
                q = (t * 0.4 + k / 6.0) % 1.0
                v2.puff(c, ix + iw * (0.2 + 0.12 * k), iy + ih - 20 + q * 120, 60 + 70 * q, "#A9CDE8", 0.22 * frost * (1 - q), k=1)
        dk = e_io(clamp(door))                                       # the door, swung open to the right
        dw = (w - 4) * (1 - dk) + 46 * dk
        dpath = path_of([(x + w - dw, my + 6), (x + w + 30 * dk, my + 6 - 40 * dk), (x + w + 30 * dk, y + h - 6 + 40 * dk),
                         (x + w - dw, y + h - 6)], close=True) if dk > 0.02 else None
        if dpath is not None:
            c.drawPath(dpath, lin_paint(x + w - dw, 0, x + w + 30 * dk, 0, [BODY, "#A8B1BE"]))
    else:
        c.drawRRect(rr(x + 10, my + 10, w - 20, h - fh - 26, 16), P("#9AA4B2"))
        c.drawRRect(rr(x + w - 50, my + 40, 14, (h - fh) * 0.35, 7), P("#6B7280"))


def ice_cube(c, x, y, s, melt=0.0, a=1.0):
    """An ice cube on a counter (screen), melting into a puddle."""
    k = 1 - 0.85 * melt
    c.drawOval(R(x - 60 * s * (0.6 + melt), y - 8 * s, 120 * s * (0.6 + melt), 18 * s), P("#7DD3FC", 0.5 * a))
    if k > 0.05:
        c.drawRRect(rr(x - 34 * s * k, y - 66 * s * k, 68 * s * k, 66 * s * k, 12 * s * k), P("#BAE6FD", 0.85 * a))
        c.drawRRect(rr(x - 22 * s * k, y - 56 * s * k, 20 * s * k, 30 * s * k, 6 * s * k), P("#F0F9FF", 0.6 * a))


def ship(c, x, y, s, t, a=1.0, blocks=1.0, melt=0.0):
    """A three-masted sailing ship loaded with ice blocks (screen), waterline at y."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.translate(0, math.sin(t * 1.6) * 4)
    hull = path_of([(-220, -60), (230, -60), (180, 40), (-170, 40)], close=True)
    c.drawPath(hull, lin_paint(0, -60, 0, 40, ["#7C4A2A", "#4A2A18"], a=a))
    for k in range(int(9 * blocks)):                                 # ice blocks in sawdust on deck
        bx = -170 + (k % 5) * 70
        by = -100 - (k // 5) * 44
        c.drawRect(R(bx - 4, by - 4, 66, 48), P("#A16207", a))
        c.drawRect(R(bx, by, 58 * (1 - 0.3 * melt), 40 * (1 - 0.3 * melt)), P("#BAE6FD", a))
    for mx_, mh in ((-120, 380), (20, 440), (150, 340)):
        c.drawLine(mx_, -60, mx_, -60 - mh, P("#3A2A18", a, stroke=10))
        sp = skia.Path()
        sp.moveTo(mx_ + 6, -60 - mh + 30)
        sp.quadTo(mx_ + 110, -60 - mh * 0.55, mx_ + 6, -110)
        sp.close()
        c.drawPath(sp, P("#F1E9D8", 0.95 * a))
    c.restore()


def sawyer(c, x, y, h, t, a=1.0):
    """A worker sawing ice (screen)."""
    person(c, x, y, h, "#7C2D12", t, pose="carry", face=1, hat="beanie", a=a)
    u = h / 140.0
    sx = math.sin(t * 9) * 16 * u
    c.drawLine(x + 30 * u + sx, y - 70 * u, x + 70 * u + sx, y + 6 * u, P("#9CA3AF", a, stroke=5 * u))


# ====================================================================================== the episode
class Fridge(EpisodeV2):
    BUILD_NO = 53
    FIRST_SET = "kitchen"
    CLEAR = "#0F1B2E"
    TITLE = {"en": "REFRIGERATOR", "ar_sa": "ثلاجة"}
    EMPH = {"en": ["CONGRATS", "MILK", "COLD", "HEATWAVE", "SINGLE", "CUBE", "ICE", "REFRIGERATOR", "YOURSELF", "SAWN",
                   "FROZEN", "LAKES", "SHIPPED", "INDIA", "SAWDUST", "LIQUID", "BOILS", "BELOW", "FREEZING", "SOAKS",
                   "HEAT", "GAS", "USED", "COMPRESSOR", "SQUEEZES", "HARD", "SQUEEZED", "HOT", "BIKE", "PUMP", "HOLDS",
                   "BOX", "COILS", "BACK", "ESCAPES", "KITCHEN", "TURNS", "HIGH", "PRESSURE", "TUBE", "THIN",
                   "SPAGHETTI", "DROPS", "ICY", "LOOP", "FOLLOW", "EIFFEL", "TOWER", "THERMOSTAT", "MAGNET", "SEAL",
                   "FOUR", "DEGREES", "MINUS", "EIGHTEEN", "FREEZER", "EINSTEIN", "PATENTED", "DOOR", "WIDE", "OPEN",
                   "NEW", "FOOD"],
            "ar_sa": ["مبروك", "الحليب", "بارد", "الصيف", "مكعب", "ثلج", "ثلاجة", "بيدك", "يقصّونه", "بحيرات", "متجمدة",
                      "الهند", "سائل", "يغلي", "الصفر", "يسحب", "الحرارة", "غاز", "ينفع", "فالكمبروسر", "يعصر", "يسخن",
                      "منفاخ", "السيكل", "شايل", "اللفّات", "ورا", "للمطبخ", "ضغط", "قوي", "ماسورة", "رفيعة", "المكرونة",
                      "ينزل", "ويبرد", "اللفة", "تابعني", "إيفل", "ثرموستات", "مغناطيس", "الباب", "أربع", "درجات",
                      "ثمنطعش", "الفريزر", "وأينشتاين", "اختراع", "فاتح", "بابها", "سكّر"]}
    KEYS = {"ar_sa": {
        ("hook", "MILK"): "الحليب", ("hook", "COLD"): "بارد", ("hook", "HEATWAVE"): "الصيف", ("hook", "ICE"): "ثلج",
        ("hook", "CONGRATS"): "مبروك", ("hook", "REFRIGERATOR"): "ثلاجة",
        ("break1", "ICE"): "ثلج", ("break1", "SAWN"): "يقصّونه", ("break1", "LAKES"): "بحيرات", ("break1", "INDIA"): "الهند",
        ("fix1", "LIQUID"): "سائل", ("fix1", "BOILS"): "يغلي", ("fix1", "FREEZING"): "الصفر", ("fix1", "SOAKS"): "يسحب",
        ("fix1", "HEAT"): "الحرارة",
        ("break2", "GAS"): "غاز", ("break2", "USED"): "ينفع",
        ("fix2", "COMPRESSOR"): "كمبروسر", ("fix2", "SQUEEZES"): "يعصر", ("fix2", "HOT"): "يسخن", ("fix2", "BIKE"): "السيكل",
        ("break3", "GAS"): "الغاز", ("break3", "HEAT"): "الحرارة",
        ("fix3", "COILS"): "اللفّات", ("fix3", "ESCAPES"): "تطلع", ("fix3", "KITCHEN"): "للمطبخ", ("fix3", "LIQUID"): "سائل",
        ("break4", "LIQUID"): "السائل", ("break4", "PRESSURE"): "ضغط",
        ("fix4", "TUBE"): "ماسورة", ("fix4", "SPAGHETTI"): "المكرونة", ("fix4", "DROPS"): "ينزل", ("fix4", "ICY"): "ويبرد",
        ("fix4", "LOOP"): "اللفة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "THERMOSTAT"): "ثرموستات", ("reveal", "OFF"): "ويطفيه", ("reveal", "MAGNET"): "مغناطيس",
        ("reveal", "SEAL"): "الباب",
        ("stat", "FOUR"): "أربع", ("stat", "MINUS"): "سالب", ("stat", "EINSTEIN"): "أينشتاين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "PUMPS"): "تطلّع", ("tag", "STAND"): "واقف", ("tag", "OPEN"): "فاتح", ("tag", "FOOD"): "سكّر"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Eiffel Tower"),
                   "stat": [("4°C", "INSIDE"), ("-18°C", "FREEZER"), ("1930", "EINSTEIN'S FRIDGE PATENT")],
                   "L": {"heat": "A HEATWAVE", "noice": "NOT ONE ICE CUBE", "name": "A REFRIGERATOR",
                         "lakes": "ICE FROM FROZEN LAKES", "india": "SHIPPED TO INDIA", "liquid": "BOILS FAR BELOW 0°C",
                         "soak": "IT SOAKS UP THE HEAT", "used": "ALL GAS: USED UP", "comp": "COMPRESSOR",
                         "squeeze": "SQUEEZED GAS GETS HOT", "holds": "IT HOLDS THE HEAT", "coils": "COILS ON THE BACK",
                         "escape": "HEAT OUT INTO THE KITCHEN", "back": "BACK TO LIQUID", "press": "HIGH PRESSURE",
                         "tube": "A TUBE AS THIN AS SPAGHETTI", "icy": "PRESSURE DROPS: ICY COLD", "thermo": "THERMOSTAT",
                         "magnet": "A MAGNET IN THE SEAL", "wait": "WAITING FOR NEW FOOD"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: برج إيفل"),
                      "stat": [("4°", "درجات داخلها"), ("-18°", "في الفريزر"), ("1930", "اختراع ثلاجة لأينشتاين")],
                      "L": {"heat": "عز الصيف", "noice": "ولا مكعب ثلج", "name": "ثلاجة",
                            "lakes": "ثلج من بحيرات متجمدة", "india": "يشحنونه لين الهند", "liquid": "يغلي تحت الصفر",
                            "soak": "يسحب الحرارة", "used": "صار غاز: ما عاد ينفع", "comp": "الكمبروسر",
                            "squeeze": "الغاز إذا انعصر يسخن", "holds": "شايل الحرارة", "coils": "اللفّات اللي ورا",
                            "escape": "الحرارة تطلع للمطبخ", "back": "يرجع سائل", "press": "ضغط قوي",
                            "tube": "ماسورة رفيعة مثل المكرونة", "icy": "الضغط ينزل: يبرد مرة",
                            "thermo": "ثرموستات", "magnet": "مغناطيس في مطاط الباب", "wait": "تدوّر على شي",
                            "bubble": "سكّر الثلاجة!"}}}
    COVER_T = ("closer", 0.6)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "milk": ("hook", "MILK", 0.15), "cold": ("hook", "COLD", 0.25), "heat": ("hook", "HEATWAVE", 0.35),
            "ice": ("hook", "ICE", 0.55), "congrats": ("hook", "CONGRATS", 0.65), "fridge": ("hook", "REFRIGERATOR", 0.9),
            "ice1": ("break1", "ICE", 0.15), "sawn": ("break1", "SAWN", 0.3), "lakes": ("break1", "LAKES", 0.45),
            "india": ("break1", "INDIA", 0.8),
            "liquid": ("fix1", "LIQUID", 0.15), "boils": ("fix1", "BOILS", 0.25), "freezing": ("fix1", "FREEZING", 0.4),
            "soaks": ("fix1", "SOAKS", 0.75), "heat1": ("fix1", "HEAT", 0.9),
            "gas2": ("break2", "GAS", 0.5), "used": ("break2", "USED", 0.85),
            "comp": ("fix2", "COMPRESSOR", 0.1), "squeeze": ("fix2", "SQUEEZES", 0.25), "hot": ("fix2", "HOT", 0.6),
            "bike": ("fix2", "BIKE", 0.85),
            "gas3": ("break3", "GAS", 0.3), "heat3": ("break3", "HEAT", 0.7),
            "coils": ("fix3", "COILS", 0.2), "escape": ("fix3", "ESCAPES", 0.45), "kitchen": ("fix3", "KITCHEN", 0.6),
            "liquid3": ("fix3", "LIQUID", 0.9),
            "liq4": ("break4", "LIQUID", 0.3), "press": ("break4", "PRESSURE", 0.8),
            "tube": ("fix4", "TUBE", 0.12), "spag": ("fix4", "SPAGHETTI", 0.3), "drops": ("fix4", "DROPS", 0.5),
            "icy": ("fix4", "ICY", 0.65), "loop": ("fix4", "LOOP", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "thermo": ("reveal", "THERMOSTAT", 0.1), "off": ("reveal", "OFF", 0.4), "magnet": ("reveal", "MAGNET", 0.7),
            "seal": ("reveal", "SEAL", 0.92),
            "s1": ("stat", "FOUR", 0.03), "s2": ("stat", "MINUS", 0.35), "s3": ("stat", "EINSTEIN", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_pumps": ("tag", "PUMPS", 0.03), "t_stand": ("tag", "STAND", 0.4), "t_open": ("tag", "OPEN", 0.55),
            "t_food": ("tag", "FOOD", 0.9)})
        T["used1"] = max(T["used"], T["gas2"]) + 0.1
        T["heat3b"] = max(T["heat3"], T["gas3"]) + 0.1
        T["press1"] = max(T["press"], T["liq4"]) + 0.1
        T["loop1"] = max(T["loop"], T["icy"], T["drops"]) + 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "ice", 1)
        self.cut(s("fix1") - 0.12, "loop", -1)
        self.cut(s("stat") - 0.12, "kitchen", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        # ---- loop camera
        lc = Camera(60, 120, 0.9)
        lc.key(s("fix1") - 0.12, 140, -400, 1.55, 0.0).key(T["soaks"] - 0.3, 120, -340, 1.35, 1.0)
        lc.key(s("break2") - 0.12, 150, -380, 1.4, 0.4)
        lc.key(s("fix2") - 0.12, 360, 420, 1.7, 0.6)
        lc.key(T["bike"] - 0.3, 400, 360, 1.45, 0.8)
        lc.key(s("break3") - 0.12, 300, 120, 0.95, 0.7)
        lc.key(s("fix3") - 0.12, 380, -40, 1.05, 0.6)
        lc.key(s("break4") - 0.12, 360, -320, 1.4, 0.6)
        lc.key(s("fix4") - 0.12, 360, -520, 2.0, 0.6).key(T["icy"] - 0.2, 220, -380, 1.3, 1.0)
        lc.key(T["loop"] - 0.3, 100, 120, 0.9, 1.2)
        lc.key(s("reveal") - 0.12, -60, -150, 1.4, 0.6).key(T["magnet"] - 0.3, -250, 60, 2.2, 0.9)
        self.lcam = lc
        kc = Camera(0, 0, 1.0)                                       # kitchen camera (screen-space zoom about the fridge)
        kc.key(0.1, 0, 0, 1.04, max(1.0, T["congrats"]))
        kc.key(T["congrats"], 0, -20, 1.1, 1.4)
        kc.key(s("stat") - 0.12, 0, 120, 0.86, 0.0).key(s("stat"), 0, 110, 0.88, 3.0)
        kc.key(s("closer") - 0.1, 0, 0, 1.0, 1.0).key(s("closer") + 0.9, 0, -10, 1.05, 3.0)
        self.kcam = kc
        self.spans = [(T["india"], T["heat1"] + 0.3), (T["used1"], T["bike"] + 0.4), (T["heat3b"], T["liquid3"] + 0.3),
                      (T["press1"], T["loop1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["india"], 0.3, 6), (T["used1"], 0.3, 6), (T["squeeze"], 0.4, 7),
                       (T["press1"], 0.4, 7), (T["seal"], 0.25, 8), (s("closer") + 0.2, 0.35, 9), (T["t_food"], 0.3, 8)]

    # ------------------------------------------------------------------ set: kitchen (hook, stat, closer), front view
    def kitchen_room(self, c, t, hot=1.0, night=0.0):
        vrect(c, 0, 0, W, H, [mix("#7A4A3A", "#1E1B3A", night), mix("#5A3426", "#14122A", night)])
        for k in range(12):                                          # wall tiles
            c.drawLine(0, 380 + k * 80, W, 380 + k * 80, P("#000000", 0.08, stroke=3))
        wx, wy = 80, 420                                             # the window with the blazing sun
        c.drawRRect(rr(wx - 10, wy - 10, 280, 360, 16), P("#E5E7EB", 0.9))
        c.drawRect(R(wx, wy, 260, 340), lin_paint(0, wy, 0, wy + 340, [mix("#FF9D5C", "#0B1030", night), mix("#FFD58A", "#1E2A5A", night)]))
        if night < 1:
            sun(c, wx + 170, wy + 110, 46, heat=hot, a=1 - night)
            heat_lines(c, wx + 30, wx + 230, wy + 200, wy + 330, t, a=0.8 * hot * (1 - night))
        c.drawLine(wx + 130, wy, wx + 130, wy + 340, P("#E5E7EB", 0.9, stroke=8))
        c.drawRect(R(0, 1240, W, H - 1240), P(KITCH[1]))
        c.drawRect(R(0, 1100, 330, 140), P("#8A6A4A"))               # the counter on the left
        c.drawRect(R(0, 1090, 340, 16), P("#D6C6A8"))
        if hot > 0 and night < 1:
            c.drawRect(R(0, 0, W, H), P("#F97316", 0.08 * hot * (1 - night)))

    def draw_kitchen(self, c, t):
        T, s = self.T, self.tl.s
        hook = t < s("break1")
        night = prog(t, s("closer") - 0.6, s("closer") + 0.6) if not hook else 0.0
        self.kitchen_room(c, t, hot=1.0 if hook else 0.6, night=night)
        cx, cy, z = self.kcam.at(t)
        c.save()
        c.translate(540 + cx, 860 + cy)
        c.scale(z, z)
        c.translate(-540, -860)
        thermo(c, 950, 560, 1.4, 0.95 if hook else 0.7)
        if hook:
            door = prog(t, T["milk"] - 0.4, T["cold"] + 0.2)
            frost = prog(t, T["cold"] - 0.2, T["cold"] + 0.4)
        else:
            door = 1.0
            frost = 0.8
        fridge_front(c, 390, 380, 470, 860, t, door=door, light=1.0, frost=frost, lit=1.0 + night)
        ice_cube(c, 200, 1092, 1.3, melt=prog(t, 0.2, T["ice"] + 0.8) if hook else 1.0)
        c.restore()
        if night > 0:
            c.drawRect(R(0, 0, W, H), P("#0B1030", 0.25 * night))
            add_glow(c, 620, 820, 380, "#9CC8E8", 0.16 * night)

    def ui_kitchen(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "heat", T["milk"] - 0.1, T["ice"] - 0.15, accent="#FB923C", size=44)
            self.chip(540, 300, "noice", T["ice"] - 0.15, T["congrats"] - 0.05, accent="#7DD3FC", size=44)
            self.chip(540, 300, "name", T["fridge"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: ice (break1)
    def draw_ice(self, c, t):
        T = self.T
        pan = e_io(prog(t, T["lakes"] + 0.2, T["india"]))
        c.save()
        c.translate(-W * pan, 0)
        v2.sky(c, W, H, 0.0, horizon_y=820)                          # left: the frozen lake at dawn
        c.drawRect(R(0, 820, W, H - 820), lin_paint(0, 820, 0, H, ["#8AA6C2", "#5E7A98"]))
        for j in range(5):                                           # the grid of blocks being cut
            for i in range(6):
                bx, by = 180 + i * 130, 980 + j * 110
                cutk = clamp(prog(t, T["sawn"] - 0.4, T["lakes"] + 0.6) * 30 - (j * 6 + i))
                c.drawRect(R(bx, by, 120, 100), P("#7F9DBB"))
                if cutk > 0:
                    c.drawRect(R(bx, by, 120, 100), P("#3B5B80", cutk, stroke=5))
        sawyer(c, 300, 1000, 210, t)
        sawyer(c, 700, 1000, 200, t + 0.5)
        for k in range(3):
            v2.puff(c, 340 + k * 400, 930, 30, "#F1F5F9", 0.5, k=1)
        c.restore()
        if pan > 0:                                                  # right: the ship crossing a hot sea to India
            c.save()
            c.translate(W * (1 - pan), 0)
            v2.sky(c, W, H, 0.0, horizon_y=760)
            sun(c, 840, 420, 64, heat=1.0)
            sea_band(c, -40, W + 40, 760, H - 760, t, col="#1E7A9A", dark="#0B3A5A")
            ship(c, 470, 1000, 1.25, t, melt=prog(t, T["india"] - 0.3, T["india"] + 1.0))
            for k in range(5):                                       # drips from the melting blocks
                q = (t * 1.4 + k / 5.0) % 1.0
                c.drawCircle(300 + k * 70, 900 + q * 90, 6, P("#7DD3FC", 0.8 * (1 - q)))
            c.restore()

    def ui_ice(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "lakes", T["sawn"] - 0.2, T["india"] - 0.3, accent="#BAE6FD", size=42)
        self.chip(540, 300, "india", T["india"] - 0.3, s("fix1") - 0.15, accent="#FB923C", size=44)
        self.badge("alert", T["india"] + 0.1, s("fix1") - 0.2, x=920, y=420)
        self.red(T["india"] + 0.1, 1.2)

    # ------------------------------------------------------------------ set: loop (fix1..fix4, cta, reveal), section
    def draw_loop(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.lcam.at(t)
        vrect(c, 0, 0, W, H, ["#2A1E2E", "#3A2626"])
        self.view(c, cam)
        c.drawRect(R(-1400, 560, 2800, 900), P(KITCH[1]))            # the floor
        c.drawRect(R(-1400, -1400, 2800, 70), P("#4A3426"))
        # stage of the story: which parts carry what
        f1 = t >= s("fix1") - 0.12
        boil = prog(t, T["boils"] - 0.3, T["boils"] + 0.3)
        all_gas = prog(t, T["gas2"] - 0.3, T["used1"])
        comp_run = prog(t, T["comp"] - 0.3, T["comp"]) if t < s("break3") - 0.12 else 1.0
        sq = prog(t, T["squeeze"] - 0.2, T["hot"] + 0.3)
        cond = prog(t, T["coils"] - 0.3, T["liquid3"] + 0.3)
        capk = prog(t, T["tube"] - 0.3, T["icy"] + 0.3)
        flow_on = t >= T["loop1"] - 0.3
        # the cabinet in section: insulated walls, freezer on top, shelves, the door on the left
        c.drawRRect(rr(-280, -580, 560, 1150, 24), P("#6B7280"))
        c.drawRRect(rr(-268, -568, 536, 1126, 18), P("#A88A44"))
        for k in range(30):
            c.drawCircle(-250 + (k * 37) % 500, -560 + (k * 97) % 1100, 5, P("#A88A44", 0.6))
        inside_col = mix("#A5D8F5", "#5A7A9A", 0.3) if f1 else "#B0C4D8"
        cool_in = prog(t, T["soaks"] - 0.4, T["heat1"] + 0.6)
        if t >= T["used1"] and t < s("fix4") - 0.12:
            cool_in = 1 - 0.6 * prog(t, T["used1"], T["used1"] + 1.0) if t < s("fix2") - 0.12 else 0.6
        if t >= s("fix4") - 0.12:
            cool_in = prog(t, T["icy"] - 0.2, T["loop1"] + 0.4)
        c.drawRRect(rr(-230, -530, 470, 1050, 14), lin_paint(0, -530, 0, 520, [mix("#4A5A70", "#7FA8CC", cool_in), mix("#3A4A60", "#5E86AE", cool_in)]))
        c.drawRect(R(-230, -260, 470, 16), P("#A8B1BE"))              # the freezer floor
        for yy in (0, 260):
            c.drawRect(R(-230, yy, 470, 8), P("#A8B1BE", 0.9))
        food(c, -120, -264, "veg", 1.2)
        food(c, -60, -4, "milk", 1.3, frost=cool_in)
        food(c, 80, -4, "juice", 1.2)
        food(c, -40, 256, "eggs", 1.4)
        food(c, 110, 256, "melon", 1.1)
        if f1 and t < s("fix2") - 0.12:                              # the food's heat going into the evaporator
            hk = prog(t, T["soaks"] - 0.4, T["soaks"] + 0.3) * (1 - all_gas)
            for k in range(5):
                q = (t * 0.7 + k / 5.0) % 1.0
                x0_, y0_ = -100 + k * 50, -60 - k * 30
                arrow(c, lerp(x0_, 150, q), lerp(y0_, -380, q), lerp(x0_, 150, q) + 20, lerp(y0_, -380, q) - 30, HOT,
                      a=hk * math.sin(q * math.pi), w=8, head=18)
        c.drawRect(R(-300, -560, 36, 1110), P(BODY))                  # the door, closed (seen edge-on)
        c.drawRect(R(-312, -100, 12, 220), P("#6B7280"))
        # the loop: pipe, then the refrigerant flowing in it
        pipe(c, LOOP[:CAP_START + 1], "#475569", 22)
        pipe(c, LOOP[CAP_START:EVAP_START + 1], "#475569", 9)
        pipe(c, LOOP[EVAP_START:], "#475569", 22)
        n = 120
        spd = 0.0
        if f1:
            spd = 0.12 if t < s("break2") - 0.12 else (0.04 if t < s("fix2") - 0.12 else 0.12)
            if flow_on or t >= s("cta") - 0.12:
                spd = 0.16
        for k in range(n):
            sp = (k / float(n) + t * spd) * LOOP_LEN
            x_, y_ = loop_at(sp)
            col = temp_col(sp)
            spm = sp % LOOP_LEN
            in_cap = LOOP_D[CAP_START] <= spm < LOOP_D[EVAP_START]
            in_evap = LOOP_D[EVAP_START] <= spm < LOOP_D[EVAP_END]
            if not f1:
                continue
            if t < s("fix4") - 0.12 and not flow_on:                 # before the loop is closed, show one part at a time
                if t < s("fix2") - 0.12:
                    if not in_evap and not (spm >= LOOP_D[EVAP_END]):
                        continue
                    col = COLD if not all_gas or not in_evap else "#A5B4FC"
                elif t < s("break3") - 0.12:
                    if spm > LOOP_D[3] and spm < LOOP_D[EVAP_END]:
                        continue
                    col = mix(COOL, HOT, sq) if spm <= LOOP_D[3] else COOL
                elif t < s("break4") - 0.12:
                    if spm > LOOP_D[CAP_START] and spm < LOOP_D[EVAP_END]:
                        continue
                    if spm <= LOOP_D[CAP_START]:
                        u_ = spm / LOOP_D[CAP_START]
                        col = HOT if t < s("fix3") - 0.12 else mix(HOT, WARM, clamp(cond * 1.5 - u_ * 0.5))
                else:
                    if in_cap and capk < (spm - LOOP_D[CAP_START]) / max(1.0, LOOP_D[EVAP_START] - LOOP_D[CAP_START]):
                        continue
                    if spm > LOOP_D[EVAP_START] and spm < LOOP_D[EVAP_END] and capk < 0.9:
                        continue
            rad = 6.5 if not in_cap else 3.5
            gasy = (in_evap and all_gas > 0 and t < s("fix2") - 0.12) or spm >= LOOP_D[EVAP_END] or spm < LOOP_D[3]
            if gasy:
                rad *= 0.75
            c.drawCircle(x_, y_, rad, P(col, 0.95))
        if f1 and boil > 0 and t < s("fix2") - 0.12:                 # bubbles as it boils in the evaporator
            for k in range(14):
                q = (t * 1.6 + k / 14.0) % 1.0
                bx, by = loop_at(LOOP_D[EVAP_START] + (k / 14.0) * (LOOP_D[EVAP_END] - LOOP_D[EVAP_START]))
                c.drawCircle(bx + math.sin(k) * 4, by - q * 14, 4 + 4 * q, P("#E0F2FE", 0.8 * boil * (1 - q), stroke=2))
        # the compressor and the coils
        compressor(c, 330, 470, 1.0, t, run=comp_run, hot=sq if t < s("fix3") - 0.12 else 0.6, squeeze=sq if s("fix2") - 0.12 <= t < s("break3") - 0.12 else 0.0)
        if s("fix3") - 0.12 <= t < s("break4") - 0.12:                # heat leaving the back coils into the kitchen
            for k in range(8):
                q = (t * 0.8 + k / 8.0) % 1.0
                yy = -440 + k * 110
                c.drawLine(490 + q * 160, yy, 520 + q * 160, yy - 20, P(HOT, cond * 0.8 * math.sin(q * math.pi), stroke=8))
            heat_lines(c, 500, 760, -500, 380, t, a=cond * 0.6)
        if s("fix2") - 0.12 <= t < s("break3") - 0.12:               # the bike pump that warms up
            bk = prog(t, T["bike"] - 0.3, T["bike"])
            if bk > 0:
                px, py = 560, 300
                c.drawRRect(rr(px - 22, py - 200, 44, 200, 10), P(mix("#6B7280", HOT, bk), bk))
                hy = py - 200 - 60 * (0.5 + 0.5 * math.sin(t * 8))
                c.drawLine(px, py - 200, px, hy, P("#9CA3AF", bk, stroke=10))
                c.drawLine(px - 50, hy, px + 50, hy, P("#1F2937", bk, stroke=16))
                add_glow(c, px, py - 100, 120, HOT, 0.4 * bk)
        if s("break4") - 0.12 <= t < s("reveal") - 0.12:              # the gauge on the high-pressure side
            gf = 0.95 if t < s("fix4") - 0.12 else lerp(0.95, 0.12, prog(t, T["drops"] - 0.3, T["drops"] + 0.4))
            gauge(c, 420, -470, 56, gf + math.sin(t * 20) * 0.01)
            if t >= s("fix4") - 0.12:
                gauge(c, 190, -615, 44, lerp(0.95, 0.12, prog(t, T["drops"] - 0.3, T["drops"] + 0.4)))
                fk = prog(t, T["icy"] - 0.3, T["icy"] + 0.3)
                if fk > 0:
                    add_glow(c, 150, -430, 200, "#BDEFFF", 0.4 * fk)
                    for k in range(10):
                        c.drawCircle(70 + (k * 37) % 160, -470 + (k * 53) % 150, 5, P("#F0F9FF", 0.8 * fk))
        if t >= s("reveal") - 0.12:                                   # thermostat dial and the door seal magnet
            tk = prog(t, T["thermo"] - 0.3, T["thermo"])
            dx, dy = -120, -200
            c.drawCircle(dx, dy, 34, P("#F8FAFC", tk))
            c.drawCircle(dx, dy, 34, P("#1F2937", tk, stroke=4))
            an = math.radians(lerp(140, 40, 0.5 + 0.5 * math.sin(t * 1.5)))
            c.drawLine(dx, dy, dx + math.cos(an) * 26, dy - math.sin(an) * 26, P(HOT, tk, stroke=6))
            on = (int(t * 1.2) % 2 == 0) and t > T["off"]
            c.drawCircle(330, 380, 14, P(GOOD if on else "#7F1D1D", tk))
            mk = prog(t, T["magnet"] - 0.3, T["magnet"] + 0.2)
            if mk > 0:                                               # the gasket in section with a magnet strip
                c.drawRRect(rr(-300, -40, 46, 120, 14), P("#111827", mk))
                c.drawRect(R(-292, -10, 30, 60), P("#DC2626", mk))
                c.drawRect(R(-292, 20, 30, 30), P("#3B82F6", mk))
                for k in range(3):
                    c.drawLine(-262, -4 + k * 26, -236, -4 + k * 26, P("#FDE68A", mk * (0.5 + 0.5 * math.sin(t * 6 + k)), stroke=4))
        c.restore()
        self.ui["cam"] = cam

    def ui_loop(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (60, 120, 0.9))
        at = lambda x, y: self.to_screen(cam, x, y)                 # noqa: E731
        if tw < s("break2") - 0.12:
            ex, ey = at(140, -420)
            self.label(ex, ey, 540, 470, "liquid", T["liquid"] - 0.1, T["soaks"] - 0.2, COOL, size=40)
            self.chip(540, 300, "soak", T["soaks"] - 0.2, s("break2") - 0.15, accent=HOT, size=44)
            self.badge("check", T["heat1"] + 0.2, s("break2") - 0.15, x=920, y=420)
        elif tw < s("fix2") - 0.12:
            self.chip(540, 300, "used", T["gas2"] - 0.2, s("fix2") - 0.15, accent="#A5B4FC", size=44)
            self.badge("alert", T["used1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["used1"], 1.2)
        elif tw < s("break3") - 0.12:
            px, py = at(330, 420)
            self.label(px, py, 540, 470, "comp", T["comp"] - 0.1, T["hot"] - 0.2, "#E5E7EB", size=42)
            self.chip(540, 300, "squeeze", T["hot"] - 0.2, s("break3") - 0.15, accent=HOT, size=42)
            self.badge("check", T["bike"] + 0.2, s("break3") - 0.15, x=920, y=420)
        elif tw < s("fix3") - 0.12:
            self.chip(540, 300, "holds", T["gas3"] - 0.2, s("fix3") - 0.15, accent=HOT, size=44)
            self.badge("alert", T["heat3b"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["heat3b"], 1.2)
        elif tw < s("break4") - 0.12:
            self.chip(540, 300, "coils", T["coils"] - 0.2, T["escape"] - 0.2, accent=WARN, size=42)
            self.chip(540, 300, "escape", T["escape"] - 0.2, T["liquid3"] - 0.2, accent=HOT, size=40)
            self.chip(540, 300, "back", T["liquid3"] - 0.2, s("break4") - 0.15, accent=COOL, size=44)
            self.badge("check", T["liquid3"] + 0.2, s("break4") - 0.15, x=920, y=420)
        elif tw < s("fix4") - 0.12:
            self.chip(540, 300, "press", T["liq4"] - 0.2, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["press1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["press1"], 1.2)
        elif tw < s("cta") - 0.12:
            self.chip(540, 300, "tube", T["tube"] - 0.2, T["drops"] - 0.2, accent="#E5E7EB", size=38)
            self.chip(540, 300, "icy", T["drops"] - 0.2, s("cta") - 0.15, accent=COOL, size=40)
            self.badge("check", T["loop1"], s("cta") - 0.15, x=920, y=420)
        elif tw >= s("reveal") - 0.12:
            dx, dy = at(-120, -200)
            self.label(dx, dy, 600, 470, "thermo", T["thermo"] - 0.1, T["magnet"] - 0.3, HILITE, size=42)
            self.chip(540, 300, "magnet", T["magnet"] - 0.2, s("stat") - 0.15, accent="#F87171", size=42)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1E1B3A", "#14122A"])
        c.drawRect(R(0, 1240, W, H - 1240), P("#2A2438"))
        fridge_front(c, 120, 360, 440, 880, t, door=1.0, light=1.0, frost=1.0, lit=1.2, food_k=0.0)
        add_glow(c, 520, 900, 420, "#9CC8E8", 0.18)
        sk = prog(t, T["t_stand"] - 0.4, T["t_stand"])
        person(c, 700, 1240, 520, "#6366F1", t, pose="look", face=-1, hat="none", hair="#2B2530", a=max(0.0, sk))
        ck = prog(t, T["t_pumps"], T["t_pumps"] + 0.4)               # the clock on the wall spinning
        c.drawCircle(860, 420, 70, P("#F8FAFC", ck))
        c.drawCircle(860, 420, 70, P("#1F2937", ck, stroke=6))
        an = t * 6.0
        c.drawLine(860, 420, 860 + math.cos(an) * 50, 420 + math.sin(an) * 50, P("#1F2937", ck, stroke=5))
        c.drawLine(860, 420, 860 + math.cos(an / 12) * 32, 420 + math.sin(an / 12) * 32, P("#1F2937", ck, stroke=7))
        if self.rtl:
            mk = prog(t, T["t_food"] - 0.5, T["t_food"])
            if mk > 0:
                from phone import mom
                mom(c, lerp(1200, 960, e_out(mk)), 1240, 320, t, a=1.0)

    def ui_tag(self, c, t, tw):
        T = self.T
        if self.rtl:
            self.chip(540, 300, "wait", T["t_open"] - 0.1, T["t_food"] - 0.1, accent="#BDEFFF", size=42)
            bubble(c, 700, 620, self.L["bubble"], self.span(T["t_food"] - 0.1, self.duration + 1), tail_left=False, size=52)
        else:
            self.chip(540, 300, "wait", T["t_open"] - 0.1, self.duration + 1, accent="#BDEFFF", size=42)

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#2A1E2E", "#3A2626"]))

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hum(max(1.5, T["congrats"]), 60.0), -20), (T["milk"] - 0.3, sfx.lock_click(61), -8),
              (T["cold"], sfx.whoosh(0.6, False, 62), -12), (T["cold"] + 0.1, sfx.sparkle(0.7, 9, 63), -10),
              (T["ice"], sfx.sizzle(0.8, 64), -14), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8), (T["fridge"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["sawn"], sfx.creak(0.8, 68), -12),
               (T["lakes"] + 0.2, sfx.whoosh(0.6, False, 69), -10), (T["india"], sfx.hiss(1.0, 70), -14),
               (T["india"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 71), -4), (T["boils"], sfx.sizzle(0.9, 72), -12),
               (T["soaks"], sfx.whirr(0.8, 220.0, 160.0, 73), -14), (T["heat1"] + 0.2, sfx.ding(), -8),
               (T["heat1"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["gas2"], sfx.hiss(0.7, 75), -12),
               (T["used1"], sfx.power_down(1.0, 76), -10), (T["used1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 77), -4), (T["comp"], sfx.hum(1.6, 90.0), -12),
               (T["squeeze"], sfx.thunk(78), -8), (T["hot"], sfx.sizzle(0.6, 79), -12), (T["bike"], sfx.hiss(0.4, 80), -10),
               (T["bike"] + 0.4, sfx.hiss(0.4, 81), -10), (T["bike"] + 0.5, sfx.ding(), -8), (T["bike"] + 0.7, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 82), -4), (T["heat3b"], sfx.sizzle(0.6, 83), -12),
               (T["heat3b"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 84), -4), (T["escape"], sfx.whoosh(0.7, True, 85), -12),
               (T["liquid3"], sfx.pop(86), -8), (T["liquid3"] + 0.2, sfx.ding(), -8), (T["liquid3"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 87), -4), (T["press1"] - 0.2, sfx.creak(0.6, 88), -12),
               (T["press1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 89), -4), (T["spag"], sfx.hiss(0.9, 90), -12),
               (T["drops"], sfx.whoosh(0.5, False, 91), -10), (T["icy"], sfx.sparkle(0.7, 10, 92), -8),
               (T["loop1"], sfx.ding(), -8), (T["loop1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(93), 0), (T["follow"] - 0.15, sfx.pop(94), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 95), -6), (T["thermo"], sfx.click(96), -6),
               (T["off"], sfx.click(97), -8), (T["seal"], sfx.lock_click(98), -4)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 99), -6), (T["s1"], sfx.pop(100), -3), (T["s2"], sfx.pop(101), -3),
               (T["s3"], sfx.pop(102), -3)]
        ev += [(T["cong2"], sfx.pop(103), -2), (T["cong2"], sfx.sparkle(1.0, 14, 104), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 105), -6), (T["t_pumps"], sfx.hum(2.5, 60.0), -18),
               (T["t_stand"], sfx.tick(), -8), (T["t_open"], sfx.tick(), -8), (T["t_food"], sfx.pop(106), -6)]
        return ev


NAME = "fridge"
EPISODE = Fridge
