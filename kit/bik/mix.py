"""Place the voiceover and sound effects on the video timeline and master to -14 LUFS."""
import json
import subprocess
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from .sfx import SR


def _load_mono(path):
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g).astype(np.float32)
    return x


def build_mix(tl, vo_wav, events, out_wav, sfx_db=-11.0):
    """events: list of (time_s, samples, gain_db). Writes a mastered stereo WAV."""
    total = int((tl.duration + 0.5) * SR)
    vo_track = np.zeros(total, np.float32)
    fx_track = np.zeros(total, np.float32)
    vo = _load_mono(vo_wav)
    cut = int(tl.cta_vo_start * SR) if tl.cta_vo_start is not None else len(vo)
    parts = [(vo[:cut], tl.lead), (vo[cut:], tl.lead + (cut / SR) + tl.pause)]
    for seg, start in parts:
        i = int(start * SR)
        n = min(len(seg), total - i)
        vo_track[i: i + n] += seg[:n]
    for t, snd, gain in events:
        if snd is None or t is None:
            continue
        i = int(t * SR)
        if i >= total or i + len(snd) <= 0:
            continue
        a = max(0, -i)
        n = min(len(snd) - a, total - max(i, 0))
        fx_track[max(i, 0): max(i, 0) + n] += snd[a: a + n] * (10 ** ((gain + sfx_db) / 20))
    # gentle ducking: effects dip 4 dB while the voice is talking
    env = np.abs(vo_track)
    k = int(0.05 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = 1 - 0.37 * np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)
    mixd = vo_track + fx_track * duck
    mixd = np.tanh(mixd * 1.2) / 1.2
    raw = out_wav.replace(".wav", "_raw.wav")
    sf.write(raw, np.stack([mixd, mixd], axis=1), SR)
    master(raw, out_wav)
    return out_wav


def master(src, dst, target=-14.0):
    pre = "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2"
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af",
                        f"{pre},loudnorm=I={target}:TP=-1.7:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
    flt = (f"{pre},loudnorm=I={target}:TP=-1.7:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
           f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true"
           f",aresample={SR},alimiter=limit=0.776:attack=2:release=60:level=0")   # brick wall at -2.2 dBFS: AAC adds up to ~1 dB
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", flt, "-ar", str(SR), dst],
                   check=True)
