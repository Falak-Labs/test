"""Measure a finished Saudi voice line by line with Whisper small (letters, silence-padded).
    python3 -I tools/check_ar_voice.py series/voice/<kit>_ar_sa
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
d = json.load(open(vo + ".json"))
y, sr = sf.read(vo + ".wav", dtype="float32")
R = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{wd}/small-encoder.int8.onnx", decoder=f"{wd}/small-decoder.int8.onnx",
                                               tokens=f"{wd}/small-tokens.txt", language="ar", task="transcribe", num_threads=2)
T = re.compile("[ً-ْـ]")


def norm(s):
    s = re.sub("[إأآٱ]", "ا", T.sub("", s)).replace("ى", "ي").replace("ة", "ه")
    return "".join(re.findall(r"[ء-ي0-9]+", s))


bad = []
for ln in d["lines"]:
    seg = y[int(ln["start"] * sr):int(ln["end"] * sr)]
    seg16 = np.concatenate([resample_poly(seg, 16000, sr), np.zeros(48000)]).astype(np.float32)
    st = R.create_stream()
    st.accept_waveform(16000, seg16)
    R.decode_stream(st)
    h = st.result.text.strip()
    e = 1 - difflib.SequenceMatcher(a=norm(ln["text"]), b=norm(h), autojunk=False).ratio()
    if e > 0.3:
        bad.append(ln["line"])
    print(f"{ln['line']:>2} {e:4.0%} {ln['end'] - ln['start']:5.1f}s | {h}")
print("weak lines:", bad or "none")
