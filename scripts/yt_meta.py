"""Upload sheet for YouTube Studio: what each build's Short needs, as JSON.
    python3 scripts/yt_meta.py <slug> [<slug> ...] > meta.json        (slug = a posts/<slug>.yml)
One entry per language, keyed "<slug>-<lang>": the video's raw link on main, the channel, the title and the description
post.py would have sent to YouTube, the language, and the post's slot in Pacific time (the Studio browser's time zone).
The steps that use it are in YOUTUBE_STUDIO_UPLOAD.md."""
import json
import os
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402

CHANNELS = {"en": ("Congrats Engineer", "UCDkfxHa7q5Ea0OoiSSi8DHA", "English"),
            "ar": ("Kef Tenbeni", "UC8qDuZpMDQXRrowaNp29vow", "Arabic")}
PT = ZoneInfo("America/Los_Angeles")


def main():
    cfg = post.load_yaml(os.path.join(post.ROOT, "config.yml"))
    out = {}
    for slug in sys.argv[1:]:
        ep = post.load_yaml(os.path.join(post.ROOT, "posts", slug + ".yml"))
        for lang, (channel, cid, language) in CHANNELS.items():
            if lang not in ep or not ep["video"].get(lang):
                continue
            when = post.fixed_time(ep, "youtube", lang)
            if when is None:
                raise SystemExit(f"{slug} {lang}: no at: time in the posts file")
            t = when.astimezone(PT)
            title = ep[lang]["title"][:100]
            desc = post.caption_for(cfg, ep, lang, "youtube")
            issues = post.check_post("youtube", title, desc)
            if issues:
                raise SystemExit(f"{slug} {lang}: {'; '.join(issues)}")
            out[f"{slug}-{lang}"] = {
                "url": cfg["raw_base"].rstrip("/") + "/" + ep["video"][lang], "channel": channel, "channel_id": cid,
                "language": language, "title": title, "desc": desc, "date": f"{t:%b} {t.day}, {t.year}",
                "time": f"{t.hour % 12 or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}", "utc": when.strftime("%Y-%m-%dT%H:%MZ")}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
