"""Episode 7 - A castle.  v2 look: one world drawn as a side section at night, five cameras ("sets") with whip cuts.

World (x to the right, ground at y = 0): attackers' field (x < -700), the moat (-700..-460), the gatehouse wall in
section (-460..-300) with its passage, guard room, murder holes, two portcullises and the drawbridge, the courtyard
(-300..250) with the well and the cellar under it, the mound with the keep (250..650), the far wall with the sally
port (700..860).  Round towers stand behind the courtyard.
"""
from v2_base import *  # noqa: F401,F403

STONE, WOOD, TEAM = "#8C92AA", "#8B5E3C", "#9F1239"       # masonry, timber, the neighbours' shirts
WX0, WX1, WTOP, PASS = -460, -300, -380, -150             # gate wall: outer face, inner face, top, passage ceiling
MX0 = -700                                                # outer bank of the moat


# ====================================================================================== pieces
def stone(c, x, y, w, h, base=STONE, seed=1, a=1.0):
    """Masonry: shaded face plus courses of blocks."""
    if w <= 1 or h <= 1:
        return
    vrect(c, x, y, w, h, [shade(base, 0.12), base, shade(base, -0.32)], [0.0, 0.35, 1.0], a=a)
    rng = random.Random(seed)
    yy, row = y + 4, 0
    while yy < y + h - 8:
        xx = x + (0 if row % 2 else -26) + rng.uniform(-6, 6)
        while xx < x + w:
            bw = rng.uniform(46, 74)
            x0, x1 = max(x + 2, xx), min(x + w - 2, xx + bw - 4)
            if x1 - x0 > 8:
                c.drawRRect(rr(x0, yy, x1 - x0, 24, 4), P("#000000" if rng.random() < 0.55 else "#FFFFFF", 0.09 * a))
            xx += bw
        yy += 29
        row += 1


def tower(c, x, base, w, h, k=1.0, seed=1, far=0.0, teeth=1.0, lit=0.0):
    """Round tower seen from the front, centre x, standing on base. k: how far it has risen, far: 0 near .. 1 distant."""
    hh = h * e_out(clamp(k))
    if hh <= 2:
        return
    x0, y0 = x - w / 2, base - hh
    stone(c, x0, y0, w, hh, mix(STONE, "#30365E", far * 0.7), seed)
    c.drawRect(R(x0, y0, w, hh), lin_paint(x0, 0, x0 + w, 0, [("#FFFFFF", 0.16), ("#000000", 0.0), ("#000000", 0.52)], [0.0, 0.3, 1.0]))
    c.drawRect(R(x0 + w - 4, y0, 3, hh), P("#BFD8FF", 0.30 * (1 - far * 0.5)))
    if k < 1:
        return
    box(c, x0 - 9, y0 - 14, w + 18, 18, mix(shade(STONE, -0.12), "#30365E", far * 0.7), r=3)
    n = max(3, int((w + 18) // 34))
    for i in range(n):
        p = clamp(teeth * n - i)
        if p > 0:
            mw = (w + 18) / n * 0.58
            box(c, x0 - 9 + i * (w + 18) / n + 2, y0 - 14 - 30 * e_back(p), mw, 30 * e_back(p) + 2, mix(STONE, "#30365E", far * 0.7), r=3)
    for fy in (0.22, 0.52):
        c.drawRRect(rr(x - 6, y0 + hh * fy, 12, 38, 6), P(mix("#10142A", "#FFC766", lit)))
        if lit > 0:
            add_glow(c, x, y0 + hh * fy + 19, 46, "#FFC766", 0.5 * lit)


def torch(c, x, y, t, k=1.0, s=1.0, seed=0):
    """Burning torch: the flame sits at (x, y)."""
    c.drawLine(x, y + 34 * s, x, y, P("#5B3A22", 1, stroke=6 * s))
    if k > 0:
        v2.flame(c, x, y, 13 * s, 62 * s, t, k, seed=seed, ang=270)
        add_glow(c, x, y - 12 * s, 90 * s, "#FF9A4D", 0.55 * k)


def ladder(c, x0, y0, x1, y1, a=1.0):
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln * 13, dx / ln * 13
    for sgn in (-1, 1):
        c.drawLine(x0 + nx * sgn, y0 + ny * sgn, x1 + nx * sgn, y1 + ny * sgn, P("#A9744A", a, stroke=6))
    for i in range(1, int(ln // 30)):
        u = i * 30 / ln
        c.drawLine(x0 + dx * u - nx, y0 + dy * u - ny, x0 + dx * u + nx, y0 + dy * u + ny, P("#C89466", a, stroke=5))


def banner(c, x, y, h, t, k=1.0, col="#F59E0B", w=46):
    """Cloth banner hanging from (x, y), unrolled by k."""
    if k <= 0:
        return
    hh = h * e_out(clamp(k))
    path = skia.Path()
    path.moveTo(x, y)
    path.lineTo(x + w, y)
    for i in range(9):
        u = i / 8
        path.lineTo(x + w + math.sin(t * 3 + u * 5 + x) * 5 * u, y + hh * u)
    path.lineTo(x + w / 2, y + hh - 16)
    for i in range(9):
        u = 1 - i / 8
        path.lineTo(x + math.sin(t * 3 + u * 5 + x) * 5 * u, y + hh * u)
    path.close()
    c.drawPath(path, lin_paint(x, 0, x + w, 0, [shade(col, 0.2), col, shade(col, -0.3)]))
    c.drawRect(R(x - 6, y - 6, w + 12, 7), P("#3A2A1A"))


def tent(c, x, s=1.0, col="#7C2D12"):
    path = skia.Path()
    path.moveTo(x - 80 * s, 0)
    path.lineTo(x, -112 * s)
    path.lineTo(x + 80 * s, 0)
    path.close()
    c.drawPath(path, lin_paint(x - 80 * s, 0, x + 80 * s, 0, [shade(col, 0.25), col, shade(col, -0.4)]))
    door = skia.Path()
    door.moveTo(x - 16 * s, 0)
    door.lineTo(x, -58 * s)
    door.lineTo(x + 16 * s, 0)
    door.close()
    c.drawPath(door, P("#150B08"))


def rock(c, x, y, r, rot=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    path = skia.Path()
    for i, (a_, k) in enumerate(((0, 1.0), (55, 0.86), (110, 1.0), (170, 0.8), (230, 0.96), (300, 0.84))):
        px, py = math.cos(math.radians(a_)) * r * k, math.sin(math.radians(a_)) * r * k
        path.moveTo(px, py) if i == 0 else path.lineTo(px, py)
    path.close()
    c.drawPath(path, rad_paint(-r * 0.3, -r * 0.4, r * 1.6, ["#C9CEDD", "#7E8498", "#3D4258"]))
    c.restore()


def water_snd(d=0.5, seed=60):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 500, 5000)
    return sfx._norm(x * sfx._env(n, 0.004, d * 0.28), 0.8)


def fanfare():
    out = np.zeros(int(1.5 * sfx.SR))
    for f, t0, d in ((392, 0.0, 0.22), (523, 0.24, 0.22), (659, 0.48, 0.22), (784, 0.74, 0.7)):
        n = int(d * sfx.SR)
        tt = np.arange(n) / sfx.SR
        tone = sum(np.sin(2 * np.pi * f * h * tt) / h for h in (1, 2, 3, 4, 5)) * sfx._ar(n, 0.02, d * 0.35)
        i = int(t0 * sfx.SR)
        out[i:i + n] += tone
    return sfx._norm(sfx._lp(out, 3200), 0.7)


# ====================================================================================== the episode
class Castle(EpisodeV2):
    BUILD_NO = 7
    FIRST_SET = "motte"
    TITLE = {"en": "CASTLE", "ar_sa": "قلعة"}
    EMPH = {"en": ["CONGRATS", "CASTLE", "FIREWOOD", "STONE", "THICKER", "ROUND", "LADDERS", "MOAT", "BATTLEMENTS", "RAM",
                   "DRAWBRIDGE", "PORTCULLIS", "MURDER", "EXPENSIVE", "STARVE", "WELL", "SALLY", "FOLLOW", "CLAW", "FOUR",
                   "YOURSELF", "TOILET"],
            "ar_sa": ["مبروك", "قلعة", "حطب", "بالحجر", "سماكته", "مدورة", "سلالم", "خندق", "أسنان", "بجذع", "جسر", "وبوابة",
                      "السكين", "غالي", "تجوع", "بير", "سري", "تابعني", "أربع", "بيدك", "والحمام", "الخندق"]}
    KEYS = {"ar_sa": {
        ("hook", "PILE"): "كومت", ("hook", "HOUSE"): "بيتك", ("hook", "CONGRATS"): "مبروك", ("hook", "CASTLE"): "قلعة",
        ("break1", "NEIGHBORS"): "الجيران", ("break1", "TORCHES"): "مشاعل", ("break1", "FIREWOOD"): "حطب",
        ("fix1", "STONE"): "بالحجر", ("fix1", "WALL"): "سور", ("fix1", "TALL"): "طولك", ("fix1", "TOWERS"): "وأبراج",
        ("fix1", "BOULDERS"): "الصخر", ("fix1", "GLANCE"): "ويزلق",
        ("break2", "LADDERS"): "سلالم", ("break2", "CLIMB"): "ويطلعون", ("break2", "OVER"): "السور",
        ("fix2", "MOAT"): "خندق", ("fix2", "AROUND"): "حولها", ("fix2", "BATTLEMENTS"): "أسنان", ("fix2", "HIDE"): "تتخبى",
        ("fix2", "SHOOT"): "وترمي",
        ("break3", "DOOR"): "الباب", ("break3", "KNOCK"): "ويدقونه", ("break3", "RAM"): "بجذع",
        ("fix3", "DRAWBRIDGE"): "جسر", ("fix3", "PORTCULLIS"): "وبوابة", ("fix3", "DROPS"): "تطيح", ("fix3", "MURDER"): "وفتحات",
        ("fix3", "ROCKS"): "حجارة", ("fix3", "BOILING"): "زيت", ("fix3", "EXPENSIVE"): "غالي",
        ("break4", "NOBODY"): "محد", ("break4", "LUNCH"): "الغدا", ("break4", "CAMP"): "يخيمون", ("break4", "STARVE"): "تجوع",
        ("fix4", "WELL"): "بير", ("fix4", "STOCK"): "وتعبي", ("fix4", "MONTHS"): "شهور", ("fix4", "SALLY"): "باب",
        ("fix4", "MIDNIGHT"): "نص", ("fix4", "RAIDS"): "الليل",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "BANNERS"): "الرايات", ("reveal", "LIGHT"): "وولع", ("reveal", "TRUMPET"): "بوق",
        ("stat", "ONE"): "تلة", ("stat", "FOUR"): "أربع", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TOILET"): "والحمام", ("tag", "HOLE"): "فتحة", ("tag", "MOAT"): "الخندق", ("tag", "SWIMS"): "يسبح"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a claw machine"),
                   "stat": [("1", "HILL"), ("4", "TOWERS"), ("0", "VISITORS")],
                   "L": {"house": "YOUR HOUSE", "wall": "CURTAIN WALL", "thick": "THICKER THAN YOU", "towers": "ROUND TOWERS",
                         "moat": "MOAT", "teeth": "BATTLEMENTS", "ram": "BATTERING RAM", "bridge": "DRAWBRIDGE",
                         "port": "PORTCULLIS", "holes": "MURDER HOLES", "oil": "TOO EXPENSIVE", "food": "FOOD", "well": "WELL",
                         "cellar": "CELLAR", "sally": "SALLY PORT", "toilet": "THE TOILET", "lunch": "LUNCH"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مكينة سحب الألعاب"),
                      "stat": [("1", "تلة"), ("4", "أبراج"), ("0", "زوار")],
                      "L": {"house": "بيتك", "wall": "السور", "thick": "أسمك من طولك", "towers": "أبراج مدورة", "moat": "خندق",
                            "teeth": "أسنان حجر", "ram": "جذع شجرة", "bridge": "جسر ينرفع", "port": "بوابة حديد",
                            "holes": "فتحات السقف", "oil": "غالي مرة", "food": "الأكل", "well": "بير", "cellar": "المخزن",
                            "sally": "باب سري", "toilet": "الحمام", "lunch": "الغدا"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "pile": ("hook", "PILE", 0.1), "house": ("hook", "HOUSE", 0.5), "congrats": ("hook", "CONGRATS", 0.65),
            "neighbors": ("break1", "NEIGHBORS", 0.15), "torches": ("break1", "TORCHES", 0.4), "firewood": ("break1", "FIREWOOD", 0.9),
            "stone": ("fix1", "STONE", 0.2), "wall": ("fix1", "WALL", 0.35), "tall": ("fix1", "TALL", 0.55),
            "towers": ("fix1", "TOWERS", 0.72), "boulders": ("fix1", "BOULDERS", 0.84), "glance": ("fix1", "GLANCE", 0.92),
            "ladders": ("break2", "LADDERS", 0.55), "climb": ("break2", "CLIMB", 0.8), "over": ("break2", "OVER", 0.9),
            "moat": ("fix2", "MOAT", 0.15), "around": ("fix2", "AROUND", 0.22), "battlements": ("fix2", "BATTLEMENTS", 0.36),
            "hide": ("fix2", "HIDE", 0.66), "shoot": ("fix2", "SHOOT", 0.9),
            "door": ("break3", "DOOR", 0.22), "knock": ("break3", "KNOCK", 0.66), "ram": ("break3", "RAM", 0.92),
            "drawbridge": ("fix3", "DRAWBRIDGE", 0.11), "portcullis": ("fix3", "PORTCULLIS", 0.2), "drops": ("fix3", "DROPS", 0.3),
            "murder": ("fix3", "MURDER", 0.48), "rocks": ("fix3", "ROCKS", 0.73), "boiling": ("fix3", "BOILING", 0.78),
            "expensive": ("fix3", "EXPENSIVE", 0.93),
            "nobody": ("break4", "NOBODY", 0.07), "lunch": ("break4", "LUNCH", 0.47), "camp": ("break4", "CAMP", 0.58),
            "starve": ("break4", "STARVE", 0.93),
            "well": ("fix4", "WELL", 0.15), "stock": ("fix4", "STOCK", 0.32), "months": ("fix4", "MONTHS", 0.5),
            "sally": ("fix4", "SALLY", 0.64), "midnight": ("fix4", "MIDNIGHT", 0.9), "raids": ("fix4", "RAIDS", 0.95),
            "follow": ("cta", "FOLLOW", 0.42),
            "banners": ("reveal", "BANNERS", 0.26), "light": ("reveal", "LIGHT", 0.4), "trumpet": ("reveal", "TRUMPET", 0.9),
            "s1": ("stat", "ONE", 0.04), "s2": ("stat", "FOUR", 0.33), "s3": ("stat", "ZERO", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "toilet": ("tag", "TOILET", 0.1), "hole": ("tag", "HOLE", 0.25), "moat2": ("tag", "MOAT", 0.6), "swims": ("tag", "SWIMS", 0.84)})
        T["fire"] = T["torches"] + 0.35
        T["hit"] = T["boulders"] + 0.30                       # the boulder meets the keep
        T["fallin"] = T["moat"] + 0.55                        # the ladder drops into the new moat
        T["crack"] = T["knock"] + 0.75                        # third knock: the door gives way
        T["slide"] = T["drawbridge"] + 0.45                   # the ram team slides off the rising bridge
        T["clang"] = T["drops"] + 0.16
        T["plop"] = T["moat2"] - 0.25
        # one world, five cameras
        self.cut(s("fix1") - 0.12, "wallcam", 1)
        self.cut(T["towers"] - 0.45, "keepcam", -1)
        self.cut(s("break2") - 0.1, "wallcam", 1)
        self.cut(s("break3") - 0.1, "gate", -1)
        self.cut(s("break4") - 0.12, "siege", 1)
        self.cut(s("fix4") - 0.12, "yard", -1)
        self.cut(T["midnight"] - 0.05, "siege", 1)
        self.cut(s("reveal") - 0.12, "keepcam", -1)
        # ground line near screen y 1230 means camera y = -270 / zoom
        self.cams = {"motte": Camera(520, -186, 1.45), "wallcam": Camera(-420, -180, 1.5), "keepcam": Camera(420, -380, 1.1),
                     "gate": Camera(-600, -150, 1.42), "siege": Camera(-760, -230, 1.18), "yard": Camera(-110, 70, 1.7)}
        cm = self.cams
        cm["motte"].key(0.05, 500, -175, 1.55, 1.4).key(s("break1") - 0.1, 330, -257, 1.05, 0.9)
        cm["wallcam"].key(s("fix1"), -420, -180, 1.5, 0.0).key(T["tall"] - 0.3, -400, -190, 1.6, 0.9)
        cm["wallcam"].key(s("break2") - 0.1, -540, -186, 1.45, 0.0).key(T["battlements"] - 0.2, -470, -300, 1.5, 0.9)
        cm["keepcam"].key(T["towers"] - 0.45, 400, -360, 1.02, 0.0).key(T["boulders"], 420, -380, 1.1, 0.8)
        cm["keepcam"].key(s("reveal") - 0.12, 420, -400, 1.05, 0.0).key(T["trumpet"] - 0.6, 470, -620, 1.5, 0.8)
        cm["keepcam"].key(T["s1"] - 0.3, 200, -337, 0.8, 0.9).key(s("closer"), 200, -320, 0.84, 2.0)
        cm["keepcam"].key(s("tag") - 0.2, -545, -150, 1.75, 0.32)
        cm["gate"].key(s("break3"), -600, -150, 1.42, 0.0).key(T["drawbridge"] - 0.2, -530, -150, 1.5, 0.6)
        cm["gate"].key(T["murder"] - 0.25, -372, -130, 2.0, 0.6)
        cm["siege"].key(s("break4"), -760, -230, 1.18, 0.0).key(T["lunch"] - 0.3, -700, -196, 1.36, 0.9)
        cm["siege"].key(T["midnight"] - 0.05, -960, -190, 1.42, 0.0)
        cm["yard"].key(s("fix4"), -110, 70, 1.7, 0.0).key(T["sally"] - 0.2, 700, -70, 1.6, 0.45)
        self.spans = [(T["fire"], T["hit"] + 0.4), (T["climb"], T["shoot"] + 0.4), (T["crack"], T["rocks"] + 0.4),
                      (T["starve"] - 0.5, T["raids"] + 0.3)]
        self.shakes = [(T["hit"], 0.5, 14), (T["knock"], 0.25, 10), (T["knock"] + 0.38, 0.25, 12), (T["crack"], 0.5, 22),
                       (T["clang"], 0.45, 26), (T["fallin"], 0.3, 8)]
        self.bridge = Track(0.0).to(T["drawbridge"], 82.0, 0.7, e_io)
        self.night = Track(0.0).to(s("break4") - 0.1, 1.0, 0.01).to(s("reveal") - 0.1, 0.35, 0.01)

    # ------------------------------------------------------------------ the world
    def world(self, c, t, cam):
        T, s = self.T, self.tl.s
        cx, cy, z = cam
        cx += math.sin(t * 0.6) * 4
        gy = (0 - cy) * z + H / 2
        night = self.night.at(t)
        stone_on = t >= T["stone"]
        self.backdrop(c, t, cx, cy, gy)
        if night > 0:
            c.drawRect(R(0, 0, W, H), P("#050818", 0.26 * night))
        self.view(c, (cx, cy, z))
        v2.ground(c, -3400, 3400)
        k_wall = prog(t, T["wall"] - 0.15, T["wall"] + 0.45)
        k_tow = prog(t, T["towers"] - 0.35, T["towers"] + 0.3)
        teeth = prog(t, T["battlements"], T["battlements"] + 0.9)
        lit = prog(t, T["light"], T["light"] + 0.8)
        # far wall and the round towers behind the courtyard
        if stone_on:
            stone(c, -300, -300 * e_out(k_wall), 1000, 300 * e_out(k_wall), "#4A4F74", 5)
            c.drawRect(R(-300, -300 * e_out(k_wall), 1000, 300 * e_out(k_wall)), P("#0A0E22", 0.35))
            for i, (tx, tw_, th) in enumerate(((-170, 130, 500), (90, 120, 450), (780, 130, 560))):
                tower(c, tx, 0, tw_, th, k_tow, seed=10 + i, far=0.55, teeth=teeth, lit=max(lit, 0.25))
        # the mound: wooden house first, the stone keep later
        hk = e_back(prog(t, 0.08, 1.0), 1.2)                         # the hill piles up in the first second
        mound = skia.Path()
        mound.moveTo(230, 2)
        mound.cubicTo(290, 2, 300, -150 * hk, 350, -150 * hk)
        mound.lineTo(550, -150 * hk)
        mound.cubicTo(600, -150 * hk, 610, 2, 670, 2)
        mound.close()
        c.drawPath(mound, lin_paint(0, -150, 0, 0, ["#3F7A4E", "#2A5540", "#1A3830"]))
        c.drawPath(mound, lin_paint(230, 0, 670, 0, [("#FFFFFF", 0.10), ("#000000", 0.0), ("#000000", 0.35)]))
        rng = random.Random(3)
        for _ in range(14):
            gx = rng.uniform(340, 560)
            c.drawLine(gx, -150 * hk, gx + rng.uniform(-5, 5), -150 * hk - rng.uniform(6, 14), P("#5FA86A", 0.8, stroke=3))
        if not stone_on:
            hp = e_back(prog(t, T["house"], T["house"] + 0.35))
            burn = clamp((t - T["fire"]) * 1.4)
            if hp > 0:
                c.save()
                c.translate(450, -150)
                c.scale(hp, hp)
                for px in range(-150, 151, 30):                                  # palisade
                    box(c, px - 12, -70, 24, 70, mix(WOOD, "#1B1210", burn * 0.8), r=4)
                    c.drawPath(_tri(px, -70, 12, 18), P(mix(shade(WOOD, 0.1), "#1B1210", burn * 0.8)))
                box(c, -70, -150, 140, 150, mix("#A9744A", "#1B1210", burn * 0.75), r=4)       # the house
                for hy in (-120, -90, -60, -30):
                    c.drawRect(R(-70, hy, 140, 3), P("#000000", 0.18))
                c.drawPath(_tri(0, -150, 92, 78), lin_paint(-92, 0, 92, 0, ["#B45309", "#92400E", "#5B2A0B"]))
                c.drawRRect(rr(-18, -62, 36, 62, 6), P("#3A2414"))
                c.drawRRect(rr(26, -112, 30, 30, 4), P(mix("#FFD98A", "#FF7A2F", burn)))
                add_glow(c, 41, -97, 50, "#FFC766", 0.45)
                c.restore()
            if t >= T["fire"]:
                for i, fx_ in enumerate((-120, -40, 30, 110)):
                    v2.flame(c, 450 + fx_, -190 - (40 if abs(fx_) < 60 else 0), 44, 250, t, burn * (0.75 + 0.25 * math.sin(t * 7 + i)), seed=i, ang=270)
                add_glow(c, 450, -230, 620, "#FF8A3D", 0.5 * burn)
                v2.smoke(c, 450, -330, t, T["fire"] + 0.2, T["stone"], rate=14, life=2.6, spread=(60, -150), rise=-90, size=(40, 150),
                         col="#5E6478", lit="#FF7A2F", lit_until=0.7, seed=4)
                v2.embers(c, 450, -260, t, T["fire"] + 0.05, 1.4, n=40, speed=700, seed=2, cone=(210, 330))
        else:
            kk = prog(t, T["stone"], T["stone"] + 0.6)
            tower(c, 450, -150, 170, 550, kk, seed=21, teeth=teeth, lit=max(lit, 0.3))
            if kk >= 1:
                c.drawRRect(rr(432, -212, 36, 62, 16), P("#2A1A10"))
            if t < T["stone"] + 1.2:
                v2.smoke(c, 450, -200, t, T["stone"] - 0.1, T["stone"] + 0.2, rate=40, life=1.1, spread=(240, -60), rise=-60,
                         size=(30, 120), col="#C9CEDD", lit=None, lit_until=0, seed=8, a=0.7)
        # far wall with the sally port
        if stone_on:
            stone(c, 700, WTOP * e_out(k_wall), 160, -WTOP * e_out(k_wall), STONE, 31)
            sp = prog(t, T["sally"], T["sally"] + 0.3)
            if k_wall >= 1:
                c.drawRRect(rr(836, -92, 24, 92, 5), P("#0A0C16"))
                c.save()
                c.translate(860, 0)
                c.scale(1 - 0.85 * sp, 1)
                stone(c, -26, -94, 26, 94, shade(STONE, -0.05), 32)
                c.restore()
                if sp > 0:
                    add_glow(c, 850, -46, 70, "#FFC766", 0.4 * sp)
        # under the courtyard: the well and the cellar
        wk = e_out(prog(t, T["well"], T["well"] + 0.6))
        under = t < s("reveal") - 0.12                           # the cutaway under the yard is only shown while it matters
        if wk > 0 and not under:
            stone(c, 0, -30, 80, 30, STONE, 41)
            c.drawLine(4, -30, 4, -84, P("#5B3A22", 1, stroke=6))
            c.drawLine(76, -30, 76, -84, P("#5B3A22", 1, stroke=6))
            box(c, -6, -92, 92, 12, "#7C4A2D", r=3)
        if wk > 0 and under:
            c.drawRect(R(12, 0, 56, 250 * wk), lin_paint(12, 0, 68, 0, ["#0B0E1C", "#141A30", "#0B0E1C"]))
            if wk >= 1:
                vrect(c, 12, 196, 56, 54, ["#2B7FB8", "#0F3A63"])
                add_glow(c, 40, 200, 60, "#7DD3FC", 0.4)
                by = lerp(190, -40, e_io(prog(t, T["well"] + 0.7, T["well"] + 1.5)))
                c.drawLine(40, -70, 40, by, P("#C9B28A", 1, stroke=3))
                box(c, 26, by, 28, 26, "#8B5E3C", r=4)
                c.drawRect(R(28, by + 2, 24, 5), P("#7DD3FC"))
            stone(c, 0, -30, 80, 30, STONE, 41)
            c.drawLine(4, -30, 4, -84, P("#5B3A22", 1, stroke=6))
            c.drawLine(76, -30, 76, -84, P("#5B3A22", 1, stroke=6))
            box(c, -6, -92, 92, 12, "#7C4A2D", r=3)
        ck = prog(t, T["stock"] - 0.25, T["stock"] + 0.2)
        if ck > 0 and under:
            c.save()
            c.clipRect(R(-290, 50, 270 * e_out(ck), 190))
            vrect(c, -290, 50, 270, 190, ["#3A2E4A", "#221C30"])
            c.drawRect(R(-290, 50, 270, 6), P("#000000", 0.4))
            add_glow(c, -155, 70, 190, "#FFC766", 0.45)
            c.drawCircle(-155, 62, 7, P("#FFE9B8"))
            goods = int(clamp((t - T["stock"]) / max(0.2, T["months"] - T["stock"] + 0.3)) * 13)
            for i in range(goods):
                gx = -278 + (i % 5) * 50 + (24 if 5 <= i < 10 else 48 if i >= 10 else 0)
                gyy = 240 - (0 if i < 5 else 46 if i < 10 else 92)
                if i % 3 == 2:
                    c.drawOval(R(gx, gyy - 40, 40, 40), rad_paint(gx + 12, gyy - 30, 40, ["#E8D5A8", "#B89B62", "#6B5A36"]))
                else:
                    cyl(c, gx, gyy - 46, 40, 46, "#8B5E3C", r=8)
                    for hy in (gyy - 36, gyy - 14):
                        c.drawRect(R(gx, hy, 40, 4), P("#3A2414"))
            c.restore()
            c.drawRect(R(-290, 50, 270 * e_out(ck), 190), P("#FFFFFF", 0.25, stroke=3))
        # the moat
        mk = e_out(prog(t, T["moat"], T["moat"] + 0.5))
        if mk > 0:
            c.drawRect(R(MX0, 0, WX0 - MX0, 124 * mk), P("#0A0D1A"))
            wl = prog(t, T["moat"] + 0.35, T["moat"] + 0.95)
            if wl > 0:
                top = lerp(120, 12, e_out(wl))
                vrect(c, MX0, top, WX0 - MX0, 124 - top + 0.5, ["#2A6A96", "#143A5E", "#0B2038"], [0.0, 0.35, 1.0])
                for i in range(5):
                    wx_ = MX0 + 20 + i * 46 + math.sin(t * 1.6 + i) * 8
                    c.drawRRect(rr(wx_, top + 4 + (i % 2) * 6, 30, 3, 1.5), P("#BFE4FF", 0.5))
        # the gate wall in section
        if stone_on:
            wh = -WTOP * e_out(k_wall)
            stone(c, WX0, -wh, WX1 - WX0, wh, STONE, 2)
            if k_wall >= 1:
                c.drawRect(R(WX0, PASS, WX1 - WX0, -PASS), P("#0C0F20"))                # passage: a dark tunnel
                stone(c, WX0, PASS, WX1 - WX0, -PASS, "#2A2E4A", 6, a=0.5)
                vrect(c, WX0, PASS, WX1 - WX0, 70, [("#000000", 0.6), ("#000000", 0.0)])
                c.drawRect(R(WX0, -8, WX1 - WX0, 8), P("#565C78"))
                c.drawRect(R(WX0, PASS - 4, WX1 - WX0, 6), P("#C9CEDD", 0.55))
                c.drawRRect(rr(WX0 + 20, -262, 120, 86, 6), P("#1A1E33"))               # guard room
                add_glow(c, WX0 + 80, -246, 70, "#FFC766", 0.35)
                for hx in (-424, -384, -344):                                           # murder holes
                    c.drawRect(R(hx - 8, -178, 16, 30), P("#0A0C16"))
                box(c, WX0 - 2, WTOP - 50, 38, 52, STONE, r=3)                          # parapet
                stone(c, WX0 - 34, -330, 36, 50, shade(STONE, -0.08), 7)                # the garderobe
                c.drawRect(R(WX0 - 28, -282, 18, 6), P("#0A0C16"))
                c.drawRect(R(WX0 - 4, WTOP, 4, -WTOP - 150), P("#BFD8FF", 0.10))
                door_k = clamp((t - T["crack"]) * 4) if t >= T["crack"] else 0.0
                if door_k < 1:                                                          # the wooden door (edge on)
                    box(c, WX0 + 2, PASS + 4, 14, -PASS - 4, WOOD, r=3)
                    for i in range(int(clamp((t - T["knock"]) * 2.7 + 0.01) * 3) if t >= T["knock"] else 0):
                        c.drawLine(WX0 + 4, -110 + i * 34, WX0 + 14, -96 + i * 34, P("#1B1210", 1, stroke=3))
                else:
                    v2.debris(c, WX0 + 8, -70, t, T["crack"], 1.3, n=9, speed=420, seed=3, cols=("#A9744A", "#7C4A2D", "#5B3A22"),
                              floor=0, cone=(-40, 40), size=(8, 26))
                for px_, t0 in ((WX1 - 22, T["portcullis"] - 0.1), (WX0 + 26, T["drops"])):    # two portcullises
                    pk = e_in(prog(t, t0, t0 + 0.16))
                    py = lerp(PASS - 150, PASS, pk)
                    c.save()
                    c.clipRect(R(px_ - 12, PASS, 24, -PASS + 2))
                    c.drawRect(R(px_ - 4, py, 8, 150), lin_paint(px_ - 4, 0, px_ + 4, 0, ["#9AA3B8", "#4A5368"]))
                    for by_ in range(0, 150, 26):
                        c.drawRect(R(px_ - 9, py + by_, 18, 5), P("#2B3248"))
                    c.drawPath(_tri(px_, py + 150, 7, -14), P("#9AA3B8"))
                    c.restore()
        # the bridge: a fixed plank first, a drawbridge later
        if t >= T["around"]:
            ang = self.bridge.at(t)
            bk = e_out(prog(t, T["around"], T["around"] + 0.4))
            c.save()
            c.translate(WX0, -2)
            c.rotate(ang)
            box(c, -(WX0 - MX0 + 8) * bk, -8, (WX0 - MX0 + 8) * bk, 12, "#8B5E3C", r=3)
            for px_ in range(-230, 0, 38):
                if -px_ < (WX0 - MX0) * bk:
                    c.drawRect(R(px_, -8, 3, 12), P("#3A2414", 0.7))
            c.restore()
            if ang > 1:
                a_ = math.radians(ang)
                ex, ey = WX0 - math.cos(a_) * 236, -2 - math.sin(a_) * 236
                c.drawLine(WX0 + 2, -250, ex, ey, P("#9AA3B8", 0.9, stroke=3))
        self.draw_people(c, t, night)
        # torches along the walls
        if stone_on and k_wall >= 1:
            for i, (tx, ty) in enumerate(((WX0 + 60, WTOP - 30), (WX1 + 60, -200), (200, -200), (640, -200), (450, -730))):
                tk = clamp((t - T["light"] - i * 0.12) * 4) if t >= T["light"] else (0.8 if i == 0 and night > 0.5 else 0.0)
                if tk > 0:
                    torch(c, tx, ty, t, tk, 1.0, seed=i)
            for i, (bx, by, bh) in enumerate(((425, -640, 150), (-195, -420, 120), (65, -380, 110), (755, -470, 130))):
                banner(c, bx, by, bh, t, prog(t, T["banners"] + i * 0.1, T["banners"] + 0.5 + i * 0.1), ["#F59E0B", "#DC2626", "#F59E0B", "#DC2626"][i])
        c.restore()
        self.ui["cam"] = (cx, cy, z)

    def draw_people(self, c, t, night):
        T, s, e = self.T, self.tl.s, self.tl.e
        stone_on = t >= T["stone"]
        # ---- the crew
        if t < T["stone"]:
            pose = "stand" if t < T["house"] else "cheer" if t < T["neighbors"] else "look" if t < T["fire"] else "duck"
            self.crew(c, t, pose, clamp((t - T["fire"] - 0.4) * 2), xs=(690, 736, 782), face=-1)
        elif t < s("break3") - 0.1:
            pose = "cheer" if t < s("break2") else "look" if t < T["climb"] else "duck" if t < T["moat"] else "cheer" if t >= T["shoot"] + 0.3 else "stand"
            if not T["battlements"] - 0.2 <= t:                          # (during the battlements shot only the one on the wall is shown)
                self.crew(c, t, pose, 0.35 if t < T["wall"] else 0.0, xs=(-250, -204, -158), face=-1)
            hd = prog(t, T["hide"], T["hide"] + 0.25)
            if t >= T["battlements"]:                                   # one of them up on the wall, behind the parapet
                engineer(c, WX0 + 70, WTOP + 34 * hd, 104, "#3B82F6", t, "duck" if hd > 0.5 else "stand", face=-1)
            if T["shoot"] <= t < T["shoot"] + 0.6:
                u = prog(t, T["shoot"], T["shoot"] + 0.45)
                ax = lerp(WX0 - 10, -900, u)
                c.drawLine(ax, WTOP - 20 + 250 * u * u, ax + 46, WTOP - 26 + 250 * u * u - 20 * u, P("#E8D5A8", 1, stroke=4))
        elif t < s("break4") - 0.12:
            pose = "look" if t < T["crack"] else "duck" if t < T["drawbridge"] else "cheer" if t >= T["rocks"] else "point"
            self.crew(c, t, pose, xs=(-250, -204, -158), face=-1)
            if t >= T["murder"] - 0.2:                                  # the one in the guard room, dropping rocks
                engineer(c, WX0 + 100, -180, 78, "#F97316", t, "carry" if t < T["boiling"] else "shrug", face=-1)
        elif t < s("fix4") - 0.12:
            self.crew(c, t, "shrug" if t >= T["lunch"] else "stand", xs=(WX0 + 46, WX0 + 92, WX0 + 138), y=WTOP, face=-1, h=92)
        elif t < T["midnight"] - 0.05:
            if t < T["sally"] - 0.2:
                self.crew(c, t, "point" if t < T["stock"] else "cheer", xs=(-210, -164, -118), face=1)
            else:                                                       # off they go, out through the hidden door
                x0 = lerp(420, 836, prog(t, T["sally"] - 0.2, T["midnight"] - 0.1))
                for i, col in enumerate(SHIRTS):
                    px = x0 + (2 - i) * 54
                    engineer(c, min(px, 846), 0, 110 + (i % 2) * 8, col, t + i * 0.3, "walk", face=1) if px < 850 else None
        elif t < s("reveal") - 0.12:
            pass                                                        # the raid: drawn with the camp, further down
        elif t < s("tag") - 0.2:
            self.crew(c, t, "cheer", xs=(-250, -204, -158), face=-1)
            hats_in_the_air(c, (-250, -204, -158), -150, t, T["cong2"])
        if t >= T["trumpet"] - 0.5:
            engineer(c, 430, -700, 96, "#3B82F6", t, "point", face=1)
            c.drawPath(_horn(476, -770), lin_paint(476, 0, 540, 0, ["#FDE68A", "#EAB308"]))
            for i in range(3):
                u = ((t - T["trumpet"]) * 0.8 + i * 0.33) % 1.0
                if t >= T["trumpet"]:
                    nx, ny = 548 + u * 120, -790 - u * 90 + math.sin(u * 9 + i) * 14
                    c.drawCircle(nx, ny, 9, P("#FDE68A", 1 - u))
                    c.drawLine(nx + 8, ny, nx + 8, ny - 30, P("#FDE68A", 1 - u, stroke=4))
        # ---- the neighbours
        if s("break1") <= t < T["stone"]:
            for i, hat in enumerate(("none", "cap", "beanie")):
                x = lerp(-420 - i * 70, 60 + i * 62, e_out(prog(t, T["neighbors"] - 0.3 + i * 0.1, T["torches"] + 0.1)))
                thrown = t >= T["torches"] + 0.15 + i * 0.08
                person(c, x, 0, 124, TEAM, t, "cheer" if thrown else "walk", hat=hat, face=1)
                if not thrown:
                    torch(c, x + 28, -128, t, 1.0, 0.8, seed=i)
                elif t < T["fire"] + 0.25:
                    u = prog(t, T["torches"] + 0.15 + i * 0.08, T["fire"] + 0.1 + i * 0.05)
                    torch(c, lerp(x + 28, 380 + i * 60, u), lerp(-128, -250, u) - 160 * math.sin(u * math.pi), t, 1.0, 0.8, seed=i)
        if s("break2") - 0.1 <= t < s("break3") - 0.1:
            gone = t >= T["fallin"]
            fk = prog(t, T["fallin"], T["fallin"] + 0.5)
            for i in range(2):
                lx = -560 - i * 90
                if t >= T["ladders"] - 0.25 - i * 0.1:
                    up = e_out(prog(t, T["ladders"] - 0.25 - i * 0.1, T["ladders"] + 0.2))
                    c.save()
                    c.translate(lx, 0)
                    c.rotate(lerp(0, -74 - i * 4, fk) if gone else 0)
                    if fk < 1:
                        ladder(c, 0, 0, (WX0 - lx - 4) * up, (WTOP - 6 + i * 30) * up, 1 - fk)
                    c.restore()
                cl = prog(t, T["climb"] - 0.3 + i * 0.25, T["over"] + 0.5 + i * 0.25)
                if not gone:
                    px, py = lerp(lx, WX0 - 6, cl), lerp(0, WTOP + i * 30, cl)
                    person(c, px, py, 118, TEAM, t, "walk" if cl < 1 else "cheer", hat=("cap", "none")[i], face=1)
                else:
                    u = prog(t, T["fallin"], T["fallin"] + 0.45)
                    person(c, lerp(-520, -600 - i * 50, u), lerp(-220, 30, e_in(u)), 118, TEAM, t, "cheer", hat=("cap", "none")[i], face=-1, a=1 - prog(u, 0.85, 1.0))
            if gone:
                splash(c, -600, 12, t, T["fallin"] + 0.4, seed=5)
                splash(c, -650, 12, t, T["fallin"] + 0.5, seed=6)
        if s("break3") - 0.1 <= t < s("break4") - 0.12:
            sl = prog(t, T["slide"], T["slide"] + 0.5)
            swing = 0.0
            for k0 in (T["knock"], T["knock"] + 0.38, T["crack"]):
                swing += bump(t, k0 - 0.2, k0 + 0.12) * 34
            run_in = t >= T["crack"] + 0.2
            for i in range(3):
                bx = -690 + i * 62 + swing
                if i == 2 and run_in:                                    # one of them makes it inside... and regrets it
                    px = lerp(bx, -384, e_out(prog(t, T["crack"] + 0.2, T["drawbridge"])))
                    hit = t >= T["murder"] + 0.4
                    person(c, px, 0, 112, TEAM, t, "duck" if hit else "walk" if t < T["drawbridge"] else "shrug", hat="beanie", face=1)
                    for j, r0 in enumerate((T["murder"] + 0.3, T["murder"] + 0.75, T["rocks"])):
                        u = prog(t, r0, r0 + 0.28)
                        if 0 < u < 1:
                            rock(c, -424 + j * 40, lerp(-170, -84, e_in(u)), 13, u * 200)
                        elif u >= 1 and t < r0 + 0.9:
                            rock(c, -424 + j * 40 + (t - r0 - 0.28) * 60 * (j - 1), -12, 13, 40 * j)
                elif sl <= 0:
                    person(c, bx, -8, 118, TEAM, t, "carry", hat=("none", "cap", "beanie")[i], face=1)
                else:
                    person(c, lerp(bx, -640 + i * 30, sl), lerp(-8, 40, e_in(sl)), 118, TEAM, t, "cheer", hat=("none", "cap", "beanie")[i], face=1, a=1 - prog(sl, 0.8, 1.0))
            if sl <= 0:                                                 # the ram
                cyl_h = 30
                c.save()
                c.translate(-720 + swing, -86)
                c.rotate(-90)
                cyl(c, -cyl_h / 2, 0, cyl_h, 250, "#7C4A2D", r=10)
                c.restore()
                box(c, -480 + swing, -106, 22, 40, "#4A5368", r=6)
            else:
                rk = prog(t, T["slide"], T["slide"] + 0.45)
                c.save()
                c.translate(-700 + 120 * rk, -86 + 110 * e_in(rk))
                c.rotate(-90 + 50 * rk)
                cyl(c, -15, 0, 30, 250, "#7C4A2D", r=10, a=1 - prog(rk, 0.85, 1.0))
                c.restore()
                splash(c, -610, 12, t, T["slide"] + 0.42, seed=7, n=30, width=1.3)
            if t >= T["boiling"] - 0.1:                                 # the cauldron nobody can afford
                ok = prog(t, T["boiling"] - 0.1, T["boiling"] + 0.15) * (1 - prog(t, T["expensive"] + 0.5, T["expensive"] + 0.8))
                if ok > 0:
                    c.save()
                    c.translate(WX0 + 46, -182)
                    c.scale(e_back(ok), e_back(ok))
                    c.drawOval(R(-24, -34, 48, 40), rad_paint(-8, -24, 44, ["#6B7385", "#2A3042", "#11151F"]))
                    c.drawOval(R(-20, -36, 40, 12), P("#FACC15"))
                    add_glow(c, 0, -30, 40, "#FACC15", 0.5)
                    c.restore()
        if s("break4") - 0.12 <= t < s("reveal") - 0.12 and not (s("fix4") - 0.12 <= t < T["midnight"] - 0.05):
            ck = prog(t, T["camp"] - 0.5, T["camp"])
            for i, tx in enumerate((-1220, -1060)):
                c.save()
                c.translate(0, 0)
                tent(c, tx, e_back(clamp(ck * 1.2 - i * 0.2)) if ck < 1 else 1.0)
                c.restore()
            fire_x = -900
            c.drawLine(fire_x - 34, 0, fire_x + 34, -12, P("#5B3A22", 1, stroke=10))
            c.drawLine(fire_x + 34, 0, fire_x - 34, -12, P("#5B3A22", 1, stroke=10))
            v2.flame(c, fire_x, -8, 26, 110, t, 0.9, seed=9, ang=270)
            add_glow(c, fire_x, -40, 320, "#FF8A3D", 0.5)
            c.drawLine(fire_x - 50, 0, fire_x - 50, -92, P("#3A2414", 1, stroke=6))
            c.drawLine(fire_x + 50, 0, fire_x + 50, -92, P("#3A2414", 1, stroke=6))
            c.drawLine(fire_x - 58, -90, fire_x + 58, -90, P("#9AA3B8", 1, stroke=4))
            raid = t >= T["raids"] + 0.2
            if not raid:
                self.roast(c, fire_x, -90, t * 90)
            asleep = t >= T["midnight"] - 0.05
            awake = t >= s("cta") + 1.3
            for i, px in enumerate((-990, -830, -770)):
                person(c, px, 0, 118, TEAM, t, "cheer" if (asleep and awake) else "duck" if asleep else "sit", hat=("none", "cap", "beanie")[i], face=1 if i == 0 else -1)
                if asleep and not awake:
                    for j in range(2):
                        u = (t * 0.7 + j * 0.5 + i * 0.3) % 1.0
                        text(c, "z", px + 20 + u * 26, -100 - u * 60, 26 + 14 * u, "#DCE7FF", "Poppins-Black", a=1 - u)
            if t >= T["midnight"] - 0.05:                               # the midnight raid: in on tiptoe, out with the roast
                got = t >= T["raids"] + 0.2
                x0 = (lerp(-1420, -960, e_out(prog(t, T["midnight"], T["raids"] + 0.2))) if not got
                      else lerp(-960, -1750, e_in(prog(t, s("cta") + 0.9, s("cta") + 2.4))))
                self.crew(c, t, "walk" if (not got or t > s("cta") + 0.9) else "carry", xs=(x0 - 100, x0 - 50, x0), face=1 if not got else -1)
                if got:
                    self.roast(c, x0 + (40 if t <= s("cta") + 0.9 else -40), -92)
            if t >= T["lunch"] - 0.2 and t < s("fix4"):                  # lunch can't get in either
                u = prog(t, T["lunch"] - 0.2, T["lunch"] + 0.9)
                lx_, ly_ = lerp(-760, -580, e_out(clamp(u * 1.6))), -40 + 120 * e_in(clamp((u - 0.55) / 0.45))
                person(c, -760, 0, 118, "#16A34A", t, "carry" if u < 0.6 else "shrug", hat="cap", face=1)
                if ly_ < 40:
                    box(c, lx_ - 16, ly_ - 30, 32, 30, "#D6A15C", r=5)
                    c.drawRect(R(lx_ - 16, ly_ - 22, 32, 4), P("#7C4A2D"))
                splash(c, -580, 12, t, T["lunch"] + 0.78, seed=11, n=14, speed=380)
        if t >= s("tag") - 0.2:                                         # nobody swims in the moat
            for i, col in enumerate(SHIRTS[:2]):                         # two of the crew look down from the wall; the third is busy
                engineer(c, WX0 + 104 + i * 42, WTOP, 88, col, t + i * 0.4, "look" if t < T["plop"] + 0.4 else "shrug", face=-1)
            u = prog(t, T["plop"], T["plop"] + 0.42)
            if 0 < u < 1:
                c.drawOval(R(WX0 - 26, lerp(-276, 4, e_in(u)), 14, 18), P("#5B3A22"))
            splash(c, WX0 - 19, 12, t, T["plop"] + 0.42, seed=13, n=16, speed=360, col="#A3B18A")
            back = prog(t, T["swims"] - 0.1, T["swims"] + 0.6)
            sx = lerp(-740, -900, e_io(back))
            person(c, sx, 0, 118, TEAM, t, "look" if back <= 0 else "walk", hat="none", face=1 if back <= 0 else -1)
            c.drawOval(R(sx - 34, -66, 68, 26), P("#F472B6", 1, stroke=11))
            if t >= T["plop"] + 0.4:
                c.drawOval(R(WX0 - 60, 12, 84, 10), P("#6B7A3A", 0.6 * (1 - prog(t, T["plop"] + 0.4, T["plop"] + 3))))

    def roast(self, c, x, y, rot=0.0):
        c.save()
        c.translate(x, y)
        c.rotate(math.sin(math.radians(rot)) * 8)
        c.drawOval(R(-26, -18, 52, 34), rad_paint(-8, -8, 40, ["#F4C27A", "#C9853B", "#7C4A1E"]))
        c.drawLine(18, -4, 34, -16, P("#F5E6C8", 1, stroke=6))
        c.drawLine(18, 6, 36, 10, P("#F5E6C8", 1, stroke=6))
        c.restore()

    def draw_motte(self, c, t):
        self.world(c, t, self.cams["motte"].at(t))

    def draw_wallcam(self, c, t):
        self.world(c, t, self.cams["wallcam"].at(t))

    def draw_keepcam(self, c, t):
        T = self.T
        self.world(c, t, self.cams["keepcam"].at(t))
        if T["boulders"] - 0.5 <= t < T["hit"] + 1.4:                    # the boulder that glances off the round keep
            u, v = prog(t, T["boulders"] - 0.5, T["hit"]), prog(t, T["hit"], T["hit"] + 1.3)
            bx = lerp(-130, 362, u) if v <= 0 else 362 - 420 * v
            by = (lerp(-1000, -480, u) - 120 * math.sin(u * math.pi)) if v <= 0 else -480 - 520 * v + 900 * v * v
            self.view(c, self.ui["cam"])
            rock(c, bx, by, 34, t * 400)
            v2.embers(c, 366, -480, t, T["hit"], 0.6, n=18, speed=520, seed=4, col="#FFE9C9", cone=(150, 250))
            c.restore()

    def draw_gate(self, c, t):
        self.world(c, t, self.cams["gate"].at(t))

    def draw_siege(self, c, t):
        self.world(c, t, self.cams["siege"].at(t))

    def draw_yard(self, c, t):
        self.world(c, t, self.cams["yard"].at(t))

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -260, 1.0)), x, y)

    def ui_motte(self, c, t, tw):
        T = self.T
        hx, hy = self.at(450, -250)
        self.label(hx + 70, hy, hx + 250, hy - 190, "house", T["house"] + 0.15, T["neighbors"] - 0.3, HILITE)
        self.badge("alert", T["fire"] + 0.3, self.tl.s("fix1") - 0.2)
        self.red(T["fire"])

    def ui_wallcam(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break2") - 0.1:
            wx, wy = self.at(WX1, -250)
            self.label(wx, wy, wx + 260, wy - 150, "wall", T["wall"] + 0.3, T["tall"] - 0.1)
            p = self.span(T["tall"] - 0.25, T["towers"] - 0.5)
            if p > 0:                                                    # how thick: a dimension line across the wall top
                x0, y0 = self.at(WX0, WTOP - 70)
                x1, _ = self.at(WX1, WTOP - 70)
                c.drawLine(x0, y0, x0 + (x1 - x0) * p, y0, P(HILITE, 1, stroke=5))
                for xx in (x0, x1):
                    c.drawLine(xx, y0 - 16, xx, y0 + 16, P(HILITE, p, stroke=5))
                v2.chip(c, (x0 + x1) / 2, y0 - 60, self.L["thick"], p, size=34, accent=HILITE)
        else:
            self.badge("alert", T["climb"] + 0.1, T["moat"] - 0.1)
            self.red(T["climb"], 1.6)
            mx, my = self.at((MX0 + WX0) / 2, 30)
            self.label(mx, my, mx - 110, my - 330, "moat", T["moat"] + 0.6, T["battlements"] - 0.1, "#7DD3FC")
            tx, ty = self.at(WX0 + 16, WTOP - 50)
            self.label(tx, ty, tx + 330, ty - 150, "teeth", T["battlements"] + 0.4, T["shoot"] + 0.1)
            self.badge("check", T["shoot"] + 0.4, s("break3") - 0.15)

    def ui_keepcam(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break2"):
            kx, ky = self.at(535, -560)
            self.label(kx, ky, 800, ky - 170, "towers", T["towers"] + 0.2, T["hit"] + 0.2)
            self.badge("check", T["hit"] + 0.35, s("break2") - 0.15, x=250, y=520)
        elif tw >= s("tag") - 0.2:
            gx, gy = self.at(WX0 - 18, -306)
            self.label(gx - 20, gy, gx - 150, gy - 220, "toilet", T["toilet"] - 0.1, T["plop"] + 1.2, HILITE)

    def ui_gate(self, c, t, tw):
        T, s = self.T, self.tl.s
        rx, ry = self.at(-600, -100)
        self.label(rx, ry, rx - 10, ry - 300, "ram", T["ram"] - 0.5, T["drawbridge"] - 0.25, WARN)
        self.badge("alert", T["crack"] + 0.1, T["drawbridge"] + 0.2)
        self.red(T["crack"], 1.6)
        bx, by = self.at(-590, -150)
        self.label(bx, by, bx - 60, by - 260, "bridge", T["drawbridge"] + 0.35, T["portcullis"] + 0.3)
        px, py = self.at(WX0 + 26, -60)
        self.label(px, py, px - 250, py - 380, "port", T["clang"] + 0.05, T["murder"] - 0.15)
        hx, hy = self.at(-384, -164)
        self.label(hx, hy, hx + 150, hy - 330, "holes", T["murder"] + 0.1, T["boiling"] - 0.2)
        ox, oy = self.at(WX0 + 46, -230)
        self.chip(ox + 10, oy - 150, "oil", T["expensive"] - 0.2, T["expensive"] + 0.7, accent=WARN, size=36)
        self.badge("check", T["rocks"] + 0.4, s("break4") - 0.2, x=230, y=520)

    def ui_siege(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4"):
            p = self.span(T["lunch"] + 0.9, s("fix4") - 0.15)
            if p > 0:
                v2.gauge(c, 60, 300, [(self.L["food"], 1 - 0.92 * prog(tw, T["lunch"] + 0.9, T["starve"] + 0.3), "#F59E0B")], p, w=330)
            self.badge("alert", T["starve"] - 0.4, s("fix4") - 0.2)
            self.red(T["starve"] - 0.5, 1.6)
        else:
            self.badge("check", T["raids"] + 0.3, s("reveal") - 0.2)

    def ui_yard(self, c, t, tw):
        T = self.T
        wx, wy = self.at(68, 150)
        self.label(wx - 56, wy, wx - 330, wy - 90, "well", T["well"] + 0.3, T["stock"] + 0.3, "#7DD3FC")
        cx_, cy_ = self.at(-200, 56)
        self.label(cx_, cy_, cx_ - 60, cy_ - 330, "cellar", T["stock"] + 0.4, T["sally"] - 0.25)
        sx, sy = self.at(848, -60)
        self.label(sx, sy, sx - 200, sy - 330, "sally", T["sally"] + 0.3, T["midnight"] - 0.1)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, True, 60), -10), (0.1, rumble(1.0, 61), -9), (T["house"], sfx.pop(62), -5)]
        ev += [(T["neighbors"], sfx.tap(63 + i), -10) for i in range(3)]
        ev += [(T["torches"] + 0.15, sfx.whoosh(0.5, True, 66), -6), (T["fire"], sfx.sizzle(1.6, 67), -4), (T["fire"] + 0.2, sfx.alarm(3, 820), -11),
               (T["fire"] + 1.2, sfx.sizzle(1.4, 68), -8)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 69), -4), (T["stone"], rumble(1.1, 70), -6), (T["wall"], sfx.thud(0.4, 71), -4),
               (T["tall"] - 0.2, sfx.pop(72), -7), (T["towers"] - 0.45, sfx.whoosh(0.4, False, 73), -4), (T["towers"], sfx.thud(0.4, 74), -5),
               (T["boulders"] - 0.5, sfx.whoosh(0.7, False, 75), -5), (T["hit"], sfx.clank(240, 0.5, 76), -2), (T["hit"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, True, 77), -4), (T["ladders"] - 0.2, sfx.clank(700, 0.25, 78), -6),
               (T["ladders"], sfx.clank(760, 0.25, 79), -7), (T["climb"], sfx.alarm(3, 820), -11)]
        ev += [(T["climb"] + 0.1 + i * 0.14, sfx.tap(80 + i), -10) for i in range(5)]
        ev += [(T["moat"], rumble(0.8, 86), -7), (T["moat"] + 0.4, water_snd(0.9, 87), -6), (T["fallin"] + 0.4, water_snd(0.6, 88), -2),
               (T["battlements"] + 0.1, sfx.pop(89), -6), (T["battlements"] + 0.35, sfx.pop(90), -7), (T["battlements"] + 0.6, sfx.pop(91), -8),
               (T["shoot"], sfx.whoosh(0.35, True, 92), -5), (T["shoot"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 93), -4), (T["knock"], sfx.thud(0.4, 94), -1), (T["knock"] + 0.38, sfx.thud(0.4, 95), -1),
               (T["crack"], sfx.snap(96), 0), (T["crack"] + 0.05, sfx.alarm(3, 820), -11)]
        ev += [(T["drawbridge"], sfx.creak(0.8, 97), -3), (T["slide"] + 0.42, water_snd(0.7, 98), -1), (T["portcullis"] - 0.1, sfx.clank(300, 0.4, 99), -6),
               (T["clang"], sfx.clank(200, 0.7, 100), 0), (T["murder"] + 0.58, sfx.thud(0.25, 101), -5), (T["murder"] + 1.03, sfx.thud(0.25, 102), -5),
               (T["rocks"] + 0.28, sfx.thud(0.25, 103), -4), (T["boiling"], sfx.pop(104), -6), (T["expensive"], sfx.buzz(), -8),
               (T["rocks"] + 0.45, sfx.chime(), -7)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 105), -4), (T["camp"] - 0.4, sfx.pop(106), -7), (T["camp"] - 0.2, sfx.pop(107), -8),
               (s("break4") + 0.3, sfx.sizzle(2.4, 108), -12), (T["lunch"] + 0.78, water_snd(0.4, 109), -5), (T["starve"] - 0.4, sfx.alarm(3, 820), -11),
               (T["starve"], sfx.womp(), -9)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 110), -4), (T["well"], rumble(0.7, 111), -7), (T["well"] + 0.7, water_snd(0.5, 112), -8),
               (T["well"] + 1.5, sfx.sparkle(0.5, 6, 113), -9)]
        ev += [(T["stock"] + i * 0.13, sfx.pop(114 + i), -9) for i in range(6)]
        ev += [(T["sally"], sfx.creak(0.5, 121), -5), (T["midnight"] - 0.05, sfx.whoosh(0.4, True, 122), -5),
               (T["raids"] + 0.2, sfx.pop(123), -3), (T["raids"] + 0.35, sfx.chime(), -7)]
        ev += [(T["pause"], sfx.click(124), 0), (T["follow"] - 0.15, sfx.pop(125), -4), (s("cta") + 1.3, sfx.alarm(2, 900), -12)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 126), -4), (T["banners"], sfx.whoosh(0.6, False, 127), -9),
               (T["light"], sfx.sizzle(0.6, 128), -10), (T["light"] + 0.2, sfx.sparkle(0.7, 8, 129), -9), (T["trumpet"], fanfare(), -5)]
        ev += [(T["s1"], sfx.pop(130), -3), (T["s2"], sfx.pop(131), -3), (T["s3"], sfx.pop(132), -3), (T["s1"] - 0.3, sfx.whoosh(1.4, False, 133), -12)]
        ev += [(T["cong2"], sfx.pop(134), -2), (T["cong2"], sfx.sparkle(1.0, 14, 135), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 136), -6), (T["plop"] + 0.42, water_snd(0.35, 137), -3), (T["swims"] + 0.35, sfx.womp(), -2)]
        return ev


def _tri(x, y, hw, h):
    """Triangle with its base centred on (x, y) and its tip h above (h < 0: below)."""
    p = skia.Path()
    p.moveTo(x - hw, y)
    p.lineTo(x, y - h)
    p.lineTo(x + hw, y)
    p.close()
    return p


def _horn(x, y):
    p = skia.Path()
    p.moveTo(x, y - 5)
    p.lineTo(x + 46, y - 20)
    p.lineTo(x + 62, y - 30)
    p.lineTo(x + 62, y + 22)
    p.lineTo(x + 46, y + 12)
    p.lineTo(x, y + 5)
    p.close()
    return p


NAME = "castle"
EPISODE = Castle
