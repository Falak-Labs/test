#!/usr/bin/env python3
"""The 4-minute show ("Survival Mode"), built from a spec in English or Arabic: one story cut from four finished builds
with a game layer on top (levels, a boss health bar that the fixes knock down, "achievement unlocked", a results card),
new narration that links the builds, world music that grows with every fix, and game jingles. No new animation.

usage:  python3 show/build_show.py <spec> <lang> <work_dir> [full|short] [fetch prep thumb audio stills video mux qa copy]
  spec      kit/show/specs/<spec>.yml (the four builds, every word on screen, the cues)
  lang      en | ar
  work_dir  anywhere outside the repo; <work_dir>/src gets the builds' final videos as <kit>-<lang>.mp4 (step fetch
            takes them from media/ or, for retired builds, from git history)
  full      the YouTube video: cold open, four levels, results card ending on "Subscribe"
  short     TikTok / Instagram / YouTube Shorts: cold open, level 1, three flashes of the other bosses, a card that sends
            people to the YouTube channel
Narration: kit/series/<voice>_lines.txt (8 lines; Arabic: <voice>_lines_ar_sa.txt) made with voice.yml, plus the three
closing lines every episode shares (kit survivalpromo). kit/show/README.md says what each line must do.
How a build is cut: hook .. fix4 (the "follow" line and its pause are dropped), the reveal, a level-clear beat, then the
joke; the stat line and the closer are dropped (their numbers move into the level-clear panel).
"""
import glob
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import time

import numpy as np
import skia
import soundfile as sf
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ROOT = os.path.dirname(KIT)
sys.path.insert(0, KIT)
sys.path.insert(0, os.path.join(KIT, "episodes"))
from bik.core import prog, clamp, e_out  # noqa: E402
from bik import v2  # noqa: E402
from bik.captions import display_word, word_key  # noqa: E402
from bik.mix import _load_mono  # noqa: E402
from show import sounds as S  # noqa: E402
from show import layout as L  # noqa: E402

W, H, FPS = 1080, 1920, 30
SPF = S.SR // FPS
BGRA = skia.kBGRA_8888_ColorType
SHOT_N = 25                       # clean frames per world in the cold open
CLEAR_S = 2.5                     # level-clear beat
CARD_IN = 0.45                    # the level card's sting comes first, then the voice
TITLE_IN = 0.40                   # the title slams in, then the voice
LEAD = 4                          # frames of sound before the picture of the reveal and of the joke (the voice starts first)

# What the series always says. A spec's own block for the language (chip, ribbon, no_icons, result_label, ...) goes on top.
STRINGS = {
    "en": dict(lv="LV {n}", level="LEVEL {n}", final="FINAL LEVEL", boss="BOSS", defeated="DEFEATED", clear="CLEAR!",
               unlocked="ACHIEVEMENT UNLOCKED", score="SCORE", title1="SURVIVAL", title2="MODE", sub="4 LEVELS  ·  4 BOSSES",
               press="PRESS START", world_clear="WORLD CLEAR!", row="LV {n}", rank="RANK S", all_levels="ALL 4 LEVELS",
               on_youtube="ON YOUTUBE", subscribe="SUBSCRIBE", or_boss="or the boss wins", next="NEXT WORLD COMING",
               flash_chip="LEVEL {n}", rtl=False, handle="@congratsengineer", promo="survivalpromo", sfx="",
               cues=dict(flash="four", ribbon="congrats", yt="on", ytcoin="youtube", handle="congrats", subscribe="subscribe")),
    "ar": dict(lv="مرحلة {n}", level="المرحلة {n}", final="المرحلة الأخيرة", boss="الزعيم", defeated="انهزم", clear="تمّت!",
               unlocked="إنجاز جديد", score="النقاط", title1="طور", title2="البقاء", sub="4 مراحل  ·  4 زعماء",
               press="اضغط ابدأ", world_clear="اكتمل العالم!", row="{n}", rank="ممتاز", all_levels="كل المراحل الأربع",
               on_youtube="على يوتيوب", subscribe="اشترك", or_boss="ولا الزعيم يكسب", next="العالم الجاي قرّب",
               flash_chip="المرحلة {n}", rtl=True, handle="@kef.tenbeni", promo="survivalpromo", sfx="_ar_sa",
               cues=dict(flash="اربع", ribbon="ومبروك", yt="يوتيوب", ytcoin="يوتيوب", handle="كيف", subscribe="اشترك")),
}
# The four music beds (kit/show/sounds.py), the key their jingles play in, and their sting in the cold open.
BED_KEY = {"desert": (74, False), "oasis": (81, False), "arctic": (76, True), "ondol": (79, False)}
BED_STAB = {
    "desert": lambda: [(S.pluck(S.midi(m), 0.9, 0.45, 0.9955, 5), 0.06 * j) for j, m in enumerate((62, 63, 66))],
    "oasis": lambda: [(S.drop(S.midi(m)), 0.07 * j) for j, m in enumerate((81, 85, 88))],
    "arctic": lambda: [(S.bell(S.midi(88), 1.2, 0.5), 0.0), (S.bell(S.midi(95), 1.0, 0.4), 0.1)],
    "ondol": lambda: [(S.pluck(S.midi(m), 1.0, 0.62, 0.997, 7), 0.07 * j) for j, m in enumerate((79, 81, 86))],
}
SPEC, STR, LEVELS, LANG = {}, {}, [], "en"


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def load_spec(sid, lang):
    """Fill SPEC / STR / LEVELS for one episode in one language and hand the words to the layout."""
    global SPEC, STR, LEVELS, LANG
    SPEC = yaml.safe_load(open(os.path.join(HERE, "specs", sid + ".yml"), encoding="utf-8"))
    SPEC["id"], LANG = sid, lang
    STR = dict(STRINGS[lang])
    own = dict(SPEC.get(lang) or {})
    STR["cues"] = dict(STR["cues"], **(own.pop("cues", None) or {}))
    STR.update(own)
    LEVELS = []
    for n, lv in enumerate(SPEC["levels"], 1):
        d = {k: v for k, v in lv.items() if k not in ("en", "ar")}
        d.update(lv[lang])
        d.update(n=n, final=(n == len(SPEC["levels"])), key=BED_KEY[d["music"]], line=3 + n, chips=[tuple(x) for x in d["chips"]])
        LEVELS.append(d)
    L.set_strings({k: v for k, v in STR.items() if k in L.T})


def voice_paths():
    v = os.path.join(KIT, "series/voice", SPEC.get("voice", SPEC["id"]) + STR["sfx"])
    p = os.path.join(KIT, "series/voice", STR["promo"] + STR["sfx"])
    return v, p


def load_ep(kit):
    spec = importlib.util.spec_from_file_location("episode_" + kit, os.path.join(KIT, "episodes", kit + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    vo = os.path.join(KIT, f"series/voice/{kit}{STR['sfx']}")
    return m.EPISODE(vo + ".json", vo + ".wav") if LANG == "en" else m.EPISODE(vo + ".json", vo + ".wav", lang="ar_sa")


def chapter_cuts(ep):
    """Frame ranges of a build that the show keeps, and its four (break, fix) times."""
    tl = ep.tl

    def first_chunk(label):
        for ch, st in zip(ep.cap.chunks, ep.cap.starts):
            if ep.words[ch[0]]["label"] == label:
                return st
        raise ValueError(label)

    last = int(ep.duration * FPS) - 1
    return dict(a=(1, int(round(tl.pause_start * FPS))),
                b=(math.ceil(first_chunk("reveal") * FPS - 1e-6), int(round((tl.e("reveal") + 0.20) * FPS))),
                c=(math.ceil(first_chunk("tag") * FPS - 1e-6), min(last, int(round((tl.e("tag") + 0.8) * FPS)))),
                spans=[(float(a), float(b)) for a, b in ep.spans], cover_t=float(ep.cover_time()))


def fetch(work):
    """The builds' final videos -> <work>/src/<kit>-<lang>.mp4, from media/ or (retired builds) from git history."""
    os.makedirs(os.path.join(work, "src"), exist_ok=True)
    slugs = {e["kit"]: e["slug"] for e in yaml.safe_load(open(os.path.join(ROOT, "episodes.yml"), encoding="utf-8"))["episodes"]}
    for lv in LEVELS:
        dst = os.path.join(work, "src", f"{lv['kit']}-{LANG}.mp4")
        if os.path.exists(dst) and os.path.getsize(dst) > 1e6:
            continue
        rel = f"media/{slugs[lv['kit']]}-{LANG}.mp4"
        if os.path.exists(os.path.join(ROOT, rel)):
            run(["cp", os.path.join(ROOT, rel), dst])
            where = "media/"
        else:
            sha = run(["git", "-C", ROOT, "log", "--diff-filter=D", "-n", "1", "--format=%H", "--", rel], capture_output=True,
                      text=True).stdout.strip()
            if not sha:
                raise SystemExit(f"{rel}: not in media/ and never deleted in git history")
            with open(dst, "wb") as f:
                run(["git", "-C", ROOT, "show", f"{sha}^:{rel}"], stdout=f)
            where = f"git {sha[:7]}^"
        print(f"fetch {lv['kit']}-{LANG}: {os.path.getsize(dst) / 1e6:.1f} MB from {where}", flush=True)


# ------------------------------------------------------------------ the plan: every segment in frames
def snap_pauses(lines, wav_path):
    """A voice file's word times can be estimates. Where a word ends a sentence or a clause inside a line, move that
    boundary onto the real pause in the recording (the nearest silence of 90 ms or more) and stretch the words on both
    sides to fit, so captions, sounds and cuts land where the voice really is."""
    a, sr = sf.read(wav_path, dtype="float32")
    a = a if a.ndim == 1 else a.mean(axis=1)
    hop = int(0.01 * sr)
    env = np.sqrt(np.array([np.mean(a[i:i + hop] ** 2) for i in range(0, len(a) - hop, hop)]) + 1e-12)
    quiet = env < 0.03 * env.max()

    def pause_near(b):
        best, j, stop = None, max(0, int((b - 0.45) * 100)), min(len(quiet), int((b + 0.45) * 100))
        while j < stop:
            if not quiet[j]:
                j += 1
                continue
            k = j
            while k < len(quiet) and quiet[k]:
                k += 1
            if k - j >= 9 and (best is None or abs((j + k) / 200 - b) < abs((best[0] + best[1]) / 2 - b)):
                best = (j / 100, k / 100)
            j = k
        return best

    for ln in lines:
        ws = ln["words"]
        cuts = [(i, pause_near(ws[i]["end"])) for i in range(len(ws) - 1) if re.search(r"[.,!?،؟]$", ws[i]["w"])]
        cuts = [(i, g) for i, g in cuts if g]
        first, new_start = 0, ws[0]["start"]
        for i, gap in cuts + [(len(ws) - 1, None)]:                # one stretch of speech at a time
            old0, old1 = ws[first]["start"], ws[i]["end"]
            new1 = gap[0] if gap else old1
            if old1 > old0 and new1 > new_start:
                f = (new1 - new_start) / (old1 - old0)
                for w in ws[first:i + 1]:
                    w["start"], w["end"] = new_start + (w["start"] - old0) * f, new_start + (w["end"] - old0) * f
            if gap:
                first, new_start = i + 1, gap[1]


def ckey(s):
    return word_key(display_word(s))


def find_cue(ln, cue, frac):
    """Index of the word in a narration line that a picture or a sound hangs on: the first word that starts with the
    cue, else the word nearest to `frac` of the line."""
    ws = ln["words"]
    k = ckey(cue) if cue else ""
    if k:
        for i, w in enumerate(ws):
            if ckey(w["w"]).startswith(k):
                return i
        print(f"  note: cue '{cue}' is not in line \"{' '.join(w['w'] for w in ws)}\"; using {frac:.0%} of the line", flush=True)
    t = ln["start"] + frac * (ln["end"] - ln["start"])
    return min(range(len(ws)), key=lambda i: abs(ws[i]["start"] - t))


class Plan:
    """variant "full": cold open, four levels, results card. variant "short": cold open, level 1, a teaser of the other
    bosses and the card that sends people to the YouTube channel."""

    def __init__(self, info_path, variant="full"):
        self.variant = variant
        self.ch = json.load(open(info_path))
        vo, promo = voice_paths()
        self.vo = json.load(open(vo + ".json"))["lines"]
        self.pv = json.load(open(promo + ".json"))["lines"]
        snap_pauses(self.vo, vo + ".wav")
        snap_pauses(self.pv, promo + ".wav")
        self.extra = {}                                            # pieces cut out of a recorded line
        for ln in self.vo + self.pv:
            ln["dur"] = ln["end"] - ln["start"]
        cu = STR["cues"]
        l1, l2, l3, l8 = self.vo[0], self.vo[1], self.vo[2], self.vo[7]
        p1, p2, p3 = self.pv[:3]
        starts = [0] + [i + 1 for i, w in enumerate(l1["words"][:-1]) if re.search(r"[.!?؟]$", w["w"])]
        if len(starts) < 3:                                        # line 1 is three short sentences; else cut it in thirds
            n1 = len(l1["words"])
            starts = [0, n1 // 3, 2 * n1 // 3]
        self.cue = dict(no=starts[:3], flash=find_cue(l2, cu.get("flash"), 0.30), ribbon=find_cue(l3, cu.get("ribbon"), 0.40),
                        sub=find_cue(l3, cu.get("sub"), 0.72), stat=find_cue(l8, cu.get("stat"), 0.25),
                        yt=find_cue(p2, cu.get("yt"), 0.40), ytcoin=find_cue(p2, cu.get("ytcoin"), 0.55),
                        handle=find_cue(p2, cu.get("handle"), 0.75), subscribe=find_cue(p3, cu.get("subscribe"), 0.5))
        self.levels = [0] if variant == "short" else list(range(len(LEVELS)))
        self.segs, self.vo_at = [], {}
        f = 0

        def add(kind, n, **kw):
            nonlocal f
            self.segs.append(dict(kind=kind, start=f, n=int(n), **kw))
            f += int(n)

        add("cover", 1)
        t1 = 0.25
        t2 = t1 + l1["dur"] + 0.30
        t3 = t2 + l2["dur"] + 0.35
        add("cold", round((t3 + TITLE_IN + l3["dur"] + 0.95) * FPS), t1=t1, t2=t2, t3=t3)
        cold = self.segs[-1]["start"] / FPS
        self.vo_at.update({1: cold + t1, 2: cold + t2, 3: cold + t3 + TITLE_IN})
        for i in self.levels:
            lv = LEVELS[i]
            ln = self.vo[lv["line"] - 1]
            cuts = self.ch[lv["kit"]]
            add("card", round((CARD_IN + ln["dur"] + 0.60) * FPS), lv=i)
            self.vo_at[lv["line"]] = self.segs[-1]["start"] / FPS + CARD_IN
            add("chapA", cuts["a"][1] - cuts["a"][0], lv=i, f0=cuts["a"][0])
            add("chapB", cuts["b"][1] - cuts["b"][0], lv=i, f0=cuts["b"][0], dissolve=4)
            add("clear", round(CLEAR_S * FPS), lv=i)
            add("chapC", cuts["c"][1] - cuts["c"][0], lv=i, f0=cuts["c"][0], dissolve=5)
        if variant == "short":
            k = self.cue["subscribe"]
            sub = dict(p3, start=p3["words"][k]["start"] - 0.05, words=p3["words"][k:])   # "Subscribe, or the boss wins."
            sub["dur"] = sub["end"] - sub["start"]
            self.extra["p3b"] = sub
            tp1 = 0.25
            t_card = tp1 + p1["dur"] + 0.30                       # three boss flashes fill tp1 .. t_card
            tp2 = t_card + TITLE_IN
            tp3 = tp2 + p2["dur"] + 0.28
            add("outro", round((tp3 + sub["dur"] + 1.1) * FPS), tp1=tp1, t_card=t_card, tp2=tp2, tp3=tp3, dissolve=6)
            o = self.segs[-1]["start"] / FPS
            self.vo_at.update({"p1": o + tp1, "p2": o + tp2, "p3b": o + tp3})
        else:
            e8 = 2.30                                              # after the fanfare
            e9 = e8 + l8["dur"] + 0.30
            add("end", round((e9 + p3["dur"] + 1.5) * FPS), t8=e8, t9=e9, dissolve=8)
            end = self.segs[-1]["start"] / FPS
            self.vo_at.update({8: end + e8, "p3": end + e9})
        self.frames = f
        self.duration = f / FPS

    def line(self, key):
        if key in self.extra:
            return self.extra[key]
        return self.pv[int(key[1:]) - 1] if isinstance(key, str) else self.vo[key - 1]

    def seg(self, kind, lv=None):
        return next(s for s in self.segs if s["kind"] == kind and (lv is None or s.get("lv") == lv))

    def has(self, kind):
        return any(s["kind"] == kind for s in self.segs)

    def word_t(self, key, idx):
        """Global time at which word idx of a narration line (1..8, or "p1".."p3" for the closing lines) starts."""
        ln = self.line(key)
        return self.vo_at[key] + ln["words"][idx]["start"] - ln["start"]

    def caption_words(self):
        out = []
        for key, t0 in sorted(self.vo_at.items(), key=lambda kv: kv[1]):
            ln = self.line(key)
            for w in ln["words"]:
                word = display_word(w["w"])
                if word:
                    out.append({"word": word, "key": word_key(word), "label": f"vo{key}", "start": t0 + w["start"] - ln["start"],
                                "end": t0 + w["end"] - ln["start"], "brk": bool(re.search(r"[.,!?،؟]$", w["w"]))})
        return out


# ------------------------------------------------------------------ prep: timings and clean pictures
def prep(out):
    os.makedirs(os.path.join(out, "cache"), exist_ok=True)
    info, surf = {}, skia.Surface(W, H)
    c = surf.getCanvas()
    stills = []
    for i, lv in enumerate(LEVELS):
        ep = load_ep(lv["kit"])
        info[lv["kit"]] = chapter_cuts(ep)
        brk1 = info[lv["kit"]]["spans"][0][0]
        shot, still = lv.get("shot", brk1 - 1.5), lv.get("still", brk1 - 0.5)      # the end of the hook: the first simple version
        t0 = time.time()
        for j in range(SHOT_N):                                  # the world moving, no HUD, no captions
            c.save()
            ep.draw_world(c, shot + j / FPS)
            c.restore()
            surf.makeImageSnapshot().save(os.path.join(out, "cache", f"shot{i}_{j:02d}.jpg"), skia.kJPEG, 92)
        c.save()
        ep.draw_world(c, still)
        c.restore()
        L.blurred(surf.makeImageSnapshot(), 16, 0.42, lv["color"]).save(os.path.join(out, "cache", f"cardbg{i}.jpg"), skia.kJPEG, 92)
        c.save()
        ep.draw_world(c, info[lv["kit"]]["cover_t"])
        c.restore()
        stills.append(surf.makeImageSnapshot())
        print(f"prep {lv['kit']}: shot {shot:.2f} still {still:.2f} {info[lv['kit']]}  ({time.time() - t0:.0f} s)", flush=True)
    L.quad(stills, 0.5).save(os.path.join(out, "cache", "wall.jpg"), skia.kJPEG, 92)
    json.dump(info, open(os.path.join(out, "chapters.json"), "w"), indent=1)


def img(out, name):
    return skia.Image.open(os.path.join(out, "cache", name))


# ------------------------------------------------------------------ audio
def chapter_audio(path):
    raw = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-vn", "-ac", "2", "-ar", str(S.SR), "-f", "f32le", "-"],
              capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def finalize(src, dst, target=-14.0):
    """Two-pass loudness to -14 LUFS and a brick wall at -2.2 dBFS (the kit's master without its compressor)."""
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={target}:TP=-1.7:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
    flt = (f"loudnorm=I={target}:TP=-1.7:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
           f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,aresample={S.SR},"
           f"alimiter=limit=0.776:attack=2:release=60:level=0")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", flt, "-ar", str(S.SR), dst])
    return js


def lufs(x):
    import pyloudnorm
    return pyloudnorm.Meter(S.SR).integrated_loudness(x.astype(np.float64))


def audio(work, out, plan):
    n = plan.frames * SPF
    chap, bed, fxb = S.stereo(n), S.stereo(n), S.stereo(n)
    vob = np.zeros(n, np.float32)
    ev = []                                                    # (seconds, sound, gain, pan)
    cue = plan.cue

    def piece(buf, srcb, f0, f1, f_out, lead=0):
        a = srcb[(f0 - lead) * SPF: f1 * SPF].copy()
        k = int(0.015 * S.SR)
        a[:k] *= np.linspace(0, 1, k)[:, None]
        a[-k:] *= np.linspace(1, 0, k)[:, None]
        i = (f_out - lead) * SPF
        buf[i:i + len(a)] += a[:max(0, len(buf) - i)]

    # narration: the new lines
    vo_p, promo_p = voice_paths()
    voices = {False: _load_mono(vo_p + ".wav"), True: _load_mono(promo_p + ".wav")}
    for num, t0 in plan.vo_at.items():
        ln = plan.line(num)
        vo = voices[isinstance(num, str)]
        a = vo[int((ln["start"] - 0.02) * S.SR) if ln["start"] > 0.02 else 0: int((ln["end"] + 0.10) * S.SR)].copy()
        k = int(0.01 * S.SR)
        a[:k] *= np.linspace(0, 1, k)
        a[-k:] *= np.linspace(1, 0, k)
        i = int((t0 - min(0.02, ln["start"])) * S.SR)
        vob[i:i + len(a)] += a
    tmp = os.path.join(plan.dir, "vo_raw.wav")
    sf.write(tmp, vob, S.SR)
    from bik.mix import master
    master(tmp, os.path.join(plan.dir, "vo_master.wav"))
    vom, _ = sf.read(os.path.join(plan.dir, "vo_master.wav"), dtype="float32")
    vom = vom if vom.ndim == 1 else vom.mean(axis=1)
    vom = np.pad(vom, (0, max(0, n - len(vom))))[:n]
    vom *= 10 ** ((-14.3 - lufs(np.stack([vom, vom], 1))) / 20)      # the same level as the narration inside the builds

    # cold open
    cold = plan.seg("cold")
    T0 = cold["start"] / FPS
    t2, t3 = T0 + cold["t2"], T0 + cold["t3"]
    S.place(bed, S.drone(t3 - T0 + 0.3), T0, 0.5)
    for k in range(3):
        tk = plan.word_t(1, cue["no"][k])
        ev += [(tk - 0.04, S.hit(20 + k), 0.6, 0.0), (tk - 0.30, S.whoosh(0.3, True, 30 + k), 0.25, 0.0)]
    four = plan.word_t(2, cue["flash"])
    tt, i = t2, 0
    while tt < t3 - 0.15:
        ev.append((tt, S.tick(i % 2 == 1), 0.32, -0.3 if i % 2 else 0.3))
        tt += 0.25 if tt < four else 0.125
        i += 1
    fd = (t3 - four) / 4
    for k in range(4):
        tk = four + k * fd
        ev.append((tk - 0.06, S.whoosh(0.35, k % 2 == 0, 40 + k), 0.4, -0.4 if k % 2 else 0.4))
        ev.append((tk, S.hit(50 + k), 0.3, 0.0))
        for snd, dt in BED_STAB[LEVELS[k]["music"]]():
            ev.append((tk + 0.05 + dt, snd, 0.5, 0.0))
    ev += [(t3 - 1.45, S.riser(1.45), 0.35, 0.0), (t3, S.slam(), 0.8, 0.0), (plan.word_t(3, cue["ribbon"]), S.coin(), 0.3, 0.2),
           (t3 + TITLE_IN + plan.vo[2]["dur"] + 0.40, S.press_start(), 0.5, 0.0)]

    # levels
    for i in plan.levels:
        lv = LEVELS[i]
        cuts = plan.ch[lv["kit"]]
        card, A, B, K, Cc = (plan.seg(k, i) for k in ("card", "chapA", "chapB", "clear", "chapC"))
        src = chapter_audio(os.path.join(work, "src", f"{lv['kit']}-{LANG}.mp4"))
        piece(chap, src, cuts["a"][0], cuts["a"][1], A["start"])
        piece(chap, src, cuts["b"][0], cuts["b"][1], B["start"], LEAD)
        piece(chap, src, cuts["c"][0], cuts["c"][1], Cc["start"], LEAD)
        tc, ta, tk = card["start"] / FPS, A["start"] / FPS, K["start"] / FPS
        loc = lambda t: ta + t - cuts["a"][0] / FPS            # build time -> show time (inside A)
        tonic, minor = lv["key"]
        ev += [(tc - 0.20, S.whoosh(0.45, True, 60 + i), 0.5, 0.0), (tc + 0.02, S.boss_appear(), 0.5, 0.0),
               (ta - 0.50, S.level_start(), 0.45, 0.0)]
        ev += [(tc + 0.85 + 0.1 * j, S.score_tick(), 0.15, 0.0) for j in range(8)]
        for j, (tb, tf) in enumerate(cuts["spans"]):
            ev.append((loc(tb) + 0.02, S.boss_attack(), 0.18, -0.2))
            ev.append((loc(tf), S.boss_down(tonic - 12, minor) if j == 3 else S.boss_hit(tonic), 0.42 if j == 3 else 0.30, 0.2))
        ev += [(tk + 0.10, S.achievement(tonic, minor), 0.5, 0.0)]
        ev += [(tk + 0.50 + 0.2 * j, S.coin(tonic), 0.26, (-0.5, 0.0, 0.5)[j]) for j in range(3)]
        ev += [(tk + 1.10 + 0.05 * j, S.score_tick(), 0.2, 0.0) for j in range(12)]
        # music: grows with the fixes; the last level's music carries on under the closing card
        end_f = plan.frames if i == plan.levels[-1] else Cc["start"] + Cc["n"]
        mev = {"card": 0.0, "a0": ta - tc, "brk": [loc(tb) - tc for tb, _ in cuts["spans"]], "fix": [loc(tf) - tc for _, tf in cuts["spans"]],
               "b0": B["start"] / FPS - tc, "clear": tk - tc, "c0": Cc["start"] / FPS - tc, "end": end_f / FPS - tc}
        m = S.MUSIC[lv["music"]](mev["end"] + 0.1, mev)
        m *= 10 ** ((-23.0 - lufs(m)) / 20)
        S.place(bed, m, tc, 1.0)
        print(f"audio level {i + 1}: music {lv['music']} {mev['end']:.1f} s", flush=True)

    tonic = LEVELS[plan.levels[-1]]["key"][0]
    if plan.has("end"):                                        # results card
        end = plan.seg("end")
        te = end["start"] / FPS
        bed[int(te * S.SR): int((te + 3.2) * S.SR)] *= 0.35
        ev += [(te + 0.05, S.victory(tonic - 12), 0.5, 0.0)] + [(te + 0.5 + 0.22 * j, S.coin(tonic), 0.26, -0.3 + 0.2 * j) for j in range(4)]
        s0 = end["t8"] + 0.15
        ev += [(te + s0 + 0.06 * j, S.score_tick(), 0.18, 0.0) for j in range(22)]
        ev += [(plan.word_t(8, cue["stat"]), S.coin(tonic), 0.32, 0.3), (plan.vo_at[8] + plan.vo[7]["dur"] + 0.02, S.hit(70), 0.5, 0.0),
               (plan.word_t("p3", cue["subscribe"]) - 0.05, S.press_start(), 0.5, 0.0)]
    if plan.has("outro"):                                      # three boss flashes, then the YouTube card
        o = plan.seg("outro")
        to = o["start"] / FPS
        fd = (o["t_card"] - o["tp1"] + 0.1) / 3
        for j in range(3):
            tk = to + o["tp1"] - 0.1 + j * fd
            ev += [(tk - 0.06, S.whoosh(0.3, j % 2 == 0, 80 + j), 0.4, 0.4 if j % 2 else -0.4), (tk, S.hit(84 + j), 0.3, 0.0)]
        tc2 = to + o["t_card"]
        bed[int(tc2 * S.SR): int((tc2 + 1.0) * S.SR)] *= 0.5
        ev += [(tc2 - 1.0, S.riser(1.0), 0.3, 0.0), (tc2, S.slam(), 0.8, 0.0), (plan.word_t("p2", cue["ytcoin"]), S.coin(tonic), 0.32, 0.2),
               (plan.word_t("p3b", 0) - 0.05, S.press_start(), 0.5, 0.0)]

    for t, snd, g, pan in ev:
        S.place(fxb, snd, t, g, pan)
    fxb = S.reverb(fxb, wet=0.10)

    # the music dips under speech; the jingles a little
    talk = np.abs(chap).max(axis=1) + np.abs(vom)
    from scipy.ndimage import uniform_filter1d
    k = int(0.06 * S.SR)
    envl = uniform_filter1d(talk, k)
    envl = uniform_filter1d(np.clip(envl / 0.06, 0, 1), k * 3)
    bed *= (1 - 0.50 * envl)[:, None]
    fxb *= (1 - 0.18 * envl)[:, None]
    mix = chap + bed + fxb
    mix[:, 0] += vom
    mix[:, 1] += vom
    raw = os.path.join(plan.dir, "mix_raw.wav")
    sf.write(raw, np.tanh(mix * 0.9) / 0.9, S.SR)
    js = finalize(raw, os.path.join(plan.dir, "mix.wav"))
    for name, x in (("builds", chap), ("narration", np.stack([vom, vom], 1)), ("music", bed), ("jingles", fxb)):
        print(f"  stem {name:9s} {lufs(x):6.1f} LUFS  peak {np.abs(x).max():.2f}")
    print(f"audio: {n / S.SR:.2f} s, in {js['input_i']} LUFS / TP {js['input_tp']} -> -14", flush=True)


# ------------------------------------------------------------------ picture
class Reader:
    """Frames of a build in order (BGRA)."""

    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "bgra", "-"],
                                  stdout=subprocess.PIPE, bufsize=W * H * 4)
        self.idx = 0
        self.scratch = np.empty((H, W, 4), np.uint8)

    def read(self, f, dst):
        while self.idx <= f:
            mv = memoryview(dst if self.idx == f else self.scratch).cast("B")
            got = 0
            while got < len(mv):
                k = self.p.stdout.readinto(mv[got:])
                if not k:
                    raise EOFError(f"frame {self.idx}")
                got += k
            self.idx += 1

    def close(self):
        self.p.stdout.close()
        self.p.kill()


def grab(path, f):
    raw = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{f / FPS:.4f}", "-i", path, "-frames:v", "1", "-f", "rawvideo",
               "-pix_fmt", "bgra", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 4).copy()


def hud_state(i, spans, t):
    done = sum(1 for _, tf in spans if t >= tf)
    hp, hit, gain, atk, score = 4.0 - done, 0.0, None, 0.0, 1000 * i + 250 * done
    for j, (tb, tf) in enumerate(spans):
        if tf <= t < tf + 0.4:
            hp = (4 - j) - e_out((t - tf) / 0.4)
            score = 1000 * i + 250 * j + 250 * e_out((t - tf) / 0.4)
        if tf <= t < tf + 0.35:
            hit = 1 - (t - tf) / 0.35
        if tf <= t < tf + 1.0:
            gain = ("+250", (t - tf) / 1.0)
        if tb <= t < min(tf, tb + 1.2):
            atk = max(atk, 1 - (t - tb) / 1.2)
    down = clamp((t - spans[3][1] - 0.45) / 0.5)
    return dict(hp=hp, score=score, atk=atk, hit=hit, down=down, gain=gain)


class Show:
    def __init__(self, work, out, plan):
        self.src, self.out, self.plan = os.path.join(work, "src"), out, plan
        self.caps = v2.Captions(plan.caption_words(), STR.get("emph") or [], rtl=STR["rtl"])
        self.wall = img(out, "wall.jpg")
        self.cardbg = [img(out, f"cardbg{i}.jpg") for i in range(len(LEVELS))]
        self.shots = {}
        self.arr = np.zeros((H, W, 4), np.uint8)
        self.surf = skia.Surface(self.arr, colorType=BGRA)
        self.c = self.surf.getCanvas()
        self.readers, self.clearbg, self.prev = {}, {}, None

    def shot(self, k, j):
        key = (k, min(SHOT_N - 1, j))
        if key not in self.shots:
            self.shots[key] = img(self.out, f"shot{key[0]}_{key[1]:02d}.jpg")
        return self.shots[key]

    def path(self, i):
        return os.path.join(self.src, f"{LEVELS[i]['kit']}-{LANG}.mp4")

    def raw(self, i, f, sequential):
        if sequential:
            if i not in self.readers:
                self.readers[i] = Reader(self.path(i))
            self.readers[i].read(f, self.arr)
        else:
            self.arr[...] = grab(self.path(i), f)

    def frame(self, g, sequential=True):
        """Draw global frame g into self.arr."""
        plan, c = self.plan, self.c
        seg = next(s for s in reversed(plan.segs) if s["start"] <= g)
        k, tg = g - seg["start"], g / FPS
        t = k / FPS
        kind, i = seg["kind"], seg.get("lv")
        lv = LEVELS[i] if i is not None else None
        c.save()
        if kind == "cover":
            L.title_art(c, self.wall, 1.0)
        elif kind == "cold":
            self.cold(c, seg, t, tg)
        elif kind == "card":
            L.level_card(c, lv, self.cardbg[i], t, seg["n"] / FPS, self.caps, tg)
            L.flash(c, 0.9 * prog(k, seg["n"] - 5, seg["n"] - 1))
        elif kind in ("chapA", "chapB", "chapC"):
            f = seg["f0"] + k
            self.raw(i, f, sequential)
            if kind == "chapB" and k == seg["n"] - 1:                 # the level-clear beat freezes on this picture
                self.clearbg[i] = L.blurred(skia.Image.fromarray(self.arr.copy(), colorType=BGRA), 30, 0.55, lv["color"])
            st = hud_state(i, plan.ch[lv["kit"]]["spans"], f / FPS)
            L.hud_bar(c, lv["n"], lv["boss"], st["hp"], st["score"], st["atk"], st["hit"], st["down"], f / FPS, st["gain"])
            if kind == "chapA":
                L.flash(c, 0.75 * (1 - prog(k, 0, 3)))
        elif kind == "clear":
            if i not in self.clearbg:                                  # stills mode: fetch the frozen picture
                cuts = plan.ch[lv["kit"]]
                self.clearbg[i] = L.blurred(skia.Image.fromarray(grab(self.path(i), cuts["b"][1] - 1), colorType=BGRA), 30, 0.55, lv["color"])
            L.clear_panel(c, lv, self.clearbg[i], t, 1000 * i)
            L.hud_bar(c, lv["n"], lv["boss"], 0.0, 1000 * (i + 1), down=1.0, t=t)       # the game bar stays on
        elif kind == "end":
            rows = [(STR["row"].format(n=v["n"]), v["unlocked"]) for v in LEVELS]
            ev = dict(score0=seg["t8"] + 0.15, score1=seg["t8"] + 1.5, power=plan.word_t(8, plan.cue["stat"]) - seg["start"] / FPS,
                      rank=seg["t8"] + plan.vo[7]["dur"], next=seg["t9"],
                      pill=plan.word_t("p3", plan.cue["subscribe"]) - seg["start"] / FPS - 0.05)
            L.end_card(c, self.wall, t, rows, ev, self.caps, tg, next_text=STR["next"], pill=(STR["subscribe"], STR["or_boss"]))
        elif kind == "outro":
            self.outro(c, seg, t, tg)
        d = seg.get("dissolve", 6 if kind == "card" else 0)
        if sequential and self.prev is not None and k < d:
            p = skia.Paint()
            p.setAlphaf(1 - (k + 1) / (d + 1))
            c.drawImage(self.prev, 0, 0, L.LIN, p)
        c.restore()
        if sequential and k == seg["n"] - 1:
            self.prev = skia.Image.fromarray(self.arr.copy(), colorType=BGRA)
        return self.arr

    def outro(self, c, seg, t, tg):
        """Short cut only: the three bosses still waiting, then the card that points to the YouTube channel."""
        plan = self.plan
        if t < seg["t_card"]:
            t0 = seg["tp1"] - 0.1
            fd = (seg["t_card"] - t0) / 3
            j = int(clamp((t - t0) / fd, 0, 2.999)) if t >= t0 else 0
            tt = max(0.0, t - t0 - j * fd)
            lv = LEVELS[j + 1]
            L.world_flash(c, self.shot(j + 1, int(tt * FPS)), j + 1, lv["boss"], tt, fd, chip=STR["flash_chip"].format(n=lv["n"]),
                          dim=lv.get("flash_dim", 0.0))
        else:
            tt = t - seg["t_card"]
            wt = lambda idx: plan.word_t("p2", idx) - seg["start"] / FPS - seg["t_card"]
            ws = plan.word_t("p3b", 0) - seg["start"] / FPS - seg["t_card"]
            cu = plan.cue
            L.yt_card(c, self.wall, tt, STR["handle"], p_top=prog(tt, 0.0, 0.14), p_yt=prog(tt, wt(cu["yt"]), wt(cu["yt"]) + 0.2),
                      p_handle=prog(tt, wt(cu["handle"]) - 0.1, wt(cu["handle"]) + 0.2), p_pill=prog(tt, ws - 0.05, ws + 0.25))
            L.flash(c, 0.8 * (1 - prog(tt, 0.0, 0.14)))
        self.caps.draw(c, W, tg)

    def cold(self, c, seg, t, tg):
        plan, cu = self.plan, self.plan.cue
        T0 = seg["start"] / FPS
        no = [plan.word_t(1, j) - T0 for j in cu["no"]]
        four = plan.word_t(2, cu["flash"]) - T0
        t2, t3 = seg["t2"], seg["t3"]
        if t < t2 - 0.04:
            L.backdrop(c, t)
            j = sum(1 for x in no if t >= x) - 1
            if j >= 0:
                L.slam_icon(c, j, t - no[j], shake_seed=j)
            L.flash(c, 1 - prog(t, 0.0, 0.2), L.DEEP)
        elif t < four:
            L.backdrop(c, t)
            L.lone(c, t - (t2 - 0.04))
        elif t < t3:
            fd = (t3 - four) / 4
            j = min(3, int((t - four) / fd))
            tt = t - four - j * fd
            L.world_flash(c, self.shot(j, int(tt * FPS)), j, LEVELS[j]["stamp"], tt, fd, dim=LEVELS[j].get("flash_dim", 0.0))
        else:
            tt = t - t3
            wt = lambda idx: plan.word_t(3, idx) - T0 - t3
            L.title_art(c, self.wall, tt, p_sur=prog(tt, 0.0, 0.14), p_mode=prog(tt, 0.20, 0.34),
                        p_rib=prog(tt, wt(cu["ribbon"]), wt(cu["ribbon"]) + 0.25), p_sub=prog(tt, wt(cu["sub"]), wt(cu["sub"]) + 0.3),
                        start=1.0 if tt > TITLE_IN + plan.vo[2]["dur"] + 0.2 else 0.0)
            L.flash(c, 0.8 * (1 - prog(tt, 0.0, 0.14)))
        self.caps.draw(c, W, tg)


def stills(work, out, plan, frames=None, name="sheet"):
    from PIL import Image
    sh = Show(work, out, plan)
    if frames is None:
        cold = plan.seg("cold")
        T0 = cold["start"]
        frames = [0, T0 + 14, round((plan.word_t(1, plan.cue["no"][2]) + 0.4) * FPS),
                  T0 + round((cold["t2"] + 0.5) * FPS), T0 + round((cold["t3"] - 0.3) * FPS), T0 + round((cold["t3"] + 2.2) * FPS)]
        for i in plan.levels:
            cuts = plan.ch[LEVELS[i]["kit"]]
            card, A, B, K, Cc = (plan.seg(k, i) for k in ("card", "chapA", "chapB", "clear", "chapC"))
            loc = lambda t: A["start"] + round(t * FPS) - cuts["a"][0]
            frames += [card["start"] + 75, loc(cuts["spans"][0][0] + 0.25), loc(cuts["spans"][2][1] + 0.6), K["start"] + 62, Cc["start"] + 60]
        last = plan.segs[-1]
        frames += [last["start"] + round(x * last["n"]) for x in (0.06, 0.18, 0.3, 0.45, 0.6, 0.75, 0.9, 0.985)]
    os.makedirs(os.path.join(plan.dir, "stills"), exist_ok=True)
    tiles = []
    for g in frames:
        a = sh.frame(min(plan.frames - 1, max(0, int(g))), sequential=False)
        tiles.append(Image.fromarray(a[..., [2, 1, 0]]).resize((W // 4, H // 4)))
    cols = 8
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W // 4, rows * H // 4), "black")
    for n, im in enumerate(tiles):
        sheet.paste(im, ((n % cols) * W // 4, (n // cols) * H // 4))
    pth = os.path.join(plan.dir, "stills", name + ".jpg")
    sheet.save(pth, quality=88)
    print("stills", pth, [int(x) for x in frames])


def thumbnail(out):
    """1280 x 720 picture for the YouTube video: the four worlds side by side under the title."""
    TW, TH = 1280, 720
    s = skia.Surface(TW, TH)
    c = s.getCanvas()
    order = list(range(4))[::-1] if STR["rtl"] else list(range(4))       # level 1 leads: on the left in English, on the right in Arabic
    for col, i in enumerate(order):
        im = img(out, f"shot{i}_12.jpg")
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(col * TW / 4, 0, TW / 4, TH))
        c.drawImageRect(im, skia.Rect.MakeXYWH(180, 100, 720, 1620), skia.Rect.MakeXYWH(col * TW / 4, 0, TW / 4, TH), L.LIN, skia.Paint())
        c.restore()
        if col:
            c.drawRect(skia.Rect.MakeXYWH(col * TW / 4 - 3, 0, 6, TH), L.P(L.DEEP, 0.95))
    c.drawRect(skia.Rect.MakeWH(TW, TH), L.P(L.DEEP, 0.36))
    c.drawRect(skia.Rect.MakeWH(TW, TH), L.rad_paint(TW / 2, TH / 2, TW * 0.62, [(L.DEEP, 0.0), (L.DEEP, 0.0), (L.DEEP, 0.7)], [0.0, 0.55, 1.0]))
    L.add_glow(c, TW / 2, 300, 620, L.HILITE, 0.22)
    L.fit(c, f"{STR['title1']} {STR['title2']}", TW / 2, 330, 150, L.HILITE, max_w=1200, stroke_color=L.DEEP, stroke_w=20, shadow_a=0.7)
    c.save()
    c.translate(TW / 2, 455)
    c.rotate(-2.5)
    c.drawRRect(L.rr(-470, -62, 940, 124, 26), L.lin_paint(-470, 0, 470, 0, ["#FF3B4E", "#FF6A3D"]))
    c.drawRRect(L.rr(-468, -60, 936, 120, 26), L.P("#FFFFFF", 0.35, stroke=3))
    ix = 392 if STR["rtl"] else -392
    L.ICON[STR["ribbon_icon"]](c, ix, 0, 96, "#FFFFFF")
    if STR.get("ribbon_crossed"):
        c.drawLine(ix - 42, 38, ix + 42, -38, L.P("#FFFFFF", 1.0, stroke=11))
    L.fit(c, STR["ribbon"], -44 if STR["rtl"] else 44, 26, 76, "#FFFFFF", max_w=720)
    c.restore()
    for col, i in enumerate(order):
        lv = LEVELS[i]
        for stroke in (True, False):
            L.fit(c, lv["stamp"], (col + 0.5) * TW / 4, 640, 62, "#FFFFFF", max_w=TW / 4 - 28,
                  **(dict(stroke_color=L.WARN, stroke_w=16, shadow_a=0.6) if stroke else {}))
    pth = os.path.join(out, "thumbnail.jpg")
    s.makeImageSnapshot().save(pth, skia.kJPEG, 92)
    print("thumbnail", pth, os.path.getsize(pth))


def video(work, out, plan):
    sh = Show(work, out, plan)
    tmp = os.path.join(plan.dir, "video.part.mp4")
    enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r",
                            str(FPS), "-i", "-", "-c:v", "libx264", "-preset", os.environ.get("BIK_PRESET", "veryfast"), "-crf",
                            os.environ.get("BIK_CRF", "18"), "-pix_fmt", "yuv420p", "-threads", "2", tmp], stdin=subprocess.PIPE)
    t0 = time.time()
    for g in range(plan.frames):
        enc.stdin.write(sh.frame(g))
        if g % 600 == 0:
            print(f"video frame {g}/{plan.frames}  {time.time() - t0:.0f} s", flush=True)
    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("encoder failed")
    for r in sh.readers.values():
        r.close()
    os.replace(tmp, os.path.join(plan.dir, "video.mp4"))
    print(f"video done in {time.time() - t0:.0f} s", flush=True)


def mux(out, name):
    from bik.render import mux as kit_mux
    final = os.path.join(out, name + ".mp4")
    kit_mux(os.path.join(out, "video.mp4"), os.path.join(out, "mix.wav"), final)
    return final


def qa(out, name, plan):
    final = os.path.join(out, name + ".mp4")
    d = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final], capture_output=True, text=True).stdout)
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", final, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    i_lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1]
    peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)[-1]
    print(f"QA  duration {d:.2f} s ({int(d // 60)}:{d % 60:04.1f})  loudness {i_lufs} LUFS  true peak {peak} dBFS  "
          f"size {os.path.getsize(final) / 1e6:.1f} MB  frames {plan.frames}")
    marks = [("cold", None)] + [("card", i) for i in plan.levels] + ([("end", None)] if plan.has("end") else [])
    chapters = [f"{int(plan.seg(k, i)['start'] / FPS // 60)}:{int(plan.seg(k, i)['start'] / FPS % 60):02d}" for k, i in marks]
    print("chapters: " + "  ".join(chapters))
    with open(os.path.join(out, "qa.json"), "w") as f:         # show/handoff.py reads the chapter times from here
        json.dump({"duration": round(d, 2), "lufs": float(i_lufs), "peak": float(peak), "chapters": chapters}, f, indent=1)


def copy(out, name, variant, work):
    """The copy that goes out: smaller, starts fast, under GitHub's 100 MB a file."""
    src = os.path.join(out, name + ".mp4")
    dst = os.path.join(work, name + ".mp4")
    for crf in ((22, 24, 26) if variant == "full" else (21, 23)):
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "copy", dst])
        if os.path.getsize(dst) < 95e6:
            break
    print(f"copy {dst} {os.path.getsize(dst) / 1e6:.1f} MB (crf {crf})")


def main():
    sid, lang, work = sys.argv[1:4]
    args = sys.argv[4:]
    variant = next((a for a in args if a in ("full", "short")), "full")
    steps = [a for a in args if a not in ("full", "short")] or ["fetch", "prep", "thumb", "audio", "stills", "video", "mux", "qa", "copy"]
    load_spec(sid, lang)
    out = os.path.join(work, lang)
    os.makedirs(out, exist_ok=True)
    if "fetch" in steps:
        fetch(work)
    if "prep" in steps:
        prep(out)
    if "thumb" in steps:
        thumbnail(out)
    plan = Plan(os.path.join(out, "chapters.json"), variant)
    plan.dir = os.path.join(out, variant)                      # this cut's own files; the cache is shared
    os.makedirs(plan.dir, exist_ok=True)
    print(f"plan {sid} {lang} {variant}: {plan.frames} frames = {plan.duration:.1f} s; " + ", ".join(
        f"{s['kind']}{'' if s.get('lv') is None else s['lv'] + 1}:{s['n']}" for s in plan.segs) + f"; cues {plan.cue}")
    name = f"{sid}-{lang}-{variant}"
    if "audio" in steps:
        audio(work, out, plan)
    if "stills" in steps:
        stills(work, out, plan)
    if "video" in steps:
        video(work, out, plan)
    if "mux" in steps:
        mux(plan.dir, name)
    if "qa" in steps:
        qa(plan.dir, name, plan)
    if "copy" in steps:
        copy(plan.dir, name, variant, work)


if __name__ == "__main__":
    main()
