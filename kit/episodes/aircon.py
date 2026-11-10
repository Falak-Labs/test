"""Episode 14 - An air conditioner.  v2 look: one house, three cameras (whip cuts between them).

room   the living room from the side (floor at y = 0): x -420..330, the front door in the left wall, the couch under
       the machine, the street beyond the right wall
unit   the machine itself: the cold coil on the wall (x 84..300, y -456..-372), the pipes through the right wall and
       the box outside (x 430..610, y -300..-130)
wide   the whole house, for the numbers
"""
from v2_base import *  # noqa: F401,F403

ROOM_L, ROOM_R, CEIL, WALL_R = -420, 330, -520, 370
LIQ, GASC, HOT, COPPER = "#38BDF8", "#FDBA74", "#EF4444", "#C7803E"
COOL, WARM = "#7DD3FC", "#FB923C"
ICOIL = [(300, -372), (84, -372), (84, -400), (276, -400), (276, -428), (84, -428), (84, -456), (300, -456)]
GASLINE = [(300, -456), (408, -456), (408, -205), (446, -205)]
THROUGH = [(446, -205), (474, -205), (474, -262)]
HOTLINE = [(474, -262), (474, -284), (520, -284)]
OCOIL = [(520, -284), (520, -150), (545, -150), (545, -284), (570, -284), (570, -150)]
LIQLINE = [(570, -150), (570, -116), (388, -116), (388, -372), (300, -372)]
COUCH_X = (130, 190, 250)                                 # where the crew sits
SEAT = -58


class Line:
    """A polyline you can walk along by distance."""

    def __init__(self, pts):
        self.pts = pts
        self.seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        self.len = sum(self.seg)

    def at(self, d):
        d = clamp(d, 0.0, self.len)
        for i, sl in enumerate(self.seg):
            if d <= sl or i == len(self.seg) - 1:
                k = clamp(d / sl) if sl else 0.0
                return lerp(self.pts[i][0], self.pts[i + 1][0], k), lerp(self.pts[i][1], self.pts[i + 1][1], k)
            d -= sl

    def path(self, d0=0.0, d1=None):
        d1 = self.len if d1 is None else min(d1, self.len)
        p = skia.Path()
        p.moveTo(*self.at(d0))
        acc = 0.0
        for i, sl in enumerate(self.seg):
            if d0 < acc + sl < d1:
                p.lineTo(*self.pts[i + 1])
            acc += sl
        p.lineTo(*self.at(d1))
        return p


IC, GL, TH, HL, OC, LL = Line(ICOIL), Line(GASLINE), Line(THROUGH), Line(HOTLINE), Line(OCOIL), Line(LIQLINE)
LOOP = Line(ICOIL + GASLINE[1:] + THROUGH[1:] + HOTLINE[1:] + OCOIL[1:] + LIQLINE[1:])
D_IC = IC.len
D_GAS = D_IC + GL.len
D_COMP = D_GAS + TH.len
D_HOT = D_COMP + HL.len
D_OC = D_HOT + OC.len


def flow_col(d):
    if d < D_IC:
        return mix(LIQ, GASC, clamp((d / D_IC - 0.2) / 0.6))
    if d < D_GAS:
        return GASC
    if d < D_HOT:
        return HOT
    if d < D_OC:
        return mix(HOT, LIQ, clamp(((d - D_HOT) / OC.len - 0.15) / 0.7))
    return LIQ


def pipe(c, ln, d0=0.0, d1=None, w=14, a=1.0):
    if (ln.len if d1 is None else d1) <= d0 or a <= 0:
        return
    p = ln.path(d0, d1)
    for col, ww in ((shade(COPPER, -0.45), w + 4), (COPPER, w), ("#1A1210", w - 7)):
        pr = P(col, a, stroke=ww)
        pr.setStrokeCap(skia.Paint.kRound_Cap)
        pr.setStrokeJoin(skia.Paint.kRound_Join)
        c.drawPath(p, pr)


def fan(c, x, y, r, ang, a=1.0, guard=True, col="#E5E9F2"):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    if guard:
        c.drawCircle(0, 0, r, P("#0B1220", 0.55 * a))
        c.drawCircle(0, 0, r, P("#94A3B8", a, stroke=max(3, r * 0.08)))
    c.rotate(ang)
    for i in range(4):
        c.save()
        c.rotate(i * 90)
        c.drawOval(R(r * 0.1, -r * 0.22, r * 0.78, r * 0.44), P(col, 0.92 * a))
        c.restore()
    c.drawCircle(0, 0, r * 0.2, P("#475569", a))
    c.restore()


def wisps(c, x0, y0, x1, y1, t, col, n=7, a=1.0, spread=40, speed=0.55, seed=0, w=6):
    """Air on the move: short curls drifting from (x0, y0) to (x1, y1)."""
    if a <= 0:
        return
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    for i in range(n):
        u = (t * speed + i / n + seed * 0.37) % 1.0
        off = math.sin(i * 12.9898 + seed) * spread * (0.3 + 0.7 * u) + math.sin(t * 3 + i) * 6
        px, py = x0 + dx * u + nx * off, y0 + dy * u + ny * off
        k = math.sin(math.pi * u) * a
        p = skia.Path()
        p.moveTo(px, py)
        p.quadTo(px + dx / ln * 22 + nx * 12, py + dy / ln * 22 + ny * 12, px + dx / ln * 44, py + dy / ln * 44)
        pr = P(col, 0.85 * k, stroke=w)
        pr.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPath(p, pr)


def penguin(c, x, y, s, t, face=1, slide=False):
    c.save()
    c.translate(x, y)
    c.scale(face * s, s)
    if slide:
        c.rotate(80)
        c.translate(-20, -18)
    else:
        c.rotate(math.sin(t * 9 + x * 0.1) * 7)
    for fx_ in (-9, 9):
        c.drawOval(R(fx_ - 9, -6, 20, 9), P("#F59E0B"))
    c.drawOval(R(-22, -66, 44, 64), P("#111827"))
    c.drawOval(R(-13, -52, 30, 48), P("#F8FAFC"))
    c.drawOval(R(-25, -48, 10, 30), P("#111827"))
    c.drawOval(R(15, -48, 10, 30), P("#111827"))
    c.drawCircle(4, -70, 17, P("#111827"))
    c.drawCircle(10, -73, 4, P("#FFFFFF"))
    c.drawCircle(11, -73, 2, P("#111827"))
    bk = skia.Path()
    bk.moveTo(16, -70)
    bk.lineTo(31, -66)
    bk.lineTo(16, -62)
    bk.close()
    c.drawPath(bk, P("#F59E0B"))
    c.restore()


def couch(c, wet=0.0, snow=0.0):
    box(c, 70, -124, 240, 78, "#5B4BC4", r=22)
    box(c, 62, -92, 34, 92, "#6D5BD0", r=14)
    box(c, 284, -92, 34, 92, "#6D5BD0", r=14)
    box(c, 92, SEAT, 196, 44, "#7C6BE0", r=12)
    c.drawRect(R(190, SEAT + 2, 2, 38), P("#000000", 0.2))
    c.drawRect(R(86, -12, 208, 12), P("#3B2F8F"))
    if wet > 0:
        c.drawOval(R(190 - 70 * wet, SEAT - 4, 140 * wet, 20 * wet), P("#38BDF8", 0.8))
        c.drawOval(R(190 - 50 * wet, SEAT - 2, 60 * wet, 8 * wet), P("#FFFFFF", 0.4))
    if snow > 0:
        c.drawRRect(rr(68, -136, 244, 22 * snow, 11), P("#F1F5F9", snow))
        c.drawRRect(rr(60, -100, 38, 14 * snow, 7), P("#F1F5F9", snow))
        c.drawRRect(rr(282, -100, 38, 14 * snow, 7), P("#F1F5F9", snow))


def remote(c, x, y, rot=0.0, a=1.0, s=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    c.drawRRect(rr(-10, -26, 20, 52, 6), P("#F8FAFC", a))
    c.drawRRect(rr(-7, -22, 14, 12, 2), P("#0EA5E9", a))
    c.drawCircle(0, -2, 4, P("#EF4444", a))
    for i in range(2):
        for j in range(2):
            c.drawCircle(-4 + i * 8, 8 + j * 8, 2.4, P("#94A3B8", a))
    c.restore()


def hum_snd(d=1.5, f=62.0):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2 * tt) + 0.25 * np.sin(2 * np.pi * f * 3.01 * tt)
    return sfx._norm(x * sfx._ar(n, 0.15, 0.4) * (0.8 + 0.2 * np.sin(2 * np.pi * 11 * tt)), 0.6)


def drip_snd(seed=0):
    n = int(0.16 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 900 + 1500 * tt / 0.16 + seed * 60
    return sfx._norm(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * sfx._env(n, 0.003, 0.05), 0.8)


def squawk(seed=0):
    n = int(0.22 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 520 + 160 * np.sin(2 * np.pi * 9 * tt) + seed * 40
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f * 2) / sfx.SR) * 0.5
    return sfx._norm(sfx._bp(x, 400, 3000) * sfx._ar(n, 0.02, 0.1), 0.6)


def wind_snd(d=1.2, seed=3, lo=300, hi=2400):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), lo, hi)
    return sfx._norm(x * sfx._ar(n, d * 0.3, d * 0.5), 0.6)


# ====================================================================================== the episode
class Aircon(EpisodeV2):
    BUILD_NO = 14
    FIRST_SET = "room"
    CLEAR = "#0B1024"
    TITLE = {"en": "AIR CONDITIONER", "ar_sa": "مكيف"}
    EMPH = {"en": ["CONGRATS", "CONDITIONER", "ICE", "MELTS", "PUDDLE", "LIQUID", "BOILS", "COIL", "HEAT", "GAS", "NOWHERE",
                   "COMPRESSOR", "SQUEEZES", "OUTSIDE", "STREET", "NEVER", "PENGUIN", "THERMOSTAT", "OFF", "ON", "WATER", "DRIPPING",
                   "COUCH", "TRAY", "DRAIN", "FILTER", "DUST", "FOLLOW", "STATION", "HIDE", "LOSE", "REMOTE", "ZERO", "YOURSELF",
                   "DAD", "DOOR", "STREET"],
            "ar_sa": ["مبروك", "مكيف", "ثلج", "يذوب", "بركة", "بسائل", "يغلي", "ملف", "الحرارة", "غاز", "وين", "كمبروسر", "يضغط",
                      "برا", "الشارع", "أبد", "للبطاريق", "ثرموستات", "يطفيه", "يشغله", "الموية", "تنقط", "كنبتك", "صينية",
                      "تصريف", "وفلتر", "الغبار", "تابعني", "فضاء", "خبّي", "وضيّع", "الريموت", "وصفر", "بيدك", "وأبوك", "الباب"]}
    KEYS = {"ar_sa": {
        ("hook", "BLOCK"): "قالب", ("hook", "ICE"): "ثلج", ("hook", "FAN"): "مروحة", ("hook", "CONGRATS"): "مبروك",
        ("break1", "ICE"): "الثلج", ("break1", "MELTS"): "يذوب", ("break1", "HOUR"): "ساعة", ("break1", "PUDDLE"): "بركة", ("break1", "WARM"): "حار",
        ("fix1", "SWAP"): "فتبدل", ("fix1", "LIQUID"): "بسائل", ("fix1", "BOILS"): "يغلي", ("fix1", "COIL"): "ملف", ("fix1", "COLD"): "بارد",
        ("fix1", "DRINKS"): "ويسحب", ("fix1", "HEAT"): "الحرارة", ("fix1", "ROOM"): "غرفتك",
        ("break2", "COOLS"): "تبرد", ("break2", "LIQUID"): "السائل", ("break2", "GAS"): "غاز", ("break2", "FULL"): "مليان", ("break2", "HEAT"): "حرارة",
        ("break2", "NOWHERE"): "وين", ("break2", "PUT"): "توديها",
        ("fix2", "COMPRESSOR"): "كمبروسر", ("fix2", "SQUEEZES"): "يضغط", ("fix2", "SECOND"): "ثاني", ("fix2", "OUTSIDE"): "برا", ("fix2", "FAN"): "مروحة",
        ("fix2", "DUMPS"): "ترمي", ("fix2", "HEAT"): "الحرارة", ("fix2", "STREET"): "الشارع",
        ("break3", "NEVER"): "يوقف", ("break3", "STOPS"): "أبد", ("break3", "LIVING"): "صالتك", ("break3", "PENGUIN"): "للبطاريق",
        ("fix3", "THERMOSTAT"): "ثرموستات", ("fix3", "OFF"): "يطفيه", ("fix3", "TEMPERATURE"): "الدرجة", ("fix3", "PICK"): "تختارها",
        ("fix3", "BACK"): "ويرجع", ("fix3", "ON"): "يشغله", ("fix3", "WARMS"): "حرّت",
        ("break4", "PERFECT"): "تمام", ("break4", "WATER"): "الموية", ("break4", "DRIPPING"): "تنقط", ("break4", "WALL"): "الجدار", ("break4", "COUCH"): "كنبتك",
        ("fix4", "TRAY"): "صينية", ("fix4", "DRAIN"): "وماسورة", ("fix4", "WATER"): "للموية", ("fix4", "PULLS"): "يسحبها", ("fix4", "AIR"): "الهوا",
        ("fix4", "FILTER"): "وفلتر", ("fix4", "CATCHES"): "يصيد", ("fix4", "DUST"): "الغبار",
        ("cta", "GRAB"): "تمسك", ("cta", "REMOTE"): "الريموت", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "HIDE"): "خبّي", ("reveal", "OUTSIDE"): "برا", ("reveal", "HANG"): "وعلّق", ("reveal", "WALL"): "الجدار", ("reveal", "LOSE"): "وضيّع",
        ("reveal", "REMOTE"): "الريموت",
        ("stat", "ONE"): "غرفة", ("stat", "TWO"): "ملفّين", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "DAD"): "وأبوك", ("tag", "CLOSE"): "سكّر", ("tag", "DOOR"): "الباب", ("tag", "COOLING"): "تبرّد", ("tag", "STREET"): "الشارع"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a space station"),
                   "stat": [("1", "ROOM"), ("2", "COILS"), ("0", "SWEAT")],
                   "L": {"ice": "ICE", "hour": "1 HOUR", "coil": "COLD COIL", "boil": "IT BOILS", "full": "FULL OF HEAT", "nowhere": "DEAD END",
                         "comp": "COMPRESSOR", "coil2": "SECOND COIL", "street": "HEAT GOES OUT", "thermo": "THERMOSTAT", "off": "OFF", "on": "ON",
                         "tray": "TRAY", "drain": "DRAIN PIPE", "filter": "FILTER", "dust": "DUST", "remote": "THE REMOTE", "lost": "GONE",
                         "hot": "STILL HOT"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: محطة فضاء"),
                      "stat": [("1", "غرفة"), ("2", "ملفّين"), ("0", "عرق")],
                      "L": {"ice": "ثلج", "hour": "ساعة وحدة", "coil": "ملف بارد", "boil": "يغلي", "full": "مليان حرارة", "nowhere": "طريق مسدود",
                            "comp": "كمبروسر", "coil2": "ملف ثاني", "street": "الحرارة تطلع برا", "thermo": "ثرموستات", "off": "طافي", "on": "شغال",
                            "tray": "صينية", "drain": "ماسورة تصريف", "filter": "فلتر", "dust": "غبار", "remote": "الريموت", "lost": "ضاع",
                            "hot": "لسا حار"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "block": ("hook", "BLOCK", 0.3), "ice": ("hook", "ICE", 0.42), "fan": ("hook", "FAN", 0.5), "congrats": ("hook", "CONGRATS", 0.56),
            "ice2": ("break1", "ICE", 0.15), "melts": ("break1", "MELTS", 0.22), "hour": ("break1", "HOUR", 0.38), "puddle": ("break1", "PUDDLE", 0.72),
            "warm": ("break1", "WARM", 0.9),
            "swap": ("fix1", "SWAP", 0.1), "liquid": ("fix1", "LIQUID", 0.36), "boils": ("fix1", "BOILS", 0.45), "cold": ("fix1", "COLD", 0.6),
            "coil": ("fix1", "COIL", 0.64), "drinks": ("fix1", "DRINKS", 0.74), "heat": ("fix1", "HEAT", 0.84), "room1": ("fix1", "ROOM", 0.95),
            "cools": ("break2", "COOLS", 0.15), "liquid2": ("break2", "LIQUID", 0.36), "gas": ("break2", "GAS", 0.5), "full": ("break2", "FULL", 0.56),
            "heat2": ("break2", "HEAT", 0.64), "nowhere": ("break2", "NOWHERE", 0.78), "put": ("break2", "PUT", 0.92),
            "compressor": ("fix2", "COMPRESSOR", 0.16), "squeezes": ("fix2", "SQUEEZES", 0.28), "second": ("fix2", "SECOND", 0.48),
            "outside": ("fix2", "OUTSIDE", 0.58), "fan2": ("fix2", "FAN", 0.7), "dumps": ("fix2", "DUMPS", 0.76), "heat3": ("fix2", "HEAT", 0.84),
            "street": ("fix2", "STREET", 0.95),
            "never": ("break3", "NEVER", 0.14), "stops": ("break3", "STOPS", 0.22), "living": ("break3", "LIVING", 0.48), "penguin": ("break3", "PENGUIN", 0.72),
            "thermostat": ("fix3", "THERMOSTAT", 0.16), "off": ("fix3", "OFF", 0.38), "temperature": ("fix3", "TEMPERATURE", 0.48), "pick": ("fix3", "PICK", 0.62),
            "back": ("fix3", "BACK", 0.72), "on": ("fix3", "ON", 0.76), "warms": ("fix3", "WARMS", 0.88),
            "perfect": ("break4", "PERFECT", 0.14), "water": ("break4", "WATER", 0.32), "dripping": ("break4", "DRIPPING", 0.46), "wall": ("break4", "WALL", 0.7),
            "couch": ("break4", "COUCH", 0.94),
            "tray": ("fix4", "TRAY", 0.14), "drain": ("fix4", "DRAIN", 0.24), "water2": ("fix4", "WATER", 0.38), "pulls": ("fix4", "PULLS", 0.46),
            "air": ("fix4", "AIR", 0.58), "filter": ("fix4", "FILTER", 0.7), "catches": ("fix4", "CATCHES", 0.8), "dust": ("fix4", "DUST", 0.92),
            "grab": ("cta", "GRAB", 0.2), "remote": ("cta", "REMOTE", 0.28), "follow": ("cta", "FOLLOW", 0.4),
            "hide": ("reveal", "HIDE", 0.12), "outside2": ("reveal", "OUTSIDE", 0.3), "hang": ("reveal", "HANG", 0.4), "wall2": ("reveal", "WALL", 0.66),
            "lose": ("reveal", "LOSE", 0.8), "remote2": ("reveal", "REMOTE", 0.9),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "TWO", 0.4), "s3": ("stat", "ZERO", 0.72),
            "cong2": ("closer", "CONGRATS", 0.16),
            "dad": ("tag", "DAD", 0.18), "close": ("tag", "CLOSE", 0.35), "door": ("tag", "DOOR", 0.48), "cooling": ("tag", "COOLING", 0.72),
            "street2": ("tag", "STREET", 0.95)})
        T["land"] = T["ice"] - 0.12                                    # the ice lands in front of the fan
        T["coil0"] = min(T["cold"], T["coil"])
        T["allgas"] = T["gas"]
        T["losecut"] = T["lose"] - 0.3
        T["slam"] = T["street2"] + 0.1
        self.cut(s("fix1") - 0.12, "unit", 1)
        self.cut(s("break3") - 0.1, "room", -1)
        self.cut(s("fix3") - 0.12, "unit", 1)
        self.cut(s("break4") - 0.12, "room", -1)
        self.cut(s("fix4") - 0.12, "unit", 1)
        self.cut(s("cta") + 0.05, "room", -1)
        self.cut(s("reveal") - 0.1, "unit", 1)
        self.cut(T["losecut"], "room", -1)
        self.cut(T["s1"] - 0.35, "wide", 1)
        self.cut(s("tag") - 0.2, "room", -1)
        rc = Camera(-160, -112, 2.35)                                  # the room
        rc.key(0.05, -165, -108, 2.5, 1.6).key(s("break1") - 0.1, -150, -123, 2.2, 0.9)
        rc.key(s("break3") - 0.1, -40, -216, 1.25, 0.0).key(T["penguin"] - 0.6, -70, -186, 1.45, 1.0)
        rc.key(s("break4") - 0.12, 150, -180, 1.5, 0.0).key(T["wall"] - 0.4, 180, -159, 1.7, 1.0)
        rc.key(s("cta") + 0.05, 175, -165, 1.7, 0.0)
        rc.key(T["losecut"], 180, -135, 2.0, 0.0)
        rc.key(s("tag") - 0.2, -335, -142, 1.9, 0.0)
        uc = Camera(180, -345, 2.3)                                    # the machine
        uc.key(s("fix1") - 0.12, 175, -340, 2.2, 0.0).key(T["coil0"] - 0.5, 185, -345, 2.4, 1.0)
        uc.key(s("fix2") - 0.1, 345, -267, 1.75, 1.0).key(T["fan2"] - 0.2, 410, -267, 1.75, 0.8)
        uc.key(s("fix3") - 0.12, 110, -300, 1.75, 0.0)
        uc.key(s("fix4") - 0.12, 200, -345, 2.2, 0.0).key(T["drain"] - 0.1, 345, -267, 1.75, 0.9).key(T["filter"] - 0.5, 200, -345, 2.1, 0.8)
        uc.key(s("reveal") - 0.1, 470, -250, 1.8, 0.0).key(T["hang"] - 0.35, 240, -330, 2.0, 0.6)
        wc = Camera(70, -166, 0.95)
        wc.key(T["s1"] - 0.35, 70, -166, 0.95, 0.0).key(s("closer"), 70, -172, 1.0, 2.2)
        self.cams = {"room": rc, "unit": uc, "wide": wc}
        self.temp = (Track(40.0).to(T["land"], 31.0, max(0.4, T["congrats"] - T["land"]), e_out)
                     .to(T["melts"], 40.0, max(0.5, T["warm"] - T["melts"]))
                     .to(T["drinks"], 30.0, max(0.5, T["room1"] - T["drinks"] + 0.3))
                     .to(s("break2"), 27.0, max(0.3, T["allgas"] - s("break2") - 0.2))
                     .to(T["allgas"], 34.0, max(0.5, T["put"] - T["allgas"]))
                     .to(T["dumps"], 24.0, max(0.5, T["street"] - T["dumps"] + 0.4))
                     .to(T["never"], -5.0, max(0.6, T["penguin"] - T["never"] + 0.3))
                     .to(T["off"], 24.0, max(0.4, T["pick"] - T["off"]))
                     .to(T["pick"] + 0.1, 26.0, max(0.2, T["on"] - T["pick"] - 0.1))
                     .to(T["on"] + 0.1, 24.0, 0.7))
        self.frost = Track(0.0).to(T["never"], 1.0, max(0.6, T["penguin"] - T["never"])).to(T["off"] - 0.2, 0.0, max(0.5, T["pick"] - T["off"] + 0.2))
        self.gasfrac = (Track(0.0).to(T["boils"], 0.35, max(0.5, T["room1"] - T["boils"]))
                        .to(T["liquid2"] - 0.2, 1.0, max(0.4, T["allgas"] - T["liquid2"] + 0.2)))
        self.runk = Track(0.0).to(T["squeezes"], 1.0, 0.4).to(T["off"], 0.0, 0.35).to(T["on"], 1.0, 0.35)
        self.fank = Track(1.0).to(T["off"], 0.0, 0.5).to(T["on"], 1.0, 0.4)
        self.built = (Track(D_IC).to(s("fix2") - 0.05, D_GAS, max(0.3, T["compressor"] - s("fix2")))
                      .to(T["squeezes"] - 0.2, D_COMP, 0.2)
                      .to(T["second"] - 0.4, D_OC, max(0.4, T["outside"] - T["second"] + 0.5))
                      .to(T["outside"] + 0.15, LOOP.len, max(0.3, T["fan2"] - T["outside"])))
        ts = np.arange(0.0, self.duration + 2.0, 1 / 30)
        self._ts = ts
        self._ph_run = np.cumsum([self.runk.at(x) for x in ts]) / 30
        self._ph_fan = np.cumsum([self.fank.at(x) for x in ts]) / 30
        self.spans = [(T["melts"] + 0.2, T["room1"]), (T["allgas"], T["street"]), (T["stops"], T["warms"]), (T["dripping"], T["dust"])]
        self.shakes = [(T["land"], 0.2, 8), (T["allgas"], 0.3, 8), (T["compressor"], 0.25, 8), (T["stops"], 0.3, 8), (T["slam"], 0.3, 14)]

    def ph_run(self, t):
        return float(np.interp(t, self._ts, self._ph_run))

    def ph_fan(self, t):
        return float(np.interp(t, self._ts, self._ph_fan))

    # ------------------------------------------------------------------ the house
    def backdrop(self, c, t, cam):
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, horizon_y=gy)
        sx, sy = self.to_screen(cam, 820, -430)
        add_glow(c, sx, sy, 520 * z, "#FF8A3D", 0.5)
        c.drawCircle(sx, sy, 80 * z, P("#FFD9A0"))

    def house(self, c, t):
        T, s = self.T, self.tl.s
        fr = self.frost.at(t)
        tagt = t >= s("tag") - 0.2
        # outside: the street and its heat
        box(c, WALL_R, 0, 1400, 22, "#4B5578")
        box(c, -1800, 0, 1340, 22, "#4B5578")
        for i in range(5):
            wisps(c, 700 + i * 150, -10, 700 + i * 150, -260, t, "#FF9A62", n=3, a=0.35, spread=14, speed=0.3, seed=i, w=5)
            wisps(c, -620 - i * 150, -10, -620 - i * 150, -260, t, "#FF9A62", n=3, a=0.35, spread=14, speed=0.3, seed=i + 7, w=5)
        # the room
        vrect(c, ROOM_L, CEIL, ROOM_R - ROOM_L, -CEIL, [mix("#3C4C74", "#7FB2D9", 0.45 * fr), mix("#2F3D61", "#6FA3CC", 0.45 * fr), mix("#242F4E", "#5C8DB8", 0.4 * fr)],
              [0.0, 0.5, 1.0])
        for px in range(ROOM_L + 70, ROOM_R, 130):
            c.drawRect(R(px, CEIL, 3, -CEIL), P("#000000", 0.10))
        c.drawRect(R(ROOM_L, -26, ROOM_R - ROOM_L, 26), P("#1B2440"))
        wx, wy = -330, -420                                                          # the window: a hot evening
        c.drawRRect(rr(wx - 8, wy - 8, 166, 196, 8), P("#141829"))
        vrect(c, wx, wy, 150, 180, ["#7C2D12", "#EA580C", "#FDBA74"], [0.0, 0.6, 1.0])
        c.drawCircle(wx + 100, wy + 120, 34, P("#FFE9B8"))
        add_glow(c, wx + 100, wy + 120, 120, "#FFB25A", 0.5)
        c.drawRect(R(wx + 72, wy, 6, 180), P("#141829"))
        c.drawRect(R(wx, wy + 86, 150, 6), P("#141829"))
        if fr > 0:
            c.drawRRect(rr(wx, wy, 150, 180, 4), P("#E0F2FE", 0.55 * fr))
        for lx in (-200, 40):                                                        # lamps
            c.drawRect(R(lx - 2, CEIL, 4, 36), P("#11151F"))
            c.drawRRect(rr(lx - 30, CEIL + 36, 60, 16, 8), P("#FFF3C4"))
            add_glow(c, lx, CEIL + 70, 300, "#FFE9B8", 0.20)
        # floor, walls, roof
        box(c, ROOM_L - 50, 0, WALL_R - ROOM_L + 60, 26, "#6B7699")
        box(c, ROOM_R, CEIL - 6, WALL_R - ROOM_R, -CEIL + 6, "#7C86A6")
        box(c, ROOM_L - 40, CEIL - 6, 40, -CEIL - 236 + 6, "#7C86A6")                  # the left wall, above the door
        box(c, ROOM_L - 52, CEIL - 40, WALL_R - ROOM_L + 64, 40, "#55607F", r=6)
        # the front door (left wall)
        dk = self.doork(t)
        c.drawRect(R(ROOM_L - 40, -236, 40, 236), P("#0B1020", 0.0 if dk > 0 else 1.0))
        if dk <= 0:
            box(c, ROOM_L - 30, -236, 20, 236, "#8B5E3C", r=3)
            c.drawCircle(ROOM_L - 14, -116, 6, P(BRASS_))
        else:                                                                        # open: the leaf swung outside
            c.save()
            c.translate(ROOM_L - 40, 0)
            box(c, -150 * dk, -236, 150 * dk + 4, 236, "#8B5E3C", r=3)
            c.drawRRect(rr(-150 * dk + 14, -216, max(0.0, 150 * dk - 28), 196, 4), P("#000000", 0.15))
            c.restore()
        if fr > 0:                                                                   # the deep freeze
            rng = random.Random(4)
            for i in range(26):
                ix = rng.uniform(ROOM_L + 10, ROOM_R - 10)
                ih = rng.uniform(18, 62) * fr
                p = skia.Path()
                p.moveTo(ix - 7, CEIL)
                p.lineTo(ix + 7, CEIL)
                p.lineTo(ix, CEIL + ih)
                p.close()
                c.drawPath(p, P("#E0F2FE", 0.9))
            c.drawRRect(rr(ROOM_L, -14 * fr, ROOM_R - ROOM_L, 14 * fr + 2, 6), P("#F1F5F9", fr))
            for i in range(40):
                u = (t * (0.25 + (i % 5) * 0.05) + i * 0.137) % 1.0
                fx_ = ROOM_L + ((i * 97.3 + math.sin(t + i) * 20) % (ROOM_R - ROOM_L))
                c.drawCircle(fx_, CEIL + u * (-CEIL), 3 + (i % 3), P("#FFFFFF", 0.85 * fr * math.sin(math.pi * u)))
        if tagt:                                                                     # the cold pouring out of the open door
            a = clamp(dk)
            wisps(c, -330, -120, -640, -130, t, COOL, n=9, a=a, spread=70, speed=0.8, seed=2, w=8)
            wisps(c, -360, -60, -640, -40, t, COOL, n=6, a=a, spread=40, speed=0.9, seed=5, w=7)

    def doork(self, t):
        T, s = self.T, self.tl.s
        if t < s("tag") - 0.2:
            return 0.0
        return 1.0 - e_in(prog(t, T["slam"] - 0.14, T["slam"]))

    # ------------------------------------------------------------------ the machine
    def machine(self, c, t):
        T, s = self.T, self.tl.s
        if t < s("fix1") - 0.12:
            return
        fr = self.frost.at(t)
        run = self.runk.at(t)
        loop = t >= T["squeezes"]
        covered_in = e_back(prog(t, T["hang"] - 0.1, T["wall2"]))
        covered_out = e_back(prog(t, T["hide"] - 0.1, T["outside2"]))
        built = self.built.at(t)
        # ---- outside: bracket, frame
        ok = e_back(prog(t, T["second"] - 0.5, T["second"] - 0.1))
        if t >= s("fix2") - 0.05:
            if ok > 0:
                c.drawLine(WALL_R, -130, 618, -130, P("#94A3B8", ok, stroke=8))
                c.drawLine(WALL_R, -60, 520, -130, P("#94A3B8", ok, stroke=6))
                c.drawRRect(rr(430, -300, 180, 170, 12), P("#0B1220", 0.55 * ok))
                c.drawRRect(rr(430, -300, 180, 170, 12), dash_paint("#CBD5E1", 0.7 * ok, 3, t))
            fk2 = e_back(prog(t, T["fan2"] - 0.2, T["fan2"] + 0.1))
            fan(c, 552, -217, 56 * fk2, self.ph_run(t) * 620, fk2)
        # ---- the indoor fan, behind the coil
        fan(c, 190, -414, 52, self.ph_fan(t) * 560, 1.0)
        # ---- pipes
        ck = prog(t, T["swap"] - 0.1, T["liquid"] - 0.1) if t < s("break2") else 1.0
        pipe(c, IC, 0.0, IC.len * ck)
        if t >= s("fix2") - 0.05:
            pipe(c, GL, 0.0, min(GL.len, built - D_IC))
            if built > D_COMP:
                pipe(c, HL, 0.0, built - D_COMP)
            if built > D_HOT:
                pipe(c, OC, 0.0, built - D_HOT)
            if built > D_OC:
                pipe(c, LL, 0.0, built - D_OC, w=10)
        else:                                                                        # a closed coil: two capped ends
            for ex, ey in ((300, -372), (300, -456)):
                c.drawRRect(rr(ex - 2, ey - 11, 10, 22, 3), P("#94A3B8", ck))
        # ---- what is inside the pipes
        if not loop:
            gf = self.gasfrac.at(t)
            full = prog(t, T["full"] - 0.1, T["full"] + 0.4)
            fill = prog(t, T["liquid"] - 0.15, T["liquid"] + 0.35)
            n = int(IC.len / 15)
            for i in range(n):
                d = (i + 0.5) / n * IC.len
                if d / IC.len > fill:
                    continue
                isgas = d / IC.len > 1 - gf
                if isgas:
                    jx, jy = math.sin(t * 9 + i * 1.7) * 2.5, math.cos(t * 11 + i) * 2.5
                    x, y = IC.at(d)
                    c.drawCircle(x + jx, y + jy, 3.4, P(mix(GASC, HOT, full), 0.95))
                else:
                    x, y = IC.at(d)
                    boil = t >= T["boils"] - 0.1
                    c.drawCircle(x, y + (math.sin(t * 14 + i) * 1.5 if boil else 0), 4.2, P(LIQ))
                    if boil and (i + int(t * 6)) % 5 == 0:
                        c.drawCircle(x + 3, y - 2, 2, P("#FFFFFF", 0.9))
            if full > 0:
                add_glow(c, 190, -414, 190, HOT, (0.35 + 0.2 * math.sin(t * 8)) * full)
        else:
            ph = self.ph_run(t) * 130
            sp = 22.0
            n = int(LOOP.len / sp)
            for i in range(n):
                d = (i * sp + ph) % LOOP.len
                if d > built:
                    continue
                x, y = LOOP.at(d)
                hot = D_COMP <= d < D_HOT + OC.len * 0.4
                c.drawCircle(x, y, 4.6 if hot else 3.8, P(flow_col(d), 0.4 + 0.6 * max(run, 0.25)))
        # ---- the compressor
        kc = e_back(prog(t, T["compressor"] - 0.2, T["compressor"] + 0.1))
        if kc > 0 and covered_out < 1:
            sq = 1 + 0.07 * math.sin(t * 34) * run
            c.save()
            c.translate(474, -205)
            c.scale(kc * sq, kc * (2 - sq))
            c.drawRRect(rr(-28, -57, 56, 114, 26), lin_paint(-28, 0, 28, 0, ["#475569", "#111827", "#334155"]))
            c.drawRRect(rr(-28, -57, 56, 114, 26), P("#94A3B8", 1, stroke=3))
            c.drawRRect(rr(-20, -8, 40, 16, 4), P("#F59E0B"))
            c.restore()
            if run > 0.5 and t < T["second"]:
                for sd in (-1, 1):
                    k = (t * 3) % 1.0
                    text(c, ">" if sd < 0 else "<", 474 + sd * (52 - 14 * k), -196, 34, "#FFFFFF", "Poppins-Black", a=1 - k)
        # ---- heat out to the street
        if t >= T["dumps"] - 0.1 and run > 0:
            a = run * prog(t, T["dumps"] - 0.1, T["dumps"] + 0.3)
            add_glow(c, 640, -215, 150, "#FF7A3D", 0.45 * a)
            wisps(c, 612, -235, 800, -270, t, WARM, n=10, a=a, spread=50, speed=1.0, seed=1, w=9)
            wisps(c, 612, -190, 790, -150, t, "#F87171", n=8, a=a * 0.9, spread=40, speed=1.1, seed=4, w=8)
        # ---- air in the room: warm in, cool out
        if t >= T["drinks"] - 0.2 and covered_in < 1:
            a_in = prog(t, T["drinks"] - 0.2, T["drinks"] + 0.2) * (1 if not loop else run) * (1 - prog(t, T["full"], T["full"] + 0.5) if not loop else 1)
            wisps(c, -40, -250, 110, -400, t, WARM, n=6, a=a_in * 0.9, spread=34, speed=0.7, seed=3, w=6)
        cool_a = self.fank.at(t) * (prog(t, T["liquid"], T["boils"]) if not loop else run)
        if not loop:
            cool_a *= 1 - prog(t, T["allgas"] - 0.3, T["allgas"] + 0.2)
            wisps(c, 160, -340, 70, -236, t, WARM, n=6, a=prog(t, T["allgas"], T["allgas"] + 0.4) * 0.9, spread=32, speed=0.8, seed=6, w=6)
        wisps(c, 170, -340, 70, -236, t, COOL, n=7, a=cool_a, spread=34, speed=0.9, seed=8, w=7)
        wisps(c, 230, -340, 250, -236, t, COOL, n=5, a=cool_a * 0.8, spread=26, speed=0.9, seed=9, w=6)
        # ---- icicles on the coil
        if fr > 0:
            for i in range(9):
                ix = 92 + i * 24
                ih = (18 + (i * 37) % 30) * fr
                p = skia.Path()
                p.moveTo(ix - 6, -364)
                p.lineTo(ix + 6, -364)
                p.lineTo(ix, -364 + ih)
                p.close()
                c.drawPath(p, P("#E0F2FE", 0.95))
            c.drawRRect(rr(74, -470, 236, 112, 18), P("#E0F2FE", 0.35 * fr))
        # ---- break 4: the drip.  fix 4: tray, drain, filter
        tray = e_back(prog(t, T["tray"] - 0.15, T["tray"] + 0.1))
        if t >= T["water"] - 0.1 and tray <= 0 and t < s("fix4") - 0.12:
            for i in range(3):
                u = ((t - T["water"]) * 1.5 + i / 3) % 1.0
                if t - T["water"] + 0.1 < i / 4.5:
                    continue
                dx = 150 + i * 40
                y = lerp(-352, SEAT - 6, e_in(u))
                c.drawOval(R(dx - 5, y - 9, 10, 15), P("#38BDF8"))
        if t >= s("fix4") - 0.12:
            wet_t = t - T["water2"]
            for i in range(10):                                                      # water condensing on the cold coil
                bx = 96 + i * 21
                u = (t * 0.9 + i * 0.31) % 1.0
                by = lerp(-440 + (i % 3) * 26, -350, e_in(u)) if wet_t > -0.4 else -440 + (i % 3) * 26
                if covered_in < 0.5:
                    c.drawOval(R(bx - 3.5, by - 6, 7, 10), P("#7DD3FC", 0.95))
            if tray > 0:
                c.save()
                c.translate(187, -340)
                c.scale(tray, tray)
                c.drawRRect(rr(-125, -6, 250, 16, 6), P("#94A3B8"))
                c.drawRRect(rr(-119, -6, 238, 9, 4), P("#38BDF8", clamp(wet_t + 0.2)))
                c.restore()
            dk = prog(t, T["drain"] - 0.1, T["drain"] + 0.55)
            if dk > 0:
                dl = Line([(312, -334), (478, -334), (478, -320)])
                pr = P("#E5E9F2", 1, stroke=10)
                pr.setStrokeCap(skia.Paint.kRound_Cap)
                pr.setStrokeJoin(skia.Paint.kRound_Join)
                c.drawPath(dl.path(0.0, dl.len * dk), pr)
                if dk >= 1 and wet_t > 0.2:
                    for i in range(3):
                        d = ((t * 0.9 + i / 3) % 1.0) * dl.len
                        x, y = dl.at(d)
                        c.drawCircle(x, y, 3, P("#38BDF8"))
                    u = (t * 1.6) % 1.0
                    c.drawOval(R(474, lerp(-318, -300 if covered_out < 0.5 else -306, u) - 6, 8, 12), P("#38BDF8"))
            grow = e_back(prog(t, T["air"] - 0.3, T["air"] + 0.5)) if t < s("cta") + 2 else 1.0
            pot_a = prog(t, T["drain"] + 0.2, T["drain"] + 0.5)
            if pot_a > 0:                                                            # a thirsty plant on top of the box outside
                p = skia.Path()
                p.moveTo(460, -324)
                p.lineTo(500, -324)
                p.lineTo(494, -300)
                p.lineTo(466, -300)
                p.close()
                c.drawPath(p, P("#C2410C", pot_a))
                c.drawLine(480, -324, 480, -324 - 34 * grow, P("#22C55E", pot_a, stroke=5))
                for sd in (-1, 1):
                    c.drawOval(R(480 + (2 if sd > 0 else -22) * 1.0, -346 - 6, 20 * grow, 10 * grow), P("#22C55E", pot_a * clamp(grow)))
                if grow > 0.6:
                    for i in range(5):
                        an = math.radians(i * 72 + t * 20)
                        c.drawCircle(480 + math.cos(an) * 9 * grow, -362 * 1.0 + math.sin(an) * 9 * grow, 6.5 * grow, P("#F472B6", pot_a))
                    c.drawCircle(480, -362, 5 * grow, P("#FDE047", pot_a))
            fk = e_out(prog(t, T["filter"] - 0.2, T["filter"] + 0.25))
            if fk > 0 and covered_in < 0.5:
                c.save()
                c.translate(0, -150 * (1 - fk))
                c.drawRRect(rr(70, -474, 240, 122, 10), P("#CBD5E1", 0.20 * fk))
                for gx in range(82, 310, 14):
                    c.drawLine(gx, -470, gx, -356, P("#E5E9F2", 0.45 * fk, stroke=1.5))
                for gy in range(-466, -354, 14):
                    c.drawLine(74, gy, 306, gy, P("#E5E9F2", 0.45 * fk, stroke=1.5))
                c.drawRRect(rr(70, -474, 240, 122, 10), P("#F8FAFC", 0.9 * fk, stroke=4))
                c.restore()
                rng = random.Random(8)
                for i in range(18):                                                  # dust flies in and sticks
                    t0 = T["catches"] - 0.3 + i * 0.05
                    u = e_out(prog(t, t0, t0 + 0.5))
                    tx, ty = rng.uniform(84, 296), rng.uniform(-462, -362)
                    sx, sy = tx - rng.uniform(200, 320), ty + rng.uniform(60, 200)
                    if u > 0:
                        c.drawCircle(lerp(sx, tx, u), lerp(sy, ty, u), rng.uniform(3, 5.5), P("#A8A29E", 0.95))
        # ---- the covers (the reveal)
        if covered_out > 0:
            c.save()
            c.translate(520, -215)
            c.scale(covered_out, covered_out)
            c.drawRRect(rr(-92, -87, 184, 174, 12), lin_paint(0, -87, 0, 87, ["#F1F5F9", "#CBD5E1", "#94A3B8"]))
            c.drawCircle(30, -2, 62, P("#1B2238"))
            fan(c, 30, -2, 56, self.ph_run(t) * 620, 1.0, guard=False, col="#64748B")
            for i in range(6):
                c.drawCircle(30, -2, 10 + i * 10, P("#E5E9F2", 0.9, stroke=2.5))
            for an in (0, 45, 90, 135):
                dx, dy = math.cos(math.radians(an)) * 62, math.sin(math.radians(an)) * 62
                c.drawLine(30 - dx, -2 - dy, 30 + dx, -2 + dy, P("#E5E9F2", 0.9, stroke=2.5))
            for i in range(5):
                c.drawRect(R(-80, -70 + i * 14, 36, 5), P("#64748B", 0.8))
            c.restore()
        if covered_in > 0:
            c.save()
            c.translate(187, -410)
            c.scale(covered_in, covered_in)
            c.drawRRect(rr(-131, -76, 262, 150, 30), lin_paint(0, -76, 0, 74, ["#FFFFFF", "#E2E8F0", "#B6C2D4"]))
            c.drawRRect(rr(-112, 46, 224, 14, 7), P("#1B2238"))
            c.drawRRect(rr(-112, -52, 224, 6, 3), P("#94A3B8", 0.6))
            c.drawCircle(104, 28, 5, P(GOOD))
            c.restore()

    # ------------------------------------------------------------------ everything else in the room
    def furniture(self, c, t):
        T, s = self.T, self.tl.s
        fr = self.frost.at(t)
        if t < s("fix1") - 0.12:                                                     # the hook: a fan, a block of ice
            box(c, -150, -70, 170, 12, "#8B5E3C", r=4)
            for tx in (-136, 6):
                c.drawRect(R(tx - 4, -58, 8, 58), P("#5B3A22"))
            melt = 1 - e_io(prog(t, T["melts"] - 0.15, T["puddle"] - 0.1))
            pud = e_out(prog(t, T["melts"] + 0.1, T["puddle"] + 0.2))
            if pud > 0:
                c.drawOval(R(-96 - 150 * pud, -6, 300 * pud, 22 * pud), P("#38BDF8", 0.85))
                c.drawOval(R(-96 - 100 * pud, -3, 120 * pud, 8 * pud), P("#FFFFFF", 0.35))
                for i in range(3):
                    u = (t * 1.7 + i / 3) % 1.0
                    c.drawOval(R(-128 + i * 30, lerp(-62, -8, e_in(u)) - 6, 8, 12), P("#38BDF8", 0.9 * clamp(melt * 3) if melt > 0.02 else 0.0))
            cold = t >= T["land"] and melt > 0.25
            col = COOL if cold else WARM
            wisps(c, -60, -150, -300, -150, t, col, n=9, a=0.95, spread=46, speed=0.9, seed=1, w=8)
            wisps(c, -60, -120, -290, -90, t, col, n=5, a=0.8, spread=30, speed=1.0, seed=2, w=7)
            # the fan on its stand
            c.drawRect(R(-12, -112, 8, 44), P("#94A3B8"))
            c.drawRRect(rr(-34, -78, 52, 10, 5), P("#64748B"))
            fan(c, -8, -150, 46, self.ph_fan(t) * 700)
            # the ice
            drop = e_in(prog(t, T["block"] - 0.45, T["land"]))
            iy = lerp(-640, -70, drop)
            if melt > 0.02:
                sq = 1 + 0.12 * bump(t, T["land"], T["land"] + 0.25)
                wdt, hgt = 72 * (0.5 + 0.5 * melt) * sq, 64 * melt / sq
                c.drawRRect(rr(-96 - wdt / 2, iy - hgt, wdt, hgt, 8), lin_paint(0, iy - hgt, 0, iy, [("#E0F2FE", 0.95), ("#7DD3FC", 0.9), ("#38BDF8", 0.85)]))
                c.drawRRect(rr(-96 - wdt / 2 + 6, iy - hgt + 6, wdt * 0.3, hgt * 0.5, 4), P("#FFFFFF", 0.6))
                if cold:
                    add_glow(c, -96, iy - hgt / 2, 90, "#7DD3FC", 0.4)
        couch(c, wet=e_out(prog(t, T["couch"] - 0.5, T["couch"] + 0.3)) * (1 - prog(t, self.tl.s("fix4"), self.tl.s("fix4") + 1.5)), snow=fr)

    def thermostat(self, c, t):
        T = self.T
        tk = e_back(prog(t, T["thermostat"] - 0.2, T["thermostat"] + 0.1))
        if tk > 0 and t < self.tl.s("tag") - 0.2:
            c.save()
            c.translate(-70, -300)
            c.scale(tk, tk)
            c.drawCircle(0, 0, 44, lin_paint(-44, -44, 44, 44, ["#FFFFFF", "#CBD5E1", "#64748B"]))
            c.drawCircle(0, 0, 34, P("#0B1220"))
            on = self.runk.at(t) > 0.5
            c.drawArc(R(-28, -28, 56, 56), 140, 260, False, P("#334155", 1, stroke=5))
            c.drawArc(R(-28, -28, 56, 56), 140, 150, False, P(GOOD if on else "#F59E0B", 1, stroke=5))
            text(c, "75" if self.lang == "en" else "24", 0, 10, 28, "#FFFFFF", "Poppins-Black")
            c.drawCircle(0, 22, 4, P(GOOD if on else "#EF4444"))
            c.restore()

    def people(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        fr = self.frost.at(t)
        if t < s("fix1") - 0.12:
            hot = t >= T["melts"] + 0.3
            self.crew(c, t, "shrug" if t >= T["puddle"] else "duck" if hot else "cheer" if t >= T["congrats"] - 0.1 else "look", xs=(-338, -290, -242), face=1)
            if t < T["land"] or hot:                                                 # sweat
                for i, px in enumerate((-338, -290, -242)):
                    u = (t * 1.3 + i * 0.4) % 1.0
                    c.drawOval(R(px + 14, -128 + u * 30, 6, 9), P("#7DD3FC", 1 - u))
            return
        if t >= s("tag") - 0.2:                                                      # dad, and whoever left the door open
            dk = self.doork(t)
            jump = bump(t, T["close"], T["close"] + 0.3) * 16
            kx = lerp(-470, -400, e_out(prog(t, T["door"] + 0.1, T["slam"])))
            person(c, kx, -jump, 96, "#FACC15", t * 1.4, "cheer" if t < T["close"] else "duck" if t < T["slam"] + 0.2 else "shrug", face=-1 if t < T["close"] else 1,
                   hair="#2B2530", pants="#2563EB")
            dx = lerp(-90, -215, e_out(prog(t, s("tag") - 0.1, T["dad"] + 0.2)))
            person(c, dx, 0, 134, "#10B981", t * 1.2, "walk" if t < T["dad"] else "point" if t < T["slam"] + 0.25 else "shrug", face=-1, hair="#9CA3AF", pants="#334155")
            c.drawRRect(rr(dx - 15, -111, 20, 5, 2.5), P("#4B5563"))                  # his moustache
            return
        # the crew on the couch
        cold = fr > 0.3
        sit_y = SEAT
        pose = "sit"
        jit = math.sin(t * 40) * 2.5 if cold else 0.0
        arms = "sit"
        if s("cta") <= t < s("reveal") - 0.1:
            arms = "sit"
        for i, (px, col) in enumerate(zip(COUCH_X, SHIRTS)):
            engineer(c, px + jit * (1 if i % 2 else -1), sit_y, 112 + (i % 2) * 6, col, t + i * 0.37, pose, face=-1)
            if cold:                                                                 # breath
                u = (t * 0.9 + i * 0.3) % 1.0
                puff(c, px - 26 - u * 26, sit_y - 96 - u * 18, 8 + 10 * u, "#E0F2FE", 0.7 * (1 - u), k=i)
        if T["couch"] - 0.35 <= t < s("fix4") - 0.12:                                 # an umbrella, indoors
            uk = e_back(prog(t, T["couch"] - 0.35, T["couch"] - 0.05))
            ux, uy = 190, sit_y - 150
            c.drawLine(ux, sit_y - 70, ux, uy, P("#E5E9F2", uk, stroke=5))
            p = skia.Path()
            p.moveTo(ux - 100 * uk, uy + 6)
            p.quadTo(ux, uy - 86 * uk, ux + 100 * uk, uy + 6)
            p.close()
            c.drawPath(p, P("#F43F5E", uk))
            for k in (-50, 0, 50):
                c.drawLine(ux + k * uk, uy + 6, ux, uy - 40 * uk, P("#9F1239", uk, stroke=2))
        # the remote
        if s("cta") <= t < s("reveal") - 0.1:
            lift = e_back(prog(t, T["grab"] - 0.2, T["grab"] + 0.1))
            remote(c, 100, -112 - 10 * lift, -14, 1.0, 1.25)
            if lift > 0 and t < T["follow"] + 1.0:
                u = (t * 1.2) % 1.0
                c.drawCircle(100, -116, 26 + 30 * u, P(HILITE, 0.9 * (1 - u), stroke=4))
        elif T["losecut"] <= t < self.tl.s("stat") + 5 and t < T["s1"] - 0.35:
            sink = e_in(prog(t, T["lose"] - 0.1, T["remote2"] + 0.1))
            c.save()
            c.clipRect(R(60, -400, 300, 400 + SEAT))
            remote(c, 160 + 0 * sink, lerp(-92, SEAT + 34, sink), lerp(-20, 80, sink), 1.0, 1.25)
            c.restore()
            qk = e_back(prog(t, T["remote2"] + 0.05, T["remote2"] + 0.3))
            for i, px in enumerate(COUCH_X):
                text(c, "?", px + 4, SEAT - 138 - 8 * math.sin(t * 5 + i), 44 * qk, HILITE, "Poppins-Black", a=clamp(qk))

    def penguins(self, c, t):
        T, s = self.T, self.tl.s
        if not T["living"] - 0.3 <= t < s("break4") - 0.12:
            return
        pk = prog(t, T["living"] - 0.3, T["penguin"] + 0.3)
        out = e_in(prog(t, T["off"] + 0.1, T["pick"] + 0.5))                          # it warms up: they go home
        for i, (tx, sc) in enumerate(((-210, 1.0), (-120, 0.85), (-30, 1.1))):
            x = lerp(ROOM_L - 60 - i * 70, tx, e_out(clamp(pk * 1.25 - i * 0.12)))
            x = lerp(x, ROOM_L - 120 - i * 40, clamp(out * 1.2 - i * 0.1))
            penguin(c, x, 0, sc, t, 1 if out <= 0 else -1, slide=(i == 1 and pk < 0.75))

    # ------------------------------------------------------------------ sets
    def world(self, c, t, cam):
        cx, cy, z = cam
        cam = (cx + math.sin(t * 0.6) * (3 if z < 2 else 1.5), cy, z)
        self.backdrop(c, t, cam)
        self.view(c, cam)
        v2.ground(c, -3400, 3400)
        self.house(c, t)
        s = self.tl.s
        tech = self.mode(t) == "unit"                                                # the machine view: no couch, no crew
        self.thermostat(c, t)
        if not tech:
            self.furniture(c, t)
        self.machine(c, t)
        if not tech:
            self.people(c, t)
        self.penguins(c, t)
        if t >= self.T["cong2"] and self.mode(t) == "wide":
            hats_in_the_air(c, COUCH_X, SEAT - 150, t, self.T["cong2"])
        c.restore()
        self.ui["cam"] = cam

    def draw_room(self, c, t):
        self.world(c, t, self.cams["room"].at(t))

    def draw_unit(self, c, t):
        self.world(c, t, self.cams["unit"].at(t))

    def draw_wide(self, c, t):
        self.world(c, t, self.cams["wide"].at(t))

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -200, 1.4)), x, y)

    def thermo(self, c, t, tw):
        """The room temperature, always on screen under the title bar."""
        deg = self.temp.at(tw)
        col = mix(LIQ, "#FFFFFF", 0.2) if deg < 12 else GOOD if deg < 27.5 else mix("#F59E0B", HOT, clamp((deg - 28) / 8))
        x = 906 if self.rtl else 174
        a = prog(t, 0.25, 0.6) * (1 - self.span(self.T["follow"] - 0.3, self.tl.s("reveal") + 0.2))
        if a <= 0:
            return
        c.drawRRect(rr(x - 104, 208, 208, 66, 33), P("#0B1024", 0.78 * a))
        c.drawRRect(rr(x - 104, 208, 208, 66, 33), P(col, 0.9 * a, stroke=3))
        c.drawRRect(rr(x - 80, 220, 12, 34, 6), P("#E5E9F2", a))
        fill = clamp((deg + 8) / 50)
        c.drawRRect(rr(x - 77, 250 - 28 * fill, 6, 28 * fill + 2, 3), P(col, a))
        c.drawCircle(x - 74, 256, 10, P(col, a))
        val = int(round(deg * 9 / 5 + 32)) if self.lang == "en" else int(round(deg))
        text(c, f"{val}°" + ("F" if self.lang == "en" else ""), x + 22, 257, 40, "#FFFFFF", "Poppins-Black", a=a)

    def ui_room(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        self.thermo(c, t, tw)
        if tw < s("break1") - 0.1:
            x0, y0 = self.at(-96, -134)
            self.label(x0, y0, x0 + 150, y0 - 330, "ice", T["land"] + 0.1, T["congrats"] + 0.3, COOL)
        elif tw < s("fix1") - 0.12:
            self.chip(540, 420, "hour", T["hour"] - 0.25, T["puddle"] - 0.1, accent=WARN, size=44)
            self.badge("alert", T["melts"] + 0.2, s("fix1") - 0.2)
            self.red(T["melts"] + 0.2, 1.8)
        elif tw < s("fix3") - 0.12:
            self.badge("alert", T["stops"], s("fix3") - 0.2)
            self.red(T["stops"], 1.8)
        elif tw < s("fix4") - 0.12:
            self.badge("alert", T["dripping"], s("fix4") - 0.2)
            self.red(T["dripping"], 1.8)
        elif tw < s("reveal") - 0.1:
            x0, y0 = self.at(100, -150)
            self.label(x0, y0, x0 + 120, y0 - 300, "remote", T["remote"] - 0.1, s("reveal") - 0.3, HILITE)
        elif tw < T["s1"] - 0.35:
            x0, y0 = self.at(160, SEAT - 6)
            self.label(x0, y0, x0 + 190, y0 - 420, "lost", T["remote2"], T["s1"] - 0.5, WARN)
        elif tw >= s("tag") - 0.2:
            x0, y0 = self.at(-560, -150)
            self.label(x0, y0, x0 + 60, y0 - 300, "hot", T["cooling"] - 0.1, self.duration + 1, WARN)

    def ui_unit(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        self.thermo(c, t, tw)
        if tw < s("break2"):
            x0, y0 = self.at(120, -456)
            self.label(x0, y0, x0 + 40, y0 - 200, "coil", T["coil0"] - 0.1, T["drinks"] - 0.1, COOL)
            x1, y1 = self.at(250, -372)
            self.label(x1, y1, x1 + 60, y1 + 190, "boil", T["boils"] - 0.05, T["coil0"] - 0.2, LIQ)
            self.badge("check", T["room1"], s("break2") - 0.15)
        elif tw < s("fix2") - 0.1:
            x0, y0 = self.at(120, -456)
            self.label(x0, y0, x0 + 60, y0 - 200, "full", T["full"], T["nowhere"] - 0.15, HOT)
            x1, y1 = self.at(306, -414)
            self.label(x1, y1, x1 - 20, y1 + 300, "nowhere", T["nowhere"], s("fix2") - 0.2, WARN)
            self.badge("alert", T["allgas"], s("fix2") - 0.2)
            self.red(T["allgas"], 1.8)
        elif tw < s("break3"):
            x0, y0 = self.at(462, -252)
            self.label(x0, y0, x0 + 130, y0 - 230, "comp", T["compressor"] + 0.1, T["second"] - 0.2, "#F59E0B")
            x1, y1 = self.at(545, -290)
            self.label(x1, y1, x1 + 40, y1 - 190, "coil2", T["second"] + 0.2, T["dumps"] - 0.1, HOT)
            self.chip(800, 800, "street", T["dumps"] + 0.1, s("break3") - 0.25, accent=WARM, size=34)
            self.badge("check", T["street"], s("break3") - 0.15, x=880, y=420)
        elif tw < s("break4"):
            x0, y0 = self.at(-70, -346)
            self.label(x0, y0, x0 + 60, y0 - 190, "thermo", T["thermostat"] + 0.1, T["off"] - 0.15, HILITE)
            off = T["off"] <= tw < T["on"]
            if tw >= T["off"] - 0.05:
                p = self.span(T["off"] - 0.05, s("break4") - 0.2)
                x1, y1 = self.at(187, -500)
                v2.chip(c, x1, y1 - 30, self.L["off" if off else "on"], p, size=44, accent=WARN if off else GOOD)
            if T["pick"] - 0.2 <= tw < T["pick"] + 0.6:                                # a tap on the dial
                x2, y2 = self.at(-70, -300)
                u = prog(tw, T["pick"] - 0.2, T["pick"] + 0.5)
                c.drawCircle(x2, y2, 40 + 90 * u, P("#FFFFFF", 0.9 * (1 - u), stroke=6))
            self.badge("check", T["warms"], s("break4") - 0.15, x=880, y=420)
        elif tw < s("cta"):
            x0, y0 = self.at(100, -336)
            self.label(x0, y0, x0 - 20, y0 + 210, "tray", T["tray"] + 0.1, T["drain"] - 0.1, "#94A3B8")
            x1, y1 = self.at(420, -334)
            self.label(x1, y1, x1 + 30, y1 - 250, "drain", T["drain"] + 0.3, T["air"] - 0.1, LIQ)
            x2, y2 = self.at(110, -470)
            self.label(x2, y2, x2 + 80, y2 - 190, "filter", T["filter"] + 0.15, T["catches"] + 0.1, "#F8FAFC")
            x3, y3 = self.at(250, -380)
            self.label(x3, y3, x3 + 90, y3 + 300, "dust", T["dust"] - 0.15, s("cta") - 0.3, "#A8A29E")
            self.badge("check", T["dust"], s("cta") - 0.15, x=880, y=420)

    def ui_wide(self, c, t, tw):
        self.thermo(c, t, tw)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.whirr(1.6, 120, 150, 61), -14), (T["block"] - 0.45, sfx.whoosh(0.35, False, 62), -12),
              (T["land"], sfx.thud(0.3, 63), -4), (T["land"] + 0.1, sfx.sparkle(0.6, 8, 64), -9), (T["congrats"] + 0.1, sfx.chime(), -8)]
        ev += [(T["melts"] + i * 0.3, drip_snd(i), -8) for i in range(5)]
        ev += [(T["melts"] + 0.2, sfx.alarm(3, 820), -11), (T["hour"] - 0.25, sfx.tick(), -6), (T["hour"] - 0.05, sfx.tick(), -6),
               (T["puddle"], sfx.pop(65), -7), (T["warm"] + 0.3, sfx.womp(), -10)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["swap"], sfx.pop(67), -6), (T["liquid"] - 0.15, drip_snd(3), -6),
               (T["boils"], sfx.sizzle(0.8, 68), -12), (T["coil0"], sfx.sparkle(0.6, 8, 69), -9), (T["drinks"], wind_snd(1.0, 4), -12),
               (T["room1"], sfx.chime(), -6)]
        ev += [(T["liquid2"], sfx.sizzle(0.7, 70), -12), (T["allgas"], sfx.alarm(3, 820), -10), (T["full"], sfx.riser(0.9, 71), -12),
               (T["nowhere"], sfx.buzz(0.35), -8)]
        ev += [(s("fix2") - 0.1, sfx.whoosh(0.5, True, 72), -6), (T["compressor"] - 0.2, sfx.thud(0.3, 73), -4), (T["squeezes"], hum_snd(1.6), -7),
               (T["second"] - 0.4, sfx.clank(520, 0.25, 74), -8), (T["second"], sfx.pop(75), -6), (T["fan2"] - 0.2, sfx.whirr(1.2, 140, 220, 76), -11),
               (T["dumps"], wind_snd(1.2, 5, 200, 1600), -9), (T["street"], sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 77), -4), (T["never"], sfx.sparkle(1.2, 16, 78), -7), (T["stops"], sfx.alarm(3, 820), -10),
               (T["living"] - 0.2, squawk(0), -7), (T["penguin"] + 0.25, squawk(2), -5), (T["penguin"] + 0.6, squawk(1), -7)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["thermostat"] - 0.2, sfx.pop(80), -5), (T["off"], sfx.power_down(0.8, 81), -9),
               (T["off"], sfx.click(82), -3), (T["pick"] - 0.2, sfx.beep(1500, 0.07), -7), (T["pick"] - 0.05, sfx.beep(1900, 0.07), -7),
               (T["on"], sfx.click(83), -3), (T["on"] + 0.05, sfx.charge_up(0.6), -11), (T["warms"], sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 84), -4), (T["perfect"], sfx.sparkle(0.6, 8, 85), -10)]
        ev += [(T["water"] + i * 0.33, drip_snd(i % 4), -5) for i in range(int(max(2, (s("fix4") - T["water"]) / 0.33)))]
        ev += [(T["dripping"], sfx.alarm(3, 820), -11), (T["couch"] - 0.35, sfx.pop(86), -5)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 87), -4), (T["tray"] - 0.15, sfx.clank(700, 0.2, 88), -7), (T["drain"] - 0.1, sfx.whoosh(0.4, True, 89), -11),
               (T["water2"], drip_snd(1), -6), (T["water2"] + 0.4, drip_snd(2), -7), (T["air"], sfx.sparkle(0.6, 8, 90), -8),
               (T["filter"] - 0.2, sfx.whoosh(0.35, False, 91), -8), (T["filter"] + 0.2, sfx.thunk(92), -6)]
        ev += [(T["catches"] - 0.3 + i * 0.1, sfx.tap(93 + i), -12) for i in range(6)]
        ev += [(T["dust"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(100), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 101), -7), (T["grab"] - 0.2, sfx.pop(102), -6),
               (T["follow"] - 0.15, sfx.pop(103), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 104), -6), (T["hide"] - 0.1, sfx.thunk(105), -4), (T["hang"] - 0.1, sfx.thunk(106), -4),
               (T["wall2"], sfx.beep(1700, 0.09), -6), (T["losecut"], sfx.whoosh(0.35, False, 107), -7), (T["lose"], sfx.whoosh(0.3, False, 108), -10),
               (T["remote2"] + 0.1, sfx.pop(109), -6)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 110), -6), (T["s1"], sfx.pop(111), -3), (T["s2"], sfx.pop(112), -3), (T["s3"], sfx.pop(113), -3)]
        ev += [(T["cong2"], sfx.pop(114), -2), (T["cong2"], sfx.sparkle(1.0, 14, 115), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 116), -6), (s("tag") - 0.1, wind_snd(1.6, 6), -12), (T["close"], sfx.pop(117), -6),
               (T["slam"], sfx.thud(0.35, 118), -1), (T["slam"] + 0.3, sfx.womp(), -3)]
        return ev


BRASS_ = "#D4A84B"
NAME = "aircon"
EPISODE = Aircon
