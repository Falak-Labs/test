"""Make the missing videos on GitHub's runners: Saudi voice (NAMAA), renders, checks.

    python scripts/produce.py plan [--only slug,slug] [--langs en,ar] [--force]   -> lines for $GITHUB_OUTPUT
    python scripts/produce.py make <slug> <kit> <langs> <look>                    -> ci_out/<slug>/
    python scripts/produce.py collect                                             -> media/, review/, kit/series/voice/

A video is copied to media/ only if it passes the gates (length, loudness, peak).  Everything needed to judge it
goes to review/<slug>/: the check sheet (one frame per beat), the numbers, and for Arabic what Whisper heard per line.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, "kit")
OUT = os.path.join(ROOT, "ci_out")
LANG = {"en": {"lines": "{kit}_lines.txt", "voice": "{kit}", "out": "{kit}", "arg": []},
        "ar": {"lines": "{kit}_lines_ar_sa.txt", "voice": "{kit}_ar_sa", "out": "{kit}_ar_sa", "arg": ["lang=ar_sa"]}}
GATE = {"en": (61.0, 70.5), "ar": (60.5, 80.0)}


def episodes():
    return yaml.safe_load(open(os.path.join(ROOT, "episodes.yml"), encoding="utf-8"))["episodes"]


def plan(a):
    only = {s for s in a.only.split(",") if s}
    langs = [s for s in a.langs.split(",") if s]
    rows = []
    for e in episodes():
        if only and e["slug"] not in only:
            continue
        need = []
        for lang in langs:
            lines = os.path.join(KIT, "series", LANG[lang]["lines"].format(kit=e["kit"]))
            scene = os.path.join(KIT, "episodes", e["kit"] + ".py")
            media = os.path.join(ROOT, "media", f"{e['slug']}-{lang}.mp4")
            if os.path.exists(lines) and os.path.exists(scene) and (a.force or not os.path.exists(media)):
                need.append(lang)
        if need:
            rows.append({"slug": e["slug"], "kit": e["kit"], "langs": ",".join(need), "ar": "ar" in need,
                         "look": int(e.get("look", 1))})
    print("matrix=" + json.dumps(rows))
    print("any=" + ("true" if rows else "false"))


def run(cmd, log, env=None):
    print("$ " + " ".join(cmd), flush=True)
    p = subprocess.Popen(cmd, cwd=KIT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    out = []
    for line in p.stdout:
        print(line, end="", flush=True)
        out.append(line)
    p.wait()
    log.extend(out)
    if p.returncode:
        raise RuntimeError(f"exit {p.returncode}: {' '.join(cmd)}")
    return "".join(out)


VOICES = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "voices.yml"))) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "voices.yml")) else {}


def make(slug, kit, langs, look):
    dst = os.path.join(OUT, slug)
    for sub in ("media", "review", "voice"):
        os.makedirs(os.path.join(dst, sub), exist_ok=True)
    env = dict(os.environ)
    if int(look) >= 2:                                   # new format: fine grain needs a stronger encode to stay ~23 MB
        env.setdefault("BIK_CRF", "24")
        env.setdefault("BIK_PRESET", "medium")
    report = {"slug": slug, "kit": kit, "langs": {}}
    failed = False
    for lang in langs.split(","):
        L, log, rep = LANG[lang], [], {"ok": False}
        report["langs"][lang] = rep
        try:
            vo = os.path.join("series", "voice", L["voice"].format(kit=kit))
            have = os.path.exists(os.path.join(KIT, vo + ".json")) and os.path.exists(os.path.join(KIT, vo + ".wav"))
            fix = os.environ.get("FIX_LINES", "").strip() if lang == "ar" else ""      # "6,11": take those Saudi lines again
            eng = VOICES.get(lang) or {}
            if not have or fix:
                if eng.get("engine") == "eleven":                                     # ElevenLabs (voices.yml)
                    if not os.environ.get("ELEVENLABS_API_KEY"):
                        raise RuntimeError("voices.yml asks for ElevenLabs but the ELEVENLABS_API_KEY secret is not set")
                    run([sys.executable, "-I", "-u", "tools/make_vo_eleven.py", "series/" + L["lines"].format(kit=kit), vo,
                         "--voice", str(eng["voice"]), "--model", eng.get("model", "eleven_multilingual_v2")]
                        + (["--only", fix] if have and fix else []), log, env)
                elif lang == "ar":
                    run([sys.executable, "-I", "-u", "tools/make_vo_namaa.py", f"series/{kit}_lines_ar_sa.txt", vo,
                         "--asr", "--seed", "301", "--max-rate", "14.5"] + (["--only", fix] if have and fix else []), log, env)
                else:
                    run([sys.executable, "-I", "-u", "tools/make_vo.py", f"series/{kit}_lines.txt", vo, "--verify"], log, env)
                for f in glob.glob(os.path.join(KIT, vo + ".json")) + glob.glob(os.path.join(KIT, vo + ".wav")):
                    shutil.copy(f, os.path.join(dst, "voice"))
                if os.path.isdir(os.path.join(KIT, vo + "_lines")):
                    shutil.copytree(os.path.join(KIT, vo + "_lines"), os.path.join(dst, "voice", os.path.basename(vo) + "_lines"),
                                    dirs_exist_ok=True)
            lines_dir = os.path.join(KIT, vo + "_lines")
            if os.path.isdir(lines_dir):
                rep["lines"] = []
                for f in sorted(glob.glob(os.path.join(lines_dir, "L*.json"))):
                    d = json.load(open(f, encoding="utf-8"))
                    rep["lines"].append({"line": os.path.basename(f)[1:3], "text": d.get("text"), "heard": d.get("whisper"),
                                         "problems": d.get("problems"), "seed": d.get("seed")})
            outdir = os.path.join("out", L["out"].format(kit=kit))
            text = run([sys.executable, "-I", "-u", "make.py", f"episodes/{kit}.py", vo, outdir] + L["arg"], log, env)
            m = re.search(r"QA\s+duration ([\d.]+)s\s+loudness (-?[\d.]+) LUFS\s+true peak (-?[\d.]+) dBFS\s+(\S+) @ (\S+)", text)
            if not m:
                raise RuntimeError("no QA line in the render output")
            dur, lufs, peak = float(m.group(1)), float(m.group(2)), float(m.group(3))
            lo, hi = GATE[lang]
            rep.update(duration=dur, lufs=lufs, peak=peak, frame=m.group(4), fps=m.group(5))
            issues = []
            if not lo <= dur <= hi:
                issues.append(f"length {dur:.1f}s outside {lo}-{hi}")
            if not -15.0 <= lufs <= -13.0:
                issues.append(f"loudness {lufs}")
            if peak > -0.9:
                issues.append(f"peak {peak}")
            if m.group(4) != "1080x1920":
                issues.append(f"frame {m.group(4)}")
            bad = [x["line"] for x in rep.get("lines", []) if x.get("problems")]
            if bad:
                rep["voice_lines_flagged"] = bad
            rep["issues"] = issues
            final = glob.glob(os.path.join(KIT, outdir, "*_final.mp4"))[0]
            if lang == "en":                             # can the words still be understood under the sound effects?
                try:
                    mixlog = []
                    mt = run([sys.executable, "-I", "-u", "tools/verify_mix.py", vo, outdir], mixlog, env)
                    mm = re.search(r"overall word error rate: (\d+)/(\d+)", mt)
                    if mm:
                        rep["mix_word_errors"] = f"{mm.group(1)}/{mm.group(2)}"
                    rep["mix_lines_off"] = [l.strip()[:160] for l in mt.splitlines() if re.match(r"^L\s*\d+\s+\d+ diff", l)]
                except Exception as e:  # noqa: BLE001
                    rep["mix_check"] = "not run: " + str(e)[:120]
            rep["size_mb"] = round(os.path.getsize(final) / 1e6, 1)
            shutil.copy(os.path.join(KIT, outdir, "qa_sheet.png"), os.path.join(dst, "review", f"qa_{lang}.png"))
            if not issues:
                shutil.copy(final, os.path.join(dst, "media", f"{slug}-{lang}.mp4"))
                rep["ok"] = True
            else:
                shutil.copy(final, os.path.join(dst, "review", f"REJECTED-{slug}-{lang}.mp4"))
                failed = True
        except Exception as e:  # noqa: BLE001
            rep["error"] = str(e)[:400]
            failed = True
        with open(os.path.join(dst, "review", f"log_{lang}.txt"), "w", encoding="utf-8") as f:
            f.write("".join(l for l in log if "Fontconfig" not in l)[-60000:])
    with open(os.path.join(dst, "review", "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if failed:
        sys.exit(1)


def collect():
    n = 0
    for d in sorted(glob.glob(os.path.join(OUT, "out-*"))):
        slug = os.path.basename(d)[4:]
        for f in glob.glob(os.path.join(d, "media", "*.mp4")):
            os.makedirs(os.path.join(ROOT, "media"), exist_ok=True)
            shutil.copy(f, os.path.join(ROOT, "media"))
            n += 1
        if os.path.isdir(os.path.join(d, "review")):
            rv = os.path.join(ROOT, "review", slug)
            os.makedirs(rv, exist_ok=True)
            for f in glob.glob(os.path.join(d, "review", "*")):
                if f.endswith(".mp4"):
                    continue                      # rejected videos stay in the run's artifact, not in the repo
                if os.path.basename(f) == "report.json" and os.path.exists(os.path.join(rv, "report.json")):
                    old = json.load(open(os.path.join(rv, "report.json"), encoding="utf-8"))
                    new = json.load(open(f, encoding="utf-8"))
                    old.setdefault("langs", {}).update(new.get("langs", {}))
                    json.dump(old, open(os.path.join(rv, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                else:
                    shutil.copy(f, rv)
        if os.path.isdir(os.path.join(d, "voice")):
            shutil.copytree(os.path.join(d, "voice"), os.path.join(KIT, "series", "voice"), dirs_exist_ok=True)
    print(f"{n} videos collected")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("plan")
    p1.add_argument("--only", default="")
    p1.add_argument("--langs", default="en,ar")
    p1.add_argument("--force", action="store_true")
    p2 = sub.add_parser("make")
    p2.add_argument("slug")
    p2.add_argument("kit")
    p2.add_argument("langs")
    p2.add_argument("look", nargs="?", default="1")
    sub.add_parser("collect")
    a = ap.parse_args()
    if a.cmd == "plan":
        plan(a)
    elif a.cmd == "make":
        make(a.slug, a.kit, a.langs, a.look)
    else:
        collect()
