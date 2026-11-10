"""Arabic text: HarfBuzz shaping (joined letters, right-to-left) drawn as skia glyph runs.

skia's plain drawString does not join Arabic letters, so every Arabic caption or label goes
through shape() here. Font: Tajawal (OFL) in fonts/ar/.
"""
import os
import re
import struct

import skia
import uharfbuzz as hb

from .core import clamp, e_back
from .draw import C, P, rect, FONT_DIR

AR_FONT_DIR = os.path.join(FONT_DIR, "ar")
AR_RE = re.compile(r"[؀-ۿ]")
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_HB, _SK = {}, {}


def is_ar(s):
    return bool(AR_RE.search(s or ""))


def norm_ar(s):
    """Matching key: no diacritics or tatweel, one alef, ى->ي, ة->ه, letters and digits only."""
    s = TASHKEEL.sub("", s)
    s = re.sub("[إأآٱ]", "ا", s)
    s = s.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    return re.sub(r"[^ء-ي0-9]", "", s)


def _path(name):
    return os.path.join(AR_FONT_DIR, name + ".ttf")


def _hb_font(name):
    if name not in _HB:
        face = hb.Face(hb.Blob.from_file_path(_path(name)))
        f = hb.Font(face)
        f.scale = (face.upem, face.upem)
        _HB[name] = (f, face.upem)
    return _HB[name]


def _sk_font(name, size):
    if name not in _SK:
        _SK[name] = skia.Typeface.MakeFromFile(_path(name))
    f = skia.Font(_SK[name], size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def shape(s, size, name="Tajawal-Black"):
    """Glyph ids, glyph positions (visual order, left to right) and the advance width."""
    font, upem = _hb_font(name)
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    k = size / upem
    gids, pos, x = [], [], 0.0
    for info, gp in zip(buf.glyph_infos, buf.glyph_positions):
        gids.append(info.codepoint)
        pos.append(skia.Point(x + gp.x_offset * k, -gp.y_offset * k))
        x += gp.x_advance * k
    return gids, pos, x


def width_ar(s, size, name="Tajawal-Black"):
    return shape(s, size, name)[2]


def _blob(s, size, name):
    gids, pos, w = shape(s, size, name)
    data = struct.pack(f"<{len(gids)}H", *gids)
    return skia.TextBlob.MakeFromPosText(data, pos, _sk_font(name, size), skia.TextEncoding.kGlyphID), w


def text_ar(c, s, x, y, size, color, name="Tajawal-Black", align="center", a=1.0,
            stroke_color=None, stroke_w=0, shadow_a=0.0):
    """Arabic counterpart of draw.text: baseline at y; align left/center/right on the visual box."""
    if a <= 0 or not s:
        return 0.0
    blob, w = _blob(s, size, name)
    x0 = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    if shadow_a > 0:
        c.drawTextBlob(blob, x0, y + size * 0.06, P("#000000", shadow_a * a, blur=size * 0.06))
    if stroke_color and stroke_w > 0:
        sp = P(stroke_color, a, stroke=stroke_w)
        sp.setStrokeJoin(skia.Paint.kRound_Join)
        c.drawTextBlob(blob, x0, y, sp)
    c.drawTextBlob(blob, x0, y, P(color, a))
    return w


def cta_pill_ar(c, W, label, sub, p, y=210):
    """Right-to-left FOLLOW pill: plus badge on the right, label, then the 'next' line to its left."""
    if p <= 0:
        return
    s = e_back(clamp(p))
    lw, sw = width_ar(label, 66, "Tajawal-Black"), width_ar(sub, 46, "Tajawal-Bold")
    w = max(lw + sw + 210, 600)
    c.save()
    c.translate(W / 2, y)
    c.scale(s, s)
    rect(c, -w / 2, -66 + 10, w, 132, "#000000", 0.35, r=66, blur=12)
    rect(c, -w / 2, -66, w, 132, "#FF4D2E", 1.0, r=66)
    rect(c, w / 2 - 118, -52, 104, 104, "#FFFFFF", 1.0, r=52)
    rect(c, w / 2 - 118 + 32, -6, 40, 12, "#FF4D2E", r=6)
    rect(c, w / 2 - 118 + 46, -20, 12, 40, "#FF4D2E", r=6)
    xr = w / 2 - 140
    text_ar(c, label, xr, 22, 66, "#FFFFFF", "Tajawal-Black", align="right")
    text_ar(c, sub, xr - lw - 22, 18, 46, "#FFE7DF", "Tajawal-Bold", align="right")
    c.restore()


def stat_badge_ar(c, x, y, big, small, p, color="#111827"):
    """Big number (Poppins digits) over an Arabic label."""
    from .draw import text, text_width
    if p <= 0:
        return
    s = e_back(clamp(p))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    w = max(text_width(big, 110, "Poppins-Black"), width_ar(small, 46, "Tajawal-Black")) + 70
    rect(c, -w / 2, -95 + 10, w, 190, "#000000", 0.3, r=34, blur=10)
    rect(c, -w / 2, -95, w, 190, "#FFFFFF", 1.0, r=34)
    text(c, big, 0, 20, 110, color, "Poppins-Black")
    text_ar(c, small, 0, 76, 46, "#6B7280", "Tajawal-Black")
    c.restore()
