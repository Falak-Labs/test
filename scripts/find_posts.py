"""Which Buffer status each of our posts has, asked one status at a time (diagnostics; changes nothing in Buffer).

    python scripts/find_posts.py <lang> <target> [<target> ...]      e.g.  en en.youtube en.instagram
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
from buffer import unwrap  # noqa: E402


def main():
    lang, targets = sys.argv[1], set(sys.argv[2:])
    cfg = post.load_yaml(os.path.join(post.ROOT, "config.yml"))
    acc = post.Account(os.environ[cfg["keys"][lang]].strip(), lang)
    buf = acc.buf
    pf = buf.field("Query", "posts")
    in_type = unwrap(next(a for a in pf["args"] if a["name"] == "input")["type"])["name"]
    sf = buf.input_field(unwrap(buf.input_field(in_type, "filter")["type"])["name"], "status")
    values = buf.enum_values(unwrap(sf["type"])["name"])
    print("Buffer post statuses:", values)
    ours = {}
    for fn in sorted(os.listdir(os.path.join(post.ROOT, "state"))):
        if fn.startswith("ep") and fn.endswith(".json"):
            for tgt, rec in post.load_state(fn[:-5])["targets"].items():
                if tgt in targets and rec.get("id"):
                    ours[rec["id"]] = f"{fn[:-5]} {tgt}"
    found = {}
    for org in {ch["organizationId"] for ch in acc.all_channels}:
        for v in values:
            nodes = buf.posts(org, [v])
            hit = [ours[n["id"]] for n in nodes if n.get("id") in ours]
            for n in nodes:
                if n.get("id") in ours:
                    found[n["id"]] = v
            print(f"{v}: {len(nodes)} posts, ours: {len(hit)}")
    for pid, name in sorted(ours.items(), key=lambda kv: kv[1]):
        print(f"  {name}: {found.get(pid, 'NOT FOUND in any status')}")


if __name__ == "__main__":
    main()
