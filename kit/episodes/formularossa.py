"""Episode 113 - Formula Rossa in Abu Dhabi (0 to 240 km/h in 4.9 s, Guinness's highest rollercoaster launch speed,
verified 2026; a hydraulic launch "similar in concept to those that fling fighter jets off aircraft carriers";
riders wear safety goggles against sand and bugs).  v2 look.

Sets: park (hook: close on the front car, a rider in big safety goggles, then the red train blasts off down the
straight past the red-roofed park in the desert; cta; stat; closer at night, for the cover), launch (break1: a hill
that would have to be 200 m tall, crossed out; fix1: a catapult flings the train like a jet off a carrier; break2: the
power lines spark; fix2: pumps squeeze oil into tanks of gas like a spring; break3: a cable tied to the nose would yank
the train back; fix3: a little cart underneath pulls it by a hook and lets go at full speed), brakes (break4: friction
brakes glowing red-hot; fix4: magnets slow it without touching), goggles (reveal: desert sand and a fly bounce off the
goggles), tag (English: a drive-thru line that never moves; Arabic: the car in front at a green light, its driver on
his phone).  No badges, logos or writing on the train or the park.
Everything is drawn in screen space; captions sit at y 1330, so the pictures stay above y 1240.
"""
from v2_base import *  # noqa: F401,F403

RED = ("#E3342F", "#B91C1C", "#7F1D1D")
SAND = ("#B98A55", "#94683D", "#6B4A2B")
RAIL_Y = 930                                           # the launch straight (park and launch sets)
Z_L, CX_L, CY_L, SY_L = 1.7, 560, 900, 820             # the close camera of the launch and brake sets
RAIL_S = SY_L + (RAIL_Y - CY_L) * Z_L                  # the rail on screen there
CL = 150                                               # length of one car
SKIN = ("#C68E62", "#A8754E")


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ====================================================================================== the train
def rider(c, x, y, s, t, speed=0.0, goggles=1.0, hair="#2B2530", a=1.0, glint=0.0):
    """A rider's head in profile (facing right), safety goggles on."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    blow = clamp(speed)
    for k in range(4):                                   # hair blown back
        p = skia.Path()
        p.moveTo(-6, -18 + k * 7)
        p.quadTo(-26 - 30 * blow, -22 + k * 7 + 6 * math.sin(t * 20 + k), -40 - 50 * blow, -14 + k * 8)
        c.drawPath(p, P(hair, a, stroke=7))
    c.drawCircle(0, -8, 22, P(SKIN[0], a))
    c.drawArc(R(-22, -32, 44, 30), 180, 180, True, P(hair, a))
    c.drawCircle(-4, -6, 6, P(SKIN[1], a))               # ear
    if goggles > 0:
        c.drawLine(-22, -12, 16, -12, P("#111827", a * goggles, stroke=7))
        c.drawRRect(rr(10, -22, 22, 18, 7), P("#1E293B", a * goggles))
        c.drawRRect(rr(10, -22, 22, 18, 7), P("#F59E0B", a * goggles, stroke=3))
        c.drawLine(15, -18, 22, -11, P("#BAE6FD", 0.8 * a * goggles, stroke=3))
        if glint > 0:
            add_glow(c, 24, -14, 30, "#FFFFFF", 0.8 * glint * a)
    c.restore()


def car(c, x, y, t, nose=False, speed=0.0, riders=True, goggles=1.0, a=1.0, glint=0.0):
    """One red race-car-shaped car, its back end at x, sitting on the rail at y (facing right)."""
    p = skia.Path()
    p.moveTo(x + 6, y - 14)
    p.lineTo(x + 6, y - 48)
    p.lineTo(x + 40, y - 52)
    p.lineTo(x + CL - (40 if nose else 20), y - 46)
    if nose:
        p.quadTo(x + CL + 30, y - 40, x + CL + 46, y - 20)
        p.lineTo(x + CL + 40, y - 14)
    else:
        p.lineTo(x + CL - 6, y - 40)
        p.lineTo(x + CL - 6, y - 14)
    p.close()
    c.drawPath(p, lin_paint(0, y - 52, 0, y - 14, [RED[0], RED[1]], a=a))
    c.drawPath(p, P(RED[2], a, stroke=3))
    c.drawLine(x + 14, y - 30, x + CL - 30, y - 30, P("#F8FAFC", 0.75 * a, stroke=4))
    for wx in (x + 30, x + CL - 30):
        c.drawCircle(wx, y - 6, 10, P("#1F2937", a))
        c.drawCircle(wx, y - 6, 4, P("#9CA3AF", a))
    if riders:
        for k, rx in enumerate((x + 52, x + 104)):
            rider(c, rx, y - 56, 0.9, t + k * 0.3, speed, goggles, a=a, glint=glint if (nose and k == 1) else 0.0,
                  hair=("#2B2530", "#6B3E26", "#111827", "#8B5A2B")[(k + int(x)) % 4])


def train(c, x, y, t, speed=0.0, goggles=1.0, a=1.0, glint=0.0, fins=0.0, n=4):
    """The train with its nose at x (facing right)."""
    for i in range(n):
        car(c, x - CL - 46 - i * (CL + 6), y, t, nose=(i == 0), speed=speed, goggles=goggles, a=a, glint=glint)
    if fins > 0:                                         # the copper fins under the cars (for the magnets)
        for i in range(n):
            fx = x - CL - 46 - i * (CL + 6) + CL / 2
            c.drawRect(R(fx - 40, y + 2, 80, 18), P("#C2773A", fins * a))


def streaks(c, x0, x1, y0, y1, t, k, seed=3):
    if k <= 0:
        return
    rng = random.Random(seed)
    for j in range(26):
        yy = rng.uniform(y0, y1)
        ln = rng.uniform(120, 340) * k
        xx = x1 - ((t * 1800 * rng.uniform(0.8, 1.3) + rng.uniform(0, 2000)) % (x1 - x0 + ln))
        c.drawLine(xx, yy, xx + ln, yy, P("#FFFFFF", 0.35 * k, stroke=rng.uniform(2, 5)))


def rail(c, y, x0=-60, x1=W + 60, night=0.0, legs=True):
    if legs:
        for x in range(int(x0), int(x1), 120):
            c.drawRect(R(x - 8, y + 8, 16, 1000 - y + 10), P(mix("#5B6475", "#2A303C", night)))
    c.drawRect(R(x0, y - 2, x1 - x0, 12), P(mix("#9CA3AF", "#4B5563", night)))
    c.drawRect(R(x0, y + 10, x1 - x0, 8), P(mix("#6B7280", "#374151", night)))


def speedo(c, x, y, kmh, a=1.0, top=240.0, r=100):
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#0F172A", 0.9 * a))
    c.drawCircle(x, y, r, P("#E2E8F0", a, stroke=8))
    arc = skia.Path()
    arc.addArc(R(x - r * 0.78, y - r * 0.78, r * 1.56, r * 1.56), 150, 240 * clamp(kmh / top))
    c.drawPath(arc, P(WARN if kmh > 120 else HILITE, a, stroke=16))
    ang = math.radians(150 + 240 * clamp(kmh / top))
    c.drawLine(x, y, x + math.cos(ang) * r * 0.72, y + math.sin(ang) * r * 0.72, P("#F8FAFC", a, stroke=7))
    c.drawCircle(x, y, 11, P("#F8FAFC", a))
    text(c, f"{int(round(kmh))}", x, y + r * 0.66, r * 0.5, "#F8FAFC", "Poppins-Black", a=a)


# ====================================================================================== the park
def sky(c, night=0.0, y1=1000):
    day = ["#1D2F5E", "#4F4C8C", "#C7687A", "#F4A95E"]
    ngt = ["#040817", "#0A1330", "#1A1E46", "#2A2350"]
    vrect(c, 0, 0, W, y1, [mix(a, b, night) for a, b in zip(day, ngt)], [0.0, 0.45, 0.8, 1.0])
    if night > 0:
        v2.stars(c, W, H, 0.0, 0.9 * night, n=180)


def palm(c, x, y, s, night=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    trunk = skia.Path()
    trunk.moveTo(-8, 0)
    trunk.quadTo(-4, -90, 10, -170)
    trunk.lineTo(18, -168)
    trunk.quadTo(6, -90, 8, 0)
    trunk.close()
    c.drawPath(trunk, P(mix("#6B4A2B", "#2A1E14", night)))
    for k in range(7):
        ang = -160 + k * 24
        p = skia.Path()
        p.moveTo(14, -170)
        ex, ey = 14 + math.cos(math.radians(ang)) * 90, -170 + math.sin(math.radians(ang)) * 50 + 30
        p.quadTo(14 + math.cos(math.radians(ang)) * 50, -200, ex, ey)
        c.drawPath(p, P(mix("#2F7A3C", "#12301A", night), 1, stroke=14))
    c.restore()


def red_roof(c, night=0.0, lit=0.0):
    """The park's big red swooping roof (plain, no badge)."""
    p = skia.Path()
    p.moveTo(470, 905)
    p.cubicTo(560, 760, 760, 700, 1140, 720)
    p.lineTo(1140, 905)
    p.close()
    c.drawPath(p, lin_paint(0, 700, 0, 905, [mix(RED[0], "#4A1010", night * 0.6), mix(RED[2], "#2A0808", night * 0.6)]))
    for k in range(5):
        q = skia.Path()
        q.moveTo(520 + k * 120, 905)
        q.cubicTo(590 + k * 110, 800, 700 + k * 90, 760, 1140, 740 + k * 30)
        c.drawPath(q, P(mix("#F87171", "#6B1A1A", night), 0.35, stroke=3))
    c.drawRect(R(470, 890, 670, 22), P(mix("#5B6475", "#262C38", night)))
    if lit > 0:
        for k in range(14):
            add_glow(c, 520 + k * 45, 892, 16, "#FDE68A", 0.7 * lit)


def hill_track(c, night=0.0, lit=0.0):
    """The coaster's tall top hat rising out of the park behind."""
    p = skia.Path()
    p.moveTo(-80, 930)
    p.cubicTo(120, 930, 160, 420, 260, 420)
    p.cubicTo(360, 420, 400, 930, 600, 930)
    c.drawPath(p, P(mix("#B91C1C", "#5A1212", night), 1, stroke=12))
    c.drawPath(p, P(mix("#FCA5A5", "#7F1D1D", night), 0.6, stroke=3))
    for k in range(9):
        x = 60 + k * 50
        m = skia.PathMeasure(p, False)
        for d in range(0, int(m.getLength()), 6):
            pos, _ = m.getPosTan(d)
            if abs(pos.x() - x) < 3:
                c.drawLine(x, pos.y() + 6, x, 1000, P(mix("#6B7280", "#2A303C", night), 1, stroke=6))
                break
    if lit > 0:
        m = skia.PathMeasure(p, False)
        for d in range(0, int(m.getLength()), 40):
            pos, _ = m.getPosTan(d)
            add_glow(c, pos.x(), pos.y() - 6, 14, "#FDE68A", 0.8 * lit)


def park(c, t, night=0.0, lit=0.0, train_x=700, speed=0.0, glint=0.0, goggles=1.0):
    sky(c, night)
    if night > 0.3:
        v2.moon(c, 860, 330, 46, a=night)
    hill_track(c, night, lit)
    red_roof(c, night, lit)
    c.drawRect(R(0, 960, W, 300), lin_paint(0, 960, 0, 1250, [mix(SAND[0], "#3A2C1E", night * 0.7), mix(SAND[2], "#1A130C", night * 0.7)]))
    for k in range(12):                                  # dunes and sand ripples
        yy = 990 + k * 22
        c.drawLine(0, yy, W, yy + 8 * math.sin(k), P(mix(SAND[1], "#2A1E14", night), 0.35, stroke=3))
    for (x, s) in ((60, 0.9), (420, 0.75), (1010, 1.0)):
        palm(c, x, 968, s, night)
    rail(c, RAIL_Y, night=night)
    streaks(c, -60, W + 60, RAIL_Y - 120, RAIL_Y - 10, t, clamp((speed - 40) / 160), seed=5)
    train(c, train_x, RAIL_Y, t, speed=clamp(speed / 200), glint=glint, goggles=goggles)
    if lit > 0:
        for k in range(10):
            add_glow(c, 40 + k * 110, RAIL_Y + 14, 12, "#FDE68A", 0.7 * lit)
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#140E08", "#050302"]))


# ====================================================================================== the launch set
def ghost_hill(c, t, k=1.0, cross=0.0):
    if k <= 0:
        return
    p = skia.Path()
    p.moveTo(60, RAIL_S)
    p.cubicTo(260, RAIL_S, 360, 250, 540, 250)
    p.cubicTo(720, 250, 820, RAIL_S, 1020, RAIL_S)
    m = skia.PathMeasure(p, False)
    seg = skia.Path()
    m.getSegment(0, m.getLength() * clamp(k), seg, True)
    pp = P("#F8FAFC", 0.85, stroke=7)
    pp.setPathEffect(skia.DashPathEffect.Make([22, 14], t * 40))
    c.drawPath(seg, pp)
    if k >= 1:                                           # a tower of 70 floors beside it, for size
        for f in range(70):
            y = RAIL_S - 10 - f * 8.9
            c.drawRect(R(880, y - 8, 110, 6), P("#CBD5E1", 0.45))
    if cross > 0:
        q = e_back(clamp(cross))
        c.drawLine(540 - 160 * q, 520 - 160 * q, 540 + 160 * q, 520 + 160 * q, P(WARN, 1, stroke=18))
        c.drawLine(540 + 160 * q, 520 - 160 * q, 540 - 160 * q, 520 + 160 * q, P(WARN, 1, stroke=18))


def carrier(c, x, y, r, t, k=0.0, a=1.0):
    """Inset: a jet flung off a ship's deck by a catapult."""
    if a <= 0:
        return
    c.save()
    c.clipRRect(skia.RRect.MakeOval(R(x - r, y - r, 2 * r, 2 * r)), skia.ClipOp.kIntersect, True)
    vrect(c, x - r, y - r, 2 * r, 2 * r, ["#3B5A8C", "#C7687A"], a=a)
    c.drawRect(R(x - r, y + 50, 2 * r, r), P("#1E3A5F", a))
    deck = skia.Path()
    deck.moveTo(x - r, y + 20)
    deck.lineTo(x + r - 40, y + 20)
    deck.lineTo(x + r - 10, y + 50)
    deck.lineTo(x - r, y + 50)
    deck.close()
    c.drawPath(deck, P("#4B5563", a))
    dashed(c, x - r, y + 22, x + r - 40, y + 22, "#FACC15", 3, 12, 8, 0, a)
    q = clamp(k)
    jx = lerp(x - r + 40, x + r + 120, q * q)
    jy = y + 6 - 60 * clamp((q - 0.55) / 0.45)
    c.save()
    c.translate(jx, jy)
    c.rotate(-12 * clamp((q - 0.55) / 0.45))
    body = skia.Path()
    body.moveTo(70, 0)
    body.lineTo(30, -10)
    body.lineTo(-50, -10)
    body.lineTo(-62, -30)
    body.lineTo(-70, -30)
    body.lineTo(-66, 2)
    body.close()
    c.drawPath(body, P("#CBD5E1", a))
    wing = skia.Path()
    wing.moveTo(10, -4)
    wing.lineTo(-30, 18)
    wing.lineTo(-44, 18)
    wing.lineTo(-24, -4)
    wing.close()
    c.drawPath(wing, P("#94A3B8", a))
    c.drawOval(R(22, -14, 26, 10), P("#38BDF8", a))
    if q > 0.05:
        v2.flame(c, -66, -6, 12, 46, t, 1.0, seed=3, ang=180.0)
    c.restore()
    if 0.05 < q < 0.7:
        for j in range(6):
            c.drawCircle(jx - 90 - j * 22, y + 14, 10 + j * 3, P("#F8FAFC", 0.4 * a * (1 - j / 6)))
    c.restore()
    c.drawCircle(x, y, r, P("#F8FAFC", 0.9 * a, stroke=6))


def power_pole(c, t, spark=0.0, need=0.0, a=1.0):
    if a <= 0:
        return
    x = 170
    c.drawRect(R(x - 14, 380, 28, RAIL_S - 380), P("#6B4A2B", a))
    c.drawRect(R(x - 90, 410, 180, 18), P("#6B4A2B", a))
    for dx in (-76, 0, 76):
        c.drawCircle(x + dx, 404, 9, P("#CBD5E1", a))
        p = skia.Path()
        p.moveTo(x + dx, 404)
        p.quadTo(x + dx + 380, 480 + spark * 40 * math.sin(t * 40 + dx), W + 40, 430)
        c.drawPath(p, P("#111827", a, stroke=5))
        if spark > 0:
            c.drawPath(p, P("#FDE68A", 0.8 * spark * (0.5 + 0.5 * math.sin(t * 50 + dx)), stroke=7))
    if spark > 0:
        v2set.sparks_shower(c, x + 76, 404, t, 0.0, dur=0.6, n=14, speed=360)
        add_glow(c, x + 76, 404, 160, "#FDE68A", 0.55 * spark)
    if need > 0:                                         # what the wires give against what one launch needs
        gx, gy, gw = 560, 470, 430
        glass(c, gx - 20, gy - 20, gw + 40, 220, r=26, a=need)
        for j, (frac, col) in enumerate(((0.28, GOOD), (min(1.0, 0.28 + 0.9 * need), WARN))):
            yy = gy + 40 + j * 90
            c.drawRRect(rr(gx, yy, gw, 34, 17), P("#FFFFFF", 0.14 * need))
            c.drawRRect(rr(gx, yy, gw * frac, 34, 17), P(col, need))
            add_glow(c, gx + gw * frac, yy + 17, 30, col, 0.6 * need)
        c.drawCircle(gx + 30, gy + 57, 18, P("#0F172A", need))
        c.drawLine(gx + 24, gy + 47, gx + 36, gy + 57, P("#FDE68A", need, stroke=4))
        c.drawLine(gx + 36, gy + 57, gx + 26, gy + 68, P("#FDE68A", need, stroke=4))


def tanks(c, t, fill=0.0, release=0.0, a=1.0):
    """The pump room cut open: tanks with oil below and gas above; the oil squeezes the gas like a spring."""
    if a <= 0:
        return
    c.drawRRect(rr(60, 980, 960, 250, 30), P("#111827", 0.92 * a))
    c.drawRRect(rr(60, 980, 960, 250, 30), P("#475569", a, stroke=4))
    for i, x in enumerate((200, 380, 560)):
        top, bot = 1000, 1210
        lvl = lerp(0.25, 0.78, clamp(fill)) - 0.5 * clamp(release)
        oil_y = bot - (bot - top) * lvl
        c.drawRRect(rr(x - 60, top, 120, bot - top, 40), P("#1E293B", a))
        c.drawRect(R(x - 58, oil_y, 116, bot - oil_y - 2), P("#D97706", 0.9 * a))
        c.drawRect(R(x - 58, top + 4, 116, oil_y - top - 4), P("#38BDF8", 0.35 * a))
        sp = skia.Path()                                 # the gas as a spring
        n = 8
        for k in range(n + 1):
            yy = lerp(top + 10, oil_y - 6, k / n)
            xx = x + (24 if k % 2 else -24) * (0 < k < n)
            (sp.moveTo if k == 0 else sp.lineTo)(xx, yy)
        c.drawPath(sp, P("#E0F2FE", 0.9 * a, stroke=5))
        c.drawRRect(rr(x - 60, top, 120, bot - top, 40), P("#94A3B8", a, stroke=4))
    # the pump and the winch drum
    c.drawRRect(rr(680, 1060, 110, 110, 20), P("#334155", a))
    ang = t * 600 * clamp(fill) * (1 - clamp(release)) + t * 2400 * clamp(release)
    for k in range(4):
        aa = math.radians(ang + k * 90)
        c.drawLine(735, 1115, 735 + math.cos(aa) * 40, 1115 + math.sin(aa) * 40, P("#94A3B8", a, stroke=6))
    c.drawCircle(900, 1105, 70, P("#475569", a))
    for k in range(6):
        aa = math.radians(ang * 2 + k * 60)
        c.drawLine(900, 1105, 900 + math.cos(aa) * 64, 1105 + math.sin(aa) * 64, P("#CBD5E1", a, stroke=4))
    if release > 0:
        add_glow(c, 900, 1105, 120, HILITE, 0.5 * release)


def catch_cart(c, x, y, hook=1.0, a=1.0):
    """The little cart under the train, its hook (the launch dog) up into the middle car."""
    c.drawRRect(rr(x - 60, y + 14, 120, 26, 8), P("#F59E0B", a))
    c.drawRRect(rr(x - 60, y + 14, 120, 26, 8), P("#78350F", a, stroke=3))
    add_glow(c, x, y + 27, 70, HILITE, 0.35 * a)
    for wx in (x - 40, x + 40):
        c.drawCircle(wx, y + 42, 8, P("#6B7280", a))
    hy = y + 14 - 24 * clamp(hook)
    c.drawLine(x, y + 16, x + 10, hy, P(HILITE, a, stroke=7))


def launch_scene(c, t, train_x=700, speed=0.0, sky_night=0.2, cable=None, yank=0.0, cart=None, cart_hook=1.0):
    sky(c, sky_night)
    c.save()
    c.translate(540, SY_L)
    c.scale(Z_L, Z_L)
    c.translate(-CX_L, -CY_L)
    c.drawRect(R(-400, 960, 2000, 500), lin_paint(0, 960, 0, 1250, [SAND[1], SAND[2]]))
    for k in range(8):
        c.drawLine(-400, 990 + k * 26, 1600, 994 + k * 26, P(SAND[2], 0.35, stroke=3))
    rail(c, RAIL_Y, x0=-400, x1=1600)
    streaks(c, -400, 1600, RAIL_Y - 120, RAIL_Y - 10, t, clamp((speed - 40) / 160), seed=8)
    if cable is not None:                                # a cable tied to the nose, to a post at the far end
        nose = train_x + 46
        c.drawLine(nose, RAIL_Y - 24, cable, RAIL_Y - 24, P("#E5E7EB", 1, stroke=4))
        c.drawRect(R(cable - 10, RAIL_Y - 70, 30, 80), P("#475569"))
    if cart is not None:
        catch_cart(c, cart, RAIL_Y, cart_hook)
    c.save()
    if yank > 0:
        c.rotate(-8 * yank, train_x, RAIL_Y)
    train(c, train_x, RAIL_Y, t, speed=clamp(speed / 200))
    c.restore()
    c.restore()
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#140E08", "#050302"]))


# ====================================================================================== the brakes
def brakes_scene(c, t, train_x, speed, hot=0.0, magnets=0.0):
    sky(c, 0.35)
    c.save()
    c.translate(540, SY_L)
    c.scale(Z_L, Z_L)
    c.translate(-CX_L, -CY_L)
    c.drawRect(R(-400, 960, 2000, 500), lin_paint(0, 960, 0, 1250, [SAND[1], SAND[2]]))
    rail(c, RAIL_Y, x0=-400, x1=1600)
    if magnets > 0:                                      # rows of magnets along the brake run
        for k in range(18):
            x = -100 + k * 70
            col = "#3B82F6" if k % 2 else "#EF4444"
            c.drawRRect(rr(x - 24, RAIL_Y + 22, 48, 36, 8), P(col, magnets))
            c.drawRRect(rr(x - 24, RAIL_Y + 22, 48, 36, 8), P("#F8FAFC", 0.6 * magnets, stroke=3))
    streaks(c, -400, 1600, RAIL_Y - 120, RAIL_Y - 10, t, clamp((speed - 40) / 160), seed=9)
    train(c, train_x, RAIL_Y, t, speed=clamp(speed / 200), fins=magnets)
    if hot > 0:                                          # friction pads glowing red-hot
        for k in range(4):
            x = train_x - 120 - k * 156
            c.drawRRect(rr(x - 36, RAIL_Y + 6, 72, 22, 6), P(mix("#6B7280", "#FF3B1F", hot)))
            add_glow(c, x, RAIL_Y + 16, 70, "#FF5A1F", 0.7 * hot)
            v2set.sparks_shower(c, x, RAIL_Y + 16, t, 0.0, dur=0.5, n=8, speed=420, seed=k)
        if hot > 0.4:
            v2.smoke(c, train_x - 300, RAIL_Y + 10, t, 0.0, rate=8, life=1.4, spread=(300, -30), rise=-60, size=(10, 40),
                     col="#6B7280")
    if magnets > 0 and speed > 5:                        # eddy swirls where the fins pass the magnets
        for k in range(4):
            x = train_x - 120 - k * 156
            for j in range(3):
                q = (t * 3 + j * 0.33) % 1.0
                c.drawCircle(x, RAIL_Y + 30, 12 + q * 40, P("#93C5FD", 0.6 * (1 - q) * magnets, stroke=3))
    c.restore()
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#140E08", "#050302"]))


# ====================================================================================== the goggles close up
def face(c, t, sand=0.0, fly=0.0, bounce=0.0):
    vrect(c, 0, 0, W, 1250, ["#1D2F5E", "#C7687A", "#F4A95E"])
    streaks(c, -60, W + 60, 260, 1180, t, 0.9, seed=12)
    c.save()
    c.translate(470, 720)
    c.scale(2.0, 2.0)
    # helmet-free head in profile, hair flying, big goggles
    for k in range(6):
        p = skia.Path()
        p.moveTo(-60, -110 + k * 22)
        p.quadTo(-170, -120 + k * 22 + 10 * math.sin(t * 18 + k), -280, -90 + k * 26)
        c.drawPath(p, P("#2B2530", 1, stroke=16))
    c.drawCircle(0, -40, 120, P(SKIN[0]))
    c.drawArc(R(-120, -165, 240, 170), 180, 170, True, P("#2B2530"))
    nose = skia.Path()
    nose.moveTo(112, -40)
    nose.lineTo(148, 4)
    nose.lineTo(110, 14)
    nose.close()
    c.drawPath(nose, P(SKIN[0]))
    c.drawArc(R(60, 40, 70, 40), 10, 140, False, P("#7F1D1D", 1, stroke=6))
    c.drawCircle(-30, -20, 26, P(SKIN[1]))
    c.drawLine(-120, -62, 80, -62, P("#111827", 1, stroke=22))
    c.drawRRect(rr(50, -104, 110, 84, 30), P("#1E293B"))
    c.drawRRect(rr(50, -104, 110, 84, 30), P("#F59E0B", 1, stroke=10))
    c.drawLine(78, -90, 112, -50, P("#BAE6FD", 0.8, stroke=8))
    c.restore()
    if sand > 0:                                         # sand grains racing at the goggles
        rng = random.Random(4)
        for j in range(40):
            q = (t * rng.uniform(1.2, 2.2) + rng.random()) % 1.0
            x = lerp(W + 40, 690, q)
            y = 588 + rng.uniform(-160, 160) * (1 - q)
            c.drawCircle(x, y, rng.uniform(3, 6), P("#E8C48A", 0.9 * sand))
    if fly > 0:                                          # the fly: in, tink, and out
        q = clamp(fly)
        if bounce <= 0:
            fx, fy = lerp(W + 60, 700, e_in(q)), lerp(420, 588, q)
        else:
            b = clamp(bounce)
            fx, fy = lerp(700, 1000, e_out(b)), lerp(588, 300, e_out(b)) + 60 * math.sin(b * 9)
        c.save()
        c.translate(fx, fy)
        c.rotate(t * 900 * (1 if bounce > 0 else 0))
        c.drawOval(R(-16, -10, 32, 20), P("#111827"))
        c.drawOval(R(-8, -24, 18, 16), P("#BAE6FD", 0.7))
        c.drawOval(R(-2, -26, 18, 16), P("#BAE6FD", 0.7))
        c.restore()
        if 0 < bounce < 0.4:
            add_glow(c, 700, 588, 90, "#FFFFFF", 0.9 * (1 - bounce / 0.4))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#140E08", "#050302"]))


# ====================================================================================== the tag
def side_car(c, x, y, s, col, a=1.0, phone=0.0, t=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(-110, -10)
    body.lineTo(-110, -48)
    body.lineTo(-60, -52)
    body.lineTo(-30, -92)
    body.lineTo(50, -92)
    body.lineTo(80, -52)
    body.lineTo(110, -46)
    body.lineTo(110, -10)
    body.close()
    c.drawPath(body, P(col, a))
    c.drawPath(body, P("#0B0E18", 0.5 * a, stroke=3))
    c.drawRect(R(-22, -84, 30, 30), P("#1E293B", a))
    c.drawRect(R(14, -84, 32, 30), P("#1E293B", a))
    for wx in (-66, 66):
        c.drawCircle(wx, -6, 22, P("#111827", a))
        c.drawCircle(wx, -6, 9, P("#6B7280", a))
    if phone > 0:
        c.drawCircle(4, -66, 14, P("#2B2530", a))
        add_glow(c, 24, -62, 40, "#93C5FD", 0.9 * phone)
        c.drawRect(R(18, -70, 10, 16), P("#E0F2FE", phone))
    c.restore()


def tag_scene(c, t, ar=False, wait=0.0, honk=0.0):
    vrect(c, 0, 0, W, 1250, ["#0B1430", "#1A2246", "#2A2350"])
    v2.stars(c, W, H, t, 0.6, n=120)
    c.drawRect(R(0, 960, W, 300), lin_paint(0, 960, 0, 1250, ["#2A2F3D", "#141822"]))
    for k in range(8):
        c.drawRect(R(k * 150 + (t * 0) % 150, 1080, 80, 10), P("#E5E7EB", 0.5))
    if not ar:                                           # a drive-thru: a line of cars stuck at the menu board
        c.drawRect(R(840, 640, 160, 300), P("#3F2A1E"))
        c.drawRect(R(856, 656, 128, 170), P("#F59E0B", 0.9))
        for k in range(4):
            c.drawRect(R(872, 676 + k * 36, 96, 14), P("#7C2D12", 0.8))
        add_glow(c, 920, 740, 160, "#F59E0B", 0.35)
        for i, (x, col) in enumerate(((700, "#3B82F6"), (470, "#10B981"), (240, "#EF4444"), (10, "#A855F7"))):
            side_car(c, x, 1010, 1.0, col)
        cx, cy = 300, 560                                # a clock spinning while nothing moves
        c.drawCircle(cx, cy, 90, P("#F8FAFC", 0.9))
        c.drawCircle(cx, cy, 90, P("#0F172A", 1, stroke=8))
        c.drawLine(cx, cy, cx + 60 * math.cos(t * 6), cy + 60 * math.sin(t * 6), P("#0F172A", 1, stroke=8))
        c.drawLine(cx, cy, cx + 40 * math.cos(t * 0.5), cy + 40 * math.sin(t * 0.5), P(WARN, 1, stroke=10))
    else:                                                # a green light, and the car in front on his phone
        c.drawRect(R(880, 420, 26, 540), P("#374151"))
        c.drawRRect(rr(840, 420, 106, 280, 24), P("#111827"))
        for k, col in enumerate(("#7F1D1D", "#78350F", "#22C55E")):
            c.drawCircle(893, 470 + k * 90, 34, P(col))
        add_glow(c, 893, 650, 120, "#22C55E", 0.6)
        side_car(c, 640, 1010, 1.2, "#E5E7EB", phone=1.0, t=t)
        side_car(c, 240, 1010, 1.2, "#3B82F6")
        if honk > 0:
            for j in range(3):
                q = (t * 2 + j * 0.33) % 1.0
                c.drawArc(R(360 - 40 - q * 60, 900 - 40 - q * 60, 80 + q * 120, 80 + q * 120), -40, 80, False,
                          P(HILITE, honk * (1 - q), stroke=6))
    c.drawRect(R(0, 1250, W, H - 1250), lin_paint(0, 1250, 0, 1500, ["#0B0E18", "#05070C"]))


class FormulaRossa(EpisodeV2):
    BUILD_NO = 113
    FIRST_SET = "park"
    CLEAR = "#070B1C"
    COVER_T = ("closer", 0.55)
    STAT_Y = 1090
    TITLE = {"en": "FORMULA ROSSA", "ar_sa": "فورمولا روسا"}
    EMPH = {"en": ["ROLLER", "COASTER", "WEAR", "SAFETY", "GOGGLES", "HITS", "TWO-FORTY", "FIVE", "SECONDS", "HILL",
                   "CATAPULT", "FLINGS", "JET", "SHIP", "PULLING", "HARD", "POWER", "WIRES", "PUMPS", "SQUEEZE", "OIL",
                   "TANKS", "GAS", "GIANT", "SPRING", "HOOKED", "FLY", "FREE", "LITTLE", "CART", "UNDERNEATH", "LETS",
                   "FULL", "SPEED", "STOPPING", "BRAKES", "RED-HOT", "MAGNETS", "TOUCHING", "FOLLOW", "SODA", "CAN",
                   "STRONGER", "ANSWER", "DESERT", "SAND", "BUGS", "HURTS", "ZERO", "FOUR", "POINT", "NINE", "GUINNESS",
                   "RECORD", "CONGRATS", "FORMULA", "ROSSA", "YOURSELF", "DRIVE-THRU", "MOVED"],
            "ar_sa": ["قطار", "الموت", "أبوظبي", "يلبسك", "نظارات", "حماية", "يوصل", "ميتين", "وأربعين", "خمس", "ثواني",
                      "النظارات", "طلعة", "فينقذف", "طيارة", "حاملة", "سحبة", "كهربا", "الأسلاك", "مضخات", "زيت",
                      "خزانات", "غاز", "زنبرك", "مربوط", "يطير", "حر", "عربية", "تسحبه", "وتفكه", "سرعة", "الفرامل",
                      "بتحمر", "مغناطيسات", "تلمسه", "متابعة", "علبة", "مليانة", "الجواب", "رمل", "الصحرا", "والحشرات",
                      "الذبانة", "توجع", "صفر", "غينيس", "مبروك", "فورمولا", "روسا", "الإشارة", "جواله"]}
    KEYS = {"ar_sa": {
        ("hook", "COASTER"): "قطار", ("hook", "WEAR"): "يلبسك", ("hook", "GOGGLES"): "نظارات",
        ("break1", "HITS"): "يوصل", ("break1", "SECONDS"): "ثواني", ("break1", "GOGGLES"): "النظارات",
        ("fix1", "HILL"): "طلعة", ("fix1", "CATAPULT"): "فينقذف", ("fix1", "JET"): "طيارة", ("fix1", "SHIP"): "حاملة",
        ("break2", "PULLING"): "سحبة", ("break2", "POWER"): "كهربا", ("break2", "WIRES"): "الأسلاك",
        ("fix2", "PUMPS"): "مضخات", ("fix2", "OIL"): "زيت", ("fix2", "GAS"): "غاز", ("fix2", "SPRING"): "زنبرك",
        ("break3", "HOOKED"): "مربوط", ("break3", "FLY"): "يطير",
        ("fix3", "CART"): "عربية", ("fix3", "PULLS"): "تسحبه", ("fix3", "LETS"): "وتفكه",
        ("break4", "STOPPING"): "توقف", ("break4", "BRAKES"): "الفرامل", ("break4", "RED"): "بتحمر",
        ("fix4", "MAGNETS"): "مغناطيسات", ("fix4", "TOUCHING"): "تلمسه",
        ("cta", "FOLLOW"): "متابعة", ("cta", "FULL"): "مليانة",
        ("reveal", "ANSWER"): "الجواب", ("reveal", "SAND"): "رمل", ("reveal", "BUGS"): "والحشرات",
        ("reveal", "FLY"): "الذبانة", ("reveal", "HURTS"): "توجع",
        ("stat", "ZERO"): "صفر", ("stat", "FOUR"): "أربعة", ("stat", "GUINNESS"): "غينيس",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "ZERO"): "خمس", ("tag", "DRIVE"): "الإشارة", ("tag", "MOVED"): "جواله"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the soda can"),
                   "stat": [("0-240", "KM/H"), ("4.9", "SECONDS"), ("1", "WORLD RECORD")],
                   "L": {"goggles": "SAFETY GOGGLES?!", "fast": "0-240 KM/H IN UNDER 5 S", "why": "WHY THE GOGGLES?",
                         "hill": "A 200 M HILL?", "catapult": "A CATAPULT, LIKE A JET", "power": "TOO MUCH POWER!",
                         "spring": "OIL SQUEEZES GAS: A SPRING", "hooked": "STILL HOOKED ON!", "cart": "A CART PULLS, THEN LETS GO",
                         "brakes": "BRAKES WOULD GLOW!", "magnets": "MAGNETS, NO TOUCHING", "sand": "SAND AND BUGS!",
                         "name": "FORMULA ROSSA", "drive": "THE DRIVE-THRU..."}},
            "ar_sa": {"follow": ("تابعني", "الجاي: علبة الغازي"),
                      "stat": [("0-240", "كيلو بالساعة"), ("4.9", "ثانية"), ("1", "رقم قياسي")],
                      "L": {"goggles": "نظارات حماية؟!", "fast": "ميتين وأربعين بخمس ثواني", "why": "ليش النظارات؟",
                            "hill": "طلعة ميتين متر؟", "catapult": "ينقذف مثل الطيارة", "power": "كهربا مرة كثير!",
                            "spring": "الزيت يضغط الغاز: زنبرك", "hooked": "للحين مربوط!", "cart": "عربية تسحبه وتفكه",
                            "brakes": "الفرامل بتحمر!", "magnets": "مغناطيس بدون لمس", "sand": "رمل وحشرات!",
                            "name": "فورمولا روسا", "drive": "واللي قدامك..."}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "coaster": ("hook", "COASTER", 0.3), "wear": ("hook", "WEAR", 0.55), "goggles": ("hook", "GOGGLES", 0.9),
            "hits": ("break1", "HITS", 0.1), "seconds": ("break1", "SECONDS", 0.5), "why": ("break1", "GOGGLES", 0.85),
            "hill": ("fix1", "HILL", 0.15), "catapult": ("fix1", "CATAPULT", 0.45), "jet": ("fix1", "JET", 0.75),
            "ship": ("fix1", "SHIP", 0.95),
            "pulling": ("break2", "PULLING", 0.1), "power": ("break2", "POWER", 0.45), "wires": ("break2", "WIRES", 0.85),
            "pumps": ("fix2", "PUMPS", 0.1), "oil": ("fix2", "OIL", 0.3), "gas": ("fix2", "GAS", 0.55),
            "spring": ("fix2", "SPRING", 0.9),
            "hooked": ("break3", "HOOKED", 0.4), "fly": ("break3", "FLY", 0.8),
            "cart": ("fix3", "CART", 0.25), "pulls": ("fix3", "PULLS", 0.5), "lets": ("fix3", "LETS", 0.7),
            "stopping": ("break4", "STOPPING", 0.15), "brakes": ("break4", "BRAKES", 0.6), "red": ("break4", "RED", 0.85),
            "magnets": ("fix4", "MAGNETS", 0.15), "touching": ("fix4", "TOUCHING", 0.85),
            "follow": ("cta", "FOLLOW", 0.1), "full": ("cta", "FULL", 0.95),
            "answer": ("reveal", "ANSWER", 0.05), "sand": ("reveal", "SAND", 0.25), "bugs": ("reveal", "BUGS", 0.4),
            "flyR": ("reveal", "FLY", 0.8), "hurts": ("reveal", "HURTS", 0.92),
            "s1": ("stat", "ZERO", 0.05), "s2": ("stat", "FOUR", 0.4), "s3": ("stat", "GUINNESS", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_zero": ("tag", "ZERO", 0.05), "t_drive": ("tag", "DRIVE", 0.6), "t_moved": ("tag", "MOVED", 0.9)})
        T["go"] = T["goggles"] + 0.25                    # the launch in the hook
        T["fast1"] = max(T["hits"], s("break1") + 0.2)
        T["jet1"] = max(T["jet"], T["catapult"] + 0.4)
        T["power1"] = max(T["power"], s("break2") + 0.3)
        T["spring1"] = max(T["spring"], T["gas"] + 0.4)
        T["hooked1"] = max(T["hooked"], s("break3") + 0.3)
        T["lets1"] = max(T["lets"], T["pulls"] + 0.4)
        T["red1"] = max(T["red"], s("break4") + 0.4)
        T["touch1"] = max(T["touching"], T["magnets"] + 0.5)
        T["bounce"] = max(T["flyR"], T["sand"] + 0.8)
        T["t_drive1"] = max(T["t_drive"], s("tag") + 0.9)
        # ---- sets
        self.cut(s("break1") - 0.12, "launch", 1)
        self.cut(s("break4") - 0.12, "brakes", -1)
        self.cut(s("cta") - 0.12, "park", 1)
        self.cut(s("reveal") - 0.12, "goggles", -1)
        self.cut(s("stat") - 0.12, "park", 1)
        self.cut(s("tag") - 0.2, "tag", -1)
        self.spans = [(T["fast1"], T["jet1"]), (T["power1"], T["spring1"]), (T["hooked1"], T["lets1"]), (T["red1"], T["touch1"])]
        self.shakes = [(T["go"], 0.6, 9), (T["fast1"], 0.3, 5), (T["jet1"], 0.4, 7), (T["power1"], 0.35, 6),
                       (T["spring1"] + 0.3, 0.4, 7), (T["hooked1"] + 0.3, 0.45, 9), (T["lets1"], 0.4, 7), (T["red1"], 0.35, 6),
                       (T["bounce"], 0.3, 5), (s("closer") + 0.2, 0.35, 6), (T["t_moved"], 0.3, 5)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    # ------------------------------------------------------------------ set: park (hook, cta, stat, closer)
    def draw_park(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            go = prog(t, T["go"], T["go"] + 1.4)
            zin = e_io(prog(t, T["wear"] - 0.3, T["goggles"] + 0.1))
            out = e_io(prog(t, T["go"] + 0.1, T["go"] + 0.9))
            z = lerp(lerp(2.6, 3.4, zin), 1.0, out)
            tx = 760 + 1400 * go * go                    # the nose runs off to the right
            hx = 760 - CL - 46 + 104                     # the front rider when the train stands
            fx, fy = lerp(hx + 6, 540, out), lerp(RAIL_Y - 66, 760, out)
            c.save()
            c.translate(540, 760)
            c.scale(z, z)
            c.translate(-fx, -fy)
            park(c, t, train_x=tx, speed=240 * go, glint=prog(t, T["goggles"] - 0.3, T["goggles"]) *
                 (1 - prog(t, T["goggles"] + 0.3, T["goggles"] + 0.7)))
            c.restore()
            speedo(c, 880, 520, 240 * smooth(go), a=prog(t, T["go"], T["go"] + 0.3))
        elif ph == "stat":
            q = prog(t, s("stat"), T["s2"] + 0.6)
            park(c, t, night=0.15, train_x=lerp(-200, 1500, q * q), speed=240 * q)
            speedo(c, 880, 560, 240 * smooth(q), a=prog(t, s("stat"), s("stat") + 0.3))
        elif ph == "closer":
            c.save()
            c.translate(540, 760)
            c.scale(1.35, 1.35)
            c.translate(-600, -760)
            park(c, t, night=1.0, lit=1.0, train_x=880, speed=0.0)
            c.restore()
        else:                                            # cta
            park(c, t, night=0.5, lit=0.6, train_x=760, speed=0.0)

    def ui_park(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "goggles", T["goggles"] - 0.3, s("break1") + 0.1, accent=HILITE, size=60)
        elif ph == "closer":
            self.chip(540, 300, "name", s("closer") + 0.2, self.duration + 1, accent=HILITE, size=60)

    # ------------------------------------------------------------------ set: launch (break1 .. fix3)
    def draw_launch(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break1":
            launch_scene(c, t, train_x=700, speed=0.0)
            speedo(c, 880, 520, 240 * smooth(prog(t, T["hits"], T["seconds"] + 0.5)), a=prog(t, s("break1"), s("break1") + 0.3))
        elif ph == "fix1":
            launch_scene(c, t, train_x=700, speed=0.0)
            ghost_hill(c, t, prog(t, T["hill"] - 0.3, T["hill"] + 0.5), cross=prog(t, T["catapult"] - 0.4, T["catapult"]))
            carrier(c, 790, 560, 170, t, k=prog(t, T["jet"] - 0.3, T["ship"] + 0.5), a=prog(t, T["catapult"], T["catapult"] + 0.3))
        elif ph == "break2":
            launch_scene(c, t, train_x=700, speed=0.0)
            power_pole(c, t, spark=prog(t, T["power"] - 0.2, T["power1"] + 0.2), need=prog(t, T["pulling"], T["power"] + 0.4))
        elif ph == "fix2":
            rel = prog(t, T["spring1"], T["spring1"] + 0.5)
            q = prog(t, T["spring1"] + 0.1, T["spring1"] + 1.4)
            launch_scene(c, t, train_x=lerp(700, 2400, q * q), speed=240 * q)
            tanks(c, t, fill=prog(t, T["pumps"] - 0.2, T["spring1"]), release=rel)
        elif ph == "break3":
            q = prog(t, s("break3"), T["hooked1"] + 0.3)
            x = lerp(300, 760, e_out(q))
            launch_scene(c, t, train_x=x, speed=200 * (1 - q), cable=870, yank=prog(t, T["hooked1"], T["hooked1"] + 0.3) *
                         (1 - 0.5 * prog(t, T["hooked1"] + 0.3, T["fly"] + 0.5)))
        else:                                            # fix3
            q = prog(t, T["cart"] - 0.3, T["lets1"])
            x = lerp(420, 760, e_in(q))
            let = prog(t, T["lets1"] - 0.1, T["lets1"] + 0.1)
            free = prog(t, T["lets1"], T["lets1"] + 0.9)
            launch_scene(c, t, train_x=x + 1200 * free * free, speed=240 * max(q * 0.8, free),
                         cart=x - 46 - CL / 2 - 200 * e_out(free), cart_hook=1 - let)

    def ui_launch(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break1":
            self.chip(540, 300, "fast", T["hits"] - 0.2, T["why"] - 0.3, accent=WARN, size=50)
            self.chip(540, 300, "why", T["why"] - 0.3, s("fix1") - 0.1, accent=HILITE, size=58)
            self.badge("alert", T["fast1"], s("fix1") - 0.2, x=160, y=470)
            self.red(T["fast1"], 1.2)
        elif ph == "fix1":
            self.chip(540, 300, "hill", T["hill"] - 0.2, T["catapult"] - 0.1, accent=WARN, size=60)
            self.chip(540, 300, "catapult", T["catapult"] - 0.1, s("break2") - 0.15, accent=GOOD, size=52)
            self.badge("check", T["jet1"], s("break2") - 0.15, x=160, y=470)
        elif ph == "break2":
            self.chip(540, 300, "power", T["power"] - 0.2, s("fix2") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["power1"], s("fix2") - 0.2, x=880, y=470)
            self.red(T["power1"], 1.2)
        elif ph == "fix2":
            self.chip(540, 300, "spring", T["oil"] - 0.2, s("break3") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["spring1"], s("break3") - 0.15, x=160, y=470)
        elif ph == "break3":
            self.chip(540, 300, "hooked", T["hooked"] - 0.2, s("fix3") - 0.15, accent=WARN, size=60)
            self.badge("alert", T["hooked1"], s("fix3") - 0.2, x=160, y=470)
            self.red(T["hooked1"], 1.2)
        else:
            self.chip(540, 300, "cart", T["cart"] - 0.2, s("break4") - 0.15, accent=GOOD, size=48)
            self.badge("check", T["lets1"], s("break4") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: brakes (break4, fix4)
    def draw_brakes(self, c, t):
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "break4":
            q = prog(t, s("break4"), T["red1"] + 0.8)
            brakes_scene(c, t, train_x=lerp(200, 760, e_out(q)), speed=240 * (1 - q), hot=prog(t, T["brakes"] - 0.2, T["red1"]))
            speedo(c, 880, 520, 240 * (1 - q), a=1.0)
        else:
            q = prog(t, T["magnets"] - 0.2, T["touch1"] + 0.6)
            brakes_scene(c, t, train_x=lerp(150, 760, e_out(q)), speed=240 * (1 - e_out(q)), magnets=prog(t, T["magnets"] - 0.3, T["magnets"] + 0.1))
            speedo(c, 880, 520, 240 * (1 - e_out(q)), a=1.0)

    def ui_brakes(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "break4":
            self.chip(540, 300, "brakes", T["brakes"] - 0.2, s("fix4") - 0.15, accent=WARN, size=58)
            self.badge("alert", T["red1"], s("fix4") - 0.2, x=160, y=470)
            self.red(T["red1"], 1.2)
        else:
            self.chip(540, 300, "magnets", T["magnets"] - 0.2, s("cta") - 0.15, accent=GOOD, size=54)
            self.badge("check", T["touch1"], s("cta") - 0.15, x=160, y=470)

    # ------------------------------------------------------------------ set: goggles (reveal)
    def draw_goggles(self, c, t):
        T, s = self.T, self.tl.s
        face(c, t, sand=prog(t, T["sand"] - 0.2, T["sand"] + 0.3), fly=prog(t, T["bugs"] - 0.2, T["bounce"]),
             bounce=prog(t, T["bounce"], T["bounce"] + 1.2))

    def ui_goggles(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "sand", T["sand"] - 0.2, s("stat") - 0.15, accent=HILITE, size=64)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        tag_scene(c, t, ar=self.rtl, honk=prog(t, T["t_moved"] - 0.3, T["t_moved"] + 0.2))

    def ui_tag(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "drive", T["t_drive1"] - 0.3, self.duration + 1, accent=WARN, size=60)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#0B1430", "#1A2246"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (0.05, sfx.hum(2.0, 70.0), -20), (T["goggles"], sfx.ding(), -8),
              (T["go"] - 0.1, sfx.charge_up(0.5), -10), (T["go"], sfx.whoosh(1.2, True, 62), -4), (T["go"], rumble(2.0, 63), -10)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.45, True, 64), -6), (T["hits"], sfx.riser(1.0, 65), -12),
               (T["fast1"] + 0.6, sfx.alarm(3, 820.0), -14)]
        ev += [(T["hill"], sfx.creak(0.8, 66), -12), (T["catapult"], sfx.thunk(67), -8), (T["jet"], sfx.whoosh(0.9, True, 68), -6),
               (T["jet1"] + 0.3, sfx.chime(), -6)]
        ev += [(T["power"], sfx.buzz(), -8), (T["power1"], sfx.sizzle(0.8, 69), -8), (T["power1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(T["pumps"], sfx.whirr(2.0, 120.0, 260.0, 70), -14), (T["gas"], gas_hiss(0.6, 71), -12),
               (T["spring1"], sfx.whoosh(1.0, True, 72), -4), (T["spring1"] + 0.3, sfx.ding(), -8), (T["spring1"] + 0.5, sfx.chime(), -6)]
        ev += [(T["hooked1"] + 0.3, sfx.clank(260.0, 0.8, 73), -4), (T["hooked1"] + 0.4, sfx.alarm(3, 820.0), -12)]
        ev += [(T["cart"], sfx.click(74), -6), (T["pulls"], sfx.whoosh(0.8, True, 75), -6), (T["lets1"], sfx.snap(76), -6),
               (T["lets1"] + 0.2, sfx.ding(), -8), (T["lets1"] + 0.4, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 77), -6), (T["brakes"], sfx.sizzle(1.0, 78), -8),
               (T["red1"], sfx.creak(0.8, 79), -10), (T["red1"] + 0.3, sfx.alarm(3, 820.0), -14)]
        ev += [(T["magnets"], sfx.hum(1.6, 110.0), -12), (T["touch1"], sfx.power_down(1.0, 80), -10), (T["touch1"] + 0.3, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["sand"], sfx.hiss(0.8, 95), -12), (T["bugs"], sfx.buzz(), -14),
               (T["bounce"], sfx.tap(96), -2), (T["bounce"] + 0.05, sfx.ding(), -8)]
        ev += [(T["s1"], sfx.pop(98), -3), (T["s1"], sfx.whoosh(1.0, True, 97), -8), (T["s2"], sfx.pop(99), -3), (T["s3"], sfx.pop(100), -3)]
        ev += [(T["cong2"], sfx.pop(101), -2), (T["cong2"], sfx.sparkle(1.4, 18, 102), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, False, 104), -6), (T["t_drive1"], sfx.tick(), -8), (T["t_moved"], sfx.womp(), -8)]
        return ev


NAME = "formularossa"
EPISODE = FormulaRossa
