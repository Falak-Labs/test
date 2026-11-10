"""Shared parts for Build-It episodes (Ep 3 on): beat timing, camera + shakes, screen-space labels, outlines,
alert/check badges, the fake pause + FOLLOW pill, stat badges, confetti and captions.

An episode subclasses Episode and fills in EMPH, KEYS, TEXT, _tracks(), draw_world(), draw_overlays(),
red_level() and sfx_events(); optional: draw_backdrop(), dusk_at(), cam_at().
"""
import math
import os
import random
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)

from bik.core import Timeline, Camera, Track, clamp, lerp, prog, e_io, e_out, e_in, e_back, bump  # noqa: E402,F401
from bik.draw import text, text_width, rect, grad_rect, glow, circle, poly, line, mix, shade, C  # noqa: E402,F401
from bik import world, fx, sfx, arabic  # noqa: E402,F401
from bik.captions import Captions, word_timings  # noqa: E402
import skia  # noqa: E402

W, H = 1080, 1920
LABELS = ["hook", "break1", "fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4", "cta", "reveal", "stat",
          "closer", "tag"]
WHITE, RED, GREEN, YELLOW = "#FFFFFF", "#EF4444", "#22C55E", "#FACC15"


class Episode:
    EMPH = {"en": []}
    KEYS = {}
    TEXT = {"en": {"follow": ("FOLLOW", "next: ..."), "stat": [("1", "A"), ("2", "B"), ("3", "C")]}}
    STAT_KEYS = ("s1", "s2", "s3")
    STAT_COLORS = ("#111827", "#111827", "#2563EB")
    TAIL = 2.0

    def __init__(self, vo_json, vo_wav, lang="en"):
        self.lang = lang
        self.rtl = lang.startswith("ar")
        self.tx = self.TEXT.get(lang, self.TEXT["en"])
        self.tl = tl = Timeline(vo_json, LABELS, lead=0.5, pause=0.6, tail=self.TAIL)
        self.words = word_timings(vo_wav, tl)
        self.cap = Captions(self.words, self.EMPH.get(lang, self.EMPH["en"]), hide=[(tl.pause_start, tl.s("cta"))])
        self.duration = tl.duration
        self.cam_state = (0.0, 0.0, 1.0)
        self.shakes = []
        self.T = {"pause": tl.pause_start}
        self._tracks()

    # ------------------------------------------------------------------ timing
    def w(self, lab, key, frac=0.5, nth=0):
        """Start of a spoken word in a beat (English key; the Saudi word via KEYS), else a fraction of the beat."""
        if self.lang in self.KEYS:
            key = self.KEYS[self.lang].get((lab, key), key)
        t = self.cap.find(lab, key, nth)
        if t is None:
            t = lerp(self.tl.s(lab), self.tl.e(lab), frac)
        return t

    def anchors(self, spec):
        """spec: {name: (label, KEY, fallback fraction)} -> fills self.T."""
        for name, (lab, key, frac) in spec.items():
            self.T[name] = self.w(lab, key, frac)

    def world_t(self, t):
        tl = self.tl
        return tl.pause_start if tl.pause_start <= t < tl.s("cta") else t

    # ------------------------------------------------------------------ camera
    def cam_at(self, t):
        return self.cam.at(t)

    def dusk_at(self, t):
        return 0.0

    def camera(self, t):
        cx, cy, z = self.cam_at(t)
        for t0, d, amp in self.shakes:
            if t0 <= t < t0 + d:
                k = (1 - (t - t0) / d) * amp
                cx += math.sin(t * 91) * k / z
                cy += math.cos(t * 77) * k / z
        return cx, cy, z

    def sc(self, x, y):
        cx, cy, z = self.cam_state
        return (x - cx) * z + W / 2, (y - cy) * z + H / 2

    def sc_rect(self, x, y, w, h):
        x0, y0 = self.sc(x, y)
        x1, y1 = self.sc(x + w, y + h)
        return x0, y0, x1 - x0, y1 - y0

    # ------------------------------------------------------------------ frame
    def draw(self, c, t):
        real_t, tw = t, self.world_t(t)
        dusk = self.dusk_at(tw)
        world.sky(c, W, H, dusk, tw)
        cx, cy, z = self.camera(tw)
        self.cam_state = (cx, cy, z)
        self.draw_backdrop(c, tw, dusk)
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)
        self.draw_world(c, tw, dusk, z)
        c.restore()
        self.draw_overlays(c, real_t, tw, dusk)
        self.draw_common(c, real_t, tw)
        self.cap.draw(c, W, real_t)

    def draw_backdrop(self, c, t, dusk):
        cx, cy, z = self.cam_state
        ground_sy = (0 - cy) * z + H / 2
        zf = clamp(0.55 * z ** 0.6, 0.12, 0.85)
        c.save()
        c.translate(W / 2, ground_sy)
        c.scale(zf, zf)
        c.translate(-cx * 0.25, 0)
        world.skyline(c, -4200, 4200, dusk)
        c.restore()

    def draw_world(self, c, t, dusk, z):
        pass

    def draw_overlays(self, c, t, tw, dusk):
        pass

    def red_level(self, t):
        return 0.0

    # ------------------------------------------------------------------ common overlays
    def draw_common(self, c, t, tw):
        T, tl = self.T, self.tl
        fx.red_vignette(c, W, H, clamp(self.red_level(tw)))
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), vignette_paint())
        pz = prog(t, T["pause"], T["pause"] + 0.25) * (1 - prog(t, tl.s("cta") + 0.55, tl.s("cta") + 0.85))
        if pz > 0:
            fx.dim(c, W, H, 0.3 * pz)
            fx.pause_icon(c, W, H, pz, t)
        pill = prog(t, T["follow"] - 0.15, T["follow"] + 0.2) * (1 - prog(t, tl.e("cta") + 0.1, tl.e("cta") + 0.4))
        if pill > 0:
            label, sub = self.tx["follow"]
            if self.rtl:
                wp = arabic.width_ar(label, 66, "Tajawal-Black") + arabic.width_ar(sub, 46, "Tajawal-Bold") + 210
            else:
                wp = text_width(label, 64, "Poppins-Black") + text_width(sub, 44, "Poppins-SemiBold") + 210
            kp = min(1.0, (W - 70) / wp)
            c.save()
            c.translate(W / 2, 210)
            c.scale(kp, kp)
            c.translate(-W / 2, -210)
            (arabic.cta_pill_ar if self.rtl else fx.cta_pill)(c, W, label, sub, pill)
            c.restore()
        bt = 1 - prog(t, tl.s("closer") - 0.1, tl.s("closer") + 0.3)
        xs = (W * 0.8, W * 0.5, W * 0.2) if self.rtl else (W * 0.2, W * 0.5, W * 0.8)
        badge = arabic.stat_badge_ar if self.rtl else fx.stat_badge
        for (big, small), x, key, col in zip(self.tx["stat"], xs, self.STAT_KEYS, self.STAT_COLORS):
            p = prog(t, T[key], T[key] + 0.3) * bt
            if p > 0:
                badge(c, x, 330, big, small, p, color=col)
        fx.confetti(c, W, H, t, T["cong2"], 2.6)

    # ------------------------------------------------------------------ helpers (screen space)
    def pill(self, c, s, x, y, p, fg="#111827", bg="#FFFFFF", size=38):
        """Label pill. s: a string or a list of parts in reading order; Arabic parts shaped, digits in Poppins,
        laid out right to left in the Arabic version."""
        if p <= 0 or not s:
            return
        parts = [s] if isinstance(s, str) else list(s)
        if self.rtl and len(parts) > 1:
            parts = parts[::-1]
        ws = [arabic.width_ar(q, size * 1.05) if arabic.is_ar(q) else text_width(q, size, "Poppins-Black")
              for q in parts]
        gap = size * 0.3
        tw = sum(ws) + gap * (len(parts) - 1)
        k = e_back(clamp(p))
        w, h = tw + 44, size * 1.55
        x = clamp(x, w / 2 + 16, W - w / 2 - 16)
        c.save()
        c.translate(x, y)
        c.scale(k, k)
        rect(c, -w / 2, -h / 2 + 6, w, h, "#000000", 0.3, r=h / 2, blur=8)
        rect(c, -w / 2, -h / 2, w, h, bg, 1.0, r=h / 2)
        xx = -tw / 2
        for q, wq in zip(parts, ws):
            if arabic.is_ar(q):
                arabic.text_ar(c, q, xx, size * 0.36, size * 1.05, fg, align="left")
            else:
                text(c, q, xx, size * 0.36, size, fg, "Poppins-Black", align="left")
            xx += wq + gap
        c.restore()

    def wpill(self, c, t, s, wx, wy, t0, t1, fg="#111827", bg="#FFFFFF", size=38, dx=0, dy=0):
        """Pill anchored to a world point, popping in at t0 and out at t1."""
        p = prog(t, t0, t0 + 0.3) * (1 - prog(t, t1 - 0.25, t1))
        if p > 0:
            x, y = self.sc(wx, wy)
            self.pill(c, s, x + dx, y + dy, p, fg, bg, size)

    def outline(self, c, t, t0, rw, dur=1.2, color=WHITE, **kw):
        if t0 <= t < t0 + dur:
            a = 1 - prog(t, t0 + dur - 0.3, t0 + dur)
            fx.outline(c, *self.sc_rect(*rw), prog(t, t0, t0 + 0.35), color=color, a=a, **kw)

    def alert(self, c, t, t0, t1, wx, wy, size=1.3):
        if t0 <= t < t1:
            x, y = self.sc(wx, wy)
            fx.alert_badge(c, clamp(x, 90, W - 90), clamp(y, 200, 1180), prog(t, t0, t0 + 0.25), size, t)

    def check(self, c, t, t0, wx, wy, size=1.4, dur=1.5):
        dur = max(0.7, dur)
        p = prog(t, t0, t0 + 0.35) * (1 - prog(t, t0 + dur - 0.3, t0 + dur))
        if p > 0:
            x, y = self.sc(wx, wy)
            fx.check_badge(c, clamp(x, 90, W - 90), clamp(y, 200, 1180), p, size)


_VIG = None


def vignette_paint():
    global _VIG
    if _VIG is None:
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.45), H * 0.78,
                                                   [C("#000000", 0), C("#000000", 0), C("#000000", 0.22)],
                                                   [0.0, 0.6, 1.0]))
        _VIG = p
    return _VIG


def ring_pts(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi):
    return [(cx + math.cos(a0 + (a1 - a0) * i / n) * rx, cy + math.sin(a0 + (a1 - a0) * i / n) * ry)
            for i in range(n + 1)]


def tap_ripple(c, x, y, t, t0, scale=1.0):
    """Screen-space tap ripple (two expanding rings)."""
    for k in (0.0, 0.15):
        u = prog(t, t0 + k, t0 + k + 0.5)
        if 0 < u < 1:
            circle(c, x, y, (20 + 70 * u) * scale, "#FFFFFF", 0.9 * (1 - u), stroke=6 * scale)
