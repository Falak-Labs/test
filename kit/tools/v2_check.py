"""Check a v2 episode before rendering: are all anchors found, then stills -> one contact sheet.

    python3 -I tools/v2_check.py <kit> [lang=en|ar_sa] [beats | t1,t2,...] [out=out/<kit>_chk] [cols=5] [scale=0.3]

- Voice: series/voice/<kit>[_ar_sa].json + .wav when they exist, else a fake evenly timed voice built from the script
  (enough to check anchors, captions and layout before the real voice exists; real timings will differ).
- Prints the duration, the start of every beat, every anchor in T and the anchors whose word was NOT FOUND in its line.
- "beats" (default) renders the middle of each of the 14 beats; or give times in seconds, comma separated.
- sweep=0.5 : instead of stills, draw a frame every 0.5 s through the whole episode and build the sound list (finds
  crashes at moments you never looked at, and slow frames).  Takes 2-3 minutes.
- anchors only (no stills): add  nostills=1.   Keep the full-size frames: add  keep=1  (they are deleted otherwise).
"""
import importlib.util
import os
import sys
import tempfile
import time

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(KIT, "episodes"))
sys.path.insert(0, os.path.join(KIT, "tools"))


def main():
    kit = sys.argv[1]
    opts = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[2:] if "=" in a}
    rest = [a for a in sys.argv[2:] if "=" not in a]
    lang = opts.get("lang", "en")
    suffix = "" if lang == "en" else "_" + lang
    vo = os.path.join(KIT, "series", "voice", kit + suffix)
    spec = importlib.util.spec_from_file_location("episode", os.path.join(KIT, "episodes", kit + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tmp = None
    if os.path.exists(vo + ".json") and os.path.exists(vo + ".wav") and not opts.get("fake"):
        jp, wp = vo + ".json", vo + ".wav"
    else:
        from check_keys import fake_voice
        lines_path = os.path.join(KIT, "series", f"{kit}_lines{suffix}.txt")
        lines = [ln.strip() for ln in open(lines_path, encoding="utf-8") if ln.strip()]
        tmp = tempfile.TemporaryDirectory()
        jp, wp = fake_voice(lines, tmp.name)
        print(f"(fake voice from {os.path.basename(lines_path)}: timings are not the real ones)")
    ep = mod.EPISODE(jp, wp, lang=lang)
    print(f"{kit} [{lang}] duration {ep.duration:.2f}s")
    print("beats: " + "  ".join(f"{lab} {ep.tl.s(lab):.2f}" for lab in ep.tl.labels))
    print("T: " + "  ".join(f"{k} {v:.2f}" for k, v in sorted(ep.T.items(), key=lambda kv: kv[1])))
    if ep.missing:
        print("ANCHORS NOT FOUND (they fall back to a beat fraction): " + "; ".join(f"{lab}/{key}" + (f" -> {k}" if k != key else "")
                                                                               for lab, key, k in ep.missing))
    else:
        print("anchors: all found")
    if opts.get("sweep"):                         # draw a frame every N seconds through the whole episode: catches crashes
        import numpy as np
        import skia
        step = float(opts["sweep"])
        surf = skia.Surface(1080, 1920)
        c = surf.getCanvas()
        t, n, worst, t0 = 0.0, 0, (0.0, 0.0), time.time()
        while t < ep.duration:
            f0 = time.time()
            c.save()
            ep.draw(c, t)
            c.restore()
            d = time.time() - f0
            if d > worst[0]:
                worst = (d, t)
            n += 1
            t += step
        ev = ep.sfx_events()
        bad = [i for i, e in enumerate(ev) if not (len(e) == 3 and (e[0] is None or isinstance(e[0], (int, float)))
                                                   and (e[1] is None or isinstance(e[1], np.ndarray)) and isinstance(e[2], (int, float)))]
        late = [round(e[0], 2) for e in ev if e[0] is not None and not -0.5 <= e[0] <= ep.duration]
        print(f"sweep: {n} frames drawn without errors in {time.time() - t0:.0f}s; slowest {worst[0]:.2f}s at t={worst[1]:.1f}; "
              f"{len(ev)} sounds" + (f"; BAD sound entries at {bad}" if bad else "") + (f"; sounds outside the video: {late}" if late else ""))
        return
    if opts.get("nostills"):
        return
    from bik.render import still, contact_sheet
    if rest and rest[0] != "beats":
        times = [float(x) for x in rest[0].split(",")]
        labels = [f"{t:.2f}s" for t in times]
    else:
        times = [(ep.tl.s(lab) + ep.tl.e(lab)) / 2 for lab in ep.tl.labels]
        labels = [f"{lab} {t:.1f}s" for lab, t in zip(ep.tl.labels, times)]
    out = opts.get("out", os.path.join(KIT, "out", f"{kit}{suffix}_chk"))
    os.makedirs(out, exist_ok=True)
    t0 = time.time()
    paths = [still(ep, t, os.path.join(out, f"f{t:06.2f}.png")) for t in times]
    sheet = contact_sheet(paths, labels, os.path.join(out, "sheet.png"), cols=int(opts.get("cols", 5)), scale=float(opts.get("scale", 0.3)))
    print(f"{len(times)} stills in {time.time() - t0:.0f}s -> {sheet}")
    if not opts.get("keep"):                      # full-size frames are ~4 MB each: keep only the sheet (keep=1 to keep them)
        for p_ in paths:
            try:
                os.remove(p_)
            except OSError:
                pass
    if tmp:
        tmp.cleanup()


if __name__ == "__main__":
    main()
