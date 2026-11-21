"""Sounds for the 4-minute show ("Survival Mode"): world music beds and game jingles. Everything is synthesized here
with numpy (no samples, no licences): plucked strings (Karplus-Strong), bells, water drops, a flute, hand drums and
chip-style jingles. All functions return float32 arrays at SR; music_* return stereo (n, 2)."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
TAU = 2 * np.pi


# ------------------------------------------------------------------ basics
def _n(d):
    return max(1, int(round(d * SR)))


def _t(d):
    return np.arange(_n(d)) / SR


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR * 0.45), "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, min(hi, SR * 0.45)], "band", fs=SR, output="sos"), x)


def fade(n, a=0.004, r=0.03):
    e = np.ones(n)
    na, nr = min(n // 2, _n(a)), min(n // 2, _n(r))
    e[:na] = np.linspace(0, 1, na)
    e[n - nr:] *= np.linspace(1, 0, nr)
    return e


def decay(n, tau, a=0.002):
    t = np.arange(n) / SR
    e = np.exp(-t / tau)
    na = min(n, _n(a))
    e[:na] *= np.linspace(0, 1, na)
    return e


def noise(d, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, _n(d))


def _phase(freq, d):
    f = np.full(_n(d), float(freq)) if np.isscalar(freq) else np.asarray(freq, float)
    ph = np.cumsum(f) / SR
    return ph % 1.0, f / SR


def _blep(t, dt):
    out = np.zeros_like(t)
    m = t < dt
    x = t[m] / dt[m]
    out[m] = 2 * x - x * x - 1
    m = t > 1 - dt
    x = (t[m] - 1) / dt[m]
    out[m] = x * x + 2 * x + 1
    return out


def saw(freq, d):
    t, dt = _phase(freq, d)
    return 2 * t - 1 - _blep(t, dt)


def pulse(freq, d, duty=0.5):
    t, dt = _phase(freq, d)
    t2 = (t + duty) % 1.0
    return (2 * t - 1 - _blep(t, dt)) - (2 * t2 - 1 - _blep(t2, dt)) + (2 * duty - 1)


def tri(freq, d):
    t, _ = _phase(freq, d)
    return 2 * np.abs(2 * t - 1) - 1


def sine(freq, d):
    f = np.full(_n(d), float(freq)) if np.isscalar(freq) else np.asarray(freq, float)
    return np.sin(TAU * np.cumsum(f) / SR)


def glide(f0, f1, d, curve=1.0):
    u = np.linspace(0, 1, _n(d)) ** curve
    return f0 * (f1 / f0) ** u


# ------------------------------------------------------------------ instruments
_CACHE = {}


def pluck(f, d=1.6, bright=0.5, damp=0.996, seed=0):
    """Plucked string (Karplus-Strong): oud when dark and low, gayageum / harp when bright."""
    key = ("pl", round(f, 2), round(d, 2), bright, damp, seed)
    if key in _CACHE:
        return _CACHE[key]
    N = max(2, int(round(SR / f - 0.5)))
    n = _n(d)
    exc = np.random.default_rng(seed).uniform(-1, 1, 3 * N)
    exc = lp(exc, 700 + 9000 * bright)[2 * N:]
    exc -= exc.mean()
    exc /= np.abs(exc).max() + 1e-9
    y = np.zeros(n + 2 * N)
    y[:N] = exc
    for k in range(N, n + N, N):
        a = y[k - N:k]
        b = np.concatenate([[0.0], y[:N - 1]]) if k == N else y[k - N - 1:k - 1]
        y[k:k + N] = 0.5 * damp * (a + b)
    y = y[:n]
    f_act = SR / (N + 0.5)
    if abs(f_act / f - 1) > 0.001:                       # exact tuning
        y = np.interp(np.arange(0, n - 1, f / f_act), np.arange(n), y)
    y = (y * fade(len(y), 0.001, 0.06)).astype(np.float32)
    _CACHE[key] = y
    return y


def bell(f, d=2.2, hard=0.5):
    key = ("be", round(f, 2), round(d, 2), hard)
    if key in _CACHE:
        return _CACHE[key]
    t = _t(d)
    y = np.zeros_like(t)
    for ratio, amp, dec in ((1.0, 1.0, 1.0), (2.0, 0.45, 0.7), (2.76, 0.30 * (0.5 + hard), 0.45), (5.4, 0.16 * (0.5 + hard), 0.25),
                            (8.93, 0.07 * (0.5 + hard), 0.14)):
        if f * ratio < SR * 0.45:
            y += amp * np.sin(TAU * f * ratio * t) * np.exp(-t / (d * 0.30 * dec))
    y = (y * fade(len(y), 0.002, 0.08) * 0.6).astype(np.float32)
    _CACHE[key] = y
    return y


def drop(f=880.0, d=0.22):
    """Water drop: a short upward chirp."""
    n = _n(d)
    t = np.arange(n) / SR
    fr = f * (1 + 0.55 * (1 - np.exp(-t / 0.018)))
    return (np.sin(TAU * np.cumsum(fr) / SR) * np.exp(-t / 0.055) * fade(n, 0.002, 0.02)).astype(np.float32)


def flute(f, d, vib=5.0, depth=0.006, seed=3):
    n = _n(d)
    t = np.arange(n) / SR
    fr = f * (1 + depth * np.sin(TAU * vib * t) * np.clip((t - 0.18) / 0.3, 0, 1))
    ph = TAU * np.cumsum(fr) / SR
    y = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.07 * np.sin(3 * ph)
    y += 0.10 * bp(noise(d, seed), f * 1.6, f * 4.5)[:n]
    return (y * fade(n, 0.07, 0.14) * 0.5).astype(np.float32)


def pad(freqs, d, cut=1100.0, attack=0.5, release=0.7):
    n = _n(d)
    y = np.zeros(n)
    for i, f in enumerate(freqs):
        for det in (-0.006, 0.0, 0.007):
            y += saw(f * (1 + det), d)[:n] * (0.8 if det else 1.0)
    y = lp(y / (3 * len(freqs)), cut, 2)
    return (y * fade(n, attack, release)).astype(np.float32)


def sub(f, d, drive=1.4):
    n = _n(d)
    y = np.tanh(drive * (sine(f, d) + 0.25 * tri(f * 2, d))) / np.tanh(drive)
    return (y[:n] * fade(n, 0.01, 0.08)).astype(np.float32)


def chip(f, d, duty=0.25, vib=0.0, cut=6500.0):
    n = _n(d)
    t = np.arange(n) / SR
    fr = f * (1 + vib * np.sin(TAU * 6.5 * t)) if vib else f
    y = lp(pulse(fr, d, duty), cut, 2)
    return (y[:n] * fade(n, 0.003, 0.02) * 0.6).astype(np.float32)


# ------------------------------------------------------------------ drums
def dum(seed=0):
    d = 0.34
    y = np.sin(TAU * np.cumsum(glide(125, 58, d, 0.5)) / SR) * decay(_n(d), 0.11)
    click = np.zeros(_n(d))
    c = lp(noise(0.012, seed), 2500) * decay(_n(0.012), 0.004)
    click[:len(c)] = c
    return ((y + 0.35 * click) * 0.9).astype(np.float32)


def tek(seed=1, soft=False):
    d = 0.11
    n = _n(d)
    y = bp(noise(d, seed), 2200, 7000) * decay(n, 0.018) + 0.5 * np.sin(TAU * 940 * np.arange(n) / SR) * decay(n, 0.03)
    return (y * (0.35 if soft else 0.75)).astype(np.float32)


def shaker(seed=2, d=0.05):
    n = _n(d)
    return (hp(noise(d, seed), 6500) * decay(n, 0.014, a=0.004) * 0.35).astype(np.float32)


def kick(soft=True):
    d = 0.30
    y = np.sin(TAU * np.cumsum(glide(78, 42, d, 0.5)) / SR) * decay(_n(d), 0.13)
    return (y * (0.8 if soft else 1.0)).astype(np.float32)


def rim():
    d = 0.06
    n = _n(d)
    y = np.sin(TAU * 1750 * np.arange(n) / SR) * decay(n, 0.012) + 0.4 * hp(noise(d, 5), 3000) * decay(n, 0.006)
    return (y * 0.4).astype(np.float32)


def kung(seed=6):
    """Janggu, low side."""
    d = 0.45
    n = _n(d)
    y = np.sin(TAU * np.cumsum(glide(150, 84, d, 0.4)) / SR) * decay(n, 0.16) + 0.3 * lp(noise(d, seed), 500) * decay(n, 0.05)
    return (y * 0.85).astype(np.float32)


def deok(seed=7, soft=False):
    """Janggu, stick side."""
    d = 0.09
    n = _n(d)
    y = bp(noise(d, seed), 1400, 4200) * decay(n, 0.016) + 0.6 * np.sin(TAU * 620 * np.arange(n) / SR) * decay(n, 0.02)
    return (y * (0.35 if soft else 0.7)).astype(np.float32)


def wind(d, seed=8, lo=300, hi=1100):
    n = _n(d)
    t = np.arange(n) / SR
    y = bp(noise(d, seed), lo, hi, 2)
    sw = 0.55 + 0.45 * np.sin(TAU * 0.11 * t + 1.0) * np.sin(TAU * 0.037 * t)
    return (y * sw * fade(n, 1.5, 1.5) * 0.5).astype(np.float32)


# ------------------------------------------------------------------ stereo helpers
def stereo(n_or_d):
    n = n_or_d if isinstance(n_or_d, (int, np.integer)) else _n(n_or_d)
    return np.zeros((n, 2), np.float32)


def place(buf, snd, t, gain=1.0, pan=0.0):
    """Add a mono or stereo sound at t seconds. pan: -1 left .. 1 right (equal power)."""
    if snd is None:
        return
    i = int(round(t * SR))
    if i >= len(buf):
        return
    if i < 0:
        snd, i = snd[-i:], 0
    n = min(len(snd), len(buf) - i)
    if n <= 0:
        return
    if snd.ndim == 1:
        a = (pan + 1) * np.pi / 4
        buf[i:i + n, 0] += snd[:n] * (gain * np.cos(a) * 1.4142)
        buf[i:i + n, 1] += snd[:n] * (gain * np.sin(a) * 1.4142)
    else:
        buf[i:i + n] += snd[:n] * gain


def ramp(n, points):
    """Piecewise-linear gain curve over n samples from [(t, value), ...]."""
    pts = sorted(points)
    ts = np.array([p[0] for p in pts]) * SR
    vs = np.array([p[1] for p in pts], float)
    return np.interp(np.arange(n), ts, vs).astype(np.float32)


def _comb(x, D, g):
    y = x.copy()
    for k in range(D, len(x), D):
        seg = y[k:k + D]
        seg += g * y[k - D:k - D + len(seg)]
    return y


def _allpass(x, D, g):
    y = np.zeros_like(x)
    y[:D] = -g * x[:D]
    for k in range(D, len(x), D):
        m = min(D, len(x) - k)
        y[k:k + m] = -g * x[k:k + m] + x[k - D:k - D + m] + g * y[k - D:k - D + m]
    return y


def reverb(st, wet=0.18, size=1.0, damp=3800.0):
    """Small hall: four combs and two allpasses per side."""
    out = st.copy()
    for ch, off in ((0, 0), (1, 23)):
        x = lp(st[:, ch].astype(np.float64), damp)
        acc = np.zeros_like(x)
        for D, g in ((1557, 0.80), (1617, 0.79), (1491, 0.81), (1422, 0.82)):
            acc += _comb(x, int((D + off) * size), g)
        acc *= 0.25
        for D, g in ((225, 0.5), (556, 0.5)):
            acc = _allpass(acc, int((D + off) * size), g)
        out[:, ch] = st[:, ch] * (1 - wet * 0.3) + acc.astype(np.float32) * wet
    return out


def echo(st, delay, fb=0.35, mix=0.3, cut=3200.0):
    """Ping-pong feedback delay on a stereo buffer."""
    D = int(delay * SR)
    src = lp(st.mean(axis=1).astype(np.float64), cut).astype(np.float32)
    wet = np.zeros_like(st)
    g = 1.0
    for k in range(1, 6):
        sh = k * D
        if sh >= len(src):
            break
        wet[sh:, (k - 1) % 2] += src[:len(src) - sh] * g
        g *= fb
    return st + wet * mix


# ------------------------------------------------------------------ sequencing
def _seq(n, step, events, fn, gain=1.0, pan=0.0, swing=0.0):
    """events: [(step_index, arg...)] -> fn(*args) placed at step_index * step."""
    buf = stereo(n)
    for ev in events:
        k, args = ev[0], ev[1:]
        snd = fn(*args)
        p = pan(k) if callable(pan) else pan
        place(buf, snd, k * step + (swing * step if k % 2 else 0.0), gain, p)
    return buf


def _loop(pattern, bars, steps_per_bar):
    """Repeat a list of bar patterns over `bars` bars. pattern: list (per bar) of [(step, arg...), ...]."""
    out = []
    for b in range(bars):
        for ev in pattern[b % len(pattern)]:
            out.append((b * steps_per_bar + ev[0],) + tuple(ev[1:]))
    return out


def _layers(n, stems, gains):
    mix = stereo(n)
    for name, st in stems.items():
        g = gains.get(name)
        if g is None:
            continue
        mix += st[:n] * (g[:, None] if isinstance(g, np.ndarray) else g)
    return mix


def _curve(n, ev, plan):
    """plan: {layer: [(event_name or seconds, value), ...]} -> gain arrays. Event names come from ev (seconds)."""
    out = {}
    for name, pts in plan.items():
        res = []
        for when, val in pts:
            if isinstance(when, tuple):                    # (event, offset)
                tt = ev[when[0]] + when[1]
            else:
                tt = ev[when] if isinstance(when, str) else when
            res.append((tt, val))
        out[name] = ramp(n, res)
    return out


# Each music_* takes the level's local event times (seconds from the level card's first frame):
#   ev = {"card": 0, "a0": .., "brk": [4], "fix": [4], "b0": .., "clear": .., "c0": .., "end": ..}
def _std_plan(ev, has=("drums", "bass", "riff", "lead", "pad", "air")):
    f, e = ev["fix"], ev
    plan = {
        "pad":   [(0, 0.0), (1.2, 0.8), ("a0", 0.55), ("clear", 0.9), ("c0", 0.5), (("end", -1.2), 0.5), ("end", 0.0)],
        "drums": [(0, 0.0), (("a0", -0.6), 0.0), ("a0", 0.75), (f[0], 0.75), (f[0] + 0.3, 0.95), (("clear", -0.05), 0.95),
                  ("clear", 0.0), (("c0", -0.1), 0.0), ("c0", 0.55), (("end", -1.0), 0.55), ("end", 0.0)],
        "bass":  [(0, 0.0), (("a0", -0.3), 0.0), ("a0", 0.9), (("clear", -0.05), 0.9), ("clear", 0.25), ("c0", 0.7),
                  (("end", -1.0), 0.7), ("end", 0.0)],
        "riff":  [(0, 0.0), (f[0] - 0.1, 0.0), (f[0] + 0.4, 0.8), (("clear", -0.05), 0.9), ("clear", 0.0), ("c0", 0.0),
                  (e["c0"] + 0.5, 0.45), (("end", -1.0), 0.45), ("end", 0.0)],
        "lead":  [(0, 0.0), (f[2] - 0.1, 0.0), (f[2] + 0.6, 0.7), (("clear", -0.05), 0.8), ("clear", 0.0), ("end", 0.0)],
        "air":   [(0, 0.0), (1.0, 1.0), ("a0", 0.6), (("end", -1.5), 0.6), ("end", 0.0)],
    }
    return {k: v for k, v in plan.items() if k in has}


def music_desert(dur, ev, bpm=104.0, root=50, seed=11):
    """Level 1: D Phrygian dominant, maqsum hand drums, oud riff, a ney-like lead."""
    n = _n(dur)
    step = 60.0 / bpm / 4
    bars = int(dur / (16 * step)) + 2
    R = root
    drums = _loop([[(0, "D"), (2, "T"), (4, "k"), (6, "T"), (8, "D"), (10, "k"), (12, "T"), (14, "k"), (15, "k")]], bars, 16)
    hit = {"D": lambda: dum(1), "T": lambda: tek(2), "k": lambda: tek(3, soft=True)}
    st_dr = _seq(n, step, [(k, h) for k, h in drums], lambda h: hit[h](), 0.9)
    st_dr += _seq(n, step, [(k,) for k in range(bars * 16)], lambda: shaker(4), 0.35, pan=lambda k: 0.5 if k % 2 else -0.5)
    chords = [(0, 4, 7), (0, 4, 7), (1, 5, 8), (-2, 1, 5)]        # D, D, Eb, Cm
    bassn = [[(0, R - 12), (6, R - 12), (8, R - 5), (14, R - 12)], [(0, R - 12), (6, R - 12), (8, R - 5), (12, R - 2), (14, R - 12)],
             [(0, R - 11), (6, R - 11), (8, R - 4), (14, R - 11)], [(0, R - 14), (6, R - 14), (8, R - 12), (12, R - 8), (14, R - 12)]]
    st_ba = _seq(n, step, _loop(bassn, bars, 16), lambda m: _bass_note(m, seed), 0.95)
    riff = [[(0, R + 12), (2, R + 13), (3, R + 16), (4, R + 17), (6, R + 16), (8, R + 13), (10, R + 12), (12, R + 16), (14, R + 13)],
            [(0, R + 12), (3, R + 19), (4, R + 20), (6, R + 19), (8, R + 17), (10, R + 16), (12, R + 13), (14, R + 12)],
            [(0, R + 13), (2, R + 17), (3, R + 20), (4, R + 22), (6, R + 20), (8, R + 17), (10, R + 13), (12, R + 17), (14, R + 20)],
            [(0, R + 10), (2, R + 13), (4, R + 17), (6, R + 13), (8, R + 12), (10, R + 16), (12, R + 19), (14, R + 16)]]
    st_ri = _seq(n, step, _loop(riff, bars, 16), lambda m: pluck(midi(m), 0.8, bright=0.42, damp=0.9955, seed=seed + 1), 0.6,
                 pan=lambda k: -0.25 if (k // 2) % 2 else 0.25)
    st_ri = echo(st_ri, step * 3, fb=0.3, mix=0.22)
    lead = [[(0, R + 19, 6), (6, R + 20, 2), (8, R + 19, 4), (12, R + 17, 2), (14, R + 16, 2)],
            [(0, R + 17, 4), (4, R + 16, 4), (8, R + 13, 4), (12, R + 12, 4)],
            [(0, R + 17, 6), (6, R + 20, 4), (10, R + 22, 2), (12, R + 20, 4)],
            [(0, R + 19, 4), (4, R + 17, 2), (6, R + 16, 2), (8, R + 13, 4), (12, R + 12, 4)]]
    st_le = _seq(n, step, _loop(lead, bars, 16), lambda m, ln: flute(midi(m), ln * step * 0.98), 0.5, pan=0.1)
    st_pa = stereo(n)
    for b in range(bars):
        ch = chords[b % 4]
        place(st_pa, pad([midi(R + 12 + c) for c in ch], 16 * step + 0.5, cut=900), b * 16 * step, 0.5,
              pan=-0.3 if b % 2 else 0.3)
    g = _curve(n, ev, _std_plan(ev, ("drums", "bass", "riff", "lead", "pad")))
    mix = _layers(n, {"drums": st_dr, "bass": st_ba, "riff": st_ri, "lead": st_le, "pad": st_pa}, g)
    return reverb(mix, wet=0.16)


def _bass_note(m, seed=0, d=0.9):
    p = pluck(midi(m), d, bright=0.16, damp=0.994, seed=seed)
    s = sub(midi(m), min(d, 0.34)) * 0.55
    out = p.copy()
    out[:len(s)] += s[:len(out)] * decay(len(s), 0.16)[:len(out)]
    return out


def music_oasis(dur, ev, bpm=96.0, root=57, seed=21):
    """Level 2: A Phrygian dominant, slower saidi groove, water-drop plucks with echo, oud bass, flute."""
    n = _n(dur)
    step = 60.0 / bpm / 4
    bars = int(dur / (16 * step)) + 2
    R = root
    hit = {"D": lambda: dum(3), "T": lambda: tek(4), "k": lambda: tek(5, soft=True)}
    drums = _loop([[(0, "D"), (2, "T"), (6, "D"), (8, "D"), (10, "k"), (12, "T"), (14, "k")]], bars, 16)
    st_dr = _seq(n, step, [(k, h) for k, h in drums], lambda h: hit[h](), 0.85)
    st_dr += _seq(n, step, [(k,) for k in range(0, bars * 16, 2)], lambda: shaker(6, 0.06), 0.3, pan=lambda k: 0.4 if (k // 2) % 2 else -0.4)
    bassn = [[(0, R - 24), (6, R - 24), (8, R - 17), (14, R - 24)], [(0, R - 24), (6, R - 24), (8, R - 17), (12, R - 14)],
             [(0, R - 23), (6, R - 23), (8, R - 16), (14, R - 23)], [(0, R - 26), (6, R - 26), (8, R - 24), (12, R - 20), (14, R - 24)]]
    st_ba = _seq(n, step, _loop(bassn, bars, 16), lambda m: _bass_note(m, seed), 0.95)
    drops = [[(0, R + 12), (3, R + 16), (6, R + 19), (10, R + 16), (12, R + 13)], [(0, R + 12), (4, R + 19), (6, R + 20), (10, R + 19), (14, R + 16)],
             [(0, R + 13), (3, R + 17), (6, R + 20), (10, R + 17), (12, R + 13)], [(0, R + 10), (4, R + 13), (8, R + 12), (10, R + 16), (14, R + 19)]]
    st_ri = _seq(n, step, _loop(drops, bars, 16), lambda m: drop(midi(m)), 0.5, pan=lambda k: -0.5 if (k // 3) % 2 else 0.5)
    st_ri += _seq(n, step, _loop(drops, bars, 16), lambda m: pluck(midi(m - 12), 0.7, bright=0.35, damp=0.995, seed=seed + 2), 0.38)
    st_ri = echo(st_ri, step * 3, fb=0.42, mix=0.38, cut=2600)
    lead = [[(0, R + 16, 8), (8, R + 17, 4), (12, R + 16, 4)], [(0, R + 13, 6), (6, R + 12, 10)],
            [(0, R + 17, 6), (6, R + 20, 6), (12, R + 17, 4)], [(0, R + 17, 4), (4, R + 13, 4), (8, R + 12, 8)]]
    st_le = _seq(n, step, _loop(lead, bars, 16), lambda m, ln: flute(midi(m), ln * step * 0.98, vib=4.6), 0.45, pan=-0.1)
    st_pa = stereo(n)
    chords = [(0, 4, 7), (0, 4, 7), (1, 5, 8), (-2, 1, 5)]
    for b in range(bars):
        place(st_pa, pad([midi(R + c) for c in chords[b % 4]], 16 * step + 0.5, cut=850), b * 16 * step, 0.5, pan=0.3 if b % 2 else -0.3)
    g = _curve(n, ev, _std_plan(ev, ("drums", "bass", "riff", "lead", "pad")))
    mix = _layers(n, {"drums": st_dr, "bass": st_ba, "riff": st_ri, "lead": st_le, "pad": st_pa}, g)
    return reverb(mix, wet=0.2)


def music_arctic(dur, ev, bpm=84.0, root=52, seed=31):
    """Level 3: E minor, glassy bells, a slow heartbeat kick, long sub notes and wind."""
    n = _n(dur)
    step = 60.0 / bpm / 4
    bars = int(dur / (16 * step)) + 2
    R = root
    st_dr = _seq(n, step, _loop([[(0, "K"), (3, "k"), (8, "K"), (12, "r")], [(0, "K"), (3, "k"), (8, "K"), (11, "k"), (12, "r"), (14, "r")]], bars, 16),
                 lambda h: {"K": kick(False), "k": kick(True) * 0.6, "r": rim()}[h], 0.8)
    st_dr += _seq(n, step, [(k,) for k in range(2, bars * 16, 4)], lambda: shaker(9, 0.08), 0.22, pan=lambda k: 0.5 if (k // 4) % 2 else -0.5)
    prog_ = [R - 24, R - 24, R - 28, R - 26]              # E, E, C, D
    st_ba = _seq(n, step, _loop([[(0, m, 15)] for m in prog_], bars, 16), lambda m, ln: sub(midi(m + 12), ln * step, 1.1) * 0.7, 0.5)
    arp = [[(0, R + 12), (2, R + 19), (4, R + 15), (6, R + 22), (8, R + 19), (10, R + 15), (12, R + 24), (14, R + 19)],
           [(0, R + 12), (2, R + 19), (4, R + 15), (6, R + 22), (8, R + 26), (10, R + 22), (12, R + 19), (14, R + 15)],
           [(0, R + 8), (2, R + 15), (4, R + 12), (6, R + 19), (8, R + 15), (10, R + 12), (12, R + 24), (14, R + 19)],
           [(0, R + 10), (2, R + 17), (4, R + 14), (6, R + 22), (8, R + 17), (10, R + 14), (12, R + 22), (14, R + 17)]]
    st_ri = _seq(n, step, _loop(arp, bars, 16), lambda m: bell(midi(m), 1.6, 0.35), 0.42, pan=lambda k: -0.45 if (k // 2) % 2 else 0.45)
    st_ri = echo(st_ri, step * 3, fb=0.4, mix=0.3, cut=4200)
    lead = [[(0, R + 24, 8), (8, R + 22, 4), (12, R + 19, 4)], [(0, R + 22, 6), (6, R + 19, 10)],
            [(0, R + 20, 8), (8, R + 19, 4), (12, R + 15, 4)], [(0, R + 17, 6), (6, R + 22, 4), (10, R + 26, 6)]]
    st_le = _seq(n, step, _loop(lead, bars, 16), lambda m, ln: bell(midi(m), max(1.8, ln * step * 1.6), 0.7), 0.5)
    st_pa = stereo(n)
    chords = [(0, 3, 7, 10), (0, 3, 7, 10), (-4, 0, 3, 7), (-2, 2, 5, 12)]      # Em7, Em7, Cmaj7, Dadd9
    for b in range(bars):
        place(st_pa, pad([midi(R + c) for c in chords[b % 4]], 16 * step + 0.8, cut=1300, attack=0.9, release=0.9), b * 16 * step, 0.55,
              pan=-0.3 if b % 2 else 0.3)
    st_air = stereo(n)
    w = wind(dur + 0.5, seed)
    place(st_air, w, 0, 0.55, -0.4)
    place(st_air, wind(dur + 0.5, seed + 1, 500, 1700), 0, 0.4, 0.5)
    g = _curve(n, ev, _std_plan(ev))
    mix = _layers(n, {"drums": st_dr, "bass": st_ba, "riff": st_ri, "lead": st_le, "pad": st_pa, "air": st_air}, g)
    return reverb(mix, wet=0.26, size=1.25)


def music_ondol(dur, ev, bpm=74.0, root=55, seed=41):
    """Level 4: G pentatonic in a 12/8 lilt, gayageum-like plucks, janggu drum, warm pad."""
    n = _n(dur)
    step = 60.0 / bpm / 3                                   # eighth-note triplets, 12 per bar
    bars = int(dur / (12 * step)) + 2
    R = root
    st_dr = _seq(n, step, _loop([[(0, "K"), (3, "d"), (6, "D"), (8, "d"), (9, "K"), (11, "d")], [(0, "K"), (3, "d"), (5, "d"), (6, "D"), (9, "K"), (10, "d"), (11, "D")]], bars, 12),
                 lambda h: {"K": kung(), "D": deok(), "d": deok(soft=True)}[h], 0.8)
    st_ba = _seq(n, step, _loop([[(0, R - 24), (6, R - 17), (9, R - 24)], [(0, R - 17), (6, R - 10), (9, R - 17)],
                                 [(0, R - 27), (6, R - 20), (9, R - 24)], [(0, R - 17), (6, R - 22), (9, R - 17)]], bars, 12),
                 lambda m: _bass_note(m, seed, 1.1), 0.9)
    riff = [[(0, R + 19), (2, R + 21), (3, R + 24), (5, R + 21), (6, R + 19), (8, R + 16), (9, R + 14), (11, R + 12)],
            [(0, R + 14), (2, R + 16), (3, R + 19), (5, R + 21), (6, R + 24), (8, R + 21), (9, R + 19), (11, R + 16)],
            [(0, R + 21), (2, R + 19), (3, R + 16), (5, R + 14), (6, R + 12), (8, R + 14), (9, R + 16), (11, R + 19)],
            [(0, R + 19), (2, R + 16), (3, R + 14), (5, R + 12), (6, R + 14), (8, R + 16), (9, R + 19), (11, R + 14)]]
    st_ri = _seq(n, step, _loop(riff, bars, 12), lambda m: pluck(midi(m), 1.3, bright=0.62, damp=0.997, seed=seed + 1), 0.5,
                 pan=lambda k: -0.3 if (k // 3) % 2 else 0.3)
    st_ri = echo(st_ri, step * 2, fb=0.28, mix=0.2)
    lead = [[(0, R + 24, 6), (6, R + 26, 3), (9, R + 24, 3)], [(0, R + 21, 6), (6, R + 19, 6)],
            [(0, R + 28, 6), (6, R + 26, 3), (9, R + 24, 3)], [(0, R + 21, 3), (3, R + 19, 3), (6, R + 24, 6)]]
    st_le = _seq(n, step, _loop(lead, bars, 12), lambda m, ln: flute(midi(m), ln * step * 0.98, vib=4.2, depth=0.009), 0.42, pan=0.15)
    st_pa = stereo(n)
    chords = [(0, 4, 7, 9), (-5, 2, 7, 9), (-3, 4, 7, 12), (2, 7, 9, 14)]   # G6, D, Em7, Dsus
    for b in range(bars):
        place(st_pa, pad([midi(R + c) for c in chords[b % 4]], 12 * step + 0.6, cut=1000), b * 12 * step, 0.5, pan=0.3 if b % 2 else -0.3)
    g = _curve(n, ev, _std_plan(ev, ("drums", "bass", "riff", "lead", "pad")))
    mix = _layers(n, {"drums": st_dr, "bass": st_ba, "riff": st_ri, "lead": st_le, "pad": st_pa}, g)
    return reverb(mix, wet=0.2)


MUSIC = {"desert": music_desert, "oasis": music_oasis, "arctic": music_arctic, "ondol": music_ondol}


# ------------------------------------------------------------------ game jingles and stings (mono unless noted)
def _notes(seq, wave=chip, gap=0.0, **kw):
    """seq: [(midi, seconds)] played one after another."""
    parts = []
    for m, d in seq:
        parts.append(wave(midi(m), d, **kw) if m is not None else np.zeros(_n(d), np.float32))
        if gap:
            parts.append(np.zeros(_n(gap), np.float32))
    return np.concatenate(parts)


def press_start():
    return _notes([(83, 0.07), (88, 0.16)], duty=0.5) * 0.8


def level_start():
    y = _notes([(76, 0.07), (80, 0.07), (83, 0.07), (88, 0.22)], duty=0.25)
    return y * 0.8


def boss_appear():
    d = 1.1
    n = _n(d)
    f = glide(midi(38), midi(35), d, 0.6)
    y = lp(pulse(f, d, 0.5) + pulse(f * 1.4142, d, 0.3) * 0.8, 900) * decay(n, 0.45, a=0.01)
    y += 0.6 * lp(noise(d, 12), 220) * decay(n, 0.35)
    y += 0.5 * np.sin(TAU * np.cumsum(glide(90, 34, d, 0.5)) / SR) * decay(n, 0.5)
    return (np.tanh(y * 1.3) * 0.8).astype(np.float32)


def boss_attack():
    y = _notes([(75, 0.06), (69, 0.06), (75, 0.06), (69, 0.09)], duty=0.5, cut=4500) * 0.7
    low = np.sin(TAU * np.cumsum(glide(140, 60, 0.3, 0.5)) / SR) * decay(_n(0.3), 0.12)
    out = np.zeros(max(len(y), len(low)), np.float32)
    out[:len(y)] += y
    out[:len(low)] += low * 0.7
    return out


def boss_hit(tonic=76):
    d = 0.14
    zap = lp(pulse(glide(1100, 180, d, 0.7), d, 0.5), 5000) * decay(_n(d), 0.06) * 0.6
    crack = hp(noise(0.05, 14), 2500) * decay(_n(0.05), 0.012) * 0.6
    coin = _notes([(tonic + 7, 0.06), (tonic + 12, 0.20)], duty=0.5) * 0.75
    out = np.zeros(_n(0.07) + len(coin), np.float32)
    out[:len(zap)] += zap.astype(np.float32)
    out[:len(crack)] += crack.astype(np.float32)
    out[_n(0.07):] += coin
    return out


def _fall(x, n, f_hi=5000.0, f_mid=1200.0, f_lo=250.0, up=False):
    """Noise whose brightness falls (or rises) over time: three filtered copies blended."""
    u = np.linspace(0, 1, n)
    if up:
        u = 1 - u
    return lp(x, f_hi)[:n] * (1 - u) ** 2 + lp(x, f_mid)[:n] * 2 * u * (1 - u) + lp(x, f_lo)[:n] * u ** 2


def boss_down(tonic=72, minor=False):
    d = 0.7
    n = _n(d)
    y = _fall(noise(d, 15), n) * decay(n, 0.22) * 0.9 + np.sin(TAU * np.cumsum(glide(110, 30, d, 0.5)) / SR) * decay(n, 0.3) * 0.8
    third = 3 if minor else 4
    fan = _notes([(tonic + k, 0.30 if k == 19 else 0.07) for k in (0, third, 7, 12, 12 + third, 19)], duty=0.25) * 0.8
    out = np.zeros(_n(0.28) + len(fan), np.float32)
    m = min(n, len(out))
    out[:m] += y.astype(np.float32)[:m]
    out[_n(0.28):] += fan
    return out


def achievement(tonic=79, minor=False):
    """Bright rising chime on the level's home chord, with a sparkle tail."""
    out = np.zeros(_n(1.7), np.float32)
    third = 3 if minor else 4
    scale = (0, 2, third, 7, 9, 12)
    for i, (m, t0) in enumerate(((tonic, 0.0), (tonic + third, 0.09), (tonic + 7, 0.18), (tonic + 12, 0.27))):
        b = bell(midi(m), 1.3, 0.6)
        out[_n(t0):_n(t0) + len(b)] += b[:len(out) - _n(t0)] * (0.7 + 0.1 * i)
        c = chip(midi(m), 0.09, 0.25) * 0.35
        out[_n(t0):_n(t0) + len(c)] += c
    rng = np.random.default_rng(16)
    for k in range(10):
        t0 = 0.4 + 0.07 * k
        s = bell(midi(tonic + 12 + scale[int(rng.integers(0, len(scale)))]), 0.5, 0.2) * 0.16
        out[_n(t0):_n(t0) + len(s)] += s[:len(out) - _n(t0)]
    return out


def score_tick():
    return chip(midi(96), 0.03, 0.5) * 0.5


def coin(tonic=76):
    return _notes([(tonic + 7, 0.05), (tonic + 12, 0.14)], duty=0.5) * 0.7


def whoosh(d=0.5, up=True, seed=17):
    n = _n(d)
    x = hp(noise(d, seed), 250)
    y = _fall(x, n, 6500.0, 1800.0, 500.0, up=up)
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return (y * e * 0.7).astype(np.float32)


def riser(d=1.6, seed=18):
    n = _n(d)
    u = np.linspace(0, 1, n)
    y = lp(saw(glide(110, 880, d, 1.6), d), 5000) * 0.35 * u ** 1.5
    y += whoosh(d, True, seed)[:n] * (0.4 + 0.8 * u)
    return (y * fade(n, 0.05, 0.01)).astype(np.float32)


def slam():
    """Title impact: sub drop, crack and a power chord."""
    d = 1.6
    n = _n(d)
    y = np.sin(TAU * np.cumsum(glide(120, 33, d, 0.45)) / SR) * decay(n, 0.5) * 1.0
    y += lp(noise(d, 19), 2600) * decay(n, 0.09) * 0.7
    ch = sum(lp(saw(midi(m), d), 2400) for m in (38, 45, 50, 57)) / 4 * decay(n, 0.7, a=0.004)
    return (np.tanh((y + ch * 0.9) * 1.2) * 0.85).astype(np.float32)


def hit(seed=20):
    """Dry cinematic hit for the cold-open words."""
    d = 0.6
    n = _n(d)
    y = np.sin(TAU * np.cumsum(glide(95, 40, d, 0.4)) / SR) * decay(n, 0.2)
    y += lp(noise(d, seed), 1800) * decay(n, 0.05) * 0.8
    return (np.tanh(y * 1.4) * 0.8).astype(np.float32)


def victory(base=67):
    """End fanfare: I - IV - V - I (from the tonic `base`) in chip brass with a bell on top."""
    one, four, five, top = ((base + k, base + k + 4, base + k + 7) for k in (0, 5, 7, 12))
    seq = [(one, 0.16), (one, 0.16), (one, 0.16), (four, 0.34), (five, 0.34), (top, 0.9)]
    out = np.zeros(_n(sum(d for _, d in seq) + 1.2), np.float32)
    t0 = 0.0
    for ch, d in seq:
        for m in ch:
            c = chip(midi(m), d * 0.95, 0.25, vib=0.004) * 0.33
            out[_n(t0):_n(t0) + len(c)] += c
        low = sub(midi(ch[0] - 24), d * 0.95) * 0.3
        out[_n(t0):_n(t0) + len(low)] += low
        t0 += d
    ring = bell(midi(base + 24), 1.6, 0.5) * 0.4
    i = _n(t0 - 0.9)
    out[i:i + len(ring)] += ring[:len(out) - i]
    return out


def drone(d, root=38):
    n = _n(d)
    y = lp(saw(midi(root), d) + saw(midi(root) * 1.004, d) + 0.6 * saw(midi(root + 7), d), 380) / 2.6
    t = np.arange(n) / SR
    return (y * (0.7 + 0.3 * np.sin(TAU * 0.5 * t)) * fade(n, 0.6, 0.4) * 0.6).astype(np.float32)


def tick(hi=False):
    d = 0.03
    return (hp(noise(d, 22), 4000 if hi else 2500) * decay(_n(d), 0.006) * 0.5).astype(np.float32)
