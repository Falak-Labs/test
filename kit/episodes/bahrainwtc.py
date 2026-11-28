"""Episode 110 - The Bahrain World Trade Center in Manama (Atkins, 2008).  v2 look.

Sets: towers (hook: close on one spinning rotor, out to the two sail-shaped towers on the shore of the Gulf with three
wind turbines hung on bridges between them; cta, stat; closer at dusk with the towers lit), plan (break1: seen from
above, the turbine is bolted in place and cannot turn; fix1: it faces north into the sea breeze; break2: a side wind
hits the blades at a slant and they slow down; fix2: the sail-shaped towers bend the wind into an S and aim it straight
at the blades), front (break3: in strong winds the two towers sway by different amounts and yank on the bridges; fix3:
rubber bearings at the bridge ends let them move half a meter; break4: the wind is stronger up high and the top rotor
races; fix4: the towers narrow as they rise and all three spin the same), study (reveal: turned the other way round
they would make fourteen percent more), tag (dad switching off the one light left on while three turbines spin outside).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

GLASSC = ("#5E8FB0", "#3F6E90", "#2B5270")             # mid-tone glass (light blue blooms white)
STEELC = ("#94A3B8", "#64748B")
SEA = ("#1F5F7A", "#174A61", "#0F3346")
SKIN = ("#C68E62", "#A8754E", "#E8B48A", "#8D5A3B")
WINDC, GOODC, BADC = "#7DD3FC", "#4ADE80", "#F87171"

BASE_Y, TOP_Y = 1150, 450                              # the towers in the front view
GX0, GX1 = 452, 628                                     # the gap between the inner edges
BRIDGES = (620, 800, 980)                              # bridge heights, top to bottom
ROTOR_R = 80


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=10, head=22):
    if a <= 0:
        return
    c.drawLine(x0, y0, x1, y1, P(col, a, stroke=w))
    ang = math.atan2(y1 - y0, x1 - x0)
    poly(c, [(x1, y1), (x1 - head * math.cos(ang - 0.5), y1 - head * math.sin(ang - 0.5)),
             (x1 - head * math.cos(ang + 0.5), y1 - head * math.sin(ang + 0.5))], col, a)


def rotor(c, x, y, r, ang, a=1.0, col="#E2E8F0", hub="#475569", tint=None):
    """A three-bladed rotor seen from the front."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#FFFFFF", 0.06 * a))
    for b in range(3):
        th = ang + b * 2.0944
        p = skia.Path()
        p.moveTo(x + math.cos(th - 0.18) * 8, y + math.sin(th - 0.18) * 8)
        p.lineTo(x + math.cos(th - 0.05) * r, y + math.sin(th - 0.05) * r)
        p.lineTo(x + math.cos(th + 0.06) * r * 0.98, y + math.sin(th + 0.06) * r * 0.98)
        p.lineTo(x + math.cos(th + 0.25) * 10, y + math.sin(th + 0.25) * 10)
        p.close()
        c.drawPath(p, P(tint or col, a))
        c.drawPath(p, P("#334155", 0.8 * a, stroke=2))
    c.drawCircle(x, y, 11, P(hub, a))
    c.drawCircle(x, y, 5, P("#CBD5E1", a))


def tower_edges(y, taper=1.0, side=-1):
    """x of the outer and inner edge of one tower at height y (side -1 left, 1 right). taper 0: straight sides."""
    u = clamp((BASE_Y - y) / (BASE_Y - TOP_Y))
    inner = GX0 if side < 0 else GX1
    w = lerp(300, lerp(300, 95, u ** 1.15), taper) * (1 - 0.15 * u * (1 - taper))
    outer = inner - w if side < 0 else inner + w
    return outer, inner


def tower(c, side, t, taper=1.0, sway=0.0, lit=0.0, a=1.0, dusk=0.0):
    """One sail-shaped tower in front view. sway: top offset in pixels (grows with height)."""
    n = 40
    outer, inner = [], []
    for k in range(n + 1):
        y = lerp(BASE_Y, TOP_Y, k / n)
        u = k / n
        o, i = tower_edges(y, taper, side)
        dx = sway * u * u
        bulge = 26 * math.sin(math.pi * u) * taper
        outer.append((o + dx + (-bulge if side < 0 else bulge), y))
        inner.append((i + dx, y))
    p = skia.Path()
    p.moveTo(*outer[0])
    for pt in outer[1:]:
        p.lineTo(*pt)
    ix = inner[-1][0]
    p.quadTo((outer[-1][0] + ix) / 2, TOP_Y - 20, ix, TOP_Y - 70)       # the sail's pointed crown, on the gap side
    for pt in reversed(inner):
        p.lineTo(*pt)
    p.close()
    left = sorted((outer[0], inner[0]))
    g0, g1, g2 = (mix(GLASSC[0], "#2A2550", dusk), mix(GLASSC[1], "#1E1B40", dusk), mix(GLASSC[2], "#15132E", dusk))
    c.drawPath(p, lin_paint(left[0][0], 0, left[1][0], 0, [g2, g0, g1] if side < 0 else [g1, g0, g2], a=a))
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    for k in range(44):                                # floors
        y = BASE_Y - 12 - k * 15.5
        c.drawLine(0, y, W, y, P("#1D3B52", 0.55 * a, stroke=2))
    if lit > 0:
        rng = random.Random(3 + side)
        for k in range(160):
            y = BASE_Y - 20 - rng.uniform(0, 640)
            o, i = tower_edges(y, taper, side)
            x = rng.uniform(min(o, i) + 10, max(o, i) - 10) + sway * ((BASE_Y - y) / (BASE_Y - TOP_Y)) ** 2
            c.drawRect(R(x, y, 14, 6), P("#FFD38A", 0.75 * lit * a))
    sx = GX0 - 120 if side < 0 else GX1 + 40                       # a soft vertical sheen on the glass
    c.drawRect(R(sx, TOP_Y - 80, 80, 900), P("#FFFFFF", 0.06 * a))
    c.restore()
    return p


def gap_x(y, sway_l=0.0, sway_r=0.0):
    u = clamp((BASE_Y - y) / (BASE_Y - TOP_Y))
    return GX0 + sway_l * u * u, GX1 + sway_r * u * u


def bridges(c, t, spins=(1.0, 1.0, 1.0), sway_l=0.0, sway_r=0.0, strain=0.0, bearings=0.0, tints=(None, None, None), a=1.0):
    for k, y in enumerate(BRIDGES):
        x0, x1 = gap_x(y, sway_l, sway_r)
        c.drawRect(R(x0, y - 9, x1 - x0, 18), P(STEELC[1], a))                  # the sky bridge behind the rotor
        for q in range(6):
            qx = lerp(x0, x1, q / 5)
            c.drawLine(qx, y - 9, qx + (x1 - x0) / 10, y + 9, P("#CBD5E1", 0.7 * a, stroke=2))
        c.drawLine(x0, y - 9, x1, y - 9, P("#CBD5E1", a, stroke=3))
        rotor(c, (x0 + x1) / 2, y, ROTOR_R - 4, t * 6.0 * spins[k] + k, a=a, tint=tints[k])
        if strain > 0:
            for ex in (x0, x1):
                add_glow(c, ex, y, 34, BADC, 0.8 * strain * (0.6 + 0.4 * math.sin(t * 20 + k)))
        if bearings > 0:
            for ex in (x0 + 2, x1 - 18):
                squash = 3 * math.sin(t * 5 + k)
                c.drawRRect(rr(ex, y - 12 + squash, 16, 24 - squash, 5), P("#111827", bearings * a))
                c.drawRRect(rr(ex + 3, y - 9 + squash, 10, 18 - squash, 4), P(GOODC, 0.9 * bearings * a))


def sky(c, dusk=0.0, dawn=0.0):
    top = mix(mix("#3A6EA5", "#F5A07A", dawn * 0.3), "#1A1D48", dusk)
    mid = mix(mix("#7FAED6", "#F4B88E", dawn), "#5E3C70", dusk)
    low = mix(mix("#E9C9A0", "#FFCF96", dawn), "#E58652", dusk)
    vrect(c, 0, 0, W, H, [top, mid, low, low], [0.0, 0.42, 0.62, 1.0])
    if dusk > 0.5:
        v2.stars(c, W, H, 0, 0.6 * dusk)


def sea_front(c, t, dusk=0.0):
    c.drawRect(R(0, BASE_Y, W, 100), lin_paint(0, BASE_Y, 0, 1250, [mix(SEA[0], "#2B2A55", dusk), SEA[2]]))
    for k in range(16):
        x = (k * 97 + t * 30) % (W + 120) - 60
        c.drawLine(x, BASE_Y + 30 + (k % 4) * 16, x + 50, BASE_Y + 30 + (k % 4) * 16, P("#9FD3E6", 0.35, stroke=3))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#0E2A3A", "#071018"]))


def city_low(c, dusk=0.0):
    rng = random.Random(8)
    x = -20
    while x < W:
        w = rng.uniform(50, 110)
        h = rng.uniform(40, 150)
        c.drawRect(R(x, BASE_Y - h, w, h), P(mix("#8B95A6", "#2A2D4A", dusk), 0.9))
        x += w + rng.uniform(4, 20)


def towers_scene(c, t, dusk=0.0, lit=0.0, spin=1.0, dawn=0.0):
    sky(c, dusk, dawn)
    if dusk < 1:
        add_glow(c, 170, 520, 180, "#FFE6A8", 0.5 * (1 - dusk))
        c.drawCircle(170, 520, 48, P("#FFF3D1", 1 - dusk))
    city_low(c, dusk)
    tower(c, -1, t, lit=lit, dusk=dusk)
    tower(c, 1, t, lit=lit, dusk=dusk)
    bridges(c, t, spins=(spin, spin, spin))
    sea_front(c, t, dusk)


# ====================================================================================== plan view (break1 .. fix2)
PCX, PCY = 540, 790


def foot(c, side, a=1.0, rot=0.0):
    """One tower's footprint from above: a sail/airfoil shape, flat side to the gap."""
    c.save()
    c.translate(PCX, PCY)
    c.rotate(rot)
    p = skia.Path()                                    # rounded front to the north (the sea), pointed tail to the south
    sg = -1 if side < 0 else 1
    p.moveTo(sg * 62, -190)
    p.cubicTo(sg * 330, -240, sg * 260, 90, sg * 84, 250)
    p.cubicTo(sg * 64, 130, sg * 56, -60, sg * 62, -190)
    p.close()
    c.drawPath(p, lin_paint(sg * 300, 0, sg * 60, 0, [GLASSC[2], GLASSC[0]], a=a))
    c.drawPath(p, P("#CBD5E1", 0.8 * a, stroke=4))
    c.restore()


def plan(c, t, lock=0.0, wind_ang=0.0, bend=0.0, spin=1.0, rot=0.0, tint=None, sea=1.0):
    vrect(c, 0, 0, W, H, ["#0F2533", "#163447"])
    c.drawRect(R(0, 300, W, 260), lin_paint(0, 300, 0, 560, [SEA[0], "#163447"], a=sea))            # the Gulf to the north
    for k in range(12):
        x = (k * 97 + t * 25) % (W + 120) - 60
        c.drawLine(x, 330 + (k % 3) * 60, x + 50, 330 + (k % 3) * 60, P("#9FD3E6", 0.3 * sea, stroke=3))
    c.drawCircle(940, 660, 46, P("#0B1620", 0.9))                     # compass
    poly(c, [(940, 622), (928, 664), (952, 664)], "#F87171")
    text(c, "N", 940, 612, 34, "#F8FAFC")
    # wind streamlines
    for k in range(7):
        xs = PCX + (k - 3) * 70
        pts = []
        for j in range(31):
            u = j / 30
            y = lerp(360, 1220, u)
            x = xs + math.tan(wind_ang) * (y - PCY)
            if bend > 0:                                # the towers squeeze and straighten the flow through the gap
                g = math.exp(-((y - PCY) / 210) ** 2)
                x = lerp(x, PCX + (k - 3) * 14, g * bend)
            pts.append((x, y))
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, dash_paint(WINDC, 0.55, 4, t * 60, 22, 16))
        u = (t * 0.5 + k / 7) % 1.0
        i = int(u * 29)
        arrow(c, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], WINDC, 0.9, 6, 14)
    foot(c, -1, rot=rot)
    foot(c, 1, rot=rot)
    # the turbine across the gap, seen from above: a blur of blades and a hub
    c.save()
    c.translate(PCX, PCY)
    c.rotate(rot)
    blur = 0.5 + 0.5 * math.sin(t * 30 * spin)
    c.drawRect(R(-58, -6, 116, 12), P(tint or "#E2E8F0", 0.5 + 0.4 * blur))
    c.drawRRect(rr(-14, -18, 28, 46, 8), P("#475569"))
    if lock > 0:
        c.drawRRect(rr(-26, 34, 52, 40, 8), P("#F59E0B", lock))
        c.drawArc(R(-18, 12, 36, 40), 180, 180, False, P("#F59E0B", lock, stroke=7))
    c.restore()
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#163447", "#071018"]))


# ====================================================================================== front close (break3 .. fix4)
def front(c, t, sway=0.0, strain=0.0, bearings=0.0, taper=1.0, wind=0.0, spins=(1.0, 1.0, 1.0), tints=(None, None, None)):
    sky(c, 0.15)
    city_low(c, 0.15)
    sl = sway * math.sin(t * 3.1) * 36
    sr = sway * math.sin(t * 3.1 + 1.9) * 22
    tower(c, -1, t, taper=taper, sway=sl)
    tower(c, 1, t, taper=taper, sway=sr)
    bridges(c, t, spins=spins, sway_l=sl, sway_r=sr, strain=strain, bearings=bearings, tints=tints)
    if wind > 0:                                       # wind arrows from the left, longer up high
        for k, y in enumerate((560, 720, 880, 1040)):
            ln = lerp(220, 90, k / 3) if taper < 0.5 else 150
            u = (t * 0.8 + k * 0.23) % 1.0
            x0 = 40 + 30 * u
            arrow(c, x0, y, x0 + ln, y, WINDC, wind * (0.4 + 0.6 * math.sin(math.pi * u)), 9, 20)
    sea_front(c, t)


# ====================================================================================== tag
def dad_tag(c, t, point=0.0, off=0.0):
    vrect(c, 0, 0, W, H, ["#3B3245", "#2A2433"])
    c.drawRRect(rr(560, 380, 420, 420, 16), P("#0E1A2B"))                   # a window with the towers outside
    c.save()
    c.clipRRect(rr(570, 390, 400, 400, 12), skia.ClipOp.kIntersect, True)
    c.translate(570, 390)
    c.scale(0.38, 0.38)
    c.translate(-60, -330)
    towers_scene(c, t, dusk=1.0, lit=1.0)
    c.restore()
    c.drawRect(R(0, 1000, W, 250), P("#5B4A3C"))
    lamp = 1 - off
    c.drawLine(300, 300, 300, 420, P("#1F2937", stroke=4))                  # the ceiling light left on
    c.drawCircle(300, 450, 34, P(mix("#FFE9A8", "#4B5563", off)))
    if lamp > 0:
        add_glow(c, 300, 450, 220, "#FFE29A", 0.45 * lamp)
    c.drawRRect(rr(160, 700, 36, 56, 6), P("#E5E7EB"))                      # the switch
    c.drawRect(R(172, 712 + 18 * off, 12, 14), P("#9CA3AF"))
    person(c, 320, 1180, 430, "#2563EB", t, pose="point" if point > 0 else "stand", face=-1, skin=SKIN[0],
           hair="#3F3F46")                                                 # dad
    person(c, 820, 1180, 300, "#F59E0B", t + 1, pose="shrug", face=-1, skin=SKIN[1], hair="#141414")


class BahrainWTC(EpisodeV2):
    BUILD_NO = 110
    FIRST_SET = "towers"
    CLEAR = "#071018"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "BAHRAIN WTC", "ar_sa": "مركز البحرين التجاري"}
    EMPH = {"en": ["TOWERS", "BAHRAIN", "THREE", "GIANT", "WIND", "TURBINES", "BOLTED", "WHICH", "WAY", "NORTH", "SEA",
                   "BREEZE", "GULF", "SIDE", "SLANT", "SAIL-SHAPED", "BEND", "STRAIGHT", "BLADES", "STRONG", "WINDS",
                   "SWAY", "YANK", "BRIDGES", "RUBBER", "BEARINGS", "HALF", "METER", "STRONGER", "HIGH", "TOP", "RACE",
                   "NARROW", "RISE", "SAME", "FOLLOW", "LOCK", "KEY", "STUDY", "OTHER", "ROUND", "FOURTEEN", "PERCENT",
                   "THOUSAND", "EIGHT", "TWENTY-NINE", "METERS", "BUSES", "CONGRATS", "YOURSELF", "DAD", "LIGHT"],
            "ar_sa": ["برجين", "البحرين", "مراوح", "عملاقة", "مثبتة", "ما", "تلف", "وين", "للشمال", "نسمة", "البحر",
                      "الخليج", "الجنب", "بالعرض", "الشراع", "يلوون", "عدل", "الهبة", "يتمايلون", "يشدون", "الجسور",
                      "وسايد", "مطاط", "نص", "متر", "أقوى", "فوق", "تطير", "يضعفون", "السرعة", "متابعة", "قفل",
                      "الجواب", "بالعكس", "أربعتعش", "بالمية", "وثمانية", "متر", "باصين", "مبروك", "وأبوك", "الأنوار",
                      "ببلاش"]}
    KEYS = {"ar_sa": {
        ("hook", "TOWERS"): "برجين", ("hook", "BAHRAIN"): "البحرين", ("hook", "THREE"): "ثلاث", ("hook", "TURBINES"): "مراوح",
        ("break1", "BOLTED"): "مثبتة", ("break1", "WHICH"): "وين",
        ("fix1", "NORTH"): "للشمال", ("fix1", "BREEZE"): "نسمة", ("fix1", "GULF"): "الخليج",
        ("break2", "SIDE"): "الجنب", ("break2", "SLANT"): "بالعرض",
        ("fix2", "SAIL"): "الشراع", ("fix2", "BEND"): "يلوون", ("fix2", "STRAIGHT"): "عدل",
        ("break3", "STRONG"): "الهبة", ("break3", "SWAY"): "يتمايلون", ("break3", "YANK"): "يشدون",
        ("fix3", "RUBBER"): "مطاط", ("fix3", "HALF"): "نص",
        ("break4", "STRONGER"): "أقوى", ("break4", "RACE"): "طيران",
        ("fix4", "NARROW"): "يضعفون", ("fix4", "SAME"): "السرعة",
        ("cta", "FOLLOW"): "متابعة", ("cta", "LOCK"): "قفل",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "STUDY"): "دراسة", ("reveal", "OTHER"): "بالعكس",
        ("reveal", "FOURTEEN"): "أربعتعش",
        ("stat", "TWO"): "ألفين", ("stat", "TWENTY"): "وعشرين", ("stat", "BUSES"): "باصين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "THREE"): "ثلاث", ("tag", "DAD"): "وأبوك", ("tag", "LIGHT"): "الأنوار"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a lock only your key opens"),
                   "stat": [("2008", "FIRST SPIN"), ("29 M", "EACH ROTOR"), ("2+", "BUSES WIDE")],
                   "L": {"three": "3 WIND TURBINES!", "bolted": "BOLTED IN PLACE", "which": "WHICH WAY TO FACE?",
                         "north": "NORTH, INTO THE SEA BREEZE", "side": "SIDE WIND = SLANTED HIT", "bend": "THE TOWERS BEND THE WIND",
                         "straight": "STRAIGHT AT THE BLADES", "sway": "THE TOWERS SWAY", "yank": "YANKING THE BRIDGES",
                         "bearings": "RUBBER BEARINGS", "half": "0.5 M OF MOVE", "race": "THE TOP ONE RACES!",
                         "narrow": "NARROWER AS THEY RISE", "same": "ALL THREE THE SAME", "other": "THE OTHER WAY ROUND?",
                         "plus": "+14% MORE", "name": "THE BAHRAIN WORLD TRADE CENTER", "light": "ONE LIGHT LEFT ON!",
                         "free": "WIND POWER, FREE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قفل ما يفتحه إلا مفتاحك"),
                      "stat": [("2008", "أول لفّة"), ("29", "متر عرض المروحة"), ("2+", "أطول من باصين")],
                      "L": {"three": "ثلاث مراوح هوا!", "bolted": "مثبّتة مكانها", "which": "وين توجّهها؟",
                            "north": "للشمال على نسمة البحر", "side": "هوا من الجنب = ضربة بالعرض", "bend": "البرجين يلوون الهوا",
                            "straight": "على الريش عدل", "sway": "البرجين يتمايلون", "yank": "يشدّون الجسور",
                            "bearings": "وسايد مطاط", "half": "نص متر حركة", "race": "اللي فوق تطير!",
                            "narrow": "يضعفون كل ما ارتفعوا", "same": "الثلاث بنفس السرعة", "other": "لو كانوا بالعكس؟",
                            "plus": "+14% زيادة", "name": "مركز البحرين التجاري العالمي", "light": "الكهربا مو ببلاش!",
                            "free": "كهربا من الهوا"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "towers": ("hook", "TOWERS", 0.15), "bahrain": ("hook", "BAHRAIN", 0.35), "three": ("hook", "THREE", 0.65),
            "turbines": ("hook", "TURBINES", 0.9),
            "bolted": ("break1", "BOLTED", 0.4), "which": ("break1", "WHICH", 0.75),
            "north": ("fix1", "NORTH", 0.25), "breeze": ("fix1", "BREEZE", 0.7), "gulf": ("fix1", "GULF", 0.95),
            "side": ("break2", "SIDE", 0.3), "slant": ("break2", "SLANT", 0.9),
            "sail": ("fix2", "SAIL", 0.2), "bend": ("fix2", "BEND", 0.45), "straight": ("fix2", "STRAIGHT", 0.8),
            "strong": ("break3", "STRONG", 0.15), "sway": ("break3", "SWAY", 0.5), "yank": ("break3", "YANK", 0.8),
            "rubber": ("fix3", "RUBBER", 0.15), "half": ("fix3", "HALF", 0.8),
            "stronger": ("break4", "STRONGER", 0.3), "race": ("break4", "RACE", 0.95),
            "narrow": ("fix4", "NARROW", 0.3), "same": ("fix4", "SAME", 0.95),
            "follow": ("cta", "FOLLOW", 0.1), "lock": ("cta", "LOCK", 0.6),
            "answer": ("reveal", "ANSWER", 0.05), "study": ("reveal", "STUDY", 0.25), "other": ("reveal", "OTHER", 0.55),
            "fourteen": ("reveal", "FOURTEEN", 0.8),
            "s1": ("stat", "TWO", 0.05), "s2": ("stat", "TWENTY", 0.5), "s3": ("stat", "BUSES", 0.9),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_three": ("tag", "THREE", 0.1), "t_dad": ("tag", "DAD", 0.6), "t_light": ("tag", "LIGHT", 0.85)})
        T["bolted1"] = max(T["bolted"], s("break1") + 0.3)
        T["breeze1"] = max(T["breeze"], T["north"] + 0.3)
        T["slant1"] = max(T["slant"], T["side"] + 0.3)
        T["straight1"] = max(T["straight"], T["bend"] + 0.3)
        T["sway1"] = max(T["sway"], s("break3") + 0.3)
        T["half1"] = max(T["half"], T["rubber"] + 0.3)
        T["race1"] = max(T["race"], T["stronger"] + 0.3)
        T["same1"] = max(T["same"], T["narrow"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "plan", 1)
        self.cut(s("break3") - 0.12, "front", -1)
        self.cut(s("cta") - 0.12, "towers", 1)
        self.cut(s("reveal") - 0.12, "study", -1)
        self.cut(s("stat") - 0.12, "towers", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["bolted1"], T["breeze1"]), (T["slant1"], T["straight1"]), (T["sway1"], T["half1"]),
                      (T["race1"], T["same1"])]
        self.shakes = [(T["three"], 0.3, 4), (T["bolted1"], 0.3, 5), (T["slant1"], 0.3, 6), (T["sway1"], 0.5, 7),
                       (T["race1"], 0.3, 6), (T["fourteen"], 0.3, 5), (s("closer") + 0.2, 0.35, 6), (T["t_light"], 0.3, 5)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: towers (hook, cta, stat, closer)
    def draw_towers(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["three"] - 0.5, s("break1") - 0.2))
            z = lerp(3.0, 1.0, k)
            fx, fy = lerp(540, 540, k), lerp(BRIDGES[1], 800, k)
            c.save()
            c.translate(540, 760)
            c.scale(z, z)
            c.translate(-fx, -fy)
            towers_scene(c, t, dawn=0.45)
            c.restore()
            c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#0E2A3A", "#071018"]))
        elif ph == "closer":
            towers_scene(c, t, dusk=1.0, lit=1.0)
        else:
            towers_scene(c, t, dusk=0.0 if ph == "stat" else 0.3, lit=0.0 if ph == "stat" else 0.3)

    def ui_towers(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "three", T["three"] - 0.2, s("break1") + 0.1, accent=HILITE, size=60)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=44)

    # ------------------------------------------------------------------ set: plan (break1 .. fix2)
    def draw_plan(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break1":
            plan(c, t, lock=prog(t, T["bolted"] - 0.2, T["bolted"] + 0.2), wind_ang=0.5 * math.sin(t * 0.9), spin=0.5)
        elif ph == "fix1":
            plan(c, t, lock=1.0, wind_ang=lerp(0.4, 0.0, prog(t, s("fix1"), T["north"] + 0.4)), spin=1.0)
        elif ph == "break2":
            ang = lerp(0.0, 0.62, prog(t, s("break2"), T["slant1"]))
            plan(c, t, lock=1.0, wind_ang=ang, spin=lerp(1.0, 0.25, prog(t, T["side"], T["slant1"])),
                 tint=BADC if t >= T["slant1"] else None)
        else:
            plan(c, t, lock=1.0, wind_ang=0.62, bend=prog(t, T["bend"] - 0.3, T["straight"]),
                 spin=lerp(0.25, 1.2, prog(t, T["bend"], T["straight1"])), tint=GOODC if t >= T["straight1"] else None)

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "bolted", T["bolted"] - 0.2, T["which"] - 0.2, accent=WARN, size=58)
            self.chip(540, 300, "which", T["which"] - 0.2, s("fix1") - 0.1, accent=HILITE, size=58)
            self.badge("alert", T["bolted1"], s("fix1") - 0.2, x=160, y=470)
            self.red(T["bolted1"], 1.2)
        elif ph == "fix1":
            self.chip(540, 300, "north", T["north"] - 0.2, s("break2") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["breeze1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "side", T["side"] - 0.2, s("fix2") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["slant1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["slant1"], 1.2)
        else:
            self.chip(540, 300, "bend", T["sail"] - 0.2, T["straight"] - 0.3, accent=WINDC, size=50)
            self.chip(540, 300, "straight", T["straight"] - 0.3, s("break3") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["straight1"], s("break3") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: front (break3 .. fix4)
    def draw_front(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break3":
            sw = prog(t, T["strong"] - 0.2, T["sway1"])
            front(c, t, sway=sw, strain=prog(t, T["yank"] - 0.3, T["yank"]), wind=sw)
        elif ph == "fix3":
            front(c, t, sway=1.0, strain=1 - prog(t, T["rubber"], T["half1"]), bearings=prog(t, T["rubber"] - 0.2, T["rubber"] + 0.2),
                  wind=1.0)
        elif ph == "break4":
            k = prog(t, s("break4"), T["race1"])
            front(c, t, sway=0.3, bearings=1.0, taper=lerp(1.0, 0.0, prog(t, s("break4") - 0.1, s("break4") + 0.4)), wind=1.0,
                  spins=(lerp(1.0, 2.6, k), 1.0, lerp(1.0, 0.45, k)), tints=(BADC if k >= 1 else None, None, None))
        else:
            k = prog(t, T["narrow"] - 0.2, T["same1"])
            front(c, t, sway=0.3, bearings=1.0, taper=k, wind=1.0, spins=(lerp(2.6, 1.0, k), 1.0, lerp(0.45, 1.0, k)),
                  tints=(GOODC, GOODC, GOODC) if t >= T["same1"] else (None, None, None))
        c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#0E2A3A", "#071018"]))
        if ph in ("fix3",):                            # a close-up of one bearing
            a = prog(t, T["rubber"] - 0.1, T["rubber"] + 0.3)
            if a > 0:
                c.drawCircle(860, 560, 130, P("#0B1620", 0.92 * a))
                c.save()
                cp = skia.Path()
                cp.addCircle(860, 560, 124)
                c.clipPath(cp, skia.ClipOp.kIntersect, True)
                c.drawRect(R(736, 520, 70, 80), P(GLASSC[1], a))
                sq = 10 * math.sin(t * 5)
                c.drawRRect(rr(806 + sq * 0.3, 534, 46 - sq * 0.3, 52, 10), P("#111827", a))
                c.drawRRect(rr(812 + sq * 0.3, 540, 34 - sq * 0.3, 40, 8), P(GOODC, a))
                c.drawRect(R(852, 548, 140, 24), P(STEELC[1], a))
                c.restore()
                c.drawCircle(860, 560, 124, P("#E2E8F0", a, stroke=8))

    def ui_front(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "sway", T["strong"] - 0.2, T["yank"] - 0.2, accent=WARN, size=58)
            self.chip(540, 300, "yank", T["yank"] - 0.2, s("fix3") - 0.15, accent=WARN, size=54)
            self.badge("alert", T["sway1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["sway1"], 1.2)
        elif ph == "fix3":
            self.chip(540, 300, "bearings", T["rubber"] - 0.2, T["half"] - 0.2, accent=GOOD, size=58)
            self.chip(540, 300, "half", T["half"] - 0.2, s("break4") - 0.15, accent=GOOD, size=58)
            self.badge("check", T["half1"], s("break4") - 0.15, x=160, y=470)
        elif ph == "break4":
            self.chip(540, 300, "race", T["stronger"] - 0.2, s("fix4") - 0.15, accent=WARN, size=58)
            self.badge("alert", T["race1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["race1"], 1.2)
        else:
            self.chip(540, 300, "narrow", T["narrow"] - 0.2, T["same"] - 0.2, accent=WINDC, size=52)
            self.chip(540, 300, "same", T["same"] - 0.2, s("cta") - 0.15, accent=GOOD, size=56)
            self.badge("check", T["same1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: study (reveal)
    def draw_study(self, c, t):
        T, s = self.T, self.tl.s
        k = e_io(prog(t, T["other"] - 0.3, T["other"] + 0.7))
        plan(c, t, wind_ang=0.0, bend=1.0, spin=lerp(1.0, 1.5, k), rot=180 * k, sea=1.0)
        g = prog(t, T["fourteen"] - 0.2, T["fourteen"] + 0.3)
        if g > 0:                                      # a power meter
            c.drawRRect(rr(120, 1040, 840, 60, 30), P("#0B1620", 0.9 * g))
            c.drawRRect(rr(128, 1048, 824 * lerp(0.0, 0.88, e_out(g)), 44, 22), P(GOODC, g))
            c.drawLine(128 + 824 * 0.77, 1036, 128 + 824 * 0.77, 1104, P("#F8FAFC", g, stroke=6))

    def ui_study(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "other", T["study"] - 0.2, T["fourteen"] - 0.2, accent=HILITE, size=56)
        self.chip(540, 300, "plus", T["fourteen"] - 0.2, s("stat") - 0.15, accent=GOOD, size=64)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        dad_tag(c, t, point=prog(t, T["t_dad"] - 0.2, T["t_dad"]), off=prog(t, T["t_light"], T["t_light"] + 0.3))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "free", T["t_three"] - 0.2, T["t_dad"] - 0.2, accent=WINDC, size=56)
        self.chip(540, 300, "light", T["t_dad"] - 0.2, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0F2533", "#163447"])

    def draw_cover(self, c):
        """As the base, but the English name drops its "THE": "THE BAHRAIN WORLD TRADE CENTER" fits in no two lines
        (cover._fit then falls back to one line that runs off the frame), "BAHRAIN WORLD TRADE CENTER" fits in two."""
        from bik import cover
        self.draw_world(c, self.cover_time())
        closer = next((ln["text"] for ln in self.tl.lines if ln["label"] == "closer"), "")
        small, name = cover.subject(self.lang, closer, self.TITLE.get(self.lang, self.TITLE["en"]))
        if not self.rtl and name.startswith("THE "):
            name = name[4:]
        return cover.overlay(c, W, H, self.BUILD_NO, self.lang, small, name)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.whirr(3.0, 90.0, 120.0, 60), -18),
              (T["three"], sfx.riser(0.8, 62), -12), (T["turbines"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["bolted1"], sfx.clank(380.0, 0.6, 64), -8),
               (T["bolted1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(T["north"], sfx.whoosh(0.8, False, 65), -12), (T["breeze1"], sfx.ding(), -8), (T["breeze1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["side"], sfx.whoosh(0.6, True, 66), -10), (T["slant1"], sfx.thunk(67), -8), (T["slant1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["bend"], sfx.whirr(1.4, 160.0, 260.0, 68), -12), (T["straight1"], sfx.ding(), -8),
               (T["straight1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, False, 69), -6), (T["sway1"], sfx.creak(1.0, 70), -8),
               (T["yank"], sfx.clank(300.0, 0.7, 71), -8), (T["sway1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["rubber"], sfx.thud(0.4, 72), -10), (T["half1"], sfx.ding(), -8), (T["half1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["stronger"], sfx.whirr(1.2, 220.0, 420.0, 73), -12), (T["race1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["narrow"], sfx.riser(0.8, 74), -12), (T["same1"], sfx.sparkle(1.0, 10, 75), -8), (T["same1"], sfx.ding(), -8),
               (T["same1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["other"], sfx.whoosh(0.8, False, 95), -10),
               (T["fourteen"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_dad"], sfx.pop(104), -8), (T["t_light"], sfx.click(105), -4),
               (T["t_light"] + 0.2, sfx.womp(), -8)]
        return ev


NAME = "bahrainwtc"
EPISODE = BahrainWTC
