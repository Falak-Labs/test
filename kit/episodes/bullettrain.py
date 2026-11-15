"""Episode 28 - A bullet train.  v2 look: Japan at dusk, six sets with whip cuts.

Sets: line (side view on the viaduct in front of Mount Fuji: the hook, the cta, the stat and the cheer), power (an
old engine drags sixteen heavy cars and crawls; then small motors pop in under every car and the whole train
pulls), map (from above: the old track's level crossing and tight bend throw the train off; then its own track with
wide tilted curves and a bridge over the road), tunnel (a blunt nose shoves the air through the tunnel and the far
end booms; a kingfisher dives without a splash, the nose grows into a beak and the exit stays quiet), quake (a cut
view of the ground: the big wave hits a fast train; then sensors feel the first small wave, the power is cut and the
train is stopped before the big shake), station (the reveal: the cleaning crew, the bow, the doors; the tag: you run
for it and it leaves exactly on time).
Side views: the rail top is y = 0, the train faces right and its nose tip is at x = tip.
"""
from v2_base import *  # noqa: F401,F403

CL, GAP = 470.0, 14.0                       # car length, gap between cars
BT, BB = -150.0, -24.0                      # roof and floor of the cars
WIRE = -300.0                               # the overhead wire
BLUE = "#1D4ED8"
NAVY = "#0B1530"
WHITE = ("#FFFFFF", "#EEF1F5", "#C2CAD6")
DUSK_FUJI = ("#4A3F78", "#2E2A5C")
TIP = 300.0                                 # line / quake sets: the nose tip


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


class Integral:
    """Running integral of f(t) sampled at 60 Hz."""

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


def bolt(c, x, y, s, col, a=1.0):
    """A small lightning bolt centred on (x, y)."""
    p = skia.Path()
    p.moveTo(x + 0.15 * s, y - s)
    p.lineTo(x - 0.45 * s, y + 0.12 * s)
    p.lineTo(x - 0.02 * s, y + 0.12 * s)
    p.lineTo(x - 0.2 * s, y + s)
    p.lineTo(x + 0.45 * s, y - 0.18 * s)
    p.lineTo(x + 0.02 * s, y - 0.18 * s)
    p.close()
    c.drawPath(p, P(col, a))


def nose_shape(tip, k):
    """Outline of the front: k 0 = a short round nose, 1 = a long beak.  Returns (path, nose length)."""
    Ln = lerp(130.0, 400.0, k)
    x0 = tip - Ln
    ty = lerp(-88.0, -46.0, k)
    p = skia.Path()
    p.moveTo(x0, BT)
    p.cubicTo(x0 + Ln * lerp(0.62, 0.40, k), BT, tip - Ln * lerp(0.02, 0.10, k), ty - lerp(48.0, 16.0, k), tip, ty)
    p.cubicTo(tip + 3, ty + lerp(36.0, 12.0, k), tip - Ln * 0.25, BB, x0 + Ln * 0.45, BB)
    p.lineTo(x0, BB)
    p.close()
    return p, Ln


def bogie(c, x, ang, motor=0.0, a=1.0, sparks=0.0, t=0.0):
    c.drawRRect(rr(x - 64, -27, 128, 16, 6), P("#374151", a))
    for wx in (x - 36, x + 36):
        c.drawCircle(wx, -13, 13, P("#111827", a))
        c.drawCircle(wx, -13, 5, P("#9CA3AF", a))
        c.drawLine(wx, -13, wx + math.cos(ang) * 11, -13 + math.sin(ang) * 11, P("#9CA3AF", a, stroke=3))
        if sparks > 0:
            add_glow(c, wx + 6, -2, 26, "#FFB347", sparks * (0.6 + 0.4 * math.sin(t * 50 + wx)) * a)
    if motor > 0:
        k = e_back(clamp(motor))
        add_glow(c, x, -40, 70 * k, "#FACC15", 0.6 * clamp(motor) * a)
        c.drawCircle(x, -40, 19 * k, P("#FACC15", a))
        bolt(c, x, -40, 13 * k, NAVY, a)


def pantograph(c, x, up=1.0, a=1.0):
    top = lerp(BT - 20, WIRE + 4, up)
    c.drawRRect(rr(x - 34, BT - 10, 68, 12, 4), P("#475569", a))
    c.drawLine(x - 26, BT - 6, x + 8, (BT + top) / 2, P("#64748B", a, stroke=5))
    c.drawLine(x + 8, (BT + top) / 2, x - 10, top, P("#64748B", a, stroke=5))
    c.drawLine(x - 40, top, x + 22, top, P("#94A3B8", a, stroke=6))


def train_side(c, tip, n=6, k=1.0, ang=0.0, lit=0.2, motors=None, panto=1.0, a=1.0, sparks=0.0, t=0.0, doors=0.0):
    """The bullet train from the side, nose tip at x = tip (facing right), n cars.  motors 0..1 pops a motor in
    under every bogie, car after car.  doors 0..1 slides the doors open."""
    p, Ln = nose_shape(tip, k)
    L0 = CL * 0.62
    cars = [(tip - Ln - L0, tip)]
    xr = tip - Ln - L0 - GAP
    for i in range(1, n):
        cars.append((xr - CL, xr))
        xr -= CL + GAP
    for i, (xl, xr_) in enumerate(cars):                                     # bogies (and motors)
        right = xr_ if i else tip - Ln * 0.5
        for bx in (xl + 74, right - 74):
            bogie(c, bx, ang, a=a, sparks=sparks, t=t)
    for i in range(1, n):                                                    # gangways
        c.drawRect(R(cars[i][1] - 4, BT + 24, cars[i - 1][0] - cars[i][1] + 8, BB - BT - 34), P("#4B5563", a))
    body_p = lin_paint(0, BT, 0, BB, list(WHITE), a=a)
    for i, (xl, xr_) in enumerate(cars):
        x_end = tip - Ln + 30 if i == 0 else xr_
        c.drawRRect(rr(xl, BT, x_end - xl, BB - BT, 20), body_p)
        c.drawRect(R(xl + 6, -66, x_end - xl - (6 if i == 0 else 12), 14), P(BLUE, a))
        c.drawRect(R(xl + 6, -46, x_end - xl - (6 if i == 0 else 12), 5), P(BLUE, a))
        nw = int((x_end - xl - 90) / 40)
        for j in range(nw):                                                  # windows
            wx = xl + 60 + j * 40
            c.drawRRect(rr(wx, -122, 26, 32, 7), P(mix("#1E293B", "#FDE68A", lit), a))
            c.drawRRect(rr(wx + 4, -118, 7, 24, 3), P("#FFFFFF", 0.22 * a))
        for dx in ((xl + 14,) if i == 0 else (xl + 14, xr_ - 50)):          # doors
            c.drawRRect(rr(dx, -128, 36, 98, 6), P("#9AA4B2", 0.5 * a, stroke=2))
            if doors > 0:
                c.drawRRect(rr(dx + 2, -126, 32, 94, 5), P("#FDE68A", 0.9 * doors * a))
                add_glow(c, dx + 18, -80, 60, "#FDE68A", 0.35 * doors * a)
        if i in (2, 5) and panto > 0:
            pantograph(c, (xl + xr_) / 2, panto, a)
    if motors is not None and motors > 0:                                    # the motors, on top (x-ray)
        for i, (xl, xr_) in enumerate(cars):
            m = clamp(motors * (n + 1.5) - i * 1.2)
            if m <= 0:
                continue
            right = xr_ if i else tip - Ln * 0.5
            for bx in (xl + 74, right - 74):
                kk = e_back(m)
                add_glow(c, bx, -30, 90 * kk, "#FACC15", 0.7 * m * a)
                c.drawCircle(bx, -30, 26 * kk, P("#FACC15", a))
                c.drawCircle(bx, -30, 26 * kk, P(NAVY, a, stroke=3))
                bolt(c, bx, -30, 17 * kk, NAVY, a)
    c.drawPath(p, body_p)                                                    # the nose
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    c.drawRect(R(tip - Ln - 10, -66, Ln + 20, 14), P(BLUE, a))
    c.drawRect(R(tip - Ln - 10, -46, Ln + 20, 5), P(BLUE, a))
    win = skia.Path()
    win.moveTo(tip - Ln * 0.98, BT + 14)
    win.lineTo(tip - Ln * 0.62, BT + 18)
    win.lineTo(tip - Ln * 0.42, BT + 50 + 10 * k)
    win.lineTo(tip - Ln * 0.95, BT + 52)
    win.close()
    c.drawPath(win, lin_paint(0, BT, 0, BT + 60, ["#0F172A", "#1E3A5F"], a=a))
    c.drawPath(p, lin_paint(0, BT - 10, 0, BT + 60, [("#FFFFFF", 0.35), ("#FFFFFF", 0.0)], a=a))
    c.restore()
    hx, hy = tip - Ln * 0.12, lerp(-60.0, -38.0, k)
    add_glow(c, hx + 30, hy, 90, "#FFF5D6", 0.35 * a)
    c.drawOval(R(hx - 14, hy - 5, 26, 10), P("#FFF8E1", a))
    return cars


def old_train(c, tip, n, ang, t, sparks=0.0, heat=0.0, a=1.0):
    """An old electric engine (boxy, maroon) dragging n heavy brown cars."""
    L = 420.0
    x0 = tip - L
    for k in range(n):                                                       # the heavy cars
        xr = x0 - GAP - k * (CL + GAP)
        xl = xr - CL
        for bx in (xl + 70, xr - 70):
            bogie(c, bx, ang * 0.3, a=a)
        box(c, xl, -158, CL, 134, "#6B4A3A" if k % 2 else "#5C4033", r=8, a=a)
        c.drawRect(R(xl + 10, -150, CL - 20, 10), P("#3F2A20", a))
        for j in range(6):
            c.drawRRect(rr(xl + 40 + j * 70, -120, 40, 30, 4), P("#2A1E18", a))
        c.drawRect(R(xr - 4, -110, GAP + 8, 40), P("#3F3F46", a))
    for bx in (x0 + 80, tip - 80):
        bogie(c, bx, ang, a=a, sparks=sparks, t=t)
    body = skia.Path()
    body.moveTo(x0, -176)
    body.lineTo(tip - 50, -176)
    body.lineTo(tip, -120)
    body.lineTo(tip, -24)
    body.lineTo(x0, -24)
    body.close()
    c.drawPath(body, lin_paint(0, -176, 0, -24, [shade("#9F1239", 0.25), "#9F1239", shade("#9F1239", -0.4)], a=a))
    c.drawRect(R(x0, -70, L, 10), P("#FDE68A", 0.8 * a))
    c.drawRRect(rr(tip - 110, -160, 70, 44, 6), P("#1E293B", a))
    for j in range(3):
        c.drawRRect(rr(x0 + 40 + j * 90, -150, 50, 40, 5), P("#1E293B", a))
    c.drawLine(x0 + 200, -176, x0 + 230, -240, P("#64748B", a, stroke=5))
    c.drawLine(x0 + 230, -240, x0 + 200, WIRE + 4, P("#64748B", a, stroke=5))
    c.drawLine(x0 + 170, WIRE + 4, x0 + 236, WIRE + 4, P("#94A3B8", a, stroke=6))
    if heat > 0:
        add_glow(c, x0 + L / 2, -100, 260, WARN, 0.45 * heat * a)
    c.drawCircle(tip - 14, -60, 9, P("#FFF8E1", a))


def fuji(c, x, base, w, h, a=1.0, snow=1.0):
    """Mount Fuji (screen space), base centred on x."""
    p = skia.Path()
    p.moveTo(x - w / 2, base)
    p.cubicTo(x - w * 0.22, base - h * 0.35, x - w * 0.09, base - h * 0.92, x - w * 0.05, base - h)
    p.lineTo(x + w * 0.05, base - h)
    p.cubicTo(x + w * 0.09, base - h * 0.92, x + w * 0.22, base - h * 0.35, x + w / 2, base)
    p.close()
    c.drawPath(p, lin_paint(0, base - h, 0, base, [DUSK_FUJI[0], DUSK_FUJI[1]], a=a))
    if snow > 0:
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        s = skia.Path()
        yb = base - h * 0.66
        s.moveTo(x - w * 0.3, yb)
        for i in range(13):
            xx = x - w * 0.3 + i * w * 0.05
            s.lineTo(xx, yb + (22 if i % 2 else -8) * (h / 600))
        s.lineTo(x + w * 0.3, yb)
        s.lineTo(x + w * 0.3, base - h - 10)
        s.lineTo(x - w * 0.3, base - h - 10)
        s.close()
        c.drawPath(s, lin_paint(0, base - h, 0, yb, ["#FFFFFF", "#F6D7E6"], a=a * snow))
        c.restore()
    add_glow(c, x, base - h * 0.7, w * 0.4, "#FFB4C8", 0.12 * a)


def kingfisher(c, x, y, s, ang, a=1.0, wing=0.0):
    """A kingfisher (blue back, orange belly, long dagger beak), centred on (x, y), pointing at ang degrees."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    c.drawOval(R(-60, -22, 100, 44), P("#1D9BF0", a))                      # body
    c.drawOval(R(-50, -2, 80, 24), P("#F97316", a))                       # belly
    c.drawCircle(38, -6, 22, P("#0EA5E9", a))                             # head
    c.drawCircle(46, -12, 5, P("#FFFFFF", a))
    c.drawCircle(47, -12, 2.6, P("#0B1020", a))
    bk = skia.Path()                                                       # the beak
    bk.moveTo(54, -16)
    bk.lineTo(118, -2)
    bk.lineTo(54, 6)
    bk.close()
    c.drawPath(bk, P("#1F2937", a))
    tail = skia.Path()
    tail.moveTo(-56, -6)
    tail.lineTo(-96, -16)
    tail.lineTo(-92, 8)
    tail.close()
    c.drawPath(tail, P("#1E40AF", a))
    wg = skia.Path()                                                       # wing, folded for the dive
    wg.moveTo(-30, -14)
    wg.lineTo(14, -18 - 30 * wing)
    wg.lineTo(-44, -2)
    wg.close()
    c.drawPath(wg, P("#2563EB", a))
    c.restore()


def bower(c, x, y, h, shirt, bow, t=0.0, a=1.0, face=1, arm=0.0):
    """A cleaner in uniform and cap who can bow (bow 0..1 bends at the hips).  Feet at (x, y)."""
    if a <= 0:
        return
    u = h / 140.0
    c.save()
    c.translate(x, y)
    c.scale(face * u, u)
    c.drawRRect(rr(-14, -62, 12, 62, 5), P("#1F2538", a))                  # legs
    c.drawRRect(rr(2, -62, 12, 62, 5), P("#1F2538", a))
    c.translate(0, -60)
    c.rotate(bow * 42)
    c.drawRRect(rr(-20, -58, 40, 62, 14), P(shirt, a))                    # torso
    sw = math.sin(t * 9) * 26 * arm
    c.drawLine(10, -48, 26 + sw * 0.3, -18 + sw * 0.4, P("#E8B48A", a, stroke=9))  # arm
    c.drawCircle(0, -76, 18, P("#E8B48A", a))                             # head
    c.drawRRect(rr(-19, -98, 38, 16, 7), P(shirt, a))                     # cap
    c.drawRRect(rr(2, -88, 26, 6, 3), P(shade(shirt, -0.3), a))
    c.restore()


def briefcase(c, x, y, a=1.0):
    c.drawRRect(rr(x - 22, y - 16, 44, 32, 5), P("#7C2D12", a))
    c.drawRRect(rr(x - 8, y - 22, 16, 8, 3), P("#7C2D12", a, stroke=3))


def gauge(c, x, y, kmh, a=1.0, label=""):
    """A speedometer (screen space): 0..340 km/h."""
    if a <= 0:
        return
    r = 150
    c.save()
    c.translate(x, y)
    k = e_back(clamp(a * 1.3))
    c.scale(k, k)
    c.drawCircle(0, 0, r + 18, P("#000000", 0.45, blur=16))
    c.drawCircle(0, 0, r + 12, P("#0F172A", 0.92))
    c.drawCircle(0, 0, r + 12, P("#FFFFFF", 0.25, stroke=3))
    for i in range(18):
        q = math.radians(150 + i * 240 / 17)
        r0 = r - (22 if i % 2 == 0 else 12)
        col = WARN if i >= 15 else "#E2E8F0"
        c.drawLine(math.cos(q) * r0, math.sin(q) * r0, math.cos(q) * (r - 4), math.sin(q) * (r - 4), P(col, 0.9, stroke=4))
    v = clamp(kmh / 340.0)
    arc = skia.Path()
    arc.addArc(R(-r + 10, -r + 10, 2 * r - 20, 2 * r - 20), 150, 240 * v)
    c.drawPath(arc, P(HILITE, 0.9, stroke=10, cap="butt"))
    q = math.radians(150 + 240 * v)
    c.drawLine(0, 0, math.cos(q) * (r - 28), math.sin(q) * (r - 28), P(WARN, 1, stroke=8))
    c.drawCircle(0, 0, 14, P("#E2E8F0"))
    text(c, f"{int(round(kmh))}", 0, 74, 54, "#FFFFFF", "Poppins-Black")
    text(c, label or "km/h", 0, 112, 26, "#94A3B8", "Poppins-Bold")
    c.restore()


def board(c, x, y, s, a=1.0, col="#FDBA74"):
    """A station clock board showing s (digits), centred on (x, y)."""
    if a <= 0:
        return
    c.drawLine(x - 90, y - 70, x - 90, y - 160, P("#475569", a, stroke=6))
    c.drawLine(x + 90, y - 70, x + 90, y - 160, P("#475569", a, stroke=6))
    c.drawRRect(rr(x - 170, y - 74, 340, 120, 14), P("#0B1020", a))
    c.drawRRect(rr(x - 170, y - 74, 340, 120, 14), P("#64748B", a, stroke=4))
    text(c, s, x, y + 22, 64, col, "Poppins-Black", a=a)


def hstreaks(c, t, a, y0, y1, n=22, seed=3):
    """Screen-space streaks rushing to the left: the train is going fast to the right."""
    if a <= 0:
        return
    rng = random.Random(seed)
    for _ in range(n):
        y = rng.uniform(y0, y1)
        sp, ln = rng.uniform(2400, 4400), rng.uniform(140, 460)
        x = W + 300 - ((t * sp + rng.uniform(0, 3000)) % (W + 900))
        p = P("#FFFFFF", a * rng.uniform(0.08, 0.28), stroke=rng.uniform(2, 5))
        p.setBlendMode(PLUS)
        c.drawLine(x, y, x + ln, y, p)


def path_pts(fn, n=220):
    return [fn(i / (n - 1)) for i in range(n)]


class Poly:
    """A polyline you can walk by distance; at(d) -> (x, y, angle in degrees)."""

    def __init__(self, pts):
        self.pts = pts
        self.cum = [0.0]
        for i in range(len(pts) - 1):
            self.cum.append(self.cum[-1] + math.dist(pts[i], pts[i + 1]))
        self.len = self.cum[-1]

    def at(self, d):
        d = clamp(d, 0.0, self.len)
        lo, hi = 0, len(self.cum) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.cum[mid] <= d:
                lo = mid
            else:
                hi = mid
        seg = self.cum[hi] - self.cum[lo]
        k = (d - self.cum[lo]) / seg if seg else 0.0
        (x0, y0), (x1, y1) = self.pts[lo], self.pts[hi]
        return lerp(x0, x1, k), lerp(y0, y1, k), math.degrees(math.atan2(y1 - y0, x1 - x0))

    def path(self):
        p = skia.Path()
        p.moveTo(*self.pts[0])
        for q in self.pts[1:]:
            p.lineTo(*q)
        return p


def old_track_pts():
    """Map set, the old line (bottom to top): a level crossing, then a tight right-left bend."""
    pts = [(-150.0, 3200.0 - i * 40.0) for i in range(79)]                 # straight up to y = 80
    for i in range(1, 25):                                                  # tight right turn, r = 130
        q = math.radians(180 + i * 90 / 24)
        pts.append((-20 + 130 * math.cos(q), 80 + 130 * math.sin(q)))
    for i in range(1, 8):
        pts.append((-20 + i * 30.0, -50.0))
    for i in range(1, 25):                                                  # tight left turn up
        q = math.radians(90 + i * 90 / 24)
        pts.append((190 + 130 * math.cos(q + math.pi), -180 + 130 * math.sin(q + math.pi)))
    for i in range(1, 50):
        pts.append((320.0, -180 - i * 40.0))
    return pts


def new_track_pts():
    """Map set, its own line: wide, gentle curves."""
    return path_pts(lambda u: (-200 + 560 * math.sin((u - 0.16) * 2.8), 2300 - u * 4600))


def train_top(c, track, s_head, n, t, derail=None, k=1.0, a=1.0):
    """The train from above, its head at distance s_head along track.  derail = (distance, time) where it leaves."""
    for i in range(n):
        L = CL * 0.62 + 260 if i == 0 else CL
        s_mid = s_head - (L / 2 if i == 0 else CL * 0.62 + 260 + GAP + (i - 1) * (CL + GAP) + CL / 2)
        x, y, ang = track.at(s_mid)
        if derail is not None and s_mid > derail[0]:
            dx_, dy_, ang0 = track.at(derail[0])
            u = s_mid - derail[0]
            ue = 900 * (1 - math.exp(-u / 900))
            q = math.radians(ang0)
            side = 1 if i % 2 == 0 else -1
            x = dx_ + math.cos(q) * ue - math.sin(q) * side * ue * 0.25
            y = dy_ + math.sin(q) * ue + math.cos(q) * side * ue * 0.25
            ang = ang0 + side * ue * 0.09
        c.save()
        c.translate(x, y)
        c.rotate(ang)
        c.drawRRect(rr(-L / 2 + 6, -38, L, 86, 30), P("#000000", 0.35 * a, blur=10))
        if i == 0:
            p = skia.Path()
            p.moveTo(-L / 2, -42)
            p.lineTo(L / 2 - 240 * k - 20, -42)
            p.cubicTo(L / 2 - 80, -42, L / 2 - 10, -10, L / 2, 0)
            p.cubicTo(L / 2 - 10, 10, L / 2 - 80, 42, L / 2 - 240 * k - 20, 42)
            p.lineTo(-L / 2, 42)
            p.close()
            c.drawPath(p, lin_paint(0, -42, 0, 42, ["#FFFFFF", "#DDE3EA", "#AEB8C6"], a=a))
            c.drawRRect(rr(L / 2 - 210, -20, 80, 40, 14), P("#0F172A", a))
        else:
            c.drawRRect(rr(-L / 2, -42, L, 84, 26), lin_paint(0, -42, 0, 42, ["#FFFFFF", "#DDE3EA", "#AEB8C6"], a=a))
        c.drawRect(R(-L / 2 + 10, -5, L - (60 if i == 0 else 20), 10), P(BLUE, a))
        c.restore()


# ---------------------------------------------------------------------------------------------- sounds
def screech(d=0.6, seed=2):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 2300 - 500 * tt / d
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * 0.5 + sfx._bp(sfx._rng(seed).standard_normal(n), 1800, 3400)
    return sfx._norm(x * sfx._ar(n, 0.03, d * 0.4), 0.5)


def horn(d=0.9):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = np.sin(2 * np.pi * 311 * tt) + 0.8 * np.sin(2 * np.pi * 370 * tt) + 0.3 * np.sin(2 * np.pi * 622 * tt)
    return sfx._norm(x * sfx._ar(n, 0.03, 0.25), 0.5)


def chime_jp():
    """A short station melody (four soft bells)."""
    out = np.zeros(int(1.6 * sfx.SR))
    for i, f in enumerate((659.3, 523.3, 587.3, 784.0)):
        b = sfx.bell(f, 0.9, 0.6)
        i0 = int(i * 0.3 * sfx.SR)
        out[i0:i0 + len(b)] += b[:len(out) - i0]
    return sfx._norm(out, 0.45)


def rush(d=1.2, seed=90):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 120, 1800)
    return sfx._norm(x * np.sin(np.linspace(0, np.pi, n)) ** 1.5, 0.6)


# ====================================================================================== the episode
class BulletTrain(EpisodeV2):
    BUILD_NO = 28
    COVER_T = ("closer", 0.9)                    # cover: the beak nose in front of Fuji, after the cheer rings
    FIRST_SET = "line"
    CLEAR = "#070B1F"
    TITLE = {"en": "BULLET TRAIN", "ar_sa": "القطر الطلقة"}
    EMPH = {"en": ["CONGRATS", "BIRD'S", "BEAK", "NOSE", "BULLET", "TRAIN", "ONE", "ENGINE", "SIXTEEN", "HEAVY", "SLOW",
                   "MOTORS", "EVERY", "WHOLE", "PULLS", "FAST", "OLD", "TIGHT", "BENDS", "CROSSINGS", "FLIES", "CURVE",
                   "OWN", "TRACK", "WIDE", "TILTED", "NOTHING", "TUNNEL", "SHOVES", "AIR", "BOOMS", "CANNON", "ENGINEER",
                   "BIRDS", "KINGFISHER", "DIVES", "SPLASH", "QUIET", "JAPAN", "EARTHQUAKES", "STOP", "SENSORS", "FIRST",
                   "WAVE", "CUT", "POWER", "BIG", "SHAKE", "FOLLOW", "HUMANOID", "ROBOT", "CREW", "CLEAN", "SEVEN",
                   "MINUTES", "BOW", "DOORS", "THREE", "HUNDRED", "TWENTY", "TWENTY-FOUR", "SECONDS", "YOURSELF", "MISS",
                   "EXACTLY", "TIME"],
            "ar_sa": ["مبروك", "منقار", "الطير", "القطر", "الطلقة", "جرار", "ستاشر", "تقيلة", "بطيء", "موتورات", "كل",
                      "يشد", "سريع", "ملفات", "ومزلقانات", "فيطير", "لوحده", "واسعة", "مايلة", "مزلقانات", "النفق", "يزق",
                      "الهوا", "المدفع", "مهندس", "الطيور", "الرفراف", "بيغطس", "رشة", "هادي", "اليابان", "زلازل", "يقف",
                      "حساسات", "رعشة", "الكهربا", "الهزة", "الكبيرة", "تابعني", "روبوت", "النضافة", "سبع", "دقايق",
                      "وينحنيلك", "الأبواب", "تلتمية", "عربية", "أربعة", "بإيدك", "اتأخرت", "هيمشي", "ميكروباص"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "TRAIN"): "قطر", ("hook", "BEAK"): "منقار", ("hook", "NOSE"): "بوزه", ("hook", "CONGRATS"): "مبروك",
        ("hook", "BULLET"): "الطلقة",
        ("break1", "ENGINE"): "جرار", ("break1", "DRAGGING"): "بيشد", ("break1", "SIXTEEN"): "ستاشر",
        ("break1", "SLOW"): "بطيء",
        ("fix1", "MOTORS"): "موتورات", ("fix1", "EVERY"): "كل", ("fix1", "WHOLE"): "كله", ("fix1", "PULLS"): "يشد",
        ("break2", "FAST"): "سريع", ("break2", "OLD"): "القديمة", ("break2", "BENDS"): "ملفات",
        ("break2", "CROSSINGS"): "مزلقانات", ("break2", "FLIES"): "يطير", ("break2", "CURVE"): "أول",
        ("fix2", "OWN"): "لوحده", ("fix2", "WIDE"): "واسعة", ("fix2", "TILTED"): "مايلة", ("fix2", "CROSSINGS"): "مزلقانات",
        ("fix2", "NOTHING"): "غير",
        ("break3", "TUNNEL"): "النفق", ("break3", "SHOVES"): "يزق", ("break3", "AIR"): "الهوا", ("break3", "FAR"): "آخر",
        ("break3", "BOOMS"): "يضرب", ("break3", "CANNON"): "المدفع",
        ("fix3", "ENGINEER"): "مهندس", ("fix3", "BIRDS"): "الطيور", ("fix3", "KINGFISHER"): "الرفراف",
        ("fix3", "DIVES"): "بيغطس", ("fix3", "SPLASH"): "رشة", ("fix3", "BEAK"): "منقار",
        ("break4", "QUIET"): "هادي", ("break4", "JAPAN"): "اليابان", ("break4", "EARTHQUAKES"): "زلازل",
        ("break4", "FAST"): "بالسرعة", ("break4", "STOP"): "يقف",
        ("fix4", "SENSORS"): "حساسات", ("fix4", "FIRST"): "أول", ("fix4", "WAVE"): "رعشة", ("fix4", "CUT"): "تقطع",
        ("fix4", "POWER"): "الكهربا", ("fix4", "BIG"): "الكبيرة", ("fix4", "HITS"): "الهزة",
        ("cta", "BOARD"): "تركب", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "CREW"): "فريق", ("reveal", "CLEAN"): "يلمعه", ("reveal", "SEVEN"): "سبع", ("reveal", "BOW"): "ينحني",
        ("reveal", "DOORS"): "الأبواب",
        ("stat", "THREE"): "تلتمية", ("stat", "SIXTEEN"): "ستاشر", ("stat", "JUST"): "أربعة",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "AFTER"): "وبعد", ("tag", "MISS"): "اتأخرت", ("tag", "LEFT"): "هيمشي", ("tag", "EXACTLY"): "ثانية",
        ("tag", "TIME"): "ميكروباص"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a humanoid robot"),
                   "stat": [("320", "KM/H"), ("16", "CARS"), ("24 s", "AVERAGE DELAY")],
                   "L": {"train": "YOUR BULLET TRAIN", "beak": "A BIRD'S BEAK", "heavy": "16 HEAVY CARS",
                         "engine": "ONE ENGINE", "slow": "TOO SLOW", "motors": "A MOTOR UNDER EVERY CAR",
                         "pulls": "THE WHOLE TRAIN PULLS", "bends": "TIGHT BEND", "crossing": "ROAD CROSSING",
                         "off": "OFF THE RAILS", "own": "ITS OWN TRACK", "wide": "WIDE CURVES", "tilt": "TILTED INWARD",
                         "bridge": "NO CROSSINGS", "push": "AIR SQUEEZED AHEAD", "boom": "BOOM!",
                         "kingfisher": "KINGFISHER", "nosplash": "NO SPLASH", "beaknose": "A BEAK FOR A NOSE",
                         "quiet": "QUIET", "quake": "EARTHQUAKE", "cantstop": "CAN'T STOP IN TIME",
                         "sensors": "SENSORS", "pwave": "FIRST SMALL WAVE", "cut": "POWER CUT", "swave": "THE BIG SHAKE",
                         "stopped": "ALREADY STOPPED", "crew": "CLEANING CREW", "doors": "DOORS OPEN",
                         "ontime": "LEFT EXACTLY ON TIME", "wait": "WAIT!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: روبوت شبه البني آدم"),
                      "stat": [("320", "كم/س"), ("16", "عربية"), ("24", "ثانية تأخير")],
                      "L": {"train": "القطر الطلقة بتاعك", "beak": "منقار طير", "heavy": "16 عربية تقيلة",
                            "engine": "جرار واحد", "slow": "بطيء أوي", "motors": "موتور تحت كل عربية",
                            "pulls": "القطر كله بيشد", "bends": "ملف ضيق", "crossing": "مزلقان",
                            "off": "طار من السكة", "own": "سكة لوحده", "wide": "ملفات واسعة", "tilt": "مايلة لجوه",
                            "bridge": "من غير مزلقانات", "push": "الهوا بيتزق قدامه", "boom": "بووم!",
                            "kingfisher": "الرفراف", "nosplash": "من غير رشة", "beaknose": "بوز زي المنقار",
                            "quiet": "هادي", "quake": "زلزال", "cantstop": "مش هيلحق يقف",
                            "sensors": "حساسات", "pwave": "أول رعشة", "cut": "الكهربا اتقطعت", "swave": "الهزة الكبيرة",
                            "stopped": "وقف خلاص", "crew": "فريق النضافة", "doors": "الأبواب اتفتحت",
                            "ontime": "مشي في ميعاده بالثانية", "wait": "استنى!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "train": ("hook", "TRAIN", 0.15), "beak": ("hook", "BEAK", 0.4), "nose": ("hook", "NOSE", 0.55),
            "congrats": ("hook", "CONGRATS", 0.65), "bullet": ("hook", "BULLET", 0.9),
            "engine": ("break1", "ENGINE", 0.15), "dragging": ("break1", "DRAGGING", 0.3),
            "sixteen": ("break1", "SIXTEEN", 0.45), "slow": ("break1", "SLOW", 0.75),
            "motors": ("fix1", "MOTORS", 0.25), "every": ("fix1", "EVERY", 0.45), "whole": ("fix1", "WHOLE", 0.75),
            "pulls": ("fix1", "PULLS", 0.9),
            "fast2": ("break2", "FAST", 0.1), "old": ("break2", "OLD", 0.25), "bends": ("break2", "BENDS", 0.45),
            "crossings": ("break2", "CROSSINGS", 0.6), "flies": ("break2", "FLIES", 0.8), "curve": ("break2", "CURVE", 0.95),
            "own": ("fix2", "OWN", 0.15), "wide": ("fix2", "WIDE", 0.35), "tilted": ("fix2", "TILTED", 0.55),
            "nocross": ("fix2", "CROSSINGS", 0.75), "nothing": ("fix2", "NOTHING", 0.9),
            "tunnel": ("break3", "TUNNEL", 0.25), "shoves": ("break3", "SHOVES", 0.4), "air": ("break3", "AIR", 0.5),
            "far": ("break3", "FAR", 0.7), "booms": ("break3", "BOOMS", 0.85), "cannon": ("break3", "CANNON", 0.95),
            "engineer": ("fix3", "ENGINEER", 0.1), "birds": ("fix3", "BIRDS", 0.25), "kingfisher": ("fix3", "KINGFISHER", 0.4),
            "dives": ("fix3", "DIVES", 0.55), "splash": ("fix3", "SPLASH", 0.72), "beak3": ("fix3", "BEAK", 0.95),
            "quiet": ("break4", "QUIET", 0.1), "japan": ("break4", "JAPAN", 0.3), "quakes": ("break4", "EARTHQUAKES", 0.45),
            "fast4": ("break4", "FAST", 0.65), "stop4": ("break4", "STOP", 0.9),
            "sensors": ("fix4", "SENSORS", 0.1), "first": ("fix4", "FIRST", 0.35), "wave4": ("fix4", "WAVE", 0.45),
            "cut": ("fix4", "CUT", 0.6), "power": ("fix4", "POWER", 0.7), "big": ("fix4", "BIG", 0.85),
            "hits": ("fix4", "HITS", 0.95),
            "board": ("cta", "BOARD", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "crew": ("reveal", "CREW", 0.15), "clean": ("reveal", "CLEAN", 0.3), "seven": ("reveal", "SEVEN", 0.45),
            "bow": ("reveal", "BOW", 0.7), "doors": ("reveal", "DOORS", 0.92),
            "s1": ("stat", "THREE", 0.04), "s2": ("stat", "SIXTEEN", 0.45), "s3": ("stat", "JUST", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "after": ("tag", "AFTER", 0.1), "miss": ("tag", "MISS", 0.35), "left": ("tag", "LEFT", 0.6),
            "exactly": ("tag", "EXACTLY", 0.8), "time": ("tag", "TIME", 0.92)})
        T["derail"] = max(T["flies"], T["curve"]) - 0.35                     # break2: it leaves the bend
        T["hit4"] = T["stop4"] - 0.15                                        # break4: the big wave reaches the train
        T["cut4"] = min(T["cut"], T["power"]) - 0.1                          # fix4: the power goes off, brakes
        T["shake4"] = max(T["big"], T["hits"], T["cut4"] + 1.9) + 0.1          # fix4: the big wave arrives (stopped)
        T["go"] = min(T["after"] + 0.5, T["left"] - 0.6)                       # tag: the train pulls out
        T["bowt"] = T["bow"] - 0.1
        dur = self.tl.duration + 1
        self.v_tun = Track(0.0).to(T["splash"] - 0.2, 1700.0, 0.5, e_in)
        self.d_tun = Integral(lambda t: self.v_tun.at(t), 0, dur)
        tt = T["splash"] - 0.2
        while self.d_tun.at(tt) < 80 and tt < dur:
            tt += 1 / 60
        T["in3b"] = tt                                                       # fix3: the beak nose enters the tunnel
        # ---- sets
        self.cut(s("break1") - 0.12, "power", 1)
        self.cut(s("fix1") - 0.12, "power", -1)                    # same set: the old engine is swapped for motors
        self.cut(s("break2") - 0.12, "map", 1)
        self.cut(s("fix2") - 0.12, "map", -1)                      # same set: its own track
        self.cut(s("break3") - 0.12, "tunnel", 1)
        self.cut(s("fix3") - 0.12, "tunnel", -1)                   # same set: the beak nose
        self.cut(s("break4") - 0.12, "quake", 1)
        self.cut(s("fix4") - 0.12, "quake", -1)                    # same set: the sensors
        self.cut(s("cta") - 0.12, "line", 1)
        self.cut(s("reveal") - 0.12, "station", 1)
        self.cut(s("stat") - 0.12, "line", -1)
        self.cut(s("tag") - 0.2, "station", 1)
        self.cams = {"line": Camera(60, -40, 1.8), "power": Camera(-250, -170, 0.95), "map": Camera(0, 300, 0.62),
                     "tunnel": Camera(-170, -300, 0.6), "quake": Camera(-150, 330, 0.7), "station": Camera(-200, -300, 1.15)}
        cm = self.cams
        cm["line"].key(0.1, 20, -60, 1.7, max(0.8, T["beak"] - 0.3))
        cm["line"].key(T["beak"] - 0.2, 150, -90, 2.3, 0.9)
        cm["line"].key(T["bullet"] - 0.5, -200, -200, 1.05, 1.1)
        cm["line"].key(s("cta") - 0.12, -260, -200, 1.0, 0.0)
        cm["line"].key(s("stat") - 0.12, -320, -250, 0.82, 0.0).key(s("stat"), -300, -245, 0.84, 3.0)
        cm["line"].key(s("closer") - 0.25, 60, -40, 1.8, 0.8)
        cm["power"].key(s("break1"), -220, -170, 0.97, 3.5)
        cm["power"].key(s("fix1") - 0.12, -250, -170, 0.95, 0.0).key(s("fix1"), -230, -165, 0.98, 3.5)
        cm["map"].key(s("break2"), 40, 260, 0.64, 3.0).key(T["derail"] - 0.4, 60, 120, 0.8, 1.0)
        cm["map"].key(s("fix2") - 0.12, 0, 300, 0.6, 0.0).key(s("fix2"), 0, 280, 0.62, 3.5)
        cm["tunnel"].key(s("break3") - 0.12, -170, -300, 0.6, 0.0).key(s("break3"), 140, -300, 0.62, max(1.0, T["booms"] - s("break3")))
        cm["tunnel"].key(s("fix3") - 0.12, -720, -200, 1.2, 0.0).key(s("fix3"), -740, -210, 1.25, 1.5)
        cm["tunnel"].key(T["in3b"] - 0.35, 60, -300, 0.62, 0.8)
        cm["quake"].key(s("break4"), -130, 320, 0.72, 3.0)
        cm["quake"].key(s("fix4") - 0.12, -150, 330, 0.7, 0.0)
        cm["station"].key(s("reveal"), -170, -300, 1.18, 3.5)
        cm["station"].key(s("tag") - 0.2, -420, -300, 1.1, 0.0).key(s("tag"), -380, -290, 1.15, 2.5)
        # ---- tracks
        dur = self.tl.duration + 1
        self.v_line = Track(2600.0).to(s("stat"), 2200.0, 0.1)
        self.d_line = Integral(lambda t: self.v_line.at(t), 0, dur)
        self.v_pow = Track(0.0).to(s("break1"), 380.0, 3.0, e_in)                # crawling
        self.v_pow.to(s("fix1") - 0.12, 0.0, 0.0).to(T["whole"] - 0.2, 2600.0, 1.4, e_in)
        self.d_pow = Integral(lambda t: self.v_pow.at(t), 0, dur)
        self.spin_pow = Track(0.0).to(s("break1"), 14.0, 0.8).to(s("fix1") - 0.12, 0.0, 0.0)
        self.a_pow = Integral(lambda t: self.spin_pow.at(t) + self.v_pow.at(t) / 13.0, 0, dur)
        self.kmh_pow = Track(0.0).to(s("break1") + 0.2, 42.0, max(1.5, T["slow"] - s("break1") + 0.5))
        self.kmh_pow.to(s("fix1") - 0.12, 0.0, 0.0).to(T["whole"] - 0.2, 320.0, 1.4, e_io)
        self.motors = Track(0.0).to(T["motors"] - 0.1, 1.0, max(0.9, T["every"] - T["motors"] + 0.6), lambda u: u)
        self.v_map = Track(2300.0).to(T["derail"] + 0.05, 0.0, 0.9, e_out)
        self.v_map.to(s("fix2") - 0.12, 1500.0, 0.0)
        self.s_map = Integral(lambda t: self.v_map.at(t), 0, dur)
        self.nose = Track(0.0).to(max(T["kingfisher"], s("fix3") + 0.6), 1.0, max(1.0, T["beak3"] - T["kingfisher"]), e_io)
        self.v_q = Track(2400.0).to(s("fix4") - 0.12, 2400.0, 0.0)
        self.v_q.to(T["cut4"] + 0.15, 0.0, min(1.8, max(0.8, T["shake4"] - T["cut4"] - 0.4)), e_out)
        self.d_q = Integral(lambda t: self.v_q.at(t), 0, dur)
        self.v_st = Track(0.0).to(T["go"], 2200.0, 2.0, e_in)
        self.d_st = Integral(lambda t: self.v_st.at(t), 0, dur)
        self.spans = [(T["slow"], T["pulls"] + 0.3), (T["derail"] + 0.2, T["nothing"] + 0.3),
                      (T["booms"], T["beak3"] + 0.3), (T["hit4"], T["shake4"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["slow"], 0.4, 6), (T["whole"], 0.4, 8), (T["derail"] + 0.25, 0.7, 14),
                       (T["booms"], 0.6, 16), (T["hit4"], 1.0, 22), (T["shake4"], 0.5, 6), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(28)
        self.houses = [(rng.uniform(0, 3000), rng.uniform(50, 120), rng.uniform(40, 90), rng.random()) for _ in range(30)]
        self.paddies = [(x, y, rng.choice(("#3F6B2E", "#4A7A33", "#365E28", "#55853A")))
                        for x in range(-1800, 1800, 260) for y in range(-2600, 2600, 220)]
        self.old_tr = Poly(old_track_pts())
        self.new_tr = Poly(new_track_pts())
        self.s_derail = self.old_tr.cum[79]                                  # the start of the tight bend

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ shared side-view pieces
    def far_layers(self, c, t, cx, cy, z, gy, d, fuji_k=1.0):
        v2.sky(c, W, H, 0.0, horizon_y=gy)
        v2.stars(c, W, H, t, 0.8, dx=-cx * 0.02)
        v2.moon(c, 200 - cx * 0.02, gy - 980, 60)
        if fuji_k > 0:
            fuji(c, 640 - cx * 0.03 - (d * 0.002) % 2400, gy - 30, 1500, 700, a=fuji_k)
        for i, (px, py, s_) in enumerate(((240, 760, 0.9), (860, 600, 0.7))):
            v2.cloud(c, (px - d * 0.01 - cx * 0.03) % (W + 700) - 250, gy - py, s_, a=0.75, seed=i)
        c.drawRect(R(0, gy, W, H - gy + 10), lin_paint(0, gy, 0, H, ["#241E45", "#120F26", "#07060F"]))
        c.save()
        c.translate(0, gy)
        for hx, hw, hh, r_ in self.houses:                                      # a far town, slowly sliding
            xx = (hx - d * 0.06 - cx * 0.1) % 3000 - 900
            c.drawRect(R(xx, -hh, hw, hh), P("#1A1840"))
            if r_ < 0.7:
                c.drawRect(R(xx + hw * 0.3, -hh * 0.6, 10, 10), P("#FDE68A", 0.7))
        c.restore()

    def viaduct(self, c, x0, x1, d, wire_on=1.0, poles=True):
        c.drawRect(R(x0, 8, x1 - x0, 56), lin_paint(0, 8, 0, 64, ["#A7B0BE", "#6B7484"]))
        c.drawRect(R(x0, 0, x1 - x0, 10), P("#4B5563"))
        c.drawLine(x0, 2, x1, 2, P("#D1D5DB", 1, stroke=4))
        off = d % 380
        xx = x0 - off - 380
        while xx < x1 + 380:
            c.drawRect(R(xx - 26, 64, 52, 1400), lin_paint(xx - 26, 0, xx + 26, 0, ["#3B4252", "#4B5263", "#2E3442"]))
            xx += 380
        if poles:
            off = d % 620
            xx = x0 - off - 620
            while xx < x1 + 620:
                c.drawRect(R(xx - 7, WIRE - 30, 14, 40 - WIRE), P("#6B7280"))
                c.drawLine(xx, WIRE - 22, xx + 70, WIRE - 22, P("#6B7280", 1, stroke=6))
                xx += 620
        c.drawLine(x0, WIRE, x1, WIRE, P("#94A3B8", 1, stroke=3))
        if wire_on > 0:
            c.drawLine(x0, WIRE, x1, WIRE, P("#FDE68A", 0.55 * wire_on, stroke=4, blur=4))

    # ------------------------------------------------------------------ set: the line in front of Fuji
    def draw_line(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["line"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        d = self.d_line.at(t)
        self.far_layers(c, t, cx, cy, z, gy + 90 * z, d)
        self.view(c, cam)
        x0, x1 = cx - 600 / z, cx + 600 / z
        self.viaduct(c, x0, x1, d)
        ang = d / 13.0
        train_side(c, TIP, n=7, k=1.0, ang=ang, lit=0.55, panto=1.0, t=t)
        c.restore()
        hstreaks(c, t, 0.6 if t < s("cta") or t >= s("stat") - 0.12 else 0.0, 300, 1250, n=20, seed=28)
        if t >= T["cong2"]:
            for k in range(4):
                v2.shock_ring(c, 200 + k * 230, 520 + (k % 2) * 90, t, T["cong2"] + 0.22 * k, 0.9, r1=170,
                              col=("#FDE68A", "#F472B6", "#7DD3FC", "#A7F3D0")[k], width=7, squash=1.0)
        self.ui["cam"] = cam

    def ui_line(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            x0, y0 = self.at(TIP - 110, -70)
            self.label(x0, y0, 640, 560, "beak", T["beak"] - 0.1, T["bullet"] - 0.4, HILITE, size=34)
            self.chip(540, 470, "train", T["bullet"] - 0.15, s("break1") + 0.2, accent=HILITE, size=38)

    # ------------------------------------------------------------------ set: power (break1, fix1)
    def draw_power(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["power"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        d = self.d_pow.at(t)
        self.far_layers(c, t, cx, cy, z, gy + 60 * z, d * 3, fuji_k=0.0)
        c.save()
        c.translate(W / 2 - cx * 0.08, gy + 30 * z)
        v2.ridge(c, -1500, 1500, 0, 230, "#2C2660", "#1A1636", seed=5, step=150, rough=0.5)
        c.restore()
        self.view(c, cam)
        x0, x1 = cx - 600 / z, cx + 600 / z
        self.viaduct(c, x0, x1, d)
        fixed = t >= s("fix1") - 0.12
        if not fixed:
            sp = prog(t, T["dragging"] - 0.3, T["dragging"]) * (1 - prog(t, s("fix1") - 0.5, s("fix1") - 0.12))
            old_train(c, 260, 6, self.a_pow.at(t), t, sparks=sp, heat=prog(t, T["slow"] - 0.3, T["slow"] + 0.4))
            if sp > 0:
                sparks_shower(c, 200, -6, t, T["dragging"] - 0.2, dur=1.2, n=16, speed=380, seed=41)
                sparks_shower(c, 40, -6, t, T["dragging"] + 0.4, dur=1.2, n=16, speed=380, seed=42)
        else:
            train_side(c, 300, n=6, k=1.0, ang=self.a_pow.at(t), lit=0.5, motors=self.motors.at(t), t=t)
        c.restore()
        if fixed and t > T["whole"]:
            hstreaks(c, t, 0.8 * prog(t, T["whole"], T["whole"] + 0.8), 300, 1250, n=26, seed=29)
        self.ui["cam"] = cam
        self.ui["fixed"] = fixed

    def ui_power(self, c, t, tw):
        T, s = self.T, self.tl.s
        gk = self.span(s("break1") + 0.1, s("break2") - 0.2)
        if not self.ui.get("fixed"):
            gauge(c, 330, 680, self.kmh_pow.at(tw), gk)
            x0, y0 = self.at(60, -176)
            self.label(x0, y0, 800, 640, "engine", T["engine"] - 0.1, T["sixteen"] - 0.1, "#FCA5A5", size=32)
            self.chip(330, 900, "heavy", T["sixteen"] - 0.1, s("fix1") - 0.15, accent="#D6A46C", size=34)
            self.chip(540, 470, "slow", T["slow"] - 0.1, s("fix1") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["slow"] + 0.2, s("fix1") - 0.2, x=880, y=330)
            self.red(T["slow"] + 0.2, 1.8)
            return
        gauge(c, 330, 680, self.kmh_pow.at(tw), gk)
        x0, y0 = self.at(300 - 400 - 0.62 * CL + 74, -40)
        self.label(x0, y0, 760, 880, "motors", T["motors"] + 0.2, T["whole"] - 0.1, HILITE, size=30)
        self.chip(540, 470, "pulls", T["whole"] - 0.1, s("break2") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["pulls"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the map from above (break2, fix2)
    def draw_map(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["map"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), P("#2C4A22"))
        self.view(c, cam)
        for x, y, col in self.paddies:                                                 # rice paddies
            c.drawRRect(rr(x + 8, y + 8, 244, 204, 10), P(col))
            c.drawRRect(rr(x + 8, y + 8, 244, 204, 10), P("#9CC8E8", 0.16))
        fixed = t >= s("fix2") - 0.12
        ry = 420.0
        c.drawRect(R(-2000, ry - 46, 4000, 92), P("#4B5563"))                        # the road
        for xx in range(-2000, 2000, 120):
            c.drawRect(R(xx, ry - 4, 60, 8), P("#F8FAFC", 0.7))
        cx_ = ((t * 260) % 2600) - 1300 if fixed else min(-330.0, -1300 + (t - s("break2")) * 900)
        for k, (ox, col) in enumerate(((0, "#EF4444"), (900, "#22D3EE"))):           # cars on the road
            xx = cx_ + ox if fixed else (cx_ if k == 0 else 600 - (t - s("break2")) * 200)
            c.drawRRect(rr(xx - 60, ry - (36 if k == 0 else -8), 120, 30, 10), P(col))
            c.drawRRect(rr(xx - 20, ry - (32 if k == 0 else -12), 40, 22, 6), P("#BFE6FF", 0.8))
        tr = self.new_tr if fixed else self.old_tr
        if fixed:
            c.drawRRect(rr(-380, ry - 150, 760, 300, 30), P("#000000", 0.35, blur=20))      # the bridge over the road
            c.drawRRect(rr(-360, ry - 130, 720, 260, 24), lin_paint(-360, 0, 360, 0, ["#7C8594", "#A3ABB8", "#7C8594"]))
            for side in (-1, 1):                                                        # fences
                p = skia.Path()
                p.moveTo(*tr.pts[0])
                for q in tr.pts[1:]:
                    p.lineTo(q[0] + side * 70, q[1])
                c.drawPath(p, dash_paint("#E5E7EB", 0.6, w=4, dash=14, gap=16))
        path = tr.path()
        c.drawPath(path, P("#6B5B4B", 1, stroke=96))                                   # ballast
        c.drawPath(path, P("#3F3A36", 1, stroke=70))
        c.drawPath(path, P("#C0C6D0", 1, stroke=46))
        c.drawPath(path, P("#3F3A36", 1, stroke=34))
        if not fixed:
            for side in (-1, 1):                                                        # crossing barriers
                bx = -150 + side * 110
                c.drawLine(bx, ry - side * 60, bx - side * 200, ry - side * 60, P("#FACC15", 1, stroke=14))
                c.drawLine(bx, ry - side * 60, bx - side * 200, ry - side * 60, dash_paint("#111827", 1, w=14, dash=20, gap=20))
            s0 = self.s_derail + (CL * 0.62 + 260) / 2 + self.s_map.at(t) - self.s_map.at(T["derail"])
            train_top(c, tr, s0, 7, t, derail=(self.s_derail, T["derail"]))
            if t > T["derail"] + 0.1:
                dx_, dy_, ang0 = tr.at(self.s_derail)
                v2.debris(c, dx_, dy_ - 300, t, T["derail"] + 0.15, dur=1.4, n=20, speed=520, seed=7, gravity=0,
                          cols=("#7A5A3A", "#A3B18A", "#3F6B2E"))
                v2.smoke(c, dx_, dy_ - 380, t, T["derail"] + 0.15, T["derail"] + 2.2, rate=16, life=1.4,
                         spread=(220, -40), rise=-40, size=(30, 110), col="#9CA3AF", lit=None, lit_until=0.0, seed=8, a=0.55)
        else:
            sh = self.s_map.at(t) - self.s_map.at(s("fix2") - 0.12)
            train_top(c, tr, 600 + sh, 7, t)
        c.restore()
        self.ui["cam"] = cam
        self.ui["fixed"] = fixed

    def ui_map(self, c, t, tw):
        T, s = self.T, self.tl.s
        if not self.ui.get("fixed"):
            x0, y0 = self.at(-150, 420)
            self.label(x0, y0, 300, 1050, "crossing", T["crossings"] - 0.1, s("fix2") - 0.15, HILITE, size=32)
            x1, y1 = self.at(-60, 0)
            self.label(x1, y1, 790, 640, "bends", T["bends"] - 0.1, s("fix2") - 0.15, "#FDBA74", size=32)
            self.chip(540, 470, "off", T["derail"] + 0.2, s("fix2") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["derail"] + 0.3, s("fix2") - 0.2, x=880, y=330)
            self.red(T["derail"] + 0.3, 1.8)
            return
        self.chip(540, 470, "own", T["own"] - 0.1, T["tilted"] - 0.15, accent=HILITE, size=40)
        self.chip(540, 470, "wide", T["wide"] - 0.05, T["tilted"] - 0.15, accent=HILITE, size=40)
        x0, y0 = self.at(0, 420)
        self.label(x0, y0, 280, 1080, "bridge", T["nocross"] - 0.1, s("break3") - 0.15, GOOD, size=32)
        k = self.span(T["tilted"] - 0.1, s("break3") - 0.15, 0.3, 0.2)            # the tilted cross-section
        if k > 0:
            c.save()
            c.translate(540, 640)
            sc = e_back(clamp(k * 1.2))
            c.scale(sc, sc)
            c.drawRRect(rr(-300, -170, 600, 340, 30), P("#000000", 0.4, blur=18))
            c.drawRRect(rr(-300, -170, 600, 340, 30), P("#0F172A", 0.92))
            c.drawRRect(rr(-300, -170, 600, 340, 30), P("#FFFFFF", 0.25, stroke=3))
            c.save()
            c.translate(0, 80)
            c.rotate(-8)
            bal = skia.Path()
            bal.moveTo(-230, 40)
            bal.lineTo(230, 40)
            bal.lineTo(180, 0)
            bal.lineTo(-180, 0)
            bal.close()
            c.drawPath(bal, P("#7C6A58"))
            for rx in (-70, 70):
                c.drawRect(R(rx - 10, -14, 20, 16), P("#CBD5E1"))
            c.drawRRect(rr(-110, -170, 220, 150, 40), lin_paint(0, -170, 0, -20, list(WHITE)))
            c.drawRect(R(-110, -76, 220, 12), P(BLUE))
            c.drawRRect(rr(-80, -150, 160, 40, 10), P("#1E293B"))
            c.restore()
            c.drawLine(190, -40, 120, 30, P(GOOD, 1, stroke=8))
            p = skia.Path()
            p.moveTo(105, 45)
            p.lineTo(150, 30)
            p.lineTo(118, 2)
            p.close()
            c.drawPath(p, P(GOOD))
            word(c, self.L["tilt"], 0, -118 + 0, 34, HILITE)
            c.restore()
        self.badge("check", T["nothing"] + 0.1, s("break3") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the tunnel (break3, fix3)
    def tip3(self, t):
        return -520 + (t - self.T["tunnel"]) * 330.0

    def wave3(self, t):
        """break3: the squeezed air runs from the nose (at "shoves") to the far portal (at "booms")."""
        T = self.T
        t0 = min(T["shoves"], T["booms"] - 0.5)
        if t < t0:
            return max(-520.0, self.tip3(t)) + 60 * prog(t, T["tunnel"], t0)
        return lerp(max(-520.0, self.tip3(t0)) + 60, 520.0, prog(t, t0, T["booms"]))

    def draw_tunnel(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["tunnel"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        self.far_layers(c, t, cx, cy, z, gy + 40 * z, 0.0, fuji_k=0.0)
        self.view(c, cam)
        x0, x1 = cx - 600 / z, cx + 600 / z
        fixed = t >= s("fix3") - 0.12
        c.drawRect(R(x0, 0, x1 - x0, 1600), lin_paint(0, 0, 0, 900, ["#3B2F2A", "#1C1512"]))
        c.drawRect(R(x0, 0, x1 - x0, 14), P("#4B5563"))
        mnt = skia.Path()                                                               # the mountain, cut open
        mnt.moveTo(-760, 0)
        mnt.cubicTo(-560, -320, -300, -820, -40, -860)
        mnt.cubicTo(220, -840, 520, -360, 760, 0)
        mnt.close()
        c.drawPath(mnt, lin_paint(0, -860, 0, 0, ["#2F6B45", "#1F4D33", "#163524"]))
        for k in range(6):
            tx_, ty_ = -420 + k * 170, -500 + abs(k - 2.5) * 110
            c.drawCircle(tx_, ty_ - 20, 34, P("#2E7D4F"))
        c.drawRect(R(-520, -200, 1040, 200), P("#07090E"))                              # the bore
        for k in range(8):
            add_glow(c, -460 + k * 130, -170, 26, "#FDE68A", 0.3)
        for px_ in (-520, 520):                                                          # portals
            c.drawRect(R(px_ - 26, -230, 52, 230), P("#94A3B8"))
        hx = 860                                                                         # a house by the exit
        jig = math.sin(t * 70) * 10 * clamp(1 - (t - T["booms"]) / 0.9) if (not fixed and t >= T["booms"]) else 0.0
        c.save()
        c.translate(jig, 0)
        box(c, hx - 80, -170, 160, 170, "#E9D5B5", r=6)
        roof = skia.Path()
        roof.moveTo(hx - 100, -166)
        roof.lineTo(hx, -250)
        roof.lineTo(hx + 100, -166)
        roof.close()
        c.drawPath(roof, P("#7F1D1D"))
        flash = clamp(1 - (t - T["booms"]) / 0.6) if (not fixed and t >= T["booms"]) else 0.0
        for k in range(2):
            c.drawRRect(rr(hx - 56 + k * 70, -130, 42, 44, 4), P(mix("#FDE68A", "#FFFFFF", flash)))
        c.restore()
        c.drawRect(R(x0, -12, x1 - x0, 12), P("#6B7280"))
        k = self.nose.at(t) if fixed else 0.0
        tip = self.tip3(t) if not fixed else -600 + self.d_tun.at(t)
        train_side(c, tip, n=6, k=k, ang=tip / 13.0, lit=0.5, panto=0.0, t=t)
        if tip > -520:                                                                   # the mountain front hides it
            c.save()
            c.clipRect(R(-520, -2000, 1040, 4000))
            c.drawRect(R(-520, -200, 1040, 200), P("#07090E", 0.82))
            for kk in range(8):
                add_glow(c, -460 + kk * 130, -170, 26, "#FDE68A", 0.3)
            c.restore()
        # the pressure wave
        if not fixed:
            if T["tunnel"] <= t < T["booms"]:
                xw = self.wave3(t)
                xn = max(-520.0, tip)
                c.drawRect(R(xn, -196, max(0.0, xw - xn), 192), lin_paint(xn, 0, xw, 0, [("#7DD3FC", 0.15), ("#7DD3FC", 0.75)]))
                c.drawLine(xw, -196, xw, -4, P("#FFFFFF", 0.9, stroke=6))
                for j in range(4):
                    yy = -170 + j * 44
                    c.drawLine(xw - 60, yy, xw - 10, yy, P("#E0F2FE", 0.7, stroke=4))
            if t >= T["booms"]:
                for kk in range(3):
                    v2.shock_ring(c, 560, -100, t, T["booms"] + kk * 0.12, 0.9, r1=520, col="#E0F2FE", width=18, squash=1.0)
                v2.smoke(c, 560, -100, t, T["booms"], T["booms"] + 1.2, rate=24, life=1.0, spread=(300, -40), rise=-30,
                         size=(30, 120), col="#CBD5E1", lit=None, lit_until=0.0, seed=12, a=0.6)
                for kk in range(5):                                                      # startled birds
                    u = prog(t, T["booms"] + kk * 0.05, T["booms"] + 1.6)
                    if 0 < u < 1:
                        bx, by = 700 + kk * 60 + u * 500, -320 - kk * 30 - u * 600
                        c.drawLine(bx - 16, by - 8, bx, by, P("#0B1020", 1, stroke=4))
                        c.drawLine(bx, by, bx + 16, by - 8, P("#0B1020", 1, stroke=4))
        else:
            t_in = T["in3b"]
            if t >= t_in:
                xw = -520 + (t - t_in) * 1900
                if xw < 520:
                    c.drawRect(R(xw - 50, -196, 50, 192), lin_paint(xw - 50, 0, xw, 0, [("#7DD3FC", 0.0), ("#7DD3FC", 0.25)]))
                else:
                    v2.smoke(c, 560, -100, t, t_in + 0.8, t_in + 1.6, rate=8, life=0.8, spread=(80, -20), rise=-20,
                             size=(14, 40), col="#E5E7EB", lit=None, lit_until=0.0, seed=13, a=0.35)
        c.restore()
        self.ui["cam"] = cam
        self.ui["fixed"] = fixed
        self.ui["tip"] = tip

    def ui_tunnel(self, c, t, tw):
        T, s = self.T, self.tl.s
        if not self.ui.get("fixed"):
            xw = self.wave3(clamp(tw, T["tunnel"], T["booms"]))
            x0, y0 = self.at(xw, -200)
            self.label(x0, y0, 560, 560, "push", T["shoves"], T["booms"] - 0.05, "#7DD3FC", size=32)
            self.chip(800, 1100, "boom", T["booms"], s("fix3") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["booms"] + 0.2, s("fix3") - 0.2, x=880, y=330)
            self.red(T["booms"] + 0.2, 1.8)
            return
        k = self.span(T["kingfisher"] - 0.3, T["beak3"] - 0.6, 0.3, 0.3)              # the kingfisher card
        if k > 0:
            c.save()
            c.translate(540, 560)
            sc = e_back(clamp(k * 1.2))
            c.scale(sc, sc)
            c.drawRRect(rr(-330, -200, 660, 400, 34), P("#000000", 0.4, blur=18))
            c.drawRRect(rr(-330, -200, 660, 400, 34), lin_paint(0, -200, 0, 200, ["#BFE3F5", "#7CC4E4"]))
            c.save()
            c.clipRect(R(-330, -200, 660, 400))
            c.drawRect(R(-330, 70, 660, 130), lin_paint(0, 70, 0, 200, ["#1E6FA8", "#0B3A63"]))
            u = prog(tw, T["dives"] - 0.3, T["dives"] + 0.6)
            bx, by = lerp(-150, 60, e_in(u)), lerp(-60, 190, e_in(u))
            kingfisher(c, bx, by, 1.5, lerp(12, 60, u), wing=1 - u)
            if u >= 0.55:
                rp = prog(tw, T["dives"] + 0.25, T["dives"] + 1.2)
                c.drawOval(R(-10 - 90 * rp, 62, 100 + 180 * rp, 18), P("#FFFFFF", 0.5 * (1 - rp), stroke=4))
            c.restore()
            c.drawRRect(rr(-330, -200, 660, 400, 34), P("#FFFFFF", 0.5, stroke=4))
            word(c, self.L["kingfisher"], 0, -140, 40, NAVY)
            c.restore()
        self.chip(540, 820, "nosplash", T["splash"] - 0.1, T["in3b"] + 0.2, accent=GOOD, size=36)
        tip = self.ui.get("tip", -600)
        if tw < T["in3b"]:
            x0, y0 = self.at(tip - 140, -60)
            self.label(x0, y0, 330, 900, "beaknose", T["kingfisher"] + 0.5, T["in3b"], HILITE, size=32)
        self.chip(800, 1090, "quiet", T["in3b"] + 0.5, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["beak3"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the quake (break4, fix4)
    EPI = (-700.0, 1100.0)

    def draw_quake(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["quake"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        d = self.d_q.at(t)
        self.far_layers(c, t, cx, cy, z, gy + 30 * z, d * 2, fuji_k=0.8)
        self.view(c, cam)
        x0, x1 = cx - 600 / z, cx + 600 / z
        fixed = t >= s("fix4") - 0.12
        vrect(c, x0, 0, x1 - x0, 2400, ["#4A3A2E", "#2E241D", "#1A1411", "#0B0807"], [0, 0.2, 0.55, 1])
        for k, yy in enumerate((260, 560, 900, 1300)):
            c.drawRect(R(x0, yy, x1 - x0, 30 + k * 6), P("#FFFFFF", 0.035))
        ex, ey = self.EPI
        t0 = s("break4") + 0.25 if not fixed else s("fix4") + 0.1
        dist_train = math.hypot(TIP - 300 - ex, 0 - ey)
        if not fixed:
            vs = dist_train / max(0.6, T["hit4"] - t0)
            vp = vs * 1.8
        else:
            vp = (ey + 0.0) / max(0.4, T["wave4"] - t0)
            vs = dist_train / max(0.6, T["shake4"] - t0)
        if t >= t0:
            add_glow(c, ex, ey, 160, WARN, 0.5 + 0.3 * math.sin(t * 20))
            c.drawCircle(ex, ey, 22, P("#FCA5A5"))
            rp, rs = (t - t0) * vp, (t - t0) * vs
            for j in range(3):                                                          # the first, small wave
                r_ = rp - j * 60
                if 0 < r_ < 3400:
                    c.drawCircle(ex, ey, r_, P("#67E8F9", 0.75 - j * 0.2, stroke=5))
            for j in range(3):                                                          # the big wave
                r_ = rs - j * 90
                if 0 < r_ < 3400:
                    c.drawCircle(ex, ey, r_, P(WARN, 0.85 - j * 0.25, stroke=22 - j * 6))
        self.ui["vp"], self.ui["t0"] = vp, t0
        c.drawRect(R(x0, -10, x1 - x0, 20), P("#57534E"))
        c.drawRect(R(x0, -8, x1 - x0, 6), P("#D1D5DB"))
        off = d % 160                                                                    # sleepers sliding past
        xx = x0 - off - 160
        while xx < x1 + 160:
            c.drawRect(R(xx, 2, 70, 10), P("#3F3A36"))
            xx += 160
        wire_on = 1.0
        if fixed and t >= T["cut4"]:
            wire_on = 1 - prog(t, T["cut4"], T["cut4"] + 0.25)
        off = d % 700                                                                    # poles and the wire
        xx = x0 - off - 700
        while xx < x1 + 700:
            c.drawRect(R(xx - 7, WIRE - 30, 14, 30 - WIRE), P("#6B7280"))
            c.drawLine(xx, WIRE - 22, xx + 70, WIRE - 22, P("#6B7280", 1, stroke=6))
            xx += 700
        c.drawLine(x0, WIRE, x1, WIRE, P("#94A3B8", 1, stroke=3))
        if wire_on > 0:
            c.drawLine(x0, WIRE, x1, WIRE, P("#FDE68A", 0.7 * wire_on, stroke=5, blur=4))
        sens = []
        if fixed:                                                                        # sensors along the line
            off = d % 900
            xx = x0 - off - 900
            while xx < x1 + 900:
                lit_ = (t >= t0) and (math.hypot(xx - ex, -ey) <= (t - t0) * vp)
                c.drawRRect(rr(xx - 26, -70, 52, 60, 8), P("#334155"))
                c.drawLine(xx, -70, xx, -120, P("#94A3B8", 1, stroke=4))
                col = "#67E8F9" if lit_ else "#475569"
                c.drawCircle(xx, -126, 10, P(col))
                if lit_:
                    add_glow(c, xx, -126, 50, "#67E8F9", 0.8)
                    if t < T["cut4"] + 0.4:
                        c.drawLine(xx, -136, xx + 40, WIRE + 10, dash_paint("#67E8F9", 0.9, w=4, t=t * 3, dash=12, gap=10))
                sens.append((xx, lit_))
                xx += 900
        self.ui["sens"] = sens
        hitk = 0.0
        if not fixed and t >= T["hit4"]:
            hitk = clamp(1 - (t - T["hit4"]) / 2.2)
        if fixed and t >= T["shake4"]:
            hitk = 0.25 * clamp(1 - (t - T["shake4"]) / 1.0)
        c.save()
        if hitk > 0:
            c.translate(math.sin(t * 60) * 26 * hitk, math.cos(t * 47) * 10 * hitk)
            c.rotate(math.sin(t * 31) * 3 * hitk)
        brake = 0.0
        if fixed and t >= T["cut4"]:
            brake = clamp(self.v_q.at(t) / 2400 * 2) * (1 if self.v_q.at(t) > 30 else 0)
        train_side(c, TIP, n=6, k=1.0, ang=d / 13.0, lit=0.5, panto=1.0, t=t, sparks=brake)
        c.restore()
        if not fixed and t >= T["hit4"]:
            sparks_shower(c, TIP - 120, -10, t, T["hit4"], dur=1.0, n=26, speed=600, seed=51)
            sparks_shower(c, TIP - 700, -10, t, T["hit4"] + 0.15, dur=1.0, n=26, speed=600, seed=52)
        c.restore()
        if self.v_q.at(t) > 400:
            hstreaks(c, t, 0.5 * clamp(self.v_q.at(t) / 2400), 250, 900, n=16, seed=31)
        self.ui["cam"] = cam
        self.ui["fixed"] = fixed

    def ui_quake(self, c, t, tw):
        T, s = self.T, self.tl.s
        if not self.ui.get("fixed"):
            self.chip(540, 470, "quake", T["quakes"] - 0.1, T["hit4"] - 0.1, accent="#FDBA74", size=42)
            self.chip(540, 470, "cantstop", T["hit4"] - 0.05, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["hit4"] + 0.2, s("fix4") - 0.2, x=880, y=330)
            self.red(T["hit4"] + 0.2, 1.8)
            return
        sens = [p for p in self.ui.get("sens", []) if -200 < self.at(p[0], 0)[0] < 1280]
        if sens:
            sx = min(sens, key=lambda p: abs(self.at(p[0], 0)[0] - 300))[0]
            x0, y0 = self.at(sx, -126)
            self.label(x0, y0, 300, 640, "sensors", T["sensors"] - 0.1, T["cut4"] - 0.1, "#67E8F9", size=32)
        self.chip(540, 470, "pwave", T["first"] - 0.1, T["cut4"] - 0.1, accent="#67E8F9", size=40)
        self.chip(540, 470, "cut", T["cut4"], T["shake4"] - 0.1, accent=HILITE, size=44)
        self.chip(540, 470, "stopped", T["shake4"], s("cta") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["shake4"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: the station (reveal, tag)
    def draw_station(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["station"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        tag = t >= s("tag") - 0.2
        self.far_layers(c, t, cx, cy, z, gy + 80 * z, 0.0, fuji_k=0.0)
        self.view(c, cam)
        x0, x1 = cx - 600 / z, cx + 600 / z
        c.drawRect(R(x0, -640, x1 - x0, 60), P("#334155"))                             # the canopy
        c.drawRect(R(x0, -584, x1 - x0, 10), P("#1E293B"))
        for k in range(int((x1 - x0) / 220) + 2):
            lx = x0 - (x0 % 220) + k * 220
            c.drawRect(R(lx - 40, -578, 80, 8), P("#FEF3C7"))
            add_glow(c, lx, -560, 90, "#FEF3C7", 0.25)
        tip = 900.0 + (self.d_st.at(t) if tag else 0.0)
        c.save()
        c.translate(0, 40)
        dk = prog(t, T["doors"] - 0.1, T["doors"] + 0.5) if not tag else 0.0
        train_side(c, tip, n=7, k=1.0, ang=tip / 13.0, lit=0.75, panto=0.0, t=t, doors=dk)
        c.restore()
        c.drawRect(R(x0, 0, x1 - x0, 90), lin_paint(0, 0, 0, 90, ["#9CA3AF", "#4B5563"]))   # the platform
        c.drawRect(R(x0, 0, x1 - x0, 14), P("#FACC15"))
        c.drawRect(R(x0, 90, x1 - x0, 1400), P("#1F2430"))
        for k in range(int((x1 - x0) / 520) + 2):                                       # pillars
            px_ = x0 - (x0 % 520) + k * 520 + 130
            c.drawRect(R(px_ - 18, -574, 36, 574), lin_paint(px_ - 18, 0, px_ + 18, 0, ["#475569", "#64748B", "#334155"]))
        if not tag:
            clock = "09:52:30"
        else:
            sec = int(clamp((t - (T["go"] - 3.0)) / 3.0) * 3)
            clock = "09:59:5" + str(7 + min(sec, 2)) if t < T["go"] else "10:00:00"
        board(c, -150, -420, clock, 1.0)
        if not tag:                                                                    # the cleaning crew
            xs = (-560, -380, -200, -20, 160)
            for i, hx in enumerate(xs):
                u = prog(t, T["crew"] - 0.4 + i * 0.08, T["crew"] + 0.5 + i * 0.08)
                xx = lerp(hx + 900, hx, e_out(u))
                busy = prog(t, T["clean"] - 0.1, T["clean"] + 0.2) * (1 - prog(t, T["bowt"] - 0.4, T["bowt"]))
                bw = prog(t, T["bowt"], T["bowt"] + 0.35) * (1 - prog(t, T["bowt"] + 1.0, T["bowt"] + 1.35))
                bower(c, xx, 0, 150, "#F43F5E", bw, t + i * 0.3, face=-1 if bw > 0 else 1, arm=busy)
            if T["clean"] <= t < T["bowt"]:                                             # sparkles on the windows
                for k in range(10):
                    ph = (t * 1.7 + k * 0.137) % 1.0
                    gx = -700 + ((k * 211) % 1500)
                    add_glow(c, gx, -60 + 40, 30 * math.sin(ph * math.pi), "#FFFFFF", 0.9 * math.sin(ph * math.pi))
        else:                                                                          # the tag: you run for it
            u = prog(t, T["after"] - 0.1, T["miss"] + 0.4)
            mx = lerp(-1000, -330, e_out(u))
            pose = "walk" if u < 1 else "shrug"
            bob = abs(math.sin(t * 14)) * 10 if u < 1 else 0.0
            person(c, mx, -bob, 140, "#2563EB", t * 2.2, pose=pose, face=1, hair="#1F1A17")
            briefcase(c, mx + 30, -40 - bob)
            if u >= 1:
                for k in range(3):
                    sw = prog(t, T["miss"] + 0.5 + k * 0.25, T["miss"] + 1.2 + k * 0.25)
                    if 0 < sw < 1:
                        c.drawCircle(mx + 26 + k * 8, -170 + sw * 60, 6, P("#7DD3FC", 1 - sw))
        c.restore()
        self.ui["cam"] = cam
        self.ui["tag"] = tag

    def ui_station(self, c, t, tw):
        T, s = self.T, self.tl.s
        if not self.ui.get("tag"):
            self.chip(540, 470, "crew", T["crew"] - 0.1, T["clean"] + 0.6, accent="#FB7185", size=40)
            k = self.span(T["clean"] - 0.1, T["doors"] + 0.2, 0.25, 0.2)
            if k > 0:
                rem = 420 * (1 - prog(tw, T["clean"], T["bowt"] - 0.1))
                v2.chip(c, 540, 600, f"{int(rem // 60)}:{int(rem % 60):02d}", k, accent=HILITE, size=64)
            self.chip(540, 1080, "doors", T["doors"] + 0.1, s("stat") - 0.15, accent=GOOD, size=38)
            return
        self.chip(540, 470, "ontime", T["left"] - 0.1, self.duration, accent=HILITE, size=40)
        x0, y0 = self.at(-330, -200)
        self.chip(max(250, x0), y0 - 40, "wait", T["after"] + 0.2, T["miss"] + 0.4, accent=WARN, size=36)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, rush(1.6, 60), -8), (0.1, sfx.whirr(2.0, 140.0, 220.0, 61), -14), (T["beak"], sfx.pop(62), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 63), -9), (T["bullet"], sfx.chime(), -9),
              (T["bullet"] + 0.2, horn(0.9), -12)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 64), -4), (T["engine"], sfx.hum(2.4, 70.0), -12),
               (T["dragging"] - 0.2, sfx.creak(1.0, 65), -8), (T["dragging"], sfx.sizzle(1.0, 66), -12),
               (T["slow"], sfx.power_down(0.8, 67), -8), (T["slow"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -5)]
        ev += [(T["motors"] - 0.1 + 0.12 * i, sfx.pop(69 + i), -13) for i in range(8)]
        ev += [(T["whole"] - 0.2, sfx.charge_up(1.0), -10), (T["whole"] + 0.2, rush(1.4, 77), -8),
               (T["pulls"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 78), -4), (s("break2"), rush(1.6, 79), -12),
               (T["crossings"], sfx.bell(1400.0, 0.3, 0.5), -16), (T["crossings"] + 0.35, sfx.bell(1400.0, 0.3, 0.5), -16),
               (T["derail"] - 0.1, screech(0.8, 80), -8),
               (T["derail"] + 0.25, boom(1.2, 81), -8), (T["derail"] + 0.5, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 82), -5), (s("fix2"), rush(2.0, 83), -12),
               (T["tilted"], sfx.pop(84), -8), (T["nothing"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 85), -4), (T["tunnel"] - 0.3, rush(1.2, 86), -10),
               (T["shoves"], sfx.whoosh(0.8, True, 87), -12), (T["booms"], boom(1.4, 88), -3),
               (T["booms"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 89), -5), (T["kingfisher"], sfx.pop(90), -9),
               (T["dives"] + 0.45, sfx.whoosh(0.5, False, 91), -18), (T["dives"] + 0.6, sfx.tap(92), -16),
               (T["beak3"] - 0.6, sfx.riser(0.8, 93), -14), (T["in3b"] - 0.1, rush(1.3, 94), -18),
               (T["beak3"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 95), -4), (s("break4"), rush(2.0, 96), -12),
               (T["quakes"], rumble(2.4, 97), -6), (T["hit4"], boom(1.4, 98), -6),
               (T["hit4"] + 0.1, sfx.creak(1.0, 99), -8), (T["hit4"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 100), -5), (s("fix4") + 0.1, rumble(1.6, 101), -14),
               (T["wave4"], sfx.beep(1500.0, 0.1), -12), (T["wave4"] + 0.15, sfx.beep(1500.0, 0.1), -12),
               (T["cut4"], sfx.power_down(1.0, 102), -6), (T["cut4"] + 0.2, sfx.hiss(1.2, 103), -10),
               (T["shake4"], rumble(1.4, 104), -10), (T["shake4"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(105), 0), (T["follow"] - 0.15, sfx.pop(106), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.4, True, 107), -6), (T["crew"], chime_jp(), -10),
               (T["clean"] + 0.2, sfx.sparkle(1.2, 12, 108), -10), (T["bowt"], sfx.pop(109), -10),
               (T["doors"], sfx.hiss(0.5, 110), -10), (T["doors"] + 0.1, sfx.ding(), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.4, False, 111), -6), (s("stat"), rush(1.8, 112), -14)]
        ev += [(T["s1"], sfx.pop(113), -3), (T["s2"], sfx.pop(114), -3), (T["s3"], sfx.pop(115), -3)]
        ev += [(T["cong2"], sfx.pop(116), -2), (T["cong2"], sfx.sparkle(1.0, 14, 117), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 118), -6), (T["go"] - 0.6, chime_jp(), -12),
               (T["go"], sfx.hiss(0.6, 119), -10), (T["go"] + 0.3, rush(2.0, 120), -10),
               (T["miss"] + 0.4, sfx.womp(), -8)]
        return ev


NAME = "bullettrain"
EPISODE = BulletTrain
