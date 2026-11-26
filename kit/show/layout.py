"""Screen layer of the 4-minute show ("Survival Mode"): the game HUD over a build, level cards, the level-clear panel,
the cold open and the results card. Drawn with the kit's own helpers so it matches the builds."""
import math
import random
import skia

from bik.core import prog, clamp, lerp, e_out, e_back
from bik.draw import text as _text, text_width as _text_width, P, R, C
from bik.arabic import is_ar, text_ar, width_ar
from bik import v2, fx
from bik.v2 import rr, lin_paint, rad_paint, glass, add_glow, stat_card, HILITE, WARN, GOOD, ACCENT, INK

W, H = 1080, 1920
NAVY, DEEP = "#0B1220", "#05070F"
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
AR_FONT = {"Poppins-Black": "Tajawal-Black", "Poppins-ExtraBold": "Tajawal-ExtraBold", "Poppins-Bold": "Tajawal-Bold",
           "Poppins-SemiBold": "Tajawal-Bold"}

# Every word the layer shows. build_show.py replaces these per episode and language (set_strings); the defaults are
# episode 1 in English, so build_survival.py still draws what it always drew.
T = dict(chip="SURVIVAL MODE  ·  ZERO ELECTRICITY", lv="LV {n}", level="LEVEL {n}", final="FINAL LEVEL", boss="BOSS",
         defeated="DEFEATED", clear="CLEAR!", unlocked="ACHIEVEMENT UNLOCKED", score="SCORE", title1="SURVIVAL", title2="MODE",
         ribbon="ZERO ELECTRICITY", ribbon_icon="bolt", ribbon_crossed=True, sub="4 LEVELS  ·  4 BOSSES", press="PRESS START",
         world_clear="WORLD CLEAR!", row="LV {n}", result_label="POWER USED", result_value="0 W", rank="RANK S",
         all_levels="ALL 4 LEVELS", on_youtube="ON YOUTUBE", subscribe="SUBSCRIBE", or_boss="or the boss wins",
         no_icons=["bolt", "flame", "signal"], rtl=False)


def set_strings(d):
    T.update(d)


def text(c, s, x, y, size, color, font="Poppins-Bold", **kw):
    """The kit's text, in either script: Arabic goes through the shaper with the matching Tajawal weight."""
    if is_ar(s):
        return text_ar(c, s, x, y, size * 1.04, color, AR_FONT.get(font, "Tajawal-Black"), **kw)
    return _text(c, s, x, y, size, color, font, **kw)


def text_width(s, size, font="Poppins-Bold"):
    return width_ar(s, size * 1.04, AR_FONT.get(font, "Tajawal-Black")) if is_ar(s) else _text_width(s, size, font)


def side(left, right):
    """(x, align) for a block that hugs the left edge in English and the right edge in Arabic."""
    return (right, "right") if T["rtl"] else (left, "left")


# ------------------------------------------------------------------ pictures
def draw_img(c, img, zoom=1.0, cx=0.5, cy=0.5, a=1.0, dim=0.0):
    """Cover the frame with img, zoomed about (cx, cy)."""
    w, h = W * zoom, H * zoom
    dst = skia.Rect.MakeXYWH(-(w - W) * cx, -(h - H) * cy, w, h)
    p = skia.Paint(AntiAlias=True)
    if a < 1:
        p.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), dst, LIN, p)
    if dim > 0:
        c.drawRect(R(0, 0, W, H), P(DEEP, dim))


def blurred(img, sigma=14.0, dim=0.5, tint=None):
    """A soft, darkened copy of a frame: the backdrop of cards and panels."""
    s = skia.Surface(W, H)
    c = s.getCanvas()
    p = skia.Paint()
    p.setImageFilter(skia.ImageFilters.Blur(sigma, sigma))
    c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), skia.Rect.MakeXYWH(-50, -90, W + 100, H + 180), LIN, p)
    c.drawRect(R(0, 0, W, H), P(DEEP, dim))
    if tint:
        c.drawRect(R(0, 0, W, H), P(tint, 0.10))
    c.drawRect(R(0, 0, W, H), rad_paint(W / 2, H / 2, H * 0.72, [(DEEP, 0.0), (DEEP, 0.0), (DEEP, 0.55)], [0.0, 0.55, 1.0]))
    return s.makeImageSnapshot()


def quad(imgs, dim=0.55):
    """Four worlds as a 2 x 2 wall (title art, results card)."""
    s = skia.Surface(W, H)
    c = s.getCanvas()
    for i, im in enumerate(imgs[:4]):
        x, y = (i % 2) * W / 2, (i // 2) * H / 2
        c.save()
        c.clipRect(R(x, y, W / 2, H / 2))
        # the middle of each picture, a little enlarged, fills its quarter
        c.drawImageRect(im, skia.Rect.MakeXYWH(W * 0.18, H * 0.16, W * 0.64, H * 0.64), R(x, y, W / 2, H / 2), LIN, skia.Paint())
        c.restore()
    c.drawRect(R(W / 2 - 3, 0, 6, H), P(DEEP, 0.9))
    c.drawRect(R(0, H / 2 - 3, W, 6), P(DEEP, 0.9))
    c.drawRect(R(0, 0, W, H), P(DEEP, dim))
    c.drawRect(R(0, 0, W, H), rad_paint(W / 2, H / 2, H * 0.7, [(DEEP, 0.0), (DEEP, 0.0), (DEEP, 0.6)], [0.0, 0.5, 1.0]))
    return s.makeImageSnapshot()


def flash(c, a, col="#FFFFFF"):
    if a > 0:
        c.drawRect(R(0, 0, W, H), P(col, clamp(a)))


def fit(c, s, x, y, size, color, font="Poppins-Black", max_w=960, **kw):
    k = min(1.0, max_w / max(1.0, text_width(s, size, font)))
    if k < 1 and kw.get("stroke_w"):
        kw["stroke_w"] = kw["stroke_w"] * max(k, 0.5)             # a shrunk word keeps a matching outline
    text(c, s, x, y, size * k, color, font, **kw)
    return size * k


# ------------------------------------------------------------------ icons (unit box about 1 x 1, centred)
def _path(pts, s, close=True):
    p = skia.Path()
    p.moveTo(pts[0][0] * s, pts[0][1] * s)
    for x, y in pts[1:]:
        p.lineTo(x * s, y * s)
    if close:
        p.close()
    return p


def icon_bolt(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawPath(_path([(-0.10, -0.52), (0.30, -0.52), (0.08, -0.08), (0.34, -0.08), (-0.22, 0.56), (-0.04, 0.06), (-0.32, 0.06)], s), P(col, a))
    c.restore()


def icon_flame(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    for k, cc, dy in ((1.0, col, 0.0), (0.52, "#FFF1C9", 0.2)):
        p = skia.Path()
        p.moveTo(0, (-0.55 * k + dy) * s)
        p.cubicTo(0.52 * k * s, (-0.02 * k + dy) * s, 0.46 * k * s, (0.52 * k + dy) * s, 0, (0.52 * k + dy) * s)
        p.cubicTo(-0.46 * k * s, (0.52 * k + dy) * s, -0.52 * k * s, (-0.02 * k + dy) * s, 0, (-0.55 * k + dy) * s)
        c.drawPath(p, P(cc, a))
    c.restore()


def icon_signal(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    for i, hh in enumerate((0.26, 0.48, 0.72, 0.98)):
        bx = (-0.46 + i * 0.25) * s
        c.drawRRect(rr(bx, (0.5 - hh) * s, 0.18 * s, hh * s, 0.05 * s), P(col, a))
    c.restore()


def icon_person(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawCircle(0, -0.30 * s, 0.17 * s, P(col, a))
    c.drawRRect(rr(-0.21 * s, -0.08 * s, 0.42 * s, 0.58 * s, 0.18 * s), P(col, a))
    c.restore()


def icon_trophy(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    p = skia.Path()
    p.moveTo(-0.30 * s, -0.42 * s)
    p.lineTo(0.30 * s, -0.42 * s)
    p.cubicTo(0.30 * s, 0.06 * s, 0.14 * s, 0.18 * s, 0.07 * s, 0.20 * s)
    p.lineTo(0.07 * s, 0.34 * s)
    p.lineTo(0.22 * s, 0.34 * s)
    p.lineTo(0.22 * s, 0.46 * s)
    p.lineTo(-0.22 * s, 0.46 * s)
    p.lineTo(-0.22 * s, 0.34 * s)
    p.lineTo(-0.07 * s, 0.34 * s)
    p.lineTo(-0.07 * s, 0.20 * s)
    p.cubicTo(-0.14 * s, 0.18 * s, -0.30 * s, 0.06 * s, -0.30 * s, -0.42 * s)
    p.close()
    c.drawPath(p, P(col, a))
    for sx in (-1, 1):
        c.drawArc(skia.Rect.MakeXYWH(sx * 0.30 * s - 0.14 * s, -0.36 * s, 0.28 * s, 0.30 * s), -90 if sx > 0 else 90, 180, False,
                  P(col, a, stroke=0.07 * s))
    c.drawRRect(rr(-0.16 * s, -0.30 * s, 0.07 * s, 0.26 * s, 0.03 * s), P("#FFFFFF", 0.45 * a))
    c.restore()


def icon_drop(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    p = skia.Path()
    p.moveTo(0, -0.56 * s)
    p.cubicTo(0.10 * s, -0.30 * s, 0.40 * s, 0.00 * s, 0.40 * s, 0.20 * s)
    p.cubicTo(0.40 * s, 0.44 * s, 0.22 * s, 0.56 * s, 0, 0.56 * s)
    p.cubicTo(-0.22 * s, 0.56 * s, -0.40 * s, 0.44 * s, -0.40 * s, 0.20 * s)
    p.cubicTo(-0.40 * s, 0.00 * s, -0.10 * s, -0.30 * s, 0, -0.56 * s)
    c.drawPath(p, P(col, a))
    c.drawArc(skia.Rect.MakeXYWH(-0.24 * s, -0.02 * s, 0.44 * s, 0.44 * s), 100, 70, False, P("#FFFFFF", 0.55 * a, stroke=0.06 * s))
    c.restore()


def icon_gear(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    for i in range(8):
        c.save()
        c.rotate(i * 45)
        c.drawRRect(rr(-0.09 * s, -0.54 * s, 0.18 * s, 0.24 * s, 0.03 * s), P(col, a))
        c.restore()
    c.drawCircle(0, 0, 0.38 * s, P(col, a))
    c.drawCircle(0, 0, 0.15 * s, P(NAVY, a))
    c.restore()


def icon_brick(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    w, h, g = 0.44 * s, 0.26 * s, 0.05 * s
    for row, xs in ((-1, (-0.5, 0.5)), (0, (-1.0, 0.0, 1.0)), (1, (-0.5, 0.5))):
        for k in xs:
            c.save()
            c.clipRect(skia.Rect.MakeXYWH(-0.50 * s, -0.46 * s, 1.0 * s, 0.92 * s))
            c.drawRRect(rr(k * (w + g) - w / 2, row * (h + g) - h / 2, w, h, 0.04 * s), P(col, a))
            c.restore()
    c.restore()


def icon_land(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    p = skia.Path()
    p.moveTo(-0.52 * s, 0.24 * s)
    p.cubicTo(-0.34 * s, -0.30 * s, 0.34 * s, -0.30 * s, 0.52 * s, 0.24 * s)
    p.close()
    c.drawPath(p, P(col, a))
    c.drawRRect(rr(-0.56 * s, 0.30 * s, 1.12 * s, 0.10 * s, 0.05 * s), P(col, 0.75 * a))
    c.drawRRect(rr(-0.40 * s, 0.46 * s, 0.80 * s, 0.07 * s, 0.035 * s), P(col, 0.45 * a))
    c.restore()


def icon_wave(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    for k, yy in enumerate((-0.22, 0.06, 0.34)):
        p = skia.Path()
        p.moveTo(-0.52 * s, yy * s)
        for i in range(4):
            x0 = (-0.52 + 0.26 * i) * s
            p.cubicTo(x0 + 0.07 * s, (yy - 0.16) * s, x0 + 0.19 * s, (yy - 0.16) * s, x0 + 0.26 * s, yy * s)
        c.drawPath(p, P(col, a * (1.0, 0.8, 0.6)[k], stroke=0.10 * s))
    c.restore()


def icon_sun(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    for i in range(8):
        c.save()
        c.rotate(i * 45)
        c.drawRRect(rr(-0.045 * s, -0.56 * s, 0.09 * s, 0.18 * s, 0.045 * s), P(col, a))
        c.restore()
    c.drawCircle(0, 0, 0.28 * s, P(col, a))
    c.restore()


def icon_snow(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    for i in range(3):
        c.save()
        c.rotate(i * 60)
        c.drawRRect(rr(-0.045 * s, -0.54 * s, 0.09 * s, 1.08 * s, 0.045 * s), P(col, a))
        for sy in (-1, 1):
            for sx in (-1, 1):
                c.drawLine(0, sy * 0.34 * s, sx * 0.14 * s, sy * 0.48 * s, P(col, a, stroke=0.07 * s))
        c.restore()
    c.restore()


def icon_clock(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawCircle(0, 0, 0.46 * s, P(col, a, stroke=0.10 * s))
    c.drawLine(0, 0, 0, -0.28 * s, P(col, a, stroke=0.09 * s))
    c.drawLine(0, 0, 0.20 * s, 0.10 * s, P(col, a, stroke=0.09 * s))
    c.restore()


def icon_coin(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawCircle(0, 0, 0.48 * s, P(col, a))
    c.drawCircle(0, 0, 0.36 * s, P(NAVY, 0.35 * a, stroke=0.05 * s))
    c.drawRRect(rr(-0.05 * s, -0.24 * s, 0.10 * s, 0.48 * s, 0.05 * s), P(NAVY, 0.55 * a))
    c.restore()


def icon_boat(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawPath(_path([(-0.52, 0.12), (0.52, 0.12), (0.34, 0.44), (-0.34, 0.44)], s), P(col, a))
    c.drawRRect(rr(-0.04 * s, -0.52 * s, 0.08 * s, 0.62 * s, 0.03 * s), P(col, a))
    c.drawPath(_path([(0.08, -0.50), (0.46, 0.02), (0.08, 0.02)], s), P(col, a))
    c.drawPath(_path([(-0.08, -0.36), (-0.36, 0.02), (-0.08, 0.02)], s), P(col, 0.8 * a))
    c.restore()


def icon_bridge(c, x, y, s, col, a=1.0):
    c.save()
    c.translate(x, y)
    c.drawRRect(rr(-0.56 * s, -0.10 * s, 1.12 * s, 0.12 * s, 0.04 * s), P(col, a))
    for px in (-0.30, 0.30):
        c.drawRRect(rr((px - 0.05) * s, -0.46 * s, 0.10 * s, 0.92 * s, 0.03 * s), P(col, a))
    for x0, x1 in ((-0.56, -0.30), (-0.30, 0.30), (0.30, 0.56)):
        p = skia.Path()
        p.moveTo(x0 * s, (-0.44 if x0 > -0.5 else -0.12) * s)
        p.quadTo((x0 + x1) / 2 * s, (0.0 if (x0, x1) == (-0.30, 0.30) else -0.20) * s, x1 * s, (-0.44 if x1 < 0.5 else -0.12) * s)
        c.drawPath(p, P(col, a, stroke=0.06 * s))
    c.restore()


def icon_rock(c, x, y, s, col, a=1.0):
    """A boulder: solid ground."""
    c.save()
    c.translate(x, y)
    c.drawPath(_path([(-0.50, 0.40), (-0.42, -0.02), (-0.16, -0.40), (0.20, -0.44), (0.46, -0.10), (0.52, 0.40)], s), P(col, a))
    c.drawPath(_path([(-0.16, -0.40), (0.20, -0.44), (0.06, -0.06), (-0.30, 0.04), (-0.42, -0.02)], s), P("#FFFFFF", 0.30 * a))
    c.drawPath(_path([(0.06, -0.06), (0.16, 0.40)], s, close=False), P(NAVY, 0.35 * a, stroke=0.04 * s))
    c.restore()


def icon_flat(c, x, y, s, col, a=1.0):
    """Flat land: a little house on level ground."""
    c.save()
    c.translate(x, y)
    c.drawRRect(rr(-0.56 * s, 0.16 * s, 1.12 * s, 0.12 * s, 0.05 * s), P(col, a))
    c.drawRRect(rr(-0.44 * s, 0.34 * s, 0.88 * s, 0.08 * s, 0.04 * s), P(col, 0.6 * a))
    c.drawRect(skia.Rect.MakeXYWH(-0.38 * s, -0.12 * s, 0.44 * s, 0.28 * s), P(col, a))
    c.drawPath(_path([(-0.46, -0.10), (-0.16, -0.38), (0.14, -0.10)], s), P(col, a))
    c.drawRect(skia.Rect.MakeXYWH(-0.21 * s, 0.00 * s, 0.10 * s, 0.16 * s), P(NAVY, 0.55 * a))
    c.drawRRect(rr(0.29 * s, -0.10 * s, 0.05 * s, 0.26 * s, 0.02 * s), P(col, a))
    c.drawCircle(0.315 * s, -0.20 * s, 0.14 * s, P(col, a))
    c.restore()


def icon_down(c, x, y, s, col, a=1.0):
    """A heavy arrow pointing down: gravity."""
    c.save()
    c.translate(x, y)
    c.drawPath(_path([(-0.16, -0.52), (0.16, -0.52), (0.16, 0.02), (0.40, 0.02), (0.0, 0.54), (-0.40, 0.02), (-0.16, 0.02)], s), P(col, a))
    c.restore()


def icon_pause(c, x, y, s, col, a=1.0):
    """Two bars: the pause button."""
    c.save()
    c.translate(x, y)
    for bx in (-0.34, 0.10):
        c.drawRRect(rr(bx * s, -0.44 * s, 0.24 * s, 0.88 * s, 0.06 * s), P(col, a))
    c.restore()


def icon_rewind(c, x, y, s, col, a=1.0):
    """Two triangles pointing back: rewind."""
    c.save()
    c.translate(x, y)
    for dx in (-0.02, 0.50):
        c.drawPath(_path([(dx, -0.42), (dx, 0.42), (dx - 0.50, 0.0)], s), P(col, a))
    c.restore()


def icon_hourglass(c, x, y, s, col, a=1.0):
    """An hourglass with most of its sand already down: time running out."""
    c.save()
    c.translate(x, y)
    for by in (-0.54, 0.44):
        c.drawRRect(rr(-0.38 * s, by * s, 0.76 * s, 0.10 * s, 0.04 * s), P(col, a))
    c.drawPath(_path([(-0.30, -0.44), (0.30, -0.44), (0.05, 0.0), (0.30, 0.44), (-0.30, 0.44), (-0.05, 0.0)], s), P(col, a))
    c.drawPath(_path([(-0.21, -0.37), (0.21, -0.37), (0.12, -0.21), (-0.12, -0.21)], s), P(NAVY, 0.55 * a))      # the empty top
    c.drawPath(_path([(-0.02, 0.06), (0.02, 0.06), (0.17, 0.30), (-0.17, 0.30)], s), P(NAVY, 0.55 * a))          # air over the pile
    c.drawRRect(rr(-0.012 * s, -0.02 * s, 0.024 * s, 0.34 * s, 0.01 * s), P(col, a))                              # the falling sand
    c.restore()


def icon_umbrella(c, x, y, s, col, a=1.0):
    """A sun umbrella with a scalloped edge: shade (sm05, "No shade")."""
    c.save()
    c.translate(x, y)
    r, y0 = 0.52, -0.06
    top = [(r * math.cos(math.radians(d)), y0 + r * math.sin(math.radians(d))) for d in range(180, 361, 10)]
    bot = []
    for k in range(3):                                           # three scallops along the lower edge, right to left
        cx = r - (2 * k + 1) * r / 3
        bot += [(cx + (r / 3) * math.cos(math.radians(d)), y0 - 0.10 * math.sin(math.radians(d))) for d in range(0, 181, 20)]
    c.drawPath(_path(top + bot, s), P(col, a))
    c.drawRRect(rr(-0.035 * s, -0.63 * s, 0.07 * s, 0.12 * s, 0.03 * s), P(col, a))          # the tip
    c.drawRRect(rr(-0.03 * s, -0.12 * s, 0.06 * s, 0.54 * s, 0.03 * s), P(col, a))           # the pole
    hook = skia.Path()
    hook.moveTo(0, 0.40 * s)
    hook.arcTo(skia.Rect.MakeLTRB(-0.20 * s, 0.30 * s, 0.0, 0.52 * s), 0, 180, False)
    c.drawPath(hook, P(col, a, stroke=0.06 * s))                                             # the handle
    c.restore()


def icon_shortcut(c, x, y, s, col, a=1.0):
    """A straight arrow over a dotted long way round: the shortcut (sm06, "No shortcut")."""
    c.save()
    c.translate(x, y)
    for d in range(18, 163, 16):                                  # the long way round, as dots under the arrow
        rad = math.radians(d)
        c.drawCircle(0.47 * math.cos(rad) * s, (0.02 + 0.50 * math.sin(rad)) * s, 0.042 * s, P(col, 0.55 * a))
    c.drawPath(_path([(-0.54, -0.25), (0.14, -0.25), (0.14, -0.46), (0.56, -0.13), (0.14, 0.20), (0.14, -0.01), (-0.54, -0.01)], s), P(col, a))
    c.restore()


def icon_lighthouse(c, x, y, s, col, a=1.0):
    """A lighthouse throwing two beams: a light at sea (sm06, "No light")."""
    c.save()
    c.translate(x, y)
    for sx in (-1, 1):                                             # the beams
        c.drawPath(_path([(sx * 0.13, -0.27), (sx * 0.58, -0.46), (sx * 0.58, -0.10)], s), P(col, 0.50 * a))
    c.drawPath(_path([(-0.22, 0.46), (-0.115, -0.12), (0.115, -0.12), (0.22, 0.46)], s), P(col, a))               # the tower
    c.drawPath(_path([(-0.157, 0.10), (-0.189, 0.28), (0.189, 0.28), (0.157, 0.10)], s), P(NAVY, 0.50 * a))       # one dark band
    c.drawRRect(rr(-0.20 * s, -0.19 * s, 0.40 * s, 0.08 * s, 0.03 * s), P(col, a))                                # the gallery
    c.drawRect(skia.Rect.MakeXYWH(-0.10 * s, -0.37 * s, 0.20 * s, 0.19 * s), P(col, a))                           # the lamp room
    c.drawRect(skia.Rect.MakeXYWH(-0.055 * s, -0.33 * s, 0.11 * s, 0.11 * s), P("#FFF1C9", a))
    c.drawPath(_path([(-0.15, -0.37), (0.0, -0.55), (0.15, -0.37)], s), P(col, a))                                # the roof
    c.drawRRect(rr(-0.32 * s, 0.44 * s, 0.64 * s, 0.09 * s, 0.04 * s), P(col, a))                                 # the rock it stands on
    c.restore()


def no_sign(c, x, y, r, p, col=WARN):
    """Red ring with a slash, stamped on with a little overshoot."""
    if p <= 0:
        return
    k = lerp(1.6, 1.0, e_out(clamp(p)))
    a = clamp(p * 3)
    c.save()
    c.translate(x, y)
    c.scale(k, k)
    c.drawCircle(0, 0, r, P(col, a, stroke=r * 0.17))
    d = r * 0.70
    c.drawLine(-d, -d, d, d, P(col, a, stroke=r * 0.17, cap="butt"))
    c.restore()


def star(c, x, y, r, col, a=1.0):
    p = skia.Path()
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(x + rad * math.cos(ang), y + rad * math.sin(ang))
    p.close()
    c.drawPath(p, P(col, a))


def backdrop(c, t):
    c.drawRect(R(0, 0, W, H), lin_paint(0, 0, 0, H, ["#05081A", "#101542", "#2B2466"], [0.0, 0.6, 1.0]))
    v2.stars(c, W, H, t, a=0.8)
    c.drawRect(R(0, 0, W, H), rad_paint(W / 2, H * 0.42, H * 0.7, [(DEEP, 0.0), (DEEP, 0.0), (DEEP, 0.7)], [0.0, 0.5, 1.0]))


# ------------------------------------------------------------------ the HUD over a build
BAR_X, BAR_Y, BAR_W, BAR_H = 24, 100, 1032, 100


def hud_bar(c, lv, boss, hp, score, atk=0.0, hit=0.0, down=0.0, t=0.0, gain=None):
    """Top bar: level chip, boss name with its health bar (4 = full), score. atk / hit / down: 0..1 pulses.
    gain: (text, 0..1 progress) floating '+250' under the score."""
    sx = math.sin(t * 61) * 5 * atk
    c.save()
    c.translate(sx, 0)
    x, y, w, h = BAR_X, BAR_Y, BAR_W, BAR_H
    c.drawRRect(rr(x, y + 8, w, h, h / 2), P("#000000", 0.5, blur=14))
    c.drawRRect(rr(x, y, w, h, h / 2), lin_paint(x, y, x, y + h, ["#1A2547", NAVY]))
    c.drawRRect(rr(x + 1, y + 1, w - 2, h - 2, h / 2), P("#FFFFFF", 0.16, stroke=2))
    if atk > 0:
        c.drawRRect(rr(x + 1, y + 1, w - 2, h - 2, h / 2), P(WARN, 0.75 * atk, stroke=4))
    # level chip
    c.drawRRect(rr(x + 13, y + 13, 132, h - 26, (h - 26) / 2), lin_paint(x, y, x, y + h, ["#FFE066", HILITE]))
    fit(c, T["lv"].format(n=lv), x + 79, y + 66, 42, NAVY, max_w=110)
    # boss name
    nx = x + 166
    ncol = WARN if atk > 0.25 else INK
    nw = text_width(boss, 36, "Poppins-Black")
    text(c, boss, nx, y + 64, 36, ncol if down < 0.5 else "#8A93A8", "Poppins-Black", align="left")
    if down > 0:
        c.drawLine(nx - 4, y + 51, nx - 4 + (nw + 8) * clamp(down * 2), y + 51, P("#8A93A8", 1.0, stroke=5))
    # health bar
    bx = nx + nw + 24
    bw = (x + w - 210) - bx
    by, bh = y + 37, 26
    c.drawRRect(rr(bx, by, bw, bh, bh / 2), P("#FFFFFF", 0.14))
    fw = bw * clamp(hp / 4.0)
    if fw > 1:
        c.save()
        c.clipRRect(rr(bx, by, bw, bh, bh / 2), True)
        c.drawRect(R(bx, by, fw, bh), lin_paint(bx, 0, bx + bw, 0, ["#FF3B4E", "#FF8A3D"]))
        c.drawRect(R(bx, by, fw, bh * 0.42), P("#FFFFFF", 0.22))
        if hit > 0:
            c.drawRect(R(bx, by, bw, bh), P("#FFFFFF", 0.85 * hit))
        c.restore()
        if atk > 0:
            add_glow(c, bx + fw / 2, by + bh / 2, fw * 0.6 + 40, WARN, 0.5 * atk)
    for q in (1, 2, 3):
        c.drawRect(R(bx + bw * q / 4 - 2, by, 4, bh), P(NAVY, 0.9))
    if down > 0:
        k = e_back(clamp(down * 2.5))
        c.save()
        c.translate(bx + bw / 2, by + bh / 2 + 13)
        c.scale(k, k)
        text(c, T["defeated"], 0, 0, 34, GOOD, "Poppins-Black", stroke_color=NAVY, stroke_w=8)
        c.restore()
    # score
    star(c, x + w - 178, y + 50, 17, HILITE)
    text(c, f"{int(score):04d}", x + w - 28, y + 66, 42, HILITE, "Poppins-Black", align="right")
    c.restore()
    if gain and 0 < gain[1] < 1:
        p = gain[1]
        a = clamp(p * 6) * (1 - prog(p, 0.65, 1.0))
        text(c, gain[0], BAR_X + BAR_W - 96, BAR_Y + BAR_H + 62 - 34 * e_out(p), 46, GOOD, "Poppins-Black", a=a,
             stroke_color=NAVY, stroke_w=9, shadow_a=0.5)


# ------------------------------------------------------------------ level card
def level_dots(c, y, cur, a=1.0, t=0.0):
    for i in range(4):
        x = W / 2 + (i - 1.5) * 92
        if i + 1 < cur:
            c.drawCircle(x, y, 22, P(GOOD, a))
            pth = skia.Path()
            pth.moveTo(x - 10, y + 1)
            pth.lineTo(x - 3, y + 8)
            pth.lineTo(x + 11, y - 7)
            c.drawPath(pth, P("#FFFFFF", a, stroke=6))
        elif i + 1 == cur:
            add_glow(c, x, y, 60, HILITE, 0.5 * a * (0.6 + 0.4 * math.sin(t * 7)))
            c.drawCircle(x, y, 24, P(HILITE, a))
            text(c, str(i + 1), x, y + 12, 32, NAVY, "Poppins-Black", a=a)
        else:
            c.drawCircle(x, y, 20, P("#FFFFFF", 0.22 * a))


def level_card(c, lv, bg, t, dur, caps=None, tg=0.0):
    """lv: dict(n, world, boss, sub, color, final). bg: blurred picture of the level's world. t: seconds into the card."""
    draw_img(c, bg, zoom=1.06 + 0.05 * t / max(dur, 0.1))
    p0 = prog(t, 0.0, 0.25)
    v2.chip(c, W / 2, 330, T["chip"], p0, size=28)
    # LEVEL n
    p1 = prog(t, 0.05, 0.40)
    if p1 > 0:
        k = lerp(1.7, 1.0, e_back(p1))
        c.save()
        c.translate(W / 2, 640)
        c.scale(k, k)
        label = T["final"] if lv.get("final") else T["level"].format(n=lv["n"])
        add_glow(c, 0, -60, 420, HILITE, 0.22 * clamp(p1 * 2))
        fit(c, label, 0, 0, 176, HILITE, max_w=940, a=clamp(p1 * 3), stroke_color=DEEP, stroke_w=18, shadow_a=0.6)
        c.restore()
    p2 = prog(t, 0.28, 0.55)
    if p2 > 0:
        fit(c, lv["world"], W / 2, 790 + 30 * (1 - e_out(p2)), 94, INK, max_w=940, a=clamp(p2 * 2), stroke_color=DEEP, stroke_w=12,
            shadow_a=0.5)
    # boss panel
    p3 = prog(t, 0.55, 0.85)
    if p3 > 0:
        c.save()
        c.translate(0, 70 * (1 - e_back(p3)))
        a = clamp(p3 * 2)
        glass(c, 90, 880, 900, 290, r=40, a=a)
        c.drawRRect(rr(92, 882, 896, 286, 40), P(WARN, 0.55 * a, stroke=3))
        bx, al = side(130, 950)
        v2.chip(c, 890 if T["rtl"] else 190, 940, T["boss"], p3, fg="#FFFFFF", bg=WARN, size=30)
        fit(c, lv["boss"], bx, 1048, 96, INK, max_w=820, a=a, align=al)
        fit(c, lv["sub"], bx, 1100, 36, "#C9D3E6", "Poppins-Bold", max_w=820, a=a, align=al)
        hp = e_out(prog(t, 0.85, 1.65))
        c.drawRRect(rr(130, 1118, 820, 28, 14), P("#FFFFFF", 0.14 * a))
        if hp > 0:
            c.drawRRect(rr(130, 1118, max(28, 820 * hp), 28, 14), lin_paint(130, 0, 950, 0, ["#FF3B4E", "#FF8A3D"], None, a))
            add_glow(c, 130 + 820 * hp, 1132, 60, WARN, 0.6 * a * (1 - prog(t, 1.65, 1.9)))
        c.restore()
    level_dots(c, 1500, lv["n"], a=prog(t, 0.3, 0.6), t=t)
    if caps is not None:
        caps.draw(c, W, tg)


# ------------------------------------------------------------------ level clear
def clear_panel(c, lv, bg, t, score0):
    """lv: dict(n, unlocked, chips [(big, small) x 3], color). bg: blurred last frame. score0: score before this level."""
    draw_img(c, bg, zoom=1.02 + 0.01 * t)
    c.drawRect(R(0, 1180, W, 300), lin_paint(0, 1180, 0, 1480, [(DEEP, 0.0), (DEEP, 0.55), (DEEP, 0.0)], [0.0, 0.5, 1.0]))
    p1 = prog(t, 0.0, 0.3)
    text(c, T["final"] if lv.get("final") else T["level"].format(n=lv["n"]), W / 2, 498, 50, INK, "Poppins-Bold", a=clamp(p1 * 2),
         shadow_a=0.5)
    if p1 > 0:
        k = lerp(1.9, 1.0, e_back(p1))
        c.save()
        c.translate(W / 2, 668)
        c.scale(k, k)
        add_glow(c, 0, -60, 520, HILITE, 0.30 * clamp(p1 * 2))
        fit(c, T["clear"], 0, 0, 178, HILITE, max_w=940, a=clamp(p1 * 3), stroke_color=DEEP, stroke_w=18, shadow_a=0.6)
        c.restore()
    p2 = prog(t, 0.22, 0.5)
    if p2 > 0:
        c.save()
        c.translate(0, 60 * (1 - e_back(p2)))
        a = clamp(p2 * 2)
        glass(c, 90, 740, 900, 176, r=40, a=a)
        c.drawRRect(rr(92, 742, 896, 172, 40), P(HILITE, 0.5 * a, stroke=3))
        add_glow(c, 190, 828, 130, HILITE, 0.35 * a)
        icon_trophy(c, 190, 826, 128, HILITE, a)
        ux, al = side(282, 950)
        text(c, T["unlocked"], ux, 806, 30, ACCENT, "Poppins-Bold", align=al, a=a)
        fit(c, lv["unlocked"], ux, 876, 62, INK, max_w=660, a=a, align=al)
        c.restore()
    for i, (big, small) in enumerate(lv["chips"][:3]):
        stat_card(c, 190 + 350 * i, 1090, big, small, prog(t, 0.5 + 0.2 * i, 0.8 + 0.2 * i), accent=lv.get("color", HILITE))
    p4 = prog(t, 1.05, 1.25)
    if p4 > 0:
        up = int(round(1000 * e_out(prog(t, 1.1, 1.7))))
        star(c, W / 2 - 250, 1296, 30, HILITE, clamp(p4 * 2))
        text(c, f"{T['score']}  {score0 + up:04d}", W / 2 + 20, 1320, 70, HILITE, "Poppins-Black", a=clamp(p4 * 2), stroke_color=DEEP,
             stroke_w=12, shadow_a=0.5)
    fx.confetti(c, W, H, t, 0.08, 2.0)


# ------------------------------------------------------------------ cold open
ICONS = (icon_bolt, icon_flame, icon_signal)
ICON = {"bolt": icon_bolt, "flame": icon_flame, "signal": icon_signal, "person": icon_person, "trophy": icon_trophy,
        "drop": icon_drop, "gear": icon_gear, "brick": icon_brick, "land": icon_land, "wave": icon_wave, "sun": icon_sun,
        "snow": icon_snow, "clock": icon_clock, "coin": icon_coin, "boat": icon_boat, "bridge": icon_bridge,
        "rock": icon_rock, "flat": icon_flat, "down": icon_down, "pause": icon_pause, "rewind": icon_rewind,
        "hourglass": icon_hourglass, "umbrella": icon_umbrella, "shortcut": icon_shortcut, "lighthouse": icon_lighthouse}
WARM_ICONS = ("flame", "sun", "coin")       # drawn orange in the cold open, the rest yellow


def slam_icon(c, k, t, shake_seed=0):
    """Word k of "No electricity. No fuel. No help.": the icon in a dark disc, then the red no-sign stamps on."""
    rnd = random.Random(shake_seed + int(t * 30))
    sh = (1 - prog(t, 0.0, 0.18)) * 14
    c.save()
    c.translate(rnd.uniform(-sh, sh), rnd.uniform(-sh, sh))
    p = prog(t, 0.0, 0.14)
    kk = lerp(0.6, 1.0, e_back(p))
    c.save()
    c.translate(W / 2, 800)
    c.scale(kk, kk)
    add_glow(c, 0, 0, 520, WARN, 0.25 * clamp(p * 2))
    c.drawCircle(0, 14, 258, P("#000000", 0.5, blur=22))
    c.drawCircle(0, 0, 250, rad_paint(-60, -80, 420, ["#22305C", NAVY, DEEP]))
    c.drawCircle(0, 0, 250, P("#FFFFFF", 0.18, stroke=4))
    name = T["no_icons"][k]
    ICON[name](c, 0, 0, 290, "#FF8A3D" if name in WARM_ICONS else HILITE)
    c.restore()
    no_sign(c, W / 2, 800, 282, prog(t, 0.10, 0.26))
    c.restore()
    flash(c, 0.55 * (1 - prog(t, 0.0, 0.10)))


def lone(c, t):
    """'Just you': one small figure in a pool of light."""
    p = prog(t, 0.0, 0.25)
    add_glow(c, W / 2, 900, 520, "#FFF1C9", 0.20 * p)
    c.drawOval(skia.Rect.MakeXYWH(W / 2 - 170, 1040, 340, 60), P("#000000", 0.5 * p, blur=18))
    icon_person(c, W / 2, 900, 330, INK, p)


def world_flash(c, frame_img, k, label, t, dur, chip=None):
    """One of the four worlds in the cold open: the clean moving picture, a red stamp, a counter."""
    draw_img(c, frame_img, zoom=1.05 + 0.05 * t / dur, cy=0.42)
    c.drawRect(R(0, 0, W, H), rad_paint(W / 2, H / 2, H * 0.7, [(DEEP, 0.0), (DEEP, 0.0), (DEEP, 0.55)], [0.0, 0.55, 1.0]))
    p = prog(t, 0.03, 0.17)
    if p > 0:
        kk = lerp(1.8, 1.0, e_out(p))
        c.save()
        c.translate(W / 2, 700)
        c.rotate(-5)
        c.scale(kk, kk)
        fit(c, label, 0, 0, 230, "#FFFFFF", max_w=900, a=clamp(p * 3), stroke_color=WARN, stroke_w=30, shadow_a=0.7)
        fit(c, label, 0, 0, 230, "#FFFFFF", max_w=900, a=clamp(p * 3))
        c.restore()
    v2.chip(c, W / 2, 330, chip or f"{k + 1} / 4", prog(t, 0.0, 0.12), size=40, accent=WARN)
    flash(c, 0.6 * (1 - prog(t, 0.0, 0.09)))


def title_art(c, wall, t, p_sur=1.0, p_mode=1.0, p_rib=1.0, p_sub=1.0, start=0.0):
    """Title: SURVIVAL / MODE, the ZERO ELECTRICITY ribbon, '4 LEVELS', and a blinking PRESS START. Also the cover."""
    draw_img(c, wall, zoom=1.04 + 0.01 * t)
    if p_sur > 0:
        k = lerp(2.2, 1.0, e_out(clamp(p_sur)))
        c.save()
        c.translate(W / 2, 800)
        c.scale(k, k)
        add_glow(c, 0, -70, 620, HILITE, 0.28 * clamp(p_sur * 2))
        fit(c, T["title1"], 0, 0, 212, HILITE, max_w=1000, a=clamp(p_sur * 3), stroke_color=DEEP, stroke_w=22, shadow_a=0.7)
        c.restore()
    if p_mode > 0:
        k = lerp(2.0, 1.0, e_out(clamp(p_mode)))
        c.save()
        c.translate(W / 2, 990)
        c.scale(k, k)
        fit(c, T["title2"], 0, 0, 212, INK, max_w=1000, a=clamp(p_mode * 3), stroke_color=DEEP, stroke_w=22, shadow_a=0.7)
        c.restore()
    if p_rib > 0:
        k = e_back(clamp(p_rib))
        c.save()
        c.translate(W / 2, 1110)
        c.rotate(-2.5)
        c.scale(k, k)
        c.drawRRect(rr(-420, -58 + 10, 840, 116, 24), P("#000000", 0.5, blur=16))
        c.drawRRect(rr(-420, -58, 840, 116, 24), lin_paint(-420, 0, 420, 0, ["#FF3B4E", "#FF6A3D"]))
        c.drawRRect(rr(-418, -56, 836, 112, 24), P("#FFFFFF", 0.35, stroke=3))
        ix = 350 if T["rtl"] else -350
        ICON[T["ribbon_icon"]](c, ix, 0, 86, "#FFFFFF")
        if T["ribbon_crossed"]:
            c.drawLine(ix - 38, 34, ix + 38, -34, P("#FFFFFF", 1.0, stroke=10))
        fit(c, T["ribbon"], -40 if T["rtl"] else 40, 22, 62, "#FFFFFF", max_w=640)
        c.restore()
    if p_sub > 0:
        text(c, T["sub"], W / 2, 1250, 44, INK, "Poppins-Bold", a=clamp(p_sub * 2), stroke_color=DEEP, stroke_w=9, shadow_a=0.5)
    if start > 0:
        a = start * (0.35 + 0.65 * (math.sin(t * 16) > -0.2))
        text(c, T["press"], W / 2, 1500, 62, HILITE, "Poppins-Black", a=a, stroke_color=DEEP, stroke_w=11, shadow_a=0.5)


# ------------------------------------------------------------------ results
def end_card(c, wall, t, rows, ev, caps=None, tg=0.0, next_text="NEW WORLD TOMORROW", pill=("FOLLOW", "or the boss wins")):
    """rows: [(level label, name)], ev: dict(score0, score1, power, rank, next) in seconds from the card's start."""
    draw_img(c, wall, zoom=1.04 + 0.004 * t, dim=0.22)
    p = prog(t, 0.05, 0.3)
    if p > 0:
        k = lerp(2.0, 1.0, e_back(p))
        c.save()
        c.translate(W / 2, 400)
        c.scale(k, k)
        add_glow(c, 0, -50, 600, HILITE, 0.28 * clamp(p * 2))
        fit(c, T["world_clear"], 0, 0, 132, HILITE, max_w=980, a=clamp(p * 3), stroke_color=DEEP, stroke_w=18, shadow_a=0.6)
        c.restore()
    pp = prog(t, 0.3, 0.55)
    if pp > 0:
        a = clamp(pp * 2)
        glass(c, 70, 450, 940, 560, r=40, a=a)
        for i, (lab, name) in enumerate(rows):
            pr = prog(t, 0.5 + 0.22 * i, 0.72 + 0.22 * i)
            if pr <= 0:
                continue
            y = 536 + 96 * i
            if T["rtl"]:
                v2.badge(c, 942, y - 14, pr, "check", t, 0.52)
                text(c, lab, 884, y, 34, "#9FB0D0", "Poppins-Bold", align="right", a=clamp(pr * 2))
                fit(c, name, 830, y, 44, INK, "Poppins-Black", max_w=520, a=clamp(pr * 2), align="right")
                text(c, "+1000", 104, y, 44, HILITE, "Poppins-Black", align="left", a=clamp(pr * 2))
            else:
                v2.badge(c, 138, y - 14, pr, "check", t, 0.52)
                text(c, lab, 196, y, 34, "#9FB0D0", "Poppins-Bold", align="left", a=clamp(pr * 2))
                fit(c, name, 300, y, 44, INK, "Poppins-Black", max_w=470, a=clamp(pr * 2), align="left")
                text(c, "+1000", 976, y, 44, HILITE, "Poppins-Black", align="right", a=clamp(pr * 2))
        pw = prog(t, ev["power"], ev["power"] + 0.25)
        c.drawRect(R(110, 876, 860, 3), P("#FFFFFF", 0.18 * a))
        lx, al = side(110, 970)
        fit(c, T["result_label"], lx, 952, 42, "#9FB0D0", "Poppins-Bold", max_w=600, align=al, a=a)
        if pw > 0:
            k = lerp(1.8, 1.0, e_back(pw))
            c.save()
            c.translate(210 if T["rtl"] else 870, 936)
            c.scale(k, k)
            add_glow(c, 0, 0, 170, ACCENT, 0.45 * clamp(pw * 2) * (1 - prog(t, ev["power"] + 0.3, ev["power"] + 1.2) * 0.6))
            fit(c, T["result_value"], 0, 22, 70, ACCENT, max_w=230, a=clamp(pw * 3))
            c.restore()
    nxt = prog(t, ev["next"], ev["next"] + 0.3)
    ps = prog(t, ev["score0"] - 0.2, ev["score0"]) * (1 - nxt)
    if ps > 0:
        val = int(round(4000 * e_out(prog(t, ev["score0"], ev["score1"]))))
        star(c, 196, 1124, 40, HILITE, ps)
        text(c, f"{val:04d}", 250, 1160, 112, HILITE, "Poppins-Black", align="left", a=ps, stroke_color=DEEP, stroke_w=14, shadow_a=0.5)
        pr = prog(t, ev["rank"], ev["rank"] + 0.2)
        if pr > 0:
            k = lerp(2.4, 1.0, e_out(pr))
            c.save()
            c.translate(850, 1120)
            c.rotate(-9)
            c.scale(k, k)
            c.drawRRect(rr(-130, -70, 260, 140, 22), P(GOOD, 0.95 * clamp(pr * 3) * (1 - nxt), stroke=9))
            fit(c, T["rank"], 0, 22, 62, GOOD, max_w=230, a=clamp(pr * 3) * (1 - nxt))
            c.restore()
    if nxt > 0:
        fit(c, next_text, W / 2, 1100, 66, INK, max_w=960, a=nxt, stroke_color=DEEP, stroke_w=12, shadow_a=0.5)
        tp = ev.get("pill", ev["next"] + 0.55)
        v2.follow_pill(c, W, pill[0], pill[1], prog(t, tp, tp + 0.3), y=1196)
    fx.confetti(c, W, H, t, 0.1, 2.6)
    if caps is not None:
        caps.draw(c, W, tg)


# ------------------------------------------------------------------ the card that sends people to the YouTube channel
def play_badge(c, x, y, s, a=1.0):
    """A plain play button: yellow disc, dark triangle."""
    add_glow(c, x, y, s * 1.6, HILITE, 0.35 * a)
    c.drawCircle(x, y, s * 0.5, P(HILITE, a))
    c.save()
    c.translate(x, y)
    c.drawPath(_path([(-0.13, -0.22), (0.24, 0.0), (-0.13, 0.22)], s), P(NAVY, a))
    c.restore()


def yt_card(c, wall, t, handle, p_top=1.0, p_yt=1.0, p_handle=1.0, p_pill=1.0):
    """ALL 4 LEVELS / ON YOUTUBE / the channel's handle / SUBSCRIBE or the boss wins."""
    draw_img(c, wall, zoom=1.04 + 0.01 * t, dim=0.25)
    if p_top > 0:
        k = lerp(2.0, 1.0, e_out(clamp(p_top)))
        c.save()
        c.translate(W / 2, 640)
        c.scale(k, k)
        add_glow(c, 0, -60, 600, HILITE, 0.28 * clamp(p_top * 2))
        fit(c, T["all_levels"], 0, 0, 150, HILITE, max_w=980, a=clamp(p_top * 3), stroke_color=DEEP, stroke_w=20, shadow_a=0.7)
        c.restore()
    if p_yt > 0:
        k = e_back(clamp(p_yt))
        c.save()
        c.translate(W / 2, 800)
        c.scale(k, k)
        ks = min(1.0, 800 / max(1.0, text_width(T["on_youtube"], 118, "Poppins-Black")))
        wy = text_width(T["on_youtube"], 118 * ks, "Poppins-Black")
        sgn = -1 if T["rtl"] else 1                                  # the play button leads the line: left in English, right in Arabic
        play_badge(c, sgn * (-wy / 2 - 30), -42, 118, clamp(p_yt * 3))
        text(c, T["on_youtube"], sgn * 62, 0, 118 * ks, INK, "Poppins-Black", a=clamp(p_yt * 3), stroke_color=DEEP, stroke_w=18, shadow_a=0.7)
        c.restore()
    if p_handle > 0:
        k = e_back(clamp(p_handle))
        a = clamp(p_handle * 3)
        c.save()
        c.translate(W / 2, 1000)
        c.scale(k, k)
        hw = text_width(handle, 70, "Poppins-Black") + 96
        c.drawRRect(rr(-hw / 2, -70 + 10, hw, 140, 70), P("#000000", 0.5 * a, blur=16))
        c.drawRRect(rr(-hw / 2, -70, hw, 140, 70), lin_paint(0, -70, 0, 70, ["#1A2547", NAVY], None, a))
        c.drawRRect(rr(-hw / 2 + 2, -68, hw - 4, 136, 68), P(HILITE, 0.9 * a, stroke=4))
        text(c, handle, 0, 25, 70, INK, "Poppins-Black", a=a)
        c.restore()
    v2.follow_pill(c, W, T["subscribe"], T["or_boss"], p_pill, y=1180)
