"""Episode 114 - an aluminum soda can (the wall is less than a tenth of a millimetre thick, the fizz pushes up to about
90 psi, the domed bottom holds the push, the body is punched from a flat disk and drawn through rings, a coating
inside keeps the metal taste out, the stay-on tab; a full can is stronger than an empty one).  v2 look.
No brand, label or writing on any can.

Sets: table (hook: a magnifier on the can's wall next to a sheet of paper, the same thickness; cta; stat; closer: the
cold can with drops and fizz, for the cover), pressure (break1: the fizz pushes out on every wall like a car tyre;
fix1: a flat bottom bulges, the dome holds), factory (break2: a flat disk and a tall can, how?; fix2: punched into a
cup, then pushed through rings, taller and thinner), taste (break3: a sip that tastes like metal; fix3: a thin plastic
coat sprayed inside), beach (break4: old tabs that came off, all over the beach; fix4: today's tab is a lever that
stays on), squeeze (reveal: an empty can crumples in a hand, the full one barely dents), tag (a friend shakes the can
and hands it over: spray).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

ALU = ("#D9DEE6", "#AEB6C2", "#7C8594", "#4B5361")     # aluminium: light, mid, dark, deep
BAND = ("#14B8A6", "#0F766E")
SKIN = ("#E0A57A", "#B97D55")
CX, TOP, BOT, RW = 540, 470, 1090, 170               # the can on the table: centre x, lid y, bottom y, half width


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== the can
def can_path(cx, top, bot, rw):
    """Side outline: lid rim, tapered neck, straight body, the rounded foot."""
    nw = rw * 0.8
    p = skia.Path()
    p.moveTo(cx - nw, top)
    p.lineTo(cx + nw, top)
    p.cubicTo(cx + nw, top + 30, cx + rw, top + 34, cx + rw, top + 64)
    p.lineTo(cx + rw, bot - 34)
    p.cubicTo(cx + rw, bot - 8, cx + rw * 0.86, bot, cx + rw * 0.74, bot)
    p.lineTo(cx - rw * 0.74, bot)
    p.cubicTo(cx - rw * 0.86, bot, cx - rw, bot - 8, cx - rw, bot - 34)
    p.lineTo(cx - rw, top + 64)
    p.cubicTo(cx - rw, top + 34, cx - nw, top + 30, cx - nw, top)
    p.close()
    return p


def can(c, cx=CX, top=TOP, bot=BOT, rw=RW, t=0.0, a=1.0, drops=0.0, xray=0.0, band=True, dent=0.0, crumple=0.0,
        shake=0.0, cold=0.0):
    """A plain aluminium can (no writing). xray 0..1 fades the skin to an outline."""
    if a <= 0:
        return
    c.save()
    if shake:
        c.rotate(shake, cx, (top + bot) / 2)
    p = can_path(cx, top, bot, rw)
    if crumple > 0 or dent > 0:                          # squeeze the middle in
        k = crumple * 0.55 + dent * 0.08
        q = skia.Path()
        m = skia.PathMeasure(p, True)
        n = 160
        L = m.getLength()
        for i in range(n + 1):
            pos, _ = m.getPosTan(L * i / n)
            x, y = pos.x(), pos.y()
            mid = math.exp(-((y - (top + bot) / 2) / ((bot - top) * 0.22)) ** 2)
            wob = 1 + (crumple * 0.18 * math.sin(y * 0.09)) if crumple else 1
            x = cx + (x - cx) * (1 - k * mid * wob)
            (q.moveTo if i == 0 else q.lineTo)(x, y)
        q.close()
        p = q
    skin = 1 - xray
    if skin > 0:
        c.drawPath(p, lin_paint(cx - rw, 0, cx + rw, 0, [ALU[3], ALU[1], ALU[0], ALU[1], ALU[2], ALU[3]],
                                [0.0, 0.2, 0.36, 0.55, 0.8, 1.0], a=a * skin))
        if band:
            c.save()
            c.clipPath(p, skia.ClipOp.kIntersect, True)
            wave = skia.Path()
            y0 = top + (bot - top) * 0.42
            wave.moveTo(cx - rw - 10, y0)
            for i in range(21):
                x = cx - rw + i * rw / 10
                wave.lineTo(x, y0 + 26 * math.sin(i * 0.7 + 0.4))
            wave.lineTo(cx + rw + 10, bot - 150)
            wave.lineTo(cx - rw - 10, bot - 150)
            wave.close()
            c.drawPath(wave, lin_paint(cx - rw, 0, cx + rw, 0, [BAND[1], BAND[0], "#5EEAD4", BAND[0], BAND[1]], a=a * skin))
            for j in range(6):                           # little bubbles printed on the band (a pattern, no words)
                c.drawCircle(cx - rw * 0.6 + j * rw * 0.25, y0 + 90 + (j % 2) * 40, 10 + (j % 3) * 4, P("#CCFBF1", 0.55 * a * skin))
            c.drawRect(R(cx - rw * 0.55, top + 64, rw * 0.18, bot - top - 110), P("#FFFFFF", 0.22 * a * skin))
            c.restore()
        if crumple > 0:
            for j in range(9):
                yy = top + 120 + j * 50
                c.drawLine(cx - rw * 0.5, yy, cx + rw * 0.4, yy + 18 * math.sin(j * 1.7), P(ALU[3], 0.6 * crumple * a, stroke=3))
    c.drawPath(p, P(ALU[3], a, stroke=4))
    # the lid seen a little from above
    c.drawOval(R(cx - rw * 0.8, top - 16, rw * 1.6, 32), P(ALU[1], a))
    c.drawOval(R(cx - rw * 0.8, top - 16, rw * 1.6, 32), P(ALU[3], a, stroke=3))
    c.drawOval(R(cx - rw * 0.55, top - 10, rw * 0.6, 18), P(ALU[2], a))
    if drops > 0:                                        # cold drops
        rng = random.Random(7)
        for j in range(34):
            x = cx + rng.uniform(-rw * 0.85, rw * 0.85)
            y = rng.uniform(top + 90, bot - 50)
            r = rng.uniform(4, 9)
            y += ((t * rng.uniform(4, 14)) % 60) if j % 4 == 0 else 0
            c.drawCircle(x, y, r, P("#E0F2FE", 0.55 * drops * a))
            c.drawCircle(x - r * 0.3, y - r * 0.3, r * 0.35, P("#FFFFFF", 0.8 * drops * a))
    if cold > 0:
        for j in range(5):
            q = (t * 0.25 + j * 0.2) % 1.0
            puff(c, cx + math.sin(j * 2.1) * rw * 0.7, top - 20 - q * 120, 40 + q * 60, "#E0F2FE", 0.18 * cold * (1 - q))
    c.restore()


def table(c, y=BOT, night=0.0):
    vrect(c, 0, 0, W, y + 10, [mix("#1E2240", "#0B0E1E", night), mix("#2B2F55", "#121630", night)])
    c.drawRect(R(0, y, W, 1250 - y), lin_paint(0, y, 0, 1250, ["#7A5236", "#4A3020"]))
    c.drawLine(0, y, W, y, P("#A0714D", 1, stroke=4))
    for k in range(5):
        c.drawLine(0, y + 26 + k * 30, W, y + 30 + k * 30, P("#5A3A26", 0.5, stroke=2))
    contact_shadow(c, CX, y, RW * 2.4, 0.55, 26)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#140E0A", "#050302"]))


def lens(c, x, y, r, t, k=1.0, wall=1.0, paper=1.0):
    """A magnifier: the can's wall (a thin metal edge) beside a sheet of paper, the same thickness."""
    if k <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(e_back(clamp(k)), e_back(clamp(k)))
    c.drawLine(r * 0.7, r * 0.7, r * 1.3, r * 1.3, P("#5B3A21", 1, stroke=34))
    c.save()
    c.clipRRect(skia.RRect.MakeOval(R(-r, -r, 2 * r, 2 * r)), skia.ClipOp.kIntersect, True)
    c.drawRect(R(-r, -r, 2 * r, 2 * r), P("#101827"))
    if wall > 0:                                         # the wall's edge, curved, very thin
        p = skia.Path()
        p.moveTo(-r * 0.75, -r)
        p.quadTo(-r * 0.35, 0, -r * 0.75, r)
        c.drawPath(p, P("#E5E7EB", wall, stroke=12))
        add_glow(c, -r * 0.5, 0, 60, "#E5E7EB", 0.25 * wall)
    if paper > 0:                                        # a sheet of paper, edge on
        c.drawRect(R(r * 0.2, -r, 12, 2 * r), P("#FEF3C7", paper))
        c.drawRect(R(r * 0.2 + 14, -r, r, 2 * r), P("#FEF3C7", 0.14 * paper))
    c.restore()
    c.drawCircle(0, 0, r, P("#E5E7EB", 1, stroke=12))
    c.drawCircle(0, 0, r - 8, P("#FFFFFF", 0.25, stroke=3))
    c.restore()


# ====================================================================================== pressure and the dome
def xray_can(c, t, push=0.0, bottom=0.0, dome=0.0, rock=0.0):
    vrect(c, 0, 0, W, 1250, ["#0E1430", "#16204A"])
    c.save()
    if rock:
        c.rotate(rock * math.sin(t * 9) * 6, CX, BOT)
    can(c, t=t, xray=0.85, band=False)
    c.save()
    c.clipPath(can_path(CX, TOP, BOT, RW), skia.ClipOp.kIntersect, True)
    rng = random.Random(3)
    for j in range(60):                                  # the fizz
        q = (t * rng.uniform(0.2, 0.5) + rng.random()) % 1.0
        x = CX + rng.uniform(-RW * 0.85, RW * 0.85)
        y = lerp(BOT - 20, TOP + 60, q)
        c.drawCircle(x, y, rng.uniform(4, 10), P("#BAE6FD", 0.5))
    c.restore()
    if push > 0:                                         # arrows pushing out on every wall
        for j in range(7):
            y = TOP + 110 + j * 70
            for sd in (-1, 1):
                x0 = CX + sd * (RW - 60)
                x1 = CX + sd * (RW + 30 + 50 * push)
                c.drawLine(x0, y, x1, y, P(WARN, push, stroke=10))
                poly(c, [(x1 + sd * 22, y), (x1, y - 16), (x1, y + 16)], WARN, push)
        for sd in (-1, 0, 1):
            x = CX + sd * 70
            c.drawLine(x, TOP + 60, x, TOP - 40 - 40 * push, P(WARN, push, stroke=10))
            poly(c, [(x, TOP - 62 - 40 * push), (x - 16, TOP - 40 - 40 * push), (x + 16, TOP - 40 - 40 * push)], WARN, push)
    if bottom > 0:                                       # the bottom: flat bulging out, or a dome curved in
        y = BOT - 20
        p = skia.Path()
        p.moveTo(CX - RW * 0.74, y)
        bulge = 70 * bottom * (1 - dome)
        dip = -60 * dome
        p.quadTo(CX, y + bulge + dip, CX + RW * 0.74, y)
        col = mix(WARN, GOOD, dome)
        c.drawPath(p, P(col, 1, stroke=18))
        add_glow(c, CX, y + (bulge + dip) / 2, 180, col, 0.45)
        if dome > 0.5:
            for j in range(5):
                x = CX - 100 + j * 50
                yy = y + dip * (1 - ((x - CX) / (RW * 0.74)) ** 2) / 2
                c.drawLine(x, yy - 70, x, yy - 14, P(HILITE, dome, stroke=6))
                poly(c, [(x, yy - 4), (x - 10, yy - 18), (x + 10, yy - 18)], HILITE, dome)
    c.restore()
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


def tire_gauge(c, x, y, r, frac, a=1.0):
    """A pressure dial with a car tyre beside it: the fizz pushes as hard as a car tyre."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#0F172A", 0.92 * a))
    c.drawCircle(x, y, r, P("#E2E8F0", a, stroke=7))
    arc = skia.Path()
    arc.addArc(R(x - r * 0.78, y - r * 0.78, r * 1.56, r * 1.56), 150, 240 * clamp(frac))
    c.drawPath(arc, P(WARN, a, stroke=14))
    ang = math.radians(150 + 240 * clamp(frac))
    c.drawLine(x, y, x + math.cos(ang) * r * 0.7, y + math.sin(ang) * r * 0.7, P("#F8FAFC", a, stroke=6))
    c.drawCircle(x - r * 1.9, y, r * 0.8, P("#111827", a))
    c.drawCircle(x - r * 1.9, y, r * 0.8, P("#374151", a, stroke=14))
    c.drawCircle(x - r * 1.9, y, r * 0.36, P("#9CA3AF", a))
    text(c, "=", x - r * 0.95, y + 22, 64, "#F8FAFC", "Poppins-Black", a=a)


# ====================================================================================== the factory
def factory(c, t, stage=0.0, ram=0.0, q_mark=0.0):
    """A flat disk -> a cup -> through the rings -> a tall can body. stage 0..3."""
    vrect(c, 0, 0, W, 1250, ["#1B2133", "#2A3148"])
    c.drawRect(R(0, 1000, W, 60), P("#3F4659"))         # the line
    for k in range(14):
        c.drawLine((k * 90 + t * 120) % (W + 90) - 45, 1000, (k * 90 + t * 120) % (W + 90) - 45, 1060, P("#2A3040", 1, stroke=6))
    # the press ram over the left station
    ry = lerp(560, 820, clamp(ram))
    c.drawRect(R(200 - 14, 300, 28, ry - 300), P("#64748B"))
    c.drawRRect(rr(200 - 90, ry, 180, 60, 10), P("#94A3B8"))
    c.drawRRect(rr(200 - 90, ry, 180, 60, 10), P("#475569", 1, stroke=4))
    # the disk / the cup at the press
    if stage < 1:
        c.drawOval(R(200 - 120, 960, 240, 40), P(ALU[0]))
        c.drawOval(R(200 - 120, 960, 240, 40), P(ALU[3], 1, stroke=3))
    else:
        cup = skia.Path()
        cup.moveTo(200 - 95, 880)
        cup.lineTo(200 - 95, 990)
        cup.quadTo(200, 1004, 200 + 95, 990)
        cup.lineTo(200 + 95, 880)
        c.drawPath(cup, lin_paint(105, 0, 295, 0, [ALU[2], ALU[0], ALU[2]]))
        c.drawOval(R(200 - 95, 868, 190, 26), P(ALU[3]))
    # the rings (ironing dies) and the tall body
    k = clamp(stage - 1.0)
    for j in range(3):
        x = 460 + j * 110
        c.drawOval(R(x - 18, 760, 36, 240), P("#F59E0B", 0.9))
        c.drawOval(R(x - 10, 780, 20, 200), P("#1B2133"))
    if k > 0:                                            # the cup pushed through the rings, growing taller
        x = lerp(380, 880, smooth(k))
        h = lerp(130, 420, smooth(k))
        w = lerp(190, 160, smooth(k))
        body = skia.Path()
        body.moveTo(x - w / 2, 1000 - h)
        body.lineTo(x - w / 2, 990)
        body.quadTo(x, 1004, x + w / 2, 990)
        body.lineTo(x + w / 2, 1000 - h)
        c.drawPath(body, lin_paint(x - w / 2, 0, x + w / 2, 0, [ALU[2], ALU[0], ALU[1], ALU[2]]))
        c.drawOval(R(x - w / 2, 1000 - h - 12, w, 24), P(ALU[3]))
        c.drawLine(x + 56, 1000 - h + 20, x + 56, 960, P("#FFFFFF", 0.3, stroke=8))
    if q_mark > 0:                                       # the tall can it has to become, as a ghost
        dashed(c, 800, 580, 800, 1000, "#F8FAFC", 4, 16, 10, t * 30, q_mark)
        dashed(c, 960, 580, 960, 1000, "#F8FAFC", 4, 16, 10, t * 30, q_mark)
        dashed(c, 800, 580, 960, 580, "#F8FAFC", 4, 16, 10, t * 30, q_mark)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


# ====================================================================================== the taste
def drinker(c, t, sip=0.0, yuck=0.0, happy=0.0):
    vrect(c, 0, 0, W, 1250, ["#2A1E3F", "#3B2A55"])
    c.save()
    c.translate(360, 760)
    c.scale(1.6, 1.6)
    c.drawRRect(rr(-130, 120, 260, 260, 90), P("#2563EB"))          # shoulders
    c.drawCircle(0, 0, 120, P(SKIN[0]))
    c.drawArc(R(-124, -128, 248, 170), 180, 175, True, P("#2B2530"))
    c.drawCircle(-36, 6, 22, P(SKIN[1]))                             # ear
    c.drawCircle(70, -20, 9, P("#1F2937"))                           # eye
    if yuck > 0:
        c.drawLine(52, -44, 88, -34 + 6 * yuck, P("#1F2937", 1, stroke=6))
        c.drawArc(R(64, 46, 48, 30), 200, 140, False, P("#7F1D1D", 1, stroke=6))
        c.drawCircle(112, 60, 7, P("#4ADE80", yuck))
    elif happy > 0:
        c.drawArc(R(60, 30, 54, 36), 20, 140, False, P("#7F1D1D", 1, stroke=6))
    nose = skia.Path()
    nose.moveTo(116, -10)
    nose.lineTo(140, 24)
    nose.lineTo(112, 30)
    nose.close()
    c.drawPath(nose, P(SKIN[0]))
    c.restore()
    ang = -50 * smooth(sip)                              # the can tipped to the mouth
    c.save()
    c.translate(600, 860)
    c.rotate(ang)
    c.scale(0.42, 0.42)
    c.translate(-CX, -(TOP + BOT) / 2)
    can(c, t=t)
    c.restore()
    if yuck > 0:                                         # a thought bubble full of nuts and bolts
        k = e_back(clamp(yuck))
        c.drawCircle(780, 470, 150 * k, P("#F8FAFC", 0.92))
        c.drawCircle(640, 610, 30 * k, P("#F8FAFC", 0.92))
        for j in range(5):
            x, y = 730 + (j % 3) * 50, 430 + (j // 3) * 60
            poly(c, [(x + 22 * math.cos(math.radians(60 * q + 30)), y + 22 * math.sin(math.radians(60 * q + 30))) for q in range(6)],
                 "#6B7280", k)
            c.drawCircle(x, y, 9, P("#F8FAFC", k))
    if happy > 0:
        for j in range(3):
            heart(c, 720 + j * 70, 470 - j * 40 - 30 * math.sin(t * 3 + j), 26, happy)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


def coat_can(c, t, spray=0.0, coat=0.0):
    vrect(c, 0, 0, W, 1250, ["#1B2133", "#2A3148"])
    can(c, t=t, xray=0.75, band=False)
    if coat > 0:                                         # the coat inside, a glossy layer
        p = can_path(CX, TOP + 8, BOT - 8, RW - 10)
        c.drawPath(p, P("#93C5FD", 0.85 * coat, stroke=10))
        add_glow(c, CX, (TOP + BOT) / 2, 260, "#93C5FD", 0.18 * coat)
    if spray > 0:                                        # the nozzle sprays a mist inside
        ny = lerp(TOP - 200, BOT - 120, clamp(spray))
        c.drawRect(R(CX - 8, TOP - 260, 16, ny - TOP + 260), P("#94A3B8"))
        c.drawRRect(rr(CX - 22, ny - 10, 44, 30, 8), P("#CBD5E1"))
        for j in range(26):
            ang = math.radians(j * 360 / 26 + t * 200)
            r = 30 + ((t * 400 + j * 37) % 120)
            c.drawCircle(CX + math.cos(ang) * r, ny + 10 + math.sin(ang) * r * 0.6, 4, P("#BFDBFE", 0.7))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


# ====================================================================================== the beach and the tab
def old_tab(c, x, y, s, ang, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    c.drawOval(R(-30, -14, 60, 28), P(ALU[0], a))
    c.drawOval(R(-30, -14, 60, 28), P(ALU[3], a, stroke=3))
    c.drawCircle(42, 0, 18, P(ALU[1], a, stroke=6))
    c.restore()


def beach(c, t, tabs=1.0, step=0.0):
    vrect(c, 0, 0, W, 560, ["#3B5A8C", "#C7687A", "#F4A95E"])
    c.drawRect(R(0, 560, W, 160), lin_paint(0, 560, 0, 720, ["#1E5F8C", "#2A7AA8"]))
    for k in range(8):
        xx = (k * 140 + t * 30) % (W + 140) - 70
        c.drawLine(xx, 600 + k * 14, xx + 70, 600 + k * 14, P("#BAE6FD", 0.4, stroke=3))
    c.drawRect(R(0, 720, W, 530), lin_paint(0, 720, 0, 1250, ["#C49A62", "#8E6A43"]))
    rng = random.Random(9)
    for j in range(26):
        old_tab(c, rng.uniform(60, W - 60), rng.uniform(780, 1200), rng.uniform(0.9, 1.4), rng.uniform(0, 360), tabs)
    if step > 0:                                         # a bare foot comes down on one: ouch
        fy = lerp(560, 940, e_in(clamp(step)))
        foot = skia.Path()
        foot.moveTo(560, fy - 200)
        foot.lineTo(560, fy - 40)
        foot.quadTo(560, fy, 640, fy)
        foot.lineTo(760, fy)
        foot.quadTo(800, fy - 20, 760, fy - 50)
        foot.lineTo(640, fy - 70)
        foot.lineTo(640, fy - 200)
        foot.close()
        c.drawPath(foot, P(SKIN[0]))
        c.drawPath(foot, P(SKIN[1], 1, stroke=4))
        if step >= 1:
            star = [(700 + math.cos(math.radians(i * 36)) * (60 if i % 2 else 26),
                     fy + 40 + math.sin(math.radians(i * 36)) * (60 if i % 2 else 26)) for i in range(10)]
            poly(c, star, WARN, 1.0)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#140E0A", "#050302"]))


def lid_top(c, t, lift=0.0, a=1.0):
    """The lid from above: the tab is a lever; lifting its ring pushes the scored flap in, and the tab stays on."""
    vrect(c, 0, 0, W, 1250, ["#1B2133", "#2A3148"])
    cx, cy, r = 540, 760, 380
    c.drawCircle(cx, cy, r, P(ALU[2]))
    c.drawCircle(cx, cy, r - 30, lin_paint(cx - r, cy - r, cx + r, cy + r, [ALU[0], ALU[1], ALU[2]]))
    c.drawCircle(cx, cy, r - 30, P(ALU[3], 1, stroke=6))
    # the scored flap near the edge (toward the top of the picture)
    flap = skia.Path()
    flap.moveTo(cx - 90, cy - 150)
    flap.quadTo(cx, cy - 300, cx + 90, cy - 150)
    flap.quadTo(cx, cy - 120, cx - 90, cy - 150)
    k = clamp(lift)
    c.drawPath(flap, P(mix(ALU[1], "#0B0E18", smooth(k * 1.4)), 1))
    c.drawPath(flap, P(ALU[3], 1, stroke=4))
    # the tab: a lever riveted in the middle; its nose presses the flap as the ring lifts
    c.drawCircle(cx, cy, 16, P(ALU[3]))
    c.save()
    c.translate(cx, cy)
    sy = 1 - 0.5 * k                                    # foreshortens as the ring end lifts toward us
    c.scale(1, sy)
    tab = skia.Path()
    tab.addRRect(rr(-60, -120, 120, 300, 50))
    hole = skia.Path()
    hole.addRRect(rr(-38, 40, 76, 110, 34))
    c.drawPath(tab, lin_paint(-60, 0, 60, 0, [ALU[2], ALU[0], ALU[2]]))
    c.drawPath(hole, P(ALU[3]))
    c.drawPath(tab, P(ALU[3], 1, stroke=4))
    c.restore()
    if k > 0.2:
        add_glow(c, cx, cy - 190, 120, GOOD, 0.4 * clamp((k - 0.2) / 0.5))
        c.drawLine(cx, cy - 120, cx, cy - 190, P(GOOD, clamp((k - 0.2) / 0.5), stroke=10))
        poly(c, [(cx, cy - 210), (cx - 16, cy - 186), (cx + 16, cy - 186)], GOOD, clamp((k - 0.2) / 0.5))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


# ====================================================================================== the squeeze
def hand(c, x, y, s, grip=0.0, a=1.0, flip=1):
    c.save()
    c.translate(x, y)
    c.scale(s * flip, s)
    palm = skia.Path()
    palm.addRRect(rr(-40, -90, 120, 180, 50))
    c.drawPath(palm, P(SKIN[0], a))
    for j in range(4):
        fy = -70 + j * 44
        c.drawRRect(rr(60 - 40 * grip, fy, 90 - 30 * grip, 34, 17), P(SKIN[0], a))
        c.drawRRect(rr(60 - 40 * grip, fy, 90 - 30 * grip, 34, 17), P(SKIN[1], a, stroke=3))
    c.drawPath(palm, P(SKIN[1], a, stroke=3))
    c.restore()


def squeeze(c, t, empty_k=0.0, full_k=0.0, arrows=0.0):
    vrect(c, 0, 0, W, 1250, ["#1B2133", "#2A3148"])
    for cx, k, crumple, dent in ((290, empty_k, empty_k, 0.0), (790, full_k, 0.0, full_k)):
        c.save()
        c.translate(cx - CX * 0.62, 260)
        c.scale(0.62, 0.62)
        can(c, t=t, crumple=crumple, dent=dent, drops=0.0 if crumple else 0.8)
        c.restore()
        hx = cx - 0.62 * RW - 70 + 40 * k
        hand(c, hx, 260 + 0.62 * (TOP + BOT) / 2, 0.9, grip=k)
        hand(c, 2 * cx - hx, 260 + 0.62 * (TOP + BOT) / 2, 0.9, grip=k, flip=-1)
    if arrows > 0:                                       # inside the full can, the fizz pushes the wall tight
        for j in range(5):
            y = 260 + 0.62 * (TOP + 120 + j * 90)
            for sd in (-1, 1):
                x0, x1 = 790 + sd * 20, 790 + sd * (0.62 * RW - 10)
                c.drawLine(x0, y, x1, y, P(HILITE, arrows, stroke=7))
                poly(c, [(x1 + sd * 16, y), (x1, y - 12), (x1, y + 12)], HILITE, arrows)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


# ====================================================================================== the tag
def tag_scene(c, t, shake=0.0, hand_over=0.0, burst=0.0, t_burst=0.0):
    vrect(c, 0, 0, W, 1250, ["#28304F", "#3A3060"])
    c.drawRect(R(0, 1060, W, 190), lin_paint(0, 1060, 0, 1250, ["#4A3A30", "#2E241E"]))
    person(c, 300, 1100, 380, "#F97316", t, pose="stand", face=1)
    sh = shake * math.sin(t * 40) * 22
    x = lerp(420, 760, smooth(hand_over))
    y = 860 + sh * (1 - hand_over)
    c.save()
    c.translate(x, y)
    c.scale(0.33, 0.33)
    c.translate(-CX, -(TOP + BOT) / 2)
    can(c, t=t, shake=sh * 0.6)
    c.restore()
    if shake > 0 and hand_over < 0.5:
        for j in range(4):
            c.drawLine(x - 80, y - 60 + j * 40, x - 140, y - 60 + j * 40, P("#F8FAFC", 0.6 * shake, stroke=4))
    if hand_over > 0:                                    # your hand reaching in from the right
        hand(c, lerp(W + 140, 860, smooth(hand_over)), 880, 0.8, grip=0.4, flip=-1)
    if burst > 0:                                        # psssht
        v2set.splash(c, x, y - 100, t, t_burst, dur=1.2, n=40, speed=900, col="#E0F2FE")
        add_glow(c, x, y - 120, 220, "#E0F2FE", 0.35 * clamp(1 - (t - t_burst) / 1.2))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


class SodaCan(EpisodeV2):
    BUILD_NO = 114
    FIRST_SET = "table"
    CLEAR = "#0B0E1E"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "ALUMINUM SODA CAN", "ar_sa": "علبة الغازي"}
    EMPH = {"en": ["SODA", "CAN'S", "WALL", "THIN", "PAPER", "FIZZ", "PUSHES", "HARD", "CAR", "TIRE", "STRONGER", "FULL",
                   "EMPTY", "BOTTOM", "DOME", "PUSH", "SHAPE", "METAL", "TALL", "CUP", "FLAT", "DISK", "PUNCHED",
                   "SQUEEZED", "TALLER", "RINGS", "BARE", "ALUMINUM", "TASTE", "PLASTIC", "COAT", "RAINCOAT", "TABS",
                   "LITTERED", "BEACH", "STAYS", "LEVER", "LID", "FOLLOW", "CRANE", "ANSWER", "TIGHT", "DENTS", "TENTH",
                   "MILLIMETER", "NINETY", "PSI", "HUNDRED", "BILLION", "CONGRATS", "YOURSELF", "SHAKES", "HANDING"],
            "ar_sa": ["جدار", "علبة", "الغازي", "رقيق", "الورقة", "الغاز", "يدف", "كفر", "السيارة", "مليانة", "أقوى",
                      "فاضية", "مقوس", "القبة", "يتحمل", "ألمنيوم", "كوب", "طويل", "قرص", "مسطح", "ينكبس", "يتمطط",
                      "حلقات", "طعم", "الحديد", "بلاستيك", "رقيقة", "الفتاحة", "الشواطئ", "تظل", "رافعة", "الغطا",
                      "متابعة", "تطول", "الجواب", "يشد", "الجدار", "تنبعج", "عشر", "ملي", "ست", "مليار", "مبروك",
                      "الشاحنات", "يرجها"]}
    KEYS = {"ar_sa": {
        ("hook", "WALL"): "جدار", ("hook", "THIN"): "رقيق", ("hook", "PAPER"): "الورقة",
        ("break1", "FIZZ"): "الغاز", ("break1", "TIRE"): "كفر", ("break1", "STRONGER"): "أقوى",
        ("fix1", "BOTTOM"): "فقاعها", ("fix1", "DOME"): "القبة", ("fix1", "PUSH"): "الدفة",
        ("break2", "SHAPE"): "تسوي", ("break2", "TALL"): "طويل",
        ("fix2", "DISK"): "قرص", ("fix2", "PUNCHED"): "ينكبس", ("fix2", "TALLER"): "يتمطط", ("fix2", "RINGS"): "حلقات",
        ("break3", "BARE"): "الألمنيوم", ("break3", "METAL"): "الحديد",
        ("fix3", "INSIDE"): "داخلها", ("fix3", "COAT"): "بلاستيك", ("fix3", "RAINCOAT"): "الطعم",
        ("break4", "TABS"): "الفتاحة", ("break4", "BEACH"): "الشواطئ",
        ("fix4", "STAYS"): "تظل", ("fix4", "LEVER"): "رافعة", ("fix4", "LID"): "الغطا",
        ("cta", "FOLLOW"): "متابعة", ("cta", "TALLER"): "بنفسها",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "FULL"): "مليانة", ("reveal", "TIGHT"): "يشد",
        ("reveal", "DENTS"): "تنبعج",
        ("stat", "TENTH"): "عشر", ("stat", "NINETY"): "ست", ("stat", "BILLION"): "مليار",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SURVIVES"): "تتحمل", ("tag", "SHAKES"): "يرجها", ("tag", "OVER"): "إياها"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a self-climbing crane"),
                   "stat": [("0.1", "MM WALL"), ("90", "PSI, TOPS"), ("100B+", "CANS A YEAR")],
                   "L": {"paper": "AS THIN AS PAPER", "tire": "PUSHES LIKE A CAR TIRE", "which": "FULL OR EMPTY?",
                         "dome": "A DOME HOLDS THE PUSH", "how": "HOW, THAT THIN?", "rings": "PUNCHED, THEN STRETCHED",
                         "metal": "TASTES LIKE METAL!", "coat": "A THIN PLASTIC COAT", "litter": "TABS ALL OVER THE BEACH",
                         "lever": "THE TAB STAYS ON", "full": "FULL IS STRONGER!", "name": "THE ALUMINUM SODA CAN",
                         "shake": "SHAKE, SHAKE..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: رافعة تطوّل نفسها"),
                      "stat": [("0.1", "ملي سماكة"), ("6×", "ضغط الهوا"), ("100B+", "علبة بالسنة")],
                      "L": {"paper": "رقيق مثل الورقة", "tire": "يدف مثل كفر السيارة", "which": "مليانة ولا فاضية؟",
                            "dome": "القبة تتحمّل الدفّة", "how": "كيف بهالرقّة؟", "rings": "ينكبس وبعدين يتمطّط",
                            "metal": "طعمه حديد!", "coat": "طبقة بلاستيك رقيقة", "litter": "الفتّاحات في الشواطئ",
                            "lever": "الفتّاحة تظل مكانها", "full": "المليانة أقوى!", "name": "علبة الغازي",
                            "shake": "يرجّها..."}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "wall": ("hook", "WALL", 0.3), "thin": ("hook", "THIN", 0.75), "paper": ("hook", "PAPER", 0.95),
            "fizz": ("break1", "FIZZ", 0.15), "tire": ("break1", "TIRE", 0.5), "stronger": ("break1", "STRONGER", 0.75),
            "bottom": ("fix1", "BOTTOM", 0.2), "dome": ("fix1", "DOME", 0.6), "push": ("fix1", "PUSH", 0.9),
            "shape": ("break2", "SHAPE", 0.3), "tall": ("break2", "TALL", 0.85),
            "disk": ("fix2", "DISK", 0.15), "punched": ("fix2", "PUNCHED", 0.35), "taller": ("fix2", "TALLER", 0.7),
            "rings": ("fix2", "RINGS", 0.95),
            "bare": ("break3", "BARE", 0.2), "metal": ("break3", "METAL", 0.85),
            "inside": ("fix3", "INSIDE", 0.2), "coat": ("fix3", "COAT", 0.6), "raincoat": ("fix3", "RAINCOAT", 0.9),
            "tabs": ("break4", "TABS", 0.2), "beach": ("break4", "BEACH", 0.9),
            "stays": ("fix4", "STAYS", 0.25), "lever": ("fix4", "LEVER", 0.6), "lid": ("fix4", "LID", 0.9),
            "follow": ("cta", "FOLLOW", 0.1), "crane": ("cta", "TALLER", 0.95),
            "answer": ("reveal", "ANSWER", 0.05), "full": ("reveal", "FULL", 0.2), "tight": ("reveal", "TIGHT", 0.6),
            "dents": ("reveal", "DENTS", 0.92),
            "s1": ("stat", "TENTH", 0.05), "s2": ("stat", "NINETY", 0.4), "s3": ("stat", "BILLION", 0.8),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_surv": ("tag", "SURVIVES", 0.05), "t_shake": ("tag", "SHAKES", 0.6), "t_over": ("tag", "OVER", 0.92)})
        T["tire1"] = max(T["tire"], s("break1") + 0.3)
        T["dome1"] = max(T["dome"], T["bottom"] + 0.5)
        T["tall1"] = max(T["tall"], s("break2") + 0.3)
        T["rings1"] = max(T["rings"], T["punched"] + 0.6)
        T["metal1"] = max(T["metal"], s("break3") + 0.4)
        T["coat1"] = max(T["coat"], T["inside"] + 0.4)
        T["beach1"] = max(T["beach"], s("break4") + 0.4)
        T["lid1"] = max(T["lid"], T["stays"] + 0.6)
        T["dents1"] = max(T["dents"], T["tight"] + 0.3)
        T["burst"] = max(T["t_over"], T["t_shake"] + 0.8)
        # ---- sets
        self.cut(s("break1") - 0.12, "pressure", 1)
        self.cut(s("break2") - 0.12, "factory", -1)
        self.cut(s("break3") - 0.12, "taste", 1)
        self.cut(s("fix3") - 0.12, "coat", -1)
        self.cut(s("break4") - 0.12, "beach", 1)
        self.cut(s("fix4") - 0.12, "lid", -1)
        self.cut(s("cta") - 0.12, "table", 1)
        self.cut(s("reveal") - 0.12, "squeeze", -1)
        self.cut(s("stat") - 0.12, "table", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["tire1"], T["dome1"]), (T["tall1"], T["rings1"]), (T["metal1"], T["coat1"]), (T["beach1"], T["lid1"])]
        self.shakes = [(T["paper"], 0.3, 4), (T["tire1"], 0.35, 6), (T["dome1"], 0.3, 5), (T["punched"], 0.3, 7),
                       (T["rings1"], 0.3, 5), (T["metal1"], 0.35, 6), (T["beach1"] + 0.2, 0.4, 8), (T["lid1"], 0.3, 5),
                       (T["dents1"], 0.3, 5), (s("closer") + 0.2, 0.35, 6), (T["burst"], 0.4, 8)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: table (hook, cta, stat, closer)
    def draw_table(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["paper"] - 0.2, s("break1") - 0.2))
            z = lerp(1.0, 0.92, k)
            table(c)
            c.save()
            c.translate(CX, BOT)
            c.scale(z, z)
            c.translate(-CX, -BOT)
            can(c, t=t, drops=0.8, cold=0.6)
            c.restore()
            lens(c, 760, 640, 190, t, k=1.0, wall=1.0, paper=prog(t, T["thin"] - 0.3, T["paper"]))
        elif ph == "stat":
            table(c)
            c.save()
            c.translate(CX, BOT)
            c.scale(0.68, 0.68)
            c.translate(-CX, -BOT)
            can(c, t=t, drops=0.8, cold=0.4)
            c.restore()
        elif ph == "closer":
            table(c, night=0.6)
            add_glow(c, CX, 700, 520, "#5EEAD4", 0.16)
            can(c, t=t, drops=1.0, cold=1.0)
        else:                                            # cta
            table(c, night=0.3)
            can(c, t=t, drops=0.8, cold=0.5)

    def ui_table(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "paper", T["thin"] - 0.3, s("break1") + 0.1, accent=HILITE, size=58)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=52)

    # ------------------------------------------------------------------ set: pressure (break1, fix1)
    def draw_pressure(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break1":
            xray_can(c, t, push=prog(t, T["fizz"] - 0.2, T["tire1"]))
            tire_gauge(c, 935, 490, 52, prog(t, T["tire"] - 0.4, T["tire1"] + 0.3), a=prog(t, T["tire"] - 0.5, T["tire"] - 0.2))
        else:
            dome = prog(t, T["dome"] - 0.3, T["dome1"])
            xray_can(c, t, push=1.0, bottom=prog(t, T["bottom"] - 0.3, T["bottom"]), dome=dome,
                     rock=prog(t, T["bottom"], T["bottom"] + 0.3) * (1 - dome))

    def ui_pressure(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "tire", T["fizz"] - 0.2, T["stronger"] - 0.3, accent=WARN, size=50)
            self.chip(540, 300, "which", T["stronger"] - 0.3, s("fix1") - 0.1, accent=HILITE, size=58)
            self.badge("alert", T["tire1"], s("fix1") - 0.2, x=160, y=470)
            self.red(T["tire1"], 1.2)
        else:
            self.chip(540, 300, "dome", T["bottom"] - 0.2, s("break2") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["dome1"], s("break2") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: factory (break2, fix2)
    def draw_factory(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break2":
            factory(c, t, stage=0.0, ram=0.0, q_mark=prog(t, T["shape"] - 0.2, T["tall1"]))
        else:
            ram = prog(t, T["punched"] - 0.3, T["punched"]) * (1 - prog(t, T["punched"] + 0.1, T["punched"] + 0.5))
            stage = 1.0 * (t >= T["punched"]) + clamp((t - T["punched"] - 0.2) / max(0.4, T["rings1"] - T["punched"]))
            factory(c, t, stage=stage, ram=ram)

    def ui_factory(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break2":
            self.chip(540, 300, "how", T["shape"] - 0.2, s("fix2") - 0.15, accent=WARN, size=62)
            self.badge("alert", T["tall1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["tall1"], 1.2)
        else:
            self.chip(540, 300, "rings", T["disk"] - 0.2, s("break3") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["rings1"], s("break3") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ sets: taste (break3), coat (fix3)
    def draw_taste(self, c, t):
        T, s = self.T, self.tl.s
        drinker(c, t, sip=prog(t, s("break3"), T["bare"] + 0.4), yuck=prog(t, T["metal"] - 0.4, T["metal1"]))

    def ui_taste(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "metal", T["bare"] - 0.1, s("fix3") - 0.15, accent=WARN, size=60)
        self.badge("alert", T["metal1"], s("fix3") - 0.2, x=160, y=470)
        self.red(T["metal1"], 1.2)

    def draw_coat(self, c, t):
        T, s = self.T, self.tl.s
        coat_can(c, t, spray=prog(t, s("fix3"), T["coat1"]) * (1 - prog(t, T["raincoat"], T["raincoat"] + 0.5)),
                 coat=prog(t, T["inside"], T["coat1"] + 0.3))

    def ui_coat(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "coat", T["inside"] - 0.2, s("break4") - 0.15, accent=GOOD, size=54)
        self.badge("check", T["coat1"], s("break4") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ sets: beach (break4), lid (fix4)
    def draw_beach(self, c, t):
        T, s = self.T, self.tl.s
        beach(c, t, tabs=prog(t, s("break4"), T["tabs"] + 0.3), step=prog(t, T["beach"] - 0.6, T["beach1"]))

    def ui_beach(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "litter", T["tabs"] - 0.2, s("fix4") - 0.15, accent=WARN, size=52)
        self.badge("alert", T["beach1"], s("fix4") - 0.2, x=160, y=470)
        self.red(T["beach1"], 1.2)

    def draw_lid(self, c, t):
        T, s = self.T, self.tl.s
        lid_top(c, t, lift=prog(t, T["lever"] - 0.4, T["lid1"]))

    def ui_lid(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "lever", T["stays"] - 0.2, s("cta") - 0.15, accent=GOOD, size=56)
        self.badge("check", T["lid1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: squeeze (reveal)
    def draw_squeeze(self, c, t):
        T, s = self.T, self.tl.s
        squeeze(c, t, empty_k=prog(t, T["answer"], T["full"] + 0.5), full_k=prog(t, T["tight"] - 0.3, T["dents1"]),
                arrows=prog(t, T["tight"] - 0.3, T["tight"] + 0.2))

    def ui_squeeze(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "full", T["full"] - 0.2, s("stat") - 0.15, accent=HILITE, size=62)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        tag_scene(c, t, shake=prog(t, T["t_shake"] - 0.5, T["t_shake"]), hand_over=prog(t, T["burst"] - 0.6, T["burst"]),
                  burst=1.0 if t >= T["burst"] else 0.0, t_burst=T["burst"])

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "shake", T["t_shake"] - 0.3, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, gas_hiss(1.2, 62), -22), (T["thin"], sfx.tick(), -6),
              (T["paper"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["fizz"], gas_hiss(0.8, 64), -12),
               (T["tire1"], sfx.thunk(65), -8), (T["tire1"] + 0.2, sfx.alarm(3, 820.0), -14)]
        ev += [(T["bottom"], sfx.clank(500.0, 0.4, 66), -12), (T["dome1"], sfx.thunk(67), -6), (T["dome1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.45, False, 68), -6), (T["tall1"], sfx.alarm(3, 820.0), -14)]
        ev += [(T["punched"], sfx.thud(0.5, 69), -4), (T["punched"] + 0.5, sfx.whirr(1.2, 160.0, 320.0, 70), -14),
               (T["rings1"], sfx.ding(), -8), (T["rings1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 71), -6), (T["bare"], gas_hiss(0.5, 72), -14),
               (T["metal1"], sfx.clank(800.0, 0.5, 73), -10), (T["metal1"] + 0.2, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, False, 74), -6), (T["inside"], sfx.hiss(1.0, 75), -12),
               (T["coat1"], sfx.ding(), -8), (T["coat1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, True, 76), -6), (T["tabs"], sfx.sparkle(0.6, 8, 77), -12),
               (T["beach1"], sfx.thud(0.4, 78), -6), (T["beach1"] + 0.2, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.45, False, 79), -6), (T["lever"], sfx.click(80), -4),
               (T["lid1"], gas_hiss(0.5, 81), -8), (T["lid1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["full"], sfx.creak(0.6, 95), -8),
               (T["dents1"], sfx.thunk(96), -8), (T["dents1"] + 0.1, sfx.ding(), -8)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (s("closer") + 0.4, gas_hiss(0.6, 103), -10),
               (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 104), -6), (T["t_shake"], sfx.whirr(0.8, 200.0, 400.0, 105), -12),
               (T["burst"], gas_hiss(1.0, 106), -2), (T["burst"] + 0.3, sfx.womp(), -8)]
        return ev


NAME = "sodacan"
EPISODE = SodaCan
