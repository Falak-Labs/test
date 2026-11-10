"""Arabic voiceover from Microsoft's neural voices (Azure Speech), made on the user's PC with ms_voices.py.

usage:
  python3 -I tools/make_vo_ms.py <elevator_ar_ms.zip | folder> <out_prefix> [--gap 0.3] [--tempo 1.0]

The zip holds L01.wav ... L14.wav (24 kHz mono), L01.json ... (the line text and Azure's word boundaries:
text, start, duration) and meta.json (voice, rate, script "sa" = Saudi, "ps" = Palestinian, "sy" = Syrian).
Outputs, same as the other voice tools: <out>.wav / .json (line and exact word timings) / .mp3, <out>_raw.*.
Render with lang=ar_sa (Saudi), lang=ar (Palestinian) or lang=ar_sy (Syrian); the tool prints the command.
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import tempfile
import zipfile

import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--gap", type=float, default=0.3)
ap.add_argument("--tempo", type=float, default=1.0)
a = ap.parse_args()

SR = 24000
TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟـ]")


def norm(w):
    w = TASHKEEL.sub("", w)
    w = re.sub("[إأآٱ]", "ا", w).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"[^ء-ي0-9a-zA-Z]", "", w)


src = a.src
if src.endswith(".zip"):  # unpack into a new empty folder; the files are only read as data
    tmp = tempfile.mkdtemp(prefix="ms_vo_")
    with zipfile.ZipFile(src) as z:
        for m in z.namelist():
            if m.endswith("/") or ".." in m.split("/") or m.startswith("/"):
                continue
            z.extract(m, tmp)
    src = tmp
found = {}
for root, _, files in os.walk(src):
    for f in files:
        found.setdefault(f, os.path.join(root, f))
meta = json.load(open(found["meta.json"], encoding="utf-8")) if "meta.json" in found else {}
names = sorted(f for f in found if re.fullmatch(r"L\d\d\.json", f))
if not names:
    raise SystemExit(f"no L01.json ... in {a.src}")


def edge_trim(x):
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x, 0.0
    db = 20 * np.log10(np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12) + 1e-12)
    voiced = np.where(db > max(db.max() - 42, -60))[0]
    if len(voiced) == 0:
        return x, 0.0
    i0, i1 = max(voiced[0] - 3, 0), min(voiced[-1] + 4, n)
    return x[i0 * win: i1 * win], i0 * win / SR


def match(display, bounds, d):
    """Exact Azure word times onto the caption words; anything unmatched is spread over its gap."""
    dn, bn = [norm(w) for w in display], [norm(b["text"]) for b in bounds]
    spans = [None] * len(display)
    if len(dn) == len(bn):
        pairs = list(zip(range(len(dn)), range(len(bn))))
    else:
        pairs = []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=dn, b=bn, autojunk=False).get_opcodes():
            if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
                pairs += list(zip(range(i1, i2), range(j1, j2)))
    for i, j in pairs:
        b = bounds[j]
        spans[i] = (b["start"], b["start"] + max(b.get("dur", 0.0), 0.06))
    i = 0
    while i < len(spans):
        if spans[i] is not None:
            i += 1
            continue
        k = i
        while k < len(spans) and spans[k] is None:
            k += 1
        t0 = spans[i - 1][1] if i else 0.0
        t1 = spans[k][0] if k < len(spans) else d
        step = max(t1 - t0, 0.06 * (k - i)) / (k - i)
        for q in range(i, k):
            spans[q] = (t0 + (q - i) * step, t0 + (q - i + 1) * step)
        i = k
    return spans, len(pairs)


pieces, timing, t, report = [], [], 0.0, []
for n, name in enumerate(names, 1):
    js = json.load(open(found[name], encoding="utf-8"))
    x, sr = sf.read(found[name[:-5] + ".wav"], dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        from scipy.signal import resample_poly
        x = resample_poly(x, SR, sr).astype(np.float32)
    y, cut = edge_trim(x)
    d = len(y) / SR
    shown = TASHKEEL.sub("", js["text"])
    display = shown.split()
    bounds = [dict(b, start=b["start"] - cut) for b in js.get("words", [])]
    spans, hit = match(display, bounds, d)
    timing.append({"line": n, "start": round(t, 3), "end": round(t + d, 3), "text": shown,
                   "words": [{"w": w, "start": round(t + min(max(s0, 0.0), d), 3), "end": round(t + min(max(s1, 0.0), d), 3)}
                             for w, (s0, s1) in zip(display, spans)]})
    report.append(f"  L{n:>2} {d:5.2f}s  {hit}/{len(display)} words timed by Azure")
    pieces.append(y)
    t += d
    if n < len(names):
        pieces.append(np.zeros(int(a.gap * SR), np.float32))
        t += a.gap

voice = "Microsoft " + meta.get("voice", "?") + (f" rate {meta['rate']}" if meta.get("rate") not in (None, "+0%") else "")
raw = a.out + "_raw"
full = np.concatenate(pieces)
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
sf.write(raw + ".wav", full, SR)
n_words = sum(len(e["text"].split()) for e in timing)
json.dump({"voice": voice, "duration": round(len(full) / SR, 2), "words": n_words, "lines": timing},
          open(raw + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if abs(a.tempo - 1.0) > 1e-6:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", raw + ".wav",
                    "-af", f"atempo={a.tempo}", a.out + ".wav"], check=True)
    for ln in timing:
        ln["start"], ln["end"] = round(ln["start"] / a.tempo, 3), round(ln["end"] / a.tempo, 3)
        for w in ln["words"]:
            w["start"], w["end"] = round(w["start"] / a.tempo, 3), round(w["end"] / a.tempo, 3)
else:
    sf.write(a.out + ".wav", full, SR)
dur = sf.info(a.out + ".wav").duration
script = meta.get("script", "sa")
json.dump({"voice": voice, "script": script, "tempo": a.tempo, "gap": a.gap, "duration": round(dur, 2),
           "words": n_words, "words_per_sec": round(n_words / dur, 2), "lines": timing},
          open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.out + ".wav",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k",
                a.out + ".mp3"], check=True)
print("\n".join(report))
lang = {"sa": "ar_sa", "ps": "ar", "sy": "ar_sy"}.get(script, "ar")
print(f"{voice}: {len(timing)} lines, {n_words} words, {dur:.2f}s ({n_words / dur:.2f} words/s) -> {a.out}.wav")
print(f"render: python3 make.py episodes/elevator.py {a.out} out/elevator_ms lang={lang}")
