"""Episode 23 - A desalination plant.  v2 look: dusk, night and under the sea, seven sets with whip cuts.

Sets: pot (a camping pot of seawater on a stove at the beach, its steam caught in a glass; then the pot grows to
city size on a burning mountain of fuel), membrane (close-up board: a piston pushes seawater through a filter so
tight that the salt stays behind; pressure gauge), intake (under the sea: sand, seaweed and jellyfish sucked into
the intake, the filter clogs; a screen goes over it), plant (inside: sand filters, the high-pressure pumps, the
membrane racks, a glass that costs a fortune, the pressure exchanger), outfall (under the sea: the salty water comes
out by the shore and the fish are unhappy; a long pipe with nozzles far out), land (the plant at the coast, a pipe
inland to a kitchen tap, the wide stat shot), fish (the tag: in English a fish that lost a video game, in Arabic a
fish turning into fesikh, Egypt's salted fish).
Ground sets: the floor or the seabed is y = 0, up is negative.
"""
from v2_base import *  # noqa: F401,F403

SEA_C, FRESH, BRINE, SALT_C = "#1E5AA8", "#7DD3FC", "#F59E0B", "#F8FAFC"
PIPE_C, SAND_C, COPPER = "#7C8499", "#C9A46A", "#C17A3A"
SKINS = ("#E8B48A", "#C68B5E", "#F1C9A5", "#8D5A3B", "#E0A47A")
TUBE = [(40, -226), (40, -300), (190, -300), (236, -254), (236, -150)]      # the pot's lid tube (set "pot")


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
    total = sum(s[2] for s in segs)
    d = (u % 1.0) * total
    for (a, b, ln) in segs:
        if d <= ln:
            k = d / ln if ln else 0
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        d -= ln
    return pts[-1]


def pipe(c, pts, col=PIPE_C, w=22, a=1.0):
    if a <= 0:
        return
    path = skia.Path()
    path.moveTo(*pts[0])
    for p in pts[1:]:
        path.lineTo(*p)
    c.drawPath(path, P("#1B2236", a, stroke=w + 8))
    c.drawPath(path, P(col, a, stroke=w))
    c.drawPath(path, P("#FFFFFF", 0.18 * a, stroke=w * 0.3))


def flow(c, pts, t, k, n=10, speed=0.45, col=FRESH, r=6, salt=0.0, seed=1):
    """Drops running along a pipe. salt > 0: that share of them are white salt grains."""
    if k <= 0:
        return
    rng = random.Random(seed)
    for i in range(n):
        u = (t * speed + i / n + rng.uniform(0, 0.03)) % 1.0
        x, y = along(pts, u)
        is_salt = rng.random() < salt
        c.drawCircle(x, y, r * (0.75 if is_salt else 1.0), P(SALT_C if is_salt else col, 0.95 * k))


def cup(c, x, y, w=62, h=92, fill=0.0, col=FRESH, a=1.0):
    """A drinking glass standing on y, centred on x; fill 0..1."""
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(x - w / 2, y - h)
    p.lineTo(x + w / 2, y - h)
    p.lineTo(x + w * 0.38, y)
    p.lineTo(x - w * 0.38, y)
    p.close()
    c.drawPath(p, P("#E0F2FE", 0.16 * a))
    if fill > 0:
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        c.drawRect(R(x - w, y - h * fill, 2 * w, h * fill), P(col, 0.85 * a))
        c.restore()
    c.drawPath(p, P("#FFFFFF", 0.85 * a, stroke=3))
    c.drawLine(x - w * 0.3, y - h * 0.85, x - w * 0.24, y - h * 0.2, P("#FFFFFF", 0.45 * a, stroke=3))


def pot(c, t, boil=0.0, steam=0.0, fill=0.0, tube=1.0):
    """A camping pot of seawater on a little stove; a copper tube from the lid drips into a glass. Ground y = 0."""
    for sd in (-1, 1):                                                              # the stove
        c.drawLine(sd * 80, 0, sd * 48, -48, P("#475569", 1, stroke=10))
    c.drawRRect(rr(-66, -56, 132, 12, 5), P("#64748B"))
    if boil > 0:
        add_glow(c, 0, -64, 130, "#FF8A3D", 0.55 * boil)
        for i, (fx_, ln) in enumerate(((-26, 50), (0, 64), (26, 46))):
            v2.flame(c, fx_, -48, 34, ln, t + i * 0.37, boil, seed=i + 1, ang=-90)
    c.drawRRect(rr(-106, -214, 212, 154, 28), lin_paint(-106, 0, 106, 0, ["#475569", "#CBD5E1", "#94A3B8", "#334155"]))
    inner = rr(-92, -196, 184, 124, 20)
    c.drawRRect(inner, P("#0B1220"))
    c.save()
    c.clipRRect(inner, skia.ClipOp.kIntersect, True)
    vrect(c, -92, -172, 184, 110, [SEA_C, "#12336B"])
    path = skia.Path()
    path.moveTo(-92, -172)
    for xx in range(-92, 94, 12):
        path.lineTo(xx, -172 + math.sin(xx * 0.08 + t * (3 + 6 * boil)) * (2 + 4 * boil))
    c.drawPath(path, P("#BFE3FF", 0.7, stroke=3))
    rng = random.Random(3)
    for _ in range(14):                                                             # salt in the water
        c.drawRect(R(rng.uniform(-80, 76), rng.uniform(-160, -82), 5, 5), P(SALT_C, 0.55))
    if boil > 0:
        for i in range(16):                                                         # boiling
            rng = random.Random(40 + i)
            u = (t * rng.uniform(0.7, 1.2) + rng.random()) % 1.0
            bx = rng.uniform(-78, 78) + math.sin(t * 5 + i) * 4
            c.drawCircle(bx, lerp(-80, -170, u), lerp(3, 8, u), P("#E6FAFF", 0.8 * boil, stroke=2))
    c.restore()
    c.drawRRect(rr(-122, -190, 16, 12, 5), P("#334155"))                            # handles
    c.drawRRect(rr(106, -190, 16, 12, 5), P("#334155"))
    c.drawRRect(rr(-114, -228, 228, 18, 9), lin_paint(-114, 0, 114, 0, ["#64748B", "#E2E8F0", "#94A3B8"]))   # lid
    c.drawCircle(-52, -236, 10, P("#334155"))
    if boil > 0:                                                                    # steam escaping under the lid
        for i in range(5):
            u = (t * 0.6 + i / 5) % 1.0
            puff(c, -90 + i * 40 + math.sin(t + i) * 8, -236 - u * 120, 16 + 30 * u, "#E5E7EB",
                 0.35 * boil * (1 - u) * (1 - 0.6 * steam))
    if tube <= 0:
        return
    if tube < 1:
        c.saveLayerAlpha(None, int(255 * tube))
    path = skia.Path()
    path.moveTo(*TUBE[0])
    for p_ in TUBE[1:]:
        path.lineTo(*p_)
    c.drawPath(path, P("#5B3A1E", 1, stroke=20))
    c.drawPath(path, P(COPPER, 1, stroke=14))
    c.drawPath(path, P("#FFD9A8", 0.35, stroke=4))
    if steam > 0:
        for i in range(7):                                                          # steam travelling down the tube
            x, y = along(TUBE, (t * 0.55 + i / 7) % 1.0)
            c.drawCircle(x, y, 6, P("#FFFFFF", 0.75 * steam))
        for i in range(3):                                                          # drops into the glass
            u = (t * 1.6 + i / 3) % 1.0
            c.drawCircle(236, lerp(-146, -30, u * u), 5, P(FRESH, 0.95 * steam))
    cup(c, 236, 0, 62, 92, fill)
    if tube < 1:
        c.restore()


def coal_heap(c, x, w, h, t, burn=0.0, seed=4):
    """A heap of coal on y = 0 from x to x + w, h tall; burn 0..1 lights glowing embers along it."""
    if h <= 2:
        return
    rng = random.Random(seed)
    n = 16
    path = skia.Path()
    path.moveTo(x, 0)
    for i in range(n + 1):
        u = i / n
        path.lineTo(x + w * u, -h * (math.sin(math.pi * u) ** 0.9) * (0.92 + 0.08 * rng.random()))
    path.close()
    c.drawPath(path, lin_paint(0, -h, 0, 0, ["#3F3F46", "#18181B"]))
    for i in range(46):
        u = rng.uniform(0.04, 0.96)
        top = -h * (math.sin(math.pi * u) ** 0.9)
        yy = top * rng.uniform(0.08, 0.95)
        xx = x + w * u
        r_ = rng.uniform(14, 30) * (h / 800) ** 0.5
        c.drawCircle(xx, yy, r_, P("#27272A"))
        c.drawCircle(xx - r_ * 0.3, yy - r_ * 0.3, r_ * 0.35, P("#71717A", 0.45))
        if burn > 0 and rng.random() < 0.45:
            add_glow(c, xx, yy, r_ * 2.4, "#FF6A2B", 0.55 * burn * (0.6 + 0.4 * math.sin(t * 6 + xx)))


def dial(c, x, y, r, k, t, warn=0.7):
    """Round pressure gauge, needle at k (0..1)."""
    c.drawCircle(x, y, r + 12, P("#475569"))
    c.drawCircle(x, y, r, P("#F8FAFC"))
    a0, a1 = 140.0, 400.0
    arc = skia.Path()
    arc.addArc(R(x - r * 0.84, y - r * 0.84, r * 1.68, r * 1.68), lerp(a0, a1, warn), (a1 - a0) * (1 - warn))
    c.drawPath(arc, P(WARN, 0.85, stroke=r * 0.12))
    for i in range(11):
        an = math.radians(lerp(a0, a1, i / 10))
        c.drawLine(x + math.cos(an) * r * 0.66, y + math.sin(an) * r * 0.66, x + math.cos(an) * r * 0.78,
                   y + math.sin(an) * r * 0.78, P("#334155", 1, stroke=4))
    an = math.radians(lerp(a0, a1, clamp(k + math.sin(t * 23) * 0.012 * k)))
    c.drawLine(x, y, x + math.cos(an) * r * 0.74, y + math.sin(an) * r * 0.74, P(WARN, 1, stroke=7))
    c.drawCircle(x, y, r * 0.12, P("#0F172A"))


def jelly(c, x, y, s, t, a=1.0, seed=0, col="#F9A8D4"):
    """A jellyfish: pulsing bell and wavy tentacles."""
    if a <= 0:
        return
    pulse = 1 + 0.1 * math.sin(t * 4 + seed)
    c.save()
    c.translate(x, y)
    c.scale(s * pulse, s / pulse)
    for i in range(5):
        tx = -22 + i * 11
        path = skia.Path()
        path.moveTo(tx, 0)
        for k in range(1, 7):
            path.lineTo(tx + math.sin(t * 3 + k + i + seed) * 5, k * 12)
        c.drawPath(path, P(col, 0.75 * a, stroke=3))
    bell = skia.Path()
    bell.addArc(R(-32, -30, 64, 60), 180, 180)
    bell.close()
    c.drawPath(bell, P(col, 0.6 * a))
    c.drawPath(bell, P("#FFFFFF", 0.65 * a, stroke=2))
    add_glow(c, 0, -8, 40, col, 0.25 * a)
    c.restore()


def weed(c, x, y, s, t, rot=0.0, a=1.0, seed=0):
    """A strand of seaweed, base at (x, y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(s, s)
    path = skia.Path()
    path.moveTo(0, 0)
    for k in range(1, 9):
        path.lineTo(math.sin(t * 2 + k * 0.8 + seed) * 9, -k * 11)
    c.drawPath(path, P("#16A34A", 0.95 * a, stroke=8))
    c.drawPath(path, P("#86EFAC", 0.5 * a, stroke=2))
    c.restore()


def fish(c, x, y, s=1.0, face=1, col="#FB923C", mood=1.0, t=0.0, shades=False, salt=0.0, dead=0.0, red=0.0, a=1.0,
         seed=0):
    """A round cartoon fish, nose at the `face` side. mood 1 happy .. -1 angry. salt 0..1 greys it and adds
    crystals; dead > 0.5 crosses the eyes; red 0..1 flushes it."""
    if a <= 0:
        return
    body = mix(mix(col, "#EF4444", 0.8 * red), "#A8A29E", 0.85 * salt)
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    wag = math.sin(t * 7 + seed) * 6 * (1 - dead)
    tail = skia.Path()
    tail.moveTo(-30, 0)
    tail.lineTo(-58, -20 + wag)
    tail.lineTo(-50, 0)
    tail.lineTo(-58, 20 + wag)
    tail.close()
    c.drawPath(tail, P(mix(body, "#000000", 0.18), a))
    c.drawOval(R(-40, -28, 80, 56), lin_paint(0, -28, 0, 28, [(mix(body, "#FFFFFF", 0.25), a), (body, a),
                                                             (mix(body, "#000000", 0.25), a)]))
    fin = skia.Path()
    fin.moveTo(-12, -25)
    fin.lineTo(4, -40)
    fin.lineTo(14, -24)
    fin.close()
    c.drawPath(fin, P(mix(body, "#000000", 0.18), a))
    ex, ey = 17, -8
    c.drawCircle(ex, ey, 9, P("#FFFFFF", a))
    if dead > 0.5:
        for sd in (-1, 1):
            c.drawLine(ex - 6, ey - 6 * sd, ex + 6, ey + 6 * sd, P("#111827", a, stroke=3))
    else:
        c.drawCircle(ex + 2, ey + 1, 4.5, P("#111827", a))
    if mood < 0:
        k = -mood
        c.drawLine(ex - 11, ey - 13 - 3 * k, ex + 10, ey - 13 + 5 * k, P("#111827", a * k, stroke=4))
    m = skia.Path()
    m.moveTo(24, 9)
    m.quadTo(29, 9 + 7 * mood, 34, 9)
    c.drawPath(m, P("#111827", a, stroke=3))
    if shades:
        c.drawRRect(rr(ex - 13, ey - 7, 27, 12, 4), P("#111827", a))
        c.drawLine(ex - 13, ey - 3, -4, ey - 6, P("#111827", a, stroke=3))
    if salt > 0:
        rng = random.Random(seed + 9)
        for _ in range(int(40 * salt)):
            c.drawRect(R(rng.uniform(-36, 30), rng.uniform(-24, 18), 4, 4), P("#FFFFFF", 0.9 * a))
    c.restore()


def sand_tank(c, x, w, h, t, k=0.0):
    """A sand filter: tall tank, left edge x, on y = 0, cut open: water above sand above gravel; k > 0 trickles."""
    c.drawRRect(rr(x, -h, w, h, w * 0.4), lin_paint(x, 0, x + w, 0, ["#475569", "#94A3B8", "#64748B"]))
    inner = rr(x + 12, -h + 14, w - 24, h - 26, w * 0.3)
    c.save()
    c.clipRRect(inner, skia.ClipOp.kIntersect, True)
    vrect(c, x, -h, w, h, ["#1D4E89", "#163A66"])
    c.drawRect(R(x, -h * 0.52, w, h * 0.36), P(SAND_C))
    rng = random.Random(int(x))
    for _ in range(40):
        c.drawCircle(rng.uniform(x, x + w), rng.uniform(-h * 0.52, -h * 0.16), 2.2, P("#8A6A3E", 0.8))
    c.drawRect(R(x, -h * 0.16, w, h * 0.16), P("#64748B"))
    for _ in range(14):
        c.drawCircle(rng.uniform(x, x + w), rng.uniform(-h * 0.15, -8), rng.uniform(5, 9), P("#94A3B8"))
    if k > 0:
        for i in range(14):
            u = (t * 0.5 + i / 14) % 1.0
            xx = x + 20 + (i * 37) % max(1, int(w - 40))
            c.drawCircle(xx, lerp(-h * 0.9, -20, u), 4, P("#BAE6FD", 0.85 * k))
    c.restore()


def pump(c, x, t, on=0.0):
    """A high-pressure pump: blue motor driving a grey pump casing, on y = 0, centred on x."""
    dx = math.sin(t * 61 + x) * 1.6 * on
    c.save()
    c.translate(dx, 0)
    box(c, x - 84, -20, 168, 20, "#334155", r=4)
    vrect(c, x - 80, -126, 100, 104, ["#60A5FA", "#2563EB", "#1E3A8A"], r=14)
    for i in range(6):
        c.drawLine(x - 70 + i * 16, -118, x - 70 + i * 16, -30, P("#1E3A8A", 0.8, stroke=4))
    c.drawCircle(x + 50, -72, 44, P("#94A3B8"))
    c.drawCircle(x + 50, -72, 30, P("#64748B"))
    an = t * 24 * on
    for k in range(3):
        a_ = an + k * 2.094
        c.drawLine(x + 50, -72, x + 50 + math.cos(a_) * 26, -72 + math.sin(a_) * 26, P("#E2E8F0", 0.9, stroke=6))
    if on > 0.5:
        add_glow(c, x - 30, -74, 90, "#93C5FD", 0.25 * on)
    c.restore()


RACK_Y = (-470, -380, -290)


def vessels(c, t, k=1.0):
    """The membrane racks: three long white pressure vessels between x = -20 and 540."""
    c.drawRect(R(-44, -520, 14, 520), P("#475569"))
    c.drawRect(R(548, -520, 14, 520), P("#475569"))
    for y in RACK_Y:
        vrect(c, -20, y - 30, 560, 60, ["#F8FAFC", "#CBD5E1", "#94A3B8"], r=30)
        c.drawRRect(rr(-26, y - 34, 26, 68, 10), P("#64748B"))
        c.drawRRect(rr(534, y - 34, 26, 68, 10), P("#64748B"))
        for j in range(9):
            c.drawLine(30 + j * 56, y - 22, 30 + j * 56, y + 22, P("#94A3B8", 0.6, stroke=2))


def exchanger(c, x, y, w, h, t, k, ph):
    """Pressure exchanger, cut open: blue seawater on the left, orange salty water on the right; the free piston sits
    at ph (0..1) and moves as the leaving salty water pushes the next batch."""
    if k <= 0:
        return
    s_ = e_back(clamp(k))
    c.save()
    c.translate(x + w / 2, y + h / 2)
    c.scale(s_, s_)
    c.translate(-(x + w / 2), -(y + h / 2))
    c.drawRRect(rr(x - 14, y - 14, w + 28, h + 28, h / 2 + 14), lin_paint(0, y - 14, 0, y + h + 14, ["#94A3B8", "#334155"]))
    inner = rr(x, y, w, h, h / 2)
    c.save()
    c.clipRRect(inner, skia.ClipOp.kIntersect, True)
    bx = x + w * (0.2 + 0.6 * ph)
    c.drawRect(R(x, y, bx - x, h), P(SEA_C))
    c.drawRect(R(bx, y, x + w - bx, h), P(BRINE))
    rng = random.Random(8)
    for _ in range(18):
        sx = rng.uniform(0, 1)
        c.drawRect(R(bx + sx * (x + w - bx) - 3, rng.uniform(y + 8, y + h - 8), 6, 6), P(SALT_C, 0.8))
    c.restore()
    c.drawRRect(rr(bx - 9, y + 3, 18, h - 6, 5), P("#E2E8F0"))
    c.restore()


def house(c, x, t, tap=0.0, fill=0.0):
    """A small house cut open at the kitchen; x = left edge, on y = 0. tap 0..1 opens the tap over a glass."""
    w, h = 380, 300
    c.drawRect(R(x, -h, w, h), P("#E7D9C4"))
    c.drawRect(R(x + 14, -h + 14, w - 28, h - 14), lin_paint(0, -h, 0, 0, ["#FDF2D8", "#F2DFB8"]))
    roof = skia.Path()
    roof.moveTo(x - 26, -h)
    roof.lineTo(x + w / 2, -h - 140)
    roof.lineTo(x + w + 26, -h)
    roof.close()
    c.drawPath(roof, lin_paint(0, -h - 140, 0, -h, ["#B45309", "#7C2D12"]))
    c.drawRRect(rr(x + 40, -250, 110, 90, 6), P("#1E293B"))                       # window
    c.drawRect(R(x + 92, -250, 6, 90), P("#E7D9C4"))
    add_glow(c, x + 270, -270, 120, "#FFE7A3", 0.35)                               # lamp
    c.drawRect(R(x + 266, -286, 8, 26), P("#57534E"))
    c.drawCircle(x + 270, -256, 14, P("#FDE68A"))
    c.drawRect(R(x + 30, -104, w - 60, 104), P("#A16207"))                          # the counter
    c.drawRect(R(x + 30, -112, w - 60, 14), P("#E5E7EB"))
    for i in range(3):
        c.drawRect(R(x + 46 + i * 104, -88, 90, 76), P("#854D0E"))
        c.drawCircle(x + 91 + i * 104, -50, 4, P("#FDE68A"))
    tx = x + 240                                                                    # the tap
    tp = skia.Path()
    tp.moveTo(tx + 34, -112)
    tp.lineTo(tx + 34, -196)
    tp.quadTo(tx + 34, -214, tx + 14, -214)
    tp.lineTo(tx, -214)
    tp.lineTo(tx, -198)
    c.drawPath(tp, P("#94A3B8", 1, stroke=12))
    c.drawPath(tp, P("#E2E8F0", 0.6, stroke=4))
    c.drawRRect(rr(tx + 44, -150, 26, 8, 4), P("#64748B"))
    if tap > 0:
        c.drawRect(R(tx - 5, -196, 10, 84 - 80 * fill), P(FRESH, 0.85 * tap))
        add_glow(c, tx, -150, 40, FRESH, 0.3 * tap)
    cup(c, tx, -112, 54, 80, fill)


def plant_bld(c, x, t):
    """The desalination plant at the coast: a long hall and white tanks; x = left edge, on y = 0."""
    box(c, x, -250, 560, 250, "#CBD5E1", r=10)
    c.drawRect(R(x, -214, 560, 20), P("#2563EB"))
    for i in range(8):
        for j in range(2):
            c.drawRRect(rr(x + 26 + i * 66, -170 + j * 70, 44, 40, 4), P("#FDE68A" if (i + j) % 3 else "#334155", 0.9))
    for i in range(3):
        cyl(c, x + 600 + i * 130, -210, 110, 210, "#E2E8F0", r=14)
        c.drawRect(R(x + 600 + i * 130, -150, 110, 10), P("#38BDF8", 0.8))
    pipe(c, [(x + 980, -24), (x + 1150, -24)], PIPE_C, 26)


def boil_snd(d=2.0, seed=70):
    n = int(d * sfx.SR)
    rng = sfx._rng(seed)
    x = sfx._bp(rng.standard_normal(n), 300, 2600)
    am = np.zeros(n)
    for _ in range(int(d * 26)):
        i = rng.integers(0, n - 400)
        am[i:i + 400] += np.hanning(400)
    return sfx._norm(x * (0.25 + am) * sfx._ar(n, 0.15, 0.4), 0.7)


def water_snd(d=0.7, seed=60):
    n = int(d * sfx.SR)
    x = sfx._bp(sfx._rng(seed).standard_normal(n), 400, 5200)
    return sfx._norm(x * sfx._env(n, 0.004, d * 0.3), 0.8)


def flow_snd(d=1.6, seed=61):
    n = int(d * sfx.SR)
    x = sfx._lp(sfx._rng(seed).standard_normal(n), 900) + 0.3 * sfx._bp(sfx._rng(seed + 1).standard_normal(n), 800, 4000)
    return sfx._norm(x * sfx._ar(n, d * 0.3, d * 0.4), 0.8)


def coins_snd(seed=80):
    rng = sfx._rng(seed)
    n = int(0.9 * sfx.SR)
    out = np.zeros(n)
    for k in range(6):
        b = sfx.bell(rng.uniform(2400, 3600), 0.3, 0.6)
        i = int(k * 0.11 * sfx.SR)
        m = min(len(b), n - i)
        out[i:i + m] += b[:m]
    return sfx._norm(out, 0.7)


# ====================================================================================== the episode
class Desal(EpisodeV2):
    BUILD_NO = 23
    FIRST_SET = "pot"
    CLEAR = "#070B1F"
    TITLE = {"en": "DESALINATION PLANT", "ar_sa": "محطة تحلية"}
    EMPH = {"en": ["CONGRATS", "BOIL", "STEAM", "DESALINATION", "PLANT", "CITY", "MOUNTAIN", "FUEL", "PUSH", "FILTER",
                   "SALT", "PRESSURE", "THOUSAND", "SAND", "SEAWEED", "JELLYFISH", "CLOG", "SCREENS", "CLEAN",
                   "MEMBRANES", "PUMPS", "POWER", "FORTUNE", "EXCHANGER", "SIXTY", "HALF", "TWICE", "FISH", "FAR",
                   "NOZZLES", "MIXES", "FOLLOW", "MILES", "KITCHEN", "TAP", "ONE", "MILLION", "ZERO", "YOURSELF",
                   "GAMER", "LOST"],
            "ar_sa": ["مبروك", "غليت", "البخار", "تحلية", "مدينة", "جبل", "وقود", "تزق", "فلتر", "الملح", "بضغط", "ستمية",
                      "رمل", "وطحالب", "وقناديل", "وبيسدوا", "شبك", "نضيفة", "للأغشية", "الطلمبات", "كهربا", "ثروة",
                      "مبادل", "ستين", "نص", "الضعف", "والسمك", "بعيد", "فتحات", "فتختلط", "تابعني", "الكيلومترات",
                      "حنفية", "مطبخك", "واحد", "مليون", "وصفر", "بإيدك", "فسيخ"]}
    KEYS = {"ar_sa": {                                  # Egyptian narrator (files keep the _ar_sa name)
        ("hook", "BOIL"): "غليت", ("hook", "SEAWATER"): "البحر", ("hook", "CATCH"): "ولميت", ("hook", "STEAM"): "البخار",
        ("hook", "CONGRATS"): "مبروك", ("hook", "DESALINATION"): "تحلية",
        ("break1", "CITY"): "مدينة", ("break1", "BURNS"): "هتحرق", ("break1", "MOUNTAIN"): "جبل", ("break1", "FUEL"): "وقود",
        ("break1", "DAY"): "يوم",
        ("fix1", "PUSH"): "تزق", ("fix1", "FILTER"): "فلتر", ("fix1", "SALT"): "الملح", ("fix1", "PRESSURE"): "بضغط",
        ("fix1", "THOUSAND"): "ستمية", ("fix1", "UNDER"): "تحت",
        ("break2", "SAND"): "رمل", ("break2", "SEAWEED"): "وطحالب", ("break2", "JELLYFISH"): "وقناديل",
        ("break2", "CLOG"): "وبيسدوا", ("break2", "DAY"): "يوم",
        ("fix2", "SCREENS"): "شبك", ("fix2", "INTAKE"): "المدخل", ("fix2", "SAND"): "رمل", ("fix2", "CLEAN"): "نضيفة",
        ("fix2", "MEMBRANES"): "للأغشية",
        ("break3", "WORKS"): "اشتغلت", ("break3", "PUMPS"): "الطلمبات", ("break3", "POWER"): "كهربا",
        ("break3", "GLASS"): "كوباية", ("break3", "FORTUNE"): "ثروة",
        ("fix3", "EXCHANGER"): "مبادل", ("fix3", "SALTY"): "المالحة", ("fix3", "LEAVING"): "الخارجة",
        ("fix3", "PUSHES"): "تزق", ("fix3", "NEXT"): "الدفعة", ("fix3", "SIXTY"): "ستين",
        ("break4", "HALF"): "نص", ("break4", "TWICE"): "الضعف", ("break4", "SALTY"): "مالحة", ("break4", "FISH"): "والسمك",
        ("break4", "PIPE"): "الماسورة", ("break4", "HAPPY"): "مبسوط",
        ("fix4", "PIPE"): "الماسورة", ("fix4", "FAR"): "بعيد", ("fix4", "SPRAY"): "وترشها", ("fix4", "NOZZLES"): "فتحات",
        ("fix4", "MIXES"): "فتختلط", ("fix4", "NOTICES"): "باله",
        ("cta", "SIP"): "تشرب", ("cta", "FOLLOW"): "تابعني",
        ("reveal", "RUN"): "مد", ("reveal", "PIPE"): "ماسورة", ("reveal", "MILES"): "الكيلومترات", ("reveal", "INLAND"): "لحد",
        ("reveal", "KITCHEN"): "مطبخك", ("reveal", "TAP"): "حنفية",
        ("stat", "ONE"): "بحر", ("stat", "MILLION"): "مليون", ("stat", "ZERO"): "وصفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "FISH"): "والسمك", ("tag", "OUTLET"): "المخرج", ("tag", "SALTIER"): "شوية", ("tag", "GAMER"): "كمان",
        ("tag", "LOST"): "فسيخ"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a nuclear power plant"),
                   "stat": [("1", "SEA"), ("1,000,000", "TONS A DAY"), ("0", "CLOUDS")],
                   "L": {"seawater": "SEAWATER", "steam": "STEAM", "plant": "DESALINATION PLANT", "city": "A WHOLE CITY",
                         "fuel": "A MOUNTAIN OF FUEL", "day": "EVERY DAY", "sea_in": "SEAWATER", "fresh": "FRESH WATER",
                         "filter": "FILTER", "salt": "SALT STAYS OUT", "pressure": "PRESSURE",
                         "deep": "= 2,000 FT UNDER THE SEA", "sand": "SAND", "weed": "SEAWEED", "jelly": "JELLYFISH",
                         "clogged": "CLOGGED IN A DAY", "screens": "INTAKE SCREENS", "sandf": "SAND FILTERS",
                         "memb": "MEMBRANES", "clean": "CLEAN WATER", "pumps": "HIGH-PRESSURE PUMPS", "power": "POWER",
                         "price": "$$$$", "per": "PER GLASS", "exch": "PRESSURE EXCHANGER", "brine": "SALTY WATER OUT",
                         "next": "NEXT BATCH IN", "bill": "POWER BILL -60%", "half": "HALF COMES BACK",
                         "twice": "2× SALTY", "far": "FAR OUT TO SEA", "nozzles": "NOZZLES", "miles": "250 MILES INLAND",
                         "tap": "KITCHEN TAP", "outlet": "OUTLET", "gameover": "GAME OVER", "fesikh": "FESIKH"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: محطة نووية"),
                      "stat": [("1", "بحر"), ("1,000,000", "طن في اليوم"), ("0", "سحاب")],
                      "L": {"seawater": "مية البحر", "steam": "بخار", "plant": "محطة تحلية", "city": "مدينة كاملة",
                            "fuel": "جبل وقود", "day": "كل يوم", "sea_in": "مية البحر", "fresh": "مية حلوة",
                            "filter": "فلتر", "salt": "الملح بيفضل برة", "pressure": "الضغط",
                            "deep": "= 600 متر تحت البحر", "sand": "رمل", "weed": "طحالب", "jelly": "قناديل",
                            "clogged": "اتسد في يوم", "screens": "شبك المدخل", "sandf": "فلاتر رمل", "memb": "الأغشية",
                            "clean": "مية نضيفة", "pumps": "طلمبات الضغط العالي", "power": "كهربا", "price": "$$$$",
                            "per": "الكوباية", "exch": "مبادل الضغط", "brine": "المالحة خارجة",
                            "next": "الدفعة الجاية داخلة", "bill": "توفير 60%", "half": "النص بيرجع",
                            "twice": "ملح الضعف", "far": "بعيد جوه البحر", "nozzles": "فتحات رش",
                            "miles": "مئات الكيلومترات", "tap": "حنفية المطبخ", "outlet": "المخرج", "gameover": "",
                            "fesikh": "فسيخ"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "boil": ("hook", "BOIL", 0.1), "seawater": ("hook", "SEAWATER", 0.2), "catch": ("hook", "CATCH", 0.35),
            "steam": ("hook", "STEAM", 0.45), "congrats": ("hook", "CONGRATS", 0.6), "desal": ("hook", "DESALINATION", 0.85),
            "city": ("break1", "CITY", 0.35), "burns": ("break1", "BURNS", 0.5), "mountain": ("break1", "MOUNTAIN", 0.62),
            "fuel": ("break1", "FUEL", 0.75), "day": ("break1", "DAY", 0.95),
            "push": ("fix1", "PUSH", 0.1), "filter": ("fix1", "FILTER", 0.3), "salt": ("fix1", "SALT", 0.45),
            "pressure": ("fix1", "PRESSURE", 0.65), "thousand": ("fix1", "THOUSAND", 0.8), "under": ("fix1", "UNDER", 0.9),
            "sand": ("break2", "SAND", 0.3), "weed": ("break2", "SEAWEED", 0.42), "jelly": ("break2", "JELLYFISH", 0.55),
            "clog": ("break2", "CLOG", 0.75), "day2": ("break2", "DAY", 0.95),
            "screens": ("fix2", "SCREENS", 0.2), "intake": ("fix2", "INTAKE", 0.35), "sandf": ("fix2", "SAND", 0.5),
            "clean": ("fix2", "CLEAN", 0.7), "memb": ("fix2", "MEMBRANES", 0.9),
            "works": ("break3", "WORKS", 0.12), "pumps": ("break3", "PUMPS", 0.35), "power": ("break3", "POWER", 0.55),
            "glass": ("break3", "GLASS", 0.75), "fortune": ("break3", "FORTUNE", 0.92),
            "exch": ("fix3", "EXCHANGER", 0.15), "salty": ("fix3", "SALTY", 0.3), "leaving": ("fix3", "LEAVING", 0.4),
            "pushes": ("fix3", "PUSHES", 0.5), "next": ("fix3", "NEXT", 0.58), "sixty": ("fix3", "SIXTY", 0.88),
            "half": ("break4", "HALF", 0.1), "twice": ("break4", "TWICE", 0.4), "salty2": ("break4", "SALTY", 0.5),
            "fish": ("break4", "FISH", 0.65), "pipe": ("break4", "PIPE", 0.8), "happy": ("break4", "HAPPY", 0.95),
            "pipe2": ("fix4", "PIPE", 0.08), "far": ("fix4", "FAR", 0.2), "spray": ("fix4", "SPRAY", 0.45),
            "nozzles": ("fix4", "NOZZLES", 0.6), "mixes": ("fix4", "MIXES", 0.75), "notices": ("fix4", "NOTICES", 0.95),
            "sip": ("cta", "SIP", 0.2), "follow": ("cta", "FOLLOW", 0.35),
            "run": ("reveal", "RUN", 0.15), "pipe3": ("reveal", "PIPE", 0.25), "miles": ("reveal", "MILES", 0.6),
            "inland": ("reveal", "INLAND", 0.7), "kitchen": ("reveal", "KITCHEN", 0.85), "tap": ("reveal", "TAP", 0.95),
            "s1": ("stat", "ONE", 0.04), "s2": ("stat", "MILLION", 0.42), "s3": ("stat", "ZERO", 0.72),
            "cong2": ("closer", "CONGRATS", 0.16),
            "fish2": ("tag", "FISH", 0.15), "outlet": ("tag", "OUTLET", 0.35), "saltier": ("tag", "SALTIER", 0.55),
            "gamer": ("tag", "GAMER", 0.75), "lost": ("tag", "LOST", 0.92)})
        T["c2"] = min(T["clean"], T["memb"])                    # the two languages say these two in either order
        T["f2end"] = max(T["clean"], T["memb"])
        T["kt"] = min(T["kitchen"], T["tap"])
        T["salt2"] = min(T["twice"], T["salty2"])
        # ---- sets
        self.cut(s("fix1") - 0.12, "membrane", 1)
        self.cut(s("break2") - 0.12, "intake", -1)
        self.cut(T["sandf"] - 0.22, "plant", 1)
        self.cut(s("break4") - 0.12, "outfall", -1)
        self.cut(s("cta") + 0.05, "land", 1)
        self.cut(s("tag") - 0.2, "fish", 1)
        self.cams = {"pot": Camera(60, -230, 1.45), "membrane": Camera(0, -40, 1.0), "intake": Camera(120, -280, 0.95),
                     "plant": Camera(-600, -250, 1.15), "outfall": Camera(-160, -280, 1.0), "land": Camera(4560, -250, 1.05),
                     "fish": Camera(0, -10, 1.0)}
        cm = self.cams
        cm["pot"].key(0.05, 60, -210, 1.3, 1.1).key(T["city"] - 0.5, 140, -640, 0.42, 1.6)
        cm["membrane"].key(s("fix1"), 0, -40, 1.06, 2.5)
        cm["intake"].key(s("break2"), 80, -280, 1.0, 1.6).key(s("fix2") - 0.1, 20, -300, 1.08, 0.8)
        cm["plant"].key(T["sandf"] - 0.1, -600, -250, 1.12, 1.0).key(T["c2"] - 0.25, 150, -300, 0.92, 1.0)
        cm["plant"].key(s("break3"), -40, -300, 0.74, 0.8).key(T["pumps"] - 0.2, -280, -240, 1.15, 0.7)
        cm["plant"].key(T["glass"] - 0.25, 560, -250, 1.2, 0.7)
        cm["plant"].key(s("fix3") - 0.1, 40, -200, 1.25, 0.8).key(T["sixty"] - 0.3, -20, -300, 0.78, 0.8)
        cm["outfall"].key(s("break4"), -120, -280, 1.0, 1.5)
        cm["outfall"].key(T["pipe2"] - 0.1, 850, -330, 0.7, max(1.0, T["nozzles"] - T["pipe2"]))
        cm["outfall"].key(T["mixes"] - 0.2, 480, -300, 0.55, 1.0)
        cm["land"].key(s("cta") - 0.1, 4440, -220, 1.25, 1.2)
        cm["land"].key(T["run"] - 0.1, 3800, -320, 0.5, max(0.8, T["miles"] - T["run"]))
        cm["land"].key(T["miles"], 2000, -560, 0.18, max(0.8, T["kt"] - T["miles"] - 0.3))
        cm["land"].key(T["kt"] - 0.3, 250, -175, 1.35, 0.9)
        cm["land"].key(T["s1"] - 0.3, 2500, -900, 0.14, 1.1)
        cm["land"].key(s("closer") - 0.2, 4700, -330, 0.6, 0.9)
        cm["fish"].key(s("tag") - 0.2, 0, -20, 1.06, 3.0)
        # ---- tracks
        self.potS = Track(1.0).to(T["city"] - 0.45, 4.2, 1.5, e_io)
        self.boil = Track(0.0).to(T["boil"] - 0.1, 1.0, 0.6)
        self.cityk = Track(0.0).to(T["city"] - 0.3, 1.0, 0.9, e_out)
        self.coal = Track(0.0).to(T["mountain"] - 0.25, 1.0, 0.8, e_out)
        self.piston = Track(0.0).to(T["push"] - 0.1, 1.0, max(1.2, T["salt"] - T["push"] + 0.6), e_io)
        self.press = Track(0.08).to(T["pressure"] - 0.15, 0.86, 0.9, e_out)
        self.clogk = Track(0.0).to(T["sand"], 0.3, 1.0).to(T["clog"] - 0.1, 1.0, 0.8)
        self.clogk.to(T["screens"] - 0.1, 0.0, 0.8)
        self.screen = Track(0.0).to(T["screens"] - 0.15, 1.0, 0.6, e_out)
        self.pumpk = Track(0.0).to(T["works"] - 0.2, 0.5, 0.5).to(T["pumps"] - 0.1, 1.0, 0.5)
        self.meterk = Track(0.2).to(T["power"] - 0.2, 0.97, max(0.8, T["fortune"] - T["power"] + 0.2))
        self.meterk.to(T["sixty"] - 0.15, 0.36, 0.9)
        self.exk = Track(0.0).to(T["exch"] - 0.15, 1.0, 0.6, e_out)
        self.plume = Track(0.0).to(T["half"] - 0.1, 1.0, max(0.8, T["fish"] - T["half"])).to(T["mixes"] - 0.1, 0.0, 1.2)
        self.mood = Track(1.0).to(T["fish"] - 0.1, -1.0, 0.5).to(T["mixes"] + 0.1, 1.0, 0.6)
        self.pipeX = Track(0.0).to(T["pipe2"] - 0.1, 1.0, max(0.9, T["spray"] - T["pipe2"]), e_io)
        self.pipeL = Track(0.0).to(T["run"] - 0.05, 1.0, max(1.0, T["kt"] - T["run"] - 0.2), e_io)
        self.saltk = Track(0.0).to(T["saltier"] - 0.1, 0.5, 0.6).to(T["gamer"] - 0.1, 1.0, 0.6)
        self.spans = [(T["burns"], T["under"] + 0.5), (T["clog"], T["f2end"] + 0.3), (T["fortune"], T["sixty"] + 0.4),
                      (T["happy"], T["notices"] + 0.3)]
        self.shakes = [(T["boil"], 0.2, 4), (T["mountain"] + 0.2, 0.4, 10), (T["push"] + 0.2, 0.3, 8), (T["clog"], 0.4, 10),
                       (T["screens"] + 0.4, 0.3, 8), (T["pumps"], 0.5, 8), (T["fortune"], 0.3, 10), (T["exch"] + 0.3, 0.3, 8),
                       (T["happy"], 0.3, 6), (T["lost"], 0.4, 12), (s("closer") + 0.2, 0.35, 10)]

    def at(self, x, y):
        return self.to_screen(self.ui.get("cam", (0, 0, 1.0)), x, y)

    # ------------------------------------------------------------------ set: the pot (hook, break1)
    def draw_pot(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["pot"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        hz = gy - 60 - 70 * z ** 0.5
        v2.sky(c, W, H, 0.0, horizon_y=hz)
        v2.stars(c, W, H, t, 0.9, dx=-cx * 0.02)
        mx = 840 - cx * 0.03
        v2.moon(c, mx, hz - 620, 60)
        vrect(c, 0, hz, W, max(4.0, gy - hz + 8), ["#2A4A86", "#14295A"])            # the sea behind the beach
        for i in range(18):
            u = i / 18
            yy = hz + (gy - hz) * u
            ww = (20 + 160 * u) * (0.6 + 0.4 * math.sin(t * 2 + i))
            c.drawRRect(rr(mx - ww / 2, yy, ww, 3 + 3 * u, 2), P("#DCE6FF", 0.45 * (1 - u * 0.6)))
        self.view(c, cam)
        x0, x1 = cx - 640 / z, cx + 640 / z
        ck = self.cityk.at(t)
        if ck > 0.02:                                                                 # the city rises behind it
            c.save()
            c.clipRect(R(-2200, -1400, 1700, 1400))
            c.translate(0, (1 - ck) * 900)
            v2set.skyline_night(c, -1750, -620, base_y=0, seed=6, hmin=260, hmax=860, lit=0.45, t=t)
            c.restore()
        c.drawRect(R(x0, 0, x1 - x0, 4000), lin_paint(0, 0, 0, 700, [SAND_C, "#7A5A35"]))
        c.drawLine(x0, 0, x1, 0, P("#E8C891", 0.8, stroke=4))
        rng = random.Random(2)
        for _ in range(40):
            c.drawOval(R(rng.uniform(-2000, 2000), rng.uniform(10, 400), rng.uniform(8, 22), rng.uniform(4, 9)),
                       P("#7A5A35", 0.5))
        S = self.potS.at(t) * e_back(prog(t, 0.0, 0.35))
        burn = self.coal.at(t)
        coal_heap(c, 430, 1100, 1000 * burn, t, burn)
        if t >= T["burns"] - 0.3:                                                    # black smoke from the fire
            v2.smoke(c, 0, -60 * S, t, T["burns"] - 0.3, rate=9, life=3.4, spread=(260, -140), rise=-50, size=(60, 300),
                     col="#3F3F46", lit="#FF8A3D", lit_until=0.4, seed=3, a=0.75)
            v2.smoke(c, 980, -900, t, T["mountain"], rate=7, life=3.4, spread=(200, -160), rise=-50, size=(60, 280),
                     col="#52525B", lit="#FF8A3D", lit_until=0.4, seed=4, a=0.7)
        c.save()
        c.scale(S, S)
        boil = self.boil.at(t) * (1 + 0.6 * burn)
        pot(c, t, boil=min(1.0, boil), steam=prog(t, T["steam"] - 0.3, T["steam"] + 0.2),
            fill=0.65 * prog(t, T["steam"] + 0.1, T["congrats"] + 1.0), tube=1 - prog(t, T["city"] - 0.6, T["city"]))
        c.restore()
        if burn > 0:                                                                 # the big fire under it
            for i in range(3):
                v2.flame(c, -200 + i * 200, -40, 110, 220 * burn, t + i * 0.3, 0.7 * burn, seed=10 + i, ang=-90)
        c.restore()
        self.ui["cam"] = cam
        self.ui["S"] = S

    def ui_pot(self, c, t, tw):
        T, s = self.T, self.tl.s
        S = self.ui.get("S", 1.0)
        if tw < s("break1") + 0.2:
            x0, y0 = self.at(-40 * S, -120 * S)
            self.label(x0, y0, 280, 560, "seawater", T["seawater"] - 0.1, s("break1"), FRESH)
            x1, y1 = self.at(120 * S, -300 * S)
            self.label(x1, y1, 800, 460, "steam", T["steam"] - 0.1, s("break1"), "#E5E7EB")
            self.chip(540, 690, "plant", T["congrats"] - 0.1, s("break1") + 0.2, accent=HILITE, size=44)
            return
        self.chip(290, 470, "city", T["city"], s("fix1") - 0.15, size=38)
        x2, y2 = self.at(900, -560)
        self.label(x2, y2, 800, 570, "fuel", T["mountain"], s("fix1") - 0.15, WARN)
        self.chip(540, 700, "day", T["day"] - 0.1, s("fix1") - 0.15, accent=WARN, size=40)
        self.badge("alert", T["burns"], s("fix1") - 0.2, y=380)
        self.red(T["burns"], 2.4)

    # ------------------------------------------------------------------ set: the membrane close-up (fix1)
    MX, X0, X1, Y0, Y1 = 70, -440, 440, -220, 140

    def draw_membrane(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["membrane"].at(t)
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#0B132B", "#05081A"]))
        for gx in range(0, W, 60):
            c.drawLine(gx, 0, gx, H, P("#FFFFFF", 0.035, stroke=1))
        for gy_ in range(0, H, 60):
            c.drawLine(0, gy_, W, gy_, P("#FFFFFF", 0.035, stroke=1))
        self.view(c, cam)
        MX, X0, X1, Y0, Y1 = self.MX, self.X0, self.X1, self.Y0, self.Y1
        pk = self.piston.at(t)
        ft = max(0.0, t - T["push"] + 0.1)
        fresh = prog(t, T["push"] + 0.2, T["salt"] + 1.2)
        face = X0 + 16 + 120 * pk
        c.drawRect(R(260, -330, 16, 120), P("#64748B"))                               # the gauge's stem
        c.drawRRect(rr(X0 - 22, Y0 - 22, X1 - X0 + 44, Y1 - Y0 + 44, 34),
                    lin_paint(0, Y0 - 22, 0, Y1 + 22, ["#64748B", "#334155"]))
        body = rr(X0, Y0, X1 - X0, Y1 - Y0, 20)
        c.drawRRect(body, P("#0B1220"))
        c.save()
        c.clipRRect(body, skia.ClipOp.kIntersect, True)
        vrect(c, X0, Y0, MX - X0, Y1 - Y0, [SEA_C, "#143A73"])
        vrect(c, MX, Y0, X1 - MX, Y1 - Y0, [mix("#0B1220", "#3BA7E0", fresh), mix("#0B1220", "#1E6FA8", fresh)])
        for i in range(54):                                                           # water gets through
            rng = random.Random(100 + i)
            y = rng.uniform(Y0 + 18, Y1 - 18) + math.sin(t * 2.3 + i) * 5
            x0_ = rng.uniform(X0 + 40, MX - 30)
            if t < T["push"] - 0.1:
                x = x0_ + math.sin(t * 1.7 + i) * 6
            else:
                span = X1 - 24 - face
                x = face + 12 + ((x0_ - X0) + ft * rng.uniform(120, 200)) % max(1.0, span)
            c.drawCircle(x, y, 8, P("#93C5FD", 0.95))
            c.drawCircle(x - 2.5, y - 2.5, 2.5, P("#FFFFFF", 0.9))
        for i in range(26):                                                           # salt can't
            rng = random.Random(300 + i)
            y = rng.uniform(Y0 + 16, Y1 - 16)
            x0_ = rng.uniform(X0 + 40, MX - 60)
            stop = MX - 18 - rng.uniform(0, 80) * (1 - 0.7 * pk)
            x = min(max(face + 14, x0_ + ft * rng.uniform(80, 150)), stop)
            if x >= stop - 0.5 and t > T["push"]:
                x -= abs(math.sin((t - T["push"]) * 9 + i)) * 5
            c.drawRRect(rr(x - 7, y - 7, 14, 14, 3), P(SALT_C, 0.95))
            c.drawRRect(rr(x - 7, y - 7, 14, 14, 3), P("#94A3B8", 0.9, stroke=2))
        c.restore()
        c.drawRect(R(X0 - 420, (Y0 + Y1) / 2 - 18, face - X0 + 420, 36), P("#94A3B8"))  # the piston
        box(c, face - 30, Y0 + 6, 30, Y1 - Y0 - 12, "#CBD5E1", r=8)
        c.drawRect(R(MX - 10, Y0, 20, Y1 - Y0), P("#FDE68A"))                         # the filter
        for yy in range(Y0 + 8, Y1, 14):
            c.drawCircle(MX, yy, 2.6, P("#B45309"))
        ok = prog(t, T["filter"] - 0.1, T["filter"] + 0.25) * (1 - prog(t, T["salt"] + 0.6, T["salt"] + 1.0))
        if ok > 0:
            c.drawRRect(rr(MX - 22, Y0 - 14, 44, Y1 - Y0 + 28, 12), P("#FFFFFF", 0.95 * ok, stroke=6))
        a_ = prog(t, s("fix1") + 0.1, s("fix1") + 0.4)
        word(c, self.L["sea_in"], (X0 + MX) / 2, Y0 - 50, 34, FRESH, a=a_)
        word(c, self.L["fresh"], (MX + X1) / 2, Y0 - 50, 34, "#BAE6FD", a=a_ * max(0.35, fresh))
        gk = prog(t, T["pressure"] - 0.4, T["pressure"])
        if gk > 0:
            c.save()
            c.translate(268, -420)
            c.scale(e_back(gk), e_back(gk))
            dial(c, 0, 0, 92, self.press.at(t), t)
            c.restore()
            word(c, self.L["pressure"], 268, -540, 32, "#E5E7EB", a=gk)
        c.restore()
        self.ui["cam"] = cam

    def ui_membrane(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(self.MX, self.Y0 + 20)
        self.label(x0, y0, 300, 560, "filter", T["filter"] - 0.1, T["salt"] - 0.05, HILITE)
        x1, y1 = self.at(self.MX - 40, -40)
        self.label(x1, y1, 300, 560, "salt", T["salt"], s("break2") - 0.2, "#E5E7EB")
        self.chip(540, 330, "deep", T["thousand"] - 0.1, s("break2") - 0.15, accent=HILITE, size=40)
        self.badge("check", T["under"] + 0.4, s("break2") - 0.15, x=130, y=700)

    # ------------------------------------------------------------------ set: the intake (break2, start of fix2)
    MOUTH = (0, -266)

    def suck(self, t, t0, start, i, rate, away=None):
        """Position of a piece of junk pulled from `start` into the intake mouth (loops); after the screen goes on it
        hangs outside the screen at the angle `away`."""
        mx, my = self.MOUTH
        rng = random.Random(i * 31 + 7)
        u = ((t - t0) * rate + rng.random()) % 1.0
        e_ = e_in(u)
        x = lerp(start[0], mx, e_) + math.sin(u * 9 + i) * 30 * (1 - e_)
        y = lerp(start[1], my, e_) + math.cos(u * 7 + i) * 20 * (1 - e_)
        a = clamp(u * 6) * clamp((1 - u) * 8)
        if away is not None:
            k = e_out(prog(t, self.T["screens"] + 0.1, self.T["screens"] + 0.7))
            if k > 0:
                r_ = 250 + 14 * math.sin(t * 2 + i)
                hx, hy = mx + math.cos(away) * r_, my + math.sin(away) * r_ * 0.8
                x, y, a = lerp(x, hx, k), lerp(y, hy, k), lerp(a, 1.0, k)
        return x, y, a

    def draw_intake(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["intake"].at(t)
        cx, cy, z = cam
        v2set.underwater(c, W, H, t, seed=7)
        self.view(c, cam)
        x0, x1 = cx - 640 / z, cx + 640 / z
        vrect(c, x0, 0, x1 - x0, 1600, [SAND_C, "#7A5A35"])
        for xx in range(int(x0) // 90 * 90, int(x1), 90):
            c.drawLine(xx, 16, xx + 50, 11, P("#E8C891", 0.35, stroke=3))
        for i, (wx, ws) in enumerate(((-520, 1.7), (-470, 1.3), (430, 1.5), (500, 1.9), (560, 1.2))):
            weed(c, wx, 4, ws, t, seed=i)
        mx, my = self.MOUTH
        cyl(c, -46, -232, 92, 236, "#64748B", r=8)                                    # the riser and its cap
        for px in (-34, 0, 34):
            c.drawRect(R(px - 4, -300, 8, 72), P("#475569"))
        c.drawRRect(rr(-150, -334, 300, 36, 16), lin_paint(0, -334, 0, -298, ["#CBD5E1", "#64748B"]))
        clog = self.clogk.at(t)
        inflow = 1 - 0.85 * clog
        for i in range(8):
            u = (t * 0.8 + i / 8) % 1.0
            for sd in (-1, 1):
                ax = sd * lerp(280, 50, u)
                p_ = P("#BAE6FD", 0.55 * inflow * (1 - u), stroke=4)
                c.drawLine(ax + sd * 12, my - 10, ax, my, p_)
                c.drawLine(ax, my, ax + sd * 12, my + 10, p_)
        if t >= T["sand"] - 0.4:                                                      # sand from the seabed
            for i in range(36):
                rng = random.Random(500 + i)
                x, y, a = self.suck(t, T["sand"] - 0.4, (rng.uniform(-620, 640), -4), i, rng.uniform(0.45, 0.8))
                c.drawCircle(x, y, rng.uniform(3, 6), P("#E8C891", 0.9 * a))
        if t >= T["weed"] - 0.3:
            for i in range(6):
                rng = random.Random(600 + i)
                st = (rng.uniform(500, 760), rng.uniform(-620, -160))
                x, y, a = self.suck(t, T["weed"] - 0.3, st, i + 40, rng.uniform(0.25, 0.4), away=-0.3 - i * 0.12)
                weed(c, x, y, 1.0, t, rot=math.sin(t + i) * 40 + 70, a=a, seed=i)
        if t >= T["jelly"] - 0.3:
            for i in range(3):
                st = (640 + i * 60, -700 + i * 170)
                x, y, a = self.suck(t, T["jelly"] - 0.3, st, i + 80, 0.22 + 0.04 * i, away=-0.9 - i * 0.35)
                jelly(c, x, y, 1.35 - 0.15 * i, t, a=a, seed=i)
        if clog > 0:
            rng = random.Random(9)
            for i in range(16):
                k = clamp(clog * 16 - i)
                if k > 0:
                    c.drawCircle(rng.uniform(-130, 130), rng.uniform(-296, -238), rng.uniform(10, 22) * k,
                                 P(rng.choice(["#78350F", "#3F6212", "#A16207"]), 0.95))
        sk = self.screen.at(t)
        if sk > 0:
            c.save()
            c.translate(0, lerp(-700, 0, e_out(sk)))
            frame = rr(-196, -368, 392, 168, 40)
            c.drawRRect(frame, P("#CBD5E1", 0.12))
            c.save()
            c.clipRRect(frame, skia.ClipOp.kIntersect, True)
            for xx in range(-196, 197, 22):
                c.drawLine(xx, -368, xx, -200, P("#E2E8F0", 0.85, stroke=3))
            for yy in range(-368, -199, 22):
                c.drawLine(-196, yy, 196, yy, P("#E2E8F0", 0.85, stroke=3))
            c.restore()
            c.drawRRect(frame, P("#F8FAFC", 1, stroke=7))
            c.restore()
        c.restore()
        self.ui["cam"] = cam

    def ui_intake(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.1:
            self.chip(220, 430, "sand", T["sand"] - 0.05, s("fix2") - 0.15, size=36)
            self.chip(520, 430, "weed", T["weed"] - 0.05, s("fix2") - 0.15, size=36)
            self.chip(840, 430, "jelly", T["jelly"] - 0.05, s("fix2") - 0.15, size=36)
            p = self.span(T["sand"] + 0.2, s("fix2") - 0.1)
            if p > 0:                                                                 # the filter, getting clogged
                k = e_back(p)
                c.save()
                c.translate(230, 700)
                c.scale(k, k)
                c.drawCircle(0, 0, 128, P("#0F172A", 0.9))
                c.drawCircle(0, 0, 116, P("#FDE68A"))
                for yy in range(-110, 111, 16):
                    for xx in range(-110, 111, 16):
                        if xx * xx + yy * yy < 110 * 110:
                            c.drawCircle(xx, yy, 2.4, P("#B45309"))
                clog = clamp(self.clogk.at(tw) / 1.0)
                rng = random.Random(21)
                for i in range(40):
                    kk = clamp(clog * 40 - i)
                    if kk > 0:
                        an, rad = rng.uniform(0, 6.283), 110 * math.sqrt(rng.random())
                        c.drawCircle(math.cos(an) * rad, math.sin(an) * rad, rng.uniform(12, 26) * kk,
                                     P(rng.choice(["#78350F", "#3F6212", "#A16207", "#F9A8D4"]), 0.95))
                c.drawCircle(0, 0, 122, P(WARN if clog > 0.6 else "#E2E8F0", 0.95, stroke=8))
                c.restore()
                word(c, self.L["filter"], 230, 545, 32, "#E5E7EB", a=p)
            self.chip(230, 880, "clogged", T["clog"], s("fix2") - 0.15, accent=WARN, size=34)
            self.badge("alert", T["clog"], s("fix2") - 0.2, y=560)
            self.red(T["clog"], 2.0)
            return
        x0, y0 = self.at(150, -330)
        self.label(x0, y0, 780, 600, "screens", T["screens"] - 0.05, T["sandf"] - 0.25, GOOD)

    # ------------------------------------------------------------------ set: inside the plant (fix2, break3, fix3)
    SEA_IN = [(-900, -440), (-713, -440), (-713, -380)]
    SEA_IN2 = [(-713, -440), (-553, -440), (-553, -380)]
    FEED = [(-490, -40), (-120, -40)]
    UP = [(-120, -40), (-90, -40), (-90, -470), (-20, -470)]
    MAN = [(-60, -470), (-60, -290)]
    FRESH_OUT = [(540, -470), (650, -470), (650, -200)]
    BRINE_OUT = [(540, -290), (600, -290), (600, -24), (900, -24)]
    EX_IN = [(600, -125), (190, -125)]
    EX_OUT = [(-60, -150), (-90, -150)]

    def draw_plant(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["plant"].at(t)
        cx, cy, z = cam
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1E2440", "#0F1428"]))
        self.view(c, cam)
        x0, x1 = cx - 640 / z, cx + 640 / z
        for xx in range(int(x0) // 160 * 160, int(x1), 160):
            c.drawLine(xx, -700, xx, 0, P("#FFFFFF", 0.04, stroke=3))
        c.drawRect(R(x0, -700, x1 - x0, 30), P("#2E3656"))
        for xx in range(int(x0) // 260 * 260, int(x1), 260):
            c.drawRRect(rr(xx + 60, -664, 130, 14, 6), P("#E0F2FE", 0.8))
            add_glow(c, xx + 125, -650, 150, "#C7E7FF", 0.15)
        c.drawRect(R(x0, 0, x1 - x0, 900), lin_paint(0, 0, 0, 400, ["#3B4160", "#202538"]))
        c.drawLine(x0, 0, x1, 0, P("#9AA6BF", 0.6, stroke=4))
        run = prog(t, T["sandf"] - 0.2, T["sandf"] + 0.4)
        clean = prog(t, T["c2"] - 0.2, T["c2"] + 0.4)
        works = max(clean, prog(t, s("break3"), s("break3") + 0.3))
        for p_ in (self.SEA_IN, self.SEA_IN2):
            pipe(c, p_)
            flow(c, p_, t, run, n=8, col="#60A5FA", salt=0.3, seed=2)
        sand_tank(c, -780, 134, 380, t, run)
        sand_tank(c, -620, 134, 380, t, run)
        pipe(c, self.FEED)
        flow(c, self.FEED, t, run, n=10, col="#BAE6FD", seed=3)
        pk = self.pumpk.at(t)
        exk = self.exk.at(t)
        ph = 0.5 + 0.5 * math.cos((t - T["exch"]) * 2.4)
        pipe(c, self.UP)
        pipe(c, self.MAN, PIPE_C, 18)
        flow(c, self.UP, t, works, n=12, col="#BAE6FD", seed=4)
        vessels(c, t)
        hl = prog(t, T["memb"] - 0.1, T["memb"] + 0.2) * (1 - prog(t, T["f2end"] + 0.8, T["f2end"] + 1.2))
        if hl > 0:
            c.drawRRect(rr(-40, -520, 620, 280, 30), P("#FFFFFF", 0.9 * hl, stroke=6))
        for y in RACK_Y:                                                              # fresh water inside the racks
            flow(c, [(0, y), (520, y)], t, works, n=8, col="#E0F2FE", r=5, seed=int(-y))
        pipe(c, self.FRESH_OUT, "#38BDF8", 18)
        flow(c, self.FRESH_OUT, t, works, n=8, col="#E0F2FE", seed=5)
        if exk < 1:
            pipe(c, self.BRINE_OUT, "#B45309", 18, a=1 - exk)
            flow(c, self.BRINE_OUT, t, works * (1 - exk), n=9, col=BRINE, salt=0.4, seed=6)
        if exk > 0:
            pipe(c, [(540, -290), (600, -290), (600, -125)] + self.EX_IN[1:], "#B45309", 18, a=exk)
            flow(c, [(540, -290), (600, -290), (600, -125), (190, -125)], t, exk, n=9, col=BRINE, salt=0.4, seed=7)
            drain = [(-60, -100), (-110, -100), (-110, -24), (-140, -24)]
            pipe(c, drain, "#92400E", 16, a=exk)
            flow(c, drain, t, exk, n=5, col="#FBBF24", seed=8)
            pipe(c, self.EX_OUT, PIPE_C, 16, a=exk)
            exchanger(c, -60, -170, 250, 90, t, exk, ph)
        for i, px in enumerate((-410, -240)):
            pump(c, px, t + i * 0.13, pk)
        fill = prog(t, T["works"] - 0.2, T["works"] + 1.5) * 0.8
        c.drawRect(R(610, -110, 80, 110), P("#475569"))
        c.drawRect(R(600, -116, 100, 10), P("#64748B"))
        cup(c, 650, -116, 64, 90, fill)
        if works > 0:
            for i in range(2):
                u = (t * 1.6 + i / 2) % 1.0
                c.drawCircle(650, lerp(-196, -120, u * u), 5, P(FRESH, 0.95 * works))
        mk = self.meterk.at(t)                                                        # the power meter on the wall
        box(c, -250, -640, 170, 150, "#E5E7EB", r=12)
        dial(c, -165, -560, 56, mk, t, warn=0.65)
        if mk > 0.7:
            for i in range(3):
                bx = -300 + i * 30
                bolt = skia.Path()
                bolt.moveTo(bx, -660)
                bolt.lineTo(bx - 14, -620)
                bolt.lineTo(bx + 2, -620)
                bolt.lineTo(bx - 10, -584)
                bolt.lineTo(bx + 18, -632)
                bolt.lineTo(bx + 2, -632)
                bolt.close()
                c.drawPath(bolt, P(HILITE, 0.9 * (0.5 + 0.5 * math.sin(t * 14 + i))))
        tag = prog(t, T["glass"] - 0.2, T["glass"] + 0.2) * (1 - prog(t, s("fix3") - 0.3, s("fix3")))
        if tag > 0:                                                                   # the price tag on the glass
            c.save()
            c.translate(690, -200)
            c.rotate(12 + math.sin(t * 3) * 4)
            c.scale(e_back(tag), e_back(tag))
            c.drawLine(-30, 10, 0, 40, P("#E5E7EB", 1, stroke=3))
            c.drawRRect(rr(0, 30, 170, 96, 14), P("#FDE68A"))
            c.drawCircle(18, 48, 7, P("#0F172A"))
            word(c, self.L["price"], 92, 86, 40, "#B91C1C")
            word(c, self.L["per"], 92, 114, 20, "#0F172A")
            c.restore()
        if t >= T["fortune"] - 0.1:
            rng = random.Random(77)
            for i in range(14):
                age = t - T["fortune"] + 0.1 - i * 0.04
                if 0 < age < 1.4:
                    vx, vy = rng.uniform(-260, 260), rng.uniform(-620, -380)
                    x, y = 760 + vx * age, -180 + vy * age + 900 * age * age
                    c.drawCircle(x, y, 13, P("#FACC15"))
                    c.drawCircle(x, y, 13, P("#A16207", 1, stroke=3))
        c.restore()
        self.ui["cam"] = cam

    def ui_plant(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break3"):
            x0, y0 = self.at(-560, -300)
            self.label(x0, y0, 790, 520, "sandf", T["sandf"] - 0.05, T["c2"] - 0.15, SAND_C)
            x1, y1 = self.at(260, -500)
            self.label(x1, y1, 290, 460, "memb", T["memb"] - 0.05, s("break3") - 0.1, "#E5E7EB")
            self.chip(760, 620, "clean", T["clean"] - 0.05, s("break3") - 0.1, accent=FRESH, size=36)
            self.badge("check", T["f2end"] + 0.3, s("break3") - 0.1, x=880, y=760)
            return
        if tw < s("fix3") - 0.1:
            x0, y0 = self.at(-300, -126)
            self.label(x0, y0, 300, 470, "pumps", T["pumps"] - 0.05, T["glass"] - 0.2, "#60A5FA")
            self.chip(800, 470, "power", T["power"] - 0.05, s("fix3") - 0.15, accent=HILITE, size=38)
            self.badge("alert", T["fortune"], s("fix3") - 0.2, y=600)
            self.red(T["fortune"], 2.0)
            return
        x0, y0 = self.at(60, -186)
        self.label(x0, y0, 540, 470, "exch", T["exch"] - 0.05, s("break4") - 0.15, GOOD)
        x1, y1 = self.at(400, -125)
        self.label(x1, y1, 800, 640, "brine", T["leaving"] - 0.1, s("break4") - 0.15, BRINE, size=30)
        x2, y2 = self.at(-90, -190)
        self.label(x2, y2, 280, 640, "next", T["next"] - 0.1, s("break4") - 0.15, FRESH, size=30)
        self.chip(700, 560, "bill", T["sixty"] - 0.05, s("break4") - 0.15, accent=GOOD, size=46)
        self.badge("check", T["sixty"] + 0.3, s("break4") - 0.15, x=920, y=900)

    # ------------------------------------------------------------------ set: the outfall (break4, fix4)
    FISHES = ((-60, -330, 1.3, 1, "#FB923C"), (130, -210, 1.0, -1, "#FACC15"), (280, -410, 1.15, -1, "#F472B6"),
              (440, -250, 0.95, 1, "#FB7185"), (-220, -470, 1.0, 1, "#FBBF24"))

    @staticmethod
    def bed_y(x):
        return 0.0 if x >= -300 else (x + 300) * 0.75

    def draw_outfall(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["outfall"].at(t)
        cx, cy, z = cam
        v2set.underwater(c, W, H, t, seed=11)
        self.view(c, cam)
        x0, x1 = cx - 640 / z, cx + 640 / z
        bed = skia.Path()                                                             # seabed and the shore's slope
        bed.moveTo(x0 - 50, 1600)
        xx = x0 - 50
        while xx <= x1 + 50:
            bed.lineTo(xx, self.bed_y(xx) + math.sin(xx * 0.02) * 4)
            xx += 30
        bed.lineTo(x1 + 50, 1600)
        bed.close()
        c.drawPath(bed, lin_paint(0, -600, 0, 400, [SAND_C, "#7A5A35"]))
        for i, (wx, ws) in enumerate(((-700, 1.4), (620, 1.5), (1300, 1.7), (1900, 1.3))):
            weed(c, wx, self.bed_y(wx) + 4, ws, t, seed=i + 3)
        end = -200 + 1500 * self.pipeX.at(t)
        start_x = -360
        pipe(c, [(start_x - 400, self.bed_y(start_x - 400) - 30), (start_x, -36), (end, -36)], "#6B7280", 34)
        c.drawRRect(rr(end - 10, -60, 20, 48, 6), P("#475569"))
        pl = self.plume.at(t)
        if pl > 0:                                                                    # salty water sinking by the shore
            for i in range(26):
                u = ((t * 0.16) + i / 26) % 1.0
                px = -160 + u * 760 + math.sin(i * 3.1) * 30
                py = -34 - 26 * math.sin(u * 3) + (i % 3) * 6
                puff(c, px, py, lerp(30, 130, u), "#C2410C", 0.32 * pl * (1 - u) * min(1.0, u * 6))
        spray = prog(t, T["spray"] - 0.2, T["spray"] + 0.3)
        if spray > 0:                                                                 # nozzles far out at sea
            for k in range(4):
                nx = end - 120 * k
                c.drawRect(R(nx - 8, -110, 16, 76), P("#64748B"))
                c.drawCircle(nx, -112, 11, P("#94A3B8"))
                add_glow(c, nx, -116, 60, BRINE, 0.5 * spray)
                for j in range(12):
                    v = (t * 1.3 + j / 12 + k * 0.17) % 1.0
                    px, py = nx + v * 220, -116 - v * 340
                    c.drawCircle(px, py, 8 + 12 * v, P(mix(BRINE, "#BAE6FD", v), 0.9 * spray * (1 - v)))
                    if j % 3 == 0:
                        puff(c, px + 30, py - 30, 40 + 90 * v, mix(BRINE, "#93C5FD", v), 0.22 * spray * (1 - v))
        mood = self.mood.at(t)
        away = prog(t, T["happy"], T["happy"] + 1.4) * (1 - prog(t, T["mixes"] - 0.2, T["mixes"] + 0.6))
        for i, (fx_, fy, fs, face, col) in enumerate(self.FISHES):
            x = fx_ + math.sin(t * 0.8 + i) * 30 - 220 * away
            y = fy + math.sin(t * 1.3 + i * 2) * 12
            f_ = -1 if away > 0.3 else face
            fish(c, x, y, fs * 1.6, f_, col, mood=mood, t=t + i, shades=(i == 1 and t >= T["notices"] - 0.2), seed=i)
            if mood < -0.3 and i % 2 == 0:
                v2set.bubbles(c, x + 50 * f_ * fs, y, t, T["fish"], rate=4, life=1.4, rise=120, size=(3, 8), seed=i)
        c.restore()
        self.ui["cam"] = cam

    def ui_outfall(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.1:
            self.chip(540, 430, "half", T["half"] - 0.05, s("fix4") - 0.15, accent=BRINE, size=40)
            x0, y0 = self.at(220, -60)
            self.label(x0, y0, 800, 600, "twice", T["salt2"] - 0.05, s("fix4") - 0.15, BRINE)
            self.badge("alert", T["happy"], s("fix4") - 0.2, y=560, x=250)
            self.red(T["happy"], 2.0)
            return
        self.chip(540, 430, "far", T["far"] - 0.05, s("cta") - 0.2, accent=FRESH, size=40)
        end = -200 + 1500 * self.pipeX.at(tw)
        x0, y0 = self.at(end - 180, -120)
        self.label(x0, y0, 790, 600, "nozzles", T["nozzles"] - 0.05, s("cta") - 0.2, GOOD)
        self.badge("check", T["mixes"] + 0.3, s("cta") - 0.2, x=250, y=600)

    # ------------------------------------------------------------------ set: the land (cta, reveal, stat, closer)
    HOUSE_X, PLANT_X, SHORE_X = 0, 4460, 5650

    def draw_land(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["land"].at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, horizon_y=gy)
        v2.stars(c, W, H, t, 1.0)
        v2.moon(c, 880, 720, 66)
        self.view(c, cam)
        for k, (yy, col) in enumerate(((0, "#7A5A3A"), (70, "#9A7448"), (180, SAND_C))):
            p = skia.Path()
            p.moveTo(-9000, yy + 3000)
            for xx in range(-9000, self.SHORE_X + 1, 400):
                p.lineTo(xx, yy - 34 * math.sin(xx * 0.003 + k * 2))
            p.lineTo(self.SHORE_X + 200, yy + 3000)
            p.close()
            c.drawPath(p, P(col))
        vrect(c, self.SHORE_X - 60, 14, 9000, 3000, ["#2B4C8C", "#12275A", "#0B1A44"], [0.0, 0.08, 0.4])   # the sea
        bed = skia.Path()                                                             # the seabed under it
        bed.moveTo(self.SHORE_X - 60, 0)
        bed.lineTo(self.SHORE_X + 2400, 700)
        bed.lineTo(self.SHORE_X + 9000, 900)
        bed.lineTo(self.SHORE_X + 9000, 4000)
        bed.lineTo(self.SHORE_X - 60, 4000)
        bed.close()
        c.drawPath(bed, P(SAND_C))
        for k in range(4):
            path = skia.Path()
            xx = self.SHORE_X
            path.moveTo(xx, 18 + k * 30)
            while xx < self.SHORE_X + 9000:
                xx += 60
                path.lineTo(xx, 18 + k * 30 + math.sin(xx * 0.01 + t * (1.2 + k * 0.3)) * 5)
            c.drawPath(path, P("#93C5FD", 0.3 - k * 0.06, stroke=4))
        v2set.skyline_night(c, -1900, -60, base_y=0, seed=8, hmin=200, hmax=700, lit=0.35, t=t)
        pw = max(26.0, 6.0 / z)
        head = lerp(self.PLANT_X - 20, self.HOUSE_X + 380, self.pipeL.at(t))
        if head < self.PLANT_X - 20:                                                  # the pipe inland
            for xx in range(int(head) // 220 * 220, self.PLANT_X, 220):
                if xx > head:
                    c.drawRect(R(xx - 5, -30, 10, 30), P("#475569"))
            c.drawLine(head, -34, self.PLANT_X - 20, -34, P("#1B2236", 1, stroke=pw + 8))
            c.drawLine(head, -34, self.PLANT_X - 20, -34, P(PIPE_C, 1, stroke=pw))
            if t < T["kt"]:
                add_glow(c, head, -34, 60 / max(z, 0.2), FRESH, 0.6)
            else:
                for i in range(40):
                    u = (t * 0.05 + i / 40) % 1.0
                    c.drawCircle(lerp(self.PLANT_X - 20, self.HOUSE_X + 380, u), -34, pw * 0.3, P("#E0F2FE", 0.9))
        house(c, self.HOUSE_X, t, tap=prog(t, T["tap"] - 0.1, T["tap"] + 0.2),
              fill=0.85 * prog(t, T["tap"] + 0.1, T["tap"] + 1.6))
        for i, hx in enumerate((520, 760, 1000)):                                    # neighbours
            box(c, hx, -170 - 30 * (i % 2), 180, 170 + 30 * (i % 2), ("#CBD5E1", "#E2E8F0", "#D6D3D1")[i], r=6)
            c.drawRRect(rr(hx + 40, -120, 40, 36, 4), P("#FDE68A", 0.9))
        plant_bld(c, self.PLANT_X, t)
        sip = prog(t, T["sip"] - 0.6, T["sip"] - 0.1)                                # a worker about to take a sip
        px = self.PLANT_X - 120
        person(c, px, 0, 132, "#F97316", t, "stand", face=1, hat="hard", skin=SKINS[1])
        cup(c, px + 26, lerp(-56, -104, e_io(sip)), 26, 38, 0.8)
        c.restore()
        self.ui["cam"] = cam

    def ui_land(self, c, t, tw):
        T, s = self.T, self.tl.s
        if s("reveal") <= tw < T["s1"] - 0.3:
            self.chip(540, 430, "miles", T["miles"] - 0.1, T["kt"] - 0.1, accent=FRESH, size=40)
            x0, y0 = self.at(self.HOUSE_X + 254, -206)
            self.label(x0, y0, 780, 560, "tap", T["tap"] - 0.05, T["s1"] - 0.35, FRESH)

    # ------------------------------------------------------------------ set: the fish (tag)
    def draw_fish(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cams["fish"].at(t)
        v2set.underwater(c, W, H, t, seed=13)
        self.view(c, cam)
        c.drawRect(R(-900, 260, 1800, 1200), lin_paint(0, 260, 0, 700, [SAND_C, "#7A5A35"]))
        pipe(c, [(-900, 200), (-380, 200)], "#6B7280", 60)                          # the outlet
        c.drawRRect(rr(-396, 160, 30, 80, 8), P("#475569"))
        for i in range(10):
            u = ((t * 0.2) + i / 10) % 1.0
            puff(c, -360 + u * 500, 200 - u * 40, lerp(30, 120, u), "#C2410C", 0.25 * (1 - u) * min(1.0, u * 5))
        pop = e_back(prog(t, T["fish2"] - 0.25, T["fish2"] + 0.15))
        ar = self.rtl
        salt = self.saltk.at(t) if ar else 0.0
        stiff = prog(t, T["lost"] - 0.1, T["lost"] + 0.4) if ar else 0.0
        red = prog(t, T["saltier"] - 0.1, T["saltier"] + 0.4) if not ar else 0.0
        mood = 1 - 2 * prog(t, T["saltier"] - 0.2, T["saltier"] + 0.2) if not ar else 1 - 2 * prog(t, T["saltier"], T["gamer"])
        fy = -40 + 110 * e_in(stiff) + (math.sin(t * 2) * 10) * (1 - stiff)
        if ar and stiff > 0:                                                          # fesikh: salted, on a newspaper
            c.drawRect(R(-300, 200, 600, 60), P("#E7E5E4", stiff))
            for i in range(5):
                c.drawLine(-280, 214 + i * 10, 280, 214 + i * 10, P("#78716C", 0.6 * stiff, stroke=3))
        if pop > 0:
            c.save()
            c.translate(40, fy)
            c.scale(pop, pop)
            fish(c, 0, 0, 4.2, 1, "#FB923C", mood=mood, t=t * (1 - stiff), salt=salt, dead=1.0 if ar and t >= T["gamer"] else 0.0,
                 red=red, seed=3)
            if ar and salt > 0:                                                       # salt raining on it
                rng = random.Random(4)
                for i in range(40):
                    u = (t * rng.uniform(0.6, 1.1) + rng.random()) % 1.0
                    c.drawRect(R(rng.uniform(-200, 200), lerp(-420, -60, u), 8, 8), P("#FFFFFF", 0.9 * salt))
            if not ar and t >= T["saltier"] - 0.2:                                    # steaming mad
                for i in range(3):
                    u = (t * 0.9 + i / 3) % 1.0
                    puff(c, -40 + i * 50, -140 - u * 180, 20 + 40 * u, "#F8FAFC", 0.6 * (1 - u))
            if not ar:
                g = e_back(prog(t, T["gamer"] - 0.25, T["gamer"] + 0.15))
                if g > 0:
                    hp = skia.Path()                                                  # headset
                    hp.addArc(R(-70, -150, 170, 150), 200, 140)
                    c.drawPath(hp, P("#111827", g, stroke=16))
                    c.drawRRect(rr(-80, -80, 34, 54, 12), P("#111827", g))
                    c.drawCircle(-63, -53, 8, P("#22C55E", g))
                    fly = prog(t, T["lost"], T["lost"] + 0.8)
                    c.save()
                    c.translate(150 + 420 * fly, 70 - 300 * fly + 500 * fly * fly)
                    c.rotate(360 * fly)
                    c.drawRRect(rr(-70, -26, 140, 52, 24), P("#334155", g))
                    for bx, col in ((-36, "#EF4444"), (30, "#22C55E"), (46, "#3B82F6")):
                        c.drawCircle(bx, -2, 8, P(col, g))
                    c.restore()
        if not ar:                                                                    # the game screen
            g = e_back(prog(t, T["gamer"] - 0.3, T["gamer"] + 0.1))
            if g > 0:
                c.save()
                c.translate(330, -260)
                c.scale(g, g)
                c.drawRRect(rr(-120, -80, 240, 160, 16), P("#0F172A"))
                c.drawRRect(rr(-108, -68, 216, 136, 10), P("#1E293B"))
                if t >= T["lost"] - 0.1:
                    word(c, self.L["gameover"], 0, 14, 34, WARN, a=0.6 + 0.4 * math.sin(t * 12))
                else:
                    for i in range(4):
                        c.drawRect(R(-90 + ((t * 120 + i * 60) % 180), -30 + i * 14, 20, 10), P(HILITE))
                c.restore()
        c.restore()
        self.ui["cam"] = cam

    def ui_fish(self, c, t, tw):
        T, s = self.T, self.tl.s
        x0, y0 = self.at(-380, 200)
        self.label(x0, y0, 280, 520, "outlet", T["outlet"] - 0.05, self.duration, BRINE, size=32)
        if self.rtl:
            self.chip(700, 470, "fesikh", T["lost"] - 0.05, self.duration, accent=HILITE, size=52)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -10), (T["boil"] - 0.1, sfx.hiss(0.5, 61), -12), (T["boil"], boil_snd(2.4), -10),
              (T["steam"], sfx.hiss(0.8, 62), -14), (T["steam"] + 0.4, water_snd(0.3, 63), -14),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9)]
        ev += [(T["city"] - 0.45, sfx.riser(1.4, 65), -10), (T["burns"], flow_snd(2.0, 66), -9), (T["mountain"], sfx.thud(0.6, 67), -3),
               (T["mountain"] + 0.15, sfx.thud(0.5, 68), -6), (T["burns"] + 0.1, sfx.alarm(3, 820), -11)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, True, 69), -4), (T["push"], sfx.creak(0.6, 70), -8), (T["push"] + 0.1, flow_snd(1.6, 71), -12),
               (T["salt"], sfx.tick(), -6), (T["salt"] + 0.15, sfx.tick(), -8), (T["pressure"], sfx.charge_up(0.8), -10),
               (T["under"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["sand"], flow_snd(2.2, 73), -10), (T["jelly"], sfx.pop(74), -10),
               (T["clog"], sfx.thunk(75), -4), (T["clog"] + 0.05, sfx.alarm(3, 820), -11)]
        ev += [(T["screens"] - 0.1, sfx.whoosh(0.5, False, 76), -8), (T["screens"] + 0.35, sfx.clank(600, 0.4, 77), -5),
               (T["sandf"] - 0.22, sfx.whoosh(0.4, True, 78), -4), (T["sandf"], flow_snd(1.4, 79), -12),
               (T["f2end"] + 0.3, sfx.chime(), -6)]
        ev += [(T["works"], water_snd(0.6, 80), -10), (T["pumps"] - 0.1, sfx.whirr(2.2, 140, 260, 81), -8),
               (T["power"], sfx.hum(1.8, 110), -10), (T["glass"], sfx.pop(82), -8), (T["fortune"], coins_snd(83), -6),
               (T["fortune"] + 0.05, sfx.alarm(3, 820), -11)]
        ev += [(T["exch"] - 0.1, sfx.clank(420, 0.5, 84), -5), (T["pushes"], flow_snd(1.4, 85), -11), (T["sixty"], sfx.power_down(0.8, 86), -10),
               (T["sixty"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, False, 87), -4), (T["half"], flow_snd(1.8, 88), -12), (T["fish"], sfx.womp(), -8),
               (T["happy"], sfx.alarm(3, 820), -11)]
        ev += [(T["pipe2"] - 0.1, sfx.whoosh(1.0, True, 89), -8), (T["spray"], sfx.hiss(1.2, 90), -10), (T["mixes"] + 0.3, sfx.chime(), -6)]
        ev += [(s("cta") - 0.12, sfx.whoosh(0.4, True, 91), -6), (T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(T["run"], sfx.whoosh(1.4, False, 94), -9), (T["miles"], sfx.riser(1.0, 95), -12), (T["tap"], water_snd(1.2, 96), -8)]
        ev += [(T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3), (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"], sfx.pop(100), -2), (T["cong2"], sfx.sparkle(1.0, 14, 101), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 102), -6), (T["fish2"], sfx.pop(103), -8), (T["saltier"], sfx.sizzle(0.6, 104), -10),
               (T["gamer"], sfx.pop(105), -9), (T["lost"], sfx.womp(), -5), (T["lost"] + 0.05, sfx.thud(0.4, 106), -6)]
        return ev


NAME = "desal"
EPISODE = Desal
