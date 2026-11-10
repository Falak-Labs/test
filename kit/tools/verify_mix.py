"""Whisper the final mix (voice + effects) line by line, to catch effects that mask words.

    python3 -I tools/verify_mix.py series/voice/<name> out/<dir>

Shifts each line of <name>.json to video time (lead 0.5 s, plus the 0.6 s fake pause before the CTA line), writes a
temporary json and runs tools/verify_vo.py on out/<dir>/mix.wav.
"""
import json
import os
import subprocess
import sys
import tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD, PAUSE, CTA_LINE = 0.5, 0.6, 10
WHISPER = os.environ.get("WHISPER_DIR", "/home/claude/tts/asr/sherpa-onnx-whisper-base.en")


def main():
    vo, out = sys.argv[1], sys.argv[2]
    js = json.load(open(vo + ".json"))
    for ln in js["lines"]:
        shift = LEAD + (PAUSE if ln["line"] >= CTA_LINE else 0.0)
        ln["start"] = round(ln["start"] + shift, 3)
        ln["end"] = round(ln["end"] + shift, 3)
        for w in ln.get("words", []):
            w["start"] = round(w["start"] + shift, 3)
            w["end"] = round(w["end"] + shift, 3)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(js, f)
        tmp = f.name
    try:
        subprocess.run([sys.executable, "-I", os.path.join(KIT, "tools", "verify_vo.py"), WHISPER,
                        os.path.join(out, "mix.wav"), tmp], check=True)
    finally:
        os.unlink(tmp)


if __name__ == "__main__":
    main()
