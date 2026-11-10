"""Episode 19 - A hydroelectric dam.  v2 look: one world and one board.

river   the canyon cut open along the river: riverbed at y = 0, the lake on the left, the dam's upstream face at
        x = -40, its crest at y = -520, the powerhouse at its toe (x 270..430), downstream to the right
plan    the dam from straight above: the arch between the canyon walls (drawn straight on the screen)
"""
from v2_base import *  # noqa: F401,F403

CREST, FULL, WATERC = -520, -470, "#2563EB"
PEN = [(-46, -300), (40, -300), (250, -70), (300, -52)]              # the penstock, intake to turbine
SPILL = [(-170, -486), (-120, -470), (30, -430), (330, -250), (560, -120), (640, -96)]   # the spillway tunnel, behind the dam
STEPS = [(520 - i * 48, -i * 52) for i in range(11)]                  # the fish ladder, river to crest


class Line:
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

    def path(self, d1=None):
        d1 = self.len if d1 is None else min(d1, self.len)
        p = skia.Path()
        p.moveTo(*self.pts[0])
        acc = 0.0
        for i, sl in enumerate(self.seg):
            if acc + sl < d1:
                p.lineTo(*self.pts[i + 1])
            acc += sl
        p.lineTo(*self.at(d1))
        return p


PENL, SPL = Line(PEN), Line(SPILL)


def dam_path():
    p = skia.Path()
    p.moveTo(-74, 0)
    p.lineTo(-40, CREST)
    p.lineTo(34, CREST)
    p.cubicTo(60, -330, 150, -110, 262, 0)
    p.close()
    return p


def fish(c, x, y, s=1.0, rot=0.0, face=-1, col="#FB7185", shades=False, a=1.0):
    """A salmon, nose at the `face` side."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s * -face, s)                                                            # drawn nose to the left, flipped for face = 1
    c.drawOval(R(-26, -11, 46, 22), lin_paint(0, -11, 0, 11, [(col, a), ("#FDA4AF", a), ("#E5E9F2", a)]))
    tail = skia.Path()
    tail.moveTo(16, 0)
    tail.lineTo(34, -13)
    tail.lineTo(30, 0)
    tail.lineTo(34, 13)
    tail.close()
    c.drawPath(tail, P(col, a))
    c.drawCircle(-16, -3, 3.2, P("#111827", a))
    if shades:
        c.drawRRect(rr(-24, -8, 16, 8, 3), P("#111827", a))
    c.restore()


def rock(c, x, y, r, seed=0, a=1.0):
    rng = random.Random(seed)
    p = skia.Path()
    n = 7
    for i in range(n):
        an = 2 * math.pi * i / n
        rr_ = r * rng.uniform(0.78, 1.1)
        px, py = x + math.cos(an) * rr_, y + math.sin(an) * rr_ * 0.8
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    c.drawPath(p, lin_paint(0, y - r, 0, y + r, [("#94A3B8", a), ("#64748B", a), ("#3B4560", a)]))


def pylon(c, x, y, h=230, a=1.0):
    c.drawLine(x - 30, y, x - 8, y - h, P("#CBD5E1", a, stroke=5))
    c.drawLine(x + 30, y, x + 8, y - h, P("#CBD5E1", a, stroke=5))
    for i in range(4):
        yy = y - h * (i + 0.5) / 5
        w = lerp(28, 10, (i + 0.5) / 5)
        c.drawLine(x - w, yy, x + w, yy - h / 6, P("#94A3B8", a, stroke=3))
        c.drawLine(x + w, yy, x - w, yy - h / 6, P("#94A3B8", a, stroke=3))
    for yy, ww in ((y - h, 54), (y - h + 40, 42)):
        c.drawLine(x - ww, yy, x + ww, yy, P("#CBD5E1", a, stroke=5))


def rain_snd(d=3.0, seed=2):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 1500, 8000)
    return sfx._norm(x * sfx._ar(n, 0.4, 0.8), 0.35)


def thunder(d=1.6, seed=4):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._lp(sfx._rng(seed).standard_normal(n), 240) * np.exp(-tt * 2.2) * (1 + 0.6 * np.sin(2 * np.pi * 5 * tt))
    return sfx._norm(x, 0.8)


def roar(d=2.0, seed=6, lo=120, hi=2200):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), lo, hi)
    return sfx._norm(x * sfx._ar(n, d * 0.25, d * 0.4), 0.5)


def plop(seed=0):
    n = int(0.18 * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 700 - 2200 * tt + seed * 40
    return sfx._norm(np.sin(2 * np.pi * np.cumsum(np.maximum(f, 120)) / sfx.SR) * sfx._env(n, 0.004, 0.06), 0.7)


def gen_hum(d=2.0):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 60 + 60 * np.minimum(1, tt / (d * 0.5))
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 2) / sfx.SR) + 0.25 * np.sin(2 * np.pi * np.cumsum(f * 3) / sfx.SR)
    return sfx._norm(x * sfx._ar(n, 0.2, 0.5), 0.5)


# ====================================================================================== the episode
class Dam(EpisodeV2):
    BUILD_NO = 19
    FIRST_SET = "river"
    CLEAR = "#0B1024"
    TITLE = {"en": "DAM", "ar_sa": "سد"}
    EMPH = {"en": ["CONGRATS", "DAM", "ROCKS", "DEEPER", "HARDER", "DOWNSTREAM", "CONCRETE", "THICKEST", "ARCH", "CANYON", "NOTHING", "TEENAGER",
                   "PENSTOCKS", "TURBINES", "GENERATORS", "ELECTRICITY", "STORM", "WATERFALL", "SPILLWAYS", "NIAGARA", "TWICE", "SALMON", "WALL",
                   "LADDER", "POOLS", "FOLLOW", "CAR", "ROAD", "GIFT", "SEVENTEEN", "MILLION", "YOURSELF", "LAZY", "ELEVATOR", "REAL"],
            "ar_sa": ["مبروك", "سد", "صخور", "تعمق", "أقوى", "التيار", "بالخرسانة", "أسمك", "القوس", "الوادي", "شي", "مراهق", "مواسير", "توربينات",
                      "مولدات", "الكهربا", "عاصفة", "شلال", "مفيضات", "نياجرا", "مرتين", "السلمون", "جدار", "سلّم", "أحواض", "تابعني", "سباق",
                      "وطريق", "هدايا", "سبعطعش", "لمليون", "بيدك", "الكسلان", "أصنصير", "صدق"]}
    KEYS = {"ar_sa": {
        ("hook", "BLOCK"): "سدّيت", ("hook", "RIVER"): "نهر", ("hook", "PILE"): "بكومة", ("hook", "ROCKS"): "صخور", ("hook", "CONGRATS"): "مبروك",
        ("break1", "LAKE"): "البحيرة", ("break1", "DAY"): "يوم", ("break1", "PUSHES"): "تدف", ("break1", "HARDER"): "أقوى", ("break1", "SHOVES"): "تجرف",
        ("break1", "DOWNSTREAM"): "التيار",
        ("fix1", "CONCRETE"): "بالخرسانة", ("fix1", "THICKEST"): "أسمك", ("fix1", "BOTTOM"): "تحت", ("fix1", "CURVED"): "ومقوّس", ("fix1", "ARCH"): "القوس",
        ("fix1", "SQUEEZES"): "تضغطه", ("fix1", "CANYON"): "جدران", ("fix1", "WALLS"): "الوادي",
        ("break2", "HOLDS"): "صامد", ("break2", "WATER"): "هالموية", ("break2", "NOTHING"): "شي", ("break2", "TEENAGER"): "مراهق",
        ("fix2", "PIPES"): "مواسير", ("fix2", "WALL"): "الجدار", ("fix2", "FALLING"): "تطيح", ("fix2", "SPINS"): "تدوّر", ("fix2", "TURBINES"): "توربينات",
        ("fix2", "GENERATORS"): "مولدات", ("fix2", "ELECTRICITY"): "الكهربا",
        ("break3", "STORM"): "عاصفة", ("break3", "FILLS"): "تملأ", ("break3", "BRIM"): "آخرها", ("break3", "WATERFALL"): "شلال",
        ("fix3", "SPILLWAYS"): "مفيضات", ("fix3", "GATES"): "بوابات", ("fix3", "CHUTES"): "ومجاري", ("fix3", "OUT"): "تطلّع", ("fix3", "NIAGARA"): "نياجرا",
        ("fix3", "TWICE"): "مرتين",
        ("break4", "SAFE"): "آمن", ("break4", "SALMON"): "السلمون", ("break4", "EGGS"): "يبيض", ("break4", "HIT"): "ويصدم", ("break4", "WALL"): "جدار",
        ("fix4", "LADDER"): "سلّم", ("fix4", "STAIRCASE"): "درج", ("fix4", "POOLS"): "أحواض", ("fix4", "JUMP"): "ينط", ("fix4", "STEP"): "درجة",
        ("cta", "FLIP"): "تشغّل", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "POWER"): "أبراج", ("reveal", "ROAD"): "وطريق", ("reveal", "GIFT"): "ومحل",
        ("stat", "ONE"): "جدار", ("stat", "SEVENTEEN"): "سبعطعش", ("stat", "MILLION"): "لمليون",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "LAZY"): "الكسلان", ("tag", "SOME"): "بعض", ("tag", "ELEVATOR"): "أصنصير", ("tag", "REAL"): "صدق", ("tag", "CHECKED"): "تأكدنا"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a race car"),
                   "stat": [("1", "WALL"), ("17", "TURBINES"), ("1M", "PEOPLE")],
                   "L": {"pile": "YOUR DAM", "push": "DEEPER = MORE PUSH", "thick": "THICKEST AT THE BOTTOM", "arch": "AN ARCH", "walls": "CANYON WALLS",
                         "lazy": "DOING NOTHING", "pen": "PENSTOCK", "turb": "TURBINE", "gen": "GENERATOR", "storm": "FULL TO THE BRIM",
                         "spill": "SPILLWAY", "gates": "GATES", "niagara": "NIAGARA FALLS x2", "salmon": "SALMON", "ladder": "FISH LADDER",
                         "switch": "THE SWITCH", "shop": "GIFT SHOP", "lift": "FISH ELEVATOR"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: سيارة سباق"),
                      "stat": [("1", "جدار"), ("17", "توربين"), ("1M", "شخص")],
                      "L": {"pile": "السد حقك", "push": "أعمق = دفع أقوى", "thick": "أسمك شي من تحت", "arch": "قوس", "walls": "جدران الوادي",
                            "lazy": "ما تسوي شي", "pen": "ماسورة عملاقة", "turb": "توربين", "gen": "مولّد", "storm": "مليانة لآخرها",
                            "spill": "مفيض", "gates": "بوابات", "niagara": "شلالات نياجرا مرتين", "salmon": "سلمون", "ladder": "سلّم السمك",
                            "switch": "المفتاح", "shop": "محل هدايا", "lift": "أصنصير السمك"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "block": ("hook", "BLOCK", 0.14), "river": ("hook", "RIVER", 0.26), "pile": ("hook", "PILE", 0.46), "rocks": ("hook", "ROCKS", 0.58),
            "congrats": ("hook", "CONGRATS", 0.64),
            "lake": ("break1", "LAKE", 0.1), "day": ("break1", "DAY", 0.3), "pushes": ("break1", "PUSHES", 0.5), "harder": ("break1", "HARDER", 0.58),
            "shoves": ("break1", "SHOVES", 0.76), "downstream": ("break1", "DOWNSTREAM", 0.92),
            "concrete": ("fix1", "CONCRETE", 0.18), "thickest": ("fix1", "THICKEST", 0.28), "bottom": ("fix1", "BOTTOM", 0.38), "curved": ("fix1", "CURVED", 0.5),
            "arch": ("fix1", "ARCH", 0.6), "squeezes": ("fix1", "SQUEEZES", 0.76), "canyon": ("fix1", "CANYON", 0.9), "walls": ("fix1", "WALLS", 0.96),
            "holds": ("break2", "HOLDS", 0.12), "water": ("break2", "WATER", 0.34), "nothing": ("break2", "NOTHING", 0.54), "teenager": ("break2", "TEENAGER", 0.72),
            "pipes": ("fix2", "PIPES", 0.14), "wall": ("fix2", "WALL", 0.36), "falling": ("fix2", "FALLING", 0.48), "spins": ("fix2", "SPINS", 0.58),
            "turbines": ("fix2", "TURBINES", 0.62), "generators": ("fix2", "GENERATORS", 0.76), "electricity": ("fix2", "ELECTRICITY", 0.92),
            "storm": ("break3", "STORM", 0.14), "fills": ("break3", "FILLS", 0.2), "brim": ("break3", "BRIM", 0.4), "waterfall": ("break3", "WATERFALL", 0.9),
            "spillways": ("fix3", "SPILLWAYS", 0.12), "gates": ("fix3", "GATES", 0.26), "chutes": ("fix3", "CHUTES", 0.34), "out": ("fix3", "OUT", 0.56),
            "niagara": ("fix3", "NIAGARA", 0.78), "twice": ("fix3", "TWICE", 0.95),
            "safe": ("break4", "SAFE", 0.14), "salmon": ("break4", "SALMON", 0.36), "eggs": ("break4", "EGGS", 0.72), "hit": ("break4", "HIT", 0.86),
            "wall2": ("break4", "WALL", 0.96),
            "ladder": ("fix4", "LADDER", 0.2), "staircase": ("fix4", "STAIRCASE", 0.38), "pools": ("fix4", "POOLS", 0.56), "jump": ("fix4", "JUMP", 0.68),
            "step": ("fix4", "STEP", 0.84),
            "flip": ("cta", "FLIP", 0.22), "follow": ("cta", "FOLLOW", 0.42),
            "power": ("reveal", "POWER", 0.2), "road": ("reveal", "ROAD", 0.5), "gift": ("reveal", "GIFT", 0.86),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "SEVENTEEN", 0.26), "s3": ("stat", "MILLION", 0.76),
            "cong2": ("closer", "CONGRATS", 0.16),
            "lazy": ("tag", "LAZY", 0.12), "some": ("tag", "SOME", 0.32), "elevator": ("tag", "ELEVATOR", 0.56), "real": ("tag", "REAL", 0.8),
            "checked": ("tag", "CHECKED", 0.95)})
        T["wash"] = T["shoves"] - 0.05
        T["plancut"] = min(T["curved"], T["arch"]) - 0.35
        T["over"] = T["brim"] + 0.2                                    # the lake comes over the top
        T["open"] = min(T["gates"], T["chutes"]) - 0.1
        T["bonk"] = min(T["hit"], T["wall2"])
        T["built"] = min(T["ladder"], T["staircase"]) - 0.15
        T["hop"] = min(T["jump"], T["pools"]) + 0.1
        self.cut(s("fix1") - 0.12, "river", 1)
        self.cut(T["plancut"], "plan", 1)
        self.cut(s("break2") - 0.1, "river", -1)
        self.cut(s("fix2") - 0.12, "river", 1)
        self.cut(s("break3") - 0.1, "river", -1)
        self.cut(s("fix3") - 0.12, "river", 1)
        self.cut(s("break4") - 0.12, "river", -1)
        self.cut(s("fix4") - 0.12, "river", 1)
        self.cut(s("cta") + 0.05, "river", -1)
        self.cut(s("reveal") - 0.1, "river", 1)
        self.cut(T["s1"] - 0.35, "river", 1)
        self.cut(s("tag") - 0.2, "river", -1)
        cm = Camera(60, -120, 2.0)
        cm.key(0.05, 70, -118, 2.2, 1.5)
        cm.key(s("break1") - 0.1, -10, -175, 1.55, 1.0).key(T["wash"] - 0.2, 110, -150, 1.6, 0.8)
        cm.key(s("fix1") - 0.12, 60, -187, 1.5, 0.0)
        cm.key(s("break2") - 0.1, -60, -187, 1.5, 0.0).key(T["teenager"] - 0.6, -210, -360, 2.2, 0.8)
        cm.key(s("fix2") - 0.12, 170, -150, 1.9, 0.0).key(T["generators"] - 0.5, 300, -128, 2.2, 0.8)
        cm.key(s("break3") - 0.1, 60, -187, 1.5, 0.0)
        cm.key(s("fix3") - 0.12, -20, -187, 1.5, 0.0).key(T["out"] - 0.5, 260, -187, 1.5, 0.9)
        cm.key(s("break4") - 0.12, 380, -122, 2.2, 0.0)
        cm.key(s("fix4") - 0.12, 300, -200, 1.45, 0.0)
        cm.key(s("cta") + 0.05, 370, -108, 2.6, 0.0)
        cm.key(s("reveal") - 0.1, 400, -250, 1.1, 0.0).key(T["gift"] - 0.6, 520, -250, 1.1, 0.8)
        cm.key(T["s1"] - 0.35, 230, -190, 0.98, 0.0).key(s("closer"), 230, -195, 1.04, 2.4)
        cm.key(s("tag") - 0.2, 590, -230, 1.9, 0.0)
        self.cam = cm
        self.lake = (Track(-22.0).to(T["rocks"] - 0.1, -74.0, 0.8).to(T["lake"], -132.0, max(0.8, T["harder"] - T["lake"]))
                     .to(T["wash"], -40.0, 0.7).to(s("fix1") - 0.12, -40.0, 0.01).to(T["concrete"] + 0.3, FULL, max(0.8, T["bottom"] - T["concrete"]))
                     .to(T["fills"] - 0.2, CREST - 8, max(0.5, T["over"] - T["fills"] + 0.2)).to(T["open"] + 0.3, FULL - 4, max(0.8, T["niagara"] - T["open"])))
        self.power = Track(0.0).to(T["spins"], 1.0, max(0.5, T["electricity"] - T["spins"])).to(T["over"] + 0.3, 0.0, 0.4).to(T["out"], 1.0, 0.8)
        self.spans = [(T["wash"], T["walls"]), (T["nothing"], T["electricity"]), (T["over"], T["twice"]), (T["bonk"], T["step"])]
        self.shakes = [(T["wash"], 0.5, 14), (T["concrete"], 0.3, 8), (T["over"], 0.5, 10), (T["open"], 0.3, 8), (T["bonk"], 0.2, 6)]

    def phase(self, t):
        s, T = self.tl.s, self.T
        for name, t0 in (("tag", s("tag") - 0.2), ("stat", T["s1"] - 0.35), ("reveal", s("reveal") - 0.1), ("cta", s("cta") + 0.05), ("ladder", s("fix4") - 0.12),
                         ("fish", s("break4") - 0.12), ("spill", s("fix3") - 0.12), ("storm", s("break3") - 0.1), ("power", s("fix2") - 0.12),
                         ("lazy", s("break2") - 0.1), ("concrete", s("fix1") - 0.12), ("flood", s("break1") - 0.1), ("pile", 0.0)):
            if t >= t0:
                return name

    # ------------------------------------------------------------------ set: the river
    def draw_river(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.cam.at(t)
        cam = (cam[0] + math.sin(t * 0.5) * 3, cam[1], cam[2])
        cx, cy, z = cam
        ph = self.phase(t)
        gy = (0 - cy) * z + H / 2
        stormk = prog(t, T["storm"] - 0.4, T["storm"] + 0.3) * (1 - prog(t, T["out"], T["niagara"])) if ph in ("storm", "spill") else 0.0
        v2.sky(c, W, H, 0.0, horizon_y=gy - 200 * z)
        v2.stars(c, W, H, t, 0.5 * (1 - stormk))
        c.save()                                                                     # the far canyon walls
        c.translate(W / 2 - cx * 0.25 * z, gy)
        c.scale(z, z)
        v2.ridge(c, -1900, 1900, 0, 700, "#2C2F63", "#191B40", seed=4, step=70, rough=0.7, peaks=7)
        c.restore()
        if stormk > 0:
            c.drawRect(R(0, 0, W, H), P("#05070F", 0.45 * stormk))
            for i in range(4):
                v2.cloud(c, 140 + i * 280 + math.sin(t * 0.4 + i) * 40, 300 + (i % 2) * 70, 1.3, body="#05060F", rim="#1B2140", a=stormk, seed=i)
            if (t * 1.7) % 1.0 < 0.06:
                c.drawRect(R(0, 0, W, H), P("#FFFFFF", 0.35 * stormk))
        self.view(c, cam)
        v2.ground(c, -3400, 3400)
        lake = self.lake.at(t)
        dam_up = ph not in ("pile", "flood")
        k_dam = e_out(prog(t, T["concrete"] - 0.3, T["concrete"] + 0.5)) if ph == "concrete" else 1.0 if dam_up else 0.0
        # the spillway tunnel, behind everything
        if ph in ("spill", "fish", "ladder", "cta", "reveal", "stat", "tag"):
            sk = prog(t, T["spillways"] - 0.2, T["open"] + 0.2) if ph == "spill" else 1.0
            pp = P("#3B4560", 1, stroke=64)
            pp.setStrokeCap(skia.Paint.kRound_Cap)
            pp.setStrokeJoin(skia.Paint.kRound_Join)
            c.drawPath(SPL.path(SPL.len * sk), pp)
            pp2 = P("#141B34", 1, stroke=50)
            pp2.setStrokeCap(skia.Paint.kRound_Cap)
            pp2.setStrokeJoin(skia.Paint.kRound_Join)
            c.drawPath(SPL.path(SPL.len * sk), pp2)
            flow = prog(t, T["open"], T["open"] + 0.6) * (1 - prog(t, T["twice"] + 0.3, T["twice"] + 1.0)) if ph == "spill" else 0.0
            if flow > 0:
                pw = P("#60A5FA", 0.9, stroke=40)
                pw.setStrokeCap(skia.Paint.kRound_Cap)
                pw.setStrokeJoin(skia.Paint.kRound_Join)
                c.drawPath(SPL.path(SPL.len * flow), pw)
                for i in range(12):
                    d = ((t * 420 + i * SPL.len / 12) % SPL.len)
                    if d < SPL.len * flow:
                        x, y = SPL.at(d)
                        c.drawCircle(x, y + math.sin(i * 3) * 9, 6, P("#DBEAFE", 0.9))
                if flow >= 1:                                                        # the jet at the far end
                    for i in range(14):
                        u = (t * 1.6 + i / 14) % 1.0
                        c.drawCircle(640 + u * 250, -96 + 150 * u * u - 20 * u + math.sin(i * 5) * 12, 12 * (1 - 0.4 * u), P("#BFDBFE", 0.85 * (1 - u)))
                    puff(c, 880 + math.sin(t * 5) * 10, -30, 70, "#DBEAFE", 0.5, k=1)
        # the lake and the river
        left_wall = -74 if dam_up else (-60 if ph == "pile" or t < T["wash"] else 2000)
        if lake < -4:
            self.water(c, -2600, left_wall, lake, t)
        tail = -40 if dam_up else -22
        self.water(c, left_wall if not dam_up else 262, 2600, tail if (dam_up or t < T["wash"]) else lerp(-22, -150, bump(t, T["wash"], T["wash"] + 1.6)) , t, deep=False)
        # the pile of rocks
        if not dam_up:
            self.pile(c, t)
            if ph == "flood" and t < T["wash"]:
                for i in range(3):
                    yy = lake + 26 + i * 34
                    ak = prog(t, T["pushes"] - 0.3 + i * 0.08, T["pushes"] + i * 0.08)
                    if yy < -8 and ak > 0:
                        ln = (34 + i * 26) * ak * (1 + 0.15 * math.sin(t * 9))
                        c.drawLine(-96 - ln, yy, -96, yy, P("#DBEAFE", 1, stroke=8))
                        for dyy in (-11, 11):
                            c.drawLine(-96, yy, -112, yy + dyy, P("#DBEAFE", 1, stroke=8))
        # the dam
        if k_dam > 0:
            c.save()
            c.clipRect(R(-400, CREST * k_dam - 30, 1000, 2000))
            dp = dam_path()
            c.drawPath(dp, lin_paint(-74, 0, 262, 0, ["#C9CFDC", "#A3ABBD", "#6B7389"]))
            c.save()
            c.clipPath(dp, skia.ClipOp.kIntersect, True)
            for yy in range(-52, CREST, -52):
                c.drawLine(-100, yy, 300, yy, P("#000000", 0.10, stroke=2))
            rng = random.Random(8)
            for _ in range(120):
                c.drawCircle(rng.uniform(-70, 250), rng.uniform(CREST, 0), rng.uniform(1.5, 4), P("#000000" if rng.random() < 0.6 else "#FFFFFF", 0.08))
            c.restore()
            c.drawRect(R(-46, CREST - 8, 86, 10), P("#E5E9F2"))                           # the crest
            c.restore()
        if ph == "concrete" and k_dam >= 1 and t < T["plancut"]:                       # deeper water, harder push
            for i in range(6):
                yy = lake + 40 + i * 70
                if yy < -10:
                    ln = 30 + i * 22
                    ak = prog(t, T["thickest"] - 0.3 + i * 0.05, T["thickest"] + i * 0.05)
                    x1 = -70 + (yy / CREST) * 30
                    c.drawLine(x1 - ln * ak - 14, yy, x1 - 14, yy, P("#BFDBFE", ak, stroke=7))
                    for dyy in (-10, 10):
                        c.drawLine(x1 - 14, yy, x1 - 30, yy + dyy, P("#BFDBFE", ak, stroke=7))
        # the power plant
        if ph in ("power", "storm", "spill", "fish", "ladder", "cta", "reveal", "stat", "tag"):
            self.plant(c, t, ph)
        if ph == "lazy":
            self.teen(c, t, lake)
        if ph == "storm":
            self.storm(c, t, lake)
        if ph in ("fish", "ladder", "tag", "reveal", "stat", "cta"):
            self.fishes(c, t, ph, lake)
        if ph in ("reveal", "stat", "tag"):
            self.extras(c, t, ph)
        self.people(c, t, ph)
        if stormk > 0:                                                               # rain
            rng = random.Random(1)
            for i in range(110):
                rx = cx + rng.uniform(-560, 560) / z * 1.0
                u = (t * (1.6 + rng.random()) + rng.random()) % 1.0
                ry = cy + (-520 + u * 1040) / z
                c.drawLine(rx, ry, rx - 10 / z, ry + 40 / z, P("#BFDBFE", 0.5 * stormk, stroke=2.5 / z))
        c.restore()
        self.ui["cam"] = cam
        self.ui["lake"] = lake

    def water(self, c, x0, x1, level, t, deep=True):
        if x1 <= x0:
            return
        vrect(c, x0, level, x1 - x0, -level + 2, ["#3B82F6", "#1D4ED8", "#172554"] if deep else ["#3B82F6", "#1E40AF"], None, a=0.92)
        p = skia.Path()
        p.moveTo(x0, level)
        x = x0
        while x < x1:
            x = min(x + 30, x1)
            p.lineTo(x, level + math.sin(x * 0.03 + t * 2.2) * 3)
        c.drawPath(p, P("#BFDBFE", 0.9, stroke=4))

    def pile(self, c, t):
        T = self.T
        spots = ((-30, -18, 34), (34, -16, 30), (96, -14, 26), (-64, -12, 22), (0, -58, 30), (60, -54, 28), (-36, -52, 24), (28, -92, 26), (-6, -122, 20))
        washed = t >= T["wash"]
        for i, (rx, ry, rr_) in enumerate(spots):
            t0 = 0.1 + i * (T["rocks"] - 0.5) / len(spots)
            k = e_in(prog(t, t0, t0 + 0.32))
            if k <= 0:
                continue
            x, y, rot = rx, lerp(ry - 520, ry, k), 0.0
            if washed:
                dt = t - T["wash"]
                x = rx + (420 + i * 60) * dt + 40 * dt * dt
                y = ry + min(0.0, -90 * math.sin(min(dt, 1.0) * math.pi) * (0.4 + (i % 3) * 0.3)) + (-ry - 14) * min(1.0, dt * 2)
            rock(c, x, y, rr_, seed=i)
        if washed:
            splash(c, 80, -30, t, T["wash"], 1.0, n=26, speed=620, seed=3)

    def plant(self, c, t, ph):
        """Penstock, turbine, generator and the little building over them."""
        T, s = self.T, self.tl.s
        pk = prog(t, T["pipes"] - 0.3, T["wall"] + 0.2) if ph == "power" else 1.0
        hk = e_back(prog(t, T["spins"] - 0.5, T["spins"] - 0.2)) if ph == "power" else 1.0
        run = self.power.at(t)
        inside = ph in ("power", "storm", "cta")                                      # show what is in the building
        pp = P("#475569", 1, stroke=34)
        pp.setStrokeCap(skia.Paint.kRound_Cap)
        pp.setStrokeJoin(skia.Paint.kRound_Join)
        c.drawPath(PENL.path(PENL.len * pk), pp)
        pp2 = P("#0F172A", 1, stroke=24)
        pp2.setStrokeCap(skia.Paint.kRound_Cap)
        pp2.setStrokeJoin(skia.Paint.kRound_Join)
        c.drawPath(PENL.path(PENL.len * pk), pp2)
        flowing = pk >= 1 and (ph != "power" or t >= T["falling"] - 0.3)
        if flowing:
            for i in range(11):
                d = (t * 300 + i * PENL.len / 11) % PENL.len
                x, y = PENL.at(d)
                c.drawCircle(x, y, 7, P("#60A5FA", 0.95))
        if hk > 0:
            box(c, 270, -150, 170, 150, "#55607F", r=8, a=hk)
            if inside:
                c.drawRRect(rr(280, -140, 150, 132, 6), P("#0B1220", hk))
                c.drawRRect(rr(296, -92, 72, 76, 34), P("#334155", hk))                # the scroll case
                c.save()
                c.translate(332, -54)
                c.rotate(t * 520 * run)
                for i in range(6):
                    c.save()
                    c.rotate(i * 60)
                    c.drawOval(R(4, -7, 26, 14), P("#7DD3FC", hk))
                    c.restore()
                c.drawCircle(0, 0, 7, P("#E5E9F2", hk))
                c.restore()
                gk = e_back(prog(t, T["generators"] - 0.3, T["generators"])) if ph == "power" else 1.0
                c.drawRect(R(328, -108, 8, 22), P("#CBD5E1", hk))                      # the shaft
                if gk > 0:
                    c.drawRRect(rr(332 - 34 * gk, -138, 68 * gk, 34, 8), P("#B45309"))
                    for i in range(5):
                        on = math.sin(t * 16 * run + i) > 0 and run > 0.3
                        c.drawRect(R(332 - 28 + i * 12, -134, 7, 26), P("#FDE047" if on else "#92400E", gk))
                # tailrace
                if flowing:
                    for i in range(5):
                        u = (t * 1.2 + i / 5) % 1.0
                        c.drawCircle(370 + u * 90, -30 + u * 6, 6, P("#60A5FA", 0.9 * (1 - u)))
            else:
                for wx in (290, 340, 390):
                    c.drawRRect(rr(wx, -120, 30, 44, 4), P("#FFE9B8", 0.9 * run + 0.08))
                c.drawRect(R(270, -156, 170, 10), P("#CBD5E1"))
            # the line out, and a bulb when it is all working
            if run > 0.05 and ph in ("power",):
                for i in range(3):
                    u = (t * 1.5 + i / 3) % 1.0
                    bx, by = lerp(366, 448, u), lerp(-150, -224, u)
                    z_ = skia.Path()
                    z_.moveTo(bx - 8, by - 12)
                    z_.lineTo(bx + 4, by - 2)
                    z_.lineTo(bx - 4, by + 2)
                    z_.lineTo(bx + 8, by + 12)
                    c.drawPath(z_, P("#FDE047", run * (1 - u), stroke=5))
                bk = prog(t, T["electricity"] - 0.3, T["electricity"])
                c.drawCircle(462, -256, 26, P(mix("#475569", "#FDE047", bk)))
                c.drawRRect(rr(451, -233, 22, 16, 4), P("#94A3B8"))
                add_glow(c, 462, -256, 90, "#FDE047", 0.7 * bk)

    def teen(self, c, t, lake):
        """All that water, doing nothing."""
        T = self.T
        x, y = -230 + math.sin(t * 0.7) * 16, lake + math.sin(t * 1.6) * 4
        c.drawOval(R(x - 64, y - 16, 128, 34), P("#F472B6"))
        c.drawOval(R(x - 34, y - 8, 68, 16), P("#1D4ED8"))
        c.save()
        c.translate(x - 6, y - 12)
        c.rotate(-80)
        engineer(c, 0, 50, 100, SHIRTS[1], t * 0.3, "stand", face=1)
        c.restore()
        c.drawRRect(rr(x - 66, y - 44, 26, 9, 3), P("#111827"))                        # sunglasses
        for j in range(2):
            u = (t * 0.5 + j * 0.5) % 1.0
            text(c, "z", x - 40 + u * 44, y - 66 - u * 50, 26 + 20 * u, "#FFFFFF", "Poppins-Black", a=0.9 * (1 - u))

    def storm(self, c, t, lake):
        """The lake comes over the top."""
        T = self.T
        ov = prog(t, T["over"], T["over"] + 0.5)
        if ov > 0:
            p = skia.Path()
            p.moveTo(-40, CREST - 12)
            p.lineTo(40, CREST - 12)
            p.cubicTo(70, -330, 160, -110, lerp(60, 290, ov), lerp(-400, 0, ov))
            p.lineTo(lerp(40, 262, ov), lerp(-420, 0, ov))
            p.cubicTo(140, -110, 46, -330, 30, CREST)
            p.close()
            c.drawPath(p, P("#60A5FA", 0.85))
            for i in range(12):
                u = (t * 1.8 + i / 12) % 1.0
                if u < ov:
                    bx = 40 + 222 * u ** 1.6
                    by = CREST + 520 * u ** 0.75
                    c.drawCircle(bx + 8, by, 7, P("#DBEAFE", 0.9))
            if ov >= 1:
                puff(c, 300 + math.sin(t * 6) * 8, -60, 80, "#DBEAFE", 0.6, k=2)
                sparks_shower(c, 350, -150, t, t - (t % 0.3), 0.4, n=8, speed=300, seed=int(t * 3), cone=(200, 340))

    def fishes(self, c, t, ph, lake):
        T, s = self.T, self.tl.s
        if ph == "fish":
            for i in range(5):
                arr = prog(t, T["salmon"] - 0.5 + i * 0.18, T["bonk"] + i * 0.12)
                x = lerp(900 + i * 40, 462 + i * 30, e_out(arr))
                y = -22 - (i % 2) * 10 + math.sin(t * 6 + i) * 4
                dizzy = arr >= 1
                fish(c, x + (math.sin(t * 20 + i) * 3 if dizzy else 0), y, 1.1, 180 if False else (math.sin(t * 5 + i) * 8), face=-1)
                if dizzy and i < 3:
                    for j in range(3):
                        an = t * 5 + j * 2.1 + i
                        c.drawCircle(x - 20 + math.cos(an) * 16, y - 26 + math.sin(an) * 6, 3.5, P("#FDE047"))
            return
        # the ladder: pools up the side, and fish going up it
        lk = prog(t, T["built"], T["built"] + 0.9) if ph == "ladder" else 1.0
        n = len(STEPS)
        for i, (sx, sy) in enumerate(STEPS[:-1]):
            kk = clamp(lk * n - i)
            if kk <= 0:
                continue
            box(c, sx - 52, sy - 22 * kk, 56, 22 * kk + 10, "#94A3B8", r=3)
            c.drawRect(R(sx - 46, sy - 22 * kk + 4, 44, 9), P("#60A5FA", kk))
            c.drawRect(R(sx - 52, sy - 34 * kk, 8, 34 * kk), P("#CBD5E1"))
        if lk >= 1:
            going = ph == "ladder" and t >= T["hop"]
            cnt = 4 if ph == "ladder" else 3
            for f in range(cnt):
                if ph == "ladder":
                    prog_f = (t - T["hop"] - f * 0.45) / 0.34 if going else -1
                else:
                    prog_f = ((t * 1.6 + f * 3.3) % (n + 3))
                if prog_f < 0:
                    fish(c, 560 + f * 44, -20 + math.sin(t * 6 + f) * 4, 1.0, 0, face=-1)
                    continue
                i = int(prog_f)
                u = prog_f - i
                if i >= n - 1:
                    continue
                x0, y0 = STEPS[i]
                x1, y1 = STEPS[i + 1]
                x = lerp(x0 - 24, x1 - 24, u)
                y = lerp(y0 - 14, y1 - 14, u) - 44 * math.sin(math.pi * u)
                fish(c, x, y, 0.9, -50 + 70 * u, face=-1)
        if ph == "tag":                                                              # ...and the fish elevator
            ek = e_back(prog(t, T["some"] - 0.2, T["some"] + 0.2))
            ex = 700
            c.drawRect(R(ex - 46, CREST - 20, 8, 520 + 20), P("#94A3B8", clamp(ek)))
            c.drawRect(R(ex + 38, CREST - 20, 8, 520 + 20), P("#94A3B8", clamp(ek)))
            c.drawRect(R(ex - 46, CREST - 28, 92, 10), P("#CBD5E1", clamp(ek)))
            up = e_io(prog(t, T["elevator"] - 0.3, T["checked"] + 0.4))
            cy_ = lerp(-60, CREST + 70, up)
            c.drawLine(ex, CREST - 20, ex, cy_ - 44, P("#E5E9F2", clamp(ek), stroke=3))
            c.drawRRect(rr(ex - 36, cy_ - 44, 72, 76, 8), P("#60A5FA", 0.75 * clamp(ek)))
            c.drawRRect(rr(ex - 36, cy_ - 44, 72, 76, 8), P("#E5E9F2", clamp(ek), stroke=4))
            fish(c, ex + 2, cy_ - 4, 1.05, math.sin(t * 2) * 5, face=-1, shades=True, a=clamp(ek))
            for i in range(3):
                c.drawCircle(ex - 20 + i * 14, cy_ - 30 - ((t * 30 + i * 9) % 20), 3, P("#DBEAFE", 0.8 * clamp(ek)))

    def extras(self, c, t, ph):
        """Power lines, a road across the top, a gift shop."""
        T, s = self.T, self.tl.s
        lk = prog(t, T["power"] - 0.2, T["power"] + 0.7) if ph == "reveal" else 1.0
        rk = prog(t, T["road"] - 0.2, T["road"] + 0.5) if ph == "reveal" else 1.0
        gk = e_back(prog(t, T["gift"] - 0.25, T["gift"] + 0.05)) if ph == "reveal" else 1.0
        # the far bank, level with the crest, for the road and the shop
        c.drawRect(R(760, CREST, 1800, 540), lin_paint(0, CREST, 0, 0, ["#3A4466", "#232A45"]))
        c.drawRect(R(760, CREST - 4, 1800, 8), P("#5C6B96"))
        for i, px in enumerate((400, 800, 1030)):
            kk = e_back(clamp(lk * 3 - i))
            if kk > 0:
                c.save()
                c.translate(px, -150 if i < 1 else CREST)
                c.scale(kk, kk)
                pylon(c, 0, 0, 230 if i < 1 else 190)
                c.restore()
        if lk >= 1:
            for (x0, y0), (x1, y1) in (((366, -150), (400, -380)), ((400, -380), (800, CREST - 190)), ((800, CREST - 190), (1030, CREST - 190)), ((1030, CREST - 190), (1500, CREST - 170))):
                p = skia.Path()
                p.moveTo(x0, y0)
                p.quadTo((x0 + x1) / 2, max(y0, y1) + 34, x1, y1)
                c.drawPath(p, P("#E5E9F2", 0.9, stroke=3))
                u = (t * 0.9) % 1.0
                bx, by = lerp(x0, x1, u), lerp(y0, y1, u) + 34 * math.sin(math.pi * u) * 0.5
                add_glow(c, bx, by, 26, "#FDE047", 0.9)
        if rk > 0:                                                                   # the road and who is on it
            c.drawRect(R(-46, CREST - 16, lerp(0, 2400, rk), 9), P("#1F2937"))
            if rk >= 1:
                for i in range(4):
                    u = (t * 0.1 + i / 4) % 1.0
                    cx_ = lerp(-80, 1300, u)
                    c.drawRRect(rr(cx_ - 20, CREST - 34, 40, 14, 5), P(("#F8FAFC", "#FDE68A", "#7DD3FC", "#F472B6")[i]))
                    c.drawRRect(rr(cx_ - 11, CREST - 44, 22, 12, 5), P(("#F8FAFC", "#FDE68A", "#7DD3FC", "#F472B6")[i]))
                    for wx in (-11, 11):
                        c.drawCircle(cx_ + wx, CREST - 20, 5.5, P("#111827"))
        if gk > 0:                                                                   # the gift shop
            c.save()
            c.translate(910, CREST - 4)
            c.scale(gk, gk)
            box(c, -56, -84, 112, 84, "#F8FAFC", r=5)
            c.drawRect(R(-12, -44, 26, 44), P("#7C5A3C"))
            c.drawRect(R(-46, -54, 26, 26), P("#7DD3FC"))
            c.drawRect(R(24, -54, 22, 26), P("#7DD3FC"))
            for i in range(7):
                c.drawRect(R(-63 + i * 18, -108, 18, 24), P("#F43F5E" if i % 2 == 0 else "#FFFFFF"))
            c.drawRRect(rr(-64, -112, 128, 7, 3), P("#BE123C"))
            heart(c, 0, -142, 0.5, 1.0)
            c.restore()

    def people(self, c, t, ph):
        T, s = self.T, self.tl.s
        if ph == "pile":
            self.crew(c, t, "cheer" if t >= T["congrats"] - 0.1 else "look", xs=(190, 232, 274), y=0, face=-1, h=104)
        elif ph == "flood":
            run = e_in(prog(t, T["wash"] - 0.2, T["wash"] + 0.8))
            self.crew(c, t * (1 + 2 * run), "walk" if run > 0 else "look", xs=tuple(x + 420 * run for x in (190, 232, 274)), y=0, face=1 if run > 0 else -1, h=104)
        elif ph == "concrete":
            self.crew(c, t, "cheer" if t >= T["bottom"] else "look", xs=(-22, 2, 26), y=CREST - 8, face=-1, h=56)
        elif ph == "ladder":
            self.crew(c, t, "cheer" if t >= T["step"] else "look", xs=(-22, 2, 26), y=CREST - 8, face=1, h=56)
        elif ph == "cta":
            bx, by = 420, -92                                                         # the big switch
            box(c, bx - 30, by - 50, 60, 100, "#1F2937", r=8)
            c.drawCircle(bx, by + 24, 9, P("#94A3B8"))
            ang = lerp(-40, -34, 0.5 + 0.5 * math.sin(t * 4))
            c.save()
            c.translate(bx, by + 24)
            c.rotate(ang)
            c.drawRRect(rr(-5, -62, 10, 62, 5), P("#E5E9F2"))
            c.drawCircle(0, -66, 12, P("#EF4444"))
            c.restore()
            engineer(c, 478, 0, 112, SHIRTS[0], t, "point", face=-1)
        elif ph == "stat":
            self.crew(c, t, "cheer", xs=(-22, 2, 26), y=CREST - 8, face=1, h=56)
            if t >= T["cong2"]:
                hats_in_the_air(c, (-22, 2, 26), CREST - 90, t, T["cong2"], height=170)

    # ------------------------------------------------------------------ set: from above
    def draw_plan(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), P("#0B1024"))
        c.drawRect(R(0, 330, W, 470), lin_paint(0, 330, 0, 800, ["#1D4ED8", "#2563EB"]))               # the lake
        for i in range(7):
            yy = 380 + i * 56
            p = skia.Path()
            p.moveTo(0, yy)
            for x in range(0, W + 1, 40):
                p.lineTo(x, yy + math.sin(x * 0.02 + t * 1.6 + i) * 5)
            c.drawPath(p, P("#BFDBFE", 0.25, stroke=3))
        c.drawRect(R(0, 780, W, 460), P("#0E1530"))                                   # the gorge downstream
        c.drawLine(540, 850, 540, 1230, P("#2563EB", 0.6, stroke=46))
        for sd in (-1, 1):                                                           # canyon walls
            p = skia.Path()
            x0 = 0 if sd < 0 else W
            p.moveTo(x0, 330)
            rng = random.Random(3 + sd)
            for yy in range(330, 1241, 70):
                p.lineTo(540 + sd * (270 + rng.uniform(-20, 26) - (40 if 640 < yy < 860 else 0)), yy)
            p.lineTo(x0, 1240)
            p.close()
            glow = prog(t, T["canyon"] - 0.2, T["walls"] + 0.2)
            c.drawPath(p, lin_paint(x0, 0, 540 + sd * 250, 0, ["#2B3352", "#4B5578"]))
            if glow > 0:
                add_glow(c, 540 + sd * 250, 800, 170, HILITE, 0.7 * glow * (0.7 + 0.3 * math.sin(t * 8)))
        ak = prog(t, T["plancut"] + 0.25, T["arch"] + 0.1)                             # the dam: an arch, bulging toward the lake
        sq = 8 * math.sin(t * 9) * prog(t, T["squeezes"] - 0.2, T["squeezes"] + 0.3) * (1 - prog(t, T["walls"], T["walls"] + 0.6))
        pts = []
        for i in range(31):
            u = i / 30
            x = lerp(292, 788, u)
            y = 812 - 150 * math.sin(math.pi * u) + sq * math.sin(math.pi * u)
            pts.append((x, y))
        n = max(2, int(31 * ak))
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:n]:
            p.lineTo(*q)
        pr = P("#C9CFDC", 1, stroke=46)
        pr.setStrokeCap(skia.Paint.kButt_Cap)
        c.drawPath(p, pr)
        c.drawPath(p, P("#FFFFFF", 0.4, stroke=4))
        pk = prog(t, T["squeezes"] - 0.7, T["squeezes"])                              # the lake pushes...
        for i in range(7):
            u = (i + 0.5) / 7
            x = lerp(320, 760, u)
            y1 = 780 - 150 * math.sin(math.pi * u) - 34
            ln = 110 * pk
            if pk > 0:
                c.drawLine(x, y1 - ln, x, y1, P("#BFDBFE", 1, stroke=8))
                for dx in (-12, 12):
                    c.drawLine(x, y1, x + dx, y1 - 18, P("#BFDBFE", pk, stroke=8))
        tk = prog(t, T["squeezes"], T["canyon"])                                      # ...and the arch passes it to the walls
        if tk > 0:
            for sd in (-1, 1):
                m = int(15 * tk)
                for i in range(2, m, 3):
                    j = 15 + sd * i
                    j2 = 15 + sd * (i + 1)
                    if 0 <= j2 <= 30:
                        (xa, ya), (xb, yb) = pts[j], pts[j2]
                        c.drawLine(xa, ya, xb, yb, P(HILITE, 1, stroke=10))
                        an = math.atan2(yb - ya, xb - xa)
                        for da in (2.5, -2.5):
                            c.drawLine(xb, yb, xb + math.cos(an + da) * 18, yb + math.sin(an + da) * 18, P(HILITE, 1, stroke=8))
        self.ui["cam"] = (0, 0, 1)

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (60, -187, 1.5)), x, y)

    def ui_river(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        ph = self.phase(tw)
        if ph == "pile":
            x0, y0 = self.at(10, -140)
            self.label(x0, y0, x0 + 150, y0 - 250, "pile", T["rocks"] + 0.1, s("break1") - 0.3, HILITE)
        elif ph == "flood":
            self.chip(540, 420, "push", T["pushes"] - 0.3, T["wash"] - 0.1, accent=WATERC, size=40)
            self.badge("alert", T["wash"], s("fix1") - 0.2, x=880, y=560)
            self.red(T["wash"], 1.8)
        elif ph == "concrete":
            x0, y0 = self.at(120, -70)
            self.label(x0, y0, x0 + 150, y0 - 330, "thick", T["thickest"], T["plancut"] - 0.05, HILITE)
        elif ph == "lazy":
            x0, y0 = self.at(-230, self.ui.get("lake", FULL) - 60)
            self.label(x0, y0, x0 + 190, y0 - 190, "lazy", T["nothing"] - 0.1, s("fix2") - 0.3, WARN)
            self.badge("alert", T["nothing"], s("fix2") - 0.2, x=880, y=420)
            self.red(T["nothing"], 1.8)
        elif ph == "power":
            x0, y0 = self.at(140, -190)
            self.label(x0, y0, x0 + 170, y0 - 190, "pen", T["pipes"] + 0.2, T["falling"] - 0.1, "#94A3B8")
            x1, y1 = self.at(332, -54)
            self.label(x1, y1, x1 - 190, y1 + 0 - 330, "turb", T["turbines"] - 0.1, T["generators"] - 0.2, "#7DD3FC")
            x2, y2 = self.at(332, -138)
            self.label(x2, y2, x2 - 60, y2 - 250, "gen", T["generators"], s("break3") - 0.3, "#FDE047")
            self.badge("check", T["electricity"], s("break3") - 0.15, x=880, y=420)
        elif ph == "storm":
            self.chip(540, 420, "storm", T["brim"] - 0.2, s("fix3") - 0.25, accent=WARN, size=44)
            self.badge("alert", T["over"], s("fix3") - 0.2, x=880, y=560)
            self.red(T["over"], 2.0)
        elif ph == "spill":
            x0, y0 = self.at(-150, -500)
            self.label(x0, y0, x0 + 60, y0 - 170, "gates", T["open"] + 0.1, T["out"] - 0.5, "#E5E9F2")
            x1, y1 = self.at(330, -250)
            self.label(x1, y1, x1 + 110, y1 - 250, "spill", T["out"] - 0.1, T["niagara"] - 0.3, "#60A5FA")
            self.chip(540, 420, "niagara", T["niagara"] - 0.2, s("break4") - 0.25, accent=HILITE, size=44)
            self.badge("check", T["twice"], s("break4") - 0.15, x=880, y=560)
        elif ph == "fish":
            x0, y0 = self.at(560, -50)
            self.label(x0, y0, x0 - 40, y0 - 300, "salmon", T["salmon"], T["bonk"] - 0.1, "#FB7185")
            self.badge("alert", T["bonk"], s("fix4") - 0.2, x=880, y=420)
            self.red(T["bonk"], 1.8)
        elif ph == "ladder":
            x0, y0 = self.at(300, -280)
            self.label(x0, y0, x0 + 190, y0 - 190, "ladder", T["built"] + 0.4, s("cta") - 0.3, HILITE)
            self.badge("check", T["step"], s("cta") - 0.15, x=880, y=420)
        elif ph == "cta":
            x0, y0 = self.at(420, -150)
            self.label(x0, y0, x0 - 170, y0 - 250, "switch", T["flip"] - 0.2, s("reveal") - 0.3, WARN)
        elif ph == "reveal":
            x0, y0 = self.at(910, CREST - 150)
            self.label(x0, y0, x0 - 190, y0 - 110, "shop", T["gift"] + 0.05, T["s1"] - 0.5, "#F43F5E")
        elif ph == "tag":
            x0, y0 = self.at(700, CREST - 30)
            self.label(x0, y0, x0 - 190, y0 - 110, "lift", T["elevator"] - 0.1, self.duration + 1, HILITE)

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.label(540, 640, 760, 480, "arch", T["arch"] - 0.1, T["canyon"] - 0.3, "#E5E9F2")
        self.label(250, 900, 250, 1100, "walls", T["canyon"] - 0.1, s("break2") - 0.3, HILITE)
        self.badge("check", T["walls"], s("break2") - 0.15, x=880, y=1120)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, roar(1.6, 6, 300, 2400), -16)]
        ev += [(0.4 + i * (T["rocks"] - 0.5) / 9, sfx.thud(0.2, 61 + i), -6 - (i % 3)) for i in range(9)]
        ev += [(T["congrats"] + 0.1, sfx.chime(), -8)]
        ev += [(T["lake"], sfx.riser(max(0.8, T["harder"] - T["lake"]), 70), -13), (T["pushes"] - 0.3, sfx.pop(71), -8), (T["harder"], sfx.creak(0.8, 72), -7),
               (T["wash"], rumble(1.2, 73), -3), (T["wash"] + 0.05, roar(1.6, 7), -5), (T["wash"] + 0.1, sfx.alarm(3, 820), -11),
               (T["downstream"] + 0.3, sfx.womp(), -9)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["concrete"] - 0.3, rumble(0.8, 75), -8), (T["concrete"] + 0.5, sfx.thud(0.5, 76), -3),
               (T["thickest"] - 0.3, sfx.pop(77), -8), (T["plancut"], sfx.whoosh(0.4, True, 78), -5), (T["plancut"] + 0.25, sfx.whoosh(0.6, True, 79), -10),
               (T["squeezes"] - 0.7, sfx.riser(0.7, 80), -13), (T["squeezes"], sfx.creak(0.7, 81), -8), (T["canyon"] - 0.2, sfx.thud(0.3, 82), -6),
               (T["walls"], sfx.chime(), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 83), -5), (T["holds"], sfx.thud(0.3, 84), -8), (T["nothing"], sfx.alarm(3, 820), -12),
               (T["teenager"] - 0.2, plop(1), -8), (T["teenager"] + 0.5, sfx.womp(), -9)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 85), -4), (T["pipes"] - 0.3, sfx.whoosh(0.7, True, 86), -9), (T["wall"] + 0.2, sfx.clank(400, 0.3, 87), -7),
               (T["falling"] - 0.3, roar(1.4, 8, 200, 1800), -11), (T["spins"] - 0.5, sfx.thunk(88), -5), (T["spins"], sfx.whirr(1.4, 120, 320, 89), -9),
               (T["generators"] - 0.3, sfx.pop(90), -6), (T["generators"], gen_hum(1.4), -9), (T["electricity"] - 0.3, sfx.charge_up(0.5), -8),
               (T["electricity"], sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 91), -5), (T["storm"] - 0.4, rain_snd(max(2.5, s("fix3") - T["storm"] + 1.5)), -10),
               (T["storm"], thunder(1.6, 4), -3), (T["brim"] + 0.1, thunder(1.2, 5), -6), (T["over"], roar(2.0, 9), -5), (T["over"] + 0.1, sfx.alarm(3, 820), -11),
               (T["over"] + 0.6, sfx.sizzle(0.6, 92), -8), (T["waterfall"] + 0.3, sfx.womp(), -9)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 93), -4), (T["spillways"] - 0.2, rumble(0.8, 94), -9), (T["open"], sfx.creak(0.6, 95), -6),
               (T["open"] + 0.1, sfx.clank(300, 0.4, 96), -5), (T["open"] + 0.3, roar(max(1.5, T["twice"] - T["open"] + 0.8), 10), -7),
               (T["niagara"] - 0.2, sfx.pop(97), -6), (T["twice"], sfx.pop(98), -5), (T["twice"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 99), -5), (T["salmon"] - 0.4, plop(0), -8), (T["salmon"], plop(2), -9), (T["eggs"], plop(3), -10),
               (T["bonk"], sfx.thud(0.2, 100), -3), (T["bonk"] + 0.12, sfx.thud(0.2, 101), -5), (T["bonk"] + 0.24, sfx.thud(0.2, 102), -6),
               (T["bonk"] + 0.1, sfx.alarm(3, 820), -11)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 103), -4)]
        ev += [(T["built"] + i * 0.085, sfx.tick(), -8) for i in range(10)]
        ev += [(T["hop"] + i * 0.34, plop(i % 5), -6) for i in range(int(max(3, min(12, (s("cta") - T["hop"]) / 0.34))))]
        ev += [(T["step"], sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(104), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 105), -7), (T["follow"] - 0.15, sfx.pop(106), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 107), -6), (T["power"] - 0.2, sfx.pop(108), -6), (T["power"] + 0.05, sfx.pop(109), -7),
               (T["power"] + 0.3, sfx.pop(110), -7), (T["power"] + 0.7, sfx.sizzle(0.5, 111), -11), (T["road"] - 0.2, sfx.whoosh(0.5, True, 112), -10),
               (T["road"] + 0.5, sfx.beep(520, 0.12), -13), (T["gift"] - 0.25, sfx.pop(113), -5), (T["gift"], sfx.ding(), -7)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 114), -6), (T["s1"], sfx.pop(115), -3), (T["s2"], sfx.pop(116), -3), (T["s3"], sfx.pop(117), -3)]
        ev += [(T["cong2"], sfx.pop(118), -2), (T["cong2"], sfx.sparkle(1.0, 14, 119), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 120), -6), (T["some"] - 0.2, sfx.thunk(121), -6), (T["elevator"] - 0.3, sfx.whirr(1.6, 140, 200, 122), -10),
               (T["real"], sfx.ding(), -5), (T["checked"] + 0.35, sfx.womp(), -3)]
        return ev


NAME = "dam"
EPISODE = Dam
