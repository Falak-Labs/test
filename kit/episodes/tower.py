"""Episode 26 - The world's tallest tower.  v2 look: the desert at dusk and at night, six sets with whip cuts.

Sets: desert (side view: floors stack up into the sky; the skinny tower sinks into the sand; later it wobbles like a
pencil on its tip; after the fixes the finished tower: an elevator light rides to the top, the spire rises through the
roof, the lights come on, the stat cards and the cheer), ground (cutaway under the tower: piles drilled fifty meters
down, the ground grips their sides and holds it up), plan (from above: three wings grow around the core and brace each
other, like a tripod), sky (the top half in the wind: whirlpools peel off and make it sway; it steps in twenty-seven times
in a spiral and the whirlpools fall apart), pump (the tower under construction: in the hot sun the concrete hardens
halfway up the pipe; at night, ice into the mixer, and the concrete climbs a record six hundred meters), lobby (the tag:
the elevator is out of order and the doorman points at the stairs).
Side views: the ground is y = 0, up is negative.  The plan: the tower's centre is (0, 0).
"""
from v2_base import *  # noqa: F401,F403

TIERS, BODY_H, SPIRE_H = 27, 1100.0, 380.0
HW0, HWC = 150.0, 56.0                       # half width at the base: with the wings / the skinny core alone
GLS, GLS_D = "#A9C1DC", "#5E7896"
CONC = "#B9BEC7"
SKINS_L = ("#E8B48A", "#C68B5E", "#F1C9A5", "#8D5A3B")
DUNES = (("#7A4A34", "#B8743F"), ("#4A2E22", "#6E4229"))
SANDG = ("#9C6B3E", "#7A5232", "#4E3420", "#24170D")
DAY = {"top": "#C2602E", "upper": "#E08A45", "mid": "#F1AE5E", "low": "#F7CB7E", "horizon": "#FFE3A6",
       "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def prof(j):
    return lerp(1.0, 0.24, clamp(j / (TIERS - 1)) ** 1.1)


def tier_hw(i, wing=1.0, step=1.0):
    """Left and right half widths of tier i (0 = bottom).  step 0: a straight box; 1: setbacks on alternate sides."""
    sl = HW0 * prof(i - (i % 2))
    sr = HW0 * prof(max(0, i - 1 + (i % 2)))
    k = step(i) if callable(step) else step
    left, right = lerp(HW0, sl, k), lerp(HW0, sr, k)
    return lerp(HWC, left, wing), lerp(HWC, right, wing)


def tower(c, t, wing=1.0, step=1.0, built=1.0, spire=0.0, lights=0.0, rot=0.0, a=1.0, seed=3):
    """The tower from the side, base centre at (0, 0).  rot in degrees about the base."""
    if a <= 0:
        return
    th = BODY_H / TIERS
    n = TIERS * built
    c.save()
    if rot:
        c.rotate(rot)
    if spire > 0 and built >= 1:
        sh = SPIRE_H * spire
        top = -BODY_H
        path = skia.Path()
        path.moveTo(-15, top + 6)
        path.lineTo(-3, top - sh)
        path.lineTo(3, top - sh)
        path.lineTo(15, top + 6)
        path.close()
        c.drawPath(path, lin_paint(-15, 0, 15, 0, ["#F1F5F9", "#CBD5E1", "#64748B"], a=a))
        for k in range(1, int(sh / 64) + 1):
            yy = top - k * 64
            ww = lerp(15, 3, k * 64 / SPIRE_H)
            c.drawLine(-ww, yy, ww, yy, P("#475569", 0.7 * a, stroke=2))
        if lights > 0:
            beacon(c, 0, top - sh - 4, t, r=6)
    for i in range(TIERS):
        p = clamp(n - i)
        if p <= 0:
            break
        y1 = -i * th
        y0 = y1 - th * p
        left, right = tier_hw(i, wing, step)
        c.drawRect(R(-left, y0, left + right, y1 - y0 + 0.8),
                   lin_paint(-left, 0, right, 0, [shade(GLS, 0.32), GLS, shade(GLS, -0.18), GLS_D], [0, 0.35, 0.62, 1], a=a))
        c.drawRect(R(-left * 0.2, y0, left * 0.2 + 5, y1 - y0 + 0.8), P("#FFFFFF", 0.13 * a))
        for f in (1, 2):
            yy = y1 - th * f / 3
            if yy > y0:
                c.drawLine(-left, yy, right, yy, P("#22314A", 0.28 * a, stroke=1.5))
        if p >= 1:
            c.drawLine(-left, y0, right, y0, P("#F8FAFC", 0.6 * a, stroke=2.5))
        if lights > 0:
            rng = random.Random(seed * 97 + i)
            for f in range(3):
                yy = y1 - th * (f + 0.5) / 3
                for xx in range(int(-left) + 6, int(right) - 8, 13):
                    if rng.random() < 0.55:
                        c.drawRect(R(xx, yy - 3, 8, 6), P("#FFE2A8", lights * a * rng.uniform(0.45, 1.0)))
    if lights > 0:
        for k in range(5):
            add_glow(c, 0, -BODY_H * (0.1 + 0.2 * k), 260 - 30 * k, "#FFD27A", 0.18 * lights * a)
    c.restore()


def crane(c, x, y, t, a=1.0):
    """A yellow tower crane standing on (x, y)."""
    c.save()
    c.translate(x, y)
    lattice(c, 0, 0, -190, w=22, col="#F59E0B")
    c.drawRect(R(-120, -204, 330, 12), P("#F59E0B", a))
    for xx in range(-110, 200, 22):
        c.drawLine(xx, -204, xx + 11, -192, P("#B45309", a, stroke=2))
    box(c, -132, -214, 40, 34, "#475569", r=4, a=a)
    c.drawRRect(rr(-14, -236, 30, 32, 5), P("#FDE68A", a))
    hx = 160 + math.sin(t * 0.8) * 14
    c.drawLine(hx, -192, hx, -110, P("#1F2937", a, stroke=2))
    c.drawRect(R(hx - 8, -110, 16, 10), P("#EF4444", a))
    beacon(c, 0, -240, t, r=4)
    c.restore()


def mixer(c, x, t, spin=1.0, a=1.0):
    """A concrete mixer truck facing right, wheels on y = 0, centred on x."""
    c.save()
    c.translate(x, 0)
    contact_shadow(c, 0, 0, 320)
    box(c, -160, -54, 320, 26, "#374151", r=6, a=a)
    box(c, 92, -130, 78, 80, "#DC2626", r=12, a=a)
    c.drawRRect(rr(120, -120, 40, 30, 6), P("#BFE6FF", 0.9 * a))
    c.save()
    c.translate(-30, -108)
    c.rotate(-10)
    oval = skia.Path()
    oval.addOval(R(-122, -52, 244, 104))
    c.drawPath(oval, lin_paint(0, -52, 0, 52, ["#F8FAFC", "#CBD5E1", "#64748B"], a=a))
    c.save()
    c.clipPath(oval, skia.ClipOp.kIntersect, True)
    for k in range(6):
        xx = (k * 52 + t * 110 * spin) % 312 - 156
        c.drawLine(xx, -56, xx - 30, 56, P("#EF4444", 0.85 * a, stroke=12))
    c.restore()
    c.drawPath(oval, P("#334155", 0.6 * a, stroke=3))
    c.restore()
    c.drawRect(R(-178, -150, 34, 40), P("#475569", a))
    for wx in (-110, -50, 120):
        c.drawCircle(wx, -16, 20, P("#111827", a))
        c.drawCircle(wx, -16, 8, P("#9CA3AF", a))
    c.restore()


def ice(c, x, y, s, rot, a=1.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.drawRRect(rr(-s / 2, -s / 2, s, s, s * 0.22), P("#E0F2FE", 0.92 * a))
    c.drawRRect(rr(-s / 2, -s / 2, s, s, s * 0.22), P("#7DD3FC", a, stroke=3))
    c.drawRRect(rr(-s * 0.3, -s * 0.32, s * 0.28, s * 0.16, 3), P("#FFFFFF", 0.9 * a))
    c.restore()


def pencil(c, x, y, L, rot, a=1.0):
    """A pencil balanced on its tip at (x, y) (screen), rot in degrees."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    tip = skia.Path()
    tip.moveTo(0, 0)
    tip.lineTo(-16, -44)
    tip.lineTo(16, -44)
    tip.close()
    c.drawPath(tip, P("#F5D0A9", a))
    c.drawPath(skia.Path().moveTo(0, 0).lineTo(-6, -16).lineTo(6, -16).close(), P("#1F2937", a))
    c.drawRect(R(-16, -44 - L, 32, L), lin_paint(-16, 0, 16, 0, ["#FDE047", "#FACC15", "#CA8A04"], a=a))
    c.drawRect(R(-16, -58 - L, 32, 14), P("#94A3B8", a))
    c.drawRRect(rr(-16, -84 - L, 32, 28, 8), P("#F472B6", a))
    c.restore()


def tripod(c, x, y, s=1.0, k=1.0, a=1.0):
    """A camera on a tripod, feet on y, centred on x."""
    if a <= 0 or k <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s * e_back(k), s * e_back(k))
    hub = (0, -150)
    for fx_ in (-70, 0, 70):
        c.drawLine(hub[0], hub[1], fx_, 0 if fx_ else -18, P("#E5E7EB", a, stroke=8))
    c.drawRRect(rr(-46, -206, 92, 56, 10), P("#334155", a))
    c.drawCircle(0, -178, 18, P("#0EA5E9", a))
    c.drawCircle(0, -178, 8, P("#E0F2FE", a))
    c.restore()


def vortex(c, x, y, r, rot, cw, a):
    if a <= 0 or r <= 1:
        return
    path = skia.Path()
    for k in range(34):
        u = k / 33
        ang = rot + u * 2.3 * math.pi * cw
        rad = r * (0.15 + 0.85 * u)
        px, py = x + math.cos(ang) * rad, y + math.sin(ang) * rad * 0.8
        (path.moveTo if k == 0 else path.lineTo)(px, py)
    c.drawPath(path, P("#E0F2FE", a, stroke=max(3.0, r * 0.09)))


def hexagon(r, rot=30.0):
    path = skia.Path()
    for k in range(6):
        q = math.radians(rot + k * 60)
        (path.moveTo if k == 0 else path.lineTo)(math.cos(q) * r, math.sin(q) * r)
    path.close()
    return path


def arrow_up(c, x, y, s, col, a):
    if a <= 0:
        return
    path = skia.Path()
    path.moveTo(x - s, y + s * 0.6)
    path.lineTo(x, y - s * 0.6)
    path.lineTo(x + s, y + s * 0.6)
    c.drawPath(path, P(col, a, stroke=s * 0.45))


def big_arrow(c, x, y0, y1, w, col, a):
    """A fat arrow from y0 to y1 (pointing towards y1)."""
    if a <= 0:
        return
    d = 1 if y1 > y0 else -1
    head = 1.1 * w
    path = skia.Path()
    path.moveTo(x - w / 2, y0)
    path.lineTo(x + w / 2, y0)
    path.lineTo(x + w / 2, y1 - d * head)
    path.lineTo(x + w, y1 - d * head)
    path.lineTo(x, y1)
    path.lineTo(x - w, y1 - d * head)
    path.lineTo(x - w / 2, y1 - d * head)
    path.close()
    c.drawPath(path, P(col, a))


# ---------------------------------------------------------------------------------------------- sounds
def wind_snd(d=3.0, seed=70):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 200, 1400) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.9 * tt))
    return sfx._norm(x * sfx._ar(n, 0.4, 0.8), 0.6)


def drill_snd(d=0.6, seed=71):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sign(np.sin(2 * np.pi * 95 * tt)) * 0.4 + sfx._bp(sfx._rng(seed).standard_normal(n), 600, 3000) * 0.6
    return sfx._norm(sfx._lp(x, 2600) * sfx._ar(n, 0.02, 0.15), 0.55)


def clink_snd(seed=72):
    return sfx._norm(sfx.bell(2600.0 + seed * 37 % 500, 0.25, 0.8), 0.5)


# ====================================================================================== the episode
class Tower(EpisodeV2):
    BUILD_NO = 26
    FIRST_SET = "desert"
    CLEAR = "#070B1F"
    TITLE = {"en": "TALLEST TOWER", "ar_sa": "أطول برج"}
    EMPH = {"en": ["CONGRATS", "STACK", "HUNDRED", "SIXTY", "FLOORS", "DESERT", "TALLEST", "TOWER", "SAND", "SOFT", "ROCK",
                   "HEAVY", "SINK", "DRILL", "NINETY-TWO", "PILES", "FIFTY", "DEEP", "GRIPPING", "HOLDS", "SKINNY",
                   "WOBBLE", "PENCIL", "TIP", "THREE", "WINGS", "CORE", "BRACING", "TRIPOD", "HIGH", "WIND", "WHIRLPOOLS",
                   "SWAY", "STEPS", "TWENTY-SEVEN", "SPIRAL", "GRIP", "HEAT", "CONCRETE", "HARDENS", "NIGHT", "ICE",
                   "RECORD", "SIX", "FOLLOW", "SPIRE", "ROOF", "LIGHTS", "EIGHT", "TWENTY-EIGHT", "SIXTY-THREE",
                   "FIFTY-SEVEN", "ELEVATORS", "YOURSELF", "ELEVATOR", "BREAKS", "TWO", "STAIRS"],
            "ar_sa": ["مبروك", "رصيت", "وستين", "الصحرا", "أطول", "برج", "رمل", "طري", "بالتقل", "هيغرز", "فتحفر", "وتسعين",
                      "عمود", "خمسين", "تمسك", "وتشيله", "رفيع", "هيتهز", "قلم", "سنه", "تلات", "جناحات", "قلب", "ساند",
                      "حامل", "الهوا", "دوامات", "تهزه", "فيدخل", "سبعة", "الحلزونة", "يمسكوش", "الحر", "الخرسانة",
                      "بتشد", "بالليل", "بتلج", "ستمية", "قياسي", "تابعني", "سارية", "ميتين", "السطح", "النور", "تمنمية",
                      "تلاتة", "أسانسير", "بإيدك", "والبواب", "عطلان", "ألفين", "سلمة"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "STACK"): "رصيت", ("hook", "SIXTY"): "وستين", ("hook", "DESERT"): "الصحرا", ("hook", "CONGRATS"): "مبروك",
        ("hook", "TALLEST"): "أطول",
        ("break1", "GROUND"): "الأرض", ("break1", "SAND"): "رمل", ("break1", "SOFT"): "طري", ("break1", "HEAVY"): "بالتقل",
        ("break1", "SINK"): "هيغرز",
        ("fix1", "DRILL"): "فتحفر", ("fix1", "PILES"): "عمود", ("fix1", "FIFTY"): "خمسين", ("fix1", "GRIPPING"): "تمسك",
        ("fix1", "HOLDS"): "وتشيله",
        ("break2", "STANDS"): "واقف", ("break2", "SKINNY"): "رفيع", ("break2", "WOBBLE"): "هيتهز", ("break2", "PENCIL"): "قلم",
        ("break2", "TIP"): "سنه",
        ("fix2", "THREE"): "تلات", ("fix2", "WINGS"): "جناحات", ("fix2", "CORE"): "قلب", ("fix2", "BRACING"): "ساند",
        ("fix2", "TRIPOD"): "حامل",
        ("break3", "HIGH"): "فوق", ("break3", "WIND"): "الهوا", ("break3", "WHIRLPOOLS"): "دوامات", ("break3", "SWAY"): "تهزه",
        ("fix3", "STEPS"): "فيدخل", ("fix3", "TWENTY"): "سبعة", ("fix3", "CLIMBS"): "طالع", ("fix3", "SPIRAL"): "الحلزونة",
        ("fix3", "GRIP"): "يمسكوش",
        ("break4", "SHAPE"): "الشكل", ("break4", "HEAT"): "الحر", ("break4", "CONCRETE"): "الخرسانة",
        ("break4", "HARDENS"): "بتشد", ("break4", "TOP"): "فوق",
        ("fix4", "NIGHT"): "بالليل", ("fix4", "ICE"): "بتلج", ("fix4", "PUMP"): "وتضخها", ("fix4", "RECORD"): "قياسي",
        ("fix4", "SIX"): "ستمية", ("fix4", "UP"): "لفوق",
        ("cta", "RIDE"): "تطلع", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PUSH"): "زق", ("reveal", "SPIRE"): "سارية", ("reveal", "ROOF"): "السطح", ("reveal", "LIGHTS"): "النور",
        ("stat", "EIGHT"): "تمنمية", ("stat", "SIXTY"): "تلاتة", ("stat", "FIFTY"): "سبعة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "DAY"): "والبواب", ("tag", "ELEVATOR"): "الأسانسير", ("tag", "BREAKS"): "عطلان", ("tag", "TWO"): "ألفين",
        ("tag", "STAIRS"): "سلمة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a tunnel boring machine"),
                   "stat": [("828", "METERS"), ("163", "FLOORS"), ("57", "ELEVATORS")],
                   "L": {"floors": "FLOORS", "tallest": "THE WORLD'S TALLEST TOWER", "sand": "SAND", "rock": "SOFT ROCK",
                         "heavy": "TOO HEAVY", "piles": "PILES", "deep": "50 M DEEP", "grip": "THE GROUND GRIPS THEM",
                         "holds": "IT HOLDS", "skinny": "TOO SKINNY", "pencil": "A PENCIL ON ITS TIP", "wings": "3 WINGS",
                         "core": "STRONG CORE", "brace": "EACH ONE BRACES THE OTHERS", "tripod": "LIKE A TRIPOD",
                         "wind": "WIND", "whirl": "WHIRLPOOLS", "sway": "THE TOWER SWAYS", "steps": "SETBACKS",
                         "spiral": "IN A SPIRAL", "nogrip": "THE WIND CAN'T GET A GRIP", "heat": "HEAT",
                         "hard": "HARDENED IN THE PIPE", "night": "POUR AT NIGHT", "ice": "ICE IN THE MIX", "m": "M",
                         "record": "WORLD RECORD", "ride": "RIDE TO THE TOP", "spire": "200 M SPIRE",
                         "broken": "OUT OF ORDER", "stairs": "STAIRS"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مكنة حفر أنفاق"),
                      "stat": [("828", "متر"), ("163", "دور"), ("57", "أسانسير")],
                      "L": {"floors": "دور", "tallest": "أطول برج في الدنيا", "sand": "رمل", "rock": "صخر طري",
                            "heavy": "تقيل أوي", "piles": "عمود", "deep": "50 متر لتحت", "grip": "الأرض ماسكاهم",
                            "holds": "شايلاه", "skinny": "رفيع أوي", "pencil": "قلم على سنه", "wings": "تلات جناحات",
                            "core": "قلب جامد", "brace": "كل واحد ساند التانيين", "tripod": "زي حامل الكاميرا",
                            "wind": "الهوا", "whirl": "دوامات", "sway": "البرج بيتهز", "steps": "دخلة",
                            "spiral": "زي الحلزونة", "nogrip": "الهوا اتلخبط", "heat": "الحر", "hard": "شدت في الماسورة",
                            "night": "صب بالليل", "ice": "تلج في الخلطة", "m": "متر", "record": "رقم قياسي",
                            "ride": "اطلع فوق", "spire": "سارية 200 متر", "broken": "عطلان", "stairs": "سلمة"}}}
    SKY_ALT = {"sky": 0.3}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "stack": ("hook", "STACK", 0.1), "sixty": ("hook", "SIXTY", 0.3), "desert": ("hook", "DESERT", 0.5),
            "congrats": ("hook", "CONGRATS", 0.65), "tallest": ("hook", "TALLEST", 0.9),
            "ground": ("break1", "GROUND", 0.1), "sand": ("break1", "SAND", 0.3), "soft": ("break1", "SOFT", 0.45),
            "heavy": ("break1", "HEAVY", 0.7), "sink": ("break1", "SINK", 0.9),
            "drill": ("fix1", "DRILL", 0.1), "piles": ("fix1", "PILES", 0.35), "fifty": ("fix1", "FIFTY", 0.45),
            "gripping": ("fix1", "GRIPPING", 0.7), "holds": ("fix1", "HOLDS", 0.9),
            "stands": ("break2", "STANDS", 0.1), "skinny": ("break2", "SKINNY", 0.35), "wobble": ("break2", "WOBBLE", 0.55),
            "pencil": ("break2", "PENCIL", 0.75), "tip": ("break2", "TIP", 0.92),
            "three": ("fix2", "THREE", 0.1), "wings": ("fix2", "WINGS", 0.2), "core": ("fix2", "CORE", 0.4),
            "bracing": ("fix2", "BRACING", 0.65), "tripod": ("fix2", "TRIPOD", 0.9),
            "high": ("break3", "HIGH", 0.1), "wind": ("break3", "WIND", 0.25), "whirl": ("break3", "WHIRLPOOLS", 0.5),
            "sway": ("break3", "SWAY", 0.9),
            "steps": ("fix3", "STEPS", 0.1), "twenty": ("fix3", "TWENTY", 0.25), "climbs": ("fix3", "CLIMBS", 0.45),
            "spiral": ("fix3", "SPIRAL", 0.6), "grip": ("fix3", "GRIP", 0.92),
            "shape": ("break4", "SHAPE", 0.1), "heat": ("break4", "HEAT", 0.35), "concrete": ("break4", "CONCRETE", 0.55),
            "hardens": ("break4", "HARDENS", 0.75), "top4": ("break4", "TOP", 0.95),
            "night": ("fix4", "NIGHT", 0.1), "ice": ("fix4", "ICE", 0.3), "pump": ("fix4", "PUMP", 0.5),
            "record": ("fix4", "RECORD", 0.65), "six": ("fix4", "SIX", 0.75), "up": ("fix4", "UP", 0.95),
            "ride": ("cta", "RIDE", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "push": ("reveal", "PUSH", 0.1), "spire": ("reveal", "SPIRE", 0.35), "roof": ("reveal", "ROOF", 0.6),
            "lights": ("reveal", "LIGHTS", 0.92),
            "s1": ("stat", "EIGHT", 0.04), "s2": ("stat", "SIXTY", 0.4), "s3": ("stat", "FIFTY", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "day": ("tag", "DAY", 0.1), "elev": ("tag", "ELEVATOR", 0.3), "breaks": ("tag", "BREAKS", 0.45),
            "two": ("tag", "TWO", 0.65), "stairs": ("tag", "STAIRS", 0.95)})
        T["built1"] = max(1.2, T["congrats"] - 0.15)                      # hook: the floors are all stacked
        T["climb0"] = T["pump"] - 0.05                                     # fix4: the concrete climbs the pipe
        T["climb1"] = max(T["climb0"] + 1.6, max(T["up"], T["six"]) + 0.2)
        T["rec"] = max(T["record"], T["climb1"])
        T["ice1"] = min(T["ice"], T["pump"] - 0.5) - 0.1
        # ---- sets
        self.cut(s("fix1") - 0.12, "ground", 1)
        self.cut(s("break2") - 0.12, "desert", -1)
        self.cut(s("fix2") - 0.12, "plan", 1)
        self.cut(s("break3") - 0.12, "sky", -1)
        self.cut(s("fix3") - 0.12, "sky", 1)                       # same set: the camera drops to the lower tiers
        self.cut(s("break4") - 0.12, "pump", 1)
        self.cut(s("fix4") - 0.12, "pump", -1)                     # same set: the stuck concrete is cleared away
        self.cut(s("cta") + 0.05, "desert", -1)
        self.cut(s("tag") - 0.2, "lobby", 1)
        self.cams = {"desert": Camera(0, -135, 2.0), "ground": Camera(0, 380, 1.0), "plan": Camera(0, 60, 1.35),
                     "sky": Camera(0, -740, 1.2), "pump": Camera(40, -375, 0.72), "lobby": Camera(0, -230, 1.18)}
        cm = self.cams
        cm["desert"].key(0.1, 0, -225, 1.2, max(0.8, T["sixty"] - 0.1))
        cm["desert"].key(T["sixty"], 0, -400, 0.78, max(0.8, T["congrats"] - T["sixty"]))
        cm["desert"].key(T["congrats"] - 0.1, 0, -435, 0.62, 1.0)
        cm["desert"].key(s("break1") - 0.1, 0, -40, 0.8, 1.0)
        cm["desert"].key(s("break2") - 0.12, 0, -560, 0.66, 0.0).key(s("break2") + 0.1, 0, -520, 0.7, 3.0)
        cm["desert"].key(s("cta") + 0.05, 0, -465, 0.58, 0.0)
        cm["desert"].key(s("reveal") - 0.1, 0, -519, 0.52, 1.4)
        cm["desert"].key(T["s1"] - 0.3, 0, -600, 0.45, 1.0).key(s("closer") - 0.2, 0, -574, 0.47, 1.0)
        cm["ground"].key(s("fix1"), 0, 365, 1.03, 4.0)
        cm["plan"].key(s("fix2") - 0.12, 0, 60, 1.35, 0.0).key(T["wings"] - 0.2, 0, 60, 1.0, 1.2)
        cm["sky"].key(s("break3"), 0, -760, 1.25, 3.5)
        cm["sky"].key(s("fix3") - 0.12, 0, -600, 1.15, 0.0)
        cm["sky"].key(T["steps"], 0, -740, 1.2, max(1.0, T["climbs"] - T["steps"] + 0.8))
        cm["pump"].key(s("break4"), 30, -360, 0.75, 4.0)
        cm["pump"].key(s("fix4") - 0.12, -330, -170, 1.6, 0.0).key(T["climb0"] - 0.2, 30, -390, 0.69, 1.4)
        cm["lobby"].key(s("tag"), 30, -250, 1.22, 3.0)
        # ---- tracks
        self.built = Track(0.035).to(0.1, 1.0, T["built1"] - 0.1, lambda u: 1 - (1 - u) ** 1.6)
        self.sink = Track(0.0).to(T["sink"] - 0.15, 170.0, 1.0, e_in)
        self.tilt = Track(0.0).to(T["sink"] - 0.05, 3.5, 1.0, e_in)
        self.wob = Track(0.0).to(T["wobble"] - 0.25, 1.0, 0.5)
        self.coreshake = Track(1.0).to(T["wings"] + 0.2, 0.0, 0.9)
        self.swayamp = Track(0.0).to(T["whirl"] - 0.1, 1.0, 0.9).to(s("fix3") - 0.12, 0.9, 0.0)
        self.swayamp.to(T["climbs"], 0.0, max(1.0, T["grip"] - T["climbs"]))
        self.stepk = Track(0.0).to(T["steps"] - 0.1, 1.0, max(1.6, T["climbs"] - T["steps"] + 0.5), lambda u: u)
        self.heat = Track(0.35).to(T["heat"] - 0.2, 0.95, 0.8)
        self.fill = Track(0.0).to(T["concrete"] - 0.1, 0.45, max(1.0, T["hardens"] - T["concrete"] + 0.1), e_out)
        self.hard = Track(0.0).to(T["hardens"] - 0.05, 1.0, 0.5)
        self.nightk = Track(0.0).to(T["night"] - 0.2, 1.0, 0.8)
        self.flow = Track(0.0).to(T["climb0"], 1.0, T["climb1"] - T["climb0"], e_io)
        self.spire = Track(0.0).to(T["push"] - 0.1, 1.0, max(1.2, T["roof"] - T["push"] + 0.3), e_io)
        self.lights = Track(0.0).to(T["lights"] - 0.1, 1.0, 0.7)
        self.revnight = Track(0.0).to(s("reveal"), 1.0, 1.2)
        self.spans = [(T["sink"], T["holds"] + 0.3), (T["wobble"], T["tripod"] + 0.3), (T["whirl"], T["grip"] + 0.3),
                      (T["hardens"], T["rec"] + 0.3)]
        self.shakes = [(T["built1"], 0.3, 8), (T["sink"], 0.9, 12), (T["holds"], 0.3, 8), (T["sway"], 0.5, 6),
                       (T["hardens"], 0.3, 8), (T["rec"], 0.3, 8), (T["roof"], 0.3, 8), (s("closer") + 0.2, 0.35, 10),
                       (T["breaks"], 0.25, 6)]
        # whirlpools behind the tower (sky set): (birth, x, y, max radius, life, spin sign, alpha)
        rng = random.Random(26)
        vs, k, tb = [], 0, T["whirl"] - 0.45
        while tb < s("fix3") + 0.6:
            vs.append((tb, 150, -560 - (k % 2) * 190 - (k * 97) % 120, 115, 2.4, 1 if k % 2 else -1, 0.9))
            tb += 0.45
            k += 1
        tb = T["grip"] - 0.7
        while tb < s("break4"):
            vs.append((tb, rng.uniform(40, 150), rng.uniform(-1080, -260), rng.uniform(16, 34), 0.7, rng.choice((-1, 1)), 0.45))
            tb += 0.09
        self.vort = vs
        order = sorted(range(11), key=lambda i: abs(i - 5) * 2 + (i > 5))
        self.pile_t = {i: T["drill"] - 0.05 + 0.13 * n for n, i in enumerate(order)}

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ set: the desert, side view
    def draw_desert(self, c, t):
        T, s, e = self.T, self.tl.s, self.tl.e
        cam = self.cams["desert"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        late = t >= s("cta") - 0.2
        self.backdrop(c, t, cx, cy, gy, moon=late, ridges=DUNES)
        nk = self.revnight.at(t) if late else 0.0
        if nk > 0:
            c.drawRect(R(0, 0, W, H), P("#050816", 0.28 * nk))
        self.view(c, cam)
        skyline_night(c, -1800, -430, 0, seed=4, hmin=50, hmax=240, lit=0.3 + 0.3 * nk, t=t)
        skyline_night(c, 430, 1800, 0, seed=7, hmin=50, hmax=210, lit=0.3 + 0.3 * nk, t=t)
        x0, x1 = cx - 760 / z, cx + 760 / z
        v2.ground(c, x0, x1, surface="#C99355", pal=SANDG)
        vrect(c, x0, 175, x1 - x0, 900, [("#3E2A1C", 0.0), ("#3E2A1C", 0.55), ("#24170D", 0.8)], [0, 0.08, 1])
        rng = random.Random(5)
        for _ in range(int((x1 - x0) / 40)):                                        # sand grains and rock cracks
            gx_, gy_ = rng.uniform(x0, x1), rng.uniform(26, 165)
            c.drawCircle(gx_, gy_, rng.uniform(1.5, 3.5), P("#E9C38A", 0.35))
        for k in range(10):
            px_ = -620 + k * 140
            c.drawLine(px_, 220 + (k % 3) * 40, px_ + 60, 260 + (k % 2) * 50, P("#1A110A", 0.5, stroke=3))
        if t < s("break2") - 0.12:                                                  # hook + break1: the skinny tower
            sk = self.sink.at(t)
            if sk > 0:
                contact_shadow(c, 0, 0, 260, 0.5)
            c.save()
            c.translate(0, sk)
            tower(c, t, wing=0.0, step=0.0, built=self.built.at(t), rot=self.tilt.at(t))
            c.restore()
            if sk > 0:
                v2.smoke(c, 0, 0, t, T["sink"] - 0.1, T["sink"] + 0.9, rate=30, life=1.2, spread=(260, -80), rise=-30,
                         size=(18, 70), col="#D9A35C", lit=None, lit_until=0.0, seed=21, a=0.7)
                v2.debris(c, 0, -6, t, T["sink"] - 0.05, dur=1.2, n=18, speed=520, seed=22, gravity=1100,
                          cols=("#E9C38A", "#C99355", "#8A5A33"))
            else:
                contact_shadow(c, 0, 0, 200, 0.5)
            hk = prog(t, T["built1"] - 0.05, T["built1"] + 0.25)
            if 0 < hk < 1:
                v2.shock_ring(c, 0, 0, t, T["built1"] - 0.05, 0.6, r1=420, col="#FDE68A", width=10, squash=0.25)
        elif not late:                                                               # break2: it wobbles like a pencil
            w = self.wob.at(t)
            rot = w * 5.5 * math.sin((t - T["wobble"]) * 4.4)
            contact_shadow(c, 0, 0, 200, 0.5)
            tower(c, t, wing=0.0, step=0.0, built=1.0, rot=rot)
        else:                                                                        # the finished tower
            contact_shadow(c, 0, 0, 420, 0.55)
            sp, lt = self.spire.at(t), self.lights.at(t)
            tower(c, t, wing=1.0, step=1.0, built=1.0, spire=sp, lights=lt)
            u = prog(t, s("cta") + 0.2, e("cta") - 0.2)
            if 0 < u < 1 or (t < s("reveal") and u >= 1):                            # an elevator rides to the top
                yy = -BODY_H * e_io(u) * 0.97
                add_glow(c, 0, yy, 60, "#FDE68A", 0.9)
                c.drawRRect(rr(-9, yy - 12, 18, 24, 4), P("#FFF7D6", 0.95))
            if lt > 0:
                for k in range(3):
                    v2.shock_ring(c, 0, -BODY_H - SPIRE_H, t, T["lights"] + 0.15 * k, 0.8, r1=380, col="#FDE68A",
                                  width=8, squash=1.0)
            if t >= T["cong2"]:
                for k in range(4):
                    bx = (-520, 520, -360, 380)[k]
                    by = (-760, -820, -1080, -1120)[k]
                    v2.shock_ring(c, bx, by, t, T["cong2"] + 0.25 * k, 0.9, r1=180, col=("#FDE68A", "#F472B6", "#7DD3FC", "#A7F3D0")[k],
                                  width=7, squash=1.0)
        c.restore()
        self.ui["cam"] = cam

    def ui_desert(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        if tw < s("break1"):
            p = self.span(T["stack"] - 0.1, T["tallest"] - 0.2, 0.2, 0.2)
            if p > 0:
                n = int(round(163 * self.built.at(tw)))
                v2.chip(c, 260, 470, f"{n} {self.L['floors']}", p, accent=HILITE, size=50)
            self.chip(540, 470, "tallest", T["tallest"] - 0.15, s("break1") + 0.25, accent=HILITE, size=36)
            return
        if tw < s("fix1"):
            x0, y0 = self.at(-330, 70)
            self.label(x0, y0, 250, 820, "sand", T["sand"], s("fix1") - 0.15, "#FDE68A")
            x1, y1 = self.at(330, 250)
            self.label(x1, y1, 820, 820, "rock", T["soft"], s("fix1") - 0.15, "#FDBA74")
            self.chip(280, 560, "heavy", T["heavy"] - 0.05, s("fix1") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["sink"] + 0.3, s("fix1") - 0.2, x=880, y=560)
            self.red(T["sink"] + 0.3, 2.0)
            return
        if tw < s("cta") - 0.2:
            self.chip(540, 470, "skinny", T["skinny"] - 0.05, s("fix2") - 0.15, accent=WARN, size=44)
            w = self.wob.at(tw)
            pa = self.span(T["pencil"] - 0.15, s("fix2") - 0.1, 0.2, 0.2)
            if pa > 0:
                pencil(c, 860, 1000, 210, w * 9 * math.sin((tw - T["wobble"]) * 4.4 + 0.6), pa)
                self.chip(820, 680, "pencil", T["pencil"] - 0.05, s("fix2") - 0.15, accent=HILITE, size=30)
            self.badge("alert", T["wobble"] + 0.2, s("fix2") - 0.2, x=200, y=640)
            self.red(T["wobble"] + 0.2, 1.8)
            return
        if tw >= s("cta"):
            self.chip(540, 470, "ride", T["ride"] - 0.1, max(T["follow"] - 0.1, T["ride"] + 0.8), accent=GOOD, size=38)
        if tw >= s("reveal") - 0.1:
            x0, y0 = self.at(6, -BODY_H - SPIRE_H * 0.55 * self.spire.at(tw))
            if tw < T["s1"] - 0.3:
                self.label(x0, y0, 780, 640, "spire", T["spire"], T["s1"] - 0.35, "#E5E7EB")

    # ------------------------------------------------------------------ set: under the tower (fix1)
    def draw_ground(self, c, t):
        T = self.T
        cam = self.cams["ground"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        self.backdrop(c, t, cx, cy, gy, moon=False, ridges=DUNES)
        self.view(c, cam)
        x0, x1 = cx - 760 / z, cx + 760 / z
        vrect(c, x0, 0, x1 - x0, 240, ["#C99355", "#A87443", "#8A5A33"], [0, 0.35, 1])
        vrect(c, x0, 240, x1 - x0, 1500, ["#6E4A31", "#4F3423", "#2A1B10"], [0, 0.35, 1])
        c.drawRect(R(x0, -6, x1 - x0, 12), P("#E2B36F"))
        rng = random.Random(8)
        for _ in range(140):
            gx_, gy_ = rng.uniform(x0, x1), rng.uniform(16, 230)
            c.drawCircle(gx_, gy_, rng.uniform(1.5, 4), P("#F0CB92", 0.35))
        for _ in range(26):
            rx, ry, rad = rng.uniform(x0, x1), rng.uniform(280, 900), rng.uniform(10, 26)
            c.drawCircle(rx, ry, rad, P("#3B2819", 0.7))
        grip = prog(t, T["gripping"] - 0.1, T["gripping"] + 0.4)
        if grip > 0:                                                                # the ground squeezing the piles
            for i in range(11):
                px = -400 + i * 80
                c.drawRect(R(px - 34, 40, 68, 520), P("#FDE68A", 0.10 * grip, blur=10))
        for i in range(11):                                                         # the piles, drilled one by one
            px = -400 + i * 80
            t0 = self.pile_t[i]
            k = e_out(prog(t, t0, t0 + 0.6))
            if k <= 0:
                continue
            d = 36 + 524 * k
            c.drawRect(R(px - 17, 36, 34, d - 36), lin_paint(px - 17, 0, px + 17, 0, ["#C4C9D1", "#9CA3AF", "#5B6270"]))
            if k < 1:
                for j in range(4):                                                  # the auger at the tip
                    yy = d - 8 - j * 14
                    ph = (t * 30 + j) % 2
                    c.drawLine(px - 17, yy + (6 if ph < 1 else -6), px + 17, yy - (6 if ph < 1 else -6), P("#475569", 1, stroke=4))
                v2.debris(c, px, 0, t, t0, dur=0.6, n=5, speed=380, seed=40 + i, gravity=1400,
                          cols=("#F0CB92", "#C99355", "#8A5A33"))
            if grip > 0:
                for j in range(5):
                    yy = 130 + j * 95
                    q = clamp(grip * 2.2 - j * 0.25)
                    pulse = 0.6 + 0.4 * math.sin(t * 8 - j * 0.8 + i)
                    for sd in (-1, 1):
                        arrow_up(c, px + sd * 28, yy, 10, GOOD, q * pulse)
        c.drawRect(R(-470, 0, 940, 36), lin_paint(0, 0, 0, 36, [shade(CONC, 0.2), shade(CONC, -0.3)]))   # the raft
        c.drawRect(R(-470, 0, 940, 3), P("#FFFFFF", 0.35))
        hold = prog(t, T["holds"] - 0.1, T["holds"] + 0.3)
        if hold > 0:
            c.drawRect(R(-470, 0, 940, 36), P(GOOD, 0.35 * hold * (1 - prog(t, T["holds"] + 0.6, T["holds"] + 1.4))))
        c.save()
        c.drawRect(R(-130, -1600, 260, 1600), lin_paint(-130, 0, 130, 0, [shade(GLS, 0.32), GLS, shade(GLS, -0.18), GLS_D],
                                                         [0, 0.35, 0.62, 1]))
        for k in range(1, 40):
            c.drawLine(-130, -k * 40, 130, -k * 40, P("#22314A", 0.3, stroke=2))
        c.drawRect(R(-26, -1600, 30, 1600), P("#FFFFFF", 0.13))
        c.restore()
        wk = 1 - prog(t, T["holds"] - 0.2, T["holds"] + 0.2)                     # the weight pressing down
        big_arrow(c, 0, -400, -150, 60, WARN, 0.85 * wk * prog(t, self.tl.s("fix1"), self.tl.s("fix1") + 0.4))
        rk = prog(t, T["fifty"] - 0.25, T["fifty"] + 0.25)                        # depth ruler
        if rk > 0:
            c.drawLine(440, 36, 440, 36 + 524 * rk, P(HILITE, 1, stroke=5))
            for j in range(6):
                yy = 36 + j * 104.8
                if yy <= 36 + 524 * rk + 0.5:
                    c.drawLine(424, yy, 456, yy, P(HILITE, 1, stroke=4))
        c.restore()
        self.ui["cam"] = cam

    def ui_ground(self, c, t, tw):
        T, s = self.T, self.tl.s
        p = self.span(T["drill"] - 0.05, s("break2") - 0.15, 0.2, 0.2)
        if p > 0:
            n = int(round(192 * prog(tw, T["drill"], max(T["piles"] + 0.3, T["drill"] + 1.5))))
            v2.chip(c, 250, 440, f"{n} {self.L['piles']}", p, accent=HILITE, size=44)
        x0, y0 = self.at(440, 560)
        self.label(x0, y0, 790, 1060, "deep", T["fifty"], s("break2") - 0.15, HILITE, size=32)
        self.chip(790, 440, "grip", T["gripping"] - 0.05, T["holds"] - 0.1, accent=GOOD, size=30)
        self.chip(790, 440, "holds", T["holds"] - 0.05, s("break2") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["holds"] + 0.15, s("break2") - 0.15, x=900, y=300)

    # ------------------------------------------------------------------ set: the plan, from above (fix2)
    WING_ANG = (-90.0, 30.0, 150.0)

    def draw_plan(self, c, t):
        T = self.T
        cam = self.cams["plan"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, W, H, ["#6B4A30", "#4A3122", "#2B1C12"]))
        self.view(c, cam)
        for k in range(16):                                                         # dunes from above
            path = skia.Path()
            yb = -1300 + k * 170
            path.moveTo(-1200, yb)
            for xx in range(-1200, 1240, 60):
                path.lineTo(xx, yb + 46 * math.sin(xx * 0.004 + k * 1.3))
            c.drawPath(path, P("#000000", 0.10, stroke=34))
            c.drawPath(path, P("#E2B36F", 0.07, stroke=6))
        jig = self.coreshake.at(t)
        ox, oy = math.sin(t * 23) * 14 * jig, math.cos(t * 19) * 10 * jig
        c.save()
        c.translate(ox, oy)
        ks = [e_out(prog(t, T["wings"] - 0.25 + 0.16 * i, T["wings"] + 0.45 + 0.16 * i)) for i in range(3)]
        c.save()                                                                     # long shadow to the lower right
        c.translate(70, 40)
        for ang, k in zip(self.WING_ANG, ks):
            if k > 0:
                c.save()
                c.rotate(ang)
                c.drawRRect(rr(40, -66, 320 * k, 132, 60), P("#000000", 0.35, blur=12))
                c.restore()
        c.drawPath(hexagon(96), P("#000000", 0.35, blur=12))
        c.restore()
        brace = prog(t, T["bracing"] - 0.1, T["bracing"] + 0.4)
        for ang, k in zip(self.WING_ANG, ks):
            if k <= 0:
                continue
            c.save()
            c.rotate(ang)
            L = 320 * k
            c.drawRRect(rr(30, -66, L + 10, 132, 60), lin_paint(0, -66, 0, 66, [shade(GLS, 0.35), GLS, GLS_D]))
            for yy in (-24, 24):
                c.drawLine(40, yy, 30 + L - 36, yy, P(mix("#334155", HILITE, brace), 0.9, stroke=6 + 4 * brace))
            for xx in range(80, int(L), 60):
                c.drawLine(xx, -60, xx, 60, P("#1E293B", 0.25, stroke=2))
            c.restore()
        c.drawPath(hexagon(96), lin_paint(-96, -96, 96, 96, [shade(CONC, 0.3), CONC, shade(CONC, -0.35)]))
        c.drawPath(hexagon(56), P("#475569"))
        for k in range(6):
            q = math.radians(30 + k * 60)
            c.drawRect(R(math.cos(q) * 34 - 9, math.sin(q) * 34 - 9, 18, 18), P("#1E293B"))
        c.drawPath(hexagon(96), P("#E2E8F0", 0.6, stroke=4))
        if brace > 0:                                                                # wings bracing each other
            for a0, a1 in ((-90, 30), (30, 150), (150, 270)):
                path = skia.Path()
                n = 18
                for j in range(n + 1):
                    q = math.radians(lerp(a0 + 18, a1 - 18, j / n))
                    (path.moveTo if j == 0 else path.lineTo)(math.cos(q) * 188, math.sin(q) * 188)
                pm = skia.PathMeasure(path, False)
                seg = skia.Path()
                pm.getSegment(0, pm.getLength() * brace, seg, True)
                c.drawPath(seg, P(GOOD, 0.95, stroke=9))
                if brace >= 1:
                    for q_ in (a0 + 18, a1 - 18):
                        q = math.radians(q_)
                        c.drawCircle(math.cos(q) * 188, math.sin(q) * 188, 11, P(GOOD))
        c.restore()
        tk = prog(t, T["tripod"] - 0.2, T["tripod"] + 0.3)
        tripod(c, 330, -230, 1.15, tk, 1.0)
        c.restore()
        self.ui["cam"] = cam

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(-215, 125)
        self.label(x0, y0, 250, 640, "wings", T["three"] - 0.05, s("break3") - 0.15, HILITE)
        x1, y1 = self.at(0, 0)
        self.label(x1, y1, 270, 1150, "core", T["core"], s("break3") - 0.15, "#E5E7EB", size=30)
        self.chip(540, 470, "brace", T["bracing"] - 0.05, T["tripod"] - 0.15, accent=GOOD, size=30)
        self.chip(540, 470, "tripod", T["tripod"] - 0.05, s("break3") - 0.15, accent=GOOD, size=38)
        self.badge("check", T["tripod"] + 0.2, s("break3") - 0.15, x=900, y=330)

    # ------------------------------------------------------------------ set: up high in the wind (break3, fix3)
    def draw_sky(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["sky"].at(t)
        cx, cy, z = cam
        v2.sky(c, W, H, 0.3, horizon_y=H * 1.25)
        v2.stars(c, W, H, t, 0.5)
        for i, (px, py, s_) in enumerate(((180, 1500, 1.3), (760, 1700, 1.5), (420, 1880, 1.2), (980, 1350, 0.9))):
            v2.cloud(c, (px + t * (14 + 4 * i)) % (W + 600) - 300, py - (cy + 800) * 0.4, s_, a=0.8, seed=i + 3)
        self.view(c, cam)
        windk = prog(t, T["wind"] - 0.4, T["wind"] + 0.2)
        if windk > 0:                                                                # streams of wind, left to right
            for j in range(26):
                yy = -1500 + j * 58
                off = (t * 820 + j * 53) % 170
                xx = -720 + off - 170
                while xx < 720:
                    wy = yy + (math.sin(xx * 0.02 + t * 6 + j) * 10 if xx > 160 else 0)
                    c.drawLine(xx, wy, xx + 90, wy, P("#DBEAFE", 0.32 * windk, stroke=4))
                    xx += 170
        steps = self.stepk.at(t) if t >= s("fix3") - 0.12 else 0.0
        stepf = (lambda i: clamp(steps * (TIERS + 2) - i))
        rot = self.swayamp.at(t) * 1.7 * math.sin(t * 2 * math.pi * 1.25)
        tower(c, t, wing=1.0, step=stepf, built=1.0, rot=rot)
        for tb, vx, vy, rmax, life, sg, al in self.vort:                            # whirlpools
            age = t - tb
            if not (0 <= age < life):
                continue
            u = age / life
            r = rmax * (0.25 + 0.75 * e_out(u))
            if steps > 0 and rmax > 60:                                              # the steps break them up
                r *= 1 - 0.7 * steps
            vortex(c, vx + r * 0.8 + age * 150, vy + math.sin(age * 3) * 16, r, age * 5 * sg, sg, al * (1 - u * u) * windk)
        sk = prog(t, T["spiral"] - 0.2, T["spiral"] + 0.7)
        if sk > 0 and t >= s("fix3") - 0.12:                                        # the spiral, wrapping up the tower
            pts = []
            n = 120
            for j in range(int(n * sk) + 1):
                u = j / n
                i = min(TIERS - 1, int(u * TIERS))
                lft, rgt = tier_hw(i, 1.0, stepf)
                q = u * 3.0 * 2 * math.pi
                hw = (lft + rgt) / 2 + 26
                pts.append((math.sin(q) * hw + (rgt - lft) / 2, -u * BODY_H, math.cos(q)))
            for (x0, y0, f0), (x1, y1, f1) in zip(pts, pts[1:]):
                c.drawLine(x0, y0, x1, y1, P(HILITE, 0.95 if f0 > 0 else 0.3, stroke=7 if f0 > 0 else 4))
        c.restore()
        for i, (px, s_) in enumerate(((120, 1.6), (520, 1.9), (930, 1.5), (300, 1.3), (760, 1.4))):   # cloud bank below
            v2.cloud(c, (px + t * (10 + 3 * i)) % (W + 500) - 250, 1660 + (i % 2) * 120 + (cy + 740) * 0.5, s_, a=0.95, seed=i + 7)
        self.ui["cam"] = cam
        self.ui["rot"] = rot

    def ui_sky(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(240, 470, "wind", T["wind"] - 0.1, T["sway"] - 0.15, accent="#7DD3FC", size=44)
            x0, y0 = self.at(270, -700)
            self.label(min(x0, 1000), y0, 820, 470, "whirl", T["whirl"], s("fix3") - 0.15, "#E0F2FE")
            self.chip(290, 470, "sway", T["sway"] - 0.1, s("fix3") - 0.15, accent=WARN, size=34)
            self.badge("alert", T["sway"], s("fix3") - 0.2, x=880, y=640)
            self.red(T["sway"], 1.8)
            return
        p = self.span(T["steps"] - 0.1, s("break4") - 0.15, 0.2, 0.2)
        if p > 0:
            n = int(round(27 * clamp(self.stepk.at(tw))))
            v2.chip(c, 540, 470, f"{n} {self.L['steps']}", p, accent=HILITE, size=50)
        self.chip(260, 640, "spiral", T["spiral"] - 0.05, s("break4") - 0.15, accent=HILITE, size=34)
        self.chip(540, 1150, "nogrip", T["grip"] - 0.1, s("break4") - 0.15, accent=GOOD, size=32)
        self.badge("check", T["grip"] + 0.2, s("break4") - 0.15, x=880, y=640)

    # ------------------------------------------------------------------ set: pouring the concrete (break4, fix4)
    PIPE_X = -40

    def draw_pump(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["pump"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        nk = self.nightk.at(t) if t >= s("fix4") - 0.12 else 0.0
        pal = {k: mix(DAY[k], v2.NIGHT[k], nk) for k in DAY}
        v2.sky(c, W, H, 0.0, pal=pal, horizon_y=gy)
        if nk < 1:                                                                   # the desert sun
            add_glow(c, 850, 600, 380, "#FFF3C4", 0.85 * (1 - nk))
            c.drawCircle(850, 600, 70, P("#FFF7DA", 0.95 * (1 - nk)))
            hk = self.heat.at(t) * (1 - nk)
            for j in range(7):
                path = skia.Path()
                yb = gy - 60 - j * 70 - (t * 40) % 70
                path.moveTo(0, yb)
                for xx in range(0, W + 40, 40):
                    path.lineTo(xx, yb + math.sin(xx * 0.03 + t * 5 + j) * 6)
                c.drawPath(path, P("#FFFFFF", 0.10 * hk, stroke=3))
        if nk > 0:
            v2.stars(c, W, H, t, nk)
            v2.moon(c, 236, gy - 900, 66, a=nk)
        c.save()
        c.translate(W / 2 - cx * 0.06 * z, gy)
        v2.ridge(c, -1500, 1500, 0, 230, mix("#C98A52", DUNES[0][0], nk), mix("#E6A866", DUNES[0][1], nk), seed=5, step=150, rough=0.5)
        c.restore()
        self.view(c, cam)
        x0, x1 = cx - 760 / z, cx + 760 / z
        v2.ground(c, x0, x1, surface=mix("#E2B36F", "#C99355", nk), pal=SANDG)
        built = 0.93
        topy = -BODY_H * built
        contact_shadow(c, 0, 0, 420, 0.5)
        tower(c, t, wing=1.0, step=1.0, built=built, lights=0.25 * nk)
        crane(c, 10, topy, t)
        px = self.PIPE_X
        c.drawLine(-250, -14, px, -14, P("#0F172A", 1, stroke=30))                   # the pipe
        c.drawLine(px, -14, px, topy + 8, P("#0F172A", 1, stroke=30))
        c.drawLine(px, -14, px, topy + 8, P("#334155", 1, stroke=16))
        c.drawLine(-250, -14, px, -14, P("#334155", 1, stroke=16))
        fixed = t >= s("fix4") - 0.12
        if not fixed:
            f = self.fill.at(t)
            hd = self.hard.at(t)
            if f > 0:
                yy = -14 + (topy + 8 + 14) * f
                col = mix("#E5E7EB", "#6B7280", hd)
                c.drawLine(-250, -14, px, -14, P(col, 1, stroke=16))
                c.drawLine(px, -14, px, yy, P(col, 1, stroke=16))
                if hd > 0.4:
                    add_glow(c, px, yy, 90, WARN, 0.5 * hd * (0.6 + 0.4 * math.sin(t * 8)))
                    for j in range(5):                                               # cracks: it set in the pipe
                        cy_ = yy + 10 + j * 24
                        c.drawLine(px - 8, cy_, px + 7, cy_ + 12, P("#111827", hd, stroke=3))
                    c.drawLine(px - 22, yy - 22, px + 22, yy + 2, P(WARN, hd, stroke=7))
                    c.drawLine(px + 22, yy - 22, px - 22, yy + 2, P(WARN, hd, stroke=7))
                    k_ = prog(t, T["hardens"] + 0.2, T["hardens"] + 0.5)
                    if k_ > 0:
                        path = skia.Path()
                        path.moveTo(px, yy - 20)
                        path.lineTo(px, topy + 40)
                        c.drawPath(path, dash_paint(WARN, 0.8 * k_, w=5, t=t))
            mixer(c, -380, t, spin=1.0)
        else:
            f = self.flow.at(t)
            if f > 0:
                yy = -14 + (topy + 8 + 14) * f
                c.drawLine(-250, -14, px, -14, P("#E5E7EB", 1, stroke=16))
                c.drawLine(px, -14, px, yy, P("#E5E7EB", 1, stroke=16))
                for j in range(int(abs(yy) / 60) + 1):                               # moving highlights
                    hy = -14 - ((j * 60 + t * 260) % max(60.0, abs(yy + 14)))
                    c.drawLine(px - 3, hy, px - 3, hy - 18, P("#FFFFFF", 0.8, stroke=3))
                add_glow(c, px, yy, 70, "#FDE68A", 0.7 * (1 - prog(t, T["climb1"], T["climb1"] + 0.6)) + 0.2)
            mixer(c, -380, t, spin=2.0)
            for j in range(9):                                                        # ice into the mixer
                t0 = T["ice1"] + j * 0.08
                u = prog(t, t0, t0 + 0.5)
                if 0 < u < 1:
                    ice(c, -420 + (j % 3) * 26, lerp(-620, -170, u * u), 26, u * 300 + j * 40, 1 - prog(u, 0.85, 1.0))
            if T["ice1"] <= t < T["ice1"] + 1.4:
                sparks_shower(c, -400, -170, t, T["ice1"] + 0.45, dur=0.6, n=14, speed=320, seed=9, col="#BAE6FD")
            if t >= T["rec"]:
                v2.shock_ring(c, px, topy, t, T["rec"], 0.8, r1=300, col="#FDE68A", width=10, squash=1.0)
        c.restore()
        self.ui["cam"] = cam

    def ui_pump(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui["cam"]
        topy = -BODY_H * 0.93
        if tw < s("fix4") - 0.12:
            p = self.span(s("break4") - 0.1, s("fix4") - 0.15)
            if p > 0:
                k = self.heat.at(tw)
                v2.gauge(c, 60, 300, [(self.L["heat"], k, mix(HILITE, WARN, k))], p, w=330)
            f = self.fill.at(tw)
            x0, y0 = self.at(self.PIPE_X, -14 + (topy + 22) * f)
            self.label(x0, y0, 790, 760, "hard", T["hardens"] - 0.05, s("fix4") - 0.15, WARN, size=30)
            self.badge("alert", T["hardens"] + 0.2, s("fix4") - 0.2, x=880, y=330)
            self.red(T["hardens"] + 0.2, 1.8)
            return
        self.chip(760, 470, "night", T["night"] - 0.1, T["ice"] - 0.1, accent="#A5B4FC", size=40)
        self.chip(760, 470, "ice", T["ice"] - 0.05, T["climb0"] + 0.4, accent="#7DD3FC", size=40)
        p = self.span(T["climb0"] + 0.3, s("cta") - 0.1, 0.2, 0.2)
        if p > 0:
            n = int(round(606 * self.flow.at(tw)))
            v2.chip(c, 250, 640, f"{n} {self.L['m']}", p, accent=GOOD, size=58)
        self.chip(250, 760, "record", T["rec"] - 0.05, s("cta") - 0.1, accent=HILITE, size=36)
        self.badge("check", T["rec"] + 0.15, s("cta") - 0.05, x=880, y=760)

    # ------------------------------------------------------------------ set: the lobby (the tag)
    def draw_lobby(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["lobby"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), P("#0B0A14"))
        self.view(c, cam)
        vrect(c, -900, -1400, 1800, 1400, ["#3A3346", "#4A4156", "#2C2636"], [0, 0.6, 1])
        rng = random.Random(4)
        for _ in range(14):                                                          # marble veins
            path = skia.Path()
            vx, vy = rng.uniform(-900, 900), rng.uniform(-1300, -60)
            path.moveTo(vx, vy)
            path.cubicTo(vx + 80, vy + 40, vx + 140, vy - 50, vx + 260, vy + 20)
            c.drawPath(path, P("#FFFFFF", 0.06, stroke=3))
        vrect(c, -900, 0, 1800, 700, ["#2A2433", "#14111C"], [0, 1])
        c.drawRect(R(-900, -4, 1800, 8), P("#B49A6A", 0.8))
        c.drawRect(R(-300, -470, 260, 470), P("#1F2937"))                            # the elevator
        c.drawRect(R(-286, -456, 232, 456), P("#0F172A"))
        for k, (x0_, w_) in enumerate(((-282, 112), (-166, 108))):
            c.drawRect(R(x0_, -450, w_, 450), lin_paint(x0_, 0, x0_ + w_, 0, ["#CBD5E1", "#94A3B8", "#64748B"]))
        c.drawLine(-170, -450, -170, 0, P("#0F172A", 1, stroke=4))
        c.drawRRect(rr(-220, -540, 100, 54, 10), P("#111827"))
        bl = 0.5 + 0.5 * math.sin(t * 9)
        word(c, "X", -170, -500, 34, mix("#7F1D1D", "#EF4444", bl))
        bk = prog(t, T["elev"] - 0.2, T["elev"] + 0.2)                               # the sign, taped on
        if bk > 0:
            c.save()
            c.translate(-170, -280)
            c.rotate(-5)
            c.scale(e_back(bk), e_back(bk))
            c.drawRRect(rr(-120, -50, 240, 100, 8), P("#FDE047"))
            for xx in (-100, 80):
                c.drawRect(R(xx, -62, 22, 26), P("#F8FAFC", 0.8))
            word(c, self.L["broken"], 0, 14, 30, "#111827")
            c.restore()
        n = 34                                                                       # the stairs, going on forever
        sx, sy, sw, sh = 60, 0, 30, 34
        path = skia.Path()
        path.moveTo(sx, sy)
        x, y = sx, sy
        for i in range(n):
            path.lineTo(x, y - sh)
            x += sw
            path.lineTo(x, y - sh)
            y -= sh
        path.lineTo(x, sy)
        path.close()
        c.drawPath(path, lin_paint(sx, 0, x, 0, ["#6B5B4E", "#57493E"]))
        x, y = sx, sy
        for i in range(n):
            c.drawLine(x, y - sh, x + sw, y - sh, P("#C8B08A", 0.8, stroke=3))
            x += sw
            y -= sh
        c.drawLine(sx + 10, -120, x + 10, y - 120, P("#B49A6A", 1, stroke=6))
        for i in range(0, n, 3):
            c.drawLine(sx + 10 + i * sw, -i * sh - 120, sx + 10 + i * sw, -i * sh, P("#B49A6A", 0.8, stroke=3))
        pose = "point" if t >= T["breaks"] - 0.15 else "stand"
        person(c, -370, 0, 140, "#1E3A8A", t, pose, face=1, hat="cap", skin=SKINS_L[1])   # the doorman
        k = prog(t, T["two"], T["two"] + 1.5)
        ex = lerp(40, 70, k)
        person(c, ex, 0, 132, SHIRTS[0], t, "look" if t < T["stairs"] - 0.1 else "shrug", face=1, hat="hard")
        c.restore()
        self.ui["cam"] = cam

    def ui_lobby(self, c, t, tw):
        T, s = self.T, self.tl.s
        p = self.span(T["two"] - 0.1, self.duration, 0.2, 0.1)
        if p > 0:
            n = int(round(2909 * e_out(prog(tw, T["two"] - 0.1, T["two"] + 1.6))))
            v2.chip(c, 540, 470, f"{n:,} {self.L['stairs']}", p, accent=WARN, size=54)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, self.SKY_ALT.get(m, 0.0), horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10)]
        k, tb = 0, 0.15
        while tb < T["built1"] - 0.1 and k < 22:
            ev.append((tb, sfx.pop(61 + k), -14))
            tb += lerp(0.1, 0.2, k / 22)
            k += 1
        ev += [(T["built1"], sfx.thud(0.5, 90), -4), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 91), -9),
               (T["tallest"], sfx.chime(), -9)]
        ev += [(T["heavy"], sfx.creak(1.0, 92), -8), (T["sink"] - 0.1, rumble(1.4, 93), -5), (T["sink"] + 0.1, sfx.thud(0.6, 94), -6),
               (T["sink"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 95), -4)]
        for i in range(11):
            if i % 2 == 0:
                ev.append((self.pile_t[i], drill_snd(0.55, 96 + i), -12))
        ev += [(T["fifty"], sfx.ding(), -10), (T["gripping"], sfx.riser(0.6, 110), -12), (T["holds"], sfx.thunk(111), -5),
               (T["holds"] + 0.15, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 112), -4), (T["wobble"], sfx.creak(1.2, 113), -8),
               (T["wobble"] + 0.9, sfx.creak(1.0, 114), -9), (T["tip"], sfx.alarm(2, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 115), -4)]
        ev += [(T["wings"] - 0.2 + 0.16 * i, sfx.pop(116 + i), -6) for i in range(3)]
        ev += [(T["bracing"], sfx.snap(120), -8), (T["tripod"] - 0.1, sfx.click(121), -6), (T["tripod"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 122), -4), (T["wind"] - 0.4, wind_snd(3.4, 123), -8),
               (T["sway"], sfx.creak(1.2, 124), -8), (T["sway"] + 0.3, sfx.alarm(2, 820.0), -13)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 125), -5), (s("fix3"), wind_snd(2.0, 126), -14)]
        dur = max(1.6, T["climbs"] - T["steps"] + 0.5)
        ev += [(T["steps"] - 0.1 + dur * j / 27, sfx.tick(), -16) for j in range(0, 27, 2)]
        ev += [(T["spiral"] - 0.2, sfx.whirr(0.8, 300.0, 700.0, 127), -12), (T["grip"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 128), -4), (T["heat"], sfx.sizzle(0.8, 129), -10),
               (T["concrete"] - 0.1, sfx.hum(1.4, 70.0), -14), (T["hardens"], sfx.clank(240.0, 0.5, 130), -6),
               (T["hardens"] + 0.25, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, True, 131), -5), (T["night"] - 0.2, sfx.whoosh(0.9, False, 132), -12)]
        ev += [(T["ice1"] + j * 0.08 + 0.45, clink_snd(133 + j), -12) for j in range(0, 9, 2)]
        ev += [(T["climb0"], sfx.hum(T["climb1"] - T["climb0"], 90.0), -12), (T["climb0"], sfx.riser(T["climb1"] - T["climb0"], 140), -10),
               (T["rec"], sfx.bell(1046.5, 1.2, 0.9), -8), (T["rec"] + 0.1, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(150), 0), (T["follow"] - 0.15, sfx.pop(151), -4), (s("cta") + 0.05, sfx.whoosh(0.4, False, 152), -7),
               (s("cta") + 0.3, sfx.ding(), -12)]
        ev += [(T["push"] - 0.1, sfx.charge_up(1.0), -9), (T["roof"], sfx.clank(500.0, 0.4, 153), -8),
               (T["lights"] - 0.05, sfx.sparkle(1.0, 14, 154), -6), (T["lights"] + 0.1, sfx.bell(784.0, 1.4, 0.9), -9)]
        ev += [(T["s1"], sfx.pop(155), -3), (T["s2"], sfx.pop(156), -3), (T["s3"], sfx.pop(157), -3)]
        ev += [(T["cong2"], sfx.pop(158), -2), (T["cong2"], sfx.sparkle(1.0, 14, 159), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 160), -6), (T["elev"] - 0.2, sfx.ding(), -8), (T["elev"] + 0.2, sfx.buzz(0.42), -8)]
        k = 0
        while T["two"] + 0.2 + k * 0.22 < self.duration - 0.3 and k < 12:
            ev.append((T["two"] + 0.2 + k * 0.22, sfx.tap(161 + k), -10))
            k += 1
        return ev


NAME = "tower"
EPISODE = Tower
