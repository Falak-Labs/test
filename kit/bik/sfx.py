"""Synthesized sound effects (48 kHz mono float32). All made in code: no licenses needed."""
import numpy as np
from scipy import signal

SR = 48000


def _t(d):
    return np.arange(int(d * SR)) / SR


def _rng(seed):
    return np.random.default_rng(seed)


def _norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1.0
    return (x / m * peak).astype(np.float32)


def _lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc / (SR / 2), 0.99), "low")
    return signal.lfilter(b, a, x)


def _hp(x, fc, order=2):
    b, a = signal.butter(order, min(fc / (SR / 2), 0.99), "high")
    return signal.lfilter(b, a, x)


def _bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), min(hi / (SR / 2), 0.99)], "band")
    return signal.lfilter(b, a, x)


def _sweep(f0, f1, d, exp=True):
    t = _t(d)
    if exp:
        f = f0 * (f1 / f0) ** (t / d)
    else:
        f = f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def _env(n, attack=0.005, decay=0.2):
    t = np.arange(n) / SR
    e = np.exp(-t / decay)
    a = int(attack * SR)
    if a > 0:
        e[:a] *= np.linspace(0, 1, a)
    return e


def _ar(n, attack, release):
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def pop(seed=0):
    x = _sweep(620, 170, 0.09) * _env(int(0.09 * SR), 0.002, 0.04)
    return _norm(x, 0.8)


def click(seed=1):
    n = int(0.03 * SR)
    x = _hp(_rng(seed).standard_normal(n), 2500) * _env(n, 0.0005, 0.004)
    x += 0.4 * np.sin(2 * np.pi * 2400 * _t(0.03)) * _env(n, 0.001, 0.01)
    return _norm(x, 0.7)


def clank(f0=380.0, d=0.7, seed=2):
    t = _t(d)
    n = len(t)
    x = np.zeros(n)
    for ratio, dec, amp in ((1, 0.30, 1.0), (2.32, 0.20, 0.6), (3.89, 0.14, 0.45), (5.41, 0.09, 0.3), (7.1, 0.06, 0.2)):
        x += amp * np.sin(2 * np.pi * f0 * ratio * t + _rng(seed).uniform(0, 6)) * np.exp(-t / dec)
    tr = _hp(_rng(seed + 1).standard_normal(n), 1500) * _env(n, 0.0005, 0.012)
    return _norm(x * 0.8 + tr * 0.6, 0.85)


def thud(d=0.4, seed=3):
    t = _t(d)
    x = _sweep(120, 45, d) * np.exp(-t / 0.11)
    nz = _lp(_rng(seed).standard_normal(len(t)), 300) * np.exp(-t / 0.05)
    return _norm(x + nz * 0.6, 0.95)


def thunk(seed=4):
    a = thud(0.35, seed)
    b = clank(240, 0.35, seed)
    n = max(len(a), len(b))
    out = np.zeros(n)
    out[: len(a)] += a
    out[: len(b)] += 0.35 * b
    return _norm(out, 0.9)


def snap(seed=5):
    d = 0.9
    n = int(d * SR)
    crack = _hp(_rng(seed).standard_normal(int(0.04 * SR)), 1800) * _env(int(0.04 * SR), 0.0005, 0.01)
    # plucked string (Karplus-Strong) with a falling pitch
    f0 = 170.0
    buf = _rng(seed + 1).uniform(-1, 1, int(SR / f0))
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx % len(buf)]
        nxt = (idx + 1) % len(buf)
        buf[idx % len(buf)] = 0.996 * 0.5 * (buf[idx % len(buf)] + buf[nxt])
        idx += 1
    out *= np.exp(-np.arange(n) / SR / 0.35)
    out[: len(crack)] += crack * 1.4
    return _norm(out, 0.95)


def alarm(beeps=3, f=900.0, on=0.13, off=0.09):
    seg = []
    for _ in range(beeps):
        t = _t(on)
        sq = np.sign(np.sin(2 * np.pi * f * t)) * 0.6 + np.sin(2 * np.pi * f * 2 * t) * 0.2
        seg.append(_lp(sq, 4000) * _ar(len(t), 0.004, 0.02))
        seg.append(np.zeros(int(off * SR)))
    return _norm(np.concatenate(seg), 0.6)


def buzz(d=0.42):
    t = _t(d)
    x = np.sign(np.sin(2 * np.pi * 110 * t)) + 0.8 * np.sign(np.sin(2 * np.pi * 116.5 * t))
    return _norm(_lp(x, 1400) * _ar(len(t), 0.01, 0.08), 0.55)


def bell(f, d=1.2, amp=1.0):
    t = _t(d)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.0 * t) + 0.12 * np.sin(2 * np.pi * f * 3.01 * t))
    return amp * x * _env(len(t), 0.002, d / 3.5)


def chime():
    notes = (1046.5, 1318.5, 1568.0, 2093.0)
    out = np.zeros(int(1.4 * SR))
    for i, f in enumerate(notes):
        b = bell(f, 1.0, 0.8)
        o = int(i * 0.07 * SR)
        out[o: o + len(b)] += b[: len(out) - o]
    return _norm(out, 0.6)


def ding():
    out = np.zeros(int(2.2 * SR))
    for f, o in ((1318.5, 0.0), (1046.5, 0.32)):
        b = bell(f, 1.8, 1.0)
        i = int(o * SR)
        out[i: i + len(b)] += b[: len(out) - i]
    return _norm(out, 0.7)


def power_down(d=1.3, seed=6):
    t = _t(d)
    x = _sweep(320, 32, d) + 0.4 * _sweep(640, 64, d)
    nz = _lp(_rng(seed).standard_normal(len(t)), 600) * 0.15
    return _norm((x + nz) * np.linspace(1, 0, len(t)) ** 0.7, 0.85)


def hum(d=2.0, f=98.0):
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 7))
    x *= 1 + 0.15 * np.sin(2 * np.pi * 5.5 * t)
    return _norm(_lp(x, 700) * _ar(len(t), 0.15, 0.25), 0.5)


def whirr(d=2.0, f0=150.0, f1=230.0, seed=7):
    t = _t(d)
    tone = _sweep(f0, f1, d, exp=False) + 0.5 * _sweep(f0 * 2, f1 * 2, d, exp=False)
    nz = _bp(_rng(seed).standard_normal(len(t)), 300, 1800) * 0.4
    return _norm((tone * 0.6 + nz) * _ar(len(t), 0.2, 0.3), 0.5)


def whoosh(d=0.55, up=True, seed=8):
    n = int(d * SR)
    x = _rng(seed).standard_normal(n)
    out = np.zeros(n)
    chunks = 24
    for k in range(chunks):
        a, b = k * n // chunks, (k + 1) * n // chunks
        frac = k / (chunks - 1)
        fc = 400 + 3600 * (frac if up else 1 - frac)
        out[a:b] = _bp(x[max(0, a - 2000):b], fc * 0.6, fc * 1.4)[-(b - a):]
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return _norm(out * env, 0.6)


def sparkle(d=0.7, n=9, seed=9):
    out = np.zeros(int(d * SR))
    r = _rng(seed)
    for _ in range(n):
        f = r.uniform(3000, 6500)
        o = int(r.uniform(0, d - 0.15) * SR)
        b = np.sin(2 * np.pi * f * _t(0.15)) * _env(int(0.15 * SR), 0.001, 0.04)
        out[o: o + len(b)] += b * r.uniform(0.4, 1.0)
    return _norm(out, 0.45)


def sizzle(d=0.6, seed=10):
    n = int(d * SR)
    r = _rng(seed)
    x = np.zeros(n)
    idx = r.integers(0, n, 400)
    x[idx] = r.uniform(-1, 1, 400)
    x = _hp(x, 2000) * np.linspace(1, 0, n)
    return _norm(x, 0.6)


def beep(f=1700.0, d=0.09):
    return _norm(np.sin(2 * np.pi * f * _t(d)) * _ar(int(d * SR), 0.003, 0.03), 0.5)


def ring(d=1.3):
    t = _t(d)
    tone = (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * (np.sin(2 * np.pi * 20 * t) > 0)
    gate = ((t % 0.65) < 0.45).astype(float)
    return _norm(tone * gate * _ar(len(t), 0.01, 0.05), 0.45)


def hiss(d=0.5, seed=11):
    n = int(d * SR)
    x = _bp(_rng(seed).standard_normal(n), 900, 4500)
    return _norm(x * np.sin(np.linspace(0, np.pi, n)), 0.45)


def lock_click(seed=12):
    a = click(seed)
    b = clank(1300, 0.12, seed)
    out = np.zeros(max(len(a), len(b)))
    out[: len(a)] += a
    out[: len(b)] += b * 0.5
    return _norm(out, 0.7)


def charge_up(d=0.8):
    return _norm(_sweep(300, 1400, d) * _ar(int(d * SR), 0.02, 0.15), 0.4)


def riser(d=1.2, seed=13):
    t = _t(d)
    nz = _bp(_rng(seed).standard_normal(len(t)), 500, 5000) * (t / d) ** 2
    return _norm(nz + 0.3 * _sweep(200, 900, d) * (t / d), 0.5)


def creak(d=1.0, seed=14):
    t = _t(d)
    f = 70 + 30 * np.sin(2 * np.pi * 1.3 * t) + _rng(seed).normal(0, 3, len(t)).cumsum() * 0.0
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    x = _bp(x, 250, 1400) * (0.5 + 0.5 * np.sin(2 * np.pi * 2.2 * t) ** 2)
    return _norm(x * _ar(len(t), 0.05, 0.1), 0.3)


def tick():
    return _norm(click(15) * 0.6, 0.5)


def womp():
    """Sad-trombone 'wah wah wah waaah' for the comedy tag: four falling notes, the last one wobbling."""
    out = []
    notes = ((311.1, 300.0, 0.30), (293.7, 283.0, 0.30), (277.2, 266.0, 0.30), (261.6, 246.9, 0.85))
    for i, (f0, f1, d) in enumerate(notes):
        t = _t(d)
        f = np.linspace(f0, f1, len(t))
        if i == len(notes) - 1:
            f = f * (1 + 0.018 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.25, 0, 1))
        ph = np.cumsum(f) / SR
        saw = 2 * (ph % 1.0) - 1
        x = _lp(_lp(saw, 1500), 1100) * _ar(len(t), 0.025, 0.09 if i < 3 else 0.3)
        out.append(x)
        out.append(np.zeros(int(0.03 * SR)))
    return _norm(np.concatenate(out), 0.8)


def tap(seed=0):
    """A light plastic button tap for button-mashing."""
    r = _rng(100 + seed)
    t = _t(0.05)
    x = _bp(r.normal(0, 1, len(t)), 1800, 5200) * _env(len(t), 0.0005, 0.012)
    x += 0.4 * np.sin(2 * np.pi * (1100 + 80 * (seed % 3)) * t) * _env(len(t), 0.0005, 0.02)
    return _norm(x, 0.7)
