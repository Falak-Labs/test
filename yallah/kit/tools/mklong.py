"""Build a day's long YouTube video (16:9) from its three Shorts: each Short in full, centred on a blurred copy of
itself, then a review round made of each lesson's quiz shot ("R" in its tl.js). Same layout as Days 4-7.

usage: python3 mklong.py <ma|pa> <day> <lesson> <lesson> <lesson> <work_dir>
       e.g. python3 mklong.py ma 8 22 23 24 /tmp/long
The Shorts are read from <work_dir>/s_<d><NN>.mp4 (downloaded from the yallah-media branch if missing).
Writes <work_dir>/final_<d>_day<day>.mp4."""
import json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EPIS = os.path.join(HERE, "..", "..", "episodes")
d, day, *rest = sys.argv[1:]
lessons, W = rest[:-1], rest[-1]
os.makedirs(W, exist_ok=True)
VF = ("[0:v]split=2[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=40[bg];"
      "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,format=yuv420p[v]")
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2"]


def run(args, out):
    tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", VF, "-map", "[v]", "-map", "0:a", *ENC, tmp], check=True)
    os.replace(tmp, out)


def quiz(n):
    tl = open(os.path.join(EPIS, f"{d}{n}", "tl.js"), encoding="utf-8").read().split("=", 1)[1]
    tl = json.loads(tl[:tl.index('\n"fx"')].rstrip(",") + "}")
    r = [s for s in tl["shots"] if s["k"] == "R"][0]
    return r["a"], r["b"] - r["a"]


parts = []
for n in lessons:
    src = os.path.join(W, f"s_{d}{n}.mp4")
    if not os.path.exists(src):
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/Falak-Labs/test/yallah-media/yallah-say-{d}-ep{n}.mp4", src)
    run(["-i", src], os.path.join(W, f"m_{d}{n}.mp4"))
    parts.append(f"m_{d}{n}.mp4")
for n in lessons:
    a, dur = quiz(n)
    run(["-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", os.path.join(W, f"s_{d}{n}.mp4")], os.path.join(W, f"rv_{d}{n}.mp4"))
    parts.append(f"rv_{d}{n}.mp4")
lst = os.path.join(W, f"c_{d}{day}.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
out = os.path.join(W, f"final_{d}_day{day}.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out[:-4] + ".part.mp4"], check=True)
os.replace(out[:-4] + ".part.mp4", out)
print(out, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
