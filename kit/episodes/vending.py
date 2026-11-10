"""Episode 17 - A vending machine.  v2 look: three sets.

front   the machine from the front in a hallway: floor at y = 0, the body x -190..190, y -640..0
side    one shelf cut open from the side: the shelf top at y = 0, its front edge at x = -260 (the glass at x = -420),
        the motor at the back (x = 300), the bin floor at y = 350
check   a board that shows what the coin slot and the bill reader do (drawn straight on the screen)
"""
from v2_base import *  # noqa: F401,F403

BODY, BODY_D = "#1D4ED8", "#172554"
COLS = (-140, -80, -20, 40)                              # slot columns 1..4 (front view)
ROWS = (-470, -370, -270, -170)                          # shelf lines A..D (front view)
BAGS = ("#F59E0B", "#EF4444", "#22C55E", "#A78BFA", "#38BDF8", "#F472B6", "#FACC15", "#FB923C")
EDGE, PITCH, GLASS_X, BIN_Y, CR, BS, ROW2 = -190, 104, -360, 420, 46, 1.5, 215   # side view: edge, pitch, glass, bin floor, coil radius, bag scale
HB = 300                                                 # how tall people are next to the machine


def bag(c, x, y, col, s=1.0, rot=0.0, face=False, a=1.0, dust=0.0):
    """A snack bag standing on (x, y)."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    c.drawRRect(rr(-20, -58, 40, 58, 6), lin_paint(-20, 0, 20, 0, [(shade(col, 0.25), a), (col, a), (shade(col, -0.3), a)]))
    for yy in (-56, -5):
        c.drawLine(-18, yy, 18, yy, P(shade(col, -0.45), a, stroke=3))
    c.drawOval(R(-13, -42, 26, 22), P("#FFFFFF", 0.85 * a))
    c.drawOval(R(-8, -37, 16, 12), P(col, a))
    if dust > 0:
        c.drawRRect(rr(-20, -58, 40, 58, 6), P("#9CA3AF", 0.55 * dust))
    if face:
        for ex in (-7, 7):
            c.drawCircle(ex, -34, 3.2, P("#111827", a))
        c.drawArc(R(-8, -30, 16, 12), 0, 180, False, P("#111827", a, stroke=2.5))
        c.drawRRect(rr(-3, -22, 6, 9, 3), P("#F43F5E", a))
    c.restore()


def coil_end(c, x, y, r=22, a=1.0):
    c.drawCircle(x, y, r, P("#CBD5E1", 0.9 * a, stroke=3))


def machine(c, t, glass=1.0, body=1.0, lit=0.0, bolts=0.0, beacon=0.0, tilt=0.0, paid=False, stock=None, flap=0.0, dusty=False, stuck=0):
    """The whole machine, front view, standing on y = 0. stock: None (full) or a set of (row, col) that are empty."""
    c.save()
    c.rotate(tilt, -190 if tilt < 0 else 190, 0)
    if body > 0:
        if lit > 0:
            add_glow(c, 0, -330, 520, "#60A5FA", 0.35 * lit)
        box(c, -190, -640, 380, 640, mix(BODY, "#2563EB", lit), r=18, a=body)
        c.drawRRect(rr(-190, -640, 380, 640, 18), P("#FFFFFF", 0.25 * body, stroke=3))
        c.drawRRect(rr(-178, -628, 356, 34, 10), P(mix("#0B1220", "#FDE68A", lit), body))
        if lit > 0:
            for i in range(7):
                c.drawRRect(rr(-160 + i * 48, -620, 30, 18, 5), P(BAGS[i % len(BAGS)], lit))
        c.drawRRect(rr(-172, -584, 256, 444, 10), P("#0B1220", body))                 # the window
        c.drawRRect(rr(-172, -584, 256, 444, 10), P(mix("#1B2238", "#DBEAFE", 0.25 * lit), 0.9 * body))
        # the panel on the right
        c.drawRRect(rr(98, -584, 78, 444, 10), P(BODY_D, body))
        c.drawRRect(rr(106, -572, 62, 34, 6), P("#052E16" if not paid else "#14532D", body))
        if paid:
            c.drawRRect(rr(112, -562, 50, 14, 4), P(GOOD, body))
        for i in range(12):
            c.drawRRect(rr(110 + (i % 3) * 20, -524 + (i // 3) * 20, 14, 14, 3), P("#CBD5E1", body))
        c.drawRRect(rr(128, -428, 8, 34, 4), P("#0B1220", body))                      # coin slot
        c.drawRRect(rr(124, -432, 16, 42, 6), P("#E5E9F2", body, stroke=3))
        c.drawRRect(rr(112, -366, 50, 10, 4), P("#0B1220", body))                     # bill slot
        c.drawRRect(rr(112, -352, 50, 5, 2), P(GOOD, body))
        c.drawRRect(rr(116, -270, 42, 34, 8), P("#0B1220", body))                     # coin return
        # the bin
        c.drawRRect(rr(-166, -128, 250, 86, 12), P("#0B1220", body))
        c.drawRRect(rr(-166, -128, 250, 86, 12), P("#94A3B8", body, stroke=3))
        if flap > 0:
            c.drawRRect(rr(-160, -124, 238, 30 + 40 * flap, 8), lin_paint(0, -124, 0, -50, [("#94A3B8", flap), ("#475569", flap)]))
        for fx_ in (-160, 160):
            c.drawRRect(rr(fx_ - 22, -8, 44, 12, 3), P("#0B1220", body))
            if bolts > 0:
                bk = clamp(bolts * 2 - (0 if fx_ < 0 else 1))
                c.drawRect(R(fx_ - 4, -30 + 22 * bk, 8, 30), P("#E5E9F2", clamp(bk * 3)))
                c.drawRRect(rr(fx_ - 10, -34 + 22 * bk, 20, 8, 3), P("#E5E9F2", clamp(bk * 3)))
    # shelves and what is on them
    for r_, ry in enumerate(ROWS):
        c.drawRect(R(-166, ry, 244, 5), P("#64748B", max(body, 0.0)))
        for k, cx_ in enumerate(COLS):
            if stock is not None and (r_, k) in stock:
                continue
            if body > 0:
                coil_end(c, cx_, ry - 28, 24, body)
            col = BAGS[(r_ * 4 + k) % len(BAGS)]
            is_dusty = dusty and (r_, k) == (3, 0)
            if (r_, k) == (1, 3) and stuck:                                           # slot B4
                for j in range(stuck):
                    c.save()
                    c.translate(cx_ - 8 + j * 14, ry - 10 + j * 6)
                    bag(c, 0, 30, col, 0.86, 24 + 10 * math.sin(t * 3 + j) - j * 40, face=(j == 0))
                    c.restore()
                continue
            bag(c, cx_, ry - 2, col if not is_dusty else "#A3A3A3", 0.86, dust=1.0 if is_dusty else 0.0)
            if is_dusty:                                                             # a cobweb for the one nobody buys
                for an in (200, 235, 270):
                    c.drawLine(cx_ + 22, ry - 58, cx_ + 22 + math.cos(math.radians(an)) * 30, ry - 58 - math.sin(math.radians(an)) * 30,
                               P("#E5E9F2", 0.7, stroke=1.5))
                c.drawArc(R(cx_ + 2, ry - 78, 40, 40), 90, 90, False, P("#E5E9F2", 0.7, stroke=1.5))
    if glass > 0 and body > 0:
        c.save()
        c.clipRRect(rr(-172, -584, 256, 444, 10))
        gy = -584 - 460 * (1 - glass)
        c.drawRect(R(-172, gy, 256, 444), P("#BAE6FD", 0.13))
        c.drawLine(-150, gy + 30, -60, gy + 430, P("#FFFFFF", 0.10, stroke=26))
        c.drawLine(-90, gy + 10, 0, gy + 410, P("#FFFFFF", 0.07, stroke=12))
        c.restore()
    if beacon > 0:
        on = math.sin(t * 18) > 0
        c.drawRRect(rr(-22, -664, 44, 26, 8), P("#7F1D1D"))
        c.drawCircle(0, -668, 16, P("#FF4D4F" if on else "#991B1B"))
        add_glow(c, 0, -668, 260, "#FF4D4F", (0.7 if on else 0.25) * beacon)
    c.restore()


def coin(c, x, y, r=28, rot=0.0, fake=False, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if fake:                                                                         # a shirt button
        c.drawCircle(0, 0, r, P("#94A3B8", a))
        c.drawCircle(0, 0, r * 0.72, P("#64748B", a, stroke=3))
        for dx, dy in ((-6, -6), (6, -6), (-6, 6), (6, 6)):
            c.drawCircle(dx, dy, 3.2, P("#1B2238", a))
    else:
        c.drawCircle(0, 0, r, rad_paint(-r * 0.3, -r * 0.3, r * 1.5, [("#FEF3C7", a), ("#FACC15", a), ("#B45309", a)]))
        c.drawCircle(0, 0, r * 0.74, P("#B45309", 0.8 * a, stroke=3))
        c.drawRect(R(-3, -r * 0.45, 6, r * 0.9), P("#B45309", 0.8 * a))
    c.restore()


def bill(c, x, y, w=240, h=110, wrinkled=False, a=1.0):
    c.save()
    c.translate(x, y)
    if wrinkled:
        p = skia.Path()
        rng = random.Random(5)
        pts = []
        for i in range(9):
            pts.append((-w / 2 + w * i / 8, -h / 2 + rng.uniform(-12, 12)))
        for i in range(9):
            pts.append((w / 2 - w * i / 8, h / 2 + rng.uniform(-12, 12)))
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, P("#4ADE80", a))
        for i in range(5):
            x0 = -w / 2 + rng.uniform(20, w - 20)
            c.drawLine(x0, -h / 2 + 8, x0 + rng.uniform(-40, 40), h / 2 - 8, P("#166534", 0.6 * a, stroke=3))
    else:
        c.drawRRect(rr(-w / 2, -h / 2, w, h, 8), P("#4ADE80", a))
        c.drawRRect(rr(-w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 5), P("#166534", 0.7 * a, stroke=3))
    c.drawCircle(0, 0, h * 0.26, P("#166534", 0.8 * a))
    c.restore()


def hum_snd(d=1.5, f=110.0):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2 * tt) + 0.3 * np.sin(2 * np.pi * f * 3.02 * tt)
    return sfx._norm(x * sfx._ar(n, 0.2, 0.5) * (0.8 + 0.2 * np.sin(2 * np.pi * 7 * tt)), 0.55)


def clink(seed=0):
    n = int(0.28 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, d in ((3100 + seed * 90, 22), (4700 + seed * 60, 30), (6900, 40)))
    return sfx._norm(x, 0.7)


def crinkle(d=0.4, seed=0):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed + 50).standard_normal(n), 2500, 9000)
    env = (sfx._rng(seed + 51).random(n) > 0.9993).astype(float)
    env = np.convolve(env, np.exp(-np.arange(900) / 180), mode="same")
    return sfx._norm(x * env * sfx._ar(n, 0.02, 0.1), 0.6)


def motor_snd(d=1.0):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sign(np.sin(2 * np.pi * 86 * tt)) * 0.4 + sfx._bp(sfx._rng(7).standard_normal(n), 400, 2400) * 0.4
    return sfx._norm(sfx._bp(x, 70, 3000) * sfx._ar(n, 0.05, 0.12), 0.5)


# ====================================================================================== the episode
class Vending(EpisodeV2):
    BUILD_NO = 17
    FIRST_SET = "front"
    CLEAR = "#0B1024"
    TITLE = {"en": "VENDING MACHINE", "ar_sa": "مكينة بيع"}
    EMPH = {"en": ["CONGRATS", "MACHINE", "SNACKS", "JAR", "GLASS", "COIN", "METAL", "BILL", "WRINKLES", "PAID", "LOCKED", "CHIPS", "SPIRAL", "MOTOR",
                   "EDGE", "STUCK", "MOCKING", "BEAMS", "AGAIN", "MONEY", "ROCKS", "FREE", "TON", "BOLT", "FLAP", "ALARM", "FOLLOW", "METRO", "GLOWING",
                   "HUM", "NOBODY", "ZERO", "YOURSELF", "TUESDAY", "TWO"],
            "ar_sa": ["مبروك", "مكينة", "شبس", "علبة", "بزجاج", "عملات", "ومعدنها", "ورق", "المكرمشة", "فلوسها", "مقفول", "تتفرج", "زنبرك", "ماطور",
                      "الحافة", "يعلق", "يستهزئ", "أشعة", "ثانية", "فلوسك", "يهز", "ببلاش", "طن", "بمسامير", "باب", "وإنذار", "تابعني", "مترو",
                      "تنوّر", "أزيز", "محد", "وصفر", "بيدك", "الثلاثاء", "ثنين"]}
    KEYS = {"ar_sa": {
        ("hook", "SNACKS"): "شبس", ("hook", "SHELF"): "رف", ("hook", "JAR"): "علبة", ("hook", "MONEY"): "للفلوس", ("hook", "CONGRATS"): "مبروك",
        ("break1", "PEOPLE"): "الناس", ("break1", "TAKE"): "ياخذون", ("break1", "JAR"): "والعلبة",
        ("fix1", "LOCK"): "فتقفل", ("fix1", "GLASS"): "بزجاج", ("fix1", "COIN"): "عملات", ("fix1", "CHECKS"): "تفحص", ("fix1", "SIZE"): "حجم",
        ("fix1", "METAL"): "ومعدنها", ("fix1", "BILL"): "وقارئ", ("fix1", "SCANS"): "يفحص", ("fix1", "LIGHT"): "بالضوء", ("fix1", "HATES"): "ويكره",
        ("fix1", "WRINKLES"): "المكرمشة",
        ("break2", "PAID"): "فلوسها", ("break2", "LOCKED"): "مقفول", ("break2", "LOOK"): "تتفرج", ("break2", "CHIPS"): "شبس",
        ("fix2", "SIT"): "فتحط", ("fix2", "SPIRAL"): "زنبرك", ("fix2", "MOTOR"): "ماطور", ("fix2", "ONE"): "لفة", ("fix2", "TURN"): "كاملة",
        ("fix2", "FRONT"): "قدام", ("fix2", "WALKS"): "يطيح", ("fix2", "EDGE"): "الحافة",
        ("break3", "CHIPS"): "كيس", ("break3", "STUCK"): "يعلق", ("break3", "HANGING"): "معلّق", ("break3", "CORNER"): "زاوية", ("break3", "MOCKING"): "يستهزئ",
        ("fix3", "INVISIBLE"): "تنشاف", ("fix3", "BEAMS"): "أشعة", ("fix3", "BOTTOM"): "تحت", ("fix3", "NOTHING"): "طاح", ("fix3", "TURNS"): "يلف",
        ("fix3", "AGAIN"): "ثانية", ("fix3", "MONEY"): "فلوسك",
        ("break4", "FAIR"): "عادلة", ("break4", "ROCKS"): "يهز", ("break4", "FREE"): "ببلاش", ("break4", "BAD"): "فكرة", ("break4", "WEIGHS"): "وزنها",
        ("break4", "TON"): "طن",
        ("fix4", "BOLT"): "فتثبتها", ("fix4", "DOWN"): "الأرض", ("fix4", "FLAP"): "باب", ("fix4", "ARMS"): "اليدين", ("fix4", "ALARM"): "وإنذار",
        ("fix4", "SCREAMS"): "يصارخ", ("fix4", "TILTS"): "مالت",
        ("cta", "PICK"): "تختار", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "GLOWING"): "تنوّر", ("reveal", "HUM"): "أزيز", ("reveal", "NOBODY"): "محد", ("reveal", "BUYS"): "يشتريه",
        ("stat", "ONE"): "مكينة", ("stat", "FIVE"): "خمسمية", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CHIPS"): "والشبس", ("tag", "SLOT"): "خانة", ("tag", "STUCK"): "عالق", ("tag", "TUESDAY"): "الثلاثاء", ("tag", "BUY"): "تشتري",
        ("tag", "TWO"): "ثنين"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a metro"),
                   "stat": [("1", "MACHINE"), ("500", "SNACKS"), ("0", "CASHIERS")],
                   "L": {"jar": "PAY HERE", "size": "SIZE", "metal": "METAL", "fake": "A BUTTON", "light": "LIGHT SCAN", "wrinkle": "TOO WRINKLED",
                         "paid": "PAID", "spiral": "SPIRAL", "motor": "MOTOR", "turn": "ONE FULL TURN", "stuck": "STUCK", "beams": "LIGHT BEAMS",
                         "nothing": "NOTHING FELL", "again": "TURN AGAIN", "refund": "OR A REFUND", "ton": "A QUARTER TON", "bolts": "BOLTS",
                         "flap": "ANTI-THEFT FLAP", "alarm": "TILT ALARM", "nobody": "NOBODY BUYS IT", "b4": "SLOT B4"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مترو"),
                      "stat": [("1", "مكينة"), ("500", "كيس"), ("0", "كاشير")],
                      "L": {"jar": "ادفع هنا", "size": "الحجم", "metal": "المعدن", "fake": "زرار قميص", "light": "فحص بالضوء", "wrinkle": "مكرمشة مرة",
                            "paid": "تم الدفع", "spiral": "زنبرك", "motor": "ماطور", "turn": "لفة كاملة", "stuck": "علق", "beams": "أشعة ضوء",
                            "nothing": "ما طاح شي", "again": "لف مرة ثانية", "refund": "أو ترجع فلوسك", "ton": "ربع طن", "bolts": "مسامير",
                            "flap": "باب ضد السرقة", "alarm": "إنذار الميلان", "nobody": "محد يشتريه", "b4": "خانة بي أربعة"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "snacks": ("hook", "SNACKS", 0.16), "shelf": ("hook", "SHELF", 0.28), "jar": ("hook", "JAR", 0.42), "money": ("hook", "MONEY", 0.52),
            "congrats": ("hook", "CONGRATS", 0.6),
            "people": ("break1", "PEOPLE", 0.2), "take": ("break1", "TAKE", 0.3), "jar2": ("break1", "JAR", 0.9),
            "lock": ("fix1", "LOCK", 0.08), "glass": ("fix1", "GLASS", 0.18), "coin": ("fix1", "COIN", 0.28), "checks": ("fix1", "CHECKS", 0.36),
            "size": ("fix1", "SIZE", 0.46), "metal": ("fix1", "METAL", 0.52), "bill": ("fix1", "BILL", 0.64), "scans": ("fix1", "SCANS", 0.72),
            "light": ("fix1", "LIGHT", 0.82), "hates": ("fix1", "HATES", 0.9), "wrinkles": ("fix1", "WRINKLES", 0.95),
            "paid": ("break2", "PAID", 0.2), "locked": ("break2", "LOCKED", 0.46), "look": ("break2", "LOOK", 0.84), "chips": ("break2", "CHIPS", 0.95),
            "sit": ("fix2", "SIT", 0.1), "spiral": ("fix2", "SPIRAL", 0.38), "motor": ("fix2", "MOTOR", 0.5), "one": ("fix2", "ONE", 0.58),
            "turn": ("fix2", "TURN", 0.66), "front": ("fix2", "FRONT", 0.78), "walks": ("fix2", "WALKS", 0.86), "edge": ("fix2", "EDGE", 0.96),
            "chips2": ("break3", "CHIPS", 0.2), "stuck": ("break3", "STUCK", 0.32), "hanging": ("break3", "HANGING", 0.46), "corner": ("break3", "CORNER", 0.68),
            "mocking": ("break3", "MOCKING", 0.82),
            "invisible": ("fix3", "INVISIBLE", 0.12), "beams": ("fix3", "BEAMS", 0.24), "bottom": ("fix3", "BOTTOM", 0.36), "nothing": ("fix3", "NOTHING", 0.46),
            "turns": ("fix3", "TURNS", 0.66), "again": ("fix3", "AGAIN", 0.72), "moneyb": ("fix3", "MONEY", 0.9),
            "fair": ("break4", "FAIR", 0.12), "rocks": ("break4", "ROCKS", 0.32), "free": ("break4", "FREE", 0.5), "bad": ("break4", "BAD", 0.6),
            "weighs": ("break4", "WEIGHS", 0.74), "ton": ("break4", "TON", 0.94),
            "bolt": ("fix4", "BOLT", 0.1), "down": ("fix4", "DOWN", 0.18), "flap": ("fix4", "FLAP", 0.34), "arms": ("fix4", "ARMS", 0.56),
            "alarm": ("fix4", "ALARM", 0.7), "screams": ("fix4", "SCREAMS", 0.8), "tilts": ("fix4", "TILTS", 0.95),
            "pick": ("cta", "PICK", 0.2), "follow": ("cta", "FOLLOW", 0.4),
            "glowing": ("reveal", "GLOWING", 0.2), "hum": ("reveal", "HUM", 0.46), "nobody": ("reveal", "NOBODY", 0.74), "buys": ("reveal", "BUYS", 0.94),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "FIVE", 0.36), "s3": ("stat", "ZERO", 0.72),
            "cong2": ("closer", "CONGRATS", 0.16),
            "chips3": ("tag", "CHIPS", 0.14), "slot": ("tag", "SLOT", 0.26), "stuck2": ("tag", "STUCK", 0.42), "tuesday": ("tag", "TUESDAY", 0.52),
            "buy": ("tag", "BUY", 0.64), "two": ("tag", "TWO", 0.9)})
        T["glass0"] = min(T["lock"], T["glass"]) - 0.1
        T["checkcut"] = T["coin"] - 0.4
        T["sizechk"] = min(T["size"], T["metal"])
        T["metalchk"] = max(T["size"], T["metal"])
        T["turn1"] = min(T["one"], T["turn"]) - 0.1
        T["fall1"] = max(T["walks"], T["front"]) - 0.05
        T["turn2"] = T["chips2"] - 0.25
        T["hang"] = min(T["stuck"], T["hanging"]) - 0.05
        T["turn3"] = min(T["turns"], T["again"]) - 0.05
        T["rock0"] = T["rocks"] - 0.15
        T["tip"] = T["bad"] - 0.05
        T["arm0"] = min(T["flap"], T["arms"]) + 0.1
        T["siren"] = min(T["alarm"], T["screams"])
        T["second"] = T["buy"] + 0.2
        self.cut(s("break1") - 0.1, "front", 1)
        self.cut(s("fix1") - 0.12, "front", 1)
        self.cut(T["checkcut"], "check", 1)
        self.cut(s("break2") - 0.1, "front", -1)
        self.cut(s("fix2") - 0.12, "side", 1)
        self.cut(s("break4") - 0.12, "front", -1)
        self.cut(s("fix4") - 0.12, "front", 1)
        self.cut(s("cta") + 0.05, "front", -1)
        self.cut(s("reveal") - 0.1, "front", 1)
        self.cut(T["s1"] - 0.35, "front", 1)
        self.cut(s("tag") - 0.2, "front", -1)
        fc = Camera(0, -205, 1.3)
        fc.key(0.05, 0, -193, 1.4, 1.6)
        fc.key(s("break1") - 0.1, 0, -193, 1.4, 0.0)
        fc.key(s("fix1") - 0.12, 0, -193, 1.4, 0.0)
        fc.key(s("break2") - 0.1, -40, -193, 1.4, 0.0).key(T["look"] - 0.5, -120, -170, 1.6, 0.8)
        fc.key(s("break4") - 0.12, -20, -193, 1.4, 0.0)
        fc.key(s("fix4") - 0.12, 0, -110, 2.3, 0.0).key(T["arm0"] - 0.45, -40, -118, 2.3, 0.5).key(T["siren"] - 0.5, -20, -193, 1.4, 0.7)
        fc.key(s("cta") + 0.05, 90, -300, 2.2, 0.0)
        fc.key(s("reveal") - 0.1, 0, -193, 1.4, 0.0).key(T["nobody"] - 0.5, -90, -150, 2.3, 0.7)
        fc.key(T["s1"] - 0.35, 0, -223, 0.9, 0.0).key(s("closer"), 0, -215, 0.96, 2.2)
        fc.key(s("tag") - 0.2, -110, -300, 1.7, 0.0).key(T["buy"] - 0.3, -90, -310, 1.85, 0.8)
        self.fcam = fc
        sc = Camera(-25, 243, 1.4)
        sc.key(s("fix2") - 0.12, -25, 243, 1.4, 0.0)
        sc.key(s("break3") - 0.1, -110, 215, 1.65, 0.7)
        sc.key(s("fix3") - 0.1, -50, 262, 1.45, 0.8)
        self.scam = sc
        tw = 2 * math.pi
        self.phi = (Track(0.0).to(T["turn1"], tw, max(0.5, T["fall1"] - T["turn1"] + 0.15), e_io)
                    .to(T["turn2"], tw * 2, max(0.4, T["hang"] - T["turn2"] + 0.1), e_io)
                    .to(T["turn3"], tw * 2.42, 0.6, e_io))
        self.spans = [(T["take"], T["glass0"] + 0.5), (T["locked"], T["fall1"] + 0.5), (T["hang"], T["turn3"] + 0.9), (T["tip"], T["tilts"])]
        self.shakes = [(T["jar2"], 0.25, 8), (T["glass0"] + 0.45, 0.2, 8), (T["fall1"] + 0.45, 0.2, 8), (T["tip"], 0.5, 12), (T["siren"], 0.3, 8)]

    # ------------------------------------------------------------------ set: the machine from the front
    def phase(self, t):
        s, T = self.tl.s, self.T
        for name, t0 in (("tag", s("tag") - 0.2), ("stat", T["s1"] - 0.35), ("reveal", s("reveal") - 0.1), ("cta", s("cta") + 0.05), ("fix4", s("fix4") - 0.12),
                         ("rock", s("break4") - 0.12), ("locked", s("break2") - 0.1), ("glass", s("fix1") - 0.12), ("steal", s("break1") - 0.1), ("shelf", 0.0)):
            if t >= t0:
                return name

    def draw_front(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.fcam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        ph = self.phase(t)
        self.view(c, cam)
        c.drawRect(R(-1100, -2400, 2200, 1410), P(shade("#2B3555", 0.14)))
        room(c, -1100, -1000, 2200, 1000, wall="#2B3555", floor="#3F4A6B", t=t, lamp=True, lamp_x=-330, panels=160)
        c.drawRect(R(-1100, -40, 2200, 40), P("#1B2440"))
        v2.ground(c, -3400, 3400) if False else None
        c.drawRect(R(-1100, 26, 2200, 1400), P("#161B33"))
        if ph in ("shelf", "steal"):
            self.shelf(c, t, ph)
        else:
            tilt = 0.0
            if ph == "rock":
                amp = 9 * prog(t, T["rock0"], T["tip"]) + 6 * prog(t, T["tip"], T["tip"] + 0.4)
                tilt = -amp * abs(math.sin((t - T["rock0"]) * 7.5)) if t >= T["rock0"] else 0.0
                tilt *= 1 - prog(t, T["weighs"], T["ton"])
            elif ph == "fix4" and t >= T["siren"] - 0.2:
                tilt = -3.5 * abs(math.sin(t * 9)) * (1 - prog(t, T["tilts"], T["tilts"] + 0.4))
            gl = e_out(prog(t, T["glass0"], T["glass0"] + 0.5)) if ph == "glass" else 1.0
            bd = e_back(prog(t, s("fix1") - 0.05, T["glass0"] + 0.1)) if ph == "glass" else 1.0
            lit = 1.0 if ph in ("stat", "tag") else prog(t, T["glowing"] - 0.2, T["glowing"] + 0.3) if ph == "reveal" else 0.0
            flick = 0.85 + 0.15 * math.sin(t * 40) if ph == "reveal" and t < T["glowing"] + 0.5 else 1.0
            stuck = 0
            if ph == "tag":
                stuck = 1 if t < T["second"] + 0.5 else 2
            machine(c, t, glass=gl, body=clamp(bd), lit=lit * flick, bolts=prog(t, T["bolt"] - 0.1, T["down"] + 0.4) if ph == "fix4" else 1.0 if ph in ("cta", "reveal", "stat", "tag") else 0.0,
                    beacon=1.0 if ph == "fix4" and T["siren"] <= t else 0.0, tilt=tilt, paid=ph == "locked" and t >= T["paid"],
                    flap=e_back(prog(t, T["flap"] - 0.2, T["flap"] + 0.1)) if ph == "fix4" else 1.0 if ph in ("cta", "reveal", "stat", "tag") else 0.0,
                    dusty=ph in ("reveal", "stat", "tag"), stuck=stuck)
            if ph == "reveal" and t >= T["hum"] - 0.2:                                # the hum
                for sd in (-1, 1):
                    for i in range(3):
                        u = (t * 1.4 + i / 3) % 1.0
                        c.drawArc(R(sd * 200 - 40 - 60 * u, -420 - 60 * u, 80 + 120 * u, 80 + 120 * u), -40 if sd > 0 else 140, 80, False,
                                  P("#FDE68A", 0.8 * (1 - u), stroke=5))
            if ph == "fix4" and T["arm0"] - 0.1 <= t < T["siren"] - 0.5:               # the sneaky arm, and the flap that stops it
                u = e_out(prog(t, T["arm0"], T["arm0"] + 0.4))
                wig = math.sin(t * 16) * 4 * (1 if u >= 1 else 0)
                c.drawLine(-330, -30, lerp(-330, -120, u), lerp(-30, -66, u) + wig, P("#E8B48A", 1, stroke=24))
                c.drawCircle(lerp(-330, -120, u), lerp(-30, -66, u) + wig, 18, P("#E8B48A"))
                c.drawLine(-420, -20, -330, -30, P(THIEF, 1, stroke=34))
            if ph == "stat" and t >= T["cong2"]:                                      # one for the road
                u = prog(t, T["cong2"] + 0.1, T["cong2"] + 0.6)
                bag(c, -20, lerp(-372, -62, e_in(u)), BAGS[5], 0.86, 200 * u)
        self.people_front(c, t, ph)
        c.restore()
        self.ui["cam"] = cam

    def shelf(self, c, t, ph):
        """Before it is a machine: three planks, snacks, and a jar that trusts you."""
        T, s = self.T, self.tl.s
        for sx in (-176, 164):
            c.drawRect(R(sx, -520, 12, 520), P("#8B5E3C"))
        taken = 0
        if ph == "steal":
            taken = int(13 * prog(t, T["take"] - 0.2, T["jar2"] - 0.3))
        k = 0
        for r_, ry in enumerate((-380, -240, -100)):
            box(c, -180, ry, 360, 12, "#A9744A", r=3)
            for i in range(5 if r_ < 2 else 3):
                k += 1
                pop_in = e_back(prog(t, 0.05 + k * 0.05, 0.3 + k * 0.05))
                if k <= taken:
                    continue
                bag(c, -140 + i * 62, ry, BAGS[k % len(BAGS)], pop_in)
        jar_gone = ph == "steal" and t >= T["jar2"] - 0.25
        if not jar_gone:
            jk = e_back(prog(t, T["jar"] - 0.4, T["jar"] - 0.1))
            c.save()
            c.translate(96, -100)
            c.scale(jk, jk)
            c.drawRRect(rr(-30, -78, 60, 78, 12), P("#BAE6FD", 0.35))
            c.drawRRect(rr(-30, -78, 60, 78, 12), P("#E0F2FE", 0.9, stroke=3))
            c.drawRRect(rr(-24, -88, 48, 12, 4), P("#94A3B8"))
            n = 2 + int(3 * prog(t, T["money"], T["congrats"] + 0.6))
            for i in range(n):
                coin(c, -12 + (i % 3) * 12, -10 - (i // 3) * 9 - (i % 2) * 4, 9)
            c.restore()
            if T["money"] - 0.25 <= t < T["money"] + 0.1:
                u = prog(t, T["money"] - 0.25, T["money"] + 0.1)
                coin(c, lerp(40, 96, u), lerp(-260, -176, e_in(u)), 10, 400 * u)

    def people_front(self, c, t, ph):
        T, s = self.T, self.tl.s
        if ph == "shelf":
            buyer = e_io(prog(t, 0.1, T["shelf"]))
            bx = lerp(-520, -292, buyer)
            engineer(c, bx, 0, HB, SHIRTS[0], t * 1.3, "walk" if buyer < 1 else "point" if t < T["jar"] else "cheer" if t >= T["congrats"] - 0.1 else "carry", face=1)
            if T["jar"] - 0.1 <= t < T["congrats"] - 0.1:
                bag(c, bx + 78, -150, BAGS[1], 1.0, 10)
            engineer(c, 300, 0, HB - 24, SHIRTS[1], t, "cheer" if t >= T["congrats"] - 0.1 else "look", face=-1)
        elif ph == "steal":
            engineer(c, 300, 0, HB - 24, SHIRTS[1], t, "shrug" if t >= T["jar2"] else "look", face=-1)
            for i, (col, hat) in enumerate((("#F472B6", "none"), ("#60A5FA", "cap"), (THIEF, "beanie"))):
                t0 = T["take"] - 0.5 + i * (T["jar2"] - T["take"]) / 2.4
                u = prog(t, t0, t0 + 0.95)
                if 0 < u < 1:
                    x = lerp(-560, 560, u)
                    person(c, x, 0, HB - 10, col, t * 2.2 + i, "carry" if u > 0.4 else "walk", face=1, hat=hat, pants="#1F2937")
                    if u > 0.4:
                        if i == 2:
                            c.drawRRect(rr(x + 54, -230, 60, 78, 12), P("#BAE6FD", 0.5))
                            c.drawRRect(rr(x + 54, -230, 60, 78, 12), P("#E0F2FE", 0.9, stroke=3))
                        else:
                            bag(c, x + 84, -140, BAGS[i + 2], 1.1, 12)
        elif ph == "glass":
            engineer(c, 300, 0, HB - 24, SHIRTS[1], t, "cheer" if t >= T["glass0"] + 0.5 else "look", face=-1)
        elif ph == "locked":
            arrive = e_out(prog(t, s("break2") - 0.1, T["paid"] - 0.25))
            lean = e_out(prog(t, T["look"] - 0.45, T["look"]))
            px = lerp(-560, -300, arrive) + 46 * lean
            engineer(c, px, 0, HB, SHIRTS[0], t * 1.3, "walk" if arrive < 1 else "point" if t < T["locked"] else "carry" if lean > 0 else "shrug", face=1)
            if T["paid"] - 0.3 <= t < T["paid"]:
                u = prog(t, T["paid"] - 0.3, T["paid"])
                coin(c, lerp(-210, 132, u), lerp(-250, -410, u) - 60 * math.sin(math.pi * u), 11, 500 * u)
            if t >= T["locked"]:
                for i in range(2):
                    text(c, "?", px - 10 + i * 34, -340 - 12 * math.sin(t * 5 + i), 64, HILITE, "Poppins-Black")
        elif ph == "rock":
            arrive = e_out(prog(t, T["rock0"] - 0.7, T["rock0"]))
            away = e_out(prog(t, T["tip"] + 0.1, T["tip"] + 0.5))
            px = lerp(-560, -268, arrive) - 80 * away
            shove = math.sin((t - T["rock0"]) * 7.5) * 14 if T["rock0"] <= t < T["tip"] else 0
            person(c, px + shove, 0, HB + 10, THIEF, t * 1.4, "walk" if arrive < 1 else "carry" if t < T["tip"] else "duck", face=1, hat="beanie", pants="#111827")
            engineer(c, 312, 0, HB - 40, SHIRTS[1], t, "look" if t < T["tip"] else "duck", face=-1)
        elif ph == "fix4":
            if t >= T["siren"] - 0.5:
                run = e_in(prog(t, T["siren"] + 0.25, T["tilts"] + 0.2))
                px = lerp(-268, -640, run)
                person(c, px, 0, HB + 10, THIEF, t * 2.4, "carry" if run <= 0 else "walk", face=1 if run <= 0 else -1, hat="beanie", pants="#111827")
                engineer(c, 312, 0, HB - 40, SHIRTS[1], t, "cheer" if t >= T["tilts"] else "look", face=-1)
        elif ph == "cta":
            hx = lerp(40, 118, e_out(prog(t, s("cta") + 0.1, T["pick"] + 0.2)))
            c.drawLine(hx - 90, -420, hx, -494, P("#E8B48A", 1, stroke=20))
            c.drawCircle(hx, -494, 13, P("#E8B48A"))
            c.drawLine(hx - 150, -390, hx - 90, -420, P(SHIRTS[0], 1, stroke=26))
        elif ph == "stat":
            for i, (px, fc_) in enumerate(((-450, 1), (-320, 1), (330, -1))):
                engineer(c, px, 0, 236 + (i % 2) * 14, SHIRTS[i], t + i * 0.37, "cheer", face=fc_)
            if t >= T["cong2"]:
                hats_in_the_air(c, (-450, -320, 330), -290, t, T["cong2"], height=300)
        elif ph == "tag":
            pose = "point" if t < T["stuck2"] else "duck" if t >= T["two"] else "carry" if T["buy"] - 0.1 <= t < T["second"] + 0.3 else "shrug"
            engineer(c, -300, 0, HB, SHIRTS[0], t, pose, face=1)
            if T["buy"] - 0.1 <= t < T["second"]:
                u = prog(t, T["buy"] - 0.1, T["second"])
                coin(c, lerp(-220, 132, u), lerp(-240, -410, u) - 50 * math.sin(math.pi * u), 11, 500 * u)

    # ------------------------------------------------------------------ set: one shelf from the side
    def draw_side(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.scam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        self.view(c, cam)
        c.drawRect(R(-1400, -1400, 2800, 2800), lin_paint(0, -600, 0, 800, ["#1B2238", "#141A30"]))
        # the cabinet
        c.drawRRect(rr(GLASS_X - 30, -180, 720, 666, 22), P(BODY))
        c.drawRRect(rr(GLASS_X, -152, 664, 610, 12), P("#0B1220"))
        c.drawRect(R(GLASS_X - 10, -152, 12, 510), P("#BAE6FD", 0.45))                 # the glass front
        c.drawRect(R(GLASS_X - 10, 368, 12, 90), P("#94A3B8"))                        # the bin door
        c.drawRRect(rr(GLASS_X, BIN_Y, 190, 38, 6), P("#334155"))
        phi = self.phi.at(t)
        for row, sy in enumerate((0, ROW2)):
            c.drawRect(R(EDGE, sy, 500, 10), P("#94A3B8"))
            ph_ = phi if row == 0 else 0.0
            self.helix(c, sy - 52, ph_, back=True)
            shift = -PITCH * ph_ / (2 * math.pi)
            for i in range(4):
                bx = EDGE + 58 + i * PITCH + shift
                col = BAGS[(i + row * 3) % len(BAGS)]
                if row == 0 and i == 0:
                    self.first_bag(c, t, bx, col)
                elif row == 0 and i == 1:
                    self.second_bag(c, t, bx, col)
                elif bx > EDGE + 10:
                    bag(c, bx, sy, col, BS)
            self.helix(c, sy - 52, ph_, back=False)
            # the motor at the back
            c.drawRRect(rr(232, sy - 96, 66, 92, 12), lin_paint(232, 0, 298, 0, ["#64748B", "#1F2937"]))
            c.save()
            c.translate(236, sy - 52)
            c.rotate(math.degrees(ph_))
            for an in range(0, 360, 45):
                c.drawLine(0, 0, math.cos(math.radians(an)) * 24, math.sin(math.radians(an)) * 24, P("#F59E0B", 1, stroke=6))
            c.drawCircle(0, 0, 12, P("#FDE68A"))
            c.restore()
        # the light beams across the way down
        bk = prog(t, T["beams"] - 0.2, T["beams"] + 0.2) if t >= s("fix3") - 0.1 else 0.0
        if bk > 0:
            broken = T["turn3"] + 0.72 <= t < T["turn3"] + 0.98
            for i, by in enumerate((300, 332, 364)):
                c.drawRRect(rr(GLASS_X + 2, by - 9, 14, 18, 4), P("#E5E9F2", bk))
                c.drawRRect(rr(EDGE - 16, by - 9, 14, 18, 4), P("#E5E9F2", bk))
                col = GOOD if broken else "#F87171"
                c.drawLine(GLASS_X + 16, by, lerp(GLASS_X + 16, EDGE - 16, bk), by, dash_paint(col, 0.6 + 0.25 * math.sin(t * 9 + i), 5 if not broken else 8, t, dash=12, gap=10))
        if t >= s("fix3") and t >= T["moneyb"] - 0.2:                                 # ...or your money back
            c.drawRRect(rr(150, 400, 150, 18, 7), P("#94A3B8"))
            for i in range(3):
                u = prog(t, T["moneyb"] - 0.2 + i * 0.1, T["moneyb"] + 0.25 + i * 0.1)
                if u > 0:
                    coin(c, 186 + i * 38, lerp(280, 382, e_in(min(1.0, u))), 17, 300 * u)
        c.restore()
        self.ui["cam"] = cam

    def helix(self, c, axis, phi, back):
        """A spiral seen from the side: the far half drawn first (dark), the near half last (bright)."""
        p = skia.Path()
        started = False
        x = EDGE + 6
        while x <= 232:
            th = 2 * math.pi * (x - EDGE) / PITCH + phi
            near = math.cos(th) > 0
            y = axis + CR * math.sin(th)
            if near != back:
                if not started:
                    p.moveTo(x, y)
                    started = True
                else:
                    p.lineTo(x, y)
            else:
                started = False
            x += 3
        pr = P("#64748B" if back else "#E5E9F2", 1, stroke=8)
        pr.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPath(p, pr)

    def first_bag(self, c, t, bx, col):
        """The one that walks off the edge on the first turn."""
        T = self.T
        if t < self.T["fall1"]:
            bag(c, bx, 0, col, BS)
            return
        dt = t - T["fall1"]
        y = min(BIN_Y - 4.0, 0 + 1000 * dt * dt)
        landed = y >= BIN_Y - 4
        bag(c, EDGE - 46 - 44 * min(dt, 0.5), y, col, BS, -70 * min(dt * 2.4, 1.0) if not landed else -90)

    def second_bag(self, c, t, bx, col):
        """The one that gets stuck, hanging by a corner, until the spiral turns a little more."""
        T = self.T
        if t < T["hang"]:
            bag(c, bx, 0, col, BS)
            return
        free = T["turn3"] + 0.45
        if t < free:
            sw = 12 * math.sin((t - T["hang"]) * 5.5) * math.exp(-(t - T["hang"]) * 0.5) + 6 * math.sin(t * 3)
            c.save()
            c.translate(EDGE - 8, -6)
            c.rotate(-58 + sw)
            bag(c, -30, 87, col, BS, 0, face=t >= T["mocking"] - 0.3)
            c.restore()
            return
        dt = t - free
        y = min(BIN_Y - 4.0, 60 + 1000 * dt * dt)
        bag(c, EDGE - 90, y, col, BS, -58 - 60 * min(dt * 2, 1.0), face=False)

    # ------------------------------------------------------------------ set: what the slots check
    def draw_check(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#141A30", "#1B2440", "#101528"]))
        # ---- the coin lane
        c.drawRRect(rr(40, 400, 1000, 480, 34), P("#0B1220", 0.8))
        c.drawRRect(rr(40, 400, 1000, 480, 34), P("#FFFFFF", 0.25, stroke=3))
        ramp = lambda x: 580 + (x - 150) * 0.15                                       # the centre line the coins roll along
        c.drawLine(110, ramp(110) + 50, 770, ramp(770) + 50, P("#94A3B8", 1, stroke=12))
        c.drawRRect(rr(96, 430, 110, 26, 8), P("#E5E9F2"))                            # the slot
        c.drawRRect(rr(116, 437, 70, 12, 5), P("#0B1220"))
        gx, mx = 410, 620
        t_fake = T["checkcut"] + 0.35
        fake_at_gate = t_fake + 0.55
        fake_bad = t >= fake_at_gate
        real0 = max(T["checks"] - 0.1, fake_at_gate + 0.3)
        ok1 = t >= T["sizechk"]
        ok2 = t >= T["metalchk"]
        gcol = WARN if fake_at_gate <= t < fake_at_gate + 0.7 else GOOD if ok1 else "#E5E9F2"
        c.drawRRect(rr(gx - 62, ramp(gx) - 62, 16, 118, 6), P(gcol))                  # the size gauge: a gate exactly one coin high
        c.drawRRect(rr(gx + 46, ramp(gx) - 62, 16, 118, 6), P(gcol))
        c.drawRRect(rr(gx - 62, ramp(gx) - 70, 124, 18, 7), P(gcol))
        mcol = GOOD if ok2 else "#C7803E"                                            # the metal check: two coils
        for dx in (-38, 38):
            for i in range(6):
                c.drawOval(R(mx + dx - 13, ramp(mx) - 62 + i * 19, 26, 30), P(mcol, 1, stroke=5))
        if ok2 and t < T["metalchk"] + 0.5:
            add_glow(c, mx, ramp(mx), 170, GOOD, 0.6 * (1 - prog(t, T["metalchk"], T["metalchk"] + 0.5)))
        c.drawRRect(rr(800, 650, 190, 180, 16), P("#334155"))                         # the cash box
        c.drawRRect(rr(800, 650, 190, 180, 16), P("#CBD5E1", 1, stroke=4))
        c.drawRRect(rr(848, 640, 94, 16, 6), P("#0B1220"))
        c.drawRRect(rr(100, 796, 190, 56, 14), P("#1F2937"))                          # the cup the rejects come back to
        c.drawRRect(rr(100, 796, 190, 56, 14), P("#94A3B8", 1, stroke=3))
        if t >= t_fake:                                                              # the fake: stopped at the gate, dropped, sent back
            if not fake_bad:
                u = prog(t, t_fake, fake_at_gate)
                x = lerp(150, gx - 40, e_in(u))
                coin(c, x, ramp(x) + 8, 36, 700 * u, fake=True)
            else:
                dt = t - fake_at_gate
                u = clamp(dt / 0.7)
                x = lerp(gx - 40, 196, e_io(u))
                y = lerp(ramp(gx - 40) + 8, 808, e_in(clamp(dt / 0.4)))
                coin(c, x, y, 36, -300 * dt, fake=True, a=1 - prog(t, fake_at_gate + 1.0, fake_at_gate + 1.3))
        if t >= real0:                                                               # the real coin
            t_end = T["metalchk"] + 0.45
            if t < T["sizechk"]:
                x = lerp(150, gx, e_io(prog(t, real0, T["sizechk"])))
            elif t < T["metalchk"]:
                x = lerp(gx, mx, prog(t, T["sizechk"], T["metalchk"]))
            else:
                x = lerp(mx, 770, e_in(prog(t, T["metalchk"], t_end)))
            if t < t_end:
                coin(c, x, ramp(x), 44, x * 1.4)
            else:
                dt = t - t_end
                yy = min(720.0, ramp(770) + 900 * dt * dt)
                if dt < 0.5:
                    coin(c, lerp(770, 894, clamp(dt * 5)), yy, 44, 800 * dt, a=1 - prog(dt, 0.25, 0.5))
        # ---- the bill lane
        c.drawRRect(rr(40, 900, 1000, 320, 34), P("#0B1220", 0.8))
        c.drawRRect(rr(40, 900, 1000, 320, 34), P("#FFFFFF", 0.25, stroke=3))
        by = 1060
        c.drawRRect(rr(380, 930, 600, 260, 26), P("#1F2937"))
        c.drawRRect(rr(380, 930, 600, 260, 26), P("#94A3B8", 1, stroke=4))
        c.drawRRect(rr(364, by - 80, 26, 160, 8), P("#0B1220"))
        for rx_ in (470, 680, 890):                                                  # rollers
            for yy in (by - 88, by + 88):
                c.drawCircle(rx_, yy, 18, P("#64748B"))
                c.drawLine(rx_, yy, rx_ + 18 * math.cos(t * 8), yy + 18 * math.sin(t * 8), P("#E5E9F2", 1, stroke=4))
        good_in = e_out(prog(t, T["bill"] - 0.2, T["bill"] + 0.35))
        scan = prog(t, T["scans"] - 0.1, T["light"] + 0.1)
        t_w = T["hates"] - 0.45
        if t < t_w and good_in > 0:
            away = prog(t, T["light"] + 0.25, T["light"] + 0.6)
            bx = lerp(150, 680, good_in) + 460 * e_in(away)
            c.save()
            c.clipRect(R(0, 900, 980, 320))
            bill(c, bx, by, 280, 130, a=1.0)
            c.restore()
            if 0 < scan < 1:
                lx = lerp(550, 810, scan)
                c.drawRect(R(lx - 6, by - 92, 12, 184), P("#A7F3D0", 0.95))
                add_glow(c, lx, by, 150, GOOD, 0.6)
            if scan >= 1 and away < 1:
                v2.badge(c, 930, 950, prog(t, T["light"] + 0.1, T["light"] + 0.3), "check", t, 0.9)
        if t >= t_w:                                                                 # the wrinkled one: in, scanned, spat out
            u_in = e_out(prog(t, t_w, t_w + 0.35))
            spit = e_out(prog(t, T["wrinkles"] - 0.1, T["wrinkles"] + 0.25))
            bx = lerp(150, 640, u_in) - 440 * spit
            c.save()
            c.clipRect(R(0, 900, 980, 320))
            c.translate(bx, by)
            c.rotate(-16 * spit)
            bill(c, 0, 0, 280, 130, wrinkled=True)
            c.restore()
            if u_in >= 1 and spit <= 0:
                lx = 550 + ((t * 300) % 260)
                c.drawRect(R(lx - 6, by - 92, 12, 184), P("#FCA5A5", 0.95))
            if spit > 0:
                v2.badge(c, 930, 950, clamp(spit * 2), "alert", t, 0.9)
        self.ui["cam"] = (0, 0, 1)
        self.ui["gate"] = (gx, ramp(gx) - 96)
        self.ui["coil"] = (mx, ramp(mx) - 60)
        self.ui["fake"] = fake_at_gate

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -200, 1.4)), x, y)

    def ui_front(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        ph = self.phase(tw)
        if ph == "shelf":
            x0, y0 = self.at(96, -186)
            self.label(x0, y0, x0 + 90, y0 - 330, "jar", T["jar"] - 0.1, T["congrats"] + 0.4, HILITE)
        elif ph == "steal":
            self.badge("alert", T["take"], s("fix1") - 0.2, x=880, y=420)
            self.red(T["take"], 1.8)
        elif ph == "glass":
            self.badge("check", T["glass0"] + 0.5, T["checkcut"], x=880, y=420)
        elif ph == "locked":
            x0, y0 = self.at(137, -574)
            self.label(x0, y0, x0 + 40, y0 - 170, "paid", T["paid"], T["locked"] - 0.1, GOOD)
            self.badge("alert", T["locked"], s("fix2") - 0.2, x=880, y=420)
            self.red(T["locked"], 1.8)
        elif ph == "rock":
            self.chip(540, 400, "ton", T["weighs"] - 0.1, s("fix4") - 0.25, accent=WARN, size=48)
            self.badge("alert", T["tip"], s("fix4") - 0.2, x=880, y=560)
            self.red(T["tip"], 1.8)
        elif ph == "fix4":
            x0, y0 = self.at(-160, -22)
            self.label(x0, y0, x0 + 60, y0 - 420, "bolts", T["bolt"] + 0.1, T["flap"] - 0.3, "#E5E9F2")
            x1, y1 = self.at(0, -104)
            self.label(x1, y1, x1 + 190, y1 - 420, "flap", T["flap"] + 0.05, T["siren"] - 0.55, HILITE)
            x2, y2 = self.at(0, -690)
            self.label(x2, y2, x2 + 240, y2 - 40, "alarm", T["siren"] + 0.2, s("cta") - 0.3, WARN)
            self.badge("check", T["tilts"], s("cta") - 0.15, x=880, y=640)
        elif ph == "reveal":
            x0, y0 = self.at(-140, -232)
            self.label(x0, y0, x0 + 120, y0 - 300, "nobody", T["nobody"], T["s1"] - 0.5, "#A3A3A3")
        elif ph == "tag":
            x0, y0 = self.at(60, -440)
            self.label(x0, y0, x0 + 150, y0 - 330, "b4", T["slot"] - 0.1, self.duration + 1, HILITE)

    def ui_side(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break3") - 0.1:
            x0, y0 = self.at(-30, -100)
            self.label(x0, y0, x0 - 60, y0 - 180, "spiral", T["spiral"] - 0.1, T["motor"] - 0.1, "#E5E9F2")
            x1, y1 = self.at(262, -100)
            self.label(x1, y1, x1 - 110, y1 - 180, "motor", T["motor"], T["turn1"] + 0.3, "#F59E0B")
            self.chip(540, 400, "turn", T["turn1"] + 0.1, T["fall1"] + 0.2, accent=HILITE, size=44)
            self.badge("check", T["fall1"] + 0.5, s("break3") - 0.15, x=880, y=420)
        elif tw < s("fix3") - 0.1:
            x0, y0 = self.at(EDGE - 70, 20)
            self.label(x0, y0, x0 + 20, y0 - 330, "stuck", T["hang"] + 0.1, s("fix3") - 0.3, WARN)
            self.badge("alert", T["hang"], s("fix3") - 0.2, x=880, y=420)
            self.red(T["hang"], 1.8)
        else:
            x0, y0 = self.at(-275, 300)
            self.label(x0, y0, x0 + 300, y0 + 60, "beams", T["beams"], T["nothing"] - 0.15, "#F87171")
            self.chip(540, 400, "nothing", T["nothing"] - 0.1, T["turn3"] - 0.05, accent=WARN, size=42)
            self.chip(540, 400, "again", T["turn3"], T["moneyb"] - 0.35, accent=GOOD, size=42)
            self.chip(540, 400, "refund", T["moneyb"] - 0.25, s("break4") - 0.25, accent=HILITE, size=42)
            self.badge("check", T["turn3"] + 0.9, s("break4") - 0.15, x=880, y=560)

    def ui_check(self, c, t, tw):
        T, s = self.T, self.tl.s
        gx, gy = self.ui.get("gate", (400, 500))
        mx, my = self.ui.get("coil", (600, 520))
        fk = self.ui.get("fake", T["checkcut"] + 0.9)
        self.chip(gx, 470, "size", T["checkcut"] + 0.3, T["bill"] - 0.3, accent=HILITE, size=40)
        self.chip(mx + 10, 470, "metal", T["checkcut"] + 0.4, T["bill"] - 0.3, accent="#C7803E", size=40)
        self.chip(430, 824, "fake", fk + 0.1, fk + 1.3, accent=WARN, size=38)
        self.chip(680, 968, "light", T["scans"] - 0.2, T["hates"] - 0.5, accent=GOOD, size=38)
        self.chip(680, 968, "wrinkle", T["wrinkles"] - 0.05, s("break2") - 0.25, accent=WARN, size=38)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10)]
        ev += [(0.1 + i * 0.05, sfx.tap(61 + i), -12) for i in range(8)]
        ev += [(T["jar"] - 0.4, sfx.pop(70), -6), (T["money"] + 0.1, clink(0), -4), (T["congrats"] + 0.1, sfx.chime(), -8)]
        ev += [(T["take"] - 0.4 + i * 0.22, crinkle(0.3, i), -7) for i in range(5)]
        ev += [(T["take"], sfx.alarm(3, 820), -11), (T["jar2"] - 0.25, clink(2), -5), (T["jar2"] + 0.3, sfx.womp(), -8)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["glass0"], sfx.whoosh(0.5, False, 72), -8), (T["glass0"] + 0.45, sfx.thud(0.3, 73), -4),
               (T["glass0"] + 0.5, sfx.lock_click(74), -2), (T["checkcut"], sfx.whoosh(0.4, True, 75), -5), (T["checkcut"] + 0.35, clink(1), -8),
               (T["checkcut"] + 0.9, sfx.buzz(0.3), -8), (T["checkcut"] + 1.3, sfx.clank(700, 0.2, 76), -10),
               (T["sizechk"], sfx.beep(1500, 0.07), -8), (T["metalchk"], sfx.beep(1900, 0.07), -8), (T["metalchk"] + 0.75, clink(3), -4),
               (T["bill"] - 0.2, sfx.whirr(0.6, 180, 260, 77), -11), (T["scans"] - 0.1, sfx.riser(0.6, 78), -13), (T["light"] + 0.15, sfx.beep(1900, 0.09), -8),
               (T["hates"] - 0.45, sfx.whirr(0.5, 180, 260, 79), -12), (T["wrinkles"] - 0.1, sfx.buzz(0.4), -6), (T["wrinkles"], crinkle(0.4, 9), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 80), -5), (T["paid"] - 0.05, clink(4), -5), (T["paid"] + 0.1, sfx.beep(1700, 0.09), -8),
               (T["locked"], sfx.alarm(3, 820), -11), (T["look"] - 0.4, sfx.thud(0.2, 81), -8), (T["chips"] + 0.3, sfx.womp(), -8)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 82), -4), (T["spiral"] - 0.1, sfx.pop(83), -7), (T["motor"], sfx.pop(84), -7),
               (T["turn1"], motor_snd(max(0.5, T["fall1"] - T["turn1"] + 0.15)), -8), (T["fall1"], sfx.whoosh(0.3, False, 85), -10),
               (T["fall1"] + 0.62, sfx.thud(0.25, 86), -3), (T["fall1"] + 0.66, crinkle(0.3, 3), -6), (T["fall1"] + 0.8, sfx.chime(), -7)]
        ev += [(T["turn2"], motor_snd(max(0.4, T["hang"] - T["turn2"] + 0.1)), -8), (T["hang"], crinkle(0.3, 5), -5), (T["hang"] + 0.05, sfx.alarm(3, 820), -11),
               (T["mocking"] - 0.3, sfx.pop(87), -6), (T["mocking"] + 0.3, sfx.womp(), -9)]
        ev += [(T["beams"] - 0.2, sfx.charge_up(0.6), -12), (T["nothing"] - 0.1, sfx.buzz(0.25), -10), (T["turn3"], motor_snd(0.6), -8),
               (T["turn3"] + 0.45, sfx.whoosh(0.3, False, 88), -10), (T["turn3"] + 0.78, sfx.beep(1900, 0.09), -7), (T["turn3"] + 1.0, sfx.thud(0.25, 89), -4),
               (T["moneyb"] - 0.1, clink(5), -5), (T["moneyb"], clink(6), -6), (T["moneyb"] + 0.3, sfx.chime(), -7)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 90), -5)]
        ev += [(T["rock0"] + i * 0.42, sfx.thud(0.25, 91 + i), -5) for i in range(int(max(2, (T["tip"] - T["rock0"]) / 0.42)))]
        ev += [(T["tip"], sfx.alarm(3, 820), -10), (T["tip"] + 0.05, sfx.creak(0.8, 97), -6), (T["weighs"] - 0.1, sfx.pop(98), -6),
               (T["ton"] + 0.05, sfx.thud(0.5, 99), -2)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 100), -4), (T["bolt"] - 0.1, sfx.whirr(0.4, 300, 520, 101), -8), (T["bolt"] + 0.2, sfx.whirr(0.4, 300, 520, 102), -8),
               (T["down"] + 0.35, sfx.thunk(103), -4), (T["flap"] - 0.2, sfx.clank(520, 0.25, 104), -6), (T["arm0"] + 0.4, sfx.thud(0.2, 105), -5),
               (T["arm0"] + 0.5, sfx.buzz(0.25), -9), (T["siren"], sfx.alarm(10, 1250, 0.09, 0.06), -6), (T["tilts"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(106), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 107), -7), (T["follow"] - 0.15, sfx.pop(108), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 109), -6), (T["glowing"] - 0.2, sfx.charge_up(0.6), -8), (T["glowing"] + 0.3, sfx.sparkle(0.7, 9, 110), -8),
               (T["hum"] - 0.2, hum_snd(1.3), -8), (T["nobody"], sfx.pop(111), -6), (T["buys"] + 0.3, sfx.womp(), -11)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 112), -6), (T["s1"], sfx.pop(113), -3), (T["s2"], sfx.pop(114), -3), (T["s3"], sfx.pop(115), -3)]
        ev += [(T["cong2"], sfx.pop(116), -2), (T["cong2"], sfx.sparkle(1.0, 14, 117), -4), (T["cong2"] + 0.1, motor_snd(0.5), -10),
               (T["cong2"] + 0.6, sfx.thud(0.25, 118), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 119), -6), (T["stuck2"], crinkle(0.3, 7), -7), (T["buy"] + 0.15, clink(7), -4),
               (T["second"] + 0.05, motor_snd(0.45), -8), (T["second"] + 0.5, crinkle(0.3, 8), -5), (T["two"] + 0.5, sfx.womp(), -3)]
        return ev


THIEF = "#374151"
NAME = "vending"
EPISODE = Vending
