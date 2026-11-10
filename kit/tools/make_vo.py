"""Voiceover for one episode with Phonon (Apache 2.0, runs on CPU): the series' house voice.

usage:
  python3 -I tools/make_vo.py <lines.txt> <out_prefix> [--voice Easton] [--tempo 0.96] [--gap 0.35]
                              [--tts-home ~/tts] [--verify]

lines.txt   one voiceover line per row, in beat order (hook, break1, fix1 ... closer).
Writes      <out_prefix>.wav / .json (line timings the animation keys to) / .mp3 (-14 LUFS preview)
            and <out_prefix>_raw.* (before the tempo change).
Fixed rules (learned on the Elevator pilot):
  * Phonon reads "..." / "…" as "dot" and can drop the word before an em dash, so both become commas.
  * Easton runs fast: tempo 0.96 + 0.35 s between lines lands a ~215-word script at ~62-63 s of voice,
    which the timeline (lead 0.5 + pause 0.6 + tail 1.8) turns into a 65-66 s video.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("lines")
ap.add_argument("out")
ap.add_argument("--voice", default="Easton")
ap.add_argument("--tempo", type=float, default=0.96)
ap.add_argument("--gap", type=float, default=0.35)
ap.add_argument("--tts-home", default=os.environ.get("TTS_HOME", os.path.expanduser("~/tts")))
ap.add_argument("--verify", action="store_true", help="transcribe back with Whisper and print word errors")
a = ap.parse_args()

MAX_PAUSE, KEEP_PAUSE = 0.16, 0.11


def clean(line):
    s = line.replace("…", ",").replace("...", ",")
    s = re.sub(r"\s*—\s*", ", ", s)
    s = re.sub(r"\s*,\s*,+", ",", s)
    return re.sub(r"\s+", " ", s).strip()


def tighten(x, sr):
    """Trim the edges and shorten pauses inside a line to KEEP_PAUSE."""
    win = int(0.01 * sr)
    n = len(x) // win
    if n == 0:
        return x
    fr = x[: n * win].reshape(n, win)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1) + 1e-12) + 1e-12)
    voiced = db > max(db.max() - 42, -60)
    if not voiced.any():
        return x
    first, last = max(np.argmax(voiced) - 2, 0), min(n - 1 - np.argmax(voiced[::-1]) + 3, n - 1)
    out, i = [], first
    while i <= last:
        j = i
        while j <= last and voiced[j] == voiced[i]:
            j += 1
        if voiced[i]:
            out.append(fr[i:j].reshape(-1))
        else:
            gap = (j - i) * win / sr
            out.append(np.zeros(int((gap if gap <= MAX_PAUSE else KEEP_PAUSE) * sr), np.float32))
        i = j
    return np.concatenate(out)


import ptts  # noqa: E402

model = os.path.join(a.tts_home, "phonon", "phonon-31m-en")
voices = os.path.join(a.tts_home, "phonon", "phonon-voices")
tts = ptts.TTS(model, lang="en", quant="q8", voice_catalog=voices)
lines = [clean(l) for l in open(a.lines, encoding="utf-8") if l.strip()]
pieces, timing, t, sr = [], [], 0.0, 24000
for i, line in enumerate(lines, 1):
    au = tighten(np.asarray(tts.synth(line, voice=a.voice), np.float32), tts.sample_rate)
    sr = tts.sample_rate
    d = len(au) / sr
    timing.append({"line": i, "start": round(t, 3), "end": round(t + d, 3), "text": line})
    pieces.append(au)
    t += d
    if i < len(lines):
        pieces.append(np.zeros(int(a.gap * sr), np.float32))
        t += a.gap
raw = a.out + "_raw"
full = np.concatenate(pieces)
sf.write(raw + ".wav", full, sr)
words = sum(len(re.findall(r"[A-Za-z0-9'’-]+", l)) for l in lines)
json.dump({"voice": a.voice, "duration": round(len(full) / sr, 2), "words": words, "lines": timing},
          open(raw + ".json", "w"), indent=1)
# slow down a touch without changing pitch, and move the line timings with it
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", raw + ".wav",
                "-af", f"atempo={a.tempo}", a.out + ".wav"], check=True)
dur = sf.info(a.out + ".wav").duration
for ln in timing:
    ln["start"], ln["end"] = round(ln["start"] / a.tempo, 3), round(ln["end"] / a.tempo, 3)
json.dump({"voice": a.voice, "tempo": a.tempo, "gap": a.gap, "duration": round(dur, 2), "words": words,
           "words_per_sec": round(words / dur, 2), "lines": timing}, open(a.out + ".json", "w"), indent=1)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.out + ".wav",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k",
                a.out + ".mp3"], check=True)
print(f"{a.voice}: {len(lines)} lines, {words} words, {dur:.2f}s of voice ({words / dur:.2f} words/s) -> {a.out}.wav")
if a.verify:
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, "-I", os.path.join(here, "verify_vo.py"),
                    os.path.join(a.tts_home, "asr", "sherpa-onnx-whisper-base.en"), a.out + ".wav", a.out + ".json"])
