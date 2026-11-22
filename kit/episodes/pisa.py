"""Episode 61 - The Leaning Tower of Pisa.  v2 look: white marble at golden hour over a green lawn; cut-open ground
in sand and soft clay for the foundation beats.

Sets: piazza (hook: close on the bell chamber hanging out past a plumb line, out to the whole tower over the lawn with
its tourists; stat: wide by day; closer: at night, floodlit), ground (break1: three floors rise and the tower starts
sinking into soft clay on one side; fix1: the building stops for almost a century of wars while water squeezes out of
the clay and it firms up), floors (break2: new floors go up straight and lean too; fix2: each upper floor is built
taller on the low side, yellow wedges, and the tower curves back like a banana), lead (break3: 1990, the top hangs
4.5 m out and the tower is closed; fix3: 600 t of lead ingots on the high side and steel cables round the third floor),
drill (break4: the weights only hold it; fix4: drills pull soil from under the high side and the tower settles back
45 cm), quake (reveal: earthquake waves die out in the soft clay while the tower sways gently), tag (EN: a tourist
"holding it up" in a phone viewfinder; AR: a wardrobe leaning in a bedroom with a cardboard box under one foot).
World: front view, the lawn at y = 0, the tower's base centre at x = 0; it leans to the right (the south side).
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of, saudi_man  # noqa: E402

GOLDEN = {"top": "#0B1A3A", "upper": "#1E3A6E", "mid": "#3E6AA8", "low": "#E39A6A", "horizon": "#FFC98A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2A2A60", "horizon": "#4A3A7A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
GREY = {"top": "#1A2234", "upper": "#2C3850", "mid": "#4A5A74", "low": "#8A8C9A", "horizon": "#C9B8A8",
        "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
MARBLE = "#F4EEE2"
MARBLE_S = "#D3C6AE"
MARBLE_D = "#A3967E"
INNER = "#6A604F"
BRONZE = "#B7792F"
LAWN = ("#6E9A3E", "#557E30", "#3C5E22")
SILT = "#9A7A50"
CLAY = "#6E5A48"
CLAY_F = "#4C3C2E"
SAND = "#A9844E"
LEADC = "#5B6270"
CABLE = "#D1D5DB"
FLOORS = (104.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 66.0)    # base, six open galleries, the bell chamber
TW, BW = 176.0, 128.0                                          # tower width, bell chamber width (world units)
BEND = (0.0, 0.0, 0.0, 0.35, 0.35, 0.35, 0.35, 0.6)            # degrees each floor tilts back (the banana)


# ------------------------------------------------------------------------------------------ tower geometry
def _rot(deg):
    q = math.radians(deg)
    return np.array([[math.cos(q), -math.sin(q), 0.0], [math.sin(q), math.cos(q), 0.0], [0.0, 0.0, 1.0]])


def _tr(x, y):
    return np.array([[1.0, 0.0, x], [0.0, 1.0, y], [0.0, 0.0, 1.0]])


def floor_frames(lean, bend=1.0, built=8.0):
    """List of (matrix, floor index, height, width, wedge degrees) in the tower's local frame (base centre at 0,0)."""
    M = _rot(lean)
    out = []
    for i, h in enumerate(FLOORS):
        k = clamp(built - i)
        if k <= 0:
            break
        w = BW if i == 7 else TW
        b = BEND[i] * bend
        if b:
            M = M @ _tr(-w / 2, 0) @ _rot(-b) @ _tr(w / 2, 0)
        out.append((M.copy(), i, h * k, w, b))
        M = M @ _tr(0, -h * k)
    return out


def tower_top(lean, bend=1.0, built=8.0):
    """Top centre of the tower relative to its base centre (unscaled world units)."""
    fr = floor_frames(lean, bend, built)
    if not fr:
        return 0.0, 0.0
    M, i, h, w, b = fr[-1]
    p = M @ np.array([0.0, -h, 1.0])
    return float(p[0]), float(p[1])


def _apply(c, M):
    c.concat(skia.Matrix.MakeAll(M[0, 0], M[0, 1], M[0, 2], M[1, 0], M[1, 1], M[1, 2], 0, 0, 1))


def floor_art(c, i, w, h, t, lit=0.0, a=1.0, bells=1.0):
    """One floor in its own frame: x in [-w/2, w/2], y from -h (top) to 0 (bottom)."""
    mb = mix(MARBLE, "#FFE0A6", 0.4 * lit)
    ms = mix(MARBLE_S, "#E8B878", 0.35 * lit)
    md = mix(MARBLE_D, "#9A6A3A", 0.3 * lit)
    if h < 4:
        return
    if i == 0:                                                   # the base: blind arcade
        c.drawRect(R(-w / 2, -h, w, h), lin_paint(-w / 2, 0, w / 2, 0, [ms, mb, mb, ms, md], a=a))
        xs = [(w / 2 - 4) * math.sin(math.radians(-72 + 144 * k / 6)) for k in range(7)]
        for k in range(6):
            x0, x1 = xs[k], xs[k + 1]
            aw = x1 - x0
            if h > 40 and aw > 8:
                p_ = skia.Path()
                p_.moveTo(x0 + 3, -8)
                p_.lineTo(x0 + 3, -h + 18 + aw / 2)
                p_.arcTo(R(x0 + 3, -h + 18, aw - 6, aw - 6), 180, 180, False)
                p_.lineTo(x1 - 3, -8)
                p_.close()
                c.drawPath(p_, P(md, 0.45 * a))
        for x_ in xs:
            c.drawRect(R(x_ - 2.5, -h + 10, 5, h - 14), P(mb, a))
        c.drawRect(R(-w / 2 - 5, -h - 5, w + 10, 10), P(mb, a))
    elif i < 7:                                                  # an open gallery: columns and arches round a core
        c.drawRect(R(-w / 2 + 9, -h + 8, w - 18, h - 8), lin_paint(-w / 2, 0, w / 2, 0, [shade(INNER, -0.2), INNER, shade(INNER, -0.35)], a=a))
        for k in range(5):                                       # doors on the core wall
            x_ = (w / 2 - 22) * math.sin(math.radians(-60 + 30 * k))
            c.drawRRect(rr(x_ - 6, -h * 0.62, 12, h * 0.5, 5), P("#2E2820", 0.7 * a))
        n = 9
        xs = []
        for k in range(n):
            ph = -80 + 160 * k / (n - 1)
            x_ = (w / 2 - 5) * math.sin(math.radians(ph))
            xs.append(x_)
            cw = 2.5 + 4.5 * math.cos(math.radians(ph))
            lk = 0.12 * math.cos(math.radians(ph + 40)) - 0.05
            c.drawRect(R(x_ - cw / 2, -h + 14, cw, h - 22), P(shade(mb, lk), a))
        for k in range(n - 1):
            x0, x1 = xs[k], xs[k + 1]
            p_ = skia.Path()
            p_.addArc(R(x0, -h + 6, x1 - x0, (x1 - x0) * 0.9), 180, 180)
            c.drawPath(p_, P(mb, a, stroke=3.5))
        c.drawRect(R(-w / 2 - 3, -9, w + 6, 9), P(ms, a))
        c.drawRect(R(-w / 2 - 5, -h - 3, w + 10, 11), P(mb, a))
    else:                                                        # the bell chamber
        c.drawRect(R(-w / 2, -h, w, h), lin_paint(-w / 2, 0, w / 2, 0, [ms, mb, ms, md], a=a))
        for k in range(4):
            x_ = (w / 2 - 18) * math.sin(math.radians(-60 + 40 * k))
            ow = 18 * math.cos(math.radians(-60 + 40 * k)) + 6
            c.drawRRect(rr(x_ - ow / 2, -h + 14, ow, h - 26, ow / 2), P("#2A241C", a))
            if bells > 0:
                c.drawCircle(x_, -h + 34, ow * 0.36, P(BRONZE, a * bells))
        c.drawRect(R(-w / 2 - 6, -h - 6, w + 12, 9), P(mb, a))
        c.drawRect(R(-w / 2 + 6, -h - 14, w - 12, 9), P(ms, a))
    c.drawRect(R(-w / 2, -h, w, h), lin_paint(-w / 2, 0, w / 2, 0, [("#FFF4DA", 0.10), ("#FFFFFF", 0.0), ("#000000", 0.0),
                                                                      ("#1A1208", 0.30)], [0.0, 0.3, 0.6, 1.0], a=a))


def tower(c, x, y, s, t, lean=3.97, bend=1.0, built=8.0, lit=0.0, a=1.0, wedge=0.0, wedge_col="#FACC15", bells=1.0,
          base_dark=0.0):
    """The tower in world space, base centre at (x, y), scale s. lean in degrees to the right; bend 0..n the banana;
    built = floors done (fractional: the top one rising); wedge 0..1 tints the extra masonry on the low side."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    for M, i, h, w, b in floor_frames(lean, bend, built):
        c.save()
        _apply(c, M)
        if b and h > 2:                                          # the wedge under this floor (taller on the low side)
            M0 = M @ _tr(-w / 2, 0) @ _rot(b) @ _tr(w / 2, 0)    # the frame before the tilt back
            Mi = np.linalg.inv(M) @ M0
            pr = Mi @ np.array([w / 2, 0.0, 1.0])
            wp = path_of([(-w / 2, 0), (w / 2, 0), (float(pr[0]), float(pr[1]))], close=True)
            c.drawPath(wp, P(mix(MARBLE_S, wedge_col, wedge)))
        floor_art(c, i, w, h, t, lit=lit, bells=bells)
        if base_dark > 0 and i == 0:
            c.drawRect(R(-w / 2, -h, w, h), P("#000000", 0.25 * base_dark))
        c.restore()
    if a < 1:
        c.restore()
    c.restore()


# ------------------------------------------------------------------------------------------ surroundings
def city_wall(c, x0, x1, y, h=70.0, night=0.0, a=1.0):
    """The old city wall of Pisa: brick with crenellations, standing on y (world)."""
    col = mix("#B0643E", "#4A2E2A", night)
    c.drawRect(R(x0, y - h, x1 - x0, h), lin_paint(0, y - h, 0, y, [shade(col, 0.1), col, shade(col, -0.25)], a=a))
    x = x0
    while x < x1:
        c.drawRect(R(x, y - h - 16, 22, 16), P(shade(col, 0.05), a))
        x += 40


def cypress(c, x, y, h, night=0.0, a=1.0):
    col = mix("#2F5A2A", "#16261A", night)
    p_ = skia.Path()
    p_.moveTo(x, y - h)
    p_.cubicTo(x + h * 0.16, y - h * 0.6, x + h * 0.12, y - h * 0.1, x, y)
    p_.cubicTo(x - h * 0.12, y - h * 0.1, x - h * 0.16, y - h * 0.6, x, y - h)
    c.drawPath(p_, P(col, a))


def lawn(c, night=0.0):
    c.drawRect(R(-3000, 0, 6000, 1400), lin_paint(0, 0, 0, 600, [mix(LAWN[0], "#1E3020", night), mix(LAWN[1], "#16261A", night),
                                                                   mix(LAWN[2], "#0E1A10", night)]))
    c.drawRect(R(-3000, -4, 6000, 8), P(mix("#E8DCC4", "#3A3A44", night), 0.8))
    c.drawRect(R(-120, 0, 240, 1400), P(mix("#E5D8BE", "#3A3644", night), 0.55))      # the stone path to the tower


def tourists(c, t, night=0.0, a=1.0, xs=(-330, -250, 230, 300, 390, -440), h=34):
    shirts = ("#EF4444", "#2563EB", "#F59E0B", "#10B981", "#A855F7", "#F472B6")
    for k, x_ in enumerate(xs):
        person(c, x_, 0, h + (k % 3) * 3, mix(shirts[k % 6], "#20202A", night * 0.6), t + k * 0.4,
               pose="point" if k == 2 else "look" if k % 2 else "stand", face=1 if x_ < 0 else -1, a=a)


def plumb(c, x_top, y_top, y0, a=1.0, col="#FDE047"):
    """Dashed plumb line from the top centre straight down to the ground (world)."""
    if a <= 0:
        return
    c.drawCircle(x_top, y_top, 7, P(col, a))
    c.drawLine(x_top, y_top, x_top, y0, dash_paint(col, a, w=4, t=0.0, dash=16, gap=12))
    c.drawCircle(x_top, y0 - 10, 9, P(col, a))


def wedge_diagram(c, x, y, s, t, k=1.0, a=1.0):
    """Close-up of two gallery floors (screen space, base centre at x, y): the lower one leaning, the upper one built
    taller on the low side (a yellow wedge, k 0..1) so it stands straighter."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.rotate(6.0)
    floor_art(c, 3, TW, 74, t, a=a)
    c.translate(0, -74)
    b = 4.0 * k
    q = math.radians(b)
    if b > 0.05:
        c.drawPath(path_of([(-TW / 2, 0), (TW / 2, 0), (-TW / 2 + TW * math.cos(q), -TW * math.sin(q))], close=True),
                   P("#FACC15", a))
    c.translate(-TW / 2, 0)
    c.rotate(-b)
    c.translate(TW / 2, 0)
    floor_art(c, 4, TW, 74, t, a=a)
    c.restore()


def ghost(c, a=1.0):
    """Dashed outline of the tower standing straight (world, base centre at 0,0)."""
    if a <= 0:
        return
    h7 = sum(FLOORS[:7])
    p_ = path_of([(-TW / 2, 0), (-TW / 2, -h7), (-BW / 2, -h7), (-BW / 2, -h7 - FLOORS[7]), (BW / 2, -h7 - FLOORS[7]),
                  (BW / 2, -h7), (TW / 2, -h7), (TW / 2, 0)], close=True)
    c.drawPath(p_, P("#FFFFFF", 0.10 * a))
    c.drawPath(p_, dash_paint("#FFFFFF", 0.85 * a, w=5, dash=20, gap=14))


def soil(c, t, x0=-1600, x1=1600, firm=0.0, wob=0.0, a=1.0):
    """Cut-open ground under y = 0: sandy silt, soft clay (firm 0..1 darkens it), dense sand (world)."""
    c.drawRect(R(x0, 0, x1 - x0, 92), lin_paint(0, 0, 0, 92, [SILT, shade(SILT, -0.18)], a=a))
    cl = mix(CLAY, CLAY_F, firm)
    top = [(xx, 90 + math.sin(xx * 0.01 + t * 9) * 8 * wob) for xx in range(int(x0), int(x1) + 1, 80)]
    bot = [(xx, 380 + math.sin(xx * 0.012 - t * 7) * 6 * wob) for xx in range(int(x1), int(x0) - 1, -80)]
    c.drawPath(path_of(top + bot, close=True), lin_paint(0, 90, 0, 380, [shade(cl, 0.1), cl, shade(cl, -0.22)], a=a))
    for k in range(5):                                           # the clay's layers
        yy = 125 + k * 52
        pts = [(xx, yy + math.sin(xx * 0.006 + k) * 7 + math.sin(xx * 0.01 + t * 9) * 6 * wob)
               for xx in range(int(x0), int(x1) + 1, 80)]
        c.drawPath(path_of(pts), P(shade(cl, -0.3), 0.45 * a, stroke=4))
    c.drawRect(R(x0, 380, x1 - x0, 1700), lin_paint(0, 380, 0, 1200, [SAND, shade(SAND, -0.35), "#2A1C10"], a=a))
    rng = random.Random(3)
    for _ in range(90):                                          # pebbles and grains
        xx, yy = rng.uniform(x0, x1), rng.uniform(8, 1000)
        c.drawCircle(xx, yy, rng.uniform(2, 6), P("#1A120A", 0.14 * a))
    c.drawRect(R(x0, -10, x1 - x0, 12), lin_paint(0, -10, 0, 2, [LAWN[0], LAWN[2]], a=a))
    c.drawLine(x0, 2, x1, 2, P("#2A1C10", 0.5 * a, stroke=3))


def foundation(c, lean, sink=0.0, a=1.0):
    """The shallow ring foundation (about 3 m) under the base, turning with the tower (world, base centre at 0,0)."""
    c.save()
    c.translate(0, sink)
    c.rotate(lean)
    c.drawRect(R(-TW / 2 - 14, 0, TW + 28, 34), P("#9A8E7A", a))
    c.drawRect(R(-TW / 2 - 14, 0, TW + 28, 34), P("#6B6152", a, stroke=3))
    c.restore()


def ingots(c, x, y, n, a=1.0):
    """A stack of lead ingots on a concrete ring (world, standing on y); n blocks laid so far (fractional)."""
    c.drawRect(R(x - 90, y - 18, 180, 18), P("#A8A29E", a))
    k = 0
    for row in range(6):
        for col in range(5 - row % 2):
            if k >= n:
                return
            bx = x - 80 + col * 34 + (row % 2) * 17
            by = y - 18 - (row + 1) * 18
            fk = clamp(n - k)
            c.drawRRect(rr(bx, by - (1 - fk) * 60, 32, 16, 3), lin_paint(0, by, 0, by + 16, ["#8A93A3", LEADC, "#3A404C"], a=a * fk))
            k += 1


def drill(c, x0, y0, x1, y1, t, run=1.0, a=1.0):
    """An inclined drill tube from the surface (x0, y0) to its tip under the foundation (x1, y1), soil coming out."""
    c.drawLine(x0, y0, x1, y1, P("#94A3B8", a, stroke=16))
    c.drawLine(x0, y0, x1, y1, P("#CBD5E1", a, stroke=6))
    c.drawRRect(rr(x0 - 40, y0 - 60, 80, 60, 10), P("#F59E0B", a))      # the rig at the surface
    c.drawRect(R(x0 - 30, y0 - 90, 14, 30), P("#475569", a))
    if run > 0:
        for k in range(6):                                       # soil travelling up the tube
            q = (t * 0.8 + k / 6.0) % 1.0
            c.drawCircle(lerp(x1, x0, q), lerp(y1, y0, q), 7, P(CLAY, a * run))


def wardrobe(c, x, y, s, lean, a=1.0, box=1.0):
    """A wardrobe tipping to the right on its right foot, a folded cardboard under the lifted left foot (feet at y)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.save()
    c.translate(100, 0)
    c.rotate(lean)
    c.drawRRect(rr(-200, -420, 200, 420, 8), lin_paint(-200, 0, 0, 0, ["#B07B4A", "#9A6638", "#7A4E2A"], a=a))
    c.drawLine(-100, -410, -100, -10, P("#5A3A20", a, stroke=3))
    for xx in (-114, -86):
        c.drawRRect(rr(xx - 4, -240, 8, 40, 4), P("#E5D3B3", a))
    c.restore()
    if box > 0:
        gap = 200 * math.sin(math.radians(lean))
        c.drawRect(R(-112, -gap, 70, gap + 2), P("#C8955A", box))
        c.drawLine(-110, -gap * 0.5, -44, -gap * 0.5, P("#9A6A3A", box, stroke=2))
    c.restore()


def viewfinder(c, x, y, w, h, a=1.0, flash=0.0):
    """A phone camera frame (screen space) with corner marks and a shutter button."""
    if a <= 0:
        return
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx_, cy_ = x + sx * w / 2, y + sy * h / 2
            c.drawLine(cx_, cy_, cx_ - sx * 70, cy_, P("#FFFFFF", a, stroke=7))
            c.drawLine(cx_, cy_, cx_, cy_ - sy * 70, P("#FFFFFF", a, stroke=7))
    c.drawCircle(x + w / 2 - 50, y - h / 2 + 50, 12, P("#EF4444", a))
    if flash > 0:
        c.drawRect(R(0, 0, W, H), P("#FFFFFF", 0.7 * flash))


def crossed_swords(c, x, y, s, a=1.0):
    for sd in (-1, 1):
        c.save()
        c.translate(x, y)
        c.rotate(sd * 35)
        c.drawRect(R(-5 * s, -70 * s, 10 * s, 110 * s), P("#E5E7EB", a))
        c.drawRect(R(-22 * s, 30 * s, 44 * s, 9 * s), P("#B45309", a))
        c.drawRect(R(-5 * s, 39 * s, 10 * s, 24 * s), P("#78350F", a))
        c.restore()


def banana(c, x, y, s, a=1.0):
    p_ = skia.Path()
    p_.moveTo(x - 60 * s, y - 40 * s)
    p_.cubicTo(x - 40 * s, y + 40 * s, x + 50 * s, y + 40 * s, x + 70 * s, y - 30 * s)
    p_.cubicTo(x + 40 * s, y + 10 * s, x - 30 * s, y + 10 * s, x - 60 * s, y - 40 * s)
    c.drawPath(p_, P("#FACC15", a))
    c.drawPath(p_, P("#A16207", a, stroke=4 * s))


def tape(c, x0, x1, y, t, a=1.0):
    """Red-and-white barrier tape between posts (world)."""
    for xx in (x0, x1):
        c.drawRect(R(xx - 4, y - 46, 8, 46), P("#E5E7EB", a))
    n = 14
    for k in range(n):
        xa, xb = lerp(x0, x1, k / n), lerp(x0, x1, (k + 1) / n)
        sag = math.sin(math.pi * (k + 0.5) / n) * 8 + math.sin(t * 3 + k) * 1.5
        c.drawLine(xa, y - 40 + sag, xb, y - 40 + sag, P("#EF4444" if k % 2 else "#F8FAFC", a, stroke=7))


# ====================================================================================== the episode
class Pisa(EpisodeV2):
    BUILD_NO = 61
    FIRST_SET = "piazza"
    CLEAR = "#0B1A3A"
    TITLE = {"en": "LEANING TOWER OF PISA", "ar_sa": "برج بيزا المايل"}
    EMPH = {"en": ["CONGRATS", "TOWER", "LEANS", "FOUR", "METERS", "STANDS", "EIGHT", "CENTURIES", "LEANING", "PISA",
                   "YOURSELF", "SOFT", "CLAY", "FIVE", "YEARS", "SINKING", "SIDE", "BREAK", "WARS", "CENTURY", "FIRMS",
                   "BUILD", "AGAIN", "EVERY", "FLOOR", "UPPER", "TALLER", "LOW", "CURVES", "BANANA", "NINETEEN",
                   "NINETY", "TOP", "HANGS", "HALF", "CLOSED", "SIX", "HUNDRED", "TONS", "LEAD", "HIGH", "STEEL",
                   "CABLES", "CASE", "WEIGHTS", "HOLD", "LESS", "GROUND", "MOVE", "DRILL", "BIT", "SETTLES",
                   "FORTY-FIVE", "CENTIMETERS", "FOLLOW", "BEDOUIN", "TENT", "TWIST", "SAVES", "EARTHQUAKES",
                   "TWELVE", "EIGHTY", "FIFTY-SIX", "FOURTEEN", "THOUSAND", "DEGREES", "TOURIST", "HAND"],
            "ar_sa": ["مبروك", "برج", "مايل", "أربعة", "متر", "وواقف", "ثمانمية", "بيزا", "المايل", "بيدك", "طين",
                      "ليّن", "خمس", "يغوص", "جهة", "استراحة", "الحروب", "مية", "يقسى", "ترجع", "الأدوار", "تميل",
                      "فتطوّل", "فوق", "النازلة", "وينحني", "الموزة", "التسعينات", "راسه", "ونص", "وسكّروه",
                      "ستمية", "رصاص", "العالية", "بكيابل", "احتياط", "الثقل", "يمسكه", "يعتدل", "الأرض", "تتحرك",
                      "فتسحب", "التراب", "شوي", "خمسة", "وأربعين", "سانتي", "تابعني", "الشعر", "والمفاجأة", "يحميه",
                      "الزلازل", "زلازل", "ستة", "وخمسين", "أربعطعش", "ألف", "طن", "درجات", "طاح", "ودولابك",
                      "كرتونة"]}
    KEYS = {"ar_sa": {
        ("hook", "LEANS"): "مايل", ("hook", "FOUR"): "أربعة", ("hook", "STANDS"): "وواقف",
        ("hook", "CENTURIES"): "ثمانمية", ("hook", "CONGRATS"): "مبروك", ("hook", "PISA"): "بيزا",
        ("break1", "CLAY"): "طين", ("break1", "FIVE"): "خمس", ("break1", "SINKING"): "يغوص", ("break1", "SIDE"): "جهة",
        ("fix1", "BREAK"): "استراحة", ("fix1", "WARS"): "الحروب", ("fix1", "CENTURY"): "مية", ("fix1", "FIRMS"): "يقسى",
        ("break2", "BUILD"): "ترجع", ("break2", "FLOOR"): "الأدوار", ("break2", "LEANS"): "تميل",
        ("fix2", "UPPER"): "فوق", ("fix2", "TALLER"): "فتطوّل", ("fix2", "LOW"): "النازلة", ("fix2", "CURVES"): "وينحني",
        ("fix2", "BANANA"): "الموزة",
        ("break3", "NINETY"): "التسعينات", ("break3", "TOP"): "راسه", ("break3", "HALF"): "ونص",
        ("break3", "CLOSED"): "وسكّروه",
        ("fix3", "SIX"): "ستمية", ("fix3", "LEAD"): "رصاص", ("fix3", "HIGH"): "العالية", ("fix3", "CABLES"): "بكيابل",
        ("fix3", "CASE"): "احتياط",
        ("break4", "WEIGHTS"): "الثقل", ("break4", "HOLD"): "يمسكه", ("break4", "LESS"): "يعتدل",
        ("break4", "GROUND"): "الأرض", ("break4", "MOVE"): "تتحرك",
        ("fix4", "DRILL"): "فتسحب", ("fix4", "SOIL"): "التراب", ("fix4", "BIT"): "شوي", ("fix4", "FORTY-FIVE"): "خمسة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "TWIST"): "والمفاجأة", ("reveal", "CLAY"): "الطين", ("reveal", "SAVES"): "يحميه",
        ("reveal", "EARTHQUAKES"): "الزلازل", ("reveal", "FOUR"): "أربعة",
        ("stat", "FIFTY-SIX"): "ستة", ("stat", "FOURTEEN"): "أربعطعش", ("stat", "DEGREES"): "درجات",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "STOOD"): "طاح", ("tag", "TOURIST"): "ودولابك", ("tag", "HAND"): "كرتونة"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: a Bedouin tent"),
                   "stat": [("56 m", "TALL"), ("14,500 t", "OF MARBLE + STONE"), ("3.97°", "OF LEAN")],
                   "L": {"out": "ALMOST 4 M OUT OF LINE", "years": "STILL STANDING: 800+ YEARS",
                         "name": "THE LEANING TOWER OF PISA", "clay": "SOFT CLAY", "sinking": "SINKING ON ONE SIDE",
                         "y1": "1173", "y2": "1178", "y3": "1272", "wars": "WARS: ALMOST 100 YEARS",
                         "firm": "THE CLAY FIRMS UP", "water": "WATER SQUEEZES OUT", "again": "BUILDING AGAIN",
                         "leanstoo": "EVERY NEW FLOOR LEANS", "taller": "TALLER ON THE LOW SIDE",
                         "banana": "CURVED LIKE A BANANA", "y1990": "1990", "hang": "TOP: 4.5 M OUT",
                         "closed": "CLOSED", "lead": "600 TONS OF LEAD", "cables": "STEEL CABLES, JUST IN CASE",
                         "high": "HIGH SIDE", "hold": "WEIGHTS ONLY HOLD IT", "move": "THE GROUND HAS TO MOVE",
                         "drill": "DRILLING OUT SOIL", "bit": "BIT BY BIT", "back": "45 CM BACK",
                         "twist": "SOFT CLAY SOAKS UP QUAKES", "quakes": "4 BIG QUAKES SINCE 1280",
                         "hand": "IT NEEDS A HAND!", "stiff": "STIFF TOWER"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: بيت الشعر"),
                      "stat": [("56", "متر طول"), ("14,500", "طن"), ("3.97°", "درجة ميلان")],
                      "L": {"out": "مايل قرابة أربعة متر", "years": "واقف من ثمانمية سنة",
                            "name": "برج بيزا المايل", "clay": "طين ليّن", "sinking": "يغوص من جهة",
                            "y1": "1173", "y2": "1178", "y3": "1272", "wars": "حروب: قرابة مية سنة",
                            "firm": "الطين يقسى", "water": "الموية تطلع منه", "again": "ترجع تبني",
                            "leanstoo": "كل دور جديد يميل", "taller": "أطول من الجهة النازلة",
                            "banana": "منحني مثل الموزة", "y1990": "1990", "hang": "راسه طالع أربعة متر ونص",
                            "closed": "مسكّر", "lead": "ستمية طن رصاص", "cables": "كيابل حديد، احتياط",
                            "high": "الجهة العالية", "hold": "الثقل يمسكه بس", "move": "لازم الأرض تتحرك",
                            "drill": "نسحب التراب", "bit": "شوي شوي", "back": "يرجع خمسة وأربعين سانتي",
                            "twist": "الطين يمتص الزلازل", "quakes": "أربعة زلازل قوية",
                            "hand": "دولابك مال!", "box": "كرتونة", "stiff": "برج قاسي"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "leans": ("hook", "LEANS", 0.15), "four": ("hook", "FOUR", 0.25), "stands": ("hook", "STANDS", 0.4),
            "cent": ("hook", "CENTURIES", 0.55), "congrats": ("hook", "CONGRATS", 0.68), "pisa": ("hook", "PISA", 0.92),
            "clay": ("break1", "CLAY", 0.3), "five": ("break1", "FIVE", 0.5), "sinking": ("break1", "SINKING", 0.75),
            "side": ("break1", "SIDE", 0.92),
            "brk": ("fix1", "BREAK", 0.15), "wars": ("fix1", "WARS", 0.3), "century": ("fix1", "CENTURY", 0.6),
            "firms": ("fix1", "FIRMS", 0.9),
            "build": ("break2", "BUILD", 0.1), "floor": ("break2", "FLOOR", 0.6), "leans2": ("break2", "LEANS", 0.85),
            "upper": ("fix2", "UPPER", 0.15), "taller": ("fix2", "TALLER", 0.3), "low": ("fix2", "LOW", 0.5),
            "curves": ("fix2", "CURVES", 0.7), "banana": ("fix2", "BANANA", 0.92),
            "ninety": ("break3", "NINETY", 0.15), "top": ("break3", "TOP", 0.3), "half": ("break3", "HALF", 0.6),
            "closed": ("break3", "CLOSED", 0.92),
            "six": ("fix3", "SIX", 0.1), "lead": ("fix3", "LEAD", 0.3), "high": ("fix3", "HIGH", 0.5),
            "cables": ("fix3", "CABLES", 0.7), "case": ("fix3", "CASE", 0.92),
            "weights": ("break4", "WEIGHTS", 0.1), "hold": ("break4", "HOLD", 0.3), "less": ("break4", "LESS", 0.55),
            "ground": ("break4", "GROUND", 0.75), "move": ("break4", "MOVE", 0.92),
            "drill": ("fix4", "DRILL", 0.1), "soil": ("fix4", "SOIL", 0.2), "bit": ("fix4", "BIT", 0.5),
            "f45": ("fix4", "FORTY-FIVE", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "twist": ("reveal", "TWIST", 0.05), "clay2": ("reveal", "CLAY", 0.25), "saves": ("reveal", "SAVES", 0.45),
            "quakes": ("reveal", "EARTHQUAKES", 0.7), "four2": ("reveal", "FOUR", 0.6),
            "s1": ("stat", "FIFTY-SIX", 0.05), "s2": ("stat", "FOURTEEN", 0.35), "s3": ("stat", "DEGREES", 0.8),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_stood": ("tag", "STOOD", 0.1), "t_tour": ("tag", "TOURIST", 0.5), "t_hand": ("tag", "HAND", 0.92)})
        T["side1"] = max(T["side"], T["sinking"]) + 0.1
        T["leans21"] = max(T["leans2"], T["floor"]) + 0.1
        T["closed1"] = max(T["closed"], T["half"]) + 0.1
        T["move1"] = max(T["move"], T["ground"]) + 0.1
        T["firms1"] = max(T["firms"], T["century"]) + 0.2
        T["banana1"] = max(T["banana"], T["curves"]) + 0.2
        T["case1"] = max(T["case"], T["cables"]) + 0.2
        T["f451"] = max(T["f45"], T["bit"]) + 0.2
        # ---- sets
        self.cut(s("break1") - 0.12, "ground", 1)
        self.cut(s("break2") - 0.12, "floors", -1)
        self.cut(s("break3") - 0.12, "lead", 1)
        self.cut(s("break4") - 0.12, "drill", -1)
        self.cut(s("reveal") - 0.12, "quake", 1)
        self.cut(s("stat") - 0.12, "piazza", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- piazza camera: from the bell chamber hanging past the plumb line, out to the whole tower on the lawn
        tx, ty = tower_top(3.97)
        cm = Camera(tx * 0.5, ty + 150, 2.2)
        cm.key(0.05, tx * 0.5, ty + 160, 2.15, 0.5)
        cm.key(max(0.6, T["stands"] - 0.5), 30, -250, 1.38, max(1.4, T["congrats"] - T["stands"] + 0.4))
        cm.key(T["congrats"] + 0.2, 30, -246, 1.42, max(1.0, s("break1") - T["congrats"]))
        cm.key(s("stat") - 0.12, 60, -300, 1.02, 0.0).key(s("stat"), 60, -302, 1.03, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 30, -280, 1.28, 1.0).key(s("closer") + 0.9, 30, -282, 1.33, 3.0)
        self.cam = cm
        self.spans = [(T["side1"], T["firms1"] + 0.3), (T["leans21"], T["banana1"] + 0.3), (T["closed1"], T["case1"] + 0.3),
                      (T["move1"], T["f451"] + 0.3)]
        self.shakes = [(0.1, 0.5, 5), (T["congrats"], 0.35, 8), (T["side1"], 0.4, 7), (T["leans21"], 0.3, 6),
                       (T["closed1"], 0.4, 7), (T["move1"], 0.3, 6), (T["quakes"] - 0.3, 1.6, 10), (s("closer") + 0.2, 0.35, 9),
                       (T["t_hand"], 0.25, 6)]

    # ------------------------------------------------------------------ set: piazza (hook, stat, closer)
    def draw_piazza(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        closer = t >= s("closer") - 0.1
        night = prog(t, s("closer") - 0.1, s("closer") + 0.8) if closer else 0.0
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN if not closer else NIGHTP, horizon_y=gy)
        if closer:
            v2.stars(c, W, H, t, 0.8 * night)
        else:
            add_glow(c, 170 - cx * 0.03, gy - 300, 520, "#FFC98A", 0.5)
        c.save()
        c.translate(W / 2 - cx * 0.08 * z, gy)
        v2.ridge(c, -1600, 1600, 0, 130, mix("#7C6C9C", "#1E1E46", night), mix("#5C4C7C", "#141432", night), seed=4, step=170,
                 rough=0.4)
        c.restore()
        self.view(c, cam)
        city_wall(c, -1500, 1500, -2, 64, night)
        for k, (x_, h_) in enumerate(((-640, 150), (-560, 120), (520, 160), (610, 130), (-900, 140), (900, 150))):
            cypress(c, x_, -2, h_, night)
        lawn(c, night)
        lit = night
        if lit > 0:
            add_glow(c, 20, -330, 520, "#FFC46A", 0.35 * lit)
        hook = t < s("break1")
        lean = 3.97
        if hook:                                                 # it tips over from the straight outline, and stops
            gk = prog(t, 0.05, 0.3) * (1 - prog(t, T["congrats"] - 0.3, T["congrats"] + 0.2))
            ghost(c, gk)
            lean = 3.97 * e_back(prog(t, 0.15, 1.1))
        tower(c, 0, 0, 1.0, t, lean=lean, bend=1.0, lit=lit)
        tourists(c, t, night)
        if hook:
            tx, ty = tower_top(lean)
            ak = prog(t, T["four"] - 0.25, T["four"] + 0.15) * gk
            if ak > 0:                                           # the top out of line with the straight outline
                hy = -sum(FLOORS) - 40
                c.drawLine(0, hy, tx, hy, P("#FDE047", ak, stroke=8))
                c.drawCircle(0, hy, 9, P("#FDE047", ak))
                arrow(c, tx - 30, hy, tx + 6, hy, "#FDE047", a=ak, w=8, head=22)
                c.drawLine(tx, hy + 10, tx, ty, P("#FDE047", 0.7 * ak, stroke=4))
            self.ui["top"] = self.to_screen(cam, tx, ty)
        c.restore()
        self.ui["cam"] = cam

    def ui_piazza(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "out", T["leans"] - 0.1, T["stands"] - 0.1, accent="#FDE047", size=46)
            self.chip(540, 300, "years", T["stands"] - 0.1, T["pisa"] - 0.3, accent=GOOD, size=44)
            self.chip(540, 300, "name", T["pisa"] - 0.3, s("break1") + 0.1, accent=HILITE, size=44)

    # ------------------------------------------------------------------ set: ground (break1, fix1)
    def draw_ground(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix1") - 0.12
        cam = (0, 80, 1.15)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        self.view(c, cam)
        firm = prog(t, T["century"] - 0.4, T["firms1"]) if fixed else 0.0
        soil(c, t, firm=firm)
        if not fixed:
            built = lerp(0.6, 3.0, prog(t, s("break1") - 0.1, T["five"]))
            lean = lerp(0.0, 1.4, e_io(prog(t, T["sinking"] - 0.3, T["side1"] + 0.3)))
        else:
            built, lean = 3.0, 1.4
        sink = lean * 4.0
        foundation(c, lean, sink)
        c.save()
        c.translate(0, sink)
        tower(c, 0, 0, 1.0, t, lean=lean, bend=0.0, built=built)
        c.restore()
        if not fixed:                                            # the clay squeezed under the low side
            sk = prog(t, T["sinking"] - 0.3, T["side1"])
            for k in range(4):
                r_ = 60 + k * 50 + (t * 40) % 50
                p_ = skia.Path()
                p_.addArc(R(90 - r_, 40 - r_ * 0.5, 2 * r_, r_), 10, 160)
                c.drawPath(p_, P("#F87171", 0.55 * sk * (1 - k / 4), stroke=5))
            if sk > 0:
                arrow(c, 70, -60, 70, 20, WARN, a=sk, w=10, head=24)
        else:
            wk = prog(t, T["century"] - 0.6, T["firms1"] + 0.5)
            rng = random.Random(7)
            for k in range(26):                                  # water drops rising out of the clay
                x_ = rng.uniform(-700, 700)
                q = (t * 0.6 + rng.random()) % 1.0
                y_ = lerp(360, 20, q)
                c.drawCircle(x_, y_, 8, P("#60A5FA", 0.85 * wk * (1 - q * 0.5)))
        c.restore()
        self.ui["cam"] = cam

    def ui_ground(self, c, t, tw):
        T, s = self.T, self.tl.s
        cam = self.ui.get("cam", (0, 80, 1.15))
        fixed = tw >= s("fix1") - 0.12
        cx_, cy_ = self.to_screen(cam, 320, 230)
        if not fixed:
            yr = "y1" if tw < T["five"] - 0.1 else "y2"
            self.chip(540, 470, yr, s("break1") - 0.1, s("fix1") - 0.15, accent="#FDE68A", size=56)
            self.label(cx_, cy_, 760, 720, "clay", T["clay"] - 0.2, s("fix1") - 0.2, accent="#D6B48A", size=34)
            self.chip(540, 300, "sinking", T["sinking"] - 0.2, s("fix1") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["side1"], s("fix1") - 0.2, x=920, y=420)
            self.red(T["side1"], 1.2)
            return
        prog_y = prog(tw, T["wars"] - 0.2, T["century"] + 0.4)
        yr = int(round(lerp(1178, 1272, prog_y)))
        sp = self.span(s("fix1") - 0.1, s("break2") - 0.15)
        if sp > 0:
            word_c = "#FDE68A"
            v2.chip(c, 540, 470, str(yr), sp, accent=word_c, size=56)
        self.chip(540, 300, "wars", T["brk"] - 0.2, T["century"] + 0.1, accent="#FCA5A5", size=44)
        self.chip(540, 300, "firm", T["century"] + 0.1, s("break2") - 0.15, accent=GOOD, size=46)
        wk = self.span(T["brk"] - 0.2, T["century"] + 0.1)
        if wk > 0:
            crossed_swords(c, 900, 640, 1.0, a=wk)
        self.label(cx_, cy_, 760, 760, "water", T["century"] - 0.3, s("break2") - 0.2, accent="#60A5FA", size=32)
        self.badge("check", T["firms1"] + 0.1, s("break2") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: floors (break2, fix2)
    def draw_floors(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        cam = (40, -290, 1.3)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        add_glow(c, 170, gy - 300, 520, "#FFC98A", 0.45)
        self.view(c, cam)
        city_wall(c, -1500, 1500, -2, 64)
        lawn(c)
        if not fixed:
            built = lerp(3.0, 6.0, prog(t, T["build"] - 0.2, T["leans21"]))
            lean = lerp(1.4, 3.2, prog(t, T["build"], T["leans21"] + 0.2))
            tower(c, 0, 0, 1.0, t, lean=lean, bend=0.0, built=built)
            lk = prog(t, T["floor"] - 0.3, T["leans21"])
            if lk > 0:                                           # the lean angle at the base
                p_ = skia.Path()
                p_.addArc(R(-260, -260, 520, 520), -90, lean * 6)
                c.drawPath(p_, P(WARN, lk, stroke=7))
                c.drawLine(0, 0, 0, -300, dash_paint("#FFFFFF", 0.7 * lk, w=3))
        else:
            close = t < T["curves"] - 0.2
            if not close:
                tower(c, 0, 0, 1.0, t, lean=3.6, bend=2.6, wedge=1.0)
                ck = prog(t, T["curves"] - 0.3, T["banana1"])
                if ck > 0:                                       # the curve of the axis
                    pts = [tower_top(3.6, 2.6, max(0.01, 8.0 * k / 20)) for k in range(1, 21)]
                    c.drawPath(path_of([(0, 0)] + pts), P("#FDE047", 0.9 * ck, stroke=5))
        c.restore()
        if fixed and t < T["curves"] - 0.2:                      # close-up: a floor built taller on the low side
            c.drawRect(R(0, 0, W, H), P("#0B1530", 0.45))
            wk = prog(t, T["taller"] - 0.3, T["low"] + 0.2)
            wedge_diagram(c, 520, 1150, 3.0, t, k=wk)
            self.ui["wedge"] = (795, 930)
        self.ui["cam"] = cam

    def ui_floors(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 300, "again", T["build"] - 0.2, T["floor"] - 0.2, accent="#FDE68A", size=46)
            self.chip(540, 300, "leanstoo", T["floor"] - 0.2, s("fix2") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["leans21"], s("fix2") - 0.2, x=920, y=420)
            self.red(T["leans21"], 1.2)
            return
        wx, wy = self.ui.get("wedge", (795, 930))
        self.label(wx, wy, 700, 520, "taller", T["taller"] - 0.2, T["curves"] - 0.25, accent="#FACC15", size=38)
        self.chip(540, 300, "banana", T["curves"] - 0.2, s("break3") - 0.15, accent="#FACC15", size=46)
        bk = self.span(T["banana"] - 0.3, s("break3") - 0.15)
        if bk > 0:
            banana(c, 880, 470, 1.0, a=bk)
        self.badge("check", T["banana1"] + 0.1, s("break3") - 0.15, x=920, y=640)

    # ------------------------------------------------------------------ set: lead (break3, fix3), 1990
    def draw_lead(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        cam = (-60, -260, 1.22)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GREY, horizon_y=gy)
        self.view(c, cam)
        city_wall(c, -1500, 1500, -2, 64)
        lawn(c)
        lean = 4.6
        if fixed:
            nk = lerp(0, 24, prog(t, T["six"] - 0.2, T["high"] + 0.4))
            ingots(c, -190, 0, nk)
            ck = prog(t, T["cables"] - 0.3, T["case1"])
            if ck > 0:                                           # two steel cables from the third floor to anchors
                fr = floor_frames(lean, 1.0)
                M = fr[2][0]
                for sd, (ax_, ay_) in enumerate(((-760, -6), (-900, -6))):
                    p = M @ np.array([-TW / 2 + 6, -50.0 + sd * 20, 1.0])
                    x1, y1 = lerp(float(p[0]), ax_, ck), lerp(float(p[1]), ay_, ck)
                    c.drawLine(float(p[0]), float(p[1]), x1, y1, P(CABLE, 1.0, stroke=5))
                    c.drawRect(R(ax_ - 20, -24, 40, 24), P("#64748B", ck))
        tower(c, 0, 0, 1.0, t, lean=lean, bend=1.0)
        if fixed:                                                # the ring round the third floor
            fr = floor_frames(lean, 1.0)
            c.save()
            _apply(c, fr[2][0])
            c.drawRect(R(-TW / 2 - 6, -54, TW + 12, 10), P(CABLE, prog(t, T["cables"] - 0.3, T["cables"])))
            c.restore()
        tx, ty = tower_top(lean)
        if not fixed:
            pk = prog(t, T["top"] - 0.3, T["top"] + 0.2)
            plumb(c, tx, ty, 0, a=pk)
            ck = prog(t, T["closed"] - 0.3, T["closed1"])
            tape(c, -260, 300, 0, t, a=ck)
        self.ui["top"] = self.to_screen(cam, tx, ty)
        self.ui["lead"] = self.to_screen(cam, -190, -60)
        self.ui["ring"] = self.to_screen(cam, -110, -300)
        c.restore()
        self.ui["cam"] = cam

    def ui_lead(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix3") - 0.12:
            self.chip(540, 470, "y1990", s("break3") - 0.1, T["half"] - 0.2, accent="#FDE68A", size=56)
            tx, ty = self.ui.get("top", (600, 500))
            self.label(tx, ty, 780, 560, "hang", T["top"] - 0.1, s("fix3") - 0.2, accent="#FDE047", size=36)
            self.chip(540, 300, "closed", T["closed"] - 0.2, s("fix3") - 0.15, accent=WARN, size=56)
            self.badge("alert", T["closed1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["closed1"], 1.2)
            return
        lx, ly = self.ui.get("lead", (300, 1100))
        self.label(lx, ly, 300, 640, "lead", T["lead"] - 0.2, T["cables"] - 0.1, accent="#CBD5E1", size=38)
        rx, ry = self.ui.get("ring", (400, 700))
        self.label(rx, ry, 330, 520, "cables", T["cables"] - 0.1, s("break4") - 0.2, accent="#E5E7EB", size=34)
        self.chip(540, 300, "high", T["high"] - 0.2, s("break4") - 0.15, accent="#93C5FD", size=40)
        self.badge("check", T["case1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: drill (break4, fix4), cut open
    def draw_drill(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix4") - 0.12
        cam = (-80, 40, 0.98)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GREY, horizon_y=gy)
        self.view(c, cam)
        soil(c, t, firm=1.0)
        lean = 4.6 if not fixed else lerp(4.6, 4.0, e_io(prog(t, T["bit"] - 0.3, T["f451"] + 0.3)))
        foundation(c, lean, 2)
        ingots(c, -190, 0, 24)
        tower(c, 0, 0, 1.0, t, lean=lean, bend=1.0)
        tx, ty = tower_top(lean)
        if not fixed:
            mk = prog(t, T["ground"] - 0.3, T["move1"])
            if mk > 0:
                for k in range(3):
                    c.drawLine(-300 + k * 60, 60 + math.sin(t * 20 + k) * 6 * mk, -120 + k * 60, 60 - math.sin(t * 20 + k) * 6 * mk,
                               P(WARN, mk, stroke=6))
        else:
            dk = prog(t, T["drill"] - 0.2, T["soil"] + 0.3)
            run = prog(t, T["soil"] - 0.2, T["soil"]) * (1 - prog(t, T["f451"], T["f451"] + 0.4))
            for k, (x1, y1) in enumerate(((-110, 70), (-70, 56))):
                drill(c, lerp(-560, -620, k), 0, lerp(-560, x1, dk), lerp(0, y1, dk), t + k * 0.3, run=run)
            hk = prog(t, T["soil"], T["f451"])
            for k in range(5):                                   # little hollows that close as the soil comes out
                r_ = 16 * (1 - abs(hk * 2 - 1))
                if r_ > 1:
                    c.drawCircle(-140 + k * 22, 60 + (k % 2) * 10, r_, P("#2A2018", 0.8))
            bk = prog(t, T["f45"] - 0.3, T["f451"])
            if bk > 0:                                           # the top moving back
                ox, oy = tower_top(4.6)
                arrow(c, ox + 40, oy - 40, tx + 10, ty - 40, GOOD, a=bk, w=10, head=26)
        self.ui["top"] = self.to_screen(cam, tx, ty)
        self.ui["under"] = self.to_screen(cam, -120, 70)
        c.restore()
        self.ui["cam"] = cam

    def ui_drill(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix4") - 0.12:
            self.chip(540, 300, "hold", T["weights"] - 0.2, T["ground"] - 0.2, accent="#CBD5E1", size=46)
            self.chip(540, 300, "move", T["ground"] - 0.2, s("fix4") - 0.15, accent=WARN, size=44)
            self.badge("alert", T["move1"], s("fix4") - 0.2, x=920, y=420)
            self.red(T["move1"], 1.2)
            return
        ux, uy = self.ui.get("under", (400, 1000))
        self.label(ux, uy, 330, 1120, "drill", T["drill"] - 0.2, T["bit"] - 0.1, accent="#F59E0B", size=36)
        self.chip(540, 300, "bit", T["bit"] - 0.2, T["f45"] - 0.2, accent="#FDE68A", size=46)
        tx, ty = self.ui.get("top", (600, 400))
        self.label(tx, ty, 780, 520, "back", T["f45"] - 0.2, s("cta") - 0.15, accent=GOOD, size=38)
        self.badge("check", T["f451"] + 0.1, s("cta") - 0.15, x=920, y=640)

    # ------------------------------------------------------------------ set: quake (reveal)
    def draw_quake(self, c, t):
        T, s = self.T, self.tl.s
        cam = (0, 60, 0.8)
        gy = (0 - cam[1]) * cam[2] + H / 2
        v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
        qk = prog(t, T["quakes"] - 0.4, T["quakes"]) * (1 - prog(t, s("stat") - 0.6, s("stat") - 0.15))
        self.view(c, cam)
        soil(c, t, firm=0.6, wob=qk)
        for k in range(3):                                       # waves coming up from the deep sand, dying in the clay
            yy = 760 - ((t * 260 + k * 120) % 380)
            amp = 26 * qk * clamp((yy - 120) / 380)
            pts = [(x_, yy + math.sin(x_ * 0.02 + t * 12) * amp) for x_ in range(-900, 901, 30)]
            c.drawPath(path_of(pts), P("#FCA5A5", 0.8 * qk * clamp((yy - 100) / 300), stroke=5))
        sway = math.sin(t * 6) * 0.5 * qk
        foundation(c, 3.97 + sway, 2)
        tower(c, 0, 0, 1.0, t, lean=3.97 + sway, bend=1.0)
        self.ui["clay"] = self.to_screen(cam, 300, 230)
        c.restore()

    def ui_quake(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "twist", T["twist"] - 0.1, T["quakes"] - 0.2, accent="#FDE68A", size=44)
        self.chip(540, 300, "quakes", T["quakes"] - 0.2, s("stat") - 0.15, accent=WARN, size=44)
        cx_, cy_ = self.ui.get("clay", (700, 1100))
        self.label(cx_, cy_, 760, 1120, "clay", T["clay2"] - 0.2, s("stat") - 0.2, accent="#D6B48A", size=34)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        if not self.rtl:
            cam = (-40, -260, 1.0)
            gy = (0 - cam[1]) * cam[2] + H / 2
            v2.sky(c, W, H, 0.0, pal=GOLDEN, horizon_y=gy)
            add_glow(c, 170, gy - 300, 520, "#FFC98A", 0.5)
            self.view(c, cam)
            city_wall(c, -1500, 1500, -2, 64)
            lawn(c)
            tower(c, 120, 0, 0.62, t, lean=3.97, bend=1.0)
            c.restore()
            # the tourist close to the camera, a hand up under the top of the tower to "hold it up"
            up = t >= T["t_tour"] - 0.2
            person(c, 877, 1262, 373, "#EF4444", t, pose="point" if up else "stand", face=-1, hair="#3A2A1A")
            fk = prog(t, T["t_hand"] - 0.05, T["t_hand"] + 0.05) * (1 - prog(t, T["t_hand"] + 0.05, T["t_hand"] + 0.35))
            viewfinder(c, 540, 760, 880, 860, a=prog(t, T["t_stood"] - 0.3, T["t_stood"]), flash=fk)
        else:
            c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#E7D8C2", "#D6C3A6", "#B79E7C"]))
            c.drawRect(R(0, 1230, W, H - 1230), P("#8A6A4A"))
            for k in range(8):
                c.drawLine(k * 150, 1230, k * 150 - 200, H, P("#6E5238", 0.6, stroke=4))
            lk = prog(t, T["t_stood"] - 0.2, T["t_tour"])
            wardrobe(c, 560, 1230, 1.55, lerp(0.0, 4.5, lk), box=prog(t, T["t_hand"] - 0.4, T["t_hand"]))
            saudi_man(c, 220, 1240, 360, t, pose="shrug" if t > T["t_tour"] else "look", face=1)

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            self.chip(540, 300, "hand", T["t_hand"] - 0.2, self.duration + 1, accent=HILITE, size=50)
        else:
            self.chip(540, 300, "hand", T["t_tour"] - 0.2, self.duration + 1, accent=HILITE, size=50)
            self.chip(820, 1080, "box", T["t_hand"] - 0.2, self.duration + 1, accent="#FDBA74", size=40)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#1E3A6E", "#3E6AA8", "#E39A6A"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.1, sfx.creak(1.2, 61), -10), (T["leans"], sfx.whoosh(0.4, False, 62), -12), (T["four"], sfx.pop(63), -8),
              (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10), (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8),
              (T["pisa"], sfx.bell(660.0, 1.4, 0.6), -12), (T["pisa"] + 0.2, sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["five"], sfx.tick(), -8),
               (T["sinking"], sfx.creak(1.0, 67), -8), (T["side1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["wars"], sfx.clank(700.0, 0.4, 69), -10),
               (T["century"], sfx.whirr(1.0, 200.0, 420.0, 70), -16), (T["firms1"], sfx.ding(), -8),
               (T["firms1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 71), -4), (T["build"], sfx.thunk(72), -8),
               (T["floor"], sfx.thunk(73), -8), (T["leans21"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 74), -4), (T["taller"], sfx.thunk(75), -8),
               (T["curves"], sfx.whoosh(0.5, True, 76), -12), (T["banana1"], sfx.ding(), -8), (T["banana1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 77), -4), (T["top"], sfx.creak(0.8, 78), -10),
               (T["closed1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 79), -4), (T["lead"], sfx.clank(300.0, 0.5, 80), -8),
               (T["high"], sfx.clank(320.0, 0.4, 81), -10), (T["cables"], sfx.snap(82), -10), (T["case1"], sfx.ding(), -8),
               (T["case1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 83), -4), (T["ground"], sfx.thud(0.4, 84), -8),
               (T["move1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 85), -4), (T["drill"], sfx.whirr(1.6, 160.0, 260.0, 86), -14),
               (T["bit"], sfx.whirr(1.0, 200.0, 320.0, 87), -16), (T["f451"], sfx.ding(), -8), (T["f451"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(88), 0), (T["follow"] - 0.15, sfx.pop(89), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 90), -6), (T["quakes"] - 0.3, rumble(1.8, 91), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 92), -6), (T["s1"], sfx.pop(93), -3), (T["s2"], sfx.pop(94), -3),
               (T["s3"], sfx.pop(95), -3)]
        ev += [(T["cong2"], sfx.pop(96), -2), (T["cong2"], sfx.sparkle(1.4, 18, 97), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 98), -6)]
        if self.rtl:
            ev += [(T["t_tour"], sfx.creak(0.6, 99), -10), (T["t_hand"], sfx.pop(100), -8)]
        else:
            ev += [(T["t_hand"], sfx.click(101), -4)]
        return ev


NAME = "pisa"
EPISODE = Pisa
