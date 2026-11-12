#!/usr/bin/env python3
"""Arabic voice test: the same Saudi lines read by several engines, scored two ways. Runs on GitHub's runner
(.github/workflows/voicetest.yml).

    python -I scripts/voicetest.py make [--only a,b] [--skip a,b]
    python -I scripts/voicetest.py score

Engines (VT_ENGINES, comma separated):
  namaa            the current narrator (NAMAA Saudi), cut from the episode's voice master
  ms_hamed         Microsoft ar-SA-HamedNeural through edge-tts (listening only: production would need the
  ms_fahed         official Azure key); ms_fahed = ar-KW-FahedNeural, a bit faster
  silma            SILMA TTS (open source, Apache-2.0 weights), voice cloned from the current narrator
  gemini_<voice>   Gemini TTS prebuilt voice, e.g. gemini_fenrir; runs only when GEMINI_API_KEY is set
  azure_<voice>    official Azure Speech, e.g. azure_hamed; runs only when AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are set
Scores: words = share of the script's words that Whisper small hears (higher is better; the same ear for every
engine), mos = UTMOS naturalness estimate 1-5 (trained on English speech: use it to rank, not as a grade).
Output: review/voicetest/<engine>.wav/.mp3, all.mp3 (every engine, a beep before each), scores.json, scores.md
Keys are read from the environment only and never printed.
"""
import argparse
import asyncio
import base64
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

SR = 24000
LANG = os.environ.get("VT_LANG") or "ar"                       # ar: the Saudi script, en: the English one
OUT = os.environ.get("VT_OUT") or "review/voicetest"
KIT = os.environ.get("VT_KIT") or "racecar"
PICK = [int(x) for x in (os.environ.get("VT_LINES") or "1,2,3,14").split(",") if x.strip()]
ENGINES = [e.strip() for e in (os.environ.get("VT_ENGINES") or
                               "namaa,ms_hamed,ms_fahed,silma,gemini_fenrir,gemini_charon,azure_hamed").split(",") if e.strip()]
ALL = open(f"kit/series/{KIT}_lines{'_ar_sa' if LANG == 'ar' else ''}.txt", encoding="utf-8").read().strip().splitlines()
RATE = os.environ.get("VT_RATE") or ""                         # e.g. +25% for every Microsoft voice
PAUSE_CAP = float(os.environ.get("VT_PAUSE_CAP") or 0)          # longest pause kept inside a line (s); 0 keeps them all
LINES = [ALL[i - 1].strip() for i in PICK]
GAP = 0.35
GEM_MODEL = os.environ.get("GEMINI_TTS_MODEL") or "gemini-3.1-flash-tts-preview"
GEM_STYLE = ("Read the following Arabic script aloud in a natural Saudi (Najdi) accent, like an energetic, friendly "
             "YouTube narrator telling a fun story, at a lively pace. Read only the script, exactly as written:\n\n")
GEM_VOICES = {"fenrir": "Fenrir", "charon": "Charon", "puck": "Puck", "orus": "Orus", "algieba": "Algieba",
              "iapetus": "Iapetus", "umbriel": "Umbriel", "sadachbia": "Sadachbia", "achird": "Achird"}
AZ_VOICES = {"hamed": ("ar-SA-HamedNeural", "+5%"), "fahed": ("ar-KW-FahedNeural", "+10%"),
             "laith": ("ar-SY-LaithNeural", "+5%"), "hamdan": ("ar-AE-HamdanNeural", "+5%"),
             "moaz": ("ar-QA-MoazNeural", "+5%"), "ali": ("ar-BH-AliNeural", "+5%"), "abdullah": ("ar-OM-AbdullahNeural", "+5%"),
             "andrew": ("en-US-AndrewMultilingualNeural", "+5%"), "brian": ("en-US-BrianMultilingualNeural", "+5%"),
             "guy": ("en-US-GuyNeural", "+5%"), "christopher": ("en-US-ChristopherNeural", "+5%")}


def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def trim(y, thr=0.01):
    idx = np.where(np.abs(y) > thr)[0]
    if len(idx) == 0:
        return y
    return y[max(0, idx[0] - int(0.03 * SR)): min(len(y), idx[-1] + int(0.08 * SR))]


def join(parts):
    gap = np.zeros(int(GAP * SR), np.float32)
    out = []
    for i, p in enumerate(parts):
        if i:
            out.append(gap)
        out.append(trim(p))
    return np.concatenate(out).astype(np.float32)


def master():
    d = json.load(open(f"kit/series/voice/{KIT}_ar_sa.json"))
    y, sr = sf.read(f"kit/series/voice/{KIT}_ar_sa.wav", dtype="float32")
    if y.ndim > 1:
        y = y.mean(1)
    if sr != SR:
        y = resample_poly(y, SR, sr).astype(np.float32)
    return d, y


def cut(d, y, n):
    L = next(l for l in d["lines"] if int(l["line"]) == n)
    return y[int(L["start"] * SR): int(L["end"] * SR)], L["text"]


def eng_namaa(_):
    d, y = master()
    return join([cut(d, y, n)[0] for n in PICK])


async def _edge(text, voice, rate, path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(path)


def cap_pauses(y, cap):
    """Shorten every quiet stretch longer than cap seconds to cap (Microsoft's voices pause long at commas)."""
    if cap <= 0:
        return y
    hop = int(0.01 * SR)
    e = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2) + 1e-12) for i in range(0, len(y) - hop, hop)])
    quiet = e < max(1e-4, 0.03 * np.percentile(e, 95))
    out, i, n = [], 0, len(quiet)
    while i < n:
        j = i
        while j < n and quiet[j] == quiet[i]:
            j += 1
        a, b = i * hop, j * hop
        if quiet[i] and (j - i) * 0.01 > cap:
            keep = int(cap * SR)
            out.append(y[a:a + keep // 2])
            out.append(y[b - keep // 2:b])
        else:
            out.append(y[a:b])
        i = j
    out.append(y[n * hop:])
    return np.concatenate(out).astype(np.float32)


def eng_ms(name):
    voice, rate = AZ_VOICES[name.split("_", 1)[1]]
    rate = RATE or rate
    parts = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(LINES):
            p = f"{td}/{i}.mp3"
            for k in range(5):
                try:
                    asyncio.run(_edge(t, voice, rate, p))
                    break
                except Exception as e:  # the service drops connections now and then
                    print("  edge-tts retry:", type(e).__name__, str(e)[:120])
                    time.sleep(4)
            else:
                return None
            parts.append(cap_pauses(load(p), PAUSE_CAP))
    return join(parts)


def eng_gemini(name):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("  skipped: no GEMINI_API_KEY secret")
        return None
    import requests
    voice = GEM_VOICES.get(name.split("_", 1)[1], name.split("_", 1)[1].capitalize())
    body = {"contents": [{"parts": [{"text": GEM_STYLE + "\n".join(LINES)}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEM_MODEL}:generateContent"
    for k in range(3):
        r = requests.post(url, headers={"x-goog-api-key": key, "Content-Type": "application/json"}, json=body, timeout=240)
        if r.status_code == 200:
            break
        print("  gemini", r.status_code, r.text[:300].replace(key, "***"))
        time.sleep(15)
    else:
        return None
    part = next(p for p in r.json()["candidates"][0]["content"]["parts"] if "inlineData" in p)["inlineData"]
    pcm = np.frombuffer(base64.b64decode(part["data"]), dtype="<i2").astype(np.float32) / 32768
    m = re.search(r"rate=(\d+)", part.get("mimeType", ""))
    sr = int(m.group(1)) if m else 24000
    if sr != SR:
        pcm = resample_poly(pcm, SR, sr).astype(np.float32)
    return trim(pcm)


def eng_azure(name):
    key, region = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
    if not (key and region):
        print("  skipped: no AZURE_SPEECH_KEY / AZURE_SPEECH_REGION secrets")
        return None
    import requests
    from xml.sax.saxutils import escape
    voice, rate = AZ_VOICES[name.split("_", 1)[1]]
    body = "<break time='350ms'/>".join(escape(t) for t in LINES)
    ssml = (f"<speak version='1.0' xml:lang='{voice[:5]}'><voice name='{voice}'><prosody rate='{rate}'>{body}"
            "</prosody></voice></speak>")
    r = requests.post(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", timeout=120,
                      headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
                               "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "build-it-voicetest"},
                      data=ssml.encode("utf-8"))
    if r.status_code != 200:
        print("  azure", r.status_code, r.text[:200])
        return None
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        f.write(r.content)
        f.flush()
        return trim(load(f.name))


def eng_silma(_):
    from silma_tts.api import SilmaTTS
    d, y = master()
    # reference: the two current lines Whisper hears best that are not in the test (the voice to keep)
    best = [8, 5] if KIT == "racecar" else [n for n in range(1, 15) if n not in PICK][:2]
    clips, texts = zip(*[cut(d, y, n) for n in best])
    ref = join(list(clips))
    m = SilmaTTS()
    parts = []
    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/ref.wav", ref, SR)
        for i, t in enumerate(LINES):
            p = f"{td}/{i}.wav"
            m.infer(ref_file=f"{td}/ref.wav", ref_text=" ".join(texts), gen_text=t, file_wave=p, seed=11, speed=1)
            parts.append(load(p))
    return join(parts)


def engine_fn(name):
    if name == "namaa":
        return eng_namaa
    if name.startswith("ms_"):
        return eng_ms
    if name.startswith("gemini_"):
        return eng_gemini
    if name.startswith("azure_"):
        return eng_azure
    if name == "silma":
        return eng_silma
    raise SystemExit(f"unknown engine {name}")


def make(only, skip):
    os.makedirs(OUT, exist_ok=True)
    for name in ENGINES:
        if (only and name not in only) or name in skip:
            continue
        print(f"[{name}]", flush=True)
        t0 = time.time()
        try:
            y = engine_fn(name)(name)
        except Exception as e:
            print(f"  failed: {type(e).__name__}: {str(e)[:300]}")
            y = None
        if y is None or len(y) < SR:
            continue
        sf.write(f"{OUT}/{name}.wav", y, SR)
        print(f"  {len(y) / SR:.1f} s of speech in {time.time() - t0:.0f} s")


T = re.compile("[ً-ْـ]")


NUM = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
       "nine": "9", "ten": "10", "twenty": "20", "thirty": "30", "ninety": "90", "hundred": "100", "thousand": "1000"}


def words(s):
    if LANG == "en":
        return [NUM.get(w, w) for w in re.findall(r"[a-z0-9']+", s.lower().replace(",", ""))]
    s = re.sub("[إأآٱ]", "ا", T.sub("", s)).replace("ى", "ي").replace("ة", "ه")
    return re.findall(r"[ء-ي0-9]+", s)


def pieces(y, sr=16000, most=8.0):
    """Cut points at pauses of 0.2 s or more, grouped into pieces of at most `most` seconds."""
    hop = int(0.02 * sr)
    e = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2) + 1e-12) for i in range(0, len(y) - hop, hop)])
    quiet = e < max(1e-4, 0.05 * np.percentile(e, 95))
    cuts, run = [], 0
    for i, q in enumerate(quiet):
        run = run + 1 if q else 0
        if run == 10:  # 0.2 s of quiet
            cuts.append((i - 5) * hop)
    out, start, last = [], 0, 0
    for c in cuts + [len(y)]:
        if c - start > most * sr and last > start:
            out.append((start, last))
            start = last
        last = c
    out.append((start, len(y)))
    return [(a, b) for a, b in out if b - a > 0.3 * sr]


def score():
    import sherpa_onnx
    import torch
    wd = os.environ.get("TTS_HOME", "/home/runner/tts") + "/asr/sherpa-onnx-whisper-small"
    R = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{wd}/small-encoder.int8.onnx", decoder=f"{wd}/small-decoder.int8.onnx",
        tokens=f"{wd}/small-tokens.txt", language=LANG, task="transcribe", num_threads=4)
    mos_model = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong", trust_repo=True)
    ref = words(" ".join(LINES))
    rows = []
    for name in ENGINES:
        p = f"{OUT}/{name}.wav"
        if not os.path.exists(p):
            continue
        y, _ = sf.read(p, dtype="float32")
        y16 = resample_poly(y, 16000, SR).astype(np.float32)
        heard = []
        for a, b in pieces(y16):  # short pieces cut at pauses: Whisper stops early on long ones
            chunk = np.concatenate([np.zeros(8000, np.float32), y16[a:b], np.zeros(8000, np.float32)])
            s = R.create_stream()
            s.accept_waveform(16000, chunk)
            R.decode_stream(s)
            heard.append(s.result.text)
        hw = words(" ".join(heard))
        sm = difflib.SequenceMatcher(None, ref, hw, autojunk=False)
        acc = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(ref))
        with torch.no_grad():
            mos = float(mos_model(torch.from_numpy(y16)[None], 16000).item())
        rows.append({"engine": name, "seconds": round(len(y) / SR, 1), "words": round(acc, 2), "mos": round(mos, 2),
                     "heard": " ".join(heard).strip()})
        print(f"{name:16s} words {acc:.0%}  mos {mos:.2f}  {len(y) / SR:.1f} s")
    # listening files, all at the same loudness
    letters = "ABCDEFGHIJ"
    concat = []
    beep = (0.25 * np.sin(2 * np.pi * 880 * np.arange(int(0.12 * SR)) / SR)).astype(np.float32)
    for i, r in enumerate(rows):
        r["letter"] = letters[i]
        src = f"{OUT}/{r['engine']}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "44100", "-b:a", "128k", f"{OUT}/{r['letter']}_{r['engine']}.mp3"], check=True)
        y = load(f"{OUT}/{r['letter']}_{r['engine']}.mp3")
        concat += [beep, np.zeros(int(0.5 * SR), np.float32), y, np.zeros(int(1.3 * SR), np.float32)]
    if concat:
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            sf.write(f.name, np.concatenate(concat), SR)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f.name, "-ar", "44100", "-b:a", "128k",
                            f"{OUT}/all.mp3"], check=True)
    json.dump({"kit": KIT, "lines": PICK, "text": LINES, "results": rows}, open(f"{OUT}/scores.json", "w"),
              ensure_ascii=False, indent=1)
    md = ["| | engine | words heard right | naturalness (UTMOS) | seconds |", "|---|---|---|---|---|"]
    md += [f"| {r['letter']} | {r['engine']} | {r['words']:.0%} | {r['mos']:.2f} | {r['seconds']} |" for r in rows]
    open(f"{OUT}/scores.md", "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "score"])
    ap.add_argument("--only", default="")
    ap.add_argument("--skip", default="")
    a = ap.parse_args()
    if a.cmd == "make":
        make({x for x in a.only.split(",") if x}, {x for x in a.skip.split(",") if x})
    else:
        score()
