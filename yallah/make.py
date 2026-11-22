#!/usr/bin/env python3
"""Yallah Say: make one Short for one dialect, start to finish, from what is in the repo.

usage: python3 yallah/make.py <lesson> <ma|pa> <out_dir> [--workers N] [--hear] [clip=take ...]

  lesson      the lesson number as kit/tools/gen2.py knows it ("01")
  out_dir     everything lands here: page/ (what was drawn), vid/ (picture pieces), final.wav, the MP4,
              sheet.jpg (frames to look at) and report.json
  --workers   how many pieces of picture are rendered at the same time (default: one per CPU)
  --hear      also transcribe every line of the finished file with Whisper (YS_WHISPER = the model folder)
  clip=take   use another take for a clip, as in build2.py (v1=v1b)

Steps: script (gen2.py) -> its lines must be the ones the voices were recorded from -> page folder (mkpage.py) ->
sound track and timeline (build2.py) -> picture in pieces (shoot.py) -> join -> add the sound -> checks.
It spends nothing: the voices are the takes already in darija/voice/<dialect><lesson>/.
The exit code is 0 only when every check passed; report.json says what was made and what failed."""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(HERE, "kit", "tools")
PER, FPS = 520, 30          # frames in one piece of picture; the pieces are joined without encoding again

args = sys.argv[1:]
flags = [a for a in args if a.startswith("--")]
alts = [a for a in args if "=" in a and not a.startswith("--")]
pos = [a for a in args if a not in flags and a not in alts]
workers = os.cpu_count() or 2
if "--workers" in args:
    workers = int(args[args.index("--workers") + 1])
    pos.remove(args[args.index("--workers") + 1])
if len(pos) != 3 or pos[1] not in ("ma", "pa") or not re.fullmatch(r"[0-9A-Za-z_-]+", pos[0]):
    sys.exit(__doc__)
LESSON, LOC, OUT = pos[0], pos[1], os.path.abspath(pos[2])
SLUG = f"{LOC}{LESSON}"
PAGE, VID = os.path.join(OUT, "page"), os.path.join(OUT, "vid")
VOICE = os.path.join(ROOT, "darija", "voice", SLUG)
NAME = f"yallah-say-{LOC}-ep{LESSON}.mp4"
REPORT = {"lesson": LESSON, "dialect": LOC, "file": NAME, "ok": False, "problems": [], "steps": {}}
T0 = time.monotonic()


def finish(code):
    REPORT["seconds"] = round(time.monotonic() - T0, 1)
    REPORT["ok"] = code == 0 and not REPORT["problems"]
    os.makedirs(OUT, exist_ok=True)
    json.dump(REPORT, open(os.path.join(OUT, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(("DONE " if REPORT["ok"] else "FAILED ") + json.dumps({k: REPORT[k] for k in ("file", "ok", "problems", "seconds")}, ensure_ascii=False), flush=True)
    sys.exit(0 if REPORT["ok"] else 1)


def run(step, cmd, env=None, keep=6):
    """Run one tool, keep the end of what it printed in the report, stop everything if it fails."""
    t = time.monotonic()
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    tail = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()][-keep:]
    REPORT["steps"][step] = {"seconds": round(time.monotonic() - t, 1), "says": tail}
    print(f"[{step}] {time.monotonic() - t:.1f}s " + (" | ".join(tail[-2:]) if tail else ""), flush=True)
    if r.returncode != 0:
        REPORT["problems"].append(f"{step} failed: " + " | ".join(tail[-3:]))
        finish(1)
    return r.stdout


def probe(path, what):
    r = subprocess.run(["ffprobe", "-v", "error", *what, "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()[0][:80]
    except Exception:      # a missing tool shows up where it is used
        return "?"


os.makedirs(PAGE, exist_ok=True)
os.makedirs(VID, exist_ok=True)

# 1. the script, and the lines the voices must have been recorded from
run("script", [sys.executable, os.path.join(TOOLS, "gen2.py"), LESSON, LOC, PAGE, os.path.join(OUT, "lines.txt")])
body = lambda p: [l.strip() for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]
recorded = os.path.join(ROOT, "darija", "lines", SLUG + ".txt")
if not os.path.exists(recorded):
    REPORT["problems"].append(f"no recorded script darija/lines/{SLUG}.txt: record the voices first")
    finish(1)
if body(recorded) != body(os.path.join(OUT, "lines.txt")):
    REPORT["problems"].append(f"the script changed after darija/lines/{SLUG}.txt was recorded: record the changed lines first")
    finish(1)
missing = [l.split("|")[1].strip() for l in body(recorded) if not os.path.exists(os.path.join(VOICE, l.split("|")[1].strip() + ".mp3"))]
if missing:
    REPORT["problems"].append(f"{len(missing)} voice takes are missing in darija/voice/{SLUG}: " + ", ".join(missing[:8]))
    finish(1)

# 2. the page folder, 3. the sound track and the timeline
run("page", [sys.executable, os.path.join(TOOLS, "mkpage.py"), LOC, PAGE])
run("sound", [sys.executable, os.path.join(TOOLS, "build2.py"), VOICE, PAGE, OUT, *alts])
tl = open(os.path.join(PAGE, "tl.js"), encoding="utf-8").read()
NF, DUR = int(re.search(r'"nf":(\d+)', tl).group(1)), float(re.search(r'"dur":([0-9.]+)', tl).group(1))
REPORT.update(frames=NF, duration=DUR, sha256={})
for f in ("page/script.js", "page/tl.js", "final.wav"):
    REPORT["sha256"][f] = hashlib.sha256(open(os.path.join(OUT, f), "rb").read()).hexdigest()

# 4. the picture, in pieces, several at a time (a piece is only kept when ffmpeg ended well and every frame is there)
pieces = [(i, a, min(PER, NF - a)) for i, a in enumerate(range(0, NF, PER))]


def piece(job):
    i, a, n = job
    out = os.path.join(VID, f"p{i:02d}.mp4")
    for attempt in (1, 2):
        if os.path.exists(out):
            os.remove(out)
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "shoot.py"), "video", PAGE, out, repr(a / FPS), repr(n / FPS)], capture_output=True, text=True)
        got = int(probe(out, ["-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames"]).get("streams", [{}])[0].get("nb_read_frames", 0)) if os.path.exists(out) else 0
        if r.returncode == 0 and got == n:
            return i, True, (r.stdout.strip().splitlines() or [""])[-1]
        last = f"piece {i}: {got} of {n} frames; " + (r.stdout + r.stderr).strip()[-300:]
    return i, False, last


t = time.monotonic()
with cf.ThreadPoolExecutor(max(1, workers)) as ex:
    done = list(ex.map(piece, pieces))
sec = time.monotonic() - t
REPORT["steps"]["picture"] = {"seconds": round(sec, 1), "pieces": len(pieces), "at_once": workers, "frames_per_second": round(NF / sec, 1)}
print(f"[picture] {NF} frames in {sec:.0f}s ({NF / sec:.1f} a second, {workers} at once)", flush=True)
for i, ok, msg in done:
    if not ok:
        REPORT["problems"].append("picture " + msg)
if REPORT["problems"]:
    finish(1)

# 5. join the pieces, 6. add the sound (the picture is copied, never encoded twice)
with open(os.path.join(OUT, "list.txt"), "w") as f:
    f.write("".join(f"file 'vid/p{i:02d}.mp4'\n" for i, _, _ in pieces))
run("join", ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt"), "-c", "copy", os.path.join(OUT, "join.tmp.mp4")])
part, final = os.path.join(OUT, NAME.replace(".mp4", ".part.mp4")), os.path.join(OUT, NAME)
run("mux", ["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "join.tmp.mp4"), "-i", os.path.join(OUT, "final.wav"), "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", part])
os.replace(part, final)
os.remove(os.path.join(OUT, "join.tmp.mp4"))

# 7. checks on the finished file
p = probe(final, ["-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels:format=duration,size"])
v = next((s for s in p.get("streams", []) if s.get("codec_name") == "h264"), {})
a = next((s for s in p.get("streams", []) if s.get("codec_name") == "aac"), {})
REPORT["video"] = {"size": int(p.get("format", {}).get("size", 0)), "frames": int(v.get("nb_frames", 0)), "width": v.get("width"), "height": v.get("height"),
                   "rate": v.get("r_frame_rate"), "audio_seconds": round(float(a.get("duration", 0)), 3), "audio_rate": a.get("sample_rate")}
REPORT["sha256"][NAME] = hashlib.sha256(open(final, "rb").read()).hexdigest()
if REPORT["video"]["frames"] != NF or (v.get("width"), v.get("height")) != (1080, 1920) or v.get("r_frame_rate") != "30/1":
    REPORT["problems"].append(f"picture is not {NF} frames of 1080x1920 at 30 a second: {REPORT['video']}")
if not a or abs(float(a.get("duration", 0)) - DUR) > 0.08:
    REPORT["problems"].append(f"sound is {a.get('duration')} s, the lesson is {DUR} s")
if not 60 <= DUR <= 175:
    REPORT["problems"].append(f"{DUR:.0f} s: a Short that can earn runs over 1 minute and stays under 3")
out = run("takes", [sys.executable, os.path.join(TOOLS, "corrcheck2.py"), final, PAGE, *alts], env={"VO": VOICE}, keep=3)
low = re.search(r"below 0\.9: (.*)", out)
REPORT["takes_below_0.9"] = low.group(1).strip() if low else "?"
if not low or low.group(1).strip() != "none":
    REPORT["problems"].append("a voice take is not intact in the finished file: " + (low.group(1).strip() if low else "no answer"))
if "--hear" in flags:
    if not os.path.isdir(os.environ.get("YS_WHISPER", "")):
        REPORT["problems"].append("--hear needs YS_WHISPER, the Whisper model folder")
    else:
        out = run("hear", [sys.executable, os.path.join(TOOLS, "check_final2.py"), final, PAGE], keep=2)
        look = [l for l in out.splitlines() if l.startswith("LOOK")]
        REPORT["heard_wrong"] = look
        if look:
            REPORT["problems"].append(f"{len(look)} lines were not heard as written: " + "; ".join(l[:90] for l in look[:4]))

# 8. frames to look at: one from every shot, a little after it starts, and the last second
try:
    from PIL import Image
    shots = json.loads(re.search(r'"shots":(\[.*?\]),\s*\n', tl, re.S).group(1))
    times = sorted({round(min(DUR - 0.2, s["a"] + min(1.6, (s["b"] - s["a"]) * 0.6)), 2) for s in shots} | {round(DUR - 0.5, 2)})[:16]
    run("frames", [sys.executable, os.path.join(TOOLS, "shoot.py"), "stills", PAGE, os.path.join(OUT, "fr"), *[str(x) for x in times]])
    ims = [Image.open(os.path.join(OUT, "fr", f)).convert("RGB") for f in sorted(os.listdir(os.path.join(OUT, "fr")))]
    cols, cw = 8, 270
    ch, rows = round(cw * 1920 / 1080), (len(ims) + 7) // 8
    sheet = Image.new("RGB", (cols * cw + (cols + 1) * 6, rows * ch + (rows + 1) * 6), (20, 20, 24))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((cw, ch), Image.LANCZOS), (6 + (i % cols) * (cw + 6), 6 + (i // cols) * (ch + 6)))
    sheet.save(os.path.join(OUT, "sheet.jpg"), quality=86)
    REPORT["sheet_times"] = times
except Exception as e:      # the sheet is for looking; the video does not depend on it
    REPORT["steps"]["frames"] = {"says": [f"no sheet: {type(e).__name__}: {str(e)[:120]}"]}

REPORT["made_with"] = {"python": sys.version.split()[0], "ffmpeg": version(["ffmpeg", "-version"]),
                       "playwright": version([sys.executable, "-m", "playwright", "--version"])}
finish(0)
