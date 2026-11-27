"""Episode 107 - A high-speed (detachable) chairlift.  v2 look.

Sets: mountain (hook: close on the top station as a chair lets go of the moving cable and rolls off on a rail, out to the
whole lift climbing a snowy mountain at dusk; cta, stat; closer with the lift lit at night), station (break1: the cable
runs as fast as a bike, a cyclist keeps pace with a chair; fix1: in the station the grip opens and the chair rolls off the
cable onto a rail; break2: still at full speed, it knocks a waiting skier flat; fix2: a row of spinning tyres slows it to a
walk, the skier sits down, the tyres speed it back up and the grip snaps shut on the cable), slope (break3: a loose grip
lets a chair slide back down the cable into the one below; fix3: a close-up of the grip, springs squeezing its jaws shut,
a tester gauge, one weak grip and the whole lift stops), terminal (break4: on a hot day the cable sags and slips on the
big wheel; fix4: a giant concrete weight in a pit pulls the wheel back and the cable runs tight), port (reveal: a 1930s
banana dock, bunches on hooks riding a cable into a ship, and one by one the hooks carry chairs), tag (English: a glove
slips off and falls into the snow; Arabic: the wedding buffet line that never moves).
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

SNOW = ("#E3EAF4", "#B9C7DA", "#8193AD")
STEELC = ("#CBD5E1", "#94A3B8", "#475569")
SKIN = ("#E8B48A", "#C68E62", "#A8754E", "#F1C7A3")
JACKETS = ("#EF4444", "#3B82F6", "#F59E0B", "#10B981", "#A855F7", "#EC4899")


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== pieces
def grip(c, x, y, s, open_=0.0, a=1.0, weak=0.0):
    """The grip on the cable at (x, y): a box with two jaws around the rope; open_ 0..1 spreads the jaws."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    col = mix("#64748B", WARN, weak)
    c.drawRRect(rr(-22, -6, 44, 30, 6), lin_paint(-22, 0, 22, 0, [shade(col, 0.3), col, shade(col, -0.3)], a=a))
    for sd in (-1, 1):
        c.save()
        c.translate(sd * 14, -2)
        c.rotate(sd * 40 * open_)
        c.drawRRect(rr(-5 if sd > 0 else -5, -16, 10, 16, 3), P("#334155", a))
        c.restore()
    c.restore()


def chair(c, x, y, s, t, riders=0, open_=0.0, swing=0.0, a=1.0, seed=0, weak=0.0, empty_seat=True):
    """A four-seat chair hanging from its grip at (x, y) on the cable. riders: how many people sit on it."""
    if a <= 0:
        return
    grip(c, x, y, s, open_, a, weak)
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.rotate(swing)
    c.drawLine(0, 22, 0, 150, P(STEELC[2], a, stroke=8))                     # the hanger
    c.drawLine(0, 150, -40, 170, P(STEELC[2], a, stroke=8))
    c.drawRRect(rr(-70, 120, 12, 70, 6), P(STEELC[1], a))                    # backrest post
    c.drawRRect(rr(-78, 118, 70, 46, 10), lin_paint(0, 118, 0, 164, ["#1E3A8A", "#172554"], a=a))   # backrest
    c.drawRRect(rr(-78, 168, 120, 18, 8), lin_paint(0, 168, 0, 186, ["#1E40AF", "#1E3A8A"], a=a))   # seat
    c.drawLine(-60, 150, 54, 150, P(STEELC[0], a, stroke=6))                  # the bar
    c.drawLine(54, 150, 54, 214, P(STEELC[0], a, stroke=6))
    c.drawLine(30, 214, 74, 214, P(STEELC[0], a, stroke=6))                   # footrest
    rng = random.Random(seed)
    for k in range(riders):
        px = -40 + k * 24
        col = JACKETS[(seed + k) % len(JACKETS)]
        c.drawRRect(rr(px - 13, 128, 26, 44, 10), P(col, a))
        c.drawCircle(px, 116, 12, P(SKIN[(seed + k) % 4], a))
        c.drawArc(R(px - 13, 102, 26, 18), 180, 180, True, P(rng.choice(["#111827", "#7C2D12", "#F59E0B"]), a))
        c.drawLine(px + 4, 176, px + 26, 206, P("#1F2937", a, stroke=9))      # legs to the footrest
        c.drawLine(px + 30, 206, px + 52, 220, P("#111827", a, stroke=5))     # skis
    c.restore()


def tower(c, x, base, top, a=1.0):
    c.drawLine(x, base, x, top, P(STEELC[2], a, stroke=22))
    c.drawLine(x - 4, base, x - 4, top, P(STEELC[1], a, stroke=6))
    c.drawRRect(rr(x - 70, top - 12, 140, 18, 6), P(STEELC[2], a))
    for sx in (-50, -18, 14, 46):
        c.drawCircle(x + sx + 4, top - 14, 9, P("#1F2937", a))


def mountains(c, t, night=0.0, snow_y=1240):
    vrect(c, 0, 0, W, 1260, [mix("#1E3A6E", "#070B1F", night), mix("#6D5A9C", "#101A3A", night),
                            mix("#F0A3A0", "#1B2A55", night)], [0, 0.55, 1])
    if night > 0:
        v2.stars(c, W, H, t, 0.9 * night)
    for k, (px, py, w, h) in enumerate(((180, 760, 520, 420), (620, 640, 640, 520), (980, 720, 480, 380))):
        p = skia.Path()
        p.moveTo(px - w / 2, py + h)
        p.lineTo(px, py)
        p.lineTo(px + w / 2, py + h)
        p.close()
        c.drawPath(p, lin_paint(px - w / 2, 0, px + w / 2, 0, [mix("#9AA8C2", "#1E2A4A", night), mix("#5E6E8E", "#141D38", night)]))
        cap = skia.Path()
        cap.moveTo(px - w * 0.16, py + h * 0.32)
        cap.lineTo(px, py)
        cap.lineTo(px + w * 0.16, py + h * 0.32)
        cap.lineTo(px + w * 0.05, py + h * 0.26)
        cap.lineTo(px - w * 0.04, py + h * 0.34)
        cap.close()
        c.drawPath(cap, P(mix("#E8EEF7", "#5B6B8C", night)))
    slope = skia.Path()                                # the ski slope rising to the right
    slope.moveTo(0, 1260)
    slope.lineTo(0, 1060)
    slope.quadTo(500, 880, 1080, 600)
    slope.lineTo(1080, 1260)
    slope.close()
    c.drawPath(slope, lin_paint(0, 600, 0, 1260, [mix(SNOW[0], "#4A5A7C", night), mix(SNOW[1], "#2E3A58", night)]))
    rng = random.Random(4)
    for k in range(26):                                # pines
        x = rng.uniform(0, W)
        yb = 1060 - (x / W) ** 1.2 * 440 + rng.uniform(20, 160)
        h = rng.uniform(50, 90)
        p = skia.Path()
        p.moveTo(x, yb - h)
        p.lineTo(x - h * 0.35, yb)
        p.lineTo(x + h * 0.35, yb)
        p.close()
        c.drawPath(p, P(mix("#1F4D3A", "#0E2219", night)))


CAB0, CAB1 = (110, 1090), (900, 520)                   # the lift line: bottom and top stations


def cable_pt(u):
    x = lerp(CAB0[0], CAB1[0], u)
    y = lerp(CAB0[1], CAB1[1], u) + math.sin(math.pi * u) * 26
    return x, y


def lift_line(c, t, night=0.0, run=1.0, lit=0.0, detach=None):
    """Towers, the cable and the chairs climbing to the top station (upper right)."""
    for u in (0.27, 0.52, 0.77):
        x, y = cable_pt(u)
        tower(c, x, y + 260, y + 14)
    p = skia.Path()
    p.moveTo(*cable_pt(0))
    for k in range(1, 41):
        p.lineTo(*cable_pt(k / 40))
    p.lineTo(1080, 520)
    c.drawPath(p, P("#1F2937", 1, stroke=5))
    # the top station, cut open: the big wheel and the slow rail
    c.drawRRect(rr(860, 420, 260, 170, 16), P(mix("#475569", "#1E293B", night), 0.95))
    c.drawRRect(rr(880, 440, 240, 132, 12), P(mix("#0F172A", "#0B1020", night)))
    c.save()
    c.translate(1010, 520)
    c.scale(1, 0.32)
    c.drawCircle(0, 0, 90, P(STEELC[1], 1, stroke=12))
    c.rotate(t * 90 * run)
    for k in range(6):
        c.rotate(60)
        c.drawLine(0, 0, 0, -86, P(STEELC[1], 0.8, stroke=6))
    c.restore()
    c.drawLine(880, 548, 1080, 548, P("#F59E0B", 1, stroke=6))            # the slow rail
    if lit > 0:
        c.drawRect(R(880, 440, 240, 132), P("#FDE68A", 0.25 * lit))
    for k in range(9):                                 # chairs riding up
        u = (k / 9 + t * 0.018 * run) % 1.0
        if u > 0.985:
            continue
        x, y = cable_pt(u)
        chair(c, x, y, 0.42, t, riders=2 + (k % 3), seed=k)
    if detach is not None:                             # one chair letting go of the cable in the station
        d = clamp(detach)
        x = lerp(880, 1010, e_out(d))
        y = lerp(520, 548, smooth(d * 3))
        chair(c, x, y, 0.42, t, riders=3, open_=clamp(d * 4), seed=11, swing=math.sin(d * 9) * 6 * (1 - d))
        if 0.05 < d < 0.4:
            add_glow(c, x, 520, 40, HILITE, 0.7 * (1 - d / 0.4))


# ====================================================================================== the station close-up
CY = 520                                               # the cable's height in the station set
RAIL = 590


def bike(c, x, y, s, t, a=1.0):
    """A cyclist seen from the side, riding right."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for wx in (-60, 60):
        c.drawCircle(wx, 0, 44, P("#111827", a, stroke=8))
        c.save()
        c.translate(wx, 0)
        c.rotate(t * 720)
        for k in range(4):
            c.rotate(45)
            c.drawLine(-40, 0, 40, 0, P("#9CA3AF", a, stroke=2))
        c.restore()
    c.drawLine(-60, 0, -10, -50, P("#DC2626", a, stroke=8))
    c.drawLine(-10, -50, 60, 0, P("#DC2626", a, stroke=8))
    c.drawLine(-10, -50, 40, -56, P("#DC2626", a, stroke=8))
    c.drawLine(-60, 0, 0, 0, P("#DC2626", a, stroke=8))
    ph = t * 9
    c.drawLine(-14, -96, -2 + math.cos(ph) * 18, -10 + math.sin(ph) * 18, P("#1F2937", a, stroke=12))   # leg
    c.drawRRect(rr(-30, -150, 34, 62, 14), P("#F59E0B", a))
    c.drawLine(0, -134, 40, -64, P(SKIN[0], a, stroke=9))
    c.drawCircle(-6, -166, 18, P(SKIN[0], a))
    c.drawArc(R(-28, -190, 44, 30), 180, 180, True, P("#2563EB", a))
    c.restore()


def skier(c, x, y, h, t, fall=0.0, sit=0.0, a=1.0, col="#EF4444"):
    """A skier standing at the loading point (feet at y); fall 0..1 knocks them over, sit 0..1 sits them down."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    if fall > 0:
        c.translate(-160 * e_out(fall), -60 * math.sin(math.pi * clamp(fall)))
        c.rotate(-100 * e_out(fall))
    c.drawLine(-50, 0, 60, 0, P("#111827", a, stroke=8))                     # skis
    u = h / 300
    kneel = 60 * sit * u
    c.drawLine(-8 * u, 0, -8 * u, -120 * u + kneel, P("#1F2937", a, stroke=22 * u))
    c.drawLine(12 * u, 0, 12 * u, -120 * u + kneel, P("#1F2937", a, stroke=22 * u))
    c.drawRRect(rr(-36 * u, -230 * u + kneel, 72 * u, 120 * u, 26 * u), P(col, a))
    c.drawCircle(0, -262 * u + kneel, 30 * u, P(SKIN[3], a))
    c.drawArc(R(-32 * u, -298 * u + kneel, 64 * u, 46 * u), 180, 180, True, P("#1E3A8A", a))
    c.drawRRect(rr(-28 * u, -272 * u + kneel, 56 * u, 14 * u, 6 * u), P("#F59E0B", a))   # goggles
    for sd in (-1, 1):                                 # poles
        c.drawLine(sd * 40 * u, -170 * u + kneel, sd * 70 * u, 0, P("#9CA3AF", a, stroke=6))
    c.restore()


def tires(c, x0, x1, y, t, spin=1.0, a=1.0):
    """A row of spinning tyres along the rail that slow the chair down and speed it up again."""
    n = 8
    for k in range(n):
        x = lerp(x0, x1, k / (n - 1))
        c.drawCircle(x, y, 24, P("#111827", a))
        c.drawCircle(x, y, 24, P("#374151", a, stroke=6))
        c.save()
        c.translate(x, y)
        c.rotate(t * 500 * spin * (1.6 - k / n))
        c.drawLine(-14, 0, 14, 0, P("#9CA3AF", a, stroke=4))
        c.drawLine(0, -14, 0, 14, P("#9CA3AF", a, stroke=4))
        c.restore()


def station(c, t, chair_x=None, open_=0.0, on_rail=0.0, tire_a=0.0, fall=0.0, sit=0.0, skier_a=1.0, bike_x=None,
            speed_lines=1.0, riders=0):
    vrect(c, 0, 0, W, H, ["#0F1B33", "#1D2C4C"])
    c.drawRect(R(0, 300, W, 120), P("#1E293B"))                              # the roof beam
    for k in range(6):
        add_glow(c, 90 + k * 190, 430, 70, "#FFF1C9", 0.35)
    c.drawRect(R(0, 1180, W, 80), lin_paint(0, 1180, 0, 1260, [SNOW[1], SNOW[2]]))   # the snowy floor and loading mat
    c.drawRect(R(560, 1170, 300, 16), P("#2563EB"))
    # the cable, running fast
    c.drawLine(0, CY, W, CY, P("#111827", 1, stroke=10))
    off = (t * 900) % 60
    for k in range(20):
        xx = k * 60 - off
        c.drawLine(xx, CY, xx + 22, CY, P("#64748B", 0.9 * speed_lines, stroke=4))
    # the slow rail inside the station
    c.drawLine(380, RAIL, W, RAIL, P("#F59E0B", 1, stroke=10))
    c.drawRect(R(370, RAIL - 30, 20, 60), P("#F59E0B"))
    if tire_a > 0:
        tires(c, 440, 1040, RAIL - 46, t, a=tire_a)
    if bike_x is not None:
        bike(c, bike_x, 1150, 1.0, t)
    skier(c, 720, 1170, 300, t, fall=fall, sit=sit, a=skier_a)
    if chair_x is not None:
        y = lerp(CY, RAIL, smooth(on_rail))
        chair(c, chair_x, y - 8, 1.6, t, riders=riders, open_=open_, seed=3)


def speedo(c, x, y, kmh, a=1.0, top=20.0, col=None):
    if a <= 0:
        return
    c.drawCircle(x, y, 110, P("#0F172A", 0.9 * a))
    c.drawCircle(x, y, 110, P("#E2E8F0", a, stroke=8))
    arc = skia.Path()
    arc.addArc(R(x - 86, y - 86, 172, 172), 150, 240 * clamp(kmh / top))
    c.drawPath(arc, P(col or (WARN if kmh > 10 else GOOD), a, stroke=18))
    ang = math.radians(150 + 240 * clamp(kmh / top))
    c.drawLine(x, y, x + math.cos(ang) * 80, y + math.sin(ang) * 80, P("#F8FAFC", a, stroke=8))
    c.drawCircle(x, y, 12, P("#F8FAFC", a))
    text(c, f"{int(round(kmh))}", x, y + 70, 54, "#F8FAFC", "Poppins-Black", a=a)


# ====================================================================================== the slope and the grip close-up
def slope_scene(c, t, slide=0.0, run=1.0):
    vrect(c, 0, 0, W, H, ["#1E3A6E", "#6D5A9C", "#F0A3A0"], [0, 0.6, 1])
    hill = skia.Path()
    hill.moveTo(0, 1260)
    hill.lineTo(0, 1180)
    hill.lineTo(1080, 640)
    hill.lineTo(1080, 1260)
    hill.close()
    c.drawPath(hill, lin_paint(0, 640, 0, 1260, [SNOW[0], SNOW[1]]))
    a0, a1 = (60, 1050), (1020, 420)
    tower(c, 200, 1180, a0[1] - (a0[1] - a1[1]) * (140 / 960) + 10)
    tower(c, 880, 760, a0[1] - (a0[1] - a1[1]) * (820 / 960) + 10)
    c.drawLine(a0[0], a0[1], a1[0], a1[1], P("#1F2937", 1, stroke=8))

    def on(u):
        return lerp(a0[0], a1[0], u), lerp(a0[1], a1[1], u)
    lx, ly = on(0.36)
    chair(c, lx, ly, 0.9, t, riders=2, seed=1)
    u_top = 0.7 - 0.31 * e_in(clamp(slide))
    ux, uy = on(u_top)
    chair(c, ux, uy, 0.9, t, riders=3, seed=4, open_=0.5 * clamp(slide * 3), weak=clamp(slide * 3),
          swing=math.sin(t * 7) * 8 * clamp(slide * 2))
    if slide >= 1:
        add_glow(c, lx + 30, ly + 60, 90, WARN, 0.5)


def grip_closeup(c, t, squeeze=1.0, test=0.0, weak=0.0, stop=0.0):
    vrect(c, 0, 0, W, H, ["#0F172A", "#1E293B"])
    cx, cy = 540, 700
    c.drawCircle(cx, cy, 70, lin_paint(cx - 70, cy - 70, cx + 70, cy + 70, ["#9CA3AF", "#4B5563", "#1F2937"]))   # cable end-on
    for k in range(6):                                 # its strands
        ang = k * math.pi / 3
        c.drawCircle(cx + math.cos(ang) * 38, cy + math.sin(ang) * 38, 22, P("#6B7280", 1, stroke=4))
    gap = lerp(150, 78, smooth(squeeze))
    for sd in (-1, 1):                                 # the two jaws
        jx = cx + sd * gap
        c.drawRRect(rr(jx - 40 if sd > 0 else jx - 40, cy - 120, 80, 240, 22),
                    lin_paint(jx - 40, 0, jx + 40, 0, ["#E2E8F0", "#94A3B8", "#475569"]))
        # the spring pushing it in
        sx0, sx1 = jx + sd * 40, jx + sd * 250
        p = skia.Path()
        p.moveTo(sx0, cy)
        n = 9
        for k in range(1, n * 2 + 1):
            xx = lerp(sx0, sx1, k / (n * 2))
            p.lineTo(xx, cy + (-52 if k % 2 else 52))
        c.drawPath(p, P(mix(GOOD, WARN, weak), 1, stroke=12))
        c.drawRRect(rr(sx1 - 20 if sd > 0 else sx1 - 20, cy - 90, 40, 180, 10), P("#334155"))
        if squeeze > 0.2:
            for j in range(3):                         # force arrows
                ax = jx + sd * (90 + 30 * j + 10 * math.sin(t * 8 + j))
                c.drawLine(ax + sd * 40, cy + 150, ax, cy + 150, P(HILITE, 0.8 * squeeze, stroke=8))
    if test > 0:                                       # the tester gauge
        gx, gy = 540, 1080
        c.drawRRect(rr(gx - 300, gy - 50, 600, 100, 50), P("#0B1220", 0.95 * test))
        f = lerp(0.85, 0.32, weak)
        c.drawRRect(rr(gx - 280, gy - 30, 560 * f, 60, 30), P(mix(GOOD, WARN, weak), test))
        c.drawLine(gx - 280 + 560 * 0.6, gy - 46, gx - 280 + 560 * 0.6, gy + 46, P("#F8FAFC", test, stroke=6))
    if stop > 0:
        k = e_back(clamp(stop))
        c.save()
        c.translate(870, 420)
        c.scale(k, k)
        add_glow(c, 0, 0, 160, WARN, 0.8)
        c.drawCircle(0, 0, 100, P("#DC2626"))
        c.drawCircle(0, 0, 100, P("#FFFFFF", 1, stroke=8))
        text(c, "STOP", 0, 22, 62, "#FFFFFF", "Poppins-Black")
        c.restore()


# ====================================================================================== the bottom terminal
def terminal(c, t, heat=0.0, sag=0.0, slip=0.0, weight=0.0, run=1.0):
    vrect(c, 0, 0, W, H, ["#1E3A6E", "#6D5A9C", "#F0A3A0"], [0, 0.6, 1])
    if heat > 0:
        add_glow(c, 880, 300, 220, "#FFD27A", 0.7 * heat)
        c.drawCircle(880, 300, 70, P("#FFE7A3", heat))
    c.drawRect(R(0, 1000, W, 260), lin_paint(0, 1000, 0, 1260, [SNOW[0], SNOW[1]]))
    shift = -150 * smooth(weight)                      # the weight pulls the wheel's carriage left
    wx, wy = 320 + shift, 720
    c.drawRect(R(90, 870, 520, 20), P("#334155"))                            # the carriage's rails
    c.drawRRect(rr(wx - 120, 840, 240, 40, 10), P("#475569"))                # the carriage
    c.save()
    c.translate(wx, wy)
    c.drawCircle(0, 0, 150, P("#64748B", 1, stroke=26))
    c.rotate(t * 120 * run)
    for k in range(8):
        c.rotate(45)
        c.drawLine(0, 0, 0, -140, P("#94A3B8", 1, stroke=8))
    c.restore()
    c.drawCircle(wx, wy, 26, P("#1F2937"))
    # the cable: round the wheel and off to the tower on the right, sagging with the heat
    tx, ty = 1060, 560
    sg = 30 + 200 * sag
    for y0 in (wy - 150, wy + 150):
        p = skia.Path()
        p.moveTo(wx, y0)
        p.quadTo((wx + tx) / 2, (y0 + ty) / 2 + sg, tx, ty + (y0 - wy) * 0.2)
        c.drawPath(p, P("#111827", 1, stroke=10))
    tower(c, 1050, 1000, ty + 10)
    if slip > 0:                                       # slip marks on the wheel
        for k in range(4):
            ang = t * 7 + k * 1.57
            sx, sy = wx + math.cos(ang) * 150, wy + math.sin(ang) * 150
            add_glow(c, sx, sy, 34, "#FB923C", 0.6 * slip)
    if heat > 0:
        thermo(c, 160, 560, 260, 0.4 + 0.5 * heat, a=heat)
    if weight > 0:                                     # the counterweight in its pit, a rope over a pulley to the carriage
        c.drawRect(R(560, 1000, 300, 240), P("#1F2937", weight))
        px, py = 700, 860
        c.drawCircle(px, py, 30, P("#94A3B8", weight, stroke=10))
        c.drawLine(wx + 120, 860, px - 30, 860, P("#111827", weight, stroke=8))
        bot = lerp(1020, 1150, smooth(weight))
        c.drawLine(px + 30, 860, px + 30, bot, P("#111827", weight, stroke=8))
        c.drawRRect(rr(px - 60, bot, 180, 90, 10), lin_paint(0, bot, 0, bot + 90, ["#D6D3CE", "#8C8780"], a=weight))
        for j in range(3):
            c.drawLine(px - 50 + j * 60, bot + 10, px - 30 + j * 60, bot + 80, P("#6B6660", 0.6 * weight, stroke=3))


def thermo(c, x, y, h, frac, a=1.0):
    if a <= 0:
        return
    c.drawRRect(rr(x - 26, y - h, 52, h, 26), P("#F8FAFC", 0.95 * a))
    c.drawRRect(rr(x - 26, y - h, 52, h, 26), P("#0F172A", a, stroke=6))
    hh = (h - 60) * clamp(frac)
    c.drawRRect(rr(x - 12, y - 30 - hh, 24, hh + 10, 12), P(WARN, a))
    c.drawCircle(x, y, 40, P(WARN, a))
    c.drawCircle(x, y, 40, P("#0F172A", a, stroke=6))


# ====================================================================================== the banana port
def bananas(c, x, y, s, a=1.0):
    if a <= 0:
        return
    for k in range(7):
        ang = -60 + k * 20
        c.save()
        c.translate(x, y + 20 * s)
        c.rotate(ang)
        p = skia.Path()
        p.moveTo(0, 0)
        p.quadTo(26 * s, 40 * s, 6 * s, 86 * s)
        p.quadTo(-6 * s, 44 * s, 0, 0)
        c.drawPath(p, lin_paint(0, 0, 0, 86 * s, ["#A3E635", "#FACC15", "#EAB308"], a=a))
        c.restore()
    c.drawLine(x, y - 10 * s, x, y + 30 * s, P("#713F12", a, stroke=8 * s))


def port(c, t, swap=0.0, snowy=0.0):
    vrect(c, 0, 0, W, H, [mix("#2C6E8F", "#1E3A6E", snowy), mix("#79C2C9", "#6D5A9C", snowy), mix("#F6D48C", "#F0A3A0", snowy)],
          [0, 0.6, 1])
    c.drawRect(R(0, 980, W, 280), P(mix("#1F6E8C", "#E3EAF4", snowy)))     # the sea (or snow)
    if snowy < 1:
        for k in range(10):
            xx = (k * 120 + t * 20) % W
            c.drawLine(xx, 1010 + (k % 3) * 40, xx + 50, 1010 + (k % 3) * 40, P("#BAE6FD", 0.6 * (1 - snowy), stroke=4))
    # the dock and a palm
    c.drawRect(R(0, 940, 360, 50), P("#7C5A3C"))
    for px in (40, 150, 260):
        c.drawRect(R(px, 990, 18, 150), P("#5B3A22"))
    c.drawLine(120, 940, 140, 660, P("#7C5A3C", 1 - snowy, stroke=16))
    for j in range(7):
        ang = -2.9 + j * 0.45
        c.drawLine(140, 660, 140 + math.cos(ang) * 120, 660 + math.sin(ang) * 60 + 30, P("#3F7A3A", 1 - snowy, stroke=12))
    # the ship on the right
    hull = skia.Path()
    hull.moveTo(640, 760)
    hull.lineTo(1120, 760)
    hull.lineTo(1120, 1020)
    hull.lineTo(700, 1020)
    hull.close()
    c.drawPath(hull, lin_paint(0, 760, 0, 1020, ["#7F1D1D", "#450A0A"], a=1 - snowy))
    c.drawRect(R(760, 640, 120, 120), P("#E5E7EB", 1 - snowy))
    c.drawRect(R(800, 560, 30, 80), P("#111827", 1 - snowy))
    # the conveyor cable from the dock up into the hold
    p0, p1 = (60, 900), (900, 640)
    c.drawLine(p0[0], p0[1], p1[0], p1[1], P("#1F2937", 1, stroke=6))
    for k in range(6):
        u = (k / 6 + t * 0.05) % 1.0
        x, y = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
        c.drawLine(x, y, x, y + 40, P("#374151", 1, stroke=5))
        sk = clamp(swap * 6 - (5 - k))                 # one by one, the hooks carry chairs instead
        if sk < 1:
            bananas(c, x, y + 40, 0.9, a=1 - sk)
        if sk > 0:
            chair(c, x, y, 0.5, t, riders=0, a=sk, seed=k)


# ====================================================================================== the tags
def glove_tag(c, t, drop=0.0):
    mountains(c, t, 0.0)
    c.drawRect(R(0, 0, W, H), P("#0B1020", 0.15))
    chair(c, 420, 470, 2.4, t, riders=1, seed=2)
    if drop > 0:                                       # the glove tumbling down into the snow
        y = lerp(940, 1170, e_in(clamp(drop)))
        x = 600 + 60 * drop
        c.save()
        c.translate(x, y)
        c.rotate(drop * 400)
        c.drawRRect(rr(-30, -22, 60, 44, 16), P("#EF4444"))
        c.drawRRect(rr(-44, -30, 22, 26, 10), P("#EF4444"))
        c.restore()
        if drop >= 1:
            v2.puff(c, x, 1180, 40, "#F8FAFC", 0.8)


def buffet_tag(c, t, wait=0.0):
    vrect(c, 0, 0, W, H, ["#3B1D4A", "#5B2A58"])
    for k in range(9):                                 # string lights
        add_glow(c, 60 + k * 120, 360 + 30 * math.sin(k), 40, "#FDE68A", 0.7)
        c.drawCircle(60 + k * 120, 360 + 30 * math.sin(k), 8, P("#FEF3C7"))
    c.drawRRect(rr(620, 640, 440, 70, 14), P("#F8FAFC"))                    # the buffet table with big rice trays
    c.drawRect(R(640, 710, 400, 240), P("#E5E7EB"))
    for k, cx in enumerate((700, 840, 980)):
        c.drawOval(R(cx - 64, 600, 128, 60), P("#B45309"))
        c.drawOval(R(cx - 52, 586, 104, 40), P("#F59E0B"))
        for j in range(3):
            v2.puff(c, cx - 20 + j * 20, 560 - (t * 30 + j * 10) % 60, 14, "#F8FAFC", 0.3)
    xs = (520, 420, 320, 220, 120, 20)
    for k, x in enumerate(xs):                         # the line that never moves
        shirt = "#F8FAFC" if k % 2 == 0 else "#E5E7EB"
        person(c, x, 1180, 360, shirt, t + k * 0.3, pose="stand" if k else "look", face=1, hair="#111827", skin=SKIN[k % 4])
        c.drawOval(R(x + 10, 1180 - 250, 60, 16), P("#F8FAFC"))               # an empty plate
    clock_a = prog(wait, 0.0, 0.2)
    if clock_a > 0:
        c.drawCircle(860, 1050, 90, P("#F8FAFC", clock_a))
        c.drawCircle(860, 1050, 90, P("#111827", clock_a, stroke=8))
        ang = -math.pi / 2 + t * 6
        c.drawLine(860, 1050, 860 + math.cos(ang) * 70, 1050 + math.sin(ang) * 70, P("#DC2626", clock_a, stroke=8))
        c.drawLine(860, 1050, 860, 990, P("#111827", clock_a, stroke=10))


class Chairlift(EpisodeV2):
    BUILD_NO = 107
    FIRST_SET = "mountain"
    CLEAR = "#0B1020"
    COVER_T = ("closer", 0.55)
    TITLE = {"en": "HIGH-SPEED CHAIRLIFT", "ar_sa": "تلفريك الكراسي"}
    EMPH = {"en": ["CHAIRS", "LET", "GO", "CABLE", "PURPOSE", "FAST", "BIKE", "WHO", "HUNG", "ROPE", "STATION", "GRIP",
                   "OPENS", "ROLLS", "ZOOMING", "KNOCK", "FLAT", "SPINNING", "TIRES", "WALK", "SPEED", "LOOSE", "SLIDES",
                   "SPRINGS", "SQUEEZE", "WEAK", "STOPS", "WHOLE", "STEEL", "LONGER", "HEAT", "SLIPS", "GIANT",
                   "CONCRETE", "WEIGHT", "TIGHT", "FOLLOW", "ICE", "HOT", "BATH", "RAILROAD", "ENGINEER", "BANANA",
                   "LOADERS", "HOOKS", "NINETEEN", "THIRTY-SIX", "THOUSAND", "FEET", "MINUTE", "CONGRATS", "YOURSELF",
                   "NEVER", "GLOVE", "HALFWAY"],
            "ar_sa": ["هالكراسي", "تفك", "الكيبل", "قصد", "سريع", "السيكل", "مين", "حبل", "المحطة", "الماسكة", "تنفك",
                      "يطلع", "مسرع", "بيطيحك", "كفرات", "يمشي", "تسرعه", "يزحلق", "سوست", "تقفلها", "ضعيفة", "يوقف",
                      "الحديد", "يطول", "الحر", "المرتخي", "ثقل", "خرسانة", "مشدود", "متابعة", "الثلج", "حارة", "مهندس",
                      "سكة", "موز", "خطاطيف", "كراسي", "وثلاثين", "متر", "بالدقيقة", "مبروك", "يشيل", "بالساعة", "طابور",
                      "البوفيه", "العرس"]}
    KEYS = {"ar_sa": {
        ("hook", "CHAIRS"): "كراسي", ("hook", "CABLE"): "الكيبل", ("hook", "PURPOSE"): "قصد",
        ("break1", "FAST"): "سريع", ("break1", "BIKE"): "السيكل", ("break1", "WHO"): "مين", ("break1", "ROPE"): "حبل",
        ("fix1", "STATION"): "المحطة", ("fix1", "GRIP"): "الماسكة", ("fix1", "ROLLS"): "يطلع",
        ("break2", "ZOOMING"): "مسرع", ("break2", "KNOCK"): "وجهك",
        ("fix2", "TIRES"): "كفرات", ("fix2", "WALK"): "يمشي", ("fix2", "SPEED"): "وبعدين",
        ("break3", "LOOSE"): "الماسكة", ("break3", "SLIDES"): "يزحلق",
        ("fix3", "SPRINGS"): "سوست", ("fix3", "SHUT"): "تقفلها", ("fix3", "WEAK"): "ضعيفة", ("fix3", "STOPS"): "يوقف",
        ("break4", "STEEL"): "الحديد", ("break4", "LONGER"): "يطول", ("break4", "HEAT"): "الحر", ("break4", "SLIPS"): "يزحلق",
        ("fix4", "CONCRETE"): "خرسانة", ("fix4", "WEIGHT"): "ثقل", ("fix4", "TIGHT"): "مشدود",
        ("cta", "FOLLOW"): "متابعة", ("cta", "ICE"): "الثلج",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "RAILROAD"): "سكة", ("reveal", "BANANA"): "موز",
        ("reveal", "HOOKS"): "خطاطيف", ("reveal", "CHAIRS"): "كراسي",
        ("stat", "NINETEEN"): "ألف", ("stat", "BANANA"): "موز", ("stat", "THOUSAND"): "متر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "GRIP"): "يشيل", ("tag", "SLIPS"): "بالساعة", ("tag", "GLOVE"): "العرس"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: ice that gets a hot bath"),
                   "stat": [("1936", "FIRST CHAIRLIFT"), ("1", "BANANA IDEA"), ("1,000", "FEET A MINUTE")],
                   "L": {"letgo": "IT LETS GO!", "bike": "AS FAST AS A BIKE!", "who": "WHO HUNG CHAIRS ON A ROPE?",
                         "opens": "THE GRIP OPENS", "rail": "IT ROLLS OFF ONTO A RAIL", "zoom": "STILL ZOOMING!",
                         "tires": "SPINNING TIRES", "walk": "SLOW AS A WALK", "loose": "A LOOSE GRIP!",
                         "slides": "IT SLIDES BACK!", "springs": "SPRINGS SQUEEZE IT SHUT", "test": "EVERY GRIP TESTED",
                         "weak": "ONE WEAK GRIP = STOP", "heat": "STEEL GETS LONGER", "slip": "IT SLIPS!",
                         "weight": "A GIANT CONCRETE WEIGHT", "tight": "PULLED TIGHT", "banana": "BANANA LOADERS",
                         "swap": "HOOKS → CHAIRS", "name": "HIGH-SPEED CHAIRLIFT", "glove": "MY GLOVE!",
                         "kmh": "KM/H"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: ثلج يتسبّح بموية حارة"),
                      "stat": [("1936", "أول تلفريك كراسي"), ("1", "فكرة موز"), ("300", "متر بالدقيقة")],
                      "L": {"letgo": "يفك الكيبل!", "bike": "سريع مثل السيكل!", "who": "مين أول من علّق كراسي؟",
                            "opens": "الماسكة تنفك", "rail": "يطلع على سكة", "zoom": "للحين مسرع!",
                            "tires": "كفرات تدور", "walk": "يمشي على هونه", "loose": "ماسكة مرتخية!",
                            "slides": "يزحلق لورا!", "springs": "سوست تقفلها", "test": "كل ماسكة تنفحص",
                            "weak": "وحدة ضعيفة = وقوف", "heat": "الحديد يطوّل في الحر", "slip": "يزحلق!",
                            "weight": "ثقل خرسانة عملاق", "tight": "مشدود", "banana": "رافعات موز",
                            "swap": "خطاطيف ← كراسي", "name": "تلفريك الكراسي السريع", "glove": "الطابور واقف!",
                            "kmh": "كم/س"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "chairs": ("hook", "CHAIRS", 0.3), "cable0": ("hook", "CABLE", 0.6), "purpose": ("hook", "PURPOSE", 0.9),
            "fast": ("break1", "FAST", 0.25), "bike": ("break1", "BIKE", 0.45), "who": ("break1", "WHO", 0.7),
            "rope": ("break1", "ROPE", 0.95),
            "station": ("fix1", "STATION", 0.2), "grip": ("fix1", "GRIP", 0.5), "rolls": ("fix1", "ROLLS", 0.85),
            "zoom": ("break2", "ZOOMING", 0.4), "knock": ("break2", "KNOCK", 0.75),
            "tires": ("fix2", "TIRES", 0.25), "walk": ("fix2", "WALK", 0.55), "speed": ("fix2", "SPEED", 0.85),
            "loose": ("break3", "LOOSE", 0.25), "slides": ("break3", "SLIDES", 0.7),
            "springs": ("fix3", "SPRINGS", 0.15), "shut": ("fix3", "SHUT", 0.4), "weak": ("fix3", "WEAK", 0.65),
            "stops": ("fix3", "STOPS", 0.85),
            "steel": ("break4", "STEEL", 0.15), "longer": ("break4", "LONGER", 0.4), "heat": ("break4", "HEAT", 0.6),
            "slips": ("break4", "SLIPS", 0.9),
            "concrete": ("fix4", "CONCRETE", 0.3), "weight": ("fix4", "WEIGHT", 0.5), "tight": ("fix4", "TIGHT", 0.9),
            "follow": ("cta", "FOLLOW", 0.1), "ice": ("cta", "ICE", 0.7),
            "answer": ("reveal", "ANSWER", 0.05), "railroad": ("reveal", "RAILROAD", 0.2), "banana": ("reveal", "BANANA", 0.45),
            "hooks": ("reveal", "HOOKS", 0.75), "chairs2": ("reveal", "CHAIRS", 0.9),
            "s1": ("stat", "NINETEEN", 0.05), "s2": ("stat", "BANANA", 0.4), "s3": ("stat", "THOUSAND", 0.7),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_grip": ("tag", "GRIP", 0.15), "t_slips": ("tag", "SLIPS", 0.35), "t_glove": ("tag", "GLOVE", 0.8)})
        T["fast1"] = max(T["fast"], s("break1") + 0.3)
        T["rolls1"] = max(T["rolls"], T["grip"] + 0.3)
        T["knock1"] = max(T["knock"], T["zoom"] + 0.3)
        T["walk1"] = max(T["walk"], T["tires"] + 0.3)
        T["slide1"] = max(T["slides"], T["loose"] + 0.3)
        T["shut1"] = max(T["shut"], T["springs"] + 0.3)
        T["slip1"] = max(T["slips"], T["heat"] + 0.3)
        T["tight1"] = max(T["tight"], T["weight"] + 0.3)
        # ---- sets
        self.cut(s("break1") - 0.12, "station", 1)
        self.cut(s("break3") - 0.12, "slope", -1)
        self.cut(s("break4") - 0.12, "terminal", 1)
        self.cut(s("cta") - 0.12, "mountain", -1)
        self.cut(s("reveal") - 0.12, "port", 1)
        self.cut(s("stat") - 0.12, "mountain", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        self.spans = [(T["fast1"], T["rolls1"]), (T["knock1"], T["walk1"]), (T["slide1"], T["shut1"]), (T["slip1"], T["tight1"])]
        self.shakes = [(T["cable0"], 0.3, 4), (T["knock1"], 0.5, 12), (T["slide1"] + 0.3, 0.5, 10), (T["stops"], 0.3, 6),
                       (T["slip1"], 0.4, 6), (T["weight"], 0.4, 8), (s("closer") + 0.2, 0.35, 6), (T["t_glove"], 0.3, 5)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: mountain (hook, cta, stat, closer)
    def draw_mountain(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            k = e_io(prog(t, T["purpose"] - 0.3, s("break1") - 0.2))
            z = lerp(2.6, 1.0, k)
            fx, fy = lerp(960, 540, k), lerp(520, 820, k)
            c.save()
            c.translate(540, 760)
            c.scale(z, z)
            c.translate(-fx, -fy)
            mountains(c, t, 0.0)
            lift_line(c, t, detach=prog(t, T["chairs"] - 0.6, T["purpose"] + 0.4))
            c.restore()
        elif ph == "closer":
            mountains(c, t, 1.0)
            lift_line(c, t, night=1.0, lit=1.0)
        else:
            night = prog(t, s("stat"), s("stat") + 1.2) * 0.5 if ph == "stat" else 0.0
            mountains(c, t, night)
            lift_line(c, t, night=night)

    def ui_mountain(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "letgo", T["cable0"] - 0.1, s("break1") + 0.1, accent=HILITE, size=60)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=50)

    # ------------------------------------------------------------------ set: station (break1 .. fix2)
    def draw_station(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break1":                             # a chair rides the fast cable, a cyclist keeps pace
            u = prog(t, s("break1") - 0.1, s("fix1") - 0.1)
            x = lerp(-120, 1260, u)
            station(c, t, chair_x=x, riders=2, bike_x=x - 40 if t >= T["bike"] - 0.6 else None)
            speedo(c, 880, 800, 18 * prog(t, T["fast"] - 0.4, T["fast"] + 0.2), a=prog(t, T["fast"] - 0.4, T["fast"]))
        elif ph == "fix1":                             # the grip opens at the station and the chair rolls onto the rail
            u = prog(t, s("fix1") - 0.1, T["rolls"] + 0.4)
            x = lerp(80, 470, e_out(u))
            station(c, t, chair_x=x, open_=prog(t, T["grip"] - 0.2, T["grip"] + 0.2),
                    on_rail=prog(t, T["grip"], T["rolls"]))
        elif ph == "break2":                           # still fast: it knocks the waiting skier flat
            u = prog(t, s("break2") - 0.1, T["knock1"])
            x = lerp(470, 700, e_in(u))
            station(c, t, chair_x=x, open_=1.0, on_rail=1.0, fall=prog(t, T["knock1"], T["knock1"] + 0.6))
        else:                                          # tyres slow it, the skier sits, then it speeds up and grips again
            slow = prog(t, T["tires"] - 0.2, T["walk"])
            x = lerp(440, 700, e_out(slow))
            sit = prog(t, T["walk"] - 0.2, T["walk"] + 0.4)
            go = prog(t, T["speed"] - 0.1, s("break3") - 0.1)
            x = x + 500 * e_in(go)
            on_rail = 1.0 - prog(t, T["speed"] + 0.2, T["speed"] + 0.6)
            station(c, t, chair_x=x, open_=on_rail, on_rail=on_rail, tire_a=prog(t, T["tires"] - 0.3, T["tires"]),
                    sit=sit, skier_a=1.0 - sit, riders=1 if sit >= 1 else 0)
            speedo(c, 880, 800, lerp(18, 4, slow) + 14 * go, a=prog(t, T["tires"] - 0.2, T["tires"] + 0.2))

    def ui_station(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "bike", T["fast"] - 0.1, T["who"] - 0.1, accent=WARN, size=56)
            self.chip(540, 300, "who", T["who"] - 0.1, s("fix1") - 0.1, accent=HILITE, size=44)
            self.badge("alert", T["fast1"], s("fix1") - 0.2, x=160, y=470)
            self.red(T["fast1"], 1.2)
        elif ph == "fix1":
            self.chip(540, 300, "opens", T["station"] - 0.1, T["rolls"] - 0.2, accent=GOOD, size=56)
            self.chip(540, 300, "rail", T["rolls"] - 0.2, s("break2") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["rolls1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "zoom", T["zoom"] - 0.2, s("fix2") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["knock1"], s("fix2") - 0.2, x=160, y=470)
            self.red(T["knock1"], 1.2)
        else:
            self.chip(540, 300, "tires", T["tires"] - 0.2, T["walk"] - 0.1, accent="#FDE68A", size=56)
            self.chip(540, 300, "walk", T["walk"] - 0.1, s("break3") - 0.15, accent=GOOD, size=56)
            self.badge("check", T["walk1"], s("break3") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: slope (break3, fix3)
    def draw_slope(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break3":
            slope_scene(c, t, slide=prog(t, T["loose"] + 0.2, T["slide1"] + 0.4))
        else:
            weak = prog(t, T["weak"] - 0.2, T["weak"] + 0.1)
            grip_closeup(c, t, squeeze=prog(t, T["springs"] - 0.2, T["shut"]) if t < T["weak"] - 0.2 else 1.0 - 0.3 * weak,
                         test=prog(t, T["shut"], T["shut"] + 0.3), weak=weak, stop=prog(t, T["stops"] - 0.1, T["stops"] + 0.3))

    def ui_slope(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break3":
            self.chip(540, 300, "loose", T["loose"] - 0.2, T["slides"] - 0.1, accent=WARN, size=58)
            self.chip(540, 300, "slides", T["slides"] - 0.1, s("fix3") - 0.15, accent=WARN, size=58)
            self.badge("alert", T["slide1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["slide1"], 1.2)
        else:
            self.chip(540, 300, "springs", T["springs"] - 0.1, T["weak"] - 0.2, accent=GOOD, size=50)
            self.chip(540, 300, "weak", T["weak"] - 0.2, s("break4") - 0.15, accent=WARN, size=50)
            self.badge("check", T["shut1"], s("break4") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: terminal (break4, fix4)
    def draw_terminal(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break4":
            heat = prog(t, T["steel"] - 0.2, T["heat"])
            terminal(c, t, heat=heat, sag=prog(t, T["longer"] - 0.2, T["heat"] + 0.3), slip=prog(t, T["slip1"], T["slip1"] + 0.3),
                     run=0.2 if t > T["slip1"] else 1.0)
        else:
            w = prog(t, T["concrete"] - 0.3, T["tight"])
            terminal(c, t, heat=1.0 - prog(t, s("fix4"), s("fix4") + 0.6), sag=1.0 - w, slip=1.0 - prog(t, s("fix4"), T["weight"]),
                     weight=w)

    def ui_terminal(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "heat", T["steel"] - 0.1, T["slips"] - 0.2, accent=WARN, size=54)
            self.chip(540, 300, "slip", T["slips"] - 0.2, s("fix4") - 0.15, accent=WARN, size=62)
            self.badge("alert", T["slip1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["slip1"], 1.2)
        else:
            self.chip(540, 300, "weight", T["concrete"] - 0.2, T["tight"] - 0.2, accent="#E5E7EB", size=50)
            self.chip(540, 300, "tight", T["tight"] - 0.2, s("cta") - 0.15, accent=GOOD, size=60)
            self.badge("check", T["tight1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: port (reveal)
    def draw_port(self, c, t):
        T, s = self.T, self.tl.s
        port(c, t, swap=prog(t, T["hooks"] - 0.2, T["chairs2"] + 0.8), snowy=prog(t, T["chairs2"], T["chairs2"] + 1.2))

    def ui_port(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "banana", T["banana"] - 0.2, T["hooks"] - 0.2, accent="#FACC15", size=56)
        self.chip(540, 300, "swap", T["hooks"] - 0.2, s("stat") - 0.15, accent=HILITE, size=56)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:
            glove_tag(c, t, drop=prog(t, T["t_slips"] + 0.3, T["t_glove"] + 0.2))
        else:
            buffet_tag(c, t, wait=prog(t, T["t_slips"], T["t_glove"]))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "glove", T["t_glove"] - 0.1, self.duration + 1, accent=WARN, size=58)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#111827", "#1F2937"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.whirr(3.0, 90.0, 110.0, 60), -20),
              (T["cable0"], sfx.lock_click(62), -4), (T["purpose"], sfx.ding(), -8)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 63), -6), (T["fast"], sfx.whirr(1.4, 180.0, 260.0, 64), -10),
               (T["bike"], sfx.ring(0.6), -14), (T["fast1"] + 0.5, sfx.alarm(3, 820.0), -14)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.45, False, 65), -6), (T["grip"], sfx.lock_click(66), -4),
               (T["rolls1"], sfx.ding(), -8), (T["rolls1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["zoom"], sfx.whoosh(0.6, True, 67), -8), (T["knock1"], sfx.thud(0.4, 68), -4), (T["knock1"], sfx.womp(), -8),
               (T["knock1"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(T["tires"], sfx.whirr(1.2, 220.0, 120.0, 69), -10), (T["walk1"], sfx.ding(), -8),
               (T["walk1"] + 0.2, sfx.chime(), -6), (T["speed"] + 0.4, sfx.lock_click(70), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.45, True, 71), -6), (T["slide1"], sfx.creak(1.0, 72), -8),
               (T["slide1"] + 0.6, sfx.clank(300.0, 0.7, 73), -6), (T["slide1"] + 0.6, sfx.alarm(3, 820.0), -12)]
        ev += [(T["springs"], sfx.snap(74), -6), (T["shut1"], sfx.ding(), -8), (T["shut1"] + 0.2, sfx.chime(), -6),
               (T["stops"], sfx.buzz(0.5), -10)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 75), -6), (T["heat"], sfx.creak(1.0, 76), -10),
               (T["slip1"], sfx.sizzle(0.8, 77), -10),
               (T["slip1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(T["concrete"], sfx.thunk(78), -6), (T["weight"], rumble(1.0, 79), -12), (T["tight1"], sfx.ding(), -8),
               (T["tight1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["banana"], sfx.pop(95), -6),
               (T["hooks"], sfx.sparkle(1.2, 12, 96), -8), (T["chairs2"], sfx.ding(), -6)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 103), -6), (T["t_glove"], sfx.womp(), -8)]
        return ev


NAME = "chairlift"
EPISODE = Chairlift
