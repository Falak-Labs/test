"""Print the video, cover frame and time Buffer holds for our scheduled posts (diagnostics; changes nothing in Buffer).

    python scripts/show_assets.py <lang> <slug> [<slug> ...]      e.g.  en ep26-tower ep27-tunnel
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post  # noqa: E402
from buffer import unwrap  # noqa: E402


def scalar_fields(buf, type_name):
    out = []
    for f in buf.type(type_name).get("fields") or []:
        t = unwrap(f["type"])
        if t["kind"] in ("SCALAR", "ENUM"):
            out.append(f["name"])
        elif t["kind"] == "OBJECT" and f["name"] in ("metadata", "video", "thumbnail"):
            inner = [g["name"] for g in buf.type(t["name"]).get("fields") or [] if unwrap(g["type"])["kind"] in ("SCALAR", "ENUM")]
            if inner:
                out.append(f["name"] + " { " + " ".join(inner) + " }")
    return out


def main():
    lang, slugs = sys.argv[1], sys.argv[2:]
    cfg = post.load_yaml(os.path.join(post.ROOT, "config.yml"))
    acc = post.Account(os.environ[cfg["keys"][lang]].strip(), lang)
    buf = acc.buf
    at = buf.type("Asset")
    if at.get("possibleTypes"):
        sel = "__typename " + " ".join(f"... on {p['name']} {{ {' '.join(scalar_fields(buf, p['name']))} }}"
                                       for p in at["possibleTypes"] if scalar_fields(buf, p["name"]))
    else:
        sel = "__typename " + " ".join(scalar_fields(buf, "Asset"))
    pf = buf.field("Query", "post")
    in_type = unwrap(next(a for a in pf["args"] if a["name"] == "input")["type"])["name"]
    for slug in slugs:
        for tgt, rec in post.load_state(slug)["targets"].items():
            if not tgt.startswith(lang + ".") or not rec.get("id"):
                continue
            d = buf.q("query($i: %s!) { post(input: $i) { id status dueAt assets { %s } } }" % (in_type, sel),
                      {"i": {"id": rec["id"]}})
            p = d.get("post") or {}
            print(f"{slug} {tgt}: {p.get('status')} due {p.get('dueAt')}")
            for a in p.get("assets") or []:
                print("   ", json.dumps(a, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
