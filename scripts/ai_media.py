"""The owner's AI media library (Higgsfield files kept in the GitHub release "ai-media"). Works from any chat's workspace.

    python3 scripts/ai_media.py list [filter]                 names, sizes and dates of what is kept
    python3 scripts/ai_media.py get <name> [folder]           download one file (default folder: ./ai-media)
    python3 scripts/ai_media.py fetch <name>=<link> ...       have GitHub's runner download Higgsfield links into the
                                                              release (workflow "Fetch media"), wait, and confirm

Uses only the GitHub REST API through `gh api` (gh release download needs GraphQL, which these sessions lack).
"""
import json
import os
import subprocess
import sys
import time

REPO = "Falak-Labs/test"
TAG = "ai-media"


def gh(*args, text=True):
    return subprocess.run(["gh", "api", *args], check=True, capture_output=True, text=text).stdout


def assets():
    try:
        rel = json.loads(gh(f"repos/{REPO}/releases/tags/{TAG}"))
    except subprocess.CalledProcessError:
        return []
    out, page = list(rel.get("assets", [])), 2
    while len(out) >= 30 * (page - 1):                 # the release object lists 30 at most; page through the rest
        more = json.loads(gh(f"repos/{REPO}/releases/{rel['id']}/assets?per_page=100&page={page - 1}"))
        if not more:
            break
        known = {a["id"] for a in out}
        out += [a for a in more if a["id"] not in known]
        if len(more) < 100:
            break
        page += 1
    return out


def cmd_list(flt=""):
    for a in sorted(assets(), key=lambda a: a["name"]):
        if flt in a["name"]:
            print(f"{a['name']:<48} {a['size'] / 1e6:7.1f} MB  {a['updated_at'][:16]}")


def cmd_get(name, folder="ai-media"):
    a = next((a for a in assets() if a["name"] == name), None)
    if not a:
        sys.exit(f"{name}: not in release {TAG}")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    data = subprocess.run(["gh", "api", "-H", "Accept: application/octet-stream", f"repos/{REPO}/releases/assets/{a['id']}"],
                          check=True, capture_output=True).stdout
    open(path, "wb").write(data)
    print(f"{path}  {len(data) / 1e6:.1f} MB")
    return path


def cmd_fetch(pairs):
    names = [p.split("=", 1)[0] for p in pairs]
    before = {a["name"]: a["updated_at"] for a in assets()}
    subprocess.run(["gh", "api", "-X", "POST", f"repos/{REPO}/actions/workflows/fetch-media.yml/dispatches",
                    "-f", "ref=main", "-f", "inputs[items]=" + " ".join(pairs)], check=True)
    for _ in range(40):
        time.sleep(15)
        now = {a["name"]: a["updated_at"] for a in assets()}
        if all(n in now and now[n] != before.get(n) for n in names):
            print("kept:", ", ".join(names))
            return
    sys.exit("not kept after 10 minutes: look at the latest run of the workflow Fetch media")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    c, rest = sys.argv[1], sys.argv[2:]
    if c == "list":
        cmd_list(*rest[:1])
    elif c == "get":
        cmd_get(*rest[:2])
    elif c == "fetch":
        cmd_fetch(rest)
    else:
        sys.exit(__doc__)
