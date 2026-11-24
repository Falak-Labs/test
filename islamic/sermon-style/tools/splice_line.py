"""Replace one line of a voice take with a single-line patch take (when a word was misread).
usage: splice_line.py take.wav take.json patch.wav patch.json line_no out.wav out.json
The cut points sit in the pauses either side of the line; timings after the line shift by the length difference.
"""
import json, re, sys
import numpy as np
import soundfile as sf

tw, tj, pw, pj, n, ow, oj = sys.argv[1:8]
n = int(n)
TAG = re.compile(r"\[[^\]]*\]")
take = json.load(open(tj, encoding="utf-8"))
patch = json.load(open(pj, encoding="utf-8"))
y, sr = sf.read(tw)
p, psr = sf.read(pw)
assert sr == psr == 44100


def words_of(text, chars, starts, ends):
    s = "".join(chars)
    i = s.find(text)
    i = 0 if i < 0 else i
    spoken = list(text)
    for m in TAG.finditer(text):
        for k in range(m.start(), m.end()):
            spoken[k] = " "
    out, cur, k0 = [], "", None
    for k, ch in enumerate(spoken + [" "]):
        if ch.isspace():
            if cur.strip(" .،,:؟?!«»\"'"):
                last = k - 1
                while last > k0 and spoken[last] in ".،,:؟?!«»\"'":
                    last -= 1
                out.append({"w": cur, "start": round(starts[i + k0], 3), "end": round(ends[i + last], 3)})
            cur, k0 = "", None
            continue
        if k0 is None:
            k0 = k
        cur += ch
    return out


L = take["lines"]
i = n - 1
cut0 = (L[i - 1]["end"] + L[i]["start"]) / 2 if i > 0 else max(0.0, L[i]["start"] - 0.1)
cut1 = (L[i]["end"] + L[i + 1]["start"]) / 2 if i + 1 < len(L) else len(y) / sr
pw_words = words_of(patch["text"], patch["chars"], patch["starts"], patch["ends"])
# trim the patch to its speech, with the same breathing room the original line had inside its cut points
lead = L[i]["start"] - cut0
tail = cut1 - L[i]["end"]
p0 = max(0, int((pw_words[0]["start"] - 0.03) * sr))
p1 = min(len(p), int((pw_words[-1]["end"] + 0.12) * sr))
seg = p[p0:p1]
# match loudness of the replaced line
orig = y[int(L[i]["start"] * sr):int(L[i]["end"] * sr)]
rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)
seg = seg * (rms(orig) / rms(seg))
fade = int(0.006 * sr)
seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
new_mid = np.concatenate([np.zeros(int(lead * sr)), seg, np.zeros(int(max(0.0, tail - 0.09) * sr))])
out = np.concatenate([y[:int(cut0 * sr)], new_mid, y[int(cut1 * sr):]])
delta = len(new_mid) / sr - (cut1 - cut0)
shift_patch = cut0 + lead - (p0 / sr)
new_line = {"text": TAG.sub("", patch["text"]).strip(),
            "words": [{"w": w["w"], "start": round(w["start"] + shift_patch, 3), "end": round(w["end"] + shift_patch, 3)} for w in pw_words]}
new_line["start"], new_line["end"] = new_line["words"][0]["start"], new_line["words"][-1]["end"]
lines = []
for k, l in enumerate(L):
    if k < i:
        lines.append(l)
    elif k == i:
        lines.append(new_line)
    else:
        lines.append({"text": l["text"], "start": round(l["start"] + delta, 3), "end": round(l["end"] + delta, 3),
                      "words": [{"w": w["w"], "start": round(w["start"] + delta, 3), "end": round(w["end"] + delta, 3)} for w in l["words"]]})
sf.write(ow, out.astype(np.float32), sr, subtype="PCM_16")
meta = {k: v for k, v in take.items() if k not in ("lines", "chars", "starts", "ends")}
meta.update({"lines": lines, "duration": round(len(out) / sr, 3), "patched": {"line": n, "seed": patch.get("seed")}})
json.dump(meta, open(oj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"line {n} replaced (seed {patch.get('seed')}), length change {delta:+.2f}s -> {ow}")
