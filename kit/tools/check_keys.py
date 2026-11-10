"""Check that every caption anchor of an episode is found in a script, before any voice exists.

    python3 -I tools/check_keys.py episodes/<ep>.py series/<ep>_lines_ar_sa.txt [lang=ar_sa]

Builds a fake voice (evenly timed words + silent wav) from the script, builds the episode in that language and
lists every anchor that falls back to a beat fraction (word not found).  Prints OK when there are none.
"""
import importlib.util
import json
import os
import sys
import tempfile

import numpy as np
import soundfile as sf

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(KIT, "episodes"))


def fake_voice(lines, tmp):
    t, out = 0.0, []
    for i, text in enumerate(lines):
        ws = []
        for w in text.split():
            ws.append({"w": w, "start": round(t, 3), "end": round(t + 0.26, 3)})
            t += 0.28
        out.append({"line": i + 1, "start": round(ws[0]["start"] - 0.02, 3), "end": round(t, 3), "text": text, "words": ws})
        t += 0.35
    js = {"voice": "fake", "tempo": 1.0, "gap": 0.35, "duration": round(t, 3), "words": sum(len(x["words"]) for x in out),
          "words_per_sec": 3.5, "lines": out}
    jp, wp = os.path.join(tmp, "fake.json"), os.path.join(tmp, "fake.wav")
    with open(jp, "w") as f:
        json.dump(js, f, ensure_ascii=False)
    sf.write(wp, np.zeros(int((t + 1) * 16000), dtype="float32"), 16000)
    return jp, wp


def main():
    ep_path, lines_path = sys.argv[1], sys.argv[2]
    lang = next((a.split("=", 1)[1] for a in sys.argv[3:] if a.startswith("lang=")), "ar_sa")
    lines = [ln.strip() for ln in open(lines_path, encoding="utf-8") if ln.strip()]
    spec = importlib.util.spec_from_file_location("ep_under_test", ep_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cls = mod.EPISODE
    misses = []
    orig = cls.w

    def w(self, lab, key, frac=0.5, nth=0):
        k = self.KEYS.get(self.lang, {}).get((lab, key), key)
        if self.cap.find(lab, k, nth) is None:
            misses.append((lab, key, k))
        return orig(self, lab, key, frac, nth)

    cls.w = w
    with tempfile.TemporaryDirectory() as tmp:
        jp, wp = fake_voice(lines, tmp)
        ep = cls(jp, wp, lang=lang)
    print(f"{os.path.basename(ep_path)} [{lang}]: {len(lines)} lines, {len(ep.T)} anchors")
    if misses:
        for lab, key, k in misses:
            print(f"  MISSING  {lab:7s} {key:12s} -> {k}")
        sys.exit(1)
    print("  OK, every anchor found")


if __name__ == "__main__":
    main()
