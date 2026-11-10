"""Write state/status.md: every post this repo created, with Buffer's current status (scheduled / sent / error).

    python scripts/status.py [--wait-now MINUTES]

--wait-now keeps checking posts that were sent "now" (tests) until they are sent or failed, up to MINUTES.
"""
import datetime as dt
import json
import os
import sys
import time

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import Buffer, BufferError  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def flat(node):
    out = {}
    for k, v in node.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                out[f"{k}.{k2}"] = v2
        else:
            out[k] = v
    return out


def snapshot(accounts):
    by_id = {}
    for lang, buf in accounts.items():
        try:
            for org in buf.organizations():
                for node in buf.posts(org["id"], ["scheduled", "sending", "sent", "error", "failed"]):
                    by_id[node["id"]] = (lang, flat(node))
        except BufferError as e:
            print(f"{lang}: Buffer error: {e}")
    return by_id


def main():
    wait = 0
    if "--wait-now" in sys.argv:
        wait = float(sys.argv[sys.argv.index("--wait-now") + 1])
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yml"), encoding="utf-8"))
    accounts = {lang: Buffer(os.environ[var].strip(), lang) for lang, var in cfg["keys"].items()
                if os.environ.get(var, "").strip()}
    states = {}
    for fn in sorted(os.listdir(os.path.join(ROOT, "state"))):
        if fn.endswith(".json"):
            states[fn[:-5]] = json.load(open(os.path.join(ROOT, "state", fn), encoding="utf-8"))
    deadline = time.time() + wait * 60
    while True:
        by_id = snapshot(accounts)
        pending_now = [t for st in states.values() for t in st["targets"].values()
                       if t.get("mode") == "shareNow" or (t.get("mode") == "customScheduled" and t.get("dueAt") and
                       t["dueAt"] <= (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S"))]
        unsettled = [t for t in pending_now if t.get("id") and by_id.get(t["id"], (None, {}))[1].get("status")
                     not in ("sent", "error", "failed")]
        if not unsettled or time.time() > deadline:
            break
        print(f"waiting for {len(unsettled)} post(s) going out now...")
        time.sleep(30)
    rows = []
    for slug, st in states.items():
        for tgt, t in sorted(st["targets"].items()):
            if not t.get("id"):
                rows.append((slug, tgt, "not created", t.get("error", "")[:160], ""))
                continue
            lang, node = by_id.get(t["id"], (None, {}))
            status = node.get("status") or "not listed"
            t["status"] = status
            err = node.get("error") or node.get("errorMessage") or node.get("error.message") or ""
            link = node.get("externalLink") or node.get("serviceLink") or ""
            when = node.get("sentAt") or node.get("dueAt") or t.get("dueAt") or ""
            rows.append((slug, tgt, status, str(err)[:160], f"{when} {link}".strip()))
        with open(os.path.join(ROOT, "state", slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=1)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = [f"# Post status {now}", "", "| Episode | Target | Status | Error | When / link |", "|---|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in rows]
    with open(os.path.join(ROOT, "state", "status.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
