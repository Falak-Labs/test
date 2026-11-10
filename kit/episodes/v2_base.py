"""Shared base for episodes in the v2 look (Episode 6 on).  Reference episode: episodes/rocket.py.

An episode subclasses EpisodeV2 and provides:
  class data   BUILD_NO, TITLE, EMPH, KEYS, TEXT (follow pill, three stat cards, label texts "L"), FIRST_SET, SKY_ALT
  _tracks()    word anchors (self.anchors), cuts between sets (self.cut), cameras, self.spans (HUD), self.shakes
  draw_<set>(c, t)        the picture of one set (screen space; use self.view(c, cam) for the world transform)
  ui_<set>(c, t, tw)      labels / badges for that set, drawn on top of the finished picture (optional)
  sfx_events()            [(time, samples, gain_db), ...]

The base does the rest: beat timeline and captions, Saudi anchors through KEYS, whip cuts, camera shake, the fake
pause, the finishing pass (bloom, grain, vignette), the progress HUD, stat cards, confetti, pause icon, FOLLOW pill.

Times: t = video time (keeps running), tw = world time (frozen during the fake pause).  draw_<set> gets tw.
"""
import math      # noqa: F401
import os
import random    # noqa: F401
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
os.environ.setdefault("BIK_CRF", "24")          # v2 frames carry fine grain: crf 18 would make ~95 MB files
os.environ.setdefault("BIK_PRESET", "medium")

import numpy as np   # noqa: E402,F401
import skia          # noqa: E402,F401

from bik.core import Timeline, Camera, Track, Steps, clamp, lerp, prog, e_io, e_out, e_in, e_back, e_elastic, bump, blink  # noqa: E402,F401
from bik.draw import C, P, R, rect, circle, poly, line, dashed, text, text_width, mix, shade  # noqa: E402,F401
from bik import sfx, v2, v2set, fx, arabic  # noqa: E402,F401
from bik.captions import word_timings, Captions as _Finder  # noqa: E402
from bik.v2 import (lin_paint, rad_paint, rr, vrect, cyl, cyl_path, box, add_glow, contact_shadow, light_cone, puff,  # noqa: E402,F401
                    glass, ACCENT, WARN, GOOD, HILITE, INK, GLASS, PLUS, SCREEN)
from bik.v2set import (STEEL, SHIRTS, dash_paint, hard_hat, hats_in_the_air, lattice, beacon, floodlight, bunker,  # noqa: E402,F401
                       engineer, person, buried_line, building_ghost, sea, heart, rumble, boom, gas_hiss,
                       skyline_night, window_night, room, underwater, bubbles, splash, sparks_shower)

W, H = 1080, 1920
LABELS = ["hook", "break1", "fix1", "break2", "fix2", "break3", "fix3", "break4", "fix4", "cta", "reveal", "stat",
          "closer", "tag"]


class EpisodeV2:
    BUILD_NO = 0
    TITLE = {"en": "BUILD"}                       # HUD title per language: {"en": "ROCKET", "ar_sa": "صاروخ"}
    EMPH = {"en": []}                             # caption words that stay yellow once spoken
    KEYS = {}                                     # {"ar_sa": {(label, "ENGLISH KEY"): "الكلمة"}} one Saudi word per anchor
    TEXT = {"en": {"follow": ("FOLLOW", "next: ..."), "stat": [("1", "A"), ("2", "B"), ("3", "C")], "L": {}}}
    STAT_COLORS = (INK, "#FFB05C", HILITE)
    STAT_Y = 440
    FIRST_SET = "main"
    SKY_ALT = {}                                  # set name -> 0 (on the ground) .. 1 (space): sky shown behind a whip cut
    CLEAR = "#070B1F"
    TAIL = 2.0
    CAPTION_Y = 1330

    def __init__(self, vo_json, vo_wav, lang="en"):
        self.lang, self.rtl = lang, lang.startswith("ar")
        self.tx = self.TEXT.get(lang, self.TEXT["en"])
        self.L = dict(self.TEXT["en"].get("L", {}), **self.tx.get("L", {}))
        self.tl = tl = Timeline(vo_json, LABELS, lead=0.5, pause=0.6, tail=self.TAIL)
        self.words = word_timings(vo_wav, tl)
        self.cap = v2.Captions(self.words, self.EMPH.get(lang, self.EMPH["en"]), rtl=self.rtl, y=self.CAPTION_Y,
                               hide=[(tl.pause_start, tl.s("cta"))])
        self._finder = _Finder(self.words)
        self.duration = tl.duration
        self.post = v2.Post(W, H)
        self.buf = None
        self.ui = {}                               # scratch: draw_<set> leaves screen positions here for ui_<set>
        self.cuts = [(-1e9, self.FIRST_SET, 0)]
        self.shakes = []                           # (t0, duration, amplitude in pixels)
        self.spans = []                            # four (t_break, t_fix) pairs for the HUD
        self.missing = []                          # anchors whose word was not found (fell back to a beat fraction)
        self.T = {"pause": tl.pause_start}
        self._t = self._tw = 0.0
        self._c = None
        self._tracks()
        self.cuts.sort(key=lambda k: k[0])

    # ------------------------------------------------------------------ timing
    def w(self, lab, key, frac=0.5, nth=0):
        """Start of a spoken word in a beat (English key; the Saudi word via KEYS), else a fraction of the beat."""
        k = self.KEYS.get(self.lang, {}).get((lab, key), key) if self.lang != "en" else key
        t = self._finder.find(lab, k, nth)
        if t is None:
            self.missing.append((lab, key, k))
            t = lerp(self.tl.s(lab), self.tl.e(lab), frac)
        return t

    def anchors(self, spec):
        """spec: {name: (label, KEY, fallback fraction)} -> fills self.T."""
        for name, (lab, key, frac) in spec.items():
            self.T[name] = self.w(lab, key, frac)

    def world_t(self, t):
        tl = self.tl
        return tl.pause_start if tl.pause_start <= t < tl.s("cta") else t

    def cut(self, t, name, direction=1):
        """Whip cut to another set at time t. direction 1: the old picture leaves downward, -1: upward."""
        self.cuts.append((t, name, direction))

    def mode(self, t):
        m = self.cuts[0][1]
        for tc, name, _ in self.cuts:
            if t >= tc:
                m = name
        return m

    def whip(self, t):
        """(vertical offset in pixels, amount 0..1) for the whip cuts."""
        for tc, _, sign in self.cuts[1:]:
            if tc - 0.13 <= t < tc:
                p = e_in(prog(t, tc - 0.13, tc))
                return sign * p * H * 0.9, p
            if tc <= t < tc + 0.16:
                p = 1 - e_out(prog(t, tc, tc + 0.16))
                return -sign * p * H * 0.9, p
        return 0.0, 0.0

    def shake(self, t):
        dx = dy = 0.0
        for t0, d, amp in self.shakes:
            if t0 <= t < t0 + d:
                k = (1 - (t - t0) / d) ** 1.5 * amp
                dx += math.sin(t * 91) * k
                dy += math.cos(t * 77) * k
        return dx, dy

    # ------------------------------------------------------------------ world <-> screen
    @staticmethod
    def view(c, cam):
        """Start drawing in world space for cam = (cx, cy, zoom). Call c.restore() when done."""
        cx, cy, z = cam
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(z, z)
        c.translate(-cx, -cy)

    @staticmethod
    def to_screen(cam, x, y):
        cx, cy, z = cam
        return (x - cx) * z + W / 2, (y - cy) * z + H / 2

    # ------------------------------------------------------------------ frame
    def draw(self, c, t):
        if self.buf is None:
            self.buf = skia.Surface(W, H)
        tw = self.world_t(t)
        self._t, self._tw, self._c = t, tw, c
        b = self.buf.getCanvas()
        b.clear(C(self.CLEAR))
        off, amt = self.whip(tw)
        sx, sy = self.shake(tw)
        m = self.mode(tw)
        if amt > 0:                                              # something behind the sliding picture, so no edge shows
            self.whip_backdrop(b, tw, m)
        b.save()
        b.translate(sx, sy + off)
        self.ui = {}
        getattr(self, "draw_" + m)(b, tw)
        b.restore()
        if amt > 0:                                              # smear during the whip
            v2.speed_streaks(b, W, H, tw, 0.9 * amt, seed=12, n=60)
            b.drawRect(R(0, 0, W, H), P(self.CLEAR, 0.25 * amt))
        self.post.apply(c, self.buf.makeImageSnapshot(), int(round(t * 30)))
        v2.hud(c, W, t, self.BUILD_NO, self.TITLE.get(self.lang, self.TITLE["en"]), self.hud_states(tw),
               a=prog(t, 0.15, 0.5), rtl=self.rtl)
        f = getattr(self, "ui_" + m, None)
        if f:
            f(c, t, tw)
        self.ui_common(c, t, tw)
        self.cap.draw(c, W, t)

    def whip_backdrop(self, c, t, m):
        v2.sky(c, W, H, self.SKY_ALT.get(m, 0.0), horizon_y=H * 0.66)
        v2.stars(c, W, H, t, 0.8)

    def backdrop(self, c, t, cx, cy, gy, sea_=False, moon=True, ridges=(("#3A3378", "#B25A72"), ("#1B1C4A", "#3B2A5E"))):
        """Far layers for outdoor ground sets at dusk: sky, stars, moon, clouds, two mountain ridges, town lights.
        Screen space with parallax. gy = screen y of the ground line. sea_=True leaves the ridges out."""
        v2.sky(c, W, H, 0.0, horizon_y=gy)
        v2.stars(c, W, H, t, 0.9, dx=-cx * 0.02, dy=(cy + 360) * -0.03)
        if moon:
            v2.moon(c, 236 - cx * 0.02, gy - 880, 74)
        for i, (px, py, s_, par) in enumerate(((260, 640, 1.0, 0.05), (840, 470, 0.72, 0.035), (-60, 400, 0.6, 0.03))):
            v2.cloud(c, (px + t * (5 + i * 2) - cx * par) % (W + 700) - 250, gy - py, s_, a=0.85, seed=i)
        if sea_ or not ridges:
            return
        c.save()
        c.translate(W / 2 - cx * 0.06, gy)
        v2.ridge(c, -1500, 1500, 0, 250, ridges[0][0], ridges[0][1], seed=5, step=150, rough=0.5)
        rng = random.Random(9)
        for _ in range(46):
            add_glow(c, rng.uniform(-900, 900), rng.uniform(-22, -4), rng.uniform(4, 9),
                     rng.choice(["#FFD98A", "#FFE9C9", "#FFB37A"]), 0.8)
        c.restore()
        c.save()
        c.translate(W / 2 - cx * 0.16, gy)
        v2.ridge(c, -1700, 1700, 0, 120, ridges[1][0], ridges[1][1], seed=8, step=70, rough=0.75)
        c.restore()

    # ------------------------------------------------------------------ the crew
    def crew(self, c, t, pose, soot=0.0, xs=(392, 438, 486), y=0, face=-1, h=118):
        """Three engineers in hard hats (world space). pose: stand | cheer | look | point | duck. With "point" only the
        middle one points and the others look. face: -1 they look left, 1 right."""
        for i, (px, col) in enumerate(zip(xs, SHIRTS)):
            engineer(c, px, y, h + (i % 2) * 8, col, t + i * 0.37, pose if not (pose == "point" and i != 1) else "look",
                     soot, face=face)

    # ------------------------------------------------------------------ UI helpers (call from ui_<set>)
    def hud_states(self, t):
        st = [("fix", t1) if t >= t1 else ("break", t0) if t >= t0 else 0 for t0, t1 in self.spans]
        return (st + [0, 0, 0, 0])[:4]

    def span(self, t0, t1, fin=0.3, fout=0.25):
        """0..1 visibility for something shown from t0 to t1 (world time), with fade in / out."""
        return prog(self._tw, t0, t0 + fin) * (1 - prog(self._tw, t1 - fout, t1))

    def badge(self, kind, t0, t1, x=W / 2 + 310, y=510, size=1.25):
        """Round status badge: kind "alert" (every break) or "check" (every fix)."""
        p = prog(self._tw, t0, t0 + 0.28) * (1 - prog(self._tw, t1 - 0.25, t1))
        if p > 0:
            v2.badge(self._c, x, y, p, kind, self._t, size)

    def red(self, t0, dur=2.2):
        """Red glow creeping in from the edges when something breaks."""
        k = clamp(1 - (self._tw - t0) / dur) * 0.8 if self._tw >= t0 else 0.0
        if k > 0:
            self._c.drawRect(R(0, 0, W, H), rad_paint(W / 2, H / 2, H * 0.75, [(WARN, 0.0), (WARN, 0.0), (WARN, 0.5 * k)],
                                                      [0.0, 0.55, 1.0]))

    def label(self, ax, ay, lx, ly, key, t0, t1, accent=ACCENT, size=34):
        """Leader-line label from the part at screen (ax, ay) to a card centred at (lx, ly). key: entry of TEXT[..]["L"]."""
        v2.callout(self._c, ax, ay, lx, ly, self.L.get(key, key), self.span(t0, t1), accent, size=size, t=self._t, rtl=self.rtl)

    def chip(self, x, y, key, t0, t1, accent=None, size=40):
        v2.chip(self._c, x, y, self.L.get(key, key), self.span(t0, t1, 0.25, 0.2), accent=accent, size=size)

    def ui_common(self, c, t, tw):
        T, tl = self.T, self.tl
        bt = 1 - prog(t, tl.s("closer") - 0.1, tl.s("closer") + 0.3)
        xs = (890, 540, 190) if self.rtl else (190, 540, 890)
        for (big, small), x, key, col in zip(self.tx["stat"], xs, ("s1", "s2", "s3"), self.STAT_COLORS):
            if key in T:
                v2.stat_card(c, x, self.STAT_Y, big, small, prog(t, T[key], T[key] + 0.3) * bt, col)
        if "cong2" in T:
            fx.confetti(c, W, H, t, T["cong2"], 2.6)
        pz = prog(t, T["pause"], T["pause"] + 0.25) * (1 - prog(t, tl.s("cta") + 0.55, tl.s("cta") + 0.85))
        v2.pause_overlay(c, W, H, pz)
        if "follow" in T:
            pill = prog(t, T["follow"] - 0.15, T["follow"] + 0.2) * (1 - prog(t, tl.e("cta") + 0.1, tl.e("cta") + 0.4))
            v2.follow_pill(c, W, self.tx["follow"][0], self.tx["follow"][1], pill, rtl=self.rtl)

    def sfx_events(self):
        return []
