"""Episode 20 - A race car.  v2 look: one world and three boards.

track   a night race from the side: the asphalt is y = 0, the car stands at x = 0 with its nose to the right and the world
        scrolls past it (self.dist_at); the pit box, the wall and the podium (x = PODX) are in the same world
top     the first fast corner from straight above (the camera rides along with the car)
brake   one front wheel cut open: carbon disc, pads, air duct
wheel   the steering wheel, straight on
"""
from v2_base import *  # noqa: F401,F403

RX, FX, RW = -150, 172, 46                                               # rear axle, front axle, wheel radius
CARBON, PAINT, SUIT = "#B4BCCD", "#F97316", "#F8FAFC"
PODX = 900
STICKERS = (("num", 140, -46, 16), ("stripe", -128, -98, 72), ("star", -96, -46, 14), ("check", -237, -122, 22), ("bolt", -40, -46, 15),
            ("heart", 104, -60, 15), ("plus", -188, -44, 11), ("num", -84, -90, 13), ("smile", 56, -58, 10), ("band", 212, -40, 34),
            ("star", -38, -108, 9), ("dots", -80, -28, 5))
BTN_COLS = ("#EF4444", "#FBBF24", "#60A5FA", "#F472B6", "#A78BFA", "#F8FAFC", "#FB923C", "#2DD4BF")
BUTTONS = ([(240, -122, 30, "#34D399", "start")] +
           [(x, y, 22, BTN_COLS[i % 8], "b") for i, (x, y) in enumerate(((-240, -122), (-180, -122), (180, -122), (-240, -64), (-180, -64),
                                                                        (180, -64), (240, -64), (-180, -6), (180, -6), (240, -6)))] +
           [(-240, 40, 27, "#38BDF8", "drink")] +
           [(x, y, 20, BTN_COLS[(i + 3) % 8], "b") for i, (x, y) in enumerate(((-180, 50), (180, 50), (240, 50), (-60, 22), (60, 22), (-225, 108),
                                                                              (225, 108)))] +
           [(x, 92, 34, "#94A3B8", "dial") for x in (-96, 0, 96)])          # 22 in all


def arrow(c, x0, y0, x1, y1, col, w=10, a=1.0, head=22):
    if a <= 0:
        return
    c.drawLine(x0, y0, x1, y1, P(col, a, stroke=w))
    an = math.atan2(y1 - y0, x1 - x0)
    for da in (2.6, -2.6):
        c.drawLine(x1, y1, x1 + math.cos(an + da) * head, y1 + math.sin(an + da) * head, P(col, a, stroke=w))


def wheel(c, x, y, rot=0.0, wear=0.0, glow=0.0, a=1.0, r=RW):
    """A wheel from the side: soft tire (red stripe), rim, five spokes and its one nut. wear 0..1, glow 0..1 = a hot brake."""
    if a <= 0:
        return
    ro = r * (1 - 0.09 * wear)
    c.drawCircle(x, y, ro, P(mix("#0B0F1A", "#4A4F5E", wear * 0.7), a))
    if wear < 1:
        c.drawCircle(x, y, ro - 7, P("#EF4444", a * (1 - wear), stroke=4))
    if wear > 0.5:                                                           # the canvas shows through
        for i in range(6):
            an = math.radians(rot + i * 60)
            c.drawCircle(x + math.cos(an) * (ro - 7), y + math.sin(an) * (ro - 7), 4, P("#9CA3AF", a * (wear - 0.5) * 2))
    c.drawCircle(x, y, r * 0.60, P("#111827", a))
    if glow > 0:
        c.drawCircle(x, y, r * 0.5, P(mix("#7C2D12", "#FF8A3D", glow), a * glow))
        add_glow(c, x, y, r * 1.6, "#FF6A2B", 0.8 * glow * a)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    for i in range(5):
        c.save()
        c.rotate(i * 72)
        c.drawRRect(rr(4, -4, r * 0.52, 8, 3), P("#CBD5E1", a))
        c.restore()
    c.restore()
    c.drawCircle(x, y, r * 0.60, P("#E5E9F2", a, stroke=4))
    c.drawCircle(x, y, 9, P("#FBBF24", a))
    c.drawCircle(x, y, 4, P("#92400E", a))


def helmet(c, x, y, r=21, a=1.0):
    c.drawCircle(x, y, r, lin_paint(0, y - r, 0, y + r, [("#FDE68A", a), ("#FBBF24", a), ("#B45309", a)]))
    vis = skia.Path()
    vis.moveTo(x + r * 0.1, y - r * 0.38)
    vis.lineTo(x + r * 0.98, y - r * 0.2)
    vis.lineTo(x + r * 0.94, y + r * 0.28)
    vis.lineTo(x + r * 0.1, y + r * 0.2)
    vis.close()
    c.drawPath(vis, P("#0B1220", a))
    c.drawLine(x + r * 0.3, y - r * 0.2, x + r * 0.75, y - r * 0.1, P("#7DD3FC", 0.7 * a, stroke=3))
    c.drawRect(R(x - r * 0.9, y - r * 0.66, r * 1.5, 5), P("#FFFFFF", 0.85 * a))


def body_path():
    p = skia.Path()
    p.moveTo(-222, -17)
    p.lineTo(-222, -50)
    p.lineTo(-198, -68)
    p.cubicTo(-150, -84, -92, -128, -54, -131)
    p.lineTo(-24, -131)
    p.lineTo(-10, -86)
    p.lineTo(72, -86)
    p.cubicTo(110, -80, 150, -68, 186, -55)
    p.lineTo(186, -17)
    p.close()
    return p


def nose_path(k):
    """The nose from x = 186 forward; k 0..1 = how far it has folded up. Returns (path, x of the tip)."""
    ln = 74 * (1 - 0.78 * k)
    n = 6
    p = skia.Path()
    p.moveTo(185, -55)
    for i in range(1, n + 1):
        u = i / n
        p.lineTo(186 + ln * u, lerp(-55, -37, u) + (9 if i % 2 else -7) * k * (i < n))
    for i in range(n, -1, -1):
        u = i / n
        p.lineTo(186 + ln * u, lerp(-17, -23, u) + (-7 if i % 2 else 6) * k * (0 < i < n))
    p.lineTo(185, -17)
    p.close()
    return p, 186 + ln


def sticker(c, kind, x, y, s, k):
    if k <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    if kind == "num":
        c.drawCircle(0, 0, s, P("#F8FAFC"))
        text(c, "20", 0, s * 0.40, s * 1.1, "#0B1024", "Poppins-Black")
    elif kind == "star":
        p = skia.Path()
        for i in range(10):
            r_ = s if i % 2 == 0 else s * 0.45
            an = -math.pi / 2 + i * math.pi / 5
            if i == 0:
                p.moveTo(math.cos(an) * r_, math.sin(an) * r_)
            else:
                p.lineTo(math.cos(an) * r_, math.sin(an) * r_)
        p.close()
        c.drawPath(p, P("#FDE047"))
    elif kind == "bolt":
        p = skia.Path()
        p.moveTo(4, -s)
        p.lineTo(-s * 0.6, 2)
        p.lineTo(-1, 2)
        p.lineTo(-5, s)
        p.lineTo(s * 0.6, -3)
        p.lineTo(1, -3)
        p.close()
        c.drawPath(p, P("#F8FAFC"))
    elif kind == "plus":
        c.drawCircle(0, 0, s, P("#F8FAFC"))
        c.drawRRect(rr(-s * 0.55, -s * 0.16, s * 1.1, s * 0.32, 2), P("#FF4D4F"))
        c.drawRRect(rr(-s * 0.16, -s * 0.55, s * 0.32, s * 1.1, 2), P("#FF4D4F"))
    elif kind == "smile":
        c.drawCircle(0, 0, s, P("#FDE047"))
        c.drawCircle(-s * 0.35, -s * 0.2, s * 0.15, P("#0B1024"))
        c.drawCircle(s * 0.35, -s * 0.2, s * 0.15, P("#0B1024"))
        c.drawArc(R(-s * 0.5, -s * 0.45, s, s * 0.95), 20, 140, False, P("#0B1024", 1, stroke=max(1.5, s * 0.16)))
    elif kind == "heart":
        hp = skia.Path()
        hp.moveTo(0, 30)
        hp.cubicTo(-70, -20, -30, -70, 0, -32)
        hp.cubicTo(30, -70, 70, -20, 0, 30)
        hp.close()
        c.scale(s / 60.0, s / 60.0)
        c.drawPath(hp, P("#FB7185"))
    elif kind == "check":
        q = s * 2 / 3
        for i in range(3):
            for j in range(3):
                c.drawRect(R(-s + i * q, -s + j * q, q, q), P("#F8FAFC" if (i + j) % 2 == 0 else "#0B1024"))
    elif kind == "stripe":
        c.drawLine(-s, s * 0.38, s, -s * 0.38, P("#F8FAFC", 1, stroke=7))
    elif kind == "band":
        c.drawLine(-s, -s * 0.24, s, s * 0.24, P("#2DD4BF", 1, stroke=6))
    elif kind == "dots":
        for i in range(3):
            c.drawCircle(i * s * 3.2, 0, s, P(("#F8FAFC", "#2DD4BF", "#FDE047")[i]))
    c.restore()


def car(c, t, rot=0.0, squat=0.0, pitch=0.0, fw=1.0, rw=1.0, halo=0.0, nose=0.0, paint=0.0, stickers=0.0, xray=0.0, cell=0.0,
        glow=(0.0, 0.0), wear=(0.0, 0.0), wheels=True, flame=0.0, thumb=0.0, dizzy=0.0):
    """The race car, nose to the right, wheels on y = 0.  fw / rw / halo 0..1: the parts that are added on the way."""
    c.save()
    c.translate(0, squat)
    if pitch:
        c.rotate(pitch, RX, -RW)
    ba = 1 - 0.66 * xray
    plate = mix("#252B40", PAINT, paint)
    if flame > 0:
        v2.flame(c, -222, -58, 20, 130, t, flame, seed=3, ang=180)
    if rw > 0:                                                               # the rear wing
        c.save()
        c.translate(-226, -70)
        c.scale(rw, rw)
        c.translate(226, 70)
        c.drawLine(-208, -66, -230, -122, P("#1F2937", 1, stroke=9))
        box(c, -268, -154, 62, 64, plate, r=6)
        c.drawLine(-260, -142, -216, -130, P("#CBD5E1", 1, stroke=8))
        c.drawLine(-260, -121, -218, -111, P("#94A3B8", 1, stroke=6))
        c.restore()
    bp = body_path()
    npth, tip = nose_path(nose)
    c.drawRect(R(-222, -21, 410, 6), P("#0B0F1A", ba))
    for pth in (bp, npth):
        c.drawPath(pth, lin_paint(0, -131, 0, -17, [(shade(CARBON, 0.22), ba), (CARBON, ba), (shade(CARBON, -0.35), ba)]))
    if paint > 0:                                                            # the paint goes on from the nose back
        c.save()
        c.clipRect(R(264 - 520 * paint, -220, 540, 240))
        for pth in (bp, npth):
            c.drawPath(pth, lin_paint(0, -131, 0, -17, [(shade(PAINT, 0.25), ba), (PAINT, ba), (shade(PAINT, -0.3), ba)]))
        c.restore()
    pod = mix(shade(CARBON, -0.28), shade(PAINT, -0.22), clamp(paint * 2.2 - 0.9))
    c.drawRRect(rr(-128, -70, 172, 50, 20), P(pod, ba))
    c.drawOval(R(26, -64, 16, 38), P("#0B0F1A", ba))
    c.drawRRect(rr(-4, -93, 72, 14, 6), P("#0B0F1A", ba))                      # the cockpit
    if xray > 0:
        tub = skia.Path()
        tub.moveTo(-28, -22)
        tub.lineTo(-32, -92)
        tub.lineTo(72, -88)
        tub.lineTo(150, -66)
        tub.lineTo(150, -22)
        tub.close()
        if cell > 0:
            c.drawPath(tub, P(HILITE, 0.22 * cell))
            c.drawPath(tub, P(HILITE, cell, stroke=5))
        c.drawLine(30, -78, 4, -42, P(PAINT, xray, stroke=16))               # the driver, lying back
        c.drawLine(4, -42, 72, -54, P(PAINT, xray, stroke=15))
        c.drawLine(72, -54, 132, -40, P(PAINT, xray, stroke=13))
        c.drawLine(30, -74, 72, -72, P("#CBD5E1", xray, stroke=9))
        c.drawCircle(80, -72, 12, P("#111827", xray, stroke=5))
    if thumb > 0:
        c.drawLine(42, -92, 64, -130, P(PAINT, thumb, stroke=10))
        c.drawCircle(66, -136, 9, P("#F8FAFC", thumb))
        c.drawLine(66, -138, 66, -154, P("#F8FAFC", thumb, stroke=7))
    helmet(c, 34, -101, 21)
    if dizzy > 0:
        for j in range(4):
            an = t * 7 + j * 1.57
            c.drawCircle(34 + math.cos(an) * 28, -136 + math.sin(an) * 8, 4.5, P(HILITE, dizzy))
    if halo > 0:
        hp = skia.Path()
        hp.moveTo(-12, -100)
        hp.quadTo(30, -136, 70, -117)
        hp.lineTo(88, -85)
        c.save()
        c.translate(38, -86)
        c.scale(1, halo)
        c.translate(-38, 86)
        c.drawPath(hp, P("#0B0F1A", 1, stroke=13))
        c.drawPath(hp, P("#D5DAE6", 1, stroke=8))
        c.restore()
    if fw > 0:                                                               # the front wing rides on the nose tip
        c.save()
        c.translate(tip - 12, -22)
        c.scale(fw, fw)
        c.rotate(-28 * nose)
        c.drawLine(-4, -4, 10, 6, P("#1F2937", 1, stroke=7))
        c.drawLine(-22, 8, 46, 12, P("#CBD5E1", 1, stroke=8))
        c.drawLine(-8, -2, 42, 4, P("#94A3B8", 1, stroke=6))
        box(c, 36, -14, 11, 30, plate, r=3)
        c.restore()
    for i, (kind, sx, sy, ss) in enumerate(STICKERS):
        sticker(c, kind, sx, sy, ss, e_back(clamp(stickers - i)))
    if wheels:
        wheel(c, RX, -RW, rot, wear[1], glow[1])
        wheel(c, FX, -RW, rot, wear[0], glow[0])
    c.restore()


def big_engine(c, x, y, t, run=0.0):
    """A V8 far too big for the job; (x, y) = the middle of its underside."""
    c.save()
    c.translate(x + math.sin(t * 70) * 2.2 * run, y)
    for i in range(4):                                                       # exhaust pipes, swept back
        p = skia.Path()
        p.moveTo(-50 + i * 30, -56)
        p.cubicTo(-50 + i * 30, -20, -96, -34 + i * 4, -112 - i * 7, -46 + i * 7)
        c.drawPath(p, P("#B45309", 1, stroke=8))
    box(c, -70, -80, 140, 80, "#55607F", r=10)
    for i in range(4):
        box(c, -64 + i * 33, -106, 27, 30, "#7C879F", r=5)
        c.drawRRect(rr(-60 + i * 33, -126, 19, 22, 5), P("#CBD5E1"))
        c.drawOval(R(-63 + i * 33, -132, 25, 10), P("#E5E9F2"))
    c.drawLine(52, -30, 42, -62, P("#0B0F1A", 1, stroke=5))
    c.drawCircle(52, -30, 17, P("#1F2937"))
    c.drawCircle(52, -30, 7, P("#CBD5E1"))
    c.drawCircle(42, -62, 10, P("#1F2937"))
    for bx in (-58, 58):
        c.drawCircle(bx, -9, 6, P("#FBBF24"))
    c.restore()


def kart(c, t, tilt=0.0, sq=0.0, engine_y=None, run=0.0):
    """A go-kart, nose to the right. engine_y: where the underside of the big engine is (None = no engine yet)."""
    c.save()
    c.rotate(tilt, -78, -24)
    c.drawRRect(rr(-106, -32 + 3 * sq, 216, 12, 6), P("#94A3B8"))
    c.drawRRect(rr(98, -46, 14, 28, 5), P("#EF4444"))
    c.drawRRect(rr(-116, -44, 12, 24, 5), P("#EF4444"))
    seat = skia.Path()
    seat.moveTo(-44, -32)
    seat.lineTo(-56, -84)
    seat.lineTo(-44, -86)
    seat.lineTo(-28, -42)
    seat.lineTo(4, -42)
    seat.lineTo(4, -32)
    seat.close()
    c.drawPath(seat, P("#1F2937"))
    c.drawLine(58, -32, 40, -74, P("#CBD5E1", 1, stroke=5))
    engineer(c, -14, -36, 92, SHIRTS[0], t, "sit", face=1)
    c.drawCircle(38, -78, 12, P("#111827", 1, stroke=6))
    if engine_y is not None:
        big_engine(c, -100, engine_y, t, run)
    for wx in (-78, 80):
        c.drawCircle(wx, -24, 24, P("#0B0F1A"))
        c.drawCircle(wx, -24, 11, P("#CBD5E1"))
        c.drawCircle(wx, -24, 4, P("#475569"))
    c.restore()


def bus(c, x, y):
    """A double-decker; (x, y) = under its wheels, in the middle."""
    c.save()
    c.translate(x, y)
    for wx in (-130, 124):
        c.drawCircle(wx, -26, 28, P("#0B0F1A"))
        c.drawCircle(wx, -26, 12, P("#CBD5E1"))
    box(c, -210, -276, 420, 246, "#DC2626", r=22)
    c.drawRect(R(-210, -160, 420, 8), P("#FDE68A"))
    rng = random.Random(4)
    for row, (yy, hh, n) in enumerate(((-252, 70, 6), (-136, 62, 5))):
        for i in range(n):
            c.drawRRect(rr(-196 + i * 66, yy, 54, hh, 8), P("#BFE3FF", 0.92))
            if rng.random() < 0.7:                                           # somebody at the window
                hx = -196 + i * 66 + 27
                c.drawCircle(hx, yy + hh - 26, 11, P("#E8B48A"))
                c.drawRRect(rr(hx - 14, yy + hh - 16, 28, 16, 6), P(rng.choice(("#1D4ED8", "#047857", "#7C3AED", "#B45309"))))
    c.drawRRect(rr(140, -136, 54, 106, 8), P("#7F1D1D"))
    c.drawRRect(rr(-210, -34, 420, 8, 4), P("#7F1D1D"))
    c.restore()


def wall(c, x, cracked=0.0):
    """A concrete wall; x = its face (the left side)."""
    box(c, x, -236, 160, 236, "#9CA3AF", r=4)
    for i in range(1, 4):
        c.drawRect(R(x, -236 + i * 59, 160, 3), P("#000000", 0.14))
    for i in range(8):
        c.drawRect(R(x + i * 20, -236, 20, 20), P("#EF4444" if i % 2 == 0 else "#F8FAFC"))
    if cracked > 0:
        for dy_, ln, an in ((-36, 70, -0.5), (-36, 56, 0.5), (-44, 84, -1.2), (-30, 44, 1.1)):
            p = skia.Path()
            p.moveTo(x + 2, dy_)
            p.lineTo(x + 2 + math.cos(an) * ln * 0.5, dy_ + math.sin(an) * ln * 0.5 + 8)
            p.lineTo(x + 2 + math.cos(an) * ln, dy_ + math.sin(an) * ln)
            c.drawPath(p, P("#1F2937", cracked, stroke=4))


def stand(c, t, seed=1):
    """A grandstand 900 wide standing on y = 0, from x = 0."""
    box(c, 0, -250, 900, 250, "#141A3A", r=4)
    rng = random.Random(seed)
    for row in range(6):
        yy = -62 - row * 30
        c.drawRect(R(8, yy, 884, 4), P("#2A3266"))
        for i in range(44):
            if rng.random() < 0.85:
                c.drawCircle(20 + i * 20 + rng.uniform(-3, 3), yy - 8, 6.5,
                             P(rng.choice(("#F87171", "#FBBF24", "#60A5FA", "#F8FAFC", "#34D399", "#F472B6")), 0.38))
    for _ in range(7):                                                       # cameras in the crowd
        fx_, fy_, ph_ = rng.uniform(20, 880), -70 - rng.randint(0, 5) * 30, rng.random()
        if (t * 0.9 + ph_) % 1.0 < 0.07:
            add_glow(c, fx_, fy_, 34, "#FFFFFF", 0.9)
    c.drawRect(R(-16, -292, 932, 14), P("#39437A"))
    for px in (0, 300, 600, 900):
        c.drawRect(R(px - 4, -292, 8, 292), P("#2A3266"))


def car_top(c, x, y, ang, steer=0.0):
    """The bare car from above; ang = 0 points up the screen."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRect(R(-40, -56, 80, 6), P("#1F2937"))
    c.drawRect(R(-42, 50, 84, 6), P("#1F2937"))
    for wx, wy, st in ((-44, -53, steer), (44, -53, steer), (-47, 53, 0.0), (47, 53, 0.0)):
        c.save()
        c.translate(wx, wy)
        c.rotate(st)
        c.drawRRect(rr(-11, -21, 22, 42, 6), P("#0B0F1A"))
        c.drawRRect(rr(-11, -21, 22, 42, 6), P("#EF4444", 0.8, stroke=2))
        c.restore()
    body = skia.Path()
    for i, (bx, by) in enumerate(((0, -94), (13, -60), (18, -10), (30, 10), (30, 62), (16, 80), (-16, 80), (-30, 62), (-30, 10), (-18, -10),
                                  (-13, -60))):
        if i == 0:
            body.moveTo(bx, by)
        else:
            body.lineTo(bx, by)
    body.close()
    c.drawPath(body, lin_paint(-30, 0, 30, 0, [shade(CARBON, 0.3), CARBON, shade(CARBON, -0.2)]))
    c.drawRRect(rr(-15, 30, 30, 42, 6), P("#7C879F"))
    for i in range(4):
        c.drawRect(R(-11, 35 + i * 9, 22, 4), P("#CBD5E1"))
    c.drawCircle(0, 2, 13, P("#FBBF24"))
    c.drawRect(R(-10, -5, 20, 4), P("#FFFFFF", 0.85))
    c.restore()


def hstreaks(c, t, a, y0, y1, n=22, seed=3):
    """Screen-space streaks rushing to the left: the car is going fast to the right."""
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


# ------------------------------------------------------------------------------------------ sounds
def rev(d=1.0, f0=90.0, f1=260.0, seed=1, power=0.7):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = f0 + (f1 - f0) * (tt / d) ** power
    ph = 2 * np.pi * np.cumsum(f) / sfx.SR
    x = sum(np.sin(ph * k) / k for k in (1, 2, 3, 4, 5, 6))
    x = np.tanh(x * 1.6) + 0.2 * sfx._bp(sfx._rng(seed).standard_normal(n), 300, 3000)
    return sfx._norm(sfx._lp(x, 2600) * sfx._ar(n, 0.04, d * 0.3), 0.6)


def screech(d=0.6, seed=2):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    f = 2300 - 500 * tt / d
    x = np.sin(2 * np.pi * np.cumsum(f) / sfx.SR) * 0.5 + sfx._bp(sfx._rng(seed).standard_normal(n), 1800, 3400)
    return sfx._norm(x * sfx._ar(n, 0.03, d * 0.4), 0.5)


def gun_snd(d=0.24, seed=3):
    n = int(d * sfx.SR)
    tt = np.arange(n) / sfx.SR
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 700, 2600) * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 46 * tt)))
    return sfx._norm(x * sfx._ar(n, 0.01, 0.05), 0.6)


def crunch(d=0.45, seed=5):
    n = int(d * sfx.SR)
    rng = sfx._rng(seed)
    x = np.zeros(n)
    for _ in range(26):
        i0 = int(rng.uniform(0, 0.7) * n)
        m = int(rng.uniform(0.01, 0.04) * sfx.SR)
        x[i0:i0 + m] += rng.standard_normal(min(m, n - i0)) * rng.uniform(0.3, 1.0) * np.linspace(1, 0, min(m, n - i0))
    return sfx._norm(sfx._bp(x, 250, 4200) * sfx._ar(n, 0.005, d * 0.5), 0.8)


# ====================================================================================== the episode
class RaceCar(EpisodeV2):
    BUILD_NO = 20
    FIRST_SET = "track"
    CLEAR = "#0B1024"
    TITLE = {"en": "RACE CAR", "ar_sa": "سيارة سباق"}
    EMPH = {"en": ["CONGRATS", "ENGINE", "GO-KART", "RACE", "CAR", "CORNER", "SLIDES", "OFF", "WINGS", "UPSIDE", "DOWN", "SQUASHES", "CEILING",
                   "THEORY", "HUNDRED", "FIRE", "CARBON", "GLOWING", "RED", "THOUSAND", "DUCTS", "SOFT", "STICKY", "WEAR", "NUT", "TWENTY",
                   "SECONDS", "FAST", "WALL", "SURVIVAL", "CELL", "HALO", "BUS", "CRUMPLES", "FOLLOW", "CRUISE", "SHIP", "STICKERS", "BUTTONS",
                   "DRINK", "DRIVER", "HORSEPOWER", "ZERO", "YOURSELF", "SPRAY", "PURPOSE"],
            "ar_sa": ["مبروك", "مكينة", "كارتينج", "سباق", "منعطف", "تزحلق", "أجنحة", "مقلوبة", "يضغطها", "السقف", "نظرياً", "ثلاثمية", "نار",
                      "الكربون", "مولّعة", "ألف", "وفتحات", "الطرية", "تخلص", "صامولة", "عشرين", "ثانيتين", "سريعة", "جدار", "كبسولة", "طوق",
                      "باص", "خشم", "تابعني", "سفينة", "ملصقات", "دركسون", "زر", "لمشروبك", "سوّاق", "حصان", "وصفر", "بيدك", "يرشّه", "متعمّد"]}
    KEYS = {"ar_sa": {
        ("hook", "BOLT"): "ركّبت", ("hook", "ENGINE"): "مكينة", ("hook", "GO-KART"): "كارتينج", ("hook", "CONGRATS"): "مبروك", ("hook", "RACE"): "سباق",
        ("break1", "FIRST"): "أول", ("break1", "CORNER"): "منعطف", ("break1", "SLIDES"): "تزحلق", ("break1", "OFF"): "برّا", ("break1", "TRACK"): "الحلبة",
        ("fix1", "WINGS"): "أجنحة", ("fix1", "UPSIDE"): "مقلوبة", ("fix1", "FRONT"): "قدّام", ("fix1", "REAR"): "وورا", ("fix1", "LIFTING"): "يرفعها",
        ("fix1", "AIR"): "الهوا", ("fix1", "SQUASHES"): "يضغطها", ("fix1", "ROAD"): "الأرض",
        ("break2", "CEILING"): "السقف", ("break2", "THEORY"): "نظرياً", ("break2", "UNTIL"): "لين", ("break2", "BRAKE"): "تدعس", ("break2", "TWO"): "ثلاثمية",
        ("break2", "CATCH"): "وتولّع", ("break2", "BRAKES"): "الفرامل", ("break2", "FIRE"): "نار",
        ("fix2", "DISCS"): "أقراص", ("fix2", "PADS"): "وفحمات", ("fix2", "GLOWING"): "مولّعة", ("fix2", "THOUSAND"): "ألف", ("fix2", "DUCTS"): "وفتحات",
        ("fix2", "COOL"): "تبرّدها",
        ("break3", "SOFT"): "الطرية", ("break3", "STICKY"): "تلصق", ("break3", "TIRES"): "الكفرات", ("break3", "WEAR"): "تخلص", ("break3", "FINISH"): "النهاية",
        ("fix3", "NUT"): "صامولة", ("fix3", "TRAIN"): "وتدرّب", ("fix3", "TWENTY"): "عشرين", ("fix3", "GUNS"): "بمسدسات", ("fix3", "JACKS"): "ورافعات",
        ("fix3", "CHANGE"): "يغيّرون", ("fix3", "SECONDS"): "ثانيتين",
        ("break4", "FAST"): "سريعة", ("break4", "MEETS"): "تسلّم", ("break4", "WALL"): "جدار",
        ("fix4", "SURVIVAL"): "كبسولة", ("fix4", "HALO"): "طوق", ("fix4", "HOLD"): "يشيل", ("fix4", "BUS"): "باص", ("fix4", "NOSE"): "خشم",
        ("fix4", "CRUMPLES"): "يتكسّر", ("fix4", "DON'T"): "تتكسّر",
        ("cta", "START"): "تشغّل", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "COVER"): "غطّها", ("reveal", "STICKERS"): "ملصقات", ("reveal", "STEERING"): "دركسون", ("reveal", "TWENTY"): "عشرين",
        ("reveal", "BUTTONS"): "زر", ("reveal", "ONE"): "واحد", ("reveal", "DRINK"): "لمشروبك",
        ("stat", "ONE"): "سوّاق", ("stat", "THOUSAND"): "ألف", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "WINNER"): "الفايز", ("tag", "DON'T"): "يشربه", ("tag", "SPRAY"): "يرشّه", ("tag", "PURPOSE"): "متعمّد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a cruise ship"),
                   "stat": [("1", "DRIVER"), ("1,000", "HORSEPOWER"), ("0", "CUP HOLDERS")],
                   "L": {"engine": "HUGE ENGINE", "car": "YOUR RACE CAR", "grip": "NO GRIP", "fwing": "FRONT WING", "rwing": "REAR WING", "lift": "LIFT",
                         "down": "DOWNFORCE", "theory": "IN THEORY", "unit": "MPH", "disc": "CARBON DISC", "pads": "PADS", "duct": "AIR DUCT",
                         "soft": "SOFT TIRES", "gf": "FRONT TIRES", "gr": "REAR TIRES", "nut": "ONE NUT", "crew": "20 PEOPLE", "gun": "WHEEL GUN",
                         "jack": "JACK", "cell": "SURVIVAL CELL", "halo": "TITANIUM HALO", "bus": "12 TONS", "nose": "CRUMPLE NOSE", "start": "START",
                         "btn": "BUTTONS", "drink": "DRINK"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: سفينة سياحية"),
                      "stat": [("1", "سوّاق"), ("1,000", "حصان"), ("0", "حامل أكواب")],
                      "L": {"engine": "مكينة ضخمة", "car": "سيارة السباق حقتك", "grip": "ما فيه ثبات", "fwing": "جناح قدّام", "rwing": "جناح ورا", "lift": "رفع",
                            "down": "ضغط لتحت", "theory": "نظرياً", "unit": "كم/س", "disc": "قرص كربون", "pads": "فحمات", "duct": "فتحة هوا",
                            "soft": "كفرات طرية", "gf": "كفرات قدّام", "gr": "كفرات ورا", "nut": "صامولة وحدة", "crew": "20 شخص", "gun": "مسدس هوا",
                            "jack": "رافعة", "cell": "كبسولة النجاة", "halo": "طوق تيتانيوم", "bus": "12 طن", "nose": "خشم يتكسّر", "start": "تشغيل",
                            "btn": "زر", "drink": "مشروب"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "bolt": ("hook", "BOLT", 0.12), "engine": ("hook", "ENGINE", 0.26), "gokart": ("hook", "GO-KART", 0.46), "congrats": ("hook", "CONGRATS", 0.58),
            "race": ("hook", "RACE", 0.88),
            "first": ("break1", "FIRST", 0.22), "corner": ("break1", "CORNER", 0.36), "slides": ("break1", "SLIDES", 0.6), "off": ("break1", "OFF", 0.78),
            "track": ("break1", "TRACK", 0.9),
            "wings": ("fix1", "WINGS", 0.14), "upside": ("fix1", "UPSIDE", 0.2), "front": ("fix1", "FRONT", 0.38), "rear": ("fix1", "REAR", 0.45),
            "lifting": ("fix1", "LIFTING", 0.6), "air": ("fix1", "AIR", 0.76), "squashes": ("fix1", "SQUASHES", 0.8), "road": ("fix1", "ROAD", 0.96),
            "ceiling": ("break2", "CEILING", 0.2), "theory": ("break2", "THEORY", 0.3), "until": ("break2", "UNTIL", 0.4), "brake": ("break2", "BRAKE", 0.5),
            "two": ("break2", "TWO", 0.56), "catch": ("break2", "CATCH", 0.9), "brakes": ("break2", "BRAKES", 0.86), "fire": ("break2", "FIRE", 0.96),
            "discs": ("fix2", "DISCS", 0.2), "pads": ("fix2", "PADS", 0.28), "glowing": ("fix2", "GLOWING", 0.44), "thousand": ("fix2", "THOUSAND", 0.64),
            "ducts": ("fix2", "DUCTS", 0.86), "cool": ("fix2", "COOL", 0.92),
            "soft": ("break3", "SOFT", 0.18), "sticky": ("break3", "STICKY", 0.32), "tires": ("break3", "TIRES", 0.42), "wear": ("break3", "WEAR", 0.52),
            "finish": ("break3", "FINISH", 0.88),
            "nut": ("fix3", "NUT", 0.16), "train": ("fix3", "TRAIN", 0.32), "twenty": ("fix3", "TWENTY", 0.36), "guns": ("fix3", "GUNS", 0.54),
            "jacks": ("fix3", "JACKS", 0.6), "change": ("fix3", "CHANGE", 0.68), "seconds": ("fix3", "SECONDS", 0.92),
            "fast": ("break4", "FAST", 0.2), "meets": ("break4", "MEETS", 0.78), "wall": ("break4", "WALL", 0.9),
            "survival": ("fix4", "SURVIVAL", 0.22), "halo": ("fix4", "HALO", 0.46), "hold": ("fix4", "HOLD", 0.56), "bus": ("fix4", "BUS", 0.7),
            "nose": ("fix4", "NOSE", 0.82), "crumples": ("fix4", "CRUMPLES", 0.87), "dont": ("fix4", "DON'T", 0.96),
            "start": ("cta", "START", 0.2), "follow": ("cta", "FOLLOW", 0.42),
            "cover": ("reveal", "COVER", 0.1), "stickers": ("reveal", "STICKERS", 0.25), "steering": ("reveal", "STEERING", 0.45),
            "twenty2": ("reveal", "TWENTY", 0.65), "buttons": ("reveal", "BUTTONS", 0.72), "one": ("reveal", "ONE", 0.82), "drink": ("reveal", "DRINK", 0.95),
            "s1": ("stat", "ONE", 0.03), "s2": ("stat", "THOUSAND", 0.3), "s3": ("stat", "ZERO", 0.66),
            "cong2": ("closer", "CONGRATS", 0.16),
            "winner": ("tag", "WINNER", 0.12), "nodrink": ("tag", "DON'T", 0.36), "spray": ("tag", "SPRAY", 0.66), "purpose": ("tag", "PURPOSE", 0.9)})
        T["land"] = T["engine"] + 0.05                                # the engine lands on its word
        T["poof"] = T["congrats"]
        T["launch"] = s("break1") - 0.5
        T["slide"] = T["slides"] - 0.15
        T["stop"] = max(T["track"] + 0.1, T["slide"] + 0.9)
        T["arrows"] = min(T["lifting"], T["air"]) - 0.25               # the lift nobody wants
        T["press"] = max(T["squashes"] - 0.3, T["arrows"] + 0.5)
        T["fireon"] = min(T["catch"], T["brakes"]) - 0.1
        T["softl"] = min(T["soft"], T["tires"])
        T["up"] = T["jacks"]                                           # the jacks go up: the stopwatch starts
        T["done"] = min(T["up"] + 2.0, s("break4") - 0.8)
        T["g1"] = T["up"] + 0.1
        T["g2"] = lerp(T["up"] + 0.1, T["done"] - 0.15, 0.70)
        T["hit"] = e("break4") + 0.03
        T["scr"] = T["hit"] - 0.7
        T["cellcut"] = min(T["hit"] + 0.85, T["survival"] - 0.45)
        T["crunch"] = T["crumples"] + 0.05
        T["busdn"] = max(T["bus"] - 1.05, T["halo"] + 0.15)             # the halo is on before the bus comes down
        T["busrest"] = max(T["bus"] - 0.45, T["busdn"] + 0.5)
        T["busup"] = max(T["busrest"] + 0.5, min(T["bus"] + 0.35, T["crunch"] - 0.75))
        T["foil1"] = max(T["front"] - 0.1, T["upside"] + 0.8)           # the card with the wing section goes away
        T["wheelcut"] = max(T["steering"] - 0.4, T["stickers"] + 0.6)
        T["st0"] = T["cover"] + 0.2
        T["st1"] = max(T["st0"] + 0.3, T["wheelcut"] - 0.12)
        T["b0"] = max(T["steering"] + 0.25, T["wheelcut"] + 0.35)
        T["b1"] = max(T["b0"] + 0.6, T["buttons"] + 0.2)
        self.cut(s("break1") - 0.1, "top", 1)
        self.cut(s("fix1") - 0.12, "track", -1)
        self.cut(s("break2") - 0.1, "track", 1)
        self.cut(T["until"] - 0.12, "track", -1)
        self.cut(s("fix2") - 0.12, "brake", 1)
        self.cut(s("break3") - 0.1, "track", -1)
        self.cut(s("fix3") - 0.12, "track", 1)
        self.cut(s("break4") - 0.12, "track", -1)
        self.cut(T["cellcut"], "track", 1)
        self.cut(s("cta") + 0.05, "wheel", -1)
        self.cut(s("reveal") - 0.1, "track", 1)
        self.cut(T["wheelcut"], "wheel", -1)
        self.cut(T["s1"] - 0.35, "track", 1)
        self.cut(s("tag") - 0.2, "track", -1)
        cm = Camera(-20, -118, 2.3)
        cm.key(0.05, -20, -104, 2.6, 1.2)
        cm.key(T["poof"] - 0.1, 40, -221, 1.22, 0.5)
        cm.key(s("fix1") - 0.12, 15, -180, 1.5, 0.0).key(T["arrows"] - 0.3, 15, -196, 1.38, 0.8)
        cm.key(s("break2") - 0.1, 15, -110, 1.5, 0.0)
        cm.key(T["until"] - 0.12, 15, -180, 1.5, 0.0).key(T["fireon"] - 0.3, 30, -169, 1.6, 0.6)
        cm.key(s("break3") - 0.1, -10, -159, 1.7, 0.0)
        cm.key(s("fix3") - 0.12, RX + 50, -117, 2.3, 0.0).key(T["train"] - 0.3, 0, -216, 1.25, 0.55).key(T["up"] - 0.25, 10, -169, 1.6, 0.45)
        cm.key(s("break4") - 0.12, 40, -190, 1.42, 0.0)
        cm.key(T["cellcut"], 15, -174, 1.55, 0.0).key(T["busdn"] - 0.2, 30, -216, 1.25, 0.55).key(T["nose"] - 0.35, 110, -180, 1.5, 0.4)
        cm.key(s("reveal") - 0.1, 15, -180, 1.5, 0.0)
        cm.key(T["s1"] - 0.35, 0, -257, 1.05, 0.0).key(s("closer"), 0, -245, 1.1, 2.4)
        cm.key(s("tag") - 0.2, PODX, -117, 2.3, 0.0)
        self.cam = cm
        tc = T["crunch"]
        self.speed = (Track(0.0).to(s("fix1") - 0.12, 2000.0, 0.01).to(T["two"] + 0.45, 500.0, max(0.6, T["fire"] - T["two"] - 0.45), e_out)
                      .to(s("fix2") - 0.12, 0.0, 0.01).to(s("break3") - 0.1, 1700.0, 0.01).to(T["wear"], 800.0, 0.8)
                      .to(s("fix3") - 0.12, 0.0, 0.01).to(s("break4") - 0.12, 2600.0, 0.01).to(T["scr"], 700.0, 0.7).to(T["hit"], 0.0, 0.01)
                      .to(tc - 0.45, 1600.0, 0.08).to(tc, 0.0, 0.12))
        self._ts = np.arange(0.0, self.duration + 1.0, 1 / 120)
        self._dist = np.cumsum([self.speed.at(x) for x in self._ts]) / 120
        self.heat = Track(0.0).to(T["glowing"] - 0.35, 1.0, max(0.5, T["thousand"] - T["glowing"] + 0.35)).to(T["cool"], 0.6, 0.6)
        self.spans = [(T["slide"], T["road"]), (T["fireon"], T["cool"]), (T["wear"], T["done"]), (T["hit"], T["dont"])]
        self.shakes = [(T["land"], 0.35, 12), (T["stop"], 0.3, 9), (T["fireon"], 0.4, 6), (T["hit"], 0.5, 18), (T["busrest"], 0.25, 7),
                       (T["crunch"], 0.35, 10)]

    def dist_at(self, t):
        return float(np.interp(t, self._ts, self._dist))

    def phase(self, t):
        s, T = self.tl.s, self.T
        for name, t0 in (("tag", s("tag") - 0.2), ("stat", T["s1"] - 0.35), ("wheel2", T["wheelcut"]), ("reveal", s("reveal") - 0.1),
                         ("cta", s("cta") + 0.05), ("cell", T["cellcut"]), ("wall", s("break4") - 0.12), ("pit", s("fix3") - 0.12),
                         ("tires", s("break3") - 0.1), ("brakes", s("fix2") - 0.12), ("bfire", T["until"] - 0.12), ("ceiling", s("break2") - 0.1),
                         ("wings", s("fix1") - 0.12), ("corner", s("break1") - 0.1), ("kart", 0.0)):
            if t >= t0:
                return name

    # ------------------------------------------------------------------ set: the track, from the side
    def draw_track(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        cam = self.cam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        dist = self.dist_at(t)
        v = self.speed.at(t)
        rot = math.degrees(dist / RW)
        v2.sky(c, W, H, 0.0, horizon_y=gy - 140 * z)
        v2.stars(c, W, H, t, 0.7)
        if ph != "ceiling":
            self.far(c, t, cam, gy, dist)
            c.drawRect(R(0, 0, W, gy), P("#0B1024", 0.3))
        self.view(c, cam)
        v2.ground(c, -3400, 3400)
        if ph == "ceiling":                                                  # a tunnel: there is a ceiling to drive on
            c.drawRect(R(-2000, -340, 4000, 340), lin_paint(0, -340, 0, 0, ["#131936", "#1B2140"]))
            c.drawRect(R(-2000, -1500, 4000, 1160), lin_paint(0, -1500, 0, -340, ["#05070F", "#0D1228"]))
            c.drawRect(R(-2000, -346, 4000, 8), P("#3A4259"))
            c.drawRect(R(-2000, -150, 4000, 5), P(ACCENT, 0.45))
            for k in range(-3, 4):
                x0 = k * 640 - (dist % 640)
                c.drawRect(R(x0 + 320, -338, 6, 338), P("#0D1228"))
                c.drawRRect(rr(x0, -338, 170, 10, 5), P("#FFF1C9"))
                add_glow(c, x0 + 85, -326, 130, "#FFF1C9", 0.5)
        else:
            self.near(c, t, dist, ph)
        if ph == "kart":
            self.d_kart(c, t)
        elif ph == "wings":
            self.d_wings(c, t, rot)
        elif ph == "ceiling":
            c.save()
            c.translate(0, -340)
            c.scale(1, -1)
            car(c, t, rot=rot, squat=3, flame=0.3)
            c.restore()
        elif ph == "bfire":
            self.d_bfire(c, t, rot)
        elif ph == "tires":
            self.d_tires(c, t, rot)
        elif ph == "pit":
            self.d_pit(c, t)
        elif ph == "wall":
            self.d_wall(c, t, dist, rot)
        elif ph == "cell":
            self.d_cell(c, t, dist, rot)
        elif ph == "reveal":
            paint = prog(t, T["cover"] - 0.15, T["cover"] + 0.25)
            nst = len(STICKERS) * prog(t, T["st0"], T["st1"])
            car(c, t, halo=1, paint=paint, stickers=nst, flame=0.2)
            if 0 < paint < 1:
                puff(c, 264 - 520 * paint, -70, 70, PAINT, 0.7, k=2)
        elif ph == "stat":
            self.d_grid(c, t)
        elif ph == "tag":
            self.d_tag(c, t)
        c.restore()
        if ph in ("wings", "ceiling", "bfire", "tires", "wall") and v > 300:
            hstreaks(c, t, clamp(v / 2400), 260, gy - 30, seed=5)
        self.ui["cam"] = cam
        self.ui["v"] = v

    def far(self, c, t, cam, gy, dist):
        """The city far away, then the grandstands and the lights."""
        cx, cy, z = cam
        c.save()
        c.translate(W / 2, gy)
        c.scale(z, z)
        off = (cx * 0.06 + dist * 0.03) % 2400
        for k in (-1, 0, 1):
            c.save()
            c.translate(k * 2400 - off, 0)
            skyline_night(c, 0, 2400, 0, seed=7, hmin=200, hmax=560, lit=0.3, t=t)
            c.restore()
        off = (cx * 0.5 + dist * 0.4) % 1500
        for k in (-1, 0, 1):
            c.save()
            c.translate(k * 1500 - off - 320, 0)
            stand(c, t, seed=3)
            floodlight(c, 1200, 640, 760, 0, t, 1.0)
            c.restore()
        c.restore()

    def near(self, c, t, dist, ph):
        """The fence, the barrier and its boards, and the kerb: everything that rushes past right behind the car."""
        if ph != "pit":
            off = dist % 800
            g0 = int(dist // 800)
            for k in range(-3, 4):
                x0 = k * 800 - off + (PODX if ph == "tag" else 0)
                c.drawRect(R(x0, -200, 800, 3), P("#94A3B8", 0.4))
                for yy in (-156, -112):
                    c.drawRect(R(x0, yy, 800, 2), P("#94A3B8", 0.22))
                c.drawRect(R(x0 + 396, -204, 8, 204), P("#4B5568"))
                box(c, x0, -58, 800, 46, "#2E3550")
                c.drawRect(R(x0, -58, 800, 4), P("#5C6B96", 0.8))
                for j in range(4):                                             # dim marks on the barrier: they show the speed
                    c.drawRect(R(x0 + 60 + j * 200, -44, 90, 20), P("#FFFFFF", 0.07 + 0.05 * ((k + g0 + j) % 2)))
        off = dist % 720
        for k in range(-5, 6):
            x0 = k * 720 - off
            c.drawRect(R(x0, 0, 360, 9), P("#EF4444"))
            c.drawRect(R(x0 + 360, 0, 360, 9), P("#F8FAFC"))

    # ---- the hook: a kart, a huge engine, a race car
    def d_kart(self, c, t):
        T, s = self.T, self.tl.s
        poof, land = T["poof"], T["land"]
        back = e_out(prog(t, poof - 0.05, poof + 0.3))
        if back > 0:
            c.save()
            c.translate(380, 0)
            c.scale(e_back(back), e_back(back))
            self.crew(c, t, "cheer", xs=(-38, 0, 38), y=0, face=-1, h=104)
            c.restore()
        if t < poof + 0.08:
            k0 = e_back(prog(t, 0.08, 0.4))
            ey = lerp(-900, -42, e_in(prog(t, land - 0.5, land)))
            sq = bump(t, land, land + 0.35)
            tilt = -7 * prog(t, land, land + 0.12) * (1 - 0.5 * prog(t, land + 0.12, land + 0.5))
            c.save()
            c.scale(1.2 * k0, 1.2 * k0)
            kart(c, t, tilt=tilt, sq=sq, engine_y=ey + 3 * sq if t >= land - 0.5 else None, run=prog(t, land + 0.7, land + 0.9))
            c.restore()
            for i, bx in enumerate((-190, -54)):                             # two bolts go in
                sparks_shower(c, bx, -56, t, land + 0.25 + i * 0.18, 0.35, n=10, speed=360, seed=20 + i)
        if t >= poof:
            k1 = lerp(0.7, 1.0, e_back(prog(t, poof, poof + 0.3)))
            rv = prog(t, T["race"] - 0.05, T["race"] + 0.15)
            c.save()
            c.scale(k1, k1)
            car(c, t, fw=0, rw=0, flame=rv * (0.8 + 0.2 * math.sin(t * 40)), squat=1.5 * rv * math.sin(t * 60))
            c.restore()
        if poof - 0.05 <= t < poof + 0.6:
            u = prog(t, poof - 0.05, poof + 0.6)
            for i in range(10):
                an = i * 0.66
                puff(c, math.cos(an) * 200 * e_out(u) * (0.45 + (i % 3) * 0.3), -76 + math.sin(an) * 76 * e_out(u), 62 + 74 * u, "#E5E9F2",
                     0.92 * (1 - u), k=i)

    # ---- fix 1: wings, upside down
    def d_wings(self, c, t, rot):
        T = self.T
        fwk = e_back(prog(t, T["wings"] - 0.15, T["wings"] + 0.1))
        rwk = e_back(prog(t, T["wings"] - 0.02, T["wings"] + 0.24))
        press = prog(t, T["press"], T["press"] + 0.35)
        car(c, t, rot=rot, fw=fwk, rw=rwk, squat=7 * press, flame=0.35)
        la = self.span(T["arrows"], T["press"] + 0.15, 0.2, 0.25)
        for ax, y0 in ((-236, -172), (262, -52)):                            # lift: what a wing does the right way up
            if la > 0:
                c.drawLine(ax, y0, ax, y0 - 96, dash_paint(WARN, la, 9, t * 2, 18, 12))
                arrow(c, ax, y0 - 96, ax, y0 - 128, WARN, 9, la, 20)
                if t >= T["press"] - 0.2:
                    c.drawLine(ax - 26, y0 - 100, ax + 26, y0 - 40, P("#FFFFFF", la, stroke=8))
                    c.drawLine(ax + 26, y0 - 100, ax - 26, y0 - 40, P("#FFFFFF", la, stroke=8))
        ak = prog(t, T["press"] - 0.25, T["press"] + 0.2)
        if ak > 0:                                                           # the air, coming over the car
            env = ((540, -34), (340, -36), (252, -66), (130, -104), (30, -136), (-70, -156), (-200, -172), (-290, -172), (-560, -150))
            for j in range(5):
                p = skia.Path()
                for i, (ex, ey) in enumerate(env):
                    yy = ey - (16 + j * 30) * (1.0 if 0 < i < len(env) - 1 else 0.6 + 0.1 * j)
                    if i == 0:
                        p.moveTo(ex, yy)
                    else:
                        px_, py_ = env[i - 1][0], env[i - 1][1] - (16 + j * 30) * (1.0 if 0 < i - 1 < len(env) - 1 else 0.6 + 0.1 * j)
                        p.quadTo(px_, py_, (px_ + ex) / 2, (py_ + yy) / 2)
                p.lineTo(env[-1][0], env[-1][1] - (16 + j * 30) * (0.6 + 0.1 * j))
                c.drawPath(p, dash_paint("#BFDBFE", 0.75 * ak, 4, t * 9 + j * 0.3, 34, 22))
            for ax, y0, y1 in ((-236, -330, -178), (262, -214, -62)):        # ...and pressing down on both wings
                b = math.sin(t * 9) * 7
                arrow(c, ax, y0 + b, ax, y1 + b, HILITE, 13, ak, 26)

    # ---- break 2: two hundred miles an hour, and the brakes
    def d_bfire(self, c, t, rot):
        T = self.T
        br = prog(t, T["brake"], T["brake"] + 0.25)
        heat = prog(t, T["brake"], T["fireon"] + 0.2)
        fire = prog(t, T["fireon"], T["fireon"] + 0.3)
        car(c, t, rot=rot, pitch=2.2 * br, glow=(heat, heat * 0.85), flame=0.3 * (1 - br))
        if fire > 0:
            for wx in (FX, RX):
                v2.flame(c, wx - 4, -RW - 14, 44, 150, t, fire, seed=int(wx), ang=246)
            v2.smoke(c, 0, 0, t, T["fireon"], None, rate=24, life=1.3, spread=(40, -70), rise=-110, size=(24, 110), col="#565D75",
                     lit_until=0.4, seed=3, origin=lambda tb: (FX - 20 - 650 * (t - tb), -90))
            v2.smoke(c, 0, 0, t, T["fireon"], None, rate=18, life=1.1, spread=(40, -70), rise=-110, size=(24, 100), col="#565D75",
                     lit_until=0.4, seed=4, origin=lambda tb: (RX - 20 - 650 * (t - tb), -90))

    # ---- break 3: soft, sticky tires
    def d_tires(self, c, t, rot):
        T, s = self.T, self.tl.s
        wr = prog(t, s("break3") + 0.2, T["wear"] + 0.2)
        gone = prog(t, T["wear"], T["wear"] + 0.3)
        c.save()
        c.translate(0, math.sin(t * 31) * 1.6 * gone)
        car(c, t, rot=rot, wear=(wr, wr), flame=0.3 * (1 - gone))
        c.restore()
        for wx in (RX, FX):                                                  # rubber, leaving
            rng = random.Random(int(wx))
            for i in range(16):
                u = (t * 2.0 + i / 16) % 1.0
                vx, vy = -rng.uniform(260, 640), -rng.uniform(40, 280)
                px = wx - RW * 0.6 + vx * u * 0.6
                py = -8 + vy * u * 0.6 + 760 * (u * 0.6) ** 2
                if py < 0:
                    c.drawCircle(px, py, rng.uniform(2.5, 5.5), P("#0B0F1A", (0.35 + 0.65 * wr) * (1 - u)))
        if gone > 0:
            for wx, sd in ((RX, 5), (FX, 6)):
                v2.smoke(c, 0, 0, t, T["wear"], None, rate=16, life=1.0, spread=(30, -30), rise=-70, size=(16, 76), col="#9AA1B5", lit_until=0,
                         seed=sd, a=0.7, origin=lambda tb, wx=wx: (wx - 20 - 600 * (t - tb), -16))

    # ---- fix 3: the pit stop
    BACK = ((-360, "look"), (-296, "duck"), (-222, "duck"), (-160, "look"), (-96, "duck"), (-30, "look"), (40, "look"), (104, "duck"),
            (170, "look"), (236, "duck"), (300, "duck"), (362, "look"))                                   # 12 on the far side
    NEAR = ((-398, "look", 1), (-322, "carry", 1), (-222, "duck", 1), (-84, "carry", -1), (112, "carry", 1), (244, "duck", -1),
            (350, "carry", -1), (400, "look", -1))                                                        # 8 on the near side: twenty

    def crew_x(self, t, i, xf):
        a0 = self.T["train"] - 0.15 + 0.022 * i
        k = e_out(prog(t, a0, a0 + 0.42))
        return xf + (1 if xf > 0 else -1) * 760 * (1 - k), k

    def d_pit(self, c, t):
        T, s = self.T, self.tl.s
        up, done = T["up"], T["done"]
        # the garage
        box(c, -700, -330, 1400, 330, "#1B2140")
        c.drawRect(R(-700, -338, 1400, 12), P("#39437A"))
        for gx in (-420, 0, 420):
            lit = gx == 0
            c.drawRRect(rr(gx - 160, -252, 320, 252, 8), P("#2A2F4A" if lit else "#0B1024"))
            if lit:
                add_glow(c, gx, -130, 280, "#FFE9B8", 0.32)
                for i in range(5):
                    c.drawRRect(rr(gx - 130 + i * 56, -220, 36, 60, 5), P("#3B4160"))
                c.drawRect(R(gx - 160, -264, 320, 16), P(PAINT))
                sticker(c, "num", gx, -256, 15, 1.0)
        c.drawRect(R(-330, -410, 660, 14), P("#4B5568"))                      # the gantry over the box
        for px in (-330, 322):
            c.drawRect(R(px, -410, 8, 410), P("#4B5568"))
        go = t >= done
        box(c, -22, -396, 44, 70, "#0B0F1A", r=8)
        c.drawCircle(0, -376, 13, P("#EF4444" if not go else "#3F1D1D"))
        c.drawCircle(0, -346, 13, P("#34D399" if go else "#14382B"))
        add_glow(c, 0, -346 if go else -376, 60, GOOD if go else WARN, 0.7)
        for bx in (-300, 300):                                               # the box, painted on the ground
            c.drawRect(R(bx - 4, -2, 8, 6), P("#FDE047"))
        # the car comes in, stops, leaves
        carx = -900 * (1 - e_out(prog(t, s("fix3") - 0.12, T["nut"] - 0.3))) + 1700 * e_in(prog(t, done + 0.12, done + 0.9))
        lift = 20 * (e_out(prog(t, up - 0.15, up + 0.02)) - e_in(prog(t, done - 0.12, done)))
        u = prog(t, up + 0.1, done - 0.15)
        for i, (xf, pose) in enumerate(self.BACK):                           # the far side of the car
            x, k = self.crew_x(t, i, xf)
            engineer(c, x, 0, 108 + (i % 3) * 5, SHIRTS[i % 3], t + i * 0.3, "walk" if k < 1 else "cheer" if go else pose, soot=0.25,
                     face=1 if xf < 0 else -1)
        c.save()
        c.translate(carx, 0)
        rot = math.degrees(carx / RW)
        working = up - 0.15 <= t < done
        c.save()
        c.translate(0, -lift)
        car(c, t, rot=rot, wheels=not working, wear=(1.0, 1.0) if t < up else (0.0, 0.0), flame=0.2 + 0.7 * prog(t, done + 0.05, done + 0.3))
        c.restore()
        if working:
            for wx, inner in ((RX, 1), (FX, -1)):
                o = e_in(prog(u, 0.18, 0.40))
                if o < 1:                                                    # the old wheel comes off
                    wheel(c, wx - inner * 30 * o, -RW - lift + 24 * o, rot, 1.0, a=1 - o)
                if u >= 0.35:                                                # the fresh one goes on
                    n_ = e_out(prog(u, 0.35, 0.70))
                    wheel(c, lerp(wx + inner * 66, wx, n_), lerp(-62, -RW - lift, n_), 0.0, 0.0)
        c.restore()
        if lift > 0.5:                                                       # the jacks
            for jx, hx in ((-244, -308), (276, 338)):
                c.drawLine(jx, -8, hx, -64, P("#E5E9F2", 1, stroke=7))
                c.drawCircle(jx, -8, 9, P("#475569"))
                box(c, min(jx, jx + (16 if jx < 0 else -16)), -20 - lift * 0.7, 16, 12, "#FDE047", r=3)
        for i, (xf, pose, face) in enumerate(self.NEAR):                     # the near side
            x, k = self.crew_x(t, 12 + i, xf)
            if pose == "carry" and abs(xf) < 200:
                p_ = "carry" if u < 0.7 else "cheer" if go else "look"
            else:
                p_ = "cheer" if go else pose
            engineer(c, x, 0, 116 + (i % 2) * 6, SHIRTS[(i + 1) % 3], t + i * 0.41, "walk" if k < 1 else p_, face=face)
            if pose == "carry" and abs(xf) < 200 and u < 0.35:               # the fresh wheel waits in his arms
                wx = RX if xf < 0 else FX
                wheel(c, wx + (1 if xf < 0 else -1) * 66 + (x - xf), -62, 0.0, 0.0)
            if pose == "duck" and k >= 1 and not go:                         # the gunners
                wx = RX if xf < 0 else FX
                sd = 1 if xf < 0 else -1
                gy_ = -RW - lift
                c.drawRRect(rr(wx - sd * 44 - 17, gy_ - 9, 34, 18, 6), P(PAINT))
                c.drawRect(R(min(wx - sd * 12, wx - sd * 30), gy_ - 5, 18, 10), P("#CBD5E1"))
                c.drawRRect(rr(wx - sd * 52 - 6, gy_ + 4, 12, 22, 4), P("#1F2937"))
                hose = skia.Path()
                hose.moveTo(wx - sd * 56, gy_ + 22)
                hose.cubicTo(wx - sd * 90, gy_ + 60, wx - sd * 120, -200, wx - sd * 96, -404)
                c.drawPath(hose, P("#0EA5E9", 0.9, stroke=5))
                for tg in (T["g1"], T["g2"]):
                    sparks_shower(c, wx, gy_, t, tg, 0.3, n=12, speed=420, seed=int(wx + tg * 10), cone=(0, 360))

    # ---- break 4: a wall
    def d_wall(self, c, t, dist, rot):
        T = self.T
        hit = T["hit"]
        wx = 262 + self.dist_at(hit) - dist
        wall(c, wx, cracked=1.0 if t >= hit else 0.0)
        dt = t - hit
        if dt < 0:
            lock = prog(t, T["scr"], T["scr"] + 0.15)
            car(c, t, rot=rot if lock < 1 else self.dist_at(T["scr"] + 0.15) / RW * 57.3, pitch=2.0 * lock, flame=0.3 * (1 - lock))
            if lock > 0:
                for wxx, sd in ((RX, 11), (FX, 12)):
                    v2.smoke(c, 0, 0, t, T["scr"], None, rate=26, life=0.7, spread=(30, -30), rise=-60, size=(14, 60), col="#C7CCDA", lit_until=0,
                             seed=sd, a=0.75, origin=lambda tb, wxx=wxx: (wxx - 30 - 900 * (t - tb), -10))
            return
        kick = bump(t, hit, hit + 0.45)
        c.save()
        c.rotate(9 * kick, FX, 0)
        car(c, t, rot=rot, fw=0, nose=1.0, wheels=False, dizzy=prog(t, hit + 0.15, hit + 0.3))
        wheel(c, RX, -RW, rot, 0.3)
        c.restore()
        wheel(c, FX - 60 - 380 * dt, -RW - abs(math.sin(dt * 6.0)) * 170 * math.exp(-dt * 1.4), rot - 900 * dt, 0.3)   # one wheel leaves
        v2.debris(c, 250, -40, t, hit, 1.6, n=14, speed=720, seed=4, floor=0, cone=(190, 300), size=(8, 26),
                  cols=("#CBD5E1", "#3A4158", "#1F2937"))
        sparks_shower(c, 256, -40, t, hit, 0.6, n=30, speed=820, seed=7, cone=(160, 290))
        v2.smoke(c, 236, -44, t, hit, hit + 0.3, rate=30, life=1.4, spread=(170, -120), rise=-80, size=(30, 120), col="#8B93A8",
                 lit_until=0.3, seed=9)

    # ---- fix 4: the survival cell, the halo, the nose
    def d_cell(self, c, t, dist, rot):
        T = self.T
        tc = T["crunch"]
        xr = prog(t, T["cellcut"] + 0.15, T["cellcut"] + 0.55)
        cellk = prog(t, T["survival"] - 0.2, T["survival"] + 0.1)
        halok = e_back(prog(t, T["halo"] - 0.15, T["halo"] + 0.12))
        wx = 204 + self.dist_at(tc + 0.12) - dist
        nose = clamp((260 - wx) / 57.7)
        bdn, brest, bup = T["busdn"], T["busrest"], T["busup"]
        sits = brest <= t < bup
        car(c, t, rot=rot, halo=halok, nose=nose, xray=xr, cell=cellk, squat=6.0 if sits else 0.0, flame=0.2,
            thumb=prog(t, T["dont"] - 0.12, T["dont"] + 0.05))
        if bdn <= t < bup + 0.45:
            by = lerp(-1200, -128, e_out(prog(t, bdn, brest))) if t < bup else lerp(-128, -1500, e_in(prog(t, bup, bup + 0.45)))
            if sits:
                by += 6
            c.drawLine(38, by - 270, 38, by - 2400, P("#E5E9F2", 1, stroke=5))
            c.drawRRect(rr(18, by - 292, 40, 22, 6), P("#FDE047"))
            bus(c, 38, by)
            if sits:
                for sd in (-1, 1):
                    for j in range(3):
                        c.drawLine(38 + sd * (70 + j * 16), -120 + j * 4, 38 + sd * (84 + j * 16), -112 + j * 4, P(HILITE, 0.9, stroke=4))
        if wx < 1400:
            wall(c, wx, cracked=prog(t, tc, tc + 0.1))
        if t >= tc:
            sparks_shower(c, 236, -38, t, tc, 0.5, n=20, speed=520, seed=13, cone=(170, 290))
            v2.debris(c, 232, -40, t, tc, 1.2, n=8, speed=380, seed=14, floor=0, cone=(190, 280), size=(5, 14),
                      cols=("#CBD5E1", "#3A4158", "#6B7385"))

    # ---- the grid: three numbers and the closer
    def d_grid(self, c, t):
        T, s = self.T, self.tl.s
        won = t >= T["cong2"]
        for px in (-474, 466):                                               # the start lights
            c.drawRect(R(px, -440, 8, 440), P("#4B5568"))
        c.drawRect(R(-474, -440, 948, 14), P("#4B5568"))
        box(c, -190, -452, 380, 66, "#0B0F1A", r=10)
        for i in range(5):
            lx = -144 + i * 72
            on = (not won) and t >= T["s1"] - 0.2 + i * 0.12
            c.drawCircle(lx, -419, 20, P("#34D399" if won else "#EF4444" if on else "#2A1416"))
            if on or won:
                add_glow(c, lx, -419, 64, GOOD if won else WARN, 0.75)
        for i in range(10):                                                  # the line
            c.drawRect(R(282 + (i % 2) * 14, 0 + (i // 2) * 2, 14, 2), P("#F8FAFC"))
        xs = (-440, -398, -356)
        self.crew(c, t, "cheer" if won else "look", xs=xs, y=0, face=1, h=110)
        if won:
            hats_in_the_air(c, xs, -124, t, T["cong2"], height=210)
        rv = prog(t, T["cong2"], T["cong2"] + 0.2) * (0.6 + 0.4 * math.sin(t * 40))
        car(c, t, halo=1, paint=1, stickers=len(STICKERS), flame=0.22 + 0.6 * rv)
        # the flag
        person(c, 420, 0, 118, "#F8FAFC", t, "cheer" if won else "stand", face=-1, hat="cap")
        fa = math.sin(t * (9 if won else 2.5)) * (22 if won else 6)
        c.save()
        c.translate(398, -132)
        c.rotate(-18 + fa)
        c.drawLine(0, 0, 0, -120, P("#CBD5E1", 1, stroke=5))
        for i in range(5):
            for j in range(4):
                wv = math.sin(t * 8 + i * 0.9) * 5 * (i / 4)
                c.drawRect(R(-90 + i * 18 - 0.5, -120 + j * 16 + wv, 18.5, 16.5), P("#F8FAFC" if (i + j) % 2 == 0 else "#0B0F1A"))
        c.restore()

    # ---- the tag: the winner's drink
    def d_tag(self, c, t):
        T = self.T
        spray = T["spray"]
        box(c, PODX - 270, -420, 540, 420, "#1B2140", r=10)                    # the board behind
        for i in range(6):
            for j in range(4):
                if (i + j) % 2 == 0:
                    c.drawRect(R(PODX - 270 + i * 90, -420 + j * 80, 90, 80), P("#FFFFFF", 0.05))
        c.drawRect(R(PODX - 270, -420, 540, 10), P(PAINT))
        box(c, PODX - 180, -54, 120, 54, "#CBD5E1", r=6)
        box(c, PODX + 60, -36, 120, 36, "#CBD5E1", r=6)
        box(c, PODX - 60, -84, 120, 84, "#F8FAFC", r=6)
        for n_, nx, ny in (("2", PODX - 120, -14), ("1", PODX, -26), ("3", PODX + 120, -6)):
            text(c, n_, nx, ny, 40, "#0B1024", "Poppins-Black")
        wet = prog(t, spray + 0.12, spray + 0.45)
        shake = prog(t, T["nodrink"] - 0.2, spray)
        pose = "carry" if t < spray + 0.15 else "shrug"
        for sd, py, sh in ((-1, -54, SHIRTS[1]), (1, -36, SHIRTS[2])):
            x = PODX + sd * 120
            engineer(c, x, py, 112, sh, t + sd * 0.3, pose, face=-sd, wet=wet)
            if t < spray + 0.15:                                             # a cup, held out in hope
                c.drawRRect(rr(x - sd * 40 - 9, py - 76, 18, 22, 4), P("#F8FAFC"))
        person(c, PODX, -84, 124, PAINT, t, "cheer", face=1, hat="cap")
        on = t >= spray
        bx, by = PODX + math.sin(t * 34) * 7 * shake, -84 - 176 + math.cos(t * 29) * 4 * shake
        c.save()
        c.translate(bx, by)
        c.rotate(math.sin(t * 5.5) * 38 if on else math.sin(t * 34) * 9 * shake)
        c.drawRRect(rr(-13, -20, 26, 50, 9), lin_paint(-13, 0, 13, 0, ["#34D399", "#047857"]))
        c.drawRRect(rr(-6, -44, 12, 28, 5), P("#047857"))
        c.drawRect(R(-13, 0, 26, 14), P("#FDE68A"))
        c.drawRRect(rr(-7, -50, 14, 9, 3), P("#FDE047"))
        c.restore()
        if on:
            ak = prog(t, spray, spray + 0.15)
            for sd in (-1, 1):
                for i in range(18):
                    u = (t * 2.2 + i / 18) % 1.0
                    px = PODX + sd * (8 + 126 * u) + math.sin(i * 7.3) * 9
                    py = -306 - 64 * math.sin(math.pi * u) + 150 * u + math.cos(i * 5.1) * 9
                    c.drawCircle(px, py, 7 * (1 - 0.4 * u), P("#FEF9C3" if i % 3 else "#FFFFFF", 0.9 * ak))
                hy = -170 if sd < 0 else -152                                  # ...and off their hard hats
                for i in range(6):
                    u = (t * 3.0 + i / 6) % 1.0
                    c.drawCircle(PODX + sd * 120 + math.sin(i * 2.4) * 34 * u, hy - 26 * math.sin(math.pi * u) + 20 * u, 4 * (1 - u) + 1.5,
                                 P("#FEF9C3", 0.9 * ak * (1 - u)))

    # ------------------------------------------------------------------ set: the corner, from above
    def draw_top(self, c, t):
        T, s = self.T, self.tl.s
        ts, tstop = T["slide"], T["stop"]
        if t <= ts:
            py = 1500.0 * (ts - t)
        else:
            py = -340 * (1 - (1 - prog(t, ts, tstop)) ** 3)
        yaw = 26 * e_out(prog(t, ts, tstop))
        steer = 26 * prog(t, ts - 0.4, ts - 0.12)
        oy = (900 - py) * 1.5
        c.drawRect(R(0, 0, W, H), P("#0E2A1F"))
        rng = random.Random(2)
        for _ in range(90):
            gx, g0, gr = rng.uniform(0, W), rng.uniform(0, 2400), rng.uniform(3, 7)
            c.drawCircle(gx, (g0 + oy) % 2400 - 240, gr, P("#1B4A33"))
        c.save()
        c.translate(540, 900)
        c.scale(1.5, 1.5)
        c.translate(-540, -py)
        c.drawRRect(rr(290, -500, 640, 560, 60), P("#6B6350"))                 # the gravel
        rng = random.Random(5)
        for _ in range(260):
            c.drawCircle(rng.uniform(300, 920), rng.uniform(-490, 50), rng.uniform(2, 4), P(rng.choice(("#8A8068", "#4F493B", "#A39A80")), 0.8))
        for i in range(17):                                                  # the tire wall
            c.drawCircle(308 + i * 38, -486, 19, P("#0B0F1A"))
            c.drawCircle(308 + i * 38, -486, 9, P("#EF4444" if i % 2 == 0 else "#F8FAFC"))
        road = skia.Path()
        road.moveTo(430, 4600)
        road.lineTo(430, 0)
        road.arcTo(R(430, -330, 660, 660), 180, 90, False)
        road.lineTo(1300, -330)
        road.lineTo(1300, -110)
        road.lineTo(760, -110)
        road.arcTo(R(650, -110, 220, 220), 270, -90, False)
        road.lineTo(650, 4600)
        road.close()
        c.drawPath(road, P("#262B3D"))
        for path_r, x0 in ((330, 430), (110, 650)):                          # kerbs round the corner
            kp = skia.Path()
            kp.addArc(R(760 - path_r, -path_r, path_r * 2, path_r * 2), 180, 90)
            c.drawPath(kp, P("#F8FAFC", 1, stroke=18, cap="butt"))
            pr = P("#EF4444", 1, stroke=18, cap="butt")
            pr.setPathEffect(skia.DashPathEffect.Make([40, 40], 0))
            c.drawPath(kp, pr)
        for yy in range(0, 4600, 300):                                       # and along the straight: they show the speed
            for x0 in (412, 650):
                c.drawRect(R(x0, yy, 18, 150), P("#EF4444"))
                c.drawRect(R(x0, yy + 150, 18, 150), P("#F8FAFC"))
        c.drawRect(R(760, -348, 540, 18), P("#F8FAFC", 0.9))
        c.drawRect(R(760, -110, 540, 8), P("#F8FAFC", 0.9))
        line = skia.Path()                                                   # the way round
        line.moveTo(540, 700)
        line.lineTo(540, 0)
        line.arcTo(R(540, -220, 440, 440), 180, 90, False)
        line.lineTo(1300, -220)
        c.drawPath(line, dash_paint(GOOD, 0.85, 7, t * 5, 30, 24))
        if t > ts:                                                           # where it went instead
            for dx in (-28, 28):
                c.drawLine(540 + dx, 20, 540 + dx + yaw * 0.6 * (1 if dx > 0 else -0.2), py + 50, P("#0B0F1A", 0.75, stroke=11))
            if py < -200:
                gk = prog(t, ts, tstop + 0.1) * (1 - prog(t, tstop + 0.3, tstop + 1.2))
                for i in range(7):
                    puff(c, 540 + math.sin(i * 2.1) * 46, py + 70 + i * 30, 34 + i * 9, "#A39A80", 0.55 * gk * (1 - i / 8), k=i)
        car_top(c, 540, py - 6 * bump(t, tstop, tstop + 0.25), yaw, steer)
        c.restore()
        v2.speed_streaks(c, W, H, t, 0.55 * (1 - prog(t, ts, ts + 0.5)), seed=9, n=22)
        pk = prog(t, ts, ts + 0.4)
        if pk > 0:
            c.drawRRect(rr(30, self.CAPTION_Y - 105, W - 60, 190, 44), P("#0B1024", 0.62 * pk, blur=22))
        self.ui["cam"] = (0, 0, 1)

    # ------------------------------------------------------------------ set: one wheel, cut open
    def draw_brake(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#151B38", "#0B1024", "#070B1F"]))
        c.drawRect(R(0, 1084, W, H - 1084), lin_paint(0, 1084, 0, H, ["#232A45", "#0C1024"]))
        c.drawRect(R(0, 1084, W, 6), P("#39425A"))
        X0, Y0, RO = 540, 772, 310
        heat = self.heat.at(t)
        spin = t * 300 * (1 - 0.6 * prog(t, T["glowing"] - 0.35, T["thousand"]))
        dk = e_back(prog(t, T["discs"] - 0.3, T["discs"]))
        pk = e_back(prog(t, T["pads"] - 0.3, T["pads"]))
        duk = prog(t, T["ducts"] - 0.3, T["ducts"] + 0.1)
        c.drawCircle(X0, Y0, RO, P("#0B0F1A"))                                # the tire and the rim, seen through
        c.drawCircle(X0, Y0, RO - 16, P("#EF4444", 0.9, stroke=7))
        c.drawCircle(X0, Y0, RO - 86, P("#10152B"))
        c.drawCircle(X0, Y0, RO - 86, P("#CBD5E1", 1, stroke=12))
        c.save()
        c.translate(X0, Y0)
        c.rotate(spin)
        for i in range(5):
            c.save()
            c.rotate(i * 72)
            c.drawRRect(rr(40, -13, RO - 132, 26, 8), P("#CBD5E1", 0.13))
            c.restore()
        c.restore()
        RD = 180 * dk
        if RD > 2:                                                           # the carbon disc
            add_glow(c, X0, Y0, RD * 1.8, "#FF5A1F", 0.9 * heat)
            c.drawCircle(X0, Y0, RD, rad_paint(X0, Y0, RD, [mix("#3A3F4E", "#FFD27A", heat), mix("#2B2F3A", "#FF5A1F", heat),
                                                           mix("#1B1E27", "#C2410C", heat)], [0.0, 0.72, 1.0]))
            for i in range(40):
                an = math.radians(spin + i * 9)
                c.drawCircle(X0 + math.cos(an) * RD * 0.93, Y0 + math.sin(an) * RD * 0.93, 4.5, P("#0B0F1A", 0.85))
            for i in range(10):
                an = math.radians(spin + i * 36)
                c.drawLine(X0 + math.cos(an) * RD * 0.46, Y0 + math.sin(an) * RD * 0.46, X0 + math.cos(an + 0.3) * RD * 0.82,
                           Y0 + math.sin(an + 0.3) * RD * 0.82, P("#000000", 0.16, stroke=5))
            c.drawCircle(X0, Y0, 66 * dk, P("#94A3B8"))
            c.drawCircle(X0, Y0, 66 * dk, P("#E5E9F2", 1, stroke=4))
            nut = skia.Path()
            for i in range(6):
                an = math.radians(spin * 1.0 + i * 60)
                if i == 0:
                    nut.moveTo(X0 + math.cos(an) * 30 * dk, Y0 + math.sin(an) * 30 * dk)
                else:
                    nut.lineTo(X0 + math.cos(an) * 30 * dk, Y0 + math.sin(an) * 30 * dk)
            nut.close()
            c.drawPath(nut, P("#FBBF24"))
        if pk > 0:                                                           # the caliper, with a pad in its window
            c.save()
            c.translate(X0, Y0)
            c.rotate(-28)
            c.scale(pk, pk)
            c.drawArc(R(-152, -152, 304, 304), -27, 54, False, P(PAINT, 1, stroke=92, cap="butt"))
            c.drawArc(R(-152, -152, 304, 304), -27, 54, False, P(shade(PAINT, -0.3), 1, stroke=6, cap="butt"))
            c.drawArc(R(-150, -150, 300, 300), -15, 30, False, P(mix("#7C2D12", "#FFB347", heat), 1, stroke=46, cap="butt"))
            for an in (-21, 21):
                c.drawCircle(math.cos(math.radians(an)) * 176, math.sin(math.radians(an)) * 176, 8, P("#1F2937"))
            c.restore()
            if heat > 0.15 and t < T["cool"] + 0.4:
                an = math.radians(-28 + 16)
                sparks_shower(c, X0 + math.cos(an) * 170, Y0 + math.sin(an) * 170, t, t - (t % 0.14), 0.3, n=7, speed=420,
                              seed=int(t * 7), cone=(20, 110))
        if duk > 0:                                                          # the duct brings air to the middle of the disc
            dx = -180 * (1 - e_out(duk))
            duct = skia.Path()
            for i, (px, py) in enumerate(((0, 610), (150, 650), (300, 724), (X0 - 150, Y0 - 34), (X0 - 150, Y0 + 34), (300, 824), (150, 896),
                                          (0, 936))):
                if i == 0:
                    duct.moveTo(px + dx, py)
                else:
                    duct.lineTo(px + dx, py)
            duct.close()
            c.drawPath(duct, P("#0EA5E9", 0.20 * duk))
            c.drawPath(duct, P("#7DD3FC", duk, stroke=5))
            rng = random.Random(8)
            for i in range(16):
                u = (t * 1.5 + i / 16) % 1.0
                yy = Y0 + rng.uniform(-150, 150) * (1 - u) ** 1.4 + rng.uniform(-22, 22) * u
                xx = lerp(0, X0 - 60, u)
                c.drawLine(xx, yy, xx + 34, yy, P("#E0F2FE", duk * (0.5 + 0.5 * u), stroke=5))
            for i in range(12):                                              # ...and it leaves through the edge
                an = math.radians(100 + i * 22)
                u = (t * 1.8 + i * 0.37) % 1.0
                r0 = RD + 10 + u * 70
                c.drawLine(X0 + math.cos(an) * r0, Y0 + math.sin(an) * r0, X0 + math.cos(an) * (r0 + 18), Y0 + math.sin(an) * (r0 + 18),
                           P("#E0F2FE", duk * (1 - u) * 0.8, stroke=4))
        self.ui["cam"] = (0, 0, 1)
        self.ui["heat"] = heat

    # ------------------------------------------------------------------ set: the steering wheel
    def draw_wheel(self, c, t):
        T, s = self.T, self.tl.s
        cta = t < s("reveal")
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#151B38", "#0B1024", "#070B1F"]))
        c.drawOval(R(-260, 1010, 1600, 1100), lin_paint(0, 1010, 0, 1500, ["#1B2140", "#0B1024"]))   # the cockpit rim
        X0, Y0 = 540, 760
        b0, b1 = T["b0"], T["b1"]
        c.save()
        c.translate(X0, Y0)
        c.scale(1.3, 1.3)
        c.rotate(math.sin(t * 1.3) * 1.2)
        for sd in (-1, 1):                                                   # the grips
            c.drawRRect(rr(sd * 306 - 54, -196, 108, 410, 52), lin_paint(0, -196, 0, 214, ["#2A3042", "#141829"]))
            for i in range(7):
                c.drawRect(R(sd * 306 - 40, -150 + i * 46, 80, 5), P("#000000", 0.25))
        body = rr(-292, -176, 584, 340, 64)
        c.drawRRect(body, lin_paint(0, -176, 0, 164, ["#3A4158", "#232941"]))
        c.drawRRect(body, P("#5B6584", 1, stroke=4))
        c.drawRRect(rr(-132, -146, 264, 132, 14), P("#05070F"))                # the screen
        on = 0.0 if cta else prog(t, b0 - 0.3, b0)
        text(c, "N", 0, -48, 84, mix("#334155", "#F8FAFC", max(on, 0.25)), "Poppins-Black")
        for i in range(12):
            lit = (not cta) and (t * 9) % 14 > i
            col = ("#34D399", "#EF4444", "#60A5FA")[i // 4]
            c.drawCircle(-99 + i * 18, -130, 6, P(col if lit else "#1F2937"))
        n = len(BUTTONS)
        for i, (bx, by, br, col, kind) in enumerate(BUTTONS):
            if kind == "start":
                k = 1.0
            else:
                tb = lerp(b0, b1, (i - 1) / (n - 2))
                k = 0.0 if cta else e_back(prog(t, tb, tb + 0.14))
            if k <= 0:
                continue
            c.save()
            c.translate(bx, by)
            c.scale(k, k)
            if kind == "dial":
                c.drawCircle(0, 0, br, P("#0B0F1A"))
                c.drawCircle(0, 0, br - 6, lin_paint(0, -br, 0, br, ["#CBD5E1", "#64748B"]))
                for j in range(8):
                    an = j * math.pi / 4
                    c.drawLine(math.cos(an) * (br - 4), math.sin(an) * (br - 4), math.cos(an) * br, math.sin(an) * br, P("#F8FAFC", 1, stroke=3))
                c.drawLine(0, 0, math.cos(i * 1.3) * (br - 12), math.sin(i * 1.3) * (br - 12), P("#EF4444", 1, stroke=5))
            else:
                c.drawCircle(0, 0, br + 4, P("#0B0F1A"))
                c.drawCircle(0, 0, br, lin_paint(0, -br, 0, br, [shade(col, 0.25), col, shade(col, -0.3)]))
                c.drawCircle(-br * 0.3, -br * 0.35, br * 0.22, P("#FFFFFF", 0.5))
                if kind == "start":
                    pul = 0.5 + 0.5 * math.sin(t * 7)
                    add_glow(c, 0, 0, 80, GOOD, (0.5 + 0.4 * pul) if cta else 0.25)
                    tri = skia.Path()
                    tri.moveTo(-8, -12)
                    tri.lineTo(13, 0)
                    tri.lineTo(-8, 12)
                    tri.close()
                    c.drawPath(tri, P("#064E3B"))
                elif kind == "drink":
                    hot = prog(t, T["one"] - 0.1, T["one"] + 0.15)
                    add_glow(c, 0, 0, 90, "#38BDF8", 0.85 * hot * (0.6 + 0.4 * math.sin(t * 9)))
                    drop = skia.Path()
                    drop.moveTo(0, -14)
                    drop.cubicTo(14, 2, 10, 14, 0, 14)
                    drop.cubicTo(-10, 14, -14, 2, 0, -14)
                    c.drawPath(drop, P("#F8FAFC"))
            c.restore()
        for sd in (-1, 1):                                                   # gloves
            reach = (0.5 + 0.5 * math.sin(t * 5)) if (cta and sd > 0) else 0.0   # a thumb, hovering over START
            tx_, ty_ = sd * (262 - 10 * reach), (-56 - 30 * reach) if (sd > 0 and cta) else -42
            c.drawLine(sd * 300, 0, tx_, ty_, P(shade(PAINT, 0.12), 1, stroke=26))
            c.drawRRect(rr(sd * 306 - 56, -16, 112, 150, 46), lin_paint(0, -16, 0, 134, [shade(PAINT, 0.12), shade(PAINT, -0.28)]))
            for i in range(3):
                c.drawRect(R(sd * 306 - 44, 24 + i * 32, 88, 5), P("#000000", 0.2))
        if not cta and t >= T["one"] - 0.1:                                  # the drink goes up the tube
            tube = skia.Path()
            tube.moveTo(-240, 40)
            tube.cubicTo(-420, 20, -430, -300, -330, -900)
            c.drawPath(tube, P("#7DD3FC", 0.6 * prog(t, T["one"] - 0.1, T["one"] + 0.2), stroke=10))
            c.drawPath(tube, dash_paint("#F8FAFC", prog(t, T["one"], T["one"] + 0.2), 6, t * 6, 14, 30))
        c.restore()
        self.ui["cam"] = (0, 0, 1)

    def whip_backdrop(self, c, t, m):
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2238", "#2E3A58", "#161B33"]))

    # ------------------------------------------------------------------ labels and badges
    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, -180, 1.5)), x, y)

    def ui_track(self, c, t, tw):
        T, s, e = self.T, self.tl.s, self.tl.e
        ph = self.phase(tw)
        if ph == "kart":
            x0, y0 = self.at(-120, -190)
            self.label(x0, y0, x0 + 330, y0 - 190, "engine", T["land"] + 0.1, T["poof"] - 0.1, "#94A3B8", size=40)
            x1, y1 = self.at(60, -90)
            self.label(x1, y1, x1 + 130, y1 - 330, "car", T["poof"] + 0.35, s("break1") - 0.3, HILITE)
        elif ph == "wings":
            x0, y0 = self.at(262, -30)
            x1, y1 = self.at(-236, -150)
            self.label(x0, y0, x0 - 120, y0 - 330, "fwing", max(T["front"] - 0.05, T["foil1"] - 0.1), T["arrows"] - 0.05, "#CBD5E1")
            self.label(x1, y1, x1 + 150, y1 - 250, "rwing", max(T["rear"] - 0.05, T["foil1"]), T["arrows"] - 0.05, "#CBD5E1")
            self.foil(c, tw)
            self.chip(540, 420, "down", T["press"] + 0.05, s("break2") - 0.25, accent=HILITE, size=44)
            self.badge("check", T["road"], s("break2") - 0.15, x=880, y=560)
        elif ph == "ceiling":
            self.chip(540, 450, "theory", T["theory"] - 0.15, T["until"] - 0.2, accent=HILITE, size=48)
        elif ph == "bfire":
            n = int(round((200 if self.lang == "en" else 320) * clamp(self.ui.get("v", 2600.0) / 2000.0)))
            self.chip(540, 420, f"{n} {self.L['unit']}", T["until"] + 0.05, s("fix2") - 0.25, accent=WARN if tw >= T["fireon"] else "#E5E9F2", size=50)
            self.badge("alert", T["fireon"], s("fix2") - 0.2, x=880, y=560)
            self.red(T["fireon"], 2.0)
        elif ph == "tires":
            x0, y0 = self.at(RX, -92)
            self.label(x0, y0, x0 + 170, y0 - 300, "soft", T["softl"] - 0.05, T["wear"] - 0.1, "#EF4444")
            wr = 1 - 0.94 * prog(tw, s("break3") + 0.2, T["wear"] + 0.2)
            col = mix(WARN, GOOD, clamp(wr * 1.6 - 0.3))
            v2.gauge(c, 60, 372, [(self.L["gf"], wr, col), (self.L["gr"], wr * 0.9, col)], prog(tw, s("break3") + 0.05, s("break3") + 0.35), w=330)
            self.badge("alert", T["wear"], s("fix3") - 0.2, x=880, y=470)
            self.red(T["wear"], 1.8)
        elif ph == "pit":
            x0, y0 = self.at(RX, -46)
            self.label(x0, y0, x0 + 150, y0 - 420, "nut", T["nut"] - 0.1, T["train"] - 0.35, "#FBBF24", size=40)
            self.chip(540, 420, "crew", T["twenty"] - 0.1, T["guns"] - 0.15, accent=HILITE, size=48)
            x1, y1 = self.at(RX - 44, -46)
            self.label(x1, y1, x1 - 30, y1 - 330, "gun", T["guns"] - 0.1, T["up"] + 0.05, PAINT)
            x2, y2 = self.at(276, -30)
            self.label(x2, y2, x2 - 60, y2 - 330, "jack", T["up"] - 0.05, T["up"] + 0.8, "#FDE047")
            self.stopwatch(c, tw)
            self.badge("check", T["done"], s("break4") - 0.15, x=880, y=560)
        elif ph == "wall":
            self.badge("alert", T["hit"], T["cellcut"] - 0.08, x=880, y=470)
            self.red(T["hit"], 1.6)
        elif ph == "cell":
            x0, y0 = self.at(110, -66)
            self.label(x0, y0, x0 + 110, y0 - 330, "cell", T["survival"] - 0.05, T["halo"] - 0.2, HILITE)
            x1, y1 = self.at(30, -128)
            self.label(x1, y1, x1 - 170, y1 - 250, "halo", T["halo"], T["busdn"] + 0.25, "#D5DAE6")
            xb, yb = self.at(38, -420)
            self.chip(xb, yb - 30, "bus", T["busrest"] + 0.05, T["busup"] + 0.1, accent=HILITE, size=44)
            x2, y2 = self.at(226, -40)
            self.label(x2, y2, x2 - 60, y2 - 330, "nose", T["nose"] - 0.1, T["crunch"] + 0.5, PAINT)
            self.badge("check", T["dont"], s("cta") + 0.05, x=880, y=470)
        elif ph == "tag":
            pass

    def foil(self, c, tw):
        """A card with a wing section on it: the right way up it lifts, upside down it presses."""
        T = self.T
        p = self.span(T["upside"] - 0.35, T["foil1"], 0.25, 0.2)
        if p <= 0:
            return
        k = e_back(clamp(p))
        fl = e_io(prog(tw, T["upside"], T["upside"] + 0.4))
        c.save()
        c.translate(540, 560)
        c.scale(k, k)
        glass(c, -230, -150, 460, 300, r=30, a=clamp(p * 3))
        c.save()
        c.rotate(180 * fl)
        sec = skia.Path()
        sec.moveTo(-150, 10)
        sec.cubicTo(-140, -52, 20, -60, 150, 8)
        sec.cubicTo(60, 16, -80, 22, -150, 10)
        sec.close()
        c.drawPath(sec, lin_paint(0, -50, 0, 20, ["#E5E9F2", "#94A3B8"]))
        c.restore()
        col = mix(WARN, HILITE, fl)
        dy = lerp(-1, 1, fl)
        arrow(c, 0, dy * 52, 0, dy * 118, col, 12, clamp(p * 3), 24)
        c.restore()
        self.chip(540, 380, "down" if fl > 0.5 else "lift", T["upside"] - 0.2, T["foil1"], accent=col, size=40)

    def stopwatch(self, c, tw):
        T = self.T
        up, done = T["up"], T["done"]
        p = prog(tw, up - 0.12, up + 0.1) * (1 - prog(tw, self.tl.s("break4") - 0.4, self.tl.s("break4") - 0.2))
        if p <= 0:
            return
        val = 2.0 * prog(tw, up, done)
        fin = tw >= done
        c.save()
        c.translate(540, 420)
        c.scale(e_back(clamp(p)), e_back(clamp(p)))
        glass(c, -190, -62, 380, 124, r=62, a=clamp(p * 3))
        c.drawRRect(rr(-189, -61, 378, 122, 61), P(GOOD if fin else "#E5E9F2", 0.9, stroke=4))
        c.drawCircle(-124, 4, 34, P("#F8FAFC", 1, stroke=7))
        c.drawRect(R(-131, -46, 14, 12), P("#F8FAFC"))
        an = math.radians(-90 + 360 * val / 2.0)
        c.drawLine(-124, 4, -124 + math.cos(an) * 22, 4 + math.sin(an) * 22, P(GOOD if fin else HILITE, 1, stroke=6))
        text(c, f"{val:.2f}", 36, 30, 84, GOOD if fin else INK, "Poppins-Black")
        c.restore()

    def ui_top(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 420, "grip", T["slides"] - 0.1, s("fix1") - 0.25, accent=WARN, size=48)
        self.badge("alert", T["off"], s("fix1") - 0.2, x=880, y=560)
        self.red(T["off"], 1.8)

    def ui_brake(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.label(470, 660, 250, 410, "disc", T["discs"] - 0.05, T["pads"] - 0.1, "#94A3B8")
        self.label(676, 690, 840, 450, "pads", T["pads"], T["glowing"] - 0.3, PAINT)
        heat = self.ui.get("heat", 0.0)
        hot = prog(tw, T["glowing"] - 0.35, T["thousand"])
        deg = int(round((20 + 980 * hot) / 10.0)) * 10
        self.chip(540, 370, f"{deg:,}°" if self.lang == "en" else f"{deg}°", T["glowing"] - 0.3, T["ducts"] - 0.3,
                  accent=mix("#E5E9F2", "#FF5A1F", heat), size=58)
        self.label(150, 700, 250, 430, "duct", T["ducts"] - 0.05, s("break3") - 0.3, "#7DD3FC")
        self.badge("check", T["cool"], s("break3") - 0.15, x=880, y=430)

    def ui_wheel(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("reveal"):
            self.label(852, 601, 800, 440, "start", T["start"] - 0.2, s("reveal") - 0.3, GOOD)
            return
        b0, b1 = T["b0"], T["b1"]
        n = 1 + int(round((len(BUTTONS) - 1) * prog(tw, b0, b1)))
        txt = f"{n} {self.L['btn']}"
        self.chip(540, 400, txt, b0 + 0.12, T["one"] - 0.15, accent=HILITE, size=50)
        self.label(228, 812, 250, 1130, "drink", T["one"] + 0.1, T["s1"] - 0.5, "#38BDF8", size=40)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (0.1, sfx.pop(61), -6), (T["land"] - 0.5, sfx.whoosh(0.5, False, 62), -8),
              (T["land"], sfx.thud(0.45, 63), -4), (T["land"] + 0.02, sfx.clank(240, 0.4, 64), -8),
              (T["land"] + 0.25, gun_snd(0.2, 65), -9), (T["land"] + 0.43, gun_snd(0.2, 66), -9), (T["land"] + 0.7, rev(0.9, 60, 110, 67), -12),
              (T["poof"] - 0.05, sfx.whoosh(0.4, True, 68), -6), (T["poof"], sfx.sparkle(0.8, 12, 69), -6), (T["poof"] + 0.1, sfx.chime(), -8),
              (T["race"] - 0.05, rev(0.9, 110, 460, 70), -8)]
        ev += [(s("break1") - 0.1, sfx.whoosh(0.4, True, 73), -5), (s("break1"), rev(max(0.8, T["slide"] - s("break1")), 300, 520, 74, 1.0), -13),
               (T["slide"], screech(max(0.7, T["stop"] - T["slide"] - 0.1), 75), -8), (T["off"], rumble(0.7, 76), -7),
               (T["off"] + 0.05, sfx.alarm(3, 820), -11), (T["stop"], sfx.thud(0.3, 77), -3), (T["stop"] + 0.35, sfx.womp(), -9)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 78), -5), (s("fix1"), rev(1.2, 260, 330, 79, 1.0), -17),
               (T["wings"] - 0.15, sfx.pop(80), -5), (T["wings"] - 0.02, sfx.pop(81), -6), (T["upside"] - 0.3, sfx.pop(82), -8),
               (T["upside"], sfx.whoosh(0.4, True, 83), -8), (T["front"], sfx.tick(), -6), (T["rear"], sfx.tick(), -6),
               (T["arrows"], sfx.buzz(0.3), -14), (T["press"] - 0.25, sfx.whoosh(0.9, True, 84), -9), (T["press"], sfx.thunk(85), -5),
               (T["road"], sfx.chime(), -6)]
        ev += [(s("break2") - 0.1, sfx.whoosh(0.4, True, 86), -5), (s("break2"), rev(max(1.0, T["until"] - s("break2")), 300, 380, 87, 1.0), -15),
               (T["theory"] - 0.15, sfx.pop(88), -6), (T["until"] - 0.12, sfx.whoosh(0.4, False, 89), -5),
               (T["until"], rev(max(0.5, T["brake"] - T["until"]), 420, 640, 90, 1.0), -12),
               (T["brake"], screech(max(0.7, T["fireon"] - T["brake"]), 91), -10), (T["fireon"], sfx.sizzle(0.9, 92), -6),
               (T["fireon"] + 0.05, boom(0.8, 93), -9), (T["fireon"] + 0.12, sfx.alarm(3, 820), -11), (T["fire"] + 0.4, sfx.womp(), -9)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, True, 94), -4), (s("fix2") + 0.05, sfx.whirr(1.2, 200, 240, 95), -15),
               (T["discs"] - 0.3, sfx.pop(96), -5), (T["discs"], sfx.clank(520, 0.3, 97), -9), (T["pads"] - 0.3, sfx.pop(98), -5),
               (T["pads"], sfx.thunk(99), -6), (T["glowing"] - 0.35, screech(0.7, 100), -15), (T["glowing"] - 0.3, sfx.riser(0.9, 101), -12),
               (T["glowing"], sfx.sizzle(0.8, 102), -9), (T["thousand"], sfx.ding(), -6), (T["ducts"] - 0.3, sfx.whoosh(0.5, True, 103), -6),
               (T["ducts"], sfx.hiss(0.9, 104), -10), (T["cool"] + 0.1, sfx.chime(), -6)]
        ev += [(s("break3") - 0.1, sfx.whoosh(0.4, False, 105), -5), (s("break3"), rev(max(1.0, T["wear"] - s("break3")), 300, 360, 106, 1.0), -15),
               (T["softl"], sfx.pop(107), -7), (T["sticky"], sfx.tick(), -8), (T["wear"], screech(0.6, 108), -10), (T["wear"] + 0.05, sfx.power_down(0.9, 109), -8),
               (T["wear"] + 0.1, sfx.alarm(3, 820), -11), (T["finish"] + 0.3, sfx.womp(), -9)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, True, 110), -4), (s("fix3"), rev(max(0.5, T["nut"] - 0.3 - s("fix3")), 300, 120, 111, 1.0), -13),
               (T["nut"] - 0.3, screech(0.25, 112), -14), (T["nut"], sfx.ding(), -8), (T["train"] - 0.3, sfx.whoosh(0.5, True, 113), -8)]
        ev += [(T["train"] - 0.1 + i * 0.07, sfx.tap(i), -11) for i in range(8)]
        ev += [(T["twenty"], sfx.pop(114), -6), (T["guns"] - 0.1, gun_snd(0.18, 115), -9), (T["up"] - 0.15, sfx.clank(300, 0.25, 116), -7),
               (T["up"], sfx.tick(), -6), (T["g1"], gun_snd(0.3, 117), -5), (T["g1"] + 0.05, gun_snd(0.3, 118), -8),
               (lerp(T["g1"], T["g2"], 0.4), sfx.thunk(119), -8), (lerp(T["g1"], T["g2"], 0.75), sfx.thunk(120), -8),
               (T["g2"], gun_snd(0.3, 121), -5), (T["g2"] + 0.05, gun_snd(0.3, 122), -8), (T["done"] - 0.12, sfx.thud(0.25, 123), -5),
               (T["done"], sfx.ding(), -4), (T["done"] + 0.12, rev(0.7, 180, 640, 124), -8), (T["done"] + 0.15, screech(0.35, 125), -14)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 126), -5), (s("break4"), rev(max(0.8, T["scr"] - s("break4")), 420, 700, 127, 1.0), -13),
               (T["scr"], screech(0.68, 128), -8), (T["hit"], crunch(0.5, 129), -2), (T["hit"], boom(0.7, 130), -6),
               (T["hit"] + 0.12, sfx.alarm(3, 820), -12), (T["hit"] + 0.35, sfx.clank(260, 0.5, 131), -9)]
        ev += [(T["cellcut"], sfx.whoosh(0.4, True, 132), -5), (T["survival"] - 0.2, sfx.charge_up(0.5), -10), (T["survival"] + 0.1, sfx.pop(133), -7),
               (T["halo"] - 0.15, sfx.clank(900, 0.4, 134), -8), (T["halo"], sfx.lock_click(135), -6),
               (T["busdn"], sfx.whirr(max(0.4, T["busrest"] - T["busdn"]), 220, 120, 136), -12), (T["busrest"], sfx.thud(0.4, 137), -4),
               (T["busrest"] + 0.05, sfx.creak(0.5, 138), -9), (T["busrest"] + 0.3, sfx.beep(520, 0.12), -12), (T["busrest"] + 0.48, sfx.beep(520, 0.12), -12),
               (T["busup"] - 0.05, sfx.whoosh(0.3, True, 139), -14), (T["crunch"] - 0.45, rev(0.45, 300, 520, 140, 1.0), -12),
               (T["crunch"], crunch(0.4, 141), -3), (T["crunch"] + 0.02, sfx.thud(0.3, 142), -6), (T["dont"], sfx.pop(143), -6),
               (T["dont"] + 0.1, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(144), 0), (s("cta") + 0.05, sfx.whoosh(0.4, False, 145), -7), (T["start"], sfx.beep(660, 0.1), -12),
               (T["start"] + 0.25, sfx.beep(660, 0.1), -12), (T["follow"] - 0.15, sfx.pop(146), -4)]
        ev += [(s("reveal") - 0.1, sfx.whoosh(0.4, True, 147), -6), (T["cover"] - 0.15, sfx.hiss(0.5, 148), -8)]
        ev += [(lerp(T["st0"], T["st1"], i / 12), sfx.pop(150 + i), -7 - (i % 3)) for i in range(12)]
        ev += [(T["wheelcut"], sfx.whoosh(0.4, False, 163), -6)]
        nb = int(max(6, min(21, (T["b1"] - T["b0"]) / 0.055)))
        ev += [(lerp(T["b0"], T["b1"], i / nb), sfx.beep(700 + i * 45, 0.05), -13) for i in range(nb)]
        ev += [(T["b1"] + 0.05, sfx.ding(), -8), (T["one"], sfx.pop(164), -5), (T["drink"], sfx.beep(520, 0.1), -10), (T["drink"] + 0.16, sfx.beep(420, 0.12), -10)]
        ev += [(T["s1"] - 0.35, sfx.whoosh(0.4, True, 165), -6), (T["s1"], sfx.pop(166), -3), (T["s2"], sfx.pop(167), -3), (T["s3"], sfx.pop(168), -3),
               (T["s2"] + 0.1, rev(0.6, 160, 420, 169), -14)]
        ev += [(T["cong2"], sfx.pop(170), -2), (T["cong2"], sfx.sparkle(1.0, 14, 171), -4), (T["cong2"] + 0.2, rev(1.0, 160, 520, 172), -13),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 173), -6), (T["winner"], sfx.pop(174), -5), (T["nodrink"] - 0.2, sfx.tick(), -8),
               (T["spray"] - 0.12, sfx.pop(175), -2), (T["spray"], sfx.hiss(1.1, 176), -6), (T["spray"] + 0.1, sfx.sizzle(0.8, 177), -10),
               (T["purpose"] + 0.45, sfx.womp(), -3)]
        return ev


NAME = "racecar"
EPISODE = RaceCar
