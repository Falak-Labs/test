"""Episode 69 - A dishwasher.  v2 look: a built-in dishwasher under a kitchen counter, shown in x-ray with its two
racks, two spray arms, the sump with its puddle, the filter, the pump and the heater.

Sets: kitchen (hook: close on the lower rack in x-ray, jets blasting from a spinning arm, a hand pulled back from the
hot spray, a thermometer passing 60 C; out to the whole kitchen; stat by day; closer: evening, the door opens on
clean plates and steam), sink (break1: a sink under a running tap, a litre meter counting up to 100 and water
pouring down the drain), box (fix1: x-ray, a small puddle in the sump, the pump throwing it up to the arms again and
again; break2: the puddle clouds with food scraps; fix2: the filter catches them, clean water goes up), arms (break3:
top view, one fixed nozzle cleans one spot of a dirty plate; fix3: an arm with angled holes spun by its own jets,
reaction arrows, a garden sprinkler inset), enzyme (break4: a magnified plate, dried egg and baked cheese, water drops
bouncing off; fix4: enzymes chopping protein and starch chains), old (reveal: 1886, a maid chips the fine china, then
Josephine Cochrane's copper machine with its wire wheel and crank; a hotel), tag (mom washing every plate at the sink
before it goes into the open machine; AR: the machine is her drying rack).
World: front view, the floor at y = 0, the machine 600 x 850 units (1 cm = 10 units) under a counter at y = -870.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of  # noqa: E402
from bigben import thermometer  # noqa: E402
from phone import bubble, mom  # noqa: E402
from evcar import dash_line  # noqa: E402

DW, DH = 600.0, 850.0
CTOP = -870.0                                   # counter top (world)
WATER = "#60A5FA"
STEEL = ("#E2E8F0", "#CBD5E1", "#94A3B8", "#64748B")
DIRT = "#8B5E34"
PLATE_COLS = ("#9AA8B8", "#86A6C2", "#B9A574", "#9AA8B8", "#B98FA4")


def kitchen(c, t, night=0.0, a=1.0):
    """Wall, backsplash tiles, cabinets on both sides of the machine, counter, wall cupboards, floor (world)."""
    wall = mix("#33507A", "#1C2742", night)
    c.drawRect(R(-2200, -2400, 4400, 2400), lin_paint(0, -2400, 0, 0, [shade(wall, 0.08), wall]))
    for k in range(-22, 23):                                            # backsplash tiles between counter and cupboards
        c.drawLine(k * 90, -1380, k * 90, CTOP, P("#C7D7EA", 0.12, stroke=2))
    for k in range(6):
        c.drawLine(-2200, CTOP - 20 - k * 90, 2200, CTOP - 20 - k * 90, P("#C7D7EA", 0.12, stroke=2))
    add_glow(c, 0, -1100, 800, "#FDE68A", 0.10 * (1 - night) + 0.06)
    wood = mix("#8A5A36", "#4A3020", night)
    for x0 in (-2200, DW / 2):                                          # base cabinets left and right
        x1 = -DW / 2 if x0 < 0 else 2200
        c.drawRect(R(x0, CTOP + 30, x1 - x0, -CTOP - 30), lin_paint(0, CTOP, 0, 0, [shade(wood, 0.1), shade(wood, -0.15)]))
        k0 = int(x0 // 450)
        for k in range(k0, k0 + 6):
            xx = k * 450 + 20
            if x0 <= xx and xx + 410 <= x1:
                c.drawRRect(rr(xx, CTOP + 60, 410, -CTOP - 90, 10), P(shade(wood, 0.06)))
                c.drawRRect(rr(xx, CTOP + 60, 410, -CTOP - 90, 10), P(shade(wood, -0.3), 0.8, stroke=4))
                c.drawRRect(rr(xx + 180, CTOP + 110, 50, 12, 6), P("#D1D5DB"))
    c.drawRect(R(-2200, CTOP, 4400, 36), lin_paint(0, CTOP, 0, CTOP + 36, ["#E7E5E4", "#A8A29E"]))   # counter top
    c.drawRect(R(-2200, -2400, 4400, 900), P(shade(wood, 0.05)))      # wall cupboards
    for k in range(-5, 5):
        c.drawRRect(rr(k * 450 + 20, -2380, 410, 860, 12), P(shade(wood, 0.12)))
        c.drawRRect(rr(k * 450 + 20, -2380, 410, 860, 12), P(shade(wood, -0.3), 0.8, stroke=4))
    floor = mix("#3B3F4E", "#1E2130", night)
    c.drawRect(R(-2200, 0, 4400, 1400), lin_paint(0, 0, 0, 800, [floor, shade(floor, -0.35)]))
    for k in range(-14, 15):
        c.drawLine(k * 180, 0, k * 260, 800, P("#9CA3AF", 0.10, stroke=2))


def plate_disc(c, x, y, r, col="#F8FAFC", dirt=0.0, a=1.0, seed=0):
    """A plate standing in the rack, face to us."""
    c.drawCircle(x, y, r, P(shade(col, -0.3), a))
    c.drawCircle(x, y, r * 0.92, P(col, a))
    c.drawCircle(x, y, r * 0.62, P(shade(col, -0.15), a, stroke=4))
    if dirt > 0:
        rng = random.Random(seed)
        for _ in range(6):
            c.drawCircle(x + rng.uniform(-0.5, 0.5) * r, y + rng.uniform(-0.5, 0.5) * r, rng.uniform(0.08, 0.2) * r,
                         P(rng.choice((DIRT, "#D97706", "#B45309")), 0.85 * dirt * a))


def cup_down(c, x, y, s, col, a=1.0):
    """A cup upside down on the upper rack (its rim on the wires at y)."""
    c.drawPath(path_of([(x - 34 * s, y), (x - 28 * s, y - 70 * s), (x + 28 * s, y - 70 * s), (x + 34 * s, y)], close=True),
               P(col, a))
    c.drawPath(path_of([(x + 30 * s, y - 52 * s), (x + 52 * s, y - 46 * s), (x + 50 * s, y - 20 * s), (x + 33 * s, y - 16 * s)]),
               P(shade(col, -0.15), a, stroke=7 * s))


def glass_down(c, x, y, s, a=1.0):
    c.drawPath(path_of([(x - 24 * s, y), (x - 20 * s, y - 84 * s), (x + 20 * s, y - 84 * s), (x + 24 * s, y)], close=True),
               P("#BFDBFE", 0.45 * a))
    c.drawLine(x - 12 * s, y - 70 * s, x - 10 * s, y - 14 * s, P("#FFFFFF", 0.6 * a, stroke=4))


def rack(c, x0, x1, y, depth=26, a=1.0):
    """Wire rack seen from the front: a rail and a row of tines."""
    c.drawLine(x0, y, x1, y, P("#94A3B8", a, stroke=7))
    c.drawLine(x0, y + depth, x1, y + depth, P("#64748B", a, stroke=5))
    for k in range(int((x1 - x0) / 26) + 1):
        xx = x0 + k * 26
        c.drawLine(xx, y + depth, xx, y - 40, P("#94A3B8", 0.55 * a, stroke=3))
    for wx in (x0 + 40, x1 - 40):
        c.drawCircle(wx, y + depth + 8, 9, P("#475569", a))


def spray_arm(c, x, y, L, ang, t, jets=1.0, up=1.0, a=1.0, hot=0.0, mist=1.0):
    """A spray arm turning about a vertical axis, front view: foreshortened bar, hub, jets fanning up (up = 1) or down."""
    k = math.cos(math.radians(ang))
    hx = L * k
    c.drawLine(x - hx, y, x + hx, y, P("#CBD5E1", a, stroke=20))
    c.drawLine(x - hx, y - 3, x + hx, y - 3, P("#F1F5F9", a, stroke=6))
    c.drawRRect(rr(x - 20, y - 14, 40, 28, 8), P("#94A3B8", a))
    if jets <= 0:
        return
    col = mix(WATER, "#FFFFFF", 0.35 + 0.3 * hot)
    for i in range(-3, 4):
        if i == 0:
            continue
        f = i / 3.0
        px = x + hx * f
        for j in range(2):
            q = (t * 3.1 + i * 0.37 + j * 0.5) % 1.0
            tilt = (1 if i > 0 else -1) * 14 * abs(k) + 20 * math.sin(math.radians(ang) + i)
            ln = 130 + 90 * j
            x1, y1 = px + tilt * (0.5 + q), y - up * ln * (0.6 + 0.4 * q)
            c.drawLine(px, y - up * 8, x1, y1, P(col, 0.65 * jets * a * (1 - 0.6 * q), stroke=5 - j * 2))
            if mist > 0:
                c.drawCircle(x1, y1, 4 + 3 * j, P("#E0F2FE", 0.4 * jets * a * mist))


def machine(c, t, xray=0.0, door=0.0, ang=0.0, jets=0.0, water=0.0, scraps=0.0, filt=0.0, pump=0.0, steam=0.0,
            hot=0.0, dirt=0.0, sparkle=0.0, lit=0.0, display="1:12", run=1.0, flow=0.0, a=1.0):
    """The dishwasher at x = 0 standing on y = 0 (world). xray 0..1 opens the front; ang = spray arm angle (degrees);
    jets 0..1 the spray; water 0..1 the sump puddle; scraps 0..1 food bits in it; filt 0..1 the filter catching them;
    flow 0..1 water running up the pipe from the pump; door 0..1 the door folded down (an open machine)."""
    if a <= 0:
        return
    c.save()
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    contact_shadow(c, 0, 0, DW * 1.02, 0.4, 22)
    x0, x1 = -DW / 2, DW / 2
    y0 = -DH
    c.drawRect(R(x0, y0, DW, DH), P("#1E293B"))                                     # the opening
    if xray > 0 or door > 0:
        k = max(xray, door)
        c.drawRect(R(x0 + 14, y0 + 90, DW - 28, DH - 110), lin_paint(x0, 0, x1, 0, ["#334155", "#475569", "#334155"], a=k))
        c.drawRect(R(x0 + 14, y0 + 90, DW - 28, DH - 110), P("#94A3B8", k, stroke=5))
        # pipe from the pump up the back to the two arms
        c.drawLine(x1 - 60, -40, x1 - 60, -470, P("#64748B", k, stroke=18))
        c.drawLine(x1 - 60, -470, 0, -470, P("#64748B", k, stroke=12))
        c.drawLine(x1 - 60, -110, 0, -110, P("#64748B", k, stroke=12))
        if flow > 0:
            dash_line(c, [(x1 - 50, -40), (x1 - 50, -470), (0, -470)], t, "#93C5FD", a=flow * k, w=8)
            dash_line(c, [(x1 - 50, -110), (0, -110)], t, "#93C5FD", a=flow * k, w=8)
        # sump: puddle, filter, heater, pump
        sx0, sx1 = x0 + 30, x1 - 30
        c.drawRect(R(sx0, -70, sx1 - sx0, 54), P("#0F172A", k))
        if water > 0:
            wl = -18 - 44 * water
            wp = [(xx, wl + math.sin(xx * 0.05 + t * 7) * 3) for xx in range(int(sx0), int(sx1) + 1, 12)]
            wcol = mix(WATER, "#8B6B45", 0.55 * scraps * (1 - filt))
            c.drawPath(path_of(wp + [(sx1, -16), (sx0, -16)], close=True), P(wcol, 0.85 * k))
            if scraps > 0:
                rng = random.Random(7)
                for i in range(28):
                    px = rng.uniform(sx0 + 10, sx1 - 10)
                    py = rng.uniform(wl + 4, -20)
                    if filt > 0:                                         # drawn into the filter in the middle
                        px = lerp(px, rng.uniform(-36, 36), e_io(clamp(filt * 1.3 - i * 0.01)))
                        py = lerp(py, rng.uniform(-60, -26), e_io(clamp(filt * 1.3 - i * 0.01)))
                    c.drawCircle(px, py, rng.uniform(4, 8), P(rng.choice((DIRT, "#A16207", "#65A30D")), scraps * k))
        c.drawRRect(rr(-48, -76, 96, 62, 10), P("#CBD5E1", 0.25 * k + 0.6 * k * filt))      # the filter cup
        for i in range(7):
            c.drawLine(-44 + i * 14.6, -74, -44 + i * 14.6, -16, P("#E2E8F0", (0.35 + 0.5 * filt) * k, stroke=2))
        for i in range(4):
            c.drawLine(-46, -70 + i * 16, 46, -70 + i * 16, P("#E2E8F0", (0.35 + 0.5 * filt) * k, stroke=2))
        hp = skia.Path()                                                  # heating element loop
        hp.moveTo(sx0 + 30, -22)
        hp.lineTo(-80, -22)
        hp.moveTo(80, -22)
        hp.lineTo(sx1 - 120, -22)
        c.drawPath(hp, P(mix("#78716C", "#F97316", hot), k, stroke=8))
        if hot > 0:
            add_glow(c, -150, -22, 60, "#F97316", 0.4 * hot * k)
            add_glow(c, 150, -22, 60, "#F97316", 0.3 * hot * k)
        c.drawRRect(rr(x1 - 120, -64, 80, 56, 12), P("#475569", k))       # pump
        c.drawCircle(x1 - 80, -36, 18, P("#94A3B8", k))
        q = math.radians(t * 900 * pump)
        c.drawLine(x1 - 80, -36, x1 - 80 + 14 * math.cos(q), -36 + 14 * math.sin(q), P("#1E293B", k, stroke=4))
        # lower rack with plates, upper rack with cups and glasses
        rack(c, x0 + 40, x1 - 40, -140, a=k)
        for i in range(5):
            plate_disc(c, -200 + i * 100, -230 - (i % 2) * 6, 88, PLATE_COLS[i], dirt=dirt, a=k, seed=i)
        rack(c, x0 + 40, x1 - 40, -500, a=k)
        for i, xx in enumerate((-200, -110, -20, 70, 160, 220)):
            if i % 2 == 0:
                cup_down(c, xx, -506, 1.0, ("#F87171", "#60A5FA", "#FBBF24")[i // 2], a=k)
            else:
                glass_down(c, xx, -506, 1.0, a=k)
        spray_arm(c, 0, -110, 240, ang, t, jets=jets * k, up=1.0, a=k, hot=hot)
        spray_arm(c, 0, -470, 200, ang * 1.3 + 40, t + 0.3, jets=jets * k, up=1.0, a=k, hot=hot)
        if sparkle > 0:
            for i in range(5):
                q_ = (t * 1.5 + i * 0.37) % 1.0
                add_glow(c, -200 + i * 100 + 30, -270 + 30 * q_, 18 + 10 * math.sin(t * 6 + i), "#FFFFFF", sparkle * k * 0.8)
    if steam > 0:
        for i in range(7):
            q = (t * 0.35 + i * 0.143) % 1.0
            puff(c, -220 + i * 74 + 30 * math.sin(t + i), y0 + 120 - q * 360, 50 + 50 * q, "#E2E8F0", 0.35 * steam * (1 - q), k=i)
    # the door: closed front (fades for x-ray) or folded down in front (open)
    fk = (1 - xray) * (1 - door)
    if fk > 0:
        c.drawRect(R(x0, y0, DW, DH), lin_paint(x0, 0, x1, 0, ["#8A94A3", mix("#B4BDC9", "#FFF3DC", 0.3 * lit), "#9AA4B2",
                                                                "#6B7685"], a=fk))
        c.drawRect(R(x0, y0, DW, 84), P("#111827", fk))
        c.drawRRect(rr(x0 + 40, y0 + 22, 150, 40, 10), P("#0B1220", fk))
        text(c, display, x0 + 115, y0 + 54, 30, "#34D399" if run > 0.5 else "#64748B", "Poppins-Black", align="center", a=fk)
        for i in range(4):
            c.drawCircle(x0 + 260 + i * 70, y0 + 42, 12, P("#374151", fk))
        c.drawRRect(rr(-180, y0 + 104, 360, 22, 11), P("#9CA3AF", fk))
        c.drawRRect(rr(-180, y0 + 104, 360, 22, 11), P("#F8FAFC", 0.5 * fk, stroke=3))
        c.drawRect(R(x0, -60, DW, 60), P("#1F2937", fk))                # kick plate
        c.drawLine(x0 + 120, y0 + 150, x0 + 60, -80, P("#FFFFFF", 0.12 * fk, stroke=26))
    if door > 0:                                                           # the door folded down toward us
        c.drawRect(R(x0, -60, DW, 60 * door), P(STEEL[2]))
        c.drawRect(R(x0 + 6, -56, DW - 12, 52 * door), P("#475569"))
    if a < 1:
        c.restore()
    c.restore()


def sink(c, t, meter=0.0, run=1.0, pile=1.0, a=1.0):
    """A kitchen sink (world: counter at y = CTOP), a running tap, a pile of dishes, water pouring to the drain."""
    wood = "#8A5A36"
    c.drawRect(R(-300, CTOP + 30, 600, -CTOP - 30), lin_paint(0, CTOP, 0, 0, [shade(wood, 0.1), shade(wood, -0.15)], a=a))
    for xx in (-280, 10):
        c.drawRRect(rr(xx, CTOP + 330, 270, -CTOP - 360, 10), P(shade(wood, 0.06), a))
        c.drawRRect(rr(xx, CTOP + 330, 270, -CTOP - 360, 10), P(shade(wood, -0.3), 0.8 * a, stroke=4))
    c.drawRRect(rr(-420, CTOP - 4, 840, 300, 30), P("#94A3B8", a))
    c.drawRRect(rr(-390, CTOP + 10, 780, 260, 26), lin_paint(0, CTOP, 0, CTOP + 270, ["#475569", "#334155"], a=a))
    c.drawCircle(0, CTOP + 236, 22, P("#1E293B", a))
    c.drawCircle(0, CTOP + 236, 22, P("#CBD5E1", a, stroke=4))
    # tap
    c.drawRRect(rr(-30, CTOP - 260, 60, 260, 20), P("#CBD5E1", a))
    c.drawPath(path_of([(-14, CTOP - 250), (-14, CTOP - 330), (150, CTOP - 330), (150, CTOP - 280)]), P("#E2E8F0", a, stroke=34))
    if run > 0:
        for i in range(3):
            c.drawLine(150 + (i - 1) * 7, CTOP - 270, 150 + (i - 1) * 7 + math.sin(t * 9 + i) * 3, CTOP + 200,
                       P(WATER, 0.6 * run * a, stroke=10 - i * 2))
        for i in range(10):
            q = (t * 1.4 + i * 0.1) % 1.0
            c.drawCircle(lerp(140, 10, q), CTOP + 225 + math.sin(q * 6) * 6, 10 * (1 - q) + 4, P("#93C5FD", 0.6 * run * a))
    for i in range(int(6 * pile)):                                         # dishes stacked in the sink
        plate_disc(c, -230 + (i % 3) * 70, CTOP + 170 - i * 22, 90, PLATE_COLS[i % 5], dirt=1.0, a=a, seed=i + 3)
    if meter > 0:                                                          # a litre counter on the wall
        c.drawRRect(rr(190, -1310, 300, 170, 24), P("#0F172A", 0.92 * a * clamp(meter * 4)))
        text(c, f"{int(round(100 * meter))} L", 340, -1196, 86, WARN if meter > 0.8 else "#93C5FD", "Poppins-Black",
             a=a * clamp(meter * 4))


def arm_top(c, cx, cy, L, ang, t, jets=1.0, a=1.0, fixed=False, push=0.0):
    """Top view of a spray arm (two blades) turning about its hub, jets leaving at an angle from the holes."""
    q = math.radians(ang)
    ux, uy = math.cos(q), math.sin(q)
    c.drawLine(cx - ux * L, cy - uy * L, cx + ux * L, cy + uy * L, P("#CBD5E1", a, stroke=46))
    c.drawLine(cx - ux * L, cy - uy * L, cx + ux * L, cy + uy * L, P("#F1F5F9", a, stroke=16))
    c.drawCircle(cx, cy, 40, P("#94A3B8", a))
    c.drawCircle(cx, cy, 14, P("#475569", a))
    for side in (-1, 1):
        for i in range(1, 4):
            d = side * L * i / 3.6
            hx, hy = cx + ux * d, cy + uy * d
            c.drawCircle(hx, hy, 8, P("#1E293B", a))
            if jets > 0:                                                   # jets leave sideways (tangent), the arm goes back
                tx, ty = -uy * side, ux * side
                for j in range(3):
                    f = (t * 4 + i * 0.3 + j * 0.33) % 1.0
                    c.drawLine(hx + tx * (20 + 120 * f), hy + ty * (20 + 120 * f), hx + tx * (50 + 120 * f) + ux * 8,
                               hy + ty * (50 + 120 * f) + uy * 8, P("#93C5FD", 0.8 * jets * a * (1 - f), stroke=8))
                if push > 0 and i == 3:
                    arrow(c, hx, hy, hx - tx * 120, hy - ty * 120, HILITE, a=push * a, w=10, head=30)


def sprinkler(c, x, y, s, ang, t, a=1.0):
    """A garden sprinkler on grass (screen space), two arms spinning, water arcs."""
    c.drawOval(R(x - 230 * s, y - 40 * s, 460 * s, 120 * s), P("#16A34A", a))
    c.drawRect(R(x - 8 * s, y - 70 * s, 16 * s, 70 * s), P("#64748B", a))
    q = math.radians(ang)
    for side in (-1, 1):
        ex, ey = x + math.cos(q) * 90 * s * side, y - 70 * s + math.sin(q) * 20 * s * side
        c.drawLine(x, y - 70 * s, ex, ey, P("#F97316", a, stroke=10 * s))
        for j in range(5):
            f = (t * 2 + j * 0.2) % 1.0
            px = ex + side * f * 150 * s
            py = ey - math.sin(f * math.pi) * 120 * s
            c.drawCircle(px, py, 6 * s, P("#93C5FD", a * (1 - f * 0.5)))


def chain(c, x0, y0, n, step, t, col, cuts=(), cut_k=0.0, a=1.0, hexes=False, seed=0):
    """A molecule chain of beads; cut positions drift apart as cut_k grows."""
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        off = sum(1 for cpos in cuts if i > cpos) * 40 * cut_k
        pts.append((x0 + i * step + off, y0 + math.sin(i * 0.9 + t * 1.5) * 10 + rng.uniform(-3, 3) +
                    sum(1 for cpos in cuts if i > cpos) * 18 * cut_k * (1 if i % 2 else -1)))
    for i in range(n - 1):
        if any(i == cpos for cpos in cuts) and cut_k > 0.15:
            continue
        c.drawLine(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], P(shade(col, -0.25), a, stroke=9))
    for (px, py) in pts:
        if hexes:
            c.drawPath(path_of([(px + 24 * math.cos(math.radians(60 * k)), py + 24 * math.sin(math.radians(60 * k)))
                                for k in range(6)], close=True), P(col, a))
        else:
            c.drawCircle(px, py, 22, P(col, a))
            c.drawCircle(px - 7, py - 7, 7, P("#FFFFFF", 0.5 * a))


def enzyme(c, x, y, s, bite, col, a=1.0, face=1):
    """A cartoon enzyme: a round body with a jaw that opens and closes."""
    m = 30 + 25 * bite
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    p_ = skia.Path()
    p_.addArc(R(-50, -50, 100, 100), m, 360 - 2 * m)
    p_.lineTo(0, 0)
    p_.close()
    c.drawPath(p_, P(col, a))
    c.drawCircle(-6, -26, 8, P("#FFFFFF", a))
    c.drawCircle(-4, -26, 4, P("#111827", a))
    c.restore()


def maid(c, x, y, h, t, a=1.0, carry=1.0):
    person(c, x, y, h, "#1F2937", t, pose="carry" if carry > 0.5 else "stand", face=1, hair="#3F2A1A", a=a)
    u = h / 140.0
    c.drawRRect(rr(x - 18 * u, y - 70 * u, 36 * u, 46 * u, 6 * u), P("#F8FAFC", 0.95 * a))     # apron


def lady(c, x, y, h, t, a=1.0, crank=0.0):
    """Josephine Cochrane in a long 1880s dress, turning a crank (screen/world units: feet at (x, y))."""
    u = h / 140.0
    c.drawPath(path_of([(x - 16 * u, y - 80 * u), (x + 16 * u, y - 80 * u), (x + 46 * u, y), (x - 46 * u, y)], close=True),
               P("#7C2D12", a))
    person(c, x, y - 2 * u, h, "#7C2D12", t, pose="carry" if crank > 0 else "stand", face=1, hair="#2A1A10", a=a)
    c.drawCircle(x - 2 * u, y - 146 * u, 13 * u, P("#2A1A10", a))                                # hair bun


def old_machine(c, x, y, s, t, crank=0.0, a=1.0):
    """Cochrane's machine: a copper boiler on legs, a wire wheel of plates inside (cut open), a crank."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for lx in (-150, 150):
        c.drawLine(lx, 0, lx * 0.85, -140, P("#44403C", a, stroke=14))
    c.drawRRect(rr(-190, -460, 380, 330, 40), lin_paint(-190, 0, 190, 0, ["#9A3412", "#EA580C", "#C2410C", "#7C2D12"], a=a))
    for k in range(4):
        c.drawLine(-190, -430 + k * 80, 190, -430 + k * 80, P("#431407", 0.5 * a, stroke=5))
    c.drawCircle(0, -295, 130, P("#1C1917", 0.85 * a))                                         # cut-open window
    ang = t * 120 * crank
    for k in range(8):                                                                          # the wire wheel of plates
        q = math.radians(ang + k * 45)
        px, py = math.cos(q) * 82, -295 + math.sin(q) * 82
        c.drawLine(0, -295, px, py, P("#A8A29E", a, stroke=3))
        c.drawCircle(px, py, 30, P("#F5F5F4", a))
        c.drawCircle(px, py, 20, P("#E7E5E4", a, stroke=3))
    for k in range(6):
        f = (t * 2.2 + k * 0.17) % 1.0
        c.drawLine(-90 + k * 36, -170, -90 + k * 36 + 10, -170 - f * 160, P("#BFDBFE", 0.6 * a * (1 - f) * crank, stroke=5))
    q = math.radians(t * 220 * crank)                                                           # crank handle
    c.drawCircle(200, -300, 14, P("#57534E", a))
    hx, hy = 200 + math.cos(q) * 60, -300 + math.sin(q) * 60
    c.drawLine(200, -300, hx, hy, P("#57534E", a, stroke=12))
    c.drawLine(hx, hy, hx + 30, hy, P("#292524", a, stroke=16))
    c.restore()


def hotel(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(R(-160, -420, 320, 420), P("#78350F", a))
    for r_ in range(5):
        for k in range(4):
            c.drawRect(R(-130 + k * 70, -390 + r_ * 70, 40, 46), P("#FDE68A", 0.85 * a))
    c.drawRect(R(-180, -460, 360, 50), P("#451A03", a))
    text(c, "HOTEL", 0, -420, 40, "#FDE68A", "Poppins-Black", a=a)
    c.restore()


# ====================================================================================== the episode
class Dishwasher(EpisodeV2):
    BUILD_NO = 69
    FIRST_SET = "kitchen"
    CLEAR = "#111827"
    TITLE = {"en": "DISHWASHER", "ar_sa": "غسالة صحون"}
    EMPH = {"en": ["CONGRATS", "BLAST", "DISHES", "HOT", "HANDS", "ARMS", "SPIN", "MOTOR", "DISHWASHER", "YOURSELF",
                   "DINNER", "HAND", "HUNDRED", "LITERS", "DRAIN", "BOX", "FEW", "BOTTOM", "PUMP", "AGAIN", "FOOD",
                   "SCRAPS", "FAST", "FILTER", "CLEAN", "JET", "FIXED", "NOZZLE", "SPOT", "ANGLED", "HOLES", "PUSH",
                   "JETS", "SPINS", "GARDEN", "SPRINKLER", "DRIED", "EGG", "CHEESE", "LAUGH", "ENZYMES", "CHOP",
                   "STARCH", "BODY", "FOLLOW", "DOME", "ABU", "DHABI", "RAINS", "LIGHT", "JOSEPHINE", "COCHRANE",
                   "SERVANTS", "CHIPPING", "CHINA", "HOTELS", "TWELVE", "SIXTY", "CENTURY", "MOM", "PLATE"],
            "ar_sa": ["مبروك", "تغسل", "الصحون", "حارة", "يدك", "أذرع", "تلف", "موتور", "غسالة", "صحون", "بيدك",
                      "عزيمة", "باليد", "مية", "لتر", "صندوق", "تحت", "ومضخة", "مرة", "تمتلي", "بقايا", "بسرعة",
                      "ففلتر", "البقايا", "النظيفة", "ترجع", "رشاش", "ثابت", "مكان", "خروم", "مايلة", "ودفّة", "تلفها",
                      "الحديقة", "البيض", "الناشف", "والجبن", "المحروق", "إنزيمات", "تقطّع", "والنشا", "جسمك",
                      "تابعني", "قبة", "أبوظبي", "نور", "جوزفين", "كوكرين", "الخدم", "صحونها", "الفنادق", "اثنعش",
                      "ستين", "وأمك", "نشّافة", "بيدها"]}
    KEYS = {"ar_sa": {
        ("hook", "BLAST"): "تغسل", ("hook", "HOT"): "حارة", ("hook", "HANDS"): "يدك", ("hook", "ARMS"): "أذرع",
        ("hook", "SPIN"): "تلف", ("hook", "MOTOR"): "موتور", ("hook", "CONGRATS"): "مبروك", ("hook", "DISHWASHER"): "غسالة",
        ("break1", "DINNER"): "عزيمة", ("break1", "HAND"): "باليد", ("break1", "HUNDRED"): "مية", ("break1", "DRAIN"): "لتر",
        ("fix1", "BOX"): "صندوق", ("fix1", "FEW"): "لتر", ("fix1", "BOTTOM"): "تحت", ("fix1", "PUMP"): "مضخة",
        ("fix1", "AGAIN"): "مرة",
        ("break2", "FILLS"): "تمتلي", ("break2", "SCRAPS"): "بقايا", ("break2", "FAST"): "بسرعة",
        ("fix2", "FILTER"): "فلتر", ("fix2", "SCRAPS"): "البقايا", ("fix2", "CLEAN"): "النظيفة", ("fix2", "BACK"): "ترجع",
        ("break3", "JET"): "رشاش", ("break3", "FIXED"): "ثابت", ("break3", "SPOT"): "مكان",
        ("fix3", "SHOOTS"): "تطلع", ("fix3", "ARMS"): "أذرع", ("fix3", "ANGLED"): "مايلة", ("fix3", "PUSH"): "دفة",
        ("fix3", "SPINS"): "تلفها", ("fix3", "GARDEN"): "الحديقة",
        ("break4", "EGG"): "البيض", ("break4", "CHEESE"): "الجبن", ("break4", "LAUGH"): "يهمهم", ("break4", "WATER"): "الموية",
        ("fix4", "ENZYMES"): "إنزيمات", ("fix4", "CHOP"): "تقطع", ("fix4", "EGG"): "البيض", ("fix4", "STARCH"): "النشا",
        ("fix4", "BODY"): "جسمك",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "EIGHTEEN"): "ألف", ("reveal", "JOSEPHINE"): "جوزفين", ("reveal", "SERVANTS"): "الخدم",
        ("reveal", "CHIPPING"): "يكسرون", ("reveal", "BUILT"): "فسوت", ("reveal", "HOTELS"): "الفنادق",
        ("stat", "TWELVE"): "اثنعش", ("stat", "SIXTY"): "ستين", ("stat", "HUNDRED"): "مية",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CENTURY"): "سنة", ("tag", "MOM"): "أمك", ("tag", "WASHES"): "تغسل", ("tag", "PLATE"): "نشافة",
        ("tag", "GOES"): "بيدها"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a dome that rains light"),
                   "stat": [("12 L", "A LOAD"), ("60°C", "HOT WATER"), ("100 L", "BY HAND")],
                   "L": {"hot": "TOO HOT FOR HANDS", "nomotor": "NO MOTOR IN THE ARMS", "name": "A DISHWASHER",
                         "sink": "UP TO 100 L BY HAND", "few": "JUST A FEW LITERS", "pump": "PUMP",
                         "again": "AGAIN AND AGAIN", "scraps": "FOOD SCRAPS", "filter": "FILTER", "clean": "CLEAN WATER UP",
                         "spot": "ONE SPOT ONLY", "angled": "ANGLED HOLES", "push": "THE JETS PUSH IT ROUND",
                         "sprinkler": "LIKE A SPRINKLER", "egg": "DRIED EGG", "cheese": "BAKED-ON CHEESE",
                         "nope": "WATER ALONE: NOPE", "enz": "ENZYMES", "chop": "CHOP PROTEIN + STARCH",
                         "body": "LIKE THE ONES IN YOUR BODY", "jo": "1886: JOSEPHINE COCHRANE", "chip": "CHIPPED CHINA",
                         "hotels": "HOTELS BOUGHT IT FIRST", "why": "BEFORE IT GOES IN..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: قبة تمطر نور"),
                      "stat": [("12", "لتر للغسلة"), ("60°", "درجة"), ("100", "لتر باليد")],
                      "L": {"hot": "حارة على يدك", "nomotor": "تلف بدون موتور", "name": "غسالة صحون",
                            "sink": "لين مية لتر باليد", "few": "كم لتر بس", "pump": "مضخة",
                            "again": "مرة ورا مرة", "scraps": "بقايا أكل", "filter": "فلتر", "clean": "النظيفة ترجع فوق",
                            "spot": "مكان واحد بس", "angled": "خروم مايلة", "push": "دفّة الموية تلفها",
                            "sprinkler": "مثل رشاش الحديقة", "egg": "بيض ناشف", "cheese": "جبن محروق",
                            "nope": "الموية لحالها: لا", "enz": "إنزيمات", "chop": "تقطّع البيض والنشا",
                            "body": "مثل اللي في جسمك", "jo": "جوزفين كوكرين", "chip": "صحون مكسورة",
                            "hotels": "اشترتها الفنادق", "why": "نشّافة!"}}}
    COVER_T = ("closer", 0.6)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "blast": ("hook", "BLAST", 0.05), "hot": ("hook", "HOT", 0.25), "hands": ("hook", "HANDS", 0.35),
            "arms": ("hook", "ARMS", 0.45), "spin": ("hook", "SPIN", 0.55), "motor": ("hook", "MOTOR", 0.62),
            "congrats": ("hook", "CONGRATS", 0.75), "name": ("hook", "DISHWASHER", 0.92),
            "dinner": ("break1", "DINNER", 0.2), "hand": ("break1", "HAND", 0.4), "hundred": ("break1", "HUNDRED", 0.6),
            "drain": ("break1", "DRAIN", 0.9),
            "box": ("fix1", "BOX", 0.15), "few": ("fix1", "FEW", 0.3), "bottom": ("fix1", "BOTTOM", 0.45),
            "pump": ("fix1", "PUMP", 0.6), "again": ("fix1", "AGAIN", 0.85),
            "fills": ("break2", "FILLS", 0.3), "scraps": ("break2", "SCRAPS", 0.6), "fast": ("break2", "FAST", 0.9),
            "filter": ("fix2", "FILTER", 0.15), "scraps2": ("fix2", "SCRAPS", 0.4), "clean": ("fix2", "CLEAN", 0.7),
            "back": ("fix2", "BACK", 0.9),
            "jet": ("break3", "JET", 0.15), "fixed": ("break3", "FIXED", 0.4), "spot": ("break3", "SPOT", 0.9),
            "shoots": ("fix3", "SHOOTS", 0.1), "arms3": ("fix3", "ARMS", 0.25), "angled": ("fix3", "ANGLED", 0.35),
            "push": ("fix3", "PUSH", 0.55), "spins": ("fix3", "SPINS", 0.7), "garden": ("fix3", "GARDEN", 0.88),
            "egg": ("break4", "EGG", 0.2), "cheese": ("break4", "CHEESE", 0.45), "laugh": ("break4", "LAUGH", 0.7),
            "water4": ("break4", "WATER", 0.92),
            "enz": ("fix4", "ENZYMES", 0.15), "chop": ("fix4", "CHOP", 0.3), "egg4": ("fix4", "EGG", 0.4),
            "starch": ("fix4", "STARCH", 0.5), "body": ("fix4", "BODY", 0.8),
            "follow": ("cta", "FOLLOW", 0.35),
            "y1886": ("reveal", "EIGHTEEN", 0.1), "jo": ("reveal", "JOSEPHINE", 0.3), "servants": ("reveal", "SERVANTS", 0.45),
            "chipping": ("reveal", "CHIPPING", 0.55), "built": ("reveal", "BUILT", 0.75), "hotels": ("reveal", "HOTELS", 0.88),
            "s1": ("stat", "TWELVE", 0.05), "s2": ("stat", "SIXTY", 0.4), "s3": ("stat", "HUNDRED", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_cent": ("tag", "CENTURY", 0.1), "t_mom": ("tag", "MOM", 0.4), "t_wash": ("tag", "WASHES", 0.55),
            "t_plate": ("tag", "PLATE", 0.7), "t_goes": ("tag", "GOES", 0.92)})
        T["drain1"] = max(T["drain"], T["hundred"]) + 0.1
        T["fast1"] = max(T["fast"], T["scraps"]) + 0.1
        T["spot1"] = max(T["spot"], T["fixed"]) + 0.1
        T["water41"] = max(T["water4"], T["laugh"]) + 0.1
        T["again1"] = max(T["again"], T["pump"]) + 0.2
        T["back1"] = max(T["back"], T["clean"]) + 0.2
        T["garden1"] = max(T["garden"], T["spins"]) + 0.2
        T["body1"] = max(T["body"], T["starch"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "sink", 1)
        self.cut(s("fix1") - 0.12, "box", -1)
        self.cut(s("break3") - 0.12, "arms", 1)
        self.cut(s("break4") - 0.12, "enzyme", -1)
        self.cut(s("reveal") - 0.12, "old", 1)
        self.cut(s("stat") - 0.12, "kitchen", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- kitchen camera: from the lower rack in x-ray out to the kitchen
        cm = Camera(0, -12, 1.75)
        cm.key(0.05, 0, -16, 1.7, 0.5)
        cm.key(max(0.6, T["congrats"] - 0.9), 0, -230, 0.95, max(1.0, T["name"] - T["congrats"] + 0.7))
        cm.key(s("stat") - 0.12, 0, -230, 0.9, 0.0).key(s("stat"), 0, -232, 0.92, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -180, 1.05, 1.0).key(s("closer") + 0.9, 0, -175, 1.1, 3.0)
        self.cam = cm
        self.spans = [(T["drain1"], T["again1"] + 0.3), (T["fast1"], T["back1"] + 0.3), (T["spot1"], T["garden1"] + 0.3),
                      (T["water41"], T["body1"] + 0.3)]
        self.shakes = [(T["blast"], 0.4, 6), (T["congrats"], 0.35, 8), (T["drain1"], 0.3, 6), (T["fast1"], 0.3, 6),
                       (T["spot1"], 0.3, 6), (T["water41"], 0.3, 6), (s("closer") + 0.2, 0.35, 9)]

    def arm_angle(self, t):
        return t * 340.0

    # ------------------------------------------------------------------ set: kitchen (hook, stat, closer)
    def draw_kitchen(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        closer = t >= s("closer") - 0.1
        night = 0.55 * prog(t, s("closer") - 0.1, s("closer") + 0.8) if closer else 0.0
        self.view(c, cam)
        kitchen(c, t, night)
        if hook:
            xr = 1.0 - prog(t, T["name"] - 0.5, T["name"] + 0.3)
            hk = prog(t, T["hot"] - 0.4, T["hot"])
            machine(c, t, xray=xr, ang=self.arm_angle(t), jets=1.0, water=0.5, steam=0.8 * hk, hot=hk, pump=1.0,
                    flow=1.0, display="0:42")
        elif closer:
            dk = prog(t, s("closer") + 0.1, s("closer") + 0.9)
            machine(c, t, door=dk, xray=0.0, jets=0.0, water=0.0, steam=dk, sparkle=dk, lit=night, display="END", run=0.0)
        else:
            machine(c, t, display="1:12", lit=0.0)
        c.restore()
        if closer and night > 0:
            c.drawRect(R(0, 0, W, H), P("#2A1E40", 0.22 * night))
        if hook:
            hk = prog(t, T["hot"] - 0.4, T["hot"]) * (1 - prog(t, T["arms"] - 0.2, T["arms"] + 0.2))
            if hk > 0:                                                 # thermometer + a hand pulled back from the spray
                thermometer(c, 900, 760, 1.6, lerp(0.2, 0.85, prog(t, T["hot"] - 0.4, T["hot"] + 0.6)), True, a=hk)
                text(c, "60°C", 900, 560, 52, "#FCA5A5", "Poppins-Black", a=hk)
                pull = e_out(prog(t, T["hands"] - 0.1, T["hands"] + 0.35))
                hx, hy = 250 - pull * 140, 760 + pull * 120
                c.drawRRect(rr(hx - 160, hy - 34, 170, 68, 30), P("#E8B48A", hk))
                for i in range(4):
                    c.drawRRect(rr(hx, hy - 34 + i * 17, 46 - i * 4, 15, 7), P("#E8B48A", hk))
                if pull > 0.3:
                    for i in range(3):
                        c.drawLine(hx + 60, hy - 50 + i * 40, hx + 100, hy - 60 + i * 40, P(WARN, hk * pull, stroke=7))

    def ui_kitchen(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "hot", T["hot"] - 0.2, T["arms"] - 0.2, accent=WARN, size=46)
            self.chip(540, 300, "nomotor", T["arms"] - 0.2, T["name"] - 0.3, accent="#93C5FD", size=42)
            self.chip(540, 300, "name", T["name"] - 0.3, s("break1") + 0.1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: sink (break1)
    def draw_sink(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, -760, 1.05)
        self.view(c, cam)
        kitchen(c, t)
        mk = prog(t, T["hand"] - 0.2, T["drain1"] + 0.3)
        sink(c, t, meter=mk, run=1.0)
        c.restore()

    def ui_sink(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "sink", T["hundred"] - 0.3, s("fix1") - 0.15, accent=WARN, size=44)
        self.badge("alert", T["drain1"], s("fix1") - 0.2, x=920, y=440)
        self.red(T["drain1"], 1.2)

    # ------------------------------------------------------------------ set: box (fix1, break2, fix2), x-ray low view
    def draw_box(self, c, t):
        T, s = self.T, self.tl.s
        f2 = t >= s("fix2") - 0.12
        b2 = t >= s("break2") - 0.12
        cam = (0, -146, 1.3) if not b2 else (0, -62, 2.3)
        self.view(c, cam)
        kitchen(c, t)
        wk = prog(t, T["few"] - 0.3, T["bottom"])
        sc = prog(t, T["fills"] - 0.3, T["scraps"] + 0.3) if b2 else 0.0
        fk = prog(t, T["filter"] - 0.2, T["scraps2"] + 0.5) if f2 else 0.0
        machine(c, t, xray=1.0, ang=self.arm_angle(t), jets=prog(t, T["pump"] - 0.2, T["pump"] + 0.3) if not b2 else 1.0,
                water=0.2 + 0.6 * wk if not b2 else 0.8, scraps=sc, filt=fk, pump=1.0,
                flow=prog(t, T["pump"] - 0.2, T["pump"] + 0.3) if not b2 else 1.0, dirt=0.6 * sc * (1 - fk))
        self.ui["sump"] = self.to_screen(cam, -150, -40)
        self.ui["pump"] = self.to_screen(cam, DW / 2 - 80, -36)
        self.ui["pipe"] = self.to_screen(cam, DW / 2 - 60, -300)
        self.ui["filter"] = self.to_screen(cam, 0, -46)
        c.restore()

    def ui_box(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break2") - 0.12:
            sx, sy = self.ui.get("sump", (400, 1100))
            self.label(sx, sy, 300, 520, "few", T["few"] - 0.2, s("break2") - 0.2, accent="#93C5FD", size=40)
            px, py = self.ui.get("pump", (800, 1100))
            self.label(px, py, 800, 640, "pump", T["pump"] - 0.2, s("break2") - 0.2, accent="#CBD5E1", size=40)
            self.chip(540, 300, "again", T["again"] - 0.3, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["again1"] + 0.1, s("break2") - 0.15, x=920, y=420)
            return
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "scraps", T["scraps"] - 0.3, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["fast1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["fast1"], 1.2)
            return
        fx_, fy_ = self.ui.get("filter", (540, 1100))
        self.label(fx_, fy_, 320, 560, "filter", T["filter"] - 0.2, s("break3") - 0.2, accent="#E2E8F0", size=42)
        self.chip(540, 300, "clean", T["clean"] - 0.3, s("break3") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["back1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: arms (break3, fix3), top view
    def draw_arms(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        vrect(c, 0, 0, W, H, ["#0F1B2E", "#16263F"])
        cx, cy = 540, 700
        c.drawCircle(cx, cy, 340, P("#1E293B"))
        c.drawCircle(cx, cy, 340, P("#475569", 1, stroke=8))
        if not fixed:                                                  # a dirty plate, one jet, one clean spot
            c.drawCircle(cx, cy, 290, P("#F8FAFC"))
            c.drawCircle(cx, cy, 190, P("#E2E8F0", 1, stroke=4))
            rng = random.Random(4)
            ck = prog(t, T["jet"] - 0.2, T["spot1"])
            for i in range(26):
                px, py = cx + rng.uniform(-230, 230), cy + rng.uniform(-230, 230)
                if math.hypot(px - cx, py - cy) > 255:
                    continue
                gone = ck if math.hypot(px - (cx + 60), py - (cy + 40)) < 80 else 0.0
                c.drawCircle(px, py, rng.uniform(14, 30), P(rng.choice((DIRT, "#D97706", "#B45309")), 0.9 * (1 - gone)))
            c.drawCircle(cx + 60, cy + 40, 80 * ck, P("#93C5FD", 0.25 * ck))
            c.drawRRect(rr(cx + 40, cy + 300, 40, 110, 10), P("#94A3B8"))      # the fixed nozzle
            for j in range(4):
                f = (t * 3 + j * 0.25) % 1.0
                c.drawCircle(cx + 60, lerp(cy + 300, cy + 60, f), 10, P("#93C5FD", 0.8 * (1 - f * 0.3)))
            return
        ang = (t - s("fix3")) * 260.0 * prog(t, T["push"] - 0.4, T["push"] + 0.4) + 20
        arm_top(c, cx, cy, 290, ang, t, jets=prog(t, T["shoots"] - 0.2, T["shoots"] + 0.2), push=prog(t, T["push"] - 0.2, T["push"] + 0.2))
        gk = prog(t, T["garden"] - 0.4, T["garden"])
        if gk > 0:
            c.drawRRect(rr(580, 1000, 460, 230, 30), P("#0B3B2A", 0.92 * gk))
            sprinkler(c, 810, 1190, 0.7, t * 400, t, a=gk)
        self.ui["hole"] = (cx + math.cos(math.radians(ang)) * 290 * 0.83, cy + math.sin(math.radians(ang)) * 290 * 0.83)

    def ui_arms(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "spot", T["fixed"] - 0.2, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["spot1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["spot1"], 1.2)
            return
        hx, hy = self.ui.get("hole", (700, 780))
        self.label(hx, hy, 300, 500, "angled", T["angled"] - 0.2, T["push"] - 0.1, accent="#93C5FD", size=40)
        self.chip(540, 300, "push", T["push"] - 0.2, T["garden"] - 0.3, accent=HILITE, size=42)
        self.chip(540, 300, "sprinkler", T["garden"] - 0.3, s("break4") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["garden1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: enzyme (break4, fix4), magnified
    def draw_enzyme(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        vrect(c, 0, 0, W, H, ["#0B1426", "#13233F"])
        if not fixed:
            c.drawCircle(540, 800, 470, P("#A9B6C6"))
            c.drawCircle(540, 800, 330, P("#8C9AAD", 1, stroke=6))
            ek = prog(t, T["egg"] - 0.3, T["egg"])
            c.drawPath(path_of([(260, 600), (520, 540), (600, 640), (560, 760), (330, 800), (240, 700)], close=True),
                       P("#FACC15", ek))
            c.drawPath(path_of([(260, 600), (520, 540), (600, 640), (560, 760), (330, 800), (240, 700)], close=True),
                       P("#CA8A04", ek, stroke=10))
            ck = prog(t, T["cheese"] - 0.3, T["cheese"])
            c.drawPath(path_of([(560, 860), (820, 820), (860, 980), (700, 1060), (540, 1000)], close=True), P("#F97316", ck))
            for i in range(6):
                c.drawCircle(600 + i * 40, 900 + (i % 2) * 50, 14, P("#9A3412", ck))
            wk = prog(t, T["laugh"] - 0.4, T["water41"] + 0.5)
            for k in range(6):                                          # water drops bouncing off
                q = (t * 1.1 + k * 0.17) % 1.0
                xx = 300 + k * 90
                yy = 380 + q * 420
                if yy > 620:
                    yy = 620 - (yy - 620) * 0.8
                    xx += (q - 0.57) * 260 * (1 if k % 2 else -1)
                c.drawCircle(xx, yy, 20, P(WATER, 0.9 * wk))
                c.drawCircle(xx - 6, yy - 7, 6, P("#FFFFFF", 0.8 * wk))
            return
        c.drawCircle(540, 800, 470, P("#1E2A40"))
        chop = prog(t, T["chop"] - 0.2, T["egg4"] + 0.6)
        chain(c, 150, 700, 10, 74, t, "#FACC15", cuts=(2, 5, 7), cut_k=chop, seed=1)            # protein (egg)
        st = prog(t, T["starch"] - 0.2, T["starch"] + 0.7)
        chain(c, 150, 930, 10, 74, t, "#FDBA74", cuts=(3, 6), cut_k=st, hexes=True, seed=2)       # starch
        ek = prog(t, T["enz"] - 0.3, T["enz"])
        for i, (ex, ey, col) in enumerate(((310, 590, "#22C55E"), (570, 590, "#A855F7"), (820, 590, "#22C55E"),
                                           (380, 1050, "#06B6D4"), (720, 1050, "#06B6D4"))):
            bite = 0.5 + 0.5 * math.sin(t * 9 + i)
            enzyme(c, ex + math.sin(t * 2 + i) * 12, ey + math.cos(t * 2.3 + i) * 10, 1.15, bite, col, a=ek,
                   face=1 if i % 2 else -1)
        bk = prog(t, T["body"] - 0.3, T["body"])
        if bk > 0:                                                      # a little body outline: the same trick
            c.drawCircle(980, 1060, 30, P("#475569", bk))
            c.drawRRect(rr(950, 1094, 60, 110, 26), P("#475569", bk))
            add_glow(c, 980, 1140, 60, GOOD, 0.6 * bk)

    def ui_enzyme(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "egg", T["egg"] - 0.2, T["cheese"] - 0.1, accent="#FDE047", size=44)
            self.chip(540, 300, "cheese", T["cheese"] - 0.1, T["laugh"] - 0.1, accent="#FDBA74", size=44)
            self.chip(540, 300, "nope", T["laugh"] - 0.1, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["water41"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["water41"], 1.2)
            return
        self.chip(540, 300, "enz", T["enz"] - 0.2, T["chop"] - 0.1, accent=GOOD, size=52)
        self.chip(540, 300, "chop", T["chop"] - 0.1, T["body"] - 0.2, accent="#FDE047", size=42)
        self.chip(540, 300, "body", T["body"] - 0.2, s("cta") - 0.15, accent="#93C5FD", size=40)
        self.badge("check", T["body1"] + 0.1, s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: old (reveal)
    def draw_old(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#4A3A28", "#3A2C1E", "#2A1E14"])
        c.drawRect(R(0, 1230, W, H - 1230), P("#5A4630"))
        for k in range(6):                                              # wallpaper stripes
            c.drawRect(R(k * 190, 0, 70, 1230), P("#5C4733", 0.5))
        built = t >= T["built"] - 0.3
        if t < T["hotels"] - 0.3:
            if not built:
                c.drawRect(R(120, 980, 840, 30), P("#6B4423"))           # the table with fine china
                for i in range(5):
                    c.drawOval(R(160 + i * 160, 950, 120, 34), P("#F5F5F4"))
                    c.drawOval(R(185 + i * 160, 958, 70, 18), P("#93C5FD", 0.6))
                maid(c, 760, 1235, 470, t)
                ck = prog(t, T["chipping"] - 0.2, T["chipping"] + 0.4)
                if ck > 0:                                               # a plate drops and chips
                    py = lerp(1000, 1210, e_in(ck))
                    c.drawOval(R(640, py - 16, 110, 32), P("#F5F5F4"))
                    if ck > 0.9:
                        sparks_shower(c, 695, 1215, t, T["chipping"] + 0.2, dur=0.6, n=12, col="#F5F5F4")
                        c.drawPath(path_of([(760, 1220), (790, 1210), (800, 1228)], close=True), P("#F5F5F4"))
            else:
                bk = prog(t, T["built"] - 0.3, T["built"] + 0.2)
                old_machine(c, 600, 1235, 1.25, t, crank=1.0, a=bk)
                lady(c, 260, 1235, 440, t, a=bk, crank=1.0)
        else:
            hk = prog(t, T["hotels"] - 0.3, T["hotels"] + 0.1)
            hotel(c, 540, 1235, 1.5, a=hk)
            for i in range(3):
                person(c, 260 + i * 260, 1235, 300, ("#1D4ED8", "#B91C1C", "#047857")[i], t, pose="cheer", face=1, a=hk)
        c.drawRect(R(0, 0, W, H), P("#704214", 0.12))

    def ui_old(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "jo", T["y1886"] - 0.2, T["chipping"] - 0.2, accent="#FDE68A", size=42)
        self.chip(540, 300, "chip", T["chipping"] - 0.2, T["built"] - 0.3, accent=WARN, size=46)
        self.chip(540, 300, "jo", T["built"] - 0.3, T["hotels"] - 0.3, accent="#FDE68A", size=42)
        self.chip(540, 300, "hotels", T["hotels"] - 0.3, s("stat") - 0.15, accent=GOOD, size=44)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        cam = (-380, -860, 0.5)
        self.view(c, cam)
        kitchen(c, t)
        c.save()
        c.translate(-700, 0)
        sink(c, t, meter=0.0, run=1.0, pile=0.7)
        c.restore()
        machine(c, t, door=1.0, xray=0.0, jets=0.0, water=0.0, dirt=0.0, sparkle=0.4, display="OFF", run=0.0)
        scrub = math.sin(t * 14) * 30 * prog(t, T["t_wash"] - 0.3, T["t_wash"])
        if self.rtl:
            mom(c, -1130, 0, 1650, t, a=1.0)
        else:
            person(c, -1130, 0, 1650, "#BE185D", t, pose="carry", face=1, hair="#7C2D12")
        plate_disc(c, -800 + scrub, -960, 90, "#E2E8F0", dirt=1 - prog(t, T["t_wash"], T["t_wash"] + 1.2))
        c.restore()

    def ui_tag(self, c, t, tw):
        T = self.T
        if self.rtl:
            bubble(c, 700, 560, self.L["why"], self.span(T["t_plate"] - 0.3, self.duration + 1), tail_left=True, size=60)
        else:
            self.chip(540, 300, "why", T["t_wash"] - 0.2, self.duration + 1, accent=HILITE, size=48)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#C9D9E6", "#9FB4C4"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whirr(max(1.0, T["congrats"]), 120.0, 160.0, 61), -16), (T["blast"], sfx.hiss(1.2, 62), -14),
              (T["hands"], sfx.sizzle(0.6, 63), -10), (T["spin"], sfx.whoosh(0.5, True, 64), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["dinner"], sfx.hiss(2.0, 68), -16),
               (T["drain1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["box"], sfx.thunk(70), -8),
               (T["pump"], sfx.whirr(1.4, 200.0, 320.0, 71), -14), (T["again1"], sfx.ding(), -8), (T["again1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["scraps"], sfx.tap(73), -10),
               (T["fast1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 74), -4), (T["filter"], sfx.click(75), -8),
               (T["back1"], sfx.ding(), -8), (T["back1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 76), -4), (T["jet"], sfx.hiss(0.8, 77), -14),
               (T["spot1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["shoots"], sfx.hiss(1.4, 79), -16),
               (T["spins"], sfx.whirr(1.2, 300.0, 520.0, 80), -14), (T["garden1"], sfx.ding(), -8),
               (T["garden1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 81), -4), (T["laugh"], sfx.tap(82), -8),
               (T["water41"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 84), -4), (T["chop"], sfx.snap(85), -10),
               (T["chop"] + 0.3, sfx.snap(86), -10), (T["starch"], sfx.snap(87), -10), (T["body1"], sfx.ding(), -8),
               (T["body1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(88), 0), (T["follow"] - 0.15, sfx.pop(89), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 90), -6), (T["chipping"] + 0.35, sfx.clank(900.0, 0.4, 91), -10),
               (T["built"], sfx.creak(0.8, 92), -12), (T["hotels"], sfx.ding(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 93), -6), (T["s1"], sfx.pop(94), -3), (T["s2"], sfx.pop(95), -3),
               (T["s3"], sfx.pop(96), -3)]
        ev += [(T["cong2"], sfx.pop(97), -2), (T["cong2"], sfx.sparkle(1.4, 18, 98), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 99), -6), (T["t_wash"], sfx.hiss(1.4, 100), -16),
               (T["t_plate"], sfx.tap(101), -8)]
        return ev


NAME = "dishwasher"
EPISODE = Dishwasher
