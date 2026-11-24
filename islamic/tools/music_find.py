"""Find and download open-licence audio for background beds (runs on the GitHub runner, which has normal internet).

Searches Openverse (Freesound, Wikimedia Commons, Jamendo, ccMixter ...) and keeps only licences that allow use in
monetised videos with remixing: CC0, Public Domain Mark, CC BY (credit goes in the description). NC, ND and SA are
dropped. Each kept file is cut to at most 180 s, saved as 128 kbps mp3, and listed with its source and licence in
index.json.
  python3 islamic/tools/music_find.py islamic/music/candidates "query one" "query two" ...
"""
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request

out = sys.argv[1]; queries = sys.argv[2:]
os.makedirs(out, exist_ok=True)
idx_p = os.path.join(out, "index.json")
index = json.load(open(idx_p)) if os.path.exists(idx_p) else {}
UA = {"User-Agent": "Falak-Labs music finder (github.com/Falak-Labs/test)"}


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


kept = 0
for q in queries:
    params = {"q": q, "license": "cc0,pdm,by", "page_size": 20, "mature": "false"}
    url = "https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode(params)
    try:
        res = json.loads(get(url))["results"]
    except Exception as e:
        print(f"search failed for {q!r}: {e}"); continue
    print(f"{q!r}: {len(res)} results")
    for r in res:
        dur = (r.get("duration") or 0) / 1000
        lic = (r.get("license") or "").lower()
        if lic not in ("cc0", "pdm", "by") or dur and dur < 20:
            continue
        rid = r["id"]
        if rid in index:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", (r.get("title") or "untitled").lower()).strip("-")[:40] or "untitled"
        name = f"{r.get('source','x')}_{slug}_{rid[:6]}.mp3"
        tmp = os.path.join(out, "_dl")
        try:
            open(tmp, "wb").write(get(r["url"], timeout=120))
            if os.path.getsize(tmp) > 60_000_000:
                raise RuntimeError("too big")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-t", "180", "-ac", "2", "-ar", "44100",
                            "-b:a", "128k", os.path.join(out, name)], check=True)
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                      os.path.join(out, name)], capture_output=True, text=True).stdout.strip() or 0)
        except Exception as e:
            print(f"  skip {name}: {e}"); continue
        finally:
            if os.path.exists(tmp): os.remove(tmp)
        index[rid] = {"file": name, "query": q, "title": r.get("title"), "creator": r.get("creator"),
                      "creator_url": r.get("creator_url"), "license": lic, "license_version": r.get("license_version"),
                      "license_url": r.get("license_url"), "source": r.get("source"), "page": r.get("foreign_landing_url"),
                      "attribution": r.get("attribution"), "tags": [t.get("name") for t in (r.get("tags") or [])][:15],
                      "duration_s": round(d, 1)}
        kept += 1
        print(f"  kept {name} ({lic}, {d:.0f}s) {r.get('foreign_landing_url')}")
        time.sleep(0.5)
    json.dump(index, open(idx_p, "w"), ensure_ascii=False, indent=1)
    time.sleep(1.5)
print(f"kept {kept} new files, {len(index)} in total")
