"""Render stills of an episode at given times into a contact sheet.

python3 tools/stills.py episodes/<name>.py series/voice/<name> out/<dir> 0.3 1.6 3.2 ... [lang=ar_sa] [cols=4] [scale=0.4]
Also prints the beat times and every anchor the scene resolved (T), so each still can be checked against its word.
"""
import importlib.util
import os
import sys
import time

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
from bik.render import still, contact_sheet  # noqa: E402


def load(path):
    spec = importlib.util.spec_from_file_location("episode", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ep, vo, out = sys.argv[1:4]
    opts = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[4:] if "=" in a}
    times = [float(a) for a in sys.argv[4:] if "=" not in a]
    lang = opts.get("lang", "en")
    cols = int(opts.get("cols", 4))
    scale = float(opts.get("scale", 0.4))
    tag = opts.get("tag", "sheet")
    os.makedirs(out, exist_ok=True)
    m = load(ep)
    scene = m.EPISODE(vo + ".json", vo + ".wav", lang=lang)
    tl = scene.tl
    print(f"duration {scene.duration:.2f}  pause {tl.pause_start:.2f}")
    print("  ".join(f"{lab} {tl.s(lab):.2f}" for lab in tl.labels))
    T = getattr(scene, "T", {})
    print("  ".join(f"{k}={v:.2f}" for k, v in sorted(T.items(), key=lambda kv: kv[1])))
    paths, labels = [], []
    for t in times:
        p = os.path.join(out, f"{tag}_{t:06.2f}.png")
        t0 = time.time()
        still(scene, t, p)
        lab = next((lb for lb in reversed(tl.labels) if tl.s(lb) - 0.4 <= t), "hook")
        paths.append(p)
        labels.append(f"{t:.2f}s {lab}")
        print(f"{p}  {time.time() - t0:.2f}s")
    sheet = contact_sheet(paths, labels, os.path.join(out, f"{tag}.png"), cols=cols, scale=scale)
    print(sheet)


if __name__ == "__main__":
    main()
