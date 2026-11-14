"""Find canvas saves without a matching restore: draw every 0.25 s and compare the canvas save counts.

    python3 -I tools/save_check.py <kit> [lang=en|ar_sa] [step=0.25]

A missing restore raises no error: the transform piles up and the picture drifts (build 23's tag did).  Prints the
times whose frame left the canvas (or the episode's own buffer) with a different save count.
"""
import importlib.util
import os
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(KIT, "episodes"))

import skia  # noqa: E402


def main():
    kit = sys.argv[1]
    opts = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[2:] if "=" in a}
    lang, step = opts.get("lang", "en"), float(opts.get("step", 0.25))
    suffix = "" if lang == "en" else "_" + lang
    spec = importlib.util.spec_from_file_location("episode", os.path.join(KIT, "episodes", kit + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    vo = os.path.join(KIT, "series", "voice", kit + suffix)
    ep = mod.EPISODE(vo + ".json", vo + ".wav", lang)
    c = skia.Surface(1080, 1920).getCanvas()
    bad, t, n = [], 0.0, 0
    while t < ep.duration:
        n0 = c.getSaveCount()
        ep.draw(c, t)
        inner = ep.buf.getCanvas().getSaveCount() if ep.buf is not None else 1
        if c.getSaveCount() != n0 or inner != 1:
            bad.append(round(t, 2))
            c.restoreToCount(n0)
            if ep.buf is not None:
                ep.buf.getCanvas().restoreToCount(1)
        t += step
        n += 1
    print(f"{kit} [{lang}] {n} frames: " + ("save/restore balanced" if not bad else f"UNBALANCED at {bad[:12]}"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
