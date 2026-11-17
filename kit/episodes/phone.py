"""Episode 35 - A smartphone.  v2 look: a giant phone on the Moon next to the Apollo lander, the 1973 brick phone that
shrinks into a chip, the phone in your hand (touch grid, tilt sensor, map), GPS satellites around the Earth, a night
photo made of fifteen shots, and the tag with mom's good-morning flowers.

Sets: moon (hook: a million times the memory of the Moon computer, playing a cat video; the stat and the closer),
brick (break1: the first mobile phone, over a kilo, ten hours to charge, thirty-five minutes of talk; fix1: it all
shrinks onto one fingernail-sized chip of nineteen billion switches), screen (break2/fix2: glass can't feel, then a grid
of invisible wires; break3/fix3: which way is up, then the accelerometer smaller than a grain of rice; break4: where
am I), space (fix4: satellites 20,000 km up, clocks corrected for relativity; the cta), night (reveal: fifteen photos
merged into one in the dark, then into the pocket), mom (the tag).
"""
from v2_base import *  # noqa: F401,F403

SPACE = {"top": "#02030A", "upper": "#050816", "mid": "#0A1030", "low": "#141B45", "horizon": "#26306B",
         "space_top": "#010208", "space_mid": "#040817", "space_low": "#0A1232"}
BODY = "#1E293B"
CYAN = "#22D3EE"
GOLD = "#F5B83D"


# ====================================================================================== pieces
def word(c, s, x, y, size, col, a=1.0, align="center"):
    if a <= 0 or not s:
        return
    if arabic.is_ar(s):
        arabic.text_ar(c, s, x, y, size * 1.15, col, "Tajawal-Black", align=align, a=a)
    else:
        text(c, s, x, y, size, col, "Poppins-Black", align=align, a=a)


def cat_face(c, x, y, s, t, a=1.0, meow=0.0):
    """A cartoon cat's head (generic)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y + math.sin(t * 3) * 6 * s)
    c.scale(s, s)
    c.rotate(math.sin(t * 2.2) * 6)
    for sx in (-1, 1):
        ear = skia.Path()
        ear.moveTo(sx * 70, -40)
        ear.lineTo(sx * 92, -128)
        ear.lineTo(sx * 18, -78)
        ear.close()
        c.drawPath(ear, P("#F59E0B", a))
        inner = skia.Path()
        inner.moveTo(sx * 64, -58)
        inner.lineTo(sx * 80, -110)
        inner.lineTo(sx * 34, -80)
        inner.close()
        c.drawPath(inner, P("#FDA4AF", a))
    c.drawOval(R(-110, -100, 220, 190), P("#F59E0B", a))
    for k in range(3):
        c.drawLine(-20 + k * 20, -98, -14 + k * 14, -60, P("#B45309", a, stroke=7))
    blink_ = 0.15 if (t % 3.1) < 0.12 else 1.0
    for sx in (-1, 1):
        c.drawOval(R(sx * 42 - 16, -30 - 20 * blink_, 32, 40 * blink_), P("#14532D", a))
        c.drawCircle(sx * 42 + 5, -36, 5 * blink_, P("#FFFFFF", a))
    c.drawPath(_nose(), P("#FB7185", a))
    if meow > 0:
        c.drawOval(R(-16, 22, 32, 30 * meow), P("#7F1D1D", a))
    else:
        c.drawArc(R(-24, 10, 24, 20), 0, 180, False, P("#7C2D12", a, stroke=5))
        c.drawArc(R(0, 10, 24, 20), 0, 180, False, P("#7C2D12", a, stroke=5))
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            c.drawLine(sx * 40, 16 + k * 10, sx * 120, 6 + k * 20, P("#FFFFFF", a * 0.85, stroke=3))
    c.restore()


def _nose():
    p = skia.Path()
    p.moveTo(-12, 0)
    p.lineTo(12, 0)
    p.lineTo(0, 14)
    p.close()
    return p


def cat_video(c, x, y, w, h, t, a=1.0, meow=0.0, bright=1.0):
    """The screen content: a cat video (rect at x, y, w, h)."""
    c.drawRect(R(x, y, w, h), lin_paint(0, y, 0, y + h, [mix("#0F172A", "#C4B5FD", bright), mix("#0F172A", "#FBCFE8", bright)], a=a))
    cat_face(c, x + w / 2, y + h * 0.5, min(w, h) / 360.0, t, a=a, meow=meow)
    c.drawRect(R(x + 24, y + h - 40, w - 48, 8), P("#FFFFFF", 0.4 * a))
    c.drawRect(R(x + 24, y + h - 40, (w - 48) * ((t * 0.07) % 1.0), 8), P("#EF4444", a))


def app_grid(c, x, y, w, h, a=1.0, hi=-1, t=0.0):
    c.drawRect(R(x, y, w, h), lin_paint(0, y, 0, y + h, ["#312E81", "#7C3AED", "#DB2777"], a=a))
    cols = ("#22C55E", "#F59E0B", "#3B82F6", "#EF4444", "#14B8A6", "#A855F7", "#F43F5E", "#84CC16", "#06B6D4",
            "#EAB308", "#6366F1", "#10B981")
    s = w / 4.0
    for i in range(12):
        cx_ = x + s * (i % 4 + 0.5)
        cy_ = y + 120 + s * (i // 4) * 1.05
        k = 1.12 if i == hi else 1.0
        c.drawRRect(rr(cx_ - s * 0.32 * k, cy_ - s * 0.32 * k, s * 0.64 * k, s * 0.64 * k, s * 0.16), P(cols[i], a))
    c.drawRRect(rr(x + w * 0.3, y + h - 30, w * 0.4, 8, 4), P("#FFFFFF", 0.7 * a))


def map_view(c, x, y, w, h, t, a=1.0):
    c.drawRect(R(x, y, w, h), P("#5B7F5A", a))
    rv = skia.Path()
    rv.moveTo(x - 20, y + h * 0.7)
    rv.cubicTo(x + w * 0.3, y + h * 0.5, x + w * 0.6, y + h * 0.9, x + w + 20, y + h * 0.6)
    c.drawPath(rv, P("#2563EB", a, stroke=40))
    for k in range(1, 6):
        c.drawLine(x + k * w / 6, y, x + k * w / 6 + 30, y + h, P("#CBD5E1", a, stroke=12))
        c.drawLine(x, y + k * h / 6, x + w, y + k * h / 6 - 20, P("#CBD5E1", a, stroke=12))
    for i in range(5):
        c.drawRRect(rr(x + 30 + (i * 157) % (w - 120), y + 60 + (i * 211) % (h - 160), 80, 60, 10), P("#3F5F3E", a))


def pin(c, x, y, s, col, a=1.0, q=False):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = skia.Path()
    p.moveTo(0, 0)
    p.cubicTo(-30, -40, -46, -60, -46, -86)
    p.cubicTo(-46, -116, -24, -136, 0, -136)
    p.cubicTo(24, -136, 46, -116, 46, -86)
    p.cubicTo(46, -60, 30, -40, 0, 0)
    c.drawPath(p, P("#000000", 0.3 * a, blur=8))
    c.drawPath(p, P(col, a))
    if q:
        text(c, "?", 0, -70, 56, "#FFFFFF", "Poppins-Black", a=a)
    else:
        c.drawCircle(0, -88, 18, P("#FFFFFF", a))
    c.restore()


def phone(c, x, y, h, t, content="cat", rot=0.0, a=1.0, grid=0.0, glow=0.0, content_rot=0.0, meow=0.0, hi=-1,
          bright=1.0, inner=None):
    """Front view of a phone centred at (x, y), height h.  content: cat | apps | map | photo | dark | black.
    content_rot turns the picture inside the screen (degrees), grid 0..1 shows the touch wires under the glass."""
    if a <= 0:
        return
    w = h * 0.48
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if glow > 0:
        add_glow(c, 0, 0, h * 0.75, CYAN, 0.35 * glow * a)
    c.drawRRect(rr(-w / 2 - 6, -h / 2 - 6, w + 12, h + 12, w * 0.16), P("#000000", 0.5 * a, blur=22))
    c.drawRRect(rr(-w / 2, -h / 2, w, h, w * 0.15), lin_paint(-w / 2, 0, w / 2, 0, ["#475569", "#CBD5E1", "#475569"], a=a))
    c.drawRRect(rr(-w / 2 + 6, -h / 2 + 6, w - 12, h - 12, w * 0.13), P("#0B0F19", a))
    sx, sy, sw, sh = -w / 2 + 16, -h / 2 + 16, w - 32, h - 32
    c.save()
    c.clipRRect(rr(sx, sy, sw, sh, w * 0.11), doAntiAlias=True)
    if content_rot:
        c.save()
        c.rotate(content_rot)
        big = max(sw, sh)
        bx, by, bw, bh = -big / 2, -sw / 2, big, sw
        _content(c, content, bx, by, bw, bh, t, a, meow, hi, bright)
        c.restore()
    else:
        _content(c, content, sx, sy, sw, sh, t, a, meow, hi, bright)
    if inner:
        inner(c, sx, sy, sw, sh)
    if grid > 0:
        n = 9
        for k in range(n + 1):
            gx = sx + k * sw / n
            c.drawLine(gx, sy, gx, sy + sh, P(CYAN, 0.75 * grid * a, stroke=3))
        for k in range(int(n * sh / sw) + 1):
            gy = sy + k * sw / n
            c.drawLine(sx, gy, sx + sw, gy, P("#A78BFA", 0.75 * grid * a, stroke=3))
    c.restore()
    c.drawRRect(rr(-w * 0.12, -h / 2 + 22, w * 0.24, 22, 11), P("#000000", a))
    c.restore()


def _content(c, kind, x, y, w, h, t, a, meow, hi, bright):
    if kind == "cat":
        cat_video(c, x, y, w, h, t, a, meow, bright)
    elif kind == "apps":
        app_grid(c, x, y, w, h, a, hi, t)
    elif kind == "map":
        map_view(c, x, y, w, h, t, a)
    elif kind == "dark":
        c.drawRect(R(x, y, w, h), P("#05060B", a))
    else:
        c.drawRect(R(x, y, w, h), P("#000000", a))


def lander(c, x, y, s, a=1.0):
    """The Apollo lunar module (feet on x, y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for sx in (-1, 1):
        c.drawLine(sx * 70, -110, sx * 150, -10, P("#CBD5E1", a, stroke=8))
        c.drawOval(R(sx * 150 - 26, -16, 52, 16), P("#E5E7EB", a))
        c.drawLine(sx * 40, -60, sx * 150, -10, P("#94A3B8", a, stroke=5))
    oc = skia.Path()
    oc.moveTo(-100, -170)
    oc.lineTo(100, -170)
    oc.lineTo(120, -130)
    oc.lineTo(100, -80)
    oc.lineTo(-100, -80)
    oc.lineTo(-120, -130)
    oc.close()
    c.drawPath(oc, lin_paint(-120, 0, 120, 0, ["#B45309", GOLD, "#FDE68A", "#B45309"], a=a))
    for k in range(5):
        c.drawLine(-90 + k * 45, -165, -80 + k * 45, -85, P("#92400E", 0.5 * a, stroke=3))
    cab = skia.Path()
    cab.moveTo(-80, -170)
    cab.lineTo(-90, -230)
    cab.lineTo(-40, -290)
    cab.lineTo(50, -290)
    cab.lineTo(95, -240)
    cab.lineTo(80, -170)
    cab.close()
    c.drawPath(cab, lin_paint(-90, 0, 95, 0, ["#6B7280", "#D1D5DB", "#9CA3AF"], a=a))
    c.drawPath(cab, P("#374151", a, stroke=3))
    tri = skia.Path()
    tri.moveTo(-50, -250)
    tri.lineTo(-20, -270)
    tri.lineTo(-20, -230)
    tri.close()
    c.drawPath(tri, P("#111827", a))
    c.drawLine(40, -290, 70, -340, P("#E5E7EB", a, stroke=4))
    c.drawCircle(70, -346, 16, P("#E5E7EB", a, stroke=4))
    c.restore()


def earth(c, x, y, r, a=1.0, spin=0.0):
    if a <= 0:
        return
    add_glow(c, x, y, r * 1.5, "#60A5FA", 0.35 * a)
    c.drawCircle(x, y, r, rad_paint(x - r * 0.3, y - r * 0.3, r * 1.4, ["#60A5FA", "#1D4ED8", "#0B1E5B"], a=a))
    c.save()
    pth = skia.Path()
    pth.addCircle(x, y, r)
    c.clipPath(pth, doAntiAlias=True)
    rng = random.Random(7)
    for i in range(9):
        lx = x + ((rng.uniform(-1.4, 1.4) + spin) % 2.8 - 1.4) * r
        ly = y + rng.uniform(-0.8, 0.8) * r
        c.drawOval(R(lx - r * 0.3, ly - r * 0.18, r * rng.uniform(0.4, 0.7), r * rng.uniform(0.25, 0.4)), P("#22C55E", 0.85 * a))
    for i in range(6):
        lx = x + ((rng.uniform(-1.4, 1.4) + spin * 1.3) % 2.8 - 1.4) * r
        ly = y + rng.uniform(-0.9, 0.9) * r
        c.drawOval(R(lx - r * 0.25, ly - 8, r * 0.5, 16), P("#FFFFFF", 0.6 * a))
    c.drawCircle(x + r * 0.35, y + r * 0.3, r * 1.05, P("#000000", 0.35 * a))
    c.restore()


def satellite(c, x, y, s, ang, a=1.0, glow=0.0):
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    for sx in (-1, 1):
        c.drawRect(R(sx * 40 - (60 if sx < 0 else 0) - (0 if sx < 0 else -0), -18, 60, 36), P("#1D4ED8", a))
        for k in range(3):
            c.drawLine(sx * 40 + (-60 if sx < 0 else 0) + k * 20, -18, sx * 40 + (-60 if sx < 0 else 0) + k * 20, 18,
                       P("#93C5FD", 0.6 * a, stroke=2))
    c.drawRRect(rr(-26, -26, 52, 52, 8), P(GOLD, a))
    c.drawLine(0, 26, 0, 46, P("#E5E7EB", a, stroke=4))
    if glow > 0:
        add_glow(c, 0, 0, 80, "#FDE047", 0.5 * glow * a)
    c.restore()


def mini_clock(c, x, y, r, t, a=1.0, ok=0.0):
    if a <= 0:
        return
    c.drawCircle(x, y, r, P("#F8FAFC", a))
    c.drawCircle(x, y, r, P(mix(WARN, GOOD, ok), a, stroke=5))
    an = t * 3.0
    c.drawLine(x, y, x + math.sin(an) * r * 0.7, y - math.cos(an) * r * 0.7, P("#0F172A", a, stroke=4))
    c.drawLine(x, y, x + math.sin(an / 12) * r * 0.45, y - math.cos(an / 12) * r * 0.45, P("#0F172A", a, stroke=5))


def brick(c, x, y, h, a=1.0, glow=0.0):
    """The 1973 brick phone, centred at (x, y), height h (with the antenna)."""
    if a <= 0:
        return
    u = h / 700.0
    c.save()
    c.translate(x, y)
    c.scale(u, u)
    c.drawRRect(rr(60, -350, 26, 170, 12), P("#475569", a))
    c.drawRRect(rr(-120, -200, 240, 550, 40), P("#000000", 0.5 * a, blur=20))
    c.drawRRect(rr(-120, -200, 240, 550, 40), lin_paint(-120, 0, 120, 0, ["#A8A29E", "#E7E5E4", "#A8A29E"], a=a))
    c.drawRRect(rr(-80, -150, 160, 60, 10), P("#14532D", a))
    word(c, "8:00", 0, -108, 34, "#4ADE80", a)
    for i in range(12):
        bx = -60 + (i % 3) * 60
        by = -40 + (i // 3) * 70
        c.drawRRect(rr(bx - 22, by - 22, 44, 44, 10), P("#57534E", a))
        c.drawRRect(rr(bx - 18, by - 22, 36, 36, 8), P("#78716C", a))
    for k in range(5):
        c.drawLine(-60 + k * 30, 300, -50 + k * 30, 330, P("#57534E", a, stroke=4))
    if glow > 0:
        add_glow(c, 0, 0, 500, HILITE, 0.3 * glow * a)
    c.restore()


def chip(c, x, y, s, t, zoom=0.0, a=1.0, glow=0.0):
    """A processor chip (centre x, y, half-size s).  zoom 0..1 shows the grid of switches getting finer."""
    if a <= 0:
        return
    for side in range(4):
        for k in range(8):
            o = -s * 0.8 + k * s * 0.228
            if side == 0:
                c.drawRect(R(x + o - 5, y - s - 22, 10, 24), P(GOLD, a))
            elif side == 1:
                c.drawRect(R(x + o - 5, y + s - 2, 10, 24), P(GOLD, a))
            elif side == 2:
                c.drawRect(R(x - s - 22, y + o - 5, 24, 10), P(GOLD, a))
            else:
                c.drawRect(R(x + s - 2, y + o - 5, 24, 10), P(GOLD, a))
    c.drawRRect(rr(x - s, y - s, 2 * s, 2 * s, s * 0.12), lin_paint(x - s, y - s, x + s, y + s, ["#1F2937", "#111827"], a=a))
    d = s * 0.66
    c.drawRect(R(x - d, y - d, 2 * d, 2 * d), lin_paint(x - d, y - d, x + d, y + d, ["#6D28D9", "#0EA5E9", "#10B981"], a=a))
    n = int(4 * (2 ** (zoom * 3.5)))
    n = max(4, min(n, 48))
    for k in range(1, n):
        q = x - d + 2 * d * k / n
        c.drawLine(q, y - d, q, y + d, P("#0F172A", 0.55 * a, stroke=max(1.0, 3 - zoom * 2)))
        q = y - d + 2 * d * k / n
        c.drawLine(x - d, q, x + d, q, P("#0F172A", 0.55 * a, stroke=max(1.0, 3 - zoom * 2)))
    if glow > 0:
        add_glow(c, x, y, s * 2, CYAN, 0.45 * glow * a)


def finger(c, x, y, s, ang=-30.0, a=1.0, nail=True):
    """An index finger whose tip is at (x, y), coming from below-right."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    c.drawRRect(rr(-38, -8, 76, 420, 38), P("#000000", 0.3 * a, blur=12))
    c.drawRRect(rr(-38, -8, 76, 420, 38), lin_paint(-38, 0, 38, 0, ["#D99A6C", "#F1BE94", "#D99A6C"], a=a))
    if nail:
        c.drawRRect(rr(-24, 4, 48, 60, 20), P("#FBD5C0", a))
    c.drawLine(-20, 150, 20, 150, P("#B9784A", 0.6 * a, stroke=4))
    c.restore()


def rice(c, x, y, s, a=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(-20)
    c.drawOval(R(-60 * s, -24 * s, 120 * s, 48 * s), P("#FEFCE8", a))
    c.drawOval(R(-60 * s, -24 * s, 120 * s, 48 * s), P("#D6D3D1", a, stroke=3))
    c.restore()


def mems(c, x, y, r, shift, a=1.0):
    """Inside the accelerometer: a silicon weight on springs with comb fingers (round inset centred at x, y)."""
    if a <= 0:
        return
    c.drawCircle(x, y, r + 10, P("#000000", 0.4 * a, blur=14))
    c.drawCircle(x, y, r + 8, P("#E2E8F0", a))
    c.save()
    pth = skia.Path()
    pth.addCircle(x, y, r)
    c.clipPath(pth, doAntiAlias=True)
    c.drawCircle(x, y, r, P("#0F172A", a))
    mx = x + shift * r * 0.22
    for sx in (-1, 1):                                          # springs
        sp = skia.Path()
        x0 = x + sx * r * 0.95
        x1 = mx + sx * r * 0.36
        sp.moveTo(x0, y)
        for k in range(1, 9):
            sp.lineTo(lerp(x0, x1, k / 9.0), y + (14 if k % 2 else -14))
        sp.lineTo(x1, y)
        c.drawPath(sp, P("#94A3B8", a, stroke=5))
    c.drawRRect(rr(mx - r * 0.36, y - r * 0.42, r * 0.72, r * 0.84, 10), lin_paint(mx - r * 0.36, 0, mx + r * 0.36, 0, ["#64748B", "#CBD5E1", "#64748B"], a=a))
    for k in range(5):                                          # comb fingers
        fy = y - r * 0.32 + k * r * 0.16
        c.drawRect(R(mx - r * 0.12, fy - 4 + r * 0.42 + 0, r * 0.24, 8), P("#38BDF8", 0.0))
        c.drawRect(R(x - r * 0.9, fy - 3, r * 0.5, 6), P("#38BDF8", a))
        c.drawRect(R(mx - r * 0.36 - r * 0.18, fy + r * 0.08 - 3, r * 0.18, 6), P("#F8FAFC", a))
    c.restore()


def pocket(c, x, y, w, a=1.0, front=False):
    """Jeans with a front pocket (top edge at y)."""
    if a <= 0:
        return
    if not front:
        c.drawRect(R(x - w, y - 40, 2 * w, 2000), lin_paint(0, y, 0, y + 900, ["#1E3A8A", "#1E40AF", "#172554"], a=a))
        c.drawLine(x - w, y - 40, x + w, y - 40, P("#B45309", a, stroke=6))
        return
    pk = skia.Path()
    pk.moveTo(x - 220, y)
    pk.quadTo(x, y + 90, x + 220, y)
    pk.lineTo(x + 240, y + 700)
    pk.lineTo(x - 240, y + 700)
    pk.close()
    c.drawPath(pk, lin_paint(0, y, 0, y + 700, ["#2548A8", "#1E3A8A"], a=a))
    d = skia.Path()
    d.moveTo(x - 220, y + 12)
    d.quadTo(x, y + 102, x + 220, y + 12)
    pa = P("#F59E0B", a, stroke=5)
    pa.setPathEffect(skia.DashPathEffect.Make([16, 12], 0))
    c.drawPath(d, pa)


def couch(c, x, y, w, a=1.0):
    c.drawRRect(rr(x - w / 2, y - 220, w, 150, 40), P("#7C3AED", a))
    c.drawRRect(rr(x - w / 2 - 30, y - 150, 80, 150, 30), P("#6D28D9", a))
    c.drawRRect(rr(x + w / 2 - 50, y - 150, 80, 150, 30), P("#6D28D9", a))
    c.drawRRect(rr(x - w / 2 + 40, y - 110, w - 80, 70, 24), P("#8B5CF6", a))


def mom(c, x, y, h, t, a=1.0):
    """A mother with a headscarf, pointing."""
    person(c, x, y, h, "#DB2777", t, pose="point", face=1, hat="none", hair="#3F2A1A", a=a)
    u = h / 140.0
    sc = skia.Path()
    sc.addCircle(x, y - 132 * u, 21 * u)
    c.drawPath(sc, P("#0EA5E9", a))
    c.drawCircle(x + 4 * u, y - 128 * u, 12 * u, P("#E8B48A", a))
    c.drawRRect(rr(x - 20 * u, y - 116 * u, 40 * u, 16 * u, 8 * u), P("#0EA5E9", a))


def rose(c, x, y, s, a=1.0, col="#E11D48"):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawLine(0, 0, 0, 70, P("#16A34A", a, stroke=6))
    c.drawOval(R(-24, 24, 24, 12), P("#22C55E", a))
    for k in range(5):
        an = math.radians(k * 72)
        c.drawCircle(math.cos(an) * 12, math.sin(an) * 12, 16, P(col, a))
    c.drawCircle(0, 0, 12, P(shade(col, -0.25), a))
    c.restore()


def flower_card(c, x, y, s, label, a=1.0):
    """A 'good morning' picture as a chat message (screen space, centre x, y)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRRect(rr(-150, -110, 300, 220, 22), P("#000000", 0.3 * a, blur=10))
    c.drawRRect(rr(-150, -110, 300, 220, 22), P("#DCFCE7", a))
    c.drawRRect(rr(-140, -100, 280, 160, 16), lin_paint(0, -100, 0, 60, ["#FDE68A", "#FBCFE8"], a=a))
    for k, col in enumerate(("#E11D48", "#F472B6", "#DC2626")):
        rose(c, -70 + k * 70, -50, 0.9, a, col)
    word(c, label, 0, 92, 30, "#166534", a)
    c.restore()


def bubble(c, x, y, s, p, tail_left=True, size=44):
    """Speech bubble (screen space), sized to its text."""
    if p <= 0:
        return
    k = e_back(clamp(p * 1.25))
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
class Phone(EpisodeV2):
    BUILD_NO = 35
    FIRST_SET = "moon"
    CLEAR = "#03040C"
    TITLE = {"en": "SMARTPHONE", "ar_sa": "موبايل"}
    EMPH = {"en": ["CONGRATS", "MILLION", "MEMORY", "COMPUTER", "MOON", "CAT", "VIDEOS", "SMARTPHONE", "FIRST", "KILO",
                   "TEN", "HOURS", "THIRTY-FIVE", "MINUTES", "SHRINK", "CHIP", "FINGERNAIL", "NINETEEN", "BILLION",
                   "SWITCHES", "GLASS", "FEEL", "FINGER", "GRID", "INVISIBLE", "WIRES", "STEALS", "CHARGE", "IDEA",
                   "HOLDING", "GRAIN", "RICE", "SILICON", "WEIGHT", "SPRINGS", "TILT", "MAP", "EXACTLY", "SATELLITES",
                   "TWENTY", "THOUSAND", "KILOMETERS", "CLOCKS", "EINSTEIN'S", "RELATIVITY", "DRIFTS", "FOLLOW", "EGYPT'S",
                   "PYRAMID", "CAMERA", "FIFTEEN", "PHOTOS", "DARK", "POCKET", "YOURSELF", "MOM", "ALWAYS", "SENDS",
                   "GOOD", "MORNING", "FLOWER"],
            "ar_sa": ["مبروك", "ذاكرة", "مليون", "كمبيوتر", "القمر", "قطط", "موبايل", "أول", "كيلو", "عشر", "ساعات",
                      "فتحشر", "شريحة", "ضفرك", "تسعتاشر", "مليار", "مفتاح", "الإزاز", "حاسس", "بصباعك", "شبكة", "سلوك",
                      "يسحب", "كهربا", "عارف", "ماسكه", "إزاي", "حباية", "رز", "سيليكون", "يايات", "تميله", "الخريطة",
                      "فين", "بالظبط", "لأقمار", "بعشرين", "ألف", "وساعاتها", "أينشتاين", "تتوه", "عشرة", "تابعني",
                      "الهرم", "كاميرا", "خمستاشر", "الضلمة", "جيبك", "بإيدك", "وأمك", "طول", "اليوم", "عشرين",
                      "صباح", "الخير", "بالورد"]}
    KEYS = {"ar_sa": {
        ("hook", "MILLION"): "مليون", ("hook", "MEMORY"): "ذاكرة", ("hook", "COMPUTER"): "كمبيوتر", ("hook", "MOON"): "القمر",
        ("hook", "CAT"): "قطط", ("hook", "CONGRATS"): "مبروك", ("hook", "SMARTPHONE"): "موبايل",
        ("break1", "FIRST"): "أول", ("break1", "KILO"): "كيلو", ("break1", "CHARGED"): "يتشحن", ("break1", "TALKED"): "ويكلم",
        ("fix1", "SHRINK"): "فتحشر", ("fix1", "CHIP"): "شريحة", ("fix1", "FINGERNAIL"): "ضفرك", ("fix1", "BILLION"): "مليار",
        ("break2", "GLASS"): "الإزاز", ("break2", "FEEL"): "حاسس", ("break2", "FINGER"): "بصباعك",
        ("fix2", "GRID"): "شبكة", ("fix2", "WIRES"): "سلوك", ("fix2", "STEALS"): "يسحب", ("fix2", "TOUCHES"): "اللمسة",
        ("break3", "IDEA"): "عارف", ("break3", "HOLDING"): "ماسكه",
        ("fix3", "CHIP"): "شريحة", ("fix3", "RICE"): "رز", ("fix3", "SILICON"): "سيليكون", ("fix3", "SPRINGS"): "يايات",
        ("fix3", "TILT"): "تميله",
        ("break4", "MAP"): "الخريطة", ("break4", "WHERE"): "فين", ("break4", "EXACTLY"): "بالظبط",
        ("fix4", "SATELLITES"): "لأقمار", ("fix4", "TWENTY"): "بعشرين", ("fix4", "CLOCKS"): "وساعاتها",
        ("fix4", "EINSTEIN"): "أينشتاين", ("fix4", "DRIFTS"): "تتوه", ("fix4", "TEN"): "عشرة",
        ("cta", "FOLLOW"): "تابعني",
        ("reveal", "CAMERA"): "كاميرا", ("reveal", "FIFTEEN"): "خمستاشر", ("reveal", "DARK"): "الضلمة",
        ("reveal", "ONE"): "واحدة", ("reveal", "POCKET"): "جيبك",
        ("stat", "NINETEEN"): "تسعتاشر", ("stat", "FIFTEEN"): "خمستاشر", ("stat", "SATELLITES"): "وأقمار",
        ("closer", "CONGRATS"): "مبروك",
        ("tag", "MOM"): "وأمك", ("tag", "ALWAYS"): "طول", ("tag", "SENDS"): "تبعتلك", ("tag", "TWENTY"): "عشرين",
        ("tag", "FLOWER"): "بالورد"}}
    TEXT = {"en": {"follow": ("FOLLOW", "next: the Great Pyramid"),
                   "stat": [("19", "BILLION SWITCHES"), ("15", "PHOTOS IN ONE"), ("20,000", "km UP: GPS")],
                   "L": {"apollo": "THE MOON COMPUTER", "kb": "MEMORY: 4 KB", "times": "x 1,000,000 MEMORY",
                         "cats": "...FOR CAT VIDEOS", "sp": "SMARTPHONE", "first": "THE FIRST MOBILE, 1973",
                         "kilo": "OVER 1 kg", "charge": "10 HOURS TO CHARGE", "talk": "35 MIN OF TALK",
                         "shrink": "SHRINK IT ALL", "nail": "SIZE OF A FINGERNAIL", "switches": "19 BILLION SWITCHES",
                         "glass": "GLASS CAN'T FEEL", "grid": "INVISIBLE WIRE GRID", "charge2": "A LITTLE CHARGE",
                         "which": "WHICH WAY IS UP?", "rice": "SMALLER THAN RICE", "springs": "WEIGHT ON SPRINGS",
                         "where": "WHERE AM I?", "up": "20,000 km UP", "clock": "CLOCKS + RELATIVITY",
                         "drift": "OFF BY 10 km A DAY", "fixed": "SPOT ON", "fifteen": "15 PHOTOS", "one": "= 1 BRIGHT PHOTO",
                         "pocket": "INTO YOUR POCKET", "mom": "ALWAYS ON THAT PHONE!", "gm": "GOOD MORNING",
                         "x20": "x 20"}},
            "ar_sa": {"follow": ("تابعني", "الجاي: الهرم الأكبر"),
                      "stat": [("19", "مليار مفتاح"), ("15", "صورة في واحدة"), ("20,000", "كيلو لحد الأقمار")],
                      "L": {"apollo": "كمبيوتر رحلة القمر", "kb": "ذاكرة: 4 كيلوبايت", "times": "ذاكرة أكتر مليون مرة",
                            "cats": "...لفيديوهات القطط", "sp": "موبايل", "first": "أول موبايل، 1973",
                            "kilo": "أتقل من كيلو", "charge": "يتشحن 10 ساعات", "talk": "يكلم 35 دقيقة",
                            "shrink": "تحشر كل ده", "nail": "قد ضفرك", "switches": "19 مليار مفتاح",
                            "glass": "الإزاز مش حاسس", "grid": "شبكة سلوك مش باينة", "charge2": "شوية كهربا",
                            "which": "ماسكه إزاي؟", "rice": "أصغر من حباية رز", "springs": "سيليكون على يايات",
                            "where": "انت فين؟", "up": "20,000 كيلو لفوق", "clock": "ساعات متظبطة",
                            "drift": "تتوه 10 كيلو في اليوم", "fixed": "مظبوط", "fifteen": "15 صورة",
                            "one": "= صورة واحدة منورة", "pocket": "في جيبك", "mom": "انت على الموبايل طول اليوم!",
                            "gm": "صباح الخير", "x20": "× 20"}}}

    # ------------------------------------------------------------------ timing
    def _tracks(self):
        s, e, T = self.tl.s, self.tl.e, self.T
        self.anchors({
            "million": ("hook", "MILLION", 0.12), "memory": ("hook", "MEMORY", 0.2), "computer": ("hook", "COMPUTER", 0.32),
            "moon": ("hook", "MOON", 0.42), "cat": ("hook", "CAT", 0.6), "congrats": ("hook", "CONGRATS", 0.75),
            "sp": ("hook", "SMARTPHONE", 0.95),
            "first": ("break1", "FIRST", 0.1), "kilo": ("break1", "KILO", 0.35), "charged": ("break1", "CHARGED", 0.5),
            "talked": ("break1", "TALKED", 0.75),
            "shrink": ("fix1", "SHRINK", 0.1), "chip": ("fix1", "CHIP", 0.35), "nail": ("fix1", "FINGERNAIL", 0.55),
            "billion": ("fix1", "BILLION", 0.8),
            "glass": ("break2", "GLASS", 0.15), "feel": ("break2", "FEEL", 0.5), "finger": ("break2", "FINGER", 0.8),
            "grid": ("fix2", "GRID", 0.3), "wires": ("fix2", "WIRES", 0.42), "steals": ("fix2", "STEALS", 0.65),
            "touches": ("fix2", "TOUCHES", 0.92),
            "idea": ("break3", "IDEA", 0.3), "holding": ("break3", "HOLDING", 0.75),
            "chip3": ("fix3", "CHIP", 0.1), "rice": ("fix3", "RICE", 0.3), "silicon": ("fix3", "SILICON", 0.5),
            "springs": ("fix3", "SPRINGS", 0.65), "tilt": ("fix3", "TILT", 0.92),
            "map": ("break4", "MAP", 0.2), "where": ("break4", "WHERE", 0.7), "exactly": ("break4", "EXACTLY", 0.6),
            "sats": ("fix4", "SATELLITES", 0.1), "twenty": ("fix4", "TWENTY", 0.2), "clocks": ("fix4", "CLOCKS", 0.45),
            "einstein": ("fix4", "EINSTEIN", 0.58), "drifts": ("fix4", "DRIFTS", 0.8), "ten": ("fix4", "TEN", 0.88),
            "follow": ("cta", "FOLLOW", 0.35),
            "camera": ("reveal", "CAMERA", 0.15), "fifteen": ("reveal", "FIFTEEN", 0.35), "one": ("reveal", "ONE", 0.5),
            "dark": ("reveal", "DARK", 0.6), "pocket": ("reveal", "POCKET", 0.92),
            "s1": ("stat", "NINETEEN", 0.04), "s2": ("stat", "FIFTEEN", 0.35), "s3": ("stat", "SATELLITES", 0.6),
            "cong2": ("closer", "CONGRATS", 0.16),
            "mom": ("tag", "MOM", 0.1), "always": ("tag", "ALWAYS", 0.35), "sends": ("tag", "SENDS", 0.6),
            "twenty_t": ("tag", "TWENTY", 0.7), "flower": ("tag", "FLOWER", 0.9)})
        T["pull"] = max(0.9, min(T["computer"], T["moon"]) - 0.3)
        T["shrink0"] = min(T["shrink"], T["chip"]) - 0.1
        T["tap"] = max(s("break2") + 0.25, min(T["glass"], T["feel"]) - 0.1)
        T["touch"] = max(T["steals"] - 0.25, T["grid"] + 0.5)
        T["turn"] = s("break3") + 0.1
        T["fix3up"] = max(T["tilt"] - 0.4, T["springs"] + 0.3)
        T["burst"] = max(T["fifteen"] - 0.1, s("reveal") + 0.2)
        T["merge"] = max(min(T["one"], T["dark"]) - 0.1, T["burst"] + 0.9)
        T["pk"] = max(T["pocket"] - 0.5, T["merge"] + 0.6)
        T["fl0"] = min(T["sends"], T["twenty_t"]) - 0.1
        # ---- sets
        self.cut(s("break1") - 0.12, "brick", 1)
        self.cut(s("break2") - 0.12, "screen", -1)
        self.cut(s("fix4") - 0.12, "space", 1)
        self.cut(s("reveal") - 0.12, "night", -1)
        self.cut(s("stat") - 0.12, "moon", 1)
        self.cut(s("tag") - 0.2, "mom", 1)
        # ---- cameras (moon world: ground y = 0, the giant phone stands at x = 170)
        cm = Camera(170, -430, 1.25)
        cm.key(0.05, 170, -430, 1.22, 1.0)
        cm.key(T["pull"], 20, -330, 0.92, 1.3)
        cm.key(T["cat"] - 0.2, 120, -420, 1.08, 1.2)
        cm.key(s("stat") - 0.12, 60, -470, 0.78, 0.0).key(s("stat"), 70, -470, 0.8, 3.0)
        cm.key(s("closer") - 0.1, 140, -240, 0.85, 1.0)
        self.cam = cm
        self.turn = Track(0.0).to(T["turn"], -90.0, 0.7).to(s("break4") - 0.12, 0.0, 0.0)
        self.upright = Track(0.0).to(T["fix3up"], 90.0, 0.6).to(s("break4") - 0.12, 0.0, 0.0)
        self.tilt = Track(0.0).to(T["rice"], 0.0, 0.0).to(T["springs"], -1.0, 0.5).to(T["springs"] + 0.7, 1.0, 0.7)
        self.tilt.to(T["tilt"], -1.0, 0.6)
        self.drift = Track(0.0).to(T["drifts"] - 0.2, 1.0, 0.8).to(T["ten"] + 0.9, 0.0, 0.5)
        self.spans = [(T["talked"], T["billion"] + 0.3), (T["finger"], T["touches"] + 0.3), (T["holding"], T["tilt"] + 0.3),
                      (T["where"], T["ten"] + 0.3)]
        self.shakes = [(T["congrats"], 0.3, 8), (T["kilo"], 0.35, 8), (T["tap"] + 0.1, 0.25, 5), (T["touch"], 0.25, 4),
                       (T["turn"] + 0.6, 0.3, 5), (T["merge"], 0.3, 6), (s("closer") + 0.2, 0.35, 10)]
        rng = random.Random(35)
        self.craters = [(rng.uniform(-1400, 1600), rng.uniform(20, 900), rng.uniform(40, 160)) for _ in range(18)]
        self.stars_ = [(rng.uniform(0, W), rng.uniform(0, H * 0.7), rng.uniform(1, 3)) for _ in range(140)]

    # ------------------------------------------------------------------ helpers
    def at(self, cam, x, y):
        return self.to_screen(cam, x, y)

    def starfield(self, c, t, a=1.0):
        for (x, y, r) in self.stars_:
            c.drawCircle(x, y, r, P("#FFFFFF", a * (0.5 + 0.5 * math.sin(t * 2 + x))))

    # ------------------------------------------------------------------ set: moon (hook, stat, closer)
    def draw_moon(self, c, t):
        T, s = self.T, self.tl.s
        cam = self.cam.at(t)
        cx, cy, z = cam
        vrect(c, 0, 0, W, H, ["#000000", "#03050F", "#0A0F24"])
        self.starfield(c, t)
        earth(c, 220 - cx * 0.05, 330 - cy * 0.03, 92, spin=t * 0.02)
        self.view(c, cam)
        gp = skia.Path()
        gp.moveTo(-2000, -60)
        for k in range(21):
            gp.lineTo(-2000 + k * 200, -60 - 30 * math.sin(k * 1.7) - 20)
        gp.lineTo(2400, 3000)
        gp.lineTo(-2000, 3000)
        gp.close()
        c.drawPath(gp, lin_paint(0, -100, 0, 900, ["#9CA3AF", "#6B7280", "#374151", "#1F2937"]))
        for (x, y, r) in self.craters:
            c.drawOval(R(x - r, y - r * 0.3, 2 * r, r * 0.6), P("#4B5563", 0.8))
            c.drawOval(R(x - r * 0.9, y - r * 0.24, 1.8 * r, r * 0.42), P("#374151", 0.8))
        lander(c, -330, -40, 0.95)
        for i in range(4):                                                            # bootprints
            c.drawOval(R(-150 + i * 70, 30 + (i % 2) * 22, 34, 14), P("#374151", 0.9))
        contact_shadow(c, 190, 4, 520, 0.6)
        meow = bump(t, T["cat"], T["cat"] + 0.6) if t < s("break1") else 0.0
        glow = prog(t, s("closer"), s("closer") + 0.5) if t >= s("closer") - 0.1 else 0.0
        phone(c, 190, -440, 860, t, "cat", meow=meow, glow=glow + 0.4)
        if t >= s("closer") - 0.1:
            add_glow(c, 190, -440, 800, CYAN, 0.12 * prog(t, s("closer"), s("closer") + 0.6))
        c.restore()
        self.ui["cam"] = cam

    def ui_moon(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw >= s("break1"):
            return
        cam = self.ui.get("cam", self.cam.at(tw))
        lx, ly = self.at(cam, -330, -300)
        self.label(lx, ly, 280, 600, "apollo", T["computer"] - 0.15, T["cat"] - 0.2, GOLD, size=34)
        self.chip(280, 690, "kb", T["computer"] + 0.2, T["cat"] - 0.2, accent="#94A3B8", size=30)
        self.chip(560, 470, "times", T["million"] - 0.1, s("break1") + 0.1, accent=HILITE, size=38)
        px, py = self.at(cam, 190, -300)
        self.label(px, py, 780, 1150, "cats", T["cat"] - 0.1, s("break1") + 0.1, "#FBCFE8", size=34)

    # ------------------------------------------------------------------ set: brick (break1, fix1)
    def draw_brick(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#0B1026", "#151B3B", "#0B1026"])
        light_cone(c, 540, -60, 90, 1300, 26, "#FFF1C9", 0.18)
        c.drawOval(R(140, 1150, 800, 90), P("#000000", 0.45, blur=20))
        k = prog(t, T["shrink0"], T["shrink0"] + 0.7) if t >= s("fix1") - 0.12 else 0.0
        bh = 820 * (1 - 0.85 * e_in(k))
        brick(c, 540, 760 + 40 * k, bh, a=1 - prog(k, 0.6, 1.0))
        if t < s("fix1") - 0.12:
            wt = prog(t, T["kilo"] - 0.2, T["kilo"] + 0.2)
            if wt > 0:
                c.drawRRect(rr(330, 1150, 420, 40, 14), P("#94A3B8", wt))
        if k > 0.6:
            ca = prog(k, 0.6, 1.0)
            zoom = prog(t, T["billion"] - 0.6, T["billion"] + 0.6)
            chip(c, 540, 760, 150 + 120 * zoom, t, zoom=zoom, a=ca, glow=prog(t, T["billion"] - 0.2, T["billion"] + 0.3))
            fa = prog(t, T["nail"] - 0.3, T["nail"]) * (1 - prog(t, T["billion"] - 0.4, T["billion"] - 0.1))
            finger(c, 790, 830, 1.0, ang=-150, a=fa)

    def ui_brick(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix1") - 0.12:
            self.chip(540, 470, "first", T["first"] - 0.1, s("fix1") - 0.15, accent="#E7E5E4", size=36)
            self.chip(250, 1180, "kilo", T["kilo"] - 0.1, s("fix1") - 0.15, accent=WARN, size=34)
            self.chip(830, 600, "charge", T["charged"] - 0.1, s("fix1") - 0.15, accent=HILITE, size=30)
            mini_clock(c, 830, 700, 44, tw * 30, self.span(T["charged"] - 0.1, s("fix1") - 0.15))
            self.chip(830, 860, "talk", T["talked"] - 0.1, s("fix1") - 0.15, accent=WARN, size=30)
            self.badge("alert", T["talked"] + 0.05, s("fix1") - 0.2, x=880, y=330)
            self.red(T["talked"] + 0.05, 1.5)
            return
        self.chip(540, 470, "shrink", T["shrink0"], T["nail"] - 0.1, accent=CYAN, size=40)
        self.chip(540, 470, "nail", T["nail"] - 0.1, T["billion"] - 0.1, accent="#FBD5C0", size=40)
        self.chip(540, 470, "switches", T["billion"] - 0.1, s("break2") - 0.15, accent=HILITE, size=40)
        self.badge("check", T["billion"] + 0.1, s("break2") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: screen (break2 .. break4)
    def draw_screen(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#111827", "#1E1B4B", "#0F172A"])
        add_glow(c, 540, 700, 700, "#6366F1", 0.25)
        px, py, ph = 540, 760, 980
        if t < s("fix2") - 0.12:
            content, hi = "apps", 5
        elif t < s("break4") - 0.12:
            content, hi = ("apps" if t < T["touch"] + 0.2 else "cat"), 5
        else:
            content, hi = "map", -1
        rot = self.turn.at(t) if s("break3") - 0.12 <= t < s("break4") - 0.12 else 0.0
        crot = self.upright.at(t) if s("fix3") - 0.12 <= t < s("break4") - 0.12 else 0.0
        sc = 1.0 - 0.18 * clamp(abs(rot) / 90.0)
        grid = prog(t, T["grid"] - 0.2, T["grid"] + 0.3) * (1 - prog(t, s("break3") - 0.5, s("break3") - 0.12)) \
            if s("fix2") - 0.12 <= t < s("break3") else 0.0
        c.save()
        c.translate(px, py)
        c.scale(sc, sc)
        c.translate(-px, -py)

        def inner(cc, sx, sy, sw, sh):
            if s("break4") - 0.12 <= t:                                                    # the lost pin
                q = (t - s("break4")) * 1.6
                spots = ((0.3, 0.35), (0.7, 0.55), (0.45, 0.75), (0.65, 0.3))
                i = int(q) % len(spots)
                j = (i + 1) % len(spots)
                f = e_io(q - int(q))
                xx = sx + sw * lerp(spots[i][0], spots[j][0], f)
                yy = sy + sh * lerp(spots[i][1], spots[j][1], f)
                pin(cc, xx, yy, 1.0, WARN, q=True)
        phone(c, px, py, ph, t, content, rot=rot, grid=grid, content_rot=crot, hi=hi, inner=inner)
        c.restore()
        # break2: the tap that does nothing; fix2: the touch that works
        if s("break2") - 0.12 <= t < s("break3") - 0.12:
            tip = (px + 70, py - 160)
            if t < s("fix2") - 0.12:
                down = bump(t, T["tap"], T["tap"] + 0.35)
                finger(c, tip[0] + 40 * (1 - down), tip[1] + 40 * (1 - down), 1.0, ang=-30, a=prog(t, s("break2"), s("break2") + 0.2))
                if t > T["tap"] + 0.2:
                    k = prog(t, T["tap"] + 0.2, T["tap"] + 0.5)
                    c.drawCircle(tip[0], tip[1], 30 + 50 * k, P(WARN, 0.8 * (1 - k), stroke=6))
            else:
                down = prog(t, T["touch"] - 0.3, T["touch"])
                finger(c, tip[0] + 60 * (1 - down), tip[1] + 60 * (1 - down), 1.0, ang=-30)
                if t >= T["touch"]:
                    add_glow(c, tip[0], tip[1], 90, CYAN, 0.8)
                    for i in range(8):
                        q = (t * 1.8 + i / 8.0) % 1.0
                        an = math.radians(i * 45)
                        r0 = 140 * (1 - q)
                        c.drawCircle(tip[0] + math.cos(an) * r0, tip[1] + math.sin(an) * r0, 7, P("#FDE047", 0.9))
        # fix3: the accelerometer inset
        if s("fix3") - 0.12 <= t < s("break4") - 0.12:
            ia = prog(t, T["chip3"] - 0.2, T["chip3"] + 0.2)
            if ia > 0:
                mx, my = 300, 520
                rk = prog(t, T["silicon"] - 0.3, T["silicon"])
                if rk < 1:
                    c.drawCircle(mx, my, 150, P("#0F172A", 0.9 * ia * (1 - rk)))
                    c.drawCircle(mx, my, 150, P("#E2E8F0", ia * (1 - rk), stroke=8))
                    rice(c, mx - 50, my + 10, 1.0, ia * (1 - rk))
                    c.drawRRect(rr(mx + 30, my - 18, 36, 36, 6), P("#111827", ia * (1 - rk)))
                    c.drawRRect(rr(mx + 34, my - 14, 28, 28, 4), P("#64748B", ia * (1 - rk)))
                if rk > 0:
                    mems(c, mx, my, 150, self.tilt.at(t), a=ia * rk)

    def ui_screen(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw < s("fix2") - 0.12:
            self.chip(540, 1190, "glass", T["glass"] - 0.1, s("fix2") - 0.15, accent=WARN, size=36)
            self.badge("alert", T["finger"] + 0.05, s("fix2") - 0.2, x=880, y=330)
            self.red(T["finger"] + 0.05, 1.3)
            return
        if tw < s("break3") - 0.12:
            self.chip(540, 1190, "grid", T["grid"] - 0.1, T["steals"] - 0.1, accent=CYAN, size=36)
            self.chip(540, 1190, "charge2", T["steals"] - 0.1, s("break3") - 0.15, accent="#FDE047", size=36)
            self.badge("check", T["touches"] + 0.1, s("break3") - 0.15, x=880, y=330)
            return
        if tw < s("fix3") - 0.12:
            self.chip(540, 1250 - 60, "which", T["idea"] - 0.15, s("fix3") - 0.15, accent=WARN, size=40)
            self.badge("alert", T["holding"] + 0.05, s("fix3") - 0.2, x=880, y=330)
            self.red(T["holding"] + 0.05, 1.3)
            return
        if tw < s("break4") - 0.12:
            self.chip(300, 720, "rice", T["rice"] - 0.1, T["silicon"] - 0.1, accent="#FEFCE8", size=32)
            self.chip(300, 720, "springs", T["silicon"] - 0.1, s("break4") - 0.15, accent="#38BDF8", size=32)
            self.badge("check", T["tilt"] + 0.1, s("break4") - 0.15, x=880, y=330)
            return
        self.chip(540, 1190, "where", T["map"] - 0.1, s("fix4") - 0.15, accent=WARN, size=40)
        self.badge("alert", T["where"] + 0.05, s("fix4") - 0.2, x=880, y=330)
        self.red(T["where"] + 0.05, 1.3)

    # ------------------------------------------------------------------ set: space (fix4, cta)
    def draw_space(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#000000", "#02040E", "#050A1E"])
        self.starfield(c, t, 0.8)
        ex, ey, er = 540, 1000, 300
        orb = 470
        c.drawOval(R(ex - orb, ey - orb * 0.82, 2 * orb, 2 * orb * 0.82), P("#334155", 0.8, stroke=3))
        earth(c, ex, ey, er, spin=t * 0.03)
        home = (ex + 40, ey - er + 8)
        sats = []
        for i in range(4):
            an = t * 0.18 + i * math.pi / 2 + 0.6
            sx_, sy_ = ex + math.cos(an) * orb, ey - math.sin(an) * orb * 0.82
            sats.append((sx_, sy_, math.sin(an)))
        for (sx_, sy_, up) in sats:
            if up > -0.2:
                k = prog(t, T["sats"] - 0.2, T["sats"] + 0.3)
                for j in range(3):
                    q = (t * 1.2 + j / 3.0) % 1.0
                    c.drawLine(lerp(sx_, home[0], q), lerp(sy_, home[1], q), lerp(sx_, home[0], min(1, q + 0.08)),
                               lerp(sy_, home[1], min(1, q + 0.08)), P("#FDE047", 0.8 * k, stroke=6))
            satellite(c, sx_, sy_, 1.2, math.degrees(math.atan2(home[1] - sy_, home[0] - sx_)) + 90, glow=0.5)
            ck = prog(t, T["clocks"] - 0.2, T["clocks"] + 0.2)
            if ck > 0 and up > -0.2:
                mini_clock(c, sx_ + 60, sy_ - 50, 26, t * 8, a=ck, ok=prog(t, T["einstein"], T["einstein"] + 0.4))
        dk = self.drift.at(t)
        pin(c, home[0] + dk * 260, home[1] - 4, 0.9, mix(GOOD, WARN, clamp(dk * 2)))
        if dk > 0.05:
            c.drawLine(home[0], home[1] + 10, home[0] + dk * 260, home[1] + 10, P(WARN, 0.9, stroke=6))
        add_glow(c, home[0], home[1], 60, GOOD, 0.5)
        self.ui["home"] = home
        self.ui["sat0"] = sats[0]

    def ui_space(self, c, t, tw):
        T, s = self.T, self.tl.s
        if tw >= s("cta") - 0.12:
            return
        self.chip(540, 470, "up", T["twenty"] - 0.15, T["clocks"] - 0.1, accent="#FDE047", size=40)
        self.chip(540, 470, "clock", T["clocks"] - 0.1, T["drifts"] - 0.2, accent=GOOD, size=36)
        self.chip(540, 470, "drift", T["drifts"] - 0.2, T["ten"] + 0.9, accent=WARN, size=36)
        self.chip(540, 470, "fixed", T["ten"] + 0.9, s("cta") - 0.15, accent=GOOD, size=40)
        self.badge("check", T["ten"] + 0.9, s("cta") - 0.15, x=880, y=330)

    # ------------------------------------------------------------------ set: night (reveal)
    def draw_night(self, c, t):
        T, s = self.T, self.tl.s
        vrect(c, 0, 0, W, H, ["#02030A", "#070B1C", "#0B1026"])
        skyline_night(c, -100, 1180, 1250, seed=7, hmin=200, hmax=520, lit=0.25, t=t)
        pk = prog(t, T["pk"], T["pk"] + 0.7)
        if pk > 0:
            pocket(c, 540, 1180, 600, a=1.0)
        py = 700 + e_in(pk) * 760
        bright = prog(t, T["merge"], T["merge"] + 0.4)

        def inner(cc, sx, sy, sw, sh):
            cc.drawRect(R(sx, sy, sw, sh), lin_paint(0, sy, 0, sy + sh, [mix("#05060B", "#38BDF8", bright),
                                                                         mix("#05060B", "#FDE68A", bright)]))
            rng = random.Random(int(t * 12))
            for i in range(int(90 * (1 - bright))):
                cc.drawCircle(sx + rng.uniform(0, sw), sy + rng.uniform(0, sh), 2.4, P("#94A3B8", 0.6))
            skyline_night(cc, sx - 40, sx + sw + 40, sy + sh * 0.8, seed=7, hmin=80, hmax=220, lit=0.3 + 0.5 * bright, t=t)
            cc.drawCircle(sx + sw * 0.75, sy + sh * 0.22, 30, P("#F1F5F9", 0.3 + 0.7 * bright))
        phone(c, 540, py, 820, t, "dark", inner=inner)
        if t < T["merge"] + 0.2:                                                          # fifteen shots fly in
            for i in range(15):
                st = T["burst"] + i * 0.05
                q = prog(t, st, st + 0.5)
                if q <= 0 or q >= 1:
                    continue
                an = math.radians(i * 24)
                ox = 540 + math.cos(an) * 520 * (1 - e_out(q))
                oy = 700 + math.sin(an) * 520 * (1 - e_out(q))
                c.drawRRect(rr(ox - 90, oy - 150, 180, 300, 16), P("#1E293B", 0.9 * (1 - q * 0.5)))
                c.drawRRect(rr(ox - 80, oy - 140, 160, 280, 12), P("#0F172A", 0.9))
        if pk > 0:
            pocket(c, 540, 1180, 600, a=1.0, front=True)

    def ui_night(self, c, t, tw):
        T, s = self.T, self.tl.s
        self.chip(540, 470, "fifteen", T["fifteen"] - 0.1, T["merge"], accent=HILITE, size=40)
        self.chip(540, 470, "one", T["merge"], T["pk"], accent=GOOD, size=40)
        self.chip(540, 470, "pocket", T["pk"], s("stat") - 0.15, accent="#93C5FD", size=40)

    # ------------------------------------------------------------------ set: mom (tag)
    def draw_mom(self, c, t):
        T = self.T
        room(c, 0, 0, W, 1250, wall="#3B2F4A", floor="#4A3B5C", t=t, lamp=True, lamp_x=300)
        vrect(c, 0, 1250, W, H - 1250, ["#4A3B5C", "#2E2440", "#1A1426"])
        couch(c, 300, 1250, 520)
        mom(c, 300, 1150, 330, t)
        c.save()
        c.translate(780, 840)
        c.rotate(6)
        c.translate(-780, -840)

        def inner(cc, sx, sy, sw, sh):
            cc.drawRect(R(sx, sy, sw, sh), P("#0B141A"))
            n = int(clamp((t - T["fl0"]) / 0.12, 0, 20)) if t >= T["fl0"] else 0
            for i in range(n):
                k = clamp((t - T["fl0"] - i * 0.12) / 0.2)
                yy = sy + sh - 120 - (n - 1 - i) * 150 * 0.62
                if yy < sy - 120:
                    continue
                flower_card(cc, sx + sw / 2 + (i % 2) * 20 - 10, yy, 0.62 * e_back(k), self.L["gm"])
        phone(c, 780, 840, 760, t, "black", inner=inner)
        c.restore()

    def ui_mom(self, c, t, tw):
        T = self.T
        k = self.span(T["mom"] - 0.05, self.duration + 1, 0.25, 0.1)
        if k > 0:
            bubble(c, 400, 560, self.L["mom"], k, tail_left=True, size=40)
        k2 = self.span(T["twenty_t"], self.duration + 1, 0.25, 0.1)
        if k2 > 0:
            v2.chip(c, 860, 1180, self.L["x20"], k2, accent="#F472B6", size=48)

    def whip_backdrop(self, c, t, m):
        vrect(c, 0, 0, W, H, ["#000000", "#050816", "#0A1232"])

    # ------------------------------------------------------------------ sound
    def sfx_events(self):
        T, s, e = self.T, self.tl.s, self.tl.e
        ev = [(0.05, sfx.whoosh(0.5, True, 60), -8), (T["memory"], sfx.beep(1500.0), -16), (T["computer"], sfx.beep(1100.0), -16),
              (T["cat"], sfx.pop(61), -10), (T["congrats"] + 0.1, sfx.sparkle(0.7, 9, 62), -9), (T["sp"], sfx.chime(), -9)]
        ev += [(s("break1") - 0.12, sfx.whoosh(0.4, True, 63), -4), (T["kilo"], sfx.thud(0.5), -6), (T["charged"], sfx.tick(), -10),
               (T["charged"] + 0.3, sfx.tick(), -10), (T["talked"] + 0.2, sfx.alarm(3, 820.0), -12)]
        ev += [(T["shrink0"], sfx.whoosh(0.6, False, 64), -8), (T["shrink0"] + 0.6, sfx.pop(65), -8), (T["nail"], sfx.click(66), -10),
               (T["billion"], sfx.sparkle(0.9, 14, 67), -10), (T["billion"] + 0.2, sfx.chime(), -6)]
        ev += [(s("break2") - 0.12, sfx.whoosh(0.4, False, 68), -4), (T["tap"] + 0.15, sfx.tap(69), -6), (T["tap"] + 0.4, sfx.buzz(0.3), -12)]
        ev += [(T["grid"], sfx.sparkle(0.6, 8, 70), -12), (T["touch"], sfx.tap(71), -6), (T["touch"] + 0.1, sfx.pop(72), -10),
               (T["touches"] + 0.1, sfx.chime(), -6)]
        ev += [(T["turn"], sfx.whoosh(0.5, True, 73), -10), (T["holding"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(T["chip3"], sfx.pop(74), -8), (T["silicon"], sfx.click(75), -10), (T["fix3up"], sfx.whoosh(0.4, False, 76), -10),
               (T["tilt"] + 0.1, sfx.ding(), -8)]
        ev += [(T["map"], sfx.pop(77), -10), (T["where"] + 0.1, sfx.alarm(3, 820.0), -12)]
        ev += [(s("fix4") - 0.12, sfx.whoosh(0.45, True, 78), -4), (T["sats"], sfx.beep(1800.0), -14), (T["clocks"], sfx.tick(), -10),
               (T["einstein"], sfx.sparkle(0.6, 9, 79), -10), (T["drifts"], sfx.womp(), -10), (T["ten"] + 0.9, sfx.ding(), -8),
               (T["ten"] + 1.1, sfx.chime(), -6)]
        ev += [(T["pause"], sfx.click(80), 0), (T["follow"] - 0.15, sfx.pop(81), -4)]
        ev += [(s("reveal") - 0.12, sfx.whoosh(0.45, False, 82), -6), (T["burst"], sfx.riser(0.8, 83), -12),
               (T["merge"], sfx.snap(84), -6), (T["pk"] + 0.3, sfx.whoosh(0.5, False, 85), -10)]
        ev += [(s("stat") - 0.12, sfx.whoosh(0.45, True, 86), -6), (T["s1"], sfx.pop(87), -3), (T["s2"], sfx.pop(88), -3),
               (T["s3"], sfx.pop(89), -3)]
        ev += [(T["cong2"], sfx.pop(90), -2), (T["cong2"], sfx.sparkle(1.0, 14, 91), -4), (e("closer") - 0.4, sfx.chime(), -6)]
        ev += [(s("tag") - 0.2, sfx.whoosh(0.45, True, 92), -6), (T["mom"], sfx.pop(93), -8)]
        for i in range(8):
            ev.append((T["fl0"] + i * 0.24, sfx.beep(1300.0 + 80 * i, 0.06), -18))
        return ev


NAME = "phone"
EPISODE = Phone
