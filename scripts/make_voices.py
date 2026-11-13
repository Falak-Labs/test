"""Make the narration for one kit on the runner, without rendering (the Make voices workflow runs this).

    KIT=nuclear LANGS=en,ar FORCE=false python scripts/make_voices.py

English uses Phonon (free, voices.yml engine: phonon), Arabic uses ElevenLabs (engine: eleven, secret
ELEVENLABS_API_KEY). Files already in kit/series/voice are kept unless FORCE=true. Prints each voice's length;
the finished video is about 3 s longer (lead, the pause before "follow", tail).
"""
import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT_DIR = os.path.join(ROOT, "kit")
VOICES = yaml.safe_load(open(os.path.join(ROOT, "voices.yml"), encoding="utf-8")) or {}
kit = os.environ["KIT"].strip()
langs = [x.strip() for x in os.environ.get("LANGS", "en,ar").split(",") if x.strip()]
force = os.environ.get("FORCE", "false").lower() == "true"


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=KIT_DIR, check=True)


for lang in langs:
    suffix = "_ar_sa" if lang == "ar" else ""
    vo, lines = f"series/voice/{kit}{suffix}", f"series/{kit}_lines{suffix}.txt"
    if not os.path.exists(os.path.join(KIT_DIR, lines)):
        sys.exit(f"{lang}: {lines} is missing")
    if all(os.path.exists(os.path.join(KIT_DIR, vo + e)) for e in (".json", ".wav")) and not force:
        print(f"{lang}: {vo} already exists, kept (FORCE=true to make it again)")
        continue
    eng = VOICES.get(lang) or {}
    if eng.get("engine") == "eleven":
        if not os.environ.get("ELEVENLABS_API_KEY"):
            sys.exit("voices.yml asks for ElevenLabs but the ELEVENLABS_API_KEY secret is not set")
        try:                                                  # who is this voice? (name, accent labels; never the key)
            import requests
            r = requests.get(f"https://api.elevenlabs.io/v1/voices/{eng['voice']}",
                             headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}, timeout=30)
            if r.ok:
                v = r.json()
                print(f"== {lang} voice {eng['voice']}: {v.get('name')!r}, category {v.get('category')}, "
                      f"labels {v.get('labels')}, description {(v.get('description') or '')[:200]!r}", flush=True)
            else:
                print(f"== {lang} voice {eng['voice']}: lookup answered {r.status_code}", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"== voice lookup failed: {type(e).__name__}", flush=True)
        fit = ["--min", "0", "--max", "9999"] if kit.startswith("sample") else []      # samples keep natural speed
        run([sys.executable, "-I", "-u", "tools/make_vo_eleven.py", lines, vo, "--voice", str(eng["voice"]),
             "--model", eng.get("model", "eleven_multilingual_v2"), "--speed", str(eng.get("speed", 1.0)),
             "--pause", str(eng.get("pause", 0.22))] + fit)
    elif eng.get("engine") == "phonon":
        run([sys.executable, "-I", "-u", "tools/make_vo.py", lines, vo, "--verify", "--voice", str(eng.get("voice", "Easton"))])
        run([sys.executable, "-I", "-u", "tools/align_words.py", vo])
    else:
        sys.exit(f"{lang}: voices.yml names no engine this script knows ({eng})")
    d = json.load(open(os.path.join(KIT_DIR, vo + ".json"), encoding="utf-8"))
    print(f"== {lang}: {d.get('duration')} s of voice, {d.get('words')} words, tempo {d.get('tempo')} "
          f"-> video about {round(float(d.get('duration', 0)) + 3.1, 1)} s", flush=True)
