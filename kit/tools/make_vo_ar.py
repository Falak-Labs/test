"""Palestinian Arabic voiceover with Sofelia TTS 82M (Apache-2.0, Kokoro-82M fine-tune, voice Eliaa).

usage:
  python3 -I tools/make_vo_ar.py <lines_ar.txt> <out_prefix> [--model-dir ~/tts/sofelia/sofelia-tts-82m]
                                 [--speed 1.0] [--tempo 1.0] [--gap 0.35] [--verify]

Same outputs as make_vo.py: <out>.wav / .json (line timings) / .mp3 and <out>_raw.*.
Write the lines file WITH vowel marks (tashkeel) in colloquial spelling: espeak drops the vowels of
unmarked words ("ربطت" -> "rbtt") and Eliaa then mumbles. The timing JSON (and so the captions) gets the
same text without the marks. Write numbers as words. A word that still sounds wrong can also go in
tools/ar_lexicon.json (surface -> diacritized).
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import types

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("lines")
ap.add_argument("out")
ap.add_argument("--model-dir", default=os.path.expanduser("~/tts/sofelia/sofelia-tts-82m"))
ap.add_argument("--voice", default="eliaa")
ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--tempo", type=float, default=1.0)
ap.add_argument("--gap", type=float, default=0.35)
ap.add_argument("--tts-home", default=os.environ.get("TTS_HOME", os.path.expanduser("~/tts")))
ap.add_argument("--verify", action="store_true")
a = ap.parse_args()

# espeak-ng comes from the espeakng_loader wheel (no system install needed)
import espeakng_loader  # noqa: E402
from phonemizer.backend.espeak.wrapper import EspeakWrapper  # noqa: E402
EspeakWrapper.set_library(espeakng_loader.get_library_path())
os.environ["ESPEAK_DATA_PATH"] = espeakng_loader.get_data_path()
if hasattr(EspeakWrapper, "set_data_path"):
    EspeakWrapper.set_data_path(espeakng_loader.get_data_path())

# kokoro's __init__ imports the English pipeline (spacy); load only kokoro.model
spec = importlib.util.find_spec("kokoro")
pkg = types.ModuleType("kokoro")
pkg.__path__ = [os.path.dirname(spec.origin)]
sys.modules["kokoro"] = pkg
import torch  # noqa: E402
from kokoro.model import KModel  # noqa: E402
from misaki import espeak  # noqa: E402

sys.path.insert(0, HERE)
from sofelia_frontend import text_to_phonemes  # noqa: E402  (vendored, reads tools/ar_lexicon.json)

MAX_PAUSE, KEEP_PAUSE, SR = 0.16, 0.11, 24000
TASHKEEL = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u0640]")  # captions show the text without vowel marks


def tighten(x, sr):
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


torch.set_num_threads(max(1, os.cpu_count() or 1))
def load_sofelia(model_dir):
    """kokoro 0.7.16 uses old-style weight_norm (weight_g / weight_v); the Sofelia checkpoint was saved with
    torch's newer parametrizations (original0 / original1) and a DataParallel 'module.' prefix. Remap and
    load strictly, so nothing is silently left at random init (that gives pure noise)."""
    path = os.path.join(model_dir, "kokoro_sofelia_82M.pth")
    m = KModel(config=os.path.join(model_dir, "config.json"), model=path)
    sd = torch.load(path, map_location="cpu", weights_only=True)
    for key, part in sd.items():
        fixed = {}
        for k, v in part.items():
            k = k[7:] if k.startswith("module.") else k
            k = k.replace(".parametrizations.weight.original0", ".weight_g")
            k = k.replace(".parametrizations.weight.original1", ".weight_v")
            fixed[k] = v
        getattr(m, key).load_state_dict(fixed, strict=True)
    return m.eval()


model = load_sofelia(a.model_dir)
pack = torch.load(os.path.join(a.model_dir, "voices", a.voice + ".pt"), map_location="cpu", weights_only=True)
g2p = espeak.EspeakG2P(language="ar")

lines = [l.strip() for l in open(a.lines, encoding="utf-8") if l.strip()]
PUNCT = set(",.;:!?\"()“”—…")
UNIT = 600 / SR  # Kokoro: one predicted duration unit = 600 samples at 24 kHz


def synth_chunk(text):
    """Audio plus word spans (seconds, chunk-relative) from the model's own phoneme durations."""
    ps = text_to_phonemes(text, g2p)[:510]
    if not ps:
        return np.zeros(0, np.float32), []
    with torch.no_grad():
        out = model(ps, pack[len(ps) - 1], a.speed, return_output=True)
    audio = np.asarray(out.audio.cpu().numpy().squeeze(), np.float32)
    dur = out.pred_dur.cpu().numpy().astype(float).reshape(-1)
    toks = [p for p in ps if p in model.vocab]
    spans, cur, u = [], None, dur[0]  # dur[0] is the start token
    for tk, d in zip(toks, dur[1:]):
        if tk == " ":
            if cur:
                spans.append(cur)
            cur = None
        elif tk not in PUNCT:
            cur = [u, u + d] if cur is None else [cur[0], u + d]
        u += d
    if cur:
        spans.append(cur)
    return audio, [(s0 * UNIT, s1 * UNIT) for s0, s1 in spans]


def edge_trim(x):
    """Trim silence at both ends (keeps 30 ms); returns audio and the seconds cut from the front."""
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x, 0.0
    db = 20 * np.log10(np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12) + 1e-12)
    voiced = np.where(db > max(db.max() - 42, -60))[0]
    if len(voiced) == 0:
        return x, 0.0
    i0, i1 = max(voiced[0] - 3, 0), min(voiced[-1] + 4, n)
    return x[i0 * win: i1 * win], i0 * win / SR


pieces, timing, t = [], [], 0.0
for i, line in enumerate(lines, 1):
    # one line may hold several sentences: synthesize each, joined by a short breath
    chunks = [c.strip() for c in re.split(r"(?<=[.!؟?:])\s+", line) if c.strip()] or [line]
    au_parts, spans, off = [], [], 0.0
    for ch in chunks:
        au, sp = synth_chunk(ch)
        spans += [(s0 + off, s1 + off) for s0, s1 in sp]
        au_parts += [au, np.zeros(int(0.12 * SR), np.float32)]
        off += len(au) / SR + 0.12
    au, cut = edge_trim(np.concatenate(au_parts[:-1]))
    d = len(au) / SR
    shown = TASHKEEL.sub("", line)
    words = shown.split()
    entry = {"line": i, "start": round(t, 3), "end": round(t + d, 3), "text": shown}
    if len(words) == len(spans):  # exact word times for the captions
        entry["words"] = [{"w": w, "start": round(t + max(0.0, s0 - cut), 3), "end": round(t + max(0.0, s1 - cut), 3)}
                          for w, (s0, s1) in zip(words, spans)]
    else:
        print(f"  L{i}: {len(words)} words vs {len(spans)} spoken words, captions will estimate", flush=True)
    timing.append(entry)
    pieces.append(au)
    t += d
    if i < len(lines):
        pieces.append(np.zeros(int(a.gap * SR), np.float32))
        t += a.gap
    print(f"  L{i:>2} {d:5.2f}s  {shown[:40]}", flush=True)

raw = a.out + "_raw"
full = np.concatenate(pieces)
sf.write(raw + ".wav", full, SR)
words = sum(len(re.findall(r"[؀-ۿ]+", l)) for l in lines)
json.dump({"voice": "Sofelia " + a.voice, "duration": round(len(full) / SR, 2), "words": words, "lines": timing},
          open(raw + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if abs(a.tempo - 1.0) > 1e-6:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", raw + ".wav",
                    "-af", f"atempo={a.tempo}", a.out + ".wav"], check=True)
    for ln in timing:
        ln["start"], ln["end"] = round(ln["start"] / a.tempo, 3), round(ln["end"] / a.tempo, 3)
        for w in ln.get("words", []):
            w["start"], w["end"] = round(w["start"] / a.tempo, 3), round(w["end"] / a.tempo, 3)
else:
    sf.write(a.out + ".wav", full, SR)
dur = sf.info(a.out + ".wav").duration
json.dump({"voice": "Sofelia " + a.voice, "speed": a.speed, "tempo": a.tempo, "gap": a.gap, "duration": round(dur, 2),
           "words": words, "words_per_sec": round(words / dur, 2), "lines": timing},
          open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.out + ".wav",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k",
                a.out + ".mp3"], check=True)
print(f"Eliaa: {len(lines)} lines, {words} words, {dur:.2f}s of voice ({words / dur:.2f} words/s) -> {a.out}.wav")
if a.verify:
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "verify_vo_ar.py"),
                    os.path.join(a.tts_home, "asr", "sherpa-onnx-whisper-small"), a.out + ".wav", a.out + ".json"])
