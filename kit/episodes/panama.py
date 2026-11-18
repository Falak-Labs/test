"""Episode 40 - The Panama Canal locks: a cargo ship climbs a staircase of water into the jungle hills.  v2 look:
tropical dusk, rain clouds over green hills, concrete lock chambers, a container ship.

Sets: canal (hook: the ship rises chamber by chamber up the staircase, rain over the hills; the reveal: the whole canal
in profile, up three steps, across the lake, down three to the Pacific; the stat; the closer back on the climbing
ship), map (break1: the Americas, the long way round South America), dam (fix1: a dam on the river, a lake fills high
above the sea, a ship crosses it), lock (break2: a ship tries to sail uphill and slides back; fix2: one chamber in
section: the gate shuts, lake water runs down a tunnel in the wall and up through the floor, no pumps, the ship rises
like a bath toy), gate (break3: one gate leaf = 400 cars; fix3: x-ray, hollow, half floating, small motors swing the
two leaves into a V), mules (break4: from above, the ship barely fits and scrapes the wall; fix4: electric mules on
the walls hold it on cables, dead center; the cta), swim (the tag: a swimmer weighed like a ship, a 36-cent toll; airport
water in English, the parking guy waving "come, come" in Arabic).
World (canal): side view, sea level y = 0, up is negative; one step = STEP units; Gatun chambers from x = -450.
"""
from v2_base import *  # noqa: F401,F403

DUSK = {"top": "#0B1030", "upper": "#1E2156", "mid": "#55306E", "low": "#C4566A", "horizon": "#F7A07A",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STEP, CW = 100.0, 300.0                  # height of one step, length of one chamber
X0 = -450.0                              # sea gate of the first (Gatun) chamber
LAKE_Y = -3 * STEP
LAKE_X0, LAKE_X1 = X0 + 3 * CW, X0 + 3 * CW + 1500.0
PAC_X0 = LAKE_X1                         # first gate of the Pacific steps
DEPTH = 90.0                             # water depth in a chamber at its low level
CONC, CONC_D = "#A8B0BE", "#5D6577"
WATER, WATER_D = "#2B7BBF", "#0E3460"
JUNGLE = ("#1F5A3A", "#0E2A1E")
STEEL_G = "#3C4658"
BOX_COLS = ("#EF4444", "#F59E0B", "#3B82F6", "#22C55E", "#E5E7EB", "#A855F7", "#14B8A6", "#F97316")


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


# ====================================================================================== pieces
def cargo_ship(c, x, y, L, t, a=1.0, face=1, tilt=0.0, lit=1.0):
    """A container ship from the side: waterline at y, centred on x, bow toward face (1 = right), length L."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    if tilt:
        c.rotate(tilt)
    k = L / 260.0
    c.scale(face * k, k)
    hull = skia.Path()
    hull.moveTo(-130, -26)
    hull.lineTo(116, -26)
    hull.quadTo(142, -26, 138, -8)
    hull.lineTo(120, 34)
    hull.lineTo(-114, 34)
    hull.quadTo(-130, 30, -131, 8)
    hull.close()
    c.drawPath(hull, lin_paint(0, -26, 0, 34, ["#263456", "#18223D", "#9F1D1D", "#6B1313"], [0, 0.5, 0.52, 1], a=a))
    c.drawLine(-128, -24, 122, -24, P("#E5E7EB", 0.7 * a, stroke=2.5))
    rng = random.Random(7)
    for tier in range(4):                                        # the containers, four high
        for k_ in range(9):
            if tier == 3 and k_ in (0, 8):
                continue
            bx = -70 + k_ * 20.5
            col = BOX_COLS[rng.randrange(len(BOX_COLS))]
            by = -26 - (tier + 1) * 12.5
            c.drawRect(R(bx, by, 19.5, 12), lin_paint(0, by, 0, by + 12, [shade(col, 0.15), shade(col, -0.25)], a=a))
            c.drawLine(bx + 6.5, by + 1, bx + 6.5, by + 11, P(shade(col, -0.4), 0.6 * a, stroke=1))
            c.drawLine(bx + 13, by + 1, bx + 13, by + 11, P(shade(col, -0.4), 0.6 * a, stroke=1))
    c.drawRect(R(-122, -96, 40, 70), lin_paint(-122, 0, -82, 0, ["#F8FAFC", "#CBD5E1"], a=a))      # the bridge
    c.drawRect(R(-128, -100, 52, 8), P("#E2E8F0", a))
    for row in range(3):
        for k_ in range(4):
            c.drawRect(R(-118 + k_ * 9, -88 + row * 17, 6, 7), P(mix("#334155", "#FDE68A", lit), a))
    c.drawRect(R(-116, -124, 14, 26), P("#1F2937", a))                                               # funnel
    c.drawRect(R(-116, -124, 14, 6), P("#EF4444", a))
    c.restore()


def water(c, x0, x1, y0, y1, t, a=1.0, lit=0.6):
    """A body of water from surface y0 down to y1."""
    if a <= 0 or y1 <= y0:
        return
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), lin_paint(0, y0, 0, y1, [WATER, "#1B5C99", WATER_D], a=0.94 * a))
    c.drawRect(R(x0, y0, x1 - x0, 5), P("#BFE6FF", 0.55 * a * lit))
    xx = x0 + 20
    while xx < x1 - 30:
        dx = math.sin(t * 1.7 + xx * 0.05) * 6
        c.drawLine(xx + dx, y0 + 12, xx + dx + 26, y0 + 12, P("#93C5FD", 0.35 * a, stroke=2.5))
        xx += 70


def concrete(c, x, y, w, h, a=1.0):
    c.drawRect(R(x, y, w, h), lin_paint(x, 0, x + w, 0, [shade(CONC, 0.1), CONC, CONC_D], a=a))
    c.drawRect(R(x, y, w, 6), P("#E5E7EB", 0.6 * a))


def gate_side(c, x, ytop, ybot, closed, a=1.0):
    """A lock gate seen from the side: solid when closed, a faint outline when it is open."""
    k = clamp(closed)
    c.drawRect(R(x - 9, ytop, 18, ybot - ytop), P(STEEL_G, a * (0.12 + 0.88 * k)))
    if k > 0.3:
        for i in range(1, 6):
            yy = lerp(ytop, ybot, i / 6.0)
            c.drawLine(x - 9, yy, x + 9, yy, P("#64748B", 0.8 * a * k, stroke=2))
    else:
        c.drawRect(R(x - 9, ytop, 18, ybot - ytop), P("#94A3B8", 0.5 * a, stroke=2))


def jungle(c, x0, x1, y, t, s=1.0, a=1.0, seed=3):
    """A strip of rainforest trees along y (round crowns, a few palms)."""
    rng = random.Random(seed)
    xx = x0
    while xx < x1:
        r = rng.uniform(26, 48) * s
        col = rng.choice(["#1E6B43", "#195C39", "#237A4B", "#14492E"])
        c.drawCircle(xx, y - r * 0.8, r, P(col, a))
        c.drawCircle(xx - r * 0.3, y - r * 1.3, r * 0.6, P(shade(col, 0.12), a))
        xx += r * 1.1


def rain(c, x0, x1, y0, y1, t, a=1.0, n=80, seed=5):
    if a <= 0:
        return
    rng = random.Random(seed)
    for i in range(n):
        x = rng.uniform(x0, x1)
        sp = rng.uniform(900, 1300)
        yy = y0 + ((t * sp + rng.uniform(0, 3000)) % (y1 - y0))
        c.drawLine(x, yy, x - 10, yy + 38, P("#BFDBFE", 0.45 * a, stroke=3))


def rain_cloud(c, x, y, s, t, a=1.0, seed=0):
    v2.cloud(c, x, y, s, body="#2E3560", rim="#7C86C9", a=a, seed=seed)


def duck(c, x, y, s=1.0, a=1.0, t=0.0):
    """A rubber bath duck floating at waterline y."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y + math.sin(t * 3) * 3)
    c.scale(s, s)
    c.drawOval(R(-40, -30, 80, 40), P("#FACC15", a))
    c.drawCircle(18, -42, 20, P("#FACC15", a))
    c.drawCircle(24, -47, 4, P("#111827", a))
    bill = skia.Path()
    bill.moveTo(34, -42)
    bill.lineTo(54, -38)
    bill.lineTo(34, -33)
    bill.close()
    c.drawPath(bill, P("#F97316", a))
    c.restore()


def ship_top(c, x, y, Wd, Ln, a=1.0):
    """A container ship from above, bow pointing up the screen; (x, y) = centre of the bow end, width Wd."""
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(x, y)
    p.quadTo(x + Wd * 0.5, y + Wd * 0.1, x + Wd * 0.5, y + Wd * 0.5)
    p.lineTo(x + Wd * 0.5, y + Ln)
    p.lineTo(x - Wd * 0.5, y + Ln)
    p.lineTo(x - Wd * 0.5, y + Wd * 0.5)
    p.quadTo(x - Wd * 0.5, y + Wd * 0.1, x, y)
    p.close()
    c.drawPath(p, lin_paint(x - Wd / 2, 0, x + Wd / 2, 0, ["#1B2540", "#2E3E66", "#1B2540"], a=a))
    rng = random.Random(3)
    rows = int((Ln - Wd * 0.8 - 140) / 44)
    for r_ in range(rows):
        yy = y + Wd * 0.62 + r_ * 44
        for k_ in range(6):
            col = BOX_COLS[rng.randrange(len(BOX_COLS))]
            bw = (Wd - 30) / 6.0
            c.drawRect(R(x - Wd / 2 + 15 + k_ * bw, yy, bw - 3, 40), P(col, 0.92 * a))
    c.drawRect(R(x - Wd * 0.45, y + Ln - 120, Wd * 0.9, 90), P("#F1F5F9", a))


def mule(c, x, y, s=1.0, a=1.0, face=1):
    """A canal mule (electric locomotive) from above, centred at (x, y), long axis up the screen."""
    if a <= 0:
        return
    c.drawRRect(rr(x - 26 * s, y - 52 * s, 52 * s, 104 * s, 10 * s), lin_paint(x - 26 * s, 0, x + 26 * s, 0,
                                                                               ["#B91C1C", "#EF4444", "#B91C1C"], a=a))
    c.drawRRect(rr(x - 18 * s, y - 40 * s, 36 * s, 28 * s, 6 * s), P("#BFE6FF", 0.8 * a))
    c.drawRect(R(x - 22 * s, y + 8 * s, 44 * s, 6 * s), P("#FDE68A", a))
    c.drawCircle(x + face * 18 * s, y, 7 * s, P("#1F2937", a))


def car_icon(c, x, y, s, col, a=1.0):
    c.drawRRect(rr(x - 14 * s, y - 6 * s, 28 * s, 10 * s, 4 * s), P(col, a))
    c.drawRRect(rr(x - 8 * s, y - 12 * s, 16 * s, 8 * s, 3 * s), P(shade(col, -0.2), a))
    c.drawCircle(x - 8 * s, y + 4 * s, 3.6 * s, P("#111827", a))
    c.drawCircle(x + 8 * s, y + 4 * s, 3.6 * s, P("#111827", a))


def pump(c, x, y, s=1.0, a=1.0):
    """A water pump icon (to cross out)."""
    c.drawRRect(rr(x - 50 * s, y - 40 * s, 100 * s, 80 * s, 14 * s), P("#64748B", a))
    c.drawCircle(x, y, 26 * s, P("#94A3B8", a))
    c.drawRect(R(x + 40 * s, y - 14 * s, 40 * s, 28 * s), P("#64748B", a))
    c.drawRect(R(x - 80 * s, y - 14 * s, 40 * s, 28 * s), P("#64748B", a))


# ====================================================================================== the episode
class Panama(EpisodeV2):
    BUILD_NO = 40
    FIRST_SET = "canal"
    CLEAR = "#0B1030"
    TITLE = {"en": "PANAMA CANAL LOCKS", "ar_sa": "هويس قناة بنما"}
    EMPH = {"en": ["CONGRATS", "CARGO", "SHIP", "CLIMB", "STAIRCASE", "MOUNTAINS", "RAIN", "PANAMA", "CANAL", "LOCKS",
                   "ATLANTIC", "PACIFIC", "AROUND", "WEEKS", "DAM", "GIANT", "LAKE", "HILLS", "UPHILL", "WATER",
                   "STEPS", "BOX", "GATES", "CLOSE", "FLOOR", "PUMPS", "BATH", "TOY", "BIGGEST", "HUNDRED", "CARS",
                   "HOLLOW", "FLOAT", "MOTORS", "WEAKER", "BARELY", "HALF", "METER", "LOCOMOTIVES", "MULES",
                   "STEEL", "CABLES", "CENTER", "FOLLOW", "DUTCH", "STORM", "BARRIER", "THREE", "OCEAN",
                   "TWENTY-SIX", "MILLION", "YOURSELF", "SWAM", "WEIGHED", "THIRTY-SIX", "CENTS", "AIRPORT"],
            "ar_sa": ["مبروك", "مركب", "عملاق", "يطلع", "سلم", "الجبل", "المطر", "هويس", "قناة", "بنما", "السويس",
                      "المستوية", "المحيطين", "جبال", "حوالين", "أسابيع", "فتسد", "نهر", "بحيرة", "عملاقة", "العالي",
                      "سلالم", "صندوق", "تتقفل", "الأرضية", "طلمبة", "وترفعه", "لعبة", "البانيو", "بوابة",
                      "أربعمية", "عربية", "مجوفة", "عايمة", "أضعف", "بالعافية", "نص", "متر", "فقاطرات", "البغال",
                      "بحبال", "حديد", "تابعني", "حاجز", "العواصف", "الهولندي", "تلات", "البحيرة", "للمحيط",
                      "وعشرين", "ميتين", "مليون", "بإيدك", "عوم", "وزنوه", "سنت", "والسايس", "تعالى"]}
    KEYS = {"ar_sa": {
        ("hook", "SHIP"): "مركب", ("hook", "CLIMB"): "يطلع", ("hook", "STAIRCASE"): "سلم", ("hook", "MOUNTAINS"): "الجبل",
        ("hook", "RAIN"): "المطر", ("hook", "CONGRATS"): "مبروك", ("hook", "PANAMA"): "هويس",
        ("break1", "MOUNTAINS"): "جبال", ("break1", "ATLANTIC"): "المحيطين", ("break1", "AROUND"): "حوالين",
        ("break1", "WEEKS"): "أسابيع",
        ("fix1", "DAM"): "فتسد", ("fix1", "LAKE"): "بحيرة", ("fix1", "HILLS"): "الجبل", ("fix1", "CROSS"): "تعدي",
        ("break2", "UPHILL"): "العالي",
        ("fix2", "STEPS"): "سلالم", ("fix2", "BOX"): "صندوق", ("fix2", "CLOSE"): "تتقفل", ("fix2", "POURS"): "تدخل",
        ("fix2", "FLOOR"): "الأرضية", ("fix2", "PUMPS"): "طلمبة", ("fix2", "LIFTING"): "وترفعه", ("fix2", "TOY"): "لعبة",
        ("break3", "GATES"): "بوابة", ("break3", "HUNDRED"): "أربعمية", ("break3", "CARS"): "عربية",
        ("fix3", "HOLLOW"): "مجوفة", ("fix3", "FLOAT"): "عايمة", ("fix3", "MOTORS"): "وموتورات", ("fix3", "WEAKER"): "أضعف",
        ("fix3", "SWING"): "تفتحها",
        ("break4", "BIG"): "الكبير", ("break4", "BARELY"): "بالعافية", ("break4", "HALF"): "نص", ("break4", "SIDE"): "ناحية",
        ("fix4", "LOCOMOTIVES"): "فقاطرات", ("fix4", "MULES"): "البغال", ("fix4", "CABLES"): "بحبال", ("fix4", "CENTER"): "النص",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "UP"): "طلعه", ("reveal", "ACROSS"): "عديه", ("reveal", "DOWN"): "ونزله", ("reveal", "OCEAN"): "للمحيط",
        ("stat", "TWENTY"): "ستة", ("stat", "HUNDRED"): "ميتين", ("stat", "OVER"): "وأكتر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SWAM"): "عوم", ("tag", "WEIGHED"): "وزنوه", ("tag", "CENTS"): "سنت", ("tag", "AIRPORT"): "والسايس"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Dutch storm barrier"),
                   "stat": [("26 m", "LIFTED BY WATER"), ("200M", "LITERS PER SHIP"), ("1M+", "SHIPS SINCE 1914")],
                   "L": {"climb": "A SHIP CLIMBS STAIRS", "rain": "RUNS ON RAIN", "locks": "PANAMA CANAL LOCKS",
                         "split": "MOUNTAINS IN THE WAY", "atl": "ATLANTIC", "pac": "PACIFIC", "weeks": "THE LONG WAY: WEEKS",
                         "panama": "PANAMA", "dam": "DAM THE RIVER", "lake": "A GIANT LAKE", "high": "26 m ABOVE THE SEA",
                         "sea": "SEA LEVEL", "cross": "SHIPS CROSS ON IT", "uphill": "SHIPS CAN'T SAIL UPHILL",
                         "steps": "WATER STEPS", "box": "A CONCRETE BOX", "close": "GATES CLOSE",
                         "tunnel": "TUNNEL FROM THE LAKE", "floor": "IN THROUGH THE FLOOR", "nopump": "NO PUMPS",
                         "toy": "LIKE A BATH TOY", "heavy": "ONE GATE LEAF", "cars": "= 400 CARS", "tonnes": "UP TO 662 t",
                         "hollow": "HOLLOW", "floats": "HALF FLOATS", "motor": "MOTORS WEAKER THAN A CAR'S",
                         "swing": "THE TWO LEAVES SWING SHUT", "tight": "BARELY FITS", "gap": "0.6 m EACH SIDE",
                         "scrape": "SCRAPE!", "mules": "MULES: ELECTRIC LOCOMOTIVES", "cables": "STEEL CABLES",
                         "center": "DEAD CENTER", "up3": "UP 3 STEPS", "acrossl": "ACROSS THE LAKE", "down3": "DOWN 3 STEPS",
                         "other": "THE OTHER OCEAN", "swam": "1928: HE SWAM IT", "weigh": "WEIGHED LIKE A SHIP",
                         "lbs": "140 lb", "toll": "TOLL: $0.36", "water7": "$7", "airport": "AIRPORT WATER"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: حاجز العواصف الهولندي"),
                      "stat": [("26", "متر لفوق بالمية"), ("200", "مليون لتر لكل مركب"), ("1914", "أكتر من مليون مركب من سنة")],
                      "L": {"climb": "مركب بيطلع سلم", "rain": "شغال بالمطر", "locks": "هويس قناة بنما",
                            "split": "جبال في النص", "atl": "الأطلسي", "pac": "الهادي", "weeks": "اللفة: أسابيع",
                            "panama": "بنما", "dam": "سد على النهر", "lake": "بحيرة عملاقة", "high": "26 متر فوق البحر",
                            "sea": "مستوى البحر", "cross": "والمراكب تعدي عليها", "uphill": "المركب مبيطلعش العالي",
                            "steps": "سلالم مية", "box": "صندوق خرسانة", "close": "البوابات تتقفل",
                            "tunnel": "نفق من البحيرة", "floor": "تدخل من الأرضية", "nopump": "من غير طلمبة",
                            "toy": "زي لعبة البانيو", "heavy": "بوابة واحدة", "cars": "= 400 عربية", "tonnes": "لحد 662 طن",
                            "hollow": "مجوفة", "floats": "نص عايمة", "motor": "موتورات أضعف من موتور العربية",
                            "swing": "الضلفتين بيتقفلوا", "tight": "داخل بالعافية", "gap": "نص متر من كل ناحية",
                            "scrape": "خبط!", "mules": "البغال: قاطرات كهربا", "cables": "حبال حديد",
                            "center": "في النص بالظبط", "up3": "تلات درجات لفوق", "acrossl": "عدّيه البحيرة",
                            "down3": "تلاتة لتحت", "other": "المحيط التاني", "swam": "عدّاها عوم", "weigh": "وزنوه زي المركب",
                            "lbs": "64 كيلو", "toll": "الرسوم: 36 سنت", "water7": "تعالى تعالى!", "airport": "السايس"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "ship": ("hook", "SHIP", 0.1), "climb": ("hook", "CLIMB", 0.2), "stair": ("hook", "STAIRCASE", 0.3),
            "mount": ("hook", "MOUNTAINS", 0.42), "rain": ("hook", "RAIN", 0.55), "congrats": ("hook", "CONGRATS", 0.7),
            "panama": ("hook", "PANAMA", 0.85),
            "mts": ("break1", "MOUNTAINS", 0.1), "atl": ("break1", "ATLANTIC", 0.3), "around": ("break1", "AROUND", 0.65),
            "weeks": ("break1", "WEEKS", 0.9),
            "dam": ("fix1", "DAM", 0.1), "lake": ("fix1", "LAKE", 0.4), "hills": ("fix1", "HILLS", 0.6),
            "cross": ("fix1", "CROSS", 0.85),
            "uphill": ("break2", "UPHILL", 0.7),
            "steps": ("fix2", "STEPS", 0.1), "box": ("fix2", "BOX", 0.25), "close": ("fix2", "CLOSE", 0.38),
            "pours": ("fix2", "POURS", 0.5), "floor": ("fix2", "FLOOR", 0.62), "pumps": ("fix2", "PUMPS", 0.72),
            "lift": ("fix2", "LIFTING", 0.82), "toy": ("fix2", "TOY", 0.93),
            "gates": ("break3", "GATES", 0.25), "hundred": ("break3", "HUNDRED", 0.65), "cars": ("break3", "CARS", 0.85),
            "hollow": ("fix3", "HOLLOW", 0.2), "float": ("fix3", "FLOAT", 0.4), "motors": ("fix3", "MOTORS", 0.6),
            "weaker": ("fix3", "WEAKER", 0.72), "swing": ("fix3", "SWING", 0.9),
            "big": ("break4", "BIG", 0.1), "barely": ("break4", "BARELY", 0.45), "half": ("break4", "HALF", 0.6),
            "side": ("break4", "SIDE", 0.9),
            "loco": ("fix4", "LOCOMOTIVES", 0.15), "mules": ("fix4", "MULES", 0.4), "cables": ("fix4", "CABLES", 0.65),
            "center": ("fix4", "CENTER", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "up": ("reveal", "UP", 0.15), "across": ("reveal", "ACROSS", 0.45), "down": ("reveal", "DOWN", 0.7),
            "ocean": ("reveal", "OCEAN", 0.9),
            "s1": ("stat", "TWENTY", 0.04), "s2": ("stat", "HUNDRED", 0.35), "s3": ("stat", "OVER", 0.68),
            "cong2": ("closer", "CONGRATS", 0.16),
            "swam": ("tag", "SWAM", 0.15), "weighed": ("tag", "WEIGHED", 0.35), "cents": ("tag", "CENTS", 0.65),
            "airport": ("tag", "AIRPORT", 0.85)})
        T["scrape"] = max(T["side"] - 0.3, T["barely"] + 0.2)
        T["valve"] = max(T["pours"] - 0.25, T["close"] + 0.3)
        T["rise"] = T["valve"] + 0.35
        T["stack"] = max(T["hundred"] - 0.3, s("break3") + 0.2)
        T["xr"] = max(T["hollow"] - 0.25, s("fix3") + 0.05)
        T["shut"] = max(T["swing"] - 0.3, T["weaker"] + 0.2)
        # ---- sets
        self.cut(s("break1") - 0.12, "map", 1)
        self.cut(s("fix1") - 0.12, "dam", -1)
        self.cut(s("break2") - 0.12, "lock", 1)
        self.cut(s("break3") - 0.12, "gate", -1)
        self.cut(s("break4") - 0.12, "mules", 1)
        self.cut(s("reveal") - 0.12, "canal", -1)
        self.cut(s("tag") - 0.2, "swim", 1)
        # ---- the climb: 0..3 = chambers passed; hook climbs from 0 to 3, the closer shows it again
        h0, h1 = 0.0, s("break1") - 0.3
        lin = (lambda x: x)
        self.climb_hook = Track(0.15).to(h0 + 0.05, 3.05, h1 - h0 - 0.05, lin)
        self.climb_close = Track(0.6).to(s("closer") - 0.1, 0.6, 0.0).to(s("closer"), 1.6, e("closer") - s("closer"), lin)
        # reveal: a ship through the whole canal (u: 0..3 up, 3..4 lake, 4..7 down, 7..7.5 ocean)
        r0 = s("reveal") + 0.05
        self.trip = Track(0.0).to(r0, 3.0, max(0.3, T["across"] - r0), lin).to(T["across"], 4.0, max(0.3, T["down"] - T["across"]), lin) \
            .to(T["down"], 7.0, max(0.3, T["ocean"] - T["down"]), lin).to(T["ocean"], 7.5, max(0.3, s("stat") - 0.15 - T["ocean"]), lin)
        cm = Camera(-20, -105, 0.95)
        cm.key(0.05, -20, -105, 0.95, 0.0).key(T["stair"], 120, -140, 0.88, 3.0).key(T["congrats"], 260, -160, 0.84, 2.4)
        cm.key(s("reveal") - 0.12, -60, -95, 0.42, 0.0).key(T["across"], 1150, -95, 0.42, 1.2)
        cm.key(T["down"], 2350, -95, 0.42, 1.0).key(T["ocean"], 3050, -95, 0.42, 1.0)
        cm.key(s("stat") - 0.12, 1250, -150, 0.27, 0.0)
        cm.key(s("closer") - 0.1, -20, -105, 0.95, 0.0).key(self.duration, 10, -115, 0.98, 2.0)
        self.cam = cm
        self.spans = [(T["weeks"], T["cross"] + 0.3), (T["uphill"], T["toy"] + 0.3), (T["cars"], T["swing"] + 0.3),
                      (T["side"], T["center"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 7), (T["uphill"] + 0.1, 0.35, 9), (T["stack"] + 0.4, 0.3, 7),
                       (T["scrape"], 0.5, 10), (T["shut"] + 0.5, 0.3, 8), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    @staticmethod
    def levels(u):
        """Water level of each Gatun chamber and the ship's (x, waterline) for climb progress u (0..3)."""
        lv = []
        for k in range(3):
            lo, hi = -k * STEP, -(k + 1) * STEP
            f = clamp((u - k) / 0.5) if u > k else 0.0
            lv.append(lerp(lo, hi, e_io(f)))
        k = int(clamp(math.floor(u), 0, 2))
        f = u - k
        cx = X0 + CW * (k + 0.5)
        if f <= 0.5:
            x = cx
        else:
            nx = X0 + CW * (k + 1.5) if k < 2 else LAKE_X0 + 260
            x = lerp(cx, nx, e_io((f - 0.5) / 0.5))
        y = lv[k] if f <= 0.5 or k < 2 else lerp(lv[2], LAKE_Y, e_io(clamp((f - 0.5) / 0.2)))
        if u >= 3.0:
            x = LAKE_X0 + 260 + (u - 3.0) * 600
            y = LAKE_Y
        return lv, x, y

    @staticmethod
    def gate_closed(g, u):
        """How closed gate g (0 = sea gate .. 3 = lake gate) is for climb progress u."""
        if g == 0:
            return 1 - clamp((0.05 - u) / 0.05) if u < 0.05 else 1.0
        o0, o1 = g - 0.5, g + 0.05                       # open while the ship passes from chamber g-1 to g
        if o0 <= u < o1:
            return 1 - clamp(min((u - o0) / 0.06, (o1 - u) / 0.06))
        return 1.0

    def terrain(self, c, t, cam, wide=False):
        """Sky, hills, rain clouds, the ground cut open under the canal (world space is set up here; caller restores)."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 40 * z)
        v2.stars(c, W, H, t, 0.5)
        c.save()
        c.translate(W / 2 - cx * z * 0.25, gy - 330 * z)
        v2.ridge(c, -1600, 1600, 0, 300, "#2A4A5A", "#183040", seed=12, step=110, rough=0.6)
        c.restore()
        self.view(c, cam)
        # far jungle hills behind the lake
        v2.ridge(c, -1200, 3400, LAKE_Y + 40, 420, JUNGLE[0], JUNGLE[1], seed=4, step=90, rough=0.6, depth=900, peaks=9)
        jungle(c, -500, 2600, LAKE_Y + 30, t, 1.0, 0.95, seed=8)
        # earth under everything
        prof = skia.Path()
        prof.moveTo(-2600, 140)
        prof.lineTo(X0 - 40, 140)
        for k in range(3):
            prof.lineTo(X0 + k * CW, -k * STEP + DEPTH + 30)
            prof.lineTo(X0 + (k + 1) * CW, -k * STEP + DEPTH + 30)
        prof.lineTo(LAKE_X0, LAKE_Y + 150)
        prof.lineTo(LAKE_X1, LAKE_Y + 150)
        for k in range(3):
            prof.lineTo(PAC_X0 + k * CW, LAKE_Y + (k + 1) * STEP + DEPTH + 30 - STEP)
            prof.lineTo(PAC_X0 + (k + 1) * CW, LAKE_Y + (k + 1) * STEP + DEPTH + 30)
        prof.lineTo(PAC_X0 + 3 * CW + 40, 140)
        prof.lineTo(5600, 140)
        prof.lineTo(5600, 9000)
        prof.lineTo(-2600, 9000)
        prof.close()
        c.drawPath(prof, lin_paint(0, LAKE_Y, 0, 900, ["#5B3F2A", "#3D2A1C", "#21160E"]))
        tex(c, prof, "stone", 1.0, 0.25)
        # the two oceans
        water(c, -2600, X0 - 40, 0, 140, t)
        water(c, PAC_X0 + 3 * CW + 40, 5600, 0, 140, t)
        c.drawRect(R(-2600, 140, 8200, 8860), lin_paint(0, 140, 0, 1200, ["#3D2A1C", "#21160E"]))
        return gy

    def staircase(self, c, t, u, side="atl", u_ship=None, ship_a=1.0, ship_len=250):
        """Three chambers going up (side 'atl') or down ('pac', mirrored on the Pacific side)."""
        lv, sx, sy = self.levels(u)
        for k in range(3):
            if side == "atl":
                x0 = X0 + k * CW
                floor = -k * STEP + DEPTH
                level = lv[k]
                top = -(k + 1) * STEP - 30
            else:
                x0 = PAC_X0 + k * CW
                floor = LAKE_Y + (k + 1) * STEP + DEPTH
                level = LAKE_Y + (k + 1) * STEP
                top = LAKE_Y + k * STEP - 30
            water(c, x0 + 10, x0 + CW - 10, level, floor, t)
            concrete(c, x0 + CW - 10 if side == "atl" else x0 - 10, top, 20, floor - top + 20)
            c.drawRect(R(x0, floor, CW, 22), P(CONC_D))
        for g in range(4):
            if side == "atl":
                gx = X0 + g * CW
                ytop = -g * STEP - 30 if g > 0 else -30
                ybot = (-(g - 1) * STEP + DEPTH) if g > 0 else DEPTH
                ytop = min(ytop, -(g) * STEP - 30)
                gate_side(c, gx, -(g) * STEP - 34 if g < 3 else LAKE_Y - 34, ybot, self.gate_closed(g, u))
            else:
                gx = PAC_X0 + g * CW
                gate_side(c, gx, LAKE_Y + g * STEP - 34 if g > 0 else LAKE_Y - 34,
                          LAKE_Y + (g + 1) * STEP + DEPTH if g < 3 else DEPTH, 1.0)
        concrete(c, X0 - 40, -30, 40, DEPTH + 60)
        if side == "atl" and ship_a > 0:
            cargo_ship(c, sx, sy, ship_len, t, a=ship_a)

    # ------------------------------------------------------------------ set: canal (hook, reveal, stat, closer)
    def draw_canal(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        rv = t >= s("reveal") - 0.12
        hook = t < s("break1")
        self.terrain(c, t, cam)
        lake_level = LAKE_Y
        water(c, LAKE_X0, LAKE_X1, lake_level, LAKE_Y + 150, t)
        concrete(c, LAKE_X0 - 20, LAKE_Y - 30, 20, 180)
        if hook:
            u = self.climb_hook.at(t)
        elif rv and t < s("closer") - 0.1:
            u = 3.0
        else:
            u = self.climb_close.at(t)
        trip = self.trip.at(t) if rv else 0.0
        self.staircase(c, t, min(u, 3.0), "atl", ship_a=0.0 if rv and t < s("closer") - 0.1 else 1.0)
        self.staircase(c, t, 3.0, "pac")
        if rv and t < s("closer") - 0.1:                                 # the reveal: one ship through the whole canal
            if trip < 3.0:
                lv, sx, sy = self.levels(trip)
                for k in range(3):                                       # show its chamber rising
                    x0 = X0 + k * CW
                    water(c, x0 + 10, x0 + CW - 10, lv[k], -k * STEP + DEPTH, t)
                cargo_ship(c, sx, sy, 250, t)
            elif trip < 4.0:
                x = lerp(LAKE_X0 + 260, LAKE_X1 - 160, trip - 3.0)
                cargo_ship(c, x, LAKE_Y, 250, t)
            elif trip < 7.0:
                d = trip - 4.0
                k = int(clamp(math.floor(d), 0, 2))
                f = d - k
                x = PAC_X0 + CW * (k + 0.5) if f < 0.5 else lerp(PAC_X0 + CW * (k + 0.5), PAC_X0 + CW * (k + 1.5), (f - 0.5) / 0.5)
                lvl = LAKE_Y + k * STEP + STEP * e_io(clamp(f / 0.5))
                if f >= 0.5:
                    lvl = LAKE_Y + (k + 1) * STEP
                cargo_ship(c, x, min(lvl, 0.0), 250, t)
            else:
                cargo_ship(c, PAC_X0 + 3 * CW + 200 + (trip - 7.0) * 700, 0, 250, t)
            for i, (bx, by) in enumerate(((LAKE_X0 + 700, LAKE_Y), (LAKE_X0 + 1150, LAKE_Y))):
                cargo_ship(c, bx + math.sin(t * 0.3 + i) * 20, by, 180, t, a=0.9, face=-1 if i else 1)
        # rain on the hills (the lake is fed by rain)
        rk = (prog(t, T["rain"] - 0.4, T["rain"]) * (1 - prog(t, s("break1") - 0.6, s("break1")))) if hook else 0.0
        if rk > 0 or rv:
            rr_ = rk if hook else 0.45
            for (qx, qy, qs, sd) in ((150, -560, 1.4, 1), (560, -620, 1.3, 2), (1300, -600, 1.4, 3)):
                rain_cloud(c, qx, LAKE_Y + qy, qs, t, a=rr_, seed=sd)
            rain(c, -200, 1700, LAKE_Y - 560, LAKE_Y + 20, t, a=rr_, n=110)
        c.restore()
        self.ui["cam"] = cam
        self.ui["u"] = u

    def ui_canal(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam.at(tw))
        if tw < s("break1"):
            self.chip(540, 560, "climb", T["climb"] - 0.15, T["rain"] - 0.15, accent="#93C5FD", size=40)
            self.chip(540, 560, "rain", T["rain"] - 0.15, T["panama"] - 0.15, accent="#BFDBFE", size=40)
            self.chip(540, 560, "locks", T["panama"] - 0.15, s("break1") + 0.1, accent=HILITE, size=44)
            return
        if s("reveal") - 0.12 <= tw < s("stat") - 0.12:
            ax, ay = self.at(cam, X0 + CW * 1.5, -2 * STEP - 60)
            self.label(ax, ay, 300, 560, "up3", T["up"] - 0.1, T["across"] - 0.1, "#93C5FD", size=34)
            bx, by = self.at(cam, LAKE_X0 + 750, LAKE_Y - 60)
            self.label(bx, by, 560, 560, "acrossl", T["across"] - 0.1, T["down"] - 0.1, GOOD, size=34)
            dx, dy = self.at(cam, PAC_X0 + CW * 1.5, LAKE_Y + 60)
            self.label(dx, dy, 780, 560, "down3", T["down"] - 0.1, T["ocean"] - 0.1, "#FDBA74", size=34)
            ox, oy = self.at(cam, PAC_X0 + 3 * CW + 300, -20)
            self.label(ox, oy, 760, 560, "other", T["ocean"] - 0.1, s("stat") - 0.15, HILITE, size=34)

    # ------------------------------------------------------------------ set: map (break1)
    ROUTE = [(830, 500), (980, 555), (1100, 650), (1105, 800), (1010, 960), (900, 1120), (830, 1232), (760, 1236),
             (700, 1100), (660, 900), (640, 700), (690, 600), (760, 588)]

    def draw_map(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B2447", "#0E3A66", "#0B2447"])
        for k in range(16):                                              # latitude lines
            c.drawLine(0, 240 + k * 70, W, 240 + k * 70, P("#1E4F80", 0.35, stroke=2))
        land = lin_paint(0, 230, 0, 1230, ["#4C8A55", "#2F6B3F", "#24553A"])
        ca = skia.Path()                                                 # Mexico and Central America down to Panama
        for i, (x, y) in enumerate(((-20, 230), (700, 230), (690, 300), (640, 360), (600, 420), (650, 470),
                                    (700, 500), (760, 525), (805, 540), (795, 562), (740, 556), (690, 536),
                                    (620, 502), (540, 452), (450, 382), (330, 332), (200, 302), (-20, 300))):
            (ca.moveTo if i == 0 else ca.lineTo)(x, y)
        ca.close()
        c.drawPath(ca, land)
        for (ix, iy, iw, ih) in ((760, 320, 150, 26), (900, 352, 90, 22), (1010, 372, 40, 16)):   # Caribbean islands
            c.drawOval(R(ix, iy, iw, ih), land)
        sa = skia.Path()                                                 # South America
        for i, (x, y) in enumerate(((800, 548), (860, 540), (950, 575), (1050, 640), (1072, 700), (1060, 780),
                                    (1000, 850), (960, 920), (900, 1000), (860, 1080), (820, 1160), (792, 1215),
                                    (772, 1200), (760, 1120), (740, 1000), (720, 880), (700, 760), (690, 660),
                                    (720, 600), (770, 570))):
            (sa.moveTo if i == 0 else sa.lineTo)(x, y)
        sa.close()
        c.drawPath(sa, land)
        tex(c, sa, "sand", 0.6, 0.18)
        mk = prog(t, T["mts"] - 0.3, T["mts"] + 0.2)                     # mountains along the isthmus
        for i in range(8):
            mx = 640 + i * 20
            my = 478 + i * 9
            tri = skia.Path()
            tri.moveTo(mx - 13, my + 8)
            tri.lineTo(mx, my - 26 * mk)
            tri.lineTo(mx + 13, my + 8)
            tri.close()
            c.drawPath(tri, P("#A16207", mk))
            c.drawPath(tri, P("#FDE68A", 0.6 * mk, stroke=2))
        add_glow(c, 790, 550, 90, "#FDE68A", 0.35 * mk)
        rk = prog(t, T["around"] - 0.5, T["weeks"])                      # the long way round, drawn as it goes
        pts = self.ROUTE
        px, py = pts[0]
        ang = 0.0
        if rk > 0:
            total = sum(math.hypot(bx - ax, by - ay) for (ax, ay), (bx, by) in zip(pts, pts[1:]))
            want = total * rk
            path = skia.Path()
            path.moveTo(*pts[0])
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                d = math.hypot(bx - ax, by - ay)
                ang = math.degrees(math.atan2(by - ay, bx - ax))
                if want <= d:
                    px, py = ax + (bx - ax) * want / d, ay + (by - ay) * want / d
                    path.lineTo(px, py)
                    break
                path.lineTo(bx, by)
                want -= d
                px, py = bx, by
            c.drawPath(path, dash_paint("#FDE68A", 1.0, 7, t, 18, 12))
        c.save()
        c.translate(px, py)
        c.scale(0.24, 0.24)
        cargo_ship(c, 0, 0, 250, t, face=-1 if 90 < ang % 360 < 270 else 1)
        c.restore()

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(330, 760, "pac", T["atl"] - 0.2, s("fix1") - 0.15, accent="#93C5FD", size=36)
        self.chip(930, 280, "atl", T["atl"] - 0.2, s("fix1") - 0.15, accent="#93C5FD", size=36)
        self.label(740, 520, 380, 470, "split", T["mts"] - 0.1, T["around"] - 0.15, "#FDE68A", size=36)
        self.chip(360, 1000, "weeks", T["around"] - 0.1, s("fix1") - 0.15, accent=WARN, size=40)
        self.badge("alert", T["weeks"] + 0.05, s("fix1") - 0.2, x=880, y=330)
        self.red(T["weeks"] + 0.05, 1.3)

    # ------------------------------------------------------------------ set: dam (fix1)
    def draw_dam(self, c, t):
        T, s = self.T, self.tl.s
        cam = (60, -330, 0.82)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 60 * z)
        v2.stars(c, W, H, t, 0.4)
        self.view(c, cam)
        v2.ridge(c, -900, 1100, -260, 520, JUNGLE[0], JUNGLE[1], seed=6, step=80, rough=0.6, depth=700, peaks=6)
        dk = e_out(prog(t, T["dam"] - 0.2, T["dam"] + 0.6))              # the dam rises
        fk = e_io(prog(t, T["lake"] - 0.5, T["hills"] + 0.4))            # the lake fills behind it
        lvl = lerp(10, LAKE_Y, fk)
        ground = skia.Path()
        ground.moveTo(-900, 120)
        ground.lineTo(-330, 120)
        ground.lineTo(-300, 30)
        ground.lineTo(560, 30)
        ground.quadTo(700, 0, 760, -420)
        ground.lineTo(1100, -500)
        ground.lineTo(1100, 3000)
        ground.lineTo(-900, 3000)
        ground.close()
        water(c, -900, -320, 0, 130, t)                                  # the sea
        water(c, -260, 700 + 60 * fk, lvl, 30, t, a=1.0 if fk > 0.02 else 0.0)
        if fk < 0.6:                                                     # the river running down to the sea
            rv = skia.Path()
            rv.moveTo(560, 26)
            rv.lineTo(-300, 26)
            rv.lineTo(-330, 4)
            c.drawPath(rv, P("#60A5FA", 0.9 * (1 - fk / 0.6), stroke=14))
        c.drawPath(ground, lin_paint(0, -400, 0, 900, ["#4D6B3A", "#3D2A1C", "#21160E"]))
        tex(c, ground, "stone", 1.0, 0.22)
        jungle(c, 600, 1100, -380, t, 1.0, 0.95, seed=11)
        if dk > 0:                                                       # the dam wall
            dp = skia.Path()
            top = lerp(30, LAKE_Y - 30, dk)
            dp.moveTo(-470, 60)
            dp.lineTo(-330, top)
            dp.lineTo(-250, top)
            dp.lineTo(-110, 60)
            dp.close()
            c.drawPath(dp, lin_paint(0, top, 0, 60, ["#6E7752", "#556045", "#3A402C"]))
            c.drawRect(R(-330, top - 6, 80, 10), P("#D1D5DB"))
            c.drawPath(dp, P("#2F3424", 1, stroke=3))
        rk = prog(t, T["lake"] - 0.6, T["lake"])
        rain_cloud(c, 250, -760, 1.5, t, a=rk, seed=3)
        rain_cloud(c, 700, -820, 1.3, t, a=rk, seed=4)
        rain(c, -100, 900, -760, lvl, t, a=rk * 0.9, n=70)
        if fk > 0.9:                                                     # a ship crosses on the lake
            xk = prog(t, T["cross"] - 0.6, s("break2") - 0.1)
            cargo_ship(c, lerp(-150, 520, xk), LAKE_Y, 200, t)
        c.restore()
        self.ui["cam"] = cam
        self.ui["lvl"] = lvl

    def ui_dam(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (60, -330, 0.82))
        ax, ay = self.at(cam, -290, LAKE_Y * min(1.0, prog(tw, T["dam"] - 0.2, T["dam"] + 0.6)) - 10)
        self.label(ax, ay, 300, 380, "dam", T["dam"] - 0.1, T["lake"] - 0.1, "#E2E8F0", size=36)
        self.chip(540, 380, "lake", T["lake"] - 0.1, T["hills"] - 0.1, accent="#93C5FD", size=40)
        k = self.span(T["hills"] - 0.1, s("break2") - 0.15)
        if k > 0:                                                        # the height arrow: 26 m above the sea
            sx, sy0 = self.at(cam, -560, 0)
            _, sy1 = self.at(cam, -560, LAKE_Y)
            c.drawLine(sx, sy0, sx, sy1, P(HILITE, k, stroke=6))
            for yy, d in ((sy0, 1), (sy1, -1)):
                hp = skia.Path()
                hp.moveTo(sx, yy)
                hp.lineTo(sx - 16, yy + 24 * d)
                hp.lineTo(sx + 16, yy + 24 * d)
                hp.close()
                c.drawPath(hp, P(HILITE, k))
            v2.chip(c, sx + 40 + 150, (sy0 + sy1) / 2, self.L["high"], k, accent=HILITE, size=32)
        self.chip(540, 380, "cross", T["cross"] - 0.1, s("break2") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["cross"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: lock (break2, fix2)
    def draw_lock(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        if not fixed:                                                    # a ship tries to sail uphill
            cam = (0, -240, 0.9)
            cx, cy, z = cam
            gy = (0 - cy) * z + H / 2
            v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 40 * z)
            self.view(c, cam)
            v2.ridge(c, -900, 900, -200, 500, JUNGLE[0], JUNGLE[1], seed=9, step=80, rough=0.6, depth=700, peaks=5)
            hill = skia.Path()
            hill.moveTo(40, 40)
            hill.quadTo(260, 20, 420, -300)
            hill.lineTo(900, -330)
            hill.lineTo(900, 3000)
            hill.lineTo(40, 3000)
            hill.close()
            water(c, -900, 120, 0, 140, t)
            c.drawRect(R(-900, 140, 1000, 2900), lin_paint(0, 140, 0, 900, ["#3D2A1C", "#21160E"]))
            c.drawPath(hill, lin_paint(0, -330, 0, 600, ["#4D6B3A", "#3D2A1C", "#21160E"]))
            water(c, 420, 900, -330, -200, t)
            jungle(c, 430, 900, -330, t, 0.9, 0.95, seed=5)
            go = prog(t, s("break2"), T["uphill"] - 0.1)
            back = prog(t, T["uphill"] - 0.1, T["uphill"] + 0.6)
            sx = lerp(-380, -40, e_in(go)) - 160 * e_out(back)
            tilt = -16 * e_out(prog(t, T["uphill"] - 0.35, T["uphill"] - 0.1)) * (1 - back)
            cargo_ship(c, sx, 0, 300, t, tilt=tilt)
            if back > 0:
                splash(c, sx + 150, 0, t, T["uphill"] - 0.1, dur=0.9, n=20, speed=520)
            c.restore()
            self.ui["cam"] = cam
            return
        cam = (0, 110, 0.98)                                             # one chamber in section
        cx, cy, z = cam
        vrect(c, 0, 0, W, H, ["#101736", "#1A2350", "#0B1030"])
        self.view(c, cam)
        LX0, LX1 = -440, 300                                             # chamber walls
        FL = 260                                                         # chamber floor
        lo, hi = 0.0, -260.0
        rk = e_io(prog(t, T["rise"], T["toy"] + 0.2))
        lvl = lerp(lo, hi, rk)
        c.drawRect(R(-1200, FL, 2400, 900), lin_paint(0, FL, 0, FL + 900, ["#3D2A1C", "#21160E"]))
        water(c, -1200, LX0 - 60, lo, FL, t)                             # the lower side
        water(c, LX1 + 60, 1200, hi, FL, t)                              # the lake side, high
        water(c, LX0, LX1, lvl, FL, t)
        concrete(c, LX1, hi - 60, 60, FL - hi + 60)                      # upper gate wall
        # the culvert: from the lake side down through the wall and under the floor
        cul = [(560, hi + 120), (560, FL + 90), (-380, FL + 90)]
        ck = prog(t, T["valve"], T["valve"] + 0.4) * (1 - prog(t, T["toy"] + 0.2, T["toy"] + 0.8))
        pth = skia.Path()
        pth.moveTo(*cul[0])
        for p_ in cul[1:]:
            pth.lineTo(*p_)
        c.drawPath(pth, P("#0B1324", 1, stroke=64))
        c.drawPath(pth, P("#1E3A5F", 1, stroke=50))
        if ck > 0:
            c.drawPath(pth, dash_paint("#93C5FD", ck, 14, t * 3, 24, 18))
            for i in range(6):                                           # holes in the floor, water boiling up
                hx = -340 + i * 110
                c.drawRect(R(hx - 14, FL - 4, 28, 60), P("#1E3A5F", 1))
                bubbles(c, hx, FL - 6, t, T["valve"], T["toy"] + 0.4, rate=10, life=1.2, spread=30,
                        rise=FL - lvl - 10, size=(4, 10), seed=i, a=0.8 * ck)
        else:
            for i in range(6):
                hx = -340 + i * 110
                c.drawRect(R(hx - 14, FL - 4, 28, 60), P("#1E3A5F", 1))
        vk = prog(t, T["valve"] - 0.2, T["valve"] + 0.2)                 # the valve wheel in the tunnel
        c.save()
        c.translate(560, hi + 230)
        c.rotate(vk * 270)
        c.drawCircle(0, 0, 34, P("#FBBF24", 1, stroke=7))
        c.drawLine(-34, 0, 34, 0, P("#FBBF24", 1, stroke=6))
        c.drawLine(0, -34, 0, 34, P("#FBBF24", 1, stroke=6))
        c.restore()
        concrete(c, LX0 - 60, hi - 60, 60, FL - hi + 60)                 # lower gate wall
        gk = prog(t, T["close"] - 0.3, T["close"] + 0.1)
        gate_side(c, LX0 - 30, hi - 60, FL, gk)
        gate_side(c, LX1 + 30, hi - 60, FL, 1.0)
        enter = e_io(prog(t, s("fix2"), T["box"]))
        cargo_ship(c, lerp(-900, -70, enter), lvl, 330, t)
        dk = prog(t, T["toy"] - 0.25, T["toy"] + 0.1)
        duck(c, 200, lvl, 0.9, a=dk, t=t)
        c.restore()
        self.ui["cam"] = cam
        self.ui["lvl"] = lvl
        self.ui["pk"] = prog(t, T["pumps"] - 0.2, T["pumps"] + 0.15)

    def ui_lock(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 470, "uphill", T["uphill"] - 0.4, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["uphill"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["uphill"] + 0.05, 1.3)
            return
        cam = self.ui.get("cam", (0, 110, 0.98))
        self.chip(540, 380, "steps", T["steps"] - 0.1, T["box"] - 0.1, accent="#93C5FD", size=40)
        self.chip(540, 380, "box", T["box"] - 0.1, T["close"] - 0.1, accent="#E2E8F0", size=40)
        self.chip(540, 380, "close", T["close"] - 0.1, T["pours"] - 0.1, accent=HILITE, size=40)
        tx, ty = self.at(cam, 560, -40)
        self.label(tx, ty, 700, 480, "tunnel", T["pours"] - 0.1, T["floor"] - 0.1, "#93C5FD", size=34)
        fx_, fy_ = self.at(cam, -120, 256)
        self.label(fx_, fy_, 540, 480, "floor", T["floor"] - 0.1, T["pumps"] - 0.1, "#93C5FD", size=34)
        pk = self.span(T["pumps"] - 0.2, T["lift"])
        if pk > 0:                                                       # a pump, crossed out
            pump(c, 230, 520, 0.9, a=pk)
            c.drawCircle(230, 520, 100, P(WARN, pk, stroke=10))
            c.drawLine(160, 590, 300, 450, P(WARN, pk, stroke=10))
            v2.chip(c, 520, 520, self.L["nopump"], pk, accent=WARN, size=40)
        self.chip(540, 470, "toy", T["toy"] - 0.15, s("break3") - 0.15, accent=HILITE, size=40)
        self.badge("check", T["toy"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: gate (break3, fix3)
    def draw_gate(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0F172A", "#1E1B4B", "#0F172A"])
        for k in range(16):
            c.drawLine(k * 80, 0, k * 80, H, P("#312E81", 0.45, stroke=2))
        for k in range(26):
            c.drawLine(0, k * 80, W, k * 80, P("#312E81", 0.45, stroke=2))
        fixed = t >= s("fix3") - 0.12
        xr = prog(t, T["xr"], T["xr"] + 0.5) if fixed else 0.0
        top_k = prog(t, T["shut"] - 0.6, T["shut"]) if fixed else 0.0
        gx, gy, gw, gh = 120, 520, 400, 640                              # one gate leaf, front view
        if top_k < 1:
            a = 1 - top_k
            if fixed:                                                    # water up to its middle
                c.drawRect(R(40, gy + gh * 0.45, 1000, gh * 0.55 + 60), lin_paint(0, gy + gh * 0.45, 0, gy + gh + 60,
                                                                                  [WATER, WATER_D], a=0.8 * xr * a))
            c.drawRect(R(gx, gy, gw, gh), lin_paint(gx, 0, gx + gw, 0, ["#4B5563", "#6B7280", "#374151"], a=a * (1 - 0.65 * xr)))
            for i in range(8):
                for j in range(5):
                    c.drawCircle(gx + 30 + j * 85, gy + 30 + i * 82, 6, P("#9CA3AF", 0.7 * a * (1 - xr)))
            c.drawRect(R(gx, gy, gw, gh), P("#E5E7EB", a, stroke=4))
            if xr > 0:                                                   # x-ray: hollow, the bottom cells full of air
                for i in range(6):
                    for j in range(3):
                        cell = R(gx + 20 + j * 125, gy + 20 + i * 102, 110, 88)
                        air = i >= 3
                        c.drawRect(cell, P("#BFDBFE" if air else "#334155", (0.75 if air else 0.4) * xr * a))
                        c.drawRect(cell, P("#E2E8F0", 0.8 * xr * a, stroke=2))
                fk = prog(t, T["float"] - 0.3, T["float"] + 0.2)
                for j in range(3):                                       # buoyancy arrows
                    ax = gx + 75 + j * 125
                    yy = gy + gh + 60 - 40 * math.sin(t * 3 + j) * fk
                    c.drawLine(ax, yy + 80, ax, yy, P(GOOD, fk * a, stroke=10))
                    hp = skia.Path()
                    hp.moveTo(ax, yy - 26)
                    hp.lineTo(ax - 20, yy + 4)
                    hp.lineTo(ax + 20, yy + 4)
                    hp.close()
                    c.drawPath(hp, P(GOOD, fk * a))
                mk = prog(t, T["motors"] - 0.3, T["motors"] + 0.2)       # the small motor on top, with its arm
                c.drawRRect(rr(gx + gw - 150, gy - 110, 130, 90, 14), P("#F59E0B", mk * a))
                c.drawCircle(gx + gw - 85, gy - 65, 26, P("#78350F", mk * a))
                c.drawLine(gx + gw - 85, gy - 65, gx + gw - 85 + math.cos(t * 6) * 22, gy - 65 + math.sin(t * 6) * 22,
                           P("#FDE68A", mk * a, stroke=6))
        if not fixed:                                                    # = 400 cars
            ck = prog(t, T["stack"], T["cars"] + 0.2)
            n = int(400 * ck)
            for i in range(n):
                r_, q = divmod(i, 20)
                car_icon(c, 600 + q * 22, 560 + r_ * 30, 0.72, BOX_COLS[(i * 7) % len(BOX_COLS)])
        if top_k > 0:                                                    # top view: two leaves swing shut into a V
            k = top_k
            c.drawRect(R(0, 300, 200, 1000), lin_paint(0, 0, 200, 0, [shade(CONC, -0.1), CONC], a=k))
            c.drawRect(R(880, 300, 200, 1000), lin_paint(880, 0, W, 0, [CONC, shade(CONC, -0.1)], a=k))
            c.drawRect(R(200, 300, 680, 1000), lin_paint(0, 300, 0, 1300, [WATER, "#1B5C99", WATER_D], a=0.9 * k))
            sw = e_io(prog(t, T["shut"], T["shut"] + 0.9))
            for sd in (-1, 1):
                hx, hy = 540 + sd * 340, 700
                a0 = 90.0
                a1 = math.degrees(math.atan2(-110, -sd * 340))
                if sd < 0 and a1 < 0:
                    a1 = a1
                if sd > 0 and a1 < 0:
                    a1 += 360.0
                ang = math.radians(lerp(a0, a1, sw))
                L_ = math.hypot(340, 110)
                ex, ey = hx + math.cos(ang) * L_, hy + math.sin(ang) * L_
                c.drawLine(hx, hy, ex, ey, P("#64748B", k, stroke=30))
                c.drawLine(hx, hy, ex, ey, P("#CBD5E1", 0.6 * k, stroke=8))
                c.drawCircle(hx, hy, 20, P("#F59E0B", k))
            if sw > 0.95:
                add_glow(c, 540, 590, 90, "#FDE68A", 0.8 * prog(t, T["shut"] + 0.85, T["shut"] + 1.1) * k)

    def ui_gate(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(320, 470, "heavy", T["gates"] - 0.1, s("fix3") - 0.15, accent="#E2E8F0", size=34)
            self.chip(760, 470, "cars", T["hundred"] - 0.1, s("fix3") - 0.15, accent=WARN, size=40)
            self.chip(320, 1205, "tonnes", T["cars"] - 0.1, s("fix3") - 0.15, accent=WARN, size=32)
            self.badge("alert", T["cars"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["cars"] + 0.05, 1.3)
            return
        self.chip(320, 470, "hollow", T["xr"], T["float"] - 0.1, accent="#BFDBFE", size=40)
        self.chip(320, 470, "floats", T["float"] - 0.1, T["motors"] - 0.1, accent=GOOD, size=40)
        self.chip(540, 380, "motor", T["motors"] - 0.1, T["shut"] - 0.1, accent="#F59E0B", size=32)
        self.chip(540, 1150, "swing", T["shut"] - 0.1, s("break4") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["swing"] + 0.2, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: mules (break4, fix4, cta)
    def draw_mules(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1F2937", "#111827"])
        fixed = t >= s("fix4") - 0.12
        cw = 700.0                                                       # chamber width on screen
        x0 = 540 - cw / 2
        c.drawRect(R(0, 0, x0, H), lin_paint(0, 0, x0, 0, [shade(CONC, -0.1), CONC]))
        c.drawRect(R(x0 + cw, 0, W - x0 - cw, H), lin_paint(x0 + cw, 0, W, 0, [CONC, shade(CONC, -0.1)]))
        for sx in (60, W - 60):                                          # mule tracks along the walls
            c.drawLine(sx - 18, 0, sx - 18, H, P("#4B5563", 1, stroke=6))
            c.drawLine(sx + 18, 0, sx + 18, H, P("#4B5563", 1, stroke=6))
            for k in range(30):
                yy = (k * 70 + t * 40) % (H + 70) - 35
                c.drawLine(sx - 26, yy, sx + 26, yy, P("#374151", 1, stroke=6))
        c.drawRect(R(x0, 0, cw, H), lin_paint(0, 0, 0, H, [WATER, "#1B5C99", WATER_D], a=0.95))
        for k in range(12):                                              # ripples
            yy = (k * 170 + t * 60) % H
            c.drawLine(x0 + 30, yy, x0 + 120, yy, P("#93C5FD", 0.25, stroke=3))
        sw_ = cw - 44                                                    # the ship: 0.6 m each side, to scale-ish
        if not fixed:
            drift = math.sin(prog(t, T["barely"], T["scrape"]) * math.pi / 2) * 22
            sx = 540 + drift
        else:
            ck = prog(t, T["cables"], T["center"])
            sx = lerp(540 + 22, 540, e_io(ck))
        by = lerp(1500, 300, prog(t, s("break4"), s("cta")))
        ship_top(c, sx, by, sw_, 1700)
        if not fixed and t > T["scrape"]:                                # scraping the wall
            sp = prog(t, T["scrape"], T["scrape"] + 1.2)
            sparks_shower(c, x0 + cw - 4, by + 420, t, T["scrape"], dur=0.9, n=30, speed=600)
            c.drawLine(x0 + cw - 2, by + 300, x0 + cw - 2, by + 300 + 500 * sp, P("#FDE68A", 0.8 * (1 - sp), stroke=6))
        if fixed:
            mk = prog(t, T["loco"] - 0.3, T["loco"] + 0.3)
            for sd, mx in ((-1, 60), (1, W - 60)):
                for j, oy in enumerate((260, 520, 1220, 1480)):
                    my = by + oy - 400
                    if -60 < my < H + 60:
                        mule(c, mx, my, 1.0, a=mk)
                        ck = prog(t, T["cables"] - 0.3, T["cables"] + 0.2)
                        if ck > 0:
                            tx = sx + sd * sw_ / 2
                            ty = by + oy - 380 + (60 if j % 2 else -60)
                            c.drawLine(mx - sd * 26, my, lerp(mx - sd * 26, tx, ck), lerp(my, ty, ck),
                                       P("#E5E7EB", 0.9 * mk, stroke=4))
        self.ui["sx"] = sx
        self.ui["by"] = by
        self.ui["x0"] = x0
        self.ui["cw"] = cw

    def ui_mules(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, cw = self.ui.get("x0", 190), self.ui.get("cw", 700)
        if tw < s("fix4") - 0.12:
            self.chip(540, 380, "tight", T["big"] - 0.1, T["half"] - 0.1, accent="#FDE68A", size=40)
            k = self.span(T["half"] - 0.1, s("fix4") - 0.15)
            if k > 0:
                for gx in (x0 + 11, x0 + cw - 11):
                    c.drawLine(gx - 12, 760, gx + 12, 760, P(HILITE, k, stroke=5))
                v2.chip(c, 540, 380, self.L["gap"], k, accent=HILITE, size=40)
            self.chip(820, 1120, "scrape", T["scrape"], s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["side"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["scrape"], 1.3)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 380, "mules", T["loco"] - 0.1, T["cables"] - 0.1, accent=WARN, size=36)
            self.chip(540, 380, "cables", T["cables"] - 0.1, T["center"] - 0.1, accent="#E2E8F0", size=40)
            self.chip(540, 380, "center", T["center"] - 0.1, s("cta") - 0.15, accent=GOOD, size=40)
            self.badge("check", T["center"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: swim (tag)
    def draw_swim(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, 1240, ["#1E2156", "#55306E", "#C4566A"])
        v2.stars(c, W, H, t, 0.4)
        concrete(c, -10, 980, 130, 300)
        concrete(c, 960, 980, 130, 300)
        water(c, 120, 960, 1010, 1260, t)
        vrect(c, 0, 1240, W, H - 1240, ["#2A3442", "#1C232D", "#0E1218"])
        wk = prog(t, T["weighed"] - 0.3, T["weighed"] + 0.1)
        if wk < 1:                                                       # the swimmer, crawling along the lock
            a = 1 - wk
            sx = 260 + (t - self.tl.s("tag")) * 120
            c.drawCircle(sx, 1004, 34, P("#E8B48A", a))
            c.drawRect(R(sx - 36, 976, 72, 18), P("#1F2937", a))
            arm = math.sin(t * 7)
            c.drawLine(sx + 14, 1016, sx + 80 + arm * 30, 960 - abs(arm) * 50, P("#E8B48A", a, stroke=16))
            splash(c, sx + 90, 1010, t, T["swam"], dur=0.6, n=12, speed=320)
        if wk > 0:                                                       # weighed like a ship
            c.drawRRect(rr(330, 1150, 420, 60, 14), P("#9CA3AF", wk))
            c.drawRect(R(700, 760, 24, 400), P("#6B7280", wk))
            c.drawCircle(712, 720, 90, P("#F8FAFC", wk))
            c.drawCircle(712, 720, 90, P("#475569", wk, stroke=8))
            for k in range(9):
                an = math.radians(-120 + k * 30)
                c.drawLine(712 + math.sin(an) * 70, 720 - math.cos(an) * 70, 712 + math.sin(an) * 82,
                           720 - math.cos(an) * 82, P("#334155", wk, stroke=4))
            nd = lerp(-120, 40, e_out(prog(t, T["weighed"], T["weighed"] + 0.6)))
            c.drawLine(712, 720, 712 + math.sin(math.radians(nd)) * 66, 720 - math.cos(math.radians(nd)) * 66,
                       P(WARN, wk, stroke=7))
            person(c, 480, 1150, 330, "#38BDF8", t, pose="stand", face=1, hat="none", wet=1.0, a=wk)
        ck = prog(t, T["cents"] - 0.2, T["cents"] + 0.2)
        if ck > 0:                                                       # the toll ticket
            c.save()
            c.translate(330, 560)
            c.rotate(-6)
            c.scale(0.8 + 0.2 * e_back(ck), 0.8 + 0.2 * e_back(ck))
            c.drawRRect(rr(-210, -90, 420, 180, 18), P("#FEF3C7", ck))
            c.drawRRect(rr(-210, -90, 420, 180, 18), P("#92400E", ck, stroke=5))
            c.restore()
        ak = prog(t, T["airport"] - 0.2, T["airport"] + 0.2)
        if ak > 0:
            if not self.rtl:                                             # a small bottle of airport water
                c.save()
                c.translate(900, 560)
                c.scale(0.6 + 0.4 * e_back(ak), 0.6 + 0.4 * e_back(ak))
                c.drawRRect(rr(-55, -120, 110, 260, 36), P("#BFDBFE", 0.9 * ak))
                c.drawRRect(rr(-55, -40, 110, 80, 6), P("#1D4ED8", ak))
                c.drawRect(R(-26, -160, 52, 42), P("#3B82F6", ak))
                c.restore()
            else:                                                        # the parking guy: "come, come"
                person(c, 900, 1240, 260, "#F97316", t, pose="cheer", face=-1, hat="cap", band=True, a=ak)

    def ui_swim(self, c, t, tw):
        T = self.T
        self.chip(540, 380, "swam", T["swam"] - 0.2, T["weighed"] - 0.1, accent="#93C5FD", size=40)
        self.chip(540, 380, "weigh", T["weighed"] - 0.1, T["airport"] - 0.1, accent=HILITE, size=40)
        k = self.span(T["weighed"] + 0.3, self.duration + 1)
        if k > 0:
            v2.chip(c, 712, 860, self.L["lbs"], k, accent=WARN, size=36)
        ck = self.span(T["cents"] - 0.1, self.duration + 1)
        if ck > 0:
            c.save()
            c.translate(330, 560)
            c.rotate(-6)
            word(c, self.L["toll"], 0, 18, 46, "#92400E", a=ck)
            c.restore()
        ak = self.span(T["airport"] - 0.1, self.duration + 1)
        if ak > 0:
            if not self.rtl:
                v2.chip(c, 900, 790, self.L["water7"], ak, accent=WARN, size=48)
                v2.chip(c, 540, 380, self.L["airport"], ak, accent=WARN, size=40)
            else:
                v2.chip(c, 700, 880, self.L["water7"], ak, accent=HILITE, size=44)
                v2.chip(c, 540, 380, self.L["airport"], ak, accent=HILITE, size=40)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(1.6, 61), -16), (0.3, sfx.clank(180.0, 0.6, 62), -10), (T["climb"], sfx.hiss(1.2, 63), -14),
              (T["stair"], sfx.clank(200.0, 0.5, 64), -12), (T["rain"], sfx.hiss(2.0, 65), -16),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 66), -9), (T["panama"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["mts"], sfx.thud(0.4), -10),
               (T["around"], sfx.whoosh(1.2, False, 68), -14), (T["weeks"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["dam"], sfx.thud(0.6), -6),
               (T["lake"], sfx.hiss(2.0, 70), -14), (T["cross"] + 0.1, sfx.ding(), -8), (T["cross"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["uphill"] - 0.1, sfx.thud(0.5), -6),
               (T["uphill"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["close"], sfx.clank(160.0, 0.8, 73), -6),
               (T["valve"], sfx.creak(0.8), -10), (T["pours"], sfx.hiss(2.4, 74), -12), (T["pumps"], sfx.pop(75), -8),
               (T["toy"], sfx.tap(76), -6), (T["toy"] + 0.2, sfx.ding(), -8), (T["toy"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 77), -4), (T["stack"], sfx.click(78), -10),
               (T["cars"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["xr"], sfx.whoosh(0.5, False, 79), -10), (T["float"], sfx.hiss(0.8, 80), -14),
               (T["motors"], sfx.whirr(1.2), -12), (T["shut"] + 0.6, sfx.clank(150.0, 0.9, 81), -6),
               (T["swing"] + 0.3, sfx.ding(), -8), (T["swing"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 82), -4), (T["scrape"], sfx.sizzle(0.9, 83), -8),
               (T["side"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["loco"], sfx.hum(1.6, 110.0), -14), (T["cables"], sfx.lock_click(84), -8),
               (T["center"] + 0.1, sfx.ding(), -8), (T["center"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(85), 0), (T["follow"] - 0.15, sfx.pop(86), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 87), -6), (T["up"], sfx.hiss(1.4, 88), -14),
               (T["across"], sfx.whoosh(1.0, True, 89), -12), (T["ocean"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 90), -6), (T["s1"], sfx.pop(91), -3), (T["s2"], sfx.pop(92), -3),
               (T["s3"], sfx.pop(93), -3)]
        ev += [(T["cong2"], sfx.pop(94), -2), (T["cong2"], sfx.sparkle(1.0, 14, 95), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 96), -6), (T["swam"], sfx.hiss(0.6, 97), -14),
               (T["weighed"], sfx.thunk(98), -8), (T["cents"], sfx.ding(), -8), (T["airport"], sfx.pop(99), -6)]
        return ev


NAME = "panama"
EPISODE = Panama
