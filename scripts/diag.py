"""Print each language's Buffer channels and every post Buffer lists (any status). No secrets printed."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import Buffer, BufferError, unwrap  # noqa: E402

for lang, var in (("en", "BUFFER_KEY_EN"), ("ar", "BUFFER_KEY_AR")):
    key = os.environ.get(var, "").strip()
    if not key:
        print(f"{lang}: no key")
        continue
    try:
        buf = Buffer(key, lang)
        ch_fields = [f["name"] for f in buf.type("Channel").get("fields") or []]
        print(f"{lang}: Channel fields: {', '.join(ch_fields)}")
        want = [f for f in ("id", "name", "displayName", "service", "isQueuePaused", "isDisconnected", "isLocked", "type",
                            "serviceId", "createdAt") if f in ch_fields]
        print(f"{lang}: PostStatus values: {', '.join(buf.enum_values('PostStatus'))}")
        for org in buf.organizations():
            d = buf.q('query { channels(input: { organizationId: "%s" }) { %s } }' % (org["id"], " ".join(want)))
            for ch in d["channels"]:
                print(f"{lang}: channel " + ", ".join(f"{k}={ch.get(k)}" for k in want if k != "id") + f" id=...{str(ch.get('id'))[-6:]}")
            posts = buf.posts(org["id"], buf.enum_values("PostStatus"))
            print(f"{lang}: {len(posts)} posts listed")
            for p in sorted(posts, key=lambda p: str(p.get("dueAt"))):
                print(f"   {p.get('channelService') or (p.get('channel') or {}).get('service')} {p.get('status')} due {p.get('dueAt')} "
                      f"sent {p.get('sentAt')} id ...{str(p.get('id'))[-6:]} {str(p.get('externalLink') or '')[:70]} {str(p.get('error') or '')[:120]}")
    except BufferError as e:
        print(f"{lang}: Buffer error: {str(e)[:500]}")
