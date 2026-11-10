"""Episode 10 - A toilet.  v2 look: one small house cut open, four cameras with whip cuts.

World (floor at y = 0): the bathroom is x -330..360, y -480..0.  The toilet stands in profile, cut open: tank on the
left wall (x -178..-42, y -352..-162), bowl and pedestal to its right (x -74..140), the trapway inside the pedestal
down to the flange at (112, 0).  Under the floor the drain drops to y = 205 and runs left to the sewer; the vent
pipe rises at x = -300 through the roof.  Cameras: room, trap (inside the pedestal), tank (inside the tank), house.
"""
from v2_base import *  # noqa: F401,F403

PORC, WATER, GASC = "#F1F5F9", "#38BDF8", "#A3E635"
TB, TF = -178.0, -296.0                        # tank: inside bottom, fill line (level 1.0)
SEW_Y, VENT_X = 205, -300
XS = (176, 214, 252)                           # where the crew stands in the bathroom


def cubic(p0, p1, p2, p3, n=14):
    out = []
    for i in range(n + 1):
        u = i / n
        a, b, c_, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        out.append((a * p0[0] + b * p1[0] + c_ * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c_ * p2[1] + d * p3[1]))
    return out


TRAP = (cubic((20, -70), (22, -26), (64, -20), (74, -62)) + cubic((74, -62), (82, -100), (86, -120), (98, -112))[1:]
        + cubic((98, -112), (114, -104), (112, -60), (112, 0))[1:])            # the S: dip, weir, down to the floor
STRAIGHT = [(20, -70), (60, -44), (112, -16), (112, 0)]
DRAIN = [(112, 0), (112, SEW_Y), (-620, SEW_Y)]
PASSAGE = [(-110, TB), (-110, -160), (-76, -150), (-40, -140), (10, -100)]


def along(pts, u):
    """The point at fraction u of a polyline."""
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    d = clamp(u) * sum(segs)
    for i, sl in enumerate(segs):
        if d <= sl or i == len(segs) - 1:
            k = clamp(d / sl) if sl else 0.0
            return lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)
        d -= sl


def poly_path(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    return p


def stream(c, pts, t, col, n=10, speed=0.7, r=7, a=1.0, lo=0.0, hi=1.0, gas=False):
    """Blobs running along a polyline (water) or drifting puffs (gas). Only the stretch lo..hi of the line carries them."""
    if a <= 0 or hi <= lo:
        return
    for i in range(n):
        u = (t * speed + i / n) % 1.0
        if not lo <= u <= hi:
            continue
        x, y = along(pts, u)
        if gas:
            puff(c, x + math.sin(t * 3 + i) * 4, y + math.cos(t * 2.3 + i) * 4, r * (0.8 + 0.25 * (i % 3)), col, a * 0.85, k=i)
        else:
            c.drawCircle(x, y, r * (0.75 + 0.25 * (i % 2)), P(col, a))


def bird(c, x, y, t, fly=0.0, s=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if fly > 0:
        fl = math.sin(t * 22) * 14
        for sd in (-1, 1):
            w = skia.Path()
            w.moveTo(0, -10)
            w.quadTo(sd * 16, -26 - fl, sd * 30, -12 + fl * 0.3)
            c.drawPath(w, P("#CBD5E1", 1, stroke=6))
    c.drawOval(R(-13, -22, 26, 22), P("#64748B"))
    c.drawOval(R(-11, -12, 16, 10), P("#94A3B8"))
    c.drawCircle(10, -24, 8, P("#64748B"))
    c.drawCircle(12, -26, 1.8, P("#0B1220"))
    bk = skia.Path()
    bk.moveTo(17, -26)
    bk.lineTo(27, -23)
    bk.lineTo(17, -20)
    bk.close()
    c.drawPath(bk, P("#FB923C"))
    if fly <= 0:
        c.drawLine(-3, 0, -3, 7, P("#FB923C", 1, stroke=2))
        c.drawLine(5, 0, 5, 7, P("#FB923C", 1, stroke=2))
    c.restore()


def flush_snd(d=1.6, seed=50):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 250, 3600) * (0.55 + 0.45 * np.sin(2 * np.pi * 7 * tt))
    return sfx._norm(x * sfx._ar(n, 0.05, d * 0.45), 0.8)


def glug(seed=0):
    n = int(0.22 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 170 + 260 * tt / 0.22 + seed * 30
    return sfx._norm(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * sfx._ar(n, 0.01, 0.08), 0.8)


def drip_snd(d=0.5, seed=60):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 500, 5000)
    return sfx._norm(x * sfx._env(n, 0.004, d * 0.28), 0.8)


# ====================================================================================== the episode
class Toilet(EpisodeV2):
    BUILD_NO = 10
    FIRST_SET = "room"
    CLEAR = "#0B1024"
    TITLE = {"en": "TOILET", "ar_sa": "كرسي حمام"}
    EMPH = {"en": ["CONGRATS", "TOILET", "BUCKET", "NOBODY", "TANK", "FLAPPER", "GRAVITY", "SEWER", "SMELL", "TRAP", "SEALS", "GAS",
                   "REFILL", "POOL", "FLOAT", "VALVE", "OVERFLOW", "DRY", "GLUG", "VENT", "ROOF", "BIRDS", "FOLLOW", "AIRPLANE", "LID",
                   "LOCK", "SHAMPOO", "ZERO", "YOURSELF", "ECONOMISTS", "PAPERS", "WINNER"],
            "ar_sa": ["مبروك", "حمام", "سطل", "ومحد", "خزان", "سدادة", "والجاذبية", "المجاري", "ريحة", "مصيدة", "وتسد", "الغاز",
                      "توقف", "مسبح", "عوّامة", "بلف", "للفايض", "اللفّة", "بق", "تهوية", "السطح", "للعصافير", "تابعني", "طيارة",
                      "غطا", "وقفل", "شامبو", "وصفر", "بيدك", "اقتصاد", "أبحاث", "فاز"]}
    KEYS = {"ar_sa": {
        ("hook", "SEAT"): "قاعدة", ("hook", "BUCKET"): "سطل", ("hook", "CONGRATS"): "مبروك",
        ("break1", "CARRY"): "يشيل", ("break1", "OUT"): "ويطلعه", ("break1", "NOBODY"): "ومحد", ("break1", "JOB"): "هالشغلة",
        ("fix1", "TANK"): "خزان", ("fix1", "BOWL"): "الكرسي", ("fix1", "FLAPPER"): "سدادة", ("fix1", "HANDLE"): "الزر",
        ("fix1", "GRAVITY"): "والجاذبية", ("fix1", "WORK"): "الوسخ",
        ("break2", "FLUSHES"): "يسحب", ("break2", "SEWER"): "المجاري", ("break2", "SMELL"): "ريحة", ("break2", "HELLO"): "وتسلّم",
        ("fix2", "BEND"): "فتلوي", ("fix2", "CALLED"): "يسمونها", ("fix2", "TRAP"): "مصيدة", ("fix2", "WATER"): "موية",
        ("fix2", "CURVE"): "فيها", ("fix2", "SEALS"): "وتسد", ("fix2", "GAS"): "الغاز",
        ("break3", "REFILL"): "تعبّي", ("break3", "STOPS"): "توقف", ("break3", "BATHROOM"): "حمامك", ("break3", "POOL"): "مسبح",
        ("fix3", "FLOAT"): "عوّامة", ("fix3", "FULL"): "امتلى", ("fix3", "SHUTS"): "تقفل", ("fix3", "VALVE"): "بلف",
        ("fix3", "OVERFLOW"): "للفايض", ("fix3", "CASE"): "احتياط",
        ("break4", "WORKS"): "يشتغل", ("break4", "RACING"): "النازلة", ("break4", "SUCKS"): "تسحب", ("break4", "DRY"): "اللفّة",
        ("break4", "GLUG"): "بق", ("break4", "SMELL"): "الريحة",
        ("fix4", "VENT"): "تهوية", ("fix4", "ROOF"): "السطح", ("fix4", "AIR"): "الهوا", ("fix4", "STAYS"): "تظل",
        ("fix4", "SMELL"): "والريحة", ("fix4", "TOP"): "تطلع", ("fix4", "SORRY"): "نعتذر", ("fix4", "BIRDS"): "للعصافير",
        ("cta", "SIT"): "تجلس", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "LID"): "غطا", ("reveal", "LOCK"): "وقفل", ("reveal", "SHAMPOO"): "شامبو", ("reveal", "READ"): "تقرا",
        ("stat", "ONE"): "ضغطة", ("stat", "SIX"): "ست", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SEAT"): "والقاعدة", ("tag", "UP"): "ترفعها", ("tag", "DOWN"): "تنزلها", ("tag", "ECONOMISTS"): "اقتصاد",
        ("tag", "PAPERS"): "أبحاث", ("tag", "WINNER"): "فاز"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an airplane"),
                   "stat": [("1", "PUSH"), ("6", "LITERS MAX"), ("0", "BUCKETS")],
                   "L": {"seat": "A SEAT", "tank": "WATER TANK", "flap": "RUBBER FLAPPER", "grav": "GRAVITY", "gas": "SEWER GAS",
                         "trap": "THE TRAP", "seal": "WATER SEAL", "float": "FLOAT", "valve": "FILL VALVE", "over": "OVERFLOW TUBE",
                         "dry": "TRAP: EMPTY", "vent": "VENT PIPE", "airin": "AIR IN", "full": "TRAP: FULL", "tie": "STILL A TIE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: طيارة"),
                      "stat": [("1", "ضغطة"), ("6", "لترات"), ("0", "سطول")],
                      "L": {"seat": "قاعدة", "tank": "خزان موية", "flap": "سدادة مطاط", "grav": "الجاذبية", "gas": "غاز المجاري",
                            "trap": "المصيدة", "seal": "موية تسد الطريق", "float": "عوّامة", "valve": "بلف الموية",
                            "over": "ماسورة الفايض", "dry": "المصيدة فاضية", "vent": "ماسورة تهوية", "airin": "هوا داخل",
                            "full": "المصيدة مليانة", "tie": "تعادل"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "seat": ("hook", "SEAT", 0.25), "bucket": ("hook", "BUCKET", 0.45), "congrats": ("hook", "CONGRATS", 0.6),
            "carry": ("break1", "CARRY", 0.3), "out": ("break1", "OUT", 0.5), "nobody": ("break1", "NOBODY", 0.65), "job": ("break1", "JOB", 0.9),
            "tank": ("fix1", "TANK", 0.12), "bowl": ("fix1", "BOWL", 0.3), "flapper": ("fix1", "FLAPPER", 0.46), "handle": ("fix1", "HANDLE", 0.7),
            "gravity": ("fix1", "GRAVITY", 0.78), "work": ("fix1", "WORK", 0.96),
            "flushes": ("break2", "FLUSHES", 0.15), "sewer": ("break2", "SEWER", 0.45), "smell": ("break2", "SMELL", 0.62), "hello": ("break2", "HELLO", 0.9),
            "bend": ("fix2", "BEND", 0.08), "called": ("fix2", "CALLED", 0.33), "trap": ("fix2", "TRAP", 0.42), "water": ("fix2", "WATER", 0.54),
            "curve": ("fix2", "CURVE", 0.74), "seals": ("fix2", "SEALS", 0.85), "gas": ("fix2", "GAS", 0.95),
            "refill": ("break3", "REFILL", 0.15), "stops": ("break3", "STOPS", 0.38), "bathroom": ("break3", "BATHROOM", 0.65), "pool": ("break3", "POOL", 0.93),
            "float": ("fix3", "FLOAT", 0.15), "full": ("fix3", "FULL", 0.36), "shuts": ("fix3", "SHUTS", 0.45), "valve": ("fix3", "VALVE", 0.58),
            "overflow": ("fix3", "OVERFLOW", 0.72), "case": ("fix3", "CASE", 0.95),
            "works": ("break4", "WORKS", 0.1), "racing": ("break4", "RACING", 0.3), "sucks": ("break4", "SUCKS", 0.48), "dry": ("break4", "DRY", 0.6),
            "glug": ("break4", "GLUG", 0.66), "smell2": ("break4", "SMELL", 0.84),
            "vent": ("fix4", "VENT", 0.14), "roof": ("fix4", "ROOF", 0.3), "air": ("fix4", "AIR", 0.34), "stays": ("fix4", "STAYS", 0.56),
            "smell3": ("fix4", "SMELL", 0.68), "top": ("fix4", "TOP", 0.82), "sorry": ("fix4", "SORRY", 0.87), "birds": ("fix4", "BIRDS", 0.94),
            "sit": ("cta", "SIT", 0.25), "follow": ("cta", "FOLLOW", 0.4),
            "lid": ("reveal", "LID", 0.25), "lock": ("reveal", "LOCK", 0.4), "shampoo": ("reveal", "SHAMPOO", 0.72), "read": ("reveal", "READ", 0.92),
            "s1": ("stat", "ONE", 0.04), "s2": ("stat", "SIX", 0.32), "s3": ("stat", "ZERO", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "seat2": ("tag", "SEAT", 0.12), "up": ("tag", "UP", 0.2), "down": ("tag", "DOWN", 0.28), "economists": ("tag", "ECONOMISTS", 0.36),
            "papers": ("tag", "PAPERS", 0.68), "winner": ("tag", "WINNER", 0.93)})
        T["land"] = T["seat"] + 0.22
        T["flush1"] = T["handle"] + 0.2
        T["gas1"] = min(T["sewer"], T["smell"]) - 0.1
        T["s"] = T["called"] - 0.45                                # the pipe is an S by now
        T["flood0"] = min(T["refill"], T["stops"]) - 0.2
        T["flush4"] = T["racing"] - 0.35
        T["empty"] = T["dry"] + 0.25
        T["flush5"] = T["air"] - 0.15
        T["poof"] = max(T["top"], T["smell3"] + 0.5)
        # ---- one world, four cameras. Floor line near screen y 1230 means camera y = -270 / zoom
        self.cut(s("fix1") - 0.12, "room", 1)
        self.cut(s("fix2") - 0.12, "trap", 1)
        self.cut(s("break3") - 0.1, "room", -1)
        self.cut(s("fix3") - 0.12, "tank", 1)
        self.cut(s("break4") - 0.12, "trap", -1)
        self.cut(s("fix4") - 0.12, "house", 1)
        self.cut(s("cta") + 0.05, "room", -1)
        self.cut(T["s1"] - 0.32, "house", 1)
        self.cut(s("tag") - 0.2, "room", -1)
        self.cams = {"room": Camera(110, -160, 1.7), "trap": Camera(64, -6, 3.0), "tank": Camera(-108, -203, 3.6),
                     "house": Camera(-60, -89, 0.9)}
        cm = self.cams
        cm["room"].key(0.05, 120, -150, 1.8, 1.4).key(s("break1"), 170, -160, 1.7, 1.0)
        cm["room"].key(s("fix1") - 0.12, 10, -180, 1.5, 0.0).key(T["flapper"] - 0.4, -10, -142, 1.9, 0.9)
        cm["room"].key(s("break2"), 20, -169, 1.6, 1.0)
        cm["room"].key(s("break3") - 0.1, 14, -180, 1.5, 0.0)
        cm["room"].key(s("cta") + 0.05, 60, -190, 1.42, 0.0).key(s("reveal") - 0.1, 80, -193, 1.4, 0.8)
        cm["room"].key(s("tag") - 0.2, 20, -140, 1.9, 0.0)
        cm["trap"].key(s("fix2") - 0.12, 64, -6, 3.0, 0.0).key(T["water"] - 0.3, 66, -14, 3.25, 0.9)
        cm["trap"].key(s("break4") - 0.12, 74, 10, 2.6, 0.0)
        cm["tank"].key(s("fix3") - 0.12, -108, -203, 3.6, 0.0).key(T["overflow"] - 0.3, -100, -210, 3.75, 0.7)
        cm["house"].key(s("fix4") - 0.12, -60, -89, 0.9, 0.0).key(T["smell3"] - 0.4, -200, -330, 1.2, 0.9)
        cm["house"].key(T["s1"] - 0.32, -30, -129, 0.62, 0.0).key(s("closer"), -60, -129, 0.66, 2.0)
        # ---- water levels and moving parts
        self.level = Track(1.0).to(T["flush1"], 0.12, 0.9, e_io).to(T["work"] + 0.2, 1.0, 1.4, e_io)
        self.level.to(T["flood0"], 1.42, 0.7).to(s("fix3") - 0.12, 0.22, 0.01).to(T["float"] + 0.2, 1.0, max(0.6, T["shuts"] - T["float"] - 0.2))
        self.level.to(T["case"] - 0.55, 1.13, 0.4).to(T["flush4"], 0.12, 0.9, e_io).to(T["empty"] + 0.3, 1.0, 1.5)
        self.level.to(T["flush5"], 0.12, 0.9, e_io).to(T["flush5"] + 1.3, 1.0, 1.6)
        self.flap = Track(0.0)
        for tf in (T["flush1"], T["flush4"], T["flush5"]):
            self.flap.to(tf - 0.05, 1.0, 0.12).to(tf + 1.0, 0.0, 0.2)
        self.flood = Track(0.0).to(T["flood0"] + 0.5, 1.0, max(0.8, T["pool"] - T["flood0"] - 0.4)).to(s("fix3") - 0.12, 0.0, 0.01)
        self.trapk = Track(0.0).to(T["bend"], 1.0, max(0.5, T["s"] - T["bend"]), e_io)           # straight pipe -> S
        self.trapw = Track(0.0).to(T["water"] - 0.2, 1.0, 0.7).to(T["sucks"], 0.0, max(0.4, T["empty"] - T["sucks"])).to(s("fix4") - 0.12, 1.0, 0.01)
        self.ventk = Track(0.0).to(T["vent"] - 0.1, 1.0, max(0.6, T["roof"] - T["vent"] + 0.3))
        self.lidk = Track(0.0).to(T["lid"], 1.0, 0.18, e_in).to(s("tag") - 0.2, 0.0, 0.01)
        self.seatk = Track(0.0).to(T["up"], 1.0, 0.18).to(T["down"], 0.0, 0.18)
        for i in range(8):
            self.seatk.to(T["economists"] + 0.2 + i * 0.42, 1.0 if i % 2 == 0 else 0.0, 0.2)
        self.doork = Track(0.0).to(T["lock"] - 0.3, 1.0, 0.3)
        self.spans = [(T["nobody"], T["work"]), (T["smell"], T["gas"]), (T["bathroom"], T["shuts"] + 0.3), (T["empty"], T["stays"] + 0.3)]
        self.shakes = [(T["land"], 0.2, 8), (T["flush1"], 0.4, 6), (T["flush4"], 0.4, 6), (T["lid"] + 0.18, 0.2, 8), (T["lock"], 0.15, 6)]

    # ------------------------------------------------------------------ helpers
    def flushing(self, t):
        """0..1 while a flush is running (water in the passage, the bowl and the drain)."""
        T = self.T
        for tf in (T["flush1"], T["flush4"], T["flush5"]):
            if tf <= t < tf + 1.5:
                return prog(t, tf, tf + 0.2) * (1 - prog(t, tf + 1.1, tf + 1.5))
        return 0.0

    def trap_pts(self, t):
        k = self.trapk.at(t)
        if k <= 0:
            return STRAIGHT
        if k >= 1:
            return TRAP
        n = len(TRAP)
        return [(lerp(along(STRAIGHT, i / (n - 1))[0], TRAP[i][0], k), lerp(along(STRAIGHT, i / (n - 1))[1], TRAP[i][1], k)) for i in range(n)]

    # ------------------------------------------------------------------ the house
    def house(self, c, t):
        T, s = self.T, self.tl.s
        lit = 1.0
        # under the floor: the drain, the branch to the sewer, the foot of the vent
        gasflow = t >= T["gas1"]
        buried_line(c, [(-900, SEW_Y), (112, SEW_Y)], GASC if gasflow else "#64748B", t, 0.5 if gasflow else 0.0, 30)
        buried_line(c, [(112, SEW_Y), (112, 26)], "#64748B", t, 0.0, 30)
        vk = self.ventk.at(t)
        if vk > 0:
            top = lerp(SEW_Y, -612, vk)
            c.drawLine(VENT_X, SEW_Y, VENT_X, max(top, 26), P("#0A0D1A", 0.9, stroke=26))
            c.drawLine(VENT_X, SEW_Y, VENT_X, max(top, 26), P("#334155", 1, stroke=20))
        # the room
        vrect(c, -330, -480, 690, 480, ["#3B4A6B", "#2E3A58", "#232C46"], [0.0, 0.5, 1.0])
        for ty in range(-240, 1, 40):                                                # tiles on the lower wall
            c.drawRect(R(-330, ty, 690, 2), P("#000000", 0.16))
        for tx in range(-330, 361, 46):
            c.drawRect(R(tx, -240, 2, 240), P("#000000", 0.14))
        c.drawRect(R(-330, -246, 690, 8), P("#7DD3FC", 0.55))
        window_night(c, 40, -430, 120, 110, t)
        c.drawRRect(rr(212, -336, 134, 336, 6), P("#1B2238"))                         # the door (in the back wall)
        dk = self.doork.at(t)
        c.save()
        c.clipRect(R(218, -330, 122, 330))
        vrect(c, 218, -330, 122, 330, ["#0B1020", "#141C36"])
        add_glow(c, 300, -200, 160, "#FFE9B8", 0.25 * (1 - dk))
        box(c, 218 + 122 * (1 - e_out(dk)), -330, 122, 330, "#7C5A3C", r=3)
        for py in (-300, -150):
            c.drawRRect(rr(232 + 122 * (1 - e_out(dk)), py, 94, 124, 5), P("#000000", 0.14))
        c.restore()
        if dk >= 1:
            locked = t >= T["lock"]
            c.drawRRect(rr(226, -196, 34, 22, 6), P("#E5E9F2"))
            c.drawCircle(243, -185, 7, P("#FF4D4F" if locked else GOOD))
            if locked:
                add_glow(c, 243, -185, 30, "#FF4D4F", 0.7)
        c.drawRect(R(-120, -480, 5, 34), P("#11151F"))                               # the lamp
        c.drawRRect(rr(-150, -448, 66, 16, 8), P("#FFF3C4"))
        add_glow(c, -117, -420, 330, "#FFE9B8", 0.30 * lit)
        box(c, -352, 0, 734, 26, "#4A5270")                                          # floor slab
        c.drawRect(R(-330, 0, 690, 3), P("#FFFFFF", 0.16))
        if vk > 0 and lerp(SEW_Y, -612, vk) < 0:                                     # the vent pipe up the wall and out
            top = lerp(SEW_Y, -612, vk)
            c.drawRect(R(VENT_X - 12, top, 24, -top), lin_paint(VENT_X - 12, 0, VENT_X + 12, 0, ["#CBD5E1", "#64748B"]))

    def shell(self, c, t):
        """Walls and roof, drawn over the room."""
        box(c, -352, -480, 22, 506, "#55607F")
        box(c, 360, -480, 22, 506, "#55607F")
        roof = skia.Path()
        roof.moveTo(-396, -470)
        roof.lineTo(15, -690)
        roof.lineTo(426, -470)
        roof.lineTo(396, -470)
        roof.lineTo(15, -652)
        roof.lineTo(-366, -470)
        roof.close()
        gable = skia.Path()
        gable.moveTo(-352, -480)
        gable.lineTo(15, -656)
        gable.lineTo(382, -480)
        gable.close()
        c.drawPath(gable, lin_paint(0, -660, 0, -480, ["#3F4A68", "#55607F"]))
        c.drawPath(roof, lin_paint(-396, 0, 426, 0, ["#B45309", "#92400E", "#6B2F0C"]))
        vk = self.ventk.at(t)
        if vk > 0.82:                                                                # the bit of vent above the roof
            top = lerp(SEW_Y, -612, vk)
            c.drawRect(R(VENT_X - 12, top, 24, -524 - top), lin_paint(VENT_X - 12, 0, VENT_X + 12, 0, ["#CBD5E1", "#64748B"]))
            c.drawRRect(rr(VENT_X - 17, top - 6, 34, 9, 3), P("#94A3B8"))

    # ------------------------------------------------------------------ the toilet, cut open
    def toilet(self, c, t):
        T, s = self.T, self.tl.s
        tk = e_back(prog(t, T["tank"] - 0.1, T["tank"] + 0.2))
        bk = e_back(prog(t, T["bowl"] - 0.15, T["bowl"] + 0.15))
        fl = self.flushing(t)
        lvl = self.level.at(t)
        wy = TB - (TB - TF) * lvl                                                    # water surface in the tank
        pts = self.trap_pts(t)
        tw = self.trapw.at(t)
        if bk > 0:
            c.save()
            c.translate(40, 0)
            c.scale(bk, bk)
            c.translate(-40, 0)
            body = skia.Path()                                                       # bowl and pedestal
            body.moveTo(-74, -156)
            body.lineTo(120, -156)
            body.quadTo(134, -150, 130, -130)
            body.cubicTo(122, -70, 150, -30, 142, 0)
            body.lineTo(-40, 0)
            body.cubicTo(-46, -40, -74, -60, -74, -110)
            body.close()
            c.drawPath(body, lin_paint(-74, 0, 142, 0, ["#FFFFFF", PORC, "#B8C2D4"], [0.0, 0.4, 1.0]))
            cav = skia.Path()                                                        # the bowl itself
            cav.moveTo(-58, -150)
            cav.lineTo(106, -150)
            cav.cubicTo(100, -100, 60, -72, 34, -70)
            cav.lineTo(8, -70)
            cav.cubicTo(-20, -74, -56, -100, -58, -150)
            cav.close()
            c.drawPath(cav, P("#16203A"))
            way = poly_path(pts)                                                     # the trapway
            pw = P("#16203A", 1, stroke=30)
            pw.setStrokeJoin(skia.Paint.kRound_Join)
            c.drawPath(way, pw)
            surf = lerp(-22, -108, tw)                                               # trap water: up to the weir when full
            if tw > 0:
                c.save()
                c.clipRect(R(-80, surf, 176 if self.trapk.at(t) < 1 else 176, 200))
                first = poly_path(pts[:len(pts) * 2 // 3 + 1] if self.trapk.at(t) >= 1 else pts)
                pb = P(WATER, 1, stroke=22)
                pb.setStrokeJoin(skia.Paint.kRound_Join)
                c.drawPath(first, pb)
                c.drawPath(cav, P(WATER))
                c.restore()
                c.drawLine(-52 + (surf + 150) * 0.3, surf, 100 - (surf + 150) * 0.45, surf, P("#E0F7FF", 0.8 * prog(tw, 0.55, 0.75), stroke=3))
            if fl > 0:                                                               # a flush on its way through
                stream(c, PASSAGE, t, "#7DD3FC", 9, 1.6, 8, fl)
                stream(c, pts, t, "#7DD3FC", 9, 1.5, 9, fl)
                c.drawPath(cav, P(WATER, 0.5 * fl))
                for i in range(4):
                    a = t * 9 + i * 1.57
                    c.drawCircle(24 + math.cos(a) * 34, -112 + math.sin(a) * 12, 6, P("#E0F7FF", 0.8 * fl))
            c.drawRRect(rr(-70, -168, 196, 12, 6), P("#E5E9F2"))                      # rim
            c.restore()
        if tk > 0:                                                                   # ---- the tank
            c.save()
            c.translate(-110, -162)
            c.scale(tk, tk)
            c.translate(110, 162)
            c.drawRRect(rr(-178, -352, 136, 190, 14), lin_paint(-178, 0, -42, 0, ["#FFFFFF", PORC, "#B8C2D4"], [0.0, 0.4, 1.0]))
            c.drawRRect(rr(-168, -342, 116, 172, 8), P("#16203A"))
            c.drawRect(R(-126, TB - 2, 32, 26), P("#16203A"))                         # the way out at the bottom
            c.save()
            c.clipRRect(rr(-168, -342, 116, 172, 8), skia.ClipOp.kIntersect, True)
            if lvl > 0:
                vrect(c, -168, wy, 116, TB - wy + 10, ["#7DD3FC", WATER, "#0E6BA8"], [0.0, 0.2, 1.0])
                c.drawRect(R(-168, wy, 116, 3), P("#E0F7FF", 0.9))
            floaty = t >= T["float"] - 0.15
            if floaty:                                                               # fill valve, float, overflow tube
                fk = e_back(prog(t, T["float"] - 0.15, T["float"] + 0.15))
                c.drawRect(R(-162, lerp(TB, -322, fk), 12, TB + 322), lin_paint(-162, 0, -150, 0, ["#E5E9F2", "#7C8499"]))
                by = clamp(wy - 6, -326, TB - 14)
                shut = by <= TF - 2
                c.drawRRect(rr(-166, -332, 26, 14, 4), P(GOOD if shut else "#F59E0B"))
                c.drawLine(-152, -322, -100, by, P("#CBD5E1", fk, stroke=4))
                c.drawCircle(-98, by, 15 * fk, rad_paint(-103, by - 5, 22, ["#FDBA74", "#F97316", "#9A3412"]))
                if not shut and t >= T["float"] + 0.2:
                    c.drawLine(-140, -322, -138, wy, P("#7DD3FC", 0.9, stroke=5))
                self.ui["float"] = (-98, by)
            if t >= T["overflow"] - 0.15:
                ok = e_back(prog(t, T["overflow"] - 0.15, T["overflow"] + 0.15))
                top = TB - (TB - TF) * 1.1
                c.drawRect(R(-76, lerp(TB, top, ok), 14, TB - top), P("#E5E9F2", 0.9))
                c.drawRect(R(-72, lerp(TB, top, ok) + 3, 6, TB - top), P("#16203A"))
                if lvl > 1.1:
                    c.drawRect(R(-72, top + 3, 6, TB - top), P("#7DD3FC"))
            c.restore()
            fa = self.flap.at(t)                                                     # the flapper
            c.save()
            c.translate(-90, TB - 3)
            c.rotate(-58 * fa)
            c.drawRRect(rr(-42, -6, 44, 11, 5), P("#EF4444"))
            c.restore()
            c.drawLine(-58, -316, -110 + 18 * fa, TB - 8 - 30 * fa, P("#94A3B8", 0.9, stroke=2))         # chain
            c.drawRRect(rr(-184, -366, 148, 16, 6), P("#E5E9F2"))                     # lid
            c.save()                                                                 # handle
            c.translate(-52, -322)
            c.rotate(28 * bump(t, T["flush1"] - 0.2, T["flush1"] + 0.3) + 28 * bump(t, T["flush4"] - 0.2, T["flush4"] + 0.3)
                     + 28 * bump(t, T["flush5"] - 0.2, T["flush5"] + 0.3))
            c.drawRRect(rr(0, -5, 34, 10, 5), lin_paint(0, -5, 0, 5, ["#F8FAFC", "#94A3B8"]))
            c.restore()
            if lvl > 1.33:                                                           # over the top it goes
                for sx in (-184, -40):
                    c.drawRect(R(sx, -350, 8, 350), P("#7DD3FC", 0.8))
            c.restore()
        # seat and lid
        if bk > 0:
            sk, lk = self.seatk.at(t), self.lidk.at(t)
            c.save()
            c.translate(-62, -170)
            c.rotate(-96 * sk)
            c.drawRRect(rr(0, -8, 186, 10, 5), P("#CBD5E1"))
            c.restore()
            c.save()
            c.translate(-62, -180)
            c.rotate(-98 * (1 - lk))
            c.drawRRect(rr(0, -8, 190, 11, 5), lin_paint(0, -8, 0, 3, ["#FFFFFF", "#CBD5E1"]))
            c.restore()

    # ------------------------------------------------------------------ the world
    def world(self, c, t, cam):
        T, s, e = self.T, self.tl.s, self.tl.e
        cx, cy, z = cam
        cx += math.sin(t * 0.6) * (3 if z < 2 else 1)
        m = self.mode(t)
        gy = (0 - cy) * z + H / 2
        if m in ("house", "room"):
            self.backdrop(c, t, cx, cy, gy)
        self.view(c, (cx, cy, z))
        v2.ground(c, -3400, 3400)
        self.house(c, t)
        # ---- the hook: a seat over a bucket
        if t < T["bowl"]:
            a = 1 - prog(t, T["bowl"] - 0.2, T["bowl"])
            carried = t >= T["carry"] - 0.2
            bx = 40 if not carried else lerp(40, 150, e_io(prog(t, T["carry"] - 0.2, T["out"] + 0.2)))
            by = 0 if not carried else -44 * prog(t, T["carry"] - 0.2, T["carry"] + 0.1)
            if s("fix1") - 0.12 <= t:
                bx, by = 40, 0
            k = e_back(prog(t, 0.08, 0.45))
            c.save()
            c.translate(bx, by)
            c.scale(k, k)
            bucket = skia.Path()
            bucket.moveTo(-46, -92)
            bucket.lineTo(46, -92)
            bucket.lineTo(36, 0)
            bucket.lineTo(-36, 0)
            bucket.close()
            c.drawPath(bucket, lin_paint(-46, 0, 46, 0, [("#94A3B8", a), ("#E2E8F0", a), ("#64748B", a)]))
            c.drawRect(R(-48, -96, 96, 8), P("#475569", a))
            sy = lerp(-560, -104, e_in(prog(t, T["seat"] - 0.2, T["land"]))) if t < s("break1") + 9 else -104
            if t >= T["carry"] - 0.2 and t < s("fix1") - 0.12:
                sy = -104
            c.drawRRect(rr(-58, sy - 6, 116, 12, 6), P("#CBD5E1", a))
            c.drawRRect(rr(-40, sy - 3, 80, 6, 3), P("#475569", a))
            c.restore()
            if s("break1") <= t < s("fix1") - 0.12:                                   # it does not smell of roses
                for i in range(3):
                    u = (t * 0.9 + i / 3) % 1.0
                    wv = skia.Path()
                    x0 = bx - 24 + i * 24
                    wv.moveTo(x0, by - 110 - u * 70)
                    wv.quadTo(x0 + 12, by - 124 - u * 70, x0, by - 138 - u * 70)
                    wv.quadTo(x0 - 12, by - 152 - u * 70, x0, by - 166 - u * 70)
                    c.drawPath(wv, P(GASC, (1 - u) * 0.9, stroke=5))
        self.toilet(c, t)
        # ---- gas and what it does
        pts = self.trap_pts(t)
        if T["gas1"] <= t < s("fix2") - 0.12:                                         # break 2: straight up the pipe
            head = prog(t, T["gas1"], T["smell"])
            stream(c, [(112, SEW_Y), (112, 0)] + list(reversed(pts)), t, GASC, 12, 0.5, 11, 1.0, 0, head, gas=True)
            if t >= T["smell"] - 0.1:
                v2.smoke(c, 24, -150, t, T["smell"] - 0.1, None, rate=10, life=2.6, spread=(110, -30), rise=-95, size=(22, 80), col=GASC,
                         lit=None, lit_until=0, seed=6, a=0.75)
        if s("fix2") - 0.12 <= t < s("break3"):                                       # fix 2: stopped at the water
            if t >= T["seals"] - 0.6:
                up = list(reversed(pts))
                stream(c, [(112, 120), (112, 0)] + up, t, GASC, 12, 0.45, 9, 1.0, 0, 0.42 if self.trapw.at(t) > 0.6 else 1.0, gas=True)
            elif t < T["water"] - 0.2:
                stream(c, [(112, 120), (112, 0)] + list(reversed(pts)), t, GASC, 12, 0.45, 9, 0.8, 0, 1.0, gas=True)
        if s("break4") - 0.12 <= t < s("fix4") - 0.12:                                # break 4: the trap is sucked dry
            fl = self.flushing(t)
            if fl > 0:
                stream(c, [(112, 0), (112, 260)], t, "#7DD3FC", 6, 2.2, 10, fl)
            if t >= T["empty"]:
                stream(c, [(112, 200), (112, 0)] + list(reversed(pts)), t, GASC, 12, 0.5, 9, 1.0, 0, prog(t, T["empty"], T["smell2"]), gas=True)
                if t >= T["smell2"] - 0.1:
                    v2.smoke(c, 24, -150, t, T["smell2"] - 0.1, None, rate=9, life=2.0, spread=(90, -30), rise=-90, size=(18, 60), col=GASC,
                             lit=None, lit_until=0, seed=8, a=0.7)
            for i, tg in enumerate((T["glug"], T["glug"] + 0.26)):
                u = prog(t, tg, tg + 0.5)
                if 0 < u < 1:
                    c.drawCircle(30 + i * 22, lerp(-66, -146, u), 9 + 6 * u, P("#E0F7FF", 0.9 * (1 - u), stroke=3))
        if m == "house" and t >= s("fix4") - 0.12:                                    # fix 4: air comes down the vent
            vk = self.ventk.at(t)
            if vk >= 1 and T["flush5"] <= t < T["flush5"] + 1.8:
                a = prog(t, T["flush5"], T["flush5"] + 0.2) * (1 - prog(t, T["flush5"] + 1.4, T["flush5"] + 1.8))
                stream(c, [(VENT_X, -600), (VENT_X, SEW_Y), (112, SEW_Y)], t, "#FFFFFF", 9, 0.9, 6, a)
                stream(c, [(112, 0), (112, SEW_Y), (-620, SEW_Y)], t, "#7DD3FC", 8, 1.0, 9, a)
            if vk >= 1 and t >= T["smell3"] - 0.3:
                stream(c, [(-620, SEW_Y), (VENT_X, SEW_Y), (VENT_X, -606)], t, GASC, 12, 0.45, 9, 1.0, 0, prog(t, T["smell3"] - 0.3, T["poof"]), gas=True)
        # ---- people
        self.people(c, t, m)
        # ---- the flood
        fdk = self.flood.at(t)
        if fdk > 0:
            top = -78 * fdk
            vrect(c, -330, top, 690, -top, [("#38BDF8", 0.55), ("#0E6BA8", 0.7)])
            for i in range(6):
                wx = -300 + i * 120 + math.sin(t * 1.7 + i) * 14
                c.drawRRect(rr(wx, top + 4 + (i % 2) * 5, 44, 4, 2), P("#E0F7FF", 0.6))
            if fdk > 0.5:                                                            # the duck
                dx, dy = -190 + math.sin(t * 0.9) * 26, top - 4 + math.sin(t * 2.2) * 3
                c.drawOval(R(dx - 24, dy - 18, 48, 26), P("#FACC15"))
                c.drawCircle(dx + 18, dy - 26, 13, P("#FACC15"))
                c.drawCircle(dx + 22, dy - 29, 2.4, P("#11151F"))
                c.drawOval(R(dx + 27, dy - 27, 14, 7), P("#FB923C"))
        self.shell(c, t)
        # ---- on the roof
        if m == "house":
            for i, (bx, by) in enumerate(((-232, -556), (-176, -586))):
                go = T["sorry"] + 0.25 + i * 0.35
                u = prog(t, go, go + 1.3)
                if t >= s("fix4") - 0.12 and u < 1:
                    bird(c, bx + 460 * u * (1 if i else 0.7), by - 330 * e_out(u), t, fly=u, s=1.25)
            if t >= T["poof"] - 0.1:
                v2.smoke(c, VENT_X, -618, t, T["poof"] - 0.1, None, rate=8, life=2.4, spread=(70, -40), rise=-80, size=(16, 60), col=GASC,
                         lit=None, lit_until=0, seed=12, a=0.75)
        c.restore()
        self.ui["cam"] = (cx, cy, z)

    def people(self, c, t, m):
        T, s, e = self.T, self.tl.s, self.tl.e
        if m == "tank" or m == "trap":
            return
        wet = self.flood.at(t)
        if t < s("break1"):
            pose = "stand" if t < T["land"] else "cheer"
            self.crew(c, t, pose, xs=XS, face=-1)
        elif t < s("fix1") - 0.12:
            cx_ = lerp(176, 190, prog(t, T["carry"] - 0.2, T["out"] + 0.2))
            engineer(c, cx_, 0, 118, SHIRTS[0], t, "carry" if t >= T["carry"] - 0.2 else "look", face=-1)
            for i, px in enumerate((250, 300)):
                off = 26 * prog(t, T["nobody"] - 0.2, T["nobody"] + 0.2)
                engineer(c, px + off, 0, 118 + (i % 2) * 8, SHIRTS[i + 1], t + i * 0.4, "shrug" if t >= T["nobody"] else "look", face=-1)
        elif t < s("fix4") - 0.12:
            if t < s("break2"):
                pose = "look" if t < T["flush1"] else "cheer" if t >= T["work"] else "point"
            elif t < s("break3") - 0.1:
                pose = "look" if t < T["smell"] else "duck"
            else:
                pose = "look" if t < T["bathroom"] - 0.3 else "shrug"
            self.crew(c, t, pose, xs=XS, face=-1) if wet <= 0.2 else [engineer(c, px, -10 * wet, 118 + (i % 2) * 8, col, t + i * 0.37, pose, face=-1, wet=wet)
                                                                      for i, (px, col) in enumerate(zip(XS, SHIRTS))]
        elif m == "house":
            if t < s("cta"):
                self.crew(c, t, "look" if t < T["stays"] else "cheer", xs=XS, face=-1)
            else:
                xs = (-640, -590, -540)
                self.crew(c, t, "cheer", xs=xs, face=1)
                hats_in_the_air(c, xs, -150, t, T["cong2"])
        elif t < s("tag") - 0.2:                                                     # the cta and the reveal
            reading = t >= T["read"] - 0.3
            engineer(c, 176, 0, 124, SHIRTS[1], t, "look" if reading else "stand", face=-1)
            if reading:
                bx, by = 150, -150
            if t >= T["shampoo"]:
                pk = e_back(prog(t, T["shampoo"], T["shampoo"] + 0.25))
                u = e_io(prog(t, T["read"] - 0.3, T["read"]))
                bx, by = lerp(-150, 156, u), lerp(-366, -146, u) - 90 * math.sin(u * math.pi)
                c.save()
                c.translate(bx, by)
                c.scale(pk, pk)
                c.drawRRect(rr(-13, -44, 26, 44, 7), lin_paint(-13, 0, 13, 0, ["#F9A8D4", "#EC4899", "#9D174D"]))
                c.drawRRect(rr(-6, -56, 12, 14, 3), P("#F8FAFC"))
                c.drawRRect(rr(-9, -32, 18, 18, 3), P("#FDF2F8"))
                for j in range(3):
                    c.drawRect(R(-6, -28 + j * 5, 12, 2), P("#9D174D", 0.7))
                c.restore()
        else:                                                                        # the tag: up or down?
            a_up = T["up"] <= t
            engineer(c, 178, 0, 120, SHIRTS[0], t, "point" if a_up else "look", face=-1)
            engineer(c, 236, 0, 126, SHIRTS[2], t + 0.4, "shrug" if t >= T["down"] else "look", face=-1)
            if t >= T["economists"]:
                for i in range(7):                                                   # the papers arrive
                    t0 = T["economists"] + i * 0.22
                    u = prog(t, t0, t0 + 0.6)
                    if u <= 0:
                        continue
                    px = -150 + (i % 3 - 1) * 16
                    py = lerp(-760, -368 - i * 7, e_in(u))
                    c.save()
                    c.translate(px, py)
                    c.rotate((1 - u) * (40 if i % 2 else -40))
                    c.drawRRect(rr(-38, -5, 76, 7, 2), P("#F8FAFC"))
                    c.drawRect(R(-38, 1, 76, 1.5), P("#94A3B8"))
                    c.restore()
            if t >= T["papers"] - 0.2:                                               # one of them, held up
                pk = e_back(prog(t, T["papers"] - 0.2, T["papers"] + 0.1))
                c.save()
                c.translate(206, -330)
                c.rotate(math.sin(t * 2) * 3)
                c.scale(pk, pk)
                c.drawRRect(rr(-52, -68, 104, 136, 5), P("#F8FAFC"))
                for j in range(3):
                    c.drawRect(R(-40, -56 + j * 9, 80 - j * 18, 4), P("#94A3B8"))
                for j, hgt in enumerate((30, 30)):
                    c.drawRect(R(-30 + j * 36, 44 - hgt, 24, hgt), P(("#38BDF8", "#FB7185")[j]))
                c.drawLine(-40, 46, 40, 46, P("#475569", 1, stroke=2))
                c.restore()

    def draw_room(self, c, t):
        self.world(c, t, self.cams["room"].at(t))

    def draw_trap(self, c, t):
        self.world(c, t, self.cams["trap"].at(t))

    def draw_tank(self, c, t):
        self.world(c, t, self.cams["tank"].at(t))

    def draw_house(self, c, t):
        self.world(c, t, self.cams["house"].at(t))

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -200, 1.4)), x, y)

    def ui_room(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            x0, y0 = self.at(98, -104)
            self.label(x0, y0, x0 + 200, y0 - 230, "seat", T["land"] + 0.05, T["congrats"] + 0.1, HILITE)
        elif tw < s("fix1") - 0.12:
            self.badge("alert", T["nobody"], s("fix1") - 0.2)
            self.red(T["nobody"], 1.6)
        elif tw < s("break2"):
            x0, y0 = self.at(-110, -352)
            self.label(x0, y0, x0 + 260, y0 - 150, "tank", T["tank"] + 0.25, T["flapper"] - 0.15, WATER)
            x1, y1 = self.at(-108, TB)
            self.label(x1, y1 + 4, x1 + 330, y1 - 330, "flap", T["flapper"] + 0.05, T["handle"] - 0.05, "#EF4444")
            p = self.span(T["gravity"] - 0.1, s("break2") - 0.2, 0.25, 0.2)
            if p > 0:
                gx, gy = self.at(184, -330)
                v2.chip(c, gx, gy, self.L["grav"], p, size=38, accent=HILITE)
                c.drawLine(gx, gy + 44, gx, gy + 44 + 120 * p, P(HILITE, p, stroke=9))
                ar = skia.Path()
                ar.moveTo(gx - 22, gy + 150 * p + 14)
                ar.lineTo(gx + 22, gy + 150 * p + 14)
                ar.lineTo(gx, gy + 150 * p + 46)
                ar.close()
                c.drawPath(ar, P(HILITE, p))
            self.badge("check", T["work"], s("break2") - 0.15, x=930, y=420)
        elif tw < s("fix2") - 0.12:
            x0, y0 = self.at(40, -300)
            self.label(x0, y0, x0 + 250, y0 - 190, "gas", T["smell"] + 0.2, s("fix2") - 0.25, GASC)
            self.badge("alert", T["smell"], s("fix2") - 0.2, x=930, y=420)
            self.red(T["smell"], 1.8)
        elif tw < s("fix3"):
            self.badge("alert", T["bathroom"], s("fix3") - 0.2, x=930, y=420)
            self.red(T["bathroom"], 1.8)
        elif tw >= s("tag") - 0.2:
            self.chip(700, 330, "tie", T["winner"] - 0.1, self.duration + 1, accent=HILITE, size=44)

    def ui_trap(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break3"):
            x0, y0 = self.at(96, -110)
            self.label(x0, y0 - 40, x0 + 190, y0 - 300, "trap", T["trap"] - 0.05, T["water"] - 0.1)
            x1, y1 = self.at(46, -40)
            self.label(x1, y1, 250, y1 + 300, "seal", T["curve"] - 0.4, T["seals"] + 0.6, WATER)
            self.badge("check", T["gas"], s("break3") - 0.15)
        else:
            x0, y0 = self.at(50, -36)
            self.label(x0, y0, 250, y0 + 300, "dry", T["empty"] + 0.05, s("fix4") - 0.2, WARN)
            self.badge("alert", T["empty"], s("fix4") - 0.2)
            self.red(T["empty"], 1.8)

    def ui_tank(self, c, t, tw):
        T, s = self.T, self.tl.s
        c.drawRRect(rr(30, self.CAPTION_Y - 105, W - 60, 190, 44), P("#0B1024", 0.62, blur=22))    # white porcelain behind the captions
        fx_, fy_ = self.at(*self.ui.get("float", (-98, -260)))
        self.label(fx_ + 30, fy_, 800, fy_ + 250, "float", T["float"] + 0.15, T["full"] + 0.2, "#F97316")
        vx, vy = self.at(-153, -325)
        self.label(vx, vy, 300, vy - 150, "valve", T["shuts"] - 0.1, T["overflow"] - 0.25, GOOD)
        ox, oy = self.at(-69, -306)
        self.label(ox + 10, oy, 820, oy - 190, "over", T["overflow"] + 0.15, s("break4") - 0.3)
        self.badge("check", T["shuts"] + 0.3, s("break4") - 0.15, x=880, y=1050)

    def ui_house(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("cta"):
            x0, y0 = self.at(VENT_X, -330)
            self.label(x0, y0, x0 + 30, y0 - 390 if tw < T["smell3"] - 0.4 else y0 - 300, "vent", T["roof"] - 0.2, T["air"] + 0.5)
            x1, y1 = self.at(VENT_X, -120)
            self.label(x1, y1, 240, y1 + 30, "airin", T["air"] + 0.1, T["stays"] - 0.1, "#FFFFFF")
            x2, y2 = self.at(96, -60)
            self.label(x2, y2, 800, y2 - 330, "full", T["stays"], T["smell3"] + 0.3, WATER)
            self.badge("check", T["stays"] + 0.3, 1e9, x=900, y=1090)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.pop(61), -6), (T["seat"] - 0.2, sfx.whoosh(0.3, False, 62), -9),
              (T["land"], sfx.clank(600, 0.25, 63), -4), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9)]
        ev += [(T["carry"] - 0.2, sfx.creak(0.4, 65), -8), (T["nobody"], sfx.alarm(3, 820), -11), (T["job"], sfx.womp(), -10)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["tank"] - 0.1, sfx.thud(0.35, 67), -4), (T["bowl"] - 0.15, sfx.thud(0.3, 68), -5),
               (T["flapper"], sfx.pop(69), -7), (T["flush1"] - 0.15, sfx.lock_click(70), -3), (T["flush1"], flush_snd(1.7, 71), -4),
               (T["work"], sfx.chime(), -7)]
        ev += [(T["gas1"], gas_hiss(1.2, 72), -9), (T["smell"], sfx.alarm(3, 820), -11), (T["hello"], sfx.womp(), -9)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["bend"], sfx.creak(0.7, 74), -4), (T["s"], sfx.clank(420, 0.3, 75), -6),
               (T["water"] - 0.2, drip_snd(0.7, 76), -6), (T["seals"], sfx.pop(77), -6), (T["gas"], sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 78), -4), (T["flood0"], drip_snd(1.6, 79), -7), (T["flood0"] + 1.0, drip_snd(1.4, 80), -8),
               (T["bathroom"], sfx.alarm(3, 820), -11), (T["pool"], drip_snd(0.5, 81), -6), (T["pool"] + 0.15, sfx.womp(), -10)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 82), -4), (T["float"] - 0.15, sfx.pop(83), -5), (T["float"] + 0.2, drip_snd(1.2, 84), -10),
               (T["shuts"], sfx.lock_click(85), -3), (T["shuts"] + 0.3, sfx.chime(), -7), (T["overflow"] - 0.15, sfx.pop(86), -5),
               (T["case"] - 0.3, drip_snd(0.6, 87), -9)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 88), -4), (T["flush4"], flush_snd(1.6, 89), -6), (T["sucks"], gas_hiss(0.6, 90), -8),
               (T["glug"], glug(0), -2), (T["glug"] + 0.26, glug(1), -2), (T["empty"], sfx.alarm(3, 820), -11), (T["smell2"] + 0.3, sfx.womp(), -10)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 91), -4), (T["vent"] - 0.1, sfx.whirr(0.9, 160, 300, 92), -9),
               (T["roof"] + 0.2, sfx.clank(500, 0.3, 93), -6), (T["flush5"], flush_snd(1.5, 94), -9), (T["air"] + 0.1, gas_hiss(1.0, 95), -11),
               (T["stays"] + 0.3, sfx.chime(), -7), (T["poof"], gas_hiss(0.6, 96), -9), (T["sorry"] + 0.25, sfx.creak(0.3, 97), -8),
               (T["sorry"] + 0.6, sfx.creak(0.3, 98), -9)]
        ev += [(T["pause"], sfx.click(99), 0), (T["follow"] - 0.15, sfx.pop(100), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 101), -7)]
        ev += [(T["lid"] + 0.18, sfx.clank(700, 0.2, 102), -3), (T["lock"] - 0.3, sfx.creak(0.3, 103), -7), (T["lock"], sfx.lock_click(104), -2),
               (T["shampoo"], sfx.pop(105), -5), (T["read"], sfx.sparkle(0.5, 6, 106), -9)]
        ev += [(T["s1"] - 0.32, sfx.whoosh(0.5, False, 107), -6), (T["s1"], sfx.pop(108), -3), (T["s2"], sfx.pop(109), -3), (T["s3"], sfx.pop(110), -3)]
        ev += [(T["cong2"], sfx.pop(111), -2), (T["cong2"], sfx.sparkle(1.0, 14, 112), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 113), -6), (T["up"], sfx.clank(800, 0.15, 114), -6), (T["down"], sfx.clank(650, 0.15, 115), -6)]
        ev += [(T["economists"] + 0.6 + i * 0.22, sfx.tap(116 + i), -9) for i in range(7)]
        ev += [(T["papers"] - 0.2, sfx.pop(124), -6), (T["winner"] + 0.3, sfx.womp(), -3)]
        return ev


NAME = "toilet"
EPISODE = Toilet
