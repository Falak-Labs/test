"""Schedule every episode in posts/*.yml on Buffer (one Buffer account per language).

Each target (en.youtube, en.instagram, en.tiktok, ar.youtube, ...) is created once; its Buffer post id goes to
state/<episode>.json so a later run never posts it twice.  A target waits (no error) while its language has no
Buffer key yet, its video is not in media/ yet, or that platform is not connected in that Buffer account.
"""
import datetime as dt
import json
import os
import re
import sys
import time
from zoneinfo import ZoneInfo

import requests
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import Buffer, BufferError, unwrap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORMS = ("youtube", "instagram", "tiktok")
HASHTAG = re.compile(r"#[^\s#]+")
TAG_LIMIT = {"instagram": 5, "tiktok": 5, "youtube": 15}      # Instagram allows 5 per post; YouTube ignores all past 15
TEXT_LIMIT = {"instagram": 2200, "tiktok": 2200, "youtube": 5000}
PREVIEW = "--preview" in sys.argv
NOW = dt.datetime.now(dt.timezone.utc)
LOG = []


def log(msg):
    print(msg, flush=True)
    LOG.append(msg)


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_state(slug):
    p = os.path.join(ROOT, "state", slug + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"targets": {}}


def save_state(slug, st):
    os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
    with open(os.path.join(ROOT, "state", slug + ".json"), "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


_URLS = {}


def media_url(cfg, rel):
    """Public URL Buffer can fetch: GitHub Pages (video/mp4) once it serves the file, else raw.githubusercontent."""
    if rel in _URLS:
        return _URLS[rel]
    size = os.path.getsize(os.path.join(ROOT, rel))
    pages = cfg["pages_base"].rstrip("/") + "/" + rel
    deadline = time.time() + 240
    while True:
        try:
            r = requests.head(pages, allow_redirects=True, timeout=30)
            if r.status_code == 200 and int(r.headers.get("content-length", -1)) == size:
                _URLS[rel] = r.url
                return r.url
        except requests.RequestException:
            pass
        if time.time() > deadline:
            break
        time.sleep(20)
    raw = cfg["raw_base"].rstrip("/") + "/" + rel
    r = requests.head(raw, allow_redirects=False, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"{rel} is not reachable on Pages or raw GitHub ({r.status_code})")
    log(f"  note: GitHub Pages is not serving {rel}; using the raw GitHub link")
    _URLS[rel] = raw
    return raw


def parse_utc(s):
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def due_time(cfg, lang, day, last=None):
    """The episode's day at the language's posting time; never in the past, and at least `every_days` after the
    channel's previous post, so episodes that arrive late queue up one by one instead of all going out at once."""
    t = cfg["times"][lang]
    hh, mm = map(int, t["at"].split(":"))
    d = dt.date.fromisoformat(str(day))
    when = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=ZoneInfo(t["zone"]))
    earliest = NOW + dt.timedelta(minutes=15)
    if last is not None:
        earliest = max(earliest, last + dt.timedelta(days=int(cfg.get("every_days", 1))) - dt.timedelta(hours=2))
    while when < earliest:
        when += dt.timedelta(days=1)
    return when


def last_due_times(files):
    """Latest post time per target (en.youtube, ...) across everything already on Buffer."""
    last = {}
    for fn in files:
        for tgt, rec in load_state(fn[:-4])["targets"].items():
            when = parse_utc(rec.get("dueAt")) if rec.get("id") else None
            if when and (tgt not in last or when > last[tgt]):
                last[tgt] = when
    return last


class Account:
    """One Buffer account (one language): its channels by service, and the post input shape its API wants."""

    def __init__(self, key, lang):
        self.buf = Buffer(key, lang)
        self.all_channels = self.buf.channels()
        self.channels = {}
        for ch in self.all_channels:
            self.channels.setdefault(ch["service"].lower(), ch)
        mf = self.buf.field("Mutation", "createPost")
        self.in_type = unwrap(next(a for a in mf["args"] if a["name"] == "input")["type"])["name"]
        mode = self.buf.input_field(self.in_type, "mode")
        self.modes = self.buf.enum_values(unwrap(mode["type"])["name"]) if mode else []
        assets = self.buf.input_field(self.in_type, "assets")
        t = assets["type"]
        while t["kind"] == "NON_NULL":
            t = t["ofType"]
        self.assets_list = t["kind"] == "LIST"
        self.asset_type = unwrap(assets["type"])["name"]
        self.post_types = self.buf.enum_values("PostType")

    def pick(self, cfg, lang, platform):
        """The connected channel for this platform whose name matches config.yml `channels` (so an English post can
        never go to an Arabic account that happens to be connected to the same Buffer login). (channel, problem)"""
        want = ((cfg.get("channels") or {}).get(lang) or {}).get(platform) or []
        mine = [ch for ch in self.all_channels if ch["service"].lower() == platform]
        if not mine:
            return None, f"{platform} is not connected in the {lang} Buffer account"
        if not want:
            return mine[0], None
        for ch in mine:
            hay = " ".join(str(ch.get(k) or "") for k in ("name", "displayName")).lower()
            if any(w.lower() in hay for w in want):
                return ch, None
        names = ", ".join(str(ch.get("displayName") or ch.get("name")) for ch in mine)
        return None, f"the {platform} account connected to the {lang} Buffer login is '{names}', not the {lang} one"

    def video_assets(self, url):
        names = {f["name"] for f in self.buf.type(self.asset_type).get("inputFields") or []}
        one = {"video": {"url": url}} if "video" in names else {"videos": [{"url": url}]}
        return [one] if self.assets_list else one

    def reel(self):
        return next((v for v in self.post_types if v.lower() in ("reel", "reels")), "reel")


def caption_for(cfg, ep, lang, platform):
    """text + call to action, then (YouTube only) the keyword line, then this platform's hashtags."""
    d = ep[lang]
    if "caption" in d:                                    # old one-caption format
        c = d["caption"].strip()
        return c + "\n\n#Shorts" if platform == "youtube" else c
    body = d["text"].strip()
    cta = (cfg.get("cta") or {}).get(lang) or {}
    line = cta.get(platform) or cta.get("default")
    if line and d.get("next"):
        body += "\n" + line.format(next=d["next"])
    parts = [body]
    if platform == "youtube" and d.get("seo"):
        parts.append(d["seo"].strip())
    tags = d.get("tags") or {}
    tags = tags if isinstance(tags, dict) else {"default": tags}
    t = (tags.get(platform) or tags.get("default") or "").strip()
    if platform == "youtube":
        t = (t + " #Shorts").strip()
    if t:
        parts.append(t)
    return "\n\n".join(parts)


def check_post(platform, title, text):
    """Problems that would make the platform reject the post or drop its hashtags."""
    issues = []
    n = len(HASHTAG.findall(text))
    if n > TAG_LIMIT[platform]:
        issues.append(f"{n} hashtags (limit {TAG_LIMIT[platform]})")
    if len(text) > TEXT_LIMIT[platform]:
        issues.append(f"caption is {len(text)} characters (limit {TEXT_LIMIT[platform]})")
    if platform == "youtube":
        if not title or len(title) > 100:
            issues.append(f"title is {len(title or '')} characters (1-100)")
        if "<" in title or ">" in title:
            issues.append("title contains < or >")
    return issues


def preview(cfg, files):
    """python scripts/post.py --preview : every caption and post time, without touching Buffer."""
    last = last_due_times(files)
    for fn in files:
        ep = load_yaml(os.path.join(ROOT, "posts", fn))
        slug, st = fn[:-4], load_state(fn[:-4])
        for lang in ("en", "ar"):
            if lang not in ep:
                continue
            for platform in PLATFORMS:
                tgt = f"{lang}.{platform}"
                if st["targets"].get(tgt, {}).get("id"):
                    print(f"== {slug} {tgt}: already on Buffer ({st['targets'][tgt].get('status')})\n")
                    continue
                when = due_time(cfg, lang, ep["date"], last.get(tgt))
                last[tgt] = when
                text, title = caption_for(cfg, ep, lang, platform), ep[lang].get("title", "")
                issues = check_post(platform, title, text)
                print(f"== {slug} {tgt}: {when.strftime('%a %d %b %H:%M %Z')} ({len(text)} chars, "
                      f"{len(HASHTAG.findall(text))} hashtags)" + (f"  PROBLEM: {'; '.join(issues)}" if issues else ""))
                if platform == "youtube":
                    print("title: " + title)
                print(text + "\n")


def main():
    cfg = load_yaml(os.path.join(ROOT, "config.yml"))
    files = sorted(f for f in os.listdir(os.path.join(ROOT, "posts")) if f.endswith(".yml"))
    if PREVIEW:
        return preview(cfg, files)
    test_only = bool(cfg.get("test_only"))
    last = last_due_times(files)
    burst_slots = {}
    held = set()
    accounts = {}
    for lang, var in cfg["keys"].items():
        key = os.environ.get(var, "").strip()
        if not key:
            log(f"{lang}: no Buffer key yet (secret {var}) - its posts wait")
            continue
        try:
            accounts[lang] = Account(key, lang)
            log(f"{lang}: Buffer channels: " + ", ".join(f"{s} ({c['displayName'] or c['name']})"
                                                        for s, c in accounts[lang].channels.items()))
        except BufferError as e:
            log(f"{lang}: Buffer error: {e}")
    for fn in files:
        ep = load_yaml(os.path.join(ROOT, "posts", fn))
        slug = fn[:-4]
        st = load_state(slug)
        now_targets = set(ep.get("now") or [])
        for lang in ("en", "ar"):
            if lang not in accounts or lang not in ep:
                continue
            if (cfg.get("hold") or {}).get(lang) and not set(ep.get("now") or []) & {f"{lang}.{p}" for p in PLATFORMS}:
                if lang not in held:
                    log(f"{lang}: on hold in config.yml - nothing is posted for this language")
                    held.add(lang)
                continue
            acc = accounts[lang]
            video = ep["video"].get(lang)
            for platform in PLATFORMS:
                tgt = f"{lang}.{platform}"
                done = st["targets"].get(tgt, {})
                if done.get("id"):
                    continue
                if test_only and tgt not in now_targets:
                    continue
                if not video or not os.path.exists(os.path.join(ROOT, video)):
                    log(f"{slug} {tgt}: waiting for the video {video}")
                    break
                ch, problem = acc.pick(cfg, lang, platform)
                if not ch:
                    log(f"{slug} {tgt}: {problem} - skipped")
                    continue
                if done.get("tries", 0) >= 3:
                    log(f"{slug} {tgt}: failed 3 times, not retrying (last error: {done.get('error')})")
                    continue
                text = caption_for(cfg, ep, lang, platform)
                issues = check_post(platform, ep[lang].get("title", ""), text)
                if issues:
                    log(f"{slug} {tgt}: not posted, fix posts/{fn}: " + "; ".join(issues))
                    continue
                inp = {"channelId": ch["id"], "text": text, "schedulingType": "automatic",
                       "assets": acc.video_assets(media_url(cfg, video))}
                if tgt in now_targets and "shareNow" in acc.modes:
                    inp["mode"] = "shareNow"
                    when = None
                else:
                    burst = (cfg.get("burst") or {}).get(lang)
                    if tgt in now_targets:
                        when = NOW + dt.timedelta(minutes=3)
                    elif burst:          # catch-up: one episode every gap minutes, starting first minutes from now
                        slot = burst_slots.setdefault(lang, {}).setdefault(slug, len(burst_slots[lang]))
                        when = max(NOW + dt.timedelta(minutes=burst.get("first", 6) + burst.get("gap", 5) * slot),
                                   dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=2))
                    else:
                        when = due_time(cfg, lang, ep["date"], last.get(tgt))
                    inp["mode"] = "customScheduled"
                    inp["dueAt"] = when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                if platform == "youtube":
                    inp["metadata"] = {"youtube": {"title": ep[lang]["title"][:100], "categoryId": str(cfg["youtube"]["categoryId"]),
                                                   "madeForKids": bool(cfg["youtube"].get("madeForKids", False)),
                                                   "notifySubscribers": True}}
                elif platform == "instagram":
                    inp["metadata"] = {"instagram": {"type": acc.reel(), "shouldShareToFeed": True}}
                try:
                    post = acc.buf.create_post(inp)
                    st["targets"][tgt] = {"id": post.get("id"), "channel": ch["id"], "service": platform,
                                          "status": post.get("status"), "dueAt": post.get("dueAt") or inp.get("dueAt"),
                                          "mode": inp["mode"], "created": NOW.isoformat(timespec="seconds")}
                    last[tgt] = when or NOW
                    shown = when.strftime("%a %d %b %H:%M %Z") if when else "now"
                    log(f"{slug} {tgt}: scheduled ({shown}) id {post.get('id')}")
                except (BufferError, requests.RequestException, RuntimeError) as e:
                    st["targets"][tgt] = {"error": str(e)[:600], "tries": done.get("tries", 0) + 1,
                                          "at": NOW.isoformat(timespec="seconds")}
                    log(f"{slug} {tgt}: FAILED: {str(e)[:300]}")
        save_state(slug, st)
    with open(os.path.join(ROOT, "state", "last-run.md"), "w", encoding="utf-8") as f:
        f.write(f"# Last posting run {NOW.isoformat(timespec='seconds')}\n\n" + "\n".join(f"- {m}" for m in LOG) + "\n")


if __name__ == "__main__":
    main()
