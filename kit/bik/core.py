"""Build-It Kit core: easing, beat timeline, camera.

Video time = voiceover time + LEAD, plus PAUSE seconds for everything from the
fake-pause beat (label "cta") onward. Every episode keys its animation to beat
labels, so the same scene code renders both cuts (TikTok and Shorts).
"""
import json
import math


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def prog(t, a, b):
    """0 before a, 1 after b, linear between."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def e_io(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def e_out(t):
    return 1 - (1 - t) ** 3


def e_in(t):
    return t ** 3


def e_back(t, s=1.9):
    c3 = s + 1
    return 1 + c3 * (t - 1) ** 3 + s * (t - 1) ** 2


def e_elastic(t):
    if t <= 0:
        return 0.0
    if t >= 1:
        return 1.0
    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1


def bump(t, a, b):
    """Smooth 0 -> 1 -> 0 hump over [a, b]."""
    p = prog(t, a, b)
    return math.sin(math.pi * p) if 0 < p < 1 else 0.0


def fade(t, a_in, b_in, a_out=None, b_out=None):
    """Fade in over [a_in, b_in], optionally out over [a_out, b_out]."""
    v = prog(t, a_in, b_in)
    if a_out is not None:
        v *= 1 - prog(t, a_out, b_out)
    return v


def blink(t, hz=2.0):
    return 1.0 if (t * hz) % 1.0 < 0.5 else 0.0


class Timeline:
    """Beat times in video seconds, built from the voiceover timing JSON."""

    def __init__(self, vo_json, labels, lead=0.5, pause_label="cta", pause=0.6, tail=2.5):
        d = json.load(open(vo_json))
        lines = d["lines"]
        if len(lines) != len(labels):
            raise ValueError(f"{len(lines)} voice lines but {len(labels)} labels")
        self.lead, self.pause, self.pause_label = lead, pause, pause_label
        self.beats, self.lines = {}, []
        self.pause_start = None
        self.cta_vo_start = None
        shift = lead
        for lab, ln in zip(labels, lines):
            if lab == pause_label:
                self.pause_start = ln["start"] + shift
                self.cta_vo_start = ln["start"]
                shift += pause
            s, e = ln["start"] + shift, ln["end"] + shift
            self.beats[lab] = (s, e)
            self.lines.append({"label": lab, "start": s, "end": e, "text": ln["text"],
                               "vo_start": ln["start"], "vo_end": ln["end"], "words": ln.get("words")})
        self.duration = lines[-1]["end"] + shift + tail
        self.labels = labels

    def has(self, lab):
        return lab in self.beats

    def s(self, lab):
        return self.beats[lab][0]

    def e(self, lab):
        return self.beats[lab][1]

    def vo_to_video(self, vo_t):
        shift = self.lead
        if self.cta_vo_start is not None and vo_t >= self.cta_vo_start - 1e-6:
            shift += self.pause
        return vo_t + shift


class Camera:
    """Keyframed camera. key(t, cx, cy, z, dur): from t, ease to the target over dur seconds.

    A key that starts before the previous move has finished takes over from wherever the
    camera is at that moment, so overlapping keys never jump."""

    def __init__(self, cx, cy, z):
        self.keys = [(-1e9, cx, cy, z, 0.0)]

    def key(self, t, cx, cy, z, dur=1.0):
        self.keys.append((t, cx, cy, z, dur))
        self.keys.sort(key=lambda k: k[0])
        return self

    @staticmethod
    def _seg(frm, k, t):
        p = e_io(prog(t, k[0], k[0] + k[4])) if k[4] > 0 else 1.0
        return (lerp(frm[0], k[1], p), lerp(frm[1], k[2], p),
                math.exp(lerp(math.log(frm[2]), math.log(k[3]), p)))  # zoom eased in log space

    def at(self, t):
        frm = self.keys[0][1:4]
        cur = None
        for k in self.keys[1:]:
            if k[0] > t:
                break
            if cur is not None:
                frm = self._seg(frm, cur, k[0])
            cur = k
        return tuple(frm) if cur is None else self._seg(frm, cur, t)


class Track:
    """Piecewise value over time: to(t, value, dur, ease) like a camera key, for any number.
    Overlapping moves hand over from the current value (no jumps)."""

    def __init__(self, v0):
        self.keys = [(-1e9, v0, 0.0, e_io)]

    def to(self, t, v, dur=0.6, ease=e_io):
        self.keys.append((t, v, dur, ease))
        self.keys.sort(key=lambda k: k[0])
        return self

    @staticmethod
    def _seg(frm, k, t):
        p = k[3](prog(t, k[0], k[0] + k[2])) if k[2] > 0 else 1.0
        return lerp(frm, k[1], p)

    def at(self, t):
        frm = self.keys[0][1]
        cur = None
        for k in self.keys[1:]:
            if k[0] > t:
                break
            if cur is not None:
                frm = self._seg(frm, cur, k[0])
            cur = k
        return frm if cur is None else self._seg(frm, cur, t)


class Steps:
    """A count that grows in discrete steps: add(t0, dur) adds +1 with a springy ease."""

    def __init__(self, v0):
        self.v0, self.steps = v0, []

    def add(self, t0, dur=0.2, n=1):
        for i in range(n):
            self.steps.append((t0 + i * dur, dur))
        return self

    def at(self, t):
        v = self.v0
        for t0, d in self.steps:
            if t >= t0 + d:
                v += 1
            elif t > t0:
                v += e_out(prog(t, t0, t0 + d))
        return v
