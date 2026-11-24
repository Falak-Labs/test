"""Episode 73 - the Lighthouse of Alexandria (the Pharos).  v2 look: the tower in elevation on its island at the
harbour mouth (1 m = 6 units, sea level y = 0): a square tier, an eight-sided tier, a round tier, the lantern with the
fire and the bronze mirror, a statue on top; the low city on the shore behind.

Sets: harbor (hook: close on the fire, out to the whole tower at night with its beam over the sea; break1: no tower,
hidden rocks in x-ray, a ship hits one and sinks, "? km"; fix1: the three tiers stack up with a 100 m ruler and a
30-floor ghost; break2: night, the tower is a black shape and a ship drifts to the rocks; fix2: the fire is lit;
fix3: close on the lantern, the bronze mirror throws a beam over the waves; reveal: wide, a ship 50 km out, then the
earthquake drops the tower into the harbour; stat: under the water, the blocks on the sea floor and one lifted by a
crane; closer: the tower lit at night), far (break3: from a ship far out the fire is a tiny spark), ramp (break4: the
tower cut open, a fire that eats a pile of wood; fix4: a ramp winds up inside and donkeys carry the wood up), street
(tag: the delivery rider lost between identical houses while you wave a phone torch from the balcony).
"""
from v2_base import *  # noqa: F401,F403
from burjalarab import path_of, GOLDEN, NIGHTP  # noqa: E402
from windtower import sun  # noqa: E402
from pyramid import palm  # noqa: E402

DUSKP = {"top": "#0A0F2E", "upper": "#24215C", "mid": "#5B3A7A", "low": "#D0705E", "horizon": "#F6A86A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DAYP = {"top": "#0E2F5E", "upper": "#1B4F8F", "mid": "#2A62A4", "low": "#3E7AB8", "horizon": "#6FA4D6",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
SEA_C, SEA_D = "#1C6E8C", "#082A44"
ST = ("#F4EAD3", "#D8C7A2", "#A99068")          # stone: lit face, front, shade
FIRE = "#FFB347"
# tiers: (bottom y, top y, half width at bottom, half width at top)
T1 = (-30.0, -360.0, 80.0, 68.0)
T2 = (-360.0, -525.0, 50.0, 45.0)
T3 = (-525.0, -585.0, 30.0, 28.0)
LANT = (-585.0, -622.0)
TOP_Y = -668.0
FIRE_Y = -600.0
ROCKS = [(-420, 70, 54), (-250, 95, 40), (330, 80, 60), (520, 110, 46), (700, 70, 38)]


def _ease_fall(k):
    return k * k


def galley(c, x, y, s, t, a=1.0, tilt=0.0, sink=0.0, lamp=0.0, face=1):
    """An old sailing ship in side view, waterline at (x, y), s = scale (1 = about 30 m long)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y + sink * 70 * s + math.sin(t * 1.7 + x * 0.01) * 3 * s)
    c.rotate(tilt + math.sin(t * 1.3 + x) * 1.5)
    c.scale(s * face, s)
    hull = skia.Path()
    hull.moveTo(-95, -26)
    hull.lineTo(88, -26)
    hull.quadTo(112, -44, 116, -62)
    hull.quadTo(100, -14, 70, 8)
    hull.lineTo(-70, 8)
    hull.quadTo(-100, -6, -112, -48)
    hull.quadTo(-104, -30, -95, -26)
    hull.close()
    c.drawPath(hull, lin_paint(0, -40, 0, 8, ["#8A5A32", "#4A2C16"], a=a))
    c.drawLine(-95, -26, 88, -26, P("#C08A52", a, stroke=4))
    for k in range(7):                                                   # oar ports
        c.drawCircle(-60 + k * 20, -12, 3.2, P("#2A170A", a))
    c.drawLine(0, -26, 0, -190, P("#3A2414", a, stroke=6))
    c.drawLine(-62, -176, 62, -176, P("#3A2414", a, stroke=5))
    sail = skia.Path()
    sail.moveTo(-60, -174)
    sail.lineTo(60, -174)
    sail.quadTo(70, -110, 56, -56)
    sail.lineTo(-56, -56)
    sail.quadTo(-70, -110, -60, -174)
    sail.close()
    c.drawPath(sail, lin_paint(-60, 0, 60, 0, ["#F4E9D4", "#D9C6A2"], a=a))
    for k in range(3):
        c.drawLine(-58 + k * 0, -150 + k * 34, 58, -150 + k * 34, P("#B4462F", 0.75 * a, stroke=7))
    if lamp > 0:
        add_glow(c, 96, -50, 22, "#FFD58A", lamp * a)
        c.drawCircle(96, -50, 4, P("#FFF1C9", lamp * a))
    c.restore()


def rocks_under(c, t, xray=0.0, a=1.0):
    """Reefs just under the surface: dark shapes, outlined in red in x-ray."""
    for i, (x, y, r) in enumerate(ROCKS):
        p = path_of([(x - r * 1.6, y + 40), (x - r, y - r * 0.4), (x - r * 0.3, y - r * 0.9), (x + r * 0.5, y - r * 0.7),
                     (x + r * 1.2, y - r * 0.2), (x + r * 1.7, y + 40)], close=True)
        c.drawPath(p, P("#0A1C2A", 0.85 * a))
        if xray > 0:
            pa = dash_paint("#F87171", xray * a, w=4, t=t)
            c.drawPath(p, pa)
            add_glow(c, x, y - r * 0.4, r * 1.6, "#EF4444", 0.25 * xray * a)


def island(c, t, night=0.0, a=1.0):
    c.drawPath(path_of([(-330, 10), (-250, -14), (-160, -30), (160, -30), (250, -16), (340, 10)], close=True),
               lin_paint(0, -30, 0, 10, [mix("#B89A6A", "#3A3048", night), mix("#6B5236", "#1B1726", night)], a=a))
    rng = random.Random(4)
    for i in range(14):
        x = rng.uniform(-300, 300)
        c.drawCircle(x, rng.uniform(-14, 6), rng.uniform(8, 18), P(mix("#8C7350", "#262033", night), a))
    c.drawRect(R(-112, -38, 224, 10), P(mix(ST[1], "#2A2840", night), a))           # the plinth


def shore(c, t, night=0.0, a=1.0):
    """Alexandria on the far shore: a low line of houses, a few palms (world, base y = -20)."""
    rng = random.Random(11)
    x = -2400.0
    while x < -380:
        w = rng.uniform(40, 110)
        h = rng.uniform(26, 80)
        col = mix("#C9B48E", "#232A4A", night)
        c.drawRect(R(x, -20 - h, w, h), P(col, 0.9 * a))
        c.drawRect(R(x, -20 - h, w, 4), P(mix("#F2E6CC", "#38406A", night), 0.9 * a))
        if night > 0.4 and rng.random() < 0.5:
            c.drawRect(R(x + w * 0.4, -20 - h * 0.6, 8, 10), P("#FFD58A", 0.7 * night * a))
        x += w + rng.uniform(4, 26)
    for px in (-1900, -1500, -1150, -760, -520):
        palm(c, px, -20, 120, sway=math.sin(t * 0.8 + px) * 0.5, a=0.9 * a * (1 - 0.6 * night))
    c.drawRect(R(-2600, -22, 2240, 24), P(mix("#D9C08E", "#2A2A44", night), a))


def water(c, t, night=0.0, a=1.0, beam=0.0, beam_x=None, under=0.0):
    """The sea from the horizon (y = -22) down; under = 0..1 shows the water as seen from below the surface."""
    c.drawRect(R(-4000, -22, 8000, 22), lin_paint(0, -22, 0, 0, [mix("#6FB3C8", "#1B2A55", night), mix(SEA_C, "#10204A", night)], a=a))
    c.drawRect(R(-4000, 0, 8000, 4000), lin_paint(0, 0, 0, 900, [mix(SEA_C, "#0E1E4A", night), mix(SEA_D, "#040A1C", night)], a=a))
    for k in range(8):
        yy = 8 + k * 26
        p = skia.Path()
        p.moveTo(-2400, yy)
        xx = -2400.0
        while xx < 2400:
            xx += 36
            p.lineTo(xx, yy + math.sin(xx * 0.018 + t * (1.2 + k * 0.2) + k) * (2 + k * 0.6))
        c.drawPath(p, P(mix("#CFF6FF", "#7C93D8", night), (0.3 - k * 0.03) * a, stroke=2.5))
    if beam > 0 and beam_x is not None:                                    # the beam's light on the waves
        for k in range(26):
            rng = random.Random(k)
            bx = beam_x + rng.uniform(-260, 260) + math.sin(t * 2 + k) * 10
            by = rng.uniform(6, 120)
            gp = P("#FFE7A8", beam * a * (0.3 + 0.4 * abs(math.sin(t * 3 + k))))
            gp.setBlendMode(PLUS)
            c.drawRect(R(bx, by, 26 + by * 0.3, 3), gp)


def tier_poly(t_, inset=0.0):
    y0, y1, w0, w1 = t_
    return [(-w0 + inset, y0), (w0 - inset, y0), (w1 - inset, y1), (-w1 + inset, y1)]


def tower(c, t, built=1.0, lit=0.0, night=0.0, fire=0.0, mirror=0.0, beam=0.0, beam_ang=8.0, fall=0.0, a=1.0,
          dark=0.0, statue=1.0):
    """The lighthouse (world). built 0..1 shows it from the bottom up; night darkens the stone; dark 0..1 makes it
    a black shape; fire / mirror / beam light the top; fall 0..1 drops the tiers into the sea."""
    if a <= 0 or built <= 0:
        return
    hb = lerp(T1[0], TOP_Y, built)
    c.save()
    cp = skia.Path()
    cp.addRect(R(-400, hb - (40 if built >= 1 else 0), 800, 800))
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    tone = clamp(night * 0.75 + dark)
    cols = [mix(ST[0], "#1C1A2E", tone), mix(ST[1], "#151425", tone), mix(ST[2], "#0E0D1A", tone)]
    warm = lit * (1 - dark)
    for i, (tt, kind) in enumerate(((T1, "sq"), (T2, "oct"), (T3, "cyl"))):
        f = clamp(fall * 3 - (2 - i))                                     # the top falls first
        dx, dy, rot = f * (160 + i * 90), _ease_fall(f) * 900, f * (24 + i * 10)
        c.save()
        if f > 0:
            c.translate(dx, dy)
            c.rotate(rot)
        y0, y1, w0, w1 = tt
        if kind == "cyl":
            cyl(c, -w0, y1, w0 * 2, y0 - y1, cols[1], a=a)
        else:
            c.drawPath(path_of(tier_poly(tt), close=True), lin_paint(-w0, 0, w0, 0, [cols[0], cols[1], cols[2]], [0.0, 0.55, 1.0], a=a))
            if kind == "oct":                                             # the angled faces of the octagon
                for sd in (-1, 1):
                    c.drawPath(path_of([(sd * w0 * 0.55, y0), (sd * w0, y0), (sd * w1, y1), (sd * w1 * 0.55, y1)], close=True),
                               P(cols[2] if sd > 0 else cols[0], 0.6 * a))
            # courses of stone and slit windows
            n = int((y0 - y1) / 22)
            for k in range(1, n):
                yy = y0 - k * (y0 - y1) / n
                ww = lerp(w0, w1, k / n)
                c.drawLine(-ww, yy, ww, yy, P(mix("#B9A47E", "#08080F", tone), 0.35 * a, stroke=1.6))
            for k in range(2, n - 1, 3):
                yy = y0 - k * (y0 - y1) / n
                for wx in ((-0.4, 0.0, 0.4) if kind == "sq" else (0.0,)):
                    win = mix("#4A3A2A", "#FFC470", clamp(lit * 0.8 + night * 0.5) if lit > 0 else 0.0)
                    c.drawRect(R(wx * w0 - 4, yy - 12, 8, 16), P(win, 0.9 * a))
        # cornice at the top of each tier
        c.drawRect(R(-w1 - 8, y1 - 8, (w1 + 8) * 2, 10), P(mix(ST[0], "#24223A", tone), a))
        if kind == "sq":                                                  # small statues on the corners
            for sd in (-1, 1):
                c.drawRect(R(sd * (w1 + 2) - 6, y1 - 30, 12, 22), P(mix("#C8A15A", "#2A2640", tone), a))
                c.drawCircle(sd * (w1 + 2), y1 - 34, 6, P(mix("#C8A15A", "#2A2640", tone), a))
        if warm > 0:                                                      # firelight from above
            c.drawPath(path_of(tier_poly(tt), close=True), lin_paint(0, y1, 0, y0, [("#FFB347", 0.5 * warm), ("#FF8A3D", 0.0)], a=a))
        c.restore()
    # lantern, mirror, fire, statue (they fall with the top tier)
    f = clamp(fall * 3 - 2)
    c.save()
    if f > 0:
        c.translate(f * 340, _ease_fall(f) * 900)
        c.rotate(f * 50)
    ly0, ly1 = LANT
    for cx_ in (-24, -8, 8, 24):
        c.drawRect(R(cx_ - 3, ly1, 6, ly0 - ly1), P(mix(ST[1], "#1A1828", tone), a))
    c.drawRect(R(-32, ly1 - 6, 64, 8), P(mix(ST[0], "#24223A", tone), a))
    if mirror > 0:                                                         # the polished bronze dish beside the flames
        dish = skia.Path()
        dish.moveTo(-14, FIRE_Y - 40)
        dish.quadTo(-58, FIRE_Y - 2, -14, FIRE_Y + 36)
        dish.lineTo(-22, FIRE_Y + 36)
        dish.quadTo(-68, FIRE_Y - 2, -22, FIRE_Y - 40)
        dish.close()
        c.drawPath(dish, lin_paint(-60, FIRE_Y - 40, -14, FIRE_Y + 36, ["#FFF4C8", "#E8B04A", "#8A5A1E"], [0.0, 0.45, 1.0], a=mirror * a))
        c.drawPath(dish, P("#5A3A12", mirror * a, stroke=1.5))
        add_glow(c, -30, FIRE_Y - 10, 16, "#FFF4C8", 0.6 * mirror * a)
        for k in range(5):                                                 # rays: flame -> dish -> out to sea
            yy = FIRE_Y - 30 + k * 15
            dx_ = -36 + abs(k - 2) * 6
            rp = P("#FFE7A8", 0.55 * mirror * beam * a, stroke=1.6)
            rp.setBlendMode(PLUS)
            c.drawLine(2, FIRE_Y + 2, dx_, yy, rp)
            c.drawLine(dx_, yy, 90, yy, rp)
    if fire > 0:
        add_glow(c, 0, FIRE_Y, 60 + 70 * fire, "#FF8A3D", 0.6 * fire * a)
        v2.flame(c, 2, ly0 + 2, 20 * fire, 34 * fire, t, power=fire, seed=5, ang=-90)
        add_glow(c, 0, FIRE_Y + 4, 18, "#FFF4D6", 0.9 * fire * a)
    if beam > 0:                                                           # a cone of light out over the sea
        c.save()
        c.translate(0, FIRE_Y)
        c.rotate(beam_ang)
        bp = skia.Path()
        bp.moveTo(0, -8)
        bp.lineTo(1900, -190)
        bp.lineTo(1900, 190)
        bp.lineTo(0, 8)
        bp.close()
        pa = lin_paint(0, 0, 1900, 0, [("#FFE7A8", 0.55 * beam), ("#FFD58A", 0.18 * beam), ("#FFD58A", 0.0)], [0.0, 0.4, 1.0], a=a)
        pa.setBlendMode(PLUS)
        c.drawPath(bp, pa)
        c.restore()
    if statue > 0:
        sc = mix("#C8A15A", "#2A2640", tone)
        c.drawRect(R(-10, ly1 - 16, 20, 10), P(sc, a * statue))
        person(c, 0, ly1 - 16, 44, mix("#C8A15A", "#2A2640", tone), t, pose="point", face=1, skin=sc, pants=sc,
               hair=sc, a=a * statue)
    c.restore()
    c.restore()


def ruler(c, x, y0, y1, label, a=1.0, col="#FDE68A"):
    if a <= 0:
        return
    c.drawLine(x, y0, x, y1, P(col, a, stroke=4))
    for yy in (y0, y1):
        c.drawLine(x - 16, yy, x + 16, yy, P(col, a, stroke=4))
    n = 10
    for k in range(1, n):
        yy = lerp(y0, y1, k / n)
        c.drawLine(x - 8, yy, x + 8, yy, P(col, 0.7 * a, stroke=2))


def wood_pile(c, x, y, s, n, a=1.0):
    """A pile of logs (world), n = how many are left."""
    if a <= 0:
        return
    k = 0
    for row in range(4):
        for i in range(5 - row):
            if k >= n:
                return
            lx = x + (i - (4 - row) / 2) * 24 * s
            ly = y - row * 16 * s
            c.drawRRect(rr(lx - 13 * s, ly - 14 * s, 26 * s, 14 * s, 6 * s), P("#7C4A21", a))
            c.drawCircle(lx + 10 * s, ly - 7 * s, 5 * s, P("#C8955A", a))
            k += 1


def donkey_side(c, x, y, s, t, face=1, load=1.0, a=1.0):
    """A donkey with a bundle of wood on its back, side view, feet at y (world or screen)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    ph = t * 8 + x * 0.05
    body = "#8B7B69"
    for i, lx in enumerate((-22, -12, 16, 26)):
        sw = math.sin(ph + (i % 2) * math.pi) * 6
        c.drawLine(lx, -30, lx + sw, 0, P("#5E5246", a, stroke=6))
    c.drawRRect(rr(-30, -52, 64, 28, 13), P(body, a))
    c.drawLine(28, -44, 44, -66, P(body, a, stroke=12))
    c.drawOval(R(34, -78, 28, 16), P("#7A6C5A", a))
    c.drawLine(40, -74, 36, -96, P("#6B5E4E", a, stroke=6))
    c.drawLine(46, -74, 46, -96, P("#6B5E4E", a, stroke=6))
    c.drawCircle(52, -72, 2, P("#111111", a))
    c.drawLine(-30, -46, -38, -28, P("#5E5246", a, stroke=3))
    if load > 0:
        for k in range(3):
            c.drawRRect(rr(-26, -70 - k * 9, 52, 10, 5), P("#7C4A21", a * load))
            c.drawCircle(24, -65 - k * 9, 4, P("#C8955A", a * load))
    c.restore()


def scooter(c, x, y, s, t, a=1.0, face=1, box=True):
    """A delivery rider on a scooter (screen), wheels on y."""
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    for wx in (-70, 70):
        c.drawCircle(wx, -26, 26, P("#111827", a))
        c.drawCircle(wx, -26, 11, P("#9CA3AF", a))
    c.drawPath(path_of([(-96, -40), (40, -40), (74, -70), (88, -40), (96, -40), (60, -16), (-80, -16)], close=True), P("#F97316", a))
    c.drawLine(74, -70, 62, -150, P("#374151", a, stroke=8))
    c.drawLine(50, -150, 76, -150, P("#111827", a, stroke=8))
    if box:
        c.drawRRect(rr(-110, -140, 74, 70, 8), P("#22C55E", a))
        c.drawRect(R(-104, -120, 62, 8), P("#FFFFFF", 0.7 * a))
    c.restore()
    person(c, x - 6 * s * face, y - 40 * s, 150 * s, "#22C55E", t, pose="sit", face=face, hat="cap", a=a)


def phone_map(c, x, y, w, h, t, a=1.0, spin=1.0):
    """A phone showing a street map with a pin that keeps jumping (screen)."""
    if a <= 0:
        return
    c.drawRRect(rr(x - w / 2 - 10, y - h / 2 - 10, w + 20, h + 20, 30), P("#0F172A", a))
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, 22), P("#E5E7EB", a))
    c.save()
    cp = skia.Path()
    cp.addRRect(rr(x - w / 2, y - h / 2, w, h, 22))
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    for k in range(-4, 6):
        c.drawLine(x - w, y + k * 48, x + w, y + k * 48 + 30, P("#FFFFFF", a, stroke=12))
        c.drawLine(x + k * 52, y - h, x + k * 52 - 20, y + h, P("#FFFFFF", a, stroke=10))
    q = int(t * 2.2 * spin) % 4
    px = x + (-0.25, 0.2, -0.1, 0.28)[q] * w
    py = y + (-0.2, 0.1, 0.28, -0.05)[q] * h
    c.drawCircle(px, py - 18, 16, P("#EF4444", a))
    c.drawPath(path_of([(px - 12, py - 10), (px + 12, py - 10), (px, py + 10)], close=True), P("#EF4444", a))
    c.drawCircle(px, py - 18, 6, P("#FFFFFF", a))
    c.restore()


# ====================================================================================== the episode
class Pharos(EpisodeV2):
    BUILD_NO = 73
    FIRST_SET = "harbor"
    CLEAR = "#060A1E"
    TITLE = {"en": "LIGHTHOUSE OF ALEXANDRIA", "ar_sa": "منارة الإسكندرية"}
    EMPH = {"en": ["CONGRATS", "TOWER", "FIRE", "LIGHTHOUSE", "ALEXANDRIA", "YOURSELF", "SHIPS", "SINKING", "HIDDEN",
                   "ROCKS", "FAR", "STONE", "HUNDRED", "METERS", "THIRTY", "FLOOR", "NIGHT", "NOBODY", "BURNING", "TINY",
                   "SPARK", "MIRROR", "BRONZE", "WAVES", "WOOD", "RAMP", "INSIDE", "ANIMALS", "TOP", "FOLLOW",
                   "VANISHES", "FIFTY", "KILOMETERS", "EARTHQUAKES", "HARBOR", "SIXTEEN", "TWENTY", "TWO", "STONES",
                   "DELIVERY", "HOUSE"],
            "ar_sa": ["مبروك", "برج", "نار", "منارة", "الإسكندرية", "بيدك", "الصخور", "تغرّق", "السفن", "كيلو", "حجر",
                      "مية", "ثلاثين", "الليل", "محد", "تولّع", "شرارة", "مراية", "برونز", "الموج", "حطب", "طريق",
                      "داخل", "والحيوانات", "تابعني", "يختفي", "خمسين", "الزلازل", "البحر", "وستمية", "وعشرين",
                      "مندوب", "التوصيل", "بيتكم"]}
    KEYS = {"ar_sa": {
        ("hook", "FIRE"): "نار", ("hook", "TOWER"): "برج", ("hook", "CONGRATS"): "مبروك", ("hook", "LIGHTHOUSE"): "منارة",
        ("break1", "SHIPS"): "السفن", ("break1", "ROCKS"): "الصخور", ("break1", "SINKING"): "تغرّق", ("break1", "FAR"): "كيلو",
        ("fix1", "STACK"): "فتبني", ("fix1", "HUNDRED"): "مية", ("fix1", "THIRTY"): "ثلاثين",
        ("break2", "NIGHT"): "الليل", ("break2", "NOBODY"): "محد",
        ("fix2", "FIRE"): "نار", ("fix2", "EVERY"): "ليلة",
        ("break3", "FAR"): "بعيد", ("break3", "TINY"): "شرارة",
        ("fix3", "MIRROR"): "مراية", ("fix3", "BRONZE"): "برونز", ("fix3", "THROWS"): "ترمي", ("fix3", "WAVES"): "الموج",
        ("break4", "WOOD"): "حطب", ("break4", "HUNDRED"): "مية",
        ("fix4", "RAMP"): "طريق", ("fix4", "INSIDE"): "داخل", ("fix4", "ANIMALS"): "الحيوانات", ("fix4", "TOP"): "فوق",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "SAILORS"): "البحارة", ("reveal", "FIFTY"): "خمسين", ("reveal", "EARTHQUAKES"): "الزلازل",
        ("reveal", "HARBOR"): "البحر",
        ("stat", "HUNDRED"): "مية", ("stat", "SIXTEEN"): "وستمية", ("stat", "TWENTY"): "وعشرين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "GUIDED"): "دلّت", ("tag", "DELIVERY"): "مندوب", ("tag", "FIND"): "يتصل", ("tag", "HOUSE"): "بيتكم"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a hall that vanishes"),
                   "stat": [("100 m", "TALL"), ("1,600", "YEARS STANDING"), ("22", "STONES LIFTED")],
                   "L": {"name": "LIGHTHOUSE OF ALEXANDRIA", "fire": "A FIRE ON A GIANT TOWER", "rocks": "HIDDEN ROCKS",
                         "howfar": "SEEN FROM HOW FAR?", "hundred": "100 m", "floors": "= A 30-FLOOR BUILDING",
                         "tiers": "SQUARE, 8 SIDES, ROUND", "night": "INVISIBLE AT NIGHT", "fire2": "A FIRE ALL NIGHT",
                         "spark": "A TINY SPARK", "mirror": "POLISHED BRONZE MIRROR", "beam": "LIGHT OVER THE WAVES",
                         "wood": "LOADS OF WOOD", "up": "100 m UP", "ramp": "A RAMP INSIDE", "donkeys": "ANIMALS CARRY IT UP",
                         "fifty": "SEEN 50 km OUT", "quake": "EARTHQUAKES", "seabed": "STONES ON THE SEA FLOOR",
                         "lifted": "LIFTED IN 2025", "where": "WHERE'S YOUR HOUSE?", "centuries": "1,600 YEARS OF SHIPS"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: مبنى يختفي"),
                      "stat": [("100", "متر"), ("1600", "سنة واقفة"), ("22", "حجر طلّعوه")],
                      "L": {"name": "منارة الإسكندرية", "fire": "نار فوق برج عملاق", "rocks": "صخور مخفية",
                            "howfar": "من كم كيلو تبان؟", "hundred": "100 متر", "floors": "= عمارة 30 دور",
                            "tiers": "مربع، ثماني، دائري", "night": "ما يبان بالليل", "fire2": "نار طول الليل",
                            "spark": "شرارة صغيرة", "mirror": "مراية برونز", "beam": "نور فوق الموج",
                            "wood": "حطب كثير", "up": "فوق 100 متر", "ramp": "طريق يلف داخل البرج", "donkeys": "الحيوانات تطلّعه",
                            "fifty": "تبان من 50 كيلو", "quake": "زلازل", "seabed": "حجارتها في قاع البحر",
                            "lifted": "طلّعوها 2025", "where": "وين بيتكم بالضبط؟", "centuries": "1600 سنة تدل السفن"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "tower": ("hook", "TOWER", 0.3), "fire": ("hook", "FIRE", 0.45), "congrats": ("hook", "CONGRATS", 0.6),
            "name": ("hook", "LIGHTHOUSE", 0.85),
            "ships": ("break1", "SHIPS", 0.1), "sinking": ("break1", "SINKING", 0.2), "rocks": ("break1", "ROCKS", 0.4),
            "far": ("break1", "FAR", 0.75),
            "stack": ("fix1", "STACK", 0.1), "hundred": ("fix1", "HUNDRED", 0.45), "thirty": ("fix1", "THIRTY", 0.8),
            "night": ("break2", "NIGHT", 0.25), "nobody": ("break2", "NOBODY", 0.5),
            "fire2": ("fix2", "FIRE", 0.3), "every": ("fix2", "EVERY", 0.85),
            "far3": ("break3", "FAR", 0.15), "tiny": ("break3", "TINY", 0.75),
            "mirror": ("fix3", "MIRROR", 0.2), "bronze": ("fix3", "BRONZE", 0.4), "throws": ("fix3", "THROWS", 0.6),
            "waves": ("fix3", "WAVES", 0.9),
            "wood": ("break4", "WOOD", 0.3), "up4": ("break4", "HUNDRED", 0.8),
            "ramp": ("fix4", "RAMP", 0.15), "inside": ("fix4", "INSIDE", 0.35), "animals": ("fix4", "ANIMALS", 0.6),
            "top4": ("fix4", "TOP", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "sailors": ("reveal", "SAILORS", 0.1), "fifty": ("reveal", "FIFTY", 0.3), "quake": ("reveal", "EARTHQUAKES", 0.7),
            "harbor": ("reveal", "HARBOR", 0.92),
            "s1": ("stat", "HUNDRED", 0.05), "s2": ("stat", "SIXTEEN", 0.35), "s3": ("stat", "TWENTY", 0.65),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_guided": ("tag", "GUIDED", 0.05), "t_delivery": ("tag", "DELIVERY", 0.45), "t_find": ("tag", "FIND", 0.7),
            "t_house": ("tag", "HOUSE", 0.9)})
        T["sink1"] = max(T["sinking"], T["rocks"], T["ships"]) + 0.2
        T["thirty1"] = max(T["thirty"], T["hundred"]) + 0.2
        T["nobody1"] = max(T["nobody"], T["night"]) + 0.15
        T["fire21"] = T["fire2"] + 0.3
        T["tiny1"] = max(T["tiny"], T["far3"]) + 0.15
        T["waves1"] = max(T["waves"], T["throws"], T["mirror"]) + 0.2
        T["up41"] = max(T["up4"], T["wood"]) + 0.2
        T["top41"] = max(T["top4"], T["animals"]) + 0.2
        T["quake1"] = max(T["quake"], T["fifty"]) + 0.1
        # ---- sets
        self.cut(s("break3") - 0.12, "far", 1)
        self.cut(s("fix3") - 0.12, "harbor", -1)
        self.cut(s("break4") - 0.12, "ramp", 1)
        self.cut(s("reveal") - 0.12, "harbor", -1)
        self.cut(s("tag") - 0.2, "street", 1)
        # ---- harbor camera
        FULL = (0, -223, 1.4)
        cm = Camera(0, -610, 3.3)
        cm.key(0.05, 0, -600, 3.1, 1.0)
        cm.key(max(1.0, T["congrats"] - 0.8), *FULL, max(1.0, T["name"] - T["congrats"] + 0.9))
        cm.key(s("break1") - 0.12, 80, -150, 1.05, 0.0)                    # wide over the sea and the reefs
        cm.key(s("fix1") - 0.1, *FULL, 1.0)
        cm.key(s("break2") - 0.12, 120, -200, 1.15, 0.0)
        cm.key(s("fix2") + 0.1, 0, -330, 1.55, 1.2)
        cm.key(s("fix3") - 0.12, 30, -598, 3.4, 0.0)                         # close on the lantern
        cm.key(T["throws"] - 0.1, 420, -420, 1.05, 1.6)                      # out along the beam
        cm.key(s("reveal") - 0.12, 900, -300, 0.42, 0.0)                     # wide: the tower and a ship far out
        cm.key(T["quake"] - 0.4, 200, -330, 0.9, 1.0)
        cm.key(s("stat") - 0.12, 120, 520, 1.1, 0.0)                         # under the water
        cm.key(s("closer") - 0.12, 0, -240, 1.22, 0.0)
        cm.key(s("closer") + 0.1, 0, -250, 1.3, 1.4)
        self.cam = cm
        self.spans = [(T["sink1"], T["thirty1"] + 0.3), (T["nobody1"], T["fire21"] + 0.4), (T["tiny1"], T["waves1"] + 0.3),
                      (T["up41"], T["top41"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["sink1"], 0.4, 8), (T["thirty1"], 0.35, 6), (T["fire21"], 0.35, 6),
                       (T["waves1"], 0.35, 6), (T["quake"], 1.4, 18), (s("closer") + 0.2, 0.35, 8), (T["t_house"], 0.3, 6)]

    # ------------------------------------------------------------------ set: harbor
    def phase(self, t):
        s, T = self.tl.s, self.T
        if t < s("break1") - 0.12:
            return "hook"
        if t < s("fix1") - 0.12:
            return "break1"
        if t < s("break2") - 0.12:
            return "fix1"
        if t < s("fix2") - 0.12:
            return "break2"
        if t < s("break3") - 0.12:
            return "fix2"
        if t < s("break4") - 0.12:
            return "fix3"
        if t < s("stat") - 0.12:
            return "reveal"
        if t < s("closer") - 0.12:
            return "stat"
        return "closer"

    def draw_harbor(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        ph = self.phase(t)
        gy = self.to_screen(cam, 0, -22)[1]
        night = 1.0
        if ph == "break1" or ph == "fix1":
            night = 0.0
        elif ph == "break2":
            night = prog(t, s("break2") - 0.1, T["night"] + 0.3)
        elif ph == "reveal":
            night = 0.55
        if ph in ("break1", "fix1"):
            v2.sky(c, W, H, 0.0, pal=DAYP, horizon_y=gy)
            sun(c, 860, gy - 520, 40, heat=0.35)
        elif ph == "break2" and night < 1:
            v2.sky(c, W, H, 0.0, pal=DUSKP, horizon_y=gy)
            c.saveLayerAlpha(None, int(255 * night))
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy)
            c.restore()
        elif ph == "reveal":
            v2.sky(c, W, H, 0.0, pal=DUSKP, horizon_y=gy)
            v2.stars(c, W, H, t, 0.4)
        else:
            v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=gy)
            v2.stars(c, W, H, t, 0.9 * night)
            v2.moon(c, 860, max(200, gy - 900), 46, a=0.85 * night)
        self.view(c, cam)
        shore(c, t, night=night)
        # beam direction sweeps slowly
        beam_ang = 6 + 5 * math.sin(t * 0.6)
        fire = mirror = beam = 0.0
        built, fall, dark, lit = 1.0, 0.0, 0.0, 0.0
        if ph == "hook":
            fire, mirror, beam, lit = 1.0, 1.0, prog(t, T["fire"] - 0.3, T["fire"] + 0.4), 1.0
        elif ph == "break1":
            built = 0.0
        elif ph == "fix1":
            built = e_io(prog(t, T["stack"] - 0.2, T["thirty"] + 0.2))
        elif ph == "break2":
            dark = prog(t, T["night"] - 0.2, T["nobody"] + 0.2)
        elif ph == "fix2":
            fire = e_out(prog(t, T["fire2"] - 0.2, T["fire2"] + 0.5))
            lit = fire
            dark = 1 - fire
        elif ph == "fix3":
            fire, lit = 1.0, 1.0
            mirror = prog(t, T["mirror"] - 0.3, T["mirror"] + 0.2)
            beam = prog(t, T["throws"] - 0.3, T["throws"] + 0.4)
        elif ph == "reveal":
            fire, mirror, lit = 1.0, 1.0, 0.7
            beam = 1 - prog(t, T["quake"], T["quake"] + 0.5)
            fall = e_in(prog(t, T["quake"] + 0.2, T["harbor"] + 0.9))
            beam_ang = 2.0
        elif ph == "stat":
            built = 0.0
        else:
            fire, mirror, beam, lit = 1.0, 1.0, 1.0, 1.0
        bx = None
        if beam > 0:
            bx = 900 + 600 * math.cos(math.radians(beam_ang))
        water(c, t, night=night, beam=beam, beam_x=bx)
        xray = prog(t, T["rocks"] - 0.3, T["rocks"] + 0.2) if ph == "break1" else (0.6 if ph == "break2" else 0.0)
        rocks_under(c, t, xray=xray)
        island(c, t, night=night)
        if ph == "fix1":
            ruler(c, 190, T1[0], TOP_Y, "", a=prog(t, T["hundred"] - 0.3, T["hundred"]))
            building_ghost(c, 240, 170, -TOP_Y, 30, prog(t, T["thirty"] - 0.4, T["thirty"]))
        tower(c, t, built=built, lit=lit, night=night, fire=fire, mirror=mirror, beam=beam, beam_ang=beam_ang, fall=fall,
              dark=dark)
        # ships
        if ph == "hook":
            galley(c, lerp(900, 520, prog(t, 0, s("break1"))), 0, 1.25, t, lamp=1.0, face=-1)
        elif ph == "break1":
            u = prog(t, s("break1") - 0.1, T["sink1"])
            hit = prog(t, T["sink1"] - 0.15, T["sink1"] + 1.4)
            galley(c, lerp(640, 360, u), 0, 1.3, t, tilt=-24 * hit, sink=hit, face=-1)
            if hit > 0:
                splash(c, 360, 0, t, T["sink1"] - 0.1, dur=0.9, n=18, speed=380)
        elif ph == "break2":
            u = prog(t, s("break2"), s("fix2"))
            galley(c, lerp(900, 600, u), 0, 1.25, t, face=-1, lamp=night)
        elif ph == "fix2":
            u = prog(t, s("fix2"), s("break3"))
            galley(c, lerp(620, 900, u), 0, 1.25, t, face=1, lamp=1.0)
        elif ph == "fix3":
            galley(c, 1500, 0, 1.6, t, face=-1, lamp=1.0)
        elif ph == "reveal":
            galley(c, 1900, 0, 2.4, t, face=-1, lamp=1.0)
            if fall > 0:
                for k in range(3):
                    splash(c, 180 + k * 120, 0, t, T["quake"] + 0.5 + k * 0.25, dur=1.2, n=24, speed=520)
        elif ph == "closer":
            galley(c, -520, 0, 1.2, t, face=1, lamp=1.0)
            galley(c, 640, 0, 1.0, t, face=-1, lamp=1.0)
        if ph == "stat":
            self.seabed(c, t)
        c.restore()
        self.ui["cam"] = cam

    def seabed(self, c, t):
        """Under the water: the fallen blocks on the sea floor, one lifted on a crane cable (world, y > 0)."""
        T = self.T
        c.drawRect(R(-3000, 4, 6000, 1400), lin_paint(0, 0, 0, 900, ["#0F4F6E", "#06233A"], a=1.0))
        for k in range(10):                                                # light rays from the surface
            x = -500 + k * 130 + math.sin(t * 0.7 + k) * 20
            pa = lin_paint(x, 0, x, 700, [("#BDE6FF", 0.18), ("#BDE6FF", 0.0)])
            pa.setBlendMode(PLUS)
            c.drawPath(path_of([(x - 20, 0), (x + 20, 0), (x + 90, 700), (x + 30, 700)], close=True), pa)
        c.drawPath(path_of([(-2000, 640), (-600, 600), (-200, 620), (300, 590), (900, 630), (2000, 610), (2000, 1400), (-2000, 1400)],
                           close=True), P("#3A3A2E"))
        rng = random.Random(7)
        blocks = []
        for k in range(22):
            bx = rng.uniform(-420, 640)
            by = rng.uniform(560, 640)
            bw, bh = rng.uniform(70, 150), rng.uniform(36, 60)
            blocks.append((bx, by, bw, bh, rng.uniform(-25, 25)))
        lift = prog(t, T["s3"] - 0.2, T["s3"] + 1.8)
        for i, (bx, by, bw, bh, rot) in enumerate(blocks):
            yy = by
            if i == 7:
                yy = lerp(by, -40, e_io(lift))
            c.save()
            c.translate(bx, yy)
            c.rotate(rot * (1 - (lift if i == 7 else 0)))
            c.drawRRect(rr(-bw / 2, -bh / 2, bw, bh, 6), lin_paint(-bw / 2, 0, bw / 2, 0, ["#C9B98E", "#8C7A55"]))
            c.drawRRect(rr(-bw / 2, -bh / 2, bw, bh, 6), P("#2F4F3A", 0.35, stroke=6))
            c.restore()
        bx7 = blocks[7][0]
        y7 = lerp(blocks[7][1], -40, e_io(lift))
        c.drawLine(bx7, -400, bx7, y7 - 24, P("#E5E7EB", 0.9, stroke=3))
        c.drawRect(R(bx7 - 180, -60, 360, 50), P("#334155"))                 # the crane barge on the surface
        c.drawLine(bx7 - 120, -60, bx7, -400, P("#F59E0B", 1.0, stroke=10))
        c.drawRect(R(-3000, -2, 6000, 6), P("#BDE6FF", 0.5))
        for k in range(8):                                                 # a few fish
            fx_ = (t * 40 + k * 260) % 1600 - 600
            fy = 200 + k * 40
            c.drawOval(R(fx_, fy, 26, 10), P("#93C5FD", 0.6))
        self.ui["lift_x"] = bx7

    def ui_harbor(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        cam = self.ui.get("cam", self.cam.at(tw))
        if ph == "hook":
            self.chip(540, 300, "fire", T["tower"] - 0.2, T["congrats"] - 0.15, accent="#FDBA74", size=44)
            self.chip(540, 300, "name", T["congrats"] - 0.15, s("break1") + 0.1, accent=HILITE, size=46)
            return
        if ph == "break1":
            x, y = self.to_screen(cam, ROCKS[1][0], ROCKS[1][1])
            self.label(x, y, 540, 760, "rocks", T["rocks"] - 0.2, T["far"] - 0.1, accent=WARN)
            self.chip(540, 300, "howfar", T["far"] - 0.2, s("fix1") - 0.15, accent=HILITE, size=46)
            self.badge("alert", T["sink1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["sink1"], 1.2)
            return
        if ph == "fix1":
            self.chip(540, 300, "tiers", T["stack"] - 0.1, T["hundred"] - 0.2, accent="#CBD5E1", size=40)
            self.chip(540, 300, "hundred", T["hundred"] - 0.2, T["thirty"] - 0.2, accent=HILITE, size=54)
            self.chip(540, 300, "floors", T["thirty"] - 0.2, s("break2") - 0.15, accent="#93C5FD", size=44)
            self.badge("check", T["thirty1"] + 0.1, s("break2") - 0.15, x=920, y=440)
            return
        if ph == "break2":
            self.chip(540, 300, "night", T["night"] - 0.1, s("fix2") - 0.15, accent="#94A3B8", size=48)
            self.badge("alert", T["nobody1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["nobody1"], 1.2)
            return
        if ph == "fix2":
            self.chip(540, 300, "fire2", T["fire2"] - 0.1, s("break3") - 0.15, accent="#FDBA74", size=50)
            self.badge("check", T["fire21"] + 0.1, s("break3") - 0.15, x=920, y=440)
            return
        if ph == "fix3":
            x, y = self.to_screen(cam, -8, FIRE_Y)
            self.label(x, y, 540, 560 if y > 700 else 1080, "mirror", T["mirror"] - 0.1, T["throws"] + 0.2, accent=HILITE)
            self.chip(540, 300, "beam", T["throws"], s("cta") - 0.15, accent="#FDE68A", size=46)
            self.badge("check", T["waves1"] + 0.1, s("break4") - 0.15, x=920, y=440)
            return
        if ph == "reveal":
            self.chip(540, 300, "fifty", T["sailors"] - 0.1, T["quake"] - 0.1, accent=HILITE, size=50)
            self.chip(540, 300, "quake", T["quake"] - 0.1, s("stat") - 0.15, accent=WARN, size=50)
            k = self.span(T["fifty"] - 0.2, T["quake"] - 0.1)
            if k > 0:
                x0, y0 = self.to_screen(cam, 60, -720)
                x1, _ = self.to_screen(cam, 1900, -720)
                dashed(c, x0, y0, x1, y0, "#FDE68A", w=5, dash=20, gap=12, phase=tw * 40, a=k)
                for xx in (x0, x1):
                    c.drawLine(xx, y0 - 16, xx, y0 + 16, P("#FDE68A", k, stroke=5))
            return
        if ph == "stat":
            self.chip(540, 640, "seabed", s("stat") + 0.1, T["s3"] - 0.1, accent="#7DD3FC", size=40)
            self.chip(540, 640, "lifted", T["s3"] - 0.1, s("closer") - 0.15, accent=HILITE, size=44)
            return

    # ------------------------------------------------------------------ set: far (break3, the first half of fix3)
    def draw_far(self, c, t):
        T, s = self.T, self.tl.s
        hy = 980
        v2.sky(c, W, H, 0.0, pal=NIGHTP, horizon_y=hy)
        v2.stars(c, W, H, t, 0.9)
        v2.moon(c, 220, 330, 40, a=0.8)
        vrect(c, 0, hy, W, H - hy, ["#132554", "#050A1C"])
        for k in range(10):
            yy = hy + 12 + k * k * 9
            c.drawLine(0, yy, W, yy + math.sin(t + k) * 4, P("#7C93D8", 0.25 - k * 0.02, stroke=2 + k * 0.4))
        sx, sy = 720, hy - 8
        tw_ = 0.6 + 0.4 * math.sin(t * 9)
        add_glow(c, sx, sy, 22, "#FFB347", 0.9 * tw_)
        c.drawCircle(sx, sy, 4.0, P("#FFF1C9", 0.95))
        rk = (t * 0.8) % 1.0
        c.drawCircle(sx, sy, 10 + 50 * rk, P("#FDE68A", 0.6 * (1 - rk), stroke=3))
        zk = prog(t, T["tiny"] - 0.3, T["tiny"] + 0.3)
        if zk > 0:                                                          # a magnifier on the spark
            mx, my, mr = 720, 700, 150
            c.drawCircle(mx, my, mr, P("#0B1433", 0.9 * zk))
            add_glow(c, mx, my + 40, 26, "#FFB347", 0.9 * zk * tw_)
            c.drawCircle(mx, my + 40, 6, P("#FFF1C9", zk))
            c.drawCircle(mx, my, mr, P("#E5E7EB", zk, stroke=10))
            c.drawLine(mx + mr * 0.7, my + mr * 0.7, mx + mr * 1.15, my + mr * 1.15, P("#E5E7EB", zk, stroke=18))
            c.drawLine(sx, sy, mx, my + mr, P("#E5E7EB", 0.4 * zk, stroke=3))
        # the ship's bow and a sailor squinting, in front
        c.save()
        c.translate(0, math.sin(t * 1.4) * 8)
        c.drawPath(path_of([(-40, 1500), (380, 1180), (560, 1150), (520, 1260), (300, 1500)], close=True),
                   lin_paint(0, 1150, 0, 1500, ["#8A5A32", "#3A2210"]))
        c.drawLine(380, 1180, 640, 1000, P("#3A2414", 1.0, stroke=10))
        person(c, 250, 1250, 300, "#1D4ED8", t, pose="look", face=1, hat="beanie")
        c.drawLine(262, 1250 - 270, 330, 1250 - 268, P("#E8B48A", 1.0, stroke=16))  # hand over the eyes
        c.restore()

    def ui_far(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "spark", T["tiny"] - 0.25, s("fix3") - 0.15, accent=WARN, size=50)
        self.badge("alert", T["tiny1"], s("fix3") - 0.2, x=920, y=440)
        self.red(T["tiny1"], 1.2)

    # ------------------------------------------------------------------ set: ramp (break4, fix4, cta)
    def draw_ramp(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0A1030", "#1A1640"])
        v2.stars(c, W, H, t, 0.6)
        fixed = t >= s("fix4") - 0.12
        cam = (0, -223, 1.4)
        self.view(c, cam)
        # the tower cut open: walls, central core, the ramp zigzagging up
        y0, y1, w0, w1 = T1
        c.drawPath(path_of(tier_poly(T1), close=True), P("#3B2F28"))
        c.drawPath(path_of(tier_poly(T1), close=True), P("#8A7A62", 1.0, stroke=10))
        for sd in (-1, 1):
            c.drawPath(path_of([(sd * w0, y0), (sd * (w0 - 14), y0), (sd * (w1 - 14), y1), (sd * w1, y1)], close=True), P("#B8A27C"))
        c.drawRect(R(-12, y1, 24, y0 - y1), P("#5B4A3C"))                 # the core
        n = 6
        pts = []
        for k in range(n + 1):
            yy = lerp(y0 - 8, y1 + 20, k / n)
            ww = lerp(w0, w1, k / n) - 18
            pts.append((-ww if k % 2 == 0 else ww, yy))
        rk = prog(t, T["ramp"] - 0.3, T["inside"] + 0.4) if fixed else 0.0
        if rk > 0:
            rp = path_of(pts)
            pm = skia.PathMeasure(rp, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * rk, seg, True)
            c.drawPath(seg, P("#C9A46A", 1.0, stroke=16))
            c.drawPath(seg, P("#8A6A3E", 1.0, stroke=3))
        # upper tiers and the lantern on top, in the night's colours
        NST = "#6E6A86"
        c.drawPath(path_of(tier_poly(T2), close=True), lin_paint(-50, 0, 50, 0, ["#8A85A3", NST, "#45405E"]))
        cyl(c, -T3[2], T3[1], T3[2] * 2, T3[0] - T3[1], NST)
        for cx_ in (-24, -8, 8, 24):
            c.drawRect(R(cx_ - 3, LANT[1], 6, LANT[0] - LANT[1]), P(NST))
        c.drawRect(R(-32, LANT[1] - 6, 64, 8), P("#8A85A3"))
        # the fire: weak before, strong once the wood arrives
        need = prog(t, T["wood"] - 0.3, T["up41"]) if not fixed else 1.0
        fk = (1 - 0.75 * need) if not fixed else lerp(0.25, 1.0, prog(t, T["animals"], T["top41"] + 0.4))
        add_glow(c, 0, FIRE_Y, 40 + 60 * fk, "#FF8A3D", 0.6 * fk)
        v2.flame(c, 2, LANT[0] + 2, 20 * fk, 34 * fk, t, power=max(0.05, fk), seed=5, ang=-90)
        # the wood: a pile at the bottom; before the fix the pile is up top and shrinks
        if not fixed:
            left = int(lerp(14, 2, prog(t, T["wood"], T["up41"] + 0.8)))
            wood_pile(c, 0, LANT[0] + 4, 0.55, left)
            c.drawLine(110, y0, 110, TOP_Y, P("#FDE68A", prog(t, T["up4"] - 0.3, T["up4"]), stroke=4))
            wood_pile(c, -180, -32, 1.0, 14)
            c.drawRect(R(-600, -30, 1200, 60), P("#6B5236"))
        else:
            c.drawRect(R(-600, -30, 1200, 60), P("#6B5236"))
            wood_pile(c, -200, -32, 1.0, 14)
            # donkeys walk the ramp
            if rk > 0.2:
                rp = path_of(pts)
                pm = skia.PathMeasure(rp, False)
                L = pm.getLength()
                for i in range(4):
                    u = (prog(t, T["inside"], s("cta") + 0.6) * 1.2 + i * 0.22) % 1.0
                    if u * L > L * rk:
                        continue
                    pos, tan = pm.getPosTan(u * L)
                    face = 1 if tan.x() > 0 else -1
                    donkey_side(c, pos.x(), pos.y() + 6, 0.55, t, face=face, load=1.0 if u < 0.95 else 0.0)
            wood_pile(c, 0, LANT[0] + 4, 0.55, int(lerp(2, 12, prog(t, T["animals"], T["top41"] + 0.6))))
        c.restore()
        self.ui["cam"] = cam

    def ui_ramp(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "wood", T["wood"] - 0.2, T["up4"] - 0.1, accent=WARN, size=50)
            self.chip(540, 300, "up", T["up4"] - 0.1, s("fix4") - 0.15, accent=HILITE, size=50)
            self.badge("alert", T["up41"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["up41"], 1.2)
            return
        self.chip(540, 300, "ramp", T["ramp"] - 0.2, T["animals"] - 0.2, accent="#FDE68A", size=46)
        self.chip(540, 300, "donkeys", T["animals"] - 0.2, s("cta") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["top41"] + 0.1, s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: street (tag)
    def draw_street(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B1030", "#1E1B4B", "#312E81"])
        v2.stars(c, W, H, t, 0.5)
        gy = 1180
        for i in range(5):                                                   # identical houses
            x = -120 + i * 300
            c.drawRect(R(x, gy - 430, 260, 430), lin_paint(x, 0, x + 260, 0, ["#5E5478", "#4A4264"]))
            c.drawRect(R(x, gy - 430, 260, 16), P("#7A6F96"))
            c.drawRect(R(x + 100, gy - 170, 60, 170), P("#3B2516"))
            c.drawCircle(x + 148, gy - 86, 4, P("#FDE68A"))
            for wx in (x + 30, x + 180):
                c.drawRect(R(wx, gy - 360, 50, 60), P("#FFD58A", 0.75))
            c.drawRect(R(x + 20, gy - 250, 220, 10), P("#9CA3AF"))          # the balcony rail
        c.drawRect(R(0, gy, W, H - gy), P("#374151"))
        dashed(c, 0, gy + 90, W, gy + 90, "#F8FAFC", w=6, dash=50, gap=40, a=0.6)
        # you on the balcony, waving the phone torch like a lighthouse
        bx, by = 790, gy - 250
        person(c, bx, by, 150, "#2563EB", t, pose="point", face=-1)
        ang = 200 + 25 * math.sin(t * 3.2)
        tk = prog(t, T["t_guided"], T["t_guided"] + 0.5)
        if tk > 0:
            light_cone(c, bx - 30, by - 120, ang, 700, 18, a=0.4 * tk)
            add_glow(c, bx - 30, by - 120, 24, "#FFFFFF", 0.9 * tk)
        # the rider circles the street, looking at his phone
        u = prog(t, s("tag") - 0.1, self.duration)
        rx = 540 + math.sin(u * 6.5) * 330
        face = 1 if math.cos(u * 6.5) > 0 else -1
        scooter(c, rx, gy + 40, 1.35, t, face=face)
        self.ui["rx"] = rx

    def ui_street(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "centuries", T["t_guided"] - 0.1, T["t_delivery"] - 0.1, accent=HILITE, size=44)
        pk = self.span(T["t_delivery"] - 0.2, self.duration + 1)
        if pk > 0:
            phone_map(c, 300, 640, 260, 440, tw, a=pk)
        self.chip(620, 440, "where", T["t_find"] - 0.2, self.duration + 1, accent=WARN, size=46)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#060A1E", "#141A3A"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["fire"] - 0.1, sfx.hiss(1.0, 62), -16),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(T["sink1"] - 0.1, sfx.clank(220.0, 0.6, 66), -6), (T["sink1"], sfx.thud(0.6, 67), -6),
               (T["sink1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        for k in range(6):
            ev.append((lerp(T["stack"], T["thirty"], k / 5), sfx.thunk(68 + k), -10))
        ev += [(T["thirty1"], sfx.ding(), -8), (T["thirty1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["night"] - 0.2, sfx.power_down(1.0, 75), -12), (T["nobody1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["fire2"] - 0.1, sfx.whoosh(0.6, True, 76), -8), (T["fire2"], sfx.hiss(1.4, 77), -12),
               (T["fire21"], sfx.ding(), -8), (T["fire21"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 78), -6), (T["tiny1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, False, 79), -6), (T["mirror"], sfx.sparkle(1.0, 12, 80), -8),
               (T["throws"], sfx.riser(0.8, 81), -12), (T["waves1"], sfx.ding(), -8), (T["waves1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 82), -6), (T["wood"], sfx.sizzle(1.0, 83), -14),
               (T["up41"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["ramp"], sfx.whoosh(0.5, False, 84), -10)]
        for k in range(5):
            ev.append((lerp(T["animals"], T["top41"] + 0.6, k / 4), sfx.tap(85 + k), -12))
        ev += [(T["top41"], sfx.ding(), -8), (T["top41"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(90), 0), (T["follow"] - 0.15, sfx.pop(91), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 92), -6), (T["fifty"], sfx.sparkle(0.9, 10, 93), -10),
               (T["quake"], v2set.rumble(2.0, 94), -6), (T["quake"] + 0.8, sfx.thud(0.8, 95), -4),
               (T["quake"] + 1.1, sfx.hiss(1.2, 96), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 97), -6), (T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3),
               (T["s3"], sfx.pop(100), -3), (T["s3"] + 0.3, sfx.whirr(1.4, 120.0, 200.0, 101), -16)]
        ev += [(T["cong2"], sfx.pop(102), -2), (T["cong2"], sfx.sparkle(1.4, 18, 103), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 104), -6), (T["t_delivery"], sfx.beep(900.0, 0.1), -12),
               (T["t_find"], sfx.ring(1.0), -14), (T["t_house"] + 0.3, sfx.womp(), -8)]
        return ev


NAME = "pharos"
EPISODE = Pharos
