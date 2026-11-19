"""median pitch (Hz), pitch spread and length of each mp3 given: pitch.py a.mp3 b.mp3 ..."""
import subprocess, sys
import numpy as np
SR = 16000


def decode(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def f0(y, lo=110, hi=620):
    W, H = int(0.04 * SR), int(0.01 * SR)
    out = []
    pk = np.abs(y).max() + 1e-9
    for i in range(0, len(y) - W, H):
        s = y[i:i + W] * np.hanning(W)
        if np.sqrt((s ** 2).mean()) < 0.04 * pk:
            continue
        s = s - s.mean()
        ac = np.correlate(s, s, 'full')[W - 1:]
        ac /= ac[0] + 1e-12
        a, b = SR // hi, SR // lo
        k = a + int(np.argmax(ac[a:b]))
        if ac[k] > 0.5:
            out.append(SR / k)
    return np.array(out)


for p in sys.argv[1:]:
    y = decode(p); f = f0(y)
    act = np.abs(y) > 0.03 * np.abs(y).max()
    idx = np.flatnonzero(act); span = (idx[-1] - idx[0]) / SR if len(idx) else 0
    print(f"{p.split('/')[-1]:14s} f0 median {np.median(f):5.0f} Hz  p10-p90 {np.percentile(f, 10):4.0f}-{np.percentile(f, 90):4.0f}  speech {span:4.2f}s  voiced frames {len(f)}")
