"""Put chosen posts back in Buffer's queue at given times. Edits the existing Buffer post (no duplicates), so it also
works for a post that failed; a post Buffer already sent is left alone.

    python scripts/requeue.py <lang> <platform> <slug>=<UTC time> [<slug>=<UTC time> ...]
    python scripts/requeue.py ar tiktok ep07-castle=2026-11-10T16:50:00Z ep08-claw=2026-11-10T17:30:00Z
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
from buffer import BufferError  # noqa: E402


def main():
    lang, platform = sys.argv[1], sys.argv[2]
    plan = dict(a.split("=", 1) for a in sys.argv[3:])
    cfg = post.load_yaml(os.path.join(post.ROOT, "config.yml"))
    key = os.environ.get(cfg["keys"][lang], "").strip()
    if not key:
        sys.exit(f"no Buffer key for {lang}")
    acc = post.Account(key, lang)
    sent = set()
    for org in {ch["organizationId"] for ch in acc.all_channels}:
        sent |= {n.get("id") for n in acc.buf.posts(org, ["sent"])}
    tgt = f"{lang}.{platform}"
    for slug, when_s in plan.items():
        ep = post.load_yaml(os.path.join(post.ROOT, "posts", slug + ".yml"))
        st = post.load_state(slug)
        rec = st["targets"].get(tgt) or {}
        when = post.parse_utc(when_s)
        if not rec.get("id"):
            post.log(f"{slug} {tgt}: no Buffer post to move")
            continue
        if rec["id"] in sent:
            post.log(f"{slug} {tgt}: already sent, left alone")
            continue
        due = when.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        inp = {"id": rec["id"], "text": post.caption_for(cfg, ep, lang, platform), "schedulingType": "automatic",
               "assets": acc.video_assets(post.media_url(cfg, ep["video"][lang]), platform, ep.get("cover_ms", 0)), "mode": "customScheduled", "dueAt": due}
        if platform == "youtube":
            inp["metadata"] = {"youtube": {"title": ep[lang]["title"][:100], "categoryId": str(cfg["youtube"]["categoryId"]),
                                           "madeForKids": bool(cfg["youtube"].get("madeForKids", False)),
                                           "notifySubscribers": True}}
        elif platform == "instagram":
            inp["metadata"] = {"instagram": {"type": acc.reel(), "shouldShareToFeed": True}}
        try:
            p = acc.buf.edit_post(inp)
            rec.update({"dueAt": p.get("dueAt") or due, "status": p.get("status") or "scheduled", "mode": "customScheduled",
                        "moved": post.NOW.isoformat(timespec="seconds")})
            post.log(f"{slug} {tgt}: queued for {when:%H:%M} UTC (Buffer status now: {p.get('status')})")
        except (BufferError, RuntimeError) as e:
            post.log(f"{slug} {tgt}: NOT queued: {str(e)[:300]}")
        post.save_state(slug, st)
    with open(os.path.join(post.ROOT, "state", "last-run.md"), "w", encoding="utf-8") as f:
        f.write(f"# Requeue run {post.NOW.isoformat(timespec='seconds')}\n\n" + "\n".join(f"- {m}" for m in post.LOG) + "\n")


if __name__ == "__main__":
    main()
