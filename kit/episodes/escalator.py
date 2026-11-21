"""Episode 56 - An escalator.  v2 look: a mall cut open, the step loop, close-ups of the wheels, the comb and the rail.

Sets: mall (hook: people ride up while an x-ray shows half the steps riding back upside down under them; fix1: the loop
of steps on a chain, pulled round by the motor at the top; closer at night), stairs (break1: someone climbing stairs,
out of breath, and a lift that takes three at a time), wheels (break2: stairs that come out of the floor already as
stairs trip a foot; fix2: two pairs of wheels on two tracks, level at the ends so the steps flatten), comb (break3: from
above, the steps slide under the floor plate and pull a shoelace in; fix3: the comb's teeth sit in the step grooves and
lift it off), rail (break4: the handrail runs slower and the rider tips back; fix4: one motor drives both, same speed),
harrods (reveal: London 1898, the first one scares a shopper, staff wait at the top), long (stat: half a metre a second,
Moscow's 126 m escalator and Japan's five-step one), tag (EN: riding up to the gym to climb the stair machine; AR:
grandma waiting at the bottom for a step to stop).
World (mall): side view, the lower floor at y = 0, the upper floor at y = -420, 30 degree incline.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of  # noqa: E402
from panama import word  # noqa: E402
from phone import mini_clock  # noqa: E402

XA, XS = -460.0, -380.0                        # lower flat start, incline start
RISE = 420.0
XE = XS + RISE / math.tan(math.radians(30))    # incline end (about 347)
XB = XE + 80.0                                 # upper flat end
D = 44.0                                       # step depth
LTOP = XB - XA
TURN = 60.0
LOOP = 2 * LTOP + 2 * TURN
NSTEP = int(LOOP / D)
V = 58.0                                       # step speed, world units per second
RET = 95.0                                     # the return run hangs this far below
STEEL, STEEL_D, GROOVE = "#9AA3B2", "#5B6372", "#3F4654"
MALL = {"top": "#0B1230", "upper": "#1A2350", "mid": "#2E3A6A", "low": "#4A4F7A", "horizon": "#6A6A8A",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}


def ypass(x):
    """Height of the passenger side (tread tops) at x."""
    if x <= XS:
        return 0.0
    if x >= XE:
        return -RISE
    return -RISE * (x - XS) / (XE - XS)


def steps_at(t, speed=V):
    """[(kind, x)] for every step: kind "top" (x = its left edge, moving right) or "ret" (moving left)."""
    out = []
    for k in range(NSTEP):
        ph = (t * speed + k * (LOOP / NSTEP)) % LOOP
        if ph < LTOP - D:
            out.append(("top", XA + ph))
        elif LTOP + TURN <= ph < 2 * LTOP + TURN - D:
            out.append(("ret", XB - D - (ph - LTOP - TURN)))
    return out


def step_top(c, x, a=1.0, hi=0.0, yfun=ypass):
    yt = yfun(x + D)
    yb = yfun(x)
    c.drawRect(R(x + 1, yt - 8, D - 2, 12), lin_paint(0, yt - 8, 0, yt + 4, [mix(STEEL, HILITE, hi), STEEL_D], a=a))
    for g in range(5):
        c.drawLine(x + 6 + g * 8, yt - 7, x + 6 + g * 8, yt + 2, P(GROOVE, 0.7 * a, stroke=2))
    c.drawRect(R(x + 1, yt - 8, 4, 4), P("#FACC15", a))
    c.drawRect(R(x + D - 5, yt - 8, 4, 4), P("#FACC15", a))
    if yb - yt > 1:                                                   # the riser
        c.drawRect(R(x, yt + 4, 5, yb - yt - 4), P(STEEL_D, a))
        c.drawRect(R(x + 5, yt + 4, D - 6, yb - yt - 4), P("#2A2F3A", 0.85 * a))


def step_ret(c, x, a=1.0, hi=0.0):
    yr = ypass(x + D) + RET
    c.drawRect(R(x + 1, yr - 2, D - 2, 12), lin_paint(0, yr, 0, yr + 10, [STEEL_D, mix("#3A404C", HILITE, hi)], a=a))
    for g in range(5):
        c.drawLine(x + 6 + g * 8, yr + 6, x + 6 + g * 8, yr + 14, P(mix(GROOVE, HILITE, hi), a, stroke=2))
    if hi > 0:
        add_glow(c, x + D / 2, yr + 6, 26, HILITE, 0.35 * hi * a)


def truss_path():
    pts = [(XA - 30, ypass(XA) + 12)]
    for x in (XS, XE, XB + 30):
        pts.append((x, ypass(x) + 12))
    for x in (XB + 30, XE, XS, XA - 30):
        pts.append((x, ypass(x) + RET + 44))
    return path_of(pts, close=True)


def sprocket(c, x, y, r, ang, a=1.0, glow=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawCircle(0, 0, r, P("#4B5563", a))
    for k in range(10):
        c.save()
        c.rotate(k * 36)
        c.drawRect(R(-5, -r - 7, 10, 10), P("#6B7280", a))
        c.restore()
    c.drawCircle(0, 0, r * 0.35, P("#9CA3AF", a))
    c.restore()
    if glow > 0:
        add_glow(c, x, y, r * 2.2, HILITE, 0.4 * glow)


def rider(c, x, y, h, shirt, t, a=1.0, lean=0.0, pose="stand", face=1, hair="#2B2530", phone=False):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(lean)
    person(c, 0, 0, h, shirt, t, pose=pose, face=face, hat="none", hair=hair, a=a)
    if phone:
        u = h / 140.0
        c.drawRRect(rr(10 * u * face, -96 * u, 12 * u, 20 * u, 3 * u), P("#111827", a))
    c.restore()


def grandma(c, x, y, h, t, lean=0.0, a=1.0):
    """A grandmother in a grey headscarf with a handbag and a cane."""
    c.save()
    c.translate(x, y)
    c.rotate(lean)
    person(c, 0, 0, h, "#7C3AED", t, pose="stand", face=1, hat="none", hair="#9CA3AF", skin="#D9A57A", a=a)
    u = h / 140.0
    sc = skia.Path()
    sc.addCircle(0, -132 * u, 21 * u)
    c.drawPath(sc, P("#6B7280", a))
    c.drawCircle(4 * u, -128 * u, 12 * u, P("#D9A57A", a))
    c.drawRRect(rr(-20 * u, -116 * u, 40 * u, 16 * u, 8 * u), P("#6B7280", a))
    c.drawRRect(rr(-30 * u, -70 * u, 22 * u, 18 * u, 4 * u), P("#92400E", a))            # handbag
    c.drawLine(26 * u, -60 * u, 34 * u, 0, P("#78350F", a, stroke=4 * u))               # cane
    c.restore()


def storefront(c, x, y, w, h, col, t, a=1.0, lit=1.0):
    c.drawRect(R(x, y - h, w, h), P("#1E2440", a))
    c.drawRect(R(x + 10, y - h + 40, w - 20, h - 50), P(mix("#2A3358", "#FDE68A", 0.35 * lit), a))
    c.drawRect(R(x, y - h, w, 30), P(col, a))
    add_glow(c, x + w / 2, y - h + 15, w * 0.5, col, 0.25 * lit * a)


# ====================================================================================== the episode
class Escalator(EpisodeV2):
    BUILD_NO = 56
    FIRST_SET = "mall"
    CLEAR = "#0B1230"
    TITLE = {"en": "ESCALATOR", "ar_sa": "سلم كهربا"}
    EMPH = {"en": ["CONGRATS", "STAIRS", "CLIMB", "THEMSELVES", "HALF", "UPSIDE", "DOWN", "FLOOR", "ESCALATOR",
                   "YOURSELF", "WEAR", "ELEVATOR", "FEW", "LOOP", "CHAIN", "MOTOR", "HOP", "MOVING", "TRIP", "TWO",
                   "PAIRS", "WHEELS", "TRACKS", "LEVEL", "FLATTEN", "SLIDE", "SHOELACE", "COMB", "STEEL", "TEETH",
                   "GROOVES", "LIFT", "HANDRAIL", "SLOWER", "BACKWARDS", "SAME", "HAND", "FEET", "FOLLOW", "SYDNEY",
                   "OPERA", "LONDON'S", "EIGHTEEN", "NINETY-EIGHT", "SCARED", "STAFF", "BRANDY", "SMELLING", "SALTS",
                   "METER", "SECOND", "HUNDRED", "TWENTY-SIX", "MOSCOW", "JAPAN", "FIVE", "GYM", "STAIR", "MACHINE"],
            "ar_sa": ["مبروك", "السلم", "بيطلعك", "لوحده", "نص", "مقلوب", "الأرض", "كهربا", "بإيدك", "بيهد", "الحيل",
                      "الأسانسير", "كام", "حلقة", "جنزير", "موتور", "ينط", "ماشي", "هيتكعبل", "أربع", "عجل", "قضيبين",
                      "بيتساووا", "يفرد", "بيدخل", "رباط", "الجزمة", "مشط", "سنان", "حديد", "مجاري", "تشيل",
                      "الدرابزين", "أبطأ", "لورا", "نفس", "وإيدك", "رجلك", "تابعني", "سيدني", "لندن", "خض", "الموظفين",
                      "يفوقوا", "داخ", "متر", "موسكو", "اليابان", "خمس", "تيتة", "الصبح", "تقف"]}
    KEYS = {"ar_sa": {
        ("hook", "STAIRS"): "السلم", ("hook", "CLIMB"): "بيطلعك", ("hook", "HALF"): "نص", ("hook", "UPSIDE"): "مقلوب",
        ("hook", "FLOOR"): "الأرض", ("hook", "CONGRATS"): "مبروك", ("hook", "ESCALATOR"): "كهربا",
        ("break1", "WEAR"): "بيهد", ("break1", "ELEVATOR"): "الأسانسير", ("break1", "FEW"): "كام",
        ("fix1", "LOOP"): "حلقة", ("fix1", "CHAIN"): "جنزير", ("fix1", "MOTOR"): "موتور", ("fix1", "PULLS"): "بيلفها",
        ("break2", "HOP"): "ينط", ("break2", "MOVING"): "ماشي", ("break2", "TRIP"): "هيتكعبل",
        ("fix2", "TWO"): "أربع", ("fix2", "WHEELS"): "عجل", ("fix2", "TRACKS"): "قضيبين", ("fix2", "ENDS"): "الطرفين",
        ("fix2", "LEVEL"): "بيتساووا", ("fix2", "FLATTEN"): "يفرد",
        ("break3", "TOP"): "فوق", ("break3", "SLIDE"): "بيدخل", ("break3", "SHOELACE"): "رباط",
        ("fix3", "COMB"): "مشط", ("fix3", "TEETH"): "سنان", ("fix3", "GROOVES"): "مجاري", ("fix3", "LIFT"): "تشيل",
        ("break4", "HANDRAIL"): "الدرابزين", ("break4", "SLOWER"): "أبطأ", ("break4", "BACKWARDS"): "لورا",
        ("fix4", "SAME"): "نفس", ("fix4", "MOTOR"): "الموتور", ("fix4", "HAND"): "إيدك", ("fix4", "FEET"): "رجلك",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "LONDON"): "لندن", ("reveal", "EIGHTEEN"): "ألف", ("reveal", "SCARED"): "خض",
        ("reveal", "STAFF"): "الموظفين", ("reveal", "BRANDY"): "يفوقوا", ("reveal", "SMELLING"): "داخ",
        ("stat", "HALF"): "نص", ("stat", "HUNDRED"): "مية", ("stat", "MOSCOW"): "موسكو", ("stat", "JAPAN"): "اليابان",
        ("stat", "FIVE"): "خمس",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "RIDE"): "تيتة", ("tag", "GYM"): "واقفة", ("tag", "CLIMB"): "الصبح", ("tag", "STAIR"): "مستنية",
        ("tag", "MACHINE"): "تقف"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Sydney Opera House"),
                   "stat": [("0.5 m/s", "SPEED"), ("126 m", "MOSCOW METRO"), ("5", "STEPS IN JAPAN")],
                   "L": {"upside": "HALF RIDE BACK UPSIDE DOWN", "name": "AN ESCALATOR", "tired": "STAIRS WEAR YOU OUT",
                         "few": "A FEW AT A TIME", "loop": "A LOOP OF STEPS ON A CHAIN", "motor": "MOTOR AT THE TOP",
                         "trip": "YOU'D TRIP!", "wheels": "2 PAIRS OF WHEELS, 2 TRACKS", "flat": "TRACKS LEVEL: FLAT STEPS",
                         "lace": "SHOELACE!", "comb": "THE COMB", "lift": "TEETH IN THE GROOVES", "slow": "RAIL TOO SLOW",
                         "same": "ONE MOTOR, SAME SPEED", "london": "LONDON, 1898", "scared": "SCARED SHOPPERS",
                         "brandy": "BRANDY & SMELLING SALTS", "gym": "GYM", "machine": "STAIR MACHINE",
                         "steps_v": "STEPS", "rail_v": "RAIL"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: أوبرا سيدني"),
                      "stat": [("0.5", "متر في الثانية"), ("126", "متر في موسكو"), ("5", "درجات في اليابان")],
                      "L": {"upside": "نص الدرج راجع مقلوب", "name": "سلم كهربا", "tired": "السلم بيهد الحيل",
                            "few": "كام واحد بس", "loop": "حلقة درج على جنزير", "motor": "موتور فوق",
                            "trip": "هتتكعبل!", "wheels": "أربع عجل على قضيبين", "flat": "القضيبين بيتساووا: الدرج يفرد",
                            "lace": "رباط الجزمة!", "comb": "المشط", "lift": "سنان في المجاري", "slow": "الدرابزين أبطأ",
                            "same": "نفس الموتور، نفس السرعة", "london": "لندن، سنة 1898", "scared": "خضّ الناس",
                            "brandy": "يفوّقوا اللي داخ", "waiting": "مستنية الدرجة تقف", "grandma": "تيتة",
                            "steps_v": "الدرج", "rail_v": "الدرابزين"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stairs": ("hook", "STAIRS", 0.05), "climb": ("hook", "CLIMB", 0.15), "half": ("hook", "HALF", 0.3),
            "upside": ("hook", "UPSIDE", 0.45), "floor": ("hook", "FLOOR", 0.6), "congrats": ("hook", "CONGRATS", 0.7),
            "name": ("hook", "ESCALATOR", 0.92),
            "wear": ("break1", "WEAR", 0.25), "elevator": ("break1", "ELEVATOR", 0.6), "few": ("break1", "FEW", 0.8),
            "loop": ("fix1", "LOOP", 0.2), "chain": ("fix1", "CHAIN", 0.4), "motor": ("fix1", "MOTOR", 0.65),
            "pulls": ("fix1", "PULLS", 0.85),
            "hop": ("break2", "HOP", 0.2), "moving": ("break2", "MOVING", 0.45), "trip": ("break2", "TRIP", 0.75),
            "two": ("fix2", "TWO", 0.1), "wheels": ("fix2", "WHEELS", 0.25), "tracks": ("fix2", "TRACKS", 0.4),
            "ends": ("fix2", "ENDS", 0.6), "level": ("fix2", "LEVEL", 0.75), "flatten": ("fix2", "FLATTEN", 0.92),
            "top3": ("break3", "TOP", 0.1), "slide": ("break3", "SLIDE", 0.35), "lace": ("break3", "SHOELACE", 0.8),
            "comb": ("fix3", "COMB", 0.15), "teeth": ("fix3", "TEETH", 0.35), "grooves": ("fix3", "GROOVES", 0.65),
            "lift": ("fix3", "LIFT", 0.85),
            "rail": ("break4", "HANDRAIL", 0.2), "slower": ("break4", "SLOWER", 0.5), "back": ("break4", "BACKWARDS", 0.9),
            "same": ("fix4", "SAME", 0.1), "motor4": ("fix4", "MOTOR", 0.25), "feet": ("fix4", "FEET", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "london": ("reveal", "LONDON", 0.05), "e1898": ("reveal", "EIGHTEEN", 0.2), "scared": ("reveal", "SCARED", 0.45),
            "staff": ("reveal", "STAFF", 0.65), "brandy": ("reveal", "BRANDY", 0.8), "salts": ("reveal", "SMELLING", 0.92),
            "s1": ("stat", "HALF", 0.05), "s2": ("stat", "HUNDRED", 0.35), "moscow": ("stat", "MOSCOW", 0.55),
            "s3": ("stat", "JAPAN", 0.75), "five": ("stat", "FIVE", 0.9),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_ride": ("tag", "RIDE", 0.1), "t_gym": ("tag", "GYM", 0.35), "t_climb": ("tag", "CLIMB", 0.65),
            "t_stair": ("tag", "STAIR", 0.75), "t_mach": ("tag", "MACHINE", 0.9)})
        T["hand"] = self.w("fix4", "HAND", 0.7, nth=1 if self.lang == "en" else 0)
        T["few1"] = max(T["few"], T["elevator"]) + 0.1
        T["trip1"] = max(T["trip"], T["moving"]) + 0.1
        T["lace1"] = max(T["lace"], T["slide"]) + 0.1
        T["back1"] = max(T["back"], T["slower"]) + 0.1
        T["pulls1"] = max(T["pulls"], T["motor"]) + 0.2
        T["flat1"] = max(T["flatten"], T["level"]) + 0.2
        T["lift1"] = max(T["lift"], T["grooves"]) + 0.2
        T["feet1"] = max(T["feet"], T["hand"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "stairs", 1)
        self.cut(s("fix1") - 0.12, "mall", -1)
        self.cut(s("break2") - 0.12, "wheels", 1)
        self.cut(s("break3") - 0.12, "comb", -1)
        self.cut(s("break4") - 0.12, "rail", 1)
        self.cut(s("reveal") - 0.12, "harrods", -1)
        self.cut(s("stat") - 0.12, "long", 1)
        self.cut(s("closer") - 0.12, "mall", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        cm = Camera(-30, -200, 1.24)
        cm.key(0.1, -20, -195, 1.2, max(1.0, T["congrats"] - 0.2))
        cm.key(T["congrats"] - 0.1, -10, -190, 1.18, 0.6)
        cm.key(s("fix1") - 0.12, -10, -190, 1.18, 0.0)
        cm.key(s("closer") - 0.12, -10, -190, 1.16, 0.0).key(s("closer"), -10, -200, 1.2, max(1.0, e("closer") - s("closer")))
        self.cam = cm
        self.spans = [(T["few1"], T["pulls1"] + 0.3), (T["trip1"], T["flat1"] + 0.3), (T["lace1"], T["lift1"] + 0.3),
                      (T["back1"], T["feet1"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["few1"], 0.4, 6), (T["trip1"], 0.45, 9), (T["lace1"], 0.4, 7),
                       (T["back1"], 0.4, 8), (T["scared"], 0.3, 6), (s("closer") + 0.2, 0.35, 9), (T["t_mach"], 0.3, 6)]

    # ------------------------------------------------------------------ the mall (hook, fix1, closer)
    def mall_bg(self, c, t, night=0.0):
        vrect(c, 0, 0, W, H, [mix("#2A3358", "#121733", night), mix("#1C2242", "#0B0F24", night)])
        for k in range(5):                                                       # ceiling lights
            add_glow(c, 120 + k * 210, 210, 90, "#FFF1C9", 0.35)
            c.drawRect(R(90 + k * 210, 196, 60, 10), P("#FFF7E0", 0.9))

    def draw_mall(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        night = 1.0 if t >= s("closer") - 0.12 else 0.0
        self.mall_bg(c, t, night)
        self.view(c, cam)
        cols = ["#E11D48", "#2563EB", "#16A34A", "#F59E0B", "#9333EA"]
        for k in range(5):                                                       # shops on both floors
            storefront(c, -760 + k * 330, -RISE - 70, 290, 230, cols[k], t, lit=0.6 + 0.4 * night)
            storefront(c, -900 + k * 330, -10, 290, 260, cols[(k + 2) % 5], t, lit=0.6 + 0.4 * night)
        c.drawRect(R(XB - 10, -RISE, 900, 56), lin_paint(0, -RISE, 0, -RISE + 56, ["#CBD5E1", "#64748B"]))  # upper floor
        c.drawRect(R(XB - 10, -RISE - 70, 900, 70), P("#BFE6FF", 0.12))                                       # its glass rail
        c.drawLine(XB - 10, -RISE - 70, XB + 900, -RISE - 70, P("#E5E7EB", 0.8, stroke=5))
        xray = 1.0 if (s("fix1") - 0.12 <= t < s("break2") - 0.12) else \
            (e_io(prog(t, T["half"] - 0.4, T["half"] + 0.2)) * (1 - prog(t, T["name"] + 0.3, s("break1"))) if t < s("break1") else 0.0)
        hi = prog(t, T["upside"] - 0.3, T["upside"] + 0.2) * (1 - prog(t, T["congrats"], T["congrats"] + 0.4))
        if xray > 0:                                                             # inside: the chain loop, sprockets, motor
            ck = prog(t, T["chain"] - 0.3, T["chain"] + 0.2) if t >= s("fix1") - 0.12 else 0.0
            mk = prog(t, T["motor"] - 0.3, T["motor"] + 0.2) if t >= s("fix1") - 0.12 else 0.0
            loop_pts = [(XA - 10, 30), (XS, 30), (XE, -RISE + 30), (XB + 10, -RISE + 30)]
            ret_pts = [(XB + 10, -RISE + RET + 16), (XE, -RISE + RET + 16), (XS, RET + 16), (XA - 10, RET + 16)]
            for pts in (loop_pts, ret_pts):
                c.drawPath(path_of(pts), dash_paint(mix("#94A3B8", HILITE, ck), xray, 6 + 4 * ck, t * 1.5, 14, 10))
            sprocket(c, XB + 10, -RISE + 30 + RET / 2 - 6, RET / 2 + 4, t * 60, a=xray, glow=mk)
            sprocket(c, XA - 10, 30 + RET / 2 - 6, RET / 2 + 4, t * 60, a=xray)
            box(c, XB - 30, -RISE + 150, 150, 80, mix("#475569", "#B45309", mk), r=10, a=xray)
            if mk > 0:
                add_glow(c, XB + 45, -RISE + 190, 120, "#FDBA74", 0.5 * mk)
                c.drawLine(XB + 45, -RISE + 150, XB + 10, -RISE + 80, P("#111827", xray, stroke=8))
        for kind, x in steps_at(t):
            if kind == "top":
                step_top(c, x)
            elif xray > 0:
                step_ret(c, x, a=xray, hi=hi)
        c.save()                                                                 # the side panel (see-through in x-ray)
        c.drawPath(truss_path(), lin_paint(0, -RISE, 0, RET, ["#8A94A4", "#5B6372", "#3F4654"], a=1 - 0.85 * xray))
        c.drawPath(truss_path(), P("#E5E7EB", 0.5, stroke=3))
        c.restore()
        self.rail(c, t, speed=V)
        for k, (kk, shirt, hair) in enumerate(((5, "#EF4444", "#2B2530"), (13, "#22C55E", "#6B4226"), (21, "#3B82F6", "#111827"))):
            ph = (t * V + kk * (LOOP / NSTEP)) % LOOP
            if XS - 80 < XA + ph < XB + 160 and ph < LTOP + 160:
                x = XA + ph
                y = ypass(x + D) - 8 if x < XB else -RISE - 8
                a_ = clamp((x - XS + 80) / 80) * (1 - clamp((x - XB) / 160))
                rider(c, x + D / 2, y, 136, shirt, t + k, a=a_, hair=hair, phone=(k == 1))
        c.drawRect(R(-1400, 6, 3000, 1600), lin_paint(0, 0, 0, 500, ["#94A3B8", "#475569"], a=1 - 0.7 * xray))  # lower floor
        c.drawRect(R(-1400, 0, 3000, 8), P("#E5E7EB", 0.9))
        c.drawRect(R(XA - 60, -2, 90, 10), P("#FACC15", 0.9))                   # the comb plates
        c.drawRect(R(XB - 30, -RISE - 2, 70, 10), P("#FACC15", 0.9))
        c.restore()
        self.ui["cam"] = cam

    def rail(self, c, t, speed=V, lag=0.0, a=1.0):
        """The glass balustrade and the moving rubber handrail along the passenger side."""
        pts = [(XA - 20, -110), (XS, -110), (XE, -RISE - 110), (XB + 20, -RISE - 110)]
        glass_ = path_of(pts + [(XB + 20, -RISE - 10), (XE, -RISE - 10), (XS, -10), (XA - 20, -10)], close=True)
        c.drawPath(glass_, P("#BFE6FF", 0.14 * a))
        c.drawPath(path_of(pts), P("#111827", a, stroke=14))
        c.drawPath(path_of(pts), dash_paint("#4B5563", a, 6, t * speed / V * (1 - lag), 10, 22))

    def ui_mall(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "upside", T["half"] - 0.1, T["congrats"] - 0.1, accent=HILITE, size=40)
            self.chip(540, 300, "name", T["name"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)
        elif tw < s("break2") - 0.12:
            self.chip(540, 300, "loop", T["loop"] - 0.2, T["motor"] - 0.2, accent=HILITE, size=40)
            self.chip(540, 300, "motor", T["motor"] - 0.2, s("break2") - 0.15, accent="#FDBA74", size=44)
            self.badge("check", T["pulls1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ break1: stairs and a lift
    def draw_stairs(self, c, t):
        T = self.T
        self.mall_bg(c, t)
        cam = (0, -200, 1.15)
        self.view(c, cam)
        for k in range(12):                                                      # a plain staircase
            c.drawRect(R(-470 + k * 40, -k * 32 - 32, 40, k * 32 + 32), P(mix("#64748B", "#475569", k / 12.0)))
            c.drawRect(R(-470 + k * 40, -k * 32 - 32, 40, 6), P("#CBD5E1"))
        q = prog(t, self.tl.s("break1"), self.tl.s("fix1")) * 0.35
        k_ = int(q * 12)
        rider(c, -450 + k_ * 40 + 20, -k_ * 32 - 32, 120, "#F59E0B", t, pose="duck" if t > T["wear"] else "walk", face=1)
        if t > T["wear"]:
            for j in range(3):
                qq = (t * 1.4 + j / 3.0) % 1.0
                c.drawCircle(-430 + k_ * 40 + j * 10, -k_ * 32 - 150 + qq * 40, 5, P("#BAE6FD", 1 - qq))
        box(c, 150, -520, 260, 520, "#475569", r=8)                              # the lift
        ek = prog(t, T["elevator"] - 0.3, T["elevator"])
        dk = e_io(prog(t, T["few"] - 0.2, T["few1"] + 0.3))
        c.drawRect(R(170, -460, 220, 460), P("#1E293B"))
        for j in range(3):
            rider(c, 205 + j * 75, 0, 120, ("#EF4444", "#3B82F6", "#22C55E")[j], t + j, face=-1, a=ek)
        c.drawRect(R(170, -460, 110 * dk, 460), P("#94A3B8"))
        c.drawRect(R(390 - 110 * dk, -460, 110 * dk, 460), P("#94A3B8"))
        for j in range(6):                                                       # the queue
            rider(c, 470 + j * 70, 0, 116, ("#A855F7", "#F97316", "#14B8A6", "#E11D48", "#64748B", "#84CC16")[j],
                  t + j, face=-1, pose="shrug" if t > T["few1"] else "stand", a=ek)
        c.drawRect(R(-1000, 0, 2600, 1400), lin_paint(0, 0, 0, 500, ["#94A3B8", "#475569"]))
        c.restore()

    def ui_stairs(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "tired", T["wear"] - 0.2, T["elevator"] - 0.2, accent="#FDBA74", size=44)
        self.chip(540, 300, "few", T["elevator"] - 0.2, s("fix1") - 0.15, accent=WARN, size=46)
        self.badge("alert", T["few1"], s("fix1") - 0.2, x=920, y=420)
        self.red(T["few1"], 1.2)

    # ------------------------------------------------------------------ break2 / fix2: wheels and tracks
    def draw_wheels(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        self.mall_bg(c, t)
        cam = (XS + 10, -20, 2.6)
        self.view(c, cam)
        c.drawRect(R(XS - 600, 6, 1400, 800), lin_paint(0, 0, 0, 300, ["#94A3B8", "#475569"]))
        if not fixed:
            def ybad(x):                                                         # stairs all the way into the floor
                return -(x - (XS - 120)) * math.tan(math.radians(30))
            c.save()
            c.clipRect(R(XS - 600, -900, 1400, 906))
            for k in range(14):
                x = XS - 160 + ((t * V + k * D) % (14 * D)) - 2 * D
                step_top(c, x, yfun=ybad)
            c.restore()
            tk = prog(t, T["trip"] - 0.3, T["trip1"] + 0.2)
            rider(c, XS - 170 + 40 * tk, 0, 120, "#F59E0B", t, lean=38 * e_in(tk), pose="walk" if tk < 0.2 else "duck", face=1)
            if tk > 0.3:
                c.drawCircle(XS - 120, -20, 16, P(WARN, 0.8 * (1 - tk)))
        else:
            wk = prog(t, T["two"] - 0.3, T["wheels"] + 0.2)
            tk = prog(t, T["tracks"] - 0.3, T["tracks"] + 0.2)
            lk = prog(t, T["ends"] - 0.3, T["level"] + 0.3)
            xs = [XA - 10 + k * 8 for k in range(100)]
            if tk > 0:
                c.drawPath(path_of([(x, ypass(x) + 30) for x in xs]), P("#FACC15", tk, stroke=6))
                c.drawPath(path_of([(x, ypass(x + D - 16) + 30) for x in xs]), dash_paint("#22D3EE", tk, 6, t, 12, 8))
            for kind, x in steps_at(t):
                if kind != "top" or not (XS - 300 < x < XS + 300):
                    continue
                yt = ypass(x + D)
                step_top(c, x, hi=0.3 * lk if abs(x - XS) < 90 else 0.0)
                if wk > 0:
                    c.drawLine(x + D - 10, yt + 4, x + D - 10, yt + 30, P("#374151", wk, stroke=4))
                    c.drawLine(x + 10, yt + 4, x + 10, yt + 30, P("#374151", wk, stroke=4))
                    c.drawCircle(x + D - 10, yt + 30, 8, P("#FACC15", wk))
                    c.drawCircle(x + 10, yt + 30, 8, P("#22D3EE", wk))
            if lk > 0:
                c.drawRect(R(XS - 260, -30, 230, 70), P(GOOD, 0.18 * lk))
            rider(c, XS - 150 + 60 * prog(t, s("fix2"), s("break3")), 0 - 8, 120, "#F59E0B", t, face=1)
        c.restore()

    def ui_wheels(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "trip", T["moving"] - 0.1, s("fix2") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["trip1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["trip1"], 1.2)
            return
        self.chip(540, 300, "wheels", T["two"] - 0.2, T["ends"] - 0.2, accent=HILITE, size=38)
        self.chip(540, 300, "flat", T["ends"] - 0.2, s("break3") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["flat1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ break3 / fix3: the comb, from above
    def draw_comb(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        self.mall_bg(c, t)
        edge = 640
        sp = 150                                                                 # px per second, up the screen
        for k in range(9):                                                       # step plates moving up
            y0 = edge + ((k * 170 - t * sp) % (9 * 170))
            c.drawRect(R(180, y0, 720, 164), lin_paint(0, y0, 0, y0 + 164, [STEEL, STEEL_D]))
            for g in range(18):
                c.drawRect(R(196 + g * 38, y0 + 4, 16, 156), P(GROOVE, 0.75))
            c.drawRect(R(180, y0, 720, 8), P("#FACC15", 0.9))
        c.drawRect(R(0, 0, W, edge), lin_paint(0, 0, 0, edge, ["#64748B", "#94A3B8"]))       # the floor plate
        for g in range(14):
            c.drawLine(40 + g * 76, 260, 40 + g * 76, edge - 20, P("#7C8798", 0.6, stroke=4))
        if not fixed:
            c.drawRect(R(180, edge - 6, 720, 14), P("#0B0F1A"))                       # the gap
        else:
            ck = prog(t, T["comb"] - 0.3, T["comb"] + 0.2)
            c.drawRect(R(180, edge - 40, 720, 40), P("#FACC15", ck))                   # the comb and its teeth
            for g in range(18):
                tooth = path_of([(196 + g * 38, edge - 4), (212 + g * 38, edge - 4), (208 + g * 38, edge + 70),
                                 (200 + g * 38, edge + 70)], close=True)
                c.drawPath(tooth, P("#EAB308", ck))
        # the shoe and its lace riding up
        q = prog(t, s("break3") - 0.1, T["lace1"] + 0.3) if not fixed else prog(t, s("fix3") - 0.1, T["lift1"])
        sy = lerp(1250, edge + 120, e_out(q))
        if fixed:
            sy = lerp(1250, edge - 220, e_io(q))
        c.drawRRect(rr(480, sy - 150, 130, 260, 60), P("#F8FAFC"))                    # a sneaker from above
        c.drawRRect(rr(480, sy - 150, 130, 70, 40), P("#E11D48"))
        for j in range(4):
            c.drawLine(510, sy - 60 + j * 28, 580, sy - 60 + j * 28, P("#94A3B8", 1.0, stroke=5))
        lace = skia.Path()
        lace.moveTo(545, sy - 20)
        tip_y = sy - 140 - 40 * math.sin(t * 3)
        if not fixed:
            tip_y = min(tip_y, edge + 4) if q > 0.6 else tip_y
            if q > 0.85:
                tip_y = edge + 2
        lace.cubicTo(640, sy - 60, 560, sy - 120, 600, tip_y)
        c.drawPath(lace, P("#EF4444", 1.0, stroke=9))
        if not fixed and q > 0.85:
            add_glow(c, 600, edge, 90, WARN, 0.6)

    def ui_comb(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "lace", T["lace"] - 0.2, s("fix3") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["lace1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["lace1"], 1.2)
            return
        self.chip(540, 300, "comb", T["comb"] - 0.2, T["grooves"] - 0.2, accent=HILITE, size=48)
        self.chip(540, 300, "lift", T["grooves"] - 0.2, s("break4") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["lift1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ break4 / fix4: the handrail
    def draw_rail(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        self.mall_bg(c, t)
        rx = XS + 40 + (t - s("break4")) * V
        cam = (rx + 40, ypass(rx) - 150, 1.6)
        self.view(c, cam)
        for kind, x in steps_at(t):
            if kind == "top":
                step_top(c, x)
        c.drawPath(truss_path(), lin_paint(0, -RISE, 0, RET, ["#8A94A4", "#5B6372", "#3F4654"]))
        slow = 0.0 if fixed else prog(t, T["slower"] - 0.4, T["back1"])
        self.rail(c, t, lag=0.55 * slow)
        y = ypass(rx + D / 2) - 8
        lean = -24 * e_io(slow)
        rider(c, rx, y, 130, "#2563EB", t, lean=lean, face=1, pose="stand")
        hx = rx + 30 - 60 * slow
        hy = ypass(hx) - 110
        c.drawLine(rx + 10 + lean * 1.5, y - 96, hx, hy, P("#E8B48A", 1.0, stroke=9))
        c.drawCircle(hx, hy, 9, P("#E8B48A"))
        c.restore()
        for j, (lab, val) in enumerate((("steps_v", 1.0), ("rail_v", 1.0 - 0.45 * slow))):
            col = GOOD if (fixed or j == 0) else mix(GOOD, WARN, slow)
            v2.chip(c, 290 + j * 500, 1110, f"{self.L[lab]} {0.5 * val:.1f} m/s" if not self.rtl else
                    f"{self.L[lab]} {0.5 * val:.1f}", 1.0, accent=col, size=34)
        if fixed:
            mk = prog(t, T["same"] - 0.2, T["motor4"] + 0.3)
            if mk > 0:                                                           # one motor, two belts
                c.drawCircle(540, 560, 70 * mk, P("#B45309", mk))
                add_glow(c, 540, 560, 140, "#FDBA74", 0.5 * mk)
                arrow(c, 540, 560, 290, 1060, HILITE, a=mk, w=8, head=20)
                arrow(c, 540, 560, 790, 1060, HILITE, a=mk, w=8, head=20)

    def ui_rail(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "slow", T["slower"] - 0.2, s("fix4") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["back1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["back1"], 1.2)
            return
        self.chip(540, 300, "same", T["same"] - 0.2, s("cta") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["feet1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ reveal: London 1898
    def draw_harrods(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#3A1A1A", "#5A2A22", "#2A1410"])
        for k in range(7):                                                       # wallpaper stripes and gas lamps
            c.drawRect(R(k * 160, 0, 70, H), P("#6A3428", 0.35))
        for k in range(4):
            add_glow(c, 140 + k * 270, 360, 80, "#FFC97A", 0.5)
            c.drawCircle(140 + k * 270, 360, 14, P("#FFE7B0"))
        c.drawRect(R(0, 1120, W, 800), lin_paint(0, 1120, 0, 1600, ["#6B4226", "#3A2414"]))  # wooden floor
        c.drawRect(R(620, 700, 460, 26), P("#8A5A30"))                           # the upper floor
        belt = path_of([(120, 1120), (640, 712), (670, 730), (160, 1140)], close=True)
        c.drawPath(belt, lin_paint(0, 700, 0, 1140, ["#5A3A20", "#3A2412"]))       # the 1898 moving ramp
        for j in range(12):
            q = (j / 12.0 + t * 0.15) % 1.0
            c.drawLine(lerp(130, 650, q), lerp(1124, 716, q), lerp(160, 675, q), lerp(1140, 730, q), P("#2A180C", 0.8, stroke=4))
        c.drawLine(110, 1030, 640, 620, P("#B8860B", 1.0, stroke=10))                # brass handrail
        for j in range(6):
            x_ = lerp(130, 620, j / 5.0)
            c.drawLine(x_, lerp(1116, 716, j / 5.0), x_, lerp(1026, 632, j / 5.0), P("#B8860B", 0.9, stroke=5))
        sk = prog(t, T["scared"] - 0.3, T["scared"] + 0.2)                       # the dizzy shopper at the top
        lx, ly = 720, 700
        c.save()
        c.translate(lx, ly)
        c.rotate(-8 * math.sin(t * 4) * sk)
        dress = path_of([(-30, -70), (30, -70), (52, 0), (-52, 0)], close=True)
        person(c, 0, 0, 130, "#7E22CE", t, pose="shrug" if sk > 0.5 else "stand", face=1, hat="none", hair="#3B2416")
        c.drawPath(dress, P("#7E22CE"))
        c.drawOval(R(-30, -150, 60, 16), P("#1F2937"))                            # her hat
        c.restore()
        if sk > 0:
            for j in range(4):                                                   # dizzy stars
                an = t * 4 + j * 1.57
                c.drawCircle(lx + math.cos(an) * 40, ly - 160 + math.sin(an) * 12, 7, P(HILITE, sk))
        stk = prog(t, T["staff"] - 0.3, T["staff"] + 0.2)
        person(c, 900, 700, 140, "#111827", t, pose="carry", face=-1, hat="none", hair="#1C1917", a=stk)
        if stk > 0:                                                              # the tray
            c.drawOval(R(800, 610, 90, 14), P("#D1D5DB", stk))
            c.drawRRect(rr(812, 580, 18, 32, 4), P("#7DD3FC", stk))              # smelling salts
            if not self.rtl:
                c.drawPath(path_of([(845, 576), (875, 576), (866, 604), (854, 604)], close=True), P("#B45309", stk))
            else:
                c.drawOval(R(842, 570, 40, 30), P("#E5E7EB", stk))               # a hand fan

    def ui_harrods(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "london", T["london"] - 0.2, T["scared"] - 0.2, accent="#FDE68A", size=46)
        self.chip(540, 300, "scared", T["scared"] - 0.2, T["brandy"] - 0.2, accent=WARN, size=44)
        self.chip(540, 300, "brandy", T["brandy"] - 0.2, s("stat") - 0.15, accent=HILITE, size=38)

    # ------------------------------------------------------------------ stat: the long one and the tiny one
    def draw_long(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#0B1230", "#141B3A", "#05070F"])
        mk = prog(t, T["moscow"] - 0.4, T["moscow"])
        x0, y0, x1, y1 = 60, 640, 640, 1180                                       # Moscow: a long tunnel down
        c.drawPath(path_of([(x0 - 30, y0 - 60), (x1 + 30, y1 - 120), (x1 + 30, y1 + 30), (x0 - 30, y0 + 80)], close=True),
                   P("#1E293B"))
        n = 34
        for j in range(n):
            q = ((j / n) + t * 0.05) % 1.0
            px, py = lerp(x0, x1, q), lerp(y0, y1, q)
            c.drawRect(R(px, py, 14, 6), P(STEEL, 0.9))
            if j % 4 == 0:
                add_glow(c, px, py - 60, 26, "#FFF1C9", 0.5)
        for j in range(5):
            q = ((j / 5.0) + t * 0.05) % 1.0
            person(c, lerp(x0, x1, q), lerp(y0, y1, q) - 4, 40, "#94A3B8", t + j, face=1, a=0.9)
        c.drawLine(x0 - 10, y0 - 40, x1 + 10, y1 - 40, P(HILITE, mk, stroke=5))
        jk = prog(t, T["five"] - 0.4, T["five"])
        bx, by = 820, 1180                                                       # Japan: five steps
        for j in range(5):
            c.drawRect(R(bx + j * 34, by - j * 20 - 20, 34, j * 20 + 20), P(mix("#64748B", "#94A3B8", j / 5.0)))
            c.drawRect(R(bx + j * 34, by - j * 20 - 20, 34, 5), P("#FACC15", 0.9))
        person(c, bx + 60, by - 40, 120, "#E11D48", t, face=1, pose="shrug" if jk > 0.5 else "stand")
        add_glow(c, bx + 85, by - 60, 140, HILITE, 0.25 * jk)

    # ------------------------------------------------------------------ tag
    def draw_tag(self, c, t):
        T = self.T
        self.mall_bg(c, t)
        if not self.rtl:
            gk = prog(t, T["t_climb"] - 0.3, T["t_climb"] + 0.2)
            if gk < 1:                                                           # riding up to the gym
                c.save()
                c.saveLayerAlpha(None, int(255 * (1 - gk)))
                self.view(c, (120, -230, 1.1))
                for kind, x in steps_at(t):
                    if kind == "top":
                        step_top(c, x)
                c.drawPath(truss_path(), lin_paint(0, -RISE, 0, RET, ["#8A94A4", "#5B6372", "#3F4654"]))
                self.rail(c, t)
                ph = (t * V) % D
                x = -60 + ph
                rider(c, x + D / 2, ypass(x + D) - 8, 120, "#2563EB", t, phone=True)
                c.drawRect(R(XB - 10, -RISE, 900, 56), P("#94A3B8"))
                c.drawRRect(rr(XB - 150, -RISE - 330, 260, 300, 12), P("#1E293B"))
                word(c, self.L["gym"], XB - 20, -RISE - 220, 70, HILITE)
                c.restore()
                c.restore()
                c.restore()
            if gk > 0:                                                           # the stair machine
                c.save()
                c.saveLayerAlpha(None, int(255 * gk))
                cx_, cy_ = 540, 1100
                c.drawRRect(rr(cx_ - 220, cy_ - 520, 440, 520, 30), P("#1F2937"))
                for j in range(7):
                    yy = cy_ - 60 - ((j * 70 + t * 160) % 490)
                    c.drawRect(R(cx_ - 180, yy, 360, 22), P("#4B5563"))
                c.drawRect(R(cx_ - 240, cy_ - 620, 20, 620), P("#9CA3AF"))
                c.drawRect(R(cx_ + 220, cy_ - 620, 20, 620), P("#9CA3AF"))
                c.drawRRect(rr(cx_ - 90, cy_ - 700, 180, 90, 12), P("#0EA5E9"))
                rider(c, cx_, cy_ - 120 + 14 * math.sin(t * 8), 260, "#2563EB", t, pose="walk", face=1)
                for j in range(4):
                    qq = (t * 1.6 + j / 4.0) % 1.0
                    c.drawCircle(cx_ + 40 + j * 8, cy_ - 400 + qq * 60, 7, P("#BAE6FD", 1 - qq))
                c.restore()
                c.restore()
        else:                                                                    # grandma waits for a step to stop
            self.view(c, (XA + 120, -100, 2.0))
            for kind, x in steps_at(t):
                if kind == "top":
                    step_top(c, x)
            c.drawPath(truss_path(), lin_paint(0, -RISE, 0, RET, ["#8A94A4", "#5B6372", "#3F4654"]))
            self.rail(c, t)
            c.drawRect(R(-1400, 6, 3000, 1600), lin_paint(0, 0, 0, 500, ["#94A3B8", "#475569"]))
            c.drawRect(R(XA - 60, -2, 90, 10), P("#FACC15", 0.9))
            gw = math.sin(t * 2.2) * 8
            grandma(c, XA - 90, 0, 150, t, lean=gw)
            c.restore()
            mini_clock(c, 860, 760, 70, t * 6, a=prog(t, T["t_climb"] - 0.3, T["t_climb"]))

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            self.chip(540, 300, "machine", T["t_stair"] - 0.2, self.duration + 1, accent=HILITE, size=46)
        else:
            self.chip(540, 300, "waiting", T["t_stair"] - 0.2, self.duration + 1, accent=HILITE, size=44)

    def whip_backdrop(self, c, t, m):
        self.mall_bg(c, t)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hum(max(1.5, T["congrats"]), 70.0), -22), (T["half"], sfx.whoosh(0.5, False, 61), -12),
              (T["upside"], sfx.sparkle(0.6, 8, 62), -10), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 63), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 64), -8), (T["name"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["wear"], sfx.buzz(0.4), -14),
               (T["few"], sfx.ring(0.6), -14), (T["few1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 66), -4), (T["chain"], sfx.whirr(1.4, 90.0, 120.0, 67), -14),
               (T["motor"], sfx.hum(1.2, 90.0), -12), (T["pulls1"], sfx.ding(), -8), (T["pulls1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["trip"], sfx.thud(0.4, 69), -6),
               (T["trip1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 70), -4), (T["wheels"], sfx.click(71), -6),
               (T["tracks"], sfx.click(72), -6), (T["flat1"], sfx.ding(), -8), (T["flat1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["lace"], sfx.snap(74), -6),
               (T["lace1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 75), -4), (T["comb"], sfx.clank(600.0, 0.3, 76), -10),
               (T["lift1"], sfx.ding(), -8), (T["lift1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 77), -4), (T["slower"], sfx.creak(0.8, 78), -10),
               (T["back1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 79), -4), (T["motor4"], sfx.hum(1.0, 95.0), -12),
               (T["feet1"], sfx.ding(), -8), (T["feet1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(80), 0), (T["follow"] - 0.15, sfx.pop(81), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 82), -6), (T["scared"], sfx.womp(), -10),
               (T["staff"], sfx.bell(1320.0, 0.6, 0.5), -12)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 83), -6), (T["s1"], sfx.pop(84), -3), (T["s2"], sfx.pop(85), -3),
               (T["s3"], sfx.pop(86), -3)]
        ev += [(T["cong2"], sfx.pop(87), -2), (T["cong2"], sfx.sparkle(1.4, 18, 88), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 89), -6), (T["t_climb"], sfx.whoosh(0.4, True, 90), -8),
               (T["t_mach"], sfx.pop(91), -6)]
        return ev


NAME = "escalator"
EPISODE = Escalator
