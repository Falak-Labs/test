"""Episode 103 - bubble wrap.  v2 look.

Sets: wall (hook: a 1957 living room whose whole wall is papered with shiny bubbles, the camera pulling out from the
bubbles to the room; break1: a couple frowns at it, NO SALE, and the question: how did it end up in every box?), box
(fix1: a cardboard box cut open, a vase on a big pillow of trapped air; the box drops, the air squishes and springs back;
break2: the one big pillow pops and the vase hits the floor; fix2: a sheet of tiny bubbles round the vase, a pin pops one
and the rest still hold; cta), factory (break3: a man red in the face blowing one tiny balloon, a counter to a million;
fix3: hot plastic film pulled onto a drum full of little cups, a flat film pressed on top, bubble wrap rolling out),
truck (break4: a truck in x-ray full of puffy rolls, MOSTLY AIR, coins flying out; fix4: the same truck packed with
flat rolls, then a little pump at a packing table blowing the flat film up into bubbles), computer (reveal: a 1959
computer with tape reels wrapped in bubble wrap and crated), sheet (stat: a big glistening sheet; closer: a roll with
the sheet unrolling, for the cover), tag (English: a giant box at the door, a mountain of bubble wrap and one tiny phone
charger; Arabic: mom's new sofa still in its plastic cover after five years).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

FILM = "#BFE6FF"
CARD = ("#D9A35E", "#B9813F", "#8A5A2B")
VASE = ("#F8FAFC", "#2563EB")


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== pieces
def bubble(c, x, y, r, a=1.0, popped=0.0, tint=FILM, squash=1.0):
    """One air bubble seen from the front: a clear dome with a rim light and a highlight. popped 0..1 flattens it into
    a crinkled disc."""
    if a <= 0 or r <= 0.5:
        return
    if popped >= 0.999:
        p = skia.Path()
        rng = random.Random(int(x * 7 + y * 13))
        for k in range(9):
            ang = k / 9 * math.tau
            rr_ = r * rng.uniform(0.55, 0.95)
            px, py = x + math.cos(ang) * rr_, y + math.sin(ang) * rr_ * squash
            (p.moveTo if k == 0 else p.lineTo)(px, py)
        p.close()
        c.drawPath(p, P(tint, 0.18 * a))
        c.drawPath(p, P("#FFFFFF", 0.35 * a, stroke=max(1.0, r * 0.06)))
        c.drawLine(x - r * 0.4, y - r * 0.1, x + r * 0.3, y + r * 0.2, P("#FFFFFF", 0.35 * a, stroke=max(1.0, r * 0.05)))
        return
    k = 1.0 - 0.35 * popped
    rx, ry = r * k, r * k * squash
    oval = R(x - rx, y - ry, 2 * rx, 2 * ry)
    c.drawOval(oval, rad_paint(x - r * 0.3, y - r * 0.35, r * 1.35, [(tint, 0.55 * a), (tint, 0.22 * a), ("#FFFFFF", 0.6 * a)],
                               [0.0, 0.72, 1.0]))
    c.drawOval(oval, P("#FFFFFF", 0.6 * a, stroke=max(1.2, r * 0.08)))
    c.drawCircle(x - r * 0.34, y - r * 0.36 * squash, r * 0.22, P("#FFFFFF", 0.9 * a))
    c.drawCircle(x + r * 0.32, y + r * 0.34 * squash, r * 0.08, P("#FFFFFF", 0.5 * a))


def sheet(c, x0, y0, x1, y1, r, a=1.0, popped=(), t=0.0, tint=FILM, film=True, wobble=0.0, squash=1.0):
    """A sheet of bubble wrap filling the rectangle: hex-packed bubbles of radius r on a thin film."""
    if a <= 0:
        return
    if film:
        c.drawRRect(rr(x0, y0, x1 - x0, y1 - y0, r * 0.6), P(tint, 0.16 * a))
        c.drawRRect(rr(x0, y0, x1 - x0, y1 - y0, r * 0.6), P("#FFFFFF", 0.3 * a, stroke=2))
    d = 2.25 * r
    cb = c.getLocalClipBounds()                        # skip bubbles that are off screen (the zoomed hook)
    row = 0
    y = y0 + r * 1.2
    while y < y1 - r * 0.9:
        x = x0 + r * 1.2 + (d / 2 if row % 2 else 0)
        col = 0
        while x < x1 - r * 0.9:
            if x + r < cb.left() or x - r > cb.right() or y + r + wobble < cb.top() or y - r - wobble > cb.bottom():
                x += d
                col += 1
                continue
            wy = math.sin(t * 2 + x * 0.01 + row) * wobble
            bubble(c, x, y + wy, r, a, popped=1.0 if (row, col) in popped else 0.0, tint=tint, squash=squash)
            x += d
            col += 1
        y += d * 0.87
        row += 1


def card_box(c, x, y, w, h, a=1.0, cut=True, flaps=1.0):
    """A cardboard box with its front face cut away (cut=True), base on y. Returns the inner rect (x0, y0, x1, y1)."""
    top = y - h
    back = R(x - w / 2 + 26, top - 30, w - 52, h)
    c.drawRect(back, P(CARD[2], a))                     # the inside back wall
    c.drawRect(R(x - w / 2 + 26, y - 30, w - 52, 30), P(shade(CARD[2], -0.2), a))
    side = skia.Path()
    side.moveTo(x - w / 2, top)
    side.lineTo(x - w / 2 + 26, top - 30)
    side.lineTo(x - w / 2 + 26, y - 30)
    side.lineTo(x - w / 2, y)
    side.close()
    c.drawPath(side, P(CARD[1], a))
    side2 = skia.Path()
    side2.moveTo(x + w / 2, top)
    side2.lineTo(x + w / 2 - 26, top - 30)
    side2.lineTo(x + w / 2 - 26, y - 30)
    side2.lineTo(x + w / 2, y)
    side2.close()
    c.drawPath(side2, P(CARD[1], a))
    if flaps > 0:                                      # the two top flaps folded open
        for sd in (-1, 1):
            f = skia.Path()
            f.moveTo(x + sd * (w / 2 - 26), top - 30)
            f.lineTo(x + sd * (w / 2 + 70 * flaps), top - 120 * flaps)
            f.lineTo(x + sd * (w / 2 + 40 * flaps), top - 150 * flaps)
            f.lineTo(x + sd * 6, top - 30)
            f.close()
            c.drawPath(f, P(CARD[0], a))
            c.drawPath(f, P(CARD[2], 0.6 * a, stroke=3))
    if not cut:
        c.drawRect(R(x - w / 2, top, w, h), P(CARD[0], a))
        c.drawLine(x - w / 2, top + h * 0.5, x + w / 2, top + h * 0.5, P("#C9A46A", a, stroke=34))
    else:                                              # the cut edge of the front face
        c.drawRect(R(x - w / 2, top, w, h), P(CARD[0], a, stroke=10))
        c.drawRect(R(x - w / 2, y - 24, w, 24), P(CARD[0], a))
    return (x - w / 2 + 26, top - 30, x + w / 2 - 26, y - 30)


def vase(c, x, y, s, a=1.0, broken=0.0, t=0.0):
    """A blue-and-white vase standing on (x, y); s = 1 is about 300 px tall. broken 0..1: it cracks and falls apart."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if broken > 0.5:                                    # pieces on the floor
        rng = random.Random(4)
        for k in range(7):
            px = rng.uniform(-130, 130) * broken
            py = -rng.uniform(4, 30)
            c.save()
            c.translate(px, py)
            c.rotate(rng.uniform(-70, 70))
            p = skia.Path()
            p.moveTo(-30, 0)
            p.lineTo(28, -6)
            p.lineTo(18, -36)
            p.lineTo(-20, -30)
            p.close()
            c.drawPath(p, P(VASE[0], a))
            c.drawLine(-20, -16, 20, -20, P(VASE[1], a, stroke=6))
            c.restore()
        c.restore()
        return
    body = skia.Path()
    body.moveTo(-34, -300)
    body.cubicTo(-30, -250, -110, -220, -110, -130)
    body.cubicTo(-110, -50, -70, -10, -50, 0)
    body.lineTo(50, 0)
    body.cubicTo(70, -10, 110, -50, 110, -130)
    body.cubicTo(110, -220, 30, -250, 34, -300)
    body.close()
    c.drawPath(body, lin_paint(-110, 0, 110, 0, ["#CBD5E1", VASE[0], "#E2E8F0", "#94A3B8"], a=a))
    for yy, w_ in ((-260, 3), (-180, 8), (-90, 8), (-30, 4)):
        c.drawLine(-100 if abs(yy) > 60 else -70, yy, 100 if abs(yy) > 60 else 70, yy, P(VASE[1], 0.85 * a, stroke=w_))
    for k in range(5):                                  # flowers
        fx_ = -70 + k * 35
        c.drawCircle(fx_, -135, 13, P(VASE[1], 0.9 * a, stroke=5))
        c.drawCircle(fx_, -135, 4, P(VASE[1], a))
    c.drawPath(body, P("#64748B", 0.7 * a, stroke=3))
    if broken > 0:                                      # cracks spreading
        for k, (dx, dy) in enumerate(((-40, -60), (30, -140), (-10, -220))):
            n = clamp(broken * 2 - k * 0.2)
            if n > 0:
                p = skia.Path()
                p.moveTo(0, -20)
                p.lineTo(dx * 0.5 * n, -20 + dy * 0.4 * n)
                p.lineTo(dx * n, dy * n)
                c.drawPath(p, P("#0F172A", a, stroke=5))
    c.restore()


def wall_room(c, t, bubbles_a=1.0, z=1.0, cx=540, cy=820):
    """A 1957 living room: a teal wall papered with bubbles, a wooden floor, an armchair and a floor lamp."""
    vrect(c, 0, 0, W, H, ["#0E3B43", "#14555E"])
    c.save()
    c.translate(cx, cy)
    c.scale(z, z)
    c.translate(-540, -820)
    vrect(c, -400, 120, W + 800, 1000, ["#1F6E78", "#2A8C96"])
    sheet(c, -380, 150, W + 380, 1080, 30, a=bubbles_a, t=t, tint="#C7F3F6", film=False)
    c.drawRect(R(-400, 1080, W + 800, 24), P("#E7D3A8"))
    vrect(c, -400, 1104, W + 800, 400, ["#7C4A2A", "#5A3219"])
    for k in range(-4, 14):
        c.drawLine(k * 110, 1104, k * 110 - 60, 1500, P("#4A2812", 0.6, stroke=3))
    # the armchair
    c.drawRRect(rr(130, 830, 300, 230, 60), P("#D6A23A"))
    c.drawRRect(rr(100, 920, 80, 190, 30), P("#B9862A"))
    c.drawRRect(rr(380, 920, 80, 190, 30), P("#B9862A"))
    c.drawRRect(rr(160, 980, 240, 110, 30), P("#E5B44D"))
    for lx in (150, 410):
        c.drawLine(lx, 1100, lx - 8, 1150, P("#3B2410", 1, stroke=12))
    # the floor lamp
    c.drawLine(860, 1150, 860, 700, P("#3F3F46", 1, stroke=10))
    c.drawCircle(860, 1150, 40, P("#27272A"))
    shade_p = skia.Path()
    shade_p.moveTo(790, 700)
    shade_p.lineTo(930, 700)
    shade_p.lineTo(890, 600)
    shade_p.lineTo(830, 600)
    shade_p.close()
    c.drawPath(shade_p, P("#FDE68A"))
    add_glow(c, 860, 690, 260, "#FFE7A3", 0.35)
    c.restore()


def stamp(c, x, y, w, h, p, col="#EF4444", rot=-12):
    """A rubber-stamp frame that slams in (the words go in a chip above it)."""
    if p <= 0:
        return
    k = lerp(1.6, 1.0, e_out(clamp(p * 1.4)))
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(k, k)
    c.drawRRect(rr(-w / 2, -h / 2, w, h, 18), P(col, 0.9 * clamp(p * 2), stroke=14))
    c.drawLine(-w / 2 + 40, -h / 2 + 30, w / 2 - 40, h / 2 - 30, P(col, 0.9 * clamp(p * 2), stroke=18))
    c.drawLine(-w / 2 + 40, h / 2 - 30, w / 2 - 40, -h / 2 + 30, P(col, 0.9 * clamp(p * 2), stroke=18))
    c.restore()


def air_pillow(c, x, y, w, h, t, a=1.0, squash=1.0, popped=0.0):
    """One big pillow of trapped air with molecules bouncing inside (base on y)."""
    if a <= 0:
        return
    hh = h * squash * (1 - 0.85 * popped)
    ww = w * (1 + 0.12 * (1 - squash)) * (1 - 0.1 * popped)
    o = R(x - ww / 2, y - hh, ww, hh)
    c.drawRRect(skia.RRect.MakeRectXY(o, ww * 0.3, hh * 0.45), rad_paint(x - ww * 0.2, y - hh * 0.7, ww * 0.8,
                [("#E0F2FE", 0.55 * a), ("#93C5FD", 0.28 * a), ("#FFFFFF", 0.5 * a)], [0, 0.75, 1]))
    c.drawRRect(skia.RRect.MakeRectXY(o, ww * 0.3, hh * 0.45), P("#FFFFFF", 0.7 * a, stroke=4))
    if popped < 0.5:
        rng = random.Random(3)
        for k in range(28):
            u = (t * rng.uniform(0.3, 0.7) + rng.random()) % 1.0
            px = x + math.sin(u * math.tau * 2 + k) * (ww / 2 - 30)
            py = y - hh / 2 + math.cos(u * math.tau * 3 + k * 1.7) * (hh / 2 - 22)
            c.drawCircle(px, py, 7, P("#38BDF8", 0.8 * a * (1 - popped * 2)))
    c.drawCircle(x - ww * 0.28, y - hh * 0.72, 14 * squash, P("#FFFFFF", 0.8 * a * (1 - popped)))


def pop_burst(c, x, y, p, r=120, col="#FFFFFF"):
    """A cartoon POP: a star of short rays."""
    if p <= 0 or p >= 1:
        return
    for k in range(12):
        ang = k / 12 * math.tau
        r0, r1 = r * (0.3 + 0.7 * p), r * (0.6 + 0.9 * p)
        c.drawLine(x + math.cos(ang) * r0, y + math.sin(ang) * r0, x + math.cos(ang) * r1, y + math.sin(ang) * r1,
                   P(col, 1 - p, stroke=10))


def pin(c, x, y, s=1.0, a=1.0):
    """A push pin pointing down at (x, y)."""
    if a <= 0:
        return
    c.drawLine(x, y, x, y - 60 * s, P("#CBD5E1", a, stroke=5 * s))
    c.drawRRect(rr(x - 24 * s, y - 110 * s, 48 * s, 54 * s, 14 * s), P("#EF4444", a))
    c.drawCircle(x, y - 118 * s, 26 * s, P("#DC2626", a))


def drum(c, x, y, r, t, spin=1.0, suck=0.0):
    """The forming drum: a steel roller with rows of little cups on its rim; suck adds the vacuum arrows."""
    c.drawCircle(x, y, r, lin_paint(x - r, y - r, x + r, y + r, ["#E2E8F0", "#94A3B8", "#475569"]))
    c.drawCircle(x, y, r, P("#1E293B", 1, stroke=6))
    n = 18
    for k in range(n):
        ang = k / n * math.tau + t * 0.9 * spin
        cx_, cy_ = x + math.cos(ang) * r * 0.86, y + math.sin(ang) * r * 0.86
        c.drawCircle(cx_, cy_, r * 0.1, P("#1E293B", 0.9))
        c.drawCircle(cx_, cy_, r * 0.06, P("#0B1220"))
        if suck > 0:
            ix, iy = x + math.cos(ang) * r * 0.62, y + math.sin(ang) * r * 0.62
            c.drawLine(cx_, cy_, ix, iy, P("#38BDF8", 0.7 * suck, stroke=4))
    c.drawCircle(x, y, r * 0.22, P("#334155"))
    c.drawCircle(x, y, r * 0.08, P("#0F172A"))


def truck(c, x, y, s, t, cargo="air", xray=1.0, coins=0.0):
    """A box truck (side view) driving right, wheels on y. cargo "air": a few puffy rolls; "flat": many thin rolls."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    bounce = math.sin(t * 14) * 3
    c.translate(0, bounce)
    c.drawRRect(rr(-420, -420, 600, 360, 18), P("#F1F5F9"))
    c.drawRRect(rr(-420, -420, 600, 360, 18), P("#94A3B8", 1, stroke=6))
    cab = skia.Path()
    cab.moveTo(190, -60)
    cab.lineTo(190, -330)
    cab.lineTo(330, -330)
    cab.lineTo(400, -200)
    cab.lineTo(400, -60)
    cab.close()
    c.drawPath(cab, P("#2563EB"))
    c.drawRRect(rr(220, -310, 100, 100, 12), P("#BFDBFE"))
    c.drawRect(R(-430, -70, 840, 30), P("#334155"))
    if xray > 0:                                       # the cut-away cargo
        c.drawRRect(rr(-400, -400, 560, 320, 12), P("#0B1220", 0.85 * xray))
        if cargo == "air":
            for k, (rx, ry, rr_) in enumerate(((-310, -170, 85), (-140, -175, 90), (30, -170, 85), (-230, -320, 75),
                                               (-60, -320, 75), (100, -320, 60))):
                c.drawCircle(rx, ry, rr_, P(FILM, 0.35 * xray))
                c.drawCircle(rx, ry, rr_, P("#FFFFFF", 0.6 * xray, stroke=4))
                for j in range(3):
                    c.drawCircle(rx, ry, rr_ * (0.75 - j * 0.22), P("#FFFFFF", 0.35 * xray, stroke=3))
        else:
            for row in range(4):
                for k in range(11):
                    rx, ry = -375 + k * 50, -125 - row * 72
                    c.drawCircle(rx, ry, 23, P("#CBD5E1", 0.9 * xray))
                    c.drawCircle(rx, ry, 23, P("#64748B", xray, stroke=3))
                    c.drawCircle(rx, ry, 6, P("#475569", xray))
    for wx in (-300, -180, 280):
        c.drawCircle(wx, -30, 50, P("#111827"))
        c.drawCircle(wx, -30, 22, P("#9CA3AF"))
        c.save()
        c.translate(wx, -30)
        c.rotate(t * 400)
        c.drawLine(-18, 0, 18, 0, P("#4B5563", 1, stroke=5))
        c.restore()
    if coins > 0:                                      # coins flying out of the back
        rng = random.Random(8)
        for k in range(10):
            u = (t * 0.9 + rng.random()) % 1.0
            px = -440 - u * 300
            py = -200 - math.sin(u * math.pi) * 160 + rng.uniform(-60, 60)
            c.drawCircle(px, py, 22, P("#FACC15", coins * (1 - u)))
            c.drawCircle(px, py, 22, P("#A16207", coins * (1 - u), stroke=4))
    c.restore()


def computer(c, x, y, s, t, wrap=0.0, crate=0.0):
    """A 1959 computer: three grey cabinets with blinking lights and two tape reels, feet on y."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for k, (cx_, w_, h_) in enumerate(((-260, 200, 520), (-30, 240, 560), (210, 220, 520))):
        c.drawRRect(rr(cx_ - w_ / 2, -h_, w_, h_, 12), lin_paint(cx_ - w_ / 2, 0, cx_ + w_ / 2, 0, ["#94A3B8", "#CBD5E1", "#94A3B8"]))
        c.drawRRect(rr(cx_ - w_ / 2, -h_, w_, h_, 12), P("#475569", 1, stroke=4))
        if k == 1:                                     # the lights panel
            for i in range(5):
                for j in range(6):
                    on = (int(t * 6) + i * 3 + j * 7) % 5 < 2
                    c.drawCircle(cx_ - 80 + j * 32, -h_ + 70 + i * 34, 9, P("#FBBF24" if on else "#78350F"))
        else:                                          # two tape reels
            for ry in (-h_ + 130, -h_ + 300):
                c.drawCircle(cx_, ry, 70, P("#1F2937"))
                c.save()
                c.translate(cx_, ry)
                c.rotate(t * (160 if k == 0 else -160))
                for a_ in range(3):
                    c.rotate(120)
                    c.drawLine(0, 0, 0, -58, P("#6B7280", 1, stroke=12))
                c.restore()
                c.drawCircle(cx_, ry, 18, P("#9CA3AF"))
    if wrap > 0:                                       # bubble wrap round the whole thing
        c.save()
        c.clipRect(R(-400, -600 * smooth(wrap) - 10, 800, 620 * smooth(wrap) + 20))
        sheet(c, -390, -590, 390, 10, 22, a=0.95, t=t)
        c.restore()
    if crate > 0:                                      # a wooden crate slides down over it
        k = smooth(crate)
        top = lerp(-1400, -640, k)
        for i in range(6):
            c.drawRect(R(-420, top + i * 108, 840, 96), P("#B7793F"))
            c.drawRect(R(-420, top + i * 108, 840, 96), P("#7C4A1E", 1, stroke=5))
        c.drawLine(-420, top, 420, top + 650, P("#7C4A1E", 1, stroke=16))
    c.restore()


def roll(c, x, y, r, t, unroll=0.0, a=1.0, big=False):
    """A roll of bubble wrap lying on its side at (x, y) with a sheet unrolling to the left (big: a tall sheet)."""
    if unroll > 0:
        L = 760 * unroll
        hh = 300 if big else 120
        c.save()
        c.clipRect(R(x - L, y + r - hh - 4, L, hh + 8))
        sheet(c, x - L, y + r - hh, x, y + r, 30 if big else 18, a=a, t=t)
        c.restore()
    c.drawCircle(x, y, r, rad_paint(x - r * 0.3, y - r * 0.3, r * 1.3, [("#E0F2FE", 0.75 * a), ("#7DD3FC", 0.45 * a),
                                                                         ("#FFFFFF", 0.7 * a)], [0, 0.8, 1]))
    for k in range(1, 6):
        c.drawCircle(x, y, r * k / 6, P("#FFFFFF", 0.35 * a, stroke=3))
    c.drawCircle(x, y, r * 0.16, P("#A16207", a))
    c.drawCircle(x, y, r * 0.09, P("#3F2A0E", a))
    rng = random.Random(5)
    for k in range(30):
        ang = rng.random() * math.tau
        rr_ = r * rng.uniform(0.25, 0.95)
        c.drawCircle(x + math.cos(ang) * rr_, y + math.sin(ang) * rr_, 7, P("#FFFFFF", 0.6 * a))


def sofa_plastic(c, x, y, t, crinkle=0.0):
    """A new sofa still in its clear plastic cover (base on y)."""
    c.drawRRect(rr(x - 380, y - 330, 760, 200, 50), P("#9F1239"))
    c.drawRRect(rr(x - 420, y - 200, 840, 160, 50), P("#BE123C"))
    for sd in (-1, 1):
        c.drawRRect(rr(x + sd * 400 - 60, y - 260, 120, 230, 50), P("#881337"))
    c.drawLine(x - 380, y - 20, x - 370, y + 20, P("#3F1D0E", 1, stroke=14))
    c.drawLine(x + 380, y - 20, x + 370, y + 20, P("#3F1D0E", 1, stroke=14))
    cover = skia.Path()
    cover.addRRect(rr(x - 470, y - 350, 940, 340, 60))
    c.drawPath(cover, P("#E0F2FE", 0.22))
    c.drawPath(cover, P("#FFFFFF", 0.65, stroke=5))
    rng = random.Random(2)
    for k in range(16):
        px, py = x + rng.uniform(-430, 430), y + rng.uniform(-330, -40)
        L = rng.uniform(40, 120)
        ang = rng.uniform(-0.6, 0.6) + math.sin(t * 3 + k) * 0.1 * crinkle
        c.drawLine(px, py, px + math.cos(ang) * L, py + math.sin(ang) * L, P("#FFFFFF", 0.55, stroke=3))
    for k in range(5):
        add_glow(c, x - 300 + k * 150, y - 260 + (k % 2) * 90, 40, "#FFFFFF", 0.35)


class BubbleWrap(EpisodeV2):
    BUILD_NO = 103
    FIRST_SET = "wall"
    CLEAR = "#0B1530"
    TITLE = {"en": "BUBBLE WRAP", "ar_sa": "نايلون الفقاعات"}
    EMPH = {"en": ["BUBBLE", "WRAP", "INVENTED", "WALLPAPER", "NOBODY", "BUMPY", "WALLS", "BOX", "TRAP", "AIR",
                   "SQUISHES", "SPRINGS", "BACK", "PILLOW", "POPS", "FLOOR", "TINY", "BUBBLES", "POP", "HOLD", "BLOW",
                   "MILLION", "BALLOONS", "HOT", "PLASTIC", "CUPS", "FLAT", "SHEET", "SEALS", "TRUCK", "MONEY", "SHIPS",
                   "PUMPED", "PACK", "FOLLOW", "TUNNEL", "TOKYO'S", "FLOODS", "IBM", "COMPUTER", "TWO", "SHOWER",
                   "CURTAINS", "FLOP", "CONGRATS", "YOURSELF", "CHARGER", "GIANT", "TEN", "FEET"],
            "ar_sa": ["نايلون", "الفقاعات", "اخترعوه", "جدران", "محد", "جدار", "كرتون", "هوا", "ينضغط", "يرجع", "مخدة",
                      "تنفجر", "تطيح", "صغيرة", "تنفقع", "يشيل", "تنفخ", "مليون", "بالونة", "فالبلاستيك", "لأكواب",
                      "وطبقة", "تسكّر", "شاحنة", "فلوس", "مسطّح", "وينفخونه", "متابعة", "نفق", "طوكيو", "آي", "بي",
                      "إم", "كمبيوترها", "ستارتين", "شاور", "مبروك", "النايلون", "الكنب", "سنين"]}
    KEYS = {"ar_sa": {
        ("hook", "BUBBLE"): "الفقاعات", ("hook", "INVENTED"): "اخترعوه", ("hook", "WALLPAPER"): "جدران",
        ("break1", "NOBODY"): "محد", ("break1", "WALLS"): "جدار", ("break1", "BOX"): "كرتون",
        ("fix1", "AIR"): "هوا", ("fix1", "SQUISHES"): "ينضغط", ("fix1", "BACK"): "يرجع",
        ("break2", "PILLOW"): "مخدة", ("break2", "POPS"): "تنفجر", ("break2", "FLOOR"): "تطيح",
        ("fix2", "TINY"): "صغيرة", ("fix2", "POP"): "تنفقع", ("fix2", "HOLD"): "يشيل",
        ("break3", "BLOW"): "تنفخ", ("break3", "MILLION"): "مليون", ("break3", "BALLOONS"): "بالونة",
        ("fix3", "PLASTIC"): "البلاستيك", ("fix3", "CUPS"): "لأكواب", ("fix3", "SHEET"): "وطبقة", ("fix3", "SEALS"): "تسكر",
        ("break4", "TRUCK"): "شاحنة", ("break4", "AIR"): "هوا", ("break4", "MONEY"): "فلوس",
        ("fix4", "FLAT"): "مسطح", ("fix4", "PUMPED"): "ينفخونه", ("fix4", "PACK"): "التغليف",
        ("cta", "FOLLOW"): "متابعة", ("cta", "TOKYO'S"): "طوكيو",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "IBM"): "آي", ("reveal", "COMPUTER"): "كمبيوترها",
        ("reveal", "WRAP"): "بالفقاعات",
        ("stat", "TWO"): "ستارتين", ("stat", "ONE"): "جدران", ("stat", "AIR"): "وهوا",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CHARGER"): "النايلون", ("tag", "GIANT"): "الكنب", ("tag", "TEN"): "سنين"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Tokyo's flood tunnel"),
                   "stat": [("2", "SHOWER CURTAINS"), ("1", "WALLPAPER FLOP"), ("1000s", "OF AIR BUBBLES")],
                   "L": {"wall": "INVENTED AS... WALLPAPER", "y1957": "1957", "nosale": "NOBODY WANTED IT!",
                         "box": "SO HOW'D IT END UP IN EVERY BOX?", "air": "TRAP AIR", "spring": "IT SQUISHES... AND SPRINGS BACK",
                         "pops": "ONE BIG PILLOW: POP!", "smash": "CRASH!", "tiny": "LOTS OF TINY BUBBLES",
                         "hold": "POP ONE... THE REST HOLD", "million": "1,000,000 BALLOONS?", "puff": "PHEW...",
                         "cups": "HOT PLASTIC + LITTLE CUPS", "seal": "A FLAT SHEET SEALS THE AIR IN",
                         "mostly": "MOSTLY... AIR", "money": "SHIPPING AIR = $$$", "flat": "IT SHIPS FLAT",
                         "pumped": "PUMPED UP WHERE YOU PACK", "ibm": "IBM!", "new": "ITS NEW COMPUTER",
                         "safe": "SHIPPED IN BUBBLE WRAP", "name": "BUBBLE WRAP", "charger": "1 PHONE CHARGER",
                         "feet": "+ 10 FEET OF BUBBLE WRAP"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: نفق فيضانات طوكيو"),
                      "stat": [("2", "ستارة شاور"), ("1", "ورق جدران فاشل"), ("1000s", "فقاعة هوا")],
                      "L": {"wall": "اخترعوه... ورق جدران", "y1957": "1957", "nosale": "محد بغاه!",
                            "box": "كيف صار في كل كرتون؟", "air": "احبس هوا", "spring": "ينضغط... ويرجع",
                            "pops": "مخدة وحدة: طاخ!", "smash": "تكسّرت!", "tiny": "فقاعات صغيرة كثير",
                            "hold": "وحدة تنفقع... والباقي يشيل", "million": "مليون بالونة؟", "puff": "تعبت...",
                            "cups": "بلاستيك حار + أكواب صغيرة", "seal": "طبقة ثانية تسكّر على الهوا",
                            "mostly": "أغلبها... هوا", "money": "شحن الهوا = فلوس", "flat": "يجي مسطّح",
                            "pumped": "ينفخونه وقت التغليف", "ibm": "آي بي إم!", "new": "كمبيوترها الجديد",
                            "safe": "انشحن بالفقاعات", "name": "نايلون الفقاعات", "charger": "النايلون للحين على الكنب",
                            "feet": "من خمس سنين!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "bubble": ("hook", "BUBBLE", 0.2), "invented": ("hook", "INVENTED", 0.5), "wallpaper": ("hook", "WALLPAPER", 0.85),
            "nobody": ("break1", "NOBODY", 0.05), "walls": ("break1", "WALLS", 0.3), "box": ("break1", "BOX", 0.9),
            "air": ("fix1", "AIR", 0.3), "squish": ("fix1", "SQUISHES", 0.6), "back": ("fix1", "BACK", 0.9),
            "pillow": ("break2", "PILLOW", 0.3), "pops": ("break2", "POPS", 0.5), "floor": ("break2", "FLOOR", 0.9),
            "tiny": ("fix2", "TINY", 0.3), "pop": ("fix2", "POP", 0.6), "hold": ("fix2", "HOLD", 0.9),
            "blow": ("break3", "BLOW", 0.35), "million": ("break3", "MILLION", 0.65), "balloons": ("break3", "BALLOONS", 0.9),
            "plastic": ("fix3", "PLASTIC", 0.15), "cups": ("fix3", "CUPS", 0.45), "sheet": ("fix3", "SHEET", 0.7),
            "seals": ("fix3", "SEALS", 0.85),
            "truck": ("break4", "TRUCK", 0.15), "mostly": ("break4", "AIR", 0.5), "money": ("break4", "MONEY", 0.9),
            "flat": ("fix4", "FLAT", 0.35), "pumped": ("fix4", "PUMPED", 0.7), "pack": ("fix4", "PACK", 0.9),
            "follow": ("cta", "FOLLOW", 0.35),
            "answer": ("reveal", "ANSWER", 0.05), "ibm": ("reveal", "IBM", 0.3), "computer": ("reveal", "COMPUTER", 0.6),
            "wrapped": ("reveal", "WRAP", 0.9),
            "s1": ("stat", "TWO", 0.05), "s2": ("stat", "ONE", 0.4), "s3": ("stat", "AIR", 0.85),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_charger": ("tag", "CHARGER", 0.2), "t_giant": ("tag", "GIANT", 0.55), "t_ten": ("tag", "TEN", 0.8)})
        T["nosale1"] = max(T["walls"], T["nobody"] + 0.3)
        T["spring1"] = max(T["back"], T["squish"] + 0.3)
        T["pop1"] = max(T["pops"], T["pillow"] + 0.3)
        T["hold1"] = max(T["hold"], T["pop"] + 0.3)
        T["million1"] = max(T["million"], T["blow"] + 0.3)
        T["seal1"] = max(T["seals"], T["cups"] + 0.3)
        T["air1"] = max(T["mostly"], T["truck"] + 0.3)
        T["pack1"] = max(T["pack"], T["pumped"] + 0.2)
        T["drop1"] = T["squish"] - 0.35                # the box drops in fix1
        T["drop2"] = max(T["hold"] - 0.45, T["pop"] + 0.25)
        # ---- sets
        self.cut(s("fix1") - 0.12, "box", 1)
        self.cut(s("break3") - 0.12, "factory", -1)
        self.cut(s("break4") - 0.12, "truck", 1)
        self.cut(s("cta") - 0.12, "box", -1)
        self.cut(s("reveal") - 0.12, "computer", 1)
        self.cut(s("stat") - 0.12, "sheet", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        self.spans = [(T["nosale1"], T["spring1"]), (T["pop1"], T["hold1"]), (T["million1"], T["seal1"]), (T["air1"], T["pack1"])]
        self.shakes = [(T["nosale1"], 0.3, 6), (T["drop1"] + 0.35, 0.3, 7), (T["pop1"], 0.35, 8), (T["floor"], 0.3, 7),
                       (T["pop"], 0.2, 4), (T["drop2"] + 0.35, 0.25, 6), (T["million1"], 0.3, 5), (T["air1"], 0.3, 5),
                       (s("closer") + 0.2, 0.35, 6), (T["t_ten"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: wall (hook, break1)
    def draw_wall(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["bubble"] - 0.3, T["wallpaper"] + 0.2))
            wall_room(c, t, z=lerp(2.6, 1.0, k), cx=lerp(560, 540, k), cy=lerp(520, 820, k))
            if k > 0.6:
                for i, (px, col, hair) in enumerate(((620, "#0EA5E9", "#3F2A1E"), (740, "#E11D48", "#1F2937"))):
                    person(c, px, 1215, 330, col, t + i, pose="look", face=-1, hair=hair, a=prog(k, 0.6, 1.0))
        else:
            wall_room(c, t)
            frown = prog(t, T["nobody"] - 0.2, T["nobody"] + 0.3)
            for i, (px, col, hair) in enumerate(((620, "#0EA5E9", "#3F2A1E"), (740, "#E11D48", "#1F2937"))):
                person(c, px, 1215, 330, col, t + i, pose="shrug" if frown > 0.5 else "look", face=-1, hair=hair)
            stamp(c, 540, 640, 520, 170, prog(t, T["nosale1"] - 0.1, T["nosale1"] + 0.25))

    def ui_wall(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "y1957", T["bubble"] - 0.1, T["invented"] - 0.05, accent="#FDE68A", size=56)
            self.chip(540, 300, "wall", T["invented"] - 0.05, s("break1") + 0.1, accent=HILITE, size=50)
        else:
            self.chip(540, 300, "nosale", T["nobody"] - 0.1, T["box"] - 0.6, accent=WARN, size=54)
            self.chip(540, 300, "box", T["box"] - 0.6, s("fix1") - 0.1, accent=HILITE, size=40)
            self.badge("alert", T["nosale1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["nosale1"], 1.2)

    # ------------------------------------------------------------------ set: box (fix1, break2, fix2, cta)
    def draw_box(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        vrect(c, 0, 0, W, H, ["#111827", "#1E293B"])
        c.drawRect(R(0, 1180, W, 200), P("#0B1220"))
        add_glow(c, 540, 700, 620, "#38BDF8", 0.12)
        dy = 0.0
        if ph == "fix1":
            d = prog(t, T["drop1"], T["drop1"] + 0.35)
            dy = -220 * (1 - e_in(d))
        elif ph == "fix2":
            d = prog(t, T["drop2"], T["drop2"] + 0.35)
            dy = -220 * (1 - e_in(d)) if t >= s("fix2") else 0
        bx, by = 540, 1180 + dy
        x0, y0, x1, y1 = card_box(c, bx, by, 760, 620)
        floor_y = y1
        if ph == "fix1":
            hit = T["drop1"] + 0.35
            sq = 1.0 - 0.38 * math.sin(math.pi * clamp((t - hit) / 0.5)) * math.exp(-max(0.0, t - hit) * 2) if t >= hit else 1.0
            pk = prog(t, s("fix1"), T["air"] + 0.2)
            air_pillow(c, bx, floor_y, 560, 260, t, a=pk, squash=sq)
            vase(c, bx, floor_y - 260 * sq * pk + 6, 0.95)
        elif ph == "break2":
            pp = prog(t, T["pop1"], T["pop1"] + 0.25)
            fall = prog(t, T["pop1"] + 0.1, T["pop1"] + 0.45)
            air_pillow(c, bx, floor_y, 560, 260, t, squash=1.0, popped=pp)
            if fall < 1:
                vase(c, bx, lerp(floor_y - 254, floor_y, e_in(fall)), 0.95)
            else:
                vase(c, bx, floor_y, 0.95, broken=0.6 + 0.4 * prog(t, T["pop1"] + 0.45, T["pop1"] + 0.8))
            pop_burst(c, bx, floor_y - 130, prog(t, T["pop1"], T["pop1"] + 0.4), r=200)
        else:                                          # fix2 and cta: a sheet of tiny bubbles round the vase
            wrap = prog(t, s("fix2"), T["tiny"] + 0.5) if ph == "fix2" else 1.0
            hit = T["drop2"] + 0.35
            sq = 1.0 - 0.12 * math.sin(math.pi * clamp((t - hit) / 0.4)) if (ph == "fix2" and t >= hit) else 1.0
            sheet(c, x0 + 10, floor_y - 170 * sq, x1 - 10, floor_y - 4, 24, a=wrap, t=t, squash=sq,
                  popped={(1, 6)} if (ph != "fix2" or t >= T["pop"] + 0.1) else ())
            vase(c, bx, floor_y - 170 * sq + 8, 0.95)
            for sd in (-1, 1):                          # bubble wrap up both sides of the vase
                c.save()
                c.clipRect(R(bx + (sd < 0) * -230 + (sd > 0) * 110, floor_y - 470, 120, 300))
                sheet(c, bx - 230 if sd < 0 else bx + 110, floor_y - 470, bx - 110 if sd < 0 else bx + 230, floor_y - 168, 20,
                      a=wrap, t=t, film=False)
                c.restore()
            if ph == "fix2":
                pk = prog(t, T["pop"] - 0.5, T["pop"])
                pin(c, x0 + 10 + 24 * 1.2 + 6 * 24 * 2.25 + 24 * 1.125, floor_y - 170 * sq + 24 * 1.2 + 24 * 2.25 * 0.87 - 30 * (1 - pk),
                    a=pk * (1 - prog(t, T["pop"] + 0.3, T["pop"] + 0.6)))
                pop_burst(c, x0 + 10 + 24 * 1.2 + 6 * 24 * 2.25 + 24 * 1.125, floor_y - 170 + 24 * 1.2 + 24 * 2.25 * 0.87,
                          prog(t, T["pop"], T["pop"] + 0.35), r=60)

    def ui_box(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix1":
            self.chip(540, 300, "air", T["air"] - 0.2, T["squish"] - 0.1, accent="#38BDF8", size=56)
            self.chip(540, 300, "spring", T["squish"] - 0.1, s("break2") - 0.15, accent=GOOD, size=42)
            self.badge("check", T["spring1"], s("break2") - 0.15, x=920, y=440)
        elif ph == "break2":
            self.chip(540, 300, "pops", T["pillow"] - 0.2, T["floor"] - 0.1, accent=WARN, size=50)
            self.chip(540, 300, "smash", T["floor"] - 0.1, s("fix2") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["pop1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["pop1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "tiny", T["tiny"] - 0.2, T["pop"] - 0.1, accent="#38BDF8", size=50)
            self.chip(540, 300, "hold", T["pop"] - 0.1, s("break3") - 0.15, accent=GOOD, size=44)
            self.badge("check", T["hold1"], s("break3") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: factory (break3, fix3)
    def draw_factory(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        vrect(c, 0, 0, W, H, ["#1C1917", "#292524"])
        c.drawRect(R(0, 1200, W, 200), P("#0C0A09"))
        if ph == "break3":
            red_k = prog(t, s("break3"), T["million1"])
            person(c, 380, 1210, 520, "#0EA5E9", t, pose="carry", face=1, skin=mix("#E8B48A", "#EF4444", 0.5 * red_k))
            br = lerp(10, 46, (t * 0.9) % 1.0)
            c.drawCircle(520, 830, br, P("#F472B6", 0.9))
            c.drawCircle(520 - br * 0.3, 830 - br * 0.3, br * 0.25, P("#FFFFFF", 0.7))
            rng = random.Random(6)                       # the pile of tiny balloons so far
            for k in range(int(4 + 10 * red_k)):
                c.drawCircle(700 + rng.uniform(-60, 220), 1190 - rng.uniform(0, 70), rng.uniform(18, 28),
                             P(rng.choice(["#F472B6", "#60A5FA", "#FACC15", "#34D399"]), 0.9))
            for k in range(3):                           # sweat
                u = (t * 1.3 + k / 3) % 1.0
                c.drawCircle(300 - k * 20, 620 + u * 120, 9, P("#7DD3FC", 1 - u))
        else:
            seal = prog(t, T["sheet"] - 0.2, T["sheet"] + 0.4)
            # the hot film from the extruder down onto the drum
            c.drawRRect(rr(150, 380, 300, 170, 20), P("#57534E"))
            c.drawRRect(rr(150, 380, 300, 170, 20), P("#A8A29E", 1, stroke=4))
            c.drawRect(R(280, 550, 40, 40), P("#78716C"))
            hot = prog(t, T["plastic"] - 0.2, T["plastic"] + 0.3)
            c.drawLine(300, 590, 300, 650, P("#FB923C", hot, stroke=14))
            add_glow(c, 300, 620, 90, "#FB923C", 0.5 * hot)
            drum(c, 420, 860, 220, t, suck=prog(t, T["cups"] - 0.3, T["cups"] + 0.2))
            arc = skia.Path()
            arc.addArc(R(420 - 232, 860 - 232, 464, 464), 180, 130 * hot)
            c.drawPath(arc, P("#FDBA74", 0.85 * hot, stroke=12))
            # the flat top film from a small roller
            c.drawCircle(700, 720, 70, lin_paint(630, 650, 770, 790, ["#E7E5E4", "#78716C"]))
            c.drawLine(700, 650, 760, 560, P("#E0F2FE", 0.8 * seal, stroke=8))
            # bubble wrap going out to the right and rolling up
            out = prog(t, T["sheet"], T["seal1"] + 0.6)
            if out > 0:
                c.save()
                c.clipRect(R(560, 980, 520 * out + 1, 220))
                sheet(c, 560, 990, 1080, 1180, 20, a=1.0, t=t)
                c.restore()
            roll(c, 930, 820, 120 * (0.4 + 0.6 * out), t, a=out)

    def ui_factory(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "million", T["blow"] - 0.2, s("fix3") - 0.15, accent=WARN, size=52)
            self.chip(760, 600, "puff", T["million1"], s("fix3") - 0.15, accent="#F8FAFC", size=38)
            self.badge("alert", T["million1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["million1"], 1.2)
        else:
            self.chip(540, 300, "cups", T["plastic"] - 0.2, T["sheet"] - 0.1, accent="#FB923C", size=42)
            self.chip(540, 300, "seal", T["sheet"] - 0.1, s("break4") - 0.15, accent=GOOD, size=38)
            self.badge("check", T["seal1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: truck (break4, fix4)
    def draw_truck(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        vrect(c, 0, 0, W, 1060, ["#0C4A6E", "#38BDF8", "#BAE6FD"], [0, 0.6, 1])
        c.drawRect(R(0, 1060, W, H - 1060), P("#374151"))
        for k in range(8):
            xx = (k * 200 - t * 600) % 1400 - 200
            c.drawRect(R(xx, 1150, 110, 14), P("#F8FAFC", 0.8))
        if ph == "break4":
            truck(c, 560, 1060, 1.0, t, cargo="air", xray=prog(t, T["truck"], T["truck"] + 0.4),
                  coins=prog(t, T["money"] - 0.4, T["money"]))
        else:
            k = prog(t, T["pumped"] - 0.5, T["pumped"])
            if k < 1:
                truck(c, 560, 1060, 1.0, t, cargo="flat", xray=1.0)
            if k > 0:                                  # the packing table with its little pump
                c.drawRect(R(0, 0, W, H), P("#0F172A", 0.85 * k))
                c.drawRRect(rr(80, 980, 920, 50, 14), P("#A16207", k))
                c.drawRRect(rr(140, 800, 220, 180, 20), P("#475569", k))
                c.drawCircle(250, 880, 46, P("#94A3B8", k))
                c.save()
                c.translate(250, 880)
                c.rotate(t * 500)
                for j in range(4):
                    c.rotate(90)
                    c.drawLine(0, 0, 0, -38, P("#1E293B", k, stroke=8))
                c.restore()
                c.drawLine(360, 960, 1000, 960, P("#E0F2FE", 0.7 * k, stroke=6))      # the flat film going in
                blown = prog(t, T["pumped"], T["pack"] + 0.5)
                n = int(10 * blown)
                for j in range(n):
                    bubble(c, 400 + j * 60, 930, 28, a=k)
                for j in range(n, 10):
                    c.drawRRect(rr(372 + j * 60, 952, 56, 10, 4), P("#E0F2FE", 0.5 * k))
                vase(c, 820, 930 - 56, 0.5, a=prog(t, T["pack"] - 0.2, T["pack"] + 0.2))

    def ui_truck(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "mostly", T["truck"] - 0.1, T["money"] - 0.3, accent=WARN, size=56)
            self.chip(540, 300, "money", T["money"] - 0.3, s("fix4") - 0.15, accent="#FACC15", size=50)
            self.badge("alert", T["air1"], s("fix4") - 0.2, x=920, y=440)
            self.red(T["air1"], 1.2)
        else:
            self.chip(540, 300, "flat", T["flat"] - 0.2, T["pumped"] - 0.2, accent="#CBD5E1", size=56)
            self.chip(540, 300, "pumped", T["pumped"] - 0.2, s("cta") - 0.15, accent=GOOD, size=44)
            self.badge("check", T["pack1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: computer (reveal)
    def draw_computer(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1E1B4B", "#312E81"])
        c.drawRect(R(0, 1180, W, 200), P("#111827"))
        for k in range(9):
            c.drawLine(k * 140, 1180, k * 140 - 80, 1400, P("#1F2937", 1, stroke=3))
        wrap = prog(t, T["computer"], T["wrapped"] + 0.3)
        crate = prog(t, T["wrapped"] + 0.2, s("stat") - 0.1)
        computer(c, 540, 1180, 1.05, t, wrap=wrap, crate=crate)

    def ui_computer(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "ibm", T["ibm"] - 0.15, T["computer"] - 0.15, accent=HILITE, size=64)
        self.chip(540, 300, "new", T["computer"] - 0.15, T["wrapped"] - 0.1, accent="#FBBF24", size=48)
        self.chip(540, 300, "safe", T["wrapped"] - 0.1, s("stat") - 0.15, accent=GOOD, size=46)

    # ------------------------------------------------------------------ set: sheet (stat, closer)
    def draw_sheet(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "stat":
            vrect(c, 0, 0, W, H, ["#0C4A6E", "#155E75"])
            sheet(c, -40, 600, W + 40, 1240, 46, a=1.0, t=t, wobble=6)
        else:
            vrect(c, 0, 0, W, H, ["#1E1B4B", "#0E7490"])
            add_glow(c, 560, 760, 560, "#67E8F9", 0.25)
            un = e_out(prog(t, s("closer") - 0.1, s("closer") + 1.2))
            roll(c, 780, 780, 260, t, unroll=un, big=True)
            for k in range(8):
                u = (t * 0.4 + k / 8) % 1.0
                add_glow(c, 200 + k * 90, lerp(1100, 400, u), 26, "#FFFFFF", 0.6 * math.sin(u * math.pi))

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:                              # a giant box, a mountain of bubble wrap, one tiny charger
            vrect(c, 0, 0, W, H, ["#334155", "#475569"])
            c.drawRect(R(0, 1120, W, 300), P("#78350F"))
            c.drawRRect(rr(60, 380, 300, 740, 10), P("#7C2D12"))           # the front door
            c.drawCircle(320, 760, 14, P("#FACC15"))
            x0, y0, x1, y1 = card_box(c, 650, 1150, 620, 520)
            spill = prog(t, T["t_giant"] - 0.3, T["t_ten"] + 0.4)
            for k in range(3):
                c.save()
                c.translate(650, y1 - 30)
                c.rotate(-24 + k * 24)
                sheet(c, -150, -230 - 240 * spill, 150, 0, 30, a=0.75, t=t, film=True, tint="#93C5FD")
                c.restore()
            up = prog(t, T["t_charger"] - 0.2, T["t_charger"] + 0.3)
            person(c, 270, 1200, 420, "#22C55E", t, pose="shrug" if T["t_ten"] <= t else "carry", face=1)
            c.drawRRect(rr(390, 790 - 40 * up, 44, 30, 8), P("#F8FAFC", up))
            c.drawLine(412, 820 - 40 * up, 412, 870 - 40 * up, P("#F8FAFC", up, stroke=5))
        else:                                         # mom's new sofa still in its plastic
            vrect(c, 0, 0, W, H, ["#3B1F1A", "#57302A"])
            c.drawRect(R(0, 1120, W, 300), P("#7C5A3A"))
            for k in range(6):
                c.drawRect(R(k * 190, 1120, 150, 300), P("#8B6A45", 0.5))
            sofa_plastic(c, 540, 1130, t, crinkle=prog(self.T["t_giant"], 0, 1))
            person(c, 860, 1200, 440, "#0F766E", t, pose="point", face=-1, hair="#111827")
            person(c, 440, 1000, 300, "#F97316", t, pose="sit", face=1)
            cal = prog(t, T["t_ten"] - 0.3, T["t_ten"] + 0.2)
            if cal > 0:
                c.drawRRect(rr(120, 420, 200, 220, 18), P("#F8FAFC", cal))
                c.drawRect(R(120, 420, 200, 60), P("#DC2626", cal))
                for i in range(5):
                    c.drawLine(150 + i * 32, 520, 170 + i * 32, 600, P("#111827", cal, stroke=6))
                c.drawLine(140, 580, 300, 540, P("#111827", cal, stroke=6))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "charger", T["t_charger"] - 0.15, T["t_ten"] - 0.15, accent="#F8FAFC", size=46)
        self.chip(540, 300, "feet", T["t_ten"] - 0.15, self.duration + 1, accent=HILITE, size=50)

    def ui_sheet(self, c, t, tw):
        T, s = self.T, self.tl.s
        if self.phase(tw) == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=52)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1F2937", "#111827"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["bubble"], sfx.sparkle(1.0, 10, 62), -10),
              (T["wallpaper"], sfx.ding(), -9)]
        ev += [(T["nosale1"], sfx.thud(0.4, 63), -4), (T["nosale1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["drop1"] + 0.35, sfx.thud(0.3, 65), -6),
               (T["drop1"] + 0.4, sfx.creak(0.6, 66), -12), (T["spring1"], sfx.ding(), -8), (T["spring1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pop1"], sfx.snap(67), -2), (T["pop1"] + 0.4, sfx.clank(900.0, 0.4, 68), -6),
               (T["pop1"] + 0.45, sfx.womp(), -10), (T["pop1"] + 0.6, sfx.alarm(3, 820.0), -12)]
        ev += [(T["pop"], sfx.pop(69), -2), (T["drop2"] + 0.35, sfx.thud(0.3, 70), -8),
               (T["hold1"], sfx.ding(), -8), (T["hold1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, False, 71), -6), (T["blow"], sfx.hiss(0.8, 72), -14),
               (T["million1"], sfx.womp(), -10), (T["million1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["plastic"], sfx.sizzle(0.8, 73), -12), (T["cups"], sfx.whirr(1.2, 140.0, 220.0, 74), -12),
               (T["seal1"], sfx.ding(), -8), (T["seal1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 75), -6), (T["truck"], sfx.hum(1.5, 70.0), -14),
               (T["money"], sfx.sparkle(0.6, 8, 76), -10), (T["air1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["pumped"], sfx.whirr(1.0, 300.0, 420.0, 77), -12), (T["pack1"], sfx.ding(), -8),
               (T["pack1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 94), -6), (T["ibm"], sfx.ding(), -6),
               (T["wrapped"] + 0.5, sfx.thud(0.4, 95), -8)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 103), -6), (T["t_giant"], sfx.creak(0.6, 104), -10),
               (T["t_ten"], sfx.womp(), -8)]
        for k in range(3):                             # a few bubble pops under the closer and the tag
            ev.append((T["cong2"] + 0.5 + k * 0.4, sfx.pop(110 + k), -12))
        return ev


NAME = "bubblewrap"
EPISODE = BubbleWrap
