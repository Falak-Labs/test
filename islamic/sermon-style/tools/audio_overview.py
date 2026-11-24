"""Overview of the reference audio: loudness, quiet gaps, spectrogram images."""
import sys, json
import numpy as np
import soundfile as sf
import librosa, librosa.display
import pyloudnorm as pyln
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src = sys.argv[1]
out = sys.argv[2]
y, sr = sf.read(src)
mono = y.mean(axis=1) if y.ndim > 1 else y
meter = pyln.Meter(sr)
res = {
    "duration_s": round(len(mono) / sr, 2),
    "integrated_lufs": round(meter.integrated_loudness(y), 2),
    "true_peak_dbfs_approx": round(20 * np.log10(np.max(np.abs(y)) + 1e-12), 2),
}
if y.ndim > 1:
    l, r = y[:, 0], y[:, 1]
    res["stereo_correlation"] = round(float(np.corrcoef(l, r)[0, 1]), 3)
    res["side_to_mid_db"] = round(20 * np.log10((np.std(l - r) + 1e-9) / (np.std(l + r) + 1e-9)), 1)

# short-term loudness every 100 ms (400 ms window)
hop = int(0.1 * sr); win = int(0.4 * sr)
st = []
for i in range(0, len(mono) - win, hop):
    seg = y[i:i + win]
    try:
        st.append(meter.integrated_loudness(seg) if len(seg) > 0 else -70)
    except Exception:
        st.append(-70)
st = np.array([s if np.isfinite(s) else -70 for s in st])
res["short_term_lufs_p10_p50_p90"] = [round(float(np.percentile(st, p)), 1) for p in (10, 50, 90)]

# RMS envelope in 20 ms frames, find quiet gaps (voice pauses)
frame = int(0.02 * sr)
rms = librosa.feature.rms(y=mono, frame_length=frame * 2, hop_length=frame)[0]
db = 20 * np.log10(rms + 1e-9)
thr = np.percentile(db, 90) - 25
quiet = db < thr
gaps = []
start = None
for i, q in enumerate(quiet):
    t = i * frame / sr
    if q and start is None:
        start = t
    if not q and start is not None:
        if t - start >= 0.25:
            gaps.append((round(start, 2), round(t, 2)))
        start = None
res["rms_db_p90"] = round(float(np.percentile(db, 90)), 1)
res["quiet_threshold_db"] = round(float(thr), 1)
res["quiet_gaps_over_250ms"] = gaps
res["n_gaps"] = len(gaps)
res["floor_db_in_gaps_median"] = round(float(np.median(db[quiet])), 1) if quiet.any() else None
json.dump(res, open(out + "/overview.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))

# Spectrogram images, 3 panels of ~23 s
S = librosa.amplitude_to_db(np.abs(librosa.stft(mono, n_fft=4096, hop_length=512)), ref=np.max)
total = len(mono) / sr
for k in range(3):
    t0, t1 = k * total / 3, (k + 1) * total / 3
    fig, ax = plt.subplots(2, 1, figsize=(18, 9), gridspec_kw={"height_ratios": [3, 1]})
    c0, c1 = int(t0 * sr / 512), int(t1 * sr / 512)
    librosa.display.specshow(S[:, c0:c1], sr=sr, hop_length=512, x_axis="time", y_axis="log", ax=ax[0], cmap="magma", vmin=-90, vmax=0)
    ax[0].set_title(f"Spectrogram {t0:.1f}-{t1:.1f}s (x axis relative)")
    tt = np.arange(len(db)) * frame / sr
    m = (tt >= t0) & (tt < t1)
    ax[1].plot(tt[m], db[m], lw=0.8)
    ax[1].axhline(thr, color="r", lw=0.6)
    ax[1].set_xlim(t0, t1)
    ax[1].set_ylabel("RMS dB")
    fig.tight_layout()
    fig.savefig(f"{out}/spec_{k}.png", dpi=70)
    plt.close(fig)
