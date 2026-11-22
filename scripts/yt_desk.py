"""The YouTube desk: what the main chat uploads in YouTube Studio, in which order, inside the daily limit.

    python3 scripts/yt_desk.py plan [--last] [--out FILE]   what to upload now; writes the upload sheet for the Studio
                                                     calls (--last: the day's last round also takes `studio: 2` builds)
    python3 scripts/yt_desk.py done <key> <video id> record one upload in youtube/ledger.json (right after each video)
    python3 scripts/yt_desk.py refused <en|ar>       record a "Daily upload limit reached" answer
    python3 scripts/yt_desk.py release <show id>     once its four uploads are recorded: take the show's TikTok and
                                                     Instagram targets off hold in posts/<id>.yml (then commit and push)
    python3 scripts/yt_desk.py check                 for the scheduled runs: is a show upload overdue?

Why: scheduled runs have no browser, so only the main chat (it has the owner's Chrome) can upload to YouTube Studio.
And YouTube limits uploads: see youtube/desk.yml. The steps around this script are in YOUTUBE_STUDIO_UPLOAD.md,
section "The desk".

What it offers, in this order:
  0. the show's full videos   1. the show's shorts        (from sheet.json on the `show` branch, kit/show/handoff.py)
  2. builds marked `studio: 1`  3. builds marked `studio: 2`  (posts/ep*.yml with the YouTube targets on `hold:`)
Only videos that go public TOMORROW (Pacific time): the Studio calls schedule for the date Studio offers by default.
A video is done when its key is in the ledger. While youtube/desk.yml says `verified: false` two limits apply:
`per_day` uploads per Pacific day, and never more than `rolling` of our own uploads inside any 24 hours (a video that
has to wait for an older upload to leave the 24 hours is listed with "not before")."""
import datetime
import json
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
import yt_meta  # noqa: E402

ROOT = post.ROOT
LEDGER = os.path.join(ROOT, "youtube", "ledger.json")
DESK = os.path.join(ROOT, "youtube", "desk.yml")
SHOW_SHEET = "https://raw.githubusercontent.com/Falak-Labs/test/show/sheet.json"
PT = ZoneInfo("America/Los_Angeles")
UTC = datetime.timezone.utc
CHANNEL = {"en": "Congrats Engineer", "ar": "Kef Tenbeni"}


def now():
    t = os.environ.get("YT_NOW")                      # tests: YT_NOW=2026-11-23T00:45Z
    return post.parse_utc(t) if t else datetime.datetime.now(UTC)


def utc(s):
    return post.parse_utc(s if len(s) > 17 else s.replace("Z", ":00Z"))


def pt(t):
    t = t.astimezone(PT)
    return f"{t:%a %b} {t.day} {t.hour % 12 or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}"


def load_ledger():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER, encoding="utf-8"))
    return {"uploads": [], "refused": []}


def save_ledger(led):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    s = json.dumps(led, ensure_ascii=False, indent=1)
    s = re.sub(r"\{\n\s+([^{}]*?)\n\s+\}", lambda m: "{" + re.sub(r"\n\s+", " ", m.group(1)) + "}", s)   # one entry per line
    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write(s + "\n")


def desk():
    d = post.load_yaml(DESK) if os.path.exists(DESK) else {}
    return {"verified": bool(d.get("verified")), "per_day": int(d.get("per_day", 6)), "rolling": int(d.get("rolling", 8))}


def show_entries():
    """The newest show episode's sheet, from the `show` branch (empty when there is none or it cannot be read)."""
    r = subprocess.run(["curl", "-sf", "--max-time", "30", SHOW_SHEET], capture_output=True, text=True)
    try:
        return json.loads(r.stdout) if r.returncode == 0 else {}
    except ValueError:
        return {}


def build_entries():
    cfg = post.load_yaml(os.path.join(ROOT, "config.yml"))
    out = {}
    for fn in sorted(os.listdir(os.path.join(ROOT, "posts"))):
        if not re.match(r"ep\d+.*\.yml$", fn):
            continue
        ep = post.load_yaml(os.path.join(ROOT, "posts", fn))
        rank = ep.get("studio")
        langs = [lang for lang in CHANNEL if f"{lang}.youtube" in (ep.get("hold") or [])]
        if rank not in (1, 2) or not langs:
            continue
        try:
            found = yt_meta.entries(fn[:-4], cfg, langs)
        except SystemExit as e:
            print(f"skipped {fn}: {e}", file=sys.stderr)
            continue
        for k, e in found.items():
            e["rank"] = 1 + rank
            out[k] = e
    return out


def candidates():
    out = {}
    for k, e in show_entries().items():
        e["rank"] = 0 if e.get("kind") == "full" else 1
        out[k] = e
    out.update(build_entries())
    return out


def used_24h(led, t):
    return [u for u in led["uploads"] if utc(u["at"]) > t - datetime.timedelta(hours=24)]


def cmd_plan(args):
    t, led, d = now(), load_ledger(), desk()
    done = {u["key"] for u in led["uploads"]}
    today = t.astimezone(PT).date()
    tomorrow = today + datetime.timedelta(days=1)
    recent = sorted(utc(u["at"]) for u in used_24h(led, t))
    today_n = sum(1 for u in led["uploads"] if utc(u["at"]).astimezone(PT).date() == today)
    room = 10 ** 6 if d["verified"] else max(0, d["per_day"] - today_n)
    top = 3 if (d["verified"] or "--last" in args) else 2
    todo, later, other = [], [], []
    for k, e in sorted(candidates().items(), key=lambda kv: (kv[1]["rank"], kv[1]["utc"])):
        if k in done:
            continue
        if utc(e["utc"]).astimezone(PT).date() != tomorrow:
            other.append((k, e))
        else:
            (todo if e["rank"] <= top else later).append((k, e))
    take, left = todo[:room], todo[room:]
    for i, (k, e) in enumerate(take):                 # the 24-hour rule: when may the i-th new upload go?
        n = len(recent) + i
        e["wait"] = None if d["verified"] or n < d["rolling"] else recent[n - d["rolling"]] + datetime.timedelta(hours=24, minutes=2)
    order = sorted(range(len(take)), key=lambda i: (take[i][1]["wait"] is not None, take[i][1]["channel"] != CHANNEL["en"], i))
    take = [take[i] for i in order]                   # one channel at a time; the ones that must wait go last
    print(f"Now {pt(t)} PT. Our Studio uploads today (Pacific day): {today_n}"
          + ("" if d["verified"] else f" of {d['per_day']}") + f"; in the last 24 hours: {len(recent)}"
          + ("" if d["verified"] else f" (never more than {d['rolling']})") + ".")
    last = sorted(led.get("refused") or [], key=lambda r: r["at"])[-1:]
    if last:
        print(f"Last refusal by YouTube: {pt(utc(last[0]['at']))} PT on {last[0]['channel']}.")
    print("\nUPLOAD NOW, in this order:" if take else "\nNothing to upload now.")
    for i, (k, e) in enumerate(take, 1):
        print(f" {i:2}. {e['channel']:18} {k:24} public {e['date']} {e['time']:>8}  {e.get('kind', 'build')}"
              + ("  + thumbnail" if e.get("thumb") else "") + (f"  NOT BEFORE {pt(e['wait'])} PT" if e["wait"] else ""))
    if left or later:
        print("\nNO ROOM in today's limit" + ("" if top == 3 else " (the day's last round, --last, also takes `studio: 2` builds)") + ":")
        for k, e in left + later:
            print(f"     {e['channel']:18} {k:24} public {e['date']} {e['time']:>8}")
    late = [(k, e) for k, e in other if utc(e["utc"]) > t - datetime.timedelta(hours=24)]
    if late:
        print("\nNOT FOR TOMORROW (already due, or for a later day; the calls schedule for tomorrow only):")
        for k, e in late:
            print(f"     {e['channel']:18} {k:24} public {e['date']} {e['time']:>8}")
    if take:
        out = args[args.index("--out") + 1] if "--out" in args else f"/tmp/yt_sheet_{t.astimezone(PT):%m%d_%H%M}.json"
        sheet = {k: {x: v for x, v in e.items() if x not in ("wait", "rank")} for k, e in take}
        with open(out, "w", encoding="utf-8") as f:
            json.dump(sheet, f, ensure_ascii=False, indent=1)
        print(f"\nsheet: {out}   (push it to the `uploads` branch under this name, then run the Studio calls per video)")


def cmd_done(args):
    key, vid = args[0], args[1]
    led = load_ledger()
    if any(u["key"] == key for u in led["uploads"]):
        raise SystemExit(f"{key} is already in the ledger")
    lang = "ar" if re.search(r"-ar(-|$)", key) else "en"
    led["uploads"].append({"key": key, "id": vid, "channel": CHANNEL[lang], "at": now().strftime("%Y-%m-%dT%H:%MZ")})
    save_ledger(led)
    print(f"recorded {key} = {vid} ({CHANNEL[lang]})")


def cmd_refused(args):
    led = load_ledger()
    led.setdefault("refused", []).append({"at": now().strftime("%Y-%m-%dT%H:%MZ"), "channel": CHANNEL[args[0]]})
    save_ledger(led)
    print("recorded the refusal")


def cmd_release(args):
    sid = args[0]
    done = {u["key"] for u in load_ledger()["uploads"]}
    want = [f"{sid}-{lang}-{kind}" for lang in CHANNEL for kind in ("full", "short")]
    missing = [k for k in want if k not in done]
    if missing and "--force" not in args:
        raise SystemExit(f"not released: {', '.join(missing)} not uploaded yet (the shorts promise the full video)")
    p = os.path.join(ROOT, "posts", sid + ".yml")
    s = open(p, encoding="utf-8").read()
    new, n = re.subn(r"(?m)^hold:.*$", "hold: [en.youtube, ar.youtube]    # the TikTok and Instagram posts were released "
                     "after the YouTube uploads", s, count=1)
    if not n or new == s:
        raise SystemExit(f"nothing to change in posts/{sid}.yml")
    open(p, "w", encoding="utf-8").write(new)
    print(f"posts/{sid}.yml: only the YouTube targets stay on hold. Commit and push: post.yml schedules the rest.")


def cmd_check(args):
    """For the scheduled runs. Only the show is checked: its four uploads are expected every day, while a build
    marked for Studio may simply not have fitted in the day's limit."""
    t, led = now(), load_ledger()
    done = {u["key"] for u in led["uploads"]}
    lines = []
    for k, e in sorted(show_entries().items(), key=lambda kv: kv[1]["utc"]):
        due = utc(e["utc"])
        if k not in done and t - datetime.timedelta(hours=24) < due < t + datetime.timedelta(hours=3):
            lines.append(f"OVERDUE on YouTube: {k} ({e['channel']}), due {pt(due)} PT, not uploaded by the main chat")
    print("\n".join(lines) if lines else "YouTube desk: nothing overdue.")


def main():
    cmds = {"plan": cmd_plan, "done": cmd_done, "refused": cmd_refused, "release": cmd_release, "check": cmd_check}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        raise SystemExit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
