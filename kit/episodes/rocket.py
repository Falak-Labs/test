"""Episode 6 - A rocket that lands itself.  The reference episode for the v2 look (episodes/v2_base.py, bik/v2.py).

Six sets with whip cuts between them: the launch pad at dusk (pad), the falling close-up (fall), high above the Earth
(space), tail first in the clouds (fall2), the landing zone at night (lz) and the ocean with the landing ship (sea).
Copy this structure for new episodes: class data, _tracks() with anchors + cuts + cameras + HUD spans, one draw_<set>
and one ui_<set> per set, sfx_events().
"""
from v2_base import *  # noqa: F401,F403

BW, BH, NH = 84, 600, 124          # rocket body width / height, nose height
PAD_Y = -46                        # top of the launch mount: the engines sit here
HULL, BAND = "#EEF1F6", "#232936"


# ====================================================================================== the rocket
def draw_rocket(c, x, y, ang, t, flame=0.0, heat=0.0, gas=(0.0, 0.0), soot=0.0, warm=0.0, s=1.0, fl_len=520,
                fins=None, fin_tilt=0.0, legs=None):
    """Rocket with its centre at (x, y), rotated ang degrees (0 = nose up). flame 0..1 engine power; heat 0..1
    re-entry glow on the nose; gas (left, right) cold-gas jets at the top; soot 0..1 burnt lower body; warm 0..1
    orange bounce light from its own flame; fins / legs: None = not fitted, else 0..1 unfolded."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    hw, top, bot = BW / 2, -BH / 2, BH / 2
    tip = top - NH
    if heat > 0:                                                     # plasma sheath streaming back from the nose
        sheath = skia.Path()
        sheath.moveTo(-200, tip + 640)
        sheath.cubicTo(-150, tip + 230, -96, tip - 4, 0, tip - 36)
        sheath.cubicTo(96, tip - 4, 150, tip + 230, 200, tip + 640)
        sheath.close()
        p = lin_paint(0, tip - 36, 0, tip + 640, [("#FFFFFF", 0.95), ("#FFD27A", 0.78), ("#FF7A2F", 0.40), ("#FF5A2A", 0.0)],
                      [0.0, 0.10, 0.42, 1.0], heat)
        p.setBlendMode(PLUS)
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 24))
        c.drawPath(sheath, p)
    if flame > 0:
        v2.flame(c, 0, bot + 54, 62, fl_len, t, flame, seed=3)
    for nx in (-27, 0, 27):                                         # engine bells
        path = skia.Path()
        path.moveTo(nx - 8, bot + 30)
        path.lineTo(nx + 8, bot + 30)
        path.lineTo(nx + 13, bot + 58)
        path.lineTo(nx - 13, bot + 58)
        path.close()
        cyl_path(c, path, nx - 13, nx + 13, "#59607A", depth=1.3)
        if flame > 0:
            add_glow(c, nx, bot + 56, 22, "#FFE9A8", 0.9 * flame)
    cyl(c, -hw - 3, bot - 2, BW + 6, 36, "#171B26", r=5)             # engine skirt
    cyl(c, -hw, top, BW, BH, HULL)                                   # hull
    if soot > 0:
        vrect(c, -hw, top + BH * 0.42, BW, BH * 0.58, [("#14161D", 0.0), ("#14161D", 0.50 * soot), ("#0C0D12", 0.86 * soot)],
              [0.0, 0.55, 1.0])
    cyl(c, -hw, top, BW, 92, BAND)                                   # interstage band
    for yy in (top + 92, -150, -30, 90, 210):                        # panel seams
        c.drawRect(R(-hw, yy - 1.5, BW, 3), P("#0B1020", 0.22))
    c.drawRect(R(hw * 0.42, top + 96, 5, BH - 100), P("#0B1020", 0.16))   # raceway
    for i, yy in enumerate((top + 112, top + 126)):                  # accent rings
        cyl(c, -hw, yy, BW, 7, ACCENT if i == 0 else "#3B82F6", depth=0.8)
    c.save()                                                         # name down the side
    c.translate(-6, 60)
    c.rotate(-90)
    text(c, "CE-06", 0, 0, 34, "#1F2637", "Poppins-Black", a=0.82 * (1 - 0.6 * soot))
    c.restore()
    if legs is not None:                                             # landing legs: folded up the hull, or out wide
        k = clamp(legs)
        th = lerp(-90.0, 40.0, e_out(k))
        for side in (-1, 1):
            c.save()
            c.translate(side * (hw + 3), bot - 10)
            if side < 0:
                c.scale(-1, 1)
            if k > 0.3:                                              # telescoping strut
                lx, ly = math.cos(math.radians(th)) * 150, math.sin(math.radians(th)) * 150
                c.drawLine(-3, -150, lx, ly, P("#8D96AB", 1, stroke=7))
                c.drawLine(-3, -150, lx * 0.5 - 1.5, ly * 0.5 - 75, P("#C9D0DE", 1, stroke=11))
            c.rotate(th)
            leg = skia.Path()
            leg.moveTo(0, -11)
            leg.lineTo(236, -5)
            leg.lineTo(236, 5)
            leg.lineTo(0, 11)
            leg.close()
            c.drawPath(leg, lin_paint(0, -11, 0, 11, ["#FFFFFF", "#DDE2EC", "#9AA3B8"]))
            c.drawRRect(rr(224, -10, 24, 20, 6), P("#2B3248"))
            c.restore()
    nose = skia.Path()                                               # nose cone
    nose.moveTo(-hw, top)
    nose.cubicTo(-hw, top - NH * 0.55, -hw * 0.35, top - NH * 0.95, 0, top - NH)
    nose.cubicTo(hw * 0.35, top - NH * 0.95, hw, top - NH * 0.55, hw, top)
    nose.close()
    cyl_path(c, nose, -hw, hw, HULL)
    c.drawRect(R(-hw, top - 2, BW, 4), P("#0B1020", 0.30))
    for side in (-1, 1):                                             # cold-gas thruster pods
        box(c, side * hw - (0 if side > 0 else 12), top + 20, 12, 30, "#3A4258", r=3)
    if fins is not None:                                             # grid fins: flat against the hull, or out like wings
        k = clamp(fins)
        for side in (-1, 1):
            c.save()
            c.translate(side * hw, top + 66)
            if side < 0:
                c.scale(-1, 1)
            c.rotate(lerp(84.0, 0.0, e_back(k)) + fin_tilt * side)
            box(c, -2, -6, 20, 12, "#3A4258", r=3)
            c.drawRRect(rr(16, -24, 66, 48, 7), lin_paint(16, -24, 16, 24, ["#C5CCDA", "#8D96AB", "#5F6880"]))
            for gx in (29, 42, 55, 68):
                c.drawRect(R(gx, -21, 3, 42), P("#2B3248", 0.85))
            for gy_ in (-9, 6):
                c.drawRect(R(19, gy_, 60, 3), P("#2B3248", 0.85))
            c.drawRRect(rr(16, -24, 66, 48, 7), P("#2B3248", 0.9, stroke=3))
            c.restore()
    c.drawRect(R(hw - 4, top - NH * 0.3, 3, BH + NH * 0.3), P("#BFD8FF", 0.50))        # cool rim light (moon)
    if warm > 0:                                                     # warm bounce from the flame
        vrect(c, -hw, top + BH * 0.55, BW, BH * 0.45, [("#FF9A4D", 0.0), ("#FF9A4D", 0.42 * warm)])
    for side, g in zip((-1, 1), gas):                                # gas jets
        if g > 0:
            gx, gy = side * (hw + 10), top + 35
            for k in range(5):
                u = ((t * 3.1 + k * 0.2) % 1.0)
                r_ = (10 + 46 * u) * g
                px_, py_ = gx + side * (16 + 120 * u) * g, gy + math.sin(k * 2.1 + t * 9) * 8
                c.drawCircle(px_, py_, r_, rad_paint(px_, py_, r_, [("#FFFFFF", 0.85 * (1 - u) * g), ("#DDEBFF", 0.0)]))
            add_glow(c, gx + side * 20, gy, 60 * g, "#DCEBFF", 0.55 * g)
    if heat > 0:                                                     # the nose itself glows
        c.save()
        c.clipPath(nose, doAntiAlias=True)
        vrect(c, -hw, tip, BW, NH, [("#FFFFFF", 0.95 * heat), ("#FFC766", 0.80 * heat), ("#FF7A2F", 0.35 * heat)])
        c.restore()
        vrect(c, -hw, top, BW, 150, [("#FF8A3D", 0.42 * heat), ("#FF8A3D", 0.0)])
        add_glow(c, 0, tip + 8, 170, "#FF9A4D", 0.50 * heat)
        add_glow(c, 0, tip - 6, 62, "#FFFFFF", 0.95 * heat)
        rng = random.Random(8)
        for _ in range(18):                                          # plasma streaks trailing back along the hull
            sx = rng.uniform(-hw - 90, hw + 90)
            ph = (t * rng.uniform(900, 1600) + rng.uniform(0, 900)) % 900
            p = P(rng.choice(["#FFD27A", "#FF9A4D", "#FFFFFF"]), 0.5 * heat * (1 - ph / 900), stroke=rng.uniform(2, 5))
            p.setBlendMode(PLUS)
            c.drawLine(sx, tip + 60 + ph, sx * 1.05, tip + 60 + ph + rng.uniform(60, 170), p)
    c.restore()


STAND, STAND_LEGS = BH / 2 + 58, BH / 2 + 150     # centre height above the surface: on the engine bells / on the legs


def pencil(c, x, y, rot, s=1.0):
    """A big yellow pencil (the tumbling comparison)."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    cyl(c, -17, -150, 34, 250, "#FACC15")
    c.drawRect(R(-6, -150, 3, 250), P("#CA8A04", 0.5))
    cyl(c, -17, -176, 34, 28, "#C9D0DE")
    c.drawRRect(rr(-17, -210, 34, 38, 9), P("#FB7185"))
    tipp = skia.Path()
    tipp.moveTo(-17, 100)
    tipp.lineTo(17, 100)
    tipp.lineTo(0, 158)
    tipp.close()
    c.drawPath(tipp, P("#F5D7A8"))
    lead = skia.Path()
    lead.moveTo(-6, 138)
    lead.lineTo(6, 138)
    lead.lineTo(0, 158)
    lead.close()
    c.drawPath(lead, P("#1F2937"))
    c.restore()


def landing_zone(c, t, lights=1.0):
    """Concrete landing pad with a ring of ground lights."""
    box(c, -340, -16, 680, 22, "#59627A", r=4)
    for sx_ in range(-300, 301, 60):
        c.drawRect(R(sx_ - 18, -15, 36, 5), P("#FACC15", 0.75))
    for i, lx in enumerate(range(-330, 331, 110)):
        on = 0.45 + 0.55 * (math.sin(t * 5 - i * 0.9) > 0.3)
        add_glow(c, lx, -20, 46, "#7DD3FC", 0.75 * on * lights)
        c.drawCircle(lx, -20, 5, P("#E0F2FE"))
    c.drawRect(R(-452, -200, 6, 200), P(STEEL))                      # windsock
    sock = skia.Path()
    w_ = math.sin(t * 3.1) * 10
    sock.moveTo(-446, -198)
    sock.lineTo(-360, -186 + w_)
    sock.lineTo(-360, -170 + w_)
    sock.lineTo(-446, -168)
    sock.close()
    c.drawPath(sock, lin_paint(-446, 0, -360, 0, ["#FB923C", "#FFFFFF", "#FB923C", "#FFFFFF"], [0.0, 0.34, 0.67, 1.0]))


def droneship(c, x, t, target=1.0, name="OF COURSE I STILL LOVE YOU", name_glow=0.0):
    """Landing barge in three-quarter view: deck top with the painted target, hull side with the name."""
    c.save()
    c.translate(x, math.sin(t * 1.1) * 4)
    hull = skia.Path()
    hull.moveTo(-440, -34)
    hull.lineTo(440, -34)
    hull.lineTo(418, 52)
    hull.lineTo(-418, 52)
    hull.close()
    c.drawPath(hull, lin_paint(0, -34, 0, 52, ["#34405E", "#1C2439", "#12182A"]))
    c.drawRect(R(-420, 30, 840, 22), P("#7F1D1D", 0.85))
    deck = skia.Path()
    deck.moveTo(-440, -34)
    deck.lineTo(-404, -84)
    deck.lineTo(404, -84)
    deck.lineTo(440, -34)
    deck.close()
    c.drawPath(deck, lin_paint(0, -84, 0, -34, ["#4A5470", "#66708C"]))
    c.drawRect(R(-440, -36, 880, 5), P("#8D96AB"))
    if target > 0:                                                   # painted target, drawn on
        ring = skia.Path()
        ring.addOval(R(-190, -74, 380, 30))
        meas = skia.PathMeasure(ring, False)
        seg = skia.Path()
        meas.getSegment(0, meas.getLength() * clamp(target), seg, True)
        c.drawPath(seg, P("#FACC15", 1, stroke=6))
        if target > 0.6:
            a_ = clamp((target - 0.6) / 0.4)
            c.drawLine(-120, -70, 120, -48, P("#FACC15", a_, stroke=5))
            c.drawLine(120, -70, -120, -48, P("#FACC15", a_, stroke=5))
    for bx in (-396, 330):                                           # deck houses at both ends
        box(c, bx, -128, 66, 52, "#2A3149", r=4)
        c.drawRRect(rr(bx + 10, -116, 18, 14, 3), P("#FFD98A"))
        add_glow(c, bx + 19, -109, 34, "#FFC766", 0.4)
    beacon(c, -366, -134, t, hz=1.0, r=5)
    beacon(c, 366, -134, t, col="#34D399", hz=1.0, r=5, ph=0.5)
    if name:
        if name_glow > 0:
            add_glow(c, 0, 4, 420, "#FFFFFF", 0.16 * name_glow)
        text(c, name, 0, 16, 36, mix("#C9D0DE", "#FFFFFF", name_glow), "Poppins-Black")
    c.restore()


def tug(c, x, t):
    """Small crew boat."""
    c.save()
    c.translate(x, math.sin(t * 1.3 + 1) * 5)
    hull = skia.Path()
    hull.moveTo(-120, -30)
    hull.lineTo(130, -30)
    hull.lineTo(96, 30)
    hull.lineTo(-104, 30)
    hull.close()
    c.drawPath(hull, lin_paint(0, -30, 0, 30, ["#F97316", "#9A3412"]))
    box(c, -96, -92, 80, 62, "#E5E9F2", r=6)
    c.drawRRect(rr(-84, -80, 22, 20, 3), P("#7DD3FC"))
    c.drawRRect(rr(-52, -80, 22, 20, 3), P("#7DD3FC"))
    c.restore()


# ====================================================================================== set pieces


def tank(c, x, t):
    """Spherical propellant tank on legs."""
    for dx in (-44, 44):
        c.drawLine(x + dx, 0, x + dx * 0.55, -70, P(STEEL, 1, stroke=7))
    contact_shadow(c, x, 4, 190, 0.45, 26)
    c.drawCircle(x, -118, 74, rad_paint(x - 28, -150, 130, ["#F2F5FA", "#B9C2D6", "#5C667F"], [0.0, 0.5, 1.0]))
    c.drawArc(R(x - 74, -192, 148, 148), 20, 140, False, P("#0B1020", 0.18, stroke=3))
    c.drawRect(R(x - 2, -230, 4, 40), P(STEEL))
    beacon(c, x, -232, t, hz=0.9, r=5, ph=0.2)


def crater(c, x, k, t):
    """Blast crater replacing the pad; k 0..1 how far it has opened."""
    if k <= 0:
        return
    w, d = 620 * k, 150 * k
    path = skia.Path()
    path.moveTo(x - w / 2 - 40, -6)
    path.cubicTo(x - w / 2, -4, x - w * 0.36, d, x, d)
    path.cubicTo(x + w * 0.36, d, x + w / 2, -4, x + w / 2 + 40, -6)
    path.close()
    c.drawPath(path, lin_paint(0, -6, 0, d, ["#0A0C16", "#191322", "#3A1B1F"]))
    hot = 0.55 + 0.25 * math.sin(t * 5)
    add_glow(c, x, d * 0.7, w * 0.42, "#FF5A2A", 0.55 * hot * k)
    add_glow(c, x - w * 0.16, d * 0.5, w * 0.18, "#FFC857", 0.45 * hot * k)
    rng = random.Random(4)
    for i in range(12):                                              # rubble on the rim
        rx = x + rng.uniform(-w / 2 - 110, w / 2 + 110)
        if abs(rx - x) < w * 0.33:
            continue
        ww, hh = rng.uniform(20, 58), rng.uniform(12, 30)
        c.save()
        c.translate(rx, -6)
        c.rotate(rng.uniform(-28, 28))
        box(c, -ww / 2, -hh, ww, hh, rng.choice(["#6B7488", "#4A5368", "#2A3042"]), r=3)
        c.restore()


# ====================================================================================== the episode
class Rocket(EpisodeV2):
    BUILD_NO = 6
    FIRST_SET = "pad"
    SKY_ALT = {"pad": 0.0, "lz": 0.0, "sea": 0.0, "fall": 0.42, "fall2": 0.36, "space": 1.0}
    TITLE = {"en": "ROCKET", "ar_sa": "صاروخ"}
    EMPH = {"en": ["CONGRATS", "LANDS", "ITSELF", "CRATER", "FLIP", "TAIL", "TUMBLE", "FINS", "STEER", "STRONG", "ZERO",
                   "TIPS", "LEGS", "CRUSH", "FOLLOW", "CASTLE", "TARGET", "NINE", "YOURSELF", "LOVE", "FEELINGS"],
            "ar_sa": ["مبروك", "بروحه", "حفرة", "تقلبه", "ذيله", "يتشقلب", "زعانف", "تسوقه", "قوي", "صفر", "ويطيح", "رجول",
                      "حشوة", "تابعني", "قلعة", "هدف", "تسع", "بيدك", "أحبك", "مشاعر"]}
    KEYS = {"ar_sa": {
        ("hook", "LAUNCH"): "طيرت", ("hook", "WAIT"): "تستنى", ("hook", "CONGRATS"): "مبروك", ("hook", "LANDS"): "ينزل",
        ("break1", "NOSE"): "خشمه", ("break1", "FASTER"): "أسرع", ("break1", "BULLET"): "الرصاصة", ("break1", "AND"): "ويخلي",
        ("break1", "LAUNCH"): "منصة", ("break1", "CRATER"): "حفرة",
        ("fix1", "GAS"): "بخاخات", ("fix1", "FLIP"): "تقلبه", ("fix1", "RELIGHT"): "وتشغل", ("fix1", "BRAKE"): "تفرمل",
        ("fix1", "TAIL"): "ذيله",
        ("break2", "AIR"): "الهوا", ("break2", "TUMBLE"): "يتشقلب", ("break2", "PENCIL"): "قلم",
        ("fix2", "GRID"): "زعانف", ("fix2", "WAFFLE"): "وافل", ("fix2", "STEER"): "تسوقه", ("fix2", "DOWN"): "تحت",
        ("break3", "STRONG"): "قوي", ("break3", "LOWEST"): "أوطى", ("break3", "PUSHES"): "يدف", ("break3", "UP"): "فوق",
        ("fix3", "HOVER"): "يوقف", ("fix3", "BURN"): "وتشغله", ("fix3", "ZERO"): "صفر", ("fix3", "TOUCHES"): "يلمس",
        ("break4", "SOFTLY"): "بشويش", ("break4", "TALL"): "طوله", ("break4", "TIPS"): "ويطيح",
        ("fix4", "LEGS"): "رجول", ("fix4", "FOLD"): "تنفتح", ("fix4", "CRUSH"): "حشوة", ("fix4", "SOAK"): "وتمتص",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PARK"): "وقف", ("reveal", "DRAW"): "وارسم", ("reveal", "LAND"): "وانزل",
        ("stat", "ONE"): "صاروخ", ("stat", "NINE"): "تسع", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "NAME"): "واسم", ("tag", "COURSE"): "أكيد", ("tag", "FEELINGS"): "مشاعر"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a castle"),
                   "stat": [("1", "ROCKET"), ("9", "ENGINES"), ("0", "PILOTS")],
                   "L": {"yours": "YOUR ROCKET", "nose": "NOSE FIRST", "gas": "GAS THRUSTERS", "relit": "3 ENGINES RELIT",
                         "fins": "GRID FINS", "waffle": "NOT FOR WAFFLES", "throttle": "LOWEST POWER", "nohover": "NO HOVERING",
                         "burn": "ONE LAST BURN", "speed": "SPEED", "height": "HEIGHT", "touch": "TOUCHDOWN",
                         "floors": "14 FLOORS", "legs": "LANDING LEGS", "crush": "CRUSH CORE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قلعة"),
                      "stat": [("1", "صاروخ"), ("9", "محركات"), ("0", "طيارين")],
                      "L": {"yours": "صاروخك", "nose": "على خشمه", "gas": "بخاخات غاز", "relit": "المحركات اشتغلت",
                            "fins": "زعانف شبك", "waffle": "مو للوافل", "throttle": "أوطى قوة", "nohover": "ما يوقف بالهوا",
                            "burn": "آخر تشغيلة", "speed": "السرعة", "height": "الارتفاع", "touch": "نزل بالسلامة",
                            "floors": "أربعطعش دور", "legs": "رجول الهبوط", "crush": "حشوة تنعصر"}}}
    TAIL = 2.0


    # ------------------------------------------------------------------ timing


    def _tracks(self):
        w, s, e = self.w, self.tl.s, self.tl.e
        T = self.T
        for name, (lab, key, frac) in {
                "launch": ("hook", "LAUNCH", 0.15), "wait": ("hook", "WAIT", 0.4), "congrats": ("hook", "CONGRATS", 0.5),
                "lands": ("hook", "LANDS", 0.85), "nose": ("break1", "NOSE", 0.2), "faster": ("break1", "FASTER", 0.35),
                "bullet": ("break1", "BULLET", 0.5), "crater": ("break1", "CRATER", 0.9),
                "gas": ("fix1", "GAS", 0.15), "flip": ("fix1", "FLIP", 0.35), "relight": ("fix1", "RELIGHT", 0.5),
                "brake": ("fix1", "BRAKE", 0.7), "tail": ("fix1", "TAIL", 0.9),
                "air": ("break2", "AIR", 0.35), "tumble": ("break2", "TUMBLE", 0.7), "pencil": ("break2", "PENCIL", 0.9),
                "grid": ("fix2", "GRID", 0.2), "waffle": ("fix2", "WAFFLE", 0.55), "steer": ("fix2", "STEER", 0.75),
                "down": ("fix2", "DOWN", 0.95),
                "strong": ("break3", "STRONG", 0.25), "lowest": ("break3", "LOWEST", 0.5), "pushes": ("break3", "PUSHES", 0.7),
                "up": ("break3", "UP", 0.95),
                "hover": ("fix3", "HOVER", 0.1), "burn": ("fix3", "BURN", 0.3), "zero": ("fix3", "ZERO", 0.55),
                "touches": ("fix3", "TOUCHES", 0.85),
                "softly": ("break4", "SOFTLY", 0.2), "tall": ("break4", "TALL", 0.45), "tips": ("break4", "TIPS", 0.85),
                "legs": ("fix4", "LEGS", 0.2), "fold": ("fix4", "FOLD", 0.35), "crush": ("fix4", "CRUSH", 0.65),
                "soak": ("fix4", "SOAK", 0.85),
                "follow": ("cta", "FOLLOW", 0.45),
                "park": ("reveal", "PARK", 0.15), "draw": ("reveal", "DRAW", 0.5), "land": ("reveal", "LAND", 0.85),
                "s1": ("stat", "ONE", 0.05), "s2": ("stat", "NINE", 0.4), "s3": ("stat", "ZERO", 0.75),
                "cong2": ("closer", "CONGRATS", 0.2),
                "name": ("tag", "NAME", 0.2), "course": ("tag", "COURSE", 0.4), "feelings": ("tag", "FEELINGS", 0.9)}.items():
            T[name] = w(lab, key, frac)
        # cuts between sets: (time, set, whip direction)
        T["cut_fall"] = s("break1") - 0.10
        T["cut_pad"] = w("break1", "AND", 0.55) + 0.02
        T["impact"] = w("break1", "LAUNCH", 0.75) + 0.02
        T["cut_space"] = s("fix1") - 0.12
        T["cut_fall2"] = s("break2") - 0.12
        T["cut_lz"] = s("break3") - 0.12
        T["cut_retry"] = s("fix4") - 0.10
        T["cut_sea"] = s("reveal") - 0.12
        T["touch3"] = T["touches"] + 0.25                      # fix 3: the perfect landing (no legs yet)
        T["tip0"] = T["tips"] - 0.35                           # break 4: it starts to go...
        T["fall4"] = T["tips"] + 0.25                          # ...and hits the ground on its side
        T["touch4"] = T["soak"] + 0.05                         # fix 4: landing on legs
        T["deck"] = T["land"] + 0.62                           # reveal: landing on the ship
        self.cuts = [(-1e9, "pad", 0), (T["cut_fall"], "fall", 1), (T["cut_pad"], "pad", -1), (T["cut_space"], "space", 1),
                     (T["cut_fall2"], "fall2", -1), (T["cut_lz"], "lz", -1), (T["cut_retry"], "lz", 1), (T["cut_sea"], "sea", -1)]
        self.cam = Camera(0, -330, 0.80)                       # launch pad camera
        self.cam.key(0.05, 0, -300, 0.90, 0.9)
        self.cam.key(T["launch"] + 0.10, 0, -600, 0.86, 1.0)
        self.cam.key(T["wait"] + 0.1, 0, -680, 0.84, 1.2)
        self.cam.key(T["cut_pad"], 0, -320, 0.84, 0.0)
        self.cam.key(T["impact"] + 0.5, 0, -290, 0.92, 1.6)
        self.cam_lz = Camera(0, -346, 0.78)                    # landing zone camera
        self.cam_lz.key(T["cut_lz"], 0, -346, 0.78, 0.0)
        self.cam_lz.key(T["lowest"], 0, -330, 0.82, 1.2)
        self.cam_lz.key(T["hover"], 0, -365, 0.74, 0.8)
        self.cam_lz.key(T["zero"], 0, -314, 0.86, 1.4)
        self.cam_lz.key(T["tall"] - 0.3, 60, -355, 0.76, 0.8)
        self.cam_lz.key(T["tips"] + 0.1, -120, -321, 0.84, 0.6)
        self.cam_lz.key(T["cut_retry"], 0, -365, 0.74, 0.0)
        self.cam_lz.key(T["crush"] - 0.2, 0, -281, 0.96, 1.2)
        self.cam_sea = Camera(0, -300, 0.80)                   # ocean camera
        self.cam_sea.key(T["cut_sea"], 60, -300, 0.80, 0.0)
        self.cam_sea.key(T["draw"], 0, -270, 0.90, 0.8)
        self.cam_sea.key(T["s1"] - 0.25, 0, -340, 0.70, 0.9)
        self.cam_sea.key(s("tag") - 0.22, 70, -30, 1.62, 0.34)
        self.shakes = [(T["launch"], 1.3, 16), (T["nose"] - 0.4, 1.9, 7), (T["impact"], 1.1, 46), (T["relight"], 0.9, 9),
                       (T["pushes"], 1.0, 8), (T["burn"], 1.0, 10), (T["touch3"], 0.4, 14), (T["fall4"], 0.9, 40),
                       (T["touch4"], 0.45, 14), (T["deck"], 0.45, 12)]
        self.flip = Track(180.0).to(T["flip"], -8.0, 0.80, e_io).to(T["flip"] + 0.80, 0.0, 0.35, e_io)
        self.spans = [(T["impact"], T["tail"]), (T["tumble"], T["steer"] + 0.7), (T["pushes"] + 0.2, T["touch3"]),
                      (T["fall4"], T["touch4"])]

    # ------------------------------------------------------------------ helpers


    # ------------------------------------------------------------------ frame

    # ------------------------------------------------------------------ set 1: the launch pad
    def draw_pad(self, c, t):
        T = self.T
        cx, cy, z = self.cam.at(t)
        cx += math.sin(t * 0.7) * 3
        gy = (0 - cy) * z + H / 2                                 # screen y of the ground line
        launched = t >= T["launch"]
        tl_ = t - T["launch"]
        rise = 0.0 if not launched else 0.5 * 1750 * max(0.0, tl_ - 0.12) ** 2
        burn = clamp(tl_ * 6) if launched else 0.0
        back = t >= T["cut_pad"]                                 # the wreck comes back
        hit = t - T["impact"]
        glow_k = burn * clamp(1 - rise / 2600) if not back else 0.0
        self.backdrop(c, t, cx, cy, gy)
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)
        v2.ground(c, -3200, 3200)
        k_cr = e_out(prog(t, T["impact"], T["impact"] + 0.5)) if back else 0.0
        fuel = clamp(1 - tl_ * 2) if launched else 1.0
        buried_line(c, [(-430, 0), (-430, 176), (-52, 176), (-52, 10)], ACCENT, t, 0.9 * fuel * (1 - k_cr))          # fuel
        buried_line(c, [(470, 0), (470, 214), (40, 214), (40, 10)], "#60A5FA", t, 0.8 * (1 - k_cr), w=7)              # power + data
        tank(c, -430, t)
        c.drawRect(R(300, -830, 6, 830), lin_paint(300, 0, 306, 0, [shade(STEEL, 0.35), shade(STEEL, -0.3)]))     # lightning mast
        beacon(c, 303, -836, t, hz=1.3, ph=0.5)
        bunker(c, 352, t, lit=glow_k)
        lean = -24 * e_out(prog(t, T["impact"] + 0.05, T["impact"] + 0.9)) if back else 0.0
        if k_cr < 1:                                             # pad apron + launch mount
            box(c, -330, -16, 660, 22, "#59627A", r=4, a=1 - k_cr)
            for sx_ in range(-300, 301, 60):
                c.drawRect(R(sx_ - 18, -15, 36, 5), P("#FACC15", 0.75 * (1 - k_cr)))
            box(c, -76, PAD_Y, 152, -PAD_Y - 14, "#343C52", r=5, a=1 - k_cr)
            contact_shadow(c, 0, -14, 300, 0.5 * (1 - k_cr), 30)
        crater(c, 0, k_cr, t)
        if glow_k > 0:                                           # the plume lights the ground
            add_glow(c, 0, -20, 1100, "#FF8A3D", 0.50 * glow_k)
            add_glow(c, 0, -20, 420, "#FFD27A", 0.50 * glow_k)
        c.save()                                                 # service tower (falls over after the hit)
        c.translate(-178, 0)
        c.rotate(lean)
        lattice(c, 0, 0, -690, 52, lit=glow_k * 0.8)
        for ay in (-560, -300):
            ext = lerp(138, 40, clamp((tl_ + 0.5) * 2.2)) if launched else 138
            box(c, 20, ay, ext, 16, "#3A4258", r=3)
        for wy in (-640, -470, -300, -130):
            add_glow(c, 26, wy, 38, "#FFF1C9", 0.75)
            c.drawCircle(26, wy, 4, P("#FFFFFF"))
        beacon(c, 0, -702, t)
        c.restore()
        on = 1.0 if not back else clamp(1 - (hit + 0.1) * 6) if hit > -0.1 else 1.0
        floodlight(c, -560, 250, -20, -420, t, on)
        floodlight(c, 560, 228, 20, -380, t, on)
        rise_at = lambda tb: 0.5 * 1750 * max(0.0, tb - T["launch"] - 0.12) ** 2      # noqa: E731
        if launched and not back:                                # exhaust: a rolling ground cloud and a trail up the sky
            v2.smoke(c, 0, -30, t, T["launch"], T["launch"] + 1.6, rate=30, life=3.8, spread=(700, -30), rise=-24,
                     size=(54, 230), col="#B9BFD0", lit="#FF8A3D", lit_until=1.0, seed=2, drag=1.8)
            v2.smoke(c, 0, 0, t, T["launch"] + 0.16, T["launch"] + 1.5, rate=90, life=3.4, spread=(46, 30), rise=-6,
                     size=(40, 135), col="#BFC5D6", lit="#FFB05C", lit_until=0.45, seed=5, drag=1.4, a=0.8,
                     origin=lambda tb: (math.sin(tb * 7) * 8, PAD_Y + 40 - rise_at(tb)))
        if not back:
            ry = PAD_Y - 58 - BH / 2 - rise
            if ry > cy - H / z:                                  # still in (or near) frame
                if not launched:
                    contact_shadow(c, 0, PAD_Y, 160, 0.6, 16)
                draw_rocket(c, 0, ry, 0, t, flame=burn, warm=burn * 0.8, fl_len=600)
                if launched:
                    v2.embers(c, 0, PAD_Y, t, T["launch"] + 0.02, 1.2, n=46, speed=1100, seed=7, cone=(185, 355))
        else:
            fall = prog(t, T["impact"] - 0.20, T["impact"])
            if 0 < fall < 1:                                     # the last instant of the fall
                ry = lerp(-2300, -330, fall)
                p = P("#FF9A4D", 0.55, stroke=70)
                p.setBlendMode(PLUS)
                p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
                c.drawLine(0, ry - 1100, 0, ry - 300, p)
                draw_rocket(c, 0, ry, 180, t, heat=1.0)
            if hit >= 0:
                v2.smoke(c, 0, 20, t, T["impact"] + 0.2, T["impact"] + 9, rate=12, life=3.8, spread=(120, -300), rise=-80,
                         size=(50, 200), col="#6A7086", lit="#FF7A2F", lit_until=1.4, seed=11, drag=1.0)
                v2.fireball(c, 0, -40, t, T["impact"], 1.8, 440)
                v2.shock_ring(c, 0, -20, t, T["impact"], 0.75, 1500)
                v2.debris(c, 0, -30, t, T["impact"], 3.2, n=22, speed=1250, floor=0, seed=6)
                v2.embers(c, 0, -30, t, T["impact"], 1.8, n=70, speed=1500, seed=9)
                add_glow(c, 0, -60, 1700, "#FFE9C9", clamp(1 - hit * 5) * 0.95)
        if back and hit >= 0:
            pose, soot = "duck" if hit < 1.0 else "stand", clamp(hit * 3)
        elif t >= T["lands"] - 0.5:
            pose, soot = "point", 0.0
        elif t >= T["wait"]:
            pose, soot = "look", 0.0
        elif launched:
            pose, soot = "cheer", 0.0
        else:
            pose, soot = "stand", 0.0
        self.crew(c, t, pose, soot)
        c.restore()
        if T["wait"] + 0.55 <= t < T["cut_fall"]:                # the returning rocket, far away: a falling star
            u = prog(t, T["wait"] + 0.55, T["cut_fall"] + 0.4)
            fx_, fy_ = lerp(690, 640, u), lerp(250, 560, e_in(u) * 0.8 + u * 0.2)
            ln = 60 + 260 * u
            p = lin_paint(fx_ + ln * 0.16, fy_ - ln, fx_, fy_, [("#FF9A4D", 0.0), ("#FFE9A8", 0.95)])
            p.setStrokeWidth(5 + 5 * u)
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setBlendMode(PLUS)
            c.drawLine(fx_ + ln * 0.16, fy_ - ln, fx_, fy_, p)
            add_glow(c, fx_, fy_, 30 + 60 * u, "#FFB05C", 0.9)
            c.drawCircle(fx_, fy_, 5 + 4 * u, P("#FFFFFF"))
            self.ui["star"] = (fx_, fy_)

    # ------------------------------------------------------------------ set 2: falling, close up (break 1)
    def fall_sky(self, c, t, t0, alt, speed=1.0, seed=30):
        v2.sky(c, W, H, alt, horizon_y=H * 1.5)
        v2.stars(c, W, H, t, 0.8, dy=-(t * 260 * speed))
        for i in range(5):                                       # cloud deck rushing up past the camera
            rng = random.Random(seed + i)
            sp = rng.uniform(1100, 1900) * speed
            y = H + 400 - ((t - t0) * sp + rng.uniform(0, 3000)) % 3200
            v2.cloud(c, rng.uniform(-60, W + 60), y, rng.uniform(1.3, 2.3), body="#1E1C45", rim="#8E4A6E", a=0.9, seed=i)
        v2.speed_streaks(c, W, H, t, 0.9 * min(1.0, speed), seed=3, n=34)

    def draw_fall(self, c, t):
        T = self.T
        self.fall_sky(c, t, T["cut_fall"], 0.42)
        u = prog(t, T["cut_fall"], T["cut_pad"])
        rx = W / 2 + math.sin(t * 2.1) * 10
        ry = lerp(700, 800, u) + math.sin(t * 3.3) * 8
        bu = prog(t, T["faster"] - 0.15, T["bullet"] + 0.55)     # the bullet it overtakes
        if 0 < bu < 1:
            bx, by = W / 2 + 290, lerp(1250, 190, e_io(bu))
            c.save()
            c.translate(bx, by)
            c.scale(1.9, 1.9)
            c.translate(-bx, -by)
            pl = lin_paint(bx, by - 170, bx, by - 30, [("#FFFFFF", 0.0), ("#FFFFFF", 0.6)])
            pl.setStyle(skia.Paint.kStroke_Style)
            pl.setStrokeWidth(6)
            c.drawLine(bx, by - 170, bx, by - 30, pl)
            path = skia.Path()
            path.moveTo(bx - 13, by - 34)
            path.lineTo(bx + 13, by - 34)
            path.lineTo(bx + 13, by + 8)
            path.quadTo(bx + 11, by + 34, bx, by + 42)
            path.quadTo(bx - 11, by + 34, bx - 13, by + 8)
            path.close()
            cyl_path(c, path, bx - 13, bx + 13, "#D9A441", depth=1.2)
            c.drawRect(R(bx - 13, by - 34, 26, 6), P("#7A5A22", 0.8))
            c.restore()
        c.save()
        c.translate(rx, ry)
        c.rotate(math.sin(t * 2.7) * 2.5)
        draw_rocket(c, 0, 0, 180, t, heat=clamp((t - T["cut_fall"]) * 3), s=1.22)
        c.restore()
        self.ui["fall"] = (rx, ry)

    # ------------------------------------------------------------------ set 3: high up (fix 1)
    def draw_space(self, c, t):
        T = self.T
        braking = e_io(prog(t, T["relight"] + 0.1, T["brake"] + 0.9))
        v2.sky(c, W, H, 1.0)
        v2.stars(c, W, H, t, 1.0, n=320, seed=2, dy=-(t * lerp(90, 14, braking)))
        v2.earth_limb(c, W, H, 1.0, y=H * 0.80 - 30 * braking)
        v2.speed_streaks(c, W, H, t, 0.75 * (1 - 0.85 * braking), seed=9, n=30)
        ang = self.flip.at(t)
        burn = clamp((t - T["relight"]) * 5) * (0.82 + 0.18 * math.sin(t * 5))
        g0 = bump(t, T["gas"], T["flip"] + 0.25)                # first jet starts the turn
        g1 = bump(t, T["flip"] + 0.55, T["flip"] + 1.15)        # opposite jet stops it
        rx = W / 2 + math.sin(t * 1.3) * 6
        ry = lerp(700, 760, e_io(prog(t, T["cut_space"], T["cut_fall2"]))) + math.sin(t * 2.1) * 5
        if burn > 0:
            add_glow(c, rx, ry + 520, 520, "#FF8A3D", 0.30 * burn)
        draw_rocket(c, rx, ry, ang, t, flame=burn, gas=(g1, g0), warm=burn * 0.7, s=1.12, fl_len=560,
                    heat=clamp(1 - (t - T["cut_space"]) * 0.9) * 0.55 * (1 - prog(t, T["flip"], T["flip"] + 0.5)))
        self.ui["space"] = (rx, ry, ang)

    # ------------------------------------------------------------------ set 4: in the clouds, tail first (break 2, fix 2)
    def draw_fall2(self, c, t):
        T, s = self.T, self.tl.s
        self.fall_sky(c, t, T["cut_fall2"], 0.36, speed=0.62, seed=50)
        tg = T["grid"] + 0.35
        w0 = 26 * math.sin((T["tumble"] - T["air"]) * 9)
        if t < T["tumble"]:                                      # the wobble grows...
            ang = 26 * e_in(prog(t, T["air"], T["tumble"])) * math.sin((t - T["air"]) * 9)
        elif t < tg:                                             # ...into a full tumble
            ang = w0 + 470 * e_io(prog(t, T["tumble"], tg))
        else:                                                    # the fins catch the air and it settles
            dt_ = t - tg
            ang = 360 + (w0 + 470 - 360) * math.exp(-3.2 * dt_) * math.cos(7.5 * dt_)
        fins = None if t < T["grid"] else prog(t, T["grid"], T["grid"] + 0.45)
        st = t - T["steer"]
        tilt = 16 * math.sin(st * 5.5) * clamp(st * 3) * clamp(1.6 - st * 0.9) if st > 0 else 0.0
        drift = 150 * math.sin(st * 2.3) * math.exp(-st * 1.1) * clamp(st * 2) if st > 0 else 0.0
        rx = W / 2 + drift + math.sin(t * 1.9) * 6
        ry = 770 + math.sin(t * 2.4) * 8
        cut_off = 1 - prog(t, s("break2") + 0.15, s("break2") + 0.7)
        if st > -0.2:                                            # where it is steering to
            a_ = clamp((st + 0.2) * 3)
            c.drawLine(W / 2, ry + 430, W / 2, 1590, dash_paint("#FACC15", 0.55 * a_, 4, t))
            for r_, al in ((54, 0.9), (30, 0.9)):
                c.drawCircle(W / 2, 1640, r_, P("#FACC15", al * a_, stroke=6))
            add_glow(c, W / 2, 1640, 150, "#FACC15", 0.35 * a_)
        pu = prog(t, T["pencil"] - 0.45, T["pencil"] + 0.95)     # the pencil it tumbles like
        if 0 < pu < 1:
            pencil(c, W / 2 + 300, lerp(-260, 1500, pu), t * 520, 1.25)
        draw_rocket(c, rx, ry, ang, t, flame=cut_off * 0.7, warm=cut_off * 0.5, s=1.05, fl_len=420, soot=0.35, fins=fins,
                    fin_tilt=tilt)
        self.ui["fall2"] = (rx, ry, ang)

    # ------------------------------------------------------------------ set 5: the landing zone (break 3 - fix 4)
    def lz_state(self, t):
        """(height of the rocket's lowest point above the pad, lean angle, engine power, legs, phase)."""
        T, s = self.T, self.tl.s
        if t < T["cut_retry"]:
            legs = None
            if t < T["hover"] - 0.1:                             # break 3: comes down, can't stay down, climbs away
                h = lerp(1700, 250, e_out(prog(t, T["cut_lz"], T["lowest"]))) + 14 * math.sin(t * 5)
                h += 1900 * e_in(prog(t, T["pushes"], T["up"] + 0.6))
                return h, 0.0, 0.62, legs, "b3"
            if t < T["burn"]:                                    # fix 3: free fall, engine off
                return lerp(2300, 760, e_in(prog(t, T["burn"] - 0.85, T["burn"]))), 0.0, 0.0, legs, "f3"
            if t < T["tip0"]:                                    # one burn, zero speed at zero height, then it stands
                p = prog(t, T["burn"], T["touch3"])
                return 760 * (1 - p) ** 2, 0.0, (1.0 if p < 1 else 0.0), legs, "f3"
            return 0.0, -90 * e_in(prog(t, T["tip0"], T["fall4"])), 0.0, legs, "b4"      # break 4: over it goes
        legs = 0.0 if t < T["fold"] else prog(t, T["fold"], T["fold"] + 0.55)           # fix 4: the same landing, on legs
        p = prog(t, T["cut_retry"], T["touch4"])
        return 1150 * (1 - p) ** 2, 0.0, (1.0 if p < 1 else 0.0), legs, "f4"

    def draw_lz(self, c, t):
        T = self.T
        cx, cy, z = self.cam_lz.at(t)
        cx += math.sin(t * 0.7) * 3
        gy = (0 - cy) * z + H / 2
        h, lean, power, legs, ph = self.lz_state(t)
        power *= 0.86 + 0.14 * math.sin(t * 6)
        self.backdrop(c, t, cx, cy, gy)
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)
        v2.ground(c, -3200, 3200)
        buried_line(c, [(470, 0), (470, 190), (-250, 190), (-250, 10)], "#60A5FA", t, 0.8, w=7)
        bunker(c, 352, t, lit=power * clamp(1 - h / 900))
        landing_zone(c, t)
        surf = -16.0
        if power > 0 and h < 1500:                               # the plume lights the pad
            add_glow(c, 0, surf, 900, "#FF8A3D", 0.42 * power * clamp(1 - h / 1300))
        floodlight(c, -590, 250, -20, -420, t, 1.0)
        floodlight(c, 590, 228, 20, -380, t, 1.0)
        if T["tall"] - 0.15 <= t < T["fall4"]:                   # scale: a fourteen-storey building
            building_ghost(c, 150, 190, BH + NH + 58, 14, prog(t, T["tall"] - 0.15, T["tall"] + 0.25) * (1 - prog(t, T["tip0"], T["tip0"] + 0.3)))
        stand = STAND_LEGS if (legs is not None and legs > 0.5) else STAND
        crashed = ph == "b4" and t >= T["fall4"]
        if not crashed:
            a_ = math.radians(lean)
            px, py = (-BW / 2 if lean < 0 else 0.0), surf        # it pivots on the edge of its base when it tips
            ox = 0.0 if lean == 0 else -BW / 2
            rx = px + (0 - ox) * math.cos(a_) + stand * math.sin(a_)
            ry = py - h - stand * math.cos(a_) + (0 - ox) * math.sin(a_)
            if h < 600 and lean == 0:
                contact_shadow(c, 0, surf + 2, 190 + 260 * clamp(1 - h / 600), 0.55 * clamp(1 - h / 600), 22)
            dip = 0.0
            if ph == "f4" and t >= T["touch4"]:                  # the legs take the hit
                dt_ = t - T["touch4"]
                dip = 16 * math.exp(-7 * dt_) * math.cos(16 * dt_)
            if ph == "f3" and t >= T["touch3"] and t < T["tip0"]:
                dt_ = t - T["touch3"]
                dip = 6 * math.exp(-8 * dt_) * math.cos(20 * dt_)
            if ry > cy - H / z - 500:
                draw_rocket(c, rx, ry + dip, lean, t, flame=power, warm=power * 0.8, fl_len=470, soot=0.45, fins=1.0, legs=legs)
            self.ui["lz"] = ((rx - cx) * z + W / 2, (ry + dip - cy) * z + H / 2, z, lean, h)
            for t0 in ((T["touch3"],) if ph in ("f3", "b4") else ()) + ((T["touch4"],) if ph == "f4" else ()):
                if t >= t0:                                      # dust ring on touchdown
                    v2.smoke(c, 0, surf - 6, t, t0, t0 + 0.25, rate=70, life=1.5, spread=(560, -16), rise=-18, size=(26, 110),
                             col="#AEB5C8", lit=None, lit_until=0, seed=21, drag=2.6, a=0.7)
        else:                                                    # it lands on its side and that is that
            v2.smoke(c, -330, 10, t, T["fall4"] + 0.2, T["fall4"] + 9, rate=12, life=3.4, spread=(150, -280), rise=-80,
                     size=(46, 180), col="#6A7086", lit="#FF7A2F", lit_until=1.3, seed=31, drag=1.0)
            v2.fireball(c, -330, -30, t, T["fall4"], 1.7, 380, seed=4)
            v2.shock_ring(c, -330, -16, t, T["fall4"], 0.7, 1300)
            v2.debris(c, -330, -30, t, T["fall4"], 3.0, n=20, speed=1150, floor=surf, seed=8)
            v2.embers(c, -330, -30, t, T["fall4"], 1.6, n=60, speed=1400, seed=10)
            add_glow(c, -330, -60, 1500, "#FFE9C9", clamp(1 - (t - T["fall4"]) * 5) * 0.9)
        if ph == "b3":
            pose, soot = ("look" if t >= T["pushes"] else "stand"), 0.0
        elif ph == "f3":
            pose, soot = ("cheer" if t >= T["touch3"] else "point"), 0.0
        elif ph == "b4":
            pose = "cheer" if t < T["tall"] else "stand" if t < T["tip0"] else "duck" if t < T["fall4"] + 1.0 else "stand"
            soot = clamp((t - T["fall4"]) * 3)
        else:
            pose, soot = ("cheer" if t >= T["touch4"] + 0.15 else "look"), 0.0
        self.crew(c, t, pose, soot)
        c.restore()

    # ------------------------------------------------------------------ set 6: the ocean (reveal, numbers, closer, joke)
    def draw_sea(self, c, t):
        T, s = self.T, self.tl.s
        cx, cy, z = self.cam_sea.at(t)
        cx += math.sin(t * 0.6) * 4
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx, cy, gy, sea_=True)
        add_glow(c, 236 - cx * 0.02, gy, 500, "#9DB7FF", 0.16)
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)
        sea(c, -3200, 3200, t, moon_x=-330)
        ship_x = lerp(1400, 70, e_out(prog(t, T["cut_sea"], T["park"] + 0.75)))
        landed = t >= T["deck"]
        bob = math.sin(t * 1.1) * 4
        tug(c, -540, t)                                          # the crew came by boat
        hats_in_the_air(c, (-580, -536, -492), -150, t, T["cong2"])
        self.crew(c, t, "cheer" if (landed and t < s("tag")) else "look", 0.0, xs=(-580, -536, -492), y=-30 + math.sin(t * 1.3 + 1) * 5, face=1)
        droneship(c, ship_x, t, target=prog(t, T["draw"], T["draw"] + 0.7), name_glow=prog(t, T["course"] - 0.1, T["course"] + 0.4))
        deck = -60.0 + bob
        if t >= T["land"] - 1.35:                                # down it comes, legs out
            p = prog(t, T["land"] - 1.35, T["deck"])
            h = 1500 * (1 - p) ** 2
            power = (0.9 + 0.1 * math.sin(t * 6)) if p < 1 else 0.0
            dt_ = t - T["deck"]
            dip = 14 * math.exp(-7 * dt_) * math.cos(16 * dt_) if dt_ >= 0 else 0.0
            if power > 0:
                add_glow(c, ship_x, deck, 800, "#FF8A3D", 0.40 * clamp(1 - h / 1200))
            if h < 500:
                contact_shadow(c, ship_x, deck + 2, 200 + 240 * clamp(1 - h / 500), 0.5 * clamp(1 - h / 500), 20)
            draw_rocket(c, ship_x, deck - h - STAND_LEGS + dip, 0, t, flame=power, warm=power * 0.8, fl_len=470, soot=0.5,
                        fins=1.0, legs=prog(t, T["land"] - 0.9, T["land"] - 0.35))
            if dt_ >= 0:
                v2.smoke(c, ship_x, deck - 4, t, T["deck"], T["deck"] + 0.3, rate=60, life=1.7, spread=(520, -14), rise=-22,
                         size=(26, 110), col="#C5CCDA", lit=None, lit_until=0, seed=41, drag=2.4, a=0.7)
        for k in range(3):                                       # waves in front of the hull
            path = skia.Path()
            yy = 44 + k * 10
            path.moveTo(-3200, yy + 60)
            xx = -3200
            while xx < 3200:
                xx += 36
                path.lineTo(xx, yy + math.sin(xx * 0.016 + t * (1.6 + k * 0.4) + k * 2) * 6)
            path.lineTo(3200, yy + 60)
            path.close()
            c.drawPath(path, P(["#132452", "#0F1C44", "#0C1738"][k], 0.92))
        if t >= T["course"] + 0.75:                              # even engineers have feelings
            u = prog(t, T["course"] + 0.75, T["course"] + 2.6)
            heart(c, 320 + math.sin(u * 5) * 16, -30 - 170 * e_out(u), 0.55 + 0.25 * e_back(clamp(u * 3)), clamp(u * 5) * (1 - prog(u, 0.8, 1.0)))
        c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, self.SKY_ALT.get(m, 0.0), horizon_y=H * (1.5 if m.startswith("fall") else 0.66))
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ UI on top of the finished picture, per set
    def ui_pad(self, c, t, tw):
        T = self.T
        p = self.span(T["wait"] + 0.05, T["congrats"] + 0.75)
        if p > 0:
            v2.chip(c, W / 2, 470, f"T+ 0{int(lerp(1, 8, prog(tw, T['wait'], T['congrats'] + 0.5)))}:00", p, accent=ACCENT)
        if "star" in self.ui and tw >= T["lands"] - 0.5:
            fx_, fy_ = self.ui["star"]
            self.label(fx_, fy_, fx_ - 300, fy_ + 150, "yours", T["lands"] - 0.5, T["cut_fall"] + 1, HILITE)
        self.badge("alert", T["impact"] + 0.25, T["cut_space"] - 0.05)
        self.red(T["impact"])

    def ui_fall(self, c, t, tw):
        T = self.T
        rx, ry = self.ui.get("fall", (W / 2, 750))
        self.label(rx, ry + 440, rx - 280, ry + 250, "nose", T["nose"] - 0.05, T["faster"] + 0.3, WARN)

    def ui_space(self, c, t, tw):
        T = self.T
        rx, ry, ang = self.ui.get("space", (W / 2, 720, 180))
        a_ = math.radians(ang)

        def pt(lx, ly):                                          # rocket-local point -> screen
            lx, ly = lx * 1.12, ly * 1.12
            return rx + lx * math.cos(a_) - ly * math.sin(a_), ry + lx * math.sin(a_) + ly * math.cos(a_)
        gx, gy = pt(BW / 2 + 6, -BH / 2 + 35)
        self.label(gx, gy, 800, 1090 if ang > 90 else 300, "gas", T["gas"], T["flip"] + 0.30)
        ex, ey = pt(-BW / 2 - 4, BH / 2 + 20)
        self.label(ex, ey, 250, ey + 10, "relit", T["relight"] + 0.05, T["tail"] + 0.15, "#FFB05C")
        self.badge("check", T["tail"], T["cut_fall2"] - 0.02)

    def ui_fall2(self, c, t, tw):
        T = self.T
        rx, ry, ang = self.ui.get("fall2", (W / 2, 770, 0))
        self.badge("alert", T["tumble"] + 0.2, T["grid"] + 0.1)
        self.red(T["tumble"], 1.6)
        if tw >= T["grid"] + 0.35:
            fx_, fy_ = rx + 92, ry - (BH / 2 - 66) * 1.05
            self.label(fx_, fy_, 820, fy_ - 130, "fins", T["grid"] + 0.35, T["waffle"] - 0.05)
            self.chip(800, fy_ - 120, "waffle", T["waffle"], T["steer"] - 0.05, accent=HILITE, size=36)
        self.badge("check", T["down"] - 0.25, T["cut_lz"] - 0.02)

    def ui_lz(self, c, t, tw):
        T, L = self.T, self.L
        sx, sy, z, lean, h = self.ui.get("lz", (W / 2, 700, 0.8, 0, 0))
        if tw < T["cut_retry"]:
            ex, ey = sx - 46 * z, sy + (BH / 2 + 30) * z
            self.label(ex, ey, 240, max(380, ey - 40), "throttle", T["lowest"] - 0.1, T["up"] + 0.2, "#FFB05C")
            self.badge("alert", T["pushes"] + 0.3, T["hover"] + 0.2)
            self.red(T["pushes"] + 0.2, 1.8)
            self.chip(W / 2, 470, "nohover", T["hover"] - 0.05, T["burn"] - 0.25, accent=WARN)
            pg = self.span(T["burn"] - 0.7, T["touch3"] + 1.2)
            if pg > 0:
                pb = prog(tw, T["burn"], T["touch3"])
                v2.gauge(c, 56, 560, [(L["speed"], (1 - pb) if tw >= T["burn"] else 1.0, "#FB923C"),
                                      (L["height"], clamp(h / 760) if tw >= T["burn"] else 1.0, "#38BDF8")], pg, w=310)
            self.label(sx - 46 * z, sy + (BH / 2 + 60) * z, 250, 1010, "burn", T["burn"] + 0.05, T["zero"] + 0.25, "#FFB05C")
            self.chip(W / 2, 470, "touch", T["touch3"] + 0.02, T["softly"] + 0.5, accent=GOOD)
            self.badge("check", T["touch3"] + 0.1, T["softly"] + 0.7)
            if self.span(T["tall"], T["tip0"] + 0.1) > 0:
                bx_, by_ = self.to_screen(self.cam_lz.at(tw), 245, -(BH + NH + 58))
                self.chip(bx_, by_ - 46, "floors", T["tall"], T["tip0"] + 0.1, size=36)
            self.badge("alert", T["fall4"] + 0.25, T["cut_retry"] - 0.05)
            self.red(T["fall4"])
        else:
            lx, ly = sx + 150 * z, sy + (BH / 2 + 80) * z
            self.label(lx, ly, 830, ly - 170, "legs", T["fold"] + 0.3, T["crush"] - 0.1)
            pc = self.span(T["crush"], T["cut_sea"] - 0.1)
            if pc > 0:                                           # magnifier: the crush core inside a leg
                self.crush_inset(c, 230, 640, pc, clamp((tw - T["touch4"]) * 6) if tw >= T["touch4"] else 0.0, t)
            self.badge("check", T["touch4"] + 0.2, T["cut_sea"] - 0.05)

    def crush_inset(self, c, x, y, p, crush, t):
        """Round magnifier showing the honeycomb core inside a leg strut, squashing on touchdown."""
        k = e_back(clamp(p))
        a = clamp(p * 3)
        r = 150
        c.save()
        c.translate(x, y)
        c.scale(k, k)
        c.drawCircle(0, 8, r + 6, P("#000000", 0.4 * a, blur=16))
        c.drawCircle(0, 0, r, P("#0B1220", 0.94 * a))
        c.save()
        clip = skia.Path()
        clip.addCircle(0, 0, r - 6)
        c.clipPath(clip, doAntiAlias=True)
        v2.cyl(c, -70, -160, 140, 320, "#C9D0DE", a=a)           # strut tube
        hgt = lerp(190, 96, e_out(crush))                        # honeycomb core: tall, then crushed
        top = 70 - hgt
        c.drawRect(R(-52, top, 104, hgt), P("#1F2637", a))
        rows = 9
        for i in range(rows):
            yy = top + (i + 0.5) * hgt / rows
            for j in range(6):
                xx = -44 + j * 17.6 + (8.8 if i % 2 else 0)
                c.drawCircle(xx, yy, min(7.5, hgt / rows * 0.46), P("#FACC15", 0.9 * a, stroke=2.5))
        v2.box(c, -58, top - 64, 116, 64, "#8D96AB", r=6, a=a)   # piston pushing down on the core
        if crush > 0:
            v2.add_glow(c, 0, top, 120, "#FFB05C", 0.5 * (1 - crush) * a)
        c.restore()
        c.drawCircle(0, 0, r, P("#FFFFFF", 0.9 * a, stroke=5))
        c.drawCircle(0, 0, r, P(ACCENT, 0.9 * a, stroke=2))
        c.restore()
        v2.chip(c, x, y + (r + 46) * k, self.L["crush"], p, size=34, accent=ACCENT)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, True, 60), -10), (0.2, sfx.pop(61), -8)]
        ev += [(T["launch"] - 0.05, rumble(2.6), 0), (T["launch"], sfx.whoosh(1.2, True, 62), -4)]
        ev += [(T["wait"] + 0.05 + i * 0.16, sfx.tick(), -12) for i in range(5)]
        ev += [(T["lands"] - 0.5, sfx.pop(63), -6)]
        ev += [(T["cut_fall"] - 0.12, sfx.whoosh(0.4, True, 64), -3), (T["cut_fall"], rumble(2.2, 44), -7),
               (T["nose"] - 0.05, sfx.pop(65), -6), (T["faster"] - 0.1, sfx.whoosh(0.7, True, 66), -6)]
        ev += [(T["cut_pad"] - 0.12, sfx.whoosh(0.4, False, 67), -3), (T["impact"] - 0.2, sfx.whoosh(0.25, False, 68), -2),
               (T["impact"], boom(), 2), (T["impact"] + 0.3, sfx.alarm(3, 820), -10)]
        ev += [(T["cut_space"] - 0.12, sfx.whoosh(0.45, True, 69), -3), (T["gas"], gas_hiss(0.9), -4),
               (T["gas"], sfx.pop(70), -8), (T["flip"] + 0.55, gas_hiss(0.6, 43), -5),
               (T["relight"], rumble(2.4, 45), -5), (T["relight"], sfx.charge_up(0.5), -8), (T["relight"] + 0.05, sfx.pop(71), -8),
               (T["tail"], sfx.chime(), -4), (T["tail"], sfx.sparkle(0.7, 9, 72), -8)]
        ev += [(T["cut_fall2"] - 0.12, sfx.whoosh(0.4, False, 73), -3), (s("break2") + 0.15, sfx.power_down(0.8, 74), -8),
               (T["air"], sfx.whoosh(0.9, True, 75), -8), (T["tumble"], sfx.whirr(1.6, 180, 420, 76), -8),
               (T["tumble"] + 0.2, sfx.alarm(3, 820), -11), (T["pencil"] - 0.3, sfx.whoosh(0.5, False, 77), -8)]
        ev += [(T["grid"], sfx.clank(520, 0.35, 78), -4), (T["grid"] + 0.12, sfx.clank(640, 0.3, 79), -6),
               (T["grid"] + 0.4, sfx.pop(80), -8), (T["waffle"], sfx.pop(81), -6), (T["steer"], sfx.whirr(1.0, 240, 300, 82), -10),
               (T["down"] - 0.25, sfx.chime(), -5)]
        ev += [(T["cut_lz"] - 0.12, sfx.whoosh(0.4, False, 83), -3), (T["cut_lz"], rumble(3.6, 46), -6),
               (T["lowest"] - 0.1, sfx.pop(84), -8), (T["pushes"], sfx.whoosh(1.3, True, 85), -5),
               (T["pushes"] + 0.3, sfx.alarm(3, 820), -11), (T["hover"] - 0.05, sfx.buzz(), -8)]
        ev += [(T["burn"] - 0.8, sfx.whoosh(0.8, False, 86), -6), (T["burn"], rumble(2.6, 47), -4), (T["burn"] + 0.05, sfx.pop(87), -8),
               (T["touch3"], sfx.thud(0.4, 88), -3), (T["touch3"] + 0.08, sfx.ding(), -6), (T["touch3"] + 0.2, sfx.chime(), -6)]
        ev += [(T["tall"], sfx.pop(89), -8), (T["tips"], sfx.creak(0.8, 90), -4), (T["fall4"], boom(1.6, 48), 1),
               (T["fall4"] + 0.3, sfx.alarm(3, 820), -11)]
        ev += [(T["cut_retry"] - 0.1, sfx.whoosh(0.4, True, 91), -3), (T["cut_retry"], rumble(4.2, 49), -7),
               (T["fold"], sfx.clank(420, 0.4, 92), -4), (T["fold"] + 0.3, sfx.lock_click(93), -4), (T["crush"], sfx.pop(94), -8),
               (T["touch4"], sfx.thud(0.45, 95), -3), (T["touch4"] + 0.05, sfx.creak(0.5, 96), -9), (T["touch4"] + 0.25, sfx.chime(), -5)]
        ev += [(T["pause"], sfx.click(97), 0), (T["follow"] - 0.15, sfx.pop(98), -4)]
        ev += [(T["cut_sea"] - 0.12, sfx.whoosh(0.45, False, 99), -3), (T["park"] - 0.2, sfx.whoosh(1.2, False, 100), -9),
               (T["draw"], sfx.sparkle(0.7, 8, 101), -8), (T["land"] - 1.3, rumble(2.2, 50), -6), (T["deck"], sfx.thud(0.45, 102), -3),
               (T["deck"] + 0.1, sfx.hiss(0.7, 103), -12), (T["deck"] + 0.25, sfx.chime(), -6)]
        ev += [(T["s1"], sfx.pop(104), -3), (T["s2"], sfx.pop(105), -3), (T["s3"], sfx.pop(106), -3),
               (T["s1"] - 0.3, sfx.whoosh(1.4, False, 107), -12)]
        ev += [(T["cong2"], sfx.pop(108), -2), (T["cong2"], sfx.sparkle(1.0, 14, 109), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.22, sfx.whoosh(0.45, False, 110), -6), (T["course"] + 0.75, sfx.sparkle(0.6, 6, 111), -8),
               (T["feelings"] + 0.35, sfx.womp(), -2)]
        return ev


NAME = "rocket"
EPISODE = Rocket
