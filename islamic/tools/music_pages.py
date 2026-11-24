"""Download tracks from their Pixabay pages (Pixabay Content License: free for commercial use in videos, no credit
needed) on the GitHub runner. Finds the audio file linked in the page, cuts it to at most 240 s, saves a 160 kbps
mp3 and lists source and licence in index.json.
  python3 islamic/tools/music_pages.py islamic/music/candidates name=https://pixabay.com/music/...-123456/ ...
"""
import json, os, re, subprocess, sys, urllib.request

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
idx_p = os.path.join(out, "index.json")
index = json.load(open(idx_p)) if os.path.exists(idx_p) else {}
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
     "Accept": "text/html,application/xhtml+xml,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9"}


def get(url, ref=None):
    h = dict(H, **({"Referer": ref} if ref else {}))
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
        return r.read()


for pair in sys.argv[2:]:
    name, page = pair.split("=", 1)
    if page.startswith("https://cdn.pixabay.com/"):   # direct file link (read from the track page in a browser)
        html, urls, title = "", [page], page.rsplit("filename=", 1)[-1]
        page = page
    else:
        try:
            html = get(page).decode("utf-8", "replace")
        except Exception as e:
            print(f"{name}: page failed: {e}"); continue
        urls = re.findall(r'https://cdn\.pixabay\.com/(?:download/)?audio/[^"\'\s<>]+?\.mp3', html.replace("\\/", "/"))
        title = (re.search(r"<title>([^<]+)</title>", html) or [None, ""])[1].strip()
    if not urls:
        print(f"{name}: no audio link in page ({len(html)} bytes, title {title!r})"); continue
    src = urls[0]
    tmp = os.path.join(out, "_dl.mp3")
    try:
        open(tmp, "wb").write(get(src, ref=page))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-t", "240", "-ar", "44100", "-b:a", "160k",
                        os.path.join(out, name + ".mp3")], check=True)
    except Exception as e:
        print(f"{name}: download failed: {e} ({src})"); continue
    finally:
        if os.path.exists(tmp): os.remove(tmp)
    index[page] = {"file": name + ".mp3", "title": title, "source": "pixabay", "page": page, "audio_url": src,
                   "license": "Pixabay Content License", "license_url": "https://pixabay.com/service/license-summary/"}
    print(f"{name}: kept ({title})")
json.dump(index, open(idx_p, "w"), ensure_ascii=False, indent=1)
