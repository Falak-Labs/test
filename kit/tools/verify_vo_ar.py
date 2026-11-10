"""Transcribe each Arabic voiceover line back with multilingual Whisper (sherpa-onnx) for a sanity check.

usage: python3 -I tools/verify_vo_ar.py <whisper_small_dir> <vo.wav> <vo.json>
Whisper writes dialect in its own (often more formal) spelling, so the error rate is only a guide:
read the transcripts and look for dropped or garbled words, not spelling differences.
"""
import difflib
import json
import re
import sys

import numpy as np
import sherpa_onnx
import soundfile as sf

wdir, wav, js = sys.argv[1:4]
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{wdir}/small-encoder.int8.onnx", decoder=f"{wdir}/small-decoder.int8.onnx",
    tokens=f"{wdir}/small-tokens.txt", language="ar", task="transcribe", num_threads=2)
audio, sr = sf.read(wav, dtype="float32")
if audio.ndim > 1:
    audio = audio.mean(axis=1)
if sr != 16000:
    from scipy.signal import resample_poly
    audio = resample_poly(audio, 16000, sr).astype(np.float32)
    sr = 16000
meta = json.load(open(js, encoding="utf-8"))
TASH = re.compile(r"[ؐ-ًؚ-ٰٟـ]")


def norm(s):
    s = TASH.sub("", s)
    s = re.sub("[إأآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    return re.findall(r"[ء-ي0-9]+", s)


tot_err = tot = 0
for ln in meta["lines"]:
    a = audio[int(max(ln["start"] - 0.05, 0) * sr): int((ln["end"] + 0.05) * sr)]
    st = rec.create_stream()
    st.accept_waveform(sr, a)
    rec.decode_stream(st)
    hyp = st.result.text.strip()
    r, h = norm(ln["text"]), norm(hyp)
    sm = difflib.SequenceMatcher(a=r, b=h)
    err = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    tot_err += err
    tot += len(r)
    print(f"L{ln['line']:>2} {err:>2} diff | {hyp}")
print(f"rough word difference: {tot_err}/{tot} = {100 * tot_err / max(tot, 1):.0f}% (dialect spelling inflates this)")
