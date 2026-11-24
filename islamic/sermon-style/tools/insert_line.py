"""Insert a separately recorded line (a patch take from vo_take.py --lines-only) into a whole-script take.

  python3 tools/insert_line.py base.wav base.json patch.wav patch.json --after 7 out.wav out.json

The take is cut in the quietest moment between line N and N+1, the patch (trimmed to its words, levelled to the
take's speech loudness) goes in between, and every later time is shifted. The json keeps vo_take's line format,
so assemble.py and build_episode.py work on the result as on any take.
"""
import argparse, json, re
import numpy as np, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("base_wav"); ap.add_argument("base_json"); ap.add_argument("patch_wav"); ap.add_argument("patch_json")
ap.add_argument("--after", type=int, required=True, help="insert after this line (1-based)")
ap.add_argument("out_wav"); ap.add_argument("out_json")
ap.add_argument("--pad", type=float, default=0.35, help="silence on each side of the patch")
a = ap.parse_args()

y, sr = sf.read(a.base_wav); p, sr2 = sf.read(a.patch_wav)
assert sr == sr2
if y.ndim > 1: y = y.mean(1)
if p.ndim > 1: p = p.mean(1)
base = json.load(open(a.base_json, encoding="utf-8"))
pj = json.load(open(a.patch_json, encoding="utf-8"))
L = base["lines"]

# words of the patch from its character alignment, audio tags left out
text = "".join(pj["chars"])
words, cur, in_tag = [], None, False
for ch, s, e in zip(pj["chars"], pj["starts"], pj["ends"]):
    if ch == "[": in_tag = True; continue
    if ch == "]": in_tag = False; continue
    if in_tag: continue
    if ch.isspace():
        if cur and re.search(r"\w", cur["w"]): words.append(cur)
        cur = None; continue
    if cur is None: cur = {"w": ch, "start": s, "end": e}
    else:
        cur["w"] += ch
        if re.match(r"\w", ch): cur["end"] = e
if cur and re.search(r"\w", cur["w"]): words.append(cur)
t0, t1 = max(0.0, words[0]["start"] - 0.06), min(len(p) / sr, words[-1]["end"] + 0.25)
seg = p[int(t0 * sr):int(t1 * sr)].copy()
f = int(0.01 * sr); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)


def speech_rms(x):
    h = int(0.02 * sr); fr = x[:len(x) // h * h].reshape(-1, h)
    r = np.sqrt((fr ** 2).mean(1)); return float(np.sqrt(np.mean(r[r > 0.25 * r.max()] ** 2)))


seg *= speech_rms(y) / speech_rms(seg)

# quietest 30 ms between the two lines
e, s = L[a.after - 1]["end"], L[a.after]["start"]
lo, hi = max(0.0, min(e, s) - 0.1), max(e, s) + 0.1
z = y[int(lo * sr):int(hi * sr)]; win, hop = int(0.03 * sr), int(0.005 * sr)
k = min(range(0, max(1, len(z) - win), hop), key=lambda k: float(np.sum(z[k:k + win] ** 2)))
c = lo + (k + win / 2) / sr
pad = np.zeros(int(a.pad * sr))
ins_start = c + a.pad
shift = 2 * a.pad + len(seg) / sr
out = np.concatenate([y[:int(c * sr)], pad, seg, pad, y[int(c * sr):]])
sf.write(a.out_wav, out, sr, subtype="PCM_16")

off = ins_start - t0
new_line = {"text": re.sub(r"\[[^\]]*\]", "", pj["text"]).strip(),
            "start": round(words[0]["start"] + off, 3), "end": round(words[-1]["end"] + off, 3),
            "words": [{"w": w["w"], "start": round(w["start"] + off, 3), "end": round(w["end"] + off, 3)} for w in words]}
lines = []
for i, ln in enumerate(L):
    if i >= a.after:
        ln = dict(ln, start=round(ln["start"] + shift, 3), end=round(ln["end"] + shift, 3),
                  words=[dict(w, start=round(w["start"] + shift, 3), end=round(w["end"] + shift, 3)) for w in ln["words"]])
    lines.append(ln)
    if i == a.after - 1:
        lines.append(new_line)
meta = dict(base, lines=lines, inserted={"after": a.after, "patch": a.patch_json})
json.dump(meta, open(a.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"inserted {len(seg) / sr:.2f}s after line {a.after}: {new_line['text']} -> {len(out) / sr:.2f}s, {len(lines)} lines")
