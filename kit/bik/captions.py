"""Word timings from the voiceover audio, and TikTok-style one-word captions."""
import bisect
import re
import numpy as np
import soundfile as sf
from .core import prog, e_back, lerp, clamp
from .draw import text, text_width
from .arabic import is_ar, norm_ar, text_ar, width_ar

BREAK_RE = re.compile(r"[,;:.!?…—،؛؟]$")


def _syllables(word):
    if is_ar(word):  # Arabic: no vowel letters to count, so weight by consonant skeleton length
        return max(1.0, len(norm_ar(word)) / 2.2) + 0.35
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1.0
    groups = re.findall(r"[aeiouy]+", w)
    n = max(1, len(groups) - (1 if w.endswith("e") and len(groups) > 1 else 0))
    return n + 0.35


def display_word(tok):
    if is_ar(tok):
        return re.sub(r"[^\u0621-\u064A\u064B-\u065F\u0670\u0671-\u06D3\u06F0-\u06F90-9]", "", tok)
    w = re.sub(r"[^A-Za-z0-9'’\-]", "", tok)
    return w.upper().replace("’", "'")


def word_key(word):
    return norm_ar(word) if is_ar(word) else re.sub(r"[^A-Z0-9]", "", word)


def word_timings(wav_path, tl):
    """Return a list of dicts {word, key, start, end, label} in video seconds."""
    audio, sr = sf.read(wav_path, dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    out = []
    for ln in tl.lines:
        vs, ve = ln["vo_start"], ln["vo_end"]
        given = ln.get("words")
        if given and len(given) == len(ln["text"].split()):  # exact times from the TTS model's durations
            for gw in given:
                word = display_word(gw["w"])
                if word:
                    out.append({"word": word, "key": word_key(word), "label": ln["label"],
                                "start": tl.vo_to_video(gw["start"]), "end": tl.vo_to_video(gw["end"])})
            continue
        seg = audio[int(vs * sr): int(ve * sr)]
        toks = ln["text"].split()
        brk = [i for i, tk in enumerate(toks[:-1]) if BREAK_RE.search(tk)]
        dur = ve - vs
        # internal silences (>= 50 ms) as phrase anchors
        win = int(0.01 * sr)
        n = len(seg) // win
        gaps = []
        if n > 10:
            fr = seg[: n * win].reshape(n, win)
            db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
            silent = db < db.max() - 30
            i = 3
            while i < n - 3:
                if silent[i]:
                    j = i
                    while j < n - 3 and silent[j]:
                        j += 1
                    if j - i >= 5:
                        gaps.append((i * 0.01, j * 0.01))
                    i = j
                else:
                    i += 1
        bounds = []  # (phrase_start, phrase_end) in line-relative seconds
        if brk and len(gaps) >= len(brk):
            chosen = sorted(sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[: len(brk)])
            st = 0.0
            for g in chosen:
                bounds.append((st, g[0]))
                st = g[1]
            bounds.append((st, dur))
            groups, prev = [], 0
            for b in brk:
                groups.append(list(range(prev, b + 1)))
                prev = b + 1
            groups.append(list(range(prev, len(toks))))
        else:
            bounds = [(0.0, dur)]
            groups = [list(range(len(toks)))]
        for (ps, pe), idxs in zip(bounds, groups):
            wts = [_syllables(toks[i]) for i in idxs]
            tot = sum(wts) or 1.0
            cur = ps
            for i, wgt in zip(idxs, wts):
                d = (pe - ps) * wgt / tot
                word = display_word(toks[i])
                if word:
                    out.append({"word": word, "key": word_key(word), "label": ln["label"],
                                "start": tl.vo_to_video(vs + cur), "end": tl.vo_to_video(vs + cur + d)})
                cur += d
    return out


class Captions:
    def __init__(self, words, emphasis=(), y=1345, size=100, max_w=920, hide=()):
        self.words = words
        self.starts = [w["start"] for w in words]
        self.emph = {word_key(e if is_ar(e) else e.upper()) for e in emphasis}
        self.y, self.size, self.max_w, self.hide = y, size, max_w, list(hide)

    def find(self, label, key, nth=0):
        """Start time of a word (by uppercase key) in a beat; None if absent."""
        if is_ar(key):  # Arabic words carry prefixes (و ف ب ل ال), so match inside the word
            k = norm_ar(key)
            hits = [w for w in self.words if w["label"] == label and k in w["key"]]
        else:
            k = re.sub(r"[^A-Z0-9]", "", key.upper())
            hits = [w for w in self.words if w["label"] == label and w["key"].startswith(k)]
        return hits[nth]["start"] if len(hits) > nth else None

    def draw(self, c, W, t):
        for a, b in self.hide:
            if a <= t < b:
                return
        i = bisect.bisect_right(self.starts, t) - 1
        if i < 0:
            return
        w = self.words[i]
        nxt = self.words[i + 1]["start"] if i + 1 < len(self.words) else w["end"] + 0.4
        if t > min(nxt, w["end"] + 0.35):
            return
        p = prog(t, w["start"], w["start"] + 0.16)
        s = lerp(0.70, 1.0, e_back(p))
        size = self.size
        ar = is_ar(w["word"])
        tw = width_ar(w["word"], size) if ar else text_width(w["word"], size, "Poppins-Black")
        if tw > self.max_w:
            size *= self.max_w / tw
        emph = w["key"] in self.emph or (ar and any(e and e in w["key"] for e in self.emph))
        col = "#FFD43B" if emph else "#FFFFFF"
        c.save()
        c.translate(W / 2, self.y)
        c.scale(s, s)
        if ar:
            text_ar(c, w["word"], 0, size * 0.34, size * 1.05, col, "Tajawal-Black", stroke_color="#0B0B0B",
                    stroke_w=size * 0.2, shadow_a=0.5, a=clamp(p * 5))
        else:
            text(c, w["word"], 0, size * 0.36, size, col, "Poppins-Black", stroke_color="#0B0B0B",
                 stroke_w=size * 0.2, shadow_a=0.5, a=clamp(p * 5))
        c.restore()
