"""Episode 100 - the Jeddah Tower (Build #100).  v2 look.

Sets: sky (hook: Jeddah by the Red Sea at dusk, the tower built to about half its height with cranes on top, its planned
outline drawing itself up to a 1,000 m ruler; cta; reveal: a race of skylines beside it, the Petronas Towers and Taipei
101 and the Burj Khalifa as outlines, the tower's height marker climbing past Petronas to almost 500 m; stat; closer:
the finished tower at night with its lights on), ground (break1: a cut through the ground, sand over soft limestone full
of seashells, a heavy block sinks and tilts; fix1: 270 piles drilled down, the longest 105 m under the middle, one
thick slab on top), wind (break2: a plain box tower, a breeze at the street, ten times faster up top, whirlpools peel off
and it sways; fix2: the real shape, thinner as it rises, the air slides past), plan (break3: a pencil on its tip
wobbling; fix3: from above three wings grow around the core and brace it, a tripod beside it), lift (break4: a lift shaft
with a bundle of steel ropes too heavy for the motor; fix4: a thin black carbon belt, the car shoots up past 630 m),
tag (stepping out of a cold car into Jeddah's damp heat: the glasses fog up).
Side views: the ground is y = 1200 in screen space, up is negative.
"""
from v2_base import *  # noqa: F401,F403

GROUND = 1200
M = 0.8                                            # pixels per metre in the sky set (1,000 m = 800 px)
TOP_M, BUILT_M = 1008.0, 490.0
CONC, GLASS_T = "#8C95A3", "#7FA6C9"
SEA = ["#0E7490", "#155E75"]
DUSKP = ["#1E1B4B", "#5B21B6", "#C2410C", "#F59E0B"]


def tower_hw(f):
    """Half widths (left, right) in metres at height fraction f (0 = ground, 1 = the tip): three wings that taper and
    end at different heights, the core going on up to a spire."""
    base = 70.0
    body = base * (1 - f) ** 0.9
    core = lerp(22.0, 3.0, f)
    left = body if f < 0.66 else max(core, body * 0.55)
    right = body if f < 0.79 else max(core, body * 0.5)
    return max(left, core), max(right, core)


def jtower(c, x, t, built=1.0, plan=1.0, lit=0.0, cranes=True, a=1.0, scale=M, glow=0.0):
    """The tower from the side, base centre at (x, GROUND). built: the solid part as a fraction of its height; plan: the
    rest drawn as a glowing outline (0..1 draws it upward)."""
    if a <= 0:
        return
    hpx = TOP_M * scale
    n = 120
    pts_l, pts_r = [], []
    for i in range(n + 1):
        f = i / n
        hl, hr = tower_hw(f)
        y = GROUND - f * hpx
        pts_l.append((x - hl * scale, y))
        pts_r.append((x + hr * scale, y))
    # solid part
    fb = clamp(built)
    if fb > 0:
        nb = int(n * fb)
        body = skia.Path()
        body.moveTo(*pts_l[0])
        for p in pts_l[1:nb + 1]:
            body.lineTo(*p)
        for p in reversed(pts_r[:nb + 1]):
            body.lineTo(*p)
        body.close()
        c.drawPath(body, lin_paint(x - 70 * scale, 0, x + 70 * scale, 0, [shade(CONC, -0.35), shade(CONC, 0.2), CONC,
                                                                           shade(CONC, -0.45)], a=a))
        c.save()
        c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawRect(R(x - 8 * scale, GROUND - hpx, 16 * scale, hpx), P("#FFFFFF", 0.12 * a))
        for k in range(1, int(fb * TOP_M / 12)):          # floor lines
            yy = GROUND - k * 12 * scale
            c.drawLine(x - 80 * scale, yy, x + 80 * scale, yy, P("#334155", 0.22 * a, stroke=1.2))
        if lit > 0:
            rng = random.Random(7)
            for k in range(1, int(fb * TOP_M / 6)):
                yy = GROUND - k * 6 * scale
                for j in range(-6, 7):
                    if rng.random() < 0.45:
                        c.drawRect(R(x + j * 9 * scale - 3, yy - 2, 6, 3), P("#FFE2A8", lit * a * rng.uniform(0.5, 1.0)))
        c.restore()
        if lit > 0:
            for k in range(6):
                add_glow(c, x, GROUND - hpx * (0.08 + 0.15 * k), 160 - 20 * k, "#FFD27A", 0.07 * lit * a)
            beacon(c, x, GROUND - hpx * fb - 6, t, r=6)
        if cranes and fb < 0.98:
            yt = GROUND - hpx * fb
            hl, hr = tower_hw(fb)
            for k, (dx, s_) in enumerate(((-hl * scale * 0.5, 0.45), (hr * scale * 0.4, 0.38))):
                crane(c, x + dx, yt, t + k, s_, flip=k == 1, a=a)
    # the planned rest: a glowing outline drawn upward
    if plan > 0 and fb < 1:
        nb = int(n * fb)
        ne = nb + int((n - nb) * clamp(plan))
        for side in (pts_l, pts_r):
            p = skia.Path()
            p.moveTo(*side[nb])
            for q in side[nb + 1:ne + 1]:
                p.lineTo(*q)
            c.drawPath(p, dash_paint("#7DD3FC", 0.95 * a, w=4, t=t))
        if ne >= n:
            c.drawLine(pts_l[n][0], pts_l[n][1], pts_r[n][0], pts_r[n][1], dash_paint("#7DD3FC", 0.95 * a, w=4, t=t))
        add_glow(c, x, (pts_l[nb][1] + pts_l[ne][1]) / 2, 160, "#38BDF8", 0.12 * a * plan)
    if glow > 0:
        add_glow(c, x, GROUND - hpx * 0.5, 420, "#FDE68A", 0.25 * glow)


def crane(c, x, y, t, s=0.5, flip=False, a=1.0):
    """A tower crane standing on (x, y), s = scale."""
    c.save()
    c.translate(x, y)
    c.scale(-s if flip else s, s)
    lattice(c, 0, 0, -190, w=22, col="#F59E0B")
    c.drawRect(R(-120, -204, 330, 12), P("#F59E0B", a))
    for xx in range(-110, 200, 22):
        c.drawLine(xx, -204, xx + 11, -192, P("#B45309", a, stroke=2))
    c.drawRRect(rr(-14, -236, 30, 32, 5), P("#FDE68A", a))
    hx = 160 + math.sin(t * 0.8) * 14
    c.drawLine(hx, -192, hx, -110, P("#1F2937", a, stroke=2))
    c.drawRect(R(hx - 8, -110, 16, 10), P("#EF4444", a))
    beacon(c, 0, -240, t, r=4)
    c.restore()


def jeddah_backdrop(c, t, pal=DUSKP, lights=0.6, haze=0.0):
    """Jeddah at dusk: the sky, the Red Sea on the left, a low city along the shore."""
    vrect(c, 0, 0, W, GROUND, pal)
    v2.stars(c, W, H, t, 0.5)
    c.drawRect(R(0, GROUND - 70, 520, 70), lin_paint(0, GROUND - 70, 0, GROUND, SEA))
    for k in range(9):
        xx = (k * 70 + t * 20) % 560 - 40
        c.drawLine(xx, GROUND - 50 + (k % 3) * 14, xx + 36, GROUND - 50 + (k % 3) * 14, P("#FDBA74", 0.45, stroke=3))
    rng = random.Random(3)
    for k in range(22):                               # the low city
        bx = 420 + k * 34
        bh = rng.uniform(30, 120)
        c.drawRect(R(bx, GROUND - bh, 30, bh), P("#1E1B3A"))
        if rng.random() < 0.7:
            c.drawRect(R(bx + 8, GROUND - bh + 10, 8, 6), P("#FFD27A", lights))
    c.drawRect(R(0, GROUND, W, H - GROUND), lin_paint(0, GROUND, 0, H, ["#3B2F2A", "#1C1512"]))
    if haze > 0:
        c.drawRect(R(0, 0, W, H), P("#E5E7EB", 0.25 * haze))


def ruler(c, x, t, k=1.0, top_m=1000, a=1.0):
    """A height ruler from the ground up to top_m (drawn upward with k)."""
    if a <= 0:
        return
    h = top_m * M * clamp(k)
    c.drawLine(x, GROUND, x, GROUND - h, P("#F8FAFC", 0.85 * a, stroke=4))
    for m_ in range(0, int(top_m * clamp(k)) + 1, 100):
        yy = GROUND - m_ * M
        c.drawLine(x - 14, yy, x + 14, yy, P("#F8FAFC", 0.85 * a, stroke=3))
    if k >= 1:
        c.drawRRect(rr(x - 86, GROUND - top_m * M - 30, 172, 56, 16), P("#0B1220", 0.85 * a))
        text(c, f"{top_m} M", x, GROUND - top_m * M + 12, 36, HILITE, "Poppins-Black", a=a)


def outline_building(c, x, h_m, kind, a=1.0, col="#CBD5E1", label=None):
    """Other famous towers as outlines for the height race (h_m in metres)."""
    if a <= 0:
        return
    h = h_m * M
    p = skia.Path()
    if kind == "petronas":
        for dx in (-34, 34):
            p.moveTo(x + dx - 18, GROUND)
            p.lineTo(x + dx - 18, GROUND - h * 0.82)
            p.lineTo(x + dx - 8, GROUND - h * 0.92)
            p.lineTo(x + dx, GROUND - h)
            p.lineTo(x + dx + 8, GROUND - h * 0.92)
            p.lineTo(x + dx + 18, GROUND - h * 0.82)
            p.lineTo(x + dx + 18, GROUND)
        c.drawLine(x - 16, GROUND - h * 0.38, x + 16, GROUND - h * 0.38, P(col, a, stroke=4))
    elif kind == "taipei":
        y = GROUND
        p.moveTo(x - 30, y)
        p.lineTo(x - 30, y - h * 0.25)
        for k in range(8):
            y0 = GROUND - h * (0.25 + k * 0.075)
            p.lineTo(x - 30, y0)
            p.lineTo(x - 36, y0 - h * 0.075)
        p.lineTo(x - 6, GROUND - h * 0.9)
        p.lineTo(x, GROUND - h)
        p.lineTo(x + 6, GROUND - h * 0.9)
        for k in reversed(range(8)):
            y0 = GROUND - h * (0.25 + k * 0.075)
            p.lineTo(x + 36, y0 - h * 0.075)
            p.lineTo(x + 30, y0)
        p.lineTo(x + 30, y)
    else:                                             # the Burj Khalifa: stepped, a long spire
        p.moveTo(x - 52, GROUND)
        for k in range(6):
            p.lineTo(x - 52 + k * 7, GROUND - h * (0.12 + k * 0.12))
            p.lineTo(x - 45 + k * 7, GROUND - h * (0.12 + k * 0.12))
        p.lineTo(x - 3, GROUND - h)
        p.lineTo(x + 3, GROUND - h)
        for k in reversed(range(6)):
            p.lineTo(x + 45 - k * 7, GROUND - h * (0.12 + k * 0.12))
            p.lineTo(x + 52 - k * 7, GROUND - h * (0.12 + k * 0.12))
        p.lineTo(x + 52, GROUND)
    c.drawPath(p, P(col, 0.15 * a))
    c.drawPath(p, P(col, a, stroke=4))
    if label:
        text(c, label, x, GROUND - h - 26, 30, col, "Poppins-Black", a=a)


def ground_cut(c, t, sink=0.0, piles=0.0, raft=0.0, tower_k=0.0):
    """Under the tower: 2 m of sand, soft limestone full of shells, harder rock deep down. sink: a heavy block sinking
    and tilting; piles: 270 piles drilled down (the middle ones deepest, 105 m); raft: one thick slab on top."""
    top = 520
    vrect(c, 0, 0, W, top, ["#1E1B4B", "#9A3412"])
    c.drawRect(R(0, top, W, 40), P("#D6B47A"))       # sand
    c.drawRect(R(0, top + 40, W, 760), lin_paint(0, top + 40, 0, top + 800, ["#CDBB97", "#A8946E", "#7D6B4E"]))
    rng = random.Random(5)
    for k in range(70):                               # shells in the soft rock
        sx, sy = rng.uniform(20, 1060), rng.uniform(top + 60, top + 760)
        c.save()
        c.translate(sx, sy)
        c.rotate(rng.uniform(0, 360))
        sh = skia.Path()
        sh.moveTo(0, 0)
        for j in range(6):
            ang = math.radians(-60 + j * 24)
            sh.lineTo(math.cos(ang) * 16, math.sin(ang) * 16)
        sh.close()
        c.drawPath(sh, P("#F5E9D3", 0.75))
        c.drawPath(sh, P("#8A7656", 0.6, stroke=2))
        c.restore()
    for k in range(40):                               # pores
        c.drawCircle(rng.uniform(20, 1060), rng.uniform(top + 60, top + 780), rng.uniform(3, 7), P("#5C4D36", 0.5))
    c.drawRect(R(0, top + 800, W, H - top - 800), P("#57534E"))
    if sink > 0 and piles <= 0:                       # a heavy block on soft rock: it sinks and tilts
        c.save()
        c.translate(540, top + 120 * sink)
        c.rotate(-7 * sink)
        c.drawRect(R(-200, -260, 400, 260), lin_paint(-200, 0, 200, 0, [shade(CONC, -0.3), CONC, shade(CONC, -0.4)]))
        text(c, "860,000 T", 0, -110, 48, "#1F2937", "Poppins-Black")
        c.restore()
        for k in range(6):                            # cracks
            cx_ = 360 + k * 70
            c.drawLine(cx_, top + 40, cx_ + 20, top + 40 + 160 * sink, P("#3F3428", sink, stroke=4))
    if piles > 0:
        for k in range(27):
            x = 60 + k * 37
            d = 1 - abs(x - 540) / 520
            depth = lerp(0.43, 1.0, d) * 105 * 6.6 * clamp(piles * 1.4 - (1 - d) * 0.4)
            c.drawRect(R(x - 9, top + 20, 18, depth), lin_paint(x - 9, 0, x + 9, 0, ["#6B7280", "#D1D5DB", "#6B7280"]))
            if 0 < depth < 690:
                c.drawCircle(x, top + 20 + depth, 10, P("#F59E0B"))
    if raft > 0:
        c.drawRect(R(40, top - 34 * raft, 1000, 60 * raft), lin_paint(0, top - 34, 0, top + 26, ["#E5E7EB", "#9CA3AF"]))
    if tower_k > 0:
        c.save()
        c.clipRect(R(0, 0, W, top - 30))
        hl, hr = tower_hw(0.0)
        base = skia.Path()
        base.moveTo(540 - hl * 3.0, top - 30)
        base.lineTo(540 - hl * 1.9, top - 30 - 900)
        base.lineTo(540 + hr * 1.9, top - 30 - 900)
        base.lineTo(540 + hr * 3.0, top - 30)
        base.close()
        c.drawPath(base, lin_paint(140, 0, 940, 0, [shade(CONC, -0.35), CONC, shade(CONC, -0.45)], a=tower_k))
        c.restore()


def box_tower(c, x, t, sway=0.0, a=1.0):
    """A plain box tower (the shape the wind loves), base at (x, GROUND)."""
    c.save()
    c.translate(x, GROUND)
    c.rotate(math.sin(t * 2.6) * 1.6 * sway)
    c.drawRect(R(-60, -980, 120, 980), lin_paint(-60, 0, 60, 0, [shade(CONC, -0.3), CONC, shade(CONC, -0.45)], a=a))
    for k in range(1, 40):
        c.drawLine(-60, -k * 25, 60, -k * 25, P("#334155", 0.2 * a, stroke=1.2))
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


def wind_streaks(c, t, y0, y1, speed, a=1.0, seed=1, n=10, length=80):
    rng = random.Random(seed)
    for k in range(n):
        y = rng.uniform(y0, y1)
        u = (t * speed / 900 + rng.random()) % 1.0
        x = lerp(-150, W + 150, u)
        c.drawLine(x, y, x - length, y, P("#E0F2FE", a * 0.8, stroke=4))
        c.drawLine(x - length, y, x - length - 14, y - 8, P("#E0F2FE", a * 0.5, stroke=3))


def pencil(c, x, y, L, rot, a=1.0):
    """A pencil balanced on its tip at (x, y), rot in degrees."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    tip = skia.Path()
    tip.moveTo(0, 0)
    tip.lineTo(-22, -60)
    tip.lineTo(22, -60)
    tip.close()
    c.drawPath(tip, P("#F5D0A9", a))
    c.drawPath(skia.Path().moveTo(0, 0).lineTo(-8, -22).lineTo(8, -22).close(), P("#1F2937", a))
    c.drawRect(R(-22, -60 - L, 44, L), lin_paint(-22, 0, 22, 0, ["#FDE047", "#FACC15", "#CA8A04"], a=a))
    c.drawRect(R(-22, -78 - L, 44, 18), P("#94A3B8", a))
    c.drawRRect(rr(-22, -112 - L, 44, 36, 10), P("#F472B6", a))
    c.restore()


def tripod(c, x, y, s=1.0, k=1.0, a=1.0):
    """A camera on a tripod, feet on y, centred on x."""
    if a <= 0 or k <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s * e_back(k), s * e_back(k))
    for fx_ in (-80, 0, 80):
        c.drawLine(0, -170, fx_, 0 if fx_ else -20, P("#E5E7EB", a, stroke=9))
    c.drawRRect(rr(-50, -230, 100, 62, 10), P("#334155", a))
    c.drawCircle(0, -199, 20, P("#0EA5E9", a))
    c.drawCircle(0, -199, 9, P("#E0F2FE", a))
    c.restore()


def plan_view(c, t, wings=0.0, wob=0.0):
    """The tower from above: a round core, and three wings growing around it at 120 degrees."""
    vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
    cx, cy = 540, 760
    for r_ in (520, 400, 280):                        # the plot's rings
        c.drawCircle(cx, cy, r_, P("#334155", 0.6, stroke=2))
    c.save()
    c.translate(cx + math.sin(t * 7) * 18 * wob, cy)
    if wings > 0:
        for k in range(3):
            ang = math.radians(-90 + k * 120)
            L = 330 * e_out(clamp(wings * 1.5 - k * 0.25))
            p = skia.Path()
            nx, ny = math.cos(ang), math.sin(ang)
            px_, py_ = -ny, nx
            p.moveTo(px_ * 95, py_ * 95)
            p.lineTo(nx * L + px_ * 40, ny * L + py_ * 40)
            p.lineTo(nx * (L + 30), ny * (L + 30))
            p.lineTo(nx * L - px_ * 40, ny * L - py_ * 40)
            p.lineTo(-px_ * 95, -py_ * 95)
            p.close()
            c.drawPath(p, lin_paint(-300, -300, 300, 300, [shade(CONC, 0.2), CONC, shade(CONC, -0.35)]))
            c.drawPath(p, P("#475569", 1.0, stroke=3))
    c.drawCircle(0, 0, 110, rad_paint(-30, -30, 140, [shade(CONC, 0.3), CONC, shade(CONC, -0.4)]))
    c.drawCircle(0, 0, 110, P("#475569", 1.0, stroke=4))
    c.restore()


def lift_shaft(c, t, heavy=0.0, belt=0.0, rise=0.0, strain=0.0):
    """A lift shaft cut open: the motor at the top, the ropes, the car. heavy: a fat bundle of steel ropes;
    belt: a thin black carbon belt; rise 0..1 the car going up."""
    vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])
    sx0, sx1 = 330, 750
    c.drawRect(R(sx0, 330, sx1 - sx0, 900), P("#0B1220"))
    for k in range(18):
        c.drawLine(sx0, 330 + k * 50, sx1, 330 + k * 50, P("#1E293B", 1.0, stroke=3))
    c.drawRect(R(sx0 - 20, 330, 20, 900), P("#334155"))
    c.drawRect(R(sx1, 330, 20, 900), P("#334155"))
    c.drawCircle(540, 400, 70, P("#64748B"))         # the motor sheave
    c.drawCircle(540, 400, 70, P("#94A3B8", 1.0, stroke=10))
    c.drawCircle(540, 400, 18, P("#1F2937"))
    car_y = lerp(1060, 560, e_io(rise)) + (math.sin(t * 40) * 4 * strain)
    if heavy > 0:                                     # a thick bundle of steel ropes
        for k in range(9):
            x = 500 + k * 10
            c.drawLine(x, 400, x + math.sin(t + k) * 2, car_y - 90, P("#9CA3AF", heavy, stroke=8))
            c.drawLine(x, 400, x, car_y - 90, P("#4B5563", 0.6 * heavy, stroke=2))
        if strain > 0:
            for k in range(6):
                u = (t * 2 + k / 6) % 1.0
                c.drawCircle(540 + math.cos(k) * 90 * u, 400 + math.sin(k * 2) * 60 * u, 5, P("#FDBA74", strain * (1 - u)))
    if belt > 0:                                      # one thin carbon belt
        c.drawRect(R(532, 400, 16, car_y - 90 - 400), P("#0A0A0A", belt))
        c.drawRect(R(536, 400, 4, car_y - 90 - 400), P("#4B5563", belt))
    c.drawRRect(rr(400, car_y - 90, 280, 200, 14), lin_paint(400, 0, 680, 0, ["#94A3B8", "#E2E8F0", "#64748B"]))
    c.drawRRect(rr(430, car_y - 60, 220, 140, 8), P("#FDE68A", 0.85))
    person(c, 500, car_y + 80, 120, "#0EA5E9", t, pose="stand", face=1)
    person(c, 580, car_y + 80, 115, "#F97316", t + 1, pose="cheer" if rise > 0.5 else "stand", face=-1)


def scale_card(c, x, y, k, heavy=True, a=1.0):
    """A see-saw scale: the steel rope bundle against the lift car."""
    if a <= 0:
        return
    tilt = 14 * k if heavy else -6 * k
    c.save()
    c.translate(x, y)
    c.drawRRect(rr(-180, -150, 360, 300, 26), P("#0B1220", 0.85 * a))
    c.drawPath(skia.Path().moveTo(-20, 90).lineTo(20, 90).lineTo(0, 40).close(), P("#94A3B8", a))
    c.rotate(tilt)
    c.drawLine(-140, 40, 140, 40, P("#CBD5E1", a, stroke=8))
    c.drawRect(R(-140, -10, 90, 50), P("#9CA3AF", a))        # ropes
    for j in range(5):
        c.drawLine(-135, -2 + j * 9, -55, -2 + j * 9, P("#4B5563", a, stroke=3))
    c.drawRRect(rr(60, -20, 70, 60, 8), P("#E2E8F0", a))      # the car
    c.restore()


def car_door(c, t, fog=0.0):
    """The tag: stepping out of a cold car into damp heat, glasses fogging."""
    vrect(c, 0, 0, W, H, ["#F59E0B", "#FDE68A", "#FEF3C7"])
    c.drawRect(R(0, 0, W, H), P("#F1F5F9", 0.25))
    jtower(c, 820, t, built=BUILT_M / TOP_M, plan=0.0, a=0.35, scale=0.5, cranes=False)
    c.drawRect(R(0, 1060, W, H - 1060), P("#78716C"))
    c.drawRRect(rr(-80, 760, 560, 330, 40), lin_paint(0, 760, 0, 1090, ["#1E3A8A", "#1E40AF"]))   # the car
    c.drawRRect(rr(0, 790, 380, 120, 20), P("#93C5FD", 0.7))
    cx, cy = 600, 600                                 # a big face with glasses
    c.drawCircle(cx, cy, 190, P("#E8B48A"))
    dome = skia.Path()
    dome.moveTo(cx - 195, cy - 40)
    dome.cubicTo(cx - 195, cy - 260, cx + 195, cy - 260, cx + 195, cy - 40)
    dome.close()
    c.drawPath(dome, P("#1F2937"))
    for dx in (-85, 85):
        c.drawRRect(rr(cx + dx - 70, cy - 30, 140, 100, 30), P("#E0F2FE", 0.35 + 0.6 * fog))
        c.drawRRect(rr(cx + dx - 70, cy - 30, 140, 100, 30), P("#111827", 1.0, stroke=10))
        if fog < 0.6:
            c.drawCircle(cx + dx, cy + 20, 14, P("#111827", 1 - fog))
    c.drawLine(cx - 15, cy + 10, cx + 15, cy + 10, P("#111827", 1.0, stroke=10))
    c.drawArc(R(cx - 60, cy + 90, 120, 60), 20, 140, False, P("#7C2D12", 1.0, stroke=8))
    rng = random.Random(4)
    for k in range(int(30 * fog)):                    # droplets on the lenses
        dx = rng.choice((-85, 85)) + rng.uniform(-55, 55)
        c.drawCircle(cx + dx, cy + 20 + rng.uniform(-35, 35), rng.uniform(3, 7), P("#FFFFFF", 0.8 * fog))
    for k in range(6):                                # humid air waving
        u = (t * 0.5 + k / 6) % 1.0
        c.drawArc(R(100 + k * 150, 300 + u * 40, 90, 40), 180, 180, False, P("#FFFFFF", 0.35 * (1 - u), stroke=4))


# ====================================================================================== the episode
class JeddahTower(EpisodeV2):
    BUILD_NO = 100
    FIRST_SET = "sky"
    CLEAR = "#0B0F24"
    TITLE = {"en": "JEDDAH TOWER", "ar_sa": "برج جدة"}
    EMPH = {"en": ["JEDDAH", "TOWER", "THOUSAND", "METERS", "TALL", "SOFT", "ROCK", "SEASHELLS", "HOW", "TWO",
                   "HUNDRED", "SEVENTY", "PILES", "FIVE", "WIND", "TEN", "FASTER", "SKINNIER", "GRAB", "WOBBLE",
                   "PENCIL", "THREE", "WINGS", "TRIPOD", "METAL", "HEAVY", "CARBON", "BELTS", "SIX", "THIRTY",
                   "FOLLOW", "SPRINKLER", "ONE", "HALFWAY", "MALAYSIA'S", "TWIN", "TOWERS", "KILOMETER", "CONGRATS",
                   "YOURSELF", "GLASSES"],
            "ar_sa": ["جدة", "برج", "كيلو", "كامل", "صخر", "لين", "صدف", "طوله", "الحين", "ميتين", "وسبعين", "عمود",
                      "مية", "وخمسة", "الهوا", "بعشر", "أنحف", "يمسكه", "يتمايل", "القلم", "أجنحة", "الستاند", "حبال",
                      "الحديد", "ثقيلة", "كربون", "ستمية", "وثلاثين", "متابعة", "رشاش", "نص", "خمسمية", "بتروناس",
                      "مبروك", "نظارتك", "تغبّش"]}
    KEYS = {"ar_sa": {
        ("hook", "JEDDAH"): "جدة", ("hook", "TOWER"): "برج", ("hook", "THOUSAND"): "كيلو",
        ("break1", "GROUND"): "أرض", ("break1", "SEASHELLS"): "صدف", ("break1", "HOW"): "كم",
        ("fix1", "TWO"): "ميتين", ("fix1", "PILES"): "عمود", ("fix1", "HUNDRED"): "مية",
        ("break2", "UP"): "فوق", ("break2", "FASTER"): "أسرع",
        ("fix2", "SKINNIER"): "أنحف", ("fix2", "GRAB"): "يمسكه",
        ("break3", "SKINNY"): "نحيف", ("break3", "PENCIL"): "القلم",
        ("fix3", "THREE"): "ثلاث", ("fix3", "TRIPOD"): "الستاند",
        ("break4", "METAL"): "الحديد", ("break4", "HEAVY"): "ثقيلة",
        ("fix4", "CARBON"): "كربون", ("fix4", "SIX"): "ستمية",
        ("cta", "FOLLOW"): "متابعة", ("cta", "SPRINKLER"): "رشاش",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "HALFWAY"): "نص", ("reveal", "MALAYSIA'S"): "بتروناس",
        ("stat", "TWO"): "ميتين", ("stat", "THREE"): "ثلاث", ("stat", "KILOMETER"): "وكيلو",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "KILOMETER"): "كيلو", ("tag", "CAR"): "السيارة", ("tag", "GLASSES"): "نظارتك"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a fire sprinkler"),
                   "stat": [("270", "PILES"), ("3", "WINGS"), ("1 KM", "OF TOWER")],
                   "L": {"km": "1,000 METERS TALL", "soft": "SOFT ROCK + SEASHELLS", "how": "HOW TALL IS IT NOW?",
                         "piles": "270 PILES", "deep": "UP TO 105 M DEEP", "breeze": "A BREEZE DOWN HERE",
                         "fast": "10x FASTER UP TOP", "skinny": "SKINNIER AS IT RISES", "grab": "THE WIND CAN'T GRAB IT",
                         "pencil": "WOBBLES LIKE A PENCIL", "wings": "3 WINGS = A TRIPOD", "heavy": "STEEL: WAY TOO HEAVY",
                         "carbon": "LIGHT CARBON BELTS", "m630": "630+ M IN ONE RIDE", "now": "ALMOST HALFWAY: ~500 M",
                         "passed": "PAST THE PETRONAS TOWERS", "name": "THE JEDDAH TOWER", "fog": "JEDDAH HUMIDITY",
                         "fogged": "...FOGGED!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: رشاش الحريق"),
                      "stat": [("270", "عمود"), ("3", "أجنحة"), ("1 KM", "من البرج")],
                      "L": {"km": "طوله كيلو كامل", "soft": "صخر لين مليان صدف", "how": "كم طوله الحين؟",
                            "piles": "270 عمود", "deep": "لين 105 متر تحت", "breeze": "تحت: نسمة",
                            "fast": "فوق: أسرع بعشر مرات", "skinny": "يصير أنحف كل ما طلع", "grab": "الهوا ما يلقى شي يمسكه",
                            "pencil": "يتمايل مثل القلم", "wings": "3 أجنحة = ستاند", "heavy": "الحديد: ثقيل مرة",
                            "carbon": "سيور كربون خفيفة", "m630": "فوق 630 متر", "now": "تقريباً النص: قرب 500 متر",
                            "passed": "عدّى أبراج بتروناس", "name": "برج جدة", "fog": "رطوبة جدة",
                            "fogged": "...تغبّشت!"}}}
    STAT_COLORS = (INK, "#FFB05C", HILITE)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "jeddah": ("hook", "JEDDAH", 0.2), "tower0": ("hook", "TOWER", 0.5), "thousand": ("hook", "THOUSAND", 0.75),
            "ground": ("break1", "GROUND", 0.15), "shells": ("break1", "SEASHELLS", 0.45), "how": ("break1", "HOW", 0.75),
            "two": ("fix1", "TWO", 0.05), "piles": ("fix1", "PILES", 0.4), "deep": ("fix1", "HUNDRED", 0.75),
            "up": ("break2", "UP", 0.1), "faster": ("break2", "FASTER", 0.8),
            "skinnier": ("fix2", "SKINNIER", 0.3), "grab": ("fix2", "GRAB", 0.85),
            "skinny": ("break3", "SKINNY", 0.3), "pencil": ("break3", "PENCIL", 0.85),
            "three": ("fix3", "THREE", 0.1), "tripod": ("fix3", "TRIPOD", 0.85),
            "metal": ("break4", "METAL", 0.15), "heavy": ("break4", "HEAVY", 0.85),
            "carbon": ("fix4", "CARBON", 0.4), "six": ("fix4", "SIX", 0.7),
            "follow": ("cta", "FOLLOW", 0.35),
            "answer": ("reveal", "ANSWER", 0.05), "halfway": ("reveal", "HALFWAY", 0.25), "passed": ("reveal", "MALAYSIA'S", 0.8),
            "s1": ("stat", "TWO", 0.05), "s2": ("stat", "THREE", 0.4), "s3": ("stat", "KILOMETER", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_km": ("tag", "KILOMETER", 0.1), "t_car": ("tag", "CAR", 0.6), "t_glasses": ("tag", "GLASSES", 0.85)})
        T["sink1"] = max(T["shells"], T["ground"]) + 0.2
        T["piles1"] = max(T["deep"], T["piles"]) + 0.1
        T["fast1"] = max(T["faster"], T["up"]) + 0.1
        T["grab1"] = max(T["grab"], T["skinnier"]) + 0.1
        T["wob1"] = max(T["pencil"], T["skinny"]) + 0.1
        T["tri1"] = max(T["tripod"], T["three"]) + 0.1
        T["heavy1"] = max(T["heavy"], T["metal"]) + 0.1
        T["belt1"] = max(T["six"], T["carbon"]) + 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "ground", 1)
        self.cut(s("break2") - 0.12, "wind", -1)
        self.cut(s("break3") - 0.12, "plan", 1)
        self.cut(s("break4") - 0.12, "lift", -1)
        self.cut(s("cta") - 0.12, "sky", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["sink1"], T["piles1"]), (T["fast1"], T["grab1"]), (T["wob1"], T["tri1"]), (T["heavy1"], T["belt1"])]
        self.shakes = [(T["thousand"], 0.3, 5), (T["sink1"], 0.4, 8), (T["fast1"], 0.4, 7), (T["wob1"], 0.3, 6),
                       (T["heavy1"], 0.4, 7), (s("closer") + 0.2, 0.35, 6), (T["t_glasses"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: sky (hook, cta, reveal, stat, closer)
    def draw_sky(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "closer":                            # the finished tower at night
            jeddah_backdrop(c, t, pal=["#020617", "#0B1036", "#1E1B4B", "#3B1F5E"], lights=1.0)
            c.save()
            c.translate(600, GROUND)
            c.scale(1.12, 1.12)
            c.translate(-600, -GROUND)
            jtower(c, 600, t, built=1.0, lit=0.8, cranes=False)
            c.restore()
            for k in range(4):
                u = (t * 0.6 + k / 4) % 1.0
                v2.shock_ring(c, 600 + (k - 1.5) * 200, 420 + k * 60, t, t - u, dur=1.0, r1=180, col="#FDE68A", width=8)
            return
        if ph == "hook":                              # close on the cranes at the top, then out to the whole kilometre
            k = e_io(prog(t, 0.3, T["thousand"] + 0.2))
            yt = GROUND - BUILT_M * M
            cx_, cy_, z = lerp(600, 540, k), lerp(yt + 40, 960, k), lerp(2.3, 1.0, k)
            c.save()
            c.translate(540, 960)
            c.scale(z, z)
            c.translate(-cx_, -cy_)
            jeddah_backdrop(c, t)
            plan = prog(t, T["tower0"] - 0.3, T["thousand"] + 0.5)
            jtower(c, 600, t, built=BUILT_M / TOP_M, plan=plan)
            ruler(c, 900, t, k=prog(t, T["tower0"], T["thousand"] + 0.5))
            c.restore()
            return
        jeddah_backdrop(c, t)
        if ph == "reveal":
            k = prog(t, T["answer"], T["halfway"] + 0.6)
            for x, hm, kind, lab, t0 in ((180, 452, "petronas", "452 M", T["answer"]), (330, 508, "taipei", "508 M", T["halfway"]),
                                         (880, 828, "burj", "828 M", T["halfway"] + 0.3)):
                outline_building(c, x, hm, kind, a=prog(t, t0, t0 + 0.4), label=lab)
            hm = lerp(300, BUILT_M, e_out(k))
            jtower(c, 600, t, built=hm / TOP_M, plan=1.0)
            y = GROUND - hm * M
            c.drawLine(120, y, 1000, y, dash_paint(HILITE, 0.9, w=4, t=t))
            c.drawRRect(rr(640, y - 34, 200, 60, 18), P("#0B1220", 0.9))
            text(c, f"{int(hm)} M", 740, y + 10, 36, HILITE, "Poppins-Black")
            if t > T["passed"]:
                c.drawCircle(180, GROUND - 452 * M - 70, 30, P(GOOD))
                c.drawPath(skia.Path().moveTo(166, GROUND - 452 * M - 70).lineTo(176, GROUND - 452 * M - 60)
                           .lineTo(196, GROUND - 452 * M - 84), P("#FFFFFF", 1.0, stroke=7))
        else:                                         # cta, stat
            jtower(c, 600, t, built=BUILT_M / TOP_M, plan=1.0)

    def ui_sky(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "km", T["thousand"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)
        elif ph == "reveal":
            self.chip(540, 300, "now", T["halfway"] - 0.1, T["passed"] - 0.2, accent=HILITE, size=44)
            self.chip(540, 300, "passed", T["passed"] - 0.2, s("stat") - 0.15, accent=GOOD, size=44)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: ground (break1, fix1)
    def draw_ground(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break1":
            ground_cut(c, t, sink=prog(t, T["sink1"] - 0.2, T["how"] + 0.4))
        else:
            ground_cut(c, t, piles=prog(t, T["two"], T["deep"] + 0.3), raft=prog(t, T["deep"], T["deep"] + 0.5),
                       tower_k=prog(t, T["piles1"] + 0.2, T["piles1"] + 0.8))

    def ui_ground(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "soft", T["ground"] - 0.1, T["how"] - 0.2, accent=WARN, size=46)
            self.chip(540, 300, "how", T["how"] - 0.2, s("fix1") - 0.1, accent=HILITE, size=50)
            self.badge("alert", T["sink1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["sink1"], 1.2)
        else:
            self.chip(540, 300, "piles", T["piles"] - 0.2, T["deep"] - 0.1, accent=GOOD, size=52)
            self.chip(540, 300, "deep", T["deep"] - 0.1, s("break2") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["piles1"], s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: wind (break2, fix2)
    def draw_wind(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        jeddah_backdrop(c, t, pal=["#0C4A6E", "#0369A1", "#7DD3FC"], lights=0.0)
        if ph == "break2":
            k = prog(t, T["up"], T["faster"] + 0.2)
            box_tower(c, 540, t, sway=k)
            wind_streaks(c, t, 1080, 1180, 300, a=0.8, seed=1, n=5, length=40)
            wind_streaks(c, t, 260, 560, 300 + 2700 * k, a=k, seed=2, n=16, length=150)
            for j in range(4):
                u = (t * 0.9 + j / 4) % 1.0
                vortex(c, 620 + u * 420, 330 + j * 70, 40 + 30 * u, t * 4 + j, 1 if j % 2 else -1, 0.8 * k * (1 - u))
        else:
            k = prog(t, s("fix2"), T["skinnier"] + 0.3)
            jtower(c, 540, t, built=1.0, plan=0.0, cranes=False, scale=0.9)
            wind_streaks(c, t, 260, 600, 3000, a=0.7, seed=2, n=16, length=150)
            for j in range(6):                        # streamlines bending smoothly around it
                y = 300 + j * 55
                p = skia.Path()
                p.moveTo(-20, y)
                p.cubicTo(400, y, 470, y - 40 * k, 540, y - 50 * k)
                p.cubicTo(610, y - 40 * k, 680, y, 1100, y)
                c.drawPath(p, P("#E0F2FE", 0.55 * k, stroke=4))

    def ui_wind(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break2":
            self.chip(540, 300, "fast", T["up"] - 0.1, s("fix2") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["fast1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["fast1"], 1.2)
        else:
            self.chip(540, 300, "skinny", T["skinnier"] - 0.2, T["grab"] - 0.1, accent=GOOD, size=48)
            self.chip(540, 300, "grab", T["grab"] - 0.1, s("break3") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["grab1"], s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: plan (break3, fix3)
    def draw_plan(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break3":
            vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
            c.drawRect(R(0, 1120, W, H - 1120), P("#334155"))
            wob = prog(t, T["skinny"], T["pencil"] + 0.3)
            pencil(c, 540, 1120, 560, math.sin(t * 5) * 14 * wob)
        else:
            plan_view(c, t, wings=prog(t, T["three"] - 0.2, T["three"] + 0.8), wob=0.0)
            tripod(c, 880, 1180, 0.9, k=prog(t, T["tripod"] - 0.2, T["tripod"] + 0.3))

    def ui_plan(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "pencil", T["skinny"] - 0.1, s("fix3") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["wob1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["wob1"], 1.2)
        else:
            self.chip(540, 300, "wings", T["three"] - 0.1, s("break4") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["tri1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: lift (break4, fix4)
    def draw_lift(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break4":
            k = prog(t, T["metal"], T["heavy"])
            lift_shaft(c, t, heavy=1.0, strain=prog(t, T["heavy1"] - 0.3, T["heavy1"] + 0.2))
            scale_card(c, 870, 620, k, heavy=True, a=prog(t, T["metal"] - 0.2, T["metal"] + 0.2))
        else:
            lift_shaft(c, t, belt=1.0, rise=prog(t, T["carbon"], T["six"] + 0.6))
            hm = int(630 * e_io(prog(t, T["carbon"], T["six"] + 0.6)))
            c.drawRRect(rr(790, 520, 240, 90, 22), P("#0B1220", 0.9))
            text(c, f"{hm} M", 910, 580, 48, HILITE, "Poppins-Black")

    def ui_lift(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "heavy", T["metal"] - 0.1, s("fix4") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["heavy1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["heavy1"], 1.2)
        else:
            self.chip(540, 300, "carbon", T["carbon"] - 0.2, T["six"] - 0.1, accent=GOOD, size=50)
            self.chip(540, 300, "m630", T["six"] - 0.1, s("cta") - 0.15, accent=HILITE, size=52)
            self.badge("check", T["belt1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        car_door(c, t, fog=prog(t, T["t_car"], T["t_glasses"] + 0.2))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "fog", T["t_km"] - 0.1, T["t_glasses"] - 0.15, accent="#F8FAFC", size=48)
        self.chip(540, 300, "fogged", T["t_glasses"] - 0.15, self.duration + 1, accent=WARN, size=58)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1E1B4B", "#5B21B6"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["tower0"], sfx.riser(1.2, 62), -12),
              (T["thousand"], sfx.sparkle(1.0, 12, 63), -8), (T["thousand"] + 0.3, sfx.ding(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["sink1"], rumble(1.6, 65), -8),
               (T["sink1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 66), -6), (T["piles"], sfx.whirr(1.0, 90.0, 160.0, 67), -12),
               (T["piles1"], sfx.ding(), -8), (T["piles1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, True, 68), -6), (T["up"], sfx.hiss(1.6, 69), -12),
               (T["fast1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.45, False, 70), -6), (T["grab1"], sfx.ding(), -8), (T["grab1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 71), -6), (T["wob1"], sfx.creak(0.8, 72), -8),
               (T["wob1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, False, 73), -6), (T["three"], sfx.pop(74), -6),
               (T["tri1"], sfx.ding(), -8), (T["tri1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 75), -6), (T["heavy"], sfx.clank(260.0, 0.7, 76), -6),
               (T["heavy1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.45, False, 77), -6), (T["carbon"], sfx.whirr(1.4, 160.0, 420.0, 78), -10),
               (T["belt1"], sfx.ding(), -8), (T["belt1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["halfway"], sfx.riser(0.9, 95), -12),
               (T["passed"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(s("closer") - 0.12, sfx.whoosh(0.45, False, 96), -6), (T["cong2"], sfx.pop(101), -2),
               (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 103), -6), (T["t_car"], sfx.click(104), -6),
               (T["t_glasses"], sfx.hiss(0.6, 105), -12), (T["t_glasses"] + 0.3, sfx.womp(), -8)]
        return ev


NAME = "jeddahtower"
EPISODE = JeddahTower
