"""Download the free Palestinian Arabic voice (Sofelia TTS 82M, Apache-2.0) and pack it as sofelia.zip.
Uses only Python's standard library, so it runs without pip or a virtual environment:
    python3 fetch_sofelia.py
Then attach sofelia.zip (about 330 MB) in the chat.
"""
import json
import os
import time
import urllib.request
import zipfile

REPO = "hamdallah/Sofelia-TTS-82M"
OUT = "sofelia-tts-82m"
SKIP_EXT = (".wav", ".mp3", ".flac", ".ogg", ".m4a", ".png", ".jpg", ".jpeg", ".gif", ".webp")


def fetch(url, dest=None, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "sofelia-fetch/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                if dest is None:
                    return r.read()
                total = int(r.headers.get("Content-Length") or 0)
                done = 0
                with open(dest + ".part", "wb") as fh:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        fh.write(chunk)
                        done += len(chunk)
                        if total > 5 << 20:
                            print(f"\r   {done / 1e6:7.1f} / {total / 1e6:.1f} MB", end="", flush=True)
                if total and done != total:
                    raise IOError(f"short read {done}/{total}")
                os.replace(dest + ".part", dest)
                if total > 5 << 20:
                    print()
                return None
        except Exception as e:
            print("   retry", i + 1, "->", e)
            time.sleep(3 * (i + 1))
    raise SystemExit("Gave up on " + url)


info = json.loads(fetch(f"https://huggingface.co/api/models/{REPO}"))
files = [s["rfilename"] for s in info["siblings"]]
for f in files:
    if f == ".gitattributes" or f.lower().endswith(SKIP_EXT):
        continue
    dest = os.path.join(OUT, f)
    if os.path.exists(dest):
        continue
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    print("downloading", f)
    fetch(f"https://huggingface.co/{REPO}/resolve/main/{f}", dest)

with zipfile.ZipFile("sofelia.zip", "w", zipfile.ZIP_STORED) as z:
    for root, _, names in os.walk(OUT):
        for n in names:
            z.write(os.path.join(root, n))
print("done: sofelia.zip,", round(os.path.getsize("sofelia.zip") / 1e6, 1), "MB")
