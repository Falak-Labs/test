#!/usr/bin/env python3
"""Seedance-only episode cutter, "cinema" style (no cartoon HUD).

usage: python3 tools/seedance_cut.py <shots.json> <voice_dir_base> <out_dir>
  shots.json: {"title": "TAIPEI 101", "kicker": "508 m · typhoon-proof",
               "shots": [{"line": 1, "src": "path.mp4", "at": 0.0}, ...],
               "numbers": [["six hundred sixty", "660"], ...]}
  One shot per narration line; a shot runs from its line's start to the next line's start.
Look: full-bleed footage with a slow push-in, soft vignette, thin gold progress bar,
big centered 1-3 word captions (Poppins Black, active word gold), small letter-spaced title.
"""
import json, os, re, subprocess, sys
import numpy as np, soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bik import sfx  # noqa: E402

W, H, FPS = 1080, 1920, 30
GOLD = "&H003CC9FF"  # ASS BGR: #FFC93C
TAIL = 1.4


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r


def probe_dur(p):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p])
    return float(r.stdout.strip())


def ass_time(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def chunks(words, numbers):
    """Merge spoken number words into numerals, then group into 1-3 word chunks."""
    words = [w for w in words if not (w["w"].startswith("[") or w["w"].endswith("]"))]   # never caption [audio tags]
    toks = []
    i = 0
    low = [re.sub(r"[^a-z0-9']", "", w["w"].lower()) for w in words]
    while i < len(words):
        hit = None
        for phrase, shown in numbers:
            p = phrase.split()
            if low[i:i + len(p)] == p:
                hit = (len(p), shown)
                break
        if hit:
            n, shown = hit
            toks.append({"w": shown, "start": words[i]["start"], "end": words[i + n - 1]["end"], "big": True})
            i += n
        else:
            toks.append(dict(words[i]))
            i += 1
    out, cur = [], []
    for t in toks:
        cur.append(t)
        end_punct = re.search(r"[.,:?!،؟]$", t["w"])
        if t.get("big") or len(cur) == 3 or end_punct or len("".join(x["w"] for x in cur)) > 14:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def pick(v, lang):
    return v.get(lang, v.get("en", "")) if isinstance(v, dict) else v


def build_ass(lines, numbers, title, kicker, total, path, lang="en", cover=None):
    ar = lang != "en"
    capfont, bigfont, tfont, kfont = (("Tajawal Black",) * 2 + ("Tajawal ExtraBold",) * 2) if ar else \
        ("Poppins Black", "Poppins Black", "Poppins Bold", "Poppins SemiBold")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{capfont},{126 if ar else 104},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,5,6,5,60,60,0,1
Style: Big,{bigfont},190,{GOLD},&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,8,5,60,60,0,1
Style: Title,{tfont},{54 if ar else 46},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,{0 if ar else 14},0,1,0,3,8,60,60,150,1
Style: Kick,{kfont},{38 if ar else 34},{GOLD},&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,{0 if ar else 6},0,1,0,3,8,60,60,214,1
Style: CovS,{tfont},{64 if ar else 58},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,4,6,5,60,60,0,1
Style: CovB,{bigfont},{150 if ar else 140},{GOLD},&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,8,5,60,60,0,1
Style: Badge,{kfont},44,&H00111111,&H00FFFFFF,&H003CC9FF,&H003CC9FF,0,0,0,0,100,100,{0 if ar else 4},0,3,14,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    if cover:
        e0 = ass_time(0.0); e1 = ass_time(0.12)
        ev.append(f"Dialogue: 3,{e0},{e1},Badge,,0,0,0,,{{\\pos({W // 2},{int(H * 0.16)})}}{cover['badge']}")
        ev.append(f"Dialogue: 3,{e0},{e1},CovS,,0,0,0,,{{\\pos({W // 2},{int(H * 0.66)})}}{cover['top']}")
        ev.append(f"Dialogue: 3,{e0},{e1},CovB,,0,0,0,,{{\\pos({W // 2},{int(H * 0.74)})\\q0}}{cover['name']}")
    # title: in for the hook, back for the closer
    for a, b in [(0.1, 3.6), (lines[-2]["start"] - 0.1, lines[-2]["end"] + 0.2)]:
        ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Title,,0,0,0,,{{\\fad(250,250)}}{title}")
        ev.append(f"Dialogue: 0,{ass_time(a + 0.15)},{ass_time(b)},Kick,,0,0,0,,{{\\fad(250,250)}}{kicker}")
    cy = int(H * 0.74)
    for li, ln in enumerate(lines):
        groups = chunks(ln["words"], numbers)
        for gi, g in enumerate(groups):
            g_start = max(g[0]["start"], 0.13 if cover else 0)
            nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else ln["end"] + 0.25
            if g[0].get("big"):
                txt = g[0]["w"]
                ev.append(f"Dialogue: 1,{ass_time(g_start)},{ass_time(nxt)},Big,,0,0,0,,"
                          f"{{\\pos({W // 2},{cy - 40})\\fscx70\\fscy70\\t(0,140,\\fscx100\\fscy100)}}{txt}")
                continue
            for k, w in enumerate(g):
                a = max(w["start"], 0.13 if cover else 0)
                b = g[k + 1]["start"] if k + 1 < len(g) else nxt
                parts = []
                for j, x in enumerate(g):
                    word = x["w"].rstrip(",.:؟،") if ar else x["w"].upper().rstrip(",.:")
                    parts.append(("{\\c" + GOLD + "}" + word + "{\\c&H00FFFFFF&}") if j == k else word)
                pop = "\\fscx86\\fscy86\\t(0,110,\\fscx100\\fscy100)" if k == 0 else ""
                if ar:          # libass lays colour-split runs left to right: put the words in visual order
                    parts = parts[::-1]
                ev.append(f"Dialogue: 1,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,"
                          f"{{\\pos({W // 2},{cy}){pop}}}" + " ".join(parts))
    open(path, "w").write(head + "\n".join(ev) + "\n")


def cut_shot(src, at, dur, out, push=0.07, shake=False):
    still = src.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    sd = dur + 1 if still else probe_dur(src)
    avail = max(0.5, sd - at)
    k = max(1.0, dur / avail * 1.01)  # slow a little if the shot is short
    n = int(round(dur * FPS))
    z = f"1+{push}*on/{n}"
    xs = "+12*sin(on*2.1)*max(0,1-on/12)" if shake else ""
    vf = (f"trim=start={at},setpts=(PTS-STARTPTS)*{k:.4f},fps={FPS},scale=2160:3840:flags=lanczos,"
          f"zoompan=z='{z}':x='iw/2-iw/zoom/2{xs}':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS},"
          f"eq=contrast=1.06:saturation=1.08,vignette=PI/5,trim=end_frame={n},setsar=1,format=yuv420p")
    tmp = out + ".part.mp4"
    if still:
        vf = vf.replace(f"trim=start={at},setpts=(PTS-STARTPTS)*{k:.4f},", "")
        vf = vf.replace("scale=2160:3840:flags=lanczos", "scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840")
    inp = ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 0.2:.3f}", "-i", src] if still else ["-i", src]
    run(["ffmpeg", "-y", "-v", "error", *inp, "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "18", "-r", str(FPS), tmp])
    os.replace(tmp, out)


def bed(total, sr=48000):
    rng = np.random.default_rng(3)
    n = int(total * sr)
    x = np.cumsum(rng.standard_normal(n)) / 400.0
    x -= np.convolve(x, np.ones(4801) / 4801, mode="same")  # brown-ish rain/wind
    x = x / (np.abs(x).max() + 1e-9) * 0.5
    t = np.arange(n) / sr
    drone = 0.25 * np.sin(2 * np.pi * 55 * t) + 0.12 * np.sin(2 * np.pi * 82.4 * t)
    y = 0.08 * x + 0.05 * drone
    fade = np.minimum(1, np.minimum(t / 1.0, (total - t) / 1.5))
    return (y * fade).astype(np.float32)


def place(buf, clip, t, gain_db, sr):
    clip = np.asarray(clip, dtype=np.float32)
    if clip.ndim > 1:
        clip = clip.mean(axis=1)
    i = int(t * sr)
    j = min(len(buf), i + len(clip))
    if i < len(buf):
        buf[i:j] += clip[: j - i] * (10 ** (gain_db / 20))


def main():
    spec_p, vbase, outd = sys.argv[1:4]
    lang = sys.argv[4] if len(sys.argv) > 4 else "en"
    spec = json.load(open(spec_p))
    vj = json.load(open(vbase + ".json"))
    lines = vj["lines"]
    os.makedirs(outd, exist_ok=True)
    total = lines[-1]["end"] + TAIL
    shots = {s["line"]: s for s in spec["shots"]}
    seg_files = []
    starts = [0.0] + [l["start"] for l in lines[1:]]
    ends = starts[1:] + [total]
    for i, ln in enumerate(lines):
        s = shots[ln["line"]]
        dur = ends[i] - starts[i]
        f = os.path.join(outd, f"seg{i + 1:02d}.mp4")
        if not os.path.exists(f) or os.environ.get("REDO"):
            cut_shot(s["src"], s.get("at", 0.0), dur, f, push=s.get("push", 0.07),
                     shake=ln["text"].startswith("But"))
        seg_files.append(f)
        print("seg", i + 1, round(dur, 2), s["src"].split("/")[-1], s.get("at", 0))
    lst = os.path.join(outd, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in seg_files))
    joined = os.path.join(outd, "joined.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

    # audio: voice + bed + cut sounds
    sr = 48000
    v, vsr = sf.read(vbase + ".wav", dtype="float32")
    if v.ndim > 1:
        v = v.mean(axis=1)
    if vsr != sr:
        idx = np.arange(int(len(v) * sr / vsr)) * vsr / sr
        v = np.interp(idx, np.arange(len(v)), v).astype(np.float32)
    buf = np.zeros(int(total * sr) + sr, dtype=np.float32)
    place(buf, v, 0.0, 0, sr)
    b = bed(total, sr)
    buf[: len(b)] += b
    ssr = getattr(sfx, "SR", 48000)
    for i, ln in enumerate(lines[1:], 1):
        if ln["text"].startswith("But"):
            place(buf, sfx.thud(), ln["start"] - 0.02, -6, ssr if ssr == sr else sr)
        elif ln["text"].startswith("So"):
            place(buf, sfx.whoosh(), ln["start"] - 0.25, -9, sr)
    mix = os.path.join(outd, "mix.wav")
    sf.write(mix, buf[: int(total * sr)], sr)

    ass = os.path.join(outd, "caps.ass")
    cov = None
    if spec.get("build_no"):
        cov = {"badge": ("  البناء رقم " + str(spec['build_no']).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")) + "  " if lang != "en" else f"  BUILD #{spec['build_no']}  "),
               "top": ("مبروك، كذا بنيت" if lang != "en" else "CONGRATS, YOU JUST BUILT"),
               "name": pick(spec.get("cover_name", spec["title"]), lang)}
    build_ass(lines, spec.get("numbers", []) if lang == "en" else spec.get("numbers_ar", []), pick(spec["title"], lang),
              pick(spec["kicker"], lang), total, ass, lang, cov)
    fonts = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts"))
    final = os.path.join(outd, spec.get("name", "episode") + f"_{lang}_final.mp4")
    tmp = final + ".part.mp4"
    fc = (f"[0:v]ass={ass}:fontsdir={fonts}[c];"
          f"color=c=0xFFC93C:s={W}x10:r={FPS}[bar];"
          f"[c][bar]overlay=x='-w+w*t/{total:.3f}':y=0:shortest=1[v];"
          f"[1:a]loudnorm=I=-13.2:TP=-1.5:LRA=11[a]")
    run(["ffmpeg", "-y", "-v", "error", "-i", joined, "-i", mix, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-ar", "48000", "-t", f"{total:.3f}", "-movflags", "+faststart", tmp])
    os.replace(tmp, final)
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-frames:v", "1", os.path.join(outd, "cover.png")])
    ts = [0.6] + [l["start"] + 0.8 for l in lines[1:]]
    for i, t in enumerate(ts):
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-vf", "scale=270:-1",
             os.path.join(outd, f"_q{i:02d}.png")])
    qs = [os.path.join(outd, f"_q{i:02d}.png") for i in range(len(ts))]
    rows = [qs[i:i + 7] for i in range(0, len(qs), 7)]
    rows[-1] += [qs[-1]] * (7 - len(rows[-1]))
    ins = sum((["-i", q] for r in rows for q in r), [])
    fc2 = ";".join(f"{''.join(f'[{r * 7 + c}]' for c in range(7))}hstack=7[r{r}]" for r in range(len(rows)))
    fc2 += ";" + "".join(f"[r{r}]" for r in range(len(rows))) + f"vstack={len(rows)}" if len(rows) > 1 else ""
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc2, os.path.join(outd, "qa_sheet.png")])
    for q in qs:
        os.remove(q)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", final, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
    d = probe_dur(final)
    print(f"QA  duration {d:.1f}s  loudness {lufs} LUFS  true peak {peak} dBFS  {W}x{H} @ {FPS}")
    print("done", final, round(total, 2))


if __name__ == "__main__":
    main()
