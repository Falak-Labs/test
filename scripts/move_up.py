"""Move queued posts of one language up to the next hour, in episode order (no duplicates: edits the Buffer posts).

    python scripts/move_up.py en [first_minutes=5] [gap_minutes=10]

Each episode's posts get the same time; episode N goes out first_minutes + (N-1)*gap_minutes from now.  The edit
resends the post's caption, video, title and settings, so nothing is lost whatever Buffer does with missing fields.
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
from buffer import BufferError  # noqa: E402


def main():
    lang = sys.argv[1]
    first = float(sys.argv[2]) if len(sys.argv) > 2 else 5
    gap = float(sys.argv[3]) if len(sys.argv) > 3 else 10
    cfg = post.load_yaml(os.path.join(post.ROOT, "config.yml"))
    key = os.environ.get(cfg["keys"][lang], "").strip()
    if not key:
        sys.exit(f"no Buffer key for {lang}")
    acc = post.Account(key, lang)
    files = sorted(f for f in os.listdir(os.path.join(post.ROOT, "posts")) if f.endswith(".yml"))
    slot = 0
    for fn in files:
        ep = post.load_yaml(os.path.join(post.ROOT, "posts", fn))
        slug, st = fn[:-4], post.load_state(fn[:-4])
        todo = [p for p in post.PLATFORMS
                if st["targets"].get(f"{lang}.{p}", {}).get("id")
                and st["targets"][f"{lang}.{p}"].get("status") not in ("sent", "sending")]
        if not todo:
            continue
        when = post.NOW + dt.timedelta(minutes=first + gap * slot)
        slot += 1
        due = when.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        for platform in todo:
            tgt = f"{lang}.{platform}"
            rec = st["targets"][tgt]
            inp = {"id": rec["id"], "text": post.caption_for(cfg, ep, lang, platform), "schedulingType": "automatic",
                   "assets": acc.video_assets(post.media_url(cfg, ep["video"][lang])), "mode": "customScheduled",
                   "dueAt": due}
            if platform == "youtube":
                inp["metadata"] = {"youtube": {"title": ep[lang]["title"][:100], "categoryId": str(cfg["youtube"]["categoryId"]),
                                               "madeForKids": bool(cfg["youtube"].get("madeForKids", False)),
                                               "notifySubscribers": True}}
            elif platform == "instagram":
                inp["metadata"] = {"instagram": {"type": acc.reel(), "shouldShareToFeed": True}}
            try:
                p = acc.buf.edit_post(inp)
                rec.update({"dueAt": p.get("dueAt") or due, "status": p.get("status") or rec.get("status"),
                            "mode": "customScheduled", "moved": post.NOW.isoformat(timespec="seconds")})
                post.log(f"{slug} {tgt}: moved to {when.astimezone(dt.timezone.utc):%H:%M} UTC (status {p.get('status')})")
            except (BufferError, RuntimeError) as e:
                post.log(f"{slug} {tgt}: NOT moved: {str(e)[:300]}")
        post.save_state(slug, st)
    with open(os.path.join(post.ROOT, "state", "last-run.md"), "w", encoding="utf-8") as f:
        f.write(f"# Move-up run {post.NOW.isoformat(timespec='seconds')}\n\n" + "\n".join(f"- {m}" for m in post.LOG) + "\n")


if __name__ == "__main__":
    main()
