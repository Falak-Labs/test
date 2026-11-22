"""Hand an episode of the show to the main chat, which uploads it to YouTube.
    python3 show/handoff.py <id> <work> [--no-push] [--any-date]      (run from kit/, after the four cuts are checked)

A scheduled run has no browser, so it cannot upload in YouTube Studio. This puts the two full cuts, the two thumbnails
and one upload sheet (<id>.json, also as sheet.json) on the `show` branch of the repo: one orphan commit, force-pushed, so the branch only
ever holds the newest episode. The main chat reads the sheet and uploads (YOUTUBE_STUDIO_UPLOAD.md, "The desk").
The short cuts are not copied: the sheet points at media/<id>-<lang>.mp4 on main, so push those to main as well.

What YouTube shows comes from show/youtube/<id>.yml (copy show/youtube/sm02.yml):
    date: 2026-11-23              the Pacific day the episode goes public (TOMORROW, seen from the run)
    chapters: {en: [...], ar: [...]}   one label per chapter mark the build prints (intro, the four levels, the results)
    en / ar: full: {time: "10:00", title, desc}   short: {time: "12:15", title, desc}
`{chapters}` in a full description becomes the chapter list ("0:00 Intro" ...), taken from <work>/<lang>/full/qa.json."""
import datetime
import json
import os
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ROOT = os.path.dirname(KIT)
RAW = "https://raw.githubusercontent.com/Falak-Labs/test"
BRANCH = "show"
CHANNELS = {"en": ("Congrats Engineer", "UCDkfxHa7q5Ea0OoiSSi8DHA", "English"),
            "ar": ("Kef Tenbeni", "UC8qDuZpMDQXRrowaNp29vow", "Arabic")}
PT = ZoneInfo("America/Los_Angeles")
UTC = datetime.timezone.utc


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def chapters_of(sid, lang, work):
    p = os.path.join(work, lang, "full", "qa.json")
    if not os.path.exists(p):                      # built before qa.json existed: the qa step alone writes it
        run([sys.executable, os.path.join(HERE, "build_show.py"), sid, lang, work, "full", "qa"], cwd=KIT)
    return json.load(open(p))["chapters"]


def entry(lang, kind, date, block, url, thumb=None):
    channel, cid, language = CHANNELS[lang]
    h, m = (int(x) for x in str(block["time"]).split(":"))
    t = datetime.datetime(date.year, date.month, date.day, h, m, tzinfo=PT)
    e = {"url": url, "channel": channel, "channel_id": cid, "language": language, "kind": kind,
         "title": block["title"].strip(), "desc": block["desc"].strip(), "date": f"{t:%b} {t.day}, {t.year}",
         "time": f"{t.hour % 12 or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}",
         "utc": t.astimezone(UTC).strftime("%Y-%m-%dT%H:%MZ")}
    if thumb:
        e["thumb"] = thumb
    return e


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2:
        raise SystemExit(__doc__)
    sid, work = args[0], os.path.abspath(args[1])
    meta = yaml.safe_load(open(os.path.join(HERE, "youtube", sid + ".yml"), encoding="utf-8"))
    date = meta["date"] if isinstance(meta["date"], datetime.date) else datetime.date.fromisoformat(str(meta["date"]))
    tomorrow = (datetime.datetime.now(PT) + datetime.timedelta(days=1)).date()
    problems = []
    if date != tomorrow and "--any-date" not in flags:
        problems.append(f"date is {date}, but the Studio calls schedule for TOMORROW only ({tomorrow} in Pacific time)")
    out = os.path.join(work, "handoff")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    sheet = {}
    for lang in ("en", "ar"):
        if lang not in meta:
            continue
        full = os.path.join(work, f"{sid}-{lang}-full.mp4")
        thumb = os.path.join(work, lang, "thumbnail.jpg")
        short = os.path.join(ROOT, "media", f"{sid}-{lang}.mp4")
        for p in (full, thumb, short):
            if not os.path.exists(p):
                problems.append(f"missing {p}")
        if problems and any("missing" in x for x in problems):
            continue
        if os.path.getsize(full) > 95e6:
            problems.append(f"{full} is over 95 MB")
        marks = chapters_of(sid, lang, work)
        labels = meta["chapters"][lang]
        if len(labels) != len(marks) or marks[0] != "0:00" or len(marks) < 3:
            problems.append(f"{lang}: {len(labels)} chapter labels for {len(marks)} marks {marks} (the first must be 0:00)")
        chapters = "\n".join(f"{t} {label}" for t, label in zip(marks, labels))
        blocks = {k: dict(meta[lang][k]) for k in ("full", "short")}
        if "{chapters}" not in blocks["full"]["desc"]:
            problems.append(f"{lang}: the full description has no {{chapters}} line")
        blocks["full"]["desc"] = blocks["full"]["desc"].replace("{chapters}", chapters)
        for kind, b in blocks.items():
            if len(b["title"].strip()) > (75 if kind == "full" else 100):
                problems.append(f"{lang} {kind}: the title has {len(b['title'].strip())} characters")
            if len(b["desc"]) > 4800 or "<" in b["title"] + b["desc"] or ">" in b["title"] + b["desc"]:
                problems.append(f"{lang} {kind}: description over 4,800 characters, or a < or > in the text (YouTube refuses both)")
        shutil.copy(full, os.path.join(out, f"{sid}-{lang}-full.mp4"))
        shutil.copy(thumb, os.path.join(out, f"{sid}-{lang}-thumb.jpg"))
        sheet[f"{sid}-{lang}-full"] = entry(lang, "full", date, blocks["full"], f"{RAW}/{BRANCH}/{sid}-{lang}-full.mp4",
                                            f"{RAW}/{BRANCH}/{sid}-{lang}-thumb.jpg")
        sheet[f"{sid}-{lang}-short"] = entry(lang, "short", date, blocks["short"], f"{RAW}/main/media/{sid}-{lang}.mp4")
    if problems:
        raise SystemExit("handoff stopped:\n  " + "\n  ".join(problems))
    for name in (sid + ".json", "sheet.json"):             # sheet.json: the fixed name scripts/yt_desk.py reads
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            json.dump(sheet, f, ensure_ascii=False, indent=1)
    for k, e in sheet.items():
        print(f"{k:16} {e['channel']:18} public {e['date']} {e['time']} PT  {e['title']}")
    if "--no-push" in flags:
        print(f"not pushed (--no-push): {out}")
        return
    origin = subprocess.run(["git", "-C", ROOT, "remote", "get-url", "origin"], capture_output=True, text=True, check=True).stdout.strip()
    run(["git", "init", "-q"], cwd=out)
    run(["git", "checkout", "-q", "--orphan", BRANCH], cwd=out)
    run(["git", "add", "."], cwd=out)
    run(["git", "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-qm",
         f"{sid}: full cuts, thumbnails and the upload sheet for the main chat"], cwd=out)
    run(["git", "remote", "add", "origin", origin], cwd=out)
    run(["git", "push", "-q", "--force", "origin", BRANCH], cwd=out)
    print(f"pushed to the `{BRANCH}` branch; the main chat uploads from there. Check one link:")
    print(f"  curl -sI {RAW}/{BRANCH}/sheet.json   (must answer 200; raw links can take a minute)")


if __name__ == "__main__":
    main()
