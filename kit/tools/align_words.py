"""Add word times to a Phonon voice JSON, so captions and animation cues land on the spoken words.

    python3 tools/align_words.py series/voice/<name>        (reads <name>.wav + <name>.json, rewrites the json)

Phonon gives line times only. Inside each line this finds the pauses, decides which pause belongs to which comma or
full stop (the split whose phrase lengths best match their syllable counts), and spreads each phrase's words by
syllables. The times go into lines[i]["words"] (absolute voice seconds), which bik.captions uses as they are.
"""
import json
import os
import re
import sys

import numpy as np
import soundfile as sf

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
from bik.captions import _syllables, BREAK_RE  # noqa: E402

SKIP = 0.06   # cost of a comma that has no pause behind it (seconds squared)


def voiced_and_gaps(seg, sr):
    win = int(0.01 * sr)
    n = len(seg) // win
    db = 20 * np.log10(np.sqrt((seg[: n * win].reshape(n, win) ** 2).mean(axis=1)) + 1e-9)
    loud = db >= db.max() - 30
    idx = np.nonzero(loud)[0]
    if len(idx) == 0:
        return 0.0, len(seg) / sr, []
    t0, t1 = idx[0] * 0.01, (idx[-1] + 1) * 0.01
    gaps, i = [], idx[0]
    while i <= idx[-1]:
        if not loud[i]:
            j = i
            while j <= idx[-1] and not loud[j]:
                j += 1
            if j - i >= 5:
                gaps.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return t0, t1, gaps


def align_line(toks, t0, t1, gaps):
    syl = [_syllables(t) for t in toks]
    brk = [i for i, t in enumerate(toks[:-1]) if BREAK_RE.search(t)]
    speech = (t1 - t0) - sum(b - a for a, b in gaps)
    rate = max(speech, 0.1) / sum(syl)
    m, n = len(brk), len(gaps)
    # boundary k: -1 = line start, else breaks[k]; gap g: -1 = t0, else gaps[g]
    def seg_cost(k0, g0, k1, g1):
        w0 = 0 if k0 < 0 else brk[k0] + 1
        w1 = len(toks) if k1 is None else brk[k1] + 1
        a = t0 if g0 < 0 else gaps[g0][1]
        b = t1 if g1 is None else gaps[g1][0]
        inner = sum(min(e, b) - max(s, a) for s, e in gaps if s >= a and e <= b)
        return ((b - a - inner) - rate * sum(syl[w0:w1])) ** 2
    best = {(-1, -1): (0.0, [])}
    for k in range(m):
        for g in range(n):
            cands = []
            for (pk, pg), (c, path) in list(best.items()):
                if pk < k and pg < g:
                    cands.append((c + seg_cost(pk, pg, k, g) + SKIP * (k - pk - 1), path + [(k, g)]))
            if cands:
                best[(k, g)] = min(cands, key=lambda x: x[0])
    final = min(((c + seg_cost(pk, pg, None, None) + SKIP * (m - 1 - pk), path)
                 for (pk, pg), (c, path) in best.items()), key=lambda x: x[0])
    bounds, k_prev, g_prev = [], -1, -1
    for k, g in final[1] + [(None, None)]:
        w0 = 0 if k_prev < 0 else brk[k_prev] + 1
        w1 = len(toks) if k is None else brk[k] + 1
        a = t0 if g_prev < 0 else gaps[g_prev][1]
        b = t1 if g is None else gaps[g][0]
        bounds.append((w0, w1, a, b))
        k_prev, g_prev = (k, g) if k is not None else (k_prev, g_prev)
    times = []
    for w0, w1, a, b in bounds:
        tot = sum(syl[w0:w1]) or 1.0
        cur = a
        for i in range(w0, w1):
            d = (b - a) * syl[i] / tot
            times.append((cur, cur + d))
            cur += d
    return times


def main():
    prefix = sys.argv[1]
    d = json.load(open(prefix + ".json"))
    audio, sr = sf.read(prefix + ".wav", dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    for ln in d["lines"]:
        toks = ln["text"].split()
        seg = audio[int(ln["start"] * sr): int(ln["end"] * sr)]
        t0, t1, gaps = voiced_and_gaps(seg, sr)
        times = align_line(toks, t0, t1, gaps)
        ln["words"] = [{"w": w, "start": round(ln["start"] + a, 3), "end": round(ln["start"] + b, 3)}
                       for w, (a, b) in zip(toks, times)]
    json.dump(d, open(prefix + ".json", "w"), indent=1, ensure_ascii=False)
    print(prefix + ".json:", sum(len(ln["words"]) for ln in d["lines"]), "words timed")


if __name__ == "__main__":
    main()
