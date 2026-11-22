"""Episode 64 - Big Ben's clock (the Great Clock of Westminster).  v2 look: the clock tower in honey-coloured stone at
dusk over the Palace, its four dials lit at night; close-up boards inside the tower for the pendulum, the gravity
escapement, the hands and the bell.

Sets: pend (hook part 1: a hand adds an old penny to the stack on the giant pendulum; fix1: the whole 4 m pendulum
next to a man, ticking every 2 s; break4: heat and cold make it drift; fix4: pennies added, each +0.4 s a day),
tower (hook part 2: out from the dial to the whole tower; stat: the dial and belfry; closer: at night, dials lit),
airy (break1: the Astronomer Royal at Greenwich wants every hour struck to the second, a telegraph line),
escape (break2: wind on the hands pushes back through the gears to the pendulum; fix2: the gravity escapement, two
arms give the same push every swing), hands (break3: cast-iron minute hands too heavy to turn; fix3: thin copper hands
over a 7 m dial with a worker on a cradle), bell (reveal: Big Ben is the bell, it cracked in its first year and still
rings cracked), tag (EN: in bed texting "On my way!"; AR: on the couch, "five minutes" while the clock spins an hour).
World of the tower set: 1 m = 10 units, the tower's base centre at (0, 0), the dial centre at (0, -585).
"""
from v2_base import *  # noqa: F401,F403
from windtower import arrow  # noqa: E402
from burjalarab import path_of, saudi_man  # noqa: E402
from towerbridge import bus  # noqa: E402

DUSKP = {"top": "#0A0A2A", "upper": "#24215C", "mid": "#6A3A78", "low": "#D0705E", "horizon": "#F6A86A",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
NIGHTP = {"top": "#030616", "upper": "#0A1238", "mid": "#1A2458", "low": "#2A2A60", "horizon": "#4A3A7A",
          "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
STONE = "#D9B877"
STONE_S = "#B8975C"
STONE_D = "#8A6E40"
GILT = "#E2B84A"
GILT_D = "#A8822A"
PRUSSIAN = "#1E3A5F"
OPAL = "#F3EEDC"
SLATE = "#3E4A5C"
COPPER = "#C8743A"
IRON = "#3A3F47"
BRONZE = "#8A6A3A"
DIAL_Y = -585.0
DIAL_R = 36.0


# ------------------------------------------------------------------------------------------ the dial
def dial(c, x, y, r, hour, minute, lit=0.0, a=1.0, hand_kind="blue", detail=1.0, hand_scale=1.0, min_ang=None):
    """A Great Clock dial at (x, y), radius r (any space). hour 0-12, minute 0-60. lit 0..1 glows the opal glass.
    hand_kind: blue (painted, today), iron (heavy cast iron), copper (thin copper). min_ang overrides the minute hand."""
    if a <= 0:
        return
    c.drawCircle(x, y, r * 1.16, P(mix(GILT_D, "#7A5A1A", 0.3), a))
    c.drawCircle(x, y, r * 1.12, lin_paint(x - r, y - r, x + r, y + r, [GILT, "#F6D77A", GILT_D], a=a))
    glass = mix(OPAL, "#FFE7A6", lit)
    c.drawCircle(x, y, r, P(glass, a))
    if lit > 0:
        add_glow(c, x, y, r * 2.2, "#FFD27A", 0.5 * lit * a)
    c.drawCircle(x, y, r * 0.98, P(PRUSSIAN, 0.9 * a, stroke=max(1.0, r * 0.03)))
    c.drawCircle(x, y, r * 0.74, P(PRUSSIAN, 0.8 * a, stroke=max(1.0, r * 0.02)))
    if detail > 0.3:                                             # the iron tracery between the pieces of glass
        for k in range(12):
            q = math.radians(k * 30 + 15)
            c.drawLine(x + math.cos(q) * r * 0.2, y + math.sin(q) * r * 0.2, x + math.cos(q) * r * 0.74,
                       y + math.sin(q) * r * 0.74, P(PRUSSIAN, 0.45 * a * detail, stroke=max(1.0, r * 0.012)))
        for rr_ in (0.36, 0.55):
            c.drawCircle(x, y, r * rr_, P(PRUSSIAN, 0.35 * a * detail, stroke=max(1.0, r * 0.01)))
        for k in range(60):                                      # minute marks
            q = math.radians(k * 6)
            l0 = 0.93 if k % 5 else 0.88
            c.drawLine(x + math.cos(q) * r * l0, y + math.sin(q) * r * l0, x + math.cos(q) * r * 0.97,
                       y + math.sin(q) * r * 0.97, P("#1A1A1A", 0.8 * a * detail, stroke=max(1.0, r * (0.012 if k % 5 else 0.022))))
        rom = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
        if r > 60:
            for k, s_ in enumerate(rom):
                q = math.radians(k * 30 - 90)
                text(c, s_, x + math.cos(q) * r * 0.81, y + math.sin(q) * r * 0.81 + r * 0.04, r * 0.11, "#14213D",
                     "Poppins-Bold", a=a * detail)
    hcol = {"blue": "#14213D", "iron": IRON, "copper": COPPER}[hand_kind]
    ha = math.radians((hour % 12 + minute / 60.0) * 30 - 90)
    ma = math.radians(minute * 6 - 90) if min_ang is None else math.radians(min_ang - 90)
    w_h = r * (0.07 if hand_kind != "iron" else 0.09)
    c.drawLine(x - math.cos(ha) * r * 0.15, y - math.sin(ha) * r * 0.15, x + math.cos(ha) * r * 0.5, y + math.sin(ha) * r * 0.5,
               P(hcol, a, stroke=w_h))
    wm = r * {"blue": 0.045, "iron": 0.085, "copper": 0.04}[hand_kind] * hand_scale
    c.drawLine(x - math.cos(ma) * r * 0.25, y - math.sin(ma) * r * 0.25, x + math.cos(ma) * r * 0.86, y + math.sin(ma) * r * 0.86,
               P(hcol, a, stroke=wm))
    if hand_kind == "copper":
        c.drawLine(x, y, x + math.cos(ma) * r * 0.84, y + math.sin(ma) * r * 0.84, P("#F4B27A", 0.8 * a, stroke=wm * 0.35))
    c.drawCircle(x, y, r * 0.06, P(hcol, a))


# ------------------------------------------------------------------------------------------ the tower and London
def elizabeth(c, t, lit=0.0, a=1.0, dusk=0.0, hour=10, minute=10):
    """The clock tower, front view, base centre at (0, 0), 960 units tall (world)."""
    st = mix(STONE, "#9C8AA0", dusk * 0.35)
    ss = mix(STONE_S, "#7A6A84", dusk * 0.35)
    sd = mix(STONE_D, "#4A3E58", dusk * 0.35)
    c.drawRect(R(-55, -520, 110, 520), lin_paint(-55, 0, 55, 0, [ss, st, st, ss, sd], a=a))     # the shaft
    for k in range(-2, 3):                                       # Gothic panels
        xx = k * 22
        c.drawLine(xx, -515, xx, -10, P(sd, 0.55 * a, stroke=2.5))
    for yy in range(-500, -10, 46):
        c.drawLine(-55, yy, 55, yy, P(sd, 0.35 * a, stroke=2))
        for k in range(-2, 2):
            c.drawRect(R(k * 22 + 7, yy + 12, 8, 18), P(mix("#3A2E2A", "#FFD27A", lit), 0.75 * a))
    c.drawRect(R(-70, -650, 140, 130), lin_paint(-70, 0, 70, 0, [ss, st, st, ss, sd], a=a))    # the clock stage
    c.drawRect(R(-64, -644, 128, 118), P(mix(GILT_D, "#5A4520", 0.4), 0.9 * a))
    c.drawRect(R(-60, -640, 120, 110), P(PRUSSIAN, 0.55 * a))
    dial(c, 0, DIAL_Y, DIAL_R, hour, minute, lit=lit, a=a, detail=0.0)
    for sx in (-70, 70):                                         # corner pinnacles
        c.drawRect(R(sx - 7, -700, 14, 80), P(st, a))
        c.drawPath(path_of([(sx - 8, -700), (sx, -738), (sx + 8, -700)], close=True), P(GILT, a))
    c.drawRect(R(-62, -735, 124, 85), lin_paint(-62, 0, 62, 0, [ss, st, ss, sd], a=a))         # the belfry
    for k in (-1, 0, 1):
        ax = k * 36
        p_ = skia.Path()
        p_.moveTo(ax - 12, -660)
        p_.lineTo(ax - 12, -712)
        p_.quadTo(ax - 12, -726, ax, -730)
        p_.quadTo(ax + 12, -726, ax + 12, -712)
        p_.lineTo(ax + 12, -660)
        p_.close()
        c.drawPath(p_, P(mix("#1A1620", "#FFD27A", lit * 0.6), a))
    roof = path_of([(-66, -735), (66, -735), (34, -850), (-34, -850)], close=True)              # the iron roof
    c.drawPath(roof, lin_paint(-66, 0, 66, 0, [shade(SLATE, 0.25), SLATE, shade(SLATE, -0.35)], a=a))
    for k in range(-3, 4):
        c.drawLine(k * 19, -735, k * 10, -850, P(GILT, 0.55 * a, stroke=2))
    for sx in (-40, 40):                                         # little gables with gilded tops
        c.drawPath(path_of([(sx - 12, -770), (sx, -800), (sx + 12, -770)], close=True), P(mix(GILT, "#FFF1B8", lit), a))
    c.drawRect(R(-18, -880, 36, 30), P(mix("#2A2A36", "#FFF1C0", max(lit, 0.0)), a))          # the lantern
    if lit > 0:
        add_glow(c, 0, -866, 60, "#FFF1C0", 0.8 * lit * a)
    c.drawPath(path_of([(-22, -880), (0, -950), (22, -880)], close=True), P(SLATE, a))
    c.drawLine(0, -950, 0, -975, P(GILT, a, stroke=4))
    c.drawCircle(0, -978, 5, P("#F6D77A", a))
    if lit > 0:
        add_glow(c, 0, -400, 200, "#FFC46A", 0.18 * lit * a)


def palace(c, x0, x1, t, lit=0.0, dusk=0.0, a=1.0):
    """The long Gothic front of the Palace to the left of the tower (world, standing on y = 0)."""
    st = mix(STONE, "#9C8AA0", dusk * 0.35)
    sd = mix(STONE_D, "#4A3E58", dusk * 0.35)
    c.drawRect(R(x0, -230, x1 - x0, 230), lin_paint(0, -230, 0, 0, [st, shade(st, -0.12)], a=a))
    x = x0
    while x < x1:
        c.drawRect(R(x, -262, 10, 262), P(sd, 0.7 * a))
        c.drawPath(path_of([(x - 3, -262), (x + 5, -292), (x + 13, -262)], close=True), P(sd, a))
        for row, yy in enumerate((-200, -130, -60)):
            c.drawRect(R(x + 16, yy, 14, 34), P(mix("#3A2E2A", "#FFD27A", lit), 0.8 * a))
        x += 44
    c.drawRect(R(x0, -236, x1 - x0, 8), P(sd, a))


def london_eye(c, x, y, r, t, a=1.0, lit=0.0):
    c.drawCircle(x, y, r, P(mix("#B8C4D4", "#9AD7FF", lit), 0.55 * a, stroke=5))
    for k in range(16):
        q = math.radians(k * 22.5 + t * 2)
        c.drawLine(x, y, x + math.cos(q) * r, y + math.sin(q) * r, P("#B8C4D4", 0.25 * a, stroke=1.5))
        c.drawCircle(x + math.cos(q) * r, y + math.sin(q) * r, 6, P(mix("#D9E2EC", "#9AD7FF", lit), 0.6 * a))
    c.drawLine(x, y, x - r * 0.5, y + r * 1.1, P("#B8C4D4", 0.5 * a, stroke=4))
    c.drawLine(x, y, x + r * 0.5, y + r * 1.1, P("#B8C4D4", 0.5 * a, stroke=4))


# ------------------------------------------------------------------------------------------ the pendulum board
def coin(c, x, y, w, a=1.0, top=False):
    """An old copper penny seen edge-on (a short cylinder) at (x, y)."""
    h = w * 0.16
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, h / 2), lin_paint(x - w / 2, 0, x + w / 2, 0, ["#7A3E1A", "#D98A4A", "#9A5428"], a=a))
    if top:
        c.drawOval(R(x - w / 2, y - h, w, h * 0.9), P("#E9A066", a))


def pendulum(c, px, py, L, t, ang, a=1.0, pennies=3.0, scale=1.0, heat=0.0, cold=0.0, stretch=0.0):
    """The Great Clock's pendulum hanging from (px, py), length L (screen), swung by ang degrees, with the shelf of
    pennies above the bob. pennies may be fractional (the top one dropping in)."""
    c.save()
    c.translate(px, py)
    c.rotate(ang)
    L2 = L * (1 + 0.012 * stretch)
    rod = mix(mix("#5A6170", "#EF4444", 0.5 * heat), "#60A5FA", 0.5 * cold)
    c.drawRect(R(-7 * scale, 0, 14 * scale, L2 - 40 * scale), lin_paint(-7 * scale, 0, 7 * scale, 0, [shade(rod, 0.3), rod, shade(rod, -0.3)], a=a))
    if heat > 0:
        add_glow(c, 0, L2 * 0.5, 90 * scale, "#EF4444", 0.35 * heat * a)
    if cold > 0:
        add_glow(c, 0, L2 * 0.5, 90 * scale, "#60A5FA", 0.35 * cold * a)
    sy = L2 - 175 * scale                                        # the shelf for the pennies
    c.drawRect(R(-46 * scale, sy, 92 * scale, 8 * scale), P("#9CA3AF", a))
    n = int(math.floor(pennies))
    for k in range(n):
        coin(c, 0, sy - 5 * scale - k * 8 * scale, 54 * scale, a=a, top=(k == n - 1 and pennies - n < 0.05))
    fr = pennies - n
    if fr > 0.01:                                                # the next penny dropping onto the stack
        yy = sy - 5 * scale - n * 8 * scale - (1 - e_out(fr)) * 160 * scale
        coin(c, 0, yy, 54 * scale, a=a, top=True)
    by = L2 - 40 * scale                                         # the bob, a heavy cylinder
    c.drawRRect(rr(-70 * scale, by - 70 * scale, 140 * scale, 150 * scale, 24 * scale),
                lin_paint(-70 * scale, 0, 70 * scale, 0, ["#3A3F47", "#8A919C", "#5A6170", "#2A2E35"], [0.0, 0.35, 0.6, 1.0], a=a))
    c.drawRect(R(-70 * scale, by - 20 * scale, 140 * scale, 6 * scale), P("#2A2E35", 0.6 * a))
    c.restore()


def shaft_bg(c, t, warm=0.6):
    """Inside the tower: a tall dark brick shaft with a warm light from above (screen)."""
    c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#2A2230", "#1C1824", "#120F18"]))
    for row in range(0, 60):
        yy = 260 + row * 26
        if yy > 1240:
            break
        off = 0 if row % 2 else 32
        for k in range(-1, 18):
            c.drawRect(R(k * 64 + off, yy, 60, 22), P("#3A2A30", 0.5))
    add_glow(c, 540, 250, 620, "#FFD9A0", 0.32 * warm)
    c.drawRect(R(0, 1180, W, 80), P("#26222C"))


def hand_drop(c, x, y, s, a=1.0, open_=0.0):
    """A hand reaching in from the right, a penny between finger and thumb (screen)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(20, -30, 260, 56, 26), P("#E8B48A", a))
    c.drawRRect(rr(250, -40, 200, 76, 20), P("#1E3A8A", a))
    c.drawRRect(rr(-30, -26 - 10 * open_, 70, 22, 11), P("#E8B48A", a))
    c.drawRRect(rr(-24, 4 + 10 * open_, 60, 20, 10), P("#D9A07A", a))
    c.restore()


def thermometer(c, x, y, s, frac, hot=True, a=1.0):
    c.drawRRect(rr(x - 14 * s, y - 150 * s, 28 * s, 160 * s, 14 * s), P("#F8FAFC", a))
    col = "#EF4444" if hot else "#60A5FA"
    c.drawCircle(x, y + 16 * s, 24 * s, P(col, a))
    c.drawRRect(rr(x - 7 * s, y - 140 * s * frac, 14 * s, 140 * s * frac + 10 * s, 7 * s), P(col, a))


# ------------------------------------------------------------------------------------------ Greenwich, the escapement, the bell
def observatory(c, x, y, s, t, a=1.0):
    """Greenwich: a red-brick house with a white dome and a telescope (screen, standing on y)."""
    c.drawRect(R(x - 160 * s, y - 220 * s, 320 * s, 220 * s), lin_paint(0, y - 220 * s, 0, y, ["#B5563A", "#8A3A28"], a=a))
    for k in range(3):
        c.drawRRect(rr(x - 120 * s + k * 90 * s, y - 170 * s, 50 * s, 90 * s, 20 * s), P("#F3EEDC", 0.85 * a))
    dome = skia.Path()
    dome.addArc(R(x - 110 * s, y - 330 * s, 220 * s, 220 * s), 180, 180)
    dome.close()
    c.drawPath(dome, lin_paint(x - 110 * s, 0, x + 110 * s, 0, ["#CBD5E1", "#F8FAFC", "#94A3B8"], a=a))
    c.save()
    c.translate(x + 20 * s, y - 280 * s)
    c.rotate(-35)
    c.drawRRect(rr(-14 * s, -150 * s, 28 * s, 170 * s, 10 * s), P("#334155", a))
    c.restore()


def escape_wheel(c, x, y, r, ang, a=1.0, col="#E2B84A"):
    """A three-legged escape wheel (two sets of three legs, the second turned 60 degrees) at (x, y)."""
    for set_, al in ((0, 1.0), (60, 0.55)):
        for k in range(3):
            q = math.radians(ang + set_ + k * 120)
            c.drawLine(x, y, x + math.cos(q) * r, y + math.sin(q) * r, P(col, al * a, stroke=r * 0.12))
            c.drawCircle(x + math.cos(q) * r, y + math.sin(q) * r, r * 0.09, P(col, al * a))
    c.drawCircle(x, y, r * 0.18, P(shade(col, -0.3), a))


def gear(c, x, y, r, ang, teeth=14, col="#9CA3AF", a=1.0):
    p_ = skia.Path()
    for k in range(teeth * 2):
        q = math.radians(ang + k * 180.0 / teeth)
        rr_ = r if k % 2 == 0 else r * 0.84
        px_, py_ = x + math.cos(q) * rr_, y + math.sin(q) * rr_
        if k == 0:
            p_.moveTo(px_, py_)
        else:
            p_.lineTo(px_, py_)
    p_.close()
    c.drawPath(p_, P(col, a))
    c.drawCircle(x, y, r * 0.25, P(shade(col, -0.4), a))


def great_bell(c, x, y, s, t, crack=0.0, ring=0.0, a=1.0, hammer=0.0):
    """Big Ben, the bell, hanging under its beam (screen): crown at (x, y)."""
    c.save()
    c.translate(x + math.sin(t * 40) * 3 * ring, y)
    c.scale(s, s)
    c.drawRect(R(-330, -60, 660, 40), P("#4B5563", a))          # the iron beam
    c.drawRect(R(-40, -20, 80, 40), P("#374151", a))
    body = skia.Path()
    body.moveTo(-70, 20)
    body.cubicTo(-150, 30, -160, 200, -190, 330)
    body.lineTo(-245, 380)
    body.lineTo(245, 380)
    body.lineTo(190, 330)
    body.cubicTo(160, 200, 150, 30, 70, 20)
    body.close()
    c.drawPath(body, lin_paint(-245, 0, 245, 0, ["#4A3A20", BRONZE, "#C8A060", "#6A5228"], [0.0, 0.35, 0.55, 1.0], a=a))
    c.drawRect(R(-235, 340, 470, 14), P("#5A4520", 0.6 * a))
    c.drawRect(R(-170, 150, 340, 8), P("#5A4520", 0.5 * a))
    if crack > 0:                                                # the crack, growing up from the rim
        pts = [(60, 380), (52, 350), (66, 320), (48, 290), (60, 262), (44, 236), (54, 210)]
        n = 1 + int(crack * (len(pts) - 1))
        c.drawPath(path_of(pts[:n + 1] if n + 1 <= len(pts) else pts), P("#1A1208", a, stroke=6))
        c.drawPath(path_of(pts[:n + 1] if n + 1 <= len(pts) else pts), P(WARN, 0.6 * a, stroke=3))
    c.restore()
    if hammer > 0 or ring > 0:                                   # the hammer outside, on its arm
        hx, hy = x + 300 * s - 40 * s * hammer, y + 240 * s
        c.drawLine(hx + 120 * s, hy - 200 * s, hx + 30 * s, hy, P("#6B7280", a, stroke=10 * s))
        c.drawRRect(rr(hx - 10 * s, hy - 40 * s, 80 * s, 80 * s, 10 * s), P("#4B5563", a))
    if ring > 0:
        for k in range(3):
            r_ = (200 + k * 110 + (t * 260) % 110) * s
            p_ = skia.Path()
            p_.addArc(R(x - r_, y + 200 * s - r_, 2 * r_, 2 * r_), -30, 60)
            c.drawPath(p_, P("#FDE68A", 0.7 * ring * (1 - k / 3), stroke=8))
            p_ = skia.Path()
            p_.addArc(R(x - r_, y + 200 * s - r_, 2 * r_, 2 * r_), 150, 60)
            c.drawPath(p_, P("#FDE68A", 0.7 * ring * (1 - k / 3), stroke=8))


def bed_scene(c, t, rtl=False, spin=0.0):
    """A bedroom at night (EN: in bed with the phone) or a sitting room (AR: on the couch with the phone) (screen)."""
    c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1E2440", "#2A3156", "#1A1E36"]))
    c.drawRect(R(0, 1180, W, 760), P("#3A2E3E"))
    if not rtl:
        c.drawRRect(rr(620, 380, 360, 420, 16), P("#0E1430"))      # the window with the clock tower outside
        c.save()
        c.clipRRect(rr(620, 380, 360, 420, 16))
        c.drawRect(R(620, 380, 360, 420), lin_paint(0, 380, 0, 800, ["#0A1238", "#2A2A60"]))
        c.translate(800, 800)
        c.scale(0.42, 0.42)
        elizabeth(c, t, lit=1.0, dusk=1.0, hour=9, minute=5)
        c.restore()
        c.drawRect(R(796, 380, 8, 420), P("#5A4A3A"))
        c.drawRect(R(620, 586, 360, 8), P("#5A4A3A"))
        c.drawRRect(rr(60, 980, 820, 220, 30), P("#6B4F3A"))        # the bed
        c.drawRRect(rr(80, 900, 220, 110, 40), P("#E5E7EB"))
        c.drawRRect(rr(220, 940, 640, 160, 50), P("#3B82F6"))       # blanket
        c.drawCircle(200, 930, 62, P("#E8B48A"))
        c.drawPath(path_of([(140, 905), (200, 860), (262, 905)], close=True), P("#2B2530"))
    else:
        c.drawCircle(780, 560, 150, P("#F8FAFC"))                   # a wall clock that runs an hour fast
        c.drawCircle(780, 560, 150, P("#1F2937", stroke=10))
        for k in range(12):
            q = math.radians(k * 30)
            c.drawLine(780 + math.cos(q) * 118, 560 + math.sin(q) * 118, 780 + math.cos(q) * 138, 560 + math.sin(q) * 138,
                       P("#1F2937", stroke=6))
        ma = math.radians(spin * 360 - 90)
        ha = math.radians(spin * 30 + 120 - 90)
        c.drawLine(780, 560, 780 + math.cos(ha) * 70, 560 + math.sin(ha) * 70, P("#1F2937", stroke=12))
        c.drawLine(780, 560, 780 + math.cos(ma) * 112, 560 + math.sin(ma) * 112, P("#DC2626", stroke=7))
        c.drawRRect(rr(60, 1000, 760, 180, 40), P("#8A6A4A"))       # the couch
        c.drawRRect(rr(60, 900, 760, 130, 40), P("#9A7A5A"))
        saudi_man(c, 420, 1150, 330, t, pose="sit", face=1)


# ====================================================================================== the episode
PIVX, PIVY, PLEN = 540.0, 160.0, 860.0                           # the pendulum on its board (screen units)


class BigBen(EpisodeV2):
    BUILD_NO = 64
    FIRST_SET = "pend"
    CLEAR = "#0A0A2A"
    TITLE = {"en": "BIG BEN'S CLOCK", "ar_sa": "ساعة بيغ بن"}
    EMPH = {"en": ["CONGRATS", "STACK", "OLD", "PENNIES", "WORLD'S", "FAMOUS", "CLOCK", "TIME", "BIG", "BEN'S",
                   "YOURSELF", "ASTRONOMER", "ROYAL", "HOUR", "SECOND", "TWICE", "HANG", "PENDULUM", "FOUR", "METERS",
                   "TICKS", "TWO", "SECONDS", "HANDS", "OUTSIDE", "GUST", "WIND", "GEARS", "GRAVITY", "ESCAPEMENT",
                   "ARMS", "SAME", "PUSH", "SWING", "CAST", "IRON", "HEAVY", "TURN", "THIN", "COPPER", "DIALS",
                   "SEVEN", "WIDE", "HEAT", "COLD", "DRIFT", "GAIN", "TENTHS", "DAY", "FOLLOW", "MUD", "SKYSCRAPERS",
                   "TWIST", "BEN", "BELL", "TOWER", "CRACKED", "FIRST", "YEAR", "RINGS", "TODAY", "SEVEN-METER",
                   "FOURTEEN", "TONS", "THREE-HUNDRED-KILO", "LONDON", "HUNDRED", "SIXTY", "YEARS", "TEXT", "WAY", "BED"],
            "ar_sa": ["مبروك", "قرش", "قديم", "أشهر", "ساعة", "بيغ", "بن", "بيدك", "الفلكي", "الملكي", "تدق",
                      "ثانيتها", "بالضبط", "بندول", "أربعة", "متر", "يتك", "ثانيتين", "العقارب", "برا", "ريح", "التروس",
                      "البندول", "ميزان", "بالجاذبية", "ذراعين", "الدفّة", "حديد", "صب", "ثقيلة", "تلفها", "نحاس",
                      "رقيق", "سبعة", "الحر", "والبرد", "وتأخّر", "قروش", "يسرّعها", "نص", "تابعني", "ناطحات", "طين",
                      "والمفاجأة", "الجرس", "البرج", "انشق", "مشقوق", "أربعطعش", "طن", "ثلاثمية", "مضبوطة", "وستين",
                      "دقايق", "ساعة"]}
    KEYS = {"ar_sa": {
        ("hook", "PENNIES"): "قرش", ("hook", "FAMOUS"): "اشهر", ("hook", "CLOCK"): "ساعه", ("hook", "CONGRATS"): "مبروك",
        ("hook", "BIG"): "بيغ",
        ("break1", "ASTRONOMER"): "الفلكي", ("break1", "HOUR"): "ساعه", ("break1", "STRUCK"): "تدق",
        ("break1", "SECOND"): "ثانيتها", ("break1", "DAY"): "بالضبط",
        ("fix1", "HANG"): "فتعلق", ("fix1", "PENDULUM"): "بندول", ("fix1", "FOUR"): "اربعه", ("fix1", "TICKS"): "يتك",
        ("fix1", "TWO"): "ثانيتين",
        ("break2", "HANDS"): "العقارب", ("break2", "OUTSIDE"): "برا", ("break2", "GUST"): "هبه", ("break2", "PUSHES"): "تدف",
        ("break2", "GEARS"): "التروس", ("break2", "PENDULUM"): "البندول",
        ("fix2", "GRAVITY"): "بالجاذبيه", ("fix2", "ESCAPEMENT"): "ميزان", ("fix2", "ARMS"): "ذراعين",
        ("fix2", "SAME"): "نفس", ("fix2", "PUSH"): "الدفه", ("fix2", "SWING"): "مره", ("fix2", "WHATEVER"): "مره",
        ("break3", "FIRST"): "اول", ("break3", "IRON"): "حديد", ("break3", "HEAVY"): "ثقيله", ("break3", "CANT"): "قدرت",
        ("break3", "TURN"): "تلفها",
        ("fix3", "THIN"): "رقيق", ("fix3", "COPPER"): "نحاس", ("fix3", "FOUR"): "اربعه", ("fix3", "DIALS"): "وجه",
        ("fix3", "SEVEN"): "سبعه", ("fix3", "WIDE"): "عرضه",
        ("break4", "HEAT"): "الحر", ("break4", "COLD"): "والبرد", ("break4", "DRIFT"): "وتاخر",
        ("fix4", "ADD"): "فتحط", ("fix4", "PENNIES"): "قروش", ("fix4", "EACH"): "وكل", ("fix4", "GAIN"): "يسرعها",
        ("fix4", "TENTHS"): "نص", ("fix4", "DAY"): "اليوم",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "TWIST"): "والمفاجاه", ("reveal", "BEN"): "بن", ("reveal", "BELL"): "الجرس", ("reveal", "TOWER"): "البرج",
        ("reveal", "CRACKED"): "انشق", ("reveal", "FIRST"): "اول", ("reveal", "RINGS"): "يدق", ("reveal", "TODAY"): "مشقوق",
        ("stat", "SEVEN"): "سبعه", ("stat", "FOURTEEN"): "اربعطعش", ("stat", "THREE"): "ثلاثميه",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "KEPT"): "مضبوطه", ("tag", "YEARS"): "سنه", ("tag", "STILL"): "وانت", ("tag", "TEXT"): "قلت",
        ("tag", "BED"): "يعني"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: Shibam's mud skyscrapers"),
                   "stat": [("7 m", "EACH DIAL"), ("13.7 t", "THE BELL"), ("300 kg", "THE PENDULUM")],
                   "L": {"pennies": "OLD PENNIES", "famous": "THE WORLD'S MOST FAMOUS CLOCK", "name": "BIG BEN'S CLOCK, LONDON",
                         "astro": "THE ASTRONOMER ROYAL", "second": "EVERY HOUR, TO THE SECOND", "checked": "CHECKED 2× A DAY",
                         "bong": "BONG!", "four": "ALMOST 4 M", "tick": "TICK... 2 S", "hands": "HANDS OUT IN THE WIND",
                         "gears": "THROUGH THE GEARS", "offbeat": "PENDULUM OFF ITS BEAT", "gravity": "GRAVITY ESCAPEMENT",
                         "arms": "TWO SMALL ARMS", "same": "THE SAME PUSH, EVERY SWING", "wind": "THE WIND CAN'T REACH IT",
                         "iron": "CAST IRON", "heavy": "TOO HEAVY TO TURN", "copper": "THIN COPPER", "m42": "4.2 M",
                         "m7": "7 M WIDE", "heat": "HEAT", "cold": "COLD", "drift": "DRIFTS OFF TIME",
                         "plus": "+0.4 S A DAY", "ontime": "ON TIME", "twist": "THE TWIST", "bigben": "BIG BEN",
                         "bell": "BIG BEN = THE BELL", "nottower": "NOT THE TOWER", "cracked": "CRACKED IN 1859",
                         "rings": "STILL RINGS CRACKED", "omw": "On my way!"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: شبام، ناطحات الطين"),
                      "stat": [("7", "متر كل وجه"), ("13.7", "طن الجرس"), ("300", "كيلو البندول")],
                      "L": {"pennies": "قروش قديمة", "famous": "أشهر ساعة في العالم", "name": "ساعة بيغ بن، لندن",
                            "astro": "الفلكي الملكي", "second": "كل ساعة بالثانية", "checked": "بالضبط",
                            "bong": "دنننق!", "four": "قرابة أربعة متر", "tick": "تك... كل ثانيتين",
                            "hands": "العقارب برا في الهوا", "gears": "عبر التروس", "offbeat": "البندول يتلخبط",
                            "gravity": "ميزان بالجاذبية", "arms": "ذراعين صغار", "same": "نفس الدفّة كل مرة",
                            "wind": "الهوا ما يوصله", "iron": "حديد صب", "heavy": "ثقيلة، ما تلف", "copper": "نحاس رقيق",
                            "m42": "4.2 م", "m7": "عرضه سبعة متر", "heat": "حر", "cold": "برد", "drift": "تقدّم وتأخّر",
                            "plus": "أسرع شوي", "ontime": "مضبوطة", "twist": "المفاجأة", "bigben": "بيغ بن",
                            "bell": "بيغ بن هو الجرس", "nottower": "مو البرج", "cracked": "انشق أول سنة",
                            "rings": "وللحين يدق مشقوق", "omw": "خمس دقايق وأكون عندك"}}}
    COVER_T = ("closer", 0.5)

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "pennies": ("hook", "PENNIES", 0.2), "famous": ("hook", "FAMOUS", 0.4), "clock": ("hook", "CLOCK", 0.5),
            "congrats": ("hook", "CONGRATS", 0.65), "bigben": ("hook", "BIG", 0.85),
            "astro": ("break1", "ASTRONOMER", 0.1), "hour": ("break1", "HOUR", 0.35), "struck": ("break1", "STRUCK", 0.45),
            "second": ("break1", "SECOND", 0.65), "day": ("break1", "DAY", 0.95),
            "hang": ("fix1", "HANG", 0.1), "pend1": ("fix1", "PENDULUM", 0.2), "four": ("fix1", "FOUR", 0.4),
            "ticks": ("fix1", "TICKS", 0.65), "two": ("fix1", "TWO", 0.85),
            "hands": ("break2", "HANDS", 0.1), "outside": ("break2", "OUTSIDE", 0.25), "gust": ("break2", "GUST", 0.4),
            "pushes": ("break2", "PUSHES", 0.55), "gears": ("break2", "GEARS", 0.75), "pend2": ("break2", "PENDULUM", 0.92),
            "gravity": ("fix2", "GRAVITY", 0.1), "escape": ("fix2", "ESCAPEMENT", 0.2), "arms": ("fix2", "ARMS", 0.4),
            "same": ("fix2", "SAME", 0.6), "push": ("fix2", "PUSH", 0.65), "swing": ("fix2", "SWING", 0.75),
            "whatever": ("fix2", "WHATEVER", 0.85),
            "first": ("break3", "FIRST", 0.1), "iron": ("break3", "IRON", 0.35), "heavy": ("break3", "HEAVY", 0.55),
            "cant": ("break3", "CANT", 0.75), "turn": ("break3", "TURN", 0.9),
            "thin": ("fix3", "THIN", 0.2), "copper": ("fix3", "COPPER", 0.3), "four3": ("fix3", "FOUR", 0.5),
            "dials": ("fix3", "DIALS", 0.7), "seven": ("fix3", "SEVEN", 0.8), "wide": ("fix3", "WIDE", 0.95),
            "heat": ("break4", "HEAT", 0.15), "cold": ("break4", "COLD", 0.4), "drift": ("break4", "DRIFT", 0.9),
            "add": ("fix4", "ADD", 0.1), "pennies4": ("fix4", "PENNIES", 0.2), "each": ("fix4", "EACH", 0.45),
            "gain": ("fix4", "GAIN", 0.6), "tenths": ("fix4", "TENTHS", 0.75), "day4": ("fix4", "DAY", 0.95),
            "follow": ("cta", "FOLLOW", 0.35),
            "twist": ("reveal", "TWIST", 0.05), "ben": ("reveal", "BEN", 0.15), "bell": ("reveal", "BELL", 0.3),
            "tower2": ("reveal", "TOWER", 0.45), "cracked": ("reveal", "CRACKED", 0.6), "first2": ("reveal", "FIRST", 0.7),
            "rings": ("reveal", "RINGS", 0.85), "today": ("reveal", "TODAY", 0.95),
            "s1": ("stat", "SEVEN", 0.05), "s2": ("stat", "FOURTEEN", 0.4), "s3": ("stat", "THREE", 0.8),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_kept": ("tag", "KEPT", 0.1), "t_years": ("tag", "YEARS", 0.35), "t_still": ("tag", "STILL", 0.55),
            "t_text": ("tag", "TEXT", 0.7), "t_bed": ("tag", "BED", 0.92)})
        T["day1"] = max(T["day"], T["second"]) + 0.2
        T["pend21"] = max(T["pend2"], T["gears"]) + 0.15
        T["turn1"] = max(T["turn"], T["cant"]) + 0.15
        T["drift1"] = max(T["drift"], T["cold"]) + 0.15
        T["two1"] = max(T["two"], T["ticks"]) + 0.3
        T["what1"] = max(T["whatever"], T["swing"]) + 0.3
        T["wide1"] = max(T["wide"], T["seven"]) + 0.3
        T["day41"] = max(T["day4"], T["tenths"]) + 0.3
        T["famous"] = max(T["famous"], T["pennies"] + 0.6)
        # ---- sets
        self.cut(T["famous"] - 0.15, "tower", 1)
        self.cut(s("break1") - 0.12, "airy", -1)
        self.cut(s("fix1") - 0.12, "pend", 1)
        self.cut(s("break2") - 0.12, "escape", -1)
        self.cut(s("break3") - 0.12, "hands", 1)
        self.cut(s("break4") - 0.12, "pend", -1)
        self.cut(s("reveal") - 0.12, "bell", 1)
        self.cut(s("stat") - 0.12, "tower", -1)
        self.cut(s("tag") - 0.2, "tag", 1)
        # ---- tower camera: from the dial out to the whole tower by "congrats"
        cm = Camera(0, DIAL_Y, 5.0)
        cm.key(T["famous"] - 0.15, 0, DIAL_Y, 5.0, 0.0)
        cm.key(T["famous"] - 0.1, 0, -560, 1.35, max(1.0, T["congrats"] - T["famous"] + 0.5))
        cm.key(s("break1") - 0.3, 0, -562, 1.37, 1.0)
        cm.key(s("stat") - 0.12, 0, -650, 2.3, 0.0).key(s("stat"), 0, -652, 2.35, max(0.5, s("closer") - s("stat") - 0.3))
        cm.key(s("closer") - 0.1, 0, -640, 1.95, 1.0).key(s("closer") + 0.9, 0, -642, 2.02, 3.0)
        self.cam = cm
        self.spans = [(T["day1"], T["two1"] + 0.3), (T["pend21"], T["what1"] + 0.3), (T["turn1"], T["wide1"] + 0.3),
                      (T["drift1"], T["day41"] + 0.3)]
        self.shakes = [(T["pennies"] + 0.35, 0.25, 5), (T["congrats"], 0.35, 8), (T["day1"], 0.4, 7), (T["gust"], 0.4, 8),
                       (T["turn1"], 0.4, 7), (T["drift1"], 0.3, 6), (T["rings"], 0.6, 9), (s("closer") + 0.2, 0.35, 9)]

    # ------------------------------------------------------------------ set: pend (hook 1, fix1, break4, fix4)
    def swing(self, t, amp=3.0):
        return amp * math.sin(2 * math.pi * t / 4.0)

    def draw_pend(self, c, t):
        T, s = self.T, self.tl.s
        shaft_bg(c, t)
        hook = t < s("break1")
        if hook:
            fz, fx, fy = 1.85, 540.0, 860.0
        elif t < s("break2"):
            fz, fx, fy = 1.0, 540.0, 700.0
        else:
            fz, fx, fy = 1.5, 540.0, 830.0
        c.save()
        c.translate(540, 760)
        c.scale(fz, fz)
        c.translate(-fx, -fy)
        ang = self.swing(t, 2.6 if hook else 3.2)
        if hook:                                                 # the giant dial, lit from behind, over the pendulum
            c.save()
            c.translate(540, 330)
            c.scale(-1, 1)
            dial(c, 0, 0, 420, 10, 10, lit=1.0, detail=1.0)
            c.restore()
            c.drawCircle(540, 330, 420 * 1.16, P("#0A0A1A", 0.35))
            add_glow(c, 540, 600, 520, "#FFE6A8", 0.35)
            n = 4 + prog(t, T["pennies"] - 0.05, T["pennies"] + 0.35)
            pendulum(c, PIVX, PIVY, PLEN, t, ang, pennies=n)
        elif t < s("break2"):                                    # fix1: the whole pendulum next to a man
            c.drawRect(R(-200, 1180, 1500, 300), P("#26222C"))
            pendulum(c, PIVX, PIVY, PLEN, t, ang, pennies=4)
            engineer(c, 820, 1180, 400, "#2563EB", t, pose="look", face=-1)
            dk = prog(t, T["four"] - 0.3, T["four"] + 0.2)
            if dk > 0:
                c.drawLine(300, PIVY, 300, PIVY + PLEN, P("#FDE047", dk, stroke=5))
                for yy in (PIVY, PIVY + PLEN):
                    c.drawLine(280, yy, 320, yy, P("#FDE047", dk, stroke=5))
            c.drawRect(R(PIVX - 60, PIVY - 30, 120, 30), P("#4B5563"))
        else:                                                    # break4 / fix4: the shelf of pennies
            fixed = t >= s("fix4") - 0.12
            heat = 0.0 if fixed else prog(t, T["heat"] - 0.2, T["heat"] + 0.2) * (1 - prog(t, T["cold"] - 0.2, T["cold"] + 0.1))
            cold = 0.0 if fixed else prog(t, T["cold"] - 0.2, T["cold"] + 0.1)
            stretch = heat - cold
            n = 4.0
            if fixed:
                n = 4 + prog(t, T["add"] - 0.1, T["add"] + 0.35) + prog(t, T["pennies4"] + 0.1, T["pennies4"] + 0.45) \
                    + prog(t, T["each"] - 0.1, T["each"] + 0.25)
            pendulum(c, PIVX, PIVY, PLEN, t, ang, pennies=n, heat=heat, cold=cold, stretch=stretch * 3)
            self.ui["fixed4"] = fixed
            self.ui["pn"] = n
        c.restore()
        # the hand that drops the penny (screen space, over the zoomed board)
        if hook:
            hk = prog(t, T["pennies"] - 0.6, T["pennies"] - 0.2) * (1 - prog(t, T["pennies"] + 0.4, T["pennies"] + 0.8))
            if hk > 0:
                q = math.radians(ang)
                sx = 540 + (PIVX + math.sin(-q) * (PLEN - 230) - 540) * 1.85
                sy = 760 + (PIVY + math.cos(q) * (PLEN - 230) - 860) * 1.85
                hand_drop(c, sx + 60 + (1 - hk) * 500, sy - 250, 1.0, open_=prog(t, T["pennies"] - 0.1, T["pennies"] + 0.1))
        elif t >= s("fix4") - 0.12:
            for k, tk in enumerate((T["add"], T["pennies4"] + 0.2, T["each"])):
                hk = prog(t, tk - 0.5, tk - 0.15) * (1 - prog(t, tk + 0.25, tk + 0.6))
                if hk > 0:
                    hand_drop(c, 640 + (1 - hk) * 500, 470 - k * 22, 1.0, open_=prog(t, tk - 0.05, tk + 0.1))

    def ui_pend(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1"):
            self.chip(540, 300, "pennies", T["pennies"] - 0.2, T["famous"], accent="#F59E0B", size=50)
            return
        if tw < s("break2"):
            self.chip(540, 300, "four", T["four"] - 0.2, T["ticks"] - 0.1, accent="#FDE047", size=48)
            self.chip(540, 300, "tick", T["ticks"] - 0.1, s("break2") - 0.15, accent=GOOD, size=46)
            self.badge("check", T["two1"] + 0.1, s("break2") - 0.15, x=920, y=420)
            return
        if tw < s("fix4") - 0.12:
            self.chip(300, 470, "heat", T["heat"] - 0.2, T["cold"] - 0.1, accent=WARN, size=48)
            self.chip(780, 470, "cold", T["cold"] - 0.1, s("fix4") - 0.15, accent="#60A5FA", size=48)
            self.chip(540, 300, "drift", T["drift"] - 0.3, s("fix4") - 0.15, accent=WARN, size=46)
            hk = self.span(T["heat"] - 0.2, s("fix4") - 0.15)
            if hk > 0:
                thermometer(c, 160, 900, 1.2, 0.85 if tw < T["cold"] else 0.15, hot=tw < T["cold"], a=hk)
            self.badge("alert", T["drift1"], s("fix4") - 0.2, x=920, y=640)
            self.red(T["drift1"], 1.2)
            return
        for k, tk in enumerate((T["add"], T["pennies4"] + 0.2, T["each"])):
            pk = self.span(tk + 0.2, tk + 1.3, 0.15, 0.3)
            if pk > 0:
                v2.chip(c, 820, 700 - k * 70 - 60 * prog(tw, tk + 0.2, tk + 1.3), self.L["plus"], pk, accent=GOOD, size=34)
        self.chip(540, 300, "ontime", T["tenths"] - 0.2, s("cta") - 0.15, accent=GOOD, size=50)
        self.badge("check", T["day41"] + 0.1, s("cta") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: tower (hook 2, stat, closer)
    def draw_tower(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        closer = t >= s("closer") - 0.1
        night = prog(t, s("closer") - 0.1, s("closer") + 0.8) if closer else 0.0
        cx, cy, z = cam
        gy = (0 - cy) * z + H / 2
        v2.sky(c, W, H, 0.0, pal=NIGHTP if closer else DUSKP, horizon_y=gy)
        if closer:
            v2.stars(c, W, H, t, 0.8 * night)
        else:
            add_glow(c, 820 - cx * 0.03, gy - 140, 420, "#FFB07A", 0.3)
        self.view(c, cam)
        london_eye(c, 340, -300, 170, t, a=0.55, lit=night)
        palace(c, -1500, -60, t, lit=0.3 + 0.7 * night, dusk=0.8)
        c.drawRect(R(-1600, 0, 3200, 600), P(mix("#3A3346", "#141428", night)))
        c.drawRect(R(-1600, 0, 3200, 10), P(mix("#6A5A70", "#2A2A48", night)))
        hh, mm = (9, 0) if closer else (5, 40)
        elizabeth(c, t, lit=max(night, 0.45), dusk=0.6 + 0.4 * night, hour=hh, minute=mm)
        bx = -200 + ((t * 60) % 1200)
        if bx < 400:
            bus(c, 160 + bx, 0, 0.9, 0.0, t, face=1)
        c.restore()
        self.ui["cam"] = cam

    def ui_tower(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("break1") - 0.12:
            self.chip(540, 300, "famous", T["famous"] - 0.1, T["congrats"] - 0.1, accent="#FDE047", size=40)
            self.chip(540, 300, "name", T["bigben"] - 0.3, s("break1") + 0.1, accent=HILITE, size=44)

    # ------------------------------------------------------------------ set: airy (break1)
    def draw_airy(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#141A3A", "#2A2E5E", "#4A3A6A"]))
        add_glow(c, 300, 640, 420, "#FFD27A", 0.25)
        sk = prog(t, T["struck"] - 0.1, T["struck"] + 0.1)
        dial(c, 300, 660, 210, 12, 0, lit=0.4, detail=1.0)
        if sk > 0:
            for k in range(3):
                r_ = 230 + k * 50 + ((t - T["struck"]) * 260) % 50
                p_ = skia.Path()
                p_.addArc(R(300 - r_, 660 - r_, 2 * r_, 2 * r_), -60, 120)
                c.drawPath(p_, P("#FDE68A", 0.7 * sk * (1 - k / 3) * (1 - prog(t, T["struck"] + 1.2, T["struck"] + 1.8)), stroke=8))
        c.drawRect(R(0, 1150, W, 120), P("#1A1E36"))
        observatory(c, 820, 1150, 0.95, t)
        wire = [(300 + 180, 820)] + [(lerp(480, 820, k / 10), lerp(820, 880, k / 10) + math.sin(math.pi * k / 10) * 70)
                                     for k in range(1, 10)] + [(820, 880)]
        c.drawPath(path_of(wire), P("#CBD5E1", 0.8, stroke=4))
        pk = prog(t, T["second"], T["day1"] + 0.6)
        if pk > 0:
            for k in range(2):
                q = clamp(pk * 1.6 - k * 0.5)
                if 0 < q < 1:
                    i = min(len(wire) - 2, int(q * (len(wire) - 1)))
                    f = q * (len(wire) - 1) - i
                    px_, py_ = lerp(wire[i][0], wire[i + 1][0], f), lerp(wire[i][1], wire[i + 1][1], f)
                    add_glow(c, px_, py_, 30, "#FDE047", 0.9)
                    c.drawCircle(px_, py_, 8, P("#FEF9C3"))
        person(c, 640, 1150, 230, "#1F2937", t, pose="look", face=-1, hat="none", hair="#6B5B4B")
        c.drawRect(R(612, 1150 - 262, 56, 14), P("#111827"))   # a top hat
        c.drawRect(R(622, 1150 - 300, 36, 40), P("#111827"))
        self.ui["obs"] = (820, 900)
        self.ui["dial"] = (300, 660)

    def ui_airy(self, c, t, tw):
        T, s = self.T, self.tl.s
        ox, oy = self.ui.get("obs", (820, 900))
        self.label(ox, oy, 760, 560, "astro", T["astro"] - 0.2, s("fix1") - 0.2, accent="#93C5FD", size=36)
        self.chip(540, 300, "second", T["hour"] - 0.2, s("fix1") - 0.15, accent="#FDE047", size=44)
        hk = self.span(T["struck"] - 0.1, T["struck"] + 1.4)
        if hk > 0:
            v2.chip(c, 300, 400, self.L["bong"], hk, accent="#FDE68A", size=44)
        if not self.rtl:
            v2.chip(c, 640, 980, self.L["checked"], self.span(T["day"] - 0.6, s("fix1") - 0.15), accent=GOOD, size=34)
        self.badge("alert", T["day1"], s("fix1") - 0.2, x=920, y=420)
        self.red(T["day1"], 1.2)

    # ------------------------------------------------------------------ set: escape (break2, fix2)
    def draw_escape(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix2") - 0.12
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#1B2240", "#141A33", "#0E1226"]))
        if not fixed:
            gk = prog(t, T["gust"] - 0.2, T["gust"] + 0.2) * (1 - prog(t, T["pend21"] + 0.4, T["pend21"] + 1.0))
            jolt = 6 * math.sin(t * 30) * gk
            dial(c, 120, 700, 360, 10, 10, lit=0.2, detail=1.0, min_ang=60 + jolt)
            for k in range(7):                                   # the wind
                yy = 420 + k * 70
                x0 = ((t * 900 + k * 230) % 1400) - 400
                c.drawLine(x0, yy, x0 + 220, yy + 10, P("#E0F2FE", 0.35 + 0.4 * gk, stroke=5))
            ga = t * 40
            for (gx, gy, gr, tt) in ((560, 860, 95, 18), (700, 960, 60, 12), (760, 760, 55, 12)):
                gear(c, gx, gy, gr, ga * (1 if tt == 18 else -1.4), teeth=tt)
            amp = 3.0 + 3.0 * prog(t, T["gears"], T["pend21"]) * math.sin(t * 7)
            pendulum(c, 930, 300, 760, t, self.swing(t, amp), pennies=3, scale=0.62)
            rk = prog(t, T["pushes"] - 0.2, T["pend21"] + 0.2)
            if rk > 0:                                           # the push travelling back through the gears
                path = [(260, 640), (560, 860), (700, 960), (760, 760), (930, 360)]
                q = clamp(rk)
                n = 1 + int(q * (len(path) - 1))
                c.drawPath(path_of(path[:n + 1]), P(WARN, 0.85, stroke=9))
                if n < len(path):
                    i = n - 1
                    f = q * (len(path) - 1) - i
                    hx, hy = lerp(path[i][0], path[min(i + 1, len(path) - 1)][0], f), lerp(path[i][1], path[min(i + 1, len(path) - 1)][1], f)
                    add_glow(c, hx, hy, 40, WARN, 0.8)
            self.ui["hand"] = (300, 560)
            self.ui["pend"] = (930, 860)
            self.ui["gear"] = (560, 860)
            return
        # fix2: the gravity escapement
        add_glow(c, 540, 600, 500, "#FFD27A", 0.18)
        th = self.swing(t, 6.0)
        beat = math.floor((t + 1.0) / 2.0)
        wa = beat * 60.0 + 60.0 * e_out(clamp(((t + 1.0) % 2.0) / 0.18))
        sx_, sy_ = 540.0, 640.0
        c.drawRect(R(sx_ - 120, sy_ - 40, 240, 30), P("#4B5563"))
        escape_wheel(c, sx_, 520, 100, wa, col=GILT)
        c.drawCircle(sx_, 520, 115, P(GILT, 0.15, stroke=2))
        for sd in (-1, 1):                                       # the two gravity arms
            px_ = sx_ + sd * 34
            carried = (th * sd) > 1.0
            arm_ang = (-th if carried else -sd * 1.5)
            c.save()
            c.translate(px_, sy_ - 10)
            c.rotate(arm_ang)
            c.drawRect(R(-7, 0, 14, 330), P("#FACC15"))
            c.drawRect(R(-16 if sd < 0 else 2, 310, 14, 26), P("#FDE047"))
            c.restore()
        c.save()
        c.translate(sx_, sy_)
        c.rotate(th)
        c.drawRect(R(-8, 0, 16, 480), lin_paint(-8, 0, 8, 0, ["#9AA3B0", "#5A6170"]))
        c.drawRRect(rr(-80, 430, 160, 130, 24), lin_paint(-80, 0, 80, 0, ["#3A3F47", "#8A919C", "#2A2E35"]))
        c.restore()
        pk = prog(t, T["same"] - 0.3, T["same"]) * (1 - prog(t, s("break3") - 0.4, s("break3") - 0.1))
        if pk > 0:
            side = 1 if math.cos(2 * math.pi * t / 4.0) > 0 else -1
            ax_ = sx_ + math.sin(math.radians(-th)) * -300
            arrow(c, ax_ - side * 90, 930, ax_ - side * 20, 930, GOOD, a=pk, w=10, head=26)
        wk = prog(t, T["whatever"] - 0.3, T["whatever"])
        for k in range(5):                                       # wind arrows stopped at the wheel
            yy = 440 + k * 40
            x1 = 360 - 40 * wk
            c.drawLine(60, yy, x1, yy, P(WARN, 0.5 * wk, stroke=6))
        if wk > 0:
            c.drawCircle(390, 520, 46, P(WARN, wk, stroke=8))
            c.drawLine(358, 488, 422, 552, P(WARN, wk, stroke=8))
        self.ui["wheel"] = (sx_ + 90, 520)
        self.ui["arm"] = (sx_ + 40, 860)

    def ui_escape(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            hx, hy = self.ui.get("hand", (300, 560))
            self.label(hx, hy, 330, 330, "hands", T["hands"] - 0.2, T["pushes"] - 0.1, accent="#93C5FD", size=38)
            gx, gy = self.ui.get("gear", (560, 860))
            self.label(gx, gy, 420, 1130, "gears", T["gears"] - 0.3, s("fix2") - 0.2, accent=WARN, size=36)
            px_, py_ = self.ui.get("pend", (930, 860))
            self.label(px_, py_, 760, 330, "offbeat", T["pend2"] - 0.2, s("fix2") - 0.2, accent=WARN, size=36)
            self.badge("alert", T["pend21"], s("fix2") - 0.2, x=920, y=640)
            self.red(T["pend21"], 1.2)
            return
        self.chip(540, 300, "gravity", T["gravity"] - 0.2, T["same"] - 0.2, accent="#FDE047", size=46)
        ax_, ay_ = self.ui.get("arm", (580, 640))
        self.label(ax_, ay_, 820, 760, "arms", T["arms"] - 0.2, s("break3") - 0.2, accent="#FACC15", size=36)
        self.chip(540, 300, "same", T["same"] - 0.2, T["whatever"] - 0.2, accent=GOOD, size=40)
        self.chip(540, 300, "wind", T["whatever"] - 0.2, s("break3") - 0.15, accent=GOOD, size=42)
        self.badge("check", T["what1"] + 0.1, s("break3") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: hands (break3, fix3)
    def draw_hands(self, c, t):
        T, s = self.T, self.tl.s
        fixed = t >= s("fix3") - 0.12
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#2A2A5A", "#3A2E5E", "#1A1A36"]))
        c.drawRect(R(70, 290, 940, 940), P(mix(GILT_D, "#3A2E1A", 0.5)))
        c.drawRect(R(90, 310, 900, 900), P(PRUSSIAN, 0.6))
        if not fixed:
            strain = prog(t, T["heavy"] - 0.4, T["cant"])
            mang = 20 + 14 * strain * (0.5 + 0.5 * math.sin(t * 11)) - 10 * prog(t, T["cant"], T["turn1"])
            dial(c, 540, 760, 400, 2, 0, lit=0.3, detail=1.0, hand_kind="iron", min_ang=mang)
            if strain > 0.2:
                for k in range(6):
                    q = (t * 3 + k / 6.0) % 1.0
                    c.drawCircle(540 + math.cos(k * 1.1) * 40 * q, 760 + math.sin(k * 1.7) * 40 * q, 5, P("#FDBA74", 0.8 * (1 - q)))
            self.ui["hand"] = (540 + math.cos(math.radians(mang - 90)) * 220, 760 + math.sin(math.radians(mang - 90)) * 220)
        else:
            mang = 270 + 180 * e_io(prog(t, T["thin"] - 0.2, s("break4") - 0.4))
            dial(c, 540, 760, 400, 2, 0, lit=0.3, detail=1.0, hand_kind="copper", min_ang=mang, hand_scale=1.2)
            mk = prog(t, T["four3"] - 0.3, T["four3"] + 0.2) * (1 - prog(t, T["dials"] - 0.2, T["dials"]))
            if mk > 0:
                q = math.radians(mang - 90)
                c.drawLine(540 - math.cos(q) * 100, 760 - math.sin(q) * 100, 540 + math.cos(q) * 344, 760 + math.sin(q) * 344,
                           P("#FDE047", mk, stroke=6))
            dk = prog(t, T["seven"] - 0.3, T["seven"] + 0.2)
            if dk > 0:
                c.drawLine(140, 1200, 940, 1200, P("#FDE047", dk, stroke=6))
                for xx in (140, 940):
                    c.drawLine(xx, 1180, xx, 1220, P("#FDE047", dk, stroke=6))
            self.ui["hand"] = (540 + math.cos(math.radians(mang - 90)) * 220, 760 + math.sin(math.radians(mang - 90)) * 220)
        c.drawLine(880, 290, 880, 1010, P("#94A3B8", stroke=3))      # a worker on a cradle in front of the dial
        c.drawLine(1000, 290, 1000, 1010, P("#94A3B8", stroke=3))
        c.drawRect(R(860, 1010, 160, 16), P("#64748B"))
        engineer(c, 940, 1010, 205, "#F59E0B", t, pose="look" if not fixed else "point", face=-1)

    def ui_hands(self, c, t, tw):
        T, s = self.T, self.tl.s
        hx, hy = self.ui.get("hand", (600, 600))
        if tw < s("fix3") - 0.12:
            self.label(hx, hy, 300, 420, "iron", T["iron"] - 0.2, s("fix3") - 0.2, accent="#9CA3AF", size=40)
            self.chip(540, 300, "heavy", T["heavy"] - 0.2, s("fix3") - 0.15, accent=WARN, size=46)
            self.badge("alert", T["turn1"], s("fix3") - 0.2, x=920, y=420)
            self.red(T["turn1"], 1.2)
            return
        self.label(hx, hy, 300, 420, "copper", T["copper"] - 0.2, T["dials"] - 0.1, accent="#F4B27A", size=40)
        v2.chip(c, 540, 1130, self.L["m42"], self.span(T["four3"] - 0.2, T["dials"] - 0.1), accent="#FDE047", size=40)
        self.chip(540, 1130, "m7", T["seven"] - 0.2, s("break4") - 0.15, accent="#FDE047", size=40)
        self.badge("check", T["wide1"] + 0.1, s("break4") - 0.15, x=920, y=420)

    # ------------------------------------------------------------------ set: bell (reveal)
    def draw_bell(self, c, t):
        T, s = self.T, self.tl.s
        c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#141834", "#1E1A30", "#120E1C"]))
        for k in range(3):                                       # arches open to the night
            ax = 180 + k * 360
            p_ = skia.Path()
            p_.moveTo(ax - 110, 1000)
            p_.lineTo(ax - 110, 420)
            p_.quadTo(ax - 110, 300, ax, 280)
            p_.quadTo(ax + 110, 300, ax + 110, 420)
            p_.lineTo(ax + 110, 1000)
            p_.close()
            c.drawPath(p_, P("#0A1238"))
        v2.stars(c, W, H, t, 0.5)
        c.drawRect(R(0, 1000, W, 260), P("#2A2230"))
        crack = prog(t, T["cracked"] - 0.2, T["first2"] + 0.3)
        hit = prog(t, T["rings"] - 0.15, T["rings"])
        ring = prog(t, T["rings"], T["rings"] + 0.2) * (1 - prog(t, s("stat") - 0.5, s("stat") - 0.15))
        great_bell(c, 540, 560, 0.95, t, crack=crack, ring=ring, hammer=hit * (1 - ring))
        person(c, 900, 1000, 290, "#2563EB", t, pose="look", face=-1)
        tk = prog(t, T["tower2"] - 0.2, T["tower2"] + 0.1) * (1 - prog(t, T["cracked"] - 0.2, T["cracked"]))
        if tk > 0:                                               # the tower crossed out
            c.save()
            c.translate(170, 1000)
            c.scale(0.5, 0.5)
            elizabeth(c, t, lit=0.5, dusk=0.6)
            c.restore()
            c.drawLine(80, 560, 260, 980, P(WARN, tk, stroke=12))
            c.drawLine(260, 560, 80, 980, P(WARN, tk, stroke=12))
        self.ui["bell"] = (540, 760)
        self.ui["crack"] = (595, 830)

    def ui_bell(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "twist", T["twist"] - 0.1, T["ben"] - 0.1, accent="#FDE68A", size=46)
        self.chip(540, 300, "bell", T["ben"] - 0.1, T["cracked"] - 0.2, accent=HILITE, size=46)
        self.chip(170, 520, "nottower", T["tower2"] - 0.2, T["cracked"] - 0.2, accent=WARN, size=36)
        cx_, cy_ = self.ui.get("crack", (595, 830))
        self.label(cx_, cy_, 760, 460, "cracked", T["cracked"] - 0.2, s("stat") - 0.2, accent=WARN, size=38)
        self.chip(540, 300, "rings", T["rings"] - 0.2, s("stat") - 0.15, accent="#FDE68A", size=44)

    # ------------------------------------------------------------------ set: tag
    def draw_tag(self, c, t):
        T = self.T
        spin = prog(t, T["t_text"], T["t_bed"] + 0.6) if self.rtl else 0.0
        bed_scene(c, t, rtl=self.rtl, spin=spin)
        pk = prog(t, T["t_still"] - 0.2, T["t_still"])
        if pk > 0:                                               # the phone
            px_, py_ = (300, 860) if not self.rtl else (470, 760)
            c.drawRRect(rr(px_ - 30, py_ - 56, 60, 112, 10), P("#111827", pk))
            c.drawRRect(rr(px_ - 24, py_ - 48, 48, 96, 6), P("#93C5FD", pk))

    def ui_tag(self, c, t, tw):
        T = self.T
        if not self.rtl:
            v2.chip(c, 360, 720, self.L["omw"], self.span(T["t_text"] - 0.1, self.duration + 1), accent=GOOD, size=50)
        else:
            v2.chip(c, 430, 640, self.L["omw"], self.span(T["t_text"] - 0.1, self.duration + 1), accent=GOOD, size=44)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#24215C", "#6A3A78", "#D0705E"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.1, sfx.tick(), -10), (T["pennies"] + 0.3, sfx.clank(1800.0, 0.3, 61), -8), (T["pennies"] + 0.35, sfx.tap(62), -6),
              (T["famous"] - 0.15, sfx.whoosh(0.5, False, 63), -6), (T["congrats"] - 0.05, sfx.whoosh(0.5, True, 64), -10),
              (T["congrats"] + 0.1, sfx.sparkle(0.9, 12, 65), -8), (T["bigben"], sfx.bell(330.0, 2.0, 0.7), -10)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 66), -4), (T["struck"], sfx.bell(330.0, 1.6, 0.6), -8),
               (T["second"], sfx.tick(), -6), (T["day"], sfx.beep(1200.0, 0.12), -12), (T["day1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix1") - 0.12, sfx.whoosh(0.4, False, 67), -4)]
        k = 0
        tt = s("fix1") + 0.3
        while tt < s("break2") - 0.2:
            ev.append((tt, sfx.tick(), -6 if k % 2 == 0 else -9))
            tt += 2.0
            k += 1
        ev += [(T["two1"], sfx.ding(), -8), (T["two1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, True, 68), -4), (T["gust"], sfx.whoosh(0.8, False, 69), -6),
               (T["gears"], sfx.whirr(1.0, 200.0, 140.0, 70), -14), (T["pend21"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix2") - 0.12, sfx.whoosh(0.4, False, 71), -4), (T["gravity"], sfx.clank(900.0, 0.3, 72), -10),
               (T["same"], sfx.tick(), -6), (T["swing"], sfx.tick(), -6), (T["what1"], sfx.ding(), -8),
               (T["what1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break3") - 0.12, sfx.whoosh(0.4, True, 73), -4), (T["iron"], sfx.clank(240.0, 0.6, 74), -8),
               (T["heavy"], sfx.creak(1.2, 75), -8), (T["turn1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.4, False, 76), -4), (T["copper"], sfx.whoosh(1.2, True, 77), -14),
               (T["seven"], sfx.pop(78), -8), (T["wide1"], sfx.ding(), -8), (T["wide1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.4, True, 79), -4), (T["heat"], sfx.sizzle(0.5, 80), -12),
               (T["cold"], sfx.hiss(0.4, 81), -14), (T["drift1"], sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.4, False, 82), -4)]
        for kk, tk in enumerate((T["add"], T["pennies4"] + 0.2, T["each"])):
            ev.append((tk + 0.2, sfx.clank(1800.0 + kk * 120, 0.25, 83 + kk), -8))
        ev += [(T["day41"], sfx.ding(), -8), (T["day41"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(90), 0), (T["follow"] - 0.15, sfx.pop(91), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 92), -6), (T["cracked"], sfx.snap(93), -6),
               (T["rings"], sfx.bell(330.0, 2.6, 0.9), -6), (T["rings"] + 0.02, sfx.bell(347.0, 2.4, 0.4), -12)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 94), -6), (T["s1"], sfx.pop(95), -3), (T["s2"], sfx.pop(96), -3),
               (T["s3"], sfx.pop(97), -3)]
        ev += [(T["cong2"], sfx.pop(98), -2), (T["cong2"], sfx.sparkle(1.4, 18, 99), -4), (e("closer") - 0.6, sfx.bell(330.0, 1.8, 0.6), -10)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 100), -6), (T["t_text"], sfx.pop(101), -6)]
        if self.rtl:
            ev += [(T["t_text"] + 0.2, sfx.whirr(1.4, 300.0, 700.0, 102), -14)]
        return ev


NAME = "bigben"
EPISODE = BigBen
