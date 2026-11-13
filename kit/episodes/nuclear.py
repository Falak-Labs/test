"""Episode 24 - A nuclear power plant.  v2 look: dusk and night, seven sets with whip cuts.

Sets: pot (a pot of water boiling on a glowing bundle of uranium rods; the crew watches), core (close-up of the core
in its water: atoms split faster and faster until the rods melt; control rods slide in and soak up the neutrons, a
power gauge follows them in and out), vessel (the reactor vessel in its hall: switched off it still glows, the pump
stops, the water boils away; backup pumps, diesel generators and a tank up high that pours in by itself), loops (one
loop sends glowing radioactive water into the turbine; then two loops: a sealed hot loop through a steam generator
and a clean loop whose steam spins the turbine), site (the plain building shaken by an earthquake, a flood and a
little plane; then the steel shell and the thick concrete dome, and the plane bounces off), plant (the finished plant
at dusk: two giant cooling towers rise and puff steam; the stat shot and the cheer), kettle (the tag: the scary tower
turns into the world's biggest kettle; in Arabic it pours a glass of tea).
Ground sets: the floor is y = 0, up is negative.  The core is a close-up board.
"""
import bisect

from v2_base import *  # noqa: F401,F403

URAN, URAN_D, NEUT = "#86EFAC", "#15803D", "#7DD3FC"
ROD, HOTC = "#8C94A8", "#FF6A2B"
WATER, WATER_D, RADC, STEAMC = "#1D5FA8", "#0B2D5C", "#A3E635", "#E8EEF8"
CONC, STEELC, TEA, PRIM = "#B9BFCC", "#7F8CA3", "#C2410C", "#FB923C"
SKINS = ("#E8B48A", "#C68B5E", "#F1C9A5", "#8D5A3B", "#E0A47A")
XR = (-240, -80, 80, 240)                     # control rods (set "core")


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def along(pts, u):
    segs = [(pts[i], pts[i + 1], math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]
    total = sum(s_[2] for s_ in segs)
    d = (u % 1.0) * total
    for (a_, b_, ln) in segs:
        if d <= ln:
            k = d / ln if ln else 0
            return a_[0] + (b_[0] - a_[0]) * k, a_[1] + (b_[1] - a_[1]) * k
        d -= ln
    return pts[-1]


def pipe(c, pts, col="#7C8499", w=22, a=1.0):
    if a <= 0:
        return
    path = skia.Path()
    path.moveTo(*pts[0])
    for p_ in pts[1:]:
        path.lineTo(*p_)
    c.drawPath(path, P("#1B2236", a, stroke=w + 8))
    c.drawPath(path, P(col, a, stroke=w))
    c.drawPath(path, P("#FFFFFF", 0.18 * a, stroke=w * 0.3))


def flow(c, pts, ph, k, n=10, col=NEUT, r=6, glow=0.0):
    """Dots moving along pts; ph = distance travelled as a fraction of the loop (grows with time)."""
    if k <= 0:
        return
    for i in range(n):
        x, y = along(pts, (ph + i / n) % 1.0)
        if glow > 0:
            add_glow(c, x, y, r * 4, col, glow * k)
        c.drawCircle(x, y, r, P(col, 0.95 * k))


class Integral:
    """Running integral of f(t) sampled at 60 Hz (smooth spins that speed up and slow down)."""

    def __init__(self, f, t0, t1):
        self.t0, self.dt = t0, 1.0 / 60
        acc, self.v = 0.0, []
        for i in range(int((t1 - t0) * 60) + 3):
            self.v.append(acc)
            acc += f(t0 + i * self.dt) * self.dt

    def at(self, t):
        i = (t - self.t0) / self.dt
        if i <= 0:
            return self.v[0]
        j = min(int(i), len(self.v) - 2)
        return lerp(self.v[j], self.v[j + 1], clamp(i - j))


def trefoil(c, x, y, r, a=1.0, col="#FACC15", ink="#111827"):
    """The radiation sign."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P(col, a))
    c.drawCircle(x, y, r, P(ink, a, stroke=max(1.5, r * 0.08)))
    for k in range(3):
        path = skia.Path()
        path.moveTo(x, y)
        path.arcTo(R(x - r * 0.82, y - r * 0.82, r * 1.64, r * 1.64), -120 + k * 120, 60, False)
        path.close()
        c.drawPath(path, P(ink, a))
    c.drawCircle(x, y, r * 0.3, P(col, a))
    c.drawCircle(x, y, r * 0.18, P(ink, a))


def fuel_rod(c, x, y0, y1, w, heat, melt=0.0, t=0.0, seed=0, a=1.0):
    """A fuel rod standing from y0 (top) to y1 (bottom), centred on x. heat 0..1 colours it, melt 0..1 sags it."""
    if a <= 0:
        return
    col = mix(ROD, HOTC, clamp(heat * 1.25))
    if heat > 0.78:
        col = mix(col, "#FFE08A", (heat - 0.78) * 3)
    sag = melt * 46
    path = skia.Path()
    path.moveTo(x - w / 2, y0 + w / 2)
    path.quadTo(x - w / 2, y0, x, y0)
    path.quadTo(x + w / 2, y0, x + w / 2, y0 + w / 2)
    path.lineTo(x + w / 2 + sag * 0.45, y1 - 24 + sag * 0.5)
    path.quadTo(x + sag * 0.2, y1 + sag * 1.1, x - w / 2 - sag * 0.45, y1 - 24 + sag * 0.5)
    path.close()
    c.drawPath(path, lin_paint(x - w / 2, 0, x + w / 2, 0, [shade(col, -0.3), shade(col, 0.28), col, shade(col, -0.35)],
                                [0.0, 0.3, 0.6, 1.0], a))
    yy = y0 + 40
    while yy < y1 - 16:
        c.drawLine(x - w / 2 + 4, yy, x + w / 2 - 4, yy, P("#000000", 0.16 * a, stroke=2))
        yy += 46
    if heat > 0.3:
        add_glow(c, x, (y0 + y1) / 2, w * 2.4, HOTC, 0.32 * (heat - 0.3) * a)
    if melt > 0:
        for i in range(3):
            u = (t * 0.9 + i * 0.33 + seed * 0.17) % 1.0
            c.drawCircle(x + (i - 1) * w * 0.28, y1 + sag + u * u * 170, 9 * (1 - u * 0.5), P(HOTC, melt * (1 - u) * a))


def atom(c, x, y, r, a=1.0):
    """A uranium atom: a green ball with a shine."""
    if a <= 0 or r <= 0:
        return
    c.drawCircle(x, y, r, rad_paint(x - r * 0.35, y - r * 0.4, r * 1.6, [("#F0FFF4", a), (URAN, a), (URAN_D, a)],
                                    [0.0, 0.35, 1.0]))
    c.drawCircle(x, y, r, P("#052E16", 0.35 * a, stroke=2))


def capsule(c, x0, y0, w, h, base, a=1.0):
    """An upright vessel with round ends (shaded steel)."""
    cyl(c, x0, y0, w, h, base, r=w / 2, a=a)


def pump(c, x, y, r, ang, on=1.0, a=1.0):
    """A pump seen from the side: round housing, spinning impeller, motor on top."""
    if a <= 0:
        return
    box(c, x - r * 0.45, y - r * 1.75, r * 0.9, r * 0.8, "#475569", r=6, a=a)
    c.drawCircle(x, y, r, rad_paint(x - r * 0.3, y - r * 0.3, r * 1.4, [shade("#64748B", 0.3), "#64748B", shade("#64748B", -0.4)], a=a))
    c.drawCircle(x, y, r * 0.72, P("#1E293B", a))
    for b in range(4):
        q = math.radians(ang + b * 90)
        c.drawLine(x, y, x + math.cos(q) * r * 0.66, y + math.sin(q) * r * 0.66, P("#CBD5E1", a, stroke=r * 0.16))
    c.drawCircle(x, y, r * 0.16, P("#94A3B8", a))
    if on > 0.5:
        c.drawCircle(x + r * 0.62, y - r * 1.55, 6, P(GOOD, a))
    else:
        c.drawCircle(x + r * 0.62, y - r * 1.55, 6, P(WARN, a))


def generator(c, x, y, t, run=0.0, w=170, h=120, a=1.0):
    """A diesel generator standing on y, left edge x. run 0..1: it shakes and smokes."""
    if a <= 0:
        return
    dx = math.sin(t * 60) * 2.0 * run
    box(c, x + dx, y - h, w, h, "#F59E0B", r=10, a=a)
    c.drawRect(R(x + 14 + dx, y - h + 18, w * 0.45, h * 0.6), P("#1F2937", a))
    for i in range(5):
        c.drawRect(R(x + 20 + dx + i * w * 0.08, y - h + 24, w * 0.04, h * 0.48), P("#374151", a))
    c.drawRect(R(x + w - 40 + dx, y - h - 70, 20, 76), P("#4B5563", a))
    word(c, "DIESEL", x + w * 0.74 + dx, y - 26, 22, "#1F2937", a)
    if run > 0:
        v2.smoke(c, x + w - 30 + dx, y - h - 74, t, 0.0, None, rate=10, life=1.5, spread=(50, -40), rise=-90, size=(12, 44),
                 col="#9CA3AF", lit=None, lit_until=0.0, a=0.8 * run)


def tower_path(x, w, h):
    hb, ht, hk = w / 2, w * 0.3, w * 0.335
    path = skia.Path()
    path.moveTo(x - hb, 0)
    path.quadTo(x - ht * 0.98, -0.5 * h, x - ht, -0.74 * h)
    path.quadTo(x - ht * 1.02, -0.9 * h, x - hk, -h)
    path.lineTo(x + hk, -h)
    path.quadTo(x + ht * 1.02, -0.9 * h, x + ht, -0.74 * h)
    path.quadTo(x + ht * 0.98, -0.5 * h, x + hb, 0)
    path.close()
    return path


def tower(c, x, w, h, k=1.0, a=1.0, lit=0.0):
    """A cooling tower standing on y = 0. k 0..1: it rises out of the ground."""
    if k <= 0 or a <= 0:
        return
    c.save()
    c.clipRect(R(x - w, -h - 400, w * 2, h + 400))
    c.translate(0, (1 - k) * h)
    cyl_path(c, tower_path(x, w, h), x - w / 2, x + w / 2, CONC, a=a, depth=0.9)
    for i in range(1, 6):                                                # faint rings of formwork
        yy = -h * i / 6
        hw = w / 2 * lerp(1.0, 0.62, i / 6)
        c.drawLine(x - hw, yy, x + hw, yy, P("#000000", 0.05 * a, stroke=2))
    c.drawOval(R(x - w * 0.335, -h - 12, w * 0.67, 24), P("#5B6274", a))
    c.drawOval(R(x - w * 0.31, -h - 7, w * 0.62, 14), P("#2A2F3D", a))
    c.drawRect(R(x - w / 2, -34, w, 34), P("#3B4252", a))                # the legs at the base
    for i in range(9):
        xx = x - w / 2 + 12 + i * (w - 24) / 8
        c.drawRect(R(xx - 5, -34, 10, 34), P("#9AA1B2", a))
    if lit > 0:
        add_glow(c, x, -h * 0.5, w * 0.7, "#FFD9A0", 0.08 * lit * a)
    c.restore()


def dome_path(r, x, y_base, y_spring):
    """Cylinder walls at +-r from y_base up to y_spring, closed by a half circle (an upside-down U)."""
    path = skia.Path()
    path.moveTo(x - r, y_base)
    path.lineTo(x - r, y_spring)
    path.arcTo(R(x - r, y_spring - r, 2 * r, 2 * r), 180, 180, False)
    path.lineTo(x + r, y_base)
    return path


def plane(c, x, y, s=1.0, rot=0.0, t=0.0, a=1.0):
    """A small cartoon propeller plane flying left (nose at -x)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    tail = skia.Path()
    tail.moveTo(46, -10)
    tail.lineTo(76, -52)
    tail.lineTo(92, -52)
    tail.lineTo(84, -8)
    tail.close()
    c.drawPath(tail, P("#EF4444", a))
    c.drawRRect(rr(-72, -16, 162, 32, 16), lin_paint(0, -16, 0, 16, ["#FFFFFF", "#CBD5E1"], a=a))
    c.drawRRect(rr(-54, -12, 26, 12, 5), P("#38BDF8", a))
    c.drawRRect(rr(-14, -2, 64, 14, 7), P("#94A3B8", a))
    c.drawRect(R(70, -6, 30, 6), P("#EF4444", a))
    blade = 30 * abs(math.sin(t * 40))
    c.drawOval(R(-84, -34, 10, 68), P("#E2E8F0", 0.35 * a))
    c.drawRRect(rr(-82, -blade, 6, blade * 2, 3), P("#475569", 0.8 * a))
    c.drawCircle(-76, 0, 6, P("#334155", a))
    c.restore()


def stars_ring(c, x, y, t, a=1.0):
    """Cartoon dizzy stars."""
    for i in range(4):
        q = t * 5 + i * math.pi / 2
        sx, sy = x + math.cos(q) * 44, y + math.sin(q) * 14
        path = skia.Path()
        for k in range(10):
            rr_ = 11 if k % 2 == 0 else 4.5
            qq = -math.pi / 2 + k * math.pi / 5
            (path.moveTo if k == 0 else path.lineTo)(sx + math.cos(qq) * rr_, sy + math.sin(qq) * rr_)
        path.close()
        c.drawPath(path, P("#FDE047", a))


def tea_glass(c, x, y, fill, a=1.0):
    """A small Egyptian tea glass standing on y, centred on x; fill 0..1."""
    if a <= 0:
        return
    w0, w1, h = 46, 34, 84
    path = skia.Path()
    path.moveTo(x - w0 / 2, y - h)
    path.lineTo(x + w0 / 2, y - h)
    path.lineTo(x + w1 / 2, y)
    path.lineTo(x - w1 / 2, y)
    path.close()
    if fill > 0:
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawRect(R(x - 30, y - h * fill * 0.9, 60, h), lin_paint(0, y - h, 0, y, ["#F59E0B", TEA], a=a))
        c.restore()
    c.drawPath(path, P("#E0F2FE", 0.22 * a))
    c.drawPath(path, P("#FFFFFF", 0.85 * a, stroke=3))
    c.drawRect(R(x - 22, y - 4, 44, 6), P("#E5E7EB", a))


def hall(c, cam, wall="#1C2340", tint=0.0, rad=0.0):
    """Inside the plant: a concrete back wall (screen space) and a lit floor (world; call inside view())."""
    cx, cy, z = cam
    c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, [mix(mix(wall, "#3A1414", tint), "#1F3A12", rad),
                                                     mix("#10162C", "#200A0A", tint)]))


def floor(c, cam):
    cx, cy, z = cam
    x0, x1 = cx - 760 / z, cx + 760 / z
    c.drawRect(R(x0, 0, x1 - x0, 1600), lin_paint(0, 0, 0, 500, ["#3B4160", "#141A2C"]))
    xx = int(x0) // 140 * 140
    while xx < x1:
        c.drawLine(xx, 0, xx - 70, 500, P("#FFFFFF", 0.05, stroke=2))
        xx += 140
    c.drawLine(x0, 0, x1, 0, P("#9AA6BF", 0.6, stroke=4))
    for xx in range(int(x0) // 400 * 400, int(x1), 400):               # wall posts and lamps
        c.drawRect(R(xx, -1500, 26, 1500), P("#2A3150", 0.8))
        add_glow(c, xx + 13, -980, 120, "#C7E7FF", 0.10)


# ---------------------------------------------------------------------------------------------- sounds
def whistle_snd(d=1.8, seed=70):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 2100 + 260 * np.minimum(1.0, tt / 0.5) + 25 * np.sin(2 * np.pi * 6 * tt)
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) + 0.3 * sfx._bp(sfx._rng(seed).standard_normal(n), 1800, 3200)
    return sfx._norm(x * sfx._ar(n, 0.12, 0.3), 0.55)


def boing_snd(d=0.7):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 420 * np.exp(-tt * 1.6) * (1 + 0.25 * np.sin(2 * np.pi * 14 * tt)) + 120
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR)
    return sfx._norm(x * np.exp(-tt * 4.0), 0.7)


def prop_snd(d=1.6, seed=71):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sign(np.sin(2 * np.pi * 52 * tt)) * 0.4 + sfx._lp(sfx._rng(seed).standard_normal(n), 900) * 0.6
    return sfx._norm(sfx._lp(x, 1400) * sfx._ar(n, 0.3, 0.4), 0.5)


def geiger_snd(d=1.4, seed=72, rate=18):
    n = int(d * sfx.SR)
    x = np.zeros(n)
    rng = sfx._rng(seed)
    for _ in range(int(d * rate)):
        i = int(rng.uniform(0, n - 400))
        x[i:i + 300] += rng.standard_normal(300) * np.exp(-np.arange(300) / 40)
    return sfx._norm(sfx._hp(x, 1500), 0.6)


def water_snd(d=1.4, seed=73):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 300, 2400)
    return sfx._norm(x * sfx._ar(n, 0.15, 0.4), 0.45)


def engine_snd(d=1.6, seed=74):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sign(np.sin(2 * np.pi * 34 * tt)) * 0.5 + sfx._lp(sfx._rng(seed).standard_normal(n), 300)
    return sfx._norm(sfx._lp(x, 700) * sfx._ar(n, 0.15, 0.3), 0.7)


# ====================================================================================== the episode
class Nuclear(EpisodeV2):
    BUILD_NO = 24
    FIRST_SET = "pot"
    CLEAR = "#070B1F"
    TITLE = {"en": "NUCLEAR POWER PLANT", "ar_sa": "محطة نووية"}
    EMPH = {"en": ["CONGRATS", "URANIUM", "BOIL", "NUCLEAR", "ATOMS", "SPLITTING", "FASTER", "MELT", "CONTROL", "RODS",
                   "NEUTRONS", "POWER", "STEADY", "OFF", "HEAT", "STOPS", "MELTS", "BACKUP", "PUMPS", "DIESEL",
                   "GENERATORS", "TANK", "HIGH", "OWN", "RADIOACTIVE", "TURBINE", "TWO", "LOOPS", "SEALED", "CLEAN",
                   "BOILS", "SPINS", "EARTHQUAKE", "FLOOD", "PLANE", "STEEL", "SHELL", "CONCRETE", "DOME", "METER",
                   "FOLLOW", "GIANT", "TOWERS", "STEAM", "ONE", "TON", "ZERO", "YOURSELF", "KETTLES"],
            "ar_sa": ["مبروك", "يورانيوم", "تغلي", "نووية", "الذرات", "بتنقسم", "أسرع", "يسيح", "قضبان", "النيوترونات",
                      "القوة", "ثابتة", "مطفية", "حرارة", "وقفت", "هيسيح", "طلمبات", "احتياطي", "ديزل", "وخزان", "فوق",
                      "لوحده", "مشعة", "التوربينة", "دايرتين", "مقفول", "نضيفة", "حديد", "خرسانة", "قبة", "متر",
                      "تابعني", "عملاقين", "برجين", "بخار", "حباية", "طن", "وصفر", "بإيدك", "براد", "شاي"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "URANIUM"): "يورانيوم", ("hook", "BOIL"): "تغلي", ("hook", "WATER"): "مية", ("hook", "CONGRATS"): "مبروك",
        ("hook", "NUCLEAR"): "نووية",
        ("break1", "ATOMS"): "الذرات", ("break1", "SPLITTING"): "بتنقسم", ("break1", "FASTER"): "أسرع",
        ("break1", "CORE"): "والقلب", ("break1", "HOT"): "بيسخن", ("break1", "MELT"): "يسيح",
        ("fix1", "CONTROL"): "قضبان", ("fix1", "SOAK"): "بتشفط", ("fix1", "NEUTRONS"): "النيوترونات",
        ("fix1", "SLIDE"): "تنزلها", ("fix1", "POWER"): "القوة",
        ("break2", "STEADY"): "ثابتة", ("break2", "SWITCHED"): "مطفية", ("break2", "HEAT"): "حرارة",
        ("break2", "WATER"): "المية", ("break2", "STOPS"): "وقفت", ("break2", "MELTS"): "هيسيح",
        ("fix2", "BACKUP"): "احتياطي", ("fix2", "PUMPS"): "طلمبات", ("fix2", "DIESEL"): "ديزل", ("fix2", "TANK"): "وخزان",
        ("fix2", "HIGH"): "فوق", ("fix2", "POURS"): "بينزل", ("fix2", "OWN"): "لوحده",
        ("break3", "TOUCHING"): "بتلمس", ("break3", "RADIOACTIVE"): "مشعة", ("break3", "SPINNING"): "تلف",
        ("break3", "TURBINE"): "التوربينة",
        ("fix3", "TWO"): "دايرتين", ("fix3", "LOOPS"): "دايرتين", ("fix3", "SEALED"): "مقفول", ("fix3", "HEATS"): "وتسخن",
        ("fix3", "CLEAN"): "نضيفة", ("fix3", "BOILS"): "تغلي", ("fix3", "SPINS"): "وتلف", ("fix3", "TURBINE"): "التوربينة",
        ("break4", "WORKS"): "شغالة", ("break4", "EARTHQUAKE"): "زلزال", ("break4", "FLOOD"): "فيضان",
        ("break4", "PLANE"): "طيارة", ("break4", "HITS"): "تخبط",
        ("fix4", "WRAP"): "فتلف", ("fix4", "STEEL"): "حديد", ("fix4", "CONCRETE"): "خرسانة", ("fix4", "DOME"): "قبة",
        ("fix4", "METER"): "متر",
        ("cta", "FLIP"): "تدوس", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "GIANT"): "عملاقين", ("reveal", "TOWERS"): "برجين", ("reveal", "PUFF"): "بيطلعش", ("reveal", "STEAM"): "بخار",
        ("stat", "ONE"): "حباية", ("stat", "TON"): "طن", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SCARY"): "خايفة", ("tag", "TOWERS"): "والأبراج", ("tag", "AFRAID"): "خايفة", ("tag", "BIGGEST"): "أكبر",
        ("tag", "KETTLES"): "براد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an aircraft carrier"),
                   "stat": [("1", "FUEL PELLET"), ("1", "TON OF COAL"), ("0", "SMOKE")],
                   "L": {"uranium": "URANIUM", "water": "WATER", "plant": "YOUR NUCLEAR POWER PLANT",
                         "split": "ATOMS SPLITTING", "melt": "MELTDOWN", "rods": "CONTROL RODS", "power": "POWER",
                         "steady": "STEADY", "off": "SWITCHED OFF", "heat": "STILL MAKING HEAT", "nowater": "PUMP STOPS",
                         "backup": "BACKUP PUMPS", "diesel": "DIESEL GENERATORS", "tank": "WATER TANK UP HIGH",
                         "gravity": "NO POWER NEEDED", "radio": "RADIOACTIVE", "turbine": "TURBINE", "loop1": "SEALED LOOP",
                         "loop2": "CLEAN WATER", "steam": "STEAM", "quake": "EARTHQUAKE", "flood": "FLOOD", "plane": "PLANE",
                         "steel": "STEEL SHELL", "concrete": "CONCRETE DOME", "thick": "1 METER+", "towers": "COOLING TOWERS",
                         "steam2": "JUST STEAM", "scary": "SCARY?", "kettle": "WORLD'S BIGGEST KETTLE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: حاملة طيارات"),
                      "stat": [("1", "حباية وقود"), ("1", "طن فحم"), ("0", "دخان")],
                      "L": {"uranium": "يورانيوم", "water": "مية", "plant": "محطتك النووية", "split": "الذرات بتنقسم",
                            "melt": "القلب بيسيح", "rods": "قضبان التحكم", "power": "القوة", "steady": "ثابتة",
                            "off": "مطفية", "heat": "لسه بتطلع حرارة", "nowater": "الطلمبة وقفت",
                            "backup": "طلمبات احتياطي", "diesel": "مولدات ديزل", "tank": "خزان مية فوق",
                            "gravity": "من غير كهربا", "radio": "مية مشعة", "turbine": "التوربينة", "loop1": "دايرة مقفولة",
                            "loop2": "مية نضيفة", "steam": "بخار", "quake": "زلزال", "flood": "فيضان", "plane": "طيارة",
                            "steel": "غلاف حديد", "concrete": "قبة خرسانة", "thick": "أكتر من متر",
                            "towers": "أبراج التبريد", "steam2": "بخار وبس", "scary": "مخيفة؟", "kettle": "أكبر براد شاي"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "uranium": ("hook", "URANIUM", 0.2), "boil": ("hook", "BOIL", 0.35), "water": ("hook", "WATER", 0.45),
            "congrats": ("hook", "CONGRATS", 0.6), "nuclear": ("hook", "NUCLEAR", 0.85),
            "atoms": ("break1", "ATOMS", 0.12), "splitting": ("break1", "SPLITTING", 0.25), "faster": ("break1", "FASTER", 0.4),
            "core": ("break1", "CORE", 0.65), "hot": ("break1", "HOT", 0.8), "melt": ("break1", "MELT", 0.95),
            "control": ("fix1", "CONTROL", 0.12), "soak": ("fix1", "SOAK", 0.3), "neutrons": ("fix1", "NEUTRONS", 0.48),
            "slide": ("fix1", "SLIDE", 0.62), "power": ("fix1", "POWER", 0.92),
            "steady": ("break2", "STEADY", 0.1), "switched": ("break2", "SWITCHED", 0.3), "heat": ("break2", "HEAT", 0.55),
            "water2": ("break2", "WATER", 0.7), "stops": ("break2", "STOPS", 0.8), "melts": ("break2", "MELTS", 0.9),
            "backup": ("fix2", "BACKUP", 0.12), "pumps": ("fix2", "PUMPS", 0.2), "diesel": ("fix2", "DIESEL", 0.35),
            "tank": ("fix2", "TANK", 0.6), "high": ("fix2", "HIGH", 0.7), "pours": ("fix2", "POURS", 0.8),
            "own": ("fix2", "OWN", 0.95),
            "touching": ("break3", "TOUCHING", 0.2), "radio": ("break3", "RADIOACTIVE", 0.45),
            "spinning": ("break3", "SPINNING", 0.8), "turbine": ("break3", "TURBINE", 0.92),
            "two": ("fix3", "TWO", 0.1), "loops": ("fix3", "LOOPS", 0.15), "sealed": ("fix3", "SEALED", 0.35),
            "heats": ("fix3", "HEATS", 0.55), "clean": ("fix3", "CLEAN", 0.62), "boils": ("fix3", "BOILS", 0.75),
            "spins": ("fix3", "SPINS", 0.85), "turbine2": ("fix3", "TURBINE", 0.95),
            "works": ("break4", "WORKS", 0.12), "quake": ("break4", "EARTHQUAKE", 0.35), "flood": ("break4", "FLOOD", 0.55),
            "plane": ("break4", "PLANE", 0.75), "hits": ("break4", "HITS", 0.85),
            "wrap": ("fix4", "WRAP", 0.12), "steel": ("fix4", "STEEL", 0.3), "concrete": ("fix4", "CONCRETE", 0.6),
            "dome": ("fix4", "DOME", 0.7), "meter": ("fix4", "METER", 0.9),
            "flip": ("cta", "FLIP", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "giant": ("reveal", "GIANT", 0.25), "towers": ("reveal", "TOWERS", 0.4), "puff": ("reveal", "PUFF", 0.6),
            "steam": ("reveal", "STEAM", 0.92),
            "s1": ("stat", "ONE", 0.04), "s2": ("stat", "TON", 0.45), "s3": ("stat", "ZERO", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "scary": ("tag", "SCARY", 0.15), "towers2": ("tag", "TOWERS", 0.25), "afraid": ("tag", "AFRAID", 0.5),
            "biggest": ("tag", "BIGGEST", 0.75), "kettles": ("tag", "KETTLES", 0.9)})
        T["bp"] = min(T["backup"], T["pumps"])                  # the two languages say these in either order
        T["cd"] = min(T["concrete"], T["dome"])
        T["tw"] = min(T["giant"], T["towers"])
        T["sc"] = min(T["scary"], T["towers2"])
        T["bonk"] = min(e("fix4") + 0.35, max(T["meter"] + 0.2, T["cd"] + 0.9))
        T["glass"] = T["kettles"] - 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "core", 1)
        self.cut(s("break2") - 0.12, "vessel", -1)
        self.cut(s("break3") - 0.12, "loops", 1)
        self.cut(s("break4") - 0.12, "site", -1)
        self.cut(s("fix4") - 0.12, "site", 1)                  # same set again: the threats start over
        self.cut(s("cta") + 0.05, "plant", -1)
        self.cut(s("tag") - 0.2, "kettle", 1)
        self.cams = {"pot": Camera(0, -215, 1.3), "core": Camera(0, -160, 0.92), "vessel": Camera(-40, -300, 0.92),
                     "loops": Camera(10, -290, 0.93), "site": Camera(0, -300, 0.92), "plant": Camera(330, -300, 0.95),
                     "kettle": Camera(60, -318, 0.85)}
        cm = self.cams
        cm["pot"].key(0.05, 0, -200, 1.38, 1.4).key(T["nuclear"] - 0.35, 40, -250, 1.12, 1.0)
        cm["core"].key(s("break1"), 0, -170, 0.98, 2.4).key(s("fix1") - 0.1, 0, -160, 0.92, 0.6)
        cm["vessel"].key(s("break2"), -40, -300, 0.95, 2.0).key(T["stops"] - 0.4, -80, -330, 1.0, 0.8)
        cm["vessel"].key(s("fix2") - 0.1, 40, -400, 0.72, 0.9).key(T["tank"] - 0.35, 60, -580, 0.6, 0.9)
        cm["loops"].key(s("break3"), 10, -290, 0.95, 2.0).key(s("fix3") - 0.1, 10, -295, 0.93, 0.8)
        cm["site"].key(s("break4"), 0, -300, 0.92, 1.5).key(T["plane"] - 0.3, 60, -330, 0.86, 0.8)
        cm["site"].key(s("fix4") - 0.12, 0, -330, 0.95, 0.0).key(T["cd"], 0, -360, 0.9, 1.0)
        cm["plant"].key(s("cta") + 0.05, 300, -290, 0.98, 1.4)
        cm["plant"].key(s("reveal") - 0.1, -90, -430, 0.62, 1.2).key(T["s1"] - 0.3, -70, -560, 0.5, 1.0)
        cm["plant"].key(s("closer") - 0.2, 40, -430, 0.64, 0.9)
        cm["kettle"].key(s("tag") - 0.2, 60, -318, 0.85, 0.0).key(T["biggest"] - 0.3, 100, -295, 0.92, 1.0)
        # ---- tracks
        self.boil = Track(0.0).to(T["boil"] - 0.1, 1.0, 0.6)
        self.heat = Track(0.3).to(T["faster"], 1.0, max(0.8, T["melt"] - T["faster"]))
        self.heat.to(T["soak"], 0.35, 0.9)
        self.ins = Track(0.0).to(T["control"] - 0.25, 0.75, 0.75, e_out)
        self.ins.to(T["slide"], 0.35, 0.45).to(T["slide"] + 0.55, 0.92, 0.45).to(T["slide"] + 1.1, 0.62, 0.5)
        self.level = Track(1.0).to(T["stops"] + 0.1, 0.22, max(0.8, T["melts"] - T["stops"] + 0.3))
        self.level.to(T["pours"], 1.0, 1.2)
        self.vheat = Track(0.35).to(T["stops"] + 0.2, 1.0, max(0.8, T["melts"] - T["stops"] + 0.2))
        self.vheat.to(T["pours"] + 0.2, 0.3, 1.2)
        self.vrods = Track(0.55).to(T["switched"] - 0.05, 1.0, 0.4, e_in)
        self.lever = Track(0.0).to(T["switched"] - 0.1, 1.0, 0.25, e_back)
        self.mainp = Track(1.0).to(T["stops"] - 0.1, 0.0, 0.6)
        self.backp = Track(0.0).to(T["bp"] + 0.35, 1.0, 0.6)
        self.rad = Track(0.0).to(T["touching"] - 0.1, 1.0, max(0.6, T["radio"] - T["touching"] + 0.3))
        self.two = Track(0.0).to(T["loops"] - 0.1, 1.0, 0.6, e_out)
        self.spin = Track(0.0).to(T["spinning"] - 0.2, 1.0, 0.5).to(s("fix3"), 0.0, 0.4).to(T["spins"] - 0.2, 1.0, 0.6)
        self.flood = Track(0.0).to(T["flood"] - 0.2, 1.0, 0.9, e_out)
        self.planeu = Track(0.0).to(T["plane"] - 0.35, 0.9, max(0.6, s("fix4") - T["plane"] + 0.25), e_io)
        self.steel = Track(0.0).to(T["steel"] - 0.25, 1.0, 0.7, e_out)
        self.conc = Track(0.0).to(T["cd"] - 0.25, 1.0, 0.8, e_out)
        self.towers = Track(0.0).to(T["tw"] - 0.15, 1.0, 0.9, e_out)
        self.kettle = Track(0.0).to(T["biggest"] - 0.2, 1.0, 0.7, e_back)
        self.pour = Track(0.0).to(T["glass"] + 0.3, 1.0, 1.2)
        t_end = self.tl.duration + 1
        self.p_main = Integral(lambda t: 720 * self.mainp.at(t), 0, t_end)
        self.p_back = Integral(lambda t: 720 * self.backp.at(t), 0, t_end)
        self.p_turb = Integral(lambda t: 1.6 * self.spin.at(t), 0, t_end)
        self.p_flow = Integral(lambda t: 0.45 * max(self.mainp.at(t), self.backp.at(t) * (t >= T["bp"])), 0, t_end)
        self.spans = [(T["melt"], T["power"] + 0.3), (T["melts"], T["own"] + 0.3), (T["turbine"], T["turbine2"] + 0.3),
                      (T["hits"], T["meter"] + 0.4)]
        self.shakes = [(T["boil"], 0.2, 4), (T["melt"], 0.5, 14), (T["control"] + 0.3, 0.25, 8), (T["switched"], 0.25, 8),
                       (T["melts"], 0.5, 14), (T["bp"] + 0.1, 0.25, 8), (T["pours"], 0.3, 8), (T["turbine"], 0.3, 10),
                       (T["quake"], 0.9, 22), (T["flood"] + 0.4, 0.3, 8), (T["steel"], 0.3, 10), (T["cd"] + 0.2, 0.35, 12),
                       (T["bonk"], 0.3, 10), (T["tw"] + 0.5, 0.4, 10), (s("closer") + 0.2, 0.35, 10), (T["kettles"], 0.3, 8)]
        # ---- the chain reaction: split times of every atom in the core (deterministic)
        self.atoms = [(-320 + 160 * i, -470 + 115 * k) for i in range(5) for k in range(6)]
        t0, t1 = s("break1") - 0.4, s("break2") + 0.2
        n = int((t1 - t0) * 60) + 1
        rates = [self.rate(t0 + j / 60) for j in range(n)]
        rng = random.Random(24)
        self.splits = []
        for _ in self.atoms:
            ph, jit, ev = rng.uniform(0, 1), rng.uniform(0.8, 1.25), []
            for j in range(n):
                ph += rates[j] * jit / 60
                if ph >= 1:
                    ph -= 1 + rng.uniform(-0.3, 0.3)
                    ev.append(t0 + j / 60)
            self.splits.append(ev)

    def rate(self, t):
        """Splits per second per atom in the core."""
        T, s = self.T, self.tl.s
        if t < s("fix1"):
            if t < T["splitting"] - 0.4:
                return 0.45
            return min(7.5, 0.45 * 2 ** ((t - T["splitting"] + 0.4) / 0.5))
        return 0.3 + 4.0 * (1 - self.ins.at(t)) ** 2

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ set: the pot (hook)
    def draw_pot(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["pot"].at(t)
        cx, cy, z = cam
        self.backdrop(c, t, cx, cy, (0 - cy) * z + H / 2)
        self.view(c, cam)
        v2.ground(c, cx - 760 / z, cx + 760 / z)
        glow = 0.6 + 0.25 * math.sin(t * 3.1) + 0.35 * prog(t, T["uranium"] - 0.3, T["uranium"] + 0.3)
        contact_shadow(c, 0, 0, 260)
        add_glow(c, 0, -90, 260, RADC, 0.22 * glow)
        add_glow(c, 0, -110, 200, "#FFB04A", 0.25 * glow)
        for i in range(4):
            fuel_rod(c, -45 + i * 30, -150, -24, 22, 0.32 + 0.12 * glow, t=t, seed=i)
        box(c, -100, -26, 200, 26, "#4B5568", r=6)
        trefoil(c, 0, -13, 10)
        for sd in (-1, 1):                                                         # the grate on its legs
            c.drawLine(sd * 132, 0, sd * 112, -168, P("#2B3040", 1, stroke=10))
        c.drawRRect(rr(-128, -176, 256, 12, 6), P("#2B3040"))
        b = self.boil.at(t)
        body = skia.Path()                                                          # the pot
        body.moveTo(-118, -322)
        body.lineTo(118, -322)
        body.lineTo(106, -186)
        body.quadTo(0, -172, -106, -186)
        body.close()
        cyl_path(c, body, -118, 118, "#9AA3B5")
        for sd in (-1, 1):
            c.drawLine(sd * 118, -300, sd * 150, -306, P("#5B6274", 1, stroke=12))
        c.drawRRect(rr(-128, -334, 256, 18, 9), P("#C7CEDB"))
        c.drawOval(R(-112, -334, 224, 22), P(mix(WATER, "#7DD3FC", 0.3 * b)))
        for i in range(12):                                                         # boiling bubbles on top
            u = (t * 2.4 + i * 0.37) % 1.0
            bx = -92 + (i * 53) % 184
            c.drawCircle(bx, -323 - u * 6, 4 + 7 * u, P("#E0F2FE", 0.85 * b * (1 - u), stroke=2.5))
        v2.smoke(c, 0, -342, t, T["boil"] - 0.1, None, rate=9, life=2.4, spread=(150, -50), rise=-110, size=(30, 120),
                 col=STEAMC, lit=None, lit_until=0.0, a=0.7 * b)
        pose = "look" if t < T["congrats"] else "cheer"
        self.crew(c, t, pose, xs=(-314, -268, -222), y=0, face=1, h=112)
        sparks_shower(c, 0, -330, t, T["congrats"], 0.7, n=14, speed=360, seed=4)
        c.restore()
        self.ui["cam"] = cam

    def ui_pot(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(48, -96)
        self.label(x0, y0, 840, y0, "uranium", T["uranium"] - 0.05, T["nuclear"] - 0.25, RADC)
        x1, y1 = self.at(70, -330)
        self.label(x1, y1, 820, 640, "water", T["water"] - 0.05, T["nuclear"] - 0.25, NEUT)
        self.chip(540, 470, "plant", T["nuclear"] - 0.1, s("break1") + 0.1, accent=HILITE, size=38)

    # ------------------------------------------------------------------ set: the core (break1, fix1)
    def rod_bottom(self, t):
        return lerp(-1250, 140, self.ins.at(t))

    def draw_core(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["core"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B132B", "#05081A"]))
        self.view(c, cam)
        heat = self.heat.at(t)
        melt = prog(t, T["melt"] - 0.35, T["melt"] + 0.5) * (1 - prog(t, s("fix1"), s("fix1") + 0.7))
        c.drawRRect(rr(-470, -580, 940, 820, 34), lin_paint(0, -580, 0, 240, [mix(WATER, "#7A2E12", heat * 0.6),
                                                                             mix(WATER_D, "#2A0E06", heat * 0.6)]))
        add_glow(c, 0, -170, 560, mix("#38BDF8", HOTC, heat), 0.22 + 0.25 * heat)
        rng = random.Random(3)
        for i in range(26):                                                         # rising bubbles, faster when hot
            u = (t * (0.25 + 0.9 * heat) + rng.uniform(0, 1)) % 1.0
            bx = rng.uniform(-440, 440)
            c.drawCircle(bx + math.sin(t * 3 + i) * 6, lerp(220, -560, u), 4 + 4 * heat, P("#E0F2FE", 0.35 + 0.3 * heat, stroke=2))
        for i in range(5):
            fuel_rod(c, -320 + 160 * i, -540, 190, 84, heat, melt, t, seed=i)
        rb = self.rod_bottom(t)
        hits = []
        for ai, (ax, ay) in enumerate(self.atoms):                                  # atoms and their neutrons
            ev = self.splits[ai]
            j = bisect.bisect_right(ev, t) - 1
            age = t - ev[j] if j >= 0 else 9.0
            if age < 0.4:
                u = age / 0.4
                rng = random.Random(ai * 977 + j)
                q = rng.uniform(0, math.pi)
                dx, dy = math.cos(q) * 30 * e_out(u), math.sin(q) * 30 * e_out(u)
                atom(c, ax + dx, ay + dy, 21, 1 - u)
                atom(c, ax - dx, ay - dy, 21, 1 - u)
                add_glow(c, ax, ay, 70, "#FFFFFF", 0.5 * (1 - u))
            else:
                atom(c, ax, ay, 30 * e_back(prog(age, 0.4, 0.65)) if age < 0.65 else 30)
            for jj in range(max(0, j - 6), j + 1):
                a2 = t - ev[jj]
                if not 0 <= a2 < 0.55:
                    continue
                rng = random.Random(ai * 131 + jj)
                for _ in range(2 + (jj % 2)):
                    q = rng.uniform(0, 2 * math.pi)
                    vx, vy = math.cos(q) * 540, math.sin(q) * 540
                    life = 0.55
                    for xr in XR:                                                   # a control rod in the way soaks it up
                        if t >= s("fix1") and vx != 0:
                            edge = xr - 17 * (1 if vx > 0 else -1)
                            ah = (edge - ax) / vx
                            if 0 < ah < life and ay + vy * ah < rb:
                                life = ah
                    if a2 < life:
                        nx, ny = ax + vx * a2, ay + vy * a2
                        if -470 < nx < 470 and -580 < ny < 240:
                            c.drawCircle(nx, ny, 6, P(NEUT, 0.95))
                            add_glow(c, nx, ny, 22, NEUT, 0.5)
                    elif a2 < life + 0.14:
                        hits.append((ax + vx * life, ay + vy * life, 1 - (a2 - life) / 0.14))
        if t >= s("fix1") - 0.2:                                                    # the control rods
            for xr in XR:
                c.drawRect(R(xr - 17, -2400, 34, rb + 2400), lin_paint(xr - 17, 0, xr + 17, 0, ["#1F2533", "#4B5568", "#1F2533"]))
                c.drawRRect(rr(xr - 17, rb - 30, 34, 30, 8), P("#FACC15"))
            for hx, hy, k in hits:
                add_glow(c, hx, hy, 40, "#FFFFFF", 0.7 * k)
            hk = prog(t, T["neutrons"] - 0.35, T["neutrons"] + 0.05)                # one hero neutron, caught by a rod
            if 0 < hk < 1:
                hx = lerp(-300, -97, hk)
                c.drawCircle(hx, -240, 11, P(NEUT))
                add_glow(c, hx, -240, 50, NEUT, 0.8)
            fl = 1 - prog(t, T["neutrons"] + 0.05, T["neutrons"] + 0.5)
            if 0 < fl < 1:
                add_glow(c, -97, -240, 120, "#FFFFFF", 0.8 * fl)
        c.restore()
        self.ui["cam"] = cam

    def ui_core(self, c, t, tw):
        T, s = self.T, self.tl.s
        p = self.span(s("break1") + 0.1, s("break2") - 0.15)
        if p > 0:
            k = clamp(math.log(self.rate(tw) / 0.2) / math.log(7.5 / 0.2))
            v2.gauge(c, 60, 300, [(self.L["power"], k, mix(GOOD, WARN, clamp((k - 0.45) * 2)))], p, w=330)
        if tw < s("fix1"):
            self.chip(540, 500, "split", T["splitting"] - 0.05, T["melt"] - 0.1, accent=NEUT, size=38)
            self.chip(540, 500, "melt", T["melt"] - 0.05, s("fix1") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["melt"], s("fix1") - 0.2, x=900, y=500)
            self.red(T["hot"], 2.4)
            return
        x0, y0 = self.at(240, -700)
        self.label(x0, y0, 800, 400, "rods", T["control"] + 0.2, T["slide"] + 0.7, HILITE)
        self.badge("check", T["power"] + 0.1, s("break2") - 0.15, x=900, y=500)

    # ------------------------------------------------------------------ set: the reactor vessel (break2, fix2)
    VX0, VY0, VW, VH = -140, -760, 280, 560
    LOOP = [(-140, -620), (-400, -620), (-400, -90), (-330, -90), (-274, -90), (0, -90), (0, -200)]

    def draw_vessel(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["vessel"].at(t)
        vh = self.vheat.at(t)
        hall(c, cam, tint=0.6 * vh * prog(t, T["stops"], T["melts"]))
        self.view(c, cam)
        floor(c, cam)
        fixed = t >= s("fix2")
        # backup pumps and the header pipe
        bk = prog(t, T["bp"] - 0.2, T["bp"] + 0.25) if fixed else 0.0
        if bk > 0:
            pipe(c, [(-660, -90), (-400, -90)], "#7C8499", 20, a=clamp(bk * 3))
            for i, px in enumerate((-500, -620)):
                k = e_back(clamp(bk * 1.3 - i * 0.3))
                if k > 0:
                    c.save()
                    c.translate(px, -50)
                    c.scale(k, k)
                    pump(c, 0, -40, 42, self.p_back.at(t) + i * 30, on=self.backp.at(t))
                    c.restore()
            if t >= T["bp"] + 0.35:
                flow(c, [(-660, -90), (-400, -90)], self.p_flow.at(t) * 2, 1.0, n=6, col=NEUT, r=6)
        # main loop
        pipe(c, self.LOOP[:7], "#7C8499", 26)
        on = self.mainp.at(t)
        ph = self.p_flow.at(t)
        flow(c, self.LOOP[:7], ph, 1.0 if (on > 0.05 or (fixed and t >= T["bp"] + 0.35)) else 0.0, n=14, col=NEUT, r=7)
        pump(c, -330, -90, 56, self.p_main.at(t), on=on)
        # the vessel, cut open
        x0, y0, w, h = self.VX0, self.VY0, self.VW, self.VH
        capsule(c, x0 - 16, y0 - 16, w + 32, h + 32, "#5B6478")
        c.save()
        c.clipRRect(rr(x0, y0, w, h, w / 2), skia.ClipOp.kIntersect, True)
        c.drawRect(R(x0, y0, w, h), P("#0E1424"))
        lev = self.level.at(t)
        wy = lerp(-210, -720, lev)
        c.drawRect(R(x0, wy, w, -200 - wy + 10), lin_paint(0, wy, 0, -200, ["#2B6CB0", "#0B2D5C"]))
        for i in range(5):
            fuel_rod(c, -80 + 40 * i, -560, -280, 26, vh, 0.6 * prog(t, T["melts"] - 0.3, T["melts"] + 0.5) * (not fixed), t, seed=i)
        rods_y = lerp(-1000, -330, self.vrods.at(t))
        for xr in (-60, -20, 20, 60):
            c.drawRect(R(xr - 6, -1200, 12, rods_y + 1200), P("#1F2533"))
        cool = clamp(lev * 1.4 - 0.4) * (1 - vh)
        add_glow(c, 0, -420, 220, "#38BDF8", 0.45 * cool)
        add_glow(c, 0, -420, 200, HOTC, 0.6 * clamp(vh - 0.35))
        if lev < 0.95:                                                             # steam above the falling water
            for i in range(8):
                u = (t * 0.8 + i * 0.13) % 1.0
                c.drawCircle(-100 + (i * 37) % 200, lerp(wy, -730, u), 10 + 18 * u, P(STEAMC, 0.25 * (1 - u) * (1 - lev)))
        c.restore()
        c.drawRRect(rr(x0, y0, w, h, w / 2), P("#CBD5E1", 0.5, stroke=4))
        # the switch panel (break2)
        pa = 1 - prog(t, s("fix2") - 0.1, s("fix2") + 0.2)
        if pa > 0:
            box(c, 300, -560, 150, 220, "#334155", r=14, a=pa)
            lv = self.lever.at(t)
            ang = lerp(-35, 35, lv)
            c.save()
            c.translate(375, -450)
            c.rotate(ang)
            c.drawRRect(rr(-8, -90, 16, 90, 8), P("#CBD5E1", pa))
            c.drawCircle(0, -94, 18, P(mix(GOOD, WARN, lv), pa))
            c.restore()
            c.drawRRect(rr(345, -462, 60, 24, 10), P("#0F172A", pa))
            word(c, "ON" if lv < 0.5 else "OFF", 375, -508 if lv < 0.5 else -366, 26, mix(GOOD, WARN, lv), pa)
        # diesel generators and their cable
        if fixed:
            gk = prog(t, T["diesel"] - 0.2, T["diesel"] + 0.2)
            if gk > 0:
                run = prog(t, T["diesel"] + 0.2, T["diesel"] + 0.5)
                for i, gx in enumerate((420, 580)):
                    k = e_back(clamp(gk * 1.3 - i * 0.3))
                    if k > 0:
                        c.save()
                        c.translate(gx + 75, 0)
                        c.scale(k, k)
                        generator(c, -75, 0, t + i * 0.3, run, w=150, h=116)
                        c.restore()
                if run > 0:
                    c.drawLine(420, -12, -620, -12, P("#111827", 1, stroke=10))
                    for i in range(10):
                        u = (t * 0.7 + i / 10) % 1.0
                        add_glow(c, lerp(420, -620, u), -12, 26, "#FDE047", 0.8 * run)
            tk = prog(t, T["tank"] - 0.25, T["tank"] + 0.35)                         # the tank up high
            if tk > 0:
                legs = 950 * e_out(tk)
                for lx in (240, 400):
                    c.drawRect(R(lx - 10, -legs, 20, legs), lin_paint(lx - 10, 0, lx + 10, 0, [STEEL, shade(STEEL, -0.4)]))
                c.drawLine(240, -legs * 0.5, 400, -legs * 0.25, P(STEEL, 1, stroke=6))
                c.drawLine(400, -legs * 0.5, 240, -legs * 0.25, P(STEEL, 1, stroke=6))
                cyl(c, 190, -legs - 230, 260, 240, "#94A3B8", r=30)
                fill = 1 - 0.55 * prog(t, T["pours"], T["pours"] + 1.4)
                c.drawRRect(rr(204, -legs - 214 + 210 * (1 - fill), 232, 210 * fill, 18), P("#2B6CB0", 0.8))
                pipe(c, [(320, -legs + 6), (320, -600), (140, -600)], "#7C8499", 18, a=clamp(tk * 2))
                pk = prog(t, T["pours"] - 0.1, T["pours"] + 0.3)
                if pk > 0:
                    flow(c, [(320, -legs + 6), (320, -600), (140, -600)], t * 0.7, pk, n=8, col=NEUT, r=6)
        c.restore()
        self.ui["cam"] = cam

    def ui_vessel(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2"):
            self.chip(540, 470, "steady", T["steady"] - 0.05, T["switched"] - 0.1, accent=GOOD, size=40)
            x0, y0 = self.at(375, -560)
            self.label(x0, y0, 790, 430, "off", T["switched"], T["heat"] - 0.1, WARN)
            x1, y1 = self.at(0, -420)
            self.label(x1, y1, 300, 430, "heat", T["heat"] - 0.05, T["stops"] - 0.1, HOTC, size=32)
            x2, y2 = self.at(-330, -150)
            self.label(x2, y2, 300, 430, "nowater", T["stops"], s("fix2") - 0.15, WARN)
            self.chip(760, 560, "melt", T["melts"] - 0.05, s("fix2") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["melts"], s("fix2") - 0.2, x=900, y=300)
            self.red(T["melts"], 2.0)
            return
        x0, y0 = self.at(-560, -130)
        self.label(x0, y0, 300, 420, "backup", T["bp"] + 0.15, T["tank"] - 0.2, NEUT)
        x1, y1 = self.at(495, -130)
        self.label(x1, y1, 780, 420, "diesel", T["diesel"] + 0.1, T["tank"] - 0.2, "#F59E0B", size=32)
        x2, y2 = self.at(200, -1060)
        self.label(x2, y2, 300, 420, "tank", T["tank"] + 0.25, s("break3") - 0.2, NEUT)
        self.chip(760, 520, "gravity", T["own"] - 0.1, s("break3") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["own"] + 0.2, s("break3") - 0.15, x=900, y=660)

    # ------------------------------------------------------------------ set: the loops (break3, fix3)
    ONE_OUT = [(-380, -700), (-380, -830), (170, -830), (170, -395)]
    ONE_BACK = [(330, -228), (330, -140), (-380, -140), (-380, -240)]
    PRIM = [(-290, -600), (-170, -600), (-60, -565), (-170, -530), (-60, -495), (-170, -460), (-60, -425), (-170, -390),
            (-60, -355), (-170, -320), (-170, -300), (-290, -300), (-380, -300), (-380, -600), (-290, -600)]
    SEC_OUT = [(-110, -760), (-110, -830), (170, -830), (170, -395)]
    SEC_BACK = [(330, -228), (330, -140), (-60, -140), (-60, -190)]

    def turbine(self, c, t, spin, rad=0.0):
        x0, x1 = 150, 380
        path = skia.Path()
        path.moveTo(x0, -392)
        path.lineTo(x1, -440)
        path.lineTo(x1, -220)
        path.lineTo(x0, -268)
        path.close()
        c.drawPath(path, lin_paint(0, -440, 0, -220, [shade(STEELC, 0.3), STEELC, shade(STEELC, -0.4)]))
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawRect(R(x0 + 16, -430, x1 - x0 - 32, 200), P("#0F172A", 0.75))
        ph = self.p_turb.at(t)
        for i in range(12):
            u = (i / 12 + ph) % 1.0
            xx = lerp(x0 + 20, x1 - 20, u)
            hh = lerp(56, 100, (xx - x0) / (x1 - x0))
            c.drawLine(xx, -330 - hh, xx + 10, -330 + hh, P(mix("#CBD5E1", RADC, rad), 0.9, stroke=7))
        c.restore()
        if rad > 0:
            add_glow(c, 265, -330, 240, RADC, 0.45 * rad)
        c.drawRect(R(x0 - 10, -336, x1 - x0 + 120, 12), P("#475569"))
        box(c, 392, -400, 110, 140, "#334155", r=12)
        bolt = skia.Path()
        for i, (bx, by) in enumerate(((452, -380), (430, -330), (450, -330), (436, -282), (474, -342), (454, -342), (468, -380))):
            (bolt.moveTo if i == 0 else bolt.lineTo)(bx, by)
        bolt.close()
        lit = spin * (1 - rad)
        c.drawPath(bolt, P(mix("#64748B", "#FDE047", lit)))
        if lit > 0.3:
            add_glow(c, 450, -330, 120, "#FDE047", 0.5 * lit)

    def draw_loops(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["loops"].at(t)
        rad = self.rad.at(t)
        two = self.two.at(t)
        hall(c, cam, rad=0.35 * rad * (1 - two))
        self.view(c, cam)
        floor(c, cam)
        one = 1 - two
        green = mix(NEUT, RADC, rad)
        pipe(c, self.ONE_OUT, "#7C8499", 24, a=one)
        pipe(c, self.ONE_BACK, "#7C8499", 24, a=one)
        flow(c, self.ONE_OUT, t * 0.5, one, n=10, col=green, r=7, glow=0.4 * rad)
        flow(c, self.ONE_BACK, t * 0.5, one, n=10, col=green, r=7, glow=0.4 * rad)
        if two > 0:                                                                # the steam generator and both loops
            pipe(c, self.SEC_OUT, "#7C8499", 24, a=two)
            pipe(c, self.SEC_BACK, "#7C8499", 24, a=two)
            k = e_back(clamp(two))
            c.save()
            c.translate(-110, -180)
            c.scale(k, k)
            c.translate(110, 180)
            capsule(c, -190, -760, 160, 580, "#64748B")
            c.drawRRect(rr(-178, -748, 136, 556, 68), P("#0E1424"))
            wl = -620
            c.drawRRect(rr(-178, wl, 136, -192 - wl, 60), lin_paint(0, wl, 0, -192, ["#3B82F6", "#1E3A8A"]))
            bo = prog(t, T["boils"] - 0.2, T["boils"] + 0.4)
            for i in range(14):
                u = (t * 1.3 + i * 0.29) % 1.0
                c.drawCircle(-165 + (i * 23) % 110, lerp(-210, wl, u), 4 + 4 * u, P("#E0F2FE", 0.7 * bo * (1 - u), stroke=2))
            for i in range(6):
                u = (t * 0.6 + i / 6) % 1.0
                c.drawCircle(-110 + math.sin(t * 2 + i) * 30, lerp(wl - 10, -740, u), 14 + 16 * u, P(STEAMC, 0.35 * bo * (1 - u)))
            pipe(c, self.PRIM[:12], PRIM, 12)
            c.restore()
            flow(c, self.PRIM, t * 0.35, two, n=22, col="#FDBA74", r=6, glow=0.2)
            sk = prog(t, T["boils"] - 0.1, T["boils"] + 0.3)
            for i in range(9):                                                       # steam to the turbine
                x, y = along(self.SEC_OUT, (t * 0.55 + i / 9) % 1.0)
                c.drawCircle(x, y, 12, P(STEAMC, 0.8 * sk))
            flow(c, self.SEC_BACK, t * 0.5, two, n=8, col=NEUT, r=7)
            se = prog(t, T["sealed"] - 0.1, T["sealed"] + 0.3)
            if se > 0:                                                               # the sealed line around the hot loop
                c.drawRRect(rr(-505, -790, 500, 640, 40), dash_paint(PRIM, se, w=5, t=t))
                c.drawRRect(rr(-268, -632, 44, 36, 8), P("#FACC15", se))
                c.drawArc(R(-262, -656, 32, 40), 180, 180, False, P("#FACC15", se, stroke=6))
        # the reactor vessel
        capsule(c, -470, -700, 180, 460, "#5B6478")
        c.drawRRect(rr(-458, -688, 156, 436, 78), lin_paint(0, -688, 0, -252, [mix("#2B6CB0", "#4D7C0F", rad), mix("#0B2D5C", "#1A2E05", rad)]))
        for i in range(4):
            fuel_rod(c, -425 + 30 * i, -560, -320, 18, 0.45, 0.0, t, seed=i)
        add_glow(c, -380, -450, 200, mix("#38BDF8", RADC, rad), 0.45)
        if rad > 0.05:                                                              # radiation signs drifting off the hot water
            for i in range(5):
                u = (t * 0.35 + i / 5) % 1.0
                x, y = along(self.ONE_OUT if i % 2 else self.ONE_BACK, u)
                trefoil(c, x + 30, y - 40, 20, a=rad * one * (1 - abs(u - 0.5) * 1.4))
        self.turbine(c, t, self.spin.at(t), rad * one)
        pose = "duck" if (t >= T["radio"] and t < s("fix3")) else ("cheer" if t >= T["spins"] else "stand")
        for i, (px, col) in enumerate(((210, SHIRTS[0]), (270, SHIRTS[1]))):
            engineer(c, px, 0, 112 + i * 8, col, t + i * 0.3, pose, face=-1)
        c.restore()
        self.ui["cam"] = cam

    def ui_loops(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3"):
            x0, y0 = self.at(-380, -780)
            self.label(x0, y0, 300, 420, "radio", T["radio"] - 0.1, s("fix3") - 0.15, RADC)
            x1, y1 = self.at(330, -440)
            self.label(x1, y1, 790, 420, "turbine", T["spinning"] - 0.1, s("fix3") - 0.15, WARN)
            self.badge("alert", T["turbine"], s("fix3") - 0.2, x=900, y=290)
            self.red(T["turbine"], 2.0)
            return
        x0, y0 = self.at(-480, -760)
        self.label(x0, y0, 280, 420, "loop1", T["sealed"] + 0.1, s("break4") - 0.2, PRIM)
        x1, y1 = self.at(-40, -300)
        self.label(x1, y1, 790, 420, "loop2", T["clean"] - 0.05, T["boils"] + 0.2, NEUT)
        x2, y2 = self.at(170, -700)
        self.label(x2, y2, 790, 420, "steam", T["boils"] + 0.25, s("break4") - 0.2, STEAMC)
        self.badge("check", T["turbine2"] + 0.25, s("break4") - 0.15, x=900, y=560)

    # ------------------------------------------------------------------ set: the site (break4, fix4)
    def draw_site(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["site"].at(t)
        cx, cy, z = cam
        self.backdrop(c, t, cx, cy, (0 - cy) * z + H / 2)
        self.view(c, cam)
        v2.ground(c, cx - 760 / z, cx + 760 / z)
        fixed = t >= s("fix4") - 0.12
        qk = bump(t, T["quake"] - 0.1, T["quake"] + 0.9) if not fixed else 0.0
        if not fixed:
            ck = prog(t, T["quake"], T["quake"] + 0.3)
            for sx_ in (-420, 380):                                                 # cracks in the ground
                path = skia.Path()
                path.moveTo(sx_, 0)
                for k in range(1, 6):
                    path.lineTo(sx_ + k * 22 * (1 if sx_ > 0 else -1) + (k % 2) * 14, k * 14)
                c.drawPath(path, P("#0B0E1A", ck, stroke=5))
        contact_shadow(c, 0, 0, 560)
        box(c, -280, -26, 560, 26, "#4B5568", r=6)
        # the reactor vessel inside
        capsule(c, -70, -330, 140, 300, "#64748B")
        add_glow(c, 0, -180, 160, "#38BDF8", 0.35)
        if not fixed:                                                               # the plain building, wobbling in the quake
            c.save()
            c.translate(0, 0)
            c.rotate(math.sin(t * 34) * 2.2 * qk)
            box(c, -230, -400, 460, 374, "#A7AEBD", r=6, a=0.92)
            c.drawRect(R(-110, -350, 220, 300), P("#0E1424", 0.85))
            capsule(c, -70, -330, 140, 300, "#64748B")
            add_glow(c, 0, -180, 140, "#38BDF8", 0.3)
            ck = prog(t, T["quake"] + 0.1, T["quake"] + 0.4)
            path = skia.Path()
            path.moveTo(150, -400)
            for k, (px, py) in enumerate(((132, -350), (160, -310), (138, -262), (168, -214))):
                path.lineTo(px, py)
            c.drawPath(path, P("#1F2937", ck, stroke=5))
            c.restore()
            fk = self.flood.at(t)                                                   # the flood rolls in from the left
            if fk > 0:
                front = lerp(-1300, 1200, fk)
                path = skia.Path()
                path.moveTo(-2000, 40)
                xx = -2000
                while xx < front:
                    path.lineTo(xx, -140 + math.sin(xx * 0.02 + t * 4) * 12)
                    xx += 30
                path.lineTo(front, 40)
                path.close()
                c.drawPath(path, P("#2563EB", 0.62))
                c.drawPath(path, P("#BFDBFE", 0.7, stroke=4))
            u = self.planeu.at(t)                                                   # the little plane, getting closer
            if u > 0:
                px, py = lerp(580, 300, u), lerp(-720, -400, u) - math.sin(u * math.pi) * 40
                plane(c, px, py, 0.9, -20, t)
                if u > 0.2:
                    dashed = skia.Path()
                    dashed.moveTo(px - 80, py + 30)
                    dashed.lineTo(200, -330)
                    c.drawPath(dashed, dash_paint(WARN, 0.8, w=4, t=t))
        else:
            sk = self.steel.at(t)                                                    # steel shell: a cut-open ring
            if sk > 0:
                c.save()
                c.clipRect(R(-500, -26 - 560 * sk, 1000, 560 * sk))
                c.drawPath(dome_path(150, 0, -26, -370), P(STEELC, 0.2))
                c.drawPath(dome_path(150, 0, -26, -370), P(STEELC, 1, stroke=18))
                c.drawPath(dome_path(150, 0, -26, -370), P("#E2E8F0", 0.5, stroke=4))
                c.restore()
            ck = self.conc.at(t)                                                     # concrete dome, more than a meter thick
            if ck > 0:
                c.save()
                c.clipRect(R(-500, -26 - 700 * ck, 1000, 700 * ck))
                c.drawPath(dome_path(222, 0, -26, -370), P("#000000", 0.35, stroke=72))
                cp = lin_paint(-260, 0, 260, 0, [shade(CONC, -0.3), shade(CONC, 0.22), CONC, shade(CONC, -0.35)], [0, 0.3, 0.6, 1])
                cp.setStyle(skia.Paint.kStroke_Style)
                cp.setStrokeWidth(64)
                c.drawPath(dome_path(222, 0, -26, -370), cp)
                c.drawPath(dome_path(222, 0, -26, -370), P("#FFFFFF", 0.18, stroke=8))
                c.restore()
                mk = prog(t, T["meter"] - 0.2, T["meter"] + 0.2)
                if mk > 0:
                    c.drawLine(190, -200, 254, -200, P(HILITE, mk, stroke=4))
                    for xx in (190, 254):
                        c.drawLine(xx, -214, xx, -186, P(HILITE, mk, stroke=4))
            person(c, 360, 0, 120, SHIRTS[1], t, "stand" if t < T["bonk"] else "point", face=-1, hat="hard", band=True)
            # the plane comes back and bounces off the dome
            hx, hy = 186, -560
            if T["bonk"] - 0.9 <= t < T["bonk"]:
                u = prog(t, T["bonk"] - 0.9, T["bonk"])
                plane(c, lerp(800, hx + 70, u), lerp(-760, hy - 10, u), 0.9, -15, t)
            elif t >= T["bonk"]:
                a_ = t - T["bonk"]
                plane(c, hx + 70 + a_ * 420, hy - 10 - a_ * 260 + 300 * a_ * a_, 0.9, -15 + a_ * 520, t,
                      a=1 - prog(a_, 1.0, 1.4))
                stars_ring(c, hx + 70 + a_ * 420, hy - 70 - a_ * 260 + 300 * a_ * a_, t, a=1 - prog(a_, 0.8, 1.2))
                v2.shock_ring(c, hx, hy, t, T["bonk"], 0.5, r1=160, col="#FFFFFF", width=10, squash=1.0)
        c.restore()
        self.ui["cam"] = cam

    def ui_site(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(250, 440, "quake", T["quake"] - 0.05, s("fix4") - 0.15, accent=WARN, size=34)
            self.chip(540, 440, "flood", T["flood"] - 0.05, s("fix4") - 0.15, accent=NEUT, size=34)
            self.chip(820, 440, "plane", T["plane"] - 0.05, s("fix4") - 0.15, accent=HILITE, size=34)
            self.badge("alert", T["hits"], s("fix4") - 0.2, x=900, y=300)
            self.red(T["hits"], 1.8)
            return
        x0, y0 = self.at(-150, -260)
        self.label(x0, y0, 280, 430, "steel", T["steel"] + 0.1, s("cta") - 0.1, STEELC)
        x1, y1 = self.at(-222, -470)
        self.label(x1, y1, 280, 540, "concrete", T["cd"] + 0.2, s("cta") - 0.1, "#E5E7EB")
        x2, y2 = self.at(254, -200)
        self.label(x2, y2, 800, 470, "thick", T["meter"], s("cta") - 0.1, HILITE)
        self.badge("check", T["bonk"] + 0.15, s("cta") - 0.05, x=880, y=640)

    # ------------------------------------------------------------------ set: the plant (cta, reveal, stat, closer)
    def draw_plant(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["plant"].at(t)
        cx, cy, z = cam
        self.backdrop(c, t, cx, cy, (0 - cy) * z + H / 2)
        self.view(c, cam)
        v2.ground(c, cx - 760 / z, cx + 760 / z)
        on = prog(t, T["cong2"], T["cong2"] + 0.3)
        tk = self.towers.at(t)
        for i, tx in enumerate((-560, -190)):                                       # the cooling towers
            k = clamp(tk * 1.25 - i * 0.25)
            tower(c, tx, 380, 620, k, lit=on)
            if k > 0 and k < 1:
                v2.smoke(c, tx, 0, t, T["tw"] - 0.1, T["tw"] + 0.9, rate=16, life=1.2, spread=(260, -40), rise=-30,
                         size=(30, 90), col="#6B7280", lit=None, lit_until=0.0, seed=10 + i, a=0.6)
            if k >= 1:
                v2.smoke(c, tx, -630, t, T["puff"] - 0.3 + i * 0.2, None, rate=5, life=4.0, spread=(110, -40), rise=-60,
                         size=(70, 230), col="#FFFFFF", lit=None, lit_until=0.0, seed=20 + i, a=0.95)
                add_glow(c, tx, -760, 260, "#FFFFFF", 0.10 * prog(t, T["puff"] - 0.3, T["puff"] + 0.8))
        # the dome
        contact_shadow(c, 150, 0, 340)
        cyl(c, 10, -250, 280, 250, CONC)
        dome = skia.Path()
        dome.addCircle(150, -250, 140)
        c.save()
        c.clipRect(R(0, -400, 300, 150))
        cyl_path(c, dome, 10, 290, CONC)
        c.restore()
        c.drawRect(R(10, -256, 280, 8), P("#000000", 0.12))
        # turbine hall and the power lines
        box(c, 320, -210, 340, 210, "#7C8499", r=6)
        c.drawRect(R(310, -226, 360, 18), P("#5B6274"))
        for i in range(6):
            c.drawRect(R(340 + i * 54, -170, 34, 40), P(mix("#2E3858", "#FFE3A3", 0.35 + 0.65 * on)))
        for lx in (760, 1000):
            lattice(c, lx, 0, -380, w=44, col=STEEL)
        for k in range(3):
            path = skia.Path()
            path.moveTo(660, -190 + k * 14)
            path.quadTo(710, -330 + k * 16, 760, -360 + k * 16)
            path.quadTo(880, -300 + k * 16, 1000, -360 + k * 16)
            path.quadTo(1200, -290 + k * 16, 1400, -360 + k * 16)
            c.drawPath(path, P(mix("#94A3B8", "#FDE047", on), 0.8, stroke=3))
        if on > 0:
            for i in range(6):
                u = (t * 0.6 + i / 6) % 1.0
                add_glow(c, lerp(660, 1400, u), -330 + math.sin(u * 9) * 20, 30, "#FDE047", 0.6 * on)
        # the big switch and the crew
        sw = 1 - prog(t, s("reveal") - 0.1, s("reveal") + 0.3)
        if sw > 0 or t >= s("closer") - 0.2:
            a_ = max(sw, prog(t, s("closer") - 0.2, s("closer")))
            c.drawRect(R(512, -150, 16, 150), P("#475569", a_))
            box(c, 485, -240, 70, 96, "#334155", r=10, a=a_)
            ang = -30 + 60 * prog(t, T["cong2"] - 0.1, T["cong2"] + 0.15)
            c.save()
            c.translate(520, -192)
            c.rotate(ang)
            c.drawRRect(rr(-6, -66, 12, 66, 6), P("#CBD5E1", a_))
            c.drawCircle(0, -70, 15, P(WARN, a_))
            c.restore()
        pose = "point" if t < s("reveal") else ("cheer" if t >= T["cong2"] else "look")
        self.crew(c, t, pose, xs=(590, 636, 682), y=0, face=-1, h=112)
        if t >= T["cong2"]:
            hats_in_the_air(c, (590, 636, 682), -90, t, T["cong2"] + 0.1)
        c.restore()
        self.ui["cam"] = cam

    def ui_plant(self, c, t, tw):
        T, s = self.T, self.tl.s
        if s("reveal") - 0.1 <= tw < T["s1"] - 0.3:
            x0, y0 = self.at(-190, -420)
            self.label(x0, y0, 780, 450, "towers", T["tw"] + 0.5, T["s1"] - 0.35, "#E5E7EB")
            self.chip(540, 600, "steam2", T["steam"] - 0.05, T["s1"] - 0.35, accent=NEUT, size=38)

    # ------------------------------------------------------------------ set: the kettle (tag)
    def draw_kettle(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["kettle"].at(t)
        cx, cy, z = cam
        self.backdrop(c, t, cx, cy, (0 - cy) * z + H / 2)
        self.view(c, cam)
        v2.ground(c, cx - 760 / z, cx + 760 / z)
        k = self.kettle.at(t)
        h = 640
        if k > 0:                                                                   # handle and spout grow out of the tower
            hk = clamp(k)
            c.drawArc(R(-270 + 60 * (1 - hk), -560, 280, 400), 90, 180, False, P("#475569", 1, stroke=44 * hk))
            c.drawArc(R(-270 + 60 * (1 - hk), -560, 280, 400), 90, 180, False, P("#94A3B8", 1, stroke=16 * hk))
        tower(c, 0, 420, h, 1.0, lit=0.4)
        if k > 0:
            hk = clamp(k)
            tipx, tipy = lerp(170, 430, hk), lerp(-300, -470, hk)
            sp = skia.Path()
            sp.moveTo(140, -250)
            sp.quadTo(250, -260, tipx - 4, tipy - 26)
            sp.lineTo(tipx + 26, tipy + 8)
            sp.quadTo(290, -110, 150, -90)
            sp.close()
            cyl_path(c, sp, 150, tipx + 22, CONC)
            c.drawRRect(rr(-50, -h - 34 - 40 * hk, 100, 30 + 40 * hk, 14), P("#5B6274"))   # lid knob
            c.drawCircle(0, -h - 40 - 40 * hk, 22 * hk, P("#94A3B8"))
            wk = prog(t, T["kettles"] - 0.15, T["kettles"] + 0.1)
            if wk > 0:                                                              # the whistle: a jet of steam
                v2.smoke(c, tipx + 20, tipy - 6, t, T["kettles"] - 0.15, None, rate=24, life=0.9, spread=(60, -260),
                         rise=-60, size=(14, 70), col=STEAMC, lit=None, lit_until=0.0, seed=33, a=0.9)
            if self.rtl:                                                            # Egypt: it pours a glass of tea
                gk = prog(t, T["glass"] - 0.1, T["glass"] + 0.2)
                if gk > 0:
                    box(c, 400, -26, 150, 26, "#6B4F3A", r=6, a=gk)
                    pk = self.pour.at(t)
                    if 0 < pk < 0.98:
                        st = skia.Path()
                        st.moveTo(tipx + 18, tipy + 2)
                        st.quadTo(tipx + 60, tipy + 60, 475, -110)
                        c.drawPath(st, P(TEA, 0.9 * gk, stroke=9))
                    tea_glass(c, 475, -26, pk, a=gk)
        v2.smoke(c, 0, -h - 10, t, s("tag") - 3.0, None, rate=4, life=4.0, spread=(100, -40), rise=-50, size=(70, 220),
                 col="#FFFFFF", lit=None, lit_until=0.0, seed=40, a=0.9 * (1 - 0.6 * clamp(k)))
        scared = T["sc"] - 0.1 <= t < T["kettles"]
        person(c, 300 if not self.rtl else 330, 0, 126, SHIRTS[2], t, "duck" if scared else "cheer", face=-1,
               skin=SKINS[1])
        c.restore()
        self.ui["cam"] = cam

    def ui_kettle(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 470, "scary", T["sc"] - 0.05, T["biggest"] - 0.1, accent=WARN, size=44)
        x0, y0 = self.at(300, -380)
        self.label(x0, y0, 540, 470, "kettle", T["kettles"] - 0.05, self.duration, HILITE)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.hum(1.6, 90.0), -14), (T["uranium"], sfx.charge_up(0.6), -12),
              (T["boil"], sfx.sizzle(1.6, 61), -12), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 62), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 63), -4)]
        pops = sorted(tt for evs in self.splits for tt in evs if s("break1") <= tt < T["melt"])
        last = -1.0
        for tt in pops:                                                              # one pop per audible split, thinned out
            if tt - last >= 0.07:
                ev.append((tt, sfx.pop(int(tt * 100) % 50), -16))
                last = tt
        ev += [(T["hot"], sfx.riser(1.0, 64), -10), (T["melt"], sfx.alarm(3, 820.0), -10), (T["melt"], rumble(1.4, 65), -6)]
        ev += [(T["control"] - 0.25, sfx.thunk(66), -4), (T["control"] - 0.1, sfx.clank(500.0, 0.4, 67), -8),
               (T["soak"], sfx.click(68), -8), (T["neutrons"] + 0.05, sfx.snap(69), -8),
               (T["slide"], sfx.whirr(1.4, 120.0, 220.0, 70), -12), (T["power"] + 0.1, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 71), -4), (T["switched"] - 0.1, sfx.clank(700.0, 0.3, 72), -4),
               (T["switched"], sfx.power_down(0.8, 73), -8), (T["heat"], sfx.hum(1.4, 70.0), -12),
               (T["stops"] - 0.1, sfx.power_down(1.0, 74), -6), (T["melts"], sfx.alarm(3, 820.0), -10)]
        ev += [(T["bp"], sfx.thud(0.4, 75), -5), (T["bp"] + 0.35, sfx.whirr(1.4, 160.0, 260.0, 76), -12),
               (T["diesel"] + 0.2, engine_snd(1.8), -7), (T["tank"], sfx.thud(0.5, 77), -4),
               (T["pours"], water_snd(1.6), -6), (T["own"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 78), -4), (T["touching"], geiger_snd(1.6), -8),
               (T["spinning"], sfx.whirr(1.2, 140.0, 240.0, 79), -12), (T["turbine"], sfx.alarm(3, 820.0), -11)]
        ev += [(T["loops"] - 0.1, sfx.pop(80), -6), (T["sealed"], sfx.lock_click(81), -5), (T["boils"], sfx.sizzle(1.2, 82), -10),
               (T["spins"], sfx.whirr(1.6, 160.0, 300.0, 83), -10), (T["turbine2"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 84), -4), (T["quake"], rumble(1.2, 85), -4),
               (T["flood"] - 0.1, water_snd(1.2, 86), -6), (T["plane"] - 0.3, prop_snd(1.6), -8), (T["hits"], sfx.alarm(3, 820.0), -11)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 87), -6), (T["steel"] - 0.1, sfx.clank(420.0, 0.5, 88), -5),
               (T["cd"] - 0.1, sfx.thud(0.5, 89), -3), (T["meter"], sfx.ding(), -8), (T["bonk"] - 0.8, prop_snd(0.9, 90), -10),
               (T["bonk"], sfx.thunk(91), -3), (T["bonk"] + 0.02, boing_snd(), -8), (T["bonk"] + 0.3, sfx.chime(), -7)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 94), -7)]
        ev += [(T["tw"] - 0.1, rumble(1.2, 95), -6), (T["puff"] - 0.2, sfx.hiss(1.0, 96), -10)]
        ev += [(T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3), (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"] - 0.05, sfx.clank(900.0, 0.2, 100), -8), (T["cong2"], sfx.pop(101), -2),
               (T["cong2"], sfx.sparkle(1.0, 14, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 103), -6), (T["sc"], sfx.womp(), -8), (T["biggest"] - 0.15, sfx.pop(104), -6),
               (T["kettles"] - 0.15, whistle_snd(1.8), -9)]
        if self.rtl:
            ev += [(T["glass"] + 0.3, water_snd(1.2, 105), -10)]
        return ev


NAME = "nuclear"
EPISODE = Nuclear
