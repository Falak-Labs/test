"""SAMPLE (not in episodes.yml): build 68 Taipei 101 retold with the Nov 23 2026 hook method and the look-3 finish.

What changes against episodes/taipei.py:
- Script (series/taipei2_lines.txt): a cold-open hook that shows the thing and does NOT give the answer ("This gold ball is
  the only thing keeping this tower up in a typhoon."), an open loop at the end of line 2 ("So how does it stay up?"),
  answered by the reveal (line 11); the "congrats, you just built" line moves to the payoff (line 13). 199 words.
- Look 3 (v2.Post3): film grade, warm halation, god rays and dust where a light is in the frame.
- On-screen chips follow the new lines (the question gets its own card).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taipei import Taipei, W, H  # noqa: E402
from v2_base import HILITE, WARN  # noqa: E402

EN_KEYS = {("hook", "SWINGING"): "BALL", ("hook", "SKYSCRAPER"): "TOWER", ("hook", "STEADY"): "KEEPING",
           ("hook", "CONGRATS"): "TYPHOON", ("hook", "TAIPEI"): "TYPHOON", ("break1", "YEAR"): "YEAR",
           ("fix2", "TOP"): "TOP", ("reveal", "TWENTY"): "TWENTY", ("tag", "BUMP"): "BUMP"}


class Taipei2(Taipei):
    LOOK = 3
    EMPH = {"en": ["GOLD", "BALL", "ONLY", "TOWER", "TYPHOON", "TYPHOONS", "EARTHQUAKES", "HOW", "STAY", "BAMBOO",
                   "EIGHT", "STEEL", "CONCRETE", "SWAYS", "SEASICK", "HANG", "FIVE", "HUNDRED", "CARS", "CABLES",
                   "WRONG", "RHYTHM", "SHAKES", "TUNE", "LEANS", "OTHER", "STOP", "PISTONS", "SHOCK", "HEAT",
                   "FOLLOW", "DISHWASHER", "BIGGEST", "METER", "CALM", "SIXTY", "FORTY", "PERCENT", "CONGRATS",
                   "TAIPEI", "101", "YOURSELF", "BUMP", "COFFEE", "LAP"]}
    TEXT = {"en": dict(Taipei.TEXT["en"], L=dict(Taipei.TEXT["en"]["L"],
                       ball="THIS GOLD BALL...", steady="...HOLDS UP A TOWER", name="IN A TYPHOON",
                       typhoon="TYPHOONS + EARTHQUAKES", quake="SO HOW DOES IT STAND?"))}

    def w(self, lab, key, frac=0.5, nth=0):
        if self.lang == "en":
            key = EN_KEYS.get((lab, key), key)
        return super().w(lab, key, frac, nth)

    def _tracks(self):
        super()._tracks()
        self.T["how"] = self.w("break1", "HOW", 0.75)

    # ------------------------------------------------------------------ look 3: a light, rays and dust per set
    def draw_city(self, c, t):
        s = self.tl.s
        stat = s("stat") - 0.12 <= t < s("closer") - 0.1
        if stat:
            self.post.light, self.post.rays, self.post.dust = (880, 260), 0.45, 0.35
        elif t >= s("fix1") - 0.12 and t < s("closer") - 0.1:
            self.post.light, self.post.rays, self.post.dust = (540, 120), 0.25, 0.3       # the calm after the storm
        else:
            self.post.dust = 0.15
        super().draw_city(c, t)

    def draw_room(self, c, t):
        self.post.light, self.post.rays, self.post.dust = (300, 380), 0.35, 0.6           # the office window
        super().draw_room(c, t)

    def draw_ball(self, c, t):
        self.post.light, self.post.rays, self.post.dust = (540, 260), 0.4, 0.7            # lamps over the damper
        super().draw_ball(c, t)

    # ------------------------------------------------------------------ the question gets its own card
    def ui_city(self, c, t, tw):
        T, s = self.T, self.tl.s
        if s("break1") - 0.12 <= tw < s("fix1") - 0.12:
            self.chip(540, 300, "typhoon", T["typhoons"] - 0.2, T["how"] - 0.25, accent="#93C5FD", size=42)
            self.chip(540, 300, "quake", T["how"] - 0.25, s("fix1") - 0.15, accent=HILITE, size=50)
            self.badge("alert", T["ground1"], T["how"] - 0.3, x=920, y=440)
            self.red(T["ground1"], 1.0)
            return
        super().ui_city(c, t, tw)


NAME = "taipei2"
EPISODE = Taipei2
_ = (W, H, WARN)
