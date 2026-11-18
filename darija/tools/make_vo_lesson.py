"""Voices for one Darija -> English lesson, with ElevenLabs. Based on kit/tools/make_vo_eleven.py, for a script with
several speakers. Needs ELEVENLABS_API_KEY in the environment (a GitHub Actions secret: the cloud workspace cannot
reach ElevenLabs), so it runs on GitHub's runner from the "Darija lesson voice" workflow.

usage:
  python3 -I darija/tools/make_vo_lesson.py <darija/lines/ep03.txt> <darija/voice/ep03> [--voices darija/voices.json] [--force]

- The script has one line per sentence:    SPEAKER | id | text to say            (optional 4th field: speed=0.9 style=0.3)
  SPEAKER is a key of voices.json (T teacher, A Adam, L Lina). id names the take (letters, digits, _ and -).
  Empty lines and lines that start with # are skipped.
- One request per line and one take per request. Writes <out>/<id>.mp3 and <out>/<id>.json (text, voice, model,
  settings and ElevenLabs' own character timings, so captions land on the words) and <out>/manifest.json
  (status, model, the lines in order, characters requested this run).
- Run it again and only new or changed lines are requested (credits are spent once per line); --force records all.
- "model" in voices.json is one model ID, or a list in order of preference: the first one the key can use is taken.
- If a request is refused, the takes made so far are kept and manifest.json says which line failed and why.
- The key is read from the environment and is never printed or written anywhere.
"""
import argparse
import base64
import json
import os
import re
import sys
import time

import requests

API = "https://api.elevenlabs.io/v1"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument("lines")
ap.add_argument("out")
ap.add_argument("--voices", default=os.path.join(HERE, "voices.json"))
ap.add_argument("--force", action="store_true")
a = ap.parse_args()

key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
if not key:
    sys.exit("ELEVENLABS_API_KEY is not set (add it as a GitHub Actions secret)")
HEAD = {"xi-api-key": key}


def clean(s):
    return str(s)[:300].replace(key, "***")


cfg = json.load(open(a.voices, encoding="utf-8"))
speakers = cfg["speakers"]
want = cfg["model"] if isinstance(cfg["model"], list) else [cfg["model"]]
fmt = cfg.get("output_format", "mp3_44100_128")
name = os.path.basename(a.out.rstrip("/"))

script, seen = [], set()
for n, raw in enumerate(open(a.lines, encoding="utf-8"), 1):
    ln = raw.strip()
    if not ln or ln.startswith("#"):
        continue
    parts = [p.strip() for p in ln.split("|")]
    if len(parts) < 3 or not parts[2]:
        sys.exit(f"{a.lines}:{n}: expected   SPEAKER | id | text to say")
    sp, tid, text = parts[0], parts[1], parts[2]
    if sp not in speakers:
        sys.exit(f"{a.lines}:{n}: unknown speaker {sp!r} (voices.json has {', '.join(speakers)})")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", tid) or tid in seen or tid == "manifest":
        sys.exit(f"{a.lines}:{n}: id {tid!r} must be unique and made of letters, digits, _ or -")
    seen.add(tid)
    opts = {}
    for tok in " ".join(parts[3:]).split():
        k, _, v = tok.partition("=")
        try:
            opts[k] = float(v)
        except ValueError:
            sys.exit(f"{a.lines}:{n}: bad setting {tok!r} (write name=number, e.g. speed=0.9)")
    script.append({"id": tid, "speaker": sp, "voice": speakers[sp]["voice"], "text": text, "opts": opts})
if not script:
    sys.exit(f"{a.lines}: no lines to record")
os.makedirs(a.out, exist_ok=True)


def settings_for(model, line):
    s = dict(cfg.get("settings", {}).get(model, {}))
    s.update(speakers[line["speaker"]].get("settings", {}).get(model, {}))
    s.update(line["opts"])
    return s


state = {"model": None, "available": [], "sent": 0, "made": [], "notes": []}


def manifest(status, error=None):
    rows = []
    for L in script:
        t = L.get("take") or {}
        ends = t.get("ends") or []
        rows.append({"id": L["id"], "speaker": L["speaker"], "voice": L["voice"], "text": L["text"], "characters": len(L["text"]),
                     "model": t.get("model"), "seconds": round(ends[-1], 3) if ends else None})
    json.dump({"episode": name, "status": status, "error": error, "model": state["model"], "models_available": state["available"],
               "requested_characters": state["sent"], "recorded_this_run": state["made"], "notes": state["notes"], "lines": rows},
              open(os.path.join(a.out, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def fail(msg):
    manifest("failed", msg)
    sys.exit(msg)


# which of the wanted models this key can use (asking costs no credits; a key without that permission just skips the check)
try:
    r = requests.get(API + "/models", headers=HEAD, timeout=60)
    if r.status_code == 200:
        state["available"] = [m["model_id"] for m in r.json() if m.get("can_do_text_to_speech")]
except requests.RequestException:
    pass
models = [m for m in want if not state["available"] or m in state["available"]]
if not models:
    fail(f"none of the models {want} can be used with this key; it offers: {', '.join(state['available'])}")


def tts(voice, body):
    url = f"{API}/text-to-speech/{voice}/with-timestamps?output_format={fmt}"
    for attempt in range(5):
        try:
            r = requests.post(url, headers={**HEAD, "Content-Type": "application/json"}, json=body, timeout=180)
        except requests.RequestException as e:
            print(f"  network error ({type(e).__name__}), retrying", flush=True)
            time.sleep(6 * (attempt + 1))
            continue
        if r.status_code == 200:
            return r.json(), None
        msg = clean(r.text)
        if r.status_code in (401, 403):
            fail(f"ElevenLabs refused the request ({r.status_code}): {msg}")
        if r.status_code in (400, 404, 422):
            return None, f"{r.status_code}: {msg}"
        print(f"  HTTP {r.status_code}, retrying: {msg}", flush=True)
        time.sleep(6 * (attempt + 1))
    return None, "kept failing after 5 tries"


for L in script:
    mp3, js = os.path.join(a.out, L["id"] + ".mp3"), os.path.join(a.out, L["id"] + ".json")
    if not a.force and os.path.exists(mp3) and os.path.exists(js):
        old = json.load(open(js, encoding="utf-8"))
        if (old.get("text") == L["text"] and old.get("voice") == L["voice"] and old.get("model") in want
                and old.get("settings") == settings_for(old.get("model"), L)):
            L["take"] = old
            state["model"] = state["model"] or old.get("model")     # new lines keep the model of the takes already made
            continue
    d, tried = None, []
    for m in ([state["model"]] if state["model"] else models):
        body = {"text": L["text"], "model_id": m}
        s = settings_for(m, L)
        if s:
            body["voice_settings"] = s
        d, err = tts(L["voice"], body)
        if d:
            state["model"] = m
            break
        tried.append(f"{m} -> {err}")
    if not d:
        fail(f"ElevenLabs refused line {L['id']} ({L['speaker']}): " + " | ".join(tried))
    state["notes"] += [f"line {L['id']}: {t}" for t in tried]          # a model that was refused before one worked
    al = d.get("alignment") or d.get("normalized_alignment") or {}
    L["take"] = {"id": L["id"], "speaker": L["speaker"], "text": L["text"], "voice": L["voice"], "model": state["model"],
                 "settings": settings_for(state["model"], L), "chars": al.get("characters", []),
                 "starts": al.get("character_start_times_seconds", []), "ends": al.get("character_end_times_seconds", [])}
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(L["take"], open(js, "w", encoding="utf-8"), ensure_ascii=False)
    state["sent"] += len(L["text"])
    state["made"].append(L["id"])
    print(f"  {L['id']} recorded ({L['speaker']}, {len(L['text'])} characters, {state['model']})", flush=True)

if state["model"] is None:
    state["model"] = next((L["take"].get("model") for L in script if L.get("take")), None)
manifest("ok")
print(f"ElevenLabs {state['model']}: {len(script)} lines, {len(state['made'])} recorded this run, "
      f"{state['sent']} characters requested -> {a.out}")
