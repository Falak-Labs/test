"""Episode 98 - the Rain Vortex at Jewel Changi Airport, Singapore.  v2 look.

Sets: inside (hook: the waterfall pouring through the hole of a glass dome into a clear drum, terraced forest, a little
train gliding through; break1: the same with a question mark where a river would be; stat, closer: night, the light
show on the water), roof (fix1: the doughnut-shaped glass roof from above in the rain, the hole off centre), section
(break2-fix4, cta, reveal: a cutaway of the dome, the floors, the pit and the tanks under it; world: x -560..560, roof
top y -600, ground floor y 300, pool y 380, tanks y 440-560), sink (tag: a kitchen tap on full over a spoon).
"""
from v2_base import *  # noqa: F401,F403

OX = 70.0                                # the oculus centre (section, world): a little off centre
ROOF_Y, FLOOR_Y, POOL_Y = -560.0, 300.0, 390.0
WATER = ("#E0F7FF", "#7DD3FC", "#38BDF8")
LEAF = ("#166534", "#15803D", "#22C55E", "#4ADE80")
DAYP = ["#0C4A6E", "#0E7490", "#67E8F9"]
NIGHT2 = ["#030712", "#0B1430", "#1E1B4B"]


def hue_col(h):
    """A light-show colour from a hue 0..1."""
    cols = ["#F472B6", "#A78BFA", "#60A5FA", "#22D3EE", "#34D399", "#FACC15", "#FB923C", "#F472B6"]
    h = h % 1.0 * (len(cols) - 1)
    i = int(h)
    return mix(cols[i], cols[i + 1], h - i)


# ------------------------------------------------------------------ the inside view (screen space)
def dome_inside(c, t, night=0.0):
    """The glass dome seen from inside: sky through triangular panes, ribs converging on the oculus."""
    vrect(c, 0, 0, W, H, [mix(a, b, night) for a, b in zip(DAYP, NIGHT2)])
    ox, oy = 580, 330
    for i in range(-12, 13):                              # ribs from the edge of the frame to the oculus
        ang = math.radians(90 + i * 8.5)
        x1, y1 = ox + math.cos(ang) * 1500, oy + math.sin(ang) * 900
        c.drawLine(ox + math.cos(ang) * 110, oy + math.sin(ang) * 34, x1, y1, P(mix("#CFFAFE", "#334155", night), 0.45, stroke=4))
    for k in range(1, 9):                                 # rings, closer together near the oculus
        rx, ry = 110 + k * k * 22, 34 + k * k * 13
        c.drawOval(R(ox - rx, oy - ry, 2 * rx, 2 * ry), P(mix("#CFFAFE", "#334155", night), 0.35, stroke=3))
    rng = random.Random(5)
    for k in range(60):                                   # cross bracing: the triangles
        a1 = rng.uniform(math.pi * 0.05, math.pi * 0.95)
        r1 = rng.uniform(1.5, 7.5)
        rx, ry = 110 + r1 * r1 * 22, 34 + r1 * r1 * 13
        x0_, y0_ = ox + math.cos(a1) * rx, oy + math.sin(a1) * ry
        rx2, ry2 = 110 + (r1 + 1) ** 2 * 22, 34 + (r1 + 1) ** 2 * 13
        x2_, y2_ = ox + math.cos(a1 + 0.12) * rx2, oy + math.sin(a1 + 0.12) * ry2
        c.drawLine(x0_, y0_, x2_, y2_, P(mix("#CFFAFE", "#334155", night), 0.25, stroke=2))
    c.drawOval(R(ox - 112, oy - 36, 224, 72), P(mix("#F0FDFF", "#94A3B8", night)))   # the oculus: sky
    c.drawOval(R(ox - 112, oy - 36, 224, 72), P("#E2E8F0", 0.9, stroke=6))
    if night < 0.5:
        add_glow(c, ox, oy, 220, "#E0F2FE", 0.5 * (1 - night))


def falling_water(c, t, x0, y0, x1, y1, w0, w1, a=1.0, night=0.0, bend=0.0):
    """A curtain of water from (x0, y0) w0 wide down to (x1, y1) w1 wide (screen), with moving streaks. bend > 0 bows
    the sides inward like a funnel."""
    if a <= 0:
        return
    path = skia.Path()
    path.moveTo(x0 - w0 / 2, y0)
    path.cubicTo(x0 - w0 / 2 + bend * 40, lerp(y0, y1, 0.45), x1 - w1 / 2 - bend * 10, lerp(y0, y1, 0.8), x1 - w1 / 2, y1)
    path.lineTo(x1 + w1 / 2, y1)
    path.cubicTo(x1 + w1 / 2 + bend * 10, lerp(y0, y1, 0.8), x0 + w0 / 2 - bend * 40, lerp(y0, y1, 0.45), x0 + w0 / 2, y0)
    path.close()
    if night > 0:
        h = t * 0.15
        c.drawPath(path, lin_paint(0, y0, 0, y1, [hue_col(h), hue_col(h + 0.25), hue_col(h + 0.5)], a=0.85 * a * night))
    c.drawPath(path, lin_paint(x0 - w0 / 2, 0, x0 + w0 / 2, 0, [WATER[2], WATER[0], WATER[1], WATER[0], WATER[2]],
                               a=0.85 * a * (1 - 0.6 * night)))
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    rng = random.Random(8)
    for k in range(46):                                   # streaks running down
        u = rng.random()
        x = lerp(x0 - w0 / 2, x0 + w0 / 2, u)
        xb = lerp(x1 - w1 / 2, x1 + w1 / 2, u)
        ph = (t * rng.uniform(1.4, 2.2) + rng.random()) % 1.0
        ya = lerp(y0, y1, ph)
        c.drawLine(lerp(x, xb, ph), ya, lerp(x, xb, ph + 0.08), ya + (y1 - y0) * 0.08, P("#FFFFFF", 0.55 * a, stroke=4))
    c.restore()


def drum(c, x, y_top, y_bot, w, a=1.0, fill=1.0):
    """The clear acrylic drum (screen or world)."""
    if a <= 0:
        return
    h = (y_bot - y_top) * fill
    yt = y_bot - h
    c.drawRect(R(x - w / 2, yt, w, h), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#BAE6FD", "#E0F2FE", "#7DD3FC", "#E0F2FE"], a=0.28 * a))
    c.drawOval(R(x - w / 2, yt - w * 0.12, w, w * 0.24), P("#E0F2FE", 0.85 * a, stroke=5))
    c.drawLine(x - w / 2, yt, x - w / 2, y_bot, P("#E0F2FE", 0.8 * a, stroke=5))
    c.drawLine(x + w / 2, yt, x + w / 2, y_bot, P("#E0F2FE", 0.8 * a, stroke=5))
    c.drawLine(x - w * 0.32, yt + 10, x - w * 0.32, y_bot - 10, P("#FFFFFF", 0.4 * a, stroke=8))


def terraces(c, t, side, night=0.0):
    """Terraced forest on one side of the valley (screen): side -1 left, 1 right."""
    rng = random.Random(10 + side)
    for row in range(6):
        y = 760 + row * 80
        x_in = 540 + side * (170 + row * 10)
        x_out = 540 + side * 700
        lo, hi = min(x_in, x_out), max(x_in, x_out)
        c.drawRect(R(lo, y + 40, hi - lo, 46), P(mix("#57534E", "#1C1917", night)))          # the terrace edge
        for k in range(9):
            x = lerp(x_in, x_out, (k + rng.random() * 0.6) / 9)
            r_ = rng.uniform(34, 56) * (1 - row * 0.05)
            col = mix(LEAF[rng.randrange(4)], "#052E16", night * 0.6)
            c.drawCircle(x, y + 30, r_, P(col))
            c.drawCircle(x - r_ * 0.3, y + 30 - r_ * 0.35, r_ * 0.45, P(mix("#86EFAC", "#14532D", night), 0.4))
    for k in range(3):                                    # a few tall palms at the back
        x = 540 + side * (330 + k * 120)
        y = 760
        c.drawLine(x, y, x + side * 10, y - 260, P("#78350F", 1.0, stroke=12))
        for j in range(6):
            ang = math.radians(-160 + j * 28)
            c.drawLine(x + side * 10, y - 260, x + side * 10 + math.cos(ang) * 90, y - 260 + math.sin(ang) * 50 + 20,
                       P(mix("#16A34A", "#052E16", night * 0.6), 1.0, stroke=14))


def sky_train(c, t, y, a=1.0):
    """A small airport train gliding across behind the waterfall (screen)."""
    x = (t * 120) % (W + 900) - 450
    for k in range(3):
        bx = x + k * 150
        c.drawRRect(rr(bx, y, 140, 56, 18), P("#F8FAFC", a))
        for j in range(4):
            c.drawRRect(rr(bx + 14 + j * 30, y + 12, 22, 20, 5), P("#1D4ED8", 0.8 * a))
    c.drawRect(R(-50, y + 60, W + 100, 14), P("#94A3B8", 0.8 * a))


# ------------------------------------------------------------------ the roof from above (screen)
def roof_top(c, t, rain=1.0, flow=0.0):
    vrect(c, 0, 0, W, H, ["#0F172A", "#14532D", "#052E16"])
    for k in range(5):                                    # the terminals around it
        c.drawRect(R(-40 + k * 240, 1240 + (k % 2) * 30, 200, 120), P("#334155"))
    cx, cy, ax, ay = 540, 800, 470, 300
    hx, hy, hax, hay = 610, 785, 135, 84                  # the hole, a bit off centre
    ring_ = skia.Path()
    ring_.addOval(R(cx - ax, cy - ay, 2 * ax, 2 * ay))
    ring_.addOval(R(hx - hax, hy - hay, 2 * hax, 2 * hay))
    ring_.setFillType(skia.PathFillType.kEvenOdd)
    c.drawPath(ring_, lin_paint(cx - ax, cy - ay, cx + ax, cy + ay, ["#A5F3FC", "#67E8F9", "#0E7490"], a=0.9))
    c.save()
    c.clipPath(ring_, skia.ClipOp.kIntersect, True)
    for k in range(-30, 31):                              # triangular glass grid
        c.drawLine(cx + k * 34 - 600, cy - 600, cx + k * 34 + 600, cy + 600, P("#ECFEFF", 0.35, stroke=2))
        c.drawLine(cx + k * 34 + 600, cy - 600, cx + k * 34 - 600, cy + 600, P("#ECFEFF", 0.35, stroke=2))
        c.drawLine(cx - 600, cy + k * 34, cx + 600, cy + k * 34, P("#ECFEFF", 0.25, stroke=2))
    if flow > 0:                                          # rain water running toward the hole
        rng = random.Random(2)
        for k in range(60):
            ang = rng.uniform(0, 2 * math.pi)
            u = (t * 0.5 + rng.random()) % 1.0
            rr_ = lerp(1.0, 0.25, u)
            x = hx + math.cos(ang) * (hax + (ax - hax) * rr_ * 0.95)
            y = hy + math.sin(ang) * (hay + (ay - hay) * rr_ * 0.95)
            c.drawCircle(x, y, 7, P("#E0F2FE", 0.85 * flow))
    c.restore()
    c.drawOval(R(cx - ax, cy - ay, 2 * ax, 2 * ay), P("#ECFEFF", 0.9, stroke=6))
    c.drawOval(R(hx - hax, hy - hay, 2 * hax, 2 * hay), P("#0C4A6E"))
    c.drawOval(R(hx - hax, hy - hay, 2 * hax, 2 * hay), P("#ECFEFF", 0.9, stroke=6))
    if flow > 0:
        add_glow(c, hx, hy, 130, "#7DD3FC", 0.5 * flow)
    if rain > 0:
        rng = random.Random(9)
        for k in range(120):
            u = (t * rng.uniform(1.1, 1.6) + rng.random()) % 1.0
            x = rng.uniform(0, W) - u * 60
            y = lerp(-60, H, u)
            c.drawLine(x, y, x - 10, y + 40, P("#BAE6FD", 0.55 * rain, stroke=3))


# ------------------------------------------------------------------ the cutaway (world)
def section(c, t, mode, k=1.0, T=None):
    """The cutaway of the dome. mode: straight | curve | mist | drum | wind | wall | loop. k 0..1 how far the beat's
    change has gone."""
    vrect_w = 1400
    c.drawRect(R(-vrect_w / 2, -900, vrect_w, 1900), lin_paint(0, -900, 0, 1000, ["#0B1430", "#0F2A4A", "#0B1220"]))
    arch = skia.Path()                                    # the roof: a thick arch with the oculus near the top
    gap0, gap1 = OX - 70, OX + 70
    arch.moveTo(-560, FLOOR_Y)
    arch.cubicTo(-560, -260, -300, ROOF_Y, gap0, ROOF_Y + 10)
    arch2 = skia.Path()
    arch2.moveTo(gap1, ROOF_Y + 10)
    arch2.cubicTo(360, ROOF_Y, 560, -260, 560, FLOOR_Y)
    for pth in (arch, arch2):
        c.drawPath(pth, P("#67E8F9", 0.35, stroke=34))
        c.drawPath(pth, P("#ECFEFF", 0.9, stroke=6))
    for side in (-1, 1):                                  # floors and terraces stepping down to the valley
        for f in range(4):
            y = FLOOR_Y - f * 95
            x_in = side * (190 + f * 70)
            x_out = side * 540
            lo, hi = min(x_in, x_out), max(x_in, x_out)
            c.drawRect(R(lo, y - 16, hi - lo, 16), P("#94A3B8"))
            rng = random.Random(f * 7 + side)
            for j in range(5):
                tx = lerp(x_in, x_out, (j + 0.5) / 5)
                c.drawCircle(tx, y - 40, rng.uniform(20, 30), P(LEAF[rng.randrange(4)]))
    c.drawRect(R(-560, FLOOR_Y, 1120, 20), P("#94A3B8"))
    pit = R(OX - 150, FLOOR_Y, 300, 160)                  # the pit and the pool
    c.drawRect(pit, P("#0B1220"))
    c.drawRect(R(OX - 150, POOL_Y, 300, 70), lin_paint(0, POOL_Y, 0, POOL_Y + 70, ["#38BDF8", "#0C4A6E"]))
    c.drawRect(R(-560, 470, 1120, 150), P("#111827"))     # the tanks level (B3)
    for tx in (-380, 330):
        c.drawRRect(rr(tx - 90, 490, 180, 110, 18), P("#1E293B"))
        lvl = 0.6 + 0.15 * math.sin(t * 0.7)
        c.drawRRect(rr(tx - 86, 490 + 110 * (1 - lvl), 172, 110 * lvl - 4, 14), P("#0EA5E9", 0.8))
    # ---- the falling water
    if mode == "straight":
        top, bot = ROOF_Y + 10, FLOOR_Y + 2
        c.drawRect(R(OX - 40 - 110 * (1 - k) * 0, top, 80, bot - top), lin_paint(OX - 40, 0, OX + 40, 0, [WATER[2], WATER[0], WATER[2]], a=0.9))
        t0 = math.floor(t / 0.8) * 0.8
        splash(c, OX, FLOOR_Y, t, t0, dur=0.8, n=30, speed=900, width=2.0)
        splash(c, OX, FLOOR_Y, t, t0 - 0.4 if t - t0 < 0.4 else t0 + 0.4, dur=0.8, n=30, speed=900, width=2.0, seed=7)
    else:
        bend = 1.0
        for sd in (-1, 1):                                # two streams arcing in from the oculus rim
            path = skia.Path()
            x0 = OX + sd * 64
            path.moveTo(x0, ROOF_Y + 14)
            path.quadTo(OX + sd * 130 * bend, -60, OX + sd * 26, FLOOR_Y + 60)
            c.drawPath(path, P(WATER[1], 0.8, stroke=34))
            c.drawPath(path, P(WATER[0], 0.9, stroke=10))
        rng = random.Random(4)
        for j in range(24):                               # drops riding the curve
            u = (t * 0.9 + rng.random()) % 1.0
            sd = rng.choice((-1, 1))
            px = (1 - u) ** 2 * (OX + sd * 64) + 2 * (1 - u) * u * (OX + sd * 130) + u * u * (OX + sd * 26)
            py = (1 - u) ** 2 * (ROOF_Y + 14) + 2 * (1 - u) * u * (-60) + u * u * (FLOOR_Y + 60)
            c.drawCircle(px, py, 6, P("#FFFFFF", 0.9))
    if mode in ("drum", "wind", "wall", "loop"):
        drum(c, OX, FLOOR_Y - 190 * (k if mode == "drum" else 1.0), FLOOR_Y + 40, 300, fill=1.0)
    if mode == "mist":                                    # mist drifting over the terraces
        for j in range(10):
            sd = -1 if j % 2 else 1
            u = (t * 0.25 + j * 0.1) % 1.0
            puff(c, OX + sd * lerp(60, 520, u), FLOOR_Y - 40 - j * 12 - u * 80, lerp(40, 110, u), "#E0F2FE", 0.4 * (1 - u) * k)
    if mode in ("wind", "wall"):                          # air dragged into the pit / sent up by the glass wall
        up = 1.0 if mode == "wall" else 0.0
        for sd in (-1, 1):
            for j in range(3):
                y0 = FLOOR_Y - 60 - j * 50
                path = skia.Path()
                path.moveTo(OX + sd * 520, y0)
                if up:
                    path.quadTo(OX + sd * 220, y0 + 20, OX + sd * 190, y0 - 160 - j * 30)
                else:
                    path.quadTo(OX + sd * 200, y0, OX + sd * 120, FLOOR_Y + 110)
                c.drawPath(path, dash_paint("#FDE68A" if up else "#FCA5A5", 0.9, w=8, t=t * (1 if sd > 0 else -1)))
        if mode == "wall":
            for sd in (-1, 1):
                c.drawRect(R(OX + sd * 170 - 10, FLOOR_Y - 44 * k, 20, 44 * k), P("#BAE6FD", 0.85))
                c.drawRect(R(OX + sd * 170 - 10, FLOOR_Y - 44 * k, 20, 44 * k), P("#FFFFFF", 0.9, stroke=3))
    if mode == "loop":                                    # rain on the roof, tanks below, pumps carry it back up
        rng = random.Random(9)
        for j in range(60):
            u = (t * rng.uniform(1.0, 1.4) + rng.random()) % 1.0
            x = rng.uniform(-560, 560)
            y = lerp(-900, ROOF_Y - 60 + abs(x - OX) * 0.18, u)
            c.drawLine(x, y, x - 8, y + 30, P("#BAE6FD", 0.6 * k, stroke=3))
        pipe = skia.Path()
        pipe.moveTo(330, 540)
        pipe.lineTo(520, 540)
        pipe.lineTo(520, -200)
        pipe.quadTo(470, -480, OX + 90, ROOF_Y - 20)
        c.drawPath(pipe, P("#334155", 1.0, stroke=22))
        c.drawPath(pipe, dash_paint("#38BDF8", k, w=10, t=t * 2))
        link = skia.Path()
        link.moveTo(OX, POOL_Y + 60)
        link.lineTo(OX, 540)
        link.lineTo(240, 540)
        c.drawPath(link, P("#334155", 1.0, stroke=22))
        c.drawPath(link, dash_paint("#38BDF8", k, w=10, t=t * 2))
        c.drawCircle(450, 540, 34, P("#F59E0B"))           # the pump
        c.drawCircle(450, 540, 34, P("#FFFFFF", 0.8, stroke=4))
        for j in range(3):
            ang = t * 8 + j * 2.09
            c.drawLine(450, 540, 450 + math.cos(ang) * 26, 540 + math.sin(ang) * 26, P("#1F2937", 1.0, stroke=6))


def people_on_terraces(c, t, wet=0.0, hat_off=0.0):
    for j, (x, f) in enumerate(((-420, 0), (-300, 1), (300, 0), (430, 1), (-200, 0))):
        y = FLOOR_Y - f * 95 - 16
        person(c, x, y, 70, SHIRTS[j % len(SHIRTS)], t + j, pose="duck" if wet > 0.5 else "look", face=1 if x < 0 else -1, wet=wet)
    if hat_off > 0:
        u = hat_off
        hard_hat(c, lerp(-300, OX - 60, u), lerp(FLOOR_Y - 180, FLOOR_Y + 100, u * u), rot=u * 400, s=0.7)


def sink_scene(c, t, on=1.0, spray=1.0, wet=0.0):
    """A kitchen: the tap on full over a spoon in the sink, spray everywhere (screen)."""
    vrect(c, 0, 0, W, H, ["#FDE68A", "#FCD34D"])
    for x in range(0, W, 90):                             # tiles
        for y in range(380, 1000, 90):
            c.drawRect(R(x + 2, y + 2, 86, 86), P("#FEF3C7", 0.8))
    c.drawRect(R(0, 1000, W, 60), P("#78350F"))           # the counter
    c.drawRect(R(0, 1060, W, H - 1060), P("#92400E"))
    c.drawRRect(rr(300, 940, 480, 90, 30), P("#94A3B8"))  # the sink
    c.drawRRect(rr(330, 950, 420, 60, 24), P("#475569"))
    c.drawRRect(rr(500, 640, 40, 300, 16), P("#CBD5E1"))  # the tap
    c.drawRRect(rr(500, 620, 160, 44, 20), P("#CBD5E1"))
    c.drawRect(R(612, 664, 40, 30), P("#94A3B8"))
    c.drawOval(R(560, 975, 110, 30), P("#E2E8F0"))        # the spoon
    c.drawLine(620, 990, 720, 960, P("#E2E8F0", 1.0, stroke=12))
    if on > 0:
        c.drawRect(R(620, 694, 24, 280), lin_paint(620, 0, 644, 0, [WATER[2], WATER[0], WATER[2]], a=0.9 * on))
    if spray > 0:                                          # a wide fan of splashes off the spoon
        rng = random.Random(3)
        for j in range(70):
            u = (t * rng.uniform(1.2, 2.0) + rng.random()) % 1.0
            ang = math.radians(rng.uniform(-170, -10))
            sp = rng.uniform(300, 760)
            x = 615 + math.cos(ang) * sp * u
            y = 975 + math.sin(ang) * sp * u + 600 * u * u
            c.drawCircle(x, y, rng.uniform(4, 9), P("#7DD3FC", 0.85 * spray * (1 - u * 0.5)))
    person(c, 250, 1000, 300, "#0EA5E9", t, pose="duck" if wet > 0.5 else "stand", face=1, wet=wet)


# ====================================================================================== the episode
class RainVortex(EpisodeV2):
    BUILD_NO = 98
    FIRST_SET = "inside"
    CLEAR = "#06121F"
    TITLE = {"en": "RAIN VORTEX", "ar_sa": "شلال المطر"}
    EMPH = {"en": ["SINGAPORE'S", "AIRPORT", "WATERFALL", "ROOF", "INDOORS", "RIVER", "WATER", "GLASS", "DOUGHNUT",
                   "HOLE", "STRAIGHT", "SPLASHES", "EVERYBODY", "OFF", "CENTER", "CURVE", "MIST", "PHONES", "PASSPORTS",
                   "WET", "CLEAR", "DRUM", "TWO", "FLOORS", "DRAGS", "WIND", "GARDEN", "WALL", "UP", "SIDEWAYS",
                   "FOLLOW", "NOODLES", "HOLES", "RAIN", "CATCHES", "PUMPS", "FORTY", "TEN", "THOUSAND", "GALLONS",
                   "TREES", "CONGRATS", "VORTEX", "YOURSELF", "TAP", "SPOON"],
            "ar_sa": ["سنغافورة", "شلال", "السقف", "داخل", "نهر", "وين", "دونات", "زجاج", "دغري", "وترش", "قوس",
                      "الرذاذ", "جوالك", "وجوازك", "تبللوا", "أسطوانة", "شفافة", "دورين", "تسحب", "ريح", "الحديقة",
                      "فجدار", "لفوق", "متابعة", "نودلز", "خروم", "المطر", "يجمعه", "والمضخات", "أربعين", "ألف",
                      "ألفين", "شجرة", "مبروك", "حنفية", "ملعقة"]}
    KEYS = {"ar_sa": {
        ("hook", "SINGAPORE"): "سنغافورة", ("hook", "WATERFALL"): "شلال", ("hook", "ROOF"): "السقف",
        ("break1", "INDOORS"): "داخل", ("break1", "RIVER"): "نهر", ("break1", "WHERE"): "وين",
        ("fix1", "ROOF"): "السقف", ("fix1", "DOUGHNUT"): "دونات", ("fix1", "HOLE"): "الفتحة",
        ("break2", "STRAIGHT"): "دغري", ("break2", "SPLASHES"): "ترش",
        ("fix2", "HOLE"): "الفتحة", ("fix2", "OFF"): "مو", ("fix2", "CURVE"): "قوس",
        ("break3", "MIST"): "الرذاذ", ("break3", "PHONES"): "جوالك", ("break3", "WET"): "تبللوا",
        ("fix3", "CLEAR"): "شفافة", ("fix3", "DRUM"): "أسطوانة", ("fix3", "TWO"): "دورين",
        ("break4", "DRAGS"): "تسحب", ("break4", "WIND"): "ريح", ("break4", "GARDEN"): "الحديقة",
        ("fix4", "WALL"): "جدار", ("fix4", "GLASS"): "زجاج", ("fix4", "UP"): "لفوق",
        ("cta", "FOLLOW"): "متابعة",
        ("reveal", "RAIN"): "المطر", ("reveal", "CATCHES"): "يجمعه", ("reveal", "PUMPS"): "المضخات",
        ("stat", "FORTY"): "أربعين", ("stat", "TEN"): "ثمانية", ("stat", "TWO"): "شجرة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "TAP"): "حنفية", ("tag", "SPOON"): "ملعقة", ("tag", "DRUM"): "أسطوانة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: noodles full of tiny holes"),
                   "stat": [("40 m", "WATERFALL"), ("10,000", "GALLONS A MINUTE"), ("2,000+", "TREES")],
                   "L": {"name": "THE RAIN VORTEX", "air": "AN AIRPORT WATERFALL", "indoors": "INDOORS. NO RIVER.",
                         "where": "WHERE'S THE WATER FROM?", "donut": "A GLASS DOUGHNUT ROOF", "hole": "THE HOLE",
                         "straight": "STRAIGHT DOWN = SPLASH", "off": "HOLE OFF CENTER", "curve": "A SMOOTH CURVE",
                         "mist": "MIST EVERYWHERE", "wet": "PHONES, PASSPORTS... WET", "drum": "A CLEAR DRUM",
                         "two": "TWO FLOORS TALL", "wind": "WIND PULLED INTO THE PIT", "wall": "A LOW GLASS WALL",
                         "up": "AIR GOES UP", "rain": "RAIN!", "loop": "PUMPED BACK UP", "tap": "TAP ON FULL",
                         "get": "GET A DRUM!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: نودلز مليانة خروم"),
                      "stat": [("40", "متر شلال"), ("38000", "لتر بالدقيقة"), ("+2000", "شجرة")],
                      "L": {"name": "شلال المطر", "air": "شلال داخل مطار", "indoors": "داخل المطار، ولا فيه نهر",
                            "where": "الموية من وين؟", "donut": "سقف دونات زجاج", "hole": "الفتحة",
                            "straight": "دغري = رشاش", "off": "الفتحة مو بالنص", "curve": "قوس ناعم",
                            "mist": "رذاذ في كل مكان", "wet": "الجوال والجواز... تبللوا", "drum": "أسطوانة شفافة",
                            "two": "طولها دورين", "wind": "ريح تنسحب للحفرة", "wall": "جدار زجاج قصير",
                            "up": "الهوا يطلع لفوق", "rain": "المطر!", "loop": "ترجع فوق بالمضخات",
                            "tap": "الحنفية على آخرها", "get": "تبي أسطوانة!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "sing": ("hook", "SINGAPORE", 0.3), "fall": ("hook", "WATERFALL", 0.6), "roof": ("hook", "ROOF", 0.9),
            "indoors": ("break1", "INDOORS", 0.1), "river": ("break1", "RIVER", 0.35), "where": ("break1", "WHERE", 0.7),
            "roof1": ("fix1", "ROOF", 0.15), "donut": ("fix1", "DOUGHNUT", 0.55), "hole": ("fix1", "HOLE", 0.85),
            "straight": ("break2", "STRAIGHT", 0.5), "splash": ("break2", "SPLASHES", 0.8),
            "hole2": ("fix2", "HOLE", 0.1), "off": ("fix2", "OFF", 0.3), "curve": ("fix2", "CURVE", 0.9),
            "mist": ("break3", "MIST", 0.2), "phones": ("break3", "PHONES", 0.6), "wet": ("break3", "WET", 0.9),
            "clear": ("fix3", "CLEAR", 0.4), "drum": ("fix3", "DRUM", 0.5), "two": ("fix3", "TWO", 0.8),
            "drags": ("break4", "DRAGS", 0.25), "wind": ("break4", "WIND", 0.75), "garden": ("break4", "GARDEN", 0.9),
            "wall": ("fix4", "WALL", 0.2), "glass": ("fix4", "GLASS", 0.45), "up": ("fix4", "UP", 0.7),
            "follow": ("cta", "FOLLOW", 0.35),
            "rain": ("reveal", "RAIN", 0.15), "catches": ("reveal", "CATCHES", 0.45), "pumps": ("reveal", "PUMPS", 0.75),
            "s1": ("stat", "FORTY", 0.05), "s2": ("stat", "TEN", 0.35), "s3": ("stat", "TWO", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_tap": ("tag", "TAP", 0.2), "t_spoon": ("tag", "SPOON", 0.5), "t_drum": ("tag", "DRUM", 0.9)})
        T["where1"] = max(T["river"], T["indoors"]) + 0.2
        T["donut1"] = max(T["donut"], T["roof1"]) + 0.25
        T["splash1"] = max(T["straight"], s("break2") + 0.3) + 0.2
        T["curve1"] = max(T["curve"], T["off"]) + 0.2
        T["wet1"] = max(T["mist"], s("break3") + 0.3) + 0.2
        T["drum1"] = max(T["drum"], T["clear"]) + 0.25
        T["wind1"] = max(T["drags"], s("break4") + 0.3) + 0.2
        T["wall1"] = max(T["wall"], T["glass"]) + 0.25
        # ---- sets
        self.cut(s("fix1") - 0.12, "roof", 1)
        self.cut(s("break2") - 0.12, "section", -1)
        self.cut(s("stat") - 0.12, "inside", 1)
        self.cut(s("tag") - 0.2, "sink", -1)
        # ---- camera (section set)
        cm = Camera(OX, 135, 0.85)
        cm.key(s("break2") - 0.12, OX, 135, 0.85, 0.0)
        cm.key(s("break3") - 0.12, OX - 50, 140, 0.9, 0.6)
        cm.key(s("fix3") - 0.12, OX, 120, 0.95, 0.6)
        cm.key(s("break4") - 0.12, OX, 135, 0.85, 0.6)
        cm.key(s("reveal") - 0.12, 30, 250, 0.74, 0.8)
        self.cam = cm
        self.spans = [(T["where1"], T["donut1"]), (T["splash1"], T["curve1"]), (T["wet1"], T["drum1"]), (T["wind1"], T["wall1"])]
        self.shakes = [(T["fall"], 0.3, 5), (T["where1"], 0.3, 5), (T["splash1"], 0.4, 9), (T["wet1"], 0.3, 6),
                       (T["wind1"], 0.35, 6), (s("closer") + 0.2, 0.35, 8), (T["t_spoon"], 0.3, 8)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: inside
    def draw_inside(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        night = 0.0
        if ph in ("stat", "closer"):
            night = prog(t, s("stat"), s("stat") + 1.0)
        zoom = 1.0
        if ph == "hook":                                  # push in from the oculus, then settle
            zoom = lerp(1.35, 1.0, e_io(prog(t, 0.0, T["fall"] + 0.6)))
        c.save()
        c.translate(540, 620)
        c.scale(zoom, zoom)
        c.translate(-540, -620)
        dome_inside(c, t, night)
        sky_train(c, t, 690, a=1.0 - 0.5 * night)
        for sd in (-1, 1):
            terraces(c, t, sd, night)
        dry = ph == "break1"
        if not dry:
            falling_water(c, t, 580, 350, 560, 1080, 200, 130, night=night, bend=1.0)
        else:
            k = prog(t, s("break1"), s("break1") + 0.3)
            falling_water(c, t, 580, 350, 560, 1080, 200, 130, a=1 - k, bend=1.0)
        drum(c, 560, 960, 1140, 280)
        c.drawRect(R(-200, 1180, W + 400, 1000), lin_paint(0, 1180, 0, 1700, [mix("#44403C", "#1C1917", night), "#0C0A09"]))   # the valley floor
        c.drawOval(R(380, 1150, 360, 70), P(mix("#0EA5E9", "#1E3A8A", night), 0.9))                                          # the pool
        for j in range(5):                                # mist at the foot
            puff(c, 560 + (j - 2) * 60, 1080 - j * 10 + math.sin(t + j) * 8, 70, "#E0F2FE", 0.25 * (1 - night * 0.5))
        if night > 0:
            add_glow(c, 570, 760, 300, hue_col(t * 0.15 + 0.3), 0.35 * night)
        c.restore()

    def ui_inside(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "air", T["fall"] - 0.2, s("break1") + 0.1, accent="#7DD3FC", size=48)
            return
        if ph == "break1":
            self.chip(540, 300, "indoors", T["indoors"] - 0.1, T["where"] - 0.2, accent=WARN, size=48)
            self.chip(540, 300, "where", T["where"] - 0.2, s("fix1") - 0.15, accent=HILITE, size=48)
            k = self.span(T["river"], s("fix1") - 0.1)
            if k > 0:
                text(c, "?", 560, 760, 300, HILITE, "Poppins-Black", a=k)
            self.badge("alert", T["where1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["where1"], 1.2)
            return
        if ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: roof (fix1)
    def draw_roof(self, c, t):
        T = self.T
        roof_top(c, t, rain=1.0, flow=prog(t, T["hole"] - 0.3, T["hole"] + 0.3))

    def ui_roof(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "donut", T["roof1"] - 0.1, T["hole"] - 0.15, accent="#67E8F9", size=48)
        self.chip(540, 300, "hole", T["hole"] - 0.15, s("break2") - 0.15, accent=HILITE, size=52)
        self.badge("check", T["donut1"], s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: section (break2 .. reveal)
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        cam = self.cam.at(t)
        self.view(c, cam)
        mode = {"break2": "straight", "fix2": "curve", "break3": "mist", "fix3": "drum", "break4": "wind", "fix4": "wall",
                "cta": "wall", "reveal": "loop"}.get(ph, "curve")
        k = 1.0
        if ph == "break3":
            k = prog(t, T["mist"] - 0.2, T["mist"] + 0.6)
        elif ph == "fix3":
            k = e_out(prog(t, T["drum"] - 0.2, T["drum"] + 0.6))
        elif ph == "fix4":
            k = e_out(prog(t, T["wall"], T["wall"] + 0.5))
        elif ph == "reveal":
            k = prog(t, T["rain"] - 0.2, T["rain"] + 0.4)
        section(c, t, mode, k, T)
        wet = 0.0
        if ph == "break2":
            wet = prog(t, T["splash"] - 0.2, T["splash"] + 0.3)
        elif ph == "break3":
            wet = prog(t, T["phones"], T["wet"] + 0.2)
        hat = prog(t, T["wind"] - 0.3, T["wind"] + 0.9) if ph == "break4" else 0.0
        people_on_terraces(c, t, wet=wet, hat_off=hat)
        if ph == "break4":                                # the palms bend toward the pit
            for sd in (-1, 1):
                bx = OX + sd * 300
                lean = 18 * prog(t, T["drags"], T["drags"] + 0.6) * (1 + 0.3 * math.sin(t * 6))
                c.drawLine(bx, FLOOR_Y - 16, bx - sd * lean, FLOOR_Y - 150, P("#78350F", 1.0, stroke=10))
                c.drawCircle(bx - sd * lean * 1.3, FLOOR_Y - 160, 40, P(LEAF[2]))
        c.restore()
        self.ui["cam"] = cam

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break2":
            self.chip(540, 300, "straight", T["straight"] - 0.2, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["splash1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["splash1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "off", T["off"] - 0.2, T["curve"] - 0.15, accent=HILITE, size=48)
            self.chip(540, 300, "curve", T["curve"] - 0.15, s("break3") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["curve1"], s("break3") - 0.15, x=920, y=440)
        elif ph == "break3":
            self.chip(540, 300, "mist", T["mist"] - 0.1, T["phones"] - 0.15, accent="#E0F2FE", size=48)
            self.chip(540, 300, "wet", T["phones"] - 0.15, s("fix3") - 0.15, accent=WARN, size=42)
            self.badge("alert", T["wet1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["wet1"], 1.2)
        elif ph == "fix3":
            self.chip(540, 300, "drum", T["clear"] - 0.2, T["two"] - 0.15, accent="#7DD3FC", size=50)
            self.chip(540, 300, "two", T["two"] - 0.15, s("break4") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["drum1"], s("break4") - 0.15, x=920, y=440)
        elif ph == "break4":
            self.chip(540, 300, "wind", T["drags"] - 0.1, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["wind1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["wind1"], 1.2)
        elif ph in ("fix4", "cta"):
            self.chip(540, 300, "wall", T["wall"] - 0.2, T["up"] - 0.15, accent="#BAE6FD", size=48)
            self.chip(540, 300, "up", T["up"] - 0.15, s("cta") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["wall1"], s("cta") - 0.15, x=920, y=440)
        elif ph == "reveal":
            self.chip(540, 300, "rain", T["rain"] - 0.15, T["pumps"] - 0.15, accent=HILITE, size=60)
            self.chip(540, 300, "loop", T["pumps"] - 0.15, s("stat") - 0.15, accent="#38BDF8", size=48)

    # ------------------------------------------------------------------ set: sink (tag)
    def draw_sink(self, c, t):
        T = self.T
        on = prog(t, T["t_tap"] - 0.1, T["t_tap"] + 0.2)
        spray = prog(t, T["t_spoon"] - 0.1, T["t_spoon"] + 0.3)
        sink_scene(c, t, on=on, spray=spray, wet=prog(t, T["t_spoon"] + 0.3, T["t_drum"]))

    def ui_sink(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "tap", T["t_tap"] - 0.1, T["t_drum"] - 0.2, accent="#38BDF8", size=48)
        self.chip(540, 300, "get", T["t_drum"] - 0.2, self.duration + 1, accent=WARN, size=54)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, DAYP)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["fall"], sfx.hiss(2.5, 62), -14), (T["roof"], sfx.chime(), -9)]
        ev += [(T["indoors"], sfx.power_down(0.8, 63), -14), (T["where1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["roof1"], sfx.hiss(2.0, 65), -16),
               (T["donut1"], sfx.ding(), -8), (T["donut1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, False, 66), -6), (T["splash1"], boom(1.0, 67), -12),
               (T["splash1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["off"], sfx.whoosh(0.6, True, 68), -12), (T["curve1"], sfx.ding(), -8), (T["curve1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["mist"], sfx.hiss(1.2, 69), -14), (T["wet1"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(T["drum"], sfx.thunk(70), -6), (T["drum1"], sfx.ding(), -8), (T["drum1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["drags"], sfx.whoosh(1.0, False, 71), -10), (T["wind1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["wall"], sfx.thunk(72), -6), (T["wall1"], sfx.ding(), -8), (T["wall1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(T["rain"], sfx.hiss(2.0, 94), -12), (T["pumps"], sfx.hum(1.5, 90.0), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 96), -6), (T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3),
               (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"], sfx.pop(100), -2), (T["cong2"], sfx.sparkle(1.4, 18, 101), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 102), -6), (T["t_tap"], sfx.hiss(2.5, 103), -10),
               (T["t_spoon"], boom(0.8, 104), -14), (T["t_drum"], sfx.womp(), -8)]
        return ev


NAME = "rainvortex"
EPISODE = RainVortex
