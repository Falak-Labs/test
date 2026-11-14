"""Draw an episode's cover (the picture that becomes frame 0 of the video and the post's cover).

    python3 -I tools/make_cover.py <kit> [lang=en|ar_sa] [out=out/<kit>_cover.png] [t=<seconds>|t=<beat>]

Uses the real voice (series/voice/<kit>[_ar_sa].json + .wav), else a fake evenly timed one built from the script.
Prints the name it found in the closing line, the title size and where the text block sits (it must stay inside
y 240-1680, the part of the frame that profile grids show).
"""
import importlib.util
import os
import sys
import tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(KIT, "episodes"))
sys.path.insert(0, os.path.join(KIT, "tools"))


def main():
    kit = sys.argv[1]
    opts = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[2:] if "=" in a}
    lang = opts.get("lang", "en")
    suffix = "" if lang == "en" else "_" + lang
    vo = os.path.join(KIT, "series", "voice", kit + suffix)
    spec = importlib.util.spec_from_file_location("episode", os.path.join(KIT, "episodes", kit + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tmp = None
    if os.path.exists(vo + ".json") and os.path.exists(vo + ".wav"):
        jp, wp = vo + ".json", vo + ".wav"
    else:
        from check_keys import fake_voice
        lines = [ln.strip() for ln in open(os.path.join(KIT, "series", f"{kit}_lines{suffix}.txt"), encoding="utf-8") if ln.strip()]
        tmp = tempfile.TemporaryDirectory()
        jp, wp = fake_voice(lines, tmp.name)
        print("(fake voice: timings are not the real ones)")
    ep = mod.EPISODE(jp, wp, lang=lang)
    if "t" in opts:
        v = opts["t"]
        ep.COVER_T = v if not v.replace(".", "").isdigit() else float(v)
    import skia
    surf = skia.Surface(1080, 1920)
    info = ep.draw_cover(surf.getCanvas())
    out = opts.get("out") or os.path.join(KIT, "out", f"{kit}{suffix}_cover.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    surf.makeImageSnapshot().save(out, skia.kPNG)
    inside = 240 <= info["top_of_text"] and info["bottom"] <= 1680
    print(f"{kit} [{lang}] cover at {ep.cover_time():.2f}s: \"{info['small']}\" / {info['lines']} size {info['size']}"
          f"  text y {info['top_of_text']:.0f}-{info['bottom']:.0f} {'inside' if inside else 'OUTSIDE'} the grid crop  -> {out}")


if __name__ == "__main__":
    main()
