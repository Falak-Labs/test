"""SAMPLE (not in episodes.yml): taipei2 (new hook method, look 3) plus AI video shots from Higgsfield (Seedance 2.5,
made free on higgsfield.ai, kept in the release ai-media). The shots replace our drawing for three moments:
- the hook (line 1): inside the tower, the golden ball swinging in the storm  -> buildit-taipei-hook.mp4
- break1 (line 2, the question): the tower in the typhoon from the street      -> buildit-taipei-storm.mp4
- the reveal (line 11, 2015): the ball swinging a full meter                   -> buildit-taipei-reveal.mp4 (optional)
HUD, chips and captions stay on top; a short cross-fade joins each shot to the animation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taipei2 import Taipei2  # noqa: E402
from aishot import Shot  # noqa: E402

FADE = 0.25


class Taipei3(Taipei2):
    SHOTS = {"hook": "buildit-taipei-hook.mp4", "break1": "buildit-taipei-storm.mp4", "reveal": "buildit-taipei-reveal.mp4"}

    def _tracks(self):
        super()._tracks()
        s, e = self.tl.s, self.tl.e
        span = {"hook": (0.0, s("break1") - 0.05), "break1": (s("break1") - 0.05, s("fix1") - 0.14),
                "reveal": (s("reveal") - 0.1, s("stat") - 0.14)}
        self.ai = []
        for lab, name in self.SHOTS.items():
            try:
                self.ai.append((span[lab][0], span[lab][1], Shot(name)))
            except Exception as ex:                           # a missing shot leaves our own animation in place
                print(f"AI shot {name} not used: {ex}")

    def _ai_at(self, t):
        for t0, t1, shot in self.ai:
            if t0 - FADE <= t < t1 + FADE:
                a = min(1.0, (t - (t0 - FADE)) / FADE) if t0 > 0.01 else 1.0
                a = min(a, 1.0, ((t1 + FADE) - t) / FADE)
                return t0, t1, shot, max(0.0, a)
        return None

    def _with_ai(self, draw, c, t):
        hit = self._ai_at(t)
        if hit is None or hit[3] < 1.0:
            draw(c, t)
        if hit is not None:
            t0, t1, shot, a = hit
            shot.draw(c, max(0.0, t - t0), length=t1 - t0, a=a)
            self.post.light, self.post.rays = None, 0.0           # the shot has its own light
            self.post.dust = 0.25

    def draw_city(self, c, t):
        self._with_ai(super().draw_city, c, t)

    def draw_ball(self, c, t):
        self._with_ai(super().draw_ball, c, t)


NAME = "taipei3"
EPISODE = Taipei3
