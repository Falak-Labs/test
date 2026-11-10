"""Episode 13 - A bank vault.  v2 look: two sets with whip cuts.

bank   the bank cut open from the side (floor at y = 0): lobby x -700..80 with the customer desk on the left, the
       vault room x 80..560 with its door in the left wall, and the ground under both (the tunnel)
door   the round vault door from the front, centred on the origin, with an x-ray panel for what is inside it
"""
from v2_base import *  # noqa: F401,F403

CONC, STEELD, BRASS = "#8E96AA", "#9AA3B8", "#D4A84B"
VX0, VX1, VTOP, WALL = 80, 560, -410, 50                 # the vault room: outer left, outer right, outer top, wall thickness
DOORH = 250                                              # height of the door opening
BX = 292                                                 # where the box stands at the start
THIEF = "#374151"


# ====================================================================================== pieces
def concrete(c, x, y, w, h, seed=1, a=1.0, bars=0.0):
    """A slab of concrete; bars 0..1 shows the steel bars inside it."""
    if w <= 0 or h <= 0:
        return
    vrect(c, x, y, w, h, [(shade(CONC, 0.1), a), (CONC, a), (shade(CONC, -0.3), a)], [0.0, 0.4, 1.0])
    rng = random.Random(seed)
    for _ in range(int(w * h / 900)):
        c.drawCircle(x + rng.uniform(3, w - 3), y + rng.uniform(3, h - 3), rng.uniform(1.5, 4), P("#000000" if rng.random() < 0.6 else "#FFFFFF", 0.10 * a))
    if bars > 0:
        vert = h > w
        n = max(2, int((h if vert else w) // 42))
        for i in range(n):
            u = (i + 0.5) / n
            if vert:
                c.drawLine(x + 8, y + h * u, x + (w - 8) * bars + 8 * (1 - bars), y + h * u, P("#F97316", 0.95 * bars, stroke=5))
            else:
                c.drawLine(x + w * u, y + 8, x + w * u, y + (h - 8) * bars + 8 * (1 - bars), P("#F97316", 0.95 * bars, stroke=5))
        for k in (0.3, 0.7):
            if vert:
                c.drawLine(x + w * k, y + 6, x + w * k, y + h - 6, P("#FB923C", 0.9 * bars, stroke=4))
            else:
                c.drawLine(x + 6, y + h * k, x + w - 6, y + h * k, P("#FB923C", 0.9 * bars, stroke=4))


def strongbox(c, x, y, s=1.0, lid=1.0, lock=0.0, a=1.0):
    """The money box, standing on (x, y)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    box(c, -46, -56, 92, 56, "#64748B", r=6, a=a)
    c.drawRect(R(-46, -34, 92, 5), P("#334155", a))
    c.save()
    c.translate(-46, -56)
    c.rotate(-70 * (1 - lid))
    box(c, 0, -14, 92, 16, "#94A3B8", r=5, a=a)
    c.restore()
    if lock > 0:
        c.drawArc(R(-9, -52 + 16 * (1 - lock), 18, 20), 180, 180, False, P("#E5E9F2", a, stroke=4))
        c.drawRRect(rr(-12, -36, 24, 18, 4), P(BRASS, a))
    c.restore()


def gold(c, x, y, n=3, a=1.0):
    for row in range(n):
        for i in range(n - row):
            bx = x + (i - (n - row - 1) / 2) * 34
            by = y - row * 16
            c.drawRRect(rr(bx - 15, by - 14, 30, 14, 3), lin_paint(0, by - 14, 0, by, [("#FDE68A", a), ("#EAB308", a), ("#A16207", a)]))
    add_glow(c, x, y - n * 8, 30 + n * 16, "#FDE047", 0.35 * a)


def wheel(c, x, y, r, ang, a=1.0):
    """The spoked hand wheel of the door, seen from the front."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawCircle(0, 0, r, P("#0B1220", 0.35 * a, stroke=r * 0.26, blur=6))
    c.drawCircle(0, 0, r, lin_paint(-r, -r, r, r, [("#FFFFFF", a), ("#CBD5E1", a), ("#64748B", a)], None))
    c.drawCircle(0, 0, r * 0.8, P("#55607F", a))
    for i in range(5):
        an = math.radians(i * 72)
        c.drawLine(0, 0, math.cos(an) * r * 0.92, math.sin(an) * r * 0.92, P("#E5E9F2", a, stroke=r * 0.16))
        c.drawCircle(math.cos(an) * r * 1.12, math.sin(an) * r * 1.12, r * 0.13, P("#F8FAFC", a))
    c.drawCircle(0, 0, r * 0.26, rad_paint(-r * 0.08, -r * 0.08, r * 0.4, [("#FFFFFF", a), ("#94A3B8", a), ("#475569", a)]))
    c.restore()


def nightcap(c, x, y, h, face=1):
    u = h / 140.0
    p = skia.Path()
    p.moveTo(x - 19 * u, y - 138 * u)
    p.lineTo(x + 19 * u, y - 138 * u)
    p.lineTo(x - face * 34 * u, y - 186 * u)
    p.close()
    c.drawPath(p, P("#60A5FA"))
    c.drawCircle(x - face * 34 * u, y - 186 * u, 7 * u, P("#F8FAFC"))
    c.drawRRect(rr(x - 21 * u, y - 142 * u, 42 * u, 8 * u, 4 * u), P("#F8FAFC"))


def drill_snd(d=1.0, seed=40):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    tone = np.sign(np.sin(2 * np.pi * (310 + 30 * np.sin(2 * np.pi * 9 * tt)) * tt)) * 0.4
    nz = sfx._bp(sfx._rng(seed).standard_normal(n), 900, 4200) * 0.6
    return sfx._norm((tone + nz) * sfx._ar(n, 0.05, 0.12), 0.6)


def glass_snd(seed=41):
    n = int(0.6 * sfx.SR)
    x = np.zeros(n)
    rng = sfx._rng(seed)
    for _ in range(26):
        i = int(rng.uniform(0, 0.35) * sfx.SR)
        m = int(rng.uniform(0.04, 0.16) * sfx.SR)
        tt = np.arange(m) / sfx.SR
        x[i:i + m] += np.sin(2 * np.pi * rng.uniform(2200, 7000) * tt) * np.exp(-tt * 40) * rng.uniform(0.3, 1.0)
    return sfx._norm(x, 0.7)


def dig_snd(seed=42):
    n = int(0.3 * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 200, 1800) * sfx._env(n, 0.01, 0.1)
    return sfx._norm(x, 0.7)


def siren(d=1.8):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 700 + 300 * np.sin(2 * np.pi * 1.4 * tt)
    return sfx._norm(np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * sfx._ar(n, 0.1, 0.4), 0.4)


# ====================================================================================== the episode
class Vault(EpisodeV2):
    BUILD_NO = 13
    FIRST_SET = "bank"
    CLEAR = "#0B1024"
    TITLE = {"en": "BANK VAULT", "ar_sa": "خزنة بنك"}
    EMPH = {"en": ["CONGRATS", "VAULT", "THIEF", "PACKED", "ROOM", "CONCRETE", "STEEL", "DRILL", "LOCK", "GLASS", "BOLTS", "CODE",
                   "MANAGER", "MIDNIGHT", "TIME", "CLOCKS", "TWO", "SLEEP", "TUNNEL", "SENSORS", "MICROPHONES", "POLICE", "FOLLOW",
                   "CONDITIONER", "GIANT", "WHEEL", "PEN", "ZERO", "YOURSELF", "STOLEN", "CHAIN"],
            "ar_sa": ["مبروك", "خزنة", "حرامي", "جهزته", "غرفة", "خرسانة", "سيخ", "دريل", "القفل", "زجاج", "مسامير", "الرقم",
                      "المدير", "الليل", "بتوقيت", "ساعات", "شخصين", "ينام", "نفق", "حساسات", "ومايكات", "بالشرطة", "تابعني",
                      "مكيف", "ضخم", "وعجلة", "وقلم", "وصفر", "بيدك", "انسرق", "السلسلة"]}
    KEYS = {"ar_sa": {
        ("hook", "MONEY"): "فلوسك", ("hook", "BOX"): "صندوق", ("hook", "LOCK"): "وقفلته", ("hook", "CONGRATS"): "مبروك",
        ("break1", "THIEF"): "حرامي", ("break1", "PICKS"): "يشيل", ("break1", "WALKS"): "ويمشي", ("break1", "PACKED"): "جهزته",
        ("fix1", "ROOM"): "غرفة", ("fix1", "CONCRETE"): "خرسانة", ("fix1", "THICK"): "سماكتها", ("fix1", "STEEL"): "سيخ",
        ("break2", "BACK"): "يرجع", ("break2", "DRILL"): "دريل", ("break2", "LOCK"): "القفل",
        ("fix2", "GLASS"): "زجاج", ("fix2", "DRILL"): "الدريل", ("fix2", "CRACKS"): "كسره", ("fix2", "SPRING"): "مسامير", ("fix2", "JAM"): "وتعلّق",
        ("fix2", "CODE"): "الرقم", ("fix2", "WORK"): "يفتحه",
        ("break3", "SKIPS"): "يترك", ("break3", "MANAGER"): "المدير", ("break3", "OPEN"): "يفتحها", ("break3", "MIDNIGHT"): "الليل",
        ("fix3", "TIME"): "قفل", ("fix3", "THREE"): "ثلاث", ("fix3", "SHUT"): "مقفل", ("fix3", "MORNING"): "الصبح", ("fix3", "CODE"): "ورقم",
        ("fix3", "TWO"): "شخصين", ("fix3", "SLEEP"): "ينام",
        ("break4", "HOPELESS"): "فايدة", ("break4", "DIGS"): "فيحفر", ("break4", "TUNNEL"): "نفق", ("break4", "FLOOR"): "الأرضية",
        ("fix4", "SENSORS"): "حساسات", ("fix4", "SHAKE"): "باهتزاز", ("fix4", "MICROPHONES"): "ومايكات", ("fix4", "SCRAPING"): "الحفر",
        ("fix4", "ALARM"): "وإنذار", ("fix4", "POLICE"): "بالشرطة", ("fix4", "THROUGH"): "يوصل",
        ("cta", "SPIN"): "تلف", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "GIANT"): "باب", ("reveal", "WHEEL"): "وعجلة", ("reveal", "PEN"): "وقلم", ("reveal", "CHAIN"): "بسلسلة", ("reveal", "STEALS"): "يسرق",
        ("stat", "ONE"): "باب", ("stat", "TWENTY"): "عشرين", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "PEN"): "والقلم", ("tag", "STOLEN"): "انسرق", ("tag", "DAY"): "يوم", ("tag", "CHAIN"): "السلسلة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an air conditioner"),
                   "stat": [("1", "DOOR"), ("20", "TONS"), ("0", "ROBBERIES")],
                   "L": {"box": "YOUR BOX", "thick": "A FOOT AND A HALF", "bars": "STEEL BARS", "glass": "GLASS PLATE", "bolts": "SPRING BOLTS",
                         "nocode": "RIGHT CODE. STILL SHUT.", "tlock": "TIME LOCK", "morning": "SHUT UNTIL MORNING", "two": "TWO PEOPLE, ONE CODE",
                         "tunnel": "TUNNEL", "sens": "SHAKE SENSORS", "mic": "MICROPHONES", "police": "POLICE", "pen": "PEN ON A CHAIN",
                         "gone": "DAY ONE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مكيف"),
                      "stat": [("1", "باب"), ("20", "طن"), ("0", "سرقات")],
                      "L": {"box": "صندوقك", "thick": "نص متر", "bars": "سيخ حديد", "glass": "لوح زجاج", "bolts": "مسامير بزنبرك",
                            "nocode": "الرقم صح. والباب مقفل.", "tlock": "قفل بتوقيت", "morning": "مقفل لين الصبح", "two": "شخصين، رقم واحد",
                            "tunnel": "نفق", "sens": "حساسات اهتزاز", "mic": "مايكات", "police": "الشرطة", "pen": "قلم بسلسلة",
                            "gone": "أول يوم"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "money": ("hook", "MONEY", 0.2), "box": ("hook", "BOX", 0.38), "lock": ("hook", "LOCK", 0.5), "congrats": ("hook", "CONGRATS", 0.6),
            "thief": ("break1", "THIEF", 0.15), "picks": ("break1", "PICKS", 0.22), "walks": ("break1", "WALKS", 0.5), "packed": ("break1", "PACKED", 0.76),
            "room": ("fix1", "ROOM", 0.25), "concrete": ("fix1", "CONCRETE", 0.36), "thick": ("fix1", "THICK", 0.7), "steel": ("fix1", "STEEL", 0.82),
            "back": ("break2", "BACK", 0.56), "drill": ("break2", "DRILL", 0.7), "lock2": ("break2", "LOCK", 0.93),
            "glass": ("fix2", "GLASS", 0.15), "drill2": ("fix2", "DRILL", 0.42), "cracks": ("fix2", "CRACKS", 0.45), "spring": ("fix2", "SPRING", 0.54),
            "jam": ("fix2", "JAM", 0.62), "code": ("fix2", "CODE", 0.88), "work": ("fix2", "WORK", 0.95),
            "skips": ("break3", "SKIPS", 0.22), "manager": ("break3", "MANAGER", 0.63), "open": ("break3", "OPEN", 0.75), "midnight": ("break3", "MIDNIGHT", 0.9),
            "time": ("fix3", "TIME", 0.13), "three": ("fix3", "THREE", 0.2), "shut": ("fix3", "SHUT", 0.4), "morning": ("fix3", "MORNING", 0.48),
            "code2": ("fix3", "CODE", 0.62), "two": ("fix3", "TWO", 0.72), "sleep": ("fix3", "SLEEP", 0.95),
            "hopeless": ("break4", "HOPELESS", 0.27), "digs": ("break4", "DIGS", 0.58), "tunnel": ("break4", "TUNNEL", 0.68), "floor": ("break4", "FLOOR", 0.93),
            "sensors": ("fix4", "SENSORS", 0.12), "shake": ("fix4", "SHAKE", 0.3), "microphones": ("fix4", "MICROPHONES", 0.35), "scraping": ("fix4", "SCRAPING", 0.55),
            "alarm": ("fix4", "ALARM", 0.7), "police": ("fix4", "POLICE", 0.83), "through": ("fix4", "THROUGH", 0.96),
            "spin": ("cta", "SPIN", 0.22), "follow": ("cta", "FOLLOW", 0.4),
            "giant": ("reveal", "GIANT", 0.2), "wheel": ("reveal", "WHEEL", 0.43), "pen": ("reveal", "PEN", 0.55), "chain": ("reveal", "CHAIN", 0.68),
            "steals": ("reveal", "STEALS", 0.88),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "TWENTY", 0.3), "s3": ("stat", "ZERO", 0.63),
            "cong2": ("closer", "CONGRATS", 0.16),
            "pen2": ("tag", "PEN", 0.2), "stolen": ("tag", "STOLEN", 0.35), "day": ("tag", "DAY", 0.58), "chain2": ("tag", "CHAIN", 0.9)})
        T["grab"] = T["picks"] + 0.25
        T["built"] = T["room"] + 0.1
        T["crack"] = T["cracks"] + 0.1                                # the glass plate breaks
        T["fire"] = max(T["spring"], T["crack"] + 0.25)               # the spring bolts shoot out
        T["dig0"] = min(T["digs"], T["tunnel"]) - 0.2
        T["caught"] = T["through"] - 0.1
        T["pencut"] = T["pen"] - 0.4
        self.cut(s("fix1") - 0.12, "bank", 1)
        self.cut(s("fix2") - 0.12, "door", 1)
        self.cut(s("break3") - 0.1, "bank", -1)
        self.cut(s("fix3") - 0.12, "door", 1)
        self.cut(s("break4") - 0.12, "bank", -1)
        self.cut(s("cta") + 0.05, "door", 1)
        self.cut(T["pencut"], "bank", -1)
        self.cut(T["s1"] - 0.35, "door", 1)
        self.cut(s("tag") - 0.2, "bank", -1)
        self.cam = Camera(226, -112, 2.4)
        cm = self.cam
        cm.key(0.05, 226, -104, 2.6, 1.6).key(s("break1") - 0.1, 200, -142, 1.9, 0.9)
        cm.key(s("fix1") - 0.12, 232, -195, 1.38, 0.0).key(T["thick"] - 0.5, 150, -142, 1.9, 0.8)
        cm.key(s("break2") - 0.1, -20, -142, 1.9, 0.6)
        cm.key(s("break3") - 0.1, -100, -154, 1.75, 0.0)
        cm.key(s("break4") - 0.12, -30, -142, 1.9, 0.0).key(T["dig0"] - 0.2, -300, 150, 1.5, 0.6).key(T["floor"] - 0.45, 10, 150, 1.5, 0.8)
        cm.key(s("fix4") - 0.1, 250, 52, 1.4, 0.7).key(T["alarm"] - 0.35, 72, 10, 1.15, 0.8)
        self.reach = (Track(-720.0).to(T["dig0"], 110.0, T["floor"] + 0.2 - T["dig0"], e_io).to(s("fix4") + 0.1, 250.0, 1.2, e_io)
                      .to(T["scraping"], 330.0, max(0.3, T["caught"] - T["scraping"]), e_io))
        cm.key(T["pencut"], -470, -108, 2.5, 0.0).key(T["pen"] + 0.2, -466, -104, 2.6, 1.6)
        cm.key(s("tag") - 0.2, -416, -135, 2.0, 0.0)
        self.dcam = Camera(0, 174, 1.15)                               # the door, from the front
        dc = self.dcam
        dc.key(s("fix2") - 0.12, 0, 174, 1.15, 0.0).key(T["drill2"] - 0.5, 0, 130, 1.45, 0.8).key(T["code"] - 0.5, 60, 150, 1.25, 0.7)
        dc.key(s("fix3") - 0.12, 0, 96, 1.3, 0.0).key(T["code2"] - 0.5, 0, 174, 1.12, 0.8)
        dc.key(s("cta") + 0.05, 0, 150, 1.05, 0.0).key(s("reveal") - 0.1, 0, 140, 1.12, 1.2)
        dc.key(T["s1"] - 0.35, 0, 94, 0.85, 0.0).key(s("closer"), 0, 100, 0.9, 2.0)
        self.spin = (Track(0.0).to(T["code"] + 0.1, 14.0, 0.15).to(T["work"], -10.0, 0.15).to(T["work"] + 0.3, 0.0, 0.2)
                     .to(T["wheel"] - 0.1, 400.0, 1.0, e_io).to(T["cong2"], 760.0, 0.9, e_io))
        self.spans = [(T["grab"], T["steel"] + 0.4), (T["lock2"] - 0.3, T["jam"] + 0.4), (T["open"], T["two"] + 0.6), (T["tunnel"], T["caught"] + 0.2)]
        self.shakes = [(T["lock"], 0.15, 6), (T["built"], 0.5, 14), (T["crack"], 0.3, 10), (T["fire"], 0.35, 14), (T["alarm"], 0.3, 8),
                       (T["caught"], 0.3, 10)]

    # ------------------------------------------------------------------ set: the bank, from the side
    def thief(self, c, x, y, t, pose="walk", face=1, h=128, bag=True):
        if bag:
            c.drawCircle(x - face * 30, y - h * 0.5, 26, rad_paint(x - face * 36, y - h * 0.56, 40, ["#E7D3A8", "#C2A46B", "#8A6F3C"]))
            c.drawRRect(rr(x - face * 30 - 8, y - h * 0.5 - 34, 16, 12, 4), P("#8A6F3C"))
        person(c, x, y, h, THIEF, t, pose, face=face, hat="beanie", pants="#111827")

    def draw_bank(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.cam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        cx, cy, z = cam
        self.view(c, cam)
        v2.ground(c, -3400, 3400)
        # ---- the tunnel
        if T["dig0"] <= t < s("cta") + 0.05:
            reach = self.reach.at(t)
            tp = skia.Path()
            tp.moveTo(-1000, 60)
            tp.cubicTo(-800, 60, -760, 190, -600, 190)
            tp.lineTo(reach, 190)
            pr = P("#4A5578", 1, stroke=142)
            pr.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawPath(tp, pr)
            pr2 = P("#080A16", 1, stroke=128)
            pr2.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawPath(tp, pr2)
            lit = lin_paint(reach - 330, 0, reach, 0, [("#FFD98A", 0.0), ("#FFD98A", 0.42)])   # his lamp
            lit.setStyle(skia.Paint.kStroke_Style)
            lit.setStrokeWidth(128)
            lit.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawLine(reach - 330, 190, reach, 190, lit)
            self.ui["reach"] = reach
            # the digger
            if t < T["caught"]:
                dig = math.sin(t * 13)
                self.thief(c, reach - 56, 250, t, "carry", 1, 104, bag=False)
                c.drawRRect(rr(reach - 130, 226, 26, 24, 5), P("#F59E0B"))            # his lamp, on the ground
                add_glow(c, reach - 117, 232, 60, "#FFE9B8", 0.8)
                c.save()
                c.translate(reach - 20, 186)
                c.rotate(-30 + 28 * dig)
                c.drawLine(0, 0, 44, -20, P("#8B5E3C", 1, stroke=6))
                c.drawRRect(rr(36, -40, 18, 34, 5), P("#CBD5E1"))
                c.restore()
                v2.debris(c, reach + 30, 190, t, t - (t % 0.24), 0.5, n=5, speed=260, seed=int(t * 4), gravity=700, cols=("#6B7699", "#8E96AA", "#51597A"),
                          cone=(160, 250), size=(6, 16))
        # ---- the lobby
        vrect(c, -700, -520, 1420, 520, ["#31466B", "#27395A", "#1D2B47"], [0.0, 0.5, 1.0])
        for px in range(-640, 720, 120):
            c.drawRect(R(px, -520, 3, 520), P("#000000", 0.12))
        c.drawRect(R(-700, -150, 1420, 6), P(BRASS, 0.5))
        box(c, -730, -556, 1480, 36, "#55607F", r=6)                                 # the roof
        window_night(c, -640, -430, 150, 190, t)
        c.drawCircle(-300, -400, 44, P("#F8FAFC"))                                    # the clock on the wall
        c.drawCircle(-300, -400, 44, P("#1B2238", 1, stroke=6))
        night = s("break3") - 0.1 <= t < s("break4") - 0.12
        ha = -90 if night else -90 + (t * 3) % 360
        c.drawLine(-300, -400, -300 + math.cos(math.radians(-90)) * 24, -400 + math.sin(math.radians(-90)) * 24, P("#1B2238", 1, stroke=6))
        c.drawLine(-300, -400, -300 + math.cos(math.radians(ha)) * 34, -400 + math.sin(math.radians(ha)) * 34, P("#EF4444", 1, stroke=4))
        for lx in (-450, -120, 330):                                                 # lamps
            c.drawRect(R(lx - 2, -520, 4, 40), P("#11151F"))
            c.drawRRect(rr(lx - 30, -482, 60, 16, 8), P("#FFF3C4"))
            add_glow(c, lx, -450, 300, "#FFE9B8", 0.22 if not night else 0.10)
        if night:
            c.drawRect(R(-700, -520, 1420, 520), P("#050818", 0.30))
        box(c, -740, 0, 1480, 30, "#55607F")
        c.drawRect(R(-700, 0, 1420, 3), P("#FFFFFF", 0.16))
        # the customer desk and the pen on its chain
        box(c, -540, -92, 150, 92, "#7C5A3C", r=6)
        box(c, -552, -104, 174, 14, "#A9744A", r=4)
        gone = t >= s("tag") - 0.2
        if t >= T["pencut"] - 0.2 and not gone:
            pk = e_back(prog(t, T["pencut"], T["pen"] + 0.1))
            ch = skia.Path()
            ch.moveTo(-500, -104)
            ch.quadTo(-474, -70 - 16 * pk, -444, -106)
            c.drawPath(ch, dash_paint("#E5E9F2", 1.0, 4, 0, dash=6, gap=4))
            c.save()
            c.translate(-444, -108)
            c.rotate(-24)
            c.drawRRect(rr(-4, -44 * pk, 8, 44 * pk, 3), P("#2563EB"))
            c.drawRRect(rr(-3, -52 * pk, 6, 9, 2), P("#F8FAFC"))
            c.restore()
        c.drawRRect(rr(-506, -108, 12, 6, 2), P("#94A3B8"))                           # where the chain was screwed on
        if gone and t >= T["stolen"] - 0.25:                                          # there he goes, chain and all
            u = prog(t, T["stolen"] - 0.25, T["chain2"] + 0.6)
            tx = lerp(-380, -760, u)
            self.thief(c, tx, 0, t * 1.5, "walk", -1, 124)
            ch = skia.Path()
            ch.moveTo(tx - 34, -96)
            ch.quadTo(tx + 20, -70 + 12 * math.sin(t * 9), tx + 64, -88 + 10 * math.sin(t * 7))
            c.drawPath(ch, dash_paint("#E5E9F2", 1.0, 4, 0, dash=6, gap=4))
            c.drawRRect(rr(tx - 44, -128, 8, 36, 3), P("#2563EB"))
        # ---- the box, then the vault
        built = t >= T["built"] - 0.05
        if not built or t < T["built"] + 0.3:
            g = e_io(prog(t, T["built"] - 0.3, T["built"] + 0.25))                    # the box grows into a room
            a = 1 - g
            taken = T["grab"] <= t < s("fix1") - 0.12
            if True:
                box(c, BX - 60, -74, 120, 12, "#7C5A3C", r=4, a=a)                   # the table
                for tx in (BX - 50, BX + 50):
                    c.drawRect(R(tx - 4, -62, 8, 62), P("#5B3A22", a))
                if t < T["lock"] - 0.25:                                             # the money goes in
                    rng = random.Random(5)
                    for i in range(12):
                        t0 = 0.12 + i * (T["lock"] - 0.75) / 12
                        u = prog(t, t0, t0 + 0.5)
                        dx, rot = rng.uniform(-22, 22), rng.uniform(-30, 30)
                        if 0 < u < 1:
                            c.save()
                            c.translate(BX + dx * (1 - u), lerp(-330, -112, e_in(u)))
                            c.rotate(rot * (1 - u) + math.sin(t * 9 + i) * 10)
                            c.drawRRect(rr(-27, -14, 54, 28, 4), P("#22C55E"))
                            c.drawRRect(rr(-22, -9, 44, 18, 3), P("#86EFAC"))
                            c.drawCircle(0, 0, 7, P("#166534"))
                            c.restore()
                if not taken:
                    strongbox(c, lerp(BX, 320, g), lerp(-74, 0, g), 1.0 + 4.2 * g, prog(t, T["lock"] - 0.3, T["lock"] - 0.1),
                              prog(t, T["lock"] - 0.05, T["lock"] + 0.1), clamp(1 - g * 1.2))
        if built:
            k = e_out(prog(t, T["built"] - 0.05, T["concrete"] + 0.3))
            bars = prog(t, T["steel"] - 0.25, T["steel"] + 0.5)
            ht = -VTOP * k
            # inside the room
            c.drawRect(R(VX0 + WALL, -ht + WALL, VX1 - VX0 - 2 * WALL, max(0.0, ht - WALL)), P("#131A30"))
            if k >= 1:
                add_glow(c, 330, -300, 300, "#FFE9B8", 0.25)
                for sx in (180, 300, 420):
                    box(c, sx - 50, -214, 100, 8, "#64748B", r=2)
                    box(c, sx - 50, -110, 100, 8, "#64748B", r=2)
                    gold(c, sx, -214, 3)
                    gold(c, sx, -110, 2)
                    gold(c, sx, -2, 3)
            concrete(c, VX0, -ht, WALL, max(0.0, ht - DOORH), 3, bars=bars)
            concrete(c, VX1 - WALL, -ht, WALL, ht, 4, bars=bars)
            concrete(c, VX0, -ht, VX1 - VX0, WALL, 5, bars=bars)
            concrete(c, VX0 - 10, 0, VX1 - VX0 + 20, 34, 6, bars=bars)                # the floor slab
            if k >= 1:
                opened = prog(t, T["open"], T["open"] + 0.5) * (1 - prog(t, s("fix3") - 0.12, s("fix3")))
                c.drawRect(R(VX0, -DOORH, WALL, DOORH), P("#0B0F1E"))
                dy = -DOORH * 0.0
                c.save()                                                             # the door, edge on
                c.translate(VX0 + 4, 0)
                c.rotate(0)
                box(c, 0 - 70 * opened, -DOORH + 4 + dy, WALL - 8, DOORH - 8, STEELD, r=6)
                c.drawRect(R(4 - 70 * opened, -DOORH + 10, 6, DOORH - 20), P("#FFFFFF", 0.3))
                c.drawOval(R(-26 - 70 * opened, -160, 22, 70), P("#E5E9F2"))
                c.drawOval(R(-20 - 70 * opened, -148, 10, 46), P("#55607F"))
                c.restore()
            # sensors and microphones (fix 4)
            if t >= T["sensors"] - 0.15:
                for i, sx in enumerate((170, 280, 390, 500)):
                    sk = e_back(prog(t, T["sensors"] - 0.15 + i * 0.07, T["sensors"] + 0.1 + i * 0.07))
                    hot = t >= T["shake"] - 0.1
                    c.drawRRect(rr(sx - 24 * sk, 5, 48 * sk, 24 * sk, 6), P("#0B1220"))
                    c.drawRRect(rr(sx - 24 * sk, 5, 48 * sk, 24 * sk, 6), P("#E5E9F2", 0.7, stroke=2))
                    c.drawCircle(sx, 17, 7 * sk, P(WARN if hot else GOOD))
                    if hot and t < s("cta"):
                        for j in range(2):
                            u = (t * 1.8 + j * 0.5 + i * 0.2) % 1.0
                            c.drawCircle(sx, 17, 12 + 50 * u, P(WARN, 0.75 * (1 - u), stroke=4))
            if t >= T["microphones"] - 0.15:
                for i, (mx, my) in enumerate(((VX0 + 25, -300), (VX1 - 25, -300), (VX1 - 25, -120))):
                    mk = e_back(prog(t, T["microphones"] - 0.15 + i * 0.08, T["microphones"] + 0.1 + i * 0.08))
                    c.drawRRect(rr(mx - 13 * mk, my - 22 * mk, 26 * mk, 42 * mk, 13 * mk), P("#0B1220"))
                    c.drawRRect(rr(mx - 8 * mk, my - 17 * mk, 16 * mk, 24 * mk, 8 * mk), P("#7DD3FC"))
                if t >= T["scraping"] - 0.3 and t < T["caught"]:                      # the scraping, as sound
                    rx = self.ui.get("reach", 250)
                    for j in range(3):
                        u = (t * 1.5 + j / 3) % 1.0
                        c.drawArc(R(rx - 40 - 120 * u, 190 - 40 - 120 * u, 80 + 240 * u, 80 + 240 * u), 250, 80, False, P("#7DD3FC", 0.8 * (1 - u), stroke=4))
            if t >= T["alarm"] - 0.05 and t < s("cta"):                               # the alarm
                on = math.sin(t * 16) > 0
                c.drawRRect(rr(60, -470, 40, 26, 6), P("#7F1D1D"))
                c.drawCircle(80, -476, 16, P("#FF4D4F" if on else "#991B1B"))
                add_glow(c, 80, -476, 240, "#FF4D4F", 0.6 if on else 0.2)
        self.people(c, t)
        c.restore()
        self.ui["cam"] = cam

    def people(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        if t < s("break1") - 0.1:                                                     # the hook
            self.crew(c, t, "look" if t < T["lock"] else "cheer", xs=(84, 128, 172), face=1)
            return
        if t < s("fix1") - 0.12:                                                     # break 1: off he walks with it
            u1 = e_out(prog(t, s("break1") - 0.1, T["grab"]))
            u2 = e_in(prog(t, T["walks"] - 0.2, e("break1") + 0.3))
            tx = lerp(-260, BX - 54, u1) if t < T["walks"] - 0.2 else lerp(BX - 54, -420, u2)
            got = t >= T["grab"]
            self.thief(c, tx, 0, t * 1.3, "carry" if got else "walk", 1 if t < T["walks"] - 0.2 else -1, 128, bag=False)
            if got:
                strongbox(c, tx + (40 if t < T["walks"] - 0.2 else -40), -64, 0.9, 1.0, 1.0)
            self.crew(c, t, "stand" if not got else "shrug", xs=(386, 422, 458), face=-1, h=108)
            return
        if t < s("break2") - 0.1:                                                    # fix 1
            pose = "cheer" if t >= T["steel"] + 0.5 else "point" if t >= T["thick"] - 0.3 else "look"
            self.crew(c, t, pose, xs=(-112, -66, -20), face=1)
            return
        if t < s("fix2") - 0.12:                                                     # break 2: the drill
            t_go = min(T["back"] - 0.75, T["drill"] - 1.2)                              # he gives up pushing and runs off
            t_in = t_go + 0.42                                                       # ...and is back with a drill
            drilling = t >= T["drill"] + 0.1
            if t < t_go:                                                             # it will not move
                tx = lerp(-330, 14, e_out(prog(t, s("break2") - 0.1, s("break2") + 0.45)))
                heave = math.sin(t * 16) * 3 if tx >= 13 else 0
                self.thief(c, tx + heave, 0, t * 1.3, "carry" if tx >= 13 else "walk", 1, 128, bag=False)
                if tx >= 13:
                    for i in range(3):
                        u = (t * 1.6 + i / 3) % 1.0
                        c.drawCircle(tx - 14 - u * 26, -150 - u * 30 + i * 6, 5 * (1 - u), P("#7DD3FC", 1 - u))
            elif t < t_in:
                tx = lerp(14, -340, e_in(prog(t, t_go, t_in)))
                self.thief(c, tx, 0, t * 2.2, "walk", -1, 128, bag=False)
            else:
                arrive = e_out(prog(t, t_in, T["drill"] - 0.05))
                tx = lerp(-340, 10, arrive)
                self.thief(c, tx, 0, t * 2.0, "carry" if arrive >= 1 else "walk", 1, 128)
                c.save()                                                             # his drill
                c.translate(tx + 34, -86 + (math.sin(t * 60) * 1.5 if drilling else 0))
                box(c, 0, -14, 40, 28, "#F59E0B", r=6)
                c.drawRect(R(8, 14, 14, 26), P("#B45309"))
                c.drawRect(R(40, -4, 26 + (8 if drilling else 0), 8), P("#E5E9F2"))
                c.restore()
            if drilling:
                sparks_shower(c, VX0 + 2, -90, t, t - (t % 0.15), 0.3, n=8, speed=380, seed=int(t * 7), cone=(110, 250))
            self.crew(c, t, "look" if not drilling else "duck", xs=(-262, -216, -170), face=1)
            return
        if t < s("break4") - 0.12:                                                   # break 3: the manager, at midnight
            arrive = e_out(prog(t, s("break3") - 0.1, T["manager"] - 0.2))
            mx = lerp(-420, -10, arrive)
            person(c, mx, 0, 124, "#93C5FD", t * 1.2, "walk" if arrive < 1 else "carry" if t >= T["open"] - 0.2 else "shrug", face=1, hair="#9CA3AF", pants="#BFDBFE")
            nightcap(c, mx, 0, 124, 1)
            self.thief(c, mx - 76, 0, t * 1.2, "walk" if arrive < 1 else "point", 1, 128)
            return
        if t < s("cta"):                                                             # break 4 and fix 4: the tunnel
            if t < T["dig0"] + 0.4:                                                  # the door will not give
                leave = e_in(prog(t, T["dig0"] - 0.45, T["dig0"] + 0.2))
                tx = lerp(22, -330, leave)
                tug = t < T["hopeless"] - 0.15
                self.thief(c, tx + (math.sin(t * 15) * 3 if tug else 0), 0, t * 2.0, "carry" if tug else "shrug" if leave <= 0 else "walk",
                           1 if leave <= 0 else -1, 128, bag=False)
                self.crew(c, t, "look", xs=(-250, -204, -158), face=1)
                return
            rx = self.reach.at(t)
            if t >= T["caught"]:
                self.thief(c, rx - 56, 250, t, "cheer", 1, 104, bag=False)            # hands up
            if t >= T["police"] - 0.1:
                arrive = e_out(prog(t, T["police"] - 0.1, T["police"] + 0.6))
                for i in range(2):
                    px = lerp(-560 - i * 60, -130 - i * 76, arrive)
                    person(c, px, 0, 128, "#1D4ED8", t * 1.6 + i, "walk" if arrive < 1 else "point", face=1, hat="cap", pants="#1E3A8A")
                cx_ = lerp(-520, rx - 250, e_out(prog(t, T["police"] + 0.1, T["caught"])))    # and one down the tunnel, behind him
                person(c, cx_, 250, 104, "#1D4ED8", t * 1.6, "walk" if t < T["caught"] else "point", face=1, hat="cap", pants="#1E3A8A")
                light_cone(c, cx_ + 26, 176, 4, 250, 14, "#FFF3C4", 0.55)
            if t >= s("fix4") - 0.1:
                self.crew(c, t, "look" if t < T["caught"] else "cheer", xs=(-330, -284, -238) if t >= T["alarm"] - 0.35 else (-100, -56, -12), face=1)
            return
        if t >= s("tag") - 0.2:
            self.crew(c, t, "look" if t < T["stolen"] + 0.2 else "shrug", xs=(-330, -284, -238), face=-1)

    # ------------------------------------------------------------------ set: the door, from the front
    def draw_door(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.dcam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 3, cam[1], cam[2])
        self.view(c, cam)
        vrect(c, -1200, -1200, 2400, 2700, ["#2B3350", "#3B4566", "#20263F"], [0.0, 0.5, 1.0])      # the concrete wall around it
        rng = random.Random(3)
        for _ in range(120):
            c.drawCircle(rng.uniform(-900, 900), rng.uniform(-900, 1200), rng.uniform(2, 6), P("#000000" if rng.random() < 0.6 else "#FFFFFF", 0.06))
        box(c, -1200, 400, 2400, 40, "#55607F")
        early = t < s("break3")                                                      # fix 2
        tl_phase = s("fix3") - 0.12 <= t < s("break4")                               # fix 3
        final = t >= s("cta")
        opening = e_io(prog(t, T["cong2"] + 0.2, T["cong2"] + 1.4)) if final else 0.0
        R0 = 330
        c.drawCircle(0, 0, R0 + 46, lin_paint(-380, -380, 380, 380, ["#E5E9F2", "#7C8499", "#3F465A"]))     # the frame
        c.drawCircle(0, 0, R0 + 8, P("#0B0F1E"))
        if opening > 0:                                                              # what it was all for
            c.save()
            cp = skia.Path()
            cp.addCircle(0, 0, R0 + 8)
            c.clipPath(cp, skia.ClipOp.kIntersect, True)
            c.drawCircle(0, 0, R0 + 8, rad_paint(0, 40, R0 * 1.2, [("#5B4A1B", opening), ("#2A2210", opening), ("#0B0F1E", 1.0)]))
            for sy in (-90, 70, 230):
                c.drawRect(R(-340, sy, 680, 12), P("#64748B", opening))
                for gx in (-230, -115, 0, 115, 230):
                    gold(c, gx, sy, 4, opening)
            add_glow(c, 0, 40, 460, "#FDE047", 0.55 * opening)
            c.restore()
        for hy in (-150, 150):                                                       # hinges
            box(c, R0 + 10, hy - 34, 90, 68, "#7C8499", r=10)
        c.save()
        c.translate(R0, 0)
        c.scale(1 - 0.86 * opening, 1)
        c.translate(-R0, 0)
        c.drawCircle(0, 0, R0, rad_paint(-110, -130, R0 * 1.6, ["#F8FAFC", "#B8C2D4", "#64748B"]))
        for rr_ in (R0 - 34, R0 - 120):
            c.drawCircle(0, 0, rr_, P("#000000", 0.14, stroke=5))
        for i in range(24):
            an = math.radians(i * 15)
            c.drawCircle(math.cos(an) * (R0 - 18), math.sin(an) * (R0 - 18), 9, rad_paint(math.cos(an) * (R0 - 18) - 3, math.sin(an) * (R0 - 18) - 3, 12,
                                                                                         ["#FFFFFF", "#94A3B8", "#475569"]))
        shine = (t * 0.35) % 1.6 if final else -1
        if 0 <= shine <= 1:
            c.save()
            cp = skia.Path()
            cp.addCircle(0, 0, R0)
            c.clipPath(cp, skia.ClipOp.kIntersect, True)
            c.rotate(24)
            c.drawRect(R(-R0 - 200 + shine * 1100, -500, 90, 1000), P("#FFFFFF", 0.20))
            c.restore()
        xray = (early or tl_phase)
        if xray:
            self.inside_door(c, t, early)
        else:
            wheel(c, 0, 0, 112, self.spin.at(t))
        if tl_phase or final:                                                        # the time lock stays on the door
            self.time_lock(c, t)
        c.restore()
        # in front of the door
        if tl_phase and t >= T["code2"] - 0.3:                                       # two people, half a code each
            pk = prog(t, T["code2"] - 0.3, T["code2"])
            for sd, col in ((-1, SHIRTS[0]), (1, SHIRTS[2])):
                engineer(c, sd * lerp(520, 300, e_out(pk)), 400, 150, col, t + sd, "point", face=-sd)
        if final and t < T["pencut"]:
            self.crew(c, t, "look" if t < T["giant"] else "cheer", xs=(-300, -240, 250), y=400, face=1, h=140)
        if final and t >= T["s1"] - 0.35:
            xs = (-420, -360, -300)
            self.crew(c, t, "cheer", xs=xs, y=400, face=1, h=128)
            hats_in_the_air(c, xs, 230, t, T["cong2"])
        if early and T["drill2"] - 0.6 <= t:                                         # the drill, coming in from the corner
            u = e_io(prog(t, T["drill2"] - 0.6, T["crack"]))
            bx, by = lerp(-420, -70, u), lerp(470, 76, u)
            jit = math.sin(t * 70) * 2 if u > 0.3 and t < T["crack"] + 0.3 else 0
            c.save()
            c.translate(bx + jit, by)
            c.rotate(-48)
            c.drawRect(R(0, -7, 150, 14), lin_paint(0, -7, 0, 7, ["#F8FAFC", "#94A3B8"]))
            for i in range(7):
                c.drawLine(10 + i * 20, -7, 22 + i * 20, 7, P("#475569", 1, stroke=3))
            box(c, -150, -34, 150, 68, "#F59E0B", r=14)
            c.drawRect(R(-120, 30, 44, 80), P("#B45309"))
            c.restore()
            if u >= 1 and t < T["crack"] + 0.4:
                sparks_shower(c, -12, 20, t, T["crack"] - 0.05, 0.5, n=16, speed=520, seed=3, cone=(0, 360))
        c.restore()
        self.ui["cam"] = cam

    def inside_door(self, c, t, early):
        """The x-ray panel: lock, glass plate, spring bolts (fix 2); in fix 3 only the lock."""
        T = self.T
        c.drawRRect(rr(-200, -170, 400, 340, 30), P("#0D1730"))
        c.drawRRect(rr(-200, -170, 400, 340, 30), dash_paint("#FFFFFF", 0.5, 3, t))
        for an in (0, 90, 180, 270):                                                 # the main bolts
            c.save()
            c.rotate(an)
            c.drawRRect(rr(60, -14, 250, 28, 8), lin_paint(0, -14, 0, 14, ["#E5E9F2", "#7C8499"]))
            c.restore()
        box(c, -70, -56, 140, 112, "#475569", r=12)                                  # the lock
        c.drawCircle(0, 0, 30, P("#1B2238"))
        c.drawCircle(0, 0, 30, P(BRASS, 1, stroke=5))
        c.drawLine(0, 0, 0, -22, P(BRASS, 1, stroke=5))
        if not early:
            return
        broken = t >= T["crack"]
        gk = prog(t, T["glass"] - 0.15, T["glass"] + 0.15)
        if not broken:                                                               # the glass plate, in front of the lock
            c.drawRRect(rr(-96, -82, 192, 164, 8), P("#7DD3FC", 0.30 * gk))
            c.drawRRect(rr(-96, -82, 192, 164, 8), P("#E0F2FE", 0.9 * gk, stroke=4))
            c.drawLine(-70, -60, -20, -76, P("#FFFFFF", 0.7 * gk, stroke=4))
        else:
            dt = t - T["crack"]
            rng = random.Random(7)
            for i in range(16):
                an = rng.uniform(0, 6.283)
                sp = rng.uniform(120, 420)
                px, py = math.cos(an) * sp * dt, math.sin(an) * sp * dt + 400 * dt * dt
                c.save()
                c.translate(px, py)
                c.rotate(dt * rng.uniform(-400, 400))
                tri = skia.Path()
                tri.moveTo(-10, -8)
                tri.lineTo(14, 0)
                tri.lineTo(-6, 12)
                tri.close()
                c.drawPath(tri, P("#BAE6FD", clamp(1.2 - dt)))
                c.restore()
        fk = e_out(prog(t, T["fire"], T["fire"] + 0.12))                             # the spring bolts
        for an in (45, 135, 225, 315):
            c.save()
            c.rotate(an)
            x0 = 96
            ln = 40 + 170 * fk
            zz = skia.Path()
            zz.moveTo(x0, 0)
            n = 8
            for i in range(1, n + 1):
                zz.lineTo(x0 + ln * i / n * 0.55, (10 if i % 2 else -10))
            c.drawPath(zz, P("#94A3B8", 0.9 * gk, stroke=3))
            c.drawRRect(rr(x0 + ln * 0.55, -11, 70, 22, 6), P("#EF4444" if fk > 0 else "#7F1D1D", gk))
            c.restore()
        if fk >= 1:
            c.drawCircle(0, 0, 330, P(WARN, 0.5 + 0.3 * math.sin(t * 8), stroke=9))
        # the keypad, to the right
        box(c, 228, 10, 74, 100, "#1B2238", r=10)
        typed = clamp((t - T["code"] + 0.5) / 0.4) if t >= T["code"] - 0.5 else 0.0
        for i in range(4):
            c.drawCircle(244 + i * 14, 28, 4.5, P(GOOD if typed * 4 > i else "#334155"))
        for i in range(9):
            c.drawRRect(rr(238 + (i % 3) * 19, 42 + (i // 3) * 19, 14, 14, 3), P("#475569"))
        if t >= T["work"] - 0.15:
            c.drawCircle(265, 28, 18, P(WARN, 0.9 * prog(t, T["work"] - 0.15, T["work"]), stroke=5))
        self.ui["glass"] = (96, -40)
        self.ui["bolt"] = (150, -150)

    def time_lock(self, c, t):
        T, s = self.T, self.tl.s
        k = e_back(prog(t, T["time"] - 0.15, T["time"] + 0.2))
        if k <= 0:
            return
        c.save()
        c.translate(0, -212)
        c.scale(k, k)
        box(c, -130, -52, 260, 104, BRASS, r=14)
        c.drawRRect(rr(-130, -52, 260, 104, 14), P("#7A5A12", 1, stroke=4))
        for i, dx in enumerate((-82, 0, 82)):
            dk = e_back(clamp((t - T["three"] + 0.1) * 4 - i * 0.6)) if t < T["shut"] else 1.0
            c.drawCircle(dx, 0, 34 * dk, P("#F8FAFC"))
            c.drawCircle(dx, 0, 34 * dk, P("#1B2238", 1, stroke=4))
            a1 = math.radians(-90 + (t * 50 + i * 70))
            c.drawLine(dx, 0, dx + math.cos(a1) * 24 * dk, math.sin(a1) * 24 * dk, P("#EF4444", 1, stroke=3))
            c.drawLine(dx, 0, dx, -15 * dk, P("#1B2238", 1, stroke=4))
        c.restore()

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -200, 1.4)), x, y)

    def ui_bank(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        if tw < s("break1") - 0.1:
            x0, y0 = self.at(BX, -134)
            self.label(x0, y0, x0 + 60, y0 - 330, "box", T["box"] - 0.1, T["congrats"] + 0.2, HILITE)
        elif tw < s("fix1") - 0.12:
            self.badge("alert", T["grab"], s("fix1") - 0.2)
            self.red(T["grab"], 1.8)
        elif tw < s("break2") - 0.1:
            p = self.span(T["thick"] - 0.9, max(T["steel"] + 0.1, T["thick"] + 0.2))
            if p > 0:                                                                # how thick: across the left wall
                x0, y0 = self.at(VX0, VTOP - 36)
                x1, _ = self.at(VX0 + WALL, VTOP - 36)
                c.drawLine(x0, y0, x0 + (x1 - x0) * p, y0, P(HILITE, 1, stroke=5))
                for xx in (x0, x1):
                    c.drawLine(xx, y0 - 16, xx, y0 + 16, P(HILITE, p, stroke=5))
                v2.chip(c, (x0 + x1) / 2 + 60, y0 - 62, self.L["thick"], p, size=34, accent=HILITE)
            x2, y2 = self.at(VX0 + 25, -330)
            self.label(x2, y2, x2 - 250, y2 + 10, "bars", T["steel"] + 0.2, s("break2") - 0.25, "#F97316")
            self.badge("check", T["steel"] + 0.5, s("break2") - 0.15)
        elif tw < s("fix2") - 0.12:
            self.badge("alert", T["lock2"] - 0.3, s("fix2") - 0.2, x=880, y=420)
            self.red(T["lock2"] - 0.3, 1.8)
        elif tw < s("break4") - 0.12:
            self.badge("alert", T["open"], s("fix3") - 0.2, x=880, y=420)
            self.red(T["open"], 1.8)
        elif tw < s("cta"):
            rx = self.reach.at(tw)
            if tw < s("fix4") - 0.1:
                x0, y0 = self.at(rx - 210, 150)
                self.label(x0, y0 - 60, x0 - 60, y0 - 160, "tunnel", T["tunnel"] + 0.1, s("fix4") - 0.2, WARN)
                self.badge("alert", T["tunnel"], s("fix4") - 0.2, x=880, y=420)
                self.red(T["tunnel"], 1.8)
            else:
                x0, y0 = self.at(390, 22)
                self.label(x0, y0, x0 + 40, y0 + 240, "sens", T["sensors"] + 0.2, T["microphones"] - 0.15, WARN)
                x1, y1 = self.at(VX1 - 25, -300)
                self.label(x1, y1, x1 - 60, y1 - 200, "mic", T["microphones"] + 0.15, T["alarm"] - 0.4, "#7DD3FC")
                x2, y2 = self.at(-168, -140)
                self.label(x2, y2, x2 - 40, y2 - 250, "police", T["police"] + 0.5, s("cta") - 0.3, "#60A5FA")
                self.badge("check", T["caught"] + 0.2, 1e9, x=880, y=420)
        elif tw < T["s1"] - 0.35:
            x0, y0 = self.at(-444, -150)
            self.label(x0, y0, x0 + 250, y0 - 250, "pen", T["pen"] + 0.1, T["s1"] - 0.5, HILITE)
        elif tw >= s("tag") - 0.2:
            x0, y0 = self.at(-500, -108)
            self.label(x0, y0, x0 + 300, y0 - 330, "gone", T["day"] - 0.1, self.duration + 1, HILITE)

    def ui_door(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.ui.get("cam", (0, 174, 1.15))
        low = H / 2 + (376 - cam[1]) * cam[2]                                        # where the bottom of the door frame is on screen
        if low > 1236:
            c.drawRRect(rr(30, self.CAPTION_Y - 105, W - 60, 190, 44), P("#0B1024", 0.62 * clamp((low - 1236) / 40), blur=22))
        if tw < s("break3"):
            gx, gy = self.at(*self.ui.get("glass", (96, -40)))
            self.label(gx, gy, 800, gy - 330, "glass", T["glass"] + 0.1, T["drill2"] - 0.1, "#7DD3FC")
            bx, by = self.at(*self.ui.get("bolt", (150, -150)))
            self.label(bx, by, 290, by - 250, "bolts", T["fire"] + 0.1, T["code"] - 0.4, "#EF4444")
            self.chip(540, 420, "nocode", T["work"] - 0.2, s("break3") - 0.2, accent=WARN, size=36)
            self.badge("check", T["jam"] + 0.4, s("break3") - 0.15, x=200, y=1120)
        elif tw < s("break4"):
            x0, y0 = self.at(0, -264)
            self.label(x0 + 80, y0, 800, y0 - 130, "tlock", T["time"] + 0.2, T["shut"] - 0.1, BRASS)
            self.chip(540, 390, "morning", T["shut"], T["code2"] - 0.4, accent=HILITE, size=38)
            p = self.span(T["code2"] - 0.1, s("break4") - 0.2)
            if p > 0:                                                                # half a code each, then the whole one
                join = e_io(prog(tw, T["two"] + 0.5, T["two"] + 0.9))
                v2.chip(c, lerp(250, 478, join), 420, "47", p, size=54, accent=SHIRTS[0])
                v2.chip(c, lerp(830, 602, join), 420, "19", p, size=54, accent=SHIRTS[2])
                if join >= 1:
                    v2.badge(c, 540, 300, prog(tw, T["two"] + 0.9, T["two"] + 1.1), "check", t, 0.8)
            self.chip(540, 1150, "two", T["two"] - 0.1, T["sleep"] - 0.3, accent=HILITE, size=36)
            p2 = self.span(T["sleep"] - 0.5, s("break4") - 0.2)
            if p2 > 0:                                                               # the manager, asleep at home
                cx_, cy_, r = 205, 1075, 150 * e_back(p2)
                c.save()
                cp = skia.Path()
                cp.addCircle(cx_, cy_, r)
                c.clipPath(cp, skia.ClipOp.kIntersect, True)
                c.drawCircle(cx_, cy_, r, lin_paint(0, cy_ - r, 0, cy_ + r, ["#27336B", "#1A2350"]))
                c.drawCircle(cx_ + 78, cy_ - 84, 24, P("#FDF6C8"))                   # the moon
                c.drawCircle(cx_ + 90, cy_ - 92, 22, P("#27336B"))
                c.drawRRect(rr(cx_ - 150, cy_ + 44, 300, 120, 10), P("#5B3A22"))      # the bed
                c.drawRRect(rr(cx_ - 128, cy_ - 30, 26, 110, 8), P("#7C5A3C"))
                c.drawRRect(rr(cx_ - 100, cy_ + 2, 78, 44, 16), P("#F8FAFC"))         # pillow
                c.drawCircle(cx_ - 62, cy_ + 6, 30, P("#E8B48A"))                     # his head
                c.drawLine(cx_ - 74, cy_ + 4, cx_ - 62, cy_ + 8, P("#2B2530", 1, stroke=4))
                cap = skia.Path()
                cap.moveTo(cx_ - 90, cy_ - 4)
                cap.lineTo(cx_ - 40, cy_ - 22)
                cap.lineTo(cx_ - 104, cy_ - 60)
                cap.close()
                c.drawPath(cap, P("#60A5FA"))
                c.drawCircle(cx_ - 104, cy_ - 60, 9, P("#F8FAFC"))
                c.drawRRect(rr(cx_ - 44, cy_ + 14, 200, 60, 22), P("#8B5CF6"))        # blanket
                c.drawRRect(rr(cx_ - 44, cy_ + 14, 200, 16, 8), P("#C4B5FD"))
                c.restore()
                c.drawCircle(cx_, cy_, r, P("#93C5FD", p2, stroke=6))
                for j in range(3):
                    u = (t * 0.6 + j / 3) % 1.0
                    text(c, "Z", cx_ - 20 + u * 90, cy_ - 30 - u * 90, 30 + 34 * u, "#FFFFFF", "Poppins-Black", a=min(1.0, 2.5 * (1 - u)) * p2)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.pop(61), -6)]
        ev += [(T["money"] - 0.2 + i * 0.13, sfx.tap(62 + i), -9) for i in range(5)]
        ev += [(T["lock"] - 0.3, sfx.thud(0.25, 68), -5), (T["lock"], sfx.lock_click(69), -1), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 70), -9)]
        ev += [(s("break1"), sfx.tap(71), -11), (s("break1") + 0.25, sfx.tap(72), -11), (T["grab"], sfx.pop(73), -5), (T["grab"] + 0.05, sfx.alarm(3, 820), -11),
               (T["packed"] + 0.3, sfx.womp(), -9)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["built"] - 0.05, rumble(0.7, 75), -10), (T["concrete"] + 0.32, sfx.thud(0.3, 76), -8),
               (T["thick"] - 0.9, sfx.pop(77), -9), (T["steel"] - 0.25, sfx.clank(520, 0.3, 78), -6), (T["steel"], sfx.clank(600, 0.3, 79), -7),
               (T["steel"] + 0.5, sfx.chime(), -6)]
        ev += [(T["drill"] + 0.1, drill_snd(max(0.6, s("fix2") - T["drill"] - 0.3), 80), -7), (T["lock2"] - 0.3, sfx.alarm(3, 820), -11)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 81), -4), (T["glass"] - 0.15, sfx.pop(82), -6),
               (T["drill2"] - 0.5, drill_snd(max(0.4, T["crack"] - T["drill2"] + 0.5), 83), -10), (T["crack"], glass_snd(84), -2),
               (T["fire"], sfx.clank(240, 0.5, 85), -1), (T["fire"] + 0.06, sfx.clank(300, 0.4, 86), -3), (T["jam"] + 0.4, sfx.chime(), -7),
               (T["code"] - 0.5, sfx.beep(1500, 0.06), -9), (T["code"] - 0.4, sfx.beep(1500, 0.06), -9), (T["code"] - 0.3, sfx.beep(1500, 0.06), -9),
               (T["code"] - 0.2, sfx.beep(1900, 0.06), -9), (T["work"] - 0.1, sfx.buzz(0.35), -7)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 87), -4), (T["manager"] - 0.2, sfx.pop(88), -8), (T["open"], sfx.creak(0.7, 89), -4),
               (T["open"] + 0.1, sfx.alarm(3, 820), -11), (T["midnight"], sfx.bell(520, 1.2, 0.5), -8)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 90), -4), (T["time"] - 0.15, sfx.thud(0.3, 91), -4)]
        ev += [(T["three"] + i * 0.15, sfx.tick(), -6) for i in range(3)]
        ev += [(T["shut"] + i * 0.3, sfx.tick(), -12) for i in range(8)]
        ev += [(T["shut"], sfx.lock_click(92), -3), (T["code2"] - 0.1, sfx.pop(93), -6), (T["code2"], sfx.pop(94), -7), (T["two"] + 0.9, sfx.chime(), -6),
               (T["sleep"] - 0.5, sfx.pop(95), -7)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 96), -4)]
        ev += [(T["dig0"] + i * 0.24, dig_snd(97 + i), -7) for i in range(int(max(1, (s("fix4") - T["dig0"]) / 0.24)))]
        ev += [(T["tunnel"], sfx.alarm(3, 820), -11)]
        ev += [(T["sensors"] - 0.15 + i * 0.07, sfx.beep(1400 + i * 120, 0.06), -8) for i in range(4)]
        ev += [(T["shake"] - 0.1, rumble(0.9, 120), -8), (T["microphones"] - 0.15, sfx.pop(121), -6), (T["scraping"] - 0.3, dig_snd(122), -6),
               (T["scraping"], dig_snd(123), -6), (T["alarm"], sfx.alarm(8, 1150, 0.11, 0.07), -7), (T["police"], siren(1.6), -9),
               (T["caught"], sfx.pop(124), -4), (T["caught"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(125), 0), (T["follow"] - 0.15, sfx.pop(126), -4), (s("cta") + 0.05, sfx.whoosh(0.4, True, 127), -7)]
        ev += [(T["giant"], sfx.thud(0.4, 128), -6), (T["wheel"] - 0.1, sfx.whirr(1.0, 160, 300, 129), -9), (T["wheel"] + 0.4, sfx.sparkle(0.7, 9, 130), -8),
               (T["pencut"], sfx.whoosh(0.4, False, 131), -6), (T["pen"], sfx.pop(132), -5), (T["chain"], sfx.clank(900, 0.2, 133), -9)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 134), -6), (T["s1"], sfx.pop(135), -3), (T["s2"], sfx.pop(136), -3), (T["s3"], sfx.pop(137), -3)]
        ev += [(T["cong2"], sfx.pop(138), -2), (T["cong2"], sfx.sparkle(1.0, 14, 139), -4), (T["cong2"] + 0.2, sfx.creak(1.0, 140), -6),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 141), -6), (T["stolen"] - 0.2, sfx.tap(142), -8), (T["stolen"], sfx.tap(143), -8),
               (T["stolen"] + 0.2, sfx.tap(144), -9), (T["chain2"] - 0.2, sfx.clank(900, 0.25, 145), -7), (T["chain2"] + 0.3, sfx.womp(), -3)]
        return ev


NAME = "vault"
EPISODE = Vault
