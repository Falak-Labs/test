#!/usr/bin/env python3
"""Publish a Seedance-style build the way produce.py does: media/<slug>-<lang>.mp4 and review/<slug>/.

usage (from kit/): python3 tools/seedance_publish.py <slug> <kit> [langs=en,ar]
  needs episodes/<kit>_sd.json (shot list, see series/SEEDANCE_STYLE.md), series/voice/<kit>.json/.wav and
  series/voice/<kit>_ar_sa.json/.wav, and the clips in out/aishots/ (scripts/ai_media.py get <name> kit/out/aishots).
A language that fails a gate goes to review/<slug>/REJECTED-<slug>-<lang>.mp4 and never to media/.
"""
import json, os, re, shutil, subprocess, sys

from PIL import Image

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(KIT)
GATE = {"en": (55.0, 75.0), "ar": (55.0, 85.0)}


def main():
    slug, kit = sys.argv[1], sys.argv[2]
    langs = (sys.argv[3] if len(sys.argv) > 3 else "en,ar").split(",")
    spec = os.path.join(KIT, "episodes", f"{kit}_sd.json")
    dst = os.path.join(ROOT, "review", slug)
    os.makedirs(dst, exist_ok=True)
    report, failed = {"slug": slug, "kit": kit, "style": "seedance"}, False
    for lang in langs:
        vo = os.path.join(KIT, "series", "voice", kit + ("_ar_sa" if lang == "ar" else ""))
        out = os.path.join(KIT, "out", f"{kit}_sd_{lang}")
        r = subprocess.run([sys.executable, "-I", os.path.join(KIT, "tools", "seedance_cut.py"), spec, vo, out, lang],
                           capture_output=True, text=True, cwd=KIT)
        rep = report.setdefault(lang, {})
        m = re.search(r"QA\s+duration ([\d.]+)s\s+loudness (-?[\d.]+) LUFS\s+true peak (-?[\d.]+) dBFS", r.stdout)
        if r.returncode or not m:
            rep["error"] = (r.stderr or r.stdout)[-400:]
            failed = True
            continue
        dur, lufs, peak = map(float, m.groups())
        lo, hi = GATE[lang]
        issues = []
        if not lo <= dur <= hi:
            issues.append(f"length {dur:.1f}s outside {lo}-{hi}")
        if not -15.0 <= lufs <= -13.0:
            issues.append(f"loudness {lufs}")
        if peak > -0.9:
            issues.append(f"peak {peak}")
        final = [f for f in os.listdir(out) if f.endswith(f"_{lang}_final.mp4")][0]
        final = os.path.join(out, final)
        rep.update(duration=dur, lufs=lufs, peak=peak, frame="1080x1920", fps="30", issues=issues,
                   size_mb=round(os.path.getsize(final) / 1e6, 1))
        shutil.copy(os.path.join(out, "qa_sheet.png"), os.path.join(dst, f"qa_{lang}.png"))
        Image.open(os.path.join(out, "cover.png")).convert("RGB").save(os.path.join(dst, f"cover_{lang}.jpg"), quality=88)
        rep["cover"] = True
        if issues:
            shutil.copy(final, os.path.join(dst, f"REJECTED-{slug}-{lang}.mp4"))
            failed = True
        else:
            os.makedirs(os.path.join(ROOT, "media"), exist_ok=True)
            shutil.copy(final, os.path.join(ROOT, "media", f"{slug}-{lang}.mp4"))
            rep["ok"] = True
        for f in os.listdir(out):                      # keep the disk free: segments are rebuilt when needed
            if f.startswith("seg") or f == "joined.mp4":
                os.remove(os.path.join(out, f))
    json.dump(report, open(os.path.join(dst, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
