"""Transcribe each voiceover line back with Whisper (sherpa-onnx) and compare to the script.

Usage: python3 -I verify_vo.py <whisper_dir> <vo.wav> <vo.json>
Prints per-line word error rate and any mismatched words.
"""
import sys, json, re, difflib
import numpy as np
import soundfile as sf
import sherpa_onnx

wdir, wav, js = sys.argv[1:4]
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{wdir}/base.en-encoder.int8.onnx", decoder=f"{wdir}/base.en-decoder.int8.onnx",
    tokens=f"{wdir}/base.en-tokens.txt", language="en", task="transcribe", num_threads=4)
audio, sr = sf.read(wav, dtype="float32")
if audio.ndim > 1:
    audio = audio.mean(axis=1)
meta = json.load(open(js))

NUM = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "ten": "10", "eleven": "11",
       "twenty": "20", "first": "1st"}
def norm(s):
    s = s.lower().replace("’", "'")
    ws = re.findall(r"[a-z0-9']+", s)
    return [NUM.get(w, w) for w in ws]

tot_err = tot = 0
for ln in meta["lines"]:
    a = audio[int(max(ln["start"] - 0.05, 0) * sr): int((ln["end"] + 0.05) * sr)]
    st = rec.create_stream(); st.accept_waveform(sr, a); rec.decode_stream(st)
    hyp = st.result.text.strip()
    r, h = norm(ln["text"]), norm(hyp)
    sm = difflib.SequenceMatcher(a=r, b=h)
    err = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    tot_err += err; tot += len(r)
    flag = "OK " if err == 0 else f"{err} diff"
    print(f"L{ln['line']:>2} {flag:7} | {hyp}")
print(f"overall word error rate: {tot_err}/{tot} = {100*tot_err/tot:.1f}%")
