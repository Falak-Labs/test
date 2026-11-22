"""Yallah Say: send each queued video to Buffer only a few minutes before it should go out.

The schedule lives here, in yallah/queue/<slug>.json, not in Buffer: Buffer's free plan holds at most 10 scheduled posts
per channel and 3,000 API requests a month, so a post is handed over when its time is near and is published a few
(random) minutes later.  One Buffer account per dialect; its key is an Actions secret named in yallah/config.json.

  python3 yallah/post_due.py --check      is anything due? (standard library only; sets the step output "due")
  python3 yallah/post_due.py --preview    every queued post, its time and caption, without touching Buffer
  python3 yallah/post_due.py              send what is due (needs requests and pyyaml, and the keys in the environment)

queue file:  {"slug": "ep01", "cover_ms": 2000,
              "ma": {"video": "<https url, or a path in this repo>", "at": "2026-11-21T13:00:00+01:00",
                     "title": "<YouTube title>", "text": "<caption>", "tags": {"default": "#a #b", "youtube": "#c"}},
              "pa": {...}}
Nothing is sent while "enabled" is false in yallah/config.json."""
import datetime as dt
import json
import os
import random
import re
import sys

HERE = os.environ.get("YALLAH_DIR") or os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
PLATFORMS = ("youtube", "instagram", "tiktok")
HASHTAG = re.compile(r"#[^\s#]+")
TAG_LIMIT = {"instagram": 5, "tiktok": 5, "youtube": 15}
TEXT_LIMIT = {"instagram": 2200, "tiktok": 2200, "youtube": 5000}
NOW = dt.datetime.now(dt.timezone.utc)
LOG = []


def log(msg):
    print(msg, flush=True)
    LOG.append(msg)


def load_state(slug):
    p = os.path.join(HERE, "state", slug + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"targets": {}}


def save_state(slug, st):
    os.makedirs(os.path.join(HERE, "state"), exist_ok=True)
    with open(os.path.join(HERE, "state", slug + ".json"), "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


def queue():
    d = os.path.join(HERE, "queue")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if fn.endswith(".json"):
            ep = json.load(open(os.path.join(d, fn), encoding="utf-8"))
            ep.setdefault("slug", fn[:-5])
            yield ep


def caption(d, platform):
    tags = d.get("tags") or {}
    tags = tags if isinstance(tags, dict) else {"default": tags}
    t = (tags.get(platform) or tags.get("default") or "").strip()
    if platform == "youtube":
        t = (t + " #Shorts").strip()
    return d["text"].strip() + ("\n\n" + t if t else "")


def problems(platform, title, text):
    out, n = [], len(HASHTAG.findall(text))
    if n > TAG_LIMIT[platform]:
        out.append(f"{n} hashtags (limit {TAG_LIMIT[platform]})")
    if len(text) > TEXT_LIMIT[platform]:
        out.append(f"caption is {len(text)} characters (limit {TEXT_LIMIT[platform]})")
    if platform == "youtube" and (not title or len(title) > 100 or "<" in title or ">" in title):
        out.append("YouTube title must be 1-100 characters without < or >")
    return out


def video_url(v):
    return v if v.startswith("http") else CFG["raw_base"].rstrip("/") + "/" + v.lstrip("/")


def go_time(slug, tgt, at):
    """When Buffer should publish: the planned time, never sooner than the shortest delay from now, plus a few random
    minutes (the same for a given post on every run, different for each platform)."""
    lo, hi = CFG.get("delay_minutes", [4, 11])
    base = max(at, NOW + dt.timedelta(minutes=lo))
    return base + dt.timedelta(seconds=random.Random(slug + tgt).randrange(0, max(1, (hi - lo) * 60)))


def items(all_of_them=False):
    """(episode, lang, platform, target, planned time, state) for every post not yet on Buffer; only the due ones unless asked."""
    lead = dt.timedelta(minutes=CFG.get("lead_minutes", 20))
    for ep in queue():
        st = load_state(ep["slug"])
        for lang in CFG["accounts"]:
            d = ep.get(lang)
            if not d or not d.get("at") or not d.get("video"):
                continue
            at = dt.datetime.fromisoformat(d["at"])
            if at.tzinfo is None:
                raise SystemExit(f"{ep['slug']} {lang}: 'at' needs a UTC offset, like 2026-11-21T13:00:00+01:00")
            if ep.get("kind") == "long":
                continue        # a long lesson goes up through YouTube Studio, never through Buffer
            for platform in (d["platforms"] if "platforms" in d else PLATFORMS):      # an empty list means nothing through Buffer
                tgt = f"{lang}.{platform}"
                done = st["targets"].get(tgt, {})
                if done.get("id") or done.get("tries", 0) >= 3:
                    continue
                if all_of_them or NOW >= at - lead:
                    yield ep, lang, platform, tgt, at, st


def check():
    n = sum(1 for _ in items()) if CFG.get("enabled") else 0
    print(f"{n} post(s) due" + ("" if CFG.get("enabled") else " (posting is switched off in yallah/config.json)"))
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"due={'true' if n else 'false'}\n")


def preview():
    n = 0
    for ep, lang, platform, tgt, at, st in items(all_of_them=True):
        d, n = ep[lang], n + 1
        text, when = caption(d, platform), go_time(ep["slug"], tgt, at)
        bad = problems(platform, d.get("title", ""), text)
        print(f"== {ep['slug']} {tgt}: planned {at.isoformat()} -> Buffer would publish about {when.astimezone(at.tzinfo).strftime('%a %d %b %H:%M')}"
              f" | handed over from {(at - dt.timedelta(minutes=CFG.get('lead_minutes', 20))).astimezone(dt.timezone.utc).strftime('%H:%M UTC')}"
              + (f"  PROBLEM: {'; '.join(bad)}" if bad else ""))
        if platform == "youtube":
            print("title: " + d.get("title", ""))
        print(f"video: {video_url(d['video'])}\n{text}\n")
    print(f"{n} post(s) waiting; posting is {'ON' if CFG.get('enabled') else 'OFF'}")


def send():
    if not CFG.get("enabled"):
        return log("posting is switched off in yallah/config.json: nothing sent")
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import requests
    from buffer import Buffer, BufferError
    from post import Account            # the same Buffer input shapes the other series posts with every day

    accounts, touched = {}, {}
    for ep, lang, platform, tgt, at, st in items():
        slug, d, ac = ep["slug"], ep[lang], CFG["accounts"][lang]
        if lang not in accounts:
            key = os.environ.get(ac["secret"], "").strip()
            if not key:
                log(f"{lang}: no Buffer key yet (secret {ac['secret']}): its posts wait")
                accounts[lang] = None
            else:
                try:
                    accounts[lang] = Account(key, lang)
                    log(f"{lang}: Buffer channels: " + ", ".join(f"{c['service']} ({c.get('displayName') or c.get('name')})" for c in accounts[lang].all_channels))
                except (BufferError, requests.RequestException) as e:
                    log(f"{lang}: Buffer error: {str(e)[:300]}")
                    accounts[lang] = None
        acc = accounts[lang]
        if not acc:
            continue
        done = st["targets"].get(tgt, {})
        ch, problem = acc.pick({"channels": {lang: ac["channels"]}}, lang, platform)
        if not ch:
            log(f"{slug} {tgt}: {problem}: skipped")
            continue
        text = caption(d, platform)
        bad = problems(platform, d.get("title", ""), text)
        if bad:
            log(f"{slug} {tgt}: not posted, fix yallah/queue/{slug}.json: " + "; ".join(bad))
            continue
        when = go_time(slug, tgt, at)
        inp = {"channelId": ch["id"], "text": text, "schedulingType": "automatic", "mode": "customScheduled",
               "dueAt": when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
               "assets": acc.video_assets(video_url(d["video"]), platform, ep.get("cover_ms", 0))}
        if platform == "youtube":
            inp["metadata"] = {"youtube": {"title": d["title"][:100], "categoryId": str(CFG["youtube"]["categoryId"]),
                                           "madeForKids": bool(CFG["youtube"].get("madeForKids", False)), "notifySubscribers": True}}
        elif platform == "instagram":
            inp["metadata"] = {"instagram": {"type": acc.reel(), "shouldShareToFeed": True}}
        try:
            post = acc.buf.create_post(inp)
            st["targets"][tgt] = {"id": post.get("id"), "channel": ch["id"], "service": platform, "status": post.get("status"),
                                  "dueAt": post.get("dueAt") or inp["dueAt"], "planned": at.isoformat(), "created": NOW.isoformat(timespec="seconds")}
            log(f"{slug} {tgt}: handed to Buffer, goes out {when.astimezone(at.tzinfo).strftime('%a %d %b %H:%M')} (id {post.get('id')})")
        except (BufferError, requests.RequestException, RuntimeError) as e:
            st["targets"][tgt] = {"error": str(e)[:600], "tries": done.get("tries", 0) + 1, "at": NOW.isoformat(timespec="seconds")}
            log(f"{slug} {tgt}: FAILED: {str(e)[:300]}")
        touched[slug] = st
    for slug, st in touched.items():
        save_state(slug, st)
    for lang, acc in accounts.items():
        if acc:
            log(f"{lang}: {acc.buf.calls} Buffer API requests this run; allowance left: {Buffer.quota.get(lang, 'not reported')}")
    if touched:
        with open(os.path.join(HERE, "state", "last-run.md"), "w", encoding="utf-8") as f:
            f.write(f"# Last Yallah Say posting run {NOW.isoformat(timespec='seconds')}\n\n" + "\n".join(f"- {m}" for m in LOG) + "\n")


def channels():
    """Which channels each Buffer key sees and which one every platform would post to. Posts nothing; works while
    posting is switched off. The answer is saved in yallah/state/channels.md (names only, never a key)."""
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import requests
    from buffer import BufferError
    from post import Account
    for lang, ac in CFG["accounts"].items():
        key = os.environ.get(ac["secret"], "").strip()
        if not key:
            log(f"{lang}: secret {ac['secret']} is not set yet")
            continue
        try:
            acc = Account(key, lang)
        except (BufferError, requests.RequestException, RuntimeError) as e:
            log(f"{lang}: Buffer error: {str(e)[:300]}")
            continue
        seen = ", ".join(f"{c['service']} ({c.get('displayName') or c.get('name')})" for c in acc.all_channels)
        log(f"{lang}: Buffer sees {seen or 'no channels'}")
        for platform in PLATFORMS:
            ch, problem = acc.pick({"channels": {lang: ac["channels"]}}, lang, platform)
            log(f"{lang}.{platform}: " + (f"will post to {ch.get('displayName') or ch.get('name')}" if ch else f"NOT READY: {problem}"))
        # where every post already handed to this account stands now: scheduled, sent (with its link) or failed
        ids = {}
        for ep in queue():
            for tgt, t in load_state(ep["slug"])["targets"].items():
                if t.get("id") and tgt.split(".")[0] == lang:
                    ids[t["id"]] = f"{ep['slug']} {tgt}"
        if ids:
            try:
                seen = {}
                for org in sorted({c["organizationId"] for c in acc.all_channels}):
                    for post in acc.buf.posts(org, ["sent", "error", "scheduled", "sending", "draft"]):
                        seen[post.get("id")] = post
                for pid, name in ids.items():
                    post = seen.get(pid)
                    if not post:
                        log(f"{name}: not in Buffer's lists (id {pid})")
                        continue
                    link = str(post.get("externalLink") or post.get("serviceLink") or "").split("?")[0]
                    err = post.get("errorMessage") or post.get("error") or ""
                    log(f"{name}: {post.get('status')}"
                        + (f", sent {post.get('sentAt')}" if post.get("sentAt") else f", due {post.get('dueAt')}")
                        + (f", {link}" if link else "") + (f", ERROR {str(err)[:240]}" if err else ""))
            except (BufferError, requests.RequestException, RuntimeError, KeyError, TypeError) as e:
                log(f"{lang}: could not read post status: {str(e)[:300]}")
    os.makedirs(os.path.join(HERE, "state"), exist_ok=True)
    with open(os.path.join(HERE, "state", "channels.md"), "w", encoding="utf-8") as f:
        f.write(f"# Yallah Say Buffer channels, checked {NOW.isoformat(timespec='seconds')}\n\n" + "\n".join(f"- {m}" for m in LOG) + "\n")


if __name__ == "__main__":
    check() if "--check" in sys.argv else preview() if "--preview" in sys.argv else channels() if "--channels" in sys.argv else send()
