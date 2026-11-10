"""Episode 8 - A claw machine.  v2 look: one arcade interior seen from the front, four cameras with whip cuts.

World (floor at y = 0): the machine stands at x = 0.  Base cabinet (y -280..-14) with the prize door, the speaker and -
in the cutaway - the coin box, the computer board, the shake sensor; feet and floor bolts under it; control panel
(-310..-280); glass box (-790..-310) with the chute column on the left, the toy pile, the gantry and the claw;
marquee (-900..-790).  The kids stand on the left, the crew on the right.
"""
from v2_base import *  # noqa: F401,F403

BODY, TRIM, METAL, COPPER = "#E11D74", "#FACC15", "#C9D1E4", "#F59E0B"
MW, PANEL, GTOP, TOP, RAIL = 230, -310, -790, -900, -762      # half width, glass floor, glass top, machine top, gantry
CH0, CH1, CHTOP = -216, -104, -420                            # the chute column inside the glass
DOOR = (-212, -200, 104, 130)                                 # the prize door on the front of the base
DOORC = (-160, -135)
HOME = -160                                                   # the claw parks above the chute
KX, KH = (-316, -366, -414), (96, 88, 100)                    # where the three kids stand, how tall they are
KCOL = (("#22D3EE", "cap"), ("#F97316", "none"), ("#A3E635", "cap"))
TED = (58, -312, 0.9)                                         # the giant teddy: x, y it sits on, scale

PILE = []                                                     # (x, y, radius, kind, tilt) from the bottom row up
_rng = random.Random(8)
for _row in range(3):
    for _i in range(6 - _row % 2):
        PILE.append([-72 + _i * 52 + (26 if _row % 2 else 0) + _rng.uniform(-4, 4), -337 - _row * 44 + _rng.uniform(-3, 3),
                     27 + _rng.uniform(-2, 2), _rng.randrange(5), _rng.uniform(-16, 16)])
PILE[13][3], PILE[14][3], PILE[11][3] = 0, 1, 3               # the bear, the duck and the frog that star in the story


# ====================================================================================== pieces
def star_path(x, y, r1, r2, n=5, rot=-90.0):
    p = skia.Path()
    for i in range(n * 2):
        a = math.radians(rot + i * 180.0 / n)
        r = r1 if i % 2 == 0 else r2
        px, py = x + math.cos(a) * r, y + math.sin(a) * r
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close()
    return p


def toy(c, kind, x, y, r, rot=0.0, a=1.0):
    """A plush toy (just the round head), centre (x, y). kind: 0 bear, 1 duck, 2 bunny, 3 frog, 4 pink blob."""
    if a <= 0:
        return
    kind %= 5
    col = ("#B5793F", "#FACC15", "#F5F3FF", "#4ADE80", "#F472B6")[kind]
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    if kind == 0:
        for sd in (-1, 1):
            c.drawCircle(sd * r * 0.72, -r * 0.72, r * 0.36, P(shade(col, -0.15)))
            c.drawCircle(sd * r * 0.72, -r * 0.72, r * 0.18, P("#E9C39A"))
    elif kind == 2:
        for sd in (-1, 1):
            c.drawRRect(rr(sd * r * 0.45 - r * 0.2, -r * 1.75, r * 0.4, r * 1.1, r * 0.2), P(col))
            c.drawRRect(rr(sd * r * 0.45 - r * 0.09, -r * 1.6, r * 0.18, r * 0.8, r * 0.09), P("#F9A8D4"))
    elif kind == 3:
        for sd in (-1, 1):
            c.drawCircle(sd * r * 0.5, -r * 0.8, r * 0.36, P(col))
    c.drawCircle(0, 0, r, rad_paint(-r * 0.35, -r * 0.4, r * 1.5, [shade(col, 0.25), col, shade(col, -0.35)]))
    ey = -r * 0.8 if kind == 3 else -r * 0.12
    for sd in (-1, 1):
        ex = sd * r * (0.5 if kind == 3 else 0.36)
        if kind == 3:
            c.drawCircle(ex, ey, r * 0.22, P("#FFFFFF"))
        c.drawCircle(ex, ey, r * 0.12, P("#1B1B2B"))
        c.drawCircle(ex - r * 0.04, ey - r * 0.05, r * 0.045, P("#FFFFFF"))
    if kind == 0:
        c.drawOval(R(-r * 0.34, r * 0.05, r * 0.68, r * 0.5), P("#E9C39A"))
        c.drawOval(R(-r * 0.13, r * 0.1, r * 0.26, r * 0.18), P("#3A2414"))
    elif kind == 1:
        c.drawOval(R(-r * 0.34, r * 0.08, r * 0.68, r * 0.36), P("#FB923C"))
    elif kind == 2:
        c.drawCircle(0, r * 0.2, r * 0.11, P("#F472B6"))
    else:
        c.drawArc(R(-r * 0.4, -r * 0.2, r * 0.8, r * 0.66), 25, 130, False, P("#14532D" if kind == 3 else "#831843", 1, stroke=r * 0.1))
        if kind == 4:
            for sd in (-1, 1):
                c.drawCircle(sd * r * 0.6, r * 0.22, r * 0.15, P("#FB7185", 0.7))
    if a < 1:
        c.restore()
    c.restore()


def teddy(c, x, y, s=1.0, squash=0.0, stretch=0.0, sleepy=False, a=1.0):
    """The giant teddy bear, sitting on (x, y). At s = 1 he is about 290 wide and 380 tall."""
    if a <= 0:
        return
    col, light = "#B5793F", "#E9C39A"
    c.save()
    c.translate(x, y)
    c.scale(s * (1 + squash * 0.10), s * (1 - squash * 0.10))
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    for sd in (-1, 1):                                                               # legs
        c.drawOval(R(sd * 95 - 55, -72, 110, 78), rad_paint(sd * 95 - 15, -52, 90, [shade(col, 0.2), col, shade(col, -0.35)]))
        c.drawOval(R(sd * 118 - 26, -58, 52, 50), P(light))
    c.drawOval(R(-112, -215, 224, 205), rad_paint(-40, -160, 230, [shade(col, 0.22), col, shade(col, -0.4)]))
    c.drawOval(R(-66, -170, 132, 130), P(light, 0.9))
    for sd in (-1, 1):                                                               # arms
        c.save()
        c.translate(sd * 104, -172)
        c.rotate(sd * -24)
        c.drawOval(R(-28, 0, 56, 112), rad_paint(-8, 30, 80, [shade(col, 0.2), col, shade(col, -0.35)]))
        c.restore()
    hy = -292 - stretch
    for sd in (-1, 1):
        c.drawCircle(sd * 62, hy - 58, 30, P(shade(col, -0.12)))
        c.drawCircle(sd * 62, hy - 58, 15, P(light))
    if stretch > 0:
        c.drawRect(R(-40, hy + 40, 80, 60), P(col))
    c.drawCircle(0, hy, 82, rad_paint(-28, hy - 30, 130, [shade(col, 0.25), col, shade(col, -0.38)]))
    c.drawOval(R(-36, hy + 4, 72, 52), P(light))
    c.drawOval(R(-14, hy + 10, 28, 19), P("#3A2414"))
    for sd in (-1, 1):
        if sleepy:
            c.drawArc(R(sd * 32 - 12, hy - 26, 24, 16), 0, 180, False, P("#1B1B2B", 1, stroke=5))
        else:
            c.drawCircle(sd * 32, hy - 16, 9.5, P("#1B1B2B"))
            c.drawCircle(sd * 32 - 3, hy - 19, 3.2, P("#FFFFFF"))
    for sd in (-1, 1):                                                               # bow tie
        p = skia.Path()
        p.moveTo(0, -214)
        p.lineTo(sd * 38, -236)
        p.lineTo(sd * 38, -192)
        p.close()
        c.drawPath(p, P("#EF4444"))
    c.drawCircle(0, -214, 10, P("#B91C1C"))
    if a < 1:
        c.restore()
    c.restore()


def claw(c, x, hy, op, grip=0.0):
    """Three-finger claw hanging at hub centre (x, hy). op 0 shut .. 1 wide open; grip 0..1 lights the coil."""
    tipx, midx = 10 + 54 * op, 30 + 30 * op
    c.drawLine(x, hy + 16, x, hy + 84, P("#8E97AD", 1, stroke=7))
    for sd in (-1, 1):
        path = skia.Path()
        path.moveTo(x + sd * 13, hy + 14)
        path.quadTo(x + sd * (midx + 16), hy + 40, x + sd * midx, hy + 66)
        path.quadTo(x + sd * (midx - 2), hy + 92, x + sd * tipx, hy + 106)
        c.drawPath(path, P("#2B3248", 1, stroke=13))
        c.drawPath(path, P(METAL, 1, stroke=8))
        c.drawCircle(x + sd * tipx, hy + 106, 6.5, P(TRIM))
        c.drawCircle(x + sd * 13, hy + 14, 6, P("#5B657E"))
    cyl(c, x - 23, hy - 20, 46, 38, "#3A4258", r=8)
    for i in range(4):                                                               # the coil
        c.drawRect(R(x - 23, hy - 15 + i * 8, 46, 4.5),
                   lin_paint(x - 23, 0, x + 23, 0, [shade(COPPER, -0.35), mix(COPPER, "#FFE3A1", grip * 0.6), shade(COPPER, -0.45)]))
    if grip > 0.05:
        add_glow(c, x, hy, 70, "#FFB347", 0.75 * grip)
        add_glow(c, x, hy, 150, "#FF8A3D", 0.25 * grip)
    c.drawRRect(rr(x - 8, hy - 30, 16, 12, 4), P("#8E97AD"))


def cabinet(c, x, hue, t, i=0):
    """Another arcade machine against the back wall, half in the dark."""
    w, h = 150, 430
    box(c, x - w / 2, -h, w, h, "#1A1740", r=8)
    c.drawRect(R(x - w / 2, -h, 6, h), P("#FFFFFF", 0.05))
    box(c, x - w / 2 - 6, -h - 34, w + 12, 40, "#231E58", r=8)
    c.drawRRect(rr(x - w / 2 + 8, -h - 26, w - 16, 22, 5), P(hue, 0.55))
    add_glow(c, x, -h - 15, 70, hue, 0.35)
    fl = 0.75 + 0.25 * math.sin(t * (5 + i) + i)
    c.drawRRect(rr(x - w / 2 + 14, -h + 26, w - 28, 120, 8), P("#05040E"))
    vrect(c, x - w / 2 + 20, -h + 32, w - 40, 108, [(hue, 0.75 * fl), (shade(hue, -0.5), 0.75 * fl)], r=5)
    add_glow(c, x, -h + 86, 150, hue, 0.30 * fl)
    box(c, x - w / 2 - 4, -h + 160, w + 8, 30, "#2B2568", r=5)
    for dx, col in ((-30, "#EF4444"), (14, "#FACC15"), (36, "#22D3EE")):
        c.drawCircle(x + dx, -h + 166, 7, P(col))
    c.drawRRect(rr(x - 22, -90, 44, 26, 4), P("#0B0A20"))
    c.drawRect(R(x - w / 2 - 6, -h - 34, w + 12, h + 34), P("#0B0820", 0.32))


def neon(c, path, col, k, w=7):
    if k <= 0:
        return
    c.drawPath(path, P(col, 0.35 * clamp(k), stroke=w * 3, blur=14))
    c.drawPath(path, P(col, clamp(k), stroke=w))
    c.drawPath(path, P("#FFFFFF", 0.75 * clamp(k), stroke=w * 0.35))


def note(c, x, y, s, col, a):
    if a <= 0:
        return
    c.drawOval(R(x - s * 0.62, y - s * 0.42, s * 1.24, s * 0.84), P(col, a))
    c.drawLine(x + s * 0.52, y, x + s * 0.52, y - s * 2.1, P(col, a, stroke=s * 0.24))
    c.drawLine(x + s * 0.52, y - s * 2.1, x + s * 1.3, y - s * 1.7, P(col, a, stroke=s * 0.34))
    add_glow(c, x, y, s * 2.4, col, 0.35 * a)


def coin(c, x, y, r, a=1.0, spin=0.0):
    w = r * (0.25 + 0.75 * abs(math.cos(spin)))
    c.drawOval(R(x - w, y - r, w * 2, r * 2), rad_paint(x - w * 0.3, y - r * 0.4, r * 1.8, [("#FFF3B0", a), ("#FACC15", a), ("#B7791F", a)]))
    c.drawOval(R(x - w * 0.6, y - r * 0.6, w * 1.2, r * 1.2), P("#B7791F", 0.45 * a, stroke=max(1.0, r * 0.12)))


def coin_snd(k=0):
    a, b = sfx.bell(2300 + (k % 3) * 150, 0.24, 1.0), sfx.bell(3460 + (k % 3) * 210, 0.16, 0.6)
    out = np.zeros(max(len(a), len(b)))
    out[:len(a)] += a
    out[:len(b)] += b
    return sfx._norm(out, 0.6)


def jingle(loops=1):
    """The song that never stops: a bouncy eight-note arcade loop."""
    notes, step = (659, 784, 1047, 784, 880, 784, 659, 523), 0.17
    out = np.zeros(int((len(notes) * step * loops + 0.3) * sfx.SR))
    for k in range(len(notes) * loops):
        f, m = notes[k % len(notes)], int(step * 0.92 * sfx.SR)
        tt = np.arange(m) / sfx.SR
        tone = (np.sign(np.sin(2 * np.pi * f * tt)) * 0.35 + np.sin(2 * np.pi * f * tt)) * sfx._ar(m, 0.005, step * 0.5)
        i = int(k * step * sfx.SR)
        out[i:i + m] += tone
    return sfx._norm(sfx._lp(out, 4200), 0.6)


# ====================================================================================== the episode
class Claw(EpisodeV2):
    BUILD_NO = 8
    FIRST_SET = "front"
    CLEAR = "#0B0A24"
    TITLE = {"en": "CLAW MACHINE", "ar_sa": "مكينة الألعاب"}
    EMPH = {"en": ["CONGRATS", "CLAW", "WINS", "EMPTY", "ELECTROMAGNET", "DIAL", "WEAK", "NOBODY", "COMPUTER", "COINS", "PROFIT",
                   "TIGHT", "ACCOUNTING", "SHAKES", "CHUTE", "BOLT", "SENSOR", "ALARM", "STUCK", "REALLY", "LOCK", "BEAM", "FOLLOW",
                   "SUBMARINE", "GIANT", "ZERO", "YOURSELF", "BIGGER", "LIVES"],
            "ar_sa": ["مبروك", "كماشة", "يفوز", "يفضى", "بمغناطيس", "مفتاح", "ترتخي", "محد", "كمبيوتر", "الريالات", "ربحك", "بقوة",
                      "حسابات", "يهز", "الفتحة", "ببراغي", "حساس", "وصفارة", "ويعلق", "صدق", "فتقفل", "ضوء", "تابعني", "غواصة",
                      "ضخم", "وصفر", "بيدك", "أكبر", "ساكن"]}
    KEYS = {"ar_sa": {
        ("hook", "HANG"): "علّقت", ("hook", "CLAW"): "كماشة", ("hook", "TOYS"): "ألعاب", ("hook", "CONGRATS"): "مبروك",
        ("break1", "NEVER"): "تفك", ("break1", "WINS"): "يفوز", ("break1", "EMPTY"): "يفضى",
        ("fix1", "ELECTROMAGNET"): "بمغناطيس", ("fix1", "DIAL"): "مفتاح", ("fix1", "LIFT"): "ترفع", ("fix1", "WEAK"): "ترتخي",
        ("fix1", "DROP"): "وتطيحها",
        ("break2", "NOBODY"): "محد", ("break2", "PLAYS"): "يلعب",
        ("fix2", "COMPUTER"): "كمبيوتر", ("fix2", "COINS"): "الريالات", ("fix2", "PRIZE"): "سعر", ("fix2", "PROFIT"): "ربحك",
        ("fix2", "TIGHT"): "بقوة", ("fix2", "LUCK"): "حظ", ("fix2", "ACCOUNTING"): "حسابات",
        ("break3", "SHAKES"): "يهز", ("break3", "TUMBLES"): "تطيح", ("break3", "CHUTE"): "الفتحة",
        ("fix3", "BOLT"): "ببراغي", ("fix3", "SENSOR"): "حساس", ("fix3", "SHOVE"): "دفّة", ("fix3", "LETS"): "تفك",
        ("fix3", "ALARM"): "وصفارة",
        ("break4", "KID"): "ولد", ("break4", "CRAWLS"): "يدخل", ("break4", "STUCK"): "ويعلق", ("break4", "HAPPENS"): "تصير",
        ("fix4", "LOCK"): "فتقفل", ("fix4", "LIGHT"): "ضوء", ("fix4", "OPENS"): "ينفتح", ("fix4", "DROPS"): "طاحت",
        ("cta", "COIN"): "ريال", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "FLASHING"): "أنوار", ("reveal", "SONG"): "وأغنية", ("reveal", "GIANT"): "ودبدوب", ("reveal", "LIFT"): "يرفعه",
        ("stat", "ONE"): "ريال", ("stat", "TWENTY"): "عشرين", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TEDDY"): "والدبدوب", ("tag", "BIGGER"): "أكبر", ("tag", "LIVES"): "ساكن"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a submarine"),
                   "stat": [("1", "COIN"), ("20", "SECONDS"), ("0", "REFUNDS")],
                   "L": {"claw": "A CLAW", "toys": "TOYS LEFT", "magnet": "ELECTROMAGNET", "grip": "GRIP POWER", "nocoins": "NO COINS",
                         "computer": "COMPUTER", "cost": "PRIZE COST", "profit": "+ YOUR PROFIT", "math": "PURE MATH",
                         "chute": "PRIZE CHUTE", "bolts": "FLOOR BOLTS", "sensor": "SHAKE SENSOR", "alarm": "ALARM",
                         "true": "TRUE STORY", "lock": "DOOR LOCK", "beam": "LIGHT BEAM", "pdoor": "PRIZE DOOR", "home": "HIS HOUSE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: غواصة"),
                      "stat": [("1", "ريال"), ("20", "ثانية"), ("0", "ترجيع")],
                      "L": {"claw": "كماشة", "toys": "الألعاب الباقية", "magnet": "مغناطيس كهربائي", "grip": "قوة المسكة",
                            "nocoins": "ولا ريال", "computer": "كمبيوتر", "cost": "سعر اللعبة", "profit": "وفوقها ربحك",
                            "math": "حسابات", "chute": "فتحة الجوايز", "bolts": "براغي في الأرض", "sensor": "حساس هز",
                            "alarm": "صفارة إنذار", "true": "قصة حقيقية", "lock": "قفل الباب", "beam": "حساس ضوء",
                            "pdoor": "باب الجوايز", "home": "بيته"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "hang": ("hook", "HANG", 0.1), "claw": ("hook", "CLAW", 0.22), "toys": ("hook", "TOYS", 0.5), "congrats": ("hook", "CONGRATS", 0.58),
            "never": ("break1", "NEVER", 0.12), "wins": ("break1", "WINS", 0.5), "empty": ("break1", "EMPTY", 0.8),
            "magnet": ("fix1", "ELECTROMAGNET", 0.2), "dial": ("fix1", "DIAL", 0.42), "lift": ("fix1", "LIFT", 0.6),
            "weak": ("fix1", "WEAK", 0.75), "drop": ("fix1", "DROP", 0.86),
            "nobody": ("break2", "NOBODY", 0.12), "plays": ("break2", "PLAYS", 0.85),
            "computer": ("fix2", "COMPUTER", 0.08), "coins": ("fix2", "COINS", 0.24), "prize": ("fix2", "PRIZE", 0.43),
            "profit": ("fix2", "PROFIT", 0.54), "tight": ("fix2", "TIGHT", 0.7), "luck": ("fix2", "LUCK", 0.8),
            "accounting": ("fix2", "ACCOUNTING", 0.9),
            "shakes": ("break3", "SHAKES", 0.2), "tumbles": ("break3", "TUMBLES", 0.6), "chute": ("break3", "CHUTE", 0.9),
            "bolt": ("fix3", "BOLT", 0.05), "sensor": ("fix3", "SENSOR", 0.3), "shove": ("fix3", "SHOVE", 0.42),
            "lets": ("fix3", "LETS", 0.56), "alarm": ("fix3", "ALARM", 0.72),
            "kid": ("break4", "KID", 0.2), "crawls": ("break4", "CRAWLS", 0.25), "stuck": ("break4", "STUCK", 0.6),
            "happens": ("break4", "HAPPENS", 0.9),
            "lock": ("fix4", "LOCK", 0.08), "beam": ("fix4", "LIGHT", 0.36), "opens": ("fix4", "OPENS", 0.62), "drops": ("fix4", "DROPS", 0.8),
            "coin": ("cta", "COIN", 0.3), "follow": ("cta", "FOLLOW", 0.42),
            "flashing": ("reveal", "FLASHING", 0.18), "song": ("reveal", "SONG", 0.38), "giant": ("reveal", "GIANT", 0.66),
            "lift2": ("reveal", "LIFT", 0.93),
            "s1": ("stat", "ONE", 0.04), "s2": ("stat", "TWENTY", 0.33), "s3": ("stat", "ZERO", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "teddy": ("tag", "TEDDY", 0.2), "bigger": ("tag", "BIGGER", 0.42), "lives": ("tag", "LIVES", 0.75)})
        T["built"] = T["congrats"] + 0.4
        T["kid0"] = min(T["kid"], T["crawls"]) - 0.15               # the small kid walks into the picture
        T["crawl0"] = max(T["crawls"] + 0.15, T["kid0"] + 0.5)      # ... and starts to climb through the door
        T["lock"] = max(T["lock"], s("fix4") + 0.55)                # (she has to be out again before it locks)
        T["land"] = T["giant"] + 0.3                              # the giant teddy hits the pile
        T["slip"] = T["lift2"] + 0.32                             # the claw slides off his head
        T["bonk"] = T["bigger"] + 0.5                             # the ghost teddy meets the prize door
        x13, x14, x11 = PILE[13][0], PILE[14][0], PILE[11][0]
        y13, y14, y11 = PILE[13][1], PILE[14][1], PILE[11][1]
        # ---- cameras: one world, four of them. Floor line near screen y 1230 means camera y = -270 / zoom
        self.cut(s("fix1") - 0.12, "claw", 1)
        self.cut(s("break2") - 0.1, "front", -1)
        self.cut(s("fix2") - 0.12, "base", 1)
        self.cut(T["tight"] - 0.45, "claw", -1)
        self.cut(s("break3") - 0.1, "front", 1)
        self.cut(s("fix3") - 0.12, "base", 1)
        self.cut(T["lets"] - 0.3, "front", -1)
        self.cut(T["kid0"], "door", 1)
        self.cut(s("cta") + 0.05, "front", -1)
        self.cams = {"front": Camera(40, -200, 1.35), "claw": Camera(0, -425, 1.8), "base": Camera(0, -85, 2.0),
                     "door": Camera(-130, -150, 1.8)}
        cm = self.cams
        cm["front"].key(0.05, 30, -215, 1.42, 1.3).key(T["congrats"] - 0.25, -10, -240, 1.12, 0.75)
        cm["front"].key(s("break1"), -50, -225, 1.2, 1.2)
        cm["front"].key(s("break2") - 0.1, -30, -225, 1.2, 0.0).key(T["plays"] - 1.0, 0, -236, 1.14, 1.5)
        cm["front"].key(s("break3") - 0.1, -60, -225, 1.2, 0.0)
        cm["front"].key(T["lets"] - 0.3, -30, -225, 1.2, 0.0).key(T["alarm"] - 0.2, -20, -262, 1.03, 0.6)
        cm["front"].key(s("cta") + 0.05, 60, -200, 1.35, 0.0).key(s("reveal") - 0.1, -20, -235, 1.15, 0.8)
        cm["front"].key(T["s1"] - 0.3, 0, -400, 0.7, 0.9).key(s("closer"), 0, -385, 0.74, 2.0)
        cm["front"].key(s("tag") - 0.2, -40, -232, 1.16, 0.32)
        cm["claw"].key(s("fix1") - 0.12, 0, -425, 1.8, 0.0).key(T["magnet"] - 0.3, 20, -455, 2.0, 0.8).key(T["lift"] - 0.4, 0, -425, 1.8, 0.8)
        cm["claw"].key(T["tight"] - 0.45, 0, -425, 1.8, 0.0)
        cm["base"].key(s("fix2") - 0.12, 20, -85, 2.0, 0.0).key(T["coins"] - 0.3, 40, -90, 2.1, 0.8)
        cm["base"].key(s("fix3") - 0.12, 0, -75, 1.9, 0.0).key(T["sensor"] - 0.3, -30, -95, 2.2, 0.6)
        cm["door"].key(T["kid0"], -225, -117, 2.3, 0.0).key(T["stuck"] - 0.6, -110, -165, 1.7, 0.5)
        cm["door"].key(s("fix4") + 0.3, -150, -150, 1.9, 0.7)
        # ---- the claw: x on the gantry, cable length (hub y = RAIL + 50 + length), opening
        self.kx, self.kl, self.ko = Track(0.0), Track(20.0), Track(1.0)
        self.grip = Track(1.0)
        self.held, self.fl, self.taken = [], [], []              # (t0, t1, kind); flights; (t0, t1, pile index)
        per = clamp((e("break1") - T["never"]) / 3.05, 0.8, 1.15)
        self.wins = [(T["never"] + i * per, T["never"] + i * per + 0.62) for i in range(3)]
        for i, (g, r) in enumerate(self.wins):                   # break 1: it never lets go
            kind = (0, 1, 3)[i]
            self.kx.to(g - 0.5, (60, 130, 0)[i], 0.24, e_io)
            self.ko.to(g - 0.5, 1.0, 0.08)
            self.kl.to(g - 0.27, (191, 235, 279)[i], 0.24, e_io)
            self.ko.to(g - 0.03, 0.22, 0.08)
            self.kl.to(g + 0.08, 20, 0.24, e_io)
            self.kx.to(g + 0.3, HOME, 0.27, e_io)
            self.ko.to(r, 1.0, 0.07)
            self.held.append((g, r, kind))
            self.fl.append((r, r + 0.2, kind, 27, HOME, -596, HOME, -330, 0, "glass"))
            self.fl.append((r + 0.3, r + 0.55, kind, 25, DOORC[0], DOORC[1], KX[i], -KH[i] - 30, 150, "out"))
        t1 = s("fix1")                                           # fix 1: strong to lift, weak to carry
        for tr, v in ((self.kx, x13), (self.kl, 20.0), (self.ko, 1.0), (self.grip, 0.0)):
            tr.to(t1 - 0.13, v, 0.01)
        self.kl.to(t1 + 0.15, 191, max(0.4, T["magnet"] - t1 - 0.3), e_io)
        self.grip.to(T["magnet"], 1.0, 0.25)
        self.ko.to(T["magnet"] + 0.05, 0.22, 0.15)
        self.kl.to(T["lift"] - 0.4, 70, 0.8, e_io)
        self.grip.to(T["weak"], 0.2, 0.3)
        self.ko.to(T["weak"], 0.55, max(0.2, T["drop"] - T["weak"]))
        self.kl.to(T["drop"] + 0.45, 20, 0.4)
        self.ko.to(T["drop"] + 0.3, 1.0, 0.2)
        self.held.append((T["magnet"] + 0.2, T["drop"] - 0.05, 0))
        self.fl.append((T["drop"] - 0.05, T["drop"] + 0.22, 0, 27, x13, -546, x13, y13, 0, "glass"))
        self.taken.append((T["magnet"] + 0.2, T["drop"] + 0.22, 13))
        tn = T["nobody"]                                         # break 2: nobody ever wins
        self.kx.to(s("break2") - 0.1, x13, 0.01)
        self.kl.to(tn - 0.32, 191, 0.28, e_io)
        self.ko.to(tn - 0.04, 0.22, 0.08)
        self.kl.to(tn + 0.1, 80, 0.3, e_io)
        self.ko.to(tn + 0.42, 0.6, 0.1)
        self.kl.to(tn + 0.9, 20, 0.3)
        self.ko.to(tn + 0.9, 1.0, 0.2)
        self.kx.to(tn + 1.0, HOME, 0.6)
        self.held.append((tn, tn + 0.5, 0))
        self.fl.append((tn + 0.5, tn + 0.75, 0, 27, x13, -536, x13, y13, 0, "glass"))
        self.taken.append((tn, tn + 0.75, 13))
        tt = T["tight"]                                          # fix 2: paid up, so it holds tight
        self.grip.to(T["profit"] + 0.05, 1.0, 0.3)
        for tr, v in ((self.kx, x14), (self.kl, 191.0), (self.ko, 1.0)):
            tr.to(tt - 0.5, v, 0.01)
        self.ko.to(tt - 0.3, 0.22, 0.15)
        self.kl.to(tt + 0.05, 20, 0.45, e_io)
        self.kx.to(tt + 0.5, HOME, 0.42, e_io)
        self.ko.to(tt + 0.95, 1.0, 0.08)
        self.held.append((tt - 0.3, tt + 0.95, 1))
        self.fl.append((tt + 0.95, tt + 1.17, 1, 27, HOME, -596, HOME, -330, 0, "glass"))
        self.taken.append((tt - 0.5, s("break3") - 0.1, 14))
        T["win"] = tt + 1.17
        self.grip.to(s("break3") - 0.1, 0.2, 0.01)
        self.taken.append((T["tumbles"] - 0.1, s("cta"), 11))    # break 3: shaken into the chute
        self.fl.append((T["tumbles"] - 0.1, T["chute"] + 0.05, 3, 27, x11, y11, HOME, -330, 110, "glass"))
        self.fl.append((T["chute"] + 0.2, T["chute"] + 0.48, 3, 25, DOORC[0], DOORC[1], -268, -186, 90, "out"))
        t3 = s("fix3") - 0.12                                    # fix 3: one shove and it lets go
        for tr, v in ((self.kx, x14), (self.kl, 80.0), (self.ko, 0.22)):
            tr.to(t3, v, 0.01)
        self.ko.to(T["lets"], 1.0, 0.1)
        self.kx.to(T["alarm"] + 0.5, HOME, 0.5)
        self.kl.to(T["alarm"] + 0.5, 20, 0.4)
        self.held.append((t3, T["lets"] + 0.05, 1))
        self.fl.append((T["lets"] + 0.05, T["lets"] + 0.3, 1, 27, x14, -536, x14, y14, 0, "glass"))
        self.taken.append((t3, T["lets"] + 0.3, 14))
        t4 = s("fix4")                                           # fix 4: the door opens for prizes only
        for tr, v in ((self.kx, HOME), (self.kl, 20.0), (self.ko, 0.22)):
            tr.to(t4 + 0.5, v, 0.01)
        self.ko.to(T["drops"] - 0.22, 1.0, 0.06)
        self.held.append((t4 + 0.5, T["drops"] - 0.22, 2))
        self.fl.append((T["drops"] - 0.22, T["drops"] + 0.06, 2, 27, HOME, -596, HOME, -330, 0, "glass"))
        tl2 = T["lift2"]                                         # the reveal: nobody can lift the giant teddy
        self.kl.to(T["giant"] - 0.2, 0, 0.2)
        self.kx.to(T["land"] + 0.15, TED[0], 0.4, e_io)
        self.kl.to(tl2 - 0.55, 14, 0.15)
        self.ko.to(tl2 - 0.32, 0.75, 0.12)
        self.grip.to(tl2 - 0.32, 1.0, 0.15)
        self.kl.to(tl2 - 0.12, 0, 0.42, e_out)
        self.ko.to(T["slip"], 1.0, 0.06)
        self.grip.to(T["slip"], 0.2, 0.1)
        self.stretch = Track(0.0).to(tl2 - 0.12, 18.0, 0.42, e_out).to(T["slip"], 0.0, 0.16, e_back)
        # ---- everything else that moves
        self.level = Track(1.0).to(T["never"] + 0.3, 0.0, max(0.5, T["empty"] - T["never"] - 0.3), e_io).to(s("fix1") - 0.13, 1.0, 0.01)
        self.cutk = (Track(0.0).to(s("fix2") - 0.12, 1.0, 0.01).to(T["tight"] - 0.45, 0.0, 0.01)
                     .to(s("fix3") - 0.12, 1.0, 0.01).to(T["lets"] - 0.3, 0.0, 0.01))
        self.lights = (Track(0.5).to(T["plays"] - 0.6, 0.18, 0.5).to(s("fix2") - 0.12, 0.5, 0.01)
                       .to(T["flashing"] - 0.05, 1.0, 0.25))
        self.doork = Track(0.0)
        for g, r in self.wins:
            self.doork.to(r + 0.24, 0.8, 0.08).to(r + 0.45, 0.0, 0.15)
        self.doork.to(T["chute"] + 0.14, 0.8, 0.08).to(T["chute"] + 0.4, 0.0, 0.15)
        self.doork.to(T["crawl0"], 1.0, 0.2).to(T["crawl0"] + 0.85, 0.0, 0.25)
        self.doork.to(t4 + 0.1, 1.0, 0.12).to(t4 + 0.55, 0.0, 0.2)
        self.doork.to(T["drops"] + 0.1, 1.0, 0.2).to(s("cta"), 0.0, 0.01)
        self.lockk = Track(0.0).to(T["lock"], 1.0, 0.15).to(T["drops"] + 0.02, 0.0, 0.1).to(s("cta"), 1.0, 0.01)
        self.coin_t = [lerp(T["coins"] - 0.3, T["profit"] - 0.15, i / 6) for i in range(7)]
        self.bolt_t = (T["bolt"], T["bolt"] + 0.26)
        self.spans = [(T["empty"] - 0.15, T["drop"] + 0.3), (T["plays"] - 0.5, T["win"] + 0.1), (T["tumbles"], T["alarm"] + 0.9),
                      (T["stuck"], T["drops"] + 0.45)]
        self.shakes = [(T["built"] - 0.05, 0.3, 9), (T["shove"], 0.35, 12), (self.bolt_t[0] + 0.14, 0.2, 9), (self.bolt_t[1] + 0.14, 0.2, 9),
                       (T["stuck"], 0.3, 8), (T["land"], 0.45, 20), (T["slip"], 0.3, 9), (T["bonk"], 0.3, 10)]
        self.shakes += [(T["shakes"] + i * 0.37, 0.3, 6) for i in range(int(max(1, (T["chute"] - T["shakes"]) / 0.37)))]
        self.wp = {}                                             # world points the labels hang on

    def rock(self, t):
        """Tilt of the whole machine while somebody shakes it (degrees)."""
        T = self.T
        if not T["shakes"] <= t < T["chute"] + 0.3:
            return 0.0
        env = prog(t, T["shakes"], T["shakes"] + 0.2) * (1 - prog(t, T["chute"], T["chute"] + 0.3))
        return math.sin((t - T["shakes"]) * 17) * 3.4 * env

    def pend(self, t):
        """(angle of the shake sensor's pendulum in radians, 0..1 how hard it is ringing)."""
        ts = self.T["shove"]
        a = 0.05 * math.sin(t * 2.2)
        if t >= ts:
            a += 0.8 * math.sin((t - ts) * 15) * math.exp(-(t - ts) * 2.4)
        hit = (1 - prog(t, ts + 0.1, ts + 1.3)) if t >= ts + 0.1 else 0.0
        return clamp(a, -0.4, 0.4), hit

    # ------------------------------------------------------------------ the room
    def arcade(self, c, t):
        lights = self.lights.at(t)
        vrect(c, -3400, -3400, 6800, 3400, ["#07061A", "#140F3A", "#231552", "#2E1A66"], [0.0, 0.5, 0.82, 1.0])
        for px in range(-3380, 3400, 260):
            c.drawRect(R(px, -3400, 3, 3400), P("#000000", 0.16))
        add_glow(c, -640, -520, 760, "#22D3EE", 0.10 + 0.07 * lights)
        add_glow(c, 660, -560, 760, "#F472B6", 0.10 + 0.07 * lights)
        add_glow(c, 0, -640, 950, "#8B5CF6", 0.20)
        vrect(c, -3400, -150, 6800, 110, [("#F472B6", 0.0), ("#F472B6", 0.20)])
        c.drawRect(R(-3400, -44, 6800, 6), P("#F9A8D4"))
        v2.ground(c, -3400, 3400, surface="#3F2F86", pal=("#251B5E", "#17123F", "#0C0926", "#05040E"))
        for i, (x, hue) in enumerate(((-770, "#22D3EE"), (-585, "#FDE047"), (585, "#FB7185"), (770, "#4ADE80"))):
            cabinet(c, x, hue, t, i)
        on = t >= self.T["flashing"] - 0.05
        fl = 1.0
        if on and t < self.T["flashing"] + 0.5:
            fl = 0.3 + 0.7 * (math.sin(t * 61) > -0.2)
        k = (0.20 if not on else 1.0) * fl
        neon(c, star_path(-520, -660, 78, 34), "#67E8F9", k)
        ring = skia.Path()
        ring.addCircle(520, -660, 70)
        neon(c, ring, "#F472B6", k)
        tri = skia.Path()
        tri.moveTo(498, -696)
        tri.lineTo(556, -660)
        tri.lineTo(498, -624)
        tri.close()
        neon(c, tri, "#FDE047", k, 6)
        zig = skia.Path()
        zig.moveTo(-610, -520)
        for i in range(1, 7):
            zig.lineTo(-610 + i * 30, -520 + (22 if i % 2 else 0))
        neon(c, zig, "#FDE047", k, 6)
        if on:
            add_glow(c, -520, -660, 260, "#67E8F9", 0.30 * fl)
            add_glow(c, 520, -660, 260, "#F472B6", 0.30 * fl)

    # ------------------------------------------------------------------ the machine
    def machine(self, c, t):
        T, s = self.T, self.tl.s
        cut, lights = self.cutk.at(t), self.lights.at(t)
        contact_shadow(c, 0, 6, 640, 0.5, 44)
        # the glass box
        vrect(c, -MW + 10, GTOP, 2 * MW - 20, PANEL - GTOP, ["#4A3CC0", "#31288C", "#1E1A5C"], [0.0, 0.5, 1.0])
        add_glow(c, 0, GTOP + 20, 460, "#C4B5FD", 0.40)
        rng = random.Random(21)
        for _ in range(28):
            sx_, sy_ = rng.uniform(-205, 205), rng.uniform(GTOP + 50, PANEL - 160)
            c.drawCircle(sx_, sy_, rng.uniform(1.5, 3.5), P("#FFFFFF", 0.22 + 0.18 * math.sin(t * 2 + sx_)))
        c.save()
        c.clipRect(R(-MW + 10, GTOP, 2 * MW - 20, PANEL - GTOP))
        self.inside(c, t)
        c.restore()
        for sx_ in (-150, 60):                                                       # reflections on the glass
            g = skia.Path()
            g.moveTo(sx_, GTOP)
            g.lineTo(sx_ + 70, GTOP)
            g.lineTo(sx_ - 90, PANEL)
            g.lineTo(sx_ - 160, PANEL)
            g.close()
            c.drawPath(g, P("#FFFFFF", 0.05))
        for sd in (-1, 1):                                                           # corner posts
            x0 = -MW if sd < 0 else MW - 16
            vrect(c, x0, GTOP - 4, 16, PANEL - GTOP + 8, [shade(BODY, 0.1), shade(BODY, -0.25)])
            c.drawRect(R(x0 + (2 if sd < 0 else 11), GTOP, 3, PANEL - GTOP), P("#FFFFFF", 0.22))
        if cut > 0 or T["profit"] - 0.3 <= t < T["win"]:                             # the wire from the computer up to the claw
            c.drawLine(206, PANEL + 30, 206, RAIL - 12, P("#34D399", 0.55, stroke=3))
        # the marquee
        box(c, -MW - 12, TOP, 2 * MW + 24, GTOP - TOP + 8, shade(BODY, -0.22), r=16)
        vrect(c, -MW + 6, TOP + 16, 2 * MW - 12, GTOP - TOP - 26, ["#3B1A7A", "#22104F"], r=10)
        for i, (sx_, r_) in enumerate(((-118, 22), (0, 31), (118, 22))):
            c.drawPath(star_path(sx_, (TOP + GTOP) / 2 + 2, r_, r_ * 0.45), P(mix("#7A6420", TRIM, clamp(lights + 0.3))))
            add_glow(c, sx_, (TOP + GTOP) / 2, r_ * 3, TRIM, 0.45 * lights)
        fast = t >= T["flashing"] - 0.05
        cols = ("#FDE047", "#FB7185", "#67E8F9")
        for row, y in enumerate((TOP + 9, GTOP - 2)):
            for i in range(10):
                x = -207 + i * 46
                on = (i + row + int(t * (11 if fast else 3))) % 3 == 0
                col = cols[(i + row) % 3] if fast else "#FDE047"
                c.drawCircle(x, y, 7, P(mix("#4A3A1A", col, clamp(lights * (1.0 if on else 0.3) + 0.12))))
                if on:
                    add_glow(c, x, y, 32, col, 0.85 * lights)
        if t >= T["alarm"] - 0.15:                                                   # the alarm beacon on the roof
            bk = e_back(prog(t, T["alarm"] - 0.15, T["alarm"] + 0.1))
            ringing = t < T["alarm"] + 2.4 and t < s("break4") + 0.1
            box(c, -26, TOP - 8 * bk, 52, 10, "#2B3248", r=3)
            dome = skia.Path()
            dome.addArc(R(-22, TOP - 8 - 26 * bk, 44, 44 * bk), 180, 180)
            dome.close()
            c.drawPath(dome, P(mix("#7F1D1D", "#FF4D4F", 1.0 if ringing else 0.25)))
            if ringing:
                pulse = 0.55 + 0.45 * math.sin(t * 16)
                add_glow(c, 0, TOP - 22, 220, "#FF4D4F", 0.7 * pulse)
                for a0 in (0, 180):
                    light_cone(c, 0, TOP - 22, (t * 300 + a0) % 360, 620, 16, "#FF6B6B", 0.30)
        # the control panel
        box(c, -MW - 10, PANEL, 2 * MW + 20, 34, shade(BODY, 0.12), r=9)
        c.drawRect(R(-MW - 6, PANEL + 2, 2 * MW + 12, 4), P("#FFFFFF", 0.28))
        lean = clamp((self.kx.at(t + 0.06) - self.kx.at(t)) * 1.6, -13, 13)
        c.drawLine(-36, PANEL + 6, -36 + lean, PANEL - 30, P("#8E97AD", 1, stroke=6))
        c.drawCircle(-36 + lean, PANEL - 34, 13, rad_paint(-40 + lean, PANEL - 39, 20, ["#FCA5A5", "#EF4444", "#991B1B"]))
        c.drawCircle(40, PANEL + 8, 15, P("#7A6420"))
        c.drawCircle(40, PANEL + 6, 12, P(mix(TRIM, "#FFFFFF", 0.3 + 0.3 * math.sin(t * 5))))
        add_glow(c, 40, PANEL + 6, 34, TRIM, 0.35 + 0.25 * math.sin(t * 5))
        c.drawRRect(rr(126, PANEL + 5, 48, 24, 5), lin_paint(126, 0, 174, 0, ["#E5E9F2", "#9AA3B8"]))
        c.drawRRect(rr(147, PANEL + 9, 6, 16, 2), P("#11151F"))
        # the base cabinet
        bx, by, bw, bh = -MW, PANEL + 30, 2 * MW, -(PANEL + 30) - 14
        if cut > 0:
            self.guts(c, t, bx, by, bw, bh)
        if cut < 1:
            a = 1 - cut
            box(c, bx, by, bw, bh, BODY, r=10, a=a)
            c.drawRect(R(bx, by + 4, 9, bh - 8), P("#FFFFFF", 0.12 * a))
            c.drawRect(R(bx + bw - 14, by + 4, 14, bh - 8), P("#000000", 0.22 * a))
            vrect(c, bx, -70, bw, 56, [("#000000", 0.0), ("#000000", 0.34 * a)])
            c.drawRect(R(bx + 14, by + 12, bw - 28, 5), P(TRIM, 0.9 * a))
            c.drawCircle(52, -140, 44, P("#1B1230", a))                              # the speaker
            for r_ in (12, 23, 34):
                c.drawCircle(52, -140, r_, P("#4C3A8A", a, stroke=3))
            c.drawPath(star_path(158, -140, 34, 15), P(TRIM, a))
            arrow = skia.Path()                                                      # "prizes come out here"
            arrow.moveTo(DOORC[0] - 18, DOOR[1] - 50)
            arrow.lineTo(DOORC[0] + 18, DOOR[1] - 50)
            arrow.lineTo(DOORC[0], DOOR[1] - 26)
            arrow.close()
            c.drawPath(arrow, P(TRIM, a))
        self.door(c, t, 1 - 0.85 * cut)
        for sd in (-1, 1):                                                           # feet, floor plates and bolts
            box(c, sd * 200 - 26, -14, 52, 14, "#2B3248", r=3)
            tb = self.bolt_t[0 if sd < 0 else 1]
            if t >= tb - 0.25:
                pk = prog(t, tb - 0.25, tb - 0.1)
                x0 = 226 if sd > 0 else -274
                c.drawRRect(rr(x0, -8, 48, 8, 2), P("#8E97AD", pk))
                k = e_in(prog(t, tb, tb + 0.14))
                hy = lerp(-90, -17, k)
                bxx = sd * 252
                c.drawRect(R(bxx - 4, hy + 8, 8, 46), lin_paint(bxx - 4, 0, bxx + 4, 0, ["#E5E9F2", "#7C8499"]))
                for i in range(5):
                    c.drawLine(bxx - 4, hy + 16 + i * 8, bxx + 4, hy + 19 + i * 8, P("#5B657E", 1, stroke=1.5))
                c.drawRRect(rr(bxx - 12, hy, 24, 10, 2), P("#F1F5F9"))
                sparks_shower(c, bxx, -10, t, tb + 0.14, 0.5, n=14, speed=420, seed=3 + sd)

    def inside(self, c, t):
        """Everything behind the glass (the caller clips to the box)."""
        T, s = self.T, self.tl.s
        vrect(c, CH0, CHTOP, CH1 - CH0, PANEL - CHTOP, [("#0E0B30", 0.55), ("#070518", 0.9)])
        for i in range(3):                                                           # chevrons: this way down
            yy = CHTOP + 28 + i * 30 + (t * 30) % 30
            if yy < PANEL - 14:
                ch = skia.Path()
                ch.moveTo(HOME - 24, yy)
                ch.lineTo(HOME, yy + 14)
                ch.lineTo(HOME + 24, yy)
                c.drawPath(ch, P(TRIM, 0.45, stroke=5))
        self.pile(c, t, (0, 1))
        if T["stuck"] - 0.3 <= t < s("fix4") + 0.15:                                 # the kid who crawled in
            k = e_back(prog(t, T["stuck"] - 0.3, T["stuck"])) * (1 - prog(t, s("fix4"), s("fix4") + 0.15))
            person(c, -22, lerp(-330, -440, k), 92, "#F472B6", t, "cheer" if t >= T["stuck"] + 0.1 else "stand", face=-1, hair="#3A2414")
        self.pile(c, t, (2,))
        if t >= T["giant"]:
            u = prog(t, T["giant"], T["land"])
            ty = lerp(TED[1] - 620, TED[1], e_in(u))
            sleepy = t >= T["lives"] + 0.15
            teddy(c, TED[0], ty, TED[2], bump(t, T["land"], T["land"] + 0.35) - 0.5 * bump(t, T["slip"], T["slip"] + 0.3),
                  self.stretch.at(t), sleepy)
            if t >= T["lives"]:                                                      # he lives here now
                hk = e_back(prog(t, T["lives"], T["lives"] + 0.3))
                c.drawLine(176, RAIL + 6, 176, RAIL + 6 + 70 * hk, P("#11151F", 1, stroke=3))
                lamp = skia.Path()
                lamp.moveTo(176 - 26 * hk, RAIL + 100 * hk + 6)
                lamp.lineTo(176 - 12 * hk, RAIL + 70 * hk + 6)
                lamp.lineTo(176 + 12 * hk, RAIL + 70 * hk + 6)
                lamp.lineTo(176 + 26 * hk, RAIL + 100 * hk + 6)
                lamp.close()
                c.drawPath(lamp, P("#F59E0B"))
                add_glow(c, 176, RAIL + 110, 170, "#FFE9B8", 0.6 * hk)
                c.save()
                c.translate(-60, -716)
                c.scale(hk, hk)
                c.drawRRect(rr(-32, -26, 64, 52, 5), P("#7C4A2D"))
                c.drawRRect(rr(-26, -20, 52, 40, 3), P("#BFE4FF"))
                toy(c, 0, 0, 4, 13)
                c.restore()
                if sleepy:
                    for j in range(3):
                        u2 = ((t - T["lives"]) * 0.6 + j / 3) % 1.0
                        text(c, "z", TED[0] + 80 + u2 * 50, -610 - u2 * 90, 30 + 22 * u2, "#FFFFFF", "Poppins-Black", a=(1 - u2) * 0.9)
        for t0, t1, kind, r, x0, y0, x1, y1, arc, where in self.fl:
            if where == "glass" and t0 <= t < t1:
                u = prog(t, t0, t1)
                toy(c, kind, lerp(x0, x1, u), lerp(y0, y1, e_in(u) if arc == 0 else u) - arc * math.sin(math.pi * u), r, u * 220 * (1 if arc else 0))
        # the chute wall (clear plastic) and the light beam across it
        c.drawRect(R(CH1 - 5, CHTOP, 5, PANEL - CHTOP), P("#BFD8FF", 0.38))
        c.drawRRect(rr(CH1 - 9, CHTOP - 7, 13, 9, 3), P(TRIM))
        if t >= T["beam"] - 0.1:
            broken = T["drops"] - 0.03 <= t < T["drops"] + 0.9
            col = GOOD if broken else "#FF4D4F"
            bk = prog(t, T["beam"] - 0.1, T["beam"] + 0.1)
            for bxx in (CH0 + 2, CH1 - 19):
                c.drawRRect(rr(bxx, -359, 14, 18, 3), P("#11151F"))
            c.drawLine(CH0 + 16, -350, lerp(CH0 + 16, CH1 - 19, bk), -350, P(col, 0.9, stroke=4))
            c.drawLine(CH0 + 16, -350, lerp(CH0 + 16, CH1 - 19, bk), -350, P("#FFFFFF", 0.7, stroke=1.5))
            add_glow(c, CH0 + 12, -350, 26, col, 0.9)
            add_glow(c, CH1 - 12, -350, 26 + 30 * broken, col, 0.9 * bk)
        # the gantry and the claw
        vrect(c, -MW + 10, RAIL - 8, 2 * MW - 20, 14, ["#E5E9F2", "#7C8499"])
        if t >= T["built"]:
            x, hy, op = self.kx.at(t), RAIL + 50 + self.kl.at(t), self.ko.at(t)
            strain = math.sin(t * 70) * 2.5 if T["lift2"] - 0.12 <= t < T["slip"] else 0.0
            box(c, x - 34, RAIL - 16, 68, 34, "#3A4258", r=7)
            for wx in (-20, 20):
                c.drawCircle(x + wx, RAIL - 12, 6, P("#11151F"))
            c.drawLine(x, RAIL + 18, x + strain, hy - 24, P("#DDE3EE", 1, stroke=3))
            for t0, t1, kind in self.held:
                if t0 <= t < t1:
                    toy(c, kind, x, hy + 96, 27, math.sin(t * 6) * 5)
            claw(c, x + strain, hy, op, self.grip.at(t) * (0.0 if t < self.tl.s("fix1") - 0.13 else 1.0))

    def pile(self, c, t, rows):
        n = int(round(self.level.at(t) * len(PILE)))
        jig = abs(self.rock(t)) * 2.2
        for i, (x, y, r, kind, rot) in enumerate(PILE):
            row = 0 if i < 6 else 1 if i < 11 else 2
            if i >= n or row not in rows or any(t0 <= t < t1 and idx == i for t0, t1, idx in self.taken):
                continue
            toy(c, kind, x + math.sin(t * 31 + i) * jig, y - abs(math.sin(t * 27 + i * 2)) * jig, r, rot)

    def guts(self, c, t, bx, by, bw, bh):
        """Inside the base (the cutaway): chute, coin box, computer board, power dial, shake sensor."""
        T = self.T
        c.save()
        c.clipRect(R(bx, by, bw, bh))
        vrect(c, bx, by, bw, bh, ["#1F173F", "#130E28"])
        vrect(c, CH0, by, CH1 - CH0, bh - 56, ["#0A0818", "#171133"])                # the chute
        c.drawRect(R(CH1, by, 5, bh - 56), P("#4A3F7A"))
        c.drawRect(R(CH0, -70, CH1 - CH0 + 5, 6), P("#4A3F7A"))
        c.drawRect(R(141, by, 4, 152), P("#5B657E"))                                 # the coin path and the coin box
        c.drawRect(R(155, by, 4, 152), P("#5B657E"))
        box(c, 104, -128, 102, 106, "#5B657E", r=7)
        c.drawRRect(rr(111, -121, 88, 92, 5), P("#12162A"))
        n = sum(1 for tc in self.coin_t if t >= tc + 0.26)
        for i in range(n):
            coin(c, 124 + (i % 4) * 21, -36 - (i // 4) * 15, 9, spin=1.25)
        for i, tc in enumerate(self.coin_t):
            if tc <= t < tc + 0.26:
                u = prog(t, tc, tc + 0.26)
                coin(c, 150, lerp(by - 20, -44, e_in(u)), 9, spin=t * 22)
        px, py, pw, ph = -84, -262, 168, 112                                         # the computer board
        paid = clamp((t - T["profit"]) * 4) if t >= T["profit"] else 0.0
        box(c, px, py, pw, ph, "#0F766E", r=8)
        c.drawRRect(rr(px, py, pw, ph, 8), P("#5EEAD4", 0.6, stroke=2))
        for i in range(5):
            yy = py + 62 + i * 9
            c.drawLine(px + 8, yy, px + 40 + i * 14, yy, P("#34D399", 0.35, stroke=2))
            c.drawLine(px + 40 + i * 14, yy, px + 52 + i * 14, yy + 10, P("#34D399", 0.35, stroke=2))
        c.drawRRect(rr(px + 96, py + 62, 46, 36, 4), P("#11151F"))
        c.drawRRect(rr(px + 60, py + 70, 26, 22, 3), P("#11151F"))
        for i in range(4):
            c.drawRect(R(px + 100 + i * 10, py + 58, 4, 4), P("#C9D1E4"))
            c.drawRect(R(px + 100 + i * 10, py + 98, 4, 4), P("#C9D1E4"))
        c.drawRRect(rr(px + 10, py + 10, 74, 42, 5), P("#04120F"))
        cnt = sum(1 for tc in self.coin_t if t >= tc + 0.22)
        text(c, "%02d" % cnt, px + 47, py + 43, 36, mix("#FB7185", "#4ADE80", paid), "Poppins-Black")
        for i in range(7):
            lit = i < cnt
            col = ("#FACC15" if i < 5 else "#4ADE80") if lit else "#14403A"
            c.drawRRect(rr(px + 94 + i * 9.5, py + 12, 7, 36, 2), P(col))
            if lit:
                add_glow(c, px + 97.5 + i * 9.5, py + 30, 14, col, 0.5)
        self.wp["cost"] = (px + 94 + 5 * 9.5 - 1.5, py + 8)
        self.wp["profit"] = (px + 94 + 7 * 9.5 - 1.5, py + 8)
        for key in ("cost", "profit"):
            wx, wy = self.wp[key]
            c.drawRect(R(wx - 1.5, wy, 3, 46), P("#FFFFFF", 0.85))
        if paid > 0:
            add_glow(c, px + pw / 2, py + ph / 2, 170, "#4ADE80", 0.45 * paid * (0.7 + 0.3 * math.sin(t * 9)))
        c.drawLine(px + pw - 14, py, px + pw - 14, by + 6, P("#34D399", 0.8, stroke=3))        # wire: board -> claw
        c.drawLine(px + pw - 14, by + 6, 206, by + 6, P("#34D399", 0.8, stroke=3))
        if T["profit"] <= t < T["profit"] + 0.9:
            u = ((t - T["profit"]) * 2.4) % 1.0
            c.drawCircle(lerp(px + pw - 14, 206, u), by + 6, 6, P("#FFFFFF"))
            add_glow(c, lerp(px + pw - 14, 206, u), by + 6, 26, "#4ADE80", 0.9)
        g = self.grip.at(t)                                                          # the power dial
        c.drawCircle(22, -92, 26, rad_paint(14, -100, 40, ["#5B657E", "#2B3248", "#161A2B"]))
        c.drawCircle(22, -92, 26, P("#C9D1E4", 0.8, stroke=3))
        da = math.radians(lerp(-220, 40, g))
        c.drawLine(22, -92, 22 + math.cos(da) * 19, -92 + math.sin(da) * 19, P(TRIM, 1, stroke=5))
        ang, hit = self.pend(t)                                                      # the shake sensor
        sx_, sy_ = -58, -132
        box(c, sx_ - 16, sy_ - 12, 32, 12, "#5B657E", r=3)
        ring = mix("#C9D1E4", "#FF4D4F", hit)
        c.drawCircle(sx_, sy_ + 52, 21, P(ring, 1, stroke=5))
        if hit > 0:
            add_glow(c, sx_, sy_ + 52, 60, "#FF4D4F", 0.8 * hit)
        ex, ey = sx_ + math.sin(ang) * 52, sy_ + math.cos(ang) * 52
        c.drawLine(sx_, sy_, ex, ey, P("#E5E9F2", 1, stroke=3))
        c.drawCircle(ex, ey, 8, rad_paint(ex - 3, ey - 3, 12, ["#FFF3B0", "#FACC15", "#B7791F"]))
        self.wp["sensor"] = (sx_, sy_ + 52)
        c.restore()
        c.drawRRect(rr(bx, by, bw, bh, 10), dash_paint("#FFFFFF", 0.45, 3, t))

    def door(self, c, t, a=1.0):
        T = self.T
        x, y, w, h = DOOR
        k, lk = self.doork.at(t), self.lockk.at(t)
        rattle = math.sin(t * 60) * 3 * bump(t, T["opens"], T["opens"] + 0.45)
        c.drawRRect(rr(x - 8, y - 8, w + 16, h + 16, 10), P(TRIM, a))
        c.drawRRect(rr(x, y, w, h, 6), P("#080614", a))
        if T["drops"] + 0.28 <= t < self.tl.s("cta"):                                # the prize waits in the doorway
            pk = e_back(prog(t, T["drops"] + 0.28, T["drops"] + 0.5))
            toy(c, 2, x + w / 2, y + h - 34 * pk, 30 * pk)
        if k < 1:
            fh = h * (1 - 0.82 * e_io(k))
            vrect(c, x + 3 + rattle, y + 3, w - 6, fh - 6, [("#7C6AE0", a), ("#3B2A8C", a)], r=5)
            c.drawRRect(rr(x + 14 + rattle, y + 12, w - 28, max(4.0, fh * 0.34), 5), P("#BFD8FF", 0.30 * a))
            c.drawRect(R(x + 12 + rattle, y + fh - 16, w - 24, 5), P(TRIM, 0.9 * a))
        if t >= T["lock"]:
            locked = lk > 0.5
            c.drawRRect(rr(lerp(x + w + 10, x + w - 20, e_out(lk)), y + h * 0.5 - 6, 32, 12, 4), P("#E5E9F2", a))
            col = "#FF4D4F" if locked else GOOD
            px_, py_ = x + w - 6, y - 30
            c.drawArc(R(px_ - 9, py_ - 20 - (0 if locked else 8), 18, 24), 180, 180, False, P("#E5E9F2", a, stroke=5))
            c.drawRRect(rr(px_ - 14, py_ - 8, 28, 22, 5), P(col, a))
            add_glow(c, px_, py_ + 3, 44, col, 0.6 * a)

    # ------------------------------------------------------------------ people
    def people(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        m = self.mode(t)
        if m == "front":
            # ---- the crew, on the right
            if t < s("break1"):
                pose = "stand" if t < T["congrats"] else "cheer"
            elif t < s("fix1"):
                pose = "cheer" if t < T["empty"] - 0.2 else "look"
            elif t < s("fix2"):
                pose = "look" if t < T["plays"] - 0.5 else "shrug"
            elif t < s("fix3"):
                pose = "look" if t < T["tumbles"] else "duck"
            elif t < s("break4"):
                pose = "point" if t < T["alarm"] + 0.9 else "cheer"
            elif t < s("cta"):
                pose = "stand"
            elif t < T["giant"]:
                pose = "stand" if t < T["flashing"] else "cheer"
            elif t < T["s1"] - 0.3:
                pose = "look" if t < T["slip"] else "shrug"
            elif t < s("tag") - 0.2:
                pose = "cheer"
            else:
                pose = "look" if t < T["lives"] + 0.2 else "shrug"
            xs = (262, 300, 338)
            self.crew(c, t, pose, xs=xs, face=-1)
            if s("closer") <= t < s("tag") - 0.2:
                hats_in_the_air(c, xs, -150, t, T["cong2"])
            # ---- the three kids, on the left
            for i, ((col, hat), h) in enumerate(zip(KCOL, KH)):
                x, pose, face, hold = KX[i], "look", 1, None
                if t < T["congrats"] + 0.2:
                    continue
                if t < s("break2") - 0.1:
                    x += lerp(-460, 0, e_out(prog(t, T["congrats"] + 0.2 + i * 0.08, T["congrats"] + 0.95 + i * 0.08)))
                    got = self.wins[i][1] + 0.55
                    pose = "cheer" if (t < s("break1") or t >= got) else "look"
                    if x < KX[i] - 8:
                        pose = "walk"
                    hold = (0, 1, 3)[i] if t >= got else None
                elif t < s("fix2") - 0.12:
                    go = prog(t, T["plays"] - 1.2, T["plays"] - 0.2)
                    if i == 0:
                        x = 30
                        pose = "look" if t < T["nobody"] + 0.75 else "shrug"
                    if go > 0:
                        x, pose, face = x - 640 * e_in(go), "walk", -1
                elif t < T["kid0"]:
                    pose = "look" if (t < T["alarm"] + 0.9 or t >= s("break4")) else "cheer"
                else:
                    if i == 0:
                        x, face = 178, -1
                    if t < T["flashing"]:
                        pose = "look"
                    elif t < T["slip"]:
                        pose = "cheer" if t < T["giant"] or t >= T["land"] else "look"
                    elif t < T["s1"] - 0.2:
                        pose = "shrug"
                    elif t < s("tag") - 0.2:
                        pose = "cheer"
                    else:
                        pose = "look"
                person(c, x, 0, h, col, t + i * 0.3, pose, face=face, hat=hat, hair="#3A2414")
                if hold is not None:
                    toy(c, hold, x, -h - 30 - (abs(math.sin((t + i * 0.3) * 9 + x)) * 7), 24)
            # ---- the one who shakes machines
            if s("break3") - 0.1 <= t < T["alarm"] + 1.3 and not (s("fix3") - 0.12 <= t < T["lets"] - 0.3):
                x, pose, face = -268, "carry", 1
                if t < T["shakes"] - 0.05:
                    x, pose = lerp(-760, -268, e_out(prog(t, s("break3") - 0.1, T["shakes"] - 0.05))), "walk"
                elif t < s("fix3"):
                    x += self.rock(t) * 2.2
                    if t >= T["chute"] + 0.48:
                        pose = "cheer"
                elif t >= T["alarm"] + 0.2:
                    x, pose, face = lerp(-268, -980, e_in(prog(t, T["alarm"] + 0.2, T["alarm"] + 1.2))), "walk", -1
                person(c, x, 0, 150, "#DC2626", t * 1.5, pose, face=face, hat="beanie")
                if T["chute"] + 0.48 <= t < s("fix3"):
                    toy(c, 3, x, -186 - abs(math.sin(t * 13.5 + x)) * 9, 25)
            if s("break1") <= t < s("fix1") - 0.12:                                  # everything they have won so far
                won = int((1 - self.level.at(t)) * 9)
                for j in range(won):
                    toy(c, j, (-470, -296, -430, -346, -452, -322, -396, -372, -440)[j], -22 - (30 if j >= 6 else 0), 22, (j * 37) % 40 - 20)
        elif m == "door":
            tk, tc = T["kid0"], T["crawl0"]
            col, t4 = "#F472B6", s("fix4")
            if tk <= t < tc:                                                         # here she comes
                person(c, lerp(-470, -240, e_out(prog(t, tk, tc))), 0, 92, col, t * 1.4, "walk", face=1, hair="#3A2414")
            elif t < tc + 0.85:                                                      # ... and in she goes
                self.through_door(c, t, prog(t, tc, tc + 0.85), col)
            elif t4 + 0.15 <= t < t4 + 0.5:                                          # out again
                self.through_door(c, t, 1 - prog(t, t4 + 0.15, t4 + 0.5), col)
            elif t >= t4 + 0.5:
                x = lerp(-236, -640, e_in(prog(t, t4 + 0.7, T["beam"])))
                person(c, x, 0, 92, col, t * 1.4, "walk" if t >= t4 + 0.7 else "cheer", face=-1, hair="#3A2414")
                toy(c, 0, x, -134, 22)
            if t >= T["stuck"] + 0.3:                                                # one of the crew comes to look
                x = lerp(-600, -350, e_out(prog(t, T["stuck"] + 0.3, T["stuck"] + 0.9)))
                pose = "walk" if t < T["stuck"] + 0.9 else "shrug" if t < t4 else "point" if t < t4 + 0.7 else "walk"
                if t >= t4 + 0.7:
                    x = lerp(-350, -700, e_in(prog(t, t4 + 0.7, T["beam"])))
                engineer(c, x, 0, 124, "#3B82F6", t, pose, face=1 if t < t4 + 0.7 else -1)

    def through_door(self, c, t, u, col):
        """The small kid climbing through the prize door: u 0 (standing outside) .. 1 (gone)."""
        k = e_io(clamp(u * 1.6))
        px, py = lerp(-240, DOOR[0] + 10, k), lerp(0, DOORC[1] + 50, k)
        sc = lerp(1.0, 0.55, e_in(clamp((u - 0.35) / 0.65)))
        c.save()
        if u > 0.45:
            c.clipRect(R(*DOOR))
        c.translate(px, py)
        c.rotate(lerp(0, 78, e_io(clamp(u * 1.8))))
        c.scale(sc, sc)
        person(c, 0, 0, 92, col, t * 1.8, "walk", face=1, hair="#3A2414", a=1 - prog(u, 0.82, 1.0))
        c.restore()

    def extras(self, c, t):
        """Things in front of the machine: toys leaving by the door, the coin, music, the ghost teddy, the mailbox."""
        T, s, e = self.T, self.tl.s, self.tl.e
        for t0, t1, kind, r, x0, y0, x1, y1, arc, where in self.fl:
            if where == "out" and t0 <= t < t1:
                u = prog(t, t0, t1)
                toy(c, kind, lerp(x0, x1, u), lerp(y0, y1, u) - arc * math.sin(math.pi * u), r, u * 300)
        if s("cta") <= t < e("cta") + 0.1 and self.mode(t) == "front":                # the coin, about to go in
            u = prog(t, e("cta") - 0.3, e("cta") - 0.12)
            cy_ = lerp(-556 + math.sin(t * 3.2) * 8, PANEL + 12, e_in(u))
            if u < 1:
                c.drawCircle(150, cy_, 52, P("#0B0A24", 0.45 * (1 - u), blur=10))
                add_glow(c, 150, cy_, 90, TRIM, 0.6)
                coin(c, 150, cy_, lerp(30, 14, u), spin=t * 2.6)
                for j in range(3):
                    gl = (t * 1.3 + j / 3) % 1.0
                    c.drawPath(star_path(150 + (j - 1) * 44, cy_ - 34 + (j % 2) * 52, 9 * math.sin(gl * math.pi), 3 * math.sin(gl * math.pi), 4, 0), P("#FFFFFF", 0.9))
        if t >= T["song"]:                                                           # the song that never stops
            for i in range(8):
                u = ((t - T["song"]) * 0.42 + i / 8) % 1.0
                if t - u / 0.42 < T["song"]:
                    continue
                sd = -1 if i % 2 else 1
                note(c, sd * (262 + 170 * u) + math.sin(u * 8 + i) * 16, -822 - 130 * u, 15 + 5 * (i % 3),
                     ("#67E8F9", "#FDE047", "#FB7185")[i % 3], min(1.0, u * 6) * (1 - u))
        if T["alarm"] <= t < T["alarm"] + 2.0 and t < s("break4") + 0.1:             # the alarm tells the whole mall
            for i in range(3):
                u = ((t - T["alarm"]) * 1.1 + i / 3) % 1.0
                r = 70 + 330 * u
                c.drawArc(R(-r, TOP - 22 - r, 2 * r, 2 * r), 205, 130, False, P("#FF6B6B", (1 - u) * 0.8, stroke=7))
        if T["bigger"] <= t < T["bonk"] + 0.7:                                       # would he fit through the prize door? no
            u = prog(t, T["bigger"], T["bonk"])
            back = prog(t, T["bonk"], T["bonk"] + 0.7)
            gx = lerp(TED[0], DOORC[0] + 60, e_in(u)) + 60 * e_out(back)
            gy = lerp(TED[1], -8, e_in(u)) - 30 * math.sin(back * math.pi)
            teddy(c, gx, gy, TED[2], bump(t, T["bonk"], T["bonk"] + 0.3), 0, False, a=0.5 * (1 - back))
            hl = prog(t, T["bigger"], T["bigger"] + 0.2) * (1 - prog(t, T["lives"] - 0.3, T["lives"] - 0.1))
            c.drawRRect(rr(DOOR[0] - 8, DOOR[1] - 8, DOOR[2] + 16, DOOR[3] + 16, 10), P(WARN, hl, stroke=7))
        if t >= T["lives"] + 0.1:                                                    # his mailbox
            mk = e_back(prog(t, T["lives"] + 0.1, T["lives"] + 0.4))
            c.drawRect(R(262, -150 * mk, 8, 150 * mk), P("#8E97AD"))
            box(c, 240, -150 * mk - 34 * mk, 60 * mk, 36 * mk, "#3B82F6", r=10 * mk)
            c.drawRect(R(294, -150 * mk - 62 * mk, 4, 34 * mk), P("#EF4444"))
            c.drawRect(R(294, -150 * mk - 62 * mk, 18 * mk, 12 * mk), P("#EF4444"))

    # ------------------------------------------------------------------ the world, the cameras
    def world(self, c, t, cam):
        T = self.T
        cx, cy, z = cam
        cx += math.sin(t * 0.6) * 3
        self.view(c, (cx, cy, z))
        self.arcade(c, t)
        if t < T["built"] + 0.1:                                                     # the hook: a claw over a box of toys
            a = 1 - prog(t, T["congrats"], T["congrats"] + 0.25)
            k = e_back(prog(t, 0.08, 0.5))
            if a > 0:
                c.save()
                c.scale(k, k)
                for i, (tx, kind) in enumerate(((-104, 0), (-52, 1), (0, 2), (52, 3), (104, 4))):
                    toy(c, kind, tx, -192 + (i % 2) * 14 + math.sin(t * 3 + i) * 3, 34, (i - 2) * 6, a)
                box(c, -160, -170, 320, 170, "#B7803F", r=8, a=a)
                for yy in (-128, -86, -44):
                    c.drawRect(R(-160, yy, 320, 4), P("#000000", 0.18 * a))
                for xx in (-146, 134):
                    c.drawRect(R(xx, -170, 12, 170), P("#8A5A2B", a))
                c.drawRect(R(-160, -170, 320, 10), P("#D9A566", a))
                c.restore()
        if t >= T["congrats"]:
            k = e_back(prog(t, T["congrats"], T["built"] + 0.1), 1.3)
            ang = self.rock(t)
            c.save()
            if k < 1:
                c.scale(lerp(0.75, 1.0, k), k)
            px = 200 if ang > 0 else -200
            c.translate(px, 0)
            c.rotate(ang)
            c.translate(-px, 0)
            self.machine(c, t)
            c.restore()
            sparks_shower(c, 0, -520, t, T["congrats"] + 0.1, 0.9, n=34, speed=780, col="#FDE047", cone=(180, 360))
        if t < T["built"]:                                                           # the claw on its rope
            hy = lerp(-1010, -385, e_io(prog(t, 0.1, T["claw"] + 0.15)))
            if t >= T["congrats"]:
                hy = lerp(-385, -692, e_io(prog(t, T["congrats"], T["built"])))
            sway = math.sin(t * 5) * 16 * (1 - prog(t, T["claw"], T["claw"] + 1.2))
            c.drawLine(0, -2800, sway, hy - 22, P("#DDE3EE", 1, stroke=3))
            claw(c, sway, hy, 0.8 + 0.2 * math.sin(t * 4))
        self.people(c, t)
        self.extras(c, t)
        c.restore()
        self.ui["cam"] = (cx, cy, z)

    def draw_front(self, c, t):
        self.world(c, t, self.cams["front"].at(t))

    def draw_claw(self, c, t):
        self.world(c, t, self.cams["claw"].at(t))

    def draw_base(self, c, t):
        self.world(c, t, self.cams["base"].at(t))

    def draw_door(self, c, t):
        self.world(c, t, self.cams["door"].at(t))

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B0A24", "#1C1247", "#2B1763"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -270, 1.0)), x, y)

    def ui_front(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            hx, hy = self.at(0, -385)
            self.label(hx + 34, hy, hx + 270, hy - 150, "claw", T["claw"] + 0.1, T["congrats"] - 0.05, HILITE)
        elif tw < s("fix1"):
            p = self.span(T["never"] + 0.3, s("fix1") - 0.2)
            if p > 0:
                v2.gauge(c, 40, 300, [(self.L["toys"], self.level.at(tw), "#F472B6")], p, w=262)
            self.badge("alert", T["empty"] - 0.15, s("fix1") - 0.2, x=975, y=470)
            self.red(T["empty"] - 0.15, 1.6)
        elif tw < s("fix2"):
            self.chip(160, 1000, "nocoins", T["plays"] - 0.4, s("fix2") - 0.2, accent=WARN, size=32)
            self.badge("alert", T["plays"] - 0.5, s("fix2") - 0.2, x=975, y=470)
            self.red(T["plays"] - 0.5, 1.6)
        elif tw < s("fix3"):
            cx_, cy_ = self.at(HOME, CHTOP + 50)
            self.label(cx_ - 20, cy_, 190, cy_ - 230, "chute", T["tumbles"] + 0.15, s("fix3") - 0.2, WARN)
            self.badge("alert", T["tumbles"], s("fix3") - 0.2, x=975, y=470)
            self.red(T["tumbles"], 1.6)
        elif tw < T["kid0"] + 0.1:
            bx_, by_ = self.at(0, TOP - 24)
            self.label(bx_ + 28, by_, 830, by_ - 46, "alarm", T["alarm"] + 0.15, T["alarm"] + 1.7, WARN)
            self.badge("check", T["alarm"] + 0.9, T["kid0"] - 0.15, x=930, y=500)
        elif tw >= s("tag") - 0.2:
            dx_, dy_ = self.at(DOOR[0], DOORC[1])
            self.label(dx_ - 6, dy_, 170, dy_ - 230, "pdoor", T["bigger"] - 0.1, T["lives"] - 0.15, WARN)
            self.chip(160, 640, "home", T["lives"] + 0.2, self.duration + 1, accent=HILITE, size=34)

    def ui_claw(self, c, t, tw):
        T, s = self.T, self.tl.s
        g = self.grip.at(tw)
        col = GOOD if g > 0.6 else WARN
        if tw < s("break2"):
            hx, hy = self.at(self.kx.at(tw), RAIL + 50 + self.kl.at(tw))
            self.label(hx + 44, hy, hx + 250, hy - 215, "magnet", T["magnet"] + 0.1, T["dial"] - 0.1, "#FFB347")
            p = self.span(T["dial"] - 0.1, s("break2") - 0.2)
            if p > 0:
                v2.gauge(c, 60, 300, [(self.L["grip"], g, col)], p, w=330)
            self.badge("check", T["drop"] + 0.3, s("break2") - 0.15)
        else:
            p = self.span(T["tight"] - 0.4, s("break3") - 0.2)
            if p > 0:
                v2.gauge(c, 60, 300, [(self.L["grip"], g, col)], p, w=330)
            self.chip(745, 650, "math", T["accounting"] - 0.1, s("break3") - 0.2, accent=HILITE, size=38)
            self.badge("check", T["win"] + 0.1, s("break3") - 0.15)

    def ui_base(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break3"):
            bx_, by_ = self.at(-40, -262)
            self.label(bx_, by_ + 24, 330, by_ - 190, "computer", T["computer"] + 0.05, T["coins"] - 0.15)
            if "cost" in self.wp:
                m1, m2 = self.at(*self.wp["cost"]), self.at(*self.wp["profit"])
                self.label(m1[0], m1[1], 730, m1[1] - 215, "cost", T["prize"] - 0.15, T["profit"] - 0.1, HILITE)
                self.label(m2[0], m2[1], 730, m2[1] - 215, "profit", T["profit"] - 0.05, T["tight"] - 0.45, GOOD)
        else:
            fx_, fy_ = self.at(252, -14)
            self.label(fx_ - 10, fy_, 800, fy_ - 215, "bolts", T["bolt"] + 0.35, T["sensor"] - 0.2)
            if "sensor" in self.wp:
                sx_, sy_ = self.at(*self.wp["sensor"])
                self.label(sx_ - 30, sy_, 275, sy_ - 430, "sensor", T["sensor"] + 0.05, T["lets"] - 0.35, WARN)

    def ui_door(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4"):
            self.badge("alert", T["stuck"], s("fix4") - 0.2, x=905, y=330)
            self.red(T["stuck"], 1.8)
            self.chip(235, 520, "true", T["happens"] - 0.5, s("fix4") - 0.15, accent=HILITE, size=38)
        else:
            lx_, ly_ = self.at(DOOR[0] + DOOR[2] + 8, DOOR[1] + DOOR[3] * 0.5)
            self.label(lx_, ly_, 860, ly_ - 150, "lock", T["lock"] + 0.15, T["beam"] - 0.15)
            bx_, by_ = self.at(CH1 - 12, -350)
            self.label(bx_, by_, 850, by_ - 140, "beam", T["beam"] + 0.15, T["opens"] - 0.05, WARN)
            self.badge("check", T["drops"] + 0.45, 1e9)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.pop(61), -5), (T["hang"] - 0.2, sfx.whirr(0.7, 220, 140, 62), -11),
              (T["claw"] + 0.15, sfx.clank(900, 0.25, 63), -9), (T["congrats"], sfx.whoosh(0.45, True, 64), -6),
              (T["built"] - 0.05, sfx.thud(0.4, 65), -4), (T["built"], sfx.sparkle(0.8, 10, 66), -7)]
        for i, (g, r) in enumerate(self.wins):
            ev += [(g - 0.5, sfx.whirr(0.5, 170, 240, 67 + i), -13), (g - 0.03, sfx.click(70 + i), -6), (r + 0.26, sfx.pop(73 + i), -7),
                   (r + 0.55, sfx.ding(), -9)]
        ev += [(T["empty"] - 0.15, sfx.alarm(3, 820), -11), (T["empty"], sfx.womp(), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 76), -4), (s("fix1") + 0.15, sfx.whirr(0.8, 200, 150, 77), -12),
               (T["magnet"], sfx.charge_up(0.5), -8), (T["magnet"] + 0.08, sfx.click(78), -5), (T["dial"] - 0.1, sfx.pop(79), -7),
               (T["lift"] - 0.4, sfx.whirr(0.8, 150, 230, 80), -11), (T["weak"], sfx.power_down(0.7, 81), -9),
               (T["drop"] + 0.2, sfx.thud(0.25, 82), -7), (T["drop"] + 0.3, sfx.chime(), -7)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 83), -4), (T["nobody"] - 0.32, sfx.whirr(0.4, 200, 150, 84), -12),
               (T["nobody"] - 0.04, sfx.click(85), -6), (T["nobody"] + 0.72, sfx.thud(0.25, 86), -8),
               (T["plays"] - 0.5, sfx.alarm(3, 820), -11), (T["plays"] - 0.6, sfx.power_down(0.9, 87), -10)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 88), -4), (T["computer"], sfx.beep(1500, 0.08), -8),
               (T["computer"] + 0.12, sfx.beep(1900, 0.08), -8)]
        ev += [(tc + 0.24, coin_snd(i), -6) for i, tc in enumerate(self.coin_t)]
        ev += [(T["profit"], sfx.charge_up(0.6), -8), (T["profit"] + 0.1, sfx.chime(), -8),
               (T["tight"] - 0.45, sfx.whoosh(0.4, False, 90), -4), (T["tight"] - 0.3, sfx.click(91), -5),
               (T["tight"] + 0.05, sfx.whirr(0.9, 150, 240, 92), -11), (T["win"], sfx.ding(), -5), (T["win"] + 0.05, sfx.sparkle(0.7, 9, 93), -7)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, True, 94), -4)]
        ev += [(T["shakes"] + i * 0.37, sfx.thud(0.3, 95 + i), -5) for i in range(int(max(1, (T["chute"] - T["shakes"]) / 0.37)))]
        ev += [(T["shakes"] + 0.18 + i * 0.37, sfx.clank(520, 0.2, 105 + i), -11) for i in range(int(max(1, (T["chute"] - T["shakes"]) / 0.37)))]
        ev += [(T["tumbles"], sfx.alarm(3, 820), -11), (T["chute"] + 0.05, sfx.thud(0.2, 115), -8), (T["chute"] + 0.2, sfx.pop(116), -6)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 117), -4), (self.bolt_t[0] + 0.14, sfx.clank(300, 0.35, 118), -3),
               (self.bolt_t[1] + 0.14, sfx.clank(280, 0.35, 119), -3), (T["sensor"], sfx.pop(120), -7),
               (T["shove"], sfx.thud(0.4, 121), -3), (T["shove"] + 0.1, sfx.beep(2000, 0.12), -6),
               (T["lets"] - 0.3, sfx.whoosh(0.4, False, 122), -5), (T["lets"], sfx.click(123), -5), (T["lets"] + 0.28, sfx.thud(0.25, 124), -8),
               (T["alarm"], sfx.alarm(7, 1150, 0.11, 0.07), -7), (T["alarm"] + 0.9, sfx.chime(), -8)]
        ev += [(T["alarm"] + 0.25 + i * 0.13, sfx.tap(125 + i), -11) for i in range(6)]
        ev += [(T["kid0"], sfx.whoosh(0.4, True, 132), -5)]
        ev += [(T["kid0"] + 0.1 + i * 0.13, sfx.tap(133 + i), -12) for i in range(3)]
        ev += [(T["crawl0"], sfx.creak(0.6, 137), -7), (T["stuck"] - 0.3, sfx.pop(138), -5), (T["stuck"], sfx.alarm(3, 820), -11),
               (T["happens"] - 0.5, sfx.pop(139), -8)]
        ev += [(s("fix4") + 0.1, sfx.creak(0.4, 140), -8), (s("fix4") + 0.5, sfx.pop(141), -8), (T["lock"], sfx.lock_click(142), -2),
               (T["beam"] - 0.1, sfx.beep(1700, 0.09), -7), (T["beam"] + 0.05, sfx.beep(2100, 0.09), -7),
               (T["opens"], sfx.buzz(0.3), -9), (T["drops"] - 0.22, sfx.whoosh(0.3, False, 143), -9), (T["drops"], sfx.beep(2400, 0.12), -5),
               (T["drops"] + 0.05, sfx.lock_click(144), -4), (T["drops"] + 0.12, sfx.creak(0.4, 145), -8), (T["drops"] + 0.45, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(146), 0), (T["follow"] - 0.15, sfx.pop(147), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 148), -7),
               (e("cta") - 0.12, coin_snd(1), -4)]
        ev += [(T["flashing"] - 0.05, sfx.sparkle(0.9, 12, 149), -7), (T["flashing"], sfx.charge_up(0.5), -10),
               (T["song"], jingle(2), -11), (T["giant"], sfx.whoosh(0.35, False, 150), -6), (T["land"], boom(0.8, 151), -4),
               (T["lift2"] - 0.5, sfx.whirr(0.9, 150, 330, 152), -9), (T["slip"], sfx.snap(153), -5), (T["slip"] + 0.05, sfx.pop(154), -6)]
        ev += [(T["s1"], sfx.pop(155), -3), (T["s2"], sfx.pop(156), -3), (T["s3"], sfx.pop(157), -3), (T["s1"] - 0.3, sfx.whoosh(1.2, False, 158), -12),
               (T["s1"] + 0.3, jingle(2), -17)]
        ev += [(T["cong2"], sfx.pop(159), -2), (T["cong2"], sfx.sparkle(1.0, 14, 160), -4), (e("closer") - 0.4, sfx.chime(), -6),
               (T["cong2"] + 0.4, jingle(1), -17)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 161), -6), (T["bigger"], sfx.whoosh(0.4, True, 162), -9), (T["bonk"], sfx.thud(0.3, 163), -4),
               (T["bonk"] + 0.05, sfx.buzz(0.3), -9), (T["lives"], sfx.pop(164), -6), (T["lives"] + 0.12, sfx.pop(165), -7),
               (T["lives"] + 0.4, sfx.womp(), -3), (T["lives"] + 1.3, jingle(1), -15)]
        return ev


NAME = "claw"
EPISODE = Claw
