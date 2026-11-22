#!/usr/bin/env python3
"""Yallah Say: give one day's videos their posting times.

usage: python3 yallah/plan_day.py <YYYY-MM-DD> <short> [<short> <short>] [--long <slug>] [--write] [--force]

  YYYY-MM-DD   the day, as people in each country see it (each dialect posts on its own local day)
  short        queue slugs of that day's Shorts in posting order (yallah/queue/<slug>.json); up to one per slot
  --long       queue slug of the day's long lesson (YouTube only)
  --write      save the times into the queue files (without it, only the plan is printed)
  --force      also move a video whose posts were already handed to Buffer

For every dialect a queue file holds, this sets
  at          the local slot from yallah/config.json with its UTC offset, worked out from the country's time zone
              (Morocco is on GMT all year since 20 Sep 2026; Palestine is +02:00 in winter and +03:00 in summer)
  platforms   what Buffer posts (post_due.py hands these over just before `at`)
  studio      what goes up through YouTube Studio, scheduled for the same time (YOUTUBE_STUDIO_UPLOAD.md)
The route of each platform is config.json's accounts.<dialect>.routes. Buffer's free plan sends 2 YouTube posts per
channel in any 24 hours: with "buffer_limits": {"youtube": 2} only the first and the last Short of the day use Buffer
for YouTube and the others wait for the Studio route."""
import datetime as dt
import json
import os
import sys
import zoneinfo

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
PLATFORMS = ("youtube", "instagram", "tiktok")
STUDIO_ZONE = zoneinfo.ZoneInfo("America/Los_Angeles")      # the owner's browser: Studio shows and takes Pacific time

args = sys.argv[1:]
write, force = "--write" in args, "--force" in args
long_slug = args[args.index("--long") + 1] if "--long" in args else None
pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--long")]
if not pos:
    sys.exit(__doc__)
try:
    day = dt.date.fromisoformat(pos[0])
except ValueError:
    sys.exit(__doc__)
shorts = pos[1:]
NOW = dt.datetime.now(dt.timezone.utc)
problems, changed = [], {}


def load(slug):
    p = os.path.join(HERE, "queue", slug + ".json")
    if not os.path.exists(p):
        problems.append(f"{slug}: yallah/queue/{slug}.json does not exist")
        return None
    ep = json.load(open(p, encoding="utf-8"))
    if ep.setdefault("slug", slug) != slug:
        problems.append(f"{slug}: the file says its slug is {ep['slug']}; post_due.py keeps its records under that name")
    return ep


def handed(slug, lang):
    p = os.path.join(HERE, "state", slug + ".json")
    if not os.path.exists(p):
        return []
    return [t for t, v in json.load(open(p, encoding="utf-8")).get("targets", {}).items() if t.startswith(lang + ".") and v.get("id")]


def stamp(slug, ep, lang, hhmm, buffer_platforms, studio_platforms):
    ac, d = CFG["accounts"][lang], ep[lang]
    zone = zoneinfo.ZoneInfo(ac["zone"])
    h, m = (int(x) for x in hhmm.split(":"))
    at = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=zone)
    iso = at.isoformat(timespec="seconds")
    was = handed(slug, lang)
    note = ""
    if was and not force:
        problems.append(f"{slug} {lang}: already handed to Buffer ({', '.join(was)}); left as it is")
        return
    if at < NOW:
        note = "  (this time has passed: it would go out at once)"
    print(f"{slug:8s} {lang}: {at.strftime('%a %d %b %H:%M')} {ac['zone'].split('/')[1]} ({iso[-6:]}) = {at.astimezone(dt.timezone.utc).strftime('%H:%M')} UTC"
          f" = {at.astimezone(STUDIO_ZONE).strftime('%a %I:%M %p')} Pacific | Buffer: {', '.join(buffer_platforms) or 'nothing'}"
          f" | Studio: {', '.join(studio_platforms) or 'nothing'}{note}")
    d["at"], d["platforms"] = iso, list(buffer_platforms)
    if studio_platforms:
        d["studio"] = list(studio_platforms)
    else:
        d.pop("studio", None)
    changed[slug] = ep


for lang, ac in CFG["accounts"].items():
    slots, routes, limits = ac.get("slots", []), ac.get("routes", {}), ac.get("buffer_limits", {})
    if len(shorts) > len(slots):
        problems.append(f"{lang}: {len(shorts)} Shorts for {len(slots)} slots a day; the extra ones get no time")
    todo = shorts[:len(slots)]
    for k, slug in enumerate(todo):
        ep = changed.get(slug) or load(slug)
        if not ep or not ep.get(lang):
            continue
        buf, stu = [], []
        for p in PLATFORMS:
            r = routes.get(p, "buffer")
            if r == "buffer" and p in limits and limits[p] < len(todo):
                # keep Buffer's daily allowance for the first and the last Short, as far apart as the day allows
                keep = sorted({0, len(todo) - 1})[:limits[p]] if limits[p] >= 2 else [len(todo) - 1][:limits[p]]
                r = "buffer" if k in keep else "studio"
            (buf if r == "buffer" else stu).append(p)
        stamp(slug, ep, lang, slots[k], buf, stu)
    if long_slug:
        ep = changed.get(long_slug) or load(long_slug)
        if ep and ep.get(lang):
            if not ac.get("long_slot"):
                problems.append(f"{lang}: no long_slot in config.json")
            else:
                ep["kind"] = "long"
                stamp(long_slug, ep, lang, ac["long_slot"], [], ["youtube"])      # a long lesson never goes through Buffer

for p in problems:
    print("NOTE: " + p)
if write:
    for slug, ep in changed.items():
        with open(os.path.join(HERE, "queue", slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(ep, f, ensure_ascii=False, indent=1)
            f.write("\n")
    print(f"saved {len(changed)} queue file(s)")
else:
    print("nothing saved (add --write)")
