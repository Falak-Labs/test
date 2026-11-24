"""Build src/data/episode.json (frames) from the voice timeline and an episode spec.
usage: build_episode.py timeline.json episodes/<name>.yml src/data/episode.json [--fps 30]
"""
import argparse, json, re, unicodedata
import yaml

ap = argparse.ArgumentParser()
ap.add_argument("timeline"); ap.add_argument("spec"); ap.add_argument("out")
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--head-lead", type=float, default=0.22, help="headline appears this long before its line is spoken")
a = ap.parse_args()
tl = json.load(open(a.timeline, encoding="utf-8"))
sp = yaml.safe_load(open(a.spec, encoding="utf-8"))
FPS = a.fps
L = {x["line"]: x for x in tl["lines"]}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[إأآا]", "ا", s).replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"[^ء-ي]", "", s)


def word_t(line, key):
    k = norm(key)
    for w in L[line]["words"]:
        if k and k in norm(w["w"]):
            return w["start"]
    raise SystemExit(f"cue word {key!r} not found in line {line}: {[w['w'] for w in L[line]['words']]}")


fr = lambda t: int(round(t * FPS))
last_end = max(x["end"] for x in tl["lines"])
card = sp.get("card")
total = tl["duration"]
if card:
    total = max(total, last_end + 0.6 + card.get("hold", 4.0))
dur_frames = fr(total)

beats = []
bl = sp["beats"]
for i, b in enumerate(bl):
    start = L[b["line"]]["start"] - a.head_lead
    nxt = L[bl[i + 1]["line"]]["start"] - a.head_lead if i + 1 < len(bl) else last_end + 0.45
    item = {"from": 0 if i == 0 else fr(max(0, start)), "to": fr(nxt)}
    segs = []
    for s in b.get("head", []):
        seg = {"t": s[0], "s": s[1]}
        if len(s) > 2:
            seg["at"] = fr(word_t(*s[2]) - 0.05)
        segs.append(seg)
    if segs:
        item["head"] = segs
    if b.get("sub"):
        item["sub"] = b["sub"]
        if b.get("sub_at"):
            item["subFrom"] = fr(word_t(*b["sub_at"]) - 0.05)
        if b.get("sub_color"):
            item["subColor"] = b["sub_color"]
    if b.get("echo"):
        item["echo"] = fr(word_t(*b["echo"]))
    beats.append(item)

scenes = []
sl = sp["scenes"]
for i, s in enumerate(sl):
    start = -1 if i == 0 else L[s["lines"][0]]["start"] - a.head_lead - 0.15
    if i + 1 < len(sl):
        end = L[sl[i + 1]["lines"][0]]["start"] - a.head_lead + 0.1
    else:
        end = total
    cues = {k: fr(word_t(*v)) for k, v in (s.get("cues") or {}).items()}
    span = {"id": s["id"], "from": fr(max(0, start)), "to": fr(end), "cue": cues}
    if s.get("labels"):
        span["labels"] = list(s["labels"])  # on-screen words that depend on the dialect
    scenes.append(span)

ep = {"fps": FPS, "durationInFrames": dur_frames, "palette": sp.get("palette", "slate"), "beats": beats, "scenes": scenes}
if card:
    ep["card"] = {"from": fr(last_end + 0.6), "to": dur_frames + 30, "lines": card["lines"], "ref": card["ref"]}
json.dump(ep, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"episode: {dur_frames} frames ({dur_frames / FPS:.1f}s), {len(beats)} beats, {len(scenes)} scenes -> {a.out}")
