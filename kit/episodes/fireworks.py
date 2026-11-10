"""Episode 12 - A fireworks show.  v2 look: a field at night, three sets with whip cuts.

field   the launch site (mortar tubes at x = 0, the firing desk far to the left at x = -900), the town and the crowd
        far back, and the whole sky above; cameras "pad" (close) and "wide" look at this one world
shell   one shell cut open, big: time fuse, burst charge, the pellets called stars
bed     where the dog is
Ground at y = 0, up is negative.
"""
from v2_base import *  # noqa: F401,F403

SHELLC = "#B7803F"
TUBES = [-300 + i * 60 for i in range(11)]
REDC, GREENC, BLUEC, PINKC, GOLDC = "#FF4D5E", "#4ADE80", "#60A5FA", "#FB7185", "#FDE047"


# ====================================================================================== pieces
def heart_pt(a):
    return (16 * math.sin(a) ** 3 / 17.0, -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) / 17.0)


def burst(c, x, y, t, t0, col, r=260, n=44, shape="ball", rot=0.0, dur=2.3, seed=1, a=1.0):
    """One shell going off at (x, y) at time t0. shape: ball | ring | heart | flash (white, dull, no stars)."""
    age = t - t0
    if not 0 <= age <= dur:
        return
    u = age / dur
    k = 1 - (1 - min(1.0, age / 0.6)) ** 3
    fade = (clamp(1 - (u - 0.45) / 0.55) if u > 0.45 else 1.0) * a
    if age < 0.2:
        add_glow(c, x, y, r * 1.5 * (1 - age / 0.2) + 50, "#FFFFFF", 0.95 * (1 - age / 0.2) * a)
    if shape == "flash":
        puff(c, x, y, 70 + 150 * k, "#8B93A8", 0.6 * fade, k=seed % 6)
        puff(c, x + 60, y - 40, 50 + 110 * k, "#6B7385", 0.5 * fade, k=(seed + 2) % 6)
        puff(c, x - 70, y + 20, 40 + 90 * k, "#6B7385", 0.45 * fade, k=(seed + 4) % 6)
        return
    add_glow(c, x, y, r * (0.5 + 0.9 * k), col, 0.20 * fade)
    rng = random.Random(seed)
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(n):
        if shape == "heart":
            dx, dy = heart_pt(2 * math.pi * i / n)
        else:
            ang = rng.uniform(0, 2 * math.pi)
            rad = 1.0 if shape == "ring" else rng.uniform(0.3, 1.0)
            dx, dy = math.cos(ang) * rad, math.sin(ang) * rad
        px = x + (dx * cr - dy * sr) * r * k
        py = y + (dx * sr + dy * cr) * r * k + 70 * u * u * (0.4 if shape == "heart" else 1.0)
        tw = 0.6 + 0.4 * math.sin(t * 31 + i * 1.7)
        c.drawLine(x + (px - x) * 0.8, y + (py - y) * 0.8, px, py, P(col, 0.55 * fade, stroke=5))
        add_glow(c, px, py, 28, col, 0.95 * fade * tw)
        c.drawCircle(px, py, 5.0, P("#FFFFFF", fade * tw))
    if shape == "ball":                                                              # a paler heart of smaller stars
        pale = mix(col, "#FFFFFF", 0.55)
        for i in range(n // 2):
            ang = rng.uniform(0, 2 * math.pi)
            rad = rng.uniform(0.15, 0.5)
            px, py = x + math.cos(ang) * rad * r * k, y + math.sin(ang) * rad * r * k + 50 * u * u
            add_glow(c, px, py, 18, pale, 0.8 * fade * (0.6 + 0.4 * math.sin(t * 37 + i)))


def shell_ball(c, x, y, r, t, lit=1.0, a=1.0):
    c.drawCircle(x, y, r, rad_paint(x - r * 0.3, y - r * 0.4, r * 1.6, [(shade(SHELLC, 0.3), a), (SHELLC, a), (shade(SHELLC, -0.45), a)]))
    c.drawLine(x - r, y, x + r, y, P("#5B3A22", 0.6 * a, stroke=max(1.5, r * 0.12)))
    if lit > 0:
        add_glow(c, x, y + r, r * 1.6, "#FFB347", 0.8 * lit * a)


def tube(c, x, s=1.0, cut=False, a=1.0):
    """A mortar tube standing on the ground at x (150 tall at s = 1), in its rack."""
    w, h = 56 * s, 150 * s
    if cut:
        c.drawRect(R(x - w / 2, -h, w, h), P("#0B1220", a))
        c.drawRect(R(x - w / 2, -h, 7 * s, h), lin_paint(x - w / 2, 0, x - w / 2 + 7 * s, 0, [("#E2E8F0", a), ("#64748B", a)]))
        c.drawRect(R(x + w / 2 - 7 * s, -h, 7 * s, h), lin_paint(x + w / 2 - 7 * s, 0, x + w / 2, 0, [("#94A3B8", a), ("#475569", a)]))
        c.drawRect(R(x - w / 2, -7 * s, w, 7 * s), P("#64748B", a))
    else:
        cyl(c, x - w / 2, -h, w, h, "#64748B", r=4 * s, a=a)
        c.drawOval(R(x - w / 2, -h - 7 * s, w, 14 * s), P("#0B1220", a))
    c.drawRect(R(x - w / 2 - 10 * s, -44 * s, w + 20 * s, 12 * s), P("#7C4A2D", a))


def crowd(c, x0, x1, t, look=0.0, seed=3, clap=None):
    """The town watching from far back: a row of dark heads, a few phones held up."""
    rng = random.Random(seed)
    x = x0
    i = 0
    while x < x1:
        h = rng.uniform(84, 124)
        col = rng.choice(["#232B55", "#2C3668", "#1C2347"])
        c.drawRRect(rr(x - 20, -h + 26, 40, h - 26, 14), P(col))
        c.drawCircle(x, -h + 8 - 5 * look, 19, P(col))
        c.drawCircle(x - 3, -h + 4 - 5 * look, 19, P("#9DB7FF", 0.16))
        if rng.random() < 0.35:
            c.drawRRect(rr(x + 14, -h - 26, 13, 22, 3), P("#E0F2FE", 0.95))
            add_glow(c, x + 20, -h - 15, 26, "#BAE6FD", 0.6)
        if clap is not None and i == clap[0]:
            k = clap[1]
            c.drawRRect(rr(x - 20, -h + 26, 40, h - 26, 14), P("#4C63C7"))
            c.drawCircle(x, -h + 8, 19, P("#4C63C7"))
            sp = 14 * abs(math.sin(t * 16)) * k
            c.drawLine(x - 6 - sp, -h - 16, x - 3, -h - 44, P("#E8B48A", k, stroke=9))
            c.drawLine(x + 6 + sp, -h - 16, x + 3, -h - 44, P("#E8B48A", k, stroke=9))
            for j in range(3):
                a = math.radians(-90 + (j - 1) * 40)
                c.drawLine(x + math.cos(a) * 34, -h - 52 + math.sin(a) * 34, x + math.cos(a) * 54, -h - 52 + math.sin(a) * 54,
                           P(HILITE, k * (0.5 + 0.5 * math.sin(t * 16)), stroke=5))
        x += rng.uniform(42, 66)
        i += 1


def thump(d=0.5, seed=40):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-tt * 9) + 40) / sfx.SR) * np.exp(-tt * 7)
    return sfx._norm(x + 0.3 * sfx._lp(sfx._rng(seed).standard_normal(n), 900) * sfx._env(n, 0.002, 0.08), 0.85)


def crackle(d=1.2, seed=41):
    n = int(d * sfx.SR)
    x = np.zeros(n)
    rng = sfx._rng(seed)
    for _ in range(int(d * 70)):
        i = int(rng.uniform(0, d - 0.01) * sfx.SR)
        x[i:i + 40] += rng.uniform(-1, 1) * np.hanning(40) * rng.uniform(0.3, 1.0)
    return sfx._norm(sfx._hp(x, 1800) * sfx._ar(n, 0.02, d * 0.6), 0.5)


def whistle(d=0.9):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    return sfx._norm(np.sin(2 * np.pi * np.cumsum(700 + 1500 * tt / d) / sfx.SR) * sfx._ar(n, 0.03, d * 0.3), 0.35)


# ====================================================================================== the episode
class Fireworks(EpisodeV2):
    BUILD_NO = 12
    FIRST_SET = "field"
    CLEAR = "#060818"
    TITLE = {"en": "FIREWORKS", "ar_sa": "ألعاب نارية"}
    EMPH = {"en": ["CONGRATS", "FIREWORKS", "TINY", "TOWN", "SHELL", "MORTAR", "LIFT", "LOW", "EYEBROWS", "FUSE", "BURST", "FLASH",
                   "COLOR", "SHAPE", "WOW", "STARS", "RED", "GREEN", "BLUE", "HEART", "SIDEWAYS", "THOUSAND", "ELECTRIC", "COMPUTER",
                   "BEAT", "FOLLOW", "VAULT", "MUSIC", "EARLY", "ZERO", "YOURSELF", "DOG", "TUESDAY"],
            "ar_sa": ["مبروك", "نارية", "صغيرة", "والديرة", "كورة", "أنبوب", "دفع", "واطية", "حواجب", "فتيل", "ويفجّر", "وميض", "لون",
                      "شكل", "واو", "نجوم", "أحمر", "أخضر", "أزرق", "قلب", "مقلوب", "ألف", "كهربائية", "وكمبيوتر", "الإيقاع", "تابعني",
                      "بنك", "موسيقى", "يصفق", "وصفر", "بيدك", "والكلب", "الثلاثاء"]}
    KEYS = {"ar_sa": {
        ("hook", "POP"): "فرقعت", ("hook", "POPPER"): "طرطيعة", ("hook", "CONGRATS"): "مبروك",
        ("break1", "TINY"): "طقّة", ("break1", "CONFETTI"): "قصاصات", ("break1", "TOWN"): "والديرة", ("break1", "WATCHING"): "تتفرج",
        ("fix1", "CREW"): "فريق", ("fix1", "SHELL"): "كورة", ("fix1", "LOWERS"): "وينزّلها", ("fix1", "TUBE"): "أنبوب", ("fix1", "LIFT"): "حشوة",
        ("fix1", "SHOOTS"): "تقذفها", ("fix1", "SKY"): "للسما",
        ("break2", "FLIES"): "تطير", ("break2", "BURSTS"): "تنفجر", ("break2", "LOW"): "واطية", ("break2", "EYEBROWS"): "حواجب",
        ("fix2", "FUSE"): "فتيل", ("fix2", "BURNS"): "يحترق", ("fix2", "UP"): "طالعة", ("fix2", "BURST"): "ويفجّر", ("fix2", "TOP"): "القمة",
        ("break3", "FLASH"): "وميض", ("break3", "BANG"): "وصوت", ("break3", "COLOR"): "لون", ("break3", "SHAPE"): "شكل", ("break3", "WOW"): "واو",
        ("fix3", "PELLETS"): "حبيبات", ("fix3", "STARS"): "نجوم", ("fix3", "STRONTIUM"): "السترونتيوم", ("fix3", "RED"): "أحمر",
        ("fix3", "GREEN"): "أخضر", ("fix3", "BLUE"): "أزرق", ("fix3", "ARRANGE"): "رتّبها", ("fix3", "HEART"): "قلب", ("fix3", "SIDEWAYS"): "مقلوب",
        ("break4", "GORGEOUS"): "تجنن", ("break4", "LIGHT"): "يولّع", ("break4", "THOUSAND"): "ألف", ("break4", "HAND"): "بيده",
        ("fix4", "ELECTRIC"): "ولاعة", ("fix4", "COMPUTER"): "وكمبيوتر", ("fix4", "FIRES"): "يطلقها", ("fix4", "EARLY"): "بثواني",
        ("fix4", "BEAT"): "الإيقاع",
        ("cta", "LOOK"): "ترفع", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "MUSIC"): "موسيقى", ("reveal", "CROWD"): "وجمهور", ("reveal", "GUY"): "وواحد", ("reveal", "CLAPS"): "يصفق",
        ("stat", "ONE"): "زر", ("stat", "THOUSAND"): "ألف", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "DOG"): "والكلب", ("tag", "BED"): "السرير", ("tag", "TUESDAY"): "الثلاثاء"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a bank vault"),
                   "stat": [("1", "BUTTON"), ("1,000", "SHELLS"), ("0", "EYEBROWS LOST")],
                   "L": {"popper": "PARTY POPPER", "shell": "PAPER SHELL", "tube": "MORTAR TUBE", "lift": "LIFT CHARGE", "fuse": "TIME FUSE",
                         "burstc": "BURST CHARGE", "nocol": "NO COLOR", "noshape": "NO SHAPE", "nowow": "NO WOW", "stars": "STARS",
                         "red": "STRONTIUM", "green": "BARIUM", "blue": "COPPER", "lit": "FUSES LIT", "match": "ELECTRIC MATCH",
                         "comp": "COMPUTER", "beat": "ON THE BEAT", "far": "FAR BACK", "early": "TOO EARLY"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: خزنة بنك"),
                      "stat": [("1", "زر"), ("1000", "قذيفة"), ("0", "حواجب محروقة")],
                      "L": {"popper": "طرطيعة", "shell": "كورة ورق", "tube": "أنبوب حديد", "lift": "حشوة الدفع", "fuse": "فتيل توقيت",
                            "burstc": "حشوة التفجير", "nocol": "بدون لون", "noshape": "بدون شكل", "nowow": "بدون واو", "stars": "نجوم",
                            "red": "سترونتيوم", "green": "باريوم", "blue": "نحاس", "lit": "فتايل مولّعة", "match": "ولاعة كهربائية",
                            "comp": "كمبيوتر", "beat": "مع الإيقاع", "far": "بعيد", "early": "بدري مرة"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "pop": ("hook", "POP", 0.14), "popper": ("hook", "POPPER", 0.3), "congrats": ("hook", "CONGRATS", 0.45),
            "tiny": ("break1", "TINY", 0.15), "confetti": ("break1", "CONFETTI", 0.48), "town": ("break1", "TOWN", 0.8), "watching": ("break1", "WATCHING", 0.9),
            "crew": ("fix1", "CREW", 0.14), "shell": ("fix1", "SHELL", 0.34), "lowers": ("fix1", "LOWERS", 0.4), "tube": ("fix1", "TUBE", 0.6),
            "lift": ("fix1", "LIFT", 0.7), "shoots": ("fix1", "SHOOTS", 0.82), "sky": ("fix1", "SKY", 0.96),
            "flies": ("break2", "FLIES", 0.15), "bursts": ("break2", "BURSTS", 0.42), "low": ("break2", "LOW", 0.52), "eyebrows": ("break2", "EYEBROWS", 0.9),
            "fuse": ("fix2", "FUSE", 0.24), "burns": ("fix2", "BURNS", 0.32), "up": ("fix2", "UP", 0.48), "burst": ("fix2", "BURST", 0.76), "top": ("fix2", "TOP", 0.93),
            "flash": ("break3", "FLASH", 0.28), "bang": ("break3", "BANG", 0.44), "color": ("break3", "COLOR", 0.6), "shape": ("break3", "SHAPE", 0.76),
            "wow": ("break3", "WOW", 0.93),
            "pellets": ("fix3", "PELLETS", 0.14), "stars": ("fix3", "STARS", 0.22), "strontium": ("fix3", "STRONTIUM", 0.26), "red": ("fix3", "RED", 0.33),
            "green": ("fix3", "GREEN", 0.4), "blue": ("fix3", "BLUE", 0.5), "arrange": ("fix3", "ARRANGE", 0.56), "heart": ("fix3", "HEART", 0.68),
            "sideways": ("fix3", "SIDEWAYS", 0.94),
            "gorgeous": ("break4", "GORGEOUS", 0.17), "light": ("break4", "LIGHT", 0.58), "thousand": ("break4", "THOUSAND", 0.68), "hand": ("break4", "HAND", 0.93),
            "electric": ("fix4", "ELECTRIC", 0.22), "computer": ("fix4", "COMPUTER", 0.4), "fires": ("fix4", "FIRES", 0.56), "early": ("fix4", "EARLY", 0.74),
            "beat": ("fix4", "BEAT", 0.95),
            "look": ("cta", "LOOK", 0.22), "follow": ("cta", "FOLLOW", 0.36),
            "music": ("reveal", "MUSIC", 0.2), "crowd": ("reveal", "CROWD", 0.38), "guy": ("reveal", "GUY", 0.7), "claps": ("reveal", "CLAPS", 0.8),
            "s1": ("stat", "ONE", 0.03), "s2": ("stat", "THOUSAND", 0.33), "s3": ("stat", "ZERO", 0.6),
            "cong2": ("closer", "CONGRATS", 0.14),
            "dog": ("tag", "DOG", 0.18), "bed": ("tag", "BED", 0.56), "tuesday": ("tag", "TUESDAY", 0.8)})
        T["heart2"] = self.w("fix3", "HEART", 0.8, nth=1)
        T["bang1"] = max(T["shoots"], T["lift"] + 0.5)                  # fix 1: the lift charge goes
        T["low0"] = T["bursts"] - 0.02                                   # break 2: far too low
        T["apex"] = T["top"] + 0.12                                      # fix 2: the burst charge, near the top
        T["dull"] = T["flash"] - 0.02
        T["reds"] = T["red"] - 0.12
        T["hb1"] = max(T["heart2"] - 0.1, T["heart"] + 0.7)
        T["hb2"] = T["sideways"] - 0.05
        # ---- sets and cameras
        self.cut(s("break1") - 0.1, "field", -1)                         # (pad -> wide)
        self.cut(s("fix1") - 0.12, "field", 1)
        self.cut(s("fix2") - 0.12, "shell", 1)
        self.cut(s("break3") - 0.1, "field", -1)
        self.cut(s("fix3") - 0.12, "shell", 1)
        self.cut(T["strontium"] - 0.3, "field", -1)
        self.cut(T["arrange"] - 0.2, "shell", 1)
        self.cut(T["hb1"] - 0.5, "field", -1)
        self.cut(s("break4") - 0.12, "field", 1)
        self.cut(T["fires"] - 0.3, "field", -1)
        self.cut(s("tag") - 0.2, "bed", 1)
        self.cam = Camera(-150, -150, 1.8)                               # one camera for the field
        cm = self.cam
        WIDE = (0, -387, 0.62)
        cm.key(0.05, -140, -140, 1.9, 1.4)
        cm.key(s("break1") - 0.1, -60, -330, 0.9, 0.0).key(T["tiny"], *WIDE, 1.6)
        cm.key(s("fix1") - 0.12, -20, -140, 1.9, 0.0).key(T["bang1"] - 0.05, 0, -520, 1.5, 0.9)
        cm.key(s("break2") - 0.1, -50, -216, 1.25, 0.0)
        cm.key(s("break3") - 0.1, *WIDE, 0.0)
        cm.key(T["strontium"] - 0.3, 0, -470, 0.66, 0.0)
        cm.key(T["hb1"] - 0.5, 0, -470, 0.66, 0.0)
        cm.key(s("break4") - 0.12, 0, -245, 1.1, 0.0)
        cm.key(s("fix4") - 0.1, 0, -180, 1.5, 0.6).key(T["computer"] - 0.45, -530, -150, 1.8, 0.7)
        cm.key(T["fires"] - 0.3, *WIDE, 0.0)
        cm.key(s("reveal") - 0.1, 60, -400, 0.64, 1.0).key(T["crowd"] - 0.4, 560, -250, 1.0, 0.7).key(T["s1"] - 0.4, 0, -330, 0.6, 0.9)
        cm.key(s("closer"), 0, -330, 0.64, 2.0)
        # ---- every shell of the show: (launch time, tube x, apex x, apex y, colour, shape, rot, radius)
        sh = []
        sh.append((T["dull"] - 0.95, 0, 20, -1150, "#FFFFFF", "flash", 0, 200))
        for i, (tt_, col) in enumerate(((T["reds"], REDC), (T["green"] - 0.1, GREENC), (T["blue"] - 0.1, BLUEC))):
            sh.append((tt_ - 0.95, TUBES[3 + i * 2], -330 + i * 330, -1180 - 60 * (i % 2), col, "ball", 0, 290))
        sh.append((T["hb1"] - 0.95, 0, -140, -1160, PINKC, "heart", 0, 300))
        sh.append((T["hb2"] - 0.95, 60, 250, -1020, REDC, "heart", 90, 260))
        lit = [T["light"] - 0.5 + i * 0.36 for i in range(8)]            # break 4: by hand, one at a time
        self.lit = lit
        for i, tt_ in enumerate(lit):
            sh.append((tt_ + 0.25, TUBES[i + 1], TUBES[i + 1] * 1.6 + 60, -1250 - 90 * (i % 3), (GOLDC, REDC, BLUEC, GREENC)[i % 4], "ball", 0, 250))
        bt = max(0.42, (T["beat"] - T["early"]) / 2.0)                   # fix 4: on the beat
        self.beats = [T["early"] + 0.1 + i * bt for i in range(-1, 4)]
        self.beats = [b for b in self.beats if b > T["fires"] + 0.5]
        for i, b in enumerate(self.beats):
            sh.append((b - 0.95, TUBES[(i * 3) % 11], -420 + i * 280, -1080 - 110 * (i % 2), (GOLDC, PINKC, BLUEC, GREENC, REDC)[i % 5], ("ball", "ring")[i % 2], 0, 280))
        t0 = s("cta") + 0.2                                               # the show itself
        i = 0
        while t0 < s("tag") - 0.9:
            quiet = T["claps"] - 0.9 <= t0 + 0.95 < T["claps"] + 0.7     # (one quiet moment, for the man who claps)
            low = T["s1"] - 0.6 <= t0 + 0.95                             # under the stat cards
            if not quiet:
                rng = random.Random(i * 13 + 5)
                sh.append((t0, TUBES[(i * 4) % 11], rng.uniform(-560, 560), rng.uniform(-900, -620) if low else rng.uniform(-1500, -820),
                           (GOLDC, PINKC, BLUEC, GREENC, REDC, "#C4B5FD")[i % 6], ("ball", "ball", "ring", "heart")[i % 4] if i % 5 else "heart",
                           rng.uniform(-20, 20), rng.uniform(210, 320)))
            t0 += 0.47
            i += 1
        self.shows = sh
        # ---- fix 2: how far the time fuse has burnt
        self.fuse = Track(0.0).to(T["burns"] - 0.1, 1.0, max(0.8, T["apex"] - T["burns"] + 0.1), lambda u: u)
        self.spans = [(T["town"], T["sky"]), (T["low0"], T["apex"] + 0.2), (T["color"] - 0.2, T["hb1"] + 0.3), (T["thousand"], T["beat"])]
        self.shakes = [(T["pop"], 0.2, 6), (T["bang1"], 0.4, 16), (T["low0"], 0.6, 26), (T["apex"], 0.5, 18), (T["dull"], 0.3, 8)]
        self.shakes += [(l + 1.2, 0.25, 6) for l in lit]

    # ------------------------------------------------------------------ set: the field
    def draw_field(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.cam.at(t)
        cam = (cam[0] + math.sin(t * 0.6) * 4, cam[1], cam[2])
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx, cy, gy, ridges=(("#1F1D4A", "#3A2A5E"), ("#12122E", "#1F1A3E")))
        c.drawRect(R(0, 0, W, H), P("#040612", 0.46))                                # a darker night than usual: it is a fireworks sky
        self.view(c, cam)
        # light from whatever is bursting right now
        for (t0, tx, ax, ay, col, shape, rot, rad) in self.shows:
            age = t - (t0 + 0.95)
            if 0 <= age < 1.2:
                add_glow(c, ax, ay, 900, col, 0.10 * (1 - age / 1.2))
        v2.ground(c, -3400, 3400, surface="#1F3B33")
        skyline_night(c, -1700, -400, 0.0, seed=5, hmin=70, hmax=210, lit=0.5, t=t)
        skyline_night(c, 400, 1700, 0.0, seed=8, hmin=70, hmax=230, lit=0.5, t=t)
        c.drawRect(R(-1700, -240, 3400, 240), P("#060818", 0.35))                     # (pushed back into the night)
        look = prog(t, T["town"] - 0.3, T["town"])
        clap = None
        if T["claps"] - 0.25 <= t < T["s1"] - 0.3:
            clap = (5, prog(t, T["claps"] - 0.25, T["claps"]))
        crowd(c, 430, 880, t, look, 4, clap)
        # the firing desk, far from the tubes
        desk = t >= s("fix4") - 0.2
        if desk:
            dk = e_back(prog(t, s("fix4") - 0.2, s("fix4") + 0.2))
            box(c, -640, -150 * dk, 22, 150 * dk, "#475569", r=3)                    # blast shield
            box(c, -590, -62 * dk, 150 * dk, 10, "#7C4A2D", r=3)
            c.drawRect(R(-578, -52 * dk, 8, 52 * dk), P("#5B3A22"))
            c.drawRect(R(-460, -52 * dk, 8, 52 * dk), P("#5B3A22"))
            c.drawRRect(rr(-556, -62 - 62 * dk, 84 * dk, 56 * dk, 5), P("#0B1220"))  # the laptop
            vrect(c, -551, -57 - 62 * dk, 74 * dk, 46 * dk, ["#0F2A3F", "#0B1626"])
            for i in range(6):
                on = any(abs(t - b) < 0.12 for b in self.beats) and i % 2 == 0
                c.drawRect(R(-546 + i * 12, -30 - 62 * dk - (14 + 10 * (i % 3)) * dk, 7, (14 + 10 * (i % 3)) * dk), P(GOLDC if on else ACCENT, 0.9))
            add_glow(c, -515, -100, 90, "#7DD3FC", 0.35 * dk)
            c.drawCircle(-460, -70 * dk, 13 * dk, P("#FF4D4F"))                      # the one button
            add_glow(c, -460, -70 * dk, 30, "#FF4D4F", 0.6 * dk)
        # the tubes
        rack = t >= s("break4") - 0.12 or (s("break3") - 0.1 <= t and self.mode(t) == "field")
        wide_only = t >= s("break3") - 0.1
        if rack or wide_only:
            for i, tx in enumerate(TUBES):
                tube(c, tx, 0.62)
            wired = prog(t, T["electric"] - 0.1, T["electric"] + 0.5)
            if wired > 0:                                                            # an electric match on every shell
                for i, tx in enumerate(TUBES):
                    wk = clamp(wired * len(TUBES) - i)
                    if wk > 0:
                        c.drawLine(tx, -90 * wk, tx, -6, P("#EF4444", 0.9, stroke=3))
                        c.drawCircle(tx, -92 * wk, 4, P(GOLDC))
                c.drawLine(TUBES[-1], -6, lerp(TUBES[-1], -466, wired), -6, P("#EF4444", 0.9, stroke=4))
                c.drawLine(-466, -6, -466, lerp(-6, -56, prog(t, T["electric"] + 0.5, T["electric"] + 0.9)), P("#EF4444", 0.9, stroke=4))
        else:
            self.one_tube(c, t)
        # shells on their way up, and their bursts
        for k, (t0, tx, ax, ay, col, shape, rot, rad) in enumerate(self.shows):
            u = prog(t, t0, t0 + 0.95)
            if 0 < u < 1:
                e_ = 1 - (1 - u) ** 2
                sx, sy = lerp(tx, ax, e_), lerp(-100, ay, e_)
                c.drawLine(sx, sy, sx - (ax - tx) * 0.05, sy + 70 * (1 - u) + 14, P("#FFD9A0", 0.7, stroke=4))
                add_glow(c, sx, sy, 22, "#FFB347", 0.9)
                c.drawCircle(sx, sy, 5, P("#FFF3C4"))
            if 0 <= t - t0 < 0.5 and (rack or wide_only):
                add_glow(c, tx, -100, 70, "#FFB347", 0.8 * (1 - (t - t0) / 0.5))
                v2.smoke(c, tx, -96, t, t0, t0 + 0.1, rate=40, life=1.0, spread=(50, -120), rise=-60, size=(10, 40), col="#8B93A8",
                         lit="#FF8A3D", lit_until=0.3, seed=k, a=0.7)
            burst(c, ax, ay, t, t0 + 0.95, col, rad, 44 if shape != "heart" else 54, shape, rot, 2.3, seed=k + 1)
        self.people(c, t)
        c.restore()
        self.ui["cam"] = cam

    def one_tube(self, c, t):
        """Hook, fix 1 and break 2: the party popper, then one mortar tube cut open, its shell and its lift charge."""
        T, s = self.T, self.tl.s
        if t < s("break1") - 0.1:
            return
        if t < s("fix1") - 0.12:
            return
        tk = e_back(prog(t, s("fix1") - 0.1, s("fix1") + 0.25))
        again = t >= s("break2") - 0.1
        fired = T["bang1"] if not again else T["flies"] - 0.35
        c.save()
        c.scale(tk, tk)
        tube(c, 0, 1.0, cut=True)
        if t < fired:                                                                # the lift charge, waiting at the bottom
            c.drawRRect(rr(-20, -30, 40, 22, 8), P("#2B3248"))
            c.drawLine(-12, -30, -12, -36, P(GOLDC, 1, stroke=2))
            c.drawLine(16, -24, 30, -150, P("#EAB308", 0.8, stroke=2))               # the quick match up the side
        c.restore()
        if not again:
            if t < T["lowers"] - 0.1:                                                # held up for everyone to see
                pk = e_back(prog(t, T["crew"] + 0.1, T["shell"] - 0.1))
                shell_ball(c, -96, -176, 24 * pk, t, 0.0)
            elif t < fired:
                u = e_io(prog(t, T["lowers"] - 0.1, T["tube"] + 0.1))
                x = lerp(-96, 0, clamp(u * 2.2))
                y = lerp(-176, -210, clamp(u * 2.2)) if u < 0.45 else lerp(-210, -54, e_in(clamp((u - 0.45) / 0.55)))
                shell_ball(c, x, y, 24, t, 0.0)
            else:
                u = prog(t, fired, fired + 0.75)
                y = lerp(-54, -1500, 1 - (1 - u) ** 2)
                shell_ball(c, 0, y, 24, t, 1.0)
                c.drawLine(0, y + 26, 0, y + 26 + 130 * (1 - u), P("#FFD9A0", 0.8, stroke=7))
        if t >= fired:
            dt = t - fired
            if dt < 0.5:
                add_glow(c, 0, -40, 260 * (1 - dt / 0.5) + 60, "#FFB347", 0.95 * (1 - dt / 0.5))
            v2.flame(c, 0, -150, 36, 240, t, clamp(1 - dt / 0.35), seed=4, ang=270)
            v2.smoke(c, 0, -150, t, fired, fired + 0.25, rate=44, life=1.6, spread=(150, -200), rise=-80, size=(18, 80), col="#8B93A8",
                     lit="#FF8A3D", lit_until=0.4, seed=7, a=0.8)
            v2.embers(c, 0, -150, t, fired, 0.9, n=26, speed=620, seed=5, cone=(240, 300))
        if again:
            if fired <= t < T["low0"]:
                u = prog(t, fired, T["low0"])
                shell_ball(c, 0, lerp(-54, -372, 1 - (1 - u) ** 2), 22, t, 1.0)
            burst(c, 0, -372, t, T["low0"], "#FFE9B8", 300, 40, "ball", 0, 1.6, seed=3)
            if T["low0"] <= t < T["low0"] + 0.5:
                add_glow(c, 0, -372, 700, "#FFFFFF", 0.7 * (1 - (t - T["low0"]) / 0.5))

    def people(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        if t < s("break1") - 0.1 or (s("break1") - 0.1 <= t < s("fix1") - 0.12):       # the hook: one party popper
            xs = (-222, -150, -78)
            popped = t >= T["pop"]
            self.crew(c, t, "stand" if not popped else "cheer" if t < s("break1") + 0.6 else "look", xs=xs, face=1, h=112)
            hx, hy = -112, -126
            cone = skia.Path()
            cone.moveTo(hx, hy)
            cone.lineTo(hx + 44, hy - 44)
            cone.lineTo(hx + 54, hy - 28)
            cone.close()
            c.drawPath(cone, lin_paint(hx, 0, hx + 54, 0, ["#F472B6", "#FDE047"]))
            if popped:
                fx.confetti  # noqa: B018  (the big confetti is for the closer; this one is small on purpose)
                rng = random.Random(6)
                age = t - T["pop"]
                for i in range(22):
                    a = math.radians(rng.uniform(-80, -10))
                    sp = rng.uniform(140, 420)
                    px = hx + 50 + math.cos(a) * sp * age * math.exp(-age * 0.8)
                    py = hy - 36 + math.sin(a) * sp * age * math.exp(-age * 0.8) + 170 * age * age
                    if py < -2 and age < 3.5:
                        c.save()
                        c.translate(px, py)
                        c.rotate(age * rng.uniform(200, 500))
                        c.drawRect(R(-5, -3, 10, 6), P(rng.choice([REDC, GOLDC, BLUEC, GREENC, PINKC]), clamp(3.5 - age)))
                        c.restore()
                if age < 0.25:
                    add_glow(c, hx + 50, hy - 36, 70, "#FFFFFF", 0.8 * (1 - age / 0.25))
            return
        if t < s("fix2") - 0.12:                                                     # fix 1 and break 2: beside the tube
            again = t >= s("break2") - 0.1
            soot = clamp((t - T["low0"]) * 3) if again else 0.0
            if again:
                pose = "look" if t < T["low0"] else "duck" if t < T["low0"] + 0.7 else "shrug"
            else:
                pose = "stand" if t < T["lowers"] - 0.1 else "point" if t < T["bang1"] else "look"
            xs = (-250, -180, -110)
            for i, (px, col) in enumerate(zip(xs, SHIRTS)):
                carry = (not again) and i == 2 and t < T["tube"] + 0.1
                engineer(c, px, 0, 112 + (i % 2) * 8, col, t + i * 0.37, "carry" if carry else pose if not (pose == "point" and i != 1) else "look", soot, face=1)
                if soot > 0.5 and t < s("fix2"):
                    v2.smoke(c, px, -130, t, T["low0"] + 0.3, None, rate=5, life=1.2, spread=(16, -30), rise=-60, size=(8, 22), col="#6B7385",
                             lit=None, lit_until=0, seed=20 + i, a=0.6)
            return
        if s("break4") - 0.12 <= t < T["fires"] - 0.3:
            if t < s("fix4") - 0.1:                                                  # break 4: a thousand fuses, by hand
                u = prog(t, self.lit[0] - 0.3, self.lit[-1] + 0.2)
                rx = lerp(TUBES[0] - 40, TUBES[8] - 10, u)
                engineer(c, rx, 0, 118, SHIRTS[1], t * 1.6, "walk" if 0 < u < 1 else "duck", clamp(u * 0.7), face=1)
                if 0 < u < 1:
                    add_glow(c, rx + 30, -70, 26, "#FFB347", 0.9)
                    c.drawCircle(rx + 30, -70, 4, P("#FFF3C4"))
                for i, tl_ in enumerate(self.lit):
                    if tl_ <= t < tl_ + 0.25:
                        sparks_shower(c, TUBES[i + 1], -96, t, tl_, 0.3, n=8, speed=260, seed=i)
                self.crew(c, t, "look" if t < T["thousand"] else "shrug", xs=(-450, -410, -370), face=1, h=104)
            else:                                                                    # fix 4: everyone behind the desk
                self.crew(c, t, "stand" if t < T["computer"] else "point", xs=(-700, -560, -510), face=1, h=108)
            return
        if t >= T["fires"] - 0.3:
            pose = "cheer" if (T["beat"] <= t < s("cta") or t >= s("closer") - 0.1) else "look"
            xs = (-700, -560, -510)
            self.crew(c, t, pose, xs=xs, face=1, h=108)
            if t >= s("closer") - 0.1:
                hats_in_the_air(c, xs, -150, t, T["cong2"])
            if T["music"] <= t:                                                      # music, from two towers of speakers
                for sd, sx in ((-1, -420), (1, 420)):
                    box(c, sx - 26, -150, 52, 150, "#161B36", r=5)
                    for j in range(3):
                        c.drawCircle(sx, -122 + j * 44, 15 + 2 * math.sin(t * 20 + j), P("#3B4A8C"))
                for i in range(6):
                    u = ((t - T["music"]) * 0.5 + i / 6) % 1.0
                    sd = -1 if i % 2 else 1
                    nx, ny = sd * (420 + 60 * u) + math.sin(u * 8 + i) * 16, -170 - 240 * u
                    col = (GOLDC, "#67E8F9", PINKC)[i % 3]
                    c.drawOval(R(nx - 10, ny - 7, 20, 14), P(col, 1 - u))
                    c.drawLine(nx + 9, ny, nx + 9, ny - 34, P(col, 1 - u, stroke=4))

    # ------------------------------------------------------------------ set: one shell, cut open
    def draw_shell(self, c, t):
        T, s = self.T, self.tl.s
        v2.sky(c, W, H, 0.55, horizon_y=H * 1.3)
        v2.stars(c, W, H, t, 0.9)
        rising = t < s("break3")
        if rising:
            v2.speed_streaks(c, W, H, t, 0.35, ang=90, seed=3, n=26)
        cx, cy, r = 540, 760, 300
        gone = rising and t >= T["apex"]
        if gone:
            dt = t - T["apex"]
            c.drawRect(R(0, 0, W, H), P("#FFFFFF", clamp(1 - dt / 0.25)))
            burst(c, cx, cy, t, T["apex"], "#FFE9B8", 520, 40, "ball", 0, 2.0, seed=2)
            return
        pop = e_back(prog(t, s("fix2") - 0.1, s("fix2") + 0.2)) if rising else 1.0
        c.save()
        c.translate(cx, cy + (math.sin(t * 9) * 5 if rising else 0))
        c.scale(pop, pop)
        c.drawCircle(0, 0, r, rad_paint(-90, -110, r * 1.6, [shade(SHELLC, 0.3), SHELLC, shade(SHELLC, -0.45)]))       # paper shell, cut open
        c.drawCircle(0, 0, r - 26, rad_paint(0, 0, r, ["#3A2A1E", "#2A1E16", "#1B1410"]))
        c.drawCircle(0, 0, r - 26, P("#E9C39A", 0.5, stroke=4))
        # the burst charge in the middle
        core = 86
        c.drawCircle(0, 0, core, rad_paint(-20, -24, core * 1.5, ["#4B5563", "#1F2937", "#0B0F17"]))
        rng = random.Random(4)
        for _ in range(40):
            a, rr_ = rng.uniform(0, 6.283), rng.uniform(0, core - 8)
            c.drawCircle(math.cos(a) * rr_, math.sin(a) * rr_, rng.uniform(2, 4), P("#6B7280"))
        # the stars
        if not rising:
            hearted = e_io(prog(t, T["arrange"] - 0.05, T["arrange"] + 0.6))
            n = 26
            for i in range(n):
                pk = e_back(clamp((t - T["pellets"] + 0.1) / 0.6 * n - i)) if t < T["strontium"] else 1.0
                a = 2 * math.pi * i / n
                bx, by = math.cos(a) * 182, math.sin(a) * 182
                hx, hy = heart_pt(a)
                x, y = lerp(bx, hx * 196, hearted), lerp(by, hy * 196 - 14, hearted)
                col = (REDC, GREENC, BLUEC)[i % 3] if hearted < 0.5 else PINKC
                if pk > 0:
                    c.drawCircle(x, y, 19 * pk, rad_paint(x - 6, y - 7, 30, ["#FFFFFF", col, shade(col, -0.5)]))
        # the time fuse: from the outside to the middle
        if rising:
            fk = self.fuse.at(t)
            path = skia.Path()
            path.moveTo(0, r + 44)
            path.lineTo(0, core - 6)
            c.drawPath(path, P("#0B0F17", 1, stroke=30))
            c.drawPath(path, P("#D6C29A", 1, stroke=18))
            if fk > 0:
                by_ = lerp(r + 44, core - 6, fk)
                c.drawLine(0, r + 44, 0, by_, P("#3A2A1A", 1, stroke=18))
                add_glow(c, 0, by_, 70, "#FFB347", 0.95)
                c.drawCircle(0, by_, 9, P("#FFF3C4"))
                v2.embers(c, 0, by_, t, t - (t % 0.12), 0.4, n=6, speed=260, seed=int(t * 8), cone=(30, 150))
            self.ui["fuse"] = (cx, cy + lerp(r + 44, core - 6, fk) * pop)
        c.restore()

    # ------------------------------------------------------------------ set: under the bed
    def draw_bed(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#151A33", "#1E2547", "#0E1226"], [0.0, 0.6, 1.0])
        cam = (20, -196, 1.7)
        self.view(c, cam)
        fl = max(0.0, math.sin(t * 5.3)) ** 6                                         # the show goes on outside
        window_night(c, 70, -600, 190, 180, t)
        add_glow(c, 165, -510, 300, (GOLDC, PINKC, BLUEC)[int(t * 1.6) % 3], 0.5 * fl)
        box(c, -700, 0, 1400, 30, "#3B2F52")
        c.drawRect(R(-700, 0, 1400, 4), P("#FFFFFF", 0.12))
        c.drawRRect(rr(-210, -520, 80, 60, 6), P("#F8FAFC"))                          # a calendar on the wall
        c.drawRect(R(-210, -520, 80, 16), P("#EF4444"))
        for j in range(3):
            c.drawRect(R(-200, -494 + j * 11, 60, 4), P("#94A3B8"))
        # the bed
        box(c, -330, -330, 34, 330, "#5B3A22", r=8)
        box(c, 300, -250, 30, 250, "#5B3A22", r=8)
        c.drawRect(R(-300, -8, 600, 8), P("#000000", 0.0))
        vrect(c, -300, -128, 600, 128, [("#05060F", 0.95), ("#0B0E1F", 0.95)])        # the dark under it
        box(c, -310, -200, 630, 76, "#E2E8F0", r=16)
        c.drawRRect(rr(-310, -230, 630, 60, 22), P("#7C3AED"))
        c.drawRRect(rr(-296, -262, 150, 56, 24), P("#F8FAFC"))
        for bx in (-286, 286):
            c.drawRect(R(bx - 8, -128, 16, 128), P("#5B3A22"))
        # the dog: two eyes, a nose, a tail that cannot keep still
        shiver = math.sin(t * 34) * 3
        ex = 40 + shiver
        for sd in (-1, 1):
            c.drawOval(R(ex + sd * 26 - 13, -84, 26, 30), P("#FDE68A"))
            c.drawCircle(ex + sd * 26 + 2 * math.sin(t * 2), -66, 7, P("#0B0F17"))
        c.drawOval(R(ex - 9, -44, 18, 12), P("#111827"))
        c.drawLine(-150 + shiver, -30, -200 + shiver * 2, -52 - abs(shiver) * 2, P("#B7803F", 1, stroke=12))
        for j in range(2):
            u = (t * 1.2 + j * 0.5) % 1.0
            c.drawArc(R(ex - 70 - 30 * u, -110 - 30 * u, 140 + 60 * u, 110 + 60 * u), 200, 140, False, P("#FFFFFF", 0.35 * (1 - u), stroke=3))
        c.restore()
        self.ui["cam"] = cam

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.4, horizon_y=H * 1.1)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -300, 1.0)), x, y)

    def ui_field(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        if tw < s("break1") - 0.1:
            x0, y0 = self.at(-80, -158)
            self.label(x0, y0, x0 + 250, y0 - 200, "popper", T["popper"] - 0.3, T["congrats"] + 0.4, HILITE)
        elif tw < s("fix1") - 0.12:
            self.badge("alert", T["town"], s("fix1") - 0.2)
            self.red(T["town"], 1.8)
        elif tw < s("break2") - 0.1:
            x0, y0 = self.at(-96, -196)
            if tw < T["lowers"] - 0.1:
                self.label(x0, y0, x0 + 30, y0 - 300, "shell", T["shell"] - 0.35, T["lowers"] - 0.15, HILITE)
            x1, y1 = self.at(28, -120)
            self.label(x1, y1, 800, y1 - 240, "tube", T["tube"] - 0.3, T["lift"] - 0.1)
            x2, y2 = self.at(18, -18)
            self.label(x2, y2, 790, y2 + 6, "lift", T["lift"] + 0.05, T["bang1"] + 0.1, "#FDBA74")
            self.badge("check", T["sky"], s("break2") - 0.15)
        elif tw < s("fix2") - 0.12:
            self.badge("alert", T["low0"], s("fix2") - 0.2)
            self.red(T["low0"], 2.0)
        elif tw < s("fix3") - 0.12:
            for i, key in enumerate(("nocol", "noshape", "nowow")):
                self.chip(250 + i * 290, 620 + (i % 2) * 90, key, T[("color", "shape", "wow")[i]] - 0.15, s("fix3") - 0.2, accent=WARN, size=34)
            self.badge("alert", T["color"] - 0.2, s("fix3") - 0.2, x=880, y=360)
            self.red(T["color"] - 0.2, 1.8)
        elif tw < s("break4") - 0.12:
            if tw < T["arrange"]:
                for i, key in enumerate(("red", "green", "blue")):
                    xx, yy = self.at(-330 + i * 330, -1180 - 60 * (i % 2) + 330)
                    t0 = (T["reds"], T["green"] - 0.1, T["blue"] - 0.1)[i]
                    self.chip(xx, yy, key, t0 + 0.15, T["arrange"] - 0.25, accent=(REDC, GREENC, BLUEC)[i], size=32)
            self.badge("check", T["hb1"] + 0.3, s("break4") - 0.15, x=880, y=1080)
        elif tw < T["fires"] - 0.3:
            if tw < s("fix4") - 0.1:
                p = self.span(T["light"] - 0.4, s("fix4") - 0.2)
                if p > 0:
                    done = sum(1 for l in self.lit if tw >= l)
                    v2.gauge(c, 60, 250, [(self.L["lit"], done / 300.0 + 0.004, WARN)], p, w=360)
                self.badge("alert", T["thousand"], s("fix4") - 0.2, x=880, y=330)
                self.red(T["thousand"], 1.8)
            else:
                x0, y0 = self.at(TUBES[5], -92)
                self.label(x0, y0, x0 + 30, y0 - 300, "match", T["electric"] + 0.15, T["computer"] - 0.5, REDC)
                x1, y1 = self.at(-515, -150)
                self.label(x1, y1, x1 + 60, y1 - 250, "comp", T["computer"] + 0.1, T["fires"] - 0.35, "#7DD3FC")
        elif tw < s("cta"):
            p = self.span(T["fires"] - 0.1, s("cta") + 0.2)
            if p > 0:                                                                # the beat, as dots along the top
                n = len(self.beats)
                for i, b in enumerate(self.beats):
                    x = 540 + (i - (n - 1) / 2) * 110
                    hit = clamp(1 - abs(tw - b) / 0.22) if tw >= b - 0.05 else 0.0
                    c.drawCircle(x, 300, 20 + 14 * hit, P(mix("#334155", HILITE, 1.0 if tw >= b else 0.0), p))
                    if hit > 0:
                        add_glow(c, x, 300, 70, HILITE, 0.8 * hit * p)
                v2.chip(c, 540, 380, self.L["beat"], p * prog(tw, self.beats[0] - 0.1, self.beats[0] + 0.15), size=34, accent=HILITE)
            self.badge("check", T["beat"], 1e9, x=880, y=520)
        elif s("reveal") <= tw < T["s1"] - 0.4:
            x0, y0 = self.at(800, -110)
            self.label(x0, y0, x0 - 60, y0 - 300, "far", T["crowd"] + 0.1, T["guy"] - 0.1)
            x1, y1 = self.at(690, -170)
            self.label(x1, y1 - 20, x1 - 200, y1 - 330, "early", T["claps"] + 0.1, T["s1"] - 0.5, HILITE)

    def ui_shell(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break3"):
            if tw < T["apex"]:
                fx_, fy_ = self.ui.get("fuse", (540, 1000))
                self.label(fx_ + 16, fy_, 830, fy_ + 90 if fy_ < 1000 else fy_ - 60, "fuse", T["fuse"] - 0.15, T["burst"] - 0.2, "#FDBA74")
                self.label(540 + 40, 760 - 40, 820, 430, "burstc", T["burst"] - 0.1, T["apex"] - 0.02, HILITE)
            self.badge("check", T["apex"] + 0.2, s("break3") - 0.15, x=880, y=360)
        else:
            self.label(540 + 182, 760, 850, 400, "stars", T["stars"] - 0.2, T["strontium"] - 0.35, HILITE)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["pop"], sfx.snap(61), -2), (T["pop"] + 0.02, sfx.pop(62), -4),
              (T["congrats"] + 0.1, sfx.sparkle(0.6, 8, 63), -10)]
        ev += [(s("break1") - 0.1, sfx.whoosh(0.5, False, 64), -6), (T["town"], sfx.alarm(3, 820), -11), (T["watching"] + 0.3, sfx.womp(), -9)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (s("fix1"), sfx.clank(300, 0.3, 66), -6), (T["shell"] - 0.3, sfx.pop(67), -6),
               (T["tube"] + 0.1, sfx.thud(0.25, 68), -5), (T["lift"], sfx.pop(69), -7), (T["bang1"], thump(0.6, 70), 0), (T["bang1"] + 0.05, whistle(0.8), -9),
               (T["sky"], sfx.chime(), -7)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, False, 71), -4), (T["flies"] - 0.35, thump(0.5, 72), -3), (T["low0"], boom(1.2, 73), 0),
               (T["low0"] + 0.1, crackle(1.0, 74), -6), (T["low0"] + 0.15, sfx.alarm(3, 820), -10), (T["eyebrows"] + 0.2, sfx.sizzle(0.6, 75), -8)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 76), -4), (T["burns"] - 0.1, sfx.sizzle(max(0.8, T["apex"] - T["burns"]), 77), -9),
               (T["burst"], sfx.pop(78), -7), (T["apex"], boom(1.3, 79), -1), (T["apex"] + 0.25, sfx.chime(), -7)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 80), -5), (T["dull"] - 0.95, thump(0.5, 81), -6), (T["dull"], boom(0.9, 82), -3),
               (T["color"] - 0.15, sfx.buzz(0.25), -10), (T["shape"] - 0.15, sfx.buzz(0.25), -10), (T["wow"] - 0.15, sfx.buzz(0.3), -9)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 83), -4)]
        ev += [(T["pellets"] - 0.1 + i * 0.05, sfx.tap(84 + i), -11) for i in range(10)]
        ev += [(T["strontium"] - 0.3, sfx.whoosh(0.35, False, 95), -6), (T["arrange"] - 0.2, sfx.whoosh(0.35, True, 96), -6),
               (T["arrange"], sfx.sparkle(0.6, 8, 97), -9), (T["hb1"] - 0.5, sfx.whoosh(0.35, False, 98), -6), (T["hb1"] + 0.3, sfx.chime(), -8)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 99), -5), (T["thousand"], sfx.alarm(3, 820), -11)]
        ev += [(l, sfx.sizzle(0.25, 100 + i), -9) for i, l in enumerate(self.lit)]
        ev += [(T["electric"] - 0.1 + i * 0.045, sfx.click(110 + i), -10) for i in range(11)]
        ev += [(T["computer"] - 0.45, sfx.whoosh(0.5, True, 122), -8), (T["computer"], sfx.beep(1500, 0.07), -8), (T["computer"] + 0.12, sfx.beep(1900, 0.07), -8),
               (T["fires"] - 0.3, sfx.whoosh(0.4, False, 123), -5), (T["beat"], sfx.chime(), -7)]
        ev += [(b, sfx.tick(), -6) for b in self.beats]
        for k, (t0, tx, ax, ay, col, shape, rot, rad) in enumerate(self.shows):       # every shell: thump up, boom, crackle
            far = t0 >= s("cta")
            ev += [(t0, thump(0.4, 130 + k), -9 if far else -6), (t0 + 0.95, boom(0.9, 180 + k), -8 if far else -4)]
            if shape != "flash" and k % 2 == 0:
                ev.append((t0 + 1.05, crackle(0.9, 230 + k), -13 if far else -9))
        ev += [(T["pause"], sfx.click(300), 0), (T["follow"] - 0.15, sfx.pop(301), -4)]
        ev += [(T["music"], sfx.sparkle(0.9, 12, 302), -9), (T["claps"] + 0.34, sfx.tap(303), -5), (T["claps"] + 0.5, sfx.tap(304), -5),
               (T["claps"] + 0.66, sfx.tap(305), -5), (T["claps"] + 0.82, sfx.tap(306), -6), (T["claps"] + 1.0, sfx.womp(), -13)]
        ev += [(T["s1"], sfx.pop(307), -3), (T["s2"], sfx.pop(308), -3), (T["s3"], sfx.pop(309), -3)]
        ev += [(T["cong2"], sfx.pop(310), -2), (T["cong2"], sfx.sparkle(1.0, 14, 311), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 312), -6), (T["dog"] + 0.1, boom(0.7, 313), -14), (T["bed"], boom(0.7, 314), -15),
               (T["bed"] + 0.2, sfx.creak(0.3, 315), -8), (T["tuesday"] + 0.3, sfx.womp(), -3)]
        return ev


NAME = "fireworks"
EPISODE = Fireworks
