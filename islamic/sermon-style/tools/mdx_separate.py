"""Minimal MDX-Net (UVR) separation with onnxruntime + numpy (no torch).
usage: mdx_separate.py model.onnx n_fft compensate in.wav out_primary.wav out_rest.wav
Input must be 44.1 kHz stereo.
"""
import sys
import numpy as np
import soundfile as sf
import onnxruntime as ort

model_path, n_fft, comp, src, out_p, out_r = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
hop, dim_f, dim_t = 1024, 3072, 256
n_bins = n_fft // 2 + 1
trim = n_fft // 2
chunk = hop * (dim_t - 1)
gen = chunk - 2 * trim
win = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n_fft) / n_fft)  # periodic hann


def stft(x):  # x: [chunk] -> [n_bins, dim_t] complex (torch.stft center=True, reflect)
    xp = np.pad(x, (n_fft // 2, n_fft // 2), mode="reflect")
    idx = np.arange(n_fft)[None, :] + hop * np.arange(dim_t)[:, None]
    frames = xp[idx] * win
    return np.fft.rfft(frames, axis=1).T


def istft(X):  # [n_bins, dim_t] -> [chunk]
    frames = np.fft.irfft(X.T, n=n_fft, axis=1) * win
    L = n_fft + hop * (dim_t - 1)
    out = np.zeros(L); env = np.zeros(L)
    for t in range(dim_t):
        out[t * hop:t * hop + n_fft] += frames[t]
        env[t * hop:t * hop + n_fft] += win ** 2
    out = out / np.maximum(env, 1e-8)
    return out[n_fft // 2:n_fft // 2 + chunk]


def to_spec(w):  # w: [2, chunk] -> [4, dim_f, dim_t]
    s = []
    for ch in range(2):
        X = stft(w[ch])
        s += [X.real, X.imag]
    return np.stack(s)[:, :dim_f].astype(np.float32)


def from_spec(s):  # [4, dim_f, dim_t] -> [2, chunk]
    pad = np.zeros((4, n_bins - dim_f, dim_t), dtype=np.float32)
    s = np.concatenate([s, pad], axis=1)
    return np.stack([istft(s[0] + 1j * s[1]), istft(s[2] + 1j * s[3])])


mix, sr = sf.read(src, always_2d=True)
assert sr == 44100, sr
mix = mix.T.astype(np.float64)
if mix.shape[0] == 1:
    mix = np.repeat(mix, 2, 0)
n = mix.shape[1]
pad = gen - n % gen
mp = np.concatenate([np.zeros((2, trim)), mix, np.zeros((2, pad)), np.zeros((2, trim))], 1)
sess = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
outs = []
i = 0
while i < n + pad:
    w = mp[:, i:i + chunk]
    spec = to_spec(w)[None]
    # "denoise" trick used by UVR: average f(x) and -f(-x)
    pred = (sess.run(None, {"input": spec})[0] * 0.5 - sess.run(None, {"input": -spec})[0] * 0.5)[0]
    wav = from_spec(pred)
    outs.append(wav[:, trim:-trim])
    i += gen
    print(f"chunk {len(outs)} done", flush=True)
primary = np.concatenate(outs, 1)[:, :n] * comp
rest = mix - primary
sf.write(out_p, primary.T, sr, subtype="FLOAT")
sf.write(out_r, rest.T, sr, subtype="FLOAT")
print("ok", primary.shape)
