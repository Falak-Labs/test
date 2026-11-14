"""Move queued posts up, platform by platform (edits the Buffer posts: no duplicates).

    python scripts/move_up.py <lang> <platforms in order> <first_minutes> <gap_minutes>
    python scripts/move_up.py en youtube,instagram 2 1   -> every YouTube post first, 1 min apart, then Instagram

Only posts Buffer still lists as scheduled are touched.  The edit resends caption, video, title and settings.
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
from buffer import BufferError  # noqa: E402


def main():
    lang, order = sys.argv[1], sys.argv[2].split(",")
    first, gap = float(sys.argv[3]), float(sys.argv[4])
    cfg = post.load_yaml(os.path.join(post.ROOT, "config.yml"))
    key = os.environ.get(cfg["keys"][lang], "").strip()
    if not key:
        sys.exit(f"no Buffer key for {lang}")
    acc = post.Account(key, lang)
    queued = set()
    for org in {ch["organizationId"] for ch in acc.all_channels}:
        queued |= {n.get("id") for n in acc.buf.posts(org, ["scheduled"])}
    post.log(f"{len(queued)} posts still queued in Buffer")
    files = sorted(f for f in os.listdir(os.path.join(post.ROOT, "posts")) if f.endswith(".yml"))
    eps = [(fn[:-4], post.load_yaml(os.path.join(post.ROOT, "posts", fn))) for fn in files]
    states = {slug: post.load_state(slug) for slug, _ in eps}
    slot = 0
    for platform in order:
        for slug, ep in eps:
            tgt = f"{lang}.{platform}"
            rec = states[slug]["targets"].get(tgt) or {}
            if not rec.get("id") or rec["id"] not in queued:
                continue
            when = post.NOW + dt.timedelta(minutes=first + gap * slot)
            slot += 1
            due = when.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            inp = {"id": rec["id"], "text": post.caption_for(cfg, ep, lang, platform), "schedulingType": "automatic",
                   "assets": acc.video_assets(post.media_url(cfg, ep["video"][lang]), platform, ep.get("cover_ms", 0)), "mode": "customScheduled",
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
                post.log(f"{slug} {tgt}: moved to {when:%H:%M} UTC")
            except (BufferError, RuntimeError) as e:
                post.log(f"{slug} {tgt}: NOT moved: {str(e)[:300]}")
    for slug, st in states.items():
        post.save_state(slug, st)
    with open(os.path.join(post.ROOT, "state", "last-run.md"), "w", encoding="utf-8") as f:
        f.write(f"# Move-up run {post.NOW.isoformat(timespec='seconds')}\n\n" + "\n".join(f"- {m}" for m in post.LOG) + "\n")


if __name__ == "__main__":
    main()
