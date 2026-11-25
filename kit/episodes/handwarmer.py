"""Episode 96 - a hand warmer.  v2 look: a clear pouch of liquid with a little metal disc, held in two mittens on a
snowy night (world: the pouch centred at (0, 0), 600 x 380 units; the disc at (-100, -50)).

Sets: pouch (hook: close on the disc, a fingertip clicks it, a front of white crystals races through the pouch and it
glows; break1: bare frozen hands in the snow, a pocket with a campfire crossed out; fix1: the pouch fills with salty
liquid while a bag of chips pours its salt; break2: the thermometer drops and it stays liquid, a lens shows molecules
wandering; fix2: the click again, a seed crystal and molecules snapping on, a row of dominoes; break3: solid white and
cooling, a knock; reveal: molecules locking into the crystal throw off sparks of heat; stat; closer: the glowing pouch
in mittens), stove (fix3: boiled in a pot, the crystals melt back from the edges), slope (break4: a ski slope, a clock
running an hour while a small pouch goes cold), packet (fix4: a throwaway warmer, its wrapper tears, air streams in,
iron grains rust and glow), bench (tag: forgotten in a back pocket, sit down, click: a heated seat).
"""
from v2_base import *  # noqa: F401,F403
from bigben import thermometer  # noqa: E402
from ondol import clock  # noqa: E402

PW, PH = 600.0, 380.0                     # the pouch (world units)
DISC = (-100.0, -50.0)
DISC_R = 46.0
LIQ = ("#8FD3FF", "#4C9BE0")
CRY = ("#F6F1E7", "#E2D6C2")
WARMC = "#FF9F43"
NIGHT = ["#050B1E", "#0C1840", "#18295A"]
MITTEN = ("#C81E3A", "#9F1239")
SKIN = "#E3A982"


def snow(c, t, n=80, a=1.0, seed=5, speed=1.0):
    """Falling snow in screen space."""
    if a <= 0:
        return
    rng = random.Random(seed)
    for k in range(n):
        sp = rng.uniform(0.05, 0.11) * speed
        u = (t * sp + rng.random()) % 1.0
        x = rng.uniform(-60, W + 60) + math.sin(t * 1.1 + k) * 22
        y = lerp(-40, H + 40, u)
        c.drawCircle(x, y, rng.uniform(2.0, 5.5), P("#F1F5F9", rng.uniform(0.35, 0.85) * a))


def night_bg(c, t, a_snow=1.0, speed=1.0):
    vrect(c, 0, 0, W, H, NIGHT)
    rng = random.Random(2)
    for k in range(40):                                                   # a few stars up high
        c.drawCircle(rng.uniform(0, W), rng.uniform(0, 620), rng.uniform(1, 2.4), P("#E0E7FF", 0.35 + 0.3 * math.sin(t + k)))
    path = skia.Path()                                                    # snowy hills far behind
    path.moveTo(0, 1180)
    for x in range(0, W + 60, 60):
        path.lineTo(x, 1150 - 60 * math.sin(x * 0.006 + 1.2) - 30 * math.sin(x * 0.017))
    path.lineTo(W, H)
    path.lineTo(0, H)
    path.close()
    c.drawPath(path, lin_paint(0, 1080, 0, H, ["#2B3E73", "#16234A"]))
    snow(c, t, 70, a_snow, 5, speed)


def crystals(c, t, heat=0.0, a=1.0, w=PW, h=PH):
    """The solid inside of a used pouch: white needles packed together (world, centred at 0, 0)."""
    c.drawRect(R(-w / 2, -h / 2, w, h), lin_paint(0, -h / 2, 0, h / 2, [mix(CRY[0], "#FFE3BF", 0.55 * heat),
                                                                       mix(CRY[1], "#FFC98A", 0.55 * heat)], a=0.97 * a))
    rng = random.Random(17)
    lite = mix("#FFFFFF", "#FFF3E0", heat)
    dark = mix("#B9A88E", "#E39A55", heat)
    for k in range(190):
        x, y = rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2)
        ang = rng.uniform(0, math.pi)
        ln = rng.uniform(16, 44)
        dx, dy = math.cos(ang) * ln / 2, math.sin(ang) * ln / 2
        c.drawLine(x - dx + 2, y - dy + 2, x + dx + 2, y + dy + 2, P(dark, 0.45 * a, stroke=2))
        c.drawLine(x - dx, y - dy, x + dx, y + dy, P(lite, 0.95 * a, stroke=3))


def disc(c, x, y, r, press=0.0, flash=0.0, a=1.0):
    """The little steel disc that starts it all (world)."""
    if a <= 0:
        return
    c.drawCircle(x + 4, y + 6, r, P("#0B1220", 0.35 * a))
    c.drawCircle(x, y, r, rad_paint(x - r * 0.35, y - r * 0.35, r * 1.5, [("#F8FAFC", a), ("#A7B4C6", a), ("#4B5A70", a)],
                                    [0.0, 0.55, 1.0]))
    c.drawCircle(x, y, r * 0.7, P("#334155", 0.55 * a, stroke=3))
    for i in range(10):                                                   # the slits that let it flex
        an = i * math.pi / 5
        c.drawLine(x + math.cos(an) * r * 0.74, y + math.sin(an) * r * 0.74, x + math.cos(an) * r * 0.9,
                   y + math.sin(an) * r * 0.9, P("#3B475A", 0.85 * a, stroke=3))
    k = clamp(press)
    c.drawCircle(x, y, r * 0.34, P(mix("#E2E8F0", "#64748B", k), a))
    c.drawCircle(x - r * 0.08, y - r * 0.08, r * 0.16, P("#FFFFFF", (0.8 - 0.6 * k) * a))
    if flash > 0:
        add_glow(c, x, y, r * 3.0, "#FFFFFF", 0.8 * flash * a)


def pouch(c, t, fill=1.0, cryst=0.0, heat=0.0, press=0.0, flash=0.0, melt=0.0, cold=0.0, a=1.0):
    """The reusable warmer (world, centred at 0, 0). fill 0..1 liquid level; cryst 0..1 how far the crystal front has run
    from the disc (1 = all of it); heat 0..1 warm glow; press 0..1 the disc pushed in; melt 0..1 the crystals melting back
    from the edges (boiled); cold 0..1 a cold blue tint."""
    if a <= 0:
        return
    x0, y0 = -PW / 2, -PH / 2
    body = rr(x0, y0, PW, PH, 120)
    if heat > 0:
        add_glow(c, 0, 0, 560, WARMC, 0.6 * heat * a)
    c.drawRRect(body, P(mix("#DCEBFA", "#9DB7E8", cold), 0.16 * a))
    c.save()
    c.clipRRect(body, skia.ClipOp.kIntersect, True)
    if fill > 0:
        ly = lerp(PH / 2, -PH / 2 + 26, clamp(fill))
        c.drawRect(R(x0, ly, PW, PH / 2 - ly + 2), lin_paint(0, ly, 0, PH / 2, [mix(LIQ[0], "#6C8FD8", cold), mix(LIQ[1], "#2E4C9A", cold)],
                                                             a=0.62 * a))
        if fill < 1:
            path = skia.Path()
            path.moveTo(x0, ly)
            for xx in range(int(x0), int(-x0) + 12, 12):
                path.lineTo(xx, ly + math.sin(xx * 0.05 + t * 6) * 4)
            c.drawPath(path, P("#E0F2FE", 0.8 * a, stroke=3))
        rng = random.Random(4)                                            # a few tiny bubbles in the liquid
        for k in range(9):
            bx, by = rng.uniform(x0 + 40, -x0 - 40), rng.uniform(ly + 20, PH / 2 - 20)
            c.drawCircle(bx, by + math.sin(t * 1.5 + k) * 4, rng.uniform(4, 8), P("#E0F2FE", 0.35 * a, stroke=2))
    if cryst > 0:
        rc = 880 * clamp(cryst)
        c.save()
        cp = skia.Path()
        cp.addCircle(DISC[0], DISC[1], max(1.0, rc))
        c.clipPath(cp, skia.ClipOp.kIntersect, True)
        if melt > 0:                                                      # the last of the crystals, a shrinking core
            ins = lerp(0, 175, clamp(melt))
            c.clipRRect(rr(x0 + ins, y0 + ins * 0.62, PW - 2 * ins, PH - 2 * ins * 0.62, max(14.0, 120 - ins * 0.6)),
                        skia.ClipOp.kIntersect, True)
        crystals(c, t, heat, a)
        c.restore()
        if cryst < 1:                                                     # the racing front
            c.drawCircle(DISC[0], DISC[1], rc, P("#FFFFFF", 0.9 * a, stroke=7))
            c.drawCircle(DISC[0], DISC[1], rc + 10, P("#BFE7FF", 0.45 * a, stroke=4))
    c.restore()
    c.drawRRect(body, P(mix("#E0F2FE", "#A5B4FC", cold), 0.95 * a, stroke=6))
    c.drawRRect(rr(x0 + 16, y0 + 16, PW - 32, PH - 32, 104), P("#F8FAFC", 0.3 * a, stroke=2))      # the welded seam
    c.drawLine(x0 + 110, y0 + 46, x0 + 290, y0 + 34, P("#FFFFFF", 0.55 * a, stroke=9))             # shine
    c.drawLine(x0 + 70, y0 + 80, x0 + 110, y0 + 64, P("#FFFFFF", 0.4 * a, stroke=7))
    disc(c, DISC[0], DISC[1], DISC_R, press, flash, a)


def mitten(c, x, y, side=1, s=1.0, bare=0.0, cold=0.0, shake=0.0, t=0.0, front=False, a=1.0):
    """A hand under a corner of the pouch at (x, y) (world): side -1 left, 1 right. bare 0..1 swaps the mitten for a
    cold bare hand; front=True draws only the thumb and fingertips that lie over the pouch."""
    if a <= 0:
        return
    c.save()
    c.translate(x + math.sin(t * 47 + side) * 5 * shake, y + math.cos(t * 41) * 3 * shake)
    c.scale(side * s, s)
    skin = mix(SKIN, "#9FB4E6", cold)
    col = mix(MITTEN[0], skin, bare)
    dk = mix(MITTEN[1], shade(skin, -0.15), bare)
    if not front:
        c.drawRRect(rr(40, 40, 170, 330, 70), lin_paint(40, 0, 210, 0, ["#334155", "#1E293B"], a=a))         # sleeve
        c.drawRRect(rr(20, 20, 210, 90, 40), P("#E2E8F0", 0.9 * a * (1 - bare)))                           # cuff
        c.drawOval(R(-70, -70, 260, 200), lin_paint(-70, 0, 190, 0, [col, dk], a=a))                       # palm under the corner
    else:
        if bare > 0.5:                                                    # four bare fingers curled over the edge
            for k in range(4):
                c.drawRRect(rr(-60 + k * 38, -96 + abs(k - 1.5) * 8, 34, 70, 17), P(skin, a))
                c.drawRRect(rr(-55 + k * 38, -92 + abs(k - 1.5) * 8, 24, 18, 8), P(shade(skin, 0.18), 0.8 * a))
        else:
            c.drawRRect(rr(-80, -110, 170, 90, 45), lin_paint(-80, 0, 90, 0, [col, dk], a=a))               # mitten top
            for k in range(5):                                            # knit lines
                c.drawLine(-60 + k * 30, -100, -60 + k * 30, -30, P(dk, 0.5 * a, stroke=3))
        c.drawRRect(rr(60, -150, 54, 120, 27), lin_paint(60, 0, 114, 0, [col, dk], a=a))                   # thumb
    c.restore()


def fingertip(c, x, y, s=1.0, press=0.0, a=1.0):
    """An index finger coming down from the upper right, its tip at (x, y) (world)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y + 10 * press)
    c.rotate(28)
    c.scale(s, s)
    c.drawRRect(rr(-26, -230, 52, 238, 26), lin_paint(-26, 0, 26, 0, [SKIN, shade(SKIN, -0.12)], a=a))
    c.drawRRect(rr(-17, -52, 34, 40, 14), P("#F6D5C0", a))                                                   # nail
    c.drawRRect(rr(-70, -420, 150, 210, 60), lin_paint(-70, 0, 80, 0, [SKIN, shade(SKIN, -0.14)], a=a))     # knuckles
    c.drawRRect(rr(-80, -700, 170, 300, 60), lin_paint(-80, 0, 90, 0, ["#334155", "#1E293B"], a=a))         # sleeve
    c.restore()


def fist(c, x, y, s=1.0, a=1.0):
    """A fist seen from the side, knuckles down at (x, y) (world): it knocks on the solid pouch."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-30, -330, 120, 230, 50), lin_paint(-30, 0, 90, 0, ["#334155", "#1E293B"], a=a))          # sleeve
    c.drawRRect(rr(-70, -130, 150, 120, 46), lin_paint(-70, 0, 80, 0, [SKIN, shade(SKIN, -0.14)], a=a))    # back of the hand
    for k in range(4):                                                                                     # curled fingers
        c.drawRRect(rr(-66 + k * 36, -40, 34, 58, 16), P(shade(SKIN, -0.04 * k), a))
        c.drawLine(-60 + k * 36, -6, -40 + k * 36, -6, P(shade(SKIN, -0.25), 0.7 * a, stroke=3))
    c.drawRRect(rr(56, -110, 44, 90, 22), P(shade(SKIN, 0.05), a))                                         # thumb
    c.restore()


def lens(c, x, y, r, t, mode="wander", k=0.0, a=1.0, heat=0.0):
    """A round close-up of the liquid (screen). mode "wander": molecules drift about; "lock": a crystal grows from the
    centre, k 0..1 of the way out, every molecule inside it snapped onto the grid; heat > 0 adds sparks of heat leaving
    the ones that just locked."""
    if a <= 0:
        return
    c.save()
    pth = skia.Path()
    pth.addCircle(x, y, r)
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    c.drawRect(R(x - r, y - r, 2 * r, 2 * r), lin_paint(0, y - r, 0, y + r, ["#0E2A55", "#091A38"], a=0.96 * a))
    sp = 44.0
    rng = random.Random(21)
    front = k * r * 1.15
    rows = int(2 * r / (sp * 0.866)) + 2
    for j in range(-rows // 2, rows // 2 + 1):
        for i in range(-int(r / sp) - 1, int(r / sp) + 2):
            gx = x + i * sp + (sp / 2 if j % 2 else 0)
            gy = y + j * sp * 0.866
            d = math.hypot(gx - x, gy - y)
            if d > r + 20:
                continue
            ph = rng.random() * 6.28
            wx = gx + math.sin(t * 1.7 + ph) * 16 + math.sin(t * 0.9 + ph * 2) * 10
            wy = gy + math.cos(t * 1.3 + ph) * 16
            locked = mode == "lock" and d < front
            u = clamp((front - d) / 40.0) if mode == "lock" else 0.0
            px, py = (lerp(wx, gx, e_out(u)), lerp(wy, gy, e_out(u))) if locked else (wx, wy)
            ang = lerp(ph, 0.5, u) if locked else ph + t * 0.8
            col = mix("#7DD3FC", "#F8FAFC", u)
            dx, dy = math.cos(ang) * 9, math.sin(ang) * 9
            c.drawLine(px - dx, py - dy, px + dx, py + dy, P(col, 0.9 * a, stroke=6))
            c.drawCircle(px - dx, py - dy, 8, P(col, a))
            c.drawCircle(px + dx, py + dy, 6, P(mix("#38BDF8", "#E2E8F0", u), a))
            if locked and heat > 0 and 0.0 < front - d < 70:              # just locked: heat flies off
                q = (front - d) / 70.0
                for m in range(3):
                    an = ph + m * 2.1
                    c.drawCircle(px + math.cos(an) * 46 * q, py + math.sin(an) * 46 * q, 5 * (1 - q) + 1,
                                 P(WARMC, (1 - q) * heat * a))
    if mode == "lock" and k > 0:                                          # the grid lines of the crystal
        c.drawCircle(x, y, front, P("#FFFFFF", 0.5 * a, stroke=3))
        if heat > 0:
            add_glow(c, x, y, front + 40, WARMC, 0.25 * heat * a)
    c.restore()
    c.drawCircle(x, y, r, P("#E2E8F0", a, stroke=12))
    c.drawLine(x + r * 0.72, y + r * 0.72, x + r * 1.12, y + r * 1.12, P("#E2E8F0", a, stroke=22))


def dominoes(c, x0, x1, y, t, t0, step=0.11, a=1.0):
    """A row of dominoes knocked over one after another from the left (screen)."""
    if a <= 0:
        return
    n = 9
    for i in range(n):
        x = lerp(x0, x1, i / (n - 1))
        f = e_in(prog(t, t0 + i * step, t0 + i * step + 0.2))
        c.save()
        c.translate(x + 22, y)
        c.rotate(72 * f)
        c.drawRRect(rr(-44, -120, 44, 120, 8), P("#F8FAFC", a))
        c.drawRRect(rr(-44, -120, 44, 120, 8), P("#0F172A", a, stroke=3))
        c.drawLine(-40, -60, -4, -60, P("#0F172A", a, stroke=3))
        for (dx, dy) in ((-22, -92), (-22, -30), (-32, -40), (-12, -20)):
            c.drawCircle(dx, dy, 5, P("#0F172A", a))
        c.restore()


def chips_bag(c, x, y, s, t, pour=0.0, a=1.0):
    """A plain bag of chips (no brand) tipping over and pouring white salt (screen)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(-40 * pour)
    c.scale(s, s)
    c.drawRRect(rr(-80, -120, 160, 240, 26), lin_paint(-80, 0, 80, 0, ["#16A34A", "#22C55E", "#15803D"], a=a))
    for yy in (-120, 120):                                                # crimped ends
        for k in range(8):
            c.drawLine(-76 + k * 21, yy - 8, -66 + k * 21, yy + 8, P("#14532D", 0.8 * a, stroke=3))
    c.drawOval(R(-52, -40, 104, 80), P("#FDE68A", a))                     # a chip on the front
    c.drawOval(R(-52, -40, 104, 80), P("#CA8A04", a, stroke=3))
    c.restore()
    if pour > 0.3:
        rng = random.Random(8)
        for k in range(40):
            u = (t * 1.6 + rng.random()) % 1.0
            gx = x + 60 * s + rng.uniform(-14, 14) * s + u * 40 * s
            gy = y - 60 * s + u * 260 * s
            c.drawRect(R(gx, gy, 6 * s, 6 * s), P("#FFFFFF", 0.9 * a * (1 - u * 0.5)))


def pocket_fire(c, x, y, s, t, cross=0.0, a=1.0):
    """A jeans pocket with a little campfire over it, crossed out (screen)."""
    if a <= 0:
        return
    c.drawRect(R(x - 190 * s, y - 60 * s, 380 * s, 300 * s), lin_paint(0, y - 60 * s, 0, y + 240 * s, ["#3B6EA8", "#1E3F6E"], a=a))   # jeans
    pk = skia.Path()                                                      # the back pocket
    pk.moveTo(x - 120 * s, y - 30 * s)
    pk.lineTo(x + 120 * s, y - 30 * s)
    pk.lineTo(x + 110 * s, y + 130 * s)
    pk.lineTo(x, y + 180 * s)
    pk.lineTo(x - 110 * s, y + 130 * s)
    pk.close()
    c.drawPath(pk, lin_paint(0, y - 30 * s, 0, y + 180 * s, ["#4A82C0", "#2C5A94"], a=a))
    c.drawPath(pk, P("#F59E0B", 0.85 * a, stroke=4 * s))                  # stitching
    for dx in (-112, 112):                                                # rivets
        c.drawCircle(x + dx * s, y - 26 * s, 8 * s, P("#D4A64A", a))
    for k in range(3):                                                    # a little campfire in the pocket
        c.drawRRect(rr(x - 62 * s + k * 14 * s, y + 70 * s - k * 10 * s, 110 * s, 18 * s, 9 * s), P("#7C4A2D", a))
    v2.flame(c, x, y + 66 * s, 70 * s, 150 * s, t, 1.0, seed=3, ang=-90)
    if cross > 0:
        k = e_out(clamp(cross))
        c.drawLine(x - 150 * s, y - 110 * s, lerp(x - 150 * s, x + 150 * s, k), lerp(y - 110 * s, y + 210 * s, k), P(WARN, a, stroke=18 * s))
        c.drawLine(x + 150 * s, y - 110 * s, lerp(x + 150 * s, x - 150 * s, k), lerp(y - 110 * s, y + 210 * s, k), P(WARN, a, stroke=18 * s))


def packet(c, x, y, s, t, open_k=0.0, rust=0.0, air=0.0, xray=0.0, a=1.0):
    """A throwaway warmer (screen, centred at x, y): a cloth pouch of iron powder in a shiny airtight wrapper. open_k
    0..1 the wrapper torn off, air 0..1 air streaming in, xray 0..1 a cut-away window on the powder, rust 0..1 grains
    turned orange-brown (and warm)."""
    if a <= 0:
        return
    w, h = 520 * s, 330 * s
    if rust > 0:
        add_glow(c, x, y, 520 * s, WARMC, 0.55 * rust * a)
    c.drawRRect(rr(x - w / 2, y - h / 2, w, h, 26 * s), lin_paint(0, y - h / 2, 0, y + h / 2, ["#EDE6D8", "#CFC4AE"], a=a))
    rng = random.Random(6)
    for k in range(120):                                                  # the cloth's tiny holes
        c.drawCircle(x + rng.uniform(-w / 2 + 14, w / 2 - 14), y + rng.uniform(-h / 2 + 14, h / 2 - 14), 2.2 * s, P("#9C8F78", 0.8 * a))
    c.drawRRect(rr(x - w / 2 + 10 * s, y - h / 2 + 10 * s, w - 20 * s, h - 20 * s, 20 * s), P("#B6A98F", 0.8 * a, stroke=3 * s))
    if xray > 0:
        win = rr(x - w * 0.38, y - h * 0.3, w * 0.76, h * 0.6, 24 * s)
        c.save()
        c.clipRRect(win, skia.ClipOp.kIntersect, True)
        c.drawRRect(win, P("#1C1917", xray * a))
        rng = random.Random(11)
        for k in range(260):
            gx = x + rng.uniform(-w * 0.38, w * 0.38)
            gy = y + rng.uniform(-h * 0.3, h * 0.3)
            r_ = rng.uniform(4, 9) * s
            kind = rng.random()
            if kind < 0.62:                                               # iron powder, rusting
                rk = clamp(rust * 1.4 - rng.random() * 0.4)
                c.drawCircle(gx, gy, r_, P(mix("#6B7280", "#C2410C", rk), xray * a))
                if rk > 0.6:
                    c.drawCircle(gx, gy, r_ * 1.8, P("#FB923C", 0.25 * rk * xray * a))
            elif kind < 0.78:                                             # salt
                c.drawRect(R(gx, gy, r_ * 1.2, r_ * 1.2), P("#F8FAFC", xray * a))
            elif kind < 0.9:                                              # charcoal
                c.drawCircle(gx, gy, r_ * 0.9, P("#0A0A0A", xray * a))
            else:                                                         # vermiculite, holding the water
                c.drawOval(R(gx - r_ * 1.4, gy - r_ * 0.6, r_ * 2.8, r_ * 1.2), P("#D4A64A", xray * a))
        c.restore()
        c.drawRRect(win, P("#E2E8F0", xray * a, stroke=6 * s))
    if air > 0:                                                           # air streaming in through the cloth
        rng = random.Random(14)
        for k in range(26):
            u = (t * 0.7 + rng.random()) % 1.0
            sx = x + rng.choice((-1, 1)) * lerp(w * 0.95, w * 0.42, u)
            sy = y + rng.uniform(-h * 0.45, h * 0.45)
            c.drawCircle(sx, sy, 9 * s, P("#7DD3FC", 0.8 * air * a * (1 - u * 0.4)))
            c.drawCircle(sx + 14 * s, sy, 9 * s, P("#BAE6FD", 0.8 * air * a * (1 - u * 0.4)))
    if open_k < 1:                                                        # the airtight wrapper
        k = e_in(clamp(open_k))
        ww, hh = w * 1.16, h * 1.22
        off = k * 900
        c.save()
        c.translate(0, off)
        c.drawRRect(rr(x - ww / 2, y - hh / 2, ww, hh, 18 * s), lin_paint(x - ww / 2, 0, x + ww / 2, 0,
                    ["#94A3B8", "#E2E8F0", "#64748B", "#CBD5E1", "#475569"], a=0.97 * a * (1 - k)))
        for yy in (y - hh / 2, y + hh / 2):                               # crimped ends
            for i in range(16):
                c.drawLine(x - ww / 2 + 10 + i * ww / 16, yy - 10, x - ww / 2 + 22 + i * ww / 16, yy + 10, P("#334155", 0.7 * a * (1 - k), stroke=3))
        c.drawLine(x - ww * 0.35, y - hh * 0.25, x + ww * 0.05, y - hh * 0.32, P("#FFFFFF", 0.6 * a * (1 - k), stroke=10))
        c.restore()


def pot_scene(c, t, boil=1.0, melt=0.0, steam=1.0):
    """The pouch boiling in a pot on a gas ring (screen)."""
    vrect(c, 0, 0, W, H, ["#1F2937", "#111827"])
    c.drawRect(R(0, 1180, W, 120), lin_paint(0, 1180, 0, 1300, ["#4B5563", "#374151"]))                 # the counter
    for i, fx_ in enumerate((-120, -40, 40, 120)):                                                      # the gas ring
        v2.flame(c, 540 + fx_, 1170, 40, 70 * boil, t + i * 0.3, boil, seed=i + 2, ang=-90)
    add_glow(c, 540, 1150, 300, "#60A5FA", 0.35 * boil)
    x0, x1, top, bot = 170, 910, 640, 1150
    c.drawRRect(rr(x0, top, x1 - x0, bot - top, 40), lin_paint(x0, 0, x1, 0, ["#475569", "#94A3B8", "#64748B", "#334155"]))   # back wall
    c.drawRRect(rr(x0 + 20, top + 30, x1 - x0 - 40, bot - top - 50, 30), P("#0F172A"))
    water_top = top + 120
    c.drawRect(R(x0 + 20, water_top, x1 - x0 - 40, bot - water_top - 20), lin_paint(0, water_top, 0, bot, ["#3B82F6", "#1E3A8A"], a=0.9))
    c.save()
    c.translate(540, 900)
    c.rotate(-6)
    c.scale(0.95, 0.95)
    pouch(c, t, fill=1.0, cryst=1.0, heat=0.2, melt=melt)
    c.restore()
    rng = random.Random(3)
    for i in range(36):                                                   # the boil
        u = (t * rng.uniform(0.8, 1.3) + rng.random()) % 1.0
        bx = rng.uniform(x0 + 50, x1 - 50) + math.sin(t * 5 + i) * 5
        c.drawCircle(bx, lerp(bot - 40, water_top + 6, u), lerp(4, 12, u), P("#DBEAFE", 0.75 * boil, stroke=3))
    c.drawRect(R(x0 + 20, water_top, x1 - x0 - 40, bot - water_top - 20), P("#60A5FA", 0.12))          # the water in front
    path = skia.Path()
    path.moveTo(x0 + 20, water_top)
    for xx in range(x0 + 20, x1 - 10, 14):
        path.lineTo(xx, water_top + math.sin(xx * 0.06 + t * 9) * 5 * boil)
    c.drawPath(path, P("#BFDBFE", 0.8, stroke=4))
    c.drawRRect(rr(x0 - 20, top - 20, x1 - x0 + 40, 40, 20), lin_paint(x0, 0, x1, 0, ["#64748B", "#E2E8F0", "#94A3B8"]))     # the rim
    for sd in (-1, 1):                                                    # handles
        c.drawRRect(rr(540 + sd * 400 - 40, top + 30, 80, 30, 15), P("#1F2937"))
    if steam > 0:
        for i in range(7):
            rng = random.Random(30 + i)
            u = (t * 0.35 + rng.random()) % 1.0
            puff(c, rng.uniform(280, 800) + math.sin(t + i) * 20, lerp(620, 340, u), lerp(40, 90, u), "#E2E8F0", 0.35 * (1 - u) * steam)


def slope_scene(c, t, hours=0.0, fade_k=0.0):
    """A ski slope by day; a clock runs an hour while a small pouch goes cold (screen)."""
    vrect(c, 0, 0, W, H, ["#5B8DEF", "#9CC3F5", "#DCEBFA"])
    c.drawCircle(860, 330, 70, P("#FEF9C3"))
    add_glow(c, 860, 330, 260, "#FEF08A", 0.5)
    for k, (x, hgt) in enumerate(((120, 300), (230, 240), (950, 280), (860, 220))):                     # pines
        tri = skia.Path()
        tri.moveTo(x, 900 - hgt)
        tri.lineTo(x - 70, 900)
        tri.lineTo(x + 70, 900)
        tri.close()
        c.drawPath(tri, P("#14532D"))
        c.drawRect(R(x - 10, 900, 20, 40), P("#3F2A1D"))
    path = skia.Path()
    path.moveTo(0, 760)
    path.lineTo(W, 1060)
    path.lineTo(W, H)
    path.lineTo(0, H)
    path.close()
    c.drawPath(path, lin_paint(0, 760, 0, H, ["#FFFFFF", "#C7D7EE", "#5B6F94"], [0.0, 0.35, 1.0]))
    u = (t * 0.12) % 1.0                                                  # a skier going down
    sx, sy = lerp(180, 900, u), lerp(800, 1030, u)
    c.save()
    c.translate(sx, sy)
    c.rotate(16)
    c.drawLine(-70, 0, 70, 0, P("#DC2626", 1.0, stroke=8))
    c.drawLine(-70, 14, 70, 14, P("#DC2626", 1.0, stroke=8))
    person(c, 0, 0, 120, "#2563EB", t, pose="duck", face=1, hat="beanie")
    c.restore()
    clock(c, 850, 620, 95, 9.0 + hours, a=1.0)
    v2.glass(c, 70, 470, 420, 300, r=36, a=1.0, tint="#0B1226")              # the pouch, going cold, on a dark card
    c.save()
    c.translate(280, 620)
    c.scale(0.55, 0.55)
    pouch(c, t, fill=1.0, cryst=1.0, heat=0.9 * (1 - fade_k), cold=fade_k * 0.6)
    c.restore()


def bench_scene(c, t, sit=0.0, click=0.0, jump=0.0):
    """A park bench by day: someone sits on a warmer forgotten in a back pocket (screen)."""
    vrect(c, 0, 0, W, H, ["#60A5FA", "#BFDBFE"])
    c.drawRect(R(0, 1060, W, H - 1060), lin_paint(0, 1060, 0, H, ["#4ADE80", "#16A34A"]))
    for x in (150, 930):                                                  # trees
        c.drawRect(R(x - 14, 820, 28, 240), P("#7C4A2D"))
        c.drawCircle(x, 780, 110, P("#22C55E"))
        c.drawCircle(x - 60, 820, 80, P("#16A34A"))
    c.drawRRect(rr(260, 940, 560, 34, 10), P("#B45309"))                  # the bench
    c.drawRRect(rr(260, 870, 560, 30, 10), P("#C2410C"))
    for x in (300, 780):
        c.drawRect(R(x - 10, 974, 20, 100), P("#374151"))
    px = lerp(900, 560, e_io(clamp(sit * 2)))
    py = 1060 if sit < 0.5 else 960 - 140 * e_out(clamp(jump))
    pose = "walk" if sit < 0.5 else ("cheer" if jump > 0 else "sit")
    if click > 0:
        add_glow(c, 560, 940, 220, WARMC, 0.85 * click)
    person(c, px, py, 230, "#7C3AED", t, pose=pose, face=-1)
    if jump > 0.2:                                                        # "!" marks
        for k, dx in enumerate((-90, 0, 90)):
            text(c, "!", 560 + dx, 560 - 30 * (k % 2), 90, WARN, "Poppins-Black", a=clamp(jump * 2))


# ====================================================================================== the episode
class HandWarmer(EpisodeV2):
    BUILD_NO = 96
    FIRST_SET = "pouch"
    CLEAR = "#050B1E"
    TITLE = {"en": "HAND WARMER", "ar_sa": "دفاية يد"}
    EMPH = {"en": ["CLICK", "DISC", "COLD", "HOT", "CRYSTALS", "FROZEN", "FIRE", "POCKET", "HEAT", "HIDING", "SALTY",
                   "SALT", "VINEGAR", "CHIPS", "COOLS", "LIQUID", "PUSH", "CRYSTAL", "DOMINOES", "HARD", "BRICK", "DONE",
                   "BOIL", "MELT", "HOUR", "SKI", "LONGER", "THROWAWAY", "RUSTS", "IRON", "WARM", "HOURS", "FOLLOW",
                   "MUSEUM", "FREEZING", "SOLID", "BOILED", "ONE", "FIFTY", "FOUR", "DEGREES", "TEN", "CONGRATS",
                   "WARMER", "YOURSELF", "HEATED", "SEATS"],
            "ar_sa": ["تطق", "القرص", "البارد", "كريستال", "حار", "متجمدة", "النار", "جيبك", "الحرارة", "مالح", "شيبس",
                      "يبرد", "سائل", "يدزه", "الدومينو", "حجر", "خلاص", "فتغليه", "يذوب", "ساعة", "الكشتة", "الحديد",
                      "تصدّي", "دفا", "متابعة", "متحف", "يتجمد", "صلب", "ضغطة", "وخمسين", "عشر", "مبروك", "دفاية",
                      "مدفّى"]}
    KEYS = {"ar_sa": {
        ("hook", "CLICK"): "تطق", ("hook", "DISC"): "هالقرص", ("hook", "COLD"): "البارد", ("hook", "CRYSTALS"): "كريستال",
        ("hook", "HOT"): "حار",
        ("break1", "FROZEN"): "متجمدة", ("break1", "FIRE"): "النار", ("break1", "POCKET"): "جيبك",
        ("break1", "HEAT"): "الحرارة",
        ("fix1", "FILL"): "فتعبي", ("fix1", "SALTY"): "مالح", ("fix1", "CHIPS"): "شيبس",
        ("break2", "COOLS"): "يبرد", ("break2", "STAYS"): "ويظل", ("break2", "PUSH"): "يدزه",
        ("fix2", "CLICK"): "فتطق", ("fix2", "CRYSTAL"): "كريستال", ("fix2", "DOMINOES"): "الدومينو",
        ("break3", "HARD"): "حجر", ("break3", "DONE"): "خلاص",
        ("fix3", "BOIL"): "فتغليه", ("fix3", "MELT"): "يذوب",
        ("break4", "HOUR"): "ساعة", ("break4", "SKI"): "الكشتة", ("break4", "LONGER"): "أطول",
        ("fix4", "THROWAWAY"): "ينرمى", ("fix4", "IRON"): "الحديد", ("fix4", "RUSTS"): "تصدّي", ("fix4", "WARM"): "دفا",
        ("cta", "FOLLOW"): "متابعة",
        ("reveal", "FREEZING"): "يتجمد", ("reveal", "SOLID"): "صلب", ("reveal", "BOILED"): "تغليه",
        ("stat", "ONE"): "ضغطة", ("stat", "FIFTY"): "أربعة", ("stat", "TEN"): "عشر",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "POCKET"): "جيبك", ("tag", "SIT"): "وتجلس", ("tag", "CLICK"): "تك", ("tag", "HEATED"): "مدفّى"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Museum of the Future"),
                   "stat": [("1", "CLICK"), ("54°C", "IN SECONDS"), ("10 H", "THROWAWAY KIND")],
                   "L": {"name": "A HAND WARMER", "click": "CLICK!", "frozen": "FROZEN FINGERS", "where": "WHERE'S THE HEAT?",
                         "fill": "SALTY LIQUID", "chips": "SAME SALT AS SALT & VINEGAR CHIPS",
                         "cools": "COOLS DOWN...", "still": "STILL LIQUID", "push": "WAITING FOR A PUSH",
                         "seed": "ONE CRYSTAL STARTS", "domino": "THE REST FOLLOW", "brick": "HARD AS A BRICK",
                         "done": "USED UP?", "boil": "BOIL A FEW MINUTES", "melt": "CRYSTALS MELT BACK",
                         "hour": "COLD WITHIN AN HOUR", "ski": "SKI DAY: ALL DAY", "iron": "IRON + AIR = RUST + HEAT",
                         "hours": "WARM FOR HOURS", "trick": "IT GETS HOT BY FREEZING!", "out": "SOLID = HEAT OUT",
                         "seat": "HEATED SEAT!", "pocket": "BACK POCKET"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: متحف المستقبل"),
                      "stat": [("1", "ضغطة"), ("54°", "خلال ثواني"), ("10", "ساعات للي ينرمى")],
                      "L": {"name": "دفاية يد", "click": "تك!", "frozen": "أصابع متجمدة", "where": "الحرارة من وين؟",
                            "fill": "سائل مالح", "chips": "نفس ملح شيبس الملح والخل",
                            "cools": "يبرد...", "still": "ويظل سائل", "push": "ينتظر أحد يدزه",
                            "seed": "حبة كريستال وحدة", "domino": "والباقي يلحقها", "brick": "صار حجر",
                            "done": "خلاص؟", "boil": "تغليه كم دقيقة", "melt": "الكريستال يذوب",
                            "hour": "يبرد خلال ساعة", "ski": "الكشتة طويلة", "iron": "حديد + هوا = صدأ + حرارة",
                            "hours": "دفا لساعات", "trick": "يسخن لأنه يتجمد!", "out": "صلب = حرارة طالعة",
                            "seat": "كرسي مدفّى!", "pocket": "الجيب الورا"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "click": ("hook", "CLICK", 0.15), "cold": ("hook", "COLD", 0.55), "crystals": ("hook", "CRYSTALS", 0.85),
            "frozen": ("break1", "FROZEN", 0.1), "campfire": ("break1", "FIRE", 0.3), "pocket": ("break1", "POCKET", 0.5),
            "heat": ("break1", "HEAT", 0.8),
            "fill": ("fix1", "FILL", 0.15), "salty": ("fix1", "SALTY", 0.35), "chips": ("fix1", "CHIPS", 0.85),
            "cools": ("break2", "COOLS", 0.15), "stays": ("break2", "STAYS", 0.5), "push": ("break2", "PUSH", 0.9),
            "click2": ("fix2", "CLICK", 0.15), "seed": ("fix2", "CRYSTAL", 0.45), "domino": ("fix2", "DOMINOES", 0.85),
            "hard": ("break3", "HARD", 0.4), "done": ("break3", "DONE", 0.85),
            "boil": ("fix3", "BOIL", 0.2), "melt": ("fix3", "MELT", 0.75),
            "hour": ("break4", "HOUR", 0.35), "ski": ("break4", "SKI", 0.7), "longer": ("break4", "LONGER", 0.9),
            "throw": ("fix4", "THROWAWAY", 0.15), "rusts": ("fix4", "RUSTS", 0.35), "iron": ("fix4", "IRON", 0.45),
            "warm": ("fix4", "WARM", 0.85),
            "follow": ("cta", "FOLLOW", 0.35),
            "freezing": ("reveal", "FREEZING", 0.3), "solid": ("reveal", "SOLID", 0.6), "boiled": ("reveal", "BOILED", 0.9),
            "s1": ("stat", "ONE", 0.05), "s2": ("stat", "FIFTY", 0.35), "s3": ("stat", "TEN", 0.75),
            "cong2": ("closer", "CONGRATS", 0.16),
            "t_pocket": ("tag", "POCKET", 0.2), "t_sit": ("tag", "SIT", 0.4), "t_click": ("tag", "CLICK", 0.65),
            "t_heated": ("tag", "HEATED", 0.85)})
        T["frozen1"] = T["frozen"] + 0.2
        T["fill1"] = max(T["fill"], T["chips"]) + 0.25
        T["stays1"] = max(T["stays"], T["cools"]) + 0.2
        T["seed1"] = max(T["seed"], T["click2"]) + 0.2
        T["hard1"] = T["hard"] + 0.1
        T["melt1"] = max(T["melt"], T["boil"]) + 0.2
        T["hour1"] = max(T["hour"], s("break4") + 0.3)
        T["warm1"] = max(T["warm"], T["iron"]) + 0.2
        # ---- sets
        self.cut(s("fix3") - 0.12, "stove", 1)
        self.cut(s("break4") - 0.12, "slope", -1)
        self.cut(s("fix4") - 0.12, "packet", 1)
        self.cut(s("reveal") - 0.12, "pouch", -1)
        self.cut(s("tag") - 0.2, "bench", 1)
        # ---- camera (pouch set)
        FULL = (0, 70, 1.0)
        LENS = (0, 150, 0.82)
        cm = Camera(DISC[0] + 80, DISC[1] + 10, 2.3)
        cm.key(0.05, DISC[0] + 70, DISC[1] + 20, 2.45, max(0.3, T["click"] - 0.05))
        cm.key(max(0.6, T["click"] + 0.35), *FULL, max(0.6, T["crystals"] - T["click"] + 0.2))
        cm.key(s("break1") - 0.12, 0, 120, 1.05, 0.0)
        cm.key(s("fix1") - 0.12, *FULL, 0.0)
        cm.key(s("break2") - 0.12, *LENS, 0.6)
        cm.key(s("fix2") - 0.12, *LENS, 0.0)
        cm.key(s("break3") - 0.12, *FULL, 0.5)
        cm.key(s("reveal") - 0.12, *LENS, 0.0)
        cm.key(s("stat") - 0.12, 0, 0, 0.9, 0.5)
        cm.key(s("closer") - 0.12, 0, 40, 1.12, 1.4)
        self.cam = cm
        self.spans = [(T["frozen1"], T["fill1"]), (T["stays1"], T["seed1"]), (T["hard1"], T["melt1"]), (T["hour1"], T["warm1"])]
        self.shakes = [(T["click"], 0.3, 7), (T["frozen1"], 0.35, 6), (T["click2"], 0.3, 6), (T["hard1"], 0.35, 8),
                       (s("closer") + 0.2, 0.35, 8), (T["t_click"], 0.3, 8)]

    def phase(self, t):
        s = self.tl.s
        for lab in ("tag", "closer", "stat", "reveal", "cta", "fix4", "break4", "fix3", "break3", "fix2", "break2", "fix1",
                    "break1"):
            if t >= s(lab) - 0.12:
                return lab
        return "hook"

    def pouch_state(self, t):
        """(fill, cryst, heat, press, flash, cold, hands_bare) of the pouch at world time t."""
        T, s = self.T, self.tl.s
        ph = self.phase(t)
        if ph == "hook":
            cr = e_io(prog(t, T["click"] + 0.1, T["crystals"] + 0.7))
            return 1.0, cr, 0.95 * prog(t, T["click"] + 0.5, T["crystals"] + 0.9), bump(t, T["click"] - 0.1, T["click"] + 0.35), \
                bump(t, T["click"], T["click"] + 0.4), 0.0, 0.0
        if ph == "break1":
            return 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0
        if ph == "fix1":
            return e_io(prog(t, T["fill"] - 0.2, T["chips"] + 0.4)), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if ph == "break2":
            return 1.0, 0.0, 0.0, 0.0, 0.0, 0.7 * prog(t, T["cools"], T["stays"]), 0.0
        if ph == "fix2":
            cr = e_io(prog(t, T["seed"], T["domino"] + 0.9))
            return 1.0, cr, 0.9 * prog(t, T["seed"] + 0.3, T["domino"] + 1.0), bump(t, T["click2"] - 0.1, T["click2"] + 0.35), \
                bump(t, T["click2"], T["click2"] + 0.4), 0.0, 0.0
        if ph == "break3":
            return 1.0, 1.0, 0.9 * (1 - prog(t, s("break3"), T["done"] + 0.3)), 0.0, 0.0, 0.25 * prog(t, T["hard"], T["done"]), 0.0
        if ph in ("reveal", "cta"):
            cr = e_io(prog(t, s("reveal") + 0.2, T["solid"] + 0.6)) if ph == "reveal" else 1.0
            return 1.0, cr, 0.9 * prog(t, s("reveal") + 0.4, T["solid"] + 0.8), 0.0, 0.0, 0.0, 0.0
        return 1.0, 1.0, 0.95, 0.0, 0.0, 0.0, 0.0                         # stat, closer

    # ------------------------------------------------------------------ set: pouch
    def draw_pouch(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        ph = self.phase(t)
        night_bg(c, t, speed=1.6 if ph == "break1" else 1.0)
        self.view(c, cam)
        fill, cryst, heat, press, flash, cold, bare = self.pouch_state(t)
        shake = 1.0 if ph == "break1" else 0.0
        for sd in (-1, 1):
            mitten(c, sd * 250, 150, side=sd, bare=bare, cold=cold, shake=shake, t=t)
        if ph != "break1":
            pouch(c, t, fill=fill, cryst=cryst, heat=heat, press=press, flash=flash, cold=cold)
        for sd in (-1, 1):
            mitten(c, sd * 250, 150, side=sd, bare=bare, cold=cold, shake=shake, t=t, front=True)
        if ph == "break1":                                                # frost on the cold fingers
            rng = random.Random(9)
            for k in range(18):
                fx_ = rng.choice((-1, 1)) * rng.uniform(170, 330)
                c.drawCircle(fx_, rng.uniform(20, 120), rng.uniform(3, 7), P("#E0F2FE", 0.5 + 0.4 * math.sin(t * 3 + k)))
        if ph == "hook":                                                  # the finger comes in and clicks
            k = 1 - prog(t, T["click"] + 0.5, T["click"] + 0.9)
            far = 1 - e_out(prog(t, 0.0, T["click"] - 0.05))
            fingertip(c, DISC[0] + 8 + 90 * far, DISC[1] - 20 - 170 * far, 1.0, press=press, a=k)
        if ph == "fix2":
            k = prog(t, s("fix2"), s("fix2") + 0.3) * (1 - prog(t, T["click2"] + 0.5, T["click2"] + 0.9))
            fingertip(c, DISC[0] + 8, DISC[1] - 20, 1.0, press=press, a=k)
        if ph == "break3":                                                # a knuckle knocks on the solid pouch
            kn = bump(t, T["hard"] - 0.1, T["hard"] + 0.12) + bump(t, T["hard"] + 0.18, T["hard"] + 0.4)
            fist(c, 150, -250 + 55 * kn, 1.0, a=prog(t, s("break3"), s("break3") + 0.3))
        c.restore()
        self.ui["cam"] = cam

    def ui_pouch(self, c, t, tw):
        T, s = self.T, self.tl.s
        ph = self.phase(tw)
        if ph == "hook":
            self.chip(540, 300, "click", T["click"] - 0.1, T["cold"] - 0.1, accent=HILITE, size=54)
            self.chip(540, 300, "name", T["crystals"] - 0.2, s("break1") + 0.1, accent=HILITE, size=50)
            k = self.span(T["crystals"], s("break1"))
            if k > 0:
                thermometer(c, 950, 900, 1.2, lerp(0.2, 0.85, prog(tw, T["crystals"], T["crystals"] + 1.0)), hot=True, a=k)
            return
        if ph == "break1":
            self.chip(540, 300, "frozen", T["frozen"] - 0.1, T["heat"] - 0.2, accent="#7DD3FC", size=46)
            self.chip(540, 300, "where", T["heat"] - 0.2, s("fix1") - 0.15, accent=HILITE, size=46)
            k = self.span(T["campfire"] - 0.2, s("fix1") - 0.15)
            pocket_fire(c, 540, 600, 1.0, tw, cross=prog(tw, T["pocket"], T["pocket"] + 0.4), a=k)
            thermometer(c, 950, 900, 1.2, 0.12, hot=False, a=self.span(s("break1"), s("fix1") - 0.15))
            self.badge("alert", T["frozen1"], s("fix1") - 0.2, x=920, y=440)
            self.red(T["frozen1"], 1.2)
            return
        if ph == "fix1":
            self.chip(540, 300, "fill", T["fill"] - 0.2, T["chips"] - 0.3, accent="#7DD3FC", size=48)
            self.chip(540, 300, "chips", T["chips"] - 0.3, s("break2") - 0.15, accent=HILITE, size=36)
            k = self.span(T["salty"] - 0.2, s("break2") - 0.15)
            chips_bag(c, 300, 520, 0.9, tw, pour=prog(tw, T["salty"], T["salty"] + 0.4), a=k)
            self.badge("check", T["fill1"], s("break2") - 0.15, x=920, y=440)
            return
        if ph == "break2":
            self.chip(540, 300, "cools", T["cools"] - 0.2, T["stays"] - 0.2, accent="#7DD3FC", size=46)
            self.chip(540, 300, "still", T["stays"] - 0.2, T["push"] - 0.2, accent=WARN, size=46)
            self.chip(540, 300, "push", T["push"] - 0.2, s("fix2") - 0.15, accent=HILITE, size=46)
            lens(c, 540, 510, 160, tw, "wander", a=self.span(T["stays"] - 0.4, s("fix2") - 0.12))
            thermometer(c, 960, 960, 1.15, lerp(0.75, 0.3, prog(tw, T["cools"], T["stays"])), hot=tw < T["stays"],
                        a=self.span(s("break2"), s("fix2") - 0.15))
            self.badge("alert", T["stays1"], s("fix2") - 0.2, x=920, y=440)
            self.red(T["stays1"], 1.2)
            return
        if ph == "fix2":
            self.chip(540, 300, "click", T["click2"] - 0.1, T["seed"] - 0.2, accent=HILITE, size=54)
            self.chip(540, 300, "seed", T["seed"] - 0.2, T["domino"] - 0.2, accent="#E0F2FE", size=46)
            self.chip(540, 300, "domino", T["domino"] - 0.2, s("break3") - 0.15, accent=GOOD, size=46)
            kl = self.span(T["seed"] - 0.3, T["domino"] - 0.1)
            lens(c, 540, 510, 160, tw, "lock", k=prog(tw, T["seed"], T["domino"]), a=kl)
            dominoes(c, 230, 850, 640, tw, T["domino"] - 0.1, a=self.span(T["domino"] - 0.2, s("break3") - 0.15))
            self.badge("check", T["seed1"], s("break3") - 0.15, x=920, y=440)
            return
        if ph == "break3":
            self.chip(540, 300, "brick", T["hard"] - 0.2, T["done"] - 0.15, accent=WARN, size=48)
            self.chip(540, 300, "done", T["done"] - 0.15, s("fix3") - 0.15, accent=WARN, size=48)
            thermometer(c, 950, 900, 1.2, lerp(0.85, 0.3, prog(tw, s("break3"), T["done"] + 0.3)), hot=True,
                        a=self.span(s("break3"), s("fix3") - 0.15))
            self.badge("alert", T["hard1"], s("fix3") - 0.2, x=920, y=440)
            self.red(T["hard1"], 1.2)
            return
        if ph == "reveal":
            self.chip(540, 300, "trick", T["freezing"] - 0.25, T["solid"] - 0.15, accent=HILITE, size=48)
            self.chip(540, 300, "out", T["solid"] - 0.15, s("stat") - 0.15, accent=WARMC, size=48)
            lens(c, 540, 510, 160, tw, "lock", k=prog(tw, T["freezing"] - 0.2, T["boiled"] + 0.2), heat=1.0,
                 a=self.span(T["freezing"] - 0.3, s("stat") - 0.12))
            return

    # ------------------------------------------------------------------ set: stove (fix3)
    def draw_stove(self, c, t):
        T = self.T
        pot_scene(c, t, boil=1.0, melt=e_io(prog(t, T["boil"] + 0.2, T["melt"] + 0.8)))

    def ui_stove(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "boil", T["boil"] - 0.2, T["melt"] - 0.2, accent="#7DD3FC", size=48)
        self.chip(540, 300, "melt", T["melt"] - 0.2, s("break4") - 0.15, accent=GOOD, size=48)
        self.badge("check", T["melt1"], s("break4") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: slope (break4)
    def draw_slope(self, c, t):
        T, s = self.T, self.tl.s
        k = prog(t, s("break4"), T["hour"] + 0.6)
        slope_scene(c, t, hours=k, fade_k=k)

    def ui_slope(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "hour", T["hour"] - 0.3, T["ski"] - 0.2, accent="#7DD3FC", size=46)
        self.chip(540, 300, "ski", T["ski"] - 0.2, s("fix4") - 0.15, accent=WARN, size=46)
        self.badge("alert", T["hour1"], s("fix4") - 0.2, x=920, y=440)
        self.red(T["hour1"], 1.2)

    # ------------------------------------------------------------------ set: packet (fix4, cta)
    def draw_packet(self, c, t):
        T = self.T
        night_bg(c, t)
        op = prog(t, T["throw"] + 0.1, T["throw"] + 0.7)
        air = prog(t, T["throw"] + 0.5, T["throw"] + 0.9)
        xr = prog(t, T["rusts"] - 0.3, T["rusts"])
        rust = prog(t, T["iron"], T["warm"] + 0.6)
        packet(c, 540, 860, 1.15, t, open_k=op, rust=rust, air=air, xray=xr)

    def ui_packet(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 300, "iron", T["rusts"] - 0.2, T["warm"] - 0.2, accent=WARMC, size=40)
        self.chip(540, 300, "hours", T["warm"] - 0.2, s("cta") - 0.15, accent=GOOD, size=48)
        thermometer(c, 960, 1180, 1.1, lerp(0.15, 0.8, prog(tw, T["iron"], T["warm"] + 0.6)), hot=True,
                    a=self.span(T["iron"] - 0.2, s("reveal") - 0.15))
        self.badge("check", T["warm1"], s("cta") - 0.15, x=920, y=440)

    # ------------------------------------------------------------------ set: bench (tag)
    def draw_bench(self, c, t):
        T = self.T
        sit = prog(t, T["t_pocket"], T["t_sit"] + 0.3)
        click = bump(t, T["t_click"] - 0.05, T["t_click"] + 0.8)
        jump = prog(t, T["t_heated"] - 0.15, T["t_heated"] + 0.2)
        bench_scene(c, t, sit=sit, click=click, jump=jump)

    def ui_bench(self, c, t, tw):
        T = self.T
        self.chip(540, 300, "pocket", T["t_pocket"] - 0.1, T["t_click"] - 0.1, accent="#C4B5FD", size=42)
        self.chip(540, 300, "seat", T["t_click"] - 0.05, self.duration + 1, accent=WARN, size=50)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, NIGHT)

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.6, False, 61), -14), (T["click"], sfx.click(62), 0), (T["click"] + 0.15, sfx.sparkle(1.2, 14, 63), -8),
              (T["crystals"], sfx.sizzle(0.8, 64), -14), (T["crystals"] + 0.3, sfx.chime(), -9)]
        ev += [(T["frozen"], sfx.whoosh(0.8, True, 65), -14), (T["frozen1"], sfx.alarm(3, 820.0), -12),
               (T["pocket"], sfx.buzz(0.4), -14)]
        ev += [(T["fill"], sfx.hiss(1.2, 66), -16), (T["salty"] + 0.1, sfx.sparkle(0.8, 10, 67), -12),
               (T["fill1"], sfx.ding(), -8), (T["fill1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["cools"], sfx.power_down(1.0, 68), -14), (T["stays1"], sfx.alarm(3, 820.0), -12)]
        ev += [(T["click2"], sfx.click(69), 0), (T["seed"], sfx.sparkle(1.0, 12, 70), -8)]
        for k in range(9):
            ev.append((T["domino"] - 0.1 + k * 0.11, sfx.tap(71 + k), -10))
        ev += [(T["seed1"], sfx.ding(), -8), (T["seed1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["hard"], sfx.thunk(80), -4), (T["hard"] + 0.25, sfx.thunk(81), -6), (T["hard1"] + 0.3, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix3") - 0.12, sfx.whoosh(0.45, True, 82), -6), (T["boil"], sfx.hiss(2.0, 83), -14),
               (T["melt1"], sfx.ding(), -8), (T["melt1"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break4") - 0.12, sfx.whoosh(0.45, False, 84), -6), (T["hour"], sfx.tick(), -8),
               (T["hour"] + 0.3, sfx.tick(), -8), (T["hour1"] + 0.4, sfx.power_down(1.0, 85), -14)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.45, True, 86), -6), (T["throw"] + 0.1, sfx.snap(87), -6),
               (T["iron"], sfx.sizzle(0.8, 88), -14), (T["warm1"], sfx.ding(), -8), (T["warm1"] + 0.2, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(92), 0), (T["follow"] - 0.15, sfx.pop(93), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 94), -6), (T["freezing"], sfx.sparkle(1.0, 12, 95), -9)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 96), -6), (T["s1"], sfx.pop(97), -3), (T["s2"], sfx.pop(98), -3),
               (T["s3"], sfx.pop(99), -3)]
        ev += [(T["cong2"], sfx.pop(100), -2), (T["cong2"], sfx.sparkle(1.4, 18, 101), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 102), -6), (T["t_click"], sfx.click(103), 0), (T["t_heated"], sfx.womp(), -8)]
        return ev


NAME = "handwarmer"
EPISODE = HandWarmer
