"""Overlays and effects. Functions say whether they draw in screen or world space."""
import math
import random
import skia
from .core import clamp, lerp, e_back, e_out, prog
from .draw import C, P, R, rect, circle, poly, line, glow, text, text_width, grad_rect

RED, GREEN, WHITE, YELLOW = "#EF4444", "#22C55E", "#FFFFFF", "#FFD43B"


def dim(c, W, H, a, color="#000814"):
    if a > 0:
        rect(c, 0, 0, W, H, color, a)


def red_vignette(c, W, H, a):
    """Screen space: red glow creeping in from the edges."""
    if a <= 0:
        return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.75,
                                               [C(RED, 0), C(RED, 0), C(RED, 0.55 * a)], [0.0, 0.55, 1.0]))
    c.drawRect(R(0, 0, W, H), p)


def flash(c, W, H, a, color=WHITE):
    if a > 0:
        rect(c, 0, 0, W, H, color, a)


def check_badge(c, x, y, p, size=1.0):
    """Green check that pops in. p: 0..1 progress of the pop (hold at 1)."""
    if p <= 0:
        return
    s = e_back(clamp(p)) * size
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    circle(c, 0, 6, 46, "#000000", 0.25, blur=8)
    circle(c, 0, 0, 46, GREEN)
    circle(c, 0, 0, 46, WHITE, stroke=7)
    pts = [(-20, 2), (-6, 16), (22, -14)]
    path = skia.Path()
    path.moveTo(*pts[0])
    path.lineTo(*pts[1])
    path.lineTo(*pts[2])
    c.drawPath(path, P(WHITE, 1, stroke=10))
    c.restore()


def alert_badge(c, x, y, p, size=1.0, t=0.0):
    if p <= 0:
        return
    s = e_back(clamp(p)) * size * (1 + 0.06 * math.sin(t * 14))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    circle(c, 0, 6, 44, "#000000", 0.25, blur=8)
    circle(c, 0, 0, 44, RED)
    circle(c, 0, 0, 44, WHITE, stroke=7)
    rect(c, -6, -26, 12, 32, WHITE, r=6)
    circle(c, 0, 18, 7, WHITE)
    c.restore()


def outline(c, x, y, w, h, p, color=WHITE, r=18, width=9, pad=14, a=1.0):
    """Highlight box around a world rect; p animates the pop (0..1), a fades it."""
    if p <= 0 or a <= 0:
        return
    k = lerp(1.25, 1.0, e_out(clamp(p * 1.6)))
    cx, cy = x + w / 2, y + h / 2
    ww, hh = (w + pad * 2) * k, (h + pad * 2) * k
    al = clamp(p * 3) * a
    rect(c, cx - ww / 2, cy - hh / 2, ww, hh, "#000000", 0.25 * al, r=r, stroke=width + 6)
    rect(c, cx - ww / 2, cy - hh / 2, ww, hh, color, al, r=r, stroke=width)


def red_glow_rect(c, x, y, w, h, a, t=0.0):
    if a <= 0:
        return
    pulse = 0.65 + 0.35 * math.sin(t * 12)
    rect(c, x - 10, y - 10, w + 20, h + 20, RED, 0.35 * a * pulse, r=16, blur=14)
    rect(c, x - 6, y - 6, w + 12, h + 12, RED, a * pulse, r=12, stroke=7)


def pause_icon(c, W, H, p, t=0.0):
    """Screen space: big 'video paused' icon."""
    if p <= 0:
        return
    s = e_back(clamp(p * 1.4))
    al = clamp(p * 4)
    c.save()
    c.translate(W / 2, H * 0.40)
    c.scale(s, s)
    circle(c, 0, 0, 150, "#000000", 0.45 * al)
    rect(c, -52, -68, 36, 136, WHITE, al, r=10)
    rect(c, 16, -68, 36, 136, WHITE, al, r=10)
    c.restore()


def cta_pill(c, W, label, sub, p, y=210):
    """Screen space pill near the top: 'FOLLOW' + 'next: ...'."""
    if p <= 0:
        return
    s = e_back(clamp(p))
    w = max(text_width(label, 64, "Poppins-Black") + text_width(sub, 44, "Poppins-SemiBold") + 210, 600)
    c.save()
    c.translate(W / 2, y)
    c.scale(s, s)
    rect(c, -w / 2, -66 + 10, w, 132, "#000000", 0.35, r=66, blur=12)
    rect(c, -w / 2, -66, w, 132, "#FF4D2E", 1.0, r=66)
    rect(c, -w / 2 + 14, -52, 104, 104, WHITE, 1.0, r=52)
    # plus sign in the circle
    rect(c, -w / 2 + 14 + 32, -6, 40, 12, "#FF4D2E", r=6)
    rect(c, -w / 2 + 14 + 46, -20, 12, 40, "#FF4D2E", r=6)
    x = -w / 2 + 140
    text(c, label, x, 22, 64, WHITE, "Poppins-Black", align="left")
    text(c, sub, x + text_width(label, 64, "Poppins-Black") + 22, 18, 44, "#FFE7DF", "Poppins-SemiBold", align="left")
    c.restore()


def confetti(c, W, H, t, t0, dur=2.6, seed=5, n=90):
    """Screen space burst from the top center."""
    if t < t0 or t > t0 + dur + 1.0:
        return
    rng = random.Random(seed)
    cols = ["#FFD43B", "#FF6B6B", "#4DABF7", "#69DB7C", "#DA77F2", "#FFA94D", WHITE]
    tt = t - t0
    for i in range(n):
        ang = rng.uniform(-math.pi * 0.95, -math.pi * 0.05)
        sp = rng.uniform(900, 1900)
        vx, vy = math.cos(ang) * sp * 0.6, math.sin(ang) * sp
        x = W / 2 + rng.uniform(-80, 80) + vx * tt
        y = H * 0.30 + vy * tt + 1500 * tt * tt
        if y > H + 50:
            continue
        rot = rng.uniform(0, 360) + tt * rng.uniform(200, 700)
        a = clamp(1 - prog(tt, dur - 0.6, dur))
        c.save()
        c.translate(x, y)
        c.rotate(rot)
        w, h = rng.uniform(12, 22), rng.uniform(22, 36)
        rect(c, -w / 2, -h / 2, w, h * abs(math.cos(math.radians(rot * 1.7))) + 4, cols[i % len(cols)], a, r=3)
        c.restore()


def sparks(c, x, y, t, t0, dur=0.7, seed=9, n=14, size=1.0):
    """World space: hot sparks flying off a point."""
    if t < t0 or t > t0 + dur:
        return
    rng = random.Random(seed)
    tt = t - t0
    for i in range(n):
        ang = rng.uniform(-math.pi, 0)
        sp = rng.uniform(250, 650) * size
        px = x + math.cos(ang) * sp * tt
        py = y + math.sin(ang) * sp * tt + 900 * tt * tt * size
        a = 1 - tt / dur
        line(c, px, py, px - math.cos(ang) * 22 * size, py - math.sin(ang) * 22 * size, "#FFD43B", 5 * size, a)
        circle(c, px, py, 4 * size, "#FFF3BF", a)


def speed_lines(c, x, y, w, h, a, t=0.0, up=True):
    """World space: streaks above (falling object) or below (rising object)."""
    if a <= 0:
        return
    rng = random.Random(1)
    for i in range(7):
        lx = x + w * (0.08 + 0.84 * i / 6)
        ln = rng.uniform(80, 200)
        off = (t * 900 + rng.uniform(0, 200)) % 220
        y0 = (y - 40 - off) if up else (y + h + 40 + off)
        line(c, lx, y0, lx, y0 - ln if up else y0 + ln, WHITE, 6, a * 0.75)


def stat_badge(c, x, y, big, small, p, color="#111827"):
    """Screen space: big number + small label, pops in."""
    if p <= 0:
        return
    s = e_back(clamp(p))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    w = max(text_width(big, 110, "Poppins-Black"), text_width(small, 40, "Poppins-Bold")) + 70
    rect(c, -w / 2, -95 + 10, w, 190, "#000000", 0.3, r=34, blur=10)
    rect(c, -w / 2, -95, w, 190, WHITE, 1.0, r=34)
    text(c, big, 0, 20, 110, color, "Poppins-Black")
    text(c, small, 0, 72, 40, "#6B7280", "Poppins-Bold")
    c.restore()
