"""Episode 67 - The Colosseum.  v2 look: the amphitheatre cut open across its short axis (the stepped seats full of
people, the outer wall with the velarium masts on top, the wooden arena floor with trapdoors and the two floors of
tunnels under it), and the whole ring seen from outside with its three tiers of arches, the attic and the awning.

Sets: section (hook: the crowd in the sun, sails slide out from the masts over them, then a trapdoor opens and a lion
rises on its lift; break1: the sun on the seats, a thermometer; fix1: 240 poles and sailcloth; break2: the wind fills
the sails like a kite and the poles bend; fix2: sailors from the navy haul the ropes down to stone posts outside;
break4: a lion walking in through the front door, the crowd yawns; fix4: the tunnels, men at the winches, a cage
rising to a trapdoor), ring (hook end, stat, closer: the ring of arches under its awning at golden hour, then at night),
gates (break3: everybody at one arch, stuck; fix3: eighty numbered arches, a ticket with its gate), ruin (reveal: the
ring today, one side fallen and the walls full of holes; a magnifier on an iron clamp being dug out), tag (a hot
parking lot from above: one tree, one shady spot, a car circling it).
World (section): 1 unit = about 0.2 m, the arena floor at y = 0, the outer wall at x = +-370..400, up to y = -330.
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of  # noqa: E402
from bigben import thermometer  # noqa: E402
from bridge import wind  # noqa: E402

STONE = ("#E7D3A8", "#D2B886", "#A8895C", "#6E5638")
SAND = "#E8C98A"
WOOD = "#8A5A2B"
CANVAS = ("#F5EBD7", "#C2410C")
CROWD = ("#B91C1C", "#1D4ED8", "#F5F5F4", "#A16207", "#15803D", "#7C3AED", "#FBBF24", "#0E7490")
WALL_X = 370.0
TOP = -330.0
MAST_TOP = -420.0


def steps():
    """The seat profile on the right side: (x, y) corners from the podium up to the outer wall."""
    pts = [(150.0, 0.0), (150.0, -34.0)]
    n = 14
    for i in range(n):
        x0 = 160 + i * (WALL_X - 160) / n
        y0 = -40 - i * 18.5
        pts += [(x0, y0), (x0 + (WALL_X - 160) / n, y0)]
    return pts


STEPS = steps()


def lion(c, x, y, s, t, walk=0.0, face=1, a=1.0, roar=0.0):
    """A cartoon lion standing on y (feet), facing right (face=1)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s * face, s)
    sw = math.sin(t * 8) * 6 * walk
    for lx, ph in ((-34, 0), (-18, 1), (22, 1), (38, 0)):
        c.drawLine(lx, -30, lx + (sw if ph else -sw), 0, P("#B45309", a, stroke=12))
    c.drawRRect(rr(-52, -62, 104, 40, 20), P("#D97706", a))
    c.drawPath(path_of([(-52, -50), (-80, -70 + math.sin(t * 3) * 6), (-88, -78 + math.sin(t * 3) * 6)]), P("#B45309", a, stroke=6))
    c.drawCircle(-88, -80 + math.sin(t * 3) * 6, 7, P("#7C2D12", a))
    c.drawCircle(52, -66, 34, P("#92400E", a))                       # mane
    c.drawCircle(58, -64, 22, P("#F59E0B", a))                       # face
    c.drawCircle(64, -70, 4, P("#1C1917", a))
    if roar > 0:
        c.drawOval(R(66, -58, 14, 10 + 8 * roar), P("#7F1D1D", a))
    else:
        c.drawCircle(76, -60, 5, P("#7C2D12", a))
    c.restore()


def crowd_on_steps(c, t, side=1, heat=0.0, cheer=0.0, fan=0.0, yawn=0.0, a=1.0, shade_k=0.0):
    """Little spectators on every tread (world), facing the arena."""
    rng = random.Random(3 if side > 0 else 5)
    for i in range(1, len(STEPS) - 1, 2):
        x0, y0 = STEPS[i + 1]
        x1 = STEPS[i + 2][0] if i + 2 < len(STEPS) else WALL_X
        n = 3
        for k in range(n):
            px = side * lerp(x0 + 6, x1 - 6, (k + 0.5) / n)
            col = rng.choice(CROWD)
            jump = abs(math.sin(t * 9 + k + i)) * 6 * cheer
            c.drawRRect(rr(px - 7, y0 - 22 - jump, 14, 20, 6), P(mix(col, "#3B2A1A", 0.35 * shade_k), a))
            skin = mix("#E8B48A", "#F87171", 0.6 * heat)
            c.drawCircle(px, y0 - 28 - jump, 7, P(mix(skin, "#6B4F3A", 0.35 * shade_k), a))
            if fan > 0 and (k + i) % 3 == 0:
                q = math.sin(t * 14 + i) * 0.6
                c.drawLine(px, y0 - 30, px - side * 14 * math.cos(q), y0 - 40 - 10 * math.sin(q), P("#F5F5F4", fan * a, stroke=5))
            if heat > 0 and (k + i) % 4 == 1:
                q = (t * 1.5 + k * 0.3 + i * 0.1) % 1.0
                c.drawCircle(px + 6, y0 - 30 + q * 14, 2.5, P("#7DD3FC", heat * a * (1 - q)))
            if yawn > 0 and (k + i) % 3 == 1:
                c.drawOval(R(px - 3, y0 - 28, 6, 6 * yawn), P("#1C1917", a))


def section(c, t, sails=0.0, wind_k=0.0, masts=1.0, heat=0.0, fan=0.0, cheer=0.0, yawn=0.0, ropes_out=0.0, posts=0.0,
            lift=0.0, trap=0.0, lion_k=1.0, under=1.0, winch=0.0, night=0.0, bend_k=0.0, sailors=0.0):
    """The amphitheatre cut across its short axis (world). sails 0..1 slides the canvas out from the masts; wind_k fills
    it upward; ropes_out shows the ropes down to the stone posts outside; lift 0..1 raises the cage to the floor; trap
    opens the trapdoor; under shows the tunnels; winch turns the capstans."""
    shade_k = 0.6 * sails * (1 - 0.6 * wind_k)
    # outside ground
    c.drawRect(R(-1400, 0, 2800, 900), lin_paint(0, 0, 0, 500, ["#6E5638", "#3B2C1C"]))
    # hypogeum (two floors of tunnels)
    if under > 0:
        c.drawRect(R(-150, 0, 300, 140), P("#2A1F16", under))
        c.drawRect(R(-150, 66, 300, 8), P("#5A4430", under))
        for x0 in (-150, 140):
            c.drawRect(R(x0, 0, 10, 140), P("#5A4430", under))
        for k, xx in enumerate((-90, 0, 90)):                             # shafts, cages and winches
            c.drawRect(R(xx - 18, 8, 36, 126), P("#1A120C", under))
            cy_ = lerp(128, 30, e_io(lift)) if k == 1 else 128
            c.drawRect(R(xx - 16, cy_ - 34, 32, 34), P(WOOD, under))
            for b in range(4):
                c.drawLine(xx - 12 + b * 8, cy_ - 32, xx - 12 + b * 8, cy_ - 2, P("#3B2A1A", under, stroke=2))
            if k == 1 and lion_k > 0 and lift < 0.98:
                lion(c, xx, cy_ - 4, 0.22, t, a=under * lion_k)
            wx = xx + (30 if k < 2 else -30)
            c.drawRect(R(wx - 5, 74, 10, 58), P("#6B4423", under))         # capstan drum
            q = t * 3 * winch
            for j in range(2):
                bx = math.cos(q + j * math.pi) * 20
                c.drawLine(wx - bx, 100, wx + bx, 100, P("#A16207", under, stroke=4))
                person(c, wx + bx * 0.9, 132, 26, "#7C2D12", t + j + k, pose="carry" if winch > 0 else "stand",
                       face=1 if bx > 0 else -1, a=under)
            c.drawLine(xx, 8, xx, cy_ - 34, P("#D6D3D1", under, stroke=1.5))
    # arena floor: planks under sand, with trapdoors
    c.drawRect(R(-150, -6, 300, 8), P(WOOD))
    c.drawRect(R(-150, -9, 300, 5), P(SAND))
    for xx in (-90, 0, 90):
        if xx == 0 and trap > 0:
            c.drawLine(xx - 18, -6, xx - 18 + 36 * math.cos(math.radians(80 * trap)), -6 - 36 * math.sin(math.radians(80 * trap)),
                       P("#6B4423", 1, stroke=5))
            c.drawRect(R(xx - 18, -8, 36, 10), P("#1A120C"))
        else:
            c.drawRect(R(xx - 18, -8, 36, 3), P("#B08A57"))
    if lion_k > 0 and lift >= 0.98:
        lion(c, 0, -9, 0.6, t, a=lion_k, roar=clamp((lift - 0.98) * 50))
    for side in (-1, 1):
        # substructure under the seats, vaulted corridors
        pts = [(side * x, y) for x, y in STEPS] + [(side * WALL_X, 0.0)]
        c.drawPath(path_of(pts, close=True), lin_paint(0, -300, 0, 0, [STONE[1], STONE[2]]))
        for k, (vx, vy) in enumerate(((230, -10), (300, -10), (300, -110))):
            c.drawRRect(rr(side * vx - 18, vy - 50, 36, 50, 16), P("#3B2C1C", 0.8))
        # treads catch light
        for i in range(1, len(STEPS) - 1, 2):
            (xa, ya), (xb, yb) = STEPS[i + 1], STEPS[min(i + 2, len(STEPS) - 1)]
            c.drawLine(side * xa, ya, side * xb, yb, P(STONE[0], 1, stroke=3))
        # podium wall
        c.drawRect(R(side * 150 - (4 if side > 0 else -4) - 4, -40, 8, 40), P("#F5F5F4"))
        c.drawRect(R(min(side * 150, side * 150 + side * 10) - 5, -40, 10, 6), P("#B91C1C"))
        crowd_on_steps(c, t, side, heat=heat, cheer=cheer, fan=fan, yawn=yawn, shade_k=shade_k)
        # the outer wall with its corridors
        x0 = WALL_X if side > 0 else -WALL_X - 30
        c.drawRect(R(x0, TOP, 30, -TOP), lin_paint(x0, 0, x0 + 30, 0, [STONE[1], STONE[0], STONE[2]]))
        for (ya, yb) in ((-100, -40), (-190, -130), (-275, -220)):
            c.drawRRect(rr(x0 + 6, ya, 18, yb - ya, 8), P("#3B2C1C"))
        c.drawRect(R(x0 - 4, TOP - 6, 38, 8), P(STONE[0]))
        # masts
        if masts > 0:
            mx = side * (WALL_X + 15)
            lean = side * 20 * bend_k * math.sin(t * 6) * wind_k
            c.drawLine(mx, TOP, mx + lean * masts, TOP + (MAST_TOP - TOP) * masts, P("#7C5A36", 1, stroke=6))
            top = (mx + lean * masts, TOP + (MAST_TOP - TOP) * masts)
            # rope from the mast top to the ring over the arena
            ring_x = side * 140
            ring_y = -360.0 - 30 * wind_k * math.sin(t * 5 + side)
            if sails > 0 or ropes_out > 0:
                c.drawLine(top[0], top[1], ring_x, ring_y, P("#E7E5E4", 0.8 * masts, stroke=2))
            if sails > 0:
                xe = lerp(top[0], ring_x, sails)
                ye = lerp(top[1], ring_y, sails)
                sag = 26 * (1 - 2.2 * wind_k) + wind_k * 18 * math.sin(t * 9 + side)
                p_ = skia.Path()
                p_.moveTo(top[0], top[1])
                p_.quadTo((top[0] + xe) / 2, (top[1] + ye) / 2 + sag, xe, ye)
                p_.lineTo(xe, ye + 12)
                p_.quadTo((top[0] + xe) / 2, (top[1] + ye) / 2 + sag + 14, top[0], top[1] + 14)
                p_.close()
                c.drawPath(p_, P(CANVAS[0], 0.95))
                for j in range(1, 4):
                    f = j / 4.0
                    sx_ = lerp(top[0], xe, f)
                    sy_ = lerp(top[1], ye, f) + sag * 4 * f * (1 - f)
                    c.drawLine(sx_, sy_, sx_, sy_ + 13, P(CANVAS[1], 0.9, stroke=10))
            if ropes_out > 0:                                               # ropes down to the stone posts
                px_ = side * 470
                c.drawLine(top[0], top[1], lerp(top[0], px_, ropes_out), lerp(top[1], -10, ropes_out), P("#E7E5E4", 0.9, stroke=2.5))
            if posts > 0:
                c.drawRRect(rr(side * 470 - 9, -34, 18, 34, 4), P("#E7E5E4", posts))
                c.drawRRect(rr(side * 470 - 9, -34, 18, 34, 4), P("#78716C", posts, stroke=2))
            if sailors > 0:
                for j in range(3):
                    sx_ = side * (430 + j * 22)
                    person(c, sx_, 0, 36, "#1E3A8A" if j % 2 else "#F8FAFC", t + j, pose="carry", face=-side,
                           hat="cap", a=sailors)
                    c.drawLine(sx_ - side * 8, -18, sx_ - side * 8, -16, P("#FFFFFF", sailors, stroke=2))
    if night > 0:
        c.drawRect(R(-1400, -1200, 2800, 2400), P("#0B1026", 0.45 * night))


def ellipse_pt(cx, cy, rx, ry, th):
    return cx + rx * math.cos(th), cy + ry * math.sin(th)


def ring(c, t, rx=430.0, ry=140.0, h=330.0, sails=1.0, crowd_k=1.0, night=0.0, holes=0.0, broken=0.0, nums=0.0, lit=0.0,
         jam=0.0, flow=0.0, warm=1.0):
    """The Colosseum from outside and a little above (world: the ellipse of its base centred on 0, 0).
    broken 0..1 drops the left part of the outer wall (the ring today); holes 0..1 the pockmarks; nums the gate
    numbers; jam / flow: people stuck at one arch, or streaming into all of them."""
    stone = [mix(col, "#2B2A45", 0.55 * night) for col in STONE]
    n = 72
    def wall_h(th):
        if broken <= 0:
            return h
        x = math.cos(th)
        if x > -0.05 or math.sin(th) < 0:
            return h
        return h * lerp(1.0, 0.42, broken * clamp((-x - 0.05) * 3))
    # back half of the wall (inner face, in shadow)
    back = [ellipse_pt(0, -h, rx, ry, math.pi + math.pi * i / n) for i in range(n + 1)]
    inner_back = [ellipse_pt(0, -h * 0.55, rx * 0.93, ry * 0.93, math.pi + math.pi * i / n) for i in range(n + 1)]
    c.drawPath(path_of(back + inner_back[::-1], close=True), P(stone[2]))
    # the bowl: seats going down to the arena
    for k in range(7):
        f = k / 7.0
        c.drawOval(R(-rx * (0.93 - 0.5 * f), -h * (0.55 - 0.35 * f) - ry * (0.93 - 0.5 * f), 2 * rx * (0.93 - 0.5 * f),
                     2 * ry * (0.93 - 0.5 * f)), P(mix(stone[1], stone[3], f * 0.6)))
        if crowd_k > 0 and k < 5:
            rng = random.Random(k)
            for i in range(46):
                th = math.pi + math.pi * (i + 0.5) / 46
                px, py = ellipse_pt(0, -h * (0.55 - 0.35 * f), rx * (0.9 - 0.5 * f), ry * (0.9 - 0.5 * f), th)
                c.drawCircle(px, py - 4, 4.5, P(rng.choice(CROWD), 0.9 * crowd_k))
    ax, ay = 0, -h * 0.2
    c.drawOval(R(-rx * 0.4, ay - ry * 0.4, rx * 0.8, ry * 0.8), P(mix(SAND, "#2B2A45", 0.5 * night)))
    # front half of the wall: outer face with three tiers of arches and the attic
    top_f = [(px, py - wall_h(th)) for (px, py), th in
             ((ellipse_pt(0, 0, rx, ry, math.pi * i / n), math.pi * i / n) for i in range(n + 1))]
    base_f = [ellipse_pt(0, 0, rx, ry, math.pi * i / n) for i in range(n + 1)]
    c.drawPath(path_of(base_f + top_f[::-1], close=True),
               lin_paint(-rx, 0, rx, 0, [stone[2], stone[0], stone[1], stone[2]], [0.0, 0.35, 0.7, 1.0]))
    tiers = ((0.02, 0.24), (0.27, 0.49), (0.52, 0.74))
    m = 40
    for i in range(m):
        th = math.pi * (i + 0.5) / m
        bx, by = ellipse_pt(0, 0, rx, ry, th)
        wk = math.sin(th)
        aw = 2 * math.pi * rx / 80 * wk * 0.55
        hh = wall_h(th)
        for (f0, f1) in tiers:
            y0, y1 = by - h * f0, by - h * f1
            if h * f1 > hh:
                continue
            ah = (y0 - y1) * 0.78
            c.drawRect(R(bx - aw / 2, y0 - ah + aw / 2, aw, ah - aw / 2), P("#2B2118"))
            c.drawCircle(bx, y0 - ah + aw / 2, aw / 2, P("#2B2118"))
            if lit > 0 and f0 > 0.2:
                c.drawRect(R(bx - aw / 2, y0 - ah + aw / 2, aw, ah - aw / 2), P("#FDBA74", 0.35 * lit))
        if hh >= h * 0.98:                                                  # attic windows every other bay
            if i % 2 == 0:
                c.drawRect(R(bx - aw * 0.25, by - h * 0.9, aw * 0.5, h * 0.06), P("#2B2118"))
            c.drawLine(bx, by - h, bx, by - h - 26, P("#7C5A36", 1, stroke=2.5))    # the poles of the awning
        if nums > 0 and 14 <= i <= 25:                                     # gate numbers over the ground arches
            text(c, ROMAN[i - 14], bx, by - h * 0.235, 11 * (0.4 + 0.6 * wk) * 1.6, "#3B2A1A", "Poppins-Black", a=nums)
        for (f0, f1) in tiers:                                              # half columns between the bays
            px_, py_ = ellipse_pt(0, 0, rx, ry, math.pi * i / m)
            if h * f1 <= wall_h(math.pi * i / m):
                c.drawLine(px_, py_ - h * f0, px_, py_ - h * f1, P(stone[0], 0.7, stroke=3 * (0.4 + 0.6 * wk)))
    for f in (0.25, 0.5, 0.75, 0.87):                                       # cornices
        pts = [(px, py - h * f) for (px, py), th in
               ((ellipse_pt(0, 0, rx, ry, math.pi * i / n), math.pi * i / n) for i in range(n + 1)) if h * f <= wall_h(th)]
        if len(pts) > 1:
            c.drawPath(path_of(pts), P(stone[0], 0.9, stroke=4))
    if holes > 0:                                                           # the holes left by the stolen iron clamps
        rng = random.Random(21)
        for _ in range(240):
            th = rng.uniform(0.15, math.pi - 0.15)
            f = rng.uniform(0.03, 0.97)
            if h * f > wall_h(th):
                continue
            px, py = ellipse_pt(0, 0, rx, ry, th)
            c.drawCircle(px, py - h * f, rng.uniform(2.0, 3.6) * (0.4 + 0.6 * math.sin(th)), P("#3B2A1A", 0.85 * holes))
    if sails > 0:                                                           # the awning from the rim to a ring inside
        k = 18
        for i in range(k):
            th0 = math.pi + math.pi * 2 * i / k
            th1 = math.pi + math.pi * 2 * (i + 1) / k
            a0 = ellipse_pt(0, -h - 26, rx, ry, th0)
            a1 = ellipse_pt(0, -h - 26, rx, ry, th1)
            b0 = ellipse_pt(0, -h - 26, rx * lerp(1.0, 0.42, sails), ry * lerp(1.0, 0.42, sails), th0)
            b1 = ellipse_pt(0, -h - 26, rx * lerp(1.0, 0.42, sails), ry * lerp(1.0, 0.42, sails), th1)
            if math.sin((th0 + th1) / 2) > 0.15:                            # skip the panels in front: keep the bowl visible
                continue
            col = CANVAS[0] if i % 2 else mix(CANVAS[0], CANVAS[1], 0.35)
            c.drawPath(path_of([a0, a1, b1, b0], close=True), P(mix(col, "#2B2A45", 0.5 * night), 0.92))
    # people at the ground arches
    if jam > 0:
        bx, by = ellipse_pt(0, 0, rx, ry, math.pi * 0.5)
        rng = random.Random(4)
        for i in range(70):
            px = bx + rng.gauss(0, 46) * (0.3 + 0.7 * jam)
            py = by + 10 + abs(rng.gauss(0, 26)) * jam
            c.drawCircle(px, py - 8, 6, P(rng.choice(CROWD), jam))
    if flow > 0:
        rng = random.Random(6)
        for i in range(90):
            gi = rng.randint(10, 29)
            th = math.pi * (gi + 0.5) / m
            bx, by = ellipse_pt(0, 0, rx, ry, th)
            q = (t * 0.6 + rng.random()) % 1.0
            px = bx + rng.uniform(-6, 6)
            py = by + 60 * (1 - q)
            c.drawCircle(px, py - 8, 5.5, P(rng.choice(CROWD), flow * min(1.0, (1 - q) * 3)))


ROMAN = ["XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX", "XXXI", "XXXII"]


def ticket(c, x, y, s, label, a=1.0):
    """A bone ticket (tessera) with its gate number (screen space)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(-8)
    c.scale(s, s)
    c.drawRRect(rr(-130, -70, 260, 140, 30), P("#000000", 0.35 * a, blur=16))
    c.drawRRect(rr(-130, -70, 260, 140, 30), P("#F5EBD7", a))
    c.drawRRect(rr(-118, -58, 236, 116, 22), P("#C2A878", a, stroke=4))
    text(c, label, 0, 26, 74, "#7C2D12", "Poppins-Black", a=a)
    c.restore()


def top_car(c, x, y, ang, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    c.drawRRect(rr(-26, -48, 52, 96, 14), P("#000000", 0.3 * a, blur=6))
    c.drawRRect(rr(-24, -46, 48, 92, 14), P(col, a))
    c.drawRRect(rr(-19, -26, 38, 22, 6), P("#1E293B", a))
    c.drawRRect(rr(-19, 18, 38, 14, 5), P("#1E293B", a))
    c.restore()


def tree_top(c, x, y, r, a=1.0):
    c.drawCircle(x + 40, y + 30, r * 1.1, P("#000000", 0.35 * a, blur=10))
    c.drawCircle(x, y, r, P("#15803D", a))
    for k in range(6):
        q = k * 1.05
        c.drawCircle(x + math.cos(q) * r * 0.5, y + math.sin(q) * r * 0.5, r * 0.45, P("#22C55E", 0.8 * a))


# ====================================================================================== the episode
class Colosseum(EpisodeV2):
    BUILD_NO = 67
    FIRST_SET = "section"
    CLEAR = "#1A1208"
    TITLE = {"en": "COLOSSEUM", "ar_sa": "الكولوسيوم"}
    EMPH = {"en": ["CONGRATS", "ROOF", "SAILS", "FIFTY", "THOUSAND", "LION", "FLOOR", "COLOSSEUM", "YOURSELF", "ROMAN",
                   "SUMMER", "BAKES", "SUN", "TWO", "HUNDRED", "FORTY", "WOODEN", "POLES", "SAILCLOTH", "SAIL", "WIND",
                   "KITE", "SAILORS", "NAVY", "ROPES", "STONE", "POSTS", "ARRIVE", "LEAVE", "EIGHTY", "ARCHES",
                   "NUMBER", "GATE", "TICKET", "SURPRISES", "STROLL", "FRONT", "DOOR", "TUNNELS", "SAND", "WINCHES",
                   "CAGES", "TRAPDOORS", "FOLLOW", "TAIPEI", "BALL", "HOLES", "WALLS", "IRON", "CLAMPS", "SEATS",
                   "GATES", "SHADED", "ROMANS", "CIRCLES", "PARKING", "SHADE"],
            "ar_sa": ["مبروك", "سقف", "أشرعة", "خمسين", "ألف", "أسد", "الأرض", "الكولوسيوم", "بيدك", "صيف", "روما",
                      "حر", "الشمس", "ميتين", "وأربعين", "صاري", "خشب", "قماش", "شراع", "ريح", "الطيارة", "بحّارة",
                      "الأسطول", "بحبال", "أعمدة", "حجر", "يدخلون", "ويطلعون", "ثمانين", "بوابة", "رقم", "وتذكرتك",
                      "مفاجآت", "والأسد", "الباب", "أنفاق", "الرمل", "رافعات", "الأقفاص", "فتحات", "تابعني", "الكورة",
                      "تايبيه", "الخروم", "جدرانه", "مشابك", "الحديد", "مقعد", "ظلّلوا", "موقف", "بظل"]}
    KEYS = {"ar_sa": {
        ("hook", "ROOF"): "سقف", ("hook", "SAILS"): "أشرعة", ("hook", "FIFTY"): "خمسين", ("hook", "LION"): "أسد",
        ("hook", "FLOOR"): "الأرض", ("hook", "CONGRATS"): "مبروك", ("hook", "COLOSSEUM"): "الكولوسيوم",
        ("break1", "SUMMER"): "صيف", ("break1", "BAKES"): "الشمس", ("break1", "DAY"): "اليوم",
        ("fix1", "TWO"): "ميتين", ("fix1", "POLES"): "صاري", ("fix1", "SAILCLOTH"): "قماش",
        ("break2", "SAIL"): "شراع", ("break2", "WIND"): "ريح", ("break2", "KITE"): "الطيارة",
        ("fix2", "SAILORS"): "بحارة", ("fix2", "NAVY"): "الأسطول", ("fix2", "ROPES"): "بحبال", ("fix2", "POSTS"): "أعمدة",
        ("break3", "FIFTY"): "خمسين", ("break3", "ARRIVE"): "يدخلون", ("break3", "LEAVE"): "ويطلعون",
        ("fix3", "EIGHTY"): "ثمانين", ("fix3", "NUMBER"): "رقم", ("fix3", "TICKET"): "وتذكرتك",
        ("break4", "SURPRISES"): "مفاجآت", ("break4", "LION"): "والأسد", ("break4", "DOOR"): "الباب",
        ("fix4", "TUNNELS"): "أنفاق", ("fix4", "WINCHES"): "رافعات", ("fix4", "CAGES"): "الأقفاص", ("fix4", "TRAPDOORS"): "فتحات",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "HOLES"): "الخروم", ("reveal", "CENTURIES"): "قرون", ("reveal", "IRON"): "مشابك",
        ("reveal", "STONES"): "حجارته",
        ("stat", "FIFTY"): "خمسين", ("stat", "EIGHTY"): "وثمانين", ("stat", "TWO"): "وميتين",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "SHADED"): "ظللوا", ("tag", "CIRCLES"): "تلف", ("tag", "PARKING"): "موقف", ("tag", "SHADE"): "بظل"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Taipei 101's giant ball"),
                   "stat": [("50,000", "SEATS"), ("80", "GATES"), ("240", "POLES")],
                   "L": {"sails": "A ROOF OF SAILS", "lion": "A LION OUT OF THE FLOOR", "name": "THE COLOSSEUM",
                         "sun": "SUN ALL DAY", "poles": "240 WOODEN POLES", "cloth": "SAILCLOTH", "kite": "A GIANT KITE",
                         "sailors": "NAVY SAILORS", "posts": "STONE POSTS", "jam": "50,000 AT ONE DOOR?",
                         "gates": "80 NUMBERED GATES", "ticket": "GATE ON YOUR TICKET", "boring": "BORING...",
                         "tunnels": "2 FLOORS OF TUNNELS", "winch": "WINCHES", "trap": "TRAPDOOR!", "holes": "ALL THESE HOLES?",
                         "clamps": "IRON CLAMPS, DUG OUT", "shade": "THE ONLY SHADE"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: كورة برج تايبيه"),
                      "stat": [("50,000", "مقعد"), ("80", "بوابة"), ("240", "صاري")],
                      "L": {"sails": "سقف من الأشرعة", "lion": "أسد من تحت الأرض", "name": "الكولوسيوم",
                            "sun": "شمس طول اليوم", "poles": "ميتين وأربعين صاري", "cloth": "قماش أشرعة",
                            "kite": "مثل الطيارة الورق", "sailors": "بحّارة الأسطول", "posts": "أعمدة حجر",
                            "jam": "خمسين ألف من باب واحد؟", "gates": "ثمانين بوابة بأرقام", "ticket": "بوابتك في تذكرتك",
                            "boring": "ممل...", "tunnels": "دورين أنفاق", "winch": "رافعات خشب", "trap": "فتحة!",
                            "holes": "وش هالخروم؟", "clamps": "مشابك حديد انقلعت", "shade": "الظل الوحيد"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "roof": ("hook", "ROOF", 0.08), "sails": ("hook", "SAILS", 0.15), "fifty": ("hook", "FIFTY", 0.25),
            "lion": ("hook", "LION", 0.45), "floor": ("hook", "FLOOR", 0.6), "congrats": ("hook", "CONGRATS", 0.75),
            "name": ("hook", "COLOSSEUM", 0.92),
            "summer": ("break1", "SUMMER", 0.3), "bakes": ("break1", "BAKES", 0.6), "day": ("break1", "DAY", 0.9),
            "two": ("fix1", "TWO", 0.2), "poles": ("fix1", "POLES", 0.55), "cloth": ("fix1", "SAILCLOTH", 0.8),
            "sail": ("break2", "SAIL", 0.2), "wind": ("break2", "WIND", 0.6), "kite": ("break2", "KITE", 0.9),
            "sailors": ("fix2", "SAILORS", 0.2), "navy": ("fix2", "NAVY", 0.4), "ropes": ("fix2", "ROPES", 0.65),
            "posts": ("fix2", "POSTS", 0.9),
            "fifty3": ("break3", "FIFTY", 0.1), "arrive": ("break3", "ARRIVE", 0.35), "leave": ("break3", "LEAVE", 0.8),
            "eighty": ("fix3", "EIGHTY", 0.2), "number": ("fix3", "NUMBER", 0.45), "ticket": ("fix3", "TICKET", 0.9),
            "surprises": ("break4", "SURPRISES", 0.3), "lion4": ("break4", "LION", 0.55), "door": ("break4", "DOOR", 0.9),
            "tunnels": ("fix4", "TUNNELS", 0.25), "winches": ("fix4", "WINCHES", 0.6), "cages": ("fix4", "CAGES", 0.75),
            "trap": ("fix4", "TRAPDOORS", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "holes": ("reveal", "HOLES", 0.25), "centuries": ("reveal", "CENTURIES", 0.5), "iron": ("reveal", "IRON", 0.75),
            "stones": ("reveal", "STONES", 0.95),
            "s1": ("stat", "FIFTY", 0.05), "s2": ("stat", "EIGHTY", 0.4), "s3": ("stat", "TWO", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_shaded": ("tag", "SHADED", 0.05), "t_circles": ("tag", "CIRCLES", 0.5), "t_parking": ("tag", "PARKING", 0.7),
            "t_shade": ("tag", "SHADE", 0.95)})
        if self.lang == "en":                                   # "SHADE" would match "shaded" first
            T["t_shade"] = self.w("tag", "SHADE", 0.95, nth=1)
        T["day1"] = max(T["day"], T["bakes"]) + 0.1
        T["kite1"] = max(T["kite"], T["wind"]) + 0.1
        T["leave1"] = max(T["leave"], T["arrive"]) + 0.1
        T["door1"] = max(T["door"], T["lion4"]) + 0.1
        T["cloth1"] = max(T["cloth"], T["poles"]) + 0.2
        T["posts1"] = max(T["posts"], T["ropes"]) + 0.2
        T["ticket1"] = max(T["ticket"], T["number"]) + 0.2
        T["trap1"] = max(T["trap"], T["cages"]) + 0.2
        # ---- sets
        self.cut(T["congrats"] - 0.15, "ring", 1)
        self.cut(s("break1") - 0.12, "section", -1)
        self.cut(s("break3") - 0.12, "gates", 1)
        self.cut(s("break4") - 0.12, "section", -1)
        self.cut(s("reveal") - 0.12, "ruin", 1)
        self.cut(s("stat") - 0.12, "ring", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- section camera
        cs = Camera(0, -150, 1.2)
        cs.key(0.05, 0, -152, 1.22, 0.4)
        cs.key(max(0.3, T["lion"] - 0.5), 0, -40, 2.3, 0.6)
        cs.key(s("break1") - 0.12, 250, -230, 2.0, 0.0)
        cs.key(s("fix1") - 0.12, 0, -170, 1.2, 0.0)
        cs.key(s("fix2") - 0.12, 340, -220, 1.5, 0.0)
        cs.key(s("break4") - 0.12, 0, -60, 2.2, 0.0)
        cs.key(s("fix4") - 0.12, 0, 40, 2.5, 0.0)
        cs.key(T["trap"] - 0.6, 0, -20, 2.3, 0.8)
        self.cam = cs
        # ---- ring camera
        cr = Camera(0, 60, 1.05)
        cr.key(T["congrats"] - 0.15, 0, 60, 1.05, 0.0).key(T["congrats"], 0, 40, 1.12, max(1.0, s("break1") - T["congrats"]))
        cr.key(s("stat") - 0.12, 0, 30, 1.1, 0.0)
        cr.key(s("closer") - 0.1, 0, 10, 1.15, 1.2).key(s("closer") + 1.1, 0, 0, 1.2, 3.0)
        self.camr = cr
        self.spans = [(T["day1"], T["cloth1"] + 0.3), (T["kite1"], T["posts1"] + 0.3), (T["leave1"], T["ticket1"] + 0.3),
                      (T["door1"], T["trap1"] + 0.3)]
        self.shakes = [(T["floor"], 0.4, 8), (T["congrats"], 0.35, 8), (T["day1"], 0.3, 6), (T["kite1"], 0.5, 8),
                       (T["leave1"], 0.3, 6), (T["door1"], 0.3, 6), (T["trap"], 0.4, 8), (s("closer") + 0.2, 0.35, 9)]

    def sky_day(self, c, gy=1180, night=0.0):
        vrect(c, 0, 0, W, H, [mix("#F59E0B", "#0B1026", night), mix("#FDBA74", "#1E1B4B", night), mix("#FDE68A", "#3B2A5E", night)],
              [0.0, 0.55, 1.0])

    # ------------------------------------------------------------------ set: section
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        self.sky_day(c)
        add_glow(c, 180, 330, 260, "#FFF7D6", 0.9)
        c.drawCircle(180, 330, 70, P("#FFF7D6"))
        hook = t < s("break1") - 0.12
        b1 = s("break1") - 0.12 <= t < s("fix1") - 0.12
        f1 = s("fix1") - 0.12 <= t < s("break2") - 0.12
        b2 = s("break2") - 0.12 <= t < s("fix2") - 0.12
        f2 = s("fix2") - 0.12 <= t < s("break3") - 0.12
        b4 = s("break4") - 0.12 <= t < s("fix4") - 0.12
        f4 = t >= s("fix4") - 0.12
        self.view(c, cam)
        if hook:
            sk = e_io(prog(t, T["roof"] - 0.2, T["fifty"] + 0.4))
            lk = prog(t, T["lion"] - 0.3, T["floor"] + 0.2)
            section(c, t, sails=sk, heat=0.6 * (1 - sk), cheer=lk, lift=lk, trap=prog(t, T["lion"] - 0.5, T["lion"] - 0.2),
                    winch=1.0, under=1.0)
        elif b1:
            section(c, t, sails=0.0, masts=0.0, heat=prog(t, T["summer"] - 0.3, T["bakes"]), fan=prog(t, T["bakes"] - 0.2, T["bakes"]),
                    under=0.0, lion_k=0.0)
        elif f1:
            mk = e_out(prog(t, T["two"] - 0.3, T["poles"]))
            section(c, t, masts=mk, sails=e_io(prog(t, T["cloth"] - 0.4, T["cloth1"] + 0.6)), heat=0.5, under=0.0, lion_k=0.0)
        elif b2:
            wk = prog(t, T["wind"] - 0.4, T["wind"])
            section(c, t, sails=1.0, wind_k=wk, bend_k=1.0, under=0.0, lion_k=0.0)
        elif f2:
            rk = prog(t, T["ropes"] - 0.3, T["posts1"])
            section(c, t, sails=1.0, wind_k=0.25 * (1 - rk), ropes_out=rk, posts=prog(t, T["ropes"] - 0.4, T["ropes"]),
                    sailors=prog(t, T["sailors"] - 0.3, T["sailors"]), under=0.0, lion_k=0.0)
        elif b4:
            section(c, t, sails=1.0, under=0.0, lion_k=0.0, yawn=prog(t, T["lion4"], T["door1"]))
            wk = prog(t, T["lion4"] - 0.4, T["door1"] + 0.6)
            lion(c, lerp(-140, -40, wk), -9, 0.55, t, walk=1.0)
        elif f4:
            lk = e_io(prog(t, T["cages"] - 0.2, T["trap"] + 0.1))
            section(c, t, sails=1.0, under=1.0, winch=prog(t, T["winches"] - 0.3, T["winches"]), lift=lk,
                    trap=prog(t, T["trap"] - 0.3, T["trap"]), cheer=prog(t, T["trap"], T["trap"] + 0.3))
        self.ui["mast"] = self.to_screen(cam, WALL_X + 15, MAST_TOP)
        self.ui["sail"] = self.to_screen(cam, 260, -390)
        self.ui["post"] = self.to_screen(cam, 470, -34)
        self.ui["tunnel"] = self.to_screen(cam, -120, 100)
        self.ui["winch"] = self.to_screen(cam, 30, 90)
        self.ui["trap"] = self.to_screen(cam, 0, -8)
        c.restore()
        if b1:
            hk = prog(t, T["bakes"] - 0.3, T["bakes"])
            thermometer(c, 940, 760, 1.5, lerp(0.3, 0.95, hk), True, a=hk)
            for k in range(5):                                             # heat shimmer
                q = (t * 0.6 + k * 0.2) % 1.0
                c.drawLine(200 + k * 160, 1100 - q * 500, 220 + k * 160, 1060 - q * 500, P("#FFFFFF", 0.25 * hk * (1 - q), stroke=4))
        if b2:
            wind(c, 0, 520, W, t, n=10, a=prog(t, T["wind"] - 0.4, T["wind"]), spread=200, seed=2, col="#FFFFFF")

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "sails", T["roof"] - 0.1, T["lion"] - 0.2, accent="#FDE68A", size=46)
            self.chip(540, 300, "lion", T["lion"] - 0.2, T["congrats"] + 0.2, accent=WARN, size=44)
            return
        if tw < s("fix1") - 0.12:
            self.chip(540, 300, "sun", T["bakes"] - 0.3, s("fix1") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["day1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["day1"], 1.2)
            return
        if tw < s("break2") - 0.12:
            mx, my = self.ui.get("mast", (900, 600))
            self.label(mx, my, 760, 520, "poles", T["two"] - 0.2, s("break2") - 0.2, accent="#FDE68A", size=40)
            self.chip(540, 300, "cloth", T["cloth"] - 0.3, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["cloth1"] + 0.1, s("break2") - 0.15, x=920, y=420)
            return
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "kite", T["kite"] - 0.4, s("fix2") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["kite1"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["kite1"], 1.2)
            return
        if tw < s("break3") - 0.12:
            self.chip(540, 300, "sailors", T["sailors"] - 0.2, T["ropes"] - 0.2, accent="#93C5FD", size=46)
            px, py = self.ui.get("post", (900, 1000))
            self.label(px, py, 640, 560, "posts", T["ropes"] - 0.2, s("break3") - 0.2, accent="#E7E5E4", size=40)
            self.badge("check", T["posts1"] + 0.1, s("break3") - 0.15, x=920, y=420)
            return
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "boring", T["lion4"] - 0.1, s("fix4") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["door1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["door1"], 1.2)
            return
        tx_, ty_ = self.ui.get("tunnel", (300, 1100))
        self.label(tx_, ty_, 300, 520, "tunnels", T["tunnels"] - 0.2, T["trap"] - 0.2, accent="#FDE68A", size=40)
        wx_, wy_ = self.ui.get("winch", (700, 1100))
        self.label(wx_, wy_, 800, 640, "winch", T["winches"] - 0.2, T["trap"] - 0.2, accent="#CBD5E1", size=40)
        self.chip(540, 300, "trap", T["trap"] - 0.2, s("cta") - 0.15, accent=HILITE, size=52)
        self.badge("check", T["trap1"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: ring (hook end, stat, closer)
    def draw_ring(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.camr.at(t)
        closer = t >= s("closer") - 0.1
        night = 0.8 * prog(t, s("closer") - 0.1, s("closer") + 0.9) if closer else 0.0
        self.sky_day(c, night=night)
        if night > 0:
            v2.stars(c, W, H, t, night)
        else:
            add_glow(c, 180, 380, 260, "#FFF7D6", 0.8)
        self.view(c, cam)
        c.drawRect(R(-1400, 120, 2800, 1400), lin_paint(0, 120, 0, 700, [mix("#9C7A4E", "#2A2238", night), mix("#5A4430", "#151226", night)]))
        c.drawOval(R(-560, 60, 1120, 240), P("#000000", 0.25))
        ring(c, t, sails=1.0, night=night, lit=night)
        c.restore()

    def ui_ring(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "name", T["name"] - 0.4, s("break1") + 0.1, accent=HILITE, size=52)

    # ------------------------------------------------------------------ set: gates (break3, fix3)
    def draw_gates(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        self.sky_day(c)
        cam = (0, 110, 2.1) if not fixed else (0, 100, 1.75)
        self.view(c, cam)
        c.drawRect(R(-1400, 120, 2800, 1400), lin_paint(0, 120, 0, 700, ["#9C7A4E", "#5A4430"]))
        if not fixed:
            ring(c, t, sails=1.0, jam=prog(t, T["fifty3"] - 0.3, T["leave1"] + 0.3))
        else:
            ring(c, t, sails=1.0, nums=prog(t, T["number"] - 0.3, T["number"]), flow=prog(t, T["eighty"] - 0.3, T["eighty"] + 0.3))
        c.restore()
        if fixed:
            ticket(c, 820, 1080, 1.0, "XXIV", a=prog(t, T["ticket"] - 0.3, T["ticket"]))

    def ui_gates(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 300, "jam", T["arrive"] - 0.3, s("fix3") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["leave1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["leave1"], 1.2)
            return
        self.chip(540, 300, "gates", T["eighty"] - 0.2, T["ticket"] - 0.3, accent="#FDE68A", size=46)
        self.chip(540, 300, "ticket", T["ticket"] - 0.3, s("break4") - 0.15, accent=GOOD, size=44)
        self.badge("check", T["ticket1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: ruin (reveal)
    def draw_ruin(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#7DD3FC", "#BAE6FD", "#E0F2FE"])
        cam = (0, 40, 1.15)
        self.view(c, cam)
        c.drawRect(R(-1400, 120, 2800, 1400), lin_paint(0, 120, 0, 700, ["#8A8A7A", "#5A5A4E"]))
        ring(c, t, sails=0.0, crowd_k=0.0, holes=prog(t, T["holes"] - 0.4, T["holes"]), broken=1.0)
        c.restore()
        mk = prog(t, T["iron"] - 0.4, T["iron"])
        if mk > 0:                                                           # magnifier: a clamp pried out of its hole
            x, y, r = 760, 1020, 190
            c.drawCircle(x, y, r, P("#D2B886", mk))
            c.drawLine(x - r, y - 20, x + r, y - 20, P("#A8895C", mk, stroke=6))
            c.drawRRect(rr(x - 70, y - 50, 140, 60, 10), P("#3B2A1A", mk))
            lift = e_out(prog(t, T["iron"], T["stones"] + 0.4))
            c.save()
            c.translate(x, y - 20 - lift * 90)
            c.rotate(-20 * lift)
            c.drawRRect(rr(-60, -14, 120, 28, 8), P("#57534E", mk))
            c.drawRect(R(-60, -14, 16, 50), P("#57534E", mk))
            c.drawRect(R(44, -14, 16, 50), P("#57534E", mk))
            c.restore()
            c.drawLine(x + 150, y - 260, x + 30, y - 40 - lift * 80, P("#78716C", mk, stroke=14))      # the pick
            c.drawCircle(x, y, r, P("#F8FAFC", mk, stroke=10))
            c.drawLine(x - r * 0.7, y + r * 0.7, x - r * 1.15, y + r * 1.15, P("#F8FAFC", mk, stroke=18))

    def ui_ruin(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "holes", T["holes"] - 0.3, T["iron"] - 0.4, accent="#FDE68A", size=46)
        self.chip(540, 300, "clamps", T["iron"] - 0.4, s("stat") - 0.15, accent=WARN, size=42)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        vrect(c, 0, 0, W, H, ["#57534E", "#44403C"])
        for k in range(7):                                                   # parking bays
            for row, y0 in enumerate((420, 1000)):
                x = 70 + k * 150
                c.drawLine(x, y0, x, y0 + 220, P("#F5F5F4", 0.8, stroke=6))
        rng = random.Random(3)
        free = 3
        for row, y0 in enumerate((420, 1000)):
            for k in range(6):
                if row == 0 and k == free:
                    continue
                top_car(c, 145 + k * 150, y0 + 110, 0 if row else 180, 1.25, rng.choice(("#F8FAFC", "#94A3B8", "#1F2937", "#B91C1C")))
        tree_top(c, 600, 300, 110)
        sk = prog(t, T["t_parking"], T["t_shade"] + 0.3)
        if sk < 1:
            top_car(c, 145 + free * 150, 530, 180, 1.25, "#F8FAFC")         # somebody already in the shade
        q = (t - T["t_shaded"]) * 1.3
        cx, cy = 540 + math.cos(q) * 300, 760 + math.sin(q) * 70
        top_car(c, cx, cy, math.degrees(q) + 180, 1.3, "#EF4444")
        c.drawRect(R(0, 0, W, H), P("#FFF7D6", 0.10 + 0.05 * math.sin(t * 3)))
        add_glow(c, 950, 120, 300, "#FFF7D6", 0.6)

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "shade", T["t_parking"] - 0.2, self.duration + 1, accent=HILITE, size=48)

    def whip_backdrop(self, c, t, m):
        self.sky_day(c)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, crowd_snd(max(1.5, T["congrats"]), 61), -20), (T["roof"], sfx.whoosh(0.8, True, 62), -10),
              (T["lion"], sfx.creak(0.8, 63), -10), (T["floor"], roar_snd(1.0, 64), -10),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 65), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 66), -8),
              (T["name"], sfx.beep(1500.0, 0.12), -10), (T["name"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 67), -4), (T["bakes"], sfx.sizzle(0.6, 68), -12),
               (T["day1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 69), -4), (T["poles"], sfx.thunk(70), -8),
               (T["cloth"], sfx.whoosh(0.6, True, 71), -10), (T["cloth1"], sfx.ding(), -8), (T["cloth1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 72), -4), (T["wind"], sfx.hiss(1.2, 73), -12),
               (T["kite1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 74), -4), (T["ropes"], sfx.creak(0.8, 75), -10),
               (T["posts1"], sfx.ding(), -8), (T["posts1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 76), -4), (T["arrive"], crowd_snd(1.2, 77), -14),
               (T["leave1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 78), -4), (T["number"], sfx.tap(79), -8),
               (T["ticket1"], sfx.ding(), -8), (T["ticket1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 80), -4), (T["door1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 81), -4), (T["winches"], sfx.creak(1.0, 82), -10),
               (T["trap"], sfx.thunk(83), -6), (T["trap"] + 0.1, roar_snd(1.0, 84), -8),
               (T["trap1"], sfx.ding(), -8), (T["trap1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(85), 0), (T["follow"] - 0.15, sfx.pop(86), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 87), -6), (T["iron"], sfx.clank(500.0, 0.5, 88), -10),
               (T["iron"] + 0.5, sfx.clank(420.0, 0.5, 89), -12)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 90), -6), (T["s1"], sfx.pop(91), -3), (T["s2"], sfx.pop(92), -3),
               (T["s3"], sfx.pop(93), -3)]
        ev += [(T["cong2"], sfx.pop(94), -2), (T["cong2"], sfx.sparkle(1.4, 18, 95), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 96), -6), (T["t_circles"], sfx.whirr(1.6, 120.0, 140.0, 97), -16),
               (T["t_shade"], sfx.buzz(0.42), -12)]
        return ev


def crowd_snd(d=1.5, seed=0):
    """A crowd murmur: band-passed noise with a slow swell."""
    rng = np.random.default_rng(seed)
    n = int(d * 48000)
    x = rng.standard_normal(n).astype(np.float32)
    x = sfx._bp(x, 300.0, 2400.0)
    env = np.sin(np.linspace(0, np.pi, n)) ** 0.6
    return sfx._norm(x * env, 0.5)


def roar_snd(d=1.0, seed=0):
    """A lion's roar, roughly: low growl noise with a falling pitch."""
    rng = np.random.default_rng(seed)
    n = int(d * 48000)
    tt = np.arange(n) / 48000.0
    f = 180 - 90 * tt / d
    tone = np.sin(2 * np.pi * np.cumsum(f) / 48000.0)
    x = tone * (0.6 + 0.4 * rng.standard_normal(n))
    x = sfx._lp(x.astype(np.float32), 900.0)
    env = np.minimum(1.0, tt / 0.08) * np.exp(-tt * 2.2)
    return sfx._norm(x * env, 0.8)


NAME = "colosseum"
EPISODE = Colosseum
