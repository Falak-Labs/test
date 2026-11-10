"""Print Buffer's mutations and the input types they take (no secrets printed)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import Buffer, unwrap  # noqa: E402


def show_input(buf, name, depth=0):
    t = buf.type(name)
    for f in t.get("inputFields") or []:
        ft = unwrap(f["type"])
        print("    " * (depth + 2) + f"{f['name']}: {ft['name']} ({ft['kind']})")
        if ft["kind"] == "INPUT_OBJECT" and depth < 2:
            show_input(buf, ft["name"], depth + 1)
        elif ft["kind"] == "ENUM":
            print("    " * (depth + 3) + "= " + ", ".join(buf.enum_values(ft["name"])))


key = os.environ.get("BUFFER_KEY_EN", "").strip()
buf = Buffer(key, "en")
for f in buf.type("Mutation").get("fields") or []:
    args = ", ".join(f"{a['name']}: {unwrap(a['type'])['name']}" for a in f.get("args") or [])
    ret = unwrap(f["type"])["name"]
    print(f"{f['name']}({args}) -> {ret}")
    if any(w in f["name"].lower() for w in ("post", "share", "publish", "queue")):
        for a in f.get("args") or []:
            at = unwrap(a["type"])
            if at["kind"] == "INPUT_OBJECT":
                show_input(buf, at["name"])
        members = [p["name"] for p in buf.type(ret).get("possibleTypes") or []]
        if members:
            print("        returns one of: " + ", ".join(members))
