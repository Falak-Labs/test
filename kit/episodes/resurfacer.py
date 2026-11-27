"""Episode 108 - An ice resurfacer (Frank Zamboni's machine of 1949).  v2 look.

Sets: rink (hook: close on the back of the machine as a towel lays down steaming hot water, out to the whole rink seen
from above with a glossy wet strip following the machine round its oval; cta, stat; closer with the rink lit and gleaming),
grooves (break1: skates carve the ice full of scratches), cutaway (fix1: a side cut of the machine on the ice, its long
blade shaving a curl thinner than a coin; break2: the shavings pile into a drift; fix2: a spinning screw carries the snow
sideways and a second one lifts it into the tank; break3: a magnifier shows dirt in the grooves; fix3: jets wash them and a
vacuum slurps the grey water up; break4: dents still dimple the ice; fix4: a towel spreads hot water that fills them and
freezes like glass), lens (reveal: a slice of ice, hot water melts the old top a little and the two layers fuse into one),
tag (English: a packed arena cheers the machine, then nobody claps for you mopping the kitchen; Arabic: mum telling you
not to drink cold water when you are hot).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

ICE = ("#9DB7D3", "#7F9DC0", "#6382A8")
GLOSS = "#4F86C2"
SKIN = ("#E8B48A", "#C68E62", "#A8754E", "#F1C7A3")
RCX, RCY, RRX, RRY = 540, 745, 250, 400               # the machine's oval on the rink


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== the rink from above
def rink(c, t, lit=0.0):
    vrect(c, 0, 0, W, H, ["#0B1020", "#141B33"])
    for k in range(70):                                # the crowd in the dark around the rink
        rng = random.Random(k)
        x = rng.uniform(0, W)
        y = rng.uniform(150, 1250)
        if 150 < x < 930 and 230 < y < 1260:
            continue
        c.drawCircle(x, y, rng.uniform(8, 13), P(rng.choice(["#EF4444", "#3B82F6", "#F8FAFC", "#F59E0B", "#22C55E"]), 0.55))
    c.drawRRect(rr(150, 230, 780, 1030, 230), P("#334155"))                 # the boards
    ice = rr(170, 250, 740, 990, 214)
    c.drawRRect(ice, lin_paint(0, 250, 0, 1240, [mix(ICE[0], "#C9DCF0", lit * 0.4), ICE[1], mix(ICE[2], ICE[1], lit * 0.3)]))
    c.save()
    c.clipRRect(ice, skia.ClipOp.kIntersect, True)
    c.drawLine(170, 745, 910, 745, P("#DC2626", 0.75, stroke=14))            # the lines
    for y in (560, 930):
        c.drawLine(170, y, 910, y, P("#2563EB", 0.7, stroke=14))
    c.drawCircle(540, 745, 90, P("#2563EB", 0.6, stroke=6))
    for (x, y) in ((340, 400), (740, 400), (340, 1090), (740, 1090)):
        c.drawCircle(x, y, 70, P("#DC2626", 0.5, stroke=5))
    for y in (300, 1190):
        c.drawLine(170, y, 910, y, P("#DC2626", 0.5, stroke=4))
    c.restore()
    if lit > 0:
        for k in range(5):
            add_glow(c, 260 + k * 140, 500 + (k % 2) * 400, 160, "#FFFFFF", 0.08 * lit)


def wet_strip(c, th0, th1, t, a=1.0):
    """The glossy strip of fresh water left behind on the oval from angle th0 to th1."""
    if th1 <= th0 or a <= 0:
        return
    p = skia.Path()
    n = max(2, int((th1 - th0) * 30))
    for k in range(n + 1):
        th = lerp(th0, th1, k / n)
        x, y = RCX + RRX * math.cos(th), RCY + RRY * math.sin(th)
        if k == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    c.drawPath(p, P(GLOSS, 0.85 * a, stroke=170))
    c.drawPath(p, P("#BFE0FF", 0.3 * a, stroke=36))


def machine_top(c, x, y, ang, s, t, steam=1.0, a=1.0):
    """The resurfacer from above, driving along `ang` (radians): body, seat, snow tank, and the towel trailing behind."""
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(ang) + 90)
    c.scale(s, s)
    c.drawRRect(rr(-95, 70, 190, 46, 10), P("#475569", a))                 # the conditioner across the back
    c.drawRect(R(-90, 116, 180, 40), lin_paint(0, 116, 0, 156, ["#93C5FD", "#3B82F6"], a=0.85 * a))   # the towel
    c.drawRRect(rr(-80, -150, 160, 230, 30), lin_paint(-80, 0, 80, 0, ["#B8C1CE", "#D5DCE5", "#9CA7B6"], a=a))
    c.drawRRect(rr(-66, -136, 132, 110, 20), P("#2563EB", a))               # the snow tank lid
    c.drawRRect(rr(-30, -10, 60, 54, 14), P("#111827", a))                  # the driver's seat
    c.drawCircle(0, 6, 18, P("#F59E0B", a))
    for sx in (-86, 86):
        for sy in (-110, 40):
            c.drawRRect(rr(sx - 10, sy - 22, 20, 44, 6), P("#1F2937", a))
    c.restore()
    if steam > 0:                                      # steam from the hot water behind it
        bx, by = x - math.cos(ang) * 150 * s, y - math.sin(ang) * 150 * s
        for k in range(6):
            u = (t * 0.9 + k / 6) % 1.0
            v2.puff(c, bx + math.sin(k * 2.1) * 50 * s - math.cos(ang) * 60 * u * s, by - 60 * u * s - math.sin(ang) * 60 * u * s,
                    (20 + 30 * u) * s, "#F8FAFC", 0.4 * (1 - u) * steam * a)


def rink_scene(c, t, th, th0=-0.4, lit=0.0, steam=1.0):
    rink(c, t, lit)
    wet_strip(c, th0, th, t)
    x, y = RCX + RRX * math.cos(th), RCY + RRY * math.sin(th)
    ang = math.atan2(RRY * math.cos(th), -RRX * math.sin(th))
    machine_top(c, x, y, ang, 0.8, t, steam=steam)


# ====================================================================================== grooves
def grooves(c, t, carve=1.0, a=1.0):
    vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
    c.drawRRect(rr(60, 380, 960, 860, 40), lin_paint(0, 380, 0, 1240, [ICE[0], ICE[1]]))
    c.save()
    c.clipRRect(rr(60, 380, 960, 860, 40), skia.ClipOp.kIntersect, True)
    rng = random.Random(3)
    n = int(60 * clamp(carve))
    for k in range(n):                                 # scratches piling up
        x0, y0 = rng.uniform(0, W), rng.uniform(380, 1240)
        r = rng.uniform(200, 600)
        st = rng.uniform(0, 360)
        sw = rng.uniform(20, 60)
        c.drawArc(R(x0 - r, y0 - r, 2 * r, 2 * r), st, sw, False, P("#3F5A80", 0.8, stroke=rng.uniform(3, 7)))
    c.restore()
    # a skate carving an arc, spraying ice
    ph = t * 1.4
    sx, sy = 540 + math.cos(ph) * 260, 800 + math.sin(ph) * 220
    ang = math.degrees(ph) + 90
    c.save()
    c.translate(sx, sy)
    c.rotate(ang)
    c.drawRRect(rr(-26, -90, 52, 180, 24), P("#111827"))
    c.drawRRect(rr(-8, -110, 16, 220, 6), P("#CBD5E1"))
    c.restore()
    for k in range(10):
        u = (t * 3 + k / 10) % 1.0
        v2.puff(c, sx - math.cos(ph) * 60 * u + math.sin(k) * 20, sy - math.sin(ph) * 60 * u, 10 + 16 * u, "#F8FAFC", 0.6 * (1 - u))


# ====================================================================================== the cutaway
ICE_Y = 1000                                            # top of the ice in the cutaway
BX = 300                                                # the blade's x


def auger(c, x, y, w, h, t, spin=1.0, vertical=False, a=1.0):
    """A screw conveyor: a tube with a turning spiral."""
    c.drawRRect(rr(x, y, w, h, 14), P("#334155", a))
    c.save()
    c.clipRRect(rr(x, y, w, h, 14), skia.ClipOp.kIntersect, True)
    n = 8
    for k in range(n + 2):
        if vertical:
            yy = y + ((k / n) * h + t * 220 * spin) % (h + h / n) - h / n
            c.drawLine(x + 6, yy, x + w - 6, yy + h / n * 0.6, P("#CBD5E1", a, stroke=8))
        else:
            xx = x + ((k / n) * w - t * 220 * spin) % (w + w / n) - w / n
            c.drawLine(xx, y + 6, xx + w / n * 0.6, y + h - 6, P("#CBD5E1", a, stroke=8))
    c.restore()


def ice_profile(c, t, flat_x, gloss_x=None, dirt=0.0, dents=0.0, x0=0, x1=W):
    """The ice slab in section: grooved ahead of the machine (right of flat_x), shaved flat behind it."""
    p = skia.Path()
    p.moveTo(x0, 1150)
    rng = random.Random(9)
    xs = list(range(int(x0), int(x1) + 1, 12))
    for x in xs:
        if x > flat_x:
            y = ICE_Y + (rng.choice([0, 0, 10, 16, 6]) if (x // 12) % 2 else 0)
        else:
            y = ICE_Y + 8 + (6 * dents * (1 + math.sin(x * 0.11)) if gloss_x is None or x > gloss_x else 0)
        p.lineTo(x, y)
    p.lineTo(x1, 1150)
    p.close()
    c.drawPath(p, lin_paint(0, ICE_Y, 0, 1150, [ICE[0], ICE[2]]))
    c.drawRect(R(x0, 1150, x1 - x0, 100), P("#5B6475"))                    # concrete with cold pipes
    for k in range(9):
        c.drawCircle(x0 + 60 + k * 120, 1185, 14, P("#38BDF8", 0.7))
    if gloss_x is not None:                            # the new glassy layer behind the towel
        c.drawRect(R(x0, ICE_Y - 6, gloss_x - x0, 20), lin_paint(0, ICE_Y - 6, 0, ICE_Y + 14, ["#E0F2FE", GLOSS]))
        c.drawLine(x0, ICE_Y - 4, gloss_x, ICE_Y - 4, P("#FFFFFF", 0.7, stroke=3))
    if dirt > 0:                                       # grit in the grooves ahead
        rng = random.Random(4)
        for k in range(30):
            x = rng.uniform(flat_x + 10, x1)
            c.drawCircle(x, ICE_Y + rng.uniform(4, 14), 4, P("#3F3F46", dirt))


def machine_side(c, t, x, a=1.0):
    """The resurfacer in a side cut, driving right; x = its rear (the towel). Returns key x positions."""
    # body
    c.drawRRect(rr(x + 160, 600, 620, 300, 30), lin_paint(0, 600, 0, 900, ["#C3CAD4", "#8E99A8"], a=a))
    c.drawRRect(rr(x + 300, 430, 460, 190, 24), lin_paint(0, 430, 0, 620, ["#3B82F6", "#1D4ED8"], a=a))   # snow tank
    c.drawRRect(rr(x + 320, 450, 420, 150, 18), P("#0B1220", 0.9 * a))
    c.drawRRect(rr(x + 560, 520, 120, 80, 14), P("#111827", a))             # seat
    for wx in (x + 300, x + 700):
        c.drawCircle(wx, 935, 58, P("#111827", a))
        c.drawCircle(wx, 935, 26, P("#9CA3AF", a))
    # the conditioner at the back
    c.drawRRect(rr(x + 20, 800, 260, 170, 20), lin_paint(0, 800, 0, 970, ["#64748B", "#334155"], a=a))
    return {"towel": x + 20, "blade": x + 150, "jets": x + 250, "vac": x + 70, "vaug": x + 230}


def cutaway(c, t, mx, step=0, k=1.0, snow=0.0, tank=0.0, dirt=0.0, wash=0.0, dents=0.0, towel=0.0, shave=0.0,
            spin=0.0, coin=0.0):
    vrect(c, 0, 0, W, H, ["#0B1020", "#16213C"])
    pos = machine_side(c, t, mx)
    flat_x = pos["blade"] + 10
    gloss_x = pos["towel"] if towel > 0 else None
    ice_profile(c, t, flat_x, gloss_x=pos["towel"] if towel > 0 else None, dirt=dirt, dents=dents)
    bx = pos["blade"]
    # the blade
    c.drawLine(bx - 60, ICE_Y + 4, bx + 40, ICE_Y + 4, P("#E5E7EB", 1, stroke=10))
    c.drawLine(bx + 40, ICE_Y + 4, bx + 50, ICE_Y - 6, P("#E5E7EB", 1, stroke=6))
    if shave > 0:                                      # a curl of ice peeling up
        p = skia.Path()
        p.moveTo(bx + 40, ICE_Y)
        p.cubicTo(bx + 60, ICE_Y - 40, bx + 10, ICE_Y - 70, bx - 10, ICE_Y - 40)
        c.drawPath(p, P("#F8FAFC", shave, stroke=6))
    if coin > 0:                                       # a coin, side on, thicker than the shaving
        c.drawRRect(rr(bx + 120, ICE_Y - 120, 150, 24, 8), lin_paint(0, ICE_Y - 120, 0, ICE_Y - 96, ["#FDE68A", "#B45309"], a=coin))
        c.drawLine(bx + 120, ICE_Y - 140, bx + 270, ICE_Y - 140, P("#F8FAFC", coin, stroke=3))
    if snow > 0:                                       # the drift of shavings in front of the blade
        v2.puff(c, bx - 20, ICE_Y - 30, 40 + 50 * snow, "#F8FAFC", 0.9 * snow)
        v2.puff(c, bx + 30, ICE_Y - 50, 30 + 40 * snow, "#F8FAFC", 0.8 * snow)
    # the screws: across under the conditioner, then up into the tank
    auger(c, bx - 90, ICE_Y - 90, 180, 46, t, spin=spin, a=0.95)
    auger(c, pos["vaug"], 620, 46, ICE_Y - 100 - 620, t, spin=spin, vertical=True, a=0.95)
    if spin > 0:
        for j in range(5):
            u = (t * 1.3 + j / 5) % 1.0
            c.drawCircle(pos["vaug"] + 23, lerp(ICE_Y - 110, 640, u), 10, P("#F8FAFC", 0.9 * spin))
    if tank > 0:                                       # snow filling the tank
        top = lerp(600, 470, clamp(tank))
        c.drawRRect(rr(mx + 320, top, 420, 600 - top, 14), P("#E2E8F0", 0.9))
    if wash > 0:                                       # jets wash the grooves; a vacuum slurps the grey water back up
        jx = pos["jets"] + 170
        for j in range(5):
            xx = jx + j * 26
            u = (t * 4 + j * 0.2) % 1.0
            c.drawLine(xx, 880, xx + 6, lerp(880, ICE_Y, u), P("#7DD3FC", 0.9 * wash, stroke=7))
        c.drawRRect(rr(jx - 10, 840, 150, 40, 10), P("#475569"))
        vx = pos["vac"]
        c.drawRect(R(vx - 10, 830, 30, ICE_Y - 830), P("#334155"))
        for j in range(4):
            u = (t * 1.6 + j / 4) % 1.0
            c.drawCircle(vx + 5, lerp(ICE_Y - 10, 840, u), 8, P("#94A3B8", 0.9 * wash))
    if towel > 0:                                      # hot water through the towel at the back, steaming
        tx = pos["towel"]
        c.drawRect(R(tx - 120, ICE_Y - 16, 130, 14), lin_paint(tx - 120, 0, tx, 0, ["#60A5FA", "#93C5FD"], a=towel))
        for j in range(5):
            u = (t * 0.8 + j / 5) % 1.0
            v2.puff(c, tx - 100 + j * 30, ICE_Y - 30 - 120 * u, 16 + 24 * u, "#F8FAFC", 0.45 * (1 - u) * towel)


def magnifier(c, x, y, r, t, dirt=0.0, wash=0.0, dents=0.0, fill=0.0, a=1.0):
    """A round close-up of the ice surface in section."""
    if a <= 0:
        return
    c.save()
    c.drawCircle(x, y, r + 14, P("#0F172A", 0.95 * a))
    cp = skia.Path()
    cp.addCircle(x, y, r)
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    vrect(c, x - r, y - r, 2 * r, 2 * r, ["#1E293B", "#334155"])
    top = y - 10
    p = skia.Path()
    p.moveTo(x - r, y + r)
    for k in range(25):
        xx = x - r + k * (2 * r / 24)
        dd = (40 if k % 4 == 1 else 0) * (1 - wash * 0) if dents == 0 else 22 * (1 + math.sin(k * 0.9)) * dents
        p.lineTo(xx, top + dd)
    p.lineTo(x + r, y + r)
    p.close()
    c.drawPath(p, lin_paint(0, top, 0, y + r, [ICE[0], ICE[2]]))
    if dirt > 0:
        for k in range(6):
            xx = x - r + (4 * k + 1) * (2 * r / 24)
            c.drawCircle(xx, top + 26, 10, P("#3F3F46", dirt * (1 - wash)))
    if fill > 0:                                       # hot water filling the dents and freezing flat
        c.drawRect(R(x - r, top - 8, 2 * r, 60 * fill), P(GLOSS, 0.9 * fill))
        c.drawLine(x - r, top - 8, x + r, top - 8, P("#FFFFFF", 0.8 * fill, stroke=4))
    c.restore()
    c.drawCircle(x, y, r, P("#E2E8F0", a, stroke=10))


# ====================================================================================== the lens (reveal)
def lens(c, t, melt=0.0, fuse=0.0):
    vrect(c, 0, 0, W, H, ["#0B1020", "#16213C"])
    x0, x1 = 140, 940
    top_old = 760
    c.drawRect(R(x0, top_old, x1 - x0, 400), lin_paint(0, top_old, 0, 1160, [ICE[0], ICE[2]]))   # the old ice
    p = skia.Path()                                     # its top, melting into soft waves
    p.moveTo(x0, top_old)
    for k in range(41):
        xx = lerp(x0, x1, k / 40)
        p.lineTo(xx, top_old + math.sin(k * 1.7 + t * 4) * 10 * melt)
    p.lineTo(x1, top_old - 30)
    p.lineTo(x0, top_old - 30)
    p.close()
    hot = mix("#F97316", GLOSS, fuse)
    c.drawRect(R(x0, top_old - 130, x1 - x0, 130), lin_paint(0, top_old - 130, 0, top_old, [mix("#FDBA74", "#E0F2FE", fuse), hot],
                                                            a=0.9))
    if melt > 0:
        c.drawRect(R(x0, top_old - 6, x1 - x0, 24), P("#FDE68A", 0.6 * melt * (1 - fuse)))
        for k in range(6):
            u = (t * 0.7 + k / 6) % 1.0
            v2.puff(c, x0 + 60 + k * 140, top_old - 140 - 100 * u, 18 + 20 * u, "#F8FAFC", 0.35 * (1 - u) * (1 - fuse))
    if fuse > 0:                                       # one block now: the seam glows and fades
        add_glow(c, 540, top_old, 400, "#FFFFFF", 0.25 * fuse)
        c.drawLine(x0, top_old - 130, x1, top_old - 130, P("#FFFFFF", 0.8 * fuse, stroke=6))
    c.drawRect(R(x0, top_old - 130, x1 - x0, 530), P("#E2E8F0", 0.8, stroke=6))


# ====================================================================================== tags
def arena_tag(c, t, cheer=1.0, kitchen=0.0):
    if kitchen < 1:
        vrect(c, 0, 0, W, H, ["#0B1020", "#1E293B"])
        rng = random.Random(2)
        for row in range(9):                           # the stands full of fans
            y = 360 + row * 56
            for k in range(16):
                x = 20 + k * 68 + (row % 2) * 30
                hop = abs(math.sin(t * 8 + k + row)) * 14 * cheer
                c.drawCircle(x, y - hop, 20, P(rng.choice(SKIN)))
                c.drawRRect(rr(x - 24, y + 14 - hop, 48, 40, 14), P(rng.choice(["#EF4444", "#3B82F6", "#F8FAFC", "#F59E0B"])))
        c.drawRect(R(0, 900, W, 350), lin_paint(0, 900, 0, 1250, [ICE[0], ICE[1]]))
        machine_top(c, 540 + math.sin(t) * 60, 1060, 0.0, 0.9, t)
    if kitchen > 0:                                    # ...and you mopping the kitchen, nobody watching
        c.save()
        c.saveLayerAlpha(None, int(255 * clamp(kitchen)))
        vrect(c, 0, 0, W, H, ["#3F3A33", "#5C5247"])
        for k in range(5):
            c.drawRect(R(k * 230 + 20, 420, 190, 240), P("#7C6F5E"))
        c.drawRect(R(0, 900, W, 360), P("#A8A29E"))
        for k in range(10):
            c.drawLine(k * 120, 900, k * 120 - 200, 1260, P("#8D8780", 0.6, stroke=3))
        person(c, 600, 1180, 420, "#22C55E", t, pose="carry", face=-1, hair="#111827")
        c.drawLine(470, 860, 380, 1180, P("#92400E", 1, stroke=10))
        c.drawOval(R(320, 1160, 120, 40), P("#E5E7EB"))
        c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E293B", "#0B1020"]))
        c.restore()
        c.restore()


def mom_tag(c, t, wag=0.0):
    vrect(c, 0, 0, W, H, ["#3B2F2A", "#5C4033"])
    c.drawRRect(rr(620, 380, 360, 300, 20), P("#F59E0B"))                  # a hot window
    add_glow(c, 800, 530, 200, "#FFD27A", 0.5)
    c.drawCircle(800, 500, 60, P("#FFF7D6"))
    c.drawRect(R(0, 1000, W, 260), P("#6B4F3A"))
    person(c, 330, 1180, 460, "#3B82F6", t, pose="stand", face=1, hair="#111827", skin=SKIN[0])     # the kid, hot
    for k in range(3):
        u = (t * 1.2 + k / 3) % 1.0
        c.drawOval(R(380 + k * 14, 760 + 40 * u, 10, 16), P("#93C5FD", 1 - u))
    c.drawRRect(rr(380, 850, 46, 110, 14), lin_paint(0, 850, 0, 960, ["#E0F2FE", "#60A5FA"]))       # an ice-cold bottle
    for k in range(4):
        v2.puff(c, 403 + math.sin(k) * 10, 840 - k * 20 - (t * 20) % 20, 8, "#E0F2FE", 0.4)
    person(c, 760, 1180, 500, "#9D174D", t, pose="point", face=-1, hair="#111827", skin=SKIN[1])     # mum
    if wag > 0:
        fx = 650 + math.sin(t * 14) * 18 * wag
        c.drawLine(700, 690, fx, 600, P(SKIN[1], 1, stroke=14))


class Resurfacer(EpisodeV2):
    BUILD_NO = 108
    FIRST_SET = "rink"
    CLEAR = "#0B1020"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "ICE RESURFACER", "ar_sa": "مكينة تنعيم الثلج"}
    EMPH = {"en": ["HOCKEY", "RINK", "ICE", "HOT", "WATER", "BATH", "SKATES", "GROOVES", "WHY", "BLADE", "SHAVES", "THINNER",
                   "COIN", "PILE", "SNOW", "SPINNING", "SCREW", "TANK", "DIRT", "JETS", "WASH", "VACUUM", "SLURPS", "BUMPY",
                   "TOWEL", "FREEZES", "GLASS", "FOLLOW", "OFFICE", "BREATHES", "TERMITE", "MELTS", "OLD", "NEW", "LAYER",
                   "STICKS", "NINETEEN", "FORTY-NINE", "CALIFORNIA", "FIFTEEN", "MINUTES", "NINETY", "CONGRATS",
                   "YOURSELF", "ARENA", "CHEERS", "MOPPING", "NOBODY", "CLAPS", "KITCHEN"],
            "ar_sa": ["ثلج", "حلبات", "يتسبح", "حارة", "أحذية", "تخدشه", "ليش", "شفرة", "تقشر", "الريال", "يتكوم", "كوم",
                      "بريمة", "البرغي", "لخزان", "الوسخ", "الخدوش", "رشاشات", "شفاط", "نقر", "ناعم", "فوطة", "الحارة",
                      "وتتجمد", "الزجاج", "متابعة", "تتنفس", "النمل", "تذوب", "القديم", "الجديدة", "تلزق", "كاليفورنيا",
                      "وربع", "ساعة", "مبروك", "يصلحون", "وأمك", "بارد", "حران"]}
    KEYS = {"ar_sa": {
        ("hook", "HOCKEY"): "حلبات", ("hook", "ICE"): "ثلج", ("hook", "HOT"): "حارة", ("hook", "BATH"): "يتسبح",
        ("break1", "SKATES"): "أحذية", ("break1", "GROOVES"): "تخدشه", ("break1", "WHY"): "ليش", ("break1", "HOT"): "حارة",
        ("fix1", "BLADE"): "شفرة", ("fix1", "SHAVES"): "تقشر", ("fix1", "COIN"): "الريال",
        ("break2", "PILE"): "يتكوم", ("break2", "SNOW"): "ثلج",
        ("fix2", "SPINNING"): "تلف", ("fix2", "SCREW"): "البرغي", ("fix2", "TANK"): "لخزان",
        ("break3", "DIRT"): "الوسخ", ("break3", "GROOVES"): "الخدوش",
        ("fix3", "JETS"): "رشاشات", ("fix3", "WASH"): "تغسله", ("fix3", "VACUUM"): "شفاط", ("fix3", "DIRTY"): "الوسخة",
        ("break4", "BUMPY"): "نقر",
        ("fix4", "TOWEL"): "فوطة", ("fix4", "HOT"): "الحارة", ("fix4", "FREEZES"): "وتتجمد", ("fix4", "GLASS"): "الزجاج",
        ("cta", "FOLLOW"): "متابعة", ("cta", "TERMITE"): "النمل",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "MELTS"): "تذوب", ("reveal", "OLD"): "القديم",
        ("reveal", "NEW"): "الجديدة", ("reveal", "STICKS"): "تلزق",
        ("stat", "NINETEEN"): "ألف", ("stat", "CALIFORNIA"): "كاليفورنيا", ("stat", "FIFTEEN"): "وربع",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "CHEERS"): "يصلحون", ("tag", "NOBODY"): "وأمك", ("tag", "KITCHEN"): "حران"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: an office that breathes"),
                   "stat": [("1949", "FIRST MACHINE"), ("15 MIN", "A WHOLE RINK"), ("90 MIN", "BY HAND")],
                   "L": {"hot": "A HOT WATER BATH?!", "grooves": "SCRATCHED UP!", "why": "WHY HOT WATER?",
                         "blade": "A LONG BLADE SHAVES IT", "coin": "THINNER THAN A COIN", "pile": "A PILE OF SNOW!",
                         "screw": "A SPINNING SCREW", "tank": "UP INTO THE TANK", "dirt": "DIRT IN THE GROOVES",
                         "jets": "JETS WASH IT", "vac": "A VACUUM SLURPS IT UP", "bumpy": "STILL BUMPY!",
                         "towel": "A TOWEL SPREADS HOT WATER", "glass": "FREEZES LIKE GLASS", "melt": "IT MELTS THE OLD TOP",
                         "stick": "THE NEW LAYER STICKS", "name": "THE ICE RESURFACER", "clap": "NOBODY CLAPS",
                         "cheer": "THE CROWD GOES WILD"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: عمارة تتنفّس"),
                      "stat": [("1949", "أول مكينة"), ("15", "دقيقة للحلبة كلها"), ("90", "دقيقة باليد")],
                      "L": {"hot": "يتسبّح بموية حارة؟!", "grooves": "مخدوش كله!", "why": "ليش موية حارة؟",
                            "blade": "شفرة طويلة تقشّره", "coin": "أرق من الريال", "pile": "كوم ثلج!",
                            "screw": "بريمة تلف", "tank": "للخزان فوق", "dirt": "وسخ في الخدوش",
                            "jets": "رشاشات تغسله", "vac": "شفاط يسحب الوسخ", "bumpy": "للحين مو ناعم!",
                            "towel": "فوطة تفرد موية حارة", "glass": "يتجمد مثل الزجاج", "melt": "تذوّب الوجه القديم",
                            "stick": "الطبقة الجديدة تلزق", "name": "مكينة تنعيم الثلج", "clap": "لا تشرب بارد!",
                            "cheer": "يصلحونه بموية حارة"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "hockey": ("hook", "HOCKEY", 0.2), "ice": ("hook", "ICE", 0.5), "hot0": ("hook", "HOT", 0.75),
            "bath": ("hook", "BATH", 0.95),
            "skates": ("break1", "SKATES", 0.1), "grooves": ("break1", "GROOVES", 0.4), "why": ("break1", "WHY", 0.65),
            "hot1": ("break1", "HOT", 0.9),
            "blade": ("fix1", "BLADE", 0.25), "shaves": ("fix1", "SHAVES", 0.45), "coin": ("fix1", "COIN", 0.9),
            "pile": ("break2", "PILE", 0.5), "snow": ("break2", "SNOW", 0.85),
            "spinning": ("fix2", "SPINNING", 0.2), "screw": ("fix2", "SCREW", 0.35), "tank": ("fix2", "TANK", 0.9),
            "dirt": ("break3", "DIRT", 0.3), "grooves3": ("break3", "GROOVES", 0.85),
            "jets": ("fix3", "JETS", 0.15), "wash": ("fix3", "WASH", 0.3), "vacuum": ("fix3", "VACUUM", 0.6),
            "dirty": ("fix3", "DIRTY", 0.85),
            "bumpy": ("break4", "BUMPY", 0.8),
            "towel": ("fix4", "TOWEL", 0.2), "hot4": ("fix4", "HOT", 0.55), "freezes": ("fix4", "FREEZES", 0.8),
            "glass": ("fix4", "GLASS", 0.95),
            "follow": ("cta", "FOLLOW", 0.1), "termite": ("cta", "TERMITE", 0.8),
            "answer": ("reveal", "ANSWER", 0.05), "melts": ("reveal", "MELTS", 0.3), "old": ("reveal", "OLD", 0.5),
            "new": ("reveal", "NEW", 0.75), "sticks": ("reveal", "STICKS", 0.9),
            "s1": ("stat", "NINETEEN", 0.05), "s2": ("stat", "CALIFORNIA", 0.4), "s3": ("stat", "FIFTEEN", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_cheer": ("tag", "CHEERS", 0.2), "t_nobody": ("tag", "NOBODY", 0.6), "t_kitchen": ("tag", "KITCHEN", 0.9)})
        T["groove1"] = max(T["grooves"], T["skates"] + 0.3)
        T["coin1"] = max(T["coin"], T["shaves"] + 0.3)
        T["pile1"] = max(T["pile"], s("break2") + 0.3)
        T["tank1"] = max(T["tank"], T["screw"] + 0.3)
        T["dirt1"] = max(T["dirt"], s("break3") + 0.3)
        T["dirty1"] = max(T["dirty"], T["vacuum"] + 0.3)
        T["bumpy1"] = max(T["bumpy"], s("break4") + 0.3)
        T["glass1"] = max(T["glass"], T["freezes"] + 0.2)
        # ---- sets
        self.cut(s("break1") - 0.12, "grooves", 1)
        self.cut(s("fix1") - 0.12, "cutaway", -1)
        self.cut(s("cta") - 0.12, "rink", 1)
        self.cut(s("reveal") - 0.12, "lens", -1)
        self.cut(s("stat") - 0.12, "rink", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["groove1"], T["coin1"]), (T["pile1"], T["tank1"]), (T["dirt1"], T["dirty1"]), (T["bumpy1"], T["glass1"])]
        self.shakes = [(T["hot0"], 0.3, 4), (T["groove1"], 0.4, 6), (T["pile1"], 0.3, 6), (T["dirt1"], 0.3, 5),
                       (T["bumpy1"], 0.3, 5), (T["sticks"], 0.3, 5), (s("closer") + 0.2, 0.35, 6), (T["t_kitchen"], 0.3, 5)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: rink (hook, cta, stat, closer)
    def th_at(self, t):
        return -0.4 + (t - 0.0) * 0.16

    def draw_rink(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        th = self.th_at(t)
        if ph == "hook":
            k = e_io(prog(t, T["hot0"] - 0.3, s("break1") - 0.2))
            mx, my = RCX + RRX * math.cos(th), RCY + RRY * math.sin(th)
            ang = math.atan2(RRY * math.cos(th), -RRX * math.sin(th))
            bx, by = mx - math.cos(ang) * 120 * 0.8, my - math.sin(ang) * 120 * 0.8
            z = lerp(2.8, 1.0, k)
            fx, fy = lerp(bx, 540, k), lerp(by, 745, k)
            c.save()
            c.translate(540, 720)
            c.scale(z, z)
            c.translate(-fx, -fy)
            rink_scene(c, t, th, th0=-1.2)
            c.restore()
            c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E293B", "#0B1020"]))
        elif ph == "closer":
            rink_scene(c, t, th, th0=th - 6.0, lit=1.0, steam=0.6)
        else:
            rink_scene(c, t, th, th0=th - (2.5 if ph == "cta" else 4.0), lit=0.4 if ph == "stat" else 0.0)

    def ui_rink(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "hot", T["hot0"] - 0.2, s("break1") + 0.1, accent=WARN, size=58)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=52)

    # ------------------------------------------------------------------ set: grooves (break1)
    def draw_grooves(self, c, t):
        T, s = self.T, self.tl.s
        grooves(c, t, carve=prog(t, s("break1") - 0.1, T["why"]))

    def ui_grooves(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "grooves", T["skates"] - 0.1, T["why"] - 0.1, accent=WARN, size=58)
        self.chip(540, 300, "why", T["why"] - 0.1, s("fix1") - 0.1, accent=HILITE, size=60)
        self.badge("alert", T["groove1"], s("fix1") - 0.2, x=160, y=470)
        self.red(T["groove1"], 1.2)

    # ------------------------------------------------------------------ set: cutaway (fix1 .. fix4)
    def draw_cutaway(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        order = ("fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4")
        i = order.index(ph) if ph in order else 6
        mx = 240 + (t - s("fix1")) * 6                 # the machine creeps forward through the whole sequence
        kw = dict(shave=1.0 if i >= 0 else 0.0)
        if i == 0:
            kw.update(shave=prog(t, T["blade"] - 0.2, T["shaves"] + 0.2), coin=prog(t, T["coin"] - 0.4, T["coin"]))
        if i >= 1:
            kw.update(snow=prog(t, s("break2"), T["pile1"] + 0.3) if i == 1 else 1.0 - prog(t, T["spinning"], T["tank"]) if i == 2
                      else 0.0)
        if i >= 2:
            kw.update(spin=prog(t, T["spinning"] - 0.3, T["spinning"]) if i == 2 else 1.0,
                      tank=prog(t, T["screw"], T["tank"] + 0.4) if i == 2 else 1.0)
        if i >= 3:
            kw.update(dirt=1.0 if i == 3 else 1.0 - prog(t, T["wash"], T["dirty"] + 0.3))
        if i >= 4:
            kw.update(wash=prog(t, T["jets"] - 0.2, T["jets"] + 0.2) if i == 4 else 1.0)
        if i >= 5:
            kw.update(dents=1.0 if i == 5 else 1.0 - prog(t, T["hot4"], T["glass"]))
        if i >= 6:
            kw.update(towel=prog(t, T["towel"] - 0.3, T["towel"] + 0.2))
        zk = e_io(prog(t, s("break3") - 0.4, s("break3") + 0.2))            # close on the blade and screws, then out
        z = lerp(1.45, 1.0, zk)
        c.save()
        c.translate(540, 860)
        c.scale(z, z)
        c.translate(-lerp(420, 540, zk), -lerp(900, 860, zk))
        cutaway(c, t, mx, **kw)
        c.restore()
        c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E293B", "#0B1020"]))
        # close-ups for the grooves, the dents and the fresh layer
        if i == 3 or i == 4:
            magnifier(c, 250, 590, 160, t, dirt=1.0, wash=prog(t, T["wash"], T["dirty"] + 0.3) if i == 4 else 0.0,
                      a=prog(t, s("break3") - 0.1, s("break3") + 0.3))
        elif i == 5 or i == 6:
            magnifier(c, 250, 590, 160, t, dents=1.0, fill=prog(t, T["hot4"], T["freezes"]) if i == 6 else 0.0,
                      a=prog(t, s("break4") - 0.1, s("break4") + 0.3))

    def ui_cutaway(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix1":
            self.chip(540, 300, "blade", T["blade"] - 0.2, T["coin"] - 0.4, accent="#E5E7EB", size=50)
            self.chip(540, 300, "coin", T["coin"] - 0.4, s("break2") - 0.15, accent=GOOD, size=54)
            self.badge("check", T["coin1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "pile", T["pile"] - 0.3, s("fix2") - 0.15, accent=WARN, size=62)
            self.badge("alert", T["pile1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["pile1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "screw", T["spinning"] - 0.2, T["tank"] - 0.3, accent="#CBD5E1", size=56)
            self.chip(540, 300, "tank", T["tank"] - 0.3, s("break3") - 0.15, accent=GOOD, size=56)
            self.badge("check", T["tank1"], s("break3") - 0.15, x=160, y=470)
        elif ph == "break3":
            self.chip(540, 300, "dirt", T["dirt"] - 0.2, s("fix3") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["dirt1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["dirt1"], 1.2)
        elif ph == "fix3":
            self.chip(540, 300, "jets", T["jets"] - 0.2, T["vacuum"] - 0.2, accent="#7DD3FC", size=58)
            self.chip(540, 300, "vac", T["vacuum"] - 0.2, s("break4") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["dirty1"], s("break4") - 0.15, x=160, y=470)
        elif ph == "break4":
            self.chip(540, 300, "bumpy", s("break4") + 0.1, s("fix4") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["bumpy1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["bumpy1"], 1.2)
        else:
            self.chip(540, 300, "towel", T["towel"] - 0.2, T["freezes"] - 0.2, accent="#93C5FD", size=48)
            self.chip(540, 300, "glass", T["freezes"] - 0.2, s("cta") - 0.15, accent=GOOD, size=56)
            self.badge("check", T["glass1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: lens (reveal)
    def draw_lens(self, c, t):
        T, s = self.T, self.tl.s
        lens(c, t, melt=prog(t, T["melts"] - 0.3, T["old"] + 0.2), fuse=prog(t, T["new"], T["sticks"] + 0.4))

    def ui_lens(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "melt", T["melts"] - 0.2, T["new"] - 0.1, accent="#FDBA74", size=56)
        self.chip(540, 300, "stick", T["new"] - 0.1, s("stat") - 0.15, accent=GOOD, size=56)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:
            arena_tag(c, t, cheer=1.0, kitchen=prog(t, T["t_nobody"] - 0.3, T["t_nobody"]))
        else:
            mom_tag(c, t, wag=prog(t, T["t_nobody"], T["t_nobody"] + 0.3))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "cheer", T["t_cheer"] - 0.2, T["t_nobody"] - 0.2, accent=HILITE, size=56)
        self.chip(540, 300, "clap", T["t_nobody"] - 0.2, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.hum(3.0, 82.0), -18), (T["hot0"], sfx.hiss(1.4, 62), -12),
              (T["bath"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["skates"], sfx.hiss(0.6, 64), -10),
               (T["groove1"], sfx.snap(65), -8), (T["groove1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 66), -6), (T["blade"], sfx.hiss(1.0, 67), -12),
               (T["coin1"], sfx.ding(), -8), (T["coin1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pile1"], sfx.thud(0.4, 68), -8), (T["pile1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["spinning"], sfx.whirr(1.6, 120.0, 180.0, 69), -10), (T["tank1"], sfx.ding(), -8),
               (T["tank1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["dirt1"], sfx.womp(), -10), (T["dirt1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["jets"], sfx.hiss(1.2, 70), -10), (T["vacuum"], sfx.whirr(1.0, 300.0, 420.0, 71), -12),
               (T["dirty1"], sfx.ding(), -8), (T["dirty1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["bumpy1"], sfx.thunk(72), -8), (T["bumpy1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["towel"], sfx.hiss(1.6, 73), -12), (T["glass1"], sfx.sparkle(1.0, 10, 74), -8), (T["glass1"], sfx.ding(), -8),
               (T["glass1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["melts"], sfx.sizzle(0.8, 95), -12),
               (T["sticks"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_cheer"], sfx.riser(0.8, 104), -12),
               (T["t_kitchen"], sfx.womp(), -8)]
        return ev


NAME = "resurfacer"
EPISODE = Resurfacer
