"""Check an English voice line by line with Whisper small (the local check of NIGHT_NOTES Nov 15).
    python3 -I tools/check_en_voice.py series/voice/<kit>            (a narration: <kit>.json + <kit>.wav)
    python3 -I tools/check_en_voice.py series/voice/<kit> mix.wav    (the same line times on a finished mix; the video
                                                                      starts 0.5 s before the voice: pass lead=0.5)
Each line's span is padded 0.5 s before and 2 s after, the words are compared with difflib; number formats show up
as differences ("1400" for "fourteen hundred"), so read the lines it prints rather than the percentage alone.
"""
import difflib
import json
import re
import sys

import numpy as np
import sherpa_onnx
import soundfile as sf
from scipy.signal import resample_poly

wd = "/home/claude/tts/asr/sherpa-onnx-whisper-small"
vo = sys.argv[1]
wav = vo + ".wav"
lead = 0.0
for a in sys.argv[2:]:
    if a.startswith("lead="):
        lead = float(a[5:])
    else:
        wav = a
d = json.load(open(vo + ".json"))
y, sr = sf.read(wav, dtype="float32")
if y.ndim > 1:
    y = y.mean(axis=1)
R = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{wd}/small-encoder.int8.onnx", decoder=f"{wd}/small-decoder.int8.onnx",
                                               tokens=f"{wd}/small-tokens.txt", language="en", task="transcribe", num_threads=2)


def words(s):
    return re.findall(r"[a-z0-9']+", s.lower().replace("-", " "))


tot = bad = 0
for i, ln in enumerate(d["lines"]):
    a = max(0.0, ln["start"] + lead - 0.5)
    b = ln["end"] + lead + (0.3 if i + 1 < len(d["lines"]) else 2.0)
    seg = y[int(a * sr):int(b * sr)]
    seg16 = np.concatenate([resample_poly(seg, 16000, sr), np.zeros(32000)]).astype(np.float32)
    st = R.create_stream()
    st.accept_waveform(16000, seg16)
    R.decode_stream(st)
    h = st.result.text.strip()
    A, B = words(ln["text"]), words(h)
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    diffs = [(A[i1:i2], B[j1:j2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    n = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    tot += len(A)
    bad += n
    flag = "  " if not diffs else "!!"
    print(f"{flag} L{i + 1:2d} {ln['end'] - ln['start']:5.1f}s | {h}")
    for x, z in diffs:
        print(f"        {' '.join(x) or '-'}  ->  {' '.join(z) or '-'}")
print(f"word differences: {bad}/{tot}")
