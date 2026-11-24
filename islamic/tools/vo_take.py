"""One continuous ElevenLabs take of a whole script, per voice, with character timings (for captions and animation).

usage (on the GitHub runner, ELEVENLABS_API_KEY in the environment):
  python -I islamic/tools/vo_take.py islamic/lines/<name>.txt islamic/takes/<name> \
      --voices id1,id2 --model eleven_v4 --stability 0.5 --similarity 0.75

Why one request for the whole script: eleven_v4 / eleven_v3 shape each sentence from the text around it, so a single
take flows like one person talking (the reference sermons are one continuous talk). Audio tags such as [softly] or
[pause] are performance directions: they are sent to the model but never appear in the word list.

Writes, per voice:
  <out>/<voice>.wav   44.1 kHz mono PCM, as recorded (no processing)
  <out>/<voice>.json  {"voice", "model", "duration", "lines": [{"text", "start", "end", "words": [{"w","start","end"}]}]}
The key is read from the environment and is never printed or written.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import wave

import requests

ap = argparse.ArgumentParser()
ap.add_argument("lines")
ap.add_argument("out")
ap.add_argument("--voices", required=True)
ap.add_argument("--model", default="eleven_v4")
ap.add_argument("--stability", type=float, default=0.5)
ap.add_argument("--similarity", type=float, default=0.75)
ap.add_argument("--force", action="store_true")
a = ap.parse_args()

key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
if not key:
    sys.exit("ELEVENLABS_API_KEY is not set")

lines = [ln.strip() for ln in open(a.lines, encoding="utf-8") if ln.strip()]
text = "\n".join(lines)
os.makedirs(a.out, exist_ok=True)
TAG = re.compile(r"\[[^\]]*\]")


def post(voice, fmt):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format={fmt}"
    body = {"text": text, "model_id": a.model,
            "voice_settings": {"stability": a.stability, "similarity_boost": a.similarity}}
    for attempt in range(5):
        r = requests.post(url, headers={"xi-api-key": key, "Content-Type": "application/json"}, json=body, timeout=300)
        if r.status_code == 200:
            return r.json(), None
        msg = r.text[:400].replace(key, "***")
        if r.status_code in (400, 401, 403, 404, 422):
            return None, f"HTTP {r.status_code}: {msg}"
        print(f"  {voice}: HTTP {r.status_code}, retrying", flush=True)
        time.sleep(8 * (attempt + 1))
    return None, "kept failing"


def words_and_lines(chars, starts, ends):
    """Map the character timings back onto the script's lines and words, skipping [tags]."""
    s = "".join(chars)
    # find each line's span inside the sent text (the API echoes the text it spoke)
    out, pos = [], 0
    for ln in lines:
        i = s.find(ln, pos)
        if i < 0:
            i = pos
        j = i + len(ln)
        pos = j
        # mask tags
        spoken = list(ln)
        for m in TAG.finditer(ln):
            for k in range(m.start(), m.end()):
                spoken[k] = " "
        words, cur, k0 = [], "", None
        for k, ch in enumerate(spoken + [" "]):
            if ch.isspace():
                if cur.strip(" .،,:؟?!«»\"'"):
                    ks = [x for x in range(k0, k) if i + x < len(starts)]
                    if ks:
                        words.append({"w": cur, "start": round(starts[i + ks[0]], 3), "end": round(ends[i + ks[-1]], 3)})
                cur, k0 = "", None
                continue
            if k0 is None:
                k0 = k
            cur += ch
        if words:
            out.append({"text": TAG.sub("", ln).strip(), "start": words[0]["start"], "end": words[-1]["end"], "words": words})
        else:
            out.append({"text": TAG.sub("", ln).strip(), "start": None, "end": None, "words": []})
    return out


report = []
for voice in [v.strip() for v in a.voices.split(",") if v.strip()]:
    wav, js = os.path.join(a.out, f"{voice}.wav"), os.path.join(a.out, f"{voice}.json")
    if not a.force and os.path.exists(wav) and os.path.exists(js):
        old = json.load(open(js, encoding="utf-8"))
        if old.get("text") == text and old.get("model") == a.model:
            print(f"{voice}: unchanged, skipped")
            continue
    d, err = post(voice, "pcm_44100")
    fmt = "pcm_44100"
    if d is None and err and "output_format" in err:
        d, err = post(voice, "mp3_44100_192")
        fmt = "mp3_44100_192"
    if d is None:
        print(f"{voice}: FAILED {err}")
        report.append({"voice": voice, "error": err})
        continue
    raw = base64.b64decode(d["audio_base64"])
    if fmt == "pcm_44100":
        with wave.open(wav, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(raw)
        dur = len(raw) / 2 / 44100
    else:
        open(wav.replace(".wav", ".mp3"), "wb").write(raw)
        os.system(f'ffmpeg -v error -y -i "{wav.replace(".wav", ".mp3")}" -ac 1 -ar 44100 "{wav}"')
        dur = None
    al = d.get("alignment") or d.get("normalized_alignment") or {}
    ch, st, en = al.get("characters", []), al.get("character_start_times_seconds", []), al.get("character_end_times_seconds", [])
    json.dump({"voice": voice, "model": a.model, "format": fmt, "text": text,
               "settings": {"stability": a.stability, "similarity_boost": a.similarity},
               "duration": round(dur, 3) if dur else None, "lines": words_and_lines(ch, st, en),
               "chars": ch, "starts": st, "ends": en}, open(js, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"{voice}: {fmt}, {dur and round(dur, 1)} s, {len(text)} characters")
    report.append({"voice": voice, "format": fmt, "seconds": dur and round(dur, 2), "characters": len(text)})
json.dump(report, open(os.path.join(a.out, "report.json"), "w"), indent=1)
