"""Narration with ElevenLabs, for either language. Needs ELEVENLABS_API_KEY in the environment (a GitHub Actions
secret: the cloud workspace cannot reach ElevenLabs), so it runs on GitHub's runner from scripts/produce.py.

usage:
  python3 -I tools/make_vo_eleven.py <lines.txt> <out_prefix> --voice <voice_id> [--model eleven_multilingual_v2]
        [--gap 0.35] [--max 66.0] [--speed 1.0] [--only 3,7]

- One request per line, with the line before and the line after sent as context so the delivery flows from line to
  line. Word times come from ElevenLabs' own character timings, so captions and animation cues land on the words.
- Writes the same files as the other voice tools: <out>.wav / .json (line and word times) / .mp3 (-14 LUFS preview),
  plus <out>_lines/ with one take per line (L01.mp3 + L01.json). Run it again and only missing lines are requested;
  --only 3,7 records lines 3 and 7 again and keeps the rest (credits are spent only on what is requested).
- Pauses inside a line longer than --pause seconds are shortened (ElevenLabs pauses long at commas).
- A voice longer than --max seconds is sped up (12% at most), one shorter than --min slowed down (8% at most), so the
  video stays inside its length window.
- The key is read from the environment and is never printed or written anywhere.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time

import numpy as np
import requests
import soundfile as sf

SR = 24000
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128"

ap = argparse.ArgumentParser()
ap.add_argument("lines")
ap.add_argument("out")
ap.add_argument("--voice", required=True)
ap.add_argument("--model", default="eleven_multilingual_v2")
ap.add_argument("--gap", type=float, default=0.35)
ap.add_argument("--max", type=float, default=66.0)
ap.add_argument("--min", type=float, default=59.0)
ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--pause", type=float, default=0.22, help="longest pause kept inside a line, seconds")
ap.add_argument("--stability", type=float, default=0.45)
ap.add_argument("--similarity", type=float, default=0.8)
ap.add_argument("--style", type=float, default=0.2)
ap.add_argument("--only", default="")
a = ap.parse_args()

key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
if not key:
    sys.exit("ELEVENLABS_API_KEY is not set (add it as a GitHub Actions secret)")

lines = [ln.strip() for ln in open(a.lines, encoding="utf-8") if ln.strip()]
only = {int(x) for x in a.only.split(",") if x.strip()}
ldir = a.out + "_lines"
os.makedirs(ldir, exist_ok=True)


def decode(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def request(i):
    body = {"text": lines[i], "model_id": a.model,
            "voice_settings": {"stability": a.stability, "similarity_boost": a.similarity, "style": a.style,
                               "use_speaker_boost": True, "speed": a.speed}}
    if a.model.startswith("eleven_multilingual") or a.model.startswith("eleven_turbo") or a.model.startswith("eleven_flash"):
        if i > 0:
            body["previous_text"] = lines[i - 1]
        if i + 1 < len(lines):
            body["next_text"] = lines[i + 1]
    for attempt in range(5):
        r = requests.post(API.format(voice=a.voice), headers={"xi-api-key": key, "Content-Type": "application/json"},
                          json=body, timeout=180)
        if r.status_code == 200:
            return r.json()
        msg = r.text[:300].replace(key, "***")
        if r.status_code in (401, 403):
            sys.exit(f"ElevenLabs refused the key ({r.status_code}): {msg}")
        if r.status_code in (400, 404, 422):
            sys.exit(f"ElevenLabs refused line {i + 1} ({r.status_code}): {msg}")
        print(f"  line {i + 1}: HTTP {r.status_code}, retrying: {msg}", flush=True)
        time.sleep(6 * (attempt + 1))
    sys.exit(f"ElevenLabs kept failing on line {i + 1}")


sent = 0
for i in range(len(lines)):
    mp3, js = os.path.join(ldir, f"L{i + 1:02d}.mp3"), os.path.join(ldir, f"L{i + 1:02d}.json")
    if os.path.exists(mp3) and os.path.exists(js) and (i + 1) not in only:
        old = json.load(open(js, encoding="utf-8"))
        if (old.get("text") == lines[i] and old.get("voice") == a.voice and old.get("model") == a.model
                and abs(old.get("speed", 1.0) - a.speed) < 1e-6):
            continue
    d = request(i)
    sent += len(lines[i])
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    al = d.get("alignment") or d.get("normalized_alignment") or {}
    json.dump({"text": lines[i], "voice": a.voice, "model": a.model, "speed": a.speed, "chars": al.get("characters", []),
               "starts": al.get("character_start_times_seconds", []), "ends": al.get("character_end_times_seconds", [])},
              open(js, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"  L{i + 1:02d} recorded ({len(lines[i])} characters)", flush=True)


def words_of(chars, starts, ends):
    out, cur, s0, e0 = [], "", None, None
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if cur:
                out.append({"w": cur, "start": s0, "end": e0})
            cur, s0 = "", None
            continue
        if not cur:
            s0 = s
        cur += ch
        e0 = e
    if cur:
        out.append({"w": cur, "start": s0, "end": e0})
    return out


def cap_pauses(y, cap):
    """Shorten every quiet stretch inside a line to `cap` seconds. Returns the audio and a time map old -> new."""
    hop = int(0.01 * SR)
    n = len(y) // hop
    if cap <= 0 or n < 3:
        return y, (lambda t: t)
    e = np.array([np.sqrt(np.mean(y[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    quiet = e < max(1e-4, 0.03 * np.percentile(e, 95))
    cuts, i = [], 0
    while i < n:
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < n and quiet[j]:
            j += 1
        if (j - i) * 0.01 > cap:
            c0, c1 = i * 0.01 + cap / 2, j * 0.01 - cap / 2
            if c1 > c0:
                cuts.append((c0, c1))
        i = j
    if not cuts:
        return y, (lambda t: t)
    parts, last = [], 0.0
    for c0, c1 in cuts:
        parts.append(y[int(last * SR): int(c0 * SR)])
        last = c1
    parts.append(y[int(last * SR):])

    def remap(t):
        d = 0.0
        for c0, c1 in cuts:
            if t >= c1:
                d += c1 - c0
            elif t > c0:
                d += t - c0
        return t - d
    return np.concatenate(parts).astype(np.float32), remap


gap = np.zeros(int(a.gap * SR), np.float32)
audio, out_lines, t = [], [], 0.0
for i in range(len(lines)):
    take = json.load(open(os.path.join(ldir, f"L{i + 1:02d}.json"), encoding="utf-8"))
    y = decode(os.path.join(ldir, f"L{i + 1:02d}.mp3"))
    nz = np.where(np.abs(y) > 0.01)[0]
    a0 = max(0, nz[0] - int(0.04 * SR)) if len(nz) else 0
    a1 = min(len(y), nz[-1] + int(0.10 * SR)) if len(nz) else len(y)
    y = y[a0:a1]
    shift = a0 / SR
    y, remap = cap_pauses(y, a.pause)
    ws = [{"w": w["w"], "start": round(t + remap(max(0.0, w["start"] - shift)), 3),
           "end": round(t + remap(max(0.0, w["end"] - shift)), 3)}
          for w in words_of(take["chars"], take["starts"], take["ends"])]
    if i:
        audio.append(gap)
        t += a.gap
        ws = [dict(w, start=round(w["start"] + a.gap, 3), end=round(w["end"] + a.gap, 3)) for w in ws]
    out_lines.append({"line": i + 1, "start": round(t, 3), "end": round(t + len(y) / SR, 3), "text": lines[i], "words": ws})
    audio.append(y)
    t += len(y) / SR
voice = np.concatenate(audio)
dur = len(voice) / SR

tempo = 1.0
if dur > a.max:
    tempo = min(1.12, dur / a.max)
elif dur < a.min:                                     # a fast reader: slow down a little so the video is long enough
    tempo = max(0.92, dur / a.min)
if tempo != 1.0:
    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/in.wav", voice, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{td}/in.wav", "-filter:a", f"atempo={tempo:.4f}", "-ar", str(SR),
                        f"{td}/out.wav"], check=True)
        voice, _ = sf.read(f"{td}/out.wav", dtype="float32")
    for L in out_lines:
        L["start"], L["end"] = round(L["start"] / tempo, 3), round(L["end"] / tempo, 3)
        for w in L["words"]:
            w["start"], w["end"] = round(w["start"] / tempo, 3), round(w["end"] / tempo, 3)
    dur = len(voice) / SR

sf.write(a.out + ".wav", voice, SR, subtype="PCM_16")
n_words = sum(len(L["words"]) for L in out_lines)
json.dump({"voice": f"elevenlabs:{a.voice}", "model": a.model, "tempo": round(tempo, 4), "gap": a.gap, "duration": round(dur, 3),
           "words": n_words, "words_per_sec": round(n_words / dur, 2), "lines": out_lines},
          open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out + ".wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100",
                "-b:a", "160k", a.out + ".mp3"], check=True)
print(f"ElevenLabs {a.voice} ({a.model}): {len(lines)} lines, {n_words} words, {dur:.2f}s of voice"
      f"{f' (tempo x{tempo:.3f})' if tempo != 1 else ''}, {sent} characters requested this run -> {a.out}.wav")
