"""Schedule every episode in posts/*.yml on Buffer (one Buffer account per language).

Each target (en.youtube, en.instagram, en.tiktok, ar.youtube, ...) is created once; its Buffer post id goes to
state/<episode>.json so a later run never posts it twice.  A target waits (no error) while its language has no
Buffer key yet, its video is not in media/ yet, or that platform is not connected in that Buffer account.
"""
import datetime as dt
import json
import os
import sys
import time
from zoneinfo import ZoneInfo

import requests
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import Buffer, BufferError, unwrap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORMS = ("youtube", "instagram", "tiktok")
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


def due_time(cfg, lang, day):
    t = cfg["times"][lang]
    hh, mm = map(int, t["at"].split(":"))
    d = dt.date.fromisoformat(str(day))
    when = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=ZoneInfo(t["zone"]))
    while when.astimezone(dt.timezone.utc) < NOW + dt.timedelta(minutes=15):
        when += dt.timedelta(days=1)
    return when


class Account:
    """One Buffer account (one language): its channels by service, and the post input shape its API wants."""

    def __init__(self, key, lang):
        self.buf = Buffer(key, lang)
        self.channels = {}
        for ch in self.buf.channels():
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

    def video_assets(self, url):
        names = {f["name"] for f in self.buf.type(self.asset_type).get("inputFields") or []}
        one = {"video": {"url": url}} if "video" in names else {"videos": [{"url": url}]}
        return [one] if self.assets_list else one

    def reel(self):
        return next((v for v in self.post_types if v.lower() in ("reel", "reels")), "reel")


def caption_for(ep, lang, platform):
    c = ep[lang]["caption"].strip()
    return c + "\n\n#Shorts" if platform == "youtube" else c


def main():
    cfg = load_yaml(os.path.join(ROOT, "config.yml"))
    test_only = bool(cfg.get("test_only"))
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
    files = sorted(f for f in os.listdir(os.path.join(ROOT, "posts")) if f.endswith(".yml"))
    for fn in files:
        ep = load_yaml(os.path.join(ROOT, "posts", fn))
        slug = fn[:-4]
        st = load_state(slug)
        now_targets = set(ep.get("now") or [])
        for lang in ("en", "ar"):
            if lang not in accounts or lang not in ep:
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
                ch = acc.channels.get(platform)
                if not ch:
                    log(f"{slug} {tgt}: {platform} is not connected in the {lang} Buffer account - skipped")
                    continue
                if done.get("tries", 0) >= 3:
                    log(f"{slug} {tgt}: failed 3 times, not retrying (last error: {done.get('error')})")
                    continue
                inp = {"channelId": ch["id"], "text": caption_for(ep, lang, platform), "schedulingType": "automatic",
                       "assets": acc.video_assets(media_url(cfg, video))}
                if tgt in now_targets and "shareNow" in acc.modes:
                    inp["mode"] = "shareNow"
                    when = None
                else:
                    when = NOW + dt.timedelta(minutes=3) if tgt in now_targets else due_time(cfg, lang, ep["date"])
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
