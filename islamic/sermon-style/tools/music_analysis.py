"""Describe the music bed: level vs voice, ducking, tempo/pulse, key/chords, spectrum, stereo, reverb tail."""
import sys, json
import numpy as np
import soundfile as sf
import librosa
import pyloudnorm as pyln
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

music_p, voice_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
END = 64.4
m, sr = sf.read(music_p, always_2d=True); m = m[:int(END * sr)]
v, _ = sf.read(voice_p, always_2d=True); v = v[:int(END * sr)]
mm, vm = m.mean(1), v.mean(1)
meter = pyln.Meter(sr)
res = {"music_lufs": round(meter.integrated_loudness(m), 1), "voice_lufs": round(meter.integrated_loudness(v), 1)}
res["music_below_voice_lu"] = round(res["voice_lufs"] - res["music_lufs"], 1)

# ducking: music level while voice active vs voice idle
hop = int(0.05 * sr)
def rms_db(x):
    r = librosa.feature.rms(y=x, frame_length=hop * 2, hop_length=hop)[0]
    return 20 * np.log10(r + 1e-9)
md, vd = rms_db(mm), rms_db(vm)
n = min(len(md), len(vd)); md, vd = md[:n], vd[:n]
active = vd > np.percentile(vd, 60)
idle = vd < np.percentile(vd, 25)
res["music_db_when_voice_active"] = round(float(np.median(md[active])), 1)
res["music_db_when_voice_idle"] = round(float(np.median(md[idle])), 1)
res["ducking_db_estimate"] = round(res["music_db_when_voice_idle"] - res["music_db_when_voice_active"], 1)

# tempo / pulse
onset = librosa.onset.onset_strength(y=mm, sr=sr)
tempo = librosa.feature.tempo(onset_envelope=onset, sr=sr)
res["tempo_bpm_estimate"] = round(float(tempo[0]), 1)
res["onset_strength_mean"] = round(float(onset.mean()), 3)
H, P = librosa.decompose.hpss(librosa.stft(mm, n_fft=4096, hop_length=1024))
eh, ep = float((np.abs(H) ** 2).sum()), float((np.abs(P) ** 2).sum())
res["harmonic_share_pct"] = round(100 * eh / (eh + ep), 1)

# key / chords: chroma on harmonic part
chroma = librosa.feature.chroma_cqt(y=librosa.istft(H, hop_length=1024), sr=sr, hop_length=4096)
names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
prof = chroma.mean(1)
maj = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
minr = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
scores = []
for k in range(12):
    scores.append((np.corrcoef(prof, np.roll(maj, k))[0, 1], names[k] + " major"))
    scores.append((np.corrcoef(prof, np.roll(minr, k))[0, 1], names[k] + " minor"))
scores.sort(reverse=True)
res["key_candidates"] = [(s, round(float(c), 3)) for c, s in scores[:3]]
res["chroma_profile"] = {names[i]: round(float(prof[i]), 3) for i in range(12)}
# chord-ish segmentation: dominant pitch classes per 2 s
seg = []
fps = sr / 4096
for t0 in np.arange(0, END, 4.0):
    c = chroma[:, int(t0 * fps):int((t0 + 4) * fps)].mean(1)
    top = np.argsort(c)[::-1][:3]
    seg.append(f"{t0:4.0f}s " + "-".join(names[i] for i in top))
res["top_pitch_classes_per_4s"] = seg

# spectrum: where the energy sits
S = np.abs(librosa.stft(mm, n_fft=8192, hop_length=2048)) ** 2
f = librosa.fft_frequencies(sr=sr, n_fft=8192)
bands = [(20, 80), (80, 250), (250, 1000), (1000, 4000), (4000, 12000), (12000, 20000)]
tot = S.sum()
res["energy_by_band_pct"] = {f"{a}-{b}Hz": round(100 * float(S[(f >= a) & (f < b)].sum() / tot), 1) for a, b in bands}
res["spectral_centroid_hz"] = round(float(np.median(librosa.feature.spectral_centroid(y=mm, sr=sr)[0])), 0)
# stereo
l, r = m[:, 0], m[:, 1]
res["music_stereo_correlation"] = round(float(np.corrcoef(l, r)[0, 1]), 3)
res["music_side_vs_mid_db"] = round(20 * np.log10(np.std(l - r) / np.std(l + r)), 1)
# level drift across the piece (does it build?)
res["music_db_by_10s"] = [round(float(np.median(md[int(i * 20):int((i + 10) * 20)])), 1) for i in range(0, int(END) - 9, 10)]
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))

fig, ax = plt.subplots(2, 1, figsize=(18, 8))
Sm = librosa.amplitude_to_db(np.abs(librosa.stft(mm, n_fft=8192, hop_length=1024)), ref=np.max)
librosa.display.specshow(Sm, sr=sr, hop_length=1024, x_axis="time", y_axis="log", ax=ax[0], cmap="magma", vmin=-80, vmax=0)
ax[0].set_title("Music stem spectrogram (log freq)")
librosa.display.specshow(chroma, sr=sr, hop_length=4096, x_axis="time", y_axis="chroma", ax=ax[1])
ax[1].set_title("Chroma")
fig.tight_layout(); fig.savefig(out.replace(".json", ".png"), dpi=60)
