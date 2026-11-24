"""Synthesise an original ambient drone bed in the reference's colour: an open fifth (root + fifth) held low and dark,
slow swells, a minor second and minor sixth drifting in for a sad Phrygian tint, a soft sub, long reverb. No samples,
no melody, no percussion, so no licence or Content ID questions.

usage: make_bed.py out.wav seconds [--root C] [--seed 3]
"""
import argparse
import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt
import pyloudnorm as pyln

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("seconds", type=float)
ap.add_argument("--root", default="C")
ap.add_argument("--seed", type=int, default=3)
ap.add_argument("--lufs", type=float, default=-24.0)
ap.add_argument("--kind", default="drone", choices=["drone", "air"], help="air = no pitched tones at all (for a no-music channel)")
a = ap.parse_args()

SR = 44100
N = int(a.seconds * SR) + SR * 4
t = np.arange(N) / SR
rng = np.random.default_rng(a.seed)
NOTES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
root_hz = 65.406 * 2 ** (NOTES[a.root] / 12)  # octave 2


def voice(freq, amp, harmonics=6, detune_cents=3.0, lfo_hz=0.05, phase=0.0):
    """Soft pad voice: a few harmonics (1/n^2), slow vibrato-free chorus from two detuned copies per channel."""
    out = np.zeros((N, 2))
    for ch, sgn in enumerate((-1, 1)):
        for k in (0, 1):
            d = (sgn * detune_cents * (0.6 + 0.4 * k)) / 1200
            f = freq * 2 ** d
            ph = rng.uniform(0, 2 * np.pi)
            for n in range(1, harmonics + 1):
                out[:, ch] += np.sin(2 * np.pi * f * n * t + ph * n) / n ** 2
    swell = 0.65 + 0.35 * np.sin(2 * np.pi * lfo_hz * t + phase)
    return out * (amp * swell)[:, None]


def window(t0, t1, fade=6.0):
    """0..1 envelope that fades in at t0 and out at t1."""
    e = np.clip((t - t0) / fade, 0, 1) * np.clip((t1 - t) / fade, 0, 1)
    return e[:, None]


bed = np.zeros((N, 2))
if a.kind == "air":
    # no notes: slow "breathing" air and a soft low rumble, like a quiet hall at night
    noise = rng.normal(0, 1, (N, 2))
    sos = butter(2, [70, 700], btype="band", fs=SR, output="sos")
    air = sosfilt(sos, noise, axis=0)
    sw = 0.55 + 0.45 * np.sin(2 * np.pi * 0.06 * t)[:, None] * np.sin(2 * np.pi * 0.023 * t + 1.1)[:, None]
    rum = sosfilt(butter(2, 90, btype="low", fs=SR, output="sos"), rng.normal(0, 1, (N, 2)), axis=0)
    bed = air * sw + 1.6 * rum
    L = int(3.5 * SR); tt = np.arange(L) / SR
    ir = rng.normal(0, 1, (L, 2)) * np.exp(-tt / 1.0)[:, None]
    wet = np.stack([fftconvolve(bed[:, c], ir[:, c])[:N] for c in range(2)], 1)
    mix = 0.6 * bed / (np.max(np.abs(bed)) + 1e-9) + 0.4 * wet / (np.max(np.abs(wet)) + 1e-9)
    mix = mix[: int(a.seconds * SR)]
    fi, fo = int(2.5 * SR), int(3.5 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None] ** 2
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    meter = pyln.Meter(SR)
    mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), a.lufs)
    sf.write(a.out, mix.astype(np.float32), SR, subtype="FLOAT")
    print(f"air bed {a.out}: {a.seconds:.1f}s, {a.lufs} LUFS")
    raise SystemExit(0)
bed += voice(root_hz, 1.0, lfo_hz=0.045)                      # root
bed += voice(root_hz * 1.5, 0.75, lfo_hz=0.037, phase=1.3)     # fifth
bed += voice(root_hz * 2, 0.45, lfo_hz=0.052, phase=2.1)       # octave
bed += voice(root_hz * 3, 0.22, harmonics=3, lfo_hz=0.061, phase=0.4)  # fifth above
# sad colour tones drifting in and out (minor second, minor sixth), like the reference's Db / Ab shading
dur = a.seconds
for i, (ratio, amp) in enumerate([(2 ** (1 / 12) * 2, 0.16), (2 ** (8 / 12) * 2, 0.18), (2 ** (1 / 12) * 2, 0.14)]):
    s = dur * (0.12 + 0.3 * i) + rng.uniform(-2, 2)
    bed += voice(root_hz * ratio, amp, harmonics=3, lfo_hz=0.03) * window(s, s + dur * 0.28)
# sub
sub = 0.35 * np.sin(2 * np.pi * root_hz / 2 * t)
bed += np.stack([sub, sub], 1) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.021 * t))[:, None]
# air: very quiet filtered noise, gives the drone a breath
noise = rng.normal(0, 1, (N, 2))
sos = butter(2, [300, 2500], btype="band", fs=SR, output="sos")
bed += 0.012 * sosfilt(sos, noise, axis=0)
# darken: low-pass at ~900 Hz (the reference keeps 96% of its energy under 1 kHz)
sos = butter(3, 900, btype="low", fs=SR, output="sos")
bed = sosfilt(sos, bed, axis=0)
# long synthetic reverb (decaying stereo noise IR)
L = int(4.5 * SR)
tt = np.arange(L) / SR
ir = rng.normal(0, 1, (L, 2)) * np.exp(-tt / 1.3)[:, None]
ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))[:, None]
wet = np.stack([fftconvolve(bed[:, c], ir[:, c])[:N] for c in range(2)], 1)
wet /= np.max(np.abs(wet)) + 1e-9
dry = bed / (np.max(np.abs(bed)) + 1e-9)
mix = 0.55 * dry + 0.45 * wet
mix = mix[: int(a.seconds * SR)]
# fade in/out
fi, fo = int(2.5 * SR), int(3.5 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None] ** 2
mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
meter = pyln.Meter(SR)
mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), a.lufs)
sf.write(a.out, mix.astype(np.float32), SR, subtype="FLOAT")
print(f"bed {a.out}: {a.seconds:.1f}s, root {a.root} ({root_hz:.1f} Hz), {a.lufs} LUFS")
