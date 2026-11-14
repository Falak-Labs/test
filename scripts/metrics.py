"""Views, likes, comments and shares of every post this repo made, as Buffer reports them (changes nothing in Buffer).

    python scripts/metrics.py

Writes state/metrics.json ({generated, channels, posts: {slug: {target: {...}}}}) and prints one row per post plus
totals per channel. Buffer refreshes post metrics on its own schedule (metricsUpdatedAt says when).
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
from buffer import Buffer, BufferError, unwrap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ours():
    """Buffer post id -> (slug, target) from state/."""
    out = {}
    for fn in sorted(os.listdir(os.path.join(ROOT, "state"))):
        if fn.startswith("ep") and fn.endswith(".json"):
            for tgt, rec in json.load(open(os.path.join(ROOT, "state", fn)))["targets"].items():
                if rec.get("id"):
                    out[rec["id"]] = (fn[:-5], tgt)
    return out


def metric_map(node):
    """Buffer's metrics list -> {name: value} (whatever names and value fields the API uses)."""
    m = {}
    for item in node.get("metrics") or []:
        if not isinstance(item, dict):
            continue
        name = item.get("type") or item.get("name") or item.get("key") or item.get("metric")
        val = next((item[k] for k in ("value", "count", "total", "amount") if k in item and item[k] is not None), None)
        if name is not None:
            m[str(name).lower()] = val
    return m


def main():
    cfg = post.load_yaml(os.path.join(ROOT, "config.yml"))
    ids = ours()
    res = {"generated": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), "channels": {}, "posts": {}, "metric_fields": None}
    for lang in ("en", "ar"):
        key = os.environ.get(cfg["keys"][lang], "").strip()
        if not key:
            print(f"{lang}: no key")
            continue
        buf = Buffer(key)
        try:
            pm = unwrap(buf.field("Post", "metrics")["type"])["name"] if buf.field("Post", "metrics") else None
            if pm and res["metric_fields"] is None:
                res["metric_fields"] = buf.selection(pm, None)
                print("PostMetric fields:", res["metric_fields"])
            for org in buf.organizations():
                sel = buf.selection("Channel", {"id", "service", "name", "displayName", "metadata"})
                try:
                    chans = buf.q('query { channels(input: { organizationId: "%s" }) { %s } }' % (org["id"], sel))["channels"]
                except BufferError as e:
                    print(f"{lang}: channels: {e}")
                    chans = []
                for ch in chans:
                    res["channels"][f"{lang}.{ch.get('service')}"] = ch
                for node in buf.posts(org["id"], ["sent"], extra=("metrics", "metricsUpdatedAt")):
                    slug, tgt = ids.get(node["id"], (None, None))
                    if not slug:
                        continue
                    res["posts"].setdefault(slug, {})[tgt] = {
                        "sentAt": node.get("sentAt"), "metricsUpdatedAt": node.get("metricsUpdatedAt"),
                        "metrics": metric_map(node), "raw": node.get("metrics"), "link": node.get("externalLink")}
        except BufferError as e:
            print(f"{lang}: Buffer error: {e}")
    json.dump(res, open(os.path.join(ROOT, "state", "metrics.json"), "w"), indent=1, ensure_ascii=False)
    names = sorted({k for p in res["posts"].values() for t in p.values() for k in t["metrics"]})
    print("metrics:", names)
    print("| post | target | sent | " + " | ".join(names) + " | updated |")
    tot = {}
    for slug in sorted(res["posts"]):
        for tgt, r in sorted(res["posts"][slug].items()):
            row = [str(r["metrics"].get(n, "")) for n in names]
            print(f"| {slug} | {tgt} | {(r['sentAt'] or '')[:16]} | " + " | ".join(row) + f" | {(r['metricsUpdatedAt'] or '')[:16]} |")
            t = tot.setdefault(tgt, {})
            for n in names:
                v = r["metrics"].get(n)
                if isinstance(v, (int, float)):
                    t[n] = t.get(n, 0) + v
    print("totals:")
    for tgt, t in sorted(tot.items()):
        print(" ", tgt, t)
    print("channels:")
    for k, ch in res["channels"].items():
        print(" ", k, json.dumps(ch.get("metadata"), ensure_ascii=False)[:300])


if __name__ == "__main__":
    main()
