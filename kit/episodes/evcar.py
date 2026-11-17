"""Episode 34 - An electric car.  v2 look: a city street at dusk, side view, plus an x-ray of the car, a top view of a
zebra crossing, a garage at night and the tag.

Sets: street (the hook: the hood opens on a trunk full of groceries, then the light turns green and the car beats a red
sports car; the stat and the closer), xray (the car turns see-through: a heavy battery on the roof makes it lean, then
eight thousand cells lie flat under the floor; a gas engine with pistons and a gearbox, then an electric motor at the
rear axle; braking turns speed into heat, then regenerative braking sends energy back to the battery), cross (top view:
a pedestrian can't hear the silent car, then it plays a sound below 20 km/h), garage (plugged in at night, full in the
morning), uncle (the tag: the uncle opens the hood to check the oil and finds the groceries).
World (street, xray, garage, uncle): side view, the road surface is y = 0, the car faces right and stays near x = 0
while the ground scrolls.
"""
from v2_base import *  # noqa: F401,F403

PEARL = "#E8EEF5"
TEAL = "#14B8A6"
RED = "#DC2626"
ASPHALT = ("#2B2F3E", "#1E2130", "#141623", "#0B0C14")
DUSK = {"top": "#070A22", "upper": "#14194A", "mid": "#3A2C6E", "low": "#9B4A72", "horizon": "#F08A5D",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
WR = 64.0                     # wheel radius
WB = 300.0                    # half wheelbase


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


class Run:
    """Distance from a Track of speed (units per second), integrated."""

    def __init__(self, track, t_end, dt=1 / 60.0):
        n = int(t_end / dt) + 3
        self.dt = dt
        self.d = np.zeros(n)
        acc = 0.0
        for i in range(1, n):
            acc += track.at((i - 0.5) * dt) * dt
            self.d[i] = acc

    def at(self, t):
        i = clamp(t / self.dt, 0, len(self.d) - 2.001)
        i0 = int(i)
        return float(self.d[i0] + (self.d[i0 + 1] - self.d[i0]) * (i - i0))


def wheel(c, x, y, rot, r=WR, glow=0.0, a=1.0, rim="#CBD5E1"):
    c.drawCircle(x, y, r, P("#0B0F1A", a))
    c.drawCircle(x, y, r * 0.62, P("#1F2937", a))
    if glow > 0:
        c.drawCircle(x, y, r * 0.5, P(mix("#7C2D12", "#FF8A3D", glow), a * glow))
        add_glow(c, x, y, r * 1.7, "#FF6A2B", 0.85 * glow * a)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    for i in range(5):
        c.save()
        c.rotate(i * 72)
        c.drawRRect(rr(6, -5, r * 0.52, 10, 4), P(rim, a))
        c.restore()
    c.restore()
    c.drawCircle(x, y, r * 0.62, P("#E5E9F2", a * 0.8, stroke=4))
    c.drawCircle(x, y, 9, P("#94A3B8", a))


def _ev_body():
    p = skia.Path()
    p.moveTo(-470, -62)
    p.lineTo(-478, -165)
    p.quadTo(-474, -214, -420, -224)
    p.lineTo(-310, -236)
    p.cubicTo(-240, -300, -150, -336, -60, -339)
    p.lineTo(50, -336)
    p.cubicTo(130, -330, 185, -262, 232, -228)
    p.lineTo(420, -206)
    p.quadTo(474, -196, 482, -140)
    p.lineTo(476, -62)
    p.close()
    return p


def _ev_glass():
    p = skia.Path()
    p.moveTo(-292, -240)
    p.cubicTo(-230, -296, -150, -322, -60, -324)
    p.lineTo(48, -321)
    p.cubicTo(120, -315, 168, -262, 206, -238)
    p.close()
    return p


def _hood():
    p = skia.Path()
    p.moveTo(234, -228)
    p.lineTo(420, -206)
    p.quadTo(474, -196, 482, -150)
    p.lineTo(470, -150)
    p.quadTo(462, -186, 418, -192)
    p.lineTo(234, -212)
    p.close()
    return p


def groceries(c, x, y, s=1.0, a=1.0, rise=0.0):
    """A paper grocery bag with a baguette, greens and an orange (feet at x, y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y - rise)
    c.scale(s, s)
    c.save()
    c.rotate(-18)
    c.drawRRect(rr(-14, -150, 30, 120, 14), lin_paint(-14, 0, 16, 0, ["#E9B872", "#C98A3E"], a=a))
    for k in range(3):
        c.drawLine(-8, -130 + k * 30, 10, -138 + k * 30, P("#8A5A22", a, stroke=3))
    c.restore()
    for i, (lx, ang) in enumerate(((10, -10), (30, 12), (46, -4))):
        c.save()
        c.translate(lx, -96)
        c.rotate(ang)
        lf = skia.Path()
        lf.moveTo(0, 0)
        lf.cubicTo(-16, -30, -6, -60, 0, -72)
        lf.cubicTo(8, -60, 16, -30, 0, 0)
        c.drawPath(lf, P(("#22C55E", "#16A34A", "#4ADE80")[i], a))
        c.restore()
    c.drawCircle(60, -100, 20, P("#FB923C", a))
    c.drawCircle(54, -106, 6, P("#FED7AA", a * 0.8))
    bag = skia.Path()
    bag.moveTo(-36, -104)
    bag.lineTo(74, -104)
    bag.lineTo(82, 0)
    bag.lineTo(-44, 0)
    bag.close()
    c.drawPath(bag, lin_paint(-44, 0, 82, 0, ["#B7834B", "#D9A86C", "#A8743E"], a=a))
    c.drawLine(-36, -104, 74, -104, P("#7C5427", a, stroke=5))
    c.restore()


def ev_side(c, x, y, s, rot, t, hood=0.0, xray=0.0, lean=0.0, squat=0.0, glow=0.0, lights=1.0, a=1.0, port=0.0,
            bag=1.0):
    """The electric car from the side, facing right, wheels on (x, y).  hood 0..1 opens the front trunk,
    xray 0..1 makes the body see-through (the parts are drawn by the scene), lean = degrees (top-heavy wobble)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    contact_shadow(c, 0, 2, 1000, 0.5 * a)
    for wx in (-WB, WB):
        wheel(c, wx, -WR, rot, glow=glow, a=a)
    c.save()
    c.translate(0, squat * 18)
    c.rotate(lean)
    body = _ev_body()
    k = 1 - xray
    if k > 0:
        c.drawPath(body, lin_paint(0, -340, 0, -62, [shade(PEARL, 0.12), PEARL, shade(PEARL, -0.18), shade(PEARL, -0.38)],
                                   [0, 0.35, 0.75, 1], a=a * k))
        c.drawPath(_ev_glass(), lin_paint(0, -330, 0, -240, ["#7DD3FC", "#1E3A5F"], a=a * k))
        c.drawRect(R(-48, -326, 14, 90), P(shade(PEARL, -0.1), a * k))                       # the pillar
        c.drawLine(-440, -150, 450, -150, P(TEAL, a * k * 0.9, stroke=6))                     # teal stripe
        for wx in (-WB, WB):                                                                  # wheel arches
            c.drawArc(R(wx - WR - 12, -WR - WR - 12, (WR + 12) * 2, (WR + 12) * 2), 180, 180, False,
                      P("#0F172A", a * k, stroke=10))
        c.drawRRect(rr(-80, -196, 40, 8, 4), P("#94A3B8", a * k))                            # door handles
        c.drawRRect(rr(-280, -196, 40, 8, 4), P("#94A3B8", a * k))
    if xray > 0:
        c.drawPath(body, P("#38BDF8", 0.12 * a * xray))
        c.drawPath(body, P("#7DD3FC", 0.9 * a * xray, stroke=5))
        c.drawPath(_ev_glass(), P("#7DD3FC", 0.5 * a * xray, stroke=3))
    if lights > 0:
        c.drawRRect(rr(452, -176, 30, 18, 8), P("#F8FAFC", a))
        add_glow(c, 490, -168, 70, "#E0F2FE", 0.55 * lights * a)
        c.drawRRect(rr(-482, -186, 18, 26, 6), P("#EF4444", a))
        add_glow(c, -486, -172, 50, "#EF4444", 0.4 * lights * a)
    if port > 0:                                                                              # charge port flap
        c.drawRRect(rr(-440, -216, 46, 34, 8), P("#0F172A", a))
        add_glow(c, -417, -199, 40, "#22C55E", 0.6 * port * a)
    if hood > 0:
        c.drawRect(R(236, -222, 236, 96), P("#0F172A", a))                                   # the front trunk
        if bag > 0:
            groceries(c, 330, -130, 0.8, a * bag, rise=hood * 30)
        c.save()
        c.translate(234, -220)
        c.rotate(-58 * e_out(clamp(hood)))
        c.translate(-234, 220)
        c.drawPath(_hood(), lin_paint(0, -228, 0, -150, [shade(PEARL, 0.15), shade(PEARL, -0.1)], a=a))
        c.drawPath(_hood(), P("#94A3B8", a, stroke=2))
        c.restore()
    c.restore()
    c.restore()


def sports_car(c, x, y, s, rot, a=1.0):
    """A low red sports car from the side, facing right."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    contact_shadow(c, 0, 2, 980, 0.45 * a)
    for wx in (-WB, WB):
        wheel(c, wx, -WR, rot, rim="#FDE68A", a=a)
    p = skia.Path()
    p.moveTo(-480, -70)
    p.lineTo(-470, -170)
    p.lineTo(-380, -190)
    p.cubicTo(-260, -200, -150, -270, -40, -272)
    p.cubicTo(60, -270, 120, -220, 200, -196)
    p.lineTo(440, -150)
    p.quadTo(492, -136, 490, -90)
    p.lineTo(486, -62)
    p.close()
    c.drawPath(p, lin_paint(0, -272, 0, -62, [shade(RED, 0.25), RED, shade(RED, -0.35)], a=a))
    g = skia.Path()
    g.moveTo(-250, -200)
    g.cubicTo(-170, -250, -110, -260, -40, -260)
    g.cubicTo(30, -258, 90, -228, 150, -200)
    g.close()
    c.drawPath(g, P("#0F172A", a))
    c.drawRect(R(-470, -214, 90, 14), P("#111827", a))                                       # spoiler
    c.drawRect(R(-440, -200, 12, 26), P("#111827", a))
    for wx in (-WB, WB):
        c.drawArc(R(wx - WR - 12, -WR - WR - 12, (WR + 12) * 2, (WR + 12) * 2), 180, 180, False, P("#450A0A", a, stroke=10))
    c.drawRRect(rr(452, -128, 34, 14, 7), P("#FEF3C7", a))
    c.restore()


def traffic_light(c, x, y, state, a=1.0):
    """Pole with three lamps; state 0 red, 1 green.  Feet at (x, y)."""
    c.drawRect(R(x - 9, y - 620, 18, 620), P("#334155", a))
    c.drawRRect(rr(x - 46, y - 860, 92, 250, 22), P("#111827", a))
    for i, (col, on) in enumerate((("#EF4444", state < 0.5), ("#F59E0B", False), ("#22C55E", state >= 0.5))):
        cy = y - 820 + i * 80
        c.drawCircle(x, cy, 30, P(col if on else shade(col, -0.7), a))
        if on:
            add_glow(c, x, cy, 120, col, 0.7 * a)


def cells(c, x0, x1, y, n, k, t, a=1.0, src=None):
    """A flat layer of n small cylindrical cells between x0 and x1 (tops at y); k 0..1 lays them in, flying from src."""
    w = (x1 - x0) / n
    for i in range(n):
        q = clamp(k * 1.6 - (i % 12) / 12.0 * 0.6)
        if q <= 0:
            continue
        tx, ty = x0 + (i + 0.5) * w, y
        if src is not None and q < 1:
            sx, sy = src[0] + ((i * 37) % 120 - 60), src[1] + ((i * 53) % 60 - 30)
            e = e_io(q)
            px = lerp(sx, tx, e)
            py = lerp(sy, ty, e) - math.sin(math.pi * e) * 160
        else:
            px, py = tx, ty
        col = ("#22C55E", "#16A34A")[i % 2]
        c.drawRRect(rr(px - w * 0.36, py, w * 0.72, 34, 5), P(col, a))
        c.drawRect(R(px - w * 0.2, py - 4, w * 0.4, 5), P("#D1FAE5", a))


def battery_block(c, x, y, w, h, a=1.0):
    """The big heavy battery (centre-bottom at x, y)."""
    if a <= 0:
        return
    c.drawRRect(rr(x - w / 2, y - h, w, h, 18), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#15803D", "#22C55E", "#166534"], a=a))
    c.drawRRect(rr(x - w / 2, y - h, w, h, 18), P("#052E16", a, stroke=6))
    bolt = skia.Path()
    bolt.moveTo(x + 10, y - h + 24)
    bolt.lineTo(x - 30, y - h / 2 + 6)
    bolt.lineTo(x - 2, y - h / 2 + 6)
    bolt.lineTo(x - 14, y - 22)
    bolt.lineTo(x + 30, y - h / 2 - 8)
    bolt.lineTo(x + 2, y - h / 2 - 8)
    bolt.close()
    c.drawPath(bolt, P("#FDE047", a))


def cg_mark(c, x, y, r=26, a=1.0):
    """Centre-of-gravity symbol."""
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#FFFFFF", a))
    for st in (0, 180):
        c.drawArc(R(x - r, y - r, 2 * r, 2 * r), st - 90, 90, True, P("#0F172A", a))
    c.drawCircle(x, y, r, P("#0F172A", a, stroke=4))


def gas_engine(c, x, y, t, run, a=1.0):
    """An engine block with four pumping pistons and sparks, and a gearbox behind it (centre-bottom at x, y)."""
    if a <= 0:
        return
    c.drawRRect(rr(x - 110, y - 120, 220, 120, 14), lin_paint(0, y - 120, 0, y, ["#9CA3AF", "#4B5563"], a=a))
    for i in range(4):
        px = x - 78 + i * 52
        ph = t * 14 * run + i * math.pi / 2
        py = y - 70 - math.sin(ph) * 22 * run
        c.drawRect(R(px - 18, y - 170, 36, 110), P("#1F2937", a))
        c.drawRRect(rr(px - 16, py - 34, 32, 30, 6), P("#E5E7EB", a))
        c.drawLine(px, py - 4, px + math.cos(ph) * 10, y - 30, P("#CBD5E1", a, stroke=6))
        if run > 0 and math.sin(ph) > 0.92:
            add_glow(c, px, y - 165, 60, "#FB923C", 0.9 * a)
            c.drawCircle(px, y - 165, 12, P("#FDE68A", a))
    for i, (gx, gy, r, sp) in enumerate(((x - 170, y - 50, 40, 1), (x - 230, y - 80, 28, -1.4))):
        c.save()
        c.translate(gx, gy)
        c.rotate(t * 200 * sp * run)
        for k in range(10):
            c.save()
            c.rotate(k * 36)
            c.drawRect(R(-6, -r - 10, 12, 14), P("#64748B", a))
            c.restore()
        c.drawCircle(0, 0, r, P("#94A3B8", a))
        c.drawCircle(0, 0, r * 0.3, P("#334155", a))
        c.restore()


def motor(c, x, y, r, ang, a=1.0, glow=0.0, rev=0.0):
    """Electric motor seen end-on: copper stator, rotor with four magnets (red N, blue S)."""
    if a <= 0:
        return
    c.drawCircle(x, y, r + 14, P("#334155", a))
    for k in range(12):
        an = math.radians(k * 30)
        c.drawCircle(x + math.cos(an) * (r + 2), y + math.sin(an) * (r + 2), 10, P("#D97706", a))
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    for k in range(4):
        c.drawArc(R(-r * 0.78, -r * 0.78, r * 1.56, r * 1.56), k * 90, 90, True, P(("#EF4444", "#3B82F6")[k % 2], a))
    c.drawCircle(0, 0, r * 0.25, P("#E5E7EB", a))
    c.restore()
    if glow > 0:
        add_glow(c, x, y, r * 2.4, "#FDE047" if rev > 0.5 else "#38BDF8", 0.55 * glow * a)


def dash_line(c, pts, t, col, a=1.0, w=10, speed=260.0, dash=34, gap=26):
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    pa = P(col, a, stroke=w)
    pa.setPathEffect(skia.DashPathEffect.Make([dash, gap], -(t * speed) % (dash + gap)))
    pa.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawPath(p, pa)


def pedal(c, x, y, lift, a=1.0):
    """A pedal and a shoe that lifts off it (screen space)."""
    if a <= 0:
        return
    c.drawRRect(rr(x - 120, y - 150, 240, 300, 40), P("#000000", 0.35 * a, blur=12))
    c.drawRRect(rr(x - 120, y - 150, 240, 300, 40), P("#1E293B", 0.95 * a))
    c.save()
    c.translate(x, y + 40)
    c.rotate(-20)
    c.drawRRect(rr(-50, -14, 100, 28, 10), P("#9CA3AF", a))
    c.restore()
    c.drawLine(x - 30, y + 60, x - 60, y + 130, P("#64748B", a, stroke=10))
    c.save()
    c.translate(x, y - 10 - lift * 70)
    c.rotate(-18)
    c.drawRRect(rr(-70, -26, 140, 52, 24), P("#F8FAFC", a))
    c.drawRRect(rr(-70, 14, 140, 14, 7), P("#E11D48", a))
    c.restore()


def battery_pill(c, x, y, pct, a=1.0, w=220):
    """Battery gauge (screen space): pct 0..100."""
    if a <= 0:
        return
    h = 76
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, 18), P("#000000", 0.35 * a, blur=10))
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, 18), P("#0F172A", 0.92 * a))
    c.drawRRect(rr(x - w / 2 + 12, y - h / 2 + 12, w - 50, h - 24, 10), P("#334155", a))
    k = clamp(pct / 100.0)
    col = mix("#F59E0B", "#22C55E", clamp((pct - 30) / 40))
    c.drawRRect(rr(x - w / 2 + 12, y - h / 2 + 12, (w - 50) * k, h - 24, 10), P(col, a))
    c.drawRRect(rr(x + w / 2 - 34, y - 14, 14, 28, 4), P("#334155", a))
    text(c, f"{pct:.0f}%", x - 12, y + 12, 34, "#FFFFFF", "Poppins-Black", a=a)


def speaker_waves(c, x, y, t, a=1.0, ang=0.0, n=3, col=HILITE, mute=0.0):
    """Sound waves going out from (x, y) toward the angle ang (degrees); mute draws a crossed speaker instead."""
    if a <= 0:
        return
    if mute > 0:
        c.save()
        c.translate(x, y)
        c.drawRRect(rr(-30, -20, 26, 40, 6), P("#E2E8F0", a * mute))
        sp = skia.Path()
        sp.moveTo(-6, -20)
        sp.lineTo(24, -44)
        sp.lineTo(24, 44)
        sp.lineTo(-6, 20)
        sp.close()
        c.drawPath(sp, P("#E2E8F0", a * mute))
        c.drawLine(36, -30, 80, 30, P(WARN, a * mute, stroke=10))
        c.drawLine(80, -30, 36, 30, P(WARN, a * mute, stroke=10))
        c.restore()
        return
    for i in range(n):
        q = (t * 1.6 + i / n) % 1.0
        r = 40 + q * 260
        c.drawArc(R(x - r, y - r, 2 * r, 2 * r), ang - 40, 80, False, P(col, a * (1 - q) * 0.95, stroke=10))


def ev_top(c, x, y, s, a=1.0, glow=0.0):
    """The car seen from above, nose pointing up the screen."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-128, -250, 256, 500, 90), P("#000000", 0.45 * a, blur=26))
    c.drawRRect(rr(-118, -240, 236, 480, 86), lin_paint(-118, 0, 118, 0, [shade(PEARL, -0.25), PEARL, shade(PEARL, -0.25)], a=a))
    c.drawRRect(rr(-92, -120, 184, 250, 50), lin_paint(0, -120, 0, 130, ["#7DD3FC", "#1E3A5F", "#0F172A"], a=a))
    c.drawRect(R(-118, -10, 236, 8), P(TEAL, a))
    for sx in (-1, 1):
        c.drawRRect(rr(sx * 70 - 22, -246, 44, 18, 8), P("#F8FAFC", a))
        c.drawRRect(rr(sx * 70 - 22, 230, 44, 14, 6), P("#EF4444", a))
        c.drawRRect(rr(sx * 118 - (12 if sx > 0 else 4), -60, 16, 30, 6), P(shade(PEARL, -0.3), a))
    if glow > 0:
        add_glow(c, 0, -300, 240, "#E0F2FE", 0.5 * glow * a)
    c.restore()


def walker_top(c, x, y, s, t, walk=1.0, look=0.0, a=1.0, wave=0.0):
    """A pedestrian seen from above, walking to the right, a phone in hand; look turns the head toward the car (down)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    ph = math.sin(t * 9) * walk
    c.drawOval(R(-30, -46, 60, 92), P("#000000", 0.35 * a, blur=8))
    c.drawRRect(rr(-12 + ph * 26, 14, 40, 18, 9), P("#1F2937", a))
    c.drawRRect(rr(-12 - ph * 26, -32, 40, 18, 9), P("#1F2937", a))
    c.drawOval(R(-30, -42, 52, 84), P("#7C3AED", a))
    c.drawCircle(4, 0, 22, P("#3F2A1A", a))
    c.save()
    c.rotate(look * 80)
    c.drawRRect(rr(18, -6, 12, 12, 4), P("#E8B48A", a))
    c.restore()
    if wave > 0:
        c.drawLine(0, 30, 10 + math.sin(t * 12) * 16, 70, P("#E8B48A", a, stroke=12))
    else:
        c.drawRRect(rr(26, 18, 22, 14, 3), P("#0EA5E9", a))
        add_glow(c, 37, 25, 30, "#7DD3FC", 0.5 * a)
    c.restore()


def window_sky(c, x, y, w, h, k, a=1.0):
    """A window whose sky goes from night (k = 0) to sunrise (k = 1)."""
    c.drawRRect(rr(x - 12, y - 12, w + 24, h + 24, 10), P("#1E293B", a))
    top = mix("#0B1030", "#60A5FA", k)
    low = mix("#1E1B4B", "#FDBA74", k)
    c.drawRect(R(x, y, w, h), lin_paint(0, y, 0, y + h, [top, low], a=a))
    c.save()
    c.clipRect(R(x, y, w, h))
    my = y + 70 + k * h * 1.2
    c.drawCircle(x + w * 0.3, my, 30, P("#F1F5F9", a * (1 - k)))
    sy = y + h + 40 - k * (h * 0.75)
    add_glow(c, x + w * 0.7, sy, 140, "#FDBA74", 0.8 * k * a)
    c.drawCircle(x + w * 0.7, sy, 38, P("#FDE68A", a * k))
    c.drawRect(R(x, y + h - 40, w, 40), P("#0F172A", a * 0.8))
    c.restore()
    c.drawLine(x + w / 2, y, x + w / 2, y + h, P("#1E293B", a, stroke=10))


def phone_icon(c, x, y, pct, a=1.0):
    c.drawRRect(rr(x - 34, y - 64, 68, 128, 14), P("#0F172A", a))
    c.drawRRect(rr(x - 28, y - 56, 56, 112, 10), P("#1E293B", a))
    k = clamp(pct / 100.0)
    c.drawRRect(rr(x - 16, y + 30 - 60 * k, 32, 60 * k, 5), P("#22C55E", a))
    c.drawRRect(rr(x - 16, y - 30, 32, 60, 5), P("#94A3B8", a, stroke=3))


def overalls_man(c, x, y, h, t, a=1.0, pose="look", face=1):
    """The neighbourhood mechanic in blue overalls and a cap (Arabic tag) or the uncle (English)."""
    person(c, x, y, h, "#1D4ED8", t, pose=pose, face=face, hat="cap", hair="#1F1A17", skin="#C68B5E", pants="#1D4ED8", a=a)
    u = h / 140.0
    p = skia.Path()
    p.moveTo(x - 12 * u, y - 118 * u)
    p.cubicTo(x - 6 * u, y - 124 * u, x + 6 * u, y - 124 * u, x + 14 * u, y - 118 * u)
    p.cubicTo(x + 6 * u, y - 114 * u, x - 6 * u, y - 114 * u, x - 12 * u, y - 118 * u)
    c.drawPath(p, P("#1F1A17", a))


def bubble(c, x, y, s, p, tail_left=True):
    """Speech bubble (screen space), sized to its text."""
    if p <= 0:
        return
    k = e_back(clamp(p * 1.25))
    size = 44
    w = (arabic.width_ar(s, size * 1.15, "Tajawal-Black") if arabic.is_ar(s) else text_width(s, size, "Poppins-Black")) + 80
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    tail = skia.Path()
    sx = -1 if tail_left else 1
    tail.moveTo(sx * w * 0.25, 40)
    tail.lineTo(sx * w * 0.32, 100)
    tail.lineTo(sx * w * 0.1, 40)
    tail.close()
    c.drawRRect(rr(-w / 2, -60, w, 120, 40), P("#000000", 0.35 * p, blur=14))
    c.drawPath(tail, P("#FFFFFF", p))
    c.drawRRect(rr(-w / 2, -60, w, 120, 40), P("#FFFFFF", p))
    word(c, s, 0, 16, size, "#0F172A", p)
    c.restore()


# ====================================================================================== the episode
class EvCar(EpisodeV2):
    BUILD_NO = 34
    FIRST_SET = "street"
    CLEAR = "#0B0E24"
    TITLE = {"en": "ELECTRIC CAR", "ar_sa": "عربية كهربا"}
    EMPH = {"en": ["CONGRATS", "TRUNK", "ENGINE", "BEATS", "SPORTS", "LINE", "ELECTRIC", "ENERGY", "HEAVY", "HUNDREDS",
                   "KILOS", "EIGHT", "THOUSAND", "CELLS", "FLAT", "FLOOR", "LOW", "HUGS", "GAS", "EXPLOSIONS", "PISTONS",
                   "GEARBOX", "WHEELS", "MOTOR", "FULL", "FORCE", "STANDSTILL", "ONE", "GEAR", "BRAKE", "HEAT", "GONE",
                   "LIFT", "FOOT", "GENERATOR", "BATTERY", "QUIET", "CROSSING", "HEAR", "TWENTY", "SOUND", "PURPOSE",
                   "EUROPE", "LAW", "FOLLOW", "SMARTPHONE", "PLUG", "NIGHT", "MORNING", "PHONE", "NORWAY", "NINETY-SIX",
                   "YOURSELF", "UNCLE", "HOOD", "OIL", "GROCERIES"],
            "ar_sa": ["مبروك", "الموتور", "شنطة", "وبتسبق", "السبور", "الإشارة", "كهربا", "طاقة", "تقيلة", "تمن", "تلاف",
                      "خلية", "الأرضية", "تحت", "تمسك", "البنزين", "انفجارات", "وبساتم", "وفتيس", "العجل", "موتور", "قوته",
                      "كاملة", "واحدة", "فرامل", "حرارة", "وتضيع", "ترفع", "رجلك", "دينامو", "للبطارية", "ساكتة",
                      "الشارع", "سامعها", "عشرين", "صوت", "مخصوص", "أوروبا", "قانون", "تابعني", "موبايل", "اشحنها",
                      "بالليل", "والصبح", "مليانة", "موبايلك", "النرويج", "وتسعين", "بإيدك", "والميكانيكي", "الكبوت",
                      "الزيت", "الخضار", "عمرة"]}
    KEYS = {"ar_sa": {
        ("hook", "TRUNK"): "شنطة", ("hook", "ENGINE"): "الموتور", ("hook", "BEATS"): "وبتسبق", ("hook", "SPORTS"): "السبور",
        ("hook", "LINE"): "الإشارة", ("hook", "CONGRATS"): "مبروك", ("hook", "ELECTRIC"): "كهربا",
        ("break1", "ENERGY"): "طاقة", ("break1", "BATTERIES"): "والبطاريات", ("break1", "HEAVY"): "تقيلة",
        ("fix1", "LAY"): "فترص", ("fix1", "CELLS"): "خلية", ("fix1", "FLOOR"): "الأرضية", ("fix1", "LOW"): "فالتقل",
        ("fix1", "HUGS"): "تمسك",
        ("break2", "GAS"): "البنزين", ("break2", "EXPLOSIONS"): "انفجارات", ("break2", "PISTONS"): "وبساتم",
        ("break2", "GEARBOX"): "وفتيس", ("break2", "WHEELS"): "العجل",
        ("fix2", "MOTOR"): "موتور", ("fix2", "FULL"): "قوته", ("fix2", "STANDSTILL"): "لحظة", ("fix2", "GEAR"): "وسرعة",
        ("break3", "BRAKE"): "فرامل", ("break3", "HEAT"): "حرارة", ("break3", "GONE"): "وتضيع",
        ("fix3", "LIFT"): "ترفع", ("fix3", "GENERATOR"): "دينامو", ("fix3", "BATTERY"): "للبطارية",
        ("break4", "QUIET"): "ساكتة", ("break4", "CROSSING"): "بيعدي", ("break4", "HEAR"): "سامعها",
        ("fix4", "TWENTY"): "عشرين", ("fix4", "SOUND"): "صوت", ("fix4", "EUROPE"): "أوروبا", ("fix4", "LAW"): "قانون",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "PLUG"): "اشحنها", ("reveal", "NIGHT"): "بالليل", ("reveal", "MORNING"): "والصبح",
        ("reveal", "FULL"): "مليانة", ("reveal", "PHONE"): "موبايلك",
        ("stat", "EIGHT"): "تمن", ("stat", "ONE"): "وسرعة", ("stat", "NORWAY"): "النرويج",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "UNCLE"): "والميكانيكي", ("tag", "HOOD"): "الكبوت", ("tag", "OIL"): "الزيت", ("tag", "GROCERIES"): "الخضار",
        ("tag", "FINDS"): "عمرة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a smartphone"),
                   "stat": [("8,000", "BATTERY CELLS"), ("1", "GEAR"), ("96%", "NORWAY'S NEW CARS")],
                   "L": {"trunk": "A TRUNK!", "noengine": "NO ENGINE", "sports": "SPORTS CAR", "go": "GO!",
                         "ev": "ELECTRIC CAR", "energy": "NEEDS LOTS OF ENERGY", "heavy": "HUNDREDS OF KILOS",
                         "lean": "TOP-HEAVY", "cells": "8,000 CELLS", "floor": "FLAT UNDER THE FLOOR",
                         "low": "WEIGHT DOWN LOW", "hugs": "HUGS THE ROAD", "explosions": "EXPLOSIONS",
                         "pistons": "PISTONS", "gearbox": "GEARBOX", "wait": "WHEELS: WAITING...",
                         "motor": "ELECTRIC MOTOR", "magnets": "MAGNETS", "full": "FULL FORCE AT 0 km/h",
                         "onegear": "JUST 1 GEAR", "heat": "HEAT", "gone": "ENERGY GONE", "lift": "FOOT OFF",
                         "gen": "MOTOR = GENERATOR", "back": "ENERGY BACK IN", "quiet": "SILENT", "hear": "CAN'T HEAR IT",
                         "sound": "SOUND ON BELOW 20 km/h", "law": "THE LAW IN EUROPE", "plug": "PLUG IN AT NIGHT",
                         "full2": "FULL BY MORNING", "kmh": "km/h", "oil": "WHERE'S THE OIL?",
                         "groc": "GROCERIES?!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: موبايل"),
                      "stat": [("8,000", "خلية بطارية"), ("1", "سرعة بس"), ("96%", "من عربيات النرويج الجديدة")],
                      "L": {"trunk": "شنطة!", "noengine": "مفيش موتور", "sports": "عربية سبور", "go": "يلا!",
                            "ev": "عربية كهربا", "energy": "عايزة طاقة كتير", "heavy": "تقيلة أوي",
                            "lean": "التقل فوق", "cells": "8,000 خلية", "floor": "تحت الأرضية",
                            "low": "التقل تحت", "hugs": "ماسكة في الأرض", "explosions": "انفجارات",
                            "pistons": "بساتم", "gearbox": "فتيس", "wait": "العجل مستني...",
                            "motor": "موتور كهربا", "magnets": "مغناطيس", "full": "قوة كاملة من أول لحظة",
                            "onegear": "سرعة واحدة بس", "heat": "حرارة", "gone": "الطاقة ضاعت", "lift": "رفعت رجلك",
                            "gen": "الموتور بقى دينامو", "back": "الكهربا راجعة", "quiet": "ساكتة",
                            "hear": "مش سامعها", "sound": "صوت لحد 20 كم/س", "law": "قانون في أوروبا",
                            "plug": "اشحنها بالليل", "full2": "الصبح مليانة", "kmh": "كم/س", "oil": "فين الزيت؟",
                            "groc": "دي عايزة عمرة!"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "trunk": ("hook", "TRUNK", 0.25), "engine": ("hook", "ENGINE", 0.32), "beats": ("hook", "BEATS", 0.45),
            "sports": ("hook", "SPORTS", 0.52), "line": ("hook", "LINE", 0.62), "congrats": ("hook", "CONGRATS", 0.72),
            "electric": ("hook", "ELECTRIC", 0.92),
            "energy": ("break1", "ENERGY", 0.3), "batteries": ("break1", "BATTERIES", 0.55), "heavy": ("break1", "HEAVY", 0.7),
            "lay": ("fix1", "LAY", 0.05), "cells": ("fix1", "CELLS", 0.3), "floor": ("fix1", "FLOOR", 0.5),
            "low": ("fix1", "LOW", 0.7), "hugs": ("fix1", "HUGS", 0.85),
            "gas": ("break2", "GAS", 0.1), "explosions": ("break2", "EXPLOSIONS", 0.3), "pistons": ("break2", "PISTONS", 0.45),
            "gearbox": ("break2", "GEARBOX", 0.6), "wheels": ("break2", "WHEELS", 0.8),
            "motor": ("fix2", "MOTOR", 0.2), "full": ("fix2", "FULL", 0.45), "standstill": ("fix2", "STANDSTILL", 0.6),
            "gear": ("fix2", "GEAR", 0.9),
            "brake": ("break3", "BRAKE", 0.25), "heat": ("break3", "HEAT", 0.6), "gone": ("break3", "GONE", 0.9),
            "lift": ("fix3", "LIFT", 0.1), "generator": ("fix3", "GENERATOR", 0.5), "battery": ("fix3", "BATTERY", 0.85),
            "quiet": ("break4", "QUIET", 0.2), "crossing": ("break4", "CROSSING", 0.5), "hear": ("break4", "HEAR", 0.8),
            "twenty": ("fix4", "TWENTY", 0.15), "sound": ("fix4", "SOUND", 0.45), "europe": ("fix4", "EUROPE", 0.75),
            "law": ("fix4", "LAW", 0.92),
            "follow": ("cta", "FOLLOW", 0.35),
            "plug": ("reveal", "PLUG", 0.15), "night": ("reveal", "NIGHT", 0.3), "morning": ("reveal", "MORNING", 0.55),
            "full2": ("reveal", "FULL", 0.75), "phone": ("reveal", "PHONE", 0.92),
            "s1": ("stat", "EIGHT", 0.04), "s2": ("stat", "ONE", 0.3), "s3": ("stat", "NORWAY", 0.55),
            "cong2": ("closer", "CONGRATS", 0.16),
            "uncle": ("tag", "UNCLE", 0.1), "hood": ("tag", "HOOD", 0.3), "oil": ("tag", "OIL", 0.5),
            "groc": ("tag", "GROCERIES", 0.75), "finds": ("tag", "FINDS", 0.7)})
        T["open"] = 0.25
        T["go"] = max(min(T["beats"], T["line"]) - 0.15, T["open"] + 1.6)        # the light turns green
        T["drop"] = min(T["batteries"], T["heavy"]) - 0.25                           # the big battery lands on the roof
        T["spread"] = min(T["lay"], T["cells"]) - 0.05
        T["eng0"] = min(T["gas"], T["explosions"]) - 0.2
        T["mot0"] = T["motor"] - 0.25
        T["regen"] = max(T["generator"] - 0.2, T["lift"] + 0.3)
        T["beep"] = min(T["sound"], T["twenty"] + 0.6) - 0.1
        T["punch"] = max(T["groc"], T["finds"]) if self.rtl else T["groc"]
        # ---- sets
        self.cut(s("break1") - 0.12, "xray", 1)
        self.cut(s("break4") - 0.12, "cross", -1)
        self.cut(s("reveal") - 0.12, "garage", 1)
        self.cut(s("stat") - 0.12, "street", -1)
        self.cut(s("tag") - 0.2, "uncle", 1)
        # ---- cameras
        cm = Camera(330, -150, 1.72)                                                  # street: close on the open trunk
        cm.key(0.05, 320, -150, 1.68, 1.0)
        cm.key(max(T["open"] + 1.2, min(T["trunk"], T["engine"]) + 0.5), 60, -260, 0.92, 1.2)   # both cars + the light
        cm.key(T["go"] + 0.6, 40, -250, 0.95, 1.4)
        cm.key(s("stat") - 0.12, 20, -250, 0.86, 0.0).key(s("stat"), 30, -250, 0.88, 3.0)
        cm.key(s("closer") - 0.1, 0, -170, 1.05, 1.0)
        self.cam = cm
        cx_ = Camera(0, -150, 0.98)                                                   # x-ray
        cx_.key(T["drop"] - 0.2, 0, -200, 0.9, 0.8)
        cx_.key(T["spread"] + 0.6, 0, -120, 1.0, 1.2)
        cx_.key(s("break2") - 0.12, 230, -150, 1.4, 0.0).key(T["gearbox"], 140, -150, 1.25, 1.2)
        cx_.key(s("fix2") - 0.12, -150, -150, 1.3, 0.8).key(T["full"], -60, -140, 1.05, 1.4)
        cx_.key(s("break3") - 0.12, 0, -120, 1.0, 0.0)
        cx_.key(s("fix3") - 0.12, -80, -130, 1.1, 1.0)
        self.camx = cx_
        # ---- speeds
        sp = Track(0.0)
        sp.to(T["go"], 2600.0, 1.0, e_in)
        sp.to(s("break1") - 0.12, 900.0, 0.0)
        sp.to(T["drop"], 0.0, 0.5)
        sp.to(T["hugs"] - 0.4, 900.0, 1.0)
        sp.to(s("break2") - 0.12, 0.0, 0.0)
        sp.to(T["mot0"] + 0.25, 1800.0, 0.9, e_in)
        sp.to(T["brake"], 300.0, 1.2)
        sp.to(s("fix3") - 0.12, 900.0, 0.0).to(T["lift"], 200.0, 3.0)
        sp.to(s("break4") - 0.12, 0.0, 0.0)
        sp.to(s("stat") - 0.12, 700.0, 0.0)
        sp.to(s("closer") - 0.1, 0.0, 0.8)
        self.spd = sp
        self.run = Run(sp, self.duration + 1)
        rival = Track(0.0).to(T["go"] + 0.15, 1900.0, 1.6, e_in).to(s("break1") - 0.12, 0.0, 0.0)
        self.rival = Run(rival, self.duration + 1)
        self.walk = Track(0.0)
        self.walk.to(s("break4") - 0.12, -230.0, 0.0).to(s("break4"), 40.0, max(0.6, T["hear"] + 0.3 - s("break4")))
        self.walk.to(T["beep"] + 0.3, -160.0, 0.6)
        self.carz = Track(0.0).to(s("break4") - 0.12, 0.0, 0.0).to(s("break4"), 200.0, max(0.5, T["hear"] - s("break4")))
        self.carz.to(T["beep"] + 0.2, 280.0, 0.8)
        self.bat = Track(62.0).to(T["regen"], 71.0, max(0.8, T["battery"] + 0.4 - T["regen"]))
        self.charge = Track(18.0).to(T["plug"] + 0.2, 100.0, max(0.8, T["full2"] - T["plug"] - 0.2))
        self.dawn = Track(0.0).to(T["night"] + 0.2, 1.0, max(0.6, T["morning"] + 0.1 - T["night"]))
        self.spans = [(T["heavy"], T["hugs"] + 0.3), (T["wheels"], T["gear"] + 0.3), (T["heat"], T["battery"] + 0.3),
                      (T["hear"], T["law"] + 0.3)]
        self.shakes = [(T["go"], 0.4, 8), (T["congrats"], 0.3, 8), (T["drop"] + 0.25, 0.4, 14), (T["mot0"] + 0.3, 0.3, 6),
                       (T["brake"], 0.3, 6), (T["hear"], 0.3, 5), (s("closer") + 0.2, 0.35, 10)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def rot(self, t):
        return math.degrees(self.run.at(t) / WR)

    def city(self, c, t, cam, d):
        """Screen-space background for the side-view street sets: dusk sky, skyline, far sidewalk."""
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=gy - 260 * z)
        v2.stars(c, W, H, t, 0.6, dx=-cx * 0.01)
        c.save()
        c.translate(-((d * 0.08 + cx * 0.08) % 1400), gy - 160 * z)
        for rep in range(3):
            skyline_night(c, rep * 1400 - 200, rep * 1400 + 1200, 0.0, seed=4 + rep % 2, hmin=200, hmax=700, lit=0.4, t=t)
        c.restore()
        return gy

    def road(self, c, d, x0, x1):
        vrect(c, x0, -160, x1 - x0, 70, ["#4B5563", "#374151"])                                  # far sidewalk
        vrect(c, x0, -90, x1 - x0, 3000, list(ASPHALT), [0, 0.03, 0.2, 1])
        for k in range(int(x0 // 260) - 1, int(x1 // 260) + 2):                                   # lane marks
            xx = k * 260 - (d % 260)
            c.drawRect(R(xx, -64, 120, 8), P("#E5E7EB", 0.7))
        c.drawRect(R(x0, 26, x1 - x0, 22), P("#6B7280"))                                         # near curb
        vrect(c, x0, 48, x1 - x0, 3000, ["#4B5563", "#1F2937", "#111827"], [0, 0.2, 1])
        for k in range(int(x0 // 520) - 1, int(x1 // 520) + 2):                                   # street lamps
            xx = k * 520 - (d * 0.999 % 520) + 200
            c.drawRect(R(xx, -760, 12, 600), P("#1F2937"))
            c.drawRRect(rr(xx - 40, -770, 90, 18, 9), P("#334155"))
            add_glow(c, xx + 6, -748, 150, "#FDE68A", 0.35)

    # ------------------------------------------------------------------ set: street (hook, stat, closer)
    def draw_street(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        d = self.run.at(t)
        gy = self.city(c, t, cam, d)
        self.view(c, cam)
        x0, x1 = cx - 640 / z, cx + 640 / z
        self.road(c, d, x0, x1)
        hook = t < s("break1")
        if hook:
            lx = 620 - d
            traffic_light(c, lx, -150, 1.0 if t >= T["go"] else 0.0)
            c.drawRect(R(lx - 260, -86, 18, 80), P("#F8FAFC", 0.8))                               # stop line
            rx = self.rival.at(t) - d
            sports_car(c, rx - 30, -70, 0.92, math.degrees(self.rival.at(t) / WR))
        hood = 0.0
        if hook:
            hood = prog(t, T["open"], T["open"] + 0.5) * (1 - prog(t, T["go"] - 0.6, T["go"] - 0.15))
        squat = clamp(self.spd.at(t) / 2600.0) * (1 if t < T["go"] + 0.8 else 0)
        ev_side(c, 0, 0, 1.0, self.rot(t), t, hood=hood, squat=-0.4 * squat)
        if hook and t >= T["go"]:
            k = prog(t, T["go"], T["go"] + 0.3) * (1 - prog(t, T["go"] + 1.6, T["go"] + 2.4))
            if k > 0:
                for i in range(8):
                    yy = -320 + i * 34
                    c.drawLine(-520 - i * 30, yy, -900 - i * 50, yy, P("#E0F2FE", 0.4 * k, stroke=5))
        if t >= s("closer") - 0.1:
            add_glow(c, 0, -200, 700, TEAL, 0.18 * prog(t, s("closer"), s("closer") + 0.6))
        c.restore()
        self.ui["street"] = cam

    def ui_street(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("street", self.cam.at(tw))
        if tw < s("break1"):
            fx_, fy_ = self.at(cam, 330, -170)
            self.label(fx_, fy_, 300, 560, "trunk", T["open"] + 0.3, T["go"] - 0.3, "#FDE68A", size=40)
            self.chip(780, 460, "noengine", min(T["engine"], T["trunk"]) + 0.2, T["go"] - 0.3, accent=WARN, size=36)
            rx, ry = self.at(cam, self.rival.at(tw) - self.run.at(tw) - 30, -330)
            if tw < T["go"] + 1.2:
                self.chip(clamp(rx, 220, 860), max(560, ry - 40), "sports", T["sports"] - 0.2, T["go"] + 1.2, accent=RED, size=36)
            self.chip(540, 640, "go", T["go"] - 0.05, T["go"] + 0.9, accent=GOOD, size=52)
            self.chip(540, 520, "ev", T["electric"] - 0.15, s("break1") + 0.1, accent=TEAL, size=44)

    # ------------------------------------------------------------------ set: x-ray (break1 .. fix3)
    def draw_xray(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.camx.at(t)
        cx, cy, z = cam
        d = self.run.at(t)
        gy = (0 - cy) * z + H / 2
        vrect(c, 0, 0, W, H, ["#06122B", "#0B1F3F", "#06122B"])
        for k in range(-2, 14):                                                                     # blueprint grid
            gx = (k * 120 - (d * z * 0.3) % 120)
            c.drawLine(gx, 0, gx, H, P("#1E3A8A", 0.35, stroke=2))
        for k in range(18):
            c.drawLine(0, k * 120, W, k * 120, P("#1E3A8A", 0.35, stroke=2))
        self.view(c, cam)
        x0, x1 = cx - 640 / z, cx + 640 / z
        c.drawRect(R(x0, 0, x1 - x0, 6), P("#7DD3FC", 0.8))
        for k in range(int(x0 // 200) - 1, int(x1 // 200) + 2):
            xx = k * 200 - (d % 200)
            c.drawRect(R(xx, 20, 90, 6), P("#7DD3FC", 0.5))
        in1 = t < s("break2") - 0.12
        drop = prog(t, T["drop"] - 0.35, T["drop"])
        spread = prog(t, T["spread"], T["spread"] + 1.1) if t >= s("fix1") - 0.12 else 0.0
        lean = 0.0
        squat = 0.0
        if in1 and drop > 0 and spread < 0.3:
            lean = math.sin((t - T["drop"]) * 7) * 4.5 * clamp((t - T["drop"]) * 3) * (1 - spread / 0.3)
            squat = drop * (1 - spread / 0.3)
        glow = 0.0
        if s("break3") - 0.12 <= t < s("fix3") - 0.12:
            glow = prog(t, T["brake"], T["brake"] + 0.4) * (1 - prog(t, s("fix3") - 0.6, s("fix3") - 0.15))
        ev_side(c, 0, 0, 1.0, self.rot(t), t, xray=1.0, lean=lean, squat=squat, glow=glow, lights=0.6)
        c.save()
        c.translate(0, squat * 18)
        c.rotate(lean)
        # the battery: big block on the roof (break1), cells under the floor (fix1 on)
        if in1:
            if spread < 1:
                by = lerp(-1100, -339, e_in(drop)) if t < T["drop"] else -339
                if drop > 0:
                    battery_block(c, 0, by, 400, 230, a=1 - prog(spread, 0.05, 0.25))
            if spread > 0:
                cells(c, -250, 250, -96, 40, spread, t, src=(0, -420))
        else:
            cells(c, -250, 250, -96, 40, 1.0, t)
        cgy = -420 if (in1 and drop > 0.5 and spread < 0.35) else (-200 if in1 and drop <= 0.5 else -80)
        if in1 and spread > 0:
            cgy = lerp(-420, -80, e_io(prog(spread, 0.2, 0.9)))
        if in1:
            cg_mark(c, 60, cgy, a=prog(t, T["heavy"] - 0.1, T["heavy"] + 0.2))
        # break2: the gas engine in front; fix2 on: the electric motor at the rear axle
        if s("break2") - 0.12 <= t < s("fix2") - 0.12 + 0.5:
            ea = prog(t, T["eng0"], T["eng0"] + 0.3) * (1 - prog(t, s("fix2") - 0.12, s("fix2") + 0.3))
            gas_engine(c, 350, -96, t, prog(t, T["explosions"] - 0.2, T["explosions"]), a=ea)
            if ea > 0:
                c.drawLine(120, -90, WB, -WR, P("#94A3B8", ea, stroke=12))
            if t >= s("fix2") - 0.12:
                pk = prog(t, s("fix2") - 0.12, s("fix2") + 0.4)
                for i in range(8):
                    an = i * 45
                    c.drawCircle(350 + math.cos(math.radians(an)) * 140 * pk, -180 + math.sin(math.radians(an)) * 140 * pk,
                                 40 * (1 - pk) + 6, P("#CBD5E1", 0.6 * (1 - pk)))
        if t >= s("fix2") - 0.12:
            ma = prog(t, T["mot0"], T["mot0"] + 0.3) if t < s("break3") - 0.12 else 1.0
            rev = 1.0 if t >= T["regen"] and t >= s("fix3") - 0.12 else 0.0
            mg = prog(t, T["mot0"], T["mot0"] + 0.4) * (1 - prog(t, s("break3") - 0.5, s("break3") - 0.12)) + \
                (prog(t, T["regen"], T["regen"] + 0.3) if t >= s("fix3") - 0.12 else 0.0)
            motor(c, -WB, -WR, 46, self.rot(t) * 2.2, a=ma, glow=mg, rev=rev)
            c.drawLine(-WB + 50, -90, -250, -96, P("#F59E0B", ma, stroke=8))                        # cable to the battery
        # fix3: energy flows back
        if t >= s("fix3") - 0.12:
            k = prog(t, T["regen"], T["regen"] + 0.3)
            dash_line(c, [(-WB, -WR), (-WB + 60, -130), (-150, -130), (0, -110)], t, "#FDE047", a=k, w=12, speed=-300)
        # break3: heat from the brakes
        if glow > 0:
            for wx in (-WB, WB):
                add_glow(c, wx, -WR - 120, 200, "#FF6A2B", 0.5 * glow)
                for i in range(3):
                    q = (t * 0.9 + i / 3.0) % 1.0
                    hp = skia.Path()
                    hx0 = wx - 30 + i * 30
                    hp.moveTo(hx0, -WR - 70 - q * 120)
                    for k in range(1, 7):
                        hp.lineTo(hx0 + math.sin(k * 1.4 + t * 8 + i) * 14, -WR - 70 - q * 120 - k * 28)
                    c.drawPath(hp, P("#FDBA74", 0.85 * glow * (1 - q), stroke=7))
        c.restore()
        c.restore()
        self.ui["xray"] = cam
        self.ui["cgy"] = cgy

    def ui_xray(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("xray", self.camx.at(tw))
        if tw < s("fix1") - 0.12:
            self.chip(540, 520, "energy", T["energy"] - 0.15, T["heavy"] - 0.1, accent=HILITE, size=38)
            self.chip(540, 520, "heavy", T["heavy"] - 0.1, s("fix1") - 0.15, accent=WARN, size=40)
            gx, gy = self.at(cam, 60, -420)
            self.label(gx + 20, gy, 820, 700, "lean", T["heavy"] + 0.1, s("fix1") - 0.15, WARN, size=32)
            self.badge("alert", T["heavy"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["heavy"] + 0.05, 1.5)
            return
        if tw < s("break2") - 0.12:
            ax, ay = self.at(cam, 120, -80)
            self.label(ax, ay, 780, 560, "cells", T["cells"] - 0.1, s("break2") - 0.15, "#22C55E", size=34)
            bx, by = self.at(cam, -150, -80)
            self.label(bx, by, 300, 1190, "floor", T["floor"] - 0.1, s("break2") - 0.15, "#7DD3FC", size=32)
            gx, gy = self.at(cam, 60, self.ui.get("cgy", -80))
            self.label(gx, gy, 300, 560, "low", T["low"] - 0.1, s("break2") - 0.15, "#FDE047", size=32)
            self.chip(780, 1190, "hugs", T["hugs"] - 0.1, s("break2") - 0.15, accent=GOOD, size=34)
            self.badge("check", T["hugs"] + 0.1, s("break2") - 0.15, x=880, y=330)
            return
        if tw < s("fix2") - 0.12:
            ex, ey = self.at(cam, 350, -260)
            self.label(ex, ey, 780, 500, "explosions", T["explosions"] - 0.1, max(T["pistons"] - 0.1, T["explosions"] + 0.9), "#FB923C", size=32)
            px, py = self.at(cam, 300, -150)
            self.label(px, py, 290, 500, "pistons", T["pistons"] - 0.1, s("fix2") - 0.15, "#E5E7EB", size=32)
            gx, gy = self.at(cam, 180, -70)
            self.label(gx, gy, 290, 640, "gearbox", T["gearbox"] - 0.1, s("fix2") - 0.15, "#94A3B8", size=32)
            self.chip(540, 1195, "wait", T["wheels"] - 0.1, s("fix2") - 0.15, accent=WARN, size=32)
            self.badge("alert", T["wheels"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["wheels"] + 0.05, 1.5)
            return
        if tw < s("break3") - 0.12:
            mx, my = self.at(cam, -WB, -WR - 50)
            self.label(mx, my, 300, 640, "motor", T["motor"] - 0.1, T["full"] + 0.2, "#38BDF8", size=34)
            self.label(mx, my + 30, 300, 640, "magnets", T["full"] + 0.2, s("break3") - 0.15, "#EF4444", size=34)
            self.chip(700, 500, "full", T["full"] - 0.1, s("break3") - 0.15, accent=HILITE, size=34)
            self.chip(760, 620, "onegear", T["gear"] - 0.2, s("break3") - 0.15, accent=GOOD, size=34)
            self.badge("check", T["gear"] + 0.1, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix3") - 0.12:
            wx, wy = self.at(cam, WB, -WR - 60)
            self.label(wx, wy, 760, 560, "heat", T["heat"] - 0.15, s("fix3") - 0.15, "#FB923C", size=36)
            self.chip(330, 560, "gone", T["gone"] - 0.15, s("fix3") - 0.15, accent=WARN, size=36)
            self.badge("alert", T["heat"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["heat"] + 0.05, 1.5)
            return
        pedal(c, 860, 620, prog(tw, T["lift"] - 0.1, T["lift"] + 0.3), self.span(T["lift"] - 0.2, T["generator"] + 0.6))
        self.chip(860, 820, "lift", T["lift"] - 0.1, T["generator"] + 0.5, accent="#E2E8F0", size=30)
        mx, my = self.at(cam, -WB, -WR - 50)
        self.label(mx, my, 300, 520, "gen", T["generator"] - 0.1, s("break4") - 0.15, "#FDE047", size=34)
        battery_pill(c, 300, 660, self.bat.at(tw), self.span(T["regen"] - 0.2, s("break4") - 0.15))
        self.chip(560, 760, "back", T["battery"] - 0.15, s("break4") - 0.15, accent=GOOD, size=32)
        self.badge("check", T["battery"] + 0.1, s("break4") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: cross (top view, break4, fix4, cta)
    def draw_cross(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#1F2333", "#191C2A", "#141622"])
        c.drawRect(R(0, 0, 150, H), P("#3F4656"))                                                  # sidewalks
        c.drawRect(R(930, 0, 150, H), P("#3F4656"))
        c.drawRect(R(146, 0, 8, H), P("#9CA3AF"))
        c.drawRect(R(926, 0, 8, H), P("#9CA3AF"))
        for i in range(6):                                                                          # zebra
            c.drawRect(R(150, 400 + i * 64, 780, 36), P("#F1F5F9", 0.85))
        c.drawLine(540, 0, 540, 360, P("#FBBF24", 0.7, stroke=6))
        c.drawLine(540, 800, 540, H, P("#FBBF24", 0.7, stroke=6))
        add_glow(c, 80, 330, 160, "#FDE68A", 0.25)
        add_glow(c, 1000, 900, 160, "#FDE68A", 0.25)
        cz = self.carz.at(t)
        car_y = 1260 - cz
        quiet = s("break4") - 0.12 <= t < s("fix4") - 0.12
        loud = t >= T["beep"]
        ev_top(c, 720, car_y, 0.72, glow=1.0)
        nose = car_y - 0.72 * 240
        if quiet:
            speaker_waves(c, 700, nose - 70, t, a=prog(t, T["quiet"] - 0.1, T["quiet"] + 0.2), mute=1.0)
        if loud:
            speaker_waves(c, 720, nose - 10, t, a=prog(t, T["beep"], T["beep"] + 0.3), ang=-90, n=4)
        wx = 540 + self.walk.at(t)
        look = prog(t, T["beep"] + 0.1, T["beep"] + 0.5)
        walking = t < T["hear"] + 0.3 or (T["beep"] + 0.1 <= t < T["beep"] + 0.9)
        walker_top(c, wx, 580, 2.2, t, walk=1.0 if walking else 0.0, look=look, wave=prog(t, T["europe"] - 0.3, T["europe"]))
        self.ui["car_y"] = car_y
        self.ui["walker"] = (wx, 580)

    def ui_cross(self, c, t, tw):
        T, s = self.T, self.tl.s
        car_y = self.ui.get("car_y", 1100)
        wx, wy = self.ui.get("walker", (540, 580))
        if tw < s("fix4") - 0.12:
            self.chip(420, car_y - 60, "quiet", T["quiet"] - 0.1, T["hear"], accent="#CBD5E1", size=34)
            self.label(wx, wy - 70, 330, 330, "hear", T["hear"] - 0.15, s("fix4") - 0.15, WARN, size=36)
            self.badge("alert", T["hear"] + 0.05, s("fix4") - 0.2, x=880, y=330)
            self.red(T["hear"] + 0.05, 1.5)
            return
        if tw < s("cta") - 0.12:
            kmh = 18 if tw < T["beep"] + 0.8 else 12
            v2.chip(c, 330, 1000, f"{kmh} {self.L['kmh']}", self.span(T["twenty"] - 0.2, s("cta") - 0.15), accent=HILITE, size=40)
            self.chip(500, 330, "sound", T["sound"] - 0.15, T["europe"] - 0.1, accent=HILITE, size=34)
            self.chip(500, 330, "law", T["europe"] - 0.1, s("cta") - 0.15, accent=GOOD, size=36)
            self.badge("check", T["law"] + 0.1, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: garage (reveal)
    def draw_garage(self, c, t):
        T = self.T
        k = self.dawn.at(t)
        room(c, 0, 0, W, 1250, wall=mix("#1E2A4A", "#3B4A6B", k), floor="#2B3346", t=t, lamp=False)
        vrect(c, 0, 1250, W, H - 1250, ["#2B3346", "#1A1F2E", "#0F121C"])
        window_sky(c, 660, 330, 330, 260, k)
        cam = (0, -210, 0.9)
        self.view(c, cam)
        c.drawRect(R(-1000, 0, 2400, 10), P("#475569"))
        ev_side(c, 110, 0, 1.0, 0.0, t, lights=0.0, port=prog(t, T["plug"] - 0.2, T["plug"] + 0.2))
        c.drawRRect(rr(-540, -520, 110, 170, 20), P("#E2E8F0"))                                    # wall charger
        c.drawRRect(rr(-522, -500, 74, 38, 8), P("#0F172A"))
        add_glow(c, -485, -481, 60, "#22C55E", 0.6)
        pk = prog(t, T["plug"] - 0.3, T["plug"] + 0.2)
        if pk > 0:
            cab = skia.Path()
            cab.moveTo(-485, -350)
            cab.cubicTo(-485, -120, lerp(-485, -360, pk), -150, lerp(-450, -307, pk), lerp(-300, -199, pk))
            c.drawPath(cab, P("#111827", 1, stroke=14))
            if pk >= 1:
                dash_line(c, [(-485, -350), (-485, -220), (-380, -190), (-307, -199)], t, "#4ADE80", a=0.9, w=6, speed=300)
        c.drawRect(R(-430, -640, 220, 16), P("#78716C"))                                           # shelf + phone
        phone_icon(c, -320, -706, lerp(15, 100, prog(t, T["night"], T["phone"] + 0.2)))
        c.restore()

    def ui_garage(self, c, t, tw):
        T, s = self.T, self.tl.s
        battery_pill(c, 380, 640, self.charge.at(tw), self.span(T["plug"] - 0.2, s("stat") - 0.15), w=260)
        self.chip(400, 470, "plug", T["plug"] - 0.1, T["morning"] - 0.1, accent=GOOD, size=40)
        self.chip(400, 470, "full2", T["morning"] - 0.1, s("stat") - 0.15, accent=HILITE, size=40)

    # ------------------------------------------------------------------ set: uncle (tag)
    def draw_uncle(self, c, t):
        T = self.T
        cam = (160, -200, 1.0)
        gy = self.city(c, t, cam, 0.0)
        self.view(c, cam)
        self.road(c, 0.0, -600, 1200)
        hood = prog(t, T["hood"] - 0.3, T["hood"] + 0.3)
        ev_side(c, -60, 0, 1.0, 0.0, t, hood=hood, bag=1.0 if t >= T["groc"] - 0.4 else 0.0)
        if t >= T["groc"] - 0.4:
            k = e_back(prog(t, T["groc"] - 0.4, T["groc"]))
            groceries(c, 270, -130 - 60 * k, 0.8 + 0.3 * k)
        man_x = 560
        overalls_man(c, man_x, 0, 300, t, pose="look" if t < T["groc"] else "shrug", face=-1)
        if hood > 0.5 and t < T["groc"]:
            c.drawLine(man_x - 60, -190, 380, -150, P("#CBD5E1", 1, stroke=6))                    # dipstick hunting
        c.restore()
        self.ui["cam"] = cam

    def ui_uncle(self, c, t, tw):
        T = self.T
        k = self.span(T["oil"] - 0.2, T["punch"] - 0.05, 0.25, 0.1)
        if k > 0:
            bubble(c, 600, 470, self.L["oil"], k, tail_left=False)
        k2 = self.span(T["punch"], self.duration + 1, 0.25, 0.1)
        if k2 > 0:
            bubble(c, 600, 470, self.L["groc"], k2, tail_left=False)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, 0.0, pal=DUSK, horizon_y=H * 0.66)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (T["open"], sfx.creak(0.6), -12), (T["open"] + 0.4, sfx.pop(61), -10),
              (T["go"] - 0.6, sfx.beep(900.0), -14), (T["go"], sfx.beep(1400.0), -12), (T["go"], sfx.whirr(1.6, 300.0, 900.0, 62), -12),
              (T["go"] + 0.2, sfx.whoosh(0.8, True, 63), -10), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 64), -9),
              (T["electric"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 65), -4), (T["drop"], sfx.thud(0.6), -6), (T["drop"] + 0.05, sfx.creak(0.8), -10),
               (T["heavy"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["spread"], sfx.sparkle(1.0, 16, 66), -10), (T["floor"], sfx.click(67), -8), (T["hugs"], sfx.ding(), -8),
               (T["hugs"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["explosions"], sfx.thunk(69), -10),
               (T["explosions"] + 0.3, sfx.thunk(70), -12), (T["gearbox"], sfx.clank(), -12), (T["wheels"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.hiss(0.5, 71), -10), (T["mot0"], sfx.charge_up(0.8), -10), (T["mot0"] + 0.3, sfx.whirr(1.4, 400.0, 1200.0, 72), -12),
               (T["gear"], sfx.ding(), -8), (T["gear"] + 0.2, sfx.chime(), -6)]
        ev += [(T["brake"], sfx.sizzle(0.8, 73), -10), (T["heat"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["lift"], sfx.click(74), -6), (T["regen"], sfx.charge_up(0.9), -10), (T["battery"], sfx.ding(), -8),
               (T["battery"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 75), -4), (T["hear"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["beep"], sfx.hum(1.4, 220.0), -12), (T["beep"] + 0.1, sfx.whirr(1.2, 500.0, 700.0, 76), -16),
               (T["law"], sfx.ding(), -8), (T["law"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(77), 0), (T["follow"] - 0.15, sfx.pop(78), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 79), -6), (T["plug"], sfx.lock_click(80), -6),
               (T["full2"], sfx.charge_up(0.6), -10), (T["full2"] + 0.3, sfx.ding(), -8)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 81), -6), (T["s1"], sfx.pop(82), -3), (T["s2"], sfx.pop(83), -3),
               (T["s3"], sfx.pop(84), -3)]
        ev += [(T["cong2"], sfx.pop(85), -2), (T["cong2"], sfx.sparkle(1.0, 14, 86), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 87), -6), (T["hood"], sfx.creak(0.6), -10), (T["punch"], sfx.womp(), -8)]
        return ev


NAME = "evcar"
EPISODE = EvCar
