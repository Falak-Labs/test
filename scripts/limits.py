"""Print Buffer's daily posting limits and each channel's time zone (read-only; no secrets printed).

    python scripts/limits.py            (tools.yml cmd=limits)

Added Nov 19 2026: Buffer started refusing YouTube posts with "You have already scheduled the maximum number of posts
YouTube allows in a day (2)" / "The daily posting limit for this channel has been reached!".
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import Buffer, BufferError, unwrap  # noqa: E402


def fields(buf, name, kind="fields"):
    return [(f["name"], unwrap(f["type"]).get("name"), unwrap(f["type"]).get("kind")) for f in buf.type(name).get(kind) or []]


for lang, var in (("en", "BUFFER_KEY_EN"), ("ar", "BUFFER_KEY_AR")):
    key = os.environ.get(var, "").strip()
    if not key:
        print(f"{lang}: no key")
        continue
    try:
        buf = Buffer(key, lang)
        qf = buf.field("Query", "dailyPostingLimits")
        in_name = unwrap(qf["args"][0]["type"])["name"] if qf and qf.get("args") else None
        out_name = unwrap(qf["type"])["name"] if qf else None
        in_f = fields(buf, in_name, "inputFields") if in_name else []
        out_f = fields(buf, out_name) if out_name else []
        print(f"{lang}: {in_name} {in_f}")
        print(f"{lang}: {out_name} {out_f}")
        ch_names = {f[0] for f in fields(buf, "Channel")}
        want = [f for f in ("id", "name", "service", "timezone", "isQueuePaused", "isDisconnected") if f in ch_names]
        for org in buf.organizations():
            chans = buf.q('query { channels(input: { organizationId: "%s" }) { %s } }' % (org["id"], " ".join(want)))["channels"]
            for ch in chans:
                print(f"{lang}: channel " + ", ".join(f"{k}={ch.get(k)}" for k in want if k != "id"))
            if not in_name:
                continue
            sel = buf.selection(out_name, None) or "__typename"
            ids = [ch["id"] for ch in chans]
            names = {f[0] for f in in_f}
            today = dt.datetime.now(dt.timezone.utc).date()
            tries = []
            base = {}
            if "organizationId" in names:
                base["organizationId"] = org["id"]
            if "channelIds" in names:
                base["channelIds"] = ids
            date_key = next((n for n in ("date", "day", "dates", "days") if n in names), None)
            if date_key:
                for d in (today, today + dt.timedelta(days=1)):
                    v = [d.isoformat()] if date_key.endswith("s") else d.isoformat()
                    tries.append(dict(base, **{date_key: v}))
            else:
                tries.append(base)
            for inp in tries:
                try:
                    d = buf.q("query($i: %s!) { dailyPostingLimits(input: $i) { %s } }" % (in_name, sel), {"i": inp})
                    shown = {k: (v if k != "channelIds" else "[%d channels]" % len(v)) for k, v in inp.items()
                             if k != "organizationId"}
                    print(f"{lang}: dailyPostingLimits {json.dumps(shown)}")
                    for row in d["dailyPostingLimits"]:
                        cid = str(row.get("channelId") or "")
                        svc = next((c.get("service") for c in chans if c["id"] == cid), "")
                        print(f"   {svc} " + json.dumps({k: v for k, v in row.items() if k != "channelId"}, ensure_ascii=False))
                except BufferError as e:
                    print(f"{lang}: dailyPostingLimits error: {str(e)[:400]}")
        print(f"{lang}: {buf.calls} API calls; allowance header: {Buffer.quota.get(lang, '?')}")
    except BufferError as e:
        print(f"{lang}: Buffer error: {str(e)[:500]}")
