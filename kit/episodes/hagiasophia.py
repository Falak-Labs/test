"""Episode 49 - The Hagia Sophia's dome.  v2 look: warm brick and gold inside, pink walls and grey lead domes outside,
a deep blue Istanbul dusk.

Sets: hall (hook: the building cut open, its brick dome floating on a ring of forty windows full of light over a huge
hall with tiny people; break3/fix3: the dome dark and solid, cracking, then forty ribs and forty windows open; reveal:
gold spreads over the dome, sun rays pour in, the dome seems to hang from the sky), pend (break1/fix1, 3D: a round
drum, then a square hall the round dome does not fit; four arches rise on four piers, curved brick triangles fill the
corners and the square turns into a circle), frame (break2/fix2: the dome pushes its piers outward until half domes
and buttresses catch the push; break4/fix4: an earthquake brings the first, flatter dome down; the new steeper dome,
the push arrows shrink, bricks in mortar as thick as the bricks bend instead of breaking), city (stat + closer: the
building over the Bosphorus at dusk), tag (a phone slides off a couch and its screen cracks).
World (hall / frame / city): front views, the floor at y = 0, 1 m = 16 units; the dome is about 31 m wide.
"""
from v2_base import *  # noqa: F401,F403
from falaj import word  # noqa: E402
from windtower import arrow  # noqa: E402
from phone import phone as phone_dev  # noqa: E402
from humanoid import crack_snd  # noqa: E402

DUSK = {"top": "#050A24", "upper": "#0E1A4A", "mid": "#263A7A", "low": "#6B5A8E", "horizon": "#F2A06B",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
GOLD, GOLD_D = "#C99A3A", "#7A5418"
BRICK, BRICK_D = "#A8654A", "#5E3324"
CUT, CUT_D = "#8A5440", "#4A2A1E"                 # brick in section
INNER, INNER_D = "#4A372C", "#241A15"             # the hall's walls in shadow
PINK, PINK_D = "#B87B5E", "#7E4A35"
LEAD, LEAD_D = "#8C9AB0", "#4E5B70"
MARBLE = "#3F6E5C"
SUNC = "#FFE3A0"
RD = 250                                           # dome radius
Y_RING, Y_WIN = -620, -700                         # cornice under the windows, base of the dome shell
RISE_NEW, RISE_OLD = 190, 120


# ====================================================================================== hall pieces
def Padd(col, a):
    p_ = P(col, a)
    p_.setBlendMode(PLUS)
    return p_


def dome_pts(rise, a=RD, y0=Y_WIN, n=48, grow=0.0):
    return [(-(a + grow) * math.cos(math.pi * i / n), y0 - (rise + grow) * math.sin(math.pi * i / n)) for i in range(n + 1)]


def path_of(pts, close=True):
    p_ = skia.Path()
    p_.moveTo(*pts[0])
    for q in pts[1:]:
        p_.lineTo(*q)
    if close:
        p_.close()
    return p_


def win_x(i, n=20):
    """Centre x and width factor of the i-th window of the far half of the ring (seen from the front)."""
    th = math.pi * (i + 0.5) / n
    return -RD * math.cos(th), math.sin(th)


def hall(c, t, wins=1.0, ribs=1.0, gold=0.0, light=1.0, solid=0.0, cracks=0.0, lift=0.0, sag=0.0, people=1.0, rise=RISE_NEW):
    """The building cut open through its middle (world space).  wins: how many of the forty windows are open,
    ribs 0..1 ribs drawn, gold 0..1 mosaic spread from the crown, light 0..1 sunlight, solid 0..1 a heavy solid dome,
    cracks 0..1, lift: the dome floats up (world units), sag: the solid dome sinks."""
    # ---- the building's mass in section
    mass = skia.Path()
    mass.moveTo(-760, 0)
    mass.lineTo(-760, -430)
    mass.lineTo(-360, -500)
    mass.lineTo(-340, -640)
    for x, y in dome_pts(rise, a=RD + 34, grow=0.0):
        mass.lineTo(x, y - 34 * math.sqrt(max(0.0, 1 - (x / (RD + 34)) ** 2)) - lift)
    mass.lineTo(340, -640)
    mass.lineTo(360, -500)
    mass.lineTo(760, -430)
    mass.lineTo(760, 0)
    mass.close()
    c.drawPath(mass, lin_paint(0, -900, 0, 0, [CUT, CUT_D]))
    tex(c, mass, "stone", 0.8, 0.25)
    # ---- the interior: aisles and nave
    c.drawRect(R(-700, -420, 370, 420), lin_paint(0, -420, 0, 0, [INNER, INNER_D]))
    c.drawRect(R(330, -420, 370, 420), lin_paint(0, -420, 0, 0, [INNER, INNER_D]))
    nave = skia.Path()
    nave.moveTo(-RD, 0)
    nave.lineTo(-RD, Y_WIN - lift)
    for x, y in dome_pts(rise):
        nave.lineTo(x, y - lift)
    nave.lineTo(RD, 0)
    nave.close()
    c.drawPath(nave, lin_paint(0, Y_WIN - rise, 0, 0, ["#3A2A20", "#5A4232", "#2A1E18"]))
    for sd in (-1, 1):                                                      # aisle arcades, two floors
        for f, (y0, y1, n) in enumerate(((0, -190, 3), (-230, -380, 4))):
            x0, x1 = (-690, -340) if sd < 0 else (340, 690)
            c.drawRect(R(x0, y0 - 10 if f else -8, x1 - x0, 10), P("#6E5444"))
            for k in range(n):
                cx_ = lerp(x0, x1, (k + 0.5) / n)
                aw = (x1 - x0) / n * 0.7
                ap = skia.Path()
                ap.moveTo(cx_ - aw / 2, y0 - (12 if f else 0))
                ap.lineTo(cx_ - aw / 2, y1 + aw / 2)
                ap.arcTo(R(cx_ - aw / 2, y1, aw, aw), 180, 180, False)
                ap.lineTo(cx_ + aw / 2, y0 - (12 if f else 0))
                ap.close()
                c.drawPath(ap, P("#1A120E"))
                if light > 0:
                    c.drawPath(ap, P("#FFB766", 0.18 * light))
            for k in range(n + 1):                                          # green marble columns
                cx_ = lerp(x0, x1, k / float(n))
                c.drawRect(R(cx_ - 7, y1 + 10, 14, (y0 - y1) - 12), lin_paint(cx_ - 7, 0, cx_ + 7, 0, [MARBLE, "#6FA08A", MARBLE]))
    # ---- far side of the nave: gallery arcades, the far great arch, the tympanum with its windows
    for f, (y0, y1, n) in enumerate(((0, -200, 5), (-240, -360, 7))):
        c.drawRect(R(-RD, y0 - (14 if f else 6), 2 * RD, 12), P("#7A5E4C"))
        for k in range(n):
            cx_ = lerp(-RD, RD, (k + 0.5) / n)
            aw = 2 * RD / n * 0.68
            ap = skia.Path()
            ap.moveTo(cx_ - aw / 2, y0 - (14 if f else 6))
            ap.lineTo(cx_ - aw / 2, y1 + aw / 2)
            ap.arcTo(R(cx_ - aw / 2, y1, aw, aw), 180, 180, False)
            ap.lineTo(cx_ + aw / 2, y0 - (14 if f else 6))
            ap.close()
            c.drawPath(ap, P("#140E0B"))
        for k in range(n + 1):
            cx_ = lerp(-RD, RD, k / float(n))
            c.drawRect(R(cx_ - 6, y1 + 8, 12, (y0 - y1) - 16), lin_paint(cx_ - 6, 0, cx_ + 6, 0, [MARBLE, "#6FA08A", MARBLE]))
    arch = skia.Path()                                                      # the tympanum under the far arch
    arch.moveTo(-RD, -370)
    arch.arcTo(R(-RD, -370 - RD, 2 * RD, 2 * RD), 180, 180, False)
    arch.lineTo(RD, -370)
    arch.close()
    c.drawPath(arch, lin_paint(0, -620, 0, -370, ["#5E4636", "#3E2C22"]))
    for row, (yy, n, wh) in enumerate(((-420, 7, 44), (-500, 5, 46), (-570, 3, 40))):
        for k in range(n):
            wx = lerp(-RD * 0.8, RD * 0.8, (k + 0.5) / n) * (1 - row * 0.18)
            c.drawRRect(rr(wx - 12, yy - wh, 24, wh, 10), P("#1C1410"))
            if light > 0:
                c.drawRRect(rr(wx - 12, yy - wh, 24, wh, 10), P(SUNC, 0.75 * light))
    sp_ = skia.Path()                                                       # the far pendentives (spandrels)
    for sd in (-1, 1):
        sp_.reset()
        sp_.moveTo(sd * RD, -370)
        sp_.lineTo(sd * RD, Y_RING)
        sp_.lineTo(0, Y_RING)
        n = 16
        for i in range(n + 1):
            an = math.pi / 2 * (1 - i / float(n))
            sp_.lineTo(sd * RD * math.cos(an), -370 - RD * math.sin(an))
        sp_.close()
        c.drawPath(sp_, lin_paint(0, Y_RING, 0, -370, [mix("#6A4A36", GOLD, gold), mix("#4A3426", GOLD_D, gold)]))
        if gold > 0:
            c.drawCircle(sd * RD * 0.62, -520, 26, P("#E8C46A", 0.7 * gold))
            c.drawCircle(sd * RD * 0.62, -520, 26, P(GOLD_D, 0.9 * gold, stroke=4))
    c.drawPath(arch, P("#C9A27A", 0.8, stroke=6))
    c.drawRect(R(-RD, Y_RING - 10, 2 * RD, 12), P("#D8C3A0"))              # the cornice
    # ---- the window band and the dome (both float up by lift)
    c.save()
    c.translate(0, -lift)
    if lift > 0:
        add_glow(c, 0, Y_RING - 40, RD * 1.3, SUNC, 0.35 * min(1.0, lift / 20.0) * light)
    c.drawRect(R(-RD, Y_WIN, 2 * RD, Y_RING - Y_WIN - 10), P("#3A2A20"))
    for i in range(20):
        wx, wf = win_x(i)
        ww = 18 * wf + 2
        open_ = clamp(wins * 20 - i)
        c.drawRRect(rr(wx - ww / 2, Y_WIN + 8, ww, (Y_RING - Y_WIN) - 26, ww * 0.45), P("#120C09"))
        if open_ > 0 and light > 0:
            c.drawRRect(rr(wx - ww / 2, Y_WIN + 8, ww, (Y_RING - Y_WIN) - 26, ww * 0.45), P(SUNC, open_ * light))
            add_glow(c, wx, (Y_WIN + Y_RING) / 2, 50, "#FFD27A", 0.5 * open_ * light)
    dp = path_of(dome_pts(rise) + [(RD, Y_WIN)])
    inner = mix(mix("#6E4A36", "#3A2A22", solid), GOLD, gold)
    c.save()
    c.clipPath(dp, doAntiAlias=True)
    c.drawRect(R(-RD, Y_WIN - rise - 10, 2 * RD, rise + 12), lin_paint(0, Y_WIN - rise, 0, Y_WIN, [inner, shade(inner, -0.3)]))
    if gold > 0:                                                            # gold spreads from the crown down
        gy = lerp(Y_WIN - rise, Y_WIN + 4, clamp(gold))
        c.drawRect(R(-RD, Y_WIN - rise - 10, 2 * RD, gy - (Y_WIN - rise - 10)),
                   lin_paint(0, Y_WIN - rise, 0, Y_WIN, ["#E2B85A", GOLD, GOLD_D]))
        rng = random.Random(5)
        for _ in range(160):
            x = rng.uniform(-RD, RD)
            y = rng.uniform(Y_WIN - rise, gy)
            c.drawRect(R(x, y, 5, 5), P("#FFE7A8", 0.35 * gold))
    if solid > 0:
        tex(c, dp, "stone", 1.2, 0.5 * solid)
    nr = int(round(20 * ribs))
    for k in range(nr + 1 if ribs > 0 else 0):                              # the ribs, seen from inside
        th = math.pi * k / 20.0
        pts = [(-RD * math.cos(th) * math.cos(f * math.pi / 32), Y_WIN - rise * math.sin(f * math.pi / 32)) for f in range(17)]
        c.drawPath(path_of(pts, close=False), P(mix("#2A1C14", "#8A6020", gold), 0.9, stroke=7))
    if cracks > 0:
        rng = random.Random(9)
        for k in range(7):
            x, y = rng.uniform(-60, 60), Y_WIN - rise + 6
            cp = skia.Path()
            cp.moveTo(x, y)
            for j in range(int(6 * cracks) + 1):
                x += rng.uniform(-30, 30)
                y += rng.uniform(16, 34)
                cp.lineTo(x, y)
            c.drawPath(cp, P("#0A0605", 0.9, stroke=4))
    c.restore()
    c.drawCircle(0, Y_WIN - rise + 30, 22, P(mix("#2A1C14", "#F0CF7A", gold), 0.9))
    th_ = lerp(14, 46, solid)
    outer = [(x, y - th_ * math.sqrt(max(0.0, 1 - (x / (RD + 34)) ** 2))) for x, y in dome_pts(rise, a=RD + 34)]
    shell = path_of(outer + list(reversed(dome_pts(rise))))
    c.drawPath(shell, lin_paint(0, Y_WIN - rise - 40, 0, Y_WIN, [LEAD, LEAD_D]))
    c.drawPath(path_of(dome_pts(rise), close=False), P(CUT_D, 1.0, stroke=10))
    c.restore()
    # ---- the cut piers at the sides of the nave
    for sd in (-1, 1):
        x0 = -340 if sd < 0 else RD
        c.drawRect(R(x0, Y_RING - 20, 90, -(Y_RING - 20)), lin_paint(x0, 0, x0 + 90, 0, [CUT, CUT_D]))
        for k in range(14):
            c.drawLine(x0, -k * 46, x0 + 90, -k * 46 - 30, P(CUT_D, 0.6, stroke=3))
    # ---- the floor, sunlight and people
    c.drawRect(R(-1500, 0, 3000, 1800), lin_paint(0, 0, 0, 300, ["#4A3A30", "#1A1410"]))
    if light > 0 and wins > 0:
        for i in range(0, 20, 2):
            wx, wf = win_x(i)
            open_ = clamp(wins * 20 - i)
            if open_ <= 0:
                continue
            bp = skia.Path()
            bp.moveTo(wx - 10, Y_RING - 30 - lift)
            bp.lineTo(wx + 10, Y_RING - 30 - lift)
            bp.lineTo(wx * 0.35 + 70, 0)
            bp.lineTo(wx * 0.35 + 10, 0)
            bp.close()
            c.drawPath(bp, Padd("#FFE2A0", 0.10 * open_ * light))
        c.drawOval(R(-220, -26, 440, 52), Padd("#FFD58A", 0.22 * light * clamp(wins * 2)))
    if people > 0:
        for k, (px, col, f) in enumerate(((-150, "#2563EB", 1), (-95, "#DB2777", 1), (-20, "#F59E0B", -1), (60, "#10B981", -1),
                                         (130, "#7C3AED", -1), (185, "#EF4444", 1))):
            person(c, px, 0, 30, col, t + k * 0.4, pose="look", face=f, hat="none", hair="#1C1917", a=people)


# ====================================================================================== pend pieces (3D)
YAW, PITCH = math.radians(32), math.radians(24)
A3, H0 = 200.0, 250.0                               # half side of the square hall, height of the piers


def p3(x, y, z, o):
    ox, oy, s = o
    xr = x * math.cos(YAW) - z * math.sin(YAW)
    zr = x * math.sin(YAW) + z * math.cos(YAW)
    yr = y * math.cos(PITCH) + zr * math.sin(PITCH)
    return ox + xr * s, oy - yr * s


def poly3(pts, o):
    return path_of([p3(x, y, z, o) for x, y, z in pts])


def pier3(c, sx, sz, h, o, a=1.0):
    if h <= 0 or a <= 0:
        return
    w = 30
    x0, z0 = sx * A3, sz * A3
    faces = [[(x0 - w, 0, z0 - w), (x0 + w, 0, z0 - w), (x0 + w, h, z0 - w), (x0 - w, h, z0 - w)],
             [(x0 - w, 0, z0 - w), (x0 - w, 0, z0 + w), (x0 - w, h, z0 + w), (x0 - w, h, z0 - w)]]
    c.drawPath(poly3(faces[0], o), P(BRICK, a))
    c.drawPath(poly3(faces[1], o), P(BRICK_D, a))
    c.drawPath(poly3([(x0 - w, h, z0 - w), (x0 + w, h, z0 - w), (x0 + w, h, z0 + w), (x0 - w, h, z0 + w)], o), P("#C98A6A", a))


def arch3(c, plane, sgn, o, k=1.0, a=1.0, col=BRICK):
    """One arch on top of the piers in the plane x = sgn*A3 ("x") or z = sgn*A3 ("z"); k 0..1 draws it from both ends."""
    if k <= 0 or a <= 0:
        return
    n = 24
    outer, inner = [], []
    for i in range(n + 1):
        u = i / float(n)
        if abs(u - 0.5) > 0.5 * k:
            continue
        an = math.pi * u
        for rad, lst in ((A3 + 26, outer), (A3 - 4, inner)):
            q = -math.cos(an) * min(rad, A3 + 26)
            y = H0 + math.sin(an) * rad
            lst.append((sgn * A3, y, q) if plane == "x" else (q, y, sgn * A3))
    if len(outer) < 2:
        return
    c.drawPath(poly3(outer + list(reversed(inner)), o), P(col, a))
    c.drawPath(poly3(outer + list(reversed(inner)), o), P(BRICK_D, 0.8 * a, stroke=3))


def pend3(c, sx, sz, k, o, a=1.0, col="#C9774E"):
    """The pendentive in corner (sx, sz), filled from the corner up to the fraction k of its height."""
    if k <= 0 or a <= 0:
        return
    hk = A3 * clamp(k)
    rq = math.sqrt(2 * A3 * A3 - hk * hk)
    zq = math.sqrt(max(0.0, rq * rq - A3 * A3))
    pts = []
    n = 14
    for i in range(n + 1):                                                  # up the arch in plane x = sx*A3
        z = lerp(sz * A3, sz * zq, i / float(n))
        pts.append((sx * A3, H0 + math.sqrt(max(0.0, A3 * A3 - z * z)), z))
    a0, a1 = math.atan2(sz * zq, sx * A3), math.atan2(sz * A3, sx * zq)
    for i in range(1, n):                                                   # the top edge at height hk
        an = lerp(a0, a1, i / float(n))
        pts.append((rq * math.cos(an), H0 + hk, rq * math.sin(an)))
    for i in range(n + 1):                                                  # down the arch in plane z = sz*A3
        x = lerp(sx * zq, sx * A3, i / float(n))
        pts.append((x, H0 + math.sqrt(max(0.0, A3 * A3 - x * x)), sz * A3))
    pp = poly3(pts, o)
    c.drawPath(pp, P(col, a))
    c.save()
    c.clipPath(pp, doAntiAlias=True)
    ox, oy, s = o
    for j in range(16):                                                     # brick courses
        yy = oy - (H0 + j * 14) * s * math.cos(PITCH) - 200
        c.drawLine(ox - 600, yy + 300, ox + 600, yy + 300, P(BRICK_D, 0.35 * a, stroke=2))
    c.restore()
    c.drawPath(pp, P("#FFD9A8", 0.5 * a, stroke=3))


def ring3(c, o, col, a=1.0, w=8, half=None):
    pts = []
    for i in range(65):
        an = 2 * math.pi * i / 64.0
        pts.append(p3(A3 * math.cos(an), H0 + A3, A3 * math.sin(an), o))
    c.drawPath(path_of(pts), P(col, a, stroke=w))


def dome3(c, o, drop=0.0, a=1.0):
    """The dome on the ring: the upper half of its outline circle plus the front half of the ring's ellipse."""
    if a <= 0:
        return
    ox, oy, s = o
    cx_, cy_ = p3(0, H0 + A3 + drop, 0, o)
    rx, ry = A3 * s, A3 * s * math.sin(PITCH)
    dp = skia.Path()
    dp.addArc(R(cx_ - rx, cy_ - rx * 0.78, 2 * rx, 2 * rx * 0.78), 180, 180)
    dp.arcTo(R(cx_ - rx, cy_ - ry, 2 * rx, 2 * ry), 0, 180, False)
    dp.close()
    c.drawPath(dp, rad_paint(cx_ - rx * 0.3, cy_ - rx * 0.5, rx * 1.4, [LEAD, "#6E7C93", LEAD_D], a=a))
    for k in range(1, 8):                                                   # ribs on the lead
        xx = cx_ - rx + 2 * rx * k / 8.0
        dd = skia.Path()
        dd.moveTo(cx_, cy_ - rx * 0.78)
        dd.quadTo(xx + (xx - cx_) * 0.25, cy_ - rx * 0.5, xx, cy_ + ry * math.sqrt(max(0.0, 1 - ((xx - cx_) / rx) ** 2)))
        c.drawPath(dd, P("#3E4A5E", 0.45 * a, stroke=2.5))
    for k in range(13):                                                     # the ring of windows
        an = math.pi * (k + 0.5) / 13.0
        wx = cx_ - rx * math.cos(an)
        wy = cy_ + ry * math.sin(an) - 14 * s
        c.drawRRect(rr(wx - 5 * s, wy - 12 * s, 10 * s, 18 * s, 4 * s), P("#FFD58A", 0.9 * a))


def emperor(c, x, y, h, t, a=1.0):
    person(c, x, y, h, "#6D28D9", t, pose="point", face=1, hat="none", hair="#3F2A1A", a=a)
    u = h / 140.0
    cp = skia.Path()                                                        # a gold crown
    cp.moveTo(x - 16 * u, y - 136 * u)
    cp.lineTo(x - 16 * u, y - 156 * u)
    cp.lineTo(x - 8 * u, y - 146 * u)
    cp.lineTo(x, y - 160 * u)
    cp.lineTo(x + 8 * u, y - 146 * u)
    cp.lineTo(x + 16 * u, y - 156 * u)
    cp.lineTo(x + 16 * u, y - 136 * u)
    cp.close()
    c.drawPath(cp, P("#FACC15", a))


# ====================================================================================== frame pieces (section diagram)
def frame(c, t, rise=RISE_NEW, lean=0.0, half=0.0, butt=0.0, cracks=0.0, fall=None, ghost=0.0, a=1.0):
    """The dome on its two piers in section (world space).  lean: degrees the piers tip outward, half 0..1 the half
    domes sliding in, butt 0..1 the buttresses rising, fall: (t0) the dome breaks and falls, ghost: old outline."""
    c.drawRect(R(-RD, Y_RING, 2 * RD, -Y_RING), lin_paint(0, Y_RING, 0, 0, ["#3A2A20", "#5A4232", "#2A1E18"]))
    for k, (px, col) in enumerate(((-120, "#2563EB"), (-40, "#DB2777"), (70, "#F59E0B"), (150, "#10B981"))):
        person(c, px, 0, 34, col, t + k * 0.5, pose="look", face=1 if px < 0 else -1, hat="none", hair="#1C1917", a=a)
    for sd in (-1, 1):                                                      # half domes sliding in from the sides
        if half > 0:
            off = (1 - e_out(clamp(half))) * 700 * sd
            c.save()
            c.translate(off, 0)
            hp = skia.Path()
            hx = sd * 340
            hp.moveTo(hx, Y_RING)
            n = 20
            for i in range(n + 1):
                an = math.pi / 2 * i / float(n)
                hp.lineTo(hx + sd * 300 * math.sin(an), Y_RING + 300 * (1 - math.cos(an)))
            hp.lineTo(hx + sd * 300, 0)
            hp.lineTo(hx + sd * 240, 0)
            for i in range(n, -1, -1):
                an = math.pi / 2 * i / float(n)
                hp.lineTo(hx + sd * 240 * math.sin(an), Y_RING + 60 + 240 * (1 - math.cos(an)))
            hp.lineTo(hx, Y_RING + 60)
            hp.close()
            ip = skia.Path()                                                 # the space under the half dome
            ip.moveTo(hx, Y_RING + 60)
            for i in range(n + 1):
                an = math.pi / 2 * i / float(n)
                ip.lineTo(hx + sd * 240 * math.sin(an), Y_RING + 60 + 240 * (1 - math.cos(an)))
            ip.lineTo(hx + sd * 240, 0)
            ip.lineTo(hx, 0)
            ip.close()
            c.drawPath(ip, lin_paint(0, Y_RING, 0, 0, ["#3A2A20", "#5A4232", "#2A1E18"]))
            c.drawPath(hp, lin_paint(0, Y_RING, 0, 0, [LEAD, LEAD_D]))
            c.drawRect(R(hx + (sd * 240 if sd > 0 else -300), Y_RING + 300, 60, 0 - (Y_RING + 300)), P(PINK_D))
            c.restore()
    for sd in (-1, 1):                                                      # the two piers, tipping out by lean
        c.save()
        px = sd * RD
        c.translate(sd * (RD + 45), 0)
        c.rotate(sd * lean)
        c.translate(-sd * (RD + 45), 0)
        x0 = -RD - 90 if sd < 0 else RD
        c.drawRect(R(x0, Y_RING, 90, -Y_RING), lin_paint(x0, 0, x0 + 90, 0, [PINK, PINK_D] if sd > 0 else [PINK_D, PINK]))
        for k in range(12):
            c.drawLine(x0, -k * 52, x0 + 90, -k * 52, P(PINK_D, 0.5, stroke=3))
        if cracks > 0:
            cp = skia.Path()
            cp.moveTo(px + sd * 10, Y_RING)
            cp.lineTo(px + sd * 30, Y_RING + 60 * cracks)
            cp.lineTo(px + sd * 12, Y_RING + 110 * cracks)
            c.drawPath(cp, P("#1A0A06", 0.9, stroke=5))
        c.restore()
    for sd in (-1, 1):                                                      # buttresses: massive blocks hugging the piers
        if butt > 0:
            hb = -560 * e_out(clamp(butt))
            x0 = RD + 40 if sd > 0 else -RD - 190
            c.drawRect(R(x0 + (20 if sd > 0 else -20), hb - 10, 150, -hb + 10), P("#000000", 0.35, blur=12))
            c.drawRect(R(x0, hb, 150, -hb), lin_paint(x0, 0, x0 + 150, 0, ["#D49A7C", PINK, PINK_D] if sd > 0 else [PINK_D, PINK, "#D49A7C"]))
            tex(c, R(x0, hb, 150, -hb), "stone", 0.9, 0.3)
            for k in range(int(-hb / 70)):
                c.drawLine(x0, -k * 70 - 20, x0 + 150, -k * 70 - 20, P(PINK_D, 0.5, stroke=3))
            for k in range(2):
                if hb < -150 - k * 220 - 90:
                    c.drawRRect(rr(x0 + 45, -150 - k * 220 - 90, 60, 90, 28), P("#2A1A14"))
    mid = math.radians(lean) * 620                                          # the dome base spreads with the piers
    c.drawRect(R(-RD - mid, Y_WIN, 2 * (RD + mid), Y_RING - Y_WIN), P(PINK))
    for i in range(11):
        wx = lerp(-RD + 30, RD - 30, i / 10.0) * (1 + mid / RD)
        c.drawRRect(rr(wx - 8, Y_WIN + 14, 16, 50, 7), P("#FFD58A", 0.85 * a))
    if fall is not None and t >= fall:                                       # the dome breaks into falling chunks
        age = t - fall
        rng = random.Random(4)
        pts = dome_pts(rise, n=16)
        for i in range(16):
            (x0_, y0_), (x1_, y1_) = pts[i], pts[i + 1]
            vx = rng.uniform(-60, 60)
            dy = 0.5 * 1500 * max(0.0, age - rng.uniform(0, 0.25)) ** 2
            rot = rng.uniform(-200, 200) * age
            mx, my = (x0_ + x1_) / 2 + vx * age, min((y0_ + y1_) / 2 + dy, -30)
            c.save()
            c.translate(mx, my)
            c.rotate(rot)
            c.drawRRect(rr(-30, -18, 60, 36, 6), P(LEAD_D))
            c.drawRRect(rr(-30, -18, 60, 12, 6), P(LEAD))
            c.restore()
        if age < 2.5:
            for k in range(6):
                v2.puff(c, -200 + k * 80, -40, 90 + 160 * age, "#B8A090", 0.5 * clamp(1 - age / 2.5), k=k)
    else:
        c.drawPath(path_of([(x * (1 + mid / RD), y) for x, y in dome_pts(rise)]), lin_paint(0, Y_WIN - rise, 0, Y_WIN, ["#2A1E18", "#4A3628"]))
        for k in range(1, 10):
            th = math.pi * k / 10.0
            pts = [(-RD * (1 + mid / RD) * math.cos(th) * math.cos(f * math.pi / 32), Y_WIN - rise * math.sin(f * math.pi / 32))
                   for f in range(17)]
            c.drawPath(path_of(pts, close=False), P("#6E5040", 0.6, stroke=4))
        outer = [(x * (1 + mid / RD), y - 30 * math.sqrt(max(0.0, 1 - (x / RD) ** 2))) for x, y in dome_pts(rise)]
        dp = path_of(outer + list(reversed([(x * (1 + mid / RD), y) for x, y in dome_pts(rise)])))
        c.drawPath(dp, lin_paint(0, Y_WIN - rise - 30, 0, Y_WIN, [LEAD, LEAD_D]))
        c.drawPath(path_of([(x * (1 + mid / RD), y) for x, y in dome_pts(rise)], close=False), P("#2A3444", 0.9, stroke=4))
        if cracks > 0:
            cp = skia.Path()
            cp.moveTo(0, Y_WIN - rise - 30)
            cp.lineTo(-14, Y_WIN - rise + 30 * cracks)
            cp.lineTo(10, Y_WIN - rise + 70 * cracks)
            c.drawPath(cp, P("#0A0605", 0.9, stroke=5))
    if ghost > 0:
        c.drawPath(path_of(dome_pts(RISE_OLD), close=False), dash_paint("#F8FAFC", ghost, w=5, t=t))


def bricks_mag(c, x, y, r, t, bend=0.0, a=1.0):
    """A magnifier on the dome's wall: brick courses in mortar as thick as the bricks; bend 0..1 sways them."""
    if a <= 0:
        return
    c.save()
    cp = skia.Path()
    cp.addCircle(x, y, r)
    c.drawCircle(x, y + 10, r, P("#000000", 0.4 * a, blur=20))
    c.clipPath(cp, doAntiAlias=True)
    c.drawRect(R(x - r, y - r, 2 * r, 2 * r), P("#D8CBB0", a))              # the mortar
    for j in range(-6, 7):
        yy = y + j * 44
        sway = math.sin(t * 5.0 + j * 0.0) * 26 * bend * (yy - (y + r)) / (2 * r)
        for k in range(-3, 4):
            xx = x + k * 120 + (j % 2) * 60 + sway
            c.drawRRect(rr(xx - 52, yy - 11, 104, 22, 4), P(BRICK, a))
            c.drawRRect(rr(xx - 52, yy - 11, 104, 7, 4), P("#C98A6A", a))
    c.restore()
    c.drawCircle(x, y, r, P("#F8FAFC", a, stroke=10))


# ====================================================================================== city pieces
def exterior(c, t, lit=0.0, minarets=1.0, a=1.0):
    """The building from the south (world space, ground y = 0): body, exedrae, half domes, the tympanum, buttresses,
    the drum with its windows, the dome, four minarets."""
    def minaret(x, h, w, a_):
        c.drawRect(R(x - w / 2, -h + 90, w, h - 90), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#E8D9C4", "#B9A68E"], a=a_))
        for by in (-h * 0.5, -h * 0.72):
            c.drawRect(R(x - w * 0.9, by, w * 1.8, 10), P("#CDBB9F", a_))
        cp = skia.Path()
        cp.moveTo(x - w / 2 - 2, -h + 90)
        cp.lineTo(x, -h - 20)
        cp.lineTo(x + w / 2 + 2, -h + 90)
        cp.close()
        c.drawPath(cp, P(LEAD, a_))
        c.drawCircle(x, -h - 24, 5, P("#FACC15", a_))
    if minarets > 0:
        for x in (-560, 560):
            minaret(x, 880, 18, 0.85 * minarets)
    c.drawRect(R(-720, -300, 1440, 300), lin_paint(0, -300, 0, 0, [PINK, PINK_D]))       # the body
    tex(c, R(-720, -300, 1440, 300), "stone", 0.9, 0.3)
    for k in range(14):
        wx = -660 + k * 101
        if abs(wx) < 380:
            continue
        c.drawRRect(rr(wx - 14, -200, 28, 70, 12), P("#2A1A14"))
        if lit > 0:
            c.drawRRect(rr(wx - 14, -200, 28, 70, 12), P("#FFC46B", 0.8 * lit))
    for sd in (-1, 1):                                                      # exedrae and half domes
        ex = skia.Path()
        ex.moveTo(sd * 520, -300)
        for i in range(17):
            an = math.pi / 2 * i / 16.0
            ex.lineTo(sd * (520 + 170 * math.sin(an)), -300 - 120 * math.cos(an))
        ex.close()
        c.drawPath(ex, lin_paint(0, -420, 0, -300, [LEAD, LEAD_D]))
        hd = skia.Path()
        hd.moveTo(sd * 250, -330)
        for i in range(25):
            an = math.pi / 2 * i / 24.0
            hd.lineTo(sd * (250 + 300 * math.sin(an)), -330 - 290 * math.cos(an))
        hd.close()
        c.drawPath(hd, lin_paint(sd * 250, -620, sd * 550, -330, [LEAD, LEAD_D]))
        for k in range(5):
            an = math.pi / 2 * (k + 0.6) / 5.4
            c.drawRRect(rr(sd * (250 + 286 * math.sin(an)) - 6, -330 - 276 * math.cos(an) + 6, 12, 22, 5),
                        P("#FFD58A" if lit > 0 else "#2A1A14", 0.9))
    ty = skia.Path()                                                        # the south tympanum under the great arch
    ty.addRect(R(-RD, Y_RING, 2 * RD, 320))
    c.drawPath(ty, lin_paint(0, Y_RING, 0, -300, [PINK, PINK_D]))
    c.drawArc(R(-RD, -370 - RD, 2 * RD, 2 * RD), 180, 180, False, P("#E2B89A", 1.0, stroke=10))
    for row, (yy, n) in enumerate(((-340, 7), (-430, 5), (-520, 3))):
        for k in range(n):
            wx = lerp(-RD * 0.78, RD * 0.78, (k + 0.5) / n) * (1 - row * 0.2)
            c.drawRRect(rr(wx - 11, yy - 44, 22, 44, 9), P("#2A1A14"))
            if lit > 0:
                c.drawRRect(rr(wx - 11, yy - 44, 22, 44, 9), P("#FFC46B", 0.7 * lit))
    for sd in (-1, 1):                                                      # the buttresses
        x0 = -370 if sd < 0 else 250
        bp = skia.Path()
        bp.moveTo(x0, 0)
        bp.lineTo(x0, -560)
        bp.lineTo(x0 + 120, -600 if sd < 0 else -560)
        bp.lineTo(x0 + 120, 0)
        bp.close()
        if sd > 0:
            bp = skia.Path()
            bp.moveTo(x0, 0)
            bp.lineTo(x0, -600)
            bp.lineTo(x0 + 120, -560)
            bp.lineTo(x0 + 120, 0)
            bp.close()
        c.drawPath(bp, lin_paint(x0, 0, x0 + 120, 0, [shade(PINK, 0.06), PINK_D] if sd > 0 else [PINK_D, shade(PINK, 0.06)]))
        for k in range(2):
            c.drawRRect(rr(x0 + 34, -150 - k * 200, 52, 90, 24), P("#3A241A"))
    c.drawRect(R(-RD - 24, Y_WIN, 2 * (RD + 24), Y_RING - Y_WIN), lin_paint(-RD, 0, RD, 0, [PINK_D, PINK, PINK_D]))
    for i in range(20):                                                     # the ring of windows (outside)
        an = math.pi * (i + 0.5) / 20.0
        wx = -(RD + 10) * math.cos(an)
        wf = math.sin(an)
        c.drawRRect(rr(wx - 7 * wf - 2, Y_WIN + 14, 14 * wf + 4, 50, 6), P("#FFC46B" if lit > 0 else "#2A1A14", 0.95))
        c.drawRect(R(wx + 9 * wf, Y_WIN + 8, 6 * wf + 2, 72), P(PINK_D))
    outer = dome_pts(RISE_NEW + 24, a=RD + 28)
    dp = path_of(outer + [(RD + 28, Y_WIN)])
    c.drawPath(dp, rad_paint(-90, Y_WIN - 200, 420, ["#A9B6C8", LEAD, LEAD_D]))
    for k in range(1, 20):                                                  # lead ribs
        th = math.pi * k / 20.0
        pts = [(-(RD + 28) * math.cos(th) * math.cos(f * math.pi / 32), Y_WIN - (RISE_NEW + 24) * math.sin(f * math.pi / 32))
               for f in range(17)]
        c.drawPath(path_of(pts, close=False), P("#55627A", 0.5, stroke=3))
    c.drawRect(R(-6, Y_WIN - RISE_NEW - 70, 12, 50), P("#E2B04A"))
    c.drawCircle(0, Y_WIN - RISE_NEW - 74, 9, P("#FACC15"))
    if minarets > 0:
        for x in (-600, 600):
            minaret(x, 940, 22, minarets)


def couch_(c, x, y, s):
    box(c, x - 230 * s, y - 210 * s, 460 * s, 120 * s, "#475569", r=30 * s)
    box(c, x - 250 * s, y - 130 * s, 500 * s, 90 * s, "#64748B", r=24 * s)
    box(c, x - 270 * s, y - 170 * s, 60 * s, 160 * s, "#334155", r=22 * s)
    box(c, x + 210 * s, y - 170 * s, 60 * s, 160 * s, "#334155", r=22 * s)
    c.drawRect(R(x - 240 * s, y - 20 * s, 20 * s, 20 * s), P("#1F2937"))
    c.drawRect(R(x + 220 * s, y - 20 * s, 20 * s, 20 * s), P("#1F2937"))


# ====================================================================================== the episode
class HagiaSophia(EpisodeV2):
    BUILD_NO = 49
    FIRST_SET = "hall"
    CLEAR = "#0E1A4A"
    TITLE = {"en": "HAGIA SOPHIA'S DOME", "ar_sa": "قبة آيا صوفيا"}
    EMPH = {"en": ["CONGRATS", "FLOAT", "BRICK", "DOME", "THIRTY", "METERS", "WIDE", "RING", "LIGHT", "HAGIA", "SOPHIA'S",
                   "ROUND", "WALLS", "EMPEROR", "GIANT", "SQUARE", "HALL", "FOUR", "HUGE", "ARCHES", "CORNERS", "CURVED",
                   "TRIANGLES", "CIRCLE", "HEAVY", "PUSHES", "OUTWARD", "SPREAD", "HALF", "DOMES", "BUTTRESSES", "SIDES",
                   "CATCH", "PUSH", "SOLID", "CRUSH", "DARK", "FORTY", "THIN", "RIBS", "WINDOWS", "BASE", "EARTHQUAKE",
                   "TWENTY-ONE", "YEARS", "CRASHING", "REBUILT", "STEEPER", "LESS", "MORTAR", "THICK", "BRICKS", "BENDS",
                   "BREAKING", "FOLLOW", "KOREAN", "FLOOR", "HEATS", "GOLD", "SUN", "POUR", "HANG", "SKY", "FIFTY-FIVE",
                   "SIX", "FIFTEEN", "CENTURIES", "YOURSELF", "SURVIVED", "EARTHQUAKES", "PHONE", "CRACKED", "COUCH"],
            "ar_sa": ["مبروك", "قبة", "طوب", "أعرض", "ثلاثين", "متر", "تطير", "حلقة", "نور", "آيا", "صوفيا", "القبة",
                      "جدار", "مدوّر", "والإمبراطور", "قاعة", "مربعة", "ضخمة", "فترفع", "أربع", "أقواس", "الزوايا",
                      "بمثلثات", "مقوّسة", "المربع", "دايرة", "بهالثقل", "تدف", "لبرا", "والأقواس", "تتباعد", "نص", "طرف",
                      "ودعامات", "الجوانب", "مليانة", "تنهار", "ثقلها", "ظلمة", "أربعين", "ضلع", "رفيع", "شباك", "زلازل",
                      "وعشرين", "سنة", "طاحت", "بنوها", "أعلى", "أقل", "والمونة", "سماكتها", "الطوبة", "فتنثني", "تنكسر",
                      "تابعني", "كورية", "ذهب", "الشمس", "معلّقة", "السما", "وخمسين", "ست", "خمستعشر", "قرن", "بيدك",
                      "تحمّلت", "وجوالك", "طيحة", "الكنب"]}
    KEYS = {"ar_sa": {
        ("hook", "FLOAT"): "تطير", ("hook", "BRICK"): "طوب", ("hook", "DOME"): "قبة", ("hook", "THIRTY"): "ثلاثين",
        ("hook", "WIDE"): "أعرض", ("hook", "RING"): "حلقة", ("hook", "LIGHT"): "نور", ("hook", "CONGRATS"): "مبروك",
        ("hook", "HAGIA"): "آيا",
        ("break1", "DOME"): "القبة", ("break1", "ROUND"): "مدوّر", ("break1", "WALLS"): "جدار",
        ("break1", "EMPEROR"): "والإمبراطور", ("break1", "SQUARE"): "مربعة", ("break1", "HALL"): "قاعة",
        ("fix1", "RAISE"): "فترفع", ("fix1", "ARCHES"): "أقواس", ("fix1", "FILL"): "وتعبّي", ("fix1", "CORNERS"): "الزوايا",
        ("fix1", "TRIANGLES"): "بمثلثات", ("fix1", "SQUARE"): "المربع", ("fix1", "CIRCLE"): "دايرة",
        ("break2", "HEAVY"): "بهالثقل", ("break2", "PUSHES"): "تدف", ("break2", "OUTWARD"): "لبرا",
        ("break2", "ARCHES"): "والأقواس", ("break2", "SPREAD"): "تتباعد",
        ("fix2", "HALF"): "نص", ("fix2", "ENDS"): "طرف", ("fix2", "BUTTRESSES"): "ودعامات", ("fix2", "SIDES"): "الجوانب",
        ("fix2", "PUSH"): "الجوانب",
        ("break3", "SOLID"): "مليانة", ("break3", "CRUSH"): "تنهار", ("break3", "HALL"): "والقاعة", ("break3", "DARK"): "ظلمة",
        ("fix3", "FORTY"): "أربعين", ("fix3", "RIBS"): "ضلع", ("fix3", "WINDOWS"): "شباك", ("fix3", "BASE"): "شباك",
        ("break4", "EARTHQUAKE"): "زلازل", ("break4", "TWENTY"): "وعشرين", ("break4", "FIRST"): "الأولى",
        ("break4", "CRASHING"): "طاحت",
        ("fix4", "REBUILT"): "بنوها", ("fix4", "STEEPER"): "أعلى", ("fix4", "LESS"): "أقل", ("fix4", "MORTAR"): "والمونة",
        ("fix4", "THICK"): "سماكتها", ("fix4", "BENDS"): "فتنثني", ("fix4", "BREAKING"): "تنكسر",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "GOLD"): "ذهب", ("reveal", "SUN"): "الشمس", ("reveal", "POUR"): "تدخل", ("reveal", "FLOOR"): "تحت",
        ("reveal", "HANG"): "معلّقة", ("reveal", "SKY"): "السما",
        ("stat", "FIFTY"): "علوها", ("stat", "SIX"): "ست", ("stat", "FIFTEEN"): "خمستعشر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SURVIVED"): "تحمّلت", ("tag", "EARTHQUAKES"): "زلازل", ("tag", "PHONE"): "وجوالك",
        ("tag", "CRACKED"): "طيحة", ("tag", "FALLING"): "طيحة", ("tag", "COUCH"): "الكنب"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a Korean heated floor"),
                   "stat": [("55 m", "HIGH"), ("<6", "YEARS TO BUILD"), ("15", "CENTURIES AGO")],
                   "L": {"wide": "OVER 30 m WIDE", "ring": "A RING OF LIGHT", "name": "THE HAGIA SOPHIA",
                         "round": "DOMES SIT ON ROUND WALLS", "square": "HE WANTS A SQUARE HALL", "gap": "IT DOESN'T FIT",
                         "arches": "4 GIANT ARCHES", "pend": "CURVED BRICK TRIANGLES", "circle": "SQUARE INTO CIRCLE",
                         "push": "THE DOME PUSHES OUT", "spread": "THE ARCHES SPREAD", "half": "HALF DOMES",
                         "butt": "GIANT BUTTRESSES", "catch": "THE PUSH GOES DOWN", "crush": "TOO HEAVY",
                         "dark": "DARK INSIDE", "ribs": "40 THIN RIBS", "wins": "40 WINDOWS", "quake": "EARTHQUAKE!",
                         "later": "21 YEARS LATER", "steep": "TALLER + STEEPER", "less": "PUSHES OUT LESS",
                         "mortar": "MORTAR AS THICK AS THE BRICKS", "bends": "IT BENDS, NOT BREAKS", "gold": "GOLD",
                         "hang": "IT SEEMS TO HANG FROM THE SKY", "h": "55 m", "crack": "CRACK!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: أرضية كورية دافية"),
                      "stat": [("55", "متر علو"), ("<6", "سنين بناء"), ("15", "قرن")],
                      "L": {"wide": "أعرض من ثلاثين متر", "ring": "حلقة نور", "name": "آيا صوفيا",
                            "round": "القبة تبي جدار مدوّر", "square": "يبي قاعة مربعة", "gap": "ما تركب!",
                            "arches": "أربع أقواس كبار", "pend": "مثلثات طوب مقوّسة", "circle": "المربع صار دايرة",
                            "push": "القبة تدف لبرا", "spread": "الأقواس تتباعد", "half": "نص قبة من كل طرف",
                            "butt": "دعامات ضخمة", "catch": "الدفّة تنزل للأرض", "crush": "ثقيلة مرة",
                            "dark": "ظلمة تحت", "ribs": "أربعين ضلع", "wins": "أربعين شباك", "quake": "زلزال!",
                            "later": "بعد واحد وعشرين سنة", "steep": "أعلى وأحدّ", "less": "تدف أقل",
                            "mortar": "مونة سماكتها قد الطوبة", "bends": "تنثني وما تنكسر", "gold": "ذهب",
                            "hang": "كأنها معلّقة في السما", "h": "55 m", "crack": "طاخ!"}}}
    COVER_T = ("closer", 0.55)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "float": ("hook", "FLOAT", 0.12), "brick": ("hook", "BRICK", 0.18), "thirty": ("hook", "THIRTY", 0.3),
            "wide": ("hook", "WIDE", 0.42), "ring": ("hook", "RING", 0.52), "light": ("hook", "LIGHT", 0.6),
            "congrats": ("hook", "CONGRATS", 0.66), "hagia": ("hook", "HAGIA", 0.85),
            "dome1": ("break1", "DOME", 0.1), "round": ("break1", "ROUND", 0.22), "walls": ("break1", "WALLS", 0.3),
            "emperor": ("break1", "EMPEROR", 0.5), "square": ("break1", "SQUARE", 0.78), "hall1": ("break1", "HALL", 0.88),
            "raise": ("fix1", "RAISE", 0.08), "arches": ("fix1", "ARCHES", 0.2), "fill": ("fix1", "FILL", 0.3),
            "corners": ("fix1", "CORNERS", 0.38), "triangles": ("fix1", "TRIANGLES", 0.6), "square2": ("fix1", "SQUARE", 0.78),
            "circle": ("fix1", "CIRCLE", 0.92),
            "heavy": ("break2", "HEAVY", 0.2), "pushes": ("break2", "PUSHES", 0.35), "outward": ("break2", "OUTWARD", 0.45),
            "arches2": ("break2", "ARCHES", 0.7), "spread": ("break2", "SPREAD", 0.9),
            "half": ("fix2", "HALF", 0.08), "ends": ("fix2", "ENDS", 0.35), "butt": ("fix2", "BUTTRESSES", 0.5),
            "sides": ("fix2", "SIDES", 0.75), "push2": ("fix2", "PUSH", 0.92),
            "solid": ("break3", "SOLID", 0.12), "crush": ("break3", "CRUSH", 0.35), "hall3": ("break3", "HALL", 0.6),
            "dark": ("break3", "DARK", 0.9),
            "forty": ("fix3", "FORTY", 0.15), "ribs": ("fix3", "RIBS", 0.35), "windows": ("fix3", "WINDOWS", 0.6),
            "base": ("fix3", "BASE", 0.9),
            "quake": ("break4", "EARTHQUAKE", 0.15), "twenty": ("break4", "TWENTY", 0.4), "first": ("break4", "FIRST", 0.65),
            "crash": ("break4", "CRASHING", 0.85),
            "rebuilt": ("fix4", "REBUILT", 0.08), "steeper": ("fix4", "STEEPER", 0.15), "less": ("fix4", "LESS", 0.4),
            "mortar": ("fix4", "MORTAR", 0.5), "thick": ("fix4", "THICK", 0.58), "bends": ("fix4", "BENDS", 0.82),
            "breaking": ("fix4", "BREAKING", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "gold": ("reveal", "GOLD", 0.15), "sun": ("reveal", "SUN", 0.3), "pour": ("reveal", "POUR", 0.38),
            "floor": ("reveal", "FLOOR", 0.55), "hang": ("reveal", "HANG", 0.85), "sky": ("reveal", "SKY", 0.95),
            "s1": ("stat", "FIFTY", 0.05), "s2": ("stat", "SIX", 0.55), "s3": ("stat", "FIFTEEN", 0.82),
            "cong2": ("closer", "CONGRATS", 0.16),
            "survived": ("tag", "SURVIVED", 0.1), "quakes": ("tag", "EARTHQUAKES", 0.35), "phone": ("tag", "PHONE", 0.6),
            "cracked": ("tag", "CRACKED", 0.7), "falling": ("tag", "FALLING", 0.78), "couch": ("tag", "COUCH", 0.92)})
        T["slip"] = T["phone"] - 0.1
        T["smash"] = min(max(T["cracked"], T["falling"]) + 0.25, T["slip"] + 0.9)
        T["morph"] = min(T["emperor"], T["square"]) - 0.1
        T["fallt"] = T["crash"] - 0.3
        # ---- sets
        self.cut(s("break1") - 0.12, "pend", 1)
        self.cut(s("break2") - 0.12, "frame", -1)
        self.cut(s("break3") - 0.12, "hall", 1)
        self.cut(s("break4") - 0.12, "frame", -1)
        self.cut(s("reveal") - 0.12, "hall", 1)
        self.cut(s("stat") - 0.12, "city", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- hall camera (hook, break3/fix3, reveal)
        cm = Camera(0, -640, 1.4)
        cm.key(0.1, 0, -600, 1.3, max(0.5, T["ring"] - 0.4))
        cm.key(T["ring"], 0, -330, 0.9, 1.3)
        cm.key(T["hagia"], 0, -300, 0.95, 1.0)
        cm.key(s("break3") - 0.12, 0, -600, 1.2, 0.0).key(T["hall3"] - 0.2, 0, -330, 0.95, 0.9)
        cm.key(s("fix3") - 0.12, 0, -560, 1.18, 0.0).key(T["windows"], 0, -520, 1.1, 1.2)
        cm.key(s("reveal") - 0.12, 0, -600, 1.25, 0.0).key(T["floor"] - 0.3, 0, -300, 0.95, 1.0)
        cm.key(T["hang"], 0, -330, 0.9, 1.2)
        self.cam = cm
        ck = Camera(0, -440, 0.7)
        ck.key(s("stat") - 0.12, 0, -440, 0.7, 0.0).key(s("stat"), 0, -450, 0.73, 3.0)
        ck.key(s("closer") - 0.2, 0, -500, 0.84, 1.0).key(s("closer") + 0.9, 0, -505, 0.86, 4.0)
        self.ccam = ck
        self.spans = [(T["hall1"], T["circle"] + 0.3), (T["spread"], T["push2"] + 0.3), (T["dark"], T["base"] + 0.3),
                      (T["crash"], T["breaking"] + 0.3)]
        self.shakes = [(T["congrats"], 0.35, 8), (T["square"] + 0.2, 0.3, 6), (T["spread"], 0.4, 7), (T["crush"], 0.4, 8),
                       (T["quake"], 1.4, 14), (T["fallt"] + 0.4, 0.5, 12), (s("closer") + 0.2, 0.35, 9), (T["smash"], 0.35, 10)]

    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    # ------------------------------------------------------------------ set: hall
    def hall_state(self, t):
        T, s = self.T, self.tl.s
        st = dict(wins=1.0, ribs=1.0, gold=0.0, light=1.0, solid=0.0, cracks=0.0, lift=0.0, people=1.0)
        if t < s("break1"):                                                  # hook: the floating dome
            st["light"] = lerp(0.75, 1.15, prog(t, T["ring"] - 0.3, T["light"] + 0.3)) - 0.15 * prog(t, T["light"] + 0.3, T["hagia"])
            st["lift"] = 6 + 4 * math.sin(t * 2.2)
        elif t < s("fix3") - 0.12:                                           # break3: solid, heavy, dark
            st.update(ribs=0.0, wins=0.0, solid=1.0, light=0.0)
            st["cracks"] = prog(t, T["crush"] - 0.1, T["crush"] + 0.8)
        elif t < s("reveal") - 0.12:                                         # fix3: ribs, then windows and light
            st["solid"] = 1 - prog(t, T["forty"] - 0.2, T["ribs"] + 0.3)
            st["ribs"] = prog(t, T["forty"] - 0.2, T["ribs"] + 0.5)
            st["wins"] = prog(t, T["windows"] - 0.4, T["base"] + 0.2)
            st["light"] = prog(t, T["windows"] - 0.2, T["base"] + 0.4)
        else:                                                                # reveal: gold, sun, floating
            st["gold"] = prog(t, T["gold"] - 0.2, T["sun"] + 0.4)
            st["light"] = lerp(0.8, 1.25, prog(t, T["sun"] - 0.2, T["pour"] + 0.4))
            st["lift"] = 14 * e_io(prog(t, T["hang"] - 0.5, T["hang"] + 0.6)) + 3 * math.sin(t * 2.2)
        return st

    def draw_hall(self, c, t):
        cam = self.cam.at(t)
        st = self.hall_state(t)
        cx, cy, z = cam
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=(0 - cy) * z + H / 2)
        v2.stars(c, W, H, t, 0.6)
        self.view(c, cam)
        hall(c, t, **st)
        dk = 0.0
        if self.tl.s("break3") - 0.12 <= t < self.tl.s("fix3") - 0.12:
            dk = prog(t, self.T["hall3"] - 0.3, self.T["dark"])
        if dk > 0:
            add_glow(c, -60, -24, 60, "#FFB45C", 0.8 * dk)                   # one small lamp in the dark
        c.restore()
        if dk > 0:
            c.drawRect(R(0, 0, W, H), P("#02030A", 0.5 * dk))
        self.ui["cam"] = cam

    def ui_hall(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, -330, 0.9))
        if tw < s("break1") - 0.12:
            k = self.span(T["thirty"] - 0.15, T["ring"])
            if k > 0:                                                        # the dimension across the dome
                xa, ya = self.at(cam, -RD, Y_WIN + 30)
                xb, yb = self.at(cam, RD, Y_WIN + 30)
                c.drawLine(xa, ya, xb, yb, P(HILITE, k, stroke=5))
                for xx in (xa, xb):
                    c.drawLine(xx, ya - 18, xx, ya + 18, P(HILITE, k, stroke=5))
                v2.chip(c, (xa + xb) / 2, ya + 70, self.L["wide"], k, accent=HILITE, size=40)
            self.chip(540, 300, "ring", T["ring"] - 0.1, T["congrats"] - 0.05, accent="#FFD58A", size=42)
            self.chip(540, 300, "name", T["hagia"] - 0.15, s("break1") + 0.1, accent=HILITE, size=48)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "crush", T["solid"] - 0.1, T["hall3"] - 0.15, accent=WARN, size=44)
            self.chip(540, 300, "dark", T["hall3"] - 0.15, s("fix3") - 0.15, accent="#94A3B8", size=42)
            self.badge("alert", T["dark"] + 0.05, s("fix3") - 0.2, x=920, y=420)
            self.red(T["crush"] + 0.05, 1.2)
            return
        if tw < s("reveal") - 0.12:
            self.chip(540, 300, "ribs", T["forty"] - 0.1, T["windows"] - 0.15, accent=HILITE, size=44)
            self.chip(540, 300, "wins", T["windows"] - 0.15, s("break4") - 0.15, accent="#FFD58A", size=44)
            self.badge("check", T["base"] + 0.05, s("break4") - 0.15, x=920, y=420)
            return
        self.chip(540, 300, "gold", T["gold"] - 0.1, T["hang"] - 0.2, accent="#FACC15", size=46)
        self.chip(540, 300, "hang", T["hang"] - 0.2, s("stat") - 0.15, accent="#FFE3A0", size=38)

    # ------------------------------------------------------------------ set: pend (3D)
    def draw_pend(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0E1A4A", "#2B3A78", "#5A4E86"])
        v2.stars(c, W, H, t, 0.5)
        z = lerp(1.1, 1.2, prog(t, s("break1"), s("break2")))
        o = (540, 1110, z)
        gp = poly3([(-420, 0, -420), (420, 0, -420), (420, 0, 420), (-420, 0, 420)], o)
        c.drawPath(gp, P("#3A3550"))
        c.drawPath(gp, P("#5A5478", stroke=3))
        fixed = t >= s("fix1") - 0.12
        hr = H0 + A3
        if not fixed:
            rk = 1 - prog(t, T["morph"], T["morph"] + 0.5)
            if rk > 0:                                                       # the round drum with its dome
                cxb, cyb = p3(0, 0, 0, o)
                cxt, cyt = p3(0, hr, 0, o)
                rx, ry = A3 * z, A3 * z * math.sin(PITCH)
                dr = skia.Path()
                dr.moveTo(cxb - rx, cyb)
                dr.arcTo(R(cxb - rx, cyb - ry, 2 * rx, 2 * ry), 180, -180, False)
                dr.lineTo(cxt + rx, cyt)
                dr.arcTo(R(cxt - rx, cyt - ry, 2 * rx, 2 * ry), 0, 180, False)
                dr.close()
                c.drawPath(dr, lin_paint(cxb - rx, 0, cxb + rx, 0, [BRICK_D, "#C98A6A", BRICK, BRICK_D], [0, 0.35, 0.6, 1], a=rk))
                c.drawOval(R(cxt - rx, cyt - ry, 2 * rx, 2 * ry), P("#C98A6A", rk))
                dome3(c, o, a=rk)
            sk = prog(t, T["morph"], T["morph"] + 0.5)
            if sk > 0:                                                       # a square hall: four walls
                for pts, col in (([(A3, 0, -A3), (A3, 0, A3), (A3, hr, A3), (A3, hr, -A3)], BRICK),
                                 ([(-A3, 0, A3), (A3, 0, A3), (A3, hr, A3), (-A3, hr, A3)], BRICK_D),
                                 ([(-A3, 0, -A3), (-A3, 0, A3), (-A3, hr, A3), (-A3, hr, -A3)], BRICK_D),
                                 ([(-A3, 0, -A3), (A3, 0, -A3), (A3, hr, -A3), (-A3, hr, -A3)], BRICK)):
                    c.drawPath(poly3(pts, o), P(col, sk))
                c.drawPath(poly3([(-A3, hr, -A3), (A3, hr, -A3), (A3, hr, A3), (-A3, hr, A3)], o), P("#3A2A22", sk))
                gk = prog(t, T["square"], T["square"] + 0.4)
                for sx_, sz_ in ((1, 1), (-1, 1), (1, -1), (-1, -1)):        # the corners the dome can't cover
                    pts = [(sx_ * A3, hr, sz_ * A3)]
                    a0 = math.atan2(0, sx_)
                    a1 = math.atan2(sz_, 0)
                    for i in range(13):
                        an = lerp(a0, a1, i / 12.0)
                        pts.append((A3 * math.cos(an), hr, A3 * math.sin(an)))
                    c.drawPath(poly3(pts, o), P(WARN, 0.75 * gk * sk))
                ring3(c, o, "#FFD58A", a=sk, w=5)
                dome3(c, o, drop=lerp(0, 60, gk) + 6 * math.sin(t * 3) * gk, a=sk)
            ek = prog(t, T["emperor"] - 0.3, T["emperor"])
            if ek > 0:
                ex, ey = p3(-A3 - 120, 0, -A3 - 60, o)
                emperor(c, ex, ey, 150, t, a=ek)
            self.ui["o"] = o
            return
        pk = prog(t, T["raise"] - 0.2, T["arches"] + 0.2)                   # piers rise, arches spring between them
        ak = prog(t, T["arches"] - 0.1, T["arches"] + 0.7)
        fk = prog(t, T["fill"] - 0.1, T["triangles"] + 0.4)
        ck = prog(t, T["circle"] - 0.2, T["circle"] + 0.4)
        dk = prog(t, T["circle"] + 0.1, T["circle"] + 0.9)
        h = H0 * e_out(pk)
        pier3(c, 1, 1, h, o)
        pend3(c, 1, 1, fk, o, col="#9A5A40")
        arch3(c, "x", 1, o, k=ak)
        arch3(c, "z", 1, o, k=ak)
        pier3(c, 1, -1, h, o)
        pier3(c, -1, 1, h, o)
        pend3(c, 1, -1, fk, o, col="#B86E4C")
        pend3(c, -1, 1, fk, o, col="#A8634A")
        if ck > 0:
            ring3(c, o, GOOD, a=ck, w=8)
        if dk > 0:
            dome3(c, o, drop=lerp(240, 0, e_out(dk)), a=dk)
        arch3(c, "x", -1, o, k=ak)
        arch3(c, "z", -1, o, k=ak)
        pend3(c, -1, -1, fk, o, col="#C9774E")
        pier3(c, -1, -1, h, o)
        if ck > 0 and dk < 1:
            ring3(c, o, GOOD, a=ck * (1 - dk), w=8)
        ex, ey = p3(-A3 - 120, 0, -A3 - 60, o)
        emperor(c, ex, ey, 150, t, a=1.0 - prog(t, s("fix1"), s("fix1") + 0.4))
        self.ui["o"] = o

    def ui_pend(self, c, t, tw):
        T, s = self.T, self.tl.s
        o = self.ui.get("o", (540, 1110, 1.1))
        if tw < s("fix1") - 0.12:
            self.chip(540, 290, "round", T["round"] - 0.2, T["morph"], accent="#FDBA74", size=40)
            self.chip(540, 290, "square", T["morph"], T["square"] + 0.3, accent=HILITE, size=40)
            self.chip(540, 290, "gap", T["square"] + 0.3, s("fix1") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["hall1"], s("fix1") - 0.2, x=920, y=430)
            self.red(T["square"] + 0.2, 1.2)
            return
        self.chip(540, 290, "arches", T["raise"] - 0.1, T["fill"] - 0.1, accent=HILITE, size=44)
        px, py = p3(-A3, H0 + A3 * 0.35, -A3, o)
        self.label(px, py, 300, 1180, "pend", T["fill"] - 0.1, T["circle"] - 0.2, "#FDBA74", size=36)
        self.chip(540, 290, "circle", T["circle"] - 0.2, s("break2") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["circle"] + 0.1, s("break2") - 0.15, x=920, y=430)

    # ------------------------------------------------------------------ set: frame (break2/fix2, break4/fix4)
    def draw_frame(self, c, t):
        T, s = self.T, self.tl.s
        quake = t >= s("break4") - 0.12
        cam = (0, -250, 0.8)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy)
        v2.stars(c, W, H, t, 0.7)
        sx_ = 0.0
        if quake and t < s("fix4") - 0.12:
            sx_ = math.sin(t * 40) * 10 * prog(t, T["quake"] - 0.2, T["quake"]) * (1 - prog(t, T["crash"] + 0.6, T["crash"] + 1.2))
        self.view(c, cam)
        c.translate(sx_, 0)
        c.drawRect(R(-1500, 0, 3000, 1200), lin_paint(0, 0, 0, 500, ["#3A3350", "#1A1730"]))
        if quake and t < s("fix4") - 0.12:
            for k in range(3):                                               # waves along the ground
                q = (t * 1.4 + k / 3.0) % 1.0
                c.drawArc(R(-200 - 900 * q, -60 * q + 10, 400 + 1800 * q, 120 * q + 20), 0, 180, False,
                          P("#F87171", 0.6 * (1 - q) * prog(t, T["quake"] - 0.2, T["quake"]), stroke=6))
        if not quake:
            fixed = t >= s("fix2") - 0.12
            lean = 0.0 if fixed else 4.0 * e_io(prog(t, T["arches2"] - 0.3, T["spread"] + 0.4))
            if fixed:
                lean = 4.0 * (1 - e_io(prog(t, T["half"] - 0.2, T["ends"] + 0.4)))
            half = prog(t, T["half"] - 0.3, T["ends"] + 0.3) if fixed else 0.0
            butt = prog(t, T["butt"] - 0.3, T["sides"]) if fixed else 0.0
            cracks = prog(t, T["spread"] - 0.4, T["spread"] + 0.3) * (1 - prog(t, T["half"], T["ends"])) if t >= s("break2") else 0.0
            frame(c, t, lean=lean, half=half, butt=butt, cracks=cracks)
            pk = prog(t, T["pushes"] - 0.3, T["outward"] + 0.2)
            for sd in (-1, 1):                                               # the push
                if not fixed:
                    arrow(c, sd * (RD - 20), Y_WIN + 20, sd * (RD + 190), Y_WIN + 50, WARN, a=pk, w=18, head=40)
                else:
                    gk = prog(t, T["push2"] - 0.5, T["push2"] + 0.3)
                    if gk > 0:
                        pts = [(sd * (RD + 20), Y_WIN + 30), (sd * (RD + 160), Y_RING + 120), (sd * (RD + 260), -300),
                               (sd * (RD + 300), -40)]
                        flow_pts(c, pts, GOOD, t, a=gk)
        else:
            fixed = t >= s("fix4") - 0.12
            if not fixed:
                fall = T["fallt"] if t >= T["fallt"] else None
                frame(c, t, rise=RISE_OLD, half=1.0, butt=1.0, fall=fall)
            else:
                nk = e_io(prog(t, T["rebuilt"] - 0.2, T["steeper"] + 0.5))
                frame(c, t, rise=lerp(RISE_OLD, RISE_NEW, nk), half=1.0, butt=1.0, ghost=prog(t, T["steeper"] - 0.2, T["steeper"] + 0.3))
                lk = prog(t, T["less"] - 0.4, T["less"] + 0.2) * (1 - prog(t, T["mortar"] - 0.3, T["mortar"]))
                for sd in (-1, 1):
                    arrow(c, sd * (RD - 20), Y_WIN + 20, sd * (RD + 70), Y_WIN + 60, GOOD, a=lk, w=14, head=30)
        c.restore()
        if quake and t >= T["mortar"] - 0.3 and t >= s("fix4") - 0.12:
            mk = prog(t, T["mortar"] - 0.3, T["mortar"] + 0.2)
            bk = prog(t, T["bends"] - 0.3, T["bends"] + 0.2)
            ax, ay = self.at(cam, 150, Y_WIN - RISE_NEW * 0.8)
            c.drawLine(ax, ay, 540 + 120, 1000 - 240, P("#F8FAFC", 0.9 * mk, stroke=5))
            c.drawCircle(ax, ay, 14, P("#F8FAFC", mk, stroke=5))
            bricks_mag(c, 540, 1000, 250 * e_back(mk), t, bend=bk, a=mk)
        self.ui["cam"] = cam

    def ui_frame(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "push", T["pushes"] - 0.15, T["arches2"] - 0.1, accent=WARN, size=44)
            self.chip(540, 300, "spread", T["arches2"] - 0.1, s("fix2") - 0.15, accent="#FDBA74", size=44)
            self.badge("alert", T["spread"] + 0.05, s("fix2") - 0.2, x=900, y=420)
            self.red(T["spread"] + 0.05, 1.2)
            return
        if tw < s("break3") - 0.12:
            self.chip(540, 300, "half", T["half"] - 0.1, T["butt"] - 0.1, accent="#93C5FD", size=44)
            self.chip(540, 300, "butt", T["butt"] - 0.1, T["push2"] - 0.4, accent="#FDBA74", size=44)
            self.chip(540, 300, "catch", T["push2"] - 0.4, s("break3") - 0.15, accent=GOOD, size=42)
            self.badge("check", T["push2"] + 0.1, s("break3") - 0.15, x=900, y=420)
            return
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "quake", T["quake"] - 0.1, T["twenty"] - 0.1, accent=WARN, size=48)
            self.chip(540, 300, "later", T["twenty"] - 0.1, s("fix4") - 0.15, accent="#FDBA74", size=42)
            self.badge("alert", T["crash"] + 0.05, s("fix4") - 0.2, x=900, y=420)
            self.red(T["crash"] + 0.05, 1.4)
            return
        self.chip(540, 300, "steep", T["rebuilt"] - 0.1, T["less"] - 0.2, accent=HILITE, size=44)
        self.chip(540, 300, "less", T["less"] - 0.2, T["mortar"] - 0.3, accent=GOOD, size=44)
        self.chip(540, 300, "mortar", T["mortar"] - 0.3, T["bends"] - 0.2, accent="#E7DCC3", size=34)
        self.chip(540, 300, "bends", T["bends"] - 0.2, s("cta") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["breaking"] + 0.05, s("cta") - 0.15, x=900, y=420)

    # ------------------------------------------------------------------ set: city (stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.ccam.at(t)
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 120 * z)
        v2.stars(c, W, H, t, 0.8)
        v2.moon(c, 860, gy - 1040 * z, 46)
        self.view(c, cam)
        c.drawRect(R(-2000, -160, 4000, 160), lin_paint(0, -160, 0, 0, ["#1E3A6E", "#0E1F44"]))      # the Bosphorus
        for k in range(30):
            xx = -1800 + k * 130
            c.drawRect(R(xx, -150 + (k % 5) * 26, 60, 3), P("#F2C38A", 0.35))
        v2.ridge(c, -2000, 2000, -160, 110, "#1A2148", "#2A2E5E", seed=3, step=110, rough=0.6)
        rng = random.Random(8)
        for _ in range(70):
            add_glow(c, rng.uniform(-1900, 1900), rng.uniform(-230, -170), rng.uniform(4, 8), "#FFD98A", 0.7)
        c.drawRect(R(-2000, 0, 4000, 900), lin_paint(0, 0, 0, 400, ["#26304A", "#121628"]))
        exterior(c, t, lit=1.0, minarets=1.0)
        for x in (-860, -780, 780, 860):                                    # cypress trees
            c.drawOval(R(x - 26, -230, 52, 230), P("#16302A"))
        if s("stat") - 0.12 <= t < s("closer"):
            hk = self.span(T["s1"] - 0.1, s("closer"))
            if hk > 0:
                x = 700
                top = Y_WIN - RISE_NEW - 24
                c.drawLine(x, 0, x, lerp(0, top, e_out(hk)), P(HILITE, hk, stroke=8))
                c.drawLine(x - 24, top, x + 24, top, P(HILITE, hk, stroke=8))
                c.drawLine(x - 24, 0, x + 24, 0, P(HILITE, hk, stroke=8))
        c.restore()
        self.ui["cam"] = cam

    def ui_city(self, c, t, tw):
        pass

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#1E2340", "#2A2F55"])
        c.drawRect(R(0, 1120, W, H - 1120), lin_paint(0, 1120, 0, H, ["#3A2E2A", "#1A1412"]))
        c.save()                                                            # a poster of the building on the wall
        c.translate(540, 520)
        c.drawRect(R(-230, -170, 460, 340), P("#0E1A4A"))
        c.drawRect(R(-230, -170, 460, 340), P("#C9A27A", stroke=12))
        c.save()
        c.translate(0, 150)
        c.scale(0.28, 0.28)
        exterior(c, t, lit=1.0, minarets=1.0)
        c.restore()
        c.restore()
        couch_(c, 540, 1120, 1.25)
        slip = prog(t, T["slip"], T["smash"])
        person(c, 470, 990, 230, "#2563EB", t, pose="sit" if t < T["smash"] + 0.1 else "shrug", face=1, hat="none", hair="#1C1917")
        if slip <= 0:
            phone_dev(c, 580, 830, 150, t, content="cat", rot=-12)
        else:
            px = lerp(580, 730, slip)
            py = lerp(830, 1170, e_in(slip))
            rot = lerp(-12, 70, slip)
            phone_dev(c, px, py, 120, t, content="cat" if t < T["smash"] else "dark", rot=rot)
            if t >= T["smash"]:
                k = prog(t, T["smash"], T["smash"] + 0.2)
                c.save()
                c.translate(px, py)
                c.rotate(rot)
                rng = random.Random(3)
                for _ in range(9):                                           # the cracked screen
                    an = rng.uniform(0, math.tau)
                    L_ = rng.uniform(40, 90) * k
                    cp = skia.Path()
                    cp.moveTo(6, -10)
                    cp.lineTo(6 + math.cos(an) * L_ * 0.5 + rng.uniform(-8, 8), -10 + math.sin(an) * L_ * 0.5)
                    cp.lineTo(6 + math.cos(an) * L_, -10 + math.sin(an) * L_)
                    c.drawPath(cp, P("#F8FAFC", 0.9, stroke=2.5))
                c.restore()
        self.ui["ph"] = (lerp(580, 730, slip), lerp(830, 1170, e_in(slip)))

    def ui_tag(self, c, t, tw):
        T = self.T
        k = self.span(T["smash"], self.duration + 1)
        if k > 0:
            kk = e_back(clamp(k))
            c.save()
            c.translate(780, 900)
            c.scale(kk, kk)
            c.rotate(-8)
            word(c, self.L["crack"], 0, 0, 76, "#FDE047")
            c.restore()

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.62)
        v2.stars(c, W, H, t, 0.6)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.hiss(max(1.0, T["ring"]), 61), -20), (0.1, sfx.sparkle(1.0, 9, 62), -12),
              (T["thirty"], sfx.tick(), -10), (T["ring"], sfx.riser(0.9, 63), -14), (T["light"], sfx.sparkle(0.8, 11, 64), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8),
              (T["hagia"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["round"], sfx.pop(68), -10),
               (T["morph"], sfx.whirr(0.5, 200.0, 320.0, 69), -14), (T["emperor"], sfx.pop(70), -8),
               (T["square"] + 0.2, sfx.thud(0.4, 71), -8), (T["hall1"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 72), -4), (T["raise"], sfx.whirr(0.7, 150.0, 260.0, 73), -14),
               (T["arches"], sfx.thud(0.3, 74), -10), (T["arches"] + 0.3, sfx.thud(0.3, 75), -10),
               (T["fill"], sfx.hiss(0.9, 76), -16), (T["triangles"], sfx.tap(77), -10),
               (T["circle"], sfx.ding(), -8), (T["circle"] + 0.4, sfx.thud(0.4, 78), -8), (T["circle"] + 0.5, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["pushes"], sfx.creak(0.9), -10),
               (T["spread"], sfx.clank(300.0, 0.4, 80), -12), (T["spread"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 81), -4), (T["half"], sfx.whoosh(0.5, False, 82), -10),
               (T["ends"], sfx.thud(0.4, 83), -8), (T["butt"], sfx.whirr(0.8, 140.0, 220.0, 84), -14),
               (T["push2"], sfx.ding(), -8), (T["push2"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 85), -4), (T["solid"], sfx.thud(0.5, 86), -6),
               (T["crush"], sfx.creak(0.8), -8), (T["dark"], sfx.power_down(0.9, 87), -12), (T["dark"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 88), -4)]
        for k in range(6):
            ev.append((T["forty"] + k * 0.18, sfx.tap(89 + k), -14))
        ev += [(T["windows"], sfx.sparkle(0.9, 12, 95), -10), (T["base"] + 0.1, sfx.ding(), -8), (T["base"] + 0.3, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 96), -4), (T["quake"] - 0.2, rumble(2.4, 97), -4),
               (T["fallt"] + 0.3, boom(1.6, 98), -6), (T["crash"] + 0.2, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 99), -4), (T["rebuilt"], sfx.whirr(0.8, 180.0, 300.0, 100), -14),
               (T["less"], sfx.pop(101), -8), (T["mortar"] - 0.2, sfx.pop(102), -6), (T["bends"], sfx.creak(0.6), -14),
               (T["breaking"] + 0.1, sfx.ding(), -8), (T["breaking"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(103), 0), (T["follow"] - 0.15, sfx.pop(104), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 105), -6), (T["gold"], sfx.sparkle(1.2, 14, 106), -8),
               (T["sun"], sfx.riser(0.8, 107), -14), (T["hang"], sfx.chime(), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 108), -6), (T["s1"], sfx.pop(109), -3), (T["s2"], sfx.pop(110), -3),
               (T["s3"], sfx.pop(111), -3)]
        ev += [(T["cong2"], sfx.pop(112), -2), (T["cong2"], sfx.sparkle(1.0, 14, 113), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 114), -6), (T["slip"], sfx.whoosh(0.4, False, 115), -14),
               (T["smash"], crack_snd(0.5, 116), -4), (T["smash"], sfx.thud(0.3, 117), -8)]
        return ev


def flow_pts(c, pts, col, t, a=1.0):
    """Moving dashes along a polyline with an arrowhead at the end (the push running to the ground)."""
    if a <= 0:
        return
    p_ = skia.Path()
    p_.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        p_.quadTo(pts[i][0], pts[i][1], mx, my)
    p_.lineTo(*pts[-1])
    c.drawPath(p_, dash_paint(col, a, w=14, t=t, dash=30, gap=18))
    x0, y0 = pts[-2]
    x1, y1 = pts[-1]
    arrow(c, lerp(x0, x1, 0.7), lerp(y0, y1, 0.7), x1, y1 + 30, col, a=a, w=14, head=36)


NAME = "hagiasophia"
EPISODE = HagiaSophia
