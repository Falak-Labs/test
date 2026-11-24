"""Split a clean voice stem into phrases at pauses, transcribe each with Whisper (sherpa-onnx),
and measure prosody per phrase (pitch, loudness, rate).
usage: voice_phrases.py vocals.wav whisper_dir out.json [end_s]
"""
import sys, json
import numpy as np
import soundfile as sf
import librosa
import parselmouth
import sherpa_onnx

src, wdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
end_s = float(sys.argv[4]) if len(sys.argv) > 4 else None
y, sr = sf.read(src, always_2d=True)
y = y.mean(1)
if end_s:
    y = y[:int(end_s * sr)]

# --- phrase segmentation on energy ---
fr = int(0.01 * sr)
rms = librosa.feature.rms(y=y, frame_length=fr * 3, hop_length=fr)[0]
db = 20 * np.log10(rms + 1e-9)
thr = np.percentile(db, 95) - float(sys.argv[5] if len(sys.argv) > 5 else 24)
voiced = db > thr
# close tiny gaps (<180 ms) and remove tiny blips (<120 ms)
def runs(mask):
    r, s = [], None
    for i, v in enumerate(mask):
        if v and s is None: s = i
        if not v and s is not None: r.append([s, i]); s = None
    if s is not None: r.append([s, len(mask)])
    return r
segs = runs(voiced)
merged = []
for s, e in segs:
    if merged and s - merged[-1][1] < 15:
        merged[-1][1] = e
    else:
        merged.append([s, e])
merged = [[s, e] for s, e in merged if e - s >= 12]

rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{wdir}/turbo-encoder.int8.onnx", decoder=f"{wdir}/turbo-decoder.int8.onnx",
    tokens=f"{wdir}/turbo-tokens.txt", language="ar", task="transcribe", num_threads=2, enable_token_timestamps=True)

y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
snd = parselmouth.Sound(y, sampling_frequency=sr)
pitch = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=400)
f0 = pitch.selected_array["frequency"]; f0t = pitch.xs()
inten = snd.to_intensity(minimum_pitch=75)

phrases = []
for s, e in merged:
    t0, t1 = s * 0.01, e * 0.01
    a, b = max(0, int((t0 - 0.05) * 16000)), int((t1 + 0.05) * 16000)
    st = rec.create_stream()
    if st.has_option("max_tokens_per_second"):
        st.set_option("max_tokens_per_second", "20")
    st.accept_waveform(16000, y16[a:b].astype(np.float32))
    rec.decode_stream(st)
    text = st.result.text.strip()
    m = (f0t >= t0) & (f0t <= t1) & (f0 > 0)
    fv = f0[m]
    phrases.append({
        "t0": round(t0, 2), "t1": round(t1, 2), "dur": round(t1 - t0, 2),
        "text": text, "n_words": len(text.split()),
        "f0_median": round(float(np.median(fv)), 1) if len(fv) else None,
        "f0_p10": round(float(np.percentile(fv, 10)), 1) if len(fv) else None,
        "f0_p90": round(float(np.percentile(fv, 90)), 1) if len(fv) else None,
        "f0_start": round(float(np.median(fv[:15])), 1) if len(fv) > 15 else None,
        "f0_end": round(float(np.median(fv[-15:])), 1) if len(fv) > 15 else None,
        "intensity_db": round(float(np.mean([inten.get_value(t) or 0 for t in np.arange(t0, t1, 0.02)])), 1),
    })
    print(phrases[-1], flush=True)

allf = f0[f0 > 0]
semis = 12 * np.log2(allf / np.median(allf))
gaps = [round(phrases[i + 1]["t0"] - phrases[i]["t1"], 2) for i in range(len(phrases) - 1)]
speech_time = sum(p["dur"] for p in phrases)
words = sum(p["n_words"] for p in phrases)
summary = {
    "f0_median_hz": round(float(np.median(allf)), 1),
    "f0_p5_p95_hz": [round(float(np.percentile(allf, 5)), 1), round(float(np.percentile(allf, 95)), 1)],
    "pitch_range_semitones_p5_p95": round(float(np.percentile(semis, 95) - np.percentile(semis, 5)), 1),
    "pitch_sd_semitones": round(float(np.std(semis)), 2),
    "n_phrases": len(phrases),
    "phrase_dur_median_s": round(float(np.median([p["dur"] for p in phrases])), 2),
    "pause_median_s": round(float(np.median(gaps)), 2) if gaps else None,
    "pause_p90_s": round(float(np.percentile(gaps, 90)), 2) if gaps else None,
    "pauses": gaps,
    "speech_time_s": round(speech_time, 2),
    "total_time_s": round(phrases[-1]["t1"] - phrases[0]["t0"], 2),
    "words": words,
    "words_per_sec_speaking": round(words / speech_time, 2),
    "words_per_sec_overall": round(words / (phrases[-1]["t1"] - phrases[0]["t0"]), 2),
}
# voice quality on all voiced audio
pp = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", 60, 400)
summary["jitter_local"] = round(parselmouth.praat.call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3), 4)
summary["shimmer_local"] = round(parselmouth.praat.call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 4)
harm = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=75)
hv = harm.values[harm.values > -200]
summary["hnr_db_mean"] = round(float(np.mean(hv)), 1)
cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
summary["spectral_centroid_hz_median"] = round(float(np.median(cent[db[:len(cent)] > thr] if len(cent) <= len(db) else cent)), 0)
form = snd.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5000)
f1 = [form.get_value_at_time(1, t) for t in f0t[f0 > 0][::5]]
f2 = [form.get_value_at_time(2, t) for t in f0t[f0 > 0][::5]]
summary["F1_F2_median_hz"] = [round(float(np.nanmedian(f1)), 0), round(float(np.nanmedian(f2)), 0)]
json.dump({"summary": summary, "phrases": phrases}, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
