"""Episode 43 - The Great Wall of China.  v2 look: dusk over ridge after ridge of mountains, a pale stone wall snaking
along the crests with its watchtowers; a desert wall of rammed earth; a brick wall glued with sticky rice soup; beacon
towers passing smoke down the line.

Sets: ridge (hook: the wall draws itself along three ranges of mountains, an Earth inset shows it would wrap more than
halfway round, a steaming bowl of rice soup; the reveal: every tower lights a beacon, "wolf smoke"; the stat; the
closer), plain (break1: riders on fast horses sweep across flat grassland at a farm; fix1: the wall on a mountain crest,
the riders stop at the foot of the cliffs), gobi (break2: a desert with no stone and no wood; fix2: soil rammed in a
wooden frame layer by layer, then reeds stacked with gravel, then the same wall weathered after 2,000 years), mortar
(break3: a Ming brick wall in the rain, the plain lime mortar crumbles; fix3: sticky rice soup stirred and poured into
the lime, tight crystals, the rain rolls off), beacon (break4: raiders at one end of a long wall, the army days away;
fix4: towers light smoke one after another down to the army camp; one smoke = 100 raiders, five = 10,000; the cta),
chat (the tag: a phone, your message "Seen" since yesterday, no reply, while beacon smoke races along a ridge).
World (ridge, plain, beacon): side view, x along the range, y down (up is negative), the plain's ground is y = 0.
"""
from v2_base import *  # noqa: F401,F403
from panama import rain  # noqa: E402

DUSK = {"top": "#0A1030", "upper": "#231F5C", "mid": "#5C3A78", "low": "#C2666A", "horizon": "#F3A46C",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
DESERT = {"top": "#3B1F2E", "upper": "#7A3B3A", "mid": "#C0663E", "low": "#EFA45C", "horizon": "#FFD28A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
RAINY = {"top": "#0B1226", "upper": "#1C2742", "mid": "#33415E", "low": "#56617A", "horizon": "#7C8194",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STONE, STONE_L, STONE_D = "#CDBB98", "#EFE2C2", "#7F6D56"
BRICK, BRICK_D = "#9E8466", "#5F4B39"
GRASS, GRASS_D = "#55743A", "#2B3F1E"
SAND, SAND_D = "#D9A35E", "#9C6A33"
EARTH, EARTH_D = "#B8865A", "#7A5432"
SMOKE = "#CFC9BF"
NEAR_TOWERS = (-1180.0, -820.0, -470.0, -120.0, 230.0, 590.0, 950.0, 1300.0)


def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def crest(x, seed=0, base=-380.0, amp=1.0):
    """Height of a mountain crest at x (world y, up is negative)."""
    k = (0.0, 1.7, 3.1)[seed % 3]
    return base - amp * (150 * math.sin(x / 300.0 + 0.6 + k) + 70 * math.sin(x / 113.0 + 1.3 + 2 * k)
                         + 26 * math.sin(x / 47.0 + k))


def poly_y(pts, x):
    """Linear interpolation of y along a polyline sorted by x."""
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return lerp(y0, y1, (x - x0) / max(1e-6, x1 - x0))
    return pts[-1][1]


def mountain(c, fn, x0, x1, top, bottom, depth=2600.0, a=1.0, step=12.0):
    """Fill under a crest function from x0 to x1."""
    p = skia.Path()
    p.moveTo(x0, depth)
    x = x0
    while x <= x1:
        p.lineTo(x, fn(x))
        x += step
    p.lineTo(x1, fn(x1))
    p.lineTo(x1, depth)
    p.close()
    ymin = min(fn(x0 + (x1 - x0) * i / 40.0) for i in range(41))
    c.drawPath(p, lin_paint(0, ymin, 0, ymin + 900, [top, bottom], a=a))


def tower(c, x, y, w, h, a=1.0, lit=1.0, fire=0.0, t=0.0):
    """A watchtower standing on (x, y): stone block, two arched windows, crenellated top, an optional beacon fire."""
    if a <= 0:
        return
    body = R(x - w / 2, y - h, w, h + 8)
    c.drawRect(body, lin_paint(x - w / 2, 0, x + w / 2, 0, [mix(STONE_L, STONE, 1 - lit), STONE, STONE_D], a=a))
    c.drawRect(R(x - w / 2 - w * 0.06, y - h - w * 0.08, w * 1.12, w * 0.1), P(STONE_L, a))
    mw = w * 1.12 / 5.0
    for i in range(5):
        if i % 2 == 0:
            c.drawRect(R(x - w / 2 - w * 0.06 + i * mw, y - h - w * 0.26, mw, w * 0.2), P(STONE, a))
    for k in (-1, 1):
        wx, wy = x + k * w * 0.22, y - h * 0.55
        win = skia.Path()
        win.moveTo(wx - w * 0.09, wy + h * 0.16)
        win.lineTo(wx - w * 0.09, wy)
        win.arcTo(R(wx - w * 0.09, wy - w * 0.09, w * 0.18, w * 0.18), 180, 180, False)
        win.lineTo(wx + w * 0.09, wy + h * 0.16)
        win.close()
        c.drawPath(win, P("#2A2230", a))
        if fire > 0:
            c.drawPath(win, P("#FFB45C", 0.7 * fire * a))
    c.drawLine(x - w / 2, y - h * 0.18, x + w / 2, y - h * 0.18, P(STONE_D, 0.5 * a, stroke=max(1.0, w * 0.03)))
    if fire > 0:
        fx_, fy_ = x, y - h - w * 0.3
        add_glow(c, fx_, fy_, w * 1.6, "#FF8A3D", 0.55 * fire * a)
        fl = skia.Path()
        fh = w * 0.55 * (0.8 + 0.2 * math.sin(t * 17 + x))
        fl.moveTo(fx_ - w * 0.18, fy_ + w * 0.06)
        fl.quadTo(fx_ - w * 0.12, fy_ - fh * 0.6, fx_, fy_ - fh)
        fl.quadTo(fx_ + w * 0.12, fy_ - fh * 0.6, fx_ + w * 0.18, fy_ + w * 0.06)
        fl.close()
        c.drawPath(fl, lin_paint(0, fy_, 0, fy_ - fh, ["#FF7A1A", "#FFD27A"], a=fire * a))


def wall_on(c, fn, x0, x1, u=1.0, wh=34.0, a=1.0, step=12.0, lit=1.0):
    """The wall following a crest from x0 toward x1, drawn up to fraction u: a pale band with a lit walkway,
    crenellations and a shadow line."""
    if u <= 0.001 or a <= 0:
        return
    xe = lerp(x0, x1, clamp(u))
    n = max(2, int(abs(xe - x0) / step) + 1)
    xs = [lerp(x0, xe, i / (n - 1.0)) for i in range(n)]
    top = [(x, fn(x) - wh) for x in xs]
    bot = [(x, fn(x) + wh * 0.25) for x in xs]
    body = skia.Path()
    body.moveTo(*top[0])
    for p_ in top[1:]:
        body.lineTo(*p_)
    for p_ in reversed(bot):
        body.lineTo(*p_)
    body.close()
    c.drawPath(body, P(mix(STONE_D, STONE, lit), a))
    mid = skia.Path()
    mid.moveTo(xs[0], fn(xs[0]) - wh * 0.45)
    for x in xs[1:]:
        mid.lineTo(x, fn(x) - wh * 0.45)
    c.drawPath(mid, P(STONE_D, 0.35 * a, stroke=max(1.0, wh * 0.06)))
    tp = skia.Path()
    tp.moveTo(*top[0])
    for p_ in top[1:]:
        tp.lineTo(*p_)
    c.drawPath(tp, P(mix(STONE, STONE_L, lit), a, stroke=max(1.5, wh * 0.22)))
    gap = wh * 0.55
    x = x0
    sgn = 1 if xe >= x0 else -1
    while (x - xe) * sgn < 0:
        yy = fn(x) - wh
        c.drawRect(R(x - gap * 0.32, yy - wh * 0.34, gap * 0.64, wh * 0.36), P(mix(STONE, STONE_L, lit * 0.6), a))
        x += gap * sgn
    bp = skia.Path()
    bp.moveTo(*bot[0])
    for p_ in bot[1:]:
        bp.lineTo(*p_)
    c.drawPath(bp, P("#140F1C", 0.5 * a, stroke=max(1.0, wh * 0.12)))


def smoke_col(c, x, y, t, t0, s=1.0, a=1.0, seed=1, n=1, gap=40.0):
    """n beacon smoke columns rising from (x, y), started at t0."""
    if t < t0 or a <= 0:
        return
    for k in range(n):
        ox = x + (k - (n - 1) / 2.0) * gap * s
        v2.smoke(c, ox, y, t, t0 + k * 0.06, rate=9, life=2.4, spread=(14 * s, -40 * s), rise=-120 * s,
                 size=(10 * s, 46 * s), col=SMOKE, lit="#FF9A4A", lit_until=0.5, seed=seed + k * 13, a=0.9 * a, drag=0.8)


def horse(c, x, y, s, ph, a=1.0, face=-1, rear=0.0, coat="#3A2A22", rider="#B91C1C", flag=True):
    """A galloping horse with a rider, hooves at (x, y). ph: gallop phase in radians. face -1 runs left."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s * (-1 if face < 0 else 1), s)
    if rear > 0:
        c.translate(-50, 0)
        c.rotate(-28 * rear)
        c.translate(50, 0)
    bob = math.sin(ph * 2) * 4
    c.translate(0, bob)
    col = P(coat, a)
    for i, (hx, off) in enumerate(((-42, 0.0), (-30, 1.3), (34, 2.6), (46, 3.9))):
        ang = math.sin(ph + off) * (0.55 if rear <= 0 else 0.2) + (0.6 * rear if i >= 2 else 0)
        kx, ky = hx + math.sin(ang) * 30, -62 + math.cos(ang) * 30
        ang2 = ang + (0.6 + 0.5 * math.sin(ph + off + 1.2))
        fx_, fy_ = kx + math.sin(ang2) * 30, ky + math.cos(ang2) * 30
        lc = coat if i % 2 else shade(coat, -0.2)
        c.drawLine(hx, -86, kx, ky, P(lc, a, stroke=13))
        c.drawLine(kx, ky, fx_, fy_, P(lc, a, stroke=9))
        c.drawRect(R(fx_ - 6, fy_ - 3, 13, 7), P("#141014", a))
    c.drawOval(R(-70, -122, 140, 58), col)
    neck = skia.Path()
    neck.moveTo(34, -116)
    neck.lineTo(70, -160)
    neck.lineTo(94, -150)
    neck.lineTo(66, -92)
    neck.close()
    c.drawPath(neck, col)
    c.save()
    c.translate(92, -156)
    c.rotate(28)
    c.drawOval(R(-12, -14, 50, 26), col)
    c.restore()
    c.drawCircle(96, -160, 3.5, P("#F8FAFC", 0.9 * a))
    mane = skia.Path()
    mane.moveTo(40, -122)
    mane.quadTo(52, -170 + math.sin(ph) * 4, 78, -168)
    c.drawPath(mane, P("#1A120E", a, stroke=9))
    tail = skia.Path()
    tail.moveTo(-68, -108)
    tail.quadTo(-104, -112 + math.sin(ph * 2) * 10, -118, -78)
    c.drawPath(tail, P("#1A120E", a, stroke=12))
    c.drawRRect(rr(-14, -176, 30, 58, 12), P(rider, a))
    c.drawCircle(4, -192, 15, P("#C98E62", a))
    c.drawRRect(rr(-14, -212, 36, 14, 6), P("#3F2A1A", a))
    c.drawLine(2, -160, 54, -150, P(rider, a, stroke=9))
    c.drawLine(-6, -126, 14, -92, P("#2B1E16", a, stroke=10))
    if flag:
        c.drawLine(-10, -150, -26, -268, P("#6B4F2A", a, stroke=5))
        fp = skia.Path()
        fy0 = -268
        fp.moveTo(-26, fy0)
        fp.quadTo(-56, fy0 + 6 + math.sin(ph * 2) * 6, -84, fy0 + 2)
        fp.lineTo(-80, fy0 + 30)
        fp.quadTo(-54, fy0 + 34 + math.sin(ph * 2 + 1) * 6, -24, fy0 + 30)
        fp.close()
        c.drawPath(fp, P("#F59E0B", a))
    c.restore()


def house_cn(c, x, y, w, h, a=1.0, lit=0.6, roof="#5B2A2A"):
    """A farmhouse with a curved, upturned roof."""
    c.drawRect(R(x - w / 2, y - h, w, h), P("#C9A57A", a))
    c.drawRect(R(x - w * 0.12, y - h * 0.6, w * 0.24, h * 0.6), P("#4A2E1E", a))
    c.drawRect(R(x - w * 0.4, y - h * 0.75, w * 0.16, h * 0.22), P("#FDE68A", lit * a))
    c.drawRect(R(x + w * 0.24, y - h * 0.75, w * 0.16, h * 0.22), P("#FDE68A", lit * a))
    rf = skia.Path()
    rf.moveTo(x - w * 0.72, y - h - h * 0.02)
    rf.quadTo(x - w * 0.5, y - h + h * 0.08, x - w * 0.36, y - h * 1.5)
    rf.lineTo(x + w * 0.36, y - h * 1.5)
    rf.quadTo(x + w * 0.5, y - h + h * 0.08, x + w * 0.72, y - h - h * 0.02)
    rf.close()
    c.drawPath(rf, P(roof, a))
    c.drawLine(x - w * 0.36, y - h * 1.5, x + w * 0.36, y - h * 1.5, P(shade(roof, 0.25), a, stroke=6))


def tent(c, x, y, s, a=1.0, col="#E5E7EB"):
    tp = skia.Path()
    tp.moveTo(x - 60 * s, y)
    tp.lineTo(x, y - 80 * s)
    tp.lineTo(x + 60 * s, y)
    tp.close()
    c.drawPath(tp, P(col, a))
    c.drawLine(x, y - 80 * s, x, y - 104 * s, P("#6B4F2A", a, stroke=4 * s))
    c.drawRect(R(x, y - 104 * s, 22 * s, 12 * s), P("#DC2626", a))
    door = skia.Path()
    door.moveTo(x - 14 * s, y)
    door.lineTo(x, y - 34 * s)
    door.lineTo(x + 14 * s, y)
    door.close()
    c.drawPath(door, P("#374151", a))


def bowl(c, x, y, s, t, a=1.0, steam=1.0, tilt=0.0):
    """A steaming bowl of sticky rice soup."""
    c.save()
    c.translate(x, y)
    c.rotate(tilt)
    c.scale(s, s)
    c.drawOval(R(-120, -34, 240, 40), P("#F8FAFC", a))
    for i in range(26):
        rx = -100 + (i * 37) % 200
        ry = -24 + (i * 13) % 18
        c.drawOval(R(rx, ry, 14, 7), P("#E7E2D3", a))
    b = skia.Path()
    b.moveTo(-128, -16)
    b.quadTo(-120, 90, 0, 96)
    b.quadTo(120, 90, 128, -16)
    b.close()
    c.drawPath(b, lin_paint(-128, 0, 128, 0, ["#1D4ED8", "#60A5FA", "#1E3A8A"], a=a))
    c.drawPath(b, P("#DBEAFE", 0.9 * a, stroke=4))
    for k in range(3):
        c.drawArc(R(-84 + k * 56, 18, 46, 30), 0, 180, False, P("#DBEAFE", 0.7 * a, stroke=4))
    c.drawRect(R(-38, 92, 76, 14), P("#1E3A8A", a))
    c.restore()
    if steam > 0:
        for k in range(3):
            q = (t * 0.7 + k / 3.0) % 1.0
            sx = x + (k - 1) * 60 * s + math.sin(t * 3 + k) * 12 * s
            sp = skia.Path()
            sp.moveTo(sx, y - 40 * s)
            sp.quadTo(sx + 30 * s, y - (90 + q * 60) * s, sx, y - (150 + q * 80) * s)
            c.drawPath(sp, P("#F8FAFC", 0.45 * steam * a * math.sin(q * math.pi), stroke=10 * s))


def earth_globe(c, x, y, r, k, a=1.0, t=0.0):
    """The Earth with a yellow line wrapping k of the way round it (k > 0.5: more than halfway)."""
    add_glow(c, x, y, r * 1.6, "#60A5FA", 0.35 * a)
    c.drawCircle(x, y, r, rad_paint(x - r * 0.35, y - r * 0.35, r * 1.4, ["#93C5FD", "#2563EB", "#1E3A8A"], a=a))
    c.save()
    clip = skia.Path()
    clip.addCircle(x, y, r)
    c.clipPath(clip, doAntiAlias=True)
    rng = random.Random(3)
    for i in range(7):
        cx_ = x + ((rng.uniform(-1, 1) * r + t * 20) % (2 * r)) - r
        cy_ = y + rng.uniform(-0.7, 0.7) * r
        c.drawOval(R(cx_ - r * 0.28, cy_ - r * 0.16, r * rng.uniform(0.35, 0.6), r * rng.uniform(0.2, 0.34)), P("#34D399", a))
    c.restore()
    c.drawCircle(x, y, r, P("#BFDBFE", 0.5 * a, stroke=3))
    if k > 0:
        c.drawArc(R(x - r * 1.14, y - r * 1.14, r * 2.28, r * 2.28), 180, 360 * k, False, P("#FACC15", a, stroke=r * 0.14))
        ang = math.radians(180 + 360 * k)
        add_glow(c, x + math.cos(ang) * r * 1.14, y + math.sin(ang) * r * 1.14, r * 0.3, "#FDE68A", 0.8 * a)
        c.drawLine(x - r * 1.3, y, x + r * 1.3, y, P("#F8FAFC", 0.5 * a * prog(k, 0.4, 0.5), stroke=3))


def wok(c, x, y, s, t, stir=0.0, a=1.0, fire=1.0, fill="#F1EEE4"):
    """A big pot of sticky rice soup on a fire, a paddle stirring it."""
    if a <= 0:
        return
    if fire > 0:
        for k in range(5):
            fh = (40 + 18 * math.sin(t * 13 + k * 1.7)) * s
            fl = skia.Path()
            fx_ = x + (k - 2) * 34 * s
            fl.moveTo(fx_ - 16 * s, y + 70 * s)
            fl.quadTo(fx_, y + 70 * s - fh * 1.4, fx_ + 16 * s, y + 70 * s)
            c.drawPath(fl, lin_paint(0, y + 70 * s, 0, y + 70 * s - fh, ["#FF6A1A", "#FFD27A"], a=fire * a))
        add_glow(c, x, y + 50 * s, 160 * s, "#FF8A3D", 0.4 * fire * a)
    c.drawOval(R(x - 150 * s, y - 26 * s, 300 * s, 50 * s), P(fill, a))
    pot = skia.Path()
    pot.moveTo(x - 160 * s, y - 6 * s)
    pot.quadTo(x - 150 * s, y + 70 * s, x, y + 76 * s)
    pot.quadTo(x + 150 * s, y + 70 * s, x + 160 * s, y - 6 * s)
    pot.close()
    c.drawPath(pot, lin_paint(x - 160 * s, 0, x + 160 * s, 0, ["#1F2937", "#4B5563", "#111827"], a=a))
    c.drawLine(x - 170 * s, y - 6 * s, x + 170 * s, y - 6 * s, P("#6B7280", a, stroke=8 * s))
    ang = math.radians(-60 + 40 * math.sin(stir * 6.0))
    px, py = x + math.cos(ang) * 60 * s, y - 10 * s
    c.drawLine(px, py, px + math.cos(ang - 1.2) * 190 * s, py - 190 * s, P("#A16207", a, stroke=12 * s))
    for k in range(3):
        q = (t * 0.6 + k / 3.0) % 1.0
        sx = x + (k - 1) * 70 * s
        sp = skia.Path()
        sp.moveTo(sx, y - 30 * s)
        sp.quadTo(sx + 26 * s, y - (80 + q * 50) * s, sx, y - (140 + q * 60) * s)
        c.drawPath(sp, P("#F8FAFC", 0.4 * a * math.sin(q * math.pi), stroke=10 * s))


def crystals(c, x, y, r, tight, a=1.0):
    """A magnifier circle: loose big crystals (tight 0) or small packed ones (tight 1)."""
    c.drawCircle(x, y, r, P("#0B1220", 0.92 * a))
    c.save()
    clip = skia.Path()
    clip.addCircle(x, y, r)
    c.clipPath(clip, doAntiAlias=True)
    rng = random.Random(7)
    if tight < 0.5:
        for i in range(22):
            cx_, cy_ = x + rng.uniform(-r, r), y + rng.uniform(-r, r)
            sz = rng.uniform(r * 0.18, r * 0.3)
            pp = skia.Path()
            for k in range(6):
                an = k * math.pi / 3 + i
                (pp.moveTo if k == 0 else pp.lineTo)(cx_ + math.cos(an) * sz, cy_ + math.sin(an) * sz * 0.8)
            pp.close()
            c.drawPath(pp, P("#CBD5E1", 0.85 * a))
        for i in range(10):
            c.drawLine(x + rng.uniform(-r, r), y + rng.uniform(-r, r), x + rng.uniform(-r, r), y + rng.uniform(-r, r),
                       P("#0B1220", a, stroke=6))
    else:
        for i in range(170):
            cx_, cy_ = x + rng.uniform(-r, r), y + rng.uniform(-r, r)
            c.drawCircle(cx_, cy_, rng.uniform(r * 0.05, r * 0.09), P(rng.choice(["#F8FAFC", "#E2E8F0", "#FDE68A"]), 0.95 * a))
    c.restore()
    c.drawCircle(x, y, r, P("#E2E8F0", a, stroke=10))
    c.drawLine(x + r * 0.72, y + r * 0.72, x + r * 1.25, y + r * 1.25, P("#E2E8F0", a, stroke=18))


def phone_chat(c, x, y, w, h, t, a, mine, seen, typing=0.0, rtl=False, k_seen=1.0):
    """A big phone with one sent message, its 'seen' line and nothing else."""
    c.drawRRect(rr(x - w / 2 - 14, y - 14, w + 28, h + 28, 56), P("#0B0F1A", a))
    c.drawRRect(rr(x - w / 2 - 14, y - 14, w + 28, h + 28, 56), P("#475569", a, stroke=4))
    c.drawRRect(rr(x - w / 2, y, w, h, 44), lin_paint(0, y, 0, y + h, ["#111B2E", "#0B1220"], a=a))
    c.drawRRect(rr(x - 70, y + 16, 140, 26, 13), P("#0B0F1A", a))
    c.drawRect(R(x - w / 2, y + 60, w, 90), P("#1E293B", a))
    c.drawCircle(x - w / 2 + 70 if not rtl else x + w / 2 - 70, y + 105, 30, P("#F59E0B", a))
    bw = min(w - 120, max(220, text_width(mine, 44, "Poppins-Bold") + 70)) if not arabic.is_ar(mine) else min(w - 120, arabic.width_ar(mine, 50, "Tajawal-Bold") + 70)
    bx = x + w / 2 - 40 - bw if not rtl else x - w / 2 + 40
    by = y + 260
    c.drawRRect(rr(bx, by, bw, 96, 34), P("#2563EB", a))
    if arabic.is_ar(mine):
        arabic.text_ar(c, mine, bx + bw / 2, by + 64, 50, "#FFFFFF", "Tajawal-Bold", a=a)
    else:
        text(c, mine, bx + bw / 2, by + 64, 44, "#FFFFFF", "Poppins-Bold", a=a)
    ka = a * k_seen
    if ka > 0:
        sy = by + 150
        if arabic.is_ar(seen):
            arabic.text_ar(c, seen, bx + bw / 2, sy, 36, "#94A3B8", "Tajawal-Bold", a=ka)
        else:
            text(c, seen, bx + bw / 2, sy, 32, "#94A3B8", "Poppins-SemiBold", a=ka)
        cx_ = bx + bw - 40 if not rtl else bx + 40
        for d in (0, 16):
            c.drawLine(cx_ - 30 + d, by + 112, cx_ - 20 + d, by + 124, P("#38BDF8", ka, stroke=5))
            c.drawLine(cx_ - 20 + d, by + 124, cx_ + d, by + 102, P("#38BDF8", ka, stroke=5))
    if typing > 0:
        tx_ = x - w / 2 + 40 if not rtl else x + w / 2 - 190
        c.drawRRect(rr(tx_, y + 520, 150, 80, 34), P("#334155", typing * a))
        for d in range(3):
            q = 0.5 + 0.5 * math.sin(t * 9 - d)
            c.drawCircle(tx_ + 40 + d * 35, y + 560, 10, P("#CBD5E1", (0.5 + 0.5 * q) * typing * a))


# ====================================================================================== the episode
class GreatWall(EpisodeV2):
    BUILD_NO = 43
    FIRST_SET = "ridge"
    CLEAR = "#0A1030"
    TITLE = {"en": "GREAT WALL OF CHINA", "ar_sa": "سور الصين العظيم"}
    EMPH = {"en": ["CONGRATS", "WALL", "HALFWAY", "EARTH", "RICE", "SOUP", "GREAT", "CHINA", "RAIDERS", "FAST",
                   "HORSES", "NORTH", "FLAT", "STOP", "RIDGES", "MOUNTAIN", "CHARGE", "GOBI", "DESERT", "STONE",
                   "WOOD", "POUND", "LAYERS", "REEDS", "GRAVEL", "STANDS", "THOUSAND", "CENTURIES", "REBUILT", "BRICK", "LIME",
                   "MORTAR", "CRUMBLES", "RAIN", "STIR", "STICKY", "STARCH", "TIGHT", "ROLLS", "LONG", "USELESS",
                   "ARMY", "DAYS", "BEACON", "TOWERS", "SIGHT", "SMOKE", "HUNDRED", "FIVE", "FOLLOW", "OMANI",
                   "FALAJ", "WOLF", "WOLVES", "COMING", "KILOMETERS", "YEARS", "MOON", "ZERO", "YOURSELF",
                   "FRIEND", "MESSAGE", "YESTERDAY", "REPLIED"],
            "ar_sa": ["مبروك", "سور", "نص", "الأرض", "بشوربة", "رز", "الصين", "العظيم", "الغزاة", "خيل", "الشمال",
                      "والسهل", "يوقفهم", "قمم", "الجبال", "تطلع", "غوبي", "حجر", "خشب", "فتدك", "طبقة", "قصب",
                      "حصى", "واقف", "ألفين", "مينغ", "طوب", "الجير", "يتفتت", "المطر", "فتخلط", "والنشا", "يشد",
                      "يزحلق", "بهالطول", "ينفع", "الجيش", "أيام", "أبراج", "تشوف", "دخانة", "مية", "وخمس",
                      "آلاف", "تابعني", "فلج", "عماني", "اربط", "يسمون", "الذيب", "وعشرين", "كيلو", "القمر",
                      "صفر", "بيدك", "الدخان", "وخويك", "رسالتك", "أمس", "رد"]}
    KEYS = {"ar_sa": {
        ("hook", "BUILD"): "بنيت", ("hook", "HALFWAY"): "نص", ("hook", "EARTH"): "الأرض", ("hook", "RICE"): "رز",
        ("hook", "CONGRATS"): "مبروك", ("hook", "GREAT"): "الصين",
        ("break1", "RAIDERS"): "الغزاة", ("break1", "HORSES"): "خيل", ("break1", "NORTH"): "الشمال",
        ("break1", "FLAT"): "والسهل", ("break1", "STOP"): "يوقفهم",
        ("fix1", "MOUNTAIN"): "الجبال", ("fix1", "RIDGES"): "قمم", ("fix1", "CHARGE"): "تطلع",
        ("break2", "GOBI"): "غوبي", ("break2", "STONE"): "حجر", ("break2", "WOOD"): "خشب",
        ("fix2", "POUND"): "فتدك", ("fix2", "LAYERS"): "طبقة", ("fix2", "REEDS"): "قصب", ("fix2", "GRAVEL"): "حصى",
        ("fix2", "STANDS"): "واقف", ("fix2", "THOUSAND"): "ألفين",
        ("break3", "CENTURIES"): "مينغ", ("break3", "BRICK"): "طوب", ("break3", "CRUMBLES"): "يتفتت",
        ("break3", "RAIN"): "المطر",
        ("fix3", "STIR"): "فتخلط", ("fix3", "RICE"): "رز", ("fix3", "STARCH"): "والنشا", ("fix3", "TIGHT"): "يشد",
        ("fix3", "ROLLS"): "يزحلق",
        ("break4", "LONG"): "بهالطول", ("break4", "USELESS"): "ينفع", ("break4", "ARMY"): "الجيش",
        ("break4", "DAYS"): "أيام",
        ("fix4", "BEACON"): "أبراج", ("fix4", "SIGHT"): "تشوف", ("fix4", "ONE"): "دخانة", ("fix4", "HUNDRED"): "مية",
        ("fix4", "FIVE"): "وخمس", ("fix4", "THOUSAND"): "آلاف",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "JOIN"): "اربط", ("reveal", "CALL"): "يسمون", ("reveal", "WOLF"): "الذيب",
        ("reveal", "WOLVES"): "الذيب",
        ("stat", "TWENTY"): "واحد", ("stat", "TWO"): "ألفين", ("stat", "MOON"): "القمر", ("stat", "ZERO"): "صفر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SMOKE"): "الدخان", ("tag", "FRIEND"): "وخويك", ("tag", "SAW"): "شاف", ("tag", "YESTERDAY"): "أمس",
        ("tag", "REPLIED"): "رد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an Omani falaj"),
                   "stat": [("21,196", "KM OF WALL"), ("2,000+", "YEARS OF BUILDING"), ("0", "SEEN FROM THE MOON")],
                   "L": {"km": "21,196 km", "half": "MORE THAN HALFWAY ROUND", "rice": "GLUED WITH RICE SOUP",
                         "name": "THE GREAT WALL OF CHINA", "raiders": "RAIDERS ON FAST HORSES",
                         "north": "FROM THE NORTH", "flat": "FLAT LAND CAN'T STOP THEM", "ridges": "ON THE RIDGES",
                         "charge": "NO HORSE CAN CHARGE UP HERE", "gobi": "GOBI DESERT", "nostone": "NO STONE",
                         "nowood": "NO WOOD", "pound": "POUND THE EARTH", "layers": "LAYER BY LAYER",
                         "reeds": "REEDS + GRAVEL", "years": "2,000 YEARS LATER", "ming": "MING BRICK WALL",
                         "lime": "PLAIN LIME MORTAR", "crumble": "IT CRUMBLES IN THE RAIN", "stir": "STICKY RICE SOUP",
                         "into": "+ LIME", "loose": "LOOSE", "tight": "PACKED TIGHT", "rolls": "RAIN ROLLS OFF",
                         "long": "THOUSANDS OF KM", "army": "THE ARMY", "days": "DAYS AWAY",
                         "beacon": "BEACON TOWERS", "sight": "IN SIGHT OF EACH OTHER", "one": "1 SMOKE = 100 RAIDERS",
                         "five": "5 SMOKES = 10,000", "join": "SEA TO DESERT", "wolf": "WOLF SMOKE",
                         "wolves": "THE WOLVES ARE COMING!", "msg": "u there?", "seen": "Seen yesterday",
                         "provinces": "ACROSS PROVINCES", "nothing": "...still nothing"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: فلج عماني"),
                      "stat": [("21,196", "كيلو سور"), ("2,000+", "سنة بناء"), ("0", "من القمر")],
                      "L": {"km": "21,196 كيلو", "half": "أكثر من نص الأرض", "rice": "ملصوق بشوربة رز",
                            "name": "سور الصين العظيم", "raiders": "غزاة على خيل",
                            "north": "من الشمال", "flat": "السهل ما يوقفهم", "ridges": "فوق القمم",
                            "charge": "ولا خيل تطلع هنا", "gobi": "صحرا غوبي", "nostone": "لا حجر",
                            "nowood": "ولا خشب", "pound": "دك التراب", "layers": "طبقة فوق طبقة",
                            "reeds": "قصب + حصى", "years": "واقف من ألفين سنة", "ming": "سور مينغ بالطوب",
                            "lime": "جير بروحه", "crumble": "يتفتت مع المطر", "stir": "شوربة رز",
                            "into": "+ جير", "loose": "مفكوك", "tight": "مشدود", "rolls": "المطر يزحلق",
                            "long": "آلاف الكيلوات", "army": "الجيش", "days": "بعيد أيام",
                            "beacon": "أبراج الإنذار", "sight": "تشوف بعض", "one": "دخانة = 100 غازي",
                            "five": "5 دخانات = 10,000", "join": "من البحر للصحرا", "wolf": "دخان الذيب",
                            "wolves": "جاكم الذيب!", "msg": "وينك؟", "seen": "شافها أمس",
                            "provinces": "من برج لبرج", "nothing": "وللحين ما رد"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "build": ("hook", "BUILD", 0.05), "halfway": ("hook", "HALFWAY", 0.3), "earth": ("hook", "EARTH", 0.42),
            "rice": ("hook", "RICE", 0.55), "congrats": ("hook", "CONGRATS", 0.72), "great": ("hook", "GREAT", 0.86),
            "raiders": ("break1", "RAIDERS", 0.1), "horses": ("break1", "HORSES", 0.3), "north": ("break1", "NORTH", 0.55),
            "flat": ("break1", "FLAT", 0.7), "stop": ("break1", "STOP", 0.9),
            "mountain": ("fix1", "MOUNTAIN", 0.35), "ridges": ("fix1", "RIDGES", 0.45), "charge": ("fix1", "CHARGE", 0.9),
            "gobi": ("break2", "GOBI", 0.35), "stone": ("break2", "STONE", 0.7), "wood": ("break2", "WOOD", 0.92),
            "pound": ("fix2", "POUND", 0.08), "layers": ("fix2", "LAYERS", 0.3), "reeds": ("fix2", "REEDS", 0.45),
            "gravel": ("fix2", "GRAVEL", 0.55), "stands": ("fix2", "STANDS", 0.7), "thousand": ("fix2", "THOUSAND", 0.85),
            "ming": ("break3", "CENTURIES", 0.1), "brick": ("break3", "BRICK", 0.4), "crumbles": ("break3", "CRUMBLES", 0.75),
            "rain": ("break3", "RAIN", 0.92),
            "stir": ("fix3", "STIR", 0.1), "rice2": ("fix3", "RICE", 0.25), "starch": ("fix3", "STARCH", 0.55),
            "tight": ("fix3", "TIGHT", 0.7), "rolls": ("fix3", "ROLLS", 0.92),
            "long": ("break4", "LONG", 0.3), "useless": ("break4", "USELESS", 0.5), "army": ("break4", "ARMY", 0.75),
            "days": ("break4", "DAYS", 0.9),
            "beacon": ("fix4", "BEACON", 0.15), "sight": ("fix4", "SIGHT", 0.3), "one": ("fix4", "ONE", 0.5),
            "hundred": ("fix4", "HUNDRED", 0.65), "five": ("fix4", "FIVE", 0.78), "tenk": ("fix4", "THOUSAND", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "join": ("reveal", "JOIN", 0.1), "call": ("reveal", "CALL", 0.4), "wolf": ("reveal", "WOLF", 0.65),
            "wolves": ("reveal", "WOLVES", 0.88),
            "s1": ("stat", "TWENTY", 0.04), "s2": ("stat", "TWO", 0.35), "moon": ("stat", "MOON", 0.62),
            "s3": ("stat", "ZERO", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "smoke": ("tag", "SMOKE", 0.1), "friend": ("tag", "FRIEND", 0.45), "saw": ("tag", "SAW", 0.55),
            "yesterday": ("tag", "YESTERDAY", 0.7), "replied": ("tag", "REPLIED", 0.92)})
        T["fall"] = max(T["crumbles"] + 0.15, s("break3") + 0.5)
        T["relay"] = max(T["beacon"] - 0.1, s("fix4") + 0.05)
        self.dt_relay = clamp((T["one"] - 0.35 - T["relay"]) / 9.0, 0.1, 0.26)
        T["camp"] = T["relay"] + 9 * self.dt_relay + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "plain", 1)
        self.cut(s("break2") - 0.12, "gobi", -1)
        self.cut(s("break3") - 0.12, "mortar", 1)
        self.cut(s("break4") - 0.12, "beacon", -1)
        self.cut(s("reveal") - 0.12, "ridge", 1)
        self.cut(s("tag") - 0.2, "chat", -1)
        # ---- ridge camera: hook, reveal, stat, closer
        cm = Camera(-60, -440, 1.0)
        cm.key(0.05, 40, -430, 1.06, 3.2).key(T["congrats"], 0, -420, 1.0, 1.6)
        cm.key(s("reveal") - 0.12, 260, -400, 0.92, 0.0).key(s("reveal"), -160, -400, 0.92, max(1.0, s("stat") - s("reveal")))
        cm.key(s("stat") - 0.12, 0, -330, 0.86, 0.0)
        cm.key(s("closer") - 0.1, 210, -470, 1.32, 0.0).key(self.duration, 180, -470, 1.38, 2.5)
        self.cam = cm
        # ---- plain camera: break1 follows the riders over the flat, fix1 shows the mountain
        cp = Camera(2050, -120, 1.05)
        cp.key(s("break1"), 1100, -120, 1.05, max(0.8, s("fix1") - s("break1")))
        cp.key(s("fix1") - 0.12, -600, -300, 0.74, 0.0).key(s("fix1"), -560, -300, 0.78, max(0.8, s("break2") - s("fix1")))
        self.cam_plain = cp
        # ---- beacon camera: the raiders at the east end, then the relay west to the army camp
        cb = Camera(1000, -260, 0.8)
        cb.key(s("break4"), 900, -260, 0.82, 1.0)
        cb.key(T["relay"], -2950, -260, 0.82, 9 * self.dt_relay + 0.2)
        cb.key(T["one"] - 0.2, -2860, -150, 1.2, 0.6)
        self.cam_beacon = cb
        self.spans = [(T["stop"], T["charge"] + 0.3), (T["wood"], T["thousand"] + 0.3), (T["crumbles"], T["rolls"] + 0.3),
                      (T["days"], T["tenk"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 7), (T["horses"] + 0.2, 0.6, 7), (T["stop"], 0.4, 8), (T["charge"], 0.35, 8),
                       (T["pound"] + 0.1, 0.25, 6), (T["layers"] + 0.1, 0.25, 6), (T["fall"], 0.4, 9), (T["army"], 0.3, 6),
                       (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def ranges(self, c, t, cam, build=1.0, fire=None, haze=0.0):
        """Sky and three mountain ranges with the wall on every crest. build 0..1 grows the walls (near first);
        fire(layer, x) -> 0..1 lights a beacon on the tower at x."""
        cx, cy, z = cam
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.47)
        v2.stars(c, W, H, t, 0.6, dx=-cx * 0.01)
        add_glow(c, W * 0.62, H * 0.47, 520, "#FFB36B", 0.35)
        for i, (px, py, s_) in enumerate(((180, 330, 1.0), (760, 250, 0.8), (980, 430, 0.6))):
            v2.cloud(c, (px + t * 6 - cx * 0.02) % (W + 600) - 200, py, s_, body="#3B2F66", rim="#FF9D73", a=0.8, seed=i)
        layers = (
            (2, 0.30, 0.52, 330.0, ("#5B4A86", "#30295C"), 12.0, (24, 32), -300.0, 0.62),
            (1, 0.58, 0.72, -150.0, ("#34305F", "#1B1C40"), 20.0, (40, 54), -330.0, 0.82),
        )
        for li, par, zs, cy_l, cols, wh, (tw_, th_), base, amp in layers:
            fn = (lambda x, sd=li, b=base, am=amp: crest(x, sd, b, am))
            c.save()
            c.translate(W / 2, H / 2)
            c.scale(z * zs, z * zs)
            c.translate(-cx * par / zs, -cy_l)
            x0, x1 = -cx * par / zs - 1100 / (z * zs), -cx * par / zs + 1100 / (z * zs)
            mountain(c, fn, x0, x1, cols[0], cols[1], step=16.0)
            wb = clamp(build * 1.6 - (0.25 if li == 1 else 0.55))
            wall_on(c, fn, x0, x1, wb, wh=wh, step=10.0, lit=0.7)
            xs = [x0 + (x1 - x0) * (k + 0.5) / 7.0 for k in range(7)]
            for k, tx_ in enumerate(xs):
                if (tx_ - x0) / (x1 - x0) <= wb:
                    f_ = fire(li, tx_) if fire else 0.0
                    tower(c, tx_, fn(tx_), tw_, th_, lit=0.7, fire=f_, t=t)
                    if f_ > 0:
                        smoke_col(c, tx_, fn(tx_) - th_ - tw_ * 0.3, t, self._fire_t.get((li, k), t), s=0.5 + 0.3 * (li == 1),
                                  a=f_, seed=li * 31 + k)
            c.restore()
            c.drawRect(R(0, 0, W, H), lin_paint(0, H * 0.35, 0, H, ["#C2666A", "#231F5C"], a=0.10 + haze))
        self.view(c, cam)
        mountain(c, crest, cx - 700 / z, cx + 700 / z, "#21303A", "#0E161C")
        wall_on(c, crest, -1500, 1500, build, wh=38.0, step=11.0)
        for k, tx_ in enumerate(NEAR_TOWERS):
            if (tx_ + 1500) / 3000.0 <= build:
                f_ = fire(0, tx_) if fire else 0.0
                tower(c, tx_, crest(tx_), 84, 112, fire=f_, t=t)
                if f_ > 0:
                    smoke_col(c, tx_, crest(tx_) - 112 - 26, t, self._fire_t.get((0, k), t), s=1.0, a=f_, seed=k)
        c.restore()

    _fire_t = {}

    # ------------------------------------------------------------------ set: ridge (hook, reveal, stat, closer)
    def draw_ridge(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        hook = t < s("break1")
        build = lerp(0.28, 1.0, e_io(prog(t, 0.1, max(1.6, T["halfway"] - 0.2)))) if hook else 1.0
        fire = None
        if not hook and t >= s("reveal") - 0.12:
            t0 = T["join"] - 0.1
            self._fire_t = {}
            for li in range(3):
                for k in range(8):
                    self._fire_t[(li, k)] = t0 + k * 0.16 + li * 0.25

            def fire(li, x, t0=t0):
                u = (x - cam[0] * (1.0 if li == 0 else 0.6)) / 1800.0 + 0.5
                return prog(t, t0 + u * 1.3 + li * 0.25, t0 + u * 1.3 + li * 0.25 + 0.3)
        self.ranges(c, t, cam, build, fire)
        self.ui["cam"] = cam

    def ui_ridge(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            k = self.span(T["halfway"] - 0.15, T["rice"] - 0.05)
            if k > 0:
                gk = prog(tw, T["halfway"] - 0.1, T["earth"] + 0.5)
                c.drawRRect(rr(190, 470, 700, 640, 60), P("#0B1220", 0.9 * k))
                c.drawRRect(rr(190, 470, 700, 640, 60), P("#FACC15", 0.6 * k, stroke=4))
                earth_globe(c, 540, 770, 205, 0.53 * e_out(gk), a=k, t=tw)
                v2.chip(c, 540, 1050, self.L["half"], k, accent=HILITE, size=38)
                v2.chip(c, 540, 520, self.L["km"], self.span(T["earth"], T["rice"] - 0.05), accent="#FACC15", size=44)
            kb = self.span(T["rice"] - 0.1, T["great"] - 0.05)
            if kb > 0:
                c.drawRRect(rr(220, 500, 640, 560, 60), P("#0B1220", 0.9 * kb))
                c.drawRRect(rr(220, 500, 640, 560, 60), P("#FACC15", 0.6 * kb, stroke=4))
                bowl(c, 540, 800, 1.6 * e_back(clamp(kb)), tw, a=kb)
                v2.chip(c, 540, 1010, self.L["rice"], kb, accent=HILITE, size=40)
            self.chip(540, 420, "name", T["great"] - 0.1, s("break1") + 0.1, accent=HILITE, size=44)
            return
        if tw < s("stat") - 0.12:
            self.chip(540, 420, "join", T["join"] - 0.1, T["call"] - 0.1, accent="#FDE68A", size=40)
            k = self.span(T["call"] - 0.1, s("stat") - 0.15)
            if k > 0:
                v2.chip(c, 540, 420, self.L["wolf"], k, accent=WARN, size=48)
                wolf_icon(c, 540, 560, 1.1 * e_back(clamp(k)), tw, a=k, howl=prog(tw, T["wolf"], T["wolf"] + 0.4))
            self.chip(540, 690, "wolves", T["wolves"] - 0.15, s("stat") - 0.15, accent=HILITE, size=40)

    # ------------------------------------------------------------------ set: plain (break1, fix1)
    MTN = [(-1900, 0), (-1640, -360), (-1450, -540), (-1240, -650), (-1060, -700), (-900, -640), (-740, -690),
           (-580, -610), (-430, -420), (-300, -170), (-230, 0)]

    def mtn_y(self, x):
        return poly_y(self.MTN, x)

    def draw_plain(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam_plain.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 40)
        add_glow(c, W * 0.7, gy - 60, 520, "#FFB36B", 0.35)
        c.save()
        c.translate(W / 2 - cx * 0.12, gy - 10)
        v2.ridge(c, -1600, 1600, 0, 240, "#4B3F78", "#2E2A5C", seed=6, step=120, rough=0.5)
        c.restore()
        self.view(c, cam)
        c.drawRect(R(-2600, 0, 6400, 2600), lin_paint(0, 0, 0, 900, [GRASS, GRASS_D, "#16210F"]))
        rng = random.Random(5)
        for i in range(90):                                          # grass tufts
            gx_ = rng.uniform(-400, 3400)
            gy_ = rng.uniform(6, 600)
            c.drawLine(gx_, gy_, gx_ + rng.uniform(-6, 6), gy_ - rng.uniform(8, 20), P("#7A9A4E", 0.6, stroke=4))
        mp = skia.Path()                                             # the mountain with the wall on its crest
        mp.moveTo(self.MTN[0][0], 0)
        for x_, y_ in self.MTN:
            mp.lineTo(x_, y_)
        mp.lineTo(self.MTN[-1][0], 0)
        mp.close()
        c.drawPath(mp, lin_paint(0, -700, 0, 0, ["#46584A", "#1E2A22"]))
        c.save()
        c.clipPath(mp, doAntiAlias=True)
        for k in range(14):                                          # rock strata on the cliffs
            yy = -80 - k * 44
            c.drawLine(-1900, yy, -200, yy + 30, P("#14201A", 0.35, stroke=5))
        for k in range(9):                                           # sunlit faces
            x_ = -1700 + k * 170
            fp = skia.Path()
            fp.moveTo(x_, self.mtn_y(x_) + 10)
            fp.lineTo(x_ + 90, self.mtn_y(x_ + 90) + 10)
            fp.lineTo(x_ + 40, 0)
            fp.close()
            c.drawPath(fp, P("#6B7F5E", 0.25))
        c.restore()
        rim = skia.Path()
        rim.moveTo(*self.MTN[0])
        for p_ in self.MTN[1:]:
            rim.lineTo(*p_)
        c.drawPath(rim, P("#F3A46C", 0.35, stroke=8))
        fn = self.mtn_y
        wall_on(c, fn, -1640, -420, 1.0, wh=50.0, step=10.0)
        for tx_ in (-1240, -900, -580):
            tower(c, tx_, fn(tx_), 96, 130)
        for i, hx in enumerate((260, 450, 640)):                     # a farm on the flat land
            house_cn(c, hx, 0, 150, 100, lit=0.7)
        c.drawLine(140, -30, 760, -30, P("#7C5A3A", 0.8, stroke=6))
        for fx_ in range(140, 761, 60):
            c.drawLine(fx_, 0, fx_, -46, P("#7C5A3A", 0.9, stroke=6))
        fixed = t >= s("fix1") - 0.12
        for i in range(5):                                           # the raiders
            if not fixed:
                u = prog(t, s("break1") - 0.1 + i * 0.12, s("fix1") + 0.2)
                hx = lerp(1900 + i * 150, 760 + i * 140, u)
                rear = 0.0
            else:
                u = e_out(prog(t, s("fix1") - 0.12 + i * 0.1, T["charge"] - 0.1))
                hx = lerp(700 + i * 170, -160 + i * 120, u)
                rear = prog(t, T["charge"] - 0.4 + i * 0.05, T["charge"])
            hy = (30 + (i % 2) * 60) if not fixed else (10 + (i % 2) * 26)
            horse(c, hx, hy, 1.25 if not fixed else 1.1, t * 11 + i * 1.3, face=-1, rear=rear,
                  rider=("#B91C1C", "#1D4ED8", "#B45309")[i % 3])
        if not fixed:
            dk = prog(t, s("break1"), T["flat"])
            for k in range(8):                                       # dust behind the horses
                v2.puff(c, lerp(2100, 1000, dk) + k * 90, 60 + (k % 3) * 24, 50 + k * 4, "#C9A36A", 0.35 * dk, k=k)
        c.restore()
        self.ui["cam"] = cam

    def ui_plain(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 420, "raiders", T["raiders"] - 0.1, T["north"] - 0.1, accent=WARN, size=40)
            self.chip(540, 420, "north", T["north"] - 0.1, T["flat"] - 0.1, accent="#E2E8F0", size=40)
            self.chip(540, 420, "flat", T["flat"] - 0.1, s("fix1") - 0.15, accent=WARN, size=38)
            self.badge("alert", T["stop"] + 0.05, s("fix1") - 0.2, x=880, y=520)
            self.red(T["stop"] + 0.05, 1.3)
            return
        cam = self.ui.get("cam", self.cam_plain.at(tw))
        ax, ay = self.at(cam, -900, self.mtn_y(-900) - 60)
        self.label(ax, ay, 360, 470, "ridges", T["mountain"] - 0.1, s("break2") - 0.15, HILITE, size=38)
        self.chip(540, 1150, "charge", T["charge"] - 0.2, s("break2") - 0.15, accent=GOOD, size=36)
        self.badge("check", T["charge"] + 0.1, s("break2") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: gobi (break2, fix2)
    def draw_gobi(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        old = fixed and t >= T["stands"] - 0.2
        z = 1.0 if not old else lerp(1.0, 0.72, e_io(prog(t, T["stands"] - 0.2, T["stands"] + 0.6)))
        cam = (0, -200, z)
        cx, cy, _ = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DESERT, horizon_y=gy - 20)
        add_glow(c, 820, 470, 300, "#FFE3A3", 0.6)
        c.drawCircle(820, 470, 70, P("#FFF4D6"))
        for i in range(2):
            v2.cloud(c, 200 + i * 520, 300 + i * 90, 0.8, body="#9A5A48", rim="#FFD7A0", a=0.5, seed=i + 4)
        self.view(c, cam)
        dn = skia.Path()
        dn.moveTo(-2000, 0)
        dn.quadTo(-1100, -120, -400, -30)
        dn.quadTo(300, 40, 1100, -90)
        dn.quadTo(1600, -150, 2200, -40)
        dn.lineTo(2200, 3000)
        dn.lineTo(-2000, 3000)
        dn.close()
        c.drawPath(dn, lin_paint(0, -150, 0, 900, [SAND, SAND_D, "#5E3B17"]))
        heat = 0.6 if not fixed else 0.3
        for i in range(7):                                           # heat shimmer
            xx = -500 + i * 170
            pth = skia.Path()
            pth.moveTo(xx, -40)
            for k in range(1, 7):
                pth.lineTo(xx + math.sin(t * 5 + k * 1.3 + i) * 12, -40 - k * 60)
            c.drawPath(pth, P("#FFD9A0", heat * 0.5 * math.sin(((t * 0.6 + i * 0.13) % 1.0) * math.pi), stroke=6))
        if not fixed:
            person(c, -200, 40, 270, "#2563EB", t, pose="shrug", face=1, hat="none", hair="#1C1917")
            c.drawRect(R(-20, -40, 230, 70), P("#7C5A3A"))            # an empty cart
            c.drawRect(R(-20, -40, 230, 70), P("#4A321E", stroke=6))
            c.drawLine(210, -30, 300, -90, P("#7C5A3A", stroke=10))
            c.drawCircle(30, 40, 30, P("#3F2A1A"))
            c.drawCircle(160, 40, 30, P("#3F2A1A"))
            tb = (t * 0.5) % 1.0                                     # a tumbleweed rolls by
            tx_ = lerp(900, -900, tb)
            c.save()
            c.translate(tx_, 10)
            c.rotate(-tb * 900)
            for k in range(8):
                c.drawArc(R(-34, -34, 68, 68), k * 45, 160, False, P("#8A6A3E", 0.9, stroke=4))
            c.restore()
        else:
            self.rammed(c, t, old)
        c.restore()
        self.ui["cam"] = cam

    def rammed(self, c, t, old):
        """The wall section: a wooden frame filled layer by layer (rammed earth), then reed + gravel layers; weathered."""
        T = self.T
        x0, x1, base, top_h = -300.0, 300.0, 40.0, 520.0
        nl = 12
        k_earth = prog(t, T["pound"] - 0.2, T["reeds"] - 0.1)
        k_reed = prog(t, T["reeds"] - 0.1, T["stands"] - 0.3)
        n_e = int(6 * k_earth + 0.999) if k_earth > 0 else 0
        n_r = int(6 * k_reed + 0.999) if k_reed > 0 else 0
        lh = top_h / nl
        if old:                                                      # the wall runs on into the distance, worn
            for k in range(1, 5):
                for sd in (-1, 1):
                    ox = sd * (600 * k)
                    h_ = top_h * (0.85 - 0.12 * k)
                    wp = skia.Path()
                    wp.moveTo(ox - 260, base)
                    wp.lineTo(ox - 250, base - h_ * 0.9)
                    wp.quadTo(ox, base - h_ * 1.05, ox + 250, base - h_ * 0.8)
                    wp.lineTo(ox + 260, base)
                    wp.close()
                    c.drawPath(wp, P(mix(EARTH, SAND, 0.4), 0.95))
                    for j in range(int(h_ / lh)):
                        c.drawLine(ox - 255, base - j * lh, ox + 255, base - j * lh, P(EARTH_D, 0.45, stroke=3))
        clip = skia.Path()
        if old:
            clip.moveTo(x0, base)
            clip.lineTo(x0 + 10, base - top_h * 0.82)
            clip.quadTo(x0 + 120, base - top_h * 0.98, 20, base - top_h * 0.9)
            clip.quadTo(160, base - top_h * 0.78, x1 - 10, base - top_h * 0.86)
            clip.lineTo(x1, base)
            clip.close()
        else:
            clip.addRect(R(x0, base - top_h, x1 - x0, top_h))
        c.save()
        c.clipPath(clip, doAntiAlias=True)
        for j in range(n_e + n_r):
            yb = base - j * lh
            if j < n_e:
                c.drawRect(R(x0, yb - lh, x1 - x0, lh), P(EARTH if j % 2 else mix(EARTH, EARTH_D, 0.25)))
                c.drawLine(x0, yb - lh, x1, yb - lh, P(EARTH_D, 0.8, stroke=3))
            else:
                reed = (j - n_e) % 2 == 0
                if reed:
                    c.drawRect(R(x0, yb - lh, x1 - x0, lh), P("#B7A64E"))
                    for xx in range(int(x0), int(x1), 12):
                        c.drawLine(xx, yb - lh + 4, xx + 6, yb - 4, P("#7C6E2A", 0.8, stroke=3))
                else:
                    c.drawRect(R(x0, yb - lh, x1 - x0, lh), P("#9CA3AF"))
                    rng = random.Random(j)
                    for _ in range(40):
                        c.drawCircle(rng.uniform(x0, x1), rng.uniform(yb - lh + 4, yb - 4), rng.uniform(3, 7), P("#6B7280"))
        c.restore()
        if not old:
            for sd in (-1, 1):                                       # the wooden frame
                px = x0 - 22 if sd < 0 else x1 + 6
                c.drawRect(R(px, base - top_h - 40, 16, top_h + 40), P("#8B5A2B"))
            ph = base - (n_e + n_r) * lh
            c.drawRect(R(x0 - 24, ph - 40, x1 - x0 + 48, 18), P("#A16207"))
            c.drawRect(R(x0 - 24, ph + 10, x1 - x0 + 48, 14), P("#A16207", 0.8))
            rk = prog(t, T["pound"] - 0.2, T["reeds"] - 0.1) * (1 - prog(t, T["reeds"] - 0.1, T["reeds"] + 0.2))
            for i, wx in enumerate((-150, 30, 190)):                  # workers ramming with poles
                up = abs(math.sin(t * 7 + i * 1.7))
                fy = ph - 10
                person(c, wx, fy, 120, ("#1D4ED8", "#B45309", "#15803D")[i], t, pose="carry", face=1, hat="none",
                       hair="#1C1917")
                pole_y = fy - 30 - up * 50 * rk
                c.drawLine(wx + 30, pole_y - 60, wx + 30, pole_y + 30, P("#7C5A3A", stroke=8))
                c.drawRect(R(wx + 16, pole_y + 24, 28, 22), P("#57534E"))
            if t >= T["reeds"] - 0.1:
                for i, wx in enumerate((-120, 120)):
                    person(c, wx, ph - 10, 120, ("#B45309", "#1D4ED8")[i], t, pose="carry", face=1, hat="none", hair="#1C1917")


    def ui_gobi(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 420, "gobi", T["gobi"] - 0.15, s("fix2") - 0.15, accent="#FDBA74", size=44)
            for i, (key, t0) in enumerate((("nostone", T["stone"]), ("nowood", T["wood"]))):
                k = self.span(t0 - 0.15, s("fix2") - 0.15)
                if k > 0:
                    x = 330 + i * 420
                    c.drawCircle(x, 640, 92, P("#0B1220", 0.75 * k))
                    if i == 0:
                        c.drawOval(R(x - 56, 610, 112, 70), P("#9CA3AF", k))
                    else:
                        c.drawRect(R(x - 12, 590, 24, 100), P("#8B5A2B", k))
                        c.drawCircle(x, 590, 42, P("#3F7A2E", k))
                    c.drawCircle(x, 640, 92, P(WARN, k, stroke=10))
                    c.drawLine(x - 64, 704, x + 64, 576, P(WARN, k, stroke=12))
                    v2.chip(c, x, 780, self.L[key], k, accent=WARN, size=32)
            self.badge("alert", T["wood"] + 0.05, s("fix2") - 0.2, x=880, y=520)
            self.red(T["wood"] + 0.05, 1.3)
            return
        self.chip(540, 420, "pound", T["pound"] - 0.1, T["layers"] - 0.1, accent="#FDBA74", size=40)
        self.chip(540, 420, "layers", T["layers"] - 0.1, T["reeds"] - 0.1, accent=GOOD, size=40)
        self.chip(540, 420, "reeds", T["reeds"] - 0.1, T["stands"] - 0.15, accent="#D9F99D", size=40)
        self.chip(540, 420, "years", T["stands"] - 0.1, s("break3") - 0.15, accent=HILITE, size=40)
        self.badge("check", T["thousand"] + 0.1, s("break3") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: mortar (break3, fix3)
    def draw_mortar(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        v2.sky(c, W, H, 0.0, pal=RAINY, horizon_y=H * 0.62)
        bw, bh, gap = 170.0, 74.0, 12.0
        x0, y0 = -40.0, 560.0
        rows = 8
        built = prog(t, s("break3") - 0.1, T["brick"] + 0.2) if not fixed else 1.0
        crumble = prog(t, T["crumbles"] - 0.2, T["rain"] + 0.4) if not fixed else 0.0
        white = prog(t, T["rice2"], T["starch"]) if fixed else 0.0
        vrect(c, 0, y0 - 20, W, rows * (bh + gap) + 40, ["#3A3328", "#2A241C"])
        nb = 0
        for r_ in range(rows):
            yy = y0 + r_ * (bh + gap)
            off = (bw + gap) / 2 if r_ % 2 else 0
            for q in range(8):
                xx = x0 - off + q * (bw + gap)
                if xx > W + 10:
                    break
                nb += 1
                if nb / 56.0 > built + 0.02:
                    continue
                slip = 0.0
                if r_ == 3 and q == 3:
                    slip = prog(t, T["fall"], T["fall"] + 0.5) if not fixed else 0.0
                rng = random.Random(r_ * 17 + q)
                col = mix(BRICK, BRICK_D, rng.uniform(0, 0.4))
                c.save()
                if slip > 0:
                    c.translate(xx + bw / 2, yy + bh / 2)
                    c.rotate(12 * slip)
                    c.translate(-(xx + bw / 2) + 30 * slip, -(yy + bh / 2) + 60 * slip)
                c.drawRRect(rr(xx, yy, bw, bh, 6), P(col))
                c.drawRRect(rr(xx + 6, yy + 6, bw - 12, 10, 4), P("#FFFFFF", 0.08))
                c.restore()
        mc = mix("#B8B2A6", "#F8FAFC", white)                       # the mortar lines
        for r_ in range(rows + 1):
            yy = y0 + r_ * (bh + gap) - gap
            c.drawRect(R(0, yy, W * built + 40, gap), P(mix(mc, "#3A3328", crumble * 0.8)))
            if crumble > 0:
                rng = random.Random(r_)
                for _ in range(10):
                    c.drawCircle(rng.uniform(0, W), yy + gap / 2, rng.uniform(3, 8), P("#1F1A14", crumble))
        for r_ in range(rows):
            yy = y0 + r_ * (bh + gap)
            off = (bw + gap) / 2 if r_ % 2 else 0
            for q in range(8):
                xx = x0 - off + q * (bw + gap) - gap
                if 0 < xx < W * built + 40:
                    c.drawRect(R(xx, yy, gap, bh), P(mix(mc, "#3A3328", crumble * 0.8)))
        if white > 0:
            add_glow(c, W / 2, y0 + 300, 520, "#F8FAFC", 0.18 * white)
        if crumble > 0:                                              # bits of mortar falling
            rng = random.Random(9)
            for i in range(26):
                st_ = T["crumbles"] + rng.uniform(0, 1.2)
                if t > st_:
                    age = t - st_
                    px = rng.uniform(40, W - 40)
                    py = y0 + rng.randint(0, rows) * (bh + gap) + 0.5 * 1400 * age * age
                    if py < H:
                        c.drawRect(R(px, py, 9, 7), P("#CFC8B8", 0.9))
        rain(c, -100, W + 100, -200, H, t, a=0.75, n=90, seed=12)
        if fixed:
            for i in range(6):                                       # drops hit and roll off
                q = (t * 1.3 + i * 0.37) % 1.0
                px = 120 + i * 160
                py = y0 + 40 + q * 600
                c.drawCircle(px, py, 9, P("#BFDBFE", 0.8 * prog(t, T["rolls"] - 0.6, T["rolls"])))
                v2set.splash(c, px, y0 + 20, t, t - (t + i * 0.3) % 0.9, dur=0.7, n=6, speed=260)
            wk = prog(t, T["stir"] - 0.3, T["stir"])
            wok(c, 300, 1110, 1.05 * wk, t, stir=t, a=wk)
            tk = prog(t, T["stir"] - 0.2, T["stir"] + 0.2)
            if tk > 0:                                               # the lime trough, the soup poured in
                c.drawRect(R(600, 1080, 360, 110), lin_paint(600, 0, 960, 0, ["#6B7280", "#9CA3AF", "#4B5563"], a=tk))
                c.drawRect(R(612, 1080, 336, 26), P(mix("#D6D3CB", "#FFFFFF", white), tk))
                pk = self.span(T["rice2"] - 0.1, T["starch"] + 0.2)
                if pk > 0:
                    pth = skia.Path()
                    pth.moveTo(440, 1070)
                    pth.quadTo(560, 960, 700, 1090)
                    c.drawPath(pth, P("#F8FAFC", 0.95 * pk, stroke=20))
                    for k in range(5):
                        q = (t * 1.5 + k / 5.0) % 1.0
                        c.drawOval(R(640 + k * 60, 1084 - 6 * math.sin(q * math.pi), 40, 14), P("#FFFFFF", 0.8 * pk))
        self.ui["y0"] = y0

    def ui_mortar(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 420, "ming", T["ming"] - 0.15, T["crumbles"] - 0.2, accent="#FDBA74", size=40)
            self.chip(540, 420, "lime", T["crumbles"] - 0.2, T["rain"] - 0.1, accent="#E2E8F0", size=40)
            self.chip(540, 420, "crumble", T["rain"] - 0.1, s("fix3") - 0.15, accent=WARN, size=38)
            self.badge("alert", T["crumbles"] + 0.05, s("fix3") - 0.2, x=880, y=520)
            self.red(T["fall"], 1.3)
            return
        self.chip(540, 420, "stir", T["stir"] - 0.1, T["starch"] - 0.1, accent="#F8FAFC", size=42)
        k = self.span(T["starch"] - 0.15, T["rolls"] - 0.1)
        if k > 0:
            c.drawRRect(rr(90, 520, 900, 420, 40), P("#0B1220", 0.6 * k))
            crystals(c, 300, 720, 130, 0.0, a=k)
            crystals(c, 760, 720, 130, prog(tw, T["starch"], T["tight"]) * 2, a=k)
            v2.chip(c, 300, 900, self.L["loose"], k, accent=WARN, size=30)
            v2.chip(c, 760, 900, self.L["tight"], self.span(T["tight"] - 0.15, T["rolls"] - 0.1), accent=GOOD, size=30)
        self.chip(540, 420, "rolls", T["rolls"] - 0.15, s("break4") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["rolls"] + 0.1, s("break4") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: beacon (break4, fix4, cta)
    LONG = [(-3800, -80), (-3300, -140), (-2800, -60), (-2300, -180), (-1800, -110), (-1300, -230), (-800, -150),
            (-300, -260), (200, -170), (700, -280), (1200, -200), (1700, -120), (2300, -60)]
    BT = (-2700.0, -2250.0, -1800.0, -1350.0, -900.0, -450.0, 0.0, 450.0, 900.0, 1350.0)

    def long_y(self, x):
        return poly_y(self.LONG, x)

    def draw_beacon(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam_beacon.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 160)
        v2.stars(c, W, H, t, 0.7, dx=-cx * 0.01)
        c.save()
        c.translate(W / 2 - cx * 0.1, gy - 120)
        v2.ridge(c, -1800, 1800, 0, 260, "#4B3F78", "#2E2A5C", seed=11, step=120, rough=0.5)
        c.restore()
        self.view(c, cam)
        mp = skia.Path()
        mp.moveTo(self.LONG[0][0], 2000)
        for x_, y_ in self.LONG:
            mp.lineTo(x_, y_)
        mp.lineTo(self.LONG[-1][0], 2000)
        mp.close()
        c.drawPath(mp, lin_paint(0, -300, 0, 600, ["#2E3B3A", "#121C1E"]))
        fixed = t >= s("fix4") - 0.12
        wall_on(c, self.long_y, -3700, 2200, 1.0, wh=40.0, step=11.0)
        nb = len(self.BT)
        for i, bx in enumerate(self.BT):
            j = nb - 1 - i                                           # relay order: east (right) to west (left)
            t0 = T["relay"] + j * self.dt_relay
            lit = prog(t, t0, t0 + 0.2) if fixed else 0.0
            n = 1
            if i == 0 and fixed:
                n = 5 if t >= T["five"] - 0.1 else 1
            tower(c, bx, self.long_y(bx), 84, 112, fire=lit, t=t)
            if lit > 0:
                smoke_col(c, bx, self.long_y(bx) - 140, t, t0, s=1.0, a=lit, seed=i * 7, n=n, gap=44)
        for k, tx_ in enumerate((-3080, -2950)):                     # the army camp at the west end
            tent(c, tx_, self.long_y(tx_) + 60, 1.3)
        ck = prog(t, T["camp"], T["camp"] + 0.3) if fixed else 0.0
        for k in range(4):
            person(c, -3110 + k * 80, self.long_y(-3000) + 80, 120, "#B91C1C", t, pose="cheer" if ck > 0.5 else "stand",
                   face=1, hat="none", hair="#1C1917")
        if t < T["relay"] + 1.0:                                     # raiders arrive at the east end
            for i in range(4):
                u = e_out(prog(t, s("break4") - 0.1 + i * 0.15, s("break4") + 1.6 + i * 0.15))
                hx = lerp(1900 + i * 140, 1050 + i * 120, u)
                horse(c, hx, self.long_y(hx) + 120 + (i % 2) * 40, 1.25, t * 11 + i, face=-1,
                      rider=("#B91C1C", "#1D4ED8")[i % 2])
        c.restore()
        self.ui["cam"] = cam

    def ui_beacon(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", self.cam_beacon.at(tw))
        if tw < s("fix4") - 0.12:
            self.chip(540, 420, "long", T["long"] - 0.15, T["army"] - 0.15, accent="#E2E8F0", size=40)
            k = self.span(T["army"] - 0.15, s("fix4") - 0.15)
            if k > 0:
                v2.chip(c, 540, 420, self.L["army"] + ": " + self.L["days"], k, accent=WARN, size=40)
                arrow_l(c, 760, 560, 300, 560, WARN, a=k)
            self.badge("alert", T["days"] + 0.05, s("fix4") - 0.2, x=880, y=520)
            self.red(T["days"] + 0.05, 1.3)
            return
        if tw < s("cta") - 0.12:
            self.chip(540, 420, "beacon", T["beacon"] - 0.15, T["sight"] - 0.1, accent=HILITE, size=42)
            self.chip(540, 420, "sight", T["sight"] - 0.1, T["one"] - 0.15, accent=GOOD, size=38)
            self.chip(540, 420, "one", T["one"] - 0.15, T["five"] - 0.15, accent="#FDE68A", size=40)
            self.chip(540, 420, "five", T["five"] - 0.15, s("cta") - 0.15, accent=WARN, size=40)
            self.badge("check", T["tenk"] + 0.1, s("cta") - 0.15, x=880, y=520)

    # ------------------------------------------------------------------ set: chat (tag)
    def draw_chat(self, c, t):
        T = self.T
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=1060)
        c.save()
        c.translate(0, 0)
        rp = [(x, 900 - 60 * math.sin(x / 160.0) - 30 * math.sin(x / 70.0)) for x in range(-40, W + 60, 20)]
        mp = skia.Path()
        mp.moveTo(-40, H)
        for x_, y_ in rp:
            mp.lineTo(x_, y_)
        mp.lineTo(W + 60, H)
        mp.close()
        c.drawPath(mp, lin_paint(0, 820, 0, 1300, ["#2E3B3A", "#0E161C"]))
        fn = (lambda x: 900 - 60 * math.sin(x / 160.0) - 30 * math.sin(x / 70.0))
        wall_on(c, fn, -40, W + 60, 1.0, wh=22.0, step=8.0)
        for i, bx in enumerate((60, 280, 500, 720, 940)):
            t0 = T["smoke"] - 0.2 + i * 0.18
            lit = prog(t, t0, t0 + 0.15)
            tower(c, bx, fn(bx), 46, 62, fire=lit, t=t)
            if lit > 0:
                smoke_col(c, bx, fn(bx) - 80, t, t0, s=0.55, a=lit, seed=i * 5)
        c.restore()
        pk = prog(t, T["friend"] - 0.45, T["friend"] - 0.1)
        if pk > 0:
            phone_chat(c, 540, 300 + (1 - e_out(pk)) * 300, 600, 820, t, pk, self.L["msg"], self.L["seen"],
                       typing=self.span(T["yesterday"], T["replied"] - 0.1), rtl=self.rtl,
                       k_seen=prog(t, T["saw"] - 0.1, T["saw"] + 0.2))

    def ui_chat(self, c, t, tw):
        T = self.T
        self.chip(540, 1190, "provinces", T["smoke"] - 0.1, T["friend"] - 0.3, accent=HILITE, size=36)
        k = self.span(T["replied"] - 0.15, self.duration + 1)
        if k > 0:
            v2.chip(c, 540, 1190, self.L["nothing"], k, accent=WARN, size=40)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.6)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.8, True, 61), -12), (0.2, rumble(1.6, 62), -14), (T["halfway"], sfx.sparkle(0.6, 8, 63), -10),
              (T["earth"], sfx.whirr(0.8), -14), (T["rice"], sfx.pop(64), -6), (T["rice"] + 0.1, sfx.hiss(0.8, 65), -16),
              (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 66), -9), (T["great"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4)]
        for k in range(18):                                          # hooves
            ev.append((s("break1") + 0.1 + k * 0.13, sfx.thud(0.12, 68 + k % 3), -12))
        ev += [(T["stop"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["mountain"], sfx.sparkle(0.6, 8, 73), -10),
               (T["charge"] - 0.3, sfx.thud(0.5), -8), (T["charge"] + 0.1, sfx.ding(), -8), (T["charge"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 74), -4), (T["gobi"], sfx.hiss(1.2, 75), -16),
               (T["stone"], sfx.buzz(0.3), -12), (T["wood"], sfx.buzz(0.3), -12), (T["wood"] + 0.1, sfx.alarm(3, 820.0), -12)]
        for k in range(10):                                          # ramming
            ev.append((T["pound"] + k * 0.28, sfx.thud(0.18, 76 + k % 2), -10))
        ev += [(T["reeds"], sfx.creak(0.6), -12), (T["gravel"], sfx.click(77), -10),
               (T["thousand"] + 0.1, sfx.ding(), -8), (T["thousand"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["brick"], sfx.clank(300.0, 0.4, 79), -12),
               (T["rain"] - 0.4, sfx.hiss(2.0, 80), -12), (T["fall"], sfx.snap(81), -6), (T["fall"] + 0.3, sfx.thud(0.4), -8),
               (T["crumbles"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["stir"], sfx.sizzle(0.8, 82), -12), (T["rice2"], sfx.hiss(1.0, 83), -14), (T["tight"], sfx.lock_click(84), -8),
               (T["rolls"] + 0.1, sfx.ding(), -8), (T["rolls"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 85), -4)]
        for k in range(10):
            ev.append((s("break4") + 0.1 + k * 0.14, sfx.thud(0.12, 86 + k % 3), -13))
        ev += [(T["days"] + 0.1, sfx.alarm(3, 820.0), -12)]
        for j in range(len(self.BT)):
            ev.append((T["relay"] + j * self.dt_relay, sfx.sizzle(0.3, 90 + j), -14))
        ev += [(T["camp"], sfx.ding(), -10), (T["one"], sfx.thunk(91), -6), (T["five"], sfx.thunk(92), -4),
               (T["tenk"] + 0.1, sfx.ding(), -8), (T["tenk"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(93), 0), (T["follow"] - 0.15, sfx.pop(94), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 95), -6), (T["join"], sfx.sizzle(1.2, 96), -14),
               (T["wolf"], sfx.whirr(0.9, 300.0, 520.0, 97), -14), (T["wolves"], sfx.alarm(2, 700.0), -14)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 98), -6), (T["s1"], sfx.pop(99), -3), (T["s2"], sfx.pop(100), -3),
               (T["s3"], sfx.pop(101), -3), (T["s3"] + 0.2, sfx.womp(), -10)]
        ev += [(T["cong2"], sfx.pop(102), -2), (T["cong2"], sfx.sparkle(1.0, 14, 103), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 104), -6), (T["smoke"], sfx.sizzle(0.8, 105), -14),
               (T["friend"], sfx.pop(106), -6), (T["saw"] + 0.1, sfx.tick(), -8), (T["yesterday"] + 0.2, sfx.tick(), -10),
               (T["replied"] + 0.1, sfx.womp(), -8)]
        return ev


def arrow_l(c, x0, y0, x1, y1, col, a=1.0, w=12, head=32):
    if a <= 0:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    c.drawLine(x0, y0, x1 - math.cos(ang) * head * 0.6, y1 - math.sin(ang) * head * 0.6, P(col, a, stroke=w))
    hp = skia.Path()
    hp.moveTo(x1, y1)
    hp.lineTo(x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head)
    hp.lineTo(x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)
    hp.close()
    c.drawPath(hp, P(col, a))


def wolf_icon(c, x, y, s, t, a=1.0, howl=0.0):
    """A wolf howling (side view silhouette on a disc)."""
    if a <= 0:
        return
    c.drawCircle(x, y, 90 * s, P("#FDE68A", 0.9 * a))
    c.save()
    c.translate(x, y + 40 * s)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(-60, 30)
    body.lineTo(-50, -10)
    body.lineTo(-10, -20)
    body.lineTo(20, -40)
    lift = 18 * howl
    body.lineTo(34, -72 - lift)
    body.lineTo(44, -60 - lift)
    body.lineTo(70, -84 - lift * 1.4)
    body.lineTo(62, -54 - lift * 0.6)
    body.lineTo(46, -30)
    body.lineTo(40, 30)
    body.lineTo(26, 30)
    body.lineTo(20, 0)
    body.lineTo(-30, 4)
    body.lineTo(-40, 30)
    body.close()
    c.drawPath(body, P("#1E1B2E", a))
    tl_ = skia.Path()
    tl_.moveTo(-50, -4)
    tl_.quadTo(-86, 0, -92, 26)
    c.drawPath(tl_, P("#1E1B2E", a, stroke=12))
    c.restore()


NAME = "greatwall"
EPISODE = GreatWall
