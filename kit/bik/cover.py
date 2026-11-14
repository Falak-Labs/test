"""Video cover: the finished build from the episode's own picture, with the build number and its name.

The cover is drawn into frame 0 of the video (one frame, 33 ms) and the posts pick that frame as the cover
(Buffer metadata.thumbnailOffset = 0 on TikTok and Instagram). Profile grids show the middle 3:4 of the 9:16 frame
(y 240-1680), so everything that matters stays inside it.

    subject(lang, closer_line, fallback) -> (small line, name)   e.g. ("CONGRATS, YOU JUST BUILT", "AN AIRCRAFT CARRIER")
    overlay(c, W, H, build_no, lang, small, name)                 badge, shading and the two lines on a finished picture
"""
import re

import skia

from bik import arabic
from bik.draw import P, R, font, rect, text, text_width

YELLOW = "#FACC15"      # the hard hat in the channel picture
NAVY = "#172554"
INK = "#070B1F"
GRID_TOP, GRID_BOTTOM = 240, 1680
MAX_W = 940

_AR = re.compile(r"^\s*و?(مبروك)[،,]?\s*(.*?(?:بنيت|سويت لك|سويت))\s+(.+?)\s+(?:بإيدك|بإيديك|بايدك|بيدك|بإيدك)\s*[.!؟]?\s*$")
_EN = re.compile(r"just built (.+?)(?: yourself)?\s*[.!]?\s*$", re.I)


def subject(lang, closer, fallback):
    """The small line and the build's name, taken from the closing line ("And congrats, you just built X yourself.")."""
    closer = (closer or "").strip()
    if lang.startswith("ar"):
        m = _AR.match(closer)
        if m:
            return f"{m.group(1)}، {m.group(2)}", m.group(3).strip()
        return "مبروك، انت بنيت", fallback
    m = _EN.search(closer)
    name = m.group(1).strip() if m else fallback
    name = re.sub(r"^(a|an)\s+", "", name, flags=re.I)
    return "CONGRATS, YOU JUST BUILT", name.upper()


def _fit(words, width_of, sizes):
    """Largest size at which the name fits in one line, or in two balanced lines."""
    for size in sizes:
        one = " ".join(words)
        if width_of(one, size) <= MAX_W:
            return size, [one]
        best = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            wa, wb = width_of(a, size), width_of(b, size)
            if max(wa, wb) <= MAX_W and (best is None or abs(wa - wb) < best[0]):
                best = (abs(wa - wb), [a, b])
        if best:
            return size, best[1]
    return sizes[-1], [" ".join(words)]


def _shade(c, W, H):
    from bik.v2 import lin_paint
    c.drawRect(R(0, 0, W, 520), lin_paint(0, 0, 0, 520, [(INK, 0.62), (INK, 0.0)]))
    c.drawRect(R(0, 1060, W, H - 1060), lin_paint(0, 1060, 0, H, [(INK, 0.0), (INK, 0.78), (INK, 0.92)], [0.0, 0.53, 1.0]))


def _badge(c, W, build_no, rtl):
    y = 352
    if rtl:
        label = f"البناء رقم {build_no}"
        tw = arabic.width_ar(label, 60, "Tajawal-Black")
    else:
        label = f"BUILD #{build_no}"
        tw = text_width(label, 54, "Poppins-Black")
    w, h = tw + 96, 104
    rect(c, W / 2 - w / 2, y - h / 2 + 8, w, h, "#000000", 0.35, r=h / 2, blur=14)
    rect(c, W / 2 - w / 2, y - h / 2, w, h, YELLOW, 1.0, r=h / 2)
    rect(c, W / 2 - w / 2 + 6, y - h / 2 + 6, w - 12, h / 2 - 6, "#FFFFFF", 0.16, r=h / 2 - 6)
    if rtl:
        arabic.text_ar(c, label, W / 2, y + 22, 60, NAVY, "Tajawal-Black")
    else:
        text(c, label, W / 2, y + 19, 54, NAVY, "Poppins-Black")


def _title_en(c, s, x, y, size):
    """Bold outlined title (round joins, so the thick outline has no spikes)."""
    f = font("Poppins-Black", size)
    x0 = x - f.measureText(s) / 2
    c.drawString(s, x0, y + size * 0.07, f, P("#000000", 0.55, blur=size * 0.07))
    sp = P(INK, 1.0, stroke=size * 0.11)
    sp.setStrokeJoin(skia.Paint.kRound_Join)
    c.drawString(s, x0, y, f, sp)
    c.drawString(s, x0, y, f, P(YELLOW, 1.0))


def overlay(c, W, H, build_no, lang, small, name):
    rtl = lang.startswith("ar")
    _shade(c, W, H)
    _badge(c, W, build_no, rtl)
    if rtl:
        size, lines = _fit(name.split(), lambda s, z: arabic.width_ar(s, z, "Tajawal-Black"), list(range(156, 96, -4)))
        lh = size * 1.12
    else:
        size, lines = _fit(name.split(), lambda s, z: text_width(s, z, "Poppins-Black"), list(range(156, 84, -4)))
        lh = size * 1.04
    base = 1608                                            # baseline of the last line of the name
    first = base - lh * (len(lines) - 1)
    small_y = first - size * (0.92 if rtl else 0.86) - 30
    if rtl:
        arabic.text_ar(c, small, W / 2, small_y, 66, "#FFFFFF", "Tajawal-Bold", shadow_a=0.6)
    else:
        text(c, small, W / 2, small_y, 54, "#FFFFFF", "Poppins-ExtraBold", shadow_a=0.6)
    for i, ln in enumerate(lines):
        y = first + i * lh
        if rtl:
            arabic.text_ar(c, ln, W / 2, y, size, YELLOW, "Tajawal-Black", stroke_color=INK, stroke_w=size * 0.12, shadow_a=0.7)
        else:
            _title_en(c, ln, W / 2, y, size)
    return {"small": small, "name": name, "size": size, "lines": lines, "top_of_text": small_y - 70, "bottom": base + size * 0.25}
