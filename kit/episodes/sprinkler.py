"""Episode 101 - a fire sprinkler.  v2 look.

Sets: office (hook: an office ceiling in perspective with about a hundred sprinkler heads, a wastebasket fire, and only
the one head above it bursts and sprays; break2: the movie version, every head pours at once; cta, reveal: the same
ceiling, one head spraying, the fire out and a 77% ring; stat), factory (break1: an 1870s piano factory, shavings catch
and the flames race along the benches; fix1: an old brass head on the pipe whose metal plug melts so the water bursts
out), bulb (fix2: a macro of a modern head, the red glass bulb with its bubble, the heat swells the liquid, the glass
pops and the water fans off the toothed plate; closer: the head big and clean, for the cover), bakery (break3: a
red-bulb head over a hot oven pops with no fire; fix3: a row of bulb colours with their temperatures, then a blue one
over the oven that stays shut), valve (break4: the main valve in the basement turned shut, upstairs the burst head only
drips; fix4: the valve chained open with a padlock and a tamper switch: a wrench on the wheel and the alarm bell rings),
tag (English: ninety candles on grandpa's cake under the sprinkler, everyone stares up, nothing; Arabic: dad's incense
burner smoking in a hotel room, the family stares up, nothing).
Perspective sets: eye at (0, 0, 0), ceiling Y = -1.5 m, floor Y = +1.5 m; proj() turns metres into screen pixels.
"""
from v2_base import *  # noqa: F401,F403

PIPE = "#B91C1C"
BRASS = ("#FDE68A", "#D4A72C", "#8A5A0B")
CHROME = ("#F8FAFC", "#CBD5E1", "#64748B")
WATER = "#7DD3FC"
BULBS = (("#FB923C", "57°"), ("#EF4444", "68°"), ("#FACC15", "79°"), ("#22C55E", "107°"), ("#3B82F6", "121°"))
HZ, F = 900.0, 760.0                                   # horizon y and focal length of the perspective sets
CEIL, FLOOR = -1.5, 1.5
FIRE_X, FIRE_Z = 0.75, 5.0                             # the wastebasket, right under a head


def proj(X, Y, Z):
    return 540 + X * F / Z, HZ + Y * F / Z


# ====================================================================================== pieces
def head(c, x, y, s, bulb="#EF4444", fill=0.0, burst=0.0, t=0.0, a=1.0, old=False, melt=0.0, glow=0.0):
    """A pendent sprinkler hanging from (x, y); s = 1 is about 100 px tall. fill 0..1: the bubble shrinks as the liquid
    swells; burst 0..1: the bulb is gone (shards fly). old=True: an 1870s brass rose with a soft-metal plug (melt)."""
    if a <= 0 or s <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    body = BRASS if not old else ("#FCD34D", "#B7791F", "#78350F")
    c.drawRect(R(-13, 0, 26, 24), lin_paint(-13, 0, 13, 0, [body[2], body[0], body[1], body[2]], a=a))
    for k in range(4):
        c.drawLine(-13, 4 + k * 5, 13, 6 + k * 5, P(body[2], 0.7 * a, stroke=1.6))
    hexp = skia.Path()
    for k, (px, py) in enumerate(((-22, 24), (22, 24), (19, 38), (-19, 38))):
        (hexp.moveTo if k == 0 else hexp.lineTo)(px, py)
    hexp.close()
    c.drawPath(hexp, lin_paint(-22, 0, 22, 0, [body[2], body[0], body[1], body[2]], a=a))
    if old:                                           # a brass rose with holes, sealed by a grey plug of soft metal
        rose = skia.Path()
        rose.addOval(R(-34, 34, 68, 46))
        c.drawPath(rose, lin_paint(-34, 0, 34, 0, [body[2], body[0], body[1], body[2]], a=a))
        for k in range(7):
            hx = -24 + k * 8
            c.drawCircle(hx, 62 + abs(hx) * 0.15, 2.6, P("#3B2405", a))
        if melt < 1:
            c.drawRRect(rr(-10, 74, 20, 14 * (1 - melt) + 2, 4), P("#9CA3AF", a))
            if melt > 0:
                for k in range(3):
                    u = (t * 1.4 + k / 3) % 1.0
                    c.drawCircle(-4 + k * 4, 88 + u * 60, 4 * (1 - u * 0.5), P("#D1D5DB", (1 - u) * a * min(1, melt * 3)))
        c.restore()
        return
    arm = lin_paint(-20, 0, 20, 0, [CHROME[2], CHROME[0], CHROME[1], CHROME[2]], a=a)
    for sd in (-1, 1):                                # the frame: two arms down to the boss
        pth = skia.Path()
        pth.moveTo(sd * 17, 36)
        pth.cubicTo(sd * 24, 52, sd * 20, 74, sd * 6, 88)
        c.drawPath(pth, P(CHROME[2], a, stroke=9))
        c.drawPath(pth, P(CHROME[0], 0.8 * a, stroke=4))
    c.drawRRect(rr(-8, 84, 16, 10, 4), arm)
    if burst < 1:                                     # the glass bulb, liquid with a bubble near the top
        ba = a * (1 - burst)
        c.drawRRect(rr(-7, 40, 14, 44, 7), P(bulb, 0.95 * ba))
        c.drawRRect(rr(-4, 44, 3, 34, 1.5), P("#FFFFFF", 0.55 * ba))
        br = 5.0 * (1 - fill)
        if br > 0.4:
            c.drawCircle(1, 47 + 2 * fill, br, P("#FFF7ED", 0.9 * ba))
        if glow > 0:
            add_glow(c, 0, 62, 40, bulb, 0.5 * glow * ba)
    if burst > 0:                                     # shards flying off
        rng = random.Random(9)
        for k in range(9):
            ang = rng.uniform(-2.6, -0.5) if k % 2 else rng.uniform(0.5, 2.6)
            sp = rng.uniform(60, 150)
            u = burst
            sx, sy = math.cos(ang) * sp * u, 60 + math.sin(ang) * sp * u * 0.4 + 220 * u * u
            tri = skia.Path()
            tri.moveTo(sx, sy)
            tri.lineTo(sx + 6, sy + 3)
            tri.lineTo(sx + 2, sy + 9)
            tri.close()
            c.drawPath(tri, P(bulb, 0.9 * (1 - u) * a))
    dfl = skia.Path()                                 # the deflector: a toothed disc seen from the side
    dfl.addOval(R(-34, 92, 68, 10))
    c.drawPath(dfl, lin_paint(-34, 0, 34, 0, [CHROME[2], CHROME[0], CHROME[1], CHROME[2]], a=a))
    for k in range(9):
        tx = -30 + k * 7.5
        c.drawLine(tx, 99, tx, 104, P(CHROME[2], a, stroke=2.5))
    c.restore()


def spray(c, x, y, s, t, k=1.0, floor_y=None, seed=1, wide=1.0):
    """Water fanning out of a head whose deflector is at (x, y): an umbrella of falling streaks."""
    if k <= 0:
        return
    rng = random.Random(seed)
    n = int(46 * k) + 6
    for i in range(n):
        ang = rng.uniform(-1, 1)
        u = (t * 1.9 + rng.random()) % 1.0
        vx = ang * 260 * s * wide
        px, py = x + vx * u, y + 40 * s * u + 620 * s * u * u
        if floor_y is not None and py > floor_y:
            continue
        L = 22 * s + 10
        c.drawLine(px, py, px - vx * 0.06, py - L, P(WATER, 0.75 * k * (1 - u * 0.5), stroke=max(1.5, 3.2 * s)))
    add_glow(c, x, y + 120 * s, 160 * s, "#BAE6FD", 0.18 * k)


def tongue(c, x, y, w, h, t, seed=0, a=1.0):
    """One flame as layered teardrops (mid-tone colours: white cores bloom into a blob in the finishing pass)."""
    if h <= 1 or a <= 0:
        return
    for k, (col, sw, sh) in enumerate((("#C2410C", 1.0, 1.0), ("#F97316", 0.72, 0.8), ("#FBBF24", 0.42, 0.55))):
        wob = math.sin(t * 13 + seed * 1.7 + k) * w * 0.12
        hh = h * sh * (0.9 + 0.1 * math.sin(t * 17 + seed))
        ww = w * sw / 2
        p = skia.Path()
        p.moveTo(x - ww, y)
        p.cubicTo(x - ww * 1.1, y - hh * 0.45, x - ww * 0.3 + wob, y - hh * 0.75, x + wob * 1.5, y - hh)
        p.cubicTo(x + ww * 0.3 + wob, y - hh * 0.75, x + ww * 1.1, y - hh * 0.45, x + ww, y)
        p.close()
        c.drawPath(p, P(col, a))


def fire(c, x, y, w, t, k=1.0, seed=0):
    """Flames standing on (x, y), w wide."""
    if k <= 0:
        return
    add_glow(c, x, y - w * 0.5, w * 1.6, "#FB923C", 0.18 * k)
    for i, dx in enumerate((-0.28, 0.0, 0.27)):
        tongue(c, x + dx * w, y, w * 0.5, w * 1.5 * k * (1.15 if i == 1 else 0.8), t + i * 0.37, seed=seed + i)


def bin_(c, x, y, h, a=1.0):
    """A metal wastebasket standing on (x, y), h tall."""
    w = h * 0.75
    pth = skia.Path()
    pth.moveTo(x - w / 2, y - h)
    pth.lineTo(x + w / 2, y - h)
    pth.lineTo(x + w * 0.4, y)
    pth.lineTo(x - w * 0.4, y)
    pth.close()
    c.drawPath(pth, lin_paint(x - w / 2, 0, x + w / 2, 0, ["#475569", "#94A3B8", "#334155"], a=a))
    for k in range(5):
        xx = x - w * 0.4 + k * w * 0.2
        c.drawLine(xx, y - h + 3, xx * 0.98 + x * 0.02, y - 3, P("#1E293B", 0.5 * a, stroke=2))


def desk(c, X0, X1, Z0, Z1, a=1.0):
    """An office desk (perspective): top at desk height, a monitor at its back edge."""
    Y = 0.75
    pts = [proj(X0, Y, Z0), proj(X1, Y, Z0), proj(X1, Y, Z1), proj(X0, Y, Z1)]
    top = skia.Path()
    for k, p in enumerate(pts):
        (top.moveTo if k == 0 else top.lineTo)(*p)
    top.close()
    fx0, fy0 = proj(X0, Y, Z0)
    fx1, fy1 = proj(X1, FLOOR, Z0)
    c.drawRect(R(fx0, fy0, fx1 - fx0, fy1 - fy0), P("#1E293B", a))
    c.drawPath(top, P("#94A3B8", a))
    mx0, my0 = proj((X0 + X1) / 2 - 0.3, Y - 0.45, Z1 - 0.1)
    mx1, my1 = proj((X0 + X1) / 2 + 0.3, Y, Z1 - 0.1)
    c.drawRect(R(mx0, my0, mx1 - mx0, my1 - my0), P("#0F172A", a))
    c.drawRect(R(mx0 + 2, my0 + 2, mx1 - mx0 - 4, (my1 - my0) * 0.7), P("#38BDF8", 0.55 * a))


def heads_grid():
    out = []
    for j in range(13):
        Z = 2.5 + 2.5 * j
        for i in range(8):
            X = -5.25 + 1.5 * i
            out.append((X, Z))
    return out


GRID = heads_grid()


def office(c, t, burst=0.0, fire_k=1.0, all_on=0.0, one=1.0, film=0.0, calm=0.0):
    """The office in perspective. burst: the head over the bin (0..1); all_on: every head pours (the movie)."""
    vrect(c, 0, 0, W, H, ["#1F2937", "#334155"])
    # ceiling: light tiles converging to the back wall
    cy_back = HZ + CEIL * F / 34
    fy_back = HZ + FLOOR * F / 34
    c.drawRect(R(0, 0, W, cy_back), lin_paint(0, 0, 0, cy_back, ["#3B4A63", "#56657E"]))
    for j in range(1, 30):
        Z = 1.0 + j * 1.25
        yy = HZ + CEIL * F / Z
        if yy > 0:
            c.drawLine(0, yy, W, yy, P("#7C8BA3", 0.35, stroke=2))
    for i in range(-9, 10):
        X = i * 0.75
        x0, y0 = proj(X, CEIL, 0.9)
        x1, y1 = proj(X, CEIL, 34)
        c.drawLine(x0, y0, x1, y1, P("#7C8BA3", 0.3, stroke=2))
    # back wall and side walls
    bx0, _ = proj(-6, 0, 34)
    bx1, _ = proj(6, 0, 34)
    c.drawRect(R(bx0, cy_back, bx1 - bx0, fy_back - cy_back), P("#475569"))
    for sd in (-1, 1):
        w = skia.Path()
        x0, y0 = proj(sd * 6, CEIL, 8.4)
        x1, y1 = proj(sd * 6, CEIL, 34)
        x2, y2 = proj(sd * 6, FLOOR, 34)
        x3, y3 = proj(sd * 6, FLOOR, 8.4)
        w.moveTo(x0, y0)
        w.lineTo(x1, y1)
        w.lineTo(x2, y2)
        w.lineTo(x3, y3)
        w.close()
        c.drawPath(w, P("#3F4B5E"))
        for k in range(4):                            # windows on the walls, a night city outside
            za, zb = 10 + k * 6, 13 + k * 6
            wa = proj(sd * 6, -0.9, za)
            wb = proj(sd * 6, 0.4, zb)
            q = skia.Path()
            q.moveTo(wa[0], wa[1])
            q.lineTo(wb[0], proj(sd * 6, -0.9, zb)[1])
            q.lineTo(wb[0], wb[1])
            q.lineTo(wa[0], proj(sd * 6, 0.4, za)[1])
            q.close()
            c.drawPath(q, P("#1E3A8A", 0.9))
    # floor: carpet
    c.drawRect(R(0, fy_back, W, H - fy_back), lin_paint(0, fy_back, 0, H, ["#334155", "#1E293B"]))
    for Z0, Z1 in ((3.2, 4.2), (6.5, 7.5), (10, 11), (14, 15)):
        desk(c, -4.6, -2.2, Z1, Z0)
        desk(c, 2.6, 5.0, Z1, Z0)
    # the fire in the wastebasket
    bx, by = proj(FIRE_X, FLOOR, FIRE_Z)
    s_ = F / FIRE_Z / 100
    bin_(c, bx, by, 0.5 * 100 * s_)
    fire(c, bx, by - 0.46 * 100 * s_, 0.5 * 100 * s_, t, fire_k, seed=3)
    if fire_k < 1 and burst > 0:
        v2.smoke(c, bx, by - 0.4 * 100 * s_, t, 0.0, rate=10, life=2.6, spread=(60, -40), rise=-60, size=(14, 60),
                 col="#94A3B8", seed=4, a=0.6 * (1 - fire_k))
    # the heads, far to near; the one over the bin can burst
    for X, Z in sorted(GRID, key=lambda p: -p[1]):
        x, y = proj(X, CEIL, Z)
        if x < -60 or x > W + 60 or y < -60:
            continue
        s = 3.2 / Z
        me = abs(X - FIRE_X) < 0.01 and abs(Z - FIRE_Z) < 0.01
        b = burst if me else all_on
        head(c, x, y, s * 100 / 100, burst=b, t=t, a=1.0)
        if b > 0.05:
            spray(c, x, y + 100 * s, s * 1.15, t + X * 0.3 + Z * 0.1, k=(one if me else all_on) * clamp(b * 3),
                  floor_y=proj(X, FLOOR, Z)[1], seed=int(Z * 7 + X * 3))
        if me and burst > 0:
            add_glow(c, x, y + 60 * s, 110, "#38BDF8", 0.45 * (1 - 0.5 * calm))
            c.drawCircle(x, y + 50 * s, 70 + 10 * math.sin(t * 6), P(HILITE, 0.8 * clamp(burst * 3) * (1 - 0.6 * calm), stroke=5))
    if all_on > 0:                                    # the movie: water everywhere
        c.drawRect(R(0, fy_back, W, H - fy_back), P("#38BDF8", 0.18 * all_on))
        rng = random.Random(5)
        for k in range(14):                           # papers flying
            u = (t * 0.5 + rng.random()) % 1.0
            px, py = rng.uniform(80, 1000), lerp(700, 1150, u)
            c.save()
            c.translate(px + math.sin(t * 2 + k) * 30, py)
            c.rotate(t * 90 + k * 40)
            c.drawRect(R(-18, -24, 36, 48), P("#F8FAFC", 0.85 * all_on))
            c.restore()
    if film > 0:                                      # a film strip frame: this is the movie version
        for x0 in (0, W - 70):
            c.drawRect(R(x0, 0, 70, H), P("#0B0B0F", 0.92 * film))
            for k in range(22):
                yy = (k * 96 + t * 120) % (H + 96) - 48
                c.drawRRect(rr(x0 + 18, yy, 34, 52, 8), P("#E5E7EB", 0.85 * film))


def factory(c, t, spread=0.0, close=0.0, melt=0.0, water=0.0):
    """An 1870s piano factory at night (side view). spread 0..1 the flames run along the benches; close 0..1 a zoom to
    the brass head on the pipe above the bench, whose plug melts and lets the water out."""
    vrect(c, 0, 0, W, H, ["#2A1410", "#3B1C12", "#1C0D08"])
    k = e_io(close)
    cxw, cyw, z = 540, lerp(960, 470, k), lerp(1.0, 2.4, k)
    c.save()
    c.translate(540, 960)
    c.scale(z, z)
    c.translate(-cxw, -cyw)
    for row in range(9):                              # brick wall
        for col in range(13):
            bx = col * 90 + (45 if row % 2 else 0) - 40
            c.drawRect(R(bx, 360 + row * 44, 84, 38), P("#5B2A1E" if (row + col) % 3 else "#4A2318"))
    for wx in (180, 900):                             # tall windows with a night sky
        c.drawRect(R(wx - 70, 420, 140, 260), P("#0F1B3D"))
        c.drawRect(R(wx - 4, 420, 8, 260), P("#2A1410"))
        c.drawRect(R(wx - 70, 546, 140, 8), P("#2A1410"))
    c.drawRect(R(0, 330, W, 30), P("#3F1D12"))       # ceiling beam and the water pipe
    c.drawRect(R(0, 300, W, 18), lin_paint(0, 300, 0, 318, ["#9CA3AF", "#4B5563"]))
    c.drawRect(R(0, 1110, W, H - 1110), lin_paint(0, 1110, 0, 1300, ["#7C4A1E", "#4A2A10"]))
    for k in range(3):                                # half-built upright pianos
        px = 150 + k * 330
        c.drawRect(R(px, 860, 230, 250), lin_paint(px, 0, px + 230, 0, ["#3B1F0E", "#6B3A1A", "#3B1F0E"]))
        c.drawRect(R(px + 10, 960, 210, 22), P("#F5F5F4"))
        for kk in range(12):
            c.drawRect(R(px + 14 + kk * 17, 962, 8, 12), P("#111827"))
    c.drawRect(R(60, 1040, 960, 22), P("#8B5A2B"))   # the bench with wood shavings
    rng = random.Random(4)
    for k in range(40):
        sx, sy = rng.uniform(80, 1000), rng.uniform(1025, 1045)
        c.drawArc(R(sx - 12, sy - 8, 24, 16), rng.uniform(0, 180), 220, False, P("#E7C27D", 0.9, stroke=3))
    lx = 250                                          # the oil lamp
    c.drawLine(lx, 360, lx, 600, P("#1F2937", 1.0, stroke=3))
    c.drawOval(R(lx - 26, 600, 52, 60), P("#FCD34D", 0.85))
    add_glow(c, lx, 630, 160, "#FDE68A", 0.4)
    # flames running along the bench
    if spread > 0:
        front = lerp(lx, 1000, spread)
        for k in range(int((front - lx) / 120) + 1):
            fx_ = lx + k * 120
            kk = clamp((front - fx_) / 160)
            for j, dx in enumerate((-30, 30)):
                tongue(c, fx_ + dx, 1040, 70, 150 * kk * (1.1 if j else 0.9), t + k * 0.3 + j, seed=k * 2 + j)
        add_glow(c, (lx + front) / 2, 960, 380, "#FB923C", 0.14 * spread)
    hx = 540                                          # the brass head on the pipe, above the middle of the bench
    head(c, hx, 318, 1.3, t=t, old=True, melt=melt)
    if water > 0:
        spray(c, hx, 318 + 96 * 1.3, 1.3, t, k=water, floor_y=1040, seed=2, wide=1.2)
    c.restore()


def bulb_macro(c, t, heat=0.0, fill=0.0, burst=0.0, water=0.0, shine=0.0):
    """One modern head blown up big (screen centre x = 540, pipe at y = 330)."""
    vrect(c, 0, 0, W, H, ["#0F172A", "#111827", "#1F1209"])
    if heat > 0:                                      # hot air rising from below
        add_glow(c, 540, 1250, 700, "#F97316", 0.55 * heat)
        rng = random.Random(2)
        for k in range(18):
            u = (t * 0.6 + rng.random()) % 1.0
            x = rng.uniform(200, 880)
            pth = skia.Path()
            y0 = lerp(1250, 620, u)
            pth.moveTo(x, y0)
            for j in range(1, 8):
                pth.lineTo(x + math.sin(t * 3 + j + k) * 12, y0 - j * 18)
            c.drawPath(pth, P("#FDBA74", 0.35 * heat * (1 - u), stroke=4))
    c.drawRect(R(0, 300, W, 46), lin_paint(0, 300, 0, 346, ["#DC2626", "#7F1D1D"]))     # the red pipe
    c.drawRect(R(0, 300, W, 8), P("#FCA5A5", 0.5))
    if shine > 0:
        add_glow(c, 540, 650, 520, "#FDE68A", 0.25 * shine)
    head(c, 540, 346, 6.2, fill=fill, burst=burst, t=t, glow=heat)
    if water > 0:
        spray(c, 540, 346 + 98 * 6.2, 2.6, t, k=water, floor_y=1230, seed=5, wide=1.1)
        c.drawLine(540, 346 + 36 * 6.2, 540, 346 + 92 * 6.2, P(WATER, 0.85 * water, stroke=26))


def bakery(c, t, pop=0.0, heat=1.0, blue=0.0, chart=0.0, water=0.0):
    """A bakery kitchen (side view): the oven, trays of bread, a head on the ceiling right above the oven."""
    vrect(c, 0, 0, W, H, ["#3F2A1D", "#2A1B12"])
    c.drawRect(R(0, 300, W, 40), P("#57534E"))       # ceiling and pipe
    c.drawRect(R(0, 340, W, 14), lin_paint(0, 340, 0, 354, ["#DC2626", "#7F1D1D"]))
    c.drawRect(R(0, 1150, W, H - 1150), P("#78716C"))
    ox, oy, ow, oh = 270, 640, 540, 510               # the oven
    c.drawRRect(rr(ox, oy, ow, oh, 18), lin_paint(ox, 0, ox + ow, 0, ["#6B7280", "#D1D5DB", "#9CA3AF", "#4B5563"]))
    c.drawRRect(rr(ox + 50, oy + 90, ow - 100, 240, 14), P("#1C0A00"))
    add_glow(c, 540, oy + 210, 300, "#FB923C", 0.7 * heat)
    c.drawRRect(rr(ox + 60, oy + 100, ow - 120, 220, 12), P("#F97316", 0.55 * heat))
    for k in range(3):                                # loaves on the shelf inside
        c.drawOval(R(ox + 90 + k * 125, oy + 240, 110, 52), P("#B45309"))
        c.drawOval(R(ox + 105 + k * 125, oy + 246, 70, 18), P("#F59E0B", 0.8))
    c.drawRect(R(ox + 40, oy + 370, ow - 80, 26), P("#374151"))
    for k in range(5):                                # trays of bread on a rack at the side
        c.drawRect(R(860, 760 + k * 80, 180, 10), P("#9CA3AF"))
        for j in range(3):
            c.drawOval(R(868 + j * 58, 728 + k * 80, 50, 32), P("#D97706"))
    rng = random.Random(3)
    for k in range(14):                               # heat rising off the oven
        u = (t * 0.7 + rng.random()) % 1.0
        x = rng.uniform(320, 760)
        pth = skia.Path()
        y0 = lerp(640, 380, u)
        pth.moveTo(x, y0)
        for j in range(1, 6):
            pth.lineTo(x + math.sin(t * 3 + j + k) * 10, y0 - j * 16)
        c.drawPath(pth, P("#FDBA74", 0.4 * heat * (1 - u), stroke=4))
    hx = 540
    col = mix("#EF4444", "#3B82F6", blue)
    head(c, hx, 354, 1.9, bulb=col, fill=0.0, burst=pop, t=t, glow=heat * (1 - blue) * 0.6)
    if water > 0:
        spray(c, hx, 354 + 98 * 1.9, 1.5, t, k=water, floor_y=1150, seed=6, wide=1.3)
        for k in range(8):                            # steam off the wet oven
            u = (t * 0.8 + k / 8) % 1.0
            puff(c, 360 + k * 50, lerp(640, 420, u), lerp(20, 60, u), "#F8FAFC", 0.4 * water * (1 - u))
    if chart > 0:                                     # the bulb colours chart
        c.drawRRect(rr(90, 420, 900, 200, 26), P("#0B1220", 0.85 * chart))
        for k, (bc, lab) in enumerate(BULBS):
            bx = 180 + k * 180
            c.save()
            c.translate(bx, 448)
            c.scale(e_back(clamp(chart * 2 - k * 0.15)), e_back(clamp(chart * 2 - k * 0.15)))
            c.drawRRect(rr(-14, 0, 28, 84, 14), P(bc, chart))
            c.drawRRect(rr(-8, 8, 6, 64, 3), P("#FFFFFF", 0.5 * chart))
            text(c, lab, 0, 150, 40, INK, "Poppins-Black", a=chart)
            c.restore()


def valve_room(c, t, shut=0.0, chain=0.0, wrench=0.0, alarm=0.0, flow=1.0, drip=0.0):
    """The basement: the main water pipe comes up through the floor, a gate valve with a handwheel; an inset upstairs."""
    vrect(c, 0, 0, W, H, ["#1C2533", "#263243"])
    for row in range(16):                             # concrete block wall
        for col in range(7):
            bx = col * 170 + (85 if row % 2 else 0) - 60
            c.drawRect(R(bx, 380 + row * 54, 164, 48), P("#334155" if (row + col) % 2 else "#2D3A4D"))
    c.drawRect(R(0, 1170, W, H - 1170), P("#1E293B"))
    px = 420
    c.drawRect(R(px - 34, 300, 68, 870), lin_paint(px - 34, 0, px + 34, 0, ["#7F1D1D", "#EF4444", "#991B1B"]))
    if flow > 0:                                      # water moving up the pipe
        for k in range(8):
            u = (t * 0.9 + k / 8) % 1.0
            c.drawLine(px, lerp(1160, 310, u), px, lerp(1160, 310, u) - 40, P("#BAE6FD", 0.7 * flow, stroke=8))
    vy = 820                                          # the valve body and its wheel
    c.drawRRect(rr(px - 70, vy - 60, 140, 120, 20), lin_paint(px - 70, 0, px + 70, 0, ["#7F1D1D", "#DC2626", "#7F1D1D"]))
    stem = lerp(150, 40, shut)
    c.drawRect(R(px - 8, vy - 60 - stem, 16, stem), P("#9CA3AF"))
    wy = vy - 60 - stem
    c.save()
    c.translate(px, wy)
    c.rotate(shut * 720 + (math.sin(t * 30) * 6 if wrench > 0.5 and alarm > 0 else 0))
    c.drawCircle(0, 0, 90, P("#DC2626", 1.0, stroke=18))
    for k in range(5):
        ang = math.radians(k * 72)
        c.drawLine(0, 0, math.cos(ang) * 86, math.sin(ang) * 86, P("#B91C1C", 1.0, stroke=10))
    c.drawCircle(0, 0, 16, P("#7F1D1D"))
    c.restore()
    if chain > 0:                                     # a chain through the wheel down to the pipe, with a padlock
        for k in range(10):
            u = k / 9
            cx_, cy_ = lerp(px + 70, px + 40, u), lerp(wy + 20, vy + 120, u)
            c.drawOval(R(cx_ - 12, cy_ - 8, 24, 16), P("#D1D5DB", chain, stroke=5))
        c.drawRRect(rr(px + 10, vy + 120, 60, 54, 10), P("#FACC15", chain))
        c.drawArc(R(px + 20, vy + 96, 40, 44), 180, 180, False, P("#9CA3AF", chain, stroke=8))
        c.drawRRect(rr(px + 90, vy - 30, 90, 70, 10), P("#6B7280", chain))      # the tamper switch box
        c.drawCircle(px + 135, vy + 5, 12, P("#EF4444" if alarm > 0 and int(t * 6) % 2 else "#7F1D1D", chain))
        c.drawLine(px + 180, vy + 5, 760, vy + 5, P("#111827", chain, stroke=5))
        c.drawLine(760, vy + 5, 760, 600, P("#111827", chain, stroke=5))
    bx, by = 800, 560                                 # the alarm bell on the wall
    c.save()
    c.translate(bx, by)
    c.rotate(math.sin(t * 50) * 10 * alarm)
    c.drawCircle(0, 0, 70, lin_paint(-70, 0, 70, 0, ["#7F1D1D", "#EF4444", "#991B1B"]))
    c.drawCircle(0, 0, 18, P("#1F2937"))
    c.restore()
    if alarm > 0:
        for k in range(3):
            u = (t * 1.5 + k / 3) % 1.0
            c.drawArc(R(bx - 90 - 60 * u, by - 90 - 60 * u, 180 + 120 * u, 180 + 120 * u), -60, 120, False,
                      P("#FCA5A5", 0.8 * alarm * (1 - u), stroke=6))
    if wrench > 0:                                    # a big wrench on the wheel
        c.save()
        c.translate(px - 60, wy + 40)
        c.rotate(-30 + 12 * math.sin(t * 6) * wrench)
        c.drawRRect(rr(-260, -14, 260, 28, 10), P("#9CA3AF", wrench))
        c.drawCircle(-270, 0, 30, P("#9CA3AF", wrench, stroke=16))
        c.restore()
    if drip > 0:                                      # upstairs inset: the head popped, only drops fall
        glass(c, 560, 380, 440, 300, r=24, a=drip)
        c.save()
        c.clipRRect(rr(560, 380, 440, 300, 24), skia.ClipOp.kIntersect, True)
        c.drawRect(R(560, 380, 440, 40), P("#94A3B8", drip))
        head(c, 780, 420, 0.9, burst=1.0, t=t, a=drip)
        for k in range(3):
            u = (t * 0.8 + k / 3) % 1.0
            c.drawCircle(780, 520 + u * 120, 6, P(WATER, drip * (1 - u)))
        fire(c, 780, 670, 70, t, drip, seed=8)
        v2.smoke(c, 780, 600, t, 0.0, rate=8, life=2.0, spread=(120, -30), rise=-50, size=(16, 50), col="#64748B",
                 seed=9, a=0.6 * drip)
        c.restore()


def ring_gauge(c, x, y, r, p, label, a=1.0):
    """A ring that fills to p (0..1) with a big percent in the middle."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#0B1220", 0.75 * a))
    c.drawCircle(x, y, r - 18, P("#334155", a, stroke=26))
    c.drawArc(R(x - r + 18, y - r + 18, 2 * r - 36, 2 * r - 36), -90, 360 * p, False, P(GOOD, a, stroke=26))
    text(c, f"{int(round(77 * p / 0.77)) if p < 0.77 else 77}%", x, y + 34, 110, INK, "Poppins-Black", a=a)
    if arabic.is_ar(label):
        arabic.text_ar(c, label, x, y + 98, 30, INK, "Tajawal-Black", a=a)
    else:
        text(c, label, x, y + 94, 26, INK, "Poppins-Black", a=a)


def cake(c, x, y, t, n=90, a=1.0):
    """A big birthday cake on a table edge at (x, y) with a field of n little candle flames."""
    c.drawOval(R(x - 230, y - 20, 460, 60), P("#E2E8F0", a))
    c.drawRect(R(x - 200, y - 170, 400, 160), lin_paint(x - 200, 0, x + 200, 0, ["#F9A8D4", "#FBCFE8", "#F472B6"], a=a))
    c.drawOval(R(x - 200, y - 200, 400, 60), P("#FCE7F3", a))
    rng = random.Random(1)
    for k in range(n):
        cx_ = x + rng.uniform(-180, 180)
        cy_ = y - 172 + rng.uniform(-22, 22)
        c.drawRect(R(cx_ - 3, cy_ - 34, 6, 34), P(rng.choice(["#60A5FA", "#FDE047", "#F87171", "#A78BFA"]), a))
        tongue(c, cx_, cy_ - 34, 12, 24, t, seed=k, a=a)
    add_glow(c, x, y - 240, 240, "#FDBA74", 0.2 * a)


def mabkhara(c, x, y, t, a=1.0):
    """An incense burner held at (x, y) with clouds of fragrant smoke."""
    c.drawRect(R(x - 34, y - 10, 68, 50), lin_paint(x - 34, 0, x + 34, 0, ["#78350F", "#D97706", "#78350F"], a=a))
    c.drawRect(R(x - 44, y - 30, 88, 22), P("#B45309", a))
    c.drawRect(R(x - 24, y + 40, 48, 30), P("#92400E", a))
    add_glow(c, x, y - 30, 60, "#FB923C", 0.6 * a)
    for k in range(10):
        u = (t * 0.35 + k / 10) % 1.0
        puff(c, x + math.sin(t + k) * 60 * u, y - 40 - u * 560, lerp(20, 110, u), "#E5E7EB", 0.45 * (1 - u) * a)


# ====================================================================================== the episode
class Sprinkler(EpisodeV2):
    BUILD_NO = 101
    FIRST_SET = "office"
    CLEAR = "#0B1020"
    TITLE = {"en": "FIRE SPRINKLER", "ar_sa": "رشاش الحريق"}
    EMPH = {"en": ["ONE", "FIRE", "HUNDRED", "SPRINKLERS", "ONLY", "FAST", "SPRINKLER", "ENOUGH", "EIGHTEEN",
                   "SEVENTY-FOUR", "PIANO", "MELTS", "MOVIES", "CEILING", "SOAKED", "GLASS", "BULB", "HEAT", "SWELLS",
                   "POP", "OVEN", "COLORS", "RED", "SEVENTY", "BLUE", "TWENTY", "FAIL", "SHUT", "WATER", "VALVE", "SOAKS", "OFFICE",
                   "LOCKED", "ALARM", "FOLLOW", "TOWERS", "UMBRELLAS", "USUALLY", "YES", "MOST", "JOB", "CONGRATS",
                   "YOURSELF", "NINETY", "CANDLES", "NOTHING"],
            "ar_sa": ["حريق", "مية", "رشاش", "واحد", "يشتغل", "بسرعة", "يكفي", "ألف", "بيانوهات", "يذوب", "الأفلام",
                      "السقف", "يتغرّق", "زجاج", "الحرارة", "وطق", "فرن", "يكسرها", "ألوان", "الحمرا", "سبعين",
                      "والزرقا", "تفشل", "الموية", "المحبس", "مفتوح", "إنذار", "متابعة", "أبراج", "مظلاتها", "غالباً",
                      "كفّى", "مبروك", "يبخّر", "بالعود", "الرشاش", "شي"]}
    KEYS = {"ar_sa": {
        ("hook", "FIRE"): "حريق", ("hook", "HUNDRED"): "مية", ("hook", "ONLY"): "بس",
        ("break1", "FIRE"): "الحريق", ("break1", "FAST"): "بسرعة", ("break1", "ENOUGH"): "يكفي",
        ("fix1", "EIGHTEEN"): "ألف", ("fix1", "PIANO"): "بيانوهات", ("fix1", "MELTS"): "يذوب",
        ("break2", "MOVIES"): "الأفلام", ("break2", "SOAK"): "يفتح", ("break2", "OFFICE"): "يتغرق",
        ("fix2", "GLASS"): "زجاج", ("fix2", "HEAT"): "الحرارة", ("fix2", "POP"): "طق",
        ("break3", "OVEN"): "فرن", ("break3", "POP"): "يكسرها", ("break3", "FIRE"): "حريق",
        ("fix3", "COLORS"): "ألوان", ("fix3", "RED"): "الحمرا", ("fix3", "BLUE"): "زرقا",
        ("break4", "REASON"): "سبب", ("break4", "FAIL"): "تفشل", ("break4", "SHUT"): "سكر",
        ("fix4", "VALVE"): "المحبس", ("fix4", "LOCKED"): "يتربط", ("fix4", "ALARM"): "نذار",
        ("cta", "FOLLOW"): "متابعة", ("cta", "UMBRELLAS"): "مظلاتها",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "USUALLY"): "غالبا", ("reveal", "ONE"): "واحد",
        ("stat", "ONE"): "حبة", ("stat", "SEVENTY"): "سبعين", ("stat", "SPRINKLER"): "ورشاش",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "NINETY"): "يبخر", ("tag", "STARES"): "يطالع", ("tag", "NOTHING"): "شي"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: towers that open umbrellas"),
                   "stat": [("1", "GLASS BULB"), ("68°C", "A RED ONE POPS"), ("77%", "OF FIRES: ONE HEAD")],
                   "L": {"hundred": "100 SPRINKLERS", "one": "ONLY ONE TURNS ON", "fast": "FIRE SPREADS FAST",
                         "enough": "IS ONE ENOUGH?", "y1874": "1874: A PIANO FACTORY", "melts": "METAL THAT MELTS",
                         "movie": "IN THE MOVIES...", "soaked": "EVERYTHING SOAKED!", "bulb": "A TINY GLASS BULB",
                         "swell": "HEAT SWELLS THE LIQUID", "pop": "POP!", "nofire": "NO FIRE AT ALL!",
                         "colors": "BULBS COME IN COLORS", "blue": "BLUE WAITS FOR 121°C", "shut": "WATER SHUT OFF",
                         "top": "TOP REASON THEY FAIL", "locked": "LOCKED OPEN", "alarm": "TURN IT = ALARM",
                         "onehead": "ONE HEAD DID THE JOB", "name": "FIRE SPRINKLER", "stare": "...NOTHING!",
                         "ninety": "90 CANDLES"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: أبراج تفتح مظلاتها"),
                      "stat": [("1", "حبة زجاج"), ("68°", "الحمرا تنكسر"), ("77%", "حرايق كفاها رشاش")],
                      "L": {"hundred": "مية رشاش", "one": "واحد بس يشتغل", "fast": "الحريق ينتشر بسرعة",
                            "enough": "رشاش واحد يكفي؟", "y1874": "1874: مصنع بيانو", "melts": "معدن يذوب",
                            "movie": "في الأفلام...", "soaked": "كل شي يتغرّق!", "bulb": "حبة زجاج صغيرة",
                            "swell": "الحرارة تنفخ السائل", "pop": "طق!", "nofire": "بدون أي حريق!",
                            "colors": "الحبات ألوان", "blue": "الزرقا تصبر لين 121°", "shut": "أحد سكّر الموية",
                            "top": "أكثر سبب للفشل", "locked": "مربوط مفتوح", "alarm": "لو لفّه = إنذار",
                            "onehead": "رشاش واحد كفّى", "name": "رشاش الحريق", "stare": "...ولا شي!",
                            "ninety": "بخور العود"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "fire0": ("hook", "FIRE", 0.2), "hundred": ("hook", "HUNDRED", 0.45), "only": ("hook", "ONLY", 0.75),
            "fire1": ("break1", "FIRE", 0.05), "fast": ("break1", "FAST", 0.3), "enough": ("break1", "ENOUGH", 0.9),
            "y1874": ("fix1", "EIGHTEEN", 0.15), "piano": ("fix1", "PIANO", 0.45), "melts": ("fix1", "MELTS", 0.9),
            "movies": ("break2", "MOVIES", 0.2), "ceiling": ("break2", "SOAK", 0.5), "soaked": ("break2", "OFFICE", 0.85),
            "glass": ("fix2", "GLASS", 0.3), "heat": ("fix2", "HEAT", 0.6), "pop": ("fix2", "POP", 0.9),
            "oven": ("break3", "OVEN", 0.3), "pop3": ("break3", "POP", 0.5), "nofire": ("break3", "FIRE", 0.85),
            "colors": ("fix3", "COLORS", 0.2), "red": ("fix3", "RED", 0.4), "blue": ("fix3", "BLUE", 0.75),
            "reason": ("break4", "REASON", 0.3), "fail": ("break4", "FAIL", 0.5), "shut": ("break4", "SHUT", 0.85),
            "valve": ("fix4", "VALVE", 0.2), "locked": ("fix4", "LOCKED", 0.45), "alarm": ("fix4", "ALARM", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "answer": ("reveal", "ANSWER", 0.05), "usually": ("reveal", "USUALLY", 0.25), "one2": ("reveal", "ONE", 0.7),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "SEVENTY", 0.4), "s3": ("stat", "SPRINKLER", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_ninety": ("tag", "NINETY", 0.1), "t_stares": ("tag", "STARES", 0.5), "t_nothing": ("tag", "NOTHING", 0.85)})
        T["burst0"] = max(T["only"], T["hundred"] + 0.3)
        T["fast1"] = max(T["fast"], T["fire1"]) + 0.2
        T["melt1"] = max(T["melts"], T["piano"]) + 0.1
        T["soak1"] = max(T["soaked"], T["ceiling"]) + 0.1
        T["pop1"] = max(T["pop"], T["heat"] + 0.3)
        T["pop3a"] = max(T["pop3"], T["oven"] + 0.3)
        T["blue1"] = max(T["blue"], T["red"]) + 0.2
        T["shut1"] = max(T["shut"], T["fail"]) + 0.1
        T["alarm1"] = max(T["alarm"], T["locked"]) + 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "factory", 1)
        self.cut(s("break2") - 0.12, "office", -1)
        self.cut(s("fix2") - 0.12, "bulb", 1)
        self.cut(s("break3") - 0.12, "bakery", -1)
        self.cut(s("break4") - 0.12, "valve", 1)
        self.cut(s("cta") - 0.12, "office", -1)
        self.cut(s("closer") - 0.12, "bulb", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["fast1"], T["melt1"]), (T["soak1"], T["pop1"]), (T["pop3a"], T["blue1"]), (T["shut1"], T["alarm1"])]
        self.shakes = [(T["burst0"], 0.3, 6), (T["fast1"], 0.35, 6), (T["soak1"], 0.35, 7), (T["pop1"], 0.3, 8),
                       (T["pop3a"], 0.3, 7), (T["shut1"], 0.35, 7), (T["alarm1"], 0.4, 7), (s("closer") + 0.2, 0.35, 6),
                       (T["t_nothing"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: office (hook, break2, cta, reveal, stat)
    def draw_office(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        z = 1.0 + 0.05 * prog(t, 0, s("break1"))
        c.save()
        c.translate(540, 760)
        c.scale(z, z)
        c.translate(-540, -760)
        if ph == "hook":
            b = prog(t, T["burst0"] - 0.05, T["burst0"] + 0.35)
            office(c, t, burst=b, fire_k=lerp(0.6, 1.0, prog(t, 0, T["hundred"])) * (1 - 0.8 * prog(t, T["burst0"] + 0.3,
                   s("break1"))))
        elif ph == "break2":
            on = prog(t, T["ceiling"] - 0.3, T["ceiling"] + 0.4)
            office(c, t, burst=on, fire_k=0.5 * (1 - on), all_on=on, film=prog(t, s("break2"), T["movies"] + 0.3))
        else:                                         # cta, reveal, stat: one head, the fire out
            office(c, t, burst=1.0, fire_k=0.0, one=lerp(1.0, 0.55, prog(t, s("cta"), s("cta") + 1.0)), calm=1.0)
            if ph == "reveal":
                ring_gauge(c, 540, 600, 220, 0.77 * e_out(prog(t, T["usually"], T["one2"] + 0.6)), self.L["onehead"],
                           a=prog(t, T["answer"] - 0.1, T["answer"] + 0.3))
        c.restore()

    def ui_office(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "hundred", T["hundred"] - 0.1, T["burst0"] - 0.05, accent=INK, size=50)
            self.chip(540, 300, "one", T["burst0"] - 0.05, s("break1") + 0.1, accent=HILITE, size=52)
        elif ph == "break2":
            self.chip(540, 300, "movie", T["movies"] - 0.2, T["soaked"] - 0.15, accent="#F8FAFC", size=50)
            self.chip(540, 300, "soaked", T["soaked"] - 0.15, s("fix2") - 0.15, accent=WARN, size=52)
            self.badge("alert", T["soak1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["soak1"], 1.2)

    # ------------------------------------------------------------------ set: factory (break1, fix1)
    def draw_factory(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        spread = prog(t, T["fire1"], T["enough"] + 0.4)
        if ph == "break1":
            factory(c, t, spread=spread)
        else:
            m = prog(t, T["melts"] - 0.2, T["melts"] + 0.4)
            factory(c, t, spread=1.0 - 0.6 * prog(t, T["melt1"] + 0.3, s("break2")), close=prog(t, s("fix1"), T["piano"]),
                    melt=m, water=prog(t, T["melt1"], T["melt1"] + 0.3))

    def ui_factory(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "fast", T["fast"] - 0.2, T["enough"] - 0.3, accent=WARN, size=50)
            self.chip(540, 300, "enough", T["enough"] - 0.3, s("fix1") - 0.1, accent=HILITE, size=54)
            self.badge("alert", T["fast1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["fast1"], 1.2)
        else:
            self.chip(540, 300, "y1874", T["y1874"] - 0.1, T["melts"] - 0.1, accent="#FDE68A", size=46)
            self.chip(540, 300, "melts", T["melts"] - 0.1, s("break2") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["melt1"], s("break2") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: bulb (fix2, closer)
    def draw_bulb(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "closer":
            bulb_macro(c, t, shine=1.0)
            return
        heat = prog(t, T["glass"], T["heat"] + 0.2)
        fill = prog(t, T["heat"], T["pop1"])
        burst = prog(t, T["pop1"], T["pop1"] + 0.5)
        bulb_macro(c, t, heat=heat, fill=fill, burst=burst, water=prog(t, T["pop1"] + 0.05, T["pop1"] + 0.3))

    def ui_bulb(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)
            return
        self.chip(540, 300, "bulb", T["glass"] - 0.2, T["heat"] - 0.1, accent=INK, size=48)
        self.chip(540, 300, "swell", T["heat"] - 0.1, T["pop1"] - 0.05, accent="#FDBA74", size=46)
        self.chip(540, 300, "pop", T["pop1"] - 0.05, s("break3") - 0.15, accent=GOOD, size=60)
        self.badge("check", T["pop1"] + 0.1, s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: bakery (break3, fix3)
    def draw_bakery(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break3":
            pop = prog(t, T["pop3a"], T["pop3a"] + 0.4)
            bakery(c, t, pop=pop, water=prog(t, T["pop3a"] + 0.1, T["pop3a"] + 0.4))
        else:
            chart = prog(t, T["colors"] - 0.2, T["colors"] + 0.4) * (1 - prog(t, T["blue"] + 0.3, T["blue"] + 0.7))
            bakery(c, t, blue=prog(t, T["blue"], T["blue"] + 0.4), chart=chart)

    def ui_bakery(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "nofire", T["pop3a"] - 0.1, s("fix3") - 0.15, accent=WARN, size=52)
            self.badge("alert", T["pop3a"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["pop3a"], 1.2)
        else:
            self.chip(540, 300, "colors", T["colors"] - 0.2, T["blue"] - 0.1, accent=HILITE, size=48)
            self.chip(540, 300, "blue", T["blue"] - 0.1, s("break4") - 0.15, accent="#60A5FA", size=46)
            self.badge("check", T["blue1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: valve (break4, fix4)
    def draw_valve(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break4":
            sh = prog(t, T["reason"], T["shut1"])
            valve_room(c, t, shut=sh, flow=1 - sh, drip=prog(t, T["shut1"] - 0.2, T["shut1"] + 0.3))
        else:
            valve_room(c, t, shut=1 - prog(t, s("fix4"), T["valve"] + 0.3), chain=prog(t, T["locked"] - 0.2, T["locked"] + 0.3),
                       wrench=prog(t, T["alarm"] - 0.5, T["alarm"] - 0.1), alarm=prog(t, T["alarm1"], T["alarm1"] + 0.2),
                       flow=prog(t, s("fix4"), T["valve"] + 0.3))

    def ui_valve(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "top", T["reason"] - 0.2, T["shut"] - 0.15, accent=HILITE, size=46)
            self.chip(540, 300, "shut", T["shut"] - 0.15, s("fix4") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["shut1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["shut1"], 1.2)
        else:
            self.chip(540, 300, "locked", T["locked"] - 0.2, T["alarm"] - 0.1, accent=GOOD, size=50)
            self.chip(540, 300, "alarm", T["alarm"] - 0.1, s("cta") - 0.15, accent=WARN, size=50)
            self.badge("check", T["alarm1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        look = prog(t, T["t_stares"] - 0.2, T["t_stares"] + 0.3)
        if not self.rtl:                              # grandpa's cake with ninety candles
            vrect(c, 0, 0, W, H, ["#3B2A4A", "#4C1D95"])
            c.drawRect(R(0, 300, W, 40), P("#CBD5E1"))
            c.drawRect(R(0, 340, W, 12), P(PIPE))
            head(c, 540, 352, 2.0, t=t)
            c.drawRect(R(0, 1060, W, 190), P("#7C2D12"))
            cake(c, 540, 1060, t, a=1.0)
            for i, (px, col) in enumerate(((180, "#22C55E"), (330, "#F97316"), (760, "#0EA5E9"), (900, "#EAB308"))):
                person(c, px, 1200, 300, col, t + i, pose="look" if look > 0.5 else "cheer", face=1 if px < 540 else -1)
            person(c, 540, 1240, 260, "#94A3B8", t, pose="look" if look > 0.5 else "stand", face=1, hair="#E5E7EB")
        else:                                         # dad's incense in a hotel room
            vrect(c, 0, 0, W, H, ["#1E3A5F", "#274B73"])
            c.drawRect(R(0, 300, W, 40), P("#E5E7EB"))
            c.drawRect(R(0, 340, W, 12), P(PIPE))
            head(c, 540, 352, 2.0, t=t)
            c.drawRect(R(0, 1080, W, 170), P("#A16207"))
            c.drawRRect(rr(620, 880, 420, 200, 24), P("#F8FAFC"))       # the hotel bed
            c.drawRRect(rr(640, 840, 160, 70, 20), P("#E2E8F0"))
            mabkhara(c, 330, 900, t)
            person(c, 330, 1200, 330, "#F8FAFC", t, pose="carry", face=1, hair="#111827")
            for i, (px, col) in enumerate(((150, "#F97316"), (760, "#22C55E"), (920, "#A855F7"))):
                person(c, px, 1220, 260, col, t + i, pose="look" if look > 0.5 else "stand", face=1 if px < 540 else -1)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300 if not self.rtl else 260, "ninety", T["t_ninety"] - 0.1, T["t_nothing"] - 0.15, accent="#FDE68A", size=46)
        self.chip(540, 300 if not self.rtl else 260, "stare", T["t_nothing"] - 0.15, self.duration + 1, accent=HILITE, size=56)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1F2937", "#111827"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["fire0"], sfx.sizzle(1.2, 62), -12), (T["hundred"], sfx.tick(), -8),
              (T["burst0"], sfx.snap(63), -4), (T["burst0"] + 0.05, sfx.hiss(1.4, 64), -10)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 65), -6), (T["fast1"], sfx.sizzle(1.4, 66), -8),
               (T["fast1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 67), -6), (T["melts"], sfx.hiss(0.8, 68), -12),
               (T["melt1"], sfx.ding(), -8), (T["melt1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, True, 69), -6), (T["ceiling"], sfx.hiss(2.0, 70), -6),
               (T["soak1"], sfx.womp(), -10), (T["soak1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.45, False, 71), -6), (T["heat"], sfx.riser(1.0, 72), -12),
               (T["pop1"], sfx.snap(73), -2), (T["pop1"] + 0.05, sfx.hiss(1.0, 74), -10), (T["pop1"] + 0.3, sfx.ding(), -8)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 75), -6), (T["pop3a"], sfx.snap(76), -4),
               (T["pop3a"] + 0.1, sfx.hiss(1.0, 77), -10), (T["pop3a"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, False, 78), -6), (T["colors"], sfx.pop(79), -6),
               (T["blue1"], sfx.ding(), -8), (T["blue1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 80), -6), (T["reason"], sfx.creak(1.0, 81), -8),
               (T["shut1"], sfx.clank(300.0, 0.6, 82), -6), (T["shut1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.45, False, 83), -6), (T["locked"], sfx.lock_click(84), -4),
               (T["alarm1"], sfx.ring(1.3), -10), (T["alarm1"] + 0.2, sfx.ding(), -8)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["usually"], sfx.riser(0.8, 95), -12),
               (T["one2"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(s("closer") - 0.12, sfx.whoosh(0.45, False, 96), -6), (T["cong2"], sfx.pop(101), -2),
               (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 103), -6), (T["t_stares"], sfx.tick(), -8),
               (T["t_nothing"], sfx.womp(), -8)]
        return ev


NAME = "sprinkler"
EPISODE = Sprinkler
