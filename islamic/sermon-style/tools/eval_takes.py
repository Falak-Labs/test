"""Compare voice takes with the reference narrator: pitch, range, pace, pauses, timbre, and a Whisper read-back check.
usage: eval_takes.py takes_dir lines.txt whisper_dir out.json
"""
import sys, json, glob, os, re, unicodedata
import numpy as np
import soundfile as sf
import librosa
import parselmouth
import sherpa_onnx

tdir, lines_p, wdir, out = sys.argv[1:5]
TAG = re.compile(r"\[[^\]]*\]")
script = " ".join(TAG.sub("", l).strip() for l in open(lines_p, encoding="utf-8") if l.strip())


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[إأآا]", "ا", s); s = s.replace("ة", "ه").replace("ى", "ي")
    s = re.sub(r"[^ء-ي ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def cer(ref, hyp):
    r, h = norm(ref).replace(" ", ""), norm(hyp).replace(" ", "")
    d = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(1, len(r))


rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{wdir}/turbo-encoder.int8.onnx", decoder=f"{wdir}/turbo-decoder.int8.onnx",
    tokens=f"{wdir}/turbo-tokens.txt", language="ar", task="transcribe", num_threads=2)

res = {}
for wav in sorted(glob.glob(os.path.join(tdir, "*.wav"))):
    vid = os.path.basename(wav)[:-4]
    meta = json.load(open(wav[:-4] + ".json", encoding="utf-8"))
    y, sr = sf.read(wav)
    snd = parselmouth.Sound(y, sampling_frequency=sr)
    p = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=400)
    f0 = p.selected_array["frequency"]; f0 = f0[f0 > 0]
    st = 12 * np.log2(f0 / np.median(f0))
    # pauses from energy
    hop = int(0.01 * sr)
    e = librosa.feature.rms(y=y, frame_length=hop * 3, hop_length=hop)[0]
    db = 20 * np.log10(e + 1e-9)
    q = db < (np.percentile(db, 95) - 30)
    gaps, s0 = [], None
    for i, v in enumerate(q):
        if v and s0 is None: s0 = i
        if not v and s0 is not None:
            if (i - s0) >= 15: gaps.append((i - s0) / 100)
            s0 = None
    words = sum(len(L["words"]) for L in meta["lines"])
    speech = len(y) / sr - sum(gaps)
    # whisper read-back in <=28 s chunks cut at line boundaries
    texts, chunk0 = [], 0.0
    bounds = [L["end"] for L in meta["lines"] if L["end"]]
    cuts, last = [], 0.0
    for b in bounds:
        if b - last > 26:
            cuts.append(last_b); last = last_b
        last_b = b
    cuts.append(len(y) / sr)
    y16 = librosa.resample(y, orig_sr=sr, target_sr=16000).astype(np.float32)
    a = 0.0
    for c in cuts:
        s = rec.create_stream(); s.accept_waveform(16000, y16[int(a * 16000):int((c + 0.15) * 16000)])
        rec.decode_stream(s); texts.append(s.result.text.strip()); a = c
    hyp = " ".join(texts)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    harm = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=75).values
    res[vid] = {
        "duration_s": round(len(y) / sr, 2),
        "f0_median_hz": round(float(np.median(f0)), 1),
        "f0_p5_p95_hz": [round(float(np.percentile(f0, 5)), 1), round(float(np.percentile(f0, 95)), 1)],
        "range_semitones_p5_p95": round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1),
        "pitch_sd_semitones": round(float(np.std(st)), 2),
        "words_per_sec_speaking": round(words / speech, 2),
        "words_per_sec_overall": round(words / (len(y) / sr), 2),
        "pauses_n": len(gaps), "pause_median_s": round(float(np.median(gaps)), 2) if gaps else None,
        "pause_p90_s": round(float(np.percentile(gaps, 90)), 2) if gaps else None,
        "spectral_centroid_hz": round(float(np.median(cent[db[:len(cent)] > np.percentile(db, 40)])), 0),
        "hnr_db": round(float(np.mean(harm[harm > -200])), 1),
        "readback_cer": round(cer(script, hyp), 3),
        "readback": hyp,
        "has_latin_in_readback": bool(re.search(r"[A-Za-z]{3,}", hyp)),
    }
    print(vid, {k: v for k, v in res[vid].items() if k != "readback"}, flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
