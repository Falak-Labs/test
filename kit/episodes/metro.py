"""Episode 18 - A driverless metro.  v2 look: three sets.

tunnel    the tunnel cut open along its length: rail top at y = 0, the roof of the bore at y = -250, the street above
          at y = -420.  A car is 300 long.
platform  a station seen from behind the platform: people stand on a floor band y -44..0, the platform edge is its far
          side (y = -44), trains stop behind it, the station ceiling is at y = -360
map       a network map, drawn straight on the screen
"""
from v2_base import *  # noqa: F401,F403

TEAL, STREET, ROOF = "#14B8A6", -420, -250
DOORS = (-78, 78)                                         # door centres along a car
PEOPLE = ("#F472B6", "#60A5FA", "#FBBF24", "#34D399", "#A78BFA", "#FB923C", "#F87171")


def car(c, x, y, t=0.0, col=TEAL, doors=0.0, head=0, tail=0, wheels=True, riders=0, hot=0.0, empty_cab=False, lit=1.0):
    """One car, 300 long, standing on the rail at y. head / tail: +1 that end is on the right, -1 on the left."""
    if wheels:
        c.drawRRect(rr(x - 138, y - 34, 276, 16, 6), P("#1F2937"))
        for bx in (-96, 96):
            c.drawRRect(rr(x + bx - 42, y - 30, 84, 14, 6), P("#374151"))
            for wx in (-22, 22):
                c.drawCircle(x + bx + wx, y - 15, 15, P("#111827"))
                c.drawCircle(x + bx + wx, y - 15, 15, P("#9CA3AF", 1, stroke=3))
                c.drawLine(x + bx + wx, y - 15, x + bx + wx + 13 * math.cos(t * 9), y - 15 + 13 * math.sin(t * 9), P("#9CA3AF", 1, stroke=3))
    body = skia.Path()
    r = 26
    nose = 54
    xl, xr, yt, yb = x - 150, x + 150, y - 174, y - 34
    body.moveTo(xl + r, yt)
    if head == 1 or tail == 1:
        body.lineTo(xr - nose, yt)
        body.quadTo(xr, yt + 8, xr, yb - 30)
        body.lineTo(xr, yb)
    else:
        body.lineTo(xr, yt)
        body.lineTo(xr, yb)
    if head == -1 or tail == -1:
        body.lineTo(xl, yb)
        body.lineTo(xl, yb - 30)
        body.quadTo(xl, yt + 8, xl + nose, yt)
    else:
        body.lineTo(xl, yb)
        body.lineTo(xl, yt)
    body.close()
    c.drawPath(body, lin_paint(0, yt, 0, yb, ["#FFFFFF", "#E2E8F0", "#94A3B8"], [0.0, 0.55, 1.0]))
    c.save()
    c.clipPath(body, skia.ClipOp.kIntersect, True)
    c.drawRect(R(xl, y - 96, 300, 14), P(col))
    c.drawRect(R(xl, yb - 8, 300, 8), P("#475569"))
    win = mix("#FFE9B8", "#FCA5A5", 0.6 * hot)
    for wx, ww in ((-131, 34), (-26, 52), (97, 34)):
        if (head == -1 or tail == -1) and wx < -100:
            continue
        if (head == 1 or tail == 1) and wx > 80:
            continue
        c.drawRRect(rr(x + wx, y - 156, ww, 46, 8), P("#0F172A"))
        c.drawRRect(rr(x + wx + 3, y - 153, ww - 6, 40, 6), P(win, 0.92 * lit))
    for i in range(riders):                                                          # who is on board
        hx = x - 14 + (i % 3) * 16 if i < 3 else x + (-118 if i == 3 else 110)
        if (head == -1 or tail == -1) and i == 3:
            continue
        if (head == 1 or tail == 1) and i == 4:
            continue
        c.drawCircle(hx, y - 128, 9, P("#E8B48A"))
        c.drawArc(R(hx - 10, y - 142, 20, 16), 180, 180, True, P(PEOPLE[i % len(PEOPLE)]))
        if hot > 0.3:
            u = (t * 1.2 + i * 0.3) % 1.0
            c.drawOval(R(hx + 7, y - 132 + u * 12, 4, 6), P("#7DD3FC", 1 - u))
    for sd, flag in ((1, head == 1 or tail == 1), (-1, head == -1 or tail == -1)):   # the ends
        if not flag:
            continue
        ex = x + sd * 150
        ws = skia.Path()
        ws.moveTo(ex - sd * 50, yt + 10)
        ws.quadTo(ex - sd * 6, yt + 14, ex - sd * 4, yb - 62)
        ws.lineTo(ex - sd * 46, yb - 62)
        ws.close()
        c.drawPath(ws, P("#0F172A"))
        if empty_cab and head == sd:
            c.drawRRect(rr(ex - sd * 40 - 9, yb - 98, 18, 30, 5), P("#475569"))          # a seat with nobody in it
        is_head = head == sd
        c.drawCircle(ex - sd * 12, yb - 22, 7, P("#FFF7DA" if is_head else "#EF4444"))
    c.restore()
    for sd, flag in ((1, head == 1), (-1, head == -1)):
        if flag:
            add_glow(c, x + sd * 150, yb - 22, 70, "#FFF3C4", 0.8)
    for sd, flag in ((1, tail == 1), (-1, tail == -1)):
        if flag:
            add_glow(c, x + sd * 150, yb - 22, 50, "#EF4444", 0.8)
    for dx in DOORS:                                                                 # doors
        op = 24 * doors
        c.drawRRect(rr(x + dx - 28, y - 160, 56, 120, 6), P("#3B2F1E" if doors > 0 else "#64748B"))
        if doors > 0:
            c.drawRRect(rr(x + dx - 25, y - 157, 50, 114, 5), P("#FDE9C0", 0.95))
        for sd in (-1, 1):
            lx = x + dx + (sd * op if sd > 0 else -26 + sd * op)
            c.drawRRect(rr(lx, y - 158, 26, 116, 4), lin_paint(0, y - 158, 0, y - 42, ["#F8FAFC", "#CBD5E1"]))
            c.drawRRect(rr(lx + 5, y - 150, 16, 44, 4), P("#0F172A"))
            c.drawRRect(rr(lx + 7, y - 148, 12, 40, 3), P(win, 0.9 * lit))


def loco(c, x, y, t):
    """A small steam engine, chimney first, running to the right."""
    for wx in (-52, 0, 52):
        c.drawCircle(x + wx, y - 20, 20, P("#111827"))
        c.drawCircle(x + wx, y - 20, 20, P("#B45309", 1, stroke=4))
        c.drawLine(x + wx, y - 20, x + wx + 17 * math.cos(t * 8), y - 20 + 17 * math.sin(t * 8), P("#B45309", 1, stroke=4))
    c.drawRRect(rr(x - 86, y - 44, 172, 16, 6), P("#1F2937"))
    c.drawRRect(rr(x - 40, y - 104, 130, 62, 28), lin_paint(0, y - 104, 0, y - 42, ["#4B5563", "#1F2937"]))
    c.drawRRect(rr(x - 92, y - 140, 60, 98, 8), P("#7F1D1D"))
    c.drawRRect(rr(x - 82, y - 128, 40, 34, 6), P("#FDE9C0"))
    c.drawRect(R(x + 56, y - 150, 20, 50), P("#111827"))
    c.drawRRect(rr(x + 50, y - 158, 32, 12, 4), P("#111827"))
    c.drawCircle(x + 10, y - 106, 12, P("#D4A84B"))


def wagon(c, x, y, t):
    for wx in (-34, 34):
        c.drawCircle(x + wx, y - 14, 14, P("#111827"))
        c.drawCircle(x + wx, y - 14, 14, P("#9CA3AF", 1, stroke=3))
        c.drawLine(x + wx, y - 14, x + wx + 12 * math.cos(t * 6), y - 14 + 12 * math.sin(t * 6), P("#9CA3AF", 1, stroke=3))
    p = skia.Path()
    p.moveTo(x - 66, y - 84)
    p.lineTo(x + 66, y - 84)
    p.lineTo(x + 54, y - 26)
    p.lineTo(x - 54, y - 26)
    p.close()
    c.drawPath(p, lin_paint(0, y - 84, 0, y - 26, ["#A9744A", "#7C5A3C"]))
    for dx in (-30, 0, 30):
        c.drawLine(x + dx * 1.15, y - 84, x + dx, y - 26, P("#5B3A22", 0.8, stroke=3))
    c.drawRRect(rr(x - 70, y - 90, 140, 10, 4), P("#5B3A22"))


def fanbig(c, x, y, r, ang):
    c.drawCircle(x, y, r + 10, P("#1F2937"))
    c.drawCircle(x, y, r, P("#0B1220"))
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    for i in range(5):
        c.save()
        c.rotate(i * 72)
        c.drawOval(R(r * 0.12, -r * 0.2, r * 0.82, r * 0.4), P("#CBD5E1"))
        c.restore()
    c.drawCircle(0, 0, r * 0.2, P("#F59E0B"))
    c.restore()
    c.drawCircle(x, y, r, P("#94A3B8", 1, stroke=6))


def gust(c, x0, y0, x1, y1, t, col, n=6, a=1.0, spread=40, seed=0, w=6, speed=0.8):
    if a <= 0:
        return
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    for i in range(n):
        u = (t * speed + i / n + seed * 0.37) % 1.0
        off = math.sin(i * 12.9898 + seed) * spread
        px, py = x0 + dx * u + nx * off, y0 + dy * u + ny * off
        p = skia.Path()
        p.moveTo(px, py)
        p.quadTo(px + dx / ln * 22 + nx * 10, py + dy / ln * 22 + ny * 10, px + dx / ln * 46, py + dy / ln * 46)
        pr = P(col, 0.85 * a * math.sin(math.pi * u), stroke=w)
        pr.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPath(p, pr)


def chug(d=0.14, seed=0):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed + 20).standard_normal(n), 300, 2600)
    return sfx._norm(x * sfx._env(n, 0.01, d * 0.4), 0.7)


def rail_hum(d=1.6, f0=120, f1=260):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = np.linspace(f0, f1, n)
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 2.01) / sfx.SR)
    return sfx._norm(x * sfx._ar(n, d * 0.2, d * 0.4), 0.5)


def screech(d=0.9, seed=3):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 2300 - 500 * tt / d + 60 * np.sin(2 * np.pi * 13 * tt)
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * 0.6 + sfx._bp(sfx._rng(seed).standard_normal(n), 1800, 5200) * 0.4
    return sfx._norm(x * sfx._ar(n, 0.05, d * 0.5), 0.5)


def door_chime():
    n = int(0.5 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * 880 * tt) * (tt < 0.22) * np.exp(-tt * 6) + np.sin(2 * np.pi * 660 * tt) * (tt >= 0.22) * np.exp(-(tt - 0.22) * 6)
    return sfx._norm(x, 0.6)


# ====================================================================================== the episode
class Metro(EpisodeV2):
    BUILD_NO = 18
    FIRST_SET = "tunnel"
    CLEAR = "#0B1024"
    TITLE = {"en": "METRO", "ar_sa": "مترو"}
    EMPH = {"en": ["CONGRATS", "METRO", "TUNNEL", "WAGON", "SLOW", "STEAM", "SMOKE", "SMOKED", "ELECTRIC", "THIRD", "SHOES", "MOTORS", "FAST", "DARK",
                   "BEACONS", "RADIO", "COMPUTER", "GAP", "DRIVER", "CROWDED", "EDGE", "GLASS", "DOORS", "STOPS", "HOT", "STUFFY", "FANS", "SHAFTS",
                   "WALKWAY", "FOLLOW", "DAM", "MAP", "MIND", "ZERO", "DRIVERLESS", "YOURSELF", "WAITING", "TICKET"],
            "ar_sa": ["مبروك", "مترو", "نفق", "عربة", "بطيء", "البخار", "دخان", "مدخّنين", "كهربائي", "ثالثة", "وأحذية", "للمواطير", "سريع", "الظلام",
                      "إشارات", "وراديو", "وكمبيوتر", "أمان", "سواق", "الزحمة", "الحافة", "زجاج", "وأبوابه", "يوقف", "حار", "وكاتم", "مراوح", "وفتحات",
                      "وممشى", "تابعني", "سد", "خريطة", "للفجوة", "وصفر", "بيدك", "تنتظر", "تذكرة"]}
    KEYS = {"ar_sa": {
        ("hook", "DIG"): "حفرت", ("hook", "TUNNEL"): "نفق", ("hook", "PUSH"): "ودفّيت", ("hook", "WAGON"): "عربة", ("hook", "CONGRATS"): "مبروك",
        ("break1", "PUSHING"): "الدف", ("break1", "SLOW"): "بطيء", ("break1", "STEAM"): "البخار", ("break1", "SMOKE"): "دخان", ("break1", "FIRST"): "أول",
        ("break1", "RIDERS"): "والركاب", ("break1", "SMOKED"): "مدخّنين",
        ("fix1", "ELECTRIC"): "كهربائي", ("fix1", "THIRD"): "ثالثة", ("fix1", "RAIL"): "سكة", ("fix1", "POWER"): "الكهربا", ("fix1", "SHOES"): "وأحذية",
        ("fix1", "FEED"): "توصلها", ("fix1", "MOTORS"): "للمواطير",
        ("break2", "FAST"): "سريع", ("break2", "CATCHES"): "يلحق", ("break2", "ANOTHER"): "ثاني", ("break2", "DARK"): "الظلام",
        ("fix2", "BEACONS"): "إشارات", ("fix2", "RADIO"): "وراديو", ("fix2", "COMPUTER"): "وكمبيوتر", ("fix2", "KEEPS"): "يخلي", ("fix2", "GAP"): "مسافة",
        ("fix2", "DRIVER"): "سواق",
        ("break3", "CROWDED"): "الزحمة", ("break3", "SOMEBODY"): "واحد", ("break3", "CLOSE"): "قريب", ("break3", "EDGE"): "الحافة",
        ("fix3", "GLASS"): "زجاج", ("fix3", "WALL"): "جدار", ("fix3", "DOORS"): "وأبوابه", ("fix3", "OPEN"): "تفتح", ("fix3", "STOPS"): "وقف",
        ("fix3", "BEHIND"): "وراها",
        ("break4", "SAFE"): "آمن", ("break4", "STOPS"): "يوقف", ("break4", "BETWEEN"): "بين", ("break4", "HOT"): "حار", ("break4", "STUFFY"): "وكاتم",
        ("fix4", "FANS"): "مراوح", ("fix4", "SHAFTS"): "وفتحات", ("fix4", "STREET"): "للشارع", ("fix4", "WALKWAY"): "وممشى", ("fix4", "STATION"): "المحطة",
        ("cta", "TAP"): "تمرر", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "MAP"): "خريطة", ("reveal", "LINES"): "ملونة", ("reveal", "VOICE"): "وصوت", ("reveal", "MIND"): "انتبه", ("reveal", "GAP"): "للفجوة",
        ("stat", "ONE"): "نفق", ("stat", "TWO"): "دقيقتين", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "GUY"): "والرجال", ("tag", "DOORS"): "الباب", ("tag", "EVERY"): "كل", ("tag", "WAITING"): "تنتظر", ("tag", "FRIEND"): "وخويّه",
        ("tag", "TICKET"): "تذكرة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a dam"),
                   "stat": [("1", "TUNNEL"), ("2", "MINUTES"), ("0", "DRIVERS")],
                   "L": {"wagon": "YOUR METRO", "slow": "SLOW", "london": "LONDON, 1863", "third": "THIRD RAIL", "shoe": "METAL SHOE", "motor": "MOTOR",
                         "beacon": "BEACONS", "radio": "RADIO", "gap": "SAFE GAP", "nodriver": "NO DRIVER", "edge": "TOO CLOSE", "glass": "GLASS WALL",
                         "aligned": "DOORS LINED UP", "hot": "HOT AND STUFFY", "fan": "GIANT FAN", "shaft": "AIR SHAFT", "walk": "LIT WALKWAY",
                         "card": "TAP HERE", "mind": "MIND THE GAP", "wait": "EVERY TRAIN BEHIND: WAITING", "ticket": "STILL BUYING A TICKET"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: سد"),
                      "stat": [("1", "نفق"), ("2", "دقيقتين"), ("0", "سواقين")],
                      "L": {"wagon": "المترو حقك", "slow": "بطيء", "london": "لندن، 1863", "third": "سكة ثالثة", "shoe": "حذاء حديد", "motor": "ماطور",
                            "beacon": "إشارات", "radio": "راديو", "gap": "مسافة أمان", "nodriver": "بدون سواق", "edge": "قريب مرة", "glass": "جدار زجاج",
                            "aligned": "الأبواب متطابقة", "hot": "حار وكاتم", "fan": "مروحة عملاقة", "shaft": "فتحة هوا", "walk": "ممشى منوّر",
                            "card": "مرر هنا", "mind": "انتبه للفجوة", "wait": "كل القطارات وراه تنتظر", "ticket": "لسا يشتري تذكرة"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "dig": ("hook", "DIG", 0.12), "tunnel": ("hook", "TUNNEL", 0.22), "push": ("hook", "PUSH", 0.36), "wagon": ("hook", "WAGON", 0.46),
            "congrats": ("hook", "CONGRATS", 0.6),
            "pushing": ("break1", "PUSHING", 0.06), "slow": ("break1", "SLOW", 0.14), "steam": ("break1", "STEAM", 0.24), "smoke": ("break1", "SMOKE", 0.46),
            "first": ("break1", "FIRST", 0.54), "riders": ("break1", "RIDERS", 0.76), "smoked": ("break1", "SMOKED", 0.95),
            "electric": ("fix1", "ELECTRIC", 0.14), "third": ("fix1", "THIRD", 0.26), "rail": ("fix1", "RAIL", 0.3), "power": ("fix1", "POWER", 0.52),
            "shoes": ("fix1", "SHOES", 0.68), "feed": ("fix1", "FEED", 0.8), "motors": ("fix1", "MOTORS", 0.94),
            "fast": ("break2", "FAST", 0.16), "catches": ("break2", "CATCHES", 0.5), "another": ("break2", "ANOTHER", 0.68), "dark": ("break2", "DARK", 0.92),
            "beacons": ("fix2", "BEACONS", 0.1), "radio": ("fix2", "RADIO", 0.28), "computer": ("fix2", "COMPUTER", 0.52), "keeps": ("fix2", "KEEPS", 0.62),
            "gap": ("fix2", "GAP", 0.7), "driver": ("fix2", "DRIVER", 0.88),
            "crowded": ("break3", "CROWDED", 0.2), "somebody": ("break3", "SOMEBODY", 0.44), "close": ("break3", "CLOSE", 0.76), "edge": ("break3", "EDGE", 0.94),
            "glass": ("fix3", "GLASS", 0.2), "wall": ("fix3", "WALL", 0.26), "doors": ("fix3", "DOORS", 0.54), "open": ("fix3", "OPEN", 0.66),
            "stops": ("fix3", "STOPS", 0.84), "behind": ("fix3", "BEHIND", 0.92),
            "safe": ("break4", "SAFE", 0.12), "stops2": ("break4", "STOPS", 0.4), "between": ("break4", "BETWEEN", 0.46), "hot": ("break4", "HOT", 0.78),
            "stuffy": ("break4", "STUFFY", 0.92),
            "fans": ("fix4", "FANS", 0.16), "shafts": ("fix4", "SHAFTS", 0.28), "street": ("fix4", "STREET", 0.44), "walkway": ("fix4", "WALKWAY", 0.62),
            "station": ("fix4", "STATION", 0.94),
            "tap": ("cta", "TAP", 0.22), "follow": ("cta", "FOLLOW", 0.42),
            "map": ("reveal", "MAP", 0.2), "lines": ("reveal", "LINES", 0.42), "voice": ("reveal", "VOICE", 0.62), "mind": ("reveal", "MIND", 0.84),
            "gap2": ("reveal", "GAP", 0.95),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "TWO", 0.5), "s3": ("stat", "ZERO", 0.78),
            "cong2": ("closer", "CONGRATS", 0.16),
            "guy": ("tag", "GUY", 0.12), "doors2": ("tag", "DOORS", 0.26), "every": ("tag", "EVERY", 0.34), "waiting": ("tag", "WAITING", 0.6),
            "friend": ("tag", "FRIEND", 0.76), "ticket": ("tag", "TICKET", 0.95)})
        T["third0"] = min(T["third"], T["rail"]) - 0.1
        T["wall0"] = min(T["glass"], T["wall"]) - 0.15
        T["arrive"] = min(T["stops"], T["doors"]) + 0.0                # the train is in, behind the glass
        T["opened"] = max(T["behind"], T["open"]) + 0.15
        T["halt"] = min(T["stops2"], T["between"])
        T["friendcut"] = T["friend"] - 0.35
        self.cut(s("fix1") - 0.12, "tunnel", 1)
        self.cut(s("break2") - 0.1, "tunnel", -1)
        self.cut(s("fix2") - 0.12, "tunnel", 1)
        self.cut(s("break3") - 0.1, "platform", 1)
        self.cut(s("break4") - 0.12, "tunnel", -1)
        self.cut(s("fix4") - 0.12, "tunnel", 1)
        self.cut(s("cta") + 0.05, "platform", -1)
        self.cut(s("reveal") - 0.1, "map", 1)
        self.cut(T["s1"] - 0.35, "tunnel", 1)
        self.cut(s("closer") - 0.1, "platform", 1)
        self.cut(s("tag") - 0.2, "platform", -1)
        tc = Camera(-60, -100, 2.0)
        tc.key(0.05, -80, -92, 2.15, 1.6).key(s("break1") - 0.1, -40, -92, 2.1, 1.0).key(T["steam"] - 0.4, 0, -98, 1.9, 0.8)
        tc.key(T["riders"] - 0.5, 150, -86, 2.4, 0.8)
        tc.key(s("fix1") - 0.12, 0, -92, 2.0, 0.0).key(T["third0"] - 0.3, -96, -36, 3.6, 0.9)
        tc.key(s("break2") - 0.1, -200, -110, 1.5, 0.0).key(T["catches"] - 0.5, 320, -100, 1.6, 1.3)
        tc.key(s("fix2") - 0.12, 0, -130, 1.25, 0.0).key(T["driver"] - 0.5, -150, -92, 2.2, 0.7)
        tc.key(s("break4") - 0.12, 0, -92, 2.1, 0.0).key(T["hot"] - 0.4, 0, -100, 2.4, 0.8)
        tc.key(s("fix4") - 0.12, -120, -232, 1.2, 0.0).key(T["walkway"] - 0.5, 150, -150, 1.6, 0.8)
        tc.key(T["s1"] - 0.35, 0, -232, 1.12, 0.0)
        self.tcam = tc
        pc = Camera(0, -142, 1.9)
        pc.key(s("break3") - 0.1, 40, -150, 1.7, 0.0).key(T["somebody"] - 0.4, 110, -142, 1.9, 0.8)
        pc.key(s("fix3") - 0.12, 30, -150, 1.75, 0.0)
        pc.key(s("cta") + 0.05, -430, -135, 2.0, 0.0)
        pc.key(s("closer") - 0.1, 0, -150, 1.75, 0.0)
        pc.key(s("tag") - 0.2, -70, -142, 1.9, 0.0).key(T["friendcut"], 400, -135, 2.0, 0.5)
        self.pcam = pc
        self.spans = [(T["smoke"], T["motors"]), (T["catches"], T["driver"]), (T["close"], T["opened"]), (T["hot"], T["station"])]
        self.shakes = [(T["smoke"], 0.25, 6), (T["dark"], 0.45, 14), (T["close"], 0.3, 8), (T["arrive"], 0.2, 5), (T["hot"], 0.25, 6)]

    def phase(self, t):
        s, T = self.tl.s, self.T
        for name, t0 in (("tag", s("tag") - 0.2), ("closer", s("closer") - 0.1), ("stat", T["s1"] - 0.35), ("cta", s("cta") + 0.05), ("air", s("fix4") - 0.12),
                         ("stuck", s("break4") - 0.12), ("psd", s("fix3") - 0.12), ("edge", s("break3") - 0.1), ("cbtc", s("fix2") - 0.12),
                         ("chase", s("break2") - 0.1), ("power", s("fix1") - 0.12), ("steam", s("break1") - 0.1), ("dig", 0.0)):
            if t >= t0:
                return name

    # ------------------------------------------------------------------ set: the tunnel
    def earth(self, c, t, x0=-2600, x1=2600, dug=None):
        """Street on top, soil, and the bore through it (dug: how far right the bore reaches)."""
        skyline_night(c, x0, x1, base_y=STREET, seed=7, hmin=120, hmax=420, t=t)
        box(c, x0, STREET, x1 - x0, 16, "#55607F")
        vrect(c, x0, STREET + 16, x1 - x0, 1500, ["#2A3152", "#1B2140", "#11162B"], [0.0, 0.3, 1.0])
        rng = random.Random(12)
        for _ in range(90):                                                          # things in the ground
            gx, gy = rng.uniform(x0, x1), rng.uniform(STREET + 40, ROOF - 24)
            c.drawOval(R(gx, gy, rng.uniform(14, 44), rng.uniform(8, 20)), P("#000000" if rng.random() < 0.6 else "#5C6B96", 0.18))
        for px in range(int(x0), int(x1), 520):
            c.drawLine(px, STREET + 70, px + 380, STREET + 70, P("#3B82F6", 0.35, stroke=10))
            c.drawLine(px + 200, STREET + 110, px + 520, STREET + 110, P("#F59E0B", 0.3, stroke=7))
        xe = x1 if dug is None else dug
        if xe > x0:
            vrect(c, x0, ROOF, xe - x0, 290, ["#161D36", "#1E2747", "#141A30"], [0.0, 0.6, 1.0])
            for rx in range(int(x0), int(xe), 130):                                  # lining rings and lamps
                c.drawRect(R(rx, ROOF, 5, 256), P("#000000", 0.22))
            for lx in range(int(x0) + 90, int(xe), 260):
                c.drawRRect(rr(lx - 22, ROOF + 4, 44, 9, 4), P("#FFF3C4"))
                add_glow(c, lx, ROOF + 30, 150, "#FFE9B8", 0.16)
            c.drawRect(R(x0, 6, xe - x0, 34), P("#0C1024"))
            for sx in range(int(x0), int(xe), 44):
                c.drawRect(R(sx, 4, 22, 9), P("#3A2A1D"))
            c.drawRect(R(x0, -3, xe - x0, 7), lin_paint(0, -3, 0, 4, ["#E5E9F2", "#64748B"]))

    def third_rail(self, c, t, k=1.0, live=0.0):
        if k <= 0:
            return
        x0, x1 = -2600, lerp(-2600, 2600, k)
        for sx in range(-2600, int(x1), 96):
            c.drawRect(R(sx, 14, 10, 14), P("#1F2937"))
        c.drawRect(R(x0, 8, x1 - x0, 9), P("#F59E0B"))
        c.drawRect(R(x0, 8, x1 - x0, 3), P("#FDE68A"))
        if live > 0:
            for i in range(14):
                u = (t * 0.5 + i / 14) % 1.0
                bx = lerp(-700, 700, u)
                z = skia.Path()
                z.moveTo(bx, 0)
                z.lineTo(bx + 7, 9)
                z.lineTo(bx + 2, 9)
                z.lineTo(bx + 9, 20)
                c.drawPath(z, P("#FDE047", live, stroke=3))

    def draw_tunnel(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.tcam.at(t)
        ph = self.phase(t)
        scroll = 0.0
        if ph == "cbtc":
            scroll = 260 * (t - s("fix2"))
        if ph == "stat":
            scroll = 0.0
        cam = (cam[0] + math.sin(t * 0.6) * 2, cam[1], cam[2])
        v2.sky(c, W, H, 0.3, horizon_y=H * 1.2)
        v2.stars(c, W, H, t, 0.6)
        self.view(c, cam)
        c.save()
        c.translate(-(scroll % 520), 0)
        dug = lerp(-420, 900, e_out(prog(t, 0.0, T["tunnel"] + 0.2))) if ph == "dig" else None
        self.earth(c, t, dug=dug)
        c.restore()
        if ph == "dig":
            if dug < 880:
                v2.debris(c, dug, -110, t, t - (t % 0.12), 0.4, n=6, speed=330, seed=int(t * 8), gravity=900, cols=("#5C6B96", "#3A4466", "#8E96AA"), cone=(120, 240), size=(6, 18))
            wx = lerp(-440, 10, e_out(prog(t, 0.15, T["congrats"] + 1.2)))
            self.riders(c, t, wx, 0.0)
            wagon(c, wx, 0, wx * 0.02)
            for i, dx in enumerate((-150, -104)):
                engineer(c, wx + dx, 4, 112, SHIRTS[i], t * 1.6 + i, "carry", face=1)
        elif ph == "steam":
            steam = t >= T["steam"] - 0.2
            wx = lerp(0, 40, prog(t, s("break1"), T["steam"])) + (lerp(0, 190, e_io(prog(t, T["steam"], T["riders"] - 0.2))) if steam else 0)
            soot = prog(t, T["smoke"], T["riders"])
            self.riders(c, t, wx, soot, cough=t >= T["riders"] - 0.2)
            wagon(c, wx, 0, wx * 0.03)
            if not steam:
                for i, dx in enumerate((-150, -104)):
                    engineer(c, wx + dx + math.sin(t * 5 + i) * 2, 4, 112, SHIRTS[i], t * 0.7 + i, "duck" if t >= T["slow"] else "carry", face=1)
                    u = (t * 1.3 + i * 0.4) % 1.0
                    c.drawOval(R(wx + dx + 16, -112 + u * 26, 6, 9), P("#7DD3FC", 1 - u))
            else:
                lx = wx + 190 - 520 * (1 - e_out(prog(t, T["steam"] - 0.2, T["steam"] + 0.3))) if t < T["steam"] + 0.3 else wx + 190
                loco(c, lx - 380 if False else wx - 176, 0, t * 2)
                v2.smoke(c, wx - 110, -160, t, T["steam"] - 0.1, None, rate=22, life=3.0, spread=(-120, 60), rise=-26, size=(24, 110), col="#3B4252",
                         lit="#6B7280", lit_until=0.3, seed=3, a=0.9)
                hz = prog(t, T["steam"], T["smoke"] + 0.6)
                c.drawRect(R(-1200, ROOF, 2400, 250), P("#111827", 0.42 * hz))
        elif ph == "power":
            tk = prog(t, T["third0"], T["third0"] + 0.6)
            go = e_in(prog(t, T["motors"] + 0.2, T["motors"] + 1.4))
            live = prog(t, T["power"] - 0.3, T["power"])
            self.third_rail(c, t, tk, live)
            cx_ = go * 900
            car(c, cx_, 0, t * (0 if go <= 0 else 3), head=1, tail=-1, riders=3)
            if tk > 0.5:                                                             # the shoe, the cable, the motor
                sk = e_back(prog(t, T["shoes"] - 0.2, T["shoes"] + 0.1))
                bx = cx_ - 96
                c.drawRRect(rr(bx - 9 * sk, -12, 18 * sk, 20 * sk, 3), P("#E5E9F2"))
                c.drawRRect(rr(bx - 16 * sk, 2, 32 * sk, 7 * sk, 3), P("#CBD5E1"))
                fed = prog(t, T["feed"] - 0.2, T["motors"])
                if sk > 0.5 and live > 0:
                    sparks_shower(c, bx + 14, 6, t, t - (t % 0.2), 0.3, n=5, speed=160, seed=int(t * 5), cone=(200, 340))
                if fed > 0:
                    c.drawLine(bx, -10, bx, -22, P("#FDE047", fed, stroke=4))
                    add_glow(c, bx, -24, 34, "#FDE047", 0.8 * fed * (0.7 + 0.3 * math.sin(t * 20)))
                    c.drawRRect(rr(bx - 16, -29, 32, 12, 5), P("#FDE047", 0.9 * fed))
        elif ph == "chase":
            ax = self.chase_x(t)
            dk = prog(t, T["catches"] - 0.6, T["catches"])
            car(c, 570, 0, 0, tail=-1, riders=4, lit=0.35)
            car(c, 870, 0, 0, riders=4, lit=0.35)
            car(c, ax - 300, 0, t * 6, riders=4)
            car(c, ax, 0, t * 6, head=1, riders=3)
            c.drawRect(R(-2400, ROOF, 4800, 290), P("#05070F", 0.55 * dk))                 # the lights go out
            light_cone(c, ax + 150, -56, 2, 330, 13, "#FFF3C4", 0.55)
            for ly in (-56,):
                add_glow(c, 424, ly, 70, "#EF4444", 0.95)
                c.drawCircle(432, ly, 8, P("#FF6B6B"))
            if T["another"] <= t < T["dark"] + 0.15:
                sparks_shower(c, ax + 60, -4, t, t - (t % 0.12), 0.3, n=7, speed=260, seed=int(t * 9), cone=(180, 260))
        elif ph == "cbtc":
            wob = 46 * math.sin(max(0.0, t - T["keeps"]) * 2.6) * prog(t, T["keeps"] - 0.2, T["keeps"] + 0.3)
            bx_, ax = 250 + wob, -250 + wob * 0.92 * prog(t, T["keeps"], T["keeps"] + 0.6)
            for i in range(-3, 4):                                                   # beacons between the rails
                kx = i * 260 - (scroll % 260)
                bk = e_back(prog(t, T["beacons"] - 0.2 + (i + 3) * 0.05, T["beacons"] + 0.1 + (i + 3) * 0.05))
                near = min(abs(kx - ax), abs(kx - bx_)) < 150
                c.drawRRect(rr(kx - 20 * bk, 8, 40 * bk, 12, 4), P("#FACC15" if near else "#7C6A16"))
                if near and bk > 0:
                    add_glow(c, kx, 10, 60, "#FACC15", 0.6)
            for tx_, hd in ((ax, 1), (bx_, 1)):
                car(c, tx_, 0, t * 6, riders=3, head=1, tail=-1, empty_cab=True)
                rk = prog(t, T["radio"] - 0.2, T["radio"] + 0.2)
                if rk > 0:
                    c.drawLine(tx_, -174, tx_, -204, P("#E5E9F2", rk, stroke=4))
                    for j in range(3):
                        u = (t * 1.3 + j / 3) % 1.0
                        c.drawArc(R(tx_ - 16 - 44 * u, -220 - 44 * u, 32 + 88 * u, 32 + 88 * u), 215, 110, False, P("#7DD3FC", 0.9 * rk * (1 - u), stroke=4))
            gk = prog(t, T["gap"] - 0.4, T["gap"] - 0.1)
            if gk > 0:
                gx0, gx1 = ax + 150, bx_ - 150
                c.drawLine(gx0, -90, lerp(gx0, gx1, gk), -90, P(GOOD, 1, stroke=6))
                for gx in (gx0, gx1):
                    c.drawLine(gx, -112, gx, -68, P(GOOD, gk, stroke=6))
            self.ui["gapx"] = (ax + bx_) / 2
            self.ui["trainx"] = ax
        elif ph == "stuck":
            hotk = prog(t, T["hot"] - 0.6, T["stuffy"])
            jx = lerp(-240, 0, e_out(prog(t, s("break4") - 0.1, T["halt"])))
            car(c, jx - 300, 0, 0 if t >= T["halt"] else t * 5, riders=4, hot=hotk)
            car(c, jx, 0, 0 if t >= T["halt"] else t * 5, riders=5, hot=hotk)
            car(c, jx + 300, 0, 0 if t >= T["halt"] else t * 5, riders=3, head=1, hot=hotk, empty_cab=True)
            if hotk > 0:
                c.drawRect(R(-2000, ROOF, 4000, 290), P("#F97316", 0.12 * hotk))
                for i in range(7):
                    u = (t * 0.5 + i / 7) % 1.0
                    gust(c, -360 + i * 120, -176, -360 + i * 120, -240, t, "#FB923C", n=2, a=hotk * 0.8, spread=10, seed=i, w=5, speed=0.5)
        elif ph == "air":
            self.air(c, t)
        elif ph == "stat":
            for i in range(2):                                                       # one every two minutes
                u = ((t - T["s1"]) * 0.36 + i / 2 + 0.2) % 1.0
                tx_ = lerp(-1700, 1700, u)
                car(c, tx_ - 300, 0, t * 7, riders=4, tail=-1)
                car(c, tx_, 0, t * 7, riders=5)
                car(c, tx_ + 300, 0, t * 7, riders=3, head=1, empty_cab=True)
        c.restore()
        self.ui["cam"] = cam

    def chase_x(self, t):
        T, s = self.T, self.tl.s
        return lerp(-900, 250, e_out(prog(t, s("break2"), T["dark"] + 0.1)))

    def riders(self, c, t, wx, soot, cough=False):
        engineer(c, wx, -40, 104, SHIRTS[2], t, "cheer" if (t >= self.T["congrats"] - 0.1 and soot <= 0) else "duck" if cough else "look", soot=soot, face=1)
        if cough:
            for j in range(3):
                u = (t * 1.6 + j / 3) % 1.0
                puff(c, wx + 30 + u * 40, -120 - u * 24, 8 + 14 * u, "#4B5563", 0.8 * (1 - u), k=j)

    def air(self, c, t):
        """Fix 4: a giant fan, a shaft up to the street, a lit walkway."""
        T, s = self.T, self.tl.s
        fk = e_back(prog(t, T["fans"] - 0.25, T["fans"] + 0.1))
        sk = prog(t, T["shafts"] - 0.2, T["street"])
        wk = prog(t, T["walkway"] - 0.3, T["walkway"] + 0.4)
        # the shaft
        if sk > 0:
            top = lerp(ROOF, STREET, sk)
            c.drawRect(R(236, top, 68, ROOF - top + 6), P("#161D36"))
            c.drawRect(R(230, top, 6, ROOF - top), P("#55607F"))
            c.drawRect(R(304, top, 6, ROOF - top), P("#55607F"))
            if sk >= 1:
                for gx in range(232, 310, 13):
                    c.drawRect(R(gx, STREET - 4, 7, 10), P("#CBD5E1"))
                gust(c, 270, ROOF + 10, 270, STREET - 150, t, "#FB923C", n=8, a=0.9, spread=20, seed=2, w=7, speed=0.7)
                hat = bump(t, T["street"] + 0.1, T["street"] + 1.3)
                person(c, 330, STREET, 96, "#F472B6", t, "duck" if hat > 0 else "stand", face=-1, hair="#2B2530", pants="#334155")
                hard_hat(c, 320 - 60 * hat, STREET - 110 - 170 * hat, rot=-200 * hat, s=0.8) if hat > 0 else None
        # the stopped train, cooling off
        cool = prog(t, T["fans"], T["street"])
        car(c, -90, 0, 0, riders=4, tail=-1, hot=1 - cool)
        car(c, 210, 0, 0, riders=4, head=1, hot=1 - cool, empty_cab=True, doors=prog(t, T["walkway"] + 0.1, T["walkway"] + 0.5))
        if fk > 0:
            c.drawRRect(rr(-560, ROOF - 10, 190, 270, 16), P("#161D36"))
            fanbig(c, -466, -125, 84 * fk, t * 520)
            gust(c, -380, -150, 500, -210, t, "#7DD3FC", n=10, a=fk, spread=34, seed=1, w=7, speed=0.9)
            gust(c, -380, -60, 480, -40, t, "#7DD3FC", n=6, a=fk * 0.8, spread=14, seed=4, w=6, speed=1.0)
        if wk > 0:                                                                   # the walkway and its lights
            x1 = lerp(330, 1200, wk)
            c.drawRect(R(330, -46, x1 - 330, 10), P("#CBD5E1"))
            for lx in range(350, int(x1), 70):
                c.drawCircle(lx, -62, 5, P("#FDE68A"))
                add_glow(c, lx, -62, 34, "#FDE68A", 0.6)
            for i in range(3):
                u = prog(t, T["walkway"] + 0.4 + i * 0.25, T["station"] + 0.8 + i * 0.25)
                if u > 0:
                    engineer(c, lerp(330, 760, u), -46, 92, SHIRTS[i], t * 1.6 + i, "walk", face=1)
            c.drawRRect(rr(620, -214, 150, 50, 10), P("#16A34A", clamp(wk * 2 - 1)))
            c.drawLine(650, -189, 720, -189, P("#FFFFFF", clamp(wk * 2 - 1), stroke=7))
            for dyy in (-14, 14):
                c.drawLine(720, -189, 700, -189 + dyy, P("#FFFFFF", clamp(wk * 2 - 1), stroke=7))

    # ------------------------------------------------------------------ set: the platform
    def draw_platform(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.pcam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 2, cam[1], cam[2])
        ph = self.phase(t)
        v2.sky(c, W, H, 0.3, horizon_y=H * 1.2)
        self.view(c, cam)
        skyline_night(c, -1600, 1600, base_y=-560, seed=9, hmin=120, hmax=380, t=t)
        box(c, -1600, -560, 3200, 16, "#55607F")
        vrect(c, -1600, -544, 3200, 1500, ["#2A3152", "#1B2140", "#11162B"], [0.0, 0.3, 1.0])
        # the station hall
        vrect(c, -1100, -360, 2200, 316, ["#55668C", "#44547A", "#364466"], [0.0, 0.5, 1.0])
        for tx_ in range(-1100, 1100, 60):
            c.drawRect(R(tx_, -360, 2, 316), P("#000000", 0.10))
        c.drawRect(R(-1100, -250, 2200, 22), P(TEAL))
        for sx in (-520, 0, 520):                                                    # station name boards
            c.drawRRect(rr(sx - 90, -330, 180, 54, 10), P("#0B1220"))
            c.drawCircle(sx - 56, -303, 16, P(TEAL, 1, stroke=7))
            c.drawRRect(rr(sx - 30, -312, 100, 8, 4), P("#F8FAFC"))
            c.drawRRect(rr(sx - 30, -298, 70, 6, 3), P("#94A3B8"))
        for lx in range(-1000, 1100, 220):
            c.drawRRect(rr(lx - 60, -358, 120, 10, 5), P("#FFF7DA"))
            add_glow(c, lx, -330, 160, "#FFE9B8", 0.10)
        c.drawRect(R(-1100, -70, 2200, 30), P("#0C1024"))                              # the track pit
        # trains
        self.station_trains(c, t, ph)
        c.drawRect(R(-1100, -212, 2200, 172), P("#1E2A4D", 0.34))                      # the train sits back from us, in the shade
        # the glass wall
        gw = prog(t, T["wall0"], T["wall0"] + 0.7) if ph == "psd" else 1.0 if ph in ("cta", "closer", "tag") else 0.0
        if gw > 0:
            self.glass_wall(c, t, gw, ph)
        # the platform floor
        vrect(c, -1100, -44, 2200, 60, ["#7C86A6", "#55607F"], [0.0, 1.0])
        c.drawRect(R(-1100, -44, 2200, 4), P("#F8FAFC"))
        c.drawRect(R(-1100, -32, 2200, 8), P("#FACC15"))
        for dx in range(-1100, 1100, 26):
            c.drawRect(R(dx, -32, 3, 8), P("#A16207", 0.5))
        c.drawRect(R(-1100, 16, 2200, 900), P("#161B33"))
        self.station_people(c, t, ph)
        c.restore()
        self.ui["cam"] = cam

    def train_x(self, t, ph):
        """Where the middle car of the train in the station is (None: no train)."""
        T, s = self.T, self.tl.s
        if ph == "edge":
            return lerp(-2400, -1500, prog(t, T["close"] - 0.6, T["edge"] + 0.5))
        if ph == "psd":
            return lerp(-1700, 0, e_out(prog(t, T["arrive"] - 1.5, T["arrive"])))
        if ph == "closer":
            return lerp(-1500, 0, e_out(prog(t, s("closer") - 0.1, T["cong2"] + 0.2)))
        if ph == "tag":
            return 0.0
        return None

    def door_open(self, t, ph):
        T, s = self.T, self.tl.s
        if ph == "psd":
            return e_io(prog(t, T["opened"], T["opened"] + 0.45))
        if ph == "closer":
            return e_io(prog(t, T["cong2"] + 0.3, T["cong2"] + 0.8))
        if ph == "tag":
            return 1.0
        return 0.0

    def station_trains(self, c, t, ph):
        tx_ = self.train_x(t, ph)
        if tx_ is None:
            return
        op = self.door_open(t, ph)
        moving = abs(tx_) > 2
        for k in (-2, -1, 0, 1):
            car(c, tx_ + k * 300, -10, t * 6 if moving else 0, doors=op, head=1 if k == 1 else 0, tail=-1 if k == -2 else 0, riders=4 if k != 1 else 3,
                wheels=False, empty_cab=True)
        if ph == "edge":
            light_cone(c, tx_ + 450, -66, 3, 900, 9, "#FFF3C4", 0.5)

    def glass_wall(self, c, t, k, ph):
        op = self.door_open(t, ph)
        aligned = ph in ("psd",) and t >= self.T["arrive"] and op < 1
        for px in range(-1050, 1050, 150):
            kk = e_out(clamp(k * 3 - (px + 1050) / 2100 * 2))
            if kk <= 0:
                continue
            h = 196 * kk
            is_door = any(abs(((px + 75) % 300) - (150 + d)) < 40 for d in DOORS)
            c.drawRect(R(px, -44 - h, 150, h), P("#BAE6FD", 0.09))
            c.drawRect(R(px, -44 - h, 5, h), P("#94A3B8"))
            c.drawLine(px + 30, -44 - h + 12, px + 70, -52, P("#FFFFFF", 0.10, stroke=14))
        c.drawRect(R(-1050, -44 - 196 * min(1.0, k * 1.2), 2100, 8), P("#94A3B8", clamp(k * 2)))
        if k >= 1:
            for cx_ in (-600, -300, 0, 300, 600):                                    # platform doors, one pair per train door
                for d in DOORS:
                    x = cx_ + d
                    for sd in (-1, 1):
                        lx = x + (sd * 26 * op if sd > 0 else -28 + sd * 26 * op)
                        c.drawRRect(rr(lx, -236, 28, 192, 3), P("#E2E8F0", 0.16))
                        c.drawRRect(rr(lx, -236, 28, 192, 3), P("#F8FAFC", 0.9, stroke=3))
                    c.drawRRect(rr(x - 34, -248, 68, 12, 4), P(GOOD if (aligned or op > 0) else "#F59E0B"))

    def station_people(self, c, t, ph):
        T, s = self.T, self.tl.s
        b = lambda i: math.sin(t * 1.4 + i * 1.9) * 2
        if ph == "edge":
            scared = t >= T["close"]
            for i, px in enumerate((-250, -160, -60, 30, 240, 330, 410)):
                person(c, px + b(i), -4, 118 + (i % 3) * 8, PEOPLE[i], t + i, "duck" if scared and i % 2 == 0 else "look", face=-1 if i % 3 else 1, hair="#2B2530", pants="#334155")
            gx = 135
            step = e_io(prog(t, T["somebody"] - 0.3, T["somebody"] + 0.4))
            person(c, gx, lerp(-4, -42, step), 128, "#EF4444", t, "look", face=-1, hat="cap", pants="#111827")
            c.drawRRect(rr(gx - 30, lerp(-4, -42, step) - 86, 12, 20, 3), P("#0B1220"))        # his phone
            c.drawRRect(rr(gx - 28, lerp(-4, -42, step) - 84, 8, 14, 2), P("#7DD3FC"))
        elif ph == "psd":
            board = prog(t, self.T["opened"] + 0.3, self.T["opened"] + 1.3)
            for i, px in enumerate((-250, -160, -60, 30, 240, 330, 410)):
                tgt = min((cx_ + d for cx_ in (-300, 0, 300) for d in DOORS), key=lambda v: abs(v - px))
                x = lerp(px, tgt, e_io(board))
                if board < 0.98:
                    person(c, x + b(i), lerp(-4, -40, board), (118 + (i % 3) * 8) * (1 - 0.25 * board), PEOPLE[i], t * (1 + board) + i, "walk" if board > 0 else "look", face=1,
                           hair="#2B2530", pants="#334155")
            if board < 0.98:
                gx = lerp(135, 78, e_io(board))
                person(c, gx, lerp(-34, -40, board), 128 * (1 - 0.25 * board), "#EF4444", t, "shrug" if board <= 0 else "walk", face=-1, hat="cap", pants="#111827")
        elif ph == "cta":
            gx = -430                                                                # the fare gate
            for px in (gx - 70, gx + 70):
                box(c, px - 18, -112, 36, 108, "#475569", r=8)
            c.drawRRect(rr(gx - 52, -84, 104, 12, 4), P("#EF4444"))
            c.drawCircle(gx + 70, -124, 22, P("#0B1220"))
            c.drawCircle(gx + 70, -124, 16, P(GOOD, 0.9, stroke=5))
            engineer(c, gx - 150, -4, 124, SHIRTS[0], t, "point", face=1)
            hx = lerp(gx - 96, gx + 30, e_out(prog(t, s("cta") + 0.2, T["tap"] + 0.2)))
            c.drawRRect(rr(hx - 4, -170, 46, 30, 6), P("#F8FAFC"))
            c.drawRRect(rr(hx, -164, 20, 8, 3), P(TEAL))
            self.crew(c, t, "look", xs=(-640, -596), y=-4, face=1, h=116) if False else None
        elif ph == "closer":
            self.crew(c, t, "cheer", xs=(-150, -104, -58), y=-4, face=1, h=120)
            if t >= T["cong2"]:
                hats_in_the_air(c, (-150, -104, -58), -160, t, T["cong2"])
            for i, px in enumerate((150, 240, 330)):
                person(c, px + b(i), -4, 120, PEOPLE[i + 2], t + i, "cheer" if t >= T["cong2"] + 0.4 else "look", face=-1, hair="#2B2530", pants="#334155")
        elif ph == "tag":
            dx = DOORS[0]
            person(c, dx, -38, 124, "#EF4444", t, "cheer", face=1, hat="cap", pants="#111827")        # arms out, holding both doors
            for i, px in enumerate((-300, 150, 250)):
                person(c, px + b(i), -4, 120, PEOPLE[i + 1], t + i, "shrug" if t >= T["every"] else "look", face=1 if px < dx else -1, hair="#2B2530", pants="#334155")
            # his friend, at the ticket machine
            box(c, 470, -190, 100, 186, "#1D4ED8", r=10)
            c.drawRRect(rr(482, -176, 76, 50, 6), P("#0B1220"))
            c.drawRRect(rr(488, -170, 64, 38, 4), P("#7DD3FC", 0.8))
            for i in range(6):
                c.drawRRect(rr(486 + (i % 3) * 24, -116 + (i // 3) * 22, 18, 16, 3), P("#CBD5E1"))
            c.drawRRect(rr(496, -60, 48, 8, 3), P("#0B1220"))
            person(c, 400, -4, 124, "#FBBF24", t * 0.5, "point", face=1, hair="#2B2530", pants="#334155")
            for i in range(3):
                u = (t * 0.6 + i / 3) % 1.0
                c.drawCircle(lerp(430, 505, u), -96 - 40 * math.sin(math.pi * u), 6, P("#FACC15", 0.9 if u < 0.95 else 0.0))

    # ------------------------------------------------------------------ set: the map
    def draw_map(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#141A30", "#1B2440", "#101528"]))
        c.drawRRect(rr(60, 380, 960, 800, 40), P("#0F172A"))
        c.drawRRect(rr(60, 380, 960, 800, 40), P("#CBD5E1", 1, stroke=5))
        for gx in range(140, 1000, 80):
            c.drawLine(gx, 400, gx, 1160, P("#FFFFFF", 0.04, stroke=2))
        for gy in range(440, 1160, 80):
            c.drawLine(80, gy, 1000, gy, P("#FFFFFF", 0.04, stroke=2))
        lines = (("#EF4444", [(130, 560), (420, 560), (640, 780), (960, 780)]),
                 ("#2563EB", [(170, 1090), (420, 840), (420, 560), (640, 460), (940, 460)]),
                 ("#16A34A", [(130, 900), (540, 900), (760, 680), (760, 440)]),
                 ("#F59E0B", [(260, 440), (260, 1100)]),
                 ("#9333EA", [(540, 1120), (540, 900), (900, 1010), (960, 1010)]))
        k = prog(t, T["map"] - 0.3, T["lines"] + 0.5)
        for i, (col, pts) in enumerate(lines):
            kk = clamp(k * 1.8 - i * 0.18)
            if kk <= 0:
                continue
            seg = [math.dist(pts[j], pts[j + 1]) for j in range(len(pts) - 1)]
            total = sum(seg) * kk
            p = skia.Path()
            p.moveTo(*pts[0])
            acc = 0.0
            for j, sl in enumerate(seg):
                if acc + sl <= total:
                    p.lineTo(*pts[j + 1])
                    acc += sl
                else:
                    u = (total - acc) / sl if sl else 0
                    p.lineTo(lerp(pts[j][0], pts[j + 1][0], u), lerp(pts[j][1], pts[j + 1][1], u))
                    break
            pr = P(col, 1, stroke=18)
            pr.setStrokeCap(skia.Paint.kRound_Cap)
            pr.setStrokeJoin(skia.Paint.kRound_Join)
            c.drawPath(p, pr)
            if kk >= 1:
                for j in range(len(pts) - 1):
                    n = max(1, int(seg[j] // 130))
                    for m in range(n + 1):
                        u = m / n
                        sx, sy = lerp(pts[j][0], pts[j + 1][0], u), lerp(pts[j][1], pts[j + 1][1], u)
                        c.drawCircle(sx, sy, 10, P("#0F172A"))
                        c.drawCircle(sx, sy, 10, P("#F8FAFC", 1, stroke=4))
        if k >= 1:
            for ix, iy in ((420, 560), (260, 560), (260, 900), (540, 900), (760, 680)):
                c.drawCircle(ix, iy, 20, P("#0F172A"))
                c.drawCircle(ix, iy, 20, P("#F8FAFC", 1, stroke=6))
        vk = e_back(prog(t, T["voice"] - 0.2, T["voice"] + 0.1))
        if vk > 0:                                                                   # the calm voice
            sx, sy = 200, 290
            c.save()
            c.translate(sx, sy)
            c.scale(vk, vk)
            sp = skia.Path()
            sp.moveTo(-34, -16)
            sp.lineTo(-12, -16)
            sp.lineTo(16, -40)
            sp.lineTo(16, 40)
            sp.lineTo(-12, 16)
            sp.lineTo(-34, 16)
            sp.close()
            c.drawPath(sp, P("#E5E9F2"))
            for j in range(3):
                u = (t * 1.2 + j / 3) % 1.0
                c.drawArc(R(10 - 50 * u, -30 - 50 * u, 60 + 100 * u, 60 + 100 * u), -40, 80, False, P("#7DD3FC", 0.9 * (1 - u), stroke=6))
            c.restore()
        self.ui["cam"] = (0, 0, 1)

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -100, 2.0)), x, y)

    def ui_tunnel(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        ph = self.phase(tw)
        if ph == "dig":
            x0, y0 = self.at(lerp(-440, 10, e_out(prog(tw, 0.15, T["congrats"] + 1.2))), -150)
            self.label(x0, y0, x0 + 120, y0 - 190, "wagon", T["wagon"], s("break1") - 0.3, HILITE)
        elif ph == "steam":
            self.chip(540, 420, "slow", T["slow"] - 0.2, T["steam"] - 0.3, accent=WARN, size=46)
            self.chip(540, 420, "london", T["first"] - 0.1, T["riders"] - 0.3, accent=HILITE, size=46)
            self.badge("alert", T["smoke"], s("fix1") - 0.2, x=880, y=560)
            self.red(T["smoke"], 1.8)
        elif ph == "power":
            x0, y0 = self.at(40, 12)
            self.label(x0, y0, x0 + 170, y0 - 280, "third", T["third0"] + 0.3, T["shoes"] - 0.3, "#F59E0B")
            x1, y1 = self.at(-96, 2)
            self.label(x1, y1, x1 - 170, y1 - 230, "shoe", T["shoes"], T["feed"] - 0.1, "#E5E9F2")
            x2, y2 = self.at(-96, -30)
            self.label(x2, y2, x2 + 60, y2 - 330, "motor", T["feed"] + 0.1, s("break2") - 0.3, "#FDE047")
            self.badge("check", T["motors"], s("break2") - 0.15, x=880, y=420)
        elif ph == "chase":
            self.badge("alert", T["catches"], s("fix2") - 0.2, x=880, y=420)
            self.red(T["catches"], 2.0)
        elif ph == "cbtc":
            x0, y0 = self.at(0, 14)
            self.label(x0, y0, x0 - 170, y0 - 420, "beacon", T["beacons"] + 0.2, T["radio"] - 0.15, "#FACC15")
            ax, ay = self.at(self.ui.get("trainx", -330), -230)
            self.label(ax, ay, ax - 40, ay - 190, "radio", T["radio"] + 0.1, T["computer"] - 0.15, "#7DD3FC")
            ck = self.span(T["computer"] - 0.2, T["driver"] - 0.55)                    # the computer that watches them
            if ck > 0:
                kx, ky = 540, 430
                c.drawRRect(rr(kx - 150 * ck, ky - 70, 300 * ck, 140, 18), P("#0B1220", 0.9))
                c.drawRRect(rr(kx - 150 * ck, ky - 70, 300 * ck, 140, 18), P("#7DD3FC", 1, stroke=4))
                if ck >= 1:
                    c.drawLine(kx - 120, ky + 26, kx + 120, ky + 26, P("#94A3B8", 1, stroke=5))
                    w_ = math.sin(tw * 2.6) * 8
                    for dx in (-56 + w_, 56 + w_):
                        c.drawRRect(rr(kx + dx - 30, ky + 8, 60, 22, 7), P(TEAL))
                    c.drawLine(kx - 26 + w_, ky - 16, kx + 26 + w_, ky - 16, P(GOOD, 1, stroke=6))
            gx, gy = self.at(self.ui.get("gapx", 0), -90)
            self.chip(gx, gy - 54, "gap", T["gap"] - 0.2, T["driver"] - 0.55, accent=GOOD, size=40)
            x3, y3 = self.at(self.ui.get("trainx", -250) + 112, -120)
            self.label(x3, y3, x3 - 190, y3 - 250, "nodriver", T["driver"] - 0.1, s("break3") - 0.3, HILITE)
            self.badge("check", T["driver"] + 0.2, s("break3") - 0.15, x=880, y=420)
        elif ph == "stuck":
            self.chip(540, 420, "hot", T["hot"] - 0.2, s("fix4") - 0.25, accent=WARN, size=46)
            self.badge("alert", T["hot"], s("fix4") - 0.2, x=880, y=560)
            self.red(T["hot"], 1.8)
        elif ph == "air":
            x0, y0 = self.at(-466, -215)
            self.label(x0, y0, x0 + 150, y0 - 110, "fan", T["fans"] + 0.1, T["shafts"] - 0.15, "#7DD3FC")
            x1, y1 = self.at(236, -340)
            self.label(x1, y1, x1 - 190, y1 - 60, "shaft", T["shafts"] + 0.2, T["walkway"] - 0.4, "#FB923C")
            x2, y2 = self.at(430, -66)
            self.label(x2, y2, x2 - 170, y2 - 300, "walk", T["walkway"] + 0.2, s("cta") - 0.3, "#FDE68A")
            self.badge("check", T["station"], s("cta") - 0.15, x=880, y=420)

    def ui_platform(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        ph = self.phase(tw)
        if ph == "edge":
            x0, y0 = self.at(135, -170)
            self.label(x0, y0, x0 + 150, y0 - 250, "edge", T["close"] - 0.1, s("fix3") - 0.3, WARN)
            self.badge("alert", T["close"], s("fix3") - 0.2, x=200, y=560)
            self.red(T["close"], 1.8)
        elif ph == "psd":
            x0, y0 = self.at(-150, -240)
            self.label(x0, y0, x0 + 60, y0 - 190, "glass", T["wall0"] + 0.4, T["doors"] - 0.3, "#BAE6FD")
            x1, y1 = self.at(DOORS[1], -250)
            self.label(x1, y1, x1 + 110, y1 - 190, "aligned", T["arrive"] + 0.1, s("break4") - 0.3, GOOD)
            self.badge("check", T["opened"] + 0.3, s("break4") - 0.15, x=200, y=560)
        elif ph == "cta":
            x0, y0 = self.at(-360, -124)
            self.label(x0, y0, x0 + 170, y0 - 230, "card", T["tap"] - 0.1, s("reveal") - 0.3, GOOD)
        elif ph == "tag":
            if tw < T["friendcut"]:
                p = self.span(T["every"] - 0.1, T["friendcut"] + 0.1)
                if p > 0:                                                            # a little line of trains, all stopped
                    v2.chip(c, 540, 400, self.L["wait"], p, size=34, accent=WARN)
                    for i in range(5):
                        c.drawRRect(rr(190 + i * 146, 470, 120, 40, 12), P("#F8FAFC", p))
                        c.drawRect(R(190 + i * 146, 488, 120, 8), P(TEAL, p))
                        c.drawCircle(300 + i * 146, 500, 6, P(WARN, p * (0.5 + 0.5 * math.sin(tw * 10 + i))))
            else:
                x0, y0 = self.at(470, -196)
                self.label(x0, y0, x0 - 110, y0 - 220, "ticket", T["friend"] + 0.2, self.duration + 1, HILITE)

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(620, 290, "mind", T["mind"] - 0.15, T["s1"] - 0.5, accent=TEAL, size=52)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, rumble(1.2, 60), -9), (0.1, sfx.whoosh(0.5, True, 61), -10)]
        ev += [(0.15 + i * 0.16, chug(0.12, i), -11) for i in range(6)]
        ev += [(T["push"] - 0.5, sfx.creak(0.6, 62), -9), (T["wagon"], sfx.clank(300, 0.2, 63), -9), (T["congrats"] + 0.1, sfx.chime(), -8)]
        ev += [(T["slow"] - 0.2, sfx.power_down(0.8, 64), -10), (T["steam"] - 0.2, sfx.hiss(0.6, 65), -7)]
        ev += [(T["steam"] + i * 0.3, chug(0.16, i + 9), -8) for i in range(int(max(2, (T["riders"] - T["steam"]) / 0.3)))]
        ev += [(T["smoke"], sfx.alarm(3, 820), -11), (T["first"] - 0.1, sfx.pop(66), -6), (T["riders"] - 0.1, sfx.hiss(0.5, 67), -9),
               (T["riders"] + 0.2, chug(0.1, 30), -6), (T["riders"] + 0.5, chug(0.1, 31), -7), (T["smoked"] + 0.3, sfx.womp(), -8)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["electric"], sfx.charge_up(0.7), -8), (T["third0"], sfx.whoosh(0.6, True, 69), -9),
               (T["power"] - 0.3, sfx.sizzle(0.6, 70), -11), (T["shoes"] - 0.2, sfx.clank(700, 0.2, 71), -6), (T["shoes"], sfx.sizzle(0.5, 72), -10),
               (T["feed"], sfx.riser(0.8, 73), -12), (T["motors"], sfx.chime(), -6), (T["motors"] + 0.2, rail_hum(1.2), -9)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 74), -5), (s("break2"), rail_hum(2.0, 160, 300), -9), (T["catches"] - 0.6, sfx.power_down(0.6, 75), -10),
               (T["catches"], sfx.alarm(4, 820), -10), (T["another"], screech(max(0.5, T["dark"] - T["another"] + 0.1), 3), -8), (T["dark"] + 0.1, sfx.thud(0.3, 76), -5)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 77), -4), (s("fix2"), rail_hum(2.0, 200, 220), -13)]
        ev += [(T["beacons"] - 0.2 + i * 0.05, sfx.beep(1300 + i * 80, 0.05), -10) for i in range(7)]
        ev += [(T["radio"] - 0.2, sfx.pop(78), -7), (T["radio"], sfx.beep(2100, 0.06), -10), (T["radio"] + 0.15, sfx.beep(2500, 0.06), -10),
               (T["computer"] - 0.2, sfx.pop(79), -5), (T["gap"] - 0.4, sfx.beep(1700, 0.08), -9), (T["driver"] - 0.1, sfx.pop(80), -6),
               (T["driver"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, True, 81), -5), (T["somebody"] - 0.3, sfx.tap(82), -9), (T["somebody"], sfx.tap(83), -9),
               (T["close"] - 0.3, rail_hum(1.4, 120, 260), -9), (T["close"], sfx.alarm(3, 820), -10), (T["close"] + 0.1, sfx.ring(0.8), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 84), -4)]
        ev += [(T["wall0"] + i * 0.08, sfx.clank(600 + i * 30, 0.15, 85 + i), -9) for i in range(7)]
        ev += [(T["arrive"] - 1.4, rail_hum(1.4, 260, 120), -9), (T["arrive"] - 0.4, screech(0.4, 5), -13), (T["arrive"] + 0.1, sfx.beep(1700, 0.08), -8),
               (T["opened"], door_chime(), -5), (T["opened"] + 0.05, sfx.hiss(0.4, 92), -10), (T["opened"] + 0.4, sfx.chime(), -7)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 93), -5), (T["halt"] - 0.5, screech(0.5, 6), -11), (T["halt"], sfx.power_down(1.0, 94), -8),
               (T["hot"], sfx.alarm(3, 820), -11), (T["hot"] - 0.4, sfx.riser(0.8, 95), -13)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 96), -4), (T["fans"] - 0.25, sfx.thunk(97), -5), (T["fans"], sfx.whirr(1.8, 90, 180, 98), -8),
               (T["shafts"] - 0.2, rumble(0.7, 99), -10), (T["street"], sfx.whoosh(0.5, True, 100), -8), (T["street"] + 0.2, sfx.pop(101), -7)]
        ev += [(T["walkway"] - 0.3 + i * 0.08, sfx.tick(), -9) for i in range(8)]
        ev += [(T["station"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(102), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 103), -7), (T["follow"] - 0.15, sfx.pop(104), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 105), -6)]
        ev += [(T["map"] - 0.3 + i * 0.14, sfx.whoosh(0.3, True, 106 + i), -12) for i in range(5)]
        ev += [(T["lines"] + 0.5, sfx.sparkle(0.6, 8, 112), -9), (T["voice"] - 0.2, door_chime(), -6), (T["mind"] - 0.15, sfx.pop(113), -8)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 114), -6), (T["s1"], sfx.pop(115), -3), (T["s2"], sfx.pop(116), -3), (T["s3"], sfx.pop(117), -3),
               (T["s1"], rail_hum(2.4, 200, 240), -13)]
        ev += [(s("closer") - 0.1, sfx.whoosh(0.4, True, 118), -6), (s("closer"), rail_hum(1.0, 260, 120), -11), (T["cong2"], sfx.pop(119), -2),
               (T["cong2"], sfx.sparkle(1.0, 14, 120), -4), (T["cong2"] + 0.3, door_chime(), -6), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 121), -6), (T["guy"], sfx.thud(0.2, 122), -7), (T["every"] - 0.1, sfx.buzz(0.3), -9),
               (T["every"] + 0.3, sfx.beep(520, 0.15), -12), (T["waiting"], sfx.beep(520, 0.25), -12), (T["friendcut"], sfx.whoosh(0.35, True, 123), -8),
               (T["friend"] + 0.3, sfx.tap(124), -8), (T["friend"] + 0.6, sfx.tap(125), -8), (T["ticket"] + 0.3, sfx.womp(), -3)]
        return ev


NAME = "metro"
EPISODE = Metro
