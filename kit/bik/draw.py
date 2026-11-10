"""Thin Skia helpers: colors, paints, shapes, text."""
import os
import skia
from .core import clamp

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
_TYPEFACES = {}


def hexrgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def C(color, a=1.0):
    r, g, b = hexrgb(color)
    return skia.ColorSetARGB(int(round(clamp(a) * 255)), r, g, b)


def mix(c1, c2, t):
    t = clamp(t)
    a, b = hexrgb(c1), hexrgb(c2)
    return "#%02x%02x%02x" % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def shade(c, k):
    """k < 0 darkens toward black, k > 0 lightens toward white."""
    return mix(c, "#000000", -k) if k < 0 else mix(c, "#ffffff", k)


def P(color="#000000", a=1.0, stroke=None, blur=0.0, cap="round"):
    p = skia.Paint(AntiAlias=True, Color=C(color, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur > 0:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def R(x, y, w, h):
    return skia.Rect.MakeXYWH(x, y, w, h)


def rect(c, x, y, w, h, color, a=1.0, r=0, stroke=None, blur=0.0):
    if a <= 0:
        return
    p = P(color, a, stroke, blur)
    if r:
        c.drawRRect(skia.RRect.MakeRectXY(R(x, y, w, h), r, r), p)
    else:
        c.drawRect(R(x, y, w, h), p)


def grad_rect(c, x, y, w, h, c0, c1, a=1.0, r=0, horizontal=False):
    if a <= 0:
        return
    p = skia.Paint(AntiAlias=True)
    pts = [skia.Point(x, y), skia.Point(x + w, y)] if horizontal else [skia.Point(x, y), skia.Point(x, y + h)]
    p.setShader(skia.GradientShader.MakeLinear(pts, [C(c0, a), C(c1, a)]))
    if r:
        c.drawRRect(skia.RRect.MakeRectXY(R(x, y, w, h), r, r), p)
    else:
        c.drawRect(R(x, y, w, h), p)


def grad_stops(c, x, y, w, h, colors, positions, a=1.0):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + h)],
                                               [C(col, a) for col in colors], positions))
    c.drawRect(R(x, y, w, h), p)


def grad_alpha(c, x, y, w, h, color, a0, a1, horizontal=False):
    """One colour fading from alpha a0 to a1 (top to bottom, or left to right)."""
    p = skia.Paint(AntiAlias=True)
    p1 = skia.Point(x + w, y) if horizontal else skia.Point(x, y + h)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, y), p1], [C(color, a0), C(color, a1)]))
    c.drawRect(R(x, y, w, h), p)


def glow(c, x, y, rad, color, a=1.0):
    """Soft radial glow."""
    if a <= 0 or rad <= 0:
        return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), rad, [C(color, a), C(color, 0)]))
    c.drawCircle(x, y, rad, p)


def circle(c, x, y, rad, color, a=1.0, stroke=None, blur=0.0):
    if a <= 0 or rad <= 0:
        return
    c.drawCircle(x, y, rad, P(color, a, stroke, blur))


def poly(c, pts, color, a=1.0, stroke=None, close=True, blur=0.0):
    if a <= 0 or len(pts) < 2:
        return
    path = skia.Path()
    path.moveTo(*pts[0])
    for pt in pts[1:]:
        path.lineTo(*pt)
    if close:
        path.close()
    c.drawPath(path, P(color, a, stroke, blur))


def line(c, x0, y0, x1, y1, color, w=4, a=1.0, cap="round"):
    if a <= 0:
        return
    c.drawLine(x0, y0, x1, y1, P(color, a, stroke=w, cap=cap))


def dashed(c, x0, y0, x1, y1, color, w=4, dash=16, gap=10, phase=0.0, a=1.0):
    if a <= 0:
        return
    p = P(color, a, stroke=w)
    p.setPathEffect(skia.DashPathEffect.Make([dash, gap], phase))
    c.drawLine(x0, y0, x1, y1, p)


def shadow(c, x, y, w, h, r=14, a=0.22, blur=14, dy=10):
    rect(c, x, y + dy, w, h, "#000000", a, r=r, blur=blur)


def typeface(name):
    if name not in _TYPEFACES:
        _TYPEFACES[name] = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, name + ".ttf"))
    return _TYPEFACES[name]


def font(name, size):
    f = skia.Font(typeface(name), size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def text_width(s, size, fontname="Poppins-Bold"):
    return font(fontname, size).measureText(s)


def text(c, s, x, y, size, color, fontname="Poppins-Bold", align="center", a=1.0,
         stroke_color=None, stroke_w=0, shadow_a=0.0):
    """Draw text with its baseline at y. align: left/center/right."""
    if a <= 0 or not s:
        return
    f = font(fontname, size)
    w = f.measureText(s)
    x0 = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    if shadow_a > 0:
        sp = P("#000000", shadow_a * a, blur=size * 0.08)
        c.drawString(s, x0, y + size * 0.06, f, sp)
    if stroke_color and stroke_w > 0:
        c.drawString(s, x0, y, f, P(stroke_color, a, stroke=stroke_w))
    c.drawString(s, x0, y, f, P(color, a))
