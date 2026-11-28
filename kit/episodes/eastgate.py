"""Episode 109 - The Eastgate Centre in Harare, Zimbabwe (Mick Pearce with Arup, 1996).  v2 look.

Sets: city (hook: close on a termite mound's knobbly top with hot air shimmering off it, out to the long concrete
office behind it whose roof carries a row of brick chimneys shimmering the same way; cta, stat; closer at dusk with the
windows lit), oven (break1: a glass tower glowing like an oven in the sun, then a termite mound with a question mark),
section (fix1: a cut through the building, thick concrete and small windows shaded by ledges; break2: by evening the
concrete glows with the day's heat; fix2: at night big fans blow cold air through the hollow floors and the concrete
turns blue; break3: next morning people and computers heat the rooms; fix3: small fans pull air through the cold floors
into the rooms; break4: warm air gathers under the ceilings; fix4: it rises up the shaft and out of the chimneys),
mound (reveal: a termite mound breathing in and out like a lung; it copied them wrong and still works), tag (two
colleagues fighting over the air-conditioner remote, both languages).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

CONC = ("#8C93A1", "#727A8A", "#59606F")              # mid-grey concrete (light grey blooms white)
ROOF = ("#A4443A", "#7E2F28")
BRICK = ("#9A5A42", "#6F3B2A")
VINE = ("#3E8E4F", "#2C6B3B")
EARTH = ("#B0683E", "#8A4C2C", "#653620")
HOT, COLD = "#F97316", "#38BDF8"
SKIN = ("#8D5A3B", "#6E4429", "#A9714B", "#C68E62")


def wavy(c, x, y, h, t, col="#FFE7C2", a=0.5, w=3, n=3, amp=6, seed=0):
    """Hot air shimmering upward from (x, y): a few wobbling lines."""
    if a <= 0:
        return
    for k in range(n):
        p = skia.Path()
        xx = x + (k - (n - 1) / 2) * 10
        for j in range(13):
            yy = y - j * h / 12
            dx = math.sin(j * 0.9 + t * 5 + k * 1.7 + seed) * amp * (j / 12)
            if j == 0:
                p.moveTo(xx + dx, yy)
            else:
                p.lineTo(xx + dx, yy)
        c.drawPath(p, P(col, a * (0.6 + 0.4 * math.sin(t * 3 + k)), stroke=w))


def arrow(c, x0, y0, x1, y1, col, a=1.0, w=10, head=22):
    if a <= 0:
        return
    c.drawLine(x0, y0, x1, y1, P(col, a, stroke=w))
    ang = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1), (x1 - head * math.cos(ang - 0.5), y1 - head * math.sin(ang - 0.5)),
           (x1 - head * math.cos(ang + 0.5), y1 - head * math.sin(ang + 0.5))]
    poly(c, pts, col, a)


def flow_arrows(c, pts, t, col, a=1.0, speed=0.6, n=4, w=9, head=18):
    """Arrows travelling along a polyline (screen space)."""
    if a <= 0 or len(pts) < 2:
        return
    segs, total = [], 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        segs.append((x0, y0, x1, y1, d))
        total += d

    def at(s):
        s = clamp(s, 0, total)
        for x0, y0, x1, y1, d in segs:
            if s <= d:
                u = s / d if d else 0
                return lerp(x0, x1, u), lerp(y0, y1, u)
            s -= d
        return pts[-1]
    for k in range(n):
        s = ((t * speed + k / n) % 1.0) * total
        xa, ya = at(s)
        xb, yb = at(s + 46)
        fade = math.sin(math.pi * (s / total))
        arrow(c, xa, ya, xb, yb, col, a * fade, w, head)


# ====================================================================================== the building from outside
BX0, BX1 = 110, 970                                    # the two blocks with the glass atrium between them
GAP0, GAP1 = 515, 565
FLOOR_TOP, FLOOR_H, NFL = 600, 56, 8                  # eight floors above the shops
SHOP_Y = FLOOR_TOP + FLOOR_H * NFL                    # 1048
GROUND_Y = 1160


def chimneys_x():
    xs = []
    for x0, x1 in ((BX0 + 20, GAP0 - 20), (GAP1 + 20, BX1 - 20)):
        n = 12
        for k in range(n):
            xs.append(lerp(x0, x1, (k + 0.5) / n))
    return xs


def facade(c, t, lit=0.0, shimmer=1.0, heat=0.0):
    """The Eastgate Centre's front: rough concrete floors with chunky ledges, small deep windows, vine columns, a red
    tiled roof with a row of brick chimneys. lit: windows lit (dusk)."""
    for x0, x1 in ((BX0, GAP0), (GAP1, BX1)):
        w = x1 - x0
        c.drawRect(R(x0, FLOOR_TOP, w, SHOP_Y - FLOOR_TOP), lin_paint(x0, 0, x1, 0, [CONC[0], CONC[1], CONC[2]]))
        tex(c, R(x0, FLOOR_TOP, w, SHOP_Y - FLOOR_TOP), "sand", 0.8, 0.25)
        for f in range(NFL):
            y = FLOOR_TOP + f * FLOOR_H
            for k in range(int(w // 44)):                  # small windows set deep in the wall
                wx = x0 + 14 + k * 44
                c.drawRect(R(wx, y + 20, 26, 26), P(mix("#1B2333", "#FFC56B", lit * (0.55 + 0.45 * ((k * 7 + f * 3) % 5 > 1))), 1))
            c.drawRect(R(x0 - 6, y + 10, w + 12, 9), P(shade(CONC[0], 0.12)))     # the ledge that shades them
            c.drawRect(R(x0 - 6, y + 19, w + 12, 4), P("#2B303B", 0.55))
        for k in range(1, int(w // 132) + 1):          # columns of steel rings with vines
            vx = x0 + k * 132 - 66
            c.drawRect(R(vx - 7, FLOOR_TOP, 14, SHOP_Y - FLOOR_TOP), P("#4B5260"))
            for j in range(18):
                yy = FLOOR_TOP + 10 + j * 25
                c.drawCircle(vx + math.sin(j * 1.3) * 6, yy, 9 + (j % 3) * 2, P(VINE[j % 2], 0.95))
        # the shops on the ground floor
        c.drawRect(R(x0, SHOP_Y, w, GROUND_Y - SHOP_Y), P("#3A3F4B"))
        for k in range(int(w // 96)):
            c.drawRect(R(x0 + 12 + k * 96, SHOP_Y + 22, 80, 82), P(mix("#1F2A3A", "#FFD08A", 0.35 + lit * 0.5)))
        # the red tiled roof
        p = skia.Path()
        p.moveTo(x0 - 12, FLOOR_TOP)
        p.lineTo(x0 + 26, FLOOR_TOP - 44)
        p.lineTo(x1 - 26, FLOOR_TOP - 44)
        p.lineTo(x1 + 12, FLOOR_TOP)
        p.close()
        c.drawPath(p, lin_paint(0, FLOOR_TOP - 44, 0, FLOOR_TOP, [ROOF[0], ROOF[1]]))
        for j in range(1, 4):
            c.drawLine(x0 + 6, FLOOR_TOP - j * 11, x1 - 6, FLOOR_TOP - j * 11, P("#6B241E", 0.6, stroke=2))
    # the glass atrium between the blocks
    c.drawRect(R(GAP0, FLOOR_TOP - 20, GAP1 - GAP0, GROUND_Y - FLOOR_TOP + 20), lin_paint(0, FLOOR_TOP, 0, GROUND_Y,
                                                                                         ["#7FB3D9", "#3E6E96"], a=0.75))
    for j in range(10):
        y = FLOOR_TOP + j * 56
        c.drawLine(GAP0, y, GAP1, y, P("#DDEBF7", 0.5, stroke=2))
    # brick chimneys along the ridge, warm air shimmering off them
    for i, x in enumerate(chimneys_x()):
        c.drawRect(R(x - 9, FLOOR_TOP - 98, 18, 56), lin_paint(x - 9, 0, x + 9, 0, [BRICK[0], BRICK[1]]))
        c.drawRect(R(x - 11, FLOOR_TOP - 104, 22, 8), P(BRICK[1]))
        if heat > 0:
            add_glow(c, x, FLOOR_TOP - 110, 22, HOT, 0.35 * heat)
        wavy(c, x, FLOOR_TOP - 108, 80, t, a=0.35 * shimmer, n=2, seed=i)


def termite_mound(c, x, y, h, t, a=1.0, shimmer=1.0, cut=0.0):
    """An African termite mound, base centre (x, y), height h: a knobbly earth spire with smaller turrets."""
    if a <= 0:
        return
    rng = random.Random(5)
    w = h * 0.42
    p = skia.Path()
    p.moveTo(x - w, y)
    pts = []
    for k in range(23):
        u = k / 22
        side = -1 if u < 0.5 else 1
        v = (0.5 - u) * 2 if u < 0.5 else (u - 0.5) * 2         # 1 at the base, 0 at the top
        hh = h * (1 - v) ** 0.9
        bump = rng.uniform(-0.06, 0.06) * h
        pts.append((x + side * w * v ** 0.75 + bump * 0.4, y - hh + abs(bump) * 0.3))
    for px, py in pts:
        p.lineTo(px, py)
    p.lineTo(x + w, y)
    p.close()
    c.drawPath(p, lin_paint(x - w, 0, x + w, 0, [EARTH[0], EARTH[1], EARTH[2]], a=a))
    tex(c, p.computeTightBounds(), "sand", 1.2, 0.4 * a)
    for tx, th, tw in ((-0.42, 0.45, 0.16), (0.36, 0.55, 0.14), (-0.18, 0.78, 0.1), (0.2, 0.72, 0.09)):
        q = skia.Path()
        bx = x + tx * w
        q.moveTo(bx - tw * h * 0.5, y - h * (th - 0.35))
        q.quadTo(bx - tw * h * 0.2, y - h * th - 10, bx, y - h * th - 18)
        q.quadTo(bx + tw * h * 0.2, y - h * th - 10, bx + tw * h * 0.5, y - h * (th - 0.35))
        q.close()
        c.drawPath(q, P(EARTH[1], a))
    for k in range(14):                                # little holes and ridges
        hx = x + rng.uniform(-0.5, 0.5) * w
        hy = y - rng.uniform(0.08, 0.7) * h
        c.drawOval(R(hx - 5, hy - 3, 10, 6), P(EARTH[2], 0.8 * a))
    if shimmer > 0:
        wavy(c, x, y - h - 12, h * 0.35, t, a=0.45 * shimmer * a, n=3, amp=8)


def city_sky(c, dusk=0.0):
    top = mix("#2F5E96", "#1B1F4A", dusk)
    mid = mix("#5C8FC4", "#6B3F6E", dusk)
    low = mix("#D49A62", "#E07B4A", dusk)
    vrect(c, 0, 0, W, H, [top, mid, low, low], [0.0, 0.45, 0.62, 1.0])
    if dusk < 1:
        add_glow(c, 860, 360, 170, "#FFE6A8", 0.55 * (1 - dusk))
        c.drawCircle(860, 360, 56, P("#FFF3D1", 1 - dusk))
    else:
        v2.stars(c, W, H, 0, 0.6)


def city_scene(c, t, dusk=0.0, lit=0.0, mound=1.0, mound_x=880, mound_h=420):
    city_sky(c, dusk)
    v2.ridge(c, -100, 1180, GROUND_Y - 120, 120, mix("#6B7F64", "#2D3150", dusk), mix("#56684F", "#232642", dusk),
             seed=3, step=120, rough=0.4)
    for k in range(9):                                 # jacaranda trees along the street
        tx = 60 + k * 125
        c.drawRect(R(tx - 5, GROUND_Y - 70, 10, 70), P("#4A3424"))
        c.drawCircle(tx, GROUND_Y - 84, 40, P(mix("#8B6BC9", "#4A3D7A", dusk), 0.95))
        c.drawCircle(tx + 24, GROUND_Y - 70, 28, P(mix("#9C7FD6", "#53458A", dusk), 0.9))
    facade(c, t, lit=lit)
    c.drawRect(R(0, GROUND_Y, W, 90), P(mix("#4B4F57", "#22252E", dusk)))
    termite_mound(c, mound_x, GROUND_Y + 60, mound_h, t, a=mound)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))


# ====================================================================================== oven (break1)
def oven(c, t, heat=1.0, q=0.0):
    vrect(c, 0, 0, W, H, ["#5B2A1A", "#B8572A", "#3A1A14"], [0.0, 0.55, 1.0])
    add_glow(c, 880, 300, 260, "#FFD27A", 0.8)
    c.drawCircle(880, 300, 80, P("#FFF0C2"))
    for k in range(12):                                # sun rays
        ang = k * math.pi / 6 + t * 0.2
        c.drawLine(880 + math.cos(ang) * 100, 300 + math.sin(ang) * 100, 880 + math.cos(ang) * 150, 300 + math.sin(ang) * 150,
                   P("#FFE29A", 0.6, stroke=8))
    # the glass tower
    x0, x1, y0, y1 = 300, 700, 380, 1180
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), lin_paint(x0, 0, x1, 0, ["#5B8DB8", "#9CC3E0", "#4A79A3"]))
    for f in range(16):
        y = y0 + f * 50
        c.drawLine(x0, y, x1, y, P("#2E4B66", 0.8, stroke=3))
    for k in range(1, 8):
        c.drawLine(x0 + k * 50, y0, x0 + k * 50, y1, P("#2E4B66", 0.6, stroke=2))
    c.drawRect(R(x0, y0, x1 - x0, y1 - y0), P(HOT, 0.45 * heat))                  # baking inside
    add_glow(c, 500, 780, 380, "#FF8A3D", 0.45 * heat)
    for k in range(6):                                 # heat waves off it
        wavy(c, x0 + 40 + k * 64, y0 - 10, 160, t, col="#FFD6A0", a=0.5 * heat, n=1, amp=10, seed=k)
    for k, (px, py) in enumerate(((380, 640), (520, 840), (620, 1040), (420, 1040))):    # workers fanning themselves
        person(c, px, py, 70, ["#2563EB", "#DB2777", "#F59E0B", "#10B981"][k], t + k, pose="shrug", skin=SKIN[k % 4],
               hair="#141414", wet=0.8 * heat)
    # a thermometer climbing
    c.drawRRect(rr(140, 640, 44, 400, 22), P("#E5E7EB"))
    c.drawRRect(rr(150, lerp(1010, 680, heat), 24, lerp(30, 350, heat), 12), P("#EF4444"))
    c.drawCircle(162, 1060, 38, P("#EF4444"))
    c.drawRect(R(0, GROUND_Y, W, 90), P("#3A2A22"))
    if q > 0:                                          # and a termite mound with a question mark
        c.save()
        c.drawCircle(810, 900, 190 * e_back(clamp(q)), P("#1C1410", 0.92))
        cp = skia.Path()
        cp.addCircle(810, 900, 180 * e_back(clamp(q)))
        c.clipPath(cp, skia.ClipOp.kIntersect, True)
        vrect(c, 620, 710, 380, 380, ["#D49A62", "#B8572A"])
        termite_mound(c, 810, 1060, 290, t, shimmer=1.0)
        c.restore()
        c.drawCircle(810, 900, 180 * e_back(clamp(q)), P("#FDE68A", q, stroke=10))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#2A1610", "#0B0E18"]))


# ====================================================================================== section (fix1 .. fix4)
SX0, SX1 = 150, 930                                    # the cut through one block
SY_ROOF = 500
SFL = 6
SFH = 112
SY0 = SY_ROOF + 30                                     # top of the first floor slab
SLAB = 30


def section(c, t, tod=0.0, wall_heat=0.0, slab_heat=0.0, sun=1.0, night=0.0, fans=0.0, small_fans=0.0, people=0.0,
            gather=0.0, rise=0.0, warmup=0.0):
    """A cut through the building. tod: 0 day, 1 evening, 2 night, 3 morning. Heat 0..1 tints the concrete."""
    skyc = [("#3E73AE", "#88B7DE"), ("#5B3B78", "#E58B54"), ("#0E1330", "#1E2550"), ("#4A7DB5", "#F2C38B")]
    i0, k = int(clamp(tod, 0, 2.999)), tod - int(clamp(tod, 0, 2.999))
    top = mix(skyc[i0][0], skyc[min(3, i0 + 1)][0], k)
    low = mix(skyc[i0][1], skyc[min(3, i0 + 1)][1], k)
    vrect(c, 0, 0, W, H, [top, low, low], [0.0, 0.6, 1.0])
    if night > 0:
        v2.stars(c, W, H, t, 0.7 * night)
        v2.moon(c, 860, 330, 46, a=night)
    if sun > 0:
        sx, sy = 1000, 330
        add_glow(c, sx, sy, 150, "#FFE6A8", 0.6 * sun)
        c.drawCircle(sx, sy, 50, P("#FFF3D1", sun))
    # roof and the chimney over the shaft
    c.drawRect(R(SX0 - 20, SY_ROOF - 10, SX1 - SX0 + 70, 40), lin_paint(0, SY_ROOF - 10, 0, SY_ROOF + 30, [ROOF[0], ROOF[1]]))
    c.drawRect(R(186, SY_ROOF - 120, 44, 112), lin_paint(186, 0, 230, 0, [BRICK[0], BRICK[1]]))
    c.drawRect(R(180, SY_ROOF - 128, 56, 12), P(BRICK[1]))
    for j in range(SFL):
        y = SY0 + j * SFH
        hcol = mix(mix(CONC[1], COLD, 0.0), HOT, slab_heat)
        # the hollow slab with its concrete teeth
        c.drawRect(R(SX0, y, SX1 - SX0, SLAB), P(hcol))
        c.drawRect(R(SX0 + 90, y + 8, SX1 - SX0 - 170, SLAB - 16), P("#20242E"))
        for q in range(26):
            qx = SX0 + 96 + q * 25
            poly(c, [(qx, y + 8), (qx + 12, y + 8), (qx + 6, y + 15)], hcol)
            poly(c, [(qx + 6, y + SLAB - 8), (qx + 18, y + SLAB - 8), (qx + 12, y + SLAB - 15)], hcol)
        # the room below the slab
        ry, rh = y + SLAB, SFH - SLAB
        room_col = mix("#3A4256", "#5A3A30", warmup * 0.6)
        c.drawRect(R(SX0 + 90, ry, SX1 - SX0 - 170, rh), P(room_col))
        for d in range(4):                             # desks with computers
            dx = SX0 + 170 + d * 150
            c.drawRect(R(dx, ry + rh - 26, 80, 8), P("#8B6B4A"))
            c.drawRect(R(dx + 26, ry + rh - 56, 34, 26), P("#111827"))
            c.drawRect(R(dx + 29, ry + rh - 53, 28, 20), P("#60A5FA", 0.8))
            if people > 0:
                person(c, dx + 98, ry + rh - 2, 60, ["#2563EB", "#DB2777", "#F59E0B", "#10B981"][(d + j) % 4], t + d + j,
                       pose="sit", skin=SKIN[(d + j) % 4], hair="#141414", a=people)
                for b in range(2):
                    u = (t * 0.7 + b * 0.5 + d * 0.13 + j * 0.21) % 1.0
                    v2.puff(c, dx + 40 + b * 50, ry + rh - 60 - 40 * u, 10 + 10 * u, HOT, 0.45 * people * (1 - u))
        if gather > 0:                                 # warm air gathering under the ceiling
            for q in range(4):
                c.drawRect(R(SX0 + 90, ry + q * 7, SX1 - SX0 - 170, 7 * gather), P(HOT, 0.55 * gather * (1 - q / 4)))
        if small_fans > 0:                             # floor grilles letting cooled air up into the room
            for g in range(5):
                gx = SX0 + 150 + g * 140
                c.drawRect(R(gx, y + SLAB - 6, 40, 6), P("#CBD5E1"))
                u = (t * 0.9 + g * 0.2) % 1.0
                arrow(c, gx + 20, y + SLAB + 6 + 40 * u, gx + 20, y + SLAB + 30 + 40 * u, COLD, 0.85 * small_fans * (1 - u), 7, 14)
    # the outer wall with deep ledges and small windows (right), the shaft (left)
    for j in range(SFL):
        y = SY0 + j * SFH
        wc = mix(CONC[0], HOT, wall_heat)
        c.drawRect(R(SX1 - 80, y + SLAB, 70, SFH - SLAB), P(wc))
        c.drawRect(R(SX1 - 70, y + SLAB + 34, 50, 30), lin_paint(0, y + SLAB + 34, 0, y + SLAB + 64, ["#93C5FD", "#3B82F6"], a=0.9))
        c.drawRect(R(SX1 - 10, y + SLAB - 2, 76, 22), P(shade(wc, 0.08)))              # the ledge
        c.drawRect(R(SX1 - 10, y + SLAB + 20, 76, 6), P("#20242E", 0.6))
    c.drawRect(R(SX0, SY_ROOF + 30, 90, SFL * SFH), P(mix(CONC[2], HOT, wall_heat * 0.6)))
    c.drawRect(R(SX0 + 30, SY_ROOF - 10, 40, SFL * SFH + 40), P("#252A35"))             # the tall shaft
    if sun > 0 and night <= 0:                          # sunbeams hitting the ledges, the windows in shade
        for j in range(SFL):
            y = SY0 + j * SFH + SLAB
            c.drawLine(1000, 330, SX1 + 60, y - 2, P("#FFE6A8", 0.25 * sun, stroke=6))
    # ground and the fan room
    c.drawRect(R(0, SY0 + SFL * SFH, W, 1250 - (SY0 + SFL * SFH)), P("#3A3F4B"))
    if fans > 0 or small_fans > 0:
        fx, fy = 320, SY0 + SFL * SFH + 10
        c.drawRRect(rr(fx - 60, fy - 2, 120, 50, 10), P("#475569"))
        for b in range(3):
            ang = t * (14 * fans + 5 * small_fans) + b * 2.094
            c.drawLine(fx, fy + 22, fx + math.cos(ang) * 22, fy + 22 + math.sin(ang) * 22, P("#E2E8F0", stroke=6))
    if fans > 0:                                       # cold night air through every hollow slab
        for j in range(SFL):
            y = SY0 + j * SFH + SLAB / 2
            flow_arrows(c, [(SX0 + 100, y), (SX1 - 90, y)], t + j * 0.17, COLD, 0.95 * fans, speed=0.55, n=3, w=7, head=14)
    if rise > 0:                                       # warm air up the shaft and out of the chimney
        for j in range(SFL):
            y = SY0 + j * SFH + SLAB + 20
            flow_arrows(c, [(SX1 - 120, y), (SX0 + 60, y)], t + j * 0.2, HOT, 0.8 * rise, speed=0.5, n=2, w=7, head=14)
        flow_arrows(c, [(SX0 + 50, SY0 + SFL * SFH), (SX0 + 50, SY_ROOF - 100), (208, SY_ROOF - 230)], t, HOT, rise,
                    speed=0.45, n=5, w=10, head=20)
        wavy(c, 208, SY_ROOF - 132, 110, t, col="#FFD6A0", a=0.6 * rise, n=3, amp=10)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))


# ====================================================================================== mound (reveal)
def lung(c, x, y, s, breath, a=1.0):
    if a <= 0:
        return
    k = 1 + 0.12 * breath
    c.drawLine(x, y - 70 * s, x, y - 20 * s, P("#FDA4AF", a, stroke=10 * s))
    for side in (-1, 1):
        c.drawOval(R(x + side * 14 * s - (side < 0) * 62 * s * k, y - 30 * s * k, 62 * s * k, 110 * s * k), P("#FB7185", a))
        c.drawOval(R(x + side * 14 * s - (side < 0) * 62 * s * k + 10 * s, y - 20 * s * k, 30 * s * k, 60 * s * k),
                   P("#FECDD3", 0.5 * a))


def mound_set(c, t, breathe=0.0, wrong=0.0, works=0.0):
    vrect(c, 0, 0, W, H, ["#2E1F17", "#6B3A22", "#2A1A12"], [0.0, 0.6, 1.0])
    ph = math.sin(t * 2.2)
    termite_mound(c, 420, 1180, 640 * (1 + 0.015 * ph * breathe), t, shimmer=0.4)
    # its inside: tunnels and the nest at the bottom
    for k in range(5):
        c.drawLine(420 + (k - 2) * 40, 1150, 420 + (k - 2) * 14, 640, P("#3E2214", 0.85, stroke=8))
    c.drawOval(R(340, 1080, 160, 70), P("#3E2214"))
    for k in range(7):                                 # termites
        u = (t * 0.3 + k / 7) % 1.0
        c.drawOval(R(350 + 140 * u, 1108 + math.sin(k) * 10, 12, 7), P("#F5DEB3"))
    if breathe > 0:                                    # air in, air out, once a day
        inn = ph > 0
        for k in range(4):
            y = 760 + k * 100
            if inn:
                arrow(c, 120, y, 220, y + 10, COLD, breathe * 0.9, 9, 18)
                arrow(c, 720, y + 10, 620, y, COLD, breathe * 0.9, 9, 18)
            else:
                arrow(c, 220, y, 120, y - 10, HOT, breathe * 0.9, 9, 18)
                arrow(c, 620, y, 720, y - 10, HOT, breathe * 0.9, 9, 18)
        lung(c, 860, 620, 1.2, max(0.0, ph), a=breathe)
    if works > 0:                                      # the building: copied wrong, still works
        c.save()
        c.translate(820, 1010)
        c.scale(0.5 * e_back(clamp(works)), 0.5 * e_back(clamp(works)))
        c.drawRect(R(-200, -200, 400, 260), P(CONC[1]))
        for f in range(5):
            c.drawRect(R(-200, -200 + f * 50, 400, 8), P(shade(CONC[0], 0.1)))
        for k in range(6):
            c.drawRect(R(-180 + k * 64, -270, 18, 70), P(BRICK[0]))
        c.restore()
        v2.badge(c, 940, 860, works, "check", t, 1.0)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E140E", "#0B0E18"]))


# ====================================================================================== tag
def office_tag(c, t, fight=0.0, fly=0.0):
    vrect(c, 0, 0, W, H, ["#2B3448", "#3D4760"])
    c.drawRect(R(0, 1000, W, 250), P("#5B5146"))
    for k in range(5):
        c.drawLine(k * 260, 1000, k * 260 - 160, 1250, P("#4A4238", 0.6, stroke=3))
    # the air conditioner on the wall
    c.drawRRect(rr(340, 430, 400, 120, 24), lin_paint(0, 430, 0, 550, ["#CBD5E1", "#94A3B8"]))
    c.drawRect(R(370, 520, 340, 10), P("#475569"))
    for k in range(5):
        u = (t * 0.8 + k / 5) % 1.0
        c.drawLine(380 + k * 70, 545 + 80 * u, 400 + k * 70, 560 + 80 * u, P("#BAE6FD", 0.7 * (1 - u), stroke=5))
    c.drawRect(R(120, 760, 840, 26), P("#7C5A3A"))                                # a desk
    # two colleagues tugging the remote
    tug = math.sin(t * 9) * 30 * fight
    person(c, 300 - tug * 0.3, 1160, 380, "#2563EB", t, pose="carry", face=1, skin=SKIN[0], hair="#141414")
    person(c, 780 - tug * 0.3, 1160, 380, "#DB2777", t + 1, pose="carry", face=-1, skin=SKIN[2], hair="#141414")
    if fly <= 0:
        rx, ry, rot = 540 + tug, 880, tug * 0.8
    else:
        u = clamp(fly)
        rx, ry, rot = 540 + 120 * u, 880 - 380 * math.sin(u * math.pi * 0.9), u * 720
    c.save()
    c.translate(rx, ry)
    c.rotate(rot)
    c.drawRRect(rr(-26, -60, 52, 120, 14), P("#F8FAFC"))
    for k in range(3):
        c.drawCircle(0, -30 + k * 26, 7, P(["#EF4444", "#3B82F6", "#22C55E"][k]))
    c.restore()


class Eastgate(EpisodeV2):
    BUILD_NO = 109
    FIRST_SET = "city"
    CLEAR = "#0B0E18"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "EASTGATE CENTRE", "ar_sa": "مركز إيستغيت"}
    EMPH = {"en": ["OFFICE", "ZIMBABWE", "COPIED", "TERMITE", "MOUND", "SUN", "GLASS", "OVENS", "COOL", "THICK", "CONCRETE",
                   "SMALL", "WINDOWS", "LEDGES", "EVENING", "HEAT", "NIGHT", "FANS", "COLD", "HOLLOW", "FLOORS", "MORNING",
                   "PEOPLE", "COMPUTERS", "FRESH", "WARM", "SOMEWHERE", "RISES", "SHAFTS", "FORTY-EIGHT", "CHIMNEYS",
                   "ROOF", "FOLLOW", "TURBINES", "MOUNDS", "BREATHE", "LUNG", "WRONG", "WORKS", "NINETEEN", "NINETY-SIX",
                   "HARARE", "TEN", "HOUR", "CONGRATS", "YOURSELF", "BUILDING", "FIGHTS", "REMOTE"],
            "ar_sa": ["عمارة", "زيمبابوي", "قلدت", "النمل", "الشمس", "الزجاج", "فرن", "بارد", "خرسانة", "سميكة", "درايش",
                      "حواف", "المغرب", "شابعة", "حرارة", "بالليل", "مراوح", "البارد", "مجوفة", "الصبح", "الكمبيوترات",
                      "يسخنون", "صغيرة", "منعش", "الحار", "يطلع", "ممرات", "وأربعين", "مدخنة", "السطح", "متابعة",
                      "برجين", "عملاقة", "الجواب", "يتنفس", "الرية", "غلط", "شغال", "هراري", "عشر", "مبروك", "يبردها",
                      "تتهاوشون", "ريموت", "المكيف"]}
    KEYS = {"ar_sa": {
        ("hook", "OFFICE"): "عمارة", ("hook", "ZIMBABWE"): "زيمبابوي", ("hook", "COPIED"): "قلدت", ("hook", "TERMITE"): "النمل",
        ("break1", "SUN"): "الشمس", ("break1", "GLASS"): "الزجاج", ("break1", "OVENS"): "فرن", ("break1", "TERMITE"): "النمل",
        ("break1", "COOL"): "بارد",
        ("fix1", "THICK"): "سميكة", ("fix1", "CONCRETE"): "خرسانة", ("fix1", "WINDOWS"): "درايش", ("fix1", "LEDGES"): "حواف",
        ("break2", "EVENING"): "المغرب", ("break2", "FULL"): "شابعة", ("break2", "HEAT"): "حرارة",
        ("fix2", "NIGHT"): "بالليل", ("fix2", "FANS"): "مراوح", ("fix2", "COLD"): "البارد", ("fix2", "HOLLOW"): "مجوفة",
        ("break3", "MORNING"): "الصبح", ("break3", "PEOPLE"): "الناس", ("break3", "COMPUTERS"): "الكمبيوترات",
        ("break3", "HEAT"): "يسخنون",
        ("fix3", "SMALL"): "صغيرة", ("fix3", "FLOORS"): "الأرضيات", ("fix3", "COOL"): "منعش",
        ("break4", "WARM"): "الحار", ("break4", "SOMEWHERE"): "مكان",
        ("fix4", "RISES"): "فيطلع", ("fix4", "SHAFTS"): "ممرات", ("fix4", "CHIMNEYS"): "مدخنة",
        ("cta", "FOLLOW"): "متابعة", ("cta", "TURBINES"): "مراوح",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "BREATHE"): "يتنفس", ("reveal", "LUNG"): "الرية", ("reveal", "WRONG"): "غلط",
        ("reveal", "WORKS"): "شغال",
        ("stat", "NINETEEN"): "ألف", ("stat", "TEN"): "عشر", ("stat", "NIGHT"): "الليل",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "BUILDING"): "عمارة", ("tag", "FIGHTS"): "تتهاوشون", ("tag", "REMOTE"): "ريموت"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: towers with wind turbines"),
                   "stat": [("1996", "OPENED IN HARARE"), ("10x", "FRESH AIR AN HOUR"), ("48", "BRICK CHIMNEYS")],
                   "L": {"copied": "IT COPIED A TERMITE MOUND", "oven": "GLASS OFFICE = OVEN", "q": "HOW DO MOUNDS STAY COOL?",
                         "thick": "THICK CONCRETE", "ledges": "LEDGES SHADE THE WINDOWS", "full": "FULL OF THE DAY'S HEAT",
                         "fans": "NIGHT FANS", "cold": "COLD AIR THROUGH HOLLOW FLOORS", "people": "PEOPLE + COMPUTERS = HEAT",
                         "small": "SMALL FANS BY DAY", "cool": "IT COMES IN COOL", "warm": "WHERE DOES THE WARM AIR GO?",
                         "chimneys": "UP AND OUT: 48 CHIMNEYS", "breathe": "MOUNDS BREATHE LIKE A LUNG",
                         "wrong": "COPIED WRONG... STILL WORKS", "name": "THE EASTGATE CENTRE", "remote": "THE AC REMOTE WAR",
                         "night": "COOLED BY NIGHT AIR"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: برجين بمراوح هوا"),
                      "stat": [("1996", "افتتحت في هراري"), ("10", "مرات يتجدد الهوا بالساعة"), ("48", "مدخنة طوب")],
                      "L": {"copied": "قلّدت بيت النمل الأبيض", "oven": "مكتب زجاج = فرن", "q": "كيف بيت النمل يظل بارد؟",
                            "thick": "خرسانة سميكة", "ledges": "حواف تظلل الدرايش", "full": "شابعة من حرارة النهار",
                            "fans": "مراوح الليل", "cold": "هوا بارد في الأرضيات", "people": "ناس + كمبيوترات = حرارة",
                            "small": "مراوح صغيرة بالنهار", "cool": "يدخل منعش", "warm": "وين يروح الهوا الحار؟",
                            "chimneys": "يطلع من ٤٨ مدخنة", "breathe": "بيت النمل يتنفّس مثل الرية",
                            "wrong": "قلّدوه غلط... وللحين شغّال", "name": "مركز إيستغيت", "remote": "حرب ريموت المكيّف",
                            "night": "يبرّدها هوا الليل"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "office": ("hook", "OFFICE", 0.2), "zimbabwe": ("hook", "ZIMBABWE", 0.4), "copied": ("hook", "COPIED", 0.6),
            "termite": ("hook", "TERMITE", 0.85),
            "sun": ("break1", "SUN", 0.05), "glass": ("break1", "GLASS", 0.2), "ovens": ("break1", "OVENS", 0.4),
            "termite1": ("break1", "TERMITE", 0.75), "cool1": ("break1", "COOL", 0.95),
            "thick": ("fix1", "THICK", 0.15), "concrete": ("fix1", "CONCRETE", 0.3), "windows": ("fix1", "WINDOWS", 0.55),
            "ledges": ("fix1", "LEDGES", 0.9),
            "evening": ("break2", "EVENING", 0.2), "full": ("break2", "FULL", 0.6), "heat2": ("break2", "HEAT", 0.9),
            "night": ("fix2", "NIGHT", 0.1), "fans": ("fix2", "FANS", 0.3), "cold": ("fix2", "COLD", 0.5),
            "hollow": ("fix2", "HOLLOW", 0.85),
            "morning": ("break3", "MORNING", 0.15), "people": ("break3", "PEOPLE", 0.35), "computers": ("break3", "COMPUTERS", 0.5),
            "heat3": ("break3", "HEAT", 0.7),
            "small": ("fix3", "SMALL", 0.1), "floors3": ("fix3", "FLOORS", 0.6), "cool3": ("fix3", "COOL", 0.95),
            "warm": ("break4", "WARM", 0.4), "somewhere": ("break4", "SOMEWHERE", 0.85),
            "rises": ("fix4", "RISES", 0.1), "shafts": ("fix4", "SHAFTS", 0.3), "chimneys": ("fix4", "CHIMNEYS", 0.8),
            "follow": ("cta", "FOLLOW", 0.1), "turbines": ("cta", "TURBINES", 0.8),
            "answer": ("reveal", "ANSWER", 0.05), "breathe": ("reveal", "BREATHE", 0.3), "lung": ("reveal", "LUNG", 0.45),
            "wrong": ("reveal", "WRONG", 0.7), "works": ("reveal", "WORKS", 0.95),
            "s1": ("stat", "NINETEEN", 0.05), "s2": ("stat", "TEN", 0.55), "s3": ("stat", "NIGHT", 0.9),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_building": ("tag", "BUILDING", 0.2), "t_fights": ("tag", "FIGHTS", 0.7), "t_remote": ("tag", "REMOTE", 0.9)})
        T["oven1"] = max(T["ovens"], T["glass"] + 0.3)
        T["ledges1"] = max(T["ledges"], T["windows"] + 0.3)
        T["full1"] = max(T["full"], s("break2") + 0.3)
        T["hollow1"] = max(T["hollow"], T["fans"] + 0.4)
        T["people1"] = max(T["people"], s("break3") + 0.3)
        T["cool31"] = max(T["cool3"], T["small"] + 0.5)
        T["warm1"] = max(T["warm"], s("break4") + 0.25)
        T["chim1"] = max(T["chimneys"], T["shafts"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "oven", 1)
        self.cut(s("fix1") - 0.12, "section", -1)
        self.cut(s("cta") - 0.12, "city", 1)
        self.cut(s("reveal") - 0.12, "mound", -1)
        self.cut(s("stat") - 0.12, "city", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["oven1"], T["ledges1"]), (T["full1"], T["hollow1"]), (T["people1"], T["cool31"]),
                      (T["warm1"], T["chim1"])]
        self.shakes = [(T["termite"], 0.3, 4), (T["oven1"], 0.4, 6), (T["full1"], 0.3, 6), (T["people1"], 0.3, 5),
                       (T["warm1"], 0.3, 5), (T["wrong"], 0.3, 5), (s("closer") + 0.2, 0.35, 6), (T["t_fights"], 0.3, 6)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: city (hook, cta, stat, closer)
    def draw_city(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["copied"] - 0.4, s("break1") - 0.25))
            z = lerp(2.7, 1.0, k)
            fx, fy = lerp(880, 540, k), lerp(GROUND_Y - 330, 800, k)
            c.save()
            c.translate(540, 760)
            c.scale(z, z)
            c.translate(-fx, -fy)
            city_scene(c, t)
            c.restore()
            c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))
        elif ph == "closer":
            city_scene(c, t, dusk=1.0, lit=1.0, mound=1.0, mound_x=985, mound_h=300)
        else:
            city_scene(c, t, dusk=0.0 if ph == "stat" else 0.35, lit=0.0 if ph == "stat" else 0.4)

    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "copied", T["copied"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=54)

    # ------------------------------------------------------------------ set: oven (break1)
    def draw_oven(self, c, t):
        T, s = self.T, self.tl.s
        oven(c, t, heat=prog(t, T["sun"] - 0.2, T["ovens"] + 0.4), q=prog(t, T["termite1"] - 0.3, T["termite1"] + 0.1))

    def ui_oven(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "oven", T["glass"] - 0.1, T["termite1"] - 0.3, accent=WARN, size=58)
        self.chip(540, 300, "q", T["termite1"] - 0.3, s("fix1") - 0.1, accent=HILITE, size=50)
        self.badge("alert", T["oven1"], s("fix1") - 0.2, x=160, y=470)
        self.red(T["oven1"], 1.2)

    # ------------------------------------------------------------------ set: section (fix1 .. fix4)
    def draw_section(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        order = ("fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4")
        i = order.index(ph) if ph in order else 6
        kw = {}
        if i == 0:
            kw = dict(tod=0.0, sun=1.0)
        elif i == 1:
            kw = dict(tod=prog(t, s("break2") - 0.1, T["evening"] + 0.5), sun=1 - prog(t, s("break2"), T["full"]),
                      wall_heat=prog(t, T["evening"], T["full1"] + 0.3), slab_heat=prog(t, T["evening"], T["full1"] + 0.3))
        elif i == 2:
            cool = prog(t, T["cold"], T["hollow1"] + 0.6)
            kw = dict(tod=1 + prog(t, s("fix2") - 0.1, T["night"] + 0.4), sun=0.0, night=prog(t, s("fix2"), T["night"] + 0.3),
                      fans=prog(t, T["fans"] - 0.2, T["fans"] + 0.2), wall_heat=1 - cool, slab_heat=1 - cool)
        elif i == 3:
            kw = dict(tod=2 + prog(t, s("break3") - 0.1, T["morning"] + 0.4), sun=prog(t, T["morning"], T["morning"] + 0.5),
                      night=1 - prog(t, s("break3"), T["morning"] + 0.3), people=prog(t, T["people"] - 0.3, T["people"]),
                      warmup=prog(t, T["computers"], T["heat3"] + 0.5))
        elif i == 4:
            kw = dict(tod=3.0, sun=1.0, people=1.0, small_fans=prog(t, T["small"] - 0.2, T["small"] + 0.2),
                      warmup=1 - prog(t, T["floors3"], T["cool31"] + 0.4))
        elif i == 5:
            kw = dict(tod=3.0, sun=1.0, people=1.0, small_fans=1.0, gather=prog(t, s("break4"), T["warm1"] + 0.3))
        else:
            kw = dict(tod=3.0, sun=1.0, people=1.0, small_fans=1.0, gather=1 - prog(t, T["rises"], T["chim1"]),
                      rise=prog(t, T["rises"] - 0.2, T["rises"] + 0.3))
        zk = e_io(prog(t, s("fix4") - 0.3, s("fix4") + 0.4))             # close on the shaft and chimney for the finale
        z = lerp(1.0, 1.12, zk)
        c.save()
        c.translate(540, 800)
        c.scale(z, z)
        c.translate(-lerp(540, 470, zk), -lerp(800, 760, zk))
        section(c, t, **kw)
        c.restore()
        c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1490, ["#1E2230", "#0B0E18"]))

    def ui_section(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "fix1":
            self.chip(540, 300, "thick", T["thick"] - 0.2, T["windows"] - 0.2, accent="#CBD5E1", size=56)
            self.chip(540, 300, "ledges", T["windows"] - 0.2, s("break2") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["ledges1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "full", T["evening"], s("fix2") - 0.15, accent=WARN, size=54)
            self.badge("alert", T["full1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["full1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "fans", T["fans"] - 0.2, T["cold"] - 0.1, accent="#7DD3FC", size=60)
            self.chip(540, 300, "cold", T["cold"] - 0.1, s("break3") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["hollow1"], s("break3") - 0.15, x=160, y=470)
        elif ph == "break3":
            self.chip(540, 300, "people", T["people"] - 0.2, s("fix3") - 0.15, accent=WARN, size=50)
            self.badge("alert", T["people1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["people1"], 1.2)
        elif ph == "fix3":
            self.chip(540, 300, "small", T["small"] - 0.2, T["floors3"] - 0.1, accent="#7DD3FC", size=56)
            self.chip(540, 300, "cool", T["floors3"] - 0.1, s("break4") - 0.15, accent=GOOD, size=58)
            self.badge("check", T["cool31"], s("break4") - 0.15, x=160, y=470)
        elif ph == "break4":
            self.chip(540, 300, "warm", s("break4") + 0.05, s("fix4") - 0.15, accent=WARN, size=48)
            self.badge("alert", T["warm1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["warm1"], 1.2)
        else:
            self.chip(540, 300, "chimneys", T["shafts"] - 0.2, s("cta") - 0.15, accent=GOOD, size=50)
            self.badge("check", T["chim1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: mound (reveal)
    def draw_mound(self, c, t):
        T, s = self.T, self.tl.s
        mound_set(c, t, breathe=prog(t, T["breathe"] - 0.3, T["breathe"] + 0.2), wrong=prog(t, T["wrong"] - 0.2, T["wrong"]),
                  works=prog(t, T["works"] - 0.3, T["works"] + 0.2))

    def ui_mound(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "breathe", T["breathe"] - 0.2, T["wrong"] - 0.2, accent="#FDA4AF", size=50)
        self.chip(540, 300, "wrong", T["wrong"] - 0.2, s("stat") - 0.15, accent=GOOD, size=52)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        office_tag(c, t, fight=prog(t, T["t_fights"] - 0.4, T["t_fights"]), fly=prog(t, T["t_remote"], T["t_remote"] + 1.0))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "night", T["t_building"] - 0.2, T["t_fights"] - 0.3, accent="#7DD3FC", size=56)
        self.chip(540, 300, "remote", T["t_fights"] - 0.3, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.hum(3.0, 90.0), -20), (T["copied"], sfx.riser(0.8, 62), -12),
              (T["termite"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["glass"], sfx.sizzle(1.2, 64), -12),
               (T["oven1"], sfx.thud(0.4, 65), -8), (T["oven1"] + 0.3, sfx.alarm(3, 820.0), -14), (T["termite1"], sfx.pop(66), -6)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 67), -6), (T["thick"], sfx.thunk(68), -8),
               (T["ledges1"], sfx.ding(), -8), (T["ledges1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["full1"], sfx.sizzle(0.8, 69), -10), (T["full1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["fans"], sfx.whirr(2.0, 120.0, 190.0, 70), -10), (T["hollow1"], sfx.ding(), -8),
               (T["hollow1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["people1"], sfx.womp(), -10), (T["people1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["small"], sfx.whirr(1.4, 240.0, 300.0, 71), -14), (T["cool31"], sfx.ding(), -8),
               (T["cool31"] + 0.2, sfx.chime(), -6)]
        ev += [(T["warm1"], sfx.thunk(72), -8), (T["warm1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["rises"], sfx.riser(1.2, 73), -12), (T["chim1"], sfx.sparkle(1.0, 10, 74), -8), (T["chim1"], sfx.ding(), -8),
               (T["chim1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["breathe"], sfx.hiss(1.2, 95), -14),
               (T["works"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_fights"], sfx.snap(104), -10),
               (T["t_remote"], sfx.whoosh(0.5, True, 105), -10), (T["t_remote"] + 0.8, sfx.womp(), -8)]
        return ev


NAME = "eastgate"
EPISODE = Eastgate
